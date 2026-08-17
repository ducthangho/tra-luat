"""Narrow, credential-free Linux delegation of exactly one operation (Issue 125 §7).

Windows is the primary platform.  Delegation exists for the single case where preflight *proved* no
usable Windows sandbox path exists, and it carries exactly one operation: ``run_test``.

The operation set is closed and the refusals are by name.  A denylist would be wrong here for the
same reason it was wrong for the child environment: the interesting failure is the operation nobody
listed.  ``FORBIDDEN_OPERATIONS`` exists anyway, on top of the closed set, so that the *reason* a
delegated claim or a delegated merge is refused appears in evidence as a named category instead of
as a generic "unknown operation" — an auditor reading the matrix should be able to see that the
question was asked.

Credential-freedom is *probed*, not asserted.  The controller plants a credential-shaped marker in
the parent environment and the job reports the environment names it actually received; the evidence
is the marker's absence observed from inside the job.  Asserting "we filtered it" proves the filter
was called, which is the weaker claim and the one that stays true after the filter breaks.

Candidate-authored summaries are not proof.  Every field in the returned evidence is either measured
by the controller (return code, timing, hashes) or is a controller input echoed back for binding
(commit, tree, test selection).  Nothing the job *says about itself* is load-bearing.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import pathlib
import platform
import stat
from collections.abc import Mapping, Sequence

from oracle.safe_io import git, require_outside_tree

from .environment import MEMORY_VARIABLE, build_child_environment, credential_shaped
from .errors import reject
from .watchdog import Deadline, python_executable, run_supervised

DELEGABLE_OPERATIONS = frozenset({"run_test"})

# Read once from the one typed pin, so this module states no identity of its own.  A second copy of
# the repository name here is exactly the parallel constant table WP125-RV-006-R5 is about.
from .sourcepin import PIN as _PIN  # noqa: E402

PIN_REPOSITORY = _PIN.repository
PIN_CANDIDATE_REF = _PIN.candidate_ref

# Named refusals.  Each of these is a thing someone could plausibly want to delegate on a bad day,
# and each would move authority off the controller and onto a runner the Packet does not trust.
FORBIDDEN_OPERATIONS = (
    "claim",
    "heartbeat",
    "verdict",
    "github_write",
    "source_mutation",
    "branch_operation",
    "ref_operation",
    "pr_operation",
    "controller_execution",
    "model_invocation",
    "merge",
    "land",
    "deploy",
    "live",
)

# A credential-shaped value the controller plants in the parent environment so the job can prove it
# did not receive it.  The name is credential-shaped on purpose: it must be caught by the same rule
# that catches a real one.
MARKER_NAME = "GITHUB_TOKEN"
MARKER_VALUE = "wp125-credential-marker-must-not-reach-the-delegated-job"

BOOTSTRAP_RELATIVE = ".github/coordination/reviewer_bootstrap"

# WP125-RV-002.  The delegated side used to be one literal probe that printed a report and exited
# zero no matter what, while `test_selection` rode along in argv and was never executed.  That is a
# job which cannot fail, and a job which cannot fail is not evidence of anything.
#
# The replacement is a closed, controller-authored map from a declared test ID to the program that
# actually implements it.  The map lives here, in trusted code, so the *caller* selects an ID and
# never supplies a command; an unknown ID is refused rather than passed through.  Each program
# returns a real process exit code that the controller records, so a failing check makes the job
# red instead of decorating a green one.
_SRC_IMPORT_SMOKE = """
import json, sys
sys.path.insert(0, sys.argv[1])
try:
    from launcher import argv, delegation, environment, inventory, parity, preflight, registry, watchdog
except Exception as exc:
    print("WP125-DELEGATED-TEST " + json.dumps({"test": "launcher_import_smoke", "ok": False, "error": type(exc).__name__}))
    raise SystemExit(1)
