# Protocol đa phiên Claude–Codex

- **Trạng thái:** Thiết kế đã chốt qua grilling ngày 2026-08-03
- **Protocol version:** 1
- **Governance baseline:** MCR-54-02, chấp thuận ngày 2026-08-08
- **Phạm vi:** Claude Code, Codex, Windows local, cloud worker và Android
- **Nguồn quyết định:** ADR-0017 đến ADR-0035
- **Kế hoạch thi công:** `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`

## 1. Mục tiêu và bất biến

Hệ thống cho phép nhiều agent run tự xử lý một mission đến `awaiting_land` mà không cần người dùng gõ lại prompt;
người có thẩm quyền có thể apply exact head SHA và hoàn tất mission từ local, web hoặc Android. GitHub Issue/PR
là control plane và nguồn trạng thái bền; Claude, Codex, ứng dụng desktop/mobile và local controller chỉ là các
giao diện/executor có thể thay thế.

Các bất biến không được hạ chuẩn:

1. Mỗi work packet có đúng một executor ghi và một lease generation còn hiệu lực.
2. Mỗi lần chạy có branch/worktree riêng; không có hai lease với effective write set giao nhau trên toàn repo.
3. Worker không ghi canonical, không bump version, không deploy và không có credential LIVE.
4. Dispatcher tuần tự là bên duy nhất chuyển state/cấp lease/merge vào mission integration branch.
5. Canonical chỉ đổi qua operation `land apply` được người có thẩm quyền gọi cho đúng mission/head SHA; mọi
   skill, comment hoặc workflow chỉ là client. Deploy là cổng riêng.
6. Mọi text tracked dùng LF, trừ `*.cmd`/`*.bat` dùng CRLF; binary/golden byte fixture không normalize.
7. Chat history, label, assignee và board không phải nguồn sự thật.
8. Một phiên chỉ giữ một vai trò trên một đơn vị công việc: execute một Packet, review một PR hoặc land một
   exact head. Substep nằm trong cùng Packet Spec không bị tách vụn; việc ngoài spec sang successor Packet.
9. Review, CI, authorization và land evidence đều gắn exact SHA. Head đổi làm bằng chứng và ủy quyền cũ hết hiệu lực.
10. GitHub durable facts và deterministic reconciler single-writer là authority cho transition; model, adapter,
    workflow trigger và prompt chỉ là worker/client có thể thay thế, không tự cấp quyền hoặc tự nối chuỗi vai trò.

## 2. Thành phần và quyền

| Thành phần | Được làm | Không được làm |
|---|---|---|
| Dispatcher/reconciler | Reconcile durable inbox, chuyển state, cấp/thu hồi lease, tạo packet/branch/PR, merge tuần tự vào integration | Ghi canonical, chạy LIVE, tự tăng budget/quyền |
| Executor | Sửa đúng effective write set trên branch của generation, tạo PR/handoff | Sửa branch khác, file land/security, tự review/approve, merge dưới vai Executor, deploy |
| Reviewer | Đọc code, chạy kiểm tra read-only trên exact SHA, ghi verdict/comment | Dùng worktree ghi của Executor, push hoặc sửa branch |
| Local controller | Nhận packet local, tạo worktree, gọi CLI headless, heartbeat/handoff | Làm generic runner, giữ credential LIVE |
| Phiên land | Tích hợp, gán version, changelog, manifest, chạy land gate | Tự cấp approval; deploy ngầm |
| Approver | Chấp nhận exact mission/head SHA và điều kiện land bằng authorization bền | Tạo quyền qua output agent, duyệt head khác hoặc bỏ qua finding/check chưa đóng |
| Land Operator | Thực hiện đúng prepare/apply đã được ủy quyền và ghi land evidence | Tự chọn head, tự nới điều kiện hoặc coi thao tác của mình là review/approval |
| Apply job | Kiểm mission/head SHA/gate/approval rồi merge đúng draft land PR | Gọi model, sửa diff, chọn head khác, deploy |
| Người có thẩm quyền | Start/pause/resume/reroute/override/authorize/apply/deploy | Thẩm quyền không được chuyển qua output của agent; chỉ có thể ủy quyền bền, có phạm vi và điều kiện |

Một người hoặc agent có thể giữ các vai ở những phiên khác nhau, nhưng assurance không được nhập nhằng. Executor có
thể làm Land Operator khi authorization cho exact SHA cho phép; việc đó không biến họ thành Reviewer hay Approver
độc lập của chính diff. Reviewer cùng provider với Executor phải là phiên mới, read-only và được ghi mức assurance
thấp hơn cross-provider.

## 3. Nguồn sự thật và schema

### 3.1 Mission Issue

Mission được tạo từ Issue Form, tối thiểu có:

```yaml
schema_version: 1
mission_id: gh-<issue>
revision: 1
plan_hash: <sha256>
supersedes_revision: null
change_request: null
base_sha: <canonical-sha>
objective: <mục tiêu>
acceptance_criteria: []
risk: normal | sensitive
requires_live: false
envelope:
  max_packets: 20
  max_successor_depth: 5
  max_attempts_per_packet: 3
  max_run_minutes: 45
  same_failure_limit: 2
  max_parallel_workers: 2
  max_agent_invocations: 30
  max_cloud_minutes: 360
  max_inbox_backlog: 100
  provider_budgets: {}
```

Trạng thái mission: `proposed`, `running`, `paused`, `blocked`, `awaiting_land`, `complete`, `cancelled`. `plan_hash`
đóng băng objective, acceptance, risk, requires_live, envelope và seed/constraint của Packet plan. Successor nằm
trong outcome/envelope đã duyệt được nối bằng event bền mà không tự tạo Mission revision; đổi phase graph,
dependency chuẩn hoặc constraint material vẫn cần MCR. Label chỉ phản chiếu state; revision/plan hash và event
journal mới là căn cứ.

#### 3.1.1 Mission Change Request

Thay đổi material của Mission Plan không được sửa im lặng vào body đang chạy. Một Change Request bền tối thiểu có:

```yaml
schema_version: 1
change_request_id: mcr-<mission>-<sequence>
mission_issue: <number>
requested_by: <actor>
reason: <text>
proposed_changes: []
affected_packets: []
landed_work_impact: none | corrective_packet | revert_packet
risk_change: none | increased | decreased
decision: pending | approved | rejected
decision_source: human
approved_by: <human-actor-or-null>
decision_url: <durable-url-or-null>
supersedes_revision: <integer>
```

Dispatcher chuyển phần bị ảnh hưởng sang `paused: change_requested`, ngừng cấp lease/merge, rồi lập impact analysis:
Packet không ảnh hưởng được giữ; Packet đổi objective/acceptance/write-set/dependency/executor/environment phải có
revision và generation mới; Packet không còn cần chuyển `cancelled`; kết quả đã landed chỉ được sửa bằng corrective
hoặc revert Packet. MCR material chỉ có hiệu lực khi human ghi quyết định bền cho exact Change Request; ủy quyền land
không đồng thời là quyền duyệt MCR.

Sau quyết định `approved`, dispatcher atomically ghi event cài Mission revision/plan hash mới, thu hồi mọi lease bị ảnh
hưởng, tăng generation, cài các Packet revision tương ứng, tính lại closure rồi readback state/hash. Chỉ các Mission hoặc
Packet đủ điều kiện mới chuyển `paused` về `running`/`ready`; bất kỳ bước hay readback nào hỏng thì vẫn `paused`. Quyết
định `rejected` giữ revision cũ và chỉ resume sau khi event/readback của quyết định đó khớp. Nếu outcome, quyền LIVE
hoặc security boundary đổi căn bản, tạo Mission mới và chuyển Mission cũ `cancelled: superseded` thay vì viết lại lịch sử.

### 3.2 Work Packet Issue

