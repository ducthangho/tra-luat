Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp nào trong thư mục làm việc; không gọi mạng. Muốn chạy thử thì chạy python trong RAM hoặc trên bản sao trong /tmp ngoài thư mục làm việc.

Thư mục làm việc: worktree kho tra-luat trên master 13bf69f, cộng tệp `ops/specs/LAUNCHER-5XX-KHONG-PHAI-CHAN-r1.md` (đặc tả cần review, Issue #1313).

Đọc: đặc tả; `.claude/skills/soan-spec/SKILL.md` (L1–L7, mục 4); `.claude/dev/launcher.py`: `_do_rest_github` (4726), `_do_mcp_endpoint` (4994), `_do_github` (người gọi, khoảng 5130–5260), `_nhan_duong`; `.claude/dev/launcher_test.py`: `t110_rest_github_phan_loai_theo_HEADER_khong_theo_MA_TRANG_THAI`, `t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec`, `t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho`, bảng `DOT_BIEN` và runner đột biến, `bang`/`TinHieuChotCa`, `_tai_launcher_thu`; `docs/adr/0053-*.md`, `0055`, `0067`.

Việc:
1. Kiểm lời khai sự thật §0 với mã (số dòng, hành vi hai nhánh HTTPError, người gọi, ca hiện có không phủ 5xx).
2. Theo L1–L7: mỗi mục tiêu chiếu write set; mỗi tiêu chí có phép đo làm nó ĐỎ thật sự đỏ được (đặc biệt M5 và đối chứng biên N1; N2 với runner thật; N3 có đo được không); mọi câu hỏi/báo/chờ chủ kho mang mã E; không ngân sách mềm.
3. Tìm ĐƯỜNG THỨ BA: còn chỗ nào khác trong `.claude/dev/launcher.py` (hay nơi gọi) phân loại HTTP theo header `X-GitHub-*` hoặc gán `chan` cho phản hồi không header mà đặc tả bỏ sót không? Đặc tả có làm `t117` gãy (mẫu đột biến cũ khớp thêm chỗ, hay mẫu mới khớp hai chỗ) không?
4. Quy tắc `e.code >= 500` có hợp lý không với các mã proxy có thể sinh (407, 429, 502, 503, 504) — có ca nào đáng ghi mà đặc tả xử lý sai?
5. Kích thước ước lượng so trần ADR-0053 (≤ 450 dòng thêm, ≤ 6 tệp).

Đầu ra stdout: (1) bảng kiểm sự thật; (2) finding P0–P3 (chỗ, vấn đề, câu thay thế); (3) ước lượng kích thước. Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
