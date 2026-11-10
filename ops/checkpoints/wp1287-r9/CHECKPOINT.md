# R9 — operator native fullflow PASS với action timeout10000

Quyền mới: chủ kho cho phép “tăng gấp đôi timeout” sau lỗi screenshot5000 ở R8. Thực hiện bằng cấu hình chính thức `timeouts.action=10000`, áp dụng cho các action dùng setting ấy. Launch30000/navigation60000/cleanup20s, pins/H2/Desktop giữ nguyên. Source ghim cho thấy default action5000 và screenshot dùng `tab.actionTimeoutOptions`.

Exact frozen execution control `64a54d8b7135674d573dc2c90833d8ccf72a64ee`; H2 `2a5803e17b7ca4910c7188bfcc2276190e2d0b4b`, tree `bfb2fad8df2634ae8dd4c839a4565b76d1cfae45`. Native13/13, ABI64bitME1080/WN280, fresh npmci/signatures/browser-install rc0, source/helper/CFT hashes matched; GitHub lease gate/fullref ownership passed trước run.

Actual child/shell0. Open12,922s; currenttab/redirect302→200/exactnonce UTF8body fixture_verified. PNG1280x720/7233bytes; PDF22774bytes parsed with expected marker+nonce; PNG/PDF commands rc0. Cleanup close0/delete0/expectedclosed1, independent readback verified, remaining0/gaps0, host lock empty. Screenshot elapsed0,360s trong lượt này: không chứng minh tăng timeout là nguyên nhân làm hết lỗi R8; đây là PASS thực trên cấu hình mới, không causal A/B.

Observer quality PARTIAL:8complete/8inconsistent module walks, do not promote inconsistent probes or infer loader cause. Observer quality does not invent a product capture failure where actual PNG/PDF proof passes. Original R8 fail/reporting-error/recovery remains unchanged. No raw native logs/profile/path export; allowlisted summary/hashes only. Native summary SHA256 `b140bb8adf494b34de4d08d55521d453c8a001492dde56f5641c9b82a25e5072`; local `native-summary.json` wraps that source digest and JSON projection.

Allowance1/1used, g9 retired at actual verified cleanup/readback; original expiry retained separately. Product authors3/3/shared3/8/design1/1/formal0/2/productpush0/1 unchanged; no product edit/new model call. U10 remains OPEN for documented PowerShell5.1/7 positives and formal OP-F01; sensitive assurance HOLD. Proceed to bounded documented-shell proof, not repeated R9 runtime experiments.
