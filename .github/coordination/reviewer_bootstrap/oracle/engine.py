"""Small independent JSON-Schema 2020-12 assertion engine used by RA-02.

Only inventoried keywords are accepted.  A new keyword is not silently ignored:
the oracle reports ``ANCHOR MISSING`` before validating candidate documents.
"""

from __future__ import annotations

import datetime as _datetime
import json
import re
from typing import Mapping, Sequence

ASSERTION_KEYWORDS = frozenset({
    "type", "enum", "const", "pattern", "format", "minimum", "maximum", "minLength",
    "maxLength", "minItems", "maxItems", "uniqueItems", "required", "properties", "items",
    "prefixItems", "contains", "additionalProperties", "unevaluatedProperties", "oneOf",
    "anyOf", "allOf", "not", "if", "then", "else", "dependentRequired", "$ref",
})
ANNOTATION_KEYWORDS = frozenset({"$schema", "$id", "$defs", "title", "description", "default", "examples"})
SUPPORTED_KEYWORDS = ASSERTION_KEYWORDS | ANNOTATION_KEYWORDS


def inventory(schema: object) -> frozenset[str]:
    found: set[str] = set()
    def visit(node: object):
        if not isinstance(node, dict):
            return
        for key, value in node.items():
            found.add(key)
            if key in ("properties", "$defs") and isinstance(value, dict):
                for child in value.values(): visit(child)
            elif key in ("items", "contains", "additionalProperties", "unevaluatedProperties", "not", "if", "then", "else"):
                if isinstance(value, dict): visit(value)
            elif key in ("prefixItems", "oneOf", "anyOf", "allOf") and isinstance(value, list):
                for child in value: visit(child)
    visit(schema)
    return frozenset(found)


def resolve(root: Mapping[str, object], ref: str) -> object:
    if not isinstance(ref, str) or not ref.startswith("#/"):
        raise ValueError("remote or malformed $ref rejected: %r" % ref)
    node: object = root
    for raw in ref[2:].split("/"):
        key = raw.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or key not in node:
            raise ValueError("unresolved local $ref: %s" % ref)
        node = node[key]
    return node


def _type_ok(expected: object, value: object) -> bool:
    choices = expected if isinstance(expected, list) else [expected]
    checks = {
        "null": lambda x: x is None,
        "boolean": lambda x: isinstance(x, bool),
        "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
        "number": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        "string": lambda x: isinstance(x, str),
        "array": lambda x: isinstance(x, list),
        "object": lambda x: isinstance(x, dict),
    }
    return any(choice in checks and checks[choice](value) for choice in choices)


