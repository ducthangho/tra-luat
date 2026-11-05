# Hồ sơ audit cá nhân — Packet1178 r4/g4

Candidate: `ef864d6b3192a08487cd7fc0e526633afcb693d9`
Tree: `70bc751068856245e92875a13e182a9c90781f8b`
Immutablebase: `ec1b18a2a007fc2e697249c727a2ca8391ab209e`; continuation: `a7b5aedc122575a66280ace3ff7f2567251af8e2`.

Spec r4-ci đã duyệt: [nguyên văn frozen](https://github.com/ducthangho/tra-luat/blob/23e75a488361ed3c1de007a56b328bf518969437/ops/specs/wp1178-r4-p2-ci.md), SHA256 `7886c45258405b3376f34ea084d12a13faceaabf056cf898a3a7db9e588bf0e2`.

Đọc [toàn bộ diff ec1→H](full-baseline.diff), gồm sáu tệp/+1181 dòng; [diff sửa tiếp a7→H](continuation.diff) chỉ hai tệp/+273/-8. Bốn tệp kế thừa giữ nguyên blob a7.

Ba P2: chuẩn bịcurl trước downloader; chặn Python có số phiên bản đang chạy trước apply; probe thực thi --version của CLI trước giữ nguyên/cài sửa. Embedded --selftest chạy entrypoint thực trong fixture cô lập; CI thêm đúng một step Linux gate-ops. Không apply lên máy thật.

Đã đo tại đúngH: tl selftest1776/1776; Ubuntu root48/48,nonroot48/48 (mỗi lượt6mutants+6healthycontrols); baselinea7 đỏ đúng ba property families; harness integrity2/2. Syntax/ShellCheck/actionlint/7workflowcontracts/EOL/diff đều0. Canonical admission tại immutablebase0; currentmaster→H không phải ancestor, được ghi riêng, chưa xác nhận integration.

NativeWindows M3: ASUS-LAPTOP, baselineec1 4/4 và candidateH6/6 trong cùng orchestrator. Cảhai sharedcheckerDAT với canary khác rỗng; parserPS+syntaxBash inventory xanh; candidate updater check-only và login idempotence xanh. Khóa đã nhả0bytes. [Raw paired evidence](windows-paired-evidence.json); [archive](windows-evidence.zip), SHA256 `25b62f5d130118f2a581bfbcee68e804e731d12e7f42fce9c127d07256290856`, CRC/log hashes đã kiểm. VM đang bận phiên khác nên không dùng.

[Executor handoff](executor-handoff.md) và [77filemanifest](executor-evidence-manifest.json), SHA256 `c90363dc1fa8f837bd3af21a83b0deb552f6a4717bc5837880e8387d2ad6ef25` đã kiểm nguyên vẹn. Source sạch kể cả ignored, chưa sourcepush.

Cần chủ kho trực tiếp đọc spec và FULLdiff của head mới, chốt findings, rồi xác nhận human_audited và quyền land cho exactH này. Audit/land cũa7 không chuyển sangH mới. Đây chưa phải PRready hoặc merged/landed. Sau audit còn connector mới,CI/M9,infra1187 dependency,fullfence,postmergeCI/M8/D1–D4. Không deploy.
