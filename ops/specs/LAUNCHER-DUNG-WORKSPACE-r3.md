# Đặc tả packet `LAUNCHER-DUNG-WORKSPACE` — revision 3

```yaml
packet_id: LAUNCHER-DUNG-WORKSPACE
revision: 3
review_class: sensitive
successor_assurance_target: cross_approved
kind: selective_replacement_design_delta
remediation_source:
  verdict: changes_requested
  reviewed_sha: 51745d9d64c2205dfc336b13995c891746c4354e
  reviewed_tree: 28f657d968763ab490b1b517613bfa0907a8b72c
  pre_patch_sha256: c5f6c905315e9700140bde2f162d024174f1581b06126bc3aec39684b9f9d0a4
  evidence: https://github.com/ducthangho/tra-luat/pull/299#issuecomment-5393428338
```

> `r3` không phải lease và không triển khai launcher. Nó chỉ thay phần thiết kế `M7`
> của revision 2 để một successor Packet có thể được đóng băng, cấp lease và đo đúng
> ranh giới vai trò. `M1`–`M6` đã land giữ nguyên.
> Verdict nguồn của PR #299 ghi `cross_provider_review_performed: true`, nhưng kết quả là
> `changes_requested` và `assurance_result: not_approved`; spec này không khai achieved
> assurance. Successor `sensitive` vẫn giữ target `cross_approved`; assurance đạt được chỉ
> sống ở verdict/receipt của exact head sau này, và fallback khác cần authority mới.
>
> Hai đầu vào bất biến không được sửa đè:
>
> - `ops/specs/LAUNCHER-DUNG-WORKSPACE.md` —
>   `sha256 94351fd0e6e0d788ddf4a13ac03b0c9a7cd82e65a44905df77a9106dff171957`;
> - `ops/specs/LAUNCHER-DUNG-WORKSPACE-r2.md` —
>   `sha256 0f66976a96f327e00e76c8ef53213559d4f323b06b1609fff1cf41fc784d0afc`.

## 1. Delta có hiệu lực

`r3` thay toàn bộ bảng cho phép và `N10`–`N13` của `r2`. Các câu trong `r2`
gọi `acceptEdits` là allowlist, chọn sandbox chỉ theo provider, để ngân sách M7
chưa xác định hoặc neo protocol bằng số dòng đều không còn được dùng để cấp lease.
Tên `selective_replacement_design_delta` khai đúng phạm vi ấy: thay có chọn lọc các
khối nêu trên, không phải một addendum chỉ nối thêm và cũng không thay phần còn lại của `r2`.

Đối với successor M7, target `cross_approved` cố ý chỉ có **một orientation**:
Executor `anthropic_claude` → Reviewer `openai_codex`. Chiều Executor `openai_codex` →
Reviewer `anthropic_claude` không được thiết kế này hứa hỗ trợ, vì tuple Reviewer Claude
vẫn fail-close ở §3; đây là giới hạn chủ ý, không phải lời khai cross-review đối xứng.

Successor vẫn chỉ được sửa:

