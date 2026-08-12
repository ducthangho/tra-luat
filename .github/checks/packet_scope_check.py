# -*- coding: utf-8 -*-
"""Fail-closed, offline enforcement for a Packet's file and Git-ref scope.

The check intentionally uses only the Python standard library.  JSON is the
preferred machine format; a deliberately small YAML subset is accepted so a
Packet's fenced Issue specification can be checked without PyYAML.

Usage:
    python .github/checks/packet_scope_check.py \
        --spec packet.json --changes changes.json [--json]

``changes.json`` has the shape ``{"files": [...], "refs": [...]}``.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath


REQUIRED_SPEC_FIELDS = {
    "packet_id",
    "revision",
    "spec_hash",
    "objective",
    "write_set",
    "ref_set",
    "depends_on",
    "executor",
    "environment",
    "risk",
    "acceptance_criteria",
}


class ScopeError(ValueError):
    """A stable, user-facing validation failure."""

    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code
        self.detail = detail


def _scalar(text: str):
    text = text.strip()
    if text == "[]":
        return []
    if text == "{}":
        return {}
    if text in {"null", "~"}:
        return None
    if text in {"true", "false"}:
        return text == "true"
    if text.startswith("["):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            inner = text[1:-1].strip()
            if not inner:
                return []
            return [_scalar(part) for part in inner.split(",")]
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        if text[0] == '"':
            return json.loads(text)
        return text[1:-1].replace("''", "'")
    try:
        return int(text)
    except ValueError:
        return text


def _parse_yaml_subset(raw: str):
    """Parse the Packet subset: top-level scalars and lists of scalars/maps.

    Unsupported nesting, tabs, anchors, aliases, tags and duplicate keys are
    rejected instead of guessed.  That keeps malformed YAML red rather than
    silently shrinking a scope.
    """
    if "\t" in raw or any(token in raw for token in ("&", "*", "!!")):
        raise ScopeError("SPEC_PARSE_ERROR", "unsupported YAML construct")
    out = {}
    active_key = None
    active_item = None
    for number, original in enumerate(raw.splitlines(), 1):
        line = original.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()
        if indent == 0:
            if ":" not in text:
                raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: expected key")
            key, value = text.split(":", 1)
            key = key.strip()
            if not key or key in out:
                raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: duplicate/empty key")
            active_item = None
            if value.strip():
                out[key] = _scalar(value)
                active_key = None
            else:
                out[key] = []
                active_key = key
            continue
        if active_key is None or not isinstance(out[active_key], list):
            raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: unexpected indentation")
        if text.startswith("- "):
            value = text[2:].strip()
            if not value:
                raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: empty list item")
            if ":" in value:
                key, item_value = value.split(":", 1)
                active_item = {key.strip(): _scalar(item_value)}
                out[active_key].append(active_item)
            else:
                active_item = None
                out[active_key].append(_scalar(value))
        elif active_item is not None and ":" in text:
            key, value = text.split(":", 1)
            key = key.strip()
            if key in active_item:
                raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: duplicate item key")
            active_item[key] = _scalar(value)
        else:
            raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: unsupported nesting")
    return out


def load_spec(path: Path):
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise ScopeError("SPEC_READ_ERROR", str(exc)) from exc
    try:
        value = json.loads(raw) if raw.lstrip().startswith("{") else _parse_yaml_subset(raw)
    except json.JSONDecodeError as exc:
        raise ScopeError("SPEC_PARSE_ERROR", str(exc)) from exc
    if not isinstance(value, dict):
        raise ScopeError("SPEC_PARSE_ERROR", "spec must be an object")
    missing = sorted(REQUIRED_SPEC_FIELDS - set(value))
    if missing:
        raise ScopeError("SPEC_MISSING_FIELD", ",".join(missing))
    scalar_contract = {
        "packet_id": str,
        "revision": int,
        "spec_hash": str,
        "objective": str,
        "executor": str,
        "environment": str,
        "risk": str,
    }
    for key, expected in scalar_contract.items():
        if not isinstance(value[key], expected) or (expected is int and isinstance(value[key], bool)):
            raise ScopeError("SPEC_FIELD_TYPE", key)
    if not re.fullmatch(r"wp[0-9]+", value["packet_id"]):
        raise ScopeError("SPEC_FIELD_VALUE", "packet_id")
    if value["revision"] < 1 or not re.fullmatch(r"[0-9a-f]{64}", value["spec_hash"]):
        raise ScopeError("SPEC_FIELD_VALUE", "revision/spec_hash")
    if value["executor"] not in {"claude", "codex"} or value["environment"] not in {"cloud", "local"}:
        raise ScopeError("SPEC_FIELD_VALUE", "executor/environment")
    if value["risk"] not in {"normal", "sensitive"}:
        raise ScopeError("SPEC_FIELD_VALUE", "risk")
    if not isinstance(value["depends_on"], list) or not isinstance(value["acceptance_criteria"], list):
        raise ScopeError("SPEC_FIELD_TYPE", "depends_on/acceptance_criteria")
    return value


def _normal_file_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ScopeError("INVALID_FILE_PATH", repr(value))
    value = unicodedata.normalize("NFC", value.replace("\\", "/"))
    raw_parts = value.split("/")
    pure = PurePosixPath(value)
    if (pure.is_absolute() or value.startswith("/") or re.match(r"^[A-Za-z]:/", value)
            or any(part in {"", ".", ".."} for part in raw_parts)):
        raise ScopeError("INVALID_FILE_PATH", value)
    return str(pure).casefold()


def _normal_ref(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ScopeError("INVALID_REF", repr(value))
    value = unicodedata.normalize("NFC", value.replace("\\", "/"))
    if not value.startswith("refs/") or value.endswith("/") or "//" in value:
        raise ScopeError("INVALID_REF", value)
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ScopeError("INVALID_REF", value)
    return value


def _rules(raw_rules: object, value_key: str, normalizer):
    if not isinstance(raw_rules, list):
        raise ScopeError("INVALID_SCOPE", f"{value_key} scope is not a list")
    result = []
    for index, rule in enumerate(raw_rules):
        if not isinstance(rule, dict) or set(rule) != {"type", value_key}:
            raise ScopeError("INVALID_SCOPE", f"{value_key}[{index}] shape")
        kind = rule["type"]
        if kind not in {"exact", "prefix"}:
            raise ScopeError("INVALID_SCOPE", f"{value_key}[{index}] type")
        result.append((kind, normalizer(rule[value_key])))
    return result


def _covered(value: str, rules) -> bool:
    for kind, declared in rules:
        if kind == "exact" and value == declared:
            return True
        if kind == "prefix" and (value == declared or value.startswith(declared + "/")):
            return True
    return False


def check(spec, changes):
    if not isinstance(changes, dict) or set(changes) != {"files", "refs"}:
        raise ScopeError("CHANGES_PARSE_ERROR", "changes must contain exactly files and refs")
    if not isinstance(changes["files"], list) or not isinstance(changes["refs"], list):
        raise ScopeError("CHANGES_PARSE_ERROR", "files and refs must be arrays")
    file_rules = _rules(spec["write_set"], "path", _normal_file_path)
    ref_rules = _rules(spec["ref_set"], "ref", _normal_ref)
    files = [_normal_file_path(item) for item in changes["files"]]
    refs = [_normal_ref(item) for item in changes["refs"]]
    outside_files = [value for value in files if not _covered(value, file_rules)]
    outside_refs = [value for value in refs if not _covered(value, ref_rules)]
    if outside_files or outside_refs:
        raise ScopeError(
            "OUT_OF_SCOPE",
            json.dumps({"files": outside_files, "refs": outside_refs}, ensure_ascii=False, sort_keys=True),
        )
    return {"files_checked": len(files), "refs_checked": len(refs)}


def _emit(payload, as_json):
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print("packet_scope_check: ok=%s error=%s" % (payload["ok"], payload.get("error")))
    return 0 if payload["ok"] else 1


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--changes", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = {"schema": "packet_scope_check.v1", "ok": False}
    try:
        spec = load_spec(args.spec)
        try:
            changes = json.loads(args.changes.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ScopeError("CHANGES_PARSE_ERROR", str(exc)) from exc
        payload.update(check(spec, changes))
        payload["ok"] = True
    except ScopeError as exc:
        payload.update(error=exc.code, detail=exc.detail)
    return _emit(payload, args.json)


if __name__ == "__main__":
    sys.exit(main())
