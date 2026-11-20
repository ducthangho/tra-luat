Bạn là reviewer ĐỘC LẬP (họ OpenAI) cho một ĐẶC TẢ packet, chưa có mã. CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; KHÔNG gọi mạng; KHÔNG đọc hay dùng secrets/credential thật (`*.enc`, `tl_secrets*`, `*token*`, `credentials*`, `~/.tra_luat_config.json`, `~/.codex`, `~/.config/gws`, `~/.notebooklm-mcp-cli`). Chạy thử trong RAM hoặc bản sao dưới /tmp hay /dev/shm, với HOME tạm.

Thư mục làm việc: clone kho tra-luat, HEAD tách ở master 0f9aa2a2cc697129e1f5be72feddf60986286865 (tree da48b7d3…, đã chứa packet N và P2BW của #433). Clone có đủ lịch sử và mọi nhánh `refs/remotes/origin/*` — dùng `git` để đo lại mọi con số (blob, dòng, OID ADR). Cộng (chưa commit):
- `ops/specs/SECRETS-SET-BUNDLE-KIEU-r1.md` — ĐẶC TẢ CẦN REVIEW (packet SECRETS-SET-BUNDLE-KIEU: `secrets-set` giải mã bundle từ Drive mà chưa kiểm kiểu; token không phải str bị `str()` thành khoá public).
- `ops/reviews/wp433-secrets-set-spec-r1/` — bằng chứng §0: `tai_hien.py` (runner: nạp `scripts/tl_gws.py` vào module mới trong RAM, MỌI hàm tải/ghi/mạng thay bằng đồ giả có đếm), `tai-hien-linux.txt` (base), `nguyen-mau.diff` (M1+M2), `nguyen-mau-linux.txt`.
- Khuôn đã land: đặc tả N `ops/specs/GWS-CRED-DICH-NGOAI-KHO-N-r2.md` trên `origin/ops/wp433-p2n-spec` (`git show origin/ops/wp433-p2n-spec:ops/specs/…`); fragment N `scripts/test_fragments/wp433_gws_cred_no.py` (khuôn TinHieuChotCa/_DB/_LUOT_DU_KIEN/phân hạng) có trong cây.

Quyết định ĐÃ CHỐT của chủ kho (không review lại lựa chọn, chỉ review việc đặc tả hiện thực đúng lựa chọn): Q1 bundle không phải object ⇒ rc 3, kiểm ngay sau giải mã, trước mọi cờ; Q2 = A, token không phải str ⇒ coi như thiếu (bỏ đồng bộ public kèm cảnh báo sẵn có, rc giữ nguyên); Q3 đo một lượt D1 nhẹ trên Windows Desktop. Không có Windows ở đây: hành vi native là lời khai cần ĐO (§4c); kiểm phép đo mô tả có đủ làm đỏ/xanh không.

Phản chứng chạy được đã có trong cây — hãy CHẠY chúng: `python -B ops/reviews/wp433-secrets-set-spec-r1/tai_hien.py .` và `python -B ops/reviews/wp433-secrets-set-spec-r1/tai_hien.py . ops/reviews/wp433-secrets-set-spec-r1/nguyen-mau.diff` (runner tự dùng HOME/TL_* tạm, khoá master giả; nếu cần đặt `TMPDIR` vào /dev/shm). Có thể áp thử M1–M2 và các đột biến §4b vào BẢN SAO trong RAM. Đừng tự soạn nội dung credential giả lập kiểu tấn công hay đường dẫn thoát khỏi cây thư mục — hướng thử nào cần loại nội dung ấy thì MÔ TẢ BẰNG LỜI, phiên điều phối sẽ dựng.

Đọc: đặc tả; `.claude/skills/soan-spec/SKILL.md` (L1–L7); `scripts/tl_gws.py` (`_nlm_contained` ~913, `cmd_secrets_set` ~992, `_secrets_set_body` ~999–1085, `_nlm_bundle_guard`, các kiểm 1870/1922 của packet N); `docs/adr/0053*`, `0055*`, `0067*`; `docs/PROTOCOL_DA_PHIEN.md` §10.1.

Việc:
1. Kiểm lời khai §0 (dòng, neo, blob/sha, thứ tự luồng, hành vi tái hiện, bộ đếm) bằng đọc/chạy.
2. M1–M2: đúng phạm vi và đúng Q1/Q2? M1 có thật đứng trước MỌI tác dụng phụ (export gws, refresh, canary, encrypt, upload) không? Có người gọi nào khác của `_secrets_set_body`/biến `bundle` bị đổi hành vi? M2 có đổi hành vi khi `TL_TOKEN` đặt, khi `--gas-token` đặt, khi token là str rỗng?
3. N1–N5, §4b: mỗi tiêu chí có phép làm đỏ; bốn đột biến có đích phân biệt, đúng nhãn, neo khớp đúng 1 lần trên NGUỒN CANDIDATE mô tả được; đột biến nào có thể bị giết vì lý do vô can (tín dụng giả); bảng hồi quy N3 khớp số đo; các lượt `kieu.*.khong_co` (base rc 1) được đặc tả xử lý đúng.
4. §4c D1: đủ phân biệt, có vế âm, nhánh KHÔNG ĐO ĐƯỢC rõ; điều kiện dừng §6 đo được.
5. Kích thước §8 (~180–250) hợp lý so với fragment N/P2BW thật (đếm dòng).

Một finding chỉ nên nêu khi nó làm sai một tiêu chí/đột biến/phép đo cụ thể; đừng nêu đề xuất làm chặt thêm mà đặc tả đã khai là giới hạn ở §2/§8.

Đầu ra stdout: bảng kiểm sự thật, finding P0–P3 (chỗ, vấn đề, bằng chứng, câu thay thế). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.


LƯỢT 2. Đây là bản sửa sau lượt 1 (sha256 đặc tả 036af79c…). Lượt 1 của bạn (`request_changes`) có 3 P2 và 2 P3; kết luận đầy đủ ở `ops/reviews/wp433-secrets-set-spec-r1/rv/luot1.stdout.txt`. Tóm tắt: (P2) N1 `dong` chỉ đếm dòng có ✗ và §4b không có phép đỏ cho bộ đếm tác dụng phụ; (P2) đột biến 1–2 có thể bị giết bởi lỗi vô can mà `_nlm_contained` đổi thành rc 5; (P2) N5 đòi D2 trước land trong khi D2 sau land, §6 thiếu KHÔNG ĐO ĐƯỢC; (P3) §0(3) thiếu bộ đếm; (P3) §0 bỏ sót `--secrets-file`, §6 gán nhầm trần ADR-0053. Xem §10 của đặc tả. Việc lượt này: kiểm từng finding đã ĐÓNG thật chưa (đo, không đọc lời), rồi review lại toàn bộ như lượt 1; chỉ nêu finding mới khi nó làm sai một tiêu chí/đột biến/phép đo cụ thể.
