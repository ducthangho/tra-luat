# WP538 — SKILL-PREFLIGHT-REVIEW-LAND, revision 4

## Authority và identity

- packet_issue: 538; packet_id: SKILL-PREFLIGHT-REVIEW-LAND; revision: 4; generation: 4.
- Chỉ thị cấp: https://github.com/ducthangho/tra-luat/issues/538#issuecomment-5695202718 (r4);
  chỉ thị r3: .../issues/538#issuecomment-5694346171; chỉ thị r2: .../issues/538#issuecomment-5668521601.
- Người cấp: ducthangho; recorder r2: Codex desktop; recorder r3 và r4: phiên claude.
  Không recorder nào tự xưng dispatcher.
- Packet kế nhiệm RIÊNG của yêu cầu #523 và bổ sung từ #463; không sửa r11/g10 cũ.
- Liên hệ điều phối #499; #467 chỉ là nguồn sự cố #463, không tự cập nhật mission graph.
- Executor: **antigravity** / **google_antigravity** / **antigravity** — ĐỔI Ở r4, xem khối
  `VÌ SAO CÓ r4`. Codex hết quota nên không sửa tiếp được; chủ kho chuyển việc sang agy.
- Reviewer: **claude** / anthropic / claude_code — ĐỔI Ở r3, xem khối ngay dưới.
- Environment: local; OS: Windows; shell: PowerShell. WSL chỉ cho probe yêu cầu WSL.
- Review class: sensitive. Assurance target: **cross_approved** — đặt ở r3, **r4 GIỮ NGUYÊN**.
  Đổi executor KHÔNG phá được mức này: agy là `google_antigravity`, reviewer là
  `anthropic_claude` — vẫn khác provider, nên cặp vẫn thoả `§8` mục 1.
- Reviewer phải ở session/context/checkout riêng, không fork context Executor; đọc spec/diff
  và tự đo. Điều kiện `xhigh > high` của CÙNG model là của r2 và **KHÔNG còn áp ở r3**: reviewer
  nay KHÁC NỀN, nên điều kiện bắt buộc là **provider khác provider của executor**, không phải
  effort cao hơn trong cùng model.
  CLI header/receipt phải chứng minh model/effort; mất bằng chứng hoặc fallback thì không
  nhận approve. Không suy model từ tài khoản GitHub hoặc từ cấu hình yêu cầu.
- Đây là cấu hình được giao; spec không khẳng định đã có lời gọi model hay review hoàn tất.

## VÌ SAO CÓ r3 — `same_provider_approved` KHÔNG đủ cho class `sensitive`

**r3 đổi ĐÚNG HAI trường: `Reviewer` và `Assurance target`. Không gì khác.** Executor vẫn là codex,
write set không đổi, `review_class` vẫn `sensitive`, toàn bộ nghĩa vụ/gate/điều kiện dừng giữ nguyên.

Lý do không phải "cho chắc hơn" mà là một câu trong protocol:

> `docs/PROTOCOL_DA_PHIEN.md` §8, dòng 580:
> **`same_provider_approved` vẫn không thay `cross_approved` cho class `sensitive`.**

WP538 là `sensitive`. Approve đã có ở r2 là **codex chấm codex** dưới *"scoped owner same-provider
exception"*. Theo dòng 580, mức ấy **không thay** `cross_approved` ở class này — nên packet **chưa**
đạt mức assurance mà chính nó đòi, dù verdict r2 là `APPROVE` và không P1/P2/P3.

Điều đáng ghi: **chính spec r2 đã tự nói ra điều đó** mà không rút ra kết luận. `R15` của r2:

> *"Assurance suy từ cặp provider/runtime độc lập và evidence. **Cùng provider không trở thành
> cross-provider vì đổi model/session**; same_provider_approved chỉ hợp lệ trong điều kiện canon
> cho phép."*

`xhigh > high` của CÙNG model là một phép tăng **effort**, không phải một phép đổi **provider**. r2
đã khai đúng nguyên tắc rồi vẫn nhận một approve cùng nền — đó là chỗ r3 sửa.

