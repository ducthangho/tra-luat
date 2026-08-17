# Vòng 4 — chốt khuyến nghị cho hai owner decision

Tiếp tục cùng session read-only. Codex đồng ý ba chỉnh sửa cuối của vòng 3:

1. launcher lane đổi thành `W0-M1 → W0-M3 → W0-M4 → W0-M2`;
2. W0-R2 không sửa `ops/lease_publish.py`, dùng module validator riêng nếu cần;
3. W0-M4 ghi cả wall elapsed và active/monotonic elapsed, ghi rõ clock làm timeout.

Không còn dissent về bundle A–G hay 9 điểm khung. Vòng này chỉ chọn **khuyến nghị chung** cho hai
owner decision; không mở scope mới.

## Đề nghị của Codex

### D1 — deadline sau W0-M4

- Giữ hợp đồng fail-closed theo **absolute wall clock**; không đổi timeout sang active-time.
- Không tự động chặn Modern Standby hay sửa power policy của máy.
- Tách profile deadline thay vì một hằng 45 phút: mặc định đề nghị **90 phút cho Claude Executor
  Opus/max**, **45 phút cho read-only reviewer**. Mọi lượt vẫn neo `deadline_utc`; sổ ghi `wall_elapsed`,
  `active_elapsed`, và `timeout_clock=wall`.
- Sau 3–5 lượt thật, xem lại percentile/thực tế; không tự động nâng trần.

Lý do: giữ nghĩa của deadline và kill tree, tránh quyền OS phát sinh; 90 phút đủ bao lượt vòng 1
(58 phút wall) mà không biến thành vô hạn. Con số là giá trị khởi điểm cần chủ kho duyệt.

### D2 — receipt v2

- Bắt buộc hai trường identity mới cho **mọi receipt tạo mới sau mốc v2**.
- 11 receipt cũ giữ nguyên, đọc theo legacy v1; không bồi/viết lại bằng suy đoán.
- v1 chỉ là historical/read-only và **không đủ điều kiện** làm bằng chứng identity cho required check
  mới; v2 là schema duy nhất cho write path mới.
- Validator phân biệt version rõ ràng, có phản chứng: receipt mới thiếu identity phải đỏ; v1 không
  được nâng quyền thành evidence v2.

Lý do: không viết lại chứng cứ lịch sử; compatibility không được hiểu thành trust escalation.

## Yêu cầu kết luận

1. Verdict riêng cho D1 và D2: `AGREE | AGREE_WITH_CHANGE | DISAGREE`.
2. Nếu đổi, chỉ nêu một giá trị/luật thay thế cụ thể và phản chứng.
3. Xác nhận bản khuyến nghị chung cuối cùng, những gì chủ kho thật sự phải duyệt, và rằng không
   cần vòng 5 nếu đã hội tụ.

Không sửa file.
