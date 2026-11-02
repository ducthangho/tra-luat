# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 2 — lượt 9 (lời gọi 9/10)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 2, generation 2 (lease `wp978-r2-g2-claude`).
Executor là Claude (họ `claude`); bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`,
`review_class: sensitive`. Không mạng, không GitHub, không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao
riêng dưới `OUT/`. Trần 10 lời gọi theo `ADR-0055` (dòng khai của spec r2); đây là lời gọi 9, còn đúng 1 sau lượt này.

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
KHÔNG chạy suite mặc định đầy đủ (~40 phút); executor chạy nó trên clone riêng của đúng head và sẽ báo số.

## Ngưỡng hạng (quyết định chủ kho #978 issuecomment-6445001458, giữ từ lượt 8)

- **P1/P2 (chặn approve):** lỗi SẢN PHẨM — `git_cuc_bo` trả sai so với Git native hoặc sai M1 trên commit Git HỢP LỆ;
  vi phạm hợp đồng (ném ngoại lệ); hồi quy tiêu chí nghiệm thu; ca/đột biến cấp TÍN DỤNG GIẢ hoặc kỳ vọng test SAI;
  bộ chạy đột biến trả `HONG` cho mục nào (đó là lỗi P1 connector vừa bắt).
- **P3 (không chặn nhưng phải liệt kê):** đột biến không tương đương còn sống mà sản phẩm vẫn đúng. Nợ có tên
  `wp978-git-reader-differential-fuzz`, owner `ducthangho`. Ghi P3 nào ĐÃ đóng / còn mở.

## Định danh (tự kiểm)

- `SRC` = `src/`, detached tại head ứng viên **`aebc808ea45408c827e753827b97f94689969db5`** (lệch thì ghi và dừng).
  `refs/remotes/origin/master` trỏ base mới **`9091cf52cf20ac197c1a356d6a33cac6bab0b318`**. Định danh là **SHA**.
- Chuỗi từ lượt 8 (approve `53ec046`): `53ec046` → `1a27c96` (merge master, miễn review) → `8cfc2a0` (fixture tag
  bằng `hash-object -t tag`, miễn review) → `28b542a` (**CHƯA từng được review offline**: S01/S02 của lượt 8 + test
  vi sai ngẫu nhiên seed 978, 150 commit) → `e5ca45b` (merge master `9091cf5`) → `aebc808` (đổi tên ca r2).
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi.
- Đặc tả: `tham-chieu/specs-wp978-r2.md` sha256 `9fe94ad05cc1129e663cf77706db92685d6130c08c6a375454781a9aca188060`
  (r2, chỉ thay N1–N3 và Q1/Q4) và `tham-chieu/specs-wp978.md` (r1, sha256 `eccd6dd2…1638`). Băm lại.
- Verdict lượt 8: `tham-chieu/wp978-g1-codex-luot8-VERDICT.md`.

## Lời khai executor (tự đo, đừng tin)

- `e5ca45b` → `aebc808` chỉ đổi `ops/ci_provenance_test.py`, +40/-40: `def c53_git_commit_khong_utf8` →
  `def c62_git_commit_khong_utf8`, ca đích của 39 mục `F13_*` từ `"c53"` sang `"c62"`. `B2_*` và `c53_wd_passed` của
  master KHÔNG đổi. `ops/ci_provenance.py` không đổi.
- `grep -c '^def c53_'` = 1, `grep -c '^def c62_'` = 1. `--mot-ca c62_git_commit_khong_utf8` rc 0; với
  `CI_PROVENANCE_MA=<ops/ci_provenance.py tại c8d92ba>` in `DO:c62_git_commit_khong_utf8:git_cuc_bo … UnicodeDecodeError`.
- Diff `9091cf5..aebc808`: đúng 2 tệp, `ops/ci_provenance.py` +22/-6, `ops/ci_provenance_test.py` +147/-0. Ruff F 0/0.

## Việc (viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận chuỗi commit; đọc `git -C src diff 9091cf5 aebc808`, `git -C src diff e5ca45b aebc808`
   và `git -C src show 28b542a`.
2. **Bộ chạy đột biến:** với từng mục `DOT_BIEN` có ca đích `c62` hoặc `c53`, xác nhận tiền tố khớp ĐÚNG MỘT ca (không
   còn `HONG`), F13_* GIET đúng `c62`, B2_* GIET đúng `c53` (`c53_wd_passed`). Chạy từng mutant theo lệnh của bộ test
   (xem `--help`/mã nguồn). Kiểm không tiền tố ca nào khác trong tệp còn trùng (vd hai ca cùng `cNN_`).
3. **`28b542a` (chưa review):** test vi sai ngẫu nhiên có tất định không (seed cố định), có thật sự so với Git native
   không, có thể chết vì lý do vô can (tín dụng giả) hay phụ thuộc môi trường (danh tính git, config toàn cục,
   CRLF, phiên bản git) không; thời gian chạy có hợp lý cho CI không; S01/S02 có được khoá không.
4. **Sản phẩm:** diff `ops/ci_provenance.py` so master có đổi gì từ `53ec046` không (phải giống blob lượt 8 đã approve,
   trừ phần do master mang vào). Tìm lỗi sản phẩm theo ngưỡng trên.
5. **Merge master:** `e5ca45b` có làm hỏng gì trong hai tệp (xung đột giải sai, ca master bị mất) không — so phần
   của master trong hai tệp với `9091cf5`.
6. Bảng N1′–N3′ (r2) và N4–N7 (r1): N3′ của bạn là `not_run`; N6 `not_measured`; N7 không áp dụng.
7. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`
khi muốn mô phỏng runner CI không có danh tính git.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: aebc808ea45408c827e753827b97f94689969db5`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự của spec r2>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC`; bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`); mỗi P3 ghi nợ có tên, owner,
  hướng xử lý; bảng nghiệm thu kèm rc và bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

D02 và F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native;
nội dung của master ngoài hai tệp write set.
