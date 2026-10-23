# Cross-review lượt 3 — packet #858 (wp858), lớp `sensitive`

Bạn là REVIEWER độc lập (họ openai). KHÔNG sửa `kho/`, KHÔNG push, KHÔNG gọi GitHub. Đột biến/phản chứng chạy trên BẢN
SAO TẠM dưới `out/`.

## Định danh — tự kiểm
- `kho/` HEAD phải là `8733f0ae7df5d9a1c704c31e6051e8cb5f439fe5`; nền `git merge-base HEAD origin/master` = `637f780…`.
- Spec `git show origin/ops/wp858-spec:ops/specs/wp858.md` sha256 `5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54`.
- Lease hiện hành: `git show origin/ops/wp858-r1-g2-lease:ops/leases/wp858-r1-g2-claude.yaml` (g2; g1 đã hết hạn). Hai
  verdict trước đã commit trên nhánh ấy ở `ops/reviews/wp858-g1-luot{1,2}-codex-verdict.md`; bản lượt 2 cũng có ở
  `VERDICT-luot2.md` cạnh tệp này.
- Phụ lục chủ kho cho `python`: phương án (a), nợ `python-probe-khong-theo-PATH`; không sửa `ops/cong_cu.py`.
- Chỉ thị chủ kho cho g2 (#858 issuecomment-6332689060, ghi hộ): F858-05 phải gọn về ≤ 450 dòng thêm, lease KHÔNG nâng trần.

## Thay đổi kể từ lượt 2 (`git diff 97544b5 HEAD`)
1. F858-03 (tái mở): dòng cuối nhánh tên trần DAT đổi từ `:giu-nguyen-PATH:` sang `/dev/null`. N4 thêm biến thể `trung`:
   thư mục thật `kho/:giu-nguyen-PATH:` + `kho/rg` hỏng (đúng phản chứng lượt 2 của bạn). Đột biến
   `wp858_sh_dong_canh_la_ten_thu_muc` đổi ngược về tên cũ.
2. F858-04: stub `cygpath -u` khi `CYGPATH_U_HONG` IN đường đúng rồi thoát 37 ⇒ installer thật phải ≠ 0. Đột biến
   `wp858_sh_cygpath_u_hong_khong_tra_loi` chỉ bỏ `return 1`; ca hình dạng nay đòi nguyên dòng chốt `-u`.
3. F858-05: `git diff --numstat 637f780 HEAD` ⇒ 6 tệp, 438 dòng thêm (chỉ nén chú thích/docstring/changelog; không bỏ
   ca âm, đột biến hay assertion — hãy KIỂM lời khai này bằng diff `97544b5..HEAD`).

## Số đo của executor trên `8733f0a` (khi `/tmp/.git` VẮNG) — giả thuyết để bác
`launcher_test` nền 234/234 · head 242/242 (cả hai có/không auth giả) · `--dot-bien` 293/293 (4 không đo được trên
Linux) · selftest 1731/1731 · release-verify strict ok 190/190 · cong_cu_test manh 61 ca, lỗi 0 · ruff F 4409=4409 ·
doctrine sạch · doc-claims ok · actionlint rc 0.
Nhắc: sandbox của CHÍNH bạn gắn `/tmp/.git` ro nên `t86`/`r484_*` có thể đỏ vì môi trường; đo delta trong cùng điều kiện.

## Việc
1. Với F858-03/04/05 (lượt 2): ĐÓNG / CHƯA ĐÓNG, kèm lệnh + kết quả thật trên head mới.
2. Đột biến lại bản vá mới (dòng canh, chốt `-u`) trên bản sao tạm; tìm đột biến sống KHÔNG tương đương.
3. `/dev/null` làm dòng canh: còn đường nào reader nhận nó làm thư mục/đưa vào PATH (Windows Git Bash, CRLF, trình cài
   in `/dev/null` rồi một thư mục…)? Mô tả bằng lời nếu cần soạn nội dung nhạy cảm.
4. Kiểm lại F858-01/02 không hồi quy.

## Đầu ra — BẮT BUỘC `out/VERDICT.md`
Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; `reviewed_head: 8733f0ae7df5d9a1c704c31e6051e8cb5f439fe5`;
bảng đối chiếu finding lượt trước; bảng finding mới (id, P0–P3, tệp:dòng, lệnh → kết quả thật, đề xuất); bảng lệnh →
kết quả; mục "không đo được". Không tính lời khai là đúng nếu chưa đo.
