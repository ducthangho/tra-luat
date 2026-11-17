tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174-WINDOWS-BACKEND r1 — hai primitive Windows native đứng riêng (đọc an toàn có định danh, nhận diện volume NTFS), chưa nối vào runtime

- packet_id: WP1174-WINDOWS-BACKEND; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #1342 |
| `nguon_cap_viec` | Chủ kho 16-11-2026 (thân Issue #1342); chủ kho 17-11-2026 yêu cầu mở phiên soạn đặc tả và chốt Q1–Q15 trong phiên điều phối #1206 — sổ quyết định chép ở §9 và đăng lên Issue #1342 trước khi đóng băng (URL ghi vào lease, trường `spec_duyet`). |
| `review_class` | `sensitive` (runtime trạng thái WP1174) |
| `base` | `a0702d06b7d3956fb91b951766c7a5d6a77a7f5b` lúc soạn; lease ghi OID base thật lúc cấp và người cấp đo lại §0 trên base ấy. |

## 0. Hiện trạng (đo 2026-11-17T06:06:54Z trên `a0702d06b7d3956fb91b951766c7a5d6a77a7f5b`)

Runtime WP1174 ở `.claude/dev/packet_loop.py` (6.359 dòng), khối chính 3659–6036, có hook ngoài khối (ví dụ 1408–1445, 2496, 3220). Chỉ chạy Linux theo thiết kế: `ops/specs/wp1174-c5-adapter-design.md` §8; `docs/PROTOCOL_DA_PHIEN.md` 941, 1591, 1623–1628.

| primitive Linux | hàm (dòng) | bất biến |
|---|---|---|
| `lstat`+`S_ISREG`, mở `O_NOFOLLOW\|O_CLOEXEC`, so `(st_dev, st_ino, size, mtime_ns, ctime_ns)` lúc mở, sau đọc trên fd, và với `path.lstat()` sau đọc | `_1174_read` 3892 | không theo symlink lá; phát hiện tráo tệp hoặc đổi entry giữa mở và đọc |
| `/proc/self/mountinfo` + `statfs` magic, chỉ ext4/xfs, đường dẫn tuyệt đối đã resolve | `_1174_platform` 4003, `_1174_mount` 4007 | đúng một hệ tệp cục bộ bền đã kiểm |
| `flock`, publish `link`/`replace` + fsync thư mục, seed `0600`, `boot_id`, `killpg` | 3989, 3945, 4712, 4801, 4259 | (ngoài r1) |

`_1174_read` còn được gọi ngoài lệnh WP1174 — hook đọc trạng thái schema 3 ở 1419. Vì vậy nối bản Windows vào `_1174_read` sẽ ĐỔI hành vi Windows của đường đọc trạng thái chung, không chỉ của lệnh WP1174. `_1174_command` (5899) từ chối mọi nền khác Linux ở 5906, trước resolver.

Test `.claude/dev/packet_loop_test.py` (16.566 dòng): 85 ca `wp1174_*` (= `WP1174_REQUIRED`, 12404; Linux bắt buộc 84); Windows bắt buộc 12 ca `WP1174_BOTH` (12414); 279 khoá `MUTANTS` chứa `1174`. Mọi giá trị `MUTANTS` là bộ ba `(tìm, thay, ca phải chết)`, các vòng 12021/12095/12105 unpack bộ ba — runner của tệp này KHÔNG có phần tử nền thứ tư (khác `launcher_test.py`).

Tiền lệ Windows (khác tệp, chép mô hình): `.claude/dev/launcher.py` `_KhoCodex` 3826 (`CreateFileW` mở chính reparse point 4020–4023, từ chối reparse 4041, ghim tổ tiên); `.claude/dev/launcher_test.py:8748` dựng junction bằng `mklink /J`.

## 1. Bậc và phạm vi r1

Hướng đã chốt (Q2): nhiều bậc, Windows chỉ được nhận ở bậc cuối kèm ADR. Dự toán của review độc lập lượt 1 cho bốn primitive (đọc, khoá, publish, volume) + probe là 530–810 dòng thêm, vượt trần `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm). Người soạn cắt:

| bậc | nội dung |
|---|---|
| **r1 (đặc tả này)** | bindings `ctypes` tối thiểu + `_1174_win_read` + `_1174_win_volume`/`_1174_win_platform`, ĐỨNG RIÊNG (không hàm hiện có nào gọi tới), + test thuần và native tập trung. Đột biến Windows do phiên điều phối chạy bằng driver NGOÀI kho trên bản sao tạm (M6), không thêm runner vào kho. Dự toán review độc lập lượt 2 (có runner trong kho) 365–540 dòng; bỏ runner (45–70) ⇒ khoảng 320–470 dòng thêm — vẫn sát trần, xem §7. |
| r1b | khoá `LockFileEx` + publish (`CreateHardLinkW`/`MoveFileExW`) + probe bốn mục. |
| r1c | seed ACL, BootId, Job Object. |
| r2 | nối các primitive vào runtime cho lệnh chỉ-đọc trên Windows. |
| r3 | mutator trên Windows; đổi protocol, cần ADR. |

Vì r1 không nối vào runtime nên mọi hàm hiện có giữ nguyên BYTE và hành vi Windows của mọi lệnh không đổi.

## 2. `write_set`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
```

## 3. `ngoai_pham_vi`

- Không sửa thân bất kỳ hàm/khối nào đang có trong `packet_loop.py`; không thêm lời gọi tới hàm `_1174_win_*` từ mã runtime. Chỉ THÊM định nghĩa mới.
- Không khoá, publish, probe, seed, BootId, Job Object (r1b, r1c).
- Không đổi `docs/`, ADR, `ops/specs/wp1174-*`.
- Không `pywin32`; không đổi `requirements.txt`/manifest.
- Mã runtime không `import` `launcher.py` (Q15). Riêng **test** được `import` `launcher.py` (chỉ đọc, không sửa) để chạy ca đối chiếu N6.
- Không đồ giả `kernel32` trên Linux (Q11).
- Không ReFS, ổ mạng, ổ rời, FAT/exFAT, UNC (Q3). Định danh tệp dùng `FileIndex` 64-bit chỉ đúng trong profile NTFS này; không suy rộng sang ReFS (`FILE_ID_INFO` 128-bit).
- Không đổi `MUTANTS` (không thêm, không bớt, không sửa khoá nào); không thêm runner đột biến; không chạy trọn bảng đột biến trên Windows (Q14); không CI Windows.

## 4. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Bindings `ctypes` (chỉ nạp khi `os.name == "nt"`, gọi lười trong hàm): `CreateFileW`, `GetFileInformationByHandle`, `GetFileInformationByHandleEx` (`FileBasicInfo`, `FileAttributeTagInfo`), `ReadFile`, `CloseHandle`, `GetVolumeInformationByHandleW`, `GetVolumeInformationW`, `GetVolumePathNameW`, `GetDriveTypeW`, `GetFileType`. Khai `argtypes`/`restype` tường minh; lỗi Win32 ⇒ `OSError` có mã. | `.claude/dev/packet_loop.py` |
| M2 | `_1174_win_read(path)`: (a) chỉ nhận đường dẫn tuyệt đối dạng ổ đĩa (`X:\…`); từ chối UNC (`\\`), namespace thiết bị/Win32 (`\\?\`, `\\.\`) và alternate data stream (`:` sau ký tự ổ); (b) mở `GENERIC_READ`, share `READ` (không `WRITE`, không `DELETE`), `OPEN_EXISTING`, `FILE_FLAG_OPEN_REPARSE_POINT`, handle không kế thừa; (c) trên CHÍNH handle trước `ReadFile`: `GetFileType == FILE_TYPE_DISK`, `FileAttributeTagInfo` không `REPARSE_POINT`/`DIRECTORY`, `GetVolumeInformationByHandleW` báo `NTFS` và serial khớp volume root `DRIVE_FIXED` (cùng phép của M3); (d) định danh = `(VolumeSerialNumber, FileIndex64, size, LastWriteTime)` từ `GetFileInformationByHandle` + `ChangeTime` từ `FileBasicInfo` (chỉ đúng trong profile NTFS này); (e) so định danh lúc mở và sau đọc trên cùng handle; lưu định danh và bytes, ĐÓNG handle đọc trong `finally`, rồi MỞ LẠI tên bằng cùng quyền/cờ, kiểm lại profile (c) và đòi định danh khớp trước khi trả bytes; luôn đóng handle mở lại; mất tên hay lỗi mở lại ⇒ từ chối, không trả bytes đã đọc — tương ứng vế `path.lstat()` của Linux (kiểm tại thời điểm, không phải khoá tên liên tục); (f) trả bytes. Chú thích ghi nguồn `launcher.py` `_KhoCodex` (3826, 4020–4041). | `.claude/dev/packet_loop.py` |
| M3 | `_1174_win_platform(fs_name, drive_type, path_text)` THUẦN (chạy mọi nền): nhận chỉ khi `fs_name == "NTFS"`, `drive_type == DRIVE_FIXED (3)`, đường dẫn tuyệt đối có ký tự ổ và không bắt đầu `\\` (UNC). `_1174_win_volume(path)`: mở thư mục với quyền `FILE_READ_ATTRIBUTES`, share `READ\|WRITE` (không `DELETE`), `FILE_FLAG_BACKUP_SEMANTICS\|FILE_FLAG_OPEN_REPARSE_POINT`, từ chối nếu chính nó là reparse point, lấy `GetVolumeInformationByHandleW` (tên FS, serial) trên CHÍNH handle ấy và `GetDriveTypeW` trên volume root lấy từ `GetVolumePathNameW`, lấy serial của volume root bằng `GetVolumeInformationW` trên chuỗi root ấy và đối chiếu với serial của handle (kiểm nhất quán, không phải định danh volume mật mã), rồi gọi `_1174_win_platform`. Trả `dict(filesystem, serial, drive_type, volume_root)`. | `.claude/dev/packet_loop.py` |
| M4 | Ca thuần (mọi nền, ID `wp1342_*`, KHÔNG thêm vào `WP1174_REQUIRED`/`WP1174_BOTH`): bảng `_1174_win_platform` nhận/từ chối; ca kiểm "không hàm hiện có nào gọi `_1174_win_`" (quét AST mọi hàm trừ các hàm `_1174_win_*`); ca bảng tên đường dẫn bị loại của M2(a); ca N2 (bảo toàn byte, xem N2) đặt TRONG tệp test này. Ca native chỉ Windows; trên Linux in `BỎ QUA <lý do>` và KHÔNG tính là đạt. | `.claude/dev/packet_loop_test.py` |
| M5 | Ca native (Windows), giữ nguyên share mode của M2: đọc tệp thường đúng bytes; từ chối thư mục; từ chối junction mở ở chế độ thư mục (M3) và junction làm tệp (M2); từ chối đường thiết bị (`\\.\NUL`, có timeout); **tráo tên qua tổ tiên không ghim**: hook kiểm thử chạy SAU khi handle đọc đầu đã đóng và TRƯỚC lần mở lại tên (ca xác nhận hook thật sự được gọi và handle đầu đã đóng); hook đổi tên thư mục cha rồi dựng lại tên cha chứa một tệp khác, xác nhận mọi thao tác thành công và định danh hai tệp khác nhau; bản gốc phải từ chối đúng vì định danh mở lại không khớp, đột biến bỏ mở lại phải trả bytes cũ và làm ca đỏ (`.claude/dev/launcher_test.py:14165` đã ghi: không đổi tên được thư mục cha khi tệp con còn mở); **đổi metadata**: handle đọc vẫn mở; mở handle thứ hai đúng `FILE_WRITE_ATTRIBUTES`, share `READ|WRITE|DELETE`, `OPEN_EXISTING`, không xin `GENERIC_WRITE`/`FILE_WRITE_DATA`; `SetFileTime` đổi `LastWriteTime` trước phép lấy định danh sau đọc, truy vấn lại xác nhận giá trị đã đổi khi handle thứ hai còn mở, rồi đòi từ chối đúng vì định danh thay đổi; handle không kế thừa (tiến trình con không thấy); ca cần symlink tệp tự kiểm quyền, thiếu ⇒ `KHÔNG ĐO ĐƯỢC` (Q12). Không dựng được điều kiện của một ca ⇒ ca in `KHÔNG ĐO ĐƯỢC`, không in đạt. | `.claude/dev/packet_loop_test.py` |
| M6 | Đột biến Windows: KHÔNG thêm runner hay bảng vào kho. Executor khai trong thân PR, cho từng đột biến, cặp (chuỗi tìm, chuỗi thay) khớp ĐÚNG MỘT chỗ trong head và ca đích; phiên điều phối áp từng đột biến trên BẢN SAO TẠM ở Desktop bằng driver ngoài kho, chạy đúng ca đích + ca đối chứng khoẻ, phân loại lỗi import/dựng fixture là KHÔNG ĐO (không phải giết). Ba đột biến: bỏ `FILE_FLAG_OPEN_REPARSE_POINT` ở `_1174_win_volume`; bỏ bước mở lại tên ở `_1174_win_read`; bỏ vế `fs_name == "NTFS"`. | `.claude/dev/packet_loop_test.py` (ca đích) |

## 5. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux không đổi: CI Ubuntu trên exact head, `gate-packet-loop` gom `GOM: ĐẠT · 16 mảnh · <n> ca bắt buộc`; 84 ca `wp1174_*` đạt. `MUTANTS` ở head bằng CHÍNH XÁC `MUTANTS` ở base (cùng tập khoá, cùng giá trị từng khoá) — r1 không thêm đột biến vào kho. | Một ca `wp1174_*` đỏ; phản chứng đổi tên một khoá giữ nguyên số lượng ⇒ ĐỎ. |
| N2 | Chỉ THÊM, đo bằng ca test trong `packet_loop_test.py` (M4) đọc `packet_loop.py` của head và blob base qua `git show <base>:…`: AST chỉ dùng để xác định các khối MỚI (gồm decorator) — mỗi khối mới là định nghĩa hàm `_1174_win_*` hoặc phép gán hằng `_1174_WIN_*`, tên không trùng base và không trùng nhau; loại đúng các khối ấy khỏi byte head thì phần còn lại phải bằng NGUYÊN BYTE base. Không chấp nhận import mới, gán lại tên cũ hay câu lệnh thực thi cấp module. `<base>` là OID đầy đủ ghi trong lease; thiếu object hay `git show` lỗi ⇒ ca ĐỎ với chẩn đoán rõ, không bỏ qua, không thay bằng HEAD/merge-base; so byte theo chính sách LF của kho. | Phản chứng (chạy trong PR): đổi chú thích/khoảng trắng một hàm cũ; thêm decorator vào hàm cũ; định nghĩa trùng tên; thêm `_1174_read = _1174_win_read` cuối module — đều ĐỎ; thêm một hàm `_1174_win_x` hợp lệ — XANH. |
| N3 | Không nối dây: ca M4 "không hàm hiện có nào gọi `_1174_win_`" đạt trên mọi nền; nối dây kiểu alias/module do N2 bắt. | Đột biến thêm `_1174_win_read(path)` vào `_1174_read` ⇒ ca ĐỎ. |
| N4 | Windows vẫn bị từ chối, không đổi: trên Desktop, `wp1174_windows_claim_rejected` và 12 ca `WP1174_BOTH` đạt, y hệt base cùng lượt. | Ca nào lệch base. (r1 không đụng `_1174_command`; răng riêng cho chốt OS thuộc r2, nơi nối dây bắt đầu.) |
| N5 | Ca native M5 đạt trên Desktop, mỗi ca in dấu hiệu dương (ID, `executed`, `passed`); ca thuần M3 đạt trên Linux và Windows. | Ca native in `BỎ QUA` trên Windows ⇒ ĐỎ; hàm trả hằng bytes rỗng ⇒ ca đọc ĐỎ. |
| N6 | Ca đối chiếu (Q15): dựng thư mục đích NTFS với ACL hợp lệ; ĐỐI CHỨNG gọi trực tiếp trên đích — cả `launcher._KhoCodex` lẫn `_1174_win_volume` mở thành công. Qua junction tới cùng đích — cả hai từ chối TẠI kiểm reparse (lý do lỗi phải là reparse, không phải lớp khác). "Không đọc đích" = không đọc nội dung tệp; truy vấn metadata ghi riêng. | Đột biến bỏ `FILE_FLAG_OPEN_REPARSE_POINT` ở `_1174_win_volume` ⇒ hàm qua được kiểm reparse và nhận đích qua junction ⇒ ca ĐỎ; đối chứng thất bại ⇒ ca KHÔNG ĐO, không đạt. |
| N7 | Ba đột biến M6 bị giết đúng ca đích trên Desktop. Hồ sơ land có: exact head/tree, băm và toàn văn driver, lệnh chạy, phiên bản Python/Windows, từng cặp tìm/thay kèm số lần khớp = 1; với mỗi đột biến: ca đích và đối chứng đạt trên bản sạch, áp đột biến trên bản sao MỚI, lưu diff thực tế, chạy lại hai ca; chỉ tính giết khi đúng assertion hành vi của ca đích thất bại, đối chứng đạt và fixture hoàn tất. Hồ sơ đủ để chạy lại không cần thân PR. Driver tự kiểm: chuỗi tìm không khớp hoặc fixture cố ý hỏng ⇒ `KHÔNG ĐO`, không "giết". | Đột biến SỐNG; hoặc ca đích "đỏ" vì `ImportError`/fixture hỏng (driver phân loại KHÔNG ĐO). |
| N8 | Ca symlink tệp: Desktop in `KHÔNG ĐO ĐƯỢC` khi không có quyền (đo 17-11-2026 trong phiên #1206 khi chạy N2 của #1356: Desktop không tạo được symlink); VM `tra-luat-win` in dấu hiệu dương ID/`executed`/`passed`. | Ca in `ĐẠT` khi không tạo được symlink; VM không có dòng dương. |
| N9 | Ruff `--select F` delta 0; `adr-song`, `doctrine-scan` rc 0; `git diff --check` sạch; `eol_policy --all` ok; `git diff --numstat base..H` ≤ 2 tệp và ≤ 450 dòng thêm (trần `ADR-0053` đã đo hiệu lực: ba phép của mục Hiệu lực rc đúng, đo 2026-11-17T06:10:33Z). | Một gate nào thất bại ⇒ ĐỎ; vượt trần ⇒ dừng theo §7. |

Đo Windows (N4–N8) do phiên điều phối chạy trên **`DESKTOP-T9R33P2`** (ưu tiên, Q8), VM `tra-luat-win` dự phòng và cho N8; base và head trong cùng một lượt; không chạy trọn bảng đột biến trên Windows.

## 6. `pham_vi_e`

Không chạm E4, không chạm E5. Không đảo quyết định "chỉ Linux" (Windows vẫn bị từ chối, primitive chưa nối), nên không E3.

## 7. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; trần vòng review theo `ADR-0048` và protocol. Chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- `git diff --numstat` vượt `ADR-0053` ⇒ dừng; câu hỏi mang **E2** (mức đã dùng, còn thiếu, để làm gì).
- Cần sửa thân một định nghĩa hiện có, cần sửa ngoài write set, hoặc cần nối dây để một tiêu chí đạt ⇒ dừng; câu hỏi mang **E1** (gốc rễ, phương án đã thử, đề xuất).
- Desktop và VM cùng offline quá hạn lease ⇒ **E2**.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục.

## 9. Sổ quyết định của lượt soạn

Chủ kho chốt trong phiên điều phối #1206, 17-11-2026: Q1 mục đích coordinator/canary Windows native, theo bậc · Q2 nhiều bậc · Q3 chỉ NTFS cục bộ · Q4 hai chỗ gần đúng chấp nhận, báo cáo Windows không là bằng chứng tới khi có ADR riêng · Q5 seed: owner SID + DACL bảo vệ + `nlink==1` (r1c) · Q6 chỉ `ctypes` · Q7 write set hai tệp · Q8 đo native ưu tiên Desktop, VM dự phòng · Q9 giữ byte hàm Linux, thêm `_1174_win_*` · Q10 probe báo từng mục, `eligible=False` (r1b) · Q11 không đồ giả Win32 · Q12 junction thay symlink · Q13 đột biến có răng, `WRITE_THROUGH` khai không đo được (r1b) · Q14 chỉ chạy ca mới + 12 ca pure trên Windows · Q15 chép mô hình từ `launcher.py`, có ca đối chiếu.

Quyết định của người soạn trong hướng đã duyệt, sau review độc lập Codex lượt 1 (`request_changes`, chín P2): cắt r1 xuống hai primitive đứng riêng, không nối dây (§1); dùng bảng đột biến riêng thay phần tử nền thứ tư; chép finding P2 về định danh/handle/volume vào M2–M3 và N2–N8. Lượt 4: `approve`, một P3 (câu cũ ở §10) đã sửa theo câu thay thế của reviewer. Sau lượt 3 (`request_changes`, một P2 + một P3): `_1174_win_read` đóng handle đầu trước khi mở lại, hook tráo tên chạy giữa hai lần mở; khai tham số handle metadata; hợp đồng tái lập cho driver đột biến; base đầy đủ cho N2. Sau lượt 2 (`request_changes`, bốn P2 + một P3): N2 bảo toàn nguyên byte ngoài khối mới; fixture tráo tên qua thư mục cha, metadata qua handle `FILE_WRITE_ATTRIBUTES`; `_1174_win_read` tự cưỡng chế profile NTFS/`FILE_TYPE_DISK`/dạng tên; N1 so nguyên `MUTANTS`; N6 có đối chứng; đột biến chạy bằng driver ngoài kho để giữ dưới trần.

## 10. `chua_do_duoc`

- Kích thước thật: dự toán khoảng 320–470 dòng (ước lượng tĩnh); vượt trần thì theo §7.
- Đột biến Windows không nằm trong kho: chạy lại sau này đòi driver ở hồ sơ land.
- Các fixture M5 (đổi tên thư mục cha sau khi handle đọc đầu đã đóng và trước lần mở lại tên; đổi metadata bằng handle `FILE_WRITE_ATTRIBUTES` trong khi handle đọc vẫn mở) là thiết kế chưa kiểm thực trên Windows; không dựng được ⇒ ca ghi KHÔNG ĐO ĐƯỢC và tiêu chí liên quan chưa đạt.
- Hành vi trên ReFS/ổ mạng: bị từ chối, không đo năng lực.
- Ca symlink tệp trên Desktop: phụ thuộc quyền máy; đo bù trên VM.
- Răng cho chốt OS của `_1174_command`: không đo ở r1 (r1 không chạm nó); thuộc r2.
