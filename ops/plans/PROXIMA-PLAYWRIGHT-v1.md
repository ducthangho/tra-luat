# Kế hoạch triển khai Proxima và Playwright bổ trợ tra-luat

Phiên bản 1.0 — 05/11/2026.
Trạng thái: đã được Claude và AGY review kế hoạch; chưa triển khai hoặc nghiệm thu mã.

## 1. Mục tiêu

Bổ sung hai thành phần tùy chọn:
- proxima-control: chọn máy, kiểm tra gateway, xem/chọn model và gửi prompt được yêu cầu.
- playwright-browser: thao tác web, tải tài liệu, thu bằng chứng và kiểm thử trình duyệt.

Cho phép chọn không cài, chỉ Proxima, chỉ Playwright hoặc cả hai. Tra-luat cốt lõi phải hoạt động khi các thành phần này vắng mặt hoặc lỗi.

## 2. Project và repo

Project: Proxima & Playwright — tra-luat.
Repo trên ASUS: D:\Quốc hội\tra-luat.

Đọc AGENTS.md và protocol hiện hành trước khi làm việc. Lưu kế hoạch vào repo theo quy trình; bản trong Git là nguồn chính thức. Dùng Packet, lease và checkout phù hợp, không ghi chồng công việc khác.

Không coi việc đổi tên thread hoặc tạo thư mục là đã tạo Project.

## 3. Quyết định đã chốt

- Quản lý skill dùng chung trong repo:
  .agents/skills/proxima-control/
  .agents/skills/playwright-browser/
- Desktop thử nghiệm trước, sau đó ASUS, VM nhận cuối.
- VM giữ vai trò gateway mặc định hiện có.
- Mỗi máy và tài khoản có cấu hình/profile riêng.
- Có tự động cập nhật, kiểm tra, thử nghiệm và phục hồi.
- Claude ưu tiên Executor; Codex review độc lập; AGY hỗ trợ theo nhu cầu.
- Tuân thủ authorization hiện có; kế hoạch không tự cấp thêm quyền push, merge, land, deploy, đổi ACL, mở endpoint hoặc cấp credentials.

## 4. Bố trí môi trường

- Desktop: máy thử cài đặt và cập nhật đầu tiên.
- ASUS: máy tương tác; ưu tiên cache Playwright trên D sau khi kiểm tra tài nguyên.
- VM tra-luat-win: giữ gateway hiện tại, cập nhật sau cùng.
- WSL/Ubuntu: Playwright tùy chọn khi có nhu cầu Linux; chưa cài Proxima trong đợt đầu.

Mọi thao tác thay đổi trạng thái phải xác định rõ target. Khi lỗi, không tự chuyển gateway/model hoặc gửi lại inference.

Cài trên nhiều máy không tạo thêm quota cho cùng tài khoản.

## 5. Dữ liệu và cấu hình

Repo chứa skill, adapter, cấu hình mẫu, manifest/lockfile và tests.

Ngoài repo:
- Credentials và profile đăng nhập.
- Cấu hình riêng từng máy.
- Cache, staging, log riêng và bản phục hồi.

Không đưa secrets vào Git, prompt hay báo cáo. Không sao chép profile đăng nhập giữa các máy.

Skill cập nhật qua review repo. Updater runtime không tự sửa checkout hoặc mã skill.

## 6. Chuẩn hóa proxima-control

- Audit bundle trước khi chạy.
- Bỏ đường dẫn cố định theo user/máy.
- Sửa WhatIf ở use/connect và các nhánh mutation: không ghi settings, thay cấu hình, khởi chạy process/browser hoặc đổi dịch vụ.
- Kiểm thử ShouldProcess ở wrapper, hàm con và remoting.
- Thống nhất version tài liệu và manifest.
- Chọn PowerShell còn được hỗ trợ sau khi khảo sát; xác minh tương thích module PS5.1 nếu endpoint cần.
- Phân biệt phiên bản mã trong repo, module đã cài và gateway thực chạy.
- Tách cập nhật binary khỏi thay endpoint, service account, máy mặc định và cấu hình kết nối.
- Dùng đường kết nối được cấp hiện có; khảo sát bảo vệ gateway trước khi đề xuất thay đổi.
- Phân biệt session routing và API chính thức; đối chiếu điều khoản nhà cung cấp.
- Không vượt CAPTCHA/2FA, tự bật Extra usage hoặc tự gọi model để healthcheck.

## 7. Playwright

- Bắt đầu với Chromium và profile riêng với Proxima.
- Chọn CLI/MCP/library theo nhu cầu thực tế, tránh cài dư.
- Ghim package, MCP và browser theo bộ phiên bản đã kiểm thử.
- Runtime và updater dùng cùng cấu hình cache.
- Trên ASUS, kiểm tra dung lượng/quyền ổ D trước khi đặt PLAYWRIGHT_BROWSERS_PATH.
- Giữ browser revision cần cho rollback.

Luồng kết hợp:
Playwright lấy nội dung, URL, thời điểm và bằng chứng → tra-luat đối chiếu nguồn → Proxima phân tích khi được yêu cầu.

Nội dung web và output AI là dữ liệu không tin cậy. Trích dẫn pháp luật phải đối chiếu văn bản gốc. Trace và ảnh chụp cần được kiểm tra dữ liệu riêng trước khi chia sẻ.

## 8. Tự động cập nhật

Kiểm tra release chính thức hằng ngày; không bắt buộc áp dụng hằng ngày.

