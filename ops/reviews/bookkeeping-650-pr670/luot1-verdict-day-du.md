**2 P1 / 1 P2 / 0 P3**
verdict: changes_requested

```yaml
reviewed_sha: d535cf64d5f676819f2fe734f9fa4cb83470613f
reviewed_tree: 0541ff8f3cc8f2d7eb2c2e9ec1d746521d388591
base: 3fee59ec32a37bde7f5eae24ff174c4235cb5a26
base_tree: 32147c90a76b90c0486f5a00dfeb4ad2381cec08
pr: 670
review_round: CLI-1
role: reviewer
provider: openai_codex
execution_surface: codex_cli
transport: machine
assurance: advisory_review
review_class_applied: sensitive
review_axes: [spec, standards_security]
model_runtime: not_measured
effort_runtime: not_measured
github_submitter_identity: null
published: false
```

Các OID trên được đo bằng Git trong checkout được giao, không chép từ prompt. Kết quả này yêu cầu sửa lời khai và ranh giới phép đo; không phủ nhận các run đã success, không tuyên đã thấy một transition sai trên GitHub. Không cấp quyền merge/land và không tạo `cross_approved`.

Authority lượt này là assignment trực tiếp của người dùng: review offline PR #670 trên exact SHA, ngưỡng **không còn P1/P2/P3**, chỉ ghi hiện vật review trong `/tmp/review670-r1-output/`. Không dùng lease executor #650 đã hết hạn để cấp việc mới. Executor là Claude; không gọi reviewer Claude, không fork context executor, không dùng subagent.

Đã đọc CONTEXT, protocol §7/§8/§10/§13 và phần liên quan, CLAUDE, hợp đồng đa provider, adapter `.agents/skills/cross-review/SKILL.md`, spec/lease r5 và verdict #667 CLI5. Scope thật của diff là **15 tệp**, đều dưới hai YAML được giao và cây `ops/land/pr666-wp650-provenance/`; không đổi workflow, sản phẩm, spec đóng băng hoặc release artifact. Spec nguồn/local/lease khớp SHA-256 `978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77`, revision **5**, generation **2**. Base bookkeeping #670 không thay acceptance baseline lịch sử của #650.

Checkout detached, tracked/untracked sạch; `.codex/` ignored và rỗng. `origin` là mirror local `/home/user/tra-luat`, không phải phép xác minh GitHub hiện hành. Không đổi origin/config/ref. Sandbox thực tế `workspace-write`; checkout được giữ chỉ đọc bằng hành vi, không tự khai cơ chế sandbox chặn mọi write. Không có header runtime độc lập của lượt này để nhận dạng exact model/effort; `codex --version` chỉ đo binary có sẵn, không chứng minh model phục vụ request.

## Lớp A — Toàn vẹn dữ kiện

**Các đối chiếu hash/OID/ID/marker hiện có đều khớp.** Có một finding về diễn giải lý do skipped, N1 bên dưới.

Lệnh đã chạy:

```text
python3 -B /tmp/review670-r1-output/run_checks.py start
  git diff --check origin/master..HEAD: rc=0, không diagnostic
  python3 -B .claude/dev/packet_loop.py doctrine-scan --root .: rc=0
    doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
  sha256sum -c <ROOT>/ops/land/pr666-wp650-provenance/SHA256SUMS-log-va-artifact.txt
    cwd=/tmp/do650, rc=0, 12/12 OK
  python3 -B ops/land/pr666-wp650-provenance/doi_chieu_buoc.py: rc=0

python3 -B /tmp/review670-r1-output/audit_facts.py
  lần hoàn chỉnh: rc=0
  YAML_UNIQUE: 2/2
  YAML_NEGATIVE duplicate key a line 2
  RAW_BYTE_EXACT: 11/11 tệp JSON
  ALL_TARGETED_FACT_ASSERTIONS_PASSED

python3 -B /tmp/review670-r1-output/audit_extra.py
  rc=0
  ARTIFACT_INTERNAL_HASHES runner/command/catalog MATCH
```

`<ROOT>` là `/tmp/claude-0/-home-user-tra-luat/0682048d-075d-5414-b3ff-642b89411167/scratchpad/rc1`. Harness lưu argv tuyệt đối, cwd, rc thật và stdout/stderr tại `commands.jsonl` và các tệp `.stdout`/`.stderr` cạnh verdict. Lần đầu `audit_facts.py` trả **1** do bộ trích của reviewer chỉ nhận executable `git`, bỏ sót `git.exe` trên Windows. Đã sửa riêng script scratch để nhận command `log -1 --format=%H` của cả hai nền và chạy lại; đây là lỗi harness reviewer, không phải finding của PR. Output lần lỗi vẫn giữ trong `audit-facts.stderr`.

| Phép đối chiếu | Đo được |
|---|---|
| 10 log + `art.zip` + `art/tl-selftest-Linux.out` | Khớp đủ 12 dòng SHA256SUMS. |
| Readback trong Git so với `/tmp/do650` | 10 readback JSON và 1 JSON artifact byte-exact; không chỉ bằng nhau sau parse. |
| YAML | Parse khóa duy nhất 2/2; negative control khóa `a` trùng bị từ chối ở dòng 2. |
| PR run `36379712476`, attempt 1 | REST head `bf63bb1…`; **cả 4 log gate*** in checkout `511612f1f9383097e06d87a2b860de9c8335471e`. |
| Synthetic merge | Git và readback commit cùng parents `ceb1a3f36912dd4f03fe1741c443cd09e82a44ee`, `bf63bb1ec485bccf8eec34cc5604f949d70fc7d6`; tree `235f6605809b4f813adf5fdc467aae3944093629`. |
| Master CI `36387278453`, launcher `36387278424` | Đúng push/attempt 1/head `f8a7829…`; 6 log checkout đúng full SHA ấy. Parents/tree khớp Git. |
| Merge #666 | OID/tree/parents/time khớp Git; committer time `2026-09-28T13:35:57+07:00` = `06:35:57Z`. Authorized head là cha thứ hai; tree head = tree merge. |
| Merge #667 | `3fee59ec32a37bde7f5eae24ff174c4235cb5a26`, parents `f8a7829…`/`60971e6…`, thời điểm `2026-09-28T10:00:09Z`; khớp readback branch và base. |
| Run/job readbacks | 3 run; danh sách jobs đủ theo `total_count` 5/5, 5/5, 2/2. 10 job được viện dẫn khớp run ID, attempt, tên, head, success và runner. Hai `chuan-bi` không được dùng làm phép checkout. |
| Markers | Có trong đúng log: selftest 1711/1711; packet-loop 291/291 + bỏ qua 1; receipt 68/68 và 74/74; doc-receipt 156/156 và 162/162; launcher Windows 172/172 và Ubuntu 188/188. |
| Workflow bytes | `ci.yml`: blob `6ba1255b5ae5635e1ffc9495b11462b3f5c2fd14`, SHA-256 `69100292ffee7b13b71053006df98239ffe1c86328d2c3af8e089b46dc243d16`; launcher: blob `24b55164eca4fef5c76aae13cb691e4bb103d05e`, SHA-256 `fd382397fe05b6d98ee9957cee19a732dbe4855c88d090a49462ec7c6cc6233f`. Cả hai giống nhau ở đủ bốn commit nêu trong YAML. |
| Lần sửa cuối workflow | `6f2b0f96165a9292e34943b1a10904d4262b6549` ngày 27-09 và `f568e342dc35cbfecc133dfe8f83e41a6065c23c` ngày 05-09; đúng `git log -1`, đều ancestor của cả bốn commit. |
| Artifact `10956094584` | ZIP hash `517a22a4579ac5a09b526e5cbd26ebcfb5ca844bb5d43ecfa8d0b1b12e374fb1` khớp archive, descriptor REST và log upload; hai member byte-exact với bản giải nén. Output hash `99cf571924ec9c5488a029b463f3bd35f117f840f1b5fd65b4d7ce2e1269838d`, command, rc=0, marker, `positive_verified=true`, hai identity sạch/trùng nhau đều khớp. |
| Thời gian artifact | `07:22:59.367940Z` → `07:25:00.302350Z`; wall delta 120.934410s và duration 120.934729s chỉ lệch 0.000319s. `expires_at=2026-12-27T06:36:01Z` khớp descriptor. |

**Phạm vi chưa đo độc lập:** raw comment authorization, lịch sử sửa comment, các readback MCP lúc 07:31/07:40/07:43, các run thu hồi/mo/launcher PR ngoài ba run được cấp, inventory 489 refs và phép quét lease lịch sử không có đủ raw nguồn trong bundle này. Các URL/ID/giờ đó vẫn là lời khai có neo kế thừa #667; không biến việc đọc lại YAML thành GET độc lập. Khoảng cách 36 giây authorization→merge chỉ được kiểm số học và đối chiếu merge Git, không xác thực lại comment. Không phát hiện mâu thuẫn mới trong các lời khai kế thừa đã giữ giới hạn này.

### N1 — P1 — `skip-windows-bi-goi-chi-linux`

**Tệp:dòng:** `ops/land/pr666-wp650-provenance.yaml:87`.

YAML viết nguyên văn:

> `17 ca BO QUA tren Windows la ca chi-Linux; khong tinh la pass. Khong phai required context.`

Đúng là 17 ca bị bỏ qua, và đúng là không tính chúng thành pass. Nhưng gom lý do thành **“ca chỉ Linux”** xóa khác biệt giữa ca gắn với cơ chế POSIX và ca còn thiếu phép thử/fixture Windows. Log của chính job ghi các trường hợp sau:

