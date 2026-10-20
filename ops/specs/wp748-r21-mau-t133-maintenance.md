# WP748 r21/g21 — tắt git auto-maintenance trên kho mẫu `_mau_t133`

## Thẩm quyền và nguồn gốc

Chỉ thị của chủ kho: "Cấp packet r21 đi" (phiên Claude Code `session_014eUnFtkty9fZicFG9T1Wei`, 2026-10-20T02:21Z),
ghi hộ ở https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6281866960. Executor: Claude Code
(`anthropic_claude`, `claude_code`, remote Linux). Reviewer: phiên Codex độc lập, chỉ đọc, neo đúng head cuối. Review
Class `sensitive`. Base: `origin/master` `3950a0f9fd0a9c29a36a599edc7a2d305619fc27` (tree `5519787a7e7f304f35209cc1eb6ef563b5ac4ab6`).

r20/g20 đã land (PR #849, merge `9422054`; hồ sơ `ops/land/pr849-wp748-land-evidence.yaml`); lease r20 rút hạn về
`2026-10-20T01:13:00Z` nên `thay_the_cho: []`.

## Lỗi

`ops-publish-lease.yml` chạy `ops/lease_publish_test.py` lấy từ `origin/master`. Run `39352202619` đỏ ở attempt 1 và 2:
`t125` (A/B toàn suite theo `GITHUB_ACTOR`) thấy lượt có actor `265/266`, lệch đúng `t133`, lý do
`shutil.Error ... .git/objects/maintenance.lock ... [Errno 2] No such file or directory`. `t133` chép (`copytree`) kho mẫu
do `_mau_t133` dựng một lần mỗi tiến trình (thêm ở WP748 r17, land qua #849). Mỗi `git commit` trên git 2.55 của runner
có thể sinh `git maintenance run --auto --detach`; tiến trình nền ấy tạo rồi xoá `maintenance.lock` ngay trong kho mẫu,
nên `copytree` thấy tệp lúc liệt kê và mất tệp lúc chép. Container dev (git 2.43) không tái hiện được.

## Write set hiệu lực

1. `ops/lease_publish_test.py`

Băm `5cb55494c271c8ab73b6728bccfa8573c971c539eb1ad6d7912b647fd55eec0f` (sorted NFC casefold, compact UTF-8 JSON). Quét
`ai-dang-giu` 2026-10-20T02:23:49Z trên 518/518 ref sống: `NGƯỜI_GIỮ 0`.

## Thay đổi

- Kho mẫu `_mau_t133` tắt `maintenance.auto` và `gc.auto` NGAY sau khi được tạo, trước commit đầu tiên, để không commit
  nào của mẫu sinh maintenance nền.
- Ca mới khoá điều kiện đó trên chính kho mẫu (đọc config thật), kèm đột biến gỡ cấu hình làm ca ĐỎ.
- Không skip ca, không nới assertion, không đổi `ops/lease_publish.py`.

## Chấp nhận

- `python3 ops/lease_publish_test.py` N/N trên Linux, kể cả `t125` A/B; ruff F delta so master = 0.
- Đột biến mới bị giết đúng ca đích.
- PR vào `master`; CI bắt buộc xanh trên head cuối; lượt `ops-publish-lease.yml` sau merge xanh là bằng chứng sau land.
- Codex review độc lập trên head cuối: 0 P0/P1/P2.
- Chủ kho duyệt lần cuối trên SHA cụ thể trước merge. Land bookkeeping là bước riêng.

## Dừng

Dừng và báo khi: có người giữ chồng lấn, cần ghi ngoài write set (vd `ops/lease_publish.py`, workflow), hoặc thiếu bằng
chứng dương.
