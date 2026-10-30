verdict: changes_requested
reviewed_sha: fff91390dafb3b8a16e6d11a7243dce036618260
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

Review hai trục Spec và Standards/Security; áp ngưỡng 0 P0–P3 của đặc tả §3, effective review class `sensitive` trong lease. Reviewer `openai_codex`, phiên độc lập; metadata launcher ghi `execution_surface: codex_cli`, `transport: machine`, run `b0c0322f711f418fb3b70079311b1827`. Bundle không có bằng chứng nhận dạng model/effort cho từng response; không suy từ tên công cụ.

### con-tro-tao-them-nghia-vu [P1]

- **Vị trí:** `cay-kho/docs/PROTOCOL_DA_PHIEN.md:1015`.
- **Bằng chứng:** dòng mới là `Chạy test thêm trên máy Windows local của chủ kho, khi máy online, theo ADR-0057.` (tên ADR có backtick trong nguồn). Đặc tả `ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md:16` chỉ nói executor **được dùng** máy; §2.1 ở dòng 31–32 đặt điều kiện **chỉ dùng khi Online** và **nếu packet đã chạy test** thì phải vá lỗi do diff. ADR ở dòng 8 và 31–35 giữ đúng hai điều kiện ấy. Trong khi đó, động từ mệnh lệnh “Chạy test thêm … khi máy online” trong worker gate có nghĩa phải chạy local mỗi khi máy online, kể cả packet chưa chọn dùng local. Đọc “theo ADR” thành chỉ tham chiếu quyền tùy chọn lại cho nghĩa khác. Như vậy con trỏ vừa mang thêm nghĩa vụ không được đặc tả cấp, vừa khiến executor có hai cách đọc về điều kiện worker gate. §2.2 của đặc tả chỉ yêu cầu một câu con trỏ, không chép doctrine.
- **Quét lớp:** đã đọc toàn bộ 75 dòng thêm, đối chiếu phần mở đầu, 10 quyết định, mục “Những gì KHÔNG đổi”, các phương án bị loại, dòng §20 và câu §10.2. Biểu hiện cùng lớp còn mở: chỉ dòng 1015. Các mệnh lệnh trong 10 quyết định đều có gạch đầu dòng tương ứng trong đặc tả; không thấy nghĩa vụ bổ sung khác. `doctrine-scan` xanh không phủ định lỗi này: mã `.claude/dev/packet_loop.py:1625` quét adapter, dùng protocol làm nguồn so sánh, không phân xử nghĩa của câu mới trong protocol.
- **Đề xuất sửa:** thay đúng câu ấy bằng một câu trung tính, ví dụ: `Quy ước sử dụng máy Windows local của chủ kho nằm tại ADR-0057.` (giữ backtick quanh tên ADR). Chỉ để điều kiện áp dụng và nghĩa vụ ở ADR. Không cần sửa đặc tả, CI hay các quyết định trong ADR.
- **Kiểm đóng lớp:** đọc lại cả hai dòng protocol được thêm và toàn ADR, xác nhận mọi nghĩa vụ vẫn truy được về §2 của đặc tả; câu §10.2 chỉ dẫn tới ADR. Chạy lại ba kiểm tra bắt buộc và phép kiểm write set/kích thước trên SHA mới; review này chỉ áp SHA nêu ở dòng 2.

## Đối chiếu đã hoàn tất

- **Mười gạch đầu dòng §2.1:** đủ ở ADR dòng 31–49: phạm vi, merge cộng thêm, khoá, kiểm tải, cô lập, môi trường, tiến độ, đo lường, bằng chứng, xem xét lại. Đường dẫn, mẫu nội dung khoá, lệnh kiểm tải, ba biến môi trường, 13 cột CSV, ngưỡng 5 phút / 10 packet / 30 ngày khớp. Quyền ghi effective write set và lệnh cấm dừng tiến trình phiên khác được giữ.
- **D1–D6:** đủ sáu hàng, số liệu, SHA, PID, thời điểm, mã lỗi và số ca khớp §1. Cách diễn đạt `tl selftest` thành “selftest của tl.py” không đổi số đo. Script đối chiếu mọi token số trong sáu ô số đo; đã đọc thêm phần sự kiện/bài học, không dùng token số làm bằng chứng cho quan hệ nhân quả.
- **§20 và §10.2:** đúng một hàng ADR-0057 trong bảng A, trạng thái Accepted, cột cổng đúng nguyên văn `không cổng — kỷ luật executor`. Đúng một câu thêm trong worker gate §10.2.4, đúng vị trí; lỗi về nghĩa câu đó được nêu ở trên.
- **Cổng:** ADR dòng 59–65 nói thẳng không có cổng cưỡng chế, nêu giới hạn khoá không nguyên tử và tooling ngoài phạm vi. Quét sáu tệp cổng của bảng §20 không thấy `KHOA.txt`, `do-luong.csv`, `list_devices`, `không đo local`. Đọc `cmd_adr_song` xác nhận đây là kiểm metadata/định tuyến, không thực thi nghĩa vụ Windows local. Không có thay đổi mã cổng hoặc CI trong diff.
- **Tham chiếu và những gì không đổi:** đặc tả tồn tại và khớp SHA-256; hai commit `1cc847d`, `e9967f0` có object commit thật; merge PR #1020 là base, PR #1010 có bản vá WinError 5 của nhóm r929; `t192_S8`, r929, c91/c93/c96 có trong các bộ test được dẫn. §8, §10.2.2, §10.2.3 tồn tại và hỗ trợ lời khai về assurance, required CI, provenance và trạng thái thiếu evidence. Không thấy ADR tự cho local thay CI/receipt, sửa branch protection hoặc cấp quyền merge.
- **Giới hạn đo:** không nhận log Windows/CSV gốc nên D1–D6 được kiểm với đặc tả đóng băng, không tái đo trên máy chủ kho. PR #1014, packet #1006/#1017, mission #748 và nội dung comment cấp quyền `6493571372` không được readback GitHub độc lập; các neo này được dẫn từ đặc tả/lease, không bị coi là đã xác minh từ API. `origin` trong clone là mirror cục bộ `/home/user/tra-luat`; không khai đã kiểm remote GitHub hiện hành. Review này không xác nhận CI, merge authority hay trạng thái landed của PR #1022.

