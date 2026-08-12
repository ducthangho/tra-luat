# -*- coding: utf-8 -*-
"""Phản chứng cặp chạy thật — wp84 r4, verdict Claude 5270183458."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zlib
from copy import deepcopy
from pathlib import Path


CHECK = Path(__file__).with_name("packet_scope_check.py")
R5_FENCE_SHA256 = "397f738afdc29a03e7e12760afc9c22d3ba6cf2ece4c1c3af806776a33b6ee12"
R5_FENCE_ZLIB_BASE64 = "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"

BASE = {
    "schema_version": 1,
    "packet_id": "wp999",
    "mission_issue": 54,
    "revision": 1,
    "spec_hash": "0" * 64,
    "objective": "đối chứng phạm vi & * !! chỉ là văn xuôi",
    "write_set": [{"type": "exact", "path": "docs/a.md"}],
    "ref_set": [{"type": "exact", "ref": "refs/heads/codex/wp999"}],
    "depends_on": [],
    "executor": "codex",
    "environment": "local",
    "risk": "normal",
    "acceptance_criteria": ["đối chứng"],
}


def _r5_fence() -> str:
    raw = zlib.decompress(base64.b64decode(R5_FENCE_ZLIB_BASE64)).decode("utf-8")
    actual = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if actual != R5_FENCE_SHA256:
        raise AssertionError("r5 fenced fixture hash drift: " + actual)
    return raw


def _run(tmp: Path, spec=BASE, changes=None, *, raw_spec=None, extra_args=None,
         hostile_encoding=False):
    spec_path = tmp / "packet.yaml"
    changes_path = tmp / "changes.json"
    if raw_spec is None:
        spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    else:
        spec_path.write_bytes(raw_spec.encode("utf-8"))
    if changes is None:
        changes = {"files": [], "refs": []}
    changes_path.write_text(json.dumps(changes, ensure_ascii=False), encoding="utf-8")
    argv = [sys.executable, str(CHECK), "--spec", str(spec_path),
            "--changes", str(changes_path), "--json"]
    if extra_args:
        argv.extend(extra_args)
    env = dict(os.environ)
    env.pop("PYTHONUTF8", None)
    env.pop("PYTHONIOENCODING", None)
    if hostile_encoding:
        env["PYTHONUTF8"] = "0"
        env["PYTHONIOENCODING"] = "cp1252"
    proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        payload = {"ok": False, "error": "NON_JSON",
                   "raw": proc.stdout.decode("utf-8", "replace"),
                   "stderr": proc.stderr.decode("utf-8", "replace")}
    return proc.returncode, payload


def main():
    cases = []
    with tempfile.TemporaryDirectory(prefix="wp84_scope_") as name:
        tmp = Path(name)

        def case(label, want_rc, *, spec=BASE, changes=None, raw_spec=None,
                 want_error=None, pair=None, extra_args=None, hostile_encoding=False,
                 detail_contains=None):
            rc, payload = _run(tmp, spec, changes, raw_spec=raw_spec,
                               extra_args=extra_args, hostile_encoding=hostile_encoding)
            ok = rc == want_rc and bool(payload.get("ok")) == (want_rc == 0)
            if want_error is not None:
                ok = ok and payload.get("error") == want_error
            if detail_contains is not None:
                ok = ok and detail_contains in str(payload.get("detail"))
            cases.append({"label": label, "ok": ok, "rc": rc, "payload": payload,
                          "pair": pair})

        case("baseline_json_green", 0,
             changes={"files": ["docs/a.md"], "refs": ["refs/heads/codex/wp999"]})
        case("outside_file_red", 1, changes={"files": ["docs/b.md"], "refs": []},
             want_error="OUT_OF_SCOPE", pair="baseline_json_green")
        case("outside_ref_red", 1, changes={"files": [], "refs": ["refs/heads/master"]},
             want_error="OUT_OF_SCOPE", pair="baseline_json_green")

        yaml_green = """schema_version: 1
packet_id: wp999
mission_issue: 54
revision: 1
spec_hash: "0000000000000000000000000000000000000000000000000000000000000000"
objective: Văn xuôi có A & B, dấu *, !!, `.github/**`, và &#34; không phải control
write_set:
  - type: prefix
    path: docs/sub
ref_set:
  - {type: prefix, ref: refs/heads/codex/wp999}
depends_on: [57]
executor: codex
environment: local
risk: normal
acceptance_criteria:
  - Chuỗi có dấu hai chấm: vẫn là văn xuôi