```text
python3 -B /tmp/review670-r1-output/reproduce_findings.py
rc=0 (thu facts, không phải consistency pass)

log-108815209421.txt:241:
  BO QUA t03_git_gia_thoat_0_im_lang_van_bi_chan: bo qua tren Windows (can shim .cmd)
log-108815209421.txt:242:
  BO QUA t28_qua_han_giet_ca_CON_CHAU: bo qua tren Windows (can kiem bang cay tien trinh that)
log-108815209421.txt:244:
  BO QUA t50_stop_roi_runner_KHONG_duoc_de_len_so: bo qua tren Windows (can kiem rieng)
log-108815209421.txt:251:
  BO QUA t76_wrapper_thoat_khong_duoc_xoa_prompt_cua_chau: ca nhom tien trinh POSIX; Windows can fixture that rieng
log-108815209421.txt:259:
  172/172 ca DA CHAY QUA (tong 189, bo qua 17, hong 0) - KHONG DU: 17 ca BO QUA, chua do gi
```

Đã đọc thêm mã tại **đúng commit `f8a7829`**, không suy từ tên test: `launcher_test.py:540` và `:906` có return bỏ qua trên Windows với hai lý do `can kiem bang cay tien trinh that` / `can kiem rieng`. Đó là nghĩa vụ chưa đo trên Windows, không phải bằng chứng rằng tính chất chỉ áp dụng Linux. Dùng nhãn “chỉ Linux” có thể khiến người đọc loại phần chưa đo khỏi đánh giá coverage Windows. Xếp P1 theo tiêu chí user về lời khai sai/phạm vi chưa chứng minh; không nói 17 ca đã bị tính thành pass, cũng không nói launcher là required context.

**Đề xuất:**

- **Vá ở đâu:** `ghi_chu` của job Windows dòng 87, nơi đang phân loại sai lý do. Không sửa lịch sử log hoặc các số 172/189/17.
- **Vá thế nào:** ghi “17 ca bị bỏ qua trên Windows”, giữ các nhóm lý do nguyên văn hoặc trỏ tới danh sách log; khai rõ có ca cần fixture/kiểm Windows riêng. Không suy “không áp dụng Windows” từ việc implementation hiện trả skip. Đây là sửa disclosure; không yêu cầu PR bookkeeping chạy thêm 17 test.
- **Ca khóa:** đối chiếu đủ 17 dòng `BO QUA` với phần ghi chú; mẫu chứa `can shim .cmd`, `can kiem rieng` hoặc `Windows can fixture that rieng` phải không được phân loại thành “chỉ Linux/không áp dụng Windows”. Các ca SIGTERM/setsid thật sự POSIX phải vẫn giữ đúng lý do. Phản chứng nguồn đã trích và đã chạy ở script trên.
- **Rủi ro:** đổi hàng loạt mọi skip thành “nợ Windows” cũng có thể sai với ca POSIX có ca tương ứng riêng. Chỉ giữ điều log/mã thật sự chứng minh; không biến bookkeeping thành mở rộng acceptance hoặc waiver mới.

### Tái hiện `doi_chieu_buoc.py` và phản chứng

```text
python3 -B ops/land/pr666-wp650-provenance/doi_chieu_buoc.py
rc=0
PR gate: 28/28; master gate: 27/27
gate-ops: 8/8 mỗi job; gate-packet-loop: 8/8 mỗi job
gate-registry: 8/8 mỗi job; launcher Windows: 11/11; Ubuntu: 7/7
all_in_order=true: 10/10 job

python3 -B /tmp/review670-r1-output/mutations.py
rc=0
EXECUTOR_MUTATION_EXACT kiem-bam -> kiem-bamX, one ANSI run-body line
EXECUTOR_EXPECTED_REJECTION:
  job=gate, runs_defined=30, runs_in_log=27, matched=21, all_in_order=false
REVIEWER_EXPECTED_REJECTION:
  job=gate-packet-loop, runs_defined=8, runs_in_log=8, matched=7, all_in_order=false
```

Phản chứng executor: đã so bytes xác nhận `.mut` chỉ đổi một dòng ANSI `python .github/checks/ci_phamvi.py --kiem-bam` thành `--kiem-bamX`, rồi chạy chính `/tmp/do650/buoc_mut.py`; tái hiện đúng **21/27**. Phản chứng riêng: trong bản sao log job **108815233290**, thêm `--reviewer-mutant` vào command `python .claude/dev/packet_loop_test.py`; bản sao matcher chỉ đổi đường input về scratch, trả **7/8, false**. Cả hai tiến trình matcher vẫn **rc=0**: output JSON báo không khớp, không được viết thành “process mutant rc≠0”.

Có thêm phép thử giới hạn: xóa một dòng thân bước khỏi bản sao job 108815233290 → **7/7, `all_in_order=true`, rc=0**. Đây là phép so **dãy con theo thứ tự**, không tự kiểm log đầy đủ. Kết quả hiện tại 8/8 đã được đối chiếu với jobs API và definitions; tất cả bước API đánh dấu skipped đều có `if:`. Không tạo finding chỉ vì matcher không phải validator tổng quát; không dùng mỗi boolean hoặc rc=0 của nó làm bằng chứng đủ mọi bước.

