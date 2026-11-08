# Review Codex offline lượt 9: packet #1252 LAUNCHER-READONLY-IGNORED r1 (Review Class: sensitive) — bản vá A10 Windows + F11

Bạn là reviewer độc lập (họ OpenAI). Lượt này CHỈ ĐỌC trên thư mục làm việc.

**QUY TẮC TUYỆT ĐỐI: KHÔNG ghi bất kỳ tệp nào trong thư mục làm việc này.** Cấm cả:
- tệp bị `.gitignore` bỏ qua, `__pycache__`, `review-evidence/`;
- `.git/**`, kể cả `git config` cục bộ;
- ghi rồi dọn sau.

Lượt chạy bằng `launcher.py run --chup-workspace` của chính ứng viên. Một lần ghi vào cây là lượt vô hiệu.

**Bước đầu tiên:** `git clone --no-hardlinks <thư mục làm việc> /tmp/rv1252i-copy`, rồi `git config core.abbrev 7` trong bản sao.
- Mọi test, đột biến, script đo và hiện vật đều chạy TRONG bản sao.
- `TMPDIR` đặt ngoài cả hai cây.

## Neo
- HEAD phải là `e6c650573452ad98c3055f5147eeacfb4767f119`. Khác thì kết luận `request_changes`.
- `e6c6505` = `77f638d` (merge: cha 1 `dd2a820` bản vá A10 trên `9e564d4`; cha 2 `9607e3e` master, chỉ thêm `ops/specs/wp1179-*`) + commit F11 (chỉ sửa test).
- Base packet: `889334fb87c25136a13c6776a40a25b401820e04`. Spec: `ops/specs/launcher-readonly-ignored-r1.md`, sha256 `b2c52a9aaf4a347dc212ad26d4b0ff83fb9cd58a70252e42f66d81b4d8d897cf`.
- Trần kích thước do chủ kho nâng (07-11-2026): **≤ 2 tệp / ≤ 1080 dòng thêm** trong `.claude/dev/**` so với base.
- Lượt 9 trên trần cứng 10 (ADR-0055). Lượt 7 chết vì đĩa đầy; lượt 8 trên `77f638d`: 1 P2 (F11). Chủ kho chọn vá F11 cơ học và push `e6c6505` TRƯỚC lượt này (lệch thứ tự M12, đã ghi trên #1252); lượt này là review trên đúng SHA đã push.

| Lượt | SHA | Kết quả |
|---|---|---|
| 1–5 | … | F1–F9, đã vá |
| 6 | `c9588aa` | 0 P1 / 1 P2 (F10), vá cơ học ở `e0aeb97` theo chủ kho |
| connector | `e0aeb97` | 3 P2, vá ở `9e564d4`; connector lại trên `9e564d4`: sạch |

## Bối cảnh lượt này: A10 Windows trên `9e564d4` ĐỎ 2/22 ca
Chạy trên máy chủ kho (Windows, Python 3.12.10), `--lap-ca <ca> --lan 3`:
1. `r1252_doi_to_tien_thu_muc_luot`: 3/3 hỏng, `du_phong: phai ra 17/... : rc=16 None`.
   Chẩn đoán trên cùng máy: tiến trình con gọi `os.rename(R, R+'-goc')` lên thư mục chứa thư mục lượt ⇒
   `PermissionError(13, 'Access is denied')` (launcher đang giữ `stdout.log` mở bên trong). Đòn "lái tổ tiên"
   KHÔNG dựng được trên Windows; rc 16 chỉ do con `makedirs` vào workspace.
2. `r1252_ghi_tep_ignored`: 1/3 hỏng (`rc=17 khong_do_duoc_workspace`), chạy lại 10/10 đạt — không tái hiện.
   Giả thuyết CHƯA ĐO: job Windows cập nhật danh sách PID trễ sau khi con thoát ⇒ `_cay_da_chet` False ⇒ 17.
   (`_giet_cay` vốn đã `sleep(0.3)` sau `TerminateJobObject` vì cùng hiện tượng.)

## Bản vá `dd2a820` (diff `9e564d4..dd2a820`, +24/−6)
- `_cay_da_chet` (Windows): poll tối đa 20×0,1 s; `[]` ⇒ True; `None` ⇒ False ngay; còn PID ⇒ ngủ rồi hỏi lại, hết hạn ⇒ False.
- Ca `(d')` thêm biến thể job báo `[7],[7],[]` ⇒ phải True. Đột biến mới `r1252_windows_khong_cho_job` (`range(20)`→`range(1)`); đích của `r1252_windows_khong_dung_job` chuyển sang dòng `return ds == []`.
- Fixture `r1252_doi_to_tien_thu_muc_luot`: con bắt `PermissionError` ở `os.rename` thì ghi tệp dấu `KL` (ngoài workspace) và thoát 0. Có dấu ⇒ chỉ đạt khi `os.name == "nt"`, rc 16 và không có `snapshot_tep_chup_bo_qua`; mọi chế độ đều bị từ chối ⇒ ca trả `bo qua` có lý do. Trên Linux cả hai chế độ vẫn đo như trước.
- Ca `r1252_ghi_tep_ignored` chỉ in thêm `snapshot_ly_do` trong thông báo.

## Lượt 8 → F11 (vá ở `e6c6505`, diff `77f638d..e6c6505`, chỉ `launcher_test.py`)
- F11 `windows-poll-khong-khoa-khoang-cho`: job giả trả rỗng theo số lần hỏi nên đột biến bỏ `time.sleep(0.1)` sống. Vá: ca `(d')` thay `m.time` bằng bộ ghi lần ngủ; job chỉ rỗng khi tổng đã ngủ ≥ 0,19 s. Đột biến mới `r1252_windows_bo_ngu`. Executor đo: 53/53 đột biến `r1252_*` giết đúng ca đích.
- Diff `.claude/dev/**` so base: 2 tệp, +1079/−8 (trần ≤ 1080).
- Đã đo SAU push (để biết, không thay review): connector sạch trên `e6c6505`; A10 Windows (máy chủ kho) 22 ca × 3: 51 qua, 15 bỏ qua có lý do nền (gồm `doi_to_tien` vì Windows từ chối rename), 0 hỏng; `launcher_test --dot-bien` Linux 655/655.

## PHÂN CÔNG
- **KHÔNG tự viết script tấn công, race, symlink, thoát thư mục hay phản chứng mới dạng ấy.** Hướng thử cần nội dung đó thì MÔ TẢ BẰNG LỜI.
- Việc của lượt này:
  1. CHẠY các ca `r1252_*` (22 ca) và các đột biến `r1252_*` (53) có sẵn — bộ chạy lọc tiền tố: nạp `launcher_test.py` bằng `importlib`, giữ mục `DOT_BIEN` có tên bắt đầu `r1252_`, gọi `chay_dot_bien()`;
  2. ĐỌC diff `9e564d4..e6c6505` (và lướt `889334f..HEAD -- .claude/dev`);
  3. ĐỘT BIẾN BẢN VÁ một dòng trong bản sao rồi chạy ca đích để đo răng.
- Gốc workspace có sẵn `.aws/` và `.codex/` rỗng, tạo trước mốc chụp. Đừng xoá.

## Việc phải kiểm
1. **Poll `_cay_da_chet`:** có làm yếu phép chứng minh "cây đã chết" không (vd. coi `None` thành True, hay kết luận True khi job còn PID)? Thời gian chờ tối đa có chấp nhận được không? Có ảnh hưởng đường quá hạn/ngắt không?
2. **Fixture `doi_to_tien`:** lối ra `bo qua` có thể mở trên Linux/macOS không (tức che mất phép đo F1 ở nền có dir_fd)? Điều kiện `os.name == "nt"` có đủ chặt? Ca còn đo điều gì trên Windows?
3. Có đột biến nào của bản vá SỐNG không.
4. F1–F11 và 3 P2 connector vẫn đóng; A1 so nền trong CÙNG môi trường (chỉ thêm ca `r1252_*`).
5. Lỗi thật khác, nếu có. A10/A11/A14: ghi `chua_do_duoc`.

## Đầu ra
- Phát hiện theo bậc P0/P1/P2/P3, mỗi phát hiện kèm slug lớp và lệnh tái hiện bằng ca/đột biến có sẵn (không có thì mô tả bằng lời).
- Khai rõ lệnh nào có thể ghi đã chạy ở bản sao nào.
- Dòng CUỐI CÙNG của stdout là ĐÚNG MỘT dòng, chữ thường:
  - `KET_LUAN: approve` nếu không còn P0/P1/P2;
  - ngược lại `KET_LUAN: request_changes`.
