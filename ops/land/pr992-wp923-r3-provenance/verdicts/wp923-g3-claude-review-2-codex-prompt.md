# Cross-review wp923 r3 — lời gọi 2/10: xác minh head MERGE

Bạn là REVIEWER độc lập (họ openai). Chỉ ĐỌC và ĐO; không sửa `cay-kho/`, không commit, không push, không gọi mạng.
Mọi lệnh `rg` phải có đường dẫn tường minh. Mọi kết luận kèm lệnh + output thật.

## Bối cảnh
- Lượt 1 `approve` head `4ea2ae5e1edf152c0a0a35fcdde6f0a9e99ae7ba` (base `7f19424478616b2c5d0a0c7f26839e1d1c41261b`), xem
  `VERDICT_LUOT1.md`. Spec `SPEC.md` (sha256 `0a694a96f02fb02c01e7707d725591dae5f4455464a77e90ca5fd22435eb1ea5`).
- Check `thu-hoi` của PR #992 đỏ `CHAN [12]` vì master đã tiến (`44884446…` không phải tổ tiên của H). Spec Q3 cho phép merge
  `origin/master` (không rebase) rồi xác minh bằng một lượt Codex trong trần.
- reviewed_sha = `5a05d472227d8c14ffa9eedfb516aa4c494108e6` (cha 1 = `4ea2ae5`, cha 2 = master `44884446f71c89e25f9a72ac58e4f597db63c1ba`).

## Phạm vi lượt này
1. `.claude/dev/ci_dang_ky_test.py` ở reviewed_sha giống TỪNG BYTE với ở `4ea2ae5`.
2. Master `7f19424..44884446` KHÔNG chạm `.claude/dev/ci_dang_ky_test.py` (Q4) và không chạm `.github/workflows/ci.yml`.
3. `git diff 44884446 5a05d47` chỉ là diff M1 (+3/−1, một tệp) — xem `diff_vs_master.patch`.
4. Tree của merge == `git merge-tree --write-tree 44884446 4ea2ae5` (không tự giải xung đột). Ghi object tạm NGOÀI `cay-kho`.
5. Commit message của merge không chứa nguyên văn dấu bỏ-qua-CI.
6. N1 trên reviewed_sha: `GIT_CONFIG_GLOBAL=<đường dẫn tuyệt đối tới gitcfg-ky> python .claude/dev/ci_dang_ky_test.py` ⇒ `TỔNG: ĐẠT`;
   và trên master `44884446` (bản sao tạm của bạn) phải ĐỎ ở `_gk commit` — tức phần master mang vào không tự sửa lỗi này.
7. N2 trên reviewed_sha không biến môi trường (nếu máy bạn có ký global hỏng thì ghi lại và đo thêm với `GIT_CONFIG_GLOBAL=/dev/null`).
8. Tệp mới/đổi từ master có chốt băm nguyên byte `ci_dang_ky_test.py` không (blob OID / sha256 của tệp ở reviewed_sha)?

## Ghi kết quả
Ghi `VERDICT.md` NGAY TỪ ĐẦU (`verdict: pending`), cập nhật sau MỖI hướng:

```
verdict: approve | changes_requested | blocked
reviewed_sha: 5a05d472227d8c14ffa9eedfb516aa4c494108e6

## BẢNG SĂN
HƯỚNG n: <tên>
  giả thuyết / lệnh / output / kết luận: LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

## FINDINGS
### <slug>  [P0|P1|P2|P3]  <tiêu đề>
```
`approve` chỉ khi không còn P0/P1/P2.
