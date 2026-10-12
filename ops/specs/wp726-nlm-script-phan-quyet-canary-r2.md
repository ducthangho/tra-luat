# wp726 — Đính chính hai P2 canary/stage và route sau PR #724 (r2)

> Đây là biên bản đính chính cho spec r1 đã thực hiện qua PR #730. Không cấp lease mới, không tự chứng minh test. Spec r1 giữ nguyên tại Git blob `3373b4fbbce531a3d60081f6d9a1331a2fd89e4c` và SHA-256 `3a6382a2e34e4b577e38dc170a7438ffc144181265d03063ccb48b360da02d43`.

## P2 canary không kết luận (#4242170323)

Spec r1 nói `nlm-auth-stage` rc 4 dẫn đến "NLM chết" rc 3. Rc 4 chỉ cho biết canary **không dương**. Quy tắc r2: sau rc 4, probe lại bằng `_nlm_auth_alive(..., require_notebook_body=True)` với stdout/stderr bị chặn; chỉ `False` cho wrapper rc 3. `None` hoặc `True` mâu thuẫn với stage cho rc 2. Không parse đầu ra thô. Test stateful phải tách riêng `False`, `None`, và `True` mâu thuẫn.

Mã đã merge ở PR #730 trên master `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`: `scripts/nlm-auto-refresh.sh` Git blob `03f726fb2d64585fa4c4aa145658f9dd3c6d72a0`; fragment Git blob `19ace16d8e1a1bbec3bd3c676eb0fcdeff183199`. Nếu đối chiếu hoặc kiểm tra thực tế bị lệch mã hoặc hành vi, mở successor code packet. Trạng thái finding: addressed at spec level; runtime chưa đo (chỉ đóng hoàn toàn khi có review/biên nhận test runtime trong Packet kế nhiệm).

## P2 stage một lần (#4242170327)

"Đúng một lần stage" áp cho **toàn một lần chạy**. Có export mới: `nlm-auth-import.sh` stage một lần; wrapper không stage lại sau import thành công. Import/stage lỗi: wrapper dừng rc 2, không stage lần hai và không xóa plaintext trên Drive. Không có export mới: đường keep-warm stage đúng một lần. Test phải đo cả hai trạng thái và mutant gọi stage lần hai.

Mã đã merge ở PR #730 trên master `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`: `scripts/nlm-auto-refresh.sh` Git blob `03f726fb2d64585fa4c4aa145658f9dd3c6d72a0`; fragment Git blob `19ace16d8e1a1bbec3bd3c676eb0fcdeff183199`. Mở successor code nếu lệch. Trạng thái finding: addressed at spec level; runtime chưa đo (đóng hoàn toàn cần review/biên nhận test trên exact head).

## P2 route tích hợp (#4242170329)

Spec r1 dùng `master`; lease chủ kho [6091612697](https://github.com/ducthangho/tra-luat/issues/726#issuecomment-6091612697) cũng ghi `target_branch_neu_land: master`. Quyết định điều phối theo ủy quyền của chủ kho (comment 6133771506, spec WP744 r2): việc PR #730 (thuộc chuỗi #725–#727) đi trực tiếp vào `master` là sai lệch tuyến lịch sử so với `docs/PROTOCOL_DA_PHIEN.md` §5. **Không cấp ngoại lệ hồi tố**; không suy `target_branch_neu_land: master` trong comment lease cũ thành ngoại lệ Protocol §5. PR #730 đã merge; không sửa lại lịch sử Git đã diễn ra.

Mọi Packet mới/kế tiếp bắt buộc theo route integration/land PR mặc định của Protocol §5 (`mission/<issue>/integration` rồi draft land PR vào canonical). Finding #4242170329 được đóng ở mức đặc tả (addressed at spec level).
