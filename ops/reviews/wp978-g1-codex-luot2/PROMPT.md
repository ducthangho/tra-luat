# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 1 — lượt 2 (lời gọi CUỐI, 2/2)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context
executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa mã nguồn trong `SRC`; mọi phép thử chạy trên
**bản sao riêng** dưới `OUT/`. Đây là lời gọi Codex cuối cùng trong trần của đặc tả (Q1: tối đa 2).

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = `src/` cạnh tệp prompt này: clone thường, detached tại head ứng viên
  **`7fcfe18181ce4d089225900e36d3aed878877e7f`** (kiểm bằng `git -C src rev-parse HEAD`; lệch thì ghi và dừng).
  Cha: `bef14035718cae862369101f79dc61e938ae6b00` (head lượt 1). Base = **`c8d92ba05c3ea875d8f84d94195430302690286d`**
  (`refs/remotes/origin/master` trong clone). Thứ định danh tệp là **băm/SHA**, không phải tên nhánh.
- `OUT` = `out/` cạnh tệp prompt này, nơi DUY NHẤT bạn ghi.
- Đặc tả `tham-chieu/wp978.md`, sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638`. Băm lại.
- Lease (bản chép) `tham-chieu/lease-wp978-r1-g1-claude.yaml`.
- Verdict lượt 1 (neo `bef1403`): `tham-chieu/luot1-VERDICT.md`, cùng các script của lượt 1 trong `tham-chieu/luot1/`
  (chúng ghi kết quả vào `out/` của thư mục chạy và tham chiếu helper `review_common.py`; đọc mã trước khi chạy lại, đường
  dẫn/anchor đột biến của chúng neo mã CŨ nên có thể cần chỉnh trên bản sao của bạn).
- Nguồn nợ gốc: `tham-chieu/review-a-VERDICT.md` (F13).

## Lượt 1 đã nêu gì, executor đã làm gì (LỜI KHAI — tự đo, đừng tin)

Lượt 1: `request_changes`, ba lớp:
`git-object-type-not-checked` (P2) · `git-header-cr-split-creates-parents` (P2) · `git-reader-fixture-domain-incomplete` (P3).

Executor khai (commit `7fcfe18`, chỉ `git -C src diff bef1403 7fcfe18` là thay đổi mới):
- `git_cuc_bo` đọc bằng MỘT lời gọi `git cat-file --batch` (sha qua stdin), đòi header `<oid> commit <size>`, kích thước là
  số và đúng bằng phần thân (+1 LF), `returncode == 0`; tách phần đầu tại LF-LF rồi tách dòng bằng LF (không `splitlines()`).
  Không peel tag. `sha` không phải `str` ⇒ None. Bỏ chốt khoảng trắng vì sha nhiều dòng làm `--batch` trả nhiều object ⇒ lệch
  kích thước ⇒ None.
- `c53` mở miền fixture: SHA-256 (kho `--object-format=sha256`), OID dài 41, ký tự `g`, chữ hoa, parent `zz`, byte không
  ASCII trong parent, hai tree, không tree, body giống header, commit gốc, CR trong author (Git native 0 parent), blob
  thường/không UTF-8/dạng commit, tree, annotated tag, SHA thiếu, rỗng, nhiều dòng, `None`, không có git trên PATH, tiêm
  `rc=128` với stdout giống commit, tiêm kích thước không phải số. Mỗi lần gọi reader được bọc: ném ⇒ giá trị
  `NEM:<lớp>` (hợp đồng reader là không ném vì `main` không bắt) — hãy đánh giá xem bọc này có tạo tín dụng giả không.
- `DOT_BIEN` có **17** mục `F13_*`, ca đích `c53`; executor khai 17/17 GIET.
- Kích thước: `git diff --numstat c8d92ba 7fcfe18` = 2 tệp, +87 dòng thêm. Đặc tả ghi "dự kiến ≤ 60 dòng thêm" (bản nháp
  38); trần ràng buộc là ADR-0053 (≤ 6 tệp / ≤ 450). Hai P2 có sẵn từ base; executor xếp chúng VÀO M1 (hợp đồng
  "không phải commit ⇒ None" và "chỉ đọc dòng tree/parent") chứ không phải "lỗi khác" của Q5. Hãy nói thẳng nếu bạn thấy
  cách xếp đó hoặc mức vượt dự kiến là vấn đề về phạm vi.

## Việc

1. Băm đặc tả; xác nhận chuỗi base → bef1403 → 7fcfe18; đọc diff base..head và bef1403..head.
2. Đo lại TỪNG lớp lượt 1 bằng phép đo của chính bạn (không chỉ đọc `c53`): blob dạng commit, tree, annotated tag ⇒ None;
   commit CR-author ⇒ parents bằng Git native; main âm/dương như lượt 1. Commit Latin-1 / SHA-256 / root / merge vẫn đúng.
3. Chạy lại 10 đột biến không tương đương còn sống ở lượt 1 (R01–R04, R06, R07, R09, R12–R14) dưới dạng tương ứng với mã mới,
   cộng R05 (tín dụng giả ở lượt 1). Báo từng cái: GIET đúng lý do / tín dụng giả / sống (tương đương hay không, kèm nhân chứng).
4. Chạy 17 đột biến `F13_*` của catalogue (lệnh dưới) và **tự đột biến thêm** mã mới tìm chốt không được bảo vệ: phân tích
   header `--batch`, so kích thước, kiểm rc, kiểm kiểu, đường lỗi `UnicodeEncodeError`.
   `python -B -c 'import importlib.util as u; s=u.spec_from_file_location("t","ops/ci_provenance_test.py"); t=u.module_from_spec(s); s.loader.exec_module(t); [print(x[0], t.chay_dot_bien(*x)) for x in t.DOT_BIEN if x[0].startswith("F13")]'`
5. Soi: hành vi `--batch` khi tên object có dấu cách hoặc dạng `<rev>:<path>`; ảnh hưởng hiệu năng/timeout; có tạo đường
   ghi/khoá nào vào kho không; docstring/comment khớp hành vi đo được; không đổi `git_blob`, `doc_wf`, REST, `main`.
6. N1–N7 như lượt 1. N3 (suite mặc định ~40 phút) chạy nếu thời gian cho phép; không thì ghi `not_run` và chạy ít nhất
   `--tat-ca-ca` (mọi ca) cùng các ca `c05`–`c09`, `c22`, `c32`, `c34`, `c53`.
7. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; cô lập git config bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` nếu cần.

## Dạng verdict — ghi TĂNG DẦN vào `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: 7fcfe18181ce4d089225900e36d3aed878877e7f`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- Mục `ĐỐI CHIẾU LƯỢT TRƯỚC`: từng slug lượt 1 ⇒ đóng / còn mở / đổi hạng, kèm phép đo.
- Bảng lớp mới (nếu có): `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện | hướng vá`. Giữ slug lượt 1 nếu
  cùng nguyên nhân.
- Bảng N1–N7 và kết quả lệnh kèm rc và bằng chứng dương.

Ngưỡng approve: **không còn P0/P1/P2**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

- D02 và F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native.
- Hỗ trợ SHA-256 TOÀN TUYẾN của `main` (`RE_SHA`/`RE_HEX40` ngoài `git_cuc_bo` giới hạn 40): ghi nhận nếu muốn, không tính hạng.
