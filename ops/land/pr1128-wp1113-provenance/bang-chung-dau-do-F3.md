# Bằng chứng phép đo đầu dò — packet #1113 CI-LAN-LUU-TRU r1 (F3)

- Nền: `591cc9d30e055b182e5f39c9e1e6c513170dc7cd` (= master 3bdd987 + commit CI của packet; không đổi dữ liệu hồ sơ). Clone: `/tmp/claude-0/-home-user-tra-luat/5c67d48b-5184-57a4-9f0f-4851929521d8/scratchpad/dd-nen`.
- Nền + DO1–DO6: `2a8d20dbdf9bfc2a63e62d1dd11d0663f1acc68b` (một commit trên nền, dựng bằng `/tmp/claude-0/-home-user-tra-luat/5c67d48b-5184-57a4-9f0f-4851929521d8/scratchpad/dau_do.py`). Clone: `/tmp/claude-0/-home-user-tra-luat/5c67d48b-5184-57a4-9f0f-4851929521d8/scratchpad/dd-daudo`.
  Nội dung đầu dò: `git -C /tmp/claude-0/-home-user-tra-luat/5c67d48b-5184-57a4-9f0f-4851929521d8/scratchpad/dd-daudo show --stat 2a8d20db`. Lượt đo bắt đầu SAU commit 12:40:15Z (thời điểm tạo log, reflog).
- Lệnh: `run:` của chính bước trong `.github/workflows/ci.yml` của cây đo (`python`→`python3`), `core.abbrev=7` cấp repo.

| Bước / bộ | Nền rc | Đầu dò rc | Ghi chú dương | Nguồn |
|---|---|---|---|---|
| gate · bundled-fragment check (topology gói) | 0 | 0 | 5.6s / 5.1s | `kq5-*.json, tlst-dd-*.log` |
| gate · gen_instructions selftest | 0 | 0 | 0.1s / 0.1s | `kq5-*.json, tlst-dd-*.log` |
| gate · tl selftest (luot PR — khong sinh bang chung) | 0 | 0 | 1774/1774 (log tlst-dd-*.log; lượt giàn rc=1 do GIT_CONFIG_PARAMETERS đè r226, chạy lại không đè) | `kq5-*.json, tlst-dd-*.log` |
| gate · workflow-audit strict | 0 | 0 | 0.3s / 0.3s | `kq5-*.json, tlst-dd-*.log` |
| gate · golden-test | 0 | 0 | 12.3s / 12.8s | `kq5-*.json, tlst-dd-*.log` |
| gate · determinism-audit strict | 0 | 0 | 18.6s / 18.5s | `kq5-*.json, tlst-dd-*.log` |
| gate · ci-phamvi guard (bang phu thuoc khop ma) | 0 | 0 | 0.5s / 0.5s | `kq5-*.json, tlst-dd-*.log` |
| gate · release-check full | 0 | 0 | 1.6s / 1.7s | `kq5-*.json, tlst-dd-*.log` |
| gate · release-verify strict (lane LAND — manifest committed) | 0 | 0 | 0.9s / 0.8s | `kq5-*.json, tlst-dd-*.log` |
| gate · release-verify strict (lane WORKER — manifest TẠM ngoài repo) | 0 | 0 | 1.9s / 1.9s | `kq5-*.json, tlst-dd-*.log` |
| gate · tl_boot smoke | 0 | 0 | 0.6s / 0.6s | `kq5-*.json, tlst-dd-*.log` |
| gate/G5 kiem ban ke | 0 | 0 | 360.0s / 359.9s | `kq4-*.json` |
| G5 probe | 0 | 0 | 0.3s / 0.3s | `kq4-*.json` |
| PR head EOL base | 0 | 0 | 0.1s / 0.1s | `kq4-*.json` |
| py_compile | 0 | 0 | 0.6s / 0.6s | `kq4-*.json` |
| release-bundle x2 | 0 | 0 | 4.6s / 4.3s | `kq4-*.json` |
| don-nhanh selftest | 0 | 0 | 26.4s / 26.5s | `kq4-*.json` |
| nhanh_don_duoc mảnh 0..7 + gộp | 0 | 0 | mảnh 1..7 trong kq4 (42/42 mỗi mảnh), mảnh 0 + gộp chạy bù: 'targeted_mutant_gate: DAT' | `kq4-*.json, m0-dd-*.log, gop-dd-*.log` |
| packet-loop selftest | 0 | 0 | 3666.1s / 3665.8s | `kq4-*-pl.json` |
| registry · ops/land_evidence_nguon_test.py | 0 | 1 | ĐỔI MÀU: DO4 → kiem-re kiem_land_evidence | `kq-*2.json` |
| registry · ops/kiem_ho_so_land_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · ops/cloud_agent_creds_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · ops/kiem_nhan_hint_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · ops/ci_provenance_test.py | 1 | 1 | lượt bộ: đỏ cả hai, cùng tập ca (môi trường: Ruff 0.16.9 / thiếu shellcheck). Sau khi sửa môi trường, các ca đỏ (guard t11/t15/t33, provenance c61) chạy lại TRÊN CẢ HAI cây ⇒ True (ca4-dd-*.log) | `kq-*2.json` |
| registry · ops/codex_cloud_setup_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · .claude/hooks/pretooluse_guard_test.py | 1 | 1 | lượt bộ: đỏ cả hai, cùng tập ca (môi trường: Ruff 0.16.9 / thiếu shellcheck). Sau khi sửa môi trường, các ca đỏ (guard t11/t15/t33, provenance c61) chạy lại TRÊN CẢ HAI cây ⇒ True (ca4-dd-*.log) | `kq-*2.json` |
| registry · .claude/hooks/subagent_ghi_detect_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · .claude/dev/codex_cred_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · .claude/dev/idiom_py_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · .githooks/eol_policy_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · .githooks/pre_push_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · .github/checks/ci_phamvi_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · scripts/tl_core/command_registry_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · .claude/dev/gate_lifecycle_test.py | 0 | 0 |  | `kq-*2.json` |
| registry · ops/lease_publish_test.py | 0 | 1 | ĐỔI MÀU: DO1/DO2/DO3 → kiem-re CA_DU_LIEU t23/t26/t27 | `kq-*3.json` |

Tập cho phép (validator đường nhanh) theo từng đầu dò: `kq-chophep.log` (DO1–DO3) và ca `t56` (DO1–DO6 trên worktree kho thật, chạy được).

## Bổ sung sau review offline lượt 4 (lớp BỌC, không thay bằng bộ con)
| Bước | Nền rc | Đầu dò rc | Ghi chú dương | Nguồn |
|---|---|---|---|---|
| gate · tl selftest (co bang chung exact-identity) — chạy NGUYÊN `run:` (`gate_lifecycle.py run --require-clean`, `RUNNER_OS=Linux`) | 0 | 0 | `"status": "pass"`, 1774/1774, head_sha đúng hai OID, base_sha 3bdd987 | `exact-dd-*.log` (cây đầu dò chạy lại tuần tự: lượt song song trả `busy` do khoá một heavy gate/máy) |
| gate-ops · gate lifecycle selftest (nen khong co cgroup) — `run:` NGUYÊN VĂN là `python .claude/dev/gate_lifecycle_test.py` | 0 | 0 | cùng lệnh với dòng registry `gate_lifecycle_test.py` | `kq-*2.json` |
| gate-ops · bo ca gate chay TRONG cgroup duoc uy quyen (Linux) | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC | container ở cgroup gốc `/` ⇒ chính bước `exit 1` "KHONG uy quyen duoc"; bảng khai `chua_do` | `/proc/self/cgroup` |
