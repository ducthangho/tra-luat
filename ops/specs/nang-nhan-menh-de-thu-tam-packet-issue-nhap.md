# `NANG-NHAN-MENH-DE-THU-TAM` — đo lại hạng của mệnh đề thứ tám, sau khi #334 land

Mục 2 của `ops/BAN_GIAO_PHIEN_20260827.md` nói việc này **chỉ mở ra SAU khi #334 land**.
#334 đã land lúc `2026-08-28T01:40Z` (master `fe6152be`), nên bằng chứng bốn tổ hợp nay đọc được
từ clone bất kỳ.

## Mệnh đề đang bàn

`docs/GOI_AGENT_DA_NEN.md`, khoảng dòng 674-686. Nguyên văn nhãn hiện tại:

> mạng đóng của sandbox là một MẶC ĐỊNH CẤU HÌNH, không phải bất biến — DÙ có biết cơ chế thì cũng
> KHÔNG làm nó thành ranh giới ⇒ **chưa xếp được**, cho câu hỏi *"nó có phải ranh giới không"*.

Và lý do nó **chưa** lên hạng, chính tệp ấy đã viết ra:

> VÌ SAO `chưa xếp được` chứ không phải `chiều MỞ`: A/B hai-biến chứng minh TỔ HỢP cấu hình đổi được
> kết quả, KHÔNG đo cờ nào là nguyên nhân; `ls-remote` không ghi `.git` nên "cờ mạng là thủ phạm" là
> SUY LUẬN, mà bảng hạng đòi cơ chế ĐÃ XÁC MINH. […] Phép tách bốn tổ hợp
> (không cờ · chỉ mạng · chỉ ghi · cả hai) thuộc packet kia; **xong nó thì hạng này đo lại được**.

Tức tệp đã ghi sẵn **đường quay lại**. Packet này đi đúng đường ấy — không phải sửa lén sau land.

## Bằng chứng nay đã có trên master

