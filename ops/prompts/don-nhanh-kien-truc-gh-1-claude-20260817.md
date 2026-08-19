# Lượt XÉT LẠI KIẾN TRÚC — cách `don-nhanh.ps1` đọc danh sách PR đang mở

Bạn là REVIEWER/KIẾN TRÚC, provider **`claude`** — **cùng nhà cung cấp với người vá**.
**CHỈ ĐỌC**: không sửa tệp trong kho, không commit, không push. Thử nghiệm chạy trên bản
sao tạm hoặc thư mục scratch.

## LƯỢT NÀY KHÔNG PHẢI LƯỢT DUYỆT

Đây **không** phải review để land. Nó trả lời đúng một câu **thiết kế**:

> Cách đọc danh sách PR đang mở của `don-nhanh.ps1` có nên **đổi kiến trúc** không, và
> nếu có thì đổi sang cái gì?

`assurance` của lượt này là `same_provider_approved` và nó **không** cấp điều kiện land cho
PR #150. Đừng viết gì hàm ý ngược lại.

## Vì sao có lượt này — ĐẾM HÌNH DẠNG LỖI, KHÔNG ĐẾM LỖI

**Ba lượt cross-review liên tiếp, ba finding, CÙNG MỘT HÀM** — hàm đọc `gh`:

| lượt | reviewer | finding | lớp lỗi |
|---|---|---|---|
| 1 | codex | `gh` thoát khác 0 mà in JSON hợp lệ ⇒ fail-close mở toang, **xoá thật** | mã thoát bị bỏ qua |
| 2 | codex | `2>&1` trộn stderr vào JSON ⇒ thao tác hợp lệ **bị từ chối oan** | hai luồng gộp làm một |
| 3 | claude | đếm **số dòng thô** thay vì **nội dung đã tách** vẫn qua bộ test ⇒ đột biến sống sót | rỗng-vs-vắng |

`CLAUDE.md`, mục "BẢY phát hiện cùng MỘT đường":

> *Mỗi lượt vá bảo toàn được thứ ta NGHĨ TỚI và làm hỏng thứ ta KHÔNG NGHĨ TỚI. Vá tiếp lúc
> nào cũng có vẻ đúng vì lần nào cũng có lỗi thật — đó chính là cách người ta ở lại quá lâu
> trong một cái hố. **Đếm hình dạng lỗi, đừng chỉ đếm lỗi**: cùng một hình dạng lặp ba lần
> trở lên thì câu hỏi đúng là "có nên làm việc này không", không phải "vá thế nào".*

Ba lần rồi. Đây là lượt đặt câu hỏi ấy.

**Hình dạng chung của cả ba:** không cái nào là lỗi *logic nghiệp vụ*. Cả ba đều ở **kênh
đọc đầu ra của một tiến trình con** — mã thoát, trộn luồng, phân biệt rỗng/vắng. Nghiệp vụ
("giữ head và base của PR đang mở") chưa bao giờ sai.

## Ba phương án, và PHÉP ĐO đã chạy sẵn cho bạn

Người vá đã đo trong container này (17-08, `GITHUB_PAT` dài 93):

```
REST  https://api.github.com/rate_limit                      -> HTTP 200, 4 header X-GitHub-*
REST  https://api.github.com/repos/ducthangho/tra-luat       -> HTTP 403, 0 header X-GitHub-*
REST  .../repos/ducthangho/tra-luat/pulls?state=open         -> HTTP 403, 0 header X-GitHub-*
      than 403: "GitHub access is not enabled for this session..."
MCP   POST https://api.githubcopilot.com/mcp/  initialize    -> HTTP 200, co Mcp-Session-Id
MCP   tools/call list_pull_requests (owner/repo/state=open)  -> 11 PR, DU ca head lan base
```

**403 với 0 header `X-GitHub-*` = proxy container tự sinh, chưa từng tới GitHub.** Đây là
chữ ký đã ghi trong `CLAUDE.md`.

### A. Giữ `gh` (hiện trạng)

### B. REST thẳng `api.github.com` (`Invoke-RestMethod` / `curl`)

### C. JSON-RPC tới MCP endpoint bằng `GITHUB_PAT`

## SÁU câu, tất cả ĐO ĐƯỢC — đừng trả lời bằng ý kiến

**1. BẤT ĐỐI XỨNG MÔI TRƯỜNG — câu dễ kết luận sai nhất.** `don-nhanh.ps1` chạy trên **máy
Windows của chủ kho**, KHÔNG chạy trong container này. `403` ở trên là chính sách proxy của
container. Hỏi: phương án nào tốt hơn ở **máy người dùng**, và phương án nào tốt hơn ở
**container/CI**? Có phải chúng KHÁC NHAU không? Nếu có, chọn theo nơi script THẬT SỰ chạy,
đừng chọn theo nơi bạn đang đứng. `CLAUDE.md`: *"một công cụ thất bại chưa phải một đường bị
chặn"* — và ngược lại, một đường chạy được ở đây chưa phải đường đúng cho họ.

