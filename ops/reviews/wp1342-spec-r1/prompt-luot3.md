Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 3, cho ĐẶC TẢ `ops/specs/WP1174-WINDOWS-BACKEND-r1.md` trong thư mục làm việc (worktree base a0702d0, đặc tả untracked). CHỈ ĐỌC; không ghi tệp; không gọi mạng.

Lượt 2 (bạn) trả `request_changes`: P2-R2-01 N2 bảo toàn byte; P2-R2-02 fixture mở lại tên/metadata không dựng được với share mode; P2-R2-03 `_1174_win_read` chưa cưỡng chế profile NTFS/tệp thường/dạng tên; P2-R2-04 N1 so số khoá; P3-R2-05 N6 thiếu đối chứng. Người soạn đã sửa tất cả, và để giữ dưới trần ADR-0053 (450 dòng thêm; ba phép đo hiệu lực đã chạy đạt) đã BỎ runner đột biến khỏi kho: đột biến do phiên điều phối chạy bằng driver ngoài kho (M6, N7).

Việc:
1. Từng finding lượt 2: đóng / chưa đóng, kèm chỗ trong đặc tả.
2. Xét kỹ tính khả thi trên Windows của fixture M5 mới: (a) đổi tên THƯ MỤC CHA trong lúc/khi tệp con đang có handle mở với share READ không DELETE — Windows có cho đổi tên thư mục cha khi một tệp con đang mở không? Nếu không, đặc tả cần nói `_1174_win_read` đóng handle trước khi mở lại, hay đổi fixture thế nào; (b) handle `FILE_WRITE_ATTRIBUTES` thứ hai khi handle đọc share chỉ READ — có mở được không. Đề xuất câu thay thế cụ thể nếu sai.
3. Lỗ mới do sửa đổi: M6 đột biến ngoài kho có làm tiêu chí N7 khó tái lập hay lách được không; N2 "ca test đọc blob base qua git show" có chạy được trong CI (clone nông? base có mặt?) không.
4. Kiểm lại L1–L7 nhanh; dự toán kích thước sau khi bỏ runner.

Đầu ra: bảng đóng finding; finding mới P0–P3 kèm câu thay thế; dự toán. Dòng CUỐI đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes` (approve chỉ khi không còn P0–P2).
