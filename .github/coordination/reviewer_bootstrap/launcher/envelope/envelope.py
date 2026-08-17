"""The one public interface of RA-04A: an immutable launch envelope, built from sealed inputs.

A caller hands over a trusted controller directory and the name of a sealed plan inside it, and
receives a structured description of a Claude Reviewer launch: executable, argument tuple, working
directory, child environment, stdin binding and evidence digests.  Nothing is spawned, claimed,
fenced, delegated or written to GitHub here, and the module holds no capability to do any of it.

Three shapes of the interface are deliberate:

  * The candidate checkout is derived from `__file__`, not supplied.  A caller who may name the
    tree that inputs must stay outside of can name a different tree.
  * The permission mode, the argument positions and the automatic-memory flag are module
    constants.  The plan may only AGREE with them; it can never contribute them.
  * The returned object is sealed.  It cannot be constructed, replaced, copied or subclassed into
    existence, so an envelope that reaches RA-04B was produced by this builder or does not exist.

The prompt is bound as stdin rather than as an argument.  A prompt on the command line is a prompt
that has to be quoted by somebody, and every place it gets quoted is a place it gets quoted wrong.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from . import attestation
from .arguments import PERMISSION_MODE, audit_argument_vector, build_argument_vector
from .environment import build_child_environment, environment_evidence
from .errors import reject
from .inventory import envelope_inventory
from .paths import CANDIDATE_ROOT, admit_external_path, inspect_directory
from .paths import inspect_sealed_file
from .sealed import (
    MAX_DOCUMENT_BYTES,
    MAX_EXECUTABLE_BYTES,
    MAX_PLAN_BYTES,
    SealedInput,
    digest,
    expected_digest,
    identity_of,
    load_sealed_input,
    read_sealed_bytes,
    reverify,
)

SCHEMA_VERSION = 2

_TOP_KEYS = frozenset(
    {
        "schema_version",
        "permission_mode",
        "binding",
        "trusted_roots",
        "executable",
        "settings",
        "prompt",
        "working_directory",
        "environment",
    }
)
_FILE_KEYS = frozenset({"path", "sha256"})
_BINDING_KEYS = frozenset({"artifact", "source_pin_sha256", "run_id", "head", "tree"})

OID40 = re.compile(r"[0-9a-f]{40}\Z")
SAFE_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


@dataclass(frozen=True)
class LaunchEnvelope:
    """Immutable launch description whose authenticity is decided outside itself.

    There is deliberately no `is_sealed()`.  A boolean the object answers about its own
    trustworthiness is worth exactly as much as the object, and an instance forged with
    `object.__new__` answered it happily.  Use `verify_launch_envelope`, which consults a private
    record this instance cannot reach and then re-reads the controller's sealed inputs.
    """

    schema_version: int
    executable: str
    arguments: tuple[str, ...]
    working_directory: str
    stdin_path: str
    environment: Mapping[str, str]
    sealed_inputs: tuple[SealedInput, ...]
    inventory_digest: str
    payload_sha256: str
    binding_sha256: str
    evidence_json: str
    evidence_sha256: str

    def __post_init__(self):
        raise reject("envelope_unattested", "a launch envelope must come from build_launch_envelope")

    def __copy__(self):
        raise reject("envelope_unattested", "a launch envelope cannot be copied")

    def __deepcopy__(self, memo):
        raise reject("envelope_unattested", "a launch envelope cannot be copied")

    def __reduce__(self):
        # Pickle would rebuild a twin through __init__ or __new__ with no attestation behind it.
        raise reject("envelope_unattested", "a launch envelope cannot be serialised")

    def as_evidence(self) -> dict[str, object]:
        """A fresh, JSON-shaped copy of the retained evidence.

        Decoded on every call on purpose: handing out the stored mapping would hand out a handle
        on the envelope's own state, and "immutable except for the part everyone reads" is not
        immutable.
        """

        return json.loads(self.evidence_json)


def _payload_of(envelope: LaunchEnvelope) -> dict[str, object]:
    """The complete payload, read back from the instance as it stands right now."""

    return {
        "schema_version": envelope.schema_version,
        "executable": envelope.executable,
        "arguments": list(envelope.arguments),
        "working_directory": envelope.working_directory,
        "stdin_path": envelope.stdin_path,
        "environment": dict(envelope.environment),
        "sealed_inputs": [item.as_evidence() for item in envelope.sealed_inputs],
        "inventory_digest": envelope.inventory_digest,
        "binding_sha256": envelope.binding_sha256,
    }


def verify_launch_envelope(envelope: object) -> dict[str, object]:
    """Verify a launch envelope against the controller-owned sealed inputs.

    Four independent questions, none of which the envelope gets to answer about itself:

    1. is this the exact class, not a subclass that redefined the answers;
    2. did the builder attest it, according to a record kept outside the instance;
    3. does the payload STILL hash to what was attested, so no field was replaced afterwards;
    4. do the controller's files on disk still match the bytes and identity that were verified.

    Only the fourth touches the filesystem, and it is the one that makes the first three mean
    something: without it, verification would only prove the envelope agrees with itself.
    """

    if type(envelope) is not LaunchEnvelope:
        raise reject("envelope_unattested", "this object is not a launch envelope")
    recorded = attestation.attested_digest(envelope)
    if recorded is None:
        raise reject("envelope_unattested", "this envelope was never produced by the builder")
    current = attestation.payload_digest(_payload_of(envelope))
    if current != recorded or current != envelope.payload_sha256:
        raise reject("envelope_payload_mismatch", "the envelope payload changed after it was built")
    for sealed in envelope.sealed_inputs:
        reverify(sealed)
    binding = json.loads(envelope.evidence_json)["binding"]
    if attestation.payload_digest(binding) != envelope.binding_sha256:
        raise reject("envelope_payload_mismatch", "the identity binding does not match its digest")
    return {
        "verified": True,
        "payload_sha256": current,
        "binding": binding,
        "binding_sha256": envelope.binding_sha256,
        "sealed_input_count": len(envelope.sealed_inputs),
    }


def _attested_envelope(**fields: object) -> LaunchEnvelope:
    """Build the instance and record its payload digest OUTSIDE it, in one place.

    The digest is derived from the payload as it stands once every field is set, so this helper
    cannot mint authority for data that did not come through the checks above it: whatever it is
    handed becomes exactly what verification later demands the controller's files still agree
    with, and a fabricated instance that skipped those checks has no record here at all.
    """

    envelope = object.__new__(LaunchEnvelope)
    for name, value in fields.items():
        object.__setattr__(envelope, name, value)
    digest_value = attestation.payload_digest(_payload_of(envelope))
    object.__setattr__(envelope, "payload_sha256", digest_value)
    attestation.attest(envelope, digest_value)
    return envelope


def _strict_object(pairs):
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON object key")
        value[key] = item
    return value


def _exact_keys(value: object, keys: frozenset[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise reject("plan_schema", "%s must be a JSON object with string keys" % label)
    if frozenset(value) != keys:
        raise reject("plan_schema", "%s has missing or extra keys" % label)
    return value


def _plan_target(controller_root: object, plan_name: object) -> pathlib.Path:
    """Locate the plan without letting the locator itself become the escape."""

    if not isinstance(controller_root, (str, pathlib.PurePath)):
        raise reject("plan_path", "the controller root must be a path")
    root = pathlib.Path(controller_root)
    if not root.is_absolute():
        raise reject("plan_path", "the controller root must be absolute")
    if not isinstance(plan_name, str) or not plan_name:
        raise reject("plan_path", "the plan name must be a non-empty string")
    if "\\" in plan_name or "/" in plan_name:
        raise reject("plan_path", "the plan name must be a direct child of the controller root")
    if plan_name in (".", ".."):
        raise reject("plan_path", "the plan name must not be a directory reference")
    # Lexical join only.  `resolve()` here would follow a link in the controller root before a
    # single lstat had run, which is precisely the ancestry erasure `paths.admit_external_path`
    # exists to prevent.
    lexical_root = pathlib.Path(os.path.normpath(str(root)))
    target = lexical_root / plan_name
    if target.parent != lexical_root:
        raise reject("plan_path", "the plan name resolves outside the controller root")
    return target


def _binding_of(plan: dict[str, object]) -> dict[str, str]:
    """Identity bindings, taken from the sealed plan and nowhere else."""

    binding = _exact_keys(plan["binding"], _BINDING_KEYS, "the plan binding")
    artifact = binding["artifact"]
    run_id = binding["run_id"]
    if not isinstance(artifact, str) or SAFE_IDENTIFIER.fullmatch(artifact) is None:
        raise reject("plan_schema", "the binding artifact name is invalid")
    if not isinstance(run_id, str) or SAFE_IDENTIFIER.fullmatch(run_id) is None:
        raise reject("plan_schema", "the binding run identifier is invalid")
    expected_digest(binding["source_pin_sha256"], "the binding source pin")
    for key in ("head", "tree"):
        value = binding[key]
        if not isinstance(value, str) or OID40.fullmatch(value) is None:
            raise reject("plan_schema", "the binding %s is not an exact object id" % key)
    return {key: binding[key] for key in sorted(_BINDING_KEYS)}


def _trusted_roots_of(plan: dict[str, object]) -> tuple[pathlib.Path, ...]:
    declared = plan["trusted_roots"]
    if not isinstance(declared, list) or not declared or len(declared) > 16:
        raise reject("plan_schema", "the plan must declare one to sixteen trusted roots")
    roots = []
    for entry in declared:
        admitted = admit_external_path(entry, "trusted root", require_readonly_parent=False)
        inspect_directory(admitted, "trusted root")
        roots.append(admitted)
    return tuple(roots)


def _sealed_from_plan(
    section: object,
    label: str,
    *,
    max_bytes: int,
    trusted_roots: tuple[pathlib.Path, ...],
) -> SealedInput:
    value = _exact_keys(section, _FILE_KEYS, label)
    sha256 = expected_digest(value["sha256"], label)
    target = admit_external_path(value["path"], label, trusted_roots=trusted_roots)
    return load_sealed_input(target, label, max_bytes=max_bytes, sha256=sha256)


def build_launch_envelope(controller_root: object, plan_name: object) -> LaunchEnvelope:
    """Build one immutable launch envelope from a sealed controller plan.

    The only inputs are a trusted directory and a file name inside it.  There is no command, no
    environment extra, no trust flag, no pre-computed observation and no callback, because each of
    those would let the caller decide the answer this module exists to compute.
    """

    plan_path = admit_external_path(str(_plan_target(controller_root, plan_name)), "launch plan")
    raw_plan = read_sealed_bytes(plan_path, "launch plan", max_bytes=MAX_PLAN_BYTES)
    plan_sealed = SealedInput(
        label="launch plan",
        path=str(plan_path),
        sha256=digest(raw_plan),
        size=len(raw_plan),
        max_bytes=MAX_PLAN_BYTES,
        content=bytes(raw_plan),
        identity=identity_of(inspect_sealed_file(plan_path, "launch plan", max_bytes=MAX_PLAN_BYTES)),
    )

    try:
        text = raw_plan.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise reject("plan_encoding", "the launch plan must be strict UTF-8") from exc
    try:
        parsed = json.loads(text, object_pairs_hook=_strict_object)
    except ValueError as exc:
        raise reject("plan_schema", "the launch plan is not a single valid JSON object") from exc

    plan = _exact_keys(parsed, _TOP_KEYS, "the launch plan")
    if plan["schema_version"] != SCHEMA_VERSION or isinstance(plan["schema_version"], bool):
        raise reject("plan_schema", "the launch plan schema revision is not supported")
    if plan["permission_mode"] != PERMISSION_MODE:
        # The plan does not supply the mode — it only agrees with it.  Disagreement is a plan
        # written for a different launcher, and running it under this one would silently grant a
        # permission posture nobody authorised.
        raise reject("permission_mode_unsupported", "the plan declares an unsupported permission mode")

    binding = _binding_of(plan)
    trusted_roots = _trusted_roots_of(plan)

    executable = _sealed_from_plan(
        plan["executable"],
        "launcher executable",
        max_bytes=MAX_EXECUTABLE_BYTES,
        trusted_roots=trusted_roots,
    )
    settings = _sealed_from_plan(
        plan["settings"],
        "launcher settings",
        max_bytes=MAX_DOCUMENT_BYTES,
        trusted_roots=trusted_roots,
    )
    prompt = _sealed_from_plan(
        plan["prompt"],
        "reviewer prompt",
        max_bytes=MAX_DOCUMENT_BYTES,
        trusted_roots=trusted_roots,
    )

    working_directory = admit_external_path(
        plan["working_directory"],
        "working directory",
        trusted_roots=trusted_roots,
        require_readonly_parent=False,
    )
    inspect_directory(working_directory, "working directory")

    child_environment = build_child_environment(plan["environment"], trusted_roots)
    arguments = build_argument_vector(executable.path, settings.path)
    argument_audit = audit_argument_vector(arguments)
    measured_inventory = envelope_inventory()

    sealed_inputs = (plan_sealed, executable, settings, prompt)
    # Everything above described the filesystem at the moment it was read.  Read it all again now
    # that the envelope is otherwise complete: a path or content swap performed during assembly
    # has to survive this second look, and it cannot.
    for sealed in sealed_inputs:
        reverify(sealed)

    binding_sha256 = attestation.payload_digest(binding)
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "permission_mode": PERMISSION_MODE,
        "binding": binding,
        "binding_sha256": binding_sha256,
        "trusted_roots": [str(root) for root in trusted_roots],
        "argument_vector": list(arguments),
        "argument_audit": argument_audit,
        "working_directory": str(working_directory),
        "stdin_path": prompt.path,
        "candidate_root": str(CANDIDATE_ROOT),
        "environment": environment_evidence(child_environment),
        "sealed_inputs": [item.as_evidence() for item in sealed_inputs],
        "inventory": {
            "prefix": measured_inventory["prefix"],
            "file_count": measured_inventory["file_count"],
            "digest": measured_inventory["digest"],
            "excluded": measured_inventory["excluded"],
            "files": measured_inventory["files"],
        },
    }
    evidence_json = json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    return _attested_envelope(
        schema_version=SCHEMA_VERSION,
        executable=executable.path,
        arguments=arguments,
        working_directory=str(working_directory),
        stdin_path=prompt.path,
        environment=child_environment,
        sealed_inputs=sealed_inputs,
        inventory_digest=str(measured_inventory["digest"]),
        binding_sha256=binding_sha256,
        evidence_json=evidence_json,
        evidence_sha256=hashlib.sha256(evidence_json.encode("utf-8")).hexdigest(),
    )
