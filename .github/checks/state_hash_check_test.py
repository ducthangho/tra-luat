# -*- coding: utf-8 -*-
"""Phản chứng hai chiều cho checkpoint hash — wp84 r4, verdict 5270183458.

Ca j/k/l chiếu nguyên basis wp88 Fork A/B vào tập canonical mới. Hash lịch sử
bất biến: test không viết lại event và không áp schema v1 hồi tố.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


CHECK = Path(__file__).with_name("state_hash_check.py")
ROOT = CHECK.parents[2]
REGISTRY = ROOT / ".github" / "coordination" / "checkpoint-schema.v1.json"
SCHEMA = ROOT / ".github" / "coordination" / "schemas" / "checkpoint-schema.v1.schema.json"

# Basis JSON nguyên văn từ comment bất biến 5264350972/5264354085; recorded
# hash là provenance, không phải lịch sử để tái tính.
FORK_A_RECORDED_HASH = "3574a68d4cfc62918e6e91e0301e7d0939ca7e5cc56bb06c6f69e35b34242428"
FORK_B_RECORDED_HASH = "f16d7dffaba9c19d6b3612611b00a4158e7cc85e57f74e361b9b3460b71b247c"
COMMON_PREDECESSOR = "184522125afd0bf3996708784e0d5c1ca934825c11a2e085da0815216450dfac"
FORK_A = json.loads(r'''{"approver":"ducthangho","authorization_id":"AUTH-WP88-01","authorization_url":"https://github.com/ducthangho/tra-luat/issues/88#issuecomment-5263869299","authorized_reviewed_head_sha":"1daa971f8d36744bb97c8904f9d2737ef1b141ea","base_sha":"d866eba152063427c00a8fbdc6934747fe764aad","blocking_findings":0,"branch":"codex/wp88-g3-f2-d-wt","deploy_performed":false,"f02_state":"open_unfixed_f3_infrastructure_lane_outside_mission_48","f04_disposition":"rejected_accepted_risk","f04_duplicate_review_comment_id":3764722484,"f2d_closed_by_wp88":false,"generation":4,"land_diff_path_count":2,"land_evidence_url":"https://github.com/ducthangho/tra-luat/issues/88#issuecomment-5264250136","land_head_sha":"1824907a17f93aec4fa68a5ad77bdba3b45a4170","landed_at":"2026-08-12T08:16:22Z","last_consumed_event_id":5264250136,"live_called":false,"merge_commit":"da8718ea601c9b0de23adc000c511e6982209c97","merge_land_authority":"exercised_and_spent","merge_method":"merge","mission_issue":48,"mission_plan_hash":"856a817c15e7bded2357b9f8df13bf65e828254d3c4d26858348f9b6a852cc0c","mission_revision":5,"mission_state":"running","next_role":"human","open_findings":[],"packet_id":"wp88","packet_issue":88,"packet_revision":4,"post_merge_ci_run_id":31577595108,"post_merge_gate":"green","pre_merge_ci_run_id":31576923447,"prev_event_hash":"184522125afd0bf3996708784e0d5c1ca934825c11a2e085da0815216450dfac","pull_request":93,"pull_request_state":"merged","review_assurance":"cross_approved","review_verdict":"approve","reviewed_sha":"1daa971f8d36744bb97c8904f9d2737ef1b141ea","row_12_outcome":"deferred","source_worktree_deleted":false,"source_worktree_mutated":false,"spec_hash":"3c2381fdc5fb3680fec97b4d45b70f30c973f9a99e3c2849f6b9ad8625f80720","state":"landed","target_ref":"master","worker_paths_byte_identical":"8/8","writer_reopened":false}''')
FORK_B = json.loads(r'''{"authorized_head_sha":"1daa971f8d36744bb97c8904f9d2737ef1b141ea","base_sha":"d866eba152063427c00a8fbdc6934747fe764aad","f2d_closed_by_wp88":false,"generation":4,"land_authorization_id":"AUTH-WP88-01","land_head_ci_run_id":31576923447,"land_head_sha":"1824907a17f93aec4fa68a5ad77bdba3b45a4170","last_consumed_event_id":5264250136,"master_after_merge":"da8718ea601c9b0de23adc000c511e6982209c97","merge_commit":"da8718ea601c9b0de23adc000c511e6982209c97","merge_method":"merge","mission_issue":48,"mission_plan_hash":"856a817c15e7bded2357b9f8df13bf65e828254d3c4d26858348f9b6a852cc0c","mission_revision":5,"mission_state":"running","next_role":"human","packet_id":"wp88","packet_issue":88,"packet_revision":4,"post_merge_ci_run_id":31577595108,"prev_event_hash":"184522125afd0bf3996708784e0d5c1ca934825c11a2e085da0815216450dfac","review_assurance_recorded":"cross_approved","row_12_outcome":"deferred","spec_hash":"3c2381fdc5fb3680fec97b4d45b70f30c973f9a99e3c2849f6b9ad8625f80720","state":"landed","write_set_count":8}''')


def _canonical_hash(basis):
    raw = json.dumps(basis, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


REGISTRY_DATA = json.loads(REGISTRY.read_text(encoding="utf-8"))
COMMON_NAMES = [item["name"] for item in REGISTRY_DATA["common_identity_basis"]["fields"]]


def _project(raw, source_hash):
    # PC-3/PC-6: chỉ chiếu giao khai tập trung; prose riêng nằm ngoài basis và
    # không được dịch chuyển head.
    basis = {name: raw[name] for name in COMMON_NAMES}
    basis.update({
        "event_type": "packet_transition",
        "event_id": raw["last_consumed_event_id"],
        "transition_from": "accepted",
        "transition_to": raw["state"],
        "consumed_fact_id": raw["last_consumed_event_id"],
    })
    fields = sorted(COMMON_NAMES + [
        item["name"]
        for item in REGISTRY_DATA["event_types"]["packet_transition"]["additional_fields"]
    ])
    return {
        "event_type": "packet_transition",
        "checkpoint_schema_id": REGISTRY_DATA["checkpoint_schema_id"],
        "checkpoint_schema_version": REGISTRY_DATA["checkpoint_schema_version"],
        "state_hash_fields": fields,
        "basis_object": basis,
        "state_hash": _canonical_hash(basis),
        "prose": {"immutable_historical_source_hash": source_hash},
    }


def _invoke(tmp, event=None, *, head=None, sibling=None, registry=REGISTRY, schema=SCHEMA,
            validate_registry=False, allow_no_head=True, allow_pre_registry=False,
            extra_args=None, hostile_encoding=False):
    args = [sys.executable, str(CHECK), "--registry", str(registry), "--schema", str(schema), "--json"]
    if validate_registry:
        args.append("--validate-registry")
    if event is not None and head is None and allow_no_head:
        args.append("--allow-unverified-no-head")
    if allow_pre_registry:
        args.append("--allow-pre-registry-head")
    for flag, value, filename in (
        ("--event", event, "event.json"),
        ("--head", head, "head.json"),
        ("--sibling", sibling, "sibling.json"),
    ):
        if value is not None:
            path = tmp / filename
            path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
            args.extend([flag, str(path)])
    if extra_args:
        args.extend(extra_args)
    env = dict(os.environ)
    env.pop("PYTHONUTF8", None)
    env.pop("PYTHONIOENCODING", None)
    if hostile_encoding:
        env["PYTHONUTF8"] = "0"
        env["PYTHONIOENCODING"] = "cp1252"
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        payload = {"ok": False, "error": "NON_JSON", "raw": proc.stdout.decode("utf-8", "replace")}
    return proc.returncode, payload


def main():
    cases = []
    with tempfile.TemporaryDirectory(prefix="wp84_state_hash_") as name:
        tmp = Path(name)
        base = _project(FORK_B, FORK_B_RECORDED_HASH)

        def record(label, result, want_rc, want_error=None, want_action=None, pair=None,
                   detail_contains=None):
            rc, payload = result
            ok = rc == want_rc and bool(payload.get("ok")) == (want_rc == 0)
            if want_error is not None:
                ok = ok and payload.get("error") == want_error
            if want_action is not None:
                ok = ok and payload.get("action") == want_action
            if detail_contains is not None:
                ok = ok and detail_contains in str(payload.get("detail"))
            cases.append({"label": label, "ok": ok, "rc": rc, "payload": payload,
                          "pair": pair})

        # Ca revision 2 (a)-(e), nay cưỡng chế theo registry tập trung.
        record("a_valid_basis_passes", _invoke(tmp, base), 0, want_action="unverified_no_head")
        changed = copy.deepcopy(base)
        changed["basis_object"]["state"] = "accepted"
        record("b_changed_field_fails", _invoke(tmp, changed), 1, "STATE_HASH_MISMATCH",
               pair="a_valid_basis_passes")
        reordered = copy.deepcopy(base)
        reordered["basis_object"] = dict(reversed(list(reordered["basis_object"].items())))
        record("c_key_order_is_canonical", _invoke(tmp, reordered), 0)
        missing_fields = copy.deepcopy(base)
        missing_fields.pop("state_hash_fields")
        record("d_state_hash_fields_required", _invoke(tmp, missing_fields), 1, "EVENT_MISSING_FIELD",
               pair="a_valid_basis_passes")
        prior = copy.deepcopy(base)
        prior["basis_object"]["prev_event_hash"] = "8" * 64
        prior["state_hash"] = _canonical_hash(prior["basis_object"])
        record("e_broken_prev_chain_fails", _invoke(tmp, base, head=prior), 1,
               "PREV_EVENT_HASH_MISMATCH", pair="current_schema_head_green")

        # Phản chứng schema/tập trường/kiểu nghiêm PC-1/PC-2 (f)-(i).
        unknown = copy.deepcopy(base)
        unknown["checkpoint_schema_version"] = 999
        record("f_unknown_schema_fails", _invoke(tmp, unknown), 1, "UNKNOWN_CHECKPOINT_SCHEMA",
               pair="a_valid_basis_passes")
        missing = copy.deepcopy(base)
        missing["basis_object"].pop("base_sha")
        record("g_missing_canonical_field_fails", _invoke(tmp, missing), 1, "CANONICAL_FIELD_MISSING",
               pair="a_valid_basis_passes")
        extra = copy.deepcopy(base)
        extra["basis_object"]["commentary"] = "must stay outside basis"
        record("h_extra_canonical_field_fails", _invoke(tmp, extra), 1, "CANONICAL_FIELD_EXTRA",
               pair="a_valid_basis_passes")
        wrong_type = copy.deepcopy(base)
        wrong_type["basis_object"]["generation"] = "4"
        record("i_wrong_canonical_type_fails", _invoke(tmp, wrong_type), 1, "CANONICAL_FIELD_TYPE",
               pair="a_valid_basis_passes")

        # (j) Hai record wp88 48/26 khoá hội tụ sau chiếu; prose khác ở ngoài basis.
        from_a = _project(FORK_A, FORK_A_RECORDED_HASH)
        from_b = _project(FORK_B, FORK_B_RECORDED_HASH)
        ra = _invoke(tmp, from_a)
        rb = _invoke(tmp, from_b)
        shared = set(FORK_A) & set(FORK_B)
        provenance_exact = (
            len(FORK_A) == 48
            and len(FORK_B) == 26
            and len(shared) == 20
            and FORK_A["prev_event_hash"] == FORK_B["prev_event_hash"] == COMMON_PREDECESSOR
            and all(FORK_A[key] == FORK_B[key] for key in shared)
        )
        j_equal = (
            provenance_exact
            and from_a["state_hash"] == from_b["state_hash"]
            and ra[0] == rb[0] == 0
        )
        cases.append({"label": "j_wp88_representation_forks_converge", "ok": j_equal,
                      "rc": max(ra[0], rb[0]), "payload": rb[1], "pair": None})

        # (k) Cùng predecessor/schema/basis/hash là retry, không phải head mới.
        record("k_identical_sibling_is_idempotent", _invoke(tmp, from_a, head=from_b, sibling=from_b), 0,
               want_action="idempotent")

        # (l) Vẫn từ hai record wp88 thật, đổi state B và hash thành sibling hợp lệ.
        divergent = _project(FORK_B, FORK_B_RECORDED_HASH)
        divergent["basis_object"]["state"] = "paused"
        divergent["basis_object"]["transition_to"] = "paused"
        divergent["state_hash"] = _canonical_hash(divergent["basis_object"])
        record("l_divergent_sibling_pauses", _invoke(tmp, from_a, head=divergent, sibling=divergent), 2,
               "SIBLING_CONFLICT", "pause", pair="k_identical_sibling_is_idempotent")

        # (m) Registry vắng/hỏng đều fail-closed.
        record("m_registry_absent_fails", _invoke(tmp, base, registry=tmp / "absent.json"), 1,
               "REGISTRY_READ_ERROR", pair="o_registry_and_schema_validate")
        broken_registry = tmp / "broken-registry.json"
        broken_registry.write_text("{broken", encoding="utf-8")
        record("n_registry_syntax_fails", _invoke(tmp, base, registry=broken_registry), 1,
               "REGISTRY_READ_ERROR", pair="o_registry_and_schema_validate")

        # Đối chứng dương PC-1 và PC-3/PC-4.
        record("o_registry_and_schema_validate", _invoke(tmp, validate_registry=True), 0,
               want_action="registry_valid")
        prose = copy.deepcopy(base)
        prose["disposition"] = "human-readable only"
        prose["notes"] = ["array order here is evidence, not basis"]
        record("p_top_level_prose_does_not_move_hash", _invoke(tmp, prose), 0)

        # CLA-01/R4-06: tái kiểm đầy đủ head schema hiện hành trước khi tin hash.
        next_event = copy.deepcopy(base)
        next_event["basis_object"]["prev_event_hash"] = base["state_hash"]
        next_event["state_hash"] = _canonical_hash(next_event["basis_object"])
        record("current_schema_head_green", _invoke(tmp, next_event, head=base), 0,
               want_action="append")
        tampered_head = copy.deepcopy(base)
        tampered_head["basis_object"]["state"] = "paused"
        record("current_schema_head_tamper_conflict", _invoke(tmp, next_event, head=tampered_head), 2,
               "HEAD_INTEGRITY_CONFLICT", "pause", pair="current_schema_head_green")
        unknown_head = copy.deepcopy(base)
        unknown_head["checkpoint_schema_version"] = 999
        record("current_schema_head_unknown_conflict", _invoke(tmp, next_event, head=unknown_head), 2,
               "HEAD_INTEGRITY_CONFLICT", "pause", pair="current_schema_head_green")
        incomplete_head = {"checkpoint_schema_id": REGISTRY_DATA["checkpoint_schema_id"],
                           "state_hash": base["state_hash"]}
        record("current_schema_head_incomplete_conflict", _invoke(tmp, next_event,
               head=incomplete_head), 2, "HEAD_INTEGRITY_CONFLICT", "pause",
               pair="current_schema_head_green")

        naked = {"state_hash": base["basis_object"]["prev_event_hash"]}
        record("naked_head_default_red", _invoke(tmp, base, head=naked), 1,
               "PRE_REGISTRY_HEAD_CONFIRMATION_REQUIRED", pair="naked_head_explicit_green")
        record("naked_head_explicit_green", _invoke(tmp, base, head=naked,
               allow_pre_registry=True), 0, want_action="unverified_pre_registry_head")
        record("no_head_default_red", _invoke(tmp, base, allow_no_head=False), 1,
               "HEAD_REQUIRED", pair="a_valid_basis_passes")

        bad_registry = copy.deepcopy(REGISTRY_DATA)
        bad_registry.pop("field_order")
        bad_registry_path = tmp / "bad-registry.json"
        bad_registry_path.write_text(json.dumps(bad_registry), encoding="utf-8")
        record("custom_registry_missing_key_json_red",
               _invoke(tmp, base, registry=bad_registry_path), 1,
               pair="o_registry_and_schema_validate")
        record("missing_custom_schema_json_red", _invoke(tmp, base,
               schema=tmp / "absent-schema.json"), 1, "REGISTRY_SCHEMA_READ_ERROR",
               pair="o_registry_and_schema_validate")
        invalid_schema_path = tmp / "invalid-schema.json"
        invalid_schema_path.write_text("[]", encoding="utf-8")
        record("invalid_custom_schema_json_red", _invoke(tmp, base,
               schema=invalid_schema_path), 1, "REGISTRY_SCHEMA_INVALID",
               pair="o_registry_and_schema_validate")
        record("invalid_flag_operator_rc64", _invoke(tmp, base,
               extra_args=["--cờ-không-hợp-lệ"], hostile_encoding=True), 64, "ARGUMENT_ERROR",
               pair="a_valid_basis_passes")
        unicode_bad = copy.deepcopy(base)
        unicode_bad["basis_object"]["state"] = "Quốc hội"
        record("utf8_hostile_negative_json", _invoke(tmp, unicode_bad,
               hostile_encoding=True), 1, "STATE_HASH_MISMATCH",
               pair="a_valid_basis_passes", detail_contains="expected")

    by_label = {item["label"]: item for item in cases}
    for item in cases:
        if item["rc"] != 0:
            pair = by_label.get(item["pair"])
            item["ok"] = item["ok"] and pair is not None and pair["rc"] == 0 and pair["ok"]
    passed = sum(item["ok"] for item in cases)
    for item in cases:
        print("[%s] %s rc=%s action=%s error=%s" % (
            "OK" if item["ok"] else "FAIL", item["label"], item["rc"],
            item["payload"].get("action"), item["payload"].get("error")
        ))
    print("state_hash_check_test: %d/%d" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
