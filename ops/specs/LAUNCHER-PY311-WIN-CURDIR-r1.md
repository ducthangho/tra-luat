tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-PY311-WIN-CURDIR r1 — launcher không được gọi API riêng chỉ có từ Python 3.12

- packet_id: LAUNCHER-PY311-WIN-CURDIR; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #1345 |
| `nguon_cap_viec` | Hồi quy của #1335 (PR #1341, `7acd29e`), phiên điều phối #1206 phát hiện; chỉ đạo đứng của chủ kho "triển khai liên tục" (#1206 issuecomment-6918292696). |
| `review_class` | `sensitive` (đường phóng agent) |
| `base` | nhánh mặc định lúc cấp lease |

## 0. Vấn đề (đo 16-11-2026)

Lane `launcher` (workflow `launcher-windows.yml`), run 43910313973 trên push `7acd29e`, job `launcher (ubuntu-latest)` chạy Python 3.11.18: `HONG r1335_F6_windows_chon_tep_theo_which` và `HONG r1335_P2_windows_bo_ung_vien_khong_duoi`, cùng `AttributeError: module 'shutil' has no attribute '_win_path_needs_curdir'`; tổng `406/408 … hong 2`. `.claude/dev/launcher.py:292` gọi thẳng `shutil._win_path_needs_curdir(s, os.F_OK | os.X_OK)`. Hàm riêng này chỉ có từ Python 3.12; Python 3.11 trên Windows sẽ ném lỗi ngay khi launcher chọn tệp thực thi. Cổng `gate` chạy 3.12 nên không bắt được.

## 1. `write_set`

```
.claude/dev/launcher.py
```

## 2. `ngoai_pham_vi`

Không sửa `.claude/dev/launcher_test.py` (đang thuộc lease `wp1336-r2-g1-claude`). Không đổi hành vi trên Python 3.12+.

## 3. `muc_tieu`

| # | mục tiêu |
|---|---|
| M1 | Lấy hàm bằng `getattr(shutil, "_win_path_needs_curdir", None)`. Không có thì dùng ngữ nghĩa của `shutil.which` Python 3.11 trên Windows: LUÔN xét cwd của tiến trình con trước PATH (3.11 chèn `os.curdir` vô điều kiện). Ghi chú thích kèm bằng chứng (phiên bản, dòng mã thư viện đã đọc). Rà toàn tệp xem còn chỗ nào gọi API riêng của `shutil`/`os` không có trên 3.11 thì sửa cùng lớp. |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Với `/usr/bin/python3.11`: `launcher_test.py --lap-ca` cho `r1335_F6_windows_chon_tep_theo_which` và `r1335_P2_windows_bo_ung_vien_khong_duoi` đều qua; trên base hai ca này ĐỎ (vế âm). | Quay về gọi thẳng `shutil._win_path_needs_curdir` ⇒ đỏ trên 3.11. |
| N2 | Với Python 3.12 và 3.13: 11 ca `r1335_*` qua (`--lap-ca` từng ca) và `t117` qua. | — |
| N3 | Ruff `--select F` delta 0; `adr-song`, `doctrine-scan` rc 0. | — |
| N4 | CI: lane `launcher` xanh trên Ubuntu 3.11 sau merge (đo hậu merge). | — |

Không chạy full suite, không chạy Windows (chỉ đạo chủ kho).

## 5. Kích thước và trần

1 tệp, dự kiến ≤ 15 dòng thêm. Trần `ADR-0053`: ≤ 450.

## 6. `luat_dung`

Cần sửa test thì DỪNG và báo (tệp test đang bị lease khác giữ).

## 7. `chua_do_duoc`

Windows thật với Python 3.11: không đo (chỉ đạo chủ kho không chạy Windows); chỉ đo bằng bộ mô phỏng `_r1335_win` trên Linux 3.11.