Tree được review: `9e6aaf583c41659cd0379292b80b07a110075605`. Checkout được xử lý read-only; sandbox thực tế cho phép ghi workspace, nên tính sạch được kết luận từ snapshot quan sát, không được khai là cơ chế filesystem cấm ghi tuyệt đối.

## Đã chạy

- `git -C cay-kho rev-parse HEAD` — rc 0; `fff91390dafb3b8a16e6d11a7243dce036618260`.
- `sha256sum cay-kho/ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md` — rc 0; `377ecea689043fcab4d007d65d9592bd28819fa37983796e0c1b75b2c154e715`.
- `git -C cay-kho status --short` — rc 0; stdout rỗng.
- Trong `cay-kho/`, với `PYTHONDONTWRITEBYTECODE=1`, cache/output ngoài checkout:
  - `python3 .claude/dev/packet_loop.py adr-song --root .` — rc 0; `adr-song: sạch — 56 ADR trên đĩa, 56 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])`.
  - `python3 .claude/dev/packet_loop.py doctrine-scan --root .` — rc 0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
  - `python3 scripts/tl.py doc-claims-check --json` — rc 0; `"ok": true`, `"files_scanned": 116`, `"flags": []`, `"advisory_count": 381`, `"layers_skipped": {}`.
- `python3 review_checks.py` — rc 0; `{"snapshot_unchanged": true}`. Lệnh, rc, hash stdout/stderr và snapshot lưu tại `evidence/`.
- `git diff 96667715996d41bc45e70a64fbaa8996de20f6a0 fff91390dafb3b8a16e6d11a7243dce036618260 | cmp - ../diff.patch` (cwd `cay-kho/`) — rc 0; stdout rỗng.
- `git diff --numstat 96667715996d41bc45e70a64fbaa8996de20f6a0 HEAD` (cwd `cay-kho/`) — rc 0; `2 0 docs/PROTOCOL_DA_PHIEN.md`, `73 0 docs/adr/0057-windows-local-may-chu-kho.md`: 2 tệp, 75 dòng thêm, 0 dòng xoá.
- `git diff --check 96667715996d41bc45e70a64fbaa8996de20f6a0 HEAD` (cwd `cay-kho/`) — rc 0; stdout rỗng.
- `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 spec_audit.py` (cwd sandbox) — rc 0; `"files": 2`, `"added_lines": 75`, `"section20_row_count": 1`, `"pointer_line": 1015`, `"gate_hits": []`; `D1-D6: 6/6 measurement cells have identical numeric tokens; prose reviewed against frozen spec.` Chi tiết đối chiếu/neo nằm trong `evidence/spec-audit.json`; script kiểm write set thực với `lease.yaml`, không suy từ danh sách tệp dự kiến.
- `git rev-parse --is-shallow-repository` (cwd `cay-kho/`) — rc 0; `false`.
- `git config --get core.abbrev` (cwd `cay-kho/`) — rc 0; `7`.
- `python3 --version`, `git --version`, `uname -sr` — rc 0; lần lượt `Python 3.13.17`, `git version 2.43.0`, `Linux 6.18.44-fc-v185`.
- `python3` heredoc với `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0`, gọi `review_checks.snapshot('final')` và so với `evidence/snapshot-before.json` — rc 0; `{"snapshot_final_unchanged": true, "head": "fff91390dafb3b8a16e6d11a7243dce036618260", "tracked_untracked_ignored_clean": true}`. Snapshot gồm HEAD/tree, tracked diff, index, trạng thái và danh sách untracked/ignored; cả đầu và cuối không có tệp untracked/ignored trong checkout. Chỉ chứng minh hai mốc quan sát không đổi, không chứng minh lịch sử không từng ghi/hoàn nguyên. Hash 11 tệp evidence ở `evidence/SHA256SUMS`.

Không chạy full selftest, Ruff, Windows local hay CI: không thuộc ba gate nghiệm thu của packet tài liệu này; không khai các phần đó là passed.
