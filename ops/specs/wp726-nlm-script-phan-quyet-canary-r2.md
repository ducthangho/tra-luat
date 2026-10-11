# wp726 — Đính chính hai P2 canary/stage và route sau PR #724 (r2)

> Đây là biên bản đính chính cho spec r1 đã thực hiện qua PR #730. Không cấp lease mới, không tự chứng minh test. Spec r1 giữ nguyên tại Git blob `3373b4fbbce531a3d60081f6d9a1331a2fd89e4c` và SHA-256 `3a6382a2e34e4b577e38dc170a7438ffc144181265d03063ccb48b360da02d43`.

## P2 canary không kết luận (#4242170323)

Spec r1 nói `nlm-auth-stage` rc 4 dẫn đến "NLM chết" rc 3. Rc 4 chỉ cho biết canary **không dương**. Quy tắc r2: sau rc 4, probe lại bằng `_nlm_auth_alive(..., require_notebook_body=True)` với stdout/stderr bị chặn; chỉ `False` cho wrapper rc 3. `None` hoặc `True` mâu thuẫn với stage cho rc 2. Không parse đầu ra thô. Test stateful phải tách `False`, `None`, và `True` mâu thuẫn.

## P2 stage một lần (#4242170327)

"Đúng một lần stage" áp cho **toàn một lần chạy**. Có export mới: `nlm-auth-import.sh` stage một lần; wrapper không stage lại sau import thành công. Import/stage lỗi: wrapper dừng rc 2, không stage lần hai và không xóa plaintext trên Drive. Không có export mới: đường keep-warm stage đúng một lần. Test phải đo cả hai trạng thái và mutant gọi stage lần hai.

Mã đã merge ở PR #730 trên master `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`: `scripts/nlm-auto-refresh.sh` Git blob `03f726fb2d64585fa4c4aa145658f9dd3c6d72a0`; fragment Git blob `19ace16d8e1a1bbec3bd3c676eb0fcdeff183199`. Đây là đối chiếu tĩnh; review/biên nhận test trên exact head phải xác nhận trước khi gọi finding đóng.

## P2 route tích hợp (#4242170329)

Spec r1 dùng `master`; lease chủ kho [6091612697](https://github.com/ducthangho/tra-luat/issues/726#issuecomment-6091612697) cũng ghi `target_branch_neu_land: master`. Quyết định ngoại lệ đối với Protocol §5 phải được ghi bền và có phạm vi #725–#727; tới đó finding route vẫn **mở**. Packet mới theo route integration/land PR mặc định.
