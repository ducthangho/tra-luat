# Cross-review PR #1114 — lượt 2: thêm vá a11 (chờ có hạn trong `_song_roi_don`)

Bạn là reviewer KHÁC HỌ (OpenAI Codex), executor là Claude. ĐỘC LẬP: chỉ tin phép đo của chính bạn. KHÔNG sửa kho; chỉ ghi trong
sandbox (đột biến trên BẢN SAO tạm).

## Đầu vào trong sandbox
- `cay-kho/` — clone, detached ở head ứng viên `51435a44659c4026539497a47ace971a71a64f40`, đủ `refs/remotes/origin/*`. Base = `3bdd9877cab2543adc413a32a47decbb585ded97` (merge-base với master).
  `git diff --name-only 3bdd987 HEAD` chỉ được chạm `ops/cloud_agent_creds_test.py`.
- `DIFF.patch` = `git diff 3bdd987..HEAD`. `DIFF-TU-LUOT1.patch` = phần đổi so với head lượt 1 `e101b11` (lượt 1 approve 0/0/0/0, verdict ở
  `nguon/VERDICT-LUOT1.md`; phần stdin/WinError 206 đã được đo ở đó — chỉ cần xác nhận không hồi quy).
- `nguon/repro_a11.py` (đo trước vá) và `nguon/repro_a11_va.py` (cùng phép đo, thêm chờ 5 s) — script tái hiện của executor. Cách chạy:
  `python3 nguon/repro_a11.py <đường-dẫn-cây> <số-vòng>`; executor chạy 12 bản song song × 150 vòng.

## Lời khai của executor (KIỂM, đừng nhận)
CI lượt `41289534297` đỏ: khi bộ đột biến chạy lại `a11_subreaper_va_esrch` làm nền, nhánh `sr=False` báo `sống [7591]`. Lời khai: `_giet_nhom` với
`_SUBREAPER=False` trả ngay sau `communicate()` (ống đóng khi cháu nhả fd, TRƯỚC khi cháu thành zombie), nên `_con_song` có thể thấy cháu ở trạng
thái R. Tái hiện dưới tải: 34/1800 trước vá, 0/1800 với chờ 5 s. Vá: `_song_roi_don(pids, cho_chet=5.0)` chờ có hạn; a9 (cần con/cháu CÒN sống)
gọi `cho_chet=0`. Đột biến bỏ `killpg` trong `ops/cloud_agent_creds.py` vẫn làm a11 và a4 ĐỎ (rc=3).

## Việc của bạn — ĐO
1. `PYTHONDONTWRITEBYTECODE=1 python3 ops/cloud_agent_creds_test.py` trên head và base (bản sao riêng): CA, ĐỘT BIẾN, TONG; delta.
2. Tái hiện cơ chế: chạy hai script repro (có thể giảm số vòng nhưng phải có tải song song). Ghi số đo. Nếu không tái hiện được thì nói rõ và đánh
   giá lời khai cơ chế bằng cách khác (đọc trạng thái `/proc/<pid>/stat` ngay sau `_giet_nhom`).
3. Chờ 5 s có che lỗi thật không? Đột biến trên bản sao: (a) bỏ `killpg` (thay bằng `p.kill()`); (b) bỏ toàn bộ việc giết trong `_giet_nhom`; (c) đổi
   `cho_chet=0` của a9 thành mặc định. Mỗi đột biến: ca nào ĐỎ/XANH, thời gian. Có ca nào giờ cần cháu chết trong <5 s mà vá làm mất răng không?
4. Các lời gọi `_song_roi_don` khác (a4, b10): khẳng định của chúng còn đo đúng điều cũ không. Thời gian suite tăng bao nhiêu.
5. `python3 -m ruff check --select F ops/cloud_agent_creds_test.py`; `git diff --check 3bdd987 HEAD`.

## Đầu ra — ghi TĂNG DẦN vào `VERDICT.md` trong sandbox
Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`. Dòng 2: `Reviewed commit: 51435a44659c4026539497a47ace971a71a64f40`.
Rồi: tóm tắt, bảng finding `- [P0..P3] <slug>: <vị trí> — <lệnh tái hiện> — <output> — <hướng vá>`.
Ngưỡng approve: không P0/P1/P2/P3. Mỗi khẳng định kèm lệnh và output; không đo được thì `KHÔNG ĐO ĐƯỢC`. Không tự khai bề mặt chạy
của chính bạn. Không cấp quyền merge/land.
