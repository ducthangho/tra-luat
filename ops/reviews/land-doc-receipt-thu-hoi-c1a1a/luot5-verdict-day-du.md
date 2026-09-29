**0 P1 / 0 P2 / 4 P3**

verdict: changes_requested

```yaml
packet: LAND-DOC-RECEIPT-THU-HOI-C1a1a
issue: 650
review_round: 5
reviewed_sha: de927ca4a6e6b516edd68a5df43678a1832aba13
reviewed_tree: 553a3f45ca392a93a85d476f5a5283d8131ae8ce
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
spec_revision: 5
spec_sha256: 978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
receipt_sha256: ca67dc6a817b7cf8643616e4762d5f3e95c0ec7a46cf9693f9436b47c00f5960
review_class: sensitive
assurance: advisory_review
provider: openai_codex
execution_surface: codex_cli
transport: machine
executor: Claude (theo assignment)
review_axes: [spec, standards_security]
```

Các định danh trên được đo bằng `git rev-parse HEAD 'HEAD^{tree}' origin/master` và SHA-256 của bytes spec/receipt, khớp đầu–cuối. Bản ghi cuối: [facts-final.json](facts-final.json), lúc **02:17:30 UTC ngày 28-09-2026**. Áp dụng authority trực tiếp của chủ kho trong assignment: thêm lượt 5 sau head drift, trần sản phẩm ≤650 dòng, mục tiêu hết P1/P2/P3. Không dùng trần 4 hoặc trần 400 cũ để bác chỉ thị mới.

**Các phản chứng nguyên thủy F30–F32 đều đã bị chặn.** Tuy nhiên bản vá còn hai vấn đề trong cơ chế oracle/probe; thêm một lỗi cấu hình Python và một nợ hiện vật ngoài phạm vi. Ba P3 thuộc B/C vẫn chặn theo ngưỡng chủ kho; không chuyển chúng thành nợ ngoài phạm vi. Chưa tìm thấy lỗi runtime sản phẩm HEAD trong tập thử hữu hạn.

Quy ước lệnh dưới đây: `ROOT` là checkout được giao; `D=$ROOT/.claude/dev`; `OUT=/tmp/review650-r5-output`. Lệnh chạy từ `ROOT`. Driver [run_logged.py](run_logged.py) ghi command argv, rc thật, thời gian, stdout/stderr riêng; rc driver 0 không thay rc tiến trình con. Các file `*.json` cùng nhãn log chứa command thực tế.

## Đối chiếu — lớp A

Nguồn lượt 4: `a004a23628a13bc1add0ae40b0318063406e3bad`. Diff sản phẩm đã đọc: `git diff a004a23..HEAD -- .claude/dev`, chỉ đổi test. Bốn đầu vào `new_mechanisms.py`, `multi_empty.py`, `purity_failure.py`, `adaptations.patch` ở `/tmp/review650-r5-input` khớp nguyên byte với bản `luot4-*` trong kho.

| Finding | Trạng thái | Bằng chứng tự chạy trên HEAD |
|---|---|---|
| F30 — thông báo K4 stale | **va_ho** — phản chứng cũ đóng, oracle mới chặn cả cách diễn đạt hợp lệ (F35) | Chạy nguyên phép `debt_stale_message` từ `luot3-supplement.py`: suite mutant rc **1**, **150/155 ca**, **159/170 mutant**, unresolved 11; đúng 5 ca K4 đỏ vì thông báo “fresh”. M5e/M5f: baseline và gác dương pass, đích đỏ đúng nghĩa/trường, `witness_killed`. |
| F31 — tuple bị cắt/rỗng | **da_va_that** trong phạm vi cơ chế tuple | M1s7 2/2 hợp lệ ⇒ `witness_killed`; 3/3 có neo vắng ⇒ `unresolved`; 3/2, 2/3, 0/0 ⇒ `unresolved: dot bien khai sai dang`. Suite với hàng 3/2 ⇒ rc **1**, **160/161 mutant**, unresolved 1. Các kiểu tuple/string, string/tuple, list, phần tử None/int đều bị bác. |
| F32 — tiến trình purity lỗi nhận tín dụng | **va_ho** — lỗi tiến trình cũ đóng, kiểm telemetry còn thiếu (F36) | Child thật rc 7 hoặc rc 1 sau JSON xanh ⇒ `LoiDo`. Mutant ném `RuntimeError` trước JSON: baseline/gác pass, target `LoiDo`, disposition `unresolved`. Telemetry đúng khóa nhưng sai kiểu còn bị nhận hoặc tính giết (F36). |