print("WP125-DELEGATED-TEST " + json.dumps({"test": "launcher_import_smoke", "ok": True, "modules": 8}))
raise SystemExit(0)
"""

_SRC_REGISTRY_COVERAGE = """
import json, sys
sys.path.insert(0, sys.argv[1])
from launcher import registry
coverage = registry.check_coverage()
print("WP125-DELEGATED-TEST " + json.dumps({"test": "launcher_registry_coverage", "ok": bool(coverage["ok"]), "cases": coverage["case_count"]}))
raise SystemExit(0 if coverage["ok"] else 1)
"""

_SRC_STATIC_BOUNDARY = """
import json, pathlib, sys
sys.path.insert(0, sys.argv[1])
from launcher import inventory
scan = inventory.scan_package(pathlib.Path(sys.argv[1]) / "launcher")
print("WP125-DELEGATED-TEST " + json.dumps({"test": "launcher_static_boundary", "ok": bool(scan["ok"]), "findings": len(scan["findings"])}))
raise SystemExit(0 if scan["ok"] else 1)
"""

DELEGATED_TESTS: Mapping[str, str] = {
    "launcher_import_smoke": _SRC_IMPORT_SMOKE,
    "launcher_registry_coverage": _SRC_REGISTRY_COVERAGE,
    "launcher_static_boundary": _SRC_STATIC_BOUNDARY,
}

DELEGATED_TEST_IDS: tuple[str, ...] = tuple(sorted(DELEGATED_TESTS))


@dataclasses.dataclass(frozen=True)
class DelegatedJob:
    """A fully-resolved delegated job.  Frozen for the same reason as the launch plan: it is evidence."""

    operation: str
    candidate_head: str
    candidate_tree: str
    test_selection: tuple[str, ...]
    commands: tuple[tuple[str, ...], ...]
    read_only_root: str
    expected_os: str
    root_evidence: Mapping[str, object]

    def as_dict(self) -> dict[str, object]:
        return {
            "operation": self.operation,
            "candidate_head": self.candidate_head,
            "candidate_tree": self.candidate_tree,
            "test_selection": list(self.test_selection),
            "commands": [list(command) for command in self.commands],
            "read_only_root": self.read_only_root,
            "expected_os": self.expected_os,
            "root_evidence": dict(self.root_evidence),
        }


def _root_error(message: str):
    return reject("delegation_scope", message)


def trust_paths(*paths: object) -> tuple[str, ...]:
    """Every directory git must be allowed to open in order to serve these worktrees.

    WP125-GATE-001-R4.  Round 3 declared the worktree and its linked gitdir and stopped there, which
    is enough for a direct ``rev-parse`` and *not* enough for a clone.  A linked worktree's gitdir
    holds only that worktree's refs and HEAD; the object database lives in the **common** gitdir, and
    a clone — including the ``upload-pack`` the ``file://`` transport starts inside the source — has
    to open it.  So the direct check went green while the nested clone was refused, which is exactly
    the split the round-4 evidence reports.

    Measured on this host: the source worktree's gitdir is
    ``D:/Quốc hội/tra-luat/.git/worktrees/<name>`` and its common dir is ``D:/Quốc hội/tra-luat/.git``
    — both non-ASCII, and only the first was ever declared.

    The ``commondir`` pointer is usually relative (``../..``), so it is resolved against the linked
    gitdir rather than used as written; a relative path handed to ``safe.directory`` matches nothing.
    """
    found: list[str] = []

    def add(value: object) -> None:
        if value is None:
            return
        text = pathlib.Path(str(value)).as_posix()
        if text and text not in found:
            found.append(text)

    for raw in paths:
        if not raw:
            continue
        path = pathlib.Path(str(raw)).resolve()
        add(path)
        marker = path / ".git"
        try:
            if marker.is_dir():
                add(marker)
                continue
            if not marker.is_file():
                continue
            pointer = marker.read_text(encoding="utf-8").strip()
            if not pointer.startswith("gitdir:"):
                continue
            linked_raw = pointer.split(":", 1)[1].strip()
            linked = pathlib.Path(linked_raw)
            if not linked.is_absolute():
                linked = (path / linked).resolve()
            add(linked)

            # The common gitdir: where the objects actually are.
            common_file = linked / "commondir"
            if common_file.is_file():
                common_raw = common_file.read_text(encoding="utf-8").strip()
                common = pathlib.Path(common_raw)
                if not common.is_absolute():
                    common = (linked / common).resolve()
                add(common)
                # And the main worktree that owns that common dir, since git checks the enclosing
                # directory when it resolves a repository through it.
                if common.name == ".git":
                    add(common.parent)
        except OSError:
            continue
    return tuple(found)


_AMBIENT_TRUST: dict[str, object] = {}


def ambient_trust_env(*paths: object, base: Mapping[str, str] | None = None) -> dict[str, str]:
    """Trust environment for direct git calls, backed by one per-process ephemeral config.

    ``safe_directory_args`` used to live here and produced ``-c safe.directory=`` arguments.  Those
    do work for the process they configure, but they cannot be handed to the RA-02 reader, which
    takes no extra arguments and no environment — so one inheritable mechanism is used everywhere
    rather than two that differ by call site.
    """
    import tempfile

    entries = trust_paths(*paths)
    directory = _AMBIENT_TRUST.get("dir")
    if directory is None:
        directory = tempfile.mkdtemp(prefix="wp125-trust-")
        _AMBIENT_TRUST["dir"] = directory
        _AMBIENT_TRUST["entries"] = []
    known = list(_AMBIENT_TRUST["entries"])
    for entry in entries:
        if entry not in known:
            known.append(entry)
    _AMBIENT_TRUST["entries"] = known
    config = pathlib.Path(str(directory)) / "ambient.gitconfig"
    config.write_text(
        "[safe]\n" + "".join("\tdirectory = %s\n" % entry for entry in known),
        encoding="utf-8",
        newline="\n",
    )
    return trust_env(config, base)


def write_trust_config(directory: object, *paths: object) -> str:
    """Write an ephemeral git *global* config granting trust for exactly these paths.

    WP125-GATE-001-R4.  Measured, with the ownership check forced on via
    ``GIT_TEST_ASSUME_DIFFERENT_OWNER``:

    * ``-c safe.directory=…`` **does** configure the process it is given to — a direct
      ``rev-parse`` succeeds with it.  That is exactly why round 3's direct verification was green.
    * It does **not** reach the ``upload-pack`` git starts *inside the source repository* for a
      ``file://`` clone, and neither does this ephemeral global config.  The nested clone fails there
      with "Could not read from remote repository" — the split the round-4 evidence reports.

    So the grant is not the defect; the transport is (see :func:`clone_source_argument`).  This file
    exists because the grant should still be complete and inheritable for everything else, and
    because ``GIT_CONFIG_GLOBAL`` lets us supply it without touching the user's real global config or
    the repository's own.  The substitute lives in the run's scratch directory and dies with it.
    """
    target = pathlib.Path(str(directory)) / "wp125-trust.gitconfig"
    entries = trust_paths(*paths)
    body = "[safe]\n" + "".join("\tdirectory = %s\n" % entry for entry in entries)
    target.write_text(body, encoding="utf-8", newline="\n")
    return str(target)


def trust_env(config_path: object, base: Mapping[str, str] | None = None) -> dict[str, str]:
    """Environment that points git at the ephemeral global config, and only at that."""
    env = dict(base if base is not None else os.environ)
    env["GIT_CONFIG_GLOBAL"] = str(config_path)
    return env


def clone_source_argument(source: object) -> str:
    """The plain local path, never a ``file://`` URL.

    WP125-GATE-001-R4.  ``file://`` selects the transport machinery, which starts ``upload-pack``
    *inside the source repository* — a separate process that performs its own ownership check and
    does not inherit the caller's grant.  Measured against a git forced to run the check: the
    ``file://`` clone fails in that child with "Could not read from remote repository" while a clone
    of the same source by plain path succeeds.  The URL bought nothing here and cost the whole
    nested boundary.
    """
    return str(pathlib.Path(str(source)))


def verify_read_only_root(
    read_only_root: str,
    *,
    candidate_root: str,
    candidate_head: str,
    candidate_tree: str,
) -> dict[str, object]:
    """Prove the delegated root exists, is genuinely not writable, and is the exact candidate.

    Writability is measured by *attempting a write*, because on Windows nothing cheaper is true.
    Measured on this host: a directory that has been ``chmod``-ed to ``0o555`` still reports
    ``os.access(path, os.W_OK) == True`` and still accepts file creation.  A control built on mode
    bits or ``os.access`` would therefore certify a fully writable directory as read-only — the same
    shape of fake green this finding is about.  The probe is refused *before* it runs unless the root
    lies outside the live candidate worktree, so the one side effect it can have is a sentinel file
    inside a directory whose read-only declaration was already false, and even that is removed.
    """
    path = pathlib.Path(read_only_root)
    if not path.is_absolute():
        raise _root_error("the delegated read-only root must be an absolute path")
    require_outside_tree(path, candidate_root, "delegated read-only root", _root_error)
    try:
        info = path.lstat()
    except OSError as exc:
        raise _root_error("the delegated read-only root does not exist") from exc
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise _root_error("the delegated read-only root is a link or reparse point")
    if not path.is_dir():
        raise _root_error("the delegated read-only root is not a directory")

    sentinel = path / ("wp125-writability-probe-%d.tmp" % os.getpid())
    writable = False
    try:
        with open(sentinel, "xb") as handle:
            handle.write(b"probe")
        writable = True
    except OSError:
        writable = False
    finally:
        try:
            sentinel.unlink()
        except OSError:
            pass
    if writable:
        raise _root_error("the delegated read-only root accepted a write and is not read-only")

    # `binary=True` so the shared reader never decodes git's output through the console code page.
    # On this host that is cp1258, and a delegated root under a Unicode path makes git quote bytes it
    # cannot represent — which would surface as a decoding crash instead of a typed rejection, from
    # the one call whose whole job is to answer an identity question about that path.
    # The shared RA-02 reader does not take an environment, so the trust is installed into this
    # process's own environment for the duration of the two reads. Nothing is written to any git
    # configuration file that outlives the run.
    previous = os.environ.get("GIT_CONFIG_GLOBAL")
    os.environ.update(
        {"GIT_CONFIG_GLOBAL": ambient_trust_env(path)["GIT_CONFIG_GLOBAL"]}
    )
    try:
        head = git(path, "rev-parse", "HEAD", error=_root_error, binary=True).decode("utf-8").strip()
        tree = (
            git(path, "rev-parse", "HEAD^{tree}", error=_root_error, binary=True)
            .decode("utf-8")
            .strip()
        )
    finally:
        if previous is None:
            os.environ.pop("GIT_CONFIG_GLOBAL", None)
        else:
            os.environ["GIT_CONFIG_GLOBAL"] = previous
    if head != candidate_head:
        raise _root_error("the delegated root is at a different commit than the candidate")
    if tree != candidate_tree:
        raise _root_error("the delegated root is at a different tree than the candidate")
    return {
        "root": str(path),
        "writability_probe": "refused",
        "head": head,
        "tree": tree,
        "identity_verified_by": "controller",
    }


def build_expected_commands(
    test_selection: Sequence[str], read_only_root: str
) -> tuple[tuple[str, ...], ...]:
    """Reconstruct the argument vectors for a selection, from the closed map alone.

    The single source of truth for what a delegated test *is*.  Used both when the job is built and
    again when the controller authenticates it, so "the job's commands" can be compared against
    something the job had no hand in producing (WP125-RV-008-R3).
    """
    bootstrap = str(pathlib.Path(read_only_root) / BOOTSTRAP_RELATIVE)
    unknown = [item for item in test_selection if item not in DELEGATED_TESTS]
    if unknown:
        raise reject("delegation_scope", "%d test ids are outside the closed map" % len(unknown))
    return tuple(
        (python_executable(), "-c", DELEGATED_TESTS[item], bootstrap) for item in test_selection
    )


def validate_operation(operation: object) -> str:
    """Accept only the one delegable operation; refuse everything else by name."""
    if not isinstance(operation, str) or not operation:
        raise reject("delegation_scope", "the delegated operation must be a non-empty string")
    if operation in FORBIDDEN_OPERATIONS:
        raise reject("delegation_scope", "operation %r is explicitly not delegable" % (operation,))
    if operation not in DELEGABLE_OPERATIONS:
        raise reject("delegation_scope", "operation %r is outside the closed delegable set" % (operation,))
    return operation


def build_job(
    *,
    operation: str,
    candidate_head: str,
    candidate_tree: str,
    test_selection: Sequence[str],
    read_only_root: str,
    eligible: bool,
    candidate_root: str,
    expected_os: str,
) -> DelegatedJob:
    """Build the job, or refuse.

    ``eligible`` is the preflight verdict, passed in rather than recomputed.  Recomputing it here
    would give this module a second opinion about whether delegation is allowed, and two opinions is
    one more than a fail-closed boundary can afford.
    """
    if not eligible:
        raise reject("delegation_scope", "delegation was attempted without preflight eligibility")
    name = validate_operation(operation)
    if expected_os not in ("Windows", "Linux"):
        raise reject("delegation_scope", "expected_os %r is not a declared runner OS" % (expected_os,))
    if not test_selection:
        raise reject("delegation_evidence", "the delegated job declares no test selection")

    selection = tuple(str(item) for item in test_selection)
    for item in selection:
        # WP125-RV-002: membership in the closed map, not a shape heuristic. Generation 1 accepted
        # anything that was neither switch-shaped nor traversal-shaped and then never ran it, so a
        # plausible-looking string bought a green job.
        if item not in DELEGATED_TESTS:
            raise reject(
                "delegation_scope",
                "test %r is not in the closed controller-authored test map" % (item,),
            )
    if len(set(selection)) != len(selection):
        raise reject("delegation_evidence", "the delegated test selection repeats an entry")

    root_evidence = verify_read_only_root(
        read_only_root,
        candidate_root=candidate_root,
        candidate_head=candidate_head,
        candidate_tree=candidate_tree,
    )
    commands = build_expected_commands(selection, read_only_root)
    return DelegatedJob(
        operation=name,
        candidate_head=candidate_head,
        candidate_tree=candidate_tree,
        test_selection=selection,
        commands=commands,
        read_only_root=str(pathlib.Path(read_only_root)),
        expected_os=expected_os,
        root_evidence=root_evidence,
    )


# The credential probe.  This is deliberately *separate* from the declared tests above: its job is
# to report, from inside the job, which environment names arrived, so the controller's claim that it
# filtered the planted marker is checked against an observation rather than restated.  It carries no
# pass/fail of its own — the tests do that, with real exit codes.
_PROBE_SOURCE = """
import json, os, platform, sys

