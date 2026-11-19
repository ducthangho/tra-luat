Bạn là reviewer ĐỘC LẬP (họ OpenAI), lượt 12 — LƯỢT XÁC NHẬN DELTA DUY NHẤT (chủ kho cấp đúng một lời gọi, §9 Q8) — cho đặc tả `ops/specs/WP1174-WINDOWS-BACKEND-r4.md` (Issue #1342, bậc r1d-a1-i). CHỈ ĐỌC; không ghi tệp trong thư mục làm việc; không gọi mạng. Chạy thử trong RAM hoặc bản sao dưới /tmp.

Clone master e2c3b82 (cộng chưa commit): bản 11 đã approve ở lượt 11 tại `ops/specs/WP1174-WINDOWS-BACKEND-r4-ban11.md` (sha256 2fcb8e60…); bản mới là `ops/specs/WP1174-WINDOWS-BACKEND-r4.md`; mã head của PR thi công (#1407, `728eccab`) cho phần test ở `ops/reviews/wp1342-spec-r4/head_packet_loop_test.py` (chỉ để đối chiếu các lời gọi kiểm signaled, không review mã); tóm tắt đo native ở `ops/reviews/wp1342-spec-r4/TOM-TAT-native.txt`.

Bối cảnh (§0, §9 Q7): đo native trên Desktop cho J3/J9 đỏ 10/10 trên bản sạch vì `WaitForSingleObject(h, 0)` ngay khi hàm trả = 258, chờ thêm = 0 sau < 50 µs; chủ kho quyết (1) chờ signaled có hạn 5 s ở mọi phép kiểm "đã signaled" sau khi hàm trả/ném, không đổi bảo đảm/mã sản phẩm, chỉnh dấu hiệu a1/k2; (2) đối chứng cho b và abi đổi sang J11 + S1; (3) ghi §0/§11.

Phạm vi CHỈ là:
1. `diff` bản 11 → bản mới: liệt kê mọi thay đổi; xác nhận chỉ chạm các điểm (1)(2)(3) và §9 Q7/Q8, §11, ghi chú numstat ở §8.
2. (1) đúng và đủ: mọi chỗ trong đặc tả kiểm "đã signaled" sau khi hàm trả/ném đều chuyển sang chờ ≤ 5 s (so với các lời gọi `_wp1342a1_tin` trong mã head: J2, J3, J8, J9); phép kiểm "CHƯA signaled" (J10b, kiểm trước cú giết) không bị đổi sai; bảo đảm sản phẩm (job rỗng khi hàm trả) giữ nguyên; dấu hiệu a1 (J3 "job not empty") và k2 (J9 phụ chưa signaled trong 5 s VÀ thiếu `cleanup:xac_nhan`) vẫn phân biệt được và vẫn đỏ đúng nhãn với chờ 5 s (phụ chờ `tha_phu` 300 s; cháu J3 chờ `tha_j3` 300 s); chờ 5 s không che đột biến nào khác (k1 ở J8: con treo vô hạn).
3. (2) hợp lý: J11 và S1 thật sự không đi qua `_1174_win_spawn_job` hay `THREADENTRY32`, nên không bị b/abi làm hỏng; đối chứng ấy vẫn chứng minh giàn/môi trường khoẻ cho ý nghĩa N7.
4. Không hồi quy ở phần không đổi.

Đầu ra stdout: danh sách thay đổi của diff, đánh giá từng điểm (1)(2)(3), finding nếu có (P0–P3). Dòng CUỐI CÙNG đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`. Chỉ approve khi không còn P0–P2.
