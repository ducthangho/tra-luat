# Nhật ký review wp1236 r9 đợt A lượt 2

Đang đo, chưa kết luận.

reviewed_sha: 6f7ccf10f2441d0c97b779cfa77ff2839b56fc47
tree: cfa758558f5d725e4e7016d16745c0d4bf155353
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

Preflight: base 0f9aa2a2cc697129e1f5be72feddf60986286865; checkout sandbox; revision 9/generation 1; write set đúng 3 tệp, +1093/-0 ≤1100. Chỉ đọc checkout; scratch dưới work. Mạng/GitHub không gọi.

## Tiến độ phép đo
- Suite Python 3.13: rc=0; CA 30/30, DOT BIEN 58/58, TU KIEM PHAN HANG DAT (2), TONG DAT.
- Ruff 0.15.15: All checks passed; đăng ký rc=0, 31/31, Ruff CI 3/3, phản chứng 1226/1226.
- Corpus HEAD: 66 tệp = 47 passed/10 failed/9 not_measured; 170 hồ sơ = 25 miễn cutover/56 đỏ/39 đạt/50 không lời khai; landed 94, lệch 0.
- F01: đối chứng list/null/số/chuỗi/mapping ngoài schema đều passed, hồ sơ không vi phạm.
- F02: YAML hỏng ParserError; byte hỏng UnicodeDecodeError; symlink tệp/thư mục được giữ, tất cả not_measured; đang xét thêm lỗi duyệt thư mục.
- F03: bản sao pr1378 có vòng alias ra CLI rc=2, không traceback; alias chia sẻ không vòng đọc được.
- Hạn chế đo quyền: thử tiến trình con hạ UID gặp PermissionError tại os.setgroups; không coi là bằng chứng lỗi sản phẩm. Đã bỏ cách này, phép tiêm PermissionError vào os.scandir không đổi quyền.

## Findings đang chốt
- G01 / F02 / k2-mat-loi-doc (P2), ops/gate_output_doi_chieu.py:94: os.walk thiếu onerror nên nuốt PermissionError khi duyệt nhánh con. Bản sao fixture có hai provenance: bình thường not_measured/provenance_nhieu; tiêm PermissionError tại scandir của nhánh chứa bản thứ hai → passed, kiem_ho_so=[] (2 lần lỗi được tiêm). Tái hiện trên Python 3.13 và 3.12. Phải truyền lỗi duyệt về biên kiem_tep để not_measured/PermissionError; thêm ca đối chứng 0/1/2 provenance và lỗi duyệt. Không được đổi lỗi quyền thành provenance_0 hoặc passed.
- G02 / F04 / test-thieu-chot (P2), ops/gate_output_doi_chieu_test.py:613: drop_duplicate_provenance_job và drop_waiver_readback_count đều SỐNG 30/30. Fixture T-v3-pass sao thêm một phần tử job giống hệt: gốc not_measured/job_id_trung_provenance, mutant passed. Bản sao readback thật sửa dòng miễn cho hợp lệ, nhân đôi tệp: gốc waiver_khong_co_can_cu:readback, mutant []. Thêm ca consumer + đột biến riêng cho mỗi chốt, đòi lỗi đúng tên và đối chứng hợp lệ.

| Slug lớp | Nguồn lượt 1 / trạng thái lượt 2 | Phạm vi đã đo và điều kiện đóng |
|---|---|---|
| yaml-ngoai-schema-bi-chan | F01 / ĐÃ VÁ THẬT | list/null/số/chuỗi/mapping ngoài schema không chặn provenance hợp lệ. |
| k2-mat-loi-doc | F02 / VÁ HỜ ở cấp lớp | YAML/UTF-8 hỏng và symlink cũ đã sửa; G01 vẫn nuốt lỗi duyệt. Đóng khi lỗi scandir không cho passed và corpus giữ nguyên. |
| cli-vong-yaml-traceback | F03 / ĐÃ VÁ THẬT | vòng alias trên bản sao pr1378 ra rc2 không traceback; alias chia sẻ không vòng vẫn đọc được. |
| test-thieu-chot | F04 / VÁ HỜ ở cấp lớp | drop_head/schema/waiver_call đã chết đúng a108/a108/a209; G02 còn hai chốt không được bảo vệ. Đóng khi hai mutant mới chết đúng tính chất và baseline xanh. |

Nguồn lượt 1: 1719d6efb61433d92bbfba38f0a4add20a97be2b. Không đổi slug để reset lịch sử: 4 lớp tổng, 2 lớp đã đóng, 2 lớp còn mở với 3 biểu hiện hiện tại (G01 một, G02 hai). Các probe lượt 1 tái dựng từ VERDICT_LUOT1_CUA_BAN.md; script lượt 1 không được đính kèm trong đầu vào. Không phát patch sản xuất.

## Giới hạn bằng chứng
Snapshot chỉ chứng minh không có delta nội dung quan sát được ở hai mốc; không chứng minh chưa từng ghi rồi hoàn nguyên. Kho nguồn ngoài checkout không nằm trong phạm vi quan sát. Hash stdout và mã thoát cuối của launcher do điều phối chốt sau khi run kết thúc. Provider/surface/transport/run_id lấy từ run/f859bee1/run.json; model/effort không có bằng chứng phục vụ. Không gửi thông điệp ra GitHub.

