# ĐẶC TẢ PACKET — WP570-BASH-NEN-MOT-BO-GIAI, revision 1

- **Issue:** https://github.com/ducthangho/tra-luat/issues/570
- **Trạng thái:** ĐÓNG BĂNG khi lease `wp570-bash-nen-r1-g1-claude` được cấp. Mọi thay đổi
  objective / acceptance / write set / executor / environment ⇒ revision mới, generation mới,
  cấp lại lease (§3.2 `docs/PROTOCOL_DA_PHIEN.md`).

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
    path: ops/cong_cu_test.py
  - type: exact
    path: ops/lease_publish_test.py
```

**KHAI THẲNG — công việc TRƯỚC LEASE.** `ops/bash_nen.py` và `ops/cong_cu_test.py` ĐÃ được thay
đổi ở PR #571 (`010fb281f52b27364e4e3e3515d125b084f9d20e`) theo chỉ thị *"Vá đi"* của chủ kho,
lúc packet này CHƯA có lease. Lease r1 bao trùm chúng về sau; nó KHÔNG hợp thức hoá ngược việc
đã làm, chỉ ghi nhận đúng sự thật để không ai đọc nhầm rằng phần ấy đã qua cổng lease.

Hai đường KHÔNG vào write set, và lý do đo được:
- `ops/cong_cu.py` — hợp nhất `_bash_windows` vào `ops/bash_nen.py` là việc ĐÚNG nhưng lease
  `wp541-path-r3-g3-claude` khai nó trong `khong_duoc_cham`. Để lại ở ratchet `CHUA_CHUYEN`.
- `ops/cai_actionlint.sh` — đã đo là LÀNH; không có gì để sửa.

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
  `HEAD` đã đo, và REF nào trỏ tới `HEAD` ấy. Trong đó `bash_nen tim` phải cho thấy
  `C:\Windows\system32\bash.EXE` **đã được THỬ rồi bị TỪ CHỐI vì phép argv** — chọn đúng thôi
  chưa đủ, phải từ chối ĐÚNG LÝ DO.
- **N10 — delta nền = 0.** Mọi cổng chạy lại trên `origin/master` sạch để so DELTA. Đỏ sẵn thì
  khai "đỏ sẵn, delta = 0", không vá lung tung.

## 6. Ngoài phạm vi

- `t131` `t132` (chưa có chỗ) · `t150` (#552) · `t125` (#562) · `t171` và mọi thứ thuộc write set
  của #541 ngoài `ops/lease_publish_test.py`.
- `ops/cai_actionlint.sh` — đã đo LÀNH.
- Hợp nhất `_bash_windows` của `ops/cong_cu.py`, và hợp nhất `_bash_posix` — chỉ được làm sau khi
  `ops/lease_publish_test.py` và `ops/cong_cu.py` rời khỏi tay lease khác; ratchet giữ chỗ.
- Giải thích cơ chế marshalling argv của `bash.exe` WSL. Hai chỗ dữ liệu chưa khép (hai `$0` khác
  nhau trong một lượt; `command -v cygpath` trả KHÔNG CÓ mà ba lời gọi `cygpath` vẫn chạy) đứng ở
  **KHÔNG ĐO ĐƯỢC**. Cấm dựng giả thuyết cho chúng: bản vá không phụ thuộc vào chúng, và ghi một
  nguyên nhân sai vào doctrine còn tệ hơn không ghi gì.

## 7. Điều kiện dừng

- Một hình dạng lỗi lặp lần thứ BA ⇒ DỪNG, hỏi *"có nên làm việc này không"*.
- Cần chạm bất kỳ đường nào ngoài write set ⇒ DỪNG, xin revision.
- `ai-dang-giu` cho `ops/lease_publish_test.py` chưa trả `rc=0` ⇒ KHÔNG chạm tệp ấy. Đo TRƯỚC mỗi
  lần chạm, đọc `rc` TRỰC TIẾP, và đọc cả `da_bi_thay_the`. "Hết hạn" KHÔNG phải "đã nhả".
- Ba chốt của N2 không phân biệt được bằng đầu vào ⇒ khai thẳng là bộ TƯƠNG ĐƯƠNG, báo lại, không
  tự quyết.
