# W0-R1B (#177) — PHỤ LỤC QUYẾT ĐỊNH, không phải spec thay thế

**Authority là thân Issue `#177`.** Tệp này chỉ ghi *quyết định chốt trần 2 vòng ảnh hưởng
tới `#177` như thế nào*. Nó **không** thay thế, không mở rộng write set, không đổi
acceptance của Issue.

## 0. Đính chính bản trước của chính tệp này

Bản đầu của tệp này được soạn khi phiên **chưa đọc được** thân `#177` (đường REST theo kho
bị proxy chặn). Nó đề xuất thêm `review_rounds_limit` như một **trần độc lập** cho
`review_rounds_used`. Sau khi đọc được thân Issue qua GitHub MCP, đề xuất đó là **sai
hướng** và đã bị gỡ:

- `#177` mục 3 đã thiết kế sẵn hai hướng (1 và 2) trong đó **mỗi vòng review phải tiêu ít
  nhất một lời gọi**. Khi đó số vòng ≤ số lời gọi ≤ trần lời gọi. Trần vòng có được
  **bắc cầu**, không cần cơ chế thứ hai.
- Thêm một trần độc lập là dựng hai cơ chế cho một việc, và làm `#177` phải khai quan hệ
  giữa **ba** trần thay vì hai — ngược đúng thứ mục 4 đòi (*quan hệ giữa chúng được khai
  tường minh*).

Bài học giữ lại: phần phân tích *hai trục đếm khác nhau* vẫn đúng và hữu ích — nhưng
**cách đóng** thì Issue đã có sẵn và tốt hơn.

## 1. Quyết định chốt trần 2 vòng gỡ đúng nút thắt của mục 3

Mục 3 của `#177` nêu cái giá của hướng 1 và 2 như sau:

> Mặc định `attempts_limit = 3` nhưng `review_calls_limit = 2`. Nếu `record-review` đòi mỗi
> vòng ít nhất một lời gọi đã tiêu, thì một packet ở mặc định **không bao giờ đạt 3 vòng
> review** — trần review cắn trước trần attempt.

Đó là cái giá **khi chưa có trần vòng canon**. Nay người giữ kho đã chốt trần canon là
**2 vòng** (`docs/PROTOCOL_DA_PHIEN.md`; `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` §10).

Vậy *"không bao giờ đạt 3 vòng review"* **thôi là khuyết điểm và trở thành ĐÚNG SPEC**.
Phản đối chính với hướng 1 và 2 mất hiệu lực.

## 2. Hệ quả trực tiếp: hướng 3 bị LOẠI

Hướng 3 của mục 3 là *giữ nguyên + hạ lời hứa* — khai `codex_review_calls_used` là **sổ tự
khai**, và **bỏ chữ `trần`** khỏi mọi chỗ mô tả nó.

Hướng đó nay **mâu thuẫn trực tiếp với canon**: canon quy định một trần **được cưỡng chế**,
không phải một con số tham khảo. Chọn hướng 3 là để canon không có chỗ bám trong mã.

Còn lại **hướng 1 hoặc hướng 2**. Chọn cái nào vẫn là quyết định của người giữ khi cấp
lease — phụ lục này **không** chọn hộ.

## 3. Điều `#177` phải trả lời thêm, do canon sinh ra

Mục 3 đòi hướng 1 và 2 trả lời: *trần nào cắn trước, và người vận hành đọc ra điều đó ở đâu.*
Canon làm câu trả lời **hẹp lại**, và thêm một câu phải trả lời:

1. Trần **vòng** phải cắn trước trần **attempt** ở cấu hình mặc định. Đây nay là hành vi
   ĐÚNG, phải có phản chứng khẳng định nó, không phải phản chứng chống nó.
2. Lượt bị `void` vì lý do thuộc `LY_DO_VOID` (quota · rate_limit · infrastructure ·
   permission) **không** được tính vào trần vòng — nếu không, một lần hết quota sẽ ăn mất
   một trong hai vòng mà reviewer chưa hề nói gì. Cần phản chứng riêng cho miễn trừ này.
3. Ca `cap_lan_4_thoat_3` và **21 ca** dùng `c.review(...)` phải đổi tiền đề theo canon
   2 vòng, và **ghi rõ lý do đổi** — đúng ràng buộc mục 4 (*không ca nào bị vô hiệu hoá để
   cho qua*).

## 4. Hai luật mới khác áp cho chính packet này

- **Mỗi finding của reviewer phải kèm gợi ý cách vá bốn phần** (vá ở đâu · vá thế nào · ca
  test khoá nó + đột biến nào phải chết · bản vá này có thể đẻ ra gì). Luật ở verdict
  contract trong `docs/PROTOCOL_DA_PHIEN.md`.
- **Master drift sau khi gate xanh ⇒ merge thẳng**, theo `docs/PROTOCOL_DA_PHIEN.md` §5.1,
  kèm sáu kích hoạt bắt buộc chạy lại. Riêng packet này, kích hoạt số 2 gần như chắc chắn
  trúng nếu `#178` land trước — hai packet dùng chung `packet_loop_test.py`.

## 5. Không đổi

`required_review_assurance: cross_approved` và `required_independent_reviewer: codex` của
`#177` **giữ nguyên**. Quyết định chốt trần vòng không đụng tới mức assurance, và không
biến `same_provider_approved` thành đủ.
