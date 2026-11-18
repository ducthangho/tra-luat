Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp (git archive), kể cả chạy `--lap-ca` ca hiện có và dựng thử bản vá trên bản sao.

Worktree kho tra-luat trên master 641108c, cộng `ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md` (Issue #387 m1): `.claude/dev/launcher.py` `lenh_run` băm stdout/stderr ngay sau p.wait() mà không kiểm cây tiến trình đã chết; packet thêm `log_bam_luc_utc`, `log_bam_cay_da_chet`, chờ có hạn ≤10s, VERSION 1.6.1, sửa neo đột biến t117/t76.

Đọc: đặc tả; `.claude/skills/soan-spec/SKILL.md` (L1–L7); `.claude/dev/launcher.py` (lenh_run, _cay_da_chet, _thanh_vien_nhom, job object Windows, chỗ băm log, chỗ xoá bản chụp prompt); `.claude/dev/launcher_test.py` (r12, r14, t76, t117, DOT_BIEN, runner); `docs/adr/0053`, `0055`, `0067`.

Việc: (1) kiểm lời khai §0 (dòng, tái hiện cháu ghi muộn trên bản sao); (2) theo L1–L7 mỗi N có phép đỏ thật, mỗi đột biến khớp đúng một chỗ và giết đúng ca đích; (3) ba quyết định tự đặt của người soạn (không đo được thì thoát chờ ngay; `ket_thuc_utc`/`thoi_luong_giay` tính cả thời gian chờ; Windows giữ không xoá prompt ngay) có hợp lý không, có đổi hợp đồng run.json mà người đọc khác phụ thuộc không (tìm mọi chỗ đọc `ket_thuc_utc`, `thoi_luong_giay`, `stdout_sha256` trong kho); (4) Windows: ca có chạy được thật không (cháu trong job object), không được BỎ QUA lặng lẽ; (5) thời gian chạy các ca mới.

Đầu ra stdout: bảng kiểm sự thật, finding P0–P3 (chỗ, vấn đề, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
