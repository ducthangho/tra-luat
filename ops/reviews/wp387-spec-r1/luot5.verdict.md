## Finding lượt 4

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| P2 · Dọn cháu có hai khe tái cấp PID | **Chưa đóng** | M4 đã bỏ gửi tín hiệu trong fixture thường. M6 vẫn yêu cầu bộ ghi chuyển tiếp `os.kill` thật với PID đọc từ tệp sau dấu `chau-xong`. `except OSError` chỉ xử lý lỗi gọi hàm. Nếu PID đã được cấp lại và lệnh thành công, tín hiệu tới tiến trình khác. N5 buộc chạy đột biến này ở cả A và B. [Đặc tả M4–M6](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L135) |
| P2 · N5 L2 cách B có bằng chứng yếu hơn A | **Đóng** | Hai cách dùng cùng runner, cùng đối chứng neutral, cùng phân loại `TinHieuChotCa`, cùng yêu cầu `OK giet 1/1` đúng ca đích và tổng kết `N/N dat`. B chỉ lọc `DOT_BIEN`, giữ nguyên hai bảng còn lại. Tôi đọc `DOT_BIEN` từ `git archive` bằng `ast.literal_eval`, rc 0, thu được 550 mục trên base. [N5](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L149) |
| P3 · Ca (e) không giết biến thể ngủ theo mốc cũ | **Đóng** | Mô phỏng (e4) bằng `python3 -B -`, rc 0. M2 cho `False, [0.03]`, còn `r387_ngu_khong_tru_lan_do` cho `False, [0.1]`. Vế danh sách thời lượng ngủ đổi màu dù kết quả boolean giống nhau. [Đặc tả M4–M6](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L135) |

## Finding mới

