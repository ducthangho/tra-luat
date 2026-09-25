# ĐẶC TẢ PACKET — WP570-BASH-NEN-MOT-BO-GIAI, revision 23

- **Issue:** https://github.com/ducthangho/tra-luat/issues/570
- **Trạng thái:** ĐÓNG BĂNG khi lease `wp570-bash-nen-r23-g23-opus` được cấp. Mọi thay đổi
  objective / acceptance / write set / executor / environment ⇒ revision mới, generation mới,
  cấp lại lease (§3.2 `docs/PROTOCOL_DA_PHIEN.md`).

## 0. Vì sao có revision 23 — reviewer CÙNG NHÀ CUNG CẤP, bảy finding, không lớp nào chạm lần ba

Codex hết hạn mức. Chủ kho chỉ thị trong phiên (2026-09-25): *"thay cross review bằng same provider
reviewer với effort hoặc mô hình ở mức cao hơn"*. Vòng 17 chạy bằng CLI `claude` không giao diện, phiên
MỚI, checkout RIÊNG tại `505ff6d`, họ `fable` effort `max` — cao hơn executor (họ `opus`, effort `high`)
ở CẢ HAI trục. Model đã phục vụ lượt ấy được ĐO, không nhận lời khai: `kiem_ket_qua` của
`.claude/dev/chon_reviewer.py` đọc `modelUsage` của kết quả JSON ⇒ ĐẠT, một họ model duy nhất.

Vòng 17 ra **P1 0 · P2 4 · P3 3**. Phiên **tái hiện độc lập cả bảy** — 19 mẫu LỌT chạy bash THẬT trên
Python 3.12 trong khi `_loi_goi_tran` trả `[]`, một mẫu `RecursionError`, và bộ chốt mù trên bản sao
tệp ca — trước khi chạm dòng nào.

### (1) Điều kiện dừng: ĐẾM LẠI, không lớp nào chạm lần thứ ba

| lớp | finding | lần của HÌNH DẠNG này |
|---|---|---|
| D — bộ chốt | F4 `.get(<trường>)`, bí danh trường | **1** — DẠNG ĐỌC TRƯỜNG. Năm lần trước (r18..vòng 16) là dạng RÀNG BUỘC tên (phạm vi/vị trí/nhánh), và N80 đã giết đúng lớp ấy: vòng 17 không có finding ràng buộc nào |
| E — nạp động (N81) | F1 bí danh / mọi đích / `eval` · F2 tải gấp hằng, mở đầu từ bảng · F6 tải hỏng bị nuốt | **1** — lượt soát đầu tiên của N81 |
| A — argv | F3 argv NỐI/TRẢI | **1** |
| A' — bộ gấp | F7 `%` với `dict` | lớp A đã được chủ kho quyết VÁ TIẾP (r17); tập toán tử vẫn KHÔNG đóng |
| tài nguyên | F5 đệ quy Python ~1000 tầng | **1** |

Lớp D được ghi rõ vì đây là lần đầu nó quay lại SAU một lần đổi kiến trúc: nếu vòng sau còn ra một
DẠNG ĐỌC TRƯỜNG khác, đó là lần hai của hình dạng này — và lần ba thì phiên DỪNG.

### (2) Bảy finding, năm luật

| finding | xử lý |
|---|---|
| F1 bí danh `import_module`/`__import__`, `a = b = …`, `m: T = …`, `importlib.__import__`, `builtins.exec`, `eval("__import__(…)")` | **N83** — ràng buộc nạp động CHỜ GIẢI, giải SAU khi mọi bảng đã dựng, bằng cả cú pháp lẫn bộ giải tên |
| F2 tải `b"…"`/`+`/f-string, `import` trong hàm chứa `exec`, nạp động, `exec` trước | **N83** — tải gấp qua `_gia_tri_hang`; mở đầu của tải sinh từ BẢNG RÀNG BUỘC của cả tệp |
| F6 tải hằng hỏng bị NUỐT (fail-open) | **N83** — NÉM (fail-close); kèm `exec` lồng quá 3 tầng cũng NÉM (phiên tự tìm) |
| F5 `RecursionError` ở ~1000 tầng | **N84** — bộ duyệt dùng ngăn xếp tường minh; quét được tới giới hạn biên dịch của Python (~10.000) |
| F3 argv `["bash", …] + x`, `[*("bash", …), x]`, `("bash",) + …` | **N85** — đi theo cú pháp tới phần tử ĐẦU |
| F7 `"%(k)s" % {…}` | **N86** |
| F4 `.get(<trường tổng hợp>)`, bí danh trường | **N87** — nguồn `tt` cho tên mang giá trị một trường tổng hợp |

## 0. Vì sao có revision 22 — ĐIỀU KIỆN DỪNG chạm ở lớp D, chủ kho chọn ĐỔI KIẾN TRÚC lần hai

Cross-review codex vòng 16 trên `2537c73` ra **11 × P2, không P1**, cả mười một **tái hiện**. Năm
trong mười một thuộc lớp D — bộ chốt XUẤT XỨ phán quyết (N22) — lần lặp thứ **NĂM** liên tiếp của lớp
ấy (r18 N64 → r19 N69 → r20 N75 → r21 N79 → vòng 16): iterable đầu của comprehension, biểu thức lúc
định nghĩa, tham số lambda/async, và năm dạng ràng buộc chưa ghi.

### (1) Phiên DỪNG và HỎI lần thứ hai

Phép đo đưa kèm câu hỏi — bộ chốt lấy HỢP mọi ràng buộc cùng tên, bỏ phạm vi/vị trí/nhánh, GIỮ luật
nhãn trường: trên CÂY THẬT bắt đúng **6 ca như cũ, THÊM 0 · MẤT 0**; **9 mẫu che tên** trong
`_MAU_TOAN_TU` chuyển thành bị bắt. **Chủ kho chọn "Đổi kiến trúc D"** (trong phiên, 2026-09-25), và
cho nạp module động chọn **"Bắt dạng hằng + fail-close"**.

### Mười một finding

| finding | lớp | xử lý |
|---|---|---|
| H7 iterable đầu · H8 đích comprehension · H10 biểu thức lúc định nghĩa · H11a walrus | D | **N80** — bắt |
| H9 tham số lambda/async · H11 `with`/`except`/`case`/`+=` che tên | D | **N80** — bắt thừa có chủ đích |
| H1 `nonlocal` ba tầng · H2 `global str` chỉ đọc | B-phạm vi | **N82** |
| H3 `__import__`/`importlib` · H4 `exec("import …")` | E — nạp động | **N81** (dạng hằng) |
| H5 độ rộng quá nhiều chữ số · H6 `join` khuếch đại | A | **N78b/N78c** |

## 0. Vì sao có revision 21 — ĐIỀU KIỆN DỪNG chạm ở lớp B, chủ kho chọn ĐỔI KIẾN TRÚC

Cross-review codex vòng 15 trên `d766249` ra **8 × P2, không P1**, cả tám **tái hiện** (bộ quét
trên Python 3.12.3 thật, chạy bash thật; bộ chốt bằng `_chot_DO_cua_cong_trong`). Năm trong tám
thuộc lớp B — bộ giải tên theo THỨ TỰ THỰC THI — và đó là lần lặp thứ **SÁU liên tiếp** của lớp
ấy (r16 N46 → r17 N53 → r18 N60 → r19 N67 → r20 N72 → vòng 15): thứ tự gán ĐÍCH, `match` gán trước
`guard`, `except*` chạy nhiều nhánh, walrus trong comprehension, phạm vi chú thích PEP 695 thấy lớp.

### (1) Phiên DỪNG và HỎI, theo điều kiện dừng của lease

Điều kiện dừng: *"một hình dạng lỗi lặp lần thứ BA ⇒ DỪNG, hỏi có nên làm việc này không"*. Phiên
dừng, đo một phương án kiến trúc, rồi hỏi chủ kho với ba lựa chọn (đổi kiến trúc · vá tiếp · khép
vòng và khai nợ). Phép đo đưa kèm câu hỏi — bỏ thứ tự và nhánh, "có ràng buộc `import` ⇒ báo":
- cây thật 264 tệp: **THÊM 0 · MẤT 0**;
- `t33` PHỦ (95): lọt 1 (`lop_gan_SAU`) — bản cài đặt thật GIỮ được nó nhờ gộp thân lớp với
  phạm vi bao, nên lọt **0**;
- `t33` KHÔNG PHỦ (63): **22** mẹo che tên chuyển thành BỊ BÁO — báo động giả CÓ CHỦ ĐÍCH.

**Chủ kho chọn: "Đổi kiến trúc (khuyến nghị)"** (trong phiên, 2026-09-24).

### (2) Luật mới chỉ có một câu — N76

Trong phạm vi mà tên PHÂN GIẢI tới (luật phạm vi từ vựng, giữ nguyên), có BẤT KỲ ràng buộc nào
là `import` theo dõi ⇒ tên CÓ THỂ là module ấy ⇒ báo. Thân lớp GỘP với phạm vi bao (nó đọc được
biến toàn cục trước khi tự gán). Hàm có ràng buộc riêng thì tên là cục bộ. Mô phỏng vị trí hoàn
tất (N46/N53/N60), `UnboundLocalError` theo thứ tự (N67), đường nhánh (N72) — **GỠ**. Một mẹo che
tên không còn tắt được cổng; muốn tắt thì đổi tên hoặc khai miễn trừ, cả hai để lại dấu trong mã.

### Tám finding, bốn lớp

| lớp | finding | xử lý |
|---|---|---|
| B — thứ tự thực thi | G1 thứ tự đích gán · G2 `match` guard · G7a PEP 695 lớp che | **N76**: nay BỊ BÁO có chủ đích |
| B — phạm vi | G3 `except*` · G6 walrus comprehension · G7b PEP 695 thấy lớp | **N76** (+ đích walrus không là cục bộ comprehension, phạm vi chú thích thấy lớp bao) |
| B' — chú thích | G4 đích không đơn dưới `__future__` | **N77** |
| A — bộ gấp hằng | G5 ngân sách không cộng dồn | **N78** |
| D — bộ chốt | G8 comprehension · (G3 phía bộ chốt) `except*` | **N79** |

## 0. Vì sao có revision 20 — SÁU finding vòng 14, và BA lỗ cùng lớp mà codex không chỉ

Cross-review codex vòng 14 — vòng ĐẦU dưới reviewer `high` — trên `38198f5` ra **6 × P2, không
P1**, cả sáu **tái hiện trước khi vá** (bộ quét trên Python 3.12.3 thật, chạy bash thật; bộ chốt
bằng `_chot_DO_cua_cong_trong` trên mẫu tối giản).

### (1) Năm trong sáu finding nằm ĐÚNG trong bản vá r19

F3 (nhánh loại trừ) và F4 (chú thích hoãn được tính lại) sinh từ N67/N68; F5 (tràn số khi gấp
`%`) từ N65; F1, F2, F7 (bộ chốt) từ N69. Đó là dấu hiệu của **luật đúng mà HẸP**: mỗi luật r19
đúng ở chỗ nó phủ và mở một cửa ngay cạnh. Nên r20 không vá theo danh sách finding mà hỏi câu
chung của từng lớp — và câu chung ấy tìm ra thêm BA lỗ LỌT mà codex không chỉ, đều đo được là
chạy bash thật:
- **M1** — lời gọi trong THÂN HÀM mà `import` của module viết ở DƯỚI hàm. N46 (r16) lọc phạm
  vi module theo vị trí BẤT KỂ lời gọi nằm đâu, nên cả dạng rất thường này LỌT từ r16.
- **L1/L2** — cạnh QUAY LUI của vòng lặp: `import` đứng sau lời gọi trong cùng thân vòng.
- **X2** — cùng lỗ ấy trong bộ chốt (món nợ r18 đã khai, nay có phép đo và đóng).

### (2) Một phần của N68 bị ĐỔI LẠI — N73

r19 (N68) coi chú thích hoãn bởi `from __future__ import annotations` là "không chạy". Sai câu
hỏi: chúng được LƯU trong `__annotations__`, và `typing.get_type_hints` TÍNH LẠI được — đo được
in ra `OK`. Câu hỏi đúng là "có được LƯU không": được lưu thì quét (như thân hàm, cũng chỉ chạy
khi có người gọi); chú thích biến CỤC BỘ trong hàm không được lưu ở đâu cả ⇒ vẫn không quét. Hệ
quả nói thẳng: hình dạng mà vòng 13 gọi là báo oan nay lại được BÁO, và đó là chủ đích.

### Sáu finding, bốn lớp

| lớp | finding (+ tự tìm) | luật |
|---|---|---|
| A — bộ gấp hằng | F5 `"%c" % <số lớn>` làm `quet` sập | **N74** |
| B — ràng buộc tới được lời gọi | F3 nhánh loại trừ (+ M1, L1, L2, lớp-chưa-gán) | **N72** |
| B' — chú thích | F4 chú thích hoãn được tính lại | **N73** |
| D — bộ chốt | F1 `assertWarns` · F2 `finally` · F7 thân lớp (+ X2) | **N75** |

B và D là CÙNG MỘT câu hỏi ("ràng buộc nào tới được một điểm") ở hai công cụ, nên r20 dùng CÙNG
một mô hình cho cả hai: đường NHÁNH điều khiển từ gốc phạm vi; loại trừ, quay lui, thống trị suy
ra từ hai đường. Doctrine "mơ hồ ⇒ không báo" GIỮ NGUYÊN. **Đối chiếu toàn cây r19 ↔ r20: THÊM 0
· MẤT 0** trên 264 tệp.

## 0. Vì sao có revision 19 — TÁM finding vòng 13, NÂNG REVIEWER, và MỘT doctrine đổi ngược

Cross-review codex vòng 13 trên `a33f3fd` ra **8 × P2, không P1**, cả tám **tái hiện trước khi
vá**. Vòng 13 còn chạy dưới cấu hình reviewer CŨ.

### (1) Chủ kho nâng reviewer lên `high`, executor effort `medium`–`high`

g18 khai lần đầu reviewer THẤP hơn executor về effort. Chủ kho đã nâng reviewer lên **`high`**
ở cài đặt tổ chức codex, và cho executor effort từ `medium` tới `high` tuỳ phiên chọn — phiên
chọn **`high`** cho lượt này. Đảo chiều đã hết; vòng 14 là vòng đầu dưới reviewer mới.

### (2) Một doctrine từ r8 bị ĐỔI NGƯỢC — N67

Từ r8, bộ giải coi phạm vi HÀM theo "luật tên cục bộ lúc biên dịch": `import` rồi gọi rồi gán
lại trong cùng một hàm là MƠ HỒ, không bắt. **Sai.** "Là cục bộ" chỉ quyết một điều: đọc TRƯỚC
lần ghi đầu thì `UnboundLocalError`. Nó KHÔNG quyết giá trị nào đang có lúc gọi. Đo trên Python
3.12.3 thật: `def f(): import subprocess; subprocess.run(["bash", …]); subprocess = object()`
**in ra `OK`**. Hình dạng `ham_gan_SAU_van_mo_ho` của `t33` — một chốt từ r16 — đã mã hoá đúng
doctrine sai ấy và được chuyển sang `_HINH_DANG_PHU`.

### (3) Hai phép đo làm luật rộng hơn đề xuất

- `pty.spawn("bash")` với CHUỖI TRẦN cũng chạy (`rc 0`) — vòng 13 dặn cẩn thận đừng bắt nó.
- chú thích biến CỤC BỘ trong hàm KHÔNG BAO GIỜ chạy, kể cả không có `__future__` (PEP 526);
  vòng 13 chỉ nêu ca `__future__`.

### Tám finding, sáu lớp

| lớp | finding | luật |
|---|---|---|
| A — nhận diện tên | F1 f-string, `%`, `join`, cắt lát · F2 `pty.spawn` | **N65**, **N66** |
| B — phạm vi | F4 thứ tự thực thi TRONG HÀM · F5 chú thích hoãn | **N67**, **N68** |
| D — ratchet | F3 `with` nuốt ngoại lệ · F7 xuất xứ theo phạm vi từ vựng | **N69** |
| F — cache | F8 `CONG_CU_BASH` tên trần: vân tay canh NHẦM tệp | **N70** |
| H — miễn trừ | F6 mục đông cứng thiếu OID tắt im lặng phép ghim | **N71** |

Lớp A là lần thứ BẢY; bộ tính hằng tiếp tục là tập toán tử KHÔNG đóng. **Đối chiếu toàn cây
r18 ↔ r19: THÊM 0 · MẤT 0** trên 264 tệp.

## 0. Vì sao có revision 18 — TÁM finding vòng 12, ĐỔI EXECUTOR, và MỘT câu r17 viết sai

Cross-review codex vòng 12 trên `bcd78e9` ra **8 × P2, không P1**. Cả tám **tái hiện trước khi
chạm một dòng vá nào**. Ba điều phải ghi trước con số.

### (1) Một câu r17 viết SAI, và chính chốt r17 đã khoá nó

r17 viết *"một `PATH=""` tường minh nghĩa là đừng tìm ở đâu cả"*, gán cho HỆ ĐIỀU HÀNH, rồi
**khoá** câu ấy bằng chốt (5) của `t51` — mà **không đo**. Vòng 12 đo, phiên đo lại:
`os.get_exec_path({"PATH": ""})` ⇒ `['']`; `subprocess.run(["bash"], env={"PATH": ""})` ở thư
mục có `bash` ⇒ `rc=0`. Thành phần RỖNG là **thư mục hiện tại**. Đây là
**N6-LOI-KHAI-RONG-HON-PHEP-DO** — và lần này do chính phiên viết ra. Một chốt khoá cứng một
ngữ nghĩa SAI thì tệ hơn không có chốt: nó làm bản vá ĐÚNG thành ĐỎ. ⇒ **N62**, và chốt (5)
được viết lại để đo bằng một thư mục hiện tại THẬT SỰ có `bash`.

### (2) Đổi executor theo chỉ thị chủ kho

Chủ kho, trong phiên 2026-09-24: executor **nâng dần**, effort **từ `medium`**. Lượt này là lượt
đầu dưới chỉ thị ấy. Theo §3.2, đổi executor ⇒ revision + generation mới — g18 ghi điều ấy.
**Một hệ quả phải nói thẳng**: nguyên tắc chủ kho đặt là *"review bằng phiên bản HOẶC effort
CAO HƠN"*. Executor nay effort `medium`; reviewer vẫn được khai `low`. Đây là **lần đầu** reviewer
THẤP hơn executor về effort. Phiên KHÔNG đổi được cấu hình reviewer (nó nằm ở cài đặt tổ chức
codex, không phải ở kho), nên khai ra để chủ kho quyết, thay vì chép lại câu "CAO HƠN" cũ.

### (3) Món nợ có tên từ r8 đến hạn một lượt

Docstring của `_loi_goi_tran` khai `os.system` / `os.execvp` / `asyncio.create_subprocess_exec`
là NỢ CÓ TÊN từ r8, và verdict r16/r17 xin reviewer đo cái nào chạy thật. Vòng 12 đo **ba**;
phiên đo thêm **sáu** — cả **CHÍN** đều **CHẠY BASH THẬT**. Và phép đo lật một giả định: KIỂU
được nhận KHÔNG theo "loại API" — `os.system(Path("bash"))` CHẠY, còn `os.popen` từ chối cả
path-like lẫn `bytes`, `create_subprocess_shell` từ chối path-like. Nên bảng API mang kiểu
được nhận **đo riêng từng mục**. ⇒ **N59**.

