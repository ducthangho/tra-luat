# wp1315 r5 — readmission SOURCE sau WP1325

Trạng thái: bản sửa thứ nhất sau Codex spec review (lượt `aa543638`, changes_requested F1–F4). Bản gốc sha256 b39c1baeed9e3da8bd688549ee43a7db969955ef88ef4eb7a6823d99c4c666da giữ làm lịch sử, không bị đổi nhãn.

## Đích và đầu vào bất biến

Khôi phục phần sửa adopted approved_pending của WP1315 trên canonical hiện hành, giữ đúng hợp đồng r39 và option A: chỉ record-lease từ một adopted projection hợp lệ với predecessor closed/scoped approval và mọi reservation đã consumed mới về leased. Không dispatch, không thêm attempt, không nâng quota hay nới quyền. Rà và giữ các ca reader state_path, predecessor closure và unused reservations đã được review ở H cũ.

Immutable acceptance baseline: c0b8e11d7099f756e65db8bd9a81493cde789a6f. Input đã được owner audit: H669=669af5f9f58dfd72324d1f5b6aaefd15745592b1, tree b69be04a3fa17be04771c2bc84717b2486b9b494. Audit cũ chỉ là lịch sử trên H669, không phải audit ứng viên mới.

Canonical snapshot C=9c1661f76d5f4ef811aa349df102989cc2e2d53d. Dependency WP1325 đã landed tại M=902b2501c02a5fec5e1e9afa4c16b2bc8ebe5106; M8 https://github.com/ducthangho/tra-luat/issues/1325#issuecomment-6914167207. Dry merge Git riêng rc0 không chứng minh ngữ nghĩa đúng, không phải ứng viên để nghiệm thu.

## Phạm vi ghi SOURCE

Chỉ ba đường dẫn:
- .claude/dev/packet_loop.py
- .claude/dev/packet_loop_test.py
- ops/specs/wp1315-adopted-pending-recovery-r1.md

Author tích hợp lại logic H669 lên C, tự dẫn xuất từ hợp đồng và bằng chứng; không áp patch mù. Giữ mọi thay đổi canonical không liên quan, đặc biệt các bản vá A9/CLR null/workflow/bundle/manifest vừa land. Không được đổi VERSION, manifest, workflow, release, danh sách người có quyền hay gate K0–K7; không thêm CLI escape hoặc đổi quyền lease/merge. Nếu cần đường dẫn thứ tư thì dừng, không mở rộng write set.

Mọi thay đổi record-lease/postimage phải giữ đúng guard cũ về TargetProof, API comment bytes/hash, identity, current I2, expiry, topology, canonical_path, seed/witness/high_water, tombstone, admission và approval. Counter/limit/call-ID/consumed flags/history giữ nguyên. Audit exact H cho phần chạm cơ chế thẩm quyền này đi theo mục "Trình tự audit trước công bố": nhãn `owner_delegated_audit`, không bao giờ ghi thành `human_audited`.

## Quy trình hữu hạn

Pha A tối đa120 phút từ một activation bền sau readiness. Dự trù20 spec review +15 metadata/ownership/publisher +25 Claude author +20 focused verification +25 independent Codex source review +15 artifacts/stop=120. Phân vai theo chỉ thị chủ kho https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916538696: spec review do OpenAI Codex (gpt-6-astra) làm, author là Claude (claude-fable-5-2), source review do một context Codex mới, độc lập. Lượt spec review đầu (`aa543638`) đã tiêu và được tính; duyệt lại bản sửa này là đúng một lượt Codex spec review bổ sung, nâng trần bằng uỷ quyền và ghi công khai. Không retry, không context nào khác. Reviewer riêng, read-only/snapshot và actual launcher/stdout/receipt neo exact H/tree, K4 thật. Không dùng context executor làm reviewer. Review spec phải approve chính bytes được cấp; thay đổi material sau review phải quay checkpoint.

