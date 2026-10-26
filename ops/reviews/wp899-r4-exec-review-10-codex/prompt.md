# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), **revision 4**, lượt 10, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context executor; không gọi subagent; không đăng
GitHub; không đẩy git; không sửa tệp nào trong cây kho (`git status` phải sạch khi xong). Mọi tệp bạn tạo nằm trong `.review/`.
Bạn không có mạng.

## Đối tượng — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| reviewed_sha (HEAD) | `4ee92cf49534baa54f9e842d4e80f9635c515a0e` |
| lượt trước (r4 lượt 9) | `d2cca1580ed23dbbc532fb21481d0fac1e6ad8ac` = cha của HEAD; verdict `.review-input/r4-luot9/VERDICT.md` (changes_requested: P2 = 1, F12 lỗi sản phẩm `doc_wf` ném khi SafeLoader dựng scalar hỏng; P3 D02, D03, D04). `.review/` lượt 9 ở `.review-input/r4-luot9/`; lượt 1–8 ở `.review-input/r4-luot{1,…,8}/` |
| base | `ba222ffd1615f0d74b59985b9612f725211b62f5` |
| đặc tả r4 | `.review-input/wp899-r4.md`, sha256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` — kiểm băm, đọc TRỌN; r3/r2 cùng thư mục cho các mục được dẫn |
| verdict r3 | `.review-input/r3-luot1/`, `.review-input/r3-luot2/` |
| A10 / log thật | `.review-input/a10/` (đo trên `52e9573`) · `.review-input/log-that/` + `SHA256SUMS` |
| kết quả tập đóng của executor | `.review-input/dot-bien-dong-luot-dau.txt` (lượt đầu, trên bộ ca TRƯỚC c52) · `.review-input/dot-bien-dong-ket-qua.txt` (lượt cuối: chỉ đo lại mã chưa giết, mã đã giết dùng lại theo băm nguồn đột biến) |
| write set (lease g4) | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` |

Delta cần review: `git diff d2cca15 HEAD` (cả hai tệp); toàn bộ: `git diff ba222ff HEAD`.

## Authority — coi là quyết định, KHÔNG phải finding