```text
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

Không sửa cấu hình người dùng, workflow, packet-loop, release artifact hoặc LIVE.

## 2. Số as-built và ngoại lệ trần có nguồn bền

Số dưới đây là GitHub PR facts trên exact head, không phải ước lượng trong spec:

| Packet | exact head đã land | as-built | trần và nguồn ngoại lệ |
|---|---|---:|---|
| #276 / [PR #289](https://github.com/ducthangho/tra-luat/pull/289) | `14e1f876a9d4b5211fa98a77703b81f0302f92e3` | 5 tệp, `+456/-15` | `3 → 5` tệp ở [lease gốc](https://github.com/ducthangho/tra-luat/issues/276#issuecomment-5385346373); `420 → 460` dòng tại [đính chính](https://github.com/ducthangho/tra-luat/issues/276#issuecomment-5386780171) |
| #290 / [PR #291](https://github.com/ducthangho/tra-luat/pull/291) | `f084aa3c338d1003e42a2e2c2ea43740d1917a16` | 6 tệp, `+775/-13` | `3 → 6` tệp tại [đính chính phạm vi](https://github.com/ducthangho/tra-luat/issues/290#issuecomment-5386185492); `400 → 520 → 750 → 800` dòng tại [520](https://github.com/ducthangho/tra-luat/issues/290#issuecomment-5387315426), [750](https://github.com/ducthangho/tra-luat/issues/290#issuecomment-5387912159) và [800](https://github.com/ducthangho/tra-luat/issues/290#issuecomment-5389210737) |
| #292 / [PR #294](https://github.com/ducthangho/tra-luat/pull/294) (`r1`) | `1dc99491bccd247c97f68e49ffeb9a74bef7d42e` | 2 tệp, `+321/-4` | `300 → 330`, chủ kho ghi tại [Issue #292](https://github.com/ducthangho/tra-luat/issues/292#issuecomment-5389910051); biên nhận land tại [Issue #292](https://github.com/ducthangho/tra-luat/issues/292#issuecomment-5390229922) |

Ngoại lệ của packet trước không truyền sang successor. M7 dùng base đã chứa PR #294,
giới hạn riêng **2 tệp / tối đa 300 dòng thêm** tính từ merge-base của successor.
Vượt trần phải dừng xin một ngoại lệ mới có URL bền; không cộng `+321` của packet đã
land vào delta mới và cũng không lấy ngoại lệ cũ làm tiền lệ.

Hai bộ đếm `hinh_dang_ke_thua` trong r1/r2 là snapshot lịch sử, không phải đầu vào
được mang sang lease mới. Giá trị hiện tại là **`KHONG_DO_DUOC`** vì chưa có phép trích
tất định kèm nguồn đầy đủ; successor không được chép lại `6` hoặc dùng nó làm gate.

## 3. M7 — chọn theo role + provider + capability

Launcher nhận ba trường đã được Packet/lease đóng băng:

```yaml
role: executor | reviewer
provider: anthropic_claude | openai_codex
capability_profile: executor_workspace_write | reviewer_read_only
```

Executable là ánh xạ đóng `anthropic_claude → claude`, `openai_codex → codex`; tên
binary không được dùng thay provider identity hoặc làm fallback khi provider không rõ.

Chỉ ba tuple sau được hỗ trợ. Mọi tuple khác, trường thiếu hoặc giá trị không biết phải
chặn **trước khi spawn**; launcher không được suy role từ tên run và không được hạ
capability theo mặc định của CLI.

| role | provider | capability_profile | argv quyền bắt buộc |
|---|---|---|---|
| `executor` | `anthropic_claude` | `executor_workspace_write` | `--permission-mode acceptEdits` **và** `--allowedTools` thực ở §4 |
| `executor` | `openai_codex` | `executor_workspace_write` | `codex exec ... -s workspace-write` |
| `reviewer` | `openai_codex` | `reviewer_read_only` | `codex exec ... -s read-only` |

`reviewer + anthropic_claude` chưa có transport read-only đã đo trong thiết kế này, nên là
**unsupported/fail-closed**, không được mượn cấu hình Claude Executor. Một Packet khác
có thể bổ sung tuple ấy sau khi có capability evidence và phản chứng riêng.

Người gọi truyền một cờ quyền/sandbox xung đột với tuple thì launcher từ chối, không
âm thầm thay, thêm lần hai hoặc chọn cờ “gần đúng”. Với Codex Reviewer, mọi dạng
`workspace-write`, `danger-full-access` hoặc bypass sandbox đều bị từ chối.

## 4. Claude Executor: mode không phải allowlist

`acceptEdits` chỉ là **permission mode**. Nó không chứng minh công cụ nào được phép.
Claude Executor chỉ được spawn khi argv chứa đúng allowlist per-run tối thiểu sau:

```text
Read
Glob
Grep
Edit
Write
Bash(git status:*)
Bash(git diff:*)
Bash(git log:*)
Bash(git show:*)
Bash(git rev-parse:*)
Bash(git merge-base:*)
Bash(python:*)
Bash(python3:*)
Bash(py:*)
Bash(rg:*)
```

Đây là **15 phần tử argv riêng biệt** đứng sau đúng một `--allowedTools`, không phải một
token nối bằng dấu cách/phẩy và không phải mô tả prose. Mỗi dòng, kể cả
`Bash(git status:*)` có khoảng trắng bên trong, là đúng một phần tử argv; lớp spawn truyền
list đối số trực tiếp, không ghép thành chuỗi để shell tách lại.

Revision này chọn hướng **(b)** cho `STD-299-02`: gỡ hẳn ba verb `git add`, `git commit`
và `git push`, thay vì dựng prefix rule theo tên generation branch. Đây là quyết định
**thu hẹp affordance**: bỏ ba cách viết tiện tay, không phải cổng tước thẩm quyền Git.
Nguồn bền tra được chỉ là `C6` tại `ops/TONG_HOP_PHAT_HIEN_20260820.md:142`, ghi **2 lượt**
Codex Executor gặp `.git` chỉ-đọc ngày 20-08-2026; nó là tiền lệ vận hành, không phải ràng
buộc vĩnh viễn. `docs/GOI_AGENT_DA_NEN.md:335` còn chứng minh mặc định ấy có thể được nới.

Chính bốn rule `Bash(python:*)`, `Bash(python3:*)`, `Bash(py:*)`, `Bash(rg:*)` bao trùm
khả năng gọi script thực hiện ba verb đã gỡ; `rg --pre` cũng chạy được chương trình ngoài.
Vì vậy ý định vận hành là Executor bàn giao working-tree diff để phiên điều phối readback
rồi commit/push, nhưng đó **không phải hệ quả an ninh** của allowlist. Hook, kiểm effective
write set và branch protection mới là các tầng phải cưỡng chế quyền thật, độc lập với
affordance này. Nhu cầu chính thức cho Executor tự stage/commit/push phải đi qua Packet
revision mới; không được nới allowlist của lượt chạy.

Nhu cầu thêm công cụ/câu lệnh phải nằm trong Packet revision mới; successor không được
sao toàn bộ allowlist rộng của `.claude/settings.json` để “cho chắc”. Hook và write set
vẫn là các lớp độc lập; allowlist không tự biến thành security boundary.

Thứ tự argv canonical:

```text
claude -p --model <model> --effort <effort>
  --permission-mode acceptEdits
  --allowedTools <15-argv-rieng-cua-danh-sach-tren>
  --output-format json
  <prompt-argument-chua-{PROMPT_FILE}>
