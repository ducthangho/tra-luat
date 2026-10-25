# Handoff wp910 — executor claude, lease `wp910-r3-g3-claude` (revision 3, pha B)

PR #917, head `a7da463`. Nguồn sự thật: spec r1 `ops/specs/wp910.md` (sha256 `2383ca2e…6613`) + r2 `ops/specs/wp910-r2.md`
(`c3179d00…e7fc`) + r3 `ops/specs/wp910-r3.md` (`bb015dc66b08f9c559a0eecb1966558030991135bbf1a8004ac7108509a433bc`), lease
`ops/leases/wp910-r3-g3-claude.yaml` (d0c09b3). Pha A: PR #913 (merge e91a68a), sổ land PR #914.

```yaml
schema_version: 1
packet_id: wp910
generation: 3
spec_hash: bb015dc66b08f9c559a0eecb1966558030991135bbf1a8004ac7108509a433bc
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_01FLVLxi5gKZgtVvbuTCEqEn
base_sha: 1797c32a     # origin/master luc re nhanh; lease ghi 50a59a9, giua hai commit chi co ops/land/** (#916)
head_sha: a7da46390177cdc2d64f516dedac19857bee86dd     # PR #917
status: done
summary: >-
  timeout-minutes cap job len 150: ci.yml gate-nhanh-manh 30, gate-registry 105; ci-dot-bien-du.yml dot-bien-du 105.
  .claude/dev/ci_dang_ky_test.py: BAM_GATE_NHANH, BAM_GATE_REGISTRY tinh lai + literal dot bien timeout-trung neo 150.
  ops/ci_duong_nhanh_test.py: anh chup dict job hai gia tri.
changed_paths: [.github/workflows/ci.yml, .github/workflows/ci-dot-bien-du.yml, .claude/dev/ci_dang_ky_test.py, ops/ci_duong_nhanh_test.py]
tests:   # tren a7da463 tru khi ghi khac
  - {name: "N1/N2 so (tep, job, buoc, timeout) da parse base/head", status: passed, evidence: "ci.yml 11 muc doi dung 2 (gate-nhanh-manh 30->150, gate-registry 105->150); ci-dot-bien-du.yml 3 muc doi 1 (dot-bien-du 105->150); launcher-windows.yml 1 muc doi 0"}
  - {name: "hai hang bam", status: passed, evidence: "lenh: nap .claude/dev/ci_dang_ky_test.py bang importlib, goi bam_gate_nhanh()/bam_gate_registry() tren yaml.safe_load(.github/workflows/ci.yml). Tren ci.yml BASE: ra dung hai hang cu (301d30a2…, e2726e28…) => True/True. Tren ci.yml HEAD: BAM_GATE_NHANH=fe061a50668af83b6c9b6939f881ba37a30083bc72a27b52c2e02350835d626b, BAM_GATE_REGISTRY=89516cf77c3ce734feadf348bfea8180254c67e8e8ec62a48e2f6ea1dc038452"}
  - {name: "N3 actionlint", status: passed, evidence: "rc 0 base va head tren ci.yml + ci-dot-bien-du.yml; shellcheck VANG"}
  - {name: "N4 .claude/dev/ci_dang_ky_test.py", status: passed, evidence: "PHAN CHUNG 1070/1070 do dung · TONG: DAT (cuc bo, khong --chay); p651-M4-yaml-tho-timeout-trung con rang vi literal 150 khop ci-dot-bien-du.yml"}
  - {name: "N4 ops/ci_duong_nhanh_test.py", status: passed, evidence: "CA: 104/104 · DOT BIEN: 392/392 bi giet dung ly do · TONG: DAT (cuc bo)"}
  - {name: "N5 ci.yml pull_request", status: passed, evidence: "run 40151191903 success; check-run tren a7da463: 25 success + 1 skipped; mergeable_state clean"}
  - {name: "N5 ci-dot-bien-du.yml dispatch", status: not_run, evidence: "chu kho chon 'Ghi not_run' (ghi ho #910 issuecomment-6392213155): ngan sach phut runner (dot-bien-du 150 + 8 manh x 360); lich tuan thu Bay 19:17 UTC chay sau merge"}
  - {name: "Codex cross-review luot 1/2", status: passed, evidence: "launcher run 55874d0034204bca8412b6d49bd7eac0, ma_thoat 0, 597.3 s, prompt_sha256 b9663c46… = sha256 tep prompt; approve tren a7da463, P0=P1=P2=P3=0; model gpt-6.1-sol xhigh theo header CLI (model THUC phuc vu KHONG_DO_DUOC). Trong sandbox reviewer, ci_duong_nhanh_test 103/104 + 387/392 DO giong het base (socket bi chan), delta 0. Ban chep ops/reviews/wp910-g3-luot1-*. Da dung 1/2."}
  - {name: "Codex connector GitHub", status: passed, evidence: "comment 6392221290 tren PR #917: Completed tren a7da463, has_any_findings false"}
test_selection:
  gate_tier: T2
  selector_policy_sha: null
  tested_sha: a7da46390177cdc2d64f516dedac19857bee86dd
  selected_groups: [ci_dang_ky_test, ci_duong_nhanh_test, actionlint, ci_yml_pr]
  full_fallback_reason: "spec muc Tieu chi"
remaining_work:
  - "merge do chu kho; sau merge: ghi so land + rut han wp910-r3-g3-claude (packet dong sau pha B)"
  - "ngoai packet (Q5, Codex H2): ca t9 cua .claude/dev/chay-cong-windows_test.ps1 doi HanGiay 6300 >= max(timeout gate*)*60 = 9000 — DIEU KIEN DA SAI TREN BASE (tu khi gate-cong-cu len 150), khong do ban va nay; reviewer chi doi chieu dieu kien, KHONG chay PowerShell nen chua biet ca ay DO that khong"
  - "ngoai packet (Codex H3): chu thich con gia tri cu — ci_dang_ky_test.py:755 'nay 105', :804 'tran 30 phut'; ci.yml:953 '105 van co theo UBUNTU', :954 'gate/gate-packet-loop van 60' (cau cuoi da sai tu base); spec cam sua ngoai cac dong neu"
next_role: human
manual_next_action: "Chu kho xet merge PR #917; sau do ghi so land va rut han wp910-r3-g3-claude"
copyable_prompt: null
failure:
  fingerprint: null
  category: null
successors: []
```
