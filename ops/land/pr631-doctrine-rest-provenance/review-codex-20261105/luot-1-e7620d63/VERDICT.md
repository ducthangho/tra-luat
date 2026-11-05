verdict: changes_requested
reviewed_sha: 6e5c74849af68e748c4844bedf5856ead4c60be3
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Reviewer: `openai_codex`, phiên độc lập, review offline qua Codex với công cụ shell cục bộ; transport `machine`. Không suy danh tính model/effort từng request từ tên công cụ. Phạm vi: `9091cf52cf20ac197c1a356d6a33cac6bab0b318..6e5c74849af68e748c4844bedf5856ead4c60be3`, gồm `CLAUDE.md` (+82/−4) và 18 hiện vật review. HEAD đúng SHA yêu cầu; tree `ffb3654a010b80c5035264d9af02f087371eb46b`; worktree sạch lúc bắt đầu. Áp ngưỡng của chỉ thị: phải hết cả P0/P1/P2/P3 mới approve.

## Finding

| ID | Mức | Tệp:dòng | Trích nguyên văn | Vì sao | Cách sửa đề xuất |
|---|---|---|---|---|---|
| F1 — phép đo chưa có neo vẫn được kể như đã xác nhận | P2 | `CLAUDE.md:728`, `CLAUDE.md:743` | «`2026-09-30T07:51–07:57Z` (14 đường: `urllib` cả 14, `curl` 10; ba vế y hệt)»; «Hook phiên 30-09 in `rest-kho=OK` lúc 06:29Z» | Các chi tiết về **chính lần chạy, thời điểm và độ phủ client** không có biên nhận tương ứng trong cây được review. `ops/reviews/pr631-review-4-opus-max/VERDICT.md:155` và `:196` nói rõ không có biên nhận cho giờ `07:51–07:57Z` và không biết `curl` phủ 10 đường nào. `pr631-review-2-opus-max/VERDICT.md:193` và `pr631-review-3-opus-max/VERDICT.md:183` cũng ghi lần hook `06:29Z` không có biên nhận. Những lần reviewer đo lại ở giờ khác đỡ **trạng thái HTTP**, không chứng minh executor đã chạy bộ đo/hook vào giờ được khai. Câu sau ở `CLAUDE.md:744` chỉ rút lời khai mạnh hơn “từ trước khi mục này được sửa”, vẫn để lời khai `06:29Z` ở dạng khẳng định. Theo yêu cầu phải neo được cả ngày giờ và số đếm, phạm vi xác nhận ở đây vượt bằng chứng. | Với bộ 14 đường, dẫn thẳng các phép đo có biên nhận, giữ đúng giờ và độ phủ client của từng reviewer (`pr631-review-3-opus-max/VERDICT.md:78`, `:138`; `pr631-review-4-opus-max/VERDICT.md:145`). Ghi riêng giờ/độ phủ executor là lời khai chưa có log gốc, **KHÔNG ĐO ĐƯỢC**, hoặc bổ sung biên nhận của đúng lần chạy. Với hook, bỏ mốc `06:29Z` hoặc gắn cùng nhãn chưa kiểm chứng cho toàn bộ câu, cho tới khi có đầu ra hook của đúng phiên. |

F1 là một lớp lỗi với hai biểu hiện. Đây là thiếu neo của lời khai về lần chạy cụ thể, **không phải** finding chỉ vì reviewer không gọi mạng đo lại REST. Không kết luận các mã HTTP được kể là sai. Những mốc executor khác cùng tình trạng (`06:30–06:31Z`, `07:10–07:11Z`, `07:11Z`) cũng cần cùng cách ghi; biên nhận lượt 3, dòng 183–185 đã phân biệt chúng với giờ đo của reviewer.

Đối chiếu tại chỗ: `rg --hidden -n -g '!.git/**'` với các mẫu `rest-kho=OK`, `2026-09-30T07:51`, `2026-09-30T06:29`, `07:51–07:57` trong `cay-kho` chỉ cho lời khai, bản patch và những nhận xét review kể trên; không cho log gốc của hai lần chạy. Lời khai `doctor` trong review 1 nói về phiên đo `2026-09-29T23:11Z`, không phải hook `2026-09-30T06:29Z`.

## Đã kiểm

Đường dẫn dưới đây tính từ `cay-kho/`. Các neo tệp đều tồn tại trong Git tại exact reviewed SHA; đã đọc nội dung, không chỉ kiểm tên.

