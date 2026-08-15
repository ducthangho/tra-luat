"""Independent stdlib JSON Schema 2020-12 assertion engine.

The engine rejects unsupported or malformed schema keywords by exact name.  It
does not contain a copy of the five protocol field contracts; those are parsed
from the Dispatcher-pinned target checkout as data.
"""

from __future__ import annotations

import datetime
import json
import math
import re
from typing import Mapping, Sequence

ASSERTION_KEYWORDS = frozenset(
    {
        "type",
        "enum",
        "const",
        "pattern",
        "format",
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "minLength",
        "maxLength",
        "minItems",
        "maxItems",
        "uniqueItems",
        "required",
        "properties",
        "items",
        "prefixItems",
        "contains",
        "minContains",
        "maxContains",
        "additionalProperties",
        "unevaluatedProperties",
        "oneOf",
        "anyOf",
        "allOf",
        "not",
        "if",
        "then",
        "else",
        "dependentRequired",
        "$ref",
    }
)
ANNOTATION_KEYWORDS = frozenset(
    {"$schema", "$id", "$defs", "title", "description", "default", "examples"}
)
SUPPORTED_KEYWORDS = ASSERTION_KEYWORDS | ANNOTATION_KEYWORDS
SCHEMA_CHILD_MAP = frozenset(
    {"items", "contains", "additionalProperties", "unevaluatedProperties", "not", "if", "then", "else"}
)
SCHEMA_CHILD_LIST = frozenset({"prefixItems", "oneOf", "anyOf", "allOf"})


def keyword_inventory(schema: object) -> frozenset[str]:
    found: set[str] = set()

    def visit(node: object) -> None:
        if isinstance(node, bool):
            return
        if not isinstance(node, dict):
            return
        for keyword, value in node.items():
            found.add(keyword)
            if keyword in ("properties", "$defs") and isinstance(value, dict):
                for child in value.values():
                    visit(child)
            elif keyword in SCHEMA_CHILD_MAP and isinstance(value, (dict, bool)):
                visit(value)
            elif keyword in SCHEMA_CHILD_LIST and isinstance(value, list):
                for child in value:
                    visit(child)

    visit(schema)
    return frozenset(found)


def resolve(root: Mapping[str, object], ref: object) -> object:
    if not isinstance(ref, str) or not ref.startswith("#/"):
        raise ValueError("remote or malformed $ref rejected: %r" % ref)
    node: object = root
    for raw in ref[2:].split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, Mapping) or key not in node:
            raise ValueError("unresolved local $ref: %s" % ref)
        node = node[key]
    return node


def _type_ok(expected: object, value: object) -> bool:
    choices = expected if isinstance(expected, list) else [expected]
    checks = {
        "null": lambda item: item is None,
        "boolean": lambda item: isinstance(item, bool),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool) and math.isfinite(item),
        "string": lambda item: isinstance(item, str),
        "array": lambda item: isinstance(item, list),
        "object": lambda item: isinstance(item, dict),
    }
    return any(choice in checks and checks[choice](value) for choice in choices)


def _json_equal(left: object, right: object) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    return type(left) is type(right) and left == right


