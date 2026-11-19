# Review độc lập ĐẶC TẢ — packet #1342 WP1174-WINDOWS-BACKEND r5 (bậc r1d-a1-ii), lượt 2

Bạn là reviewer độc lập, CHỈ ĐỌC; không sửa tệp, không commit, không gọi mạng.

- Cây làm việc = worktree tách rời của `origin/master` `4eda94e9effc6cfe7fcc0b3e3fb4151ad437ecbd` (base mới của đặc tả). Tệp chưa commit: `ops/specs/WP1174-WINDOWS-BACKEND-r5.md` (bản 2, sha256 791673a89b7861b338a07ff45f7e0f51fed696406cb0b00b2541f415abe344a9), `ops/specs/WP1174-WINDOWS-BACKEND-r5-ban1.md` (bản bạn review lượt 1), `ops/specs/r5-luot1.verdict.txt` (verdict lượt 1 của bạn: 1 P1, 4 P2, 1 P3).
- Nguồn như lượt 1: r4 trên `origin/ops/wp1342-r4-spec`, hồ sơ land `ops/land/pr1407-wp1342-*`, driver r4 `ops/land/pr1407-wp1342-provenance/windows-native/desktop/dot_bien_r4_ban2.py`, công cụ ngoài kho ở `/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/spec1342a1ii` (`n2_test_r5.py`, `n2_r5_extra.py`, `base_r5.py`).

## Việc (đo bằng lệnh, ghi lệnh + rc; không đo được ghi `not_run`)

1. Với TỪNG finding lượt 1: đóng thật hay chưa (`diff -u` hai bản để thấy delta). Trọng tâm: J4 đối chứng (ii) nay gọi CHÍNH `_1174_win_spawn_job` của một bản nạp module riêng (`_module1174(c)`, xem dòng ~10647 tệp test) với `_1174_WIN_JOB_LIMIT = 0x2800` — có thật sự cùng chuỗi job tổ tiên, cùng lệnh, cùng cách quan sát với đường đo không; có cách nào bản nạp riêng rò sang đường đo (vd e1 trên bản sao sản phẩm mà đối chứng/đường đo nạp khác tệp) không.
2. Delta mới có tạo lỗ mới không (hạn chung 75 s và dự phòng; kiểm `WAIT_TIMEOUT` thô; trình tự dữ liệu J12; điều kiện đủ của e1c; a1@J12 chỉ chấm ở nhánh B).
3. Kiểm lại nhanh các phần không đổi chỉ khi delta chạm tới chúng. Đối chiếu `git diff --stat 11bd033 4eda94e` và blob hai tệp write set trên `4eda94e`.

Nếu một hướng thử cần nội dung dạng đường dẫn thoát khỏi cây thư mục, MÔ TẢ BẰNG LỜI.

## Đầu ra

Tiếng Việt. Bảng trạng thái finding lượt 1; finding mới mức P0–P3 kèm bằng chứng và câu thay thế. DÒNG CUỐI CÙNG đúng một trong hai:
KET_LUAN: approve
KET_LUAN: request_changes