## Lớp B — Bốn mốc provenance

| Mốc | Kết luận theo nguồn thật sự có |
|---|---|
| Run | Đủ facts cho 3 run/attempt được cấp: repository, event, ID, attempt, head, path, conclusion. Là kiểm lại readback được giao offline, không phải API reviewer tự gọi. |
| Checkout | Đủ: SHA in ngay sau `git log -1 --format=%H` trong đúng 10 log; log PR fetch/checkout synthetic merge. Parents/tree của chính OID ấy được Git object xác định và readback synthetic đối chiếu. Không lấy ref merge hiện tại thay cho run cũ. |
| Workflow definition | Blob/hash và sự khớp thân bước đã đo đúng; chủ kho đã chấp nhận **loại nguồn thay thế**. Exact **commit nguồn do GitHub chọn** chưa được nguồn đó phân biệt, nhưng YAML gán giá trị đơn với nhãn measured. N2. |
| Gate output | Các marker, command bodies, step conclusions và OS/runtime có trong log/API. Master `gate` có receipt artifact và numeric rc trực tiếp. Các job khác khai không có uploaded artifact; rc được suy từ step conclusion theo chính chú thích dòng 39, không phải numeric returncode trong receipt. Giữ khác biệt này. |

Runtime đo lại từ log: 8 job CI Ubuntu **24.04.5 / CPython 3.12.14**; launcher Windows **Server 2025 / CPython 3.13.15**; launcher Ubuntu **24.04.5 / CPython 3.11.16**. Đã kiểm definitions không có `continue-on-error` ở các steps được xét. API success và marker dương hỗ trợ kết quả bước chạy, nhưng không chứng minh các ca/bước skipped đã thực thi.

**Job ngoài `gate` không có artifact:** khai `KHONG CO` là đúng với workflow và descriptor được cấp. Run PR và launcher có `total_count=0`; master có đúng một artifact của `gate`. Các log đã neo SHA-256 vẫn là nguồn cho command/output; không cần bịa uploaded-artifact ID cho chúng. Hệ quả: chỉ master `gate` có receipt JSON để tái dùng theo giao thức artifact exact-identity; hash log của các job khác không biến chúng thành receipt ấy, cũng không cho mọi job cùng numeric rc trực tiếp của selftest. Không mở finding riêng chỉ vì workflow không upload artifact; thiếu uploaded artifact đã được khai và output có log để đối chiếu. Không tuyên gate evidence artifact đầy đủ cho 10 job.

### N2 — P1 — `ci-danh-tinh-suy-tu-head`

**Tệp:dòng:** `ops/land/pr666-wp650-provenance.yaml:49`, `:62`, `:85`, `:90`; phần dùng kết quả tại `ops/land/pr666-wp650-land-evidence.yaml:35` và `:39`.

Ba `workflow_definition` ghi `commit=511612f…` hoặc `f8a7829…`, đồng thời `trang_thai: measured_nguon_thay_the`. Phần chứng minh (a) chỉ ra bytes bằng nhau ở **bốn commit khác nhau**; (b) so run bodies từ log với bytes lấy tại `f8a7829`. Hai phép đo đó đúng, nhưng **không phân biệt GitHub đã dùng commit nào trong bốn commit**. Chúng chứng minh nội dung đối chiếu, không tự chọn được exact nguồn OID đang điền trong field `commit` theo §10.2.2.

Lệnh/phản chứng đã chạy:

```text
python3 -B /tmp/review670-r1-output/reproduce_findings.py
rc=0
defined_source=f8a7829 vs defined_source=ceb1a3f:
  JSON_EQUAL=True; all_in_order=10/10 both

ceb1a3f36912dd4f03fe1741c443cd09e82a44ee 6ba1255b5ae5635e1ffc9495b11462b3f5c2fd14 24b55164eca4fef5c76aae13cb691e4bb103d05e
bf63bb1ec485bccf8eec34cc5604f949d70fc7d6 6ba1255b5ae5635e1ffc9495b11462b3f5c2fd14 24b55164eca4fef5c76aae13cb691e4bb103d05e
511612f1f9383097e06d87a2b860de9c8335471e 6ba1255b5ae5635e1ffc9495b11462b3f5c2fd14 24b55164eca4fef5c76aae13cb691e4bb103d05e
f8a7829cc44f296c25faf1a6439b603ba840f70b 6ba1255b5ae5635e1ffc9495b11462b3f5c2fd14 24b55164eca4fef5c76aae13cb691e4bb103d05e

DECLARED_EXACT_WORKFLOW_COMMITS
  36379712476 -> 511612f1f9383097e06d87a2b860de9c8335471e measured_nguon_thay_the
  36387278453 -> f8a7829cc44f296c25faf1a6439b603ba840f70b measured_nguon_thay_the
  36387278424 -> f8a7829cc44f296c25faf1a6439b603ba840f70b measured_nguon_thay_the
```

