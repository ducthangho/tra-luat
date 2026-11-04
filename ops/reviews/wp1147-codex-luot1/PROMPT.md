# Cross-review Codex — packet #1147 (`CI-PROVENANCE-NEN-MOT-LAN`) revision 1 — lượt 1 (1/10)

Bạn là **reviewer độc lập, offline** cho Packet #1147, revision 1, generation 1 (lease `wp1147-r1-g1-claude`).
Executor là Claude (họ `claude`); bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`.
Không mạng, không GitHub, không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao riêng dưới `OUT/`. Trần 10 lời gọi
(`ADR-0055`, dòng khai đầu đặc tả).

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
KHÔNG chạy suite mặc định đầy đủ (~20–40 phút); executor đã chạy, log ở `tham-chieu/suite-*-linux.txt`.

## Ngưỡng hạng
- **P0/P1/P2 (chặn approve):** bộ chạy đột biến cho kết quả SAI so với trước (một đột biến trước `GIET` nay khác, hoặc
  ngược lại); cache dùng sai khoá (bản gốc khác nhau dùng chung kết quả; ca khác nhau dùng chung); bản gốc đỏ mà mục nào
  không ra `HONG`; quá hạn bị xếp `GIET`/`SONG_SOT`; ca `c63` cấp tín dụng giả hoặc kỳ vọng sai; hồi quy nghiệm thu.
- **P3:** thiếu độ phủ thuần tuý (đột biến không tương đương còn sống mà hành vi vẫn đúng).

## Định danh (tự kiểm)
- `SRC` = `src/`, detached tại head ứng viên **`7295d5c7171267c8abf13b711108c315fe697b73`**, cha là base
  **`02ddeb4e9ea9c130d935adc4d5bce4f11db7d6a0`** (`refs/remotes/origin/master`). Định danh là **SHA**.
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi. Đặc tả `tham-chieu/wp1147.md` sha256
  `983d5490e6dadcb61c664c7dde8af44adb5f440161cbef37292f61bffd46e0ba`. Băm lại.

## Lời khai executor (tự đo)
- Diff base..head: 1 tệp `ops/ci_provenance_test.py`, +42/-7.
  - `chay_con` bắt `TimeoutExpired` ⇒ `(124, "QUA_HAN:<ca>…")`.
  - `nen_cua` cache `_NEN[(ca, sha256(bản gốc))]`; `chay_dot_bien` lấy bản gốc từ đó.
  - Ca mới `c63_ban_goc_mot_lan_moi_ca` (mock `chay_con`).
- Linux, cùng lệnh: base `CA 62/62 · DOT BIEN 398/398 · TONG DAT` trong 2269 s; head `CA 63/63 · 398/398 · DAT` trong 1152 s.
- Ba đột biến tay, đều rc 3 `DO:c63_`: gỡ cache (`if True:`); gỡ bắt `TimeoutExpired`; cho bản gốc đỏ đi tiếp.

## Việc (viết VERDICT sau mỗi bước)
1. Băm đặc tả; xác nhận SHA; đọc `git -C src diff 02ddeb4 7295d5c`.
2. **Tương đương phân hạng:** với MỌI mục `DOT_BIEN` và `TU_KIEM`, kết quả (hạng) của head phải bằng base. Không cần chạy
   suite đầy đủ: so log của executor. Đo độc lập bằng mẫu đại diện (ví dụ vài mục mỗi ca đích; đủ mọi ca đích nếu được) và
   so hạng head với base.
3. **Cache:** khoá có đủ không (ca, nội dung bản gốc)? Có trạng thái nào lọt giữa các mục (vd tệp tạm bị xoá trước khi mục
   sau dùng; `ra` của bản gốc dùng trong thông báo HONG)? Bản gốc đỏ ⇒ mọi mục HONG, đo được. Chạy `--mot-ca` (đường con)
   có bị cache ảnh hưởng không. `TU_KIEM` (classifier controls) có còn đúng không.
4. **Quá hạn:** 124 ⇒ `phan_hang` = HONG; không còn traceback sập bộ. Có đường nào rc 124 bị nhầm là GIET.
5. **`c63`:** có răng thật không (đột biến của bạn trên `nen_cua`/`chay_con`/`chay_dot_bien`); có phụ thuộc thứ tự `DOT_BIEN`
   ("2 mục đầu nhắm c34") theo cách dễ vỡ không; mock `__name__ + ".chay_con"` có đúng khi chạy qua `--mot-ca` và khi chạy
   bộ mặc định.
6. Bảng N1–N6 của đặc tả (N2, N3 Windows, N6 của bạn: `not_run`/`not_measured` nếu không đo).
7. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy
`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` khi cần.

## Dạng verdict — `OUT/VERDICT.md`
- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: 7295d5c7171267c8abf13b711108c315fe697b73`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- Bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`); bảng nghiệm thu kèm rc và bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi
`ops/ci_provenance.py` (sản phẩm); `.claude/dev/ci_dang_ky_test.py`; `ci.yml`; nợ `wp978-git-reader-differential-fuzz`;
Windows native (executor đo riêng).
