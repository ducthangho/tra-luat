# ADR-0049 — Cổng hai nền trước phát hành, không phải mỗi lần land

- **Trạng thái:** Accepted (2026-09-16, chỉ thị chủ kho `ducthangho`; packet #548 `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`)

ADR này ghi nhận việc **đổi tiêu chuẩn gate**: cổng kiểm thử hai nền (Linux và Windows) trước khi phát hành được bảo đảm bằng **cổng tại chỗ của `deploy-package.*`**, KHÔNG phải bằng lane `master` của `.github/workflows/ci.yml`.

## 1. Bối cảnh & Hiện trạng đo được

Từ quyết định grilling 2026-07-09 (#8), `ci.yml` chạy cả `ubuntu-latest` và `windows-latest` để bắt lớp lỗi phụ thuộc nền (mã hóa cp1258, ký tự xuống dòng, đường dẫn file). Tuy nhiên, các phép đo thực tế (16-09-2026, nền `f27a28f`) cho thấy hai bất cập lớn:

1. **Hậu quả chặn = 0:** Lane Windows trên `master` chạy **SAU** khi PR đã merge. Không có cổng nào chặn land theo kết quả này. Thực tế PR #545 và #547 đều merge thành công trong khi lane Windows của `master` đỏ sẵn (delta = 0). Tức kho trả chi phí đầy đủ cho một tín hiệu không chặn được gì.
2. **Chi phí Actions cạn kiệt:** Runner Windows tính phí gấp đôi (hệ số 2). Đo r245 (13-08): ~20 phút tính tiền mỗi lượt × 13,6 lượt/ngày ≈ 8.100 phút/tháng, vượt xa hạn mức Free 2.000 phút/tháng và đã cạn kiệt thật vào ngày 12-08.
3. **Trôi lệch cấu trúc:** Ba job `gate`, `gate-registry`, `gate-packet-loop` mang ba bản chép nguyên văn cùng một biểu thức ma trận phức tạp.

## 2. Quyết định: Đổi tiêu chuẩn gate

1. **Đổi cò Windows trong `ci.yml`:** Bỏ điều kiện `github.ref == 'refs/heads/master'`. Windows chỉ còn kích hoạt khi gọi tay qua `workflow_dispatch` hoặc khi PR có nhãn `windows` (dành cho các thay đổi chạm mã phụ thuộc nền tảng).
2. **Khử trùng lặp qua job `chuan-bi`:** Thêm job `chuan-bi` (chạy trên `ubuntu-latest`, không checkout mã nguồn), tính danh sách nền một lần và xuất qua `outputs.os`. Ba job `gate`, `gate-registry`, `gate-packet-loop` khai `needs: chuan-bi` và đọc `needs.chuan-bi.outputs.os`.
3. **Cổng hai nền chuyển về `deploy-package.*`:** Trước khi phát hành gói (`tl drive-push` lên LIVE), người vận hành bắt buộc phải chạy bộ cổng kiểm tra tại chỗ của `deploy-package.ps1` / `deploy-package.sh` (8 cổng: `--selftest`, `doc-claims-check`, `doctrine-scan`, `adr-song`, `workflow-audit`, `golden-test`, `determinism-audit`, `release-verify`). Cổng này chặn thật khi đỏ (dòng 234: `Bad 'GATE ĐỎ — DỪNG, không build/không đẩy'`).

## 3. Phần mất mát & Rủi ro đã nhận

- **Mất soi Windows tự động cho ~22 bước test:** Việc bỏ Windows khỏi mỗi lần land vào `master` đồng nghĩa ~22 bước kiểm thử trong `ci.yml` (như `lease_publish_test`, `ci_dang_ky_test`, `packet-loop selftest`) không còn được chạy tự động trên Windows sau mỗi commit vào master.
- **Cổng Windows đang đỏ biến mất khỏi CI không phải vì được chữa:** Tại commit `f27a28f` và `a612c70`, lane Windows trên `master` đang đỏ sẵn 15 ca ở `lease-publish selftest` (nợ WP541 do hardcode `/usr/bin:/bin`). Việc bỏ Windows khỏi `master` làm tín hiệu đỏ này biến mất khỏi CI, nhưng ADR-0049 **KHÔNG** chữa nợ WP541 mà chuyển việc bảo đảm sang các cổng tại chỗ trước phát hành. Nợ WP541 vẫn còn nguyên.
- **Đường nhãn `windows` không tự sinh run khi PR đứng yên:** `ci.yml` dùng trigger `pull_request` mặc định (không khai `types: [labeled]`). Việc gắn nhãn `windows` lên một PR đang đứng yên sẽ không tự kích hoạt build; nhãn chỉ có hiệu lực ở lần push kế tiếp (`synchronize`) hoặc khi tạo PR đã có nhãn. Đây là rủi ro vận hành do người điều phối nhận và chịu trách nhiệm.
- Đây là **rủi ro đã nhận** (K4), được chấp nhận để đổi lấy việc bảo toàn hạn mức CI và phục hồi tín hiệu đọc được. Nợ có tên `BATTERY-DEPLOY-HEP-HON-LANE-CI` ghi nhận việc mở rộng danh mục kiểm thử của script deploy khi cần thiết.

## 4. Lời khai trung thực về Windows CI khi land

Tuyên bố *"land không còn chạy Windows"* là **KHÔNG đúng tuyệt đối**:
- Workflow `.github/workflows/launcher-windows.yml` (với `paths: .claude/dev/**`) vẫn được giữ nguyên. Mọi thay đổi chạm `.claude/dev/**` khi push vào `master` vẫn kích hoạt và tiêu tốn ~5 phút Windows (Đ6, run `35125176975`).
