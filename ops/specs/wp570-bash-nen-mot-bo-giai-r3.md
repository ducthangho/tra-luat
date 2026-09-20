# ĐẶC TẢ PACKET — WP570-BASH-NEN-MOT-BO-GIAI, revision 3

- **Issue:** https://github.com/ducthangho/tra-luat/issues/570
- **Trạng thái:** ĐÓNG BĂNG khi lease `wp570-bash-nen-r3-g3-claude` được cấp. Mọi thay đổi
  objective / acceptance / write set / executor / environment ⇒ revision mới, generation mới,
  cấp lại lease (§3.2 `docs/PROTOCOL_DA_PHIEN.md`).

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
- **N13 — ratchet phải NGẮN đi thật.** Sau N7 và N12, `ops/lease_publish_test.py` và
  `ops/cong_cu_test.py` phải RỜI khỏi `CHUA_CHUYEN`. `N5` là thứ bắt việc quên xoá, nên tiêu chí
  này đo được bằng chính cổng chứ không bằng mắt.

## 6. Ngoài phạm vi

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
