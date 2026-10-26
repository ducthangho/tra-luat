# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 4**, lượt 7, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `9b329bfab0b38a821992a7105d479ca44bed389b` |
| lượt trước (r4 lượt 6) | `35453ff30170998ffea663801299db5876cc8e0c` = cha của HEAD; verdict `.review-input/r4-luot6/VERDICT.md` (changes_requested: F10 P1, 26 đột biến sống — 25 P1, 1 P3 tương đương). `.review/` lượt 6 ở `.review-input/r4-luot6/`; lượt 1–5 ở `.review-input/r4-luot{1,2,3,4,5}/` |
| điểm xuất phát / base | `fe7522e` (ba tệp từ ứng viên r3 `7f5a02c`) / `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả r4 | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN; r3/r2 cùng thư mục cho các mục được dẫn |
| verdict r3 | `.review-input/r3-luot1/`, `.review-input/r3-luot2/` |
| A10 / log thật | `.review-input/a10/` (đo trên `52e9573`) · `.review-input/log-that/` + `SHA256SUMS` |
| tự đột biến của executor | `.review-input/tu-dot-bien/` (`tu_dot_bien*.py` hai vòng tay + `toan_tu.py` đột biến TOÁN TỬ tự động trên mọi hàm r4, kết quả `kq*.txt`; script trỏ đường dẫn tuyệt đối của executor — đọc làm tham chiếu, chạy lại bằng phép đo của bạn) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff 35453ff HEAD`; toàn bộ: `git diff ba222ff HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q12 của đặc tả r4.
- **Quyết định chủ kho sau checkpoint V5 của lượt 2** (phiên executor, 25-10-2026, trả lời checkpoint #899
  issuecomment-6393643859): *(1) đẩy nhánh lưu trữ — đã đẩy `ops/wp899-g3-luu-tru` @ `e47df3b`; (2) **nâng trần**; tiếp tục vòng
  vá tới hết P1, P2; không đẩy nhánh code, không chạy gate nặng cho tới khi đủ điều kiện merge.* Vì vậy V5 KHÔNG còn dừng packet ở
  lượt này; trần dòng do chủ kho nâng mà chưa nêu số — numstat hiện tại 1 + 444 + 1289 = **1734**. Không coi việc vượt 1250 là
  finding; báo con số nếu bạn thấy cần.
- Ngân sách Codex: đây là lời gọi **7/8** của r4 — LƯỢT OFFLINE CUỐI; lời gọi 8/8 dành cho connector sau lần đẩy (chủ kho chưa đổi trần lời gọi).
- `gioi_han_khai` của r4: đường cần quyền sửa nội dung tại SHA checkout là giới hạn khai.

- **Hai quyết định chủ kho sau checkpoint lượt 5** (#899 issuecomment-6394979394, trả lời trong phiên executor 25-10-2026):
  (1) **tiêu chí phân hạng đã chốt**: đột biến SỐNG là P1 khi nó đổi kết quả trên đầu vào mà đặc tả ĐỊNH NGHĨA kết quả (M4/M12,
  `dinh_nghia`, A1–A27, D01 dưới đây); đột biến chỉ sống ở miền đặc tả KHÔNG định nghĩa ⇒ P3 kèm đề xuất quyết định và lý do
  vì sao đặc tả không định nghĩa; đột biến làm công cụ NÉM ở đầu vào đòi "không ném" ⇒ P1/P2. (2) **D01: `env: null` ở job hoặc
  workflow ⇒ CHẶN** (null không phải dict); khoá `env:` VẮNG ⇒ không chặn.
- **Quyết định chủ kho sau checkpoint lượt 6** (#899 issuecomment-6396568278): *vá rồi một lượt review nữa* (lượt này), giữ lời gọi
  cuối cho connector. Tiêu chí phân hạng và D01 ở trên giữ nguyên.

## Executor đã làm gì sau lượt 6 (đánh giá, đừng nhận lời)

Mã sản phẩm KHÔNG đổi (`git diff 35453ff HEAD -- ops/ci_provenance.py` rỗng); chỉ `ops/ci_provenance_test.py`.

1. **c50** — mỗi đầu vào làm 25 đột biến P1 lượt 6 của bạn đổi kết quả, dựng lại thành hàng có kỳ vọng theo định nghĩa spec, đòi
   `ghep_buoc` + trọn danh sách marker; mỗi hàng dựng lười và bắt ngoại lệ. Hai hàng có chốt riêng: `##[endgroup]` MÀU trong khối
   (đòi `buoc_xac_thuc == 0`); dòng không màu SAU `shell:` (metadata hợp lệ ⇒ marker) và TRƯỚC `shell:` (không hợp lệ).
