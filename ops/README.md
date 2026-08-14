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
| `granted_by` **không nằm trong** `NGUOI_CO_THAM_QUYEN`, hoặc `GITHUB_ACTOR` không có thẩm quyền | `4` |
| lease đã hết hạn, hoặc hạn thiếu múi giờ | `8` |
| `reviewed_sha_required` không phải 40 hex thường | `8` |
| thiếu trường bắt buộc, `packet_issue` không phải số, YAML hỏng | `8` |
| đã đăng rồi (`posted_comment_id`) — **bỏ qua**, không phải lỗi | `9` |
| mỏ neo prompt hỏng: thiếu `prompt_path`, tệp không có, đường dẫn ra ngoài kho, hoặc **băm lệch** | `6` |

`ops/lease_publish_test.py` giữ 27 ca cho những chốt đó, và **workflow chạy chính
bộ test ấy trước mỗi lượt đăng** — rẻ hơn nhiều so với một lần đăng sai.

### Mỏ neo prompt (`prompt_path` + `prompt_sha256_required`)

Lease nào neo prompt thì phải khai **cả hai** trường, đi thành đôi. Một con băm không
kèm địa chỉ thì không kiểm được — nó chỉ là niềm tin viết dưới dạng hex; một địa chỉ
không kèm băm thì tệp đổi lúc nào cũng không ai hay.

Chốt này sinh ra từ một sự cố đã trả giá. Lease #3 của wp55 ghi
`prompt_sha256_required: 46a833cc…` mà không nói băm **cái gì**, và không văn bản nào
ứng với con băm ấy — đã quét 294.578 cửa sổ 5292-byte trên toàn bộ comment #54+#55 và
941 blob của ba nhánh, 0 khớp. Cổng `--expected-prompt-sha256` phía reviewer vì thế
không ai qua được, mà nó hỏng **im lặng**: lease hợp lệ, hạn còn, chỉ thiếu đúng cái
vật nó trỏ tới. wp55 đứng im hai ngày.

Kèm theo là một quy ước về **chỗ để prompt**: prompt là một **tệp** trong
`ops/prompts/`, không phải một khối trong comment. Một khối trong `<details>` có ít
nhất 12 cách cắt hợp lý (kèm/không thẻ, kèm/không `<summary>`, ruột fence, có/không
`strip`, CRLF/LF) — mỗi cách một băm khác nhau, nên "băm khớp" không có nghĩa xác
định. `sha256sum <tệp>` chỉ có một câu trả lời.

Ba chi tiết cài đặt đã đo, đừng "dọn" nhầm:

- Băm đọc **byte** (`read_bytes`), không đọc văn bản. `read_text` chuẩn hoá xuống dòng
  nên cùng một tệp cho hai băm khác nhau tuỳ nền — xanh ở Linux, đỏ ở Windows.
