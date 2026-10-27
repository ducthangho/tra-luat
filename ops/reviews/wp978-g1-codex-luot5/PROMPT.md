# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 1 — lượt 5 (lời gọi 5/8)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context
executor. Không mạng, không GitHub, không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao riêng dưới `OUT/`.
Trần lời gọi do chủ kho nâng lên 8 (#978 issuecomment-6442791177), kèm luật vòng đời V1–V3 (đẩy một lần sau approve ·
dừng vá khi P0=P1=P2=0, mỗi P3 có quyết định · review THEO LỚP: khái quát mỗi biểu hiện thành một lớp nguyên nhân rồi
quét MỌI biểu hiện cùng lớp trước khi báo).

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
Không chạy suite mặc định đầy đủ (~40 phút). Executor khai đã chạy nó trên clone riêng của đúng head: xem
`tham-chieu/suite-afcadd5-executor.txt` (lời khai, không phải phép đo của bạn).

## Định danh (tự kiểm)

- `SRC` = `src/`, detached tại head ứng viên **`afcadd5673009dd4a6a56076af04f57b0ba56c11`** (lệch thì ghi và dừng).
  Chuỗi: base **`c8d92ba05c3ea875d8f84d94195430302690286d`** → `bef1403` (lượt 1) → `7fcfe18` (lượt 2, cắt) → `fdf1f05`
  (lượt 3) → `aa2a1f3` (lượt 4) → head. `refs/remotes/origin/master` trỏ base. Định danh là **SHA**.
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi.
- Đặc tả `tham-chieu/wp978.md`, sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638`. Băm lại.
- Verdict trước: `tham-chieu/luot1-VERDICT.md`, `luot2-VERDICT-TAM.md` (bản tạm), `luot3-VERDICT.md`, `luot4-VERDICT.md`.
  Script lượt 4: `tham-chieu/luot4/extra_domain.py`, `continuation_criterion.py` (đọc trước khi chạy; neo có thể là mã cũ).

## Lời khai executor (tự đo)

`aa2a1f3` → `afcadd5` chỉ đổi `ops/ci_provenance_test.py`: thêm vào `c53` một commit hợp lệ có `mergetag` nhiều dòng
(nội dung tag chứa ` tree <oid>` và ` parent <oid>` ở dòng tiếp nối, giữ dấu cách), kỳ vọng tree/parents của commit ngoài,
đi qua oracle Git native; thêm đột biến `F13_lstrip_dau_dong` (= Z01 lượt 4). Khai 27/27 mục `F13_*` GIET. Sản phẩm
không đổi từ `aa2a1f3`. Diff base..head: 2 tệp, +119/-6.

## Việc (viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận chuỗi commit; đọc `git -C src diff aa2a1f3 afcadd5`.
2. Đối chiếu lớp `git-reader-fixture-domain-incomplete` (P2 lượt 4): Z01 nay có bị giết đúng `c53` và đúng lý do không;
   kiểm các lớp đã đóng ở lượt 1–4 không hồi quy (có thể tái dùng script cũ trên bản sao).
3. `python -B ops/ci_provenance_test.py --tat-ca-ca` và 27 mutant F13:
   `python -B -c 'import importlib.util as u; s=u.spec_from_file_location("t","ops/ci_provenance_test.py"); t=u.module_from_spec(s); s.loader.exec_module(t); [print(x[0], t.chay_dot_bien(*x)[0]) for x in t.DOT_BIEN if x[0].startswith("F13")]'`
4. **Theo V3**: với lớp độ phủ fixture, đừng dừng ở Z01 — quét CẢ LỚP: liệt kê các phép chuẩn hoá/biến đổi dòng header mà
   một parser có thể làm sai (strip hai phía, rstrip, gộp khoảng trắng, tách theo CR/VT/FF, hạ chữ, cắt ở NUL, bỏ dòng
   rỗng, đọc dòng tiếp nối như dòng mới, chấp nhận `tree`/`parent` sau dấu cách, …) và với mỗi phép, đo xem có commit
   Git HỢP LỆ (fsck chấp nhận) nào phân biệt được không, rồi xem `c53` có giết mutant tương ứng không. Báo đầy đủ trong
   MỘT lượt: mutant không tương đương sống trên đầu vào Git hợp lệ ⇒ cùng lớp P2; tương đương ⇒ nêu lý do.
5. N1, N2, N4, N5 như trước; N3 `not_run` của bạn; N6 `not_measured`; N7 không áp dụng.
6. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` nếu cần.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: afcadd5673009dd4a6a56076af04f57b0ba56c11`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC`; bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`, giữ slug cũ nếu cùng nguyên nhân);
  mỗi P3 còn mở ghi đề xuất quyết định (nợ có tên, owner, hướng xử lý); bảng N1–N7 kèm rc và bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

D02 và F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native; SHA-256
toàn tuyến của `main` ngoài `git_cuc_bo`.
