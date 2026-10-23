verdict: changes_requested
reviewed_sha: 52e1f0b69d90247c6b7c90730b81ff8af3de3cba
reviewed_tree: 73e070534bad5749e5ab727797272c1b1ebcfef4
base_sha: 4581cfa5124ef803bfda10ce4de499b0ed31380e

Có **1 P2 và 1 P3** trong evaluator vừa tổng quát hóa. P2 là hồi quy miền biểu thức mà bản cũ hỗ trợ:
tách `&&` ngay trong literal của ref/label. Bảng N2 hiện tại đúng theo mô hình. N4 chưa đo được offline,
tách khỏi verdict mã và không phải finding. Review này không cấp merge/land.

Reviewer: OpenAI Codex, độc lập với executor Claude; `codex_cli`, transport `machine`, run `8ee64590`.
[Header của đúng run](evidence/reviewer-header.txt) công bố Codex CLI 0.163.0, model `gpt-6.1-sol`, effort `xhigh`.
Đây là bằng chứng header, không chứng minh mọi request giữ nguyên model/effort. Áp ngưỡng không còn P0/P1/P2.

## BẢNG ĐO

### Danh tính, phạm vi và tính toàn vẹn

- `sha256sum SPEC.md`: `13abe7208cb50f08013937c4db9cb434d44dcb9dcd81c6920bb98fe017620124`, khớp LEASE.
  HEAD/tree khớp snapshot; checkout detached; `core.abbrev=7` trên checkout và cả hai clone A/B.
- `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/scope_hunts.py` →
  `WRITE_SET True`, `DIFF_PACKET_EXACT True`, `NUMSTAT_EXACT True`, `YAML_OUTSIDE_ALLOWED_EQUAL True`.
  Diff đúng 5 tệp cho phép. YAML parse chỉ khác `on.workflow_dispatch` và `jobs.chuan-bi.outputs.os`;
  jobs/checks, steps, timeout, concurrency và các trigger còn lại bằng nhau. PyYAML đọc `on` thành khóa `True`.
- Trong `ops/ci_duong_nhanh_test.py`, loại hai hằng `KHUNG_TOP`/`KHUNG_JOB` thì AST toàn module bằng nhau;
  hai hằng cũng chỉ khác đúng input dispatch và output os. Diff chỉ sửa hai dòng ghim (2284, 2286).
  `CLAUDE.md` chỉ mở rộng đúng một câu ở bài học (c).
- `PYTHONDONTWRITEBYTECODE=1 python3 evidence/topology_pin_probe.py` → `base-pins/base-YAML rc=0`,
  `base-pins/head-YAML rc=3 DO:y13...cap workflow lech khung`, `head-pins/head-YAML rc=0`.
  Đã đo được lý do SPEC cho phép sửa hai ghim. `git -C cay-kho diff --check <base> <head>` rc=0.
  [Log phạm vi](evidence/scope_hunts.log), [log ghim](evidence/topology_pin_probe.log).

### Tái lập số PR: nền và head trong cùng một lệnh

