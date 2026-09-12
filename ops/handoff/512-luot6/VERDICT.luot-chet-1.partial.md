verdict: in_progress
reviewed_sha: 353eae10120da2a1788dcaf7a906fe46261bd71b
reviewed_base: 015ffcc09d76fbc9cdfbc3d2ee0735c3ead8d364
reviewed_files_sha256: pending
model_tu_khai: GPT-6 (Codex); khác nền tác giả Claude Opus 5 theo EVIDENCE.md
review_round: 6
so_p1: pending
so_p2: pending
so_p3: pending
so_the_hien: pending
hint_sha256: pending
previous_hint_sha256: 9087726521c621617de5dc9fc40eab5e0f302f928662d23a8c62d47e81b47cdc

## ĐỐI CHIẾU LƯỢT TRƯỚC
Đang kiểm độc lập bảy lớp và năm thể hiện mở của lượt 5.

## BẢNG ĐO
Đã đọc lời khai và trích CI thật; chưa công nhận các số cho đến khi đo.

## Findings theo lớp
Đang đo, chưa kết luận.

## Mutant đã chạy
Chưa chạy.

## chua_do_duoc
Windows tại HEAD này; không mạng/CI theo giới hạn người dùng. Gốc S8 ngoài write set được tách khỏi đề xuất sửa.

### Cập nhật phép đo độc lập (chưa chốt)
- HEAD/base/hash/merge/write set và năm neo dòng của log tác giả đã khớp. Bảng S2 67/195/746/914/991/1082 tái lập từ base lease b98531e; lease thật lấy từ ref offline origin/ops/cap-lease-504.
- Full wrapper trên bản sao chọn lọc đã đạt 155/155 ×3 với TAR_OPTIONS=--no-same-owner. Lần nguyên dạng rc=5 do ownership tar; một lần đặt TMPDIR trong cây bị lỗi sao chép đệ quy của harness đã hủy, không tính làm finding.
- Catalogue 16/16 giết thật được chạy lại; riêng control lỗi vô can Exception trần bị catalogue tính nhầm GIẾT THẬT, RuntimeError bị loại đúng.
- M15/M16/M17 chết đúng chốt. N01/N02 đảo nhãn A/B vẫn qua t160; N10 bỏ luồng tee tại t125 vẫn qua t158; N12 hồi sinh retry qua Popen vẫn qua t160. Đang kiểm full wrapper và chuẩn bị HINT đúng write set.
- HEAD thật: mismatch giả tại biên tiến trình sinh đúng hai vế, bốn tee, không run/Popen phụ. Timeout 0.5s qua consumer thật thu hồi hai cháu: nhịp 13→13 và 12→12.
