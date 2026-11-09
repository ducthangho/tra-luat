# Mission #1238 — bàn giao dispatcher mới cho P2–P6

Prepared 2026-11-09T11:13:26.203249+00:00. Đây là đầu vào tiếp nối, không phải lease, spec revision mới, gói phát hành hoặc chứng nhận một phiên mới đã nhận quyền. Khi phiên mới nhận bàn giao, dùng một dispatcher duy nhất; phiên cũ kết thúc ở gói này và không khởi chạy P2 song song.

## Điểm chốt đã hoàn tất

Canonical master tại lúc đóng gói: `09643583d170c66ce3bcc74170d054d0f5ac9356`. P1-S4 #1296/PR #1301 đã landed; #1295 sửa thật và closed. [M8 authoritative](https://github.com/ducthangho/tra-luat/issues/1296#issuecomment-6738308285): actual MCI42595864844/23Ubuntu/selftest1777/strict184/officialartifact/full-sourceAUX8/fouranchors; D1–D4rc0, g3 retired2026-11-09T10:56:54Z, activeclaims0 trong write set. P1-S1/S2/S3 đã landed trước đó. Không mở lại/review lại P1 chỉ vì đổi phiên.

#1296 đã dùng author2/2, formal2/2(CLI1+human1), shared8/8, productpush1/1. Mọi counter/lỗi/parenthistory giữ nguyên; không mượn budget đã đóng cho P2. Human approval P1 H2 `15ad82f56924a0ccc99833ec73eec078ce00b726` không áp cho candidate P2 H2 khác dưới đây. P0 F1/F2 vẫn là historical exact-H7 owner exceptions, không sửa lịch sử hoặc mở rộng waiver.

## Quyền và vai trò kế thừa

Đọc AGENTS.md → CONTEXT.md → protocol → CLAUDE.md → Mission/Packet hiện hành → providerpolicy tại canonical mới đọc trực tiếp. Kế hoạch chuẩn `ops/plans/PROXIMA-PLAYWRIGHT-v1.md`, đồ thị/outcome không đổi. Status đầu tài liệu v1 và Claude-priority là lịch sử; chỉ thị mới nhất của chủ kho chọn Codex CLI Executor high và Reviewer Codex CLI fresh độc lập/read-only xhigh hoặc effort/model cao hơn. Không tự khôi phục Claude/AGY theo preference cũ. Không fork context Executor sang Reviewer. Phạm vi sensitive vẫn cần actual đủ assurance, không tự ký human.

Quyền tiếp tục triển khai/review/merge/land/ghi sổ đã cấp được giữ, đối chiếu dấu vết bền theo Packet; không xin lại xác nhận chung. Trước mutation phải xác minh exact scope/head/base/descriptor/spec/hash/budget/ownership/lease/hostauthority còn hợp lệ. Khi thật sự thiếu quyền hoặc dữ liệu, chuẩn bị checkpoint cụ thể rồi mới hỏi. Handoff này không tăng cap, không cấp lease hay quyền hostactivation/LIVE mới. Không Windows CI/full Windows mutant CI; focused native Windows được phép. U6 personal/non-commercial đã được xác nhận, không hỏi lại. Tối đa2productworkers khi write sets không giao.

## Thứ tự triển khai

