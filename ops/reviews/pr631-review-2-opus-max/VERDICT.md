verdict: changes_requested
reviewed_sha: f174628063fb55ee9f6b2f5f8a3dcca0e403dbe6
P1: 0   P2: 1   P3: 3
reviewer_provider: anthropic_claude
model_tu_khai: claude-opus-5-5 (Opus 5.5)
execution_surface_tu_khai: Claude Agent SDK trong container Linux 6.18.44-fc-v50 x86_64 · Python 3.11.15 · curl 8.5.0 · git 2.43.0 · KHÔNG có `gh` · có codex/claude/rg · HTTPS qua proxy cục bộ 127.0.0.1:42681 (lượt 1b ghi 40613, tức khác cổng) · GITHUB_PAT 93 ký tự, GH_TOKEN/GITHUB_TOKEN 14 ký tự · phiên KHÔNG có công cụ MCP github · đo 2026-09-30T06:44Z–06:58Z

Lượt 2, `advisory_review`. Reviewer và executor cùng provider (Anthropic), nên lượt này chỉ có giá trị tư vấn và
không thay được một lượt review khác provider. `cay-kho` ở `f174628`. `git diff aecc978 f174628` trùng byte với
`DIFF.vong1.patch`, và `git diff origin/master f174628` trùng byte với `DIFF.patch`. Bản vá vòng 1 chỉ đổi
`CLAUDE.md` (+58/−20). Lúc 06:45Z, REST vẫn trả head PR là `bc5b7f69…`, tức `aecc978`/`f174628` chưa được đẩy (khớp
PROMPT).

**Tóm tắt.** Bản vá đóng đúng F1, F3, F6, F8, L1-1, L1-3, L1-4. Còn một P2 và ba P3, và cả bốn đều do chữ mới của
chính bản vá:
- N1 (P2): bản vá tuyên *"MỌI câu 403 … ĐÃ TRÔI"* và bảo các câu về `gh` *"mất chân đỡ"*. Thật ra chỉ đường REST
  THEO KHO là trôi. Proxy vẫn chặn 403 bất kể token ở GraphQL, `/search`, `/user/repos`, kho khác và
  `/collaborators`, và kho đã có ba biên nhận GraphQL 403 từ trước bản vá.
- N2: số của phiên 30-09 bị ghép sang phiên 25-09.
- N3: danh sách chỗ còn văn bản 403 sót chính tệp "chi tiết" của mục này.
- N4: *"trôi hơn một tháng không ai thấy"* bị một biên nhận ngày 21-09 bác.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lệnh kiểm chung, chạy trong `cay-kho`:
`rg -n 'không còn để thử lại|chưa ai đo được|Nền đã đổi|cùng container remote|NAY CÓ|đã có client thứ hai thật|HAI DÒNG 403|Máy đã đúng sẵn|đúng phép đối chứng hai chiều của lượt 17-08|cấp danh tính hộ' CLAUDE.md`
→ chỉ còn **1** dòng (`:151`), và đó là chỗ trích *"bản trước khai …"*.

