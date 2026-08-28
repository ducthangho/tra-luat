#!/usr/bin/env python3
"""Validate a review verdict against its on-disk schema and runtime bindings.

JSON Schema owns the document shape.  The repository-specific
``x-tra-luat-runtime-bindings`` annotation only binds fields whose expected
values exist at runtime, such as the exact review head and packet generation.
"""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import exceptions as jsonschema_exceptions
from jsonschema import validators


SCHEMA_REVIEW = (
    Path(__file__).resolve().parents[2]
    / ".github"
    / "coordination"
    / "schemas"
    / "review_verdict.v1.schema.json"
)


BINDING_KEY = "x-tra-luat-runtime-bindings"

# Allow-list, not deny-list.  Every key below MUST be declared by the schema:
# a schema that omits one cannot measure that binding, so it is refused rather
# than skipped.  Unknown keys are refused too — a binding this module does not
# implement must never read as enforced.
BINDING_MOC = {
    "reviewed_sha": "exact_review_head",
    "generation": "exact_packet_generation",
}
BINDING_DANH_SACH = ("role", "model_reviewer_identity.provider")
BINDING_BAT_BUOC = tuple(BINDING_MOC) + BINDING_DANH_SACH


class ReviewVerdictError(ValueError):
    """A verdict or its schema could not be measured as valid."""


def _read_json(path: Path, label: str):
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReviewVerdictError(
            f"không đọc được {label} {path}: {type(exc).__name__}"
        ) from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReviewVerdictError(
            f"không parse được {label} {path}: dòng {exc.lineno}, cột {exc.colno}"
        ) from exc


def _truong(doc: dict, ten: str):
    """Read one required field, failing closed instead of raising KeyError."""
    if ten not in doc:
        raise ReviewVerdictError(f"verdict thiếu trường bắt buộc {ten}")
    return doc[ten]


def load_review_verdict(path: str | Path) -> dict:
    """Read one verdict JSON document from disk, failing closed on its type."""
    verdict_path = Path(path)
    verdict = _read_json(verdict_path, "verdict")
    if not isinstance(verdict, dict):
        raise ReviewVerdictError(
            f"verdict {verdict_path} phải là JSON object, nhận {type(verdict).__name__}"
        )
    return verdict


def validate_review_verdict(
    verdict: dict,
    *,
    expected_reviewed_sha: str,
    expected_generation: int,
    schema_path: str | Path = SCHEMA_REVIEW,
) -> dict:
    """Validate JSON Schema shape, then apply the bindings declared by that schema."""
    schema_path = Path(schema_path)
    schema = _read_json(schema_path, "schema review")
    if not isinstance(schema, dict):
        raise ReviewVerdictError(
            f"schema review {schema_path} phải là JSON object, "
            f"nhận {type(schema).__name__}"
        )

    try:
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)
        errors = sorted(
            validator_class(schema).iter_errors(verdict),
            key=lambda err: tuple(str(part) for part in err.absolute_path),
        )
    except jsonschema_exceptions.SchemaError as exc:
        raise ReviewVerdictError(
            f"schema review {schema_path} không hợp lệ: {exc.message}"
        ) from exc
    if errors:
        first = errors[0]
        where = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise ReviewVerdictError(
            f"verdict không qua jsonschema tại {where}: {first.message}"
        )

    bindings = schema.get(BINDING_KEY)
    if bindings is None:
        raise ReviewVerdictError(
            f"schema review {schema_path} không khai {BINDING_KEY}: "
            "không có gì cưỡng chế semantic identity"
        )
    if not isinstance(bindings, dict):
        raise ReviewVerdictError(f"{BINDING_KEY} phải là JSON object")

    thieu = [khoa for khoa in BINDING_BAT_BUOC if khoa not in bindings]
    if thieu:
        raise ReviewVerdictError(
            f"{BINDING_KEY} thiếu binding bắt buộc: {', '.join(sorted(thieu))}"
        )
    la = [khoa for khoa in bindings if khoa not in BINDING_BAT_BUOC]
    if la:
        raise ReviewVerdictError(
            f"{BINDING_KEY} khai binding không nhận diện được: {', '.join(sorted(la))}"
        )

    for khoa, moc in BINDING_MOC.items():
        if bindings[khoa] != moc:
            raise ReviewVerdictError(f"binding {khoa} không được nhận diện")
    for khoa in BINDING_DANH_SACH:
        if not isinstance(bindings[khoa], list) or not bindings[khoa]:
            raise ReviewVerdictError(f"binding {khoa} phải là danh sách không rỗng")

    if _truong(verdict, "reviewed_sha") != expected_reviewed_sha:
        raise ReviewVerdictError(
            "reviewed_sha của verdict không khớp exact head đã đưa ra review"
        )
    if _truong(verdict, "generation") != expected_generation:
        raise ReviewVerdictError(
            "generation của verdict không khớp packet generation đang chạy"
        )
    if _truong(verdict, "role") not in bindings["role"]:
        raise ReviewVerdictError("role của verdict không nằm trong runtime binding")
    danh_tinh = _truong(verdict, "model_reviewer_identity")
    if not isinstance(danh_tinh, dict):
        raise ReviewVerdictError("model_reviewer_identity phải là JSON object")
    if _truong(danh_tinh, "provider") not in bindings["model_reviewer_identity.provider"]:
        raise ReviewVerdictError(
            "model_reviewer_identity.provider không nằm trong runtime binding"
        )

    return verdict
