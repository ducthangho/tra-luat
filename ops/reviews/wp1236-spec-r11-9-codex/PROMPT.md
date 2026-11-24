# Review ĐẶC TẢ wp1236 r11 — vòng 9 — reviewer độc lập, theo PROTOCOL §8.3

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã), review class `sensitive`. Kho: ducthangho/tra-luat.

## Bối cảnh
r10 bản sửa 3 được approve ở vòng 8 (`lich_su/VERDICT_vong8_codex.json`). Thi công đợt A theo r10 ra review MÃ lượt 7 (`lich_su/VERDICT_ma_luot7.json`, `f4f17bc`) và lượt 8 (`lich_su/VERDICT_ma_luot8.json`, `5a1bf33`), cả hai `changes_requested` cùng lớp `test-thieu-chot` P2 sau hai cách sửa khác nhau; hội tụ mã 7→8 = 0/2. Gốc đo được: r10 coi MỌI đột biến sống không tương đương mà reviewer tự dựng là P2, miền đột biến không có biên (25 → 14 → 11 với họ mới mỗi lượt). Chủ kho quyết **E1** (#1236 issuecomment-7057154780): **đóng miền** bằng r11. r11 thêm luật 6 (bảng đóng 45 điểm so × họ biến đổi H1–H10, phân hạng (a) P2 trong bảng / (b) P3 `ngoai_bang_dong`), luật 7 (hợp đồng đầu ra hai nền), dạng ledger `KHONG_AP_DUNG → <id> TUONG_DUONG`, mô tả `tep_danh_gia` theo token tối đại (lookbehind không bắt buộc), và đề nghị trần 2100 (E2, chờ chủ kho duyệt cùng spec_hash).

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/work/`.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/SPEC.md`, sha256 `8a77e52341ba6f3a9785d10f938cb91c11e7223f69ed1154ed4bb1ee5adfd887` (= `git show 9f7fd71:ops/specs/wp1236-r11.md`). Kiểm sha256 trước; lệch thì dừng. Phần mới: `git diff --no-index ops/specs/wp1236-r10.md ops/specs/wp1236-r11.md`.
- Kho `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/repo` HEAD `9f7fd71` (nhánh đặc tả). Inventory mà luật 6 neo vào: `git show b6c0063:ops/reviews/wp1236-a-r10-ma-8-codex/comparison_coverage.json` (và `comparison_inventory.json`); hiện vật review mã lượt 7–8 dưới `ops/reviews/wp1236-a-r10-ma-{7,8}-codex/` tại `b6c0063`. Mã đợt A lượt 8: nhánh `ma-5a1bf33` (`ops/gate_output_doi_chieu.py`, `ops/gate_output_doi_chieu_test.py`).
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/ISSUE.md`; `CLAUDE.md`; `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12; `docs/adr/0053*`, `0055*`, `0060*`, `0067*`. Lịch sử vòng 1–8 ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/lich_su/`.

## Việc phải làm
0. **Nhãn cho MỌI lớp còn mở của vòng 8 đặc tả và lượt 8 mã** (`test-thieu-chot` = `nghiem-thu-khong-co-lap-chot-dich`, `hop-dong-dau-vao-dau-ra-chua-chot`): bốn nhãn §8.3 ở MỨC ĐẶC TẢ (đặc tả đã đủ để một bản thi công đóng lớp chưa), kèm trích dẫn/phép đo. Giữ slug.
1. **Bảng đóng có thật sự CÓ BIÊN và KIỂM ĐƯỢC không**: 45 hàng có khớp mọi điểm so chuỗi/miền của `ops/gate_output_doi_chieu.py` tại `ma-5a1bf33` (tự liệt kê lại từ mã, đừng tin inventory); H1–H10 có phủ mọi họ đã gây P2 ở lượt 6–8 không; định nghĩa ô áp dụng có đủ rõ để executor và reviewer cho CÙNG một tập ô không; phân hạng (a)/(b) có quyết định được cho mọi đột biến sống không, có lỗ nào để một đột biến lẽ ra (a) bị đẩy thành (b) hoặc ngược lại.
2. Luật 7 có đủ chặt để chặn lại N03 và các biến thể (khai báo bỏ qua chen khối, mẫu số giả) không; seam độc lập nền cho m65/m79 có đặc tả đủ không.
3. Luật 5 dạng `KHONG_AP_DUNG → TUONG_DUONG` có mở lỗ né hồi quy không; mô tả mới của `tep_danh_gia` có đổi luật cổng không (chứng minh tương đương hay phản chứng).
4. **Quét lớp** trước khi báo; số tổng, `nang_tran` (1700 → 2100) có nhất quán không. Không mở lại lớp đã `DA_VA_THAT` trừ khi r11 làm hỏng chúng (có phép đo).

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (reviewer xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2 trở lên phải có phép đo hoặc trích dẫn.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/work/VERDICT.json`, ghi tăng dần; kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/work/VERDICT.json --vong 9` (phải `HOP_LE`; lưu vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/work/kiem_verdict.txt`). Khoá: `spec_sha256`, `vong`: 9, `findings` [`id` Z01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table` [`slug`, `finding_ids`, `manifestations`, `highest_open_severity`, `nguon`, `common_fix`, `closing_check`, `ly_do_va_rieng`], `prior_class_status` [`slug`, `finding_cu`, `vong_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`vong8_sang_9`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-9-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
