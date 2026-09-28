**0 P1 / 0 P2 / 3 P3**

verdict: changes_requested

```yaml
packet: LAND-DOC-RECEIPT-THU-HOI-C1a1a
issue: 650
review_round: 6
reviewed_sha: a212059c5a2ea7379e08c3081f777583dcaa5f62
reviewed_tree: 736e65f6e96de218d3fafcdbcfa1fa0d32fac52a
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
previous_reviewed_sha: de927ca4a6e6b516edd68a5df43678a1832aba13
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

Các OID đo bằng `git rev-parse HEAD 'HEAD^{tree}' origin/master`, khớp đầu–cuối. Băm spec trong blob `HEAD:ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md` và bản trên đĩa bằng nhau; receipt cũng khớp assignment. Parent duy nhất của HEAD là `de927ca4a6e6b516edd68a5df43678a1832aba13`: đúng một commit vá. Xem [facts.json](facts.json), [snapshot-before.json](snapshot-before.json), [snapshot-after.json](snapshot-after.json).

Authority lượt 6 và trần sản phẩm ≤650 nhận trực tiếp từ chủ kho trong assignment, dẫn [#650 comment 5862203801](https://github.com/ducthangho/tra-luat/issues/650#issuecomment-5862203801), ngày 28-09-2026. Không xác minh lại GitHub qua mạng. Không coi các trần lịch sử trong spec là lý do bác chỉ thị trực tiếp này. Phạm vi chỉ gồm F34–F37, cơ chế của bản vá `a212059`, ba driver runtime được giao và các gate bắt buộc. Không audit lại toàn bộ A0 hay mở săn mutant khác.

**Hai finding cũ đóng trọn trong phạm vi đo: F36 và F37. F34/F35 đóng phản chứng gốc nhưng còn vấn đề của chính cách vá.** Ba P3 dưới đây đều thuộc phạm vi được giao và vẫn chặn theo mục tiêu hết P1/P2/P3. Không thấy lỗi runtime HEAD trong tập thử. Không đếm lại F34/F35 thành finding mở ngoài F38/F39.

Quy ước: `ROOT` là checkout được giao; `OUT=/tmp/review650-r6-output`; lệnh chạy từ `ROOT`. [run_logged.py](run_logged.py) ghi argv, rc con, stdout/stderr và thời gian vào `*.json`, `*.stdout`, `*.stderr`. Driver này trả 0 sau khi ghi log, nên **rc trong JSON mới là rc lệnh được đo**. Mọi lệnh qua driver dùng `PYTHONDONTWRITEBYTECODE=1` và `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`.

## Đối chiếu lượt 5

Nguồn: `luot5-VERDICT.md`, `luot5-verdict-day-du.md` tại `de927ca`. Chín script đầu vào có bản `luot5-*` tương ứng trong checkout đều khớp byte. Các driver dùng trực tiếp HEAD; không chép code sửa vào checkout.

| Finding | Trạng thái | Bằng chứng tự chạy |
|---|---|---|
| F34 — `phu-thuoc-cau-hinh-python` | **va_ho** | Hai cấu hình từng lỗi nay suite rc 0, **156/156; 161/161**. `focused_controls.py ROOT limit` dưới cả env 0 và `-X 640`: actual/suite limit cùng 4300; baseline `pass`; M2j ném đúng `ValueError@58#0`, `witness_killed`. Tuy nhiên việc ghim ở mức module làm đổi cấu hình của tiến trình nạp và con ngoài test, F38. |
| F35 — `oracle-k4-ghim-cau-chu` | **va_ho** | Phép cũ `focused_controls.py ROOT wording` nay `guard=pass, oracle=pass`; thêm `receipt`, dấu tiếng Việt và đảo thứ tự S/H đều qua. Bản sao trả `K4: S: receipt stale, chạy lại` vẫn bị gọi là sai nghĩa; control `stale_english` có sẵn trong `mechanisms.py` lượt 5 cũng còn đỏ (F39). Cơ chế lọc cùng dòng bỏ lọt lý do K4 mâu thuẫn khác khoảng trắng (F40). |
| F36 — `tin-dung-gia` | **da_va_that** | Đo đúng phép schema cũ trực tiếp trên HEAD, thay việc áp patch có neo stale: `ev=null`, `ev=[1]`, hai cờ bằng 1 → **LoiDo / unresolved**; telemetry xanh → `pass`, comment vô hại → `unresolved/song`. Telemetry có sự kiện hoặc cờ bool false → **TinHieuChotCa / witness_killed**. M1s6–M1s9 thật đều `witness_killed`. |
| F37 — `no-ngoai-danh-muc` | **da_va_that** | `git diff --check origin/master..HEAD` **rc 0**; `git check-attr` xác nhận ngoại lệ chỉ cho patch/verdict trong thư mục packet. Hash patch lượt 4 và các payload hiện có khớp manifest; không đổi bytes hiện vật cũ. Chi tiết bên dưới. |

