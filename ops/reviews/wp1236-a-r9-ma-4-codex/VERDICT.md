# Nhật ký review wp1236 r9 đợt A lượt 4

Đang đo, chưa kết luận.

reviewed_sha: b533028656dc2c4ac8de8751a9730f2d8b60d116
tree: 042f215b5dfe0465f1ce743dcaa1690a466dc80a
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

Preflight: origin đúng; nhánh sandbox là checkout review được giao; base 0f9aa2a2cc697129e1f5be72feddf60986286865; r9/g1; lease còn hạn; review_class sensitive. Đúng 3 tệp, +1131/-0 <=1200. Reviewer openai_codex / codex_cli / machine, run dfd564938ead4a049ef16184c8aac6dd theo run.json; model/effort phục vụ KHONG_DO_DUOC. Sandbox workspace-write; giữ checkout chỉ đọc bằng thao tác.

## Tiến độ đo
- probes rc=0: F01 YAML ngoài schema giữ passed; F02/G01 YAML/UTF-8/symlink/lỗi duyệt trả not_measured đúng lý do; vòng alias F03 trả rc=2, không traceback.
- cli_edge_probe rc=0 trên Python 3.13 và 3.12: tệp quá dài, thư mục quá dài, thư mục vắng đều rc=2 không traceback; H02 đóng.
- corpus rc=0: 66 tệp 47/10/9; 170 hồ sơ 25/56/39/50; 94 landed, lệch 0. Ruff và đăng ký CI rc=0.
- Suite Python 3.13 rc=0: CA 31/31, DOT BIEN 65/65, tự kiểm 2/2, TONG DAT; khớp regex đăng ký. Audit riêng 65/65 đúng ca đích; m6 giữ not_measured do KeyError, m22/m23/m64 chỉ đo thay lý do (không suy rằng trạng thái cổng đổi).
- Đối chứng lượt 4 rc=0: bốn mutant bỏ chốt checkout skipped-id, tuyệt đối, symlink thư mục provenance, symlink readback đều làm kiem_ho_so từ vi phạm thành []; mã gốc chặn đúng. Mutant checkout skipped-id đã xác nhận SỐNG 31/31; các mutant khác còn chạy bộ ca.

## Finding xác nhận trong lượt 4

J01 — P2, lớp `test-thieu-chot` (tiếp F04/G02/H01): bốn chốt được mục Module mới liệt kê chưa có ca âm độc lập. Các bản `drop_checkout_skip_membership`, `drop_absolute_path`, `drop_readback_symlink`, `drop_directory_symlink_reason` đều SỐNG 31/31. `contrasts_luot4.py` rc=0: mã gốc từ chối lần lượt provenance_chua_du, tep_danh_gia_khong_hop_le, waiver_khong_co_can_cu:readback, symlink; mỗi mutant cho kiem_ho_so=[] trên cùng bản sao fixture, gồm landed=True. Mã gốc thực hiện đúng các chốt; cần bổ sung test, không nới đặc tả. Căn cứ P2: chốt đặc tả không được bộ ca bảo vệ, và việc bỏ nó đổi kết quả consumer thành nhận lời khai không đủ điều kiện.

Vị trí ca: a114 (ops/gate_output_doi_chieu_test.py:366), a204 (:453), a209 (:519), a112/a116 (:336/:403). a204 dùng đường tuyệt đối không tồn tại nên không phân biệt bỏ chốt tuyệt đối với is_file; a209 không thử symlink readback; a116 chỉ thử symlink tệp, chưa thử thư mục; a114 thử not_measured nhưng chưa thử checkout skipped của job success.

Cách sửa: sửa bản sao fixture thật trong bốn ca để chỉ một chốt trượt, chạy cả helper và kiem_ho_so, giữ đối chứng hợp lệ, thêm bốn mutant tương ứng; mỗi mutant phải chết bằng TinHieuChotCa tại ca đích. Không sửa module để làm test dễ xanh, tránh chốt khác bắt thay (đặc biệt symlink có sẵn trong a204).

## Đối chiếu lớp lịch sử — đang chờ hoàn tất chạy đủ mutant riêng

