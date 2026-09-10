---
schema_version: 1
kieu: dac_ta_packet
packet_id: wp-codex-credential-refresh
packet_issue: 484
revision: 4
generation: 4
environment: local
platform: windows
executor: codex
risk: sensitive
review_class: sensitive
authority: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5613357281
base_sha: c0a5cbe89a90588115262e1a2c3ac84cbd98be9e
base_tree: f9897f6dba19484900776d7af7e9b042070d4ce1
branch: codex/wp484-g4-windows
depends_on: []
---

# WP484 r4 — khôi phục Codex credential trên Windows

## Objective

Materialize credential an toàn vào home Codex có hiệu lực; cho nhận snapshot mới khi auth thất bại, probe trước promote và resume đúng công việc. Không truyền snapshot thô cho child. Revision này thay spec hẹp r1 của #485 theo quyết định chủ kho đã ghi bền ở authority trên.

## Write set chính xác

```text
.claude/dev/codex_cred.py
.claude/dev/codex_cred_test.py
.claude/dev/codex_env_policy.py
.claude/dev/launcher.py
.claude/dev/launcher_test.py
.claude/dev/packet_loop_test.py
.claude/hooks/session-start.sh
.claude/hooks/session_start.py
.github/workflows/launcher-windows.yml
ops/handoff/wp-codex-credential-refresh-exec-g4.md
ops/leases/wp-codex-credential-refresh-exec-g3.yaml
ops/leases/wp-codex-credential-refresh-exec-g4.yaml
ops/specs/wp-codex-credential-refresh.md
```

