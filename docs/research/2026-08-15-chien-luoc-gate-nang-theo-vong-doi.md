# Chiến lược gate nặng theo vòng đời: tránh lặp full selftest mà không hạ assurance

- **Ngày:** 2026-08-15 (Asia/Saigon)
- **Phạm vi:** khảo sát read-only runner, CI, hook và protocol; không chạy full selftest, không sửa production/workflow
- **Head cục bộ được đọc:** nhánh `ops/wp55-verdict-6`
- **Tính chất:** khuyến nghị triển khai; nguồn quy tắc vẫn là protocol/ADR đã accepted

## Kết luận điều hành

Không nên để Executor, Reviewer và CI đều chạy lại `scripts/tl.py --selftest` trên cùng một SHA. Cách tối ưu có thể
áp dụng ngay mà không hạ assurance là:

1. **Một full gate canonical cho mỗi exact SHA/identity**, ưu tiên CI; các phiên sau readback và tái dùng evidence,
   không chạy lại local chỉ để lấy cùng một tín hiệu.
2. **Executor/Reviewer chạy test đích trước**: suite của component đổi, regression fixture và probe đối chứng; đây mới
   là nơi cho feedback nhanh và cũng là nơi full generic suite có thể không phủ.
3. **Một host chỉ chạy một gate nặng tại một thời điểm**. Phân tích/read-only review có thể song song; không chạy
   đồng thời selftest, golden, determinism, bundle và một repair lab trên cùng máy Windows.
4. **Full vẫn bắt buộc tại checkpoint có giá trị**: exact PR/integration candidate, canonical khi identity đổi, và
   exact release artifact. Đây là giảm chạy lặp, không phải bỏ full oracle.

Affected-test selector chưa thể activate hôm nay. ADR-0035 yêu cầu instrument → callable/group isolation → parallel
full → shadow 2–4 tuần → activate; hai tệp policy/schema mà ADR-0032 quy định hiện chưa tồn tại trong `HEAD`.

## 1. Repo đã quyết định đúng hướng, nhưng implementation chưa theo kịp