Lệnh đã chạy, mỗi driver rc **0**:

```text
python3 -B "$OUT/new_mechanisms.py" "$ROOT"
python3 -B "$OUT/multi_empty.py" "$ROOT"
python3 -B "$OUT/purity_failure.py" "$ROOT"
python3 -B "$OUT/f30.py" "$ROOT"
```

Log: [A-new.stdout](A-new.stdout), [A-empty.stdout](A-empty.stdout), [A-purity.stdout](A-purity.stdout), [A-f30.stdout](A-f30.stdout). `audit.py` lấy từ `luot3-audit.py`, chỉ chuyển marker về scratch lượt 5 ([diff](audit-adaptation.patch)); `f30.py` gọi riêng phép F30, không chạy các hướng săn khác của `extra()`.

## Lớp B — bốn bản Python

```text
python3.10 -B "$D/doc_receipt_thu_hoi_test.py"
python3.11 -B "$D/doc_receipt_thu_hoi_test.py"
python3.12 -B "$D/doc_receipt_thu_hoi_test.py"
python3.13 -B "$D/doc_receipt_thu_hoi_test.py"
```

| Python đo được | Suite rc; ca; mutant | M2k | 100.000 tầng, median / max trong 20 lần |
|---|---|---|---|
| 3.10.20 | **0; 155/155; 161/161** | `witness_killed` | **0,068 / 0,225 ms** |
| 3.11.15 | **0; 155/155; 161/161** | `witness_killed` | **0,065 / 0,226 ms** |
| 3.12.3 | **0; 155/155; 161/161** | `witness_killed` | **0,345 / 0,499 ms** |
| 3.13.12 | **0; 155/155; 161/161** | `witness_killed` | **0,509 / 8,566 ms** |

Mỗi suite: `witness_killed 161 · equivalent_verified 9 · unresolved 0`. Thời gian suite 11,27–13,27 giây trong các process chạy đồng thời, không dùng số này làm benchmark độc lập.

`python3.<v> -B "$OUT/versions.py" "$ROOT"` chạy trên cả bốn, rc 0. 100.000 tầng luôn ném `RecursionError`; không mã thoát âm, segfault hoặc timeout. 1.000/5.000 tầng: 3.10/3.11 ném, 3.12/3.13 parse được; 10.000 tầng đều ném. M2k chết đúng `long_sau: NEM:RecursionError@58#0`. Bảy hàng ngoại lệ M2b3/M2c3/M2d/M2e'/M6d/M2j/M2k đều chết đúng loại + dòng + giai đoạn trên bốn bản. Không thấy phụ thuộc cách viết thông báo ngoại lệ hay số dòng traceback trong tập này.

Đây là phép đo Linux x86_64, `recursionlimit=1000`, mặc định `int_max_str_digits=4300`; **không phải phép đo đúng CPython 3.12.14 của CI**. Log `B-suite-*.stdout`, `B-probe-*.stdout` giữ kết quả từng bản.

### F34 — P3 — `phu-thuoc-cau-hinh-python`: giới hạn số của oracle và child không đồng bộ

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:96`, `:125`, `:153`, `:163`.

`sys.get_int_max_str_digits() or 4300` biến giá trị hợp lệ **0 = không giới hạn** thành giới hạn giả 4300. Oracle vẫn đòi 4301 chữ số bị bác, trong khi HEAD đúng là chấp nhận. Với `-X int_max_str_digits=640`, parent dựng ca 641 chữ số nhưng child CLI chỉ nhận `sys.executable -B`; không thừa kế `-X`, nên dùng 4300 và trả rc 0 đúng theo cấu hình của nó.

**Đã chạy:**

```text
env PYTHONINTMAXSTRDIGITS=0 python3.10 -B .claude/dev/doc_receipt_thu_hoi_test.py
env PYTHONINTMAXSTRDIGITS=0 python3.11 -B .claude/dev/doc_receipt_thu_hoi_test.py
env PYTHONINTMAXSTRDIGITS=0 python3.12 -B .claude/dev/doc_receipt_thu_hoi_test.py
env PYTHONINTMAXSTRDIGITS=0 python3.13 -B .claude/dev/doc_receipt_thu_hoi_test.py
# cả bốn rc=1: 153/155 ca, 161/170 mutant, equivalent_verified 0, unresolved 9