Lệnh đã chạy: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/ab.py`. Script dùng hai clone local exact SHA,
`core.abbrev=7`, đặt `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null` giống nhau cho mọi lệnh.
Mỗi phía lần lượt chạy:

```sh
python3 .claude/dev/ci_dang_ky_test.py
python3 ops/ci_duong_nhanh_test.py
python3 ops/lease_publish_test.py
actionlint -no-color
ruff check --no-cache --select F scripts/tl.py ops/lease_publish_test.py ops/ci_duong_nhanh_test.py .claude/dev/ci_dang_ky_test.py
python3 .claude/dev/packet_loop.py doctrine-scan --root .
```

| Phép đo | PR khai | Nền đo được | Head đo được | Đánh giá |
|---|---|---|---|---|
| Registry mặc định, không `--chay` | 1053 → 1056 | [PHẢN CHỨNG: 1052/1053 đỏ đúng; rc=1](evidence/base-0.log) | [PHẢN CHỨNG: 1056/1056 đỏ đúng; rc=0](evidence/head-0.log) | Số lượng +3 khớp; xem chạy lại bên dưới |
| Fast-path | 104/104; 383/383 cả hai | [CA: 103/104 dat · 0 do · 1 hong; DOT BIEN: 378/383 bi giet dung ly do; rc=1](evidence/base-1.log) | [CA: 103/104 dat · 0 do · 1 hong; DOT BIEN: 378/383 bi giet dung ly do; rc=1](evidence/head-1.log) | Cùng lỗi socket fixture, thiếu khả năng đo đủ |
| Lease publish toàn bộ | 265/267 cả hai | [lease_publish: 265/267 đạt; đã chạy=267, bỏ qua=0; rc=1](evidence/base-2.log) | [lease_publish: 265/267 đạt; đã chạy=267, bỏ qua=0; rc=1](evidence/head-2.log) | Hai ca thiếu shellcheck; không bỏ qua |
| actionlint 1.7.7 | Không thêm finding | [0 finding; rc=0](evidence/base-3.log) | [0 finding; rc=0](evidence/head-3.log) | Delta 0; thiếu shellcheck |
| Bare Ruff F | Delta 0 | [21 finding; rc=1](evidence/base-4.log) | [21 finding; rc=1](evidence/head-4.log) | Đối chiếu multiset: delta 0 |
| Doctrine scan | rc=0 | [doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine; rc=0](evidence/base-5.log) | [doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine; rc=0](evidence/head-5.log) | 10 tệp, không chép doctrine |

[JSON mã thoát/thời lượng từng lệnh](evidence/ab.json), [driver log](evidence/ab-driver.log).

Lượt đầu chưa cô lập Git config bị fixture commit rc=128: máy bật `commit.gpgsign=true`, signer `/tmp/code-sign`
không kết nối được endpoint loopback trong sandbox. Lượt này dừng trước kết quả suite; đã giữ
[log setup](evidence/setup-base-0.log). Không sửa Git global config hoặc dùng mạng để khắc phục; chỉ cô lập
config của subprocess fixture. Sau cô lập, lượt đầu registry nền có một probe process-cleanup không ổn định
`p637-A3c-chau-setsid-thoat-nhom-van-bi-bat` LỌT: 1052/1053. Chạy lại **cả hai vế trong một lệnh**, cùng env/config,
cho nền **1053/1053 rc=0**, head **1056/1056 rc=0**:
[base repeat](evidence/base-registry-repeat.log), [head repeat](evidence/head-registry-repeat.log).
Không xóa bằng chứng lần đầu hay suy probe ngoài diff này là lỗi packet.

Fast-path cả hai: `t20zo_la_khong_phai_tep_thuong_do` hỏng tại `socket.bind`, `PermissionError: [Errno 1] Operation not permitted`.
Năm mutant phụ thuộc ca này không đo được đúng lý do vì ca nền chưa xanh. Không gọi 378/383 là 383/383.
Lease hai ca đỏ: `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck` và
`t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`, đều thiếu `shellcheck` trên PATH.
`actionlint rc=0` không chứng minh đã kiểm luật shell.

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/lint_delta.py`: Ruff local **0.16.9** (workflow pin 0.15.15),
Python **3.13.16** (CI khai 3.12). Hai phía 7 F401 + 2 F541 + 12 F821 = 21: 9 ở lease test, 12 ở tl.py.
So multiset `(file tương đối, code, message)`, không chỉ số lượng: `RUFF_NORMALIZED_DELTA {} {} equal=True`.
[Log lint delta](evidence/lint_delta.log). Contract `RUFF CI: 3/3` trong registry test là phép đo khác với bare lint.

### N1 và N2 trên chính biểu thức YAML head

N1 đúng: choice, required false, default `windows-and-ubuntu`, options đúng thứ tự hai giá trị yêu cầu.
`loi_ci_dispatch_windows` đọc workflow thật và không báo lỗi trên head. Lệnh
`PYTHONDONTWRITEBYTECODE=1 python3 evidence/evaluator.py` đọc expression qua YAML từ Git object, không chép lại.