Author handoff đóng băng exact H/tree/diff và kết quả thật. Chạy11 nhóm WP1315,13 healthy controls và4 targeted mutants cùng healthy controls trong quỹ focused20 phút; không coi phép đo hẹp là full M9/native. AST/diff/Ruff delta với C và immutable baseline được ghi thật. Mọi failed/timeout/skipped/not_run giữ riêng. Một lỗi ngoài phạm vi hoặc hết quỹ thì dừng phần phụ thuộc, không sửa lan.

Đóng/rút hạn lease author sau pha A. Không giữ lease đang viết hoặc chạy đồng hồ kiểm chứng trong lúc chờ audit. Chuẩn bị gói audit exact H; audit do phiên điều phối thực hiện theo uỷ quyền và ghi nhãn `owner_delegated_audit`, không ký hay khai là human. Audit exact H (theo trình tự ở mục "Trình tự audit trước công bố") là gate bắt buộc trước pha B. Không chuyển audit H669 hoặc SOURCE approval thành target approval.

Pha B được đề nghị tối đa900 phút, chỉ kích hoạt sau audit exact H theo mục "Trình tự audit trước công bố", publication/land authority hợp lệ và toàn bộ readiness/whole-fit. Một activation bền đóng băng absolute deadline start+900; không thay thời gian r40/r55. Phân bổ30 local gates +20 metadata +450 khối native/CI/connector +20 reconciliation +330 masterCI +30 artifacts/closure +20 reserve=900. Trong khối450: Windows tập trung tối đa60 phút trên `tra-luat-win` hoặc `DESKTOP-T9R33P2` và Linux tối đa150 phút; PR Ubuntu CI và fullM9 chạy trên runner riêng, không quá khối450. Queue/setup/cleanup tính trong quỹ. Không giảm configured timeouts để tạo fit; không đủ actual remaining fit thì dừng trước batch.

Đúng một source push chính, một draftPR mới, một genuine connector trên H, một automatic PR Ubuntu ci.yml, một full M9 đủ8 shards trên H, và một automatic master ci.yml sau conditional merge. Attempts đều1, reruns0. Đọc các endpoint connector trước để không bắn trùng. Các phép đo workflow-definition chỉ đọc phải gắn đúng real run ID/artifact, ghi riêng, không là lượt test. Không trigger Windows CI theo chỉ thị miễn Windows CI của owner; nếu workflow phụ Windows tự xuất hiện, giữ trạng thái thực tế và xử lý theo waiver bền, không ghi cancelled thành passed. Waiver self-test cục bộ r55 chỉ áp dụng r55; pha B này vẫn đòi local self-test N/N trước push. CI master sau merge được bớt test dài (selftest đầy đủ, packet-loop CI) theo chỉ thị https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916597687; phần bớt ghi `waived_by_owner`/`not_run`.

Native Windows theo chỉ thị https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916597687: chỉ chạy tập bắt buộc Windows đúng 24 ID (11 nhóm, 13 controls) của danh mục đóng băng ở trên, trên H, mutant chỉ chạy Linux; trên `tra-luat-win` hoặc `DESKTOP-T9R33P2`, runtime Python>=3.13 đo thật, trần60 phút; không chạy paired baseline/H đầy đủ. Linux native H một full main harness, trần150 phút. Danh mục ID là danh mục đóng băng ở trên; không ca bắt buộc nào được skipped/not_run, không dùng scratch/CI thay native. Kết quả baseline thất bại chỉ là baseline, không tự miễn case đỏ trong write set; candidate phải đạt mọi required case. Probe công cụ/runtime/FS/ACL/host lock thực tế trước heavy gate. Chỉ tiếp nhận source-only summaries/hash, raw private host logs giữ tại host.

M9 full mode bắt buộc và không được thu hẹp. PR/master four-dimension provenance phải gắn đúng H hoặc M; không tái nhãn output của PR cho master, không sửa producer not_measured thành passed. Positive output/supplement phải có nguồn và mapping thật. CI đỏ hoặc required proof chưa đo thì không merge/land.