Protocol đã định nghĩa T0–T5 và nói rõ không chạy toàn bộ legacy selftest sau mọi thao tác nhỏ
([`docs/PROTOCOL_DA_PHIEN.md:468-480`](../PROTOCOL_DA_PHIEN.md#L468)). Nó cũng quy định unknown path, runner,
shared state, security/workflow, release/EOL/policy change phải fallback full; evidence chỉ được tái dùng khi exact
identity khớp ([`:482-491`](../PROTOCOL_DA_PHIEN.md#L482)). ADR-0035 accepted cùng thứ tự rollout và giữ T3/T5 là
full checkpoint ([`docs/adr/0035-dieu-phoi-ben-vung-va-selftest-phan-tang.md:46-57`](../adr/0035-dieu-phoi-ben-vung-va-selftest-phan-tang.md#L46)).

Khoảng cách hiện tại:

- CI PR vẫn gọi trực tiếp `python scripts/tl.py --selftest`
  ([`.github/workflows/ci.yml:120-129`](../../.github/workflows/ci.yml#L120)).
- Full pre-push chỉ được kích hoạt khi ref đích là `refs/heads/master`; push nhánh thường không chạy full hook này
  ([`.githooks/pre-push:340-358`](../../.githooks/pre-push#L340)).
- `.github/coordination/change-impact.v1.json` và schema tương ứng không có trong `HEAD`, dù ADR-0032 chỉ định đó là
  policy canonical ([`docs/adr/0032-change-impact-rule-co-huong.md:18-24`](../adr/0032-change-impact-rule-co-huong.md#L18)).
- CI đã giảm chi phí theo cách an toàn: hủy run cũ của cùng PR và mặc định PR thường chỉ chạy Linux; Windows chạy ở
  master, manual dispatch hoặc PR có nhãn `windows` ([`.github/workflows/ci.yml:21-48`](../../.github/workflows/ci.yml#L21)).
  Tuy vậy, đây mới là giảm duplication theo run/platform, chưa phải affected-test selection.

## 2. Vì sao chưa thể thêm `--filter` vào full harness

`tl_selftest.py` là một chương trình eager, không phải registry của test callable độc lập:

- `run()` tạo `cases=[]`, rồi các biểu thức trong `cases.append(...)` được tính ngay; file còn chụp global module state
  để phát hiện monkeypatch rò sang test sau ([`scripts/tl_selftest.py:47-56`](../../scripts/tl_selftest.py#L47)).
- Helper `_t110` cũng gọi `fn()` ngay khi đăng ký ([`:9100-9106`](../../scripts/tl_selftest.py#L9100)).
- Chỉ sau khi mọi khối đã chạy, harness mới tally và in `N/N` ([`:29742-29761`](../../scripts/tl_selftest.py#L29742)).

Do đó lọc danh sách `cases` ở cuối chỉ lọc **output**, không giảm công việc. Chia ID theo modulo/process trước khi
dọn global-state coupling có thể làm đổi thứ tự và tạo xanh/đỏ giả. Protocol đã cấm coi hai cách này là isolation
hợp lệ ([`docs/PROTOCOL_DA_PHIEN.md:488-491`](../PROTOCOL_DA_PHIEN.md#L488)).

Repo đã có seam tốt hơn cho test mới: fragment packet-owned theo ADR-0031. Loader có `candidate_paths` để chọn source
ở tầng nội bộ ([`scripts/tl_core/test_fragments.py:331-349`](../../scripts/tl_core/test_fragments.py#L331)), nhưng
runtime adapter hiện gọi `load_runtime_fragment_cases()` không truyền tập chọn và chạy mọi fragment trong full
harness ([`scripts/tl_selftest.py:29318-29330`](../../scripts/tl_selftest.py#L29318)). Nói cách khác, file boundary đã
có nhưng public targeted runner/evidence chưa hoàn tất.

## 3. Case study PR #120: full xanh không thay targeted review

GitHub Actions `gate` run [`31875177993`](https://github.com/ducthangho/tra-luat/actions/runs/31875177993), gắn với
PR head `427021049bc8677f5915da13b8ac38a53c949b93`, xanh. Job Ubuntu chạy từ 08:43:20 đến 08:47:00 UTC; riêng
bước selftest của `scripts/tl.py` chạy khoảng 109 giây (08:43:58–08:45:47). Tuy nhiên workflow tại thời điểm đó chưa truyền `ref:` cho
`actions/checkout` trên event PR, nên association với head chưa đủ chứng minh checkout/tested tree là exact head;
run này dùng tốt cho số đo chi phí nhưng **không** được tái dùng làm exact-head evidence theo policy mới.

Cross-review lượt 9 vẫn tìm được 3 P1 bằng doctrine fixtures và 1 P2 bằng suite
`.claude/dev/packet_loop_test.py`; verdict neo cùng exact SHA tại
[PR review #4943588803](https://github.com/ducthangho/tra-luat/pull/120#pullrequestreview-4943588803). Local full selftest
của Reviewer bị hủy ở ngưỡng 5 phút mà không in N/N, trong khi các probe đích cho kết quả sớm. Sau đó đối chiếu Linux
xác nhận bảy fixture doctrine tái lập; mutant stdout còn khác kết quả Windows/Python 3.13 với Linux/Python 3.11
([PR comment #5301744013](https://github.com/ducthangho/tra-luat/pull/120#issuecomment-5301744013)).

Bài học không phải “full suite vô ích”. Bài học là:

- không cần Reviewer chạy lại full evidence khi CI tương lai đã ghi và validate exact SHA/tree/identity;
- full generic suite không thay thế suite component mới chưa được nối CI;
- platform trigger phải dựa vào impact: thay codepage/stdout/path/fence parser cần targeted Windows evidence, dù PR
  thường chỉ có Linux full;
- chạy nhiều process nặng đồng thời trên cùng host có thể làm elapsed time xấu hơn chạy tuần tự.

## 4. Policy áp dụng ngay, trước khi selector chính thức tồn tại

### 4.1. Phân vai evidence

| Checkpoint | Chạy tại phiên làm việc | Full generic selftest | Điều kiện |
|---|---|---:|---|
| T0 — sau edit | compile changed Python; test mới/sửa; fixture đối chứng | Không | advisory, fail-fast |
| T1 — trước push/handoff | always-on cheap guards + suite component + packet fragment | Không chạy local mặc định | PR CI sẽ tạo full evidence cho exact SHA |
| T2 — Reviewer | readback full CI exact SHA; chạy adversarial/targeted và coverage gap | Chỉ khi CI thiếu/sai identity hoặc Reviewer yêu cầu | không lặp cùng OS/runtime vô ích |
| T3 — integration/land | full gate canonical trên frozen candidate, parity cần thiết | Có | exact SHA/tree + policy/runner/runtime |
| T4 — canonical | reuse T3 duy nhất khi identity khớp; nếu merge/rebase/base đổi thì chạy lại | Có điều kiện | fail-closed |
| T5 — release | package/topology/smoke/full trên exact artifact | Có | neo artifact SHA-256 |

Trong giai đoạn chưa activate selector, yêu cầu “T1/T2 full theo policy hiện hành” vẫn được đáp ứng bằng **một run CI
canonical trên exact SHA**, không phải bằng N bản local giống nhau. Không tái dùng khi SHA/tree, OS/runtime,
runner/test catalog/policy hoặc artifact identity khác.

### 4.2. Thứ tự gate để fail sớm

1. identity/readback, lease/write-set, `git diff --check`, compile changed Python;
2. test mới/sửa và minimal paired controls (cùng fixture, khác đúng một biến);
3. suite component bị chạm, ví dụ `packet_loop_test.py`;
4. gate theo artifact bị chạm: docs, EOL, golden, release, bundle;
5. full generic suite đúng một lần ở CI/checkpoint yêu cầu.

Một lỗi ở bước 1–3 dừng vòng edit hiện tại; chưa cần đốt full 1.696 ca để xác nhận một candidate đã chắc chắn đỏ.
Ở T3/T5 có thể tiếp tục các shard sau lỗi để thu chẩn đoán đầy đủ; ở T0–T2 ưu tiên fail-fast.

### 4.3. Quy tắc tài nguyên trên host

- Mỗi physical host có semaphore `heavy_gate=1`; selftest, golden, determinism, bundle và mutation suite lớn cùng
  hàng đợi, không cùng chạy.
- Các probe nhỏ độc lập và hai nhánh review Standards/Spec có thể song song.
- Mỗi gate có timeout riêng và ghi `pass | fail | timeout | infra_error`; timeout không được đổi thành pass và không
  nên retry vô hạn. Nếu CI exact-SHA đã có evidence hợp lệ, dùng evidence đó; nếu chưa có thì trạng thái là thiếu gate.
- CI dùng `concurrency.cancel-in-progress` cho head PR cũ như hiện tại; không hủy land/release evidence đang chạy.

### 4.4. Cache và tái dùng

Ưu tiên **evidence cache theo exact identity**, không cache phán quyết monolith theo phỏng đoán changed-path. Một bản
ghi tối thiểu cần: tested SHA/tree, base SHA, OS, Python, runner hash, catalog/policy hash, command, selected tests,
start/end/duration, rc, first failure và artifact hash. Dependency cache chỉ giảm setup; nó không chứng minh test đã
chạy. `last-failed` chỉ dùng vòng debug, không dùng làm promotion evidence.

## 5. Selector fail-closed sau khi có nền kỹ thuật

Mapping phải là `changed path → capability/module → reverse/transitive dependants → groups/tests`, không phải basename
hay grep tên test. Catalog mỗi group cần ít nhất: `id`, owned/trigger paths, transitive triggers, tier, platforms,
hermeticity, shard safety, always-on và duration estimate.

Full fallback bắt buộc khi:

- path mới/unmapped, rename/delete hoặc diff base/head không xác định;
- đổi selector/catalog/runner, shared fixture/global state hoặc fragment loader;
- đổi security/workflow, EOL, release/package/manifest/generator/golden;
- selected set rỗng bất ngờ, mapping parse lỗi, group chưa khai hermetic/shard-safe;
- Reviewer/Land Operator yêu cầu widen.

Aggregator luôn phải phát verdict. Không dùng top-level `paths-ignore` hoặc job `skipped` như evidence dương.

## 6. Sharding và parallelism

Không shard monolith hiện tại. Trước hết chuyển test thành callable/group có setup/teardown và kiểm restore state sau
mỗi group; các ca còn order-dependent ở một serial group. Sau đó chạy group trong process cô lập, cân shard theo
duration lịch sử thay vì số case. Aggregator fail nếu thiếu/trùng/skipped shard.

Mức song song nên tách theo nơi chạy:

- **Một máy developer/reviewer:** `heavy_gate=1`, vì contention CPU/I/O/process startup đã làm timeout dài hơn.
- **CI full checkpoint:** shard process-isolated có `max-parallel` giới hạn; matrix OS ở ngoài shard.
- **T0–T2:** fail-fast để rút latency.
- **T3–T5:** ưu tiên thu đủ failure matrix; giữ first failure, không retry tới xanh rồi xóa dấu.

## 7. Lộ trình nhỏ, có thể kiểm chứng

1. **Runbook-only, áp dụng ngay:** Reviewer prompt phải readback CI exact-SHA và cấm duplicate local full khi identity
   khớp; thêm quy tắc một heavy gate/host và targeted-before-full. Không đổi production.
2. **Instrument:** xuất JSON/JUnit duration theo gate; với legacy harness tạm đo theo block/group thô. Thu p50/p95,
   top slow, startup/I/O, flake, timeout và platform delta.
3. **Public targeted runner:** cho fragment/component suite chạy theo ID/group trước full harness; selector unknown ID
   phải đỏ, không trả tập rỗng. Nối `packet_loop_test.py` hoặc catalog tương đương vào required affected gate.
4. **Callable/group isolation:** chuyển dần eager registration; ưu tiên fragment, release/workflow/docs rồi legacy;
   giữ serial quarantine cho stateful cases.
5. **Parallel full không giảm coverage:** process-isolated shards + aggregator + duration balancing; kiểm parity.
6. **Shadow selector 2–4 tuần:** luôn sinh selected plan nhưng vẫn chạy full T3/T4; đo failure chỉ-full, mapping drift,
   selected/total ratio và fallback reasons.
7. **Activate có rollback:** T1/T2 dùng affected selection; unknown/failure tự fallback full. T3/T5 vẫn full.

Acceptance criterion để rời shadow: không có missed failure chưa giải thích; mọi failure chỉ-full đã tạo mapping/rule
hoặc always-on group; catalog/policy/runner có hash; exact-SHA aggregator luôn báo đủ mandatory groups; có kill switch
quay về full.

## 8. Phán quyết

Phương án tối ưu cho repo này không phải “chạy 1.696 test nhanh hơn bằng filter”, mà là **đặt full oracle đúng
checkpoint, tái dùng evidence exact-SHA và làm targeted signal mạnh hơn**. Có thể áp dụng ngay phần điều phối để tránh
Executor/Reviewer/CI chạy lặp. Selector và sharding chỉ nên được bật sau khi monolith eager được tách và shadow chứng
minh không bỏ sót.

Nguồn nền chi tiết và tài liệu chính thức đã được tổng hợp trước tại
[`docs/research/2026-08-08-toi-uu-selftest-gate.md`](2026-08-08-toi-uu-selftest-gate.md); báo cáo này cập nhật trạng
thái triển khai hiện tại và bằng chứng PR #120.