## Hoàn tất phép đo
Suite 3.12 rc0 đầy đủ 30/30, 58/58, tự kiểm DAT, TONG DAT. Audit 58 mutant rc0, có đúng tín hiệu ca đích. Mutant độc lập 10/10 chạy xong rc0: 8 chết bằng TinHieuChotCa, hai sống là G02. Kiểm miễn qua helper và consumer trả đủ chín tên điều kiện cố định, head giống/khác đúng. CLI thiếu provenance rc2, không khớp provenance rc3.

# VERDICT wp1236 r9 đợt A lượt 2
reviewed_sha: 6f7ccf10f2441d0c97b779cfa77ff2839b56fc47
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

## Finding lượt 1 của tôi

- F01: ĐÓNG — YAML list/null/số/chuỗi/mapping ngoài schema đều giữ `passed`, không chặn oan đối chứng.
- F02: CÒN MỞ — YAML hỏng, UTF-8 hỏng và symlink đã được xử lý đúng; lỗi duyệt thư mục vẫn bị nuốt, xem G01.
- F03: ĐÓNG — vòng alias trên bản sao pr1378 trả CLI rc=2, không traceback; alias chia sẻ không vòng vẫn đọc được.
- F04: CÒN MỞ — `drop_head`, `drop_schema`, `drop_waiver_call` đã chết đúng a108/a108/a209; lớp thiếu ca bảo vệ chốt còn hai biểu hiện tại G02.

## Findings mới

- id: G01
  severity: P2
  vi_tri: ops/gate_output_doi_chieu.py:94
  van_de: `os.walk` không có `onerror` nên bỏ qua lỗi duyệt, cho `passed` dù chưa xác minh được tính duy nhất của provenance; tiếp nối lớp F02.
  bang_chung: `python3 -B ../work/review_probe.py walkerror` và bản Python 3.12 đều rc=0; bản sao fixture có hai provenance trả `not_measured/provenance_nhieu`, nhưng tiêm `PermissionError` tại `os.scandir` của nhánh chứa bản thứ hai khiến `kiem_tep=('passed', [])`, `kiem_ho_so=[]`.
  de_xuat: Truyền lỗi duyệt qua `onerror` về biên `kiem_tep` để trả `not_measured/PermissionError`; thêm ca tiêm lỗi cùng đối chứng 0/1/2 provenance, tránh đổi lỗi quyền thành kết quả sạch.

- id: G02
  severity: P2
  vi_tri: ops/gate_output_doi_chieu_test.py:613
  van_de: Bộ ca không bảo vệ chốt job_id trùng trong provenance và chốt đúng một readback miễn trừ; tiếp nối lớp F04.
  bang_chung: `python3 -B ../work/review_probe.py mutant <tên>` với `drop_duplicate_provenance_job` và `drop_waiver_readback_count` đều rc=0, SỐNG 30/30; `contrasts` và `waiver_probes.py` đều rc=0, chứng minh mã gốc chặn `job_id_trung_provenance`/`waiver_khong_co_can_cu:readback`, còn mutant nhận `passed`/`[]`.
  de_xuat: Thêm ca từ bản sao fixture có job trùng và hai readback, kiểm cả consumer `kiem_ho_so`; thêm hai đột biến riêng, đòi chết đúng lý do và giữ đối chứng hợp lệ.

## Đã đo lại, khớp

- `python3 -B ops/gate_output_doi_chieu_test.py` và Python 3.12: rc=0; **CA 30/30 · DOT BIEN 58/58 · TU KIEM PHAN HANG: DAT · TONG: DAT**. Audit từng ca đích đạt; riêng m6 chỉ chứng minh lý do đổi từ `bo_sinh_la` sang `KeyError`. Đột biến riêng: 8 chết, 2 sống.
- `review_probe.py corpus`: rc=0; 66 tệp = **47/10/9**; 170 hồ sơ = **25/56/39/50**; 94 landed, lệch 0. Chưa thấy trường hợp hoàn toàn thiếu provenance khớp mà lời khai dương vẫn qua ngoài giới hạn đặc tả; G01 làm mất bảo đảm duy nhất khi duyệt lỗi.
- Ruff 0.15.15, `python3 -B -m ruff check --no-cache --select F` trên ba tệp: rc=0. `python3 -B .claude/dev/ci_dang_ky_test.py`: rc=0, đăng ký 31/31, Ruff CI 3/3, phản chứng 1226/1226.
- `git diff --numstat origin/master...HEAD`: ba tệp, +1093/−0 ≤1100; `git diff --check origin/master...HEAD`: rc=0. HEAD giữ nguyên; tree `cfa758558f5d725e4e7016d16745c0d4bf155353`; hash 17.333 tệp đầu/cuối không đổi, kể cả ignored.
- Linux; Python 3.13.18/PyYAML 6.0.3 và Python 3.12.3/PyYAML 6.0.1. CI khai Python 3.12, fetch-depth 0; ca archive và symlink đã chạy. Windows và CI từ xa: `not_run`; không gọi mạng/GitHub. G01 đo bằng tiêm lỗi; thử hạ UID để đo quyền thật bị sandbox từ chối.
- Reviewer `openai_codex / codex_cli / machine`, run `f859bee1b70844738bbec8fed1d1e0b6`; model/effort phục vụ `KHONG_DO_DUOC`; sandbox `workspace-write`, checkout được giữ chỉ đọc bằng thao tác.
KET_LUAN: changes_requested
