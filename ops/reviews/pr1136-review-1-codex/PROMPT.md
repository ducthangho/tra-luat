# Cross-review PR #1136 — ghi sổ cross-review Codex lượt 1 của PR #1131 (+ 1 lượt hỏng xác thực), lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox (đột biến trên BẢN SAO tạm).

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `1a87a863174ef104b2df8bc98b77724fb6796d9b`, đủ `refs/remotes/origin/*`.
  **Base = `62e629156fd0729b743f15eed2f32487786b9adc`** (merge-base với master). `git diff --name-only 62e6291 HEAD` chỉ được chạm
  `ops/reviews/**`. Hai commit nội dung: `62a30b1` (hiện vật) và `1a87a86` (biên nhận + README).
- `DIFF.patch` = `git diff 62e6291..HEAD`.
- `nguon/review1131a/` (lượt HỎNG xác thực, run ee42b27f, rc=1, không VERDICT) và `nguon/review1131b/` (lượt tính, run 260f271e) — bản
  sao thư mục sandbox GỐC (PROMPT, VERDICT, launcher.json, launcher.err, runs/<id>/*, evidence/*, *.py, audit.gitconfig, DIFF.patch;
  KHÔNG kèm cay-kho/, work/, nguon/). Nguồn để kiểm "chép nguyên byte".

Thứ được ghi sổ:
| Thư mục kho | Nguồn | Lượt | reviewed_sha | Verdict |
|---|---|---|---|---|
| `ops/reviews/pr1131-review-1-codex` | `nguon/review1131b` | 1 | `0e824fe` | approve 0/0/0/0 |
| `ops/reviews/pr1131-review-1-codex/luot-hong-xac-thuc` | `nguon/review1131a` | (không tính) | `0e824fe` | không có VERDICT (401) |
Merge PR #1131 = `2609cd8` (cha thứ hai = `0e824fe`). Ánh xạ tệp: `launcher.out` ↔ `launcher.json`; `run/*` ↔ `runs/<id>/*`;
`evidence/*.py`, `evidence/audit.gitconfig` ↔ tệp cùng tên ở gốc sandbox. Tiền lệ: `ops/reviews/pr1119-review-*` (kể cả `luot-hong-dia/`).

Lời khai cần KIỂM: `evidence/gates-progress.txt` có khoảng trắng cuối dòng và được giữ nguyên byte; executor khai đường nhanh CI chạy
`git diff --check` với `core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab` (`ops/ci_duong_nhanh.py`) nên không đỏ. Đo bằng chính
cấu hình đó, và tìm cổng nào KHÁC chạy `--check` nghiêm hơn trên PR này.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub chỉ kiểm được qua git tại chỗ
và các tệp; phần khác ghi KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. Cổng: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, các ca `t26_*`/`t27_*` của
   `ops/lease_publish_test.py` (gọi trực tiếp hàm), `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `git diff --check` dưới cấu hình
   CI (và ghi kết quả `--check` mặc định). So head với base (delta). Đột biến: đổi một trường đo được của biên nhận mới trên bản sao tạm ⇒
   cổng phải không xanh đúng tệp đó.
2. Byte: mỗi tệp trong thư mục (và `luot-hong-xac-thuc/`) khớp byte với nguồn theo ánh xạ; bản phẳng `-verdict.md` khớp `VERDICT.md`;
   `SHA256SUMS` `sha256sum -c` sạch và phủ đủ tệp; mọi tệp nguồn VẮNG trong kho phải có trong `OMITTED.txt` (của thư mục tương ứng) với
   sha256/bytes đúng, kể cả lời khai "tái lập bằng git diff". Tìm tệp nguồn bị bỏ sót mà không khai, KỂ CẢ trong thư mục con.
3. Biên nhận `ops/reviews/pr1131-review-1-codex-verdict.receipt.yaml`: từng trường đo được (verdict/assurance/đếm P*; reviewed_sha/tree;
   `land_merge_commit` và cha thứ hai; `evidence_url` neo `62a30b1` là tổ tiên của HEAD và blob băm đúng; run.json: run_id/ma_thoat/thời
   lượng/số sự kiện/model/effort/prompt_sha256/sandbox_trang_thai; review_class qua `_tinh_lop_tu_write_set` trên diff `180039c..0e824fe`;
   caveat `LUOT-HONG-XAC-THUC-KHONG-TINH` khớp run ee42b27f; câu `ket_luan` so với verdict). Tìm lời khai không khớp nguồn hoặc rộng hơn
   phép đo, và lệch tiền lệ không lý do.
4. README `ops/reviews/README.md`: 1 hàng mục lục + 4 hàng caveat khớp biên nhận; so tập hàng `| ` tại base với HEAD: HEAD = base + đúng
   5 hàng mới, không mất hàng nào.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 1a87a863174ef104b2df8bc98b77724fb6796d9b`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
