# Bản thử phục dựng gói lượt 8, thực hiện trong review lượt 9

Thư mục này là bản sao phục dựng gói lượt 8 dùng cho phép thử
`artifact_checks.py` của reviewer lượt 9. Nó không phải lần chạy test mới trên
head lượt 9 hay head lượt 10. Các timestamp, đường dẫn scratch và số đo bên trong
thuộc hiện vật lịch sử lượt 8; giữ nguyên để truy nguồn.

`../artifact-checks.json` ghi lượt 9: bản lượt 8 gốc khi ấy có 50/69 tệp,
bản thử phục dựng đạt 69/69. Khi chép bản thử vào kho tại c43347d, 19 tệp rig/
lại bị thiếu. Gợi ý lượt 10 điền chúng bằng byte có đúng băm từ gói lượt 8
đã hoàn chỉnh, không sửa manifest để bỏ cam kết. `sha256sum --check ARTIFACTS.sha256`
trong bản gợi ý đạt 69/69. Kết quả thử này không biến suite lịch sử thành suite mới chạy.

chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit
