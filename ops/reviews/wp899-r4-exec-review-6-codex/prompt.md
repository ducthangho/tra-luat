# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 4**, lượt 6, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `35453ff30170998ffea663801299db5876cc8e0c` |
| lượt trước (r4 lượt 5) | `22da28c738e651361274c1264e681a52461dad1e` = cha của HEAD; verdict `.review-input/r4-luot5/VERDICT.md` (changes_requested: F10 P1, 27 đột biến sống; D01 P3). `.review/` lượt 5 ở `.review-input/r4-luot5/`; lượt 1–4 ở `.review-input/r4-luot{1,2,3,4}/` |
| điểm xuất phát / base | `fe7522e` (ba tệp từ ứng viên r3 `7f5a02c`) / `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả r4 | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN; r3/r2 cùng thư mục cho các mục được dẫn |
| verdict r3 | `.review-input/r3-luot1/`, `.review-input/r3-luot2/` |
| A10 / log thật | `.review-input/a10/` (đo trên `52e9573`) · `.review-input/log-that/` + `SHA256SUMS` |
| tự đột biến của executor | `.review-input/tu-dot-bien/` (`tu_dot_bien*.py` hai vòng tay + `toan_tu.py` đột biến TOÁN TỬ tự động trên mọi hàm r4, kết quả `kq*.txt`; script trỏ đường dẫn tuyệt đối của executor — đọc làm tham chiếu, chạy lại bằng phép đo của bạn) |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` |

Delta cần review: `git diff 22da28c HEAD`; toàn bộ: `git diff ba222ff HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q12 của đặc tả r4.
- **Quyết định chủ kho sau checkpoint V5 của lượt 2** (phiên executor, 25-10-2026, trả lời checkpoint #899
  issuecomment-6393643859): *(1) đẩy nhánh lưu trữ — đã đẩy `ops/wp899-g3-luu-tru` @ `e47df3b`; (2) **nâng trần**; tiếp tục vòng
  vá tới hết P1, P2; không đẩy nhánh code, không chạy gate nặng cho tới khi đủ điều kiện merge.* Vì vậy V5 KHÔNG còn dừng packet ở
  lượt này; trần dòng do chủ kho nâng mà chưa nêu số — numstat hiện tại 1 + 444 + 1204 = **1649**. Không coi việc vượt 1250 là
  finding; báo con số nếu bạn thấy cần.
- Ngân sách Codex: đây là lời gọi **6/8** của r4; sau lượt này còn 2, một dành cho connector sau lần đẩy (chủ kho chưa đổi trần lời gọi).
- `gioi_han_khai` của r4: đường cần quyền sửa nội dung tại SHA checkout là giới hạn khai.

- **Hai quyết định chủ kho sau checkpoint lượt 5** (#899 issuecomment-6394979394, trả lời trong phiên executor 25-10-2026):
  (1) **tiêu chí phân hạng đã chốt**: đột biến SỐNG là P1 khi nó đổi kết quả trên đầu vào mà đặc tả ĐỊNH NGHĨA kết quả (M4/M12,
  `dinh_nghia`, A1–A27, D01 dưới đây); đột biến chỉ sống ở miền đặc tả KHÔNG định nghĩa ⇒ P3 kèm đề xuất quyết định và lý do
  vì sao đặc tả không định nghĩa; đột biến làm công cụ NÉM ở đầu vào đòi "không ném" ⇒ P1/P2. (2) **D01: `env: null` ở job hoặc
  workflow ⇒ CHẶN** (null không phải dict); khoá `env:` VẮNG ⇒ không chặn.

## Executor đã làm gì sau lượt 5 (đánh giá, đừng nhận lời)

1. **D01** (`ops/ci_provenance.py`): `_env_chan(d)` nhận dict CHA, `"env" in d and (type(d["env"]) is not dict or any(...))`;
   gọi `_env_chan(wf)`, `_env_chan(j)`. c46 thêm `env: null` hai mức (chặn). Đây là thay đổi mã sản phẩm DUY NHẤT của lượt.
2. **c49 — oracle + bộ sinh nhiều trục** (đóng LỚP thay vì vá theo danh sách): 250 kịch bản, `random.Random(899)`; oracle
   `oracle_chan` / `oracle_job` / `RE_GOI_ORACLE` viết thẳng từ định nghĩa spec bằng phép so chuỗi, KHÔNG gọi hàm công cụ. Trục:
   1–3 job, job đích ở vị trí bất kỳ, alias `name:` (đôi khi TRÙNG khoá job khác ⇒ vế d), hậu tố ma trận dài 90 ký tự; tới 10 bước
   (`number` qua 9→10); bước `skipped`; `env` ba mức trên miền `ENV_MIEN` (vắng/null/{}/dict/khoá chặn đầu-giữa-cuối, giá trị
   rỗng/list/biểu thức/0/False/""); `defaults`; `shell` trên `SHELL_MIEN`; khoá lạ; `VAR=`; đối số; bước ghi `GITHUB_ENV`/
   `GITHUB_PATH` (cuối chuỗi, giữa chuỗi, không ranh giới từ, `run:` list có `name:`) ở mọi vị trí và ở job khác; mỗi nhóm một giây
   riêng; nhiễu loạn REST: cửa sổ giờ SAU hoặc TRƯỚC header ở một bước bất kỳ, tên lệch ở một vị trí bất kỳ (kể cả skipped),
   `number` float nguyên. So TRỌN danh sách marker và `ghep_buoc`. Phân bố đo được: 189 ghép passed / 61 ghép hỏng có chủ đích;
   487 mục marker (74 passed · 75 failed · 338 chặn chế độ); kịch bản mà tên REST trỏ DUY NHẤT job KHÁC bị bỏ (0 trên hạt giống này).
3. c48 thêm: dấu cách SAU dấu nối dòng cuối (lời khai tương đương `n_goi_strip_run` của executor lượt 4 là SAI — bạn đúng), màu
   không có `\x1b[0m`, `run:` hai LF cuối (khối một dòng ⇒ marker; khối có dòng màu rỗng ⇒ không), `uses:` có khoảng trắng.
4. `frontier5.py` của bạn chạy lại (đặt lại neo cho 8 đột biến `env` theo chữ ký mới): 22/22 GIET (gồm `n_goi_strip_run`);
   `nested_only_after_shell` giữ là TƯƠNG ĐƯƠNG theo chính `nested_after_equivalent.py` của bạn ở lượt 4. 22 đột biến ấy ghi vào
   DOT_BIEN. Đột biến toán tử tự động (`toan_tu.py`, `kq8.txt`) chạy lại sau D01: 130 bản, 0 sống, 0 tín dụng giả.
5. Suite tại chỗ: `CA: 49/49 dat` · `DOT BIEN: 231/231 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
6. A9/A10 chưa chạy lại (chủ kho: chỉ chạy chỗ thay đổi; A10 một lần trên SHA cuối). D01 có thể đổi provenance của run nào có
   `env: null` — `ci.yml` tại `b27fe85`/`dc65714` không có (hãy kiểm khi REPLAY A10 offline).

## Cách làm — BẮT BUỘC

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Đối chiếu F01–F11**: chạy lại MỌI script lượt 1–5 của bạn (`.review-input/r4-luot{1,2,3,4,5}/`); F10 phải được chứng minh ĐÓNG
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
