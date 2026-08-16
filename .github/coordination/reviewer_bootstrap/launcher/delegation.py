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


def safe_directory_args(*paths: object) -> tuple[str, ...]:
    """Per-command ``safe.directory`` entries for exactly the paths this command will touch.

    WP125-GATE-001-R3.  A linked checkout keeps its ``.git`` as a file pointing at a gitdir that git
    treats as a separate ownership domain, and under a Unicode path the two are easy to get wrong
    together.  The alternative fixes are both unacceptable here: ``git config --global
    safe.directory`` mutates the user's configuration, and writing into the repository's own config
    mutates the thing under review.  ``-c`` supplies the trust for one invocation and leaves nothing
    behind — the trust boundary is exactly as wide as the command, and no wider.

    Both the worktree and its linked gitdir are declared, because the checkout is trusted only if git
    can open both.
    """
    args: list[str] = []
    for raw in paths:
        if not raw:
            continue
        path = pathlib.Path(str(raw))
        args.extend(("-c", "safe.directory=%s" % path.as_posix()))
        git_marker = path / ".git"
        try:
            if git_marker.is_file():
                pointer = git_marker.read_text(encoding="utf-8").strip()
                if pointer.startswith("gitdir:"):
                    linked = pathlib.Path(pointer.split(":", 1)[1].strip())
                    args.extend(("-c", "safe.directory=%s" % linked.as_posix()))
            elif git_marker.is_dir():
                args.extend(("-c", "safe.directory=%s" % git_marker.as_posix()))
        except OSError:
            continue
    return tuple(args)


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
    trust = safe_directory_args(path)
    head = (
        git(path, *trust, "rev-parse", "HEAD", error=_root_error, binary=True).decode("utf-8").strip()
    )
    tree = (
        git(path, *trust, "rev-parse", "HEAD^{tree}", error=_root_error, binary=True)
        .decode("utf-8")
        .strip()
    )
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
