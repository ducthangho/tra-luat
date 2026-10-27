# Handoff wp923 r3 g3 — executor claude (packet A: fixture gpgsign)

- Packet #923, revision 3, generation 3. Lease `wp923-r3-g3-claude`, nhánh `ops/wp923-r3-g3-lease` @ `2b93bd1`. Đọc lúc 14:28Z,
  còn hạn tới 2026-10-29T13:50Z. Spec `ops/specs/wp923-r3.md` sha256
  `0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5`, băm lại khớp.
- Nhánh code `agent/wp923-g3-claude` rẽ từ `7f19424478616b2c5d0a0c7f26839e1d1c41261b` (master sau PR #983; clone KHÔNG nông).
  Head ứng viên `4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba`.
- Codex: `doctor --kiem-song` = DUNG_DUOC, dùng credential của chính container này.

## M1
`.claude/dev/ci_dang_ky_test.py`, lambda `_gk` (khối `with tempfile.TemporaryDirectory() as _k`, các ca `p643-A1-git-that-*`):
thêm `"-c", "commit.gpgsign=false"` vào lệnh git, kèm một dòng chú thích mốc `#923 r3`. Diff +3/−1, một tệp.

Quét cả tệp tìm lời gọi git (`rg -n '"commit"|"tag"|commit -|gpgsign|"git"' .claude/dev/ci_dang_ky_test.py`):
| dòng (base) | lời gọi | commit/tag trên kho tạm? | xử lý |
|---|---|---|---|
| 98 | `git -C root check-ignore -z --stdin` | không | giữ |
| 838 | `git merge-base --is-ancestor` | không | giữ |
| 840 | `git diff --name-only --no-renames -z` | không | giữ |
| 1332 | `_git(*a)` = `git -C <tmp> *a`: chỉ `init -q`, `add -f` | không | giữ (không cùng hình dạng) |
| 2122 | `_dif` (argv giả để so) | không | giữ |
| 2126 | `_gk(...)`: `init`, `add -A`, **`commit -qm`**, `checkout`, `rev-parse` | **có** | **sửa** |

Không có `tag`, `merge`, `commit-tree` nào khác trên kho tạm trong tệp.

## Tiêu chí (đo tại chỗ)
- **N1** `GIT_CONFIG_GLOBAL=<tệp: [commit] gpgsign = true; [gpg] program = /bin/false> python .claude/dev/ci_dang_ky_test.py`:
  base `7f19424` → `rc=1`, `CalledProcessError: ['git','-C','/tmp/…','-c','user.name=t','-c','user.email=t@t','commit','-qm','0']
  returned non-zero exit status 128`; head `4ea2ae5` → `rc=0`, `PHẢN CHỨNG: 1070/1070 đỏ đúng`, `TỔNG: ĐẠT`.
- **N2** không biến môi trường: `TỔNG: ĐẠT` ở base và head. `BAM_GATE_REGISTRY` và `BAM_GATE_NHANH` không đổi
  (`git diff -U0 | rg '^[-+]BAM_GATE'` rỗng).
- **N3** `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `git diff --check` rc 0. Mọi lệnh `rg` trong handoff này
  đều có đường dẫn.
- **N4** `python scripts/tl.py --selftest` trên `4ea2ae5`: `1731/1731`. CI của PR đo sau khi đẩy.
- Ruff: KHÔNG ĐO ĐƯỢC tại chỗ (`No module named ruff`).

## Cross-review
- Lời gọi Codex 1/10, run `6e8f1806` qua `launcher.py run`: `ma_thoat 0`, 996,5 s. `approve` trên `4ea2ae5`, không có finding
  P0–P3. Hiện vật ở `ops/reviews/wp923-g3-claude-review-1-codex/`. Header model/effort: `stderr.log` vẫn chỉ 39 byte, nên
  KHÔNG ĐO ĐƯỢC (đây là lỗi 3, thuộc #987).
- Chưa tới lời gọi thứ 3, nên chưa đo lại ba phép ADR-0055.

## Lỗi khác lộ ra (ghi, KHÔNG vá — Q5)
1. **Hai ca selftest khác cũng phụ thuộc signer của máy.** Reviewer chạy `scripts/tl.py --selftest` trong sandbox Codex (máy có
   ký commit toàn cục, signer `/tmp/code-sign` bị chặn loopback) và ra `1729/1731`. Đỏ là
   `_c226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `_c268_l2_trichotomy_theo_trang_thai_object` (`scripts/tl_selftest.py`,
   khoảng dòng 26947–26999 và 28552–28602). Cả hai cũng đỏ trên base; với `GIT_CONFIG_GLOBAL=/dev/null` thì `1731/1731`.
   Cùng lớp nguyên nhân với M1 nhưng nằm ngoài write set. Ứng viên: packet riêng, hoặc gom thành một helper dựng kho tạm dùng
   chung để không phải vá lặp lại từng chỗ.
2. Reviewer ghi rằng các lượt chạy kế thừa cấu hình đã vô tình kích hoạt signer `/tmp/code-sign`, signer này thử kết nối dịch vụ
   ký loopback và bị sandbox chặn. Lộ cùng lỗi 1: fixture git kế thừa cấu hình ký của máy.
