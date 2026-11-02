# Cross-review PR #1131 — ghi sổ 2 lượt cross-review Codex của PR #1119 (+ 1 lượt hỏng vì hết đĩa), lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox (đột biến trên BẢN SAO tạm).

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `0e824fe4c1ac674081c93c6f2098e5433c932890`, đủ `refs/remotes/origin/*`.
  **Base = `180039c4b791fba4c89991623151cbb7378fce53`** (merge-base với master). `git diff --name-only 180039c HEAD` chỉ được chạm
  `ops/reviews/**`. Hai commit nội dung: `9105a1a` (hiện vật) và `0e824fe` (2 biên nhận + README).
- `DIFF.patch` = `git diff 180039c..HEAD`.
- `nguon/review1119a/` (lượt HỎNG vì hết đĩa, run e9bd8492), `nguon/review1119b/` (lượt 1), `nguon/review1119c/` (lượt 2) — bản sao thư mục
  sandbox GỐC (PROMPT, VERDICT, launcher.json, launcher.err, runs/<id>/*, evidence/*, *.py, audit.gitconfig, DIFF*.patch, nguon/<tệp>;
  KHÔNG kèm cay-kho/, work/ và các thư mục con của nguon/). Nguồn để kiểm "chép nguyên byte".

Thứ được ghi sổ:
| Thư mục kho | Nguồn | Lượt | reviewed_sha | Verdict |
|---|---|---|---|---|
| `ops/reviews/pr1119-review-1-codex` | `nguon/review1119b` | 1 | `a8f7470` | request_changes 0/0/0/2 |
| `ops/reviews/pr1119-review-1-codex/luot-hong-dia` | `nguon/review1119a` | (không tính) | `a8f7470` | VERDICT tạm, hết đĩa |
| `ops/reviews/pr1119-review-2-codex` | `nguon/review1119c` | 2 | `8715ac9` | approve 0/0/0/0 |
Merge PR #1119 = `180039c` (cha thứ hai = `8715ac9`). Ánh xạ tệp: `launcher.out` ↔ `launcher.json`; `run/*` ↔ `runs/<id>/*`;
`evidence/*.py`, `evidence/audit.gitconfig` ↔ tệp cùng tên ở gốc sandbox; lượt 2: `diff-ops-reviews-tu-luot1.patch` ↔
`DIFF-OPS-REVIEWS-TU-LUOT1.patch`, `verdict-cu/luot1-VERDICT.md` ↔ `nguon/VERDICT-LUOT1.md`. Tiền lệ: `ops/reviews/pr1058-review-{1,2}-codex*`
(lượt 1 changes_requested ⇒ `cross_reviewed`) và `pr1110-review-*`/`pr1114-review-*`.

Lời khai cần KIỂM: VERDICT.md lượt 2 kết thúc bằng một dòng trống và được giữ nguyên byte; executor khai đường nhanh CI chạy
`git diff --check` với `core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab` (`ops/ci_duong_nhanh.py`) nên không đỏ. Đo bằng chính
hàm/cấu hình đó, và tìm xem có cổng nào KHÁC (ci.yml, gate, selftest) chạy `--check` nghiêm hơn trên PR này không.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub chỉ kiểm được qua git tại chỗ
và các tệp; phần khác ghi KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. Cổng: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, các ca `t26_*`/`t27_*` của
   `ops/lease_publish_test.py` (gọi trực tiếp hàm), `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `git diff --check` dưới cấu hình
   CI ở trên (và ghi cả kết quả `--check` mặc định). So head với base (delta). Đột biến: đổi một trường đo được của MỖI biên nhận mới
   trên bản sao tạm ⇒ cổng phải không xanh đúng tệp đó.
2. Byte: mỗi tệp trong hai thư mục (và `luot-hong-dia/`) khớp byte với nguồn theo ánh xạ; bản phẳng `-verdict.md` khớp `VERDICT.md`;
   `SHA256SUMS` `sha256sum -c` sạch và phủ đủ tệp; mọi tệp nguồn VẮNG trong kho phải có trong `OMITTED.txt` (của thư mục tương ứng) với
   sha256/bytes đúng, kể cả lời khai "tái lập bằng git diff". Tìm tệp nguồn bị bỏ sót mà không khai, KỂ CẢ trong thư mục con của evidence/.
3. Biên nhận `ops/reviews/pr1119-review-{1,2}-codex-verdict.receipt.yaml`: từng trường đo được (verdict/assurance/đếm P*/findings_ids so
   verdict; reviewed_sha/tree; `land_merge_commit` và cha thứ hai; tổ tiên reviewed_sha → merge cho lượt 1; `evidence_url` neo `9105a1a` là tổ
   tiên của HEAD và blob băm đúng; run.json: run_id/ma_thoat/thời lượng/số sự kiện/model/effort/prompt_sha256/sandbox_trang_thai;
   review_class qua `_tinh_lop_tu_write_set` trên diff base..reviewed_sha; `xu_ly_finding` lượt 1 khớp commit vá `6379bc5`; caveat
   `LUOT-HONG-DIA-KHONG-TINH` khớp run e9bd8492). Tìm lời khai không khớp nguồn hoặc rộng hơn phép đo, và lệch tiền lệ không lý do.
4. README `ops/reviews/README.md`: 2 hàng mục lục + 8 hàng caveat khớp biên nhận; so tập hàng `| ` tại base với HEAD: HEAD = base + đúng
   10 hàng mới, không mất hàng nào.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 0e824fe4c1ac674081c93c6f2098e5433c932890`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
