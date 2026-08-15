"""Narrow WP122 gateway: exact identity, two additive operations, durable readback.

The public transport surface is deliberately closed to two exact POST routes.  There is no raw
GitHub client, arbitrary endpoint, method override, command, credential, header, ref, workflow,
approval, mark-ready or merge primitive in this module.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Callable

from core import operations as core_operations

from .authority import AuthoritySnapshot, LANE_ID, OID40
from .errors import GatewayRejected, reject
from .fake_transport import FakeGatewayGitHub

MAX_REQUEST_BYTES = 64 * 1024
SCHEMA_VERSION = 1
POST_HEARTBEAT = "post_heartbeat"
POST_VERDICT = "post_verdict"
ROUTES = {
    "/capabilities/heartbeat": POST_HEARTBEAT,
    "/capabilities/verdict": POST_VERDICT,
}
SAFE_RECONCILE_KEY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{7,127}\Z")
SAFE_SESSION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:@/-]{0,127}\Z")
SAFE_FINDING = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")

_TOP_KEYS = frozenset(
    {
        "schema_version",
        "operation",
        "repository",
        "lane",
        "reviewed_sha",
        "packet_issue",
        "packet_revision",
        "generation",
        "attempt",
        "reconcile_key",
        "body",
    }
)
_HEARTBEAT_BODY_KEYS = frozenset({"lease_id", "provider", "session_id", "status"})
_VERDICT_BODY_KEYS = frozenset(
    {"verdict", "reviewer_provider", "reviewer_session_id", "review_axes", "finding_ids"}
)
_VERDICTS = frozenset({"approve", "changes_requested", "blocked"})
_REVIEWERS = frozenset({"claude", "codex", "human"})
_HEARTBEAT_STATUS = frozenset({"running", "reviewing"})
_EXPECTED_AXES = ("standards_security", "spec")


def _exact_object(value: object, keys: frozenset[str], category: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise reject(category, "request object shape is invalid")
    if frozenset(value) != keys:
        raise reject("extra_or_missing_key", "request has missing or extra keys")
    return value


def _positive_int(value: object, category: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise reject(category, "request identity integer is invalid")
    return value


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _strict_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON object key")
        value[key] = item
    return value


def _safe_string(value: object, category: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise reject(category, "request contains an invalid bounded identifier")
    return value


class CapabilityGateway:
    """Validate and execute only additive heartbeat and exact-head verdict creation."""

    def __init__(self, authority: AuthoritySnapshot, store: FakeGatewayGitHub):
        if type(authority) is not AuthoritySnapshot or not authority.is_sealed():
            raise reject("candidate_authority", "gateway requires a sealed external authority")
        if not isinstance(store, FakeGatewayGitHub):
            raise reject("backend_type", "gateway tests require the integrated RA-01 fake store")
        if store.repo != authority.repository:
            raise reject("backend_repository", "fake store repository disagrees with authority")
        self._authority = authority
        self._store = store

    @property
    def store(self) -> FakeGatewayGitHub:
        return self._store

    def handle_transport(self, method: str, path: str, raw_request: bytes) -> dict[str, object]:
        """Closed two-route adapter; every other method/path rejects before a store call."""

        if not isinstance(method, str) or method != "POST":
            raise reject("method_not_allowed", "only the two declared additive POST routes exist")
        if not isinstance(path, str):
            raise reject("endpoint_not_allowed", "POST endpoint is outside the closed route set")
        operation = ROUTES.get(path)
        if operation is None:
            raise reject("endpoint_not_allowed", "POST endpoint is outside the closed route set")
        return self._execute(operation, raw_request)

    def create_heartbeat(self, raw_request: bytes) -> dict[str, object]:
        return self._execute(POST_HEARTBEAT, raw_request)

    def create_verdict(self, raw_request: bytes) -> dict[str, object]:
        return self._execute(POST_VERDICT, raw_request)

    def _decode(self, raw_request: bytes) -> dict[str, object]:
        if not isinstance(raw_request, bytes):
            raise reject("malformed_payload", "request must be raw bytes")
        if len(raw_request) > MAX_REQUEST_BYTES:
            raise reject("oversized_payload", "request exceeds the fixed byte limit")
        try:
            text = raw_request.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise reject("non_utf8_payload", "request is not strict UTF-8") from exc
        try:
            value = json.loads(text, object_pairs_hook=_strict_object)
        except ValueError as exc:
            raise reject("malformed_payload", "request is not valid JSON") from exc
        if isinstance(value, dict) and "reconcile_key" not in value:
            raise reject("missing_reconcile_key", "request reconcile key is required")
        return _exact_object(value, _TOP_KEYS, "malformed_payload")

    def _validate(self, expected_operation: str, raw_request: bytes):
        request = self._decode(raw_request)
        if request["schema_version"] != SCHEMA_VERSION or isinstance(
            request["schema_version"], bool
        ):
            raise reject("schema_revision", "request schema revision is not authorized")
        if request["operation"] != expected_operation:
            raise reject("operation_not_allowed", "request operation does not match the closed route")
        if request["repository"] != self._authority.repository:
            raise reject("wrong_repository", "request repository does not match authority")
        lane_id = request["lane"]
        if not isinstance(lane_id, str) or LANE_ID.fullmatch(lane_id) is None:
            raise reject("unsafe_lane", "lane identifier is not a closed issue/PR lane")
        lane = self._authority.lanes.get(lane_id)
        if lane is None:
            raise reject("unknown_lane", "lane is not present in current authority")
        reviewed_sha = request["reviewed_sha"]
        if not isinstance(reviewed_sha, str) or OID40.fullmatch(reviewed_sha) is None:
            raise reject("reviewed_sha_absent", "reviewed SHA is not an exact object id")
        if reviewed_sha != lane.reviewed_sha:
            owners = [
                item.lane_id
                for item in self._authority.lanes.values()
                if item.reviewed_sha == reviewed_sha
            ]
            if owners:
                raise reject("cross_lane_sha", "reviewed SHA belongs to another authorized lane")
            raise reject("reviewed_sha_absent", "reviewed SHA is absent from the authorized lane")

        packet = self._authority.packet
        identity = (
            ("packet_issue", packet.issue, "stale_packet_issue"),
            ("packet_revision", packet.revision, "stale_revision"),
            ("generation", packet.generation, "stale_generation"),
            ("attempt", packet.attempt, "stale_attempt"),
        )
        for key, expected, category in identity:
            actual = _positive_int(request[key], category)
            if actual != expected:
                raise reject(category, "request identity is stale or fenced")
        reconcile_key = _safe_string(
            request["reconcile_key"], "missing_reconcile_key", SAFE_RECONCILE_KEY
        )

        if expected_operation == POST_HEARTBEAT:
            body = _exact_object(request["body"], _HEARTBEAT_BODY_KEYS, "malformed_payload")
            if not lane.lease_active:
                raise reject("fenced_lease", "heartbeat lease is fenced or expired")
            if body["lease_id"] != lane.lease_id:
                raise reject("stale_lease", "heartbeat lease id is not current")
            if body["provider"] != lane.heartbeat_provider:
                raise reject("wrong_provider", "heartbeat provider is not authorized for this lane")
            _safe_string(body["session_id"], "malformed_payload", SAFE_SESSION)
            if body["status"] not in _HEARTBEAT_STATUS:
                raise reject("malformed_payload", "heartbeat status is outside the closed enum")
        else:
            body = _exact_object(request["body"], _VERDICT_BODY_KEYS, "malformed_payload")
            if not lane.verdict_enabled:
                raise reject("fenced_verdict", "verdict authority is fenced")
            if body["verdict"] not in _VERDICTS or body["reviewer_provider"] not in _REVIEWERS:
                raise reject("malformed_payload", "verdict enum is outside the closed contract")
            if body["reviewer_provider"] != lane.reviewer_provider:
                raise reject("wrong_provider", "reviewer provider is not authorized for this lane")
            _safe_string(body["reviewer_session_id"], "malformed_payload", SAFE_SESSION)
            axes = body["review_axes"]
            if (
                not isinstance(axes, list)
                or len(axes) != len(_EXPECTED_AXES)
                or frozenset(axes) != frozenset(_EXPECTED_AXES)
            ):
                raise reject("malformed_payload", "both review axes are required exactly once")
            findings = body["finding_ids"]
            if not isinstance(findings, list) or len(findings) > 100:
                raise reject("malformed_payload", "finding_ids must be a bounded list")
            if len(set(findings)) != len(findings) or not all(
                isinstance(item, str) and SAFE_FINDING.fullmatch(item) is not None
                for item in findings
            ):
                raise reject("malformed_payload", "finding_ids contain invalid or duplicate values")
        return request, lane, reconcile_key

    def _object_id(self, request: dict[str, object]) -> int:
        seed = "\0".join(
            (
                str(request["repository"]),
                str(request["lane"]),
                str(request["reconcile_key"]),
            )
        ).encode("utf-8")
        return int(hashlib.sha256(seed).hexdigest()[:15], 16)

    def _duplicate_verdict(self, request: dict[str, object]) -> None:
        for record in self._store.snapshot_objects().values():
            if (
                record.get("gateway_created") is True
                and record.get("operation") == POST_VERDICT
                and record.get("lane") == request["lane"]
                and record.get("reviewed_sha") == request["reviewed_sha"]
                and record.get("reconcile_key") != request["reconcile_key"]
            ):
                raise reject("duplicate_verdict", "a verdict already exists for this exact lane head")

    def _execute(self, expected_operation: str, raw_request: bytes) -> dict[str, object]:
        request, lane, reconcile_key = self._validate(expected_operation, raw_request)
        if expected_operation == POST_VERDICT:
            self._duplicate_verdict(request)

        object_id = self._object_id(request)
        body_text = _canonical(request)
        expected_record = {
            "id": object_id,
            "issue_number": lane.number,
            "body": body_text,
            "author": self._authority.gateway_author,
            "repository": self._authority.repository,
            "lane": lane.lane_id,
            "reviewed_sha": lane.reviewed_sha,
            "operation": expected_operation,
            "reconcile_key": reconcile_key,
            "gateway_created": True,
        }

        existing_object = self._store.snapshot_objects().get(object_id)
        if (
            existing_object is not None
            and existing_object.get("reconcile_key") != reconcile_key
            and existing_object != expected_record
        ):
            raise reject("object_id_collision", "deterministic fake object id is already occupied")
        core_payload = {
            "schema_version": SCHEMA_VERSION,
            "object_id": object_id,
            "author": self._authority.gateway_author,
            "repository": self._authority.repository,
            "lane": lane.lane_id,
            "reviewed_sha": lane.reviewed_sha,
            "body": body_text,
            "body_sha256": hashlib.sha256(body_text.encode("utf-8")).hexdigest(),
        }
        try:
            if expected_operation == POST_HEARTBEAT:
                outcome = self._store.call(
                    POST_HEARTBEAT,
                    {
                        "repo": self._authority.repository,
                        "issue_number": lane.number,
                        "reconcile_key": reconcile_key,
                        "payload": core_payload,
                    },
                )
            else:
                outcome = self._store.call(
                    POST_VERDICT,
                    {
                        "repo": self._authority.repository,
                        "issue_number": lane.number,
                        "reconcile_key": reconcile_key,
                        "reviewed_sha": lane.reviewed_sha,
                        "verdict": request["body"]["verdict"],
                        "payload": core_payload,
                    },
                )
        except core_operations.CredentialSurfaceError as exc:
            raise reject(
                "credential_surface",
                "integrated fake store rejected credential-like durable content",
            ) from exc
        except Exception as exc:
            status = getattr(exc, "status", None)
            category = "reconcile_conflict" if status == 409 else "backend_rejected"
            raise reject(category, "integrated fake store rejected the additive operation") from exc

        created = outcome.get("created") is True
        expected_durable_record = {
            "op": expected_operation,
            "issue_number": lane.number,
            "payload": core_payload,
        }
        if expected_operation == POST_VERDICT:
            expected_durable_record.update(
                {"reviewed_sha": lane.reviewed_sha, "verdict": request["body"]["verdict"]}
            )
        durable_record = outcome.get("record")
        try:
            readback = self._store.call(
                "read_comment",
                {"repo": self._authority.repository, "comment_id": object_id},
            )
        except Exception as exc:
            raise reject("readback_failed", "created object could not be read back") from exc
        if durable_record != expected_durable_record or readback != expected_record:
            raise reject("readback_mismatch", "durable readback did not match the exact created object")
        return {
            "schema_version": SCHEMA_VERSION,
            "created": created,
            "object_id": object_id,
            "author": readback["author"],
            "repository": readback["repository"],
            "lane": readback["lane"],
            "reviewed_sha": readback["reviewed_sha"],
            "operation": expected_operation,
            "reconcile_key": reconcile_key,
            "body_sha256": hashlib.sha256(readback["body"].encode("utf-8")).hexdigest(),
        }