names = sorted(os.environ)
report = {
    "environment_names": names,
    "credential_marker_present": "GITHUB_TOKEN" in os.environ,
    "credential_shaped_names": [
        name for name in names
        if any(part in name.upper() for part in ("TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "COOKIE"))
    ],
    "automatic_memory": os.environ.get("CLAUDE_CODE_DISABLE_AUTO_MEMORY"),
    "runner": {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    },
    "write_attempted": False,
}
print("WP125-DELEGATED-REPORT " + json.dumps(report, sort_keys=True))
"""


def run_job(
    job: DelegatedJob,
    *,
    parent_environment: Mapping[str, str],
    candidate_root: str,
    working_directory: str,
    deadline: Deadline,
) -> dict[str, object]:
    """Run the delegated job under the controller's watchdog and return measured evidence.

    Refuses outright when the runner is not the OS the job was built for.  §7 forbids fabricating
    delegated Linux execution, and the only way to honour that on a Windows host is to make a
    Linux-declared job fail here rather than quietly run somewhere else and be reported as Linux.
    """
    actual_os = platform.system()
    if actual_os != job.expected_os:
        raise reject(
            "delegation_scope",
            "the runner is %r but the job was built for %r" % (actual_os, job.expected_os),
        )

    parent = dict(parent_environment)
    parent[MARKER_NAME] = MARKER_VALUE  # planted so its absence downstream is a measurement
    environment = build_child_environment(parent, candidate_root=candidate_root)

    leaked = sorted(name for name in environment if credential_shaped(name))
    if leaked:
        raise reject("delegation_credential", "%d credential-shaped names reached the job" % len(leaked))

    # The credential probe first, then every declared test, each with its own real exit code.
    probe = run_supervised(
        (python_executable(), "-c", _PROBE_SOURCE),
        environment=environment,
        working_directory=working_directory,
        deadline=deadline,
        label="delegated-credential-probe",
    )

    per_test: list[dict[str, object]] = []
    for test_id, command in zip(job.test_selection, job.commands):
        outcome = run_supervised(
            command,
            environment=environment,
            working_directory=working_directory,
            deadline=deadline,
            label="delegated-%s" % test_id,
        )
        per_test.append(
            {
                "test_id": test_id,
                "return_code": outcome.return_code,
                "status": outcome.status,
                "fenced": outcome.fenced,
                "cleanup": outcome.cleanup,
                "report": _test_report_line(outcome.stdout_text, test_id),
            }
        )

    failed = [item for item in per_test if item["return_code"] != 0]
    evidence = {
        "job": job.as_dict(),
        "runner_os": actual_os,
        "expected_os": job.expected_os,
        "per_test": per_test,
        "return_codes": {item["test_id"]: item["return_code"] for item in per_test},
        "tests_executed": len(per_test),
        "tests_failed": len(failed),
        "probe_return_code": probe.return_code,
        "status": "passed" if not failed and probe.return_code == 0 else "failed",
        "timeout_source": "controller",
        "cleanup": probe.cleanup,
        "runner_fingerprint": {
            "controller_system": platform.system(),
            "controller_release": platform.release(),
            "controller_machine": platform.machine(),
            "os_name": os.name,
        },
        "credential_marker_planted": True,
        "marker_name": MARKER_NAME,
        "environment_memory_variable": MEMORY_VARIABLE,
        "candidate_summary_is_proof": False,
    }
    # The job's self-report is audited against what the controller independently knows it planted.
    # Only the audited summary is retained — names and booleans, never values.
    evidence["job_report"] = audit_job_report(probe.stdout_text, evidence)
    evidence["runner"] = evidence["job_report"].get("runner")
    if failed:
        raise reject(
            "delegation_evidence",
            "%d of %d declared delegated tests returned a non-zero code"
            % (len(failed), len(per_test)),
        )
    evidence["evidence_sha256"] = hashlib.sha256(
        json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return evidence


# --------------------------------------------------------------------------- the transport
#
# WP125-RV-008-R5.  Round 4 declared a transport and never called it.  `context` carried
# ``delegated_linux_transport``, the controller asked whether it was truthy, and then ran the job on
# whatever machine it happened to be sitting on — so on Linux the delegated result was a local
# result with a Linux label, and on Windows the surface was unreachable by construction.  A declared
# transport that is never invoked is not a boundary; it is a comment with a truthiness check.
#
# What follows is the boundary.  An envelope is a sealed object bound to the pin, carrying exactly
# one closed operation and a `dispatch` method the controller *calls*.  What crosses is a request
# naming the operation, the pin digest, the closed test-ID selection and the read-only root — no
# command line, no model invocation, no claim, no ref, no credential.  What comes back is measured
# at the far side and re-bound here against the pin and against the controller's own closed map, so
# a far side that lies about its OS, its root, its head, its tree, its selection or its return codes
# is refused rather than believed.

TRANSPORT_CONTRACT = "wp125.linux_run_test_transport.v1"

# The two honest modes a piece of transport evidence can be in, and they are not interchangeable.
# `production_linux` is a real authenticated Linux runner.  `offline_test_double` is a controller-
# owned stand-in that exists to prove the contract is actually called and actually rejects bad
# answers; §7 forbids it from ever standing in for the first, so the mode travels with the evidence
# and the retained receipt names it.
TRANSPORT_MODES = ("production_linux", "offline_test_double")


@dataclasses.dataclass(frozen=True)
class TransportRequest:
    """Exactly what may cross the boundary.  Frozen, and it is evidence."""

    contract: str
    operation: str
    pin_digest: str
    receipt_sha256: str
    repository: str
    candidate_ref: str
    candidate_head: str
    candidate_tree: str
    read_only_root: str
    test_selection: tuple[str, ...]
    deadline_seconds: float

    def as_dict(self) -> dict[str, object]:
        return {
            "contract": self.contract,
            "operation": self.operation,
            "pin_digest": self.pin_digest,
            "receipt_sha256": self.receipt_sha256,
            "repository": self.repository,
            "candidate_ref": self.candidate_ref,
            "candidate_head": self.candidate_head,
            "candidate_tree": self.candidate_tree,
            "read_only_root": self.read_only_root,
            "test_selection": list(self.test_selection),
            "deadline_seconds": self.deadline_seconds,
        }

    def request_hash(self) -> str:
        return hashlib.sha256(
            json.dumps(
                self.as_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode("utf-8")
        ).hexdigest()


def pin_digest() -> str:
    """A digest of the one typed pin, so evidence can be bound to it without restating it."""
    from .sourcepin import PIN

    return hashlib.sha256(
        json.dumps(
            PIN.sealed_document(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def authenticate_transport(envelope: object, context: Mapping[str, object]) -> dict[str, object]:
    """Authenticate a transport envelope against the sealed pin, or fail closed.

    A truthy value is not a transport.  An arbitrary callable is not a transport either: a bare
    callable can be handed a request and return anything, and "the caller supplied a function" is not
    an authority statement.  What is required is an object that declares this contract, declares the
    one closed operation, binds itself to the pin digest this controller computes for itself, and
    exposes ``dispatch``.
    """
    if envelope is None:
        raise reject(
            "sandbox_unavailable",
            "environment_unavailable: no authenticated Linux transport is configured",
        )
    if getattr(envelope, "contract", None) != TRANSPORT_CONTRACT:
        raise reject("transport_authority", "the transport does not declare the closed contract")
    if getattr(envelope, "operation", None) != "run_test":
        raise reject(
            "transport_authority", "the transport is not bound to the closed run_test operation"
        )
    mode = getattr(envelope, "mode", None)
    if mode not in TRANSPORT_MODES:
        raise reject("transport_authority", "the transport declares no known evidence mode")
    expected = pin_digest()
    if getattr(envelope, "pin_digest", None) != expected:
        raise reject("transport_authority", "the transport is not sealed to this Packet's pin")
    dispatch = getattr(envelope, "dispatch", None)
    if not callable(dispatch):
        raise reject("transport_authority", "the transport exposes no dispatch capability")
    if getattr(envelope, "repository", None) != str(context.get("repository", PIN_REPOSITORY)):
        raise reject("transport_authority", "the transport names a different repository")
    return {
        "contract": TRANSPORT_CONTRACT,
        "operation": "run_test",
        "mode": mode,
        "pin_digest": expected,
        "dispatch_is_callable": True,
        "authenticated_before_dispatch": True,
    }


def _remote_error(message: str):
    return reject("delegation_evidence", message)


def dispatch_run_test(
    envelope: object,
    *,
    job: DelegatedJob,
    context: Mapping[str, object],
    deadline: Deadline,
    receipt_sha256: str,
    authentication: Mapping[str, object],
) -> dict[str, object]:
    """Call the authenticated transport, then bind what it returns.  Nothing runs locally here.

    Every transport/authentication/routing/root/selection check has already finished, and
    :func:`authenticate_transport` is called again immediately below so the window between the last
    check and the dispatch contains no unchecked state.  The evidence that comes back is treated as
    an untrusted claim: the OS, root, head, tree, selection and return codes are all re-derived
    against the controller's own closed map and the sealed pin before any of it is retained.
    """
    identity = authenticate_transport(envelope, context)
    if identity != dict(authentication["transport_identity"]):
        raise reject("transport_authority", "the transport identity changed before dispatch")

    request = TransportRequest(
        contract=TRANSPORT_CONTRACT,
        operation="run_test",
        pin_digest=identity["pin_digest"],
        receipt_sha256=receipt_sha256,
        repository=PIN_REPOSITORY,
        candidate_ref=PIN_CANDIDATE_REF,
        candidate_head=job.candidate_head,
        candidate_tree=job.candidate_tree,
        read_only_root=job.read_only_root,
        test_selection=tuple(job.test_selection),
        deadline_seconds=round(float(deadline.requested_seconds), 3),
    )
    # Nothing forbidden may be named in a request. This is a closed set on the way out as well as on
    # the way in, so a request that acquired an extra field cannot quietly carry one.
    for forbidden in FORBIDDEN_OPERATIONS:
        if forbidden in request.as_dict():
            raise reject("delegation_scope", "the transport request names a forbidden operation")

    answer = envelope.dispatch(request)
    return bind_transport_evidence(
        answer, request=request, job=job, mode=identity["mode"], deadline=deadline
    )


def bind_transport_evidence(
    answer: object,
    *,
    request: TransportRequest,
    job: DelegatedJob,
    mode: str,
    deadline: Deadline,
) -> dict[str, object]:
    """Re-derive every load-bearing field of a transport answer.  The far side is not believed.

    The far side measured; this decides.  Each check below names a way an answer could be wrong that
    a weaker check would have accepted — most of all ``runner_os``, which round 4 read from
    ``platform.system()`` on the *controller* and therefore never learned anything about the runner.
    """
    if not isinstance(answer, Mapping):
        raise _remote_error("the transport returned no evidence")
    if answer.get("request_hash") != request.request_hash():
        raise _remote_error("the transport evidence answers a different request")
    if answer.get("runner_os") != "Linux":
        raise reject(
            "delegation_scope",
            "the transport ran on %r; the delegated surface is Linux-only" % (answer.get("runner_os"),),
        )
    if answer.get("measured_at") != "remote_runner":
        raise _remote_error("the transport evidence was not measured at the runner")
    if answer.get("head") != request.candidate_head or answer.get("tree") != request.candidate_tree:
        raise reject("delegation_scope", "the runner is not at the candidate commit and tree")
    if answer.get("read_only_root_probe") != "refused":
        raise reject("delegation_scope", "the runner did not prove a read-only root by writing to it")
    if answer.get("credential_marker_present") is not False:
        raise reject("delegation_credential", "a credential reached the delegated runner")
    if answer.get("credential_shaped_names"):
        raise reject(
            "delegation_credential",
            "%d credential-shaped names were observed at the runner"
            % len(answer["credential_shaped_names"]),
        )
    # The child-environment contract holds across the boundary too, and a field that is retained but
    # never compared is the shape every one of these rounds has been about.
    if answer.get("automatic_memory") != "1":
        raise reject("child_environment", "the runner did not observe the memory variable as 1")
    fingerprint = answer.get("runner")
    if not isinstance(fingerprint, Mapping) or fingerprint.get("system") != "Linux":
        raise _remote_error("the runner fingerprint disagrees with the reported runner OS")

    # The selection is reconstructed from the controller's closed map, not read out of the answer.
    reconstructed = tuple(job.test_selection)
    reported = tuple(answer.get("test_selection") or ())
    if reported != reconstructed:
        raise reject("delegation_scope", "the runner ran a different selection than the closed map")
    unknown = [item for item in reported if item not in DELEGATED_TESTS]
    if unknown:
        raise reject("delegation_scope", "the runner reports %d tests outside the map" % len(unknown))

    codes = answer.get("return_codes")
    if not isinstance(codes, Mapping) or sorted(codes) != sorted(reconstructed):
        raise _remote_error("the transport evidence has no return code for each declared test")
    if not all(isinstance(value, int) for value in codes.values()):
        raise _remote_error("the transport evidence carries a return code that is not an integer")
    failed = sorted(test for test, value in codes.items() if value != 0)

    if answer.get("deadline_source") != "controller":
        raise _remote_error("the runner did not run under the controller's deadline")
    if answer.get("cleanup_proven") is not True:
        raise reject("watchdog_cleanup", "the runner did not prove it cleaned up")
    if deadline.expired():
        raise reject("lease_expired", "the controller deadline passed while the transport ran")

    evidence = {
        "transport_contract": TRANSPORT_CONTRACT,
        "transport_invoked": True,
        "transport_mode": mode,
        "is_real_production_linux_transport": mode == "production_linux",
        "request": request.as_dict(),
        "request_hash": request.request_hash(),
        "runner_os": "Linux",
        "expected_os": job.expected_os,
        "job": job.as_dict(),
        "test_selection": list(reconstructed),
        "return_codes": dict(codes),
        "tests_executed": len(reconstructed),
        "tests_failed": len(failed),
        "per_test": [
            {"test_id": test, "return_code": codes[test], "measured_at": "remote_runner"}
            for test in reconstructed
        ],
        "status": "passed" if not failed else "failed",
        "timeout_source": "controller",
        "deadline_source": "controller",
        "cleanup": {"cleanup_proven": True, "measured_at": "remote_runner"},
        "runner": answer.get("runner"),
        "credential_marker_planted": True,
        "marker_name": MARKER_NAME,
        "environment_memory_variable": MEMORY_VARIABLE,
        "job_report": {
            "observed_from_inside_job": True,
            "credential_marker_present": False,
            "credential_shaped_names": [],
            "automatic_memory": answer.get("automatic_memory"),
            "runner": answer.get("runner"),
        },
        "candidate_summary_is_proof": False,
    }
    if failed:
        raise reject(
            "delegation_evidence",
            "%d of %d delegated tests returned a non-zero code at the runner"
            % (len(failed), len(reconstructed)),
        )
    evidence["evidence_sha256"] = hashlib.sha256(
        json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return evidence


def _test_report_line(stdout_text: str, test_id: str) -> dict[str, object]:
    """Extract the declared test's own machine-readable line, for context only.

    The verdict comes from the process exit code above; this is recorded so an auditor can see what
    the test said, not so the controller can believe it.
    """
    prefix = "WP125-DELEGATED-TEST "
    for line in str(stdout_text).splitlines():
        index = line.find(prefix)
        if index < 0:
            continue
        try:
            payload = json.loads(line[index + len(prefix) :].strip())
        except ValueError:
            continue
        if payload.get("test") == test_id:
            return payload
    return {"test": test_id, "report_present": False}


def audit_job_report(report_line: str, evidence: Mapping[str, object]) -> dict[str, object]:
    """Check the job's self-report *against* the controller's measurements.

    The report is untrusted data.  It is useful for exactly one thing — observing, from inside the
    job, that the credential marker never arrived — and that observation is only meaningful because
    the controller independently knows it planted the marker.
    """
    prefix = "WP125-DELEGATED-REPORT "
    index = report_line.find(prefix)
    if index < 0:
        raise reject("delegation_evidence", "the delegated job produced no machine-readable report")
    try:
        payload = json.loads(report_line[index + len(prefix) :].strip().splitlines()[0])
    except (ValueError, IndexError) as exc:
        raise reject("delegation_evidence", "the delegated report is not valid JSON") from exc

    if payload.get("credential_marker_present") is not False:
        raise reject("delegation_credential", "the credential marker reached the delegated job")
    if payload.get("credential_shaped_names"):
        raise reject(
            "delegation_credential",
            "%d credential-shaped names were observed inside the job"
            % len(payload["credential_shaped_names"]),
        )
    if payload.get("automatic_memory") != "1":
        raise reject("child_environment", "the delegated job did not observe the memory variable")
    if evidence.get("probe_return_code") != 0:
        raise reject("delegation_evidence", "the delegated credential probe did not exit zero")
    return {
        "observed_from_inside_job": True,
        "credential_marker_present": False,
        "credential_shaped_names": [],
        "automatic_memory": payload.get("automatic_memory"),
        "runner": payload.get("runner"),
        "test_selection": payload.get("test_selection"),
    }
