verdict: approve
reviewed_sha: ab2842378652cf03c1d5964c927abb2391f2834f
reviewed_tree: 0de09eee4329870875ab19b6aa2a60b7a5cf69f0
base_sha: 4581cfa5124ef803bfda10ce4de499b0ed31380e
previous_reviewed_sha: 52e1f0b69d90247c6b7c90730b81ff8af3de3cba

Hai finding lượt 1 **ĐÃ VÁ THẬT**. Không còn P0/P1/P2 trong phạm vi đã đo; còn một P3 lexical bên dưới,
không ảnh hưởng biểu thức workflow hiện tại. Áp ngưỡng của prompt: approve mã khi không còn P0/P1/P2.
**N4: KHÔNG ĐO ĐƯỢC offline**, tách khỏi verdict mã. Không khẳng định CI GitHub xanh hoặc đủ điều kiện merge/land.

Reviewer độc lập: OpenAI Codex; provider `openai_codex`, execution_surface `codex_cli`, transport `machine`,
run `53e0afe6c13040eaae397872429ef80a`, session `01a16497-b30a-7371-9a4c-03f26139713e`.
[Header đúng run](evidence/reviewer-header.txt) công bố Codex CLI 0.163.0, `gpt-6.1-sol`, effort `xhigh`;
header không chứng minh model/effort của mọi request. [Metadata launcher](runs/53e0afe6/run.json).
Không mạng, không đăng GitHub; checkout `cay-kho/` được đối xử read-only. Mutation/thử sửa chỉ trên archive tạm.
Sandbox thực tế là workspace-write, không tự khai checkout được hệ điều hành khóa ghi.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: [VERDICT-luot1.md](VERDICT-luot1.md), exact SHA `52e1f0b69d90247c6b7c90730b81ff8af3de3cba`.

| Finding / lớp | Kết luận | Phép đo độc lập trên head mới |
|---|---|---|
| evaluator-splits-quoted-operators [P2] | **ĐÃ VÁ THẬT — ĐÓNG** | Giữ nguyên script lượt 1, chỉ đổi head SHA: 258 biểu thức × 36 context = 9.288 cặp nền nhận; **equal=9288, new_rejects=0, new_changes=0**, so với 6.264 cặp bị từ chối sai lượt 1. Ref/label chứa `&&` tính đúng cả khớp/không khớp; `\|\|` trong ref/label nay nhận đúng. Actionlint các ca literal rc=0. |
| evaluator-accepts-numeric-property [P3] | **ĐÃ VÁ THẬT — ĐÓNG** | `inputs.123` bị từ chối với ValueError/`KHÔNG ĐO ĐƯỢC`, actionlint rc=1 (INTEGER thay IDENT). `inputs.runner-set` nhận: khớp ⇒ hai nền, không khớp/vắng ⇒ Ubuntu; actionlint rc=0. `_runner`, `runner_1` cũng đúng. Mở rộng 99 tên: parser/model đồng ý 99/99. |

Lệnh đã chạy, rc=0:

```sh
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/evaluator.py > evidence/evaluator.log 2>&1
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/edges.py > evidence/edges.log 2>&1
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/hunts.py > evidence/hunts.log 2>&1
```

[Log đối chiếu đúng phép đo cũ](evidence/evaluator.log), [biên/identifier đầy đủ](evidence/edges.log),
[bản ngắn](evidence/edges-summary.log), [bộ săn sinh](evidence/hunts.log).
`EXACT_ROUND1_SCRIPT_EXCEPT_HEAD True` được kiểm bằng so nội dung script trong [summary.log](evidence/summary.log).
Biểu thức YAML nền thật, A3-ref và fromJSON: mỗi loại **36/36** cặp giữ kết quả cũ.

Đối với phần nền từng từ chối: bộ sinh hợp lệ mới có **47.808** cặp nền từ chối nhưng head nhận đúng theo cây oracle;
ngoặc nhóm/escaped quote ngoài grammar tối giản tiếp tục bị từ chối; atom lạ/nhánh rỗng ẩn sau vế đúng vẫn bị từ chối.
Không tuyên bố mọi biểu thức nền từ chối đều an toàn: phép săn whitespace tìm được một ngoại lệ lexical P3,
được ghi riêng bên dưới, thay vì che bằng tổng 9.288/9.288.

