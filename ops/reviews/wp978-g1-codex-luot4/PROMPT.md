# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 1 — lượt 4 (lời gọi CUỐI, 4/4)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context
executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa mã nguồn trong `SRC`; mọi phép thử chạy trên
**bản sao riêng** dưới `OUT/`. Trần lời gọi do chủ kho nâng lên 4 (#978 issuecomment-6441085134); đây là lời gọi cuối.

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
Không chạy suite mặc định đầy đủ (~40 phút); executor tự chạy.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = `src/` cạnh tệp prompt này, detached tại head ứng viên **`aa2a1f326eb964b1cf8f45454593971e0ab11b73`**
  (kiểm `git -C src rev-parse HEAD`; lệch thì ghi và dừng). Chuỗi: base **`c8d92ba05c3ea875d8f84d94195430302690286d`**
  → `bef14035718cae862369101f79dc61e938ae6b00` (lượt 1) → `7fcfe18181ce4d089225900e36d3aed878877e7f` (lượt 2, bị cắt)
  → `fdf1f05c1b3d845a694c796a81a8bd5c218a68c8` (lượt 3) → head. `refs/remotes/origin/master` trỏ base. Định danh là **SHA**.
- `OUT` = `out/` cạnh tệp prompt này, nơi DUY NHẤT bạn ghi.
- Đặc tả `tham-chieu/wp978.md`, sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638`. Băm lại.
- Verdict trước: `tham-chieu/luot1-VERDICT.md`, `tham-chieu/luot2-VERDICT-TAM.md` (bản tạm), `tham-chieu/luot3-VERDICT.md`;
  script lượt 3 ở `tham-chieu/luot3/` (đọc mã trước khi chạy; neo đột biến của chúng có thể là mã CŨ).

## Lời khai của executor (tự đo, đừng tin)

`fdf1f05` → `aa2a1f3`:
- `git_cuc_bo`: `parent` chỉ được đọc trong DÃY LIỀN SAU dòng đầu, và dòng đầu phải là `tree ` (ngữ pháp Git); vẫn đòi
  đúng một dòng `tree ` trong header (object hai `tree` mà `fsck` từ chối ⇒ None, chặt hơn parser Git).
- `c53`: thêm commit 3 parent thứ tự không sắp xếp; hai commit hợp lệ có `parent` sau committer / sau header mở rộng
  (kỳ vọng 0 parent); object hỏng `parent` trước `tree` và `tree <oid>\rparent <oid>`; commit SHA-256 có 3 parent.
  Thêm **oracle Git native** cho MỌI commit hợp lệ trong fixture: `git log -1 --no-walk --format=%T%n%P` (không dùng
  `git show` vì nó đọc object cha — cha trong fixture không tồn tại).
- Executor cố ý KHÔNG dùng `git log --format=%P` trong SẢN PHẨM: trên clone nông (checkout CI), commit biên bị graft
  nên `%P` rỗng, sai đúng ca merge PR. Hãy phán xét lựa chọn này.
- `DOT_BIEN`: 26 mục `F13_*` (thêm `F13_cha_quet_ca_dau`, `F13_bo_tree_dong_dau`, `F13_cha_chi_hai`, `F13_cha_chi_40`),
  khai 26/26 GIET. Diff base..head: 2 tệp, +116/-6.
- Lưu ý hợp đồng lượt 3 nêu (M2 chỉ cho `UnicodeDecodeError` thành tín hiệu chốt; bộ bọc hiện rộng hơn): executor ghi vào
  handoff như một lệch câu chữ đặc tả cần chủ kho xác nhận, không tự sửa đặc tả đóng băng.

## Việc (viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận chuỗi commit; đọc `git -C src diff fdf1f05 aa2a1f3` và diff base..head của `ops/ci_provenance.py`.
2. Đối chiếu hai lớp lượt 3 (`git-header-extension-creates-parents`, `git-reader-fixture-domain-incomplete`) và các lớp
   đã đóng ở lượt 1–3 (không hồi quy): đóng / còn mở, bằng phép đo của chính bạn (`tham-chieu/luot3/extension_*.py` có
   thể tái dùng). Chạy lại Y01/Y02 tương ứng mã head.
3. `python -B ops/ci_provenance_test.py --tat-ca-ca` và 26 mutant F13:
   `python -B -c 'import importlib.util as u; s=u.spec_from_file_location("t","ops/ci_provenance_test.py"); t=u.module_from_spec(s); s.loader.exec_module(t); [print(x[0], t.chay_dot_bien(*x)[0]) for x in t.DOT_BIEN if x[0].startswith("F13")]'`
4. Tự đột biến thêm `git_cuc_bo` và đối chiếu thêm các dạng commit hợp lệ khác với Git native (vd. `gpgsig`/`mergetag`
   nhiều dòng có dòng tiếp nối bắt đầu bằng dấu cách, `encoding`, octopus, root). Ngưỡng hạng: chỉ sai kết quả trên
   đầu vào Git hợp lệ (fsck chấp nhận) hoặc mutant không tương đương sống trên đầu vào ấy mới là P2; độ phủ trên đầu ra git
   không thể sinh ra là P3.
5. N1, N2, N4, N5 như trước; N3 `not_run`; N6 `not_measured`; N7 không áp dụng.
6. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` nếu cần.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: aa2a1f326eb964b1cf8f45454593971e0ab11b73`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC`, bảng lớp mới nếu có (`slug | hạng | file:dòng | phép đo | hướng vá`, giữ slug cũ nếu cùng
  nguyên nhân), bảng N1–N7 kèm rc và bằng chứng dương.

Ngưỡng approve: **không còn P0/P1/P2**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

D02 và F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native; SHA-256
toàn tuyến của `main` ngoài `git_cuc_bo`.
