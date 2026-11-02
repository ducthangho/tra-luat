# Cross-review PR #1119 — ghi sổ 4 lượt cross-review Codex của PR #1110 (2 lượt) và PR #1114 (2 lượt), lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox (đột biến trên BẢN SAO tạm).

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `a8f74709578f3c68833d366ed80b66fc10fbf0a3`, đủ `refs/remotes/origin/*`.
  **Base = `f4b513da5802d439aedbe58ae4a5cd38ff47d6ab`** (merge-base với master). `git diff --name-only f4b513d HEAD` chỉ được chạm
  `ops/reviews/**`. Hai commit nội dung: `cf5acfa` (hiện vật 4 lượt) và `a8f7470` (4 biên nhận + README).
- `DIFF.patch` = `git diff f4b513d..HEAD`.
- `nguon/review1110a/`, `nguon/review1110b/`, `nguon/review1114a/`, `nguon/review1114b/` — bản sao thư mục sandbox GỐC của bốn lượt
  (PROMPT, VERDICT, launcher.json, launcher.err, runs/<id>/*, evidence/*, *.py, DIFF*.patch, bin/, probes/, nguon/<tệp> nếu có;
  KHÔNG kèm cay-kho/, work/, copies/ và các thư mục con của nguon/). Đây là nguồn để kiểm "chép nguyên byte".

Thứ được ghi sổ:
| Thư mục kho | Nguồn | PR | Lượt | reviewed_sha | Merge PR |
|---|---|---|---|---|---|
| `ops/reviews/pr1110-review-1-codex` | `nguon/review1110a` | #1110 | 1 | `e137f8c` | `f4b513d` (cha 2 = `3a3aac5`) |
| `ops/reviews/pr1110-review-2-codex` | `nguon/review1110b` | #1110 | 2 | `3a3aac5` | `f4b513d` |
| `ops/reviews/pr1114-review-1-codex` | `nguon/review1114a` | #1114 | 1 | `e101b11` | `fb74c6e` (cha 2 = `51435a4`) |
| `ops/reviews/pr1114-review-2-codex` | `nguon/review1114b` | #1114 | 2 | `51435a4` | `fb74c6e` |
Ánh xạ tệp: `launcher.out` ↔ `launcher.json`; `run/*` ↔ `runs/<id>/*`; `evidence/*.py` và `evidence/audit.gitconfig` ↔ tệp cùng tên ở gốc
sandbox; `bin/*` `probes/*` giữ đường dẫn; lượt 2: `diff-tu-luot1.patch` ↔ `DIFF-TU-LUOT1.patch`, `diff-ops-reviews-tu-luot1.patch` ↔
`DIFF-OPS-REVIEWS-TU-LUOT1.patch`, `verdict-cu/luot1-VERDICT.md` ↔ `nguon/VERDICT-LUOT1.md`, `nguon/repro_a11*.py` ↔ `nguon/repro_a11*.py`.
Tiền lệ cùng dạng: `ops/reviews/pr1058-review-{1,2}-codex*` (hai lượt một PR) và `pr1075-review-1-codex*`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub chỉ kiểm được qua git tại chỗ
và các tệp; phần khác ghi KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. Cổng: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, các ca `t26_*`/`t27_*` của
   `ops/lease_publish_test.py` (gọi trực tiếp hàm), `python3 .claude/dev/packet_loop.py doctrine-scan --root .`,
   `git diff --check f4b513d HEAD`. So head với base (delta). Đột biến: đổi một trường đo được của MỖI biên nhận mới (băm, reviewed_sha,
   evidence_url) trên bản sao tạm ⇒ cổng phải ĐỎ đúng tệp đó.
2. Byte: với mỗi thư mục, mỗi tệp khớp byte với nguồn theo ánh xạ trên; bản phẳng `-verdict.md` khớp `VERDICT.md`; `SHA256SUMS`
   `sha256sum -c` sạch và phủ đủ tệp; mọi tệp nguồn VẮNG trong kho phải có trong `OMITTED.txt` với sha256/bytes đúng (tệp >500 KB,
   `launcher.err` rỗng, `DIFF.patch` của #1110 — kiểm cả lời khai "tái lập bằng git diff"). Tìm tệp nguồn bị bỏ sót mà không khai.
3. Biên nhận `ops/reviews/pr111{0,4}-review-{1,2}-codex-verdict.receipt.yaml`: từng trường đo được (verdict + đếm P*, reviewed_sha/tree,
   `land_merge_commit` và cha thứ hai, quan hệ tổ tiên reviewed_sha → merge cho lượt 1, `evidence_url` neo `cf5acfa` là tổ tiên của HEAD
   và blob băm đúng, run.json: run_id/ma_thoat/thời lượng/số sự kiện model/effort/prompt_sha256/sandbox_trang_thai, review_class qua
   `_tinh_lop_tu_write_set` trên diff base..reviewed_sha của từng lượt, và câu `ket_luan` so với verdict). Tìm lời khai không khớp nguồn hoặc
   rộng hơn phép đo, và lệch so tiền lệ pr1058/pr1075 mà không có lý do. Caveat `SANDBOX-KHONG-DO-DUOC` phải khớp đúng các lượt có
   `sandbox_trang_thai KHONG_DO_DUOC`.
4. README `ops/reviews/README.md`: 4 hàng mục lục + 19 hàng caveat khớp biên nhận; so tập hàng `| ` của README tại base với tại HEAD:
   HEAD phải là base cộng đúng 23 hàng mới, không mất hàng nào.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: a8f74709578f3c68833d366ed80b66fc10fbf0a3`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
