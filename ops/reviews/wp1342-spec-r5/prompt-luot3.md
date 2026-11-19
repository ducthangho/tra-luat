# Review độc lập ĐẶC TẢ — packet #1342 WP1174-WINDOWS-BACKEND r5 (bậc r1d-a1-ii), lượt 3

Bạn là reviewer độc lập, CHỈ ĐỌC; không sửa tệp, không commit, không gọi mạng.

- Cây làm việc = worktree tách rời của `origin/master` `4eda94e9effc6cfe7fcc0b3e3fb4151ad437ecbd` (base mới của đặc tả). Tệp chưa commit: `ops/specs/WP1174-WINDOWS-BACKEND-r5.md` (bản 3, sha256 bdc139edea905d0fec6a0b947b2b2e269501a7f23fcea74970080c81b02043e7), `ops/specs/WP1174-WINDOWS-BACKEND-r5-ban2.md` (bản bạn review lượt 2), `ops/specs/r5-luot2.verdict.txt` (verdict lượt 2 của bạn: F1 P1, F2–F4 P2, F5 P3); bản 1 + verdict lượt 1 vẫn ở `ops/specs/WP1174-WINDOWS-BACKEND-r5-ban1.md`, `ops/specs/r5-luot1.verdict.txt`.
- Nguồn như lượt 1: r4 trên `origin/ops/wp1342-r4-spec`, hồ sơ land `ops/land/pr1407-wp1342-*`, driver r4 `ops/land/pr1407-wp1342-provenance/windows-native/desktop/dot_bien_r4_ban2.py`, công cụ ngoài kho ở `/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/spec1342a1ii` (`n2_test_r5.py`, `n2_r5_extra.py`, `base_r5.py`).

## Việc (đo bằng lệnh, ghi lệnh + rc; không đo được ghi `not_run`)

1. Với TỪNG finding lượt 2 (F1–F5) và phần còn mở của lượt 1: đóng thật hay chưa (`diff -u` bản 2 với bản 3). Trọng tâm: J4 nạp bản đối chứng qua `_module1174(SimpleNamespace(script=...))`, argv cháu cố định, phân loại bảy vế; luật chờ thô và ngân sách 45 s; trình tự J12.
2. Delta mới có tạo lỗ mới không; có mâu thuẫn nội tại nào giữa M1–M4, §4b, N6–N7, §7 không.
3. Kiểm lại nhanh các phần không đổi chỉ khi delta chạm tới chúng. Đối chiếu `git diff --stat 11bd033 4eda94e` và blob hai tệp write set trên `4eda94e`.

Nếu một hướng thử cần nội dung dạng đường dẫn thoát khỏi cây thư mục, MÔ TẢ BẰNG LỜI.

## Đầu ra

Tiếng Việt. Bảng trạng thái finding lượt 2; finding mới mức P0–P3 kèm bằng chứng và câu thay thế. DÒNG CUỐI CÙNG đúng một trong hai:
KET_LUAN: approve
KET_LUAN: request_changes
