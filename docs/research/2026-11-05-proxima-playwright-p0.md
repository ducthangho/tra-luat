# Báo cáo khảo sát P0 — Proxima và Playwright bổ trợ tra-luat

Packet #1239 · Mission #1238 · revision 2 · generation 2 · lease `wp1239-r2-g2-claude`. Executor anthropic_claude / claude_code / machine-local, viết ngày 2026-11-06 (UTC). Đây chỉ là tài liệu: P0 không cài, không kích hoạt, không probe mạng hay gateway, không gọi model, không chạy hay import bundle Proxima, và không giải unknown nào bằng cài đặt.

Nhãn theo từng datum: `da_do` (số đo hoặc băm tái lập được, ghi rõ ai đo) · `da_quan_sat` (một quan sát trực tiếp, chưa tái lập) · `quan_sat_corroboration` (hai quan sát khớp nhau, không chứng minh danh tính) · `doc_ma` (đọc mã hoặc tài liệu, chưa chạy) · `chua_do` (chưa đo).

Nguồn và thời điểm. Executor g2 KHÔNG tự chạy survey. Số liệu môi trường, bundle và upstream lấy từ `evidence.json` do dispatcher cấp ngoài repo (sha256 `5e8de8afe1fab6c3093a83940a5657f57ff61fb2a54cd6599a11e933256f0716`): survey tiếp nối ghi 2026-11-05T15:28:56Z, cập nhật 15:41:30Z; kiểm toàn vẹn đầu vào 15:33:39Z; preflight dispatcher 16:46:42Z; mục upstream và bundle chỉ ghi ngày 2026-11-05, không có giờ. Datum chỉ có ở spec r2 §7 được ghi "(spec §7)". Phép đo của g2 chỉ dùng git cục bộ trên object do controller chuẩn bị (không fetch, không gọi mạng), 2026-11-06T02:08–02:16Z. Báo cáo g1 (sha256 `5f993d828d874f27243ddedd0200184c09aff4558185df4abce18ae6b3a2ef41`) chỉ là tài liệu khảo sát lịch sử; không số đo nào của g1 được nhận là số đo hôm nay.

hint_provenance: bố cục mục và bảng U theo spec r2 §4, §7–§9; g2 tự viết lời văn sau khi đối chiếu evidence và tự đo lại; không áp patch, không chép nguyên product g1; chỗ kết luận trùng g1 (vd U12) do g2 tái dẫn xuất từ evidence và chỉ thị lượt chạy.

