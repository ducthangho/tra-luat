# Packet Spec — W0-R1B (Issue #177), phạm vi ĐÃ MỞ RỘNG

**TRẠNG THÁI: CHƯA ĐƯỢC BẮT ĐẦU.** Tệp này là bản mô tả thay thế cho thân Issue `#177`.
Nội dung dưới đây soạn để **dán thẳng** vào Issue. Sau khi dán, đọc ngược về và đối
chiếu: tầng vận chuyển của GitHub chuẩn hoá dấu nháy kép thành thực thể HTML, và **trong
code span thì thực thể KHÔNG được giải mã** nên nó hiện nguyên văn ra màn hình. Bản này
đã tránh sẵn dấu nháy kép và dấu ngoặc nhọn bên trong mọi code span.

**Vì sao phải mở rộng:** người giữ kho đã chốt trần review canon là **2 VÒNG**
(`docs/PROTOCOL_DA_PHIEN.md`, và `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` §10). Trần đó
rơi vào một trục đếm mà `packet_loop.py` **chưa có trần nào cả** — khác với trục mà
`#177` bản gốc nhắm tới. Chi tiết ở mục 2.

---

## THÂN ISSUE — dán từ đây

### W0-R1B — Trần review đang TỰ NGUYỆN ở cả hai trục đếm

Phụ thuộc: `W0-R1 integrated`.
Write set: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`.
Review class: `sensitive`.

### 1. Trục LỜI GỌI — có trần, nhưng trần không có răng

`record-review` **không đọc sổ lời gọi**. Bỏ qua `record-review-call` thì nhiều vòng
review vẫn khép trọn với `used=0/2`.

Phản chứng chạy được: `init` rồi lặp ba lần cặp `begin-attempt` + `record-review`, không
gọi `record-review-call` lần nào. Kết quả: packet khép, `codex_review_calls_used` vẫn
bằng 0, trần 2 chưa từng được chạm.

Nguyên nhân: mọi bộ đếm khác của tệp này được **dệt vào đường bắt buộc** — không đi qua
chúng thì không đi tiếp được. Riêng `codex_review_calls_used` nằm trên một lệnh **rời**,
người vận hành phải tự nhớ gọi. Bộ đếm nào cần người nhớ thì nó là tài liệu, không phải cổng.

### 2. Trục VÒNG — không có trần nào để mà tự nguyện

Đây là phần **mới**, sinh ra từ quyết định chốt trần 2 vòng.

Đo trên `packet_loop.py`: `review_rounds_used` chỉ được khởi tạo (dòng 638) và **tăng**
(dòng 997). Không có `review_rounds_limit`. Không nơi nào đọc nó để chặn.

Hai bộ đếm này là **hai trục khác nhau**, và chính chú thích trong `W0-R1` đã ghi:
*Khác `codex_review_calls_used`: một vòng có thể tốn nhiều lời gọi.*

| trục | bộ đếm | hằng | cưỡng chế |
|---|---|---|---|
| vòng — thứ vừa được chốt trần 2 | `review_rounds_used` | không có | **không có gì cả** |
| lời gọi — trục chi phí | `codex_review_calls_used` | `MAC_DINH_TRAN_REVIEW_CALL` = 2 | có, nhưng **né được** (mục 1) |

Nên trần 2 lời gọi sẵn có **không** thoả điều khoản 2 vòng. Không được coi việc đã có
trần lời gọi là đã xong việc.

**Bằng chứng lịch sử:** packet `W0-R1` đã chạy **4 vòng** review. Trần của kế hoạch cũ là
**3 vòng** (`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` §8). Tức nó vượt cả trần cũ, và không
có gì dừng nó lại.

### 3. Phải làm gì

1. Dệt `codex_review_calls_used` vào đường bắt buộc, hoặc để `record-review` tự đọc sổ
   lời gọi. Sau thay đổi, không còn đường nào khép một vòng review mà bộ đếm không nhúc nhích.
2. Thêm `review_rounds_limit`, mặc định 2, và cưỡng chế nó y như trần lời gọi đang làm:
   cạn thì đưa packet về `checkpoint` và thoát `RC_TRAN`.
3. Lượt bị `void` vì lý do thuộc `LY_DO_VOID` (quota, rate_limit, infrastructure,
   permission) **không** tính vào trần vòng. Một vòng là một lượt reviewer trả verdict
   trên một exact head, cộng lượt executor sửa theo verdict đó.
4. Hai trần cưỡng chế **độc lập**. Cạn trần nào cũng dừng. Không gộp chúng làm một.

### 4. Tiêu chí nghiệm thu

- Phản chứng ở mục 1 phải **đỏ** sau bản vá: ba vòng review không gọi
  `record-review-call` không còn khép được với `used=0/2`.
- Có phản chứng cho trần vòng: vòng thứ ba bị chặn, packet về `checkpoint`, mã thoát
  `RC_TRAN`.
- Có phản chứng cho miễn trừ `void`: một lượt `void` vì quota **không** làm tăng
  `review_rounds_used`, và không đẩy packet tới trần sớm.
- Có phản chứng cho tính độc lập: cạn trần vòng khi trần lời gọi **chưa** cạn thì vẫn
  phải dừng, và ngược lại.
- Mỗi lớp lách phải có đột biến của nó, theo đúng khuôn `AC 18` mà bộ test hiện dùng.
- `python3 .claude/dev/packet_loop_test.py` xanh toàn bộ, số ca và số đột biến **chép từ
  đầu ra của máy**, không gõ tay.

### 5. Ràng buộc

- Write set đúng hai tệp trên, kiểm trên **TỪNG commit**, không chỉ trên diff gộp.
- Chạy bộ test **trong** `.claude/dev/`. Chạy từ thư mục tạm cho **đỏ giả**: vài ca tìm
  tệp kho theo đường dẫn tương đối và tìm lịch sử git.
- Đặt `core.abbrev` bằng 7 trước khi chạy bất kỳ cổng nào, đúng như CI ghim. Không đặt
  thì hai ca doc-claims **đỏ oan** trên clone đủ lịch sử, và đỏ oan đó đứng trước mọi
  cổng khác nên nó che mất phép đo thật.
- Trần review áp cho chính packet này: **2 vòng**.
- Mỗi finding của reviewer phải kèm gợi ý cách vá bốn phần, theo verdict contract trong
  `docs/PROTOCOL_DA_PHIEN.md`.

### 6. Không thuộc phạm vi

- Không đụng `#178` (W0-RC). Hai packet dùng chung tệp nên **không chạy song song**.
- Không đổi ngữ nghĩa `attempts_used` hay trần executor.
- Không đổi định nghĩa `LY_DO_VOID`.

## THÂN ISSUE — hết
