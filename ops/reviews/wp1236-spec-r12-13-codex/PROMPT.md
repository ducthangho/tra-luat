# Review ĐẶC TẢ wp1236 r12 — vòng 13 — reviewer độc lập, theo PROTOCOL §8.3

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã), review class `sensitive`. Kho: ducthangho/tra-luat. Lời gọi Codex 14/14 (CUỐI) của PR #1459 (chủ kho nâng trần, #1236 issuecomment-7062258757).

## Bối cảnh
r11 bản sửa 2 (`30386131…`) approve ở vòng 11 (`lich_su/VERDICT_vong11_codex.json`). Thi công đợt A theo r11 ra review MÃ lượt 9, 10, 11 (`lich_su/VERDICT_ma_luot{9,10,11}.json`) cùng P2 `test-thieu-chot` ở miền ngữ pháp luật 4, hội tụ 1/2 → 0/1 → 0/1: regex dùng `\d`/`\s`/`\S`/`\w` là lớp UNICODE, đột biến loại một tập con bất kỳ luôn dựng được, vét cạn bằng test không hội tụ. Chủ kho quyết E1 (#1236 issuecomment-7062234670): r12 đổi ngữ pháp sang lớp ASCII đóng (luật 8) với năm chỗ văn bản tự do có mệnh đề ràng buộc tường minh. Đây là ĐỔI LUẬT CỔNG (chủ kho đã chọn hướng; còn phải duyệt băm sau review).

Vòng 12 (`lich_su/VERDICT_vong12_codex.json`, r12 `0acd3f87…`): changes_requested — AC01 P2, AC02 P2, AC03 P2, AC04 P3. Chủ kho quyết E1 (#1236 issuecomment-7062521692): ĐÓNG TẬP TOÁN TỬ — bản sửa 1 thêm luật 9 (miền bắt buộc = manifest bộ quét ghim 24 toán tử (A) ∪ kho 201 ID (B); đột biến reviewer tự dựng ngoài (A)∪(B) là P3 `ngoai_bang_dong`; thứ tự xét duy nhất), sửa luật 8 (bỏ lời khẳng định vét cạn, mệnh đề văn bản tự do theo ngữ nghĩa backtracking, điều kiện chung UTF-8/CR/LF, Cs, D2b là văn bản tự do thứ sáu, kho lịch sử xét trước) và số liệu (201 ID, nang_tran). Kiểm phần mới: `git diff 04095f1 138ecd7 -- ops/specs/`. Với luật 9, kiểm: (A) có thật sự tất định và hữu hạn (chạy `quet_dot_bien.py sinh` trên module `ma-0d81487` hai lần, so manifest); thứ tự xét có cho hai reviewer cùng phân hạng không; phạm vi P3 `ngoai_bang_dong` có mở lỗ để chuyển một lỗ thật (mã sai) thành P3 không — luật 9 chỉ áp cho lớp `test-thieu-chot`, lỗi hành vi của mã vẫn là finding theo mức thật.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/work/`.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/SPEC.md`, sha256 `8372a138e5121f108e0547cf86d3a6289c5ddeb5e69ce7b172a062eb9b9f9f39` (= `git show 138ecd7:ops/specs/wp1236-r12.md`). Kiểm sha256; lệch thì dừng. Phần mới: `git diff --no-index ops/specs/wp1236-r11.md ops/specs/wp1236-r12.md`.
- Kho `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/repo` HEAD `138ecd7` (nhánh đặc tả). Mã đợt A theo r11 (tham chiếu, CHƯA theo r12): nhánh `ma-0d81487`. Hiện vật review mã lượt 9–11 và kho đột biến cộng dồn ở nhánh `lease-moi` (`ops/reviews/wp1236-a-r11-ma-{9,10,11}-codex/`).
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/ISSUE.md`; `CLAUDE.md`; `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12; `docs/adr/0053*`, `0055*`, `0060*`, `0067*`. Lịch sử ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/lich_su/`.

## Việc phải làm
0. **Nhãn cho MỌI lớp còn mở** (`test-thieu-chot`/`nghiem-thu-khong-co-lap-chot-dich` ở mức đặc tả sau review mã lượt 9–11): bốn nhãn §8.3, kèm phép đo/trích dẫn. Giữ slug.
1. **Luật 8 có làm miền ngữ pháp HỮU HẠN và vét cạn được thật không**: mọi regex của mục *Module mới* (và D2b của đợt C) chỉ còn lớp ASCII đóng + literal + đúng năm chỗ văn bản tự do; danh sách mệnh đề ràng buộc văn bản tự do có đủ để executor/reviewer phân hạng CÙNG một kết quả cho cùng đột biến (P2 nới / P3 thu hẹp); còn lớp nào vô hạn bị bỏ sót (`.`, `[^\]]`, `[^/]`, lookahead…); kho đột biến 186 ID và 15 cặp lượt 11 xử lý thế nào theo luật 5 (đo: áp từng cặp `r11_*` lên bản ASCII tưởng tượng — mô tả bằng lời là đủ).
2. **Đổi luật cổng có an toàn không**: đo lại trên `ops/land/**` tại base `8048551` (66 tệp đánh giá, 170 hồ sơ) rằng không tệp/hồ sơ nào đổi kết quả; có hồ sơ/readback thật nào dùng URL ngoài lớp `[A-Za-z0-9._~/%-]` không.
3. **Quét lớp** trước khi báo; số tổng, `nang_tran` (2100, numstat r11 1985 — r12 cần viết lại ca ngữ pháp) nhất quán. Không mở lại lớp `DA_VA_THAT` trừ khi r12 làm hỏng (có phép đo).

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (reviewer xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2 trở lên phải có phép đo hoặc trích dẫn.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/work/VERDICT.json`, ghi tăng dần; kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/work/VERDICT.json --vong 13` (phải `HOP_LE`; lưu `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/work/kiem_verdict.txt`). Khoá: `spec_sha256`, `vong`: 13, `findings` [`id` AD01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table` [`slug`, `finding_ids`, `manifestations`, `highest_open_severity`, `nguon`, `common_fix`, `closing_check`, `ly_do_va_rieng`], `prior_class_status` [`slug`, `finding_cu`, `vong_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`vong12_sang_13`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r12-13-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
