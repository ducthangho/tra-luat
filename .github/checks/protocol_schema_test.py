#!/usr/bin/env python3
"""Offline validator and executable counter-proofs for protocol artifacts.

The schemas formalize fields and enums from docs/PROTOCOL_DA_PHIEN.md.  This
module intentionally uses only the Python standard library.  With no arguments
it runs the test suite; validation modes are suitable for local callers.
"""

from __future__ import annotations

import argparse
import ast
import copy
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_POINTER = "docs/PROTOCOL_DA_PHIEN.md"
SCHEMA_NAMES = (
    "handoff.schema.json",
    "review.schema.json",
    "land.schema.json",
    "state.schema.json",
    "command.schema.json",
)
FORM_NAMES = ("mission.yml", "work-packet.yml", "change-request.yml")

_FORM_FIXTURES: dict[str, dict[str, Any]] = {
    "mission.yml": {
        "schema_version": 1,
        "mission_id": "gh-123",
        "revision": 1,
        "plan_hash": "1" * 64,
        "supersedes_revision": None,
        "change_request": None,
        "base_sha": "2" * 40,
        "objective": "Deliver one bounded outcome.",
        "acceptance_criteria": ["Evidence is machine-readable."],
        "risk": "normal",
        "requires_live": False,
        "envelope": {
            "max_packets": 20,
            "max_successor_depth": 5,
            "max_attempts_per_packet": 3,
            "max_run_minutes": 45,
            "same_failure_limit": 2,
            "max_parallel_workers": 2,
            "max_agent_invocations": 30,
            "max_cloud_minutes": 360,
            "max_inbox_backlog": 100,
            "provider_budgets": {},
        },
    },
    "work-packet.yml": {
        "schema_version": 1,
        "packet_id": "wp123",
        "mission_issue": 54,
        "revision": 1,
        "spec_hash": "3" * 64,
        "objective": "Produce one reviewable artifact.",
        "write_set": [{"type": "exact", "path": "path/to/file"}],
        "depends_on": [],
        "executor": "codex",
        "environment": "local",
        "risk": "sensitive",
        "acceptance_criteria": ["The offline validator passes."],
    },
    "change-request.yml": {
        "schema_version": 1,
        "change_request_id": "mcr-54-03",
        "mission_issue": 54,
        "requested_by": "repo-owner",
        "reason": "A material constraint changed.",
        "proposed_changes": ["Replace one frozen constraint."],
        "affected_packets": ["wp60"],
        "landed_work_impact": "none",
        "risk_change": "none",
        "decision": "pending",
        "decision_source": "human",
        "approved_by": None,
        "decision_url": None,
        "supersedes_revision": 3,
    },
}

_FORM_ENUMS = {
    ("mission.yml", "risk"): {"normal", "sensitive"},
    ("mission.yml", "requires_live"): {False, True},
    ("work-packet.yml", "executor"): {"claude", "codex"},
    ("work-packet.yml", "environment"): {"cloud", "local"},
    ("work-packet.yml", "risk"): {"normal", "sensitive"},
    ("change-request.yml", "landed_work_impact"): {
        "none",
        "corrective_packet",
        "revert_packet",
    },
    ("change-request.yml", "risk_change"): {"none", "increased", "decreased"},
    ("change-request.yml", "decision"): {"pending", "approved", "rejected"},
    ("change-request.yml", "decision_source"): {"human"},
}

# Exact properties are a counter-drift inventory.  Schema descriptions may
# point to the protocol but do not restate its rules.
_EXPECTED_PROPERTIES: dict[str, set[str]] = {
    "handoff.schema.json": {
        "schema_version",
        "packet_id",
        "generation",
        "spec_hash",
        "provider",
        "role",
        "session_id",
        "base_sha",
        "head_sha",
        "status",
        "summary",
        "changed_paths",
        "tests",
        "test_selection",
        "remaining_work",
        "next_role",
        "manual_next_action",
        "copyable_prompt",
        "failure",
        "successors",
    },
    "review.schema.json": {
        "schema_version",
        "packet_id",
        "generation",
        "provider",
        "role",
        "session_id",
        "reviewed_sha",
        "independent_from_executor_session",
        "review_axes",
        "tests",
        "findings",
        "verdict",
        "assurance",
        "evidence_url",
    },
    "land.schema.json": {
        "schema_version",
        "authorization_id",
        "decision",
        "mission_id",
        "mission_revision",
        "change_request",
        "packet_issue",
        "packet_id",
        "packet_revision",
        "packet_generation",
        "spec_hash",
        "pr",
        "authorized_head_sha",
        "authorized_tree_sha",
        "authorized_base_sha",
        "target_branch",
        "integration_mode",
        "actor",
        "issued_at",
        "expires_at",
        "review_assurance",
        "executor_evidence_ids",
        "reviewer_evidence_ids",
        "ci_run_id",
        "ci_check_run_ids",
        "cumulative_changed_paths",
        "blocking_findings",
        "advisory_findings_deferred",
        "authorization_status",
        "land_evidence_id",
        "generation",
        "provider",
        "role",
        "session_id",
        "input_packet_generations",
        "approver",
        "authorization_url",
        "land_operator",
        "merge_method",
        "merge_commit",
        "pre_merge_checks",
        "post_merge_checks",
        "bookkeeping",
        "tests",
    },
    "state.schema.json": {
        "schema_version",
        "mission_issue",
        "mission_revision",
        "mission_state",
        "packet_id",
        "packet_revision",
        "spec_hash",
        "packet_state",
        "lease",
        "budget",
        "review_assurance",
        "head_sha",
        "tested_sha",
        "handoff_url",
        "commit_shas",
        "last_consumed_event_id",
    },
    "command.schema.json": {
        "schema_version",
        "command",
        "mission_id",
        "packet_id",
        "head_sha",
        "reason",
        "actor",
        "expected_state_revision",
    },
}

