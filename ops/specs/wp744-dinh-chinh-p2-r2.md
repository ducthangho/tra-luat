# wp744 — Đính chính P2 của PR #724, spec r2

## Định danh và mỏ neo

- `packet_id`: `wp744`; `packet_issue`: #744; `mission_issue`: #744; `revision`: 2; `generation`: 2.
- `base_sha` và `immutable_acceptance_baseline`: `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9` (master đo lại ngày 2026-10-13). `start_from_sha` cũng bằng base này vì g1 chưa có delta sản phẩm.
- PR #746 tại `5b68a7b1d82d8edef94609188e154faeaca656bc` là bản đề xuất trước lease, chỉ làm nguồn đọc; các commit đó không được ghi nhận là thi công có lease.
- Lease g1 `wp744-r1-g1-claude-windows-20261012` đã hết hạn, worktree/remote head g1 vẫn ở base và sạch; không hồi sinh lease hoặc branch g1.
- Executor: `google_antigravity`, `model: gemini-3.8-flash-high`, `model_family: gemini`, `execution_surface: antigravity`, `transport: machine/local`, Windows; branch/worktree mới `agent/wp744-g2-antigravity` từ base SHA trên. Reviewer: Codex CLI, `model_family: openai`, context/worktree độc lập, read-only, trên exact head; chỉ verdict có evidence họ model và exact SHA mới có thể đạt `cross_approved`.
- `risk`: sensitive; `review_class` tối thiểu sensitive. Dispatcher xác định `effective_review_class: sensitive` từ closure bốn tệp và nội dung canary/stage ở ranh giới credential theo Protocol §10; không hạ lớp.

## Objective và quyết định tuyến

Đính chính các P2 của review #724 trong bốn spec r2. Quyết định điều phối theo ủy quyền của chủ kho: các PR lịch sử #725–727 đã đi trực tiếp vào master được ghi là sai lệch tuyến theo Protocol §5; **không cấp ngoại lệ hồi tố**. Các Packet kế tiếp phải đi qua mission integration và cổng land. Không sửa lại sự kiện Git đã xảy ra.

Ma trận đúng năm finding của review #724:

| Finding | Trạng thái ở proposal #746 | Điều kiện đóng ở Packet này |
| --- | --- | --- |
| `#4242170323` | addressed at spec level; runtime chưa đo | r2 phân biệt `False` sau stage rc4 với `None`, neo mã #730; mở successor code nếu lệch |
| `#4242170327` | addressed at spec level; runtime chưa đo | r2 buộc export/new và keep-warm chỉ stage một lần, neo mã #730; mở successor code nếu lệch |
| `#4242170329` | OPEN: thiếu quyết định tuyến | ghi sai lệch lịch sử #725–727, không ngoại lệ hồi tố, mọi Packet sau dùng mission integration |
| `#4242170331` | addressed at spec level; Linux audit chưa đo | r2 khóa full target SHA và hai blob OID, pre-run reject mismatch |
| `#4242170336` | addressed at spec level; Linux audit chưa đo | r2 nêu rig bốn chu kỳ, mutant/generator và SHA256SUMS để replay trong Packet audit riêng |

`addressed at spec level` không phải đóng finding runtime hoặc Linux zombie. Bằng chứng đóng cuối cùng cần code/test và audit đúng Packet kế nhiệm.

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
4. Chỉ đổi bốn tệp trong write set. Chạy `git diff --check`, so SHA-256 từng tệp, `python scripts/pkg_secret_scan.py` trên bốn tệp và `python scripts/tl.py --selftest` trên Windows. Ghi command, rc, head/tree, passed/failed/skipped/not_run/not_measured. Handoff ghi session ID, model yêu cầu và model/họ thực đo được từ lượt AG; thiếu bằng chứng họ model thì không khai `cross_approved`. Cross-review Codex độc lập trên exact head; không tự approve/merge/land.
5. PR Executor mới trỏ `mission/744/integration` dựng từ base SHA; PR #746 giữ draft làm hồ sơ đề xuất. Không CI hoặc push cho tới khi các phép kiểm cục bộ và handoff sạch; không LIVE, Drive hoặc credential thật.

## Required checks sau push

Dispatcher lấy tên required checks thật từ branch protection và CI workflow tại thời điểm push, ghi vào handoff kèm policy/catalog/runner identity; không suy `skipped` hoặc check vắng mặt là pass. T1/T2 của Packet sensitive cần classifier + aggregator có positive marker trên exact Executor head/tree, full selftest artifact (JSON + output hash) trên Windows và Linux nếu matrix yêu cầu, security/write-set/EOL/manifest gates và secret scan. T3/T4 là cổng integration/land riêng trên frozen integration/canonical SHA; không coi phép đo local hoặc review advisory thay chúng. Linux audit #728 và runtime canary/stage tiếp tục OPEN cho đến khi có phép đo riêng; lệnh đọc spec không tạo bằng chứng cho chúng.

## Dừng

Dừng nếu head/base đổi, lease hết hạn, holder scan không xác định, cần ghi ngoài bốn tệp, hoặc reviewer tìm P1/P2 chưa được gom theo lớp. Không coi review advisory trước lease là `cross_approved`.