| Slug | IDs | Kết quả hiện tại |
|---|---|---|
| yaml-ngoai-schema-bi-chan | F01 | ĐÃ VÁ THẬT; list/null/int/str/mapping ngoài schema giữ passed |
| k2-mat-loi-doc | F02, G01 | ĐÃ VÁ THẬT; ParserError/UnicodeDecodeError/symlink/PermissionError giữ đúng trạng thái và lý do |
| cli-vong-yaml-traceback | F03, H02 | ĐÃ VÁ THẬT; alias vòng và cả hai đường stat lỗi rc=2, không traceback |
| test-thieu-chot | F04, G02, H01, J01 | G02 và H01 đã vá đúng các biểu hiện; lớp F04 CÒN MỞ tại J01 |

Bốn lớp lịch sử, một lớp còn mở; J01 gồm bốn biểu hiện P2. Phép đo không chứng minh provenance/readback được ký hay log thật có dấu hiệu dương; đây là giới hạn được đặc tả chấp nhận. Không phát hiện lời khai dương lọt mã gốc ngoài phạm vi giới hạn đó.

J02 — P3, cùng lớp `test-thieu-chot`: `drop_duplicate_skip` SỐNG 31/31. Với bản sao T-skip nhân đôi một dòng skipped, mã gốc trả not_measured/job_lap, mutant trả not_measured/co_job_skipped. Chỉ mất chẩn đoán parser; K8 vẫn chặn, không có lời khai dương lọt hay hồ sơ hợp lệ bị chặn oan. Bổ sung ở a103 (:167) biến thể lặp skipped và lặp chéo job/skipped, kiểm đúng job_lap và thêm mutant; không sửa ngữ pháp hoặc ưu tiên K8. Không dùng biểu hiện này để nâng mức P2 của J01.

Đính chính vị trí ca trong ghi chú trên: a114 bắt đầu dòng 365; a209 dòng 522; a112 dòng 339; a116 dòng 404.

`python3 -B ../work/mutants_luot4.py` hoàn tất rc=0: cả 5 mutant mới SỐNG 31/31; không lỗi setup/import. `spec_matrix.py` rc=0: 50 script sinh thật = v1 20/v2 28/v3 2, tập hash đúng BO_SINH; failed ưu tiên skipped; lời khai âm không đủ cho landed; CLI tham số/help đúng rc.

- Suite Python 3.12.3 hoàn tất rc=0: CA 31/31, DOT BIEN 65/65, tự kiểm DAT, TONG DAT; không BO QUA trên Linux. `audit_controls.py` rc=0 xác nhận m38 làm đối chứng toàn CRLF từ passed thành not_measured/cr_le.
- Khác biệt môi trường ghi tại REVIEW_SCOPE.md: CI ghim PyYAML 6.0.3; Python 3.12 cục bộ có 6.0.1, Python 3.13 có 6.0.3. CI từ xa/Windows not_run; không giả chúng thành passed.

## Hoàn tất phép đo

