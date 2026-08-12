# -*- coding: utf-8 -*-
"""Chốt offline fail-closed cho phạm vi tệp/ref — wp84 r4, verdict 5270183458."""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath


REQUIRED_SPEC_FIELDS = {
    "schema_version", "packet_id", "mission_issue", "revision", "spec_hash",
    "objective", "write_set", "ref_set", "depends_on", "executor",
    "environment", "risk", "acceptance_criteria",
}


class ScopeError(ValueError):
    """Lỗi dữ liệu Packet/repository có mã ổn định (rc=1)."""

    def __init__(self, code: str, detail: str):
        super().__init__(detail)
        self.code = code
        self.detail = detail


class OperatorError(ValueError):
    """Lỗi gọi lệnh ổn định (rc=64, tách khỏi lỗi dữ liệu)."""

    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise OperatorError(message)


def _configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="strict")


def _json_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ScopeError("SPEC_DUPLICATE_KEY", str(key))
        out[key] = value
    return out


def _split_flow(inner: str) -> list[str]:
    parts, start, depth, quote, backtick = [], 0, 0, None, False
    escaped = False
    for index, char in enumerate(inner):
        if quote:
            if quote == '"' and escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if backtick:
            if char == "`":
                backtick = False
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "`":
            backtick = True
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
            if depth < 0:
                raise ScopeError("SPEC_PARSE_ERROR", "unbalanced flow value")
        elif char == "," and depth == 0:
            parts.append(inner[start:index].strip())
            start = index + 1
    if quote or backtick or depth:
        raise ScopeError("SPEC_PARSE_ERROR", "unterminated flow value")
    tail = inner[start:].strip()
    if tail:
        parts.append(tail)
    elif inner.strip():
        raise ScopeError("SPEC_PARSE_ERROR", "empty flow item")
    return parts


def _split_mapping(text: str) -> tuple[str, str]:
    quote, backtick, depth, escaped = None, False, 0, False
    for index, char in enumerate(text):
        if quote:
            if quote == '"' and escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if backtick:
            if char == "`":
                backtick = False
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "`":
            backtick = True
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
        elif char == ":" and depth == 0:
            return text[:index].strip(), text[index + 1:].strip()
    raise ScopeError("SPEC_PARSE_ERROR", "expected mapping separator")


def _scalar(text: str):
    text = text.strip()
    if not text:
        raise ScopeError("SPEC_PARSE_ERROR", "empty scalar")
    # CLA-04/R4-01: chỉ bác control ở vị trí cấu trúc; prose được giữ nguyên
    # dù có &, *, !!, Markdown, glob hoặc HTML entity.
    if re.match(r"^(?:&[A-Za-z0-9_-]+|\*[A-Za-z0-9_-]+|![!A-Za-z0-9_-]+)(?:\s|$)", text):
        raise ScopeError("SPEC_PARSE_ERROR", "unsupported YAML control " + text.split()[0])
    if text[0] in "[{":
        close = "]" if text[0] == "[" else "}"
        if not text.endswith(close):
            raise ScopeError("SPEC_PARSE_ERROR", "unterminated flow value")
        parts = _split_flow(text[1:-1])
        if text[0] == "[":
            return [_scalar(part) for part in parts]
        out = {}
        for part in parts:
            key, value = _split_mapping(part)
            key = _scalar(key) if key[:1] in {'"', "'"} else key
            if not isinstance(key, str) or not key or key in out:
                raise ScopeError("SPEC_DUPLICATE_KEY", str(key))
            out[key] = _scalar(value)
        return out
    if text in {"null", "~"}:
        return None
    if text in {"true", "false"}:
        return text == "true"
    if text[:1] in {'"', "'"}:
        if len(text) < 2 or text[-1] != text[0]:
            raise ScopeError("SPEC_PARSE_ERROR", "unterminated quoted scalar")
        if text[0] == '"':
            try:
                return json.loads(text)
            except json.JSONDecodeError as exc:
                raise ScopeError("SPEC_PARSE_ERROR", str(exc)) from exc
        return text[1:-1].replace("''", "'")
    try:
        return int(text)
    except ValueError:
        return text


def _is_item_mapping(text: str) -> bool:
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_-]*\s*:\s*", text))