§8 dòng 849 nói thẳng cách duy nhất được phép ghi nhận mức ấy:

> *"nếu cùng provider thì phải là phiên mới và mang `same_provider_approved`, **không giả thành
> cross-review**"*

Nên verdict r2 **không bị huỷ và không bị gọi là sai** — nó là một `same_provider_approved` hợp lệ,
ghi đúng tên. r3 chỉ nói rằng với `sensitive`, cần thêm một lượt **khác nền** nữa.

*Ghi rõ phần KHÔNG đo được:* r3 **không** khẳng định verdict r2 bỏ sót lỗi nào. Lượt cross-provider
có thể ra `approve` không thêm finding nào — và **một kết luận sạch có giá ngang một phát hiện**.
Thứ r3 sửa là **mức assurance được ghi**, không phải chất lượng của lượt review trước.

## Ngoại lệ điều phối r2 — phạm vi riêng WP538

Do packet_loop init từ chối codex/codex rc=4, thực hiện chỉ thị same-provider bằng
nhật ký/receipt Issue và ops/reviews/wp538/, không ghi tay .packet_state và không khai
đã qua state machine tự động. Không giả reviewer Claude hoặc sửa runtime ngoài scope.
Launcher, exact-SHA, clean checkout, quyền ghi, model/effort và deadline vẫn được đo.
Mỗi lượt có ID, SHA, thời điểm, artifact hash, danh tính thực tế, verdict và bảng lớp.
Chỉ thị chủ kho: https://github.com/ducthangho/tra-luat/issues/538#issuecomment-5668521601.
R1 là lịch sử; các yêu cầu nội dung không bị rút trong r2 giữ nguyên bên dưới.
Lease r1 chỉ được thêm da_bi_thay_the liên kết r2; spec r1 không sửa bytes.

## Baseline và nguồn

- base_sha / immutable acceptance baseline: c66415aa8dabb48a23fc23751a1eb54aab0330eb.
- base_tree: 8ea03f4c12845fe8011c5fb9103faef15964c66c.
- Branch: codex/wp538-r1-g1; branch ownership: exclusive — **CHUYỂN GIAO Ở r4 sang antigravity**.
  Giữ nguyên TÊN nhánh vì đó là head của PR #539; đổi nhánh là bỏ PR. Tên nhánh mang dấu vết
  lịch sử, còn quyền ghi đi theo VAI executor. Codex KHÔNG còn quyền ghi nhánh này.
- target_branch_neu_land: master (chỉ là đích dự kiến; chưa cấp quyền land).
- start_from_sha ban đầu bằng base_sha; reviewed candidate sẽ lấy HEAD sau thi công,
  không thay immutable baseline khi lease tiếp tục.
- Input #529: c08d845a88dc588eb839fc5bb7ee7b50b4ac481f. Dùng làm hồ sơ/ý định để tái
  dẫn xuất trên canonical base, không coi là predecessor đã integrated hoặc cherry-pick mù.
- Input spec #523 r11: ops/specs/QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG-r11.md trên
  claude/spec-quy-trinh-r11-20260913, SHA-256
  42b0f477b7db2b1cb954ee9a345c9fcc1a2fb805ec9c260461187180fdc4226b, 40257 bytes.
- Input #463: https://github.com/ducthangho/tra-luat/issues/463#issuecomment-5667674547.
- Gói nháp trước cấp quyền không là candidate approved; tiếp nhận từng đoạn theo spec này.

## Objective, write set và ranh giới

Cập nhật quy trình candidate preflight, fresh reviewer bootstrap và land evidence.
Nguồn doctrine là protocol; ba skill gốc và ba adapter Codex chứa cú pháp/công cụ/con trỏ.
Không nhét định nghĩa mới vào adapter để tránh sửa nguồn doctrine.

Write-set chính xác (prefix duy nhất có dấu `/` cuối):