Không ghi CHANGELOG.md (#491), RELEASE_MANIFEST.json, VERSION, workflow ngoài phạm vi, lease g1 hoặc các file khác. Tái sử dụng helper trong các file trên; cần thêm companion ngoài tập này phải xuất impact finding, không tự thêm quyền. CHANGELOG/release bookkeeping là land obligation, không phải quyền worker.

## Acceptance và phản chứng

1. **Home nhất quán.** Launcher, env-policy, doctor, hook và codex_cred cùng dùng CODEX_HOME khác rỗng; vắng/rỗng dùng ~/.codex. Test cả custom/default home, đường dẫn không hợp lệ và legacy policy ở cả hai home. Doctor không báo thiếu credential trong khi materializer vừa ghi vào custom home.
2. **Đầu vào và đích an toàn.** Validate object/tokens trước freshness; reject malformed JSON, UTF-8 hỏng và schema không hợp lệ bằng lỗi kiểm soát. Từ chối symlink/reparse point ở file hoặc ancestor; không ghi credential vào repo. Atomic replace và quyền truy cập phù hợp nền; fail-closed khi không chứng minh được primitive an toàn. Không hạ cấp snapshot mới hơn; đo byte-preservation khi từ chối.
3. **Ranh giới môi trường.** Materialize trước mọi child/probe/version; loại CODEX_AUTH_JSON khỏi child environment. Test fake child thù địch đọc biến và kiểm credential tại home đã chọn. Không log raw/base64/token hoặc truyền qua argv.
4. **Đổi snapshot có kiểm chứng.** Auth failure sinh trạng thái chờ snapshot mới; cùng snapshot đã thất bại không được retry vô hạn. Probe candidate trong vùng riêng bằng cơ chế codex_cred có sẵn, đòi rc=0 và marker TRALUAT-CRED-OK. Chỉ promote sau thành công; lỗi/timeout/missing marker giữ nguyên credential cũ. Không sửa config người dùng hoặc tự khởi động device-auth trong test.
5. **Resume và attempt.** Lưu checkpoint tối thiểu không chứa secret, neo HEAD/prompt hash/checkpoint identity. Credential mới không cho resume khi bất kỳ mốc nào lệch. Auth/quota failures có evidence được tách khỏi content attempt; unknown failure không được tự void. Có ca phản chứng giả thông điệp auth/quota nhằm tránh hoàn attempt sai.
6. **Bằng chứng và hồi quy.** Regression r357-r360 của #485 phải được tái dẫn xuất trên base mới. Giữ stable IDs `cred-r1-probe-inherits-raw-snapshot` và `cred-r1-hook-keeps-stale-readable-auth`. Các ứng viên R3 (home divergence, corrupt-disk crash) chưa có severity cuối; đo lại trước phân loại. Test Windows và Linux theo phạm vi, ghi riêng skipped/not_run; mock không thay bằng chứng kernel.

## Gate và admission

- Dùng ops/lease_publish.py kiểm schema lease, review class và hash prompt/spec; rà ownership bằng ai-dang-giu rồi đối chiếu quyết định bền mới hơn, không coi TTL file cũ thay thế authority.
- Policy `.github/coordination/change-impact.v1.json` được protocol mô tả nhưng chưa có ở base này. Không khai đã chạy closure validator. Manual admission chỉ được dùng tập exact paths chủ kho duyệt, review class sensitive và không mở rộng companion; bất kỳ coupling mới nào đều chặn nội dung tới khi được chốt.
- Targeted: credential tests, các case launcher liên quan, env-policy tests hiện có qua harness của kho, bash syntax và Python syntax. Windows UTF-8 phải được đặt trong môi trường test. Lỗi nền t11 được đo đối chứng trước khi xử lý; không bỏ guard để làm test xanh.
- Final worker gate theo CLAUDE.md/protocol: positive test evidence, temporary manifest verify, exact changed-path/spec/lease/EOL checks; một full oracle trên mỗi exact identity. Không tự sửa security/gate/manifest để qua.
- Hosted CI cuối chỉ sau khi candidate đóng băng và review xong; Windows launcher bị skipped không coi passed. Không claim gate xanh nếu thiếu required check hoặc positive marker.

## R4/G4 authority, scope limits and budget

Owner decisions: issuecomment-5613270248 and issuecomment-5613357281 on issue #484. Entry candidate 625ea2a2cbe37626970550c8c2b4800af214b5fb, tree cb8161ee4a4fb36403db19514455332a916f24dd. Product base remains c0a5cbe89a90588115262e1a2c3ac84cbd98be9e. G3 independent approve and failed CI runs 34434932435 / 34434934941 remain historical exact-SHA evidence, not current acceptance.

Executor OpenAI Codex desktop/service, Windows local, machine/local. Reviewer independent Anthropic Claude Code, machine/local, source read-only, external prepared scratch, sensitive class, model ratchet >= claude-fable-5/max with final modelUsage validation. Executor never self-reviews or self-approves. No real credential/device-auth/LIVE probe in tests.

The G3 lease file may ONLY receive da_bi_thay_the pointing to G4; all historical values remain. G4 lease must carry the reverse thay_the_cho marker. Metadata-only administrative commits/pushes on G3 and G4 are authorized to establish consistent two-way ownership before content work; G3 journal is not reset. Re-scan full refs and ownership before beginning the sole remaining content attempt.

packet_loop_test.py changes are limited to stale void fixtures and genuine positive/negative nonce controls for void_bo_dot_nonce and void_bo_khop_nonce. Never restore automatic refunds for unknown post-spawn child failures. launcher-windows.yml changes are limited to installing/probing shellcheck, rg and actionlint with existing repo tools; no altered selection, skips, assertions, permissions or runner matrix. All other runtime changes repair demonstrated credential/test failures within the listed paths.

Global content attempts used 2 of 3; G4 may use exactly one remaining attempt. Preserve historical reviewer calls and G3's consumed Claude call; one further Claude call, at most 20 minutes. No timeout refunds or counter reset. New run starts 2026-09-10T04:50:00Z and ends no later than 2026-09-10T06:20:00Z; protocol invocation/cloud-minute limits remain. Lease lasts 240 minutes from verified durable grant timestamp, heartbeat every 30 minutes, no automatic renewal.

Run targeted Windows/Linux neutral and adversarial tests, freeze candidate, cross-review, then exactly one full CI per final reviewed identity. Required skipped/missing checks are not pass. Publish validated verdicts and receipts to #484 and successor draft PR; no raw transcripts or credentials. No merge, land, deploy, LIVE, force-push, guard change/bypass or unapproved path. If budgets or a repeated failure prevent convergence, preserve evidence and use rescue, not another call.

## Owner-approved continuation run

Authority: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5614142416. Owner approved continuation on the same r4/g4 from 2026-09-10T06:22:58Z to 2026-09-10T07:52:58Z. This replaces only the expired run clock, preserves global3/3 used attempts and one remaining Claude call, max20min. Owner additionally authorizes CI after independent approve, and conditional merge/land only after exact-SHA required gates and protocol authority/audit checks. This supersedes the earlier no-merge/no-land instruction conditionally; no deploy, LIVE, scope expansion or extra attempt/review. Lease expiry unchanged.
