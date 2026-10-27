verdict: changes_requested
reviewed_sha: 7ae7fc1ec1b8345115a4918aedefff6e45d20b2a
Kết quả: 0 P0, 6 P1, 2 P2, 0 P3.

Đã hoàn tất review tại SHA trên, tree `cf51019934695202163c3613dc88bb364a89b6fa`. Gate và suite hiện có xanh; các phản chứng dưới đây chứng minh chưa đạt trọn đặc tả. Giữ nguyên `cay-kho/`, không push, không gọi mạng. Mọi phép đổi code/fixture nằm ở bản sao ngoài cây được review.

## BẢNG ĐO
| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Exact SHA / spec | head 7ae7fc1, spec băm đóng băng | `rev-parse HEAD`, `sha256sum`: khớp đủ OID/băm | có |
| CLI head | rc=0; nợ 1/60/5; chưa đo 0 | `python3 ops/bien_nhan_v2.py --root .`, `gate-head.log`, `gate-ci.log`: đúng dòng và rc=0 | có |
| Full suite / m13 / m73–m82 | 76/76; 84/84; 2/2 | `test-suite-ci.log`: rc=0, đúng ba tỉ lệ trên origin/master=e139e55, không origin/HEAD; m13 và tất cả m73–m82 đều `giet_that` | có, trong phạm vi ca hiện có |
| Nợ rỗng | rc=1; 66 dòng | `python3 probe_debt.py`: rc=1; 60 L-ANCESTRY, 1 L-REVIEW, 5 L-SURFACE, unknown=[]; tập tuple khớp hằng | có theo thuật toán hiện tại |
| Sinh nợ | đúng khối hằng | `probe_debt.py` gọi `--sinh-no-cau-lich-su`: rc=0, `exact_block_equal=true`, `# 66 mục` | có |
| M1/A1, exact SHA | khác ký tự cuối không khớp; có mốc miễn | c69 đạt; m73/m74 giết c69; riêng mốc bị tẩy bằng sửa khoảng trắng (hướng 3) | chưa đạt toàn M1/Q7 |
| M2/A2, ba trạng thái | ancestor=1, ngoài=0, OID thiếu=2 | c71 đạt, m76/m77 giết c71; hướng 5 git/branch lỗi ra 2; hướng 3 và 6 phản chứng mốc/OID | chưa đạt toàn M2 |
| M2/A3, scalar | dấu/không dấu/folded/literal được nhận | c72 đạt; m78/m79 giết c72; đo riêng m78 vẫn bắt `khoi_gap`, chỉ mất `khoi_lit` (`probe-a3.log`) | hành vi cơ bản đạt; răng A3 folded khai quá rộng |
| M3/A4 | đối chiếu run.json, caveat; vắng run.json không áp | c73/m80 đạt; hướng 4 nguồn hỏng bị nuốt; hướng 7 bỏ khai báo thứ hai | chưa đạt toàn M3 |
| M4/A5 | nợ đóng băng/co, nợ chết phải xoá | c74/c75 đạt; m81/m82 giết đúng ca; hướng 4 lỗi đo bị ghi nợ chết | có răng cơ bản, sai phân loại nguồn hỏng |
| M5, từng chốt | mỗi chốt có test/đột biến | r1–r5 khác m73–m82: mỗi lượt 76/76, không ca đỏ (hướng 10); c73 không dựng lịch sử git thật (hướng 9) | không đạt |
| A6 base và head | cả hai sạch, test N/N; base+code mới+nợ rỗng đỏ | head và gate nền cũ rc=0; luật mới trên dữ liệu base e3ea139: nợ mặc định rc=0 (1/60/5), nợ rỗng rc=1 đúng 66 dòng, tập tuple bằng head (`probe-debt.log`); suite base rc=0, `68/68 · 74/74 · 2/2` (`test-suite-base.log`) | có |
| A7 nền trước thi công | A1–A5 chưa làm | `probe_debt.py`: tại base e3ea139 không có `_kiem_cau_lich_su`, không có `NO_CAU_LICH_SU`, không có c69–c76 | có |
| Ruff F / doctrine / diff | delta 0 / sạch / sạch | F541 cũ duy nhất ở base và head; doctrine rc=0 quét 10 tệp; `git -C cay-kho diff --check origin/master HEAD` rc=0 | có |

## BẢNG SĂN