- `prompt_path` là dữ liệu YAML mà lại thành một lượt **đọc đĩa**, nên có hai lớp chặn
  đường ra: lọc dạng đường dẫn (tuyệt đối, `..`, dấu `\`) trước khi chạm hệ tệp, rồi
  `relative_to` sau `resolve()`. Đã đo bằng đột biến: bỏ lớp nào thì lớp kia vẫn trả
  đúng `6` — **hai lớp chồng nhau về mã thoát**, chỉ khác thông điệp. Lớp bắt được
  symlink (đường dẫn sạch về mặt chuỗi) là `relative_to`. Vì thế phản chứng neo
  **thông điệp** chứ không chỉ mã thoát; neo mỗi mã thì đột biến gỡ một lớp sống sót
  và bộ test nói dối rằng nó có đo lớp ấy.
- Chốt `9` (đã đăng rồi) chạy **trước**, nên với lease đã đăng thì `check` không kiểm
  mỏ neo nữa. Thứ canh lease thật là ca `t23`, và nó nằm trong bộ test mà workflow
  chạy trước mỗi lượt đăng — đổi một byte trong `ops/prompts/**` là đỏ.

Luật `granted_by` cố ý trùng với `.claude/dev/packet_loop.py record-lease`: cùng một
doctrine ("không tự cấp lease") được cưỡng chế ở hai tầng độc lập — một tầng lúc chạy
máy trạng thái, một tầng ở cửa đăng. Tầng nào thủng thì tầng kia còn đỡ.

### Danh sách CẤM không bao giờ đủ — bài học `lease-authority-spoof`

Bản đầu chỉ từ chối **đúng hai chuỗi** `claude` và `codex`. Cross-review lượt 4 (codex,
14-08-2026) tái hiện được: `codex-dispatcher`, `ai-codex-bot`, `cödex` đều `rc=0`, cấp
được lease rồi mở lượt. Nguyên văn kết luận — *"distinguishes spelling, not authority"*:
chốt phân biệt **cách viết**, không phân biệt **thẩm quyền**. Lỗ không bị bịt, nó chỉ
chuyển chỗ từ `init` sang `record-lease`.

Đắng hơn: prompt do chính phiên soạn cho reviewer **liệt kê `codex-dispatcher` làm
hướng tấn công số 1**, rồi cổng vẫn thua đúng ca đó. Nghĩ ra được phép thử mà không
chạy nó thì phép thử ấy không tồn tại.

Nay đảo chiều: `NGUOI_CO_THAM_QUYEN` là danh sách **CHO PHÉP**. Danh sách cấm phải đoán
trước mọi cách viết của kẻ gian — thua từ trong thiết kế; danh sách cho phép chỉ phải
liệt kê một tập nhỏ và biết trước.

**Nói thẳng giới hạn**, đừng đọc rộng hơn thực tế: danh sách chứng minh cái *tên* được
phép cấp lease, **không** chứng minh đúng người đó đã gõ. Thứ thật sự neo là hai thứ
khác — sửa danh sách phải qua một commit có review, và chốt `GITHUB_ACTOR` (danh tính
do GitHub xác thực; kẻ soạn tệp YAML đặt được `granted_by` nhưng không đặt được biến
đó). Chốt `GITHUB_ACTOR` chỉ áp khi biến có mặt, tức khi chạy trong Actions — chạy tay
ở máy thì lớp ấy vắng, và nói vậy còn hơn giả vờ có.

## Ba chỗ đã cân nhắc, ghi lại để khỏi "sửa" nhầm

**Chốt chống lặp nằm ở `if:` mức job, KHÔNG nằm trong thông điệp commit.** Bước ghi
ngược chạm đúng đường dẫn workflow theo dõi nên về nguyên tắc tự kích hoạt lại. Bản
đầu chặn bằng dấu bỏ-qua-CI trong commit — **sai chỗ**: dấu ấy sống trong lịch sử, và
khi commit ghi ngược thành HEAD của một PR thì nó tắt luôn gate của PR đó (đụng thật
ở PR #100: `0` check run mà PR vẫn hiện `clean`). Nay chống lặp là `if:` bỏ qua khi
head commit do `github-actions[bot]` tạo. Kể cả chốt ấy thủng cũng không thành vòng
lặp: push bằng `GITHUB_TOKEN` vốn không sinh lượt chạy mới, và chốt idempotent `rc=9`
dừng sau đúng một vòng. Ca `t24` cấm mọi workflow nhét dấu ấy vào `git commit`.

**Không dùng `pull_request_target`.** Nó chạy code của nhánh đích với token ghi.

**Phút Actions.** r245 đã đo: Free 2.000 phút/tháng bị đốt ~8.100 nên CI từng chết hẳn
từ 12-08 19:30. Hai workflow ở đây chạy `ubuntu-latest` (hệ số 1×), vài giây, không
matrix — nhiễu không đáng kể so với gate Windows ~20 phút/lượt. `ops-open-pr` còn lọc
`[open-pr]` ngay ở mức `job.if` nên lượt không khớp **không tốn runner**.

## Chưa được nghiệm thu

Phần logic (`lease_publish.py`) có 27 ca phản chứng và đã chạy thử trọn vòng bằng một
`gh` giả: tìm tệp → cổng → dựng thân → đăng → ghi ngược → chạy lại ra `9`. Sáu đột
biến (chạy trên **bản sao tạm**, không đụng tệp thật) giết đúng ca đích của từng cái,
kể cả hai ca mà lượt đo đầu cho thấy bộ test **không** thật sự đo — xem mục mỏ neo
prompt ở trên.

**Nhưng chưa lượt nào chạy thật trên Actions.** Workflow chỉ kích hoạt sau khi có mặt
ở nhánh được push, và lượt đầu tiên cần người xem kết quả. Đúng bài học "script đa nền
phải chạy THẬT trên nền đó" — cho tới lúc đó, đường này coi như **chưa được đo**.
