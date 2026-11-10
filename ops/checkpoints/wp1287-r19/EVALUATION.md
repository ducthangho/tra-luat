# Đánh giá pilot so với quy trình hiện hành

Protocol8/8.3/12 đã yêu cầu stable ID, gom lớp, đối chiếu lỗi cũ và checkpoint sau ba lượt. Pilot giữ các điều đó và thêm hợp đồng file/line bắt buộc, discovery chỉ delta sau lượt đầu và cấm lặp finding cũ trong findings[]. Lỗi cũ chưa đóng vẫn chặn, được ghi trong bảng trạng thái và kiểm regression; đọc ngữ cảnh chỉ để hiểu hunk mới. Không sửa protocol chung.

Số đo trước review: candidate mới có400 dòng thêm trong ba tệp so B; delta từ H2 có44 dòng thêm+21 dòng xoá=65 dòng thay đổi trong một tệp. Discovery scope giảm83,75% theo dòng thay đổi (65/400), không phải số token hoặc thời gian tiết kiệm đã đo. Quét cùng pattern sửa thêm các biểu hiện Bash hash/pipeline và PowerShell version/empty TargetId ngoài ba biểu hiện preflight ban đầu.

Kiểm chứng nguồn: Bash Linux25/25; PowerShell5.1/7 native70/70. Các số này gồm ca dương, ca âm, config emitter và đối chứng mutant; không gọi là95 ca browser hoặc95 core tests. Core selftest độc lập1777/1777. Một lần kiểm guard đầu tiên bắt nhánh Bash rc1 chưa dừng; giữ kết quả hỏng và sửa trước lúc đóng băng review. Đây là phản hồi có ích từ phép thử, không là independent finding mới.

Chưa có thí nghiệm A/B ngẫu nhiên hoặc đo token; không kết luận nhanh hơn theo hệ số. Delta-only giảm đọc lại nhưng có nguy cơ bỏ lỗi nền/cắt ngang; pilot giảm rủi ro bằng full review r18 đã có, regression cho lớp cũ, đọc phụ thuộc cần thiết và giữ nguyên nghĩa vụ OP-F01/U10/assurance. Chưa đóng lớp chỉ vì test tổng xanh. Kết quả reviewer sẽ được ghi riêng sau khi có verdict.
