# Nhật ký review wp1236 r9 đợt A lượt 1

Đang đo, chưa kết luận.

reviewed_sha: 1719d6efb61433d92bbfba38f0a4add20a97be2b
tree: 7a3db03ad9cdf461fd376629a06140291abbc308
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

Preflight: origin đúng; nhánh review sandbox sạch tracked/untracked, ignored .codex/ có sẵn; base 0f9aa2a2cc697129e1f5be72feddf60986286865; revision 9, generation 1, lease còn hạn; write set 3 tệp, +1076/-0 <=1100. Reviewer openai_codex/codex_cli/machine theo run.json f9f3c0c5789949439978def4d8dc6ae4; model/effort phục vụ KHONG_DO_DUOC; sandbox workspace-write, tuân thủ read-only bằng thao tác.

## Kết quả đã đo (đang bổ sung)
- Suite rc=0: CA 28/28, DOT BIEN 50/50, TU KIEM PHAN HANG DAT (2), TONG DAT.
- Registration rc=0: 31/31; Ruff CI contract 3/3; phản chứng 1226/1226.
- Corpus: 66 tệp = 47 passed/10 failed/9 not_measured. 170 hồ sơ = 25 MIEN_CUTOVER/56 DO/39 DAT/50 KHONG_LOI_KHAI.
- F01 P2 dự kiến, ops/gate_output_doi_chieu.py:105–108: YAML hợp lệ không phải mapping gây AttributeError thay vì bỏ qua schema; fixture T-v3-pass từ passed thành not_measured.
- F02 P2 dự kiến, ops/gate_output_doi_chieu.py:101–104,131: nuốt lỗi đọc YAML và xoá lý do symlink K2; bản sao fixture có YAML hỏng/UTF-8 hỏng vẫn passed, hồ sơ dương không vi phạm, trái hợp đồng exception và gom lý do.
- Test bổ sung drop_head/drop_waiver_call: cả 28/28 ca đều xanh (SỐNG). Đang đo thêm đối chứng và kiểm đường CLI.

- Phản chứng đã hoàn tất: probes rc=0; CLI trên bản sao pr1378 có vòng alias YAML ra rc=1, stderr có Traceback/RecursionError.
- Đột biến riêng: drop_head, drop_schema, drop_waiver_call SỐNG, mỗi bản 28/28. drop_run bị a101 bắt (27/28), đúng sai lệch provenance_0 → tap_job_lech.
- Đối chứng riêng rc=0: head/schema/run sai bị mã gốc chặn provenance_0, bản đột biến passed; readback MEMBER bị mã gốc chặn waiver_khong_co_can_cu:tac_gia, bản bỏ lời gọi kiem_mien trả [].
- Audit 50 đột biến rc=0, đều phân hạng GIET ở ca đích. Riêng m6: not_measured/bo_sinh_la → not_measured/KeyError tại tra nhãn K7; chứng minh tên lỗi đổi, chưa chứng minh trạng thái chặn phụ thuộc whitelist. Các 49 ca còn lại không lộ lỗi runtime.
- Python 3.12.3 / PyYAML 6.0.1: A1-2, A2-11, A2-13 đều rc=0. CI khai Python 3.12 + fetch-depth 0; Python 3.11.18 ở máy cũng có tarfile.data_filter. Không gọi mạng; Windows không chạy, không thuộc bắt buộc đợt A.

## Bảng lớp finding — lượt 1, cùng reviewed_sha

| Slug | Finding | Mức | Cơ chế và điều kiện đóng |
|---|---|---|---|
| yaml-ngoai-schema-bi-chan | F01 | P2 | Lọc kiểu/schema trước truy cập; list/null/số/chuỗi không ảnh hưởng provenance hợp lệ. |
| k2-mat-loi-doc | F02 | P2 | Không nuốt ngoại lệ hoặc xoá lý do; ca YAML/UTF-8 hỏng và symlink giữ lỗi đúng hợp đồng. |
| cli-vong-yaml-traceback | F03 | P2 | Kiểm vòng và biên lỗi CLI; không traceback với bản sao fixture có vòng. |
| test-thieu-chot | F04 | P2 | Oracle qua consumer thật cho head/schema/miễn; ba mutant còn sống phải bị bắt đúng lý do. |

Bốn lớp, sáu biểu hiện chính (F04 có ba chốt). Đây là lượt review mã đầu, không có finding lượt mã trước cần đối chiếu. Các giới hạn log/provenance/readback viết tay và neo commit hồ sơ đã khai trong đặc tả không được tính thành lỗi mới. Không dựng hay gửi patch sản xuất.

Snapshot chỉ chứng minh không có delta quan sát được giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên; không quan sát repository nguồn ngoài checkout được giao. Hash stdout cuối cùng của run và ma_thoat launcher phải do bên điều phối chốt sau khi phiên kết thúc.

# VERDICT wp1236 r9 đợt A lượt 1
reviewed_sha: 1719d6efb61433d92bbfba38f0a4add20a97be2b
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8
## Findings
- id: F01
  severity: P2
  vi_tri: ops/gate_output_doi_chieu.py:106
  van_de: chon_provenance gọi y.get trước khi loại dữ liệu không phải mapping, khiến YAML không thuộc schema chặn oan một hồ sơ hợp lệ.
  bang_chung: `TMPDIR=../work python3 -B ../work/review_probe.py probes` (rc=0): đối chứng T-v3-pass là passed; thêm YAML chứa bản sao danh sách checkout thì chon_provenance ném AttributeError, kiem_tep trả not_measured/AttributeError và kiem_ho_so báo vi phạm.
  de_xuat: Theo đặc tả, loại YAML không phải mapping hoặc không có schema ci_provenance/1 trước khi đọc trường; thêm đối chứng với list/null/số/chuỗi và mapping ngoài schema.
