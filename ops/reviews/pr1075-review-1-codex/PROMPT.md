# Cross-review PR #1075 — ghi sổ cross-review Codex lượt 1 của PR #1071, lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `907c474e5dd22b2f389e8c342e7c79c6fbcb760e`, đủ `refs/remotes/origin/*`.
  **Base = `3574cb07dba8a8f7f32384ee3d1d3dfbf3a4f70e`** (merge-base với master). `git diff --name-only 3574cb0 HEAD` chỉ được chạm
  `ops/reviews/**`. Hai commit nội dung: `629543d` (hiện vật) và `16f9658` (biên nhận + README); sau đó là hai merge commit đưa master
  vào nhánh (`1907678` có giải xung đột README, `907c474`).
- `DIFF.patch` = `git diff 3574cb0..HEAD`.
- `nguon/review1071a/` — bản sao thư mục sandbox GỐC của lượt review #1071 (PROMPT, VERDICT, launcher.json, runs/<id>/*, evidence/*,
  *.py, DIFF.patch). Đây là nguồn để kiểm "chép nguyên byte".

Thứ được ghi sổ: PR #1071 (merge `0d79022`, cha thứ hai `0104461`), lượt 1 trên `0104461` (approve). Tiền lệ cùng dạng:
`ops/reviews/pr1058-review-{1,2}-codex*` và `pr1050-review-*`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub chỉ kiểm được qua git tại chỗ
và các tệp; phần khác ghi KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. Cổng: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, các ca `t26_*`/`t27_*` của
   `ops/lease_publish_test.py` (gọi trực tiếp hàm), `python3 .claude/dev/packet_loop.py doctrine-scan --root .`,
   `git diff --check 3574cb0 HEAD`. So head với base (delta). Đột biến: đổi một trường đo được của biên nhận mới (băm, reviewed_sha,
   evidence_url) trên bản sao tạm ⇒ cổng phải ĐỎ đúng tệp đó.
2. Byte: mỗi tệp trong `ops/reviews/pr1071-review-1-codex/` khớp byte với tệp tương ứng trong `nguon/review1071a/`
   (`launcher.out` ↔ `launcher.json`; `run/*` ↔ `runs/<id>/*`; `evidence/*.py` ↔ `*.py` gốc); bản phẳng `-verdict.md` khớp `VERDICT.md`;
   `SHA256SUMS` `sha256sum -c` sạch và phủ đủ tệp; mọi tệp nguồn VẮNG trong kho phải có trong `OMITTED.txt` với sha256/bytes đúng (kể cả
   `evidence/readme.diff`). Tìm tệp nguồn bị bỏ sót mà không khai.
3. Biên nhận `ops/reviews/pr1071-review-1-codex-verdict.receipt.yaml`: từng trường đo được (verdict + đếm P*, reviewed_sha và
   reviewed_tree, `land_merge_commit` và cha thứ hai, `evidence_url` neo commit tổ tiên của HEAD và blob băm đúng, run.json:
   run_id/ma_thoat/thời lượng/số sự kiện model/effort/prompt_sha256/sandbox_trang_thai, review_class qua `_tinh_lop_tu_write_set` trên
   diff `97120d3..0104461`, và câu `ket_luan` so với verdict). Tìm lời khai không khớp nguồn hoặc rộng hơn phép đo, và lệch so tiền lệ
   pr1058 mà không có lý do.
4. README `ops/reviews/README.md`: 1 hàng mục lục + 3 hàng caveat khớp biên nhận; hai merge commit giữ nguyên MỌI hàng có sẵn trên
   master (so tập hàng `| ` của README tại base với tại HEAD: HEAD phải là base cộng đúng 4 hàng mới).

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 907c474e5dd22b2f389e8c342e7c79c6fbcb760e`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
