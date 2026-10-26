# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 4**, lượt 4, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `75d0f6b5fe01611dda0b8768e50f5826657135e7` |
| lượt trước (r4 lượt 3) | `27997a73c6b01e577ed655ea94e73d56adf697da` = cha của HEAD; verdict `.review-input/r4-luot3/VERDICT.md` (changes_requested: F10 P1, bốn nhóm biểu hiện, 28 đột biến sống). `.review/` lượt 3 ở `.review-input/r4-luot3/`; lượt 1, 2 ở `.review-input/r4-luot{1,2}/` |
| điểm xuất phát / base | `fe7522e` (ba tệp từ ứng viên r3 `7f5a02c`) / `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả r4 | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN; r3/r2 cùng thư mục cho các mục được dẫn |
| verdict r3 | `.review-input/r3-luot1/`, `.review-input/r3-luot2/` |
| A10 / log thật | `.review-input/a10/` (đo trên `52e9573`) · `.review-input/log-that/` + `SHA256SUMS` |
| tự đột biến của executor | `.review-input/tu-dot-bien/` (`tu_dot_bien*.py` hai vòng tay + `toan_tu.py` đột biến TOÁN TỬ tự động trên mọi hàm r4, kết quả `kq*.txt`; script trỏ đường dẫn tuyệt đối của executor — đọc làm tham chiếu, chạy lại bằng phép đo của bạn) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff 27997a7 HEAD`; toàn bộ: `git diff ba222ff HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q12 của đặc tả r4.
- **Quyết định chủ kho sau checkpoint V5 của lượt 2** (phiên executor, 25-10-2026, trả lời checkpoint #899
  issuecomment-6393643859): *(1) đẩy nhánh lưu trữ — đã đẩy `ops/wp899-g3-luu-tru` @ `e47df3b`; (2) **nâng trần**; tiếp tục vòng
  vá tới hết P1, P2; không đẩy nhánh code, không chạy gate nặng cho tới khi đủ điều kiện merge.* Vì vậy V5 KHÔNG còn dừng packet ở
  lượt này; trần dòng do chủ kho nâng mà chưa nêu số — numstat hiện tại 1 + 444 + 946 = **1391**. Không coi việc vượt 1250 là
  finding; báo con số nếu bạn thấy cần.
- Ngân sách Codex: đây là lời gọi **4/8** của r4 (chủ kho chưa đổi trần lời gọi).
- `gioi_han_khai` của r4: đường cần quyền sửa nội dung tại SHA checkout là giới hạn khai.

## Executor đã làm gì sau lượt 3 (đánh giá, đừng nhận lời)

1. Chạy lại NGUYÊN `frontier.py` + `frontier2.py` của bạn trên HEAD: 59/61 GIET. Hai con còn lại: `log_group_close_exact` là
   `HONG_NEO` vì mã giờ CHÍNH LÀ bản ấy (so `##[endgroup]` nguyên văn — đo 753/753 dòng đóng trên 37 log thật; chiều ngược lại có
   đột biến `L3_endgroup_startswith`); `log_nested_after_only` executor khai TƯƠNG ĐƯƠNG: trước `shell:` mọi dòng không màu
   mà không bắt đầu bằng `shell: ` đã làm `ok` sai, kể cả `##[group]…`. Kiểm lời khai.
2. **c46** (miền chặn chế độ, mỗi biến thể một trục, có chặn lẫn đối chứng): `env` job `[]`/list/biểu thức/`{}`, `env` workflow
   dict, `defaults: {}` hai mức, `shell` null/sh/pwsh, từng khoá allowlist `id`/`if`/`timeout-minutes`/`continue-on-error`; khối
   nhiều dòng chỉ một dòng có `VAR=`.
3. **c47** (biên ghép + xác thực khối; ca cần marker thì đòi marker): `number` bool ở `Set up job`, `number` float, alias
   `name:` của job, ma trận `j ()`, tên job có xuống dòng, `Post ` ở giữa tên bước, khoảng trắng cuối `run:` (đòi marker),
   hai dòng trùng (đòi một mục), `GITHUB_ENV` ở bước ĐẦU (log không có nhóm setup) và cách đích một bước, `##[endgroup]` có đuôi,
   `shell:` thiếu dấu cách, `run: 5` có `name:` mà khối in lại là `5` (không marker, không ném).
4. **Công cụ**: `##[endgroup]` so nguyên văn; `gio` cắt về giây ngay ở `tach_buoc` (`d[:19] + "Z"`, bỏ phép tách regex tương
   đương); bỏ trần 200 dòng của `dong_khop` (không ca nào đo được, spec M4 không đặt trần).
5. **Đột biến toán tử tự động** (`toan_tu.py`, 130 bản biên dịch được trên các hàm r4): sau vá, 0 SONG, 0 TIN_DUNG_GIA; 22 bản
   vừa bị giết đúng ca vừa làm công cụ ném ở ca khác (`GIET+NEM`) — báo nếu bạn cho rằng bản nào trong số đó là lỗ thật.
   c23/c39 nay bắt ngoại lệ (không ném là tính chất ca đo).
6. Suite tại chỗ: `CA: 47/47 dat` · `DOT BIEN: 155/155 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
7. A9/A10 chưa chạy lại trên HEAD (chủ kho hoãn gate nặng tới khi đủ điều kiện merge) — hãy REPLAY A10 offline như lượt trước.

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F11**: chạy lại MỌI script lượt 1–3 của bạn (`.review-input/r4-luot{1,2,3}/`); F10 phải được chứng minh ĐÓNG
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
