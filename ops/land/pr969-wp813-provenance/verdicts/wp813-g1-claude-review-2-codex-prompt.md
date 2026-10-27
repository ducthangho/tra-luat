# Cross-review Codex — packet #813 (`MAY-ADR-0054-b`) revision 2 — lượt 2

Bạn là **reviewer độc lập, offline** cho Packet #813, revision 2, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context
executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa mã nguồn của packet; mọi phép thử (đột biến,
fixture, script) chạy trên **bản sao riêng** của bạn dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp prompt này: clone thường (`.git` là thư mục, không nông), detached tại head ứng viên
  **`79bbbdc16bd873f319ab70885039413735ee2fb3`**. Base = **`f577ab5b467510f3fa7ed27107dc2eab539d3bef`** (`origin/master` lúc
  cấp lease; ref `refs/remotes/origin/master` trong clone trỏ base). Thứ định danh tệp là **băm/SHA**, không phải tên nhánh.
- `OUT` = thư mục `out/` cạnh tệp prompt này, là nơi DUY NHẤT bạn ghi.
- Đặc tả con `tham-chieu/wp813-r2.md`, sha256 `9df36da1ef2be23c7519934bf6aee0dfecb6d2082cb8e485c7a6819c8a6154f3`.
  Tệp này chỉ có trên nhánh đặc tả, không có trong `SRC`, nên được chép sang đây; hãy băm lại.
- Phần chung (ràng buộc) `SRC/ops/specs/may-adr-0054-chung.md`, sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
- Lease (bản chép) `tham-chieu/lease-wp813-r2-g1-claude.yaml`. Write set gồm `.claude/dev/packet_loop.py` và
  `.claude/dev/packet_loop_test.py`. Diff ≤ 450 dòng thêm (ADR-0053).
- Đầu vào thiết kế, KHÔNG phải đặc tả: `tham-chieu/wp834-g1-codex-luot8-VERDICT.md` là verdict cuối của #834 trên cửa `accept`
  mà packet này dựa vào. Nợ `wp834-run-scoping-fields-unvalidated` của #834 được gộp vào đây thành M5.

## Vì sao có lượt 2 (ADR-0052: từ lượt hai phải nêu lý do)

Lượt 1 (`tham-chieu/wp813-g1-codex-luot1-VERDICT.md`, trên `d789393`) trả `request_changes` với 4 lớp P2:
`ci-reopen-run-context-unbound`, `checkpoint-spec-context-unbound`, `checkpoint-nested-scope-unvalidated`,
`r813-mutation-evidence-incomplete`. Executor đã vá trên head mới (`git diff d789393 79bbbdc` là phần vá).
Lượt này phải (a) đo lại từng lớp lượt 1 bằng chính các phản chứng của lượt 1 (hoặc tương đương) và nói rõ đóng hay chưa;
(b) review không lọc toàn bộ `git diff f577ab5 79bbbdc` như lượt đầu, vì bản vá đã đổi `_kiem_ci` (tham số `ket`) mà
`accept` của #834 dùng chung. Giữ nguyên slug của lượt 1 cho lớp nào còn mở; lớp mới thì đặt slug mới.

## Việc

1. Băm lại hai đặc tả. Xác nhận base là tổ tiên head. Đọc `git diff f577ab5 79bbbdc`.
2. Review **không lọc** (chuẩn connector) theo bất biến I1–I11 của phần chung mà packet chạm, và theo M1, M2, M3, M5 của
   đặc tả con. M4 (protocol) đã tách khỏi r2, không nằm trong packet. Mô hình tin cậy Đ/H/R ở phần chung: readback R do người
   gọi lấy, máy chỉ kiểm nhất quán, nhưng I7 vẫn áp cho R.
3. Đối chiếu **từng** ca bắt buộc trong mục `nghiem_thu` của đặc tả con với ca `r813_*` tương ứng. Với mỗi ca, đo xem đột biến
   `r813_*` khai trong `MUTANTS` có giết đúng ca ấy và **đúng lý do** không: đọc tên ca, lớp ngoại lệ và thông điệp, không chỉ mã
   thoát. Mutant chết vì traceback hoặc CLI sập là tín dụng giả. Sau đó tự đột biến thêm bản vá để tìm chốt **không** được ca nào
   bảo vệ.
