verdict: approve
reviewed_sha: e2fa6d74507e47e6c7114c765fca34e75c024d96
P1: 0   P2: 0   P3: 0
reviewer_provider: anthropic_claude
model_tu_khai: claude-opus-5-5 (Opus 5.5)
execution_surface_tu_khai: Claude Agent SDK, container Linux 6.18.44-fc-v50 x86_64 · Python 3.11.15 · curl 8.5.0 · git 2.43.0 · KHÔNG có `gh` · có rg/codex/claude · HTTPS qua proxy cục bộ 127.0.0.1:39695 (lượt 3 ghi 45805, lượt 2 ghi 42681) · GITHUB_PAT 93 ký tự, GH_TOKEN/GITHUB_TOKEN 14 ký tự · phiên KHÔNG có công cụ MCP github · đo 2026-09-30T07:59:57Z–08:23Z

Lượt 4, `advisory_review`. Reviewer và executor cùng provider (Anthropic), nên lượt này chỉ có giá trị tư vấn. Nó
không thay được một lượt review khác provider.

**Tóm tắt.** Vòng vá `53792ed..e2fa6d7` đóng đúng N5, và theo đó N1 và F4 (hai mục lượt 3 còn ĐÓNG-MỘT-PHẦN).
Mọi con số và biên nhận mới đều tái lập được. 14 đường của câu "Đo thêm" tôi đo lại ở ba vế token × hai client,
và chúng cho đúng chữ ký đã khai. Hai biên nhận cũng khớp: `commits/…` 21-09 và "2 đường kho" 17-08. Riêng giờ đo
`07:51–07:57Z` không có biên nhận nên KHÔNG ĐO ĐƯỢC; trạng thái thì bị kẹp hai phía bởi lượt 3 (07:27–07:41Z) và
lượt này (08:03–08:05Z), cùng kết quả. Tôi quét theo lớp trên toàn bộ `CLAUDE.md` và không thấy câu nào còn khai
trạng thái REST/`gh` cũ như hiện tại. Bốn chỗ chữ mới cũng không vượt phép đo theo trục nào. Byte-giữ và ba cổng đều
đạt. Không còn P1/P2/P3 ⇒ **approve**. `HINT.patch` rỗng. Có sáu mục thông tin cho executor (không tính finding);
đáng làm nhất là sửa thân PR #631: nó còn một con số lỗi thời và năm lời khai mà `CLAUDE.md` nay đã rút hoặc bác
(Thông tin 4).

`git diff 53792ed e2fa6d7` trùng byte `DIFF.vong.patch` (chỉ `CLAUDE.md`, +8/−4). `git diff origin/master e2fa6d7`
trùng byte `DIFF.patch`. Lúc 08:04Z REST vẫn trả head PR #631 là `bc5b7f69…`, và `GET commits/e2fa6d7…` → 422 từ
GitHub, tức `e2fa6d7` chưa được đẩy (khớp PROMPT).

Ghi nhận READ-ONLY: lệnh `git status --porcelain --ignored` đầu tiên (07:59:57Z) đã làm mới bộ đệm stat
`cay-kho/.git/index` (mtime 07:59:58Z). Nội dung cây, ref và HEAD không đổi (`git diff --quiet HEAD` rc=0, 0 tệp
untracked/ignored). Từ đó mọi lệnh git trong `cay-kho` chạy với `GIT_OPTIONAL_LOCKS=0`, và index không bị ghi lại.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lệnh kiểm chung (trong `cay-kho`):
```
rg -n 'CHỈ ở `/repos/<kho>`' CLAUDE.md                → 0 hit (rc=1)
rg -n 'MỌI câu 403|hơn một tháng|không ai thấy|Nền đã đổi|HAI DÒNG 403|Máy đã đúng sẵn' CLAUDE.md → 0 hit (rc=1)
```

