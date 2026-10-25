verdict: changes_requested
reviewed_sha: af5edd354d414999eb8355f8dc4d799958f08aca
P1: 0   P2: 2   P3: 2
reviewer_provider: anthropic_claude
model_tu_khai: claude-opus-5-5
effort_tu_khai: KHONG_DO_DUOC
execution_surface_tu_khai: subagent trong phiên Claude Code (không phải claude CLI riêng)
cross_provider: false

## Findings
- P2 `bo-sot-cung-lop` tại CLAUDE.md:551 (§Đẩy ref, 16-08). Câu "`curl https://api.github.com` cũng 403" chưa được đánh dấu đã trôi. Đo 2026-09-29: `curl -o /dev/null -w '%{http_code}' https://api.github.com` ra 200. Đề xuất: ghi "(đo 16-08; đã trôi, đo lại 29-09: 200 kèm X-GitHub-*)".
- P2 `tham-chieu-hep-bo-sot-menh-lenh-15-08` tại :620-624, :637, :671. Câu mới viết "HAI DÒNG 403 Ở TRÊN", tức chỉ hai dòng 17-08. Đoạn 15-08 vẫn khai "REST bị PROXY chặn 403 bất kể token", "`gh` cài cũng vô ích", "không bằng REST thẳng", và không có đánh dấu nào. Dòng :671 "mọi thao tác kho trả 403" cũng vậy. Người đọc sẽ vẫn tin rằng cài `gh` là vô ích. Đề xuất: đổi thành "MỌI DÒNG 403 Ở TRÊN, của 15-08 lẫn 17-08"; ghi rằng các hệ quả về `gh` đã mất chân đỡ nhưng `gh` chưa được đo lại, nên là KHÔNG ĐO ĐƯỢC; thêm "(trạng thái 17-08, nay đã trôi)" vào :671.
- P3 `khai-rong-hon-phep-do` tại :639-640. Câu "Nền đã đổi, KHÔNG phải lượt cũ đo sai" không có phép đo nào đỡ, vì lượt cũ không đo lại được. Đề xuất: viết là giải thích mạnh nhất, không phải điều đã chứng minh.
- P3 `khong-do-duoc-mot-phan-do-duoc` tại :642-643. Hai điều đo được: `/user` gọi không token trả `login` = chủ kho, và hiện tượng này đã có từ 17-08 (khi đó `/user` không token đã trả 200). Nên không phải "KHÔNG ĐO ĐƯỢC mới".

## Phép đo lại (2026-09-29T23:11Z)
Có token và không token cho kết quả y hệt: `/rate_limit`, `/user`, `/repos/ducthangho/tra-luat`, `/repos/.../pulls/631` đều trả `HTTP/1.1 200 OK`, mỗi phản hồi có 4 header `x-github-*`. Kho có `private=True`. `/user` không token trả `login=ducthangho`. `doctor` in `rest-kho=OK · rest-chung=OK`.
issuecomment-5811128755 (issue #523, bản chiếu lease `quy-trinh-lap-review-r15-g16-claude`) đọc qua REST: `'`=44, `"`=2, `>`=8, `<`=3; không có thực thể HTML nào (`&#39;`, `&#34;`, `&gt;`, `&lt;`, `&amp;`, `&quot;` đều bằng 0). Khớp lời khai.

## Cổng
doctrine-scan rc=0 (10 tệp) · adr-song rc=0 (50/50) · doc-claims-check --strict --json rc=0 ok=true (110 tệp, 381 advisory). Sau khi chạy, `git status` vẫn sạch.

## KHÔNG ĐO ĐƯỢC
- Lời khai "đọc qua MCP cũng ra ký tự thật": chưa đo lại qua MCP.
- `ai-dang-giu CLAUDE.md`: bộ đệm cục bộ có 14 ref, `ls-remote` có 521. Muốn đo thì phải fetch, mà cây là READ-ONLY, nên chưa đo.
- launcher.py :1919-1920 và :3366-3373 còn bảng "REST CHẶN 403". Bảng có ghi ngày 15-08/17-08 và nằm ngoài write set của PR, nên không tính là finding; chỉ ghi lại để có packet theo sau.