| # | Lượt | Hạng · lớp | Trạng thái | Bằng chứng |
|---|---|---|---|---|
| F1 | 1b | P1 `khai-vang-mat-khong-do` | **ĐÓNG** | Câu vắng mặt chỉ còn dạng trích ở `:151`. Tôi đo lại (`scratch/do_238.py`, 06:46:57Z): #238 có 9 comment. Cả 7/7 `posted_comment_id` (đọc từ `ops/leases/lease-dang-windows-*-20260822.yaml`) đều còn, đều `github-actions[bot]`, đều `created==updated` (22-08). Số `'` theo thứ tự tạo là **22/33/14/49/34/33/19**, 0 thực thể, 0 `&`. `urllib` và `curl` cho sha256 thân khớp 7/7. Phần giới hạn mới ở `:156-157` đứng được. |
| F2 | 1b | P2 `trang-thai-cu-khong-danh-dau` | **ĐÓNG-MỘT-PHẦN** | Phần đánh dấu đã đủ: mọi câu 403 của mục REST đều có nhãn (`:640-642`, `:655-658`, `:708-709`), và nhãn mơ hồ "HAI DÒNG" không còn. **Nội dung nhãn thì rộng hơn phép đo**: "MỌI câu 403 … ĐÃ TRÔI" và "`gh` … mất chân đỡ", trong khi GraphQL (đường của `gh` porcelain) và nhiều đường REST khác vẫn 403 do proxy → **N1**. Vế `gh` đóng sai, và đó cũng là chữ do chính hint lượt 1 và 1b gợi ra. |
| F3 | 1b | P2 `trang-thai-cu-khong-danh-dau` | **ĐÓNG** | `:562-568` đã có nhãn. Tôi tái lập: gốc `/` → **200**, thân `{}` (2 byte), không `Server`, 0 `X-GitHub-*`. Kết quả này đúng ở 5 vế `urllib` và 3 vế `curl`. Tuyên bố an toàn nay chỉ còn phạm vi `git-receive-pack`, và REST DELETE được ghi là KHÔNG ĐO ĐƯỢC. Có một cụm trong câu vá, *"`/repos/<kho>/…` thì 200"*, rộng hơn phép đo (`/collaborators` 403 do proxy, `/branches/master/protection` 403 do GitHub). Cụm này gộp vào N1 (hunk 1). |
| F4 | 1b | P2 `pham-vi-tuyen-bo-rong-hon-do` | **ĐÓNG-MỘT-PHẦN** | Mọi câu được chỉ đã sửa, và `rg` ở trên cho 0 hit với "Nền đã đổi", "cùng container remote", "NAY CÓ", "đã có client thứ hai thật". **Nhưng lớp này tái phát trong câu mới ở `:655-658`**, lần này theo trục ĐƯỜNG DẪN thay vì trục PHIÊN: đo 4 đường theo kho rồi tuyên "MỌI câu 403 … ĐÃ TRÔI" → **N1**. |
| F5 | 1b | P2 `chan-doan-sai-vi-sao-troi` | **ĐÓNG-MỘT-PHẦN** | Phần sửa sai "17-08 không ghi điều kiện" đã xong. Còn giữ tiền đề *"vẫn trôi hơn một tháng không ai thấy"*, và biên nhận trong kho bác chữ "không ai thấy": ngày 21-09 có phiên đã GỌI REST `/repos/<kho>/…` và nhận 200. Còn "hơn một tháng" thì không có phép đo nào đỡ → **N4**. |
| F6 | 1b | P3 `doi-chung-khong-rang` | **ĐÓNG** | Đã có vế token giả, và đã bỏ câu *"(đúng phép đối chứng hai chiều …)"*. Tôi tái lập: token giả (Bearer/`token`) cho 200, cùng `login=ducthangho`, cùng `Github-Authentication-Token-Expiration: 2026-09-30 08:22:21 UTC` ở mọi vế và cả hai client. |
| F7 | 1b | P3 `pham-vi-tuyen-bo-rong-hon-do` | **ĐÓNG-MỘT-PHẦN** | Câu "Máy đã đúng sẵn" đã bỏ. Câu "in OK từ trước" đã có nhãn "KHÔNG có biên nhận". Danh sách chỗ còn văn bản 403 cũ đã thêm vào. **Danh sách vẫn thiếu** `docs/GOI_AGENT_DA_NEN.md:246-257`, tức tệp "chi tiết" mà chính tiêu đề `:599` trỏ tới, và `launcher.py:1910-1935` (khối `gh` trong `CONG_CU`; lượt 1 đã chỉ `:1919-1920`) → **N3**. |
| F8 | 1b | P3 `thieu-dieu-kien-do` | **ĐÓNG** | `:142-143` đã có lại căn cứ (*"mục REST 17-08 …: `repos/…` → 403 do proxy"*). `:148-149` đã ghi phạm vi "trên comment ẤY". Công cụ MCP được khai thẳng là "không ghi; chưa đo lại". |
| L1-1 | 1 | P2 `bo-sot-cung-lop` (`:551`) | **ĐÓNG** | Giống F3. |
| L1-2 | 1 | P2 `tham-chieu-hep-bo-sot-menh-lenh-15-08` | **ĐÓNG-MỘT-PHẦN** | Đã có "HAI" → "MỌI", nhãn 15-08 ở `:640-642` và nhãn `t103` ở `:708-709`. Chữ "các hệ quả về `gh` đã mất chân đỡ" mà hint lượt 1 đề xuất thì đo ra là sai một phần → **N1**. |
| L1-3 | 1 | P3 `khai-rong-hon-phep-do` | **ĐÓNG** | "Nền đã đổi, KHÔNG phải lượt cũ đo sai" đã thay bằng "Nguyên nhân KHÔNG ĐO ĐƯỢC … thế chưa phải chứng minh" (`:661-663`). |
| L1-4 | 1 | P3 `khong-do-duoc-mot-phan-do-duoc` | **ĐÓNG** | Phần đo được đã được ghi ra: `/user` → `login` chủ kho (`:672`), tôi tái lập ở 5 vế. Nhãn KHÔNG ĐO ĐƯỢC nay chỉ còn gắn cho "tầng nào thay" và "17-08/25-09 có bị thay không". Hai điều này đúng là chưa đo được: 17-08 không có vế token giả. |

