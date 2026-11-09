# Human audit H2 — Packet #1296 / PR #1301

Trạng thái: hồ sơ để người audit tự đọc; **chưa có human verdict**. PR [#1301](https://github.com/ducthangho/tra-luat/pull/1301) còn draft. Quyền thực thi merge/land đã được chủ kho cấp trong hội thoại; hồ sơ này yêu cầu một hành vi khác: người độc lập thực sự đọc và đánh giá code/spec trên SHA mới. Codex không thể tự xác nhận việc người đã đọc.

Candidate H2 `15ad82f56924a0ccc99833ec73eec078ce00b726`, tree `50fbceb65cea60cc62222c3cd3a3651a6dd13981`; immutable base `91be484a05ab40adf6573f11ef6ec0264fc9a3aa`. Spec revision3/generation3, SHA256 `780a5fa9b7cf86ec277e734bbbd43c9d1ef153b4750227ae173987a192fb39c4`. Bản vá một tệp +66/-2, không thay runtime module, manifest, S1/S2, workflow hoặc release files.

## Đọc và tự đánh giá hai trục

Đọc [toàn bộ diff](entire-product.diff), [toàn bộ harness H2](product/ProximaManifest.Tests.ps1), [spec r3](spec/wp1296-r3.md), và [verdict độc lập nguyên bản](evidence/model-verdict.md). Nguồn GitHub bất biến: [harness](https://github.com/ducthangho/tra-luat/blob/15ad82f56924a0ccc99833ec73eec078ce00b726/.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1), [spec](https://github.com/ducthangho/tra-luat/blob/552e80497c44d3f7a9b162875e86c02ffe2e6bb8/ops/specs/wp1296-r3.md). Các gợi ý sau không giới hạn finding mà bạn có thể nêu.

- **Spec:** comment vô hại và metadata null/default được chấp nhận; genuine requirements được chặn không phụ thuộc chữ hoa/thường hay culture. API `RequiresPSSnapIns` của PS5.1 và API Core được xử lý đúng. Chốt cấu trúc AST và schema vẫn giữ. Literal `RootModule='#REQUIRES -Version 5.1'` phải PM01pass và PM02VALUE[RootModule]/runtime0, không được tính thành normal7-positive hoặc semantic kill.
- **Standards/security:** kiểm requirements trước SafeGetValue/import; member/kiểu không biết fail-closed; không chạy manifest để tìm requirements. Các guard named blocks/traps/background/node/child/bool/parse-error và kiểm hash/runtime cô lập có bị yếu đi hay tạo hồi quy khác không?

## Bằng chứng đã kiểm, cùng giới hạn

Actual independent CodexCLI reviewer gpt-6.1-sol/xhigh > executorhigh, fresh clone/context read-only, cả hai trục approve, findings[]; [v2 delivery](evidence/model-delivery.receipt.yaml). Đây là same-provider, không phải human/cross audit.

[AUX2](evidence/AUX2-native-Linux.json) kiểm đủ1876 tệp native/95 observations/95 dòng ledger, normal7/CX12/S2normal26 trên cả PS5.1/7;57 meaningful requirement rejections,6literal,3PS7snapin inert, historical/parser/baseline/guard-only rollback controls. Linux exactH2 1777/1777, strict184/184, Ruff rc1/12F821 lịch sử/delta0. Source Windows là scoped committed-blob export, không fullGitcheckout; parent cultures và children en-AU được khai riêng. H1 API failure và hai operatorrc2 giữ nguyên với timestamp riêng, không ghi lại thành pass. Không chứng minh arbitrary-code execution hoặc gateway/endpoint thật.

[AUX5 PRCI](evidence/AUX5-PRCI.json) PASSED: run42583491058 attempt1,23/23Ubuntu và24/24checks; đọc23logs/43962dòng/95sourcefiles. Actual synthetic checkout51a3fb14080c946397b506945caafc0618742393 parents[B,H2], treeH2. Actual GraphQL/REST workflow-definition byte/OID được kiểm. Core1777/1777; G5 61ca/490mutants/0errors; packet-loop1359/1359 với một ca Windows và mutant tương ứng không ghi công. Rawcanonical not_measured giữ nguyên, manualfullsourceaudit riêng. Admission officialZIP/checker0 nhưng A0discoveryNOT_RUN do upstream policy, không gọi activationpass. PR workflow không sinh lifecycleartifact; actualpostmergeartifact vẫn phải có sau merge.

Connector [receipt](https://github.com/ducthangho/tra-luat/pull/1301#issuecomment-6735243094) đã review đúngH2/no findings, summary hiddenstate đầy đủH2; securityreview của connector chưa chạy, không suy thành crossassurance. WindowsCI/fullWindowsmutantCI không chạy theo chỉ thị chủ kho; focusednative đã đo. Không LIVE/deploy/runtimeactivation.

Nợ #1295 được reviewer xác nhận đã vá thật trong code; vẫn OPEN tới khi land. Waiver/human audit H4 cũ và P0 F1/F2 lịch sử không chuyển sang H2. Không có finding mới được phát hiện trong các lượt hiện có; nếu bạn thấy lỗi, ghi finding của chính bạn.

## Điều kiện tiếp theo và kết luận của người audit

Currentmaster vẫn B, currentPRhead vẫn H2, chỉ g3 có hiệu lực trong write set. Rules endpoint đọc được các required contexts; legacybranchprotection API403 giữ như hạn chế, không suy thành không có protection. Lease YAMLalias đã sửa dạng biểu diễn bằng hai danh sách tường minh: toàn bộ mapping quyền/spec/generation/expiry trước/sau bằng nhau, không đổi H2. Preflight K0/K1/K2/K3/K5/K6/K7 không báo thiếu; K4 được để chờ tuyến human-sensitive-assurance, không bịa owner record. AIreview thật/v2 vẫn giữ riêng.

Sau actual human approval trên H2, dispatcher mới ghi bền verdict của người, kiểm lại head/master/rules/refs/lease/K0–K7, Ready và auto-review terminal, normalmerge, actualMCI/officialartifact/fullsourceAUX, M8/readback/retire/D1D4. Hậu kiểm chưa chạy; chưa merged/landed, Mission chưa complete. Nếu base/head/authority stale hoặc gate khác không đạt, dừng theo thực tế.

Người audit tự ghi: đã đọc spec/toàn bộdiff; đánh giá của mình cho hai trục; finding còn mở hoặc không; verdict `approve`, `changes_requested` hoặc `blocked` trên exactH2. [Template](human-verdict-template.json) chỉ để điền sau khi thực sự đọc, chưa là verdict.

Nguồn yêu cầu: [PROTOCOL §8](https://github.com/ducthangho/tra-luat/blob/91be484a05ab40adf6573f11ef6ec0264fc9a3aa/docs/PROTOCOL_DA_PHIEN.md#8-review-phân-tầng): người audit phải “tự đọc spec/diff, ghi evidence audit và verdict bền”; same-provider không thay assurance bắt buộc của class sensitive.