def validate(schema: Mapping[str, object], instance: object) -> list[dict[str, object]]:
    root = schema

    def walk(node: object, value: object, path: tuple[object, ...], refs: tuple[str, ...]) -> list[dict[str, object]]:
        errors: list[dict[str, object]] = []

        def fail(keyword: str, message: str, at: tuple[object, ...] = path) -> None:
            errors.append({"path": list(at), "keyword": keyword, "message": message})

        if node is True:
            return errors
        if node is False:
            fail("false_schema", "boolean false schema rejects every instance")
            return errors
        if not isinstance(node, Mapping):
            fail("schema", "schema node is not an object or boolean")
            return errors

        if "$ref" in node:
            try:
                ref = node["$ref"]
                if not isinstance(ref, str) or ref in refs:
                    raise ValueError("cyclic or malformed $ref rejected: %r" % ref)
                errors.extend(walk(resolve(root, ref), value, path, refs + (ref,)))
            except ValueError as exc:
                fail("$ref", str(exc))

        if "type" in node and not _type_ok(node["type"], value):
            fail("type", "type mismatch")
        if "const" in node and not _json_equal(value, node["const"]):
            fail("const", "const mismatch")
        if "enum" in node and isinstance(node["enum"], list) and not any(
            _json_equal(value, choice) for choice in node["enum"]
        ):
            fail("enum", "enum mismatch")

        if isinstance(value, str):
            if "pattern" in node:
                try:
                    matched = re.search(str(node["pattern"]), value) is not None
                except re.error as exc:
                    fail("pattern", "invalid schema pattern: %s" % exc)
                else:
                    if not matched:
                        fail("pattern", "pattern mismatch")
            if isinstance(node.get("minLength"), int) and len(value) < node["minLength"]:
                fail("minLength", "string too short")
            if isinstance(node.get("maxLength"), int) and len(value) > node["maxLength"]:
                fail("maxLength", "string too long")
            if node.get("format") == "date-time":
                try:
                    parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
                    if parsed.tzinfo is None:
                        raise ValueError("timezone required")
                except ValueError:
                    fail("format", "invalid date-time")
            elif node.get("format") == "uri" and re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value) is None:
                fail("format", "invalid absolute URI")

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            comparisons = (
                ("minimum", lambda left, right: left < right, "below minimum"),
                ("maximum", lambda left, right: left > right, "above maximum"),
                ("exclusiveMinimum", lambda left, right: left <= right, "not above exclusiveMinimum"),
                ("exclusiveMaximum", lambda left, right: left >= right, "not below exclusiveMaximum"),
            )
            for keyword, predicate, message in comparisons:
                if keyword in node and predicate(value, node[keyword]):
                    fail(keyword, message)

        evaluated_properties: set[str] = set()
        if isinstance(value, dict):
            required = node.get("required", [])
            if isinstance(required, list):
                for key in required:
                    if key not in value:
                        fail("required", "required property missing", path + (key,))
            properties = node.get("properties", {})
            if isinstance(properties, Mapping):
                for key, child in properties.items():
                    if key in value:
                        evaluated_properties.add(key)
                        errors.extend(walk(child, value[key], path + (key,), refs))
            extras = set(value) - evaluated_properties
            additional = node.get("additionalProperties", True)
            if additional is False:
                for key in sorted(extras):
                    fail("additionalProperties", "additional property rejected", path + (key,))
            elif isinstance(additional, (dict, bool)):
                for key in sorted(extras):
                    errors.extend(walk(additional, value[key], path + (key,), refs))
                    evaluated_properties.add(key)
            if node.get("unevaluatedProperties") is False:
                for key in sorted(set(value) - evaluated_properties):
                    fail("unevaluatedProperties", "unevaluated property rejected", path + (key,))
            dependent = node.get("dependentRequired", {})
            if isinstance(dependent, Mapping):
                for key, dependencies in dependent.items():
                    if key in value and isinstance(dependencies, list):
                        for dependency in dependencies:
                            if dependency not in value:
                                fail("dependentRequired", "dependent property missing", path + (dependency,))

        if isinstance(value, list):
            if isinstance(node.get("minItems"), int) and len(value) < node["minItems"]:
                fail("minItems", "too few items")
            if isinstance(node.get("maxItems"), int) and len(value) > node["maxItems"]:
                fail("maxItems", "too many items")
            if node.get("uniqueItems") is True:
                for index, item in enumerate(value):
                    if any(_json_equal(item, prior) for prior in value[:index]):
                        fail("uniqueItems", "duplicate item", path + (index,))
                        break
            prefix = node.get("prefixItems", [])
            if isinstance(prefix, list):
                for index, child in enumerate(prefix[: len(value)]):
                    errors.extend(walk(child, value[index], path + (index,), refs))
            items = node.get("items")
            if isinstance(items, (dict, bool)):
                start = len(prefix) if isinstance(prefix, list) else 0
                for index in range(start, len(value)):
                    errors.extend(walk(items, value[index], path + (index,), refs))
            if "contains" in node:
                count = sum(not walk(node["contains"], item, path + (index,), refs) for index, item in enumerate(value))
                minimum = node.get("minContains", 1)
                maximum = node.get("maxContains")
                if count < minimum or (isinstance(maximum, int) and count > maximum):
                    fail("contains", "contains match count outside bounds")

        for keyword in ("allOf", "anyOf", "oneOf"):
            children = node.get(keyword)
            if isinstance(children, list):
                outcomes = [not walk(child, value, path, refs) for child in children]
                good = all(outcomes) if keyword == "allOf" else any(outcomes) if keyword == "anyOf" else sum(outcomes) == 1
                if not good:
                    fail(keyword, "%s failed" % keyword)
        if "not" in node and not walk(node["not"], value, path, refs):
            fail("not", "not subschema matched")
        if "if" in node:
            branch = "then" if not walk(node["if"], value, path, refs) else "else"
            if branch in node:
                errors.extend(walk(node[branch], value, path, refs))
        return errors

    return walk(root, instance, (), ())