- Q1–Q12 của đặc tả r4.
- **Tiêu chí phân hạng** (#899 issuecomment-6396095156): đột biến SỐNG là P1 khi nó đổi kết quả trên đầu vào mà đặc tả ĐỊNH NGHĨA
  kết quả; chỉ sống ở miền đặc tả KHÔNG định nghĩa ⇒ P3 kèm đề xuất; làm công cụ NÉM ở đầu vào đòi "không ném" ⇒ P1/P2.
  **D01**: `env: null` ở job/workflow ⇒ CHẶN; khoá `env:` vắng ⇒ không chặn.
- **Trả lời checkpoint lượt 7** (#899 issuecomment-6400403263) và **lượt 9** (#899 issuecomment-6404816990), chủ kho chọn trong phiên executor:
  (1) **ngân sách Codex r4 nâng lên 11**: đây là lời gọi **10/11**, LƯỢT OFFLINE CUỐI; lời gọi 11/11 dành cho connector sau lần đẩy. Tệp lease g4
  vẫn ghi `limit: 8` vì executor không được sửa lease; quyết định nằm ở hai comment trên, không phải finding.
  (2) **trần dòng khoảng 2050**: numstat hiện tại 444 + 1595 = **2039**.
  (3) **D02**: `uses:` nhiều dòng giữ "dòng đầu" ⇒ P3 nợ, không mở lại.
  (4) **F10 đổi cách tiếp cận sang TẬP ĐỘT BIẾN ĐÓNG** sau năm lượt không hội tụ (28 · 17 · 27 · 26 · 32 mã sống mới).
- **Lease g4** (#899 issuecomment-6399500529 / -6399592086) thay g3 và bỏ `.claude/dev/ci_dang_ky_test.py` khỏi write set
  (nhả cho #763). Commit HEAD `4316812` trả tệp ấy về như base. Head vì vậy sẽ ĐỎ ở `gate-registry` cho tới khi dòng `MOI` được đăng
  ký lại bằng một lease khác. Đó là giới hạn khai, KHÔNG phải finding.
- `gioi_han_khai` của r4: đường cần quyền sửa nội dung tại SHA checkout là giới hạn khai.

## Tập đột biến đóng — đây là thước F10 của lượt này

`python -B ops/ci_provenance_test.py --dot-bien-dong [SONG_SONG]` (`ops/ci_provenance_test.py`, khối `HAM_DONG` … `chay_dot_bien_dong`).

- **Phạm vi**: MỌI nút AST trong chín hàm r4 `HAM_DONG` = `_env_chan` `doc_wf` `ghep_job` `ten_du_kien` `_gio` `ghep_buoc`
  `chan_buoc` `tach_buoc` `do_dau_duong`.
- **Bảng toán tử cố định** (`_toan_tu`): đổi so sánh; `and`↔`or`; bỏ từng vế; bỏ `not`; đảo `bool`; số ±1; mọi hằng chuỗi qua
  `bien_dang` + chuỗi rỗng; `IfExp` lấy một nhánh; `if` cố định đúng/sai; bỏ từng bộ lọc comprehension; bỏ từng đối số khi có ≥ 2;
  `return None`.
- **Hạng**: GIET = ≥ 1 ca chết bởi `TinHieuChotCa` của CHÍNH ca ấy (`DO:<ca>:`) · TIN_DUNG_GIA = chỉ chết vì lỗi vô can · SONG.
- **Đạt** ⇔ 0 SONG ngoài `TUONG_DUONG` · 0 TIN_DUNG_GIA · không mục `TUONG_DUONG` nào bị giết, và không mục nào trỏ mã đã rời tập.
- **Kết quả của executor trên HEAD** (đo lại TRỌN vì nguồn sản phẩm đổi nên mọi băm đột biến đổi): `DOT BIEN DONG: 1007/1015 giet ·
  8 tuong duong co chung minh · 0 song · 0 tin dung gia · 0 chung minh tuong duong sai` · `TONG DONG: DAT`. Lượt đầu (bộ ca trước c52) có 57 mã không bị giết (lượt 8 của bạn đính chính con số 58).
- **Vá P2 lượt 8**: `_toan_tu` thêm `bo_ngoai_le{k}` — bỏ TỪNG lớp trong tuple của `except` (sinh `doc_wf#7:bo_ngoai_le0/1`);
  c52 thêm hàng `doc_wf` trên YAML lồng 5000 mức phải trả None. `bo_ngoai_le1` (bỏ `RecursionError`) chết ở c52;
  `bo_ngoai_le0` (bỏ `yaml.YAMLError`) chết ở `c32_workflow_khong_doc_duoc` (đo: `DO:c32…:YAML hỏng: công cụ ném ParserError`).
- **Vá F12 lượt 9** (`ops/ci_provenance.py:160`): `doc_wf` bắt thêm ĐÚNG bốn lớp bạn đo được — `ValueError` `KeyError` `IndexError`
  `AttributeError` — không bắt `Exception`. c52 thêm 8 đầu vào của bạn (`name: <scalar>` + `jobs: {j: {}}`), đòi `doc_wf` trả None;
  đối chứng `name: "2026-02-30"` (có nháy) vẫn ra dict. Tập đóng tự sinh `doc_wf#7:bo_ngoai_le0…5` — mỗi lớp mới có ≥ 1 đầu vào giết.
  Đột biến tay `A18_yaml_hong_nem` neo lại theo dòng mới, vẫn chết ở c32.
- **D03/D04 lượt 9**: c52 thêm hai hàng `Build ${{x}}` (alias job, `name:` bước); c51 hàng "hai bước cùng script" đòi
  `buoc_xac_thuc == 2`. Ba đột biến ngoài tập bạn đo (`startswith` ×2, `so = 1`) khoá thành `L9_*` trong `DOT_BIEN`.
- Bộ ca thường của tệp trên HEAD: `CA: 52/52 dat` · `DOT BIEN: 291/291 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`.
- A10 LIVE (có mạng, phía executor) trên `d2cca15`: hai run 39342960764 / 40074551995 cho mốc Gate GIỐNG HỆT lần đo `52e9573`
  (13+1, 22+1). Mã sản phẩm đổi từ đó chỉ ở `doc_wf` (nhánh lỗi); replay offline của bạn trên HEAD vẫn là phép đo bắt buộc.

## Vai trò lượt này — BẮT BUỘC, theo thứ tự

1. `.review/VERDICT.md` pending ngay đầu, cập nhật dần.
2. Kiểm băm spec, HEAD, base, write set, numstat, `git diff --check`.
3. **Kiểm bản vá F12 và BỘ SINH, không nhận lời.** Trước hết chạy lại `product_yaml9.py` (8 đầu vào + đối chứng) và `gap8.py`/`gap_e2e8.py`
   trên HEAD; rồi tìm lớp ngoại lệ dựng scalar/constructor KHÁC của SafeLoader mà bản vá chưa bắt (đo, không suy), và kiểm bản vá
   không nuốt lỗi lập trình ngoài `safe_load`. Rồi rà bảng kiểu nút lượt 8 tìm **lỗ cùng hình dạng** — một kiểu nút mà toán tử bậc một tự
   nhiên SỐNG và đổi kết quả đặc tả định nghĩa — mà lượt 8 chưa thử. (a) Liệt kê mọi kiểu nút AST có trong chín hàm, rồi chỉ ra kiểu nào mang ngữ nghĩa mà
   `_toan_tu` KHÔNG đột biến (ví dụ Subscript chỉ số, Attribute, phép số học, `in` trên chuỗi, lát cắt không hằng, gọi một đối số,
   `for`/`zip`, walrus…). Mỗi lỗ là **P2** nếu một toán tử bậc một tự nhiên trên kiểu ấy SỐNG và đổi kết quả đặc tả định nghĩa — đo
   bằng mutant chạy được, không suy. (b) Kiểm mã đột biến ổn định và `sinh_dot_bien_dong` không âm thầm bỏ mutant (`compile` lỗi,
   trùng nguồn qua `dict`). (c) Kiểm phân hạng không cấp tín dụng giả (`DO:<ca>:` khớp đúng ca; `--tat-ca-ca` dừng ở rc 3 đầu tiên).
4. **Kiểm từng chứng minh trong `TUONG_DUONG`** (8 mục): dựng đầu vào phân biệt nếu có. Một chứng minh SAI là **P1**.
5. **Chạy lại tập đóng** trên HEAD bằng phép đo của bạn (`python -B`, `PYTHONDONTWRITEBYTECODE=1`). Nếu thời gian không đủ cho
   1009 mã, lấy một mẫu ≥ 150 mã phủ cả chín hàm, rồi đo lại TRỌN 58 mã của `dot-bien-dong-luot-dau.txt` không ở hạng GIET. Nói
   rõ đã đo bao nhiêu và báo `KHÔNG ĐO ĐƯỢC` cho phần còn lại.
6. **Săn LỖI SẢN PHẨM** trong `ops/ci_provenance.py` theo M1–M12/A1–A27 và `dinh_nghia` r4: đầu vào thật mà công cụ ra kết quả sai,
   ném, hoặc ra `passed` khi phải `not_measured`/`failed`. Đây là việc chính của lượt; một lỗi sản phẩm đo được là P0/P1/P2 theo hạng.
7. **Đột biến bạn tự nghĩ ra NGOÀI tập đóng** (không phải đột biến bậc một của bảng toán tử): ghi **P3** kèm đề xuất, TRỪ khi nó đi kèm
   một lỗi sản phẩm thật (mục 6), hoặc lộ ra một lỗ của bộ sinh (mục 3a). Đây là hệ quả của quyết định (4): thước F10 là tập đóng,
   và việc thêm đột biến tay mỗi lượt là thứ đã không hội tụ năm lần.
8. Đối chiếu F01–F11; chạy lại các script lượt 1–7 của bạn ở mức đủ để khẳng định không thoái lui (không bắt buộc lại toàn bộ frontier).
9. Replay A10 offline (`.review-input/a10/`); khác provenance trên `52e9573` thì giải thích từng khác biệt.
10. **Không tự soạn nội dung tấn công nhạy cảm**; hướng nào cần thì MÔ TẢ BẰNG LỜI. Review theo LỚP (V3).

## Hạng

- **P0**: bằng chứng sai theo hướng có lợi (thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3), hoặc rò credential.
- **P1**: vi phạm M1–M12/A1–A27 đo được; chứng minh tương đương sai; tập đóng báo DAT trong khi một mã của CHÍNH tập đóng sống.
- **P2**: lỗi thật nhưng hẹp; lỗ bộ sinh đo được (mục 3a); ca có mặt mà không đo.
- **P3**: nợ/chất lượng; đột biến ngoài tập đóng không kèm lỗi sản phẩm; kèm đề xuất quyết định có căn cứ.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; rồi `reviewed_sha:`, `base_sha:`, `Reviewed commit: <40 hex>`.
Approve CHỈ khi P0 = P1 = P2 = 0 (V2), mỗi P3 có quyết định đề xuất. Bắt buộc: bảng ĐỐI CHIẾU F01–F11; **BẢNG LỚP**
`| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |`; kết quả mục 3 (bảng kiểu nút: có toán
tử / không / mutant đo được); bảng 8 chứng minh tương đương (giữ / bác + đầu vào); số mã tập đóng bạn đã đo và hạng; lỗi sản phẩm
tìm được (hoặc "không tìm được" kèm các hướng đã thử); đối chiếu A1–A27; kết quả replay A10. Không khẳng định thứ chưa đo; không đo
được thì ghi `KHÔNG ĐO ĐƯỢC`.