| Neo | Kết quả |
|---|---|
| `.claude/dev/launcher.py:4536`, `_do_github` | Có hàm và các chú thích 403 cũ như `CLAUDE.md:746` mô tả. Phân biệt chẩn đoán đường với khả năng làm việc. |
| `rest-kho`, `launcher.py:4606` | Đo GET đúng `/repos/{slug}` lấy từ origin; không đo mọi đường con, PR hay GraphQL. Giới hạn mới ở `CLAUDE.md:155`, `:742` khớp mã. |
| `_do_rest_github`, `launcher.py:4147` | Giá trị thành công là có header tên bắt đầu bằng `x-github` và status 2xx (`:4177–4180`); không xác minh token người gọi hay login. Khớp cảnh báo ở `CLAUDE.md:755`. Ví dụ 403 trong docstring có ngày 17-08. |
| `gh-kho`, `launcher.py:4634` | Gọi `gh api repos/{slug} --jq .full_name`; đây là một thao tác REST theo kho. Không chứng minh lệnh dùng GraphQL chạy được. |
| `gh-cli`, `rest-chung`, tập quyết định `DUNG_DUOC` | `launcher.py:4702` chỉ nhận `git`, `gh-kho`, `rest-kho`; hai mục chẩn đoán không quyết định. Khớp `CLAUDE.md:787–794`. |
| `t103`, `.claude/dev/launcher_test.py:3593` | Tồn tại dưới tên `t103_nam_finding_cua_bot_review_PR128`; phần thử GitHub phân biệt có CLI/xác thực với thao tác kho. Không coi việc test có mặt là bằng chứng đã chạy test trong lượt này. |
| `t110`, `.claude/dev/launcher_test.py:3351` | Tồn tại dưới tên `t110_rest_github_phan_loai_theo_HEADER_khong_theo_MA_TRANG_THAI`; dùng phản hồi giả kiểm header và trạng thái thứ ba. 403 ngày 17-08 là ví dụ lịch sử, đúng mô tả mới. |
| `CONG_CU`, `bat_buoc.remote: False`, `launcher.py:2621`, `:2645` | Mục `gh` có `mac_dinh: True`, `remote: False`, `ci: False`; chú thích dùng hai đường kho 403 để suy về `gh`, đúng chỗ văn bản mới chỉ ra còn lý do cũ. |
| Khối “KHONG cai `gh`”, `.claude/hooks/session-start.sh:230` | Tồn tại; còn câu cài cũng không dùng được dựa vào phép đo 15-08. `CLAUDE.md:747` trỏ đúng khối. Không chạy hook, vì hook có thao tác cài đặt và mạng. |
| Bảng “GitHub: bốn đường”, `docs/GOI_AGENT_DA_NEN.md:260` | Có bảng trạng thái 15-08, REST chặn và `gh` cài vô ích (`:266–267`); khớp neo mới. Danh sách trong `CLAUDE.md` có giới hạn “mẫu có thể sót”, không nhận là quét đủ toàn kho. |
| `doctor` không hỏi GraphQL | Đọc đường gọi trong `_do_github`; tìm `graphql` không phân biệt hoa/thường trong `launcher.py` cho 0 hit. Không chạy `doctor` vì nó có phép đo mạng, gồm POST MCP. |
| `ops/land/pr594-wp578-land-evidence.yaml:579`, `b94182b` | Biên nhận ghi REST GET `commits/8394f7411bfbeacdd1b6d5eafda21473f6487268`, HTTP 200. `git log -S` xác nhận dòng thêm ở `b94182b7e0e4ab9036e1376e46c99076ada63811`, `2026-09-21T17:47:06+00:00`. `execution_surface: claude_code` có ở dòng 19. Commit là tổ tiên base; khớp `CLAUDE.md:763–764`. |
| GraphQL 403 ngày 21-09 | `ops/land/pr594-wp578-land-evidence.yaml:523` ghi rõ POST `/graphql` và thông điệp bị chặn. Dòng thêm ở `a479699b7195ed12c5b30d5a70c95762e46a4490`, `2026-09-21T18:11:22+00:00`. |
| GraphQL 403 ngày 28-09 | `ops/land/pr666-wp650-provenance.yaml:8`, `:10–11` có thời gian và thông điệp. `git log -S` xác nhận `fcef7c38a8bb470f2fea8ca9a4199eb8d63049a5`, `2026-09-28T16:30:42+00:00`. |
| GraphQL 403 ngày 29-09 | `ops/land/pr680-wp676-land-evidence.yaml:146` ghi truy vấn WorkflowRun, HTTP 403 và giờ `09:14Z`. Dòng thêm ở `c928ba9d48c0930c164a0da215847785a67cf00e`, `2026-09-29T09:17:12+00:00`. Cả ba commit GraphQL là tổ tiên base, khớp `CLAUDE.md:734`. |

