# Hồ sơ để người audit tự đọc — PR #1294 / wp1285 r8/g9

**Trạng thái: CHỜ HUMAN AUDIT THỰC TẾ. Chưa có kết luận “đạt”, chưa merge/land.** Đây là hồ sơ do Codex dispatcher chuẩn bị, không phải verdict của người audit. Chỉ ký sau khi tự đọc các nguồn; có thể trả changes_requested thay vì approve.

Ứng viên H4 `ecd8cee3ea6da6513a37a9b9aa6c9db65472e41c`, tree `ebe647c4bc68fb75b3ad7319a79ad3bf0f143a70`. [Spec r8 đóng băng](https://github.com/ducthangho/tra-luat/blob/03c626536460de0217b9de24c052fed202643a1e/ops/specs/wp1285-r8.md), SHA256 `d8195383ceed002d15b9db09e51cae1c4f2d90f0237ef33333cead4d629b26e9`. Bản r5–r8 nguyên văn trong [spec-chain](spec-chain). Người được đề nghị audit: `ducthangho`, độc lập với tác giả sản phẩm thực tế là Codex CLI; tài khoản GitHub dùng vận chuyển output không được coi là model author hay bằng chứng người đã đọc.

## 1. Đọc toàn bộ thay đổi sản phẩm và spec

[Toàn bộ diff E..H4: 3 tệp mới / 450 dòng thêm / 0 dòng xóa](entire-product.diff). Cả ba bản trong [product](product) có byte/hash khớp source H4; source gốc cũng ở các liên kết dưới:

- [Manifest, 13 dòng](https://github.com/ducthangho/tra-luat/blob/ecd8cee3ea6da6513a37a9b9aa6c9db65472e41c/.agents/skills/proxima-control/scripts/ProximaControl.psd1): đúng các giá trị/exports, module2.0.0, PS5.1/Desktop+Core; không khởi động dịch vụ hay kết nối.
- [SKILL, 64 dòng](https://github.com/ducthangho/tra-luat/blob/ecd8cee3ea6da6513a37a9b9aa6c9db65472e41c/.agents/skills/proxima-control/SKILL.md): đọc toàn bộ lệnh và giới hạn; TargetId/ConfigPath/RepositoryRoot tường minh, help/WhatIf/version semantics, add-on tùy chọn và core/package isolation.
- [Harness, 373 dòng](https://github.com/ducthangho/tra-luat/blob/ecd8cee3ea6da6513a37a9b9aa6c9db65472e41c/.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1): đọc toàn bộ AST node/edge/bool/background checks trước SafeGetValue/import, bảy PM, counterexamples, child/report/cleanup/source-hash evidence. S1/S2/core không đổi trong Packet này.

Người audit tự đánh giá trục **spec**: sản phẩm khớp các yêu cầu r8/r5 còn hiệu lực sau ngoại lệ P3 không? Tự đánh giá trục **standards/security**: guard, import/hash-before-execution, optional isolation, xử lý lỗi và quyền có vấn đề nào khác không? Các gợi ý này không giới hạn finding; điều bị bản tóm tắt bỏ sót vẫn phải nêu nếu phát hiện.

## 2. P3 đã được chủ kho chấp nhận và ghi nợ, chưa vá

[Quyết định miễn đúng H4](https://github.com/ducthangho/tra-luat/pull/1294#issuecomment-6731269220); [Packet nợ #1295](https://github.com/ducthangho/tra-luat/issues/1295). Chỉ WP1285-R7-F01/P3 (`manifest-requires-guard-comment-regex`) được miễn cho exact H4. Comment `# Requires the S2 hash guard` bị chặn nhầm; `#REQUIRES -Version 5.1` dưới tr-TR/az-Latn-AZ lọt PM01 trên cả PS5.1/7. Không chứng minh thực thi mã tùy ý. Ví dụ `#requiresX` của reviewer thực tế bị parser từ chối, không phải comment vô hại; giữ kết quả này để tránh lặp sai lời khai.

Native probe: 12 quan sát, 251 tệp gốc đã kiểm hash; ZIP `bd1f9a882f3b0a91e358fbbaaff3f3ab9b4187ac10fd9cc15d9d030fd27dcf91`. Nợ mở, class history F01 giữ nguyên; việc chấp nhận không đóng nợ, không miễn finding khác hay SHA mới. Các biểu hiện named-block/background lịch sử đã được vá; whole-class chưa được khai “đóng hết” khi requirements remnant còn nợ.

## 3. Bằng chứng máy và giới hạn phải đọc

[Chỉ mục nguồn đầy đủ](evidence-index.json) dẫn đến dữ liệu gốc và receipt độc lập. Đây là kết quả đo/kiểm của máy và các agent, không thay người tự audit mã:

- Linux exact H4: selftest1777/1777, strict184/184, Ruff rc1 với12F821 lịch sử và delta0, admission dùng E rc0, doctrine/ADR/doc-claims/diffcheck0.
- Native PS5.1/7: mỗi bản7normal +12CXparent +26S2normal, tổng90 positive parentcases; Bbaseline7RED mỗi bản, không lỗi setup. Sáu AST negatives và rollback chỉ Background, toàn bộ455sourcefiles/39logs/15phases/nested artifacts đã giữ và kiểm. Dữ liệu fixture cô lập; chưa chứng minh WinRM/gateway thật/activation. S3 children không dùng EP bypass; 14 cờ Bypass bên trong harness S2 cũ không đổi đã được công khai, GPOUndefined, không thay policy bền.
- PRCI42539770394 attempt1:23/23Ubuntu jobs,26/26checks, các mốc run/checkout/workflow-definition/output có nguồn/AUX11. Thực chạy synthetic `[E,H4]`, treeH4; không nói API head thay cho checkout. Core1777/1777; packet-loop1359/1359 và một ca Windows/pwsh-only bị skip, mutant tương ứng không được ghi công. Raw canonical `not_measured` giữ nguyên. Ba admission receipts rc0 nhưng A0discovery NOT_RUN do upstream policy, không phải activation/full discovery PASS.
- Codex4 approve H4 trước push: source M5/K4 có thật. Claude5 `changes_requested`, `fullscope=false`, childrc0 nhưng launcher16/snapshotFAILED; model chỉ Read/Glob/Grep. Dấu hook và cache Python do lệnh diagnostic của root tạo làm thêm4entry, không đổi entry gốc; repo nguồn delta0. Root nhận lỗi. Không sửa/xóa để làm gate xanh, không biến Claude thành approve/cross_approved. Human audit này đọc nguồn GitHub bất biến độc lập, thay tuyến assurance thất bại; không dùng failed run làm assurance, không miễn hay sửa kết quả snapshot cũ.
- WindowsCI/fullWindowsmutantCI không chạy theo chỉ thị chủ kho; focusednative được phép. Không LIVE, không deploy/activate. PostmergeCI chưa chạy vì chưa merge; chưa có `landed`/M8 cuối.

## 4. Base hiện tại và việc land có điều kiện

Admission base lịch sử E=`eefce7fe828a68a13b4b7e3b1e17c1ddb2b6deee`. Master hiện tại D=`4068b3a2a0087db287ea979eccbd372a7a0938d7` thêm đúng16spec markdown GIAM-HOI ngoài Packet, không đổi code/catalog/protocol/workflow đang áp dụng. Hồ sơ phân loại trong evidence-index. H4 không đổi; mergepreview không xung đột, tree dự kiến `f20cb1aa78756ae0a0b818c34e8d90f152b06a2f`. CI cũ không được đổi lời khai thành đã chạy D. Sau khi người audit thực sự approve: dispatcher kiểm lại exacthead/master/rules/fullrefs/solelease/connector/K0-K7, Ready và auto-review, normalmerge đúng head, actualM CI/officialartifact/fullsourceAUX, M8/readback/nhảlease/D1–D4. Chỉ sau đó mới `landed`; Mission1238 và nợ1295/P2/các Packet sau còn mở.

Không dùng human-only K4 để giả thời điểm audit trước push: primary M5 là Codex4 thật; human audit bổ sung assurance được thực hiện và ghi thời điểm thật bây giờ. Quyền merge/land chủ kho đã cấp, không xin lại.

## 5. Người audit ghi kết luận của chính mình

Sau khi tự đọc các nguồn trên, ghi rõ đã đọc spec/diff; nhận xét của bạn cho hai trục spec và standards/security; finding còn lại (hoặc không có finding khác ngoài P3 đã miễn); và verdict của bạn cho H4 `ecd8cee3ea6da6513a37a9b9aa6c9db65472e41c`. Có thể trả blocked/changes_requested nếu thiếu dữ liệu hoặc còn lỗi. Không ký khi chưa đọc. Template [human-verdict-template.json](human-verdict-template.json) chỉ là cấu trúc chờ điền, chưa phải receipt/verdict.

Codex chỉ được ghi bền lời khai thực tế của người audit và readback khớp sau khi nhận được; không tự điền “tôi đã đọc”, verdict approve hay `human_audited=true` thay người. Protocol§8 yêu cầu: người audit “tự đọc spec/diff, ghi evidence audit và verdict bền” neo exactSHA.