"""
        case("yaml_prose_and_flow_green", 0, raw_spec=yaml_green,
             changes={"files": ["docs/sub/x.md"], "refs": ["refs/heads/codex/wp999/topic"]})
        case("prefix_boundary_red", 1, raw_spec=yaml_green,
             changes={"files": ["docs/submarine/x.md"], "refs": []},
             want_error="OUT_OF_SCOPE", pair="yaml_prose_and_flow_green")
        case("unterminated_flow_red", 1,
             raw_spec=yaml_green.replace("depends_on: [57]", "depends_on: [57"),
             want_error="SPEC_PARSE_ERROR", pair="yaml_prose_and_flow_green")
        case("anchor_structural_red", 1,
             raw_spec=yaml_green.replace("objective: Văn", "objective: &neo Văn"),
             want_error="SPEC_PARSE_ERROR", pair="yaml_prose_and_flow_green")
        case("alias_structural_red", 1,
             raw_spec=yaml_green.replace("objective: Văn", "objective: *neo Văn"),
             want_error="SPEC_PARSE_ERROR", pair="yaml_prose_and_flow_green")
        case("tag_structural_red", 1,
             raw_spec=yaml_green.replace("objective: Văn", "objective: !!str Văn"),
             want_error="SPEC_PARSE_ERROR", pair="yaml_prose_and_flow_green")
        case("duplicate_yaml_red", 1, raw_spec=yaml_green + "risk: normal\n",
             want_error="SPEC_DUPLICATE_KEY", pair="yaml_prose_and_flow_green")

        duplicate_json = json.dumps(BASE, ensure_ascii=False)[:-1] + ',"ref_set":[]}'
        case("duplicate_json_red", 1, raw_spec=duplicate_json,
             want_error="SPEC_DUPLICATE_KEY", pair="baseline_json_green")

        missing_schema = deepcopy(BASE)
        missing_schema.pop("schema_version")
        case("missing_schema_version_red", 1, spec=missing_schema,
             want_error="SPEC_MISSING_FIELD", pair="baseline_json_green",
             detail_contains="schema_version")
        missing_mission = deepcopy(BASE)
        missing_mission.pop("mission_issue")
        case("missing_mission_issue_red", 1, spec=missing_mission,
             want_error="SPEC_MISSING_FIELD", pair="baseline_json_green",
             detail_contains="mission_issue")
        missing_ref = deepcopy(BASE)
        missing_ref.pop("ref_set")
        case("missing_ref_set_red", 1, spec=missing_ref,
             want_error="SPEC_MISSING_FIELD", pair="baseline_json_green",
             detail_contains="ref_set")
        for field in sorted(set(BASE) - {"schema_version", "mission_issue", "ref_set"}):
            missing_one = deepcopy(BASE)
            missing_one.pop(field)
            case("missing_required_%s_red" % field, 1, spec=missing_one,
                 want_error="SPEC_MISSING_FIELD", pair="baseline_json_green",
                 detail_contains=field)
        for label, field, value in (
            ("schema_version_string_red", "schema_version", "1"),
            ("schema_version_unknown_red", "schema_version", 999),
            ("mission_issue_string_red", "mission_issue", "54"),
        ):
            invalid = deepcopy(BASE)
            invalid[field] = value
            case(label, 1, spec=invalid, want_error=(
                "SPEC_FIELD_TYPE" if isinstance(value, str) else "SPEC_FIELD_VALUE"),
                pair="baseline_json_green", detail_contains=field)

        case_spec = deepcopy(BASE)
        case_spec["write_set"] = [{"type": "exact", "path": "Docs/A.md"}]
        case("case_exact_green", 0, spec=case_spec,
             changes={"files": ["Docs/A.md"], "refs": []})
        case("case_mismatch_red", 1, spec=case_spec,
             changes={"files": ["docs/a.md"], "refs": []},
             want_error="OUT_OF_SCOPE", pair="case_exact_green",
             detail_contains="casefold_collisions")

        nfc_spec = deepcopy(BASE)
        nfc_spec["write_set"] = [{"type": "exact", "path": "docs/Quốc-hội.md"}]
        case("unicode_nfc_green", 0, spec=nfc_spec,
             changes={"files": ["docs/Quo\u0302\u0301c-ho\u0323\u0302i.md"], "refs": []})
        case("unicode_invalid_path_red", 1, spec=nfc_spec,
             changes={"files": ["Quốc hội/../x"], "refs": []},
             want_error="INVALID_FILE_PATH", pair="unicode_nfc_green",
             hostile_encoding=True, detail_contains="Quốc hội")

        case("malformed_changes_red", 1, changes={"files": []},
             want_error="CHANGES_PARSE_ERROR", pair="baseline_json_green")
        case("invalid_flag_operator_rc64", 64, extra_args=["--không-hợp-lệ"],
             want_error="ARGUMENT_ERROR", pair="baseline_json_green")

        r5 = _r5_fence()
        r5_changes = {
            "files": ["docs/PROTOCOL_DA_PHIEN.md"],
            "refs": ["refs/heads/codex/wp84-r5-g5-protocol-hash-hardening"],
        }
        case("r5_exact_posted_bytes_green", 0, raw_spec=r5, changes=r5_changes)
        case("r5_ref_g3_out_of_scope_red", 1, raw_spec=r5, changes={
            "files": [], "refs": ["refs/heads/codex/wp84-r3-g3-protocol-hash-hardening"]},
            want_error="OUT_OF_SCOPE", pair="r5_exact_posted_bytes_green")
        lines = r5.splitlines(keepends=True)
        start = next(i for i, line in enumerate(lines) if line == "ref_set:\n")
        removed = lines[start:start + 3]
        if removed != ["ref_set:\n", "  - type: exact\n",
                       "    ref: refs/heads/codex/wp84-r5-g5-protocol-hash-hardening\n"]:
            raise AssertionError("r5 ref_set fence shape drift")
        without_ref = "".join(lines[:start] + lines[start + 3:])
        case("r5_delete_exact_three_ref_set_lines_red", 1, raw_spec=without_ref,
             changes=r5_changes, want_error="SPEC_MISSING_FIELD",
             detail_contains="ref_set", pair="r5_exact_posted_bytes_green")

    by_label = {item["label"]: item for item in cases}
    for item in cases:
        if item["rc"] != 0:
            pair = by_label.get(item["pair"])
            item["ok"] = item["ok"] and pair is not None and pair["rc"] == 0 and pair["ok"]
    passed = sum(item["ok"] for item in cases)
    for item in cases:
        print("[%s] %s rc=%s error=%s pair=%s" % (
            "OK" if item["ok"] else "FAIL", item["label"], item["rc"],
            item["payload"].get("error"), item["pair"]))
    print("packet_scope_check_test: %d/%d" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