def _parse_yaml_subset(raw: str):
    """Đọc fenced subset nhưng không diễn giải prose thành cú pháp YAML."""
    if "\t" in raw:
        raise ScopeError("SPEC_PARSE_ERROR", "tabs are not supported")
    out, active_key, active_item = {}, None, None
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
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key):
                raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: invalid key")
            if key in out:
                raise ScopeError("SPEC_DUPLICATE_KEY", key)
            active_item = None
            if value.strip():
                out[key] = _scalar(value)
                active_key = None
            else:
                out[key] = []
                active_key = key
            continue
        if indent < 2 or active_key is None or not isinstance(out[active_key], list):
            raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: unexpected indentation")
        if indent == 2 and text.startswith("- "):
            value = text[2:].strip()
            if not value:
                raise ScopeError("SPEC_PARSE_ERROR", f"line {number}: empty list item")
            if _is_item_mapping(value):
                key, item_value = value.split(":", 1)
                active_item = {key.strip(): _scalar(item_value)}
                out[active_key].append(active_item)
            else:
                active_item = None
                out[active_key].append(_scalar(value))
        elif indent >= 4 and active_item is not None and _is_item_mapping(text):
            key, value = text.split(":", 1)
            key = key.strip()
            if key in active_item:
                raise ScopeError("SPEC_DUPLICATE_KEY", key)
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
        value = (json.loads(raw, object_pairs_hook=_json_object)
                 if raw.lstrip().startswith("{") else _parse_yaml_subset(raw))
    except json.JSONDecodeError as exc:
        raise ScopeError("SPEC_PARSE_ERROR", str(exc)) from exc
    if not isinstance(value, dict):
        raise ScopeError("SPEC_PARSE_ERROR", "spec must be an object")
    missing = sorted(REQUIRED_SPEC_FIELDS - set(value))
    if missing:
        raise ScopeError("SPEC_MISSING_FIELD", ",".join(missing))
    contracts = {
        "schema_version": int, "packet_id": str, "mission_issue": int,
        "revision": int, "spec_hash": str, "objective": str,
        "executor": str, "environment": str, "risk": str,
    }
    for key, expected in contracts.items():
        if not isinstance(value[key], expected) or (expected is int and isinstance(value[key], bool)):
            raise ScopeError("SPEC_FIELD_TYPE", key)
    if value["schema_version"] != 1 or value["mission_issue"] < 1:
        raise ScopeError("SPEC_FIELD_VALUE", "schema_version/mission_issue")
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
    pure = PurePosixPath(value)
    if (pure.is_absolute() or value.startswith("/") or re.match(r"^[A-Za-z]:/", value)
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise ScopeError("INVALID_FILE_PATH", value)
    return str(pure)


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
        if rule["type"] not in {"exact", "prefix"}:
            raise ScopeError("INVALID_SCOPE", f"{value_key}[{index}] type")
        result.append((rule["type"], normalizer(rule[value_key])))
    return result


def _covered(value: str, rules) -> bool:
    return any((kind == "exact" and value == declared) or
               (kind == "prefix" and (value == declared or value.startswith(declared + "/")))
               for kind, declared in rules)


def _casefold_collisions(values: list[str]) -> list[list[str]]:
    groups = {}
    for value in values:
        groups.setdefault(value.casefold(), set()).add(value)
    return [sorted(group) for group in groups.values() if len(group) > 1]


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
    collision_signal = {
        "files": _casefold_collisions(files + [value for _, value in file_rules]),
        "refs": _casefold_collisions(refs + [value for _, value in ref_rules]),
    }
    if outside_files or outside_refs:
        raise ScopeError("OUT_OF_SCOPE", json.dumps({
            "files": outside_files, "refs": outside_refs,
            "casefold_collisions": collision_signal,
        }, ensure_ascii=False, sort_keys=True))
    return {"files_checked": len(files), "refs_checked": len(refs),
            "casefold_collisions": collision_signal}


def _emit(payload, as_json, rc):
    if as_json or rc == 64:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print("packet_scope_check: ok=%s error=%s" % (payload["ok"], payload.get("error")))
    return rc


def main(argv=None):
    _configure_stdout()
    payload = {"schema": "packet_scope_check.v1", "ok": False}
    as_json = "--json" in (sys.argv[1:] if argv is None else argv)
    try:
        parser = JsonArgumentParser()
        parser.add_argument("--spec", required=True, type=Path)
        parser.add_argument("--changes", required=True, type=Path)
        parser.add_argument("--json", action="store_true")
        args = parser.parse_args(argv)
        as_json = args.json
        spec = load_spec(args.spec)
        try:
            changes = json.loads(args.changes.read_text(encoding="utf-8-sig"),
                                 object_pairs_hook=_json_object)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ScopeError("CHANGES_PARSE_ERROR", str(exc)) from exc
        payload.update(check(spec, changes))
        payload["ok"] = True
        return _emit(payload, as_json, 0)
    except OperatorError as exc:
        payload.update(error="ARGUMENT_ERROR", detail=exc.detail)
        return _emit(payload, True, 64)
    except ScopeError as exc:
        payload.update(error=exc.code, detail=exc.detail)
        return _emit(payload, as_json, 1)


if __name__ == "__main__":
    sys.exit(main())
