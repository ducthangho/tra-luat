<!-- Verdict codex lượt 2/2 (gpt-6-astra, reasoning effort xhigh — header log runtime "reasoning effort: xhigh", session 01a0e570-0ced-7192-a092-5a85901eacae), codex_cli tại chỗ, sandbox clone riêng, trên 8378f331 (tree 2c4d29f), base ceb1a3f3, spec sha256 978058983e8e…. Chép NGUYÊN VĂN; không sửa chữ nào. Đường /tmp/review650-r2/* là đường trong sandbox reviewer; bản sao các script nằm cạnh tệp này. -->
**9 P1 / 1 P2 / 0 P3**

verdict: changes_requested

```yaml
reviewed_sha: 8378f331aff651e32496b02589d674239fbd92f7
reviewed_tree: 2c4d29f753ff1367ba5fa829153f771d259ffb8d
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
spec_sha256: 978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
packet: LAND-DOC-RECEIPT-THU-HOI-C1a1a
issue: 650
revision: 5
review_class: sensitive
round: 2/2
provider: openai_codex
execution_surface: codex_cli
transport: machine
assurance: advisory_review
```

Các băm trên được đo ở đầu và cuối, không lấy từ lời khai executor. Reviewer độc lập với executor Claude; không có reviewer Claude trong lượt này. Đây là review offline theo chỉ thị người dùng, không phải approval hay quyền land. Ngưỡng áp dụng: lỗi hành vi hoặc vi phạm A0/A1 chặn merge theo spec là P1; lệch hợp đồng có hậu quả là P2.

**Kết quả chính:** 13/14 biểu hiện cũ đã được vá trên đúng phép đo của lượt 1; F2 mới vá một phần. Suite gốc đạt **128/128 ca, 109/109 đột biến**, nhưng **9 bản đột biến mới vẫn qua nguyên suite**, bộ phân hạng còn cấp tín dụng giả, và có một lỗi runtime thật trên HEAD. Không được dùng số tổng xanh để đóng A0. F17–F22 là lỗi độ phủ/oracle, không khẳng định mã sản phẩm hiện chứa các hành vi mutant; F23 là lỗi runtime đo trực tiếp trên HEAD.

Mọi hiện vật ở `/tmp/review650-r2/`, ngoài checkout. Script [probe650.py](/tmp/review650-r2/probe650.py) tái chạy lượt 1, chỉ chuyển mỏ neo timestamp sang `\d`; [probe_new.py](/tmp/review650-r2/probe_new.py) chứa các phép phản chứng mới và cặp neo/thay chính xác; [run_checks.py](/tmp/review650-r2/run_checks.py) lưu command, rc và output cổng. Những bản đột biến là dữ liệu phản chứng, không phải patch để áp vào branch.

## Đối chiếu lượt 1

Nguồn: `ops/reviews/land-doc-receipt-thu-hoi-c1a1a/luot1-VERDICT.md`, SHA lượt 1 `96a93226109038331fb09d2a35bd71b73e6e43be`. Trong các lệnh dưới, cwd là checkout được giao. Lệnh `probe650.py "$PWD" <mode>` chạy thành công rc 0; rc suite/CLI con được ghi riêng. Mỗi suite mutant trong bảng đã được chạy thật bằng `python3 -B /tmp/review650-r2/<tên>/.claude/dev/doc_receipt_thu_hoi_test.py`.

| Finding | Trạng thái | Lệnh đã chạy / output phân biệt trên HEAD mới |
|---|---|---|
| F1 | `da_va_that` | `python3 -B /tmp/review650-r2/probe650.py "$PWD" actual`: `ket_luan=[]`, `{}`, list có phần tử, `null`, số ⇒ K5 `do`, dict đủ ba khoá; CLI list **rc 12**, `ok:false`, không traceback. Đảo tuple về frozenset: ca `k5_ket_luan_list` ném TypeError, bị oracle bắt. |
| F2 | `va_ho` | Mode `credit`: cả ba lỗi vô can cũ (`len(0)`, tra dict, decode byte chẩn đoán) nay `unresolved`. Nhưng `probe_new.py "$PWD" credit` có **3/3** biến thể vẫn `witness_killed`, giữ nguyên chốt cần đo; F15. |
| F3 | `da_va_that` | Mode `mutants`, suite `hex_charset` **rc 1**: `HONG hex40_ngoai_af`, `HONG hex64_ngoai_af`; mutant nhận `g` nhưng ca đích đòi K2 đỏ. |
| F4 | `da_va_that` | Mode `mutants`, suite `int_float` **rc 1**: `HONG int_float`, `run_id=1.5` làm mutant `ok:true` trái K2 đỏ. |
| F5 | `da_va_that` | Mode `mutants`, suite `hex64_length` **rc 1**: `HONG hex64_65`; mutant nhận 65 ký tự, ca đích đổi màu. |
| F6 | `da_va_that` | Mode `mutants`, suite `timestamp_z` **rc 1**: `HONG gio_hau_to_X`. Mỏ neo đã chuyển sang `\dZ`; lỗi hậu tố X được chặn. Những thành phần khác còn hở ở F19. |
| F7 | `da_va_that` | Mode `mutants`, suite `ok_not_bool` **rc 1**: `HONG duong_fixture`, API `ok:1` bị kiểm `type is bool` bắt. Nhánh CLI còn hở ở F17. |
| F8 | `da_va_that` | Mode `mutants`, suite `cli_dict_lost` **rc 1**: `stdout khong phai MOT dong JSON dung dict ... '{"ok": true}'`. Phạm vi parity còn thiếu ở F17/F18. |
| F9 | `da_va_that` | Mode `extra`, suite `bom_order_v2` **rc 1**: `thu tu ['decode','slice','decode','parse'] != ['slice','decode','parse']`. Trace gốc: thường `slice,decode,parse:str`; BOM chỉ `slice`. Phép đo identity str còn hở ở F21. |
| F10 | `da_va_that` | Mode `extra`, suite `reasons_not_strings` **rc 1**: `[0,…]` bị bắt; đo riêng ca `k5_rc` cũng đỏ với `ly_do:[0]`. Ý nghĩa lý do lan còn hở ở F22. |
| F11 | `da_va_that` | Mode `extra`: `٢026-09-25T01:25:14Z` khớp spec và HEAD trả `ok:true`. Đột biến ASCII-only `M3f6` làm chính ca `gio_unicode_so` đỏ. |
| F12 | `da_va_that` | Mode `caller`, suite `kho_fixed` **rc 1**: `HONG duong_kho_khac`; caller và cả nhóm đổi kho đúng vẫn được HEAD nhận. |
| F13 | `da_va_that` | Mode `caller`, suite `nhanh_fixed` **rc 1**: `HONG duong_nhanh_khac`; caller và cả nhóm đổi `main` đúng được HEAD nhận. |
| F14 | `da_va_that` | Mode `caller`, suite `hex_numeric_coerce` **rc 1**: `HONG hex_la_so`; int dài 40 chữ số bị HEAD bác, mutant ép str bị ca đích bắt. |

Log đầy đủ: `old-actual.jsonl`, `old-credit.jsonl`, `old-mutants.jsonl`, `old-extra.jsonl`, `old-caller.jsonl`; log từng suite là `<tên>.log`. `targeted-fixes.jsonl` lưu thêm 14 phép đo trực tiếp đúng ca đích trên mutant DB. Kết luận vá thật ở bảng chỉ đóng **biểu hiện cụ thể cũ**; không đóng toàn lớp khi đã có phản chứng mới bên dưới. Không dùng lỗi mỏ neo của meta-test để thay cho bằng chứng ca đích đỏ.

## Findings mới

**F15 — P1 — `tin-dung-gia` — mảnh dòng không chứng minh đúng giai đoạn gây lỗi; F2 còn mở.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:67`, `:338`, `:339`.

Đã chạy `python3 -B /tmp/review650-r2/probe_new.py "$PWD" credit`, rc 0; log `new-credit.jsonl`:

```text
M2d  : NEM:TypeError@type(r["schema_version"]) is int             -> witness_killed
M2e' : NEM:KeyError@[KIEU[k](r[k]) for k in ["tree_S"]]          -> witness_killed
M2b' : NEM:UnicodeDecodeError@raw.decode("utf-8", "strict")      -> witness_killed
fixture_positive=True; original_guard_preserved=True (cả ba)
```

Mỗi mutant chỉ thêm một thao tác chẩn đoán **sau `ghi("K1", loi)`, trong nhánh `if loi`**. Chốt root-dict, tập khoá và `try` decode vẫn nguyên. K1 đã xác định đỏ đúng trước khi chẩn đoán ném. Classifier vẫn gán công cho nghĩa vụ cũ vì `manh in ...`; nó không kiểm frame/địa điểm thực thi của chốt đã bị thay. Chuỗi `raw.decode(` còn bỏ qua cả codec và vị trí.

Đề xuất: sửa `ca()`/`chay_dot_bien()` để evidence ngoại lệ neo vị trí executable cụ thể của mutant và giai đoạn dự kiến, thay vì chỉ text substring. Với root/keys có thể dùng mutant fail-open trả kết quả quan sát được để ca thất bại bằng assertion, giảm lệ thuộc ngoại lệ. Giữ ba control ở trên, cùng control ngoại lệ khác loại và fixture đỏ. Rủi ro vá: ghim số dòng tuyệt đối dễ hỏng sau chèn dòng; ánh xạ vị trí từ bản mutant/AST, không nới về dò chuỗi khi không đo được.

**F16 — P1 — `tin-dung-gia` — nhắm `duong_fixture` được miễn chốt A1.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:247`, `:277`, `:332`.

Cùng lệnh `probe_new.py "$PWD" credit`, rc 0:

```text
M3w descriptor_cam_null : fixture ok=False, K2=do -> witness_killed
M3x policy_cam_null     : fixture ok=False, K2=do -> witness_killed
M3y profile_cam_null    : fixture ok=False, K2=do -> witness_killed
M1o ok_la_int           : fixture ok=1           -> witness_killed
control raise RuntimeError("unrelated"), target=duong_fixture -> witness_killed
```

Đây là bốn hàng thật trong DB, không chỉ probe giả. `if dich != "duong_fixture"` bỏ kiểm fixture dương cho đúng những hàng này. A1 đóng băng đòi **mọi** mutant giữ fixture dương xanh; tổng 109 đang tính cả bốn trường hợp không đạt A1. Control cho thấy đổi tên ca đích cũng mở đường cho lỗi hoàn toàn vô can.

Đề xuất: đưa A1 thành điều kiện độc lập, không suy từ tên ca đích. Chọn mutant vẫn giữ fixture nền nếu có thể; nếu nghĩa vụ null/bool bắt buộc làm đỏ chính fixture, phải khai mâu thuẫn A0–A1 và xin quyết định/revision tại checkpoint, giữ `unresolved` tới khi có authority. Không xoá các ca dương null để làm số đẹp. Ca khoá: bốn hàng trên và lỗi runtime vô can phải không được chứng nhận A1 đạt. Rủi ro vá: chỉ bỏ câu `if` sẽ làm các hàng này unresolved đúng nhưng chưa giải quyết hợp đồng; không coi đó là đã hoàn tất độ phủ.

**F17 — P1 — `dot-bien-tuong-duong-hoac-thieu` — parity dict của CLI vẫn coi số nguyên bằng bool.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:128`, `:281`.

Đã chạy `python3 -B /tmp/review650-r2/cli_ok_int/.claude/dev/doc_receipt_thu_hoi_test.py`, **rc 0**:

```text
nghia vu: witness_killed 109 · equivalent_verified 6 · unresolved 0
doc_receipt_thu_hoi tests: 128/128 ca QUA · 109/109 dot bien GIET
CLI fixture: rc=0,  stdout ... "ok": 1
CLI H stale: rc=12, stdout ... "ok": 0
```

Mutant chỉ thêm `kq["ok"] = int(kq["ok"])` trước `print`; API vẫn đúng bool. So dict bằng `==` không phân biệt `1/True`, `0/False`, nên bản vá F7 chưa được áp ở biên JSON CLI. M1 đòi `ok` bool.

Đề xuất: kiểm schema/kiểu của JSON CLI bằng cùng oracle hình dạng độc lập như API, rồi mới so giá trị. Thêm ID và mutant chỉ đổi kiểu ở CLI, ca rc 0 và rc 12. Rủi ro vá: không dùng so raw stdout để ép thứ tự khoá hoặc khoảng trắng không thuộc hợp đồng.

**F18 — P1 — `dot-bien-tuong-duong-hoac-thieu` — CLI parity chưa thử receipt đỏ, có thể đổi K5 đỏ thành thành công.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:114`, `:120`, `:127`.

Đã chạy `python3 -B /tmp/review650-r2/cli_ignores_k5/.claude/dev/doc_receipt_thu_hoi_test.py`, **rc 0**, nguyên **128/128 · 109/109**, `unresolved 0`. Sau đó CLI con qua `probe_new.py "$PWD" followup`:

```text
receipt ket_luan=[]
HEAD API: ok=False, K5=do
mutant CLI: rc=0, {"luat":{"K1":"qua",...,"K5":"qua"},"ly_do":[],"ok":true}
```

Mutant thêm nhánh ngay trước print: nếu K5 đỏ thì thay kết quả bằng dict xanh. `ca_cli` luôn ghi `ma(FIX)`; ca rc 12 duy nhất thay caller H, chỉ đi K4. Vì thế mất toàn bộ kết quả lỗi K1/K2/K3/K5 tại CLI vẫn có thể lọt. Đặc biệt các ca sai kiểu `ket_luan` mới chỉ bảo vệ API; CLI list ở F1 do reviewer đo, chưa nằm trong suite sản phẩm.

Đề xuất: cho ca CLI nhận bytes/fixture và tham số riêng, đo parity cả từng nhánh luật đỏ, gồm list/dict/null/số ở kết luận và một K1 đỏ. Thêm mutant làm sai riêng nhánh đỏ CLI. Rủi ro vá: đừng dựng expected bằng một API đã bị cùng lỗi biến đổi; kiểm vectơ luật/kiểu mong đợi độc lập trước khi so parity.

**F19 — P1 — `dot-bien-tuong-duong-hoac-thieu` — timestamp còn thiếu nghĩa vụ chữ số và độ rộng của các nhóm.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:96`, `:233`.

Đã chạy cả ba lệnh `python3 -B /tmp/review650-r2/<tên>/.claude/dev/doc_receipt_thu_hoi_test.py`, từng lệnh **rc 0**, nguyên **128/128 · 109/109**, `unresolved 0`:

| Tên | Đột biến tại `_khop` | Input phản chứng | HEAD → mutant |
|---|---|---|---|
| `timestamp_width` | Đổi các `\d\d` thành `\d+` | `2026-9-25T1:2:3Z` | K2 đỏ → `ok:true` |
| `timestamp_digit` | Đổi các `\d\d` thành `..` | `2026-aa-25T01:25:14Z` | K2 đỏ → `ok:true` |
| `timestamp_year_long` | Đổi `\d{4}` thành `\d{4,5}` | `20266-09-25T01:25:14Z` | K2 đỏ → `ok:true` |

Các mỏ neo DB đều được giữ; đây là đột biến sống thực sự, không phải meta-test không áp được. M3f2 đo năm thiếu, M3f3/f4 đo dấu phân cách, M3f5 đo Z; chúng không chứng minh năm không dư, các nhóm còn lại đúng hai chữ số và không nhận chữ. A0 yêu cầu phân rã predicate ghép, không chỉ có một ID đại diện toàn regex.

Đề xuất: lập ID theo thành phần mẫu và miền chữ số/độ dài, thêm biên ít/đủ/nhiều và chữ không phải số cho từng nhóm. Ca dương Unicode vẫn giữ. Rủi ro vá: không thêm ràng buộc lịch hoặc ASCII-only ngoài regex đóng băng.

**F20 — P1 — `dot-bien-tuong-duong-hoac-thieu` — `tinh` chỉ kiểm import tĩnh, không kiểm purity hay cấm tiến trình con.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:156`, `:159`, `:282`.

Đã chạy hai suite `purity_dynamic` và `purity_state`, từng lệnh **rc 0**, nguyên **128/128 · 109/109**, `unresolved 0`:

```text
purity_dynamic: thêm __import__("subprocess").run([sys.executable,"-c","pass"],check=True)
purity_state:   tăng sys._receipt650_probe_count trong mỗi lời gọi kiem_json
probe followup: đã quan sát 1 lời gọi subprocess.run; kết quả vẫn ok=True
probe state:   side_effect=1
```

Các lời gọi thật của mutant chỉ khởi động Python `pass`, không git/mạng. AST `Import`/`ImportFrom` không thấy `__import__`, và tập import cho phép `sys` không ngăn sửa trạng thái toàn cục. M1s đang chứng minh một quy ước import, chưa chứng minh M1 hàm thuần và §3 không mở tiến trình con. Điều này là lỗi oracle A0, không khẳng định HEAD thật đang mở tiến trình.

Đề xuất: tách nghĩa vụ import/lời khai khỏi hành vi runtime; đặt probe các biên side effect trong phạm vi gọi `kiem_json` (process/network/file/state) và ca lặp với input giống nhau. Bổ sung hai control trên; static scan chỉ là lớp hỗ trợ. Rủi ro vá: không chặn I/O đọc receipt của `main()` vốn được M1 cho phép, và không biến denylist import thành lời hứa chứng minh mọi chương trình Python đều thuần.

**F21 — P1 — `dot-bien-tuong-duong-hoac-thieu` — oracle “chính str đã decode” thiếu input làm phép chuẩn hoá tạo str khác.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:134`, `:144`, `:149`, `:219`, `:284`.

Đã chạy `python3 -B /tmp/review650-r2/str_normalize_after_decode/.claude/dev/doc_receipt_thu_hoi_test.py`, **rc 0**, nguyên **128/128 · 109/109**, `unresolved 0`. Mutant thêm `chuoi = chuoi.strip()` sau decode, trước parser. `probe_new.py "$PWD" oracle`, rc 0:

```text
input = khoảng trắng + receipt + newline
parser.same_identity=False
parser.same_value=False
ok=True
```

`ma(FIX)` không có whitespace ở hai đầu, nên `.strip()` trả lại chính object cũ trên input duy nhất của spy. Với input JSON whitespace hợp lệ, parser nhận một chuỗi khác, trái M2(c). M2c chỉ có mutant bytes; M2h chỉ có mutant decode trước BOM; thiếu ID/phép đo độc lập cho biến đổi str sau decode.

Đề xuất: bổ sung input có whitespace, giữ object decode và kiểm identity ở parser; tách ID “nhận chính str” khỏi “không nhận bytes” và “decode một lần”. Ca khoá là mutant `.strip()` trên cả input thường/whitespace. Rủi ro vá: spy phải restore trong `finally`, không tạo lỗi do can thiệp stdlib rồi tính là giết mutant.

**F22 — P1 — `dot-bien-tuong-duong-hoac-thieu` — có tiền tố lý do chưa chứng minh K1 đỏ là nguyên nhân.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:73`, `:280`.

Đã chạy `python3 -B /tmp/review650-r2/k1_reason_wrong_semantic/.claude/dev/doc_receipt_thu_hoi_test.py`, **rc 0**, nguyên **128/128 · 109/109**, `unresolved 0`:

```text
raw=b'{'
luat: K1..K5 đều do
ly_do: ["K1: khong phai JSON", "K2: K1 qua", "K3: K1 qua", "K4: K1 qua", "K5: K1 qua"]
```

Mutant thay riêng phần lý do `K1 do` thành `K1 qua` trước `ly_do.extend`, giữ nguyên mỏ neo các mutant DB. Oracle chỉ kiểm `startswith(k + ":")`, nên thông điệp nói ngược nguyên nhân vẫn được nhận. M1 yêu cầu K2–K5 đỏ **với lý do K1 đỏ**; M1q mới đo có/không dòng lý do, chưa đo nội dung nghĩa vụ ấy.

Đề xuất: kiểm nguyên nhân lan K1 cho từng K2–K5, thêm mutant đổi nghĩa/chỉ nhầm luật nguồn. Không cần ghim toàn bộ văn phong; có thể dùng mã nguyên nhân ổn định trong chuỗi nếu giữ schema. Rủi ro vá: tránh kiểm substring mơ hồ cho phép `K1 qua, không phải K1 do` cũng pass.

**F23 — P1 — `lech-dac-ta` — parser làm hàm/CLI ném ngoại lệ với một số nguyên JSON hợp lệ.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi.py:57`, `:58`, `:105`.

Đã chạy trên **HEAD thật**, không mutant: `python3 -B /tmp/review650-r2/probe_new.py "$PWD" followup`, rc script 0; command CLI và traceback đủ ở `new-followup.jsonl` / `actual-bigint.log`:

```text
receipt: 6352 bytes; đúng 38 khoá; chỉ run_id đổi thành int có 4500 chữ số
API: ValueError: Exceeds the limit (4300 digits) for integer string conversion
CLI: rc=1, stdout=''
control ở process probe riêng, int_max_str_digits=0:
  JSON parse thành int; chỉ run_id khác FIX; HEAD trả ok=True, K1..K5 qua
```

M3 không đặt trần chữ số cho int; M1 đòi dict và CLI rc 0/12/2. `json.loads` trên Python 3.11.15 ném `ValueError` cho đầu vào này, không phải `JSONDecodeError`, nên lọt hai nhánh catch. Đây không phải input khổng lồ gây hết bộ nhớ. Kết quả còn lệ thuộc cấu hình interpreter ngoài tham số hàm.

Đề xuất: xác định rõ miền/parser số nguyên theo hợp đồng. Nếu giữ M3 hiện tại, dùng cách parse int cục bộ phù hợp miền; nếu muốn giới hạn tài nguyên, cần authority sửa spec và trả kết quả lỗi có cấu trúc cho giới hạn đó. Thêm ca 4300/4301/4500 chữ số qua API và CLI. Rủi ro vá: không gọi `sys.set_int_max_str_digits(0)` trong hàm sản phẩm vì thay trạng thái toàn process và phá purity; không bắt rộng mọi Exception rồi che lỗi lập trình. Control của reviewer đổi cấu hình chỉ trong process probe, phục hồi trong `finally`.

**F24 — P2 — `lech-dac-ta` — M2a có phép đo mạnh hơn, nhưng disposition trái A2 đóng băng.**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:211`, `:213`; spec A2 tại `ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md:175`.

Đã chạy `python3 -B /tmp/review650-r2/probe_new.py "$PWD" td`, rc 0:

```text
M2a bỏ riêng chốt BOM:
  ca bom: PASS (parser str vẫn bác BOM)
  ca thu_tu_k1: FAIL, ['decode','parse'] != ['slice','decode','parse']
  disposition: witness_killed
```

**Phán xử:** oracle thứ tự đúng với M2(a) và có răng hơn phép đo verdict cũ. Nhưng không thể gọi disposition hiện tại là “đúng spec vì chặt hơn”: A2 ghi tường minh mutant bỏ riêng chốt BOM là `equivalent_verified`, **không được đếm đã giết**. Hai mệnh đề trong spec dùng hai cấp quan sát khác nhau; dưới toàn bộ M2, mutant thực tế không tương đương. Executor đã tự giải xung đột bằng cách đổi disposition và số tổng (+1 killed, −1 equivalent) khi spec vẫn đóng băng.

Đề xuất: giữ cả phép đo BOM lẫn thứ tự, đem xung đột A2–M2 tới checkpoint để chủ kho phân định phạm vi equivalence hoặc revision có thẩm quyền. Nếu tách hai ID/cấp quan sát, nhãn phải nói rõ đang tương đương về verdict hay về toàn hành vi. Rủi ro vá: đừng ép `equivalent_verified` cho toàn M2 trái bằng chứng, cũng đừng bỏ spy hợp lệ chỉ để khớp số đếm cũ. Đây là lệch hợp đồng có hậu quả thống kê, không phải lỗi runtime của kiểm BOM hiện tại.

## Audit A0

Đếm được **115 ID duy nhất** = 84 hàng DB + 31 hàng `_theo_truong()`. Disposition do suite in là **109 witness / 6 equivalent / 0 unresolved**. Đây là số chương trình tự phân hạng, **không phải 115 nghĩa vụ đã được reviewer chấp nhận**: F15/F16 bác tính đúng của phân hạng, F17–F22 chứng minh thiếu độ phân biệt, F24 chưa giải quyết disposition.

Đối chiếu dưới đây bắt đầu từ văn bản M1–M6/M8, không suy ngược từ số ca đang có:

| Mệnh đề nguồn | ID / oracle hiện có | Kết quả audit độc lập |
|---|---|---|
| M1 hàm thuần; không process/git/mạng | M1s, `tinh` | Import tĩnh có ID; hành vi purity chưa được đo đúng, F20. |
| M1 trả dict, đúng cấu trúc ba khoá | `ca()` dòng 71 kiểm; M1r ở CLI | Oracle hiện có kiểm shape API, nhưng không có ID/mutant riêng cho dạng dict/đủ ba khoá ở API. Không lấy ca bool M1o thay toàn nghĩa vụ shape. |
| M1 `ok` bool và mọi luật qua | M1o/M1a | API bool/all→any có răng; M1o không đạt A1 (F16); CLI bool lọt (F17). |
| M1 năm trạng thái, không dừng sớm | M1b/M1c, vectơ trong `ca()` | Các mutant cũ bị đúng ca đích giết; phối hợp K3+K4 có đo. |
| M1 lý do list[str], K1 lan có lý do K1 đỏ | M1d/M1p/M1q | Kiểu list[str] và có dòng được giữ; lý do sai nghĩa vẫn xanh, F22. |
| M1 CLI một dòng, đúng dict | M1n/M1r | Một dòng và mất khoá được bắt; kiểu bool và parity receipt đỏ thiếu, F17/F18. |
| M1 rc 0/12/2, OSError, tham số sai | M1e–m, `ca_cli` | Rc đọc trực tiếp. Rỗng/39/41/hoa/nonhex kiểm thêm đều rc 2; `--kho` thiếu có ca. Lỗi parser thật làm rc 1, F23. |
| M1 không quyền land, không chứng minh provenance | M1t, `tinh`, docstring sản phẩm | Lời khai hiện đúng; `tinh` kiểm cả hai câu, nhưng ID M1t chỉ mô tả/mutate câu quyền land. Giới hạn caller có khai ở docstring; không chứng minh nguồn caller trong lát này. |
| M2(a) BOM đỏ / trước decode | M2a/M2a′, M2h, spy | Cả verdict và thứ tự có răng; disposition M2a trái A2, F24. |
| M2(b) UTF-8 strict, decode một lần, lỗi decode đỏ | M2b/M2b′/M2h | Byte 0x80 và thứ tự đo được. Phân hạng exception vẫn có F15. |
| M2(c) parser nhận chính str, không bytes, JSON lỗi đỏ | M2c/M2c′, spy | Bốn UTF-16/32 đi qua decode strict rồi parser str bác; loads(bytes) bị bắt. Chính str sau decode thiếu ID phân biệt riêng, mutant chuẩn hoá sống, F21. |
| M2(d) root dict | M2d | Null/list được bác trên HEAD; tín dụng exception có F15. |
| M2(e) đúng 38 khoá | M2e/M2e′, 38 ca thiếu | Fixture/38 khoá khớp receipt; thiếu từng khoá/thừa có ca; F15 còn ở classifier. |
| M2(f)(g) schema int-không-bool, ==1, event hằng | M2f/M2f′/M2g | Ca True/2/event_v2 có răng; schema K2 bị K1 che được khai đúng. |
| M3 hex40: str, alphabet, case, độ dài, toàn chuỗi; nullable oid | M3a/b/g/n/o/s/t/u, ID từng trường | Các biểu hiện F3/F14 đóng; bổ sung 39/41 và g có răng; nullable oid có ca riêng. |
| M3 hex64 và descriptor nullable | M3e/h/p/q/r/w, ID từng trường | 63/65/alphabet có răng. M3w null dùng mutant làm fixture đỏ, F16. |
| M3 int-không-bool, job_id không null | M3c/d/v, ID từng trường | Bool/float/null có ca; runtime miền int chưa đủ, F23. |
| M3 timestamp toàn mẫu `\d...` | M3f/f2–f6, M3.thoi_diem_utc | T/dấu/Z/Unicode được đo, còn năm dư và chữ số/độ rộng các nhóm, F19. |
| M3 policy/profile null hoặc dict/str; discovery str | M3i/j/x/y, ID theo trường | Vế dict/str có ca; hai vế null vi phạm A1, F16. Discovery sai miền được bắt. |
| M3 ba dict và hai list | ID `M3.so_thu_hoi_S/T`, `M3.ngan_sach`, `M3.metadata_T`, `M3.thu_hoi_moi` | Bỏ predicate từng trường giết đúng ca; chỉ kiểm kiểu, không thêm diễn giải nội dung ngoài spec. |
| M3 C đồng nhất/đúng kiểu, C≠S vẫn dương | M3k/l/m/n; ba TD C | Loại mỗi trường khỏi đồng nhất, bỏ kiểu cả nhóm, ca nhóm 39 và nhóm dương khác S đều có răng. Sáu TD kiểm riêng bên dưới. |
| M4 nguồn caller kho/nhánh và bốn phép bằng | M4a–f/j/k | Ca nhóm âm, caller đổi cùng nhóm dương và mutant ghim đều phân biệt đúng. |
| M4 hằng host/đường workflow/ref heads | M4g–i | Đo lại từng mutant và ca đích; đều thất bại đúng assertion. |
| M5 S/base, H/head; nguồn caller; stale báo chạy lại | M5a–d | Bỏ từng vế/lấy từ receipt bị bắt; lời lý do hiện có `stale, chay lai`, chưa có ID/mutant riêng cho nghĩa thông báo stale. |
| M6 rc=0, kết luận tập đóng, chế độ hằng | M6a–d | Các mutant bỏ vế được bắt; JSON sai kiểu kết luận không còn ném trên API. CLI không bảo vệ mọi đầu vào đỏ, F18. |
| M8 đăng ký và hai cặp bằng nhau >0 | M8a/b, `ca_dang_ky` | Đo bằng **chay_moi hiện tại sau #661**: dương rc 0; năm dòng lệch/0 rc 1; bỏ đăng ký báo lỗi; cả hai backreference có răng. Đăng ký và >0 được assertion trực tiếp kiểm, không có ID riêng ngoài M8a/b. A0 bắt ID M1–M6; không tự mở rộng quy tắc đó thành finding riêng cho M8. |

Các chỗ thiếu ID hình dạng API/câu provenance/thông báo stale được ghi rõ; không coi việc oracle tình cờ kiểm chúng là đã hoàn tất phân rã A0. Những thiếu sót này cùng cơ chế `dot-bien-tuong-duong-hoac-thieu`; chúng không được dùng để tăng riêng số finding bên trên. Audit A0 **failed** dù `unresolved` chương trình in bằng 0.

**Sáu dòng TD còn lại:** chạy `python3 -B /tmp/review650-r2/probe_new.py "$PWD" td` (rc 0), mỗi mutant chạy cả bộ ca, thêm phản chứng tại ranh giới; log `new-td.jsonl`.

| ID | Đo bổ sung | Kết luận |
|---|---|---|
| M1j | Bỏ riêng kiểm base không rỗng; CLI base rỗng vẫn rc 2 ở hex40 | `equivalent_verified` đúng |
| M1k | Tương tự head rỗng vẫn rc 2 | `equivalent_verified` đúng |
| M3.schema_version | True, 1.0, 2, null đều K1 đỏ trước K2 | `equivalent_verified` đúng |
| M3.checkout_commit | Bỏ kiểu riêng; đơn trường/cả nhóm null, số, 39 ký tự vẫn K2 đỏ | `equivalent_verified` đúng |
| M3.bo_kiem_da_chay_commit | Cùng phép đo, hai chốt kiểu còn lại + đồng nhất còn chặn | `equivalent_verified` đúng |
| M3.workflow_definition_commit | Cùng phép đo | `equivalent_verified` đúng |

Không cộng ba phép bỏ riêng C để suy bỏ cả nhóm tương đương. M3n trên nhóm 39 ký tự vẫn bị giết. Không tìm được TD sai trong sáu hàng này. M2a đã ra khỏi TD, được xử riêng ở F24.

**Kiểm bản vá có gây lỗ mới:** spy `m.json.loads` tạm sửa đúng module `json` dùng chung, nhưng phép đo thành công **và thất bại** đều phục hồi đúng object gốc (`restored=True`). Không có bằng chứng rò spy sau ca trên đường đã chạy. Control parser alias hợp lệ làm spy đỏ vì không thấy `parse`; đây là giới hạn phụ thuộc cách cài đặt, không được tính là một mutant vi phạm spec. Chuẩn hoá `raw=bytes(raw)` cũng làm spy mất sự kiện và suite đỏ; không tính sống. Thử thay lý do sau `ly_do.extend` đầu tiên làm mutant M1p ném TypeError vô can và suite rc 1; đã loại phép thử ấy, dùng bản trước extend ở F22 để giữ nguyên toàn bộ meta-test. Không có phép thử dựng nội dung đường dẫn thoát cây.

## Master drift, phạm vi và bằng chứng

`python3 -B /tmp/review650-r2/run_checks.py "$PWD" producer`, rc 0, dùng AST xác định đúng dict chứa event `thu_hoi_admission_receipt`, rồi so **bytes nguyên khối dòng**, không chỉ so AST:

```text
5618f61c6ac2fa14aab52b0f5ce3d065aee8e022: dòng 1877–1891, 1121 bytes
ceb1a3f36912dd4f03fe1741c443cd09e82a44ee: dòng 2036–2050, 1121 bytes
8378f331aff651e32496b02589d674239fbd92f7: dòng 2036–2050, 1121 bytes
sha256 cả ba: 557d5f2298cda80e5dae35679e9eea4af71a7a978084ba7d50f62f6a7ea40d82
receipt_blocks_byte_equal=True
```

Khối có 24 khoá; workflow bổ sung không đổi qua drift (`git diff` workflow giữa base lượt 1 và base hiện tại rỗng). Phép đo này chứng minh **khối dựng dict** không đổi, không tuyên bố toàn `lease_publish.py` hay mọi hành vi producer không đổi. File `lease_publish.py` thực sự có diff #589 ngoài khối ấy. Receipt mẫu băm `ca67dc6a817b7cf8643616e4762d5f3e95c0ec7a46cf9693f9436b47c00f5960`; fixture bằng đúng toàn bộ giá trị và kiểu, đủ 38 khoá.

Diff registry so base hiện tại chỉ thêm đúng một dòng `MOI`, giữ nguyên `bang_chung_xanh` và consumer của #661. Consumer thật với riêng suite này nhận rc 0. Không chạy `--chay` toàn registry vì đó gọi thêm các suite ngoài phép đo được cấp; A13 mới đo được phạm vi consumer của suite này, không khai toàn CI.

A14: ba tệp sản phẩm **+1 +111 +367 = +479/−0**. Đây là **ngoại lệ có phạm vi ≤500** theo dữ kiện authority người dùng cung cấp ở lease `c1a1a-exec-2-claude-20260927.yaml` trên nhánh `ops/cap-lease-650`; không gọi là đạt trần gốc 300 hay trần 400 trong spec. Spec mang theo và hiện vật review không tính theo chỉ thị. Không lấy lease vắng trong checkout làm finding.

## Đã chạy

`run_checks.py` lưu stdout/stderr và rc từng lệnh trong `checks.jsonl`; không suy rc từ pipe. Các mode probe ghi rc tiến trình con trong JSONL hoặc log riêng.

| Lệnh | Rc / bằng chứng dương | Trạng thái |
|---|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master` đầu/cuối | 0; đúng ba OID đầu báo cáo | passed |
| `sha256sum` spec và receipt; băm lại bằng Python cuối lượt | 0; khớp cả hai băm chỉ thị | passed |
| `python3 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; 128/128 ca, 109/109 mutant; 109/6/0 | passed với giới hạn A0 nêu trên |
| `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 -B .claude/dev/ci_dang_ky_test.py` | 0; đăng ký 22/22, launcher contract 4/4, Ruff contract 3/3, **938/938 phản chứng**, `TỔNG: ĐẠT` | passed |
| `python3 -m ruff check --no-cache --select F .claude/dev/doc_receipt_thu_hoi.py .claude/dev/doc_receipt_thu_hoi_test.py .claude/dev/ci_dang_ky_test.py` | 0; `All checks passed!` | passed |
| Ruff F trên bytes registry `origin/master`, qua `--stdin-filename` và `-` | 0; `All checks passed!`; hai file mới 0 lỗi ⇒ **delta F=0** | passed |
| `python3 -m ruff check --no-cache --select F --output-format json --stdin-filename <checkout>/scripts/tl.py -`, stdin từ `git show HEAD:scripts/tl.py` rồi `origin/master:scripts/tl.py` | Cả hai **rc 1**, cùng **12 F821**, diagnostics bằng nhau ⇒ **delta F=0** | lint failed sẵn ở nền; tiêu chí delta passed |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; 10 tệp, 0 chỗ chép doctrine | passed |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0; 50 ADR/50 dòng khớp 1–1 | passed |
| `git diff --numstat origin/master..HEAD` | 0; sản phẩm +479/−0; toàn output ở `numstat.stdout` | passed theo ngoại lệ ≤500 |
| `git diff --check origin/master..HEAD` | 0; không lỗi whitespace | passed |
| `probe650.py "$PWD" actual / credit / mutants / extra / caller / targeted / registry` (mỗi mode một lệnh) | Mỗi rc 0; 11 mutant sống cũ nay có assertion đích đỏ; CLI/API và consumer có log riêng | đo xong |
| `probe_new.py "$PWD" credit / td / oracle / mutants / followup` | Mỗi rc 0; 3 tín dụng giả, 4 vi phạm A1, 6 TD hợp lệ, 9 suite mutant sống, lỗi runtime F23 | failed cho các nghĩa vụ tương ứng |
| `python3 -B /tmp/review650-r2/run_checks.py "$PWD" producer` | 0; khối receipt 3/3 byte-equal | passed |
| Snapshot bytes đầu/cuối bằng `run_checks.py` | 0; **2291/2291 tệp quan sát không đổi**, diff/index rỗng, status giữ nguyên chỉ `.codex/` ignored | passed |

Không có check `skipped` nào được tính pass. CI remote/full CI/Windows và `ci_dang_ky_test.py --chay` toàn registry: **not_run**. Không chạy cài dependency, fetch, API, commit/push/merge/deploy hay gọi mạng. Registry chỉ tạo commit trong fixture tạm do test sở hữu; đã tắt signer cho tiến trình test theo chỉ thị, không đổi Git config checkout.

Môi trường đo: Linux, Python **3.11.15**, Ruff **0.16.9**, `codex-cli 0.157.1`. Ruff pin/probe contract là 3/3 của registry; bare lint được đo riêng bằng Ruff đang có, không giả khai đã chạy bản pin khác. `codex --version` rc 0 kèm cảnh báo không tạo được PATH aliases vì filesystem read-only; không sửa quyền hay lách cảnh báo. Checkout detached HEAD, origin là mirror local `/home/user/tra-luat`, `core.abbrev=7`. Không xác minh remote GitHub, lease/generation live, lịch sử vận chuyển verdict hoặc model/effort bằng log launcher trong phạm vi offline; chúng là **not_measured**, không được nâng assurance. Cặp executor–reviewer khai theo assignment; không lấy actor GitHub làm model identity. Sandbox thực tế workspace-write; sự bất biến checkout được đo bằng snapshot, không khai có cưỡng chế read-only toàn cây. Phạm vi snapshot là checkout được giao, không gồm repo nguồn mirror.

## Lịch sử lớp và stop condition

| Slug lớp giữ nguyên | Finding còn mở lượt này | Mức cao nhất | Đóng lớp bằng gì |
|---|---|---|---|
| `tin-dung-gia` | F2 → F15; F16 | P1 | Classifier từ chối lỗi vô can đúng loại/mảnh dòng; A1 được kiểm độc lập, không miễn theo tên ca. |
| `dot-bien-tuong-duong-hoac-thieu` | F17–F22; các ID thiếu ghi trong A0 | P1 | Đối chiếu ngược M1–M6 đầy đủ; từng mutant sống đổi màu đúng ca, không đỏ do setup/mỏ neo/ngoại lệ vô can. |
| `lech-dac-ta` | F23/F24 | P1 | Biên parser có kết quả đúng hợp đồng; quyết định bền giải xung đột A2–M2 và disposition. |

Ba lớp đã có ở lượt 1 vẫn còn mở; **0/3 lớp được đóng hoàn toàn**, dù 13/14 biểu hiện cũ đã vá. Không đổi slug để reset lịch sử. Lớp độ phủ đã lặp từ các lượt đặc tả và cả hai lượt thi công.

Đây là **lượt cuối 2/2**. Theo protocol §8/§12, chuyển **Review Rescue Checkpoint / human audit của chủ kho** với các hiện vật này; không gọi lượt model thứ ba, không đổi tên packet để reset trần. Reviewer không sửa branch, không cấp lease và không tự quyết revision/land. Tệp verdict này là đầu ra offline để bên điều phối vận chuyển bằng receipt riêng.