## Findings

`HINT.patch` phủ N1–N4: 5 hunk, +52/−28, chỉ sửa `CLAUDE.md`. Nó được kiểm như sau:
- `patch -p0 --dry-run` trên bản sao `scratch/thu/` → rc=0, bản sao không đổi.
- Áp thật trên bản sao thứ hai `scratch/thu2/` → rc=0, kết quả trùng byte với `scratch/sau/CLAUDE.md`.
- Ba dòng chứa dấu chéo ngược + `u0308` (`:103`, `:104`, `:140`) giữ nguyên byte, và U+0308 thật vẫn là 0.
- Dựng A/B trong **một** lệnh: hai clone từ `kho.git`, cùng ở `f174628`, một clone để nền, một clone đã áp hint.
  Ba cổng cho kết quả **y hệt** nhau (`scratch/gate_nen_vs_hint.log`).
- **Cổng đã bắt được bản nháp đầu của chính hint.** Bản nháp viết cụm "phiên land", và `doctrine-scan` trả **rc=6**
  (`[bang-vai-tro-muc-2] chép doctrine: 'phiên land'`). Tôi viết lại thành "phiên lập hồ sơ land", và cổng về rc=0.

**Trước khi áp:** executor phải chạy `ai-dang-giu CLAUDE.md`, vì tôi chưa đo được ai đang giữ tệp (xem KHÔNG ĐO ĐƯỢC).

### N1 · P2 · `pham-vi-tuyen-bo-rong-hon-do` · `CLAUDE.md:655-658` (và `:640-642`, `:565`)
**Lời khai (câu mới của bản vá):** *"MỌI câu 403 Ở TRÊN ĐÃ TRÔI Ở CÁC PHIÊN ĐÃ ĐO — trạng thái REST của 15-08
("REST … 403 bất kể token") và 17-08 (… "REST bị chặn ĐÚNG CHỖ làm việc"). Các câu SUY từ đó về `gh` — "cài cũng
vô ích", "MỌI lệnh việc thật ăn 403", "mọi thao tác kho trả 403" — mất chân đỡ"*. Chú thích 15-08 ở `:640-642`
cũng viết *"`gh` cài cũng vô ích" mất chân đỡ*.

Phép đo đỡ lời khai chỉ gồm **4 đường theo kho** (`/rate_limit` · `/user` · `/repos/<kho>` · `/pulls/N`), nhưng lời
khai phủ cả REST lẫn `gh`. Tôi đo thêm (`scratch/do_duong_khac.py`, 2026-09-30T06:49:46–06:49:55Z, `urllib`, ba vế
không token · `GITHUB_PAT` · token giả, kết quả y hệt nhau ở cả ba):
```
/graphql                                403  Server=None  X-GitHub-*=0  "GitHub GraphQL is not available from Claude Code sessions; use the REST API (gh api repos/{owner}/{repo}/...)…"
/search/issues?q=…                      403  Server=None  X-GitHub-*=0  "…sessions are bound to their configured repositories. Use repository-scoped endpoints…"
/user/repos                             403  Server=None  X-GitHub-*=0  (cùng thân trên)
/repos/cli/cli                          403  Server=None  X-GitHub-*=0  "GitHub access to this repository is not enabled for this session. Use add_repo…"
/repos/<kho>/collaborators              403  Server=None  X-GitHub-*=0  "Access to this GitHub API path is not permitted through this proxy."
/repos/<kho>/branches/master/protection 403  Server=github.com  X-GitHub-*=4  "Resource not accessible by integration"
/repos/<kho>/{rulesets,rules/branches/master,branches/master,git/refs/heads/master,actions/runs} 200 CÓ X-GitHub-*
```
Tôi đo lại bằng chính bộ phân loại của kho (`scratch/do_launcher_rest.log`, 06:57:47Z; nạp `launcher.py` bằng
importlib, không ghi bytecode): `_do_rest_github` trên `/graphql` trả `tt=chan`, `"HTTP 403 (KHONG header GitHub ->
proxy tu sinh)"` ở cả ba vế token. Trên `/repos/ducthangho/tra-luat` nó trả `mo`/`OK` ở cả ba vế, kể cả token giả.