Packet dùng ID bền `wp<issue>` và tối thiểu có:

```yaml
schema_version: 1
packet_id: wp<issue>
mission_issue: <number>
revision: 1
spec_hash: <sha256>
objective: <một kết quả tự đủ>
write_set:
  - type: exact | prefix
    path: <repo-relative-path>
ref_set:
  - type: exact | prefix
    ref: <fully-qualified-git-ref>
depends_on: []
executor: claude | codex
environment: cloud | local
risk: normal | sensitive
acceptance_criteria: []
```

Khi vào `ready`, spec được đóng băng bằng `spec_hash`. Đổi objective, acceptance, write set, dependency, executor
hoặc environment tạo revision mới và làm lease cũ mất hiệu lực. Dispatcher bổ sung các trường phái sinh, không
cho người dùng/agent tự khai:

```yaml
change_policy_sha: <canonical-policy-sha>
effective_write_set: []
required_checks: []
land_obligations: []
```

Các trường này cùng nằm trong `spec_hash`. Policy đổi làm closure thay đổi thì packet phải tạo revision và
generation mới trước khi chạy tiếp.

`Packet Spec` là hợp đồng ở các trường trên. `Session Plan` chỉ là checklist chiến thuật của một phiên và có thể
đổi thứ tự/cách làm nếu vẫn giữ nguyên Packet Spec. Phát hiện ngoài spec phải xuất handoff/successor rồi kết thúc
phiên; agent không tự mở write set. Findings của Reviewer được sửa trong cùng Packet khi spec vẫn đủ; finding cho
thấy chính spec thiếu thì verdict là `blocked` và đi qua revision mới.

`ref_set` là phạm vi Git ref song song với phạm vi tệp của `write_set`: nó liệt kê chính xác hoặc theo prefix
những ref mà Packet được phép tạo, cập nhật hoặc xóa. Ref thực tế không được khai là vi phạm, kể cả khi diff tệp
vẫn nằm hoàn toàn trong `write_set`; `write_set` không diễn đạt được rủi ro ref. Tên ref phải ở dạng đầy đủ
`refs/...`, và validator so nó với `ref_set` chứ không suy từ branch đang checkout. Tiền lệ đo được là wp82 phải
ràng buộc các ref thu hồi bằng `acceptance_criteria` vì Packet Spec lúc đó chưa có trường máy đọc được này.

### 3.3 State projection, event journal và recovery snapshot

Dispatcher sở hữu một JSON state projection có schema version trong comment riêng. Projection giữ revision,
spec hash, state, lease, budget, review assurance và các commit/handoff liên quan; label, assignee và Project chỉ
phản chiếu nó để người dùng xem trên web/Android. Projection không phải bản sao duy nhất vì Issue comment có thể
bị update/delete.

Command/handoff phải tồn tại trước thành durable inbox fact có GitHub object ID; workflow trigger chỉ là wake-up,
không phải hàng đợi. Reconciler single-writer đọc fact chưa tiêu thụ theo `(created_at, id)`, kiểm
`expected_state_revision`/generation/spec hash và áp transition idempotent. Mỗi transition accepted nối một
state-event comment chứa event, full post-state checkpoint, `state_hash` và `prev_event_hash`, rồi mới cập nhật
projection với `last_consumed_event_id`; bot không sửa event cũ.

Workflow reconciler dùng một concurrency group với `queue: max`, `cancel-in-progress: false` chỉ để backpressure:
queue có trần và thứ tự run không phải thứ tự dispatch nên không được dùng làm nguồn đúng. Scheduled/manual
reconcile thu hồi fact khi wake-up bị hủy, queue đầy hoặc runner lỗi. Projection lệch journal được dựng lại từ
checkpoint/chain; thiếu/trùng/sai hash hay sửa/xóa fact đã consume chuyển mission sang `paused`, không đoán hoặc
lùi state. Inbox vượt `max_inbox_backlog` cũng PAUSE nhưng không xóa fact; reconciler xử lý theo page hữu hạn và
tự wake lại cho tới khi hết backlog.

Mỗi revision của mission active có recovery snapshot JSON trong workflow artifact với retention tối đa cấu hình
repo cho phép; artifact là backup có hạn, không phải nguồn sự thật. Khi apply, final state hash và mission ID được
neo vào commit canonical. Threat model này chống mất/sửa nhầm một object, không chống repository administrator
có chủ ý phá mọi bản sao. Comment, review và handoff của agent vẫn là dữ liệu, không mang thẩm quyền.

#### 3.3.1 Checkpoint hash canonical có version

Mỗi state-event sinh sau khi checkpoint schema được cài trên canonical **phải** khai
`checkpoint_schema_id`, `checkpoint_schema_version`, `state_hash_fields`, `basis_object` và `state_hash`.
Registry duy nhất cho tập trường/kiểu có thứ tự của từng `event_type` là
`.github/coordination/checkpoint-schema.v1.json`; schema của chính registry là
`.github/coordination/schemas/checkpoint-schema.v1.schema.json`. Validator stdlib phải đọc và kiểm cả hai; thiếu,
hỏng cú pháp, schema/version lạ hoặc event type không có trong registry đều fail-closed. `.github/schemas/state.schema.json`
thuộc wp60 đang blocked phải khớp `checkpoint_schema_id`/`checkpoint_schema_version` khi wp60 được unblock;
quy tắc phối hợp này không tự đổi spec, revision hay state của wp60.

