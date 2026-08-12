# -*- coding: utf-8 -*-
"""Two-way executable counter-proofs for canonical checkpoint hashing.

Cases j/k/l project the verbatim published wp88 Fork A/Fork B basis objects
onto the new canonical field set.  The historical hashes remain immutable:
this test neither rewrites events nor treats the v1 schema as retroactive.
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

# Verbatim JSON basis blocks published in immutable comments 5264350972 and
# 5264354085.  The recorded hashes are provenance, not recomputed history.
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
    # Only the centrally-declared intersection is projected.  Fork-specific
    # prose/disposition remains outside basis_object and cannot move the head.
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
            validate_registry=False):
    args = [sys.executable, str(CHECK), "--registry", str(registry), "--schema", str(schema), "--json"]
    if validate_registry:
        args.append("--validate-registry")
    for flag, value, filename in (
        ("--event", event, "event.json"),
        ("--head", head, "head.json"),
        ("--sibling", sibling, "sibling.json"),
    ):
        if value is not None:
            path = tmp / filename
            path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
            args.extend([flag, str(path)])
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
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

        def record(label, result, want_rc, want_error=None, want_action=None):
            rc, payload = result
            ok = rc == want_rc and bool(payload.get("ok")) == (want_rc == 0)
            if want_error is not None:
                ok = ok and payload.get("error") == want_error
            if want_action is not None:
                ok = ok and payload.get("action") == want_action
            cases.append((label, ok, rc, payload))

        # Revision-2 cases (a)-(e), now enforced against the central registry.
        record("a_valid_basis_passes", _invoke(tmp, base), 0, want_action="append")
        changed = copy.deepcopy(base)
        changed["basis_object"]["state"] = "accepted"
        record("b_changed_field_fails", _invoke(tmp, changed), 1, "STATE_HASH_MISMATCH")
        reordered = copy.deepcopy(base)
        reordered["basis_object"] = dict(reversed(list(reordered["basis_object"].items())))
        record("c_key_order_is_canonical", _invoke(tmp, reordered), 0)
        missing_fields = copy.deepcopy(base)
        missing_fields.pop("state_hash_fields")
        record("d_state_hash_fields_required", _invoke(tmp, missing_fields), 1, "EVENT_MISSING_FIELD")
        wrong_head = {"state_hash": "9" * 64}
        record("e_broken_prev_chain_fails", _invoke(tmp, base, head=wrong_head), 1,
               "PREV_EVENT_HASH_MISMATCH")

        # PC-1/PC-2 strict schema, field-set and type counter-proofs (f)-(i).
        unknown = copy.deepcopy(base)
        unknown["checkpoint_schema_version"] = 999
        record("f_unknown_schema_fails", _invoke(tmp, unknown), 1, "UNKNOWN_CHECKPOINT_SCHEMA")
        missing = copy.deepcopy(base)
        missing["basis_object"].pop("base_sha")
        record("g_missing_canonical_field_fails", _invoke(tmp, missing), 1, "CANONICAL_FIELD_MISSING")
        extra = copy.deepcopy(base)
        extra["basis_object"]["commentary"] = "must stay outside basis"
        record("h_extra_canonical_field_fails", _invoke(tmp, extra), 1, "CANONICAL_FIELD_EXTRA")
        wrong_type = copy.deepcopy(base)
        wrong_type["basis_object"]["generation"] = "4"
        record("i_wrong_canonical_type_fails", _invoke(tmp, wrong_type), 1, "CANONICAL_FIELD_TYPE")

        # (j) The actual 48-key and 26-key wp88 records converge after central
        # projection.  Their different prose remains outside the basis.
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
        cases.append(("j_wp88_representation_forks_converge", j_equal, max(ra[0], rb[0]), rb[1]))

        # (k) Same predecessor/schema/basis/hash is a retry, not a new head.
        record("k_identical_sibling_is_idempotent", _invoke(tmp, from_a, sibling=from_b), 0,
               want_action="idempotent")

        # (l) Still derived from the two real wp88 records, but alter B's
        # substantive state and re-hash it as an independently valid sibling.
        divergent = _project(FORK_B, FORK_B_RECORDED_HASH)
        divergent["basis_object"]["state"] = "paused"
        divergent["basis_object"]["transition_to"] = "paused"
        divergent["state_hash"] = _canonical_hash(divergent["basis_object"])
        record("l_divergent_sibling_pauses", _invoke(tmp, from_a, sibling=divergent), 2,
               "SIBLING_CONFLICT", "pause")

        # (m) Registry absence and malformed content both fail closed.
        record("m_registry_absent_fails", _invoke(tmp, base, registry=tmp / "absent.json"), 1,
               "REGISTRY_READ_ERROR")
        broken_registry = tmp / "broken-registry.json"
        broken_registry.write_text("{broken", encoding="utf-8")
        record("n_registry_syntax_fails", _invoke(tmp, base, registry=broken_registry), 1,
               "REGISTRY_READ_ERROR")

        # Positive counterparts for PC-1 and PC-3/PC-4.
        record("o_registry_and_schema_validate", _invoke(tmp, validate_registry=True), 0,
               want_action="registry_valid")
        prose = copy.deepcopy(base)
        prose["disposition"] = "human-readable only"
        prose["notes"] = ["array order here is evidence, not basis"]
        record("p_top_level_prose_does_not_move_hash", _invoke(tmp, prose), 0)

    passed = sum(1 for _, ok, _, _ in cases if ok)
    for label, ok, rc, payload in cases:
        print("[%s] %s rc=%s action=%s error=%s" % (
            "OK" if ok else "FAIL", label, rc, payload.get("action"), payload.get("error")
        ))
    print("state_hash_check_test: %d/%d" % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
