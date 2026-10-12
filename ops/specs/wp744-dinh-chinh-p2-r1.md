# wp744 — Đính chính P2 của PR #724, spec r1

## Định danh và mỏ neo

- `packet_id`: `wp744`; `packet_issue`: #744; `mission_issue`: #744; `revision`: 1; `generation`: 1.
- `base_sha`: `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9` (master đã đo ngày 2026-10-12).
- PR #746 tại `5b68a7b1d82d8edef94609188e154faeaca656bc` là bản đề xuất trước lease, chỉ làm nguồn đọc; các commit đó không được ghi nhận là thi công có lease.
- Executor: Claude Code trên Windows, branch riêng `agent/wp744-g1-claude` từ base SHA trên. Reviewer: Codex độc lập, read-only, trên exact head.
- `risk`: sensitive; `review_class` và `effective_review_class`: sensitive vì spec ràng buộc canary, stage và credential boundary. Không hạ lớp.

## Objective và quyết định tuyến

Đính chính các P2 của review #724 trong bốn spec r2. Quyết định điều phối theo ủy quyền của chủ kho: các PR lịch sử #725–727 đã đi trực tiếp vào master được ghi là sai lệch tuyến theo Protocol §5; **không cấp ngoại lệ hồi tố**. Các Packet kế tiếp phải đi qua mission integration và cổng land. Không sửa lại sự kiện Git đã xảy ra.

## Effective write set

Chỉ bốn đường dẫn chính xác sau, không có prefix:

1. `ops/specs/wp725-nlm-huong-dan-tai-lieu-r2.md`
2. `ops/specs/wp726-nlm-script-phan-quyet-canary-r2.md`
3. `ops/specs/wp727-nlm-refresh-va-goi-y-tl-gws-r2.md`
4. `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md`

Không sửa r1, script runtime, lease, CI, manifest, credential hoặc hiện vật audit Linux trong Packet này. Nếu cần đường dẫn khác, dừng và lập revision mới.

## Acceptance

1. Ma trận năm P2 của review #724 nêu đúng trạng thái từng finding và bằng chứng đóng ở mức spec. `False` sau stage rc4 khác `None`; luồng export/new và keep-warm chỉ stage một lần.
2. Ba spec #725–727 ghi rõ sai lệch tuyến lịch sử, không suy `target_branch_neu_land: master` của lease cũ thành ngoại lệ Protocol §5; quy tắc tương lai là mission integration.
3. Spec #728 khóa target `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`, blob PowerShell `24240a31be4d51332f748d3fdadf3307cb6f1a88` và Tests `4dc5994c363245219419fc0e2a20350761d6f7f1`; lệch mỏ neo phải từ chối trước khi chạy. Rig bốn chu kỳ, mutant/generator và SHA256SUMS phải được lưu để replay trong Packet audit riêng; không khai audit đã đạt từ spec.
4. Chỉ đổi bốn tệp trong write set. Chạy `git diff --check`, so SHA-256 từng tệp, secret scan theo phạm vi, và cross-review Codex độc lập trên exact head. Báo rõ passed/failed/not_run/not_measured; không tự approve/merge/land.
5. PR Executor mới trỏ `mission/744/integration` dựng từ base SHA; PR #746 giữ draft làm hồ sơ đề xuất. Không CI hoặc push cho tới khi các phép kiểm cục bộ và handoff sạch; không LIVE, Drive hoặc credential thật.

## Dừng

Dừng nếu head/base đổi, lease hết hạn, holder scan không xác định, cần ghi ngoài bốn tệp, hoặc reviewer tìm P1/P2 chưa được gom theo lớp. Không coi review advisory trước lease là `cross_approved`.