Các phép cũ đã chạy: [limit.stdout](limit.stdout), [limit-x640.stdout](limit-x640.stdout), [wording.stdout](wording.stdout), [mechanisms.stdout](mechanisms.stdout), [schema.stdout](schema.stdout). [mechanisms_scoped.py](mechanisms_scoped.py) giữ nguyên các phần K4 và telemetry của lượt 5, chỉ **bỏ khối F31 ngoài phạm vi**; diff tại [mechanisms-scoping.patch](mechanisms-scoping.patch). [schema_head.py](schema_head.py) dùng cùng payload/benign-comment/disposition của `schema_control.py`, đo trực tiếp trên HEAD, thêm đối chứng `ev=[1]`, hai cờ false và M1s6–9; không áp lại bản vá F36 vào test đã vá.

## F38 — P3 — `phu-thuoc-cau-hinh-python`: import test đổi cấu hình toàn tiến trình và child không thuộc test

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:100`, `:101`.

`sys.set_int_max_str_digits` và phép gán `os.environ` chạy ngay khi import, không có phạm vi hoặc hoàn nguyên. Chỉ đọc/nạp module test, chưa gọi `main`, đã làm cấu hình do tiến trình chủ đặt biến mất. Từ env 0, một phép `json.loads` 4.500 chữ số của caller đang hợp lệ trở thành `ValueError`; các child caller tạo sau import cũng bị chuyển từ 0 sang 4300. Từ `-X 640`, import lại nới giới hạn cha lên 4300. Đây là tác dụng phụ của bản vá, không phải lỗi `kiem_json`.

**Lệnh đã chạy (mỗi driver/tiến trình đo rc 0):**

```text
env PYTHONINTMAXSTRDIGITS=0 python3.12 -B "$OUT/import_effect.py" "$ROOT"
python3.12 -X int_max_str_digits=640 -B "$OUT/import_effect.py" "$ROOT"
```

Output rút từ [import-zero.stdout](import-zero.stdout):

```json
{"before":{"limit":0,"env":"0","parse":"parsed_4500","child":{"child_limit":0},"child_rc":0},"after_import":{"limit":4300,"env":"4300","parse":"ValueError","child":{"child_limit":4300},"child_rc":0},"called_main":false}
```

[import-x640.stdout](import-x640.stdout): parent `640 → 4300`; env `null → "4300"`, cũng chưa gọi main. Không quy việc `-X` không thừa kế cho bản vá: child trước import ở control này đã có mặc định 4300.

**Phần đã sửa đúng:** CLI/purity helpers hiện chạy child bằng cùng executable và `-B`, thừa kế env 4300. 17 phép probe tương ứng argv/env của hai helper đều ra 4300; bản thân `ca_cli`/`ca_tinh` pass. Cả chín mutant tương đương và các mutant còn lại qua ở hai cấu hình khởi động. Không tìm thấy child sẵn có nào còn dùng cấu hình 0/640 sau khi suite ghim. Vấn đề là ảnh hưởng ra ngoài phạm vi phép đo, không phải đồng bộ còn thất bại.

**Đề xuất:** bỏ thay đổi cấu hình lúc import. Cô lập chạy suite hoặc phép đo số dài trong child có giới hạn chỉ định; nếu chạy trong cùng process, dùng phạm vi `try/finally` khôi phục cả giá trị giới hạn lẫn trạng thái có/vắng của env, và truyền env riêng cho child test. Ca khóa: import từ 0 và 640 phải giữ cấu hình/khả năng parse của caller và child không thuộc test; suite vẫn **156/156; 161/161**, M2j baseline phải xanh trước khi nhận tín dụng. Rủi ro vá: hoàn nguyên quá sớm hoặc chỉ ghim parent sẽ mở lại F34; cần giữ phép đo parent/CLI/purity đồng bộ trong phạm vi test. P3 vì lỗi ghép test trong cùng process; đường CI chạy suite thành process riêng hiện vẫn xanh.

## F39 — P3 — `oracle-k4-ghim-cau-chu`: regex vẫn bác cùng thông báo chỉ đổi dấu phân cách

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:93`.

