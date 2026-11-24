# VERDICT wp1236 r9 vòng 1
spec_sha256: ba466e72bb86c33462847c9ab92469d44acbf6bcc81b4443179d33c2e00940e7

## Findings

- id: R01
  severity: P2
  vi_tri: SPEC.md:62,189–201,305–306
  van_de: Luật cấm CR mâu thuẫn với census bắt buộc của A1-2, nên triển khai đúng đặc tả không thể qua nghiệm thu.
  bang_chung: `python3 -B work/audit_crlf.py` rc 0: hai tệp `pr1312…/danh-gia-gate-output-43466453500.txt` và `pr1317…/danh-gia-gate-output-43655477175.txt` có 27 CRLF/tệp ngay trong blob `8048551`; tham chiếu dùng `read_text()` tự chuẩn hóa nên cho passed. Thêm đúng luật cấm CR làm census thành **45/10/11**, hồ sơ thành **55/38/77**; bản sao chỉ đổi CRLF thành LF đều passed. Chi tiết: [audit_crlf.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-codex/work/audit_crlf.json).
  de_xuat: Chốt một chính sách thống nhất: nhận CRLF, chỉ từ chối CR lẻ và sửa A1-3; hoặc giữ cấm CR rồi sửa census A1-2, số hồ sơ và tập miễn trừ tương ứng. Không để executor tự đổi kỳ vọng khi thi công.

- id: R02
  severity: P2
  vi_tri: SPEC.md:192–194,207,215,244
  van_de: Ba đột biến m13, m22 và mC1 không làm đỏ đúng ca đích đã chỉ định.
  bang_chung: `python3 -B work/audit_r9.py` rc 0: run_id dạng chuỗi bị cả K2 chuẩn lẫn m13 chỉ so `==` từ chối; float cùng giá trị mới phân biệt được. [audit_path_target.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-codex/work/audit_path_target.json), phép đo rc 0: đường `../pr1453-wp433-provenance/…` vẫn bị chốt nằm dưới thư mục riêng từ chối sau khi bỏ kiểm `..`, nên m22 sống. C1 chỉ đòi “D2b không thiếu”; bỏ cả D2b bằng mC1 vẫn thỏa đúng kỳ vọng đó.
  de_xuat: Thêm run_id dạng float và attempt dạng bool/float; thử đường `extra/../<tệp hợp lệ>` vẫn phân giải bên trong thư mục để tách chốt cấm `..`; chuyển mC1 sang ca âm C2 hoặc thêm đối chứng âm vào C1. Giữ yêu cầu chết đúng ca và đúng lý do.

- id: R03
  severity: P2
  vi_tri: SPEC.md:266–272
  van_de: Khối nang_tran thiếu ba trường bắt buộc theo ADR-0053 mà đặc tả đã chọn áp dụng.
  bang_chung: ADR-0053, mục “Vượt trần MỚI”, đòi `ai_nang, can_cu, tran_cu, tran_moi`; `audit_r9.py` rc 0 đọc khối hiện có chỉ `can_cu, dot, thay_the, tran_de_nghi`. Đợt A tự ước lượng khoảng 600 dòng thêm, vượt 450.
  de_xuat: Bổ sung đúng hợp đồng: `ai_nang: ducthangho`, `tran_cu` 6 tệp/450 dòng thêm, `tran_moi` 3 tệp/650 dòng thêm; giữ căn cứ ước lượng và yêu cầu numstat thật trước review mã. Đây vẫn là đề nghị chờ chủ kho duyệt.

- id: R04
  severity: P2
  vi_tri: SPEC.md:123,244–246
  van_de: D2b bỏ neo attempt giữa M8 và tệp đánh giá, nên nhận evidence của lượt khác với lượt M8 khai.
  bang_chung: `python3 -B work/audit_attempt.py` rc 0: bản sao M8 thật của pr1231 khai run `42032872356`, `run_attempt: 2`, giữ merge SHA; tệp đánh giá và provenance nguyên bản đều attempt 1. `kiem_tep` vẫn passed, mọi vế D2b viết tại dòng 123 đều đúng, CLI D1–D4 hiện hành rc 0. Đối chứng attempt 1 cũng đạt. Đây là kiểm các vế thiết kế, không khai đã chạy mã D2b tương lai. Chi tiết: [audit_attempt.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-codex/work/audit_attempt.json).
  de_xuat: Đòi `ci_master.run_attempt` là int dương và bằng attempt của header/provenance; thêm ca thiếu, sai kiểu và lệch attempt, kèm đột biến riêng. Điều này giữ cùng job/attempt theo protocol §10.2.2 mà không cần đọc log hoặc gọi mạng.

- id: R05
  severity: P3
  vi_tri: SPEC.md:57,158,263–264
  van_de: Ba số đếm dùng làm căn cứ không khớp nguồn đã ghim.
  bang_chung: `python3 -B work/audit_r9.py` rc 0; `git ls-tree` và `git show` tại base cho **50 script = 20 v1 + 28 v2 + 2 v3**, không phải 49 = 19 + 28 + 2; `thamchieu.py` có **88 dòng**, không phải 95; bảng A có **38 ID đột biến**, thiếu m38, không phải 39. Chi tiết: [audit_r9.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-1-codex/work/audit_r9.json).
  de_xuat: Sửa các số và phân rã; nếu muốn đủ 39 đột biến thì định nghĩa thêm đột biến cùng ca đích thực sự phân biệt được.

## Đã đo lại, khớp

- SHA đặc tả khớp; reviewed SHA `89c07bc3fac42b059395f2947dd8992982e77161`, tree `524f7aca9a65bf502191ae279f658b476f62055a`; base `8048551a9b1eb886c126d2a1a4df0f95fb285964`.
- Hai lệnh tham chiếu `python3 -B ops/reviews/wp1236-r9-soan/{thamchieu,do_loi_khai}.py .` đều rc 0: đúng **47/10/9** và **53/40/77** theo tham chiếu; khác đặc tả ở R01. Sáu fixture cho đúng trạng thái/lý do đã khai; băm bộ sinh trong 66 header đúng **29/35/2**.
- `audit_history.py` rc 0: git archive hai commit `bb47274`, `7f22121` đều được; hồ sơ #1127 ở cả hai bản bị từ chối vì lời khai dương không có tệp danh-gia, đúng A2-11.
- Đã kiểm các khác biệt của tham chiếu: CRLF, job skipped lặp, kiểu số và symlink. Trừ mâu thuẫn R01, áp đặc tả chặt hơn; kết quả tham chiếu không chứng minh đã thực thi các chốt ấy.
- Hai OID ADR-0053/0055 tồn tại đúng điểm thêm tệp và nằm trên first-parent của origin/master được cấp. CI có checkout fetch-depth 0; phép đo không cần mạng; ca symlink chạy được trên Linux.
- Provider `openai_codex`, surface `codex_cli`, transport `machine`, run `16033899eb164087a1ab87ad75f46d67`; Python 3.13.18/PyYAML 6.0.3. Model/effort thực phục vụ: KHONG_DO_DUOC từ receipt hiện có.
- `passed`: các phép đo nêu trên; `failed`: các yêu cầu thiết kế/nghiệm thu ở R01–R04; `not_run`: mã triển khai r9, full CI, Windows, Ruff. Không có phép đo đã chạy bị skipped. Không sửa repository, không gọi mạng; cuối lượt 17.334 tệp tracked không đổi băm, diff/index rỗng. Ignored `.codex/` chỉ được liệt kê, không có snapshot byte đầu lượt để kết luận về phần này.

KET_LUAN: changes_requested