_EXPECTED_REQUIRED: dict[tuple[str, str], set[str]] = {
    ("handoff.schema.json", "/required"): {
        "schema_version",
        "packet_id",
        "generation",
        "spec_hash",
        "provider",
        "role",
        "session_id",
        "head_sha",
        "status",
        "next_role",
        "manual_next_action",
        "copyable_prompt",
    },
    ("handoff.schema.json", "/$defs/test_passed/required"): {
        "name",
        "status",
        "evidence",
    },
    ("handoff.schema.json", "/$defs/test_not_run/required"): {
        "name",
        "status",
        "evidence",
        "reason",
    },
    ("handoff.schema.json", "/$defs/test_selection/required"): {
        "gate_tier",
        "selector_policy_sha",
        "tested_sha",
        "selected_groups",
        "full_fallback_reason",
    },
    ("handoff.schema.json", "/$defs/failure/required"): {
        "fingerprint",
        "category",
    },
    ("handoff.schema.json", "/$defs/successor/required"): {
        "successor_key",
        "objective",
        "write_set",
        "depends_on",
        "executor",
        "environment",
        "acceptance_criteria",
    },
    ("review.schema.json", "/required"): {
        "schema_version",
        "packet_id",
        "generation",
        "provider",
        "role",
        "session_id",
        "reviewed_sha",
        "independent_from_executor_session",
        "review_axes",
        "tests",
        "findings",
        "verdict",
        "assurance",
    },
    ("review.schema.json", "/$defs/test_passed/required"): {
        "name",
        "status",
        "evidence",
    },
    ("review.schema.json", "/$defs/test_not_run/required"): {
        "name",
        "status",
        "evidence",
        "reason",
    },
    ("land.schema.json", "/oneOf/0/required"): {
        "schema_version",
        "authorization_id",
        "decision",
        "mission_id",
        "authorized_head_sha",
        "actor",
        "role",
        "session_id",
    },
    ("land.schema.json", "/oneOf/1/required"): {
        "schema_version",
        "land_evidence_id",
        "mission_id",
        "generation",
        "provider",
        "role",
        "session_id",
        "input_packet_generations",
        "authorized_head_sha",
        "approver",
        "authorization_url",
        "land_operator",
        "merge_method",
        "merge_commit",
        "pre_merge_checks",
        "post_merge_checks",
        "bookkeeping",
    },
    ("land.schema.json", "/$defs/test_passed/required"): {
        "name",
        "status",
        "evidence",
    },
    ("land.schema.json", "/$defs/test_not_run/required"): {
        "name",
        "status",
        "evidence",
        "reason",
    },
    ("state.schema.json", "/required"): {
        "schema_version",
        "mission_issue",
        "mission_revision",
        "mission_state",
        "last_consumed_event_id",
    },
    ("state.schema.json", "/$defs/lease/required"): {
        "packet_id",
        "executor",
        "environment",
        "branch",
        "write_set_hash",
        "generation",
        "heartbeat_at",
        "lease_until",
    },
    ("state.schema.json", "/$defs/budget/required"): {
        "used",
        "reserved",
        "limit",
    },
    ("command.schema.json", "/required"): {
        "schema_version",
        "command",
        "actor",
        "expected_state_revision",
    },
    ("command.schema.json", "/allOf/0/then/required"): {"mission_id"},
    ("command.schema.json", "/allOf/1/then/required"): {"packet_id", "reason"},
    ("command.schema.json", "/allOf/2/then/required"): {"mission_id", "head_sha"},
}

_ALLOWED_SCHEMA_KEYWORDS = {
    "$schema",
    "$id",
    "$ref",
    "$defs",
    "title",
    "description",
    "type",
    "properties",
    "required",
    "additionalProperties",
    "items",
    "enum",
    "const",
    "pattern",
    "minItems",
    "maxItems",
    "contains",
    "allOf",
    "anyOf",
    "oneOf",
    "if",
    "then",
    "else",
    "minLength",
    "minimum",
    "maximum",
    "uniqueItems",
}


def _pointer(parts: list[str | int]) -> str:
    if not parts:
        return "/"
    return "/" + "/".join(str(part).replace("~", "~0").replace("/", "~1") for part in parts)


def _resolve_pointer(document: Any, pointer: str) -> Any:
    node = document
    for token in pointer.strip("/").split("/") if pointer != "/" else []:
        token = token.replace("~1", "/").replace("~0", "~")
        node = node[int(token)] if isinstance(node, list) else node[token]
    return node


def _schema_keyword_errors(schema: Any, path: list[str | int] | None = None) -> list[str]:
    path = path or []
    errors: list[str] = []
    if not isinstance(schema, dict):
        return errors
    for key in schema:
        if key not in _ALLOWED_SCHEMA_KEYWORDS:
            errors.append(f"{_pointer(path)}/{key}: unsupported schema keyword")
    for key, value in schema.items():
        if key in {"properties", "$defs"} and isinstance(value, dict):
            for name, child in value.items():
                errors.extend(_schema_keyword_errors(child, path + [key, name]))
        elif key in {"items", "contains", "if", "then", "else", "additionalProperties"}:
            if isinstance(value, dict):
                errors.extend(_schema_keyword_errors(value, path + [key]))
        elif key in {"allOf", "anyOf", "oneOf"} and isinstance(value, list):
            for index, child in enumerate(value):
                errors.extend(_schema_keyword_errors(child, path + [key, index]))
    return errors


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, False)