Rút ra ba điều:
- **Chính sách theo ĐƯỜNG DẪN của proxy vẫn sống, bất kể token.** Thứ đã trôi là TẬP đường được mở (nay có đường
  theo kho), không phải bản thân câu *"REST … 403 bất kể token"*. Câu 17-08 *"theo ĐƯỜNG DẪN"* vẫn đúng.
- **Các câu về `gh` không mất chân đỡ, chỉ đổi chân đỡ.** GraphQL đang 403 do proxy, và chính thông điệp của proxy
  bảo người dùng `gh` chuyển sang `gh api repos/…`. Kho cũng đã có biên nhận GraphQL 403 từ TRƯỚC bản vá, cả ba đều
  nằm trên `origin/master`. Ngày dưới đây là ngày dòng được thêm (`git log -S`):
  `ops/land/pr594-wp578-land-evidence.yaml:523` (`80d4dd4`, 21-09), `ops/land/pr666-wp650-provenance.yaml:10-11`
  (`fcef7c3`, 28-09), `ops/land/pr680-wp676-land-evidence.yaml:146` (`c928ba9`, 29-09). Đây lại là bệnh *"hỏi chỗ
  tiện tay thay vì hỏi chỗ kết luận được ghi"*, vốn chính là gốc của F1.
- **Người đọc sẽ hành động sai.** Người làm theo `:640-642` sẽ cài `gh` và tin `gh-kho=OK`. Nhưng `gh-kho` chỉ chạy
  `gh api repos/<slug>` (`launcher.py:3462`), tức REST, nên nó xanh. Trong khi đó lệnh `gh` nào đi qua GraphQL thì ăn
  403. Đây đúng hình dạng `t103` mà `:703-711` dạy. Riêng việc `gh` porcelain dùng GraphQL là hiểu biết về `gh`,
  **KHÔNG ĐO ĐƯỢC** ở đây vì không có `gh`. Chính vì thế văn bản phải nói "chưa đo, và đường GraphQL đang chặn" chứ
  không được nói "mất chân đỡ".

Ở `:565`, cụm *"`/repos/<kho>/…` thì 200 CÓ `X-GitHub-*`"* dùng dấu "…" để phủ mọi đường con, nhưng hai đường con
đo được cho kết quả khác (xem bảng).

**Vì sao P2 mà không P1:** vế REST-theo-kho của nhãn là đúng, và vế `gh` đã tự rào bằng "KHÔNG ĐO ĐƯỢC". Chỗ sai là
đã bỏ sót một chân đỡ đo được, và cái sót ấy dẫn người đọc hành động sai. Đó là định nghĩa P2.

**Sửa:** hunk 1, 2, 3 và 5 của `HINT.patch`.
- Thu nhãn về đúng "đường REST THEO KHO".
- Ghi các đường vẫn 403 do proxy, kèm ngày và ba vế token.
- Ghi rằng câu `gh` chỉ mất chân đỡ CŨ, còn chân đỡ MỚI là GraphQL 403 (dẫn ba biên nhận).
- Ghi rằng `gh-kho=OK` không có nghĩa là mọi lệnh `gh` làm được việc.
- Thu cụm "…" ở `:565` về "các đường đã đo".
- Nhãn `t103` ghi thêm "GraphQL vẫn 403 (đo 30-09)".

### N2 · P3 · `ghep-sai-luot` · `CLAUDE.md:658-661`
**Lời khai:** *"Đo `2026-09-25T01:1xZ` (một phiên remote) và `2026-09-30T06:30–06:31Z` (…): `/rate_limit` · `/user`
· `/repos/<kho>` · `/repos/<kho>/pulls/631` đều **200 CÓ `X-GitHub-*`**, `Server: github.com`."*

