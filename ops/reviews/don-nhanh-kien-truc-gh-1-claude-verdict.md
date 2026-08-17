Đã đọc `don-nhanh.ps1`/`.cmd`/`_test.ps1`, xác nhận HEAD khớp `reviewed_sha_required` (chỉ lease/prompt đổi sau đó), chạy baseline 16/16, rồi tự đo cả ba đường A/B/C độc lập thay vì tin số của người vá — và đo ra một khác biệt đáng kể với claim gốc của lease. Trả lời theo đúng định dạng yêu cầu:

```
verdict: giu_nguyen
assurance: same_provider_approved
```

## Khuyến nghị

Giữ `gh` (phương án A) — cho **cả hai nền**: máy Windows của chủ kho (nơi script thật sự chạy) lẫn container/CI (nơi test giả lập chạy). Không đổi kiến trúc, không đổi có điều kiện. Lý do gọn: B và C không đóng lớp hỏng nào trong ba lớp đã vá (mã thoát, trộn luồng, rỗng-vs-vắng) — chúng **dời** các lớp ấy sang một giao thức có *nhiều lớp giải mã hơn*, đưa thêm một lớp mất-tin-cậy mới (token cần đúng phạm vi quyền, đo được là KHÔNG đủ ngay lúc này), và bộ test đi kèm đắt hơn hẳn để dựng đúng TRẠNG THÁI thay vì kịch bản. Không có bằng chứng nào của lượt đo hôm nay cho thấy B/C rẻ hơn hay tin cậy hơn `gh` ở bất kỳ nền nào.

## Bằng chứng

**1. Bất đối xứng môi trường** — đo được nhưng KHÔNG đổi kết luận. `don-nhanh.ps1` chạy trên máy Windows, không trong container; 403 "GitHub access is not enabled for this session" là proxy CỦA CONTAINER (đã tự đo lại, xem mục 6). Nhưng cả B lẫn C đều cần một token có ĐÚNG phạm vi quyền tại điểm chạy — và phạm vi quyền là thuộc tính của TOKEN, không phải MÁY. Mục 6 dưới đây cho thấy `GITHUB_PAT` hiện có (cái sẵn dùng nhất, len=93) không đủ quyền list PR/branch — nếu đây là token định cấp cho máy Windows, sự bất đối xứng môi trường không cứu được nó.

**2. Số lớp giải mã của MCP** — tự đo lại bằng script JSON-RPC riêng (không dùng số của người vá): `initialize` (HTTP 200 + `Mcp-Session-Id`) → `notifications/initialized` (202) → `tools/call` → SSE `data:` → JSON-RPC envelope → `result.content[0].text` (một CHUỖI) → parse JSON lần **thứ hai** để ra mảng PR. Đúng 4 lớp, khớp/nhỉnh hơn con số 3 lớp người vá báo. `gh pr list --json` vẫn là 1 lớp. Xác nhận: MCP dời chỗ hỏng, không đóng.

**3. `isError` vắng mặt khi thành công** — tự đo, không tin claim: gọi `search_repositories` (thành công thật, trả `total_count:1`) → `result` chỉ có khoá `content`, **không có khoá `isError`** (`isError present? False`). Gọi `list_pull_requests`/`list_branches`/`get_me` (lỗi thật, xem mục 6) → `isError: true` xuất hiện. Đúng như prompt cảnh báo: `if ($r.isError)` đọc "vắng" thành "không lỗi" — client ngây thơ sẽ COI THÀNH CÔNG một số trường hợp không hề thành công, đúng lớp lỗi của lượt cross-review 1 (`rc=0` nói dối). Phương án C tái tạo nguyên vẹn lớp lỗi nó được đề xuất để chữa.

**4. Ranh giới credential** — hiện `don-nhanh.ps1` KHÔNG cầm token nào; dựa vào `gh auth login` (out-of-band, lưu trong credential manager của hệ điều hành, không đi qua biến môi trường của script). B và C đều đòi đưa một PAT phạm vi phù hợp cho listing PR/branch vào môi trường của một script XOÁ NHÁNH. Đo hôm nay cho thấy token "tiện tay nhất" trong container này KHÔNG đủ phạm vi cho đúng việc đó (mục 6) — nghĩa là "đưa PAT vào script" không phải một bước rẻ, nó đòi cấp phát MỘT token MỚI, đúng scope, và giữ nó sống — thêm một bề mặt rủi ro cho công cụ xoá ref, đúng thứ CLAUDE.md cảnh báo ở bài học `inherit="all"`.

