# `ops/` — thao tác GitHub bằng git

## Vấn đề

Git chạm tới được commit, nhánh, tag, `refs/pull/N/head`, `git notes` — tức toàn bộ
phần **mã**. Git **không** chạm tới được issue, comment, PR, review, label,
check-run: đó là cơ sở dữ liệu riêng của GitHub, không phải object trong git, và
không có lệnh git nào tạo ra chúng. GitHub cũng không có push-option kiểu
`-o merge_request.create` như GitLab.

Điều đó thành vấn đề vì **quyền API gắn theo xuất xứ phiên**. Đo 13/14-08-2026 trên
20+ phiên cùng một `environment_id`: phiên `origin: desktop_app`/`android` gọi được
`api.github.com`; phiên `origin: claude_code_mcp_seed` nhận `403` ở mọi lời gọi —
trong khi clone/fetch/push đều chạy bình thường ở cả hai. Nên bất cứ quy trình nào
điều phối qua API đều có phiên làm được, phiên không.

## Cách chữa: git là đường vận chuyển

```
git push  →  Actions kích hoạt  →  workflow dùng GITHUB_TOKEN gọi API  →  comment/PR
```

Phiên chạy chỉ cần quyền **git**. Không phiên nào cần API nữa.

Kèm theo một lợi ích lớn hơn cả việc gỡ tắc: **lease sống trong kho**. Nó diff được,
review được, không mất theo container, và không phụ thuộc vào việc ai đó còn đọc
được một comment. Comment trên issue trở thành **bản chiếu**, không còn là nguồn sự
thật. Cùng bài học với "prompt reviewer phải commit vào kho", chỉ tổng quát hơn.

## Dùng

```bash
# 1. soạn lease
cp ops/leases/wp55-r2-review-3-codex-20260814.yaml ops/leases/<lease-id>.yaml
$EDITOR ops/leases/<lease-id>.yaml

# 2. tự kiểm TRƯỚC khi push — cùng cổng mà workflow sẽ chạy
python3 ops/lease_publish.py check ops/leases/<lease-id>.yaml
python3 ops/lease_publish.py body  ops/leases/<lease-id>.yaml   # xem trước thân comment

# 3. push lên nhánh ops/** → workflow đăng và ghi ngược posted_comment_id
git checkout -b ops/lease-<lease-id>
git add ops/leases && git commit -m "ops: lease <lease-id>"
git push -u origin ops/lease-<lease-id>
```

Mở PR cũng đi đường này: thêm `[open-pr]` vào thông điệp commit khi push một nhánh
`claude/**` hoặc `ops/**`.

## Cổng chặn — và vì sao nó nghiêm

Workflow chạy bằng `GITHUB_TOKEN`, nghĩa là **push được thành đăng được**. Thứ duy
nhất đứng giữa một tệp YAML trong kho và một comment mang danh nghĩa kho là
`ops/lease_publish.py`. Nó chặn:

| Ca | Mã |
|---|---|
| `granted_by` mang tên một provider (`claude`/`codex`) — agent tự cấp cho mình | `4` |
| lease đã hết hạn, hoặc hạn thiếu múi giờ | `8` |
| `reviewed_sha_required` không phải 40 hex thường | `8` |
| thiếu trường bắt buộc, `packet_issue` không phải số, YAML hỏng | `8` |
| đã đăng rồi (`posted_comment_id`) — **bỏ qua**, không phải lỗi | `9` |

`ops/lease_publish_test.py` giữ 13 ca cho những chốt đó, và **workflow chạy chính
bộ test ấy trước mỗi lượt đăng** — rẻ hơn nhiều so với một lần đăng sai.

Luật `granted_by` cố ý trùng với `.claude/dev/packet_loop.py record-lease`: cùng một
doctrine ("không tự cấp lease") được cưỡng chế ở hai tầng độc lập — một tầng lúc chạy
máy trạng thái, một tầng ở cửa đăng. Tầng nào thủng thì tầng kia còn đỡ.

## Ba chỗ đã cân nhắc, ghi lại để khỏi "sửa" nhầm

**`[skip ci]` trong commit ghi ngược là bắt buộc.** Bước đó ghi vào đúng đường dẫn mà
workflow đang theo dõi; bỏ nó ra là mỗi lượt đăng tự kích hoạt thêm một lượt nữa.
Chốt idempotent giữ cho không đăng trùng, nhưng vẫn đốt phút.

**Không dùng `pull_request_target`.** Nó chạy code của nhánh đích với token ghi.

**Phút Actions.** r245 đã đo: Free 2.000 phút/tháng bị đốt ~8.100 nên CI từng chết hẳn
từ 12-08 19:30. Hai workflow ở đây chạy `ubuntu-latest` (hệ số 1×), vài giây, không
matrix — nhiễu không đáng kể so với gate Windows ~20 phút/lượt. `ops-open-pr` còn lọc
`[open-pr]` ngay ở mức `job.if` nên lượt không khớp **không tốn runner**.

## Chưa được nghiệm thu

Phần logic (`lease_publish.py`) có 13 ca phản chứng và đã chạy thử trọn vòng bằng một
`gh` giả: tìm tệp → cổng → dựng thân → đăng → ghi ngược → chạy lại ra `9`.

**Nhưng chưa lượt nào chạy thật trên Actions.** Workflow chỉ kích hoạt sau khi có mặt
ở nhánh được push, và lượt đầu tiên cần người xem kết quả. Đúng bài học "script đa nền
phải chạy THẬT trên nền đó" — cho tới lúc đó, đường này coi như **chưa được đo**.