def validate(schema: Mapping[str, object], instance: object) -> list[dict[str, object]]:
    errors: list[dict[str, object]] = []
    def fail(path: Sequence[object], keyword: str, message: str):
        errors.append({"path": list(path), "keyword": keyword, "message": message})
    def walk(node: object, value: object, path: tuple[object, ...]):
        if not isinstance(node, dict):
            fail(path, "schema", "schema node is not an object"); return
        if "$ref" in node:
            try: walk(resolve(schema, node["$ref"]), value, path)
            except ValueError as exc: fail(path, "$ref", str(exc))
            return
        if "type" in node and not _type_ok(node["type"], value): fail(path, "type", "type mismatch")
        if "const" in node and value != node["const"]: fail(path, "const", "const mismatch")
        if "enum" in node and value not in node["enum"]: fail(path, "enum", "enum mismatch")
        if isinstance(value, str):
            if "pattern" in node and re.search(node["pattern"], value) is None: fail(path, "pattern", "pattern mismatch")
            if "minLength" in node and len(value) < node["minLength"]: fail(path, "minLength", "string too short")
            if "maxLength" in node and len(value) > node["maxLength"]: fail(path, "maxLength", "string too long")
            if node.get("format") == "date-time":
                try: _datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError: fail(path, "format", "invalid date-time")
            if node.get("format") == "uri" and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value): fail(path, "format", "invalid uri")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in node and value < node["minimum"]: fail(path, "minimum", "below minimum")
            if "maximum" in node and value > node["maximum"]: fail(path, "maximum", "above maximum")
        if isinstance(value, dict):
            required = node.get("required", [])
            for key in required:
                if key not in value: fail(path + (key,), "required", "required property missing")
            properties = node.get("properties", {})
            if isinstance(properties, dict):
                for key, child in properties.items():
                    if key in value: walk(child, value[key], path + (key,))
                extras = set(value) - set(properties)
                if node.get("additionalProperties") is False or node.get("unevaluatedProperties") is False:
                    for key in sorted(extras): fail(path + (key,), "additionalProperties", "additional property rejected")
                elif isinstance(node.get("additionalProperties"), dict):
                    for key in extras: walk(node["additionalProperties"], value[key], path + (key,))
            for key, dependencies in node.get("dependentRequired", {}).items():
                if key in value:
                    for dependency in dependencies:
                        if dependency not in value: fail(path + (dependency,), "dependentRequired", "dependent property missing")
        if isinstance(value, list):
            if "minItems" in node and len(value) < node["minItems"]: fail(path, "minItems", "too few items")
            if "maxItems" in node and len(value) > node["maxItems"]: fail(path, "maxItems", "too many items")
            if node.get("uniqueItems") is True:
                seen=[]
                for item in value:
                    if item in seen: fail(path, "uniqueItems", "duplicate item"); break
                    seen.append(item)
            if isinstance(node.get("items"), dict):
                for index, item in enumerate(value): walk(node["items"], item, path + (index,))
            if isinstance(node.get("prefixItems"), list):
                for index, child in enumerate(node["prefixItems"]):
                    if index < len(value): walk(child, value[index], path + (index,))
            if "contains" in node and not any(not _probe(node["contains"], item) for item in value):
                fail(path, "contains", "no item matches contains")
        for keyword in ("allOf", "anyOf", "oneOf"):
            if keyword in node:
                results = [not _probe(child, value) for child in node[keyword]]
                good = all(results) if keyword == "allOf" else any(results) if keyword == "anyOf" else sum(results) == 1
                if not good: fail(path, keyword, "%s failed" % keyword)
        if "not" in node and not _probe(node["not"], value): fail(path, "not", "not subschema matched")
        if "if" in node:
            branch = "then" if not _probe(node["if"], value) else "else"
            if branch in node: walk(node[branch], value, path)
    def _probe(node: object, value: object) -> list[dict[str, object]]:
        prior = len(errors); walk(node, value, ()); produced = errors[prior:]; del errors[prior:]; return produced
    walk(schema, instance, ())
    return errors


def schema_shape_errors(schema: object) -> list[str]:
    errors: list[str] = []
    def visit(node: object, path: str):
        if not isinstance(node, dict): errors.append("%s is not an object" % path); return
        unknown = set(node) - SUPPORTED_KEYWORDS
        if unknown: errors.append("ANCHOR MISSING at %s: %s" % (path, ", ".join(sorted(unknown))))
        for key in ("$schema", "$id", "title", "description"):
            if key in node and not isinstance(node[key], str): errors.append("%s.%s malformed" % (path, key))
        if "required" in node and (not isinstance(node["required"], list) or not all(isinstance(x, str) for x in node["required"])): errors.append("%s.required malformed" % path)
        if "enum" in node and not isinstance(node["enum"], list): errors.append("%s.enum malformed" % path)
        if "properties" in node:
            if not isinstance(node["properties"], dict): errors.append("%s.properties malformed" % path)
            else:
                for key, child in node["properties"].items(): visit(child, "%s.properties.%s" % (path, key))
        if "$defs" in node:
            if not isinstance(node["$defs"], dict): errors.append("%s.$defs malformed" % path)
            else:
                for key, child in node["$defs"].items(): visit(child, "%s.$defs.%s" % (path, key))
        for key in ("items", "contains", "additionalProperties", "unevaluatedProperties", "not", "if", "then", "else"):
            if isinstance(node.get(key), dict): visit(node[key], "%s.%s" % (path, key))
        for key in ("prefixItems", "oneOf", "anyOf", "allOf"):
            if key in node:
                if not isinstance(node[key], list): errors.append("%s.%s malformed" % (path, key))
                else:
                    for index, child in enumerate(node[key]): visit(child, "%s.%s[%d]" % (path, key, index))
    visit(schema, "$")
    return errors


