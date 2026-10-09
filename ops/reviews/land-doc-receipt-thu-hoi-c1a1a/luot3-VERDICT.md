<!-- Verdict codex lượt 3/3 (gpt-6-astra, reasoning effort xhigh — header log runtime "reasoning effort: xhigh", session 01a0e58d-3b8d-7c31-bc01-4175032823dc), codex_cli tại chỗ, sandbox clone riêng, trên fb8ccff8 (tree aac6522), base ceb1a3f3, spec sha256 978058983e8e…. Lượt audit DANH MỤC theo quyết định chủ kho "Đóng danh mục + 1 lượt". Chép NGUYÊN VĂN; không sửa chữ nào. Đường /tmp/review650-r3/* là đường trong sandbox reviewer; bản sao script nằm cạnh tệp này. -->
**0 P1 / 5 P2 / 1 P3**

verdict: changes_requested

```yaml
reviewed_sha: fb8ccff8bcf88aad011016afff3936c2fb4877c7
reviewed_tree: aac6522a2418ce55c092947e078fc5a41ad6746a
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
spec_sha256: 978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
provider: openai_codex
execution_surface: codex_cli
transport: machine
assurance: advisory_review
round: 3/3
```

Các băm được đo đầu/cuối và không đổi. [Verdict đầy đủ](/tmp/review650-r3/VERDICT.md), [script audit](/tmp/review650-r3/audit.py), [probe classifier](/tmp/review650-r3/classifier_stage.py), [manifest bằng chứng](/tmp/review650-r3/ARTIFACTS.sha256).

Áp dụng đúng checkpoint **“Đóng danh mục + 1 lượt”**: F25–F29 thuộc các chiều đã khai hoặc disposition; F30 là nợ ngoài danh mục, **không chặn merge**. Không tìm thấy lỗi runtime mới trên HEAD trong tập đầu vào đã thử.

Suite xanh **153/153 ca · 152/152 đột biến**, nhưng audit chưa chấp nhận A0. Các phản chứng dưới đây chạy trên bản sao ngoài checkout; không khẳng định sản phẩm HEAD đang chứa hành vi của mutant.

## Đối chiếu lượt 2

Đã chạy nguyên script `luot2-probe_new.py` trong scratch với đủ năm mode `credit`, `mutants`, `td`, `oracle`, `followup`; mỗi driver rc 0. Rc tiến trình con được ghi riêng.

| Finding | Kết luận | Bằng chứng |
|---|---|---|
| F15 | `va_ho` | Ba control cũ bị từ chối. Nhưng dòng neo duy nhất chuyển sang chẩn đoán **sau K1 đỏ** vẫn được tính `witness_killed`; F25. |
| F16 | `va_ho` | M1o và đối chứng nullable đã đúng. Bốn hàng nhánh xanh miễn A1 bằng `None`, dù mỗi mutant làm đỏ toàn bộ 11 ca dương; F26. |
| F17 | `da_va_that` | `cli_ok_int` suite rc 1, lỗi đúng `cli:xanh` vì `ok:1`. |
| F18 | `da_va_that` | Đo riêng mutant nuốt từng luật, chỉ kích hoạt K2–K5 khi K1 qua: đúng các ca CLI tương ứng đều bắt được. |
| F19 | `da_va_that` | Ba mutant giờ cũ đều đỏ; kiểm riêng đủ 24 ô TOK và ca Unicode, mỗi ô có baseline xanh/mutant đích đỏ. |
| F20 | `va_ho` | Hai mutant cũ bị bắt; bốn biến thể process/sys/tệp/global module vẫn qua toàn suite; F29. |
| F21 | `da_va_that` | Chuẩn hoá chuỗi sau decode bị spy identity bắt; spy được phục hồi cả khi thành công và thất bại. |
| F22 | `da_va_that` | Đổi lý do `K1 do` thành `K1 qua` bị đúng ca `bom` bắt. |
| F23 | `da_va_that` | 4300 chữ số: CLI 0; 4301/4500: K1 đỏ, CLI 12. JSON lồng 1000 tầng thực sự gây `RecursionError`, HEAD chuyển thành K1 đỏ/CLI 12. |
| F24 | `da_va_that` | M2a tương đương ở cấp verdict; M2a2 bị oracle thứ tự giết; M2a′ ghép bị BOM giết. Phù hợp quyết định “Hai ID, hai cấp”. |

**7/10 đã vá thật; 3/10 vá hờ.**

## Danh mục

Đo được **130 hàng DB + 31 hàng `_theo_truong()` = 161 ID duy nhất**. [Census từng hàng](/tmp/review650-r3/census.jsonl) ghi baseline, ca đích, A1 và disposition. Fixture khớp đủ 38 khoá, giá trị và kiểu của receipt thật.

| Chiều | Kết quả audit |
|---|---|
| 1. Predicate từng trường | **Đủ 31 ô**; 27 witness, 4 TD hợp lý: schema và ba C bị chốt khác che. |
| 2. Hex40/hex64 | Alphabet, hoa, độ dài và fullmatch có răng. **Bắt buộc str của hex64 chưa phân biệt**; F28. |
| 3. Int | **Đủ** bool, float, chuỗi và null job_id; mutant bị đúng ca đích bắt. |
| 4. Regex giờ | **Đủ 24/24 ô TOK**, cộng Unicode; từng ô phân biệt. |
| 5. Nullable | **Đủ** các nhánh null/non-null đã khai. Đối chứng M3w/x/y thật sự xanh. |
| 6. Hình dạng API | **Thiếu hai ô K1 đỏ**; bốn ô xanh có miễn A1 không hợp lệ. F26/F27. |
| 7. CLI | **Đủ trong chiều khai**: rc, lỗi tham số, một dòng, parity/kiểu bool, từng luật đỏ. Đã tránh tín dụng do K1 lan khi đo K2–K5. |
| 8. K1/parser | **Đủ các ô khai**; witness hiện tại có lỗi đích đúng. Cơ chế chứng nhận ngoại lệ còn F25. |
| 9. Quan hệ C/K3/K4/K5 | **Đủ các ô quan hệ/giá trị khai**; mutant nhóm và từng vế phân biệt. Chín TD tổng cộng được kiểm lại, không thấy TD sai. |
| 10. Tính thuần | Có đủ tên nhóm nhưng **cả bốn nhóm runtime còn biến thể sống**; F29. |
| 11. M8 | Hai backreference có răng. Consumer nhận dòng dương, bác sáu dòng lệch/zero; bỏ đăng ký bị bắt. |
| 12. Phân hạng | Sai loại/dòng/neo trùng bị bác; **neo đúng chữ nhưng sai giai đoạn vẫn được nhận**. A1 còn miễn sai; F25/F26. |

Ma trận chiều 6:

| Trường | K1 đỏ | K2–K5 đỏ | Xanh |
|---|---|---|---|
| `ok` bool | **Thiếu ID** | M1o | M1o2 — A1 sai |
| `luat` dict | M1v | M1u | M1u2 — A1 sai |
| `ly_do` list | M1w | M1w2 | M1w3 — A1 sai |
| Tập ba khoá ngoài cùng | **Thiếu ID** | M1x | M1x2 — A1 sai |

## Findings

Các lệnh dưới chạy từ checkout được giao; `$ROOT` là checkout, `$OUT=/tmp/review650-r3`.

### F25 — P2 — `tin-dung-gia`

**Vị trí:** `.claude/dev/doc_receipt_thu_hoi_test.py:80`, `:435`.

Bộ phân hạng vẫn nhận ngoại lệ ở sai giai đoạn. Đã chạy:

```text
python3 -B "$OUT/classifier_stage.py" "$ROOT"
rc=0
baseline byte_0x80: pass
mutant duong_fixture: pass
anchor_lines: [76]
exception at 56: UnicodeDecodeError, luat={}
exception at 76: UnicodeDecodeError, luat={'K1':'do'}
disposition: witness_killed
```

Control giữ nguyên decode strict và catch, chỉ đổi cách viết thành đối số có tên. Sau khi K1 đã ghi đỏ, thêm một decode chẩn đoán bằng **đúng dòng neo nguyên văn**, duy nhất trong mutant. Classifier tính ngoại lệ chẩn đoán thành bằng chứng cho M2b3.

**Đề xuất:** giữ kiểm loại/dòng nhưng neo thêm vùng thực thi hoặc giai đoạn dự kiến từ nguồn; ngoại lệ decode/parser được tính phải xảy ra trước khi K1 đã ghi. Khoá control này cùng wrong-type/wrong-line/duplicate-line. Tránh hard-code số dòng tuyệt đối hoặc quay lại dò substring.

### F26 — P2 — `tin-dung-gia`

**Vị trí:** `.claude/dev/doc_receipt_thu_hoi_test.py:345`, `:347`, `:351`, `:353`, `:425`.

Bốn hàng nhánh xanh tự miễn A1. Đã chạy:

```text
python3 -B "$OUT/audit.py" "$ROOT" classifier
rc=0
M1o2/M1u2/M1w3/M1x2:
  positive_count=11
  positive_pass=0
  disposition=witness_killed
```

Quyết định nullable được thực hiện đúng; nó không cấp miễn A1 cho bốn hàng mới. Việc miễn cũng không bắt buộc về kỹ thuật: `classifier_stage.py` đo **4/4 biến thể** làm sai hình dạng trên `duong_c_khac_s`, giữ `duong_fixture` xanh, vẫn giết đúng mutant.

Probe phụ: tên gác không tồn tại `not_a_case`, hoặc ca âm `bom`, vẫn được classifier nhận.

**Đề xuất:** dùng mutant có đối chứng dương thật hoặc giữ unresolved đến khi có quyết định riêng. Kiểm tên ca gác tồn tại, là ca dương và khác đích. Không bỏ kiểm kiểu nhánh xanh hay thay gác bằng ca âm.

### F27 — P2 — `dot-bien-tuong-duong-hoac-thieu`

**Vị trí:** `.claude/dev/doc_receipt_thu_hoi_test.py:343`.

Thiếu hai ô trong chính ma trận đã khai: **`ok` bool khi K1 đỏ** và **tập khoá ngoài cùng khi K1 đỏ**.

Đã chạy:

```text
python3 -B "$OUT/audit.py" "$ROOT" attacks
rc=0
shape_k1_ok:   baseline bom=pass; mutant bom=TinHieuChotCa, ok=0
shape_k1_keys: baseline bom=pass; mutant bom=TinHieuChotCa, extra=1
```

Oracle hiện có bắt được, nhưng cả 161 ID không có hai ô này. Đây là finding **thiếu ô**, không phải lời khai mutant sống.

**Đề xuất:** thêm hai ID/mutant trên `_TRA1`, đích `bom`, gác `duong_fixture`. Kiểm đủ ma trận 4×3; không lấy mutant thiếu trạng thái trong `luat` thay cho khoá ngoài cùng.

### F28 — P2 — `dot-bien-tuong-duong-hoac-thieu`

**Vị trí:** `.claude/dev/doc_receipt_thu_hoi_test.py:126`, `:311`.

M3u chỉ thử số 40 chữ số ở `T`; không phân biệt việc hex64 ép số thành str.

Đã chạy qua `audit.py attacks`:

```text
python3 -B /tmp/review650-r3/hex64_number_coerce/.claude/dev/doc_receipt_thu_hoi_test.py
rc=0
153/153 ca QUA · 152/152 dot bien GIET
unresolved 0

workflow_definition_sha256 = int('1' * 64):
HEAD: K2=do
mutant: ok=true
```

Mutant chỉ thêm vào `_khop`:

```python
if mau == "[0-9a-f]{64}":
    return lambda v: re.fullmatch(mau, str(v)) is not None
```

Mọi mỏ neo DB còn áp được.

**Đề xuất:** thêm ca số đủ 64 chữ số cho SHA256 và descriptor non-null, cùng mutant chỉ nới hex64. Không dùng số ngắn làm bằng chứng kiểu vì nó có thể chỉ bị bác bởi độ dài; giữ null descriptor xanh.

### F29 — P2 — `dot-bien-tuong-duong-hoac-thieu`

**Vị trí:** `.claude/dev/doc_receipt_thu_hoi_test.py:206`, `:208`, `:218`.

Đã chạy `audit.py attacks` và `supplement.py extra`, mỗi driver rc 0. Bốn suite mutant đều **rc 0, 153/153 · 152/152, unresolved 0**; gọi riêng `tinh` cũng pass:

| Mutant | Tác dụng phụ đo được |
|---|---|
| `pure_sys_list` | `sys.path` tăng 3 phần tử trong ba lần gọi của `tinh`. |
| `pure_module_list` | List global đổi `[] → [1863,1863,1]`. |
| `pure_io_file` | `io.open` ghi tệp scratch: `before → side-effect`. |
| `pure_posix_spawn` | Observer ghi một process Python `-c pass` ngay trong `tinh`. |

Snapshot `id()` không thấy sửa list tại chỗ. Hook `builtins.open` không thấy `io.open`; các hook process hiện tại không thấy `posix_spawn`.

**Đề xuất:** đo purity trong process cô lập; kiểm nội dung mutable thuộc hợp đồng và quan sát file/process ở tầng dùng chung. Khoá bốn biến thể trên với baseline HEAD. Tránh deepcopy mù toàn `sys`, rò hook sang suite hoặc nhận cache thư viện hợp lệ thành tác dụng phụ cấm.

## Nợ ngoài danh mục

### F30 — P3 — `no-ngoai-danh-muc`

**Tên nợ:** `K4-THONG-BAO-STALE`. **Không chặn merge.**

**Vị trí:** `.claude/dev/doc_receipt_thu_hoi.py:86`; oracle test `:65`.

Đã chạy:

```text
python3 -B "$OUT/supplement.py" "$ROOT" extra
driver rc=0
debt_stale_message suite rc=0
153/153 ca · 152/152 mutant
```

Chỉ đổi `stale, chay lai` thành `fresh, khong can chay lai`; K4 vẫn đỏ nhưng lý do nói ngược. Danh mục khai quan hệ K4 và nghĩa lý do lan K1, chưa khai chiều ngữ nghĩa thông báo stale. HEAD hiện ghi đúng.

**Đề xuất:** đợt mở danh mục sau thêm mã nguyên nhân hoặc oracle ngữ nghĩa ổn định; tránh ghim toàn bộ văn phong.

## Runtime thật trên HEAD

`audit.py runtime` rc 0:

- **592 lần gọi API**: 38 trường × 14 giá trị bất thường, cộng 60 mức sâu của ba C; không ngoại lệ ngoài hợp đồng.
- **16 mẫu API + CLI**: rỗng, byte hỏng, BOM, scalar, dữ liệu thừa, surrogate, số lớn, lồng sâu; rc chỉ 0 hoặc 12.
- Lỗi tham số/tệp không tồn tại trả 2 qua suite CLI.
- Parser thật ném `RecursionError` với mảng và object 1000 tầng trên Python 3.11.15; HEAD trả K1 đỏ/CLI 12.

Mở rộng F23 sang `RecursionError` phù hợp quyết định parser từ chối ⇒ fail-close. Đây là tập thử hữu hạn, không phải chứng minh mọi bytes đều an toàn tài nguyên.

## Đã chạy

| Lệnh/phạm vi | Rc và bằng chứng | Trạng thái |
|---|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master`; băm spec/receipt đầu-cuối | 0; khớp định danh | passed |
| Suite `doc_receipt_thu_hoi_test.py` | 0; 153/153 · 152/152 | suite passed; audit A0 failed |
| `ci_dang_ky_test.py`, tắt signer bằng env process | 0; 22/22 đăng ký, 4/4 launcher contract, 3/3 Ruff contract, **938/938 phản chứng** | passed |
| Ruff F ba tệp sản phẩm | 0; `All checks passed!` | passed |
| Ruff F so bytes registry ở base | 0; delta F=0 | passed |
| Ruff F `scripts/tl.py` HEAD/base | Cả hai rc 1, cùng 12 F821, diagnostics bằng nhau | lint nền failed; delta passed |
| `packet_loop.py doctrine-scan --root .` | 0; 10 tệp, 0 chỗ chép doctrine | passed |
| `packet_loop.py adr-song --root .` | 0; 50 ADR/50 dòng | passed |
| `git diff --numstat origin/master..HEAD` | 0; sản phẩm **+582/−0** trên ba tệp | passed theo ngoại lệ ≤650 |
| `git diff --check origin/master..HEAD` | 0 | passed |
| Năm mode probe lượt 2 | Mỗi driver 0; rc con ghi riêng | đo xong |
| Census, attacks, classifier, runtime | Mỗi driver 0 | kết luận theo từng nghĩa vụ |
| Consumer `chay_moi` với riêng suite mới | 0; nhận suite thật; bác sáu dòng lệch/zero | passed |
| Snapshot đầu/cuối | **2296/2296 tệp không đổi**, HEAD/tree/diff/index không đổi | passed |
| Kiểm manifest artifact | **174/174 băm khớp** | passed |

**not_run:** full CI, remote CI, Windows và toàn bộ registry `--chay`. Không tính check skipped thành pass. Signer chỉ tắt cho process test/fixture tạm; không đổi Git config checkout.

Môi trường: Linux, Python 3.11.15, Ruff 0.16.9, codex-cli 0.157.1. Lease/generation live và authority remote nhận theo dữ kiện người dùng, không xác minh qua mạng. Không có header launcher để độc lập xác nhận model-version/effort hiện tại; giữ `advisory_review`. Checkout được giữ chỉ đọc; mọi artifact ở scratch ngoài repository.

Đây là **lượt cuối 3/3**. Chuyển verdict cùng bằng chứng về Review Rescue Checkpoint/human audit; không gọi lượt model 4 và không tạo quyền merge/land.