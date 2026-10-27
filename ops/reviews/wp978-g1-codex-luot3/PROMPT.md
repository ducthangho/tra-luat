# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 1 — lượt 3 (lời gọi 3/4)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context
executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa mã nguồn trong `SRC`; mọi phép thử chạy trên
**bản sao riêng** dưới `OUT/`. Trần lời gọi đã được chủ kho nâng từ 2 lên 4 (ghi hộ ở #978 issuecomment-6441085134).

**Ưu tiên kết luận.** Lượt 2 bị cắt `rc=1` trước khi ra kết luận và mất trọn verdict. Vì vậy hãy viết `OUT/VERDICT.md`
SỚM và cập nhật dần: dòng 1 phải luôn là kết luận tốt nhất hiện có theo bằng chứng đã đo, không để "đang kiểm". Không chạy
suite mặc định đầy đủ (~40 phút); executor tự chạy nó.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = `src/` cạnh tệp prompt này, detached tại head ứng viên **`fdf1f05c1b3d845a694c796a81a8bd5c218a68c8`**
  (kiểm `git -C src rev-parse HEAD`; lệch thì ghi và dừng). Chuỗi: base **`c8d92ba05c3ea875d8f84d94195430302690286d`**
  → `bef14035718cae862369101f79dc61e938ae6b00` (lượt 1) → `7fcfe18181ce4d089225900e36d3aed878877e7f` (lượt 2) → head.
  `refs/remotes/origin/master` trong clone trỏ base. Thứ định danh tệp là **băm/SHA**.
- `OUT` = `out/` cạnh tệp prompt này, nơi DUY NHẤT bạn ghi.
- Đặc tả `tham-chieu/wp978.md`, sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638`. Băm lại.
- Lease (bản chép) `tham-chieu/lease-wp978-r1-g1-claude.yaml`.
- Verdict lượt 1: `tham-chieu/luot1-VERDICT.md` (+ script `tham-chieu/luot1/`). Bản TẠM lượt 2 (không phải verdict):
  `tham-chieu/luot2-VERDICT-TAM.md`, mutant mới của lượt 2 `tham-chieu/luot2/new-mutants/X01…X11.py` (bản sao TOÀN tệp
  `ops/ci_provenance.py` tại `7fcfe18` đã đột biến), `new-survivors-all-cases.json`, `wrapper-analysis.json`.

## Lời khai của executor (tự đo, đừng tin)

Thay đổi duy nhất từ `7fcfe18` → `fdf1f05` là `ops/ci_provenance_test.py`:
- Đóng 5 mutant sống của lượt 2 bằng tiêm đầu ra/lỗi `subprocess.run` (stdout rỗng; header thừa trường trên đầu ra THẬT;
  thân cụt 2 byte; `TimeoutExpired`) và sha `"\udc80"` (UnicodeEncodeError). Thêm 5 mục `DOT_BIEN` tương ứng.
- Bộ bọc `doc()` trong `c53`: chỉ đổi ngoại lệ thành giá trị `NEM:<lớp>` khi traceback đi qua khung `git_cuc_bo`
  (vi phạm hợp đồng không-ném của reader — `main` không bắt); lỗi không qua khung ấy ném tiếp ⇒ rc 4 / vô can.
  Executor coi mutant X11 (ném AttributeError NGAY TRONG `git_cuc_bo`) là giết ĐÚNG, vì reader ném là vi phạm hợp đồng.
  Hãy phán xét lập luận này; nếu bạn thấy nó cấp tín dụng giả thì nêu một mutant cụ thể chứng minh.
- `DOT_BIEN` có 22 mục `F13_*`, ca đích `c53`; executor khai 22/22 GIET. Diff base..head: 2 tệp, +99/-6.
- Phạm vi: hai P2 lượt 1 có sẵn từ base; executor xếp vào M1 (hợp đồng "không phải commit ⇒ None", "chỉ đọc dòng
  tree/parent"), không phải "lỗi khác" của Q5. Đặc tả ghi "dự kiến ≤ 60 dòng thêm"; trần ràng buộc ADR-0053 ≤ 450.

## Việc (theo thứ tự, viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận chuỗi commit; đọc `git -C src diff 7fcfe18 fdf1f05` và `git -C src diff c8d92ba fdf1f05 -- ops/ci_provenance.py`.
2. Đối chiếu từng lớp lượt 1 (`git-object-type-not-checked`, `git-header-cr-split-creates-parents`,
   `git-reader-fixture-domain-incomplete`) và từng phát hiện tạm của lượt 2 (X01–X06, bộ bọc) trên head: đóng / còn mở,
   kèm phép đo của chính bạn. Chạy lại X01–X06 tương ứng với mã head (mã sản phẩm không đổi từ `7fcfe18`, nên có thể dùng
   thẳng các tệp X* làm `CI_PROVENANCE_MA` với test head).
3. `python -B ops/ci_provenance_test.py --tat-ca-ca` (mọi ca) và chạy 22 mutant F13:
   `python -B -c 'import importlib.util as u; s=u.spec_from_file_location("t","ops/ci_provenance_test.py"); t=u.module_from_spec(s); s.loader.exec_module(t); [print(x[0], t.chay_dot_bien(*x)[0]) for x in t.DOT_BIEN if x[0].startswith("F13")]'`
4. Có thời gian thì tự đột biến thêm `git_cuc_bo` tìm chốt không được bảo vệ; mỗi mutant sống nêu tương đương hay không,
   kèm nhân chứng. Đánh giá theo ngưỡng: chỉ mutant KHÔNG tương đương làm sai kết quả trên đầu vào Git có thể xảy ra mới là
   P2; độ phủ thuần tuý trên đầu ra git không thể sinh ra là P3.
5. N1, N2, N4, N5 như lượt 1; N3 = `not_run` (executor chạy); N6 `not_measured`; N7 không áp dụng.
6. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` nếu cần.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: fdf1f05c1b3d845a694c796a81a8bd5c218a68c8`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC` (lượt 1 + bản tạm lượt 2), rồi bảng lớp mới nếu có:
  `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện | hướng vá` (giữ slug cũ nếu cùng nguyên nhân).
- Bảng N1–N7 kèm rc và bằng chứng dương.

Ngưỡng approve: **không còn P0/P1/P2**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

D02 và F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native; hỗ trợ
SHA-256 toàn tuyến của `main` ngoài `git_cuc_bo`.