## (a) Project, repo, protocol tại baseline
- Repo github.com/ducthangho/tra-luat; baseline commit `fe84620f897913c7f6c2ce5a0c7316a49655e82f`, tree `9c5534209694e0a7d71cca91b874c053762106f1`; HEAD và tree của checkout khớp lúc 02:08Z → `da_do` (g2).
- AGENTS.md (blob `5fea56ea9d14c2922d8771e7fc5bd69d728a000e`) và `docs/PROTOCOL_DA_PHIEN.md` (blob `342ea958a2036c54422b16354f3e8ccf4f1269b2`) có tại baseline → `da_do` (g2).
- Spec: commit `5dfb0e724ff7dc92f9aa54204a6981c5e4715948`, path ops/specs/PROXIMA-PLAYWRIGHT-P0-r2.md (ngoài product tree), sha256 blob `c8eabf2c900b4416f8c4e289a667a59cf511a0f96fbd80ecde5fc823857d8ee3` khớp `spec_hash` của lease → `da_do` (g2, object cục bộ). Việc ref ops/proxima-playwright-p0-spec trỏ commit ấy: g2 không đọc lại từ remote → `chua_do` với g2.
- Lease `wp1239-r2-g2-claude`: commit `167e9d22a3d6e1d4518bd2837891d367fccb853b` (ref ops/wp1239-r2-g2-lease), blob sha256 `8b81e47041611a1726a4791ca171b309dc3403f696f1e121b7685717350723cf`, hạn 2026-11-06T05:56:59Z, prompt sha256 `7a17740bd500db48d31a1a97f8aa3fa992b644f6421d2fc86faa481a22cc9fa5`; cùng commit, lease g1 mang `da_bi_thay_the: wp1239-r2-g2-claude` → `da_do` (g2). Xung đột write set đo lúc cấp (01:56:59Z): 0 người giữ → `da_do` (dispatcher, ghi trong lease). Comment công bố https://github.com/ducthangho/tra-luat/issues/1239#issuecomment-6674902602 : dispatcher khai đã kiểm, g2 không đọc lại.
- Class `sensitive`: g2 chạy lại `ops/lease_publish.py` (hàm `_tinh_lop_tu_write_set`) tại baseline cho 2 path, từng path riêng cũng ra `sensitive`; `write_set_hash` tính lại theo công thức của descriptor = `df7de52a9da7e047e70bdf23f07b0e79aaac059272bbbfaaa7f6fe1a063372c6` → `da_do` (g2).
- Policy change-impact (.github/coordination/change-impact.v1.json và schema) vắng tại baseline và tại `51d6509e918b8b5403248b52727e53358a23a3a0` (ref origin/master cục bộ, fetch lúc 01:59:29Z, không phải đọc live) → `da_do` (g2); dispatcher đo vắng tại `4fb3c034d0456a600634f501b8f20bd1487e3b83` lúc 16:46Z. Vì vậy closure dùng descriptor thủ công trong spec, chủ kho duyệt CHỈ cho wp1239 revision 2: https://github.com/ducthangho/tra-luat/issues/1238#issuecomment-6663938704
- `.github/workflows/ci.yml` tại `4fb3c034…` có sha256 `aed785d6f1911f390fe1190d5caa575de58a5531252afc6f83981ca19681be67`, khớp required_checks của lease → `da_do` (g2). Branch protection: dispatcher đọc ra HTTP 403 lúc 16:46Z → `chua_do`; theo required_checks, merge bị chặn tới khi đọc được.
- Tại baseline `.agents/skills/` chỉ có cross-review, land-packets, work-packet; proxima-control và playwright-browser chưa có → `da_do` (g2).
- Project "Proxima & Playwright — tra-luat": không có bằng chứng đã tạo hay đã xác minh → `chua_do`. Đổi tên thread, đặt tên chat/nhánh hay tạo thư mục KHÔNG được tính là tạo Project.
- Đường dẫn repo `D:\Quốc hội\tra-luat` ở §2 kế hoạch: CONTEXT.md tại baseline (blob `c201c97045125cb9dbd00e1b59259984fc72d12f`) khai canonical ở đúng đường dẫn ấy nhưng không nêu máy → `doc_ma`; việc repo đó nằm trên ASUS → `chua_do`.
- Kế hoạch trong Git (ops/plans/PROXIMA-PLAYWRIGHT-v1.md) chép nguyên byte từ artifact dispatcher: 9990 byte, 196 dòng LF, 0 CR, không BOM, sha256 `5c0c1fa6ad465eaf2037031b79e05f3740118dbbe01fc48ce8278f27f6db9ebb` = hash nguồn ở spec §1 → `da_do` (g2). Nguồn bền: https://github.com/ducthangho/tra-luat/issues/1238#issuecomment-6662301825 ; g2 không đọc lại comment.

## (b) Môi trường và VM
- Kết nối device f728 và device 810 cùng hostname TRA-LUAT-WIN, cùng boot time 2026-10-31T08:22:02.5Z → `quan_sat_corroboration`. Không chứng minh danh tính, chưa chứng minh là cùng một máy (U2).
- 810: PowerShell 5.1.20348.5756, service Running → `da_quan_sat`. Probe module tại 810 thất bại (Import-PowerShellDataFile unavailable) → `da_quan_sat`; nguyên nhân `chua_do`.
- 810: process list bị trộn output Format-Table nên KHÔNG đủ positive evidence (spec §7); không khẳng định cả hai shell đều thấy Proxima ở session 0.
- f728: PowerShell 7.6.9, thấy Proxima ở session 0 → `da_quan_sat`. Service query qua CIM trả Access denied → `da_quan_sat`.
- f728: script đọc tiếp KHÔNG đạt completion (spec §7); chỉ probe metadata riêng đã completed (`metadata_read_completed: true`).
- Module đã cài tại f728: metadata version 1.0.1, khai báo PowerShell 5.1 → `doc_ma`; sha256 manifest `3f2ac59e201128f03d047da69698567b75675917687d75e8312fd7e34f14ee77` do survey ghi, g2 không đo lại → `da_quan_sat`.
- Runtime tại f728: file version 5.5.0, product version 5.5.0.0 → `da_quan_sat`. Chưa có bằng chứng binary này build từ commit upstream đọc ở (d) (U12).
- Tương thích endpoint PowerShell 5.1 → `chua_do` (U1).
- Bundle environment chỉ nhắc f728, không nhắc 810 (spec §7) → `doc_ma`. Đó là kết nối DỰ ĐỊNH, không chứng minh xác thực remote (U11). Không tự fallback sang 810 hay máy khác (D3).
- Desktop, ASUS, WSL: evidence không có số đo tài nguyên, PowerShell hay ổ đĩa → `chua_do`.
- Kết nối Desktop → ASUS → VM qua gateway hiện tại chưa đo bằng mạng trong P0 → `chua_do`; bảo vệ gateway mới chỉ đọc tài liệu.

