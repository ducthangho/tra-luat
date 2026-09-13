verdict: changes_requested
reviewed_sha: dcd70395399808ef2acb02fae84993898bd3dccc
P1: 0
P2: 1

Kết luận cuối: **changes_requested — 0 P1 / 1 P2 / 0 P3**. Đã ghi 10 hướng săn tăng dần; giữ nguyên stable slug lớp A của lượt trước.

## ĐỐI CHIẾU LƯỢT TRƯỚC — đo ban đầu, không tính N

Lệnh: `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/check_previous.py` (rc=0); output đầy đủ: `review/logs/previous.log`.

- `rang-luot7-nhan-bo-khong-chay-la-nen-sach` [P3]: **ĐÃ VÁ THẬT** đối với finding cũ. Trước khi tin số đo, đột biến mã có sẵn cho `phan_chung()` trả False ngay: `chay = (False, 0, set())`; predicate nền từ chối (`False`).
- `ruff-phan-chung-ghim-nhan-tin-dung-tu-probe` [P2]: **ĐÃ VÁ THẬT**. Bỏ riêng chốt ghim consumer: `main_rc=1 count=111 unique=111 failed=['ruff-pin-required']`; các ca của năm cửa khác không LỌT.
- `ruff-khuon-chua-chung-minh-provisioning` [P2]: đã xác minh các ca cũ đổi màu đúng; chấm cuối sau khi săn biến thể mới. Mỗi mutant vẫn chạy 111 tên phân biệt và main rc=1. Cờ-trình → đúng 3 ca; toán-tử → đúng 2; probe-argv → đúng 1; env-giá-trị → đúng 1; env-phạm-vi → đúng 1. Sáu tập đích, kể cả chốt ghim, không giao nhau **trên fixture đã giao**. Chưa khái quát thành độc lập trên mọi đầu vào.

Đo nền riêng: `python3 -B cay-kho/.claude/dev/ci_dang_ky_test.py` rc=0, PHẢN CHỨNG 111/111; `python3 -B -m ruff check --no-cache --select F cay-kho/.claude/dev/ci_dang_ky_test.py` → All checks passed. Log: `review/logs/baseline.log`.

## BẢNG SĂN

HƯỚNG 1: Chuỗi TOML nhiều dòng của probe Ruff
  giả thuyết : Nếu cắt theo dòng vật lý trước khi xét dấu nháy, một argv cấu hình hợp lệ bị chia và mất probe. Biến thể mới: newline nằm TRONG chuỗi, không phải nối hai lệnh bằng &&/; ở lượt 8.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 1`
  output     :
```text
EXEC "python -m ruff --config 'line-length = 88\nindent-width = 4' --version" rc= 0 stdout= 'ruff 0.15.15' stderr= ''
argv= ['python', '-m', 'ruff', '--config', 'line-length = 88\nindent-width = 4', '--version']
product _dong_logic= [['python', '-m', 'ruff', '--config', "'line-length", '=', '88'], ['indent-width', '=', "4'", '--version']]
consumer= ["CI không in probe Ruff --version (job: ['gate-registry'])"]
```
  kết luận   : LỖI

HƯỚNG 2: Dấu # bên trong giá trị cấu hình Ruff
  giả thuyết : Nếu regex xóa comment không xét dấu nháy, dấu # là dữ liệu sẽ nuốt --version. Khác H1: một dòng duy nhất, nhánh xóa comment gây lỗi.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 2`
  output     :
```text
EXEC 'python -m ruff --config \'lint.dummy-variable-rgx = "^_#.*$"\' --version' rc= 0 stdout= 'ruff 0.15.15' stderr= ''
product _dong_logic= [['python', '-m', 'ruff', '--config', "'lint.dummy-variable-rgx", '=', '"^_']]
consumer= ["CI không in probe Ruff --version (job: ['gate-registry'])"]
unquoted comment control= [['python', '-m', 'ruff', '--version']] []
```
  kết luận   : LỖI

HƯỚNG 3: Tùy chọn module viết liền -mruff
  giả thuyết : Nếu chỉ tìm token -m riêng, lời gọi Python hợp lệ bằng tùy chọn ghép bị đọc thành cài hỏng. Biến thể chưa đo: -m có đối số gắn liền, không thêm cờ đứng trước -m như lượt 8 H3.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 3`
  output     :
```text
EXEC 'python -mruff --version' rc= 0 stdout= 'ruff 0.15.15' stderr= ''
recognition= False
consumer= ["CI không in probe Ruff --version (job: ['gate-registry'])"]
install is not execution= False
```
  kết luận   : LỖI

HƯỚNG 4: Env đã bị ghi đè vẫn bị tính là hiệu lực
  giả thuyết : Nếu cộng lỗi ở mọi scope thay vì hợp nhất theo thứ tự, PYTHONUTF8 xấu ở workflow vẫn làm đỏ dù cả ba job ghi đè thành 1. Khác các lượt trước: đo precedence giữa hai map, không đo riêng tên/giá trị.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 4`
  output     :
