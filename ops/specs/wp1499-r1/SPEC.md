# Launcher ghi đúng định danh CLI Antigravity

Đặc tả r1 chờ review độc lập, chưa cấp lease. Kế thừa bằng chứng Mission #1172 r97 và tách khỏi hai lượt reviewer của B4/PR2. Base nguồn a2bdb480e8fb54c152af190378c434fa41b0feaf. Launcher trên base này có cùng SHA-256 với bản đã dùng để đo nguyên nhân. Phạm vi sensitive vì bảng Launcher cũng là nguồn cấu trúc cho bộ kiểm biên nhận.

## Mục tiêu

Khi Protocol Launcher gọi trực tiếp executable `agy`, sổ ghi `google_antigravity / antigravity / machine/local`. Giữ nguyên miền provider của biên nhận. Tên executable xác định route cục bộ, còn danh tính model/session cần bằng chứng từ lượt chạy thật.

## Phạm vi ghi dự kiến

- `.claude/dev/launcher.py` và `.claude/dev/launcher_test.py`.
- Đặc tả của packet và changelog nếu quy trình kho yêu cầu.
- Dùng cấu hình phiên riêng để giới hạn lệnh reviewer. Không sửa ACL, ghi credential, cấp quyền chung cho Bash hoặc thay hợp đồng review.

Đối chiếu #1233 trước khi cấp lease. #1233 xử lý prerequisite credential trên các route native. Packet này chỉ sửa receipt/runtime labeling và đo quyền lệnh. Hai packet dùng chung tệp nên chạy tuần tự theo lease.

## Nghiệm thu

1. CLI trực tiếp `agy`, Windows `agy.EXE`, và đường dẫn tuyệt đối khớp đúng tuple. Lệnh tương tự nhưng khác basename và luồng wrapper vẫn theo hợp đồng cũ. Các route Claude/Codex/LLM giữ phân loại.
2. Bộ kiểm biên nhận đọc cùng tập provider/surface/transport trước và sau. Không đổi chính sách model assurance hoặc mặc định bảo mật.
3. Launcher và biên nhận chạy bộ test hiện hành. Thêm hồi quy cho receipt của AGY và phép đo đường dẫn Windows.
4. Native Windows smoke trên đúng candidate: prompt/hash/head/worktree/deadline được kiểm, allow đúng `git --version` thì có kết quả, lệnh chỉ đọc ngoài danh sách bị từ chối. run.json ghi tuple AGY đúng. Không khởi chạy B4/PR2 trong packet này.
5. Review độc lập, audit và cổng theo lớp sensitive trên đúng SHA trước khi land. Ngân sách B4 và PR2 vẫn là 6/6.

Bằng chứng liên quan: smoke a2bfbc77 thành công về quyền lệnh nhưng Launcher ghi local_process; hai lượt review chính thức 9a626605 và 18f4b763 phản hồi rỗng khi bị từ chối command. [Hồ sơ](https://github.com/ducthangho/tra-luat/commit/3ba3141b18c4bcefc2801f2b53f6fa5542187549).
