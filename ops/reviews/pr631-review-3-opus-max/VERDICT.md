verdict: changes_requested
reviewed_sha: e271af618f9a52eb2291b7fe0da68f07923f1caa
P1: 0   P2: 0   P3: 1
reviewer_provider: anthropic_claude
model_tu_khai: claude-opus-5-5 (Opus 5.5)
execution_surface_tu_khai: Claude Agent SDK trong container Linux 6.18.44-fc-v50 x86_64 · Python 3.11.15 · curl 8.5.0 · git 2.43.0 · KHÔNG có `gh` · có codex/claude/rg · HTTPS qua proxy cục bộ 127.0.0.1:45805 (lượt 2 ghi 42681, lượt 1b ghi 40613) · GITHUB_PAT 93 ký tự, GH_TOKEN/GITHUB_TOKEN 14 ký tự · phiên KHÔNG có công cụ MCP github · đo 2026-09-30T07:26Z–07:46Z

Lượt 3, `advisory_review`. Reviewer và executor cùng provider (Anthropic), nên lượt này chỉ có giá trị tư vấn. Nó
không thay được một lượt review khác provider.

`cay-kho` ở `e271af6`. `git diff 280ea34 e271af6` trùng byte `DIFF.vong.patch`: chỉ đổi `CLAUDE.md`, +41/−25.
`git diff origin/master e271af6` trùng byte `DIFF.patch`. Lúc 07:27Z và 07:45:59Z, REST vẫn trả head PR #631 là
`bc5b7f69…` (`scratch/do_rest.log`, `scratch/do_238.log`), tức `e271af6` chưa được đẩy (khớp PROMPT).

**Tóm tắt.** Vòng vá này đóng đúng N2, N3, N4, và theo chúng là F2, F5, F7, L1-2. Mọi con số và biên nhận mới đều
tái lập được: trạng thái REST đo bằng ba vế token, phần lớn bằng cả hai client; biên nhận kiểm bằng `git log -S`
(bảng "Phép đo lại"). Giờ đo của phiên executor thì không có biên nhận nên KHÔNG ĐO ĐƯỢC. Dù vậy, các phép đo độc
lập kẹp hai phía đều cho cùng kết quả. Với mốc `06:30–06:31Z`, hai phía là lượt 1b (06:07–06:23Z) và lượt 2
(06:44–06:58Z). Với mốc `07:10–07:11Z`, hai phía là lượt 2 (06:49Z) và lượt này (07:27Z).