HƯỚNG 1: tính toàn vẹn đầu vào và gate ban đầu
  giả thuyết : sai SHA/spec hoặc ref mặc định có thể làm phép đo lệch.
  lệnh       : `git -C cay-kho rev-parse HEAD`; `sha256sum cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN.md`; clone cục bộ `mirror.git` vào `/tmp/wp960-review-copy`, checkout exact SHA; `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .`.
  output     : HEAD `7ae7fc1ec1b8345115a4918aedefff6e45d20b2a`; spec `69394c7658db28196b72e3a1b00f4f6931ad9aba8b9fdcf76563fab33edaa671`; gate rc=0, `242 ĐẠT v2 · 11/11 miễn trừ legacy · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 295`; `câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 5 · L-SURFACE chua_do_duoc 0`; `TỔNG: ĐẠT`.
  kết luận   : KHÔNG PHẢI LỖI ở SHA/spec/gate ban đầu. Log: `gate-head.log`.

Ghi chú dữ kiện môi trường: khác lời mô tả trong prompt, `cay-kho/.git/refs/remotes/origin/HEAD` thực tế CÓ và chứa `ref: refs/remotes/origin/agent/wp960-g1-claude`, trỏ head packet. Clone thông thường từ mirror tạo `origin/master=e149e4a…` (nhánh local master của mirror), còn `cay-kho` có `origin/master=e139e55…`. Bản sao đã xoá `origin/HEAD` và ghim lại `origin/master=e139e55883d90fd74a358230be5599c9e223d4b3` để đo CI. Đây là dữ kiện chuẩn bị phép đo, chưa quy thành lỗi sản phẩm. Cây được review không đổi.

HƯỚNG 2: kiểm tra tĩnh và doctrine
  giả thuyết : thay đổi phát sinh lỗi F hoặc chép doctrine.
  lệnh       : `ruff check --no-cache --select F ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py`; `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git -C cay-kho diff --check origin/master HEAD`.
  output     : ruff có 1 F541 ở test dòng 1677 (đang đối chiếu nền); doctrine rc=0, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`; diff-check rc=0, stdout rỗng.
  kết luận   : KHÔNG PHẢI LỖI. Ruff trên `git show e139e55:ops/bien_nhan_v2{,_test}.py` có đúng cùng F541 ở dòng 1677: nền 1, head 1, delta 0.

HƯỚNG 3: mốc muộn và commit đầu tiên thêm câu
  giả thuyết : blame dòng hiện tại không chứng minh commit đầu tiên thêm câu.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 probe_fixtures.py anchors` (builder có sẵn `_kho_cau`, `_ghi_bn_cau`, `_kiem_cau` của c71; chỉ đổi fixture).
  output     : cả plain, folded `>-`, literal `|`, scalar trong list đều cho `add-anchor-only rc=1`, `same-sentence-whitespace rc=0`, `after-commit rc=0`; `chua_do=[]` ở tất cả. Ví dụ plain: first=`ede3cfadd60dc9d925cf81d9bd06bf7da61be8f7`, later=`6cdb1482486fb82e3e322ea0e94795988df04a77`. Câu chỉ đổi `chua vao` thành `chua  vao` và thêm `dung_tai: later`; theo chính `_cac_cau`, câu chuẩn hoá giữ nguyên.
  kết luận   : LỖI — mốc hậu sinh tẩy trắng câu lịch sử. Toàn output: `probe-anchors.log`.

Đo bổ sung hướng 3: chỉ đổi cách viết YAML (plain/list thêm dấu nháy, folded/literal đổi thụt đầu dòng), giữ **nguyên giá trị scalar sau parse**, rồi commit: đủ bốn kiểu đều in `exact-scalar-equal=True`, `YAML-only-format rc=0`. Đối chứng chỉ thêm mốc muộn vẫn rc=1. Đây không phụ thuộc cách hiểu khoảng trắng có tạo câu mới hay không; nội dung scalar giống hệt từng ký tự. `probe-anchors.log` chứa cả lượt đo bổ sung này.

