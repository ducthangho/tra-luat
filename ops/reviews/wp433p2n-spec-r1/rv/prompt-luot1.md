Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Thư mục làm việc: clone kho tra-luat, HEAD tách ở master 8a72d28d7a413047733277545fc8547f32010593 (tree df0bbe85…, đã chứa P2a, P2b, C1, R của #433 trong `scripts/tl_gws.py`). Clone có đủ lịch sử và mọi nhánh `refs/remotes/origin/*` — dùng `git` để đo lại mọi con số (blob, dòng, OID ADR). Cộng (chưa commit):
- `ops/specs/GWS-CRED-DICH-NGOAI-KHO-N-r1.md` — ĐẶC TẢ CẦN REVIEW (packet N: đóng bốn nợ có tên của #433 — test packet 1 so chuỗi đường trên Windows; W6 thiếu chốt thư mục tổ tiên; bundle không phải dict; `_trong_kho_git` nuốt OSError).
- `ops/reviews/wp433p2n-spec-r1/` — bằng chứng §0: `tai_hien.py` + `tai-hien-linux.txt` (tái hiện Linux cho nợ 2–4), `probe433n.py`/`do433n.py` + `probe-linux.txt` + `desktop-wp433n-out-20261120T012952Z/` (probe Windows thật cho nợ 1, đầu ra thô).
- Khuôn đã land: đặc tả R `GWS-CRED-DICH-NGOAI-KHO-R-r1b.md` và C1 `GWS-CRED-DICH-NGOAI-KHO-C1-r1.md` nằm trên nhánh `origin/ops/wp433-p2r-spec` và `origin/ops/wp433-p2c-spec` (`git show <nhánh>:ops/specs/…`); fragment R `scripts/test_fragments/wp433_gws_cred_win_reparse.py`, C1 `wp433_gws_cred_win_duong.py`, P2a `wp433_gws_cred_dich_ngoai_kho.py`, packet 1 `wp433_nlm_gws_dich_ngoai_kho.py` có trong cây.

Quyết định ĐÃ CHỐT của chủ kho (không review lại lựa chọn, chỉ review việc đặc tả hiện thực đúng lựa chọn): Q1 sửa test, không sửa mã dựng đường; Q2 = A, W6 chốt từ gốc như W4/W5 (chấp nhận từ chối HOME có tổ tiên symlink); Q3 bundle không phải dict ⇒ rc 3; Q5 áp cùng chốt cho jar NLM W1–W3. Không có Windows ở đây: hành vi native là lời khai cần ĐO (§4c); kiểm phép đo được mô tả có đủ làm đỏ/xanh lời khai không. Phản chứng chạy được đã có trong cây — hãy CHẠY chúng (vd `python -B ops/reviews/wp433p2n-spec-r1/tai_hien.py`, probe packet 1 trên Linux) và có thể áp thử M1–M4 vào BẢN SAO trong RAM/`/tmp`. Đừng tự soạn đường dẫn dựng để thoát khỏi cây thư mục hay nội dung credential giả lập kiểu tấn công — hướng thử nào cần loại nội dung ấy thì MÔ TẢ BẰNG LỜI, phiên điều phối sẽ dựng.

Đọc: đặc tả N; `.claude/skills/soan-spec/SKILL.md` (L1–L7); `scripts/tl_gws.py` (`_trong_kho_git` ~1120–1140, `_kiem_dich_ghi`, `_dich_cred_gws` ~1220, `_dich_cred_gws_nt` ~1305, `_dich_jar_nlm`, `cmd_nlm_auth_pull` ~1830, `cmd_bootstrap` ~1880–1960, `_bootstrap_agent_creds` ~1446); fragment packet 1 dòng 230–250; `docs/adr/0053*`, `0055*`, `0067*`; `docs/PROTOCOL_DA_PHIEN.md` §10.1.

Việc:
1. Kiểm lời khai §0 (dòng, neo, blob/sha, người gọi, hành vi tái hiện) bằng đọc/chạy.
2. M1–M4: đúng phạm vi? M2 đổi chữ ký `_dich_cred_gws(_nt)` có phá neo `_DB`/`_TU_KIEM` nào của fragment P2a/packet 1/C1/R không (đếm thật)? W6 đi qua `_dich_cred_gws` trên POSIX quét từ `/` — có hồi quy cho ca HOME thường (vd HOME dưới /tmp, HOME trong kho) không? `_dich_jar_nlm` khi chuyển sang chốt từ gốc giữ đúng tiền tố/thông báo cụm không? M3 đặt đúng chỗ (trước mọi gán env/ghi)? M4 có đổi hành vi cho người gọi nào chưa bọc OSError không (kiểm hết người gọi `_trong_kho_git`)?
3. N1–N7, §4b: mỗi tiêu chí có phép làm đỏ; năm đột biến có đích phân biệt, đúng nhãn, neo khớp 1 lần trên NGUỒN CANDIDATE mô tả được; đột biến nào có thể bị giết vì lý do vô can (tín dụng giả); bọc `os.lstat` ở N4 có làm mù phép đo không; N1 phép so `startswith` chuẩn hoá có đúng cả POSIX lẫn nt.
4. §4c: D2/D3/D4/D5 đủ phân biệt, có vế âm, nhánh KHÔNG ĐO ĐƯỢC rõ; điều kiện dừng §6 đo được.
5. Kích thước §8 (~195–250) hợp lý so với fragment R thật (đếm dòng).

Một finding chỉ nên nêu khi nó làm sai một tiêu chí/đột biến/phép đo cụ thể; đừng nêu đề xuất làm chặt thêm mà đặc tả đã khai là giới hạn ở §2/§8.

Đầu ra stdout: bảng kiểm sự thật, finding P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