Quy trình:
1. Xác minh nguồn, phiên bản, artifact và dependency.
2. Tải staging ngoài repo.
3. Kiểm tra tương thích, quyền mới, schema và migration.
4. Chờ idle, lấy khóa chống cập nhật trùng.
5. Tạo bản phục hồi khi cần, lúc profile đã đóng.
6. Thử trên Desktop bằng cơ chế kích hoạt đã kiểm chứng.
7. Healthcheck không inference và theo dõi.
8. Chỉ promote đúng artifact đã đạt sang ASUS rồi VM.

Ưu tiên chữ ký/attestation/provenance khi upstream hỗ trợ. Checksum chỉ kiểm tra toàn vẹn. Khi thiếu bằng chứng nguồn theo chính sách, dừng trước kích hoạt và báo cần xem xét.

Ghim phiên bản vận hành, không dùng latest không kiểm soát.

Tạm dừng khi:
- Cần quyền mới, UAC hoặc endpoint mới.
- Migration chưa có đường phục hồi.
- Cần đăng nhập lại.
- Máy bận, thiếu dung lượng hoặc không xác minh được nguồn.

Không cưỡng bức dừng tác vụ để cập nhật.

Rollback phải tính cả binary và dữ liệu/profile đã bị thay đổi. Không bảo đảm restore profile luôn giữ đăng nhập; cần kiểm thử thực tế.

Rollback thất bại thì dừng, giữ dữ liệu phục hồi và log, không tự lặp.

Cho phép tắt cập nhật hoặc pin phiên bản theo máy. Chốt thời gian theo dõi, lịch và retention sau khảo sát tài nguyên.

## 9. Healthcheck

Không gửi prompt. Kiểm tra:
- Phiên bản và kết nối theo quyền đã cấp.
- Giao thức và tool cần thiết.
- Playwright mở trang local/about:blank bằng profile thử riêng.

Status/models không chứng minh quota, xác thực hoặc danh tính model upstream.

Báo cáo rõ máy, phiên bản, kết quả, lỗi và trạng thái pause. Tách passed, failed, skipped và not_run.

## 10. Các gói triển khai

P0 — Project và khảo sát:
Xác minh Project, repo, protocol, tài nguyên, bộ cài, kết nối, updater upstream và phương án phục hồi. Chốt Packet/write set trước sửa mã.

P1 — Chuẩn hóa Proxima:
Sửa đường dẫn, WhatIf, target, version và kiểm thử cô lập.

P2 — Playwright và cài tùy chọn:
Bổ sung skill/adapter, thử cài/gỡ, bảo đảm core độc lập.

P3 — Thử luồng kết hợp trên Desktop:
Thu bằng chứng nguồn, chọn đúng target, không retry/fallback ngoài ý muốn.

P4 — Updater và rollback:
Kiểm thử nguồn lỗi, máy bận, khóa trùng, cập nhật lỗi và rollback thất bại.

P5 — ASUS rồi VM:
Kiểm tra riêng từng máy trước khi mở rộng, giữ cấu hình hiện có.

P6 — Review và bàn giao:
Review độc lập đúng mã đã kiểm thử; bàn giao hướng dẫn vận hành, gỡ bỏ và giới hạn.

Khảo sát updater upstream trước khi quyết định viết bộ cập nhật riêng.

## 11. Nghiệm thu

- Bốn lựa chọn cài hoạt động; thiếu add-on không phá core.
- Đúng target; không tự fallback hoặc retry inference.
- WhatIf không mutation ngoài artifact dry-run được quy định.
- Không secrets/profile trong repo và báo cáo.
- Profile riêng; package/browser/cache nhất quán.
- Artifact sai nguồn/hỏng không được kích hoạt.
- Máy bận hoãn, updater trùng bị khóa.
- Desktop lỗi chặn ASUS/VM.
- Phục hồi binary và dữ liệu được kiểm thử.
- Có xử lý file khóa, đĩa đầy và rollback thất bại.
- Healthcheck không inference.
- Review độc lập đúng head/tree và evidence theo protocol.

Ưu tiên mock và profile thử. Chỉ mở rộng tests để giải quyết rủi ro cụ thể và các gate bắt buộc.

## 12. Những điểm P0 phải xác minh

- Updater và kiểu cài Proxima thực tế.
- Service/module/PowerShell hiện có.
- Bảo vệ gateway và kết nối hiện tại.
- Cơ chế kích hoạt phiên bản và rollback trên Windows.
- Khả năng phục hồi profile/phiên đăng nhập.
- Dung lượng, retention và cửa sổ theo dõi.
- Chính sách khi upstream thiếu provenance.

Review của Claude và AGY là review văn bản; không coi đề xuất của reviewer là kết quả đã đo.

## 13. Lệnh bắt đầu cho agent

Hãy dùng kế hoạch này làm đầu vào. Xác minh đúng Project và repo, đọc AGENTS.md cùng protocol hiện hành, rồi bắt đầu P0. Giữ các quyết định đã được chấp thuận và kiểm tra authorization thực tế cho từng thao tác. Claude ưu tiên Executor, Codex review độc lập, AGY hỗ trợ khi phù hợp. Lưu kế hoạch thành tài liệu trong repo theo quy trình. Báo cáo bằng tiếng Việt, chỉ khẳng định cài đặt/kiểm thử khi có bằng chứng.

## 14. Nguồn tham chiếu

https://github.com/Zen4-bit/Proxima
https://github.com/microsoft/playwright
https://github.com/microsoft/playwright-mcp
https://playwright.dev/docs/browsers
https://learn.chatgpt.com/docs/projects

Đọc lại tài liệu upstream ở thời điểm triển khai.