## BẢNG ĐO

### Toàn vẹn, phạm vi và môi trường

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/scope.py > evidence/scope.log 2>&1`, rc=0:

- HEAD/tree khớp snapshot; status đầu và cuối không có thay đổi. `SPEC.md` SHA-256
  `13abe7208cb50f08013937c4db9cb434d44dcb9dcd81c6920bb98fe017620124`, đúng LEASE.
- `git diff --numstat 52e1f0b ab28423`: **55 insertions, 2 deletions, chỉ `ops/lease_publish_test.py`**.
  Bốn tệp packet còn lại byte-exact với lượt 1.
- `PACKET_DIFF_EXACT True`, `PACKET_NUMSTAT_EXACT True`: diff toàn packet và numstat khớp hiện vật giao.
  Đúng năm đường dẫn write set; `git diff --check <base> <head>` rc=0.
- So AST lượt 1/head: chỉ hai hàm đổi là `_danh_gia_bieu_thuc_chuan_bi` và `t162_M4_evaluator_toi_gian_chuan_bi`.
  Bỏ hai hàm ấy, AST toàn module bằng nhau. Do đó các phần khác của bảng lượt 1 không có thay đổi mã;
  kết quả chưa chạy lại vẫn được phân biệt với phép đo mới.
- Python **3.13.16**; actionlint **1.7.7**, Go 1.23.4/linux-amd64; Ruff **0.16.9** (khác pin CI 0.15.15).
  **Không có shellcheck trên PATH.** Không cài thêm, không dùng mạng.
- Hai clone A/B đều `core.abbrev=7`; Git global config bị cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null`
  để fixture không kế thừa ký commit của máy. Không đổi Git config của checkout review.

[scope.log](evidence/scope.log), [summary.log](evidence/summary.log).
Hai lần quan sát nội dung **4.897 tệp tracked** cho hash bằng nhau; status cuối gồm untracked/ignored rỗng,
HEAD/tree giữ nguyên. Đây là so trạng thái quan sát, không phải audit mọi syscall ghi trong lịch sử run.

### Tái lập head/nền trong một lệnh

Lệnh driver đã chạy đến hết, rc=0; rc từng suite được lưu riêng, không bị driver rc che:

```sh
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/ab.py > evidence/ab-driver.log 2>&1
```

Driver tạo clone local exact base/head, ghim `core.abbrev=7`, truyền cùng env/config và lần lượt chạy mỗi phía:

```sh
python3 .claude/dev/ci_dang_ky_test.py
python3 ops/ci_duong_nhanh_test.py
actionlint -no-color
ruff check --no-cache --select F scripts/tl.py ops/lease_publish_test.py ops/ci_duong_nhanh_test.py .claude/dev/ci_dang_ky_test.py
python3 .claude/dev/packet_loop.py doctrine-scan --root .
# Thêm trên head:
python3 ops/lease_publish_test.py --chi-ca=t16
```

| Phép đo | Lời khai cần đối chiếu | Nền đo mới | Head đo mới | Kết luận |
|---|---|---|---|---|
| Registry mặc định, không `--chay` | 1053 → 1056 | [1053/1053 đỏ đúng; rc=0](evidence/base-0.log) | [1056/1056 đỏ đúng; rc=0](evidence/head-0.log) | **Khớp** |
| Fast-path | 104/104; 383/383 cả hai | [103/104 đạt, 0 đỏ, 1 hỏng; 378/383 mutant bị giết; rc=1](evidence/base-1.log) | [103/104 đạt, 0 đỏ, 1 hỏng; 378/383 mutant bị giết; rc=1](evidence/head-1.log) | **KHÔNG ĐO ĐƯỢC đủ** do fixture socket; delta quan sát 0 |
| Lease publish t16 | Head 9/9 | Không yêu cầu | [9/9 đạt; đã chạy=9, bỏ qua=0; rc=0](evidence/head-5.log) | **Khớp**, có `t162` |
| actionlint | Không thêm finding | [0 finding; rc=0](evidence/base-2.log) | [0 finding; rc=0](evidence/head-2.log) | Delta 0; thiếu shellcheck |
| Bare Ruff F | Delta 0 | [21 finding; rc=1](evidence/base-3.log) | [21 finding; rc=1](evidence/head-3.log) | Multiset `(file tương đối, code, message)` bằng nhau, không chỉ số lượng |
| Doctrine scan | rc=0 | [10 tệp, 0 chỗ chép; rc=0](evidence/base-4.log) | [10 tệp, 0 chỗ chép; rc=0](evidence/head-4.log) | Khớp |
| Lease toàn 267 ca | Bảng lượt 1: 265/267 cả hai | **not_run** lượt này | **not_run** lượt này | Không đổi ngoài evaluator/t162 theo AST; không biến số cũ thành phép đo mới |