| # | Lượt | Hạng · lớp | Trạng thái | Bằng chứng |
|---|---|---|---|---|
| N5 | 3 | P3 `pham-vi-tuyen-bo-rong-hon-do` (`:659`, trục đường dẫn, chiều thu hẹp) | **ĐÓNG** | Chữ "CHỈ ở `/repos/<kho>`, PR, comment" đã mất (0 hit). `:659` nay ghi "ĐÃ TRÔI ở các đường ĐÃ ĐO ra 200 (liệt kê dưới; đường chưa đo: KHÔNG ĐO ĐƯỢC)", tức giới hạn đúng tập đã đo và không khai tập đủ. `:664-668` liệt kê đích danh comment `5811128755` và 10 đường con. Cả 11 đường tôi tái lập ra **200, `Server: github.com`, 4 `X-GitHub-*`**; ba đường `hooks`/`keys`/`actions/secrets` ra 403 do proxy. Đo ở ba vế token × hai client (`urllib` 08:04:04–08:04:21Z, `curl` 08:04:33–08:04:49Z; `scratch/do_rest.{log,json}`). Biên nhận `commits/…` 21-09 (`b94182b`, tổ tiên `origin/master`) nay được dẫn ngay trong danh sách (`:666`), nên hết mâu thuẫn với `:700`. `:644` thêm "KHÔNG chỉ ba loại ấy". |
| N1 | 2 | P2 `pham-vi-tuyen-bo-rong-hon-do` | **ĐÓNG** | Lượt 3 ghi ĐÓNG-MỘT-PHẦN và phần còn lại chính là N5, nay đã ĐÓNG. Phần rộng ("MỌI câu 403") vẫn 0 hit. Năm đường 403 do proxy ở `:669-672` tôi tái lập đủ (`/graphql`, `/search/issues`, `/user/repos`, `/repos/cli/cli`, `/collaborators`: 403, không `Server`, 0 `X-GitHub-*`, ba vế, hai client). |
| F4 | 1b | P2 `pham-vi-tuyen-bo-rong-hon-do` | **ĐÓNG** | Lượt 3 ghi ĐÓNG-MỘT-PHẦN vì N5. Bốn chỗ vòng này viết mới (`:644`, `:659`, `:664-668`, `:726`) không có lượng từ phổ quát hay "CHỈ" nào vượt phép đo (xem quét theo lớp ở Findings). |

Kiểm hồi quy các mục lượt 3 đã chấm ĐÓNG. Vòng này chỉ thay 4 dòng cũ (`:644`, `:659`, `:664`, `:722`) bằng 8 dòng
mới (`:644`, `:659`, `:664-668`, `:726`). 1024 dòng còn lại trùng byte với `53792ed`, dời +4 kể từ dòng cũ `:665`
(`git diff -U0 53792ed e2fa6d7` và `difflib`). Không mục nào mở lại:
- **N2** (tách phiên 25-09/30-09, `:661-664`): không đổi nội dung. Tôi tái lập `/pulls/623` và `/pulls/631` → 200,
  `Server: github.com`, 4 `X-GitHub-*`, ba vế, hai client.
- **N3/F7** (danh sách chỗ còn văn bản 403, nay `:681-685`) và **N4/F5** (biên nhận 21-09, nay `:699-702`): không đổi.
  `git log -S 'commits/8394f7411bfbeacdd1b6d5eafda21473f6487268' -- ops/land/pr594-wp578-land-evidence.yaml` →
  `b94182b 2026-09-21T17:47:06+00:00`, dòng `:579` ghi `REST GET …/commits/8394f74…`.
- **F1** (`:151-158`): tôi GET lại #238 lúc 08:08:33Z (`scratch/do_238.log`). Có 9 comment, đủ 7/7
  `posted_comment_id` (đọc từ 7 tệp `ops/leases/lease-dang-windows-*-20260822.yaml`), tác giả `github-actions[bot]`,
  `created==updated` (22-08). Theo thứ tự ID tăng dần, số `'` là 22/33/14/49/34/33/19; 0 thực thể, 0 `&`. `curl`
  cho sha256 thân khớp `urllib` 7/7.