- `docs/PROTOCOL_DA_PHIEN.md`
- `.claude/skills/work-packet/SKILL.md`
- `.claude/skills/cross-review/SKILL.md`
- `.claude/skills/land-packets/SKILL.md`
- `.agents/skills/work-packet/SKILL.md`
- `.agents/skills/cross-review/SKILL.md`
- `.agents/skills/land-packets/SKILL.md`
- `ops/specs/wp538-skill-preflight-review-land-r2.md`
- `ops/leases/wp538-r2-g2-codex-windows.yaml`
- `ops/leases/wp538-r1-g1-codex-windows.yaml` (chỉ thêm bia mộ thay thế r2)
- `ops/reviews/wp538/`

Đây là write-set được chủ kho cấp theo gói đã trình, không tự suy `effective_write_set`
từ một policy chưa có. Cổng bootstrap lease tính review class là sensitive; trước thi
công phải đọc lại tình trạng change-impact/closure trên canonical. Nếu công cụ closure
chưa có, khai nợ #473 và mức assurance bằng chứng, không tự xuất bốn trường phái sinh
như thể dispatcher đã tính. Có coupling mới cần path khác thì dừng/revision.

ADR-0044: khai lý do gói >3 file — 3 skill và 3 adapter phải đồng bộ cùng nguồn protocol.
Phạm vi hữu hạn là 7 file sản phẩm; spec/lease/review là hiện vật điều phối. Không miễn
đếm adapter mới: đo một endpoint baseline→candidate, ghi riêng số sản phẩm và hiện vật.
Ba nhóm được soi riêng trong một review; đây không phải cách reset attempt hoặc finding.
Không có quyền thay các trần budget qua phần giải trình kích thước này.

Không sửa launcher, packet_loop.py, hooks, workflows, release manifest, CHANGELOG,
root SKILL.md, secrets, ruleset thực hoặc bất kỳ hồ sơ đóng băng của #523/#463.
Không dùng packet mới để đóng #523/#467/#499 hoặc tuyên bố các mission complete.

## Acceptance: hai mươi yêu cầu bổ sung

Reviewer phải đọc từng yêu cầu, kiểm con trỏ tới đúng nội dung và phân biệt lời hướng dẫn
với bằng chứng runtime. CLI example mới được parse và thử trên dữ liệu vô hại hoặc snapshot;
không thử mutation GitHub/merge/LIVE như một test của tài liệu.

