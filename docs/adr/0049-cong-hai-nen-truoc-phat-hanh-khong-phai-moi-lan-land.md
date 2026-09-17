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
3. **Cổng hai nền tại chỗ của `deploy-package.*`:** Trước khi phát hành gói (`tl drive-push` lên LIVE), người vận hành bắt buộc phải chạy bộ cổng kiểm tra tại chỗ của `deploy-package.ps1` / `deploy-package.sh` (8 cổng: `selftest`, `gen_inst`, `workflow`, `golden`, `docclaims`, `determinism`, `relcheck`, `relverify`). Cổng này chặn thật khi đỏ (dòng 234: `Bad 'GATE ĐỎ — DỪNG, không build/không đẩy'`).

## 3. Phần mất mát & Rủi ro đã nhận

- **Mất soi Windows tự động cho ~22 bước test:** Việc bỏ Windows khỏi mỗi lần land vào `master` đồng nghĩa ~22 bước kiểm thử trong `ci.yml` (như `lease_publish_test`, `ci_dang_ky_test`, `packet-loop selftest`) không còn được chạy tự động trên Windows sau mỗi commit vào master.
- **Cổng Windows đang đỏ biến mất khỏi CI không phải vì được chữa:** Tại thời điểm land (commit `a612c70`, run `35232106589`, job `105238582317`), lane `gate (windows-latest)` trên `master` đang đỏ sẵn 15 ca ở bước 18 `lease-publish selftest` (`133/148 đạt`, do `shutil.which("git", path="/usr/bin:/bin")` hardcode tại `ops/lease_publish.py:1106`, nợ WP541). Việc bỏ Windows khỏi `master` làm tín hiệu đỏ này biến mất khỏi CI, nhưng ADR-0049 **KHÔNG** chữa nợ WP541. Nợ WP541 vẫn còn nguyên và được xử lý ở packet riêng.
- **Độ phủ Windows tự động về 0 trên thực tế cho `ops/`, `scripts/`, `.github/`:**
  - `ci.yml` dùng trigger `pull_request` mặc định (không khai `types: [labeled]`), nên gắn nhãn `windows` lên PR đang đứng yên không tự kích hoạt run mới mà chỉ ăn ở lần push kế tiếp (`synchronize`) hoặc khi tạo PR đã có nhãn.
  - Dưới chính sách `manual_ci_budget: 0` (cấm `workflow_dispatch`), Windows tự động không còn chạy cho `ops/**`, `scripts/**`, `.github/**` (WP541 là bằng chứng sống).
  - 8 cổng tại chỗ của `deploy-package.*` là script chạy tay và **không bao gồm** `lease_publish_test` hay các test của `ops/`, nên không thay thế được toàn bộ lane CI bị gỡ.
  - Đây là **rủi ro đã nhận** (K4), được chấp nhận để bảo toàn hạn mức CI. Người điều phối và người phát hành chịu trách nhiệm khi thay đổi chạm mã phụ thuộc nền tảng. Nợ có tên `BATTERY-DEPLOY-HEP-HON-LANE-CI` ghi nhận việc mở rộng danh mục kiểm thử của script deploy khi cần thiết.

## 4. Lời khai trung thực về Windows CI khi land

Tuyên bố *"land không còn chạy Windows"* là **KHÔNG đúng tuyệt đối**:
- Workflow `.github/workflows/launcher-windows.yml` (với `paths: .claude/dev/**`) vẫn được giữ nguyên. Mọi thay đổi chạm `.claude/dev/**` khi push vào `master` vẫn kích hoạt và tiêu tốn ~5 phút Windows (Đ6, run `35125176975`).