Lúc 01:1xZ ngày 25-09 thì PR #631 **chưa tồn tại**. REST GET `/pulls/631` → `created_at: 2026-09-25T01:35:03Z`, và
commit đầu `d63cd40` là 01:34:28Z (`git log --date=iso-strict origin/master..f174628`). Bảng đo 25-09 trong
`PR-BODY.md` ghi `/pulls/623` và chỉ ghi `hdr_github=True`, không có `Server`. Như vậy `/pulls/631` và
`Server: github.com` là số của phiên 30-09 bị gán sang phiên 25-09. Đây đúng bệnh *"ghép sai lượt"* mà `:327-331`
tố cáo, và nó nằm ngay trong câu dạy "ghi PHẠM VI (phiên nào)".
**Sửa:** tách số theo phiên (hunk 3).

### N3 · P3 · `pham-vi-tuyen-bo-rong-hon-do` (tiếp F7) · `CLAUDE.md:667-669`
**Lời khai:** *"Văn bản 403 cũ cũng KHÔNG chỉ nằm ở đây: `_do_github` cùng chú thích quanh nó trong
`.claude/dev/launcher.py`, và khối "KHONG cai `gh`" trong `.claude/hooks/session-start.sh`."*

Câu này đọc như một danh sách đủ, nhưng còn sót:
```
rg -n 'CHẶN|cài cũng vô ích' docs/GOI_AGENT_DA_NEN.md   # :252 "REST thẳng … **CHẶN**" · :253 "`gh` … **cài cũng vô ích**"
sed -n '1910,1935p' .claude/dev/launcher.py              # khối `gh` của CONG_CU: "/repos/<kho> -> 403 … MOI lenh viec that … an 403"
```
- `docs/GOI_AGENT_DA_NEN.md:246-257` (mục "GitHub: bốn đường, hỏng độc lập") là **tệp "chi tiết" mà chính tiêu đề
  mục trỏ tới** (`CLAUDE.md:599`). Bảng "trạng thái (đo 15-08-2026)" ở đó vẫn khai REST CHẶN và `gh` "cài cũng vô
  ích". Chữ "chính sách theo đường dẫn" ở `:256` thì vẫn đúng (N1).
- `launcher.py:1910-1935` nằm cách `_do_github` (`:3363`) khoảng 1450 dòng, nên cụm "quanh nó" không phủ tới. Chú
  thích này đang đỡ quyết định `"bat_buoc": {"remote": False}` của `gh` (`:1935`). Lượt 1 đã chỉ đúng `:1919-1920`.

Bản vá liệt kê đúng những chỗ lượt 1b chỉ và sót những chỗ không ai chỉ. Đây là hình dạng `VÁ ĐÚNG CHỖ ĐƯỢC CHỈ
RỒI BỎ SÓT ĐƯỜNG THỨ BA` (`:525-545`). Hồ sơ lịch sử có ngày trong `ops/` (specs/land/prompts/handoff, và
`ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` đã "ĐÃ RÚT") thì KHÔNG cần đưa vào danh sách.
**Sửa:** mở rộng danh sách (cuối hunk 3).

### N4 · P3 · `chan-doan-sai-vi-sao-troi` (tiếp F5) · `CLAUDE.md:683-684`
**Lời khai:** *"Lượt 17-08 CÓ ghi ngày và hai vế token mà vẫn trôi hơn một tháng không ai thấy"*.

- *"không ai thấy"* là lời khai VẮNG MẶT, và kho có biên nhận bác nó.
  `ops/land/pr594-wp578-land-evidence.yaml:579` ghi `REST GET /repos/ducthangho/tra-luat/commits/8394f741… (HTTP
  200)`, dòng được thêm ở `b94182b` lúc 2026-09-21T17:47:06Z. Các dòng `:268`, `:286-288` ghi REST timeline #601 và
  `pulls/601/reviews` lúc ~18:45Z–19:05Z ngày 21-09. Vậy một phiên đã **dùng** trạng thái mới 4 ngày trước phép đo
  25-09, và `CLAUDE.md` vẫn đứng nguyên.
  Kiểm bằng `git log -S 'commits/8394f7411bfbeacdd1b6d5eafda21473f6487268' -- ops/land/pr594-wp578-land-evidence.yaml`.
