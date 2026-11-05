# Cross-review wp1237 r1 — LƯỢT 4 (xác minh head sau merge master), reviewer openai_codex, read-only với kho

Không sửa `cay-kho`. Được ghi trong thư mục hiện tại.

## Bối cảnh
- Lượt 3 (`VERDICT_luot3.md`) approve trên `69dbf3af3c82bc6e1d6769666ca670bd706e80a5`.
- Head hiện tại `97cb2dda246886c7d4bec2bea4a4b89342403a65` = merge commit: cha 1 là `69dbf3a`, cha 2 là
  `origin/master` `4fb3c034d0456a600634f501b8f20bd1487e3b83`. Lý do: check `thu-hoi` đòi master là tổ tiên của head.
- `diff_writeset_luot3_vs_head.patch`: diff hai tệp write set giữa 69dbf3a và head (kỳ vọng RỖNG).
- `numstat_vs_master.txt`: diff giữa master 4fb3c03 và head (kỳ vọng chỉ 2 tệp write set).

## Việc (ngắn)
1. Chạy trong `cay-kho`: `git rev-parse HEAD HEAD^1 HEAD^2`, `git diff --stat HEAD^1 HEAD -- ops/cai_actionlint.sh ops/lease_publish_test.py`,
   `git diff --numstat HEAD^2 HEAD`, `git merge-base --is-ancestor HEAD^2 HEAD`. Xác nhận merge không đổi nội dung đã review và không
   kéo thay đổi nào ngoài master vào.
2. Chạy `bash -n ops/cai_actionlint.sh`, `shellcheck ops/cai_actionlint.sh` (nếu có), và `python3 ops/lease_publish_test.py --chi-ca=t35`,
   `--chi-ca=t37`, `--chi-ca=t38` trên head (t237 cần socket: KHÔNG ĐO ĐƯỢC trong sandbox, ghi rõ).
3. Xem các thay đổi phía master có tương tác với hai tệp write set không (vd. ca khác trong lease_publish_test.py trùng tên t237,
   hay workflow gọi cai_actionlint.sh với biến mới).

## Đầu ra
Ghi `VERDICT.md` (verdict, reviewed_sha: 97cb2dda246886c7d4bec2bea4a4b89342403a65, bảng đo LỆNH + OUTPUT, findings nếu có).
DÒNG CUỐI CÙNG của câu trả lời cuối của bạn (stdout) PHẢI đúng một trong:
`KET_LUAN: approve` · `KET_LUAN: changes_requested` · `KET_LUAN: blocked`
`changes_requested` chỉ khi có P0–P2 có bằng chứng chạy được.
