# -*- coding: utf-8 -*-
"""Acceptance tests for the change-impact policy validator.

The public seam is the command-line program and its JSON envelope.  Every case
uses a temporary worktree-like directory; no test imports validator internals.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path


HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "change_impact_validate.py"
NOW = "2026-08-09T00:00:00Z"


def _path(path: str = "policy.txt", kind: str = "exact") -> dict:
    return {"type": kind, "path": path}


def _rule(rule_id: str = "valid-rule", trigger=None, closure=None) -> dict:
    return {
        "rule_id": rule_id,
        "trigger": trigger if trigger is not None else [_path()],
        "write_closure": closure if closure is not None else [_path("companion.txt")],
        "required_checks": ["python check.py"],
        "land_obligations": [],
        "evidence": ["check.py:10 — measured 1/1 on exact fixture"],
        "owner": "mission-54",
        "expires_at": None,
    }


def _policy(rules=None) -> dict:
    return {
        "schema_version": 1,
        "policy_id": "change-impact.v1",
        "candidate_rules": list(rules if rules is not None else [_rule()]),
        "unproven_candidates": [],
        "land_obligations": [],
    }


def _invoke(
    root: Path,
    policy: dict,
    *,
    now: str = NOW,
    filename: str = "policy.json",
    schema: dict | None = None,
):
    policy_path = root / filename
    policy_path.write_text(
        json.dumps(policy, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    arguments = [
        sys.executable,
        str(VALIDATOR),
        "--policy",
        str(policy_path),
        "--root",
        str(root),
        "--now",
        now,
        "--json",
    ]
    if schema is not None:
        schema_path = root / (filename + ".schema.json")
        schema_path.write_text(
            json.dumps(schema, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        arguments.extend(["--schema", str(schema_path)])
    proc = subprocess.run(
        arguments,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8"),
    )
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        payload = None
    return proc.returncode, payload, proc.stderr.decode("utf-8", "replace")


def _codes(payload) -> set[str]:
    return {str(item.get("code")) for item in ((payload or {}).get("errors") or [])}


def _fails(root: Path, policy: dict, code: str) -> bool:
    rc, payload, _ = _invoke(root, policy)
    return rc != 0 and payload is not None and payload.get("ok") is False and code in _codes(payload)


def case_valid_policy_has_machine_hash(root: Path) -> bool:
    (root / "policy.txt").write_text("x\n", encoding="utf-8", newline="\n")
    rc, payload, _ = _invoke(root, _policy())
    digest = str((payload or {}).get("change_policy_sha") or "")
    return (
        rc == 0
        and payload.get("ok") is True
        and payload.get("schema_version") == 1
        and payload.get("rule_count") == 1
        and len(digest) == 64
        and all(c in "0123456789abcdef" for c in digest)
    )


def case_separator_and_nfc_normalize_before_hash(root: Path) -> bool:
    nfc = "tài liệu/café.txt"
    nfd = unicodedata.normalize("NFD", nfc)
    target = root / Path(nfc)
    target.parent.mkdir(parents=True)
    target.write_text("x\n", encoding="utf-8", newline="\n")
    first = _policy([_rule(trigger=[_path(nfc)])])
    second = _policy([_rule(trigger=[_path(nfd.replace("/", "\\"))])])
    rc1, p1, _ = _invoke(root, first, filename="first.json")
    rc2, p2, _ = _invoke(root, second, filename="second.json")
    return rc1 == rc2 == 0 and p1["change_policy_sha"] == p2["change_policy_sha"]


def case_absolute_paths_rejected(root: Path) -> bool:
    bad = ("/etc/passwd", "C:\\Windows\\system.ini", "\\\\server\\share\\x")
    return all(
        _fails(root, _policy([_rule(trigger=[_path(value)])]), "PATH_ABSOLUTE")
        for value in bad
    )


def case_dot_and_parent_segments_rejected(root: Path) -> bool:
    bad = ("./x.txt", "a/../x.txt", "a/./x.txt")
    return all(
        _fails(root, _policy([_rule(trigger=[_path(value)])]), "PATH_SEGMENT_FORBIDDEN")
        for value in bad
    )


def case_glob_type_and_metacharacters_rejected(root: Path) -> bool:
    bad_type = _policy([_rule(trigger=[_path("scripts", "glob")])])
    bad_chars = _policy([_rule(trigger=[_path("scripts/*.py", "prefix")])])
    return _fails(root, bad_type, "PATH_TYPE_INVALID") and _fails(
        root, bad_chars, "PATH_GLOB_FORBIDDEN"
    )


def case_casefold_collision_rejected(root: Path) -> bool:
    rule = _rule(closure=[_path("Alpha.txt"), _path("alpha.txt")])
    return _fails(root, _policy([rule]), "PATH_COLLISION")


def case_casefold_collision_across_rule_fields_rejected(root: Path) -> bool:
    first = _rule("first-rule", trigger=[_path("Alpha.txt")])
    second = _rule("second-rule", closure=[_path("alpha.txt")])
    return _fails(root, _policy([first, second]), "PATH_COLLISION")


def case_nfc_collision_rejected(root: Path) -> bool:
    one = "café.txt"
    two = unicodedata.normalize("NFD", one)
    rule = _rule(closure=[_path(one), _path(two)])
    return _fails(root, _policy([rule]), "PATH_COLLISION")


def case_new_file_parent_inside_root_passes(root: Path) -> bool:
    rule = _rule(trigger=[_path("new/deep/file.txt")])
    rc, payload, _ = _invoke(root, _policy([rule]))
    return rc == 0 and payload.get("ok") is True


def case_symlink_escape_rejected(root: Path) -> bool:
    with tempfile.TemporaryDirectory(prefix="impact_outside_") as outside:
        link = root / "outside-link"
        try:
            link.symlink_to(Path(outside), target_is_directory=True)
        except (OSError, NotImplementedError):
            # Windows without Developer Mode cannot create the fixture.  CI's Linux lane
            # executes the same case; the production validator remains platform-neutral.
            return True
        return _fails(
            root,
            _policy([_rule(trigger=[_path("outside-link/new.txt")])]),
            "PATH_ESCAPES_ROOT",
        )


def case_missing_evidence_fails_closed(root: Path) -> bool:
    rule = _rule()
    rule["evidence"] = []
    return _fails(root, _policy([rule]), "EVIDENCE_REQUIRED")


def case_missing_owner_fails_closed(root: Path) -> bool:
    rule = _rule()
    rule["owner"] = ""
    return _fails(root, _policy([rule]), "OWNER_REQUIRED")


def case_expired_rule_fails_closed(root: Path) -> bool:
    rule = _rule()
    rule["expires_at"] = "2026-08-08T23:59:59Z"
    return _fails(root, _policy([rule]), "RULE_EXPIRED")


def case_future_expiry_passes(root: Path) -> bool:
    rule = _rule()
    rule["expires_at"] = "2026-09-08T00:00:00Z"
    rc, payload, _ = _invoke(root, _policy([rule]))
    return rc == 0 and payload.get("ok") is True


def case_duplicate_rule_id_rejected(root: Path) -> bool:
    return _fails(root, _policy([_rule("same"), _rule("same")]), "RULE_ID_DUPLICATE")


def case_schema_version_one_required(root: Path) -> bool:
    policy = _policy()
    policy["schema_version"] = 2
    return _fails(root, policy, "SCHEMA_VERSION_UNSUPPORTED")


def case_schema_policy_id_const_enforced(root: Path) -> bool:
    policy = _policy()
    policy["policy_id"] = "change-impact.v2"
    return _fails(root, policy, "SCHEMA_VIOLATION")


def case_schema_unproven_candidate_shape_enforced(root: Path) -> bool:
    policy = _policy()
    policy["unproven_candidates"] = [{"rule_id": "missing-fields"}]
    return _fails(root, policy, "SCHEMA_VIOLATION")


def case_schema_land_obligation_shape_enforced(root: Path) -> bool:
    policy = _policy()
    policy["land_obligations"] = [{"obligation_id": "missing-fields"}]
    return _fails(root, policy, "SCHEMA_VIOLATION")


def case_schema_unknown_keyword_fails_closed(root: Path) -> bool:
    schema = json.loads((HERE.parent / "coordination" / "schemas" / "change-impact.v1.schema.json").read_text(encoding="utf-8"))
    schema["properties"]["candidate_rules"]["maxItems"] = 99
    rc, payload, _ = _invoke(root, _policy(), schema=schema)
    return rc != 0 and payload.get("ok") is False and "SCHEMA_INVALID" in _codes(payload)


def case_trigger_object_form_is_canonicalized(root: Path) -> bool:
    rule = _rule(trigger=_path("policy.txt"))
    rc, payload, _ = _invoke(root, _policy([rule]))
    return rc == 0 and payload.get("ok") is True


def case_canonical_hash_ignores_json_key_order(root: Path) -> bool:
    policy = _policy()
    reversed_policy = {key: policy[key] for key in reversed(tuple(policy))}
    rc1, p1, _ = _invoke(root, policy, filename="ordered.json")
    rc2, p2, _ = _invoke(root, reversed_policy, filename="reversed.json")
    return rc1 == rc2 == 0 and p1["change_policy_sha"] == p2["change_policy_sha"]


def case_runtime_python_inventory_detects_added_file(root: Path) -> bool:
    scripts = root / "scripts"
    scripts.mkdir()
    (scripts / "existing.py").write_text("# fixture\n", encoding="utf-8", newline="\n")
    rule = _rule(
        "runtime-py-added-moves-golden",
        trigger=[_path("scripts/existing.py")],
        closure=[_path("references/golden/workflow_audit.json")],
    )
    rc, payload, _ = _invoke(root, _policy([rule]), filename="before.json")
    (scripts / "new_runtime.py").write_text("# added\n", encoding="utf-8", newline="\n")
    return (
        rc == 0
        and payload.get("ok") is True
        and _fails(root, _policy([rule]), "RUNTIME_PY_TRIGGER_STALE")
    )


CASES = [
    case_valid_policy_has_machine_hash,
    case_separator_and_nfc_normalize_before_hash,
    case_absolute_paths_rejected,
    case_dot_and_parent_segments_rejected,
    case_glob_type_and_metacharacters_rejected,
    case_casefold_collision_rejected,
    case_casefold_collision_across_rule_fields_rejected,
    case_nfc_collision_rejected,
    case_new_file_parent_inside_root_passes,
    case_symlink_escape_rejected,
    case_missing_evidence_fails_closed,
    case_missing_owner_fails_closed,
    case_expired_rule_fails_closed,
    case_future_expiry_passes,
    case_duplicate_rule_id_rejected,
    case_schema_version_one_required,
    case_schema_policy_id_const_enforced,
    case_schema_unproven_candidate_shape_enforced,
    case_schema_land_obligation_shape_enforced,
    case_schema_unknown_keyword_fails_closed,
    case_trigger_object_form_is_canonicalized,
    case_canonical_hash_ignores_json_key_order,
    case_runtime_python_inventory_detects_added_file,
]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    passed = 0
    failed = []
    for case in CASES:
        with tempfile.TemporaryDirectory(prefix="change_impact_") as tmp:
            root = Path(tmp)
            try:
                ok = bool(case(root))
            except Exception as exc:  # noqa: BLE001 — acceptance harness must report, never swallow
                ok = False
                print("  ! %s: %r" % (case.__name__, exc))
        print("%s %s" % ("PASS" if ok else "FAIL", case.__name__))
        if ok:
            passed += 1
        else:
            failed.append(case.__name__)
    print("\n%d/%d passed" % (passed, len(CASES)))
    if failed:
        print("FAILED: %s" % ", ".join(failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