- *"hơn một tháng"* là một con số không có phép đo. Không biết trạng thái lật lúc nào. Biên nhận 20-09
  (`ops/specs/THU-HOI-LEASE-A1a.md:98`) nói về kho NGOÀI (`actions/upload-artifact`), nên không dùng làm mốc được.
- Chẩn đoán còn lại, *"không gì đối chiếu văn bản với phép đo sống"*, thì đúng, và ca 21-09 còn làm nó mạnh hơn.
**Sửa:** hunk 4.

## Phép đo lại

Chỉ GET, không in token. Log thô nằm trong `scratch/`: `do_rest.{py,log,json}`, `do_rest_curl.log`,
`do_rest_curl2.log`, `do_238.{py,log}`, `do_duong_khac.{py,log,json}`, `do_launcher_rest.log`.

| Lời khai trong `DIFF.vong1.patch` | Đo 2026-09-30 | Kết quả |
|---|---|---|
| `:562-564` gốc `/` → 200 `{}` 2 byte, không `Server`/`X-GitHub-*`, 3 vế, 2 client | `urllib` 5 vế (06:45Z) · `curl` 3 vế (06:47Z; dòng HTTP cuối là `HTTP/1.1 200 OK`) | ✓ tái lập |
| `:659-661` bốn đường đều 200 CÓ `X-GitHub-*`, `Server: github.com` | như trên | ✓ ở phiên 30-09 (4 header `x-github-*`). ✗ ở phiên 25-09 cho `/pulls/631` và `Server` ⇒ **N2** |
| `:670-674` token giả vẫn 200 · cùng `login` · cùng `Github-Authentication-Token-Expiration` `2026-09-30 08:22:21 UTC` · "chưa tới 2h sau lúc đo" | `urllib` 5 vế + `curl` 3 vế | ✓ `login=ducthangho`, expiration giống hệt lúc 06:45–06:49Z. Tính từ 06:30–06:31Z thì còn 1h51–1h52, tức "chưa tới 2h" ✓ |
| `:672` `/rate_limit` · `/user` · `/repos/<kho>` · `/pulls/631` vẫn 200 với token giả | như trên | ✓. PR #631 `open`, head `bc5b7f69…` |
| `:676` `rest-kho=OK` chỉ đòi 2xx kèm `X-GitHub-*` | đọc `launcher.py:2974-3015` và gọi thẳng `_do_rest_github` | ✓ `ok = co_gh and 200<=status<300`. `/repos/<kho>` → `OK` ở cả 3 vế, kể cả token giả |
| `:146-148` 5811128755: 44 `'` · 8 `>` · 3 `<` · 0 thực thể; `urllib`/`curl` khớp băm | 5 vế `urllib` + 3 vế `curl` | ✓ 44 · 8 · 3 · 2 `"` · 0 `&` · 0 thực thể. sha256 thân `837f9c28…` ở mọi vế. `github-actions[bot]`, `created==updated` 2026-09-24T09:02:18Z |
| `:153-155` 7/7 comment lease còn trên #238 · `created==updated` · `'` = 22/33/14/49/34/33/19 · 0 thực thể · 0 `&` · hai client khớp băm | `do_238.py` | ✓ đủ cả. Dãy số là theo thứ tự TẠO (cũng là thứ tự id). Theo thứ tự tên tệp thì khác (22/33/49/33/14/34/19) |
| thêm: thân issue #238 | `urllib` 5 vế | `ducthangho` (OWNER), 0 `'` · 6 `"` · 3 `>` · 0 thực thể. Chỉ là dữ liệu phụ: không biết thân này có bị sửa sau 22-08 không (`updated_at` 23-08 cũng đổi khi có comment mới) |
| thêm: đường khác của REST/GraphQL | `do_duong_khac.py` + `_do_rest_github` | xem N1 |

## Cổng

