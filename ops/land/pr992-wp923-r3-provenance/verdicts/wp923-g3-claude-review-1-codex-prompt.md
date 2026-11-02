# Cross-review packet wp923 r3 (packet A) — lớp sensitive, reviewer codex, lời gọi 1/10

Bạn là REVIEWER độc lập (họ openai) cho diff của executor họ claude. Chỉ ĐỌC và ĐO; không sửa `cay-kho/`, không commit,
không push, không gọi mạng. Mọi kết luận kèm lệnh + output thật. Mọi lệnh `rg` phải có đường dẫn tường minh (không đường
dẫn thì `rg` đọc stdin và treo).

## Neo
- base_sha = `7f19424478616b2c5d0a0c7f26839e1d1c41261b` (master sau merge PR #983)
- reviewed_sha = `4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba` (kiểm `git -C cay-kho rev-parse HEAD`)
- Spec đóng băng `SPEC.md`, sha256 `0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5` (tự băm lại).
- Diff: `diff.patch`. Tệp cấu hình phản chứng: `gitcfg-ky` (`commit.gpgsign=true`, `gpg.program=/bin/false`).
- Log của executor: `n1_base.log` (rc=1, CalledProcessError 128 ở `_gk ... commit`), `n1_head.log`, `n2_r3_base.log`,
  `n2_r3_head.log` (đều `TỔNG: ĐẠT`).

## Executor khai
- M1: thêm `"-c", "commit.gpgsign=false"` vào lambda `_gk` (~dòng 2127), kèm một dòng chú thích có mốc `#923 r3`. +3/−1.
- Quét cả tệp: lời gọi git có `commit`/`tag` chỉ có `_gk("commit", ...)` dòng ~2134. Helper `_git` (~dòng 1331) chỉ gọi
  `init` và `add -f`, không commit/tag ⇒ không cùng hình dạng, không sửa. Các lời gọi `git` khác (dòng 98, 838, 840, 2122)
  là `check-ignore`/`merge-base`/`diff`, không ghi commit.
- N1: `GIT_CONFIG_GLOBAL=gitcfg-ky python .claude/dev/ci_dang_ky_test.py` ⇒ base rc=1, head rc=0 `TỔNG: ĐẠT`.
- N2: không biến môi trường ⇒ `TỔNG: ĐẠT` ở base và head; `BAM_GATE_REGISTRY`/`BAM_GATE_NHANH` không đổi.
- N3: `doctrine-scan --root .` rc 0; `git diff --check` rc 0. N4: `tl.py --selftest` 1731/1731.

## BẢNG SĂN ≥ 5 hướng ĐỘC LẬP, mỗi hướng LỆNH + OUTPUT THẬT
Gợi ý (tự thêm hướng khác):
- H1 Diff đúng phạm vi: một tệp, ≤ 15 dòng thêm, chỉ lambda `_gk` + chú thích; AST khác base đúng ở đối số list của `_gk`.
- H2 N1 tự chạy cả hai chiều trên bản sao: tạo worktree/clone tạm ở base trong thư mục của bạn (KHÔNG sửa `cay-kho`), chạy
  với `GIT_CONFIG_GLOBAL=<đường dẫn tuyệt đối tới gitcfg-ky>`; base phải đỏ đúng chỗ `_gk commit`, head phải `TỔNG: ĐẠT`.
  Lưu ý: chính môi trường của bạn có thể đã có `commit.gpgsign=true` (lượt review trước của packet này gặp đúng lỗi đó) —
  ghi lại `git config --show-origin --get-regexp 'commit.gpgsign|gpg'` trước khi đo.
- H3 Độ phủ quét: còn lời gọi git nào trong tệp (kể cả trong chuỗi workflow, fixture, `subprocess` gián tiếp, `tag -s`,
  `merge`, `commit-tree`) có thể ký trên kho tạm mà executor bỏ sót? Có `tag.gpgsign` cần chặn không?
- H4 Đột biến: gỡ `commit.gpgsign=false` ⇒ N1 head phải đỏ lại; thay bằng `commit.gpgsign=true` ⇒ đỏ. Chứng minh phản chứng
  có răng.
- H5 Không đổi hằng/ghim: `BAM_GATE_*` và mọi chỗ băm job/ci.yml không bị ảnh hưởng; N2 `TỔNG: ĐẠT` ở reviewed_sha.
- H6 Chú thích mới đúng sự thật và đúng idiom tệp (mốc `#923 r3`), không tạo khẳng định HIỆN TẠI dễ cũ.

## Ghi kết quả
Ghi `VERDICT.md` NGAY TỪ ĐẦU (`verdict: pending`) và cập nhật sau MỖI hướng. Dạng:

```
verdict: approve | changes_requested | blocked
reviewed_sha: 4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba

## BẢNG SĂN
HƯỚNG n: <tên>
  giả thuyết / lệnh / output / kết luận: LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

## FINDINGS
### <slug>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG / VẤN ĐỀ / ĐÃ THỬ NGHIỆM / ĐỘ TIN
```

`approve` chỉ khi không còn P0/P1/P2.