### Tám finding, sáu lớp

| lớp | finding | luật |
|---|---|---|
| A — nhận diện tên | F1 `dict` làm argv; F2 vỏ bọc giữ hằng; F3 API khác | **N58**, **N59** |
| B — phạm vi | F5 tên LỚP ràng buộc sau CẢ thân (thân lớp chạy lúc định nghĩa) | **N60** |
| D — ratchet | F4 xuất xứ còn sống qua nhánh CÓ THỂ không chạy | **N64** |
| F — cache | F6 `BASH_ENV` ngoài khoá — mọi biến `bash` đọc đều là đầu vào | **N61** |
| G — PATH | F7 thành phần RỖNG là thư mục hiện tại (r17 viết SAI) | **N62** |
| H — mới | F8 hạn ngạch gõ nhầm làm `quet()` NÉM thay vì fail-close | **N63** |

**Lớp A là lần thứ SÁU.** Chủ kho đã quyết cơ chế ở lần thứ năm (bộ tính hằng). F1/F2 nằm trong
đúng phạm vi cơ chế ấy và được hấp thụ rẻ; F3 là nợ có tên đến hạn. Nhưng nói thẳng: bộ tính
hằng biến "liệt kê HÌNH DẠNG" thành "liệt kê TOÁN TỬ" — một tập nhỏ hơn nhiều nhưng **KHÔNG
đóng**. Thứ đóng được cửa là phân tích luồng dữ liệu, và nó vẫn là nợ có tên.

**Đối chiếu toàn cây r17 ↔ r18: THÊM 0 · MẤT 0** trên 264 tệp — chín API mới không lộ ra lời
gọi trần nào trên kho.

## 0. Vì sao có revision 17 — LỚP A LẶP LẦN THỨ NĂM, nên đổi KIẾN TRÚC chứ không nới bảng

Cross-review codex vòng 11 trên `fe6034a` ra **8 × P2, không P1**. Cả tám **tái hiện trước khi
chạm một dòng vá nào**. Nhưng điều đáng ghi không phải con số — mà là **HAI trong tám là báo
động giả do CHÍNH bản vá r16 đẻ ra**, và **bốn** là chỗ r16 vá hụt trong đúng hàm nó vừa mở
rộng.

### Điều kiện dừng đã nổ, và phiên đã DỪNG để hỏi

`dieu_kien_dung` của lease ghi: *"Một hình dạng lỗi lặp lần thứ BA ⇒ DỪNG, hỏi 'có nên làm
việc này không', không hỏi 'vá thế nào'."* Lớp A — nhận diện tên `bash` theo **hình dạng cú
pháp của đối số** — nay là lần thứ **NĂM**:

| lần | revision | hình dạng bỏ sót |
|---|---|---|
| 1 | r7 | HOA/thường (`casefold`) |
| 2 | r11 | hằng `bytes` |
| 3 | r12 | đuôi `.pyw`, cách viết đường |
| 4 | r16 | `pathlib`, hai helper shell |
| 5 | **r17** | `Path("", "bash")`, `Path(".", "bash")`, `{"bash"}` — **và một báo động giả** |

Phiên **không tự chọn**. Phiên đo ba phương án rồi đưa cho chủ kho:

- **(a) nới bảng liệt kê thêm hai hình dạng** — rẻ, nhưng phép đo nói thẳng rằng lần thứ SÁU
  sẽ tới;
- **(b) BỘ TÍNH HẰNG** — rút gọn biểu thức về một GIÁ TRỊ rồi mới hỏi. Đo trên **20 hình
  dạng**: luật liệt kê r16 sai **5/20**, bộ tính hằng sai **1/20**;