HƯỚNG 4: nguồn surface hỏng và phân biệt ba trạng thái
  giả thuyết : có tệp mà không đọc được khác trường hợp A4 không có run.json.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 probe_fixtures.py surfaces` (đổi một nguồn trong fixture c73).
  output     : đối chứng `surface-mismatch rc=1`; đổi run.json thành `{`, `[]`, `{}` hoặc verdict thành byte `ff` đều cho `rc=0`, `chua_do=[]`; inject mục nợ L-SURFACE vào các ca nguồn hỏng lại cho `rc=1` cùng `NỢ CHẾT`, vẫn `chua_do=[]`. Run.json không tồn tại: `rc=0` và 1 mục `surface_chua_do`, đúng A4 khi không có nợ.
  kết luận   : LỖI — lỗi đo bị nuốt thành sạch hoặc gán vi phạm nợ chết. Log: `probe-surfaces.log`.

HƯỚNG 5: git hỏng, nhánh mặc định thiếu, object thiếu và YAML có alias vòng
  giả thuyết : mọi lỗi đo phải vào rc=2, không crash hay vi phạm thường.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 probe_fixtures.py measurement`.
  output     : `git-fails rc=2`, `merge-base-fails rc=2`, `branch-missing rc=2`, `moc-missing-object rc=2`, đều có mục L-ANCESTRY trong `chua_do`; thêm fixture `cycle: &self [*self]` thì `RecursionError maximum recursion depth exceeded`.
  kết luận   : LỖI ở YAML alias vòng; KHÔNG PHẢI LỖI với bốn đường git/object/branch đã đo. Log: `probe-errors.log`.

Bổ sung hướng 5: CLI thật trên fixture alias vòng trả **rc=1** với traceback cuối `RecursionError: maximum recursion depth exceeded`, thay vì rc=2 có thông báo KHÔNG ĐO ĐƯỢC.

HƯỚNG 6: ứng viên OID hợp lệ nhưng toàn chữ a–f
  giả thuyết : điều kiện bắt buộc có chữ số loại nhầm Git OID thật.
  lệnh       : `git -C /tmp/wp960-review-copy rev-list refs/remotes/origin/master` lọc prefix 7 hex toàn chữ ⇒ 10 commit; `PYTHONDONTWRITEBYTECODE=1 python3 probe_fixtures.py candidates` (fixture c71, nạp object qua fetch đường dẫn cục bộ).
  output     : `oid-prefix-resolves ecebffe9675d0952f3a0ab65eaa44087853a26bc`; câu với OID 40 hex này ⇒ rc=1, cùng câu với `ecebffe9` ⇒ rc=1, rút gọn còn `ecebffe` ⇒ rc=0, không có lỗi/unknown; `deadbeef` không tra được cũng ⇒ rc=0.
  kết luận   : LỖI — OID thật bị bỏ qua chỉ vì không có chữ số; OID không tra được cũng mất trạng thái thứ ba. Log: `probe-candidates.log`.

HƯỚNG 7: nhiều khai báo surface trên một dòng
  giả thuyết : M3 đòi bắt mọi dòng có surface khác, không chỉ token đầu tiên sau match đầu tiên.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 probe_fixtures.py surfaces`, thay đúng một dòng verdict của c73 thành `execution_surface: codex_cli; execution_surface: codex_service`.
  output     : `surface-two-fields-same-line {"rc": 0, "loi": [], "chua_do": [], "surface_chua_do": []}`, trong khi đối chứng chỉ khai `codex_service` ⇒ rc=1.
  kết luận   : LỖI — khai báo thứ hai khác run.json không được xét. Log: `probe-surfaces.log`.

HƯỚNG 8: tái đo suite và CI không có origin/HEAD
  giả thuyết : fallback origin/master bị sai khi checkout merge commit, hoặc test/đột biến cũ hỏng.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2_test.py`; `git update-ref refs/remotes/origin/master e139e55883d90fd74a358230be5599c9e223d4b3` và xoá symbolic `origin/HEAD` CHỈ trên bản sao; chạy lại CLI và full suite trên cấu hình ref ổn định này.
  output     : lượt đầu rc=0, `76/76 ca đạt · 84/84 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 66/84 đột biến thường khai đối chứng`; gate sau ghim ref rc=0, nợ 1/60/5, không unknown (`gate-ci.log`). Suite lặp sau ghim ref cũng rc=0, đúng `76/76 · 84/84 · 2/2`, `TỔNG: ĐẠT` (`test-suite-ci.log`).
  kết luận   : KHÔNG PHẢI LỖI: fallback origin/master làm việc trên exact merge commit 7ae7fc1 trong cây đầy đủ, không origin/HEAD. Đây là mô phỏng cấu hình ref checkout, không tự khai đã gọi GitHub Actions.

HƯỚNG 9: fixture A4 có lịch sử Git thật theo nghiệm thu hay không
  giả thuyết : lời khai ở test 2487–2488 và điều kiện nghiệm thu đòi mọi fixture có lịch sử thật.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 probe_fixtures.py acceptance`; gọi nguyên c73, quan sát builder `_cay`, chạy `git rev-parse --verify HEAD` với `GIT_CEILING_DIRECTORIES` chặn lẫn kho cha.
  output     : bốn fixture đều `git_rc=128`, `git_HEAD_exists=false`, `fatal: not a git repository (or any of the parent directories): .git`; c73 vẫn `('qua', None)`.
  kết luận   : LỖI — phạm vi ca test khai rộng hơn phép dựng fixture, không đạt tiền đề nghiệm thu. Log: `probe-acceptance.log`.

HƯỚNG 10: gỡ từng chốt mới khác m73–m82
  giả thuyết : vài chốt mới chưa có ca sẵn nào thực sự khoá.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_mutations.py`, bản sao clone từ mirror ở `/tmp/wp960-mutations`, exact head, origin/master ghim e139e55 và origin/HEAD vắng. Mỗi lượt thay một mẫu đúng 1 lần trong production, nạp lại, gọi toàn bộ `CA` qua `_chay_1`. Đo 76 ca chức năng; không coi việc phá anchor chuỗi của bộ tự tiêm m73–m82 là một ca nghiệp vụ bắt lỗi.
  output     : r1-moc-khong-doi-oid40, r2-luot-bien-nhan-khac-thieu, r3-merge-base-loi-thanh-vi-pham, r4-run-json-thieu-surface-thanh-vi-pham và r5-moc-blame-hong-thanh-vi-pham đều `{"passed": 76, "total": 76, "red": []}`. Đối chứng r6 bỏ fallback nhánh: 70/76, đỏ c40, c14, c71, c72, c74, c76, tất cả `giet_that`; script chứa nguyên văn mọi cặp neo/thay. Runner rc=0 là hoàn tất phép đo, không phải mutants được coi là đúng.
  kết luận   : LỖI — đủ năm chốt mới khác m73–m82 đã đo, chưa được ca nào khoá. Đối chứng nhánh mặc định có răng thật. Log: `probe-mutations.log`.

| đột biến reviewer | chốt gỡ | ca đỏ trong toàn bộ 76 CA |
|---|---|---|
| r1 | bỏ yêu cầu mốc đủ 40 hex ở 1135 | không ca nào; 76/76 |
| r2 | bỏ kiểm `luot` hỏng của receipt khác ở 1215 | không ca nào; 76/76 |
| r3 | bỏ phân loại lỗi merge-base ngoài 0/1 ở 1245–1247 | không ca nào; 76/76 |
| r4 | bỏ chốt run.json không có surface ở 1273–1275 | không ca nào; 76/76 |
| r5 | blame không đo được trả False thay None ở 1140–1141 | không ca nào; 76/76 |
| r6 | chỉ thử origin/HEAD, bỏ fallback origin/master/master ở 1102 | c40, c14, c71, c72, c74, c76; 70/76 |

HƯỚNG 11: nợ tại base và phép sinh khối hằng
  giả thuyết : 66 mục có thể được đóng băng từ head hoặc lệch dữ liệu base.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 probe_debt.py`; clone base e3ea139, giữ dữ liệu base, ghim nhánh mặc định bằng base, chỉ chép mã cổng head vào bản sao để áp luật mới, rồi khôi phục.
  output     : head+nợ rỗng: rc=1, 66 lỗi, tập tuple khớp hằng; sinh khối: rc=0, exact_block_equal=true, `# 66 mục`; base trước thi công không luật/mục nợ/ca c69–c76; base+luật mới+nợ mặc định: rc=0, 0 lỗi, nợ 1/60/5; base+luật mới+nợ rỗng: rc=1, 66 lỗi; unknown=[]; tập vi phạm base bằng head. Gate cũ trên base rc=0, `TỔNG: ĐẠT`.
  kết luận   : KHÔNG PHẢI LỖI về xuất xứ và sự khớp tập của 66 mục **theo bộ chọn hiện tại**. Những bỏ sót của bộ chọn đã ghi riêng, không lấy số 66 làm bằng chứng thuật toán nhận đủ mọi câu. Log: `probe-debt.log`, `gate-base-old.log`, `generated-debt.txt`.

Bổ sung hướng 11: suite gốc tại base e3ea139 đã hoàn tất rc=0, `68/68 ca đạt · 74/74 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 56/74 đột biến thường khai đối chứng`, `TỔNG: ĐẠT` (`test-suite-base.log`).

Bổ sung hướng 10 — chứng minh đột biến tác động đúng đường, không phải thay đổi vô nghĩa: `PYTHONDONTWRITEBYTECODE=1 python3 probe_guard_paths.py` dùng các builder c69/c71/c73 và bản sao `_dot_bien_tep` sẵn có. Output thực (`probe-guard-paths.log`): r1 mốc rút còn 7 hex: baseline rc=1 → mutant rc=0; r2 `luot` biên nhận sau là chuỗi: baseline rc=2 → mutant TypeError; r3 merge-base rc=127: baseline rc=2 → mutant rc=1; r4 run.json `{}`: baseline rc=0 → mutant rc=1 với surface None (cả hai vẫn sai trạng thái theo finding nguồn hỏng); r5 blame rc=127: baseline rc=2 → mutant rc=1.

HƯỚNG 12: đột biến m78 chết vì nhánh nào của c72
  giả thuyết : m78 có thể giết c72 bằng literal `|`, trong khi folded `>-` mà A3 yêu cầu không bị làm yếu.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 probe_fixtures.py a3`; áp nguyên đột biến m78 có sẵn bằng `_dot_bien_tep`, gọi nguyên c72 và quan sát trường vi phạm.
  output     : `m78-actual-fields ['co_dau', 'khoi_gap', 'khong_dau']`; c72 `giet_that` vì thiếu `khoi_lit`; **khoi_gap vẫn vi phạm** dưới đột biến. Log `probe-a3.log`.
  kết luận   : LỖI — m78 không chứng minh răng trên ca folded A3; tín dụng giết ca đến từ thể hiện literal bổ sung.

### moc-muon-tay-trang-cau-cu [P1] Sửa hình thức câu cho phép gắn mốc sau commit đầu tiên
TỆP/DÒNG: `ops/bien_nhan_v2.py:1109–1148`, trọng tâm 1126–1129.
VẤN ĐỀ: Q7 đòi mốc là tổ tiên của commit **đầu tiên** thêm câu. Mã lấy blame của dòng hiện tại, đổi dòng chưa commit thành HEAD. Chỉ thêm một khoảng trắng (bị chính `_cac_cau` loại khi chuẩn hoá) làm dòng bị blame vào HEAD/commit sửa hình thức; mốc quá muộn được công nhận. Đã đo câu sai trạng thái thoát L-ANCESTRY; cùng hàm kiểm mốc này cũng được L-REVIEW gọi tại dòng 1223.
ĐÃ THỬ NGHIỆM: `python3 probe_fixtures.py anchors`; thêm mốc muộn một mình ⇒ rc=1, sửa thêm `chua vao` → `chua  vao` ⇒ rc=0, commit thay đổi ấy vẫn rc=0. Đo thêm thay nháy/thụt dòng YAML, **giá trị scalar bằng hệt** (`exact-scalar-equal=True`), vẫn rc=0 sau commit. Tái hiện đủ plain, `>-`, `|` và scalar list. `probe-anchors.log` giữ SHA commit đầu/later và mọi output.
GỢI Ý: vá `_commit_them_cau` vì đây là nơi xác định nguồn gốc câu: truy lịch sử của câu đã chuẩn hoá đến lần thêm đầu, không lấy commit định dạng hiện tại làm mốc; không đo chắc thì trả trạng thái thứ ba. Khoá bằng fixture có câu ở commit A, commit B về sau, thêm mốc B kèm sửa khoảng trắng/reflow; phải còn rc=1 trước và sau commit. Đột biến quay về blame dòng hiện tại phải bị giết. Rủi ro: lịch sử rename, nhiều câu chung scalar và merge cần quy tắc nguồn gốc rõ để tránh kết tội nhầm.
ĐỘ TIN: cao.

### surface-hong-nguon-thanh-sach-hoac-no-chet [P1] Không đọc được nguồn surface bị coi là luật không áp
TỆP/DÒNG: `ops/bien_nhan_v2.py:1269–1279`, liên quan 1156–1164 và 1374–1377.
VẤN ĐỀ: A4 chỉ miễn trường hợp **không có run.json trong kho**. Tệp đã có nhưng JSON hỏng, kiểu sai, thiếu trường, hoặc verdict không giải mã được là lỗi đo. Mã đưa tất cả vào `surface_chua_do`, không vào `chua_cau`; `_ma_thoat` vì thế trả 0. Nếu có mục nợ, cùng lỗi đo biến thành `NỢ CHẾT` và rc=1, dù chưa chứng minh câu hết vi phạm. Đúng lớp lỗi R4-02.
ĐÃ THỬ NGHIỆM: `python3 probe_fixtures.py surfaces`; đối chứng sai surface rc=1; run.json `{` / `[]` / `{}` và verdict byte `ff` ⇒ rc=0, `chua_do=[]`; inject tuple nợ vào fixture nguồn hỏng ⇒ rc=1, `NỢ CHẾT`. Log `probe-surfaces.log`.
GỢI Ý: tại nhánh đọc run/verdict, tách vắng run.json được miễn theo A4 khỏi nguồn có mà hỏng; lỗi đọc/parse/schema phải ghi đúng tuple vào `chua` để chốt nợ chết không dùng sự thiếu bằng chứng. Khoá bằng cặp fixture có/không nợ, nguồn hỏng ⇒ rc=2 và không `NỢ CHẾT`; giữ ca vắng run.json không nợ ⇒ rc=0. Đột biến đưa lỗi đọc về `sf_chua` phải chết. Rủi ro: không được biến miễn trừ A4 thành lỗi hoặc làm phát sinh nợ giả khi nguồn không còn trong phạm vi.
ĐỘ TIN: cao.

### oid-hop-le-toan-chu-bi-bo-qua [P1] Bắt buộc có chữ số làm bỏ sót Git OID hợp lệ
TỆP/DÒNG: `ops/bien_nhan_v2.py:968–970`, dùng ở 1206–1208.
VẤN ĐỀ: M2 không giới hạn OID phải vừa có số vừa có chữ. Prefix thật `ecebffe` tra được commit trên origin/master nhưng bị regex loại. Cùng câu sai sự thật chỉ cần rút OID 8 xuống 7 hex là cổng xanh. OID toàn chữ không tra được cũng không vào rc=2 như M2 yêu cầu.
ĐÃ THỬ NGHIỆM: `python3 probe_fixtures.py candidates`; `git rev-parse ecebffe^{commit}` ⇒ `ecebffe9675d0952f3a0ab65eaa44087853a26bc`; câu dùng đầy đủ OID/`ecebffe9` ⇒ rc=1, dùng `ecebffe` ⇒ rc=0, dùng `deadbeef` ⇒ rc=0. Phép quét origin/master đo được 10 commit có prefix 7 toàn chữ. Log `probe-candidates.log`.
GỢI Ý: sửa bộ chọn OID tại `_RE_OID`, không thêm ngoại lệ theo tên; phân biệt ứng viên hex bằng ngữ cảnh và phép tra Git thay vì yêu cầu chữ số. Khoá bằng OID thật toàn chữ, OID toàn số, OID thiếu và sha256 không phải Git OID. Đột biến khôi phục lookahead chữ số phải chết. Rủi ro: từ ngôn ngữ tự nhiên cũng có thể chỉ chứa a–f; cần kiểm ngữ cảnh để không tạo rc=2 hàng loạt cho từ thường.
ĐỘ TIN: cao.

### yaml-alias-vong-lam-crash [P1] YAML hợp lệ có alias vòng làm CLI thoát 1 với traceback
TỆP/DÒNG: `ops/bien_nhan_v2.py:1069–1081`, gọi ở 1201–1203 và 1367.
VẤN ĐỀ: `_duyet_scalar` đệ quy trên đồ thị YAML mà không kiểm chu trình. `safe_load` chấp nhận alias vòng, `compose` giữ đồ thị đó; vòng duyệt mới gây RecursionError ngoài bộ phân ba trạng thái. CLI trả rc=1 thông thường và traceback, không trả rc=2/giải thích lỗi đo. Chỉ một trường phụ trong receipt có thể làm ngừng toàn sổ.
ĐÃ THỬ NGHIỆM: `python3 probe_fixtures.py measurement`, thêm `cycle: &self [*self]` vào fixture c71 ⇒ RecursionError; CLI thật cùng fixture ⇒ rc=1, stderr cuối `RecursionError: maximum recursion depth exceeded` (`probe-errors.log`).
GỢI Ý: canh chu trình bằng danh tính node trên stack duyệt tại `_duyet_scalar`, chuyển dữ liệu không duyệt được thành `KhongDoDuoc`/chua; không gộp thành lỗi nghiệp vụ. Khoá bằng alias vòng ⇒ rc=2, alias dùng lại nhưng không vòng vẫn được duyệt theo từng đường. Đột biến gỡ chốt vòng phải chết. Rủi ro: dùng một tập seen toàn cục sẽ bỏ qua alias hợp lệ ở mapping khác có mốc khác.
ĐỘ TIN: cao.

### surface-thu-hai-cung-dong-bi-bo [P1] Chỉ xét khai báo surface đầu tiên trên dòng
TỆP/DÒNG: `ops/bien_nhan_v2.py:1166–1172`.
VẤN ĐỀ: `.search` lấy một match, `next` lấy một token. Dòng có khai báo đúng trước và khai báo sai sau được kết luận sạch, dù M3 đòi caveat khi verdict có dòng khớp `execution[_ ]surface` với S' khác run.json. Thêm khai báo đúng phía trước làm mất cảnh báo của khai báo sai có sẵn.
ĐÃ THỬ NGHIỆM: `python3 probe_fixtures.py surfaces`; run.json `codex_cli`, verdict chỉ `execution_surface: codex_service` ⇒ rc=1; đổi đúng dòng verdict thành `execution_surface: codex_cli; execution_surface: codex_service` ⇒ rc=0, không unknown (`probe-surfaces.log`).
GỢI Ý: sửa `_surface_cua_verdict` để duyệt từng khai báo và lấy giá trị gắn với chính match đó, tránh tìm token lạc sang phần sau. Khoá bằng hai khai báo cùng dòng theo cả hai thứ tự; đột biến quay về `.search` đầu tiên phải chết. Rủi ro: văn xuôi giải thích/so sánh surface không được tự động đọc thành nhiều lời tự khai thiếu ngữ cảnh.
ĐỘ TIN: cao.

### chot-moi-chua-duoc-ca-nao-khoa [P1] Gỡ riêng các chốt mới mà toàn bộ 76 ca vẫn qua
TỆP/DÒNG: `ops/bien_nhan_v2_test.py:2605–2738`, bổ sung đột biến ở 3325 trở đi; các chốt production ở 1135, 1140–1141, 1215, 1245–1247, 1273–1275.
VẤN ĐỀ: M5 và phần nghiệm thu đòi từng chốt có răng. Năm đột biến độc lập đã hoàn tất, mỗi cái gỡ một chốt **khác m73–m82**, mà cả 76 ca có sẵn đều qua. Không chỉ là thay đổi vô nghĩa: đã đo các fixture chỉ đổi một yếu tố, cho thấy mutant nhận mốc 7 hex, crash với `luot` của receipt sau không phải số, hoặc chuyển lỗi đọc Git/nguồn thành trạng thái khác. Những đường mới này không được c69–c74 và các ca cũ khoá.
ĐÃ THỬ NGHIỆM: `python3 -u probe_mutations.py` trên clone `/tmp/wp960-mutations` tại exact SHA, từng mẫu khớp 1 lần, chạy toàn bộ `CA`; r1–r5 đều `passed=76,total=76,red=[]`. Đối chứng R6 chỉ còn 70/76, đỏ c40/c14/c71/c72/c74/c76 (`giet_that`). `probe_guard_paths.py` xác nhận baseline→mutant của r1: 1→0; r2: 2→TypeError; r3: 2→1; r4: 0→1; r5: 2→1. Bằng chứng: `probe-mutations.log`, `probe-guard-paths.log`; cặp neo/thay nguyên văn ở `probe_mutations.py`.
GỢI Ý: mở rộng c69/c70 kiểm `luot` hỏng ở **receipt khác**; c71 kiểm mốc 7 hex, lỗi `blame`, lỗi `merge-base` và ưu tiên rc=2; c73 kiểm nguồn có mà hỏng với/không mục nợ. Đặt kỳ vọng theo đặc tả, nhất là nguồn hỏng phải ra 2, rồi thêm từng đột biến r1–r5 vào bộ thử với đối chứng dương còn sạch. Rủi ro: assert exception hoặc giàn giáo hỏng không được lĩnh tín dụng giết chốt; giữ kiểm loại lỗi và đúng tuple luật/field.
ĐỘ TIN: cao.

### a4-fixture-khong-co-lich-su-git [P2] Ca A4 khai có kho Git thật nhưng chỉ tạo thư mục .git rỗng
TỆP/DÒNG: `ops/bien_nhan_v2_test.py:2487–2488`, 2697–2721; builder 237–247.
VẤN ĐỀ: phần nghiệm thu đóng băng yêu cầu mỗi ca dựng fixture trong kho Git tạm có lịch sử thật; chú thích test cũng khẳng định mọi ca làm vậy. c73 gọi `_cay` chỉ mkdir `.git`, rồi ghi run/verdict chưa commit. Ca hiện có đo so chuỗi trên filesystem, không đo tiền đề tệp và lịch sử của fixture trong kho như đã khai.
ĐÃ THỬ NGHIỆM: `python3 probe_fixtures.py acceptance` gọi nguyên c73; cả 4 fixture đều `git rev-parse --verify HEAD` rc=128, `.git/HEAD` không tồn tại; c73 vẫn qua. Chặn truy kho cha bằng `GIT_CEILING_DIRECTORIES`, không suy từ `/tmp/.git`. Log `probe-acceptance.log`.
GỢI Ý: đổi c73 dùng builder kho thật sẵn có, commit receipt/run/verdict của fixture dương rồi đổi đúng một yếu tố theo A4. Chốt dựng fixture phải xác nhận HEAD và object chứa nguồn; đột biến thay init/commit bằng mkdir cần làm ca đỏ. Rủi ro: đừng để chốt dựng fixture giết m80 trước khi nó tới phép so surface; giữ phân loại giàn giáo riêng.
ĐỘ TIN: cao.

### a3-mutant-chet-boi-literal-khong-phai-folded [P2] m78 không làm ca folded của A3 xanh như phép đo đặc tả yêu cầu
TỆP/DÒNG: `ops/bien_nhan_v2_test.py:2669–2686`, 3346–3349; `ops/bien_nhan_v2.py:1201–1204`.
VẤN ĐỀ: A3 yêu cầu răng của biến thể xuống dòng folded `>-` bằng đột biến khớp từng dòng thay scalar nối. m78 chỉ đổi `_cac_cau` sau khi `yaml.compose` đã gấp `>-` thành một dòng. Nó vẫn bắt `khoi_gap`; c72 đỏ do mất riêng trường literal `khoi_lit`. Dòng `giet_that` cho đúng tên c72 không chứng minh điều kiện folded được khoá bởi m78.
ĐÃ THỬ NGHIỆM: `python3 probe_fixtures.py a3` áp nguyên m78, gọi nguyên c72 ⇒ `m78-actual-fields ['co_dau', 'khoi_gap', 'khong_dau']`, rồi `giet_that` chỉ vì thiếu `khoi_lit` (`probe-a3.log`).
GỢI Ý: tách kiểm folded/literal trong c72 để mỗi răng có đích rõ; đột biến A3 cần làm yếu đường đọc raw YAML/compose thành chỉ xét các dòng vật lý để chính ca folded mất vi phạm. Giữ đột biến hiện tại cho chốt literal và diễn đạt đúng phạm vi. Khoá bằng kiểm đúng field folded thay vì chỉ thiếu một phần tử bất kỳ trong mảng bốn trường. Rủi ro: mutant phá parser toàn cục có thể giết ca vì YAML/giàn giáo hỏng; cần đối chứng một dòng vẫn qua và kiểm loại lỗi.
ĐỘ TIN: cao.

## Hiện vật và giới hạn phép đo

`test-suite-ci.log` là suite head trên cấu hình ref đã ghim; `test-suite-base.log` là suite gốc base; `gate-ci.log`, `gate-base-old.log`, `doctrine.log` lưu stdout/stderr thật. Các `probe-*.py` và `probe-*.log` giữ phép đổi fixture/chốt và output; `generated-debt.txt` là khối nợ sinh lại. Mọi script probe dùng builder/ca có sẵn, đổi code hoặc fixture trên thư mục tạm. Không sinh HINT.patch; hướng vá ghi ngay trong từng finding.

Chưa gọi GitHub Actions thật; phép đo CI ở đây là checkout exact merge commit đầy đủ lịch sử, origin/master=e139e55, không origin/HEAD. Không suy kết quả cho mọi cách viết tay ngoài những biến thể đã thử. Không có ca nào báo `Codex home is inside a repository` trong các suite đã chạy.

Kiểm cuối: `git -C cay-kho status --porcelain=v1` rỗng; HEAD và tree giữ nguyên như trên; `git -C cay-kho diff --check origin/master HEAD` rc=0. Bản sao đột biến đã tự khôi phục production, băm SHA-256 `ba13b46ceac9e9d9ca1eca2670395e94c3b79de417af480c71b150a331a9fb70` khớp `cay-kho/ops/bien_nhan_v2.py`, status bản sao rỗng.
