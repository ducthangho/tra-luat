"""Executable WP149 positive and hostile matrix for the RA-04A launch envelope.

Every case is REGISTERED before anything runs, so the denominator is fixed before the numerator is
known.  The final report separates scheduled, executed, passed, failed, skipped and not-run: a
suite that quietly stops scheduling a case is the suite most likely to report green.

Security properties are checked with explicit branches through `ensure`, never with `assert`, so
`python -O` executes exactly the same teeth as `python`.  `POS-011` measures that claim on the
source instead of restating it.

Four of the Packet's required checks are repository gates rather than cases here — the repository
selftest, strict release verification, release-bundle determinism and `git diff --check`.  They are
named in `EXTERNAL_GATES` so the report says out loud which checks this file does NOT cover.
"""

from __future__ import annotations

import ast
import contextlib
import copy
import dataclasses
import hashlib
import inspect
import json
import os
import pathlib
import stat
import sys
import tempfile
from collections.abc import Callable, Iterator
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
CANDIDATE_ROOT = HERE.parents[4]
BOOTSTRAP_ROOT = HERE.parents[1]
if str(BOOTSTRAP_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOTSTRAP_ROOT))

from core import scanner as core_scanner  # noqa: E402
from core.guards import EnvGuard, NetworkGuard  # noqa: E402
from launcher.envelope import ALLOWED_ENVIRONMENT_NAMES  # noqa: E402
from launcher.envelope import arguments as arguments_module  # noqa: E402
from launcher.envelope import boundary as boundary_module  # noqa: E402
from launcher.envelope import environment as environment_module  # noqa: E402
from launcher.envelope import inventory as inventory_module  # noqa: E402
from launcher.envelope import paths as paths_module  # noqa: E402
from launcher.envelope import sealed as sealed_module  # noqa: E402
from launcher.envelope.envelope import LaunchEnvelope, build_launch_envelope  # noqa: E402
from launcher.envelope.errors import EnvelopeRejected  # noqa: E402
from oracle import safe_io as safe_io_module  # noqa: E402

CONTROLLER_DIRECTORY = "hồ sơ rà soát"
WORKSPACE_DIRECTORY = "phiên rà soát"
TOOLS_DIRECTORY = "công cụ"
PLAN_NAME = "launch plan.json"
EXECUTABLE_NAME = "claude launcher.bin"
SETTINGS_NAME = "settings.json"
PROMPT_NAME = "prompt.md"

EXECUTABLE_BYTES = b"#!fake-reviewer-launcher\nthis fixture is never executed\n"
SETTINGS_BYTES = b'{"permissions":{"defaultMode":"dontAsk"}}\n'
PROMPT_BYTES = "Rà soát ứng viên theo hai trục độc lập.\n".encode("utf-8")

REQUIRED_CHECKS = (
    "immutable_launch_envelope_interface",
    "permission_mode_exact_dontask",
    "memory_disabled_and_closed_environment",
    "sealed_input_path_and_content_integrity",
    "hostile_argument_environment_and_path_controls",
    "source_inventory_and_static_boundary",
    "optimized_python_controls",
    "eol_policy",
)
EXTERNAL_GATES = (
    "repository_selftest",
    "strict_release_verify",
    "release_bundle_determinism",
    "diff_check",
)


def ensure(condition: object, message: str) -> None:
    """The only checking primitive in this suite.

    It is a branch and a raise, not an `assert`, because `python -O` deletes assertions and a
    security suite that thins out under optimisation was never measuring the optimised build.
    """

    if not condition:
        raise AssertionError(message)


