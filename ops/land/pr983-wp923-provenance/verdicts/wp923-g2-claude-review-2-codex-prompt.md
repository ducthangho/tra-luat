# Cross-review lượt 2/2 — packet wp923 r2 g2, head MERGE

Bạn là REVIEWER độc lập (họ openai). Chỉ ĐỌC và ĐO; không sửa `cay-kho/`, không commit, không push, không gọi mạng.
Mọi kết luận kèm lệnh + output thật.

## Bối cảnh
- Lượt 1 đã `approve` head `67bacb3b51ac9eda72297b10b15b798b3ca51959` (base `e139e55883d90fd74a358230be5599c9e223d4b3`).
  Verdict lượt 1: `VERDICT_LUOT1.md`. Spec đóng băng: `SPEC.md` (sha256 `a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1`).
- Check `thu-hoi` của PR đỏ vì master đã tiến (S không phải tổ tiên của H). Chủ kho quyết định (ghi hộ #923
  issuecomment-6440352875): merge `origin/master` vào nhánh, rồi Codex lượt 2/2 xác minh head merge.
- reviewed_sha = `bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00` (merge commit; cha 1 = `67bacb3`, cha 2 = master
  `09db70350414d767b793a71cb630e643f216a1b1`). Kiểm `git -C cay-kho rev-parse HEAD` và `git -C cay-kho log -1 --format=%P`.
- Phép đo của executor trên head merge: `n2_merge.log` (giống hệt byte log head lượt 1), `diff_vs_master.patch`,
  `master_mang_vao.stat` (phần master mang vào so với base cũ).

## Phạm vi lượt này (theo quyết định chủ kho)
1. Write set giống TỪNG BYTE với `67bacb3`: `.claude/dev/ci_dang_ky_test.py` ở `bbfb96c` == ở `67bacb3`.
2. Phần merge KHÔNG mang thêm finding mới cho packet:
   - master `e139e55..09db703` KHÔNG chạm `.claude/dev/ci_dang_ky_test.py` (Q4), cũng không chạm `.github/workflows/ci.yml`
     (nếu chạm thì các khẳng định timeout trong chú thích phải đối chiếu lại).
   - diff `09db703..bbfb96c` chỉ là 3 dòng chú thích như lượt 1 (N1: +2/−1, AST bằng nhau so với master).
   - merge commit không có nội dung tự giải quyết xung đột (so tree merge với `git merge-tree --write-tree 09db703 67bacb3`).
   - N3 sau merge: tệp mới/đổi từ master có chốt băm nguyên byte `ci_dang_ky_test.py` không (blob OID, sha256)?
   - Commit message của merge không chứa nguyên văn dấu bỏ-qua-CI.
3. Nếu môi trường cho phép: chạy `python .claude/dev/ci_dang_ky_test.py` (KHÔNG `--chay`) ở reviewed_sha và
   `python scripts/tl.py --selftest`. Lượt 1 gặp lỗi fixture git do ký commit kế thừa từ cấu hình toàn cục — nếu gặp lại thì
   cô lập riêng cho tiến trình test (vd biến môi trường `GIT_CONFIG_GLOBAL=/dev/null`), không sửa kho, ghi rõ đã làm gì.

## BẢNG SĂN ≥ 5 hướng độc lập, mỗi hướng LỆNH + OUTPUT THẬT

## Ghi kết quả
Ghi `VERDICT.md` ở thư mục này NGAY TỪ ĐẦU (`verdict: pending`) và cập nhật sau MỖI hướng. Dạng:

```
verdict: approve | changes_requested | blocked
reviewed_sha: bbfb96cbe6b30e0b5b1b30982eae2b5893ac2c00

## BẢNG SĂN
HƯỚNG n: <tên>
  giả thuyết / lệnh / output / kết luận: LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

## FINDINGS
### <slug>  [P0|P1|P2|P3]  <tiêu đề>
```

`approve` chỉ khi không còn P0/P1/P2.
