```yaml
mission_issue: 76
packet_issue: 86
packet_id: wp86
revision: 2
generation: 2
spec_hash: bfadd19276dac14fa2f1263519ca9664ce4146c7899e4db43436546f18ffbe3d
source: '%TEMP%/tra-luat-wp86-cloud-handoff.md (máy ASUS, thu hồi 2026-08-11)'
note: 'Ảnh chụp handoff gốc. Trạng thái sống nằm ở Issue #86; Issue thắng khi lệch.'
```

# Handoff — wp86 RA-02 chuyển sang cloud/Linux

## Mục tiêu phiên mới

Làm Reconciler/Dispatcher độc lập cho Mission #76 và wp86. Tiêu thụ quyết định mới của chủ kho:
“Tôi đồng ý đổi môi trường” sau khi được đề xuất đổi wp86 revision 2 sang cloud/Linux runner.
Ghi quyết định này thành authorization bền, cài Packet revision/spec hash mới, kiểm preflight rồi
cấp lease và dispatch một Executor Codex/Linux mới. Không implement, review, merge hoặc land trong
chính phiên Reconciler.

## Trạng thái exact đã readback

- Repo: `D:\Quốc hội\tra-luat`
- Mission: https://github.com/ducthangho/tra-luat/issues/76
  - OPEN, `state:paused`, revision 2
  - plan hash `b170ac20b1c8ef211bb9ab5fd1a9ddfae84270b75bb91475ddf5d757750cafb5`
  - `max_agent_invocations: 68`, `max_cloud_minutes: 300`, `max_parallel_workers: 1`
- RA-01/wp77: integrated through PR #79 at merge commit
  `ea92ec960a23026ab345d8e9b97b36479a66d240`.
- Remote `mission/76/integration` readback currently equals
  `ea92ec960a23026ab345d8e9b97b36479a66d240`.
- RA-02/wp86: https://github.com/ducthangho/tra-luat/issues/86
  - OPEN, `state:proposed`, revision 1, generation 1
  - current spec hash `2675d472ff6943eefc5033d2d2ef999eb3f65bf7cafe3ba9078601a927d4f339`
  - current environment is `local`; this revision is to be superseded, not edited in place as if
    still valid.
  - Full objective, acceptance criteria and write set are authoritative in the Issue body; do not
    duplicate or weaken them.
- Local blocker evidence:
  https://github.com/ducthangho/tra-luat/issues/86#issuecomment-5248476131
- Mission pause event:
  https://github.com/ducthangho/tra-luat/issues/76#issuecomment-5248480320
- Mission MCR/budget evidence:
  - authorization: https://github.com/ducthangho/tra-luat/issues/76#issuecomment-5248394766
  - MCR analysis: https://github.com/ducthangho/tra-luat/issues/76#issuecomment-5248400061
  - revision install: https://github.com/ducthangho/tra-luat/issues/76#issuecomment-5248418968

## Thay đổi được chủ kho cho phép

Chỉ Packet wp86 thay đổi material:

- revision `1 -> 2`
- generation `1 -> 2`; fence generation 1 dù chưa có lease
- `environment: local -> cloud`
- `required_runner` đổi từ WSL2-specific thành credential-free Linux runner thực tế có working
  user/network/pid namespaces, non-root, read-only target, cgroup/resource controls và parent-held
  timeout
- label `env:local -> env:cloud`

Giữ nguyên executor Codex, objective, base SHA, integration branch, dependency `[77]`, hai write-set
prefix, risk sensitive, required review assurance cross-approved, acceptance/non-goals và mọi cấm
LIVE/release/deploy/merge/land. Không sửa Mission body hoặc plan hash: revision 2 của Mission đã cho
phép 300 cloud minutes.

## Trình tự bắt buộc

1. Raw-readback #76, #77, #86 và remote integration ref. Dừng nếu SHA/state/hash khác phần trên.
2. Duplicate/write-set/max_parallel/budget preflight. Recount `used / reserved / limit`; không reset
   lịch sử và tính phiên Reconciler mới vào ledger bảo thủ. Nếu không đủ dưới limit 68 thì pause.
3. Đăng authorization bền trên #86, nêu exact revision/environment change, `approved_by:
   ducthangho`, `decision: approved`, nguồn là owner reply trong task trước. Dùng reconcile key duy
   nhất và readback đúng một lần.
4. Sửa raw Issue body thành revision 2/generation 2, environment cloud và required-runner trung lập
   như trên. Thêm đoạn revision provenance nếu cần; không đổi contract khác.
5. Blank duy nhất dòng `spec_hash: `, chuẩn hóa LF, không trim cuối. Trước tiên tái lập anchor #60:
   `33a04b6fb5215dd79cf553908ecb7c1a8790f6951c379029bc184acd965b54d4`.
   Sau đó tính candidate, cài, raw-readback và xác nhận installed == recomputed. Không cài hash tính
   từ body cục bộ chưa đối chiếu raw.
6. Chuyển label wp86 sang `env:cloud`; vẫn `state:proposed` trong lúc capability preflight.
7. Probe runner thật trước lease. Việc có nhãn “Ubuntu” không đủ. Phải chứng minh non-root,
   user/network/pid namespaces, network isolation, target read-only, resource controls và timeout
   bên ngoài child. Job chạy candidate head không có secret. Nếu probe fail, giữ proposed và Mission
   paused; không fallback chạy trần và không tiêu content attempt.
8. Khi mọi readback đạt: `wp86 proposed -> ready`, `Mission paused -> running`, rồi cấp generation-2
   lease có expiry cho một Executor Codex mới. Tạo worktree/branch từ exact
   `mission/76/integration@ea92ec...`, ví dụ `agent/wp86-r2-g2-codex`; fetch/readback lại trước tạo.
9. Dispatch Executor bằng task cloud/Linux riêng với toàn bộ lease/spec URLs. Executor chỉ sửa:
   - `.github/coordination/reviewer_bootstrap/sandbox/**`
   - `.github/coordination/reviewer_bootstrap/oracle/**`
   PR phải Draft, target `mission/76/integration`; không merge/land.
10. Theo dõi heartbeat/handoff. Sau exact-head handoff, dispatch Reviewer độc lập cross-provider hoặc
    human audit; Executor không tự cấp assurance. Không merge nếu chưa có exact-head approve và
    authorization riêng.

## Stop conditions

- Không dùng raw token/cookie hoặc chạy candidate ngoài sandbox để lách runner.
- Không tự hạ assurance, mở write set, sửa `.github/workflows/**` hay năm schema Mission #54.
- Không sửa canonical/master, VERSION, changelog, release manifest; không deploy/LIVE.
- Bất kỳ head/base/spec/hash/lease mismatch nào: ghi evidence, pause, không push.
- PR #81 là orphan Draft lịch sử; không dùng hoặc merge.

## Suggested skills

- Reconciler hiện tại: không cần skill implement; làm control-plane và hash/readback thuần.
- Executor mới sau lease: dùng `implement` vì công việc bám Packet Spec #86.
- Nếu runner Linux vẫn hỏng: dùng `diagnosing-bugs` để phân loại capability failure, không sửa scope.
- Reviewer độc lập sau handoff: dùng `code-review` để review Standards và Spec trên exact head.