## Danh mục kiểm chứng tập trung đóng băng

Danh mục dưới đây đóng băng TRƯỚC khi author bắt đầu. Author và reviewer không được đổi, thêm hay bớt ID. Mọi ID trong danh mục đều là ca bắt buộc.

Mười một nhóm WP1315 (ID phải có đúng một lần trong `CASES` của H):
`wp1315_adopted_pending_valid`, `wp1315_adopted_pending_historical`, `wp1315_adopted_pending_rejections`, `wp1315_pending_intermediate_no_dispatch`, `wp1315_pending_postimage_exact`, `wp1315_pending_exhausted_budget`, `wp1315_ordinary_record_lease_whitelist`, `wp1315_pending_target_proof`, `wp1315_pending_unflagged_readers`, `wp1315_pending_predecessor_closure`, `wp1315_pending_unused_reservation`.

Mười ba healthy controls (đều đã có trong `CASES` ở C):
`wp1174_lifecycle_scoped_lifecycle`, `wp1174_lifecycle_identity_advisory`, `wp1174_lifecycle_legacy_unchanged`, `wp1174_lifecycle_guard_readonly`, `wp1174_adopt_postimage_all`, `wp1174_adopt_finalize_replay`, `wp1303_target_context`, `wp1303_target_supported_pairs`, `cong_c_k3_p1`, `cong_c_k3_p2_commit_doi`, `cong_c_k3_p2_original_head`, `cong_c_k3_original_tien_to`, `k3s_comment_that_sach`.

Bốn targeted mutant (khoá trong `MUTANTS`, mỗi cái có ca đích riêng):
- `m1315_reader_state_path` → `wp1315_pending_unflagged_readers`.
- `m1315_predecessor_attempt_open` → `wp1315_pending_predecessor_closure`.
- `m1315_predecessor_latest_verdict` → `wp1315_pending_predecessor_closure`.
- `m1315_unused_predecessor_call` → `wp1315_pending_unused_reservation`.

Oracle:
- Tập ID thực chạy phải BẰNG đúng tập ID yêu cầu (so tập, không so số đếm). `chay_suite` bỏ qua im lặng ID không có trong `CASES`, nên phải kiểm sự có mặt trước khi chạy.
- Mỗi nhóm WP1315 và mỗi control phải passed.
- Mỗi mutant phải làm ca đích của nó đỏ vì assertion của chính ca ấy, không phải vì lỗi import hay dựng fixture. Healthy control trên CÙNG sản phẩm đã đột biến (cùng hash) phải passed. Với `m1315_reader_state_path`, mutant chỉ cắt đường đọc chẩn đoán `_reader_state`, nên control là `wp1315_adopted_pending_valid` và `wp1315_adopted_pending_historical` (luồng recovery không qua `_reader_state`). Ca đích `wp1315_pending_unflagged_readers` chạy nguyên vẹn, không thu hẹp, và phải đỏ ở assertion của nhánh inactive-policy. Với ba mutant chốt phục hồi, control là `wp1315_adopted_pending_valid`. Một control đỏ dưới mutant thì chặn bước phụ thuộc, không được bỏ qua.
- `failed`, `timeout`, `skipped`, `not_run` hay `UNKNOWN` ở bất kỳ ca bắt buộc nào đều chặn bước phụ thuộc.
- Tập bắt buộc trên Linux: toàn bộ 11 nhóm, 13 controls và 4 mutant kèm control. Tập bắt buộc trên Windows (theo https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916597687) là đúng 24 ID: 11 nhóm cộng 13 controls, chạy trên H. Loại trừ duy nhất được phép trên Windows là 4 lượt mutant; chúng chỉ chạy trên Linux. Ngoài loại trừ ấy, tập ID Windows thực chạy phải bằng đúng 24 ID, và mọi kết quả `failed`, `skipped`, `not_run`, `timeout` hay `UNKNOWN` đều chặn bước phụ thuộc. Thiếu một ID bắt buộc thì bị từ chối như một lỗi, không ghi thành `not_run` để đi tiếp. K6 không bị nới.
- Ruff F: delta so với C phải bằng 0, tức multiset thông báo F của hai tệp Python tại H giống hệt tại C.

