# Handoff wp886 — executor claude, lease `wp886-r2-g2-claude` (revision 2)

Bản CUỐI — PR #888 đã được chủ kho merge 2026-10-24T03:01:16Z (head `99b354c`). Nguồn sự thật: spec r1 `ops/specs/wp886.md`
(sha256 `28d1bb708621c6d410aa2f22ba11f295a5a9407d74d7aa736ddd30421e4f96a6`) + delta r2 `ops/specs/wp886-r2.md`
(sha256 `c019dbbacf838cddac40da8b360a0564c9383a10a07821735a7f3366ef72d68b`), lease `ops/leases/wp886-r2-g2-claude.yaml`
(13f61a5). Lịch sử r1: `ops/handoff/wp886-g1-claude.md` trên `ops/wp886-r1-g1-lease`.

```yaml
schema_version: 1
packet_id: wp886
generation: 2
spec_hash: c019dbbacf838cddac40da8b360a0564c9383a10a07821735a7f3366ef72d68b
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_01FLVLxi5gKZgtVvbuTCEqEn
base_sha: e63961f27b53e66db8e6600009f97d5706743063
head_sha: 99b354ca7bcc40ce0c4f7d9db445b852510b5809     # PR #888 MERGED boi ducthangho 2026-10-24T03:01:16Z
status: done
summary: >-
  r2: merge master truoc (76cf4c5 / #895 doi ops/cong_cu_test.py nhung khong cham fixture), roi sua CHI fixture
  python_alias_behavior_test: Windows tao `python3.cmd` goi sys.executable, POSIX giu symlink `python3`. Ly do .cmd thay
  symlink python3.exe: fixture cu chua bao gio CHAY symlink (checker dung sys.executable); nay probe chay that tep tim
  duoc tren PATH, ma chay python.exe qua symlink tren Windows CHUA DO (co the khong thay DLL/stdlib canh link); .cmd goi
  duong dan tuyet doi va khong can dac quyen symlink. Phien dieu phoi xac nhan .cmd nam trong r2 (spec ghi `tep co duoi
  PATHEXT`), dieu kien do that tren windows-latest.
changed_paths: [ops/cong_cu.py, ops/cong_cu_test.py, .claude/dev/launcher_test.py, scripts/tl_selftest.py,
                RELEASE_MANIFEST.json, changelog.d/wp-886.md]
tests:   # tren 99b354c tru khi ghi khac
  - {name: ci.yml pull_request (ubuntu), status: passed, evidence: "run 40050753537: 23/23 job success, nhan ubuntu-latest, head_sha 99b354c"}
  - {name: "N8 ci.yml runner_set=windows-only", status: passed, evidence: "run 40050767584: 15 success + 1 skipped (gate-cong-cu-gop chi Ubuntu); gate-cong-cu (windows-latest, 0): 'cong_cu_test: 59/59 dat; tong=61, bo qua=2, tien kiem bo qua=0' (t51/t48 gioi han nen, master cung bo qua); fixture CU do o run 39913747351"}
  - {name: launcher-windows.yml (workflow_dispatch), status: passed, evidence: "run 40050769532 success: 210/210 ca qua (bo qua 49); DOT BIEN 248/248 (77 khong do duoc tren Windows); wp886_cc_* do duoc deu OK"}
  - {name: tl.py --selftest, status: passed, evidence: "1731/1731 rc=0 (cuc bo, 1c138c7 — 99b354c chi doi .claude/dev/launcher_test.py); job gate Ubuntu run 40050753537 success"}
  - {name: release-verify --strict, status: passed, evidence: "ok=true, expected=checked=192"}
  - {name: ops/cong_cu_test.py (Linux), status: passed, evidence: "61/61, bo qua 0, tien kiem bo qua 0, cong cay that DAT; ban kinh 490 do o gate-cong-cu Ubuntu 8 manh (run 40050753537 success)"}
  - {name: dot bien wp886, status: passed, evidence: "11/11 wp886_cc_* giet dung ca (Codex luot 3 tu dem AST: 11, 16/16 luot ca dich); khai '10' truoc do la SAI (luc ay chi co 9)"}
  - {name: ruff F delta, status: passed, evidence: "launcher_test 5=5; reviewer do 4399=4399 tren 4 tep"}
  - {name: Codex cross-review, status: passed, evidence: "luot 1 approve N1-N5 (883f685c, a9be582) · luot 2 pending, khong P0-P3 (cd636453, 1c138c7) · luot 3 APPROVE (a94adf40, 99b354c = head da merge). Verdict tren nhanh lease. Da dung 3/5 loi goi."}
  - {name: Codex connector P1 (discussion_r4360957322), status: passed, evidence: "fixture python3.cmd, xanh Windows; tra loi + resolve"}
test_selection:
  gate_tier: T3
  selector_policy_sha: null
  tested_sha: 99b354ca7bcc40ce0c4f7d9db445b852510b5809
  selected_groups: [ci_yml_pr, ci_yml_windows_only, launcher_windows, cong_cu_test, tl_selftest, release_verify, launcher_test_wp886]
  full_fallback_reason: "spec muc Cong"
remaining_work:
  - "master tien toi 2c11396 sau khi review (chi CLAUDE.md + ops/land/**, khong cham 6 tep PR) — merge do chu kho, khong xung dot"
  - "ngoai packet: cong_cu.yaml dong 25-26 con chu thich mo ta no python-probe-khong-theo-PATH (Q2 cam sua yaml) — nay loi thoi"
  - "ngoai packet: buoc `cai_cong_cu.sh shellcheck` tren Windows tung do thoang qua (run 40048563126: shellcheck vang tren runner, choco cai cham); tu het o run 40050767584"
next_role: land_operator
manual_next_action: "Ghi so land PR #888 (merge commit tren master) va rut han wp886-r2-g2-claude"
copyable_prompt: null
failure:
  fingerprint: null
  category: null
successors: []
```
