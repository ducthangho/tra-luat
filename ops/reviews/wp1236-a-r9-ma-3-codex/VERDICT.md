# Nhật ký review wp1236 r9 đợt A lượt 3

Đang đo, chưa kết luận.
reviewed_sha: e323bd4dfb4fe422016c4fd010fa964b6cb748b0
tree: c9825e1e1ce716164656d32ea782d1f9ac69a8c9
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

Preflight khớp: origin ducthangho/tra-luat, nhánh sandbox, immutable baseline 0f9aa2a2cc697129e1f5be72feddf60986286865; spec r9/g1 khớp blob tại 176feba3a09a4e86c6d8b06487f3e4224571be51; lease còn hạn, sensitive; write set 3 tệp +1117/-0 <=1200. Ignored .codex/ có sẵn, không có delta tracked/untracked.
Reviewer openai_codex/codex_cli/machine theo run.json cc95d7e5648241d9acb70e701f443796. Model/effort phục vụ KHONG_DO_DUOC. Sandbox workspace-write; read-only bằng thao tác; mọi bản sao/script/log trong work. Không gọi mạng/GitHub.

## Số đo giữa lượt
- Ruff 0.15.15, ba tệp: rc=0. CI registration rc=0, 31/31; Ruff CI contract 3/3; phản chứng 1226/1226.
- Corpus rc=0: 66 tệp 47 passed/10 failed/9 not_measured; 170 hồ sơ 25 miễn cutover/56 đỏ/39 đạt/50 không lời khai; 94 landed, 0 lệch.
- Probes cũ rc=0: F01 các kiểu YAML ngoài schema đều passed; F02 YAML/UTF-8 hỏng và symlink đều not_measured; G01 walkerror = not_measured/PermissionError, consumer chặn. F03 vòng alias CLI rc=2, không traceback; chia sẻ alias không vòng hợp lệ.
- Waiver probes rc=0: đúng các tên điều kiện url/readback/doc_readback/html_url/tac_gia/dong_mien/han/os/sha; hai readback bị consumer chặn.
- Finding mới đã đo: CLI kiem-tep kiểm Path.is_file/is_dir ngoài biên try; tên thành phần >255 byte (lấy tên fixture thật lặp lại) ném OSError ENAMETOOLONG và traceback, rc=1 thay vì lỗi tham số có kiểm soát. Tái hiện cả Python 3.13.18 và 3.12.3. cli_edge_probe.py rc=0; child longfile/longdir rc=1, traceback=True; đối chứng missingdir rc=2, traceback=False.

- Suite Python 3.13 rc=0: CA 31/31, DOT BIEN 61/61, TU KIEM PHAN HANG DAT (2), TONG DAT. Audit riêng 61 đột biến rc=0, tất cả GIET đúng ca đích; m6 giữ giới hạn cũ: bo_sinh_la đổi thành KeyError ở K7, chỉ chứng minh oracle tên lý do.
- Đối chứng mới (new_contrasts.py rc=0): bỏ riêng kiểm tổng job hoặc trạng thái dòng tổng làm bản sao T-v3-pass tự mâu thuẫn đi từ not_measured/moc_lech thành passed, consumer không vi phạm. Đang chờ kết quả toàn bộ ca trên ba mutant mới.

## Đối chiếu hợp đồng
- Module: BO_SINH ba băm, CHECK_BAT_BUOC_TEN năm tên khớp AST packet_loop; regex/parser đóng, K1–K8, chuẩn hoá lời khai/ba ngoại lệ, token/bảy trạng thái, trích tên tệp và luật đường dẫn/landed đã đọc đối chiếu đặc tả. Các sai lệch bản tham chiếu cũ không được lấy làm chuẩn.
- contract_probe.py rc=0, 13 kiểm độc lập: token, ba tên phi-lời-khai, dạng landed/kiểu bool, gom nhiều lỗi K3–K6, job/skip trùng, positive/negative landed và tệp thường.
- CLI bình thường đủ rc 0/1/2/3 trong suite; lỗi tham số stat vẫn còn (H02). kiem_mien đủ tên lý do cố định và đúng thứ tự, đo helper lẫn consumer ở waiver_probes.py.
- Python 3.12.3 / PyYAML 6.0.1 suite rc=0, 31/31 +61/61 + tự kiểm2; Python 3.13.18 / PyYAML 6.0.3 tương tự. gate-registry CI ghim Python3.12, PyYAML6.0.3, fetch-depth0. Archive cần lịch sử và symlink cần POSIX, đều có trong CI Linux; Python cũ không là mục tiêu CI. Không cần mạng khi chạy bộ này. Không có ca skipped trong hai lượt Linux; Windows/CI từ xa not_run.
- diff --check rc=0. write_set_hash e348a0aec274cc000368e7b728a9a70423434e000ace619fbc059383907fb2f5 khớp lease; đăng ký chỉ thêm một mục.

