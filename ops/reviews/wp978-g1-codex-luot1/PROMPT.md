# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 1 — lượt 1

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context
executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa mã nguồn trong `SRC`; mọi phép thử (đột biến,
fixture, script) chạy trên **bản sao riêng** dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp prompt này: clone thường (`.git` là thư mục), detached tại head ứng viên
  **`bef14035718cae862369101f79dc61e938ae6b00`** (xác nhận bằng `git -C src rev-parse HEAD`; nếu khác thì ghi lệch và dừng).
  Base = **`c8d92ba05c3ea875d8f84d94195430302690286d`** (`refs/remotes/origin/master` trong clone trỏ base).
  Thứ định danh tệp là **băm/SHA**, không phải tên nhánh.
- `OUT` = thư mục `out/` cạnh tệp prompt này, là nơi DUY NHẤT bạn ghi.
- Đặc tả `tham-chieu/wp978.md`, sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638`. Hãy băm lại.
- Lease (bản chép) `tham-chieu/lease-wp978-r1-g1-claude.yaml`. Write set của diff PR: `ops/ci_provenance.py`,
  `ops/ci_provenance_test.py`. Trần ADR-0053: ≤ 6 tệp / ≤ 450 dòng thêm.
- Nguồn nợ: `tham-chieu/review-a-VERDICT.md` (verdict lượt review độc lập A trên `4511b1e`, lớp F13) và các script tái
  hiện `tham-chieu/review-a-reviewer-*.py` cùng kết quả JSON của chúng. Đây là ĐẦU VÀO để đối chiếu, không phải đặc tả.

## Việc

1. Băm lại đặc tả. Xác nhận base là cha của head. Đọc `git -C src diff c8d92ba bef1403`.
2. Review **không lọc** theo M1–M3 và N1–N7 của đặc tả. Trọng tâm: `git_cuc_bo` trong `ops/ci_provenance.py`.
3. Đo F13 đã đóng bằng phép đo của CHÍNH bạn, độc lập với ca `c53` của executor: dựng commit Git thật (UTF-8; message
   ISO-8859-1; author ISO-8859-1; header `encoding`), gọi `git_cuc_bo` và `main` qua đường thật. Có thể chạy lại script tái
   hiện của review A (đọc mã trước khi tin; nó tìm `ops/ci_provenance_test.py` theo `cwd`).
4. Đối chiếu từng tiêu chí N1–N3:
   - N1: `python -B ops/ci_provenance_test.py --mot-ca c53_git_commit_khong_utf8` trên head ⇒ rc 0; cùng ca với
     `CI_PROVENANCE_MA=<bản ops/ci_provenance.py tại base>` ⇒ `DO:c53_…` vì `UnicodeDecodeError`.
   - N2: ba đột biến `F13_*` trong `DOT_BIEN` của `ops/ci_provenance_test.py` có giết ĐÚNG `c53` và ĐÚNG lý do không
     (rc 3 + `DO:<ca>:`, không phải rc 4 / tín dụng giả). Chạy từng đột biến bằng:
     `python -B -c 'import importlib.util as u,sys; s=u.spec_from_file_location("t","ops/ci_provenance_test.py"); t=u.module_from_spec(s); s.loader.exec_module(t); [print(x[0], t.chay_dot_bien(*x)) for x in t.DOT_BIEN if x[0].startswith("F13")]'`
     (cwd = `src` hoặc bản sao trong `OUT/`). Rồi **tự đột biến thêm** `git_cuc_bo` để tìm chốt KHÔNG được ca nào bảo vệ
     (ví dụ: nới/siết regex OID, bỏ `len(tree) != 1`, tách phần đầu bằng `\r\n`, đọc trường ngoài phần đầu, giải mã bằng
     `errors="replace"`, đổi `-p` thành loại khác). Mỗi đột biến sống thì nêu rõ có phải tương đương không, kèm lý do.
   - N3: suite mặc định `python -B ops/ci_provenance_test.py` tốn khoảng 40 phút. Executor khai head `CA: 53/53`,
     `DOT BIEN: 295/295`, `TONG: DAT`; base `52/52`, `292/292`. Chạy nếu thời gian cho phép; nếu không, ghi rõ
     `not_run` cho N3 thay vì nhận lời khai, và ít nhất chạy các ca chạm `moc_checkout`/Git: `c05`–`c09`, `c22`, `c32`, `c34`,
     `c53` (tên đầy đủ: `grep -n '^def c' ops/ci_provenance_test.py`).
5. Đặc biệt soi (gợi ý, không giới hạn):
   - Hành vi với commit UTF-8 bình thường có đổi không (giá trị trả về, kiểu `str`, thứ tự parents).
   - OID SHA-256 (64 hex): kho Git dùng `--object-format=sha256` có được xử lý đúng không.
   - Đầu vào không phải commit: blob, tree, tag (annotated), SHA thiếu, SHA rỗng/không hợp lệ, `git` không có trên PATH.
   - Lời khai trong docstring/comment có khớp hành vi đo được không.
   - Ca `c53` có phải "ca có ĐO" không: đột biến về mã base có thật sự làm nó đỏ vì `UnicodeDecodeError` hay vì lý do khác.
   - Phạm vi: diff chỉ chạm hai tệp write set; không đổi hành vi `git_blob`, `doc_wf`, REST.
6. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời** trong verdict, đừng tự soạn.

## Cách chạy

- `export PYTHONDONTWRITEBYTECODE=1`. Nếu git toàn cục có `commit.gpgsign=true`, cô lập bằng
  `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` (ca `c53` dựng object bằng `hash-object`, không cần ký).
- Thư mục tạm đặt dưới `OUT/tmp` (`TMPDIR=$PWD/out/tmp`).

## Dạng verdict — ghi TĂNG DẦN vào `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: bef14035718cae862369101f79dc61e938ae6b00`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- Sau đó là bảng lớp, đếm theo nguyên nhân chứ không theo số biểu hiện:
  `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá`.
- Bảng đối chiếu N1–N7. Kết quả các lệnh đã chạy, kèm rc và bằng chứng dương (`N/N` với hai số bằng nhau).

Slug kebab-case ổn định, đặt theo nguyên nhân. Ngưỡng approve: **không còn P0/P1/P2**. P3 còn lại thì nêu tên và hướng xử
lý. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

- D02 (`uses` nhiều dòng) và F10/D05 (biên `try` của parser): nợ P3 riêng của #899.
- `.claude/dev/ci_dang_ky_test.py`, mốc Workflow definition, LIVE CI, Windows native.
