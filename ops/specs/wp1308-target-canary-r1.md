# wp1308 r1 — Admission và canary target ASUS WSL
packet_id: wp1308
revision: 1
generation: 1
mission_issue: 1172
mission_revision: 30
mission_plan_sha256: 51653585b74fc47054c24e574fb9a5cad08dda87b555f8eab3cff3121e174781
contract_id: WP1308-r1-target-asus-canary
immutable_acceptance_baseline: 6f32aad6fe9db93867fc87456541740f80bf79a4
admission_ref: refs/heads/ops/wp1308-target-r1-g1@4286691bba2f7181397bec9d00c0ba1089542f7a
admission_path: ops/admissions/wp1308-r1-g1.json
admission_sha256: a3929510cfc85b7183e40a87b959a45140a6e2e99f0f2bb6ef50eecae123a936
executor: codex
environment: local
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: human_audited

## Assignment
Quyết định TARGET-ASUS-1 của chủ kho đã được ghi nhận tại Mission1172/comment6818098358; installed plan30/comment6818183619.
Sole dispatcher Packet1308; source1174/1303 đã đóng, chỉ giữ lịch sử.
Scope chỉ một journal fresh lineage, runtime ASUS Ubuntu-Clean WSL2/ext4 ordinary user, metadata canary.
Write set hiệu lực: ops/canary/wp1308-target-canary.md.
Không sửa product/protocol/workflows/accounts/ACL/credentials/LIVE; không Windows CI/full Windows mutants, không M9 mới.
Descriptor phải được phát hành qua immutable Git và lease publisher/I2 thật trước init; local copies không cấp quyền.
Hết cửa sổ 2026-11-12T11:03:13Z hoặc boot/mount drift thì dừng, readmission đúng authority, không tự gia hạn.

## Envelope
Một attempt, một review round, một Codex service review call độc lập requested xhigh so với executor requested high.
Actual serving identity unknown nếu không đo được. Canary bounded10phút; toàn cửa sổ180phút tính từ installed event.
Giữ mọi lịch sử/failure/counter/unknown costs, không reset, không vay allowance source.

## Acceptance và thứ tự
1. Xác minh canonical product/launcher, installed Mission30, exact spec/admission/lease và current expiry/revocation.
2. Xác minh runtime root/boot/mount/ext4+magic, quiescence/handoff, seed ownership600 và fresh lineage.
3. Scoped init qua launcher; state awaiting_lease/revision0, witness initialized/high_water đồng bộ.
4. Record lease bằng I2(H/Đ/R) thực tế; begin-attempt một lần, reserve trước dispatch.
5. Tạo local metadata canary candidate, ghim SHA/tree/diff; reviewer độc lập có effort cao hơn đọc exact H.
6. Scoped service advisory review chỉ vào approved_pending_human; thiếu actual-human không accepted.
7. Sau concrete human audit đúng PR/H/tree/spec/generation/state/receipt, controlled publication/CI/collector/accept theo protocol hiện hành.
Không tự tạo human receipt hoặc suy MCR approval là target acceptance. Bước7 chưa thể nhận pass trước người thật review.
8. Negative malformed/stale admission bị chặn/no state or witness write/no dispatch; giữ raw outcomes/rc.
9. Bookkeeping/lease closure thực tế; PR0–PR8 không được dispatch trước target acceptance.

## Rollback
Mismatch, timeout, unknown hoặc quota hết: không dispatch/retry mù; giữ journal/witness/seed/counters và receipt.
Không xóa hoặc copy-back để reset. Boot đổi cần readmission, không sửa trực tiếp binding đã frozen.
Không tự promote target toàn kho, không successor tự động.
