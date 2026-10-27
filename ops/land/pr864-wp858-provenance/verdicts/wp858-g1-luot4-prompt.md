# Cross-review lượt 4 — packet #858 (wp858), lớp `sensitive`

Bạn là REVIEWER độc lập (họ openai). KHÔNG sửa `kho/`, KHÔNG push, KHÔNG gọi GitHub. Đột biến/phản chứng chạy trên BẢN
SAO TẠM dưới `out/`. Đây là lời gọi Codex thứ 4/5 của packet; lượt 5 là lượt cuối.

## Định danh — tự kiểm
- `kho/` HEAD phải là `93fd69fb958527ba738f882391956311972de60b`; nền `git merge-base HEAD origin/master` = `637f780…`.
- Spec `git show origin/ops/wp858-spec:ops/specs/wp858.md` sha256 `5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54`.
- Lease `origin/ops/wp858-r1-g2-lease:ops/leases/wp858-r1-g2-claude.yaml`; ba verdict trước ở
  `origin/ops/wp858-r1-g2-lease:ops/reviews/wp858-g1-luot{1,2,3}-codex-verdict.md` (lượt 3 bạn không thấy hai tệp đầu vì
  ref cục bộ lúc ấy chưa fetch lại — nay đã có; hãy `git show` để tự kiểm). Bản lượt 3: `VERDICT-luot3.md` cạnh tệp này.
- Phụ lục chủ kho `python` (a), nợ `python-probe-khong-theo-PATH`; chỉ thị g2: diff ≤ 450 dòng thêm, không nâng trần.

## Thay đổi kể từ lượt 3 (`git diff 8733f0a HEAD`)
1. F858-03: CẢ dòng canh `/dev/null` LẪN thư mục chọn nay in bằng `printf '\n%s\n'` — luôn đứng riêng một dòng dù stdout
   trình cài không kết thúc bằng LF. N4 thêm biến thể `khong_lf`: stdout trình cài `bash` là tiền tố KHÔNG LF và
   `<tiền tố>/dev/null/rg` hỏng (đúng phản chứng lượt 3 của bạn). Đột biến `wp858_sh_dong_canh_khong_tach_dong`.
   Ghi chú phạm vi: stub chỉ in khi cài `bash`; công thức `rg` (bộ chọn riêng, giữ nguyên theo Q1 của spec) tự nó cũng
   nối dòng khi trình cài `ripgrep` không kết thúc bằng LF — executor ghi đây là nợ ngoài phạm vi, không vá. Hãy đánh
   giá cách xếp loại này.
2. F858-06: ca Windows dương khi `GITHUB_PATH` rỗng (⇒ vẫn phải qua `cygpath -u`). Đột biến
   `wp858_sh_cygpath_u_chi_khi_ghi_path`; ca hình dạng đòi nguyên cặp dòng `if [ -n "$win" ]; then` + `d="$(cygpath -u`.
3. Diff: `git diff --numstat 637f780 HEAD` ⇒ 6 tệp, 448 dòng thêm (chỉ nén chú thích/changelog — kiểm lại).

## Số đo executor trên `93fd69f` (khi `/tmp/.git` VẮNG) — giả thuyết để bác
`launcher_test` nền 234/234 · head 242/242 (có/không auth giả) · `--dot-bien` 295/295 (4 không đo được Linux) · selftest
1731/1731 · release-verify ok 190/190 · cong_cu_test manh 61 ca lỗi 0 · ruff F 4409=4409 · doctrine/doc-claims/actionlint
sạch. Sandbox của bạn gắn `/tmp/.git` ro ⇒ `t86`/`r484_*` có thể đỏ vì môi trường; đo delta trong cùng điều kiện.

## Việc
1. F858-03 và F858-06: ĐÓNG / CHƯA ĐÓNG kèm lệnh + kết quả thật; chạy lại phản chứng không-LF của bạn.
2. Kiểm F858-01/02/04/05 không hồi quy.
3. Đột biến bản vá mới; tìm đột biến sống KHÔNG tương đương; tìm đường nào khác để stdout trình cài lọt thành `DICH`
   (CR đơn, `\r\n` cuối, NUL, trình cài in ra stderr…). Hướng cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI.

## Đầu ra — BẮT BUỘC `out/VERDICT.md`
Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; `reviewed_head: 93fd69fb958527ba738f882391956311972de60b`;
bảng đối chiếu finding trước; bảng finding mới (id, P0–P3, tệp:dòng, lệnh → kết quả thật, đề xuất); bảng lệnh → kết quả;
mục "không đo được". Không tính lời khai là đúng nếu chưa đo.