N1 chỉ đóng một phần. Để thu câu "MỌI câu 403" về đúng phạm vi, bản vá viết câu mới ở `:659` là *"ĐÃ TRÔI —
**CHỈ** ở `/repos/<kho>`, PR, comment"*. Câu này trái với 12 đường con theo kho đo ra 200. Nó cũng trái với chính
biên nhận `commits/…` = 200 mà tệp dẫn ở `:696`. Còn lại một P3 (N5), `HINT.patch` phủ nó. Không có P1/P2.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lệnh kiểm chung (trong `cay-kho`):
```
rg -n 'MỌI câu 403|hơn một tháng|không ai thấy|Nền đã đổi|cùng container remote|NAY CÓ|đã có client thứ hai thật|HAI DÒNG 403|Máy đã đúng sẵn|/repos/<kho>/…` thì 200' CLAUDE.md
```
→ **0 hit** (rc=1). `rg -n 'mất chân đỡ' CLAUDE.md` → chỉ `:645` và `:670`, cả hai là *"chỉ mất chân đỡ CŨ"*.

| # | Lượt | Hạng · lớp | Trạng thái | Bằng chứng |
|---|---|---|---|---|
| N1 | 2 | P2 `pham-vi-tuyen-bo-rong-hon-do` | **ĐÓNG-MỘT-PHẦN** | Phần rộng đã đóng. "MỌI câu 403" đã mất (0 hit). Nhãn 15-08 ở `:643-646` ghi "trôi MỘT PHẦN". `:665-668` liệt kê năm đường vẫn 403 do proxy, tôi tái lập đủ năm (urllib 07:27Z cả năm; curl 07:28Z cho `/graphql`, `/collaborators`, `/repos/cli/cli`; ba vế y hệt). `:667-668` dẫn biên nhận GraphQL 403: `a479699` (21-09, ghi rõ `POST /graphql`), `fcef7c3` (28-09), `c928ba9` (29-09), cả ba là tổ tiên của `origin/master`. Câu `gh` đã sửa thành "chỉ mất chân đỡ CŨ". `:726-727` ghi `gh-kho=OK` KHÔNG phủ GraphQL. Cụm "…" ở `:566` đã thu lại, kèm `collaborators`/`protection`. **Phần còn lại:** câu thay thế ở `:659` thu hẹp quá tay thành "CHỈ ở `/repos/<kho>`, PR, comment" → **N5**. |
| N2 | 2 | P3 `ghep-sai-luot` | **ĐÓNG** | `:661-664` đã tách hai phiên. Vế 25-09 ghi `/pulls/623`, "chỉ ghi `hdr_github=True`". Tôi GET thân PR #631 thật qua REST và so với `PR-BODY.md`: trùng, chỉ khác dòng trống cuối. Thân có 8 lần `hdr_github=True` và 2 lần `pulls/623`. Vế 30-09 ghi `/pulls/631`, `Server: github.com`, tôi tái lập (PR tạo 2026-09-25T01:35:03Z, sau mốc 01:1xZ). |
| N3 | 2 | P3 `pham-vi-tuyen-bo-rong-hon-do` | **ĐÓNG** | `:678-681` đã thêm `CONG_CU` (mục `gh`, `launcher.py:1910-1939`) và bảng "GitHub: bốn đường, hỏng độc lập" (`docs/GOI_AGENT_DA_NEN.md:246-257`). Danh sách có rào "mẫu có thể sót", nên không còn đọc như một danh sách đủ. Tôi quét lại và thấy thêm ba chỗ; hàng rào đã phủ chúng, nên chỉ ghi làm thông tin (xem cuối Findings). |
| N4 | 2 | P3 `chan-doan-sai-vi-sao-troi` | **ĐÓNG** | "hơn một tháng … không ai thấy": 0 hit. `:695-698` dẫn `b94182b`: `git log -S 'commits/8394f7411bfbeacdd1b6d5eafda21473f6487268' -- ops/land/pr594-wp578-land-evidence.yaml` chỉ ra `b94182b 2026-09-21T17:47:06+00:00`. Dòng biên nhận (`:579`) ghi `REST GET …/commits/8394f74… (HTTP 200)`. Tệp ấy khai `execution_surface: claude_code` và chép nguyên văn thông điệp GraphQL của proxy, nên phiên 21-09 đứng sau proxy Claude Code, tức đúng "trạng thái MỚI". "Sai từ LÚC NÀO: KHÔNG ĐO ĐƯỢC" là đúng phạm vi. Tôi GET lại đường ấy lúc 07:27Z và 07:32Z: 200, 4 `X-GitHub-*`, ba vế. |
| F2 | 1b | P2 `trang-thai-cu-khong-danh-dau` | **ĐÓNG** | Mọi câu 403 cũ đều có nhãn: 16-08 ở `:563-571`, 15-08 ở `:643-646`, 17-08 ở `:659-681`, `t103` ở `:722-724`. Nội dung nhãn được theo dõi ở N1/N5. |
| F4 | 1b | P2 `pham-vi-tuyen-bo-rong-hon-do` | **ĐÓNG-MỘT-PHẦN** | Các câu gốc đã sửa (0 hit ở lệnh trên). Lớp này tái phát lần thứ hai, cũng trên trục ĐƯỜNG DẪN nhưng theo chiều ngược: lượt 2 là "MỌI", lượt này là "CHỈ" ở `:659` → **N5** (P3). |
| F5 | 1b | P2 `chan-doan-sai-vi-sao-troi` | **ĐÓNG** | Đóng theo N4. |
| F7 | 1b | P3 `pham-vi-tuyen-bo-rong-hon-do` | **ĐÓNG** | Đóng theo N3. |
| L1-2 | 1 | P2 `tham-chieu-hep-bo-sot-menh-lenh-15-08` | **ĐÓNG** | Chữ "mất chân đỡ" (do hint lượt 1 gợi ra) đã thành "chỉ mất chân đỡ CŨ" (`:645`, `:670`), kèm GraphQL 403 (`:644`, `:665-668`, `:723`). |

Tôi cũng kiểm hồi quy các mục lượt 2 đã chấm ĐÓNG. Không mục nào mở lại:
- **F1:** `:151-158` không đổi. Tôi GET lại `#238` lúc 07:45:58Z (`scratch/do_238.log`): có 9 comment, đủ 7/7
  `posted_comment_id`, tác giả `github-actions[bot]`, `created==updated`. Số `'` là 22/33/14/49/34/33/19, 0 thực thể,
  0 `&`.