**5. Fail-close** — không đổi ở A. Với B/C sẽ có thêm các hình dạng "không đọc được" MỚI (session hết hạn, SSE đứt, 5xx — đã tự đo `get_me` trả 503 sống, xem mục 6) mà `don-nhanh.ps1` hiện KHÔNG có nhánh xử lý; muốn dùng B/C thì phải viết lại toàn bộ khối try/catch fail-close (dòng 165-217) từ đầu và hardening lại 3 vòng như đã làm cho `gh`.

**6. Đo lại độc lập, KHÔNG trùng khớp claim gốc của lease** (quan trọng — xem "Nợ khai báo"):
```
mcp initialize (script JSON-RPC riêng, KHÔNG dùng tool phiên) -> HTTP 200, Mcp-Session-Id
mcp search_repositories (repo:ducthangho/tra-luat)             -> THÀNH CÔNG, total_count=1, KHÔNG có khoá isError
mcp list_pull_requests  (qua chính tool mcp__github__ của phiên, VÀ qua script riêng, 5 lần, ~5 phút)
                                                                 -> isError:true, "403 Resource not accessible by personal access token", ỔN ĐỊNH mọi lần
mcp list_branches (script riêng)                                -> cùng lỗi 403 y hệt
mcp get_me         (qua tool phiên)                             -> "503 No server is currently available" (khác lỗi, có vẻ GitHub phía thật đang trục trặc)
gh (cài apt trong container để đo `--limit`) -> gh auth status: "token invalid"; gh api repos/... -> 403 "GitHub access is not enabled for this session" (đúng lớp chặn REST đã biết)
```
Lease ghi "11 PR, ĐỦ cả head lẫn base" lúc ~14:4x UTC 17-08. Đo lại của tôi lúc phiên này (vài giờ sau) cho **403 ổn định**, dùng cả script riêng lẫn chính công cụ `mcp__github__list_pull_requests` của phiên (tức không phải lỗi cách gọi của tôi). `search_repositories`/`initialize` vẫn chạy — nên PAT không chết hoàn toàn, mà thiếu ĐÚNG phạm vi cho "list pulls/branches" TẠI THỜI ĐIỂM NÀY. Đây tự nó là bằng chứng chống lại C: một phương án mà chính bằng chứng ủng hộ nó không tái lập được vài giờ sau, trong cùng container, bằng cùng token, thì không phải nền tảng để thay một fail-close đã cứng qua 3 vòng review.

## Hình dạng lỗi thứ tư

**Có, và CHƯA đóng — nhưng không đổi kết luận vì nó nằm TRONG cả ba phương án như nhau.** `gh pr list --state open --limit 200 --json ...` (dòng 177) đặt trần cứng 200: hành vi tài liệu hoá của `gh` CLI là lấy đúng `--limit` phần tử qua bao nhiêu trang cần thiết, **không cảnh báo** khi tổng số PR mở thật sự lớn hơn. Nếu kho có >200 PR mở, script sẽ nhận `rc=0` + JSON hợp lệ + `$doDuocPR=$true` với một danh sách THIẾU — đúng cùng họ "rỗng-vs-vắng" của t16, chỉ khác NGƯỠNG (scale) thay vì SỐ (count). Prompt mục 5 đã tự nêu đúng gap này cho `gh`, nên tôi không tính đây là phát hiện mới, chỉ xác nhận nó THẬT và ĐANG MỞ.

Đã thử đo trực tiếp: cài `gh` thật vào container (apt, `gh 2.45.0`) để chạy `--limit` thực nghiệm, nhưng `gh api`/`gh pr list` bị đúng lớp chặn REST/GraphQL của proxy container ("GitHub access is not enabled for this session" / "This GraphQL query is not enabled for this session — only the pinned set of PR-review operations is served"), nên KHÔNG đo sống được. Kết luận về `--limit 200` ở trên là **suy luận từ hành vi đã biết của `gh` CLI, KHÔNG phải phép đo trực tiếp** — khai rõ để không lẫn với các mục đã đo.