| Phase | Packet | Hành động/điều kiện |
|---|---|---|
| P2 | [#1287](https://github.com/ducthangho/tra-luat/issues/1287) | Ưu tiên mở checkpoint r4 để phân biệt nguyên nhân U10; chốt fullCFTnative và cleanup OP-F01, rồi actualfreshreview/gates/PRCI/MCI/M8. |
| P3 | [#1297](https://github.com/ducthangho/tra-luat/issues/1297) | Sau P2landed: Desktop evidence→tra-luatverify→Proxima chỉkhiđượcyêucầu; chứng minh U11auth/WhatIf/isolation. |
| P4 | [#1298](https://github.com/ducthangho/tra-luat/issues/1298) | Có thể đọc nguồn/soạn thiết kế trong lúc P2blocked; canary/activation theo dependency. U4/U5/U7/U8/U12 phải đủ proof trước promotion, rollback binary+matchingtestprofile. |
| P5 | [#1299](https://github.com/ducthangho/tra-luat/issues/1299) | Sau Desktop/P4PASS, ASUS rồiVM theo hostplan/target-exclusiveauthority; không đổi gateway/account/endpoint/profile. |
| P6 | [#1300](https://github.com/ducthangho/tra-luat/issues/1300) | Đối chiếu mọioutcome/U1–U12/per-PacketM8/hostacceptance/leaseclosure/handover rồi mới đóngMission. |

Không gom P2–P6 thành một Executor/lease/PR lớn; dispatcher mới quản lý toàn lộ trình, từng Packet có nguồn và phiên thực thi riêng. Dependency chưa đạt thì làm phần planning/read-only độc lập, không chạy rollout để lấy tiến độ.

## P2 — trạng thái phải giữ nguyên

Immutable acceptance base `bf9914cb1a8e6f5047468f4d130b587015f8d73f`; unpushed H2 `2a5803e17b7ca4910c7188bfcc2276190e2d0b4b`, tree `bfb2fad8df2634ae8dd4c839a4565b76d1cfae45`. Ba tệp mới dưới `.agents/skills/playwright-browser/`: package.json/package-lock.json/SKILL.md; +377/-0. Source spec r3 `3d633584f9da9b8847d92d06d4a47104ccdbf21a:ops/specs/wp1287-r3.md`, SHA256 `9b8deaee351417aaf3e417b553bf5817c477aad6fdd811ab0711541c4eea5625`, controlref `ops/wp1287-spec`. [G3 lease lịch sử](https://github.com/ducthangho/tra-luat/issues/1287#issuecomment-6725545853) hết hạn2026-11-09T00:45:26Z; không có lease kế nhiệm đang cấp ở gói này.

Author3/3 đã dùng; formal0/2, shared2/8, productpush0/1. Không reset do phiên mới hoặc Issue khác. Không gọi author4 nếu chưa có checkpoint/allowance được authority hiện có thực sự bao phủ. CandidateH2 cleanup đạt49focused(Linux15+native34), fullLinux1777/strict184/Ruffdelta0/AUX2, nhưng **OP-F01 chưa formalclose và U10 fullCFTWindows FAIL**. Các kết quả cũ không chứng nhận currentmaster mới. Phân loại drift `bf9914cb1a8e6f5047468f4d130b587015f8d73f`→canonical hiện tại trước chốt admission/currentbase và phép carry; giữ B lịch sử, không rebase/resetbase âm thầm. SHA mới cần review/gates trên SHA đó.

FullCFT1252/CLI0.1.23 launch failed, Node24 diagnostic failed; headless_shell mở nhưng screenshotfailed; priorCLI0.1.22 failed. Không đổi pin/version/timeout/target hoặc dùng shell thay fullCFT để gọiPASS. D4 RAM~1.1GBfree là snapshot khác thời điểm, không chứng minh causal. Log Node24 có `<launched> pid5108` nhưng thiếu handshake, không tự gọi crash hay kết luậnNode24/RAM là nguyên nhân.

Đầu vào r4: `ops/checkpoints/wp1296-r3/P2-U10-diagnostic-design.md` trên controlref `ops/wp1296-spec` (cũng trong ZIP). Trước phép đo mới phải freeze r4/spec/hash/descriptor/boundedallowance/ownership/lease. Đề xuất tối đa một tái hiện đúng bộghim/target/timeout với instrumentation launcher/browser, ownedPIDtree/exit/tài nguyên/sựkiện cùng thời điểm. Nếu không phân biệt được giảthuyết thì dừng checkpoint, không loop mù. Source/pin change là quyết định cụ thể riêng; root dispatcher không vá sản phẩm thay Executor.

## Host và unknowns

Snapshot thiết bị vừa đọc: Desktop `a5f7076e-a491-4f84-829b-8d1fbcc1c767` online; ASUS `7404cfba-9034-4787-b46b-7c358126a411` offline; hai connection tra-luat-win `f7281f27-f79f-40a2-a2f5-b454b58a166a` và `810f79bb-c01e-4157-a5f2-9562ac6d551d` online. Phải list/recheck identity lại, Online/hostname không phải authproof; hai connection VM từng cùng OSfingerprints không cho phép hoán đổi tùy ý. Desktop là native target thử trước, không thay bằng VM khifail.

Desktop có Python thực `C:\tl-win\wp1271-tools\python-3.12.10\python.exe`; alias python từng là WindowsApps stub, không dùng để suy test đã chạy. PS7 `C:\Program Files\PowerShell\7\pwsh.exe`; native PS51 cũng đã được đo. Lock `C:\tl-win\KHOA.txt`, ledger `C:\tl-win\do-luong.csv`: cô lập ownedfixtures/PID, heartbeat/deadline/cleanup/realrc theoADR57–59. Không đổi policy toànmáy/tắtsandbox/antivirus/kill-all/copyloginprofile. Quyền trust cũ chỉ đúng thư mục đã nêu, không mở rộng qua bàn giao.

U1/U3 isolatedcontrols và U2partial fingerprints không phải realendpoint/auth/installedruntime proof. P4 sourcev5.5.0 cho thấy autoDownload/onquitinstall; P4-DESIGN-F01/U5/U12 provenance/pin chưa đủ, hash không thay attestation/signature-policy. Không kích hoạt installer/updater/service/endpoint mới để đóng unknown. U7retention/soak, U8testprofile restore, U9disk/ACL/cache/rollbackreserve, U10nativecompat, U11remoteauth còn phải nghiệm thu đúng phase.

## Gói offline và khởi động phiên mới

ZIP chứa `P2/candidate-H2.bundle` và bản gốc budget/spec/lease cũ/handoff tác giả/critical nativeZIPs+Linuxflow evidence/manifest. Bundle là local offline transport, không đẩy candidate chưa review lên remote. Clone canonical có đủ history B; `git bundle verify` trước import `refs/heads/agent/wp1287-r3-g3-codex` vào ref candidate riêng, kiểm head/tree/3paths. Không thực thi candidate hay test từ bundle trước preflight/lease. RawZIPnative giữ nguyên; node_modules/npm-cache/.git và các clone core-combination lớn không đóng lại, exclusions có danh sách và các nguồn còn tra qua pinnedreceipts/controlrefs. Không xem đóng gói là chạy lại hoặc audit toàn bộ evidence.

Nếu phiên mới dùng workspace khác, đính kèm ZIP để chuyển H2 chưa push và rawsource; localpaths chỉ là gợi ý, không giả định chúng tồn tại. File auth/credentials/loginprofile không nằm trong phần lựa chọn đóng gói. Không chạy mù script lịch sử vì có constants H/M cũ; luôn đo và bind actualidentities lại. Receipt/humanwaiver/lease cũ có scope/time riêng, không được hồi tố hoặc chuyển candidate.

Bước đầu phiên mới: nhận vai dispatcher duy nhất trên Mission bằng ghi nhận bền, đọc lại nguồn/currentfacts, kiểm gói/hashes/B/H2/budget và activeclaims, soạn r4boundeddiagnosis rồi cấp đúng lease trong quyền đã có. Sau từng Packet đạt thì review/CI/land/M8/retire/readback và chuyển dependency kế tiếp. Không gọi Missioncomplete khi còn requiredoutcome/unknown/lease chưa đạt.