Phép thử đổi **chỉ literal ref đọc định nghĩa** trong bản sao matcher từ `f8a7829` sang `ceb1a3f`; toàn bộ JSON kết quả giữ nguyên. Đây không phải bằng chứng GitHub đã dùng `ceb1a3f`, mà là bằng chứng phép đo được viện dẫn **không nhận dạng được lựa chọn commit**. Đọc toàn bộ ba run JSON không có `WorkflowRun.file.repositoryFileUrl`; các `head_sha`/head commit và checkout không cung cấp mốc nguồn workflow riêng. §10.2.2 cấm đồng nhất các mốc đó.

**Chấp nhận quyết định chủ kho ở dòng 107–109:** không ghi finding vì thiếu GraphQL, không bác tư cách loại nguồn thay thế và không yêu cầu xin lại sự chấp nhận ấy. Finding nằm ở việc nâng **bytes tương đương/commit đối chiếu** thành **exact source commit đã đo**, rồi dùng câu “bốn mốc đã đo/đã đóng” mà không khai giới hạn OID này. Quyết định chấp nhận loại nguồn không tự làm phép đo phân biệt được hai commit có cùng bytes. Không khẳng định các giá trị OID hiện điền chắc chắn sai; chúng đang được khẳng định mạnh hơn nguồn chứng minh. Xếp P1 vì hạ nguồn có thể dùng chúng như exact provenance đã đo.

**Đề xuất:**

- **Vá ở đâu:** ba record `workflow_definition` và giải thích `workflow_definition_nguon`; cập nhật câu đóng điều kiện trong land YAML cùng phạm vi. Đây là nơi trộn commit đại diện với commit nguồn CI; không sửa blob/hash vốn đúng.
- **Vá thế nào:** tách `commit_doi_chieu`/tập commit có cùng bytes khỏi exact definition source commit. Exact nguồn chưa đo thì khai rõ; vẫn giữ kết quả measured cho blob/hash, đối chiếu run bodies và disposition chủ kho chấp nhận nguồn thay thế. Nếu kết luận landed dựa vào disposition chấp nhận evidence tương đương đó, diễn đạt đúng là **chấp nhận nguồn thay thế với giới hạn exact nguồn OID**, không gọi giới hạn ấy là đã đo. Muốn khai actual source OID thì phải có nguồn khác phân biệt được nó, không nhất thiết GraphQL. Không suy thêm waiver ngoài nội dung authority đã có.
- **Ca khóa:** cùng input hiện tại, đọc definition ở `ceb1a3f` và `f8a7829` phải cùng xác nhận bytes, nhưng không được tự tạo hai kết luận “đã đo source commit” khác nhau. Đối chứng thứ hai: thay một thân bước phải vẫn bị phát hiện như mutant 21/27. Kiểm riêng source identity, bytes equivalence và disposition; không gộp thành một boolean `measured`.
- **Rủi ro:** chỉ đổi tên field mà vẫn để land note nói mọi thành phần exact identity đã đo là vá hờ. Ngược lại, xóa nguồn thay thế/đòi GraphQL bắt buộc sẽ phủ nhận quyết định chủ kho và bỏ mất evidence hợp lệ. Giữ evidence, sửa phạm vi lời khẳng định.

N2 nối lớp **G1 `ci-danh-tinh-suy-tu-head`** của #667: G1 trước được đóng nhờ ghi `*_suy_ra` và không dùng các giá trị ấy làm provenance. #670 có nhiều phép đo mới thật, nhưng phần exact source commit lại được nâng nhãn khi phép phân biệt vẫn thiếu. Không reset lịch sử lớp bằng tên mới.

## Lớp C — Required contexts và kết luận `landed`

**Required contexts hiện tại được đối chiếu đúng, không có finding riêng về danh sách.** Cả `/rules/branches/master` và ruleset 20856202 cho cùng ba context cùng producer integration ID **15368**:

```text
gate (ubuntu-latest)
gate-packet-loop (ubuntu-latest)
gate-ops (ubuntu-latest)
strict_required_status_checks_policy=false
```

Ruleset `active`, áp `~DEFAULT_BRANCH`, không exclude, bypass actors rỗng; branch readback tên master trỏ đúng base `3fee59e…`. Đồng thời legacy summary trong **GET branch** có `required_status_checks.enforcement_level=off`, `contexts=[]`, `checks=[]`. Vì thế không bỏ quên kiểu branch protection cổ điển, cũng không dùng lỗi 403 của `/protection` làm bằng chứng nó tắt. Đây là kết luận trong phạm vi fields của readback được cấp, không kiểm lại quyền/remote hiện hành.

Trong hai run PR/master, ba job cùng tên đều success. Launcher/mo không nằm trong tập context hiện tại; skipped của chúng vẫn không phải pass và không tạo Windows execution. Không suy mọi acceptance/obligation của packet từ danh sách branch contexts.

`updated_at=2026-09-27T20:19:13.048+07:00` chuyển UTC đúng là **2026-09-27T13:19:13.048Z**, trước merge. Nguồn history thực tế trong `/tmp/do650/hist.json` trả:

```json
{"message":"Resource not accessible by integration","documentation_url":"https://docs.github.com/rest/repos/rules#get-repository-ruleset-history","status":"403"}
```

YAML đã ghi rõ đây là readback **hiện tại**, lịch sử tại merge chỉ suy từ updated_at; không gọi 403 là pass. Timestamp này không chứng minh toàn bộ lịch sử policy khác/ruleset đã xóa/legacy protection. Tôi không dùng nó để khẳng định đã GET policy tại 06:35:57Z. Với phạm vi lời khai hiện tại đã giới hạn, không có lệnh/phản chứng chứng minh danh sách đang ghi sai.

Việc chuẩn bị `landed: true` **có hiệu lực khi PR này merge** không tự mâu thuẫn với việc branch review chưa vào master: điều kiện được viết rõ ở dòng 30/37; không thấy consumer máy trong scope được viện dẫn đã bỏ qua điều kiện này. PR #667 đã merge thật. Tuy nhiên kết luận “bốn mốc đã đóng” vẫn chịu giới hạn N2, và hồ sơ tham chiếu còn câu trái trạng thái dự kiến sau merge, N3.

### N3 — P2 — `landed-vuot-bang-chung`

**Tệp:dòng:** thay đổi tại `ops/land/pr666-wp650-land-evidence.yaml:29`; câu bị bỏ sót tại `ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a-r5.ERRATA.md:16` và `:17`.

Erratum đang viết **không có neo “tại lúc ghi erratum”**:

> `Không tạo revision hồi tố cho packet đã merge. Trạng thái packet là`
>
> `` `merged`, CHƯA `landed` — xem `trang_thai_packet` trong `ops/land/pr666-wp650-land-evidence.yaml`. ``

Trong khi PR này đặt đích được tham chiếu thành `landed: true`, có hiệu lực khi bản sửa merge. Tại thời điểm đó hai tuyên bố hiện tại của cùng hồ sơ nói ngược nhau. Đây là câu trạng thái đang trỏ tới nguồn hiện hành, không phải quote trong verdict lịch sử, commit message đóng băng hay `cau_sai` của lease. Nó đúng ở #667 và không cần viết lại lịch sử; thiếu **neo thời điểm** mới là lỗi của việc cập nhật trạng thái lần này.

```text
python3 -B /tmp/review670-r1-output/reproduce_findings.py
rc=0
ops/land/pr666-wp650-land-evidence.yaml:29:   landed: true
ops/land/pr666-wp650-land-evidence.yaml:30:   landed_hieu_luc_tu: 'merge commit cua PR mang ban sua nay vao master (tep chi co tren master sau thoi diem ay).'
ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a-r5.ERRATA.md:16:
  ... Không tạo revision hồi tố cho packet đã merge. Trạng thái packet là
ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a-r5.ERRATA.md:17:
  `merged`, CHƯA `landed` — xem `trang_thai_packet` trong `ops/land/pr666-wp650-land-evidence.yaml`.
UNQUALIFIED_ERRATUM_CONFLICT=True
```

Xếp P2: thiếu neo thời gian khiến người đọc spec/erratum nhận trạng thái khác với hồ sơ nghiệm thu sau merge. Không dùng N3 để khẳng định #650 hiện đã landed, cũng không sửa ngược phán quyết #667 vốn đúng tại SHA cũ.

**Đề xuất:**

- **Vá ở đâu:** câu trạng thái ở erratum nếu được cấp write set, hoặc thêm đính chính có chỉ đích erratum/dòng vào land YAML trong write set hiện tại. Không sửa spec r5 đóng băng, lease hay verdict đã giao.
- **Vá thế nào:** gắn câu cũ với mốc #667/trước bản cập nhật provenance; trạng thái hiện hành lấy từ `trang_thai_packet` cùng điều kiện hiệu lực. Tương tự cách PR này đã sửa lời hồi thuật `nang_tran` ở dòng 226. Nếu cần sửa erratum ngoài write set thì executor phải có authority phù hợp; reviewer không tự mở rộng scope.
- **Ca khóa:** đọc land YAML và erratum ở cùng exact head, xét cả trước và sau mốc hiệu lực merge. Hai câu hiện tại không được trái nhau; câu lịch sử có mốc và quote `cau_sai` vẫn được giữ. Phép thử hiện tại đã bắt cặp mâu thuẫn nguyên văn; chưa tuyên đã triển khai validator ngữ nghĩa.
- **Rủi ro:** thay mọi “CHƯA landed” thành “đã landed” sẽ làm sai lịch sử. Sửa toàn spec để làm đồng nhất trạng thái sẽ phá băm r5. Chỉ bổ sung thời điểm/phạm vi và con trỏ.

N3 giữ slug lớp **G2/H1/K1/L1 `landed-vuot-bang-chung`** từ #667, với biểu hiện mới do đổi trạng thái mà chưa neo lại câu ở erratum. Giữ riêng cơ chế identity N2, không đếm lại hậu quả landed của N2 thành finding thứ tư.

