# Thẩm định góp ý ADR-0017…0032 và khuyến nghị hợp nhất cuối

- **Ngày kiểm:** 2026-08-03 (Asia/Saigon)
- **Đầu vào:** `D:/Quốc hội/_docs_lam_viec/DANH_GIA_ADR_0017_0032_2026-08-03.md`
- **Phạm vi kiểm:** các gợn V.1–V.5, khuyến nghị VIII.1–VIII.8 và câu hỏi IX.1–IX.8
- **Nguồn:** cây Git hiện tại, `origin/master`, lịch sử Git và tài liệu chính thức của GitHub
- **Tính chất:** báo cáo nghiên cứu; không phải nguồn quy tắc vận hành. Protocol và ADR sau khi land mới là nguồn chuẩn.

## 1. Phán quyết ngắn

Bản góp ý có chất lượng cao và phần lớn nên được tiếp thu. Kết quả chi tiết là:

- **Tiếp thu toàn phần:** V.1, V.2, V.4, V.5; VIII.2, VIII.4, VIII.5, VIII.6, VIII.8.
- **Tiếp thu một phần và thay bằng cơ chế mạnh hơn:** V.3; VIII.1, VIII.3, VIII.7.
- **Bác toàn phần:** không có.

Ba điều cần sửa trong chính lời khuyến nghị:

1. PR docs-only không tác động release bundle/manifest, nhưng **vẫn tác động gate tài liệu**; không thể gọi là
   “0 tác động cổng”. CI hiện chạy `doc-claims-check --strict`, và mã hiện tại chủ ý quét `docs/`.
2. “Snapshot định kỳ vào artifact hoặc Issue body” chưa đủ bền: comment và Issue đều sửa/xóa được; Action
   artifact mặc định hết hạn. Cần event journal có thể dựng lại state, checkpoint sau **mỗi transition**, và
   artifact chỉ làm bản sao dự phòng có hạn.
3. “Gate thấy coupling ngoài closure thì luôn thêm rule” có thể đóng băng một coupling ngẫu nhiên. Cần ratchet
   bắt buộc xử lý nguyên nhân, nhưng kết quả hợp lệ có thể là thêm rule, đổi thành land obligation, sinh/bỏ pin
   động, hoặc ngoại lệ có chủ, lý do và hạn dùng.

Ngoài tám câu hỏi của bản góp ý, kiểm tài liệu GitHub phát hiện một khoảng hở **P0**: chỉ dùng một Actions
`concurrency` group với `cancel-in-progress: false` không tạo hàng đợi lossless. Mặc định chỉ một run được pending;
run pending cũ có thể bị run mới thay thế, và thứ tự bắt đầu không được bảo đảm. Protocol hiện coi concurrency
như đủ để tuần tự hóa dispatcher, nên phải bổ sung durable inbox/reconciliation trước khi xây dispatcher.

### Trạng thái hợp nhất sau báo cáo

Các khuyến nghị đã được đưa vào bản thiết kế cuối: sửa ADR-0017/0025/0026/0028/0029/0030/0031/0032,
`CONTEXT.md` và Protocol; bổ sung **ADR-0033 — Durable inbox và reconciler** cho P0. Bản cuối chốt thêm đường dẫn
policy/schema, bundled module `planned:scripts/tl_test_fragments_bundled.py`, zero-legacy cutover, budget reservation,
full-state checkpoint sau mỗi transition và exact-prefix release exclusion. Báo cáo này vẫn non-normative;
ADR/Protocol thắng nếu số dòng hoặc mô tả trạng thái vật lý bên dưới trở nên cũ.

## 2. Trạng thái vật lý đã kiểm

Tại thời điểm kiểm:

- Local `master` ở `e8134a2`, chậm hơn `origin/master` chín commit; `origin/master` ở `ac63cd7` (merge PR #21).
- `docs/PROTOCOL_DA_PHIEN.md` và ADR-0017…0032 vẫn untracked trong worktree dùng chung; `CONTEXT.md` và nhiều
  tệp runtime đang bị các phiên khác sửa.
- Có bảy worktree được Git ghi nhận. Có ba remote branch chưa được merge vào `origin/master`; trạng thái này
  **không đủ để kết luận** có bao nhiêu PR đang mở, nhưng đủ bác giả định rằng cutover có thể mặc nhiên coi là
  không còn công việc cũ.
- `planned:scripts/test_fragments/` và change-impact policy chưa tồn tại; các cơ chế đó vẫn là thiết kế.

Vì vậy khuyến nghị land “hiến pháp” sớm là đúng, nhưng phải dựng PR từ `origin/master` mới nhất trong worktree
riêng, không stage từ cây canonical đang bẩn.

## 3. Thẩm định V.1–V.5

### V.1 — `claimed` và `leased`: tiếp thu toàn phần

**Bằng chứng.** ADR-0017 vẫn dùng `claimed` trong điều kiện mission complete
(`docs/adr/0017-pr-github-la-ban-giao-va-dieu-phoi-chinh.md:45`). Protocol dùng state chuẩn `leased` ở dòng 115
và cấm complete khi còn `ready`, `leased`, `running`, `reviewing`, `blocked` ở dòng 331; ADR-0025 và ADR-0030
cùng theo mô hình sau.

**Kết luận.** Đây không chỉ là mỹ phẩm: hai danh sách điều kiện complete là doctrine trùng lặp và ADR-0017 đang
thiếu `reviewing`. Sửa ADR-0017 thành:

- dùng `leased`, không dùng `claimed` như state;
- không chép lại danh sách terminal/non-terminal;
- ủy quyền definition of done cho ADR-0030 và Protocol mục 12.

### V.2 — số học mission envelope: tiếp thu toàn phần, giữ mặc định 30

**Bằng chứng.** Protocol đặt `max_packets: 20`, `max_attempts_per_packet: 3` và
`max_agent_invocations: 30`; ADR-0029 nói invocation gồm cả executor lẫn reviewer. Nếu một packet thành công cần
ít nhất một executor run và một reviewer run, 20 packet thành công ngay lần đầu đã có thể cần 40 invocation.
Trường hợp 20 packet dùng đủ ba executor attempt rồi mới review có thể cần 80 invocation. Các trần vì vậy không
thể đồng thời “tiêu hết”.

**Kết luận.** Không nhất thiết tăng 30: trần invocation là budget mission độc lập, còn packet/attempt/depth là
trần cấu trúc. Hệ thống phải dừng ở **trần đầu tiên chạm**, không hứa rằng mọi tổ hợp trần đều khả dụng. Bổ sung
vào ADR-0029/Protocol:

- định nghĩa một invocation là một lần gọi model/run executor hoặc reviewer;
- retries do quota không ăn content attempt nhưng vẫn ăn invocation nếu provider thực sự nhận request;
- trước khi cấp lease/review phải dự toán invocation còn lại; thiếu budget thì `paused` với lý do và phép tính;
- state UI hiển thị `used / limit / reserved`, tránh PAUSE “bí ẩn”.

### V.3 — một state comment là điểm mất đơn: tiếp thu một phần, thay snapshot định kỳ bằng journal

**Bằng chứng repo.** ADR-0025 và Protocol mục 3.3 đặt toàn bộ machine state trong một JSON block ở một comment do
dispatcher sở hữu. Không có snapshot/recovery contract.

**Bằng chứng nền tảng.** GitHub có API sửa/xóa issue comment; token có quyền Issues hoặc Pull requests write có
thể gọi endpoint xóa. Event `issue_comment` có activity `created`, `edited`, `deleted`, nên hệ có thể phát hiện
thay đổi nhưng không thể giả định comment bất biến. Action artifact mặc định chỉ giữ 90 ngày và có thể bị xóa;
retention tối đa còn phụ thuộc loại repo/chính sách. Xem tài liệu chính thức:

- [REST API endpoints for issue comments](https://docs.github.com/en/rest/issues/comments)
- [Events that trigger workflows — `issue_comment`](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issue_comment)
- [Removing workflow artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts)
- [Artifact and log retention](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-retention-period-for-github-actions-artifacts-and-logs)

**Kết luận hợp nhất.** Giữ state block làm **projection để đọc nhanh**, không làm bản duy nhất có thể phục hồi.
Mỗi transition được chấp nhận phải sinh một record append-only, có:

```json
{
  "schema_version": 1,
  "event_id": "gh-comment-or-dispatch-id",
  "entity_id": "mission-or-packet",
  "expected_state_revision": 7,
  "generation": 2,
  "spec_hash": "...",
  "actor": "...",
  "payload_hash": "...",
  "result": "accepted-or-rejected",
  "previous_event_hash": "...",
  "state_hash": "..."
}
```

Sau **mỗi** transition, dispatcher ghi full-state checkpoint mới, nối hash với checkpoint trước; không chỉ chụp
“định kỳ”. State block chứa ID/hash checkpoint cuối. Reconciler có thể dựng lại state từ checkpoint còn sống và
các event tiếp theo. Sửa/xóa command, event hoặc checkpoint đã tiêu thụ phải tạo audit và `paused`, không âm thầm
chấp nhận nội dung mới. Artifact là bản sao hỗ trợ điều tra, retention ít nhất bằng mission retention + 30 ngày,
không phải nguồn duy nhất. Khi land, ledger cuối được lưu vào báo cáo canonical.

### V.4 — resolver tên ca mới: tiếp thu toàn phần và tổng quát hóa

**Bằng chứng.** Commit `c07384a` thêm ca `r326_con_tro_ten_ca_resolve`. Mã tại
`origin/master:scripts/tl_selftest.py:26104-26124` chỉ bóc đăng ký `_t110("rNNN_...")` trong monolith và chỉ quét
con trỏ `` `rNNN_slug` `` trong `RASOAT_HOSO_LOOP.md`. Nó không biết fragment `wp<issue>_<slug>`, không quét
`planned:scripts/test_fragments/`, và không chứng minh topology bundled.

**Kết luận.** Không vá thêm một regex riêng trong đúng ca r326. Gói ADR-0031 phải tạo một test-ID registry/parser
dùng chung, nhận:

- legacy ID `rNNN[_slug]` từ `tl_selftest.py`;
- packet ID `wp<issue>_<slug>` từ fragment;
- bundled module sinh ra.

Resolver tài liệu và duplicate-ID gate cùng đọc registry này. Acceptance test phải chứng minh ID `wp*` hợp lệ
resolve ở dev lẫn bundle, ID bịa bị bắt, và một ID xuất hiện ở hai topology bị từ chối.

### V.5 — loại fragment khỏi manifest: tiếp thu toàn phần, sửa khẩu độ exclude

**Bằng chứng.** `origin/master:scripts/tl_core/release.py:328-333` có `_RELEASE_EXCLUDE_DIRS`, nhưng chưa có
`test_fragments`; `_release_should_include` tại dòng 467-498 loại theo **bất kỳ path component** nào nằm trong
set đó. Danh sách required file tại dòng 387 trở đi chưa có bundled test module. Vì thế ADR-0031 chưa có răng
runtime.

**Kết luận.** Không nên thêm tên chung `test_fragments` vào set loại mọi thư mục cùng tên ở mọi cấp. Dùng prefix
canonical chính xác `planned:scripts/test_fragments/` (hoặc một predicate tương đương) và thêm bundled module đã chốt
đường dẫn vào `_RELEASE_REQUIRED_FILES`. Test phải khóa hành vi, không chỉ khóa hằng:

1. fake root có fragment: manifest/bundle không chứa fragment;
2. fake root có bundled module: module có trong manifest/bundle;
3. fake root thiếu bundled module: `release-manifest`/`release-verify --strict` fail và nêu đúng đường dẫn;
4. generator chạy hai lần và trên Windows/Linux cho byte giống nhau;
5. worker sinh module ứng viên ở temp, không ghi tệp land-only vào diff.

## 4. Thẩm định VIII.1–VIII.8

| Mục | Phán quyết | Khuyến nghị hợp nhất |
|---|---|---|
| VIII.1 Land ADR/Protocol ngay | **Một phần** | Làm ngay bằng một PR docs-only từ `origin/master`, nhưng bỏ tuyên bố “0 tác động gate”. `docs/` không vào release manifest/bundle (`release.py:328-333`) nhưng CI vẫn chạy `doc-claims-check --strict`, và `_DOC_CLAIMS_ORPHAN_EXTRA` gồm `docs/adr/*.md` (`workflow.py:816-820`). Phải chạy gate tài liệu và `git diff --check`. |
| VIII.2 Sửa từ vựng và envelope | **Toàn phần** | Sửa V.1; giữ 30 invocation nhưng ghi rõ trần đầu tiên thắng, reservation và lý do PAUSE như V.2. |
| VIII.3 Ratchet + policy file + seed | **Một phần** | Nhận ratchet có phân loại, không bắt mọi miss thành coupling vĩnh viễn. Chốt file canonical `.github/coordination/change-impact.v1.json` và schema `.github/coordination/schemas/change-impact.v1.schema.json`; JSON giảm phụ thuộc parser và có byte/hash tất định. Seed bằng tool đọc các input đã có của required files, `doc-claims-check`, golden/workflow checks để sinh **candidate report**; human review mới promote rule. |
| VIII.4 Cutover PR cũ | **Toàn phần** | Chọn cửa sổ **zero legacy writer/PR vào lane mới**, không auto-detect lane theo diff. Ghi `activation_base_sha` và `protocol_version`; trước activation phải land/cancel/reroute mọi PR kiểu cũ. Nếu buộc giữ PR lịch sử, nó ở lane legacy allowlist theo PR number và phải land trước khi dispatcher cấp worker packet đầu tiên. |
| VIII.5 Fragment trước EOL | **Toàn phần** | Trong pha 1, land fragment loader/generator/behavior tests trước; writer của generator phải ghi LF tường minh. Thiết kế loader theo wrapper/new files để không rewrite toàn monolith CRLF. Sau đó mới freeze/drain và migration EOL A/B/C. |
| VIII.6 Resolver + exclusion behavior | **Toàn phần** | Thực hiện V.4 và V.5 trong cùng epic fragment harness; đây là acceptance criteria, không để thành follow-up tùy chọn. |
| VIII.7 Snapshot state | **Một phần** | Nhận mục tiêu nhưng thay snapshot định kỳ bằng event journal + checkpoint mỗi transition + reconcile; artifact chỉ backup có hạn. Xem V.3 và P0 bên dưới. |
| VIII.8 `docs/research/` | **Toàn phần** | Land cùng PR hiến pháp. Gắn rõ `non-normative`, ngày đo, mốc commit và nguồn; protocol/ADR thắng nếu nghiên cứu cũ. Không chép nguyên bản góp ý ngoài repo nếu không cần—land báo cáo kiểm chứng/synthesis để giữ provenance. |

### Định dạng change-impact policy đề xuất

```json
{
  "schema_version": 1,
  "rules": [
    {
      "rule_id": "skill-size-doc-claim",
      "trigger": {"type": "exact", "path": "SKILL.md"},
      "write_closure": [
        {"type": "exact", "path": "references/GOTCHAS.md"}
      ],
      "required_checks": ["r219_gotchas_nhan_trang_thai"],
      "land_obligations": [],
      "rationale": "temporary dynamic-size pin",
      "owner": "foundation",
      "expires_when": "size claim is generated or removed"
    }
  ]
}
```

Ratchet chuẩn khi gate phát hiện `IMPACT_POLICY_MISS`:

1. Packet không được accepted chỉ bằng cách thêm file ngoài closure.
2. Phải chọn và audit một trong bốn kết cục: thêm/sửa rule; chuyển thành land obligation; loại/sinh invariant
   động; hoặc ngoại lệ có `owner`, `reason`, `expires_at` và human approval.
3. Thêm regression tái hiện miss và CI kiểm closure từ diff.
4. Rule tạm hết điều kiện phải bị ratchet ngược để thu hẹp policy.

## 5. Trả lời IX.1–IX.8

1. **Có nhận ratchet**, theo ratchet có phân loại ở trên; không tự động hóa coupling ngẫu nhiên thành luật vĩnh viễn.
2. **Chọn zero-legacy-PR/writer tại activation**. Chỉ dùng allowlist PR number như ngoại lệ chuyển tiếp, không
   suy lane từ tên branch/diff.
3. **Giữ `max_agent_invocations: 30` có chủ đích** như trần chi phí độc lập; ghi rõ trần đầu tiên thắng và expose
   phép tính/reservation. Không coi `20 × 3` là quota được bảo đảm.
4. **Có durability**, nhưng dùng event journal + checkpoint sau mỗi transition; artifact/Issue body đơn lẻ không đủ.
5. **Fragments trước EOL**, với loader/writer mới không rewrite monolith và luôn ghi LF.
6. **Policy JSON ở `.github/coordination/`**, schema versioned; dispatcher/platform owner quản; seed từ candidate
   extraction của gate hiện tại rồi human review.
7. **Có mở rộng resolver**, bằng registry/parser ID dùng chung cho cả `r*`, `wp*`, dev fragments và bundled module.
8. **Cho `docs/research/` vào PR**, dưới nhãn non-normative và mốc đo rõ ràng.

## 6. Khoảng hở P0 mới: Actions concurrency không phải durable dispatcher queue

Protocol mục 3.3 hiện nói mọi workflow đổi state dùng cùng concurrency group với
`cancel-in-progress: false`, rồi suy ra dispatcher cập nhật tuần tự. Kết luận “không chạy đồng thời” đúng, nhưng
kết luận ngầm “mọi event đều được xử lý theo thứ tự và không mất” không đúng.

Theo tài liệu GitHub hiện tại, concurrency group mặc định chỉ giữ tối đa một run đang chạy và một run pending;
run pending mới thay run pending cũ. GitHub cũng nói thứ tự bắt đầu không được bảo đảm. Tùy chọn `queue: max` có
thể giữ nhiều pending hơn, nhưng thứ tự vẫn dựa thời điểm bắt đầu chờ, không phải thời điểm dispatch, và queue có
trần. Nguồn chính thức:

- [Workflow syntax — concurrency](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax-for-github-actions#concurrency)
- [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)

### Vá bắt buộc trước dispatcher shadow

1. Comment/dispatch của người dùng hoặc worker là **durable inbox fact** có ID; workflow wake-up chỉ là tín hiệu,
   không phải bản thân hàng đợi.
2. Một reconciler đọc các command chưa xử lý theo thứ tự tất định (issue comment API trả comment theo ID tăng),
   kiểm `expected_state_revision`/generation/spec hash, rồi áp transition idempotent.
3. Dùng concurrency `queue: max` + `cancel-in-progress: false` nếu repo hỗ trợ, nhưng chỉ làm backpressure. Một
   scheduled/manual reconcile phải thu hồi event bị workflow bỏ/lỗi.
4. State projection ghi `last_consumed_event_id`, checkpoint hash và revision. Event tới sai thứ tự không bị mất:
   nó chờ predecessor hoặc bị reject có audit theo state machine.
5. Acceptance test phải bắn ít nhất ba event khi một run đang chạy, chứng minh không event nào mất; cố tình đảo
   lịch chạy; retry cùng event ID; sửa/xóa comment đã consume; và khôi phục sau khi xóa state projection.

Đây phải là promotion gate của pha 3 shadow. Nếu chưa vá, lease/generation có thể đúng trên giấy nhưng event
heartbeat, handoff hoặc pause hợp lệ vẫn có thể biến mất trước khi dispatcher đọc.

## 7. Phương án hoàn thiện cuối cùng

### PR D0 — land hiến pháp, ngay

- ADR-0017…0032, Protocol, glossary/context và các báo cáo nghiên cứu non-normative.
- Sửa `claimed`/complete ownership; làm rõ budget; thêm ratchet contract, cutover contract, thứ tự fragment trước
  EOL, test-ID registry, release-exclusion behavior và state journal/concurrency correction.
- Dựng từ `origin/master` mới nhất trong worktree riêng; chạy `doc-claims-check --strict`, kiểm link/path,
  `git diff --check`; không trộn runtime.

### Epic F1 — fragment infrastructure

- Loader/generator mới, test ID registry cho `r*` và `wp*`, duplicate gate, temp bundled topology và canonical
  bundled module land-only.
- Exclude đúng prefix `planned:scripts/test_fragments/`; bundled module là required release file; khóa năm behavior test
  V.5.
- Writer dùng UTF-8/LF/tất định ngay từ đầu. Legacy selftest mặc định đóng băng.

### Epic F2 — EOL maintenance

- Zero writer/PR window, ghi `EOL_BASE_SHA`.
- Ba commit A policy/validator, B renormalize-only, C regenerate/parity.
- Mọi branch cũ rebase trước khi writer mở lại.

### Epic F3 — protocol/safety và activation

- Change-impact JSON/schema, candidate seed + human promotion, ratchet CI.
- Hai CI lane, branch/security rules, adapters; chưa provider secret.
- Drain PR kiểu cũ, ghi `activation_base_sha`, rồi mới bật nguyên tử deferred numbering + worker gate.

### Epic A3 — dispatcher shadow, chỉ sau foundation

- Durable inbox, event journal, checkpoint/recovery, reconciliation và concurrency stress tests P0.
- Chứng minh race/retry/edit/delete/recovery trước mọi provider secret hay model call.

Các pha automation còn lại giữ đúng ADR-0026 và chỉ promote từng epic. Trật tự này tiếp thu toàn bộ giá trị của
bản góp ý, đồng thời không biến docs-only thành “không cần gate”, artifact thành database, hay Actions concurrency
thành hàng đợi mà nền tảng không cam kết.

## 8. Nguồn kiểm chính

### Repo

- `docs/PROTOCOL_DA_PHIEN.md`
- `docs/adr/0017-pr-github-la-ban-giao-va-dieu-phoi-chinh.md`
- `docs/adr/0025-issue-contract-va-state-machine.md`
- `docs/adr/0026-rollout-theo-promotion-gate.md`
- `docs/adr/0029-budget-guard-cho-agent.md`
- `docs/adr/0030-definition-of-done-cua-mission.md`
- `docs/adr/0031-test-fragment-thay-khoa-toan-cuc-selftest.md`
- `docs/adr/0032-change-impact-rule-co-huong.md`
- `origin/master:.github/workflows/ci.yml`
- `origin/master:scripts/tl_core/release.py:328-505`
- `origin/master:scripts/tl_core/workflow.py:786-820`
- `origin/master:scripts/tl_selftest.py:26097-26124`
- commit `c07384a` và merge `ac63cd7`

### Nền tảng

- [GitHub Actions concurrency](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax-for-github-actions#concurrency)
- [Issue comments REST API](https://docs.github.com/en/rest/issues/comments)
- [Actions issue-comment events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issue_comment)
- [Artifact retention](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-retention-period-for-github-actions-artifacts-and-logs)
- [Claude Code on mobile](https://code.claude.com/docs/en/mobile)
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control)
- [Codex from anywhere](https://openai.com/index/work-with-codex-from-anywhere/)

## 9. Trạng thái hợp nhất sau báo cáo

Các kết luận đã được đưa vào bộ tài liệu chuẩn: `CONTEXT.md`,
`docs/PROTOCOL_DA_PHIEN.md`, ADR-0017, ADR-0025, ADR-0026, ADR-0028–ADR-0032 và ADR-0033 mới. Phần Android
được sửa thành một yêu cầu adapter-neutral `land apply`, không còn coi điện thoại là giới hạn nền tảng.
Nhận xét về Actions concurrency được nâng thành ADR-0033 với durable inbox, reconciler, event journal
và checkpoint nối hash. Ký hiệu `planned:<repo-relative-path>` tách đích đến tương lai khỏi khẳng định
đường dẫn đang tồn tại, để bootstrap documentation vẫn qua đúng cổng doc-claims thay vì né cổng.