4. Đặc biệt soi (gợi ý, không giới hạn):
   - `mo-lai`: điều kiện vào (approved_pending; running chỉ khi quyền mở lại hiện hành là `ci-do` cùng generation và cùng head);
     head lấy từ state chứ không từ người gọi.
   - Biên nhận H dùng lại `_du_dieu_kien_approve` với verdict `changes_requested`: có đúng tuple I10 không; `connector_refs` và
     `check_refs` trùng, thiếu, thừa, sai kiểu.
   - `connector` phải phủ **bằng đúng** P0–P2. Khi gọi `_doc_connector` với tham số mới `p0p2`, đường `accept` không truyền tham số
     ấy: kiểm rằng hợp đồng của `accept` không đổi.
   - `ci-do`: chọn lượt check-run mới nhất, lọc app/kho/head, danh sách kết luận cho phép.
   - Bộ đếm same-failure: bất biến `findings` trong `_load` nay tính cả sự kiện `mo_lai` trong history.
   - `_xet_dung`: `CUA_DI_TIEP` và cửa khép lượt.
   - Quyền `mo_lai_tu` và `checkpoint_day` theo I6 (neo, bị thay, mất sau khi dùng).
   - `chu-kho-duyet`: chỉ đọc `origin/master` sau fetch và đối chiếu `ls-remote`; lược đồ checkpoint; phạm vi
     `cho_phep_va` / `cho_phep_day`; dùng lại một hiện vật.
   - I4: mọi lần từ chối giữ state nguyên byte. I5: `_xet_dung` chạy sau khi mọi đầu vào đã xác thực. I9: đường cũ không đổi
     (state cũ không có `mo_lai_tu`/`checkpoint_day` vẫn đọc được).
   - M5: `_kiem_ci` kiểm kiểu của **mọi** run trước khi lọc.
   Nếu thấy đặc tả mâu thuẫn với code hiện hành thì nêu rõ.
5. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời** trong verdict, đừng tự soạn.

## Cách chạy

- Suite đầy đủ `python .claude/dev/packet_loop_test.py` tốn khoảng 45–60 phút. Ưu tiên chạy có chọn lọc:
  - `python -B -W ignore tham-chieu/chon.py src 'r813_*'` chạy các ca theo tên hoặc tiền tố `*` (gộp nhiều mẫu bằng dấu phẩy).
  - `python -B -W ignore tham-chieu/dotbien.py src r813_` chạy các đột biến theo tiền tố tên, đúng logic mục 3 của `main()` (ca
    đích, đối chứng khác họ, phân hạng tín dụng giả). Hãy đọc mã hai script này trước khi tin kết quả của chúng.
  - Chạy thêm `r834_` và `r812_` để kiểm I9 và không hồi quy, nếu thời gian cho phép.
- Muốn thử đột biến của riêng bạn: chép `SRC` sang `OUT/`, sửa bản chép, rồi trỏ hai script vào bản chép.
- Nếu git toàn cục của sandbox có `commit.gpgsign=true`, cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
- `export PYTHONDONTWRITEBYTECODE=1`.

## Dạng verdict — ghi TĂNG DẦN vào `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: 79bbbdc16bd873f319ab70885039413735ee2fb3`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>` và `Chung sha256: <đủ 64 ký tự>`.
- Sau đó là bảng lớp, đếm theo nguyên nhân chứ không theo số biểu hiện:
  `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá`.
- Bảng đối chiếu từng ca bắt buộc. Kết quả các lệnh đã chạy, kèm rc và bằng chứng dương.

Slug phải là kebab-case ổn định, đặt theo nguyên nhân, để các lượt sau so được. Ngưỡng approve: **không còn P0/P1/P2**. P3 còn lại
thì nêu tên và hướng xử lý. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

- Protocol §4/§12 (`cho_chu_kho` trong đồ thị): M4 của r1, làm sau khi #943 land.
- Vòng P3 (#814), generation kế tiếp (#815), ghi đẩy và tiêu thụ `checkpoint_day`/`mo_lai_tu` ở cửa đẩy (#816).
- Nợ P3 `required-mutation-coverage-missing` của #834, trừ khi chạm đúng chốt M5.
- Packet này KHÔNG kích hoạt ADR-0054.