- **F3/L1-1:** `:563-571` có đổi ở vòng này, và nhãn vẫn đúng. Gốc `/` → 200, thân `{}` (2 byte), không `Server`, 0
  `X-GitHub-*`, ở cả ba vế và hai client. REST DELETE vẫn là KHÔNG ĐO ĐƯỢC.
- **F6:** Token giả → 200, `login=ducthangho`, `Github-Authentication-Token-Expiration: 2026-09-30 08:22:21 UTC`, giống
  nhau ở mọi vế.
- **F8:** `:142-143` vẫn giữ căn cứ (nay ghi `/repos/<kho>` · `/pulls/N` → 403 do proxy).
- **L1-3** (`:671-673`) và **L1-4** (`:684-686`): không đổi.

## Findings

`HINT.patch` phủ N5: 1 hunk, +5/−2, chỉ sửa `CLAUDE.md`. Cách tôi kiểm nó:
- `patch -p0 --dry-run` trên bản sao `scratch/thu/` → rc=0, bản sao không đổi.
- Áp thật trên `scratch/thu2/` → rc=0, kết quả trùng byte `scratch/sau/CLAUDE.md`.
- A/B trong **một** lệnh: hai clone `--no-local` từ `kho.git`, cùng detached ở `e271af6`, `core.abbrev=7`. Một clone
  để nền, một clone áp hint. Ba cổng cho kết quả y hệt nhau (`scratch/gate_nen_vs_hint.log`, 07:42:52Z).
- Ba dòng có dấu chéo ngược + `u0308` (`:103`, `:104`, `:140`) trùng byte giữa nền và hint (băm gộp
  `dc7b34a791216b3c`). U+0308 thật = 0.

