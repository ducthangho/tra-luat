#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate and canonically hash the repository change-impact policy.

This program intentionally uses only the Python standard library.  It is a
fail-closed CI boundary: malformed policy, unsafe paths, and expired rules all
produce a non-zero exit status and a deterministic JSON error envelope.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_POLICY = HERE.parent / "coordination" / "change-impact.v1.json"
DEFAULT_SCHEMA = HERE.parent / "coordination" / "schemas" / "change-impact.v1.schema.json"
RULE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DRIVE_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:/")
GLOB_CHARS_RE = re.compile(r"[*?\[\]{}]")
PATH_TYPES = frozenset({"exact", "prefix"})
SCHEMA_KEYWORDS = frozenset(
    {
        "$defs",
        "$id",
        "$ref",
        "$schema",
        "additionalProperties",
        "const",
        "description",
        "enum",
        "format",
        "items",
        "minItems",
        "minLength",
        "oneOf",
        "pattern",
        "properties",
        "required",
        "title",
        "type",
    }
)


class SchemaDefinitionError(ValueError):
    """Raised when the checked-in schema uses an invalid local contract."""


def _nfc(value: Any) -> Any:
    if isinstance(value, dict):
        return {unicodedata.normalize("NFC", str(key)): _nfc(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_nfc(item) for item in value]
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    return value


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _parse_time(value: str) -> datetime:
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise SchemaDefinitionError("unsupported type: " + str(expected))


def _schema_ref(root: dict[str, Any], reference: str) -> dict[str, Any]:
    if not isinstance(reference, str) or not reference.startswith("#/"):
        raise SchemaDefinitionError("only local JSON pointers are supported")
    current: Any = root
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or part not in current:
            raise SchemaDefinitionError("unresolved ref: " + reference)
        current = current[part]
    if not isinstance(current, dict):
        raise SchemaDefinitionError("ref is not an object: " + reference)
    return current


def _assert_schema_keywords(node: Any, location: str = "schema") -> None:
    """Fail closed when v1's stdlib evaluator cannot enforce a schema keyword."""
    if not isinstance(node, dict):
        raise SchemaDefinitionError("schema node is not an object at " + location)
    unknown = sorted(set(node) - SCHEMA_KEYWORDS)
    if unknown:
        raise SchemaDefinitionError("unsupported keywords at %s: %s" % (location, ",".join(unknown)))
    schema_format = node.get("format")
    if schema_format is not None and schema_format != "date-time":
        raise SchemaDefinitionError("unsupported format at %s: %s" % (location, schema_format))
    additional = node.get("additionalProperties")
    if additional is not None and not isinstance(additional, bool):
        raise SchemaDefinitionError("additionalProperties schema unsupported at " + location)
    for keyword in ("$defs", "properties"):
        children = node.get(keyword, {})
        if not isinstance(children, dict):
            raise SchemaDefinitionError(keyword + " must be an object at " + location)
        for name in sorted(children):
            _assert_schema_keywords(children[name], "%s.%s.%s" % (location, keyword, name))
    if "items" in node:
        _assert_schema_keywords(node["items"], location + ".items")
    alternatives = node.get("oneOf", [])
    if not isinstance(alternatives, list):
        raise SchemaDefinitionError("oneOf must be an array at " + location)
    for index, alternative in enumerate(alternatives):
        _assert_schema_keywords(alternative, "%s.oneOf[%d]" % (location, index))


def _schema_findings(
    value: Any,
    node: Any,
    root: dict[str, Any],
    location: str = "policy",
) -> list[tuple[str, str]]:
    """Validate the JSON-Schema subset used by change-impact.v1."""
    if not isinstance(node, dict):
        raise SchemaDefinitionError("schema node is not an object at " + location)
    if "$ref" in node:
        return _schema_findings(value, _schema_ref(root, node["$ref"]), root, location)

    alternatives = node.get("oneOf")
    if alternatives is not None:
        if not isinstance(alternatives, list) or not alternatives:
            raise SchemaDefinitionError("oneOf must be a non-empty array at " + location)
        matches = [not _schema_findings(value, item, root, location) for item in alternatives]
        return [] if sum(matches) == 1 else [(location, "oneOf matched %d branches" % sum(matches))]

    expected = node.get("type")
    if expected is not None:
        expected_types = expected if isinstance(expected, list) else [expected]
        if not expected_types or not all(isinstance(item, str) for item in expected_types):
            raise SchemaDefinitionError("type must be a string or non-empty string array")
        if not any(_json_type_matches(value, item) for item in expected_types):
            return [(location, "type must be " + "|".join(expected_types))]

    if "const" in node and (type(value) is not type(node["const"]) or value != node["const"]):
        return [(location, "const mismatch")]
    if "enum" in node:
        choices = node["enum"]
        if not isinstance(choices, list):
            raise SchemaDefinitionError("enum must be an array at " + location)
        if not any(type(value) is type(choice) and value == choice for choice in choices):
            return [(location, "value is not in enum")]

    findings: list[tuple[str, str]] = []
    if isinstance(value, dict):
        properties = node.get("properties", {})
        required = node.get("required", [])
        if not isinstance(properties, dict) or not isinstance(required, list):
            raise SchemaDefinitionError("object keywords malformed at " + location)
        for name in required:
            if not isinstance(name, str):
                raise SchemaDefinitionError("required entry is not a string at " + location)
            if name not in value:
                findings.append((location + "." + name, "required property missing"))
        if node.get("additionalProperties") is False:
            for name in sorted(set(value) - set(properties)):
                findings.append((location + "." + str(name), "additional property forbidden"))
        for name in sorted(set(value) & set(properties)):
            findings.extend(
                _schema_findings(value[name], properties[name], root, location + "." + str(name))
            )
    elif isinstance(value, list):
        minimum = node.get("minItems")
        if minimum is not None and (not isinstance(minimum, int) or minimum < 0):
            raise SchemaDefinitionError("minItems malformed at " + location)
        if isinstance(minimum, int) and len(value) < minimum:
            findings.append((location, "minItems=%d" % minimum))
        if "items" in node:
            for index, item in enumerate(value):
                findings.extend(
                    _schema_findings(item, node["items"], root, "%s[%d]" % (location, index))
                )
    elif isinstance(value, str):
        minimum = node.get("minLength")
        if minimum is not None and (not isinstance(minimum, int) or minimum < 0):
            raise SchemaDefinitionError("minLength malformed at " + location)
        if isinstance(minimum, int) and len(value) < minimum:
            findings.append((location, "minLength=%d" % minimum))
        pattern = node.get("pattern")
        if pattern is not None:
            if not isinstance(pattern, str):
                raise SchemaDefinitionError("pattern is not a string at " + location)
            try:
                matched = re.search(pattern, value) is not None
            except re.error as exc:
                raise SchemaDefinitionError("invalid pattern at " + location) from exc
            if not matched:
                findings.append((location, "pattern mismatch"))
        if node.get("format") == "date-time":
            try:
                _parse_time(value)
            except (TypeError, ValueError):
                findings.append((location, "invalid date-time"))
    return findings


def _repo_root() -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(HERE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode == 0:
        text = proc.stdout.decode("utf-8", "replace").strip()
        if text:
            return Path(text)
    return HERE.parent.parent


class Validation:
    def __init__(self, root: Path, now: datetime):
        self.root = root.resolve(strict=True)
        self.now = now
        self.errors: list[dict[str, str]] = []
        self.path_count = 0
        self.path_identities: dict[str, tuple[str, str, str]] = {}

    def error(self, code: str, location: str, detail: str = "") -> None:
        item = {"code": code, "location": location}
        if detail:
            item["detail"] = unicodedata.normalize("NFC", str(detail))
        self.errors.append(item)

    def _inside_root(self, candidate: Path) -> bool:
        try:
            return os.path.commonpath((str(self.root), str(candidate))) == str(self.root)
        except (OSError, ValueError):
            return False

    def path_spec(self, value: Any, location: str) -> dict[str, str] | None:
        if not isinstance(value, dict):
            self.error("PATH_SPEC_INVALID", location, "expected object")
            return None
        extra = sorted(set(value) - {"type", "path"})
        if extra:
            self.error("PATH_SPEC_INVALID", location, "unknown fields: " + ",".join(extra))
        kind = value.get("type")
        if kind not in PATH_TYPES:
            self.error("PATH_TYPE_INVALID", location + ".type", str(kind))
        raw = value.get("path")
        if not isinstance(raw, str) or not raw:
            self.error("PATH_EMPTY", location + ".path")
            return None

        source_slash = raw.replace("\\", "/")
        slash = unicodedata.normalize("NFC", source_slash)
        if slash.startswith("/") or slash.startswith("//") or DRIVE_ABSOLUTE_RE.match(slash):
            self.error("PATH_ABSOLUTE", location + ".path", slash)
            return None
        parts = slash.split("/")
        if any(part in {".", ".."} for part in parts):
            self.error("PATH_SEGMENT_FORBIDDEN", location + ".path", slash)
            return None
        if any(not part for part in parts):
            self.error("PATH_EMPTY_SEGMENT", location + ".path", slash)
            return None
        if GLOB_CHARS_RE.search(slash):
            self.error("PATH_GLOB_FORBIDDEN", location + ".path", slash)
            return None

        current = self.root
        try:
            for part in parts:
                candidate = current / part
                if candidate.exists() or candidate.is_symlink():
                    current = candidate.resolve(strict=True)
                else:
                    current = candidate
            resolved = current.resolve(strict=False)
        except (OSError, RuntimeError) as exc:
            self.error("PATH_RESOLVE_FAILED", location + ".path", type(exc).__name__)
            return None
        if not self._inside_root(resolved):
            self.error("PATH_ESCAPES_ROOT", location + ".path", slash)
            return None

        identity = slash.casefold()
        previous = self.path_identities.get(identity)
        if previous is not None:
            previous_path, previous_source, previous_location = previous
            if slash != previous_path or source_slash != previous_source:
                self.error("PATH_COLLISION", location, "collides with " + previous_location)
        else:
            self.path_identities[identity] = (slash, source_slash, location)

        self.path_count += 1
        return {"type": str(kind), "path": slash}

    def path_specs(self, value: Any, location: str, *, allow_object: bool = False) -> list[dict[str, str]]:
        values = [value] if allow_object and isinstance(value, dict) else value
        if not isinstance(values, list) or not values:
            self.error("PATH_LIST_REQUIRED", location)
            return []
        result = []
        for index, item in enumerate(values):
            item_location = "%s[%d]" % (location, index)
            normalized = self.path_spec(item, item_location)
            if normalized is None:
                continue
            result.append(normalized)
        return result

    def runtime_python_inventory(self, rules: list[dict[str, Any]]) -> None:
        runtime_rule = next(
            (rule for rule in rules if rule.get("rule_id") == "runtime-py-added-moves-golden"),
            None,
        )
        if runtime_rule is None:
            return
        scripts = self.root / "scripts"
        actual = {
            "scripts/" + path.name
            for path in scripts.glob("*.py")
            if path.is_file() or path.is_symlink()
        } if scripts.is_dir() else set()
        declared = {
            item["path"]
            for item in runtime_rule.get("trigger", [])
            if item.get("type") == "exact"
            and item.get("path", "").startswith("scripts/")
            and "/" not in item.get("path", "")[len("scripts/"):]
            and item.get("path", "").endswith(".py")
        }
        missing = sorted(actual - declared)
        stale = sorted(declared - actual)
        if missing or stale:
            detail = "missing=%s; stale=%s" % (",".join(missing) or "-", ",".join(stale) or "-")
            self.error("RUNTIME_PY_TRIGGER_STALE", "candidate_rules.runtime-py-added-moves-golden.trigger", detail)

    def string_list(self, value: Any, location: str, *, required: bool = False) -> list[str]:
        if not isinstance(value, list):
            self.error("LIST_REQUIRED", location)
            return []
        result = []
        for index, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                self.error("STRING_REQUIRED", "%s[%d]" % (location, index))
            else:
                result.append(unicodedata.normalize("NFC", item))
        if required and not result:
            self.error("EVIDENCE_REQUIRED", location)
        return result

    def rule(self, value: Any, index: int) -> dict[str, Any] | None:
        location = "candidate_rules[%d]" % index
        if not isinstance(value, dict):
            self.error("RULE_INVALID", location, "expected object")
            return None
        expected = {
            "rule_id",
            "trigger",
            "write_closure",
            "required_checks",
            "land_obligations",
            "evidence",
            "owner",
            "expires_at",
        }
        missing = sorted(expected - set(value))
        extra = sorted(set(value) - expected)
        if missing:
            self.error("RULE_FIELD_REQUIRED", location, "missing: " + ",".join(missing))
        if extra:
            self.error("RULE_FIELD_UNKNOWN", location, "unknown: " + ",".join(extra))

        rule_id = value.get("rule_id")
        if not isinstance(rule_id, str) or not RULE_ID_RE.fullmatch(rule_id):
            self.error("RULE_ID_INVALID", location + ".rule_id", str(rule_id))
            rule_id = ""
        owner = value.get("owner")
        if not isinstance(owner, str) or not owner.strip():
            self.error("OWNER_REQUIRED", location + ".owner")
            owner = ""

        trigger = self.path_specs(value.get("trigger"), location + ".trigger", allow_object=True)
        closure = self.path_specs(value.get("write_closure"), location + ".write_closure")
        checks = self.string_list(value.get("required_checks"), location + ".required_checks")
        obligations = self.string_list(value.get("land_obligations"), location + ".land_obligations")
        evidence = self.string_list(value.get("evidence"), location + ".evidence", required=True)

        expires_at = value.get("expires_at")
        if expires_at is not None:
            if not isinstance(expires_at, str):
                self.error("EXPIRES_AT_INVALID", location + ".expires_at", str(expires_at))
            else:
                try:
                    expiry = _parse_time(expires_at)
                    if expiry <= self.now:
                        self.error("RULE_EXPIRED", location + ".expires_at", expires_at)
                except (TypeError, ValueError):
                    self.error("EXPIRES_AT_INVALID", location + ".expires_at", expires_at)

        return {
            "rule_id": unicodedata.normalize("NFC", rule_id),
            "trigger": trigger,
            "write_closure": closure,
            "required_checks": checks,
            "land_obligations": obligations,
            "evidence": evidence,
            "owner": unicodedata.normalize("NFC", owner),
            "expires_at": unicodedata.normalize("NFC", expires_at) if isinstance(expires_at, str) else None,
        }


def _load_json(path: Path, code: str) -> tuple[Any, dict[str, str] | None]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            return json.load(stream), None
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, {"code": code, "location": path.name, "detail": type(exc).__name__}


def _failure_payload(errors: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "ok": False,
        "change_policy_sha": None,
        "rule_count": 0,
        "path_spec_count": 0,
        "errors": errors,
    }


def validate(policy: Any, schema: Any, root: Path, now: datetime) -> dict[str, Any]:
    check = Validation(root, now)
    if not isinstance(schema, dict):
        check.error("SCHEMA_INVALID", "schema", "expected object")
    else:
        try:
            _assert_schema_keywords(schema)
        except SchemaDefinitionError as exc:
            check.error("SCHEMA_INVALID", "schema", str(exc))
        declared = (((schema.get("properties") or {}).get("schema_version") or {}).get("const"))
        if declared != 1:
            check.error("SCHEMA_INVALID", "schema.properties.schema_version.const", str(declared))
        try:
            for location, detail in _schema_findings(policy, schema, schema):
                check.error("SCHEMA_VIOLATION", location, detail)
        except SchemaDefinitionError as exc:
            check.error("SCHEMA_INVALID", "schema", str(exc))

    if not isinstance(policy, dict):
        check.error("POLICY_INVALID", "policy", "expected object")
        policy = {}
    schema_version = policy.get("schema_version")
    if schema_version != 1:
        check.error("SCHEMA_VERSION_UNSUPPORTED", "schema_version", str(schema_version))
    policy_id = policy.get("policy_id")
    if not isinstance(policy_id, str) or not policy_id.strip():
        check.error("POLICY_ID_REQUIRED", "policy_id")
        policy_id = ""

    allowed_top = {
        "schema_version",
        "policy_id",
        "candidate_rules",
        "unproven_candidates",
        "land_obligations",
    }
    extra_top = sorted(set(policy) - allowed_top)
    if extra_top:
        check.error("POLICY_FIELD_UNKNOWN", "policy", "unknown: " + ",".join(extra_top))

    raw_rules = policy.get("candidate_rules")
    if not isinstance(raw_rules, list):
        check.error("RULE_LIST_REQUIRED", "candidate_rules")
        raw_rules = []
    rules = []
    seen: dict[str, int] = {}
    for index, raw_rule in enumerate(raw_rules):
        normalized = check.rule(raw_rule, index)
        if normalized is None:
            continue
        rule_id = normalized["rule_id"]
        if rule_id in seen:
            check.error(
                "RULE_ID_DUPLICATE",
                "candidate_rules[%d].rule_id" % index,
                "first at candidate_rules[%d]" % seen[rule_id],
            )
        elif rule_id:
            seen[rule_id] = index
        rules.append(normalized)
    check.runtime_python_inventory(rules)

    unproven = policy.get("unproven_candidates")
    if not isinstance(unproven, list):
        check.error("LIST_REQUIRED", "unproven_candidates")
        unproven = []
    obligations = policy.get("land_obligations")
    if not isinstance(obligations, list):
        check.error("LIST_REQUIRED", "land_obligations")
        obligations = []

    canonical = {
        "schema_version": schema_version,
        "policy_id": unicodedata.normalize("NFC", policy_id),
        "candidate_rules": rules,
        "unproven_candidates": _nfc(unproven),
        "land_obligations": _nfc(obligations),
    }
    errors = sorted(
        check.errors,
        key=lambda item: (item.get("code", ""), item.get("location", ""), item.get("detail", "")),
    )
    digest = hashlib.sha256(_canonical_bytes(canonical)).hexdigest() if not errors else None
    return {
        "schema_version": 1,
        "ok": not errors,
        "change_policy_sha": digest,
        "rule_count": len(rules),
        "path_spec_count": check.path_count,
        "errors": errors,
    }


def _emit(payload: dict[str, Any], as_json: bool) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    else:
        status = "ok" if payload.get("ok") else "failed"
        sys.stdout.write(
            "change-impact: %s rules=%s sha=%s\n"
            % (status, payload.get("rule_count"), payload.get("change_policy_sha") or "-")
        )
        for error in payload.get("errors") or []:
            sys.stdout.write(
                "  %s %s%s\n"
                % (
                    error.get("code"),
                    error.get("location"),
                    ": " + error.get("detail") if error.get("detail") else "",
                )
            )
    return 0 if payload.get("ok") else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate change-impact.v1 policy.")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--root", type=Path, default=_repo_root())
    parser.add_argument("--now", help="UTC timestamp override for deterministic expiry tests")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        now = _parse_time(args.now) if args.now else datetime.now(timezone.utc)
    except (TypeError, ValueError):
        return _emit(
            _failure_payload([{"code": "NOW_INVALID", "location": "--now"}]),
            args.json,
        )

    policy, policy_error = _load_json(args.policy, "POLICY_READ_FAILED")
    schema, schema_error = _load_json(args.schema, "SCHEMA_READ_FAILED")
    if policy_error or schema_error:
        payload = _failure_payload(
            sorted(
                [item for item in (policy_error, schema_error) if item],
                key=lambda item: (item["code"], item["location"]),
            )
        )
        return _emit(payload, args.json)
    try:
        payload = validate(policy, schema, args.root, now)
    except (OSError, RuntimeError) as exc:
        payload = _failure_payload(
            [{"code": "ROOT_INVALID", "location": "--root", "detail": type(exc).__name__}]
        )
    return _emit(payload, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
