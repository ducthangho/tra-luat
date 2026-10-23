# Cross-review lượt 5/5 (CUỐI) — packet #858 (wp858), lớp `sensitive`

Bạn là REVIEWER độc lập (họ openai). KHÔNG sửa `kho/`, KHÔNG push, KHÔNG gọi GitHub. Đột biến/phản chứng chạy trên BẢN
SAO TẠM dưới `out/`. Đây là lời gọi Codex CUỐI CÙNG của packet.

## Định danh — tự kiểm
- `kho/` HEAD phải là `521efebab226fe3a92b2ccce4a59c27dd638edff`; nền `git merge-base HEAD origin/master` = `637f780…`.
- Spec `git show origin/ops/wp858-spec:ops/specs/wp858.md` sha256 `5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54`.
- Lease `origin/ops/wp858-r1-g2-lease:ops/leases/wp858-r1-g2-claude.yaml`; bốn verdict trước ở
  `origin/ops/wp858-r1-g2-lease:ops/reviews/wp858-g1-luot{1,2,3,4}-codex-verdict.md`; lượt 4 cũng ở `VERDICT-luot4.md`.

## Quyết định chủ kho có thẩm quyền (ghi hộ trên #858; bạn không có mạng nên chép ý tại đây)
- issuecomment-6312034981 — `python` phương án (a): ca python chỉ khẳng định rc 0 + không in thư mục bản hỏng; nợ
  `python-probe-khong-theo-PATH`; không sửa `ops/cong_cu.py`.
- issuecomment-6332689060 — lease g2; diff ≤ 450 dòng thêm, KHÔNG nâng trần.
- issuecomment-6333879879 — **chọn A cho F858-03**: đường *writer muộn* (con của trình cài ghi stdout SAU dòng canh) là
  **nợ có tên `cai-stdout-writer-muon`**, P2 mở CÓ quyết định chủ kho (thoả M-1). Không tách kênh, không nâng trần.
  Verdict ĐƯỢC giữ F858-03/writer-muộn ở trạng thái mở. Gốc chung (kết quả và log trình cài chung stdout) để packet riêng,
  kèm nợ `rg-installer-stdout-khong-LF`. **Một P0/P1 mới hoặc một P2 mới KHÁC vẫn chặn.**

## Thay đổi kể từ lượt 4 (`git diff 93fd69f HEAD`)
- F858-07: fixture `env_them` nhận `None` để BỎ biến; ca linux/macos/windows chạy cả `GITHUB_PATH` rỗng lẫn VẮNG (dưới
  `set -u`). Đột biến `wp858_sh_github_path_vang_khong_mac_dinh` (bỏ `:-`) phải bị ca Linux giết. Ca hình dạng đòi nguyên
  dòng `  if [ -n "${GITHUB_PATH:-}" ]; then`.
- Changelog gọn lại; diff `637f780..HEAD` = 6 tệp / 450 dòng thêm.

## Số đo executor trên `521efeb` (khi `/tmp/.git` VẮNG) — giả thuyết để bác
`launcher_test` nền 234/234 · head 242/242 (có/không auth giả) · `--dot-bien` 296/296 (4 không đo được Linux) · selftest
1731/1731 · release-verify ok 190/190 · cong_cu_test manh 61 ca lỗi 0 · ruff F 4409=4409 · doctrine/doc-claims/actionlint sạch.
Sandbox của bạn gắn `/tmp/.git` ro ⇒ `t86`/`r484_*` có thể đỏ vì môi trường; đo delta trong cùng điều kiện.

## Việc
1. F858-07: ĐÓNG / CHƯA ĐÓNG (lệnh + kết quả thật). F858-01/02/04/05/06: không hồi quy.
2. F858-03: xác nhận các đường ĐÃ vá (dòng trống, trùng tên canh, không LF) vẫn đóng; đường writer muộn được phép mở theo
   quyết định chủ kho — ghi trạng thái "mở có quyết định chủ kho" thay vì chặn.
3. Tìm P0/P1 mới hoặc P2 mới KHÁC lớp `stdout-installer-bi-nhan-lam-ket-qua-chon`: đột biến sống không tương đương,
   hồi quy, vượt write set/trần. Hướng cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI.

## Đầu ra — BẮT BUỘC `out/VERDICT.md`
Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; `reviewed_head: 521efebab226fe3a92b2ccce4a59c27dd638edff`;
bảng đối chiếu mọi finding trước (F858-01..07); bảng finding mới; bảng lệnh → kết quả; mục "không đo được". `approve` là
đúng khi không còn P0/P1 và mọi P2/P3 mở đều có quyết định chủ kho ở trên.