```

`--output-format json` là cờ một giá trị kết thúc vùng nhận-nhiều-giá-trị trước prompt.
Prompt phải là đúng một positional cuối, còn nguyên byte sau thay `{PROMPT_FILE}`.
Không đặt `--allowedTools` ngay trước prompt. Nếu CLI/version không parse được bố cục
này thì trạng thái là `KHONG_DO_DUOC` và chặn, không đổi sang stdin theo suy đoán.

Các dạng `bypassPermissions`, `--dangerously-skip-permissions` hoặc alias giải ra
chế độ bỏ qua quyền đều bị chặn trước spawn. `acceptEdits` có mặt mà `--allowedTools`
vắng/rỗng cũng bị chặn.

Chốt phải parse **toàn bộ argv** theo grammar từng CLI và chỉ nhận schema đóng về vị trí,
tên, arity và giá trị mà launcher sinh/nhận cho tuple §3; không có passthrough
`argparse.REMAINDER` tổng quát. Token/cờ ngoài schema, dù chưa được phân loại là cờ quyền,
đều là `KHONG_DO_DUOC` và bị chặn trước spawn. Riêng Codex, `-c`/`--config`, `-p`/`--profile`,
`--enable` và `--disable` đều bị chặn cho tới khi một Packet revision allowlist đúng
tên+giá trị cần thiết. Như vậy cấu hình sandbox không lọt qua một cờ chưa được người viết
blacklist nghĩ tới.

## 5. Nghiệm thu successor — tách gate hồi quy và bằng chứng năng lực

Hai câu hỏi sau thuộc hai tầng khác nhau; gộp chúng vào một required suite sẽ làm cổng
phụ thuộc credential thay vì đo hồi quy launcher:

| câu hỏi | tầng | cần credential? |
|---|---|---|
| CLI có thật sự cưỡng chế sandbox không? | năng lực | **có** |
| launcher có sinh đúng argv/schema không? | hồi quy, required gate | **không** |

Required gate trong `.claude/dev/launcher_test.py` cùng mutation suite phải **offline và
tất định**. `N10a`, `N10b`, `N11`–`N13`, `N10c-hq` và `N10d-hq` chạy qua
`launcher run` với child ghi argv/đầu vào và số lần spawn: chúng đo argv cuối, schema đóng
trên toàn bộ argv, xung đột và mutation mà không cần credential. Child ghi argv chỉ hợp lệ
ở tầng này và không bao giờ là bằng chứng hoàn tất `N10c-nl`/`N10d-nl`.
Ca process thật không thuộc required gate ngay từ đầu; vắng credential ở gate này vì vậy
không phải một ca bị bỏ qua trá hình, và suite không được rẽ nhánh hay báo pass cho ca ấy.

Route đo `N10c-nl`/`N10d-nl` **chưa tồn tại**; workflow hiện hành không gọi Codex và đo tay
ad-hoc không phải biên nhận nghiệm thu. Dựng route cùng validator là packet riêng mang nợ
`NO-LUC-N10-NL-ROUTE`. Cho tới khi nợ ấy land, cả hai ID là `KHONG_DO_DUOC` và **chặn
nghiệm thu successor**, không chặn required gate. Hai chốt khác nhau: gate offline vẫn có
thể xanh, nhưng successor chưa được nghiệm thu; không đưa credential vào gate để đổi điều đó.

Route tương lai phải xuất artifact `launcher-m7-capability`, tệp `evidence/receipt.json`.
Biên nhận tối thiểu có `schema_version: 1`, `successor_sha`, `executable_path`,
`executable_version`, `provider: openai_codex`, `fixture_before_sha256`, `sentinel_path`,
`sentinel_sha256` và `cases`; `cases` chứa đúng hai ca, mỗi ca có `id` (`N10c-nl` hoặc
`N10d-nl`), `role`, `capability_profile`, `argv`, `tool_call`, `tool_result`,
`sentinel_present`, `fixture_after_sha256` và `verdict`.
Validator bắt buộc là `python ops/validate_launcher_capability_receipt.py <receipt> <sha>`;
script này cũng thuộc nợ trên và hiện chưa tồn tại, nên trước khi lệnh có thật và trả `rc=0`,
biên nhận không được công nhận và trạng thái vẫn là `KHONG_DO_DUOC`.

Phép đo năng lực **cấm child giả**: phải gọi executable `codex` thật qua chính
`launcher run` và đo một lần ghi thật.

Fixture là một clone tạm độc lập, có fingerprint trước-run và sentinel vắng. Hai lượt
dùng cùng binary/provider `openai_codex`, cùng workspace đã khôi phục về đúng fingerprint,
cùng prompt yêu cầu thực hiện đúng một write probe tạo sentinel với byte đã chốt; chỉ hai
trường `role` và `capability_profile` được đổi. Event stream `codex exec --json` phải có
tool-call máy đọc được (`apply_patch` hoặc write tool tương đương) với target+payload đúng
sentinel, kèm tool-result tương ứng; lời tự thuật văn xuôi rằng đã thử không phải evidence.
Thiếu cặp event ấy, credential/process thật, hoặc nền không cho chạy sandbox lồng nhau là
`KHONG_DO_DUOC` và **chặn nghiệm thu successor**, không được tính là pass; required gate
xanh không thay được biên nhận này. ID năng lực không phải bước required-gate; nếu hệ CI
biểu diễn nó là `skipped` thì vẫn không phải pass và không gỡ chặn nghiệm thu. Biên nhận
hạ xuống argv-only hoặc child giả không hợp
lệ vì thiếu marker process thật và cặp event/result. Ở tầng hồi quy, thiếu assertion máy
đọc được về argv/schema hoặc mutation tương ứng thì required gate không được xanh bằng prose.

Mỗi tính chất hồi quy có đột biến riêng chạy trên bản sao tạm, không dùng `.pyc` cũ.
Với biên nhận năng lực `N10c-nl`/`N10d-nl`, evidence bị hạ xuống argv hoặc thay `codex` bằng
child giả phải bị bộ kiểm bác vì mất marker process thật và kết quả write probe.

| ID | tầng / required gate | phép đo dương/âm bắt buộc | đột biến phải chết |
|---|---|---|---|
| `N10a` | hồi quy / có | Claude Executor nhận `acceptEdits`, đúng 15 argv riêng của allowlist §4 và prompt đúng một lần ở vị trí cuối | nối allowlist thành một token, bỏ `--allowedTools`, thêm lại một Git mutation verb, hoặc dời cờ kết thúc để prompt bị nuốt; mutant verb chỉ đo chuỗi allowlist, không đo thẩm quyền tương đương |
| `N10b` | hồi quy / có | `acceptEdits` có nhưng allowlist vắng/rỗng ⇒ chặn, child spawn `0` lần | coi mode là đủ quyền |
| `N10c-hq` | hồi quy / có | argv cuối có đúng `-s workspace-write` và toàn schema đóng | đổi sandbox/schema phải làm required gate đỏ |
| `N10c-nl` | năng lực / không | process Codex Executor thật thử write probe, sentinel xuất hiện đúng byte; vắng/sai ⇒ ĐỎ | hạ biên nhận xuống argv/child giả hoặc cấp `read-only` không được công nhận |
| `N10d-hq` | hồi quy / có | argv cuối có đúng `-s read-only` và toàn schema đóng | đổi sandbox/schema phải làm required gate đỏ |
| `N10d-nl` | năng lực / không | process Codex Reviewer thật thử cùng write probe nhưng bị từ chối; sentinel vắng, fixture nguyên fingerprint; ghi được ⇒ ĐỎ | hạ biên nhận xuống argv/child giả hoặc cấp `workspace-write` không được công nhận |
| `N11` | hồi quy / có | role/provider/capability thiếu, sai chính tả, không hỗ trợ hoặc tuple chéo ⇒ chặn trước spawn | unknown đi qua hoặc fallback theo provider |
| `N12` | hồi quy / có | toàn argv ngoài schema đóng ⇒ chặn trước spawn `0` lần; tối thiểu thử `-c 'sandbox_workspace_write.writable_roots=[...]'`, `--config`, `-p`/`--profile` và `--enable`/`--disable` | chỉ lọc `-s`, chỉ chặn một cách viết, cho `REMAINDER` đi qua hoặc âm thầm sửa argv |
| `N13` | hồi quy / có | caller đã truyền đúng mode/sandbox/allowlist ⇒ không thêm lần hai, prompt vẫn nguyên | duplicate cờ hoặc bắt oan đường hợp lệ |

Ca `N10c-nl` và `N10d-nl` là một cặp A/B duy nhất: **cùng provider, cùng binary/version, cùng
workspace fixture/fingerprint và cùng write probe**, chỉ đổi role + capability. Bằng chứng
phải có cả argv exact và hai kết quả ghi ngược nhau; hai argv khác nhau tự chúng chưa đủ.
Nếu chỉ chạy riêng từng ca, không chứng minh write probe đã được thử, hoặc không đối chiếu
fingerprint thì chưa chứng minh launcher cưỡng chế capability theo role.

## 6. Dependency hồi quy packet-loop — đã land, có khai va chạm

Fact phiên bản hiện hành sau quyết định land của chủ kho:

```yaml
issue: 302
pull_request: 303
pr_head_sha: 77f3c4361c8a9a12f514dd3b7440109da706ad62
merge_commit: 8ba8acaa4d4e0f8e7a38228ab5b5f16f64cb960c
merge_tree: e8a23968d92b63f14bfffe23d83bce506f168915
status: landed_with_declared_owner_override_and_lease_collision
cross_review: https://github.com/ducthangho/tra-luat/pull/303#issuecomment-5392476465
declared_lease_collision: https://github.com/ducthangho/tra-luat/issues/298#issuecomment-5392499800
```

`issue_state` cố ý không được đóng băng trong spec. Preflight của successor đọc lại Issue
#302 trực tiếp từ GitHub và ghi URL + thời điểm + state vào evidence **chỉ để audit**;
state ấy không phải vị ngữ dependency. Cổng có thể ĐỎ là phép ancestry exact-SHA bên dưới
cộng phép quét effective write-set trên toàn bộ lease/ref; thiếu một trong hai phép đo là
`KHONG_DO_DUOC` và chặn.

PR #303 bắt đầu là hiện vật **pre-lease**, nên lịch sử cũ từ chối dùng nó làm authority
cho một implementation Codex generation 2 là đúng tại thời điểm đó. Owner sau này đã
land exact head ấy; merge commit và tree trên là **version authority** chứng minh bản vá
đã vào `master`, nhưng không hồi tố execution lineage:

- PR #303 không phải implementation Codex generation 2 và không được đổi nhãn thành vậy;
- Codex generation-2 attempt bị supersede, dừng trước commit/push; nó không tạo completion evidence;
- quan sát TOCTOU của attempt Codex chỉ là advisory hoặc đầu vào cho successor improvement,
  không phải bằng chứng đóng dependency;
- cross-review exact head của PR #303 chứng minh review của byte đã land, không chứng minh
  một lineage Codex generation 2 chưa từng tạo commit.

Successor M7 chỉ được cấp lease khi lệnh `git merge-base --is-ancestor
8ba8acaa4d4e0f8e7a38228ab5b5f16f64cb960c <successor-base>` trả `rc=0` và đã quét lại
effective write-set exclusion trên toàn bộ lease/ref; `rc` khác `0` hoặc không chạy được
đều chặn. Va chạm với lease #298
được khai ở URL trên là một owner override đã xảy ra, **không** là tiền lệ cho lần cấp
lease kế tiếp và không được đọc thành write set hiện đã tự do.

## 7. Điều kiện dừng

- Cần sửa ngoài `launcher.py` + `launcher_test.py`, hoặc vượt 2 tệp / `+300`.
- Cần thêm một tuple provider/role/capability chưa có bằng chứng trong §3.
- Với `N10a`/`N10b`/`N11`–`N13`, child không ghi argv+prompt cuối thật, mutant không chạy
  hoặc không có răng.
- Với `N10c-hq`/`N10d-hq`, argv/schema hoặc mutation offline không có assertion
  máy đọc được ⇒ required gate đỏ; credential không phải đầu vào của tầng này.
- Với `N10c-nl`/`N10d-nl`, route/validator chưa land, không gọi được process Codex thật,
  hoặc event `--json` không chứng minh bằng máy write probe đã được thử ⇒
  `KHONG_DO_DUOC` và chặn nghiệm thu successor, không chặn required gate; cấm tính
  `skipped` là pass, dùng gate xanh hoặc hạ xuống child/argv-only để thay biên nhận.
- Phép ancestry exact SHA #302 không trả `rc=0`, hoặc chưa quét lại toàn bộ lease/ref mà
  M7 đã được khai `ready`.
- Windows hoặc required gate vắng/skipped trên exact head, hoặc review không neo đúng SHA.
