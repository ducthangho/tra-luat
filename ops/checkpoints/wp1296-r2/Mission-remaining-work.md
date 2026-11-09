# Mission1238 — phần việc còn lại sau P1-S3

Owner yêu cầu09/11: tạo Packet sửa nợ, gom các việc cần để hoàn tất Mission. Kế hoạch v1/outcomes giữ nguyên; bảng này là register triển khai, không tự cấp host activation/LIVE hoặc bỏ gate.

| Việc | Packet | Trạng thái thật / điều kiện đóng |
|---|---|---|
| Guard ScriptRequirements / debt1295 | #1296 | r2/g2 một tệp. H1 Linux1777đạt nhưng PS51normal1/7FAILED vì tên RequiresPSSnapIns; r2 sửa theo actual API probe. Chưa review/CI/land, debt1295OPEN. |
| Playwright optional + cleanup OP-F01 | #1287 | H2cleanup49focusedđạt, formalNOTRUN; U10 fullCFTnativeDesktopFAILED. D4readonly mới không chứng minh nguyênnhân. R4 cần giảthuyết/checkpoint/frozenallowance, không blindretry hoặc đổi pin/timeout/target. |
| Desktop combined canary | #1297 | proposed, chờP1/P2/corrective. Thu bytes/URL/time/hash → tra-luatverify; Proxima chỉkhiđượcyêucầu, khônghealthcheckinference/retry/fallback. U11auth/U2ifVM phảiđo. |
| Updater/rollback | #1298 | proposed. Sourcev5.5.0 vẫn autoDownload/onquitinstall; P4-DESIGN-F01 chưachứngminhpin/idle/canarycontrol. U4/U5/U7/U8/U12 chặnactivation. Verify binary+data/testprofile rollback/failurepause/locks/busy/diskfull; sourcepolicy khôngtựhạ. |
| ASUS rồi VM | #1299 | proposed, sauDesktop/P4PASS. ASUSOffline; exactVMconnection/fingerprints/capability/remoteauth/cachefreeD+ACL/rollbackreserve/provenance phảiđo trước riêngtừngmáy. Khôngđổigateway/account/endpoint/profile hoặcđổitargetkhiDesktopfails. |
| Final acceptance / handover | #1300 | proposed, chỉđóngMissionkhi mọirequiredPacketlanded/eachacceptance/readback/leaseclosuređạt. Source/installedmodule/runtimeversions táchriêng; vận hành/pause/uninstall/limits cóbằngchứng. |
| P0F1/F2 | #1239 historical | ownerwaived exactH7/6704067442, immutableblockedverdict/servingidentitynotmeasured giữnguyên. Khôngphải patchcodecóthểsửa bằngsuydiễnquákhứ, khôngapplywaiverchoSHA mới. |
| Lưu Git thụ động | M8 S3 / weeklylane | M8Issue làauthoritative, đãpost/readback/D1D4/closure. QueueweeklyarchivekhôngchặnđóngPacket; khôngđẻmodelreview/WindowsCI/PRđệquy. |

U6 cá nhân/phi thương mại đã được chủ kho xác nhận. U1/U3 đã có isolatednativecontrols; khôngđồngnhấtvớirealendpoint/auth/installedruntime. U2 đã cóOSfingerprints cùngVM, khôngphảihardwareattestation/auth. Unknowns còn lại giữmởtới khi cóproof, khônggọiMissioncomplete từ việc đãtạoIssue.

Executor: freshCodexCLI high; Reviewer: freshindependentreadonlyCLI xhigh, sameprovider. Sensitiveassurance phảiđủ theoactualevidence/newexactSHA; rootkhôngkýhuman. MỗiPacketfreeze spec/hash/descriptor/budget/ownership/lease trướcproductwrite; tốiđa2productworkers. OwnerkhôngchạyWindowsCI/fullWindowsmutantCI; focusednativeallowed. Mọichi phí/lịch sửparent vàAGYunknown đượcgiữ, khôngresetquaIssue.
