# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 1 — lượt 6 (lời gọi 6/8)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không mạng, không GitHub,
không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao riêng dưới `OUT/`. Trần 8 lời gọi và luật V1–V3 do chủ kho
quyết (#978 issuecomment-6442791177): đẩy một lần sau approve · dừng vá khi P0=P1=P2=0, mỗi P3 có quyết định · review
THEO LỚP (quét mọi biểu hiện cùng lớp trước khi báo).

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
Không chạy suite mặc định đầy đủ (~40 phút); executor chạy nó trên clone riêng của đúng head.

## Định danh (tự kiểm)

- `SRC` = `src/`, detached tại head ứng viên **`2c907a47e22c7b0706df766176180a798ed7f69f`** (lệch thì ghi và dừng).
  Chuỗi: base **`c8d92ba05c3ea875d8f84d94195430302690286d`** → `bef1403` → `7fcfe18` → `fdf1f05` → `aa2a1f3` →
  `afcadd5` (lượt 5) → head. `refs/remotes/origin/master` trỏ base. Định danh là **SHA**.
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi.
- Đặc tả `tham-chieu/wp978.md`, sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638`. Băm lại.
- Verdict trước: `tham-chieu/luot{1,3,4,5}-VERDICT.md`, `luot2-VERDICT-TAM.md` (bản tạm). Lượt 5 để lại 49 đột biến
  `tham-chieu/luot5/domain-mutants/D01…D49*.py` (bản sao TOÀN tệp `ops/ci_provenance.py` tại `afcadd5`, sản phẩm KHÔNG
  đổi tới head) và `tham-chieu/luot5/domain_criterion.py`.

## Lời khai executor (tự đo)

`afcadd5` → `2c907a4` chỉ đổi `ops/ci_provenance_test.py`:
- `c53` thêm nhân chứng commit HỢP LỆ (oracle Git native `log -1 --no-walk --format=%T%n%P`): author chứa `tree <oid>`
  kẹp giữa VT/FF/FS/GS/RS/byte 0x85/UTF-8 LS/PS/NEL; dòng sau committer là `\ttree <oid>`, `\rtree <oid>`,
  `tree\t<oid>`, `Tree <oid>`, `tree\n <oid>` (gập), `ｔｒｅｅ <oid>` (fullwidth); hai ca M1 kỳ vọng None: dòng `tree `
  rỗng sau committer, và `x-review v\r\n\r\ntree <oid>`.
- 16 mục `DOT_BIEN` mới (`F13_bien_doi_*`, `F13_crlf_truoc_tach`); khai 43/43 F13 GIET.
- Chạy 49 tệp D của lượt 5 làm `CI_PROVENANCE_MA` với `c53` head: executor khai chỉ còn SỐNG đúng 10 tệp D10, D11, D12,
  D14, D16, D31, D33, D38, D39, D42 — trùng nhóm tương đương E1–E6 lượt 5 đã chứng minh. Diff base..head: 2 tệp, +134/-6.

## Việc (viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận chuỗi commit; đọc `git -C src diff afcadd5 2c907a4`.
2. Đối chiếu lớp `git-reader-fixture-domain-incomplete` (P2 lượt 5): chạy lại 49 tệp D với `c53` head; mỗi D không tương
   đương phải rc 3 với `DO:c53_…` đúng lý do (đọc output, không chỉ rc). Kiểm lại các lớp đã đóng lượt 1–5 không hồi quy.
3. `python -B ops/ci_provenance_test.py --tat-ca-ca` và mọi mutant F13:
   `python -B -c 'import importlib.util as u; s=u.spec_from_file_location("t","ops/ci_provenance_test.py"); t=u.module_from_spec(s); s.loader.exec_module(t); [print(x[0], t.chay_dot_bien(*x)[0]) for x in t.DOT_BIEN if x[0].startswith("F13")]'`
4. **Theo V3**, quét tiếp CẢ LỚP còn lại mà lượt 5 chưa phủ, trong MỘT lượt: các cách parser có thể đọc sai ranh giới
   header/body hoặc vị trí dãy `parent` (vd. nhiều dòng trống, `\n\n` trong giá trị header nhiều dòng, `parent` nằm giữa hai
   `tree`, dòng `parent` có dấu cách thừa, octopus rất dài), và với mỗi phép đo có commit Git HỢP LỆ nào phân biệt được
   không. Mutant không tương đương sống trên đầu vào hợp lệ ⇒ cùng lớp P2; tương đương ⇒ nêu lý do.
   Đồng thời đánh giá chính các fixture mới có hợp lệ không (fsck strict, không cần `--literally`).
5. N1, N2, N4, N5 như trước; N3 `not_run` của bạn; N6 `not_measured`; N7 không áp dụng.
6. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` nếu cần.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: 2c907a47e22c7b0706df766176180a798ed7f69f`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC`; bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`, giữ slug cũ nếu cùng nguyên nhân);
  mỗi P3 còn mở ghi đề xuất quyết định (nợ có tên, owner, hướng xử lý); bảng N1–N7 kèm rc và bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

D02 và F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native; SHA-256
toàn tuyến của `main` ngoài `git_cuc_bo`.
