# Review ĐẶC TẢ wp1236 r11 bản sửa 1 — vòng 11 — reviewer độc lập, theo PROTOCOL §8.3

Bạn là reviewer ĐỘC LẬP cho một ĐẶC TẢ packet (không phải mã), review class `sensitive`. Kho: ducthangho/tra-luat.

## Bối cảnh
Vòng 9 (`lich_su/VERDICT_vong9_codex.json`, r11 `8a77e523…`): `changes_requested` — Z01 P2 `nghiem-thu-khong-co-lap-chot-dich` (bảng đóng chưa chốt TẬP Ô HỮU HẠN có đầu vào/kỳ vọng/tuyến; chưa chốt ưu tiên giữa ngữ pháp, hồi quy và (a)/(b)), Z02 P3 `so-do-khong-cung-pham-vi-nguon` (127 ⇒ 152 ID). Chủ kho nâng trần Codex của PR #1459 lên 12 và chọn liệt kê ô (E2 + E1, #1236 issuecomment-7057440613). Đây là lời gọi 12/12 (CUỐI). Vòng 10 (`lich_su/VERDICT_vong10_codex.json`, bản sửa 1): AA01 P2 — băm chưa phủ hạt giống đầu vào và phép chiếu; bản sửa 2 đưa `hat_giong` (fixture kèm sha256 byte, readback, dòng miễn, mẫu lời khai, hồ sơ consumer) và `chieu` vào đối tượng được băm `628e2704…`, bộ test đọc mọi đầu vào gốc từ hạt giống. Bản sửa 1: tập 125 ô đóng băng `ops/specs/wp1236-r11-bang-o.json` (băm JSON chuẩn `6f129585…`), thứ tự ưu tiên luật 1/2/4/5 trước luật 6, phân hạng theo ô phân biệt, kho cộng dồn 152 ID có băm, seam độc lập nền.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/work/`.

## Đầu vào
- Đặc tả: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/SPEC.md`, sha256 `30386131d8017bf982ca0be7707c8d5fd3035e9586c5f94a446f45c40fc863d1` (= `git show 2d9baf0:ops/specs/wp1236-r11.md`). Kiểm sha256 trước; lệch thì dừng. Phần mới so vòng 9: `git diff 90cb0a6 2d9baf0 -- ops/specs/`.
- Kho `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/repo` HEAD `2d9baf0` (nhánh đặc tả). Hiện vật review mã lượt 7–8 và kho 152 ID: `ops/reviews/wp1236-a-r10-ma-{7,8}-codex/` tại `b6c0063`.
- Mã thi công tham chiếu (để kiểm đặc tả có thi công được và tập ô có khớp không, KHÔNG phải đối tượng review mã): nhánh `ma-2719f81` — `ops/gate_output_doi_chieu_test.py` sinh tập ô bằng `bang_o()`, so băm `BAM_BANG_O`, chạy qua `chay_o` (ca `a126_tap_o_dong`); `a127` hợp đồng đầu ra hai nền; `a128` seam. Mã sản phẩm `ops/gate_output_doi_chieu.py` không đổi so với `79b3c24`.
- `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/ISSUE.md`; `CLAUDE.md`; `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12; `docs/adr/0053*`, `0055*`, `0060*`, `0067*`. Lịch sử vòng 1–9 ở `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/lich_su/`.

## Việc phải làm
0. **Nhãn cho MỌI lớp còn mở của vòng 10** (AA01 và lớp lịch sử `VA_MOT_PHAN`): bốn nhãn §8.3 ở MỨC ĐẶC TẢ, kèm phép đo. Giữ slug.
1. **Tập ô có thật sự hữu hạn, xác định và kiểm được không**: tệp JSON khớp băm khai; `bang_o()` ở `ma-2719f81` sinh đúng tệp ấy; mỗi kỳ vọng có suy được từ LUẬT của hàng trong đặc tả (mục *Module mới*) chứ không chép từ mã; executor và reviewer có cho CÙNG một phân hạng cho cùng một đột biến không; thứ tự ưu tiên có khép mọi trường hợp không.
2. **Phủ**: tập ô có bao đủ mọi họ đã gây P2 ở lượt mã 6–8 (`kho_dot_bien_reviewer_luot6_7_8.jsonl`) không — đo: áp từng `r7_*`, `r8_*` lên mã sản phẩm rồi chạy riêng `a126` tại `ma-2719f81`; đột biến nào có ô phân biệt mà a126 vẫn xanh là lỗ thật. Hàng nào trong 45 không có ô và lý do có hợp lệ không.
3. Số tổng (152, 125, trần 2100 đề nghị) nhất quán; không mở lại lớp đã `DA_VA_THAT` trừ khi bản sửa 1 làm hỏng (có phép đo).

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (reviewer xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2 trở lên phải có phép đo hoặc trích dẫn.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/work/VERDICT.json`, ghi tăng dần; kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/work/VERDICT.json --vong 11` (phải `HOP_LE`; lưu vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/work/kiem_verdict.txt`). Khoá: `spec_sha256`, `vong`: 11, `findings` [`id` AB01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table` [`slug`, `finding_ids`, `manifestations`, `highest_open_severity`, `nguon`, `common_fix`, `closing_check`, `ly_do_va_rieng`], `prior_class_status` [`slug`, `finding_cu`, `vong_xuat_hien`, `status`, `evidence`, `chua_do_duoc`], `bang_noi_slug`, `hoi_tu` {`vong10_sang_11`: "|F|/|U|", `lop_lap_lan_ba`: [...]}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r11-11-codex/work/VERDICT.md` — tóm tắt; dòng cuối `KET_LUAN: approve | changes_requested`.
