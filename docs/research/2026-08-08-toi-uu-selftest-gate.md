# Tối ưu selftest và full gate cho quy trình packet

- **Ngày nghiên cứu:** 2026-08-08 (Asia/Saigon)
- **Repo/head được kiểm:** `ducthangho/tra-luat` tại `f27287c9379ba6640bc14604d4ccc9afe228861a`
- **Phạm vi:** chiến lược test/gate; không sửa code, workflow hay protocol
- **Nguồn:** cây Git hiện tại và tài liệu chính thức của Google, Bazel, pytest/pytest-xdist, GitHub
- **Tính chất:** báo cáo nghiên cứu non-normative; protocol/ADR và workflow đã land mới là nguồn quy tắc.

## 1. Kết luận ngắn

**Có, nên ngừng chạy toàn bộ 1.696 selftest trong mọi phiên Executor/packet.** Mô hình phù hợp hơn là:

1. mỗi packet chạy gate nhanh, bất biến bắt buộc và test bị ảnh hưởng;
2. full suite chỉ chạy tại checkpoint tích hợp/land quan trọng trên exact candidate;
3. full hoặc extended suite tiếp tục chạy ở canonical/post-merge và release artifact khi exact tree/artifact khác;
4. selector phải fail-closed và luôn có safety net full-suite để bắt mapping drift.

Nhưng **không nên lập tức thêm cờ lọc tên vào harness hiện tại rồi bỏ full selftest**. `tl_selftest.py` hiện không
phải tập 1.696 test unit độc lập: nhiều biểu thức test chạy eager trong một hàm gần 30.000 dòng, chia sẻ module/global
state và monkeypatch. Lọc danh sách kết quả ở cuối không giảm thời gian; chia shard trước khi cô lập còn có thể đổi
ngữ nghĩa và tạo xanh giả/đỏ giả.

Thứ tự đầu tư khuyến nghị là:

> **đo thời gian → tạo test case/group thực thi độc lập → shard/parallel full suite → affected-test selection ở
> shadow mode → giảm tần suất full suite per-packet.**