## Lớp D — Phạm vi, nợ và đối chiếu lịch sử

Không có P3 mở mới. Đường cứng `/tmp/do650/` và ref `f8a7829` trong `doi_chieu_buoc.py` phù hợp vai trò **script tái hiện phép đo lịch sử này**, đúng input user đã cấp; nó không được quảng bá là validator portable của sản phẩm. Script chạy lại thành công. Nếu chuyển thành công cụ dùng chung sau này thì cần input paths/ref tường minh, kiểm returncode, khóa trùng YAML và completeness; đó không phải acceptance mới của PR bookkeeping. Hai mutant cho thấy rc=0 không tự là pass và boolean subset không tự là đủ steps, đã được giữ đúng trong verdict.

Các mục `khong_do_duoc` phân biệt được: GraphQL không đọc được; history 403; uploaded artifact không tồn tại theo thiết kế. “Không có artifact” đã có descriptor đếm 0 cho hai run, nên là **đo được sự vắng mặt của artifact**, không phải mơ hồ liệu endpoint đã trả dữ liệu hay chưa. Numeric rc trực tiếp chỉ có ở receipt selftest. Exact workflow source OID chưa được khai thiếu riêng là N2; các giới hạn còn lại không bị biến thành pass trong review này.

Mục `khong_do_duoc` của land YAML còn chứa chuỗi “DA DONG 16:28Z”; đọc nó như lịch sử cập nhật/disposition, không như một enum trạng thái test. Các trường `*_suy_ra` ở phần cũ và câu cập nhật 16:28Z cho thấy nguồn cũ/mới khác nhau; không tạo finding chỉ vì tên trường lịch sử chưa được xóa. Việc đóng exact workflow identity vẫn phải sửa theo N2.

Đối chiếu với verdict #667 CLI5 (`reviewed_sha=5fe6f25066636be50256450a1202fa39d8dd45df`):

| Lớp | Kết quả tại #670 CLI1 | Nối lịch sử/phép kiểm |
|---|---|---|
| `ci-danh-tinh-suy-tu-head` | **Tái mở, N2/P1** | Checkout nay đo thật; bytes definition đúng; exact definition source OID vẫn không được phân biệt. Phản chứng đọc definition từ base cho JSON identical. |
| `landed-vuot-bang-chung` | **Tái mở về tính nhất quán, N3/P2** | Dòng `nang_tran` 226 đã được neo “lúc ghi”; erratum 16–17 chưa có neo tương tự. N2 còn giới hạn cho căn cứ đổi trạng thái. |
| `skip-windows-bi-goi-chi-linux` | **Mới, N1/P1** | Ghi chú mới ở provenance so với raw log/mã frozen. |
| `authority-thieu-than-readback`, `chuyen-vai-cung-session-chua-khai` | Không mở finding mới | Disclosure raw comment/MCP/identity và cùng session còn giữ; không tự xác thực lại authority online. |
| `acceptance-doi-khong-revision` | Giữ disposition owner | A14 r5 vẫn ghi không đạt; spec hash không đổi, không revision hồi tố. |
| `validator-land-chua-co` | Giữ nợ #669 | YAML vẫn khai LAND-EVIDENCE-VALIDATOR, owner quyết ngày 28-09, ngoài bookkeeping. Không bắt #670 triển khai validator để vá lời khai. |

**3 lớp mở / 3 biểu hiện:** 1 lớp mới, 2 lớp nối/tái mở từ #667; mức cao nhất P1. Không tính tỷ lệ hội tụ bằng cách ghép hai PR khác baseline; tập mở ở verdict #667 CLI5 là rỗng nên F/U=N/A. Chỉ thị user cho lượt CLI1 là authority review hiện tại; không suy allowance tương lai từ số vòng cũ.

## Đã chạy