```text
workflow env= {'PYTHONUTF8': '2'}
job overrides= {'gate': '1', 'gate-registry': '1', 'gate-packet-loop': '1'}
effective PYTHONUTF8= 1
EXEC 'python -m ruff --version' rc= 0 stdout= 'ruff 0.15.15' stderr= ''
consumer= ["CI có env ngoài danh sách chứng minh được, nên đích cài Ruff không còn chứng minh được (job: ['gate', 'gate-packet-loop', 'gate-registry'])"]
helper= ['PYTHONUTF8=2']
```
  kết luận   : LỖI

HƯỚNG 5: Chuẩn hóa env khác cách Python đọc
  giả thuyết : Nếu strip/lower và allowlist codec không tương ứng runtime, giá trị có khoảng trắng có thể lọt trong khi alias codec hợp lệ bị chặn. Biến thể mới so lượt 8 H9: biểu diễn/chuẩn hóa, không literal 2 hay codec không tồn tại.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 5`
  output     :
```text
EXEC 'python -m ruff --version' rc= 1 stdout= '' stderr= 'Fatal Python error: preconfig_init_utf8_mode: invalid PYTHONUTF8 environment variable value\nPython runtime state: preinitializing'
value= ('PYTHONUTF8', ' 1 ') helper= [] consumer= []
EXEC 'python -m ruff --version' rc= 1 stdout= '' stderr= 'Fatal Python error: preconfig_init_utf8_mode: invalid PYTHONUTF8 environment variable value\nPython runtime state: preinitializing'
value= ('PYTHONUTF8', '1 ') helper= [] consumer= []
EXEC 'python -m ruff --version' rc= 0 stdout= 'ruff 0.15.15' stderr= ''
value= ('PYTHONIOENCODING', 'utf_8') helper= ['PYTHONIOENCODING=utf_8'] consumer= ["CI có env ngoài danh sách chứng minh được, nên đích cài Ruff không còn chứng minh được (job: ['gate-registry'])"]
EXEC 'python -m ruff --version' rc= 0 stdout= 'ruff 0.15.15' stderr= ''
value= ('PYTHONIOENCODING', 'UTF-8') helper= [] consumer= []
```
  kết luận   : LỖI

HƯỚNG 6: Comment --chay làm bước vô can bị soi env
  giả thuyết : Nếu bộ lọc env dùng substring trên run thô, chỉ thêm comment vô hại cũng đổi phạm vi. Khác lượt 8 H2: kiểm chính bộ lọc mới, cùng bước trước/sau chỉ khác comment.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 6`
  output     :
```text
unrelated step= cài actionlint cho G5
before comment= []
after comment= ["CI có env ngoài danh sách chứng minh được, nên đích cài Ruff không còn chứng minh được (job: ['gate-registry'])"]
logical commands unchanged= True
```
  kết luận   : LỖI

HƯỚNG 7: Registry dùng tab giữa tên tệp và tùy chọn
  giả thuyết : Nếu nhận registry bằng chuỗi nguyên văn, argv tương đương mất job_registry. Khác lượt 8 H7: một lời gọi duy nhất giữ vị trí, chỉ đổi dấu phân cách argv của REGISTRY.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 7`
  output     :
```text
argv equivalent= True
consumer= ['CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)']
```
  kết luận   : LỖI

HƯỚNG 8: Hai chốt cùng bắt một biến thể probe hợp lệ
  giả thuyết : Nếu sáu chốt chỉ độc lập trên fixture riêng, một probe module có -u sẽ đồng thời bị mutant cờ-trình và mutant probe-argv từ chối. Biến thể mới: tương tác hai cửa, không đo lại riêng sáu tập ca cũ.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 8`
  output     :
```text
EXEC 'python -u -m ruff --version' rc= 0 stdout= 'ruff 0.15.15' stderr= ''
original consumer= []
go-cua-co-trinh ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])", "CI không in probe Ruff --version (job: ['gate-registry'])", "CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
go-cua-toan-tu []
go-cua-probe-argv ["CI không in probe Ruff --version (job: ['gate-registry'])"]
go-cua-env-gia-tri []
go-cua-env-pham-vi []
go-chot-ghim-consumer []
SAME INPUT rejected by= ['go-cua-co-trinh', 'go-cua-probe-argv']
```
  kết luận   : LỖI

