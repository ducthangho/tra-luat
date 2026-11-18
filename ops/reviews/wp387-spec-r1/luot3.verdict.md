# Review độc lập lượt 3 · Issue #387

Bản review có SHA-256 `7611a4a022b1660843cf1a8836a7533b063e9e63364c978bff9701681deb1ea7`. Đã đối chiếu bằng `diff -u` với bản lượt 2 và đọc mã tại HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout đang ở detached HEAD, trùng `origin/master` cục bộ. Phiên OpenAI dùng `openai_codex / codex_cli / machine` trên Linux, Python 3.13.18.

## Finding lượt 2

| Mức | Finding | Trạng thái | Đối chiếu |
|---|---|---|---|
| P1 | Con Windows có thể thoát trước lúc gán job | **Đóng ở đặc tả** | M4 buộc mọi con trong fixture chung đợi `job-da-gan`. `_job_windows` chỉ trả handle sau khi `AssignProcessToJobObject` thành công. Ca có cháu còn phải thấy PID trong danh sách của đúng job. Windows native vẫn chờ N5. |
| P2 | `[]` sau deadline thành `true`, đột biến `timeout=15` có thể sống | **Đóng** | M2 xét `None` → quá hạn → `[]`. Ca (e2) trả `[]` muộn. Ca (e3) gọi `_thanh_vien_nhom` thật và kiểm `timeout` đi đến `subprocess.run`, nên bắt được việc khôi phục hằng `15` ngay trong lời gọi `ps`. |
| P2 | Ctrl-C ghi đè `ma_that` hoặc che `kq_chup` | **Đóng** | Vị trí xét cờ sau dòng 2978 giữ thứ tự ưu tiên của `stop`, trạng thái kết thúc và kết quả chụp. Nhánh mới chỉ đổi `ma` khi trạng thái còn `xong`. Ca (h1) kiểm rc 130 và `ma_thoat == 0`, ca (h2) kiểm giữ `ghi_workspace`. |
| P2 | Hai cách chạy Windows native đòi bằng chứng khác nhau | **Chưa đóng hết** | L1 và L2 đã dùng chung danh sách. L3 vẫn đòi kết quả quan sát của mutant `nhom_luon_rong` ở cách A, còn cách B chỉ áp M6 rồi yêu cầu “ghi theo dự kiến”. |
| P3 | Mốc giờ `xZ`, mốc 400 và số đột biến | **Đóng** | Mốc giờ thiếu độ chính xác đã được chú thích. §6 gọi 400 là mốc rà dự toán. M6, N4 và §8 nhất quán về 15 đột biến mới, 14 mục đo trên Linux và 5 mục chuyển sang B nếu tách. |

## Finding lượt 3

- **P2 — M4 yêu cầu dọn fixture bằng PID trần.** Tệp PID vẫn tồn tại sau khi cháu đã thoát, kể cả ở đường chạy xanh của (a), (a′) và (c). `finally` vẫn gọi `os.kill(pid, signal.SIGTERM)`. Nếu hệ điều hành đã cấp lại PID, fixture có thể kết thúc tiến trình khác trên máy chủ kho. Dùng handle của chính tiến trình hoặc kiểm khóa danh tính trước khi gửi tín hiệu. [M4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md:121)
- **P2 — L3 cần cùng một quy tắc bằng chứng cho cả hai đường native.** Giữ `xoa_prompt_khi_wrapper_vua_thoat` ở diện miễn đo trên Windows vì `t76` tự skip. Với `nhom_luon_rong`, hoặc yêu cầu cách B áp riêng neo M5 và ghi kết quả quan sát của `t67`, hoặc đặt kết quả Windows của neo này là tùy chọn cho cả hai cách. N4 đã yêu cầu bằng chứng giết cả hai neo trên Linux. [N5](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md:135)
- **P3 — M2 cần quy định cách tính thời gian ngủ sau lần dò.** Lấy phần còn lại từ mốc monotonic sau lần dò. Nếu danh sách còn thành viên và phần còn lại `<= 0` thì trả `False`. Dùng lại `con_lai` trước lần dò có thể ngủ quá hạn. Thứ tự `None` → `> het` → `[]` vẫn nhất quán với việc chấp nhận `[]` đúng tại mốc hạn. [M2](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md:119)

