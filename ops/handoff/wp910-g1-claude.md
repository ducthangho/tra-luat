# Handoff wp910 — executor claude, lease `wp910-r2-g2-claude` (revision 2, pha A)

PR #913 (draft), head `6e09f4b`. Nguồn sự thật: spec r1 `ops/specs/wp910.md` (sha256
`2383ca2e540203e0b449e3f6118d84817f81984e937d463e99a7b862449a6613`) + delta r2 `ops/specs/wp910-r2.md` (sha256
`c3179d006b46fa82fe144cc1200dab72dbd9e88de28159f541504a7831dde7fc`), lease `ops/leases/wp910-r2-g2-claude.yaml` (22e93c4).
Lượt r1 dừng ở #910 issuecomment-6383050837 (ci_dang_ky_test.py băm trọn gate-nhanh-manh); chủ kho chọn 1 (issuecomment-6383127937).

```yaml
schema_version: 1
packet_id: wp910
generation: 2
spec_hash: c3179d006b46fa82fe144cc1200dab72dbd9e88de28159f541504a7831dde7fc
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_01FLVLxi5gKZgtVvbuTCEqEn
base_sha: e739ac1b74024a20949425c447fb6cf025317c0e
head_sha: 6e09f4b013629ae3d8d6e75f1a1c8e10aaa960b4     # PR #913 (draft)
status: done
summary: >-
  timeout-minutes cap job len 150: ci.yml gate 60, gate-ops 60, gate-packet-loop 120; launcher-windows.yml launcher 40.
  ops/ci_duong_nhanh_test.py: anh chup dict job (3 gia tri) va moc dot bien yml_gate_timeout_1_phut (neo 150).
  gate-nhanh-manh giu 30 — doi sang pha B cung gate-registry/dot-bien-du (can sua BAM_GATE_NHANH/BAM_GATE_REGISTRY trong
  .claude/dev/ci_dang_ky_test.py, dang bi wp899-r3-g2-claude giu).
changed_paths: [.github/workflows/ci.yml, .github/workflows/launcher-windows.yml, ops/ci_duong_nhanh_test.py]
tests:   # tren 6e09f4b tru khi ghi khac
  - {name: "N1/N2 so (job, buoc, timeout) da parse base/head", status: passed, evidence: "ci.yml 11 muc, doi dung 3 (gate 60->150, gate-ops 60->150, gate-packet-loop 120->150); launcher-windows.yml 1 muc, doi 1 (40->150); gate-nhanh-manh giu 30. Lenh: yaml.safe_load cua git show e739ac1:<tep> va tep head, liet ke job+buoc co timeout-minutes, so tung cap"}
  - {name: "N3 actionlint", status: passed, evidence: "rc 0 tren base va head (actionlint 1.7.7); shellcheck VANG trong container nen luat shell khong do"}
  - {name: "N4 ops/ci_duong_nhanh_test.py", status: passed, evidence: "CA: 104/104 dat · DOT BIEN: 392/392 bi giet dung ly do · TONG: DAT (cuc bo)"}
  - {name: "N4 .claude/dev/ci_dang_ky_test.py (KHONG sua)", status: passed, evidence: "PHAN CHUNG 1070/1070 do dung · TONG: DAT (cuc bo, khong --chay); voi ban 5 job (r1) thi DO 'hai job manh/gom nhanh_don_duoc lech cau hinh ghim'"}
  - {name: "N5 ci.yml pull_request", status: passed, evidence: "run 40086912335 success; 25/25 check-run tren 6e09f4b success"}
  - {name: "N5 launcher-windows.yml workflow_dispatch", status: passed, evidence: "run 40086911203 success tren 6e09f4b"}
  - {name: "Codex cross-review luot 1/2", status: passed, evidence: "launcher run 2073ebe8ffc34d17a3667e49f8634f4d, ma_thoat 0, 677.9 s, prompt_sha256 0a56f8b4… = sha256 tep prompt; approve tren 6e09f4b, 0 finding P0-P3; model gpt-6.1-sol xhigh theo header CLI (model THUC phuc vu KHONG_DO_DUOC). Reviewer ghi: ci_duong_nhanh_test DO giong het base trong sandbox cua no (cam bind socket Unix) — gioi han moi truong. Ban chep ops/reviews/wp910-g2-luot1-*. Da dung 1/2 loi goi."}
test_selection:
  gate_tier: T2
  selector_policy_sha: null
  tested_sha: 6e09f4b013629ae3d8d6e75f1a1c8e10aaa960b4
  selected_groups: [ci_duong_nhanh_test, ci_dang_ky_test, actionlint, ci_yml_pr, launcher_windows_dispatch]
  full_fallback_reason: "spec muc Tieu chi"
remaining_work:
  - "pha B (revision rieng): gate-registry 105, dot-bien-du 105, gate-nhanh-manh 30 -> 150; sua BAM_GATE_NHANH + BAM_GATE_REGISTRY + dot bien timeout-trung trong .claude/dev/ci_dang_ky_test.py; chi mo sau khi wp899-r3-g2-claude nha tep ay"
  - "ngoai packet: chu thich ci.yml tren gate-registry ('Timeout KHAC gate/gate-packet-loop (van 60)') da cu tu truoc (gate-packet-loop 120) va nay cang sai; spec cam sua ngoai dong timeout"
  - "merge do chu kho; sau merge: ghi so land + rut han lease"
next_role: human
manual_next_action: "Chu kho xet merge PR #913; sau do ghi so land va rut han wp910-r2-g2-claude"
copyable_prompt: null
failure:
  fingerprint: null
  category: null
successors: []
```
