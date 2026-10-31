# Cross-review PR #1058 — ghi sổ land packet #1045 (biên nhận 3 lượt Codex + hồ sơ land PR #1047), lượt 1

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox.

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `5dd347c67da680099e292acf02da7e363a0559bd`, đủ `refs/remotes/origin/*` (gồm
  `origin/ops/wp1045-r1-g1-lease` mang lease + handoff). **Base = `afc82f6d7447eb76fc8adbe46c1be90be88d331f`** (merge-base với master).
  `git diff --name-only afc82f6 HEAD` chỉ được chạm `ops/reviews/**` và `ops/land/**`.
- `DIFF.patch` = `git diff afc82f6..HEAD`.

Thứ được ghi sổ: packet #1045 `CAI-CONG-CU-DAT-THEO-TRANG-THAI`, PR #1047 merge `b2d5f06` (head `2014602`). Hiện vật Codex gốc nằm
ở `ops/handoff/wp1045-g1-claude/` trên nhánh lease @ `4b4f37f`; lease rút hạn ở `a430543`.

Trước phép đo: `git config core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1`. Không có mạng: lời khai về GitHub (run/jobs/comment) chỉ
kiểm được qua tệp readback trong `ops/land/pr1047-wp1045-provenance/` — đối chiếu lời khai ↔ tệp, và nói rõ phần nào KHÔNG ĐO ĐƯỢC.

## Việc của bạn — ĐO, đừng đọc
1. Cổng: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`, các ca `t26_*`/`t27_*` của
   `ops/lease_publish_test.py` (gọi trực tiếp hàm), `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `git diff --check`.
   So head với base (delta).
2. Byte: mỗi `ops/reviews/wp1045-g1-codex-luot{n}/` và bản phẳng `-verdict.md` khớp byte với `ops/handoff/wp1045-g1-claude/luot{n}/`
   trên `origin/ops/wp1045-r1-g1-lease`; mọi `SHA256SUMS` (reviews + provenance) `sha256sum -c` sạch.
3. Biên nhận: từng trường có thể đo (verdict, đếm P*, reviewed_sha, tổ tiên của `b2d5f06`, `evidence_url` neo commit tổ tiên của HEAD,
   run.json: run_id/ma_thoat/thời lượng/số sự kiện model/prompt_sha256/sandbox_trang_thai, cửa sổ lease so `bat_dau_utc`). Tìm lời
   khai KHÔNG khớp nguồn.
4. Hồ sơ land `ops/land/pr1047-wp1045-land-evidence.yaml`: mỗi lời khai `measured` có nguồn trong provenance và nói ĐÚNG điều tệp
   nguồn nói (số job, nhãn, conclusion, SHA, thời điểm, lease_until, ai-dang-giu NGƯỜI_GIỮ). Kiểm `merge-va-diff.txt` bằng git tại chỗ.
   Kiểm `landed: false` và §8.1 `CHUA_DAT` có nhất quán với chính hồ sơ không; có câu nào khai mạnh hơn phép đo không.
5. README `ops/reviews/README.md`: hàng mục lục + caveat của wp1045 khớp biên nhận; merge `33118e0` giữ nguyên các hàng của PR #1050.

Hướng thử nào cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI, đừng tự dựng.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 5dd347c67da680099e292acf02da7e363a0559bd`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
