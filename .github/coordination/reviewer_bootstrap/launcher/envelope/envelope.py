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
import pathlib
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from .arguments import PERMISSION_MODE, audit_argument_vector, build_argument_vector
from .environment import build_child_environment, environment_evidence
from .errors import reject
from .inventory import envelope_inventory
from .paths import CANDIDATE_ROOT, admit_external_path, inspect_directory
from .sealed import (
    MAX_DOCUMENT_BYTES,
    MAX_EXECUTABLE_BYTES,
    MAX_PLAN_BYTES,
    SealedInput,
    digest,
    expected_digest,
    load_sealed_input,
    read_sealed_bytes,
    reverify,
)

SCHEMA_VERSION = 1

_TOP_KEYS = frozenset(
    {
        "schema_version",
        "permission_mode",
        "executable",
        "settings",
        "prompt",
        "working_directory",
        "environment",
    }
)
_FILE_KEYS = frozenset({"path", "sha256"})
_SEAL = object()


@dataclass(frozen=True)
class LaunchEnvelope:
    """Immutable launch description; only this module's builder can produce one."""

    schema_version: int
    executable: str
    arguments: tuple[str, ...]
    working_directory: str
    stdin_path: str
    environment: Mapping[str, str]
    sealed_inputs: tuple[SealedInput, ...]
    inventory_digest: str
    evidence_json: str
    evidence_sha256: str
    _seal: object = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        raise reject("envelope_unsealed", "a launch envelope must come from build_launch_envelope")

    def is_sealed(self) -> bool:
        return type(self) is LaunchEnvelope and getattr(self, "_seal", None) is _SEAL

    def __copy__(self):
        raise reject("envelope_unsealed", "a sealed launch envelope cannot be copied")

    def __deepcopy__(self, memo):
        raise reject("envelope_unsealed", "a sealed launch envelope cannot be copied")

    def as_evidence(self) -> dict[str, object]:
        """A fresh, JSON-shaped copy of the retained evidence.

        Decoded on every call on purpose: handing out the stored mapping would hand out a handle
        on the envelope's own state, and "immutable except for the part everyone reads" is not
        immutable.
        """

        return json.loads(self.evidence_json)


def _sealed_envelope(**fields: object) -> LaunchEnvelope:
    envelope = object.__new__(LaunchEnvelope)
    for name, value in fields.items():
        object.__setattr__(envelope, name, value)
    object.__setattr__(envelope, "_seal", _SEAL)
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
    resolved_root = root.resolve()
    target = resolved_root / plan_name
    if target.parent != resolved_root:
        raise reject("plan_path", "the plan name resolves outside the controller root")
    return target


def _sealed_from_plan(section: object, label: str, *, max_bytes: int) -> SealedInput:
    value = _exact_keys(section, _FILE_KEYS, label)
    sha256 = expected_digest(value["sha256"], label)
    target = admit_external_path(value["path"], label)
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

    executable = _sealed_from_plan(
        plan["executable"], "launcher executable", max_bytes=MAX_EXECUTABLE_BYTES
    )
    settings = _sealed_from_plan(plan["settings"], "launcher settings", max_bytes=MAX_DOCUMENT_BYTES)
    prompt = _sealed_from_plan(plan["prompt"], "reviewer prompt", max_bytes=MAX_DOCUMENT_BYTES)

    working_directory = admit_external_path(plan["working_directory"], "working directory")
    inspect_directory(working_directory, "working directory")

    child_environment = build_child_environment(plan["environment"])
    arguments = build_argument_vector(executable.path, settings.path)
    argument_audit = audit_argument_vector(arguments)
    measured_inventory = envelope_inventory()

    sealed_inputs = (plan_sealed, executable, settings, prompt)
    # Everything above described the filesystem at the moment it was read.  Read it all again now
    # that the envelope is otherwise complete: a path or content swap performed during assembly
    # has to survive this second look, and it cannot.
    for sealed in sealed_inputs:
        reverify(sealed)

    evidence = {
        "schema_version": SCHEMA_VERSION,
        "permission_mode": PERMISSION_MODE,
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
            "files": measured_inventory["files"],
        },
    }
    evidence_json = json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    return _sealed_envelope(
        schema_version=SCHEMA_VERSION,
        executable=executable.path,
        arguments=arguments,
        working_directory=str(working_directory),
        stdin_path=prompt.path,
        environment=child_environment,
        sealed_inputs=sealed_inputs,
        inventory_digest=str(measured_inventory["digest"]),
        evidence_json=evidence_json,
        evidence_sha256=hashlib.sha256(evidence_json.encode("utf-8")).hexdigest(),
    )
