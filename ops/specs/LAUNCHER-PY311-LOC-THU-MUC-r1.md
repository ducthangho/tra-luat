tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-PY311-LOC-THU-MUC r1 — ca canh bộ lọc "kết quả phải nằm trong d" của `_ShutilWin311.which`

- packet_id: LAUNCHER-PY311-LOC-THU-MUC; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #1375 |
| `nguon_cap_viec` | Nợ ghi khi land #1345 (comment chủ kho trên #1345, 2026-11-17T03:07:50Z): "chưa có ca canh bộ lọc 'kết quả phải nằm trong `d`' của nhánh 3.11". Chủ kho 17-11-2026 (phiên điều phối #1206) chọn làm ngay khoản nợ này. |
| `review_class` | `sensitive`: `.claude/dev/launcher_test.py` không khớp mục tường minh nào trong `_BANG_LOP`, nhận lớp mặc định fail-closed từ `_tinh_lop_tu_write_set` (review độc lập lượt 1, F3). Đối chiếu lại bằng `lease_publish check` khi cấp lease; không hạ lớp vì diff nhỏ. |
| `base` | `39ce682b42fe82bb6a0fd66c4d81c08961598f98` lúc soạn; lease ghi OID base thật lúc cấp. |

## 0. Hiện trạng (đo 2026-11-17T12:47:10Z trên `39ce682`, Linux, Python 3.13.18)

- `.claude/dev/launcher.py` dòng 275–290: lớp `_ShutilWin311` (wp1345) thay `shutil` khi Python < 3.12 trong `_thuc_thi` (dòng 302). `which(cmd)` tách `d, ten = os.path.split(cmd)`, gọi `shutil.which(ten, path=d + os.pathsep + os.curdir)` rồi CHỈ nhận kết quả khi `os.path.normpath(os.path.dirname(u)) == os.path.normpath(d)` (dòng 289–290).
- Đo hành vi trên Linux (gọi thẳng lớp): thư mục `d` rỗng, thư mục làm việc của tiến trình có tệp thực thi `foo` ⇒ `which(<d>/foo)` trả `None`; cùng phép gọi khi bỏ bộ lọc (trả thẳng `shutil.which(...)`) ⇒ `./foo` — tức nhận nhầm tệp ở cwd của LAUNCHER; `d` có `foo` ⇒ trả `<d>/foo`.
- `.claude/dev/launcher_test.py`: 0 dòng nhắc `_ShutilWin311` (đo `grep -c`); bảng đột biến `DOT_BIEN` (dòng 14590) khai `(tên, (tìm, thay), [ca đích])`; ca đăng ký bằng decorator ghi vào `CA` (dòng 55, 71). Runner `DOT_BIEN` (khoảng 16994–17057) áp đột biến lên BẢN SAO của `launcher.py` và đổi `LAUNCHER_DANG_DUNG`; ca muốn thấy bản đột biến phải nạp qua `_tai_launcher_thu()` (dòng 335–337). Chỉ `TinHieuChotCa` của đúng ca (phát qua `bang(...)`, dòng 193) được tính là GIẾT; `assert` thường tính là `loi` (dòng 222–239). Runner chạy ca tuần tự trong cùng tiến trình; thiếu ca đích thì báo `SAI - ca dich khong tim thay/trung` (dòng 17046–17050).

## 1. `write_set`