**2. MCP có thật sự BỚT lớp không, hay chỉ ĐỔI lớp?** Đo cụ thể: một phản hồi MCP đi qua
mấy lớp giải mã trước khi ra `baseRefName`? Người vá đếm được **HTTP → SSE (`data:`) →
`content[0].text` (chuỗi) → JSON** = ba lớp, cộng bắt tay `initialize` + `Mcp-Session-Id`.
Còn `gh pr list --json` là **một** lớp. Nếu MCP nhiều lớp hơn thì nó **dời** chỗ hỏng chứ
không **đóng** lớp hỏng — đúng thứ `CLAUDE.md` gọi là *"bản vá đầu tiên chỉ DỜI vấn đề sang
một tệp ít người mở hơn"*.

**3. `isError` VẮNG MẶT.** Lời gọi thành công trả `isError: None` — trường ấy **không có**.
Ai viết `if ($r.isError)` sẽ đọc "vắng" thành "không lỗi". So sánh thẳng với lỗi lượt 1
(`rc=0` nói dối) và với doctrine `None ≠ False`. **Phương án C có tái tạo đúng lớp lỗi mà
nó được đề xuất để chữa không?** Dựng phép thử: gọi MCP với `owner`/`repo` sai, xem trường
nào xuất hiện, và một client ngây thơ sẽ hiểu thành gì.

**4. Ranh giới credential.** Hiện `don-nhanh.ps1` **không đọc token nào** — nó dựa vào
`gh` đã đăng nhập sẵn. B và C đều đòi token trong môi trường script. `CLAUDE.md` có mục cấm
đọc secrets ngoài quy trình, và có bài học `inherit = "all"` bị thu hồi vì *"đổi MỘT
credential lấy CẢ MÔI TRƯỜNG"*. Hỏi: đưa `GITHUB_PAT` vào một script XOÁ NHÁNH là được hay
mất? Trả lời bằng phạm vi quyền cụ thể, không bằng cảm giác.

**5. Fail-close còn giữ được không.** Bất biến hiện tại: **không đọc được danh sách PR ⇒
TỪ CHỐI XOÁ (rc=13)**. Với B và C, "không đọc được" có bao nhiêu hình dạng mới (timeout, 5xx,
SSE đứt giữa chừng, session hết hạn, phân trang thiếu)? Liệt kê, rồi nói mỗi hình dạng sẽ
rơi vào nhánh nào. **Một hình dạng rơi vào nhánh "coi như không có PR" là một lỗ y hệt lượt
1.** Chú ý riêng: MCP `list_pull_requests` có **phân trang** — đọc thiếu trang cuối ra một
danh sách PR NGẮN HƠN thực tế, tức giữ hụt base, tức xoá nhầm. `gh pr list --limit 200` có
cùng vấn đề ở ngưỡng khác.

**6. KẾT LUẬN "GIỮ NGUYÊN" LÀ HỢP LỆ.** Nếu bằng chứng nói ba lỗi kia là hình dạng **đã
đóng hết** (mã thoát ✓, tách luồng ✓, rỗng-vs-vắng ✓) và không còn hình dạng thứ tư nào
trong cùng kênh, thì "giữ `gh`" là câu trả lời đúng và bạn nên nói thẳng. Đừng đề xuất đổi
kiến trúc chỉ vì lượt này tên là "xét lại kiến trúc" — đó là thiên kiến của chính cái khung
câu hỏi. Nhưng nếu bạn giữ `gh`, hãy nêu **hình dạng thứ tư** mà bạn đã tìm và loại trừ
được, để kết luận ấy có răng.

## Ràng buộc cho mọi đề xuất

- Phải chạy trên **Windows PowerShell 5.1 lẫn pwsh 7+** (`.cmd` bọc ưu tiên pwsh, nhưng 5.1
  là đường lùi và **chưa được kiểm**).
- Không được làm mất bất biến fail-close.
- Phải nêu **bộ test đi kèm** trông thế nào — phương án nào khó dựng đồ giả TRẠNG THÁI hơn
  thì đắt hơn, vì kho này đã trả giá cho đồ giả diễn KỊCH BẢN.
- Nếu đề xuất đổi: nêu **đường di trú**, và nói rõ nó có làm hỏng `-BoQuaLopPR` / bảng mã
  thoát trong `.cmd` không.

## Định dạng trả lời

```
verdict: giu_nguyen | doi_kien_truc | doi_co_dieu_kien
assurance: same_provider_approved

## Khuyến nghị

Một đoạn. Chọn A/B/C (hoặc kết hợp), nói rõ CHO NỀN NÀO.

## Bằng chứng

Mỗi khuyến nghị neo vào một phép đo ĐÃ CHẠY. Mục không chạy được ⇒ KHÔNG ĐO ĐƯỢC.

## Hình dạng lỗi thứ tư

Có hay không, và bạn đã thử gì để tìm.

## Nợ khai báo

## Phép đo đã chạy
```

Nguồn có thẩm quyền là tệp lease trên **đầu nhánh**:
`git show origin/ops/don-nhanh-giu-base-pr:ops/leases/don-nhanh-kien-truc-gh-1-claude-20260817.yaml`
— lease trong cây bạn checkout là bản của lượt TRƯỚC.
