# Nhật ký review wp1236 r9 đợt A lượt 5

Đang đo, chưa kết luận.

reviewed_sha: 028f8b3681edf41386ce6d89858505993b4ac82c
tree: 82ecb2864344670de67461c8cc64a9b9a9cd3af1
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

Preflight khớp: sandbox review độc lập, origin ducthangho/tra-luat; base 0f9aa2a2cc697129e1f5be72feddf60986286865; ref spec 176feba3a09a4e86c6d8b06487f3e4224571be51 và local spec cùng băm; revision 9/generation 1; 3 tệp +1169/-0 ≤1200. Lease đến 2026-11-22T15:35Z. Review class sensitive. Reviewer openai_codex/codex_cli/machine, run 58c14bdb8b934d428241d3314802545e; model/effort phục vụ KHONG_DO_DUOC. Sandbox workspace-write, giữ repo read-only bằng thao tác.

## Tiến độ
- Đã đọc toàn bộ module và 31 ca/81 đột biến; đang chạy suite, audit từng ca đích, replay 19 mutant cũ và corpus.
- Bare Ruff 0.15.15, --no-cache --select F trên đúng ba tệp: rc=0, All checks passed.

- Corpus rc=0: 66 tệp 47/10/9; 170 hồ sơ 25/56/39/50, 94 landed, 0 lệch.
- Probe cũ và 8 script replay rc=0; F01/F02/F03/G01/H02 vẫn chặn đúng.
- Finding K01 dự kiến (lớp F04): drop_negative_claim_guard SỐNG 31/31; bản sao pr1378 chỉ đổi gate_output thành not_measured/skipped/not_run: mã gốc landed_khong_loi_khai_gate_output, mutant nhận []; mã gốc đúng đặc tả. Đang đo các biểu hiện khác và severity.

- Suite Python 3.13: rc=0, CA 31/31, DOT BIEN 81/81, TU KIEM PHAN HANG DAT (2), TONG DAT. Audit 81/81 GIET đúng ca; chi tiết audit.stdout. Nhiều mutant chỉ đổi lý do, không lật trạng thái: m6/m22/m23/m64/m66–m69/m71/m73/m79/m80.
- contrasts_luot5.py rc=0: bản sao pr1378 với token âm lọt mutant; bỏ hai phi lời khai chặn oan đối chứng; đổi fullmatch header/tổng nhận tệp không đúng grammar. Chưa thấy lỗi tương ứng trong mã gốc.

## Đối chiếu lượt trước (đang hoàn thiện)
- F01/F02/F03/G01: ĐÃ VÁ THẬT qua probes/walkerror/CLI; G02/H01 đã có audit ca đích, đang hoàn tất replay toàn bộ suite cho từng mutant.
- H02: ĐÃ VÁ THẬT — cả đường stat tệp và thư mục ENAMETOOLONG, Python 3.12/3.13 đều rc=2, không traceback.
- J01: ĐÃ VÁ THẬT — bốn mutant cũ đỏ rc=3 lần lượt a114/a204/a209/a116; các contrast tách riêng xác nhận gốc chặn và mutant nhận.
- J02: ĐÃ VÁ THẬT — drop_duplicate_skip đỏ rc=3 ở a103; không chỉ suy từ tổng 81/81.
- F04: CHƯA ĐÓNG LỚP — các biểu hiện cũ đã vá, nhưng drop_negative_claim_guard, drop_nonclaim_limits, drop_nonclaim_disposition, parser_partial_header đều SỐNG 31/31; đang hoàn tất các biến thể còn lại.

## Phân hạng tạm
- K01 P2, slug test-thieu-chot (tiếp F04/G02/H01/J01/J02): luật landed chỉ chấp nhận dương/waiver hợp lệ, hai ngoại lệ phi lời khai và fullmatch cấu trúc chưa có ca riêng. Đối chứng cho thấy mutant nhận sai hoặc chặn oan, không phải lỗi mã gốc.
- K02 dự kiến P3: bỏ lọc tên check passed / nới parser skipped chỉ đổi lý do not_measured; cổng vẫn từ chối. Không nâng lên P2 theo giả thuyết hậu quả.
- parser_partial_job là mutant tương đương với grammar hiện tại do nhóm (.*) cuối dòng; không tính thành finding.