def sha256_of(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class Fixture:
    """A sealed controller directory outside the candidate checkout.

    The names carry spaces and Vietnamese diacritics on purpose: they are the cheapest way to
    prove that no quoting layer exists, because a quoting bug in a path with a space is loud.
    """

    def __init__(self, temp: tempfile.TemporaryDirectory):
        self.temp = temp
        self.root = pathlib.Path(temp.name).resolve()
        self.controller = self.root / CONTROLLER_DIRECTORY
        self.workspace = self.root / WORKSPACE_DIRECTORY
        self.tools = self.root / TOOLS_DIRECTORY
        self.plan_name = PLAN_NAME
        self.plan = self.controller / PLAN_NAME
        self.executable = self.controller / EXECUTABLE_NAME
        self.settings = self.controller / SETTINGS_NAME
        self.prompt = self.controller / PROMPT_NAME

    # ── construction ────────────────────────────────────────────────────────
    def seal(self, path: pathlib.Path, raw: bytes) -> None:
        path.write_bytes(raw)
        path.chmod(stat.S_IREAD)

    def unseal(self, path: pathlib.Path) -> None:
        path.chmod(stat.S_IREAD | stat.S_IWRITE)

    def create(self, *, mutate=None, seal_plan: bool = True, plan_bytes: bytes | None = None) -> None:
        self.controller.mkdir()
        self.workspace.mkdir()
        self.tools.mkdir()
        self.seal(self.executable, EXECUTABLE_BYTES)
        self.seal(self.settings, SETTINGS_BYTES)
        self.seal(self.prompt, PROMPT_BYTES)
        document = self.plan_document()
        if mutate is not None:
            mutate(document)
        raw = plan_bytes if plan_bytes is not None else self.encode(document)
        self.plan.write_bytes(raw)
        if seal_plan:
            self.plan.chmod(stat.S_IREAD)

    @staticmethod
    def encode(document: object) -> bytes:
        return json.dumps(document, ensure_ascii=False, sort_keys=True).encode("utf-8")

    def plan_document(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "permission_mode": "dontAsk",
            "executable": {"path": str(self.executable), "sha256": sha256_of(EXECUTABLE_BYTES)},
            "settings": {"path": str(self.settings), "sha256": sha256_of(SETTINGS_BYTES)},
            "prompt": {"path": str(self.prompt), "sha256": sha256_of(PROMPT_BYTES)},
            "working_directory": str(self.workspace),
            "environment": {
                "PATH": [str(self.tools)],
                "TEMP": str(self.root),
                "LANG": "vi_VN.UTF-8",
            },
        }

    def reseal_plan(self, document: object) -> None:
        self.unseal(self.plan)
        self.seal(self.plan, self.encode(document))

    def build(self) -> LaunchEnvelope:
        return build_launch_envelope(self.controller, self.plan_name)

    # ── observation ─────────────────────────────────────────────────────────
    def snapshot(self) -> dict[str, object]:
        seen: dict[str, object] = {}
        for path in sorted(self.root.rglob("*")):
            info = path.lstat()
            key = path.relative_to(self.root).as_posix()
            if stat.S_ISDIR(info.st_mode):
                seen[key] = {"kind": "dir", "mode": stat.S_IMODE(info.st_mode)}
            elif stat.S_ISREG(info.st_mode):
                seen[key] = {
                    "kind": "file",
                    "mode": stat.S_IMODE(info.st_mode),
                    "size": info.st_size,
                    "sha256": sha256_of(path.read_bytes()),
                }
            else:
                seen[key] = {"kind": "other", "mode": stat.S_IMODE(info.st_mode)}
        return seen

    def release(self) -> None:
        for path in sorted(self.root.rglob("*"), reverse=True):
            try:
                path.chmod(stat.S_IREAD | stat.S_IWRITE)
            except OSError:
                pass


@contextlib.contextmanager
def controller_fixture(mutate=None, *, seal_plan: bool = True, plan_bytes: bytes | None = None) -> Iterator[Fixture]:
    temp = tempfile.TemporaryDirectory(prefix="wp149-envelope-")
    fixture = Fixture(temp)
    try:
        fixture.create(mutate=mutate, seal_plan=seal_plan, plan_bytes=plan_bytes)
        yield fixture
    finally:
        fixture.release()
        temp.cleanup()


def expect_rejection(case_id: str, action: Callable[[], object], expected: str) -> dict[str, object]:
    try:
        action()
    except EnvelopeRejected as exc:
        actual = exc.category
        message = str(exc)
    else:
        raise AssertionError("%s accepted an input that must reject" % case_id)
    ensure(actual == expected, "%s category=%s expected=%s" % (case_id, actual, expected))
    return {"expected_rejection": expected, "actual_rejection": actual, "safe_message": message}


def plan_rejection(
    case_id: str,
    expected: str,
    mutate=None,
    *,
    prepare=None,
    seal_plan: bool = True,
    plan_bytes: bytes | None = None,
) -> dict[str, object]:
    """Reject, and prove the rejection touched nothing on the way out."""

    with controller_fixture(mutate=mutate, seal_plan=seal_plan, plan_bytes=plan_bytes) as fixture:
        if prepare is not None:
            prepare(fixture)
        before = fixture.snapshot()
        result = expect_rejection(case_id, fixture.build, expected)
        ensure(fixture.snapshot() == before, "%s mutated the sealed controller inputs" % case_id)
        result["controller_unchanged"] = True
        return result


CASES: list[tuple[str, str, Callable[[], dict[str, object]]]] = []


def case(case_id: str, check: str):
    def register(function: Callable[[], dict[str, object]]):
        CASES.append((case_id, check, function))
        return function

    return register


# ── positives ───────────────────────────────────────────────────────────────


@case("WP149-POS-001-sealed-structured-envelope", "immutable_launch_envelope_interface")
def positive_structured_envelope():
    with controller_fixture() as fixture:
        envelope = fixture.build()
        ensure(isinstance(envelope, LaunchEnvelope), "builder did not return a launch envelope")
        ensure(envelope.is_sealed(), "returned envelope is not sealed")
        ensure(isinstance(envelope.arguments, tuple), "argument vector is not a tuple")
        ensure(envelope.schema_version == 1, "envelope schema revision is not one")
        ensure(envelope.executable == str(fixture.executable), "executable path mismatch")
        ensure(envelope.working_directory == str(fixture.workspace), "working directory mismatch")
        ensure(envelope.stdin_path == str(fixture.prompt), "prompt is not bound to stdin")
        ensure(len(envelope.sealed_inputs) == 4, "envelope does not carry four sealed inputs")
        ensure(len(envelope.inventory_digest) == 64, "inventory digest is not a SHA-256")
        return {
            "arguments": list(envelope.arguments),
            "sealed_input_labels": [item.label for item in envelope.sealed_inputs],
            "inventory_digest": envelope.inventory_digest,
        }


@case("WP149-POS-002-permission-mode-exact-and-single", "permission_mode_exact_dontask")
def positive_permission_mode():
    with controller_fixture() as fixture:
        vector = fixture.build().arguments
        flags = [index for index, value in enumerate(vector) if value == "--permission-mode"]
        ensure(flags == [arguments_module.PERMISSION_FLAG_INDEX], "permission flag is not exactly once")
        ensure(vector[flags[0] + 1] == "dontAsk", "permission value is not the exact spelling")
        lowered = [value.lower() for value in vector]
        ensure(lowered.count("--permission-mode") == 1, "a case variant adds a second permission flag")
        ensure("--dangerously-skip-permissions" not in lowered, "a bypass switch reached the vector")
        audit = arguments_module.audit_argument_vector(vector)
        ensure(audit["permission_flag_count"] == 1, "audit counted more than one permission decision")
        return {"vector": list(vector), "audit": audit}


@case("WP149-POS-003-memory-flag-injected-once", "memory_disabled_and_closed_environment")
def positive_memory_flag():
    with controller_fixture() as fixture:
        child = fixture.build().environment
        name = environment_module.MEMORY_FLAG_NAME
        ensure(child.get(name) == "1", "the automatic-memory flag is not disabled")
        folded = [key for key in child if key.upper() == name]
        ensure(folded == [name], "the automatic-memory flag appears under more than one spelling")
        return {"memory_flag": child[name], "occurrences": len(folded)}


@case("WP149-POS-004-closed-environment-and-tripwires", "memory_disabled_and_closed_environment")
def positive_closed_environment():
    markers = {
        "GH_TOKEN": "FAKE-WP149-GH-MARKER",
        "GITHUB_TOKEN": "FAKE-WP149-GITHUB-MARKER",
        "ANTHROPIC_API_KEY": "FAKE-WP149-ANTHROPIC-MARKER",
        "AWS_SECRET_ACCESS_KEY": "FAKE-WP149-AWS-MARKER",
    }
    with controller_fixture() as fixture:
        with EnvGuard(inject=dict(markers), guard_subprocess=True) as recorder, NetworkGuard() as network:
            envelope = fixture.build()
            reads = recorder.sensitive_reads()
            attempts = list(network.attempts)
        child = envelope.environment
        allowed = set(ALLOWED_ENVIRONMENT_NAMES) | {environment_module.MEMORY_FLAG_NAME}
        unexpected = sorted(set(child) - allowed)
        ensure(unexpected == [], "the child environment carries names outside the closed allowlist")
        ensure(reads == [], "building the envelope read a protected environment value")
        ensure(attempts == [], "building the envelope attempted a network operation")
        for name in markers:
            ensure(name not in child, "a credential name reached the child environment")
        leaked = [
            name
            for name, value in child.items()
            if any(marker in value for marker in markers.values())
        ]
        ensure(leaked == [], "a credential value reached a child environment value")
        evidence = envelope.as_evidence()["environment"]
        ensure("value_shapes" in evidence, "environment evidence lost its redacted shapes")
        for shape in evidence["value_shapes"].values():
            ensure(set(shape) == {"length", "sha256"}, "environment evidence records a raw value")
        return {
            "names": sorted(child),
            "sensitive_reads": reads,
            "network_attempts": attempts,
            "unexpected_names": unexpected,
        }


@case("WP149-POS-005-sealed-inputs-are-read-twice", "sealed_input_path_and_content_integrity")
def positive_sealed_reread():
    counts: dict[str, int] = {}
    real = sealed_module.read_sealed_bytes

    def counting(target, label, *, max_bytes):
        counts[label] = counts.get(label, 0) + 1
        return real(target, label, max_bytes=max_bytes)

    with controller_fixture() as fixture:
        with mock.patch.object(sealed_module, "read_sealed_bytes", counting):
            envelope = fixture.build()
        expected = {
            "launch plan": 1,
            "launcher executable": 2,
            "launcher settings": 2,
            "reviewer prompt": 2,
        }
        # The plan's first read happens through the builder's own binding, so the seam sees it
        # once; every other input is read once to validate and once to re-verify.
        ensure(counts == expected, "the sealed re-read did not happen exactly once per input")
        digests = {item.label: item.sha256 for item in envelope.sealed_inputs}
        ensure(digests["launcher settings"] == sha256_of(SETTINGS_BYTES), "settings digest mismatch")
        ensure(digests["reviewer prompt"] == sha256_of(PROMPT_BYTES), "prompt digest mismatch")
        ensure(digests["launcher executable"] == sha256_of(EXECUTABLE_BYTES), "executable digest mismatch")
        return {"seam_calls": counts, "digests": digests}


@case("WP149-POS-006-whole-token-paths-without-quoting", "hostile_argument_environment_and_path_controls")
def positive_whole_tokens():
    with controller_fixture() as fixture:
        vector = fixture.build().arguments
        executable, settings = vector[0], vector[5]
        ensure(executable == str(fixture.executable), "executable token was rewritten")
        ensure(settings == str(fixture.settings), "settings token was rewritten")
        ensure(" " in executable, "the fixture lost its space-bearing path")
        ensure("ồ" in settings, "the fixture lost its Vietnamese path segment")
        for element in vector:
            ensure('"' not in element, "an element carries an injected quote")
            ensure("'" not in element, "an element carries an injected quote")
            ensure("^" not in element, "an element carries a shell escape")
        return {"executable": executable, "settings": settings, "element_count": len(vector)}


@case("WP149-POS-007-separator-spellings-normalise", "hostile_argument_environment_and_path_controls")
def positive_separator_spellings():
    """A trailing or foreign separator is the same directory, and must normalise to it.

    The forward-slash spelling is a genuinely different string only where `os.sep` is a backslash;
    on POSIX that third spelling collapses into the first, and the case says so rather than
    claiming three independent observations on every platform.
    """

    with controller_fixture() as fixture:
        first = fixture.build().working_directory
        document = fixture.plan_document()
        document["working_directory"] = str(fixture.workspace) + os.sep
        fixture.reseal_plan(document)
        trailing = fixture.build().working_directory
        document["working_directory"] = str(fixture.workspace).replace(os.sep, "/")
        fixture.reseal_plan(document)
        alternate = fixture.build().working_directory
        ensure(first == trailing, "a trailing separator produced a different working directory")
        ensure(first == alternate, "an alternate separator produced a different working directory")
        return {
            "working_directory": first,
            "spellings_tested": 3,
            "distinct_spellings": 3 if os.sep != "/" else 2,
        }


@case("WP149-POS-008-inventory-covers-the-write-set", "source_inventory_and_static_boundary")
def positive_inventory():
    measured = inventory_module.envelope_inventory()
    names = [item["path"] for item in measured["files"]]
    on_disk = sorted(
        path.name for path in HERE.iterdir() if path.is_file() and path.name != "__pycache__"
    )
    ensure(measured["prefix"] == inventory_module.ENVELOPE_PREFIX, "inventory prefix is not the write set")
    ensure(names == on_disk, "the inventory does not cover every file below the prefix")
    ensure(measured["file_count"] == len(on_disk), "inventory file count disagrees with the prefix")
    for item in measured["files"]:
        ensure("/" not in item["path"], "an inventory entry escaped the prefix root")
        ensure(len(item["sha256"]) == 64, "an inventory entry has no digest")
    ensure(
        inventory_module.envelope_inventory()["digest"] == measured["digest"],
        "the inventory digest is not stable across two runs",
    )
    return {"file_count": measured["file_count"], "digest": measured["digest"], "files": names}


@case("WP149-POS-009-static-boundary-is-clean", "source_inventory_and_static_boundary")
def positive_boundary_clean():
    report = boundary_module.scan_prefix()
    ensure(report["findings"] == [], "the static boundary scan found a forbidden capability")
    ensure("selftest.py" in report["scanned"], "the scan skipped the suite itself")
    ensure(len(report["scanned"]) >= 9, "the scan covered fewer modules than the package holds")
    ensure(boundary_module.COVERAGE["not_covered"], "the scan claims to cover everything")
    return {"scanned": report["scanned"], "findings": report["findings"]}


HOSTILE_SNIPPETS = (
    ("process_spawn", "import subprocess\nsubprocess.run(['claude'])\n"),
    ("process_spawn", "import os\nos.system('claude --permission-mode auto')\n"),
    ("process_spawn", "import os as o\no.posix_spawn('/bin/sh', [], {})\n"),
    ("network_or_github_client", "import requests\n"),
    ("network_or_github_client", "import socket\n"),
    ("shell_execution", "import shlex\n"),
    ("dynamic_code", "import importlib\n"),
    ("dynamic_code", "value = eval('1 + 1')\n"),
    ("unmediated_file_read", "raw = open('secrets.txt')\n"),
    ("windows_process_api", "handle.AssignProcessToJobObject(job, child)\n"),
    ("durable_state_operation", "store.post_heartbeat(payload)\n"),
    ("durable_state_operation", "store.create_verdict(payload)\n"),
    ("fenced_launcher_import", "from launcher.flat import spawn_reviewer\n"),
    ("fenced_launcher_import", "import reviewer_launcher\n"),
    ("package_boundary", "from gateway.gateway import CapabilityGateway\n"),
    ("package_boundary", "from ..legacy import spawn_reviewer\n"),
    ("ambient_environment_read", "import os\ntoken = os.getenv('GH_TOKEN')\n"),
    ("security_assert", "def check(x):\n    assert x, 'unsafe'\n"),
    ("import_not_allowed", "import antigravity\n"),
    ("filesystem_mutation", "import os\nos.chmod('input.json', 438)\n"),
)


@case("WP149-POS-010-boundary-detector-counter-control", "source_inventory_and_static_boundary")
def positive_boundary_counter_control():
    """A detector that never fires is indistinguishable from a detector that is broken."""

    observed = []
    for expected, snippet in HOSTILE_SNIPPETS:
        findings = boundary_module.scan_source(snippet, "hostile.py")
        categories = sorted({item["category"] for item in findings})
        ensure(
            expected in categories,
            "the scanner missed %s in %r (saw %s)" % (expected, snippet, categories),
        )
        observed.append({"expected": expected, "categories": categories})
    clean = boundary_module.scan_source("import json\nvalue = json.dumps({})\n", "clean.py")
    ensure(clean == [], "the scanner accuses an innocent module")
    return {"snippets": len(HOSTILE_SNIPPETS), "observed": observed}


@case("WP149-POS-011-no-assert-below-the-prefix", "optimized_python_controls")
def positive_no_assert():
    offenders = []
    for path in sorted(HERE.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        offenders.extend(
            (path.name, node.lineno) for node in ast.walk(tree) if isinstance(node, ast.Assert)
        )
    ensure(offenders == [], "an optimisation-removable assertion carries a security branch")
    return {"files": [path.name for path in sorted(HERE.glob("*.py"))], "assert_nodes": offenders}


@case("WP149-POS-012-optimised-branches-still-execute", "optimized_python_controls")
def positive_optimised_branches():
    raised = None
    try:
        ensure(False, "the suite's own checking primitive must raise")
    except AssertionError as exc:
        raised = str(exc)
    ensure(raised is not None, "ensure() did not raise under the current optimisation level")
    rejected = expect_rejection(
        "WP149-POS-012-optimised-branches-still-execute",
        lambda: arguments_module.audit_argument_vector(
            ("claude", "-p", "--permission-mode", "auto", "--settings", "s")
        ),
        "argument_permission_value",
    )
    return {"optimized": not __debug__, "ensure_raised": raised, "security_branch": rejected}


@case("WP149-POS-013-eol-and-encoding-policy", "eol_policy")
def positive_eol_policy():
    surveyed = []
    violations = []
    for path in sorted(HERE.iterdir()):
        if not path.is_file():
            continue
        raw = path.read_bytes()
        lf = raw.count(b"\n")
        crlf = raw.count(b"\r\n")
        cr = raw.count(b"\r")
        if crlf or cr:
            violations.append({"file": path.name, "reason": "carriage_return"})
        if raw.startswith(b"\xef\xbb\xbf"):
            violations.append({"file": path.name, "reason": "byte_order_mark"})
        if raw and not raw.endswith(b"\n"):
            violations.append({"file": path.name, "reason": "missing_final_newline"})
        try:
            raw.decode("utf-8", errors="strict")
        except UnicodeError:
            violations.append({"file": path.name, "reason": "not_utf8"})
        surveyed.append({"file": path.name, "lf": lf, "crlf": crlf})
    ensure(violations == [], "the prefix violates the LF, BOM or encoding policy")
    ensure(surveyed, "the EOL survey measured no files at all")
    return {"surveyed": surveyed, "violations": violations, "file_count": len(surveyed)}


@case("WP149-POS-014-envelope-is-immutable", "immutable_launch_envelope_interface")
def positive_immutable():
    with controller_fixture() as fixture:
        envelope = fixture.build()
        attribute_error = None
        try:
            envelope.executable = "C:\\attacker\\claude.exe"
        except (AttributeError, TypeError) as exc:
            attribute_error = type(exc).__name__
        ensure(attribute_error is not None, "envelope attributes are writable")
        mapping_error = None
        try:
            envelope.environment["GH_TOKEN"] = "FAKE-WP149-MARKER"
        except TypeError as exc:
            mapping_error = type(exc).__name__
        ensure(mapping_error is not None, "the child environment mapping is writable")
        first = envelope.as_evidence()
        first["permission_mode"] = "auto"
        ensure(
            envelope.as_evidence()["permission_mode"] == "dontAsk",
            "mutating a returned evidence copy changed the envelope",
        )
        ensure(
            envelope.evidence_sha256 == sha256_of(envelope.evidence_json.encode("utf-8")),
            "the evidence digest does not bind the evidence bytes",
        )
        return {"attribute_mutation": attribute_error, "mapping_mutation": mapping_error}


@case("WP149-POS-015-shared-hardened-reader-reuse", "sealed_input_path_and_content_integrity")
def positive_shared_reader():
    ensure(
        sealed_module.read_regular_single_link is safe_io_module.read_regular_single_link,
        "the sealed reader is not the sanctioned shared hardened reader",
    )
    ensure(
        paths_module.require_outside_tree is safe_io_module.require_outside_tree,
        "the candidate-tree check is not the sanctioned shared implementation",
    )
    duplicates = []
    for path in boundary_module.implementation_modules():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        duplicates.extend(
            (path.name, node.lineno)
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
            and node.func.attr in {"open", "fdopen", "fstat"}
        )
    ensure(duplicates == [], "the package carries a driftable second low-level reader")
    return {"shared_identity": True, "duplicate_low_level_reader_calls": duplicates}


@case("WP149-POS-016-controller-inputs-are-not-mutated", "sealed_input_path_and_content_integrity")
def positive_inputs_untouched():
    with controller_fixture() as fixture:
        before = fixture.snapshot()
        fixture.build()
        after = fixture.snapshot()
        ensure(before == after, "building the envelope changed the sealed controller directory")
        ensure(
            (stat.S_IMODE(fixture.settings.lstat().st_mode) & stat.S_IWUSR) == 0,
            "the builder relaxed a sealed input's mode",
        )
        return {"entries": len(before), "unchanged": True}


@case("WP149-POS-017-evidence-is-deterministic", "immutable_launch_envelope_interface")
def positive_deterministic_evidence():
    with controller_fixture() as fixture:
        first = fixture.build()
        second = fixture.build()
        ensure(first.evidence_json == second.evidence_json, "two builds produced different evidence")
        ensure(first.evidence_sha256 == second.evidence_sha256, "two builds produced different digests")
        ensure(first.arguments == second.arguments, "two builds produced different argument vectors")
        ensure(dict(first.environment) == dict(second.environment), "two builds produced different environments")
        decoded = first.as_evidence()
        canonical = json.dumps(decoded, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        ensure(canonical == first.evidence_json, "the retained evidence is not canonical JSON")
        return {"evidence_sha256": first.evidence_sha256, "builds": 2}


@case("WP149-POS-018-borrowed-alias-resolver-identity", "source_inventory_and_static_boundary")
def positive_alias_resolver_identity():
    ensure(boundary_module._resolve_call is core_scanner._resolve_call, "the alias resolver drifted")
    ensure(boundary_module._alias_map is core_scanner._alias_map, "the alias map drifted")
    ensure(boundary_module._dotted is core_scanner._dotted, "the dotted-name resolver drifted")
    network = boundary_module.IMPORT_CLASSES["network_or_github_client"]
    missing = sorted(set(core_scanner.FORBIDDEN_IMPORTS) - set(network))
    ensure(missing == [], "the network class stopped covering the RA-01 forbidden import table")
    return {"shared_resolver": True, "missing_forbidden_imports": missing}


PUBLIC_PARAMETER_DENYLIST = frozenset(
    {
        "allow",
        "args",
        "argv",
        "callback",
        "clean",
        "command",
        "env",
        "environ",
        "extra",
        "force",
        "hook",
        "insecure",
        "observed",
        "shell",
        "skip",
        "trust",
        "trusted",
        "unsafe",
        "candidate_root",
    }
)


@case("WP149-POS-019-interface-has-no-trust-seam", "immutable_launch_envelope_interface")
def positive_no_trust_seam():
    package = sys.modules["launcher.envelope"]
    audited = []
    for name in package.__all__:
        member = getattr(package, name)
        if not inspect.isfunction(member):
            continue
        signature = inspect.signature(member)
        for parameter in signature.parameters.values():
            ensure(
                parameter.kind
                not in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL),
                "%s accepts open-ended arguments" % name,
            )
            ensure(
                parameter.name not in PUBLIC_PARAMETER_DENYLIST,
                "%s accepts a command, environment or trust parameter" % name,
            )
            # A parameter with no default carries the `Parameter.empty` SENTINEL, and that
            # sentinel is a class — so `callable()` says yes to it.  Testing the default without
            # first asking whether there IS one accuses every ordinary parameter of being a
            # callback seam, which is how a detector ends up measuring its own sentinel.
            declared_default = parameter.default is not inspect.Parameter.empty
            ensure(
                not (declared_default and isinstance(parameter.default, bool)),
                "%s accepts a boolean trust claim" % name,
            )
            ensure(
                not (declared_default and callable(parameter.default)),
                "%s accepts a callback default" % name,
            )
            annotation = str(parameter.annotation)
            ensure("Callable" not in annotation, "%s accepts a callback" % name)
            ensure("bool" not in annotation, "%s accepts a boolean claim" % name)
        audited.append({"name": name, "parameters": [p.name for p in signature.parameters.values()]})
    ensure(audited, "the public surface exposes no callable to audit")
    return {"audited": audited}


@case("WP149-POS-020-required-check-coverage", "immutable_launch_envelope_interface")
def positive_required_check_coverage():
    identifiers = [case_id for case_id, _check, _fn in CASES]
    ensure(len(identifiers) == len(set(identifiers)), "two cases share one identifier")
    covered = {check for _case_id, check, _fn in CASES}
    unknown = sorted(covered - set(REQUIRED_CHECKS))
    missing = sorted(set(REQUIRED_CHECKS) - covered)
    ensure(unknown == [], "a case claims a check that is not required")
    ensure(missing == [], "a required check has no registered case")
    overlap = sorted(set(REQUIRED_CHECKS) & set(EXTERNAL_GATES))
    ensure(overlap == [], "an external repository gate is claimed as an in-suite check")
    return {
        "scheduled": len(CASES),
        "in_suite_checks": sorted(covered),
        "external_gates": list(EXTERNAL_GATES),
    }


@case("WP149-POS-021-forged-subclass-is-not-sealed", "immutable_launch_envelope_interface")
def positive_forged_subclass():
    class ForgedEnvelope(LaunchEnvelope):
        def __init__(self):
            object.__setattr__(self, "executable", "C:\\attacker\\claude.exe")
            object.__setattr__(self, "_seal", None)

        def __post_init__(self):
            pass

    forged = ForgedEnvelope()
    ensure(not forged.is_sealed(), "a forged subclass reports itself as sealed")
    ensure(not LaunchEnvelope.is_sealed(forged), "the seal check can be answered by the subclass")
    return {"forged_is_sealed": forged.is_sealed()}


# ── negatives: permission mode and argument vector ──────────────────────────


@case("WP149-NEG-001-plan-permission-auto", "permission_mode_exact_dontask")
def negative_permission_auto():
    return plan_rejection(
        "WP149-NEG-001-plan-permission-auto",
        "permission_mode_unsupported",
        lambda plan: plan.__setitem__("permission_mode", "auto"),
    )


@case("WP149-NEG-002-plan-permission-case-folded", "permission_mode_exact_dontask")
def negative_permission_case():
    return plan_rejection(
        "WP149-NEG-002-plan-permission-case-folded",
        "permission_mode_unsupported",
        lambda plan: plan.__setitem__("permission_mode", "dontask"),
    )


@case("WP149-NEG-003-plan-permission-missing", "permission_mode_exact_dontask")
def negative_permission_missing():
    return plan_rejection(
        "WP149-NEG-003-plan-permission-missing",
        "plan_schema",
        lambda plan: plan.pop("permission_mode"),
    )


@case("WP149-NEG-004-vector-permission-flag-absent", "permission_mode_exact_dontask")
def negative_vector_flag_absent():
    return expect_rejection(
        "WP149-NEG-004-vector-permission-flag-absent",
        lambda: arguments_module.audit_argument_vector(
            ("claude", "-p", "--verbose", "dontAsk", "--settings", "s")
        ),
        "argument_permission_missing",
    )


@case("WP149-NEG-005-vector-permission-duplicated", "permission_mode_exact_dontask")
def negative_vector_duplicate():
    return expect_rejection(
        "WP149-NEG-005-vector-permission-duplicated",
        lambda: arguments_module.audit_argument_vector(
            ("claude", "-p", "--permission-mode", "dontAsk", "--settings", "--permission-mode")
        ),
        "argument_permission_duplicate",
    )


@case("WP149-NEG-006-vector-permission-value-auto", "permission_mode_exact_dontask")
def negative_vector_value():
    return expect_rejection(
        "WP149-NEG-006-vector-permission-value-auto",
        lambda: arguments_module.audit_argument_vector(
            ("claude", "-p", "--permission-mode", "acceptEdits", "--settings", "s")
        ),
        "argument_permission_value",
    )


@case("WP149-NEG-007-vector-permission-value-in-slot", "hostile_argument_environment_and_path_controls")
def negative_vector_value_in_slot():
    return expect_rejection(
        "WP149-NEG-007-vector-permission-value-in-slot",
        lambda: arguments_module.audit_argument_vector(
            ("claude", "-p", "--permission-mode", "dontAsk", "--settings", "DONTASK")
        ),
        "argument_permission_injection",
    )


@case("WP149-NEG-008-executable-path-is-an-option", "hostile_argument_environment_and_path_controls")
def negative_executable_option():
    return plan_rejection(
        "WP149-NEG-008-executable-path-is-an-option",
        "path_option_smuggling",
        lambda plan: plan["executable"].__setitem__("path", "--permission-mode"),
    )


@case("WP149-NEG-009-settings-path-control-character", "hostile_argument_environment_and_path_controls")
def negative_settings_control_character():
    def mutate(plan):
        plan["settings"]["path"] = plan["settings"]["path"] + "\n--permission-mode auto"

    return plan_rejection(
        "WP149-NEG-009-settings-path-control-character",
        "path_control_character",
        mutate,
    )


# ── negatives: environment ──────────────────────────────────────────────────


def environment_rejection(case_id: str, expected: str, name: str, value: object):
    return plan_rejection(
        case_id,
        expected,
        lambda plan: plan["environment"].__setitem__(name, value),
    )


@case("WP149-NEG-010-memory-flag-declared", "memory_disabled_and_closed_environment")
def negative_memory_declared():
    return environment_rejection(
        "WP149-NEG-010-memory-flag-declared",
        "environment_memory_override",
        "CLAUDE_CODE_DISABLE_AUTO_MEMORY",
        "0",
    )


@case("WP149-NEG-011-memory-flag-declared-case-folded", "memory_disabled_and_closed_environment")
def negative_memory_declared_folded():
    return environment_rejection(
        "WP149-NEG-011-memory-flag-declared-case-folded",
        "environment_memory_override",
        "Claude_Code_Disable_Auto_Memory",
        "0",
    )


@case("WP149-NEG-012-environment-case-collision", "memory_disabled_and_closed_environment")
def negative_case_collision():
    return environment_rejection(
        "WP149-NEG-012-environment-case-collision",
        "environment_case_collision",
        "Path",
        ["C:\\Windows\\System32"],
    )


for _suffix, _slug, _name in (
    ("013", "pythonpath", "PYTHONPATH"),
    ("014", "bash-env", "BASH_ENV"),
    ("015", "env", "ENV"),
    ("016", "node-options", "NODE_OPTIONS"),
    ("017", "git-config-global", "GIT_CONFIG_GLOBAL"),
    ("018", "ld-preload", "LD_PRELOAD"),
):
    _case_id = "WP149-NEG-%s-%s-injection" % (_suffix, _slug)

    @case(_case_id, "memory_disabled_and_closed_environment")
    def _injection_case(case_id=_case_id, name=_name):
        return environment_rejection(case_id, "environment_injection_name", name, "C:\\attacker")


for _suffix, _slug, _name in (
    ("019", "gh-token", "GH_TOKEN"),
    ("020", "anthropic-api-key", "ANTHROPIC_API_KEY"),
    ("021", "aws-secret", "AWS_SECRET_ACCESS_KEY"),
):
    _case_id = "WP149-NEG-%s-%s-credential" % (_suffix, _slug)

    @case(_case_id, "memory_disabled_and_closed_environment")
    def _credential_case(case_id=_case_id, name=_name):
        return environment_rejection(
            case_id, "environment_credential_name", name, "FAKE-WP149-CREDENTIAL"
        )


@case("WP149-NEG-022-environment-extra-name", "memory_disabled_and_closed_environment")
def negative_environment_extra():
    return environment_rejection(
        "WP149-NEG-022-environment-extra-name",
        "environment_name_not_allowed",
        "REVIEWER_BOOTSTRAP_MODE",
        "candidate",
    )


@case("WP149-NEG-023-path-declared-as-string", "memory_disabled_and_closed_environment")
def negative_path_string():
    return environment_rejection(
        "WP149-NEG-023-path-declared-as-string",
        "environment_path_not_list",
        "PATH",
        "C:\\Windows\\System32;C:\\attacker",
    )


@case("WP149-NEG-024-path-entry-relative", "hostile_argument_environment_and_path_controls")
def negative_path_relative():
    return environment_rejection(
        "WP149-NEG-024-path-entry-relative",
        "path_entry_relative",
        "PATH",
        ["tools"],
    )


@case("WP149-NEG-025-path-entry-empty", "hostile_argument_environment_and_path_controls")
def negative_path_empty():
    return environment_rejection(
        "WP149-NEG-025-path-entry-empty",
        "path_entry_empty",
        "PATH",
        [""],
    )


@case("WP149-NEG-026-path-entry-current-directory", "hostile_argument_environment_and_path_controls")
def negative_path_current_directory():
    return environment_rejection(
        "WP149-NEG-026-path-entry-current-directory",
        "path_entry_current_directory",
        "PATH",
        ["."],
    )


@case("WP149-NEG-027-path-entry-inside-candidate", "hostile_argument_environment_and_path_controls")
def negative_path_inside_candidate():
    return environment_rejection(
        "WP149-NEG-027-path-entry-inside-candidate",
        "path_entry_inside_candidate",
        "PATH",
        [str(CANDIDATE_ROOT / "scripts")],
    )


@case("WP149-NEG-028-path-entry-hidden-separator", "hostile_argument_environment_and_path_controls")
def negative_path_hidden_separator():
    return environment_rejection(
        "WP149-NEG-028-path-entry-hidden-separator",
        "path_entry_separator",
        "PATH",
        ["C:\\tools" + os.pathsep + "C:\\attacker"],
    )


@case("WP149-NEG-029-environment-value-control-character", "memory_disabled_and_closed_environment")
def negative_environment_control():
    return environment_rejection(
        "WP149-NEG-029-environment-value-control-character",
        "environment_value_control_character",
        "LANG",
        "vi_VN.UTF-8\nGH_TOKEN=FAKE",
    )


@case("WP149-NEG-030-environment-value-not-a-string", "memory_disabled_and_closed_environment")
def negative_environment_value_type():
    return environment_rejection(
        "WP149-NEG-030-environment-value-not-a-string",
        "environment_value_type",
        "LANG",
        7,
    )


# ── negatives: sealed inputs and paths ──────────────────────────────────────


@case("WP149-NEG-031-settings-digest-mismatch", "sealed_input_path_and_content_integrity")
def negative_settings_digest():
    return plan_rejection(
        "WP149-NEG-031-settings-digest-mismatch",
        "sealed_input_digest",
        lambda plan: plan["settings"].__setitem__("sha256", "0" * 64),
    )


@case("WP149-NEG-032-prompt-is-writable", "sealed_input_path_and_content_integrity")
def negative_prompt_writable():
    return plan_rejection(
        "WP149-NEG-032-prompt-is-writable",
        "path_writable",
        prepare=lambda fixture: fixture.unseal(fixture.prompt),
    )


@case("WP149-NEG-033-settings-has-a-second-link", "sealed_input_path_and_content_integrity")
def negative_settings_hardlink():
    with controller_fixture() as fixture:
        alias = fixture.controller / "settings.alias.json"
        try:
            os.link(fixture.settings, alias)
        except (OSError, NotImplementedError, AttributeError):
            # Some filesystems refuse a second link.  Exercise the exact branch through a
            # link-count stat instead of shrinking the denominator to fit the environment.
            linked = os.stat_result((stat.S_IFREG | 0o444, 0, 0, 2, 0, 0, len(SETTINGS_BYTES), 0, 0, 0))
            with mock.patch.object(pathlib.Path, "lstat", return_value=linked):
                result = expect_rejection(
                    "WP149-NEG-033-settings-has-a-second-link",
                    lambda: paths_module.inspect_sealed_file(
                        fixture.settings, "launcher settings", max_bytes=1024
                    ),
                    "path_hardlink",
                )
            result["fixture"] = "portable_link_count_stat"
            return result
        result = expect_rejection(
            "WP149-NEG-033-settings-has-a-second-link",
            fixture.build,
            "path_hardlink",
        )
        result["fixture"] = "filesystem_hard_link"
        result["link_count"] = fixture.settings.lstat().st_nlink
        return result


@case("WP149-NEG-034-prompt-is-a-symlink", "sealed_input_path_and_content_integrity")
def negative_prompt_symlink():
    with controller_fixture() as fixture:
        target = fixture.controller / "prompt.link.md"
        try:
            os.symlink(fixture.prompt, target)
        except (OSError, NotImplementedError, AttributeError):
            # Windows without Developer Mode cannot create a symlink unprivileged; drive the same
            # lstat branch with a symlink-mode result rather than skipping the case.
            linked = os.stat_result((stat.S_IFLNK | 0o777, 0, 0, 1, 0, 0, 0, 0, 0, 0))
            with mock.patch.object(pathlib.Path, "lstat", return_value=linked):
                result = expect_rejection(
                    "WP149-NEG-034-prompt-is-a-symlink",
                    lambda: paths_module.inspect_sealed_file(
                        fixture.prompt, "reviewer prompt", max_bytes=1024
                    ),
                    "path_symlink",
                )
            result["fixture"] = "portable_symlink_lstat"
            return result
        document = fixture.plan_document()
        document["prompt"]["path"] = str(target)
        fixture.reseal_plan(document)
        result = expect_rejection(
            "WP149-NEG-034-prompt-is-a-symlink",
            fixture.build,
            "path_symlink",
        )
        result["fixture"] = "filesystem_symlink"
        return result


@case("WP149-NEG-035-plan-name-traversal", "sealed_input_path_and_content_integrity")
def negative_plan_traversal():
    with controller_fixture() as fixture:
        return expect_rejection(
            "WP149-NEG-035-plan-name-traversal",
            lambda: build_launch_envelope(fixture.controller, "../launch plan.json"),
            "plan_path",
        )


@case("WP149-NEG-036-controller-root-relative", "sealed_input_path_and_content_integrity")
def negative_controller_relative():
    with controller_fixture() as fixture:
        return expect_rejection(
            "WP149-NEG-036-controller-root-relative",
            lambda: build_launch_envelope("controller", fixture.plan_name),
            "plan_path",
        )


@case("WP149-NEG-037-plan-inside-the-candidate", "sealed_input_path_and_content_integrity")
def negative_plan_inside_candidate():
    return expect_rejection(
        "WP149-NEG-037-plan-inside-the-candidate",
        lambda: build_launch_envelope(CANDIDATE_ROOT, "VERSION"),
        "path_inside_candidate",
    )


@case("WP149-NEG-038-executable-inside-the-candidate", "hostile_argument_environment_and_path_controls")
def negative_executable_inside_candidate():
    return plan_rejection(
        "WP149-NEG-038-executable-inside-the-candidate",
        "path_inside_candidate",
        lambda plan: plan["executable"].__setitem__("path", str(CANDIDATE_ROOT / "VERSION")),
    )


@case("WP149-NEG-039-working-directory-inside-the-candidate", "hostile_argument_environment_and_path_controls")
def negative_workdir_inside_candidate():
    return plan_rejection(
        "WP149-NEG-039-working-directory-inside-the-candidate",
        "path_inside_candidate",
        lambda plan: plan.__setitem__("working_directory", str(CANDIDATE_ROOT)),
    )


@case("WP149-NEG-040-working-directory-is-a-file", "hostile_argument_environment_and_path_controls")
def negative_workdir_is_file():
    with controller_fixture() as fixture:
        document = fixture.plan_document()
        document["working_directory"] = str(fixture.settings)
        fixture.reseal_plan(document)
        return expect_rejection(
            "WP149-NEG-040-working-directory-is-a-file",
            fixture.build,
            "path_not_directory",
        )


@case("WP149-NEG-041-executable-is-absent", "sealed_input_path_and_content_integrity")
def negative_executable_absent():
    with controller_fixture() as fixture:
        document = fixture.plan_document()
        document["executable"]["path"] = str(fixture.controller / "absent launcher.bin")
        fixture.reseal_plan(document)
        return expect_rejection(
            "WP149-NEG-041-executable-is-absent",
            fixture.build,
            "path_missing",
        )


@case("WP149-NEG-042-settings-alternate-data-stream", "hostile_argument_environment_and_path_controls")
def negative_settings_ads():
    return plan_rejection(
        "WP149-NEG-042-settings-alternate-data-stream",
        "path_alternate_data_stream",
        lambda plan: plan["settings"].__setitem__("path", plan["settings"]["path"] + ":wp149"),
    )


@case("WP149-NEG-043-prompt-reserved-device", "hostile_argument_environment_and_path_controls")
def negative_prompt_device():
    def mutate(plan):
        parent = str(pathlib.PurePath(plan["prompt"]["path"]).parent)
        plan["prompt"]["path"] = str(pathlib.PurePath(parent) / "NUL")

    return plan_rejection(
        "WP149-NEG-043-prompt-reserved-device",
        "path_reserved_device",
        mutate,
    )


@case("WP149-NEG-044-settings-unc-share", "hostile_argument_environment_and_path_controls")
def negative_settings_unc():
    return plan_rejection(
        "WP149-NEG-044-settings-unc-share",
        "path_unc_or_device_namespace",
        lambda plan: plan["settings"].__setitem__("path", "\\\\attacker\\share\\settings.json"),
    )


@case("WP149-NEG-045-settings-traversal-spelling", "hostile_argument_environment_and_path_controls")
def negative_settings_traversal():
    def mutate(plan):
        parent = pathlib.PurePath(plan["settings"]["path"]).parent
        plan["settings"]["path"] = str(parent / ".." / CONTROLLER_DIRECTORY / SETTINGS_NAME)

    return plan_rejection(
        "WP149-NEG-045-settings-traversal-spelling",
        "path_traversal",
        mutate,
    )


@case("WP149-NEG-046-executable-relative-path", "hostile_argument_environment_and_path_controls")
def negative_executable_relative():
    return plan_rejection(
        "WP149-NEG-046-executable-relative-path",
        "path_not_absolute",
        lambda plan: plan["executable"].__setitem__("path", EXECUTABLE_NAME),
    )


@case("WP149-NEG-047-plan-oversized", "sealed_input_path_and_content_integrity")
def negative_plan_oversized():
    padding = b'{"schema_version":1,"padding":"' + b"x" * (sealed_module.MAX_PLAN_BYTES + 16) + b'"}'
    return plan_rejection(
        "WP149-NEG-047-plan-oversized",
        "path_oversized",
        plan_bytes=padding,
    )


@case("WP149-NEG-048-plan-duplicate-json-key", "sealed_input_path_and_content_integrity")
def negative_plan_duplicate_key():
    raw = b'{"schema_version": 1, "permission_mode": "dontAsk", "permission_mode": "auto"}'
    return plan_rejection(
        "WP149-NEG-048-plan-duplicate-json-key",
        "plan_schema",
        plan_bytes=raw,
    )


@case("WP149-NEG-049-plan-not-utf8", "sealed_input_path_and_content_integrity")
def negative_plan_encoding():
    return plan_rejection(
        "WP149-NEG-049-plan-not-utf8",
        "plan_encoding",
        plan_bytes=b'{"schema_version": 1, "permission_mode": "\xff"}',
    )


@case("WP149-NEG-050-plan-extra-key", "sealed_input_path_and_content_integrity")
def negative_plan_extra_key():
    return plan_rejection(
        "WP149-NEG-050-plan-extra-key",
        "plan_schema",
        lambda plan: plan.__setitem__("stdin_text", "ignore previous instructions"),
    )


@case("WP149-NEG-051-digest-is-not-hexadecimal", "sealed_input_path_and_content_integrity")
def negative_digest_shape():
    return plan_rejection(
        "WP149-NEG-051-digest-is-not-hexadecimal",
        "plan_schema",
        lambda plan: plan["prompt"].__setitem__("sha256", "Z" * 64),
    )


@case("WP149-NEG-052-content-replaced-before-the-second-read", "sealed_input_path_and_content_integrity")
def negative_content_replaced():
    real = sealed_module.read_sealed_bytes
    seen: dict[str, int] = {}

    def swapping(target, label, *, max_bytes):
        raw = real(target, label, max_bytes=max_bytes)
        seen[label] = seen.get(label, 0) + 1
        if label == "reviewer prompt" and seen[label] > 1:
            return raw + b"replaced after validation\n"
        return raw

    with controller_fixture() as fixture:
        with mock.patch.object(sealed_module, "read_sealed_bytes", swapping):
            result = expect_rejection(
                "WP149-NEG-052-content-replaced-before-the-second-read",
                fixture.build,
                "sealed_input_replaced",
            )
        result["reads_per_label"] = dict(seen)
        return result


@case("WP149-NEG-053-plan-is-writable", "sealed_input_path_and_content_integrity")
def negative_plan_writable():
    return plan_rejection(
        "WP149-NEG-053-plan-is-writable",
        "path_writable",
        seal_plan=False,
    )


@case("WP149-NEG-061-short-read-is-refused", "sealed_input_path_and_content_integrity")
def negative_short_read():
    """A read that returns fewer bytes than the file holds is never hashed anyway.

    Windows text mode is the realistic cause: the shared reader opens without `O_BINARY`, so a
    launcher binary containing CRLF would come back shortened and its digest would describe bytes
    that are not on disk.  The stub below produces the same shape deliberately.
    """

    def truncating(target, label, error, *, require_readonly=False):
        return b""

    with controller_fixture() as fixture:
        with mock.patch.object(sealed_module, "read_regular_single_link", truncating):
            return expect_rejection(
                "WP149-NEG-061-short-read-is-refused",
                fixture.build,
                "sealed_input_short_read",
            )


# ── negatives: interface forgery, inventory and evidence ────────────────────


@case("WP149-NEG-054-direct-construction", "immutable_launch_envelope_interface")
def negative_direct_construction():
    return expect_rejection(
        "WP149-NEG-054-direct-construction",
        lambda: LaunchEnvelope(
            schema_version=1,
            executable="C:\\attacker\\claude.exe",
            arguments=("claude",),
            working_directory="C:\\attacker",
            stdin_path="C:\\attacker\\prompt.md",
            environment={},
            sealed_inputs=(),
            inventory_digest="0" * 64,
            evidence_json="{}",
            evidence_sha256="0" * 64,
        ),
        "envelope_unsealed",
    )


@case("WP149-NEG-055-dataclass-replace", "immutable_launch_envelope_interface")
def negative_dataclass_replace():
    with controller_fixture() as fixture:
        envelope = fixture.build()
        return expect_rejection(
            "WP149-NEG-055-dataclass-replace",
            lambda: dataclasses.replace(envelope, executable="C:\\attacker\\claude.exe"),
            "envelope_unsealed",
        )


@case("WP149-NEG-056-shallow-copy", "immutable_launch_envelope_interface")
def negative_shallow_copy():
    with controller_fixture() as fixture:
        envelope = fixture.build()
        return expect_rejection(
            "WP149-NEG-056-shallow-copy",
            lambda: copy.copy(envelope),
            "envelope_unsealed",
        )


@case("WP149-NEG-057-deep-copy", "immutable_launch_envelope_interface")
def negative_deep_copy():
    with controller_fixture() as fixture:
        envelope = fixture.build()
        return expect_rejection(
            "WP149-NEG-057-deep-copy",
            lambda: copy.deepcopy(envelope),
            "envelope_unsealed",
        )


@case("WP149-NEG-058-inventory-omission-changes-the-digest", "source_inventory_and_static_boundary")
def negative_inventory_omission():
    with tempfile.TemporaryDirectory(prefix="wp149-inventory-") as temporary:
        root = pathlib.Path(temporary).resolve()
        first = root / "alpha.py"
        second = root / "beta.py"
        first.write_bytes(b"alpha\n")
        second.write_bytes(b"beta\n")
        full = inventory_module.inventory_of(root)
        second.chmod(stat.S_IREAD | stat.S_IWRITE)
        second.unlink()
        reduced = inventory_module.inventory_of(root)
        ensure(full["file_count"] == 2, "the inventory fixture did not measure both files")
        ensure(reduced["file_count"] == 1, "the inventory did not notice a removed file")
        ensure(full["digest"] != reduced["digest"], "an omitted file left the digest unchanged")
        third = root / "alpha.py"
        third.chmod(stat.S_IREAD | stat.S_IWRITE)
        third.write_bytes(b"alpha modified\n")
        modified = inventory_module.inventory_of(root)
        ensure(modified["digest"] != reduced["digest"], "a modified byte left the digest unchanged")
        return {
            "full_digest": full["digest"],
            "reduced_digest": reduced["digest"],
            "modified_digest": modified["digest"],
        }


@case("WP149-NEG-059-evidence-tamper-breaks-the-digest", "immutable_launch_envelope_interface")
def negative_evidence_tamper():
    with controller_fixture() as fixture:
        envelope = fixture.build()
        tampered = envelope.as_evidence()
        tampered["permission_mode"] = "bypassPermissions"
        raw = json.dumps(tampered, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        ensure(
            sha256_of(raw.encode("utf-8")) != envelope.evidence_sha256,
            "tampered evidence kept the retained digest",
        )
        ensure(
            envelope.as_evidence()["permission_mode"] == "dontAsk",
            "the tampered copy leaked back into the envelope",
        )
        return {"retained": envelope.evidence_sha256, "tampered": sha256_of(raw.encode("utf-8"))}


@case("WP149-NEG-060-inventory-prefix-must-be-the-write-set", "source_inventory_and_static_boundary")
def negative_inventory_prefix():
    with mock.patch.object(inventory_module, "ENVELOPE_PREFIX", "docs/other/"):
        return expect_rejection(
            "WP149-NEG-060-inventory-prefix-must-be-the-write-set",
            inventory_module.envelope_inventory,
            "inventory_prefix",
        )


def main() -> int:
    records = []
    failed = 0
    executed = 0
    for case_id, check, function in CASES:
        executed += 1
        try:
            evidence = function()
        except Exception as exc:  # noqa: BLE001 - every failure becomes a named red record
            failed += 1
            records.append(
                {
                    "case_id": case_id,
                    "check": check,
                    "status": "failed",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
        else:
            records.append(
                {"case_id": case_id, "check": check, "status": "passed", "evidence": evidence}
            )
    report = {
        "schema_version": 1,
        "suite": "wp149_launch_envelope_matrix",
        "optimized": not __debug__,
        "scheduled": len(CASES),
        "executed": executed,
        "passed": executed - failed,
        "failed": failed,
        "skipped": 0,
        "not_run": len(CASES) - executed,
        "required_checks": list(REQUIRED_CHECKS),
        "external_gates": list(EXTERNAL_GATES),
        # Hoisted out of `records` deliberately.  A failure buried inside sixty kilobytes of
        # passing evidence is a failure the reader has to go looking for, and the key sorts before
        # `records` so it survives any consumer that truncates a long line.
        "failures": [
            {
                "case_id": record["case_id"],
                "check": record["check"],
                "error_type": record.get("error_type"),
                "error": record.get("error"),
            }
            for record in records
            if record["status"] == "failed"
        ],
        "records": records,
    }
    report["ok"] = (
        report["scheduled"] > 0
        and report["executed"] == report["scheduled"]
        and report["passed"] == report["scheduled"]
        and report["failed"] == 0
        and report["skipped"] == 0
        and report["not_run"] == 0
    )
    # ASCII-escaped on purpose.  The fixtures carry Vietnamese path segments, and a Windows console
    # on a cp1258 code page cannot encode them: the suite would then die IN ITS OWN REPORT LINE
    # after every case had already passed, turning a green run into an encoding traceback.  The
    # escapes are still exact JSON, so the machine reader loses nothing.
    print(json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
