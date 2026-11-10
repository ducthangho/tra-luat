# Đánh giá tại chỗ sau R6 — không phải review độc lập

## Điều đã đo

R4 timeout trước handshake và driver đóng browser sau30s. R5 các tệp chính có mặt, phiên không thuộc session0, không có event khớp trong cửa sổ đọc; không chứng minh policy vắng mặt. R6 mới: openCLIrc0 và sessionnonce khớp sau khoảng31s tổng lệnh, kết quả trỏ tới empty snapshotfile trong ownedscratch. Đây không phải bằng chứng finalURL/source/capture/fullflow. Probe5/15/25s chưa thấy chrome.dll nhưng đã thấy chrome_elf; hai tiến trình có uvh64.dll. Sau mốc probe cuối, census có thêm tiến trình: không được gọi chrome.dll vắng mặt suốt lượt chạy.

WCT chỉ trả thread nodes/statusRunning hoặc Blocked, không có cạnh lock đủ để định danh điểm nghẽn. Cấu trúc ctypes WN280 khớp layout đã selfcheck; WaitTime là trường API ghi nguyên giá trị, tài liệu không chốt đơn vị trong phần mô tả, không suy thời lượng từ nhãn wait_ms trong helper. Nguồn API: https://learn.microsoft.com/en-us/windows/win32/api/wct/ns-wct-waitchain_node_info . Module presence không chứng minh injection gây lỗi. Chưa nối hash/path của module đang nạp với tệp cài đặt trước khi PID thoát; không kết luận UltraViewer gây treo. Changelog vendor đã đọc https://www.ultraviewer.net/changelogs.html không cung cấp fix Chromium cụ thể để chọn bản thay; không version hunting.

RAM trống giảm từ khoảng1GiB xuống164MB trong R6, trong khi commitfree vẫn~6GB. Không có proof OOM; khác biệt R4/R6 có thể do nhiều biến chưa kiểm soát. Đọc saucleanup khoảng1.28GiBfree. Mốc2GiB chỉ là đề xuất điều kiện vận hành thận trọng cho kế hoạch tương lai, KHÔNG thêm hoặc đổi acceptance gốc và KHÔNG là bằng chứng nguyên nhân.

## Lỗi điều phối cần chặn ở helper kế nhiệm

OP-R6-LOCK-01 (operational, formaloccurrences0): finally nhả testlock dù census còn3browser, sau close timeout. Không được sửa lại history; lỗi này nằm ở helper đo ngoài sản phẩm, không phải H2 SKILL. Cleanup hồi phục sau đó close0/delete-data0, ownedChrome0/lockempty; lệnh Stop-Process có fence nhưng không PID nào khớp/sống nên KHÔNG thực thi termination. Helper kế nhiệm phải hoàn tất cleanup/verification trước khi nhả khóa, hoặc handoff paused với hạn/ownership rõ; giữ lỗi gốc thay vì báo CLEANUP OK từ processrc đơn lẻ.

## Đường tiếp nối có thể thực thi sau khi đủ điều kiện

1. Khôi phục đăng nhập Codex CLI theo tài khoản đã cấp. Lượt advisory dbbd85a4108448ce8f793b3ff72de4f1 rc1 trước modelgeneration; logged-in status không chứng minh refresh hoạt động. Giữ đúng gói5tệp đã được user cho gửi; không đọc thêm repo/native raw. Fresh invocation/nonce/deadline phải ghi, không hồi sinh run cũ. Shared2/8/designadvisory0/1/formal0/2/author3/3/productpush0/1 giữ nguyên.
2. Sau advisory, chọn đúng một kiểm tra có giá trị phân biệt. Không tự mở lại giống R4/R6 chỉ vì một lần open0. Nếu chọn fullflow acceptance, phải freeze scope riêng, H2 source-byte bridge, cùng pins/timeouts/target, fresh ownedfixture/session, candidate npmci+signatures/redirect/sourcebytes/PNG/PDF/cleanup theo r3. Điểm guard tài nguyên/idle phải nêu trước, không forceclose ứng dụng khác, thay policy/timeout/sandbox/antivirus hay đổi VM thayDesktop. Phải giữ cả lỗi cũ và ra thất bại nếu bất kỳ proof nào thiếu.
3. Native fullflow chưa đạt; fullsource audit R6 raw chưa chạy; formalreview H2 chưa chạy và sensitive assurance vẫnHOLD. P3#1297 chưa canary; P4#1298 chỉ source/design, activation gatedU4/U5/U7/U8/U12; P5#1299 chưa rollout; P6#1300 chưa finalacceptance. Không merge/land/completeMission bằng kết quả diagnostic.

Mọi kết luận ở đây là operator assessment từ dữ liệu đã có. Không gọi thành independent advisory, không tự approve sản phẩm, không tăng cap do thay revision hoặc session.