Bản vá thay một câu đóng băng bằng một nhóm nhỏ cách viết, nhưng vẫn đòi đúng một dấu cách sau S/H. Thêm `:` để tách tên trường khỏi **nguyên cụm M5** `receipt stale, chạy lại` không đổi nghĩa, luật hay trường lệch; oracle vẫn báo sai nghĩa. Spec M5 không quy định dấu phân cách này. Finding không yêu cầu oracle hiểu mọi diễn đạt tự do.

**Lệnh đã chạy:**

```text
python3.12 -B "$OUT/k4_patch_check.py" "$ROOT"  # rc=0
python3.12 -B "$OUT/mechanisms_scoped.py" "$ROOT"  # rc=0; giữ control K4 lượt 5
```

Output của bản sao chỉ đổi câu thông báo:

```text
ly_do = ["K4: S: receipt stale, chạy lại", "K4: H: receipt stale, chạy lại"]
ok = false; K1/K2/K3/K5 = qua; K4 = do
duong_fixture: pass
k4_base: TinHieuChotCa: ... ly do K4 sai nghia: ['K4: S: receipt stale, chạy lại']
k4_ca_hai: TinHieuChotCa: ... ly do K4 sai nghia: [...S..., ...H...]
```

Control `K4: S: receipt stale, rerun` nguyên từ lượt 5 cũng bị bác; ví dụ tiếng Việt ở trên giữ nguyên cụm M5 nên không cần dựa vào tranh luận dịch nghĩa `rerun`. [k4-patch.stdout](k4-patch.stdout) ghi đủ sáu ca K4 và gác dương.

**Đề xuất:** tách nhận diện tên trường/dấu phân cách khỏi cụm báo stale/chạy lại; chuẩn hóa các dạng phân cách tương đương đã đo trước khi so nghĩa và đa tập trường. Nếu định đóng băng một định dạng duy nhất thì cần hợp đồng đầu ra rõ, không tự thêm ràng buộc vào M5 qua test. Khóa cặp không/có `:` sau trường, các cặp có/không `receipt`, có/không dấu và thứ tự S/H. Rủi ro: nới regex kiểu substring sẽ bỏ lọt phủ định hoặc phần đuôi ngược nghĩa; giữ đối chứng `fresh`, sai trường, trùng/thiếu/thừa và `stale..., fresh`. P3 về oracle, không phải runtime HEAD trả kết quả sai.