| ID | Nơi dự kiến | Nghĩa vụ |
|---|---|---|
| R01 | §10.2 | Trước freeze/review cuối, ghi CI plan và đo khả năng sinh required contexts: marker/trailer, event, filters, candidate và ngân sách. Marker chặn event cần thiết phải được xử lý trước freeze; không sửa SHA sau review rồi tái dùng verdict. Ngoại lệ skip hậu merge cần authority riêng. |
| R02 | §10.2 | Đo canonical ancestry và preflight admission bằng mã canonical trước thao tác tốn gate. Rc 1 là không ancestor; lỗi đọc không phải kết luận ancestry. Local admission trước PR không thay receipt CI sau PR; thứ tự job tự động cần workflow support riêng. |
| R03 | §3.2/§7 | Ghi riêng continuation base, reviewed candidate và immutable acceptance baseline kèm authority. Đổi lease không di chuyển baseline nghiệm thu. Thay baseline phải có quyết định và revision phù hợp; không tự ghi thêm trường không được schema nhận. |
| R04 | §10.2 | Evidence CI tách run head, checkout SHA/parents/tree, workflow-definition SHA và nguồn từng dữ kiện. Synthetic merge phải được chứng minh từ checkout/log/artifact; tree tương đương không đồng nhất commit, thời điểm hoặc loại test. |
| R05 | §10.2 | Workflow definition lấy từ provenance có exact OID, trong lane GitHub có thể dùng WorkflowRun.file.repositoryFileUrl và tải blob để băm. REST head không thay provenance; trường thiếu/403 là chưa đo. |
| R06 | §10.2 | Probe toàn bộ dependency của heavy gate trong chính runtime sẽ chạy: Git, Python/modules, jq, actionlint, shell và công cụ được command gọi. Windows host xanh không chứng minh WSL xanh. |
| R07 | §10.2 | Job skipped không có runner là chưa thực thi; chỉ gắn owner_waived khi có waiver đúng scope. Không tính pass hay Windows execution, không làm mất yêu cầu còn thiếu khi không có waiver. |
| R08 | §13 land | Ruleset mutation cần quyền riêng: snapshot đầy đủ, payload chỉ writable fields, diff đúng trường được phép, read-before-write và readback sau write. Giữ integration ID cùng trường ngoài scope; nếu upstream đổi giữa hai lần đọc thì dừng. Không hứa tính nguyên tử khi API không cung cấp. |
| R09 | §10.2 | API thiếu quyền ghi not_measured cho đúng endpoint; fallback GraphQL aggregate → jobs/logs → statuses không tự nâng chất lượng chứng minh. Chỉ nhận bằng chứng đủ SHA/attempt/context và nội dung dương. |
| R10 | §10.2/spec consumer | Tiêu chí mutant riêng cần receipt dương/âm cho đúng consumer/tiêu chí. A7 chỉ bắt buộc ở packet có A7; số tổng suite không thay phép đo ấy. |
| R11 | §5.1/§13 land | Fence đổi phải có delta đầy đủ tên/old/new ref; synthetic merge đòi parents/tree giải thích. Fence mới chỉ được nhận trong authority được cấp; không loại refs/pull khỏi phép đếm hoặc coi head/base khác là vô hại. |
| R12 | §4/§13 land | Executor lease và land authority có hạn/phạm vi riêng. Hết executor lease không gia hạn sửa code; thao tác hậu merge còn được phép phải được liệt kê trong land authority còn hiệu lực. |
| R13 | §8 | Reviewer clone phải bootstrap bằng remote thật, path/trust đúng nền, longpaths khi cần, tool/env capability. Không tự chấp nhận trust hay bypass permission. Bootstrap hoàn tất trước khi giao checkout read-only. |
| R14 | §8/§7 | Receipt đối chiếu rc con, model evidence, permission denials, stable artifacts và exact SHA/tree đầu/cuối. Launcher rc=0 hoặc actor GitHub không chứng minh model reviewer. |
| R15 | §8 | Assurance suy từ cặp provider/runtime độc lập và evidence. Cùng provider không trở thành cross-provider vì đổi model/session; same_provider_approved chỉ hợp lệ trong điều kiện canon cho phép. |
| R16 | §8 | Ghi Ruff pin/probe contract và bare Ruff lint riêng cùng command/rc/scope. Không dùng nhãn Ruff passed khi bare lint chưa đo hoặc đang đỏ. |
| R17 | §8 | Cache ngoài checkout hoặc no-cache; read-only snapshot kiểm ignored/untracked/tracked. Snapshot sạch không chứng minh chưa từng ghi; khai giới hạn quan sát. |
| R18 | §7/§13 land | Biên nhận đăng comment có ID, raw JSON parse, body/hash exact readback. Cú pháp body file nằm trong adapter, không đóng băng CLI thành doctrine. |
| R19 | §10.2 | Báo riêng merged, landed, packet complete, mission complete và căn cứ từng trạng thái. Hoàn tất một packet không đóng các dependency/packet khác. |
| R20 | §3.2 | Spec authoritative được xác minh từ nguồn blob/hash chỉ định. Bản trong product tree cũ không cho phép ghi ngoài write-set; source-of-truth và local copy được báo riêng. |

## Bảo toàn công việc #523

