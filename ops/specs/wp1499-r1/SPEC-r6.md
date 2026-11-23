# WP1499 r6 — Cập nhật fixture kiểm biên nhận theo route AGY

Kế nhiệm r5 tại 874a586679d2e7170153ab83fdab3d7a42cec512, SHA-256 10d4d67abed73bc0f827106a6e725006122c240bdc3837238e6207bbd3841a54. Giữ nguyên base a2bdb480e8fb54c152af190378c434fa41b0feaf, mục tiêu, phân công Codex executor và reviewer Antigravity độc lập, cổng bảo mật và toàn bộ tiêu chí r5. Thay thế duy nhất danh sách write set nguồn và bổ sung điều kiện kiểm fixture dưới đây. Chưa cấp lease cho r6.

## Write set

- .claude/dev/launcher.py
- .claude/dev/launcher_test.py
- ops/bien_nhan_v2_test.py

Kế thừa diff executor g3 đã giữ ở dạng patch, hai tệp Launcher. Không tái sử dụng approval, gate hoặc verdict cũ cho candidate mới. Trong tệp thứ ba chỉ đổi fixture của c28/c44 và hằng đầu vào trực tiếp dùng bởi hai ca. Giữ nguyên validator production ops/bien_nhan_v2.py, hợp đồng transport, ngưỡng bảo mật và phép kiểm hiện hành. Không sửa bộ test để bỏ qua lỗi sở hữu Git hoặc bỏ ca cho xanh.

## Nghiệm thu bổ sung

- c28 vẫn kiểm đúng bảng _PROVIDER_NGOAI_CLI bằng một hàng ngoài CLI thực tế còn lại. Chứng minh phép thay chỉ khớp đúng một hàng, tạo đúng vi phạm arity của bảng đó và giữ yêu cầu rc2 cùng nội dung chẩn đoán.
- c44 dùng hàng Antigravity CLI hiện hành. Làm sai riêng giá trị transport trong fixture, giữ nguyên các cột còn lại. Ca đối xứng phải nhận biên nhận machine/local trên hàng đúng và từ chối trên hàng fixture bị đổi sang machine. Giữ nguyên phép đối chiếu với bảng kế hoạch provider.
- Chạy hai bộ test hiện hành và các ca tập trung trên base/candidate phù hợp. Lỗi môi trường phải được tái hiện trên base trước khi phân loại, ghi command/rc/count và phân loại thật. Dùng checkout/fixture do đúng người chạy sở hữu. Không tắt kiểm tra Git hoặc thêm ngoại lệ tin cậy toàn cục.
- Các kiểm native Windows, holder exclusivity, receipt map, independent source review, exact-head audit và CI tiếp tục theo r5. Phạm vi review độc lập gồm toàn diff mới ở cả ba tệp.

Lịch sử: g2 và g3 đã dùng hai lượt executor. Review mã chính thức chưa dùng lượt nào. B4 và PR2 giữ 6/6 mỗi gói, chỉ kích hoạt theo điều kiện r98 sau khi WP1499 đạt.