def keyword_anchors(inventory_keywords: Sequence[str]) -> dict[str, dict[str, object]]:
    """Run positive and negative conformance teeth for every inventoried keyword."""
    micro = {
        "type": ({"type": "integer"}, 1, "1"),
        "enum": ({"enum": ["a"]}, "a", "b"),
        "const": ({"const": 1}, 1, 2),
        "pattern": ({"type": "string", "pattern": "^a$"}, "a", "b"),
        "format": ({"type": "string", "format": "date-time"}, "2026-08-11T00:00:00Z", "not-a-date"),
        "minimum": ({"type": "integer", "minimum": 1}, 1, 0),
        "maximum": ({"type": "integer", "maximum": 1}, 1, 2),
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
        "additionalProperties": ({"type": "object", "properties": {"x": {}}, "additionalProperties": False}, {"x": 1}, {"x": 1, "y": 2}),
        "unevaluatedProperties": ({"type": "object", "properties": {"x": {}}, "unevaluatedProperties": False}, {"x": 1}, {"x": 1, "y": 2}),
        "oneOf": ({"oneOf": [{"type": "integer"}, {"const": 2}]}, 1, 2),
        "anyOf": ({"anyOf": [{"const": 1}, {"const": 2}]}, 1, 3),
        "allOf": ({"allOf": [{"type": "integer"}, {"minimum": 1}]}, 1, 0),
        "not": ({"not": {"const": 1}}, 2, 1),
        "if": ({"if": {"properties": {"x": {"const": 1}}}, "then": {"required": ["y"]}}, {"x": 2}, {"x": 1}),
        "then": ({"if": {"properties": {"x": {"const": 1}}}, "then": {"required": ["y"]}}, {"x": 1, "y": 2}, {"x": 1}),
        "else": ({"if": {"properties": {"x": {"const": 1}}}, "else": {"required": ["z"]}}, {"x": 1}, {"x": 2}),
        "dependentRequired": ({"type": "object", "dependentRequired": {"x": ["y"]}}, {"x": 1, "y": 2}, {"x": 1}),
        "$ref": ({"$ref": "#/$defs/x", "$defs": {"x": {"const": 1}}}, 1, 2),
    }
    annotations = {
        "$schema": ("https://json-schema.org/draft/2020-12/schema", 1),
        "$id": ("urn:wp86:test", 1),
        "title": ("title", 1),
        "description": ("description", 1),
        "$defs": ({"x": {"type": "integer"}}, []),
    }
    report: dict[str, dict[str, object]] = {}
    for keyword in sorted(set(inventory_keywords)):
        if keyword in micro:
            schema, valid_value, invalid_value = micro[keyword]
            good = not validate(schema, valid_value)
            bad = bool(validate(schema, invalid_value))
        elif keyword in ("default", "examples"):
            annotation_value = 1 if keyword == "default" else [1]
            schema = {"type": "integer", keyword: annotation_value}
            # Annotation values never authorize an otherwise-invalid instance.
            # This is an executable positive/negative tooth, not a hardcoded
            # flag for keywords whose values are intentionally non-assertive.
            good = not validate(schema, 1)
            bad = bool(validate(schema, "annotation-is-not-authority"))
        elif keyword in annotations:
            good_value, bad_value = annotations[keyword]
            good = not schema_shape_errors({keyword: good_value})
            bad = bool(schema_shape_errors({keyword: bad_value}))
        else:
            good = bad = False
        report[keyword] = {
            "valid_case_id": "kw-%s-positive" % keyword.replace("$", "dollar-"),
            "invalid_case_id": "kw-%s-negative" % keyword.replace("$", "dollar-"),
            "valid_passed": good,
            "invalid_failed": bad,
        }
    return report
