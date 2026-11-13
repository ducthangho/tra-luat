# wp1308 r2 — Target readmission và canary sau WP1309
packet_id: wp1308
revision: 2
generation: 2
mission_issue: 1172
mission_revision: 32
mission_plan_sha256: 98c506e169e61fb41dfea63e7bd83e088271b462bc786df9a9a9c4c653a7e188
contract_id: WP1308-r2-readmission-after1309
immutable_acceptance_baseline: dc635d3c90ecc348bc916bfd3e9b0a8f8ad9000d
admission_ref: refs/heads/ops/wp1308-target-r2-g2@910098b6062ac30e0eacd9b17683862fd36e29ee
admission_path: ops/admissions/wp1308-r2-g2.json
admission_sha256: 429b2fc41c6e76a9acdf2f2ffdb38e603e736b3cc6dc0437936ce748ef2ea315
executor: codex
environment: local
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: human_audited

## Authority và phạm vi
MCR r32 được chủ kho duyệt tại https://github.com/ducthangho/tra-luat/issues/1308#issuecomment-6847732450.
Actual installed plan: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6848535449; source WP1309/PR1311 phải landed và closed trước installation.
Consumer product pinned dc635d3c90ecc348bc916bfd3e9b0a8f8ad9000d, SHA256 ccabfccea64894fe18b6eee1de42259d7788b7ad2393439c3f5630fd0c4f5b28.
Chỉ metadata/canary năm path bên dưới; không product, protocol, workflow, credential, ACL/account, LIVE hoặc policy toàn kho.
Không Windows CI/full Windows mutants hoặc full M9 mới. Required gate vượt reserve thì checkpoint, không skip.
Window thực tế 2026-11-13T08:58:44Z đến 2026-11-13T11:58:44Z; không hồi sinh window g1 hoặc SOURCE đã đóng.

## Effective write set
- ops/admissions/wp1308-r2-g2.json
- ops/specs/wp1308-target-canary-r2.md
- ops/prompts/wp1308-target-canary-r2.txt
- ops/leases/wp1308-r2-g2-codex.yaml
- ops/canary/wp1308-target-canary.md

## Envelope và provenance
Một target lineage mới g0=2 chỉ sau khi chứng minh g1 chưa từng tạo state/witness và không begun attempt.
Giữ các init failures/transport diagnostics, toàn bộ chi phí/counters/unknown lịch sử; không refund/reset.
Một attempt, một review round, một independent Codex service reviewer requested xhigh so với executor high.
Thêm đúng một genuine GitHub Codex Connector review trên exact published H; tổng hai model workloads riêng, không dùng receipt source hoặc coi automatic event là miễn phí.
Serving model/effort không đo được vẫn UNKNOWN; model output là advisory, không human/native receipt.
Canary kỹ thuật tối đa60phút trong window180phút; reviewer tối đa10phút.
Hai P/H publication heads và tối đa hai Ubuntu PR CI heads/attempts; không automatic successor.
Đánh giá remaining fit trước mỗi action; timeout/skipped/infra/not_run/unknown không pass.

## Admission và bootstrap
Freeze spec → immutable admission, current lease publisher/bot/I2 và installed Mission từ canonical.
FILE chỉ byte copy; không mock TargetProof hoặc source policy, không tự bật ADR0054.
Quiescence/handoff và native topology phải đo lại đúng boot/root/mount.
Scoped init dương/âm: malformed/stale FILE bị chặn trước unauthorized state/witness write/dispatch; valid init chỉ awaiting_lease.
Witness initialized/high_water và state readback phải đồng bộ; private seed32bytes mode600, không công bố bytes/HMAC.
Record lease bằng actual I2/comments rồi reserve attempt trước executor work.
P chỉ gồm metadata đã được canonical control-plane admission/publisher kiểm, dùng tạo genuine PR identity.
H local giữ trọn năm-path diff từ baselineM, chỉ thêm canary metadata; source implementation không thay đổi.
Human audit phải có PR/H/tree/spec/generation/receipt thật trước first H publication; không chuyển MCR thành outcome audit.

## Review và nghiệm thu
Ghi transition/review-call reservation thật; independent reviewer đọc exact H, có raw output/provenance và closed advisory receipt.
Advisory approve chỉ approved_pending, accepted_sha/human_acceptance vẫn null.
Actual human exact-head audit/publication/CI/connector/canonical evidence trước accept; missing-human negative có healthy controls khi các inputs khác đã đủ.
Không formal GitHub Approve hoặc machine-as-human; không lấy source reviews/diagnostic để thay target acceptance.
Nhận actual receipts/source/code/runner binding, no-write negatives và bookkeeping/lease closure; PR0–PR8 chưa được dispatch bởi canary.

## Rollback
Mismatch/unknown/timeout/expiry: stop dispatch và checkpoint, giữ journal/witness/seed/history/counters.
Không xóa, restore/copy-back hoặc resume writer cũ. Boot/mount drift phải readmission đúng authority.
Không merge/revert source hoặc tăng cap trong Packet này.