- **P2 · Đường ca đỏ có thể kết thúc cháu qua Job Object và bỏ lại tệp fixture.** M4 đặt `_r387_cho_cay_rong` sau các khẳng định, còn §8 giữ handle tới khi tiến trình test thoát. `_job_windows` đặt `KILL_ON_JOB_CLOSE`, nên một lượt `--lap-ca` hoặc runner đột biến thoát trước khi cháu tự thoát có thể kết thúc cháu khi Windows đóng handle cuối. Bộ ghi `os.kill`/`os.killpg` không quan sát được đường này. Trong runner nhiều ca, `San.__exit__` gọi `rmtree(..., ignore_errors=True)` trước khi cháu nhả `stdout.log`. Trên Windows, tệp còn mở có thể khiến thư mục tạm sót lại mà harness không báo. Chưa có bằng chứng cháu làm ca sau đỏ oan. Trên POSIX, phép dò nhóm chỉ đọc và fixture thường không có đường gửi tín hiệu mới. Đặt bước chờ vào teardown, trước khi dọn thư mục, áp dụng cả khi ca đỏ và giữ lỗi gốc. Quy định rõ ai đóng handle đúng một lần sau khi job rỗng, cùng cách báo lỗi nếu hết hạn hoặc không đo được. [M4](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L135) · [§8](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L191) · [Cờ job](.claude/dev/launcher.py#L925) · [Teardown của harness](.claude/dev/launcher_test.py#L177)

Với finding tái cấp PID, cho đột biến đi qua bộ ghi dùng hàm đích giả không gửi tín hiệu, rồi yêu cầu ca đỏ ở đúng vế nhật ký. Việc bọc `os.killpg` cần theo nền vì Windows không có API Python này.

Đối chiếu L1–L7, đơn vị đếm và ánh xạ write set nhất quán. L3 và L6 còn điểm cụ thể đã nêu ở trên về phản chứng harness. L4 ghi `khong_ap_dung`; §0 phân biệt mốc đo lịch sử với bản vá thử hiện tại theo L5; §6 không đặt ngân sách mềm và gắn E2 cho các điểm xin quyền theo L7. §9 dẫn nhầm vị trí bảy luật trong skill, thực tế ở §2.

Review độc lập qua Codex, dùng shell cục bộ và không gọi mạng. `HEAD` tách tại cùng OID với `master`, `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả đang xét là `633e7500c05fa60d8ad1e47bd4e5d72cc348e165389e17a746f6d5e53b10fb1b`. `mktemp -d /tmp/r387-review.XXXXXX` trả rc 1 vì hệ tệp chỉ đọc. `--lap-ca`, toàn suite và Windows native đều chưa chạy trong lượt này.

KET_LUAN: request_changes
tokens used
89,402
## Finding lượt 4

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| P2 · Dọn cháu có hai khe tái cấp PID | **Chưa đóng** | M4 đã bỏ gửi tín hiệu trong fixture thường. M6 vẫn yêu cầu bộ ghi chuyển tiếp `os.kill` thật với PID đọc từ tệp sau dấu `chau-xong`. `except OSError` chỉ xử lý lỗi gọi hàm. Nếu PID đã được cấp lại và lệnh thành công, tín hiệu tới tiến trình khác. N5 buộc chạy đột biến này ở cả A và B. [Đặc tả M4–M6](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L135) |
| P2 · N5 L2 cách B có bằng chứng yếu hơn A | **Đóng** | Hai cách dùng cùng runner, cùng đối chứng neutral, cùng phân loại `TinHieuChotCa`, cùng yêu cầu `OK giet 1/1` đúng ca đích và tổng kết `N/N dat`. B chỉ lọc `DOT_BIEN`, giữ nguyên hai bảng còn lại. Tôi đọc `DOT_BIEN` từ `git archive` bằng `ast.literal_eval`, rc 0, thu được 550 mục trên base. [N5](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L149) |
| P3 · Ca (e) không giết biến thể ngủ theo mốc cũ | **Đóng** | Mô phỏng (e4) bằng `python3 -B -`, rc 0. M2 cho `False, [0.03]`, còn `r387_ngu_khong_tru_lan_do` cho `False, [0.1]`. Vế danh sách thời lượng ngủ đổi màu dù kết quả boolean giống nhau. [Đặc tả M4–M6](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L135) |

## Finding mới

- **P2 · Đường ca đỏ có thể kết thúc cháu qua Job Object và bỏ lại tệp fixture.** M4 đặt `_r387_cho_cay_rong` sau các khẳng định, còn §8 giữ handle tới khi tiến trình test thoát. `_job_windows` đặt `KILL_ON_JOB_CLOSE`, nên một lượt `--lap-ca` hoặc runner đột biến thoát trước khi cháu tự thoát có thể kết thúc cháu khi Windows đóng handle cuối. Bộ ghi `os.kill`/`os.killpg` không quan sát được đường này. Trong runner nhiều ca, `San.__exit__` gọi `rmtree(..., ignore_errors=True)` trước khi cháu nhả `stdout.log`. Trên Windows, tệp còn mở có thể khiến thư mục tạm sót lại mà harness không báo. Chưa có bằng chứng cháu làm ca sau đỏ oan. Trên POSIX, phép dò nhóm chỉ đọc và fixture thường không có đường gửi tín hiệu mới. Đặt bước chờ vào teardown, trước khi dọn thư mục, áp dụng cả khi ca đỏ và giữ lỗi gốc. Quy định rõ ai đóng handle đúng một lần sau khi job rỗng, cùng cách báo lỗi nếu hết hạn hoặc không đo được. [M4](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L135) · [§8](ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md#L191) · [Cờ job](.claude/dev/launcher.py#L925) · [Teardown của harness](.claude/dev/launcher_test.py#L177)

Với finding tái cấp PID, cho đột biến đi qua bộ ghi dùng hàm đích giả không gửi tín hiệu, rồi yêu cầu ca đỏ ở đúng vế nhật ký. Việc bọc `os.killpg` cần theo nền vì Windows không có API Python này.

Đối chiếu L1–L7, đơn vị đếm và ánh xạ write set nhất quán. L3 và L6 còn điểm cụ thể đã nêu ở trên về phản chứng harness. L4 ghi `khong_ap_dung`; §0 phân biệt mốc đo lịch sử với bản vá thử hiện tại theo L5; §6 không đặt ngân sách mềm và gắn E2 cho các điểm xin quyền theo L7. §9 dẫn nhầm vị trí bảy luật trong skill, thực tế ở §2.

Review độc lập qua Codex, dùng shell cục bộ và không gọi mạng. `HEAD` tách tại cùng OID với `master`, `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. SHA-256 đặc tả đang xét là `633e7500c05fa60d8ad1e47bd4e5d72cc348e165389e17a746f6d5e53b10fb1b`. `mktemp -d /tmp/r387-review.XXXXXX` trả rc 1 vì hệ tệp chỉ đọc. `--lap-ca`, toàn suite và Windows native đều chưa chạy trong lượt này.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:37:17Z