## (c) Đọc mã proxima-control (`doc_ma`, chưa test)
- Nguồn: mục `bundle_audit` của evidence — survey Claude ngày 2026-11-05 và đọc mã độc lập của Codex, không phải test hành vi; g2 không mở, chạy hay import bundle. Tệp được định vị: proxima-control/scripts/ProximaControl.psm1, Run-Px.ps1, ProximaControl.psd1.
- `use` lưu config mà không qua ShouldProcess; `connect` tạo session và lưu config mà không qua ShouldProcess.
- Wrapper Run-Px gọi connect TRƯỚC khi chuyển operation.WhatIf xuống.
- Hàm export Invoke-ProximaOperation không khai SupportsShouldProcess.
- `status` đi vòng helper HTTP chung, tự gắn header Authorization kiểu Bearer.
- Hệ quả (spec §7): dùng -WhatIf mà nhánh mutation vẫn có thể ghi settings, khởi chạy process hoặc đổi service (U3).
- Đường dẫn cố định theo user/máy: kế hoạch đòi bỏ nhưng evidence không chỉ ra vị trí → `chua_do`; P1-S1 phải tự định vị.
- Advisor findings đang mở được theo dõi riêng, không trình bày như remediation kế thừa (spec §12: `khong_ap_dung`).

## (d) Updater upstream (`doc_ma`)
- Nguồn: https://github.com/Zen4-bit/Proxima/blob/0e92241847c40d1c3b26b6785ab43dc8710888aa/electron/main-v2.cjs (theo evidence; g2 không mở lại). Dòng 16–17 đặt autoDownload = true và autoInstallOnAppQuit = true; kiểm cập nhật 5 giây sau khởi động; thao tác thủ công updater-install gọi quitAndInstall.
- Đây là đọc mã nguồn tại một commit, không chứng minh binary đã cài chạy đúng mã ấy. Hành vi thực tế trên máy → `chua_do` (U4, U12).
- Trước mọi activation phải có bằng chứng KIỂM SOÁT được updater (tắt hoặc ghim) trên Desktop thử nghiệm, thuộc P4; thiếu thì dừng (D5). P0 không thử.

## (e) Artifact, provenance, license
- ZIP bundle sha256 `6275a551b532b75063bd184895287836cd8acdeba9d696e1a233900e68913748` (survey 2026-11-05; g2 không mở lại ZIP) → `da_do`, chỉ chứng minh toàn vẹn.
- Chữ ký, attestation, provenance → `chua_do` (U5); activation dừng theo D5.
- License tại cùng commit upstream: personal/non-commercial, không cho triển khai doanh nghiệp/tổ chức → `doc_ma`. Mức phù hợp với mục đích dùng chờ chủ kho xác nhận bằng văn bản (U6).
- Ứng viên phiên bản trong evidence, chưa kiểm, chưa ghim, không kèm URL hay thời điểm: Proxima v5.5.0, Playwright v1.64.1, MCP v0.0.84, CLI v0.1.23 → ghim là `chua_do` (U10).

## (f) Quyết định D1–D7 (đã chốt ở spec §5, P0 chỉ ghi nhận)
- D1: Playwright dùng CLI trước; MCP chỉ thêm khi có nhu cầu được duyệt; chưa làm library/adapter Python; không thêm dependency vào core tra-luat.
- D2: thứ tự Desktop → ASUS → VM; VM giữ vai trò gateway hiện tại.
- D3: khi lỗi không fallback gateway/model/device, không retry inference, không suy diễn target thay thế; mọi thao tác đổi trạng thái nêu target tường minh.
- D4: healthcheck không gửi prompt; status/models không chứng minh quota, xác thực hay danh tính model.
- D5: thiếu provenance theo chính sách thì dừng trước activation; checksum chỉ chứng minh toàn vẹn.
- D6: hai skill tùy chọn .agents/skills/proxima-control và .agents/skills/playwright-browser trong repo, độc lập; bốn tổ hợp (cả hai, chỉ Proxima, chỉ Playwright, không cái nào) đều phải chạy; thiếu hay lỗi một skill không ảnh hưởng skill kia hay core.
- D7: P0 kết thúc bằng tài liệu trung thực; không cài, không activation, không rollback test, không đổi credentials/profile/endpoint.
- Hệ quả về dữ liệu (kế hoạch §5): profile đăng nhập, config thật, cache, staging và log nằm ngoài repo; repo chỉ giữ config MẪU.