python3.12 -X int_max_str_digits=640 -B .claude/dev/doc_receipt_thu_hoi_test.py
# rc=1: 154/155 ca, 161/170 mutant
# HONG cli:k1_so_dai: rc=0 ... "ok": true

env PYTHONINTMAXSTRDIGITS=0 python3.12 -B "$OUT/focused_controls.py" "$ROOT" limit
# driver rc=0: actual_limit=0; suite_limit=4300
# baseline và mutant đều TinHieuChotCa ở so_dai_vuot
# M2j vẫn nhận ["witness_killed", "giet"]
```

Ảnh hưởng là gate đỏ giả và số đo mutant sai trong cấu hình được Python hỗ trợ; chưa phải lỗi consumer JSON. P3 vì cấu hình mặc định/CI đã đo vẫn xanh. Log: `B-unlimited-*.stdout`, [B-limit640.stdout](B-limit640.stdout), [B-limit-credit.stdout](B-limit-credit.stdout).

**Đề xuất:** cô lập và ghim giới hạn hữu hạn riêng cho phép đo ValueError, đồng bộ parent/child trước khi dựng fixture; hoặc giữ 0 đúng nghĩa và tách phép đo giới hạn sang child có giới hạn được chỉ định. Không bỏ mutant M2j hay đổi runtime sản phẩm để chiều oracle. Khóa bằng cấu hình 0, mặc định và `-X ...=640`; kiểm baseline đích pass trước khi ghi giết. Control ngoài checkout ghim 4300 cho cả parent và environment child đã chạy từ cả hai cấu hình lỗi, đều **rc 0; 155/155; 161/161** ([driver](pinned_limit_control.py), `B-pinned-from-*.stdout`). Khi vá cần giữ nguyên cấu hình bên ngoài test và tránh chỉ sửa số đếm/oracle mà để child dùng cấu hình khác.

## Lớp C — cơ chế vừa thêm

`python3 -B "$OUT/mechanisms.py" "$ROOT"` rc **0**. Năm ca sẵn có đi qua oracle K4: `k4_base`, `k4_head`, `a11_k3_k4`, `kieu_S`, `kieu_H`; baseline đều pass. Ca thêm: S/H cùng lệch; S list; H dict; S null/H bool; caller và receipt cùng đổi S/H — đều đúng kỳ vọng. Mutant chỉ nói “fresh” khi K2 đỏ bị `kieu_S`/`kieu_H` bắt. Không thấy đường S/H sai kiểu né oracle. CLI dùng so toàn kết quả với API; không tự kiểm nghĩa K4 bằng helper mới, nhưng các ca API tương ứng có đo nghĩa. Không tìm được bỏ lọt trong các đường này.

### F35 — P3 — `oracle-k4-ghim-cau-chu`: báo “sai nghĩa” với thông báo vẫn đúng M5

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:89–92`.

Spec M5 đòi thông báo receipt stale/chạy lại; không đóng băng nguyên văn ASCII hoặc thứ tự S trước H. So danh sách nguyên văn tại d.91 biến chi tiết triển khai thành yêu cầu mới.

**Đã chạy:**

```text
python3 -B "$OUT/focused_controls.py" "$ROOT" wording  # rc=0
baseline:    K4=do, ok=false, ["K4: S stale, chay lai"]
alternative: K4=do, ok=false, ["K4: S receipt stale, chay lai"]
gác dương: pass
oracle: TinHieuChotCa: k4_base: ly do K4 sai nghia:
        ['K4: S receipt stale, chay lai']
```

Bản sao chỉ thêm từ `receipt`, không đổi field, độ tươi, vector luật hay ý nghĩa chạy lại. Một control khác đảo thứ tự hai lý do vẫn bị bác khi cả S/H lệch; năm ca hiện có chỉ lệch một trường nên không bộc lộ việc ghim thứ tự này. Log: [C-wording.stdout](C-wording.stdout), [C-mechanisms.stdout](C-mechanisms.stdout).

