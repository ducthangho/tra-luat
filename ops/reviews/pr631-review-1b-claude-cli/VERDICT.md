verdict: changes_requested
reviewed_sha: af5edd354d414999eb8355f8dc4d799958f08aca
P1: 1   P2: 4   P3: 3
reviewer_provider: anthropic_claude
model_tu_khai: claude-opus-5-5 (Opus 5.5)
execution_surface_tu_khai: Claude Code CLI (Agent SDK) trong container Linux 6.18.44-fc-v50 x86_64 · Python 3.11.15 · curl 8.5.0 · git 2.43.0 · KHÔNG có `gh` · có `codex` (/opt/node22/bin/codex) · HTTPS ra ngoài qua proxy cục bộ 127.0.0.1:40613 (README của proxy ghi TLS tái kết thúc ở egress — tài liệu, không phải phép đo) · GITHUB_PAT đặt (93 ký tự), GH_TOKEN/GITHUB_TOKEN 14 ký tự · phiên KHÔNG có công cụ MCP github · đo 2026-09-30T06:07Z–06:23Z

Lượt 1b, `advisory_review`: cùng provider với bên soạn (Anthropic), nên đây là ý kiến tư vấn,
không thay được một lượt review khác provider. Cây đã review: `cay-kho` tại `af5edd3`. `CLAUDE.md`
ở đó trùng từng byte với head PR `bc5b7f6` (`git diff --quiet bc5b7f6 af5edd3 -- CLAUDE.md`). REST
lúc 06:16Z vẫn trả head `bc5b7f69…`, PR đang mở. `DIFF.patch` trùng `git diff c16bec6 af5edd3`
(+22/−2).

## Findings

`HINT.patch` phủ cả tám finding: 5 hunk, +56/−20, chỉ sửa `CLAUDE.md`. `patch -p0 --dry-run` trên
bản sao trong `scratch/thu/` cho rc=0. Áp xong thì khớp từng byte với `scratch/sau/CLAUDE.md`. Dòng
140 (có chuỗi thoát ASCII `̈`) giữ nguyên byte.
**Trước khi áp:** hint cũng ghi vào `CLAUDE.md`, nên executor phải chạy `ai-dang-giu CLAUDE.md`
trước (xem comment PR 5825817421). REST cho thấy #579 `closed` lúc 2026-09-27T17:45Z. Còn lease nào
khác đang giữ tệp thì tôi KHÔNG ĐO.

### F1 · P1 · `khai-vang-mat-khong-do` · `CLAUDE.md:148-149`
**Lời khai:** *"comment của lượt 22-08 không còn để thử lại, ca ấy ở nguyên **KHÔNG ĐO ĐƯỢC**. Đừng
đọc thành "đã bắt được MCP bóp méo" — chưa ai đo được điều đó."*

**SAI.** Chính `CLAUDE.md:129` gọi tên ca này là "comment lease `#238`". Cả 7 comment lease trên
#238 vẫn còn, chưa ai sửa, và REST đọc được chúng.
```
rg -c posted_comment_id cay-kho/ops/leases/lease-dang-windows-*-20260822.yaml | wc -l      # 7
curl -sS -H 'Accept: application/vnd.github+json' \
  'https://api.github.com/repos/ducthangho/tra-luat/issues/238/comments?per_page=100' \
  | python3 -c 'import sys,json,re;[print(c["id"],c["user"]["login"],c["created_at"]==c["updated_at"],c["body"].count(chr(39)),len(re.findall(r"&(#\d+|#[xX][0-9a-fA-F]+|[A-Za-z]\w*);",c["body"]))) for c in json.load(sys.stdin)]'
```
Kết quả đo lúc 2026-09-30T06:09Z và đo lại lúc 06:23Z:
- #238 có 9 comment. **7/7** `posted_comment_id` đều có mặt, tác giả `github-actions[bot]`, tạo
  2026-08-22T05:52:23Z → 10:31:25Z.
