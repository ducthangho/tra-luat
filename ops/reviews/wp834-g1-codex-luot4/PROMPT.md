# Cross-review Codex — packet #834 (`MAY-ADR-0054-a2`) — lượt 4

Bạn là **reviewer độc lập, offline** cho Packet #834, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context
executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa mã nguồn của packet; mọi phép thử (đột biến,
fixture, script) chạy trên **bản sao riêng** của bạn dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp prompt này: clone thường (`.git` là thư mục, không nông), detached tại head ứng viên
  **`dcb77e78113ed66641771a82f404b713c9602d4d`**. Base = **`ab344da5f07cce673d97056b70b002911c4d5082`** (`origin/master`
  lúc cấp lease; ref `refs/remotes/origin/master` trong clone trỏ base). Thứ định danh tệp là **băm/SHA**, không phải tên nhánh.
- `OUT` = thư mục `out/` cạnh tệp prompt này — nơi DUY NHẤT bạn ghi.
- Đặc tả con `SRC/ops/specs/wp834.md` sha256 `c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2`.
- Phần chung (ràng buộc) `SRC/ops/specs/may-adr-0054-chung.md` sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
- Lease (bản chép) `tham-chieu/lease-wp834-r1-g1-claude.yaml`. Write set: `.claude/dev/packet_loop.py`,
  `.claude/dev/packet_loop_test.py`, `docs/PROTOCOL_DA_PHIEN.md` (§4). Diff ≤ 450 dòng thêm (ADR-0053).
- Đầu vào thiết kế (KHÔNG phải đặc tả): `tham-chieu/wp812-g2-codex-luot1-VERDICT.md` — verdict Codex trên candidate g2 của #812,
  nơi các lớp `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite` và phần connector
  của `findings-not-receipt-bound` được giao cho packet này. Đo xem bản này có đóng các lớp ấy không.


## Lượt 4 — lý do và đối chiếu lượt trước

Lời gọi Codex thứ **4/8** (ADR-0052). Lý do: lượt 3 trên `7436fe3` trả `request_changes` (0 P0, 0 P1, 3 P2), bản chép ở
`tham-chieu/VERDICT-luot3.md` sha256 `d452fd8bd7898faa4a905714fcc016336211a46e9b60684be578f0550d3bca72` (các lượt trước:
`VERDICT-luot2.md` sha256 `cb53cee193fa89c7b0c593e660fe183514a86b42a164f2bdd4be5e69935621be`, `VERDICT-luot1.md` sha256
`cc5621187bccd6e8e63e37ee660d7eb92c26eb88d6090122e3892cfa501b5e0e`). Executor vá ở commit `dcb77e7` (cha `7436fe3`):
F5 dựng và mã hoá state dự kiến TRƯỚC `_xet_dung`; F4 `_r834_ca` phân loại CLI sập là tín dụng giả (`CliSapDo`) và đột biến parser
giữ cấu trúc nhóm regex; F2 ca/đột biến cho dừng trước H/P3, job chưa xanh, P1 ở review comment.
Mở verdict bằng **ĐỐI CHIẾU LƯỢT TRƯỚC** cho mọi slug còn mở của lượt 3 (đóng — ĐÃ VÁ THẬT / còn mở, kèm phép đo), đo lại ba
đột biến sống lượt 3 trên head mới, rồi review lại toàn bộ diff `ab344da..dcb77e7` (và `git diff 7436fe3 dcb77e7`) — finding mới,
kể cả do bản vá sinh ra, đếm riêng. Diff đang sát trần kích thước (executor khai 432/450 dòng thêm): nếu đề xuất vá, ưu tiên hướng
không tăng diff.
Executor khai (đừng tin, hãy đo): 54/54 ca `r834_*`; 49 đột biến `r834_*` + `r812_bo_generation` giết đúng ca, 0 sống, 0 tín dụng giả.

## Việc

