---
schema_version: 1
kieu: dac_ta_packet
packet_id: wp-codex-credential-refresh
packet_issue: 484
revision: 3
generation: 3
environment: local
platform: windows
executor: codex
risk: sensitive
review_class: sensitive
authority: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5612165878
base_sha: c0a5cbe89a90588115262e1a2c3ac84cbd98be9e
base_tree: f9897f6dba19484900776d7af7e9b042070d4ce1
branch: codex/wp484-g3-windows
depends_on: []
---

# WP484 r3 — khôi phục Codex credential trên Windows

## Objective

Materialize credential an toàn vào home Codex có hiệu lực; cho nhận snapshot mới khi auth thất bại, probe trước promote và resume đúng công việc. Không truyền snapshot thô cho child. Revision này thay spec hẹp r1 của #485 theo quyết định chủ kho đã ghi bền ở authority trên.

## Write set chính xác

```text
.claude/dev/codex_cred.py
.claude/dev/codex_cred_test.py
.claude/dev/codex_env_policy.py
.claude/dev/launcher.py
.claude/dev/launcher_test.py
.claude/hooks/session-start.sh
.claude/hooks/session_start.py
ops/handoff/wp-codex-credential-refresh-exec-g3.md
ops/leases/wp-codex-credential-refresh-exec-g3.yaml
ops/specs/wp-codex-credential-refresh.md
```

Không ghi CHANGELOG.md (#491), RELEASE_MANIFEST.json, VERSION, workflow, lease g1 hoặc các file khác. Tái sử dụng helper trong các file trên; cần thêm companion ngoài tập này phải xuất impact finding, không tự thêm quyền. CHANGELOG/release bookkeeping là land obligation, không phải quyền worker.

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

## Vai trò, lịch sử và dừng

- Executor: OpenAI Codex desktop/service, Windows local, machine/local. Reviewer: phiên Claude Code độc lập, source read-only; model/effort do chon_reviewer.py chọn, modelUsage kiểm lại sau lượt thật. Không đổi vai tự review.
- Reviewer không viết credential/launcher runtime cho executor; chỉ test/repro và finding. Không dùng hint runtime trong packet sensitive.
- Hai Codex review calls và hai verdict R1/R2 của #485 giữ nguyên. R3 Claude timeout 124 có token/output trong transcript nhưng không verdict; không xóa lịch sử hoặc coi là approve.
- G2 áp trần protocol: 3 content attempts, 90 phút/run, lease 240 phút, heartbeat 30 phút. Review deadline riêng; hết budget/same-failure/permission/quota thì rescue checkpoint. Không tự reset counters hoặc coi reroute là approve.
- Không push branch g1; successor PR phải trỏ lịch sử #485. Không merge/land/deploy/LIVE/force-push. Head/base/spec/ownership drift chặn thao tác phụ thuộc trước khi ghi; phải đo lại.

## Hash

Spec hash là SHA-256 toàn bộ bytes UTF-8 LF của tệp này, lưu ngoài tệp ở lease và comment authority/activation. Write-set hash dùng các đường trong khối text trên đã sort ordinal, UTF-8 LF, có LF cuối. Không tự chèn hash của tệp vào chính tệp.

## Continuation r3/g3 — quyết định chủ kho ngày 10-09-2026

R3 giữ nguyên sáu acceptance sản phẩm của r2; các mô tả lịch sử g2 ở trên không cấp quyền hồi sinh lease cũ. Entry candidate là3dcbfd7567a6c92be2d1182db95b84a4e738dbc1/tree8d6381d4920acceffb38b7015e0ed550c8b76bd8. Product diff base vẫn làc0a5cbe89a90588115262e1a2c3ac84cbd98be9e. G3 chỉ đổi metadata trước review; không tự rebase/merge master.

Quyết định chủ kho: https://github.com/ducthangho/tra-luat/issues/484#issuecomment-5612165878, theo CONTINUATION_G3_PROPOSAL.md SHA25614b4c9bb800181cc31bd3f2aae7e31f1f516b1b604992fa3c70dd6d6d05af27d. Lease g2 đã hết hạn, g3 chỉ bắt đầu sau admission và readback grant riêng. Không sửa lịch sử g1/g2.

Budget kế thừa: g2 đã dùng1 content attempt trên tổng3. State-dir g3 mới có trần2 attempt còn lại; tổng toàn chuỗi=g2(1)+g3(0..2), không reset. Commit metadata g3 tính là content attempt mới. Giữ2 Codex review lịch sử, Claude R3 timeout, g2 scope review, A1 approve, A2 timeout và A3 timeout. A2/A3 đã sinh nội dung, không refund. G3 được thêm tối đa2 Claude review calls, mỗi call20phút; model ratchet tối thiểu claude-fable-5/max. Các trần protocol30invocations/360cloud-minutes vẫn áp dụng;90phút/run,240phút/lease,heartbeat30phút. Không tự nới khi không hội tụ.

Reviewer dùng source read-only và scratch mới chuẩn bị sẵn với harness của repository; không recursive cleanup, không blanket Write/Edit vào source. Permission-mode default và danh sách tools tường minh. User-level codex_supervision_guard.py ngoài write set: không sửa/tắt/lách. Cờ JSON chỉ xuất kết quả cuối; transcript metadata mới là bằng chứng tiến độ, không stdout0. Permission failure phải được khai, không giả approve. Full candidate gồm metadata g3 phải được review exactSHA; prior runtime evidence chỉ được reuse nếu xác minh byte identity và khai giới hạn.

Được đăng authority/admission, verdict và receipt đã validate lên issue484/successorPR; không đăng credential/raw transcript. Chỉ push successor và mở draftPR khi candidate đủ điều kiện chạy fullCI cuối theo chỉ thị chủ kho. Chưa đủ required checks không được claim gate xanh. Không merge/land/deploy/LIVE/force-push.