Bảy tệp của glob `ops/leases/lease-dang-windows-*-20260822.yaml` đều khai packet issue `238` và có `posted_comment_id`:

| Tệp trong `ops/leases/` | Dòng | ID |
|---|---:|---:|
| `lease-dang-windows-exec-1-codex-20260822.yaml` | 118 | 5378293440 |
| `lease-dang-windows-exec-2-codex-20260822.yaml` | 133 | 5378345150 |
| `lease-dang-windows-review-1-claude-20260822.yaml` | 94 | 5378963941 |
| `lease-dang-windows-exec-3-codex-20260822.yaml` | 145 | 5379124290 |
| `lease-dang-windows-review-2-claude-20260822.yaml` | 131 | 5379504423 |
| `lease-dang-windows-exec-4-codex-20260822.yaml` | 146 | 5379627095 |
| `lease-dang-windows-review-3-claude-20260822.yaml` | 112 | 5379775615 |

Các phần đối chiếu nội dung và biên nhận:

- **7/7 comment và số ký tự:** `pr631-review-1b-claude-cli/VERDICT.md:35–45`, lượt 2 dòng 166, lượt 3 dòng 46 và lượt 4 dòng 51–54 cùng kể đủ bảy ID, `created_at == updated_at`, dãy dấu nháy `22/33/14/49/34/33/19`, 0 thực thể và 0 dấu `&`. Dãy theo thứ tự ID/thời điểm tạo, không theo tên tệp. `CLAUDE.md:163–167` chép khớp và giữ giới hạn không có đầu ra MCP cũ, không biết comment cụ thể đã đọc, hai REST client chung proxy. Đây là kiểm tính nhất quán của biên nhận, không phải tôi đã tải lại comment.
- **Comment 5811128755:** lượt 1b dòng 194, lượt 2 dòng 165, lượt 4 dòng 168 cùng ghi 44 dấu nháy đơn, 8 dấu `>`, 3 dấu `<`, 0 thực thể. Khớp `CLAUDE.md:156–159`; lời khai đọc MCP chỉ nhận phạm vi comment ấy và ghi thiếu tên công cụ.
- **200/403 và danh tính:** lượt 2 dòng 64–77, lượt 3 dòng 138–150, lượt 4 dòng 153–168 đỡ các trạng thái được kể: gốc `/` trả `{}` 2 byte không header GitHub; kho/PR/comment có header; `collaborators` bị proxy chặn; `protection` trả lỗi integration từ GitHub; token giả/không/thật cho cùng login và expiration `2026-09-30 08:22:21 UTC`. Không ghép kết quả 30-09 sang 25-09; vế 25-09 ghi PR 623 và chỉ `hdr_github=True`. Độ chính xác về giờ/lần chạy executor còn F1.
- **Danh sách 14 đường:** đếm được comment + 10 đường con 200 + 3 đường 403. Những đường này có kết quả đo lại trong lượt 3/4. Phép đếm danh sách không xác minh được executor đã đo 14/10 đường vào `07:51–07:57Z`.
- **18 hiện vật review:** đúng 2 tệp lượt 1 và 4 tệp mỗi lượt 1b/2/3/4. Cả 12 băm PROMPT/VERDICT/HINT trong bốn `RUN.md` đều khớp byte hiện vật; HINT lượt 4 rỗng. Các verdict neo những SHA lịch sử riêng, không được dùng như review của exact SHA hiện tại. Lời nhắc P1 bị bác trong `CLAUDE.md:160` khớp F1 của lượt 1b. Không tự suy các log `scratch/` được kể trong verdict đã được lưu trong checkout.
- **Mâu thuẫn trong `CLAUDE.md`:** đã đọc các vùng readback/MCP, “hỏi chỗ tiện tay”, “có MẶT khác có ĐO”, “Đẩy ref”, và “GitHub: bốn đường”; quét mọi hit REST/403/GraphQL/`gh` trong toàn tệp. Các trạng thái cũ 15/16/17-08 và câu “mọi thao tác kho” đã có nhãn phạm vi. REST DELETE và khả năng ghi không được nhận là đã đo. Ngoài F1, không thấy mâu thuẫn mới cần finding.
- **Byte nhạy với Unicode:** ba dòng chứa chuỗi thoát ASCII cho U+0308 giữ nguyên từng byte so base; cả base/head có 0 U+0308 thật và 2 U+00F6.
- **Chuỗi nhạy cảm:** quét toàn bộ 1.486 dòng thêm, kể cả các HINT/PROMPT, bằng mẫu của `scripts/pkg_secret_scan.py`, `scripts/hooks/secret_guard.py` và mẫu PAT GitHub: 0 hit bí mật; 0 chuỗi bỏ-qua-CI nguyên văn; 0 cú pháp mở biểu thức Actions. Quét toàn bộ 19 tệp cũng không thấy mẫu bí mật. Năm chuỗi bỏ-qua-CI và một ví dụ biểu thức Actions ở phần cũ của `CLAUDE.md` đã có nguyên byte ở base; không phải nội dung thêm của PR, và PR không đổi workflow. Không chép lại các chuỗi đó vào verdict.

