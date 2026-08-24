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
và `git push`, thay vì dựng prefix rule theo tên generation branch. Phép đo nền là bảy
lượt Codex Executor có mount `.git` chỉ-đọc nhưng packet vẫn được land qua phiên điều
phối; giữ quyền Git mutation riêng cho Claude sẽ biến một tình cờ sandbox thành bất đối
xứng thiết kế. Hệ quả vận hành: Executor do launcher spawn chỉ sinh working-tree diff;
phiên điều phối áp dụng/commit/push sau readback. Nhu cầu để Executor tự stage, commit hoặc
push phải đi qua Packet revision mới, không được nới allowlist của lượt chạy.

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

Chốt này phải parse nhóm cờ quyền/sandbox theo grammar từng CLI rồi chỉ nhận đúng
tên+giá trị của tuple §3; không dùng blacklist substring. Cờ quyền mới/không biết là
`KHONG_DO_DUOC` và chặn. Như vậy một alias mới không lọt chỉ vì chưa có trong danh sách cấm.

## 5. Nghiệm thu successor — đo argv cuối và process thật

`N10a`, `N10b` và `N11`–`N13` chạy qua `launcher run` với child ghi argv/đầu vào và
số lần spawn; không kiểm một biến trung gian hay chỉ grep mã. Riêng `N10c`/`N10d`
**cấm child giả**: phải gọi executable `codex` thật đã ghi version, qua chính
`launcher run`, và đo kết quả của một lần ghi thật trong workspace fixture.

Fixture là một clone tạm độc lập, có fingerprint trước-run và sentinel vắng. Hai lượt
dùng cùng binary/provider `openai_codex`, cùng workspace đã khôi phục về đúng fingerprint,
cùng prompt yêu cầu thực hiện đúng một write probe tạo sentinel với byte đã chốt; chỉ hai
trường `role` và `capability_profile` được đổi. Output process phải có positive evidence
write probe đã được thử. Thiếu evidence đã thử, thiếu credential/process thật, hoặc nền
không cho chạy sandbox lồng nhau là `KHONG_DO_DUOC` và **chặn**, không được tính là pass.

Mỗi tính chất có đột biến riêng chạy trên bản sao tạm, không dùng `.pyc` cũ. Với
`N10c`/`N10d`, đột biến hạ phép đo xuống argv hoặc thay `codex` bằng child giả phải làm
ca đích đỏ vì mất marker process thật và kết quả write probe.

| ID | phép đo dương/âm bắt buộc | đột biến phải chết |
|---|---|---|
| `N10a` | Claude Executor nhận `acceptEdits`, đúng 15 argv riêng của allowlist §4 và prompt đúng một lần ở vị trí cuối | nối allowlist thành một token, bỏ `--allowedTools`, thêm lại một Git mutation verb, hoặc dời cờ kết thúc để prompt bị nuốt |
| `N10b` | `acceptEdits` có nhưng allowlist vắng/rỗng ⇒ chặn, child spawn `0` lần | coi mode là đủ quyền |
| `N10c` | Process Codex Executor thật nhận đúng `-s workspace-write`, thử write probe và sentinel xuất hiện với đúng byte; không xuất hiện/sai byte ⇒ ĐỎ | hạ xuống chỉ đo argv/dùng child giả, hoặc cấp `read-only` |
| `N10d` | Process Codex Reviewer thật nhận đúng `-s read-only`, thử cùng write probe nhưng bị từ chối; sentinel vẫn vắng và fixture giữ nguyên fingerprint; ghi thành công ⇒ ĐỎ | hạ xuống chỉ đo argv/dùng child giả, hoặc cấp `workspace-write` |
| `N11` | role/provider/capability thiếu, sai chính tả, không hỗ trợ hoặc tuple chéo ⇒ chặn trước spawn | unknown đi qua hoặc fallback theo provider |
| `N12` | mọi bypass ở §3–§4 và cờ quyền xung đột ⇒ chặn trước spawn | chỉ chặn một cách viết hoặc âm thầm sửa argv |
| `N13` | caller đã truyền đúng mode/sandbox/allowlist ⇒ không thêm lần hai, prompt vẫn nguyên | duplicate cờ hoặc bắt oan đường hợp lệ |

Ca `N10c` và `N10d` là một cặp A/B duy nhất: **cùng provider, cùng binary/version, cùng
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

`issue_state` cố ý không được đóng băng trong spec. Preflight của successor phải đọc lại
Issue #302 trực tiếp từ GitHub, ghi URL + thời điểm đọc + state nhận được vào evidence;
không đọc được hoặc state không phù hợp với dependency đã khai ⇒ `KHONG_DO_DUOC` và chặn.

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

Successor M7 chỉ được cấp lease khi base của nó chứa
`8ba8acaa4d4e0f8e7a38228ab5b5f16f64cb960c` (đo bằng ancestry, không so tiền tố) và
đã quét lại effective write-set exclusion trên toàn bộ lease/ref. Va chạm với lease #298
được khai ở URL trên là một owner override đã xảy ra, **không** là tiền lệ cho lần cấp
lease kế tiếp và không được đọc thành write set hiện đã tự do.

## 7. Điều kiện dừng

- Cần sửa ngoài `launcher.py` + `launcher_test.py`, hoặc vượt 2 tệp / `+300`.
- Cần thêm một tuple provider/role/capability chưa có bằng chứng trong §3.
- Ca chỉ đọc mã, child không ghi argv/prompt thật, mutant không chạy hoặc không có răng.
- Base successor không chứa merge commit #302, hoặc chưa quét lại lease mà M7 đã được khai `ready`.
- Windows hoặc required gate vắng/skipped trên exact head, hoặc review không neo đúng SHA.
