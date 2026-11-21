# Review ĐẶC TẢ wp1236 r10 — vòng 5 — reviewer độc lập, theo PROTOCOL §8.3

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã), review class `sensitive`. Kho: ducthangho/tra-luat.

## Bối cảnh
r10 thay r9 (`e3efa593…`). Vòng 4 (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/lich_su/VERDICT_vong4_codex.json`, đúng §8.3) cho `changes_requested` với U01 P3 (`hop-dong-dau-vao-dau-ra-chua-chot`), U02 P3 (`nghiem-thu-khong-co-lap-chot-dich`), U03 P2 (`pham-vi-kiem-chung-trai-adr-windows`), và dựng 12 lớp lịch sử vòng 1–3. Ngoài ra review MÃ r9 đợt A lượt 6 (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/lich_su/VERDICT_ma_luot6_codex.json`) chạm Review Rescue Checkpoint §12 cho lớp `test-thieu-chot` (hai chuyển tiếp 0/1); soạn giả chuyển cách làm mới vào r10 (mục *Ma trận chốt–ca–đột biến*, luật 3–5). Quyết định chủ kho về Windows: #1236 issuecomment-7048063512 (đợt A: Windows local, miễn Windows CI). Nâng trần A lên 1400: issuecomment-7047718543. VERDICT vòng 1–3 (không theo §8.3) ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/lich_su/` chỉ để tra nguồn.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/work/`.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI; dựng biến thể bằng cách SỬA BẢN SAO fixture thật là được.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/SPEC.md`, sha256 `9816599335afce624a058b445f0d9d85b1683fcc32aa232b874fa43b506c63ff` (= `git show 4b5e3c6:ops/specs/wp1236-r10.md`). Kiểm sha256 trước; lệch thì dừng. `git diff --no-index <(git show 4b5e3c6:ops/specs/wp1236-r9.md) /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/SPEC.md` (hoặc tương đương) là phần mới.
- Kho `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/repo`, HEAD `4b5e3c6`, lịch sử đầy đủ. Hiện vật review mã r9: `git show refs/remotes/origin/ops/wp1236-r9-a-lease:ops/reviews/wp1236-a-r9-ma-6-codex/…` (và `ma-1..5`). Mã r9 đợt A tham chiếu (commit cục bộ của executor, KHÔNG ở remote): tệp ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/repo` tại `c2d606b` — chỉ đọc.
- Bản tham chiếu đo: `ops/reviews/wp1236-r9-soan/`; `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/ISSUE.md`.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §10.2.2, §12, §20 · `docs/adr/0053*`, `0055*`, `0057*`–`0060*`, `0062*`, `0067*`.

## Việc phải làm
0. **Nhãn cho MỌI lớp của vòng 4** (U01, U02, U03 và 12 lớp lịch sử): `DA_VA_THAT` · `VA_MOT_PHAN` · `CHUA_VA` · `KHONG_DO_DUOC` trên r10, kèm trích dẫn/phép đo. Giữ slug của vòng 4; nếu tách/gộp, ghi `bang_noi_slug`. Cộng lớp `test-thieu-chot` của review mã lượt 6 (nối với `nghiem-thu-khong-co-lap-chot-dich` nếu bạn xét cùng cơ chế, ghi lý do).
1. **Cách làm mới có đóng được lớp không** (§12 checkpoint): tập toán tử đóng (a)–(l), ma trận nghĩa, kho đột biến reviewer làm hồi quy. Có toán tử/họ đầu vào nào mà review mã lượt 6 hay bạn nghĩ ra vẫn nằm ngoài? Luật có đủ chặt để executor không tự suy, và có kiểm được (reviewer chạy lại được) không? Nếu cách làm này vẫn không chống đỡ được bằng phép đo, nói thẳng (đó là E1).
2. **Quét lớp trước khi báo**; không báo lỗi lẻ.
3. Phần còn lại của đặc tả không đổi so r9 nhưng phải nhất quán với chỗ đổi (Windows, hợp đồng đầu ra, kích thước 1324/1400, `luat_dung`).

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (reviewer xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA); P3 không tự động "không chặn". Mỗi P2 trở lên phải có phép đo hoặc trích dẫn.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/work/VERDICT.json`, ghi tăng dần; kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/work/VERDICT.json --vong 5` (phải `HOP_LE`; lưu vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/work/kiem_verdict.txt`). Khoá: `spec_sha256`, `vong`: 5, `findings` [`id` V01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table` [`slug`, `finding_ids`, `manifestations`, `highest_open_severity`, `nguon`, `common_fix`, `closing_check`, `ly_do_va_rieng`], `prior_class_status` [`slug`, `finding_cu`, `vong_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`vong4_sang_5`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r10-5-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