- **F2**: mọi câu 403 cũ vẫn có nhãn: 16-08 ở `:563-571`, 15-08 ở `:643-646`, 17-08 ở `:659-685`, `t103` ở `:726-728`.
- **F3/L1-1** (`:563-571`): gốc `/` → 200, thân `{}` 2 byte, không `Server`, 0 `X-GitHub-*`. `/collaborators` →
  403 do proxy, `/branches/master/protection` → 403 CÓ `Server: github.com` và 4 `X-GitHub-*` (*"Resource not
  accessible by integration"*). Ba vế, hai client.
- **F6/L1-4**: token giả → 200, `login=ducthangho`, `Github-Authentication-Token-Expiration: 2026-09-30 08:22:21 UTC`
  (đo 08:04Z), giống hệt vế không token và vế token thật. Sau mốc ấy header đã xoay sang `16:18:14 UTC`, vẫn giống
  hệt ở ba vế (Thông tin 6).
- **F8** (`:142-143`), **L1-2** (`:645`, `:674`), **L1-3** (`:675-677`): không đổi.

## Findings

**Không có finding P1/P2/P3.** `HINT.patch` rỗng (0 byte). `patch -p0 --dry-run` trên bản sao `scratch/thu/CLAUDE.md`
→ rc=0, bản sao không đổi (sha256 `116a5bfc…`).

### Quét theo lớp (việc 3)

Lệnh (trong `cay-kho`):
```
rg -n -e '403' -e 'REST' -e '\bgh\b' -e 'api\.github' -e 'proxy' -e 'GraphQL' -e 'graphql' CLAUDE.md
awk 'NR>=555 && NR<=731 && /CHỈ|[Mm]ọi|MỌI|chỉ /' CLAUDE.md          # lượng từ trong vùng REST
```
Tôi đọc từng hit, và đọc trọn tệp (1031 dòng).

**Bốn chỗ vòng này viết mới**, xét theo bảy trục (phiên · đường dẫn · phương thức · client · token · công cụ · thời điểm):
- `:659`: tiêu đề nay giới hạn đúng tập đã đo ra 200. Đường chưa đo thì gắn KHÔNG ĐO ĐƯỢC. Câu không còn lượng từ
  phổ quát hay "CHỈ" theo đường dẫn nào. "CHỈ ở các phiên đã đo" giữ đúng trục phiên.
- `:664-668`: mọi trục đều được ghi (ngày giờ, 14 đường đích danh, hai client kèm số đường mỗi client, ba vế token).
  Tôi tái lập cả 14 đường. Mẫu `commits/<sha>` là route, không phải một SHA: proxy cho qua với mọi SHA thử.
  Phương thức không ghi trong câu. Nhưng "ra 200" là kết quả đọc, còn `:693` (GHI: KHÔNG ĐO ĐƯỢC) và `:570` (REST
  DELETE: KHÔNG ĐO ĐƯỢC) chặn cách hiểu thành phương thức ghi. Lượt 3 cũng xét trục này và không tính.
- `:644`: "KHÔNG chỉ ba loại ấy" đúng. "các đường khác liệt kê" trỏ đúng bảy đường 403 do proxy còn lại (cùng
  `/graphql` là tám), mọi đường đều tái lập (xem Thông tin 1 về việc bỏ chữ "đo 30-09").
- `:726`: "'mọi' đã rộng hơn phép đo 17-08 — 2 đường kho" đúng cả số lẫn thứ tự thời gian (xem Phép đo lại).

**Chỗ cũ trong vùng REST/`gh`**: mọi câu khai 403 hoặc "`gh` vô ích" đều có nhãn, gồm 16-08 (`:563-571`), 15-08
(`:643-646`), 17-08 (`:659-685`) và `t103` (`:726-728`). Các câu khai trạng thái mới đều ghi phiên và trỏ `doctor`
(`:144-146`, `:678-680`). Hai câu nêu ví dụ, `:144-145` và `:566-567` ("`/repos/<kho>`, PR và comment … KHÔNG phải
mọi đường con"), không khai tập đủ nên không mâu thuẫn danh sách mới. Mọi con trỏ nội bộ của chữ mới đều trỏ tới
đúng gạch có thật và đúng hướng: "Câu 403 REST" dưới (`:659`), "Bài học gốc" dưới (`:696`), "phép đo 17-08 ghi ở
trên" (`:647-650`). `:800-802` (12-08, "KHÔNG cài gh … kho dùng GitHub qua MCP") là lý do thiết kế có ghi ngày,
không khai 403, và khớp `:646` ("giữ hay bỏ thì tệp này chưa ghi quyết định").

### Thông tin, không tính finding

1. **`:644` bỏ chữ "đo 30-09"** khỏi vế 403. Bản `e271af6` ghi "và 4 đường khác đo 30-09", bản này ghi "và các đường
   khác liệt kê (gạch 'Câu 403 REST' dưới)". Ngày không mất: gạch được trỏ tới ghi ngày cho từng nhóm đường
   (`07:10–07:11Z`, `07:51–07:57Z`). Riêng `/graphql` còn có biên nhận 21-09 · 28-09 · 29-09, nên con trỏ thực ra
   đúng hơn chữ "đo 30-09" cũ. Vế `/graphql` ở cả hai bản vốn không mang ngày trong câu. Không cần sửa.
2. **Thân 403 của proxy hôm nay nói thẳng rằng quyền theo kho là cấu hình THEO PHIÊN**
   (`scratch/thong_diep_proxy.log`, 08:05Z, nguyên văn):
   - `/repos/cli/cli` → *"GitHub access to this repository is not enabled for this session. Use add_repo to request
     access. If add_repo answers that read access is already available and you need GitHub API or write access,
     call add_repo again with access:"push" to attach the repository with credentials."*
   - `/search/issues` và `/user/repos` → *"This GitHub API path is not available: sessions are bound to their
     configured repositories. Use repository-scoped endpoints (repos/{owner}/{repo}/...)."*

   Câu thứ nhất gần với thân 403 ngày 15-08 mà `:676-677` trích (*"not enabled for this session"*). Dữ kiện này
   nghiêng về giả thuyết "cấu hình THEO PHIÊN" ở `:675`, nhưng không tách được nguyên nhân cho các phiên 15-08 và
   17-08, nên "Nguyên nhân KHÔNG ĐO ĐƯỢC" vẫn đúng. Tệp chưa nhắc `add_repo`, là đường chữa mà chính proxy chỉ ra. Tôi
   không tính finding, vì người gặp 403 đọc được đường ấy ngay trong thân phản hồi. Một packet sau có thể thêm câu
   "gặp 403 không header GitHub: đọc thân 403 trước".
3. **Ba chỗ ngoài `CLAUDE.md` mà lượt 3 ghi vẫn còn nguyên**, vì chỉ `CLAUDE.md` đổi:
   `.claude/dev/launcher_test.py:3119`, `.claude/dev/packet_loop.py:1202`, `scripts/don-nhanh_test.ps1:420`. Riêng
   `packet_loop.py:1199-1202` (*"`/repos/…/protection` trả 403 với 0 header GitHub — proxy chặn theo ĐƯỜNG DẪN"*)
   nay bị phép đo bác: 403 **CÓ** `Server: github.com` và 4 `X-GitHub-*` (*"Resource not accessible by
   integration"*), ba vế, hai client. Kết luận "không kiểm chứng nổi" của nó vẫn đứng. Cả ba nằm ngoài write set;
   danh sách `:681-685` có rào "mẫu có thể sót", nên việc này thuộc packet theo sau, như lượt 3 đã ghi.
4. **Thân PR #631 trên GitHub đã cũ.** Tôi GET lúc 08:13:47Z: thân trùng `PR-BODY.md` (khác `\n` cuối). Nó còn
   một con số lỗi thời, "`+22/−2`, Hai chỗ" (thực tế `CLAUDE.md` +82/−4 so `origin/master`, `git diff --numstat`), và
   năm lời khai mà `CLAUDE.md` nay đã rút hoặc bác:
   - "cùng container remote": `:661` nay chỉ ghi "một phiên remote".
   - "Nền đã đổi — không phải lượt cũ đo sai": bị bác ở `:675-677` ("Nguyên nhân KHÔNG ĐO ĐƯỢC … thế chưa phải chứng
     minh").
   - "máy đã đúng sẵn … từ trước khi mục này được sửa": bị bác ở `:680-681` ("KHÔNG có biên nhận").
   - "comment của lượt 22-08 không còn để thử lại": bị bác ở `:151-153`, P1 của lượt 1b.
   - "cấp danh tính hộ": bị bác ở `:690` ("bị THAY, không chỉ được 'cấp hộ'").

   Merge commit của kho chỉ chép tiêu đề PR (`c16bec6` và `7b308bc` mỗi cái 3 dòng), nên thân PR không vào lịch sử
   git. Nhưng người đọc trang PR sẽ gặp bản đã bị bác. Executor nên sửa thân PR lúc đẩy. Đây không phải finding trên
   `CLAUDE.md`.
5. **`:705-716`** (`api.githubcopilot.com` gọi được, JSON-RPC tới `/mcp/` bằng `GITHUB_PAT`, "44 công cụ") là lời
   khai trạng thái của phiên 15-08, không thuộc REST/`gh`. Tôi không đo được (xem KHÔNG ĐO ĐƯỢC).
6. **Sau mốc `Github-Authentication-Token-Expiration` mà `:689` ghi (08:22:21 UTC).** Tôi đo lúc 08:22:42–08:22:46Z
   (`scratch/sau_han.log`, `urllib`, ba vế). `/user`, `/repos/<kho>` và `/pulls/631` vẫn 200, `Server: github.com`,
   4 `X-GitHub-*`. Header hạn nay là **`2026-09-30 16:18:14 UTC`**, giống hệt nhau ở ba vế; lúc 08:04Z nó còn là
   `08:22:21 UTC`. Vậy credential mà proxy gắn vào đã được thay ở đâu đó trong khoảng 08:04:53–08:22:42Z, và đường
   vẫn sống qua mốc hạn cũ. Con số `08:22:21 UTC` ở `:689` là ảnh chụp của MỘT credential, không phải hạn của phiên.
   Câu ấy đã gắn "lúc đo", nên đúng phạm vi; tôi ghi lại để không ai dùng con số ấy làm mốc hết hạn. Dữ kiện này đỡ
   thêm cho `:692` ("`200` … KHÔNG chứng minh token của bạn còn sống"). Không tính finding.

## Phép đo lại

Tôi chỉ dùng GET và không in token. Ba vế: không token · `Authorization: Bearer $GITHUB_PAT` · `Bearer ghp_` + 36×`x`
(giả). `curl` nhận header từ tệp `-K` tạm (0600), nên token không nằm trong argv. Log thô: `scratch/do_rest.{py,log,json}`
(`urllib` 08:03:56–08:04:26Z, `curl` 08:04:26–08:04:53Z), `scratch/thong_diep_proxy.log` (thân 403 đầy đủ, 08:05Z),
`scratch/so_contents.py`, `scratch/do_238.log`, `scratch/pr_body_comment.log`.
Mỗi đường trong 26 đường cho **đúng một** chữ ký (status, `Server`, số `X-GitHub-*`) qua 6 lần đo (3 vế × 2 client).

| Lời khai mới trong `DIFF.vong.patch` | Đo 2026-09-30 (phiên này) | Kết quả |
|---|---|---|
| `:664-665` "Đo thêm `2026-09-30T07:51–07:57Z`" | tìm biên nhận: `rg '07:51\|07:57'` toàn cây + `git log --all --since 07:45Z` | Không có biên nhận nào ngoài chính `CLAUDE.md:665` ⇒ **giờ đo: KHÔNG ĐO ĐƯỢC**. Trạng thái thì tái lập, và bị kẹp hai phía cho cùng kết quả: lượt 3 (07:27–07:41Z; tập của nó CHỨA cả 14 đường: 12 đường con ⊇ 10 đường này, cùng `hooks`/`keys`/`actions/secrets`, comment đo 07:27Z; `luot-3-opus-max/VERDICT.md:78-85`, `:138`) và lượt này (08:03–08:05Z) |
| `:665` "14 đường: `urllib` cả 14, `curl` 10; ba vế y hệt" | 14 = comment + 10 đường con + 3 đường 403 | ✓ đếm đúng 14. Tôi đo cả 14 bằng **cả hai** client, nên tập con 10 đường nào của `curl` cũng được phủ. Ba vế y hệt ở mọi đường |
| `:665-668` comment `5811128755` và 10 đường con (`commits/<sha>` · `issues/631` · `issues` · `issues/238/comments` · `pulls` · `actions/runs` · `git/refs/heads/master` · `contents/VERSION` · `branches/master` · `rulesets`) → 200 CÓ `X-GitHub-*` | urllib + curl, 3 vế | ✓ cả 11: **200, `Server: github.com`, 4 `X-GitHub-*`**. Riêng `contents/VERSION`: thân lệch giữa các lần gọi, nhưng che tham số `token=` ngắn hạn trong `download_url` thì mọi khoá JSON trùng nhau (`scratch/so_contents.py`). Đó là nhiễu thời gian, không phụ thuộc vế |
| `:666` `commits/<sha>` "biên nhận 200 từ 21-09, gạch 'Bài học gốc' dưới" | `git log -S` + `sed -n 577,581p` | ✓ `ops/land/pr594-wp578-land-evidence.yaml:579` ghi `REST GET …/commits/8394f74… (HTTP 200)`, thêm ở `b94182b` (2026-09-21T17:47:06Z, tổ tiên `origin/master`), `execution_surface: claude_code`. Gạch "Bài học gốc" ở `:696`, đúng là "dưới". `<sha>` là mẫu route: SHA master `c16bec6` và SHA `bc5b7f6` cũng 200 CÓ `X-GitHub-*`; SHA `e2fa6d7` ra 422 **từ GitHub** (4 `X-GitHub-*`), tức proxy cho qua route với mọi SHA |
| `:668` `hooks` · `keys` · `actions/secrets` → 403 do proxy | urllib + curl, 3 vế | ✓ 403, không `Server`, 0 `X-GitHub-*`. Thân: *"Access to this GitHub API path is not permitted through this proxy."* (`hooks`, `keys`), *"Access to this GitHub **Actions** path is not permitted through this proxy."* (`actions/secrets`) |
| `:644` "`/repos/<kho>`, PR, comment nay 200 (phiên đo 25-09, 30-09; KHÔNG chỉ ba loại ấy)" | như trên | ✓ 30-09: 11 đường ngoài ba loại ấy ra 200. "403 … vẫn đúng ở `/graphql` và các đường khác liệt kê": ✓ đủ 8 đường 403 do proxy được liệt kê (`hooks`, `keys`, `actions/secrets`, `/graphql`, `/search/issues`, `/user/repos`, `/repos/cli/cli`, `/collaborators`), ba vế y hệt, hai client |
| `:659` "ĐÃ TRÔI ở các đường ĐÃ ĐO ra 200 (liệt kê dưới; đường chưa đo: KHÔNG ĐO ĐƯỢC)" | đối chiếu danh sách `:661-668` | ✓ mọi đường được liệt kê là 200 đều tái lập ở 30-09 (`/rate_limit`, `/user`, `/repos/<kho>`, `/pulls/623`, `/pulls/631` và 11 đường trên) |
| `:726` "'mọi' đã rộng hơn phép đo 17-08 ghi ở trên — 2 đường kho" | `git log -S` câu `t103`, `git show 40590bd:CLAUDE.md` | ✓ câu "mọi thao tác kho trả 403" thêm ở `56f7774` (2026-08-17T04:15:09Z), **sau** phép đo 17-08 (`40590bd`, 01:40:25Z). Phép đo ấy có đúng 2 đường kho: `/repos/<kho>` và `/repos/<kho>/pulls/N` (`40590bd:CLAUDE.md:259-260`, nay `:648-649`) |
| `:726-727` "25-09/30-09 `/repos/<kho>` và PR trả 200, GraphQL vẫn 403 do proxy (đo 30-09)" | như trên | ✓ (GET; POST xem KHÔNG ĐO ĐƯỢC) |

Đo thêm để kiểm hồi quy (không phải chữ mới của vòng này): gốc `/` → 200 `{}` không `Server` (`:563-566`);
`/branches/master/protection` → 403 CÓ `Server: github.com` + 4 `X-GitHub-*`, *"Resource not accessible by
integration"* (`:568`); `/user` ở cả ba vế → `login=ducthangho`, `Github-Authentication-Token-Expiration:
2026-09-30 08:22:21 UTC` (`:688-689`); comment `5811128755`: `'`=44, `>`=8, `<`=3, `"`=2, 0 thực thể (`:147-148`);
PR #631 head vẫn `bc5b7f69…`, thân sống trùng `PR-BODY.md` (chỉ khác `\n` cuối).

## Cổng

Tôi chạy trong `cay-kho` tại `e2fa6d7`, `core.abbrev=7`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`, lúc
08:11:42–08:11:49Z (`scratch/gate_e2fa6d7.log`). Trước và sau: 0 tệp untracked, 0 tệp ignored, `git diff --quiet
HEAD` rc=0, mtime `.git/index` không đổi (07:59:58Z), HEAD vẫn `e2fa6d7`.
- `packet_loop.py doctrine-scan --root .` → **rc=0**, "sạch — đã quét 10 tệp, 0 chỗ chép doctrine".
- `packet_loop.py adr-song --root .` → **rc=0**, "50 ADR trên đĩa, 50 dòng trong §20, khớp 1–1 (tha thiếu trạng
  thái: ['0016'])".
- `tl.py doc-claims-check --strict --json` → **rc=0**, `ok=true`, `files_scanned=110`, `flags=0`,
  `advisory_count=381`, `CLAUDE.md` có trong `roots`.

A/B dựng trong **một** lệnh: hai clone `--no-local` từ `kho.git`, nền `53792ed` và sau `e2fa6d7`, `core.abbrev=7`
(`scratch/gate_ab.log`, 08:11:03–08:11:31Z). Ba cổng y hệt nhau: rc=0 · rc=0 · rc=0, 110 tệp, 0 flag, 381 advisory.
`git status --porcelain --ignored` rỗng sau cổng ở cả hai clone. Ba cổng này chỉ canh HÌNH THỨC (`:336-337`).

Byte-giữ (việc 4, `scratch/bytegiu.log`):
- Dòng có dấu chéo ngược + `u0308`: `:103` (dòng `co`+`\`+`u0308`+`dex` liền), `:104`, `:140`. Cả ba trùng byte ở
  `origin/master`, `af5edd3`, `bc5b7f6`, `aecc978`, `f174628`, `280ea34`, `e271af6`, `53792ed`, `e2fa6d7` (băm gộp
  `dc7b34a791216b3c`). Mẫu được dựng từ byte `0x5c`, không gõ dấu chéo. U+0308 thật = 0, U+00F6 = 2 ở cả chín revision.
- `git diff --quiet <commit thêm> e2fa6d7 -- ops/reviews/<dir>` rc=0 cho cả bốn thư mục: `pr631-review-1-claude`
  (`bc5b7f6`), `-1b-claude-cli` (`aecc978`), `-2-opus-max` (`280ea34`), `-3-opus-max` (`53792ed`). Không commit nào
  sau đó chạm chúng, và tập blob không đổi. `git diff --name-status 53792ed e2fa6d7` chỉ ra `M CLAUDE.md`.
- Mọi tệp trong `luot-*/` của sandbox trùng byte bản trong kho, tập tên tệp trùng. Sha256 `luot-3-opus-max/*`
  khớp số ghi trong `RUN.md` (VERDICT `a06c84f9…`, HINT `13ca0981…`, PROMPT `37aa015e…`).

## KHÔNG ĐO ĐƯỢC
1. **Giờ đo `07:51–07:57Z` của executor** (`:665`) và việc `curl` phủ 10 đường nào: không có biên nhận trong cây
   hay trong ref (`rg -n -e '07:51' -e '07:57'` chỉ ra `CLAUDE.md:665`; `git log --all --since 07:45Z` chỉ có
   `53792ed` và `e2fa6d7`). Tôi tái lập được TRẠNG THÁI, không tái lập được THỜI ĐIỂM của phiên kia. Các giờ cũ
   (`06:29Z`, `06:30–06:31Z`, `07:10Z`, `07:10–07:11Z`, `07:11Z`) vẫn như lượt 3 ghi.
2. **POST `/graphql`** và **mọi phương thức GHI qua REST** (`DELETE /git/refs/…` …): phạm vi của tôi chỉ là GET. Vế
   POST của `:727` đứng trên các biên nhận mà `:671-672` dẫn, và tôi đã kiểm cả ba: `git blame` cho thấy
   `pr594-wp578-land-evidence.yaml:523` (*"POST /graphql: GitHub GraphQL is not available…"*) được thêm ở `a479699`
   (2026-09-21T18:11:22Z); `pr666-wp650-provenance.yaml` thêm chuỗi ấy ở `fcef7c3` (28-09);
   `pr680-wp676-land-evidence.yaml:146` (`node(id:`) ở `c928ba9` (29-09). Cả ba là tổ tiên của `origin/master`.
   Vế ấy còn đứng trên thông điệp chính sách của proxy.
3. **`gh`**: container không có.
4. **Đọc qua MCP** (comment `5811128755`, bảy comment #238): phiên này không có công cụ MCP github, và JSON-RPC là
   POST.
5. **`api.githubcopilot.com`** (`:705-716`): muốn đo phải POST `initialize`, và host này nằm ngoài phạm vi GET được
   phép (chỉ `api.github.com`). Tôi không chạy `doctor`, vì nó POST tới MCP.
6. **Tầng nào thay header Authorization**, và **nguyên nhân 403 → 200** ở các phiên 15-08/17-08: vẫn chưa tách được.
   Dữ kiện mới ở Thông tin 2 chỉ nghiêng về một giả thuyết, không chứng minh.
7. **Ai đang giữ `CLAUDE.md`** (`ai-dang-giu`): `cay-kho` là READ-ONLY, và `origin` là mirror dựng từ kho cục bộ
   của executor, nên không trả lời được "lease nào đang giữ" (`:196-212`). Vòng này không có hint để áp, nhưng
   executor vẫn phải đo trên ref thật trước khi đẩy.
