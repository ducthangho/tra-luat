# -*- coding: utf-8 -*-
"""Offline validator for canonical, versioned state-event hashes.

The registry is the single source for each event type's ordered field set and
types.  This check never reads GitHub, the network, environment credentials or
secrets.  Its inputs are explicit local JSON files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
DEFAULT_REGISTRY = HERE.parent.parent / "coordination" / "checkpoint-schema.v1.json"
DEFAULT_SCHEMA = HERE.parent.parent / "coordination" / "schemas" / "checkpoint-schema.v1.schema.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
GIT_OID = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
JSON_TYPES = {"null", "boolean", "integer", "number", "string", "array", "object"}


class StateHashError(ValueError):
    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code
        self.detail = detail


def _read_json(path: Path, code: str):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StateHashError(code, f"{path}: {exc}") from exc


def _is_json_type(value, kind):
    if kind == "null":
        return value is None
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "string":
        return isinstance(value, str)
    if kind == "array":
        return isinstance(value, list)
    if kind == "object":
        return isinstance(value, dict)
    return False


def _schema_check(value, schema, at="$"):
    """Validate the deterministic JSON-Schema subset used by the registry schema."""
    if not isinstance(schema, dict):
        raise StateHashError("REGISTRY_SCHEMA_INVALID", f"{at}: schema is not an object")
    if "const" in schema and value != schema["const"]:
        raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: const")
    if "enum" in schema and value not in schema["enum"]:
        raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: enum")
    declared = schema.get("type")
    if declared is not None:
        kinds = [declared] if isinstance(declared, str) else declared
        if not isinstance(kinds, list) or not kinds or any(k not in JSON_TYPES for k in kinds):
            raise StateHashError("REGISTRY_SCHEMA_INVALID", f"{at}: invalid type declaration")
        if not any(_is_json_type(value, kind) for kind in kinds):
            raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: type")
    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: minLength")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: minItems")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(v, sort_keys=True, separators=(",", ":")) for v in value]
            if len(encoded) != len(set(encoded)):
                raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: uniqueItems")
        if "items" in schema:
            for index, item in enumerate(value):
                _schema_check(item, schema["items"], f"{at}[{index}]")
    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in value]
        if missing:
            raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: missing {missing}")
        if len(value) < schema.get("minProperties", 0):
            raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: minProperties")
        properties = schema.get("properties", {})
        extra_rule = schema.get("additionalProperties", True)
        for key, child in value.items():
            if key in properties:
                _schema_check(child, properties[key], f"{at}.{key}")
            elif extra_rule is False:
                raise StateHashError("REGISTRY_SCHEMA_MISMATCH", f"{at}: extra {key}")
            elif isinstance(extra_rule, dict):
                _schema_check(child, extra_rule, f"{at}.{key}")


def _descriptor(desc, at):
    if not isinstance(desc, dict):
        raise StateHashError("REGISTRY_INVALID", f"{at}: descriptor is not an object")
    allowed = {"name", "types", "format", "enum"}
    if set(desc) - allowed or not {"name", "types"}.issubset(desc):
        raise StateHashError("REGISTRY_INVALID", f"{at}: descriptor shape")
    if not isinstance(desc["name"], str) or not desc["name"]:
        raise StateHashError("REGISTRY_INVALID", f"{at}: name")
    types = desc["types"]
    if (not isinstance(types, list) or not types or len(types) != len(set(types))
            or any(kind not in JSON_TYPES for kind in types)):
        raise StateHashError("REGISTRY_INVALID", f"{at}: types")
    if desc.get("format") not in {None, "sha256", "git_oid"}:
        raise StateHashError("REGISTRY_INVALID", f"{at}: format")
    if "enum" in desc and (not isinstance(desc["enum"], list) or not desc["enum"]):
        raise StateHashError("REGISTRY_INVALID", f"{at}: enum")
    return desc


def load_registry(registry_path: Path, schema_path: Path):
    registry = _read_json(registry_path, "REGISTRY_READ_ERROR")
    schema = _read_json(schema_path, "REGISTRY_SCHEMA_READ_ERROR")
    _schema_check(registry, schema)
    if registry.get("field_order") != "lexicographic_code_point":
        raise StateHashError("REGISTRY_INVALID", "field_order")
    common = registry.get("common_identity_basis")
    event_types = registry.get("event_types")
    if not isinstance(common, dict) or not isinstance(common.get("fields"), list):
        raise StateHashError("REGISTRY_INVALID", "common_identity_basis.fields")
    if not isinstance(event_types, dict) or not event_types:
        raise StateHashError("REGISTRY_INVALID", "event_types")
    common_fields = [_descriptor(item, f"common[{index}]") for index, item in enumerate(common["fields"])]
    common_names = [item["name"] for item in common_fields]
    if len(common_names) != len(set(common_names)):
        raise StateHashError("REGISTRY_INVALID", "duplicate common field")
    compiled = {}
    for event_type, declaration in event_types.items():
        if not isinstance(event_type, str) or not isinstance(declaration, dict):
            raise StateHashError("REGISTRY_INVALID", "event type shape")
        extra = declaration.get("additional_fields")
        if not isinstance(extra, list):
            raise StateHashError("REGISTRY_INVALID", f"{event_type}: additional_fields")
        descriptors = common_fields + [
            _descriptor(item, f"{event_type}[{index}]") for index, item in enumerate(extra)
        ]
        names = [item["name"] for item in descriptors]
        if len(names) != len(set(names)):
            raise StateHashError("REGISTRY_INVALID", f"{event_type}: duplicate field")
        event_field = next((item for item in extra if item["name"] == "event_type"), None)
        if event_field is None or event_field.get("enum") != [event_type]:
            raise StateHashError("REGISTRY_INVALID", f"{event_type}: event_type enum")
        compiled[event_type] = sorted(descriptors, key=lambda item: item["name"])
    return registry, compiled


def canonical_bytes(basis):
    # sort_keys is recursive; arrays retain their declared order.  encode adds
    # neither BOM nor trailing LF.
    return json.dumps(
        basis, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_hash(basis):
    return hashlib.sha256(canonical_bytes(basis)).hexdigest()


def _check_value(value, descriptor):
    if not any(_is_json_type(value, kind) for kind in descriptor["types"]):
        return False
    if "enum" in descriptor and value not in descriptor["enum"]:
        return False
    fmt = descriptor.get("format")
    if value is not None and fmt == "sha256" and not HEX64.fullmatch(value):
        return False
    if value is not None and fmt == "git_oid" and not GIT_OID.fullmatch(value):
        return False
    return True


def validate_event(event, registry, compiled, head_hash=None):
    if not isinstance(event, dict):
        raise StateHashError("EVENT_PARSE_ERROR", "event must be an object")
    required = {
        "event_type", "checkpoint_schema_id", "checkpoint_schema_version",
        "state_hash_fields", "basis_object", "state_hash",
    }
    missing_top = sorted(required - set(event))
    if missing_top:
        raise StateHashError("EVENT_MISSING_FIELD", ",".join(missing_top))
    if (event["checkpoint_schema_id"] != registry["checkpoint_schema_id"]
            or event["checkpoint_schema_version"] != registry["checkpoint_schema_version"]):
        raise StateHashError("UNKNOWN_CHECKPOINT_SCHEMA", "schema id/version")
    event_type = event["event_type"]
    if event_type not in compiled:
        raise StateHashError("UNKNOWN_EVENT_TYPE", repr(event_type))
    descriptors = compiled[event_type]
    expected_names = [item["name"] for item in descriptors]
    if event["state_hash_fields"] != expected_names:
        raise StateHashError("STATE_HASH_FIELDS_MISMATCH", "ordered field list differs from registry")
    basis = event["basis_object"]
    if not isinstance(basis, dict):
        raise StateHashError("BASIS_NOT_OBJECT", "basis_object")
    missing = sorted(set(expected_names) - set(basis))
    extra = sorted(set(basis) - set(expected_names))
    if missing:
        raise StateHashError("CANONICAL_FIELD_MISSING", ",".join(missing))
    if extra:
        raise StateHashError("CANONICAL_FIELD_EXTRA", ",".join(extra))
    for descriptor in descriptors:
        if not _check_value(basis[descriptor["name"]], descriptor):
            raise StateHashError("CANONICAL_FIELD_TYPE", descriptor["name"])
    if basis["event_type"] != event_type:
        raise StateHashError("EVENT_TYPE_MISMATCH", event_type)
    if not isinstance(event["state_hash"], str) or not HEX64.fullmatch(event["state_hash"]):
        raise StateHashError("STATE_HASH_INVALID", repr(event["state_hash"]))
    computed = canonical_hash(basis)
    if computed != event["state_hash"]:
        raise StateHashError("STATE_HASH_MISMATCH", f"expected {computed}")
    if head_hash is not None and basis["prev_event_hash"] != head_hash:
        raise StateHashError("PREV_EVENT_HASH_MISMATCH", f"expected {head_hash}")
    return computed


def _head_hash(path: Path):
    head = _read_json(path, "HEAD_READ_ERROR")
    if not isinstance(head, dict) or not isinstance(head.get("state_hash"), str):
        raise StateHashError("HEAD_INVALID", "raw head must carry state_hash")
    if not HEX64.fullmatch(head["state_hash"]):
        raise StateHashError("HEAD_INVALID", "state_hash")
    return head["state_hash"]


def _emit(payload, as_json, rc=None):
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print("state_hash_check: ok=%s action=%s error=%s" % (
            payload["ok"], payload.get("action"), payload.get("error")
        ))
    if rc is not None:
        return rc
    return 0 if payload["ok"] else 1


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--head", type=Path, help="raw journal head JSON, never a projection")
    parser.add_argument("--sibling", type=Path, help="already-appended sibling event JSON")
    parser.add_argument("--validate-registry", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = {"schema": "state_hash_check.v1", "ok": False}
    try:
        registry, compiled = load_registry(args.registry, args.schema)
        payload["checkpoint_schema_id"] = registry["checkpoint_schema_id"]
        payload["checkpoint_schema_version"] = registry["checkpoint_schema_version"]
        payload["event_type_count"] = len(compiled)
        if args.validate_registry and args.event is None:
            payload.update(ok=True, action="registry_valid")
            return _emit(payload, args.json)
        if args.event is None:
            raise StateHashError("EVENT_REQUIRED", "--event")
        event = _read_json(args.event, "EVENT_READ_ERROR")
        head_hash = _head_hash(args.head) if args.head else None
        computed = validate_event(event, registry, compiled, head_hash)
        payload.update(state_hash=computed, event_type=event["event_type"], action="append")
        if args.sibling:
            sibling = _read_json(args.sibling, "SIBLING_READ_ERROR")
            validate_event(sibling, registry, compiled, head_hash)
            same_predecessor = (
                sibling["basis_object"]["prev_event_hash"]
                == event["basis_object"]["prev_event_hash"]
            )
            if same_predecessor:
                same_schema = (
                    sibling["checkpoint_schema_id"] == event["checkpoint_schema_id"]
                    and sibling["checkpoint_schema_version"] == event["checkpoint_schema_version"]
                )
                same_basis = canonical_bytes(sibling["basis_object"]) == canonical_bytes(event["basis_object"])
                same_hash = sibling["state_hash"] == event["state_hash"]
                if same_schema and same_basis and same_hash:
                    payload["action"] = "idempotent"
                else:
                    raise StateHashError(
                        "SIBLING_CONFLICT",
                        "same predecessor with different schema, canonical basis, or hash",
                    )
        payload["ok"] = True
    except StateHashError as exc:
        payload.update(error=exc.code, detail=exc.detail)
        if exc.code == "SIBLING_CONFLICT":
            payload.update(action="pause", next_role="human")
            return _emit(payload, args.json, rc=2)
    return _emit(payload, args.json)


if __name__ == "__main__":
    sys.exit(main())
