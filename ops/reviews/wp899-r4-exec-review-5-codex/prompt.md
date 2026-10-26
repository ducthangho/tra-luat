# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 4**, lượt 5, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `22da28c738e651361274c1264e681a52461dad1e` |
| lượt trước (r4 lượt 4) | `75d0f6b5fe01611dda0b8768e50f5826657135e7` = cha của HEAD; verdict `.review-input/r4-luot4/VERDICT.md` (changes_requested: F10 P1, bốn nhóm, 17 đột biến sống). `.review/` lượt 4 ở `.review-input/r4-luot4/`; lượt 1–3 ở `.review-input/r4-luot{1,2,3}/` |
| điểm xuất phát / base | `fe7522e` (ba tệp từ ứng viên r3 `7f5a02c`) / `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả r4 | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN; r3/r2 cùng thư mục cho các mục được dẫn |
| verdict r3 | `.review-input/r3-luot1/`, `.review-input/r3-luot2/` |
| A10 / log thật | `.review-input/a10/` (đo trên `52e9573`) · `.review-input/log-that/` + `SHA256SUMS` |
| tự đột biến của executor | `.review-input/tu-dot-bien/` (`tu_dot_bien*.py` hai vòng tay + `toan_tu.py` đột biến TOÁN TỬ tự động trên mọi hàm r4, kết quả `kq*.txt`; script trỏ đường dẫn tuyệt đối của executor — đọc làm tham chiếu, chạy lại bằng phép đo của bạn) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff 75d0f6b HEAD`; toàn bộ: `git diff ba222ff HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q12 của đặc tả r4.
- **Quyết định chủ kho sau checkpoint V5 của lượt 2** (phiên executor, 25-10-2026, trả lời checkpoint #899
  issuecomment-6393643859): *(1) đẩy nhánh lưu trữ — đã đẩy `ops/wp899-g3-luu-tru` @ `e47df3b`; (2) **nâng trần**; tiếp tục vòng
  vá tới hết P1, P2; không đẩy nhánh code, không chạy gate nặng cho tới khi đủ điều kiện merge.* Vì vậy V5 KHÔNG còn dừng packet ở
  lượt này; trần dòng do chủ kho nâng mà chưa nêu số — numstat hiện tại 1 + 444 + 1060 = **1505**. Không coi việc vượt 1250 là
  finding; báo con số nếu bạn thấy cần.
- Ngân sách Codex: đây là lời gọi **5/8** của r4; sau lượt này còn 3, gồm cả lượt connector sau lần đẩy (chủ kho chưa đổi trần lời gọi).
- `gioi_han_khai` của r4: đường cần quyền sửa nội dung tại SHA checkout là giới hạn khai.

## Executor đã làm gì sau lượt 4 (đánh giá, đừng nhận lời)

1. Chạy lại NGUYÊN `new_frontier.py` lượt 4 của bạn trên HEAD: **20/20 GIET** (sau khi thêm alias có khoảng trắng hai đầu cho
   `job_alias_strip`). Mã sản phẩm KHÔNG đổi ở lượt này (`git diff 75d0f6b HEAD -- ops/ci_provenance.py` rỗng).
2. Ba lượt liền F10 lặp vì executor vá theo danh sách đột biến. Lượt này đóng LỚP bằng **c48 — bảng biến dạng**: MỌI hằng chuỗi và
   tập liệt kê của mã r4 (tên metadata `Set up job`/`Complete job`, `Post `, `Run `, tên REST, alias `name:` của job (kể cả có
   khoảng trắng hai đầu và ký tự regex), `conclusion`, `CI_DANG_KY_`, `shell`, khoá allowlist, `GITHUB_ENV`/`GITHUB_PATH`
   (chữ thường, không `$`, đứng trước mà skipped), header/`shell:`/`##[endgroup]` của khối, mã màu `36m`, `##[group]run` thường,
   `##[GROUP]` hoa, `run:` có `\r`, giờ REST thiếu `Z`, `uses: ""` ở bước/job, `name: null`, `run: ""` kèm `uses:`) đi qua
   hàm `bien_dang` (hậu tố, bớt ký tự cuối, hoa/thường/đảo hoa, khoảng trắng hai đầu); kỳ vọng mỗi hàng lấy từ định nghĩa NGUYÊN
   VĂN của spec, đòi cả `ghep_buoc` lẫn danh sách marker. **119 hàng.**
3. Executor tự sinh **35 đột biến chuẩn hoá** (strip/lower/re.I/match/splitlines/tập liệt kê/điều kiện đã chạy…, `tu-dot-bien/
   mau_chuan_hoa.py` + `khung.py`, kết quả `kq6.txt`): 34 GIET; 1 khai TƯƠNG ĐƯƠNG — `n_goi_strip_run` (`run.strip()` thay
   `run.rstrip("\n")` trước `dong_logic`): `dong_logic` đã strip từng dòng logic và bỏ dòng rỗng, còn khối chỉ được xét khi
   `run.rstrip("\n")` BẰNG khối in lại. Kiểm lời khai. Đột biến toán tử tự động lượt trước (`toan_tu.py`, `kq4.txt`) vẫn hiệu lực
   vì mã sản phẩm không đổi.
4. DOT_BIEN thêm 20 đột biến lượt 4 của bạn + 34 đột biến chuẩn hoá (ca đích = ca đo được là giết). Suite tại chỗ:
   `CA: 48/48 dat` · `DOT BIEN: 209/209 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
5. A9/A10 chưa chạy lại (chủ kho: chỉ chạy chỗ thay đổi; A10 chạy một lần trên SHA cuối). Mã sản phẩm không đổi so `75d0f6b`, nên
   REPLAY A10 offline trên `75d0f6b` của bạn (nếu có) vẫn áp; không có thì replay lại.

## Hạng — nói rõ để hai lượt đếm cùng một thước

Đột biến SỐNG là P1 khi nó đổi kết quả trên một đầu vào mà đặc tả ĐỊNH NGHĨA kết quả (M4/M12, `dinh_nghia`, A1–A27) — tức chốt đặc
tả đòi mà ca không có răng. Đột biến sống chỉ ở miền đặc tả KHÔNG định nghĩa (chọn tuỳ ý giữa hai hành vi đều fail-closed, hay một
đầu vào mà runner thật không sinh) thì ghi P3 kèm đề xuất quyết định, và nói rõ vì sao đặc tả không định nghĩa nó. Đột biến làm
công cụ NÉM ở một đầu vào mà đặc tả đòi "không ném" là P1/P2 như cũ.

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F11**: chạy lại MỌI script lượt 1–4 của bạn (`.review-input/r4-luot{1,2,3,4}/`); F10 phải được chứng minh ĐÓNG
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