N1–N8/M16 và slug trong spec #523 là hồ sơ bất biến. Nếu tái dẫn xuất nội dung vòng review,
giữ nghĩa vụ đếm theo lớp/đơn vị nghĩa, phạm vi đo và giới hạn evidence; reviewer tự dựng
thước cho các nghĩa vụ đó, executor không tự phán nghiệm thu.
Giữ bảng truy vết bốn lớp còn mở: dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi;
bien-nhan-thieu-so-ci-da-chi; phep-do-doctrine-khong-du-rang;
bien-nhan-luot-8-lan-du-lieu-luot-6. Không reset lịch sử vì đổi số packet.
Receipt đã giao không sửa bytes; correction mới chỉ ghi dưới ops/reviews/wp538/ và phải
nối lại nguồn cũ cùng phạm vi sửa. Nợ scanner và hợp đồng bổ sung receipt lượt 5 chưa
được giao sửa runtime/hợp đồng trong packet này; ghi unresolved, không nhận là đóng.
Packet mới hoàn tất phần 20 yêu cầu không đồng nghĩa #523 được approve hay complete.

## Gate và ngân sách

- Trước mọi ghi: đọc lại exact head/base, full sorted remote refs + hash, lease/hạn,
  write-set/exclusion. Ref đổi thì dừng ghi, phân tích delta và cập nhật fence chỉ khi
  xác minh không xung đột hoặc đã tích hợp có kiểm tra theo chỉ thị r2.
- Metadata: lease_publish check + kiem-github; spec blob hash = disk hash; exact readback
  Issue/comment và remote branch. Không coi code 0 thiếu bằng chứng dương là pass.
- Nội dung: doctrine-scan gồm .agents paths, adr-song, doc-claims-check --strict,
  bien_nhan_v2, git diff --check, release-verify --strict --json với ok=true và
  expected_file_count == checked_file_count. Xác định đúng cú pháp ở canonical tool.
- core.abbrev=7; Python gọi theo interpreter đã resolve. Cache/output đặt ngoài checkout.
- Chỉ chạy targeted local cho diff. KHÔNG CI, full CI hoặc CI Windows trong vòng
  vá/review; không mở PR/dispatch gây chạy tự động. Verdict đăng Issue #538. Chỉ đẩy
  nhánh riêng khi đã kiểm trigger không chạy workflow. CI chưa chạy ghi not_run.
- Vòng lặp theo chỉ thị r2: sửa theo LỚP → reviewer độc lập → đăng verdict → sửa tiếp,
  đến approve hoặc hết P1/P2; không tự đổi slug/reset lịch sử. Trần hai lần gọi r1
  không còn áp; giữ deadline 90 phút/run, heartbeat 30 phút, checkpoint khi quota,
  permission, không đo được hoặc cùng lớp không hội tụ cần đổi cách làm.
- Lease 24 giờ từ thời điểm ghi, hạn cụ thể trong YAML. Hết hạn không bắt đầu run mới.
- Không có merge/land/deploy/LIVE authority. Ruleset section chỉ là tài liệu.

## Done và stop

Done của thi công là diff trong scope, gate có bằng chứng, reviewer độc lập đúng model/
effort cao hơn xác nhận exact candidate, receipt và handoff được đọc lại. Không tự nhận
same_provider_approved từ việc owner cho phép fallback hoặc từ việc cấp lease.
Dừng nếu stale lease/spec/head, thiếu năng lực reviewer, permissions deny, path ngoài
scope, nghĩa vụ cần đổi, con trỏ không có đích, gate thiếu evidence hoặc budget cạn.

## Công thức đóng băng

spec_hash = SHA-256 của toàn bộ bytes UTF-8/LF file này. Hash lưu ngoài file (lease và
Issue receipt) để không có vòng tự băm. Thay bytes sau cấp quyền cần revision/generation
mới theo protocol; không amend spec đã công bố để làm khớp nội dung.

## VÌ SAO CÓ r4

`§3.2`: đổi **executor** tạo revision mới và làm lease cũ mất hiệu lực. Chủ kho chỉ thị nguyên văn:
*"#539 là các lỗi đơn giản, hãy cho anti gravity sửa (agy) vì Codex đã hết quota không sửa được
nữa"*. Nên đây là r4 + g4 + cấp lại lease, không phải một phép vá vào g3.

Không phải thủ tục suông: g3 khai `executor: codex` và `branch_ownership: exclusive` cho codex. Để
agy ghi vào đúng nhánh ấy mà không đổi lease là **ghi ngoài thẩm quyền** — đúng thứ write-set
exclusion sinh ra để chặn.