`state_hash_fields` là mảng tên trường theo thứ tự lexicographic code point do registry ghim cho event type. Nó là bằng chứng đọc được, nhưng
không trao cho event quyền tự chọn tập trường. Yêu cầu cũ chỉ bắt mỗi event tự công bố `state_hash_fields` là điều
kiện cần nhưng chưa đủ: wp88 Fork A (Issue #88 comment 5264350972) công bố 48 trường và tái lập được
`3574a68d4cfc62918e6e91e0301e7d0939ca7e5cc56bb06c6f69e35b34242428`; Fork B (comment 5264354085)
công bố 26 trường và tái lập được `f16d7dffaba9c19d6b3612611b00a4158e7cc85e57f74e361b9b3460b71b247c`.
Hai event cùng predecessor `184522125afd0bf3996708784e0d5c1ca934825c11a2e085da0815216450dfac`, và validator chỉ
kiểm basis tự công bố sẽ cho cả hai pass. Registry tập trung mới làm basis canonical.

Lõi định danh chung trong registry xuất phát từ giao 20 khóa mà hai Reconciler wp88 độc lập cùng chọn và bất đồng
0 giá trị, sau khi loại hai khóa riêng của wp88 là `f2d_closed_by_wp88` và `row_12_outcome`: `base_sha`,
`generation`, `land_head_sha`, `last_consumed_event_id`, `merge_commit`, `merge_method`, `mission_issue`,
`mission_plan_hash`, `mission_revision`, `mission_state`, `next_role`, `packet_id`, `packet_issue`,
`packet_revision`, `post_merge_ci_run_id`, `prev_event_hash`, `spec_hash`, `state`. Trường mở rộng theo event type
phải có căn cứ trong hợp đồng transition/evidence (ví dụ event/fact identity, review exact SHA hoặc land
authorization) ghi ngay trong registry; Reconciler không thêm trường tùy hứng.

Basis được ghim nguyên văn, không phụ thuộc serializer mặc định của nền tảng:

```text
state_hash = SHA-256(UTF-8(compact-sorted JSON của basis_object))
compact     = separators ',' và ':', không khoảng trắng
sorted      = khóa object theo code point, lexicographic và đệ quy
array       = giữ nguyên thứ tự đã đặc tả, tuyệt đối không sort
encoding    = UTF-8 không BOM, không trailing LF
basis_object = chính xác tập trường registry của event_type
```

Thiếu một trường, thừa một trường, sai kiểu, `state_hash_fields` khác thứ tự registry hoặc hash lệch đều
fail-closed. `null`, boolean, integer, number, string, array và object giữ đúng kiểu JSON; không ép chuỗi thành số
hay coi boolean là integer. Trường giải thích/prose/disposition/ghi chú vẫn được mang ở ngoài `basis_object` làm
bằng chứng cho người đọc nhưng không được dịch chuyển head. Bằng chứng đo được từ wp88: 28 trường chỉ Fork A có,
trong đó `f04_disposition`, `f02_state`, `f04_duplicate_review_comment_id`, `open_findings`, `blocking_findings`,
`branch`, `landed_at`, `target_ref`, đã từng nằm trong hash basis dù là diễn giải hoặc metadata trình bày.

Schema v1 chỉ áp dụng tiến về trước cho event sinh **sau commit canonical cài registry**. Fork A, Fork B và repair
head `6aafeaba9f11fad6f719cfff6f5cfd07088581bf356474c7c7a3607f8684ff64` ở Issue #88 comment
5264973649 là bằng chứng lịch sử bất biến: không sửa, xóa, rút lại, tính lại theo schema mới hoặc đảo quyết định
chọn Fork B.

#### 3.3.2 Đọc lại head và xử lý sibling

Ngay trước append, Reconciler phải đọc lại head hiện tại từ **raw journal**, không dùng label hay projection. Nếu
đã có sibling cùng `prev_event_hash`, cùng `checkpoint_schema_id`/`checkpoint_schema_version` và cùng canonical
`basis_object`/`state_hash`, đó là retry idempotent: giữ một logical head và không append transition thứ hai. Nếu
cùng predecessor nhưng schema, basis hoặc hash khác, Reconciler phải fail-closed: PAUSE, ghi durable conflict,
đặt `next_role: human`; không agent tie-break, không “first append wins”, không đoán. Quy tắc này nâng bất biến
ADR-0033 “retry cùng ID không tạo transition thứ hai” lên mức hash, vì hai fork wp88 đã cùng tiêu thụ fact
5264250136 mà vẫn tạo được hai transition.

#### 3.3.3 Basis của body lấy từ GitHub

Hash body Issue/comment phải đọc trường `.body` trực tiếp từ REST JSON. Không hash JSON wrapper, output có thêm LF
hay chuỗi HTML-escaped. Đường đọc GitHub qua MCP đã được đo là có thể đổi `"` thành `&#34;` và `>` thành `&gt;`;
nếu chỉ có representation đó thì phải HTML-unescape đúng một lần để khôi phục raw body trước khi hash, nhưng đường
REST raw vẫn là chuẩn. Tiền lệ wp84 cho thấy cùng spec có hash đúng `2e07767f...` sau unescape nhưng thành
`c35a0434...` nếu hash representation đã escape.

Mọi handoff có `handoff_body_sha256` phải công bố `handoff_body_hash_basis` đủ để bên thứ ba tái lập: nguồn raw
REST `.body`; marker đầu/cuối và occurrence xác định chính xác đoạn payload; quy tắc chuẩn hóa CRLF/CR thành LF;
trường `handoff_body_sha256` được để trống theo đúng một dạng đã khai để tránh tự tham chiếu; có hay không `rstrip`;
UTF-8 có hay không BOM; marker có nằm trong basis và có trailing LF hay không. Thiếu một thuộc tính basis trên là
fail-closed, không thử nhiều biến thể rồi chọn hash tình cờ khớp. Tiền lệ wp87 cho thấy năm tập trường post-state
hợp lý vẫn không tái lập được các token `f6c79bb8...`/`a875517a...`; checkpoint không tái tính được chỉ là token
nối chuỗi, không đủ để dựng lại projection.

## 4. State machine và lease

Packet đi theo:

```text
proposed → ready → leased → running → reviewing → accepted → integrated → landed
                 ↘ paused | blocked | cancelled | stale
```

Mỗi phiên chỉ thực hiện một chuyển động có trách nhiệm rõ: execute một Packet, review một PR hoặc land một exact
head. “Một đơn vị công việc” không có nghĩa một micro-step: Executor được hoàn thành mọi substep cần thiết trong
objective/write set/acceptance của Packet. Khi xuất hiện outcome độc lập hoặc phạm vi mới, phiên ghi successor và
dừng; phiên mới nhận Packet mới. Reviewer không chuyển vai sang sửa code trong cùng phiên, và phiên land không tạo
feature diff.

Lease gồm:

```yaml
packet_id: wp<issue>
executor: claude | codex
environment: cloud | local
branch: agent/wp<issue>-g<generation>-<executor>
write_set_hash: <sha256>
generation: <integer>
heartbeat_at: <timestamp>
lease_until: <timestamp>
```

Sau 30 phút không có tiến triển, dispatcher thu hồi lease, tăng generation rồi mới reroute. Worker cũ sống lại
không thể heartbeat, push hợp lệ hoặc handoff. Branch/PR cũ chuyển `stale`; generation mới được đọc diff cũ nhưng
không tự cherry-pick. Commit SHA cuối được giữ trong state projection và event journal.

Local worktree stale được dọn khi process dừng. Remote branch/PR stale giữ đến khi mission kết thúc cộng 30 ngày;
`/packet preserve` kéo dài thời hạn. Cleanup chỉ bắt đầu sau khi báo cáo cuối và final state hash trên canonical
đã được readback khớp; artifact hết hạn không được dùng làm bằng chứng mission complete.

## 5. Write set và giảm conflict

Write set chỉ nhận đường dẫn chính xác hoặc prefix thư mục, không nhận glob tùy ý. Trước khi so giao, dispatcher:

1. đổi separator thành `/`;
2. từ chối absolute path, `.`/`..` và path thoát repo;
3. chuẩn hóa Unicode NFC;
4. case-fold để bắt va chạm trên Windows;
5. resolve symlink/parent của file mới và kiểm vẫn nằm trong worktree;
6. hash biểu diễn canonical.

Change-impact policy chuẩn ở `.github/coordination/change-impact.v1.json`, schema ở
`.github/coordination/schemas/change-impact.v1.schema.json`; cả hai thuộc security paths trên canonical. JSON
`schema_version: 1` được validator Python stdlib đọc tất định. Mỗi rule có `rule_id`, `evidence`, `owner`, hạn
dùng nếu tạm và quan hệ có hướng:

```yaml
rule_id: <stable-id>
trigger: {type: exact | prefix, path: <repo-relative-path>}
write_closure: [{type: exact | prefix, path: <repo-relative-path>}]
required_checks: []
land_obligations: []
evidence: []
owner: <team-or-role>
expires_at: <timestamp-or-null>
```

Dispatcher tính closure bắc cầu từ write set khai báo, tạo effective write set rồi mới kiểm giao nhau/cấp lease.
CI tính lại policy từ canonical và trigger từ diff để bắt khai thiếu. `write_closure` cấp quyền sửa companion nếu
cần; `required_checks` chứng minh invariant nhưng không ép file phải đổi; `land_obligations` không trao file
land-only cho worker. Với invariant hiện tại, `SKILL.md` tạm kéo `references/GOTCHAS.md` vào closure và bắt chạy
check r219, còn sửa GOTCHAS độc lập không khóa ngược `SKILL.md`; nếu pin số đo động được loại bỏ thì policy cũng
phải thu hẹp thay vì giữ coupling giả vĩnh viễn.

Effective-write-set exclusion áp dụng toàn repo, kể cả giữa hai mission. Diff ngoài tập hiệu lực bị CI từ chối.
Mở rộng phạm vi hay đổi closure là revision mới, generation mới và cấp lại lease. Khi change-impact policy đổi,
dispatcher pause và re-evaluate mọi packet chưa terminal; generation chỉ được giữ nếu closure/check/hash không
đổi. Không dùng nhóm file đối xứng để khóa rộng và không hợp thức hóa pin số đo động vốn nên được sinh hoặc bỏ.

Khi Packet land, `write_set` của revision đó khóa lại cùng lịch sử; nó không trao quyền sửa tệp vô thời hạn và tệp
đã land không mặc nhiên thuộc một worker cũ. Muốn sửa tiếp chỉ có hai đường hợp lệ: mint Packet mới sở hữu tệp,
hoặc mở rộng `write_set` của một Packet đang mở bằng revision/generation mới rồi cấp lease lại. Sửa tệp đã land
khi không Packet active nào sở hữu là vi phạm dù branch có nguồn gốc từ Packet cũ. Tiền lệ là branch
`codex/wp63-row49-behavior-evidence` sửa artifact của wp63 sau khi wp63 đã merge và không Packet nào phủ; cách xử
lý hợp lệ là đưa exact path đó vào wp82 revision 2, không hợp thức hóa quyền sở hữu ngầm của branch.

Seed foundation chạy read-only để lập candidate từ tri thức máy đã có trong `doc-claims-check`, golden và release
gate; human review từng rule trước khi ghi canonical. Nếu check phát `impact_hint` máy đọc được cho coupling ngoài
closure, ratchet chặn generation và buộc finding kết thúc bằng rule/land obligation, sinh hoặc gỡ invariant động,
hay ngoại lệ có owner/reason/expiry/human approval. Policy change đi qua packet nhạy cảm; integrate resolution rồi
mới cấp generation nội dung mới. Gate không tự sửa policy và lỗi test thường không tự biến thành coupling.
Rule/exception hết hạn phải fail tới khi được thu hẹp, xóa hoặc gia hạn có review.

`scripts/tl_selftest.py` là legacy harness dùng chung và mặc định không thuộc packet thường. Regression test mới
nằm trong file chính xác `scripts/test_fragments/wp<issue>_<slug>.py`; mỗi packet sở hữu fragment riêng và worker
gate auto-discover theo thứ tự tất định, đồng thời từ chối ID trùng. Không dùng `merge=union` cho Python hoặc cấu
hình thực thi vì phép ghép theo dòng không bảo đảm thứ tự/ngữ nghĩa. Packet cần sửa chính harness hoặc cùng chạm
`scripts/tl.py` vẫn phải chạy tuần tự; protocol không cấp lease theo vùng dòng.

Mỗi mission có `mission/<issue>/integration` từ base SHA cố định. Packet PR vào integration, không vào canonical.
Dispatcher merge tuần tự packet đã accepted. Packet có dependency chỉ chạy sau predecessor đã integrated; packet
độc lập có thể chạy song song nhưng phải rebase và chạy lại gate trước khi merge. Mỗi mission chỉ có một draft
land PR từ integration vào canonical.

## 6. Định tuyến cloud và local

`executor` và `environment` là hai trường độc lập. `cloud` là mặc định vì Windows host có thể tắt. `local` chỉ
dùng khi cần tài nguyên cục bộ, parity Windows hoặc khi người dùng chọn rõ. Dispatcher không tự đổi môi trường;
môi trường không khả dụng dẫn đến `paused`.

Cloud worker chạy trên runner tạm thời và chỉ làm offline. Packet local nằm trong hàng đợi tới khi controller
Windows trực tuyến. Controller Python chạy bằng Scheduled Task dưới tài khoản ít quyền, tạo worktree rồi gọi
`claude -p` hoặc `codex exec`. Đây là headless worker run; không hứa xuất hiện như chat trong ứng dụng. Remote của
Claude/Codex là giao diện can thiệp tùy chọn, không phải control plane và không hoạt động thay local host khi host
tắt.

GitHub Agentic Workflows (`gh-aw`) có thể được thử nghiệm như một implementation của provider adapter vì hỗ trợ
worker Codex/Claude, sandbox và safe outputs. Nó không được giữ projection, chọn transition, tự phê duyệt hoặc
thay reconciler. Khi còn public preview, workflow Markdown phải compile thành lock file được pin/review; token và
tool permission tối thiểu; input không tin cậy không đi vào job có quyền ghi; mọi write đi qua safe output đã được
validator của reconciler kiểm exact identity. Adapter phải có feature flag, kill switch, quota và đường quay về
deterministic runner mà không đổi schema/state. Không dùng chuỗi `workflow_run` làm state machine: giới hạn chain,
quyền của downstream workflow và lịch chạy không tạo ra durable ordering hay authority.

## 7. Handoff và tự sinh phiên kế nhiệm

Executor luôn xuất handoff máy đọc được:

```yaml
schema_version: 1
packet_id: wp<issue>
generation: <integer>
spec_hash: <sha256>
provider: claude | codex
role: executor
session_id: <stable-run-id>
base_sha: <git-oid>
head_sha: <git-oid-or-null>
status: done | needs_followup | blocked
summary: <text>
changed_paths: []
tests:
  - name: <gate>
    status: passed | failed | not_run
    evidence: <url-or-summary>
test_selection:
  gate_tier: T0 | T1 | T2 | T3 | T4 | T5
  selector_policy_sha: <git-oid-or-policy-hash>
  tested_sha: <git-oid>
  selected_groups: []
  full_fallback_reason: <reason-or-null>
remaining_work: []
next_role: reviewer | executor | land_operator | human | null
manual_next_action: <action-or-null>
copyable_prompt: <prompt-or-null>
failure:
  fingerprint: <stable-hash-or-null>
  category: content | quota | infrastructure | permission | null
successors:
  - successor_key: <stable-local-key>
    objective: <text>
    write_set: []
    depends_on: []
    executor: claude | codex
    environment: cloud | local
    acceptance_criteria: []
```

Executor đăng handoff/evidence lên Packet Issue và PR trước khi state rời `running`. Test evidence phải có lệnh,
rc đọc trực tiếp và bằng chứng dương (`N/N`, `ok=true`, số file/hash...), không chỉ “passed”. `changed_paths` phải
khớp diff của exact `head_sha`; `tested_sha` phải bằng head được đề nghị review; test không chạy phải ghi
`not_run` cùng lý do. Selector evidence phải ghi tier, policy/catalog identity, nhóm đã chọn và lý do fallback;
không được chỉ ghi “affected tests passed”.

Khi dispatcher/reviewer automation chưa được promote, mỗi phiên còn phải điền `next_role`,
`manual_next_action` và `copyable_prompt` đủ để người giữ tạo một phiên Claude/Codex mới. Prompt phải neo
mission/packet/revision/generation/exact SHA, vai trò, phạm vi, gate và stop conditions; nó là tiện ích bootstrap,
không phải lease, approval hay authority. Mẫu chuẩn ở `docs/prompts/MANUAL_SUCCESSOR_HANDOFF_D0.md`.

Reviewer xuất evidence độc lập:

```yaml
schema_version: 1
packet_id: wp<issue>
generation: <integer>
provider: claude | codex | human
role: reviewer
session_id: <stable-run-id>
reviewed_sha: <git-oid>
independent_from_executor_session: true
review_axes: [spec, standards_security]
tests: []
findings: []
verdict: approve | changes_requested | blocked
assurance: cross_approved | same_provider_approved | human_audited | review_deferred
evidence_url: <pr-review-or-comment-url>
```

Land evidence tách approval khỏi thao tác:

```yaml
schema_version: 1
mission_id: gh-<issue>
generation: <land-attempt-integer>
provider: claude | codex | human | github-actions
role: land_operator
session_id: <stable-run-id>
input_packet_generations: []
authorized_head_sha: <git-oid>
approver: <actor>
authorization_url: <durable-url>
land_operator: <actor>
merge_method: merge | squash | rebase
merge_commit: <git-oid>
pre_merge_checks: []
post_merge_checks: []
bookkeeping: []
```

Thiếu evidence bắt buộc chặn transition tương ứng; chat transcript hoặc lời tự khai không thay thế GitHub object,
commit và workflow run. Khi `head_sha` đổi, review verdict, CI và authorization của SHA cũ mất hiệu lực.

Dispatcher kiểm schema, generation, spec hash, changed paths, budget và mission envelope. Khóa khử trùng do
dispatcher tính từ mission, packet cha, generation và `successor_key`; chạy lại workflow không tạo Issue trùng.
Packet cloud hợp lệ chạy ngay; packet local tự chạy khi host lên. Hệ thống chỉ hỏi người dùng ở `paused`,
`blocked`, quyền LIVE hoặc land/deploy.

Với handoff Executor `status: done`, reconciler phải đọc lại PR head và so đồng thời mission revision, Packet
revision/spec hash, generation, lease, `head_sha`, `tested_sha`, changed paths và gate policy. Chỉ khi tất cả khớp,
nó mới ghi transition `running → reviewing` idempotent rồi dispatch một Reviewer mới, context/worktree độc lập và
read-only mặc định. Executor không tự tạo review có thẩm quyền; nếu chưa có automation, nó chỉ xuất prompt thủ
công nói trên và dừng. Reviewer `changes_requested` tạo finding có stable ID; reconciler trả đúng Packet/generation
về executor/rework, còn commit mới luôn làm verdict/CI/authorization của head cũ hết hiệu lực.

## 8. Review phân tầng

Mức review được ghi tường minh:

1. `cross_approved`: Claude review Codex hoặc Codex review Claude.
2. `human_audited`: người audit có danh tính bền trên GitHub, độc lập với Executor/tác giả, tự đọc spec/diff, ghi
   evidence audit và verdict bền, đồng thời neo cả hai vào exact `reviewed_sha`.
3. `same_provider_approved`: phiên mới, context/worktree riêng và read-only cùng nền tảng khi phía kia hết quota.
4. `review_deferred`: chưa có reviewer; vẫn được vào draft land PR nhưng cần xác nhận riêng khi apply.

Reviewer có `contents: read` và chỉ có quyền ghi review/comment PR. `changes_requested` trả về executor, không cho
reviewer sửa branch. Lỗi quota/rate-limit không tiêu thụ attempt nội dung; circuit breaker ngừng gọi provider tới
thời điểm reset. Dispatcher, không phải Executor, quyết định fallback/reroute; cấm đổi provider để lách budget.
Reviewer cùng provider phải tự đọc spec/diff, chạy lại check cần thiết và không chỉ tóm tắt báo cáo Executor.
Approval luôn neo `reviewed_sha`; commit mới buộc review lại.

Workflow, security paths, credential boundary, dispatcher, migration dữ liệu và LIVE adapter không được dùng
`review_deferred`: phải có cross-review khác nền tảng hoặc human review có audit. `same_provider_approved` có thể
là phản biện bổ sung nhưng một mình không thay mức assurance bắt buộc cho các phạm vi nhạy cảm này.

## 9. EOL và tệp phái sinh

Policy đích:

```gitattributes
* text=auto eol=lf
*.cmd text eol=crlf
*.bat text eol=crlf
# Các loại binary và golden byte fixtures: -text
```

`.editorconfig`, helper ghi text canonical, hook Python và CI cùng cưỡng chế policy. Gate đọc blob trong Git index,
không tin working tree hay `core.autocrlf`; validator phải xử lý file mới, Unicode và khoảng trắng trong tên.

EOL được chuyển trong maintenance mission có operational freeze/drain. Trước khi có dispatcher, người vận hành
chốt SHA từ `origin/master` mới nhất, kiểm kê worktree cùng PR/branch đang sống, ngừng writer mới và yêu cầu mỗi
chủ phiên push, bàn giao hoặc hủy. Sau khi có dispatcher, cùng điều kiện được cưỡng chế bằng `PAUSE`, ngừng cấp
lease và đợi mọi lease kết thúc.

Migration dùng ba commit: (A) policy/helper/validator theo policy đích và thay mọi hook shell chỉ so với `HEAD`;
(B) chỉ `git add --renormalize .`; (C) tái sinh manifest/golden/derived artifact và chạy parity Windows–Linux.
Không dùng `--no-verify` như đường chuẩn. Ghi lại EOL base SHA; mọi branch/worktree cũ phải rebase lên mốc đó
trước khi tiếp tục ghi hoặc nhận lease mới.

Worker không sửa `VERSION`, hằng version trong `tl.py`, header `SKILL.md`, `CHANGELOG.md` hoặc
`RELEASE_MANIFEST.json`. Test/artifact dùng ID `wp<issue>_<slug>`; changelog fragment dùng
`changelog.d/wp-<issue>.md`. Test fragment được giữ trong Git nhưng release filter loại đúng prefix
`scripts/test_fragments/`, không loại mọi thư mục trùng basename; phiên land sinh tất định bundled test module
`scripts/tl_test_fragments_bundled.py` từ các fragment, rồi mới gán release, bump ba chỗ, hợp nhất changelog
fragment và tái sinh manifest. Module trở thành required release file tại cùng activation với generator.
Loader/generator ghi UTF-8 LF tường minh, không phụ thuộc newline mặc định của Windows.

Deferred numbering không được bật trước worker gate mới. Hai thay đổi tạo một activation boundary nguyên tử:
nếu worker gate dùng manifest tạm chưa sẵn sàng thì dispatcher không cấp packet worker, kể cả policy/adapters đã
được land ở trạng thái tắt.

## 10. Worker gate, land gate và definition of done

### 10.1 Gate selftest phân tầng và fail-closed

Không chạy toàn bộ legacy selftest sau mọi thao tác nhỏ. Gate classifier và aggregator vẫn luôn chạy và quyết
định tier theo changed paths, change-impact closure, risk, test catalog, runner/policy identity và checkpoint:

| Tier | Checkpoint | Yêu cầu tối thiểu |
|---|---|---|
| T0 | inner loop của Executor | test/fragment trực tiếp cho thay đổi; không phải promotion evidence |
| T1 | packet worker gate | affected fragments/groups cùng always-on write-set, EOL, security, manifest/package và selector guards |
| T2 | trước `ready_for_rereview` | chạy lại T1 trên exact head; full nếu packet sensitive hoặc classifier yêu cầu |
| T3 | integration freeze/`land prepare` | full selftest và release gates trên Windows + Linux cho frozen integration SHA |
| T4 | canonical/`merge_group` | full trên candidate canonical, hoặc reuse duy nhất evidence T3 khi toàn bộ exact identity khớp |
| T5 | exact release artifact | full smoke/verify trên bundle/artifact có hash sẽ phát hành |

Unknown/unmapped path, selector/catalog/runner/shared fixture hoặc global state thay đổi, security/workflow,
release/manifest/package, EOL hay gate policy thay đổi phải fallback full; classifier lỗi/không đọc được cũng
fallback full. Top-level path filter hoặc job `skipped` không phải evidence: classifier + aggregator bắt buộc tạo
kết quả dương và chặn merge khi required tier thiếu. Evidence chỉ được reuse khi tested SHA/tree, policy/catalog,
runner, OS/runtime matrix và artifact hash (nếu có) khớp chính xác; head hoặc một identity đổi thì chạy lại.

Selector chỉ được activate sau khi legacy harness đã tách thành callable/group cô lập, duration được đo, full có
thể chạy song song an toàn, và shadow 2–4 tuần chứng minh affected selection không bỏ sót failure so với full.
Trước activation, T1/T2 vẫn chạy full theo policy hiện hành. Lọc output sau khi eager harness đã chạy hoặc shard
theo modulo không được coi là tối ưu hay isolation hợp lệ.

### 10.2 Worker/land gate và trạng thái hoàn tất

Worker gate kiểm generation/spec/write-set, EOL, security paths, offline tests và manifest tạm ngoài repo. Gate
dùng primitive hiện có theo nghĩa tương đương:

```text
release-manifest --root <worktree> --out <temporary-path>
release-verify <temporary-path> --root <worktree> --strict
```

Manifest tạm không tracked, không phải release artifact, không cấp version và không thay thế manifest canonical.
Worker CI không so feature branch với `RELEASE_MANIFEST.json` committed. Mọi code/test do feature branch cung cấp
phải chạy trong job không có provider secret. Gate auto-discover toàn bộ test fragment, kiểm tên/ID duy nhất và
chạy cùng legacy harness. Test-ID registry dùng chung phải lập chỉ mục cả `rNNN_*` của harness,
`wp<issue>_<slug>` của fragment và ID trong bundled module; resolver tài liệu cùng duplicate gate đọc registry
này và có negative fixture cho tên bịa. Worker dùng đúng land generator để sinh bundled candidate trong thư mục
tạm ngoài repo, kiểm byte/topology nhưng không sửa module land-only trong diff.

Các thuật ngữ trạng thái không dùng thay nhau:

- `merged`: PR đã vào nhánh đích của PR;
- `integrated`: Packet PR đã vào mission integration branch;
- `landed`: kết quả đã vào canonical ở exact SHA được duyệt, hậu-merge gate xanh và bookkeeping Packet xong;
- `complete`: toàn Mission đã readback canonical, đạt final acceptance và không còn Packet/lease mở.

Vì vậy Packet merge vào integration mới là `integrated`, chưa `landed`. PR đi thẳng canonical trong giai đoạn
bootstrap cũng chỉ thành `landed` sau post-merge evidence và bookkeeping.

Land gate đóng băng mission, rebase/integrate lần cuối, gán version/changelog/manifest và chạy parity
Windows–Linux. Land sinh bundled test module theo thứ tự tất định, kiểm cả chế độ dev có fragment lẫn topology
bundle chỉ có module sinh. Bundle không chứa fragment và thiếu bundled module phải fail với lỗi đích danh;
behavior test dựng root giả để chứng minh exclusion đi qua đường release thật, không chỉ kiểm membership của một
constant. Dispatcher được mở draft land PR nhưng không merge.

`land prepare` mặc định là dry-run/prepare. `land apply` là operation tất định của control plane: không gọi model,
không sửa diff và chỉ nhận `mission_id` cùng exact `head_sha` đã freeze. Apply phải xác minh land gate vẫn xanh,
head PR chưa đổi, review assurance đủ, authorization bền ghi đúng SHA/điều kiện, actor qua allowlist/quyền
`maintain`, GitHub Environment approval đã có và branch protection cho phép merge; mọi chấp nhận/từ chối đều có
audit. Approver có thể ủy quyền một agent làm Land Operator, kể cả agent từng là Executor, nhưng operator không
được tự sửa điều kiện, chọn head khác hoặc tính thao tác đó là approval độc lập.

Ba client tương đương được phép gọi operation: `land-packets --apply` ở local, comment
`/land apply <mission_id> <head_sha>` và typed `workflow_dispatch` có hai input đó. Vì vậy người dùng có thể đóng
mission từ GitHub trên Android khi Windows tắt, nhưng hệ thống vẫn dừng ở `awaiting_land` cho tới phê duyệt tường
minh; không auto-merge. Deploy/publish LIVE là cổng riêng. Mission chỉ `complete` sau apply, kiểm lại canonical và
không còn packet/lease mở. Deploy chỉ thuộc completion nếu acceptance criteria khai rõ.

## 11. Security boundary

1. Worker không có Drive/GAS/NLM/registry/deploy credential hoặc config LIVE.
2. Workflow có credential lấy định nghĩa từ canonical; không chạy `pull_request_target` với mã chưa tin cậy.
3. Mỗi job có `GITHUB_TOKEN` ngắn hạn và permissions tối thiểu; canonical có branch protection.
4. Action bên thứ ba pin commit SHA. Security paths chỉ đổi qua packet hạ tầng do người dùng duyệt.
5. Agent-generation và branch-code test là các job tách biệt; test job không có secret.
6. Provider credential dùng key riêng, quota cứng, dễ thu hồi. Đích là broker xác thực GitHub OIDC; direct
   GitHub Secret chỉ là bước chuyển tiếp.
7. Guard từ chối LIVE khi `CI`/`GITHUB_ACTIONS` là defense-in-depth, không phải ranh giới thật.
8. Lệnh điều phối chỉ hợp lệ khi actor nằm trong allowlist canonical và GitHub API xác nhận quyền `maintain`.

Tập lệnh đóng: `/mission start|pause|resume`, `/packet retry|cancel|reroute|preserve`, `/land prepare`,
`/land apply <mission_id> <head_sha>` và các override có lý do. Workflow dispatch apply dùng typed inputs tương
đương và cùng parser/authorization operation. Mọi lệnh chấp nhận/từ chối, budget change và review override đều
có audit.

## 12. Stop conditions và budget

Mặc định: 3 attempt/packet, 45 phút/run, cùng failure fingerprint nội dung hai lần thì blocked, tối đa 20 packet,
độ sâu kế nhiệm 5, hai worker song song, 30 agent invocation và 360 cloud minute. Các trần độc lập và trần chạm
trước thắng: 20 packet là guard cấu trúc, không hứa đủ invocation cho 20 × 3 attempt cùng reviewer. Trước khi cấp
lease/review, dispatcher ước tính `used / reserved / limit` cho packet đã biết dưới review policy hiện tại; phần
còn lại không đủ thì `paused: budget_infeasible` với phép tính hiển thị. Provider phải có hard quota ngày và
tháng; 80% cảnh báo, 100% pause. Không tự đổi provider để lách budget.

Mission không được complete khi còn packet `ready`, `leased`, `running`, `reviewing`, `blocked` hoặc khi land gate
chưa xanh. Land thất bại quay về `paused` hoặc sinh packet sửa lỗi trong envelope.

Khi chạm attempt/same-failure/quota/permission stop condition, phiên ghi failure evidence và handoff rồi dừng.
Human/dispatcher có thể reroute bằng generation mới nhưng không hồi sinh lease cũ. Nếu stop condition cho thấy
Packet Spec hoặc Mission Plan sai, phải đi qua Packet revision hoặc Mission Change Request; không thêm cờ nới bí
mật. Việc mới phát hiện trong phiên chỉ được tiếp tục tại chỗ khi nó là substep cần thiết trong spec hiện hành.

## 13. Hợp đồng ba skill

### `work-packet` — model-invoked

Trigger khi agent nhận Issue có lease hợp lệ. Trình tự bắt buộc: đọc protocol → preflight spec/lease/worktree →
heartbeat → chỉ sửa effective write set → worker gate → PR → handoff. Hoàn tất khi handoff hợp lệ đã được dispatcher nhận.
Skill từ chối làm việc nếu lease/generation/spec hash sai, cần LIVE, closure thiếu hoặc security path chưa duyệt.
Adapter chỉ trỏ các mục protocol và mô tả cú pháp/công cụ riêng của nền; không sao chép schema, stop condition hay
completion criteria. Phiên `work-packet` không chuyển vai sang reviewer hoặc land trong cùng run.

### `cross-review` — model-invoked

Trigger khi PR vào `reviewing`. Đọc protocol/spec/diff/gate evidence; review hai trục `Spec` và `Standards/Security`;
không sửa file; xuất verdict `approve | changes_requested | blocked` có severity/evidence. Hoàn tất khi verdict
đã ghi vào PR và state nhận đúng review assurance.
Reviewer dùng checkout/context độc lập, ghi exact `reviewed_sha`; nếu cùng provider thì phải là phiên mới và mang
`same_provider_approved`, không giả thành cross-review.

### `land-packets` — user-invoked client

Không tự trigger. Mặc định gọi `land prepare`: freeze mission, kiểm packet/review/override, rebase integration,
tạo release metadata và chạy land gate. `--apply` gửi mission/head SHA tới cùng operation `land apply` mà
GitHub/Android dùng; skill không chứa quyền hay logic merge riêng. Deploy là lệnh riêng và cần quyền LIVE.
Phiên land chỉ nhận authorization bền cho exact SHA. Adapter không tự cấp approval; Land Operator ghi merge,
post-merge và bookkeeping evidence trước khi chuyển `landed`/`complete`.

`.claude/skills/` và `planned:.agents/skills/` chỉ chứa adapter mỏng về cú pháp/công cụ của từng nền tảng. Quy tắc, schema
và completion criteria chỉ nằm trong file này. `CLAUDE.md` và `AGENTS.md` chỉ có con trỏ bắt buộc; CI so parity
adapter và từ chối bản sao doctrine bị lệch.

## 14. Rollout

**Bootstrap D0:** tạo worktree sạch từ `origin/master` mới nhất và land ADR-0017–0033, protocol, CONTEXT cùng
`docs/research/` non-normative bằng một PR docs-only. Không stage từ canonical đang bẩn; docs bị loại khỏi release
bundle nhưng vẫn phải qua `doc-claims-check --strict`, kiểm link/path và `git diff --check`.

1. Baseline: test-fragment loader/generator/behavior gate trước; sau đó operational freeze/drain, maintenance EOL
   ba commit và bắt buộc branch cũ rebase lên EOL base.
2. Protocol/safety: change-impact JSON/schema/seed, adapters, branch protection, security paths và worker/land
   gates; chưa có provider secret.
   Chỉ cuối pha này mới kích hoạt nguyên tử deferred numbering + worker gate manifest tạm; trước đó không cấp
   packet worker.
3. Test economics: instrument duration, tách callable/group, dọn global state, parallel full, shadow selector
   2–4 tuần rồi mới activate gate T0–T5 fail-closed.
4. Dispatcher shadow: durable inbox, reconciler, event journal/checkpoint/recovery và fixture/dry-run cho parser,
   state, race, lease, path normalization, burst/queue-loss cùng handoff idempotency.
5. Cloud canary: một provider, một packet, không successor tự động; `gh-aw` chỉ là adapter canary có kill switch.
6. Dual provider: auto-dispatch Reviewer mới, review phân tầng và circuit breaker.
7. Autonomous mission: successor trong envelope và lệnh Android.
8. Local controller: Scheduled Task, offline queue, reboot/recovery/stale tests.
9. Land automation: chỉ promote sau nhiều mission không có stale lease, out-of-effective-write-set, event mất
   hay duplicate packet.

Protocol cutover chọn zero legacy writer: trước activation, mọi PR kiểu cũ chạm version/changelog/manifest phải
merge, đóng hoặc chuyển sang packet mới; chỉ activation PR còn được nhắm canonical. Ghi `protocol_cutover_sha`
và `protocol_version`, rồi đổi required checks một lần. Không tự suy lane từ tuổi/branch/diff và không giữ lane
v0 lâu dài; ngoại lệ hiếm phải allowlist đúng PR number và kết thúc trước packet worker đầu tiên.

Mỗi pha có kill switch. Vi phạm bất biến là rollback/pause, không phải lý do nới gate.

Rollout có hai chân trời rõ nghĩa:

- **Foundation horizon (pha 1–2):** phạm vi cam kết trước, đem lại EOL canonical, deferred artifacts,
  test-fragment harness, change-impact policy, protocol/adapters và hai CI lane cho các phiên do người dùng khởi
  chạy. Kết thúc pha 2 không được quảng bá là autonomous.
- **Automation horizon (pha 3–9):** roadmap bắt buộc để đạt mục tiêu tự sinh kế nhiệm, cloud/local continuity và
  land xuyên thiết bị. Mỗi pha là một epic/PR/mission riêng, chỉ promote sau evidence và budget review; phase 3
  test-economics và phase 4 shadow phải xanh trước mọi provider secret hoặc model call.

Definition of done toàn hệ thống vẫn là tiêu chí mục 17 sau pha 9. “Foundation complete” chỉ là mốc giảm conflict,
không phải “mission automation complete”.

## 15. Phán quyết so sánh

Bản ADR-0017 mở rộng thắng phương án Drive ban đầu ở control plane: Issue/PR cho prompt, diff, review, audit và
Android trong cùng một hệ thống; GitHub Actions giữ chuỗi cloud chạy khi Windows tắt. Vì vậy registry phiên và
hàng đợi handoff trên Drive bị loại. Những phần của phương án cũ vẫn cần giữ là EOL canonical, changelog fragment,
đánh số trì hoãn và land tuần tự.

Phản biện được tiếp thu nhưng siết thêm ở các điểm sau:

| Nhận định đầu vào | Kết luận hợp nhất |
|---|---|
| Cần guard `GITHUB_ACTIONS` cho LIVE | Đúng như defense-in-depth; ranh giới thật phải là không cấp LIVE credential |
| Claim bằng assignee + label + TTL 30 phút | Chưa đủ; UI không atomic và TTL không chống split-brain, nên thêm lease + fencing generation |
| Một executor, nền tảng kia review | Đúng; bổ sung review phân tầng/circuit breaker để hết token không khóa mission thường |
| Issue thay Drive handoff | Đúng; thêm schema, spec hash, durable inbox, journal/checkpoint và reconciler idempotent |
| Worker không bump version | Đúng nhưng chưa đủ; cấm cả `rNNN`, dùng `wp<issue>` bền và fragment tới phiên land |
| Worktree giảm conflict | Chỉ giải quyết cô lập vật lý; write-set exclusion và mission integration branch mới giải quyết trùng việc/hội tụ |
| Nhóm tệp dính nhau | Quá rộng và sai với coupling một chiều; dùng change-impact closure + required checks có hướng |
| Tự sinh phiên kế nhiệm | Khả thi ở dạng headless worker; không thể hứa một chat tương tác chung giữa hai sản phẩm |
| Cloud worker dùng GitHub Secrets | Chỉ chấp nhận khóa provider riêng có quota như bước chuyển tiếp; đích là OIDC broker |
| Actions concurrency là hàng đợi | Sai; `queue: max` chỉ backpressure có trần/thứ tự run không bảo đảm, nên cần inbox bền + reconcile |

## 16. Các phương án bị loại

| Phương án | Vì sao không chọn |
|---|---|
| Nhiều phiên cùng một working tree | Cô lập file không tồn tại; trạng thái Git và file phái sinh va nhau trực tiếp |
| Chỉ dùng worktree | Cô lập vật lý nhưng không ngăn hai agent nhận cùng việc hoặc sửa write set giao nhau |
| Drive làm registry/handoff | Trùng nguồn sự thật với GitHub, thiếu lease/PR/check/audit native |
| Assignee/label làm lock | Không atomic, có thể có nhiều assignee và không chống worker cũ sống lại |
| TTL không có generation | Tạo split-brain sau takeover |
| Claude và Codex cùng implement một packet | Tốn quota, last-writer-wins và khó xác định trách nhiệm |
| PR worker trực tiếp vào canonical | Dồn conflict và trao quá nhiều quyền cho worker |
| Generic self-hosted Actions runner trên PC | Bề mặt thực thi rộng vào máy cá nhân và credential local |
| Hook EOL shell đơn lẻ | Không phủ CI/writer/file mới; dễ hỏng với NUL, Unicode và tên có khoảng trắng |
| `GITHUB_ACTIONS` guard là security boundary | Feature branch có thể sửa guard; chỉ thiếu credential LIVE mới là ranh giới |
| Một mutable state comment | Có thể sửa/xóa và không đủ để phục hồi; chỉ giữ làm projection trên journal/checkpoint |
| Actions concurrency làm durable queue | Pending có thể bị thay/đầy và thứ tự run không bảo đảm; cần inbox bền + reconciler |
| Action artifact làm state database | Có retention và bị xóa cùng workflow run; chỉ dùng recovery backup có hạn |
| Tự merge/deploy khi agent báo done | Lẫn quyền kỹ thuật với quyền canonical/LIVE và có thể hoàn tất giả |

## 17. Tiêu chí nghiệm thu hệ thống

Hệ thống chỉ được coi là triển khai xong khi chứng minh được:

- hai packet effective write set không giao chạy song song mà không đụng file/worktree;
- thay `SKILL.md` tự mở rộng effective write set/check theo policy; sửa GOTCHAS độc lập không khóa ngược, còn
  packet hoặc diff khai thiếu closure bị từ chối;
- hai packet thêm regression test song song qua hai fragment, ID trùng bị từ chối, con trỏ `wp*` resolve ở dev
  và bundle, fragment bị loại đúng prefix còn bundled module là required file/tái sinh cùng byte Windows–Linux;
- lease generation cũ không thể push/handoff sau takeover;
- workflow retry không tạo successor trùng;
- burst ít nhất ba inbox fact khi reconciler đang chạy không làm mất event dù wake-up bị thay/đảo lịch; retry cùng
  ID chỉ áp một lần, projection bị xóa dựng lại được, còn edit/delete fact đã consume làm PAUSE có audit;
- path collision Unicode/case/separator bị bắt trên Windows lẫn Linux;
- worker không sửa file land/security và không có credential LIVE;
- quota/provider outage chuyển đúng review fallback/circuit breaker;
- budget UI hiện `used/reserved/limit` và PAUSE `budget_infeasible` trước khi cấp lease không đủ invocation;
- Windows host tắt không làm mất packet local, bật lại tự tiếp tục đúng generation;
- Android đọc được prompt/state, gọi `/land apply` hoặc workflow dispatch cho exact head SHA và đóng mission mà
  không cần Windows host; stale head/actor lạ bị từ chối có audit;
- renormalize cho cùng blob EOL trên Windows/Linux, manifest và full gate xanh;
- migration EOL chứng minh đã drain mọi writer, commit giữa chỉ đổi newline và branch cũ bị chặn tới khi rebase
  lên EOL base;
- dispatcher từ chối cấp packet nếu deferred numbering và worker-gate profile chưa cùng active; manifest tạm
  strict-verify xanh nhưng không xuất hiện trong diff hoặc release artifact;
- protocol cutover không còn legacy writer/PR chưa phân loại và ghi exact cutover SHA trước packet worker đầu;
- mission chỉ complete sau canonical apply, và deploy không tự chạy.

## 18. Căn cứ khả năng nền tảng

- Claude Code hỗ trợ worktree và Remote Control; Remote vẫn chạy trên máy local và cần process/host còn hoạt động:
  [Worktrees](https://code.claude.com/docs/en/worktrees),
  [Remote Control](https://code.claude.com/docs/en/remote-control).
- Codex/ChatGPT hỗ trợ worktree, automation và Remote giữa desktop/mobile; đây là giao diện hữu ích nhưng không
  thay thế GitHub control plane:
  [Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees),
  [Remote connections](https://learn.chatgpt.com/docs/remote-connections),
  [Automations](https://learn.chatgpt.com/docs/automations).
- GitHub Actions cung cấp concurrency và token permissions/OIDC; concurrency chỉ giới hạn song song, tài liệu nêu
  pending replacement, `queue: max` tối đa 100 và thứ tự run không bảo đảm nên không thay durable inbox:
  [Concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency),
  [Workflow permissions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication),
  [OIDC](https://docs.github.com/en/actions/reference/security/oidc).
- GitHub cho phép update/delete Issue comment và workflow artifact có retention/hết hạn; đây là căn cứ để dùng
  journal/checkpoint + backup thay vì một comment/artifact đơn lẻ:
  [Issue comments REST API](https://docs.github.com/en/rest/issues/comments),
  [Artifact retention](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-retention-period-for-github-actions-artifacts-and-logs).
- GitHub hỗ trợ chạy `workflow_dispatch` thủ công và merge PR sau required checks; đây là các client mobile/web
  của `land apply`, không phải nơi định nghĩa lại quyền:
  [Run a workflow manually](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow),
  [Merge a pull request](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request).
- Claude Code trên Android có thể làm client cho cloud session hoặc phiên local qua Remote Control; Codex Remote
  cũng cho phép tiếp tục task từ điện thoại. Đây là lý do protocol coi UI/cú pháp skill là adapter, không
  là hợp đồng land duy nhất:
  [Claude Code on mobile](https://code.claude.com/docs/en/mobile),
  [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control),
  [Codex from anywhere](https://openai.com/index/work-with-codex-from-anywhere/),
  [GitHub Mobile workflow dispatch](https://github.blog/changelog/2024-07-30-run-workflows-set-as-workflow_dispatch-manually/).

## 19. Bootstrap gaps đo tại 2026-08-03

Đây là khoảng cách giữa protocol và repo hiện tại, phải xử lý theo rollout chứ không được hiểu là đã triển khai:

- Local `master` đang sau `origin/master=ac63cd7`; ADR/protocol/research vẫn untracked trong cây có nhiều thay đổi
  runtime của phiên khác. Bootstrap D0 phải đi từ worktree sạch, không stage toàn bộ cây hiện tại.
- `.gitattributes` vẫn dùng `* -text`, chỉ ép LF cho `*.sh`; ADR-0018 chưa được thi hành.
- `CLAUDE.md` vẫn yêu cầu mọi phiên bump VERSION ba chỗ/CHANGELOG, mâu thuẫn với deferred numbering của worker.
- `.github/workflows/ci.yml` chưa có `permissions:` tối thiểu và đang chạy strict verify với manifest committed,
  nên chưa tách worker gate/land gate và chưa được kích hoạt deferred numbering cho worker.
- Chưa có change-impact policy/closure trong Issue contract hoặc CI; coupling `SKILL.md` → GOTCHAS/check r219
  vẫn chỉ lộ ra sau khi selftest chạy.
- Mission F1 #40 đã land `scripts/test_fragments/`, test-ID registry/bundled module và behavior gate cho
  exact-prefix exclusion; việc giữ bundled module đồng bộ với generator trên real tree thuộc gate riêng.
- Guard `drive-push` hiện nằm ở `scripts/tl_gws.py` và chỉ nhìn `BUNDLE_META.json`; vị trí `release.py:960` là logic
  đọc archive, không phải guard publish. Chưa có policy CI tập trung cho mọi lệnh LIVE.
- Ba skill, adapter, Issue Forms, dispatcher, provider broker, local controller và branch protection nêu trên chưa
  tồn tại trong repo.
- Chưa có durable inbox, state-event checkpoint hay reconciler; chỉ cấu hình concurrency sau này sẽ không đủ để
  bảo đảm không rơi command/handoff.
- Chưa có operation `/land apply` hay typed workflow dispatch dùng exact head SHA; Android hiện chỉ quan sát và
  chuẩn bị, chưa thể hoàn tất mission theo protocol.
- Repo đang có nhiều worktree/phiên hoạt động; maintenance EOL chỉ được bắt đầu sau operational freeze/drain do
  người vận hành cưỡng chế. Không viện dẫn `dispatcher PAUSE` trong bootstrap khi dispatcher chưa tồn tại.
