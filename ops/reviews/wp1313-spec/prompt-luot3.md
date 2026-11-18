Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 3, cho đặc tả `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r3.md` (Issue #1313). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử thì chạy trong RAM hoặc bản sao trong /tmp.

Thư mục làm việc: worktree kho tra-luat trên master 3d6bfa5, có r2 (bạn đã approve ở lượt 2; chủ kho duyệt băm) và r3. Executor của r2 dừng ở preflight theo §6 vì tìm thấy chỗ thứ ba cùng suy diễn: `.claude/dev/mcp_github_doc.py` `Phien._post` (nhánh HTTPError mô tả mọi lỗi không header là "proxy tu sinh", kể cả 5xx). r3 thêm chỗ đó (M8, M9, N6), mở write set lên 4 tệp, sửa §6; mục 9 liệt kê thay đổi. Phần còn lại giữ nguyên r2.

Việc:
1. So r2 ↔ r3 (`diff`): xác nhận chỉ đổi những gì mục 9 nói.
2. Kiểm §0 mới với mã `.claude/dev/mcp_github_doc.py` và `.claude/dev/mcp_github_doc_test.py` (dòng, hành vi, runner `--dot-bien`, phân hạng `TinHieuChotCa`, mẫu đếm CI trong `.claude/dev/ci_dang_ky_test.py`).
3. Theo L1–L7 của `.claude/skills/soan-spec/SKILL.md`: M8/M9/N6 có phép đỏ đỏ được không; đột biến mới có khớp đúng một chỗ không và không phá mẫu `DOT_BIEN` cũ của `mcp_github_doc_test.py`; `t06` có còn đúng không.
4. Quét lại toàn kho (ngoài `*.md`, `ops/**`) còn chỗ thứ tư cùng suy diễn "thất bại ⇒ chặn/proxy" mà r3 bỏ sót không (gợi ý: `rg -n 'x-github'`, `rg -n 'proxy tu sinh'`).
5. Kích thước so trần ADR-0053 (≤ 450 dòng thêm, ≤ 6 tệp).

Đầu ra stdout: bảng kiểm, finding P0–P3 (chỗ, vấn đề, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