14/14 mutant cũ chết đúng ca; 5/5 mới sống. Lớp `test-thieu-chot` nối F04/G02/H01/J01/J02, một lớp còn mở (P2 cao nhất), năm biểu hiện mới gồm bốn P2 và một P3. Snapshot cuối khớp đầu, 17.333 tệp. Xem REVIEW_SCOPE.md và các tệp *.json/*.stdout/*.stderr cho scope, command, rc và output.

# VERDICT wp1236 r9 đợt A lượt 4
reviewed_sha: b533028656dc2c4ac8de8751a9730f2d8b60d116
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

## Finding lượt 1–3 của tôi còn mở

- F01: ĐÓNG — năm dạng YAML ngoài schema đều giữ đối chứng `passed`.
- F02: ĐÓNG — YAML/UTF-8 hỏng, symlink và lỗi duyệt đều trả `not_measured`, giữ đúng lý do.
- F03: ĐÓNG — vòng alias và hai đường kiểm filesystem lỗi đều trả rc=2, không traceback.
- F04: CÒN MỞ — các biểu hiện cũ đã sửa; lớp thiếu ca bảo vệ còn J01/J02.
- G01: ĐÓNG — tiêm `PermissionError` không còn cho `passed`; `drop_walk_onerror` chết đúng a117.
- G02: ĐÓNG — hai mutant bỏ chốt job trùng/readback duy nhất chết đúng a117/a209.
- H01: ĐÓNG — `drop_summary_total`, `drop_summary_status` chết đúng a110; `drop_failed_consistency` chết đúng a113.
- H02: ĐÓNG — `cli_edge_probe.py` kiểm cả tệp/thư mục quá dài trên Python 3.12/3.13: rc=2, không traceback.

## Findings mới

- id: J01
  severity: P2
  vi_tri: ops/gate_output_doi_chieu_test.py:365; :453; :522; :404
  van_de: Bộ ca chưa bảo vệ độc lập bốn điều kiện đặc tả: checkout skipped phải thuộc job skipped, cấm đường dẫn tuyệt đối, cấm symlink readback và giữ lý do symlink thư mục provenance.
  bang_chung: `python3 -B ../work/mutants_luot4.py` (rc=0): `drop_checkout_skip_membership`, `drop_absolute_path`, `drop_readback_symlink`, `drop_directory_symlink_reason` đều SỐNG 31/31; `python3 -B ../work/contrasts_luot4.py` (rc=0): mã gốc chặn đúng từng trường hợp, mỗi mutant cho `kiem_ho_so=[]`. P2 vì các chốt được mục Module mới liệt kê chưa có ca bảo vệ; đây là lỗi độ phủ test, không phải lời khai đang lọt trên mã gốc.
  de_xuat: Thêm bốn biến thể từ fixture thật vào a114/a204/a209/a116, kiểm qua `kiem_ho_so` và thêm mutant tương ứng; dùng đường tuyệt đối có tệp thật, tách fixture để chốt khác không bắt thay, giữ đối chứng hợp lệ; không đổi luật module.

- id: J02
  severity: P3
  vi_tri: ops/gate_output_doi_chieu_test.py:167
  van_de: Bộ ca chưa bắt việc bỏ kiểm trùng ID ở nhánh dòng skipped của parser, cùng lớp F04.
  bang_chung: Hai lệnh trên đều rc=0: `drop_duplicate_skip` SỐNG 31/31; bản sao T-skip có dòng skipped lặp đổi từ `not_measured/job_lap` sang `not_measured/co_job_skipped`. P3 vì chỉ mất chẩn đoán; K8 vẫn chặn, chưa làm đổi kết quả nhận/từ chối hồ sơ.
  de_xuat: Thêm biến thể skipped trùng và trùng chéo job/skipped tại a103, đòi đúng `job_lap`, kèm mutant; giữ nguyên ưu tiên K8.

## Đã đo lại, khớp

- Suite trên Python 3.13.18 và 3.12.3: rc=0; **CA 31/31 · DOT BIEN 65/65 · TU KIEM PHAN HANG: DAT · TONG: DAT**; khớp regex đăng ký. Audit 65/65 đúng ca đích; m6/m22/m23/m64 chỉ chứng minh lý do đổi, không chứng minh trạng thái chặn đổi.
- Đột biến riêng cũ: **14/14 chết**, toàn bộ tín hiệu đỏ rc=3 của ca kiểm; mới: **5/5 sống** như J01/J02. Các probe cũ, đối chứng miễn và kiểm hợp đồng bổ sung đều rc=0.
- Corpus: **66 tệp = 47/10/9**; **170 hồ sơ = 25/56/39/50**; 94 landed, lệch 0. Ba hash BO_SINH khớp 50 script thật (20/28/2). Chưa tìm thấy lời khai dương lọt mã gốc ngoài giới hạn đặc tả đã khai.
- Ruff 0.15.15, `python3 -B -m ruff check --no-cache --select F` trên ba tệp: rc=0. `python3 -B .claude/dev/ci_dang_ky_test.py`: rc=0, đăng ký 31/31, Ruff CI contract 3/3, phản chứng 1226/1226.
- `git diff --numstat origin/master...HEAD`: đúng 3 tệp, +1131/−0 ≤1200; `git diff --check origin/master...HEAD`: rc=0. HEAD giữ nguyên; tree `042f215b5dfe0465f1ce743dcaa1690a466dc80a`; snapshot 17.333 tệp đầu/cuối không đổi, kể cả ignored.
- Linux; archive lịch sử và symlink đã chạy, không ca Linux skipped. CI khai Python 3.12 và fetch-depth 0. Windows/CI từ xa: `not_run`; không gọi mạng. Reviewer `openai_codex / codex_cli / machine`, run `dfd564938ead4a049ef16184c8aac6dd`; model/effort phục vụ `KHONG_DO_DUOC`; sandbox `workspace-write`, giữ checkout chỉ đọc bằng thao tác.
KET_LUAN: changes_requested
