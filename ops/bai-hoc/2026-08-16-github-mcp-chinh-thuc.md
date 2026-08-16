# Bài học: GitHub KHÔNG bị chặn — chỉ là tôi gõ nhầm host suốt một ngày

**Ngày đo:** 2026-08-16 · **Phiên:** wp55 executor `claude`

Tôi vận hành cả ngày trên giả định *"api.github.com trả 403 nên GitHub API không dùng được"*.
Giả định ấy **sai**, câu trả lời đúng nằm sẵn trong kho từ 14-08, và tôi đã đọc lướt qua nó.

---

## Đường ĐÚNG — đo được, chép nguyên số

```bash
curl -sS -X POST https://api.githubcopilot.com/mcp/ \
  -H "Authorization: Bearer $GITHUB_PAT" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'
```

| | |
|---|---|
| có `GITHUB_PAT` | **HTTP 200**, 44 công cụ |
| không token | **HTTP 401** |

Có `create_pull_request`, `merge_pull_request`, `pull_request_read`, `add_issue_comment`,
`create_or_update_file`, `update_pull_request_branch`, … Đủ cho mọi việc mà phiên agent cần
làm với GitHub.

Đã dùng thật: mở PR #129 cho `ops/master-ac19-viet-lai-rebase` → `master`.

## Đường SAI — và vì sao nó đánh lừa

```bash
curl https://api.github.com/repos/<owner>/<repo>       # HTTP 403
```

Thân phản hồi:

```json
{"message":"GitHub access is not enabled for this session.
            An org admin must connect the Claude GitHub App for this organization."}
```

**Ba cái bẫy nằm trong đúng thông điệp này:**

1. Nó trả **403 kể cả khi KHÔNG gửi token**, nên trông y hệt một lệnh cấm ở tầng mạng.
2. Nó **gợi ý một cách chữa** ("nhờ admin kết nối Claude GitHub App") — cách ấy ĐÃ THỬ và
   KHÔNG được. Làm theo là đi vào ngõ cụt đã biết.
3. Nó **không nhắc gì** tới `api.githubcopilot.com`, là đường thật sự chạy.

Và proxy KHÔNG hề chặn — đo được: `curl https://api.github.com` (gốc) trả **200**,
`recentRelayFailures` của proxy **rỗng**. Nên đổ cho proxy cũng sai.

## Hai host, đừng lẫn

| host | trạng thái | dùng cho |
|---|---|---|
| `api.github.com` | **403**, ngõ cụt | không dùng |
| `api.githubcopilot.com/mcp/` | **200** với `GITHUB_PAT` | MỌI việc GitHub |

Khác nhau đúng một chữ trong tên miền. Đó là tất cả.

## Câu trả lời đã nằm sẵn trong kho từ 14-08

`ops/prompts/wp55-r2-review-4-codex-20260814.md`, nguyên văn:

> - `gh` KHONG co san.
> - api.github.com tra 403 o tang PROXY — 403 ca khi khong gui token. Token tot hay
>   xau khong cuu duoc duong nay; **dung mat thi gio thay token.**
> - **api.githubcopilot.com/mcp/ (GitHub MCP Server chinh thuc) CHAY**: initialize tra
>   HTTP 200 voi `Authorization: Bearer $GITHUB_PAT`, va 401 khi khong token.
> Nen: doc PR/issue va dang verdict bang cong cu MCP github.

Tôi đọc **vế đầu** (api.github.com 403) và bỏ **vế sau** (đường thay thế) — hai vế nằm cạnh
nhau, cách nhau một dòng.

## Cái giá phải trả

Cả một ngày làm việc dựa trên giả định "GitHub API bị chặn":

- mọi lease, mọi prompt đều dựng quanh cầu git→workflow như đường DUY NHẤT;
- handoff §7 ghi "GitHub blocked" như một sự thật;
- khuyên chủ kho đi hỏi admin bật GitHub App — **đúng cách đã thử và thất bại**, tức là
  lặp lại một sai lầm đã được sửa;
- không mở được PR, không đọc được verdict trên PR, không đăng được comment — trong khi cả
  ba đều làm được.

Cầu git→workflow (`ops-publish-lease.yml`, `ops-open-pr.yml`) vẫn tốt và vẫn nên giữ: nó
chạy được ngay cả khi phiên KHÔNG có `GITHUB_PAT`. Nhưng nó là **đường dự phòng**, không
phải đường duy nhất, và tôi đã coi nó là duy nhất.

---

## CHỐT — dán vào BƯỚC 0 của mọi phiên chạm GitHub

```bash
# 1. Có PAT không?
[ -n "${GITHUB_PAT:-}" ] && echo "PAT: có, ${#GITHUB_PAT} ký tự" || echo "PAT: CHƯA ĐẶT"

# 2. MCP chính thức có chạy không? ĐÒI 200.
curl -sS -o /dev/null -w 'MCP github: HTTP %{http_code}\n' \
  -X POST https://api.githubcopilot.com/mcp/ \
  -H "Authorization: Bearer $GITHUB_PAT" -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"p","version":"1"}}}'
```

**200 ⇒ dùng MCP cho mọi việc GitHub. Đừng đụng `api.github.com`. Đừng đi hỏi admin.**

Chỉ khi bước 2 KHÔNG ra 200 thì mới lùi về cầu git→workflow, và phải **báo con số đo được**
chứ không báo "GitHub bị chặn".

## Ba quy tắc rút ra, rộng hơn chuyện GitHub

**1. Một thông điệp lỗi có thể vừa THẬT vừa LẠC HƯỚNG.** *"GitHub access is not enabled"*
đúng về `api.github.com` và vô nghĩa với `api.githubcopilot.com`. Cách chữa nó gợi ý là
cách đã thất bại. Đọc thông điệp để biết **cái gì hỏng**, đừng nhận luôn **cách nó bảo
chữa**.

**2. Khi tài liệu nói "X không chạy", đọc tiếp câu sau.** Người viết tài liệu hầu như luôn
ghi kèm đường thay thế — họ vừa mới đi qua nó. Dừng ở câu đầu là bỏ đúng phần có giá trị.

**3. In phản hồi THÔ trước, phân tích sau.** Lời gọi `create_pull_request` đầu tiên ĐÃ tạo
PR thành công, nhưng trình phân tích của tôi nuốt kết quả và in `PR #None`. Tôi gọi lại và
nhận `422 already exists`. Suýt nữa kết luận "MCP không tạo được PR". Với một API lần đầu
dùng, `head -c 700` phản hồi thô rẻ hơn nhiều so với một kết luận sai.

## Đây là lần thứ BA cùng một lớp lỗi trong một phiên

| lần | tôi kết luận | sự thật | ai chỉnh |
|---|---|---|---|
| 1 | "không gọi được codex" | codex cài được, chạy được, tìm ra P1 thật | chủ kho |
| 2 | "`launcher.py` bị thiếu" | nhánh ghim base cũ hơn commit thêm nó | chủ kho |
| 3 | "GitHub API bị chặn" | sai host; MCP chính thức chạy tốt | chủ kho |

Cùng một hình dạng cả ba lần: **kết luận từ tài liệu hoặc từ một phép đo hẹp, thay vì đo
đúng thứ cần đo.** Và cả ba lần đều mất thời gian của chủ kho để chỉnh lại.

> Trước khi báo "X không dùng được", phải trả lời được: **tôi đã đo ĐÚNG X chưa, hay đo một
> thứ gần giống X?**
