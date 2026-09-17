verdict: approve
reviewed_sha: 2b28061d9b07

# CROSS-REVIEW LƯỢT 5 — packet #546 `MOI-TRUONG-CONG-CU-DO-DUOC` r1/g1

| | |
|---|---|
| `reviewed_sha` | `2b28061d9b07` |
| `base_sha` | `f27a28ffa3cc` · `numstat` **3 tệp, +308 / −3** |
| lượt trước | `81f7067c6f16` — lượt 4, `LỚP 9` mở |
| diễn biến lượt này | `81f7067..2b28061` = **1 tệp, +2 / −2** |
| kết luận | **`approve`** — `LỚP 9` **ĐÓNG, có răng trên Windows THẬT**; không hồi quy mới |
| assurance | **`advisory_review`** |

## HIỆN VẬT ĐO

| tệp | nguồn |
|---|---|
| `ops/reviews/moi-truong/windows-2b28061-TONGKET-lop9.txt` | chủ kho dán nguyên văn từ phiên PS7, máy Windows của chủ kho |

**Một điều KHÔNG ĐO ĐƯỢC, khai ngay đây.** `N1.log` đầy đủ nằm trên Drive
(`_HOP_NAP`, `fileId 1g46B-V5D0SdM2IcPUaMVUAr74uySKiRY`, 1 999 B theo siêu dữ liệu). Phiên này đọc
nó qua MCP Google Drive và bản về **đã bị chuẩn hoá kiểu Markdown** — dấu gạch dưới bị thoát (`\_`),
mọi dòng kết thúc bằng hai dấu cách. Đó là tạo tác của **đường ĐỌC**, đúng lớp lỗi kho đã trả giá.
Nên verdict này **không khai `sha256` của `N1.log`**: byte thật của nó là `KHÔNG ĐO ĐƯỢC` từ đây.
Nội dung thông tin thì tra được, và nó khớp dòng tổng kết trong bản dán.

## `LỚP 9` — ĐÓNG, xác nhận trên Windows THẬT

Bản vá, toàn bộ diễn biến lượt này:

```python
-    bang(rc == 0 and "BIEN UTF-8" in "\n".join(in_dong) and "CANH BAO" not in "\n".join(in_dong), ...)
+    bang(rc == 0 and "BIEN UTF-8" in "\n".join(in_dong) and not any("CANH BAO" in d and "UTF-8" in d for d in in_dong), ...)
-    bang(rc_v == 0 and "CANH BAO" in "\n".join(in_dong), "thieu phai canh bao")
+    bang(rc_v == 0 and any("CANH BAO" in d and "UTF-8" in d for d in in_dong), "thieu phai canh bao")
```

Đo trên `MINGW64_NT-10.0-26200`, python 3.13.1, chạy tại
`/d/Quốc hội/tl546 do546 lop9/kho` — **dấu cách VÀ ký tự ngoài ASCII**, tức đúng nền đã làm `LỚP 9` đỏ:

```
N2 => 1/1 qua, 0 bo qua, 0 hong
N3 => 0/1 qua, 0 bo qua, 1 hong     (quay ve dang RONG cu)     TRUOC=1 SAU=0
N4 => 0/1 qua, 0 bo qua, 1 hong     (go canh bao UTF-8)        TRUOC=1 SAU=0
```

Bộ đo **tự chứng minh đột biến đã áp** (`TRUOC=1 SAU=0` ở cả hai), nên "sống sót" không thể bị nhầm
với "chưa áp". `N3` là phép đo quyết định: nó chứng minh **bản vá** đóng `LỚP 9`, chứ không phải
đường dẫn tình cờ sạch.

**AGY VÁ HƠN THỨ TÔI YÊU CẦU, và đó là công của agy.** Bàn giao của tôi chỉ nêu vế phủ định. Vế
khẳng định thứ hai (`thieu phai canh bao`) trước đó cũng khớp cảnh báo đường dẫn của `M5`, nên ở
đường có dấu cách nó **xanh kể cả khi cảnh báo UTF-8 bị gỡ hẳn** — một kênh dương tính giả tôi
không phát hiện. Agy siết cả hai vế. `N4` chính là phép đo cho vế ấy, và nó giết đột biến.

## KHAI VÒNG TRÒN — bắt buộc, theo cảnh báo trong chính lease

Lease #546 viết: *"nếu reviewer cấp HINT patch mà executor áp gần nguyên bản thì reviewer đang tự
chấm bản vá của mình"*. Áp vào đây, trung thực:

- Bàn giao `LỚP 9` của tôi đề xuất **đúng** hình dạng *"neo `CANH BAO` và `UTF-8` trên CÙNG một
  dòng"*. Agy áp đúng thế. ⇒ Phán quyết của tôi về **hình dạng** bản vá **không có giá trị độc lập**.
- Thứ **có** giá trị độc lập là `N3`/`N4`: đột biến đo **hành vi**, không đọc mã, và cả hai số đều
  sinh trên máy chủ kho chứ không phải trên rig của tôi.
- Thứ **hoàn toàn độc lập với tôi** là vế khẳng định thứ hai — tôi không nêu, agy tự tìm.

## MỘT QUAN SÁT KHÔNG GIẢI THÍCH ĐƯỢC — `t53` và `t73`

| | Windows @ `81f7067` | Windows @ `2b28061` |
|---|---|---|
| `N1` | `169/172` (tổng 189, bỏ qua 17, **hỏng 3**) | `172/172` (tổng 189, bỏ qua 17, **hỏng 0**) |
| ba ca hỏng | `t53` · `t73` · `t150` | — |