```
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- Không sửa `.claude/dev/launcher.py` (bộ lọc đã đúng; packet chỉ thêm răng).
- Không CI Windows, không đo native Windows: ca là ca thuần gọi thẳng lớp, chạy mọi nền.
- Không đổi đột biến hiện có trong `DOT_BIEN`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Một ca mới `r1375_shutilwin311_chi_nhan_trong_d` (đăng ký vào `CA` như các ca khác); ca nạp module bằng `_tai_launcher_thu()` TRONG thân ca và lấy `_ShutilWin311` từ module ấy; mọi khẳng định dùng `bang(...)` trực tiếp tại ca, thông điệp định danh vế (a)/(b); vế (b) kiểm `u is not None` TRƯỚC khi lấy `dirname(u)`. Trong thư mục tạm riêng của ca, dựng `d/` rỗng và `cwd/` có tệp thực thi tên `foo` (trên Windows dùng `foo.exe`/`foo.cmd` theo PATHEXT nếu ca chạy ở đó; trên POSIX chmod +x); đặt thư mục làm việc của tiến trình là `cwd/` TRONG phạm vi ca và khôi phục trong `finally`; khẳng định (a) `_ShutilWin311.which(<d>/foo)` trả `None`; (b) sau khi tạo `foo` thực thi trong `d/`, trả đúng đường dẫn trong `d/` (so `os.path.normpath(os.path.dirname(...)) == os.path.normpath(d)`). Mỗi khẳng định có thông điệp định danh vế (a)/(b). | `.claude/dev/launcher_test.py` |
| M2 | Một đột biến mới trong `DOT_BIEN`: `r1375_bo_loc_thu_muc`, tìm `return u if u and os.path.normpath(os.path.dirname(u)) == os.path.normpath(d) else None` thay `return u`, ca đích `["r1375_shutilwin311_chi_nhan_trong_d"]`. | `.claude/dev/launcher_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Ca M1 ĐẠT trên head (Linux, cả Python 3.11 của lane launcher và 3.12+ của gate — ca gọi thẳng lớp nên không phụ thuộc phiên bản); runner ghi `qua` khi không đột biến. | Đột biến M2 qua runner ⇒ ca ĐỎ tại `bang(...)` vế (a) (nhận `./foo`), runner ghi `giet`, không phải `loi`/`bo_qua`. Đối chứng RIÊNG cho vế (b): thay toàn bộ biểu thức trả về của bộ lọc bằng `return None` ⇒ vế (a) qua, vế (b) ĐỎ tại `bang(...)` (không phải `TypeError`). |
| N2 | Bộ đột biến của `launcher_test.py` trên CI giết `r1375_bo_loc_thu_muc` đúng ca đích (bán kính đột biến của lane hiện hành báo giết 1/1). | Xoá ca hoặc bỏ đăng ký vào `CA` ⇒ runner báo thiếu ca đích và thất bại; giữ ca nhưng bỏ khẳng định vế (a) ⇒ M2 SỐNG, bộ đột biến ĐỎ. |
| N3 | Ca M1 không rò trạng thái: sau ca, thư mục làm việc của tiến trình bằng trước ca; các ca khác của `launcher_test.py` đạt như base. | Bỏ khôi phục cwd trong `finally` ⇒ phép so cwd trước/sau (đặt trong chính ca) ĐỎ. |
| N4 | Đo trên exact head, ghi lệnh + mã thoát + bằng chứng dương: `ruff --select F` delta 0 trên tệp; `doctrine-scan`, `adr-song` rc 0; `git diff --check` sạch; `git diff --numstat base..H` đúng 1 tệp, ≤ 450 dòng thêm (`ADR-0053`). | Phản chứng lint: thêm một tên chưa định nghĩa ⇒ ruff delta ≠ 0; phản chứng phạm vi: thêm một đường dẫn thứ hai ⇒ numstat 2 tệp. `doctrine-scan`/`adr-song`: không có phản chứng riêng ở packet này (canh bất biến, răng do bộ test của chính chúng) — khai thẳng. |

## 5. `pham_vi_e`

Không chạm E4, không chạm E5.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Cần sửa `launcher.py` hoặc ngoài write set để một tiêu chí đạt ⇒ dừng triển khai và đi revision đặc tả; chỉ hỏi **E1** khi không còn phương án có phép đo chống đỡ.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục (bổ sung răng cho bộ lọc đã đúng).

## 8. `chua_do_duoc`

- Ca không đo nhánh Windows thật của `_thuc_thi` (đã có ca `r1335_*`); chỉ đo hành vi của lớp `_ShutilWin311`.
- Kích thước ước lượng tĩnh (2026-11-17T12:52:14Z, chưa có diff): ~30–50 dòng thêm vào một tệp; đo lại bằng numstat trước khi công bố.