1. Băm lại hai đặc tả; xác nhận base là tổ tiên head; đọc `git diff ab344da dcb77e7` (và `git diff 7436fe3 dcb77e7` cho phần vá).
2. Review **không lọc** (chuẩn connector) theo bất biến I1–I11 của phần chung mà packet chạm và M1–M5 của đặc tả con.
   Mô hình tin cậy hạng Đ/H/R ở phần chung: readback R do người gọi lấy, máy chỉ kiểm nhất quán — nhưng I7 vẫn áp cho R.
3. Đối chiếu **từng** ca bắt buộc của mục `nghiem_thu` với ca `r834_*` tương ứng; với mỗi ca, đo đột biến `r834_*` khai trong
   `MUTANTS` có giết đúng ca ấy **đúng lý do** không (đọc tên ca + lớp ngoại lệ + thông điệp, không chỉ mã thoát; mutant chết vì
   traceback/CLI sập là tín dụng giả). Rồi tự đột biến thêm bản vá để tìm chốt **không** có ca nào bảo vệ.
4. Đặc biệt soi (gợi ý, không giới hạn): khớp `Reviewed commit:` theo tiền tố; finding của bot ở cả ba endpoint (review,
   review comment, issue comment) và review cũ/khác head; badge không/hai/ngoài miền; phần tử khác kho/PR; `_trang_du` (trang,
   `total_count`, id trùng); chọn run mới nhất + attempt mới nhất; job ↔ check-run (`check_run_url`, kho, app, suite) và việc gọi lại
   `cmd_kiem_gate`; `--workflow-jobs` nhiều tệp; `_slug_connector` (dùng lại `_du_dieu_kien_approve` cho biên nhận connector:
   có đúng tuple I10 không, `connector_refs` trùng/thiếu/thừa/sai kiểu); quyết định P3 (trùng, thiếu, thừa, sai kiểu); I4 — mọi
   từ chối giữ state nguyên byte, kể cả từ chối muộn; I5 — `_xet_dung` sau khi mọi đầu vào đã xác thực; I9 — đường cũ không đổi.
   Code hiện hành đã đổi sau ngày soạn đặc tả vì #929 (`_che_do_0054` quét theo cụm khai); nếu thấy đặc tả mâu thuẫn với code
   hiện hành thì nêu rõ.
5. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời** trong verdict, đừng tự soạn.

## Cách chạy

- Suite đầy đủ `python .claude/dev/packet_loop_test.py` tốn ~45 phút; ưu tiên chạy có chọn lọc:
  `python -B tham-chieu/chay_ca_va_dot_bien.py src r834_ r834_` (chạy ca theo tiền tố, rồi đột biến theo tiền tố, trên bản sao tạm;
  in `GIET/SONG/TIN_DUNG_GIA` kèm thông điệp). Chạy thêm `r812_` để kiểm I9/không hồi quy nếu thời gian cho phép.
- Nếu git toàn cục của sandbox có `commit.gpgsign=true`, cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
- `export PYTHONDONTWRITEBYTECODE=1`.

## Dạng verdict — ghi TĂNG DẦN vào `OUT/VERDICT.md`

Dòng 1 `Verdict: approve` hoặc `Verdict: request_changes`; dòng 2 `Reviewed commit: dcb77e78113ed66641771a82f404b713c9602d4d`;
dòng 3 `Spec sha256: c57ef4d8…` (đủ 64 ký tự) và `Chung sha256: 4e3d1e1b…` (đủ 64). Sau đó: bảng lớp — đếm theo nguyên nhân,
không theo số biểu hiện (`slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá`); bảng đối chiếu từng ca
bắt buộc; kết quả lệnh đã chạy với rc và bằng chứng dương. Ngưỡng approve: **không còn P0/P1/P2**. P3 còn lại nêu tên, hướng.
Verdict chỉ neo commit trên, không cấp quyền push/merge/land.

## Ngoài phạm vi (không tính hạng)

`mo-lai`, `cho_chu_kho`, checkpoint (#813) · vòng P3 (#814) · generation kế tiếp (#815) · ghi đẩy, kích hoạt (#816).
Packet này KHÔNG kích hoạt ADR-0054. Nợ P3 của #929 (`ls[0] == 0` trong `_che_do_0054` chưa có ca) không thuộc đặc tả này.
