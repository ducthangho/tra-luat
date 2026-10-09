<!-- Verdict codex lượt 3/3 (gpt-6-astra, reasoning effort xhigh — header log runtime "reasoning effort: xhigh", session 01a0e58d-3b8d-7c31-bc01-4175032823dc), codex_cli tại chỗ, sandbox clone riêng, trên fb8ccff8 (tree aac6522), base ceb1a3f3, spec sha256 978058983e8e…. Lượt audit DANH MỤC theo quyết định chủ kho "Đóng danh mục + 1 lượt". Chép NGUYÊN VĂN; không sửa chữ nào. Đường /tmp/review650-r3/* là đường trong sandbox reviewer; bản sao script nằm cạnh tệp này. -->
**0 P1 / 5 P2 / 1 P3**

verdict: changes_requested

```yaml
reviewed_sha: fb8ccff8bcf88aad011016afff3936c2fb4877c7
reviewed_tree: aac6522a2418ce55c092947e078fc5a41ad6746a
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
spec_sha256: 978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
receipt_sha256: ca67dc6a817b7cf8643616e4762d5f3e95c0ec7a46cf9693f9436b47c00f5960
packet: LAND-DOC-RECEIPT-THU-HOI-C1a1a
issue: 650
revision: 5
round: 3/3
review_class: sensitive
provider: openai_codex
execution_surface: codex_cli
transport: machine
assurance: advisory_review
```

Các OID và băm được đo đầu/cuối; không đổi. Đây là audit **danh mục đóng** theo chỉ thị chủ kho được người dùng cung cấp: Issue #650 comment 5861474826, lease `c1a1a-exec-2-claude-20260927`, lựa chọn “Đóng danh mục + 1 lượt”. Không dùng quy tắc săn đột biến mở của hai lượt trước. F25–F29 thuộc các chiều đã khai hoặc disposition A1; F30 nằm ngoài danh mục, chỉ P3 và **không chặn merge**.

Suite HEAD xanh **153/153 ca · 152/152 đột biến**, in `witness_killed 152 · equivalent_verified 9 · unresolved 0 · a1_khong_ap_dung 4`. Audit độc lập vẫn chưa chấp nhận A0: có hai ô ma trận thiếu, một ô hex64 chưa phân biệt, probe tính thuần bị lách, bộ phân hạng còn nhận tín dụng sai và bốn miễn A1 chưa hợp lệ. **Không tìm thấy lỗi runtime mới trên HEAD trong các phép thử đã chạy.** Các hành vi sai dưới đây, trừ việc phân hạng/khai miễn trong chính suite, là phản chứng trên bản sao đột biến, không phải lời khẳng định mã sản phẩm đang có những hành vi đó.

Hiện vật ngoài checkout: `/tmp/review650-r3/`. Trong mọi lệnh dưới, `$ROOT` là checkout được giao, `$OUT=/tmp/review650-r3`, Python dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`. Script và log được giữ cùng verdict; `ARTIFACTS.sha256` neo byte của chúng. Không có bản vá sản phẩm, commit, push hoặc lời gọi mạng.

## Đối chiếu lượt 2

Nguồn đối chiếu: `ops/reviews/land-doc-receipt-thu-hoi-c1a1a/luot2-verdict-day-du.md`, SHA `8378f331aff651e32496b02589d674239fbd92f7`. Đã chép **nguyên byte** `luot2-probe_new.py` ra scratch và chạy đủ năm mode `credit`, `mutants`, `td`, `oracle`, `followup`; mỗi lệnh điều khiển rc 0. Rc mutant/CLI con được ghi riêng, không lấy rc điều khiển làm pass.

| Finding | Kết luận | Phép đo trên HEAD mới |
|---|---|---|
| F15 | `va_ho` | Ba control cũ bị từ chối `unresolved`; sai loại, sai dòng, dòng trùng cũng bị từ chối. Nhưng `classifier_stage.py` giữ nguyên chốt decode, chuyển dòng neo duy nhất sang chẩn đoán sau K1 đỏ, vẫn nhận `witness_killed`. F25. |
| F16 | `va_ho` | M1o nhánh đỏ giữ fixture xanh; M3w/x/y có `duong_doi_chung` xanh và đích đỏ, phù hợp quyết định chủ kho. Tuy nhiên M1o2/u2/w3/x2 miễn A1 bằng `None`: cả **11/11 ca dương** đỏ trên mỗi mutant nhưng vẫn được tính giết. F26. |
| F17 | `da_va_that` | Mode `mutants`, `cli_ok_int`: suite rc 1, lỗi đúng `cli:xanh`, `ok:1` bị oracle kiểu bắt; ca đỏ `ok:0` cũng bị kiểm bằng cùng oracle. |
| F18 | `da_va_that` | Mode `followup`, mutant nuốt K5: suite rc 1. Đo bổ sung `supplement.py cli_laws` tránh tín dụng từ K1 lan: từng mutant K2–K5 chỉ kích hoạt khi K1 qua; lần lượt bị đúng `cli:k2_T`, `cli:k3_repo`, `cli:k4_head`, `cli:k5_ket_luan` bắt. K1 bị `cli:k1_bom` bắt. |
| F19 | `da_va_that` | Ba mutant cũ width/digit/year-long đều suite rc 1 vì đúng ca giờ. `census` kiểm đủ **24 ô TOK**, mỗi ca gốc pass, mutant của chính ô thất bại. Ca Unicode M3f6 cũng phân biệt. |
| F20 | `va_ho` | `purity_dynamic` và `purity_state` cũ nay suite rc 1 vì `tinh`. Nhưng cả bốn biến thể trong các nhóm đã khai—process, sys, tệp, global module—vẫn qua toàn suite. F29. |
| F21 | `da_va_that` | `str_normalize_after_decode` rc 1: `['slice','decode','parse:str']` khác trace mong đợi. Spy được phục hồi ở cả đường thành công/thất bại. Alias parser hợp lệ vẫn là giới hạn phụ thuộc cách cài đặt của spy; không tính alias đó là lỗi sản phẩm. |
| F22 | `da_va_that` | Hai phép đổi `K1 do` thành `K1 qua` đều rc 1 vì đúng ca `bom`; oracle hiện kiểm đủ bốn lý do lan K1. |
| F23 | `da_va_that` | Trên HEAD thật: số 4300 chữ số API xanh/CLI 0; 4301 và 4500 chữ số parser ném `ValueError`, API trả K1 đỏ/CLI 12. Mảng và object lồng 1000 tầng thực sự làm parser ném `RecursionError` trên Python 3.11.15, HEAD chuyển thành K1 đỏ/CLI 12. M2j/k bị ca tương ứng giết. |
| F24 | `da_va_that` | M2a: ca BOM pass và `equivalent_verified` ở cấp verdict, loại riêng spy thứ tự theo quyết định “Hai ID, hai cấp”. M2a2: cùng phép bỏ BOM bị `thu_tu_k1` giết; M2a′ ghép bị BOM giết. Không còn nhập hai cấp vào một disposition. |

Bảy finding đã vá thật trong phạm vi đo; ba finding còn vá hờ. Không suy từ đó rằng toàn bộ lớp lỗi đã đóng.

## Danh mục

`python3 -B "$OUT/audit.py" "$ROOT" census` rc 0: **130 hàng DB + 31 hàng `_theo_truong()` = 161 ID duy nhất**, 149 ca dữ liệu + 4 ca đặc biệt. Script chạy lại từng disposition và, với các hàng witness không phải M8, chạy riêng ca đích trên baseline/mutant; không chỉ đọc số suite. Log `census.jsonl` chứa từng ID, baseline, lỗi đích, A1 và disposition. Fixture khớp đủ **38/38 khoá, giá trị và kiểu** của receipt thật.

| Chiều | Đủ/thiếu ô và tính phân biệt | Bằng chứng |
|---|---|---|
| **1. Áp predicate từng trường** | **Đủ 31 ô**: 28 trường SAI + 3 C. 27 witness, 4 TD hợp lý. | Mỗi phép bỏ áp kiểu bị đúng ca trường giết; schema bị K1 che, ba C bị hai chốt kiểu còn lại + đồng nhất che. `census`, `old-td.jsonl`. Không cộng ba TD riêng thành TD cho cả nhóm. |
| **2. Hex40/hex64** | Alphabet, hoa, ngắn/dài và fullmatch có răng. **Ô bắt buộc str chưa phân biệt cho hex64**: M3u chỉ dùng số 40 chữ số ở T. | M3a/b/e/o/p/q/r/s/t/u đều giết mutant đã chọn. Nhưng `hex64_number_coerce` nhận số 64 chữ số, vẫn suite xanh 153/153 · 152/152. F28. Đổi riêng hex64 sang `match` bị `hex64_65` bắt, không báo nhầm sống. |
| **3. Int** | **Đủ** bool, float, chuỗi, null job_id theo chiều khai. | M3c/v/v2/d bị đúng `kieu_job_id`, `int_float`, `int_chuoi`, `job_id_null` bắt; int dài được đo thêm ở parser. |
| **4. Regex giờ** | **Đủ 24/24 ô** = 6 nhóm số × 3 + 6 hằng × 1; có thêm Unicode. | `census`: M3z.* đều baseline pass/mutant đích đỏ; M3f6 ASCII-only bị ca Unicode bắt. Ba mutant tổng hợp lượt 2 đều đỏ vì ca giờ. Không thêm luật lịch ngoài regex. |
| **5. Nullable** | **Đủ** bốn nhận-null và ba nhánh nhận non-null đã khai. | M3g/w/x/y/h/i/j phân biệt. W/x/y có đối chứng riêng thật sự xanh; không dùng chúng làm finding A1 mới. |
| **6. Hình dạng API** | **Thiếu hai ô K1 đỏ**: kiểu `ok` và tập khoá ngoài cùng; bốn ô nhánh xanh có disposition A1 sai. | Ma trận bên dưới; `audit.py attacks` chứng minh oracle `bom` có thể bắt hai mutant còn thiếu ID. F26/F27. |
| **7. CLI** | **Đủ trong các chiều khai**: rc, lỗi tham số, một dòng JSON, parity dict/kiểu bool, từng luật đỏ. | M1e–n/r/y/z; `cli-laws.jsonl` có ca độc lập cho K1–K5, tránh chỉ giết nhờ K1 kéo các luật khác đỏ. Hai TD base/head rỗng được chốt hex40 che. |
| **8. K1 thứ tự/parser** | **Đủ các ô đã khai**. Các witness hiện có có lỗi đích đúng; cơ chế công nhận ngoại lệ vẫn có lỗ F25. | M2a/a2/a′, b/b′/b3, c/c′/c3, d/e/e′/f/f′/g/h/i/j/k; BOM, UTF-16/32, strict, identity str, root/keys/schema/event và parser limits đã chạy. M2b′/c′ TD hợp lý vì `ValueError` bắt trùm; mutant nhóm gỡ lớp che bị giết. |
| **9. K2 C / K3 / K4 / K5** | **Đủ các ô quan hệ và giá trị khai**. | M3k–n + ba TD C; M4a–k; M5a–d; M6a–d đều đo riêng. Ca cả nhóm C sai kiểu, kho/nhánh đổi cùng nhóm, caller dương khác kho/nhánh có răng. Nghĩa thông báo stale ở F30 là nợ ngoài danh mục quan hệ này. |
| **10. Tính thuần** | Có đủ tên nhóm/ID, **chưa phân biệt trong cả bốn nhóm runtime**. | `pure_posix_spawn`, `pure_sys_list`, `pure_io_file`, `pure_module_list` đều toàn suite rc 0, đo được tác dụng phụ ngay khi `tinh` pass. M1s/t import/lời khai hiện có vẫn bị đúng ca bắt. F29. |
| **11. M8** | **Đủ hai ô backreference**, đăng ký và consumer hiện tại hoạt động. | M8a/b giết đúng; bỏ đăng ký bị `ca_dang_ky` bắt. `chay_moi` nhận dòng 3/3 · 2/2 và từ chối sáu dòng lệch/zero; nhận suite thật rc 0. `consumer.jsonl`. |
| **12. Phân hạng** | So loại/dòng/duy nhất có đo, nhưng **chưa đủ phân biệt nguyên nhân ngoại lệ**. A1 explicit có mặt nhưng bốn miễn không đúng. | Sai loại/sai dòng/neo trùng ⇒ unresolved; neo đúng chữ và duy nhất nhưng sai giai đoạn ⇒ vẫn witness. Ca gác trùng đích ⇒ unresolved; tên gác không tồn tại hoặc ca gác âm vẫn được nhận. F25/F26. |

Ma trận chiều 6, chỉ tính **kiểu/hình dạng × nhánh** đúng như danh mục khai:

| Trường | K1 đỏ | K2–K5 đỏ | Xanh |
|---|---|---|---|
| `ok` bool | **THIẾU ID** | M1o | M1o2, A1 không hợp lệ |
| `luat` dict | M1v | M1u | M1u2, A1 không hợp lệ |
| `ly_do` list | M1w | M1w2 | M1w3, A1 không hợp lệ |
| Tập ba khoá ngoài cùng | **THIẾU ID** | M1x | M1x2, A1 không hợp lệ |

M1a–d và M1q/q2 đo giá trị/lan luật/lý do, không thay hai ô kiểu/hình dạng còn thiếu. M1p đo phần tử `ly_do` là str. Tổng **9 TD** được kiểm lại và không thấy disposition TD sai: M1j/k, M2a, M2b′/c′, M3.schema_version và ba C.

## Findings

### F25 — P2 — `tin-dung-gia`: neo duy nhất vẫn nhận ngoại lệ ở sai giai đoạn

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:80`, `:435`. Chiều 12; tiếp nối F15/F2.

**Đã chạy:** `python3 -B "$OUT/classifier_stage.py" "$ROOT"` → rc 0, `classifier-stage.jsonl`:

```text
baseline byte_0x80: pass; mutant duong_fixture: pass
original_catches_preserved: true
anchor_lines: [76]
exception at 56: UnicodeDecodeError, luat={}
exception at 76: UnicodeDecodeError, luat={'K1':'do'}, loi=['khong phai UTF-8 strict']
target: byte_0x80: NEM:UnicodeDecodeError@76
disposition: ['witness_killed', 'giet']
```

Control giữ decode strict và toàn bộ catch tại vị trí cũ, chỉ viết tương đương bằng `encoding="utf-8", errors="strict"`. Sau `ghi("K1", loi)`, nó thêm một decode chẩn đoán bằng **đúng dòng neo nguyên văn**, xuất hiện duy nhất. Chốt cần đo đã xử lý lỗi đúng, K1 đã đỏ; ngoại lệ mới phát sinh từ chẩn đoán vẫn được tính cho M2b3. Bản vá đã bỏ substring và kiểm đúng số dòng, nhưng số dòng được tìm lại bằng chữ trong mutant nên không chứng minh đúng giai đoạn/chốt. Đây là control tấn công classifier; không khẳng định hàng M2b3 hiện tại tự chứa thao tác chẩn đoán đó.

**Đề xuất:** tại `ca`/`chay_dot_bien`, giữ kiểm loại và dòng, bổ sung provenance của vị trí thực thi: node/vùng parse trong `kiem_json` và giai đoạn dự kiến, được ánh xạ từ neo nguồn. Với hàng decode/parser, ngoại lệ được tính phải phát sinh trước khi K1 đã được ghi. Hoặc dùng mutant fail-open và oracle kết quả ở các hàng không cần ngoại lệ trần. Khoá bằng control trên cùng ba control cũ, wrong-type/wrong-line/duplicate-line. **Rủi ro vá:** không hard-code dòng 56; chèn dòng hợp lệ phải không làm mất mapping, và không bắt mọi ngoại lệ làm tín dụng.

### F26 — P2 — `tin-dung-gia`: bốn hàng nhánh xanh tự miễn A1

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:345`, `:347`, `:351`, `:353`, `:425`. Chiều 6/12; tiếp nối F16.

**Đã chạy:** `python3 -B "$OUT/audit.py" "$ROOT" classifier` → rc 0:

```text
M1o2, M1u2, M1w3, M1x2:
  disposition = witness_killed
  positive_count = 11; positive_pass = 0  (mỗi hàng)
M3w/x/y: duong_doi_chung=pass; duong_fixture=TinHieuChotCa; witness_killed
```

Quyết định cho nhóm nullable đã được làm đúng. Bốn hàng mới lại dùng `None` để không chạy đối chứng nào; A1 trong spec không có ngoại lệ này. “Nhánh xanh nên không áp dụng được” cũng không phải bất khả thi về kỹ thuật: cùng `classifier_stage.py`, cả bốn mutant chỉ làm sai hình dạng trên ca dương `duong_c_khac_s`, giữ `duong_fixture` xanh, đều được **witness_killed với A1 thật**. Không cần miễn A1 để có ô phân biệt.

Probe phụ trong cùng chiều: thay ca gác bằng `not_a_case` hoặc `bom` vẫn được nhận witness; cái đầu không chạy ca nào, cái sau là ca âm. Đây là điểm yếu của đường khai đối chứng, không phải lời khẳng định DB hiện đang dùng hai tên đó.

**Đề xuất:** thay bốn mutant bằng biến thể có đối chứng dương thật, như hướng đã đo; hoặc giữ unresolved tới khi có quyết định chủ kho áp riêng cho miễn A1. Kiểm tên ca gác tồn tại, là ca dương và khác đích; không chỉ kiểm `gac != dich`. Khoá bốn hàng và hai tên gác sai ở trên. **Rủi ro vá:** đừng bỏ kiểm kiểu nhánh xanh hoặc đổi ca gác sang một ca đỏ; giữ quyết định `duong_doi_chung` cho nullable.

### F27 — P2 — `dot-bien-tuong-duong-hoac-thieu`: thiếu hai ô trong ma trận kết quả đã khai

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:343`. Chiều 6; lỗi thiếu ô, không phải mutant sống.

**Đã chạy:** `python3 -B "$OUT/audit.py" "$ROOT" attacks` → rc 0; `attacks.jsonl`:

```text
shape_k1_ok:   baseline bom=pass; mutant bom=TinHieuChotCa, ok=0
shape_k1_keys: baseline bom=pass; mutant bom=TinHieuChotCa, extra=1
```

Đã đối chiếu cả **161 ID**, không có hàng kiểu `ok` ở nhánh return K1 đỏ, cũng không có hàng tập khoá ngoài cùng ở nhánh ấy. Có oracle tổng bắt được không thay nghĩa vụ ô/ID theo danh mục đóng. Hai phản chứng đo trên `_TRA1`, giữ fixture dương nguyên vẹn; có thể bổ sung trực tiếp, không phải thay đổi miền kiểm.

**Đề xuất:** thêm hai ID và mutant vào DB, dùng `bom` làm đích, `duong_fixture` làm gác; kiểm ma trận 4×3 có đủ 12 ô. **Rủi ro vá:** không lấy M1b (thiếu trạng thái trong `luat`) hoặc M1q (lý do lan) thay cho kiểu `ok`/khoá ngoài cùng.

### F28 — P2 — `dot-bien-tuong-duong-hoac-thieu`: bắt buộc str của hex64 chưa có phép phân biệt

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:126`, `:311`. Chiều 2.

**Đã chạy:** `python3 -B "$OUT/audit.py" "$ROOT" attacks` → rc 0; tiến trình con:

```text
python3 -B /tmp/review650-r3/hex64_number_coerce/.claude/dev/doc_receipt_thu_hoi_test.py
rc=0
witness_killed 152 · equivalent_verified 9 · unresolved 0 · a1_khong_ap_dung 4
153/153 ca QUA · 152/152 dot bien GIET
workflow_definition_sha256 = int('1' * 64): HEAD K2=do; mutant ok=true
```

Mutant tại `_khop` chỉ thay miền hex64:

```python
if mau == "[0-9a-f]{64}":
    return lambda v: re.fullmatch(mau, str(v)) is not None
```

Mọi mỏ neo DB còn áp được. M3u dùng `hex_la_so` chỉ đặt số ở `T` (hex40), nên không phân biệt việc hex64 ép số thành str. `_theo_truong` của `workflow_definition_sha256` dùng chữ hoa; của descriptor dùng chuỗi quá ngắn; cả hai vẫn bị mutant bác. Đây là đúng điều kiện **bắt buộc str** của hex40/hex64 trong chiều đã khai, không mở sang predicate mới.

**Đề xuất:** thêm ca số 64 chữ số cho `workflow_definition_sha256` và nhánh non-null descriptor, cùng mutant chỉ nới hex64; giữ nhóm hex40 độc lập. Oracle K2 phải đổi màu đúng ca. **Rủi ro vá:** không coi “số ít chữ số bị bác” là bằng chứng kiểm kiểu—nó có thể chỉ chết vì độ dài; giữ ca null descriptor xanh.

### F29 — P2 — `dot-bien-tuong-duong-hoac-thieu`: probe tính thuần lọt bốn nhóm đã khai

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:206`, `:208`, `:218`. Chiều 10; tiếp nối F20.

**Đã chạy:** `audit.py attacks` và `supplement.py extra`, mỗi driver rc 0. Bốn suite con dưới đây đều rc 0, **153/153 ca · 152/152 mutant, unresolved 0**; gọi riêng oracle `tinh` cũng pass:

| Bản sao mutant | Tác dụng phụ độc lập đo được |
|---|---|
| `/tmp/review650-r3/pure_sys_list/.claude/dev/doc_receipt_thu_hoi_test.py` | `sys.path.append(...)`; sau ba lần gọi của `tinh`, độ dài tăng **3**. |
| `/tmp/review650-r3/pure_module_list/.claude/dev/doc_receipt_thu_hoi_test.py` | List global `_REVIEW_LOG`: `[] → [1863,1863,1]`. |
| `/tmp/review650-r3/pure_io_file/.claude/dev/doc_receipt_thu_hoi_test.py` | `io.open` ghi tệp scratch; nội dung `before → side-effect`. |
| `/tmp/review650-r3/pure_posix_spawn/.claude/dev/doc_receipt_thu_hoi_test.py` | `os.posix_spawn` + `waitpid` khi raw là `{`; observer ghi **một tiến trình Python `-c pass`** ngay trong `tinh`. |

Snapshot `id()` không đổi khi sửa list tại chỗ. Patch `builtins.open` không chặn `io.open`; patch `Popen`/`system`/`popen` không quan sát `posix_spawn`. Những biến thể này không đổi kết quả nghiệp vụ và không dùng mạng. Tệp ghi là đường tuyệt đối cố định bên trong scratch của reviewer; không dựng nội dung đường dẫn thoát cây.

**Đề xuất:** chạy phép đo purity trong process cô lập; với sys/module, đo nội dung trạng thái mutable thuộc hợp đồng hoặc baseline/readback có cấu trúc; với file/process, quan sát các sự kiện ở tầng dùng chung phù hợp Python/OS, thay vì chỉ một vài hàm tiện ích. Khoá bốn biến thể đã đo và một baseline HEAD không có tác dụng phụ. **Rủi ro vá:** phân biệt cache thư viện hợp lệ với trạng thái caller/module; tránh deepcopy mù toàn `sys`, rò monkeypatch/audit hook sang suite hoặc biến test thành phụ thuộc Windows chưa đo. Không tuyên bố đây là sandbox chặn mọi tác dụng phụ chỉ từ vài hook.

## Nợ ngoài danh mục

### F30 — P3 — `no-ngoai-danh-muc`: chưa gác nghĩa của thông báo stale

**Không chặn merge.** Tên nợ: `K4-THONG-BAO-STALE`. Đây là khoảng trống đã được ghi trong audit lượt 2, nay giữ đúng mức nợ theo checkpoint.

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi.py:86`; oracle `.claude/dev/doc_receipt_thu_hoi_test.py:65`.

**Đã chạy:** `python3 -B "$OUT/supplement.py" "$ROOT" extra` → rc 0; suite con `debt_stale_message/.claude/dev/doc_receipt_thu_hoi_test.py` → rc 0, **153/153 · 152/152**. Chỉ đổi chữ `stale, chay lai` thành `fresh, khong can chay lai`; receipt lệch S vẫn K4 đỏ nhưng lý do nói “không cần chạy lại”.

Danh mục chiều 9 khai M5a–d về quan hệ S/base, H/head và nguồn caller; chiều 6 khai nghĩa lý do lan **K1**. Chưa khai chiều ngữ nghĩa thông báo stale K4. Theo authority lượt này, không nâng phần thiếu ấy thành finding chặn. HEAD hiện ghi thông báo đúng.

**Đề xuất:** successor/đợt mở danh mục sau thêm mã nguyên nhân stale hoặc oracle ngữ nghĩa ổn định cùng mutant trên. **Rủi ro vá:** tránh ghim toàn bộ câu chữ, dấu câu hoặc ngôn ngữ hiển thị nếu không thuộc hợp đồng.

## Runtime thật trên HEAD

`python3 -B "$OUT/audit.py" "$ROOT" runtime` rc 0, `runtime.jsonl`:

- **592 lần gọi API**: 38 trường × 14 giá trị bất thường, cộng 60 mức sâu 950–1009 cho ba trường C. Không ngoại lệ ngoài hợp đồng; kết quả giữ dict ba khoá và bool `ok`.
- **16 mẫu API + CLI**, gồm rỗng/whitespace, BOM riêng, byte UTF-8 hỏng, scalar/null, dữ liệu thừa, surrogate, số lớn và lồng sâu. Rc chỉ 0 hoặc 12; không traceback. Ca lỗi tham số/tệp không tồn tại trả 2 được đo bởi suite/CLI oracle.
- Parser thuần `json.loads` ném `RecursionError` thật với cả mảng và object 1000 tầng; HEAD API trả K1 đỏ, CLI 12. Việc mở rộng F23 sang RecursionError phù hợp quyết định **parser từ chối ⇒ K1 đỏ fail-close**, không thấy lệch spec cần finding.
- `NaN`/Infinity được dùng như đầu vào không chuẩn để thử crash; không tuyên bố Python parse được chúng là chứng minh JSON chuẩn. Surrogate trong `discovery` vẫn là str theo miền hiện tại. Không bổ sung luật ngữ nghĩa cho các cấu trúc ngoài phạm vi.

Đây là tập thử hữu hạn, không phải bằng chứng mọi bytes đều không thể gây lỗi hoặc cạn tài nguyên. Mode `followup` còn xác nhận số 4500 chữ số parse được trong process probe khi tắt giới hạn int, rồi phục hồi cấu hình; sản phẩm không sửa cấu hình interpreter.

## Đã chạy

`run_checks.py` ghi stdout, stderr và rc thật vào `checks.jsonl`; log dài để trong scratch. Các số cổng dưới đây được đọc từ output dương, không suy từ rc trơn.

| Lệnh/phạm vi | Rc và bằng chứng | Trạng thái |
|---|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master`; băm spec/receipt đầu-cuối | 0; khớp khối YAML | passed |
| `python3 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; 153/153 · 152/152; 152 witness, 9 TD, 0 unresolved, 4 A1 miễn | suite passed; audit A0 failed |
| `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 -B .claude/dev/ci_dang_ky_test.py` | 0; đăng ký 22/22, launcher contract 4/4, Ruff contract 3/3, **938/938 phản chứng**, `TỔNG: ĐẠT` | passed |
| `python3 -m ruff check --no-cache --select F` trên ba tệp write set | 0; `All checks passed!` | bare lint passed |
| Cùng Ruff trên bytes registry `origin/master` qua `--stdin-filename ... -` | 0; không F; hai tệp mới cũng không F ⇒ delta 0 | delta passed |
| Ruff F trên `scripts/tl.py`, stdin từ `git show HEAD:scripts/tl.py` và `origin/master:scripts/tl.py` | Cả hai rc 1, cùng 12 F821; diagnostics bằng nhau ⇒ delta 0 | bare lint failed sẵn ở nền; delta passed |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; 10 tệp, 0 chỗ chép doctrine | passed |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0; 50 ADR/50 dòng khớp 1–1 | passed |
| `git diff --numstat origin/master..HEAD` | 0; sản phẩm +1 registry, +114 module, +467 test = **+582/−0** | passed theo ngoại lệ ≤650 |
| `git diff --check origin/master..HEAD` | 0; không lỗi whitespace | passed |
| `probe_new.py "$ROOT" credit / mutants / td / oracle / followup` | Năm driver rc 0; rc con và assertion trong `old-*.jsonl` | đo xong; kết luận theo bảng F15–F24 |
| `audit.py "$ROOT" census / attacks / classifier / runtime` | Bốn driver rc 0; từng ID, mutant sống/chết và runtime có log riêng | đo xong; có failure nghĩa vụ F26–F29 |
| `classifier_stage.py "$ROOT"` | 0; tín dụng sai tái lập; 4/4 cách giữ A1 có witness | F25 failed; remediation probe passed |
| `supplement.py "$ROOT" cli_laws / registry / ruff / extra` | Bốn driver rc 0; 5 luật CLI phân biệt, consumer 1 dương/6 âm, 4 nhóm purity bị lách và nợ stale | kết quả theo từng nghĩa vụ |
| Snapshot đầu/cuối | 0; **2296/2296 tệp quan sát không đổi**; HEAD/tree/status/diff/index không đổi | passed |

Numstat toàn bộ còn chứa spec đóng băng và hiện vật hai lượt review mang theo như assignment; không gộp chúng thành số dòng sản phẩm. Không gọi ngoại lệ 650 là đạt trần gốc ADR-0044. Registry diff chỉ thêm một dòng MOI.

**not_run:** full CI, CI remote/Windows, toàn bộ nhóm `ci_dang_ky_test.py --chay`, fetch/API và deploy. Đã chạy consumer `chay_moi` thật với **riêng suite mới**, cộng runner giả cho regex; không khai đó là chạy toàn registry `--chay`. Không có check skipped nào được tính pass. Signer chỉ bị tắt cho process test và fixture Git tạm do registry sở hữu; reviewer không tạo commit hay sửa Git config checkout.

**Môi trường/giới hạn:** Linux, Python 3.11.15, Ruff 0.16.9, codex-cli 0.157.1; detached HEAD; `core.abbrev=7`. Origin là mirror local `/home/user/tra-luat` đã được cấp, không xác minh lại GitHub qua mạng. Lease/generation live và comment authority nhận theo dữ kiện người dùng, không tự chứng nhận đã đọc remote. Reviewer là Codex thuộc họ GPT-6 theo system; không có header launcher hiện tại để độc lập xác nhận model-version/effort/session ID, nên không nâng khỏi `advisory_review`. Executor Claude theo assignment; không có reviewer Claude hoặc subagent review. Sandbox thực tế workspace-write; reviewer giữ checkout chỉ đọc bằng cách đặt mọi artifact/cache ra ngoài. Snapshot chứng minh không có delta ở hai mốc, không chứng minh lịch sử chưa từng có ghi rồi hoàn nguyên; không snapshot repo mirror nguồn nằm ngoài phạm vi review.

Skill áp dụng: [cross-review](/tmp/claude-0/-home-user-tra-luat/0682048d-075d-5414-b3ff-642b89411167/scratchpad/rv3/.agents/skills/cross-review/SKILL.md). Không gửi verdict ra ứng dụng ngoài.

## Lịch sử lớp và điểm dừng

| Slug giữ nguyên | Nối lịch sử | Kết luận lượt 3 |
|---|---|---|
| `tin-dung-gia` | F2 → F15 → F25; F16 → F26 | Còn P2: kiểm nguyên nhân exception và A1. |
| `dot-bien-tuong-duong-hoac-thieu` | F17–F22; F20 → F29; thêm F27/F28 trong chiều đóng | Các biểu hiện CLI/giờ/parser/lý do cũ đã vá; catalog vẫn thiếu hoặc không phân biệt. |
| `lech-dac-ta` | F23/F24 | Hai biểu hiện cũ đã đóng theo các quyết định chủ kho; không reset lịch sử. |
| `no-ngoai-danh-muc` | Khoảng trống thông báo stale đã ghi ở audit lượt 2 → F30 | Nợ P3, không chặn theo checkpoint hiện hành. |

Đây là **lượt cuối 3/3**. Verdict chuyển lại Review Rescue Checkpoint/human audit với các hiện vật đã đo; không đề nghị hay tự gọi lượt model 4. `changes_requested` này không sửa Packet, không cấp lease và không tạo quyền merge/land.
