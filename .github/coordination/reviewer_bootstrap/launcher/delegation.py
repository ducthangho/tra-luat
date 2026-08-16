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
import platform
from collections.abc import Mapping, Sequence

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


@dataclasses.dataclass(frozen=True)
class DelegatedJob:
    """A fully-resolved delegated job.  Frozen for the same reason as the launch plan: it is evidence."""

    operation: str
    candidate_head: str
    candidate_tree: str
    test_selection: tuple[str, ...]
    command: tuple[str, ...]
    read_only_root: str

    def as_dict(self) -> dict[str, object]:
        return {
            "operation": self.operation,
            "candidate_head": self.candidate_head,
            "candidate_tree": self.candidate_tree,
            "test_selection": list(self.test_selection),
            "command": list(self.command),
            "read_only_root": self.read_only_root,
        }


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
) -> DelegatedJob:
    """Build the job, or refuse.

    ``eligible`` is the preflight verdict, passed in rather than recomputed.  Recomputing it here
    would give this module a second opinion about whether delegation is allowed, and two opinions is
    one more than a fail-closed boundary can afford.
    """
    if not eligible:
        raise reject("delegation_scope", "delegation was attempted without preflight eligibility")
    name = validate_operation(operation)
    if not test_selection:
        raise reject("delegation_evidence", "the delegated job declares no test selection")
    selection = tuple(str(item) for item in test_selection)
    for item in selection:
        if not item or item.startswith("-") or ".." in item:
            raise reject("delegation_scope", "test selection entry %r is not a declared test" % (item,))
    command = (python_executable(), "-c", _PROBE_SOURCE, *selection)
    return DelegatedJob(
        operation=name,
        candidate_head=candidate_head,
        candidate_tree=candidate_tree,
        test_selection=selection,
        command=command,
        read_only_root=read_only_root,
    )


# The job body.  It reports the environment *names* it received and the marker's presence, then runs
# the declared selection.  Kept as a literal so the delegated side cannot be swapped for something
# the controller did not author — there is no file on disk for anyone to edit between build and run.
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
    "test_selection": sys.argv[1:],
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
    """Run the delegated job under the controller's watchdog and return measured evidence."""
    parent = dict(parent_environment)
    parent[MARKER_NAME] = MARKER_VALUE  # planted so its absence downstream is a measurement
    environment = build_child_environment(parent, candidate_root=candidate_root)

    leaked = sorted(name for name in environment if credential_shaped(name))
    if leaked:
        raise reject("delegation_credential", "%d credential-shaped names reached the job" % len(leaked))

    outcome = run_supervised(
        job.command,
        environment=environment,
        working_directory=working_directory,
        deadline=deadline,
        label="delegated-run-test",
    )

    evidence = {
        "job": job.as_dict(),
        "return_code": outcome.return_code,
        "status": outcome.status,
        "fenced": outcome.fenced,
        "timeout_source": "controller",
        "cleanup": outcome.cleanup,
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
    evidence["job_report"] = audit_job_report(outcome.stdout_text, evidence)
    evidence["runner"] = evidence["job_report"].get("runner")
    evidence["evidence_sha256"] = hashlib.sha256(
        json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return evidence


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
    if evidence.get("return_code") != 0:
        raise reject("delegation_evidence", "the delegated job did not exit zero")
    return {
        "observed_from_inside_job": True,
        "credential_marker_present": False,
        "credential_shaped_names": [],
        "automatic_memory": payload.get("automatic_memory"),
        "runner": payload.get("runner"),
        "test_selection": payload.get("test_selection"),
    }