## F40 — P3 — `oracle-k4-bo-sot-ly-do`: lọc đúng khoảng trắng bỏ qua lý do mâu thuẫn

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:93` (`if x.startswith("K4: ")`).

Một lý do `K4:S fresh, khong can chay lai` bị bỏ khỏi tập kiểm vì thiếu khoảng trắng sau `:`. Khi có sẵn lý do đúng cho S, so `sorted` vẫn thành công: cùng kết quả chứa cả “stale, chạy lại” và “fresh, không cần chạy lại” mà oracle xanh. Dòng lọc này nằm trong cơ chế K4 được bản vá thay; không khẳng định lỗi xuất hiện lần đầu ở commit này (phép lọc hẹp đã có tại `de927ca`). Nó vẫn thuộc phép kiểm độ lỏng của oracle mà lượt 6 được giao.

**Lệnh đã chạy:**

```text
python3.12 -B "$OUT/k4_patch_check.py" "$ROOT"  # rc=0
python3.12 -B "$OUT/k4_survives.py" "$ROOT"     # driver rc=0; suite mutant rc=0
```

Mutant chỉ thêm lý do khi S lệch, không đổi vector luật hoặc mã thoát:

```text
ly_do = ["K4: S stale, chay lai", "K4: H stale, chay lai",
         "K4:S fresh, khong can chay lai"]
