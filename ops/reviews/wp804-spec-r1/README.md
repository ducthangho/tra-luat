# wp804 — đặc tả `HOAN-LOI-GOI-CODEX` r1: DỪNG, chưa duyệt băm

Đặc tả ở `ops/specs/HOAN-LOI-GOI-CODEX-r1.md` (sha256 `3ecd7f1350834a4f6672791a0bbf205d49048e49d8db217c91d8c1bf4b92fd2f`) **không được duyệt băm và
không có lease**. Không phiên nào được lấy nó làm căn cứ thi công.

Chủ kho quyết định dừng ngày 2026-11-18 (phiên điều phối #1206, qua AskUserQuestion), sau 3/10 lời gọi Codex review đặc tả,
trên master `aeb5cae0af01538c88ab2b50c27902dfaf7a7382`.

Lý do dừng:
- Để hoàn một lời gọi an toàn, phải chứng minh lời gọi đó chưa sinh output. Sau ba lượt review, chỉ còn hai ca chứng minh được:
  1. tiến trình bị ngắt trong lúc chụp workspace;
  2. hạn hết đúng trong lúc chụp.
  Cả hai đều xảy ra TRƯỚC khi sinh tiến trình codex.
- Hai hướng chứng minh còn lại đều bị bác vì reviewer đo được phản chứng:
  - Hướng "vắng khung response": reviewer đo được một bản ghi ký `xong`, `model_phuc_vu=[]` trong khi tiến trình con đã in output.
  - Điểm `_phong`: reviewer đo được `Popen` có thể ném lỗi SAU khi đã fork và tiến trình con đã chạy.
- Hệ quả là ca thực tế chính của #804 (codex đã chạy rồi chết vì quota hoặc vì quyền) vẫn không hoàn được. Đây là nợ
  `wp804-post-spawn-unrefundable`.
- Lượt 3 còn 1 P1 và 6 P2 (xem `luot3.verdict.txt`). Đóng hết chúng sẽ vượt trần 450 dòng của `ADR-0053`, nên phải tách hai packet:
  - A: launcher;
  - B: packet_loop, chỉ làm sau khi A land.
  Giá trị thực dụng thấp so với chi phí đó.
- Cửa bù ngân sách có người duyệt vẫn là `nang-tran`.

Nếu làm lại: bắt đầu từ bản 3 cộng các sửa F1–F7 trong `luot3.verdict.txt`, tách A/B như đề xuất ở đó, mỗi packet có đặc tả
và lượt review riêng.

Tệp trong thư mục:
- `dac-ta-ban1.md`, `dac-ta-ban2.md`: bản đặc tả đã được review ở lượt 1 và lượt 2.
- `prompt-luotN.md`: prompt của từng lượt.
- `luotN.stdout.txt`: toàn bộ output của Codex ở từng lượt.
- `luotN.verdict.txt`: phần verdict trích ra.
- Lượt 1 không có tệp verdict trích riêng; verdict nằm sau dòng `codex` cuối cùng trong `luot1.stdout.txt`.

Lệnh đã dùng cho mỗi lượt:

    codex exec --sandbox read-only --skip-git-repo-check -C <worktree master aeb5cae> "$(cat prompt-luotN.md)" < /dev/null