| Command/phép đo | Mã thoát và bằng chứng | Trạng thái/phạm vi |
|---|---|---|
| `git rev-parse HEAD HEAD^{tree} origin/master`; `git show -s` các merge | 0; exact OID/tree/parents/time ở đầu và lớp A | **passed**, Git local |
| `git symbolic-ref -q --short HEAD` | 1, rỗng | Đo detached, không phải failure gate |
| `git diff --check origin/master..HEAD` | 0, không diagnostic | **passed** |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; 10 tệp, 0 chỗ chép doctrine | **passed**, không thay review ngữ nghĩa |
| `sha256sum -c <ROOT>/ops/land/pr666-wp650-provenance/SHA256SUMS-log-va-artifact.txt` tại `/tmp/do650` | 0; 12/12 OK | **passed** |
| `python3 -B /tmp/review670-r1-output/audit_facts.py` | Lần đầu 1 do parser scratch chưa nhận git.exe; lần hoàn chỉnh 0, `ALL_TARGETED_FACT_ASSERTIONS_PASSED` | **passed** đối chiếu cuối; giữ log failure harness |
| YAML UniqueLoader và duplicate control trong audit | 0; 2/2 unique, `duplicate key a line 2` | **passed** |
| `python3 -B ops/land/pr666-wp650-provenance/doi_chieu_buoc.py` | 0; 10/10 job khớp, counts như lớp A | **passed** trong scope so thân bước |
| `python3 -B /tmp/do650/buoc_mut.py` qua mutations harness | 0; 21/27, `all_in_order=false` | **passed** phản chứng đúng thuộc tính; matcher process không trả lỗi |
| `python3 -B /tmp/review670-r1-output/mutations.py` | 0; own mutation 7/8 false; deletion probe 7/7 true | Đã đo positive/negative và giới hạn completeness |
| `python3 -B /tmp/review670-r1-output/audit_extra.py` | 0; runner/command/catalog hashes khớp, 10 runtime, skipped có if | **passed** |
| `python3 -B /tmp/review670-r1-output/reproduce_findings.py` | 0; quotes N1/N3, source-ref comparison identical | Thu facts thành công; **không** phải verdict pass |
| `git --version`; `codex --version` | 0; Git 2.43.0, codex-cli 0.158.0 | Đo binary. Codex báo không tạo được PATH aliases do read-only filesystem; không có inference về runtime model. |
| Snapshot đầu/cuối | Xem khóa cuối bên dưới | Nội dung checkout/ref/index/status ở hai mốc |

**failed:** assertions ngữ nghĩa N1/N2/N3 chưa đạt theo evidence trên. Không có mandatory gate thực thi còn đỏ sau khi sửa lỗi harness reviewer. Hai phép đọc phụ có chẩn đoán riêng: một `rg` nhắc path `.claude/dev/test_catalog.py` không tồn tại (rc=2; sau đó đọc đúng `gate_lifecycle.py`), và phép thử băm command ban đầu thiếu LF khác giá trị artifact (không phải assertion pass); đã đọc `_json_bytes` dòng 85 và băm đúng bytes có LF, kết quả khớp. Không dùng các lỗi công cụ reviewer này làm finding sản phẩm.

**skipped trong evidence nguồn:** giữ đúng steps skipped của PR/master/launcher Ubuntu; Windows 17 test và Ubuntu 1 test của launcher; packet-loop bỏ qua 1 ca cùng mutant tương ứng. Chúng không phải test reviewer vừa chạy, không được nâng thành pass.

**not_run:** mọi network/fetch/GET/GraphQL/đăng verdict; full CI/selftest sản phẩm; tests Python 3.10–3.13; Windows execution mới; Ruff pin/probe và bare lint; `adr-song`; quét lease có gọi remote; release/deploy/LIVE. Scope là audit evidence bookkeeping và các phép đo bắt buộc trong assignment, không thay đổi runtime sản phẩm.

**not_measured:** GitHub PR head/base hiện hành, độc lập nguồn gốc HTTP của readback executor, exact workflow source commit theo N2, numeric rc trực tiếp ở các job không có receipt, lịch sử ruleset/legacy policy tại merge, raw authorization/human identity, inventory refs lịch sử, runtime model/effort và allowance toàn lịch sử. Không dùng việc tool local rc=0 để lấp các khoảng này.

Môi trường: Linux x86_64, kernel `6.18.44-fc-v37`, Python **3.11.15**, PyYAML **6.0.1**, Git **2.43.0**. Python review chạy `-B`; harness đặt `PYTHONDONTWRITEBYTECODE=1`, cache ngoài checkout. Không chạy heavy gate cần `core.abbrev`; không ghi config vào repo. OID/băm đều lấy dạng đầy đủ.

Băm hai YAML đã đọc: provenance `a8c0661ff9fcd8da05b0041fd0b98e9063c515682afd30b0521150a308c15ad9`; land evidence `4e45d8b4d042ae65ef27d75f8b76f76a9b2ad6ee4561517d87b1a28245b674ba`. Full binary diff SHA-256 `b4a81cca27d12b5e48b657e8f24c3bc6152a5cfe7eaf7b09b3b241ff1c55f943`. Hash đảm bảo bytes đối chiếu, không xác minh tác giả HTTP.

Verdict chỉ ghi tệp `-o` theo assignment. Chưa đăng GitHub, không có delivery receipt được tự nhận hoàn tất. Không commit, push, merge, gọi mạng hoặc ghi checkout được review.

**Khóa cuối:** `python3 -B /tmp/review670-r1-output/run_checks.py end` **rc=0**, `SNAPSHOT_UNCHANGED 2384`. Băm nội dung **2384 tracked paths**, HEAD/tree/base, refs, diff/index, full PR diff, untracked/ignored đều giữ nguyên so mốc đầu; `.codex/` vẫn rỗng. Không mở/snapshot repo nguồn ngoài checkout. Kết quả chỉ chứng minh không có delta ở hai mốc quan sát, không chứng minh chưa từng ghi rồi hoàn nguyên trong toàn lịch sử tiến trình.