## Lớp finding và tính liên tục
- yaml-ngoai-schema-bi-chan (F01, nguồn 1719d6e): đã đo, đóng.
- k2-mat-loi-doc (F02 → G01, nguồn 1719d6e/6f7ccf1): đã đo lỗi đọc/parse, symlink và walkerror, đóng.
- cli-vong-yaml-traceback (F03 → H02): biểu hiện vòng alias đã đóng; cơ chế thiếu biên ngoại lệ CLI còn ở bước stat của kiem-tep. Giữ slug nguồn; không coi chữa riêng alias là đóng mọi đường CLI.
- test-thieu-chot (F04 → G02/H01): head/schema/consumer miễn và job trùng/hai readback đã được kiểm; đang đo K7 từng thành phần và vế failed của K5. Không reset lớp chỉ vì đổi vị trí chốt thiếu ca.

- Audit chi tiết còn một giới hạn oracle: m22/m23 đỏ a204 vì lý do đổi từ tep_danh_gia_khong_hop_le sang danh_gia_khong_passed:...:symlink; fixture a204 tạo lk cho cả các vế nên K2 vẫn chặn sau khi bỏ chốt đường dẫn. Do đó 61/61 không có nghĩa mọi mutant làm trạng thái từ chặn thành pass; m6 cũng chỉ đổi tên lỗi. Đây là giới hạn bằng chứng, không gọi chúng là chứng minh false-acceptance.

- G02 hai biểu hiện đã ĐÓNG độc lập: drop_duplicate_provenance_job chết đúng a117 (30/31); drop_waiver_readback_count chết đúng a209 (30/31); đối chứng consumer từ fixture thật chứng minh original từ chối và mutant nhận passed/miễn. Các chi tiết đứng riêng trong extra-mutants.log, contrasts.log, waiver-probes.log.

### H02 — P2 — biên CLI (cùng lớp F03)
Vị trí ops/gate_output_doi_chieu.py:311. Path.is_file()/is_dir() chạy ngoài try, nên ENAMETOOLONG trả rc1 kèm traceback, trái hợp đồng lỗi tham số rc2 và không traceback. Cả nhánh đường dẫn tệp và --provenance tái hiện trên Python3.12/3.13; child rc1, traceback=True. cli_edge_probe.py rc0 là mã của script đo, không nhầm với child.
Đề xuất: bao bước kiểm tham số filesystem bằng biên OSError, in chẩn đoán có kiểm soát và trả2; ca riêng cho lỗi stat ở tệp/thư mục cùng đối chứng passed/failed/not_measured. Không đổi quy ước lỗi đọc bên trong kiem_tep vốn là not_measured/rc3.

### H01 — P2 — test-thieu-chot, tiếp nối F04
Đã xác nhận drop_summary_total SỐNG 31/31 (extra_mutants.py). a110 chỉ làm sai số passed, hoặc đổi trạng thái và số passed cùng lúc; không có biến thể chỉ đổi tổng job. Với bản sao T-v3-pass đổi dòng tổng thành passed (39/40), mã gốc not_measured/moc_lech, mutant bỏ riêng so tổng cho passed và kiem_ho_so=[] (new_contrasts.py rc0). Đặc tả K7 đúng; lỗi là bộ ca không bảo vệ từng thành phần bộ ba.
Đề xuất tách ca một biến đổi duy nhất ở từng thành phần (trạng thái, số passed, tổng job), kiểm qua kiem_tep và consumer, thêm mutant riêng giữ xanh đối chứng; tránh một vế khác của tuple bắt thay vế bị gỡ. Chưa sửa mã trong repository.

## Kết quả cuối lượt
- Đột biến riêng: 11 chết đúng ca, 3 sống. Chi tiết extra-mutants.log và từng *-results.json.
- Snapshot 17333 tệp không đổi (tracked/untracked/ignored), HEAD/tree giữ nguyên; diff index và worktree rỗng. Giới hạn: chỉ đo hai mốc, không chứng minh toàn bộ lịch sử; repo nguồn ngoài checkout không quan sát.
- Hash stdout cuối phiên và rc launcher do điều phối chốt sau khi phiên kết thúc; verdict không cấp quyền merge/land.

# VERDICT wp1236 r9 đợt A lượt 3
reviewed_sha: e323bd4dfb4fe422016c4fd010fa964b6cb748b0
spec_sha256: e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8

## Finding lượt 1–2 của tôi còn mở

- F01: ĐÓNG — năm dạng YAML ngoài schema đều giữ đối chứng `passed`.
- F02: ĐÓNG — lỗi YAML/UTF-8, symlink và lỗi duyệt đều được giữ, không còn trả `passed`.
- F03: CÒN MỞ — vòng alias đã sửa (rc=2, không traceback), nhưng lớp biên CLI còn thiếu xử lý lỗi kiểm đường dẫn; xem H02.
- F04: CÒN MỞ — các chốt head/schema/miễn đã có ca bảo vệ; còn đột biến sống ở K7 và một vế K5, xem H01.
- G01: ĐÓNG — `walkerror` trả `not_measured/PermissionError`; mutant bỏ `onerror` chết đúng `a117`.
- G02: ĐÓNG — `drop_duplicate_provenance_job` và `drop_waiver_readback_count` chết đúng `a117`/`a209`; đối chứng qua consumer cũng chặn đúng.