- **(c) đảo thành danh sách CHO PHÉP** — đúng doctrine `CLAUDE.md`, nhưng đo được nó sẽ bắt
  **276/586** lời gọi trên cây thật, tức một ratchet 276 mục, **trái thẳng N13** (*"ratchet
  phải NGẮN đi"*).

**Chủ kho chọn (b).** ⇒ **N52**.

### Tám phát hiện, sáu lớp

**Lớp A — bề mặt nhận diện tên** (F2 `Path` nhiều thành phần, F6 tập một phần tử, **F3 báo
động giả**). `Path("", "bash")` đo được là **CHẠY THẬT** (in ra `OK`); `run({"bash"})` thoát
`rc=0`. Chiều ngược: `subprocess.getoutput(Path("bash"))` ném
`TypeError: path-like args is not allowed when shell is true` — r16 báo `[(3, 0)]` cho nó, tức
**bắt oan**, và *"một cổng bắt oan là cổng sẽ bị tắt"*. ⇒ **N52**.

**Lớp B — mô hình phạm vi** (F4). N46 lọc theo vị trí rồi vẫn đòi **đúng một** ràng buộc, nên
`subprocess = object()` · `import subprocess` · `run(["bash"])` cho hai ràng buộc cùng nằm
trước lời gọi ⇒ mơ hồ ⇒ **LỌT**. Và ràng buộc được neo vào **chỗ viết tên** thay vì chỗ
**hoàn tất**, nên `subprocess = subprocess.run(["bash"])` cũng lọt. ⇒ **N53**.

**Lớp C — ranh giới báo cáo** (F7). Đúng món nợ **đặc tả r15 tự khai là chưa đo**:
`_duong_bao_cao` **không đơn ánh** — một đường mang byte `0xff` và một đường chứa bốn ký tự
ASCII `\`,`x`,`f`,`f` cùng ra một chuỗi, mà chuỗi ấy **là KHOÁ** của `co_loi_goi_tran`, nên
một tệp ĐÈ tệp kia. ⇒ **N54**.

**Lớp D — ratchet phán quyết** (F5). N49 gieo sẵn `rc` và so **trùng chuỗi** cho trường tổng
hợp, nên nó **bắt oan bốn ca** — `rc` gieo sẵn, `config["trang_thai"]`, bí danh đã bị ghi đè,
`kq[1]["co_loi_goi_tran"]`. ⇒ **N55**.

**Lớp F — cache** (F1). Vân tay N51 chụp `chan_doan`, tức chỉ những ứng viên **đã có mặt**.
Một `bash` MỚI trong thư mục `PATH` **không đổi** thì không ứng viên cũ nào đổi ⇒ cache trả
`None` trên máy đã có bash. ⇒ **N56**.

**Lớp G — mới** (F8). `PATH` **VẮNG** ≠ `PATH` **RỖNG**: `os.get_exec_path()`/`execvp` lùi về
`os.defpath` khi biến vắng. Gộp hai ca lại làm `ung_vien()` trả `[]` trên máy chạy `bash` được.
`None ≠ ""`, cùng họ `None ≠ False`. ⇒ **N57**.

### Bản vá tự nó làm gãy phép đo, LẦN THỨ HAI liên tiếp

r16 làm gãy 10 phép đo cũ; r17 làm gãy **7 mỏ neo đột biến**. Đó không phải tai nạn mà là hệ
quả có thể đoán trước của việc đổi cơ chế, và cổng bán kính bắt được cả hai lần. Riêng một
chỗ **cổng trên CÂY THẬT** bắt, không phải bộ ca: bản đầu của N52 rút gọn **cả vector**, nên
`subprocess.run(["bash", "-c", kich])` — phần tử sau là một BIẾN — không rút gọn được và
**LỌT**; `.claude/dev/launcher_test.py` khai 7 mà đo được 6. Sửa: mở bao chứa theo **cú pháp**
trước, rút gọn **phần tử đầu** sau.

**Đối chiếu toàn cây r16 ↔ r17: THÊM 0 · MẤT 0** trên 264 tệp. Bộ tính hằng tương đương trên
mã thật và mạnh hơn hẳn trên hình dạng tổng hợp — đúng thứ ta muốn ở một phép đổi cơ chế.

## 0. Vì sao có revision 16 — MƯỜI finding, và BA lớp tự chúng quay lại

Cross-review codex vòng 10 trên `8180970` ra **7 × P2**; cộng ba P2 của lượt `1091c8a` (r14)
chưa từng được xử — vì lượt ấy đẩy lên SAU vòng 8 nên verdict r15 đã ghi `chưa review`, không
ghi `0`. Tổng **10 finding, không có P1**. Executor **đo lại cả mười, cả mười tái hiện đúng
lời soát** trước khi chạm một dòng vá nào.

Xếp theo LỚP, không theo từng lỗi — và ba trong sáu lớp là những lớp packet này ĐÃ đặt tên:

**Lớp A — bề mặt gọi bash che theo LIỆT KÊ** (`getoutput`/`getstatusoutput`; `Path("bash")`).
Đây là **lần thứ TƯ** của lớp *"so khớp theo MỘT cách viết"*: casefold (r7) → byte (r11) →
đuôi `.pyw` (r12) → nay `pathlib` và hai helper shell. `getstatusoutput("bash -c …")` đo được
là **chạy thật**, trả `(0, 'XIN_CHAO')`. ⇒ **N45**.

**Lớp B — mô hình phạm vi Python sai NGỮ NGHĨA**, hai mặt khác nhau:
(a) module và thân lớp chạy theo **thứ tự câu lệnh**, không theo luật tên-cục-bộ-lúc-biên-dịch
của hàm; `import subprocess` · `subprocess.run(["bash"])` · `subprocess = runner` đo được `[]`
trong khi lời gọi dòng 2 **chạy thật**. ⇒ **N46**.
(b) `type X[T] = …` (PEP 695) có phạm vi chú thích RIÊNG; r15 để `T` rò ra phạm vi chứa và
nuốt lời gọi ở dòng dưới. Đo trên Python **3.12.3 thật**. ⇒ **N47**.

**Lớp C — ranh giới báo cáo chỉ sạch trên lối THÀNH CÔNG.** r15 vá `_duong_bao_cao` cho
`co_loi_goi_tran` nhưng nhánh LỖI vẫn nhét đường THÔ vào `ly_do`: một mục `ops/bad_\xff.py`
cú pháp hỏng làm `quet --json` nhả byte `0xff` và bộ đọc UTF-8 nghiêm từ chối **cả** bản báo
cáo — cổng mất tiếng nói đúng lúc nó có chuyện để nói. ⇒ **N48**.

**Lớp D — ratchet N22 nhận diện theo MỘT hình dạng cú pháp.** Nó khớp đúng chữ `rc` và đúng
lời gọi `bang`/`dung`. Hai cửa hậu, cả hai đo được: `assert rc == 2` ⇒ `[]`, và **ca THẬT**
`t45` đặt mã thoát vào `rc_cong` nên **lọt khỏi ratchet từ r11 tới r15**. Cùng LỚP với lớp A —
so khớp theo một cách viết — nên chữa cùng một kiểu: bám vào thứ không đổi tên được, là giá
trị trả về của `_quet`. ⇒ **N49**.

**Lớp E — một cổng không thể ĐỎ thì không phải cổng.** `CA_PHAN_QUYET` đòi mỗi miễn trừ kèm
"lý do kiểm toán được", nhưng không mã nào ĐỌC lý do ấy: thay bằng `""`, khoảng trắng, `None`
hay `123` thì cổng vẫn `rc=0`. Đây là **N6-LOI-KHAI-RONG-HON-PHEP-DO** lần thứ TƯ trong
packet. Kèm theo: thông điệp hỏng của chốt (0) vẫn dặn *"`!=` là ca ÂM hợp lệ, KHÔNG được ép
vào `CA_PHAN_QUYET`"* — đúng cái luật r14 vừa bỏ; ai gặp ĐỎ mà làm theo sẽ khôi phục luật cũ.
Chữa bằng cơ chế: thông điệp **sinh ra từ `_MAU_MONG`**, nên không lệch khỏi luật được nữa.
⇒ **N50**.

**Lớp F — cache trả lời cũ sau khi thế giới đổi.** Khoá gom đủ mọi ĐẦU VÀO (N19 đã làm), nhưng
phán quyết không sinh ra từ đầu vào — nó sinh ra từ phép thử NĂNG LỰC trên một TỆP. Thay tệp
tại chỗ thì khoá không đổi một bit. Tái hiện **cả hai chiều**; chiều độc là `xấu → tốt`: cổng
báo KHÔNG CÓ `bash` trên một máy ĐÃ CÓ. ⇒ **N51**.

### Hai món phải ghi ra, không giấu

1. **`_ra_json` đổi HÌNH DẠNG đầu ra.** `ensure_ascii=True` làm chữ Việt trong `ly_do` ra dưới
   dạng `\uXXXX`. Máy đọc thì y hệt (`json.loads` trả đúng chuỗi cũ), mắt người đọc thì xấu
   hơn. Đổi lấy một lối ra **không bao giờ hỏng**, và chỗ đổi được ghi ở đây chứ không để ai
   phát hiện sau.
2. **N46 còn một lối báo oan chưa đóng.** Một `global` ghi từ hàm định nghĩa SAU lời gọi nhưng
   được gọi TRƯỚC thì vị trí cú pháp nói sai. Nó cần phân tích luồng gọi — **nợ có tên**, khai
   trong docstring `_giai_ten`, không phải chỗ đã kín. Hai chỗ còn lại (nhánh `if` không chạy;
   vòng lặp) đều rơi về phía THẬN TRỌNG.

### Một chỗ verdict r15 nói thiếu, sửa ở đây

Verdict r15 đóng bằng câu *"84/84 bán kính đều 1/52"*. Đúng với các ca ĐÃ CÓ, nhưng nó không
nói rằng **`t45` đang trói phán quyết mà không nằm trong bản kiểm kê** — vì luật kiểm kê lúc
ấy mù trước cái tên `rc_cong`. Một con số 84/84 trên một bộ luật có lỗ thì không rộng bằng lời
nó nghe. r16 vá cái lỗ, và `t45` **vào bản kiểm kê kèm lý do đo được**.

## 0. Vì sao có revision 15 — SÁU finding vòng 8, và hai chỗ executor tự nhận sai

Cross-review codex vòng 8 trên `f6189e3` ra **6 × P2**. Executor **đo lại cả sáu, cả sáu tái
hiện chính xác**.

| | Đo được trên `f6189e3` | Luật |
|---|---|---|
| **F19** `global` + `import` sau phép gán | `[]` — lời gọi bash THẬT không bị thấy | **N39** |
| **F20** cookie mã hoá hỏng | `rc=1` + **traceback**, stdout KHÔNG phải JSON | **N42** |
| **F21** đường mang byte xấu | JSON **không đọc được** bằng bộ đọc UTF-8 nghiêm | **N43** |
| **F22** `_NGAY_GO` | chỉ ở `Assign` + f-string, **không một `Compare` nào**, không `import datetime` | **N44** |
| **F23** PEP 695 `type_params` | **`KeyError`** — CLI thoát 1; và `def f[subprocess]()` **bắt oan** | **N41** |
| **F24** walrus lúc định nghĩa | `[(4, 0)]` — bắt oan một phép che hợp lệ | **N40** |

### HAI CHỖ EXECUTOR TỰ NHẬN SAI — ghi trước, vì chúng là dữ kiện về ĐỘ TIN của verdict

**(a) F19: executor đã lập luận NGƯỢC LẠI codex ở vòng 7, và executor SAI.**
Verdict r13 viết: *"fixture của codex mơ hồ vì tên bị ràng buộc hai lần, nên bộ giải từ chối là
đúng."* Sai. **Sự mơ hồ nằm ở phạm vi MODULE, không nằm trong thân hàm đã tự `import`.** Cơ chế
thật: bản r13 `pop` ràng buộc khỏi phạm vi khai `global`, và `_giai_ten` gặp `global` thì nhảy
thẳng về bảng module. Codex nêu lại đúng ca ấy ở vòng 8; lần này executor đo lại thay vì bảo lưu.

**(b) F21 là món NỢ verdict r13 ĐÃ TỰ KHAI** — *"báo cáo một đường như vậy ra JSON trên nền khác
thì CHƯA ĐO."* Nay đo được. Nợ đến hạn, không phải bất ngờ.

**(c) F22 lại đúng họ N6-LOI-KHAI-RONG-HON-PHEP-DO** — lần thứ **BA** trong packet (sau
`ANH_CHUP_DONG_CUNG` ở r13, và chính bảng ratchet này): *"NGÀY GỠ"* là **chữ trang trí trong lý
do**, không phải phép đo.

### F23 ĐO ĐƯỢC THẬT, không viết theo mô tả

Máy soạn bản vá chạy **Python 3.11**, nơi cú pháp PEP 695 còn là `SyntaxError` — chưa tới
`KeyError`. Nhưng máy **có sẵn `/usr/bin/python3.12`**, nên phép đo chạy trên **3.12.3 thật**:

```
def f[T: shutil.which("bash")](): pass          => KeyError   (SAP, khong phai bo sot)
class C[T: subprocess.run(["bash"])]: pass      => KeyError
def f[subprocess](): subprocess.run(["bash"])   => [(3, 4)]   (BAT OAN)
```

`t50` tự đi tìm trình thông dịch **>= 3.12** và đo qua tiến trình con của nó; không tìm thấy thì
`BoQuaMoiTruong` **kèm chẩn đoán đo được** — `KHÔNG ĐO ĐƯỢC` không được lặng lẽ thành xanh. CI
ghim `python-version: "3.12"` ở **cả ba** chỗ gọi bộ ca, nên trên CI ca này CHẠY.

### Ba khuyết tật của chính bản vá r15, bắt được trước khi chạy bộ

1. Nhánh `elif` cho walrus **không bao giờ chạy được** — nhánh `if` phía trên đã nuốt
   `FunctionDef`. Một bản vá không tới được thì không phải bản vá.
2. `_giai_ten` gặp `global` là **nhảy thẳng về bảng module**, nên "chép thay vì dời" một mình
   không đủ. Phải thêm: phạm vi khai `global` mà TỰ NÓ ràng buộc tên ấy thì dùng ràng buộc ấy.
3. Đột biến `bn_bo_type_params` **không giết được gì** vì bộ ca chạy 3.11. Tách PEP 695 thành
   ca `t50` có **nền riêng** biết tự khai khi không đo được.

### CÁI GIÁ, khai thẳng

- **`quet()` nay đọc ĐỒNG HỒ.** Phán quyết phụ thuộc ngày — đó là điều packet này vốn chống
  (*"phán quyết phụ thuộc trạng thái LOCAL"*). Giảm thiểu: so theo **UTC**, và `hom_nay` tiêm
  được để ca đo ĐỎ được mà không phải chờ tới cuối năm. Nhưng **vẫn là một biến ngoài mã**, và
  ghi ra ở đây thay vì để người sau phát hiện.
- **`_duong_bao_cao` là một phép LOSSY ở biên giới báo cáo.** Đường nội bộ vẫn nguyên vẹn cho
  việc đối chiếu INDEX; nhưng hai đường khác nhau về byte xấu CÓ THỂ in ra giống nhau. Chưa đo
  trường hợp ấy.

## 0. Vì sao có revision 14 — NỚI N22, vì cùng một hình dạng lỗi lặp BA revision liên tiếp

r14 **không** sinh từ một finding của codex. Nó sinh từ **bán kính đột biến của chính bộ ca**,
và từ một quyết định của chủ kho sau khi executor trình phép đo.

### Hình dạng lặp

| revision | ca | chốt SAI | vì sao lọt qua N22 cũ |
|---|---|---|---|
| r11 | `t45` | "cây bẩn ⇒ điểm vào phải hỏng" | không so `rc` với `2`, không so `trang_thai` với `"DO"` |
| r12 | `t47` | đọc `ngoai_danh_sach` | không phải phép so trên `rc`/`trang_thai` |
| r13 | `t48` | `rc == 0` | luật cũ **chỉ** phủ chiều ĐỎ |

Cả ba đều là *"ca chốt trên KẾT QUẢ trong khi thuộc tính nó phải trói là CƠ CHẾ"*, và cả ba
đều được **bán kính đột biến** bắt chứ không phải luật bắt. `dieu_kien_dung` bắt dừng ở lần
thứ **ba**; executor dừng, trình phép đo, chủ kho quyết: **nới N22**.

### Một câu của r7 bị BÁC bằng phép đo

r7 thu hẹp N22 về chiều ĐỎ với lý lẽ: *"chiều XANH (`rc == 0 … "DAT"`) là NỀN của gần như mọi
ca — cấm nó thì không ca nào viết được."* Câu ấy **chưa từng được đo**. r14 đo:

```
13 ca co goi `_quet`
noi rong bat them:  SAU ca   (khong phai "gan het")
```

Sáu ca ấy đi đúng **hai** đường, không có đường thứ ba:
- **viết lại theo TRƯỜNG CƠ CHẾ** — `t27` (chú thích không sinh lời gọi ⇒ `co_loi_goi_tran`
  rỗng), `t35`, `t37`, `t46`;
- **khai tường minh vào `CA_PHAN_QUYET` kèm lý do** — `t44` và `t47`: fail-close **là** thuộc
  tính của chúng.

`CA_PHAN_QUYET` từ danh sách **ba mục bỏ sót sáu** thành **kiểm kê năm mục đủ**. Câu cũ của r7
được **giữ nguyên trong docstring** cạnh phép đo bác nó — không xoá.

### Bốn khuyết tật của chính bản vá r14, bắt được trước khi chạy bộ

1. Một sửa vào **nhầm ca** (`t25` thay vì `t27`) vì neo theo VĂN BẢN. Hoàn nguyên, định vị lại
   qua `ast` theo **tên hàm**.
2. Lát cắt ăn mất `return ra` ⇒ hàm trả `None` ⇒ **luật im hoàn toàn**. Tự kiểm bắt: cả năm tên
   trong danh sách báo "không còn chốt".
3. Một script ném lỗi **sau khi sửa, trước khi ghi** ⇒ mất thay đổi mà executor tưởng đã vào.
4. Đột biến `t39_bo_phep_so_bang` mất mỏ neo (dòng nó neo không còn). Thay bằng **hai** đột
   biến trói **hai chiều** của luật mới — kể cả chiều "nới quá", đúng chiều r7 đã sợ.

## 0. Vì sao có revision 13 — ẢNH CHỤP "ĐÔNG CỨNG" chỉ ĐẾM SỐ, và hai món nợ đến hạn

Cross-review codex vòng 7 trên `cf6e6cb` ra **3 × P2**; executor **đo lại cả ba, cả ba tái hiện**.

### Một lỗi trong chính phép ĐẾM của executor — ghi trước, vì nó suýt làm hỏng verdict

Lần đếm đầu ra **1** finding. **Sai.** API trả `totalCount: 32` mà chỉ đưa **30** kèm
`hasNextPage: true`; verdict suýt được viết trên một **phép quét MÙ**. Đây đúng hình dạng mà
`ai-dang-giu` của kho đã dạy từ g9: *chốt hai nguồn rồi mới kết luận*. Lấy đủ thì là **3 × P2**.
Ghi ra vì một phép đếm mù không tự khai là mù.

### Ba finding

| | Đo được trên `cf6e6cb` |
|---|---|
| **F16** biểu thức lúc định nghĩa | `def f(shutil=shutil.which("bash"))` ⇒ `[]` — định nghĩa `f` CÓ gọi bash mà cổng không thấy |
| **F17** ảnh chụp "đông cứng" | đổi **HẾT** bảy `shutil.which("bash")` sang `subprocess.run(["bash"])`, giữ nguyên số 7 ⇒ vẫn `rc=0 DAT`, `lech_so` RỖNG |
| **F18** khung `ls-files` | `ops/va\r.py` (bẩn) và `ops/va\n.py` (sạch, OID cao hơn) gộp thành MỘT `rel` ⇒ `rc=0 DAT`, `co_loi_goi_tran` **RỖNG** — vi phạm tàng hình |

### F16 và F17 là HAI MÓN NỢ ĐÃ KHAI TRƯỚC, nay đến hạn — không phải hai bất ngờ

- **F16**: spec r12 ghi nguyên văn chỗ bỏ qua — *"decorator / giá trị mặc định của một `def`
  lồng và `iter` đầu tiên của comprehension thật ra thuộc phạm vi NGOÀI… chưa có phép đo nào
  cần nó."* Codex đưa ra **đúng phép đo ấy**. Bốn hình dạng (`x=…`, `@…`, `x: …`, `class C(…)`)
  vốn **đã** bắt được vì tên không bị che; lệch chỉ lộ khi **chính tham số che tên module**.
- **F17** là hình dạng kho đã đặt tên ở packet **N6-LOI-KHAI-RONG-HON-PHEP-DO**: bảng KHAI
  *"không được sửa một byte"* mà chỉ **ĐO số lời gọi**. Lời khai rộng hơn phép đo.

### F18 — lớp mới: một phép biến đổi làm mất thông tin chạy TRƯỚC khi tách khung

`text=True` dịch dòng phổ quát trước khi tách `\0`/`\t`, nên hai đường khác nhau trong INDEX
gộp làm một và `_doc_noi_dung` ghi đè im lặng. Khác các lớp trước: không phải trạng thái máy,
không phải một cách viết — mà là **thứ tự** giữa giải mã và tách khung.

### Một khuyết tật của chính bản vá r13, CỔNG bắt được trước executor

Bản đầu của N37 truyền nút phạm vi vào hàm duyệt như **gốc**, nên chính nó không còn được nhận
là phạm vi: **một hàm lồng trong hàm mất đúng một tầng**. Cổng trên cây THẬT ra **ĐỎ** và chỉ
thẳng `scripts/tl_selftest.py` (khai 1 lời gọi, đo được 0) — tức N31 (cổng được nối vào điểm
vào) đã trả công ngay ở revision kế tiếp. Ca tối giản: `def run(): def f(): import shutil as
sh; sh.which("bash")` ⇒ `[]`. Đã viết lại thành **một đường duyệt duy nhất** (`tham`).

### CÁI GIÁ, khai thẳng

- Làm mới một ảnh chụp đông cứng nay **phải cập nhật OID tường minh**. Đó là cái giá, và là
  cái giá ĐÚNG: nếu không thì "đông cứng" chỉ là một chữ trong docstring.
- Giải mã đường dẫn bằng `surrogateescape` giữ được byte nhưng **báo cáo** một đường như vậy
  ra JSON vẫn có thể lỗi trên nền khác — **CHƯA ĐO trên Windows**.

## 0. Vì sao có revision 12 — ĐỔI EFFORT xuống `low`, và BỐN mặt của "đọc INDEX cho đúng"

r12 tồn tại vì **hai** lý do độc lập.

### Lý do thứ nhất: chủ kho hạ EFFORT của cả executor lẫn reviewer xuống `low`

Chỉ thị 2026-09-23: *"Executor: fable 5.1, effort **low**. Review codex gpt-6-astra, effort
**low**."* r11 đóng băng `effort: medium` cho cả hai, **và §7.0 nêu đích danh hai con số ấy**.
Đổi một thuộc tính của executor ⇒ `docs/PROTOCOL_DA_PHIEN.md` §3.2 đòi revision + generation
mới — cùng hình dạng r8 (đổi executor `claude` → `fable`). Không phải một sửa nhỏ trong lease.

### Lý do thứ hai: cross-review codex vòng 6 trên `1d63f80` — 4 × P2, tái hiện cả bốn

| | đo được trên `1d63f80` |
|---|---|
| **F12** `git replace` | sau `git replace <xấu> <sạch>`: `ngoai_danh_sach` **RỖNG**; đặt `GIT_NO_REPLACE_OBJECTS=1` ⇒ `['vi_pham.py']` |
| **F13** INDEX chưa hoà giải | `ls-files -s` phát stage **1/2/3**; bản ghi rơi mất trường stage ⇒ blob SHA lớn nhất thắng ⇒ `ngoai=[]` |
| **F14** PEP 263 / BOM | `# coding: latin-1` và BOM UTF-8 đều ra `rc=3 KHONG_DO_DUOC` — Python **hợp lệ** chặn vĩnh viễn cả kho |
| **F15** `VI_PHAM.PY` / `.pyw` | `ls-files --cached -s -- '*.py'` trả **RỖNG** ⇒ cả hai vô hình |

**F12 là MẶT THỨ TÁM của lớp *phán quyết phụ thuộc trạng thái LOCAL của máy*** — nhưng nó
**không** đòi một quyết định kiến trúc thứ ba. Nó là đúng món **nợ spec r11 đã KHAI TRƯỚC**:
*"Danh sách biến git bị gỡ KHÔNG BAO GIỜ ĐỦ… Một biến git mới mà r11 chưa biết sẽ KHÔNG bị gỡ."*
Nợ ấy nay đến hạn. Cơ chế không đổi (gỡ môi trường + ghim nguồn đối tượng), chỉ thêm một biến
và một cờ. Ghi ra để người sau phân biệt *"lớp sống lại"* với *"nợ đã khai đến hạn"*.

**F15 là thực thể THỨ BA của lớp *so khớp theo MỘT cách viết*** (sau hoa/thường ở r7 và hằng
byte ở r11). Lần thứ ba thì chữa bằng **cơ chế**: hậu tố ra một hàm `_la_nguon_py` dùng
`casefold()`, và pathspec `*.py` bị bỏ hẳn — lọc trong Python, không nhờ git so chuỗi.

### Một khuyết tật của chính bản vá r12, tự bắt trước khi đo

Bản đầu đặt HAI hàng rào cho ref thay thế ở **hai nơi** (biến môi trường trong
`_moi_truong_git_sach`, cờ `--no-replace-objects` tại chỗ gọi). Hậu quả: **không đột biến nào
đo được cái nào** — bỏ một hàng rào thì hàng rào kia vẫn che, nên ca đích vẫn xanh. *Một luật
không thể ĐỎ thì không phải luật.* Đã gom cả hai vào **một** hàm `_chay_git`, nơi dựng mọi tiến
trình git con của cổng; một đột biến gỡ cả hai, và `t47` chốt (1) ĐỎ được.

## 0. Vì sao có revision 11 — LỚP ẤY CÒN PHỦ "BYTE NÀO" và "INDEX NÀO", và CỔNG CHƯA TỪNG ĐƯỢC NỐI

Cross-review codex vòng 5 trên `6131cbd` ra **1 × P1 + 5 × P2** — **P1 đầu tiên** của packet.
Executor **đo lại cả sáu, cả sáu tái hiện chính xác**.

### P1 — cái cổng cả packet sinh ra để dựng CHƯA TỪNG được nối vào chỗ nó gác

`.github/workflows/ci.yml` gọi `python ops/cong_cu_test.py` ở **BA** chỗ và **KHÔNG** chỗ nào
gọi `ops/bash_nen.py quet`. `main()` thì chỉ chạy ca trên cây **GIẢ** cộng bán kính đột biến.
Đo lại trên một **bản sao kho** (không chạm tệp ngoài write set), **bằng chứng dương**:

```
them `vi_pham_moi.py` co shutil.which("bash") roi `git add`:
  python3 ops/bash_nen.py quet --root .  =>  rc=2 DO, ngoai_danh_sach=['vi_pham_moi.py']
  python3 ops/cong_cu_test.py            =>  rc=1 (chi la nen t2_go_canary)
                                             ten tep vi pham xuat hien 0 LAN trong ca bao cao
```

Một cổng không ai gọi thì không phải cổng. Đây là hình dạng **nặng nhất** packet gặp: bốn
revision trước đi hoàn thiện một cái cổng mà không ai kiểm xem nó có được cắm vào không.

### Hai P2 là MẶT THỨ SÁU và THỨ BẢY của lớp r9 đã "giết bằng kiến trúc"

| mặt | đo được trên `6131cbd` |
|---|---|
| **symlink** — mục `*.py` trong INDEX là symlink | `read_text()` đi theo **ra ngoài kho**; sửa tệp đích bên ngoài làm phán quyết đổi `['ops/lien_ket.py']` → `[]` trong khi INDEX **không đổi một byte**, `nguon_tep` vẫn khai `git` |
| **`GIT_INDEX_FILE`** kế thừa | cùng một kho: index THẬT trả `['bad.py']`, đặt `GIT_INDEX_FILE` trả `[]` — **cả hai lần đều khai `nguon_tep=git`** |

r9 lấy **DANH SÁCH** từ INDEX và tưởng thế là giết xong lớp *phán quyết phụ thuộc trạng thái
LOCAL của máy*. Nhưng lớp ấy còn phủ **"BYTE nào"** (nội dung vẫn đọc từ cây làm việc) và
**"INDEX nào"** (`git -C` không ghim được kho khi biến môi trường chọn index có mặt).
Chủ kho quyết ở r11: **nội dung cũng lấy từ INDEX** (`cat-file --batch` trên blob đã stage),
và **gỡ mọi biến git chọn kho / chọn index / tiêm cấu hình** khỏi tiến trình con.
Đây là lần thứ HAI chủ kho quyết kiến trúc cho cùng một lớp — ghi ra vì nó là dữ kiện về LỚP,
không phải về một bản vá.

### Ba P2 còn lại — hai trong số đó là mặt mới của hai lớp đã có tên

- **`global` / `nonlocal`** (lớp của N27: *phân loại ràng buộc theo TÊN mà bỏ một TRƯỜNG*).
  Sai **cả hai hướng**: `def f(): global subprocess; import subprocess; …run(["bash"])` ⇒ `[]`
  (LỌT một lời gọi thật); `def f(): global subprocess; subprocess = gia()` rồi gọi ở module ⇒
  `[(5, 0)]` (OAN). `nonlocal` cùng bệnh: `[(6, 4)]`.
- **walrus trong comprehension** (cùng lớp). PEP 572: `:=` trong comprehension ràng buộc ở
  phạm vi **CHỨA** nó. Bỏ qua ⇒ `[(3, 0)]` — cổng CHẶN một phép che hợp lệ.
- **hằng byte** (lớp *so hằng theo MỘT kiểu biểu diễn*, cùng lớp với mặt hoa/thường ở r7).
  `shutil.which(b"bash")`, `run([b"bash"])`, `run(b"bash")`, `executable=b"bash"`,
  `which(b"BASH.EXE")` — **cả năm** ra `[]`, một đường vòng không cần phân tích luồng dữ liệu.

### CÁI GIÁ, khai thẳng

- **Tệp đã `git add` rồi sửa tiếp trên đĩa được quét ở DẠNG ĐÃ STAGE.** Cổng thôi phản ánh đĩa.
  Trong CI không khác gì (checkout sạch); tại chỗ nghĩa là "cổng xử thứ anh đã stage" — đúng
  mạch N23. `t46` chốt (3) trói đúng đánh đổi ấy.
- **Mục `*.py` là symlink ⇒ fail-close có tên.** Đo trên kho hôm nay: `git ls-files -s -- '*.py'`
  có **0** mục mode `120000` trên **264** — luật này không tốn gì ở hiện tại, nó là hàng rào cho
  ngày mai.
- **Danh sách biến git bị gỡ KHÔNG BAO GIỜ ĐỦ.** Đó chính là lý do nó đi KÈM việc đọc blob:
  hai hàng rào phải cùng thủng thì phán quyết mới sai. Một biến git mới mà r11 chưa biết sẽ
  KHÔNG bị gỡ — ghi ra thay vì để người sau tưởng danh sách là đủ.
- **Nhánh `nonlocal` chỉ đo được theo CHIỀU BỚT OAN.** `nonlocal x` đòi `x` đã bị ràng buộc ở
  một phạm vi hàm bao, nên tên ấy **luôn** có ≥2 ràng buộc ⇒ bộ giải luôn trả `None`. Không
  dựng được ca dương cho nhánh ấy; khai thẳng thay vì giả vờ phủ hai chiều.
- **Fixture nguyên văn của codex cho `global` vẫn ra `[]` sau khi vá** — nhưng vì **lý do khác
  và đúng**: nó có thêm `subprocess = object()` ở module, nên tên bị ràng buộc **hai lần** ⇒ mơ
  hồ ⇒ bộ giải từ chối theo luật bảo thủ của chính nó. Ca cô lập (`def f(): global subprocess;
  import subprocess; …`) nay **BẮT** `[(4, 4)]`, tức cơ chế codex nêu ĐÃ được vá.

## 0. Vì sao có revision 10 — CỬA SAU của một lớp đã tưởng giết xong, và một PHƯƠNG PHÁP được đóng băng

r10 tồn tại vì **hai** lý do, và cả hai đổi tiêu chí nghiệm thu nên §3.2 đòi revision mới.

### Lý do thứ nhất: N23 để hở một đường LÙI, và đường ấy mở lại đúng cái lớp r9 vừa giết

Cross-review codex vòng 4 trên `e290f99` ra **2 × P2**. Executor **đo lại cả hai, cả hai tái
hiện chính xác** — không nhận lời khai:

| | Đo lại được trên `e290f99` |
|---|---|
| **F5** không fail-close khi INDEX hỏng | cây có `.git` GIẢ ⇒ `_liet_ke_py` trả `rac_bi_ignore.py` kèm `rglob-git-hong`; `quet` ra **`rc=2 DO`** |
| **F6** `ImportFrom.level` bị bỏ qua | `from .subprocess import run; run(args=["bash"])` ⇒ **`[(2, 0)]`** — bắt oan một API nội bộ |

**F5 KHÔNG phải "một lỗi nữa".** Lớp *phán quyết phụ thuộc trạng thái LOCAL của máy* đã lộ BỐN
mặt qua ba bản vá nối tiếp, và r9 giết nó bằng kiến trúc: danh sách = INDEX, không còn luật
ignore nào để nghe. Nhưng r9 **giữ lại một đường LÙI** khi git hỏng, và trên đường ấy danh sách
lại là `rglob` — tức lại nghe trạng thái máy. r9 **đặt tên** cho đường lùi (`rglob-git-hong`)
với lý lẽ *"người đọc phải thấy"*. Một **TRƯỜNG** cho người đọc không phải một **CỔNG**: đúng
thứ `CLAUDE.md` gọi là *lời dặn bằng miệng không phải hàng rào*, lần này nằm trong chính mã của
packet. Không lấy được INDEX thì **không có danh sách**, nên **không có phán quyết**.

**Quét theo LỚP ra mặt thứ BA codex không chỉ.** Chỉ thị chủ kho: *"cross-review tìm kiếm, phân
theo LỚP, không phải từng lỗi riêng lẻ"*. Lớp của F6 là *"một ràng buộc được phân loại theo cái
TÊN mà bỏ qua một TRƯỜNG của nút AST quyết định ý nghĩa"*. Ba mặt, **hai chiều ngược nhau**:

| mặt | chiều | đo được trước vá | codex chỉ? |
|---|---|---|---|
| `ImportFrom.level >= 1` | **bắt oan** | `[(2, 0)]` | có |
| `import subprocess.x` (ràng buộc `subprocess` vào module THẬT) | **bỏ sót** | `[]` | **không** |
| `from subprocess import *` | bỏ sót | `[]` | không — **nợ có tên** từ trước, không phải mặt mới |

### Lý do thứ hai: PHƯƠNG PHÁP của vòng lặp chưa từng được đóng băng ở đâu

Chủ kho (phiên 2026-09-21 ~18:2xZ, nhắc lại 2026-09-23) đổi điều kiện thoát vòng lặp từ *"tới
khi APPROVE"* sang **"tới khi không còn finding P1, P2, P3"**, và ghi thêm phương pháp: review
bằng **codex phiên bản/effort cao hơn**, **hint patch** cho vấn đề phức tạp, **phân theo lớp
lỗi**, **đăng verdict** mỗi vòng, **không CI** tới khi đủ điều kiện merge, **không cần CI
Windows** (lỗi đã biết từ trước).

**ĐO, không đoán:** spec r9 §7 chỉ liệt kê điều kiện dừng của **EXECUTOR**; `dieu_kien_dung`
của lease g9 cũng vậy. **Không chỗ nào** ghi điều kiện thoát của VÒNG LẶP REVIEW. Nên đây là
**ghi lần đầu**, không phải sửa một tiêu chí đã đóng băng. Nó vào §7.0.

### CÁI GIÁ, khai thẳng

- `KHONG_DO_DUOC` **nhiều hơn** trước: mọi cây có `.git` mà git hỏng (hết giờ, rc khác 0, không
  sinh được tiến trình) nay làm cổng dừng thay vì ra số. Đó là **cố ý** — `None ≠ False`.
- `rglob` **vẫn sống** cho cây KHÔNG phải kho git. Bộ ca dựng cây giả phụ thuộc đường ấy, nên nó
  có ca giữ riêng (`t44` chốt (2)); thiếu chiều ấy thì một đột biến *"lúc nào cũng
  KHÔNG_ĐO_ĐƯỢC"* sẽ sống và cả bộ ca chết theo.
- **LỠ HẠN LEASE g9 ĐÃ TỐN MỘT NGÀY.** g9 hết hạn 2026-09-22T06:25Z với bản vá r10 đã viết xong
  nhưng chưa land. Phiên KHÔNG tự gia hạn, KHÔNG đẩy — đúng luật — và cái giá là 26 giờ. Ghi ra
  để hạn của g10 được đặt theo phép đo ấy chứ không theo thói quen.

## 0. Vì sao có revision 9 — GIẾT CẢ MỘT LỚP BẰNG KIẾN TRÚC, không vá mặt thứ tư

r9 **thu hẹp N17**. Đó là đổi tiêu chí nghiệm thu, nên `docs/PROTOCOL_DA_PHIEN.md` §3.2 đòi
revision mới. N17 (r4) khai *"cổng quét TOÀN CÂY"*; r9 đọc lại cho đúng: **toàn cây, phần
ĐÃ THEO DÕI** — danh sách tệp là `git ls-files --cached`, không hơn.

### Lý do: một lớp đã vá BA mặt nối tiếp, và mặt thứ tư đo được

Lớp *"phán quyết phụ thuộc trạng thái LOCAL của máy chạy"*:

| vòng | mặt được bịt | mặt hở ra |
|---|---|---|
| 1 | thư mục rác (`node_modules/`) — `rglob` chạm cả thứ `.gitignore` đã loại | `core.excludesFile` TOÀN CỤC |
| 2 | `core.excludesFile`, `.git/info/exclude` | `.gitignore` CHƯA THEO DÕI trong cây làm việc |
| r8 | blob `.gitignore` ĐÃ THEO DÕI, `XDG_CONFIG_HOME` | **kho nào trả lời** khi `.git` lồng nhau |

Mỗi bản vá **đúng, có răng, và để hở mặt kế**. `CLAUDE.md` gọi tên hình dạng ấy: *"vá đúng chỗ
được chỉ rồi bỏ sót đường thứ ba"*. Đến mặt thứ ba, executor **DỪNG** theo `dieu_kien_dung` và
hỏi *"có nên làm việc này không"* thay vì *"vá mặt thứ tư thế nào"*.

**Gốc của cả lớp là một quyết định kiến trúc ở r7:** cổng quét cả tệp **CHƯA THEO DÕI**, nên nó
buộc phải tự trả lời *"tệp nào bị ignore"* — và câu ấy **luôn còn một tầng máy nữa**.

**CHỦ KHO QUYẾT: chỉ quét INDEX.** Khi cổng không đọc luật ignore nào, cả lớp **chết theo kiến
trúc**, không phải theo bản vá. ~110 dòng kho tạm + trích blob bị gỡ hẳn.

### CÁI GIÁ, khai thẳng — đây là một ĐÁNH ĐỔI, không phải một tính chất tự nhiên

Tệp **chưa `git add`** không được quét. Trong CI cây luôn đã commit nên độ phủ không giảm; tại
chỗ, ai quên `add` sẽ thấy ở PR. **Câu sau là LÝ LẼ về CI, CHƯA ĐO** — ghi đúng như thế.

Hệ quả đo được: `ls-files --cached -- '*.py'` = **264 tệp**, `--others` thô = **0** ⇒ chênh **0**
trên kho hôm nay. Con số ấy **sẽ khác** trên một cây có tệp chưa add.

Và kỳ vọng "nhanh hơn" **KHÔNG THÀNH**: `quet` kho thật 3,04 / 3,04 / 3,12s, so HEAD 2,8–3,1s.
Chi phí nằm ở `ast.parse` 264 tệp, không ở việc liệt kê (6–8ms ở cả hai bản). Khai ra thay vì
im, vì một kỳ vọng sai được giữ lại sẽ thành lý lẽ cho quyết định sau.

## 0. Vì sao có revision 8 — ĐỔI EXECUTOR sang Fable 5.1

r8 không bác r7. Nó đổi **executor**, và `docs/PROTOCOL_DA_PHIEN.md:115` nói rõ đó là thứ đòi
revision mới: *"Packet đổi objective/acceptance/write-set/dependency/**executor**/environment
phải có [revision mới, generation mới, cấp lại lease]"*. Chạy executor khác dưới lease g7 —
vốn khai `executor: claude` — là thi công ngoài thứ lease khai, đúng loại sai mà `t24` (ghi
chú SAI SỰ THẬT) sinh ra để bắt.

**Chỉ thị chủ kho** (phiên 2026-09-21 ~16:1xZ): *"Sử dụng fable7.1 executor cho #581 tới
approve"*.

### "Fable 7.1" KHÔNG TỒN TẠI trong môi trường này — khai thẳng thay vì đoán

Phiên **không** tự dịch "7.1" thành một bản có thật. Nó DỪNG và hỏi, vì lệch phiên bản đúng là
loại nhầm lẫn packet này đã trả giá ở bộ đo `570-do-9` (chạy đúng nhưng trên **cây sai**, và
không có chốt nào bắt). Đo được trong môi trường phiên:

```
Agent model enum:  sonnet | opus | haiku | fable
Fable duy nhất với tới được:  claude-fable-5-1   (Fable 5.1)
```

Chủ kho xác nhận **Fable 5.1**. Lease g8 khai `model: claude-fable-5-1`, **không** khai "7.1".

### CÁI GIÁ, khai trước khi ai phải tự tìm ra

Executor mới **không sống qua** bảy lần lặp của hình dạng *"một ca khẳng định KẾT QUẢ trong khi
thuộc tính phải trói là CƠ CHẾ"*, cũng không sống qua năm lần mắc bẫy *"đột biến tệp không cắn
được mã đã nạp trong tiến trình"*. Những bài học ấy hiện chỉ sống ở ba chỗ:

1. **Đặc tả này** (N20, N21, N22 và §0 của r4/r6/r7);
2. **Docstring từng ca** — mỗi ca nêu THUỘC TÍNH nó trói ngay dòng đầu;
3. **Cổng đo được** — 44 ca, 52 đột biến, bán kính 1/44, cộng luật `t39` (N22).

Chỗ (3) là chỗ duy nhất **không phụ thuộc trí nhớ ai**. Đó là lý do việc đổi executor ở giữa
packet chịu được: thứ giữ chất lượng là **phép đo**, không phải người. Nhưng nói cho đủ —
`t39` chỉ bắt hình dạng "chốt trên PHÁN QUYẾT"; lần thứ BẢY (chốt cuối của `t41`) **không**
phải hình dạng ấy nên nó lọt qua `t39` và chỉ bị **bán kính đột biến** bắt. Phần còn lại vẫn
dựa vào người đọc. Đó là **nợ có tên**, không phải chỗ đã kín.

### Cái KHÔNG đổi

`assurance_target: human_audited` và `cross_reviewer_requirement` giữ nguyên: **cấm
`self_review` và `self_approve`**. Đổi executor **không** làm Fable được tự duyệt. *"Tới
approve"* trong chỉ thị nghĩa là **codex hết finding** cộng **chủ kho nghiệm thu** — không
phải executor tự tuyên bố xong.

Và một ràng buộc kế thừa: phiên claude hiện tại **là tác giả** của bản vá đang nằm trong #581,
nên nó cũng không được đóng vai reviewer cho Fable ở phần mã ấy. Vai của nó từ r8 là **điều
phối và đo**, không phải duyệt.

## 0. Vì sao có revision 7 — BỐN finding P2 của codex, và một LUẬT cho bộ ca

r7 không bác r6. Nó nhận một lượt **cross-review codex**, và — quan trọng hơn — nhận một
**hình dạng lỗi đã lặp SÁU lần** mà `dieu_kien_dung` bắt phải dừng lại từ lần thứ ba.

### Bốn finding — đo lại cả bốn, cả bốn tái hiện chính xác

Connector `codex` hồi phục hạn mức (lượt trước trên #571 nó trả *"You have reached your Codex
usage limits"*) và review `55f9bce` lúc 07:35–07:44Z: `COMMENTED`, **4×P2**, tất cả trên
`ops/bash_nen.py`. Executor **đo lại** thay vì nhận lời khai:

| | codex khai | executor đo được |
|---|---|---|
| **A** ratchet tha CẢ TỆP | thêm lời gọi thứ hai vào mục khai 1 vẫn `DAT` | `rc=0 DAT`, `co_loi_goi_tran=[2,3]` |
| **B** quét cả thư mục bị `.gitignore` | báo động giả | `node_modules/x.py` ⇒ **DO**; `hong.py` ⇒ **rc=3 KHONG_DO_DUOC** |
| **C** khoá cache thiếu `cwd`/`PATHEXT` | trả bản nhớ sai | đổi `cwd` ⇒ **cùng kết quả** |
| **D** tên thực thi so PHÂN BIỆT hoa/thường | `BASH.EXE` lọt | `BASH.EXE` ⇒ `[]`, `Bash.exe` ⇒ `[]` |

**D đắt nhất:** cổng vừa mở ra toàn cây bị **đi vòng bằng một phím Shift**, trên đúng cái nền
mà packet này sinh ra để phục vụ. **B nặng hơn lời khai:** vế *fail-close CẢ KHO* vì một tệp
rác không phân tích được là executor đo thêm — codex không nói.

Cách vá: (A) mỗi mục `CHUA_CHUYEN` mang **số lần được phép**, lệch chiều nào cũng ĐỎ;
(B) **hỏi git** (`ls-files --cached --others --exclude-standard`) thay vì chép một danh sách
cấm, và khai `nguon_tep` ba trạng thái; (C) `getcwd()` + `PATHEXT` vào khoá — khai thẳng rằng
`PATHEXT` **chưa đo được** trên nền Linux, nó vào khoá vì lý lẽ đọc từ mã; (D) `casefold()`
một phía, kèm chắn `isinstance(str)`.

### Hình dạng lặp lần thứ SÁU — lý do thật khiến r7 tồn tại

Một ca khẳng định **KẾT QUẢ / PHÁN QUYẾT** trong khi thuộc tính nó phải trói là một **CƠ CHẾ**,
hoặc là thứ ca khác **đã** trói:

| | chỗ | bắt ở |
|---|---|---|
| 1 | `_ket_luan_ban_kinh` in NGUYÊN NHÂN khi mới chỉ ĐẾM | r4 |
| 2 | `t33` chốt (3) cấm chuỗi trên TOÀN docstring | r4 |
| 3 | `t35` chốt (1) khẳng định `rc == 2` — thuộc tính của `t25` | r4 |
| 4 | `t34` khẳng định `sau == khac` — cơ chế là KHOÁ CACHE | r6 |
| 5 | `t38` khẳng định `t1 != t2` — giá trị trả về là chuỗi TƯƠNG ĐỐI | r7, bắt trước khi đẩy |
| 6 | `t37` chốt (3) khẳng định `rc == 2` — lại thuộc tính của `t25` | r7, cổng bán kính bắt |

`dieu_kien_dung` của g6 ghi: *"Một hình dạng lỗi lặp lần thứ BA ⇒ DỪNG, hỏi **có nên làm việc
này không**, không hỏi **vá thế nào**."* Đã quá gấp đôi ngưỡng, và mỗi lần chỉ lộ ra **sau**
một lượt đột biến 55 phút.

**CHỦ KHO QUYẾT: thêm LUẬT, không vá từng ca** — chỉ thị 2026-09-21, chọn *"Thêm LUẬT cấm,
không vá từng ca"* trong ba phương án đã trình (hai phương án kia: chỉ sửa `t37`; hoặc dừng
hẳn). Đó là **N22**.

## 0. Vì sao có revision 6 — `t34` ĐỎ trên Windows, và NGUYÊN NHÂN CHƯA ĐO ĐƯỢC

r6 không bác r4. Nó nhận một **phép đo Windows** mà r4 chưa có, và sửa một khuyết tật nằm trong
**chính bộ đo** của r4.

**Vì sao có khoảng trống generation 5.** `wp570-bash-nen-r5-g5-bia-mo` là một lease **bia mộ**,
`write_set` RỖNG, cấp 2026-09-20T19:44Z theo chỉ thị *"thu hồi sớm lease g4 của #570 bằng bia
mộ đi"* (`issuecomment-5752188461`), với lý do **packet đã LAND** (PR #571 merge `395bc7b1`).
Đo lúc 2026-09-21T01:4xZ: `ai-dang-giu` trả `NGƯỜI_GIỮ 0` cho cả bốn đường — thu hồi **đã có
hiệu lực thật**, không phải khai suông.

**Nhưng tiền đề "packet đã LAND" là KHÔNG ĐỦ, và đây là chỗ phải ghi thẳng.** Bản merge
`395bc7b1` mang r3: `thu_muc = goc / "ops"`, `CHUA_CHUYEN = {}`, 35 ca. Ba finding của
cross-review **không nằm trong bản đã merge**; chúng còn dang dở lúc `af0d261` được lấy, và nay
sống ở PR **#581** (`c0bc5a5`). Tức lease bị thu hồi trên một tiền đề đúng-một-nửa. Không ai
làm sai: người ra chỉ thị đọc "PR đã merge" là hợp lý. Ghi ra để lần sau *"packet đã land"* được
đọc là **"nhánh đã hết việc chưa?"**, không phải *"có PR nào merge chưa?"*.

### Phép đo sinh ra r6

Bộ đo `570-do-10` (máy chủ kho, 2026-09-21, HEAD `c0bc5a5`, chốt cây ĐẠT) đóng **hai** finding
và mở lại **một**:

| | Trên Windows, bản `c0bc5a5` |
|---|---|
| **F1** độ phủ | ✅ ĐÓNG — `E_hinh_dang_PHU_bi_bo_sot: []`, `E_hinh_dang_KHONG_PHU_bi_bat_oan: []` |
| **F2** phạm vi | ✅ ĐÓNG — `pham_vi: toan-cay`, 4 tệp/11 lời gọi đều trong `chua_chuyen`, `ngoai_danh_sach` rỗng |
| **F3** cache | ❌ **CHƯA ĐÓNG** — `t34` ĐỎ, `cong_cu_test: 37/38 đạt` |

```
ĐỎ  t34_cache_tim_bash_phai_theo_doi_MOI_TRUONG:
    trước='C:\Program Files\Git\bin\bash.exe'
    đặt  ='…\Temp\tmppjuaw8uq\bash'
    nhận ='C:\Program Files\Git\bin\bash.exe'
```

Và vì `t34` đỏ **độc lập với mọi đột biến**, nó tự cộng vào bán kính của **từng** đột biến —
19 dòng `ĐỎ … bán kính 2/38`. Chúng là **hệ quả của một ca đỏ**, không phải 19 khuyết tật. Đây
là lần đầu kho đo được hình dạng ấy, và nó đáng ghi: *một ca đỏ cố định làm hỏng phép đo bán
kính của TOÀN BỘ bộ đột biến*.

### NGUYÊN NHÂN: KHÔNG ĐO ĐƯỢC — hai giả thuyết, log không phân biệt nổi

- **(a)** khoá cache vẫn nuốt môi trường trên Windows;
- **(b)** cache **đã** tính lại và có XÉT ứng viên mới, nhưng ứng viên bị **năng lực** từ chối
  nên bộ giải lùi về Git Bash — tức `tim_bash` làm đúng việc của nó.

Cả hai **dự đoán cùng một `nhận == trước`**, nên con số ấy không phân biệt được. Thứ phân biệt
được là `chan_doan` của lần gọi **thứ hai** — mà cả `t34` lẫn phép `F` của bộ đo đều **vứt nó
đi** (`sau, _ = tim_bash()`). Đúng bài học `_ket_luan_ban_kinh` đã ghi ở r4: khẳng định một kết
quả trong khi ném mất bằng chứng giải thích nó.

Có một dấu hiệu **khớp hình dạng** (b): `t34` làm `shutil.copy2(bash → tmp/'bash')`, tức một bản
sao **trơ**, mất đuôi `.exe` và không có DLL bên cạnh; trên Git for Windows, `bash.exe` cần
`msys-2.0.dll` nằm cùng thư mục. Trên Linux bản sao chạy được nên Linux xanh. **Khớp hình dạng
KHÔNG phải đã đo** — r6 không viết nó thành nguyên nhân, r6 dựng phép đo phân biệt được.

## 0. Vì sao có revision 4 — MỞ PHẠM VI CỔNG ra TOÀN CÂY

r4 không bác r3. Nó mở **phạm vi quét của cổng**, và lý do là một lượt cross-review ĐO ĐƯỢC,
không phải một ý hay.

Lượt `advisory_review` trên `05ec2eb5` (PR #571, 20-09-2026T15:56Z, `VERDICT.md`
sha256 `59eec0aa4245a0a6073799f3085dae778e4eee1dad5e32bab0a554cdd3c22ef6`) ra
`verdict: changes_requested` với ba finding. Phiên executor **đo lại cả ba** thay vì nhận lời
khai, và **cả ba tái hiện chính xác**:

| finding | reviewer khai | executor đo lại |
|---|---|---|
| F1 `_loi_goi_tran` khai "MỌI" | BẮT 3 / LỌT 9 trên 12 hình dạng | BẮT 3 / LỌT 9 |
| F2 cổng chỉ phủ `ops/**` | 11 lời gọi / 4 tệp ngoài phạm vi | 11 / 4, y hệt danh sách |
| F3 cache bỏ qua môi trường | `B != C` khi đặt `CONG_CU_BASH` sau lần gọi đầu | khoá cache `[[], false]`, B≠C |

**F2 là cái đắt nhất, và nó bác một câu của chính packet này.** PR mở đầu bằng *"một bộ giải
dùng chung + một CỔNG chặn bản sao thứ tư"*. Nhưng bản sao thứ tư **đã sống sẵn ngoài hàng
rào** trước khi cổng ra đời:

```
.claude/dev/launcher_test.py:6004
    bash = (shutil.which("bash") if not LA_WINDOWS else
            ("C:/Program Files/Git/bin/bash.exe" if Path(...).exists() else shutil.which("bash")))
```

Đó là một bộ giải RIÊNG quyết bằng **ĐƯỜNG DẪN GHI CỨNG** — đúng hình dạng vừa bị gỡ khỏi
`_bash_posix` (r2) và `_bash_windows` (r3). Và `.claude/hooks/session_start.py:58` chạy ở
**mọi phiên**.

Nên r3 §N4 khoanh cổng vào `ops/**` là một lời khai **hẹp hơn thứ packet hứa**, trong khi
docstring của cổng lại khai **rộng hơn thứ nó làm**. Hai cái sai ngược chiều nhau, gặp nhau ở
giữa thành một cổng trông như đã chặn xong.

**CHỦ KHO QUYẾT: mở phạm vi ra toàn cây** (chỉ thị 20-09-2026 ~16:0xZ, chọn "Mở phạm vi cổng ra
toàn cây" trong ba phương án đã trình: thu hẹp lời khai · mở phạm vi · để nguyên).

**KHAI THẲNG CÁI GIÁ:** ratchet sẽ **DÀI RA** thay vì ngắn đi — từ rỗng lên 4 mục. Đó là đi
ngược tinh thần "ratchet phải NGẮN đi" của N5/N13. Chấp nhận có điều kiện: mỗi mục phải mang
**NGÀY GỠ** và lý do đo được, và N13 được viết lại cho đúng (xem §5). Một danh sách dài ra mà
không có ngày gỡ thì đúng là nghĩa trang mà N5 sinh ra để chặn.

## 0. Vì sao có revision 3 — MỞ WRITE SET sang `ops/cong_cu.py`

r3 KHÔNG bác r2. Nó mở đúng một đường, vì hai điều kiện đã đổi và cả hai đo được.

**(a) Lý do loại trừ của r2 đã hết hiệu lực.** r2 §4 viết: *"`ops/cong_cu.py` — hợp nhất
`_bash_windows` vào `ops/bash_nen.py` là việc ĐÚNG nhưng lease `wp541-path-r3-g3-claude` khai
nó trong `khong_duoc_cham`"*. Lease ấy **đã bị thu hồi** bằng bia mộ hai chiều (lease kế nhiệm
`wp541-path-r4-g4-bia-mo`). Đo 20-09-2026T05:05Z, đọc `rc` TRỰC TIẾP:

```
ai-dang-giu ops/cong_cu.py   rc=0   NGƯỜI_GIỮ 0: không có
```

Tức rào chắn không còn là "có người khác giữ" mà chỉ còn là write set của chính packet này —
thứ sửa được bằng revision. Đây là lý do DUY NHẤT r2 nêu để loại `ops/cong_cu.py`.

**(b) Phép đo Windows lượt 5 cho một lý do THUẬN mà r2 chưa có.** Bộ đo `570-do-5`
(`DO-570-LUOT5.ps1`, `sha256 01a2bc92e69aa735212490f5b5d35dc73b6c9a1ca9936939d88f2e7a1e97a6cc`,
`HEAD 4fc3ca8f`): đột biến `t22_bash_lay_ca_system_root` cho bán kính **không đọc được** trên
Windows, và **hai lượt cho hai kết quả KHÁC NHAU**:

| lượt | HEAD | bán kính | ca oan | phân hạng |
|---|---|---|---|---|
| `570-do-3` | `42dd49db` | 9/31 | `t3 t4 t7 t8 t9 t11 t21 t24` | tất cả `giet_that` |
| `570-do-5` | `4fc3ca8f` | 2/32 | `t2` | `tin_dung_gia` |

Cùng đột biến, cùng máy, cách ~2,5 giờ, và `_bash_windows` / `_chay` / tám ca kia KHÔNG đổi giữa
hai commit. **Nguyên nhân của chênh lệch ấy đứng ở `KHÔNG ĐO ĐƯỢC`** — cấm dựng giả thuyết cho
nó, y như hai chỗ chưa khép ở §6.

Nhưng thứ ĐO ĐƯỢC đủ để ra quyết định: `t22` tồn tại **chỉ để canh một bộ lọc theo TÊN**
(`%SystemRoot%`) trong bộ giải RIÊNG thứ hai. Đó đúng hình dạng *"danh sách CẤM không bao giờ
đủ"* mà §2 đã nêu, và là bộ giải cuối cùng còn sót. Hợp nhất nó vào `tim_bash()` làm bộ lọc theo
tên biến mất, `t22` mất đối tượng, và cả lớp bất ổn này chết **theo KIẾN TRÚC** chứ không theo
bản vá — đúng cách kho đã thoát khỏi "bảy phát hiện cùng một đường".

**KHAI THẲNG MỘT CÁI GIÁ.** Hợp nhất bây giờ thì mất phép so trước/sau cho câu hỏi ở (b).
Phiên này đã nêu cái giá ấy và chủ kho quyết vẫn làm (chỉ thị *"Cấp lease r3/g3 đi, rồi chuyển
cong_cu.py"*). Ghi ra đây để không ai đọc ngược rằng câu hỏi ấy đã được trả lời — nó **bị bỏ
lại**, không bị giải.

**(c) r2 có một lời khai nay đã cũ.** r2 §6 ghi hợp nhất `_bash_windows` là *"ngoài phạm vi"*.
r3 đưa nó VÀO phạm vi. Không xoá câu cũ ở §6 mà đánh dấu — một đặc tả sửa lặng lẽ lời khai cũ
là thứ khó kiểm nhất.

## 0. Vì sao có revision 2 — r1 SAI ở ba chỗ, và phép đo là thứ chỉ ra

r1 không bị bác về hướng. Nó sai ở ba câu, và cả ba chỉ lộ ra sau khi lượt đo Windows
`570-do-3` chạy thật (`DO-570-LUOT3.ps1`, `sha256 99380e45ee03f361a18c040686c78ad1bced2cd4787f4099c81ba862829666ad`,
log 20-09-2026T01:49 giờ máy).

**(a) Điều kiện bắt đầu KHÔNG BAO GIỜ THOẢ ĐƯỢC.** r1 §7 và `DIEU_KIEN_BAT_DAU` của lease g1
viết *"cho tới khi `ai-dang-giu` trả `rc=0` / `NGƯỜI_GIỮ 0`"*. Nhưng lease của CHÍNH packet này
giữ `ops/lease_publish_test.py`, nên `NGƯỜI_GIỮ` không bao giờ về 0 trong khi lease còn sống.
Ý định là *"không còn người giữ NÀO KHÁC"*. Câu viết quá rộng, và một điều kiện không thoả được
sẽ bị người sau lặng lẽ diễn giải lại — đó là cách một chốt chết mà vẫn trông như còn sống.

**(b) N9 KHÔNG ĐO ĐƯỢC bằng công cụ đang có.** r1 đòi log Windows cho thấy
`C:\Windows\system32\bash.EXE` *"đã được THỬ rồi bị TỪ CHỐI vì phép argv"*. Đo được: `tim_bash`
DỪNG ở ứng viên đầu tiên đạt, mà Git Bash trên PATH đạt trước, nên System32 **chưa từng được thử**
và chẩn đoán chỉ có một dòng. Tiêu chí đòi một thứ mà CLI không sinh ra được.

**(c) Năm ca nghiệm thu nằm trong một tệp KHÔNG CHẠY NỔI trên nền cần đo.** Đo được:
`ops/cong_cu_test.py::_chay_batch` gọi `subprocess.run([bash, "./cai_cong_cu.sh", "--bat-buoc"])`
với `bash` lấy bằng `shutil.which("bash")` ⇒ `C:\Windows\system32\bash.EXE` ⇒ **TREO**, hết hạn
60s, rồi `TemporaryDirectory` chết tiếp bằng `WinError 32` / `WinError 5`. Cả suite chết trong
`batch_behavior_test()` — TRƯỚC vòng lặp ca của `main()`. Nên `T23`–`T27` **chưa từng chạy trên
Windows**, dù chúng sinh ra để đo Windows. Đúng bệnh *"ca có MẶT khác ca có ĐO"*.

Và (c) phơi ra một **dạng hỏng THỨ BA của cùng bộ phóng WSL**, chưa từng được đo ở lượt 1 hay 2:
không chỉ `rc=127` và nuốt argv, mà **TREO**. Phép năng lực của `ops/bash_nen.py` có hạn 30s nên
nó vẫn bắt được — nhưng đó là MAY, không phải thiết kế: chưa có ca nào canh mặt ấy.

## 1. Vì sao có packet này — ĐÃ ĐO, không phải giả thuyết

Sáu ca `t35`–`t40` của `ops/lease_publish_test.py` ĐỎ trên Windows thật với `rc=127`. Issue #570
nêu giả thuyết *"script chưa từng chạy"* và yêu cầu **ĐO**, cấm xác nhận bằng suy luận.

Đã đo, 19-09-2026, `Windows-11-10.0.26200`, `python 3.13.1`, máy chủ kho. Bộ đo `DO-570.ps1`
(`sha256 f7d235ab2375c6d88bdd40a8eb4c94a9fde9884e4cb5208686ebb4f4c273f396`, bản `570-do-1`) và
`DO-570-LUOT2.ps1` (`sha256 233ea1b14f4aaac627fea0c2c1f684819abf0f4f212aa56b4d2642319abb11b8`,
bản `570-do-2`). Đính chính đã đăng: #570#issuecomment-5743594728.

**Phán quyết:** `a_GIAN_HONG_SCRIPT_LANH`, ra giống nhau trên CẢ HAI hình dạng đường dẫn.

- `shutil.which("bash")` trên máy ấy trả `C:\Windows\system32\bash.EXE` — **bộ phóng WSL**.
  Tự khai: `ARGV0=/bin/bash`, `UNAME=…microsoft-standard-WSL2`, `CYGPATH=KHONG_CO`.
- Đưa nó đường dẫn Windows ⇒ `rc=127` + `No such file or directory`, trùng từng chữ với log #570.
- Truyền đối số vị trí qua `-c` ⇒ **đối số không tới nơi**: `$0=/bin/bash`, `$#=0`; với một
  script 6 dòng, lỗi hiện ở **dòng 7** nội dung `t40` — đối số bị nối vào THÂN SCRIPT rồi chạy
  như một lệnh. Từ đó `$1`/`$2`/`$3` rỗng nên `exec "$3"` chết `exec: : not found`.
- `ops/cai_actionlint.sh` **LÀNH**: trên `C:\Program Files\Git\bin\bash.exe`, cùng máy, cùng các
  đường dẫn ấy, **26/26** khẳng định của sáu ca ĐẠT, và **6/6** đột biến bị giết ĐÚNG LÝ DO.
- **KHÔNG phải nguyên nhân: dạng đường dẫn.** Git Bash nhận đúng chuỗi `str(Path)` có dấu, có
  khoảng trắng, có dấu chéo ngược. Hai lượt đổi đúng một biến (`D:\Quốc hội\…` so với
  `C:\…\Temp\…` ASCII) cho kết quả y hệt. Cấm vá bằng cách `cygpath` hoá đường dẫn.

## 2. Hình dạng kế thừa — LẦN THỨ BA, nên không vá theo kiểu cũ

| lần | nơi | neo |
|---|---|---|
| 1 | `_bash_posix()` trong `ops/lease_publish_test.py` | `master e03c6d28`, run `32351777642` |
| 2 | `_bash_windows()` trong `ops/cong_cu.py` | run `33612364175`, 02-09-2026 |
| 3 | `t35`–`t40` gọi `shutil.which("bash")` trần | #570, 19-09-2026 |

`CLAUDE.md`: hình dạng lặp lần thứ ba thì câu hỏi đúng là *"có nên làm việc này không"*. Chủ kho
đã quyết: **MỘT bộ giải dùng chung + một CỔNG làm ĐỎ mọi lời gọi trần mới**. Bản vá thứ tư theo
kiểu cũ (thêm bộ giải riêng thứ ba) bị TỪ CHỐI có chủ đích.

Ràng buộc thiết kế kèm theo, có bằng chứng: hai bộ giải cũ lọc theo TÊN (`"system32"`,
`%SystemRoot%`) — đúng hình dạng *"danh sách CẤM không bao giờ đủ"*. Phép đo lượt 2 cho thấy
**không lọc theo tên nào diễn tả nổi "con bash này làm hỏng argv"**. Nên bộ giải phải quyết bằng
**phép thử NĂNG LỰC**.

## 3. Objective

Sáu ca `t35`–`t40` đo được ĐÚNG điều tên chúng nói, trên Windows thật; và khuyết tật
"phân giải `bash` theo TÊN rồi coi hit đầu tiên là dùng được" không thể tái sinh lặng lẽ trong
`ops/**`.

## 4. Write set

```yaml
write_set:
  - type: exact
    path: ops/bash_nen.py
  - type: exact
    path: ops/cong_cu.py          # THÊM ở r3 — xem §0(a)
  - type: exact
    path: ops/cong_cu_test.py
  - type: exact
    path: ops/lease_publish_test.py
```

**KHAI THẲNG — công việc TRƯỚC LEASE.** `ops/bash_nen.py` và `ops/cong_cu_test.py` ĐÃ được thay
đổi ở PR #571 (`010fb281f52b27364e4e3e3515d125b084f9d20e`) theo chỉ thị *"Vá đi"* của chủ kho,
lúc packet này CHƯA có lease. Lease r1 bao trùm chúng về sau; nó KHÔNG hợp thức hoá ngược việc
đã làm, chỉ ghi nhận đúng sự thật để không ai đọc nhầm rằng phần ấy đã qua cổng lease.

~~Hai đường KHÔNG vào write set~~ — **r3 rút xuống còn MỘT**:
- ~~`ops/cong_cu.py` — … lease `wp541-path-r3-g3-claude` khai nó trong `khong_duoc_cham`~~
  **HẾT HIỆU LỰC ở r3.** Lease ấy đã bị thu hồi; `ai-dang-giu ops/cong_cu.py` ⇒ `rc=0`,
  `NGƯỜI_GIỮ 0`. Nay nằm TRONG write set (§0(a), N14).
- `ops/cai_actionlint.sh` — đã đo là LÀNH; không có gì để sửa. **Vẫn ngoài write set.**

## 5. Tiêu chí nghiệm thu

Mỗi tiêu chí NEO LÝ DO, không chỉ neo `rc`. Ca nào không phân biệt được bằng đầu vào thì khai
thẳng là bộ TƯƠNG ĐƯƠNG, không giả vờ có nhiều chốt.

- **N1 — bộ giải quyết bằng NĂNG LỰC.** `ops/bash_nen.py::_do_nang_luc` chạy hai phép thật:
  (1) trung thực argv — `-c <script> <nhãn> A1 A2 A3` phải cho `$0 == nhãn`, `$# == 3`,
  `$1 == A1`; (2) mở được đường dẫn bản địa — chạy được script truyền bằng `str(Path)`.
  Thiếu một trong hai ⇒ TỪ CHỐI. Không ứng viên nào đạt ⇒ `None`, người gọi fail-close.
- **N2 — ba chốt con của phép argv có răng RIÊNG.** Ba `bash` giả, mỗi con hỏng đúng một chốt
  (`$0`, `$#`, `$1`); ba đột biến, mỗi đột biến gỡ đúng một chốt, cả ba phải làm ca đích ĐỎ.
  (Sinh ra vì đột biến đầu tiên SỐNG SÓT — nó chỉ gỡ một trong ba chốt.)
- **N3 — hai phép KHÔNG suy ra nhau.** Con giả "nuốt argv" vẫn mở được tệp; con giả "không mở
  được tệp" truyền đúng argv. Mỗi con chỉ bị đúng một phép bắt.
- **N4 — cổng chặn bản sao thứ tư.** `ops/**` có lời gọi `bash` trần ngoài danh sách cho phép
  ⇒ ĐỎ. Đột biến nới danh sách phải làm ca đích ĐỎ.
- **N5 — ratchet HAI CHIỀU.** Mục trong `CHUA_CHUYEN` mà đã SẠCH cũng làm cổng ĐỎ. Đột biến bỏ
  chiều ngược phải làm ca đích ĐỎ.
- **N6 — cổng đo CẤU TRÚC, không đo chuỗi.** Tệp chỉ NHẮC TỚI lời gọi trần trong chú thích,
  docstring hay một chuỗi hằng KHÔNG được làm cổng ĐỎ. Đột biến đổi sang khớp chuỗi thô phải làm
  ca đích ĐỎ. (Sinh ra vì bản đầu của cổng đếm luôn hai lần nhắc trong chính docstring của nó —
  đúng bệnh `t43` đã ĐỎ oan.)
- **N7 — sáu ca dùng bộ giải chung.** `t35`–`t40` lấy `bash` qua `ops/bash_nen.py`, không gọi
  `shutil.which("bash")` trần. Sau đó `ops/lease_publish_test.py` phải RỜI khỏi `CHUA_CHUYEN`,
  và N5 là thứ bắt việc quên xoá.
- **N8 — thiếu bash dùng được thì ĐỎ, không bỏ qua.** Sáu ca phải fail-close với thông điệp nêu
  chẩn đoán (ứng viên nào bị từ chối vì lý do gì), KHÔNG được `return` sớm rồi được đếm là ĐẠT —
  bệnh `t24` kho đã ghi sổ.
- **N9 — nghiệm thu trên WINDOWS THẬT.** ADR-0049: cổng hai nền là CỔNG TẠI CHỖ, không phải lane
  `master`. Nên N1–N8 phải có một lượt đo trên máy chủ kho, và log phải TỰ KHAI `sha256` bộ đo,
  `HEAD` đã đo, và REF nào trỏ tới `HEAD` ấy. Hai điều kiện, vì r1 đòi một thứ không sinh ra được:
  · `ops/bash_nen.py` phải có đường chẩn đoán thử **MỌI** ứng viên (không dừng ở cái đầu tiên đạt),
    và log phải cho thấy `C:\Windows\system32\bash.EXE` **đã được THỬ rồi bị TỪ CHỐI vì phép
    argv** — chọn đúng thôi chưa đủ, phải từ chối ĐÚNG LÝ DO;
  · lượt ấy phải CHẠY ĐƯỢC `T23`–`T27` trên Windows, tức N12 phải xong trước. Một lượt chết ở
    `batch_behavior_test()` là **KHÔNG ĐO ĐƯỢC**, KHÔNG phải "đạt".
- **N10 — delta nền = 0.** Mọi cổng chạy lại trên `origin/master` sạch để so DELTA. Đỏ sẵn thì
  khai "đỏ sẵn, delta = 0", không vá lung tung.
- **N11 — mặt TREO phải có răng.** Một `bash` giả KHÔNG BAO GIỜ trả phải bị `_do_nang_luc` TỪ
  CHỐI trong hạn, và đột biến bỏ/nới hạn phải làm ca đích ĐỎ. Hôm nay hạn 30s chặn được mặt ấy
  nhưng KHÔNG ca nào canh — tức nó đang đúng do may. (Sinh từ phép đo `570-do-3`: WSL bash làm
  `./cai_cong_cu.sh` treo tới 60s thay vì `rc=127`.)
- **N12 — `ops/cong_cu_test.py` phải chạy được trên Windows.** Ba lời gọi `bash` trần của nó phải
  đi qua `tim_bash()`, và suite phải tới được vòng lặp ca trên Windows. Không có N12 thì N9 vô
  nghĩa: năm ca nghiệm thu nằm trong chính tệp không khởi động nổi.
- **N14 — `ops/cong_cu.py` dùng bộ giải chung, và `CHUA_CHUYEN` về RỖNG.** `_bash_windows()`
  uỷ quyền cho `ops/bash_nen.py::tim_bash()`; không còn bộ lọc theo TÊN nào RA QUYẾT ĐỊNH trong
  `ops/**`. Sau đó `ops/cong_cu.py` phải RỜI `CHUA_CHUYEN`, và vì nó là mục cuối cùng, danh sách
  ấy phải RỖNG. N5 (ratchet hai chiều) là thứ bắt việc quên xoá — tức N14 đo được bằng chính
  cổng, không bằng mắt.
- **N15 — `t22` phải ĐO THỨ MỚI, không được giữ lại làm cảnh.** Ca `t22` hôm nay khẳng định
  `_bash_windows` LOẠI ứng viên dưới `%SystemRoot%` theo ĐƯỜNG DẪN. Sau N14 mệnh đề ấy không còn
  đúng theo nghĩa cũ: thứ loại bộ phóng WSL là PHÉP NĂNG LỰC. Nên `t22` phải được viết lại để đo
  hành vi MỚI, và phải có đột biến riêng làm nó ĐỎ. **Giữ nguyên `t22` cũ là cấm** — một ca còn
  MẶT mà không còn ĐO là đúng bệnh `t24` kho đã ghi sổ.
- **N16 — báo cáo bán kính nêu LÝ DO ở MỌI nhánh ĐỎ.** Không nhánh nào được chỉ in TÊN ca oan.
  Mỗi nhánh (`oan`, `gia`) phải có đột biến RIÊNG làm ca đích ĐỎ, phân biệt được bằng ĐẦU VÀO —
  nếu không phân biệt được thì khai thẳng là bộ TƯƠNG ĐƯƠNG. (Sinh ra vì bản vá sáng 20-09 chỉ
  gắn lý do vào nhánh `oan`, rồi lượt đo `570-do-5` rơi vào nhánh `gia` và lại không đọc được gì
  — *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"*.)
- **N17 — cổng quét TOÀN CÂY, không chỉ `ops/**`.** `quet()` đi hết cây kho (trừ `.git/` và
  `ops/reviews/` — ảnh chụp đông cứng). Bốn tệp đo được ở §0 nạp vào `CHUA_CHUYEN`, MỖI MỤC
  kèm **ngày gỡ** và lý do. Đột biến thu phạm vi về `ops/**` phải làm ca đích ĐỎ — nếu không
  thì không ai biết cổng đang phủ tới đâu.
- **N18 — độ phủ của `_loi_goi_tran` phải ĐO ĐƯỢC THEO HÌNH DẠNG.** Một bảng hình dạng lời gọi
  (ít nhất: `which` chuỗi · `which` keyword · `which("bash.exe")` · `run`/`Popen` list ·
  `run(args=)`), mỗi hình dạng một khẳng định. Và **docstring phải khai ĐÚNG phạm vi** — cấm
  chữ "MỌI" khi phép đo chỉ phủ một tập. (Sinh từ F1: hàm khai "mọi lời gọi phân giải `bash`
  theo TÊN", đo được 3/12. Đáng kể nhất là `which("bash.exe")` — đúng cách viết Windows của
  đúng khuyết tật Windows mà packet này sinh ra để chặn.)
- **N19 — cache của `tim_bash` phải theo dõi MÔI TRƯỜNG, hoặc khai thẳng là không.** `ung_vien`
  đọc `CONG_CU_BASH`/`PATH`/`SystemRoot`/`ProgramFiles` từ `os.environ` khi tham số là `None`,
  nên khoá cache phải gồm chúng. Phản chứng hai chiều: đặt `CONG_CU_BASH` SAU lần gọi đầu thì
  lần gọi sau phải thấy. (Sinh từ F3. Hôm nay chưa cắn ca nào vì bộ test tiêm qua `env=` của
  tiến trình con, nhưng đó là bẫy nằm chờ.)
- **N23 — DANH SÁCH TỆP LÀ INDEX, KHÔNG HƠN. SINH TỪ r9.**
  `_liet_ke_py` chạy đúng `git ls-files --cached -z -- '*.py'`: **không cờ exclude nào**,
  không `--others`, không kho tạm. `nguon_tep` giữ ba trạng thái, nghĩa đọc lại:
  `git` = danh sách từ INDEX · `rglob` = cây KHÔNG phải kho git (bộ ca dựng cây giả) ·
  `git-hong: …` = có `.git` mà lệnh git hỏng. **SỬA Ở r10 (N26):** trạng thái thứ ba trước đây
  trả một danh sách `rglob` kèm nhãn `rglob-git-hong`; nay nó **không trả danh sách nào** và
  `quet()` biến nó thành `KHONG_DO_DUOC`. Xem N26.
  Chốt: **không luật ignore nào đổi được danh sách** — `.gitignore` chưa/đã theo dõi,
  `.git/info/exclude`, `core.excludesFile` cục bộ, `GIT_CONFIG_GLOBAL`,
  `$XDG_CONFIG_HOME/git/ignore` — sáu mặt, danh sách y hệt nền. Và một tệp `add -f` khớp
  `.gitignore` đã commit **vẫn phải có mặt**. Đột biến nghe lại luật ignore phải làm ca đích ĐỎ.
  ĐÁNH ĐỔI: tệp chưa `add` KHÔNG được quét — `t37` chốt cả hai chiều và docstring gọi thẳng
  đó là quyết định của chủ kho, không phải tính chất tự nhiên.
- **N39 — RÀNG BUỘC `global`/`nonlocal` ĐƯỢC CHÉP, KHÔNG DỜI. SINH TỪ r15.**
  Phạm vi khai `global x` mà TỰ NÓ ràng buộc `x` thì trong phạm vi ấy dùng ràng buộc ấy; khai
  ĐỌC KHÔNG thì về bảng module. Bảng module nhận thêm bản chép, nên ngoài module vẫn mơ hồ.
  **Hai chiều:** `global x; import x` ⇒ BẮT trong thân · `global x; x = gia()` ⇒ KHÔNG bắt.
- **N40 — `:=` TRONG TRƯỜNG LÚC ĐỊNH NGHĨA RÀNG BUỘC Ở PHẠM VI CHỨA. SINH TỪ r15.**
  Decorator, giá trị mặc định, chú thích, cơ sở lớp — vì chính chúng được TÍNH ở phạm vi chứa
  (N37). **KHÔNG** xuống thân: `:=` trong thân là của thân. **Hai chiều** phải có ca.
- **N41 — THAM SỐ KIỂU PEP 695 PHẢI ĐƯỢC THĂM VÀ PHẢI CHE ĐƯỢC. SINH TỪ r15.**
  `type_params` vào danh sách nút tính ở phạm vi ngoài; tên `TypeVar`/`ParamSpec`/`TypeVarTuple`
  ràng buộc trong phạm vi con. Lời gọi ở `bound` mà không được thăm thì bảng tra thiếu mục và
  đó là **`KeyError`** — sập, không phải bỏ sót. Ca đích phải tự khai khi nền không đo được.
- **N42 — LỖI GIẢI MÃ LÀ `KHONG_DO_DUOC`, KHÔNG PHẢI TRACEBACK. SINH TỪ r15.**
  `SyntaxError`/`LookupError`/`ValueError` quanh `_doc_noi_dung` ⇒ `rc=3` kèm báo cáo JSON.
  **BẮT HẸP** — chỉ quanh lời gọi ấy — để một lỗi hiện thực khác không bị biến thành "phép đo
  thất bại".
- **N43 — BIÊN GIỚI BÁO CÁO PHẢI RA JSON HỢP LỆ. SINH TỪ r15.**
  Đường nội bộ giữ byte (`surrogateescape`, N36); đường ĐI RA báo cáo đổi surrogate thành
  `\\xNN`. **Chiều ngược:** đường Unicode thường phải nguyên vẹn.
- **N44 — NGÀY GỠ PHẢI ĐƯỢC ĐỌC, KHÔNG PHẢI MỘT CHỮ TRONG LÝ DO. SINH TỪ r15.**
  `quet()` so ngày **UTC** với `_NGAY_GO`; quá hạn ⇒ ĐỎ, nêu tên mục. `hom_nay` tiêm được cho
  ca đo. **Hai chiều:** ĐÚNG ngày gỡ vẫn phải qua.
- **N36 — KHUNG `ls-files -z` TÁCH TRÊN BYTES, GIẢI MÃ SAU. SINH TỪ r13.**
  Không `text=True`. Tách `\0` rồi `\t` trên **bytes**, rồi mới giải mã đường bằng
  `surrogateescape`. Dịch dòng phổ quát chạy trước khi tách khung làm hai đường khác nhau gộp
  làm một và một blob ghi đè blob kia **im lặng**.
- **N37 — BIỂU THỨC LÚC ĐỊNH NGHĨA TÍNH Ở PHẠM VI NGOÀI. SINH TỪ r13.**
  Decorator, giá trị mặc định, chú thích, cơ sở lớp và `iter` **đầu tiên** của comprehension
  giải ở phạm vi **CHỨA**; chỉ **THÂN** ở phạm vi mới. Một đường duyệt **duy nhất** xử lý nút
  phạm vi, kẻo hàm lồng trong hàm mất một tầng.
- **N38 — ĐÔNG CỨNG PHẢI GHIM BLOB, KHÔNG CHỈ ĐẾM SỐ. SINH TỪ r13.**
  Mục `ANH_CHUP_DONG_CUNG` mang `(số_lần, OID_blob, lý_do)`; OID lệch ⇒ **ĐỎ**, dù số khớp.
  Báo cáo mang `lech_oid_dong_cung`. **Chiều ngược** phải có ca: ảnh chụp NGUYÊN BẢN cho
  `lech_oid` RỖNG.
- **N32 — REF THAY THẾ CỦA MÁY KHÔNG ĐƯỢC ĐỔI BYTES CỔNG ĐỌC. SINH TỪ r12.**
  Mọi tiến trình `git` con đi qua **một** hàm `_chay_git`, mang `--no-replace-objects` **và**
  `GIT_NO_REPLACE_OBJECTS=1`. Hai hàng rào phải ở CÙNG một chỗ: tách ra hai nơi thì không đột
  biến nào đo được cái nào.
- **N33 — INDEX CHƯA HOÀ GIẢI ⇒ KHÔNG ĐO ĐƯỢC, NÊU TÊN. SINH TỪ r12.**
  Bản ghi mang **cả ba** trường `(đường, chế_độ, sha)` cộng **stage**; chỉ stage `0` được nhận.
  Còn stage 1/2/3 ⇒ `KHONG_DO_DUOC` nêu tên đường. Chọn bừa một stage là tự bịa ra một cây
  chưa từng tồn tại.
- **N34 — GIẢI MÃ NGUỒN THEO KHAI BÁO CỦA CHÍNH TỆP. SINH TỪ r12.**
  `tokenize.detect_encoding` trên blob thô (PEP 263 + BOM), cho **cả** đường git lẫn đường
  `rglob`. Fail-close đúng chỗ là khi KHÔNG ĐO ĐƯỢC; một tệp Python hợp lệ mà làm cổng chặn cả
  kho là đọc sai cách, không phải không đo được. **Chiều ngược** phải có ca: tệp BOM **mang**
  lời gọi trần vẫn phải bị bắt.
- **N35 — HẬU TỐ NGUỒN PYTHON SO KHÔNG PHÂN BIỆT HOA/THƯỜNG, GỒM `.pyw`. SINH TỪ r12.**
  Một hàm `_la_nguon_py` dùng `casefold()`; **không** dùng pathspec `*.py` của git. **Chiều
  ngược** phải có ca: `.txt` mang lời gọi trần vẫn KHÔNG được quét.
- **N28 — DANH SÁCH *VÀ* NỘI DUNG ĐỀU TỪ INDEX; MÔI TRƯỜNG GIT PHẢI SẠCH. SINH TỪ r11.**
  Nội dung lấy bằng `git cat-file --batch` trên blob đã stage, không `read_text()` trên cây làm
  việc. Mục mode `120000` (symlink) ⇒ **`KHONG_DO_DUOC` nêu tên**, không im lặng bỏ qua. Mọi
  tiến trình git con chạy với môi trường đã gỡ `GIT_DIR`, `GIT_INDEX_FILE`, `GIT_WORK_TREE`,
  `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`,
  `GIT_CEILING_DIRECTORIES`, `GIT_DISCOVERY_ACROSS_FILESYSTEM`, `GIT_NAMESPACE`,
  `GIT_INDEX_VERSION`, `GIT_CONFIG*`, `GIT_CONFIG_KEY_n`, `GIT_CONFIG_VALUE_n`. Báo cáo mang
  `nguon_noi_dung` và `bien_git_da_go` — đọc được, không phải tin lời.
  **Ba chiều** phải có ca: sửa trên đĩa sau `git add` KHÔNG đổi phán quyết · `GIT_INDEX_FILE`
  KHÔNG đổi danh sách · symlink ⇒ `KHONG_DO_DUOC` nêu tên.
- **N29 — GIẢI TÊN PHẢI TÔN TRỌNG `global`/`nonlocal` VÀ WALRUS TRONG COMPREHENSION. SINH TỪ r11.**
  Ràng buộc khai `global`/`nonlocal` thuộc phạm vi **SỞ HỮU**, không phải phạm vi cú pháp chứa
  nó; khai **đọc không** (không gán gì trong thân) KHÔNG chuyển gì. `:=` trong comprehension
  ràng buộc ở phạm vi **CHỨA** comprehension (PEP 572). Hai chiều: LỌT và OAN đều phải có ca.
- **N30 — HẰNG CHƯƠNG TRÌNH SO THEO MỌI KIỂU BIỂU DIỄN. SINH TỪ r11.**
  `str` và `bytes` ASCII, không phân biệt hoa/thường. Byte ngoài ASCII KHÔNG giải mã bừa.
  Cùng lớp với mặt hoa/thường ở r7: *một bảng hằng chỉ phủ một cách viết là một đường vòng*.
- **N31 — CỔNG PHẢI ĐƯỢC NỐI VÀO ĐIỂM VÀO MÀ CI GỌI. SINH TỪ r11 (P1).**
  `ops/cong_cu_test.py` — chính lệnh CI chạy — phải chạy `quet` trên cây **THẬT** đúng MỘT lần,
  **TRƯỚC** bộ đột biến (đột biến dựng cây SAO và tráo `BASH_NEN`), và kéo mã thoát khác 0 khi
  cổng `DO` **hoặc** `KHONG_DO_DUOC` — hai nhãn riêng, không gộp. **Hai chiều** phải có ca: cây
  sạch ⇒ qua; cây có lời gọi trần đã `git add` ⇒ hỏng **và nêu tên tệp**.
- **N26 — KHÔNG LẤY ĐƯỢC INDEX ⇒ KHÔNG ĐO ĐƯỢC, KHÔNG LÙI. SINH TỪ r10.**
  Cây có `.git` mà `git ls-files` hết giờ / trả rc khác 0 / không sinh được tiến trình ⇒
  `_liet_ke_py` trả `([], "git-hong: <lý do đo được>")` và `quet()` trả **`RC_KHONG_DO_DUOC`**
  kèm `nguon_tep` khai VÌ SAO. **Cấm lùi về `rglob`**: danh sách rộng hơn thì phán quyết lại
  phụ thuộc trạng thái LOCAL của máy — đúng lớp r9 giết bằng kiến trúc, sống qua cửa sau.
  Đo được trước vá trên `e290f99`: cây `.git` giả ⇒ `rc=2 DO`, `ngoai_danh_sach=['rac…py']`.
  **HAI CHIỀU:** cây KHÔNG có `.git` vẫn `rglob` và vẫn phán quyết được — thiếu chiều này thì
  đột biến *"lúc nào cũng KHÔNG_ĐO_ĐƯỢC"* sống. Ca đích chốt trên `rc == 3`, nên nó KHÔNG thuộc
  `CA_PHAN_QUYET` (N22 chỉ phủ `rc == 2` / `trang_thai == "DO"`).
- **N27 — RÀNG BUỘC IMPORT PHÂN LOẠI THEO CÁC TRƯỜNG CỦA NÚT, KHÔNG THEO MỖI CÁI TÊN. SINH TỪ r10.**
  `ImportFrom` chỉ là stdlib khi **`level == 0`**; `from .subprocess import run` là module CÙNG
  GÓI. `Import` tên CÓ CHẤM và KHÔNG `as` (`import subprocess.x`) **ràng buộc** tên `subprocess`
  vào chính module stdlib ấy — luật Python, không phải suy diễn. `import subprocess.x as y`
  KHÔNG ràng buộc `subprocess`. Bảng hình dạng của N18 phải mang **cả ba chiều**: một hình dạng
  PHỦ mới, hai hình dạng KHÔNG PHỦ mới, và `from . import subprocess` giữ lại làm chiều thứ ba
  để một bản vá cho `level` không âm thầm làm hỏng nó.
  **KHÔNG PHỦ, nợ có tên (không đổi):** `from subprocess import *` — `*` đòi biết module xuất ra
  những gì, tức phải NẠP nó, chứ không phải đọc cây cú pháp. Cùng hàng `shell=True`.
- **N24 — MỘT ca ĐỎ Ở NỀN không được đầu độc phép đo bán kính của TOÀN BỘ bộ đột biến. SINH TỪ r9.**
  Nghiệm thu Windows `570-do-14` đo được: `t38` đỏ ở nền ⇒ **45/46 đột biến** in
  `giết THÊM ['t38_…']`, `lỗi đột biến=45`. Cả 45 dòng là hệ quả của **MỘT** ca; người đọc phải
  lội hết mới thấy điều duy nhất có thật. Đây là **lần thứ HAI** (lần đầu `570-do-10` với `t34`,
  spec r6 §0) — lặp lần thứ hai thì chữa bằng cơ chế.
  Phải: chạy bộ ca trên NỀN trước; ca đỏ ở nền bị **loại khỏi cả tử số lẫn mẫu số** của bán
  kính; báo **một lần** kèm tên; đích đỏ ở nền ⇒ **KHÔNG ĐO ĐƯỢC**, không phải "giết đúng";
  và **vẫn kéo mã thoát khác 0** — KHÔNG ĐO ĐƯỢC không được lặng lẽ thành xanh.
- **N25 — ca đo phải chốt TIỀN ĐỀ trước khi chốt kết luận. SINH TỪ r9.**
  `t38` bản cũ kết luận *"khoá cache không gồm `cwd`"* trong khi log Windows cho thấy `cwd=a`
  đã trả **Git Bash**, tức bản ghi đè chưa bao giờ được chọn — **một nguyên nhân chưa đo**.
  Phải: chốt tiền đề (`normcase(abspath(t1))` == bản ghi đè, tính NGAY trong tiến trình con khi
  cwd còn ở `a/`, vì tên ứng viên là TƯƠNG ĐỐI); không đạt ⇒ KHÔNG ĐO ĐƯỢC kèm `chan_doan`
  **đo được**, không phải suy đoán. Đạt rồi mới chốt kết luận.
  GIỚI HẠN CÓ TÊN: phép so chứng minh bộ giải đã CHỌN tên trỏ vào `a/`, **không** chứng minh
  tệp ấy đã chạy — đo được: bản sao `chmod 644` cộng `/usr/bin` trên PATH thì `execvp` giải tên
  tương đối sang `/usr/bin/bash`. Với `PATH='.'` hai câu trùng nhau; đó là lý do PATH phải là `.`.
- **N22 — KHÔNG ca nào ngoài CA PHÁN QUYẾT được trói PHÁN QUYẾT của cổng. SINH TỪ r7, NỚI Ở r14.**
  Một ca tự kiểm quét **`ast`** toàn bộ `ops/cong_cu_test.py`: trong thân mỗi hàm ca **có gọi
  `_quet(...)`**, nếu đối số ĐIỀU KIỆN của một `bang(...)`/`dung(...)` chạm tới `rc` hoặc tới
  một **TRƯỜNG TỔNG HỢP** (`trang_thai`, `ngoai_danh_sach`, `ly_do`) — **mọi toán tử, mọi giá
  trị** — thì hàm ấy **phải** nằm trong `CA_PHAN_QUYET` khai tường minh **kèm lý do**.
  **TRƯỜNG CƠ CHẾ** (`co_loi_goi_tran`, `lech_so_loi_goi`, `lech_oid_dong_cung`, `nguon_tep`,
  `nguon_noi_dung`, `bien_git_da_go`, `lien_ket_tuong_trung`, `muc_ratchet_da_sach`,
  `so_cho_phep`) thì **tự do** — mỗi trường một luật, nên bán kính đột biến còn đọc được.
  **HAI CHIỀU:** một tên trong `CA_PHAN_QUYET` mà **không còn** chốt phán quyết nào cũng ĐỎ.
  **CHỐNG NỚI QUÁ:** phải có ca giữ chiều ngược — thêm TRƯỜNG CƠ CHẾ vào danh sách tổng hợp
  làm luật bắt oan, và một luật bắt oan là luật sẽ bị tắt.
  **GIỮ** thu hẹp (a) của r7: chỉ ca có gọi `_quet`. Bản đầu tóm luôn `t2`, `t4`, `t7`… —
  những ca phán quyết của `ops/cong_cu.py kiem-tra`, chẳng liên quan tới cổng `bash_nen`.
  Danh sách này là một **KIỂM KÊ**, không phải một lệnh cấm.

  **VÌ SAO LÀ LUẬT CHỨ KHÔNG PHẢI LỜI KHUYÊN:** sáu lần trước đều là người viết ĐÃ BIẾT nguyên
  tắc ấy rồi vẫn vi phạm — ba lần trong số đó do chính phiên vừa ghi nguyên tắc vào docstring.
  Một nguyên tắc chỉ sống trong docstring thì không phải hàng rào, nó là một lời nhắc mà người
  đang vội sẽ đi qua.

  **NỢ CÓ TÊN:** luật này bắt theo HÌNH DẠNG CÚ PHÁP, nên nó KHÔNG bắt được một ca trói lại
  phán quyết bằng đường vòng — gọi qua hàm phụ, so chuỗi `ly_do`, hay đọc `ngoai_danh_sach`
  rồi suy ra. Nó **thu hẹp cửa, không đóng cửa**. Khai ra thay vì để người sau tưởng đã kín.

  **LẦN THỨ BẢY, THỨ TÁM, THỨ CHÍN — và lần này luật MỚI là thứ bắt.** r11 `t45`, r12 `t47`,
  r13 `t48`: cả ba lọt qua bản r7 vì bản ấy chỉ phủ chiều ĐỎ và chỉ phép so BẰNG. Cả ba đều do
  **bán kính đột biến** bắt, không phải luật. Đó đúng là điều đoạn trên nói: một nguyên tắc chỉ
  sống trong docstring thì không phải hàng rào. Nay nó là hàng rào.
- **N20 — ca cache phải đo VIỆC TÍNH LẠI, và phải GIỮ bằng chứng. SINH TỪ r6.**
  `t34` bản r4 khẳng định `sau == khac` — một **kết quả**, trong khi thuộc tính N19 nói về
  **khoá cache**. Hai thứ ấy trùng nhau trên Linux và TÁCH RA trên Windows, nơi ứng viên ghi đè
  có thể bị **năng lực** từ chối. Ca ấy vì thế đỏ mà không nói được vì sao (xem §0).
  Ba chốt, theo đúng thứ tự:
  1. **Chốt CHÍNH, độc lập nền:** `chan_doan` của lần gọi THỨ HAI phải **chứa** đường ghi đè
     như một ứng viên ĐÃ ĐƯỢC XÉT. Đây đúng là thứ N19 sửa: khoá cũ trả bản nhớ mà không hỏi
     ứng viên nào, nên đường ghi đè sẽ KHÔNG có mặt. Đột biến `t34_khoa_cache_bo_moi_truong`
     phải làm ca đích ĐỎ **qua chốt này**.
  2. Nếu ứng viên ghi đè được CHẤP NHẬN (`dat == true`) ⇒ chốt thêm `sau == khac`.
  3. Nếu nó bị TỪ CHỐI ⇒ **KHÔNG ĐO ĐƯỢC**, kèm `ly_do` **đo được** lấy từ `chan_doan`, không
     phải kèm một suy đoán. `None ≠ False`.
  Và bộ dựng ứng viên phải cố tạo một bản ghi đè **CHẠY ĐƯỢC** trước đã: giữ nguyên **tên tệp**
  (kể cả đuôi `.exe`) và chép kèm các `*.dll` cùng thư mục. Bỏ qua bước ấy là tự chế một ứng
  viên hỏng rồi đổ cho bộ giải.
- **N21 — bộ đo Windows phải CHỐT CÂY trước khi đo. SINH TỪ r6.**
  Lượt `570-do-9` chạy đúng nhưng trên **cây sai**: clone lúc 16:27:55Z, bản vá `c0bc5a5` đẩy
  lúc ~16:33Z, nên nó đo `af0d261` — bản TRƯỚC vá — và vẫn in ra một bảng số trông hợp lệ. Bộ đo
  **tự khai** đủ thông tin để phát hiện (`HEAD` + ba băm) nhưng **không chốt**.
  Bộ đo phải GHIM commit + ba băm và **DỪNG** `rc≠0` khi lệch, in cả hai bên; lệch mà vẫn chạy
  thì kết quả phải mang dấu `KHONG_DO_DUOC_CAY_KHAC` và mã thoát khác 0. Lời dặn bằng miệng
  ("đừng chạy vội") KHÔNG phải hàng rào.
- **N13 — ratchet phải NGẮN đi thật. VIẾT LẠI Ở r4.** Bản r3 nói "danh sách phải ngắn đi", và
  r4 làm nó DÀI RA (0 → 4 mục) vì mở phạm vi. Nói cho đúng: thứ phải ngắn đi là **số lời gọi
  trần CHƯA ĐƯỢC NHÌN THẤY**, không phải độ dài danh sách. Mở phạm vi làm danh sách dài ra
  nhưng làm số-chưa-nhìn-thấy về **0** — đó mới là chiều đúng.
  Chốt thay thế: (a) mọi mục `CHUA_CHUYEN` phải có **ngày gỡ**; (b) `ops/lease_publish_test.py`
  và `ops/cong_cu_test.py` và `ops/cong_cu.py` KHÔNG được quay lại danh sách; (c) N5 (chiều
  ngược) vẫn bắt việc quên xoá khi một mục đã sạch.

- **N45 — bề mặt gọi `bash` đi theo CƠ CHẾ, không theo LIỆT KÊ. SINH TỪ vòng 10.**
  (a) `subprocess.getoutput` / `getstatusoutput` với `cmd` là hằng `bash` (đến bằng VỊ TRÍ hay
  `cmd=`) ⇒ BẮT; chúng có chữ ký RIÊNG, cấm mượn luật vị trí thứ ba của `Popen`.
  (b) tên chương trình bọc `pathlib` — `Path("bash")`, `pathlib.PurePath("bash.exe")` — ở
  `which`, ở `argv[0]` và ở `executable=` ⇒ BẮT.
  CHIỀU NGƯỢC BẮT BUỘC: `Path` bị che bởi một `def` cục bộ, `Path` không từ `pathlib`,
  `Path("/usr/bin/bash")` (một ĐƯỜNG, không phải phân giải theo TÊN), `Path("bash","x")`, và
  `x.getoutput("bash")` trên một module khác ⇒ KHÔNG bắt. Bộ lọc RẺ `_mang_hang_bash` phải
  rộng ít nhất bằng luật thật, kẻo luật thật không bao giờ được hỏi.
  NỢ CÓ TÊN, khai trong docstring: `getoutput("bash -c x")` — một dòng lệnh shell NHIỀU TỪ —
  KHÔNG phủ. Tách dòng lệnh shell là bài toán khác và ở đây chưa đo được cái nào.
- **N46 — MODULE và THÂN LỚP tra tên theo THỨ TỰ CÂU LỆNH; HÀM thì KHÔNG. SINH TỪ vòng 10.**
  Đây là hai luật khác nhau của chính Python, không phải một tinh chỉnh. Bốn chốt, hai chiều:
  gọi TRƯỚC khi gán đè (module, thân lớp) ⇒ BẮT; gán TRƯỚC rồi gọi ⇒ KHÔNG; thân lớp mà mọi
  ràng buộc đều nằm SAU lời gọi ⇒ đi tiếp ra phạm vi BAO chứ không trả None; trong HÀM thì
  `import` rồi gọi rồi gán vẫn MƠ HỒ — mặt này là chốt giữ cho bản vá không tràn sang phạm vi
  hàm, và phải có đột biến làm nó ĐỎ.
- **N47 — `type X[T] = …` có phạm vi chú thích RIÊNG. SINH TỪ vòng 10.**
  Chỉ TÊN alias ràng buộc ở phạm vi chứa; `type_params` và `value` nằm trong phạm vi alias.
  Ba chốt: `T` của alias không che được tên ở dòng SAU; giá trị alias không có tham số kiểu
  vẫn là module thật ⇒ BẮT; BÊN TRONG giá trị alias thì `T` mới là TypeVar ⇒ KHÔNG bắt.
  Chạy trên trình thông dịch **≥ 3.12 thật**; không có thì `BoQuaMoiTruong` KÈM CHẨN ĐOÁN,
  không phải ĐẠT. CI ghim 3.12 ở cả ba chỗ nên ở đó nó CHẠY.
- **N48 — MỌI lối ra của báo cáo phải an toàn, không chỉ lối THÀNH CÔNG. SINH TỪ vòng 10.**
  Hai lớp, và **mỗi lớp phải đo được MỘT MÌNH**: (a) `_duong_bao_cao` phủ từng TRƯỜNG mang
  đường, kể cả `ly_do` của nhánh fail-close và danh sách symlink; (b) `_ra_json` bảo đảm
  stdout của CLI thuần ASCII. Hai lớp cùng che lối `--json`, nên lớp (a) được đo riêng ở lối
  NGƯỜI ĐỌC (không `--json`), nơi không có (b) đỡ. Chỉ đo lối JSON thì một bản vá gỡ (a) đi
  vẫn xanh — tức nửa hàng rào không ai gác.
- **N49 — ratchet phán quyết đi theo RÀNG BUỘC của `_quet`, không theo chữ `rc`. SINH TỪ vòng
  10 (ba P2 của lượt `1091c8a`).** Phải bắt: `assert` trần (CHỈ điều kiện, KHÔNG đọc thông
  điệp), bí danh nhiều tầng (`rc_cong`, `ma = _quet(...)[0]`, `y = rc`), và lời gọi lồng
  (`bang(_quet(...)[0] == 2, …)`). Phải KHÔNG bắt: trường CƠ CHẾ của báo cáo
  (`co_loi_goi_tran`, `lech_oid_dong_cung`), thông điệp văn xuôi, và ca không gọi `_quet`.
  Bảng `_MAU_TOAN_TU` là bản KIỂM KÊ của chính luật này và mọi mục phải khớp `_MAU_MONG`.
- **N50 — mỗi miễn trừ phải mang LÝ DO ĐỌC ĐƯỢC, và lời dặn phải SINH RA TỪ LUẬT. SINH TỪ
  vòng 10.** (a) mục `CA_PHAN_QUYET` ánh xạ tới thứ không phải chuỗi-không-rỗng ⇒ ĐỎ; `""`,
  khoảng trắng, `None`, số đều phải ĐỎ, và phải ĐỎ **một mình** (hai chốt kia im lặng).
  (b) thông điệp hỏng của chốt (0) đọc hai danh sách PHẢI-bắt / KHÔNG-được-bắt **từ
  `_MAU_MONG`**; cấm viết tay, vì bản viết tay đã lệch khỏi luật đúng một revision sau khi
  luật đổi.
- **N51 — cache phải HẾT HIỆU LỰC khi chính TỆP ứng viên đổi. SINH TỪ vòng 10.**
  Vân tay phủ **MỌI** ứng viên đã thử, không chỉ kẻ thắng — vì khi kết quả là `None` thì không
  có kẻ thắng nào, mà `chan_doan` chính là thứ phải hết hiệu lực. Vân tay gồm
  `mtime_ns`/`size`/`ino`/`dev`/`mode`: không cái nào MỘT MÌNH đủ. Ba chốt: tốt→xấu, xấu→tốt,
  và **chiều ngược bắt buộc** — cache VẪN LÀ cache khi không có gì đổi (bỏ cache đi thì hai
  chốt đầu vẫn xanh trong khi mỗi lượt `quet` đẻ thêm hàng chục tiến trình con).
  KHE CÒN LẠI, khai thẳng: tệp vẫn có thể bị thay GIỮA lúc so vân tay và lúc chạy. Vân tay
  thu hẹp cửa sổ, không đóng được nó.

- **N52 — nhận diện tên `bash` bằng BỘ TÍNH HẰNG, không bằng bảng HÌNH DẠNG. SINH TỪ vòng 11,
  chủ kho chọn sau khi đọc phép đo ba phương án.**
  Đối số được **rút gọn về một GIÁ TRỊ** rồi mới hỏi "giá trị này có phải tên `bash`". Phủ:
  hằng `str`/`bytes`, bao chứa lồng nhau, phép nối hằng (`"ba" + "sh"`, nối liền kề), và hàm
  dựng `pathlib` khi callee giải được về `pathlib` thật. `argv` **mở bao chứa theo CÚ PHÁP
  trước** — chỉ phần tử ĐẦU cần là hằng, vì các phần tử sau là đối số và thường là biến (bỏ
  bước này thì `run(["bash", "-c", x])` lọt; đo được trên cây thật).
  CHIỀU NGƯỢC BẮT BUỘC, mỗi mặt một chốt: tập **nhiều** phần tử ⇒ KHÔNG (thứ tự duyệt không
  xác định); `Path("usr", "bash")` nối thành một ĐƯỜNG ⇒ KHÔNG; `Path` bị che hay không từ
  `pathlib` ⇒ KHÔNG; và **hai helper shell KHÔNG nhận path-like** — `Popen(shell=True)` từ
  chối đối số đường dẫn, nên `getoutput(Path("bash"))` là BÁO ĐỘNG GIẢ.
  Bộ lọc RẺ phải rộng ít nhất bằng luật thật, kể cả với phép nối hằng; hẹp hơn là một lỗi
  **LỌT IM LẶNG** vì luật thật không bao giờ được hỏi.
  NỢ CÓ TÊN: mọi thứ đi qua BIẾN, `os.fspath`, `getattr`, hay một hàm người dùng viết. Rút
  gọn hằng không phải phân tích luồng dữ liệu.
- **N53 — ràng buộc HOÀN TẤT MUỘN NHẤT thắng, và hoàn tất là SAU khi vế phải tính xong.
  SINH TỪ vòng 11.** Ở module và thân lớp, không gian tên bị sửa TUẦN TỰ. Bốn chốt: re-import
  sau phép gán ⇒ BẮT; `x = x.run(["bash"])` (lời gọi nằm trong chính biểu thức sinh ra ràng
  buộc) ⇒ BẮT; `def x(a=x.run(["bash"]))` ⇒ BẮT; thân lớp cùng thế. Chiều ngược: gán TRƯỚC ⇒
  KHÔNG; hai ràng buộc hoàn tất CÙNG một chỗ (`a = b = …`) ⇒ vẫn mơ hồ; trong HÀM thì luật
  biên dịch giữ nguyên. Mặc định của một CÂU LỆNH là "câu lệnh đã xong" — thiếu điều ấy thì
  `type X = …` và `:=` trong comprehension ràng buộc ở `(0, 0)` và cổng BẮT OAN.
- **N54 — phép HIỂN THỊ phải ĐƠN ÁNH, và KHOÁ báo cáo KHÔNG dùng phép hiển thị. SINH TỪ vòng
  11; đây là món nợ đặc tả r15 TỰ KHAI.** `co_loi_goi_tran` giữ đường NGUYÊN VẸN (an toàn do
  `_ra_json` lo ở biên giới); `_duong_bao_cao` nhân đôi dấu chéo ngược TRƯỚC khi thoát
  surrogate, nên mọi `\x` ĐƠN trong kết quả chỉ có thể đến từ một surrogate. Chốt: hai tệp
  vi phạm với tên đụng nhau phải cho **HAI** khoá; đường Unicode thường phải nguyên vẹn; và
  mọi câu CHỮ dựng từ khoá phải đi qua lớp hiển thị.
- **N55 — ratchet phán quyết đi theo XUẤT XỨ CÓ VỊ TRÍ, không theo trùng tên. SINH TỪ vòng
  11.** Mỗi tên mang danh sách `(vị trí hoàn tất, nguồn)` với nguồn ∈ {`ma`, `bao`, `bo_doi`,
  `khac`}; tại một phép chốt thì ràng buộc MUỘN NHẤT TRƯỚC nó mới tính — cùng cơ chế N53.
  Phải KHÔNG bắt: `rc` gieo sẵn không từ `_quet`, một chuỗi trùng tên trường trên đối tượng
  khác, bí danh đã bị ghi đè, và `kq[1]["co_loi_goi_tran"]`. Phải bắt: `kq[0]`,
  `kq[1]["trang_thai"]`, `_quet(…)[1]` gán ra tên khác.
- **N56 — vân tay cache phủ CẢ TẬP ỨNG VIÊN, không chỉ những cái đã thử. SINH TỪ vòng 11.**
  Đếm lại ứng viên ở mỗi lần trúng cache (chỉ `stat`, không phóng tiến trình). Chiều VẮNG →
  CÓ là chiều độc: cổng báo KHÔNG CÓ `bash` trên máy ĐÃ CÓ. Chiều ngược N51 vẫn bắt buộc:
  cache VẪN LÀ cache khi không có gì đổi.
- **N57 — `PATH` VẮNG ≠ `PATH` RỖNG. SINH TỪ vòng 11.** Biến vắng ⇒ lùi về `os.defpath`, đúng
  như `os.get_exec_path()`/`execvp`; `PATH=""` tường minh ⇒ không tìm ở đâu cả. Hai chốt, hai
  chiều, trong một ca.

- **N58 — bộ tính hằng gấp `dict` làm argv và VỎ BỌC GIỮ HẰNG. SINH TỪ vòng 12.**
  `dict`: KHOÁ ĐẦU TIÊN là chương trình (thứ tự khoá xác định); khoá `None` (một `**x`) ⇒ không
  đoán. Vỏ bọc: `.encode()`/`.decode()` trên hằng (không che được); `str(…)`/`bytes(…)` CHỈ khi
  tên dựng sẵn KHÔNG có ràng buộc nào trong chuỗi phạm vi; `os.fspath`/`fsencode`/`fsdecode` CHỈ
  khi callee giải về `os` thật. Gọi HÀM THẬT trên giá trị đã gấp — `str(b"bash")` ra `"b'bash'"`
  như Python làm, nên không bị nhận nhầm. Chiều ngược bắt buộc: `str` bị che, `**x` đứng đầu.
- **N59 — CHÍN API phóng theo TÊN ngoài `subprocess`/`shutil`, mỗi mục ba thuộc tính ĐO ĐƯỢC.**
  Vị trí đối số (hai `spawn*p*` mang CHẾ ĐỘ ở vị trí 0), tên từ khoá (`inspect.signature`), và
  KIỂU được nhận. Tra theo CẶP (module, hàm), không theo tên trần. Chiều ngược bắt buộc:
  `os.popen(Path)`, `os.popen(b"…")`, `create_subprocess_shell(Path)`, biến thể KHÔNG `p`
  (`execv`, `posix_spawn` — đo được là không tìm theo PATH), `"bash"` ở vị trí CHẾ ĐỘ, `os`
  bị che, module khác trùng tên hàm.
- **N60 — tên LỚP ràng buộc SAU cả thân và decorator; tên HÀM thì sau header.** Thân lớp CHẠY
  lúc định nghĩa, thân hàm thì không. Chiều ngược: gọi SAU lớp cùng tên ⇒ không bắt.
- **N61 — khoá cache băm TOÀN BỘ môi trường.** `bash` đọc môi trường của chính nó; danh sách
  biến "có ảnh hưởng" không bao giờ đủ. Chỉ lưu BĂM. Chốt tách được N61 khỏi N56: ứng viên giữ
  nguyên mà `BASH_ENV` đổi.
- **N62 — thành phần `PATH` RỖNG là THƯ MỤC HIỆN TẠI, và chuỗi ứng viên giữ `./`.** Thay thế
  câu SAI của N57 (r17). `Path(".") / "bash"` chuẩn hoá thành TÊN TRẦN, nên phép thử sẽ đi tìm
  theo PATH thay vì thử đúng tệp — chuỗi phải là `os.path.join(".", "bash")`. CHƯA ĐO trên
  Windows.
- **N63 — hạn ngạch HỎNG thì FAIL-CLOSE, không ném.** Hỏi kiểu, không ép kiểu: không phải
  `int`, là `bool`, hay âm ⇒ `None` ⇒ `khong_khai_so` ⇒ KHONG_DO_DUOC. Chiều ngược: hạn ngạch
  hợp lệ (kể cả 0, kể cả mục ba phần tử) đọc đúng.
- **N64 — ratchet tính TẬP NGUỒN CÒN TỚI ĐƯỢC, không chọn MỘT nguồn muộn nhất.** Ràng buộc
  mang tập nút điều khiển bao quanh nó; ràng buộc có điều kiện GỘP vào tập, ràng buộc chắc chắn
  chạy trước phép chốt thì che thứ cũ hơn. Biến lặp `for` là có điều kiện. Chiều ngược: ghi
  đè CÙNG nhánh với phép chốt ⇒ không bắt. Nợ có tên: ràng buộc mang qua vòng lặp.

- **N65 — bộ tính hằng gấp f-string KHÔNG biểu thức, `%`, `"sep".join([...])`, cắt lát/chỉ số
  trên hằng.** Phép thật trên giá trị đã gấp; không gọi hàm người dùng. Bộ lọc rẻ phải thấy cả
  bốn (`join` không có mảnh nào là hằng `bash`). Âm: f-string có biến, `join` trên biến, lát cắt
  ra chuỗi khác.
- **N66 — `pty.spawn(argv)` là lời phóng KIỂU ARGV**, kể cả chuỗi trần. Âm: `pty` bị che.
- **N67 — phạm vi HÀM trực tiếp chứa lời gọi theo THỨ TỰ THỰC THI; tên cục bộ chưa có lần ghi
  hoàn tất là `UnboundLocalError`, KHÔNG đọc sang phạm vi ngoài.** Hàm BAO NGOÀI không lọc theo
  vị trí. Đổi ngược doctrine r8/N46.
- **N68 — chú thích không được tính thì không quét**: có `from __future__ import annotations`,
  hoặc `AnnAssign` trong thân hàm. Lời gọi trong chú thích bị bỏ qua được GHI TƯỜNG MINH là
  "không chạy", để chốt `KeyError` của N41 vẫn giữ cho mọi nút khác.
- **N69 — ratchet: `with` có trình quản lý NUỐT NGOẠI LỆ đã biết là nút điều khiển; xuất xứ
  tách theo PHẠM VI từ vựng, tra theo luật closure.** Âm: `with` thường; hàm phụ có biến riêng.
- **N70 — `CONG_CU_BASH` không có dấu phân cách đường được phân giải qua PATH (ngữ nghĩa N62)
  một lần, và cả phép thử lẫn vân tay dùng đường đã phân giải.** `./bash` tường minh giữ nguyên.
- **N71 — mọi mục `ANH_CHUP_DONG_CUNG` phải là bộ ba với OID 40 hex thường, kiểm ở MỌI chế độ
  cây; sai ⇒ `mien_tru_hong` ⇒ KHONG_DO_DUOC.** Không áp lên `CHO_PHEP`/`CHUA_CHUYEN`.

- **N72 — ràng buộc TỚI ĐƯỢC lời gọi theo NHÁNH điều khiển.** Mỗi ràng buộc và mỗi lời gọi
  mang đường `((id(nút), nhánh), …)` từ gốc phạm vi. Tới được: (tiến) hoàn tất trước và không
  tách ở một cặp nhánh LOẠI TRỪ (`if`/`else`, hai `except`, `except`/`else`, hai `case`); hoặc
  (lùi) cùng trong thân một vòng lặp. Bị che khi một ràng buộc khác THỐNG TRỊ lời gọi (đường là
  tiền tố) và nằm giữa. `finally` luôn chạy. Một phạm vi theo thứ tự với lời gọi chỉ khi mọi phạm
  vi ở giữa CHẠY NGAY (thân lớp, list/set/dict comprehension). Thân lớp: lối chưa gán đọc phạm vi
  bao, và nếu phạm vi bao KHÔNG ràng buộc tên ấy thì lối ấy là `NameError` ⇒ báo theo lối còn lại.
  Mơ hồ ⇒ không báo, giữ nguyên. Âm: `except`/`case` anh em, `lop_goi_import_sau`,
  `listcomp_goi_import_sau`, `finally_che_sau`, `lop_nhanh_import_module_che`.
- **N73 — chú thích được LƯU thì quét** (tham số, trả về, biến module/lớp — có hay không có
  `__future__`); chú thích biến CỤC BỘ trong hàm không được lưu ⇒ không quét.
- **N74 — mọi phép thật của bộ gấp hằng đi qua MỘT cửa**: ném vì giá trị ⇒ `_KHONG_BIET` (chương
  trình thật cũng ném lúc tính đối số); `%` có ngân sách khuếch đại 4096 ⇒ vượt thì
  `_VuotNganSach`; `quet` bắt MỌI `Exception` của bộ quét trên một tệp ⇒ `KHONG_DO_DUOC` kèm tên
  ngoại lệ, không traceback.
- **N75 — bộ chốt: nhánh thay nút.** Chỉ trình quản lý NUỐT ngoại lệ (`suppress`, `raises`,
  `assertRaises`, `assertRaisesRegex`) là nhánh có điều kiện — `assertWarns*` không. `finally`
  luôn chạy. Thân lớp không nhìn thấy được từ hàm lồng. Cạnh quay lui của vòng lặp. Cùng mô hình
  loại trừ/thống trị với N72.

- **N76 — bộ giải tên KHÔNG theo thứ tự, KHÔNG theo nhánh.** Trong phạm vi thắng (luật phạm vi
  từ vựng), có bất kỳ ràng buộc `import` theo dõi ⇒ báo. Thân lớp gộp với phạm vi bao; phạm vi
  chú thích PEP 695 nhìn thấy lớp bao nó; đích `:=` trong comprehension không phải ràng buộc cục
  bộ của comprehension. Thay N46/N53/N60/N67/N72 (gỡ). Mọi mẹo che tên PHẢI bị báo —
  `_HINH_DANG_BAO_THAN_TRONG` của `t33`. Nợ: hai `import` KHÁC NHAU cùng một tên ⇒ không báo.
- **N77 — chú thích trên ĐÍCH KHÔNG ĐƠN khi có `__future__` không được tính, không được lưu ⇒
  không quét**; không có `__future__` thì nó được tính ở module/thân lớp ⇒ quét.
- **N78 — ngân sách khuếch đại của `%` là TỔNG** mọi độ rộng/độ chính xác (và số nguyên đối số
  khi có `*`), không phải từng ô.
- **N79 — bộ chốt: comprehension là phạm vi riêng, đích lặp là ràng buộc cục bộ; `except*`
  không loại trừ nhau.**

- **N80 — bộ chốt: nguồn của một tên là HỢP nguồn của MỌI ràng buộc cùng tên trong cả tệp ca**,
  mọi dạng ràng buộc có giá trị (gán, gán chú thích, `+=`, `:=`, `for`/comprehension — kể cả phần tử
  của danh sách hằng, `with … as`). Không hỏi phạm vi, vị trí hay nhánh. Giữ luật nhãn trường.
  Thay N64/N69/N75/N79 (gỡ). Mẫu che tên PHẢI bị bắt.
- **N81 — nạp động với tên HẰNG**: `__import__`, `__builtins__.__import__`, `builtins.__import__`,
  `importlib.import_module` làm bộ nhận hay gán vào tên; `exec`/`eval` với chuỗi HẰNG (giới hạn độ
  sâu 3, độ dài 100 000) — `import` trong tải vào bảng module, lời gọi bash trong tải báo tại vị trí
  `exec`. Không hằng ⇒ nợ có tên.
- **N82 — `nonlocal` tới đúng chủ sở hữu** (bỏ qua hàm giữa cũng khai `nonlocal`); **`global` chỉ
  đọc** không che tên dựng sẵn khi bảng module không ràng buộc tên ấy.
- **N78b/N78c — ngân sách tính TRƯỚC khi dựng**: số độ rộng quá nhiều chữ số (trước `int()`), và
  độ dài `join` = tổng phần tử + dấu phân cách × (n − 1).

- **N83 — nạp động và tải `exec`/`eval`, dạng HẰNG, đầy đủ hơn**: ràng buộc `m = <lời gọi>` (mọi
  đích tên, kể cả gán chú thích và `:=`) được ghi CHỜ GIẢI rồi giải sau khi mọi bảng đã dựng, bằng CẢ
  cú pháp lẫn bộ giải tên (bí danh, hai tầng); `importlib.__import__`; giá trị của `eval` hằng; callee
  `builtins.exec`/`from builtins import exec`; tải gấp qua `_gia_tri_hang` (`bytes` giải mã như trình
  thông dịch); tên trong tải giải theo MỌI ràng buộc `import` của cả tệp; tải hằng không phân tích
  được hoặc lồng quá 3 tầng ⇒ NÉM. Nợ: đích bộ, `:=` trong comprehension, `.eval` trên đối tượng khác.
- **N84 — bộ duyệt KHÔNG đệ quy Python** (`tham`, dựng cây phạm vi, phần tử đầu argv): quét được mọi
  tệp mà Python 3.12 biên dịch được.
- **N85 — argv NỐI/TRẢI**: phần tử ĐẦU của `[…] + …`, `(…) + …`, `[*(…), …]` khi bao chứa viết tại
  lời gọi. Phần tử đầu là BIẾN ⇒ nợ luồng dữ liệu (kể cả khi biến rỗng thì bash chạy).
- **N86 — `%` với vế phải `dict`** được gấp.
- **N87 — bộ chốt: `.get(<trường tổng hợp>)` là một phép đọc trường; tên mang giá trị một trường
  tổng hợp có nguồn `tt`, và chạm tới nó là chạm phán quyết.** Chiều ngược: trường CƠ CHẾ và
  `.get` trên đối tượng khác không tính.

## 6. Ngoài phạm vi

**r4 RÚT một mục ra khỏi đây:** phạm vi cổng. Cổng nay phủ toàn cây (N17). Việc SỬA 11 lời gọi
ngoài `ops/**` thì **vẫn ngoài phạm vi** — r4 chỉ làm chúng NHÌN THẤY ĐƯỢC và có ngày gỡ; sửa
chúng đụng `.claude/**` và `scripts/**`, không nằm trong write set.

- `t131` `t132` (chưa có chỗ) · `t150` (#552) · `t125` (#562) · `t171` và mọi thứ thuộc write set
  của #541 ngoài `ops/lease_publish_test.py`.
- `ops/cai_actionlint.sh` — đã đo LÀNH.
- ~~Hợp nhất `_bash_windows` của `ops/cong_cu.py`~~ — **HẾT HIỆU LỰC ở r3**, nay là N14. Điều
  kiện câu cũ nêu (*"sau khi … rời khỏi tay lease khác"*) ĐÃ THOẢ: đo 20-09T05:05Z,
  `ai-dang-giu ops/cong_cu.py` ⇒ `rc=0`, `NGƯỜI_GIỮ 0`. `_bash_posix` thì đã hợp nhất ở r2.
- Giải thích cơ chế marshalling argv của `bash.exe` WSL. Hai chỗ dữ liệu chưa khép (hai `$0` khác
  nhau trong một lượt; `command -v cygpath` trả KHÔNG CÓ mà ba lời gọi `cygpath` vẫn chạy) đứng ở
  **KHÔNG ĐO ĐƯỢC**. Cấm dựng giả thuyết cho chúng: bản vá không phụ thuộc vào chúng, và ghi một
  nguyên nhân sai vào doctrine còn tệ hơn không ghi gì.

## 7. Điều kiện dừng

### 7.0 ĐIỀU KIỆN THOÁT CỦA VÒNG LẶP REVIEW — ghi lần đầu ở r10

Chủ kho, phiên 2026-09-21 ~18:2xZ và nhắc lại 2026-09-23. **Trước r10 điều kiện này chưa từng
được ghi ở đâu** — không ở spec r9 §7, không ở `dieu_kien_dung` của lease g9 — nên đây là ghi
lần đầu, không phải sửa một tiêu chí đã đóng băng.

- **THOÁT khi: không còn finding P1, P2, P3.** KHÔNG phải "khi approve".
  - CHẶT hơn ở chỗ nó **nêu rõ ngưỡng**: một phép ĐẾM trên nhãn mức độ, hết chỗ diễn giải.
  - LỎNG hơn ở chỗ nó **cho phép** finding dưới P3 (P4 / nit / informational) còn lại.
  - **HỆ QUẢ THAO TÁC:** mỗi verdict phải **ĐẾM THEO MỨC ĐỘ**, không chỉ đếm tổng. Ô chưa
    review ghi `chưa review`, **không** ghi `0` — `None ≠ False`.
- **MỘT VÒNG =** vá → review chéo → **đọc finding và ĐO LẠI từng cái** (không nhận lời khai) →
  **trừu tượng hoá thành LỚP rồi quét cả cây tìm thực thể khác** → vá theo lớp → chạy trọn bộ ca
  + bán kính đột biến → **đăng verdict kèm bảng đếm theo mức độ** → lặp.
- **Review chéo dùng phiên bản / effort CAO HƠN executor.** r10: reviewer `codex gpt-6-astra`
  effort `low`; executor `fable` (`claude-fable-5-1`) effort `low` (r12; r10–r11 là `medium`).
- **HINT PATCH** cho vấn đề phức tạp: verdict phải nêu **CƠ CHẾ** và chỗ sửa, không chỉ triệu
  chứng — để vòng sau không phải tự tìm lại.
- **KHÔNG chạy CI, không `workflow_dispatch`, không full CI** cho tới khi đủ điều kiện merge.
  **KHÔNG cần CI Windows** — chủ kho: lỗi Windows đã biết từ trước. Đo cục bộ, cộng bộ đo
  Windows chạy TAY trên máy chủ kho.
- Chưa tới ngưỡng thoát mà lease hết hạn ⇒ **DỪNG, xin thế hệ mới. KHÔNG tự gia hạn.**
  Đã xảy ra hai lần: g6 lỡ hạn 09:45Z; g9 lỡ hạn 2026-09-22T06:25Z và mất 26 giờ.

### 7.1 Điều kiện dừng của EXECUTOR

- Một hình dạng lỗi lặp lần thứ BA ⇒ DỪNG, hỏi *"có nên làm việc này không"*.
- Cần chạm bất kỳ đường nào ngoài write set ⇒ DỪNG, xin revision.
- `ai-dang-giu` cho `ops/lease_publish_test.py` còn cho thấy một NGƯỜI GIỮ NÀO KHÁC ngoài lease
  của chính packet này ⇒ KHÔNG chạm tệp ấy. Đo TRƯỚC mỗi lần chạm, đọc `rc` TRỰC TIẾP, và đọc cả
  `da_bi_thay_the`. "Hết hạn" KHÔNG phải "đã nhả"; "đã land" cũng KHÔNG phải "đã nhả".
  **Đây là câu r1 viết SAI** — r1 đòi `rc=0` / `NGƯỜI_GIỮ 0`, mà lease của chính packet luôn giữ
  đường ấy nên điều kiện không bao giờ thoả được. Một điều kiện không thoả được sẽ bị diễn giải
  lại trong im lặng; nêu ra đây thay vì để nó chết âm thầm.
- Ba chốt của N2 không phân biệt được bằng đầu vào ⇒ khai thẳng là bộ TƯƠNG ĐƯƠNG, báo lại, không
  tự quyết.
- **Sau N14, nếu `ops/cong_cu.py` cần một phép lọc theo TÊN để chạy được ⇒ DỪNG và báo.** Đó là
  dấu hiệu bộ giải năng lực chưa đủ cho đường ấy, và vá bằng cách nhét lại một danh sách cấm là
  tái sinh đúng khuyết tật packet này sinh ra để giết.
- **Nếu hợp nhất xong mà bán kính đột biến trên Windows VẪN không đọc được ⇒ DỪNG.** Đó là lần
  thứ BA của cùng một hình dạng, và câu hỏi đúng lúc ấy là *"có nên đo bằng bán kính không"*,
  không phải *"nới ngưỡng thế nào"*.
