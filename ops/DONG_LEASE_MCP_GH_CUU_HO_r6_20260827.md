# ĐÓNG SỚM lease `mcp-gh-cuu-ho-exec-1r6-codex-20260827` — 27-08-2026

**Tệp này chỉ để TÌM THẤY.** Bản có thẩm quyền là khối `DONG_LEASE` trong chính lease
`ops/leases/mcp-gh-cuu-ho-exec-1r6-codex-20260827.yaml`. Đừng chép số liệu ra đây rồi để hai bản
trôi lệch — đúng bệnh đã làm một packet tiền nhiệm bị `blocked`.

Nó tồn tại vì kho đã có `ops/RUT_LEASE_PLAT_X8_20260821.md` và một phiên sau sẽ `grep` chữ
"RUT_LEASE"/"ĐÓNG LEASE" chứ không đọc từng lease.

| khoá | giá trị |
|---|---|
| `lease_id` | `mcp-gh-cuu-ho-exec-1r6-codex-20260827` |
| packet | `MCP-GH-CUU-HO`, Issue #319, PR #339 |
| đã đăng | **CÓ** — `posted_comment_id: 5433738994` |
| hạn gốc | `2026-08-28T03:00:00Z` |
| hạn sau khi đóng | `2026-08-27T04:20:00Z` — rút ngắn 22 giờ 40 phút |
| người quyết | người giữ kho, direct in-session 27-08-2026 |
| lý do | verdict vòng 4 `changes_requested` với HAI P1 trong write set, biên ngân sách 0, lease CẤM nâng trần ⇒ không land được và không vá tiếp được trong cùng lease |

## KHÁC tiền lệ PLAT-X8 ở một chỗ quan trọng

`RUT_LEASE_PLAT_X8` rút một lease **chưa từng được đăng** — nên không có bản chiếu nào để lệch.
Lease này **đã đăng**. Comment `5433738994` trên #319 vẫn hiển thị hạn CŨ và không có đường nào
đính chính nó tự động. **Bản chiếu và bản có thẩm quyền nay LỆCH NHAU**, và cách duy nhất người đọc
issue biết là đọc lease.

## Nợ kỹ thuật bị lần thứ HAI trong hai ngày

`AG-T0-01B-thu-hoi-lease-chua-co-duong`. Nguyên văn đã ghi từ 21-08: *"kho vốn không có đường ấy…
cơ chế duy nhất được cài đặt là chờ hết hạn."*

Cái đã làm ở đây là **sửa một trường** cho tới khi `ai-dang-giu` đọc ra `HẾT_HẠN`. **Đừng đọc thành
"kho có đường thu hồi lease".** Không tầng nào cưỡng chế rằng executor phải ngừng ghi.

Đề xuất khi có packet chạm được `ops/lease_publish.py`: một khối `DONG_LEASE` **có schema**, cộng
một lượt đăng comment đính chính lên issue khi lease bị đóng sớm — để bản chiếu không đứng yên khi
bản có thẩm quyền đổi.

## Đã xác minh sau khi đóng

`ops/lease_publish.py ai-dang-giu` trên nhánh lease đã đồng bộ (`dbce615`):

    .claude/dev/mcp_gh_test.py   ->  NGƯỜI_GIỮ 0
    .claude/dev/mcp_gh.py        ->  NGƯỜI_GIỮ 0
    ops/specs/mcp-gh-cuu-ho.md   ->  NGƯỜI_GIỮ 0

Đối chứng — hai packet khác KHÔNG bị đụng:

    docs/GOI_AGENT_DA_NEN.md     ->  NGƯỜI_GIỮ 1  (doctrine-ranh-gioi-reviewer-exec-1r4, #318)
    .claude/dev/probe_mang.py    ->  NGƯỜI_GIỮ 1  (mang-sandbox-codex-exec-1, #334)

## Việc KHÔNG bị đụng

Nhánh `claude/mcp-gh-cuu-ho-exec-1` giữ nguyên tại `f461413a`, cổng xanh
(`CA 40/40 · ĐỘT BIẾN 48/48 · D8(a)(b)(c) ĐẠT · rc=0`). Không revert, không đóng PR #339.
Đóng lease là nhả QUYỀN GHI, không phải bỏ việc.
