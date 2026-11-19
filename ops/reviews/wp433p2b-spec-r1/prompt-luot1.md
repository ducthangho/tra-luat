Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp (nếu /tmp chỉ đọc, mô phỏng trong RAM và ghi rõ là mô phỏng).

Thư mục làm việc: clone kho tra-luat ở master 11bd0336d00b4a9544e70dcbbe049d372053a3ec (đã chứa packet 1 `NLM-GWS-DICH-NGOAI-KHO` và P2a `GWS-CRED-DICH-NGOAI-KHO-A`: `scripts/tl_gws.py`, fragment `scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py`, `scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py`), cộng (chưa commit):
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-B-r1.md` — ĐẶC TẢ CẦN REVIEW (packet P2b, Issue #433: kiểm DỮ LIỆU của W6 trong `cmd_bootstrap` — `token`/`webappUrl` trước khi gán env, config cũ không phải dict, tuần tự hoá config; cộng ca hồi quy `jar_rong_base`).
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md` (P2a đã land, khuôn) và `ops/specs/GWS-CRED-DICH-NGOAI-KHO-r1-truoc-tach.md` (bản trước khi tách; M7, N9w6, N3d, §4b dòng 24–29 là nguồn của P2b).
- `ops/reviews/wp433p2b-spec-r1/do/` — script đo của phiên soạn và output: `do_w6.py` (hành vi base, §0.2), `va_ung_vien.py` (dựng NGUỒN ỨNG VIÊN prototype của M1–M3 từ `scripts/tl_gws.py`: `python3 -I va_ung_vien.py <vào> <ra>`), `do_dot_bien.py` (bộ chạy tạm bảng đột biến §4b: `python3 -I do_dot_bien.py <thư mục scripts> <tl_gws ứng viên>`), `chay_frag.py` (chạy fragment trên một cây), các tệp `.txt` là output đã ghi.

Quyết định chủ kho là RÀNG BUỘC, không tranh luận: phạm vi P2b = kiểm dữ liệu W6 + `jar_rong_base` (tách từ P2a); Windows/UNC thuộc P2c; §9 Q1 (ngoại lệ bundled) chặn lease không chặn review — đừng nêu Q1 là finding. Q2, Q3 là câu hỏi mở cho chủ kho; chỉ nêu finding nếu đặc tả tự mâu thuẫn với chúng.

Đọc: đặc tả; `.claude/skills/soan-spec/SKILL.md` (L1–L7); `scripts/tl_gws.py` (`cmd_bootstrap` ~1740–1870, `cmd_nlm_auth_pull` ~1690, `_nlm_auth_load` ~2015, `_kiem_dich_ghi` ~1173, `_ghi_nguyen_tu_0600` ~1158); hai fragment wp433 hiện có; `ops/cloud_agent_creds_test.py` (bảng PD 796–806); `docs/adr/0053*`, `docs/adr/0055*`.

Việc:
1. Kiểm từng lời khai sự thật §0 (dòng, thứ tự thao tác W6, bảng B0–B20, bẫy neo §0.3) bằng đọc và CHẠY: dựng nguồn ứng viên bằng `va_ung_vien.py` vào /tmp (hoặc trong RAM), chạy `do_w6.py`, `do_dot_bien.py`, và hai fragment kề bên qua `chay_frag.py` trên cây có nguồn ứng viên. Ghi lệch.
2. M1–M3: mô tả có đủ chặt để hai executor độc lập viết ra cùng hành vi không; có đường dữ liệu nào vào env hoặc config mà vẫn ném ngoại lệ thoát `cmd_bootstrap`, hoặc ghi config sai, mà đặc tả không phủ (giá trị kiểu lạ, khoá lạ, config cũ lạ, thứ tự kiểm/gán, `--require-agent-creds`, `env` code/cowork thay vì chat). Nêu bằng phép đo chạy được, đừng tự soạn đường dẫn hệ tệp bất thường — mô tả bằng lời nếu cần.
3. Theo L1–L7: mỗi N có phép đo làm nó đỏ; mỗi đột biến §4b có đích (ca, lượt, nhãn) phân biệt; cột E/H, tập khai theo lượt, cột nền nhất quán; tổng đếm (21, E 7, H 14, posix 2) đúng; N3 đẳng thức tổng kết và tự kiểm (`tu_kiem_doi_kieu`, `tu_kiem_sai_luot`) còn có răng; ba phản chứng bộ đo đỏ được.
4. Các lượt không là đích đột biến (đoạn sau bảng §4b): lời khai "đo hành vi, không là phép đỏ" có làm ca thành "có MẶT mà không ĐO" không.
5. Ước lượng kích thước §8 (251–336 dòng thêm, trần 450) so với fragment P2a (389 dòng) và numstat của P2a (`git diff --numstat 417b593^1 417b593`).

Đầu ra stdout: bảng kiểm sự thật, finding P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
