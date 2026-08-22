# HANDOFF — `LEASE-DANG-WINDOWS` (#238), Executor lượt 4 (`codex`)

- Provider `openai_codex`; execution surface Codex workspace service; transport machine; role Executor.
- Bản vá nguyên vẹn: `73/73 đạt; đã chạy=73, bỏ qua=0`; `rc=0`.
- Bản vá + X1: `64/65 đạt; đã chạy=65, bỏ qua=8`; `rc=1`; ca đỏ thật: `t73_nen_posix_khong_duoc_bo_qua_ca_nao`.
- X1 không kèm bản vá: `64/64 đạt; đã chạy=64, bỏ qua=8`; `rc=0` (XANH, tái hiện đúng lỗ).
- `git diff --numstat ba82b06f..HEAD` trên write-set: `2 4 .github/workflows/ops-publish-lease.yml`; `122 16 ops/lease_publish_test.py`; tổng 2 tệp, `+124/-20`, dư 1/125 dòng thêm.
- Cổng kế thừa: suite với ba biến GitHub và `gh` vắng vẫn `73/73`; actionlint 1.7.7 với ShellCheck 0.9.0 có mặt `rc=0`; M1–M4/A5/D3/D4 và 8 guard giết `15/15`; P1-1/P1-2/P1-2(b), W6′/W7′/W8/W9 đều đỏ.
- `chua_do_duoc`: W3′ và hành vi P1-3 trên `windows-latest` thật ở exact head mới; ShellCheck có/vắng trên runner Windows; nguyên nhân gốc tám ca/t49 và argv t49 thật; `gh` thật.

---

## PHỤ LỤC của PHIÊN ĐIỀU PHỐI — mỏ neo theo `AGENTS.md` §5

> Phần trên là **báo cáo của executor**, giữ nguyên văn, không sửa một chữ.
> Phần này do phiên điều phối thêm sau, để đóng đúng một finding **P1** của
> `chatgpt-codex-connector` trên PR `#246`: báo cáo thiếu **exact head SHA**, **tree hash**,
> **command** và tách **`passed`/`failed`/`skipped`/`not_run`** mà `AGENTS.md:110-122` đòi.

### Mỏ neo — hai head, hai vai trò khác nhau

| vai trò | commit | tree |
|---|---|---|
| **head MÃ** — nơi ba số của cổng được đo | `7f91ea1cffe17af391362a91b83907c32b16f3b2` | `e077a14f4c094f8ee01b757e02a59b775e3af170` |
| **head SẼ LAND** — sau khi merge `origin/master` (`195a478`) | `e969739cb3aed38a4aad575df4184f541275f31f` | `4e47518164f3451191b759fff3f3fe724a1c357a` |

Hai tree **KHÁC NHAU** — merge kéo vào các tệp của master. Write-set thì **không đổi**:
`git diff --numstat 7f91ea1 e969739 -- <write-set>` ⇒ **rỗng**.

### Command và mã thoát thật

```
PATH=/tmp/actionlint:$PATH python3 ops/lease_publish_test.py
  · bản vá nguyên vẹn (7f91ea1)      rc=0   73/73 đạt; đã chạy=73, bỏ qua=0
  · bản vá + X1                      rc=1   64/65 đạt; đã chạy=65, bỏ qua=8   ĐỎ t73_nen_posix_khong_duoc_bo_qua_ca_nao
  · X1 KHÔNG kèm bản vá (đối chứng)  rc=0   64/64 đạt; đã chạy=64, bỏ qua=8   XANH — lỗ tái hiện đúng
  · sau merge (e969739)              rc=0   73/73 đạt; đã chạy=73, bỏ qua=0

git diff --numstat ba82b06f <head> -- .github/workflows/ops-publish-lease.yml ops/lease_publish.py ops/lease_publish_test.py
  · 7f91ea1 và e969739 đều cho: 2 tệp, +124/-20   (trần 125)
```

`X1` = bỏ mệnh đề `(nen or os.name) == "nt"` khỏi `_ly_do_bo_qua_workflow`, áp trên **bản sao tạm**.

### `passed` / `failed` / `skipped` / `not_run` — tách riêng

Lượt `workflow_dispatch` **`32568867269`** trên **`e969739cb3aed38a4aad575df4184f541275f31f`**,
`run_attempt: 1`, 2 job, không job nào đỏ:

| job | passed | failed | skipped | not_run |
|---|---|---|---|---|
| `gate (ubuntu-latest)` | `lease_publish: 73/73 đạt; đã chạy=73, bỏ qua=0` (0 dòng `BỎ QUA`) | 0 | các bước có `if:` không thoả (`PR head contains required EOL base` — event là `workflow_dispatch`; `gate lifecycle` — nền có cgroup; `tl selftest (lượt PR)`) | 0 |
| `gate (windows-latest)` | `lease_publish: 65/65 đạt; đã chạy=65, bỏ qua=8` (đúng 8 dòng `BỎ QUA`) | 0 | như trên, cộng `don-nhanh selftest` và `bo ca gate chay TRONG cgroup (Linux)` | 0 |

65 + 8 = 73. Tám ca bỏ qua là `t51 t52 t59 t60 t62 t63 t66 t68`, mỗi ca in
`runs-on đã đọc được: 'ubuntu-latest', phân giải thành ['ubuntu-latest']`.
**`t49` KHÔNG nằm trong** — nó chạy thật trên Windows.
**`t73` KHÔNG nằm trong** — số Windows đi `64 → 65` so với lượt trước, tức nó chạy thật và xanh.

### Về phần SAI của finding — nói thẳng để hồ sơ không mang số hỏng

Finding neo vào commit **`dfe4d157194ddcd861ba5e0d042437c4ed91f96d`**. Commit ấy **KHÔNG TỒN TẠI**:
`git cat-file -t` trong kho và `get_commit` qua API đều trả *không tìm thấy*. `merge_commit_sha`
của PR `#246` lúc đo là `None`.

Và câu *"bằng chứng Actions … chạy trên commit khác `e969739…`"* **nói ngược**: `e969739` **CHÍNH LÀ**
head của PR `#246`, nên lượt `32568867269` chạy đúng trên head chứ không phải trên SHA khác.

Phần **đúng** của finding là phần đã vá ở trên: báo cáo thiếu mỏ neo mà `AGENTS.md` đòi.

### Phần commit này KHÔNG đo được

Commit mang chính phụ lục này có SHA **chưa tồn tại lúc viết** — không tự tham chiếu được. Nó
**không đổi một dòng mã nào** (chỉ `ops/handoff/**`, ngoài write-set), nên ba số của cổng ở trên
giữ nguyên; lượt CI đo nó được nêu trong thread PR `#246`.