- id: F02
  severity: P2
  vi_tri: ops/gate_output_doi_chieu.py:103
  van_de: K2 nuốt ngoại lệ đọc YAML và xoá lý do đã gom tại dòng 131, trái hợp đồng trả not_measured khi có ngoại lệ và giữ đủ lý do.
  bang_chung: Cùng lệnh probes (rc=0): thêm bản sao provenance hỏng YAML hoặc UTF-8 vẫn cho kiem_tep=('passed', []), kiem_ho_so=[]; thêm symlink khiến chon_provenance trả ['symlink'] nhưng kiem_tep xoá lý do này.
  de_xuat: Không continue khi đọc/giải mã/parse thất bại; truyền ngoại lệ về kiem_tep để trả not_measured với tên ngoại lệ, giữ lý do từ chon_provenance và thêm ca kiểm cả thư mục có provenance hợp lệ lẫn tệp lỗi. Đặc tả là chuẩn; bản tham chiếu cũng nuốt lỗi không hợp thức hoá hành vi này.
- id: F03
  severity: P2
  vi_tri: ops/gate_output_doi_chieu.py:320
  van_de: CLI chỉ bắt lỗi nạp YAML, nên vòng tham chiếu do safe_load dựng ra làm loi_khai đệ quy vô hạn và in traceback, trái yêu cầu không traceback ở mọi đường.
  bang_chung: Lệnh probes (rc=0) sửa bản sao hồ sơ pr1378 rồi gọi kiem-ho-so: tiến trình con rc=1, Traceback=True, RecursionError: maximum recursion depth exceeded; stderr lưu tại ../work/cycle-cli.log.
  de_xuat: Phát hiện vòng tham chiếu khi duyệt và chuyển dữ liệu không xử lý được thành lỗi CLI có kiểm soát; thêm ca từ bản sao fixture, kiểm mã thoát và không có traceback.
- id: F04
  severity: P2
  vi_tri: ops/gate_output_doi_chieu_test.py:529
  van_de: Bộ ca chưa bảo vệ các chốt head/schema của K2 và đường kiểm miễn qua kiem_ho_so; A2-9 chỉ gọi helper nên không kiểm kết quả waiver_khong_co_can_cu mà đặc tả yêu cầu.
  bang_chung: `python3 -B ../work/review_probe.py mutant <tên>` với drop_head, drop_schema, drop_waiver_call đều rc=0, CA 28/28, RESULT SONG; `python3 -B ../work/review_probe.py contrasts` (rc=0) cho mã gốc chặn head/schema sai và readback MEMBER, còn các mutant nhận passed hoặc []. Mutant drop_run bị a101 bắt, 27/28.
  de_xuat: Thêm ca âm riêng cho head/schema, chạy các biến thể miễn qua kiem_ho_so, giữ đối chứng hợp lệ và thêm đột biến bỏ lời gọi; mỗi ca phải đỏ vì đúng chốt bị gỡ.
## Đã đo lại, khớp
- `python3 -B ops/gate_output_doi_chieu_test.py`: rc=0; CA 28/28, DOT BIEN 50/50, TU KIEM PHAN HANG DAT, TONG DAT. Audit riêng xác nhận đúng ca đích; riêng m6 đổi bo_sinh_la thành KeyError tại K7, nên chỉ chứng minh tên lỗi đổi, chưa chứng minh whitelist quyết định trạng thái chặn.
- `python3 -B ../work/review_probe.py corpus`: rc=0; 66 tệp = 47 passed/10 failed/9 not_measured; 170 hồ sơ = 25 miễn cutover/56 đỏ/39 đạt/50 không lời khai. Chưa tìm thấy lời khai dương thiếu hoàn toàn provenance khớp lọt qua mã gốc ngoài các giới hạn đặc tả đã khai.
- Ruff 0.15.15, `python3 -m ruff check --no-cache --select F` trên ba tệp: rc=0. `python3 -B .claude/dev/ci_dang_ky_test.py`: rc=0, đăng ký 31/31, Ruff CI contract 3/3, phản chứng 1226/1226.
- A1-2, A2-11, A2-13 đạt trên Python 3.12.3: 170 hồ sơ, 94 landed, 0 lệch. CI khai Python 3.12 và fetch-depth 0; không cần mạng. Symlink đã đo trên Linux; Windows not_run, không bắt buộc đợt A.
- `git diff --numstat origin/master...HEAD`: rc=0, đúng ba tệp, +1076/-0 ≤1100; `git diff --check origin/master...HEAD`: rc=0. HEAD giữ nguyên; tree 7a3db03ad9cdf461fd376629a06140291abbc308; hash 17.333 tệp đầu/cuối không đổi, kể cả ignored .codex/ có sẵn.
- Reviewer openai_codex / codex_cli / machine, run f9f3c0c5789949439978def4d8dc6ae4; Linux, Python 3.13.18, PyYAML 6.0.3. Model/effort phục vụ KHONG_DO_DUOC. Sandbox workspace-write; checkout được giữ chỉ đọc bằng thao tác. Không gọi GitHub/mạng; CI từ xa not_run.
KET_LUAN: changes_requested