## Môi trường và bằng chứng
- Python 3.13.18/PyYAML 6.0.3 và Python 3.12.3/PyYAML 6.0.1: cả hai suite rc=0, 31/31 và 81/81.
- CI yml khai Python 3.12, fetch-depth 0; ca archive thực chạy trên các OID ghim 8048551/bb47274/7f22121, symlink thực chạy trên POSIX; không có ca Linux skipped.
- Bare Ruff 0.15.15 rc=0, khác với Ruff CI contract 3/3 trong registration. Đăng ký regex khớp stdout suite đã đo.

- K01 đã xác nhận đủ 5 mutant sống 31/31: drop_negative_claim_guard, drop_nonclaim_limits, drop_nonclaim_disposition, parser_partial_header, parser_partial_summary. Cả năm có contrast qua kiem_ho_so, rc=0; không do lỗi setup.

- Kết thúc 8 mutant mới (new-mutants.json rc=0): 8/8 SỐNG 31/31, gồm 5 biểu hiện P2 (K01), 2 biểu hiện chẩn đoán P3 (K02), 1 mutant tương đương parser_partial_job không tính finding. Tất cả đối chứng đã chạy, logs contrasts5.stdout và diagnostic-contrasts.stdout.
- Replay 5 mutant lượt 4 hoàn tất rc=0; 5/5 CHẾT đúng ca, nên J01/J02 ĐÓNG. Bộ 14 mutant lượt 1–3 đang hoàn tất; các kết quả đã có đều chết rc=3 đúng ca.

# VERDICT wp1236 r9 đợt A lượt 5
reviewed_sha: 028f8b3681edf41386ce6d89858505993b4ac82c
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

## Finding lượt 1–4 của tôi còn mở

- F01: ĐÓNG — năm dạng YAML ngoài schema đều giữ đối chứng `passed`.
- F02: ĐÓNG — YAML/UTF-8 hỏng, symlink và lỗi duyệt đều trả `not_measured`, giữ lý do.
- F03: ĐÓNG — vòng alias trả CLI rc=2, không traceback; alias chia sẻ không vòng vẫn đọc được.
- F04: CÒN MỞ — các biểu hiện cũ đã vá, nhưng lớp `test-thieu-chot` còn K01/K02 bên dưới.
- G01: ĐÓNG — tiêm `PermissionError` bị chặn; `drop_walk_onerror` chết đúng a117.
- G02: ĐÓNG — hai mutant bỏ kiểm job trùng/readback duy nhất chết đúng a117/a209.
- H01: ĐÓNG — bỏ kiểm tổng số, trạng thái tổng và vế kết luận thứ hai chết đúng a110/a113.
- H02: ĐÓNG — đường dẫn tệp/thư mục quá dài trả rc=2, không traceback trên Python 3.12 và 3.13.
- J01: ĐÓNG — bốn mutant checkout skipped/đường tuyệt đối/readback symlink/symlink thư mục chết đúng a114/a204/a209/a116; đối chứng riêng qua consumer cũng khớp.
- J02: ĐÓNG — `drop_duplicate_skip` chết đúng a103; mã gốc giữ `job_lap`.

## Findings mới

- id: K01
  severity: P2
  vi_tri: ops/gate_output_doi_chieu_test.py:167; :429; :614
  van_de: Bộ test chưa bảo vệ riêng luật landed với token âm, hai ngoại lệ phi lời khai và yêu cầu khớp trọn header/dòng tổng; tiếp nối lớp F04.
  bang_chung: `python3 -B ../work/new_mutants_luot5.py` (rc=0): `drop_negative_claim_guard`, `drop_nonclaim_limits`, `drop_nonclaim_disposition`, `parser_partial_header`, `parser_partial_summary` đều SỐNG 31/31. `python3 -B ../work/contrasts_luot5.py` (rc=0): bản sao pr1378 chỉ khai `not_measured`/`skipped`/`not_run` bị mã gốc chặn nhưng mutant nhận `[]`; bỏ hai ngoại lệ khiến hồ sơ hợp lệ có metadata thật bị chặn `dinh_dang_loi_khai`; thêm hậu tố vào header/tổng của T-v3-pass bị mã gốc chặn nhưng mutant trả `passed`, hồ sơ `[]`. P2 vì thiếu ca bảo vệ các điều kiện đặc tả và đã đo được nhận sai/chặn oan trên mutant; mã gốc đúng.
  de_xuat: Bổ sung ba token âm trên hồ sơ landed vào a212, đủ ba tên phi lời khai vào a201, hậu tố thừa ở header/tổng vào a103; kiểm qua consumer, giữ đối chứng hợp lệ và thêm mutant riêng. Tránh để lỗi khác bắt thay hoặc siết nhầm grammar hợp lệ.

