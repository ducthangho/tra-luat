# Review mã GIAM-HOI-P1-SOAN-SPEC r7 g1 — lượt 2 (lời gọi Codex 2/10): xác minh head sau merge master

Bạn là reviewer độc lập, phiên mới, **chỉ đọc** với kho. Không sửa `cay-kho/`, không commit, không đổi HEAD của `cay-kho/`.
Được ghi trong thư mục hiện tại ngoài `cay-kho/` (dùng `scratch/l2/`). Sandbox cấm ghi thư mục tên `.git`: muốn thử bằng Git thì
dựng kho riêng có tên khác trong `scratch/l2/`. Không dùng mạng, không đọc `~/.codex`. Ổ đĩa còn rất ít chỗ (dưới 500 MB): không
tạo bản sao làm việc đầy đủ của kho.

## Bối cảnh

- Lượt 1 (`VERDICT.md` hiện có trong thư mục này, đổi tên thành `VERDICT-luot1.md`) approve, 0 finding, trên
  `68f4f73c3caae73a6a44be1215050ea8938bac65` (tree `9acd42b130ea1acdba31b36a7bb8258d86aca589`).
- Head mới **H = `e97d5d87f4f17c14fe350fb2fe56eddbd9301c9e`** là merge commit: cha 1 là `68f4f73`, cha 2 là `origin/master`
  `dc635d3c90ec…` (lấy đủ SHA bằng `git rev-parse H^2`). Lý do: cổng `thu-hoi` đòi `master` là tổ tiên của head, và `master` đã đi
  tiếp sau base cũ `6f32aad`.
- `cay-kho/` đã checkout H (tách rời), là checkout thưa (không có `ops/reviews/`, `ops/land/` trong cây làm việc).
- Đặc tả `cay-kho/ops/specs/GIAM-HOI-P1-SOAN-SPEC-r7.md` (sha256 `353048bc4f77b3ed39d73b51c869deea787d8a4bd59477e4b351a840e3cc8bd3`).
  Vị từ của nó là khối ```python mục 4 (bản bạn trích ở lượt 1: `scratch/kiem_p1.py`, đo lại sha256 trước khi dùng).

## Việc (ngắn)

1. Trong `cay-kho`: `git rev-parse H H^{tree} H^1 H^2`, `git diff --stat H^1 H -- .claude/skills/soan-spec/SKILL.md
   docs/PROTOCOL_DA_PHIEN.md` (kỳ vọng rỗng), `git diff --numstat H^2 H` (kỳ vọng đúng hai tệp write set, +45/−8 và +4/−4),
   `git merge-base --is-ancestor H^2 H`. Xác nhận merge không đổi nội dung đã review và không kéo gì ngoài `master` vào.
2. Chạy vị từ với base là `H^2`: `python scratch/kiem_p1.py ops/specs/GIAM-HOI-P1-SOAN-SPEC-r7.md <H^2>` từ gốc `cay-kho`
   (phải `ĐẠT`); `git diff --check H^2 H`; `python .claude/dev/packet_loop.py doctrine-scan --root .`;
   `python .claude/dev/packet_loop.py adr-song --root .`.
3. Xem các commit `master` mới (`git log --oneline 6f32aad..H^2`) có chạm hai tệp write set hay tương tác với nội dung mới không
   (ví dụ thêm dòng §20, đổi cổng mà dòng §20 mới trỏ tới, đổi `ADR-0055`/`ADR-0053`).

## Đầu ra

Ghi `VERDICT.md` (ghi đè; bản lượt 1 đã được chép ra `VERDICT-luot1.md`), mở đầu:

```
verdict: approve | changes_requested | blocked
reviewed_sha: e97d5d87f4f17c14fe350fb2fe56eddbd9301c9e
reviewed_tree: <tree đo được>
spec_sha256: <đo được>
```

rồi bảng lệnh kèm rc và dòng kết luận, finding `P1-L2-01`… nếu có (mức P0–P3, bằng chứng chạy được), những gì không đo được.
DÒNG CUỐI CÙNG của câu trả lời cuối của bạn (stdout) PHẢI đúng một trong:
`KET_LUAN: approve` · `KET_LUAN: changes_requested` · `KET_LUAN: blocked`.
