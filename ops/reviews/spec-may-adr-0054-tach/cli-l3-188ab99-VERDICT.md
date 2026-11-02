VERDICT: changes_requested
P0=0 P1=0 P2=1 P3=0

## Lớp khoi-tao-moi-mau-thuan-duong-cu — P2

- biểu hiện: ops/specs/wp812.md:M1 — `record-lease` bắt buộc đọc lease remote, kiểm I2 và đặc tả trước khi xác định chế độ, nhưng I9 vẫn yêu cầu giữ nguyên các ca cũ vốn không dựng những hiện vật này.
- biểu hiện: ops/specs/wp815.md:M2 — Nhóm NGỮ CẢNH vẫn được định nghĩa bằng tập khóa mà `init` của #812 ghi từ lease, trong khi #812 M1 và I9 vừa giữ `init` nguyên trạng, chuyển việc đọc lease sang `record-lease`.
- đường lỗi cụ thể: `Ctx.cap_lease` tại `.claude/dev/packet_loop_test.py:282` chỉ truyền bốn trường lease trực tiếp; mã hiện hành nhận và chuyển sang `leased`. Áp nghĩa vụ remote của M1 vô điều kiện sẽ làm đường cũ đỏ, trái I9. Với generation kế tiếp, `init` hiện hành ghi `lease=None`, không ghi `branch`, `generation` hay `spec_hash` từ lease; lấy đúng tập khóa theo #815 M2 sẽ bỏ sót ngữ cảnh do `record-lease` tạo, khiến nhánh hoặc đặc tả g1 bị chép sang g2, trái chính nghiệm thu #815. Phép đo dùng hàm thật với `_load`/`_save` thay bằng RAM xác nhận các dữ kiện này.
- hướng sửa ở mức lớp: Chốt rõ ranh giới tương thích tại `record-lease`, đồng thời đổi #815 M2 sang lấy tập khóa từ nơi thực sự dựng ngữ cảnh lease. Khóa bằng hai đối chứng: lời gọi lease cũ tiếp tục chạy; g2 thay toàn bộ ngữ cảnh bằng lease mới và ca phải đỏ khi đột biến chép ngữ cảnh cũ. Giữ chốt ngăn packet đã xác định áp ADR-0054 quay sang đường cũ.