# wp725 — Đính chính hồ sơ r1 sau PR #724 (r2)

> Đây là biên bản đính chính cho spec r1 đã thực hiện qua PR #729. Không cấp lease mới, không yêu cầu chạy lại packet sản phẩm. Bản r1 giữ nguyên tại Git blob `34138d63e7049fdbb3c63e031ddce4c67c451597` và SHA-256 `cc259607cee772d9170520bbadc57b7cc0e2b41e8bfce1973a798c5f7e73b01e`.

## Finding P2: route tích hợp (#4242170329)

Spec r1 ghi PR vào `master`. Quy tắc mặc định của `docs/PROTOCOL_DA_PHIEN.md` §5 là Packet PR vào `mission/<issue>/integration`, rồi draft land PR vào canonical. Lease do chủ kho đăng cho #725 tại [comment 6091609833](https://github.com/ducthangho/tra-luat/issues/725#issuecomment-6091609833) đã ghi `target_branch_neu_land: master`; đó là bằng chứng về route được chỉ định cho lượt lịch sử, không phải bằng chứng đã thực hiện integration/land PR. PR #729 đã merge; không sửa lại sự kiện đó.

Để adjudicate finding này, cần quyết định bền của chủ kho nêu rõ liệu route `master` của #725–#727 là ngoại lệ có giới hạn đối với §5, cùng lý do và phạm vi. Trước quyết định ấy, finding vẫn **mở**. Mọi Packet mới đi qua integration/land PR theo §5 trừ ngoại lệ được ghi trước khi cấp lease.

## Phạm vi r2

Chỉ ghi lại sự khác biệt giữa spec r1 và protocol. Không đổi write set, acceptance, review hay bằng chứng của PR #729. Không coi việc sửa tài liệu này là một lần land mới.
