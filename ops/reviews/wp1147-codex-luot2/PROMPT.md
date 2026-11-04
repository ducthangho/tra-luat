# Cross-review Codex — packet #1147 (`CI-PROVENANCE-NEN-MOT-LAN`) revision 2 — lượt 2 (2/10)

Bạn là **reviewer độc lập, offline** cho Packet #1147, revision 2, generation 2 (lease `wp1147-r2-g2-claude`).
- Executor là Claude (họ `claude`); bạn là Codex (họ `openai`). Vì vậy `assurance_target` là `cross_approved`, `review_class` là `sensitive`.
- Không dùng mạng, không GitHub, không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao riêng dưới `OUT/`.
- Trần là 10 lời gọi; đây là lời gọi thứ 2.

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM rồi cập nhật dần. Dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo tới lúc đó.
KHÔNG chạy suite mặc định đầy đủ; executor chạy nó ở clone riêng.

## Ngưỡng hạng (như lượt 1)
- **P0/P1/P2:** bất kỳ điều nào sau đây.
  - Hạng đột biến khác base.
  - Khoá cache sai.
  - Bản gốc đỏ mà có mục không ra HONG.
  - Quá hạn bị xếp GIET hoặc SONG_SOT.
  - Ca cấp tín dụng giả hoặc kỳ vọng sai.
  - Ca mất răng: một phép kiểm trước đây đỏ nay không còn đỏ.
  - Hồi quy nghiệm thu.
- **P3:** thiếu độ phủ thuần tuý.

## Định danh (tự kiểm)
- `SRC` = `src/`, detached tại **`2344011617fa753adceef0be3306374cb3a096a1`**.
  - Đây là merge commit. Cha 1 là `f2176345f3d6cf564ad827f7648416b4cc488204` (r2), cha 2 là `origin/master` = `1f0941e9b`.
  - Chuỗi trên nhánh: `02ddeb4` (base r1) → `7295d5c` (r1, lượt 1 approve) → `f217634` (r2) → merge master → head.
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi.
- Đặc tả trong `tham-chieu/`. Băm lại cả hai:
  - r1 `wp1147.md`, sha256 `983d5490…46e0ba`;
  - r2 `wp1147-r2.md`, sha256 `b8f69631a070aab3effee8c40e21a7159964885363287f94e682c5e5afa2cd96`.
- Verdict lượt 1: `tham-chieu/luot1-VERDICT.md`.

## Lời khai executor (tự đo, đừng tin)
- `7295d5c` → `f217634` chỉ đổi `ops/ci_provenance_test.py`.
  - **M4** (`c62`): so reader với kỳ vọng TỪNG mục ngay khi đọc, nên bản đột biến dừng ở mục lệch đầu tiên. Thêm chốt `len(kq) == len(mong) == len(ca) + 1`.
  - **M5** (`c63`, vá P3 lượt 1): ba cặp (ca, nội dung) phân biệt, gọi lại cùng cặp, đòi đúng 3 lần chạy.
- Đột biến tay (Linux), đều cho rc 3 `DO:c63_`: bỏ ca khỏi khoá; bỏ nội dung khỏi khoá; gỡ cache; gỡ bắt quá hạn; cho bản gốc đỏ đi tiếp.
- Linux, 55 mục `c62` qua `chay_dot_bien`: 125.9 s → 75.8 s, 55/55 GIET.
- Merge master: diff `origin/master..HEAD` chỉ có `ops/ci_provenance_test.py` (+51/-9). Master không chạm write set.
- Lý do của r2: trên Windows thật (tra-luat-win), bộ mặc định của `7295d5c` mất 7745 s, vượt trần 5400 s.

## Việc (viết VERDICT sau mỗi bước)
1. Băm hai đặc tả. Xác nhận cha của merge. Đọc `git -C src diff 7295d5c f217634` và `git -C src diff 1f0941e9b HEAD`.
2. **M4 có giữ ngữ nghĩa không:**
   - Tập kỳ vọng, thứ tự, oracle Git native và mọi chốt sau vòng so có còn chạy trên head đúng không.
   - Một bản đột biến từng `GIET` có thể chuyển sang `TIN_DUNG_GIA` hoặc `HONG` vì dừng sớm không.
   - Thông báo `DO:c62_…` có còn chứa đủ tín hiệu không.
   - Chạy mọi mục `F13_*` (55) và `B2_*` (6) qua `chay_dot_bien` trên head; so hạng với base. Đo thời gian.
3. **M5:** P3 lượt 1 đã đóng thật chưa. Tái dựng đúng hai mutant của lượt 1 (`drop_case_from_key`, `drop_content_from_key`); cả hai phải ra rc 3.
4. **Tương đương hạng** trên mẫu đại diện của mọi ca đích, giống lượt 1. Kèm thêm `TU_KIEM`.
5. Bảng nghiệm thu: N1, N2, N4–N7 của r1, và N3′, N7 của r2. Phần nào không đo được thì ghi `not_measured`.
6. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy
`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` khi cần.

## Dạng verdict — `OUT/VERDICT.md`
- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: 2344011617fa753adceef0be3306374cb3a096a1`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự của r2>`.
- Bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`), và bảng nghiệm thu kèm rc cùng bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0**. Verdict chỉ neo commit trên; nó không cấp quyền push, merge hay land.

## Ngoài phạm vi
- `ops/ci_provenance.py`, `.claude/dev/ci_dang_ky_test.py`, `ci.yml`.
- Nợ `wp978-git-reader-differential-fuzz`.
- Windows native.