Không có finding P0 hoặc P1 mới.

## Neo, ngân sách và nghiệm thu

- **t117.** Đọc hai tệp nguồn từ `git archive HEAD` trong bộ nhớ và áp đúng quy tắc `str.count` của t117. Phép kiểm rc 0, đủ 550 mục base, không lệch số chỗ khớp: 538 chung, 7 POSIX, 5 Windows. Ngoại lệ `hook_phien_bo_phep_so_nang_luc` khớp đúng hai chỗ. Chuỗi trần `timeout=15` khớp **bốn** chỗ, nên mẫu mới phải lấy ngữ cảnh của lời gọi `ps` trong `_thanh_vien_nhom`. Mười lăm mẫu mới và hai neo sửa chỉ có thể xác nhận số khớp trên head triển khai.
- **§8.** Vá thử được báo là +314 dòng. Dự toán 320–440 dành thêm 6–126 dòng cho bản triển khai và còn 10 dòng ở đầu trên so với trần 450. Hai OID ADR trong spec khớp lịch sử first-parent của ref cục bộ. Nếu phải tách, A và B cần revision và gate riêng vì cùng sửa `launcher_test.py`. A nên giữ ca (e) và (g) cùng các đột biến tương ứng nếu A đưa toàn bộ hành vi Darwin/Windows vào sử dụng. Phương án §8 hiện chuyển các phép đo trực tiếp của deadline và giữ prompt sang B.
- **L1–L7.** L1 có 11 ca native và yêu cầu từng ca có bằng chứng chạy. L2 yêu cầu 15 mục chết đúng ca đích. L3 còn chênh bằng chứng như trên. Blob được giao kết thúc ở §8, chỉ có nhãn L1–L3. §9 và L4–L7 chưa có nội dung để rà.
- **Chạy thử.** `mktemp -d /tmp/r387-review.XXXXXX` trả rc 1 do filesystem chỉ đọc. Phép đếm neo trong bộ nhớ đã chạy. `--lap-ca`, toàn bộ `launcher_test.py` và Windows native đều `not_run` trong phiên này.

KET_LUAN: request_changes
tokens used
67,514
# Review độc lập lượt 3 · Issue #387