def schema_shape_errors(schema: object) -> list[str]:
    errors: list[str] = []

    def visit(node: object, path: str) -> None:
        if isinstance(node, bool):
            return
        if not isinstance(node, dict):
            errors.append("%s is not a schema object or boolean" % path)
            return
        unknown = set(node) - SUPPORTED_KEYWORDS
        if unknown:
            errors.append("ANCHOR_MISSING at %s: %s" % (path, ",".join(sorted(unknown))))
        if "$ref" in node:
            try:
                if not isinstance(schema, Mapping):
                    raise ValueError("root schema is not an object")
                resolve(schema, node["$ref"])
            except ValueError as exc:
                errors.append("%s.$ref rejected: %s" % (path, exc))
        for keyword in ("$schema", "$id", "title", "description", "format", "pattern"):
            if keyword in node and not isinstance(node[keyword], str):
                errors.append("%s.%s malformed" % (path, keyword))
        for keyword in ("required", "enum"):
            if keyword in node and not isinstance(node[keyword], list):
                errors.append("%s.%s malformed" % (path, keyword))
        for keyword in ("properties", "$defs"):
            if keyword in node:
                if not isinstance(node[keyword], dict):
                    errors.append("%s.%s malformed" % (path, keyword))
                else:
                    for key, child in node[keyword].items():
                        visit(child, "%s.%s.%s" % (path, keyword, key))
        for keyword in SCHEMA_CHILD_MAP:
            if keyword in node:
                if not isinstance(node[keyword], (dict, bool)):
                    errors.append("%s.%s malformed" % (path, keyword))
                else:
                    visit(node[keyword], "%s.%s" % (path, keyword))
        for keyword in SCHEMA_CHILD_LIST:
            if keyword in node:
                if not isinstance(node[keyword], list):
                    errors.append("%s.%s malformed" % (path, keyword))
                else:
                    for index, child in enumerate(node[keyword]):
                        visit(child, "%s.%s[%d]" % (path, keyword, index))

    visit(schema, "$")
    return errors


