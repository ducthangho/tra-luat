"""Executable WP122 positive and named fail-closed capability matrix.

Every registered case is scheduled before execution. The final JSON separates scheduled,
executed, passed, failed, skipped and not-run; this suite never treats a smaller denominator as
green. Security checks use explicit branches so ``python -O`` executes the same teeth.
"""

from __future__ import annotations

import ast
import contextlib
import copy
import json
import os
import pathlib
import stat
import sys
import tempfile
from collections.abc import Callable, Iterator
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
CANDIDATE_ROOT = HERE.parents[3]
BOOTSTRAP_ROOT = HERE.parent
if str(BOOTSTRAP_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOTSTRAP_ROOT))

from core.guards import EnvGuard, NetworkGuard  # noqa: E402
from gateway import authority as authority_module  # noqa: E402
from gateway.authority import load_authority  # noqa: E402
from gateway.errors import GatewayRejected  # noqa: E402
from gateway.fake_transport import FakeGatewayGitHub  # noqa: E402
from gateway.gateway import MAX_REQUEST_BYTES, CapabilityGateway  # noqa: E402

REPOSITORY = "ducthangho/tra-luat"
ISSUE_HEAD = "1" * 40
PR_HEAD = "2" * 40
PACKET = {"issue": 122, "revision": 1, "generation": 1, "attempt": 1}
LEASE_ID = "wp122-r1-g1-lease"
GATEWAY_AUTHOR = "github-app/reviewer-bootstrap"


