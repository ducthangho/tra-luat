# Cross-review OFFLINE — packet #1189 LEASE-PUBLISH-GHIM-PYTHON r1 g1 (reviewer: openai_codex)

Bạn là REVIEWER độc lập (lượt 1). reviewed_sha = 3ca0da3b94a3078199ca8712bc26aa3b04009226,
base = 1f0941e9bba1d1d517eda4174167b81963c06bd5.

cwd chứa: `SPEC.md` (đặc tả đóng băng, sha256 8f4f89a1414fd009f5a16be358925332c6c576a132710f5819e5cce7e778f5ce — hãy tự kiểm),
`LEASE.yaml`, `diff.patch`, `numstat.txt`, `a1_check.py` (phép đo A1 của executor), `cay-kho/` (clone đầy đủ lịch sử,
checkout reviewed_sha, core.abbrev=7). Python 3.12 có PyYAML 6.0.3:
`/tmp/claude-0/-home-user-tra-luat/de0a61d6-485d-5aff-a726-b5b4e3780688/scratchpad/py312/bin/python` (gọi là PY312).
`actionlint` ở `/root/.local/bin/actionlint`; `shellcheck` ở PATH hệ thống.

Nhiệm vụ: kiểm bản vá đúng đặc tả và an toàn. ĐO, đừng tin lời khai của executor.
1. Đọc SPEC.md §2/§4/§5 và diff.patch. Bản vá có đúng "một bước `actions/setup-python@v5`, `python-version: "3.12"`,
   sau checkout, trước bước gọi `python3` đầu tiên", và KHÔNG đổi bước/`on:`/`permissions`/`if:`/`env:` nào khác?
2. A1: `PY312 a1_check.py cay-kho/.github/workflows/ops-publish-lease.yml`; tự dựng ba đột biến của đặc tả (bỏ bước ·
   `"3.x"` · dời bước xuống sau `cài PyYAML`) trên BẢN SAO tạm NGOÀI `cay-kho/` và xác nhận phép đo ĐỎ.
3. A2: trong `cay-kho/`, với PATH có thư mục bin của PY312 đứng đầu (để `python3` là 3.12) và `/root/.local/bin`:
   `python3 ops/lease_publish_test.py` — đòi dòng `lease_publish: N/N đạt` hai số bằng nhau, `bỏ qua=0`.
4. A3: `actionlint cay-kho/.github/workflows/ops-publish-lease.yml` rc=0, với shellcheck có mặt.
5. A4: numstat chỉ 1 tệp.
6. Rủi ro: setup-python có đổi `python3` trên PATH cho các bước sau không; có bước nào gọi python tuyệt đối
   (`/usr/bin/python3`) hay phụ thuộc gói python hệ thống mà sẽ vỡ; có ảnh hưởng `permissions`; tag `@v5` nhất quán với
   `ci.yml` không; chú thích mới có chứa cú pháp biểu thức Actions (dấu đô la + ngoặc nhọn đôi) không — điều đó bị cấm.

KHÔNG sửa gì trong `cay-kho/` (đột biến chỉ trên bản sao tạm ngoài cây). Không push, không gọi GitHub.

Severity theo ADR-0060 M1: P0/P1/P2 chặn; P3 không chặn nhưng phải nêu kèm bằng chứng.
Ghi DẦN kết quả vào `VERDICT.md` trong cwd (tạo ngay từ đầu với `verdict: pending`, cập nhật sau mỗi phép đo):

```
verdict: approve | changes_requested
reviewed_sha: 3ca0da3b94a3078199ca8712bc26aa3b04009226
findings:
  - id · severity · tệp:dòng · mô tả · phép đo tái hiện
phep_do:
  - lệnh · rc · dòng kết quả then chốt
```
