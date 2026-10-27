# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 1 — lượt 8 (lời gọi CUỐI, 8/8)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không mạng, không GitHub,
không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao riêng dưới `OUT/`. Trần 8 lời gọi và luật V1–V3 do chủ kho
quyết (#978 issuecomment-6442791177). Đây là lời gọi cuối.

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
Không chạy suite mặc định đầy đủ (~40 phút); executor chạy nó trên clone riêng của đúng head.

## NGƯỠNG HẠNG MỚI — quyết định chủ kho (#978 issuecomment-6445001458), thay ngưỡng executor đặt từ lượt 4

- **P2 (chặn approve):** lỗi SẢN PHẨM — `git_cuc_bo` trả sai so với Git native, hoặc sai quy tắc M1 của đặc tả, trên một
  commit Git HỢP LỆ; hoặc vi phạm hợp đồng (ném ngoại lệ), hoặc hồi quy bất kỳ tiêu chí N1–N5. Cũng là P2: ca/đột biến của
  executor cấp TÍN DỤNG GIẢ (giết vì lý do vô can) hoặc kỳ vọng của test SAI.
- **P3 (không chặn):** đột biến không tương đương còn sống mà sản phẩm vẫn đúng — tức thiếu độ phủ thuần tuý. Chủ kho đã
  đặt tên nợ `wp978-git-reader-differential-fuzz`, owner `ducthangho`, hướng xử lý: test vi sai sinh ngẫu nhiên theo ngữ
  pháp header Git ở packet sau. Liệt kê survivor mới bạn tìm được dưới lớp P3 này (kèm nhân chứng) để packet sau dùng.
- Không hạ một lỗi sản phẩm thành P3 vì nó "chỉ là fixture".

## Định danh (tự kiểm)

- `SRC` = `src/`, detached tại head ứng viên **`53ec046fc6c9ebc2b60871a5c0413570d3b0430d`** (lệch thì ghi và dừng).
  Chuỗi: base **`c8d92ba05c3ea875d8f84d94195430302690286d`** → `bef1403` → `7fcfe18` → `fdf1f05` → `aa2a1f3` → `afcadd5`
  → `2c907a4` → `bf8ef91` (lượt 7) → head. `refs/remotes/origin/master` trỏ base. Định danh là **SHA**.
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi.
- Đặc tả `tham-chieu/wp978.md`, sha256 `eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638`. Băm lại.
- Verdict trước: `tham-chieu/luot{1,3,4,5,6,7}-VERDICT.md`, `luot2-VERDICT-TAM.md`. Đột biến cũ (bản sao TOÀN tệp sản phẩm;
  sản phẩm KHÔNG đổi từ `aa2a1f3`): `tham-chieu/luot5/domain-mutants/D*.py`, `tham-chieu/luot6/boundary-mutants/{B,P}*.py`,
  `tham-chieu/luot7/cross-mutants/C*.py`.

## Lời khai executor (tự đo)

`bf8ef91` → `53ec046` chỉ đổi `ops/ci_provenance_test.py`: ma trận `c53` thêm parent trùng A,B,A và A,A,A; dòng mở rộng
`tree\t <oid>`, `tree\r\n <oid>`, `tree\n\t<oid>`, `tree\r\n\t<oid>`; 5 mục `DOT_BIEN` mới (gập CRLF+SP / LF+TAB /
CRLF+TAB, loại trùng lệch một, rstrip tên trường). Khai: 25/25 tệp C lượt 7 bị giết; D/B/P chỉ còn sống các mục đã chứng minh
tương đương; 53 F13 mutant GIET. Suite đầy đủ trên `bf8ef91` (clone riêng): `CA: 53/53`, `DOT BIEN: 340/340`,
`TONG: DAT` (xem `tham-chieu/suite-bf8ef91-executor.txt`); suite trên head đang chạy. Diff base..head: 2 tệp, +157/-6.

## Việc (viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận chuỗi commit; đọc `git -C src diff bf8ef91 53ec046` và diff sản phẩm base..head.
2. Theo ngưỡng mới, tìm **lỗi sản phẩm**: đối chiếu `git_cuc_bo` với Git native trên commit hợp lệ đa dạng (dùng lại các
   ma trận/quét của lượt 5–7), và hợp đồng không-ném. Kiểm các lớp sản phẩm đã đóng (encoding, loại object, CR, parent sau
   committer) không hồi quy.
3. Kiểm **tính đúng của test**: kỳ vọng M1 trong ma trận có độc lập và đúng không; có ca nào chết vì lý do vô can (tín dụng
   giả) không; chạy `--tat-ca-ca` và mọi mutant F13 (lệnh như trước), cùng các tệp C/D/B/P cũ với `c53` head.
4. N1, N2, N4, N5 như trước; N3 `not_run` của bạn; N6 `not_measured`; N7 không áp dụng.
5. Liệt kê survivor độ phủ mới (nếu có) dưới lớp P3 `git-reader-fixture-domain-incomplete` kèm nhân chứng.
6. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` nếu cần.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: 53ec046fc6c9ebc2b60871a5c0413570d3b0430d`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC`; bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`); mỗi P3 ghi nợ có tên, owner, hướng xử
  lý; bảng N1–N7 kèm rc và bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0** theo ngưỡng hạng mới ở trên. Verdict chỉ neo commit trên, không cấp quyền push, merge
hay land.

## Ngoài phạm vi (không tính hạng)

D02 và F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native; SHA-256
toàn tuyến của `main` ngoài `git_cuc_bo`.
