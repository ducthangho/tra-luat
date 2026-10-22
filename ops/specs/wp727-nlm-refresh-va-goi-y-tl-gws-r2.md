# wp727 — Đính chính route lịch sử sau PR #724 (r2)

> Biên bản cho spec r1 đã thực hiện qua PR #731; không cấp lease mới. Spec r1 giữ nguyên tại Git blob `6d88f2ddbaef5b696b793605dfb4eaee3065ff75` và SHA-256 `ba3d44d79e0b2c63118285f1ef62c16437bce6b86fc1abc5429c32a97a95d913`.

## P2 route tích hợp (#4242170329)

Spec r1 ghi PR vào `master`; lease chủ kho [6091615222](https://github.com/ducthangho/tra-luat/issues/727#issuecomment-6091615222) ghi `target_branch_neu_land: master`. Protocol §5 mặc định đòi Packet PR vào `mission/<issue>/integration` và draft land PR cho canonical. Biên bản này không nói đã có integration/land PR. PR #731 đã merge, nên không thể sửa lại lịch sử bằng một spec mới.

Quyết định điều phối theo ủy quyền của chủ kho (comment 6133771506, spec WP744 r2): việc PR #731 (và chuỗi #725–#727) đi trực tiếp vào `master` được ghi nhận là sai lệch tuyến so với Protocol §5. **Không cấp ngoại lệ hồi tố**; không suy `target_branch_neu_land: master` của lease cũ thành ngoại lệ Protocol §5. PR #731 đã merge; không sửa lại sự kiện Git đã xảy ra trong lịch sử.

Quy tắc cho tương lai: tuyến mặc định là Protocol §5 (`mission/<issue>/integration` rồi draft land PR vào canonical). Ngoại lệ chỉ hợp lệ khi chủ kho quyết định và ghi rõ trong spec/lease của chính Packet đó — tiền lệ #755 (wp728 r2) và chính biên bản này, đi vào `master` theo spec WP744 r3 (#744 issuecomment-6272548529). Finding #4242170329 được đóng ở mức đặc tả (addressed at spec level).

## Phạm vi r2

Chỉ ghi lại sự khác biệt giữa spec r1 và protocol theo quyết định điều phối. Không đổi write set, acceptance, review hay bằng chứng của PR #731. Không coi việc sửa tài liệu này là một lần land mới.
