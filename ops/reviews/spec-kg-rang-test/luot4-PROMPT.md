# Review đặc tả packet wp822 (#822) — lượt 4, offline

Bạn là reviewer độc lập (họ openai). Trả lời tiếng Việt. Ghi kết luận vào tệp đầu ra `-o`.

- Kho `ducthangho/tra-luat`, checkout hiện tại HEAD phải là `a5305449893109a62fe04f9a7f4ae2d7fd27534e`
  (kiểm `git rev-parse HEAD`; lệch thì `blocked`). Lịch sử: `fb490a7` (master) → `0b1ca26` (lượt 1) → `5e34b5d` (lượt 2) → `435dd91` (lượt 3) → HEAD (vá P3 lượt 3).
- Thay đổi duy nhất: tệp mới `ops/specs/wp822.md` — đặc tả đóng băng cho một packet sẽ do một phiên KHÁC thi hành.
- Ngữ cảnh: đọc `.claude/skills/soan-spec/SKILL.md` (luật L1–L6 cho đặc tả), `docs/PROTOCOL_DA_PHIEN.md`,
  `.claude/dev/packet_loop.py` (hàm `_doc_check_runs`, `cmd_kiem_gate`), `.claude/dev/packet_loop_test.py`
  (họ ca `kg_*`, bảng `MUTANTS`, bộ chạy đột biến `chay_suite`/`_phan_loai_dot_bien`/`_doi_chung_khac_ho`),
  `ops/specs/wp788.md` nếu có (không có trên master thì bỏ qua), ADR-0052/0053.

Review như một code review thông thường của connector, KHÔNG lọc theo mô hình tin cậy hay theo phạm vi bạn đoán chủ
kho quan tâm. Báo mọi lỗi thật với mức P0–P3. Nhóm finding theo LỚP. Finding hợp lệ gồm:
- dữ kiện sai về mã/kho (hãy ĐO: chạy lệnh, dựng probe trên bản sao trong /tmp, không sửa checkout);
- cặp tìm/thay D1–D6 không khớp đúng một chỗ trong `packet_loop.py`, hoặc không gỡ đúng thành phần khai;
- tiêu chí nghiệm thu không thể ĐỎ, hoặc đỏ/xanh vì lý do khác thứ nó khai đo (L3, L6);
- mục tiêu đòi thứ write set (1 tệp) không kham được (L2), mâu thuẫn nội bộ, con số không có đơn vị/thời điểm (L1, L5);
- bảng kiểm kê thiếu thành phần thật của hai hàm (gỡ ra thì lệnh cấp xanh giả / đổi lý do);
- yêu cầu nào executor không thể thực hiện được với bộ chạy đột biến hiện có của suite.

Đặc biệt hãy chạy thử: áp D1–D6 lên bản sao `packet_loop.py`, chạy các ca `kg_*` (vd nạp module test,
`chay_suite(script, dir, chi_chay={k for k in _KG_CA})`) và xác nhận lời khai "6 đột biến do=0 trên 100 ca, nền 100/100".
Cũng kiểm lời khai A3 (nền: `thiếu/sai kiểu trường ['conclusion']`; D6: `THỪA id`).

Dạng đầu ra:
```
verdict: approve | changes_requested | blocked
reviewed_sha: <40>
dem: P0=<n> P1=<n> P2=<n> P3=<n>
```
rồi finding theo lớp (id, mức, vị trí `ops/specs/wp822.md:dòng`, phép đo chạy được + output, HINT sửa), rồi bảng
kiểm các lời khai số đã đo lại. `approve` chỉ khi P0=P1=P2=P3=0.

## Đối chiếu lượt trước
Verdict lượt 1 (changes_requested, P2=4: S822-01..04) ở `/tmp/claude-0/-home-user-tra-luat/353bc79e-3dd4-5d53-a13a-54256c3f5d49/scratchpad/rv822-4/verdict-luot1.md và lượt 2 (P2=1, S822-02 tái mở) ở /tmp/claude-0/-home-user-tra-luat/353bc79e-3dd4-5d53-a13a-54256c3f5d49/scratchpad/rv822-4/verdict-luot2.md, lượt 3 (P3=1, S822-04 tái mở thu hẹp) ở /tmp/claude-0/-home-user-tra-luat/353bc79e-3dd4-5d53-a13a-54256c3f5d49/scratchpad/rv822-4/verdict-luot3.md`. Với từng finding, xếp ĐÃ ĐÓNG / CÒN MỞ
kèm phép đo, rồi đọc diff `435dd91..HEAD` đối kháng: bản vá có mở mâu thuẫn mới, có đòi thứ write set không kham được,
có tiêu chí mới nào không thể đỏ (đặc biệt M6/A12, A11, ba dạng ca của M3, K37) không. Vẫn báo mọi lỗi mới thấy.
