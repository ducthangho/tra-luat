# Handoff wp886 — executor claude, lease `wp886-r2-g2-claude` (revision 2)

Bản TẠM, cập nhật theo tiến độ. Nguồn sự thật: spec r1 `ops/specs/wp886.md`
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
head_sha: 1c138c714f9c192ea730b65c5d18ff5eda1ca660     # PR #888; da merge master 33e6d4c (gom #881, #895)
status: needs_followup
summary: >-
  r2: merge master truoc (76cf4c5 / #895 doi ops/cong_cu_test.py nhung khong cham fixture), roi sua CHI fixture
  python_alias_behavior_test: Windows tao `python3.cmd` goi sys.executable, POSIX giu symlink `python3`. Ly do .cmd thay
  symlink python3.exe: fixture cu chua bao gio CHAY symlink (checker dung sys.executable); nay probe chay that tep tim
  duoc tren PATH, ma chay python.exe qua symlink tren Windows CHUA DO (co the khong thay DLL/stdlib canh link); .cmd goi
  duong dan tuyet doi va khong can dac quyen symlink. Phien dieu phoi xac nhan .cmd nam trong r2 (spec ghi `tep co duoi
  PATHEXT`), dieu kien do that tren windows-latest.
changed_paths: [ops/cong_cu.py, ops/cong_cu_test.py, .claude/dev/launcher_test.py, scripts/tl_selftest.py,
                RELEASE_MANIFEST.json, changelog.d/wp-886.md]
tests:   # tren 1c138c7 (Linux) tru khi ghi khac
  - {name: release-verify --strict, status: passed, evidence: "ok=true, expected=checked=192"}
  - {name: ops/cong_cu_test.py, status: passed, evidence: "61/61, bo qua 0, tien kiem bo qua 0, cong cay that DAT; ban kinh 490 dot bien: dang chay"}
  - {name: tl.py --selftest, status: passed, evidence: "1731/1731 rc=0 (so bo: changelog doi giua luot; se chay lai tren head cuoi)"}
  - {name: dot bien wp886 (rieng), status: passed, evidence: "10/10 giet dung ca bang TinHieuChotCa (them wp886_cc_bo_muc_PATH_rong, 7ce1b02)"}
  - {name: N8 phan chung, status: passed, evidence: "fixture CU (python3 khong duoi) DO tren windows-latest that: run 39913747351, TinHieuChotCa 'may chi co python3 bi probe alias python chan: rc=3'"}
  - {name: N8 ci.yml runner_set=windows-only, status: not_run, evidence: "run 40048563126 dang chay gate-cong-cu (windows-latest, 0)"}
  - {name: ci.yml windows — gate / gate-packet-loop, status: failed, evidence: "run 40048563126: DO o buoc `cai_cong_cu.sh shellcheck` (shellcheck vang tren runner: FileNotFoundError; luot truoc 39913747351 co san 0.9.0 trong 18s) — khong do diff; se chay lai mot lan khi run xong. PR comment issuecomment-6378021629"}
  - {name: Codex cross-review, status: passed, evidence: "luot 1/5 run 883f685c head a9be582: approve pham vi N1-N5, khong P0-P3 moi (verdict tren ops/wp886-r1-g1-lease df4620f)"}
test_selection:
  gate_tier: T3
  selector_policy_sha: null
  tested_sha: 1c138c714f9c192ea730b65c5d18ff5eda1ca660
  selected_groups: [cong_cu_test, tl_selftest, release_verify, launcher_test_wp886]
  full_fallback_reason: "spec muc Cong"
remaining_work:
  - "N8: gate-cong-cu (windows-latest, 0) XANH tren head cuoi; resolve thread P1 discussion_r4360957322"
  - "chay lai mot lan cac job Windows do o buoc shellcheck de xac nhan khong thuoc PR"
  - "ci.yml Ubuntu xanh tren head cuoi; launcher-windows.yml dispatch mot lan"
  - "Codex luot 2+ tren head cuoi toi khi het P1/P2/P3 (con 4/5)"
  - "tl.py --selftest lai tren head cuoi"
next_role: executor
manual_next_action: null
copyable_prompt: null
failure:
  fingerprint: null
  category: null
successors: []
```