**r4 đổi ĐÚNG HAI thứ: `Executor` và chủ sở hữu nhánh.** Cộng một khối khai ngân sách DÒNG ở dưới,
là thứ chủ kho chọn khi được hỏi. `Reviewer` vẫn claude, `Assurance target` vẫn `cross_approved`,
`review_class` vẫn sensitive, `base_sha` vẫn `c66415aa`, write set sản phẩm vẫn đúng bảy tệp ấy.

## VIỆC CỦA r4 — ĐO ĐƯỢC, KHÔNG MÔ TẢ CHUNG

Lượt CI **tự động** trên `f2aa1f9f` (run `34914089592`) cho `gate (ubuntu-latest)` **failure**.
Nguyên nhân là `.claude/dev/idiom_py_test.py`, hai ca đỏ:

```
ĐỎ  ba_nen_path:   idiom#4 trên nền chỉ có python: rc=127; trên nền chỉ có py: rc=127
ĐỎ  hop_dong_khoi: 4 khối sai hợp đồng:
      .claude/skills/cross-review/SKILL.md:566  THIẾU_GÁN
      .claude/skills/work-packet/SKILL.md:38    THIẾU_GÁN
      .claude/skills/work-packet/SKILL.md:61    THIẾU_GÁN
      .claude/skills/work-packet/SKILL.md:100   SAI_DẠNG
```

**Delta là của packet này, không phải đỏ sẵn.** Đo một biến — cùng container, cùng lệnh, chỉ khác
commit: `origin/master` ⇒ **7/7 đạt, 0 đỏ**; `f2aa1f9f` ⇒ **5/7 đạt, 2 đỏ**.

**Hai ca đỏ có MỘT gốc.** `work-packet/SKILL.md:100` viết `PY="$(command -v python3)"` — giải MỘT
tên. Trên nền chỉ có `python`, hoặc chỉ có `py`, `$PY` rỗng nên khối thoát `rc=127`: đó chính là
`ba_nen_path`. Đúng luật đang có trong `CLAUDE.md`: *"Không được giả định Windows có `python3`"*.
Ba khối còn lại dùng `"$PY"` mà không có phép gán nào trong khối.

Dạng chuẩn cổng đòi, nguyên văn từ `.claude/dev/idiom_py_test.py:55`:

```
PY="$(command -v python3 || command -v python || command -v py)"
```

### A-r4-1 — bốn khối idiom

Thay phép gán một-tên ở `work-packet/SKILL.md:100` bằng idiom BA TÊN trên, và thêm đúng dòng ấy làm
**dòng đầu** của ba khối `THIẾU_GÁN`. Phép gán phải đứng TRƯỚC lần dùng `"$PY"` đầu tiên trong cùng
khối — cổng tố cả `GÁN_MUỘN`, nên đặt cuối khối là vẫn đỏ.

Chốt: `python3 .claude/dev/idiom_py_test.py` phải về **7/7 đạt, 0 ĐỎ** — hai số bằng nhau, đọc `rc`
trực tiếp, không qua pipe. Đây là cùng con số mà `origin/master` cho, nên tiêu chí là ĐẠT NỀN,
không phải "đỡ đỏ hơn".

### A-r4-2 — merge base

`thu-hoi` hiện **rc=12**: `workflow_sha 19de5669 != S c66415aa — định nghĩa không neo canonical`.
Đó là **base drift**, không phải lỗi nội dung. Merge `origin/master` (`19de5669`) vào nhánh packet
bằng **merge commit**; không rebase, không force-push — nhánh này là head của một PR đang mở.

`immutable_acceptance_baseline` **KHÔNG đổi** theo phép merge này: nó vẫn là `c66415aa`. Merge base
làm cổng đo được, nó không dời mốc nghiệm thu.

### A-r4-3 — phạm vi

Chỉ hai tệp sản phẩm bị đụng (`work-packet/SKILL.md`, `cross-review/SKILL.md`), cả hai đã trong
write set. **Không nới phạm vi**, không đụng `.claude/dev/idiom_py_test.py` để cổng hết đỏ — sửa bộ
đo thay vì sửa thứ nó đo là hành vi bị cấm ở mọi revision của packet này.