Số lượng 1.696 không tự nó là vấn đề. Chi phí nằm ở thời gian từng ca, setup lặp lại, I/O, topology bundle, các gate
trùng công việc và đường chạy tuần tự. Google phân biệt test theo **size** (tài nguyên/thời gian/cách chạy) và
**scope** (phần hành vi được kiểm), đồng thời nhấn mạnh test nhỏ thường nhanh và tất định hơn; số dòng hay số ca
không phải thước đo size. Xem [Software Engineering at Google — Testing Overview](https://abseil.io/resources/swe-book/html/ch11.html).

## 2. Trạng thái vật lý của repo

### 2.1. Full gate hiện tại

`.github/workflows/ci.yml:21-115` có một job matrix Linux/Windows. Trên mỗi OS, các bước chạy tuần tự gồm compile,
EOL, bundled topology, generator selftest, toàn bộ `tl --selftest`, workflow audit, golden, doc claims,
determinism, release check, manifest verify, hai lần build bundle và boot smoke. Matrix đã cho hai OS chạy song
song khi runner sẵn có, nhưng bên trong mỗi OS chưa có song song hóa theo nhóm gate.

Việc giữ parity hai OS là có căn cứ nội bộ: comment workflow ghi nhận lỗi encoding/path/symlink và lỗi topology
bundle từng lọt qua gate một nền (`.github/workflows/ci.yml:3-8,72-83`). Vì vậy không nên bỏ Windows/Linux parity
khỏi checkpoint land/release. Có thể chỉ giảm parity ở inner loop/packet đối với nhóm đã chứng minh platform-neutral.

### 2.2. Harness là monolith có thứ tự và state chung

Các đặc điểm quan trọng:

- `scripts/tl_selftest.py:47-56` tạo `cases=[]`, chụp function/class của module dùng chung, rồi thực thi biểu thức
  test ngay khi `append`; đây không phải đăng ký callable để runner chọn sau.
- `scripts/tl_selftest.py:49-55` nói rõ nhiều test monkeypatch `_TL_MODULE`, và test cuối phải bắt việc quên restore
  vì stub có thể sống tiếp làm các test sau xanh giả.
- helper `_t110` ở `scripts/tl_selftest.py:9100-9106` cũng gọi `fn()` ngay khi đăng ký.
- fragment packet được discover rồi chạy bên trong chính full harness tại `scripts/tl_selftest.py:29305-29320`.
- tally chỉ diễn ra sau khi mọi code phía trên đã chạy (`scripts/tl_selftest.py:29744-29748`).
- `scripts/tl.py:1236-1270` đã có điểm tốt: mỗi full run ghim profile, chặn mạng mặc định và dùng cache dir tạm;
  đây là nền để tiếp tục tăng hermeticity.

Hệ quả: selector phải chặn **trước khi thực thi case**, không phải lọc `cases` sau cùng. Parallelism phải bắt đầu
từ process/group độc lập hoặc từ việc refactor ca thành callable có setup/teardown rõ, không chia dòng tùy ý trong
hàm `run()` hiện tại.

### 2.3. Protocol đã có đúng seam khái niệm

Thiết kế hiện tại đã đi đúng hướng:

- test mới thuộc packet nằm trong `scripts/test_fragments/wp<issue>_<slug>.py`; legacy harness mặc định không thuộc
  packet thường (`docs/PROTOCOL_DA_PHIEN.md:267-271`);
- F3-06 dự kiến worker gate gồm fragment tests, evidence/write-set/EOL/security; F3-07 là land gate sinh artifact và
  parity (`docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md:133-148`);
- `land prepare` đã được xác định là checkpoint generate derived files và chạy parity/full gate
  (`docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md:224-230`).

Vì thế tối ưu đề xuất không thay doctrine cốt lõi; nó làm rõ **khi nào full suite cần chạy** và những điều kiện kỹ
thuật để worker gate thật sự nhanh mà không fail-open.

## 3. Best practices từ nguồn chính thức

### 3.1. Presubmit nhanh, post-submit/RC rộng hơn

Google nêu trực tiếp rằng chạy mọi test ở presubmit là quá đắt; test có thể giới hạn theo scope hoặc chọn theo xác
suất phát hiện lỗi. Quy tắc kinh nghiệm của họ là presubmit chỉ giữ test **nhanh và tin cậy**, chấp nhận bớt coverage
nếu post-submit bắt phần lọt và tổ chức chấp nhận/có cơ chế rollback. Xem [Continuous Integration — Why presubmit
isn't enough và Presubmit versus post-submit](https://abseil.io/resources/swe-book/html/ch23.html).

Cùng nguồn đó yêu cầu Continuous Build chạy mọi test liên quan sau submit, và giải thích vì sao release candidate
vẫn cần comprehensive suite: sanity, auditability, cherry-pick và emergency path. Đây là căn cứ cho mô hình nhiều
tầng, không phải căn cứ để bỏ full suite hoàn toàn. Xem [Continuous Build và Release candidate testing](https://abseil.io/resources/swe-book/html/ch23.html).

Google cũng khuyên giảm scope hoặc tách test lớn thành các test nhỏ hơn để chạy song song trước khi dùng mẹo hạ
coverage. Xem [Large Tests — Speeding up tests](https://abseil.io/resources/swe-book/html/ch14.html).

### 3.2. Chọn test theo dependency/impact, không chỉ theo tên file

Mẫu mạnh là changed path → module/target → reverse/transitive dependants → test. Google CI chạy cả test trực tiếp
bị ảnh hưởng lẫn test phụ thuộc bắc cầu vào file đổi; Bazel có phép `rdeps` để tìm reverse dependency trong closure.
Xem [Software Engineering at Google — Large-Scale Changes](https://abseil.io/resources/swe-book/html/ch22.html) và
[Bazel Query Guide — Reverse dependencies](https://bazel.build/query/guide#reverse-dependencies).

Android `TEST_MAPPING` là ví dụ first-party gần với change-impact policy của repo: mapping presubmit/postsubmit
được đặt cạnh source; đổi file trong directory/subdirectory kích hoạt test mapping của directory và các mapping cha.
Xem [Google Testing Blog — Android Platform Testing Made Easy](https://testing.googleblog.com/2019/01/android-platform-testing-made-easy.html).

Với repo này, không cần chuyển sang Bazel để dùng nguyên tắc đó. `change-impact policy` dự kiến có thể là dependency
catalog nhỏ, explicit và reviewable. Điều quan trọng là selector tính closure, không phải suy từ basename của một
module rồi chỉ chọn các test tình cờ chứa basename đó trong tên.

### 3.3. Marker/filter phải typed và được kiểm lỗi

pytest hỗ trợ chọn theo marker (`-m`), node ID và tên (`-k`). Tài liệu cũng khuyên đăng ký marker; `strict_markers`
biến marker gõ sai thành lỗi thay vì âm thầm deselect. Xem [pytest — Working with custom markers](https://docs.pytest.org/en/stable/example/markers.html)
và [pytest — strict markers](https://docs.pytest.org/en/stable/how-to/mark.html#raising-errors-on-unknown-marks).

Mẫu áp dụng cho custom harness: group/tier/platform/hermeticity phải là enum/schema machine-readable; group lạ,
path chưa map hoặc mapping parse lỗi phải **escalate full**, không trả về tập test rỗng.

`pytest --lf` chỉ chạy test đã fail ở lần trước, còn `--ff` chạy test fail trước rồi chạy phần còn lại. Vì vậy
last-failed hữu ích cho vòng debug cá nhân nhưng không đủ làm evidence merge/land. Xem [pytest cache — rerunning only
failures](https://docs.pytest.org/en/stable/how-to/cache.html#usage).

### 3.4. Sharding/parallelism chỉ an toàn sau isolation

Bazel mô tả sharding bằng nhiều invocation runner, mỗi shard nhận tổng số shard và chỉ số shard; chính test runner
phải hỗ trợ chọn ca. Bazel đồng thời yêu cầu test hermetic, chỉ dùng dependency đã khai báo, vì non-hermetic test
làm mất khả năng tái hiện lịch sử và truy thủ phạm. Xem [Bazel Test Encyclopedia — hermeticity và test sharding](https://bazel.build/reference/test-encyclopedia).

pytest-xdist có thể chạy `pytest -n auto`; các mode `loadscope`, `loadgroup`, `loadfile` giữ nhóm cùng process, còn
`worksteal` cân bằng tốt hơn khi duration lệch lớn. Nhưng mỗi worker vẫn full-collect, collection và thứ tự phải giống
nhau; stdout/PDB cũng có giới hạn. Xem [pytest-xdist — Distribution](https://pytest-xdist.readthedocs.io/en/stable/distribution.html),
[How it works](https://pytest-xdist.readthedocs.io/en/stable/how-it-works.html) và
[Known limitations](https://pytest-xdist.readthedocs.io/en/stable/known-limitations.html).

Do harness hiện có order/global-state coupling, không nên áp xdist hay chia modulo trực tiếp. Nên chạy từng
**group process-isolated**, rồi mới cân shard bằng số đo duration lịch sử. Test cố ý serial được đánh dấu riêng.

GitHub Actions matrix hỗ trợ các shard chạy song song và `max-parallel` để giới hạn tải; `fail-fast` quyết định có
hủy matrix còn lại khi shard bắt buộc fail. Xem [GitHub Actions — matrix, failure handling và max-parallel](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations).

### 3.5. Cache chỉ đúng khi input đầy đủ và test hermetic

Bazel mặc định chỉ tái dùng test result khi test/dependency không đổi; test external, test được yêu cầu chạy nhiều
lần hoặc test đã fail sẽ bị chạy lại trong chế độ `auto`. Xem [Bazel `--cache_test_results`](https://bazel.build/docs/user-manual#flag--cache_test_results).
Bazel remote cache hoạt động vì action khai rõ input, output, command line và environment; build tái hiện được thì
output máy khác mới có thể tái dùng an toàn. Xem [Bazel Remote Caching](https://bazel.build/remote/caching).

GitHub Actions dependency cache chỉ nên dùng để giảm setup/download; key nên chứa OS và hash lockfile. Cache không
được chứa secret và không nên được hiểu là bằng chứng “test đã xanh” của SHA khác. Xem [GitHub Actions — Dependency
caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching).

CI hiện không có bước cài dependency đáng kể, nên Actions dependency cache có thể ít lợi ích. Lợi ích lớn hơn sẽ đến
từ result cache **sau khi** test được chia thành unit có declared inputs. Không cache toàn bộ verdict của monolith
theo changed paths tự suy đoán.

### 3.6. Required-check topology phải luôn phát verdict

GitHub cảnh báo workflow bị bỏ qua do path filter sẽ để check ở trạng thái Pending và có thể chặn merge; ngược lại,
một **job** conditional bị skip lại báo Success, kể cả khi là required check. Xem [Workflow syntax — path filters](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore)
và [Status checks — skipped jobs](https://docs.github.com/en/pull-requests/reference/status-checks).

Do đó không nên dùng top-level `paths` để bỏ cả required workflow. Required workflow phải luôn chạy một classifier
và một policy aggregator. Aggregator chỉ xanh khi:

- changed paths đã được phân loại;
- mọi mandatory/selected shard đã báo kết quả cho đúng SHA;
- lý do deselect được ghi trong evidence;
- unknown/unmapped path đã kích hoạt full fallback.

Path filter của GitHub còn có giới hạn: với diff trên 3.000 file, match ngoài 3.000 file đầu có thể không kích hoạt
workflow. Đây là lý do thứ hai để selector security-critical tự đọc diff đầy đủ trong workflow luôn chạy, thay vì
dùng path filter làm policy oracle. Xem [Workflow syntax — Git diff comparisons](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#git-diff-comparisons).

Khi branch có push head mới, `concurrency` với `cancel-in-progress: true` có thể hủy CI của head cũ để không đốt
compute; không dùng cách này cho land/release run đang tạo evidence cần bảo tồn. Xem [GitHub Actions — Control
concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).

Nếu sau này dùng merge queue, required workflow phải nghe `merge_group`; GitHub tạo SHA tạm gồm latest base và các
PR đứng trước. Check trên PR head không thay thế check trên merge-group SHA. Xem [GitHub Actions — `merge_group`](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group)
và [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).

## 4. Mô hình checkpoint đề xuất cho tra-luat

| Tầng | Khi chạy | Nội dung | Full 1.696? | Evidence/quy tắc |
|---|---|---|---:|---|
| **T0 — inner loop** | sau edit nhỏ, trước commit | compile/lint/diff check; test mới/sửa; module/group gần nhất | Không | advisory; `last-failed` chỉ debug, không làm authorization |
| **T1 — Executor packet** | trước push/handoff mỗi packet | always-on integrity rẻ; write-set/security/EOL; fragment của packet; affected groups theo closure | Không, trừ fallback | ghi exact SHA, changed paths, policy version/hash, selected/excluded groups, duration và verdict |
| **T2 — ready for rereview** | head packet ổn định | T1 từ clean tree + cross-cutting gates liên quan; reviewer có thể yêu cầu widen | Theo impact/risk | mọi commit mới vô hiệu evidence như protocol hiện tại |
| **T3 — integration/land prepare** | mission integration candidate đã freeze | full selftest; full release/determinism/golden/topology; parity Linux–Windows; artifact-derived checks | **Có** | bắt buộc trên exact candidate/tree; là checkpoint chính thay cho full mỗi packet |
| **T4 — canonical/merge group** | merge-group SHA hoặc post-merge canonical | full suite hoặc tái dùng T3 chỉ khi exact commit/tree và môi trường được chứng minh đồng nhất | Có điều kiện fail-closed | SHA/tree khác, merge commit/rebase khác hoặc base tiến lên ⇒ chạy lại; failure có owner/rollback/stop-the-line |
| **T5 — release candidate/package** | khi tạo artifact phát hành thật | package/manifest/bundle topology, determinism, security/read-only và comprehensive suite cần cho artifact | Có khi artifact/tree đổi | kết quả neo vào exact artifact hash; không tái dùng evidence dev-tree để chứng minh topology package |

Hai tối ưu quan trọng trong bảng:

1. **Full suite chuyển từ mỗi packet sang integration candidate.** N packet độc lập không còn nhân N lần 1.696 ca.
2. **Evidence có thể tái dùng theo exact identity, không theo “cùng nội dung có vẻ giống”.** Nếu integration được
   fast-forward nguyên exact commit đã test, T4 có thể readback và dùng evidence T3. Nếu merge/rebase tạo SHA/tree
   khác, base tiến lên, generated metadata đổi hoặc package được tái sinh, phải chạy gate tương ứng lại.

Schedule/nightly trên default branch phù hợp cho extended variants, repeated runs tìm flake, random non-selected
canary hoặc gate quá đắt; GitHub xác nhận scheduled workflow chạy trên latest default-branch commit. Xem
[Workflow syntax — `on.schedule`](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onschedule).
Nightly không thay thế exact-SHA land evidence vì có khoảng trễ và có thể chạy trên commit khác.

## 5. Thiết kế affected-test selector fail-closed

### 5.1. Catalog tối thiểu

Mỗi test group/case cần metadata machine-readable, ví dụ về khái niệm:

```yaml
id: release_integrity
owned_paths:
  - scripts/tl_core/release.py
  - RELEASE_MANIFEST.json
transitive_triggers:
  - scripts/tl.py
  - scripts/tl_core/test_fragments.py
tier: medium
platforms: [linux, windows]
hermetic: true
shard_safe: false
always_on: false
```

Catalog nên mở rộng chính change-impact policy đã dự kiến, không dựng doctrine thứ hai. Selector nhận base/head SHA,
đọc changed paths/rename/delete, tính effective write closure và trả một plan có hash. Worker evidence ghi cả plan
hash để reviewer/CI tính lại được.

### 5.2. Always-on packet checks

T1 không có nghĩa là “chỉ chạy test mới”. Các guard rẻ, có signal cao nên luôn chạy:

- `git diff --check`;
- compile/lint cho Python bị chạm;
- write-set/lease/generation/security path validation;
- EOL policy phù hợp phạm vi;
- fragment contract, uniqueness, discovery/index checks;
- classifier/selector self-check và nonempty coverage assertion.

Docs-only có thể chạy `doc-claims-check --strict`, link/path, EOL, write-set/security và chứng minh package hash
không đổi; không cần full runtime selftest nếu impact policy không phát runtime consumer. Fragment-only cần chạy
fragment mới + fragment loader/contract + affected subsystem, nhưng điều này chỉ nhanh sau khi có runner fragment
tách khỏi full harness.

### 5.3. Full fallback bắt buộc

Selector phải chuyển sang full khi có một trong các điều kiện sau:

- path mới/chưa map, mapping/schema/selector parse lỗi hoặc selected set rỗng bất ngờ;
- đổi chính test runner, shared fixture, global config/profile, fragment loader hoặc test catalog;
- đổi `scripts/tl.py` ở seam dùng chung rộng mà closure chưa chứng minh được;
- đổi release/package/manifest/golden generator, security policy, EOL policy hoặc CI workflow;
- rename/delete, generated artifact drift hoặc diff base/head không xác định chắc chắn;
- test/group chưa khai hermeticity hay shard safety;
- Reviewer/Land Operator yêu cầu widen/full do risk hoặc evidence thiếu.

### 5.4. Safety net chống mapping drift

Trước khi activation, chạy selector ở **shadow mode** trong một khoảng đo (khuyến nghị khởi đầu 2–4 tuần hoặc đủ
số packet đại diện): T1 vẫn chạy selected suite, T3/T4 vẫn full; đối chiếu failure nào chỉ full suite bắt được.

Theo dõi ít nhất:

- p50/p95 wall time theo tier, OS và group;
- top slow groups/cases và setup time;
- selected/total ratio;
- missed-failure/selector false-negative;
- flake rate và first-failure được giữ lại;
- shard imbalance, CPU utilization và cache hit nếu có;
- số lần full fallback theo lý do.

Mọi lỗi chỉ full suite bắt được phải tạo hành động cụ thể: bổ sung dependency trigger/mapping, sửa hidden dependency,
hoặc đánh dấu group always-on. Có thể chạy ngẫu nhiên một phần non-selected tests ở T1/T2 để phát hiện drift sớm;
random canary là bổ sung, không thay periodic/full checkpoint.

## 6. Kế hoạch triển khai tối thiểu, theo thứ tự rủi ro

### Bước 1 — Instrument trước khi tối ưu

Hiện verdict chỉ có tên/pass-fail; chưa có duration từng ca. Thêm monotonic timing theo case/group và xuất JSON/JUnit
hoặc artifact. Không quyết định shard count hay SLO từ số 1.696. Xác định top 20 điểm nóng, setup bị lặp, I/O và
gate nào thực chất kiểm cùng một invariant.

### Bước 2 — Tạo seam thực thi thật

Chuyển dần từ eager `cases.append((name, expr))`/`_t110(name, fn)` sang registration của callable/metadata, mỗi ca
có setup/teardown và restore state rõ. Ưu tiên:

1. packet fragments — đã có file boundary;
2. các cụm release/workflow/docs — đã có module boundary;
3. legacy blocks còn lại theo capability;
4. một serial group tạm thời cho ca order-dependent chưa thể cô lập.

Giữ invariant chụp/so sánh module state sau mỗi group hoặc process, không chỉ cuối toàn suite.

### Bước 3 — Parallel full suite trước

Chạy group process-isolated trên một OS, cân shard bằng duration lịch sử, sau đó matrix Linux/Windows. Một aggregator
duy nhất nhận đủ shard IDs và fail nếu shard thiếu/skipped/duplicate. Làm bước này trước giúp giảm wall-clock mà chưa
giảm coverage, nên có risk thấp hơn affected selection.

### Bước 4 — Shadow affected selection

Dùng catalog/change-impact closure để tạo T1 plan nhưng vẫn chạy full ở T3/T4. So selected failures với full failures,
sửa mapping drift đến khi có đủ dữ liệu. Không dùng tỷ lệ 80/15/5 của Google như quota cứng; chính nguồn gọi đó là
rough guideline và nói mỗi team cần mix theo kiến trúc địa phương. Xem [Testing Overview — test pyramid](https://abseil.io/resources/swe-book/html/ch11.html#test-scope).

### Bước 5 — Activate tiered gate

Chỉ sau shadow period mới bỏ full khỏi packet bình thường. Branch protection require một `gate-policy` aggregator
luôn chạy; shard job conditional không tự nó là authorization. Full vẫn bắt buộc ở T3 và khi fallback. T4/T5 dùng
exact identity rule ở §4 để tránh chạy lặp vô ích nhưng không tái dùng evidence sai SHA/tree/artifact.

## 7. Những việc không nên làm

1. **Không thêm `--filter` chỉ lọc output cuối harness.** Toàn bộ eager expression đã chạy.
2. **Không chia 1.696 ID theo modulo ngay.** Global monkeypatch/order coupling hiện hữu; shard có thể thay kết quả.
3. **Không mặc định docs-only = bỏ toàn workflow bằng `paths-ignore`.** Required check có thể Pending; classifier
   luôn chạy an toàn hơn.
4. **Không coi job skipped = check đã chứng minh invariant.** GitHub báo skipped job là Success.
5. **Không dùng cache dependency hoặc last-failed như test-result authorization.** Chúng không chứng minh suite
   cần thiết đã chạy trên exact SHA.
6. **Không retry đến xanh rồi xóa dấu first failure.** Retry chỉ phân loại flake; first failure phải còn trong evidence.
7. **Không chuyển wholesale sang Bazel/pytest chỉ để có filter.** Repo có custom harness, topology bundle và protocol
   riêng; trước mắt nên mượn nguyên tắc declared dependency, marker strict, process isolation và aggregator. Có thể
   migrate dần test mới sau khi đo chi phí/lợi ích.
8. **Không bỏ full suite ở checkpoint cuối.** Selective testing giảm latency, không tự chứng minh selector không bỏ
   sót; post-submit/RC là lớp defense-in-depth được các nguồn chính thức giữ lại.

## 8. Phán quyết áp dụng

Khuyến nghị cụ thể cho roadmap là giữ nguyên ý tưởng hai lane F3-06/F3-07 nhưng bổ sung các acceptance criterion sau:

- worker gate không gọi full legacy selftest mặc định;
- fragment runner thật sự chỉ execute selected fragment/affected groups;
- selector/catalog fail-closed, plan có hash và evidence exact-SHA;
- thay selector/catalog/runner/shared state tự động full fallback;
- land prepare chạy full suite, parity và artifact gates trên frozen integration candidate;
- canonical/merge-group/release chỉ tái dùng evidence nếu exact identity contract khớp; nếu không thì chạy lại;
- rollout có timing telemetry, shadow comparison và missed-failure feedback loop.

Đây là phương án cân bằng tốt nhất giữa tốc độ và assurance: Executor nhận feedback nhanh hơn, Reviewer không phải
đợi 1.696 ca cho thay đổi docs/fragment hẹp, trong khi quyền land/release vẫn dựa trên full evidence ở exact
checkpoint có giá trị.

## 9. Danh mục nguồn chính thức

- [Software Engineering at Google — Testing Overview](https://abseil.io/resources/swe-book/html/ch11.html)
- [Software Engineering at Google — Large Tests](https://abseil.io/resources/swe-book/html/ch14.html)
- [Software Engineering at Google — Large-Scale Changes](https://abseil.io/resources/swe-book/html/ch22.html)
- [Software Engineering at Google — Continuous Integration](https://abseil.io/resources/swe-book/html/ch23.html)
- [Google Testing Blog — Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html)
- [Google Testing Blog — Android Platform Testing Made Easy](https://testing.googleblog.com/2019/01/android-platform-testing-made-easy.html)
- [Bazel Test Encyclopedia](https://bazel.build/reference/test-encyclopedia)
- [Bazel Commands and Options](https://bazel.build/docs/user-manual)
- [Bazel Query Guide](https://bazel.build/query/guide)
- [Bazel Remote Caching](https://bazel.build/remote/caching)
- [pytest — Working with custom markers](https://docs.pytest.org/en/stable/example/markers.html)
- [pytest — Registering and validating marks](https://docs.pytest.org/en/stable/how-to/mark.html)
- [pytest — Cache and rerun failures](https://docs.pytest.org/en/stable/how-to/cache.html)
- [pytest-xdist — Distribution](https://pytest-xdist.readthedocs.io/en/stable/distribution.html)
- [pytest-xdist — How it works](https://pytest-xdist.readthedocs.io/en/stable/how-it-works.html)
- [pytest-xdist — Known limitations](https://pytest-xdist.readthedocs.io/en/stable/known-limitations.html)
- [GitHub Actions — Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub Actions — Matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [GitHub Actions — Dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)
- [GitHub Actions — Concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
- [GitHub Actions — Events and `merge_group`](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group)
- [GitHub — Status checks](https://docs.github.com/en/pull-requests/reference/status-checks)
- [GitHub — Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
