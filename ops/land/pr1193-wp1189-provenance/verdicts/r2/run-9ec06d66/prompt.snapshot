# Cross-review OFFLINE lượt 2 — packet #1189 LEASE-PUBLISH-GHIM-PYTHON r1 g1 (reviewer: openai_codex)

Bạn là REVIEWER độc lập. reviewed_sha = d5d3c8ffc021db8a99c366c7520b4f063cd27ab8,
base = 1f0941e9bba1d1d517eda4174167b81963c06bd5. SHA của lượt 1 = 3ca0da3b94a3078199ca8712bc26aa3b04009226.

Lượt 1 (`VERDICT_luot1.md`) cho `approve` với một P3 (F1: chú thích khẳng định `python3` của runner là 3.14, trong khi
SPEC §7 nói đó mới là suy luận). Executor sửa CHỈ câu chú thích; delta giữa hai lượt ở `delta_luot1_luot2.patch`.

cwd chứa: `SPEC.md` (sha256 8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce — tự kiểm), `LEASE.yaml`,
`diff.patch` (base→reviewed_sha), `delta_luot1_luot2.patch`, `numstat.txt`, `a1_check.py`, `VERDICT_luot1.md`,
`cay-kho/` (clone đầy đủ lịch sử, checkout reviewed_sha, core.abbrev=7).
Python 3.12 + PyYAML 6.0.3: `/tmp/claude-0/-home-user-tra-luat/de0a61d6-485d-5aff-a726-b5b4e3780688/scratchpad/py312/bin/python`
(PY312). `actionlint` ở `/root/.local/bin`; `shellcheck` ở PATH hệ thống.

Nhiệm vụ (ĐO, đừng tin lời khai):
1. Xác nhận delta giữa hai lượt chỉ là chú thích (không đổi khoá YAML nào): so `yaml.safe_load` của hai SHA.
2. F1 đã đóng chưa: chú thích mới còn khẳng định điều gì SPEC chưa đo không? Có cú pháp biểu thức Actions (dấu đô la +
   ngoặc nhọn đôi) trong dòng chú thích mới không?
3. Chạy lại trên reviewed_sha: A1 (`PY312 a1_check.py cay-kho/.github/workflows/ops-publish-lease.yml`), A3
   (`actionlint` rc=0, shellcheck có mặt), A4 (numstat 1 tệp), `git diff --check base reviewed_sha` rc=0.
   A2 (`python3 ops/lease_publish_test.py` trong `cay-kho/`, PATH có bin của PY312 đứng đầu) — đòi dòng
   `lease_publish: N/N đạt` hai số bằng nhau, `bỏ qua=0`. Selftest tl.py KHÔNG bắt buộc chạy lại (delta chỉ là chú thích
   YAML; lượt 1 đã đo trên 3ca0da3); nếu chạy, nhớ lượt 1 phải tắt ký commit cho kho mẫu trong env tiến trình.
4. Kiểm lại toàn bộ diff.patch lần nữa với con mắt mới: có rủi ro nào lượt 1 bỏ sót không?

KHÔNG sửa gì trong `cay-kho/`. Không push, không gọi GitHub.
Severity ADR-0060 M1: P0/P1/P2 chặn; P3 không chặn nhưng phải nêu kèm bằng chứng.
Ghi DẦN vào `VERDICT.md` trong cwd (tạo ngay với `verdict: pending`), cùng dạng với `VERDICT_luot1.md`:
`verdict`, `reviewed_sha`, `findings` (kèm trạng thái F1: closed/open), `phep_do` (lệnh · rc · dòng then chốt).
