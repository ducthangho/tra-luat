# ĐẶC TẢ PACKET — `TAT-DINH-VOID-HA-TANG`, **revision 3**

```yaml
packet_id: TAT-DINH-VOID-HA-TANG
packet_issue: 262
revision: 3
generation: 1
thay_the: ops/specs/TAT-DINH-VOID-HA-TANG-r2.md   # r2, sha256 dcfb81bb699a603ec90db53be18975fc75c7938e20e8d997f702703cec386be1
review_class: sensitive
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: 05de1ab81c235235b971a6fb8d8ae1fb226295d5
```

## 0. Delta so `revision 2` — đổi TIÊU CHÍ PHÂN LOẠI, không đổi thêm một điều kiện

r1 nhận `stdout_byte: 0` kèm rc≠0. r2 bỏ nó, giữ `ma_thoat ∈ {12,13}`. **Cả hai đều sai theo CÙNG
một cách**, và đây là lần thứ **HAI** của cùng hình dạng — nên r3 không thêm điều kiện thứ ba mà
đổi **thứ được phép làm bằng chứng**.

Đo bằng launcher THẬT, con tự thoát 12 sau khi in một lỗi nội dung:

```
run.json  = {"trang_thai":"xong","ma_thoat":12,"stdout_byte":0}
void-attempt --reason infrastructure  ->  rc=0,  attempts_used 1 -> 0
```

`launcher.py:50-51` đã cảnh báo đúng điều này, nguyên văn:

> *"với `run`, mã thoát của **TIẾN TRÌNH CON** được trả nguyên vẹn, nên nó **ĐÈ LÊN** mọi mã ở đây"*

### Luật thay thế: NGUỒN GỐC, không phải giá trị

| trường | ai đặt | dùng làm bằng chứng? |
|---|---|---|
| `ma_thoat` | **tiến trình con** (trả nguyên vẹn) | **KHÔNG** |
| `stdout_byte` | **tiến trình con** | **KHÔNG** |
| `trang_thai: qua_han` | **launcher** (`launcher.py:1486`, cưỡng chế hạn chót) | có |
| `trang_thai: hong` | **launcher** (`launcher.py:1407`, không chạy được lệnh) | có |
| `trang_thai: xong` | con đã chạy và tự thoát | **KHÔNG** |

Một tiêu chí chỉ được làm bằng chứng hạ tầng khi **kẻ bị đo không đặt được giá trị ấy**. r1 và r2
đều vi phạm; r3 phát biểu thẳng luật đó thay vì liệt kê thêm ca.

**Ca thiếu công cụ / chưa xác thực không mất chỗ**: ảnh `doctor --json` đã phủ, và ảnh ấy là một
**phép đo** chứ không phải lời khai của tiến trình bị đo.

### Thứ hai: N10 của r2 đòi CHẠY, ca lại chỉ khớp chuỗi

r2 N10 viết *"chạy đúng khối lệnh đã sửa… **Không** được đo bằng cách đọc tài liệu"*. Ca đã giao chỉ
kiểm hai chuỗi con, nên `doctor --json >` (lệnh hỏng cú pháp) **vẫn qua**. Executor **tự khai giới
hạn ấy trong prompt gọi review rồi vẫn giao** — cùng thói *"nghĩ ra được phép thử mà không chạy nó
thì phép thử ấy không tồn tại"*.

## 1. `write_set` — giữ 3 đường dẫn của r2

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md
```

## 2. `ngan_sach_kich_thuoc` — GIỮ 320, không xin nới

Cả hai bản vá là **bớt**: M3″ xoá một nhánh, N10′ thay một hàm khớp chuỗi bằng một hàm chạy thật.
Nếu tổng vượt 320 thì **DỪNG và nén**, không nới lần thứ hai — r2 đã nới một lần.

## 3. `muc_tieu` — chỉ ghi cái ĐỔI so với r2

M1 · M2 · M4 · M5 · M6 · M8 giữ **nguyên văn**.

| # | mục tiêu | tệp |
|---|---|---|
| **M3″** | Bằng chứng từ `run.json` **CHỈ** nhận `trang_thai ∈ {`qua_han`, `hong`}` — hai giá trị do **launcher** đặt. **BỎ** `ma_thoat`, **BỎ** `stdout_byte`: cả hai do tiến trình con quyết định, nên chúng là **lời khai của kẻ bị đo**. Ca thiếu công cụ/chưa xác thực đi bằng ảnh `doctor` | `packet_loop.py` |
| **N10′** | Ca canh luồng canonical phải **TRÍCH khối lệnh rồi CHẠY nó**, không khớp chuỗi. Chạy trong thư mục state riêng để không đụng state vận hành | `packet_loop_test.py` |

## 4. `nghiem_thu` — chỉ ghi cái ĐỔI

| # | nghiệm thu | phép đo làm nó ĐỎ |
|---|---|---|
| **N4d** | `run.json` do launcher THẬT sinh ra từ một con **tự thoát 12** ⇒ `rc=10`, `attempts_used` **không** giảm. Cùng vậy với **13** | đột biến khôi phục `ma_thoat ∈ {12,13}` ⇒ ca ĐỎ |
| **N4e** | `trang_thai: qua_han` và `trang_thai: hong` ⇒ `rc=0` — chiều **BẮT OAN** | ca chiều-tha; giết bằng đột biến **siết** (bỏ luôn `trang_thai`) ⇒ chỉ N4e ĐỎ, N4d vẫn xanh |
| **N10′** | Khối lệnh trích từ `§7.4a` **chạy được**, sinh ảnh `doctor` thật và mở được lượt | đột biến làm hỏng lệnh trong **tài liệu** (ví dụ cắt cụt `doctor --json >`) ⇒ ca ĐỎ. Ca cũ khớp-chuỗi **không** đỏ với đột biến này — đó là bằng chứng nó chưa từng đo |

## 5. `dieu_kien_dung`

- **Attempt 3/3 là lượt CUỐI.** Hỏng nữa ⇒ packet về `blocked`, xuất handoff, reroute là việc của
  bên điều phối.
- **Vượt 320 dòng ⇒ nén, KHÔNG nới.** r2 đã nới một lần.
- **Nếu lại xuất hiện một tiêu chí phân loại dựa trên giá trị mà bên bị đo đặt được** ⇒ lần thứ BA
  của cùng hình dạng ⇒ DỪNG, không vá lần thứ tư (`docs/PROTOCOL_DA_PHIEN.md` §12).

## 6. `chua_do_duoc`

- **`trang_thai` vẫn là thứ launcher GHI RA ĐĨA**, nên ai sửa được tệp `run.json` thì sửa được nó.
  r3 chỉ đóng đường *"con tự chọn mã thoát"*, **không** đóng đường *"người vận hành sửa tệp"*. Đường
  sau đã có cửa `--khong-co-bang-chung` **có ghi sổ**; ai chịu ghi sổ thì không cần giả mạo.
- **N10′ chạy khối PowerShell — trên Linux chạy được hay không phụ thuộc `pwsh` có mặt.** Nếu vắng,
  ca phải **bỏ qua CÓ IN LÝ DO** và điều đó phải đo được, chứ không im lặng xanh.
- **Bốn chỗ mỏng của r1 vẫn còn nguyên**, không cái nào được đóng qua ba vòng review: ngưỡng tươi
  3600s đo bằng `mtime` · `getattr` nuốt im lặng một lần đổi tên · `--can-cu` chỉ kiểm không rỗng ·
  `quota`/`rate_limit` nhận theo lời khai.
