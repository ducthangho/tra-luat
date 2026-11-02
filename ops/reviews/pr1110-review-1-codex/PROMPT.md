# Cross-review PR #1110 — ghi sổ cross-review Codex lượt 1 của PR #1075, lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `e137f8ce1215e0e6a6c8fbc1aa949b31fa2e4e7d`, đủ `refs/remotes/origin/*`.
  **Base = `c6dd7b33b4f215809bf281ee1533bc1e8fa6920c`** (merge-base với master). `git diff --name-only c6dd7b3 HEAD` chỉ được chạm
  `ops/reviews/**`. Hai commit nội dung: `f0c4ed6` (hiện vật) và `6af4c9a` (biên nhận + README); sau đó là một merge commit đưa master
  vào nhánh (`e137f8c`, không xung đột).
- `DIFF.patch` = `git diff c6dd7b3..HEAD`.
- `nguon/review1075a/` — bản sao thư mục sandbox GỐC của lượt review #1075 (PROMPT, VERDICT, launcher.json, launcher.err, runs/<id>/*,
  evidence/*, *.py, DIFF.patch; KHÔNG kèm cay-kho/, work/, nguon/ của nó). Đây là nguồn để kiểm "chép nguyên byte".

Thứ được ghi sổ: PR #1075 (merge `53d670c`, cha thứ hai `907c474`), lượt 1 trên `907c474` (approve). Tiền lệ cùng dạng:
`ops/reviews/pr1071-review-1-codex*` và `pr1058-review-*`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub chỉ kiểm được qua git tại chỗ
và các tệp; phần khác ghi KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. Cổng: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, các ca `t26_*`/`t27_*` của
   `ops/lease_publish_test.py` (gọi trực tiếp hàm), `python3 .claude/dev/packet_loop.py doctrine-scan --root .`,
   `git diff --check c6dd7b3 HEAD`. So head với base (delta). Đột biến: đổi một trường đo được của biên nhận mới (băm, reviewed_sha,
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
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: e137f8ce1215e0e6a6c8fbc1aa949b31fa2e4e7d`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