- id: K02
  severity: P3
  vi_tri: ops/gate_output_doi_chieu_test.py:167; :298
  van_de: Hai biến thể còn sống chỉ làm mất hoặc đổi chẩn đoán ở check bắt buộc và dòng skipped, cùng lớp F04.
  bang_chung: Cùng lệnh mutant (rc=0), `drop_k8_passed_name_filter` và `skip_legacy_job_parser` đều SỐNG 31/31. `contrasts_luot5.py` và `diagnostic_contrasts.py` (đều rc=0): mutant thứ nhất mất `check_bat_buoc:gate-registry (ubuntu-latest)`; mutant thứ hai đổi `dong_la` thành `co_job_skipped`. Cả hai vẫn `not_measured`, hồ sơ dương vẫn bị chặn; vì vậy P3.
  de_xuat: Thêm biến thể job bắt buộc `not_measured` với tổng nhất quán, và dòng skipped có hậu tố; đòi đúng lý do, giữ đối chứng hợp lệ và ưu tiên K8.

## Đã đo lại, khớp

- `python3 -B ops/gate_output_doi_chieu_test.py` và bản Python 3.12: rc=0; **CA 31/31 · DOT BIEN 81/81 · TU KIEM PHAN HANG: DAT · TONG: DAT**; stdout khớp regex đăng ký.
- Replay **19/19 mutant cũ chết**, đều rc=3 đúng ca. Audit **81/81 mutant của suite** đạt ca đích; một số chỉ chứng minh lý do đổi, không chứng minh quyết định cổng đổi. `parser_partial_job` là mutant tương đương do `(.*)` cuối regex, không tính finding.
- Corpus: **66 tệp = 47 passed/10 failed/9 not_measured**; **170 hồ sơ = 25 miễn cutover/56 đỏ/39 đạt/50 không lời khai**; 94 landed, lệch 0. Ba băm BO_SINH khớp 50 script thật (20/28/2). Chưa thấy mã gốc nhận lời khai dương sai ngoài các giới hạn đặc tả đã khai.
- K1–K8, API lời khai, điều kiện miễn và CLI đã đối chiếu; các probe cũ, đối chứng miễn, gom lý do và biên CLI đều hoàn tất. Ruff 0.15.15 trên ba tệp: rc=0. `ci_dang_ky_test.py`: rc=0, đăng ký 31/31, Ruff CI contract 3/3, phản chứng 1226/1226.
- `git diff --numstat origin/master...HEAD`: 3 tệp, +1169/−0 ≤1200. `git diff --check origin/master...HEAD`: rc=0. HEAD giữ nguyên; tree `82ecb2864344670de67461c8cc64a9b9a9cd3af1`; snapshot 17.333 tệp đầu/cuối không đổi, kể cả ignored.
- Linux; Python 3.13.18/PyYAML 6.0.3 và Python 3.12.3/PyYAML 6.0.1. Archive lịch sử và symlink đã chạy; không ca Linux skipped. CI khai Python 3.12, fetch-depth 0. Windows/CI từ xa: `not_run`; không gọi mạng.
- Reviewer `openai_codex / codex_cli / machine`, run `58c14bdb8b934d428241d3314802545e`; model/effort phục vụ `KHONG_DO_DUOC`; sandbox `workspace-write`, giữ checkout chỉ đọc bằng thao tác. Snapshot chỉ chứng minh không có delta giữa hai mốc.
- Báo cáo, script và log ở `work/VERDICT.md`; bảng đối chiếu ở `work/DOI_CHIEU_DAC_TA.md`, phân hạng ở `work/PHAN_HANG_DOT_BIEN.md`. Lớp F04 tiếp tục tái diễn; cần checkpoint theo protocol §8.3/§12.
KET_LUAN: changes_requested