Chạy trong `cay-kho` tại `f174628`, `core.abbrev=7`, `PYTHONDONTWRITEBYTECODE=1`. `git status --porcelain --ignored`
rỗng cả trước lẫn sau, kể cả sau khi nạp `launcher.py` bằng importlib. HEAD vẫn là `f174628`.
- `packet_loop.py doctrine-scan --root .` → **rc=0**, "sạch — đã quét 10 tệp, 0 chỗ chép doctrine".
- `packet_loop.py adr-song --root .` → **rc=0**, "50 ADR trên đĩa, 50 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])".
- `tl.py doc-claims-check --strict --json` → **rc=0**, `ok=true`, `files_scanned=110` (`CLAUDE.md` có trong
  `roots`), `flags=[]`, `advisory_count=381`. Con số này bằng số lượt 1b đo ở `af5edd3`.

Chạy A/B, nền và hint, trên hai clone dựng trong cùng một lệnh: ba cổng y hệt nhau (rc=0 · rc=0 · rc=0, 110 tệp, 381
advisory). Ba cổng này chỉ canh HÌNH THỨC (`:335-337`), nên không cổng nào có thể thấy N1–N4.

Byte-giữ (việc 4):
- Có 3 dòng chứa dấu chéo ngược + `u0308`: `:103` (dòng có `co`+`\`+`u0308`+`dex` liền), `:104` và `:140`. Cả ba
  trùng từng byte giữa `origin/master`, `aecc978` và `f174628`. Số U+0308 thật là 0 ở cả ba revision; U+00F6 là 2.
- `git diff --quiet aecc978 f174628 -- 'ops/reviews/pr631-review-1*'` → rc=0. Sáu blob có sha giống nhau. `git diff
  --name-status aecc978 f174628` chỉ ra `M CLAUDE.md`. `luot1/*` và `luot1b/*` trùng byte với bản trong kho.

## KHÔNG ĐO ĐƯỢC
1. **Đọc qua MCP** (5811128755, 7 comment #238): phiên này không có công cụ MCP github, và JSON-RPC là POST, nằm
   ngoài phạm vi chỉ GET. Lời khai `:148-149` là lời khai của phiên 25-09, và bản vá đã tự ghi "chưa đo lại".
2. **`gh`**: container không có `gh`. Việc lệnh `gh` nào đi qua GraphQL là hiểu biết về `gh`, không phải phép đo ở
   đây. Thứ đo được là đường `/graphql` 403 do proxy, và thông điệp của chính proxy chỉ `gh` sang `gh api repos/…`.
3. **"Hook phiên 30-09 in `rest-kho=OK` lúc 06:29Z"** (`:666`): không có biên nhận trong kho, và tôi không chạy được
   `doctor` vì nó POST `initialize` tới MCP. Phần tương đương mà tôi đo được là `_do_rest_github` trên
   `/repos/<kho>` → `OK` lúc 06:57Z, ở phiên của tôi.
4. **Tầng nào thay header Authorization**: proxy cục bộ hay proxy egress, chưa tách được. Có hai dữ kiện phụ. Một:
   GitHub gọi credential được chèn là *"integration"* (`/branches/master/protection` → *"Resource not accessible by
   integration"*). Hai: `docs/GOI_AGENT_DA_NEN.md:706` đã ghi cơ chế "proxy egress … tự chèn credential" cho `git`
   (24-08). Cả hai đều không định vị được tầng cho REST.
5. **Nguyên nhân 403 → 200 ở 15-08/17-08**: vẫn chưa tách được. Hôm nay đo được proxy ràng buộc phiên với kho đã
   cấu hình, và thân 403 cho kho chưa gắn gần như trùng chữ thân 15-08. Đó là giả thuyết có dữ kiện đỡ, chưa phải
   phép đo của phiên cũ.
6. **Thời điểm REST theo kho lật từ 403 sang 200**: biên nhận sớm nhất có 200 là 21-09 (N4). Các câu 403 trong hồ sơ
   tháng 9 (`ops/land/pr480/487/489/493`) là đo mới hay chép lại câu cũ thì tôi không tách được.
7. **Phương thức GHI qua REST**: chỉ được GET.
8. **Người đang giữ `CLAUDE.md`** (`ai-dang-giu`): chưa chạy. Cây là READ-ONLY, và `cay-kho` chỉ có 13 nhánh
   `refs/remotes/origin/*` (mirror `kho.git` có 77 ref). Mirror dựng từ kho cục bộ của executor, không phải từ
   GitHub, nên không thể dùng nó để trả lời "lease nào đang giữ" (`:212-219`). Executor phải đo trên ref thật trước
   khi áp hint.