[ab.json: exact SHA, lệnh, rc, thời lượng](evidence/ab.json), [driver log](evidence/ab-driver.log).
Fast-path hai phía cùng hỏng tại `t20zo_la_khong_phai_tep_thuong_do`: `socket.bind` ném
`PermissionError: [Errno 1] Operation not permitted`. Năm mutant của ca ấy không có baseline xanh;
không gọi 378/383 là 383/383 và không coi đây là hồi quy packet. Không nới quyền hoặc thay socket bằng đồ giả.
Hai ca lease đỏ ở lượt 1 cần shellcheck; chưa tái đo chúng lượt này.

Bare lint: cả hai **7 F401 + 2 F541 + 12 F821 = 21**; [JSON nền](evidence/ruff-base.json),
[JSON head](evidence/ruff-head.json), `RUFF_NORMALIZED_DELTA {} {} equal=True` trong [summary.log](evidence/summary.log).
Ruff pin/probe contract của registry và bare lint thật là hai phép khác nhau; không ghi “Ruff xanh”.

### N2 trên chính expression YAML head

Expression được đọc từ Git object `.github/workflows/ci.yml`, không chép lại trong oracle.
[evaluator.log](evidence/evaluator.log), lệnh ở mục đối chiếu:

| Event | runner_set / label | Mảng model trả |
|---|---|---|
| workflow_dispatch | windows-only | `["windows-latest"]` |
| workflow_dispatch | windows-and-ubuntu | `["ubuntu-latest","windows-latest"]` |
| workflow_dispatch | vắng trong ctx.inputs | `["ubuntu-latest","windows-latest"]` |
| pull_request | không nhãn windows | `["ubuntu-latest"]` |
| pull_request | nhãn windows | `["ubuntu-latest","windows-latest"]` |
| push master | không input | `["ubuntu-latest"]` |

Đây là bảng **model**, không là bằng chứng service hydrate default/inputs ra sao.
N1, N3, DAG/dataflow, các ghim YAML và câu CLAUDE.md không đổi với lượt 1 theo diff; registry mới cũng xanh.

### Bộ tách mới: cú pháp biên và fail-close

Cùng lệnh `python3 evidence/edges.py` với bytecode off/Git config cô lập ở trên, rc=0;
[output đầy đủ](evidence/edges.log), [tóm tắt từng ca](evidence/edges-summary.log):

| Hướng / ca thực tế | Output thật | Đánh giá |
|---|---|---|
| Literal `''`: ref `refs/heads/it''s&&x`, label `win''\|\|dows` | Head ValueError/`KHÔNG ĐO ĐƯỢC`; actionlint rc=0; nền/lượt 1 cũng từ chối | Grammar atom chưa hỗ trợ escaped quote; **không phải hồi quy**. Scanner không biến nó thành kết quả sai |
| Ngoặc nhóm lồng: `contains((github.event.pull_request.labels.*.name), 'windows')`, `(github.event_name == 'push')` | Cả ba evaluator ValueError; actionlint rc=0 | Giới hạn tối giản có sẵn; không khai hỗ trợ toàn ngữ pháp Actions |
| Ngoặc trong literal `a&&b\|\|((x))` | Nhận và trả đúng; actionlint rc=0 | Không đếm ngoặc/toán tử trong literal |
| Toán tử sát ngoặc: `contains(...,'a&&b')&&github.ref=='x'\|\|github.event_name=='push'` | Head hai nền đúng; actionlint rc=0 | Tách được toán tử thật sau dấu `)` |
| Nhánh AND/OR rỗng ở đầu, cuối, giữa | Sáu ca head ValueError; actionlint rc=1 | Không lọt nhánh rỗng, kể cả khi vế trước đúng |
| Ngoặc thừa mở, thừa đóng, đảo `)(` | Head ValueError; actionlint rc=1 | Depth cuối không bắt riêng `)(`, atom regex vẫn bắt |
| Literal không đóng `github.ref == 'x` | Head ValueError, thông báo `literal/ngoặc không cân`; actionlint rc=1 | Fail-close |
| Whitespace TAB/CR/LF | `guard_probe`: nhận và tính đúng; actionlint rc=0 | Hợp lệ |
| Whitespace VT/FF/NBSP/EM SPACE ngoài literal | Model nhận, actionlint rc=1; ca đơn nền/lượt 1 cũng nhận | **LỖI lexical P3**; ca mới có literal `\|\|` trước bị từ chối nay bị nhận sai |
| `always()`/`fromJSON(...)` sau OR đúng hoặc AND sai, atom ở nhánh sau nhánh đầu đúng | Tất cả ValueError/`KHÔNG ĐO ĐƯỢC` | Không short-circuit qua kiểm atom |
| Mảng JSON hỏng ở nhánh sau hoặc fallback dù nhánh đầu đúng | Hai ca ValueError trước trả kết quả | Validate cả mảng không được chọn |