**Đề xuất:** kiểm độc lập tập trường lệch và nghĩa stale/chạy lại theo hợp đồng, với đối chứng cách diễn đạt hợp lệ; chỉ ghim toàn văn/thứ tự nếu chủ kho thật sự đưa chúng thành hợp đồng. Vẫn phải bác “fresh”, sai trường, thiếu/thừa lý do; không chữa bằng chỉ kiểm có substring `stale`. Khóa cặp `S stale, chay lai` / `S receipt stale, chay lai`, ca cả hai trường và các mutant M5e/M5f. Rủi ro của oracle quá lỏng là cấp lại tín dụng cho thông báo ngược nghĩa; cần giữ các đối chứng âm hiện có. Đây là lỗi bảo trì/độ đúng oracle, chưa làm HEAD bác receipt hợp lệ.

### F36 — P3 — `tin-dung-gia`: `LoiDo` chưa phân loại telemetry đúng khóa nhưng sai kiểu

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:243–246`, consumer `:478–490`.

Bản vá kiểm rc, kiểu dict và tập khóa nhưng chưa kiểm kiểu giá trị. `ev=null` được xem là bằng chứng tác dụng phụ, trong khi chưa có danh sách sự kiện hợp lệ. `trang_thai=1, tat_dinh=1` được nhận là xanh do `1 == True`.

**Đã chạy bằng child thật, không giả `CompletedProcess`:**

```text
python3 -B "$OUT/mechanisms.py" "$ROOT"       # rc=0
python3 -B "$OUT/schema_control.py" "$ROOT"   # rc=0
child rc=0; ev=null, trang_thai=true, tat_dinh=true
  -> TinHieuChotCa: tinh: kiem_json co tac dung phu
  -> mutant CHỈ thêm comment vô hại: witness_killed
child rc=0; ev=[], trang_thai=1, tat_dinh=1
  -> pass
JSON thiếu khóa / không phải dict / không parse được
  -> LoiDo, unresolved (đúng)
```

Điều kiện tái hiện được nói rõ: reviewer làm hỏng payload probe bằng hậu tố in JSON, trên bản test nạp ngoài checkout. Probe HEAD bình thường không phát kiểu sai này; **không** coi đây là crash hay đường tấn công receipt của runtime. P3 vì là lỗ trong kiểm tính hợp lệ của phép đo nội bộ; các lỗi tiến trình F32 cũ đã đóng.

**Đề xuất:** trước so kết quả, đòi `ev` là `list[str]`, hai cờ là `bool` thật; sai schema ⇒ `LoiDo`/`unresolved`; telemetry hợp lệ có cờ false/sự kiện thật vẫn là `TinHieuChotCa`. Control test-only ngoài checkout thêm kiểm kiểu đã đổi cả hai payload sai thành `LoiDo/unresolved`, giữ baseline xanh và **M1s6–M1s9 đều witness_killed** ([C-schema-control.stdout](C-schema-control.stdout)). Khóa thêm ev chứa phần tử không phải str. Tránh bắt mọi bất thường thành `LoiDo`, vì sẽ làm mất tín hiệu giết của tác dụng phụ thật.

Control này là bằng chứng đề xuất trên bản sao test, **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**; không phải bản vá đã áp vào branch.

## Lớp D — runtime thật trên HEAD

Không tìm thấy ngoại lệ API, CLI rc ngoài `{0,12,2}`, segfault hay treo trong các phép sau, trên cả bốn Python:

- `python3.<v> -B "$OUT/runtime_isolated.py" "$ROOT"`: **592 API/bản**, `errors: []`; **16 mẫu API+CLI/bản**, rc 0/12, toàn bộ JSON CLI bằng API. Gồm 38 trường ×14 giá trị, 60 độ sâu nhóm C, bytes/JSON hỏng, số lớn, surrogate, lồng sâu.
- `python3.<v> -B "$OUT/runtime_depth.py" "$ROOT"`: nhóm C ở **900, 990, 1000, 1200, 2000, 5000** tầng; sáu API+CLI/bản đều xử lý được, CLI 12. 3.12/3.13 parse được nhóm C sâu rồi trả K2 đỏ; không suy rằng K1 phải đỏ giống 3.10/3.11.
- `python3.<v> -B "$OUT/focused_controls.py" "$ROOT" receipt`: receipt thật khớp fixture, API `ok:true`, đủ năm luật `qua`, CLI **rc 0** trên cả bốn. Ca lỗi tham số/tệp vắng **rc 2** do suite CLI đo.

Các driver đều rc 0; log `D-runtime-*.stdout`, `D-depth-*.stdout`, `D-receipt-*.stdout`. Đợt runtime đầu dùng chung tên fixture scratch giữa các phiên bản có va chạm; đã **loại khỏi evidence**, giữ dưới tên `setup-invalid-D-runtime-*`, rồi chạy lại với thư mục riêng từng phiên bản. Kết quả ở trên chỉ lấy từ lượt đã cô lập và đối chiếu API/CLI.

## Nợ ngoài phạm vi

### F37 — P3 — `no-ngoai-danh-muc`: patch lưu bằng chứng làm `diff --check` đỏ

**Tệp:dòng:** `ops/reviews/land-doc-receipt-thu-hoi-c1a1a/luot4-adaptations.patch:18`.

```text
git diff --check origin/master..HEAD  # rc=2
ops/reviews/land-doc-receipt-thu-hoi-c1a1a/luot4-adaptations.patch:18: trailing whitespace.
+ 

