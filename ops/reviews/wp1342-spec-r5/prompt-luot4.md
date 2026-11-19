# Review độc lập ĐẶC TẢ — packet #1342 WP1174-WINDOWS-BACKEND r5 (bậc r1d-a1-ii), lượt 4

Bạn là reviewer độc lập, CHỈ ĐỌC; không sửa tệp, không commit, không gọi mạng. Giữ đầu ra gọn; KẾT THÚC bằng thông điệp cuối có dòng KET_LUAN (lượt trước phiên dừng giữa chừng không có thông điệp cuối — hãy dành ngân sách cho kết luận).

- Cây làm việc = worktree tách rời của `origin/master` `4eda94e9effc6cfe7fcc0b3e3fb4151ad437ecbd`. Tệp chưa commit: `ops/specs/WP1174-WINDOWS-BACKEND-r5.md` (bản 4, sha256 e823ed0bd67f82aa3c870a8d574e2cd8150659d3cf5e98f8ae3ba3b86c17eb5a) và `ops/specs/WP1174-WINDOWS-BACKEND-r5-ban2.md` (bản đã review lượt 2) để `diff -u`.
- Nguồn: r4 trên `origin/ops/wp1342-r4-spec`; hồ sơ land `ops/land/pr1407-wp1342-land-evidence.yaml`; driver r4 `ops/land/pr1407-wp1342-provenance/windows-native/desktop/dot_bien_r4_ban2.py`; hạ tầng test r4 ở `.claude/dev/packet_loop_test.py` 18560–18934, `_module1174` 10647, `_native1342` 18159; sản phẩm `.claude/dev/packet_loop.py` 6745–6912.

Finding lượt 2 (của bạn) cần kiểm đã đóng: F1 P1 J4 nạp bản đối chứng phải neo đúng tệp sản phẩm đang đo (`_module1174` cần `c.script`), argv giống hệt, tách khoá kết quả khỏi argv, dọn tệp kết quả trước đường đo; F2 P2 nhãn đối chứng (ii) gộp nhiều lỗi ⇒ e1c ghi công sai; F3 P2 hạn chung có thể cắt phép chờ 5 s, `_wp1342a1_tin` gộp WAIT_TIMEOUT/WAIT_FAILED, `join(20)` ngoài ngân sách; F4 P2 J12 phải kiểm lại `chau` khi thấy `ket_qua`, payload `long` thiếu mã Win32; F5 P3 không máy nào ra nhánh (B) vì lý do hỗn hợp. Lượt 3 dừng không verdict, với quan sát: tệp `long` chỉ có khi job trong đã gán, nên nhánh (C) không có `long` — bản 4 đã sửa.

## Việc (đo bằng lệnh, ghi lệnh + rc)

1. Bảng trạng thái F1–F5 và quan sát lượt 3: đóng thật hay chưa.
2. Delta có tạo lỗ mới hoặc mâu thuẫn nội tại (M1–M4, §4b, N6–N7, §7) không. Kiểm riêng: thứ tự phân loại bảy vế của J4 (ii) và đường đo có tự mâu thuẫn không; ngân sách 75 s/45 s có đủ cho J4 (hai lời gọi) và J12 không.
3. Chỉ P0–P2 mới chặn approve; P3 ghi kèm nhưng không chặn.

Nếu một hướng thử cần nội dung dạng đường dẫn thoát khỏi cây thư mục, MÔ TẢ BẰNG LỜI.

## Đầu ra

Tiếng Việt, gọn. Bảng trạng thái; finding mới P0–P3 kèm bằng chứng + câu thay thế. DÒNG CUỐI CÙNG đúng một trong hai:
KET_LUAN: approve
KET_LUAN: request_changes
