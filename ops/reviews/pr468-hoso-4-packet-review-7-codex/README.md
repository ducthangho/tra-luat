# Hiện vật reviewer lượt 7 — PR #468

reviewed_sha: `b2ea0f24576275014e8124bfd3e0b6a16c3ca8b5`

Đọc kết luận trong `../VERDICT.md`. Gói này chứa phép đo của lượt 7, không phải một bản vá branch.
Mọi lệnh chạy từ thư mục chứa PROMPT.md, chỉ dùng tệp bên trong sandbox; không dùng mạng.

- `initial.json`, `manifest-check.log`: HEAD/tree/môi trường, diff/numstat, băm 62 hiện vật gốc và danh sách 12 tệp bổ sung ngoài manifest cũ.
- `harness.log`, `attack_h.log`, `replay/attack-h-*.json`: kết quả nguyên harness/attack_h từ gói TRONG KHO. Đầu ra corpus trùng từng byte với gói lượt 6.
- `replay_package.py`: dựng ba symlink tạm để nguyên script gói tìm được layout cũ, gọi trực tiếp các script trong kho rồi dọn symlink trong finally. Mặc định chạy harness/attack_h/extra_checks; có thể truyền từng tên. Không chạy song song với test sao chép toàn cây. Lượt 7 gọi thêm `python3 do-review7/replay_package.py extra_checks.py` để tái đo bốn mutant.
- `harness-direct.log`: lỗi khi gọi nguyên script mà chưa tái lập layout. Lỗi này không được tính là lỗi H.
- `static_checks.py`, `static.json`, `static.log`: băm spec/lease/Issue, neo commit, bốn fixture D9 nguyên byte, replay stdout, quét lease snapshot và hai mô hình thời hạn/cập nhật master. Script chỉ tạo symlink khi import harness rồi dọn ngay; không chạy cùng test sao chép cây.
- `measure_costs.py`, `nen-measurements.json`: chạy bản sao nguyên `tinh.py` trong `nen-a1-a5/`, đối chiếu byte đầu ra, tính độc lập từ giây; ghi từng cặp và trung vị/dải sai số.
- `run_measurements.py`: nhóm `real` thử pretooluse/mcp; nhóm `gates` chạy các cổng đã ghi; nhóm `lease-rerun` chạy lease test trên cây sạch sau khi dọn symlink. Đầu ra và rc/thời điểm/thời lượng/băm lưu riêng. Hai suite nhóm real đỏ vì rig; không khai xanh.
- `lease-publish-test.stdout`: lần đầu t82 lỗi copytree do symlink reviewer. `lease-publish-test-rerun.stdout`: chạy lại khi sạch, 121/121 rc0. Giữ cả hai, không quy lỗi đầu cho PR.
- `issue-anchor-fix-check.json`: phép đọc blob LO tại b743f179/8c3e371/HEAD, chứng minh hướng sửa neo Issue #464.
- `build_verdict.py`: công cụ dựng báo cáo từ kết quả có sẵn, không phải phép kiểm. Mặc định vẫn `dang-do`; `--final` chỉ dùng sau khi hoàn tất kiểm cuối.
- `final-check.json`: kiểm HEAD/tree, status, diff tracked và băm gói gốc lần cuối.

`ARTIFACTS.sha256` băm các hiện vật ổn định trong thư mục này, không gồm bản thân manifest, cache hay thư mục tmp. Các stdout cũ được chép vào `replay/outputs/` chỉ để script gói đọc lại; không phải suite lượt 7 vừa chạy. Nguyên liệu MCP trong `nen-a1-a5/raw/` là bản chép của executor, không phải phản hồi mạng reviewer đã tự lấy.

Không có commit/push vào cây/ref được review. Các test có thể tự tạo repository giả và commit fixture bên trong thư mục tmp của sandbox.
