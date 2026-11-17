tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-DOT-BIEN-R1335-THEO-NEN r1 — đột biến r1335 tương đương trên Windows phải khai theo nền, và có cặp đột biến riêng cho Windows

- packet_id: LAUNCHER-DOT-BIEN-R1335-THEO-NEN; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #1356 |
| `nguon_cap_viec` | Chủ kho yêu cầu 17-11-2026 ("Mở packet sửa hai đột biến r1335 sống trên Windows"); nợ phát hiện ở hồ sơ land #1336 (PR #1355). |
| `review_class` | `sensitive` (bảng đột biến của đường phóng agent) |
| `base` | nhánh mặc định lúc cấp lease |

## 0. Vấn đề (đo 17-11-2026)

Lane `launcher (windows-latest)` trên `7acd29e` (run 43910313973), `e4cce23` (43975814821), `866e522` (44003367352): `r1335_N3c_phong_lenh_goc SAI giet 0/1` và `r1335_F2_path_theo_cwd_launcher SAI giet 0/1`. Nguyên nhân đọc từ mã trên base:
- N3c bỏ `executable=exe` ở lời gọi `_phong` của `lenh_run`; trên Windows dòng ngay trước (`if exe and platform.system() == "Windows": lenh_con[0], exe = exe, None`) đã đặt `exe = None` ⇒ đột biến TƯƠNG ĐƯƠNG trên Windows.
- F2 sửa dòng `os.path.join(cwd, d or ".", s) for d` của nhánh POSIX trong `_thuc_thi`; Windows đi nhánh riêng ⇒ TƯƠNG ĐƯƠNG trên Windows.
Runner đột biến của `launcher_test.py` đã có cơ chế phần tử thứ tư `('posix'|'windows', lý do)` ⇒ in `KHONG DO DUOC tren nen nay` thay cho `SAI`.

## 1. `write_set`

```
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

Không sửa `.claude/dev/launcher.py`. Không đổi ca `r1335_*` nào ngoài việc cần thiết để đột biến Windows mới bị giết đúng lý do (nếu cần sửa ca, DỪNG và báo trước).

## 3. `muc_tieu`

| # | mục tiêu |
|---|---|
| M1 | Hai đột biến `r1335_N3c_phong_lenh_goc`, `r1335_F2_path_theo_cwd_launcher` mang phần tử thứ tư `('posix', <lý do nêu dòng mã làm nó tương đương trên Windows>)`. |
| M2 | Thêm đột biến chỉ-Windows `('windows', lý do)` bỏ việc thay `argv[0]` trên Windows (dòng `if exe and platform.system() == "Windows": lenh_con[0], exe = exe, None`), đích `r1335_symlink_doi_dich_giua_bam_va_phong`. |
| M3 | Thêm đột biến chỉ-Windows bỏ neo PATH theo cwd con ở nhánh Windows của `_thuc_thi` (phần `os.path.join(cwd, d or ".") for d in p.split(os.pathsep)`), đích `r1335_khac_cwd_bam_va_chay_tep_trong_workspace`. |
| M4 | Văn bản đích của mỗi đột biến mới khớp ĐÚNG MỘT chỗ trong `launcher.py` (t117 xanh). |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux: hai đột biến M1 vẫn giết đúng ca đích; hai đột biến M2/M3 in `KHONG DO DUOC tren nen nay`. `t117` xanh. | Bỏ phần tử thứ tư ở M1 ⇒ không đổi trên Linux (đúng); gắn nhầm `'windows'` cho M1 ⇒ Linux in KHONG DO DUOC (sai). |
| N2 | Windows (máy Desktop/VM của chủ kho, do phiên điều phối chạy): bốn đột biến trên chạy trong runner đột biến — M1 in `KHONG DO DUOC`, M2/M3 `OK giet 1/1` đúng ca đích. | Đột biến M2/M3 sống ⇒ đỏ. |
| N3 | Ruff `--select F` delta 0; `adr-song`, `doctrine-scan` rc 0. | — |
| N4 | Hậu merge: lane `launcher (windows-latest)` không còn dòng `SAI` cho đột biến `r1335_*`. | Còn `SAI`. |

Chỉ chạy test nhắm đích (`--lap-ca`, chạy đột biến theo tên); không chạy trọn suite.

## 5. Kích thước và trần

1 tệp, dự kiến ≤ 30 dòng thêm. Trần `ADR-0053`: ≤ 450.

## 6. `luat_dung`

Đột biến M2/M3 không giết được ca đích trên Windows mà không sửa ca ⇒ DỪNG, báo kèm log, không tự sửa ca.

## 7. `chua_do_duoc`

Executor không có Windows; N2 do phiên điều phối đo trên máy Windows của chủ kho trước merge; N4 đo hậu merge.
