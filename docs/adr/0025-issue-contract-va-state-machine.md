# ADR-0025 — Issue contract và state machine

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Mission và Work Packet được tạo từ GitHub Issue Forms có schema version. Phần dễ đọc của Issue giữ mục tiêu,
prompt, acceptance criteria, write set, dependency, executor và environment để dùng được trên web/Android. Khi
packet vào `ready`, dispatcher tính effective write set/required checks từ change-impact policy canonical rồi
đóng băng cả policy SHA trong spec hash. Đổi trường điều phối hoặc policy làm closure thay đổi phải tạo revision
mới, thu hồi lease cũ và cấp generation mới.

Trạng thái hiện thời nằm trong JSON **state projection** ở comment riêng do dispatcher sở hữu, nhưng comment này
không còn là bản sao duy nhất vì GitHub cho phép update/delete comment. Trước mỗi lần sửa projection, dispatcher
nối một **state event** mới: schema version, revision, event, full post-state checkpoint, state hash và
`prev_event_hash`; event cũ không bị bot sửa. Projection lệch journal thì tự dựng lại từ checkpoint/chain; thiếu,
trùng hoặc sai hash thì fail-closed sang `paused`, không đoán trạng thái.

Mỗi revision còn có recovery snapshot JSON trong artifact xoay vòng khi mission đang active. Artifact chỉ là
backup có thời hạn, không thay journal; land apply neo `mission_id` và final state hash vào commit canonical.
Label, assignee và project board chỉ là hình chiếu UI, không phải khóa hay nguồn sự thật. Handoff đầy đủ được lưu
bền trong bot comment và PR. Packet đi qua state machine
`proposed → ready → leased → running → reviewing → accepted → integrated → landed`, cùng các nhánh `paused`, `blocked`,
`cancelled` và `stale`.

Command/handoff phải tồn tại thành durable inbox fact có GitHub object ID trước khi dispatcher xử lý. Reconciler
single-writer đọc fact chưa tiêu thụ theo thứ tự tất định, áp transition idempotent và ghi
`last_consumed_event_id`. GitHub Actions concurrency dùng `queue: max` và không `cancel-in-progress` chỉ làm
backpressure, vì queue có trần và thứ tự run không bảo đảm thứ tự dispatch; scheduled/manual reconcile bắt event
bị bỏ. Projection/journal có revision và spec hash; event cũ hoặc generation cũ bị từ chối thay vì ghi đè trạng
thái mới. Thiết kế này chống mất/sửa nhầm một object, không tuyên bố chống repository administrator có chủ ý phá
cả comment, artifact và lịch sử canonical.