**Trước khi áp:** executor phải chạy `ai-dang-giu CLAUDE.md` trên ref thật (xem KHÔNG ĐO ĐƯỢC #6).

### N5 · P3 · `pham-vi-tuyen-bo-rong-hon-do` (tiếp N1/F4, trục đường dẫn, chiều thu hẹp) · `CLAUDE.md:659`

**Lời khai (câu mới của vòng vá):** *"**Câu 403 REST Ở TRÊN ĐÃ TRÔI — CHỈ ở `/repos/<kho>`, PR, comment, CHỈ ở các
phiên đã đo**"*.

"CHỈ" biến ba loại đường thành một **tập đủ**. Đọc theo chữ, 15-08 (*"REST thẳng … bị PROXY chặn 403"*) và 17-08
(*"REST bị chặn ĐÚNG CHỖ làm việc"*) vẫn đúng ở mọi đường theo kho khác. Có ba bằng chứng bác điều đó:
1. **Chính tệp bác nó.** `:696` dùng `REST GET /repos/<kho>/commits/…` → 200 (21-09) làm bằng chứng rằng "trạng
   thái MỚI đã có người DÙNG". Đó là một đường ngoài ba loại `/repos/<kho>` · PR · comment.
   (``rg -n 'CHỈ ở `/repos/<kho>`' CLAUDE.md`` → `:659`; `rg -n 'commits/' CLAUDE.md` → `:696`.)
2. **Đo 30-09 bác nó.** Ba vế (không token · `GITHUB_PAT` · token giả) cho kết quả y hệt nhau, **12** đường con theo
   kho đều **200, `Server: github.com`, 4 `X-GitHub-*`**. Hai client khớp nhau: `urllib` đo 07:32:10–07:32:23Z
   (`scratch/do_duong_con.{log,json}`). `curl` đo lại 5 đường 200 và 3 đường 403 lúc 07:40:50–07:40:57Z
   (`scratch/do_duong_con_curl.log`).
   ```
   commits/8394f74… · actions/runs · git/refs/heads/master · branches/master · rulesets · issues/631
   issues/238/comments · pulls/631/reviews · contents/VERSION · check-suites/96331398646 · pulls · issues   → 200 CÓ X-GitHub-*
   hooks · keys · actions/secrets                                                                          → 403 KHÔNG Server, 0 X-GitHub-* (proxy)
   ```
   Bộ phân loại của chính kho (`_do_rest_github`, nạp bằng importlib, không ghi bytecode) cho `commits/…` →
   `mo`/`OK` ở cả ba vế (`scratch/do_launcher_rest.log`, 07:36Z).
3. **Executor đã có số liệu này khi viết.** Verdict lượt 2 đã nằm trong kho từ `280ea34`:
   `git show e271af6:ops/reviews/pr631-review-2-opus-max/VERDICT.md | sed -n 73p` →
   `/repos/<kho>/{rulesets,rules/branches/master,branches/master,git/refs/heads/master,actions/runs} 200 CÓ X-GitHub-*`.

Đây là hình dạng `:526-546` (*"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ … TỰ TÁI TẠO lỗ nó vừa lấp"*). Lượt 2 chỉ ra "MỌI" (rộng quá),
và câu thay thế dùng "CHỈ" (hẹp quá). Cả hai cùng lệch khỏi phép đo trên trục ĐƯỜNG DẪN, và nằm ngay trong gạch dạy
*"ghi PHẠM VI (phiên nào, ĐƯỜNG nào)"* (`:699`). Hai câu cùng nghĩa ở chỗ khác thì viết đúng: `:145` và `:566` ghi
*"KHÔNG phải mọi đường con"* mà không dùng "CHỈ". Riêng `:643` chỉ liệt kê ví dụ, không khai tập đủ, nên tôi không tính.

**Vì sao P3 mà không P2:** câu đọc theo chữ là sai. Nhưng hành động nó gây ra là né REST ở `commits`/`actions`/…
và đi đường MCP. Đường MCP chạy được (`:709-711`), nên tôi không dựng được hậu quả sai nào. Ngoài ra `:145` và `:566`
ngay gần đó đã nói đúng.

**Sửa (`HINT.patch`):**
- Đổi tiêu đề gạch thành "ở các đường THEO KHO đã đo (KHÔNG phải mọi đường con), CHỈ ở các phiên đã đo".
- Thêm một câu "KHÔNG chỉ ba loại …". Câu này dẫn biên nhận 21-09 mà tệp đã có, cùng năm đường đo 30-09 **ghi đích
  danh** (không dùng placeholder), kèm giờ, client và phiên đo.
- Executor phải tự đo lại trước khi commit, đúng như NHÃN.

### Thông tin, không tính finding

1. **Danh sách `:678-681`** đã rào "mẫu có thể sót". Tôi quét
   `rg --hidden -n -i -g '!ops/**' -g '!.git/**' -e 'bi proxy' -e '403 với 0 header' -e 'ăn 403 do proxy' .`
   (5 hit: hai hit đã có trong danh sách là `launcher.py:3412` và `session-start.sh:196`, ba hit còn lại là chỗ mới).
   Ba chỗ mới vẫn dựa trên 403 cũ, và nằm ngoài write set của PR. Packet theo sau nên gộp vào:
   - `.claude/dev/launcher_test.py:3114-3121`: docstring `t109`. Nó đỡ đúng quyết định `bat_buoc.remote: False` bằng
     403 17-08, song song với mục `CONG_CU` đã được liệt kê.
   - `.claude/dev/packet_loop.py:1199-1202`: *"`/repos/…/protection` trả 403 với 0 header GitHub — proxy chặn theo
     ĐƯỜNG DẪN"*. Đo 30-09 thì `branches/master/protection` → 403 **CÓ** `Server: github.com` và 4 `X-GitHub-*`
     (*"Resource not accessible by integration"*), tức cơ chế đã đổi. Kết luận "không kiểm chứng nổi" thì vẫn đúng.
   - `scripts/don-nhanh_test.ps1:419-421`: *"`gh` bi proxy container chan ca REST lan GraphQL"*.
2. **Hệ quả thật của câu mới `:726-727`** (*"`gh-kho=OK` KHÔNG nói lệnh `gh` đi GraphQL làm được"*): có hai adapter
   hướng dẫn `gh api graphql`, là `.claude/skills/work-packet/SKILL.md:33` (lấy spec) và
   `.claude/skills/cross-review/SKILL.md:541-557` (provenance). Ở phiên Claude Code, đường ấy ăn 403 do proxy, và
   `ops/land/*` có ba biên nhận đúng ca này. Câu CLAUDE.md đúng; hai adapter nằm ngoài PR.
3. **Thông điệp đầy đủ của proxy cho `/graphql`** (629 byte) còn chỉ sẵn "CCR routes" REST cho review threads,
   auto-merge, ready-for-review và convert-to-draft (`GET …/pulls/{n}/ccr/review_threads`, `PUT|DELETE …/ccr/auto_merge`, …).
   `:667` trích rút gọn có dấu "…", nên không sai. Tôi chỉ ghi lại vì nó nói `gh` porcelain có đường thay ở đâu.

## Phép đo lại

Tôi chỉ dùng GET và không in token. Ba vế: không token · `Authorization: Bearer $GITHUB_PAT` · `Bearer ghp_xxx…`
(giả). Log thô: `scratch/do_rest.{py,log,json}` (urllib 07:27:36–07:27:49Z), `scratch/do_rest_curl.log` (curl
07:28:10–07:28:21Z), `scratch/do_duong_con.{log,json}` (urllib 07:32Z), `scratch/do_duong_con_curl.log` (curl
07:40Z), `scratch/do_launcher_rest.log` (`_do_rest_github`, 07:36Z), `scratch/pr631_body_live.md`.

| Lời khai mới trong `DIFF.vong.patch` | Đo 2026-09-30 (phiên này) | Kết quả |
|---|---|---|
| `:143` 17-08: `/repos/<kho>` · `/pulls/N` → 403 do proxy | đối chiếu `:648-650` | ✓ trích đúng |
| `:144-146` 25-09 và 30-09: REST GET `/repos/<kho>`, PR, comment → 200 kèm `X-GitHub-*` | urllib + curl, 3 vế; 25-09: `d63cd40` ghi "REST tới `repos/…` trả 200 kèm `X-GitHub-*`" và đã đọc 5811128755 | ✓ 30-09 tái lập: `/repos/<kho>`, `/pulls/623`, `/pulls/631`, `/issues/comments/5811128755` đều 200, `Server: github.com`, 4 `X-GitHub-*` (urllib cả bốn; curl trừ `/pulls/623`). Vế 25-09 chỉ có lời khai của phiên ấy, không có header từng đường |
| `:146` `doctor` (`rest-kho`) chỉ hỏi `/repos/<kho>` | `launcher.py:3424-3438` | ✓ `rest-chung` = `/rate_limit`, `rest-kho` = `/repos/{slug}` |
| `:566-568` `07:11Z`, urllib, 3 vế: `collaborators` 403 proxy · `protection` 403 GitHub | urllib 07:27:47–07:27:49Z · curl 07:28:19–07:28:21Z · `_do_rest_github` | ✓ `collaborators`: 403, không `Server`, 0 `X-GitHub-*`, thân *"Access to this GitHub API path is not permitted through this proxy."* · `protection`: 403, `Server: github.com`, 4 `X-GitHub-*`, *"Resource not accessible by integration"* (launcher: `mo`, "toi GitHub, thieu quyen"). Giờ `07:11Z` là giờ phiên executor, KHÔNG ĐO ĐƯỢC. Trạng thái thì tái lập, và lượt 2 (06:49Z, `luot-2-opus-max/VERDICT.md:71-72`) với lượt này (07:27Z) kẹp hai phía, cùng kết quả |
| `:643-645` "403 bất kể token, theo ĐƯỜNG DẪN" vẫn đúng ở `/graphql` + 4 đường khác | như dưới | ✓ đúng 4 đường khác: `/search/issues`, `/user/repos`, `/repos/cli/cli`, `/collaborators` |
| `:661-662` bảng 25-09 trong thân PR #631: 4 đường, `/pulls/623`, chỉ `hdr_github=True` | GET `/pulls/631` → `body` | ✓ thân thật == `PR-BODY.md` (chỉ khác `\n` cuối): 8× `hdr_github=True`, 2× `pulls/623`, 1× `2026-09-25T01:1xZ`, không có `Server` |
| `:663-664` 30-09: 4 đường + `/pulls/631` → 200 CÓ `X-GitHub-*`, `Server: github.com`, 3 vế | urllib + curl | ✓ urllib: cả 6 đường (`/rate_limit`, `/user`, `/repos/<kho>`, `/pulls/623`, `/pulls/631`, comment); curl: 5 đường (trừ `/pulls/623`). 3 vế y hệt ở cả hai client |
| `:665-668` GET, 3 vế y hệt: 403, không `Server`, 0 `X-GitHub-*` ở `/graphql`, `/search/issues`, `/user/repos`, `/repos/cli/cli`, `/collaborators`; trích thông điệp GraphQL | urllib (5 đường) + curl (`/graphql`, `/collaborators`, `/repos/cli/cli`) | ✓ cả 5. Thông điệp thật: *"GitHub GraphQL is not available from Claude Code sessions; use the REST API (gh api repos/{owner}/{repo}/...). For review threads, …"*. Trích có "…" là đúng |
| `:667-668` biên nhận GraphQL 403 21-09 · 28-09 · 29-09 trong `ops/land/` | `git log -S` | ✓ `pr594…:523` thêm ở `a479699` (2026-09-21T18:11:22Z, **POST** `/graphql`), `pr666…provenance:10-11` ở `fcef7c3` (2026-09-28T16:30:42Z), `pr680…:146` ở `c928ba9` (2026-09-29T09:17:12Z). Cả ba đều là tổ tiên của `origin/master` |
| `:675-676` `doctor` không hỏi GraphQL | `rg -n -i graphql .claude/dev/launcher.py` | ✓ 0 hit. `gh-kho` = `gh api repos/{slug}` (`:3462`), là REST |
| `:678-681` các chỗ còn văn bản 403 | `rg --hidden` ngoài `ops/` | ✓ ba chỗ được liệt kê đều có thật (`launcher.py:1910-1939`, `:3363-3378`, `:3448-3459`; `session-start.sh:196-201`; `GOI_AGENT_DA_NEN.md:246-257`). Có thêm 3 chỗ đã được hàng rào phủ (xem Findings) |
| `:695-698` 21-09, phiên land #594, REST GET `commits/…` → 200, dòng thêm ở `b94182b` | `git log -S` + GET lại | ✓ (xem N4) |
| `:722-723` "GraphQL vẫn 403 do proxy (đo 30-09)" | GET `/graphql` | ✓ ở GET. POST thì tôi KHÔNG ĐO ĐƯỢC (chỉ được GET). Vế POST đứng trên biên nhận `a479699` (POST, 21-09) và `c928ba9` (truy vấn `node(id:)`, 29-09) mà `:667-668` đã dẫn, cộng thông điệp chính sách của proxy. Tôi không tính finding |
| `:726-727` `gh-kho` chỉ là một đường REST | `launcher.py:3460-3467` | ✓ |
| (thêm) 12 đường con theo kho khác | urllib 07:32Z + curl 07:40Z | 200 CÓ `X-GitHub-*` ⇒ **N5** |
| (thêm) `hooks` · `keys` · `actions/secrets` | như trên | 403 do proxy, giống `collaborators` |

## Cổng

Tôi chạy trong `cay-kho` tại `e271af6`, `core.abbrev=7`, `PYTHONDONTWRITEBYTECODE=1`, lúc 07:26:44Z.
`git status --porcelain --ignored` rỗng trước và sau, kể cả sau khi nạp `launcher.py` bằng importlib. HEAD vẫn là
`e271af6`. Log: `scratch/gate_e271af6.log`.
- `packet_loop.py doctrine-scan --root .` → **rc=0**, "sạch — đã quét 10 tệp, 0 chỗ chép doctrine".
- `packet_loop.py adr-song --root .` → **rc=0**, "50 ADR trên đĩa, 50 dòng trong §20, khớp 1–1 (tha thiếu trạng
  thái: ['0016'])".
