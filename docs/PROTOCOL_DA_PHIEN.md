# Protocol đa phiên đa provider

## Google Antigravity provider identity

`google_antigravity` là provider riêng cho Executor hoặc Reviewer khi Packet và lease
cấp đúng vai. Mỗi lượt phải ghi `provider`, họ model thực sự phục vụ lượt chạy
(`model_family`: `claude`, `openai` hoặc `gemini`),
`execution_surface: antigravity` và `transport: machine/local` theo hợp đồng
provider; không suy họ model từ tên ứng dụng. Lượt Antigravity thiếu một trong
ba thuộc tính sau provider phải dừng. Claude Code và Codex giữ identity cũ tương
ứng họ `claude` và `openai`. Review cùng provider hoặc cùng họ model không được
ghi `cross_approved`; chỉ review độc lập trên exact SHA mới có thể được xét assurance.
Danh tính này không cấp lease: người cấp vẫn phải qua allowlist và authority bền.

- **Trạng thái:** Thiết kế đã chốt qua grilling ngày 2026-08-03
- **Protocol version:** 1
- **Governance baseline:** MCR-54-02, chấp thuận ngày 2026-08-08
- **Phạm vi:** Claude Code, Codex, Google Antigravity, Windows local, cloud worker và Android
- **Nguồn quyết định:** §20 là bảng định tuyến ADR đang hiệu lực — MỘT dòng cho MỖI ADR, máy canh bằng `packet_loop.py adr-song`. Dòng cũ ghi một PHẠM VI (`ADR-0017 đến ADR-0035`) và phạm vi ấy đã chết: 45 ADR tồn tại, 10 ADR quản trị nằm ngoài nó.
- **Kế hoạch thi công:** `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`

## 1. Mục tiêu và bất biến

Hệ thống cho phép nhiều agent run tự xử lý một mission đến `awaiting_land` mà không cần người dùng gõ lại prompt;
người có thẩm quyền có thể apply exact head SHA và hoàn tất mission từ local, web hoặc Android. GitHub Issue/PR
là control plane và nguồn trạng thái bền; Claude, Codex, Antigravity, ứng dụng desktop/mobile và local controller chỉ là các
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
  max_run_minutes: 90
  same_failure_limit: 2
  max_parallel_workers: 2
  max_agent_invocations: 30
  max_cloud_minutes: 360
  max_inbox_backlog: 100
  provider_budgets: {}
```

`max_run_minutes: 90` là profile khởi điểm đã duyệt cho cả Executor và Reviewer. Deadline luôn là
absolute wall clock và fail-closed; không đổi sang active-time và không tự sửa power policy. Sau 3–5 run thật,
Mission owner xem lại profile bằng số đo wall/working-state; dispatcher không tự nâng trần.

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
depends_on: []
executor: claude | codex | google_antigravity
environment: cloud | local
risk: normal | sensitive
review_class: routine | systemic | sensitive
acceptance_criteria: []
```

`executor` trong Packet là provider được giao, không phải phép suy họ model. Khi giao
`google_antigravity`, lease và evidence lượt chạy phải khai riêng họ model, surface và
transport thực tế theo hợp đồng provider ở đầu tài liệu.

Khi vào `ready`, spec được đóng băng bằng `spec_hash`. Đổi objective, acceptance, write set, dependency, executor
hoặc environment tạo revision mới và làm lease cũ mất hiệu lực. Dispatcher bổ sung các trường phái sinh, không
cho người dùng/agent tự khai:

```yaml
change_policy_sha: <canonical-policy-sha>
effective_write_set: []
required_checks: []
land_obligations: []
effective_review_class: routine | systemic | sensitive
```

Các trường này cùng nằm trong `spec_hash`. Policy đổi làm closure thay đổi thì packet phải tạo revision và
generation mới trước khi chạy tiếp.

`Packet Spec` là hợp đồng ở các trường trên. `Session Plan` chỉ là checklist chiến thuật của một phiên và có thể
đổi thứ tự/cách làm nếu vẫn giữ nguyên Packet Spec. Phát hiện ngoài spec phải xuất handoff/successor rồi kết thúc
phiên; agent không tự mở write set. Findings của Reviewer được sửa trong cùng Packet khi spec vẫn đủ; finding cho
thấy chính spec thiếu thì verdict là `blocked` và đi qua revision mới.

#### 3.2.1 Nguồn spec và ba mốc Git

Trước khi thi công hoặc review, đọc spec từ đúng repository/ref/OID/path do authority chỉ định,
kiểm blob và SHA-256 của bytes theo công thức của spec, rồi đối chiếu revision/generation với
lease và receipt đã công bố. Tên nhánh hoặc bản spec sẵn trong product tree không thay việc
xác minh ấy. Báo riêng nguồn authoritative (OID/path/hash) và local copy (path/hash, khớp hay
stale). Có thể đọc blob vào scratch ngoài checkout; spec mới ở ref khác không cấp quyền copy
nó vào product tree ngoài effective write set. Thiếu nguồn hoặc hash lệch thì dừng.

Hồ sơ spec/continuation/handoff phải phân biệt:

- **Immutable acceptance baseline**: OID gốc dùng đo toàn bộ diff và nghiệm thu của Packet.
- **Continuation base**: OID được phép bắt đầu run/generation tiếp theo, kèm authority cho
  việc tiếp tục; có thể đã chứa metadata hoặc phần thi công trước.
- **Reviewed candidate**: exact head và tree thật sự đưa ra review, cùng phạm vi diff từ
  immutable baseline; không mặc nhiên bằng continuation base.

Gia hạn/thay lease không dời baseline nghiệm thu. Đổi baseline cần quyết định bền và revision
Packet/Mission tương ứng; không dùng head mới để làm biến mất diff hoặc lịch sử finding.
Các tên trên mô tả nghĩa vụ evidence, không tự thêm field vào schema. Khi schema hiện hành
chưa nhận trường, ghi bảng đối chiếu trong evidence/handoff được contract cho phép, kèm
nguồn authority; không sửa tay state hoặc khai field phái sinh thay dispatcher.

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

## 4. State machine và lease

Packet đi theo:

```text
proposed → ready → leased → running → reviewing → accepted → integrated → landed
                 ↘ paused | blocked | cancelled | stale
```