HƯỚNG 9: Con trỏ chú thích giữ nguyên bản gốc gate
  giả thuyết : Nếu tiết kiệm 28 dòng đã xóa hoặc đổi doctrine gốc, danh sách comment nguyên văn ở gate sẽ lệch origin/master. Đây là thay đổi riêng của head lượt 9.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 9`
  output     :
```text
whole gate comments before/after= 351 349 byte-identical= False
setup block byte-identical= True
comments moved with registry= ['      # Sổ ở ci_dang_ky_test.py được đối chiếu với phép tìm tệp trên cây. Các tệp dưới', '      # ops/reviews/** là hiện vật review bất biến, không phải mã sống để CI chạy.']
each moved line preserved exactly once= True
entire gate unchanged from round8= True
pointers= ["# evidence. Nó KHÔNG deselect test và KHÔNG thay promotion gate A2 — xem", "# Vì sao Windows có điều kiện: xem chú thích cùng chỗ ở job `gate` (bản gốc).", "# r226 — vì sao ghim `core.abbrev 7`: xem chú thích cùng bước ở job `gate`.", "# r226 — vì sao `fetch-depth: 0`: xem chú thích cùng bước ở job `gate`.", "# Vì sao cài trước phép test đầu tiên (G5/T6): xem job `gate`.", "# Vì sao Windows có điều kiện: xem chú thích cùng chỗ ở job `gate` (bản gốc).", "# r226 — vì sao ghim `core.abbrev 7`: xem chú thích cùng bước ở job `gate`.", "# r226 — vì sao `fetch-depth: 0`: xem chú thích cùng bước ở job `gate`.", "# Vì sao cài trước phép test đầu tiên (G5/T6): xem job `gate`."]
```
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 10: Toán tử shell được trích dẫn là dữ liệu
  giả thuyết : Nếu mất thông tin dấu nháy trước khi nhận toán tử, các đối số literal ;/&&/| bị chia thành lệnh. Biến thể chưa đo: toán tử là argv dữ liệu, không toán tử thực như lượt 8 H5; không dựng payload bypass.
  lệnh       : `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 10`
  output     :
```text
EXEC "python -c 'import sys; print(repr(sys.argv[1:]))' ';'" rc= 0 stdout= "[';']" stderr= ''
shell argv= ['python', '-c', 'import sys; print(repr(sys.argv[1:]))', ';']
product logical commands= [['python', '-c', 'import sys; print(repr(sys.argv[1:]))']]
EXEC "python -c 'import sys; print(repr(sys.argv[1:]))' '&&'" rc= 0 stdout= "['&&']" stderr= ''
shell argv= ['python', '-c', 'import sys; print(repr(sys.argv[1:]))', '&&']
product logical commands= [['python', '-c', 'import sys; print(repr(sys.argv[1:]))']]
EXEC "python -c 'import sys; print(repr(sys.argv[1:]))' '|'" rc= 0 stdout= "['|']" stderr= ''
shell argv= ['python', '-c', 'import sys; print(repr(sys.argv[1:]))', '|']
product logical commands= [['python', '-c', 'import sys; print(repr(sys.argv[1:]))']]
EXEC "python -c 'import sys; print(repr(sys.argv[1:]))' '|&'" rc= 0 stdout= "['|&']" stderr= ''
shell argv= ['python', '-c', 'import sys; print(repr(sys.argv[1:]))', '|&']
product logical commands= [['python', '-c', 'import sys; print(repr(sys.argv[1:]))', '|&']]
Scope: direct tokenizer defect; no end-to-end Ruff bypass claimed.
```
  kết luận   : LỖI

## ĐỐI CHIẾU LƯỢT TRƯỚC — cập nhật sau săn

- `ruff-khuon-chua-chung-minh-provisioning` [P2]: **VÁ SINH LỖI MỚI**. H1/H2/H10 chỉ ra bộ tách làm mất ranh giới trích dẫn; H5 chỉ ra `strip()` mới cho `PYTHONUTF8="1 "` qua sạch trong khi Python rc=1. H4/H6 đo phạm vi env chưa phản ánh môi trường hiệu lực. Các triệu chứng cùng lớp được giữ chung stable slug, không cộng mỗi hướng thành một finding.
- Sáu chốt: **độc lập trên đúng sáu tập ca được giao, chưa độc lập theo yêu cầu toàn miền đầu vào**. H8 dùng một probe hợp lệ duy nhất `python -u -m ruff --version`: bản gốc `[]`, gỡ cờ-trình làm 3 thông điệp lỗi, gỡ probe-argv làm 1 thông điệp lỗi; bốn mutant khác vẫn `[]`. H5 có đầu vào xấu mà consumer gốc không chốt nào bắt. Đây là phép mới về tương tác, không tính lại việc chạy sáu bộ ca cũ.
- Lớp B: đã chạy lại công cụ trích từ `origin/ops/cap-lease-463`, bộ test **13/13 rc=0**; đọc cặp SPEC-r21/LEASE-exec-2r10 với `--nghiem-ngat` → **rc=0, 0 chốt bỏ qua**. Log: `review/logs/contract-test.log`, `review/logs/contract-pair.log`. Sự tồn tại trên HEAD được kiểm riêng trước khi chấm cuối; kết quả nhánh phụ không chứng nhận bản HEAD.

Ghi chú rig H9: phép so nguyên danh sách comment trong gate ban đầu lệch 351→349 và assertion của rig đỏ. Đã kiểm diff: đúng hai dòng đi cùng bước registry sang job mới, vẫn nguyên văn mỗi dòng một bản. So đúng khối setup và đối chiếu gate với lượt 8 đều bằng byte. Đây là lỗi phạm vi phép so ban đầu, **không** ghi thành finding sản phẩm.

## ĐO BỔ SUNG — không tính N

`TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/corroborate.py` → rc=0 (`review/logs/corroborate.log`). Với env ở bước Ruff là `PYTHONUTF8="1 "`, bản gốc và cả sáu mutant đều trả `[]`. Main tĩnh trên **bản sao** workflow: rc=0, ĐĂNG KÝ 21/21, LAUNCHER WINDOWS 4/4, RUFF CI 4/4, PHẢN CHỨNG 111/111. H5 đã chạy Python thật với chính giá trị này và nhận fatal error rc=1. Không suy từ đây rằng toàn CI có thể xanh: phép main tĩnh không thực thi workflow.

A/B với mã lượt 8 cũng đã đo: `PYTHONUTF8="1 "` được cả hai bản nhận, nên đây là **lỗ chưa đóng ở giá trị chuẩn hóa**, không phải chứng cứ lỗi mới xuất hiện lần đầu tại head này. Ngược lại, `PYTHONIOENCODING=utf_8`: lượt 8 `[]`, head hiện tại có lỗi env, Python thật vẫn chạy Ruff rc=0. Chính chiều chặn oan alias codec là bằng chứng **VÁ SINH LỖI MỚI**.

`TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/audit.py` → rc=0 (`review/logs/audit.log`):

- HEAD/tree và merge-base khớp; diff +374/−88 và +126/−6 = **500 additions / 2 tệp**.
- Job fields, tiền tố 9 bước, đa tập dict bước sau loại riêng dòng comment thuần trong run, triggers, concurrency, timeout: đều True. Bốn mutant job-if / bỏ setup / bỏ on / bỏ timeout làm đỏ đúng phép liên quan.
- 40 → gate 38 / gate-registry 10 / gate-packet-loop 10. Ba context Ubuntu được suy từ job không có name; trạng thái ruleset trực tiếp chưa đo.
- Actionlint **1.7.12**, shellcheck **0.9.0**: ci.yml của snapshot origin/master và HEAD đều rc=0, 0 chẩn đoán, delta đa tập rỗng. Ca âm **đột biến mã có sẵn** tại lệnh printf của ops-don-ref: bỏ dấu nháy ở một biến → rc 1→1, số chẩn đoán 1→2, thêm SC2086. Log JSON/err giữ đầy đủ ở `review/logs/*-lint.*`. Không chứng nhận thay cho actionlint 1.7.7 mà workflow ghim.
- AST: chỉ hai hàm có sẵn đổi là `loi_ruff_ci` và `phan_chung`; các hàm mới là helper Ruff. `bang_chung_xanh`, `chay_moi`, `main` không đổi.
- Hai tệp lớp B trên HEAD: `git cat-file -e HEAD:<path>` đều rc=128. **CHƯA VÁ trên HEAD**, nhưng không mang chúng vào #463 là **đúng S1/A8**: write set đúng hai đường; thêm công cụ ops là đường thứ ba, bất kể còn bao nhiêu dòng. Không tạo finding để ép mở write set. Kết quả 13/13 của nhánh `origin/ops/cap-lease-463` chỉ là phép đo bản nhánh phụ.
- Hai bản ops (tài liệu và HEAD) cùng SHA256 `b56636d9c26d9b0f7b537d71e9a7edc7ef446e8c51ef0466fbc849a064497134`, HEAD bằng byte với base. Đã đọc đủ 2692 dòng bản cấp, gồm writer/reader, runner, 23 nhóm tự kiểm, bảng 76 mutant và main; không sửa tệp ops của cây review.
- Mirror bare và snapshot khớp **368 tên+OID**; không shallow, core.abbrev=7. Phép so trong sandbox không xác minh tính đầy đủ của ref trên GitHub trực tiếp.

Ghi chú rig cấu trúc: bản đầu so dict bước thô báo lệch; diff xác định đúng hai bản sao bước Force LF thay sáu dòng comment bằng một con trỏ, không đổi lệnh. Rig đã loại riêng dòng comment thuần để so lệnh; tính toàn vẹn comment được đo độc lập ở H9. Ca âm actionlint ban đầu chọn mỏ neo không có trong workflow; sửa mỏ neo sang biến có sẵn rồi mới chạy và tính số. Hai lỗi rig không phải finding sản phẩm.

## ĐỐI CHIẾU LƯỢT TRƯỚC — chấm cuối

| Finding / lớp | Chấm | Bằng chứng tự đo |
|---|---|---|
| `ruff-khuon-chua-chung-minh-provisioning` [P2] | **VÁ SINH LỖI MỚI** | Ca cũ có răng đúng; H1–H8/H10 còn phản ví dụ. A/B codec `utf_8`: lượt 8 nhận, head từ chối dù Python chạy rc=0. `PYTHONUTF8="1 "` là lỗ còn sót, cả hai bản đều nhận; không gọi nó là lỗi mới. |
| `ruff-phan-chung-ghim-nhan-tin-dung-tu-probe` [P2] | **ĐÃ VÁ THẬT** | Bỏ chốt ghim: main rc=1, 111 ca phân biệt, chỉ `ruff-pin-required` LỌT. Log `go-chot-ghim-consumer-main.log`. |
| `rang-luot7-nhan-bo-khong-chay-la-nen-sach` [P3] | **ĐÃ VÁ THẬT** | Known-answer trả False trước ca: `(False,0,set())`, predicate nền False; chạy công cụ nháp thật sau đó rc=0 và khớp phép đo riêng. |
| B — công cụ `ops/kiem_hop_dong_packet*.py` | **CHƯA VÁ trên HEAD; đúng S1/A8** | Cả hai path không tồn tại ở HEAD (rc=128). Bản trích nhánh phụ chạy 13/13, cặp spec/lease rc=0. Thêm chúng vào packet là thêm đường dẫn thứ ba; không yêu cầu làm vậy và không cộng finding phạm vi. |

Mỗi cửa cũ được kiểm bằng cả giá trị trả về của suite, số ca/tên phân biệt và rc main. Sự độc lập chỉ đúng trên fixture đích đã giao; H8 phủ định phát biểu rộng hơn bằng một đầu vào hợp lệ. Lớp A giữ stable slug từ lượt trước, không đổi tên để làm mất lịch sử lặp.

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được | Khớp? |
|---|---|---|---|
| SHA | dcd70395399808ef2acb02fae84993898bd3dccc | khớp đầu/cuối; tree e27b172ce2b77a0be2c78dc600460fbe636ff886 | Có |
| merge-base | bb7013c7669da19304a8769e5b25f8c1f8951e9c | khớp; snapshot origin/master là 32f95f0240df74e1ae7739ae1fe8d257686604bd | Có |
| spec / lease hash | decdb1a1… / 46182004… | khớp đủ SHA256 (audit.log) | Có |
| ĐĂNG KÝ | 21/21 | 21/21, rc=0 | Có |
| LAUNCHER WINDOWS tĩnh | 4/4 | 4/4; chưa chạy Windows | Có trong phạm vi tĩnh |
| RUFF CI nền | 4/4 | 4/4, rc=0 | Có trên workflow nguyên bản |
| PHẢN CHỨNG | 111/111 | 111/111, 111 tên phân biệt | Có |
| Ruff F | All checks passed | All checks passed, `--no-cache --select F` | Có |
| A8 tệp Python | +374/−88 | +374/−88 | Có |
| A8 workflow | +126/−6 | +126/−6 | Có |
| A8 tổng | 500/500, hai tệp | 500 additions, 94 deletions, hai tệp | Có; hết biên additions |
| Bộ nháp không nhận bộ không chạy | đã vá P3 | early return False bị từ chối trước khi dùng số đo | Có |
| Răng riêng của sáu mutant trên ca đích | các tập LỌT đúng và tách biệt | 3 / 2 / 1 / 1 / 1 / 1, mỗi mutant 111 ca, main rc=1 | Có trên fixture được giao |
| Sáu chốt độc lập trên đầu vào mới | phải độc lập | H8: cùng probe hợp lệ đổi màu dưới cả hai mutant cờ-trình/probe-argv | **Không** |
| Env chứng minh được thực thi | kiểm tên và giá trị | H5: `PYTHONUTF8="1 "` được nhận, Python fatal rc=1; `utf_8` chạy được lại bị từ chối | **Không** |
| Probe nhận dạng theo argv | dùng chung vị từ, bỏ so chuỗi | H1/H2: lexer làm hỏng argv trước khi vị từ chạy; H3 không nhận -mruff | **Không** |
| Phạm vi env chỉ ở bước liên quan | bước vô can không đỏ oan | H6: chỉ comment --chay đổi màu bước actionlint | **Không** |
| Bản gốc comment gate | giữ nguyên từng chữ khi thay bản lặp bằng con trỏ | setup nguyên byte so master; gate nguyên byte so lượt 8; hai comment dời theo registry còn đủ | Có |
| A2 cấu trúc | bảo toàn bước/lệnh, chỉ dời hai bước và nhân setup | 40 → 38+10+10, đa tập chuẩn hóa đúng; chỉ comment setup bản lặp đổi | Có ở mức cấu trúc |
| A2 kết luận trên hai lane | tập tên/nền/conclusion | chưa có phép chạy CI được phép | **KHÔNG ĐO ĐƯỢC** |
| A3/A4 | job fields, prefix9, on/concurrency, timeout=60 | tất cả đúng; bốn mutant làm đỏ phép tương ứng | Có cục bộ |
| Actionlint A/B | delta đa tập = 0 | rc 0→0, 0→0 chẩn đoán với 1.7.12 + shellcheck 0.9.0 | Có với toolchain này; 1.7.7 chưa đo |
| Ca âm actionlint | lỗi mới phải lộ dù rc không đổi | rc 1→1; SC1003 → SC1003+SC2086 | Có |
| doc-claims-check | sandbox từng rc=0; bằng chứng nền so nguồn ở 22f0e6f2 | tại head hiện tại rc=0, ok=true, 107 tệp, flags=0, 376 advisory, không bỏ lớp | Chỉ xác minh sandbox hiện tại; không đo cây nguồn bên ngoài |
| doctrine-scan | adapter yêu cầu sạch | rc=0, quét 7 tệp, 0 chỗ chép doctrine | Có |
| Ref trong bundle | 368, không shallow | bare = snapshot 368 tên+OID, không shallow, core.abbrev=7 | Có trong bundle |
| Ref GitHub trực tiếp | không đo được offline | không truy cập ngoài sandbox | **KHÔNG ĐO ĐƯỢC** |
| Lớp B trên head | cố ý không đưa đường thứ ba | vắng hai path; nhánh phụ 13/13, cặp spec/lease rc=0 | Đúng phạm vi; không gọi là đã vá trên head |
| Ops đã land, nghĩa vụ đọc | không thuộc write set | đã đọc; cùng byte với base/bản cấp; full cục bộ rc=0, 8/8, 10/10, 23/23 nhóm, 76/76 tự đột biến | Đã tự đo; không kết luận các nợ F/G cũ đã vá |
| A1/A5 | chủ kho cấm CI, KHÔNG ĐO ĐƯỢC | không phóng CI, không dùng thời gian head khác | **KHÔNG ĐO ĐƯỢC** |
| A6 live ruleset/readback trước merge | cần đủ ba context Ubuntu | đã xác định ba tên từ cấu trúc; chưa có readback live trong phạm vi đóng | **KHÔNG ĐO ĐƯỢC** |
| Cây được review | không sửa/commit | status rỗng, log reviewed_sha..HEAD rỗng, SHA/tree không đổi | Có |

Bộ ops: `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL="$PWD/review/gitconfig-empty" GIT_CONFIG_NOSYSTEM=1 python3 -B review/cay-thu/ops/nhanh_don_duoc_test.py` → **rc=0**. Output thật ở `review/logs/ops-suite.log`: `TU KIEM co dot bien rieng: 23/23 nhom bat buoc · dot bien giet 76/76`, `8/8`, `MUTANT: giet = 10 · khong giet = 0 · khong do duoc = 0 / tong 10`.

Cổng tài liệu: chạy trong `cay-kho/`, `python3 -B scripts/tl.py doc-claims-check --strict` → rc=0; `python3 -B cay-kho/.claude/dev/packet_loop.py doctrine-scan --root cay-kho` từ sandbox → rc=0. Đây là cổng cục bộ riêng lẻ, không là full CI.

## Finding

### ruff-khuon-chua-chung-minh-provisioning  [P2]  Hợp đồng Ruff còn làm hỏng argv và xác nhận sai môi trường thực thi

TỆP/DÒNG: `cay-kho/.claude/dev/ci_dang_ky_test.py:171` (chuẩn hóa env), `:178` (tokenizer mất dấu nháy), `:187` (cắt dòng vật lý), `:188` (xóa comment), `:197` (tách toán tử theo giá trị token), `:214` (nhận tùy chọn Python), `:313` (nhận registry bằng substring), `:324` (gom env theo substring). Chốt probe dùng kết quả ấy tại `:269`.

VẤN ĐỀ: Các ca lượt trước đã được sửa đúng, nhưng phép diễn giải lệnh/env vẫn không tương ứng với đầu vào thực thi. Các phép đo đều gọi trực tiếp consumer của sản phẩm; những probe Ruff dùng làm đối chứng được chạy thật trong sandbox, không cài pip hay chạy workflow.

- **Bỏ lọt giá trị env:** `PYTHONUTF8="1 "` hoặc `" 1 "` tại bước cài được `_env_khong_chung_minh` và `loi_ruff_ci` nhận (`[]`), nhưng Python chết ngay ở preinitializing, rc=1. Main tĩnh trên bản sao có đầu vào ấy vẫn **RUFF CI 4/4, PHẢN CHỨNG 111/111, rc=0**. `strip()` đã làm mất khác biệt mà Python thật coi là không hợp lệ.
- **Chặn oan do bản vá mới:** `PYTHONIOENCODING=utf_8` chạy thật `ruff 0.15.15`, rc=0; lượt 8 nhận, head này từ chối. Env workflow bị cả ba job ghi đè hợp lệ cũng vẫn bị cộng lỗi từ scope đã hết hiệu lực. Chỉ thêm comment `# --chay` vào bước actionlint với nhãn env vô hại khiến bước đó bị coi là liên quan tới registry (H4–H6).
- **Lexer và nhận dạng:** cấu hình Ruff TOML nhiều dòng hoặc chứa `#` trong dấu nháy chạy thật rc=0, nhưng parser lần lượt cắt chuỗi và xóa phần còn lại của argv, làm mất probe. `-mruff` hợp lệ cũng không được nhận. Đối số literal `;`, `&&`, `|` bị mất tại helper vì thông tin dấu nháy không còn khi so toán tử. Registry đổi riêng space thành tab có cùng argv mà bị báo không có job (H1–H3/H7/H10).
- **Tính độc lập được đòi trong PROMPT:** một probe hợp lệ `python -u -m ruff --version` được bản gốc nhận; gỡ cờ-trình làm consumer đỏ, gỡ probe-argv cũng làm đỏ cùng đầu vào. Hai cửa chỉ tách biệt trên bảng fixture đã chọn, chưa tách biệt ở miền đầu vào của hợp đồng (H8). Đầu vào whitespace env ở trên thì không chốt nào bắt.

Ảnh hưởng được chứng minh là sai âm/sai dương của **hợp đồng tĩnh Ruff**. Workflow nguyên bản vẫn qua cổng nền. Không có bằng chứng bypass toàn CI; env sai làm Python thật đỏ, và `--chay` không được thực thi trong phép main tĩnh.

ĐÃ THỬ VÁ: **có, chỉ một phần env trên bản sao** — đột biến bỏ thao tác trim khoảng trắng trước kiểm giá trị, thêm alias `utf_8` vào tập hiện có và kỳ vọng tập tương ứng. **0 dòng vật lý tăng**, diff phần Python so base vẫn **+374/−88**, cộng workflow giữ nguyên **+126** ⇒ **500 additions / 2 tệp**, đúng A8. Bản sao đã được trả về nguyên trạng sau đo. Đây là thử nghiệm chẩn đoán, **không phải gói vá đầy đủ**, không đóng finding và không giao patch gate để áp mù.

Phần còn lại đề xuất **bằng lời** theo PROMPT: thay chuỗi xử lý dòng/regex rồi mất dấu nháy bằng cách phân tích có giữ ranh giới trích dẫn và loại token; hợp nhất nhận dạng lời gọi registry với cách hiểu argv; tính env hiệu lực theo scope của từng bước thực thi; xác minh giá trị theo đúng cách runtime đọc. Cần xử lý miền shell không hỗ trợ theo một hợp đồng công khai, không âm thầm biến dữ liệu thành lệnh. Chi phí của **gói đầy đủ chưa đo**, executor phải thay thế/rút gọn trong chính hai path để giữ additions ≤500. Không đề nghị nâng trần lần thứ tư hoặc thêm đường thứ ba. Cùng hình dạng qua nhiều lượt cần xem lại cách biểu diễn hợp đồng theo §12, không chỉ nối thêm ca lẻ.

ĐÃ THỬ NGHIỆM: `python3 -B review/hunt.py 1` … `10` (mỗi lệnh tự ghi log và khối hướng); `python3 -B review/corroborate.py` → môi trường sai vẫn qua main 111/111; `python3 -B review/try_env_mutation.py` → main rc=0, 111/111, hai giá trị có khoảng trắng bị từ chối, `utf_8`/`UTF-8` được nhận, additions giữ 500. Xem `review/logs/h*.log`, `corroborate.log`, `env-partial.log`, `env-partial-main.log`. Dùng TMPDIR/PYTHONDONTWRITEBYTECODE như các lệnh đầy đủ phía trên.

ĐỘ TIN: **cao** với các đầu vào đã đo; không khái quát thành bao phủ mọi cú pháp shell, mọi codec hoặc mọi runner.

## Hướng chuyển điều phối bằng lời — KHÔNG ĐO ĐƯỢC, không tính N/P

1. **Luồng điều khiển của toán tử:** trên bản sao, lấy nguyên dòng cài Ruff sẵn có đặt vào nhánh chỉ thực thi khi lệnh trước thất bại; cho lệnh trước thành công, giữ probe và registry phía sau. Đối chiếu consumer với nhật ký thực thi trong môi trường ban đầu chưa có Ruff. Cần phân biệt “dòng có trong run” với “dòng đã chạy”; không tự soạn payload trong lượt này.
2. **Command substitution và tùy chọn kết thúc diễn giải của Python:** dùng mã/lời gọi đã có làm vật liệu, dựng biến thể mà chuỗi chứa từ Ruff nằm trong đối số dữ liệu hoặc trong chương trình `-c`, rồi hỏi riêng vị từ nhận lời gọi, chốt probe và tiến trình Python thật. Ghi rõ argv mà Python nhận và module có chạy hay không. Chưa dựng hay đo nên không kết luận có bypass.
3. **Here-document:** công thức đã được chuyển bằng lời ở lượt 8 vẫn chưa có probe được cấp trong sandbox này. Không lặp nó thành một hướng săn mới, không tính nó là đã đóng.

## Giới hạn, cách đếm và bàn giao

- **10 khối hướng đã ghi tăng dần**. Nếu gom H1/H2/H10 thành một họ lexer rộng, vẫn còn **8 hướng độc lập**: lexer; tùy chọn module ghép; precedence env; chuẩn hóa env; scope env theo comment; nhận registry; tương tác hai cửa; toàn vẹn comment sau rút gọn. Đo nền, sáu mutant cũ và đối chiếu lượt trước không tính N.
- Tổng finding cần xử lý của #463: **0 P1 / 1 P2 / 0 P3**. Giữ chung stable slug của lớp A, không đếm mỗi triệu chứng hay mỗi ca đỏ thành một lỗi riêng. Lỗi pin-test và công cụ nháp của lượt 8 đã vá thật.
- Reviewer: **Codex / OpenAI**, execution surface: **Codex service qua API**, transport: **machine**. Không có receipt runtime chứng nhận model/effort cụ thể trong bundle; không suy danh tính từ trường khai trong lease hay actor GitHub.
- Nghĩa vụ ops là **đọc**, cùng byte với base. Bộ cục bộ xanh dưới cấu hình Git trung hòa không chứng minh các nợ F/G về cấu hình ký và tái dùng kênh đã biến mất; không tuyên bố chúng đã vá, không mở write set để xử lý.
- `A1/A5` vẫn **KHÔNG ĐO ĐƯỢC** vì chủ kho cấm CI. A2 conclusions và A6 live readback cũng chưa đo trong phạm vi đóng. Không dùng log head khác để ghi đạt; không phóng workflow, push, commit, merge, gọi mạng hoặc đăng thông điệp ra ngoài.
- `do_rang_luot8.py` chỉ đổi ROOT/TAM để mọi tệp nằm trong sandbox. Mã đo, log và bản sao đều ở `review/`; cây `cay-kho/` không có sửa đổi/commit mới. Không sửa bare mirror.
- Verdict là hiện vật bàn giao trong sandbox theo PROMPT; chưa đăng PR hay cập nhật state/receipt. Yêu cầu đăng PR của adapter không mở phạm vi đọc/ghi đã bị PROMPT giới hạn.

Kiểm bất biến cuối: `review/logs/final-state.json` — bốn lệnh đều rc=0; status và log SHA..HEAD rỗng, HEAD/tree nguyên vẹn.