## Lịch sử và bất biến dữ liệu

"Giữ lịch sử" nghĩa là mọi mục lịch sử, counters và witness đã có được giữ nguyên byte. Chỉ được NỐI THÊM đúng một sự kiện recovery có ràng buộc, kèm việc tăng revision của state/witness và `high_water` mà sự kiện ấy đòi, đúng như hành vi đã review ở H669. Không sửa hay xoá mục cũ.

## Trình tự audit trước công bố và bộ ràng buộc cuối

Audit trước pha B là `owner_delegated_audit` do phiên điều phối Claude Code thực hiện theo uỷ quyền https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916538696. Bản ghi đăng trên Issue #1315 TRƯỚC khi push H, và ràng buộc đúng bộ: `packet_id` `wp1315`, revision 5, generation 5 (author), H, tree, `spec_sha256` của spec này, cùng sha của review Codex nguồn. Bản ghi không dùng schema `human_exact_head_audit.v1`, không mang `assurance: human_audited` và không được nộp vào nhánh human của K4.

K4 của `kiem-merge` đi đường review model: dùng run.json và stdout của lượt Codex source review trên đúng H, với dòng cuối `KET_LUAN: approve`. Lease mà K4 đọc là lease validation generation 6 trên nhánh `ops/wp1315-r5-g6-validation`. Lease ấy ghi `start_from_sha` và `reviewed_sha_required` bằng đúng H, kèm liên kết tới bản ghi audit uỷ quyền của generation 5. Audit generation 5 không bị đổi nhãn thành audit generation 6; lease g6 chỉ trỏ tới nó. Nếu một cổng máy đòi đúng nhãn human mà không nhận nhãn uỷ quyền, phiên dừng ở cổng đó và báo lại, không sửa cổng.

## Authority, chi và điểm kết thúc

Pha A dùng revision5/generation5 và nhánh mới, metadata namespace riêng; pha B generation6 validation-only nếu H không đổi. Không hồi sinh generation4 đã đóng. Metadata spec/prompt/lease/registration/publisher chỉ trong namespace được cấp; quét toàn kho và bia mộ đầy đủ, không lọc bỏ nhánh người khác. Chỉ cấp lease khi ownership/I2/current authority thật đủ.

Allowance tăng thêm: spec reviewer1 + author1 + source reviewer1 + connector1; tính thành1author và3review workloads (spec/source/connector), giữ mọi lịch sử WP1315/WP1325 và UNKNOWN billing. Không coi chúng là quota chưa dùng của r40/r55, không refund/reset clock hoặc attempt. Chưa có nghĩa vụ hoàn tất khi gặp E1–E5 hoặc proof/cap stop.

Sau audit thật và mọi K0–K7/native/CI/connector đạt mới conditional merge đúng H; verify parents/tree/CI master, đăng M8 và exact-readback, nhả lease, đóng WP1315. PR1318 cũ chỉ xử lý sau successor thực sự land, không xóa branch/ref. Không sửa ruleset.

Public scope đề nghị: repo ducthangho/tra-luat, Issues1172/1315 và successorPR; ba source paths cùng source-only metadata/receipts/hash và ordinary provenance workflows. Loại trừ raw model thinking/transcript, secrets, private host logs và real target state/seed/journal/witness/boot bindings.

Không installation, enrollment/grant/G5, LIVE, target mutation hoặc đóng Mission1172. Sau WP1315 thực sự land mới chuẩn bị target readmission từ facts và authority còn hiệu lực; mọi target history/counters/seed/witness phải được giữ qua canonical operations.