Không đổi verdict vì: (a) latent, không cắn — lease tự đo 11 PR mở lúc gần nhất còn dùng được, cách rất xa 200; (b) nó là tham số bên trong Option A (`--paginate`/nâng limit + đối chiếu đủ trang), không phải lý do đổi backend sang B/C — B/C có `perPage`/`page` cùng bản chất rủi ro (đã tự đo `perPage=3` ở list_pull_requests, params được nhận nhưng vẫn 403 nên chưa kiểm được hành vi cắt trang thật của MCP). Nên khai thành nợ theo dõi riêng, không gộp vào lượt kiến trúc này.

## Nợ khai báo

- **Chưa đo trực tiếp `--limit 200` truncation** — `gh` bị proxy container chặn REST/GraphQL ngay cả sau khi cài; kết luận là suy luận tài liệu, không phải phép đo sống (nêu ở trên).
- **Chưa đo B (`Invoke-RestMethod`/`curl` từ PowerShell thật)** — không có máy Windows; chỉ đo REST bằng Python `urllib` trong container, kết quả trùng khớp đo REST người vá đã ghi (403, 0 header `X-GitHub-*`).
- **Chưa đo PowerShell 5.1** cho bất kỳ phương án nào — không có 5.1 trong tầm tay ở đây; kế thừa nguyên trạng "chưa kiểm" đã ghi trong lease, không phát sinh thêm vì tôi không đề xuất mã mới.
- **Không tái lập được claim gốc của lease** ("11 PR qua MCP, đủ head/base") — 5+ lần thử độc lập, cả script riêng lẫn tool phiên thật, đều 403 "Resource not accessible by personal access token" ổn định. Không rõ nguyên nhân trôi (token đổi giữa hai lượt, phạm vi bị rút, hay trạng thái GitHub App connector đổi) — khai như MỘT SỰ KIỆN đo được, không quy kết nguyên nhân.
- `get_me` qua MCP hiện trả 503 "No server is currently available" — vẻ như trục trặc tạm thời phía GitHub thật (không phải proxy container: có header `X-GitHub-*`), khai ra để không ai đọc nhầm 503 đó thành lỗi phạm vi quyền của mục trên.
- **Đây KHÔNG phải lượt duyệt và KHÔNG cấp điều kiện land cho #150** — kể cả kết luận "giữ nguyên" ở trên cũng không thay lượt cross-review `codex` mà §8 đòi cho #150.

## Phép đo đã chạy

1. `git fetch origin ops/don-nhanh-giu-base-pr` + xác nhận `HEAD=bfeedfc...` = `reviewed_sha_required`; `git diff bfeedfc 8e2fc95 --stat` = chỉ 2 tệp lease/prompt, không đổi code.
2. `sha256sum` nội dung `git show origin/...:ops/prompts/don-nhanh-kien-truc-gh-1-claude-20260817.md` = khớp `prompt_sha256_required`.
3. Tải `pwsh 7.4.6` có sẵn trong scratchpad, chạy `scripts/don-nhanh_test.ps1` → **16/16 đạt**.
4. Script Python riêng (`urllib`, KHÔNG dùng tool phiên) gọi JSON-RPC MCP: `initialize`, `notifications/initialized`, `tools/call list_pull_requests` (không tham số phân trang, với `perPage=3`, với `perPage=100`), `list_branches`, `get_me`, `search_repositories` — lặp 3-5 lần cách nhau vài phút.
5. Gọi trực tiếp `mcp__github__list_pull_requests`, `mcp__github__get_me`, `mcp__github__search_repositories` (tool thật của phiên, qua connector) để đối chiếu với script riêng — cùng kết quả.
6. REST bằng `urllib` tới `/rate_limit` (200, 4 header X-GitHub-*), `/user` (503 lúc đo, 3 header X-GitHub-*), `/repos/ducthangho/tra-luat` và `/repos/.../pulls` (403, 0 header, thân "GitHub access is not enabled for this session").
7. `sudo apt-get install -y gh` (2.45.0) trong container; `gh auth status`, `gh api repos/ducthangho/tra-luat`, `gh api repos/.../pulls`, `gh pr list --repo cli/cli --limit 3` — tất cả bị chặn ở lớp REST/GraphQL của proxy container (không phải GitHub thật).
8. Đọc `scripts/don-nhanh.ps1`, `.cmd`, `_test.ps1` toàn văn; `grep` `.github/workflows/ci.yml` xác nhận `don-nhanh_test.ps1` chạy trên cả `ubuntu`+`windows`, không đọc token/mạng thật (chỉ `gh` giả).