Packet áp `ADR-0054` (chế độ chỉ xác định ở `record-lease` đường lease ref của `.claude/dev/packet_loop.py`) có thêm
`approved_pending` giữa `reviewing` và `accepted`: `approve` có biên nhận ghi sổ rồi vào `approved_pending`; chỉ
cửa `accept` (packet #834) đưa sang `accepted`, và chỉ khi packet áp `ADR-0054`, đo được đủ: đầu nhánh lease trên remote
bằng SHA đang chờ; mọi check bắt buộc xanh trên attempt mới nhất của run mới nhất (§10.2); connector xong trên đúng kho,
PR và head, không còn P0–P2; mỗi P3 còn mở (offline và connector, slug lấy từ biên nhận) có đúng một quyết định. Thiếu
một điều kiện thì state giữ nguyên. Packet chưa áp giữ đường `reviewing → accepted`.

Mỗi phiên chỉ thực hiện một chuyển động có trách nhiệm rõ: execute một Packet, review một PR hoặc land một exact
head. “Một đơn vị công việc” không có nghĩa một micro-step: Executor được hoàn thành mọi substep cần thiết trong
objective/write set/acceptance của Packet. Khi xuất hiện outcome độc lập hoặc phạm vi mới, phiên ghi successor và
dừng; phiên mới nhận Packet mới. Reviewer không chuyển vai sang sửa code trong cùng phiên, và phiên land không tạo
feature diff.

Lease gồm:

```yaml
packet_id: wp<issue>
role: executor
executor: claude | codex | google_antigravity
provider: claude | codex | google_antigravity  # phải khớp executor của lease Executor
model_family: claude | openai | gemini          # AG khai họ model thực chạy
execution_surface: <actual-surface>             # AG: antigravity
transport: <actual-transport>                   # AG: machine/local
reviewer: claude | codex | google_antigravity | human | null  # nếu đã được định tuyến
environment: cloud | local
branch: agent/wp<issue>-g<generation>-<executor>
write_set_hash: <sha256>
generation: <integer>
heartbeat_at: <timestamp>
lease_until: <timestamp>
heartbeat_required_minutes: 360   # lease MỚI cấp sau khi ADR-0056 kích hoạt; lease đã cấp giữ số đã đóng dấu
```

Lease `role: reviewer` khai `provider: claude | codex | google_antigravity | human`
và `executor` là provider đã viết code. Reviewer AG khai `model_family`,
`execution_surface: antigravity`, `transport: machine/local` của chính lượt review;
Reviewer human chỉ dùng với `human_audited` hoặc fallback được khai tường minh,
không mang họ model. Lease Executor dự kiến Reviewer AG còn khai
`reviewer_model_family`, `reviewer_execution_surface`, `reviewer_transport` khi
đã định tuyến. `cross_approved` nghiêm ngặt cần cả hai actor và họ model xác định.

Sau 6 giờ (360 phút) không có tiến triển, dispatcher thu hồi lease, tăng generation rồi mới reroute
(`ADR-0056`; ngưỡng cũ 30 phút của `ADR-0017`). Ngưỡng này chỉ áp cho lease MỚI cấp sau khi `ADR-0056`
kích hoạt vận hành; lease đã cấp — kể cả WP748 g19 — giữ nguyên byte và giữ `heartbeat_required_minutes`
đã đóng dấu trong chính nó. Muốn một packet đang chạy hưởng 360 phút thì phải có lease kế nhiệm được
cấp quyền riêng. `lease_until` tuyệt đối, fencing theo generation, bia mộ hai chiều và vô hiệu theo
exact head KHÔNG đổi: hết `lease_until` thì lease hết dù còn trong 6 giờ. Worker cũ sống lại
không thể heartbeat, push hợp lệ hoặc handoff. Branch/PR cũ chuyển `stale`; generation mới được đọc diff cũ nhưng
không tự cherry-pick. Commit SHA cuối được giữ trong state projection và event journal.

Khi packet vào state `reviewing`, `review_sla` là absolute timestamp do dispatcher/người giữ ghi vào lease/state
bằng audit bền; mặc định khi đo được là thời điểm vào `reviewing` + 2 giờ. Thiếu trường, không parse được
hoặc cơ sở giờ mơ hồ thì KHÔNG treo lease; đồng hồ thu-hồi-6-giờ (360 phút, cùng ngưỡng không tiến triển
ở trên) tiếp tục chạy theo xử lý fail-closed. Với
`review_sla` hợp lệ, lease vào chế độ *treo theo review* tối đa tới timestamp đó. Verdict `changes_requested`
đổ về thì executor phải heartbeat trong 15 phút, không thì thu hồi như thường. Quá `review_sla` mà chưa có verdict:
lease trở lại đồng hồ thường — phiên ấm là TỐI ƯU HOÁ, không phải quyền.

Executor lease chỉ cấp quyền thi công trong write set/generation và hạn của nó. Land authority
là quyền riêng, phải có exact SHA, phạm vi thao tác, điều kiện và hạn riêng (§13). Hết executor
lease thì ngừng sửa code; land authority còn hạn không gia hạn lease. Hậu-merge gate hoặc
bookkeeping chỉ tiếp tục nếu chính các thao tác ấy nằm trong land authority còn hiệu lực.
Không có quyền tương ứng thì handoff phần còn lại, không tự hồi sinh lease.

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
độc lập có thể chạy song song nhưng phải rebase và chạy lại gate trước khi merge — **trừ
ngoại lệ MASTER DRIFT ở §5.1**. Mỗi mission chỉ có một draft
land PR từ integration vào canonical.

### 5.1 Ngoại lệ master drift — merge thẳng, không chạy lại gate

Áp khi **đủ cả ba**: reviewer đã `approve`; required gate đã xanh trên **exact head của
nhánh**; và thứ thay đổi kể từ lúc đó là **master**, không phải head nhánh.

Trường hợp này không lặp pre-merge gate chỉ vì master drift, sau khi đối chiếu fence và
sáu kích hoạt dưới đây. Merge sạch chỉ hoàn tất thao tác merge; hậu-merge gate, authority
và bookkeeping vẫn theo §10.2/§13, chưa tự thành `landed`.

Vì sao không phá bất biến exact-SHA: quy tắc `head đổi ⇒ evidence stale` (§8, và điều
kiện reuse ở phần selector) nói về **head của nhánh được review**. Ở đây head nhánh
**không đổi** — review vẫn neo đúng SHA nó đã duyệt, gate vẫn đo đúng head nó đã chạy.
Evidence về head nhánh vẫn đúng phạm vi đã đo; nó không chứng minh tree tích hợp mới hoặc
tự mở rộng authorization sang base mới. Trước điều khoản này, hai sự kiện *head nhánh đổi* và
*master đổi* bị đọc lẫn, nên mọi lượt master drift đều phải trả giá một lượt gate đầy
đủ dù không có gì để đo lại.

**Nhưng merge sạch là bảo đảm VĂN BẢN, không phải NGỮ NGHĨA.** Git chỉ biết dòng đụng
dòng; nó không biết hai thay đổi ở hai chỗ khác nhau có làm hỏng nhau không. Nên ngoại
lệ chỉ mở khi **không trúng dòng nào** trong danh sách kích hoạt dưới đây. Trúng bất kỳ
dòng nào ⇒ **chạy lại gate SAU khi merge**.

Đặt `BASE` = merge-base của nhánh với master tại lượt gate xanh;
`DRIFT` = `git diff --name-only BASE origin/master`.

| # | kích hoạt | vì sao |
|---|---|---|
| 1 | `git merge` báo conflict | không còn là merge sạch |
| 2 | `DRIFT` giao **write set** của packet ≠ rỗng | hai bên cùng sửa một tệp; merge dòng không chứng minh ngữ nghĩa |
| 3 | `DRIFT` chạm **artefact phái sinh** (manifest phát hành, golden, VERSION) | tệp SINH RA; hai bên tái sinh độc lập thì bản gộp khác bản sinh lại |
| 4 | `DRIFT` đổi bất kỳ **bộ đếm ratchet** (số tệp gói, khe slot, số lệnh đã kiểm) | ratchet đếm toàn cây; hai bên cùng +1 thì tổng phải +2, merge dòng không cộng hộ |
| 5 | `DRIFT` chạm tệp mà nhánh **import hoặc gọi**, kể cả khác tên/thư mục | đổi chữ ký ở master + thêm lời gọi ở nhánh = gãy, git không thấy |
| 6 | `DRIFT` chạm định nghĩa workflow hoặc hook | đổi chính ĐỊNH NGHĨA cổng: lượt gate cũ đo bằng luật cũ |

Kích hoạt 3 và 4 không phải giả định: đã đo được một packet đẩy số lệnh đã kiểm từ 165
lên 166 trong golden. Hai packet cùng thêm một lệnh sẽ sửa **dòng khác nhau** nên git
merge sạch, mà tổng thì sai — và cổng golden sẽ đỏ trên canonical khi không còn ai chạy.

**Ghi lại cho đọc được sau.** Merge theo ngoại lệ này thì thông điệp merge phải nêu
`BASE`, `DRIFT` gồm mấy tệp, và **đã đối chiếu sáu kích hoạt, không trúng dòng nào**.
Không viết được câu đó nghĩa là chưa đối chiếu — thì chạy lại gate.

**Fence đầy đủ trước thao tác.** Lưu toàn bộ kết quả remote refs đã sắp xếp, thuật toán
canonical hóa/hash, endpoint, thời điểm và rc. So bằng tên **và** OID; delta phải liệt kê
mọi ref thêm/xóa/đổi với `name / old OID / new OID`, kể cả `HEAD`, tags và `refs/pull/*`.
Không bỏ pull refs để giữ hash cũ, không coi head/base khác là vô hại vì cùng số lượng ref.
Khi fence đổi, dừng ghi để phân loại từng delta, đối chiếu lease/write-set và sáu kích hoạt.
Chỉ nhận fence mới trong phạm vi authority đã cấp; nếu ngoài phạm vi thì cần quyết định mới.
Ref synthetic merge đổi phải giải thích bằng parents/tree và quan hệ với head/base đã đo
(§10.2.2), không suy bằng tên ref. Quy tắc này cũng áp dụng cho thao tác land (§13).

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
provider: claude | codex | google_antigravity
model_family: claude | openai | gemini
execution_surface: <actual-surface>  # AG: antigravity
transport: <actual-transport>        # AG: machine/local
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
hint_provenance:          # tuỳ chọn — chỉ khai khi có hunk bắt nguồn từ hint của reviewer (§8)
  - finding_id: <slug>
    reviewer: claude | codex | google_antigravity | human
    # Identity thực của hint nằm ở review receipt; AG ghi family/surface/transport tại đó.
    paths: []             # hunk/tệp bắt nguồn từ hint
    da_tai_dan_xuat: true # executor đã re-derive + tự đo, không chép mù
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
    executor: claude | codex | google_antigravity
    # Runtime family/surface/transport được neo trong lease và handoff của successor.
    environment: cloud | local
    acceptance_criteria: []
```

Executor đăng handoff/evidence lên Packet Issue và PR trước khi state rời `running` (packet áp `ADR-0054`: chưa có
PR trước lần đẩy, nên chỉ Packet Issue; xem ánh xạ ở ADR ấy; packet áp `ADR-0060` đọc theo mục review offline
trước push của ADR ấy). Test evidence phải có lệnh,
rc đọc trực tiếp và bằng chứng dương (`N/N`, `ok=true`, số file/hash...), không chỉ “passed”. `changed_paths` phải
khớp diff của exact `head_sha`; `tested_sha` phải bằng head được đề nghị review; test không chạy phải ghi
`not_run` cùng lý do. Selector evidence phải ghi tier, policy/catalog identity, nhóm đã chọn và lý do fallback;
không được chỉ ghi “affected tests passed”. `hint_provenance` là trường TUỲ CHỌN: handoff không dùng hint vẫn
hợp lệ khi vắng trường này; quy tắc dùng hint ở §8.

Handoff kèm bảng ba mốc ở §3.2.1 và SHA/tree đầu–cuối run. Khi chưa commit, khai HEAD nền
cùng diff/hash hiện vật của working tree; không gọi HEAD nền là candidate đã test/review.
Receipt thực thi đối chiếu rc tiến trình con với launcher, model/effort quan sát được,
permission denials, trạng thái cuối và hash/size của artifacts đã ổn định (§8.1).
Rc launcher bằng 0 hoặc chỉ có tệp output không chứng minh công việc đã hoàn tất.

**Biên nhận vận chuyển comment.** Khi vai được giao có quyền đăng, giữ bytes UTF-8 của body,
hash và raw JSON phản hồi. Parse JSON để lấy object ID/URL đúng loại Issue comment hoặc PR
review, rồi GET lại chính ID đó, parse `body`, so exact text và SHA-256 của UTF-8 đã giải mã.
Không hash chuỗi JSON escape thay body, không bỏ newline hay chuẩn hóa Unicode để làm khớp.
Receipt nối ID, URL, actor vận chuyển, body hash nguồn/readback, thời điểm và rc; phản hồi rỗng,
parse lỗi, 403 hoặc body lệch chưa chứng minh giao thành công. Correction là receipt mới nối
nguồn cũ; không sửa bytes receipt đã giao. Cú pháp body-file thuộc adapter, không là schema.

Phiên executor ĐƯỢC giữ ấm chờ verdict, với điều kiện handoff §7 đã đăng ĐẦY ĐỦ TRƯỚC khi vào chờ
và dùng đúng tổ hợp kích hoạt review (`status: needs_followup`, `next_role: reviewer`). Đường phục-hồi-nguội luôn
phải đủ sống một mình: phiên ấm chết giữa chừng không được làm mất gì. Trong cửa sổ đóng băng, phiên ấm
chỉ được đọc/phân tích/soạn nháp ngoài cây;
không commit/push vào nhánh packet.

Khi dispatcher/reviewer automation chưa được promote, mỗi phiên còn phải điền `next_role`,
`manual_next_action` và `copyable_prompt` đủ để người giữ tạo một phiên Claude/Codex/Antigravity mới. Prompt phải neo
mission/packet/revision/generation/exact SHA, vai trò, phạm vi, gate và stop conditions; nó là tiện ích bootstrap,
không phải lease, approval hay authority. Mẫu chuẩn ở `docs/prompts/MANUAL_SUCCESSOR_HANDOFF_D0.md`.

Reviewer xuất evidence độc lập:

```yaml
schema_version: 1
packet_id: wp<issue>
generation: <integer>
provider: claude | codex | google_antigravity | human
role: reviewer
model_family: claude | openai | gemini | null  # human: null
execution_surface: <actual-surface>             # AG: antigravity
transport: <actual-transport>                   # AG: machine/local
session_id: <stable-run-id>
model_reviewer_identity: <provider/model/session attestation>
github_submitter_identity: <github actor or null when not published>
reviewed_sha: <git-oid>
independent_from_executor_session: true
review_axes: [spec, standards_security]
tests: []
findings: []
verdict: approve | changes_requested | blocked
assurance: cross_approved | same_provider_approved | human_audited | review_deferred
evidence_url: <pr-review-or-comment-url>
```

Mỗi phần tử của `findings` **bắt buộc** kèm gợi ý cách vá gồm bốn phần: **vá ở đâu**
(tệp + hàm/ca, và tại sao ở đó chứ không chỗ khác); **vá thế nào** (với MÃ SẢN PHẨM:
chỉ mô tả hướng, không viết cả bản vá; với TEST/ĐỘT BIẾN/SCRIPT ĐO: được ở mức mã chạy
được, vì bản chất của chúng là đặc tả phản chứng); **ca test khoá nó**
(phép thử nào làm bản vá có răng, và đột biến nào phải chết sau khi vá — không nêu được
thì nói thẳng là chưa nghĩ ra); **bản vá này có thể đẻ ra gì** (hình dạng lỗi nào nó có
nguy cơ mở). Nhiều đường vá thì nêu đường rẻ nhất mà vẫn đóng lớp, rồi nói đường đắt hơn
mua thêm được gì; cho rằng không nên vá thì nói thẳng — khai thành nợ là một gợi ý hợp
lệ. Gợi ý là gợi ý, không phải chỉ thị: người vá được làm khác, và lượt sau Reviewer
không được coi *đã làm theo gợi ý của tôi* là bằng chứng đúng — vẫn phải đo. Finding
không có gợi ý, hoặc gợi ý chỉ nhắc lại chính finding, thì verdict **chưa hoàn chỉnh**.

Evidence trên là verdict contract; delivery/provenance bền dùng `review_delivery_receipt` hiện có. Đích v2 tối
thiểu có `schema_version: 2`, receipt ID, `reviewed_sha`, verdict path/hash, hai identity ở trên, evidence URL
và khai loại/cường độ mỏ neo. Mỏ neo có thể là canonical ancestry, protected evidence ref hoặc check
object; không bắt mọi verdict phải có tag. Receipt mirror trên PR branch không tự tạo required-check
authority. Packet state chỉ giữ receipt ID/hash sau validation, không chép raw identity fields thành một schema
song song.

Cutover v2 không viết lại 11 receipt v1 cũ: chúng là historical/read-only và không đủ tư cách làm
identity evidence cho required check mới. Legacy exemption phải neo vào allowlist đóng băng đúng 11
filename+hash tại cutover; `schema_version: 1` do tác giả tệp mới tự khai không tạo miễn trừ. Mọi receipt
ngoài allowlist phải validate như v2. Bộ kiểm phải làm đỏ cả receipt mới tự khai v1 lẫn mutant nới allowlist
để chứa tệp tấn công.

Land evidence tách approval khỏi thao tác:

```yaml
schema_version: 1
mission_id: gh-<issue>
generation: <land-attempt-integer>
provider: claude | codex | human | github-actions
role: land_operator
model_family: claude | openai | null  # human/github-actions: null
execution_surface: <actual-surface>
transport: <actual-transport>
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

`google_antigravity` chỉ được định tuyến làm Executor hoặc Reviewer theo Packet;
không có quyền `land_operator` trong schema này.

Thiếu evidence bắt buộc chặn transition tương ứng; chat transcript hoặc lời tự khai không thay thế GitHub object,
commit và workflow run. Khi `head_sha` đổi, review verdict, CI và authorization của SHA cũ mất hiệu lực.

Dispatcher kiểm schema, generation, spec hash, changed paths, budget và mission envelope. Khóa khử trùng do
dispatcher tính từ mission, packet cha, generation và `successor_key`; chạy lại workflow không tạo Issue trùng.
Packet cloud hợp lệ chạy ngay; packet local tự chạy khi host lên. Hệ thống chỉ hỏi người dùng ở `paused`,
`blocked`, quyền LIVE hoặc land/deploy.

Với handoff Executor `status: done` HOẶC tổ hợp `status: needs_followup` VÀ `next_role: reviewer`, reconciler phải
đọc lại PR head (packet áp `ADR-0054`, trước lần đẩy: SHA ứng viên cục bộ trong handoff và bundle; packet áp
`ADR-0060`: mỏ neo theo mục review offline trước push của ADR ấy) và so đồng thời mission revision, Packet revision/spec hash, generation, lease, `head_sha`,
`tested_sha`, changed paths và gate policy. Chỉ khi tất cả khớp,
nó mới ghi transition `running → reviewing` idempotent rồi dispatch một Reviewer mới, context/worktree độc lập và
read-only mặc định. Executor không tự tạo review có thẩm quyền; nếu chưa có automation, nó chỉ xuất prompt thủ
công nói trên và dừng. Reviewer `changes_requested` tạo finding có stable ID; reconciler trả đúng Packet/generation
về executor/rework, còn commit mới luôn làm verdict/CI/authorization của head cũ hết hiệu lực.

## 8. Review phân tầng

Mức review được ghi tường minh:

1. `cross_approved`: reviewer và executor dùng hai họ model độc lập phục vụ lượt chạy (ví dụ họ Claude review họ Codex hoặc ngược lại); neo vào họ model đã phục vụ lượt chạy, không neo vào hãng công cụ. Cùng một họ model dù qua hai vỏ công cụ khác nhau (như Antigravity đặt model Claude được Claude Code review) vẫn là `same_provider_approved`, không thành `cross_approved`. Ba mức bằng chứng họ model: `do_may` (máy đo từng lượt chạy), `khai_co_audit` (người khai kèm người audit xác nhận; mức này bắt buộc phải tự khai là yếu hơn `do_may` ngay tại chỗ dùng), hoặc `khong_do_duoc`.
2. `human_audited`: người audit có danh tính bền trên GitHub, độc lập với Executor/tác giả, tự đọc spec/diff, ghi
   evidence audit và verdict bền, đồng thời neo cả hai vào exact `reviewed_sha`.
3. `same_provider_approved`: cùng provider trong điều kiện fallback được canon cho phép,
   phiên/context/checkout mới độc lập, read-only; không fork context Executor. Đổi model/session
   trong cùng provider vẫn là same-provider, không thành cross-provider.
4. `review_deferred`: chưa có reviewer; vẫn được vào draft land PR nhưng cần xác nhận riêng khi apply.

**Ngưỡng severity theo Review Class (M1 của #523).** Đây là điều kiện nội dung
cần kiểm cùng assurance, không phải quyền tự approve hoặc land:

| Class | Điều kiện severity mặc định để xét approval |
|---|---|
| `routine` | Không còn P0/P1/P2 nếu packet áp `ADR-0054`; packet chưa áp giữ luật cũ: hết P0/P1, P2 được giữ dạng nợ. P3 còn lại phải có nợ có tên, owner và hướng xử lý được ghi trong verdict. |
| `systemic` | Không còn P0/P1/P2 (như cũ, mọi packet); P3 còn lại phải có nợ có tên, owner và hướng xử lý được ghi trong verdict. |
| `sensitive` | Không còn P0/P1/P2 nếu packet áp `ADR-0054`; packet chưa áp giữ luật cũ: hết P0, có quyết định cho từng finding còn mở. Cần approval tường minh đúng assurance và quyết định có căn cứ cho từng finding P3 còn mở; thiếu quyết định thì chưa đủ. |
| thiếu/không rõ | Xử lý như `sensitive`, không suy ra `routine`. |

"Packet áp `ADR-0054`" nghĩa là đặc tả có dòng khai hợp lệ theo mục *Hiệu lực* của ADR ấy; vòng vá thêm vì P3 và
điều kiện dừng sớm cũng ở ADR ấy.
P0 chặn approval ở mọi class. Bảng không tự cho phép bỏ qua finding hoặc miễn
review/gate/exact-SHA/human audit. Packet hoặc chỉ thị có ngưỡng chặt hơn thì áp
ngưỡng đó; ví dụ yêu cầu0P1/P2/P3 vẫn chặn dù ngưỡng mặc định cho phép ghi nợ.
Reviewer ghi ngưỡng đã áp và assurance riêng; “đủ severity” chưa phải “approved”.
Packet áp `ADR-0060` dùng điều kiện severity, Windows, mốc bỏ draft và sổ sách của ADR ấy thay cho bảng trên.

Reviewer có `contents: read` và chỉ có quyền ghi review/comment PR. `changes_requested` trả về executor, không cho
reviewer sửa branch. Lỗi quota/rate-limit không tiêu thụ attempt nội dung; circuit breaker ngừng gọi provider tới
thời điểm reset. Dispatcher, không phải Executor, quyết định fallback/reroute; cấm đổi provider để lách budget.
Reviewer cùng provider phải tự đọc spec/diff, chạy lại check cần thiết và không chỉ tóm tắt báo cáo Executor.
Approval luôn neo `reviewed_sha`; commit mới buộc review lại.

Finding của reviewer NÊN kèm *bằng chứng chạy được*: cặp neo/thay đột biến nguyên văn, phác thảo ca test
(fixture + khẳng định), script đo A/B — tất cả đã CHẠY trong sandbox/cây riêng của reviewer và ghi kết quả chạy
kèm theo. Chúng là DỮ LIỆU trong verdict, không phải commit và không mang quyền ghi. Executor tái dẫn xuất trên
cây thật (mỏ neo, tính duy nhất, tương tác với ca sẵn có), tự chạy gate, tự viết commit — bước chép-lại là một
bước KIỂM, không được bỏ.

Reviewer muốn đi xa hơn được đính `goi-y-<finding>.patch` sinh từ cây riêng của mình — đính dạng ARTIFACT
(comment/tệp), không push ref vào kho. Ba ràng buộc:

1. Patch phải mang nhãn nguyên văn: *“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm
   commit”*. Executor không được `git am` mù; worker gate chạy đủ như mọi diff khác.
2. Handoff/PR của executor phải khai `hint_provenance` (§7): hunk nào bắt nguồn từ hint của reviewer nào. Thiếu
   khai thì lượt review kế phải coi là vi phạm quy trình.
3. Với packet `sensitive`, patch-as-hint chỉ đủ điều kiện cho (a) tệp TEST thuần hoặc (b) tooling không tham gia
   authority/gate/runtime. `.github/workflows/`, launcher, gate lifecycle, dispatcher/reconciler và LIVE adapter
   bị loại trừ tường minh. Hunk hỗn hợp, path không phân loại được hoặc `paths` rỗng khi có hint cũng KHÔNG đủ
   điều kiện; các trường hợp bị loại trừ đi đường mô tả hướng. Lý do: reviewer lượt kế thường là chính tác giả hint
   — hunk không đủ điều kiện do reviewer viết rồi reviewer duyệt là self-review đội lốt cross-review, đúng thứ
   nhãn assurance tồn tại để chặn.

Reviewer phải được cấp NĂNG LỰC ĐO LẠI HIỆN TRẠNG, không chỉ diff. Khi đóng review bundle, Dispatcher phải
phân loại và ghi vào bundle mọi khẳng định định lượng trong đặc tả, handoff, bảng bằng chứng hoặc verdict mà
giá trị phụ thuộc nội dung/lịch sử/ref của kho (số ref, số lease, số biên nhận, kích thước diff của một phạm vi
khác). Chỉ cần có một khẳng định như vậy thì sandbox
reviewer phải chứa một bản sao kho đủ để họ tự chạy lệnh đo — thực tế rẻ nhất là `git clone --bare` kèm một
bản làm việc, đặt BÊN TRONG sandbox để ràng buộc "không đọc ra ngoài" vẫn giữ nguyên. Reviewer chỉ nhận diff
và tài liệu tham chiếu thì **không có cách nào** kiểm một con số nào: cả một lớp lỗi — con số từng đúng rồi
cũ đi — nằm ngoài tầm với, và ba lượt review liên tiếp có thể đọc qua nó mà không ai dừng lại. Đo được trên
PR #250: ba lượt chỉ-đọc cho `4 → 11 → 2` finding và **0** con số phân rã; lượt đầu tiên có mirror cho **3**.
Các số về lượt review này hiện chỉ có ở comment PR #250, chưa có biên nhận trong kho; chúng là nguồn ngoài
không tái lập được từ review bundle offline, không phải điều kiện để luật trên có hiệu lực.
Bắt reviewer tự vá và tự thử nghiệm nâng CHẤT LƯỢNG finding; chỉ năng lực đo mới nâng ĐỘ PHỦ — không đòn bẩy
nào thay được đòn bẩy kia.

Bản sao ấy phải TÁI LẬP MÔI TRƯỜNG CỔNG, không chỉ tái lập nội dung. Một clone sạch có cấu hình git khác cây
gốc, và cổng của kho này đọc cấu hình ấy: `core.abbrev` **phải ghim = 7** trong sandbox. Đo được ngay ở lượt
review đầu tiên dùng cơ chế này (PR #252): sandbox không ghim ⇒ `git rev-parse --short` trả **8** ⇒
`doc-claims-check --strict` đổi năm SHA dài 8 ký tự từ *advisory* thành **cờ cứng** ⇒ `rc=2`, và reviewer
báo "cổng bắt buộc không xanh" trong khi cây gốc `rc=0`. Ghim `core.abbrev=7` trong chính sandbox ấy ⇒ `rc=0`.
Bẫy này đã có trong `CLAUDE.md` từ `v1.35.78` cho đường phát hành; cấp mirror cho reviewer là **mở lại đúng
nó ở một cửa mới**. Nên: dựng sandbox xong thì chạy thử bộ cổng NGAY TRONG sandbox và đối chiếu với cây gốc
trên cùng commit — **lệch là lỗi sandbox cho tới khi chứng minh ngược lại**, và đừng giao một mirror chưa
đối chiếu.

Từ lượt review thứ HAI trở đi, verdict phải có mục `ĐỐI CHIẾU LƯỢT TRƯỚC`: với TỪNG finding của lượt liền
trước, reviewer tự kiểm trên cây hiện tại và phân loại `ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ`,
kèm bằng chứng họ tự đo — không nhận lời khai của executor. Mục này rẻ và bắt được thứ không lượt nào khác
nhìn tới: bản vá **tự sinh lỗi**. Ca thật (PR #250, lượt 3): executor sửa một con số ở một chỗ và sót chỗ thứ
hai trong cùng tệp, để lại hai lời khai mâu thuẫn; chỉ mục đối chiếu bắt được, vì chỉ nó nhìn lại chỗ vừa sửa.

Bảng bằng chứng do executor cung cấp phải TỰ KHAI GIỚI HẠN của nó. Danh sách khẳng định giao cho reviewer trở
thành TRẦN của họ nếu không nói ngược lại: kèm chính lệnh/script đã dùng để trích danh sách, nói rõ nó lọc theo
tiêu chí gì và do đó bỏ sót cái gì, và tuyên bố tường minh rằng **mỗi mục nó bỏ sót mà reviewer tìm ra được
tính là finding**. Không khai thì bảng ấy vừa định hướng vừa giới hạn cùng lúc, và giới hạn là phần không ai
thấy. Cùng gốc với "danh sách CẤM không bao giờ đủ", ở dạng bộ lọc trích dẫn.

Điều KHÔNG đổi theo các cơ chế trên (nói tường minh để khỏi bị đọc rộng):

- Reviewer vẫn không có quyền ghi vào nhánh packet, không push ref hint vào kho.
- Đường ra khỏi `reviewing` vẫn chỉ là verdict của reviewer khai báo (packet_loop đã cưỡng chế — giữ nguyên).
- Trần lượt Codex/PR (con số ở `ADR-0052`), các bộ đếm §12, và mức assurance theo class không đổi.
- `same_provider_approved` vẫn không thay `cross_approved` cho class `sensitive`.

`model_reviewer_identity` và `github_submitter_identity` là hai trường độc lập. Actor chép hoặc đăng output không
được khai thành model reviewer; ngược lại một model review khác nền không tự cấp GitHub authority cho actor đăng.
Trong M1–M2, verdict Codex do `launcher.py` neo exact SHA và hash output có thể là evidence `cross_approved`, nhưng
comment/tệp/receipt do tài khoản tác giả vận chuyển không trở thành required check hay merge authorization. Human
Land Approver phải readback exact-head verdict/receipt trước khi land Packet `sensitive`. Chỉ M3 mới được đề nghị
Dedicated App/Check Run làm publisher authority, sau canary và human activation.

Workflow, security paths, credential boundary, dispatcher, migration dữ liệu và LIVE adapter không được dùng
`review_deferred`: phải có cross-review khác nền tảng hoặc human review có audit. `same_provider_approved` có thể
là phản biện bổ sung nhưng một mình không thay mức assurance bắt buộc cho các phạm vi nhạy cảm này.

Mặc định vận hành khi quota Codex hữu hạn: Claude Code `opus` với effort `max` là Executor code chính. Mỗi Mission
dành ít nhất 70% ngân sách Executor dự kiến cho Claude và đặt trần Codex Executor ở 30%; đây là ceiling, không phải
chỉ tiêu phải tiêu. Codex chỉ nhận Packet `routine`/`systemic` nhỏ, đóng và độc lập khi phần ngân sách review đã
được reserve; tỷ lệ thực tế có thể là 0%. PR do Codex code phải được phiên Claude mới độc lập hoặc human review.
Codex vẫn là Reviewer read-only trên exact SHA ứng viên cho Packet giá trị hoặc rủi ro cao: với packet áp `ADR-0054`
là commit cục bộ, review offline rồi đẩy đúng SHA ấy; packet chưa áp thì SHA ứng viên là PR head như cũ. Số lượt Codex tối đa mỗi PR
và điều kiện cấp từng lượt sau lượt đầu ở `ADR-0052` (protocol không chép con số). Hết trần mà chưa approve thì
chuyển sang checkpoint tách phần đã ổn hoặc xem lại thiết kế, không tiếp tục gọi Codex theo quán tính. Packet thường có thể fallback
sang phiên Claude mới độc lập với nhãn `same_provider_approved` hoặc sang `human_audited`; phạm vi nhạy cảm vẫn
phải chờ Codex cross-review hoặc human audit.

Review Class được tính fail-closed từ `risk`, effective write set và diff thật. Packet khai `review_class` là
mức tối thiểu; dispatcher ghi `effective_review_class` bằng mức cao hơn giữa khai báo và classifier. Executor
không được hạ lớp. Path không biết, classifier lỗi hoặc bằng chứng không đọc được đều thành `sensitive`; human
chỉ override bằng quyết định có audit.

- `sensitive`: workflow/CI authority, security/credential boundary, dispatcher/reconciler, review/land authority,
  launcher hoặc gate lifecycle, migration dữ liệu và LIVE adapter. Phải có Codex `cross_approved` hoặc
  `human_audited`; hết quota mà chưa có human thì pause.
- `systemic`: protocol/schema/harness dùng chung hoặc enabler ảnh hưởng ít nhất ba downstream Packet/consumer.
  Dùng Codex cho review đầu; mỗi lượt sau lượt đầu chỉ cấp khi còn P0/P1, finding cắt ngang hoặc cần xác minh
  lại (luật chung cho mọi class ở `ADR-0052`). Trường hợp
  khác fallback sang phiên Claude mới độc lập hoặc human audit đúng nhãn.
- `routine`: thay đổi cô lập, docs hoặc test/report không đổi authority/security boundary. Mặc định dùng phiên
  Claude mới độc lập hoặc human; Codex chỉ dùng khi dispatcher/human nâng lớp có audit.

Trong rollout Thin Orchestration, tối đa hai Executor writer chạy đồng thời và chỉ khi effective write set không
giao. Claude là mặc định; Codex writer còn phải qua trần ngân sách 30% và review-reservation gate. Mỗi Packet có
worktree/branch riêng. Reviewer read-only không chiếm writer slot, nhưng từ lúc chốt
`reviewed_sha` tới khi verdict được ghi, branch Packet bị đóng băng; commit mới hủy lượt review hiện hành và phải
quay lại state rework/review đúng budget. Slot trống không phải lý do mở Packet khi dependency, lease hay write
set chưa an toàn.

Rework không preempt writer đang chạy. Khi có slot kế tiếp, cùng priority thì rework đi trước Packet chưa mở;
khác priority thì Packet P cao hơn đi trước rework P thấp hơn. Scheduler phải ghi lý do bỏ qua Packet ưu tiên cao.
Write set là path/prefix repo-relative có thể so máy; nhãn `planned:` chỉ cho path chưa tồn tại, không cho prose.

### 8.1 Bootstrap reviewer và receipt thực thi

Hoàn tất bootstrap **trước** khi giao checkout read-only: clone riêng từ remote thật hoặc
mirror đã kiểm và đặt origin về endpoint thật; chứng minh objects/exact head, tree và phạm vi
refs đã cấp. Bootstrapper xác minh path/trust trên đúng OS, longpaths nếu đường dẫn Windows
đòi hỏi, Git config phục vụ gate và toàn bộ tool/env capability trong runtime sẽ chạy.
Không tự chấp nhận trust, đổi permission hay dùng cờ bypass để làm probe xanh. Permission
denial là evidence thiếu năng lực; sửa bootstrap bằng quyền đã cấp hoặc trả checkpoint.
Clone, cài dependency và cấu hình cần thiết kết thúc trước mốc snapshot bàn giao.

Ghi cặp Executor–Reviewer thực tế: provider, model, effort, execution surface, transport,
session/run ID và nguồn đo. Cấu hình yêu cầu không phải runtime evidence. Nếu Packet đòi
reviewer cùng model nhưng effort cao hơn, phải đối chiếu cả hai lượt với thang effort đã
xác minh của model ấy; không suy thứ tự giữa các model khác nhau. Header CLI chỉ chứng minh
model/effort CLI công bố; không chứng minh mọi request giữ model đó. Evidence fallback hoặc
không đủ nhận dạng thì chưa nhận assurance. ChatGPT Web qua người vận chuyển vẫn chỉ là
`advisory_review` theo hợp đồng provider, không tự tạo các mức approval ở trên.

Sau run, đối chiếu trạng thái terminal/rc con, launcher rc, lỗi permission, header/model
evidence và verdict; cùng exact SHA/tree ở đầu/cuối. Output phải ổn định sau khi writer
kết thúc, ghi path/size/hash và xác minh lại trước bàn giao. Timeout, output dở dang hoặc
launcher rc=0 nhưng con lỗi không là review hoàn chỉnh. GitHub actor chỉ là submitter (§7).
Producer và consumer phải cùng trỏ hiện vật của đúng run trong scratch riêng; ghi rõ nguồn
code/Git và đường dẫn hiện vật, không chọn JSON, diff hay numstat theo cwd ngầm định.

### 8.2 Phạm vi phép đo và checkout read-only

Đặt cache/output ngoài checkout hoặc dùng no-cache, kể cả bytecode Python, Ruff và pytest.
Snapshot đầu/cuối kiểm tracked, untracked **và ignored**, HEAD/tree, diff/index và nội dung
hiện vật có thể thay đổi; không chỉ đếm path. Kiểm cả checkout được giao lẫn repo nguồn nếu
nó nằm trong phạm vi quan sát. Snapshot sạch chỉ chứng minh không có delta quan sát được
ở hai mốc; nó không chứng minh chưa từng ghi rồi hoàn nguyên trong cả lịch sử run. Ghi rõ
giới hạn đó và sandbox mode thực tế; prompt read-only không thay cơ chế sandbox.

Tách **Ruff pin/probe contract** (workflow cài đúng pin và probe version đúng cấu trúc) khỏi
**bare Ruff lint** (chạy lint thật với config/rules/path cụ thể). Mỗi phép có command, rc,
scope, tool version và output riêng. Contract xanh không chứng minh lint xanh; bare lint
chưa chạy ghi `not_run`, lỗi quyền ghi `not_measured`, đỏ giữ `failed` cùng delta baseline
nếu tiêu chí cho phép nợ nền. Không dùng nhãn chung “Ruff passed” cho kết quả contract.

### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu

Giữ stable slug theo lớp nguyên nhân/đơn vị nghĩa qua các lượt; một finding tách thành nhiều
biểu hiện vẫn phải nối lớp cũ. Reviewer tự dựng thước kiểm acceptance và soi cả câu cũ trái
tiêu chí mới, không lấy danh sách Executor làm trần. Bảng đối chiếu ghi nguồn lượt/SHA,
phạm vi đã đo, kết quả dương/âm và phần chưa đo; tổng suite hay số dòng khớp không đóng lớp.
Đổi Packet hoặc baseline không reset lịch sử, budget hay receipt đã giao (§3.2.1/§12).
Với packet áp `ADR-0054`, reviewer khái quát mỗi biểu hiện thành lớp và quét mọi biểu hiện cùng lớp trên candidate
trước khi báo, không báo từng lỗi riêng lẻ.

**Bảng lớp của mỗi lượt.** Mỗi finding có đúng một slug lớp nguyên nhân; mỗi lớp ghi
các finding IDs/biểu hiện, mức nghiêm trọng cao nhất còn mở, nguồn lượt/SHA, cách vá
chung và phép kiểm đóng lớp. Nếu cần vá riêng từng biểu hiện, ghi lý do cơ chế không
cho một thay đổi chung; gợi ý reviewer vẫn theo §7/§8, không trở thành mệnh lệnh.
Đếm số lớp và số biểu hiện riêng. Tách/gộp lớp cần bảng nối slug nguồn, lý do và phép
đối chiếu trên cùng tập finding; không đổi khóa để xóa lần tái diễn hoặc làm đẹp tỷ lệ.

Từ lượt sau, bảng đối chiếu vẫn phân từng finding trước theo bốn nhãn ở §8; lớp chỉ
được ghi **ĐÃ VÁ THẬT** khi mọi biểu hiện thuộc phạm vi được kiểm độc lập đã đóng,
không còn biểu hiện cùng cơ chế do bản vá sinh ra và không còn phần phải đo để đóng
lớp. Thiếu quan sát, cắt acceptance hoặc chuyển biểu hiện ra ngoài scope không được
tính là vá. Ghi phần `chua_do_duoc`/successor và authority riêng; giữ slug trong lịch
sử. Phép đo target/non-target và đối chứng phải đủ để quyết kết luận; lỗi setup hay
tổng suite xanh không thay bằng chứng cho đúng tính chất của từng lớp.

Open P0 luôn chặn approval. Với P1/P2/P3, đối chiếu điều kiện severity của Packet,
Review Class và assurance §8 riêng với bảng đối chiếu; hết finding hoặc tỷ lệ vá cao
không tự tạo approval, không miễn exact-SHA audit/gate. Các nghĩa vụ bảng lớp/đọc nghĩa
ở đây là kỷ luật review; scanner xanh không chứng minh chúng đã được máy cưỡng chế.

Hồ sơ kế thừa #523 trong WP538 giữ N1–N8/M16 ở spec nguồn bất biến và bốn lớp **unresolved**:

| Slug nguồn | Phần chưa được tuyên bố đóng bởi cập nhật tài liệu này |
|---|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | Nghĩa vụ đối chiếu luật cũ với tiêu chí mới trong hồ sơ #523 |
| `bien-nhan-thieu-so-ci-da-chi` | Biên nhận thiếu số CI đã chi; không thay bằng ước lượng |
| `phep-do-doctrine-khong-du-rang` | Nợ scanner; quét sạch không chứng minh đủ độ phủ ngữ nghĩa |
| `bien-nhan-luot-8-lan-du-lieu-luot-6` | Nguồn dữ liệu receipt phải nối đúng lượt |

Đây là mốc bảo toàn lịch sử, không là bảng trạng thái live. Quyết định đóng về sau cần
evidence/authority của đúng scope; bổ sung hợp đồng receipt lượt 5 và sửa scanner chưa được
giao ở WP538. Hoàn thành R01–R20 không tự approve/complete #523 hoặc mission liên quan.

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

Trong giai đoạn pre-selector, “T1/T2 vẫn chạy full” nghĩa là **một full oracle trên mỗi exact identity**, không
phải Executor, Reviewer và CI đều lặp cùng lệnh trên cùng SHA. Executor chạy targeted/component/probe trước; CI
ghi checkout identity theo §10.2.2 và phát artifact gồm JSON + output của full selftest; Reviewer validate positive marker,
output hash, SHA/tree/base/runner/command/OS/runtime rồi tái dùng lane phù hợp, đồng thời tự chạy probe đối nghịch. Evidence thiếu, đỏ, stale hoặc lệch bất kỳ
identity nào phải fallback full. Mỗi physical host giữ tối đa một heavy gate; timeout/busy là trạng thái thiếu gate,
không được đổi thành pass. Cơ chế dev-side là `.claude/dev/gate_lifecycle.py` và `/gate-targeted`; nó chỉ chống chạy
trùng và ghi/validate evidence, **không** tự chọn affected tests và không được quảng bá là A2-05/A2-06 đã activate.

### 10.2 Worker/land gate và trạng thái hoàn tất

#### 10.2.1 Candidate preflight trước freeze

Trước freeze/review cuối và trước thao tác tốn heavy gate, lưu CI plan neo candidate,
canonical base, workflow/policy identity, required contexts/OS, event dự kiến, trigger/filter,
ngân sách còn lại và nguồn authority. Kiểm toàn bộ commit message/trailer có tác động tới
event dự kiến: push xét message trong push, pull_request xét HEAD; xét cả branches/paths,
activity types và điều kiện job. Không suy CI eligibility chỉ từ diff hoặc “mergeable”.
Các marker `[skip ci]`, `[ci skip]`, `[no ci]`, `[skip actions]`, `[actions skip]` và trailer
`skip-checks: true` (kể cả dạng không có dấu cách sau `:`) tác động `push`/`pull_request`, không mặc nhiên
chặn `pull_request_target` hay event khác; workflow bị lọc có thể để required check pending.
Đối chiếu [quy tắc skip của GitHub](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs).
Marker chặn event cần thiết phải xử lý trước freeze trong quyền đã cấp. Head đổi để sửa
message thì review/gate cũ stale; không review rồi sửa SHA và tái dùng verdict. Authority
hoãn CI trong vòng sửa chỉ tạo `not_run`, không tạo pass hoặc miễn required checks. Skip
hậu merge cần authority riêng xác định exact scope và nghĩa vụ evidence thay thế.

Đo ancestry từ OID canonical đã đọc trực tiếp remote và candidate có đủ lịch sử/objects.
Rc 0 của phép ancestor là có, rc 1 là không ancestor, lỗi đọc/lệnh khác là `not_measured`;
không xử lý mọi rc khác 0 như cùng một kết luận. Chạy preflight admission bằng **mã canonical**
đã ghim, đọc candidate qua object store và lưu command/rc/SHA/hash/output. Không chạy checker
do candidate cung cấp để tự chứng nhận. Local pre-PR admission không có run/check-run/attempt
GitHub, không được giả các trường đó hoặc dùng thay receipt admission sau PR. Muốn job tự
động chạy admission trước heavy job cần workflow support riêng; tài liệu không tạo thứ tự.

Probe toàn bộ dependency mà heavy command thực sự gọi trong **chính runtime** ấy: Git,
Python đúng executable và modules, jq, actionlint, shell cùng helper/transitive tools. Ghi
version/path, import/probe command và rc; thiếu dependency thì chưa bắt đầu heavy gate.
Windows host xanh không chứng minh WSL/Linux/container xanh; từng runtime cần probe riêng.
Riêng admission hiện dùng bộ giải Git với PATH `/usr/bin:/bin`: native Windows chưa được
hỗ trợ. Nhận diện giới hạn trước khi gọi checker; không sửa PATH/consumer để lách chốt.
Chỉ dùng Linux/WSL được Packet cấp, với mã canonical tại S, object H và dependency đã đo
trong runtime đó. Không có lane phù hợp hoặc chưa có receipt dương thì ghi admission
`not_measured`, bàn giao canonical S/H, hash code, command/lỗi và bước còn thiếu; dừng
trước heavy gate. Receipt trên H đã commit không chứng nhận phần sửa chưa đóng băng.

#### 10.2.2 Identity và provenance CI

Mỗi bằng chứng CI phải tách và dẫn nguồn cho bốn mốc:

| Mốc | Dữ liệu và nguồn kiểm |
|---|---|
| Run | repository, run ID, attempt, event, run head SHA từ API của đúng run |
| Checkout | SHA thực sự chạy, parents và tree từ checkout/log/artifact của đúng job/attempt |
| Workflow definition | repository/path, exact commit OID, blob OID và SHA-256 của bytes định nghĩa |
| Gate output | job/check-run/context, runner/OS/runtime, command/rc, marker dương và artifact ID/hash |

Không đồng nhất REST run head với checkout hay workflow-definition SHA. Với synthetic merge,
chứng minh parents trỏ đúng head/base và tree từ checkout/log/artifact tương ứng; chỉ đo
`refs/pull/.../merge` hiện tại không chứng minh run cũ đã test ref ấy. Tree bằng nhau không
đồng nhất commit, thời điểm, workflow, loại test hoặc runtime; không tự nâng test head thành
test merge hoặc test Windows. Thiếu một mốc bắt buộc thì ghi thiếu, không suy để lấp receipt.

Trong lane GitHub, có thể đọc `WorkflowRun.file.repositoryFileUrl`, xác minh URL chứa đúng
repository/path và exact OID, tải blob tại OID ấy rồi băm bytes. `file` là nullable: null,
GraphQL errors, 403, URL chỉ chứa ref trôi hoặc không lấy được blob là `not_measured` cho
provenance. Không lấy REST `head_sha` hay workflow ở HEAD hiện tại thay vào. Có thể dùng
nguồn provenance khác chỉ khi tự chứng minh cùng run/attempt và exact definition identity.
Xem [schema Actions của GitHub](https://docs.github.com/en/graphql/reference/actions).

#### 10.2.3 Evidence thiếu, skipped và tiêu chí riêng

Ghi `passed`, `failed`, `skipped`, `not_run` và `not_measured` riêng. API thiếu quyền chỉ
cho biết endpoint/field ấy chưa đo được; giữ HTTP status và lỗi thực. Có thể thu tiếp theo
chuỗi GraphQL aggregate → jobs/logs → commit statuses, nhưng mỗi nguồn chỉ chứng minh phần
nó chứa. Paginate đủ, chọn đúng SHA/run/attempt/context/producer; statuses không tự có
workflow/runner/command/output. Chỉ nhận khi tổng evidence đủ identity và nội dung dương,
không đổi 403 hay list rỗng thành pass.

Job `skipped` không được cấp runner là chưa thực thi, không là Windows execution dù tên job
có Windows. `owner_waived` là disposition riêng chỉ khi có waiver bền của owner: nguồn/actor,
exact SHA, context/OS, lý do, phạm vi/hạn và điều kiện thay thế. Giữ nguyên kết quả skipped;
waiver không viết lại nó thành passed, không tự gỡ branch protection. Không có waiver đúng
scope thì required evidence còn thiếu và tiếp tục chặn gate.

Tiêu chí đột biến riêng phải có receipt dương (baseline) và âm (mutant bị bắt vì đúng tính
chất), gắn exact consumer, criterion, command/rc, output/hash và phạm vi đo. **A7 chỉ bắt
buộc khi Packet có A7**; khi có, tổng suite không thay receipt cho đúng consumer/tiêu chí A7.
Mutant chết vì setup/import/permission không chứng minh tính chất; thiếu receipt để unresolved.

#### 10.2.4 Worker gate và hoàn tất

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
Quy ước sử dụng máy Windows local của chủ kho nằm tại `ADR-0057`, `ADR-0058` và `ADR-0059`; packet áp `ADR-0060` đọc
thêm mục Windows và mục sổ sách của ADR ấy.

Các thuật ngữ trạng thái không dùng thay nhau:

- `merged`: PR đã vào nhánh đích của PR;
- `integrated`: Packet PR đã vào mission integration branch;
- `landed`: kết quả đã vào canonical ở exact SHA được duyệt, hậu-merge gate xanh và bookkeeping Packet xong;
- **Packet complete**: đã kiểm từng acceptance/obligation của đúng Packet, có land evidence và
  bookkeeping được nhận, không còn việc/lease mở của Packet; không tự thêm state `complete`
  vào packet schema chỉ vì dùng nhãn báo cáo này;
- **Mission complete** (`complete` của Mission): toàn Mission đã readback canonical, đạt final
  acceptance, mọi Packet cần thiết đã landed và không còn Packet/lease/công việc mở.

Vì vậy Packet merge vào integration mới là `integrated`, chưa `landed`. PR đi thẳng canonical trong giai đoạn
bootstrap cũng chỉ thành `landed` sau post-merge evidence và bookkeeping.
Handoff báo riêng từng trạng thái cùng URL/OID/receipt làm căn cứ và phần còn thiếu; một
Packet complete không đóng dependency hoặc Packet/Mission khác.

**`bookkeeping Packet xong` đòi DUYỆT TỪNG MỤC việc mà lease khai, không dừng ở hiện vật chính.** Một phép thử
hiện vật (`grep` thấy thứ đã land trên canonical) trả lời đúng **một** câu hỏi — *deliverable chính có ở đó
không* — và mù với mọi mục nằm ngoài tệp ấy. Lease nào khai `viec_trong_revision`, `acceptance_criteria` hay
danh sách tương đương thì mỗi mục phải có phép đo riêng trước khi packet rời hàng đợi; mục không đo được thì
khai `KHÔNG ĐO ĐƯỢC` chứ không im lặng bỏ qua.

**Đoạn này đặt NGHĨA VỤ; nó KHÔNG khai có hay không có cổng thi hành.** Quy tắc trên là **normative** cho
người vận hành — đừng đọc động từ *"đòi"* / *"phải"* thành *"đã có máy canh"*. Muốn biết hiện có cổng nào
cưỡng chế nó hay không thì **ĐO trên một revision cụ thể**; doctrine không phải chỗ trả lời câu ấy, và một
con số ghi ở đây sai ngay ở lần land kế tiếp. Cổng thi hành thuộc packet kế nhiệm (Issue #284), có lease
riêng. Khai thẳng vì im lặng ở đây sẽ tái tạo ĐÚNG lỗi mà quy tắc này sinh ra để chặn: một thứ trông như
bảo vệ cả gói trong khi không đo gì.

Căn cứ, tách theo thứ TÁI LẬP ĐƯỢC từ kho và thứ KHÔNG — packet `CI-NOI-BANG-VAO-GATE` (#254):
lease `-r2` khai **năm** mục `viec_trong_revision` (**đo được**: tệp lease trên `ops/ci-noi-bang-vao-gate`);
bốn mục đầu có hiện vật trên canonical (**đo được**); mục thứ năm nhắm vào **thân Issue**, nên trạng thái của
nó **KHÔNG ĐO ĐƯỢC** từ kho — và chính điều đó là ví dụ sống cho quy tắc. Câu *"packet đóng bằng đúng một
phép thử"* cũng **KHÔNG ĐO ĐƯỢC**: kho không giữ receipt của lần đóng. Cùng họ *"cổng vắng mặt trông giống
cổng xanh"*, đổi đối tượng: **một phép thử đo đúng MỘT thứ, bị đọc thành đo CẢ GÓI.**

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

**Phân loại chi CI theo mục đích (M7 của #523).** Ghi loại trước khi chủ động
phát sinh lượt chạy; tên event không quyết định loại:

| Loại | Điều kiện và cách ghi chi |
|---|---|
| Gate tự động | Workflow phát sinh từ event hợp lệ trong công việc đã được cấp; ghi run ID/attempt, exact SHA và chi tự động riêng. Không coi “tự động” là quyền push/mở PR để lách lệnh chưa chạy CI. |
| Phép đo được cấp | Có mục tiêu/phản chứng, scope và allowance hữu hạn công bố trước; ghi `used / reserved / limit`, rồi gắn kết quả với run ID/attempt và exact SHA. `workflow_dispatch` hợp lệ có thể thuộc loại này. |
| Thăm dò chưa được cấp | Không có mục tiêu/allowance/authority thích hợp: không chạy; muốn chuyển thành phép đo thì phải có kế hoạch và quyền trước. |

Một dispatch để đo được cấp và một dispatch thăm dò có cùng event vẫn khác loại.
Thiếu mục đích/authority thì chưa đủ điều kiện chạy, không mặc định là gate tự động.
Sổ chi tách cửa sổ hiện tại với lịch sử toàn packet, ghi rõ đơn vị allowance;
không cộng run với attempt như cùng đơn vị. Lịch sử chưa đo đủ là `KHONG_DO_DUOC`,
không phải0 và không dùng để suy phần ngân sách còn lại. Rerun cũng phải được tính
theo đơn vị đã chốt. Ngân sách tự động và phép đo không tự vay lẫn nhau.
Phân loại này không thay §10.2 về admission/provenance/gate hay chỉ thị thời điểm
chạy: khi owner yêu cầu đợi tới đủ điều kiện merge, không chạy CI/fullCI giữa vòng vá.

**Đẩy nhánh code packet và vòng vá thêm vì P3** theo `ADR-0054`, chỉ cho packet áp ADR ấy: điều kiện trước lần đẩy,
ngoại lệ đẩy vá CI (bản vá phải được approve trên SHA mới trước khi đẩy, kèm biên nhận), yêu cầu đối với máy
trạng thái, điều kiện kích hoạt, và trần vòng thêm ở ADR ấy (protocol không chép con số). ADR ấy **chưa kích hoạt**
tới khi packet máy của nó land; trước đó không packet nào áp nó.

**Tín hiệu không hội tụ theo lớp.** Với chuyển tiếp từ lượt r sang r+1, đặt U là tập
slug lớp còn mở ở cuối lượt r, F là tập con của U được reviewer lượt r+1 xác minh
ĐÃ VÁ THẬT theo §8.3. Tỷ lệ = |F|/|U|; nhiều finding cùng lớp chỉ tính một lần.
U rỗng thì tỷ lệ không xác định (`N/A`), không phải 0% hay 100%; không ghép hai tỷ lệ
thấp qua một chuyển tiếp N/A. Hai chuyển tiếp liên tiếp có tỷ lệ <50% thì dừng vòng
vá và đưa bằng chứng tới Review Rescue Checkpoint bên dưới. Ngưỡng này là heuristic
kế thừa từ #523, không là chứng minh thống kê; không thay trần độc lập.

Báo riêng các lớp mới tại r+1 (không nằm trong U), lớp tái mở và phần chưa đo; chúng
không vào tử số F. Tỷ lệ cao chỉ nói về tập U, không chứng minh hội tụ khi lớp mới
vẫn xuất hiện, không thay điều kiện dừng theo class/Packet hay bằng chứng approval.
Một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint;
ba biểu hiện của lớp trong cùng một lượt chỉ là một lần xuất hiện. Revision/scope
cut không reset lịch sử đó, không tự cấp thêm review call hoặc attempt.

Mặc định: 3 attempt/packet, 90 phút/run cho cả Executor và Reviewer, cùng failure fingerprint nội dung hai lần thì
blocked, tối đa 20 packet,
độ sâu kế nhiệm 5, hai worker song song, 30 agent invocation và 360 cloud minute. Các trần độc lập và trần chạm
trước thắng: 20 packet là guard cấu trúc, không hứa đủ invocation cho 20 × 3 attempt cùng reviewer. Trước khi cấp
lease/review, dispatcher ước tính `used / reserved / limit` cho packet đã biết dưới review policy hiện tại; phần
còn lại không đủ thì `paused: budget_infeasible` với phép tính hiển thị. Provider phải có hard quota ngày và
tháng; 80% cảnh báo, 100% pause. Không tự đổi provider để lách budget.

Executor đăng handoff đầy đủ rồi KẾT THÚC run hiện hành; thời gian CHỜ verdict nằm ngoài run. Việc chờ dùng
cơ chế đánh thức (alarm/monitor/notification), không poll chủ động. Khi verdict đổ về, lượt xử lý tiếp theo là RUN MỚI
với trần 90 phút và đồng hồ absolute wall clock riêng; run mới phải ĐO LẠI trước khi làm: `git ls-remote` head, hạn lease,
state packet, sáu kích hoạt drift — trí nhớ ấm không thay được phép đo (bài học “phiên sau phải đo lại”).

Mission không được complete khi còn packet `ready`, `leased`, `running`, `reviewing`, `blocked` hoặc khi land gate
chưa xanh. Land thất bại quay về `paused` hoặc sinh packet sửa lỗi trong envelope.

Khi chạm attempt/same-failure/quota/permission stop condition, phiên ghi failure evidence và handoff rồi dừng.
Human/dispatcher có thể reroute bằng generation mới nhưng không hồi sinh lease cũ. Nếu stop condition cho thấy
Packet Spec hoặc Mission Plan sai, phải đi qua Packet revision hoặc Mission Change Request; không thêm cờ nới bí
mật. Việc mới phát hiện trong phiên chỉ được tiếp tục tại chỗ khi nó là substep cần thiết trong spec hiện hành.

Trần lượt Codex review trên cùng PR (`ADR-0052`) là một stop condition riêng của review budget. Review Rescue Checkpoint được
kích hoạt khi chạm trần này hoặc khi PR chạm trần vòng review canon của `ADR-0043` mà chưa approve. Chạm checkpoint
không tự biến Packet thành thất bại nội dung và không cho phép gọi thêm bằng prompt/phiên khác để lách trần.

State giữ riêng `codex_review_calls_used`, `codex_executor_calls_used` và `review_rounds_used`.
`codex_review_calls_used` tăng khi launcher có bằng chứng lời gọi review đã bắt đầu sinh output/token, kể cả timeout
hoặc output sai schema; trần trên một PR theo `ADR-0052`. Lỗi preflight, permission denial hoặc rate-limit trước khi model
sinh output không tăng bộ đếm này. `codex_executor_calls_used` thuộc executor ceiling 30% và không vay/hoàn review
cap. `review_rounds_used` chỉ tăng khi verdict qua schema, exact-SHA và receipt validation. Output sai schema
fail-closed và không tự gọi lại; human chỉ được lập receipt có audit từ raw output bất biến khi verdict và SHA
hoàn toàn rõ, nếu không đi Review Rescue Checkpoint. Đổi prompt, session hay tên attempt không reset các bộ đếm.

Launcher cưỡng chế deadline bằng absolute wall clock: chờ theo lát bị chặn và so lại wall time sau mỗi lát, kể cả
khi OS không tính low-power state vào wait timeout. Sổ ghi `wall_elapsed_seconds`, `working_elapsed_seconds`,
`working_clock` và `timeout_clock=wall`. Trên Windows, chỉ được khai working-state time từ
`QueryUnbiasedInterruptTime` sau khi probe symbol an toàn; QPC/`time.monotonic()` không phải awake clock. Nền chưa
có clock đã kiểm chứng phải ghi `null/unavailable`. Launcher chỉ ghi bằng chứng và giữ kill-tree/rc `124/125`; nó
không tự động `void-attempt`. Tự động phân loại infrastructure void cần Packet và phản chứng riêng ở packet-loop.

Chỉ được tách Stable Slice khi phần đó hữu ích độc lập, đạt acceptance riêng, không phụ thuộc phần đang có finding,
không làm yếu security/gate và có test/evidence dương của chính nó. Stable Slice phải đi qua Packet/PR sạch và
review lại trên exact head mới; cấm merge branch trộn lẫn rồi hứa xử lý phần lỗi sau. Phần còn lại thành
Remediation Slice kế nhiệm, giữ nguyên stable finding IDs và lịch sử. Finding cắt ngang bất biến lõi thì không
tách: phải revision Packet/Mission, human audit hoặc pause để xem lại thiết kế. Cùng hình dạng lỗi xuất hiện lần
thứ ba bắt buộc xem lại có nên tiếp tục cách làm đó, không chỉ vá lần thứ tư.

## 13. Hợp đồng ba skill

### `work-packet` — model-invoked

Trigger khi agent nhận Issue có lease hợp lệ. Trình tự bắt buộc: đọc protocol → preflight spec/lease/worktree →
heartbeat → chỉ sửa effective write set → worker gate → PR → handoff (packet áp `ADR-0054`: worker gate → handoff →
review → đẩy → PR, theo ánh xạ ở ADR ấy). Hoàn tất khi handoff hợp lệ đã được dispatcher nhận (packet áp `ADR-0054`:
khi SHA đã approve được đẩy và PR đã mở; run kết thúc trước đó thì run kế nhiệm làm nốt, xem ADR ấy). Packet áp
`ADR-0060` đọc trình tự trước push theo mục review offline trước push của ADR ấy.
Skill từ chối làm việc nếu lease/generation/spec hash sai, cần LIVE, closure thiếu hoặc security path chưa duyệt.
Adapter chỉ trỏ các mục protocol và mô tả cú pháp/công cụ riêng của nền; không sao chép schema, stop condition hay
completion criteria. Phiên `work-packet` không chuyển vai sang reviewer hoặc land trong cùng run.

### `cross-review` — model-invoked

Trigger khi PR vào `reviewing` (packet áp `ADR-0054`: khi Packet vào `reviewing` với SHA ứng viên cục bộ; packet áp
`ADR-0060`: theo mục review offline trước push của ADR ấy). Đọc protocol/spec/diff/gate evidence; review hai trục `Spec` và `Standards/Security`;
không sửa file; xuất verdict `approve | changes_requested | blocked` có severity/evidence. Finding nên kèm
*bằng chứng chạy được* và patch-as-hint (nếu dùng) phải theo đúng ràng buộc §8 — đính dạng artifact, không push
ref. Hoàn tất khi verdict đã ghi vào PR và state nhận đúng review assurance (packet áp `ADR-0054`: ghi vào biên nhận
và Packet Issue trước lần đẩy, chép sang PR sau đó; state nhận verdict theo yêu cầu máy trạng thái ở ADR ấy; packet
áp `ADR-0060`: nơi ghi verdict trước push theo mục review offline trước push của ADR ấy).
Reviewer dùng checkout/context độc lập, ghi exact `reviewed_sha`; nếu cùng provider thì phải là phiên mới và mang
assurance theo §8 khi evidence đủ, không tự nhận `same_provider_approved` chỉ từ cấu hình
cùng provider và không giả thành cross-provider.

Trong bootstrap trước W1-S1, adapter hiện tại tiếp tục dùng prepared sandbox ngoài kho, closed read scope và bản
sao writable chỉ để chạy phản chứng mà không chạm kho thật; mọi transport chưa chứng minh phải khai caveat. W1-S1
chỉ cập nhật adapter mỏng sau khi prompt contract và receipt/state integration đã land; không được viết trước cú
pháp cho capability chưa tồn tại.

### `land-packets` — user-invoked client

Không tự trigger. Mặc định gọi `land prepare`: freeze mission, kiểm packet/review/override, rebase integration,
tạo release metadata và chạy land gate. `--apply` gửi mission/head SHA tới cùng operation `land apply` mà
GitHub/Android dùng; skill không chứa quyền hay logic merge riêng. Deploy là lệnh riêng và cần quyền LIVE.
Phiên land chỉ nhận authorization bền cho exact SHA. Adapter không tự cấp approval; Land Operator ghi merge,
post-merge và bookkeeping evidence trước khi chuyển `landed`/`complete`.

#### 13.1 Evidence trước và sau land

Land authority phải chỉ rõ approver/nguồn bền, exact candidate SHA, đích, phương thức merge,
phạm vi/hạn, điều kiện gate và các thao tác hậu merge được phép. Đối chiếu riêng executor lease
(§4); không dùng lease thay land authority hoặc dùng quyền land để sửa sản phẩm. Trước thao
tác ghi, đọc lại exact head/base và full ref fence, giải thích mọi delta theo §5.1. Nhận fence
mới không tự nhận candidate mới; đổi head đòi review/gate/authorization tương ứng.

Sau merge, ghi merge commit/parents/tree, xác minh quan hệ với candidate/target, đọc hậu-merge
gate bằng các identity §10.2.2, làm từng mục bookkeeping còn trong authority và đăng/readback
receipt theo §7. Hết hạn hoặc thiếu quyền cho bước còn lại thì dừng bước ấy và handoff; không
gọi `landed`/Packet complete/Mission complete khi thiếu bằng chứng tương ứng.

#### 13.2 Thay ruleset trong phạm vi được ủy quyền riêng

Đây là nghĩa vụ cho tác vụ ruleset được cấp riêng, không cấp quyền mutation từ skill land.
Authority phải xác định repository/ruleset ID, trường được đổi, mục tiêu/hạn và nguồn owner.
Trước write: đọc snapshot đầy đủ với quyền nhìn được các trường (kể cả bypass actors), lưu
raw JSON/hash; lập payload chỉ gồm writable fields theo API, bảo toàn mọi field ngoài scope
và `integration_id` gắn required context. Không copy `id`, `_links`, timestamps hay response
metadata vào request. Field lạ/thiếu không được im lặng bỏ; không đủ thông tin thì dừng.

Review diff payload so với writable projection của snapshot, rồi GET lại ngay trước write.
Upstream khác snapshot thì dừng và phân loại, không ghi đè bằng payload cũ. Chỉ write đúng
diff được cấp; sau đó GET/readback, so tất cả writable fields với payload và lưu rc/status,
hash trước/sau cùng authority. Readback lệch là chưa hoàn tất, không tự retry/rollback ngoài
quyền. Read-before-write/readback giảm rủi ro nhưng **không nguyên tử**: vẫn có cửa sổ race
giữa GET và write; không hứa compare-and-swap khi API chưa cung cấp bảo đảm ấy. Cần loại
race thì phải có cơ chế phối hợp writer/quyền thích hợp được cấp riêng.
Tham chiếu [API ruleset](https://docs.github.com/en/rest/repos/rules#update-a-repository-ruleset).

[Adapter Claude](../.claude/skills/) và [adapter Codex](../.agents/skills/) chỉ chứa cú pháp/công cụ của từng nền tảng. Quy tắc, schema
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

Phiên bản đầu dùng Thin Orchestration: tái dùng `launcher.py`, `packet_loop.py`, ba skill và GitHub Issue/PR;
không thêm daemon, TUI hay orchestrator tổng quát và không cài dự án bên ngoài vào critical path. Automation chỉ
được quyết định điều tất định như validate, classifier, budget, evidence và state transition. Human giữ quyền chọn
Stable Slice, revision thiết kế/Packet/Mission, land và activation mọi Dedicated App/required check.

Auto-dispatch chưa được promote chỉ vì shadow xanh. Trước khi cân nhắc promote, phải có ít nhất ba Mission thực tế
liên tiếp đã landed và canonical readback mà không có stale review/lease, out-of-effective-write-set hoặc sai
reviewer/publisher identity. Một vi phạm làm chuỗi đếm lại từ Mission kế tiếp; promotion vẫn cần human approval,
negative fixtures và kill switch, nên ngưỡng ba Mission là điều kiện cần chứ không phải quyền tự động bật.

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


## 20. Quy tắc đang hiệu lực — bảng định tuyến ADR

**Đây là chỗ DUY NHẤT trả lời câu "agent phải đọc gì để làm đúng".** Trước 22-08-2026 câu trả lời
nằm ở dòng đầu tệp này dưới dạng một PHẠM VI (`ADR-0017 đến ADR-0035`), và phạm vi ấy đã chết:
đo được ngày ấy có **45** ADR, protocol nhắc tên **4**, và trọn `0036`–`0045` — mười ADR quản trị,
gồm cả ba ADR người giữ kho vừa duyệt — nằm ngoài. Một dòng phạm vi phải được người sửa tay mỗi
lần thêm ADR; kho này vừa trả giá cho **năm** con trỏ chết cùng hình dạng (PR #230 bốn cái, cộng
docstring `t34` trỏ `t42` đã bị gỡ). Nên bảng dưới đây **do máy canh**, không do kỷ luật:

```
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"   .claude/dev/packet_loop.py adr-song --root .
```

Cổng ấy ĐỎ khi: một ADR không có dòng trong bảng · bảng trỏ một ADR không tồn tại · một ADR có
hai dòng · một ADR không có dòng `Trạng thái` đọc được · **hai tệp cùng một số ADR** · **một
tên tệp không đúng dạng và không nằm trong danh sách cho phép** · **một rào khối mã hoặc một
comment HTML không được đóng**. Thêm ADR mà quên bảng ⇒ **gate đỏ**, không phải im lặng.
Phản chứng cho từng luật ở `.claude/dev/packet_loop_test.py`.

**Chỉ metadata RENDER RA mới được tính.** Một dòng bảng `ADR-NNNN` hay một dòng `Trạng thái`
nằm trong khối mã có rào hoặc trong comment HTML là VĂN BẢN, không phải khai báo — cổng che
hai vùng ấy trước khi đếm. Rào không đóng thì ĐỎ chứ không che tới hết tệp: một rào hở sẽ
nuốt mọi metadata phía sau, tức biến lỗi định dạng thành cổng câm.

Rào MỞ và rào ĐÓNG **không cùng luật**, và gộp chúng là lỗi đã trả giá (cross-review lượt 3):
rào đóng phải cùng loại ký tự, không ngắn hơn rào mở, và **sau nó chỉ được có khoảng trắng**:
ba backtick rồi `not-a-close` **không** đóng được gì. Rào mở bằng **backtick** thì info string không được
chứa backtick; rào mở bằng **ngã** thì info string tuỳ ý. Hai luật ấy kéo cổng ngược chiều
nhau — một cái siết, một cái nới — nên mỗi cái có ca riêng và đột biến riêng.

**Một dòng chỉ được tính khi nó THUỘC VỀ một bảng.** Che vùng không-render là điều kiện CẦN
chứ không đủ: Markdown còn nhiều cách để một dòng hiện ra mà không phải là dòng bảng —
`<pre>` `<div>` `<script>` `<textarea>` `<p>`, hay đơn giản là một dòng bắt đầu bằng `|` đứng
sau một đoạn văn. Đo được: **cả sáu dạng ấy** qua lọt phép đếm khi cổng chỉ tìm "dòng TRÔNG
GIỐNG một dòng bảng". Đó cũng là lý do phép đếm `45 = 45` KHÔNG tự nó đủ — một dòng bị quên
trong bảng thật, bù bằng một dòng giả ở vùng không render, vẫn cho hai số bằng nhau.
Cổng vì thế định vị **bảng** (dòng tiêu đề `| ADR |` + dòng phân cách) rồi chỉ đọc các dòng
`|` **liền mạch** ngay sau đó; mọi dòng ngoài khối liền mạch ấy không được tính, ở đâu cũng
vậy. Đây KHÔNG phải bộ phân tích Markdown — nó chỉ định vị đúng một cấu trúc đã biết, và chốt
ở TẦNG thay vì vá thêm từng dạng. Hai đột biến tách hai tính chất: `adr_hang_nhan_ca_van_xuoi`
bỏ cả neo `^|` (nhận mọi lần nhắc ADR ở bất kỳ đâu), `adr_dem_moi_dong_giong_hang_bang` giữ neo
mà bỏ tính thuộc-về-bảng — tức phân biệt *"TRÔNG GIỐNG một dòng bảng"* với *"THUỘC VỀ một bảng"*.

Dạng tên tệp ADR, ghi ĐÚNG NHƯ MÃ (`_ADR_TEN_TEP`): `^(\d{4})-[0-9a-z]([0-9a-z-]*[0-9a-z])?\.md$` —
chặt hơn `^\d{4}-[0-9a-z-]+\.md$` ở đúng một chỗ: ký tự đầu và cuối của slug phải
là chữ-số. Thông điệp lỗi in ra chính `pattern` ấy, nên câu này không trôi khỏi mã được.

Hai luật cuối sinh từ một finding cross-review (codex, P2 trên PR #233) và đáng đọc kỹ hơn
phần còn lại, vì nó phá đúng thứ bảng này khoe là bằng chứng: bản đầu gom tệp bằng một map
khoá theo bốn chữ số đầu, nên hai tệp cùng số thì cái sau ĐÈ cái trước — 2 tệp trên đĩa mà
cổng in *"1 ADR trên đĩa, 1 dòng trong §20"* rồi trả `rc=0`. **Hai số bằng nhau chỉ là bằng
chứng khi chúng đến từ HAI phép đếm ĐỘC LẬP;** ở bản đầu cả hai đều rút từ cùng cái map đã bị
nuốt, nên chúng bằng nhau bất kể bao nhiêu tệp biến mất.

### Cột "cổng đã ĐO" nghĩa là gì — đọc trước khi dùng

Ba giá trị, và **hai trong ba là lời khai yếu**:

- **`0 cổng`** — phép đo MẠNH: không tệp cổng nào (`ops/lease_publish.py`, `.claude/dev/packet_loop.py`,
  `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`, `ci.yml`, `ops-publish-lease.yml`) nhắc
  tới khái niệm của ADR ấy dù chỉ một lần. Luật đó **chỉ sống bằng kỷ luật đọc**.
- **`có nhắc: <tệp>×<n>`** — PROXY, **KHÔNG** phải bằng chứng cưỡng chế. Nó chứng minh cái TÊN có
  mặt, không chứng minh cổng ĐỌC nó. Kho này đã trả giá bốn lần cho đúng chỗ đó
  (`which(gh)` · `rest-chung` · `gh auth status` · `mcp` gộp). Muốn biết thật thì phải có phản chứng.
- **`chưa đo`** — trạng thái THỨ BA, không được đọc thành `0` cũng không được đọc thành `có`.

Lệnh tái lập cột ấy nằm trong `ops/HOAN_THIEN_KE_HOACH_20260822.md` §1.

### A. ADR quản trị phiên đa agent

| ADR | luật | trạng thái | cổng đã ĐO (22-08-2026) |
|---|---|---|---|
| `ADR-0017` | GitHub PR là bàn giao chính; canonical độc quyền phát hành | Accepted — câu ngưỡng thu hồi *"30 phút không có tiến triển"* **đã bị thay** bởi `ADR-0056` (2026-10-19) cho lease mới; phần còn lại vẫn hiệu lực | có nhắc: rải khắp — chưa tách được cổng riêng |
| `ADR-0018` | EOL canonical theo loại tệp | Accepted | có nhắc: `ci.yml`×19 |
| `ADR-0019` | Ba skill, hai adapter, một protocol | Accepted | có nhắc: `packet_loop.py`×31 (`doctrine-scan`) |
| `ADR-0020` | Ranh giới an ninh cho worker cloud | Accepted | chưa đo |
| `ADR-0021` | Local controller headless trên Windows | Accepted | chưa đo |
| `ADR-0022` | Hai cổng land và deploy | Accepted | chưa đo |
| `ADR-0023` | Thẩm quyền lệnh điều phối | Accepted | có nhắc: `lease_publish.py`×12 · `packet_loop.py`×20 (`guard`) |
| `ADR-0024` | Review phân tầng khi hết quota | Accepted | chưa đo |
| `ADR-0025` | Issue contract và state machine | Accepted | có nhắc: `packet_loop.py`×173 (`transition`) |
| `ADR-0026` | Rollout theo promotion gate | Accepted | chưa đo |
| `ADR-0027` | Mission integration branch | Accepted | có nhắc: `packet_loop.py`×1 |
| `ADR-0028` | Stale generation và retention | Accepted | có nhắc: `packet_loop.py`×6 |
| `ADR-0029` | Budget guard cho agent | Accepted | có nhắc: `packet_loop.py`×62 · `launcher.py`×44 |
| `ADR-0030` | Definition of done của mission | Accepted | có nhắc: `packet_loop.py`×2 |
| `ADR-0031` | Test fragment thay khóa toàn cục selftest | Accepted | có nhắc: `ci.yml`×7 · `gate_lifecycle.py`×2 |
| `ADR-0032` | Change-impact rule có hướng | Accepted | **0 cổng** |
| `ADR-0033` | Durable inbox và reconciler | Accepted | có nhắc: `packet_loop.py`×3 |
| `ADR-0034` | Change-control, review độc lập và thẩm quyền land | Accepted | có nhắc: `lease_publish.py`×10 · `packet_loop.py`×11 |
| `ADR-0035` | Điều phối bền vững và selftest phân tầng | Accepted | chưa đo |
| `ADR-0036` | Claude Executor mặc định, Codex review theo rủi ro | Superseded một phần bởi ADR-0041; con số trục LỜI GỌI **đã bị thay** bởi `ADR-0052` (2026-10-16) | có nhắc: `packet_loop.py`×29 (`RC_PROVIDER`) |
| `ADR-0037` | Review Rescue Checkpoint và tách Stable Slice | Accepted — con số lượt Codex của nó **đã bị thay** bởi `ADR-0052` (2026-10-16) | **0 cổng** |
| `ADR-0038` | Review Class fail-closed và phân bổ quota Codex | Accepted — điều kiện cấp *"lượt hai"* của `systemic` **đã mở rộng** sang mọi lượt sau lượt đầu, mọi class, bởi `ADR-0052` (2026-10-16) | **0 cổng** — `review_class` khai 10/49 lease |
| `ADR-0039` | Thin Orchestration và ngưỡng promote auto-dispatch | Accepted | **0 cổng** |
| `ADR-0040` | Tách Model Reviewer Identity khỏi GitHub Submitter Identity | Accepted | **0 cổng** |
| `ADR-0041` | Ngân sách Executor Claude tối thiểu 70%, Codex tối đa 30% | Accepted | có nhắc: `launcher.py`×22 |
| `ADR-0042` | Deadline wall-clock và working-state evidence | Accepted | có nhắc: `launcher.py`×11 · `gate_lifecycle.py`×3 |
| `ADR-0043` | Trần vòng review canon là HAI, và nó chỉ có một chỗ ở | Accepted — con số trục VÒNG **đã bị thay** bởi `ADR-0048` (2026-09-12); ba trục, trần độc lập, `nang_tran` và luật một-chỗ-ở vẫn hiệu lực | **0 cổng** — `so-canon` chưa tồn tại |
| `ADR-0044` | Ngưỡng kích thước packet, neo từ số đo của chính kho | Accepted — cặp số class `sensitive` **đã bị thay** bởi `ADR-0053` (2026-10-16); trần packet thường vẫn hiệu lực | **0 cổng** |
| `ADR-0045` | Đảo vai executor/reviewer là NGOẠI LỆ CÓ VẾT, không phải mặc định mới | Accepted | **0 cổng** |
| `ADR-0046` | Tác giả xuyên suốt, reviewer mới mỗi lượt, cắt phiên ở biên packet | Proposed | **0 cổng vận hành**; `adr-song` chỉ canh đăng ký/trạng thái |
| `ADR-0047` | Nguồn tin cậy cho cổng đọc lease: danh tính ghim, hồ sơ tiến trình, toàn vẹn object | Proposed | **0 cổng** (đo 08-09-2026, `origin/master` `585c7d5`: chưa có adapter/digest/băm object); `adr-song` chỉ canh đăng ký/trạng thái |
| `ADR-0048` | Trần trục VÒNG nâng theo chỉ thị chủ kho 12-09-2026, thay số của `ADR-0043`; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | **0 cổng** — `so-canon` vẫn chưa tồn tại (nợ cùng tên) |
| `ADR-0049` | Cổng hai nền trước phát hành, không phải mỗi lần land | Accepted | có nhắc: `ci.yml` · `deploy-package.*` |
| `ADR-0050` | `cross_approved` neo vào họ model, không vào hãng công cụ; ba mức bằng chứng model | Accepted | `ops/bien_nhan_v2.py` (`_NEO_LUAT_CHEP_TAY` + chốt tách họ model) |
| `ADR-0052` | Trần trục LỜI GỌI Codex mỗi PR nâng theo chỉ thị chủ kho 16-10-2026, thay số của `ADR-0036`/`0037`; lượt sau lượt đầu phải có lý do; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted — con số trục LỜI GỌI **đã bị thay** bởi `ADR-0055` (2026-10-25) cho đặc tả khai `ADR-0055`; đặc tả khai `ADR-0052` giữ con số của nó | `packet_loop.py`: bộ đếm trong state từ #775 (`init --codex-review-calls-limit`, mặc định hai; `record-codex-call` chặn trước khi vượt) — không gì đọc dòng khai của đặc tả |
| `ADR-0053` | Trần kích thước packet `sensitive` nâng theo chỉ thị chủ kho 16-10-2026, thay cặp số `sensitive` của `ADR-0044`; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | **0 cổng** |
| `ADR-0054` | Đẩy nhánh code packet khi đủ điều kiện merge, review offline neo SHA cục bộ, dừng vá khi hết P0/P1/P2 ở mọi class, review tìm theo lớp; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted — chưa kích hoạt, chờ packet máy `MAY-ADR-0054` | **0 cổng** — không bộ đếm số lần đẩy |
| `ADR-0055` | Trần trục LỜI GỌI Codex mỗi PR nâng theo chỉ thị chủ kho 25-10-2026, thay số của `ADR-0052`; trục LỜI GỌI nay bằng trục VÒNG; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | `packet_loop.py`: cùng bộ đếm trong state như `ADR-0052` — người khởi tạo tự truyền trần; không gì đọc dòng khai `tran_loi_goi_codex:` |
| `ADR-0056` | Ngưỡng thu hồi lease vì không tiến triển nâng từ 30 lên 360 phút theo chỉ thị chủ kho 19-10-2026, thay đúng câu 30 phút của `ADR-0017`; chỉ áp lease mới, không hồi tố; `lease_until`, generation, bia mộ, exact head và heartbeat 15 phút sau `changes_requested` giữ nguyên | Accepted — đã kích hoạt vận hành (merge PR thi công wp943) | **0 cổng** — không controller trong kho mang hằng 30 phút; không có controller ngoài, phiên điều phối áp tay |
| `ADR-0057` | Máy Windows local của chủ kho dùng khi online theo chỉ thị chủ kho 29-10-2026; đã chạy local thì vá lỗi local do diff trước merge; cộng thêm, không thay check bắt buộc CI; phạm vi và khoá sửa bởi `ADR-0058` | Accepted | không cổng — kỷ luật executor |
| `ADR-0058` | Máy Windows local: sửa đúng §1 Phạm vi và §3 Khoá của `ADR-0057` theo chỉ thị chủ kho 30-10-2026 — phạm vi là mọi máy Windows của chủ kho `Online` trong `list_devices`; khoá và sổ đo theo từng máy; dòng khoá có hạn không quá 2 giờ, khoá hết hiệu lực khi quá hạn, khi dòng dạng cũ quá 2 giờ, hoặc khi phiên giữ khoá tuyên bố bỏ có bằng chứng; khoá bổ sung bởi `ADR-0059` | Accepted | không cổng — kỷ luật executor |
| `ADR-0059` | Máy Windows local: chỉ bổ sung §3 Hạn khoá của `ADR-0058` và §3 Khoá của `ADR-0057` theo đặc tả chủ kho duyệt 31-10-2026 — nhịp tim của dòng khoá, tiếp nhận khoá khi còn tiến trình, lượt bị ngắt, đọc lại trước khi ghi lại, nhả khoá; luật nằm trong ADR | Accepted | không cổng — kỷ luật executor |
| `ADR-0060` | Điều kiện merge, mốc bỏ draft và làn sổ sách cho packet có dòng khai `dieu_kien_merge` hợp lệ; luật chi tiết chỉ ở ADR ấy; độc lập với `ADR-0054`; không hồi tố | Accepted | `packet_loop.py` `kiem-merge` (K0–K6), `kiem-dong-wp` (D1–D4) |
| `ADR-0061` | Không ghi được trạng thái "credential Codex bị từ chối": chấp nhận vĩnh viễn khả năng probe lặp khi state còn đọc được mà chưa nhớ danh tính ấy (nợ #825); cả ba lối báo lỗi ghi có lý do riêng; không dựng chỗ lưu dự phòng | Accepted | có nhắc: `launcher.py`×4 (hàm/tên nợ, chưa chứng minh cổng đọc quyết định); việc chấp nhận sống bằng kỷ luật đọc |

### B. ADR ngoài phạm vi protocol — thuộc `scripts/tl.py` và đường phát hành

Liệt kê TỪNG SỐ, không dùng phạm vi: một phạm vi là thứ vừa giết dòng 7.

| ADR | luật | trạng thái |
|---|---|---|
| `ADR-0001` | Chỉ canonical đánh version; nhánh song song giao nộp bundle không-version | Superseded by ADR-0017 |
| `ADR-0002` | bind(tl) copy-globals là giàn giáo di cư, không phải kiến trúc đích | Accepted |
| `ADR-0003` | Profile marker trên Drive là nguồn sự thật về tồn tại/định danh profile; config là cache | Accepted |
| `ADR-0004` | Hợp nhất các đường ingest bằng engine chung có ngân sách hiệu năng | Accepted |
| `ADR-0005` | Môi trường chạy sở hữu source policy, ingest engine sở hữu bất biến toàn vẹn | Accepted |
| `ADR-0006` | Content-addressed ingest và thay thế tường minh | Accepted |
| `ADR-0007` | Bundle tái tạo giống byte tuyệt đối, ưu tiên tính tất định hơn kích thước | Accepted |
| `ADR-0008` | Topology shard hợp nhất (declared+observed) và partial trung thực | Chấp nhận |
| `ADR-0009` | Đặc tả thể thức là nguồn sự thật duy nhất; thang thẩm quyền 3 bậc khi nguồn lệch nhau | accepted |
| `ADR-0010` | nlm_status là từ vựng ĐÓNG ở cửa ghi; tách nlm_claim/nlm_due (desync ≠ coverage_gap) | accepted |
| `ADR-0011` | SourceRevision tách khỏi Content Identity; claim key không đội lốt content_hash | Accepted |
| `ADR-0012` | Marker write là transaction chứng minh được; schema v2 có fingerprint, rollout 2 pha | Accepted |
| `ADR-0013` | ZIP ingest: immutable plan bundle — apply không được tự lập kế hoạch mới | Accepted |
| `ADR-0014` | `ingest_commit`: gộp organize+rename+upsert+readback thành MỘT round-trip GAS | Accepted |
| `ADR-0015` | Lane STAGED: hoãn cổng chất lượng có kỷ luật + verify PARITY + bulk-flip corpus | Accepted |
| `ADR-0016` | Lớp điều phối rà soát hồ sơ: state LAI, một-người-ghi theo claim, anchor biến tái-rà thành phép tính | KHÔNG CÓ DÒNG TRẠNG THÁI |

### Nợ có tên đã lộ ra khi dựng bảng này

- **`ADR-0016-THIEU-DONG-TRANG-THAI`** — `docs/adr/0016-*.md` không có dòng `Trạng thái` nào. Đó là
  trạng thái thứ ba (`không đo được`), nên cổng phải ĐỎ; nó hiện được tha bằng một danh sách
  ngoại lệ **liệt kê tường minh** trong `packet_loop.py`, và một ADR MỚI thiếu dòng ấy vẫn ĐỎ
  (có phản chứng). Ghi ở `ops/NO_KY_THUAT.md`.
- **`TU-VUNG-TRANG-THAI-ADR-TROI`** — đo được bốn cách viết cho cùng một nghĩa: `Accepted` (39),
  `accepted` (2), `Chấp nhận` (1), và `Superseded một phần bởi ADR-0041` (1) — chuỗi cuối bắt đầu
  bằng `Superseded` nhưng ADR ấy **vẫn còn hiệu lực một phần**. Vì vậy cổng ở đây cố ý KHÔNG phán
  xử hiệu lực từ chuỗi trạng thái; nó chỉ đòi **có mặt trong bảng**. Phán xử hiệu lực bằng cách
  khớp tiền tố chuỗi là đúng hình dạng lỗi *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"*.
