# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 1 — lượt 7 (lời gọi 7/8)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không mạng, không GitHub,
không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao riêng dưới `OUT/`. Trần 8 lời gọi và luật V1–V3 do chủ kho
quyết (#978 issuecomment-6442791177): đẩy một lần sau approve · dừng vá khi P0=P1=P2=0, mỗi P3 có quyết định · review
THEO LỚP. Còn đúng một lời gọi sau lượt này.

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
Không chạy suite mặc định đầy đủ (~40 phút); executor chạy nó trên clone riêng của đúng head.

## Định danh (tự kiểm)

- `SRC` = `src/`, detached tại head ứng viên **`bf8ef9125ba54312d41baf3eb6ed88d564758256`** (lệch thì ghi và dừng).
  Chuỗi: base **`c8d92ba05c3ea875d8f84d94195430302690286d`** → `bef1403` → `7fcfe18` → `fdf1f05` → `aa2a1f3` → `afcadd5`
  → `2c907a4` (lượt 6) → head. `refs/remotes/origin/master` trỏ base. Định danh là **SHA**.
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi.
- Đặc tả `tham-chieu/wp978.md`, sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638`. Băm lại.
- Verdict trước: `tham-chieu/luot{1,3,4,5,6}-VERDICT.md`, `luot2-VERDICT-TAM.md`. Đột biến cũ (bản sao TOÀN tệp sản phẩm,
  sản phẩm KHÔNG đổi từ `aa2a1f3` tới head): `tham-chieu/luot5/domain-mutants/D*.py`, `tham-chieu/luot6/boundary-mutants/{B,P}*.py`,
  script quét `tham-chieu/luot6/boundary_sweep.py`.

## Lời khai executor (tự đo)

`2c907a4` → `bf8ef91` chỉ đổi `ops/ci_provenance_test.py`. Thay vì thêm nhân chứng tay, `c53` thêm một **ma trận tổ hợp**
150 commit hợp lệ: danh sách parent {rỗng, một, TRÙNG, 3, 257} × dòng mở rộng sau committer {không có, `x-review start`
+ dòng tiếp nối chỉ SP / TAB / SP+TAB rồi `tree <oid>`, `tree ` rỗng, extension nhiều dòng có ` tree`/` parent` tiếp nối}
× thân {không có dòng trống/không thân, `m`, metadata giữa hai đoạn, metadata đầu thân, thân bắt đầu bằng dòng trống}.
Kỳ vọng tính ĐỘC LẬP với sản phẩm: đếm dòng bắt đầu `tree ` trong phần trước LF-LF đầu tiên; ≠ 1 ⇒ None (M1), ngược lại
dict được vòng oracle Git native kiểm. Thêm 5 mục `DOT_BIEN` (rsplit, dòng trắng là ranh giới, strip payload, gộp parent
trùng, giới hạn 256 parent); khai 48/48 F13 GIET. Chạy lại mọi tệp D/B/P cũ với `c53` head: executor khai chỉ còn SỐNG
B05, B06, B12, P02–P08 và D10, D11, D12, D14, D16, D31, D33, D38, D39, D42 — đúng các mục bạn/lượt trước đã chứng minh
tương đương. `c53` chạy ~4 s. Diff base..head: 2 tệp, +152/-6.

## Việc (viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận chuỗi commit; đọc `git -C src diff 2c907a4 bf8ef91`.
2. Chạy lại mọi tệp D/B/P cũ với `c53` head; mỗi mục không tương đương phải rc 3 với `DO:c53_…` đúng lý do. Kiểm các lớp
   đã đóng lượt 1–6 không hồi quy.
3. `python -B ops/ci_provenance_test.py --tat-ca-ca` và mọi mutant F13 (lệnh như các lượt trước). Kiểm riêng: phép tính kỳ
   vọng M1 trong ma trận có thật sự độc lập với sản phẩm không (nó có thể vô tình chép đúng lỗi của sản phẩm không), và
   mọi commit trong ma trận có hợp lệ không (hash-object không `--literally` ⇒ rc 0; fsck strict nếu bạn dựng cha thật).
4. **Theo V3**: đánh giá ma trận có đóng lớp `git-reader-fixture-domain-incomplete` theo CẤU TRÚC không — tức một biến đổi
   parser mới, thuộc các trục đã quét ở lượt 4–6 (chuẩn hoá dòng, phân cách, ranh giới header/body, dãy parent, số/thứ tự
   cha) hoặc tổ hợp của chúng, có còn sống không. Quét thêm các tổ hợp liên trục mà lượt 5–6 chỉ thử riêng lẻ. Mutant
   không tương đương sống trên đầu vào Git hợp lệ ⇒ cùng lớp P2; tương đương ⇒ nêu lý do. Nếu bạn kết luận lớp đã đóng,
   nói rõ miền nào CHƯA quét để chủ kho quyết nợ.
5. N1, N2, N4, N5 như trước; N3 `not_run` của bạn; N6 `not_measured`; N7 không áp dụng.
6. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` nếu cần.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: bf8ef9125ba54312d41baf3eb6ed88d564758256`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC`; bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`, giữ slug cũ nếu cùng nguyên nhân);
  mỗi P3 còn mở ghi đề xuất quyết định (nợ có tên, owner, hướng xử lý); bảng N1–N7 kèm rc và bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

D02 và F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native; SHA-256
toàn tuyến của `main` ngoài `git_cuc_bo`.
