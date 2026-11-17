tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174-WINDOWS-BACKEND r2 — khoá và publish Windows native đứng riêng (bậc r1b), chưa nối vào runtime

- packet_id: WP1174-WINDOWS-BACKEND; revision: 2;

| trường | giá trị |
|---|---|
| `packet_issue` | #1342 |
| `nguon_cap_viec` | Lộ trình bậc ở §1 đặc tả r1 (`ops/specs/WP1174-WINDOWS-BACKEND-r1.md`, blob `cd72be856c628b454d9d71b1feaf6f7b6fc1fbc1`, sha256 `bcae8d15…`, nhánh `ops/wp1342-r1-g1-lease`): bậc **r1b** = khoá `LockFileEx` + publish `CreateHardLinkW`/`MoveFileExW` + probe. Chủ kho 17-11-2026 trong phiên điều phối #1206 duyệt ba khuyến nghị: làm r1b ngay; tách probe sang bậc r1c; review độc lập đặc tả trước khi duyệt băm. |
| `review_class` | `sensitive` (runtime trạng thái WP1174) |
| `base` | `39ce682b42fe82bb6a0fd66c4d81c08961598f98` lúc soạn (master sau merge PR #1374); lease ghi OID base thật lúc cấp và người cấp đo lại §0 trên base ấy. |

**Đánh số:** `revision: 2` là revision thứ hai của packet (ADR-0063 đòi số nguyên). Nó là bậc **r1b** của lộ trình, KHÔNG phải bậc "r2" (nối dây) trong bảng bậc của đặc tả r1.

## 0. Hiện trạng (đo 2026-11-17T12:26:33Z trên `39ce682`; số dòng tính từ `def` tới dòng cuối thân, gồm docstring và dòng trắng bên trong, không gồm decorator)

| primitive Linux | hàm (dòng) | dòng mã | bất biến |
|---|---|---|---|
| khoá cố định | `_1174_lock` 3989 (decorator `@contextlib.contextmanager` ở 3988) | 12 | mở `O_RDWR\|O_CREAT\|O_CLOEXEC\|O_NOFOLLOW` mode 0600; phải là tệp thường; `flock(LOCK_EX)` chặn tới khi có; sau khi có khoá, `(st_dev, st_ino)` của fd phải bằng của `lstat` tên; nhường fd; luôn đóng |
| publish trọn vẹn | `_1174_persist` 3945 | 41 | `create`: tên chưa tồn tại (có thì `FileExistsError`), ghi tệp tạm cùng thư mục + fsync, fsync thư mục, `link` không ghi đè, xoá tạm; `update`: đích phải là tệp thường, `replace`; fsync thư mục; đọc lại bằng `_1174_read` phải đúng bytes; lỗi giữa chừng chỉ xoá ảnh TẠM, không xoá ảnh đã publish |
| probe | `_1174_probe` 4037 | 36 | (ngoài r2 — chuyển sang bậc r1c theo duyệt của chủ kho) |

r1 (land `ded5d41`, hồ sơ `ops/land/pr1363-wp1342-land-evidence.yaml`) đã có, đứng riêng: `_1174_WIN_FIXED`, `_1174_win_path`, `_1174_win_platform`, `_1174_win_api`, `_1174_win_open` (cứng `OPEN_EXISTING`), `_1174_win_profile`, `_1174_win_identity`, `_1174_win_volume`, `_1174_win_read` (dòng 6037–6166 trên `39ce682`). `_1174_win_api` bind mười API phục vụ đọc/định danh/volume; r2 cần thêm bindings ghi.

Mọi lệnh WP1174 được chấp nhận qua input/platform/admission, kể cả chỉ đọc, đều lấy `_1174_lock` (`_1174_command` 5917) và đi qua `_1174_runtime` (4801, đọc `boot_id`), nên bậc nối dây cần cả r1b (khoá) lẫn r1c (BootId); r2 không nối dây.

Chốt không-nối-dây đã có: ca `wp1342_additive_byte_preserved` (`.claude/dev/packet_loop_test.py`) gọi `_wired1342` trên CÂY LÀM VIỆC (#1365, merge `285a0b1`): mọi chỗ ngoài khối `_1174_win_*` nhắc tới `_1174_win_` làm ca ĐỎ. Chốt này chỉ miễn các khối mà `_new1342` nhận: `def _1174_win_*` KHÔNG decorator, default chỉ là hằng. Vì vậy mọi hàm mới của r2 phải không decorator (xem M2); khi đó chúng được chốt phủ, không cần ca không-nối-dây mới.

`_additive1342` (helper N2 của r1) loại MỌI khối `_1174_win_*` khỏi head và báo trùng tên nếu tên đã có trong base; trên base `39ce682` (đã chứa chín khối r1) nó trả lỗi ngay cả với base/base (đo trong review độc lập lượt 1, `ops/reviews/wp1342-spec-r2/luot1.stdout.txt`). r2 cần helper riêng (M7).

Kích thước: r1 = +130 dòng mã / +298 dòng test = +428 (đo `nghiem-thu-ded5d41.txt`). Ước lượng r2 (tĩnh, chưa đo): người soạn ~320–420; review độc lập lượt 1 ~360–480 sau các sửa đổi ⇒ CHƯA đủ cơ sở khẳng định dưới trần; đo numstat thật, vượt thì theo §7, không cắt ca đo hay cleanup để ép số dòng.

## 1. Phạm vi r2

Thêm, ĐỨNG RIÊNG (không hàm hiện có nào gọi tới): bindings ghi, `_1174_win_lock`, `_1174_win_persist`, helper so-additive cho r2, cùng ca test thuần (Linux) và native (Windows). Không sửa thân bất kỳ định nghĩa hiện có nào, kể cả các hàm `_1174_win_*` của r1.

## 2. `write_set`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
```

## 3. `ngoai_pham_vi`

- Không sửa thân hàm/khối nào đang có trong `packet_loop.py` (kể cả `_1174_win_api`, `_1174_win_open` của r1); bindings và mở-có-tạo đi trong hàm MỚI. Không thêm lời gọi tới `_1174_win_*` từ mã runtime.
- Không probe, seed, BootId, Job Object (bậc r1c); không nối dây (bậc nối dây sau r1c).
- Không fsync thư mục trên Windows (không có tương đương đáng tin); độ bền dựa `os.fsync` của tệp tạm (trên Windows là `_commit`, tức `FlushFileBuffers`) + `MOVEFILE_WRITE_THROUGH`, khai KHÔNG ĐO ĐƯỢC (Q13).
- Không thêm ca thường trực so byte base với cây làm việc (bẫy đã gỡ ở #1365); helper M7 là HÀM, không đăng ký vào `CASES`; phép "chỉ thêm" đo MỘT LẦN lúc PR (N2). Không sửa `_new1342`, `_additive1342`, `_wired1342`, `_additive_case1342`.
- Không hứa tương đương POSIX `replace` khi một tiến trình khác đang mở đích mà không share `DELETE`: khi ấy `update` báo lỗi (M3, P6).
- Không `pywin32`; không đổi `requirements.txt`/manifest; không `docs/`, ADR.
- Không đồ giả `kernel32` trên Linux (Q11); không ReFS/ổ mạng/ổ rời/UNC (Q3).
- Không đổi `MUTANTS`; không thêm runner đột biến; không CI Windows.

## 4. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Hàm MỚI `_1174_win_api_ghi()`: gọi `_1174_win_api()` rồi bind thêm trên cùng `kernel32` (argtypes/restype tường minh) đúng SÁU API: `LockFileEx`, `UnlockFileEx`, `CreateHardLinkW`, `MoveFileExW`, `DeleteFileW`, `GetHandleInformation`; và cấu trúc `OVERLAPPED` khai bằng `ctypes` (Internal/InternalHigh kích thước con trỏ, hai DWORD Offset/OffsetHigh, HANDLE hEvent). Trả `(c, w, k, OVERLAPPED)`. Năm API phục vụ primitive M2/M3; `GetHandleInformation` phục vụ phép đo handle không kế thừa của ca L2. Không bind API ngoài tập sáu này. Chỉ chạy khi `os.name == "nt"` (lỗi `_1174Error` "native Windows required" ở nền khác, do `_1174_win_api`). | `.claude/dev/packet_loop.py` |
| M2 | `_1174_win_lock(path)` là hàm KHÔNG decorator (để `_new1342` nhận là khối mới): nó trả một context manager dựng từ generator nội bộ được bọc bằng `contextlib.contextmanager` BÊN TRONG thân hàm; không thực thi mới ở cấp module. Khi vào context: (a) chỉ nhận đường dẫn của `_1174_win_path`; thư mục cha qua `_1174_win_volume` (NTFS cố định); (b) `CreateFileW` `GENERIC_READ\|GENERIC_WRITE`, share `READ\|WRITE` (không `DELETE`), `OPEN_ALWAYS`, `FILE_FLAG_OPEN_REPARSE_POINT`, security attributes mặc định (handle không kế thừa); (c) trên handle: `_1174_win_identity` (tệp thường, không reparse, profile NTFS); (d) `LockFileEx(LOCKFILE_EXCLUSIVE_LOCK, 0, 0xFFFFFFFF, 0xFFFFFFFF, OVERLAPPED 0)` CHẶN tới khi có (giống `flock(LOCK_EX)`); cùng một đối tượng `OVERLAPPED` sống suốt context và dùng lại cho `UnlockFileEx` cùng vùng; (e) sau khi có khoá, mở lại TÊN bằng `FILE_READ_ATTRIBUTES`, share `READ\|WRITE\|DELETE`, `OPEN_EXISTING`, `FILE_FLAG_OPEN_REPARSE_POINT` và đòi định danh `(serial, FileIndex64)` khớp handle khoá (tương ứng vế `lstat` của Linux; đóng handle mở lại ngay); (f) nhường handle; `finally`: `UnlockFileEx` rồi `CloseHandle`; tệp khoá GIỮ LẠI sau khi nhả (như Linux). | `.claude/dev/packet_loop.py` |
| M3 | `_1174_win_persist(path, raw, *, create)` bám `_1174_persist`: (a) TRƯỚC mọi kiểm khác: `type(raw) is bytes` và `type(create) is bool` (sai ⇒ `_1174Error` "persist bytes/mode"); rồi `_1174_win_path`; thư mục cha qua `_1174_win_volume`; (b) `create=True`: tên phải chưa tồn tại (`os.path.lexists` ⇒ `FileExistsError`); `create=False`: đích mở `OPEN_EXISTING` + `FILE_FLAG_OPEN_REPARSE_POINT` qua `_1174_win_identity` phải là tệp thường không reparse; Handle kiểm đích của (b) chỉ sống trong phạm vi kiểm và phải ĐÓNG trước publish. (c) tệp tạm `tempfile.mkstemp(prefix=".wp1174-", dir=<cha>)`, ghi qua `with os.fdopen(fd, "wb")`: ghi, `flush`, `os.fsync`, và stream ĐÃ ĐÓNG trước `CreateHardLinkW`/`MoveFileExW`; tên tạm giữ trong một biến cục bộ, gán `None` NGAY sau khi tên tạm đã bị xoá hoặc đã được move thành đích; (d) `create`: `CreateHardLinkW(path, tạm)` (không ghi đè; lỗi `ERROR_ALREADY_EXISTS` ⇒ `FileExistsError`), rồi `DeleteFileW(tạm)`; `update`: `MoveFileExW(tạm, path, MOVEFILE_REPLACE_EXISTING\|MOVEFILE_WRITE_THROUGH)`; (e) đọc lại bằng `_1174_win_read(path)` phải đúng `raw` — lúc này hàm không còn sở hữu handle ghi nào; (f) `finally`: chỉ xoá ảnh TẠM còn lại (biến tên tạm khác `None`), không bao giờ xoá đích đã publish. Khi `MoveFileExW` thất bại (ví dụ đích đang được mở không share `DELETE`), hàm báo lỗi, đích giữ nguyên bytes và tệp tạm được dọn. Chú thích ghi rõ: không fsync thư mục, độ bền khai không đo được (Q13). | `.claude/dev/packet_loop.py` |
| M4 | Ca THUẦN (chạy mọi nền, ID `wp1342_pure_lock_persist_refuse`): trên nền không phải Windows, `_1174_win_lock` (ca phải ĐI VÀO context manager, `with _1174_win_lock(...)`, không chỉ gọi hàm) và `_1174_win_persist` từ chối bằng `_1174Error` với đường dẫn POSIX ("Windows drive path required") và với đường dẫn ổ đĩa hợp lệ ("native Windows required"), và KHÔNG tạo tệp nào trong thư mục tạm của ca; `_1174_win_persist` với `raw` kiểu `str` (đường dẫn ổ đĩa hợp lệ) từ chối bằng `_1174Error` "persist bytes/mode" — kiểm kiểu đứng TRƯỚC kiểm đường dẫn và nền. Trên Windows, ca chỉ kiểm vế đường dẫn POSIX (vế "native Windows required" không áp). Không thêm vào `WP1174_REQUIRED`/`WP1174_BOTH`. | `.claude/dev/packet_loop_test.py` |
| M5 | Ca NATIVE (Windows; nền khác in `BỎ QUA <lý do>` và không tính đạt), dấu hiệu dương như r1 (`WP1342_NATIVE_V1 {id, executed, passed, os, python}`), ID `wp1342_native_lock_*`/`wp1342_native_persist_*`: **L1** khoá loại trừ liên tiến trình: khi đang giữ, tiến trình con (Python, `ctypes`) mở cùng tệp share `READ\|WRITE` và gọi `LockFileEx(LOCKFILE_FAIL_IMMEDIATELY, …)` (khoá CHIA SẺ) phải thất bại `ERROR_LOCK_VIOLATION` (33); sau khi nhả, cùng lời gọi thành công; **L2** handle khoá không kế thừa (`GetHandleInformation` không có `HANDLE_FLAG_INHERIT`); **L3** tên khoá là thư mục hoặc junction ⇒ từ chối; tên chưa có ⇒ tạo, và còn tồn tại sau khi nhả; **P1** `create` tên mới ⇒ đúng bytes, không còn tệp `.wp1174-*` trong thư mục; **P2** `create` trên tên đã có ⇒ `FileExistsError`, nội dung cũ nguyên vẹn, không còn tệp tạm; **P3** `update` ⇒ đích có bytes mới, một hard link khác trỏ ảnh cũ vẫn giữ bytes cũ (như vế `replace` của probe Linux), không còn tệp tạm; **P4** `update` khi đích là thư mục hoặc junction ⇒ từ chối, đích không đổi; **P5** (chỉ VM, cần quyền symlink) `update` khi đích là symlink tệp ⇒ từ chối, symlink và tệp đích của nó không đổi; Desktop thiếu quyền ⇒ in `KHÔNG ĐO ĐƯỢC`; **P6** một handle khác giữ đích mở KHÔNG share `DELETE` ⇒ `update` báo lỗi, đích giữ nguyên bytes, không còn tệp tạm; đóng handle ấy rồi `update` lại ⇒ đạt; **B1** bindings: sáu API của M1 có đúng `argtypes`/`restype` khai ở hợp đồng ca (bảng trong ca), và `ctypes.sizeof(OVERLAPPED)` cùng offset từng trường đúng bố cục Windows cho kiến trúc của tiến trình Python đang chạy; Không dựng được điều kiện của một ca ⇒ `KHÔNG ĐO ĐƯỢC`, không in đạt. | `.claude/dev/packet_loop_test.py` |
| M6 | Đột biến Windows: KHÔNG thêm runner/bảng vào kho. Executor khai trong thân PR, cho từng đột biến, cặp (tìm, thay) khớp ĐÚNG MỘT chỗ trong head, ca đích và ca đối chứng; phiên điều phối chạy bằng driver ngoài kho trên bản sao tạm ở Desktop (khuôn driver r1, hồ sơ `ops/land/pr1363-wp1342-provenance/desktop-dot-bien/`). Một đột biến có thể gồm NHIỀU cặp (tìm, thay), mỗi cặp khớp đúng một chỗ. Ba đột biến: (a) `_1174_win_lock` đổi `LOCKFILE_EXCLUSIVE_LOCK` thành 0 (khoá chia sẻ) ⇒ L1 ĐỎ tại assertion "tiến trình con phải thất bại 33"; (b) vô hiệu hoá MỌI thao tác xoá tên tạm trên đường `create` (lời gọi xoá sau `CreateHardLinkW` VÀ đường dọn trong `finally`) ⇒ P1 ĐỎ tại assertion "còn tên `.wp1174-*`", đối chứng P3 vẫn đạt; (c) `_1174_win_persist` bỏ `MOVEFILE_REPLACE_EXISTING` ⇒ P3 ĐỎ tại một assertion hành vi có định danh (ca bắt lỗi publish và assert, không để một exception không phân loại làm ca đỏ). | `.claude/dev/packet_loop_test.py` (ca đích) |
| M7 | Helper so-additive cho r2 `_additive1342r2(base, head)` (HÀM, không đăng ký vào `CASES`): chỉ loại khỏi head những khối mới mà `_new1342` nhận VÀ có tên CHƯA tồn tại trong base; giữ nguyên byte mọi định nghĩa đã có (gồm các khối `_1174_win_*` của r1); phần còn lại phải bằng NGUYÊN BYTE base; tên mới không trùng nhau. Dùng lại `_new1342`, không sửa nó. | `.claude/dev/packet_loop_test.py` |

## 5. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux không đổi: CI Ubuntu trên exact head, `gate-packet-loop` gom `GOM: ĐẠT · 16 mảnh · <n> ca bắt buộc`; mọi ca `wp1174_*` và `wp1342_*` hiện có đạt theo tính áp dụng (ca native trên Linux là `BỎ QUA`, không khai đạt); `MUTANTS` head bằng CHÍNH XÁC base (cùng tập khoá, cùng giá trị). | Một ca đỏ; phản chứng đổi tên một khoá `MUTANTS` giữ nguyên số lượng ⇒ phép so ĐỎ. |
| N2 | Chỉ THÊM, đo MỘT LẦN trên PR (không phải ca thường trực): nạp `.claude/dev/packet_loop_test.py` của head và gọi `_additive1342r2(<blob base>, <blob head>)` với `<base>` = OID base trong lease, `<head>` = exact head; phải ra `[]`. Kèm ba phép tự kiểm của helper: base/base ⇒ `[]`; base + một hàm `_1174_win_x` hợp lệ ⇒ `[]`. Executor ghi lệnh và kết quả vào thân PR; phiên điều phối đo lại và ghi vào hồ sơ land. | Phản chứng (trong PR, trên bản sao tạm): sửa một byte trong thân `_1174_win_api` (hàm r1) ⇒ khác `[]`; sửa một byte trong `_1174_lock` ⇒ khác `[]`; thêm `@contextlib.contextmanager` vào `_1174_win_lock` ⇒ khác `[]`. |
| N3 | Không nối dây: `wp1342_additive_byte_preserved` (vế N3 trên cây làm việc) đạt trên head. | Đột biến thêm `_1174_win_lock` vào thân `_1174_lock` ⇒ ca ĐỎ (`N3 trên CÂY LÀM VIỆC`). |
| N4 | M4 đạt trên Linux (CI) và trên Windows (Desktop). | Đột biến xoá dòng kiểm kiểu `persist bytes/mode` ở `_1174_win_persist` ⇒ lỗi đổi thành "native Windows required" ⇒ vế kiểu của M4 ĐỎ trên Linux. (Bỏ kiểm `_1174_win_path` ở hàm này KHÔNG làm ca đổi màu vì `_1174_win_volume` chặn cùng thông báo — ghi thẳng, không tính là răng.) |
| N5 | Windows vẫn bị từ chối, không đổi: trên Desktop, `wp1174_windows_claim_rejected` và 12 ca `WP1174_BOTH` đạt, y hệt base cùng lượt; ca native r1 `wp1342_native_*` vẫn đạt. | Ca nào lệch base. |
| N6 | Ca native M5 (L1–L3, P1–P4, P6, B1) đạt trên Desktop, mỗi ca in dấu hiệu dương; P5 đạt trên VM `tra-luat-win` (Desktop in `KHÔNG ĐO ĐƯỢC`). | Ca native in `BỎ QUA` trên Windows ⇒ ĐỎ; P5 in đạt khi không tạo được symlink ⇒ ĐỎ; chạy riêng B1 trên bản sao MỚI sau khi bỏ khai signature `GetHandleInformation` trong `_1174_win_api_ghi` ⇒ B1 thất bại tại assertion signature có định danh (không yêu cầu L2 giữ xanh trên đột biến này, và lỗi của L2 KHÔNG tính thay cho B1); trên bản sạch L2 gọi API có signature đúng và kiểm cờ handle thật. |
| N7 | Ba đột biến M6 bị giết đúng ca đích trên Desktop, theo đúng hợp đồng N7 của r1 (exact head/tree, băm + toàn văn driver, lệnh, Python/Windows, MỌI cặp tìm/thay của đột biến, mỗi cặp khớp = 1, ca đích + đối chứng đạt trên bản sạch, bản sao MỚI, diff thực tế; chỉ tính giết khi assertion hành vi của ca đích thất bại và đối chứng đạt; tự kiểm chuỗi không khớp ⇒ `KHÔNG ĐO`). Hồ sơ land mang driver và `dot-bien.json` byte-exact (đối chiếu băm đo trên máy). | Đột biến SỐNG; hoặc ca đích "đỏ" vì lỗi import/fixture (phải phân loại `KHÔNG ĐO`). |
| N8 | Ruff `--select F` delta 0 trên hai tệp; `adr-song`, `doctrine-scan` rc 0; `git diff --check` sạch; `eol_policy --all` ok; `git diff --numstat base..H` ≤ 2 tệp và ≤ 450 dòng thêm (`ADR-0053`). | Một gate thất bại ⇒ ĐỎ; vượt trần ⇒ dừng theo §7. |

Đo Windows (N4 phần Windows, N5–N7) do phiên điều phối chạy trên **`DESKTOP-T9R33P2`** (ưu tiên, Q8), VM `tra-luat-win` cho P5 và dự phòng; base và head trong cùng một lượt; không chạy trọn bảng đột biến trên Windows.

## 6. `pham_vi_e`

Không chạm E4, không chạm E5. Không đảo quyết định "chỉ Linux" (Windows vẫn bị từ chối, primitive chưa nối), nên không E3.

## 7. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; trần vòng review theo `ADR-0048` và protocol. Chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- `git diff --numstat` vượt `ADR-0053` ⇒ dừng; câu hỏi mang **E2** (mức đã dùng, còn thiếu, để làm gì).
- Cần sửa thân một định nghĩa hiện có, cần sửa ngoài write set, hoặc cần nối dây để một tiêu chí đạt ⇒ dừng triển khai và đi revision đặc tả theo protocol. Chỉ hỏi **E1** khi đã xét lại cách làm mà không còn phương án có phép đo chống đỡ (kèm gốc rễ, phương án đã thử, đề xuất); thiếu quyền thuộc **E2**.
- Đặc tả này không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2** (quyền duyệt thuộc chủ kho), một lần, sau khi review độc lập approve.
- Desktop và VM cùng offline quá hạn lease ⇒ **E2**.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục. Ghi chú từ r1 (không phải bộ đếm lỗi): driver đột biến r1 cần ba lượt vì hai lỗi DRIVER ngoài kho (clone đường dẫn quá dài; phân loại đọc sai kiểu lỗi trả về dạng chuỗi); driver r2 dùng lại bản đã sửa (sha256 `1ee98b9c…` làm khuôn) với `MUT_GOC` ngắn và `core.longpaths`.

## 9. Sổ quyết định của lượt soạn

Chủ kho 17-11-2026 (phiên điều phối #1206): đồng ý ba khuyến nghị — (1) làm bậc r1b ngay (bậc nối dây cần cả r1b và r1c theo số đo §0); (2) tách r1b: khoá + publish ở revision này, probe sang r1c; (3) review độc lập Codex đặc tả (tối đa 4 lượt, con số do chủ kho chọn trong khuyến nghị) trước khi chủ kho duyệt băm một lần (E2, `ADR-0067`). Giữ nguyên các quyết định r1: Q3, Q6, Q7, Q8, Q11, Q13.

Sau review độc lập lượt 1 (`request_changes`, 2 P1 + 3 P2 + 2 P3, `ops/reviews/wp1342-spec-r2/luot1.stdout.txt`): thêm helper so-additive riêng M7 (F1); `_1174_win_lock` không decorator (F2); đột biến (b) gồm mọi đường xoá tạm, cho phép nhiều cặp (F3); vòng đời handle trong M3 + ca P6 (F4); bindings cắt còn sáu API + ca B1 (F5; lượt 2 G1: nói rõ `GetHandleInformation` phục vụ L2 và cách chạy riêng đột biến của B1); số đo §0 đo lại kèm mốc giờ (F6); mã E cho câu chờ chủ kho (F7).

Quyết định của người soạn trong hướng đã duyệt: bindings ghi trong hàm MỚI `_1174_win_api_ghi` (không sửa `_1174_win_api`); mở-có-tạo của khoá gọi `CreateFileW` trực tiếp (không sửa `_1174_win_open` cứng `OPEN_EXISTING`); phép "chỉ thêm" đo một lần lúc PR thay vì ca thường trực; đột biến (b) chọn bước xoá tệp tạm thay vì đổi link thành replace vì vế kiểm tồn tại trước đã chặn `create` trên tên có sẵn nên đột biến đổi link không đổi màu ca nào.

## 10. `chua_do_duoc`

- Kích thước thật: ước lượng tĩnh ~320–480 dòng thêm (người soạn và review độc lập); có thể vượt trần, khi đó theo §7.
- Độ bền sau mất điện: không fsync thư mục trên Windows; `MOVEFILE_WRITE_THROUGH` và `FlushFileBuffers` khai, không đo được (Q13).
- Khoá chặn vô hạn (`LockFileEx` không timeout) giống `flock`; không có ca đo khoá chết.
- P5 (symlink tệp) chỉ đo được trên VM có quyền; Desktop ghi `KHÔNG ĐO ĐƯỢC`.
- Hành vi trên ReFS/ổ mạng: bị từ chối ở `_1174_win_volume`, không đo năng lực.
