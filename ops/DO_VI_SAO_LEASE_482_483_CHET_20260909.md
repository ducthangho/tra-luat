# HỒ SƠ — trạng thái được khai của hai phiên executor #482/#483

**Điều phối khai đã đọc API lúc `2026-09-09T09:32Z`**, phiên `session_01UN8WRS5Bc5pBBzYPDqs9Dx`.
Công cụ được khai: `mcp__Claude_Code_Remote__{list_sessions,get_session}`.

**Giới hạn nguồn:** không kèm response API, transcript hoặc log đọc lại. Các trường
session, số token, chi phí, trạng thái, model, nhánh trong container và thông báo lỗi
dưới đây là ATTESTATION của điều phối; reviewer offline không xác minh được sự kiện API.
Phép tính từ các mốc được khai và việc đọc ref trong snapshot Git là hai phần đối chứng
được riêng. Không dùng số học đúng để xác thực các mốc nguồn.

## Vì sao tệp này tồn tại

`ops/land/pr478-land-evidence.yaml` (đã ở `master` qua PR #486) khai trong `bookkeeping`:

> **Hai packet mới mở và lease đã HẾT HẠN mà KHÔNG có việc nào được làm:** #482
> `MU-REF-KHONG-PHU-TAG` và #483 `VERDICT-KHONG-BOC-HOI` […] **VÌ SAO thì KHÔNG ĐO ĐƯỢC** từ phiên
> này — công cụ quản lý phiên đã ngắt, không đọc được transcript của hai phiên executor.

Câu *"KHÔNG ĐO ĐƯỢC"* ấy mô tả giới hạn **của phiên trước**. Phiên điều phối hiện tại khai
đã dùng công cụ quản lý phiên để bổ sung dữ liệu; nguồn thô chưa được lưu trong hồ sơ.
Ghi ra đây thay vì để nguyên một ô trống, và ghi **cả chỗ lời khai cũ rộng hơn phép đo của nó**.

## Hai phiên executor được điều phối khai đã tìm thấy — chưa xác minh lượng việc của packet

| trường | #482 | #483 |
|---|---|---|
| session id | `session_01URP5SCYUtnDcnJT1ZiKciM` | `session_01EqPtjFXUFep4TY5KWNyNr8` |
| tiêu đề | `#482 MU-REF-KHONG-PHU-TAG — executor` | `#483 VERDICT-KHONG-BOC-HOI — executor` |
| tags | `executor`, `mission-481`, `packet-482` | `executor`, `mission-481`, `packet-483` |
| parent | `session_01C52eS8AgeiwTrDifXGDGYP` | `session_01C52eS8AgeiwTrDifXGDGYP` |
| model cấu hình / đã phục vụ | `claude-fable-5-1` / `claude-fable-5-1` | `claude-fable-5-1` / `claude-fable-5-1` |
| tạo lúc | `2026-09-08T03:45:45Z` | `2026-09-08T03:46:32Z` |
| cập nhật cuối | `2026-09-08T04:08:49Z` | `2026-09-08T04:02:28Z` |
| chênh lệch tạo/cập nhật cuối | **23 phút 04 giây** | **15 phút 56 giây** |
| `output_tokens` | **66 709 token** | **26 680 token** |
| `cost_usd` | **8,898 USD** | **5,127 USD** |
| `context_usage.used_tokens` | 233 392 / 1 000 000 token | 212 175 / 1 000 000 token |
| `status_bucket` | `SESSION_STATUS_BUCKET_FAILED` | `SESSION_STATUS_BUCKET_FAILED` |
| `connection_status` | `disconnected` | `disconnected` |
| nhánh trong container | `claude/mu-ref-khong-phu-tag` | `claude/verdict-khong-boc-hoi` |

## Thông báo lỗi cuối được khai — chưa đủ để loại trừ nguyên nhân khác

Điều phối khai cả hai phiên trả cùng nội dung `post_turn_summary` sau:

```
status_category: failed
status_detail:   "You've hit your weekly limit · resets Sep 9, 8am (UTC)"
rate_limit_info: {rateLimitType: "seven_day", status: "rejected",
                  resetsAt: 1788940800, isUsingOverage: false}
```

`resetsAt 1788940800` (đơn vị: giây Unix) quy đổi thành **`2026-09-09T08:00:00Z`**.
Mốc `2026-09-09T09:32:00Z` cách mốc reset được thông báo **1 giờ 32 phút**. Số học này
không xác nhận hạn mức thực tế đã reset hoặc tài khoản đã dùng được trở lại.

Nếu bản chép API đúng, thông báo cuối ghi một lần từ chối do hạn mức tuần. Nó chưa đủ
để loại trừ lỗi packet, lease hoặc môi trường; chưa có transcript để xác định toàn bộ
diễn biến hay chứng minh hai phiên bị chặn cùng thời điểm.

## LỜI KHAI CŨ RỘNG HƠN PHÉP ĐO CỦA NÓ

Land evidence cũ khai *"KHÔNG có việc nào được làm"* từ việc không tìm thấy nhánh/PR
và số comment được thuật lại. Điều phối khai lần đọc ref lúc `2026-09-09T09:32Z` có
**312 ref nhánh**; inventory đúng lần đọc ấy không kèm. Việc đếm ref không kiểm được số
PR hoặc comment trên GitHub.

Hậu kiểm offline bằng snapshot gói lúc `2026-09-09T10:28:51Z` đếm **313/313 ref nhánh**
khớp giữa `cay-kho/` và `kho.git`. **2/2 tên nhánh** `claude/mu-ref-khong-phu-tag` và
`claude/verdict-khong-boc-hoi` vắng trong tập đó. Ref `ops/cap-lease-mu-ref-va-verdict`
trỏ commit `a2468831896601c60c216133eac2ba1366fd3254`. Đây là snapshot cục bộ; không phải
phép đọc lại GitHub hoặc tái tạo inventory ở mốc lịch sử trước đó.

Hai phiên được khai sinh **66 709 token** và **26 680 token**. Nếu dữ liệu API đúng, nó
cho biết phiên có sinh nội dung; chưa xác nhận nội dung là công việc của packet. Các mốc
tạo/cập nhật cách nhau **23 phút 04 giây** và **15 phút 56 giây**, không đo thời gian tính
toán liên tục. Không thấy tên nhánh trong snapshot không chứng minh chưa từng push,
nhánh chỉ tồn tại cục bộ, container đã mất nội dung hoặc không còn đường phục hồi.

Câu giới hạn được đối chứng: **"hai tên nhánh dự kiến vắng trong snapshot refs/heads"**.
Không nâng nó thành kết luận về mọi hiện vật, lịch sử push hoặc lượng việc đã làm.

**Giới hạn của phép đo này, nói thẳng:** `output_tokens`, nếu bản chép API đúng, cho biết phiên có sinh nội dung; nó **KHÔNG** chứng minh nội dung ấy là việc của packet, cũng không nói được bao nhiêu phần
việc đã xong. Transcript hai phiên chưa được lưu/đối chứng. Trạng thái `IDLE` + `disconnected` cũng
chỉ là lời khai API. Khả năng phục hồi nội dung chưa được kiểm; hồ sơ này không cấp quyền
mở lại phiên hoặc gửi thông điệp.

## Hệ quả cho việc cấp lại lease

Điều phối dẫn điều kiện dừng *"đừng cấp lại lease trước khi biết lượt đầu chết ở đâu"*.
Hồ sơ mới chỉ có thông báo lỗi hạn mức được chép lại. **Chưa đủ bằng chứng để tuyên điều
kiện dừng đã thoả**, hạn mức đã khả dụng hoặc đã biết trạng thái công việc có thể phục hồi.
Quyết định cấp lại cần nguồn phiên và trạng thái hiện hành được người có thẩm quyền kiểm.

Đề xuất điều phối `revision: 2`, giữ `generation: 1` và cùng `spec_hash` chỉ có hiệu lực
nếu contract thực sự không đổi và được cấp theo authority hiện hành. Đây không phải lease
mới. Đẩy đầu ra sớm trong write set được cấp có thể giảm rủi ro mất việc khi phiên ngắt;
snapshot này không chứng minh mọi nội dung chưa push đều đã mất.