### KHÔNG làm

Không gọi CI tay, không `workflow_dispatch`, không lane `windows` trước merge (`manual_ci_budget: 0`).
Chỉ thị chủ kho nguyên văn: *"CI Window gặp lỗi đã biết, để đỡ tốn tiền, không chạy CI Windows"*.
`gate (windows-latest)` và `gate-registry (windows-latest)` đang đỏ trên `f2aa1f9f` thuộc đúng lớp
lỗi Windows đã biết ấy; r4 **không** giao việc chữa chúng và **không** miễn trừ chúng.

## KHAI NGÂN SÁCH DÒNG CHO ADR-0044 — đóng finding P2

Lượt cross-review claude trên `f2aa1f9f` mở P2 `adr-0044-khai-ngoai-le-chi-phu-mot-trong-hai-nguong`:
ADR-0044 cho `sensitive` đặt **≤ 3 tệp VÀ ≤ 300 dòng thêm**; đo trên `c66415aa..f2aa1f9f` giới hạn ở
tệp sản phẩm ra **7 tệp / +772 dòng**, vượt CẢ HAI. Dòng 111–112 của r3 khai ngoại lệ hoàn toàn theo
khung SỐ TỆP; không một con số dòng nào xuất hiện. Chủ kho chọn khai ngân sách dòng, nên r4 khai:

- **Ngưỡng bị vượt:** 300 dòng thêm. **Đo được:** +772. **Bội số:** 2,6×.
- **Vì sao không tách nhỏ được theo DÒNG:** sáu tệp adapter (`.claude/skills/*` và `.agents/skills/*`
  cho `work-packet`, `cross-review`, `land-packets`) phải trỏ CÙNG một nguồn protocol tại CÙNG một
  thời điểm. Tách thành nhiều packet thì giữa hai lần land sẽ có một cửa sổ mà một nửa adapter trỏ
  luật cũ và một nửa trỏ luật mới — mà `doctrine-scan` không bắt được trạng thái nửa vời ấy, vì nó
  đo adapter có CHÉP doctrine hay không, không đo adapter có ĐỒNG BỘ với nhau hay không. Chi phí của
  một cửa sổ như thế cao hơn chi phí của một packet lớn.
- **Thừa nhận, không né:** ADR-0044 neo ngưỡng dòng từ dữ liệu số VÒNG REVIEW của chính kho —
  `PLAT-M4` +351 ⇒ 1 vòng / 1 finding; `PLAT-X4` **+721 ⇒ 3 vòng / 8 finding**. **+772 nằm TRÊN**
  đúng điểm mà ADR dẫn ra làm bằng chứng "đã quá lớn". Khai ở đây nghĩa là ta biết mình đang ở đâu
  trên thang ấy và chấp nhận trả giá bằng số vòng review, **không** phải ta cho rằng ngưỡng ấy sai.
- **KHÔNG miễn trừ gì.** Khối này là một lời KHAI theo đòi hỏi của ADR-0044, không phải một phép
  miễn. Mọi nghĩa vụ review và cổng của packet giữ nguyên.

Finding P3 `hien-vat-review-wp538-khong-co-trong-kho` của cùng lượt **đã đóng một phần** bằng
`ops/reviews/wp538/wp538-review-1-claude-verdict.md` (`sha256`
`8d778449060d6863b1d363e4a86d00f302fe3c055ae31da1938a3a44bcff9e79`) và biên nhận v2 bên cạnh. Phần
CÒN LẠI đã khai trong chính biên nhận ấy và **không** được đọc là đã đóng: ba cổng chạm
`ops/reviews/` đều glob TẦNG ĐẦU, nên hiện vật nằm ở thư mục con không cổng nào chấm. Đóng hẳn đòi
một quyết định của chủ kho (nới write set, hay đổi ba cổng sang `rglob`); r4 **không** tự quyết.
