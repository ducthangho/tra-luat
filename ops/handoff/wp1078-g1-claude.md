# Handoff wp1078 — executor `claude` (phiên cloud), 01-11-2026

- Packet #1078 `CAI-CONG-CU-PYTHON-HAM-KE-THUA` r1 · lease hiệu lực `ops/leases/wp1078-r1-g2-claude.yaml` (g2; g1 mang
  `da_bi_thay_the`) · đặc tả `ops/specs/wp1078.md`, sha256 `2fb1b2633ae09e4b737f97d601186389fd801cc294a5217ea07b3e761c3bf13b`.
- Nhánh `agent/wp1078-g1-claude`, PR #1097, head **`7f8be85a7cf9077400fc1747aa6e23128f087677`**. Diff so base `90c101b` đúng hai
  tệp (`git diff --numstat 90c101b..7f8be85`): `ops/cai_cong_cu.sh` +10/−7, `.claude/dev/launcher_test.py` +103/−5
  (tổng **+113/−12**). Không merge/land, không force-push.

## Quyết định của chủ kho trong packet (ghi hộ, băm byte KHÔNG ĐO ĐƯỢC)
| lease | quyết định |
|---|---|
| g2 | áp bản vá lượt 2 và nâng trần Codex 2→3; lượt 3 còn chặn thì dừng |

## Thay đổi
- `ops/cai_cong_cu.sh`: chọn Python bằng `type -P python` → `python3` → `py -3` (chỉ tệp trên PATH, hàm/alias/builtin
  kế thừa không được chọn); `PY[0]` không phải đường dẫn tuyệt đối thì thoát 4 — chốt áp cả nhánh dùng lại `PY` có sẵn.
- `.claude/dev/launcher_test.py`: ca `r831_cai_rg_{linux,macos}_python_ham_ke_thua`,
  `r1078_ham_python_khong_phai_python_khong_duoc_goi`, `r1078_hinh_dang_chon_python_bang_type_P`,
  `r1078_py_dung_lai_khong_tuyet_doi_phai_thoat_4` (4 biến thể môi trường); regex `r886` đọc dòng `type -P`; fixture
  `_wp831_chay_cai_rg` chép từ `CAI_SH_DANG_DUNG`; 4 đột biến `wp1078_*` (kind `cai_sh`).

## Nghiệm thu — đo trên `7f8be85`
- **A1** (Linux, phiên này, `/tmp/.git` vắng) `python3 .claude/dev/launcher_test.py`: `328/328` · `--dot-bien`: `522/522`; 4 đột
  biến `wp1078_*` giết đúng ca đích bằng assertion của chính ca.
- **A2** phản chứng trên base `90c101b`: cả 4 ca hành vi ĐỎ (ca M3: rc=0 mà `GITHUB_PATH` rỗng — hỏng mà xanh). Lệnh và output
  trong commit message `882cb50`.
- **A3** `cong_cu_test`: lượt tại chỗ bị cắt ở trần 1h của tác vụ nền — KHÔNG ĐO ĐƯỢC tại chỗ; bằng chứng là CI
  `gate-cong-cu (ubuntu-latest, 0..7)` + `gate-cong-cu-gop (ubuntu-latest)` success trên run `41268758209`.
- **A4** ruff F delta 0 · `bash -n ops/cai_cong_cu.sh` rc0 · `git diff --check` rc0 · `doctrine-scan` rc0.
  CI trên `7f8be85` (đọc check run qua REST, 41 run): 39 success, 2 skipped — `gate-cong-cu-gop` của lượt Windows (job loại
  Windows theo thiết kế) và `launcher (Windows that)` (lane `launcher-windows.yml`, không phải gate).
  Windows `workflow_dispatch` `runner_set=windows-only` run `41270527156`: 15 job nhãn `windows-latest`, `runner_id` khác 0, đều
  success; trong `gate (windows-latest)` bước 7 `cài shellcheck cho G5` và bước 8 `cài rg cho G5` (chạy `bash ops/cai_cong_cu.sh`)
  success. Giới hạn: `gate-cong-cu` trên Windows chỉ chạy mảnh 0 (bán kính đột biến chỉ đo trên Ubuntu).

## Cross-review Codex — 3/3 lời gọi (trần g2)
`launcher.py run ... -- codex exec -c model_reasoning_effort=xhigh --sandbox workspace-write`. Hiện vật nguyên byte ở
`ops/handoff/wp1078-g1-claude/luot{1..3}/` (PROMPT, VERDICT, HINT nếu có, run/{run.json,checkpoint.json,stdout.log,stderr.log})
kèm `SHA256SUMS`.

| lượt | run_id | head | thời lượng | model_phuc_vu | verdict | sha256 verdict |
|---|---|---|---|---|---|---|
| 1 | `bba0dc8891e34555b98a36dd0852a120` | `47b873a` | 929.618 s | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 0 P1, 2 P2, 0 P3) | `640b1878…8682a` |
| 2 | `9f526f63961d4532a5f3c0f04af497ec` | `0311db4` | 1091.401 s | DO_DUOC `gpt-6.1-sol` | changes_requested (0 P0, 0 P1, 1 P2, 0 P3) | `2003a88b…19fca97` |
| 3 | `57324dd939bf4ff4b5dd44fdcb05433d` | `7f8be85` | 1225.274 s | DO_DUOC `gpt-6.1-sol` | approve (0 P0, 0 P1, 0 P2, 0 P3) | `a28cc902…f392448` |

PR #1097: 0 review thread, 0 comment tại lúc ghi.

## Việc còn lại
- Merge/land: chủ kho (`uy_quyen_merge: false`).
- Sau merge: rút hạn lease g2 (nhả `launcher_test.py` cho #1079).