## (g) Đề xuất tách P1 (chưa gán ID, lease hay revision; P0 không mở P1)
- S1 Đường dẫn/cấu hình: bỏ path cố định theo user/máy; seam đề xuất là đường dẫn config truyền tường minh (tham số hoặc biến môi trường, không tự dò sang máy/tài khoản khác); config thật ngoài repo theo từng máy, config mẫu trong repo.
- S2 WhatIf/ShouldProcess: use/connect, wrapper, hàm con, operation export, remoting; test âm tính mutation trên PowerShell 5.1 và 7 (U1, U3).
- S3 Version/manifest/docs: tách version trong repo, module đã cài và runtime gateway thực chạy.
- Mỗi S là một packet riêng; danh sách tệp do dispatcher/người giữ chốt; spec r2 đề xuất ≤6 tệp mỗi packet.
- Trần theo ADR, phải đo lại lúc cấp lease: path dự kiến dưới .agents/skills/ đo tại baseline ra `sensitive` (g2, tiền tố `planned:` qua cùng hàm) ⇒ ≤3 tệp và ≤300 dòng thêm (`docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md`); ≤6 tệp và ≤450 dòng thêm chỉ khi spec P1 mang đúng một dòng khai hợp lệ theo `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md`. Packet thường: ≤6 tệp và ≤1.000 dòng thêm cộng xoá. Spec r2 không có dòng khai ấy (g2 đếm 0).

## (h) chua_do_duoc
| # | Hạng mục | Owner | Điều kiện đóng | Hạn |
|---|---|---|---|---|
| U1 | Tương thích endpoint PowerShell 5.1 | Executor P1-S2 | Design schema trước lease; test cô lập PS5.1 + PS7 có log | design: trước lease P1-S2; test: trước accept/merge P1-S2 |
| U2 | Danh tính VM (f728/810) | người giữ + Executor P5 | Định danh bằng nguồn tin cậy, không chỉ hostname/boot | trước P3 nhắm VM và trước P5 |
| U3 | Lỗi WhatIf | Executor P1-S2 | Design ShouldProcess trước lease; test âm tính mutation | design: trước lease; test: trước accept/merge |
| U4 | Hành vi updater thực tế | Executor P4 | Quan sát trên Desktop thử nghiệm, chứng minh kiểm soát được | design P4 được dự thảo khi còn unknown; activation chặn tới khi có proof |
| U5 | Chữ ký/attestation/provenance artifact | người giữ | Có attestation hoặc quyết định chính sách ghi rõ | trước mọi activation |
| U6 | License fit | người giữ | Xác nhận bằng văn bản | trước rollout P5 |
| U7 | Retention, soak, cửa sổ theo dõi | Executor P4 | Ghi phương pháp, ngưỡng, owner | trước activation |
| U8 | Restore profile/đăng nhập | Executor P4 | Thử với profile thử, không dùng profile thật | trước activation |
| U9 | Cache: dung lượng/ACL ổ D trên ASUS | Executor P5 | Đo dung lượng trống và ACL | trước khi đặt PLAYWRIGHT_BROWSERS_PATH |
| U10 | Version Playwright CLI ghim | Executor P2 | Lockfile + browser revision đã test | trước merge P2 |
| U11 | Xác thực remote tới f728 | người giữ + Executor P3 | Bằng chứng auth thực, không chỉ bundle environment | trước P3 |
| U12 | Binary 5.5.0 khớp mã upstream đã đọc (g2 bổ sung ngoài bảng §8 spec) | người giữ + Executor P4 | Provenance nối artifact với commit, hoặc quyết định chính sách ghi rõ | trước activation P4 |

## (i) Unknown chặn gói nào
- P0: không bị chặn; chỉ cần ghi các unknown trung thực, không giải bằng cài đặt hay probe.
- P1-S2: lease cần design U1/U3; accept/merge cần test U1/U3. Test hành vi của code chưa viết KHÔNG chặn lease. P1-S1 và P1-S3: bảng không gán unknown chặn.
- P2: U10.
- P3: U11; thêm U2 nếu target là VM; D3 áp dụng.
- P4: design không bị chặn; activation bị chặn bởi U4, U5, U7, U8 và U12 (g2 bổ sung).
- P5: U2, U5, U6, U9.
