# HANDOFF — `LEASE-DANG-WINDOWS` (#238), executor lượt 2 (`codex`)

> Bản chép **NGUYÊN VĂN** stdout của lượt chạy `4e5c6da3` (`ma_thoat=0`,
> `thoi_luong_giay=2376.8`, `stdout_byte=4298`). Không sửa byte nào dưới dấu gạch.
>
> Phiên điều phối đo lại độc lập trên exact head `edc1906c`: write_set delta **2 tệp, +90/−20**
> (trần 90) · `ops/lease_publish.py` khớp **BYTE-FOR-BYTE** với `ba82b06f` · suite **`72/72`**
> `đã chạy=72, bỏ qua=0` ở **cả hai** môi trường · `actionlint` trên `ops-publish-lease.yml`
> (thứ `t33` **thật sự** lint) `rc=0`, với `shellcheck 0.9.0` **có mặt**.
>
> **`W3′` ĐẠT** — `workflow_dispatch` run **`32558427472`**: `success`, `run_attempt: 1`,
> `total_jobs: 2`, `failed_jobs: 0`; `gate (windows-latest)` **success**, bước
> `lease-publish selftest` **success**; `gate (ubuntu-latest)` cùng vậy.
>
> **Hai chỗ executor TỪ CHỐI làm tròn, và cả hai đều đúng:** không nhận nguyên nhân `t49` (giả
> thuyết shebang chưa đo được từ Linux), và không nhận gate `actionlint` 5 workflow là pass vì
> `ops-don-ref.yml SC1003:info` là finding **nền** ngoài write set. Chỗ thứ hai lộ ra lỗi trong
> **gate của phiên điều phối**: `t33` chỉ lint `ops-publish-lease.yml`, không phải cả 5.

---

Đã commit và push executor head; chưa thể coi Packet hoàn tất vì còn nghiệm thu Windows thật và gate actionlint nền ngoài write-set.

### 1. Diff và mỏ neo

- Branch: `codex/lease-dang-windows-1`
- Head/remote: `edc1906cf01fcceb15c646e1fdc4fcd8957644ed`
- Tree: `5b195f0720a38d6bbc320e2264405ca579bddb4b`
- Parent: `2ab3560a8a406c1b436221fb3c6d23234aefdde0`
- Worktree sạch; `git ls-remote` khớp exact head.

`git diff --numstat ba82b06f..HEAD`:

```text
2   4   .github/workflows/ops-publish-lease.yml
88  16  ops/lease_publish_test.py
```

Tổng đúng 90 dòng thêm, 2 tệp khác `ba82b06f`. `ops/lease_publish.py` được khôi phục byte-for-byte nên không xuất hiện trong numstat.

Provider: `openai_codex`; execution surface: Codex workspace service; transport: machine; role: Executor.

### 2. Hai suite và lint

- Suite thường: `rc=0`, `72/72 đạt; đã chạy=72, bỏ qua=0`.
- Suite với ba biến GitHub và `gh` thật vắng mặt: `rc=0`, cùng `72/72`; phép tìm `gh` trả `rc=127`.
- ShellCheck được kiểm trước actionlint: `/usr/bin/shellcheck` `0.9.0`.
- actionlint: `/tmp/actionlint/actionlint` `1.7.7`.
- `actionlint .github/workflows/ops-publish-lease.yml`: `rc=0`.
- `actionlint .github/workflows/*.yml`: `rc=1`, duy nhất `ops-don-ref.yml:106`, `SC1003:info`. Tệp này giống base (`git diff --quiet 2ab3560a... -- ops-don-ref.yml` trả `0`) và ngoài write-set. Không nhận gate này là pass, không sửa lấn phạm vi.

### 3. Phản chứng

Tổng cộng `21/21` mutant bị giết.

| Nhóm | Kết quả | Ca đỏ |
|---|---:|---|
| Gỡ riêng `rc`, `stdout`, `stderr` | 3/3 | `t69` |
| W6 | 1/1 | `t70`; đổi YAML thật sang matrix Ubuntu+Windows làm đủ 8/8 ca chạy lại |
| W7 | 1/1 | `t71` |
| W8 | 1/1 | `t72` |
| M1–M3 | 3/3 | `t64` |
| M4 | 1/1 | `t51`, `t63`, `t67` |
| A5 | 1/1 | `t64`, `t66`, `t67`, `t68` |
| D3/D4 | 2/2 | `t64` |
| Gỡ guard `kiem-github` | 1/1 | `t60`, `t64`, `t66`, `t67` |
| Gỡ guard `check` | 1/1 | `t51`, `t64`, `t66`, `t67` |
| Gỡ sáu guard còn lại | 6/6 | mỗi mutant làm `t64`, `t66`, `t67` đỏ |

Danh sách đa sát: M4, A5 và cả tám mutant gỡ guard.

### 4. Nguyên nhân thật của `t49`

Nguyên nhân thật vẫn **KHÔNG ĐO ĐƯỢC** trong Linux. Lượt Windows cũ chỉ ghi nhận tệp `calls` không sinh; harness cũ đã làm mất `rc/stdout/stderr`, nên chưa thể khẳng định lỗi chính xác là shebang không phần mở rộng.

Bản vá tại [ops/lease_publish_test.py](/tmp/claude-0/-home-user-tra-luat/c7eab052-cf71-5777-b253-6b2e409ca64f/scratchpad/wkw/ops/lease_publish_test.py:2246):

- Trên Windows dựng `gh.exe` từ `sys.executable`, còn script giả là đối số `api`.
- Chạy đúng mối nối `gh api ...`, không bỏ qua `t49`.
- Xóa log giữa hai lượt để buộc đồ giả phải chạy lại.
- Nếu log không sinh, lỗi nay chứa đủ `KHÔNG ĐO ĐƯỢC`, `rc`, `stdout`, `stderr`.

### 5. Các ca sẽ bỏ qua trên Windows

Lý do của từng ca đều được đọc động từ YAML: job `dang`, `runs-on: 'ubuntu-latest'`, phân giải `['ubuntu-latest']`, nên artefact được đo chỉ chạy Ubuntu.

| Ca |
|---|
| `t51_lease_giua_bi_chan_van_xu_ly_het_nhung_luot_DO` |
| `t52_buoc_ghi_nguoc_phai_chay_sau_buoc_dang_DO` |
| `t59_moi_lease_goi_kiem_github_truoc_check` |
| `t60_kiem_github_hong_khong_POST_va_lam_buoc_DO` |
| `t62_kiem_github_rc9_bo_qua_lease_va_buoc_XANH` |
| `t63_check_rc9_bo_qua_lease_va_buoc_XANH` |
| `t66_moi_guard_co_phan_chung_va_ve_theo_vi_tri` |
| `t68_post_rc_hong_khong_duoc_mark` |

Mô phỏng riêng cơ chế phạm vi cho kết quả `64/64 đạt; đã chạy=64, bỏ qua=8`, in đủ tám lý do. Đây không phải chạy Windows thật.

### 6. `chua_do_duoc`

- Chưa có `workflow_dispatch` thật, nên chưa có `run_id` và kết luận từng job Ubuntu/Windows cho exact head.
- Nguyên nhân thật của `t49` vẫn chờ phép đo Windows.
- `gh` thật vẫn chưa được đo.
- Gate actionlint năm workflow hiện đỏ bởi finding nền ngoài write-set nêu trên.

Exact head đã sẵn sàng để phiên điều phối chạy W3′: `edc1906cf01fcceb15c646e1fdc4fcd8957644ed`.
