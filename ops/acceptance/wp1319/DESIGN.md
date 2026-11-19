# WP1319 — Bounded design cho phần nghiệm thu mở rộng (bản nháp, 2026-11-17)

Trạng thái: **nháp, chưa duyệt, chưa thi công**. Tài liệu này chỉ đề xuất ranh giới.
Nó không cấp lease, không cấp quyền tác động host, không đổi gateway/service/account/endpoint/ACL, không cấp LIVE.
Mỗi mục dưới đây phải có spec đóng băng (`ops/specs/…`, `spec_hash`), write set, budget, generation và lease
trước khi chạy. Không mục nào là yêu cầu hồi tố với các canary P3–P6 đã đóng.
Phân loại do owner quyết: (R) bắt buộc cho "nghiệm thu đủ" · (O) tùy chọn / mở rộng.

## Ràng buộc chung cho mọi mục
- Host: Desktop `a5f7076e` là máy thử mặc định (kế hoạch §3 và §4). ASUS chỉ chạy khi owner chỉ định lại. VM `f7281f27` **không** nhận thử nghiệm phá hủy vì đang giữ gateway mặc định và chỉ còn ~1,67 GB trống (đo 17/11).
- Không dùng/copy profile đăng nhập thật. Chỉ dùng **profile thử** tạo mới, tài khoản Windows riêng hoặc thư mục `--user-data-dir` riêng.
- Không tự đăng nhập hoặc 2FA. Bước nào cần đăng nhập thì dừng và ghi `cần_người`.
- Không gửi inference để healthcheck. Không retry hoặc fallback model/gateway.
- Lấy khóa `KHOA.txt` theo ADR-0057/0058 (có hạn và nhịp tim). Không xóa khóa của người khác. Máy bận thì hoãn.
- Mỗi lần chạy phải có: artifact chính thức + sha256 + nguồn (release URL, asset digest). Giữ bản phục hồi trước khi đổi. Giữ raw FAIL. Không tự lặp khi rollback thất bại.
- Tiêu chí dừng: thiếu dung lượng (< 2× kích thước bộ cài + dữ liệu), cần UAC hoặc quyền mới, nguồn không xác minh được.

## D1. NSIS thực (O hoặc R, owner quyết)
- Mục tiêu: chứng minh bộ cài NSIS chính thức của Proxima cài, gỡ và cài lại được trên **profile thử**, không chạm cài đặt hiện có.
- Artifact: bộ cài NSIS chính thức của đúng phiên bản đang ghim (5.5.0, asset digest đã ghi ở P6). Phải xác nhận lại digest trước khi chạy.
- Target: Desktop, tài khoản Windows thử (cài per-user) hoặc VM dùng một lần nếu owner cấp. **Không** chạy trên VM gateway.
- Đo: rc của installer · danh sách tệp và registry trước/sau (HKCU) · shortcut · uninstaller rc · tàn dư sau gỡ · cài đặt hiện có không đổi (hash).
- Rollback: gỡ bằng uninstaller, rồi xóa thư mục cài thử. Profile thật không bị đụng tới.
- PASS: cài, khởi động không inference (status), gỡ sạch, cài đặt gốc giữ nguyên byte.

## D2. Migration khác phiên bản (O)
- Cần **hai** artifact chính thức: phiên bản cũ N-1 và 5.5.0, cả hai có digest. Chưa có N-1 thì mục này `not_run` kèm lý do.
- Trên profile thử: cài N-1 → tạo dữ liệu thử (không đăng nhập) → nâng lên 5.5.0 theo cơ chế đã kiểm chứng (updater bị tắt hoặc ghim, U4) → đo schema/dữ liệu → rollback về N-1 bằng binary + dữ liệu đã sao lưu.
- PASS: dữ liệu thử còn đủ sau nâng cấp; rollback trả đúng byte của dữ liệu đã sao lưu.

## D3. Runtime promotion / LIVE (O, ngoài phạm vi mặc định)
- Không thực hiện trong #1319 nếu owner không cấp **riêng** quyền promotion. Câu "nghiệm thu đủ" không bao gồm quyền này.
- Thiết kế nếu được cấp: promotion fence Desktop (hoặc ASUS theo owner) → ASUS → VM. Trên mỗi máy kiểm: artifact đúng digest, healthcheck không inference, gateway/service/account/endpoint không đổi. Máy trước FAIL thì máy sau bị chặn.

## D4. U8 — restore profile/đăng nhập (R cho phần dữ liệu, O cho phần đăng nhập)
- Đã có (lời khai P4): restore binary + 7957 tệp khớp. Chưa có: bằng chứng **phiên** (cookie/token) còn dùng được sau restore.
- Thiết kế: profile thử có trạng thái không cần đăng nhập (cấu hình, lịch sử cục bộ) → sao lưu lúc đóng profile → làm hỏng có kiểm soát → restore → so hash tệp và trạng thái ứng dụng đọc được.
- Phần đăng nhập: **không hứa** giữ được. Chỉ thử khi owner tự đăng nhập profile thử. Nếu phiên mất sau restore thì đó là kết quả đúng phải ghi lại, không phải lỗi phải giấu.
- PASS (phần dữ liệu): restore trả đúng byte và ứng dụng mở lại được. Phần đăng nhập: chỉ ghi `quan_sat`.

## D5. Kiểm release hằng ngày (R nếu owner coi §8 là bắt buộc)
- Hiện trạng 17/11: không có scheduler trên Desktop/VM. ASUS chưa đo. Ngày 13/11 chỉ có lần kiểm chạy tay.
- Thiết kế: tác vụ **chỉ đọc** chạy 1 lần/ngày trên **một** máy (đề xuất Desktop). Tác vụ gọi API release chính thức, so phiên bản và digest với pin, ghi kết quả ra tệp log cục bộ. **Không tải, không cài, không apply.**
- Cài tác vụ nền là thay đổi host, nên cần lease riêng và owner duyệt. Gỡ bằng `Unregister-ScheduledTask`.
- PASS: chạy theo lịch ≥ 2 ngày liên tiếp, log đúng, không có mutation.

## Thứ tự đề xuất
1. Lấy gói raw và hoàn tất ma trận (không cần host).
2. Thiết kế D5 + D4 phần dữ liệu (rủi ro thấp, trên Desktop).
3. D1 khi owner chọn R.
4. D2/D3 chỉ khi owner cấp riêng.