`docs/MANG_SANDBOX_CODEX.md` (land cùng #334) có bảng bốn tổ hợp:

| tổ hợp | `network_access` | `writable_roots` | socket | url | git |
|---|---|---|---:|---:|---:|
| (a) | không | không | 1 | 1 | 1 |
| (b) | **CÓ** | không | 0 | 0 | 0 |
| (c) | không | CÓ | 1 | 1 | 1 |
| (d) | CÓ | CÓ | 0 | 0 | 0 |

> `network_access=true` một mình đã đảo cả ba quan sát; `writable_roots` không đảo ô nào.

Đó đúng là phép tách một-biến mà mệnh đề thứ tám đang chờ.

## CÂU HỎI CỦA PACKET — và nó là câu hỏi THẬT, không phải tu từ

Bàn giao phiên trước viết rằng mệnh đề "**có thể** lên `cơ chế đã xác minh — chiều MỞ`, phân bố về
`1/5/2/0/0`". **Đó là GIẢ THUYẾT của phiên ấy, không phải kết luận đã đo.** Packet này phải tự
quyết, và phải quyết bằng phép đo, vì cùng tệp bằng chứng ấy mang **hai giới hạn** mà bàn giao
không nhắc tới:

1. **Chính `docs/MANG_SANDBOX_CODEX.md` tự hạ phạm vi:**
   > Loopback không phải egress: cờ này gate capability socket rộng hơn hai phép HTTPS ra ngoài,
   > nên kết quả chỉ **xác minh phạm vi cờ cấu hình đã đo, không xác minh một ranh giới mạng**.

2. **Kênh `git` ở (a)/(c) là `KHÔNG_ĐO_ĐƯỢC`, không phải "bị chặn":**
   > `git` ở (a)/(c) bị chặn bởi CHÍNH SÁCH SANDBOX hay bởi HẠ TẦNG PROXY của phiên chạy — **CHƯA
   > TÁCH ĐƯỢC.** […] `class` của `git` phụ thuộc cấu hình proxy TỪNG PHIÊN, không phải hằng số
   > theo Codex.

Nên ba khả năng đều mở, và packet phải chọn một **kèm lý lẽ đo được**:

- **(A)** Nâng lên `cơ chế đã xác minh — chiều MỞ` **không kèm điều kiện** ⇒ phân bố `1/5/2/0/0`.
- **(B)** Nâng lên `chiều MỞ` **kèm thu hẹp phạm vi tường minh** (ví dụ: xác minh cho socket và
  url; `git` vẫn `KHÔNG_ĐO_ĐƯỢC` và phải nói ra ngay tại chỗ) ⇒ phân bố vẫn `1/5/2/0/0` nhưng
  nội dung mệnh đề khác hẳn (A).
- **(C)** **GIỮ** `chưa xếp được`, vì hai giới hạn trên nghĩa là cơ chế vẫn chưa xác minh đủ cho
  câu hỏi *"nó có phải ranh giới không"* ⇒ phân bố giữ `1/4/3/0/0`.

**Không được chọn (A) chỉ vì bàn giao gợi ý (A).** Kho này có bảy lần bắt được lỗi
"bản ghi nói ngược thứ đo được", và một bản ghi *đúng ý người viết trước* vẫn là bản ghi phải bị đo lại.

## Ràng buộc

- Nếu đổi nhãn thì phải đổi **CẢ BA** thứ cùng lúc, không được đổi một: (i) nhãn của mệnh đề,
  (ii) đoạn `VÌ SAO ... chứ không phải ...` giải thích nhãn ấy, (iii) phép đếm phân bố ở khoảng
  dòng 625-626. Kho hỏng **bốn lần** đúng hình dạng "sửa TRƯỜNG được nới, quên VĂN BẢN mô tả nó".
- Bảng hạng ở dòng 616-620 là **hợp đồng**; đọc nó trước, đừng nhớ theo lần trước.
- **KHÔNG chép số đo, probe hay bảng hai pha từ `docs/MANG_SANDBOX_CODEX.md` về đây** — chính tệp
  đang sửa đã dặn *"Thứ ở packet kia là số đo đầy đủ, probe và bảng hai pha — đừng chép chúng về
  đây."* Trỏ sang, đừng nhân bản.
- Reviewer vòng 14 của #318 đã chốt một câu phải giữ: *"hạng đo TRẠNG THÁI BẰNG CHỨNG mà người đọc
  exact tree có thể kiểm, không phải nhãn chân trị của thế giới bên ngoài."* Mọi lựa chọn phải
  đứng được dưới câu đó.

## write set đề xuất

- `docs/GOI_AGENT_DA_NEN.md`

Đúng một đường. `docs/MANG_SANDBOX_CODEX.md` **KHÔNG** vào write set — packet này chỉ ĐỌC nó.

## Ngân sách đề xuất

Nếu chọn (A) hoặc (B): sửa nhãn ~1 dòng · viết lại đoạn `VÌ SAO` ~8-12 dòng · sửa phép đếm ~2 dòng.
Nếu chọn (C): chỉ cần ghi thêm rằng bằng chứng đã có mà vẫn không đủ, và VÌ SAO — cũng ~8-12 dòng.
Ước lượng **~25 dòng**; trần đề xuất **50**, biên gấp đôi.

**Chạm trần ⇒ CẮT hoặc VIẾT NGẮN LẠI, KHÔNG nâng trần.** #319 đã nâng bốn lần và con số mất hết ý
nghĩa.

## Tiền lệ đọc trước khi làm

`docs/GOI_AGENT_DA_NEN.md` đã đi qua **15 vòng** cross-review ở packet #318, trong đó ba vòng cuối
đều xoay quanh đúng mệnh đề này. Đọc `ops/reviews/doctrine-ranh-gioi-reviewer-review-{13,14,15}-codex-verdict.md`
trên nhánh `ops/cap-lease-tach-314` trước khi gõ dòng nào — vòng 13 bắt được một bản vá **khai một
phép đo KHÔNG XẢY RA**, và vòng 14 bắt được nhãn hạ đúng mà **nội dung mệnh đề vẫn khai "biết cơ chế"**.
Hai lỗi ấy nằm chính xác ở chỗ packet này sắp chạm vào.
