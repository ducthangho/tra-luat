# Cross-review OFFLINE lượt 4 — packet #1189 LEASE-PUBLISH-GHIM-PYTHON r1 g1 (reviewer: openai_codex)

Bạn là REVIEWER độc lập. reviewed_sha = 275869169e134758bb145565d28f0b0897a92f87.
Chuỗi commit từ lượt 3 (3b430923c88f67041ce79ce9b2f8aac0e53a28b4, đã approve — `VERDICT_luot3.md`):
- ccf77900e698727d9d5987414bc85def40f0c17c: merge origin/master 358451e80b573d148807717bece3fd973915fbad vào nhánh (tránh trôi head).
- 275869169e…: thêm `ops/specs/lease-publish-ghim-python-r1.md`, chép nguyên byte đặc tả từ nhánh lease, vì `kiem-merge`
  K1 đọc blob đặc tả TẠI HEAD. Chủ kho đã duyệt nới write set thêm tệp này và A4 thành 2 tệp.

cwd chứa: `SPEC.md` (bản đặc tả từ nhánh lease, sha256 8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce),
`a1_check.py`, `VERDICT_luot3.md`, `diff_vs_master.patch` (358451e→reviewed_sha), `delta_luot3_luot4.patch` (lớn vì gồm phần
master), `cay-kho/` (clone đầy đủ lịch sử, checkout reviewed_sha, core.abbrev=7).
Python 3.12 + PyYAML 6.0.3: `/tmp/claude-0/-home-user-tra-luat/de0a61d6-485d-5aff-a726-b5b4e3780688/scratchpad/py312/bin/python`
(PY312). `actionlint` ở `/root/.local/bin`; `shellcheck` ở PATH hệ thống.

Nhiệm vụ (ĐO, đừng tin lời khai):
1. `git diff --numstat 358451e reviewed_sha` trong `cay-kho/`: đúng 2 tệp — `.github/workflows/ops-publish-lease.yml` (+8, giống
   từng byte bản vá đã approve ở lượt 2/3) và `ops/specs/lease-publish-ghim-python-r1.md`. 358451e là tổ tiên của reviewed_sha.
2. Tệp đặc tả tại reviewed_sha có sha256 đúng 8f4f89a1…5ce và giống từng byte `SPEC.md`.
3. Merge ccf7790 sạch: phần nó đưa vào chỉ là nội dung của master (không đổi tệp nào khác ngoài master).
4. Chạy lại trên reviewed_sha: A1 (`PY312 a1_check.py cay-kho/.github/workflows/ops-publish-lease.yml`), A3 (actionlint rc=0,
   shellcheck có mặt), `git diff --check 358451e reviewed_sha` rc=0, A2 (`python3 ops/lease_publish_test.py` trong `cay-kho/`, PATH
   có bin của PY312 đứng đầu) — đòi `lease_publish: N/N đạt` hai số bằng nhau, `bỏ qua=0`.
5. Việc thêm tệp đặc tả vào `ops/specs/` có làm vỡ chốt nào khác của kho không (ví dụ quét doctrine:
   `python3 .claude/dev/packet_loop.py doctrine-scan --root .` trong `cay-kho/`).

KHÔNG sửa gì trong `cay-kho/`. Không push, không gọi GitHub.
Severity ADR-0060 M1: P0/P1/P2 chặn; P3 không chặn nhưng phải nêu kèm bằng chứng.
Ghi DẦN vào `VERDICT.md` trong cwd (tạo ngay với `verdict: pending`), cùng dạng với `VERDICT_luot3.md`.

BẮT BUỘC cho thông điệp cuối cùng của bạn (stdout): dòng CUỐI CÙNG phải đúng nguyên văn một trong hai dòng sau, không thêm gì:
`KET_LUAN: approve` hoặc `KET_LUAN: changes_requested`.