## BẢNG ĐỘT BIẾN

```sh
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/mutations.py > evidence/mutations-driver.log 2>&1
```

Driver dùng **`mktemp -d` + `git -C cay-kho archive ab2842378652cf03c1d5964c927abb2391f2834f`**,
giải nén từng mutant riêng, bytecode off, `core.abbrev=7` qua config env. Mỗi bản chạy đúng:

```sh
python3 ops/lease_publish_test.py --chi-ca=t162
```

| Bản | Output thật | Kết luận |
|---|---|---|
| Control head không sửa | [1/1 đạt; rc=0](evidence/mutation-control.log) | Ca nền xanh |
| (a) Đổi hai `_tach` thành `split` thô | [0/1; rc=1](evidence/mutation-a-raw-split.log), `evaluator phải NHẬN và tính đúng (ref chứa &&): ValueError...` | **CHẾT đúng lý do** |
| (b) Nới regex tên input về `\w+` | [0/1; rc=1](evidence/mutation-b-input-word-regex.log), `evaluator phải NHẬN và tính đúng (input có gạch nối): ValueError...` | **CHẾT đúng lý do**; chính mutant yêu cầu bị ca hyphen giết trước khi đến ca numeric |
| (c) Bỏ `if trong_nhay or sau: _khong_do_duoc(...)` | [1/1 đạt; rc=0](evidence/mutation-c-remove-balance-guard.log) | **SỐNG**; không khai 3/3 chết |

[Driver đầy đủ](evidence/mutations-driver.log), [JSON](evidence/mutations.json),
[các diff mutant](evidence/mutations.OeLjIL/).

Giải thích mutant (c), đã đo thêm:

```sh
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/guard_probe.py > evidence/guard_probe.log 2>&1
```

Head bắt `github.ref=='a` bằng thông báo `literal/ngoặc không cân`; mutant vẫn ValueError qua `_nguyen_tu` với
thông báo `vế điều kiện không nằm trong tập tối giản hỗ trợ`. `t162` chỉ đòi nhãn chung `KHÔNG ĐO ĐƯỢC` nên vẫn xanh.
10.149 điều kiện (sửa một ký tự quanh bốn atom + mọi chuỗi dài 0–5 trên alphabet `'()&|x`) × hai context =
**20.298 cặp: acceptance/result bằng nhau 20.298, different=0; 15.596 cặp đổi thông báo**.
[guard_probe.log](evidence/guard_probe.log). Đây là mẫu hữu hạn, không là chứng minh tương đương mọi input.

Ca khóa không có răng **riêng cho chẩn đoán của guard**; chốt fail-close còn được atom validator bảo vệ.
Không nâng thành P2 vì chưa có input bị mutant nhận sai trong phép đo và guard vẫn hiện diện trên head.
Muốn chốt chính nhánh guard thì thêm ca đòi thông báo đặc hiệu cho nháy/ngoặc thừa thiếu hoặc đo splitter riêng;
không cần buộc mọi mutant tương đương về acceptance phải chết bằng một khẳng định acceptance chung.

## BẢNG SĂN

Các hướng mới dành riêng commit sửa; output thật trong [hunts.log](evidence/hunts.log), rc=0:

```sh
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/hunts.py > evidence/hunts.log 2>&1
```

| Hướng độc lập / giả thuyết | Phép thử và output thật | Kết luận |
|---|---|---|
| H1 — Bảo toàn literal và ưu tiên/nhánh: splitter có thể tính sai khi quoted AND/OR, ngoặc trong literal xen toán tử thật | Generator giữ cây riêng, expected tính trực tiếp từ atom/context, không parse bằng helper review. `HUNT1_TYPED_TREE`: 2.184 expressions, 52.416 pairs, `head_rejects=0`, `head_wrong=0`; 47.808 cặp nền từ chối và 51.408 cặp lượt 1 từ chối nay nhận đúng. `HUNT1_MULTI_BRANCH`: 300 expressions, 7.200 pairs, `rejects=0`, `wrong=0` | **KHÔNG PHẢI LỖI** trong grammar/cây đã sinh |
| H2 — Eager validation: unsupported atom có thể trốn sau vế đúng, AND sai hoặc nhánh không chọn | Context độc ném RuntimeError ngay khi `.get()` bị gọi; 56 biểu thức chứa atom lạ/nhánh rỗng/nháy thiếu/mảng hỏng. `HUNT2_EAGER_FAILCLOSE`: `rejected_before_context=56`, `accepted=0`, `read_context=0`, `other=0` | **KHÔNG PHẢI LỖI** — validation trước mọi lần đọc context trong mẫu |
| H3 — Lexical tên input: regex mới có thể từ chối tên hợp lệ hoặc nhận chữ số/Unicode/hyphen sai vị trí | 99 tên, có tích Descartes `a,_ ,1,-` dài 1–3 và biên Unicode/dấu chấm/space. Actionlint đối chứng từng tên; `HUNT3_IDENTIFIER_DIFFERENTIAL`: `agree=99`, `mismatch=0`, 46 tên nhận đúng cả match/miss/absent | **KHÔNG PHẢI LỖI** trong mẫu tên |
| H4 — Mở rộng miền giao với whitespace: việc giữ literal OR có thể cho cú pháp Actions sai đi qua `\s` | `python3 evidence/guard_probe.py` cùng env ở trên: VT/FF/NBSP/EM SPACE ngoài literal + ref `x\|\|y`: base/lượt 1 ValueError, head OK/hai nền, actionlint rc=1; space/TAB/CR/LF actionlint rc=0 | **LỖI P3** lexical bên dưới; không ảnh hưởng YAML hiện tại |
| H5 — Mutant guard sống có thật sự mở fail-close hay chỉ đổi đường báo lỗi? | Cùng lệnh `guard_probe.py`: 20.298/20.298 cặp giữ acceptance/result, 15.596 đổi diagnostic; ca ngoặc đảo vẫn bị atom regex từ chối | **KHÔNG PHẢI LỖI hành vi đã đo**; thiếu khóa riêng cho diagnostic đã được ghi rõ |

Các oracle hữu hạn dùng đúng kiểu context của helper; không thay engine Actions thật, không kiểm đầy đủ case folding,
truthiness hay default hydration của dịch vụ. Actionlint ở đây là parser/typechecker đối chứng, không chạy expression.

## BẢNG LỚP

| Slug | Nguồn / biểu hiện | Mức cao nhất còn mở | Quyết định |
|---|---|---|---|
| evaluator-splits-quoted-operators | Lượt 1 SHA 52e1f0b: ref/label chứa AND/OR | Không còn | ĐÓNG; 9.288 cặp + ca mới + mutant split chết |
| evaluator-accepts-numeric-property | Lượt 1 SHA 52e1f0b: numeric đầu / hyphen hợp lệ | Không còn | ĐÓNG; numeric/hyphen đối chứng + 99 tên + mutant regex chết |
| evaluator-accepts-non-actions-whitespace | Lượt 2 SHA ab28423: VT/FF/NBSP/EM SPACE ngoài literal trong miền newly accepted | P3 | Nợ có tên, owner executor wp878; chấp nhận không chặn approval mã, hướng xử lý dưới đây |

Hai lớp cũ đóng; một lớp lexical bổ sung, bốn ký tự đại diện cùng cơ chế. Không gộp P3 whitespace vào lớp split literal:
split nay giữ literal đúng; root cause lexical là `\s`/`strip` rộng hơn lexer Actions. Mutant guard sống là quan sát về
độ phủ ca khóa, không chứng minh thêm lớp bug hành vi.