duong_fixture, k4_base, k4_head, k4_ca_hai, a11_k3_k4, kieu_S, kieu_H: pass
nghia vu: witness_killed 161 · equivalent_verified 9 · unresolved 0
doc_receipt_thu_hoi tests: 156/156 ca QUA · 161/161 dot bien GIET
```

Script và bản sao mutant nằm ngoài checkout: [k4_survives.py](k4_survives.py), [k4-survives.stdout](k4-survives.stdout), [k4_unspaced_contradiction.log](k4_unspaced_contradiction.log). Đây là bằng chứng suite còn nhận đầu ra mâu thuẫn, không phải bằng chứng HEAD đang phát thông báo ấy.

**Đề xuất:** thu nhận mọi lý do mang nhãn K4 trước khi kiểm định dạng/nghĩa; lý do K4 không parse được phải làm ca đỏ, không được biến mất qua bộ lọc. Giữ phân biệt K1 đỏ và các lý do thuộc K2/K3/K5. Ca khóa: một lý do stale hợp lệ cộng dòng `K4:S fresh...` phải đỏ; cùng mutant với khoảng trắng vốn đã đỏ; ca cả hai trường và đa tập không trùng vẫn xanh. Rủi ro: nhận diện nhãn quá rộng có thể vơ cả lý do luật khác; cần ca phối hợp K3+K4. P3 vì lỗ test, chưa thấy sai runtime thật.

F39 và F40 là hai lỗi riêng: nới phân cách sau tên trường không làm dòng bị loại khỏi bộ lọc quay lại; sửa bộ lọc không làm câu có dấu `:` sau S/H được chấp nhận. Vì vậy giữ hai ID/phép kiểm đóng, không gộp để giảm số đếm.

## Kiểm lại đối chứng executor và ngoại lệ whitespace

Đã chạy nguyên nội dung `luot5-executor-va5_check.py` (bản ngoài checkout `executor_va5_check.py`): rc 0. Kết quả đúng với lời khai trong phạm vi script ấy: `receipt_word`, `co_dau`, `dao_thu_tu` đều pass kể cả `k4_ca_hai`; `fresh`, sai trường, lý do trùng và `stale_then_fresh` bị bắt tại ca liên quan. Script không bao phủ F38–F40 nên không dùng kết quả của nó để đóng các điểm này.

Đối chứng độc lập cho lỗi executor tự khai: trên **bản sao test**, chỉ bỏ `sorted` ở vế phải. `k4_base` và `k4_head` vẫn pass, riêng `k4_ca_hai` ném `TinHieuChotCa`; HEAD qua cả ba. Như vậy ca mới thật sự bắt được lỗi S/H so với H/S, không chỉ tăng N. `sorted` hai vế hiện giữ **đa tập**, nên phát hiện lý do trùng (tốt hơn đổi thẳng thành `set`).

F37: [artifacts-final.stdout](artifacts-final.stdout) ghi đầy đủ phép băm và `git check-attr`:

- `luot4-adaptations.patch` = `7bb765d45809fe826514133aaf8b803ab8d23c051693cb8e47498c7b73f830d5`, đúng manifest, không bị strip space.
- Cả **7/7 tệp `luot4-*`** trong checkout không đổi byte so `de927ca`.
- Manifest lượt 4: 4 tệp hiện vật có bản chép trực tiếp khớp băm. `VERDICT.md` được lưu thành `luot4-verdict-day-du.md` với một dòng HTML metadata có sẵn từ commit trước: hash cả tệp là `7c14b52c4ab8a4ddf2eef79be482c3461c01c27b49da7d625e79a7b144095937`; **phần thân sau đúng dòng metadata** khớp hash gốc `fb7a1305cc42e1dad49bcffb8fe5dc05177651d70273c974ebc3aac4679ff566`. Không gọi toàn tệp bọc là byte-identical.
- Manifest lượt 5: **11/11 payload có bản trong checkout** khớp băm, gồm bản đầy đủ `luot5-verdict-day-du.md` và patch/script đã lưu. Wrapper `luot5-VERDICT.md` là tệp vận chuyển khác, không thay payload `VERDICT.md` trong manifest.
- **109/114 mục lượt 4 và 206/217 mục lượt 5 không được lưu trong checkout** này; không tuyên bố đã xác minh toàn manifest. Sự vắng mặt đó không do `.gitattributes`, không mở finding mới ngoài scope.
- `-whitespace` chỉ tác động mẫu `*.patch`, `luot*-VERDICT.md`, `luot*-verdict-day-du.md` dưới thư mục packet (kể cả thư mục con/future file khớp mẫu). Script Python, JSON, manifest hash và đường cùng tên bên ngoài packet vẫn `whitespace: unspecified`. `text: auto`, `eol: lf` không đổi. Phạm vi rộng hơn một patch lỗi nhưng vẫn nằm trong loại hiện vật nguyên byte đã được giao, không nới sang mã sản phẩm; không thấy vượt phạm vi cần ghi finding.

## Runtime

Chỉ tái chạy ba driver được giao, trên HEAD thật bằng Python **3.10.20 / 3.11.15 / 3.12.3 / 3.13.12**:

```text
python3.<v> -B "$OUT/runtime_isolated.py" "$ROOT"
python3.<v> -B "$OUT/runtime_depth.py" "$ROOT"
python3.<v> -B "$OUT/focused_controls.py" "$ROOT" receipt
```

Mỗi driver rc **0**. Mỗi Python có **592 ca API**, `errors=[]`; thêm **16 mẫu API+CLI** và **6 độ sâu nhóm C (900/990/1000/1200/2000/5000)**: không ngoại lệ API, không CLI rc ngoài `{0,12,2}`, không timeout/crash; mọi JSON CLI bằng API. Receipt thật bằng fixture, API `ok:true`, năm luật `qua`, CLI rc **0** trên cả bốn. CLI lỗi tham số/tệp vắng rc **2** được suite đo riêng.

Các driver import module test nên hiện ghim **4300** trước phép đo (tác dụng F38 được khai rõ). Kết quả runtime không chứng minh hành vi ở mọi cấu hình giới hạn ngoài suite. Không chạy thêm fuzz/runtime khác. Suite có ca 100.000 tầng nhưng lượt này không chạy lại benchmark `versions.py`. Log `runtime-*.stdout`, `depth-*.stdout`, `receipt-*.stdout`; tổng đối chiếu tự động tại [runtime-summary.json](runtime-summary.json). Mỗi phiên bản dùng thư mục fixture riêng, không có va chạm tên giữa các phiên bản.

## Nợ ngoài phạm vi

**Không phát sinh nợ ngoài phạm vi mới.** F37 trước đây mang slug `no-ngoai-danh-muc`, nay được giao đích danh và đã đóng trong phạm vi hiện vật/whitespace. Ba P3 F38–F40 đều ở cơ chế được giao, không chuyển chúng sang nợ để bỏ qua. Không thử nội dung dựng đường dẫn thoát cây; không có hướng nào của lượt này cần phép đó.

## Đã chạy

| Lệnh/phạm vi (từ ROOT, qua `run_logged.py` khi có nhãn log) | Rc thật và bằng chứng | Trạng thái |
|---|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master`; đọc blob spec và SHA256 spec/receipt | 0; đúng khối định danh, đầu–cuối không đổi | passed |
| `git diff de927ca..a212059` | 0; chỉ sản phẩm test và hiện vật review; raw diff `patch.txt` | measured |
| `python3.10 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; **156/156 ca; 161/161 mutant; equivalent 9; unresolved 0** | passed |
| Cùng suite bằng `python3.11`, `python3.12`, `python3.13` | Mỗi lệnh 0; cùng số dương trên | passed |
| `env PYTHONINTMAXSTRDIGITS=0 python3.12 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; **156/156; 161/161** | passed |
| `python3.12 -X int_max_str_digits=640 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; **156/156; 161/161** | passed |
| `focused_controls.py ROOT limit` dưới env 0 và `-X 640` | Mỗi lệnh 0; baseline pass, M2j giết đúng | passed trong scope số dài |
| `focused_controls.py ROOT wording` | 0; biến thể thêm receipt pass | passed cho phản chứng cũ |
| `python3.12 -B "$OUT/mechanisms_scoped.py" ROOT` | 0; K4 baseline/đảo thứ tự pass, English còn bị bác; telemetry sai schema unresolved | measured; F39 |
| `python3.12 -B "$OUT/schema_head.py" ROOT` | 0; schema sai → LoiDo, telemetry hợp lệ giữ đúng tín hiệu; M1s6–9 chết | passed |
| `python3.12 -B "$OUT/executor_va5_check.py" ROOT` | 0; xác nhận các đối chứng executor, đầy đủ tại `executor-check.stdout` | passed trong phạm vi script |
| `import_effect.py ROOT` dưới env 0 và `-X 640` | Mỗi lệnh 0; thay cấu hình host/child chỉ vì import | audit failed: F38 |
| `python3.12 -B "$OUT/k4_patch_check.py" ROOT` | 0; câu đúng bị bác, câu sai lọt; phục hồi lỗi unsorted làm đỏ riêng ca hai trường | audit failed: F39/F40 |
| `python3.12 -B "$OUT/k4_survives.py" ROOT` | Driver 0; suite mutant **rc 0, 156/156; 161/161** dù chứa lý do mâu thuẫn | audit failed: F40 |
| `python3 -B .claude/dev/ci_dang_ky_test.py` (signer tắt bằng env nói trên) | 0; **22/22 đăng ký; 4/4 launcher contract; 3/3 Ruff contract; 938/938 phản chứng; TỔNG ĐẠT** | passed |
| `python3 -m ruff --version` | 0; **0.16.9** | measured |
| `python3 -m ruff check --no-cache --select F` ba tệp sản phẩm | 0; **All checks passed!** | bare lint passed |
| `python3 -B "$OUT/ruff_delta.py"` | Driver 0; Ruff F registry base/HEAD cùng 0; hai tệp mới 0. `scripts/tl.py` base/HEAD cùng **rc 1, 12 F821**, diagnostics giống nhau | bare lint tl.py failed sẵn; **delta F = 0 passed** |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; **10 tệp, 0 chỗ chép doctrine** | passed |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0; **50 ADR/50 dòng**, ngoại lệ 0016 có sẵn | passed |
| `git diff --numstat origin/master..HEAD` | 0; **40 đường, +4250/−0** toàn diff. Sản phẩm đúng ba đường **+1 +114 +522 = +637/−0 ≤650** | passed theo trần sản phẩm được giao |
| `git diff --check origin/master..HEAD` | 0; không diagnostic; thuộc tính và hash đã kiểm riêng | passed |
| `python3 -B "$OUT/artifact_check.py"` | 0; số/hash/giới hạn bản lưu ở mục F37 | passed trong scope hiện vật có sẵn |
| Ba driver runtime trên bốn Python | 12 lệnh rc 0; số dương ở mục Runtime | passed trong tập thử |
| `snapshot.py before/after`, so bytes tracked/untracked/ignored, diff/index, HEAD/tree | Mỗi lệnh 0; **2324/2324 tệp bằng băm**, diff/index rỗng; chỉ `.codex/` ignored có sẵn | passed |

`ruff_delta.py` lấy bytes base bằng `git show origin/master:<path>` rồi dùng `ruff check --no-cache --select F --output-format json --stdin-filename <path> -`; log giữ argv/rc/diagnostics. Hai `git show` cho tệp mới trả **128 vì chưa tồn tại ở base**, được khai là `absent_at_base`, không gọi là lint pass. Ruff pin/probe contract là phép riêng trong registry; không khai Ruff đang cài là đúng phiên bản pin CI.

**not_run:** CI remote, full CI, Windows, đúng CPython 3.12.14 của CI, toàn registry `--chay`, xác minh live PR/lease/generation/comment qua GitHub, các driver lượt 5 ngoài phạm vi (census/attacks/classifier/F31/benchmark), merge/land/deploy/LIVE. Không chạy `schema_control.py` nguyên bản vì neo cũ đã được thay; phép tương ứng đã chạy trực tiếp bằng `schema_head.py`, không tính setup hỏng là pass. **skipped:** không có check skipped nào được dùng làm bằng chứng pass.

## Giới hạn và lịch sử lớp

Checkout detached, `core.abbrev=7`, origin là mirror local `/home/user/tra-luat` được giao. Snapshot chỉ phủ checkout này, không phủ repository nguồn Executor. Sandbox thực tế `workspace-write`; checkout được giữ chỉ đọc bằng thao tác, cache/output/mutant ngoài cây. Snapshot bằng nhau chứng minh hai mốc không có delta, không chứng minh toàn lịch sử không từng ghi rồi hoàn nguyên. Không chỉnh Git config checkout, không commit/push/mạng. Registry test tự tạo lịch sử trong repository tạm theo lệnh test được giao.

Provider/surface/transport khai theo assignment và adapter `cross-review`; system cho biết họ GPT-6. Không có header launcher của chính run để độc lập đo model-version/effort/session ID, không suy từ lịch sử lượt 5 hay actor GitHub; giữ **advisory_review**, không tự tạo `cross_approved`. Không có reviewer Claude hay subagent. Lease/generation live không được đo lại trong lượt offline; hồ sơ trước ghi `c1a1a-exec-2-claude-20260927`, không dùng tên ấy để tự cấp quyền tiếp tục ngoài assignment lượt 6.

| Slug | Nguồn và trạng thái lượt 6 | Phép kiểm đóng còn lại |
|---|---|---|
| `phu-thuoc-cau-hinh-python` | F34 tại `de927ca`; phản chứng lệch parent/child đóng, F38 P3 do ghim toàn cục mới | Import không đổi host/child ngoài test; suite và M2j vẫn đúng dưới 0/640/4300 |
| `oracle-k4-ghim-cau-chu` | F35 tại `de927ca`; các biến thể cũ chính qua, F39 P3 còn phân biệt dấu phân cách không thuộc hợp đồng | Cặp cùng nghĩa không/có dấu `:` qua, âm ngược nghĩa vẫn đỏ |
| `oracle-k4-bo-sot-ly-do` | F40 P3 mới ghi nhận, ngay bộ lọc oracle được giao; không phải tuyên bố regression mới ở runtime | Mọi lý do mang nhãn K4 đều được kiểm, dòng mâu thuẫn không bị bỏ lọt |
| `tin-dung-gia` | F36 đóng trong miền schema telemetry; M1s6–9 giữ tín hiệu | Không còn biểu hiện mở từ F36 trong scope đã đo |
| `no-ngoai-danh-muc` | F37 đóng, không nợ mới | Giữ bytes/hash và ngoại lệ đúng thư mục/loại hiện vật |

Lượt này có **3 biểu hiện mở / 3 lớp mở**, đều P3, không có P1/P2 mới. Kết quả này chỉ là verdict lượt 6 trên exact SHA nêu trên; không tự cấp lượt 7 hay quyền sửa/land.