## Findings mới

- id: H01
  severity: P2
  vi_tri: ops/gate_output_doi_chieu_test.py:308
  van_de: Bộ ca không bảo vệ riêng trạng thái và tổng số job của dòng tổng K7; tiếp nối lớp F04.
  bang_chung: `python3 -B ../work/extra_mutants.py` (rc=0): `drop_summary_total`, `drop_summary_status` đều SỐNG 31/31. `python3 -B ../work/new_contrasts.py` (rc=0): trên bản sao T-v3-pass, chỉ đổi tổng thành `passed (39/40)` hoặc trạng thái thành `failed (39/39)` khiến mã gốc trả `not_measured/moc_lech`, nhưng mutant trả `passed`, `kiem_ho_so=[]`. `drop_failed_consistency` cũng SỐNG 31/31; biến thể này chỉ làm đổi lý do từ chối K5, chưa làm lời khai dương qua.
  de_xuat: Tại a110, thêm biến thể chỉ đổi một thành phần của bộ ba, kiểm cả kiem_tep và kiem_ho_so, kèm mutant riêng; tại a113, thêm conclusion khác success với trạng thái not_measured. Giữ đối chứng hợp lệ và tránh để một điều kiện khác bắt thay. Mã gốc K7 đúng đặc tả; cần sửa bộ test.

- id: H02
  severity: P2
  vi_tri: ops/gate_output_doi_chieu.py:311
  van_de: is_file/is_dir nằm ngoài biên bắt ngoại lệ, làm CLI kiem-tep in traceback và trả rc=1 khi tham số đường dẫn gây OSError, trái hợp đồng CLI; tiếp nối lớp F03.
  bang_chung: `python3 -B ../work/cli_edge_probe.py` (rc=0): đường dẫn có thành phần quá dài, dựng từ tên fixture thật, gây ENAMETOOLONG ở cả tệp và --provenance; tiến trình con trên Python 3.12.3/3.13.18 đều `rc=1, traceback=True`. Đối chứng thư mục vắng trả `rc=2, traceback=False`.
  de_xuat: Bắt OSError quanh bước kiểm tham số filesystem, trả rc=2 cùng chẩn đoán có kiểm soát; thêm ca riêng cho stat tệp và thư mục. Giữ quy ước lỗi đọc bên trong kiem_tep là not_measured/rc=3 và đối chứng passed/failed.

## Đã đo lại, khớp

- `python3 -B ops/gate_output_doi_chieu_test.py` và `/usr/bin/python3.12 -B ops/gate_output_doi_chieu_test.py`: rc=0; **CA 31/31 · DOT BIEN 61/61 · TU KIEM PHAN HANG: DAT · TONG: DAT**. Đầu ra khớp regex đăng ký. Audit riêng 61 mutant đạt ca đích; m6, m22, m23 chỉ chứng minh lý do đổi, không chứng minh trạng thái chặn đổi. Đột biến riêng: 11 chết đúng ca, 3 sống đã nêu ở H01.
- `review_probe.py corpus` (rc=0): 66 tệp = **47/10/9**; 170 hồ sơ = **25/56/39/50**; 94 landed, 0 lệch. Chưa tìm thấy lời khai dương thiếu provenance khớp lọt trên mã gốc ngoài giới hạn đặc tả đã khai.
- Probe lượt 1–2, `walkerror`, đối chứng waiver và 13 kiểm hợp đồng bổ sung đều hoàn tất rc=0; tên điều kiện miễn khớp. Các lỗi CLI mới được tách tại H02.
- Ruff 0.15.15, `python3 -B -m ruff check --no-cache --select F` trên ba tệp: rc=0. `python3 -B .claude/dev/ci_dang_ky_test.py`: rc=0; đăng ký 31/31, Ruff CI contract 3/3, phản chứng 1226/1226.
- `git diff --numstat origin/master...HEAD`: đúng 3 tệp, +1117/−0 ≤1200; `git diff --check origin/master...HEAD`: rc=0. HEAD giữ nguyên, tree `c9825e1e1ce716164656d32ea782d1f9ac69a8c9`; snapshot 17.333 tệp đầu/cuối không đổi, kể cả ignored.
- Linux; Python 3.13.18/PyYAML 6.0.3 và Python 3.12.3/PyYAML 6.0.1. CI khai Python 3.12, fetch-depth 0; archive và symlink đã chạy, không ca Linux nào skipped. Windows và CI từ xa: not_run; không gọi mạng/GitHub.
- Reviewer `openai_codex / codex_cli / machine`, run `cc95d7e5648241d9acb70e701f443796`; model/effort phục vụ KHONG_DO_DUOC; sandbox workspace-write, giữ checkout chỉ đọc bằng thao tác.
KET_LUAN: changes_requested
