"""Trusted protocol-derived answer key.

This module is part of the pinned trusted source.  It never reads expected
results, validators, snapshots or labels from the candidate target.
"""

from __future__ import annotations

import hashlib
import re
from types import MappingProxyType
from typing import Mapping

DIALECT = "https://json-schema.org/draft/2020-12/schema"
EXPECTED_FILES = (
    "handoff.schema.json",
    "review.schema.json",
    "land.schema.json",
    "state.schema.json",
    "command.schema.json",
)

_PIN_ITEMS = (
    ("protocol_commit_sha", "ea92ec960a23026ab345d8e9b97b36479a66d240"),
    ("protocol_path", "docs/PROTOCOL_DA_PHIEN.md"),
    ("protocol_file_git_oid", "541e911d272b4b75afb072f25008e8149f97084c"),
    ("protocol_file_sha256", "57f6dde9ce348414b32dcd33a71dae52102a5726130149579926906e15d7916d"),
    ("mission_issue", 76),
    ("mission_revision", 3),
    ("mission_plan_hash", "346f9a6d89cf327b67d7ce7b7ea1e7b769f59a3bd90518afa9da5cec280ebde0"),
    ("packet_issue", 86),
    ("packet_revision", 4),
    ("packet_generation", 4),
    ("packet_spec_hash", "3a15ea7229d790e40da4e8973348b0727224abd716463605923056d4289c1913"),
)
PINS = MappingProxyType(dict(_PIN_ITEMS))


def verify_pin_readback(readback: Mapping[str, object], protocol_source: bytes) -> dict[str, str]:
    """Bind runtime authority and exact protocol bytes before any evaluation.

    ``readback`` is supplied by the trusted dispatcher rather than inferred
    from candidate data.  Comparing it to a private immutable tuple catches a
    monkeypatched/corrupted public pin mapping as well as stale dispatcher
    facts.  The Git blob oid and SHA-256 independently bind the supplied source
    bytes; a path or commit label alone is not treated as evidence.
    """
    installed = dict(PINS)
    expected = dict(_PIN_ITEMS)
    if installed != expected:
        raise ValueError("installed answer-key pins were mutated")
    if dict(readback) != expected:
        missing = sorted(set(expected) - set(readback))
        extra = sorted(set(readback) - set(expected))
        changed = sorted(
            key for key in set(expected) & set(readback) if expected[key] != readback[key]
        )
        raise ValueError(
            "pin readback mismatch: missing=%s extra=%s changed=%s"
            % (missing, extra, changed)
        )
    sha256 = hashlib.sha256(protocol_source).hexdigest()
    header = ("blob %d\0" % len(protocol_source)).encode("ascii")
    git_oid = hashlib.sha1(header + protocol_source).hexdigest()
    if sha256 != expected["protocol_file_sha256"]:
        raise ValueError("protocol source SHA-256 mismatch")
    if git_oid != expected["protocol_file_git_oid"]:
        raise ValueError("protocol source Git blob mismatch")
    return {"sha256": sha256, "git_oid": git_oid}

TOP_FIELDS = {
    "handoff.schema.json": frozenset({
        "schema_version", "packet_id", "generation", "spec_hash", "provider", "role",
        "session_id", "base_sha", "head_sha", "status", "summary", "changed_paths",
        "tests", "test_selection", "remaining_work", "next_role", "manual_next_action",
        "copyable_prompt", "failure", "successors",
    }),
    "review.schema.json": frozenset({
        "schema_version", "packet_id", "generation", "provider", "role", "session_id",
        "reviewed_sha", "independent_from_executor_session", "review_axes", "tests",
        "findings", "verdict", "assurance", "evidence_url",
    }),
    "land.schema.json": frozenset({
        "schema_version", "authorization_id", "decision", "mission_id", "mission_revision",
        "change_request", "packet_issue", "packet_id", "packet_revision", "packet_generation",
        "spec_hash", "pr", "authorized_head_sha", "authorized_tree_sha",
        "authorized_base_sha", "target_branch", "integration_mode", "actor", "issued_at",
        "expires_at", "review_assurance", "executor_evidence_ids", "reviewer_evidence_ids",
        "ci_run_id", "ci_check_run_ids", "cumulative_changed_paths", "blocking_findings",
        "advisory_findings_deferred", "authorization_status", "land_evidence_id", "generation",
        "provider", "role", "session_id", "input_packet_generations", "approver",
        "authorization_url", "land_operator", "merge_method", "merge_commit",
        "pre_merge_checks", "post_merge_checks", "bookkeeping", "tests",
    }),
    "state.schema.json": frozenset({
        "schema_version", "mission_issue", "mission_revision", "mission_state", "packet_id",
        "packet_revision", "spec_hash", "packet_state", "lease", "budget", "review_assurance",
        "head_sha", "tested_sha", "handoff_url", "commit_shas", "last_consumed_event_id",
    }),
    "command.schema.json": frozenset({
        "schema_version", "command", "mission_id", "packet_id", "head_sha", "reason",
        "actor", "expected_state_revision",
    }),
}

TOP_REQUIRED = {
    "handoff.schema.json": frozenset({
        "schema_version", "packet_id", "generation", "spec_hash", "provider", "role",
        "session_id", "head_sha", "status", "next_role", "manual_next_action", "copyable_prompt",
    }),
    "review.schema.json": frozenset({
        "schema_version", "packet_id", "generation", "provider", "role", "session_id",
        "reviewed_sha", "independent_from_executor_session", "review_axes", "tests", "findings",
        "verdict", "assurance",
    }),
    "state.schema.json": frozenset({
        "schema_version", "mission_issue", "mission_revision", "mission_state", "last_consumed_event_id",
    }),
    "command.schema.json": frozenset({"schema_version", "command", "actor", "expected_state_revision"}),
}