## Cổng

Chạy trực tiếp trong checkout `cay-kho`, với `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`. Python đều dùng `-B`; cache và thư mục tạm của `tl.py` được trỏ ra `/tmp`. Không dùng kết quả của các lượt review cũ thay cho các lần chạy dưới đây.

| Lệnh | rc | Marker dương / kết quả |
|---|---:|---|
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 59 ADR trên đĩa, 59 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `python3 -B scripts/tl.py doc-claims-check --json` | 0 | `ok: true`, `schema: doc_claims_check.v1`, `files_scanned: 120`, `flags: []`, `advisory_count: 381`, `layers_skipped: {}`, có `CLAUDE.md` trong `roots`; stderr rỗng. |

`claims_flagged: 381` của JSON là các advisory ở đây, không phải 381 lỗi chặn: `flags` rỗng và mọi giá trị `by_layer` đều 0. Lệnh được yêu cầu không có `--strict` (`strict: false`). Không có cổng đỏ nên không cần chạy đối chiếu baseline. Số 50 ADR trong review lượt 4 thuộc SHA lịch sử `e2fa6d7`; đã đếm chính cây commit ấy được 50, không mâu thuẫn với 59 ADR của reviewed SHA hiện tại.

## KHÔNG ĐO ĐƯỢC

- Không gọi mạng trong lượt này. Toàn bộ mã HTTP, header, login, expiration, nội dung comment/PR, `updated_at` và băm thân phản hồi từ xa chỉ được đối chiếu giữa văn bản với biên nhận lưu trong kho; không được xác nhận lại độc lập với GitHub.
- Không có log gốc của các lần chạy executor và hook nêu ở F1. Các lần reviewer đo lại không tái lập thời điểm hay độ phủ client của lần chạy khác. Phần này cần được thể hiện ngay trong lời khai ở `CLAUDE.md`.
- Không kiểm trực tiếp thân PR #631/bảng đo 25-09, lần đọc MCP 25-09, đầu ra MCP 22-08, hoặc lần đọc lại bảy comment qua MCP. Không xác lập rằng hai client REST chung proxy là hai đường truyền độc lập tới origin.
- Không đo REST DELETE/phương thức ghi, xoá ref hay đẩy tag; không chạy `gh` hoặc `doctor` để thử mạng. Khả năng lệnh `gh` dùng GraphQL vẫn là giới hạn được văn bản khai ra.
- Không xác định tầng thay Authorization, nguyên nhân chuyển 403→200, thời điểm chuyển, hoặc việc header từng bị thay ở phiên 15/17-08 hay 25-09. Không suy số đo của một phiên thành trạng thái chung.
- Không xác nhận trạng thái GitHub hiện tại, CI hậu merge, hay điều kiện khác của hồ sơ land. Verdict này không tự cấp quyền đổi `landed`.

Tôi không ghi, tạo hay xoá bất kỳ tệp nào trong `./cay-kho`; mọi tệp phục vụ lượt review nằm ở `/tmp`, và đầu ra giao nộp duy nhất là `./out/VERDICT.md`. Snapshot đầu/cuối có **13.524 mục mỗi bên, 0 mục đổi nội dung/mode/đích symlink** (gồm `.git/index`, tệp ignored/untracked); HEAD/tree giữ nguyên và status đều rỗng, phép đối chiếu **PASS**. Snapshot sạch chỉ chứng minh không có delta quan sát được giữa hai mốc, không tự chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Sandbox thực tế là `workspace-write`; ràng buộc read-only của checkout được tuân thủ bằng cách chọn lệnh và đặt mọi đầu ra ra ngoài cây.