| Event | runner_set | Nhãn | Mảng model trả |
|---|---|---|---|
| workflow_dispatch | windows-only | trống | `["windows-latest"]` |
| workflow_dispatch | windows-and-ubuntu | trống | `["ubuntu-latest","windows-latest"]` |
| workflow_dispatch | vắng trong ctx.inputs | trống | `["ubuntu-latest","windows-latest"]` |
| pull_request | vắng | trống | `["ubuntu-latest"]` |
| pull_request | vắng | windows | `["ubuntu-latest","windows-latest"]` |
| push master | vắng | trống | `["ubuntu-latest"]` |

Đây là kết quả của MÔ HÌNH. Context trống do test dựng không chứng minh service sẽ cung cấp context trống.

### Ngữ nghĩa Actions: đo tĩnh và giới hạn offline

`actionlint -no-color -debug -shellcheck= -pyflakes= evidence/semantics-static.yml` không finding:
`true || false && false`, `true && 'chosen' || 'fallback'`, `inputs.runner_set` và `github.event.inputs.runner_set`
đều parse/typecheck được. [Log](evidence/semantics-static.log). actionlint không chạy biểu thức.
Tài liệu actionlint 1.7.7 cài sẵn mô tả choice là string ở cả hai context; Boolean mới khác kiểu.
[Trích tài liệu offline](evidence/offline-actionlint-inputs.txt), nguồn `/root/.local/bin/docs/checks.md:1443`–1504.
Không có engine Actions thật hoặc tài liệu GitHub lưu offline trong các vị trí đã tìm; không tải qua mạng.

| Giả định cần kiểm | Trạng thái đo | Hệ quả nếu sai |
|---|---|---|
| `&&` ưu tiên hơn `\|\|` | Model dùng thứ tự ấy; actionlint nhận cú pháp. **KHÔNG ĐO ĐƯỢC** trên Actions thật | Nếu nhóm khác, Windows-only có thể bị nhánh hai nền ghi đè |
| `a && 'chuỗi' \|\| b` giữ nguyên string truthy | Parse/typecheck được; **KHÔNG ĐO ĐƯỢC** giá trị/truthiness trên Actions thật | Output có thể thành Boolean/giá trị khác, làm fromJson/matrix lỗi |
| Non-dispatch thiếu input trả `''` | Test tự dựng `{}`; **KHÔNG ĐO ĐƯỢC** context dịch vụ | Nếu vắng gây lỗi truy cập, chuan-bi có thể đỏ; nếu inject default/string khác thì event guard vẫn bảo vệ PR/push |
| API dispatch bỏ khóa nhưng workflow có default vẫn trả `''` | **KHÔNG ĐO ĐƯỢC** default hydration; không coi “request thiếu khóa” là “context rỗng” | Nếu dịch vụ áp default `windows-and-ubuntu`, output vẫn hai nền như input rỗng; chưa chứng minh lỗi mã |
| choice và `github.event.inputs` so với `inputs` | Tài liệu/typechecker local: choice string ở cả hai; payload thật và API validation: **KHÔNG ĐO ĐƯỢC** | Nếu inputs không chứa choice nhưng event.inputs có, explicit Windows-only có thể rơi về hai nền |

**N4: KHÔNG ĐO ĐƯỢC** — không dispatch GitHub, không jobs API, không có số phút Ubuntu/Windows hoặc bằng chứng
startup thật. Mô phỏng DAG bên dưới không thay thế N4. Chưa xác nhận M-1/M-2 của lease hay CI xanh trên GitHub.

