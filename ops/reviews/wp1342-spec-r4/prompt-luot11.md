Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 11 — LƯỢT XÁC NHẬN CUỐI (chủ kho cấp thêm đúng một lời gọi, §9 Q6) — cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342, bậc r1d-a1-i). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit: đặc tả r1–r4, bản 10 đã review ở lượt 10 tại `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban10.md`, các verdict `ops/reviews/wp1342-spec-r4/luot1..10.verdict.txt`).

Ràng buộc đã chốt (§9 Q1–Q6, không tranh luận). Đây KHÔNG phải lượt tìm finding mới trên toàn đặc tả; phạm vi là:
1. `diff` bản 10 (`-ban10.md`) với bản hiện tại. Xác nhận diff CHỈ chạm N2 (§5) và §9 (Q6) / §11 (nhật ký). Nêu mọi dòng khác bị đổi.
2. Ba finding lượt 10 (`luot10.verdict.txt`: R10-1, R10-2, R10-3) đã ĐÓNG THẬT. CHẠY N2 trong RAM trên `packet_loop_test.py` của base theo đúng chữ N2 hiện tại: base xanh bốn vế; đối chứng dương (hai `def` mới có tiền tố `_wp1342a1_`, một gán tên mới có tiền tố, `CASES += [("wp1342_native_job_review", _native1342("wp1342_native_job_review", _wp1342a1_fn))]` đặt trong cửa sổ đăng ký) XANH; mọi phản chứng đã liệt kê ở N2 ĐỎ, kể cả phản chứng lệch ID `("wp1342_native_job_x", _native1342("wp1174_writer_accept", _wp1342a1_fn))` và đăng ký trùng `wp1174_writer_accept`; một `CASES += [...]` dạng list comprehension ĐỎ.
3. Rà nhanh hồi quy: các chốt đã đóng ở lượt 1–10 không bị bản này làm hở lại.

Đầu ra stdout: bảng ba finding R10 (đóng/chưa, kèm bằng chứng chạy), kết quả diff, kết quả N2 trong RAM, finding nếu có (P0–P3). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
