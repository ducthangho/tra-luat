# Cross-review CI-CONCURRENCY-MASTER r1 — đang thực hiện

reviewed_sha: 024212c1f565858788edc0b3e48fdf8a356ac8b4
base_sha: 9091cf52cf20ac197c1a356d6a33cac6bab0b318
windows: not_required (ghi nhận quyết định của chủ kho trong đặc tả; không chạy Windows)
provider: openai_codex
execution_surface: Codex agent, shell cục bộ qua exec_command
transport: direct
review_class: sensitive

## Preflight

- `git -C kho rev-parse HEAD`: rc 0, đúng SHA được chỉ định.
- `git -C kho status --short`: rc 0, output rỗng.
- `sha256sum kho/ops/specs/CI-CONCURRENCY-MASTER-r1.md`: rc 0, `72b63a79e0b63193904aaa5378ffd266bce1eb0322cf8c4e425c5b7d9a58f7f8`, đúng đặc tả đóng băng.
- Diff base..head gồm đúng bốn tệp trong write set, 130 dòng thêm, 4 dòng xóa.
- Kho được xử lý chỉ đọc; thử đột biến sẽ thực hiện trên bản sao tạm bên ngoài kho.

## Trạng thái

Đã đọc chỉ thị, AGENTS.md, diff, đặc tả, ADR-0060 M1–M3 và protocol §8/§13. Chưa có kết luận approve/changes_requested; chưa coi phép đo nào chưa chạy là pass.

## Phép đo đã xong

- `python ops/ci_duong_nhanh_test.py --mot-ca y13b_concurrency_master_theo_sha` (cwd `kho`): rc 0, stdout/stderr rỗng, ca có trong registry và không có nhánh bỏ qua.
- `python ops/ci_duong_nhanh_test.py --mot-ca y13_khoa_topology_cua_ci_yml_ngoai_than_run` (cwd `kho`): rc 0, stdout/stderr rỗng.
- Tree head: `3c8753a8f73c8cce0cbeba27ba457105461b0ab3`; `core.abbrev=7`; Python 3.13.18; actionlint 1.7.7 có mặt; shellcheck vắng.
- Snapshot gồm tracked/index, diff và untracked/ignored: sạch; lưu tại `out/before.json`.
- Đọc trực tiếp GitHub Issue #1132 và comment authority: spec được chủ kho duyệt ở `issuecomment-6566883677`; lease projection đúng base/spec/write set, generation 1, hạn 2026-11-03T01:29:00Z.
- Đã đọc được danh sách cả 8 run A5 trên GitHub: vế cũ có 2 lượt cancelled, vế mới cả 4 lượt success. Đang đối chiếu job count, runner_id, thời điểm và byte workflow tại từng SHA.

Đột biến, lint delta và ba cổng A8 đang chạy trên bản sao tạm ngoài kho. Script tái lập: `out/review_checks.py`. Bộ đầy đủ 30–40 phút chưa chạy; không dùng số kiểm kê thay kết quả suite.

## Phát hiện đã có bằng chứng (đang hoàn tất báo cáo)

- **F1 — P3 — `concurrency-comment-permanent-gap` — `.github/workflows/ci.yml:55`**: chú thích mới nói commit của lượt pending bị thay chỗ “không bao giờ được gate”. Câu này vượt quá hậu quả thật của việc hủy một run: retry hoặc dispatch vẫn có thể gate đúng commit ấy. GitHub readback độc lập: push run `41336643336`, attempt 1, `cancelled`; dispatch run `41356691133`, `success`; cả hai cùng `head_sha=f2102fc388a884d994f7bfeb29ef6863b9972b66`. Đề xuất giới hạn câu vào việc lượt push tự động bị mất và commit có thể còn thiếu gate nếu không chạy lại; khóa bằng kiểm tra chú thích, tránh mọi cú pháp nội suy Actions trong chú thích mới. Không đổi hành vi workflow. Theo ADR-0060 M1, P3 mở cần đóng hoặc chủ kho miễn trên exact SHA.

## Kết quả bổ sung

- Đột biến: 3 đột biến đăng ký liên quan concurrency đều `GIET`; 8 đột biến do reviewer tự đo (group cũ, cancel=true/false, group tương đương khác byte ở từng workflow) đều bị `y13b` giết bằng `DO:...`, rc 3. `y13` đơn lẻ không đo launcher nên các biến thể launcher sống trước `y13`, nhưng bị `y13b` bắt; không có đột biến nào sống qua cả hai ca.
- Số kiểm kê AST/runtime: base 113 ca/419 đột biến, head 114 ca/421 đột biến; không phải kết quả full suite.
- actionlint 1.7.7 trên hai workflow: base rc 0, head rc 0, không output, delta 0. shellcheck vắng: không tuyên bố đã lint shell.
- A8: doctrine-scan, adr-song, doc-claims-check đều rc 0 ở base và head; stdout trùng byte. doc-claims-check `ok=true`, flags rỗng, cùng 381 advisory nền.
- A9/A10 đọc được ở exact head: CI đột biến đầy đủ run `41373591105` đang queued; CI PR run `41373632563` đang queued; chưa có bằng chứng success cho hai tiêu chí này.

Các log độc lập được lưu ở `mutations.json`, `lint.json`, `gates.json`, `workflows.json`, `a5-github.json` cùng thư mục với verdict.

## Kiểm tra chốt trước khi viết kết luận

- A5: đọc byte workflow tại cả 8 SHA bằng `git show`; 4 lượt cũ cùng hash workflow, 4 lượt mới cùng hash khác; mọi lượt chỉ `on: push` nhánh thử, job `sleep 120`, cancel expression đúng nhánh thử. Không có sửa đổi workflow lẫn giữa một vế.
- A7 máy: câu cũ vắng, có `một lượt pending`, có `#1132`, không có ký hiệu mở biểu thức Actions trong phần chú thích concurrency mới. F1 là vấn đề nghĩa của câu, các phép khớp chữ A7 không bắt được.
- M2: đã quét cả 8 tệp workflow, cả cấp workflow và job. Chỉ `ci.yml` và `launcher-windows.yml` gác push master, đều đã vá. Các khối cố định/theo ref còn lại thuộc dọn ref, mở PR, đăng lease và admission PR; không phải gate push master.
- PR #1141 hiện draft, head đúng SHA; chưa đủ điều kiện merge vì A9/A10 chưa success, connector/kiem-merge chưa xác minh và F1 chưa đóng/miễn.
- Snapshot cuối `after.json` trùng byte với `before.json` (`cmp` rc 0): head/tree, index, tracked diff, untracked/ignored không có delta quan sát được. Điều này chỉ chứng minh hai mốc quan sát, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.