- Cả 7 comment có `updated_at == created_at`.
- Số `'` thật lần lượt là 22/33/14/49/34/33/19.
- Không có **thực thể HTML nào** (tính mọi dạng `&…;`), và cũng **không có dấu `&` nào**.
- `curl` và `urllib` cho thân comment khớp từng byte (thử trên 5378293440 và 5379124290).

Tức là ca 22-08 **đo được, và đã đo**. Byte GitHub lưu cho các comment ấy là ký tự thật, và chúng
chưa hề bị sửa kể từ 22-08. Vậy `&#39;` mà lượt 22-08 thấy phải sinh ra trên **đường ĐỌC MCP** lúc
đó. Giới hạn của kết luận này nằm ở mục KHÔNG ĐO ĐƯỢC. Lời khai này trái với chính luật của tệp:
`:202` ("không đo được không phải không có") và `:184-186` ("nếu thứ tôi đang tìm CÓ THẬT thì nó
được ghi ở đâu?"). Chỗ ghi ấy chính là `posted_comment_id`, nằm ngay trong kho. Đây là lời khai vắng
mặt không kèm phép đo nào, viết vào doctrine, và nó làm người sau không đo lại một câu hỏi vốn đã
trả lời được.

**Sửa:** hunk 1 của `HINT.patch`. Ghi rằng ca cũ vẫn còn và đã đo, bỏ câu "chưa ai đo được", và
khai rõ giới hạn (xem mục KHÔNG ĐO ĐƯỢC).

### F2 · P2 · `trang-thai-cu-khong-danh-dau` · `CLAUDE.md:620-624`, `:629-632`, `:670-671` (nhãn mơ hồ ở `:637`)
Nhãn mới *"HAI DÒNG 403 Ở TRÊN ĐÃ TRÔI"* không nói là hai dòng nào. `rg -n 403 CLAUDE.md` cho
`548 549 551 620 622 627 632 637 652 671`. Riêng trong mục REST, bỏ chính nhãn (`:637`) và câu
chuyện `CONNECT` (`:652`), còn **5 dòng** khai trạng thái 403: `:620`, `:622`, `:627`, `:632`,
`:671`. Dòng `:671` còn nằm **DƯỚI** nhãn, trong gạch `t103`, nên chữ "Ở TRÊN" không thể phủ tới nó.
Dòng `:551` thuộc mục khác, xem F3. Ba câu
kết luận dựa trên 403 vẫn đứng như trạng thái hiện tại, không có nhãn nào:
- `:623` — *"`gh` … **cài cũng vô ích** vì nó đi đúng đường bị chặn"*.
- `:623-624` — *"Việc của kho đi bằng **MCP github + git**, không bằng REST thẳng"*. Tiền đề của
  chỉ thị này là REST bị chặn, mà REST `/repos/…` nay trả 200 (xem Phép đo lại).
- `:629-632` — *"câu đúng … **'REST bị chặn ĐÚNG CHỖ làm việc'**"* và *"MỌI lệnh việc thật ăn
  403"*; thêm `:670-671` *"mọi thao tác kho trả 403"*.

PR nói *"đừng đọc mục này thành 'REST nay dùng thoải mái'"*, nhưng không nói chỉ thị ở `:624` còn
hiệu lực hay không, và nếu còn thì vì lý do gì. Người đọc hoặc tiếp tục né REST/`gh` vì một lý do
đã chết, hoặc tự bỏ chỉ thị khi chủ kho chưa quyết.

**Sửa:** hunk 3 thêm chú thích trạng thái cho gạch 15-08 và nói thẳng rằng chỉ thị đã mất lý do cũ,
còn giữ hay bỏ thì chưa có quyết định. Hunk 4 liệt kê MỌI câu 403. Hunk 5 thêm nhãn cho `:670-671`.

### F3 · P2 · `trang-thai-cu-khong-danh-dau` · `CLAUDE.md:551`
Câu *"`curl https://api.github.com` cũng 403"* (mục 16-08 "Đẩy ref từ phiên web") không được đánh
dấu. Đo lại:
```
curl -sS -D - https://api.github.com/ | tr -d '\r' | grep -iE '^(HTTP/|server:|x-github-|content-length:)|^\{'
```
Kết quả: `HTTP/1.1 200 OK` · `Content-Length: 2` · thân `{}` · **không có `Server: github.com`, không
có `X-GitHub-*`**. `urllib` cho cùng kết quả trên cả 3 vế token. Theo luật header của tệp (`:625`),
đây là proxy tự trả chứ không phải GitHub. Ai đo lại chỉ bằng mã trạng thái sẽ thấy 200 và kết luận
sai. Còn `/repos/<kho>/…` thì trả 200 CÓ `X-GitHub-*`, dưới một danh tính bị thay giữa đường (F6).

Chỗ đáng lo nhất là mục này chứa một **tuyên bố an toàn**: *"Phiên web KHÔNG xoá được ref"*. Tuyên bố
ấy mới được đo cho `git-receive-pack`. Qua REST (`DELETE /git/refs/…`), với một danh tính đã được
cấp sẵn, thì KHÔNG ĐO ĐƯỢC: lượt này chỉ được GET, và đó cũng là thao tác phá. PR mở "REST đã thông"
nhưng không nhắc tới mục này.

**Sửa:** hunk 2 đánh dấu dòng 551 là đã trôi, ghi kết quả đo của `/`, và khai rằng đường GHI qua
REST là KHÔNG ĐO ĐƯỢC.

### F4 · P2 · `pham-vi-tuyen-bo-rong-hon-do` · `CLAUDE.md:637-641`, `:143-144`, `:150`
Các câu *"ĐÃ TRÔI"*, *"cùng container remote"*, **"Nền đã đổi, KHÔNG phải lượt cũ đo sai"**, *"NAY
CÓ … nên phép đo ấy làm được"* và *"đã có client thứ hai thật"* đều nói về nguyên nhân, hoặc phổ
quát hoá từ phép đo của một phiên. Thứ đo được thật chỉ là: phiên của tác giả (09-25) và phiên
review này (09-30) cho 200. Có ba dấu hiệu cho thấy trạng thái có thể gắn theo phiên, và không có
phép đo nào tách được "nền đổi cho mọi phiên" khỏi "cấu hình theo phiên":
- Thân 403 cũ mà tệp tự trích (`:621`) ghi *"GitHub access is not enabled **for this session**"*.
- Trong phiên này, credential mà GitHub thấy ở cả 5 vế mang
  `Github-Authentication-Token-Expiration: 2026-09-30 08:22:21 UTC`, tức hết hạn khoảng 2h14 sau lúc
  đo. Đó là credential ngắn hạn.
- Đường `/` vẫn do proxy tự trả (F3), tức tầng chính sách theo đường dẫn vẫn còn.

"Cùng container remote" cũng không thể là cùng container với 17-08, vì container gắn theo từng
phiên. Câu "không phải lượt cũ đo sai" thì có thể nói là *không có dấu hiệu* đo sai, vì 17-08 có
ghi header và 15-08 có ghi thân 403. Nhưng khẳng định **nguyên nhân** là rộng hơn phép đo, đúng loại
lời khai mà đề bài bảo phải ghi finding. Hậu quả: văn bản lặp lại đúng lỗi phạm vi đã làm dòng 17-08
trôi. Một phiên gặp lại 403 do proxy sẽ đọc "NAY CÓ", rồi nghi token của mình, đúng kiểu đi lạc mà
`:632-634` đã cảnh báo.

**Sửa:** hunk 1 và hunk 4: ghi "ở các phiên đã đo", viết "nguyên nhân KHÔNG ĐO ĐƯỢC", và nói rõ
`doctor` là nguồn trạng thái của từng phiên.

### F5 · P2 · `chan-doan-sai-vi-sao-troi` · `CLAUDE.md:648-649`
**Lời khai:** *"Mục này ghi ĐIỀU KIỆN ĐO (ngày · container · hai vế token) đúng vì lượt 17-08 không
ghi, nên nó trôi hơn một tháng mà không ai thấy."* **Sai so với chính tệp:**
`sed -n '618,636p' cay-kho/CLAUDE.md` cho thấy:
- 17-08 có ghi ngày: *"ĐO LẠI 17-08-2026"* (`:625`).
- 17-08 có ghi hai vế token: *"Chạy cả có token lẫn không token: kết quả Y HỆT"* (`:628`).
- Container được kế thừa từ gạch cha: *"Đo 15-08-2026 trong container remote"* (`:618-619`).
- 17-08 còn trỏ sẵn tới `doctor` (`:634-636`).

Chẩn đoán sai kéo theo thuốc sai: thứ PR coi là thuốc thì 17-08 đã làm rồi, mà dòng ấy vẫn trôi.
Nguyên nhân thật là một quan sát của MỘT phiên bị viết thành trạng thái chung, và không có gì đối
chiếu văn bản với phép đo sống. Văn bản mới của PR đang lặp lại đúng lỗi đó (F4).

**Sửa:** gạch cuối của hunk 4.

### F6 · P3 · `doi-chung-khong-rang` · `CLAUDE.md:638-639`, `:642-644`
Câu *"(đúng phép đối chứng hai chiều của lượt 17-08)"* và câu *"vế không token vẫn 200 ⇒ có tầng nào
đó **cấp** danh tính hộ"* chưa đúng hẳn. Tôi thêm một vế thứ ba là **token GIẢ**:
```
for a in "" "Authorization: Bearer khong-hop-le" "Authorization: token $GITHUB_PAT"; do
  curl -sS -D - -o /dev/null ${a:+-H "$a"} https://api.github.com/user | tr -d '\r' \
  | grep -iE '^(HTTP/1.1 [0-9]{3} [A-Z]|github-authentication-token-expiration)' | tr '\n' ' '; echo; done
```
Kết quả: 200 ở mọi vế, cùng `login`, cùng `Github-Authentication-Token-Expiration`. Phạm vi đo:
- `urllib`: mọi endpoint (`/rate_limit`, `/user`, `/repos` kho riêng, `/pulls/631`, `/pulls/623`,
  `/issues/comments/5811128755`), mỗi endpoint 3 vế: không token · `Bearer` thật · `Bearer` giả.
- `curl`: `/rate_limit`, `/user`, `/repos`, `/pulls/631`, mỗi endpoint 3 vế; riêng `/user` thì đo
  đủ 5 dạng (không token · `Bearer`/`token` thật · `Bearer`/`token` giả).

Nghĩa là header của người gọi bị **THAY**,
không chỉ được "cấp hộ" khi thiếu. Vì vậy hai vế có/không token chắc chắn phải "Y HỆT", và phép ấy
không đối chứng được gì (`:844`: "Một phép kiểm không thể đỏ thì không phải bằng chứng"). Hệ quả thực
hành mà PR ghi, "đừng dùng làm phép thử credential", vẫn đúng, nhưng còn nói nhẹ hơn thực tế. Giới
hạn: phép đo làm ở phiên 09-30. Phiên 09-25 có bị thay header không thì KHÔNG ĐO ĐƯỢC.

**Sửa:** gạch thứ hai của hunk 4, thêm vế token giả làm đối chứng thật.

### F7 · P3 · `pham-vi-tuyen-bo-rong-hon-do` · `CLAUDE.md:640`
Câu *"Máy đã đúng sẵn, chỉ VĂN BẢN cũ"* bỏ sót chỗ: văn bản cũ còn nằm ngay trong "máy".
```
rg -n 'CHẶN  403|MỌI lệnh việc thật|bi PROXY|khong dung duoc cho viec|không đọc nổi một|đường hai .chan.' \
  cay-kho/.claude/dev/launcher.py cay-kho/.claude/hooks/session-start.sh
```
Lệnh cho ra `launcher.py:3370` (docstring `_do_github`), `:3421`, `:3450`, `:3511`, `:3522`, và
`session-start.sh:196-199` (*"`gh` co cai cung khong dung duoc cho viec cua kho"*).

Phần "`doctor` in `rest-kho=OK`" thì khớp với code: `_do_rest_github` cho ok khi có `X-GitHub-*` và
mã 2xx, và `_nhan_duong` in ra `OK`. Hook có chạy `doctor --doi-kha-dung` (`session-start.sh:628`).
Nên với phép đo của tôi, `doctor` *sẽ* in `OK`. Đây là suy ra, tôi không chạy `doctor` (xem mục
KHÔNG ĐO ĐƯỢC). Còn "từ trước khi mục này được sửa" thì không có biên nhận nào trong kho: tìm
`rest-kho=OK` ngoài code cho 0 kết quả.

**Sửa:** cuối gạch đầu của hunk 4 nêu các chỗ ấy. Bản thân các tệp đó nằm ngoài write set của PR.

### F8 · P3 · `thieu-dieu-kien-do` · `CLAUDE.md:142`, `:146-147`
- Ở `:142`, câu "Lúc viết (22-08) container KHÔNG có" đã **mất** bằng chứng mà bản cũ có kèm (*"REST
  tới `repos/…` bị proxy chặn 403"*). Kết luận còn đó, căn cứ thì không.
- Ở `:146-147`, câu "hiện tượng 22-08 **KHÔNG TÁI LẬP**" có ba vấn đề. Nó không ghi công cụ MCP nào
  đã được dùng. Lượt 22-08 dùng `issue_read` · `list_issues` (`:134`). Và phép thử chạy trên một
  comment KHÁC ca 22-08, trong khi ca 22-08 vẫn còn (F1).

**Sửa:** hunk 1: trả lại căn cứ, và ghi phạm vi là "trên comment ấy". Công cụ MCP đã dùng vẫn chưa
có trong văn bản; executor cần điền.

## Phép đo lại

Hai client, `urllib` (`scratch/do_rest.py`) và `curl`, đo ba vế: không token, `GITHUB_PAT`, và token
giả. Chỉ dùng GET, không in token. Log thô nằm trong `scratch/`: `do_rest.log`, `do_rest.json`,
`do_rest_curl.log`, `do_user_exp.log`, `dem_5811128755.log`, `issue238_comments.log/json`, và
`comment_*.json|txt`.

| Lời khai (PR) | Đo 2026-09-30 | Kết quả |
|---|---|---|
| `/rate_limit` 200 CÓ `X-GitHub-*`, có/không token | 3 vế × 2 client | ✓ 200, 4 header `x-github-*` (có `request-id`) |
| `/user` như trên | như trên | ✓ 200 (`login` giống nhau ở MỌI vế) |
| `/repos/<kho>` như trên | như trên | ✓ 200; `private: true`, `visibility: private` |
| `/repos/<kho>/pulls/N` (#631; PR body dùng #623) | như trên | ✓ 200 cả hai (#631 open, head `bc5b7f69`) |
| "có/không token Y HỆT" | thêm vế token giả | ✓, nhưng token giả CŨNG y hệt ⇒ F6 |
| "vế không token vẫn 200 trên kho RIÊNG" | `/repos` → `private: true` | ✓ |
| 5811128755: 44 `'` · 8 `>` · 3 `<` · 0 thực thể (PR body: 2 `"`) | REST `urllib` + `curl` | ✓ 44 · 8 · 3 · 2 `"` · 0 thực thể · 0 `&`. Tác giả `github-actions[bot]`, trên #523; `created == updated` (2026-09-24T09:02:18Z); đúng là bản chiếu lease; sha256 thân `837f9c28…`; hai client khớp byte |
| "comment 22-08 không còn để thử lại" | GET `/issues/238/comments` | ✗ 7/7 vẫn còn, chưa sửa, ký tự thật ⇒ **F1** |
| (`:551`) "`curl https://api.github.com` cũng 403" | `curl` + `urllib` | ✗ 200 `{}` do proxy tự trả ⇒ **F3** |
| "đọc CHÍNH comment đó qua MCP cũng ra ký tự thật" | — | KHÔNG ĐO ĐƯỢC (xem dưới) |
| "`doctor` in `rest-kho=OK`" | đọc code + phép đo trên | khớp (suy ra, không chạy `doctor`) |
| (`:609-612`) GH_TOKEN/GITHUB_TOKEN là chuỗi giữ chỗ 14 ký tự | chỉ đo độ dài | khớp (14 · 14; GITHUB_PAT dài 93) |

## Cổng

Chạy trong `cay-kho` tại `af5edd3`, `core.abbrev=7`, `PYTHONDONTWRITEBYTECODE=1`. `git status
--porcelain --ignored` rỗng cả trước lẫn sau.

| Cổng | rc | Bằng chứng dương |
|---|---|---|
| `packet_loop.py doctrine-scan --root .` | **0** | sạch, quét 10 tệp, 0 chỗ chép |
| `packet_loop.py adr-song --root .` | **0** | 50 ADR / 50 dòng §20 (tha thiếu trạng thái `0016`) |
| `tl.py doc-claims-check --strict --json` | **0** | `ok=true`, `files_scanned=110` (có `CLAUDE.md` trong `roots`), `flags=0`, `advisory_count=381` |

Tôi cũng dựng hai clone trong CÙNG một lệnh (06:23Z): một clone nền, một clone đã áp `HINT.patch`.
Cả ba cổng **y hệt nhau** trên hai clone (log: `scratch/gate_nen_vs_hint.log`), nên delta của hint
bằng 0. Đúng như `:328` đã nói, ba cổng này chỉ canh HÌNH THỨC. Không cổng nào có thể thấy F1–F8, và
việc chúng xanh không nói gì về nội dung PR.

## KHÔNG ĐO ĐƯỢC

1. **Đọc comment qua MCP.** Không đo được việc MCP đọc 5811128755 hay các comment #238 ra gì. Phiên
   này không có công cụ MCP github. JSON-RPC tới `api.githubcopilot.com` là POST, nằm ngoài phạm vi
   "chỉ GET". Vì vậy câu "đọc qua MCP ra ký tự thật" là lời khai của tác giả, tôi không kiểm được.
2. **Giới hạn của kết luận F1.** Đầu ra thô của MCP ngày 22-08 không thấy lưu trong kho. Tìm
   `&#39;` trong kho, bỏ `CLAUDE.md`/`CHANGELOG.md`, ra 7 tệp. Chỉ một tệp nhắc `#238`, và chỉ để kể
   lại chứ không chứa đầu ra thô (`ops/reviews/r330-rig-quyet-mau-audit-nguoi-verdict.receipt.yaml:118`).
   Cả hai client REST đi qua cùng một chuỗi proxy, tức có một tầng chung. "Byte trên GitHub" chỉ được
   đo tới mức đó.
3. **Tầng nào thay header Authorization.** Có thể là proxy cục bộ `127.0.0.1:40613` hoặc proxy
   egress. Tôi chỉ loại được cấu hình client, vì `curl` và `urllib` cho kết quả như nhau.
4. **Phiên 09-25 của tác giả có bị thay header không.** Tôi chỉ đo được phiên này.
5. **Nguyên nhân 403 → 200.** Không tách được "đổi cho mọi phiên" với "cấu hình theo phiên". Lượt
   17-08 có đo sai hay không thì là quá khứ, không đo lại được.
6. **Phương thức GHI qua REST** (`DELETE /git/refs/…` và các lệnh ghi khác): phạm vi chỉ GET, và đó
   cũng là thao tác phá. Đây là lý do F3 xếp P2 chứ không phải P1: rủi ro chưa được đo.
7. **`doctor`.** Tôi không chạy `doctor`, vì nó POST `initialize` tới endpoint MCP khai trong
   `.mcp.json`. Việc `doctor` in `rest-kho=OK` trước ngày 2026-09-25 cũng không có biên nhận.
8. **`gh`.** Container không có `gh`, và cài nó thì không phải một phép GET. Vì vậy "`gh` nay dùng
   được" chỉ là suy ra từ REST, không phải phép đo.
9. **Người đang giữ `CLAUDE.md` lúc này** (`ai-dang-giu`): chưa chạy, vì cần fetch đủ ref. Executor
   phải đo trước khi áp hint.
10. **Công cụ MCP mà tác giả dùng ngày 09-25:** PR không ghi, nên không truy được.