### evaluator-accepts-non-actions-whitespace  [P3]

**TỆP/DÒNG:** `ops/lease_publish_test.py:7917` (miền nhận mới đi vào atom regex), liên quan `:7884`, `:7890`
và các `\s`/`strip` của grammar. Root cause này đã tồn tại cho ref đơn ở nền; commit sửa làm nó biểu hiện ở
biểu thức trước bị từ chối vì literal có OR. Đây không phải lỗi mới của logic ưu tiên toán tử hay chọn runner thật.

**VẤN ĐỀ / TÁC ĐỘNG:** helper có thể trả một mảng thành công cho expression không được lexer Actions chấp nhận.
Ví dụ tạo đúng hai ký tự U+00A0 ngoài literal (escape trong đoạn Python dưới là cách dựng ký tự, không phải hai chữ
`\` và `u` được đưa vào expression):

```python
cond = "github.ref\u00a0==\u00a0'x||y'"
expr = f"({cond}) && '[\"ubuntu-latest\",\"windows-latest\"]' || '[\"ubuntu-latest\"]'"
ctx = {"ref": "x||y"}
```

**PHÉP ĐO:**

```sh
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/whitespace_probe.py > evidence/whitespace_probe.log 2>&1
```

rc=0; [output thật](evidence/whitespace_probe.log):

- `newly-accepted-invalid-nbsp`: base/lượt 1 **ValueError**, head **OK `["ubuntu-latest","windows-latest"]`**,
  actionlint **rc=1**, `got unexpected character '\u00a0' while lexing expression`.
- Đối chứng ref đơn `'x'` với cùng NBSP: cả ba evaluator đều OK/actionlint rc=1 ⇒ lexical permissiveness có sẵn.
- NBSP **bên trong** literal `'x ||y'`: head tính đúng, actionlint rc=0.
- TAB/CR/LF ngoài literal: head tính đúng, actionlint rc=0. VT/FF/EM SPACE: kết quả tương tự NBSP sai trong guard_probe.

**ĐÃ THỬ HƯỚNG SỬA:** thêm kiểm whitespace ngoài literal theo tập space/TAB/CR/LF trên **archive tạm**:
NBSP ngoài literal bị ValueError trước tính, Unicode trong literal và TAB/CR/LF vẫn nhận; t162 **1/1 rc=0**.
[Log t162](evidence/whitespace-fix-t162.log), [thử nghiệm patch](evidence/whitespace-fix.patch).
Patch là dữ liệu minh họa: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.
Chưa đo toàn gate cho thử nghiệm này; không áp vào checkout được review.

**CÁCH KHÓA / QUYẾT ĐỊNH:** owner **executor wp878**. Nếu siết grammar, kiểm whitespace ngoài literal trước mọi
`strip` hoặc dùng lexer/tập whitespace đúng, giữ Unicode trong literal; thêm ca âm NBSP/VT/FF và ca dương TAB/CR/LF,
Unicode trong literal, đối chứng actionlint. Không chỉ dùng `re.ASCII`: VT/FF vẫn thuộc `\s` ASCII.
Ghi P3 và chấp nhận làm nợ vì chỉ ảnh hưởng helper mô phỏng với input lexical lạ; workflow hiện tại dùng ASCII chuẩn,
actionlint vẫn kiểm workflow độc lập. Không có bằng chứng ảnh hưởng runtime hoặc bypass quyền/CI admission.
Không yêu cầu thêm vòng P2 vì đã đóng hai lớp cũ. Độ tin cao cho phản ví dụ, giới hạn tác động như trên.

## N4 — KHÔNG ĐO ĐƯỢC OFFLINE

Không dispatch thật, không đọc jobs API, không đo phút Ubuntu/Windows hoặc startup/skipped của jobs trên GitHub.
Bảng model, actionlint và mô phỏng DAG lượt 1 không thay N4. M-1/M-2 và CI thật chưa được xác nhận bởi lượt review này.
Theo chỉ thị review, thiếu phép đo N4 được tách khỏi verdict mã; **approve** ở đầu file là quyết định mã trên exact SHA,
không là quyền merge/land/deploy.
