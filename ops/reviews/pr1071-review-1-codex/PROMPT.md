# Cross-review PR #1071 — ghi sổ 2 lượt cross-review Codex của PR #1058, lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `01044616f0258e41608feac5b01f80770beec7a5`, đủ `refs/remotes/origin/*`.
  **Base = `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`** (merge-base với master). `git diff --name-only 97120d3 HEAD` chỉ được chạm
  `ops/reviews/**`. Head là merge commit `origin/master` vào nhánh; hai commit nội dung là `3145d82` (hiện vật) và `c92c709` (biên nhận +
  README).
- `DIFF.patch` = `git diff 97120d3..HEAD`.
- `nguon/review1058a/` và `nguon/review1058b/` — bản sao thư mục sandbox GỐC của hai lượt review #1058 (PROMPT, VERDICT, launcher.json,
  runs/<id>/*, evidence/*, *.py, DIFF.patch; lượt 2 thêm DIFF-LUOT2.patch, VERDICT-LUOT1.md). Đây là nguồn để kiểm "chép nguyên byte".

Thứ được ghi sổ: PR #1058 (merge `9c7dc11`, cha thứ hai `3534a6e`), lượt 1 trên `5dd347c` (request_changes), lượt 2 trên `3534a6e`
(approve). Tiền lệ cùng dạng: `ops/reviews/pr1050-review-{1,2}-codex*` và các biên nhận `pr1056-*`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub chỉ kiểm được qua git tại chỗ
và các tệp; phần khác ghi KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. Cổng: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, các ca `t26_*`/`t27_*` của
   `ops/lease_publish_test.py` (gọi trực tiếp hàm), `python3 .claude/dev/packet_loop.py doctrine-scan --root .`,
   `git diff --check 97120d3 HEAD`. So head với base (delta). Đột biến: đổi một trường đo được của biên nhận mới (băm, reviewed_sha,
   evidence_url) trên bản sao tạm ⇒ cổng phải ĐỎ đúng tệp đó.
2. Byte: mỗi tệp trong `ops/reviews/pr1058-review-{1,2}-codex/` khớp byte với tệp tương ứng trong `nguon/review1058{a,b}/`
   (`launcher.out` ↔ `launcher.json`; `run/*` ↔ `runs/<id>/*`; `evidence/*.py` ↔ `*.py` gốc; `diff-tu-luot1.patch` ↔ `DIFF-LUOT2.patch`;
   `verdict-cu/luot1-VERDICT.md` ↔ `VERDICT-LUOT1.md`); bản phẳng `-verdict.md` khớp `VERDICT.md`; `SHA256SUMS` `sha256sum -c` sạch và
   phủ đủ tệp; mọi tệp nguồn VẮNG trong kho phải có mặt trong `OMITTED.txt` với sha256/bytes đúng (kể cả `evidence/gates-summary.log`).
   Tìm tệp nguồn bị bỏ sót mà không khai.
3. Biên nhận `ops/reviews/pr1058-review-{1,2}-codex-verdict.receipt.yaml`: từng trường đo được (verdict + đếm P* so verdict, reviewed_sha
   và reviewed_tree, quan hệ tổ tiên với `9c7dc11`, `land_merge_commit` và cha thứ hai, `evidence_url` neo commit tổ tiên của HEAD và blob
   băm đúng, run.json: run_id/ma_thoat/thời lượng/số sự kiện model/effort/prompt_sha256/sandbox_trang_thai, review_class qua
   `_tinh_lop_tu_write_set` trên diff `afc82f6..reviewed_sha`). Tìm lời khai KHÔNG khớp nguồn hoặc rộng hơn phép đo, và lệch so tiền lệ
   pr1050 mà không có lý do.
4. README `ops/reviews/README.md`: 2 hàng mục lục + 7 hàng caveat khớp biên nhận (id caveat, số đếm, head, bytes); merge `0104461` giữ
   nguyên các hàng có sẵn trên master.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 01044616f0258e41608feac5b01f80770beec7a5`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