def ensure(condition: object, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def authority_document(*, lease_active: bool = True, verdict_enabled: bool = True):
    return {
        "schema_version": 1,
        "repository": REPOSITORY,
        "packet": dict(PACKET),
        "gateway_author": GATEWAY_AUTHOR,
        "lanes": {
            "issue:122": {
                "kind": "issue",
                "number": 122,
                "reviewed_sha": ISSUE_HEAD,
                "lease_id": LEASE_ID,
                "lease_active": lease_active,
                "verdict_enabled": verdict_enabled,
                "heartbeat_provider": "codex",
                "reviewer_provider": "claude",
            },
            "pr:124": {
                "kind": "pr",
                "number": 124,
                "reviewed_sha": PR_HEAD,
                "lease_id": "wp122-review-lane",
                "lease_active": True,
                "verdict_enabled": verdict_enabled,
                "heartbeat_provider": "codex",
                "reviewer_provider": "claude",
            },
        },
    }


def seal_json(path: pathlib.Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    path.chmod(stat.S_IREAD)


@contextlib.contextmanager
def gateway_fixture(
    *, lease_active: bool = True, verdict_enabled: bool = True
) -> Iterator[CapabilityGateway]:
    temp = tempfile.TemporaryDirectory(prefix="wp122-gateway-")
    root = pathlib.Path(temp.name).resolve()
    authority_path = root / "authority.json"
    seal_json(
        authority_path,
        authority_document(lease_active=lease_active, verdict_enabled=verdict_enabled),
    )
    try:
        authority = load_authority(root, "authority.json", candidate_root=CANDIDATE_ROOT)
        store = FakeGatewayGitHub(root / "ledger.json", repo=REPOSITORY)
        store.add_comment(900001, 7, "unrelated-object-byte-sentinel")
        yield CapabilityGateway(authority, store)
    finally:
        try:
            authority_path.chmod(stat.S_IREAD | stat.S_IWRITE)
        except OSError:
            pass
        temp.cleanup()


def request(operation: str, **updates: object) -> bytes:
    if operation == "post_heartbeat":
        value = {
            "schema_version": 1,
            "operation": operation,
            "repository": REPOSITORY,
            "lane": "issue:122",
            "reviewed_sha": ISSUE_HEAD,
            "packet_issue": 122,
            "packet_revision": 1,
            "generation": 1,
            "attempt": 1,
            "reconcile_key": "wp122-heartbeat-0001",
            "body": {
                "lease_id": LEASE_ID,
                "provider": "codex",
                "session_id": "executor-session-1",
                "status": "running",
            },
        }
    else:
        value = {
            "schema_version": 1,
            "operation": operation,
            "repository": REPOSITORY,
            "lane": "pr:124",
            "reviewed_sha": PR_HEAD,
            "packet_issue": 122,
            "packet_revision": 1,
            "generation": 1,
            "attempt": 1,
            "reconcile_key": "wp122-verdict-0001",
            "body": {
                "verdict": "approve",
                "reviewer_provider": "claude",
                "reviewer_session_id": "reviewer-session-1",
                "review_axes": ["standards_security", "spec"],
                "finding_ids": [],
            },
        }
    for key, replacement in updates.items():
        value[key] = replacement
    return json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")


def decoded(raw: bytes) -> dict[str, object]:
    value = json.loads(raw.decode("utf-8"))
    ensure(isinstance(value, dict), "fixture request is not an object")
    return value


def encoded(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")


def rejection(
    case_id: str,
    gateway: CapabilityGateway,
    action: Callable[[], object],
    expected_category: str,
) -> dict[str, object]:
    store = gateway.store
    before_writes = store.total_durable_write_count()
    before_gateway_objects = store.gateway_write_count()
    before_objects = store.snapshot_objects()
    try:
        action()
    except GatewayRejected as exc:
        actual = exc.category
        message = str(exc)
    else:
        raise AssertionError("%s accepted an operation expected to reject" % case_id)
    ensure(
        actual == expected_category,
        "%s category=%s expected=%s" % (case_id, actual, expected_category),
    )
    ensure(
        store.total_durable_write_count() == before_writes,
        "%s changed the integrated ledger before rejection" % case_id,
    )
    ensure(
        store.gateway_write_count() == before_gateway_objects,
        "%s created an additive object before rejection" % case_id,
    )
    ensure(store.snapshot_objects() == before_objects, "%s changed fake GitHub objects" % case_id)
    return {
        "expected_rejection": expected_category,
        "actual_rejection": actual,
        "write_count_before": before_writes,
        "write_count_after": store.total_durable_write_count(),
        "gateway_objects_before": before_gateway_objects,
        "gateway_objects_after": store.gateway_write_count(),
        "safe_message": message,
    }


CASES: list[tuple[str, Callable[[], dict[str, object]]]] = []


def case(case_id: str):
    def register(function: Callable[[], dict[str, object]]):
        CASES.append((case_id, function))
        return function

    return register


@case("WP122-POS-001-heartbeat-additive-readback")
def positive_heartbeat():
    with gateway_fixture() as gateway:
        unrelated = copy.deepcopy(gateway.store.comments[900001])
        receipt = gateway.create_heartbeat(request("post_heartbeat"))
        ensure(receipt["created"] is True, "first heartbeat was not created")
        ensure(gateway.store.gateway_write_count() == 1, "heartbeat object count is not one")
        ensure(gateway.store.total_durable_write_count() == 1, "heartbeat ledger count is not one")
        ensure(receipt["author"] == GATEWAY_AUTHOR, "readback author mismatch")
        ensure(receipt["repository"] == REPOSITORY, "readback repository mismatch")
        ensure(receipt["lane"] == "issue:122", "readback lane mismatch")
        ensure(receipt["reviewed_sha"] == ISSUE_HEAD, "readback SHA mismatch")
        ensure(gateway.store.comments[900001] == unrelated, "unrelated object changed")
        return {"receipt": receipt, "object_count": 1, "unrelated_byte_identical": True}


@case("WP122-POS-002-heartbeat-identical-retry")
def positive_heartbeat_retry():
    with gateway_fixture() as gateway:
        first = gateway.create_heartbeat(request("post_heartbeat"))
        before = gateway.store.gateway_write_count()
        second = gateway.create_heartbeat(request("post_heartbeat"))
        ensure(first["object_id"] == second["object_id"], "retry changed object id")
        ensure(first["body_sha256"] == second["body_sha256"], "retry changed body digest")
        ensure(second["created"] is False, "retry reported a duplicate creation")
        ensure(gateway.store.gateway_write_count() == before, "retry created another object")
        ensure(gateway.store.total_durable_write_count() == 1, "retry created another ledger row")
        return {"same_receipt": True, "additional_objects": 0, "durable_rows": 1}


@case("WP122-POS-003-verdict-exact-head-readback")
def positive_verdict():
    with gateway_fixture() as gateway:
        receipt = gateway.create_verdict(request("post_verdict"))
        ensure(receipt["created"] is True, "first verdict was not created")
        ensure(
            receipt["lane"] == "pr:124" and receipt["reviewed_sha"] == PR_HEAD,
            "verdict pin mismatch",
        )
        ensure(gateway.store.gateway_write_count() == 1, "verdict count is not one")
        return {"receipt": receipt, "object_count": gateway.store.gateway_write_count()}


@case("WP122-POS-004-closed-fake-store-operation-surface")
def positive_closed_store_surface():
    with gateway_fixture() as gateway:
        gateway.create_heartbeat(request("post_heartbeat"))
        verdict = decoded(request("post_verdict"))
        verdict["reconcile_key"] = "wp122-verdict-closed-surface"
        gateway.create_verdict(encoded(verdict))
        allowed = {"post_heartbeat", "post_verdict", "read_comment"}
        unexpected = sorted(set(gateway.store.calls) - allowed)
        ensure(not unexpected, "fake store saw operations outside the closed allowlist")
        ensure(set(gateway.store.calls) == allowed, "positive run did not exercise all allowed fake ops")
        return {"calls": list(gateway.store.calls), "unexpected": unexpected}


@case("WP122-POS-005-credential-and-network-tripwires")
def positive_credential_free():
    with gateway_fixture() as gateway:
        with EnvGuard(
            inject={
                "GH_TOKEN": "FAKE-WP122-GH-MARKER",
                "GITHUB_TOKEN": "FAKE-WP122-GITHUB-MARKER",
                "AWS_SECRET_ACCESS_KEY": "FAKE-WP122-AWS-MARKER",
            },
            guard_subprocess=True,
        ) as environment, NetworkGuard() as network:
            gateway.create_heartbeat(request("post_heartbeat"))
            reads = environment.sensitive_reads()
            attempts = list(network.attempts)
        ensure(reads == [], "gateway read a protected environment value")
        ensure(attempts == [], "gateway attempted a network operation")
        return {"sensitive_reads": reads, "network_attempts": attempts}


@case("WP122-POS-006-optimized-boundaries-use-no-assert")
def positive_explicit_boundaries():
    files = [HERE / "authority.py", HERE / "gateway.py", HERE / "fake_transport.py"]
    assert_nodes = []
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assert_nodes.extend(
            (path.name, node.lineno) for node in ast.walk(tree) if isinstance(node, ast.Assert)
        )
    ensure(assert_nodes == [], "security modules contain optimization-removable assertions")
    return {"files": [path.name for path in files], "assert_nodes": assert_nodes}


def request_negative(
    case_id: str, expected: str, mutate: Callable[[dict[str, object]], None]
):
    with gateway_fixture() as gateway:
        value = decoded(request("post_heartbeat"))
        mutate(value)
        return rejection(case_id, gateway, lambda: gateway.create_heartbeat(encoded(value)), expected)


@case("WP122-NEG-001-wrong-repository")
def negative_wrong_repository():
    return request_negative(
        "WP122-NEG-001-wrong-repository",
        "wrong_repository",
        lambda value: value.__setitem__("repository", "attacker/other"),
    )


@case("WP122-NEG-002-unknown-lane")
def negative_unknown_lane():
    return request_negative(
        "WP122-NEG-002-unknown-lane",
        "unknown_lane",
        lambda value: value.__setitem__("lane", "issue:999"),
    )


@case("WP122-NEG-003-reviewed-sha-absent")
def negative_absent_sha():
    return request_negative(
        "WP122-NEG-003-reviewed-sha-absent",
        "reviewed_sha_absent",
        lambda value: value.__setitem__("reviewed_sha", "3" * 40),
    )


@case("WP122-NEG-004-cross-lane-sha")
def negative_cross_lane_sha():
    return request_negative(
        "WP122-NEG-004-cross-lane-sha",
        "cross_lane_sha",
        lambda value: value.__setitem__("reviewed_sha", PR_HEAD),
    )


@case("WP122-NEG-005-stale-generation")
def negative_generation():
    return request_negative(
        "WP122-NEG-005-stale-generation",
        "stale_generation",
        lambda value: value.__setitem__("generation", 2),
    )


@case("WP122-NEG-006-stale-revision")
def negative_revision():
    return request_negative(
        "WP122-NEG-006-stale-revision",
        "stale_revision",
        lambda value: value.__setitem__("packet_revision", 2),
    )


@case("WP122-NEG-007-stale-attempt")
def negative_attempt():
    return request_negative(
        "WP122-NEG-007-stale-attempt",
        "stale_attempt",
        lambda value: value.__setitem__("attempt", 2),
    )


@case("WP122-NEG-008-stale-packet-issue")
def negative_packet():
    return request_negative(
        "WP122-NEG-008-stale-packet-issue",
        "stale_packet_issue",
        lambda value: value.__setitem__("packet_issue", 999),
    )


@case("WP122-NEG-009-fenced-expired-heartbeat")
def negative_fenced_heartbeat():
    with gateway_fixture(lease_active=False) as gateway:
        return rejection(
            "WP122-NEG-009-fenced-expired-heartbeat",
            gateway,
            lambda: gateway.create_heartbeat(request("post_heartbeat")),
            "fenced_lease",
        )


@case("WP122-NEG-010-stale-lease-id")
def negative_stale_lease():
    with gateway_fixture() as gateway:
        value = decoded(request("post_heartbeat"))
        value["body"]["lease_id"] = "old-fenced-lease"
        return rejection(
            "WP122-NEG-010-stale-lease-id",
            gateway,
            lambda: gateway.create_heartbeat(encoded(value)),
            "stale_lease",
        )


@case("WP122-NEG-011-duplicate-verdict-current-head")
def negative_duplicate_verdict():
    with gateway_fixture() as gateway:
        gateway.create_verdict(request("post_verdict"))
        value = decoded(request("post_verdict"))
        value["reconcile_key"] = "wp122-verdict-duplicate-0002"
        return rejection(
            "WP122-NEG-011-duplicate-verdict-current-head",
            gateway,
            lambda: gateway.create_verdict(encoded(value)),
            "duplicate_verdict",
        )


@case("WP122-NEG-012-missing-reconcile-key")
def negative_missing_key():
    with gateway_fixture() as gateway:
        value = decoded(request("post_heartbeat"))
        del value["reconcile_key"]
        return rejection(
            "WP122-NEG-012-missing-reconcile-key",
            gateway,
            lambda: gateway.create_heartbeat(encoded(value)),
            "missing_reconcile_key",
        )


@case("WP122-NEG-013-reconcile-key-conflicting-payload")
def negative_reconcile_conflict():
    with gateway_fixture() as gateway:
        gateway.create_heartbeat(request("post_heartbeat"))
        value = decoded(request("post_heartbeat"))
        value["body"]["status"] = "reviewing"
        return rejection(
            "WP122-NEG-013-reconcile-key-conflicting-payload",
            gateway,
            lambda: gateway.create_heartbeat(encoded(value)),
            "reconcile_conflict",
        )


def transport_negative(case_id: str, method: str, path: str, expected: str):
    with gateway_fixture() as gateway:
        return rejection(
            case_id,
            gateway,
            lambda: gateway.handle_transport(method, path, request("post_heartbeat")),
            expected,
        )


for suffix, forbidden_method in (("014", "PATCH"), ("015", "PUT"), ("016", "DELETE")):
    current_id = "WP122-NEG-%s-%s-method" % (suffix, forbidden_method.lower())

    @case(current_id)
    def _method_case(method=forbidden_method, case_id=current_id):
        return transport_negative(case_id, method, "/capabilities/heartbeat", "method_not_allowed")


for suffix, slug, forbidden_path in (
    ("017", "arbitrary-post", "/api/custom"),
    ("018", "issue-metadata", "/issues/122/metadata"),
    ("019", "label", "/issues/122/labels"),
    ("020", "state", "/issues/122/state"),
    ("021", "approval", "/pulls/124/reviews/approve"),
    ("022", "mark-ready", "/pulls/124/ready"),
    ("023", "merge", "/pulls/124/merge"),
    ("024", "ref", "/git/refs/heads/x"),
    ("025", "workflow", "/actions/workflows/x/dispatches"),
):
    current_id = "WP122-NEG-%s-%s-operation" % (suffix, slug)

    @case(current_id)
    def _post_case(path=forbidden_path, case_id=current_id):
        return transport_negative(case_id, "POST", path, "endpoint_not_allowed")


@case("WP122-NEG-026-malformed-json")
def negative_malformed():
    with gateway_fixture() as gateway:
        return rejection(
            "WP122-NEG-026-malformed-json",
            gateway,
            lambda: gateway.create_heartbeat(b"{not-json"),
            "malformed_payload",
        )


@case("WP122-NEG-027-extra-key")
def negative_extra_key():
    with gateway_fixture() as gateway:
        value = decoded(request("post_heartbeat"))
        value["token"] = "ghp_0123456789abcdefghijkl"
        marker = value["token"]
        result = rejection(
            "WP122-NEG-027-extra-key",
            gateway,
            lambda: gateway.create_heartbeat(encoded(value)),
            "extra_or_missing_key",
        )
        ensure(marker not in result["safe_message"], "credential-like extra value leaked")
        return result


@case("WP122-NEG-028-oversized-payload")
def negative_oversized():
    with gateway_fixture() as gateway:
        raw = b"{" + b"x" * (MAX_REQUEST_BYTES + 1) + b"}"
        return rejection(
            "WP122-NEG-028-oversized-payload",
            gateway,
            lambda: gateway.create_heartbeat(raw),
            "oversized_payload",
        )


@case("WP122-NEG-029-non-utf8-payload")
def negative_non_utf8():
    with gateway_fixture() as gateway:
        return rejection(
            "WP122-NEG-029-non-utf8-payload",
            gateway,
            lambda: gateway.create_heartbeat(b"{\"x\":\"\xff\"}"),
            "non_utf8_payload",
        )


@case("WP122-NEG-030-unsafe-lane-path")
def negative_lane_path():
    return request_negative(
        "WP122-NEG-030-unsafe-lane-path",
        "unsafe_lane",
        lambda value: value.__setitem__("lane", "../../refs/heads/master"),
    )


@case("WP122-NEG-031-candidate-controlled-authority-field")
def negative_candidate_authority_field():
    with gateway_fixture() as gateway:
        value = decoded(request("post_heartbeat"))
        value["authority_path"] = "candidate/authority.json"
        return rejection(
            "WP122-NEG-031-candidate-controlled-authority-field",
            gateway,
            lambda: gateway.create_heartbeat(encoded(value)),
            "extra_or_missing_key",
        )


@case("WP122-NEG-032-authority-path-traversal")
def negative_authority_traversal():
    with tempfile.TemporaryDirectory(prefix="wp122-authority-path-") as tmp:
        root = pathlib.Path(tmp).resolve()
        try:
            load_authority(root, "../authority.json", candidate_root=CANDIDATE_ROOT)
        except GatewayRejected as exc:
            ensure(exc.category == "authority_path", "authority traversal category mismatch")
            return {"expected_rejection": "authority_path", "actual_rejection": exc.category}
        raise AssertionError("authority traversal was accepted")


@case("WP122-NEG-033-authority-inside-candidate")
def negative_authority_inside_candidate():
    temp = tempfile.TemporaryDirectory(prefix="wp122-candidate-authority-")
    root = pathlib.Path(temp.name).resolve()
    path = root / "authority.json"
    seal_json(path, authority_document())
    try:
        try:
            load_authority(root, "authority.json", candidate_root=root)
        except GatewayRejected as exc:
            ensure(exc.category == "candidate_authority", "inside-candidate category mismatch")
            return {"expected_rejection": "candidate_authority", "actual_rejection": exc.category}
        raise AssertionError("candidate-contained authority was accepted")
    finally:
        path.chmod(stat.S_IREAD | stat.S_IWRITE)
        temp.cleanup()


@case("WP122-NEG-034-authority-hardlink")
def negative_authority_hardlink():
    temp = tempfile.TemporaryDirectory(prefix="wp122-authority-hardlink-")
    root = pathlib.Path(temp.name).resolve()
    source = root / "source.json"
    linked = root / "authority.json"
    source.write_text(json.dumps(authority_document()), encoding="utf-8", newline="\n")
    os.link(source, linked)
    source.chmod(stat.S_IREAD)
    try:
        try:
            load_authority(root, "authority.json", candidate_root=CANDIDATE_ROOT)
        except GatewayRejected as exc:
            ensure(exc.category == "authority_hardlink", "hardlink category mismatch")
            return {
                "expected_rejection": "authority_hardlink",
                "actual_rejection": exc.category,
                "link_count": linked.stat().st_nlink,
            }
        raise AssertionError("hardlinked authority was accepted")
    finally:
        source.chmod(stat.S_IREAD | stat.S_IWRITE)
        linked.chmod(stat.S_IREAD | stat.S_IWRITE)
        temp.cleanup()


@case("WP122-NEG-035-authority-symlink")
def negative_authority_symlink():
    temp = tempfile.TemporaryDirectory(prefix="wp122-authority-symlink-")
    root = pathlib.Path(temp.name).resolve()
    source = root / "source.json"
    linked = root / "authority.json"
    source.write_text(json.dumps(authority_document()), encoding="utf-8", newline="\n")
    source.chmod(stat.S_IREAD)
    try:
        fixture_kind = "filesystem_symlink"
        try:
            os.symlink(source, linked)
        except OSError:
            # Windows without Developer Mode cannot construct a symlink as an unprivileged
            # process. Exercise the exact lstat branch with a symlink-mode result instead of
            # skipping or shrinking the denominator; POSIX and capable Windows use the real FS.
            fixture_kind = "portable_symlink_lstat"
            symlink_stat = os.stat_result((stat.S_IFLNK | 0o777, 0, 0, 1, 0, 0, 0, 0, 0, 0))
            with mock.patch.object(pathlib.Path, "lstat", return_value=symlink_stat):
                try:
                    authority_module._safe_read_authority(linked)
                except GatewayRejected as exc:
                    ensure(exc.category == "authority_symlink", "symlink category mismatch")
                    return {
                        "expected_rejection": "authority_symlink",
                        "actual_rejection": exc.category,
                        "fixture": fixture_kind,
                    }
                raise AssertionError("synthetic symlink lstat was accepted")
        try:
            load_authority(root, "authority.json", candidate_root=CANDIDATE_ROOT)
        except GatewayRejected as exc:
            ensure(exc.category == "authority_symlink", "symlink category mismatch")
            return {
                "expected_rejection": "authority_symlink",
                "actual_rejection": exc.category,
                "fixture": fixture_kind,
            }
        raise AssertionError("symlinked authority was accepted")
    finally:
        source.chmod(stat.S_IREAD | stat.S_IWRITE)
        temp.cleanup()


@case("WP122-NEG-036-fenced-verdict-authority")
def negative_fenced_verdict():
    with gateway_fixture(verdict_enabled=False) as gateway:
        return rejection(
            "WP122-NEG-036-fenced-verdict-authority",
            gateway,
            lambda: gateway.create_verdict(request("post_verdict")),
            "fenced_verdict",
        )


@case("WP122-NEG-037-verdict-body-extra-key")
def negative_verdict_extra():
    with gateway_fixture() as gateway:
        value = decoded(request("post_verdict"))
        value["body"]["approval"] = True
        return rejection(
            "WP122-NEG-037-verdict-body-extra-key",
            gateway,
            lambda: gateway.create_verdict(encoded(value)),
            "extra_or_missing_key",
        )


@case("WP122-NEG-038-route-operation-mismatch")
def negative_route_operation_mismatch():
    with gateway_fixture() as gateway:
        return rejection(
            "WP122-NEG-038-route-operation-mismatch",
            gateway,
            lambda: gateway.handle_transport(
                "POST", "/capabilities/heartbeat", request("post_verdict")
            ),
            "operation_not_allowed",
        )


@case("WP122-NEG-039-wrong-heartbeat-provider")
def negative_heartbeat_provider():
    with gateway_fixture() as gateway:
        value = decoded(request("post_heartbeat"))
        value["body"]["provider"] = "claude"
        return rejection(
            "WP122-NEG-039-wrong-heartbeat-provider",
            gateway,
            lambda: gateway.create_heartbeat(encoded(value)),
            "wrong_provider",
        )


@case("WP122-NEG-040-wrong-reviewer-provider")
def negative_reviewer_provider():
    with gateway_fixture() as gateway:
        value = decoded(request("post_verdict"))
        value["body"]["reviewer_provider"] = "codex"
        return rejection(
            "WP122-NEG-040-wrong-reviewer-provider",
            gateway,
            lambda: gateway.create_verdict(encoded(value)),
            "wrong_provider",
        )


@case("WP122-NEG-041-duplicate-json-key")
def negative_duplicate_json_key():
    with gateway_fixture() as gateway:
        text = request("post_heartbeat").decode("utf-8")
        needle = '"repository": "ducthangho/tra-luat"'
        ensure(needle in text, "duplicate-key fixture anchor missing")
        text = text.replace(
            needle,
            needle + ', "repository": "attacker/other"',
            1,
        )
        return rejection(
            "WP122-NEG-041-duplicate-json-key",
            gateway,
            lambda: gateway.create_heartbeat(text.encode("utf-8")),
            "malformed_payload",
        )


@case("WP122-POS-007-sealed-authority-immutable")
def positive_authority_immutable():
    temp = tempfile.TemporaryDirectory(prefix="wp122-authority-immutable-")
    root = pathlib.Path(temp.name).resolve()
    path = root / "authority.json"
    seal_json(path, authority_document())
    try:
        authority = load_authority(root, "authority.json", candidate_root=CANDIDATE_ROOT)
        mutation_error = None
        try:
            authority.repository = "attacker/other"
        except (AttributeError, TypeError) as exc:
            mutation_error = type(exc).__name__
        ensure(mutation_error is not None, "sealed authority attributes are mutable")
        try:
            authority.lanes["issue:999"] = authority.lanes["issue:122"]
        except TypeError as exc:
            mapping_error = type(exc).__name__
        else:
            raise AssertionError("sealed authority lane mapping is mutable")
        return {"attribute_mutation": mutation_error, "mapping_mutation": mapping_error}
    finally:
        path.chmod(stat.S_IREAD | stat.S_IWRITE)
        temp.cleanup()


def main() -> int:
    records = []
    failed = 0
    executed = 0
    for case_id, function in CASES:
        executed += 1
        try:
            evidence = function()
        except Exception as exc:  # noqa: BLE001 - every failure becomes a named red record
            failed += 1
            records.append(
                {
                    "case_id": case_id,
                    "status": "failed",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
        else:
            records.append({"case_id": case_id, "status": "passed", "evidence": evidence})
    report = {
        "schema_version": 1,
        "suite": "wp122_gateway_capability_matrix",
        "optimized": not __debug__,
        "scheduled": len(CASES),
        "executed": executed,
        "passed": executed - failed,
        "failed": failed,
        "skipped": 0,
        "not_run": len(CASES) - executed,
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
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
