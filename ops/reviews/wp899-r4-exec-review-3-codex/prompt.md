# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 4**, lượt 3, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `27997a73c6b01e577ed655ea94e73d56adf697da` |
| lượt trước (r4 lượt 2) | `52e9573d0bd401a629a031a9c32df7bfd17c27c1` = cha của HEAD; verdict `.review-input/r4-luot2/VERDICT.md` (changes_requested: F10 P1 LẶP LỚP). Toàn bộ `.review/` lượt 2 ở `.review-input/r4-luot2/`; lượt 1 ở `.review-input/r4-luot1/` |
| điểm xuất phát / base | `fe7522e` (ba tệp từ ứng viên r3 `7f5a02c`) / `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả r4 | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN; r3/r2 cùng thư mục cho các mục được dẫn |
| verdict r3 | `.review-input/r3-luot1/`, `.review-input/r3-luot2/` |
| A10 / log thật | `.review-input/a10/` (đo trên `52e9573`) · `.review-input/log-that/` + `SHA256SUMS` |
| tự đột biến của executor | `.review-input/tu-dot-bien/` (script + kết quả hai vòng; script trỏ đường dẫn tuyệt đối của executor và neo ở `52e9573`/giữa chừng — đọc làm tham chiếu, không tin kết quả) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff 52e9573 HEAD`; toàn bộ: `git diff ba222ff HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q12 của đặc tả r4.
- **Quyết định chủ kho sau checkpoint V5 của lượt 2** (phiên executor, 25-10-2026, trả lời checkpoint #899
  issuecomment-6393643859): *(1) đẩy nhánh lưu trữ — đã đẩy `ops/wp899-g3-luu-tru` @ `e47df3b`; (2) **nâng trần**; tiếp tục vòng
  vá tới hết P1, P2; không đẩy nhánh code, không chạy gate nặng cho tới khi đủ điều kiện merge.* Vì vậy V5 KHÔNG còn dừng packet ở
  lượt này; trần dòng do chủ kho nâng mà chưa nêu số — numstat hiện tại 1 + 444 + 867 = **1312**. Không coi việc vượt 1250 là
  finding; báo con số nếu bạn thấy cần.
- Ngân sách Codex: đây là lời gọi **3/8** của r4 (chủ kho chưa đổi trần lời gọi).
- `gioi_han_khai` của r4: đường cần quyền sửa nội dung tại SHA checkout là giới hạn khai.

## Executor đã làm gì sau lượt 2 (đánh giá, đừng nhận lời)

F10 lặp vì executor vá đúng chỗ được chỉ rồi bỏ sót đường kế tiếp. Lượt này executor **tự đột biến có hệ thống** mọi chốt mới của
r4 trước khi gửi (64 đột biến, hai vòng, `.review-input/tu-dot-bien/`), rồi với mỗi đột biến sống: thêm một biến thể ca + một mục
`DOT_BIEN`, hoặc đơn giản hoá mã khi chốt thừa/tương đương.

1. **Công cụ** (`git diff 52e9573 HEAD -- ops/ci_provenance.py`): bỏ `re.S` ở `ghep_job` (hẹp hơn, fail-closed); `_gio` bỏ tham số
   `mau`, header được cắt về giây ở chỗ gọi (`b["gio"][:19] + "Z"`); vế (b) đòi tên REST là chuỗi khác rỗng (trước đó REST `name:
   null` khớp `ten_du_kien` = None); `chan_buoc` đọc `GITHUB_ENV/PATH` qua `str(t.get("run", ""))` thay cho guard kiểu.
2. **Test**: hai biểu hiện F10 lượt 2 (`number` 0/âm; `steps:` YAML thiếu/null/số/không phải list) + mọi đột biến sống của tự đột
   biến: hậu tố tên job (`jx`, `j x`), `name: ""` của job, đối chứng khoá khớp khi job có `name:`, `name:` job khác không phải chuỗi,
   `name:` bước rỗng / không phải chuỗi, `run:` không phải chuỗi (cả khi có `name:`), dòng đầu có khoảng trắng cuối, bước tên
   `Postgres`, bước `failure` vẫn tính là đã chạy, log THIẾU nhóm, REST THỪA bước `skipped`, bước `skipped` đứng TRƯỚC (c45: tên vẫn
   kiểm; giờ và vị trí theo bước đã chạy), đuôi thừa sau `Z`, đường dẫn MOI chứa `GITHUB_PATH` ở chính bước ấy, c38/c44 bắt ngoại lệ
   (vế c và chốt dạng phải hỏng êm), c32 đòi `ghep_buoc` = `not_measured`. c12–c14 bỏ chỉ số `[0]` (từng ném `IndexError` = tín dụng giả
   dưới đột biến).
3. **Đột biến executor khai TƯƠNG ĐƯƠNG, không thêm ca**: luật nhóm lồng chỉ áp sau `shell:` (trước `shell:` đã bị luật cấu trúc cũ
   chặn); `[:i+1]` thay `[:i]` ở `GITHUB_ENV` chỉ khác khi chính bước tối giản nhắc chữ ấy (đã có ca đường dẫn `GITHUB_PATH_test.py`).
   Kiểm hai lời khai này.
4. Suite tại chỗ: `CA: 45/45 dat` · `DOT BIEN: 125/125 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
   Script lượt 2 của bạn chạy lại trên HEAD: `shape_audit.py` ⇒ `rest_number_cho_zero` GIET c44; `--containers` ⇒
   `yaml_steps_bo_list_guard` GIET c44, `rest_steps_bo_list_guard` GIET c22.
5. A9/A10 chưa chạy lại trên HEAD này (chủ kho: không chạy gate nặng cho tới khi đủ điều kiện merge). A10 trên `52e9573` trùng byte
   lượt 1; logic giờ/tên của HEAD đổi ⇒ hãy REPLAY A10 offline từ `.review-input/log-that/` + `a10/out-*/{run.json,jobs.json}` +
   `git show <sha>:.github/workflows/ci.yml` và so với `a10/out-*/provenance.yaml`.

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F11**: chạy lại MỌI script lượt 1 và lượt 2 của bạn (`.review-input/r4-luot{1,2}/`); F10 phải được chứng minh ĐÓNG
   CẢ LỚP — tự đột biến thêm mọi chốt dạng/miền giá trị/vị trí của `ghep_job`/`ten_du_kien`/`_gio`/`ghep_buoc`/`chan_buoc`/
   `do_dau_duong`/`tach_buoc` mà executor chưa thử; báo mọi đột biến SỐNG.
4. Đột biến trên BẢN SAO TẠM (`python -B`, `PYTHONDONTWRITEBYTECODE=1`, `CI_PROVENANCE_MA=<bản sao>`); chỉ tính giết khi ca đích
   chết bởi `TinHieuChotCa` của ĐÚNG ca; đột biến làm công cụ NÉM ở một ca không bắt ngoại lệ là TIN_DUNG_GIA — báo riêng.
5. Replay A10 offline (mục 5 trên); khác provenance trên `52e9573` thì giải thích từng khác biệt.
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
