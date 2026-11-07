# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r3 — lượt 3 (vòng lặp tới khi sạch)

Bạn là reviewer độc lập (provider OpenAI Codex), không sửa kho đang review.

## Đối tượng
- Mirror đầy đủ, không shallow: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv3/cay-kho`, detached tại reviewed_sha `0924f4f69b26728a29faa970d1660aff6dc176ad`.
  `origin/master` trong mirror = `d26b36f5…`; số đo spec neo base `889334fb87c25136a13c6776a40a25b401820e04` (và `08bcb51f…` cho §11), cả hai có trong mirror.
  READ-ONLY: `python -B`, PYTHONDONTWRITEBYTECODE=1, không tạo tệp trong cây.
- Tệp review: `ops/specs/wp1179-c1a1b-r3.md` (sha256 `779f9384cf87aacd9bbe3c5737c9585ef4c408178df8fc7b4c3121fa31aab039`).
  Lịch sử: r1, r2 cùng thư mục; verdict lượt 1 (trên r1) và lượt 2 (trên r2) ở `ops/specs/wp1179-c1a1b-r1-do/review-luot1/` và `.../review-luot2-r2/` (kèm evidence + probe đã chạy). Hồ sơ `.../ho-so-luot2.md`.
- Thư mục ghi được: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv3/sandbox`.

## Bối cảnh
Chủ kho đổi hướng (#1179 comment 6686369822): không human audit; lặp vá spec, mỗi vòng một lượt Codex độc lập, tới khi MỘT lượt cho 0 P1 / 0 P2 / 0 P3. Trần lời gọi nâng 10→16; pha spec tối đa 4 lượt (lượt này là lượt 3). Quyết định giữ: trần kích thước thi công ≤2 tệp/≤750 dòng; F6 theo nhánh "so OID trước"; phạm vi C1a1b (C1a2, C1b, #656, #564, #1160 ngoài phạm vi). Spec chưa ghi nâng trần 16 (ghi ở comment trên); đó KHÔNG là finding của r3 nếu chỉ vì chưa phản ánh quyết định ra sau commit — nhưng nếu phần ngân sách của r3 sai/khai rộng hơn phép đo ở thời điểm của nó thì vẫn là finding.

## Nhiệm vụ
1. Xác minh F6, F7, F8 của lượt 2 đã vá thật trên r3 (chạy lại/viết lại probe lượt 2 cần thiết). Phán xét riêng: VÁ THẬT / MỘT PHẦN / CHƯA.
2. Review TOÀN BỘ r3 theo LỚP (ADR-0060 M2) — không chỉ phần đổi: hợp đồng ABI/rc, bảng đóng §2.3 × bảng G6/G7/G8, tham số/N6, ngân sách §2.6, write set §3, mọi tiêu chí A1–A20 (oracle có phân biệt không, đột biến có đổi màu đúng ca đích không, ca có đo thật không), §8/§11 so với ADR-0055/0052/protocol §12, nội nhất quán giữa các mục. Mọi biểu hiện, kể cả P3.
3. Đo lại các con số có thể đo. Prototype nhỏ trong sandbox được phép; ghi lệnh/rc/output.
Hướng thử nào cần soạn nội dung dạng thoát thư mục thì mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv3/sandbox/VERDICT.md`: đầu tệp reviewed_sha, spec_sha256, model/effort tự khai, verdict `approve` | `changes_requested` | `blocked`; bảng F6–F8; bảng lớp; finding mới `F<n>` (đánh số tiếp từ F9; mức, slug lớp, vị trí, mô tả, phép đo lệnh/rc/output, đề xuất sửa cụ thể); dòng cuối `TONG: P1=<a> P2=<b> P3=<c>`. Chỉ `approve` khi 0/0/0.
