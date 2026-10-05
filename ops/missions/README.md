# Mission #686: kế hoạch có phiên bản

`mission-686-r1.yaml` là bản **tái dựng hồi tố**, không phải một Mission Plan
đã được cài ngày 29-09-2026. `mission-686-r2.yaml` là bản đề xuất sau quyết
định đổi executor trên Issue #686; `mcr-686-01.yaml` ghi quyết định ấy và phần
chuẩn hóa schema. `mcr-686-02.yaml` ghi quyết định thêm wp709 trước wp685.
`mission-686-r3.yaml` và `events/mission-686-r3-bootstrap.json` là hồ sơ
bootstrap thủ công theo quyết định đó. Event/comment và projection cần được
đọc lại trước khi xem r3 là trạng thái điều phối. Reconciler tự động và
recovery artifact của protocol §3.3 chưa được cài; hồ sơ này không chứng minh
hai cơ chế ấy đã chạy.

`plan_hash` là SHA-256 của JSON chuẩn hóa từ YAML: bỏ riêng trường cấp cao
`plan_hash`, rồi serialize mapping còn lại bằng Python `json.dumps` với
`sort_keys=True`, `separators=(',', ':')`, `ensure_ascii=False`; mã hóa UTF-8.
Công thức này tránh vòng tự băm và cho phép đối chiếu độc lập. SHA-256 của
**bytes tệp** là một giá trị khác, cần đo và ghi khi chốt commit.

Trước khi dùng r2 để điều phối, cần xác minh lại MCR trên Issue, đóng băng
spec wp685 revision/generation mới, đọc lại Q5/lease/baseline, rồi ghi event
và state checkpoint theo protocol §3.3. Khi chưa có các sự kiện ấy, trạng thái
`proposed` không được suy diễn thành `running` hay `ready`.
