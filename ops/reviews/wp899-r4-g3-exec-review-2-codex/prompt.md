# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 4**, lượt 2, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `52e9573d0bd401a629a031a9c32df7bfd17c27c1` |
| lượt trước (r4 lượt 1) | `ca11a6f1a7eb5286eeb6efc730d99beb33e2dcd1` = cha của HEAD; verdict `.review-input/r4-luot1/VERDICT.md` (changes_requested: F09 P0, F10 P1, F11 P2, cả ba MỚI). Toàn bộ `.review/` của lượt 1 (script, probe, mutant, kết quả) ở `.review-input/r4-luot1/` |
| điểm xuất phát | `fe7522e` (ba tệp từ ứng viên r3 `7f5a02c`) |
| base | `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả r4 | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN; r3/r2 cùng thư mục cho các mục được dẫn |
| verdict r3 | `.review-input/r3-luot1/`, `.review-input/r3-luot2/` |
| A10 | `.review-input/a10/` (đo LIVE lại trên HEAD này); log đầy đủ 37 job ở `.review-input/log-that/` kèm `SHA256SUMS` |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff ca11a6f HEAD`; toàn bộ: `git diff ba222ff HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q12 của đặc tả r4. Trần **≤ 3 tệp / ≤ 1250 dòng thêm**. Executor khai numstat so `ba222ff` = 1 + 444 + 805 = **1250**
  (chạm trần, không còn dư).
- **V5 — ĐÂY LÀ LƯỢT 2 CỦA r4, lời gọi Codex 2/8.** Một lớp — F01–F11 — **lặp ở lượt này ⇒ packet DỪNG HẲN**. Phân loại
  CHÍNH XÁC theo nguyên nhân, không theo vị trí: biểu hiện mới cùng nguyên nhân với một lớp đã có là LẶP LỚP; nguyên nhân khác
  thì slug mới. Đừng nới để cứu packet, cũng đừng gộp một nguyên nhân khác vào lớp cũ cho tiện.
- `gioi_han_khai` của r4: đường cần quyền sửa nội dung tại SHA checkout là giới hạn khai, không phải finding.

## Executor đã vá gì sau lượt 1 (đánh giá, đừng nhận lời)

1. **F09**: `_gio(v, mau=RE_GIO)` parse lịch thật (`datetime.strptime` trên 19 ký tự đầu) SAU khi khớp dạng; dùng cho cả
   `started_at`/`completed_at` (dạng `…Z`) và giờ header (dạng `TS` của log, cắt về giây). Sai dạng hay sai lịch ⇒ `None` ⇒ vế (c)
   hỏng ⇒ cả job không marker, không ném. c38 thêm sáu biến thể REST (30/2, tháng 13, giờ 24, phút 99, giây 99, offset `+00:00`)
   và hai biến thể header (thiếu timestamp, 30/2) với cửa sổ REST hợp lệ bao quanh. Đột biến: bỏ kiểm lịch, nhận offset, lấy giờ
   REST khi header thiếu; `A22_khong_cat_giay` đổi neo theo hàm mới.
2. **F10**: c37 thêm bốn biến thể state sau `buoc_rest`: đảo thứ tự `steps[]` (giữ `number`) ⇒ passed; `number` trùng ⇒
   `steps_rest_sai_dang`; `run:` có dòng đầu rỗng ⇒ tên `Run ` khớp ⇒ passed; `name:` có `${{` ⇒ `b_ten_buoc_lech`. Bốn đột biến
   tương ứng. **Quét cả lớp:** ca mới c44 cho MỌI chốt dạng còn lại của `ghep_buoc`/`ghep_job` (`number` thiếu/bool, phần tử
   `steps[]` không phải dict, bước YAML không phải dict, job YAML không phải dict) ⇒ đúng `ly_do`, không ném; mỗi chốt một đột biến.
3. **F11**: c42 lặp ba đối chứng trên cả `GITHUB_ENV` lẫn `GITHUB_PATH`; đột biến bỏ PATH.
4. Suite tại chỗ: `CA: 44/44 dat` · `DOT BIEN: 99/99 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
5. Executor đã chạy lại script của bạn ở lượt 1 trên bản này (`calendar_cases.py`, `verify_new_cases.py`, `extra_mutants_r4.py`):
   calendar cả sáu ca `not_measured`; các ca reviewer DAT; các mutant lượt 1 có neo đổi (`gio_*` dùng neo cũ `b["gio"][:19]`) được
   executor chạy lại trên neo mới `a <= h <= z` (bỏ cận dưới, bỏ cận trên) và đều GIET c38. `number_missing_tu_sinh` bị bộ phân hạng
   của bạn xếp TIN_DUNG_GIA vì làm công cụ NÉM ở ca khác (fail-loud), còn ca đích c44 chết đúng `TinHieuChotCa`. Hãy tự chạy lại.
6. A10 LIVE trên HEAD này: provenance của cả hai run **trùng byte** với lượt 1 (`5ad9afea…afe0`, `24ffa770…185b`).
7. A9 (`ci_dang_ky_test.py --chay`, đo trên cây đang vá dở giữa ca11a6f và HEAD): `ops/ci_provenance_test.py: ĐẠT rc=0`; tổng ĐỎ do
   hai test ngoài write set: `pretooluse_guard_test.py` (38/41, đỏ y hệt trên base `ba222ff` ⇒ delta 0) và `nhanh_don_duoc_test.py`
   hết giờ 5400 s (`LỖI HẠ TẦNG`). Executor sẽ đo lại A9 trên SHA cuối trước khi đẩy.

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F11**: F09–F11 phải được chứng minh ĐÓNG bằng phản chứng chạy được (chạy lại MỌI script lượt 1 của bạn từ
   `.review-input/r4-luot1/`, thêm biến thể cùng cơ chế); F01–F08 giữ đóng, F02 chạy lại phản chứng r3.
4. Chạy ca có sẵn; đột biến trên BẢN SAO TẠM (`python -B`, `PYTHONDONTWRITEBYTECODE=1`, `CI_PROVENANCE_MA=<bản sao>`); chỉ tính
   giết khi ca đích chết bởi `TinHieuChotCa` của ĐÚNG ca. Báo mutant nào SỐNG.
5. Quét lớp MỚI do bản vá sinh (parse lịch: năm 0000, ngày 29/2 năm nhuận/không nhuận, phần thập phân header dài, timestamp header
   có khoảng trắng, so datetime naive; c44: ca nào có mặt mà không đo).
6. **Không tự soạn nội dung tấn công nhạy cảm**; hướng nào cần thì MÔ TẢ BẰNG LỜI.
7. Review theo LỚP (V3).

## Hạng

- **P0**: bằng chứng sai theo hướng có lợi (thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3), hoặc rò credential.
- **P1**: vi phạm M1–M12/A1–A27 đo được; ca/mutant không có răng ở chốt đặc tả đòi.
- **P2**: lỗi thật nhưng hẹp, hoặc ca có mặt mà không đo.
- **P3**: nợ/chất lượng; kèm đề xuất quyết định có căn cứ.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; rồi `reviewed_sha:`, `base_sha:`, `Reviewed commit: <40 hex>`.
Approve CHỈ khi P0 = P1 = P2 = 0 (V2), mỗi P3 có quyết định đề xuất. Bắt buộc: bảng ĐỐI CHIẾU F01–F11; **BẢNG LỚP**
`| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |`; ghi rõ lớp nào LẶP (⇒ V5) và lớp nào mới;
đối chiếu A1–A27; danh sách mutant kèm hạng. Không khẳng định thứ chưa đo; không đo được thì ghi `KHÔNG ĐO ĐƯỢC`.