git diff --check origin/master..HEAD -- .claude/dev  # rc=0
```

Đây là dòng context trống của unified diff được lưu làm hiện vật. Lượt 4 tại a004a23 chưa chứa hiện vật này nên kết quả sạch của lượt 4 không phải bằng chứng cho HEAD hiện tại. Không coi là lỗi runtime hoặc tự sửa ngoài write set.

**Owner:** chủ kho/điều phối hiện vật review. **Đề xuất:** bảo toàn bytes/băm bằng chứng gốc; chọn cách lưu/biểu diễn hiện vật không xung đột gate whitespace, hoặc quyết định ngoại lệ phạm vi có căn cứ. Không strip space mù trong patch vì có thể phá cú pháp/băm hiện vật. Khóa bằng đọc lại hash/khả năng dùng patch và chạy đúng `git diff --check` toàn diff. Nợ này ngoài A–D; ba P3 F34–F36 ở trong phạm vi vẫn cần xử lý theo ngưỡng được giao. Không mở cuộc săn mutant chiều khác.

## Đã chạy

| Lệnh/phạm vi | Rc và bằng chứng | Trạng thái |
|---|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master`; SHA256 spec/receipt | 0; khớp khối đầu và cuối | passed |
| Suite `doc_receipt_thu_hoi_test.py`, 4 Python mặc định | Mỗi bản 0; **155/155; 161/161; equivalent 9; unresolved 0** | passed |
| `versions.py`, 4 Python | Mỗi bản 0; M2k + 6 hàng ngoại lệ khác chết đúng; 20 lần/độ sâu/bản | passed trong môi trường đo |
| Suite với `PYTHONINTMAXSTRDIGITS=0`, 4 bản; `-X ...=640`, 3.12 | Mỗi lệnh 1; số đo ở F34 | failed |
| Control ghim giới hạn, 2 cấu hình trên 3.12 | Mỗi lệnh 0; **155/155; 161/161** | passed, bản đo ngoài checkout |
| `new_mechanisms.py`, `multi_empty.py`, `purity_failure.py`, `f30.py` | Driver mỗi lệnh 0; rc mutant và tín hiệu ở lớp A | đã đo |
| `mechanisms.py`, `focused_controls.py ... wording`, `schema_control.py` | Driver mỗi lệnh 0; phản chứng F35/F36 ở lớp C | audit failed |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | 0; **22/22 đăng ký; 4/4 launcher contract; 3/3 Ruff contract; 938/938 phản chứng; TỔNG ĐẠT** | passed |
| `python3 -B "$OUT/supplement.py" "$ROOT" registry` | Driver 0; `chay_moi` suite thật rc 0; nhận dòng dương, bác 6 dòng lệch/zero, bắt mất đăng ký | passed |
| `python3 -m ruff --version` | 0; **0.16.9** | measured |
| `python3 -m ruff check --no-cache --select F` ba tệp write set | 0; `All checks passed!` | bare lint passed |
| Ruff F bytes registry `origin/master` qua `--stdin-filename` | 0; không diagnostic; hai tệp mới không có ở base | delta F = 0 |
| `python3 -B "$OUT/supplement.py" "$ROOT" ruff` | Driver 0; `scripts/tl.py` HEAD/base đều **rc 1**, cùng 12 F821, diagnostics bằng nhau | bare lint failed ở nền; delta passed |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; **10 tệp, 0 chỗ chép doctrine** | passed |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0; **50 ADR/50 dòng**, ngoại lệ ADR-0016 có sẵn | passed |
| `git diff --numstat origin/master..HEAD` | 0; **25 đường, +3577/−0** toàn diff; sản phẩm đúng 3 đường, **+630/−0 = 1+114+515**, dưới 650 | passed trong scope sản phẩm |
| `git diff --check origin/master..HEAD` | **2**, đúng một vị trí F37 | failed |
| Cùng lệnh giới hạn `.claude/dev` | 0; không lỗi | passed trong scope dev |
| Runtime/API/CLI + receipt thật, 4 Python | Driver 0; chi tiết lớp D | passed trong tập thử |
| Snapshot tracked/untracked/ignored, diff/index, HEAD/tree | **2309/2309 tệp cùng băm**, diff/index rỗng; chỉ `.codex/` ignored đã có từ đầu | passed |

