# ĐO — vì sao hai lease #482/#483 hết hạn mà không có hiện vật

**Đo lúc `2026-09-09T09:32Z`**, phiên `session_01UN8WRS5Bc5pBBzYPDqs9Dx`.
Công cụ: `mcp__Claude_Code_Remote__{list_sessions,get_session}`.

## Vì sao tệp này tồn tại

`ops/land/pr478-land-evidence.yaml` (đã ở `master` qua PR #486) khai trong `bookkeeping`:

> **Hai packet mới mở và lease đã HẾT HẠN mà KHÔNG có việc nào được làm:** #482
> `MU-REF-KHONG-PHU-TAG` và #483 `VERDICT-KHONG-BOC-HOI` […] **VÌ SAO thì KHÔNG ĐO ĐƯỢC** từ phiên
> này — công cụ quản lý phiên đã ngắt, không đọc được transcript của hai phiên executor.

Câu *"KHÔNG ĐO ĐƯỢC"* ấy đúng **với phiên đó**. Phiên này có công cụ quản lý phiên, nên đo được.
Ghi ra đây thay vì để nguyên một ô trống, và ghi **cả chỗ lời khai cũ rộng hơn phép đo của nó**.

## Hai phiên executor CÓ TỒN TẠI — đo được, trái với "không có việc nào được làm"

| trường | #482 | #483 |
|---|---|---|
| session id | `session_01URP5SCYUtnDcnJT1ZiKciM` | `session_01EqPtjFXUFep4TY5KWNyNr8` |
| tiêu đề | `#482 MU-REF-KHONG-PHU-TAG — executor` | `#483 VERDICT-KHONG-BOC-HOI — executor` |
| tags | `executor`, `mission-481`, `packet-482` | `executor`, `mission-481`, `packet-483` |
| parent | `session_01C52eS8AgeiwTrDifXGDGYP` | `session_01C52eS8AgeiwTrDifXGDGYP` |
| model cấu hình / đã phục vụ | `claude-fable-5-1` / `claude-fable-5-1` | `claude-fable-5-1` / `claude-fable-5-1` |
| tạo lúc | `2026-09-08T03:45:45Z` | `2026-09-08T03:46:32Z` |
| cập nhật cuối | `2026-09-08T04:08:49Z` | `2026-09-08T04:02:28Z` |
| khoảng sống | **23 phút 04 giây** | **15 phút 56 giây** |
| `output_tokens` | **66 709 token** | **26 680 token** |
| `cost_usd` | **8,898 USD** | **5,127 USD** |
| `context_usage.used_tokens` | 233 392 / 1 000 000 token | 212 175 / 1 000 000 token |
| `status_bucket` | `SESSION_STATUS_BUCKET_FAILED` | `SESSION_STATUS_BUCKET_FAILED` |
| `connection_status` | `disconnected` | `disconnected` |
| nhánh trong container | `claude/mu-ref-khong-phu-tag` | `claude/verdict-khong-boc-hoi` |

## NGUYÊN NHÂN — một, và giống nhau ở cả hai

Cả hai phiên có **cùng một** `post_turn_summary`:

```
status_category: failed
status_detail:   "You've hit your weekly limit · resets Sep 9, 8am (UTC)"
rate_limit_info: {rateLimitType: "seven_day", status: "rejected",
                  resetsAt: 1788940800, isUsingOverage: false}
```

`resetsAt 1788940800` = **`2026-09-09T08:00:00Z`**. Tại lúc đo (`09:32Z`) hạn mức ấy **đã reset
được 1 giờ 32 phút**.

Nguyên nhân là **hạn mức 7 ngày của tài khoản bị từ chối**, không phải lỗi packet, không phải lỗi
lease, không phải môi trường. Cả hai phiên bị chặn cùng lúc vì dùng chung một hạn mức.

## LỜI KHAI CŨ RỘNG HƠN PHÉP ĐO CỦA NÓ

Land evidence khai *"KHÔNG có việc nào được làm"* và dẫn ba phép đo: 0 nhánh trên `origin`, 0 PR,
Issue chỉ có 2 comment. Ba phép đo ấy **đúng** — đo lại `2026-09-09T09:32Z` trên 312 `refs/heads`:
không ref nào tên `claude/mu-ref-khong-phu-tag` hay `claude/verdict-khong-boc-hoi`; chỉ có
`ops/cap-lease-mu-ref-va-verdict` (nhánh CẤP lease).

Nhưng ba phép đo ấy đo **HIỆN VẬT**, còn kết luận nói về **VIỆC**. Hai phiên sinh ra
**66 709** và **26 680** token đầu ra trong **23 phút** và **16 phút** — tức có chạy và có sinh nội
dung. Điều **không** xảy ra là **push**: container ngắt, nhánh chỉ tồn tại cục bộ, nội dung mất.

Câu đúng với phép đo: **"không có hiện vật nào được đẩy lên"**, không phải "không có việc nào được
làm". Cùng lớp lỗi mà `CLAUDE.md` gọi là *lời khai rộng hơn phép đo*, và cùng lớp với
`VERDICT-KHONG-BOC-HOI` — chính packet #483.

**Giới hạn của phép đo này, nói thẳng:** `output_tokens` chứng minh phiên đã chạy và đã sinh nội
dung; nó **KHÔNG** chứng minh nội dung ấy là việc của packet, cũng không nói được bao nhiêu phần
việc đã xong. Transcript hai phiên chưa đọc. Muốn biết còn cứu được gì thì phải mở lại chính hai
phiên ấy (`unarchive`/`send_message`), và tới lúc đo thì chúng `IDLE` + `disconnected`.

## Hệ quả cho việc cấp lại lease

Điều kiện dừng mà bàn giao đặt ra — *"đừng cấp lại lease trước khi biết lượt đầu chết ở đâu"* —
**đã thoả**: lượt đầu chết vì hạn mức tuần, và hạn mức đã reset.

Nếu chủ kho quyết định cấp lại: `revision: 2`, `generation` giữ **1** (contract không đổi, cùng
`spec_hash`). Kèm một chốt rút từ chính sự cố: executor phải **push nhánh sớm** thay vì đợi xong —
một phiên bị cắt giữa chừng không mang được gì ra ngoài container.
