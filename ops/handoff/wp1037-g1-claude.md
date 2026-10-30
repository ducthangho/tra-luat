# Handoff wp1037 g1 — executor `claude` (phiên cloud), 30-10-2026

- Packet #1037 `BIEN-NHAN-V2-TEST-IN-CHI-TIET-TIN-DUNG-GIA` r1 · lease `ops/leases/wp1037-r1-g1-claude.yaml` (đăng bởi run
  41029967015, xanh) · đặc tả `ops/specs/wp1037.md` @ `e16fb55`, sha256 `253f12ae9c7e68c57a153c1f0e89993f65bf303529ed3f2444ed769a909b3230`.
- Phiên ghi lease CŨNG là executor (chỉ thị chủ kho trong phiên `session_015GtxrYjGJtmjF3eT1nCSG9`).
- Nhánh `agent/wp1037-g1-claude`, PR draft #1041, head **`91466322f705658ed51b80c7c152f6b77f4f90c6`**. Diff đúng 1 tệp
  `ops/bien_nhan_v2_test.py` so base `757bde5`. Không merge/land, không force-push.

## Lịch sử nhánh
| commit | nội dung |
|---|---|
| `016852a` | `_vi_tri_nem`, `_dong_chi_tiet` (trần 2000), `_dong_ket_qua_dot_bien`, ca `c98` |
| `9146632` | vá Codex lượt 1: `_dot_bien(chi=…)` để `c98` đi qua thân `do()` thật + thu stdout; khoá trần mặc định và số dòng ném |

## Tiêu chí — đo trên `9146632`
- **A1 Linux**: `python3 ops/bien_nhan_v2_test.py` ⇒ `95/95 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`,
  `TỔNG: ĐẠT`. Windows: chưa đo trên head này (CI lượt PR chỉ Ubuntu).
- **A2** răng (bản sao đủ cây, `c98` qua `_chay_1`): 11/11 đột biến `giet_that` đúng chốt — bỏ vị trí ném · chi tiết luôn rỗng ·
  dây nối mất chi tiết · bỏ trần · chỉ dòng đầu · in cả khi đạt · `do()` quay về `print` cũ · số dòng = 0 · trần mặc định vô hạn ·
  khung ngoài cùng · bỏ bộ lọc `chi`. Đối chứng `qua`.
- **A3** mô phỏng ca laptop (m81 → c74 ném `AttributeError`): log in `chi tiết [tin_dung_gia]:` + `AttributeError: … [ném tại
  bien_nhan_v2_test.py:<dòng> in <hàm>]`; phân hạng `tin_dung_gia`, rc=1 giữ nguyên.
- **A4** ruff F: 1 F541 cả base lẫn head ⇒ delta 0 · `git diff --check` rc0 · `doctrine-scan` rc0 · `bien_nhan_v2 --root .`
  `TỔNG: ĐẠT`. CI lượt PR: xem check run của head trên PR #1041.

## Cross-review Codex — 2/2 lời gọi (trần lease)
`launcher.py run ... -- codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh --sandbox workspace-write`. Hiện vật nguyên byte ở
`ops/handoff/wp1037-g1-claude/` (SHA256SUMS kèm).

| lượt | run_id | head | thời lượng | model_phuc_vu | verdict | sha256 verdict |
|---|---|---|---|---|---|---|
| 1 | `4d0668e2f3d045ef86354bea2a6afd29` | `016852a` | 934.249 s, rc0 | `gpt-6-astra` 27/27 | request_changes (1 P2, 2 P3) | `e33a3c3e…f2a95b` |
| 2 | `e400a3206474480f827b771e59395389` | `9146632` | 567.318 s, rc0 | `gpt-6-astra` 19/19 | **approve** (0/0/0/0) | `2f482565…49feaf` |

Lượt 2 ghi năm đột biến của mã test còn SỐNG qua `c98`, xếp là giới hạn độ phủ (không phải finding): bỏ khôi phục `CA[i]` (lời
gọi thứ hai gán lại che lần thứ nhất) · bỏ khôi phục `_CA` ngoài (`_chay_1` ngoài cùng xoá `_CA`) · bỏ chốt đếm số dòng khi đạt
(chỉ xoá chốt) · thêm dòng + xoá chốt (phản chứng kép) · `main` chỉ chạy m81 (đo bằng so log head/base, không qua `c98`).

## Windows — đo trên `9146632`
`workflow_dispatch` `runner_set=windows-only`, run 41069257658:
- attempt 1: job `gate-ops (windows-latest)` (124108765783) ⇒ `bien_nhan_v2_test: 95/95 ca đạt · 137/137 đột biến thường CÓ RĂNG ·
  2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`; `lease_publish: 255/255 đạt` (bỏ qua 13 ca chỉ-Ubuntu). Hai job `gate-packet-loop` và
  `gate-cong-cu (windows-latest, 0)` ĐỎ ở bước `G5 probe` vì runner thiếu shellcheck — gốc lỗi ở `ops/cai_cong_cu.sh` (bộ chọn tin
  rc của `kiem-tra --chi`), ngoài write set; tách thành packet #1045 (PR #1047). Comment PR #1041 issuecomment-6524864187.
- attempt 2 (`rerun_failed_jobs` một lần, 15:28Z): cả hai job XANH; toàn run `conclusion: success`, 15/15 job Windows xanh.

## Việc còn lại
- Lần sau `bien_nhan_v2_test` có `tin_dung_gia` trên laptop, log sẽ mang ngoại lệ + vị trí.
- Merge/land: chủ kho (`uy_quyen_merge: false`).
