# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r2 — lượt XÁC MINH (lượt 2/2 của phiên soạn)

Bạn là reviewer độc lập (provider OpenAI Codex), không sửa kho đang review.

## Đối tượng
- Mirror đầy đủ, không shallow: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv2/cay-kho`, detached tại reviewed_sha `735a0ef8480f62b9a5f003135ee5fcbf4bd0bd54`.
  `origin/master` trong mirror = `08bcb51f…` (master đã tiến sau khi soạn; các số đo của spec neo base `889334fb87c25136a13c6776a40a25b401820e04`, vẫn có trong mirror). Head đã merge master; diff spec không đổi do merge.
  Cây READ-ONLY: dùng `python -B`, PYTHONDONTWRITEBYTECODE=1, không tạo tệp trong đó.
- Tệp review: `ops/specs/wp1179-c1a1b-r2.md` (sha256 `04fa50683c44f3db093ab2396ebef7e0a12b88740eb35745da39c8016e9d108d`).
  So với r1 (`ops/specs/wp1179-c1a1b-r1.md`, sha256 `3dc6a2b9…6d04`): `git -C <mirror> diff --no-index` hai tệp hoặc diff thường.
- Verdict lượt 1 trên r1: `ops/specs/wp1179-c1a1b-r1-do/review-luot1/VERDICT.md` (F1–F5) và evidence/probe của lượt ấy chép ở `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv2/luot1-evidence`.
- Thư mục ghi được: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv2/sandbox`.

## Bối cảnh quyết định
Chủ kho chọn Review Rescue (A): r2 đổi phương pháp ở gốc lớp `phan-loai-vang-va-khong-do-duoc` (bảng đóng sự kiện × luật, G1 không gặp MOC ⇒ do), vá F1 (một trục ngân sách tính tiếp), F2 (G7/G8 tương thích producer: nhận symlink, so OID entry, khai giới hạn), F3 (ba tree khác nhau, A18 end-to-end, ma trận ok iff + byte stdout), F5. Duyệt nang_tran ≤2 tệp/≤750 dòng và một trục ngân sách. Ghi ở §0.3. Điều kiện: nếu lượt này còn finding thuộc `phan-loai-vang-va-khong-do-duoc` hoặc `dot-bien-tuong-duong-hoac-thieu` thì packet DỪNG và chuyển human audit — nên phán xét hai lớp ấy thật cẩn thận, không nới, không thổi phồng.

## Nhiệm vụ
1. Với TỪNG F1–F5: ĐÃ VÁ THẬT / VÁ MỘT PHẦN / CHƯA VÁ, kèm phép đo hoặc lập luận. Chạy lại các probe lượt 1 có liên quan (`/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv2/luot1-evidence` + các `probe_*.py` bạn tự viết lại nếu cần) trên r2.
2. Review theo LỚP (ADR-0060 M2) toàn bộ phần r2 thêm/đổi (§0.3, §2.2, §2.3 bảng đóng, §2.4 G1/G7/G8, §2.6, §3, §4 A4/A5/A7/A9/A11/A13/A16/A18/A20, §6–§10): tìm biểu hiện mới, kể cả mâu thuẫn nội tại giữa bảng đóng §2.3 và bảng G6/G7/G8, và giữa §8 với ADR-0055/ADR-0052/protocol §12.
3. Kiểm tính phân biệt của các đột biến mới khai (mỗi đột biến có làm ca đích đổi màu không). Prototype nhỏ trong sandbox được phép.
4. Đo lại S4 (4.360/64) trên base.
Hướng thử nào cần soạn nội dung dạng thoát thư mục thì mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv2/sandbox/VERDICT.md`: đầu tệp reviewed_sha, spec_sha256, model/effort tự khai, verdict `approve` | `changes_requested` | `blocked`; bảng F1–F5; bảng hai lớp; finding mới dạng `F<n>` (mức, slug lớp, vị trí, mô tả, phép đo lệnh/rc/output, đề xuất); dòng cuối `TONG: P1=<a> P2=<b> P3=<c>`.
