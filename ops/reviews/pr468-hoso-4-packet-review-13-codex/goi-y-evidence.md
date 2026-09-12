# Gợi ý bổ sung phương pháp cho EVIDENCE — dữ liệu reviewer

chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit

Trích ứng viên bằng `python3 -B do-review13/claims_inventory.py`: sáu tệp hồ sơ vừa đổi,
git diff --unified=0 từ 02b0b86 tới f77f198, lấy dòng thêm có chữ số rồi phân loại thủ công.
Bộ lọc bắt cả SHA/ngày/ID, bỏ sót số viết bằng chữ, câu không đổi và lỗi ngữ nghĩa;
hiện vật lịch sử bất biến được kiểm manifest riêng. Mọi mục bỏ sót mà reviewer phát hiện
vẫn được tính là finding. Executor phải xuất script/lệnh tương đương cùng gói kế tiếp.

Bổ sung bảng số 23631 B và manifest 178/178 (reviewer đã băm lại); 1166.934 s,
536028 B, prompt hash, model 6/6 và hai preflight rc=11 là lời khai vận chuyển;
gói chưa có raw run/session/prompt, KHÔNG ĐO ĐƯỢC độc lập. Không biến manifest/schema
xanh thành xác thực model hoặc quyền merge. Giữ nguyên receipt/verdict lịch sử.