COMMANDS = (
    "/mission start", "/mission pause", "/mission resume", "/packet retry",
    "/packet cancel", "/packet reroute", "/packet preserve", "/land prepare", "/land apply",
)
ENUMS = {
    ("handoff.schema.json", "provider"): ("claude", "codex"),
    ("handoff.schema.json", "status"): ("done", "needs_followup", "blocked"),
    ("review.schema.json", "provider"): ("claude", "codex", "human"),
    ("review.schema.json", "verdict"): ("approve", "changes_requested", "blocked"),
    ("state.schema.json", "mission_state"): ("proposed", "running", "paused", "blocked", "awaiting_land", "complete", "cancelled"),
    ("command.schema.json", "command"): COMMANDS,
}
CONSTS = {
    ("handoff.schema.json", "schema_version"): 1,
    ("handoff.schema.json", "role"): "executor",
    ("review.schema.json", "schema_version"): 1,
    ("review.schema.json", "role"): "reviewer",
    ("review.schema.json", "independent_from_executor_session"): True,
    ("land.schema.json", "schema_version"): 1,
    ("state.schema.json", "schema_version"): 1,
    ("command.schema.json", "schema_version"): 1,
}
PATTERNS = {
    ("handoff.schema.json", "packet_id"): "wp[1-9][0-9]*",
    ("review.schema.json", "packet_id"): "wp[1-9][0-9]*",
    ("land.schema.json", "mission_id"): "gh-[1-9][0-9]*",
    ("land.schema.json", "packet_id"): "wp[1-9][0-9]*",
    ("state.schema.json", "packet_id"): "wp[1-9][0-9]*",
    ("command.schema.json", "mission_id"): "gh-[1-9][0-9]*",
    ("command.schema.json", "packet_id"): "wp[1-9][0-9]*",
}

LAND_REQUIRED_VARIANTS = (
    frozenset({"schema_version", "authorization_id", "decision", "mission_id", "authorized_head_sha", "actor", "role", "session_id"}),
    frozenset({
        "schema_version", "land_evidence_id", "mission_id", "generation", "provider", "role",
        "session_id", "input_packet_generations", "authorized_head_sha", "approver",
        "authorization_url", "land_operator", "merge_method", "merge_commit", "pre_merge_checks",
        "post_merge_checks", "bookkeeping",
    }),
)


def _local_refs(schema: object):
    if isinstance(schema, dict):
        for key, value in schema.items():
            if key == "$ref":
                yield value
            yield from _local_refs(value)
    elif isinstance(schema, list):
        for value in schema:
            yield from _local_refs(value)


def _resolve_pointer(schema: Mapping[str, object], ref: str) -> object:
    if not isinstance(ref, str) or not ref.startswith("#/"):
        raise ValueError("remote or malformed $ref rejected: %r" % ref)
    node: object = schema
    for raw in ref[2:].split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or key not in node:
            raise ValueError("unresolved local $ref: %s" % ref)
        node = node[key]
    return node


def check_contract(name: str, schema: object) -> list[str]:
    """Compare candidate schema facts with the protocol-derived field contract."""
    errors: list[str] = []
    if name not in EXPECTED_FILES:
        return ["unexpected schema name: %s" % name]
    if not isinstance(schema, dict):
        return ["schema is not an object"]
    if schema.get("$schema") != DIALECT:
        errors.append("dialect must be pinned to %s" % DIALECT)
    if schema.get("type") != "object":
        errors.append("top-level type must be object")
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return errors + ["properties must be an object"]
    actual_fields = frozenset(properties)
    if actual_fields != TOP_FIELDS[name]:
        errors.append("field set mismatch: missing=%s extra=%s" % (
            sorted(TOP_FIELDS[name] - actual_fields), sorted(actual_fields - TOP_FIELDS[name])))
    if name in TOP_REQUIRED:
        actual_required = frozenset(schema.get("required", []))
        if actual_required != TOP_REQUIRED[name]:
            errors.append("required set mismatch: expected=%s got=%s" % (
                sorted(TOP_REQUIRED[name]), sorted(actual_required)))
    if schema.get("additionalProperties") is not True:
        errors.append("top-level additionalProperties must remain true")
    for (schema_name, field), values in ENUMS.items():
        if schema_name == name and tuple(properties.get(field, {}).get("enum", ())) != values:
            errors.append("enum mismatch at properties.%s" % field)
    for (schema_name, field), value in CONSTS.items():
        if schema_name == name and properties.get(field, {}).get("const") != value:
            errors.append("const mismatch at properties.%s" % field)
    for (schema_name, field), value in PATTERNS.items():
        if schema_name == name and properties.get(field, {}).get("pattern") != value:
            errors.append("pattern mismatch at properties.%s" % field)
    if name == "land.schema.json":
        variants = schema.get("oneOf")
        got = tuple(frozenset(item.get("required", [])) for item in variants) if isinstance(variants, list) and all(isinstance(item, dict) for item in variants) else ()
        if got != LAND_REQUIRED_VARIANTS:
            errors.append("land oneOf required variants mismatch")
    if name == "review.schema.json":
        axes = properties.get("review_axes", {})
        if axes.get("uniqueItems") is not True or axes.get("contains") != {"const": "spec"} or axes.get("allOf") != [{"contains": {"const": "standards_security"}}]:
            errors.append("review_axes must require both independent axes")
    if name == "command.schema.json":
        conditionals = schema.get("allOf")
        if not isinstance(conditionals, list) or len(conditionals) != 3:
            errors.append("command conditional requirement set must contain three branches")
    for ref in _local_refs(schema):
        try:
            _resolve_pointer(schema, ref)
        except ValueError as exc:
            errors.append(str(exc))
    return errors
