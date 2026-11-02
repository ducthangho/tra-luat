# Cross-review PR #1110 — ghi sổ cross-review Codex lượt 1 của PR #1075, lượt 2

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `3a3aac561ba359c08dfe92d95584b56494fc12d4`, đủ `refs/remotes/origin/*`.
  **Base = `fb74c6eca742205acc0af9bb7ea89da94f15aa21`** (merge-base với master). `git diff --name-only fb74c6e HEAD` chỉ được chạm
  `ops/reviews/**`. Hai commit nội dung: `f0c4ed6` (hiện vật) và `6af4c9a` (biên nhận + README); sau đó là hai merge commit đưa master
  vào nhánh (`e137f8c` và `3a3aac5`, không xung đột).
- Lượt 1 trên `e137f8c` approve 0/0/0/0 (`nguon/VERDICT-LUOT1.md`); Windows khi đó đỏ ở `p3b4_co_blob` (WinError 206) — lỗi của master,
  đã vá ở PR #1114 (merge `fb74c6e`, nay là base). `DIFF-OPS-REVIEWS-TU-LUOT1.patch` = `git diff e137f8c..HEAD -- ops/reviews` (phải RỖNG nếu
  hai merge không đổi hiện vật/biên nhận/README của PR).
- `DIFF.patch` = `git diff fb74c6e..HEAD`.
- `nguon/review1075a/` — bản sao thư mục sandbox GỐC của lượt review #1075 (PROMPT, VERDICT, launcher.json, launcher.err, runs/<id>/*,
  evidence/*, *.py, DIFF.patch; KHÔNG kèm cay-kho/, work/, nguon/ của nó). Đây là nguồn để kiểm "chép nguyên byte".

Thứ được ghi sổ: PR #1075 (merge `53d670c`, cha thứ hai `907c474`), lượt 1 trên `907c474` (approve). Tiền lệ cùng dạng:
`ops/reviews/pr1071-review-1-codex*` và `pr1058-review-*`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub chỉ kiểm được qua git tại chỗ
và các tệp; phần khác ghi KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. Cổng: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, các ca `t26_*`/`t27_*` của
   `ops/lease_publish_test.py` (gọi trực tiếp hàm), `python3 .claude/dev/packet_loop.py doctrine-scan --root .`,
   `git diff --check fb74c6e HEAD`. So head với base (delta). Đột biến: đổi một trường đo được của biên nhận mới (băm, reviewed_sha,
   evidence_url) trên bản sao tạm ⇒ cổng phải ĐỎ đúng tệp đó.
2. Byte: mỗi tệp trong `ops/reviews/pr1075-review-1-codex/` khớp byte với tệp tương ứng trong `nguon/review1075a/`
   (`launcher.out` ↔ `launcher.json`; `run/*` ↔ `runs/<id>/*`; `evidence/*.py` ↔ `*.py` gốc); bản phẳng `-verdict.md` khớp `VERDICT.md`;
   `SHA256SUMS` `sha256sum -c` sạch và phủ đủ tệp; mọi tệp nguồn VẮNG trong kho phải có trong `OMITTED.txt` với sha256/bytes đúng (kể cả
   `launcher.err` rỗng). Tìm tệp nguồn bị bỏ sót mà không khai.
3. Biên nhận `ops/reviews/pr1075-review-1-codex-verdict.receipt.yaml`: từng trường đo được (verdict + đếm P*, reviewed_sha và
   reviewed_tree, `land_merge_commit` và cha thứ hai, `evidence_url` neo commit tổ tiên của HEAD và blob băm đúng, run.json:
   run_id/ma_thoat/thời lượng/số sự kiện model/effort/prompt_sha256/sandbox_trang_thai, review_class qua `_tinh_lop_tu_write_set` trên
   diff `3574cb0..907c474`, và câu `ket_luan` so với verdict). Tìm lời khai không khớp nguồn hoặc rộng hơn phép đo, và lệch so tiền lệ
   pr1071 mà không có lý do.
4. README `ops/reviews/README.md`: 1 hàng mục lục + 3 hàng caveat khớp biên nhận; merge commit giữ nguyên MỌI hàng có sẵn trên
   master (so tập hàng `| ` của README tại base với tại HEAD: HEAD phải là base cộng đúng 4 hàng mới).

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 3a3aac561ba359c08dfe92d95584b56494fc12d4`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
