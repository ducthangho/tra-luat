# WP1315 r5/g5 — readmission SOURCE sau WP1325

Trạng thái: PROPOSED; chưa cấp lease, chưa gọi model, chưa tạo ứng viên nguồn.

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

Mọi thay đổi record-lease/postimage phải giữ đúng guard cũ về TargetProof, API comment bytes/hash, identity, current I2, expiry, topology, canonical_path, seed/witness/high_water, tombstone, admission và approval. Counter/limit/call-ID/consumed flags/history giữ nguyên. Không tự gọi delegated_audited thay cho actual-human audit đối với phần chạm cơ chế thẩm quyền này.

## Quy trình hữu hạn

Pha A tối đa120 phút từ một activation bền sau readiness. Dự trù20 spec review +15 metadata/ownership/publisher +25 Claude author +20 focused verification +25 independent Codex source review +15 artifacts/stop=120. Một fresh Claude spec review, một fresh Claude author, một fresh independent Codex source review; không retry hoặc context mới. Reviewer riêng, read-only/snapshot và actual launcher/stdout/receipt neo exact H/tree, K4 thật. Không dùng context executor làm reviewer. Review spec phải approve chính bytes được cấp; thay đổi material sau review phải quay checkpoint.

Author handoff đóng băng exact H/tree/diff và kết quả thật. Chạy11 nhóm WP1315,13 healthy controls và4 targeted mutants cùng healthy controls trong quỹ focused20 phút; không coi phép đo hẹp là full M9/native. AST/diff/Ruff delta với C và immutable baseline được ghi thật. Mọi failed/timeout/skipped/not_run giữ riêng. Một lỗi ngoài phạm vi hoặc hết quỹ thì dừng phần phụ thuộc, không sửa lan.

Đóng/rút hạn lease author sau pha A. Không giữ lease đang viết hoặc chạy đồng hồ kiểm chứng trong lúc chờ owner đọc source. Chuẩn bị gói audit exact H cho owner; không AI ký thay. Owner source audit thật và quyết định exact H là gate bắt buộc trước pha B. Không chuyển audit H669 hoặc SOURCE approval thành target approval.

Pha B được đề nghị tối đa900 phút, chỉ kích hoạt sau actual-human exact-H audit, publication/land authority hợp lệ và toàn bộ readiness/whole-fit. Một activation bền đóng băng absolute deadline start+900; không thay thời gian r40/r55. Phân bổ30 local gates +20 metadata +450 khối native/CI/connector +20 reconciliation +330 masterCI +30 artifacts/closure +20 reserve=900. Trong khối450: Windows baseline/candidate150+150 và Linux150, tuần tự nếu cùng host; PR Ubuntu CI và fullM9 chạy trên runner riêng, không quá khối450. Queue/setup/cleanup tính trong quỹ. Không giảm configured timeouts để tạo fit; không đủ actual remaining fit thì dừng trước batch.

Đúng một source push chính, một draftPR mới, một genuine connector trên H, một automatic PR Ubuntu ci.yml, một full M9 đủ8 shards trên H, và một automatic master ci.yml sau conditional merge. Attempts đều1, reruns0. Đọc các endpoint connector trước để không bắn trùng. Các phép đo workflow-definition chỉ đọc phải gắn đúng real run ID/artifact, ghi riêng, không là lượt test. Không trigger Windows CI theo chỉ thị miễn Windows CI của owner; nếu workflow phụ Windows tự xuất hiện, giữ trạng thái thực tế và xử lý theo waiver bền, không ghi cancelled thành passed. Waiver self-test cục bộ r55 chỉ áp dụng r55; pha B này vẫn đòi local self-test N/N.

Native Windows một paired parent trên baseline/H, đúng cùng host/command/runtime Python>=3.13 và ACL capability đo thật: python -u .claude/dev/packet_loop_test.py, trần150 phút/checkout,300/cặp. Linux native H một full main harness, trần150 phút. Đóng băng catalog case IDs từ source và bắt đủ positive cases; không mandatory skipped/not_run, không dùng scratch/CI thay native. Kết quả baseline thất bại chỉ là baseline, không tự miễn case đỏ trong write set; candidate phải đạt mọi required case. Probe công cụ/runtime/FS/ACL/host lock thực tế trước heavy gate. Chỉ tiếp nhận source-only summaries/hash, raw private host logs giữ tại host.

M9 full mode bắt buộc và không được thu hẹp. PR/master four-dimension provenance phải gắn đúng H hoặc M; không tái nhãn output của PR cho master, không sửa producer not_measured thành passed. Positive output/supplement phải có nguồn và mapping thật. CI đỏ hoặc required proof chưa đo thì không merge/land.

## Authority, chi và điểm kết thúc

Pha A dùng revision5/generation5 và nhánh mới, metadata namespace riêng; pha B generation6 validation-only nếu H không đổi. Không hồi sinh generation4 đã đóng. Metadata spec/prompt/lease/registration/publisher chỉ trong namespace được cấp; quét toàn kho và bia mộ đầy đủ, không lọc bỏ nhánh người khác. Chỉ cấp lease khi ownership/I2/current authority thật đủ.

Allowance tăng thêm: spec reviewer1 + author1 + source reviewer1 + connector1; tính thành1author và3review workloads (spec/source/connector), giữ mọi lịch sử WP1315/WP1325 và UNKNOWN billing. Không coi chúng là quota chưa dùng của r40/r55, không refund/reset clock hoặc attempt. Chưa có nghĩa vụ hoàn tất khi gặp E1–E5 hoặc proof/cap stop.

Sau audit thật và mọi K0–K7/native/CI/connector đạt mới conditional merge đúng H; verify parents/tree/CI master, đăng M8 và exact-readback, nhả lease, đóng WP1315. PR1318 cũ chỉ xử lý sau successor thực sự land, không xóa branch/ref. Không sửa ruleset.

Public scope đề nghị: repo ducthangho/tra-luat, Issues1172/1315 và successorPR; ba source paths cùng source-only metadata/receipts/hash và ordinary provenance workflows. Loại trừ raw model thinking/transcript, secrets, private host logs và real target state/seed/journal/witness/boot bindings.

Không installation, enrollment/grant/G5, LIVE, target mutation hoặc đóng Mission1172. Sau WP1315 thực sự land mới chuẩn bị target readmission từ facts và authority còn hiệu lực; mọi target history/counters/seed/witness phải được giữ qua canonical operations.
