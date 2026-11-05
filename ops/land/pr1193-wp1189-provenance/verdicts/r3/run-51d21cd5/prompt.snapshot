# Cross-review OFFLINE lượt 3 — packet #1189 LEASE-PUBLISH-GHIM-PYTHON r1 g1 (reviewer: openai_codex)

Bạn là REVIEWER độc lập. reviewed_sha = 3b430923c88f67041ce79ce9b2f8aac0e53a28b4 — một MERGE COMMIT,
cha 1 = d5d3c8ffc021db8a99c366c7520b4f063cd27ab8 (đã approve ở lượt 2, xem `VERDICT_luot2.md`),
cha 2 = 5fe92c1390ca1723d19f374bd364487f013986a1 (origin/master hiện tại).

Lý do merge: cổng `thu-hoi` trên PR #1193 đỏ rc=12 *"S 5fe92c1 không phải tổ tiên của H d5d3c8f"* vì master đã đi tiếp sau base
1f0941e9bba1d1d517eda4174167b81963c06bd5. Executor merge master vào nhánh, KHÔNG sửa gì khác.

cwd chứa: `SPEC.md` (sha256 8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce — tự kiểm), `a1_check.py`,
`VERDICT_luot2.md`, `diff_vs_master.patch` (5fe92c1→reviewed_sha), `diff_luot2.patch` (1f0941e→d5d3c8f),
`cay-kho/` (clone đầy đủ lịch sử, checkout reviewed_sha, core.abbrev=7).
Python 3.12 + PyYAML 6.0.3: `/tmp/claude-0/-home-user-tra-luat/de0a61d6-485d-5aff-a726-b5b4e3780688/scratchpad/py312/bin/python`
(PY312). `actionlint` ở `/root/.local/bin`; `shellcheck` ở PATH hệ thống.

Nhiệm vụ (ĐO, đừng tin lời khai):
1. Merge có sạch không: cây của reviewed_sha có đúng bằng cây của "5fe92c1 + bản vá d5d3c8f" không (vd `git merge-tree`
   hoặc so `git diff 5fe92c1 reviewed_sha` với `git diff 1f0941e d5d3c8f`); merge có lén đổi tệp nào khác không;
   5fe92c1 là tổ tiên của reviewed_sha (`git merge-base --is-ancestor`).
2. Phần master mới (1f0941e..5fe92c1) có đụng `ops-publish-lease.yml`, `ops/lease_publish*.py` hay thứ gì làm bản vá
   mất tác dụng không.
3. Chạy lại trên reviewed_sha: A1, A3 (actionlint rc=0, shellcheck có mặt), A4 (`git diff --numstat 5fe92c1 reviewed_sha`
   chỉ 1 tệp), `git diff --check 5fe92c1 reviewed_sha` rc=0, A2 (`python3 ops/lease_publish_test.py` trong `cay-kho/`,
   PATH có bin của PY312 đứng đầu) — đòi `lease_publish: N/N đạt` hai số bằng nhau, `bỏ qua=0`.
   Selftest tl.py không bắt buộc.

KHÔNG sửa gì trong `cay-kho/`. Không push, không gọi GitHub.
Severity ADR-0060 M1: P0/P1/P2 chặn; P3 không chặn nhưng phải nêu kèm bằng chứng.
Ghi DẦN vào `VERDICT.md` trong cwd (tạo ngay với `verdict: pending`), cùng dạng với `VERDICT_luot2.md`.
