tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174-WINDOWS-BACKEND r3 — seed riêng và BootId Windows native đứng riêng (bậc r1c), chưa nối vào runtime

- packet_id: WP1174-WINDOWS-BACKEND; revision: 3;

| trường | giá trị |
|---|---|
| `packet_issue` | #1342 |
| `nguon_cap_viec` | Lộ trình bậc ở §1 đặc tả r1 (bậc r1c: seed ACL, BootId, Job Object). Chủ kho 17-11-2026 (phiên điều phối #1206) duyệt bốn khuyến nghị: tách r1c — revision này gồm seed + BootId, tiến trình (Job Object) + probe sang bậc mới r1d; BootId lấy từ registry `PrefetchParameters\BootId`; DACL seed chỉ cho người dùng hiện tại và SYSTEM; đo BootId đổi bằng MỘT lần khởi động lại VM `tra-luat-win`. |
| `review_class` | `sensitive` (runtime trạng thái WP1174) |
| `base` | master SAU KHI revision 2 (bậc r1b, `ops/specs/WP1174-WINDOWS-BACKEND-r2.md`, sha256 `ff7bcc07…`) đã land; lease ghi OID base thật và người cấp đo lại §0 trên base ấy. |

**Đánh số:** `revision: 3` là revision thứ ba của packet (ADR-0063 đòi số nguyên), là bậc **r1c** của lộ trình — không phải bậc "r3" (mutator) trong bảng bậc của đặc tả r1.

## 0. Hiện trạng (đo 2026-11-17T12:58:04Z trên `39ce682`; dòng sẽ trôi khi r2 land, đo lại lúc cấp lease)

| Linux | hàm (dòng) | bất biến |
|---|---|---|
| seed riêng | `_1174_seed` 4712 (16 dòng) | `lstat`: tệp thường, mode `0600`, `st_uid == geteuid()`, `st_nlink == 1`; đọc bằng `_1174_read`; `lstat` lại: `(dev, ino, mode, nlink, uid)` không đổi; `len == 32` và `sha256 == e["private_seed_sha256"]`; `OSError` ⇒ `ValueError("WP1174 UNKNOWN: private seed read/lstat")` |
| boot id | `_1174_runtime` 4806 (một biểu thức) | `/proc/sys/kernel/random/boot_id` (chuỗi, bỏ khoảng trắng) phải bằng `e["boot_id"]` đã ghi lúc admission |

Mẫu Windows trong kho: `.claude/dev/launcher.py` `_KhoCodex._win_private` (khoảng 4060–4090): `GetSecurityInfo(handle, SE_FILE_OBJECT, OWNER|DACL)` → `ConvertSecurityDescriptorToStringSecurityDescriptorW` → so owner và từng ACE trên chuỗi SDDL. Mẫu ấy kiểm owner thuộc `{người dùng, SYSTEM, Administrators}`; với ACE ALLOW còn cho `OWNER RIGHTS` (`S-1-3-4`, alias `OW`) sau khi chuẩn hoá SID; bỏ qua ACE `IO` và deny. r3 CHẶT hơn theo quyết định chủ kho (§4 M2) và không kế thừa ngoại lệ `OW`.

`_1174_win_read`, `_1174_win_open`, `_1174_win_identity` (r1) đã có; r2 thêm `_1174_win_api_ghi`. Chốt không-nối-dây `_wired1342` (trên cây làm việc) phủ mọi hàm mới tên `_1174_win_*` không decorator.

Kích thước ước lượng (tĩnh, chưa đo): người soạn ~300–390; review độc lập lượt 1 ~362–480 sau các sửa đổi ⇒ CHƯA đủ cơ sở khẳng định dưới trần; đo numstat thật, vượt thì theo §7, không cắt assertion hay cleanup để ép số dòng.

## 1. Phạm vi r3

Thêm, ĐỨNG RIÊNG (không hàm hiện có nào gọi tới): bindings bảo mật, hàm THUẦN chính sách SDDL, `_1174_win_seed`, `_1174_win_boot_id`, ca test thuần (Linux) và native (Windows). Không sửa thân định nghĩa nào đang có, kể cả các hàm `_1174_win_*` của r1/r2.

## 2. `write_set`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
```

## 3. `ngoai_pham_vi`

- Không sửa thân hàm/khối nào đang có (kể cả `_1174_win_*` của r1, r2, và helper test `_new1342`/`_additive1342`/`_wired1342`/`_additive1342r2`).
- Không tiến trình/Job Object, không probe (bậc r1d); không nối dây.
- Không ghi/tạo seed (chỉ ĐỌC và kiểm, như `_1174_seed`); tạo seed đúng ACL chỉ có trong FIXTURE test.
- Không cho Administrators, `OWNER RIGHTS` (`OW`) hay bất kỳ SID nào khác ngoài người dùng hiện tại và SYSTEM.
- Không `pywin32`; `winreg` là thư viện chuẩn. Không đồ giả Win32 trên Linux (Q11).
- Không đổi `MUTANTS`; không thêm runner; không CI Windows.

## 4. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Hàm MỚI `_1174_win_api_bao_mat()`: gọi `_1174_win_api()` rồi bind (argtypes/restype tường minh) trên `advapi32`: `GetSecurityInfo`, `ConvertSecurityDescriptorToStringSecurityDescriptorW`, `OpenProcessToken`, `GetTokenInformation`, `ConvertSidToStringSidW`; trên `kernel32`: `LocalFree`, `GetCurrentProcess`. Trả các đối tượng cần dùng. Không bind API ngoài tập này. | `.claude/dev/packet_loop.py` |
| M2 | Hàm THUẦN `_1174_win_seed_acl(sddl, user_sid)` (chạy mọi nền). Grammar được hỗ trợ (đúng dạng `ConvertSecurityDescriptorToStringSecurityDescriptorW` sinh cho `OWNER\|DACL`): `O:<sid>D:<cờ DACL><ACE>…`, không phần nào khác (`G:`, `S:` ⇒ từ chối), không phần dư. Cờ DACL là chuỗi con của `{P, AI, AR}` (cờ DACL `AI`/`AR` KHÁC cờ ACE `ID/IO/OI/CI`). Trả `True` khi và chỉ khi: (a) có đúng một phần `O:` và nó là `user_sid`; (b) có đúng một phần `D:`, cờ DACL chứa `P`, và không có `NO_ACCESS_CONTROL`; (c) DACL có ít nhất một ACE, MỌI ACE có đúng 6 trường, loại `A` (ALLOW), cờ ACE rỗng (không `ID`/`IO`/`OI`/`CI`), SID thuộc `{user_sid, "SY", "S-1-5-18"}`; (d) có ít nhất một ACE cho `user_sid`. Mọi chuỗi không phân tích được ⇒ `False`. | `.claude/dev/packet_loop.py` |
| M3 | `_1174_win_seed(e)` bám `_1174_seed`: (a) `_1174_win_path(e["private_seed_path"])`; (b) mở `GENERIC_READ\|READ_CONTROL`, share `READ`, `OPEN_EXISTING`, `FILE_FLAG_OPEN_REPARSE_POINT` (handle không kế thừa); (c) trên handle: `_1174_win_identity` (tệp thường, không reparse, NTFS); `NumberOfLinks == 1` (`GetFileInformationByHandleEx(FileStandardInfo)` — bind qua bindings r1); SID người dùng hiện tại từ token tiến trình; SDDL `OWNER\|DACL` từ `GetSecurityInfo` qua `_1174_win_seed_acl` phải `True`; (d) đọc bytes trên CÙNG handle; (e) sau đọc, lặp lại (c) trên cùng handle và đòi định danh, `NumberOfLinks`, SDDL không đổi; (f) đóng handle trong `finally`, giải phóng mọi bộ nhớ `LocalFree`; (g) `len == 32` và `sha256 == e["private_seed_sha256"]`; (h) lỗi Win32 (`OSError`) ⇒ `ValueError("WP1174 UNKNOWN: private seed read/lstat")` như Linux; vi phạm chính sách ⇒ `_1174Error`. | `.claude/dev/packet_loop.py` |
| M4 | `_1174_win_boot_id()`: đọc `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters` giá trị `BootId` bằng `winreg` (`KEY_READ \| KEY_WOW64_64KEY`); bắt buộc kiểu `REG_DWORD`; trả `str(int)`. Thiếu khoá/giá trị, sai kiểu, lỗi đọc (`OSError`) ⇒ `_1174Error` (fail-closed), không fallback. Hàm KHÔNG có seam kiểm thử: nó `import winreg` trong thân và gọi qua thuộc tính module (`winreg.OpenKeyEx`, `winreg.QueryValueEx`, không `from winreg import …`), để ca B2 patch được đúng hai hàm ấy mà mã lấy giá trị, xử lý lỗi và kiểm kiểu của runtime chạy nguyên vẹn. Chú thích ghi rõ: khoá này không có tài liệu chính thức của Microsoft. | `.claude/dev/packet_loop.py` |
| M5 | Ca THUẦN (mọi nền), ID `wp1342_pure_seed_acl_bang`: bảng `_1174_win_seed_acl` với `user_sid` mẫu `S-1-5-21-1-2-3-1001`: NHẬN `O:<u>D:P(A;;FA;;;<u>)`, `O:<u>D:P(A;;FA;;;<u>)(A;;FA;;;SY)`, `O:<u>D:P(A;;FA;;;<u>)(A;;FA;;;S-1-5-18)`; và NHẬN cờ DACL hợp lệ có thêm `AI`/`AR`: `O:<u>D:PAI(A;;FA;;;<u>)`, `O:<u>D:PAR(A;;FA;;;<u>)`. TỪ CHỐI: owner khác; thiếu phần `O:`; hai phần `O:`; hai phần `D:`; có phần `G:`; thiếu `P` (`D:AI(…)`); có `NO_ACCESS_CONTROL`; ACE cho `BA`; ACE cho `OW`; ACE cho SID người khác; ACE deny `D`; ACE cờ `ID`; ACE cờ `IO`; ACE cờ `OI`; ACE cờ `CI`; ACE 5 trường; DACL rỗng `D:P`; chỉ có ACE `SY`; phần dư không phân tích được sau ACE cuối; chuỗi rác. Mỗi dòng bảng là một `bang(...)`/assert có nhãn riêng. Và ID `wp1342_pure_seed_boot_refuse`: trên nền không phải Windows, `_1174_win_seed({...})` với đường ổ đĩa hợp lệ và `_1174_win_boot_id()` từ chối bằng `_1174Error` "native Windows required" (seed: sau kiểm đường dẫn). Không thêm vào `WP1174_REQUIRED`/`WP1174_BOTH`. | `.claude/dev/packet_loop_test.py` |
| M6 | Ca NATIVE (Windows; nền khác `BỎ QUA <lý do>` không tính đạt), dấu hiệu dương `WP1342_NATIVE_V1`, ID `wp1342_native_seed_*`/`wp1342_native_boot_*`. FIXTURE tạo seed 32 byte với DACL `D:P` cho người dùng hiện tại và SYSTEM (bindings FIXTURE nằm trong tệp test, không trong runtime). **S1** seed đúng ⇒ trả đúng bytes; **S2** seed 32 byte đúng hash và đúng ACL nhưng có thêm một hard link ⇒ từ chối (nlink); **S3** DACL thêm ACE Administrators ⇒ từ chối; **S4** DACL không bảo vệ (kế thừa từ cha) ⇒ từ chối; **S5** seed đúng 32 byte, đúng ACL, nlink 1, nhưng `sha256` khác `e["private_seed_sha256"]` ⇒ từ chối; **S6** 31 byte ⇒ từ chối; **S7** đường là thư mục hoặc junction ⇒ từ chối; **S8** hook kiểm thử (`between`) chạy sau khi đọc, trước kiểm lại, đổi DACL từ dạng hợp lệ `{u, SYSTEM}` sang dạng HỢP LỆ khác `{u}` (giữ owner và cờ `P`), rồi đọc lại SD xác nhận thay đổi đã thành công ⇒ bản sạch từ chối tại assertion `private seed metadata drift` (không phải tại kiểm chính sách); **B1** `_1174_win_boot_id()` trả chuỗi chữ số, hai lần gọi liên tiếp bằng nhau; **B2** gọi `_1174_win_boot_id()` đường MẶC ĐỊNH, patch có phạm vi từng trường hợp (khôi phục trong `finally`, không sửa registry thật) tại `winreg.OpenKeyEx` hoặc `winreg.QueryValueEx`: `OpenKeyEx` ném `FileNotFoundError` (thiếu khoá); `QueryValueEx` ném `FileNotFoundError` (thiếu giá trị); `QueryValueEx` ném `PermissionError` (lỗi đọc); `QueryValueEx` trả `("5", REG_SZ)` (chuỗi số, để đột biến bỏ kiểm kiểu không đỏ nhờ lỗi `int`); `QueryValueEx` trả `(5, REG_QWORD)` ⇒ đều `_1174Error`; đối chứng `QueryValueEx` trả `(5, REG_DWORD)` ⇒ `"5"`. Không dựng được điều kiện ⇒ `KHÔNG ĐO ĐƯỢC`. | `.claude/dev/packet_loop_test.py` |
| M7 | Đột biến Windows qua driver ngoài kho (khuôn r1/r2): (a) bỏ MỌI kiểm `NumberOfLinks == 1` (trước và sau đọc) ⇒ S2 ĐỎ; (b) chỉ bỏ so `sha256` (giữ kiểm chiều dài) ⇒ S5 ĐỎ; (c) loại TOÀN BỘ khối kiểm hậu đọc (định danh, nlink, SDDL), giữ hook và kiểm trước đọc ⇒ S8 ĐỎ tại assertion "đã trả bytes dù metadata đổi", S1 vẫn đạt. Đột biến THUẦN-trên-Windows: (f) bỏ kiểm kiểu `REG_DWORD` ở `_1174_win_boot_id` ⇒ B2 ĐỎ tại dòng "REG_SZ", đối chứng DWORD vẫn đạt; (h) bọc lời đọc registry bằng `except OSError: return "5"` (fallback) ⇒ B2 ĐỎ tại dòng "thiếu khoá". Đột biến THUẦN (phiên điều phối chạy trên Linux bằng cùng driver): (d) bỏ đòi cờ `P` ở `_1174_win_seed_acl` ⇒ `wp1342_pure_seed_acl_bang` ĐỎ tại dòng "thiếu P"; (e) thêm `"BA"` vào tập SID cho phép ⇒ ĐỎ tại dòng "ACE cho BA"; (g) chỉ chấp nhận cờ DACL đúng bằng `P` ⇒ ĐỎ tại dòng nhận `PAI`. Mỗi đột biến có thể nhiều cặp (tìm, thay), mỗi cặp khớp đúng một chỗ. | `.claude/dev/packet_loop_test.py` (ca đích) |
| M8 | Hàm `_1174_win_seed` nhận một tham số kiểm thử `between=None` (default hằng, để `_new1342` nhận) chạy SAU khi đọc bytes và TRƯỚC kiểm lại (e) — chỉ phục vụ S8, như `between` của `_1174_win_read`. | `.claude/dev/packet_loop.py` |

## 5. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux không đổi: CI Ubuntu exact head, gom `GOM: ĐẠT · 16 mảnh · <n> ca`; mọi ca `wp1174_*`, `wp1342_*` hiện có đạt theo tính áp dụng; `MUTANTS` head bằng CHÍNH XÁC base. | Một ca đỏ; đổi tên một khoá `MUTANTS` giữ số lượng ⇒ phép so ĐỎ. |
| N2 | Chỉ THÊM, đo MỘT LẦN trên PR bằng `_additive1342r2(<blob base>, <blob head>)` (helper của r2) ⇒ `[]`; executor ghi lệnh + kết quả vào thân PR, phiên điều phối đo lại. | Sửa một byte thân hàm r1/r2 ⇒ khác `[]`; thêm decorator vào hàm mới ⇒ khác `[]`. |
| N3 | Không nối dây: `wp1342_additive_byte_preserved` (vế N3 trên cây làm việc) đạt. | Thêm lời gọi `_1174_win_seed` trong `_1174_seed` ⇒ ca ĐỎ. |
| N4 | M5 đạt trên Linux (CI) và Windows (Desktop). | Đột biến (d), (e), (g) của M7 ⇒ ĐỎ đúng dòng bảng. |
| N5 | Windows vẫn bị từ chối, không đổi: `wp1174_windows_claim_rejected` + 12 ca `WP1174_BOTH` đạt y hệt base; ca native r1/r2 vẫn đạt. | Ca nào lệch base. |
| N6 | Ca native M6 (S1–S8, B1, B2) đạt trên Desktop, mỗi ca dấu hiệu dương. | Ca native in `BỎ QUA` trên Windows ⇒ ĐỎ. |
| N7 | BootId đổi qua một lần khởi động lại: trên VM `tra-luat-win`, phiên điều phối chạy CÙNG exact head (ghi SHA/tree trong hồ sơ) để ghi `_1174_win_boot_id()` trước, khởi động lại VM MỘT lần, ghi lại sau; hai giá trị khác nhau và giá trị sau ≥ giá trị trước + 1. Hồ sơ land ghi cả hai giá trị và giờ khởi động lại. | Hai giá trị bằng nhau ⇒ ĐỎ (nguồn không đổi theo lần khởi động). |
| N8 | Tám đột biến M7 ((a)–(c), (f), (h) trên Windows; (d), (e), (g) trên Linux) bị giết đúng ca đích theo hợp đồng N7 của r1 (driver byte-exact trong hồ sơ land; chỉ tính giết khi assertion hành vi của ca đích thất bại và đối chứng đạt; chuỗi không khớp ⇒ `KHÔNG ĐO`). | Đột biến SỐNG, hoặc ca "đỏ" vì lỗi import/fixture. |
| N9 | Ruff `--select F` delta 0 trên hai tệp; `adr-song`, `doctrine-scan` rc 0; `git diff --check` sạch; `eol_policy --all` ok; numstat ≤ 2 tệp, ≤ 450 dòng thêm (`ADR-0053`). | Một cổng thất bại ⇒ ĐỎ; vượt trần ⇒ dừng theo §7. |

Đo Windows (N4 phần Windows, N5, N6, N8) trên **`DESKTOP-T9R33P2`** (ưu tiên, Q8), VM `tra-luat-win` dự phòng và cho N7.

## 6. `pham_vi_e`

Không chạm E4, không chạm E5. Không đảo quyết định "chỉ Linux" (primitive chưa nối), nên không E3. Khởi động lại VM ở N7 là việc chủ kho đã duyệt trong khuyến nghị Q4 (17-11-2026); ngoài đúng một lần ấy không khởi động lại máy nào.

## 7. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; trần vòng review theo `ADR-0048` và protocol. Chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- `git diff --numstat` vượt `ADR-0053` ⇒ dừng; câu hỏi mang **E2**.
- Cần sửa thân một định nghĩa hiện có, ngoài write set, hoặc nối dây để một tiêu chí đạt ⇒ dừng triển khai và đi revision đặc tả; chỉ hỏi **E1** khi không còn phương án có phép đo chống đỡ; thiếu quyền ⇒ **E2**.
- Desktop và VM cùng offline quá hạn lease ⇒ **E2**. VM không khởi động lại được hoặc không trở lại sau khởi động ⇒ N7 ghi `KHÔNG ĐO ĐƯỢC`, không khởi động lại lần hai; báo **E2**.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**, một lần, sau khi review độc lập approve.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục. Ghi chú từ r1/r2 (không phải bộ đếm lỗi): decorator làm `_new1342` không nhận khối mới (r2 F2) — mọi hàm mới r3 không decorator; helper so-additive dùng `_additive1342r2` (r2 F1), không dùng helper r1.

## 9. Sổ quyết định của lượt soạn

Chủ kho 17-11-2026 (phiên điều phối #1206) đồng ý bốn khuyến nghị: Q1 tách r1c (seed + BootId ở revision này; tiến trình + probe sang r1d); Q2 BootId từ registry `PrefetchParameters\BootId`, fail-closed, khai rủi ro không có tài liệu chính thức; Q3 DACL seed chỉ `{người dùng hiện tại, SYSTEM}`, DACL bảo vệ, mọi ACE ALLOW, owner = người dùng hiện tại; Q4 đo BootId đổi bằng một lần khởi động lại VM `tra-luat-win`. Giữ nguyên các quyết định r1: Q3 (NTFS cục bộ), Q5, Q6, Q7, Q8, Q11.

Sau review độc lập lượt 1 (`request_changes`, 3 P2 + 1 P3): thêm ca B2 cho các nhánh fail-closed của BootId (F1; lượt 2 F5: bỏ seam `doc=` vì nó bỏ qua mã đọc mặc định — B2 patch `winreg.OpenKeyEx`/`QueryValueEx` trong phạm vi ca, thêm đột biến fallback (h)); chốt grammar SDDL, nhận cờ DACL `AI`/`AR`, bảng từ chối đủ owner/DACL lặp, `G:`, cờ ACE `IO`/`CI`, phần dư (F2); S8 đổi giữa hai DACL hợp lệ, đột biến (a)/(b)/(c) chốt phạm vi (F3); §0 nêu ngoại lệ `OW` của mẫu launcher (F4).

Quyết định của người soạn trong hướng đã duyệt: tách chính sách SDDL thành hàm THUẦN để bảng ca chạy được trên Linux (răng đo trên CI); cờ ACE phải rỗng (seed là tệp, không có ACE kế thừa hợp lệ); `between` kiểm thử cho S8 theo khuôn `_1174_win_read`.

## 10. `chua_do_duoc`

- Kích thước thật: ước lượng tĩnh ~300–480 dòng thêm (người soạn và review độc lập); có thể vượt trần, khi đó theo §7.
- `BootId` registry không có tài liệu chính thức; hành vi khi Windows cập nhật lớn hoặc khởi động nhanh (Fast Startup/hibernate) chưa đo — N7 chỉ đo khởi động lại thường.
- Chính sách SDDL dựa trên dạng chuỗi do `ConvertSecurityDescriptorToStringSecurityDescriptorW` sinh; các ACE dạng callback/object (hiếm trên tệp NTFS thường) bị từ chối vì không đúng 6 trường hoặc không phải `A`.
- Số dòng §0 đo trên `39ce682`, sẽ trôi sau khi r2 land; người cấp lease đo lại.