Bản review có SHA-256 `7611a4a022b1660843cf1a8836a7533b063e9e63364c978bff9701681deb1ea7`. Đã đối chiếu bằng `diff -u` với bản lượt 2 và đọc mã tại HEAD `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout đang ở detached HEAD, trùng `origin/master` cục bộ. Phiên OpenAI dùng `openai_codex / codex_cli / machine` trên Linux, Python 3.13.18.

## Finding lượt 2

| Mức | Finding | Trạng thái | Đối chiếu |
|---|---|---|---|
| P1 | Con Windows có thể thoát trước lúc gán job | **Đóng ở đặc tả** | M4 buộc mọi con trong fixture chung đợi `job-da-gan`. `_job_windows` chỉ trả handle sau khi `AssignProcessToJobObject` thành công. Ca có cháu còn phải thấy PID trong danh sách của đúng job. Windows native vẫn chờ N5. |
| P2 | `[]` sau deadline thành `true`, đột biến `timeout=15` có thể sống | **Đóng** | M2 xét `None` → quá hạn → `[]`. Ca (e2) trả `[]` muộn. Ca (e3) gọi `_thanh_vien_nhom` thật và kiểm `timeout` đi đến `subprocess.run`, nên bắt được việc khôi phục hằng `15` ngay trong lời gọi `ps`. |
| P2 | Ctrl-C ghi đè `ma_that` hoặc che `kq_chup` | **Đóng** | Vị trí xét cờ sau dòng 2978 giữ thứ tự ưu tiên của `stop`, trạng thái kết thúc và kết quả chụp. Nhánh mới chỉ đổi `ma` khi trạng thái còn `xong`. Ca (h1) kiểm rc 130 và `ma_thoat == 0`, ca (h2) kiểm giữ `ghi_workspace`. |
| P2 | Hai cách chạy Windows native đòi bằng chứng khác nhau | **Chưa đóng hết** | L1 và L2 đã dùng chung danh sách. L3 vẫn đòi kết quả quan sát của mutant `nhom_luon_rong` ở cách A, còn cách B chỉ áp M6 rồi yêu cầu “ghi theo dự kiến”. |
| P3 | Mốc giờ `xZ`, mốc 400 và số đột biến | **Đóng** | Mốc giờ thiếu độ chính xác đã được chú thích. §6 gọi 400 là mốc rà dự toán. M6, N4 và §8 nhất quán về 15 đột biến mới, 14 mục đo trên Linux và 5 mục chuyển sang B nếu tách. |

## Finding lượt 3

- **P2 — M4 yêu cầu dọn fixture bằng PID trần.** Tệp PID vẫn tồn tại sau khi cháu đã thoát, kể cả ở đường chạy xanh của (a), (a′) và (c). `finally` vẫn gọi `os.kill(pid, signal.SIGTERM)`. Nếu hệ điều hành đã cấp lại PID, fixture có thể kết thúc tiến trình khác trên máy chủ kho. Dùng handle của chính tiến trình hoặc kiểm khóa danh tính trước khi gửi tín hiệu. [M4](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md:121)
- **P2 — L3 cần cùng một quy tắc bằng chứng cho cả hai đường native.** Giữ `xoa_prompt_khi_wrapper_vua_thoat` ở diện miễn đo trên Windows vì `t76` tự skip. Với `nhom_luon_rong`, hoặc yêu cầu cách B áp riêng neo M5 và ghi kết quả quan sát của `t67`, hoặc đặt kết quả Windows của neo này là tùy chọn cho cả hai cách. N4 đã yêu cầu bằng chứng giết cả hai neo trên Linux. [N5](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md:135)
- **P3 — M2 cần quy định cách tính thời gian ngủ sau lần dò.** Lấy phần còn lại từ mốc monotonic sau lần dò. Nếu danh sách còn thành viên và phần còn lại `<= 0` thì trả `False`. Dùng lại `con_lai` trước lần dò có thể ngủ quá hạn. Thứ tự `None` → `> het` → `[]` vẫn nhất quán với việc chấp nhận `[]` đúng tại mốc hạn. [M2](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP2/ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md:119)

Không có finding P0 hoặc P1 mới.

## Neo, ngân sách và nghiệm thu

- **t117.** Đọc hai tệp nguồn từ `git archive HEAD` trong bộ nhớ và áp đúng quy tắc `str.count` của t117. Phép kiểm rc 0, đủ 550 mục base, không lệch số chỗ khớp: 538 chung, 7 POSIX, 5 Windows. Ngoại lệ `hook_phien_bo_phep_so_nang_luc` khớp đúng hai chỗ. Chuỗi trần `timeout=15` khớp **bốn** chỗ, nên mẫu mới phải lấy ngữ cảnh của lời gọi `ps` trong `_thanh_vien_nhom`. Mười lăm mẫu mới và hai neo sửa chỉ có thể xác nhận số khớp trên head triển khai.
- **§8.** Vá thử được báo là +314 dòng. Dự toán 320–440 dành thêm 6–126 dòng cho bản triển khai và còn 10 dòng ở đầu trên so với trần 450. Hai OID ADR trong spec khớp lịch sử first-parent của ref cục bộ. Nếu phải tách, A và B cần revision và gate riêng vì cùng sửa `launcher_test.py`. A nên giữ ca (e) và (g) cùng các đột biến tương ứng nếu A đưa toàn bộ hành vi Darwin/Windows vào sử dụng. Phương án §8 hiện chuyển các phép đo trực tiếp của deadline và giữ prompt sang B.
- **L1–L7.** L1 có 11 ca native và yêu cầu từng ca có bằng chứng chạy. L2 yêu cầu 15 mục chết đúng ca đích. L3 còn chênh bằng chứng như trên. Blob được giao kết thúc ở §8, chỉ có nhãn L1–L3. §9 và L4–L7 chưa có nội dung để rà.
- **Chạy thử.** `mktemp -d /tmp/r387-review.XXXXXX` trả rc 1 do filesystem chỉ đọc. Phép đếm neo trong bộ nhớ đã chạy. `--lap-ca`, toàn bộ `launcher_test.py` và Windows native đều `not_run` trong phiên này.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T06:06:12Z