### Tương thích và fail-close của evaluator

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/evaluator.py` → [log đầy đủ](evidence/evaluator.log):

- Biểu thức nền thật, A3 có `github.ref`, fail-close `fromJSON(...)`: mỗi ca **36/36** context cho cùng kết quả cũ/mới.
- Sinh 258 biểu thức OR 1–3 atom trong grammar cũ × 36 context: cũ nhận **9288** cặp, mới trùng **3024**,
  từ chối **6264**, không có mảng trả khác trong phần được cả hai nhận. Tập hữu hạn này không vét hết ngôn ngữ;
  phản ví dụ literal `&&` đã bác bỏ yêu cầu tương thích trên MỌI biểu thức cũ nhận.
- Ref `feature&&x` và label `win&&dows`: cũ OK/hai nền khi khớp; mới ValueError; actionlint rc=0. `git check-ref-format 'refs/heads/feature&&x'` rc=0.
- `inputs.123`: mới OK/trả mảng, actionlint rc=1 với token INTEGER sau dấu chấm. Chiều nhận sai đã đo.
- `contains(..., 'win||dows')`, ngoặc lồng, equality với chuỗi rỗng: actionlint nhận, mô hình từ chối.
  Hai trường hợp đầu là giới hạn có sẵn; không báo thành hồi quy mới. Literal `&&` là hồi quy mới.
- Nhánh OR/AND rỗng bị mới từ chối đúng. Bản cũ có thể nhận OR rỗng hoặc atom lạ ở sau vế đúng do short-circuit;
  việc mới kiểm tất cả atom và từ chối chúng là siết fail-close có ích, khác lỗi từ chối literal hợp lệ.
- Ký tự AND/OR trong mảng JSON không bị split nhầm; `fromJSON(...)` ngoài vẫn bị từ chối.

## BẢNG ĐỘT BIẾN

`PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py` tạo `mktemp -d`, dùng
`git -C cay-kho archive 52e1f0b69d90247c6b7c90730b81ff8af3de3cba`, giải nén mỗi mutant riêng.
Không sửa `cay-kho/`. Trong MỖI bản chạy đủ ba lệnh, env/config giống A/B:

```sh
python3 ops/lease_publish_test.py --chi-ca=t16
python3 .claude/dev/ci_dang_ky_test.py
python3 ops/ci_duong_nhanh_test.py
```

| Mutant | Lease t16 | Registry mặc định | Fast-path | Sống/chết và chốt |
|---|---|---|---|---|
| (a) Gỡ nhánh Windows-only | [8/9 đạt; đã chạy=9, bỏ qua=0; rc=1](evidence/mutations.kWuwnF/a-remove-branch-0.log) | [rc=1](evidence/mutations.kWuwnF/a-remove-branch-1.log) | [rc=1; y13 ĐỎ](evidence/mutations.kWuwnF/a-remove-branch-2.log) | CHẾT — t162 + đọc input/ba mảng + y13 |
| (b) Default thành windows-only | [9/9 đạt; đã chạy=9, bỏ qua=0; rc=0](evidence/mutations.kWuwnF/b-change-default-0.log) | [rc=1](evidence/mutations.kWuwnF/b-change-default-1.log) | [rc=1; y13 ĐỎ](evidence/mutations.kWuwnF/b-change-default-2.log) | CHẾT — hợp đồng input + y13 |
| (c) Bỏ option windows-only | [9/9 đạt; đã chạy=9, bỏ qua=0; rc=0](evidence/mutations.kWuwnF/c-remove-option-0.log) | [rc=1](evidence/mutations.kWuwnF/c-remove-option-1.log) | [rc=1; y13 ĐỎ](evidence/mutations.kWuwnF/c-remove-option-2.log) | CHẾT — hợp đồng input + y13 |
| (d) Nhánh đầu trả hai nền | [8/9 đạt; đã chạy=9, bỏ qua=0; rc=1](evidence/mutations.kWuwnF/d-two-platforms-0.log) | [rc=1](evidence/mutations.kWuwnF/d-two-platforms-1.log) | [rc=1; y13 ĐỎ](evidence/mutations.kWuwnF/d-two-platforms-2.log) | CHẾT — t162 + ba mảng + y13 |
| (e) Đảo thứ tự nhánh | [8/9 đạt; đã chạy=9, bỏ qua=0; rc=1](evidence/mutations.kWuwnF/e-swap-branches-0.log) | [rc=1](evidence/mutations.kWuwnF/e-swap-branches-1.log) | [rc=1; y13 ĐỎ](evidence/mutations.kWuwnF/e-swap-branches-2.log) | CHẾT — t162 + thứ tự mảng + y13 |

[JSON 15 lượt](evidence/mutations.json), [driver log](evidence/mutations-driver.log); mỗi mutant có diff riêng trong thư mục archive.
“CHẾT” chỉ tính khi thấy lỗi đúng chốt (`t162`, `ci.yml` input/mảng, `y13`), không lấy rc đỏ vì sandbox làm bằng chứng.
Các lượt fast-path mutant còn có lỗi socket nền và mutant nội bộ không đo được vì y13 gốc đã đỏ;
chỉ lỗi y13 trực tiếp trên workflow bị đột biến là bằng chứng ở cột trên.

## BẢNG SĂN

Ba hướng sau độc lập với grammar evaluator, năm đột biến yêu cầu và phép đối chiếu scope.
Cùng lệnh `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/scope_hunts.py`,
[output thật](evidence/scope_hunts.log), rc=0:

| Hướng / giả thuyết | Output thật và phép thử | Kết luận |
|---|---|---|
| Dependency/artefact: thiếu Ubuntu làm mất predecessor hoặc artefact gom mảnh | `HUNT1_DAG {"job_ids":9,"instances":23,"ubuntu":["chuan-bi"],"windows":22,"errors":[]}`; cả hai cặp upload/download Windows `matched=8/8` | KHÔNG PHẢI LỖI trong cấu trúc mô phỏng; startup thật KHÔNG ĐO ĐƯỢC |
| Dataflow: runner_set lạ có thể vào thẳng runner hoặc shell | `HUNT2_TAINT`: chỉ reference ở `jobs.chuan-bi.outputs.os`; 16 giá trị gồm chuỗi ký tự shell/JSON/object/bool, `unexpected=[]`; output chỉ mảng hằng | KHÔNG PHẢI LỖI trong dataflow và model; không nói API chấp nhận giá trị lạ, không đo case folding của Actions |
| Meta-test: vô hiệu checker mới mà phản chứng vẫn xanh | Archive sạch, monkeypatch checker trả `([],3)`; `phan_chung=False`; hai probe default/option `LỌT`; `1054/1056 đỏ đúng` | KHÔNG PHẢI LỖI — checker no-op bị giết bằng đúng hai probe mới |

## BẢNG LỚP

| Slug | Biểu hiện | Hạng | Cách đóng |
|---|---|---|---|
| evaluator-splits-quoted-operators | ref literal `&&`; label literal `&&` | P2 | Split theo token/quote/ngoặc; A/B old grammar + ca âm + t16 |
| evaluator-accepts-numeric-property | nhận identifier số; từ chối identifier có gạch nối | P3 | Identifier grammar đúng; actionlint hai chiều + t16 |

Hai lớp, bốn biểu hiện; review lượt 1 trên exact SHA ở đầu file. Hai lớp cần sửa ở hai thao tác khác nhau
(scanner toán tử và regex tên input); không gộp để bỏ sót một chiều. P3 owner: executor wp878, nên xử lý cùng helper;
P2 còn mở là lý do yêu cầu thay đổi.

### evaluator-splits-quoted-operators  [P2]  Tách toán tử trong literal làm mất tương thích evaluator cũ

**TỆP/DÒNG:** `ops/lease_publish_test.py:7893`.

**VẤN ĐỀ:** `ve.split("&&")` tách ngay trong chuỗi đơn. Với điều kiện `github.ref == 'refs/heads/feature&&x'`
hoặc `contains(github.event.pull_request.labels.*.name, 'win&&dows')`, helper cũ nhận và tính đúng,
helper mới ném ValueError trước khi tính. Đây là ref/label literal hợp lệ trong grammar mà helper đã hỗ trợ,
không phải yêu cầu mở thêm cú pháp ngoài phạm vi. Hồi quy này vi phạm chốt tương thích của review;
không khẳng định expression hiện tại của workflow chọn sai nền.

**ĐÃ THỬ NGHIỆM:** `PYTHONDONTWRITEBYTECODE=1 python3 evidence/evaluator.py` →
`valid-ref-with-and`/`valid-label-with-and`: old OK/hai nền, new `ValueError KHÔNG ĐO ĐƯỢC`;
actionlint hai ca rc=0. 6264/9288 cặp old nhận trong mẫu bị new từ chối.
`git check-ref-format 'refs/heads/feature&&x'` rc=0.

**ĐÃ THỬ VÁ:** có, chỉ trên archive tạm. `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null python3 evidence/repair_probe.py`
đổi split thành scanner theo quote/độ sâu ngoặc → `REPAIR_COMPATIBILITY 9288/9288 mismatches=0`,
`REPAIR_T16 rc=0`, 9/9. [Log](evidence/repair_probe.log), [t16](evidence/repair-t16.log).
Đây là thử nghiệm minh họa, executor tự tái dẫn xuất và đo, không áp vào checkout được review.

**GỢI Ý VÁ / CA KHÓA / RỦI RO:** thay split tại dòng 7893 bằng tách token ngoài literal/ngoặc hàm;
khóa ref và contains label chứa cả `&&`/`||`, operator thật ngoài quote, nhánh rỗng và atom không hỗ trợ.
Giữ việc kiểm toàn bộ atom trước khi tính. Scanner sai có thể mở ngữ pháp ngoài ý muốn hoặc che nhánh rỗng;
đối chiếu old/new trên phần hợp lệ và vẫn giữ fail-close phần lạ.

**ĐỘ TIN:** cao, có phản ví dụ và bản thử sửa đã chạy. P2 còn mở.

### evaluator-accepts-numeric-property  [P3]  Grammar tên input nhận sai và từ chối sai

**TỆP/DÒNG:** `ops/lease_publish_test.py:7889`.

**VẤN ĐỀ:** regex `inputs\.(\w+)` nhận `inputs.123` nhưng từ chối `inputs.runner-set`.
Parser actionlint làm ngược lại đúng grammar property. Lỗ này nằm ở mô hình fail-close;
workflow hiện tại dùng `runner_set`, không chịu ảnh hưởng.

**ĐÃ THỬ NGHIỆM:** `PYTHONDONTWRITEBYTECODE=1 python3 evidence/identifier_probe.py` →
`123`: HEAD OK/trả mảng, actionlint rc=1 `unexpected token "INTEGER" ... expecting "IDENT", "*"`;
`runner-set`: HEAD ValueError, actionlint rc=0; `_runner` và `runner_1` đều HEAD OK/actionlint rc=0.
[Log](evidence/identifier_probe.log).

**ĐÃ THỬ VÁ:** có, trên cùng archive thử sửa: identifier `[A-Za-z_][A-Za-z0-9_-]*` cho đúng kết quả cả bốn ca;
`inputs.123`, nhánh rỗng, fromJSON vẫn ValueError, t16 9/9. Không sửa checkout reviewed.

**GỢI Ý VÁ / CA KHÓA / RỦI RO:** dùng grammar identifier của Actions, hoặc chỉ hỗ trợ runner_set nếu chủ ý giữ tối giản;
khóa cả số đầu và dấu gạch nối bằng actionlint đối chứng. Regex quá chặt có thể làm mất input hợp lệ.
Owner executor wp878; quyết định P3: nên vá cùng helper, không phải blocker độc lập.

**ĐỘ TIN:** cao với đối chiếu static parser; runtime GitHub chưa đo.

## Giới hạn và checkout read-only

Chỉ đo offline Linux trong sandbox `workspace-write`; mọi code edit/đột biến ở archive/clone riêng dưới `evidence/`.
Không sửa nhánh executor, không đăng GitHub, không dispatch, merge hoặc deploy. Không nhận các kết quả suite lỗi setup
là pass. N4, phút tính tiền, payload/default thực và full CI trên GitHub chưa đo.

Snapshot read-only: 4897 file nội dung, HEAD/tree, tracked/untracked/ignored status, worktree/index diff trước/sau **bằng nhau**.
[Trước](evidence/read-only-before.json), [sau](evidence/read-only-after.json). Snapshot chỉ chứng minh không có delta giữa hai mốc quan sát; không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

Trạng thái bảng đo: hoàn tất 12 lệnh A/B và 15 lệnh mutant.
