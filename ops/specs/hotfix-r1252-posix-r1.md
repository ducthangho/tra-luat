# HOTFIX-R1252-POSIX r1 — đánh dấu posix cho đột biến r1252_ghi_de_dich_truc_tiep

- packet_id: HOTFIX-R1252-POSIX
- revision: 1
- Issue: #1272 · tracker #1206
- Chủ kho chọn "Mở packet hotfix" ngày 2026-11-07 (phiên điều phối session_015GtxrYPjZCTZeRiazdssgq).

## 1. Vấn đề

Push master `27fd80803e9a8f80e660752f58c8dd477e9730c8` làm workflow `launcher-windows.yml` đỏ
(run 42360967762). Job `windows-latest`, bước `Tu dot bien`, báo `DOT BIEN 520/521`. Đột biến đỏ
duy nhất là `r1252_ghi_de_dich_truc_tiep SAI giet 0/1`.

Giả thuyết, CHƯA ĐO: đột biến đó sửa một dòng chỉ chạy khi `_CO_DIR_FD` đúng. Trên Windows
`_CO_DIR_FD` là False, nên ca đích không thể giết được đột biến ở đó.

## 2. Việc phải làm

A1. ĐO TRƯỚC, trên máy `tra-luat-win`, rồi mới sửa:
- giữ khoá `C:\tl-win\KHOA.txt`;
- chỉ chạy tập trung, KHÔNG chạy `--dot-bien` toàn bộ;
- in giá trị `_CO_DIR_FD` của `launcher.py` tại `27fd808`;
- áp đúng đột biến lên một BẢN SAO, chạy riêng ca đích `r1252_ghi_bang_chung_an_toan`, ghi kết quả.

Nếu số đo bác giả thuyết (ví dụ `_CO_DIR_FD` là True trên Windows, hoặc ca đích đỏ) thì DỪNG và
báo phiên điều phối, không vá theo đoán.

A2. Nếu giả thuyết đúng: thêm phần tử thứ tư `("posix", "<lý do>")` cho entry
`r1252_ghi_de_dich_truc_tiep` trong bảng đột biến của `.claude/dev/launcher_test.py`. Dùng đúng
cơ chế đã có, như entry `ban_chup_de_ho_quyen`. Lý do phải nói rõ nhánh `dir_fd` không có trên Windows.

A3. Phản chứng trên Linux: đột biến `r1252_ghi_de_dich_truc_tiep` vẫn bị ca đích giết.

A4. Bộ test `launcher_test.py` trên Linux: số ca qua bằng nền, không thêm hay bớt ca.

A5. Không đổi hành vi của `launcher.py`. Không đổi entry đột biến nào khác.

## 3. Trần

- Diff PR: đúng 1 tệp `.claude/dev/launcher_test.py`, ≤ 15 dòng thêm, ≤ 5 dòng xoá.
- Review: một lượt connector `@codex review` trên PR. Có finding P1–P3 thì vá và review lại,
  tối đa 3 lời gọi Codex. Vượt ⇒ Review Rescue Checkpoint, hỏi chủ kho.

## 4. Ngoài phạm vi

- Việc `launcher-windows.yml` tự chạy toàn bộ đột biến trên Windows khi push master. Đây là
  chuyện chính sách CI, sẽ ghi thành nợ riêng.
- Sửa `launcher.py`.

## 5. Hoàn tất

PR merge vào master. Lượt `launcher-windows` kế tiếp trên master không còn đỏ vì đột biến này.
Nếu không có lượt nào tự chạy thì nêu rõ là chưa đo được.