Môi trường của `run_logged.py`: `PYTHONDONTWRITEBYTECODE=1`; signer test tắt bằng **`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`**, không sửa Git config checkout. Registry test tự dựng lịch sử trong repo tạm; reviewer không tạo commit trong checkout, không push/mạng. Ruff pin/probe contract và bare lint là hai phép riêng; **không** tuyên bố lint đã chạy bằng đúng pin CI.

**not_run:** CI remote, full CI, Windows, CPython **3.12.14**, toàn registry `--chay`, revalidate lease/generation/PR live qua GitHub, merge/land/deploy/LIVE. Đã chạy riêng consumer `chay_moi` cho suite này. **skipped:** không dùng check skipped làm bằng chứng pass.

## Phạm vi assurance và lịch sử lớp

- Scratch do reviewer ghi ở `/tmp/review650-r5-output`; checkout detached, `core.abbrev=7`, origin là mirror được giao `/home/user/tra-luat`. Không kiểm remote qua mạng hoặc snapshot repo nguồn Executor. Lease `c1a1a-exec-2-claude-20260927`, generation/state live và quyền thêm lượt 5 nhận theo assignment; không tự khai đã revalidate trên GitHub.
- Reviewer mới độc lập với Executor theo vai được giao; không có reviewer Claude, không dùng subagent. `codex --version` rc 0, **0.157.1**, kèm cảnh báo không tạo được PATH alias vì read-only; không bypass. System công bố họ GPT-6; không có header launcher của chính run để độc lập đo model-version/effort/session, nên giữ **advisory_review**.
- Sandbox thực tế `workspace-write`; reviewer giữ checkout read-only bằng thao tác và cache ngoài cây. Snapshot chỉ chứng minh bytes ở hai mốc không đổi, không chứng minh mọi lịch sử thao tác. Không sửa authority/state hoặc tự tạo approval.

| Slug | Kết quả lượt 5 / phần còn mở | Phép kiểm đóng |
|---|---|---|
| `tin-dung-gia` | F31 đóng; lỗi tiến trình F32 đóng, telemetry F36 **P3** còn mở | Schema sai ⇒ `LoiDo/unresolved`; telemetry hợp lệ và M1s6–9 giữ kết quả đúng |
| `phu-thuoc-cau-hinh-python` | F34 **P3**, mới trong scope B | Baseline/M2j/CLI đúng dưới 0, 4300, `-X 640`, parent/child đồng bộ |
| `oracle-k4-ghim-cau-chu` | F35 **P3**, do cơ chế vá F30; phản chứng nghĩa sai của F30 đã đóng | Cặp diễn đạt hợp lệ qua; fresh/sai trường/thiếu-thừa vẫn bị bắt |
| `no-ngoai-danh-muc` | Nghĩa stale F30 được mở vào scope C theo chỉ thị mới; F37 **P3** là nợ hiện vật mới, không đồng nhất nguyên nhân với F30 | Chủ kho xử lý hiện vật/gate trong scope riêng, giữ provenance |

Bốn finding mới F34–F37 thuộc bốn lớp trên; không đếm thêm F30/F32 thành finding mở riêng. Các biểu hiện P2 cụ thể của lượt 4 không còn tái hiện. Phần còn lại được đánh P3 theo tác động/điều kiện tái hiện đã khai, **không** vì thiếu ngân sách hoặc muốn ghi nợ cho xong. Chưa đạt ngưỡng hết P1/P2/P3. Lượt 5 kết thúc với `changes_requested`; không tự cấp lượt 6 hoặc quyền ghi/land.