def _validate(
    schema: dict[str, Any],
    value: Any,
    root_schema: dict[str, Any],
    path: list[str | int] | None = None,
) -> list[dict[str, str]]:
    path = path or []
    errors: list[dict[str, str]] = []

    if "$ref" in schema:
        ref = schema["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/"):
            return [{"path": _pointer(path), "keyword": "$ref", "message": "only local refs are supported"}]
        return _validate(_resolve_pointer(root_schema, ref[1:]), value, root_schema, path)

    expected_type = schema.get("type")
    if expected_type is not None:
        expected_types = [expected_type] if isinstance(expected_type, str) else expected_type
        if not any(_type_matches(value, item) for item in expected_types):
            return [
                {
                    "path": _pointer(path),
                    "keyword": "type",
                    "message": f"expected {expected_types!r}",
                }
            ]

    if "enum" in schema and value not in schema["enum"]:
        errors.append({"path": _pointer(path), "keyword": "enum", "message": "value is not in enum"})
    if "const" in schema and value != schema["const"]:
        errors.append({"path": _pointer(path), "keyword": "const", "message": "value does not match const"})
    if isinstance(value, str):
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append({"path": _pointer(path), "keyword": "pattern", "message": "string does not match"})
        if len(value) < schema.get("minLength", 0):
            errors.append({"path": _pointer(path), "keyword": "minLength", "message": "string is too short"})
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append({"path": _pointer(path), "keyword": "minimum", "message": "number is too small"})
        if "maximum" in schema and value > schema["maximum"]:
            errors.append({"path": _pointer(path), "keyword": "maximum", "message": "number is too large"})

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(
                    {
                        "path": _pointer(path + [required]),
                        "keyword": "required",
                        "message": "required property is missing",
                    }
                )
        for key, child in value.items():
            if key in properties:
                errors.extend(_validate(properties[key], child, root_schema, path + [key]))
            elif schema.get("additionalProperties") is False:
                errors.append(
                    {
                        "path": _pointer(path + [key]),
                        "keyword": "additionalProperties",
                        "message": "unexpected property",
                    }
                )
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(_validate(schema["additionalProperties"], child, root_schema, path + [key]))

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append({"path": _pointer(path), "keyword": "minItems", "message": "array is too short"})
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append({"path": _pointer(path), "keyword": "maxItems", "message": "array is too long"})
        if schema.get("uniqueItems"):
            encoded = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(encoded) != len(set(encoded)):
                errors.append({"path": _pointer(path), "keyword": "uniqueItems", "message": "items repeat"})
        if isinstance(schema.get("items"), dict):
            for index, child in enumerate(value):
                errors.extend(_validate(schema["items"], child, root_schema, path + [index]))
        if "contains" in schema and not any(
            not _validate(schema["contains"], child, root_schema, path + [index])
            for index, child in enumerate(value)
        ):
            errors.append({"path": _pointer(path), "keyword": "contains", "message": "no item matches"})

    for child in schema.get("allOf", []):
        errors.extend(_validate(child, value, root_schema, path))
    if "anyOf" in schema:
        if not any(not _validate(child, value, root_schema, path) for child in schema["anyOf"]):
            errors.append({"path": _pointer(path), "keyword": "anyOf", "message": "no branch matches"})
    if "oneOf" in schema:
        branches = [_validate(child, value, root_schema, path) for child in schema["oneOf"]]
        matched = sum(not branch for branch in branches)
        if matched != 1:
            errors.append(
                {
                    "path": _pointer(path),
                    "keyword": "oneOf",
                    "message": f"expected exactly one matching branch; got {matched}",
                }
            )
            if matched == 0 and branches:
                errors.extend(min(branches, key=len))
    if "if" in schema:
        condition_matches = not _validate(schema["if"], value, root_schema, path)
        selected = schema.get("then") if condition_matches else schema.get("else")
        if selected:
            errors.extend(_validate(selected, value, root_schema, path))
    return errors