2. **c49** đòi mọi phân hoạch được lấy mẫu ≥ 5 lần (marker passed/failed/chặn; ghép passed và hỏng từng vế a/b/c/d/dạng; job đích
   không đứng đầu; `number` ≥ 10) — trên hạt giống hiện tại nhỏ nhất là 10.
3. DOT_BIEN thêm 24 đột biến lượt 6 của bạn (neo nguyên văn của bạn; `env_only_keys_str` không thêm vì bạn đã khai P3 tương đương).
   Đo bằng khung tự đột biến (`tu-dot-bien/khung_l6.py`, `kq10.txt`): 24/24 giết ở c50; `rest_number_order_contiguous` đồng thời làm
   c22 ném `ValueError` (min trên steps rỗng) — c22 chỉ bắt hai lớp lỗi chiếu dữ liệu từ r2.
4. Suite tại chỗ: `CA: 50/50 dat` · `DOT BIEN: 255/255 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
5. A9/A10 chưa chạy lại (mã sản phẩm không đổi từ `35453ff`).

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F11**: chạy lại MỌI script lượt 1–6 của bạn (`.review-input/r4-luot{1,2,3,4,5,6}/`); F10 phải được chứng minh ĐÓNG
   CẢ LỚP — tự đột biến thêm mọi chốt dạng/miền giá trị/vị trí của `ghep_job`/`ten_du_kien`/`_gio`/`ghep_buoc`/`chan_buoc`/
   `do_dau_duong`/`tach_buoc` mà executor chưa thử; báo mọi đột biến SỐNG.
4. Đột biến trên BẢN SAO TẠM (`python -B`, `PYTHONDONTWRITEBYTECODE=1`, `CI_PROVENANCE_MA=<bản sao>`); chỉ tính giết khi ca đích
   chết bởi `TinHieuChotCa` của ĐÚNG ca; đột biến làm công cụ NÉM ở một ca không bắt ngoại lệ là TIN_DUNG_GIA — báo riêng.
5. Replay A10 offline (mục 7 trên); khác provenance trên `52e9573` thì giải thích từng khác biệt.
6. **Không tự soạn nội dung tấn công nhạy cảm**; hướng nào cần thì MÔ TẢ BẰNG LỜI. Review theo LỚP (V3).

## Hạng

- **P0**: bằng chứng sai theo hướng có lợi (thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3), hoặc rò credential.
- **P1**: vi phạm M1–M12/A1–A27 đo được; ca/mutant không có răng ở chốt đặc tả đòi.
- **P2**: lỗi thật nhưng hẹp, hoặc ca có mặt mà không đo.
- **P3**: nợ/chất lượng; kèm đề xuất quyết định có căn cứ.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; rồi `reviewed_sha:`, `base_sha:`, `Reviewed commit: <40 hex>`.
Approve CHỈ khi P0 = P1 = P2 = 0 (V2), mỗi P3 có quyết định đề xuất. Bắt buộc: bảng ĐỐI CHIẾU F01–F11; **BẢNG LỚP**
`| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |`; lớp nào lặp, lớp nào mới; đối chiếu A1–A27;
danh sách mutant kèm hạng (gồm đột biến bạn tự thêm); kết quả replay A10. Không khẳng định thứ chưa đo; không đo được thì ghi
`KHÔNG ĐO ĐƯỢC`.