- `tl.py doc-claims-check --strict --json` → **rc=0**, `ok=true`, `files_scanned=110`, `flags=0`, `advisory_count=381`,
  `CLAUDE.md` có trong `roots`.

Tôi chạy A/B nền và hint trên hai clone dựng trong cùng một lệnh (07:42:52Z). Ba cổng cho kết quả y hệt nhau: rc=0 ·
rc=0 · rc=0, 110 tệp, 381 advisory. Ba cổng này chỉ canh HÌNH THỨC (`:336-337`), nên không cổng nào thấy được N5.

Byte-giữ (việc 4):
- Có ba dòng chứa dấu chéo ngược + `u0308`: `:103` (dòng `co`+`\`+`u0308`+`dex` liền), `:104` và `:140`. Cả ba
  trùng byte ở `origin/master`, `d63cd40`, `af5edd3`, `aecc978`, `f174628`, `280ea34` và `e271af6`. U+0308 thật = 0,
  U+00F6 = 2 ở cả bảy revision.
- Mỗi thư mục review được so từ commit thêm nó tới `e271af6`, lệnh `git diff --quiet <commit thêm> e271af6 --
  ops/reviews/<dir>`, và cả ba đều rc=0: `pr631-review-1-claude` (thêm ở `bc5b7f6`), `pr631-review-1b-claude-cli`
  (`aecc978`), `pr631-review-2-opus-max` (`280ea34`). Tập blob cũng giống nhau. `git diff --name-status 280ea34
  e271af6` chỉ ra `M CLAUDE.md`.
- Mọi tệp trong `luot-*/` của sandbox trùng byte với bản trong kho. Sha256 của `luot-2-opus-max/*` và
  `luot-1b-claude-cli/*` khớp số ghi trong `RUN.md` tương ứng.

## KHÔNG ĐO ĐƯỢC
1. **POST `/graphql`** (tức cách `gh`/client GraphQL thật gọi): phạm vi của tôi chỉ là GET. Vế POST của lời khai
   `:723` đứng trên biên nhận của phiên khác (21-09, 29-09), tôi không đo lại được.
2. **`gh`**: container không có `gh`. Lệnh `gh` nào đi qua GraphQL là hiểu biết về `gh`, không phải phép đo ở đây.
3. **Giờ đo của executor** (`06:30–06:31Z`, `07:10Z`, `07:10–07:11Z`, `07:11Z`) và **"Hook phiên 30-09 in
   `rest-kho=OK` lúc 06:29Z"** (`:676`): không có biên nhận trong kho. Tôi tái lập được TRẠNG THÁI lúc 07:27–07:46Z,
   nhưng không tái lập được thời điểm của phiên kia. Tôi không chạy `doctor`, vì nó POST `initialize` tới MCP.
4. **Đọc qua MCP** (5811128755, các comment #238): phiên này không có công cụ MCP github, và JSON-RPC là POST.
5. **Tầng nào thay header Authorization**, và **nguyên nhân 403 → 200**: vẫn chưa tách được, như lượt 1b/2. Có một
   dữ kiện phụ mới: `packet_loop.py:1199-1202` ghi `protection` từng là 403 do proxy, nay là 403 do GitHub. Tức tập
   đường mà proxy cho qua đã đổi ở cả những đường không phải "việc thật". Dữ kiện này không định vị được thời điểm hay
   tầng.
6. **Ai đang giữ `CLAUDE.md`** (`ai-dang-giu`): tôi chưa chạy. `cay-kho` là READ-ONLY, và `origin` là mirror dựng từ
   kho cục bộ của executor chứ không phải GitHub, nên nó không trả lời được "lease nào đang giữ" (`:196-212`).
   Executor phải đo trên ref thật trước khi áp hint.
7. **Phương thức GHI qua REST** (`DELETE /git/refs/…` và các lệnh ghi khác): ngoài phạm vi, vì chỉ được GET.