def _split_flow(text: str, delimiter: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    escaped = False
    for index, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote == '"':
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
        elif char == delimiter and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def _split_key_value(text: str) -> tuple[str, str] | None:
    parts = _split_flow(text, ":")
    if len(parts) < 2:
        return None
    return parts[0], ":".join(parts[1:]).strip()


def _scalar(text: str) -> Any:
    text = text.strip()
    if text in {"", "null", "Null", "NULL", "~"}:
        return None
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [] if not inner else [_scalar(part) for part in _split_flow(inner, ",")]
    if text.startswith("{") and text.endswith("}"):
        result: dict[str, Any] = {}
        inner = text[1:-1].strip()
        if not inner:
            return result
        for part in _split_flow(inner, ","):
            split = _split_key_value(part)
            if split is None:
                raise ValueError(f"invalid flow mapping: {part}")
            key, value = split
            result[str(_scalar(key))] = _scalar(value)
        return result
    if text[:1] in {'"', "'"} and text[-1:] == text[:1]:
        return ast.literal_eval(text)
    if re.fullmatch(r"-?[0-9]+", text):
        return int(text)
    return text


def _yaml_subset(text: str) -> Any:
    raw_lines = text.replace("\r\n", "\n").split("\n")
    lines = [(len(line) - len(line.lstrip(" ")), line.lstrip(" ")) for line in raw_lines if line.strip()]

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        is_list = lines[index][1].startswith("- ")
        container: Any = [] if is_list else {}
        while index < len(lines):
            current_indent, content = lines[index]
            if current_indent < indent:
                break
            if current_indent != indent:
                raise ValueError(f"unexpected indentation at line {index + 1}")
            if is_list:
                if not content.startswith("- "):
                    break
                item = content[2:].strip()
                split = _split_key_value(item)
                if split is not None and not item.startswith(("{", "[", "'", '"')):
                    key, rest = split
                    mapping: dict[str, Any] = {str(_scalar(key)): _scalar(rest) if rest else None}
                    index += 1
                    while index < len(lines) and lines[index][0] > indent:
                        child_indent, child_content = lines[index]
                        child_split = _split_key_value(child_content)
                        if child_split is None:
                            raise ValueError(f"invalid mapping continuation at line {index + 1}")
                        child_key, child_rest = child_split
                        child_key = str(_scalar(child_key))
                        if child_rest in {"|", "|-", ">", ">-"}:
                            block_indent = child_indent + 2
                            values: list[str] = []
                            index += 1
                            while index < len(lines) and lines[index][0] >= block_indent:
                                values.append(" " * (lines[index][0] - block_indent) + lines[index][1])
                                index += 1
                            mapping[child_key] = "\n".join(values)
                        elif child_rest:
                            mapping[child_key] = _scalar(child_rest)
                            index += 1
                        elif index + 1 < len(lines) and lines[index + 1][0] > child_indent:
                            mapping[child_key], index = parse_block(index + 1, lines[index + 1][0])
                        else:
                            mapping[child_key] = None
                            index += 1
                    container.append(mapping)
                    continue
                container.append(_scalar(item))
                index += 1
                continue

            if content.startswith("- "):
                break
            split = _split_key_value(content)
            if split is None:
                raise ValueError(f"invalid mapping at line {index + 1}")
            key, rest = split
            key = str(_scalar(key))
            if rest in {"|", "|-", ">", ">-"}:
                block_indent = indent + 2
                values: list[str] = []
                index += 1
                while index < len(lines) and lines[index][0] >= block_indent:
                    values.append(" " * (lines[index][0] - block_indent) + lines[index][1])
                    index += 1
                container[key] = "\n".join(values)
            elif rest:
                container[key] = _scalar(rest)
                index += 1
            elif index + 1 < len(lines) and lines[index + 1][0] > indent:
                container[key], index = parse_block(index + 1, lines[index + 1][0])
            else:
                container[key] = None
                index += 1
        return container, index

    if not lines:
        return None
    value, end = parse_block(0, lines[0][0])
    if end != len(lines):
        raise ValueError("unparsed YAML content")
    return value


def _load_document(text: str, format_name: str) -> Any:
    if format_name == "json":
        return json.loads(text)
    if format_name == "yaml":
        return _yaml_subset(text)
    if format_name == "markdown":
        match = re.search(r"```(?:yaml|json)\s*\n(.*?)\n```", text, re.DOTALL)
        if not match:
            raise ValueError("no fenced YAML/JSON block found")
        fenced = match.group(1)
        return json.loads(fenced) if fenced.lstrip().startswith(("{", "[")) else _yaml_subset(fenced)
    raise ValueError(f"unsupported document format: {format_name}")


def _load_artifact(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return _yaml_subset(text)


def _contract_errors(root: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    required_count = 0
    for name in SCHEMA_NAMES:
        path = root / ".github" / "schemas" / name
        if not path.is_file():
            errors.append(f"missing schema: {name}")
            continue
        schema = _load_artifact(path)
        errors.extend(f"{name}:{message}" for message in _schema_keyword_errors(schema))
        actual_properties = set(schema.get("properties", {}))
        if actual_properties != _EXPECTED_PROPERTIES[name]:
            errors.append(
                f"{name}: root properties drift: missing={sorted(_EXPECTED_PROPERTIES[name] - actual_properties)} "
                f"extra={sorted(actual_properties - _EXPECTED_PROPERTIES[name])}"
            )
        for node in _walk_dicts(schema):
            description = node.get("description")
            if description is not None and (
                not isinstance(description, str)
                or PROTOCOL_POINTER not in description
                or len(description) > 240
            ):
                errors.append(f"{name}: description must be <=240 chars and point to {PROTOCOL_POINTER}")
    for (name, pointer), expected in _EXPECTED_REQUIRED.items():
        path = root / ".github" / "schemas" / name
        if not path.is_file():
            continue
        schema = _load_artifact(path)
        try:
            actual = set(_resolve_pointer(schema, pointer))
        except (KeyError, IndexError, TypeError):
            actual = set()
        required_count += len(expected)
        if actual != expected:
            errors.append(
                f"{name}{pointer}: required drift: missing={sorted(expected - actual)} extra={sorted(actual - expected)}"
            )

    for name in FORM_NAMES:
        path = root / ".github" / "ISSUE_TEMPLATE" / name
        if not path.is_file():
            errors.append(f"missing form: {name}")
            continue
        form = _load_artifact(path)
        items = [item for item in form.get("body", []) if item.get("id")]
        ids = {item["id"] for item in items}
        expected_ids = set(_FORM_FIXTURES[name])
        if ids != expected_ids:
            errors.append(f"{name}: field drift: missing={sorted(expected_ids - ids)} extra={sorted(ids - expected_ids)}")
        required_ids = {
            item["id"] for item in items if item.get("validations", {}).get("required") is True
        }
        required_count += len(expected_ids)
        if required_ids != expected_ids:
            errors.append(
                f"{name}: required drift: missing={sorted(expected_ids - required_ids)} extra={sorted(required_ids - expected_ids)}"
            )
        markdown = [item for item in form.get("body", []) if item.get("type") == "markdown"]
        for item in markdown:
            value = item.get("attributes", {}).get("value", "")
            if PROTOCOL_POINTER not in value or len(value) > 360:
                errors.append(f"{name}: markdown must be <=360 chars and point to {PROTOCOL_POINTER}")
    return errors, required_count


def _walk_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_dicts(child)


def _render_form_body(form: dict[str, Any], values: dict[str, Any]) -> str:
    sections: list[str] = []
    for item in form.get("body", []):
        field_id = item.get("id")
        if not field_id or field_id not in values:
            continue
        label = item.get("attributes", {}).get("label", field_id)
        value = values[field_id]
        if isinstance(value, (dict, list)):
            rendered = "```json\n" + json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n```"
        elif value is None:
            rendered = "null"
        elif isinstance(value, bool):
            rendered = str(value).lower()
        else:
            rendered = str(value)
        sections.append(f"### {label}\n\n{rendered}")
    return "\n\n".join(sections) + "\n"


def _parse_form_body(form: dict[str, Any], text: str, name: str) -> tuple[dict[str, Any], list[dict[str, str]]]:
    label_to_id = {
        item.get("attributes", {}).get("label", item.get("id")): item.get("id")
        for item in form.get("body", [])
        if item.get("id")
    }
    matches = list(re.finditer(r"(?m)^### (.+?)\s*$", text))
    raw_values: dict[str, str] = {}
    for index, match in enumerate(matches):
        label = match.group(1)
        field_id = label_to_id.get(label)
        if field_id is None:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        raw_values[field_id] = text[match.end() : end].strip()
    values: dict[str, Any] = {}
    errors: list[dict[str, str]] = []
    expected = _FORM_FIXTURES[name]
    for field_id, prototype in expected.items():
        if field_id not in raw_values or raw_values[field_id] in {"", "_No response_"}:
            errors.append(
                {"path": f"/{field_id}", "keyword": "required", "message": "required form field is missing"}
            )
            continue
        raw = raw_values[field_id]
        fence = re.fullmatch(r"```json\s*\n(.*?)\n```", raw, re.DOTALL)
        if fence:
            raw = fence.group(1)
        try:
            if isinstance(prototype, (dict, list)):
                value = json.loads(raw)
            elif prototype is None:
                value = None if raw == "null" else raw
            elif isinstance(prototype, bool):
                if raw not in {"true", "false"}:
                    raise ValueError("expected true or false")
                value = raw == "true"
            elif isinstance(prototype, int):
                value = int(raw)
            else:
                value = raw
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append({"path": f"/{field_id}", "keyword": "parse", "message": str(exc)})
            continue
        if not isinstance(value, type(prototype)) and prototype is not None:
            errors.append({"path": f"/{field_id}", "keyword": "type", "message": "wrong field type"})
        enum = _FORM_ENUMS.get((name, field_id))
        if enum is not None and value not in enum:
            errors.append({"path": f"/{field_id}", "keyword": "enum", "message": "value is not in enum"})
        values[field_id] = value
    if name == "mission.yml":
        if not re.fullmatch(r"gh-[1-9][0-9]*", str(values.get("mission_id", ""))):
            errors.append({"path": "/mission_id", "keyword": "pattern", "message": "invalid mission id"})
        if not re.fullmatch(r"[0-9a-f]{64}", str(values.get("plan_hash", ""))):
            errors.append({"path": "/plan_hash", "keyword": "pattern", "message": "invalid plan hash"})
        if not re.fullmatch(r"[0-9a-f]{40}", str(values.get("base_sha", ""))):
            errors.append({"path": "/base_sha", "keyword": "pattern", "message": "invalid base sha"})
    if name == "work-packet.yml":
        if not re.fullmatch(r"wp[1-9][0-9]*", str(values.get("packet_id", ""))):
            errors.append({"path": "/packet_id", "keyword": "pattern", "message": "invalid packet id"})
        if not re.fullmatch(r"[0-9a-f]{64}", str(values.get("spec_hash", ""))):
            errors.append({"path": "/spec_hash", "keyword": "pattern", "message": "invalid spec hash"})
    return values, errors


def _valid_documents() -> dict[str, dict[str, Any]]:
    passed = {"name": "gate", "status": "passed", "evidence": "rc 0; ok=true"}
    return {
        "handoff.schema.json": {
            "schema_version": 1,
            "packet_id": "wp60",
            "generation": 7,
            "spec_hash": "3" * 64,
            "provider": "codex",
            "role": "executor",
            "session_id": "codex-wp60-r1g7-executor-01",
            "base_sha": "4" * 40,
            "head_sha": None,
            "status": "done",
            "summary": "Schema artifacts reconstructed.",
            "changed_paths": [".github/schemas/handoff.schema.json"],
            "tests": [passed],
            "test_selection": {
                "gate_tier": "T2",
                "selector_policy_sha": "5" * 40,
                "tested_sha": "6" * 40,
                "selected_groups": ["full"],
                "full_fallback_reason": "sensitive packet",
            },
            "remaining_work": [],
            "next_role": "reviewer",
            "manual_next_action": "Start a fresh reviewer.",
            "copyable_prompt": "Review exact head in a read-only worktree.",
            "failure": {"fingerprint": None, "category": None},
            "successors": [],
        },
        "review.schema.json": {
            "schema_version": 1,
            "packet_id": "wp60",
            "generation": 7,
            "provider": "claude",
            "role": "reviewer",
            "session_id": "claude-wp60-r1g7-reviewer-01",
            "reviewed_sha": "6" * 40,
            "independent_from_executor_session": True,
            "review_axes": ["spec", "standards_security"],
            "tests": [passed],
            "findings": [],
            "verdict": "approve",
            "assurance": "cross_approved",
            "evidence_url": "https://github.com/ducthangho/tra-luat/pull/1#issuecomment-1",
        },
        "land.schema.json": {
            "schema_version": 1,
            "land_evidence_id": "WP60-R1G7-LAND-EVIDENCE-01",
            "mission_id": "gh-54",
            "generation": 1,
            "provider": "human",
            "role": "land_operator",
            "session_id": "human-land-01",
            "input_packet_generations": ["wp60@7"],
            "authorized_head_sha": "6" * 40,
            "approver": "repo-owner",
            "authorization_url": "https://github.com/ducthangho/tra-luat/issues/60#issuecomment-1",
            "land_operator": "repo-owner",
            "merge_method": "merge",
            "merge_commit": "7" * 40,
            "pre_merge_checks": [],
            "post_merge_checks": [],
            "bookkeeping": [],
            "tests": [passed],
        },
        "state.schema.json": {
            "schema_version": 1,
            "mission_issue": 54,
            "mission_revision": 3,
            "mission_state": "running",
            "packet_id": "wp60",
            "packet_revision": 1,
            "spec_hash": "3" * 64,
            "packet_state": "running",
            "lease": {
                "packet_id": "wp60",
                "executor": "codex",
                "environment": "local",
                "branch": "codex/wp60-g7-f3-01-github-schema",
                "write_set_hash": "8" * 64,
                "generation": 7,
                "heartbeat_at": "2026-08-09T22:09:28Z",
                "lease_until": "2026-08-10T00:06:30Z",
            },
            "budget": {"used": 1, "reserved": 1, "limit": 30},
            "review_assurance": "review_deferred",
            "head_sha": None,
            "tested_sha": None,
            "handoff_url": None,
            "commit_shas": [],
            "last_consumed_event_id": 5234096965,
        },
        "command.schema.json": {
            "schema_version": 1,
            "command": "/land apply",
            "mission_id": "gh-54",
            "head_sha": "6" * 40,
            "reason": "Apply the authorized exact head.",
            "actor": "repo-owner",
            "expected_state_revision": 12,
        },
    }


_WP57_EXECUTOR = """schema_version: 1
packet_id: wp57
revision: 3
generation: 3
spec_hash: 228ecb03adbaa1ac160fd1ea4b614c56300cbaab01809c8859aeef624f5de2fc
provider: codex
role: executor
session_id: codex-20260808-wp57-g3
superseded_head_sha: f27287c9379ba6640bc14604d4ccc9afe228861a
head_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
tested_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
branch: codex/wp57-g3-f3-00-automation-first
pr: https://github.com/ducthangho/tra-luat/pull/59
status: done
verdict: ready_for_rereview
gate_tier: T2
full_fallback_reason: sensitive packet; legacy runner + manifest changed; selector pre-activation
changed_path_count: 8
remaining_work: []
next_role: reviewer
manual_next_action: create a fresh cross-provider Claude Reviewer on exact generation-3 head
executor_evidence_url: https://github.com/ducthangho/tra-luat/pull/59#issuecomment-5225389852
"""

_WP57_REVIEWER = """schema_version: 1
packet_id: wp57
mission_issue: 54
packet_issue: 57
revision: 3
generation: 3
spec_hash: 228ecb03adbaa1ac160fd1ea4b614c56300cbaab01809c8859aeef624f5de2fc
provider: claude
role: reviewer
session_id: claude-20260808-wp57-g3-review
base_sha: 0844c0bc24399fa4b8430750dc69f7388c23eb8b
reviewed_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
tested_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
branch: codex/wp57-g3-f3-00-automation-first
pr: https://github.com/ducthangho/tra-luat/pull/59
independence: fresh session; read-only; did not execute this packet; no write/commit/push/rebase
superseded_evidence_used: none
verdict: approve
assurance: cross_approved
axes: [spec, standards_security]
gate_tier: T2
findings: [WP57-R3G3-CLD-01, WP57-R3G3-CLD-02, WP57-R3G3-CLD-03]
blocking_findings: []
next_role: land_operator
manual_next_action: reconciler/Approver quyết định bước kế; Reviewer không merge/land
land_authorization: absent
issue_projection: state:reviewing
pr_state: draft
"""

_WP57_AUTHORIZATION = """schema_version: 1
authorization_id: WP57-R3G3-LAND-AUTH-01
decision: approved
mission_id: gh-54
mission_revision: 3
change_request: MCR-54-02
packet_issue: 57
packet_id: wp57
packet_revision: 3
packet_generation: 3
spec_hash: 228ecb03adbaa1ac160fd1ea4b614c56300cbaab01809c8859aeef624f5de2fc
pr: https://github.com/ducthangho/tra-luat/pull/59
authorized_head_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
authorized_tree_sha: 194bac05ceeefeafe4d3eff30fadfa27a311dcf1
authorized_base_sha: 0844c0bc24399fa4b8430750dc69f7388c23eb8b
target_branch: master
integration_mode: bootstrap_direct_canonical
merge_method: merge
actor: ducthangho
provider: codex
role: approver_land_operator
session_id: codex-20260808-wp57-r3g3-approver-land
issued_at: 2026-08-08T09:21:20Z
expires_at: 2026-08-08T11:21:20Z
review_assurance: cross_approved
executor_evidence_ids: [5225391077, 5225389852]
reviewer_evidence_ids: [5225459747, 5225459844]
ci_run_id: 31249160032
ci_check_run_ids: [93082632941, 93082632896]
cumulative_changed_paths: 10
blocking_findings: []
advisory_findings_deferred: [WP57-R3G3-CLD-01, WP57-R3G3-CLD-02, WP57-R3G3-CLD-03]
authorization_status: active
"""

_WP57_LAND = """schema_version: 1
land_evidence_id: WP57-R3G3-LAND-EVIDENCE-01
mission_id: gh-54
generation: 1
provider: codex
role: land_operator
session_id: codex-20260808-wp57-r3g3-approver-land
input_packet_generations: [wp57@3]
authorized_head_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
authorized_tree_sha: 194bac05ceeefeafe4d3eff30fadfa27a311dcf1
approver: ducthangho
authorization_url: https://github.com/ducthangho/tra-luat/issues/57#issuecomment-5225492673
land_operator: ducthangho
merge_method: merge
merge_commit: 3910bd2cb7a933fce82f22eb4d0b73b56f7ec8a3
canonical_tree_sha: 194bac05ceeefeafe4d3eff30fadfa27a311dcf1
pre_merge_checks:
  - {run_id: 31249160032, head_sha: 2a384acf14c374b58b6045b83d91694a16f65c12, conclusion: success, os: [ubuntu-latest, windows-latest]}
  - {review_issue_comment_id: 5225459747, review_pr_comment_id: 5225459844, assurance: cross_approved}
post_merge_checks:
  - {run_id: 31250454568, head_sha: 3910bd2cb7a933fce82f22eb4d0b73b56f7ec8a3, conclusion: success}
  - {job_id: 93085901542, os: ubuntu-latest, conclusion: success}
  - {job_id: 93085901565, os: windows-latest, conclusion: success}
bookkeeping:
  - pending: set Packet #57 projection state:landed
  - pending: close Packet #57 as completed
  - keep Mission #54 open; no mission-complete claim
advisory_findings_deferred: [WP57-R3G3-CLD-01, WP57-R3G3-CLD-02, WP57-R3G3-CLD-03]
status: applied_checks_green_pending_bookkeeping
"""


def _run_process(args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), *args],
        input=input_text,
        text=True,
        encoding="utf-8",
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _run_suite() -> int:
    total = 0
    passed = 0
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        nonlocal total, passed
        total += 1
        if condition:
            passed += 1
        else:
            failures.append(f"{name}: {detail}")

    contract = _run_process(["--contract-check"])
    check("contract_inventory", contract.returncode == 0, contract.stdout + contract.stderr)

    with tempfile.TemporaryDirectory(prefix="wp60-schema-") as temporary:
        temp = Path(temporary)
        valid_documents = _valid_documents()
        for schema_name, document in valid_documents.items():
            document_path = temp / f"valid-{schema_name}.json"
            _write_json(document_path, document)
            result = _run_process(
                [
                    "--schema",
                    str(ROOT / ".github" / "schemas" / schema_name),
                    "--document",
                    str(document_path),
                    "--format",
                    "json",
                ]
            )
            check(f"valid_{schema_name}", result.returncode == 0, result.stdout + result.stderr)

        for form_name, values in _FORM_FIXTURES.items():
            form_path = ROOT / ".github" / "ISSUE_TEMPLATE" / form_name
            form = _load_artifact(form_path) if form_path.is_file() else {"body": []}
            valid_body = _render_form_body(form, values)
            body_path = temp / f"valid-{form_name}.md"
            body_path.write_text(valid_body, encoding="utf-8", newline="\n")
            result = _run_process(
                ["--form", str(form_path), "--document", str(body_path), "--form-name", form_name]
            )
            check(f"valid_form_{form_name}", result.returncode == 0, result.stdout + result.stderr)
            for field_id in values:
                missing_values = dict(values)
                missing_values.pop(field_id)
                body_path.write_text(_render_form_body(form, missing_values), encoding="utf-8", newline="\n")
                result = _run_process(
                    ["--form", str(form_path), "--document", str(body_path), "--form-name", form_name]
                )
                check(
                    f"form_{form_name}_missing_{field_id}",
                    result.returncode == 1 and f'"path": "/{field_id}"' in result.stdout,
                    result.stdout + result.stderr,
                )

        # Every frozen required entry has mutation teeth: deleting it from the
        # artifact makes the contract subprocess red.
        mutation_count = 0
        for (schema_name, pointer), fields in _EXPECTED_REQUIRED.items():
            source_schema = _load_artifact(ROOT / ".github" / "schemas" / schema_name)
            for field in sorted(fields):
                mutation_count += 1
                mutation_root = temp / "mutation-root"
                for name in SCHEMA_NAMES:
                    _write_json(
                        mutation_root / ".github" / "schemas" / name,
                        _load_artifact(ROOT / ".github" / "schemas" / name),
                    )
                for name in FORM_NAMES:
                    _write_json(
                        mutation_root / ".github" / "ISSUE_TEMPLATE" / name,
                        _load_artifact(ROOT / ".github" / "ISSUE_TEMPLATE" / name),
                    )
                mutated = copy.deepcopy(source_schema)
                required = _resolve_pointer(mutated, pointer)
                required.remove(field)
                _write_json(mutation_root / ".github" / "schemas" / schema_name, mutated)
                result = _run_process(["--contract-check", "--root", str(mutation_root)])
                check(
                    f"required_mutation_{schema_name}_{field}",
                    result.returncode == 1 and "required drift" in result.stdout,
                    result.stdout + result.stderr,
                )

        review = valid_documents["review.schema.json"]
        for label, mutation in (
            ("review_independence_false", {"independent_from_executor_session": False}),
            ("review_one_axis", {"review_axes": ["spec"]}),
        ):
            document = copy.deepcopy(review)
            document.update(mutation)
            path = temp / f"{label}.json"
            _write_json(path, document)
            result = _run_process(
                ["--schema", str(ROOT / ".github/schemas/review.schema.json"), "--document", str(path)]
            )
            check(label, result.returncode == 1, result.stdout + result.stderr)

        no_reason = copy.deepcopy(review)
        no_reason["tests"] = [{"name": "skipped", "status": "not_run", "evidence": "not executed"}]
        path = temp / "not-run-no-reason.json"
        _write_json(path, no_reason)
        result = _run_process(
            ["--schema", str(ROOT / ".github/schemas/review.schema.json"), "--document", str(path)]
        )
        check("not_run_requires_reason", result.returncode == 1, result.stdout + result.stderr)
        no_reason["tests"][0]["reason"] = "preflight stopped"
        _write_json(path, no_reason)
        result = _run_process(
            ["--schema", str(ROOT / ".github/schemas/review.schema.json"), "--document", str(path)]
        )
        check("not_run_with_reason", result.returncode == 0, result.stdout + result.stderr)

        command = valid_documents["command.schema.json"]
        for label, bad_sha in (("authority_sha_null", None), ("authority_sha_short", "abc1234")):
            document = dict(command)
            document["head_sha"] = bad_sha
            path = temp / f"{label}.json"
            _write_json(path, document)
            result = _run_process(
                ["--schema", str(ROOT / ".github/schemas/command.schema.json"), "--document", str(path)]
            )
            check(label, result.returncode == 1, result.stdout + result.stderr)

        # Unknown schema keywords are infrastructure errors, never green.
        unknown_schema = _load_artifact(ROOT / ".github/schemas/state.schema.json")
        unknown_schema["containss"] = {"const": 1}
        unknown_path = temp / "unknown-keyword.schema.json"
        _write_json(unknown_path, unknown_schema)
        document_path = temp / "state.json"
        _write_json(document_path, valid_documents["state.schema.json"])
        result = _run_process(
            ["--schema", str(unknown_path), "--document", str(document_path)]
        )
        check("unknown_keyword_rc2", result.returncode == 2, result.stdout + result.stderr)

        reverse = (
            ("5225391077", "handoff.schema.json", _WP57_EXECUTOR, 1, {("/copyable_prompt", "required")}),
            (
                "5225459747",
                "review.schema.json",
                _WP57_REVIEWER,
                1,
                {
                    ("/independent_from_executor_session", "required"),
                    ("/review_axes", "required"),
                    ("/tests", "required"),
                },
            ),
            ("5225492673", "land.schema.json", _WP57_AUTHORIZATION, 0, set()),
            ("5225520427", "land.schema.json", _WP57_LAND, 0, set()),
        )
        for comment_id, schema_name, yaml_text, expected_rc, expected_errors in reverse:
            result = _run_process(
                [
                    "--schema",
                    str(ROOT / ".github" / "schemas" / schema_name),
                    "--format",
                    "yaml",
                ],
                input_text=yaml_text,
            )
            observed: set[tuple[str, str]] = set()
            try:
                payload = json.loads(result.stdout)
                observed = {(error["path"], error["keyword"]) for error in payload.get("errors", [])}
            except json.JSONDecodeError:
                pass
            check(
                f"reverse_wp57_{comment_id}",
                result.returncode == expected_rc and observed == expected_errors,
                result.stdout + result.stderr,
            )

    print(f"required inventory: {sum(len(value) for value in _EXPECTED_REQUIRED.values())} entries")
    print(f"required mutation counter-proofs: {mutation_count}/{mutation_count}")
    for failure in failures:
        print(f"[FAIL] {failure}")
    print(f"== protocol_schema_test {passed}/{total} ==")
    return 0 if passed == total else 1


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--form", type=Path)
    parser.add_argument("--form-name", choices=FORM_NAMES)
    parser.add_argument("--document", type=Path)
    parser.add_argument("--format", choices=("json", "yaml", "markdown"), default="json")
    parser.add_argument("--contract-check", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    if args.contract_check:
        errors, required_count = _contract_errors(args.root.resolve())
        payload = {
            "ok": not errors,
            "required_inventory": required_count,
            "error_count": len(errors),
            "errors": errors,
        }
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return 0 if not errors else 1

    if args.schema:
        try:
            schema = _load_artifact(args.schema)
            keyword_errors = _schema_keyword_errors(schema)
            if keyword_errors:
                print(json.dumps({"ok": False, "infrastructure_errors": keyword_errors}, ensure_ascii=False))
                return 2
            text = args.document.read_text(encoding="utf-8") if args.document else sys.stdin.read()
            document = _load_document(text, args.format)
            errors = _validate(schema, document, schema)
        except (OSError, ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
            print(json.dumps({"ok": False, "parse_error": str(exc)}, ensure_ascii=False))
            return 2
        print(
            json.dumps(
                {"ok": not errors, "error_count": len(errors), "errors": errors},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0 if not errors else 1

    if args.form:
        if not args.form_name or not args.document:
            parser.error("--form requires --form-name and --document")
        try:
            form = _load_artifact(args.form)
            _, errors = _parse_form_body(
                form,
                args.document.read_text(encoding="utf-8"),
                args.form_name,
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(json.dumps({"ok": False, "parse_error": str(exc)}, ensure_ascii=False))
            return 2
        print(json.dumps({"ok": not errors, "error_count": len(errors), "errors": errors}, ensure_ascii=False))
        return 0 if not errors else 1

    return _run_suite()


if __name__ == "__main__":
    raise SystemExit(_main())
