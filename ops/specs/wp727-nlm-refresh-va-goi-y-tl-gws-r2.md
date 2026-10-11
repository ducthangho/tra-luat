# wp727 — Đính chính route lịch sử sau PR #724 (r2)

> Biên bản cho spec r1 đã thực hiện qua PR #731; không cấp lease mới. Spec r1 giữ nguyên tại Git blob `6d88f2ddbaef5b696b793605dfb4eaee3065ff75` và SHA-256 `ba3d44d79e0b2c63118285f1ef62c16437bce6b86fc1abc5429c32a97a95d913`.

## P2 route tích hợp (#4242170329)

Spec r1 ghi PR vào `master`; lease chủ kho [6091615222](https://github.com/ducthangho/tra-luat/issues/727#issuecomment-6091615222) ghi `target_branch_neu_land: master`. Protocol §5 mặc định đòi Packet PR vào `mission/<issue>/integration` và draft land PR cho canonical. Biên bản này không nói đã có integration/land PR. PR #731 đã merge, nên không thể sửa lại lịch sử bằng một spec mới.

Muốn adjudicate route của #725–#727 như ngoại lệ cần quyết định bền của chủ kho, nêu đúng phạm vi và lý do. Trước quyết định ấy, P2 route vẫn **mở**. Mọi Packet mới dùng route §5 trừ khi được cấp ngoại lệ riêng trước transition.