`t150` xanh thì giải thích được. **`t53` và `t73` thì KHÔNG.** Chúng không nằm trong 17 ca bỏ qua,
tức đã CHẠY và ĐẠT. Một diff **2 dòng trong một ca test khác** không thể làm điều đó.

Thứ đã đổi là **rig**: lượt 4 chạy thẳng trong `D:\Quốc hội\tl546`; lượt 5 chạy trong một **clone
sạch** do bộ đo tự tạo (tôi đổi thiết kế sau khi bản trước suýt bảo chủ kho `checkout` đè lên cây
làm việc đang có thay đổi chưa commit của agy).

Hệ quả phải ghi, vì nó **sửa một lời khai của chính verdict lượt 4**: nhãn *"ĐỎ SẴN"* dán cho
`t53`/`t73` ở lượt 4 là **hẹp hơn sự thật**. Đúng hơn: **đỏ trong checkout ấy, xanh trong clone
sạch** — tức nhiều khả năng chúng phụ thuộc TRẠNG THÁI CÂY chứ không phải đỏ theo mã. Chưa ai đo
được biến nào gây ra, nên đây là `KHÔNG ĐO ĐƯỢC`, không phải "đã chữa".

Vì sao việc này **không** chặn `approve`: chiều lệch có lợi (`3 → 0`, không ca nào mới đỏ), và câu
hỏi của packet là *"bản vá có đóng `LỚP 9` mà không gây hồi quy không"* — cả hai vế đều có phép đo.
Nhưng nó **phải** thành nợ có tên, kẻo lần sau ai đó lại đọc "đỏ sẵn" thành một sự thật của mã:
**`T53-T73-DO-THEO-RIG-CHUA-BIET-BIEN`**.

## BẢNG ĐO ĐẦY ĐỦ — kể cả cái khớp

| phép đo | nền | kết quả |
|---|---|---|
| `t150` ở đường không dấu cách | Linux | `1/1 qua` |
| `t150` ở đường có dấu cách | Linux | `1/1 qua` |
| `t150` ở đường dấu cách + ngoài ASCII | Linux | `1/1 qua` |
| `t150` ở đường dấu cách + ngoài ASCII | **Windows** | **`1/1 qua`** |
| đột biến quay về dạng rộng cũ, đường có dấu cách | Linux · **Windows** | **bị giết** cả hai |
| đột biến gỡ cảnh báo UTF-8 | Linux · **Windows** | **bị giết** cả hai |
| đột biến gỡ tiêu đề `BIEN UTF-8` | Linux | bị giết |
| đột biến đổi `UTF-8` → `UTF8` trong thân cảnh báo | Linux | bị giết |
| `launcher_test` | Linux | `187/188` (tổng 189, bỏ qua 1, hỏng 1 = `t53`) — **y hệt `81f7067`, delta 0** |
| `launcher_test` | **Windows** | `172/172` (tổng 189, bỏ qua 17, hỏng 0) |
| `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` | Linux | **rc=0** cả bốn |
| `ruff` | Linux | **KHÔNG ĐO ĐƯỢC** — container không có module |

**Trần ADR-0044 sau ngoại lệ chủ kho: ≤ 3 tệp / ≤ 340 dòng thêm. Đang ở `3 tệp / 308 dòng`.** Đạt,
còn 32 dòng dư.

## MỘT LỖI CỦA BỘ ĐO CỦA TÔI — ghi vì nó suýt thành báo cáo sai

Lượt chạy Linux ĐẦU TIÊN của đột biến `N3` cho **SỐNG SÓT**. Nếu tin, tôi đã báo rằng bản vá của agy
không đóng được `LỚP 9` — sai hoàn toàn. Nguyên nhân: runner của tôi chép cây từ đường **có** dấu
cách **vào** `…/scratchpad/db_MC` — **không** dấu cách. Đột biến chạy ở đường sạch nên dạng rộng cũ
đương nhiên xanh.

Đúng bệnh `H8` của đợt PS7 trước (`$env:TEMP` rỗng ⇒ đột biến chưa từng được áp ⇒ "sống sót" giả),
và lần này nó tái phát ở **chiều khác**: đột biến ĐƯỢC áp, nhưng chạy ở **nền sai**. Nên chốt
`TRUOC=1 SAU=0` là **cần mà KHÔNG đủ** — nó chứng minh đột biến đã áp, **không** chứng minh nền đo
đúng biến. Bộ đo gửi chủ kho nay **fail-close** khi đường nền không có dấu cách (`exit 95`), và in
thẳng `NEN CO DAU CACH: co  <= day la bien dang do`.

## `LỚP` CÒN LẠI — trạng thái, không làm tròn

| lớp | trạng thái | phán quyết có giá trị ĐỘC LẬP? |
|---|---|---|
| 1a | đóng một phần — dấu vết tự tay dựng vẫn ra `DA_CHAY` | không (HINT) |
| 1b · 3 · 5 | đóng | không (HINT) |
| 2 | **ĐÓNG** + nợ `HOOK-KHONG-DAT-DUOC-BIEN-CHO-PHIEN` | **có** |
| 4 · 6 | **ĐÓNG** | **có** |
| 7 · 8 | **ĐÓNG** — xác nhận trên Windows | **có** |
| **9** | **ĐÓNG** — xác nhận trên Windows, hai đột biến bị giết | **một phần** (xem khai vòng tròn) |

## ASSURANCE — trần cứng, không phải nhận xét về bản vá

`advisory_review`. `antigravity` xuất hiện **0 lần** trong `docs/PROTOCOL_DA_PHIEN.md`, và §8 nêu
**đích danh** `Codex` cho class `sensitive`. Không bản vá nào của packet này mua được `cross_approved`;
việc ấy thuộc packet riêng **#551** (spec đã đóng băng, chưa cấp lease, xếp sau #548).

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
