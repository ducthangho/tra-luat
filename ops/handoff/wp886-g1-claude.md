# Handoff wp886 — executor claude, lease `wp886-r1-g1-claude`

Bản TẠM. Executor dừng ở r1 theo quyết định chủ kho **"Chọn A"** (ghi hộ:
https://github.com/ducthangho/tra-luat/issues/886#issuecomment-6359482987). Việc còn lại chờ revision r2.

Nguồn sự thật: spec `ops/specs/wp886.md` @ `ops/wp886-spec` 9226472 (sha256
`28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6`), lease `ops/leases/wp886-r1-g1-claude.yaml` (3f90105).

```yaml
schema_version: 1
packet_id: wp886
generation: 1
spec_hash: 28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_01FLVLxi5gKZgtVvbuTCEqEn
base_sha: e63961f27b53e66db8e6600009f97d5706743063
head_sha: efa6e8d6b1dc3f1eafff5aaad492dae055a5d784     # PR #888 (draft)
status: blocked
summary: >-
  ops/cong_cu.py giai `python` theo PATH dung thu tu cai_cong_cu.sh (TEN_PYTHON: python -> python3 -> py -3), luat
  native nhu _ten_tran_giai_ra (Windows chi nhan duoi PATHEXT); khong ten nao => KHONG_DO_DUOC kem ten thieu, khong roi
  ve sys.executable. Ca r886_n1..n4, n6 (tinh, moi nen), r886_ten_python_khop_cai_cong_cu_sh; r858_cai_python nang ve
  N1/N3 day du; 8 dot bien wp886_cc_* tren dich moi "cong_cu". BLOCKED: ops/cong_cu_test.py (ngoai write set, lease
  wp879-r1-g1-claude) do tren Windows o tien kiem python_alias_behavior_test vi fixture symlink `python3` KHONG DUOI —
  dung xung dot spec da luong truoc; chu kho chon A (revision r2 sua fixture).
changed_paths: [ops/cong_cu.py, .claude/dev/launcher_test.py, scripts/tl_selftest.py, RELEASE_MANIFEST.json,
                changelog.d/wp-886.md]
tests:   # tren efa6e8d (Linux, container remote) tru khi ghi khac
  - {name: launcher_test, status: passed, evidence: "nen e63961f 250/250 (tong 252, bo qua 2) · head 256/256 (tong 258, bo qua 2), CA HAI che do co/khong CODEX_AUTH_JSON gia; hai ve dung trong MOT lenh (scratchpad ab/run.sh); delta do moi = 0"}
  - {name: phan chung tren nen e63961f, status: passed, evidence: "r886_n1/n2/n3/n4 + r858_cai_python DO bang TinHieuChotCa voi cong_cu.py cua nen; n6/Q1 khong nap duoc API moi (AttributeError, du kien)"}
  - {name: dot bien wp886 (rieng), status: passed, evidence: "9/9 giet dung ca dich bang TinHieuChotCa: 8 wp886_cc_* + wp858_yaml_python_linux_ve_dirname; moi dot bien co it nhat mot ca dich chay duoc tren Windows"}
  - {name: launcher_test --dot-bien (toan bo), status: not_run, evidence: "dang chay sau khi phien bi khoi dong lai; se cap nhat"}
  - {name: tl.py --selftest, status: passed, evidence: "1731/1731 rc=0"}
  - {name: release-verify --strict, status: passed, evidence: "ok=true, expected=checked=192"}
  - {name: ops/cong_cu_test.py (Linux), status: passed, evidence: "61/61, bo qua 0, tien kiem bo qua 0, cong cay that DAT, rc=0"}
  - {name: ruff F delta, status: passed, evidence: "cong_cu.py 1=1 · launcher_test 5=5 · tl_selftest 4392=4392 · tl.py 12=12"}
  - {name: doctrine-scan / doc-claims-check --strict, status: passed, evidence: "rc0 / rc0"}
  - {name: ci.yml PR (ubuntu), status: passed, evidence: "run 39913744298: gate, gate-ops, gate-packet-loop, gate-registry, gate-cong-cu 0..7 + gop, gate-nhanh-manh 0..7 + gop deu success"}
  - {name: ci.yml runner_set=windows-only, status: failed, evidence: "run 39913747351: gate + gate-cong-cu(0) DO o python_alias_behavior_test (CO CHU DICH, xem summary); gate-registry DO o ops/land_evidence_nguon_test.py 63/64 — do san tren master e63961f (run 39905884453 job 120258809916), khong thuoc PR"}
  - {name: launcher-windows.yml (workflow_dispatch), status: not_run, evidence: "cho head cuoi cua r2"}
  - {name: Codex cross-review, status: not_run, evidence: "0/5 loi goi; chu kho cam goi Codex trong luc cho r2"}
test_selection:
  gate_tier: T3
  selector_policy_sha: null
  tested_sha: efa6e8d6b1dc3f1eafff5aaad492dae055a5d784
  selected_groups: [launcher_test, cong_cu_test, tl_selftest, release_verify, ruff_F, doctrine_scan, doc_claims]
  full_fallback_reason: "spec muc Cong liet ke dich danh cac cong nay"
remaining_work:
  - "r2: cap lease sau khi wp879-r1-g1-claude het han (2026-10-24T01:22Z) hoac duoc rut han; dua ops/cong_cu_test.py vao write set; bia mo hai chieu cho wp886-r1-g1-claude"
  - "r2: sua fixture python_alias_behavior_test — ban NHAP do executor soan, CHUA commit: Windows dung `python3.cmd` goi sys.executable (symlink `python3.exe` CHUA DO: python co the khong thay DLL canh link); POSIX giu symlink `python3`. Linux voi ban nhap: xem dong cap nhat sau"
  - "r2: merge master (khong rebase), tai sinh RELEASE_MANIFEST + ratchet neu master tien"
  - "r2: ci.yml xanh tren head cuoi + windows-only (gate-cong-cu) + launcher-windows.yml dispatch MOT lan"
  - "r2: cross-review Codex (sandbox + PROMPT da soan cho r1, can sua neo head va them cau hoi fixture)"
  - "ngoai packet: cong_cu.yaml dong 25-26 con chu thich mo ta no `python-probe-khong-theo-PATH` (Q2 cam sua yaml) — se loi thoi khi packet land"
next_role: human
manual_next_action: "Phien dieu phoi soan spec wp886 r2 + cap lease r2 sau 2026-10-24T01:22Z"
copyable_prompt: null
failure:
  fingerprint: null
  category: content
successors: []
```

## Ghi chú vận hành
- Phiên executor bị khởi động lại một lần giữa chừng. Các cổng chạy nền đã xong TRƯỚC lúc khởi động lại; log nằm
  trong scratchpad của phiên (không bền).
- Lúc chuẩn bị bản nháp r2, bản `cong_cu_test.py` nháp bị chép nhầm vào clone đang chạy `--dot-bien` khoảng vài
  giây, rồi được hoàn nguyên ngay (`git checkout`; cây sạch ở `efa6e8d`). `launcher_test.py` không đọc `cong_cu_test.py`
  (chỉ nhắc trong chú thích), nên lượt đo ấy không bị ảnh hưởng.
- Nguồn bản sao kho trong container là clone NÔNG (`shallow roots` khi dựng mirror); head/base đủ để đo.