def keyword_controls(
    keywords: Sequence[str],
    independent: object | None = None,
) -> dict[str, dict[str, object]]:
    """Executable positive/negative teeth for every schema keyword.

    Trước bản vá này cả hai răng đều do CHÍNH `engine.validate` chấm — bộ máy tự
    chấm bài của mình, và cái cổng tự chấm đó lại có quyền làm đỏ cả oracle (R7
    của verdict 5297249899).  Nay mỗi răng phải được BỘ MÁY ĐỘC LẬP xác nhận, và
    hai bên bất đồng là một bản ghi ĐỎ chứ không phải một phiếu bầu.

    `independent` phải có `.validate(schema, instance) -> bool` (hợp lệ?) và
    `.check_schema(schema) -> bool` (schema hợp lệ?).  Thiếu nó thì mọi control
    đỏ theo TÊN, không im lặng bỏ qua.
    """
    micro: dict[str, tuple[object, object, object]] = {
        "type": ({"type": "integer"}, 1, "1"),
        "enum": ({"enum": ["a"]}, "a", "b"),
        "const": ({"const": 1}, 1, 2),
        "pattern": ({"type": "string", "pattern": "^a$"}, "a", "b"),
        "format": ({"type": "string", "format": "date-time"}, "2026-08-14T00:00:00Z", "not-a-date"),
        "minimum": ({"type": "integer", "minimum": 1}, 1, 0),
        "maximum": ({"type": "integer", "maximum": 1}, 1, 2),
        "exclusiveMinimum": ({"type": "integer", "exclusiveMinimum": 1}, 2, 1),
        "exclusiveMaximum": ({"type": "integer", "exclusiveMaximum": 1}, 0, 1),
        "minLength": ({"type": "string", "minLength": 1}, "x", ""),
        "maxLength": ({"type": "string", "maxLength": 1}, "x", "xx"),
        "minItems": ({"type": "array", "minItems": 1}, [1], []),
        "maxItems": ({"type": "array", "maxItems": 1}, [1], [1, 2]),
        "uniqueItems": ({"type": "array", "uniqueItems": True}, [1, 2], [1, 1]),
        "required": ({"type": "object", "required": ["x"]}, {"x": 1}, {}),
        "properties": ({"type": "object", "properties": {"x": {"const": 1}}}, {"x": 1}, {"x": 2}),
        "items": ({"type": "array", "items": {"type": "integer"}}, [1], ["x"]),
        "prefixItems": ({"type": "array", "prefixItems": [{"type": "integer"}]}, [1], ["x"]),
        "contains": ({"type": "array", "contains": {"const": 1}}, [0, 1], [0, 2]),
        "minContains": ({"type": "array", "contains": {"const": 1}, "minContains": 2}, [1, 1], [1]),
        "maxContains": ({"type": "array", "contains": {"const": 1}, "maxContains": 1}, [1], [1, 1]),
        "additionalProperties": ({"type": "object", "properties": {"x": {}}, "additionalProperties": False}, {"x": 1}, {"y": 1}),
        "unevaluatedProperties": ({"type": "object", "properties": {"x": {}}, "unevaluatedProperties": False}, {"x": 1}, {"y": 1}),
        "oneOf": ({"oneOf": [{"type": "integer"}, {"const": 2}]}, 1, 2),
        "anyOf": ({"anyOf": [{"const": 1}, {"const": 2}]}, 1, 3),
        "allOf": ({"allOf": [{"type": "integer"}, {"minimum": 1}]}, 1, 0),
        "not": ({"not": {"const": 1}}, 2, 1),
        "if": ({"if": {"properties": {"x": {"const": 1}}}, "then": {"required": ["y"]}}, {"x": 2}, {"x": 1}),
        "then": ({"if": {"properties": {"x": {"const": 1}}}, "then": {"required": ["y"]}}, {"x": 1, "y": 1}, {"x": 1}),
        "else": ({"if": {"properties": {"x": {"const": 1}}}, "else": {"required": ["z"]}}, {"x": 1}, {"x": 2}),
        "dependentRequired": ({"type": "object", "dependentRequired": {"x": ["y"]}}, {"x": 1, "y": 2}, {"x": 1}),
        "$ref": ({"$ref": "#/$defs/x", "$defs": {"x": {"const": 1}}}, 1, 2),
    }
    annotation_good: dict[str, object] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://fixture.ra02.invalid/control.json",
        "$defs": {"x": {"type": "integer"}},
        "title": "text",
        "description": "text",
        "default": 1,
        "examples": [1],
    }
    annotation_bad: dict[str, object] = {
        "$schema": 1,
        "$id": 1,
        "$defs": [],
        "title": 1,
        "description": 1,
    }

    def _record(
        local_positive: bool,
        local_negative: bool,
        independent_positive: bool | None,
        independent_negative: bool | None,
        mode: str,
    ) -> dict[str, object]:
        agreement = (
            independent_positive is not None
            and independent_negative is not None
            and bool(local_positive) is bool(independent_positive)
            and bool(local_negative) is bool(independent_negative)
        )
        return {
            "positive_passed": bool(local_positive and independent_positive and agreement),
            "negative_failed": bool(local_negative and independent_negative and agreement),
            "local_positive": bool(local_positive),
            "local_negative": bool(local_negative),
            "independent_positive": independent_positive,
            "independent_negative": independent_negative,
            "engine_agreement": agreement,
            "negative_mode": mode,
        }

    controls: dict[str, dict[str, object]] = {}
    for keyword in sorted(set(keywords)):
        if independent is None:
            controls[keyword] = {
                "positive_passed": False,
                "negative_failed": False,
                "local_positive": None,
                "local_negative": None,
                "independent_positive": None,
                "independent_negative": None,
                "engine_agreement": False,
                "negative_mode": "INDEPENDENT_ENGINE_MISSING",
            }
            continue
        if keyword in micro:
            schema, good, bad = micro[keyword]
            controls[keyword] = _record(
                not validate(schema, good),
                bool(validate(schema, bad)),
                independent.validate(schema, good),
                not independent.validate(schema, bad),
                "instance",
            )
        elif keyword in ANNOTATION_KEYWORDS:
            good_value = annotation_good.get(keyword, "text")
            good_schema = {"type": "integer", keyword: good_value}
            if keyword in annotation_bad:
                bad_schema = {"type": "integer", keyword: annotation_bad[keyword]}
                controls[keyword] = _record(
                    not schema_shape_errors(good_schema) and not validate(good_schema, 1),
                    bool(schema_shape_errors(bad_schema)),
                    independent.check_schema(good_schema) and independent.validate(good_schema, 1),
                    not independent.check_schema(bad_schema),
                    "schema_shape",
                )
            else:
                # `default`/`examples` là chú thích, không phải thẩm quyền: răng âm
                # của chúng là "một instance sai kiểu vẫn phải đỏ", chứ không phải
                # "giá trị chú thích sai làm schema đỏ".
                controls[keyword] = _record(
                    not schema_shape_errors(good_schema) and not validate(good_schema, 1),
                    bool(validate(good_schema, "wrong-type")),
                    independent.check_schema(good_schema) and independent.validate(good_schema, 1),
                    not independent.validate(good_schema, "wrong-type"),
                    "annotation_not_authority",
                )
        else:
            controls[keyword] = {
                "positive_passed": False,
                "negative_failed": False,
                "local_positive": None,
                "local_negative": None,
                "independent_positive": None,
                "independent_negative": None,
                "engine_agreement": False,
                "negative_mode": "ANCHOR_MISSING",
            }
    return controls
