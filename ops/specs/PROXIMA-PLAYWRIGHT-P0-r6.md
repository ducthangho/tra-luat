# wp1239 r6 — Proxima & Playwright (đề xuất, chưa frozen)
> Tài liệu đề xuất để người giữ duyệt. Không cấp lease, không cấp quyền ghi, push, merge, land hay deploy.
> Ref authoritative dự kiến: `ops/specs/PROXIMA-PLAYWRIGHT-P0-r6.md`. Đây là ref control-plane **bên ngoài** worker product. Người giữ/dispatcher công bố ref này trước lease. Spec không được copy vào write_set. Việc chuẩn bị spec không tự tạo quyền ghi vào repo control-plane.
## 1. Định danh
packet_id: wp1239
revision: 6
packet_issue: 1239
mission_issue: 1238
status: proposed
- nguon_cap_viec: Mission #1238. Kế hoạch "Kế hoạch triển khai Proxima và Playwright bổ trợ tra-luat" v1.0, ngày 05/11/2026, UTF-8, LF, sha256 `5c0c1fa6ad465eaf2037031b79e05f3740118dbbe01fc48ce8278f27f6db9ebb`.
- immutable START/H0: commit `ba0126bd20c99669264b788e15da2b6ebcda0fd7`, tree `43ce78d329fd54266ad73baba351044a0feca85c`. Đây là nguồn tiếp tục đã review, không phải integration base để tính diff.
- S_lease: canonical master được dispatcher fetch + ls-remote xác minh ngay trước cấp lease; SHA/tree ghi literal trong lease/assignment trước khi worker chạy, phải chứa lower-bound `12e5b36225005e257026e57903f2e859a870e6f9`. Không bắt worker chạy với base chưa đo.
- Quan hệ base: H mới phải chứa H0 và S_final làm tổ tiên. S_final ban đầu là S_lease; cho phép refresh tối đa một lần theo §15 trước review cuối. Diff/scope nghiệm thu tính S_final..H, không tính các thay đổi canonical kế thừa như code do Packet viết.
## 2. review_class
- **`sensitive`**, mức sàn giữ nguyên cho đúng hai path §3; classifier đã đo trên source không đổi tại canonical 08bcb51fbed359eaeeca41bc3a0559fe308c0aa9. Dispatcher phải đo lại tại S_lease, ghi source OID/hash và chỉ giữ hoặc tăng class; không suy từ path thiếu.
- Không hạ class. Nếu write_set đổi thì phải đo lại, và chỉ được giữ hoặc tăng class.
- Review chính thức là review độc lập của Codex trên exact head SHA/tree của doc candidate. Review advisory, review của Claude/AGY hoặc review spec không thay thế review này.
## 3. write_set (đóng, đúng 2 path, cả hai là tệp mới)
1. `ops/plans/PROXIMA-PLAYWRIGHT-v1.md`
2. `docs/research/2026-11-05-proxima-playwright-p0.md`
- Mọi path khác nằm ngoài phạm vi: spec, `.agents/skills/**`, manifest, tests, config, AGENTS.md, protocol.
- **Budget đề xuất, chưa đo trên diff:** M1 196 dòng + M2 ≤100 dòng = ≤296 additions trên 2 tệp. Mức này nằm trong trần sensitive ≤3 tệp/≤300 additions.
- Nếu diff thực tế vượt budget thì dừng và revise trước review.
## 4. muc_tieu (mỗi mục chiếu đúng 1 path)
**M1 → `ops/plans/PROXIMA-PLAYWRIGHT-v1.md`**
- Lưu kế hoạch nguồn nguyên văn byte. Không thêm header, front-matter hay chú thích.
- sha256 phải bằng hash nguồn §1. Lệch hash thì dừng và báo, không "sửa cho khớp".
**M2 → `docs/research/2026-11-05-proxima-playwright-p0.md`**
- Báo cáo khảo sát trung thực. Chỉ dựa trên tài liệu, mã và quan sát đã có. Không cài, không probe mạng, không inference.
- Nhãn bằng chứng: `da_do` | `da_quan_sat` | `quan_sat_corroboration` | `doc_ma` | `chua_do`.
- Gắn nhãn theo từng datum. Không bắt mọi mệnh đề văn xuôi mang đúng một nhãn cứng.
- Nội dung bắt buộc:
  - (a) Project/repo/protocol theo bằng chứng tại baseline. Đổi tên thread hay tạo thư mục không được coi là tạo Project.
  - (b) Môi trường và VM (§7).
  - (c) Đọc mã proxima-control.
  - (d) Updater upstream.
  - (e) Artifact, provenance, license.
  - (f) D1–D7.
  - (g) Đề xuất tách P1.
  - (h) Bảng chua_do_duoc.
  - (i) Ánh xạ unknown → gói bị chặn.
- Không hứa exact SHA của chính M2.
## 5. Quyết định thiết kế (đã chốt, P0 chỉ ghi nhận)
- **D1.** Playwright dùng CLI trước. MCP chỉ thêm khi có nhu cầu được duyệt. Chưa làm library/adapter Python. Không thêm dependency vào core tra-luat.
- **D2.** Thứ tự: Desktop → ASUS → VM. VM giữ gateway hiện tại.
- **D3.** Khi lỗi: không fallback gateway/model/device, không retry inference, không suy diễn target thay thế.
- **D4.** Healthcheck không gửi prompt. Status/models không chứng minh quota, xác thực hay danh tính model.
- **D5.** Thiếu provenance theo chính sách thì dừng trước activation. Checksum chỉ chứng minh toàn vẹn.
- **D6.** Hai path tùy chọn `.agents/skills/proxima-control` và `.agents/skills/playwright-browser` được giữ độc lập.
  - Bốn tổ hợp phải hoạt động: cả hai có, chỉ Proxima, chỉ Playwright, không có cái nào.
  - Thiếu hay lỗi một skill không ảnh hưởng skill kia hay core.
- **D7.** P0 kết thúc bằng tài liệu trung thực. P0 không cài, không activation, không rollback test, không đổi credentials/profile/endpoint.
## 6. Đề xuất tách P1 (chỉ đề xuất, không lease/packet_id/revision)
- **S1. Đường dẫn/cấu hình:**
  - Bỏ path cố định theo user/máy.
  - Config **mẫu** nằm trong repo. Config **thật** nằm ngoài repo.
- **S2. WhatIf/ShouldProcess:** use/connect, wrapper, hàm con, exported operation, remoting.
- **S3. Version/manifest/docs:** phân biệt version trong repo, module đã cài và runtime gateway thực chạy.
- Mỗi packet ≤6 tệp. Danh sách tệp do dispatcher/người giữ chốt.
## 7. Hiện trạng ghi vào report
**Môi trường/VM** (nhãn theo từng datum)
- Hai quan sát (device f728 và 810) cùng hostname `TRA-LUAT-WIN`, cùng boot time `2026-10-31T08:22:02.5Z` → `quan_sat_corroboration`. Điều này không chứng minh danh tính và chưa chứng minh là cùng một máy.
- Shell tại device 810: PowerShell `5.1.20348.5756`, service Running → `da_quan_sat`.
- Shell tại device f728: PowerShell `7.6.9`, thấy Proxima ở session 0 → `da_quan_sat`.
- Process list tại 810 không đủ positive evidence vì output Format-Table bị trộn. Không khẳng định cả hai shell đều thấy Proxima ở session 0.
- Metadata module 1.0.1 khai báo PS5.1 → `doc_ma`.
- Tại f728, runtime file version `5.5.0`, product version `5.5.0.0` → `da_quan_sat`.
- Service query tại f728 trả Access denied → `da_quan_sat`.
- Script đọc tiếp tại f728 **không đạt completion**. Chỉ probe metadata riêng đã completed.
- Tương thích endpoint PS5.1 → `chua_do`.
- Bundle environment chỉ nhắc device f728, không nhắc 810.
  - Đây là bằng chứng về kết nối dự định, **không** chứng minh xác thực remote.
  - Không tự fallback sang 810 hay device khác (D3).
**proxima-control** (`doc_ma`, chưa test)
- Có lỗi WhatIf ở settings, connect, wrapper và exported operation.
- Nhánh mutation có thể ghi settings, khởi chạy process hoặc đổi service khi dùng `-WhatIf`.
**Updater** (`doc_ma`)
- `electron/main-v2.cjs` @ `0e92241847c40d1c3b26b6785ab43dc8710888aa` có `autoDownload` và `autoInstallOnAppQuit`.
- Hành vi trên máy → `chua_do`.
**ZIP**
- sha256 `6275a551b532b75063bd184895287836cd8acdeba9d696e1a233900e68913748` → `da_do`, chỉ chứng minh toàn vẹn.
- Chữ ký/attestation/provenance → `chua_do`. Activation dừng theo D5.
**License** (`doc_ma`)
- Điều khoản personal/noncommercial. Cần xác nhận phù hợp mục đích trước rollout.
**Kết nối** (`chua_do`)
- Đường Desktop → ASUS → VM qua gateway hiện tại chưa đo bằng mạng ở P0. Bảo vệ gateway mới chỉ đọc tài liệu.
**Advisor findings đang mở**
- Theo dõi riêng, không trình bày như remediation kế thừa.
## 8. chua_do_duoc (owner / điều kiện đóng / hạn)
| # | Hạng mục | Owner | Điều kiện đóng | Hạn |
|---|---|---|---|---|
| U1 | Tương thích endpoint PS5.1 | Executor P1-S2 | Schema/design trước lease. Test cô lập PS5.1 + PS7 có log. | design: trước lease P1-S2; test: trước accept/merge P1-S2 |
| U2 | Danh tính VM (f728/810) | người giữ + Executor P5 | Định danh bằng nguồn tin cậy, không chỉ hostname/boot | trước P3 target VM và trước P5 |
| U3 | Lỗi WhatIf | Executor P1-S2 | Design ShouldProcess trước lease. Test âm tính mutation. | design: trước lease; test: trước accept/merge |
| U4 | Hành vi updater thực tế | Executor P4 | Quan sát trên Desktop thử nghiệm | Design P4 được dự thảo khi còn unknown. Activation chặn trước proof. |
| U5 | Provenance artifact | người giữ | Có attestation hoặc quyết định chính sách ghi rõ | trước mọi activation |
| U6 | License fit | người giữ | Xác nhận bằng văn bản | trước rollout P5 |
| U7 | Retention/soak/cửa sổ theo dõi | Executor P4 | Ghi phương pháp, ngưỡng, owner | trước activation |
| U8 | Restore profile/đăng nhập | Executor P4 | Thử với profile thử, không dùng profile thật | trước activation |
| U9 | Dung lượng/ACL ổ D trên ASUS | Executor P5 | Đo dung lượng trống và ACL | trước đặt `PLAYWRIGHT_BROWSERS_PATH` |
| U10 | Version Playwright CLI ghim | Executor P2 | Lockfile + browser revision đã test | trước merge P2 |
| U11 | Xác thực remote tới f728 | người giữ + Executor P3 | Bằng chứng auth thực, không chỉ bundle environment | trước P3 |
## 9. Unknown chặn gói nào
- **P1-S2:** lease cần design U1/U3. Accept/merge cần test U1/U3. Test hành vi của code chưa viết **không** chặn lease.
- **P2:** U10.
- **P3:** U11. Thêm U2 nếu target là VM. D3 áp dụng.
- **P4:** design không bị chặn. Activation chặn bởi U4, U5, U7, U8.
- **P5:** U2, U5, U6, U9.
- **P0:** không bị chặn. P0 chỉ cần ghi các unknown này trung thực.
## 10. ngoai_pham_vi
- Cài, gỡ, cập nhật Proxima/Playwright/MCP.
- Probe mạng, gọi model, gửi prompt.
- Sửa `.agents/skills/**`, adapter, manifest, tests, updater, config.
- Rollback test, activation, promote sang ASUS/VM.
- Đổi gateway, endpoint, ACL, service account, credentials hoặc profile.
- Cấp lease, push, merge, land, deploy.
- Ghi spec, AGENTS.md, protocol hoặc repo control-plane.
- Mọi công việc P1–P6.
## 11. nghiem_thu
**Kiểm tự động (integrity/paths/base; output lệnh ghi vào PR/packet, không ghi vào M1)**
- **N1.** sha256 của M1 = `5c0c1fa6ad465eaf2037031b79e05f3740118dbbe01fc48ce8278f27f6db9ebb`. M1 không có BOM, không có CRLF.
- **N2.** `git diff --name-only S_final..H` cho **đúng** 2 path ở §3: không thiếu, không thừa. Spec ở ref ngoài, không nằm trong diff.
- **N3.** Kiểm tra base:
  - `git merge-base --is-ancestor S_final H` thành công.
  - Tree của START/H0 = `43ce78d329fd54266ad73baba351044a0feca85c`; tree S_final phải khớp binding literal mới nhất đã ghi trước merge/review. H0 cũng phải là tổ tiên H.
  - Nếu base dịch chuyển: có continuation authorization.
- **N4.** Cả hai tệp tồn tại tại H và không rỗng.
  - Cả hai tệp là UTF-8, chỉ dùng LF, không có BOM.
  - `git diff --check S_final..H` trả rc 0. Ghi output thực tế, kèm số path/dòng đã kiểm (positive check count). Không ghi pass khi chưa chạy.
  - Additions theo `git diff --numstat S_final..H` có tổng ≤296 trên 2 tệp. Reviewer đối chiếu giới hạn ≤296 additions trên output thực.
**Phản chứng integrity**
- Chạy được trong scratch, không trên nhánh:
  - Sửa 1 byte hoặc đổi LF→CRLF trong M1 → N1 FAIL.
  - Thêm path thứ 3 → N2 FAIL.
  - Baseline không phải tổ tiên → N3 FAIL.
  - Tệp rỗng → N4 FAIL.
- Ghi output thực nếu đã chạy. Không khẳng định đã chạy khi chưa chạy.
**MANUAL evidence review (reviewer, không dùng grep giả làm semantic verifier)**
- **R1.** M2 có đủ các mục (a)–(i). Reviewer chỉ ra mục thiếu nếu có.
- **R2.** Nhãn datum ở §7 khớp bằng chứng. Không nâng `quan_sat_corroboration`/`da_quan_sat` thành `da_do`. Không suy ra auth remote từ bundle environment.
- **R3.** Credential: review chỉ tìm credential material cụ thể hoặc canary.
  - Không blanket-grep `secret`/`token`/`profile` trên M1 nguyên văn, vì dễ false positive.
  - Tên trường token/profile không phải secret.
  - Spec không hứa tự động phát hiện mọi secret.
- **R4.** M2 không chứa lệnh cài/activation và không chứa kết quả probe mạng giả định.
**Điều kiện nhận passed**
- Chỉ nhận passed khi có positive evidence cho N1–N4 và R1–R4 trên exact doc candidate (head SHA/tree H).
- Sau đó: Codex review độc lập, rồi người giữ duyệt.
## 12. hinh_dang_ke_thua
- `khong_ap_dung`, vì đây là tính năng mới.
- Advisor findings đang mở được theo dõi riêng, không giả làm inherited remediation.
## 13. dependencies và vòng đời spec
- Mission #1238; packet #1239 (proposed).
- Baseline commit/tree ở §1. Kế hoạch nguồn có hash ở §1.
- AGENTS.md và protocol tại baseline.
- Lease do dispatcher/người giữ cấp.
- Spec chỉ frozen khi đủ các bước sau, theo đúng thứ tự:
  1. Chủ kho duyệt exact spec sha256. Hash tính trên bytes của spec; spec không tự nhúng hash của chính nó.
  2. Controller được cấp quyền có phạm vi để công bố đúng exact bytes đó vào external Git ref/OID/path. Sau khi công bố, phải readback blob và hash khớp sha256 đã duyệt.
  3. Spec frozen.
  4. Dispatcher cấp lease ghi rõ revision/generation, write_set và required gates.
- Việc chủ kho duyệt nội dung không tự cấp quyền publish. Công bố ref cần authorization riêng có phạm vi (ref/path cụ thể).
- Trước đó spec là bản nháp, không có hiệu lực ủy quyền. Khi chưa có spec ref đã readback và lease thì không được thực thi M1/M2.

## 14. Descriptor closure thủ công đề xuất — cần chủ kho duyệt riêng
- r4 kế nhiệm r3 chỉ sau owner duyệt exact hash và policy S ở §15. r3 giữ nguyên tại 645c073fa062bc37abfebdbf0631886cfff1ff42, SHA256 6f79a4bd4724b78dd97ca2d106f59aa6e3392700c89869a3894d15f23330a1da. Giữ r1/r2/r3 nguyên byte. r2 source: 5dfb0e724ff7dc92f9aa54204a6981c5e4715948, SHA256 c8eabf2c900b4416f8c4e289a667a59cf511a0f96fbd80ecde5fc823857d8ee3.
- r1 source: commit 11fb77c07f848b957aa5eb0c4b8d90c972af2c26; SHA256 76bc8cf9ad5e21add3b5b7a23fbed6ac7c2f9bd3c63e04e1aec44e104960c631.
- Lý do: protocol §3.2/§5 đòi closure từ policy canonical nhưng policy và schema chưa tồn tại tại canonical đo được. Không được suy closure bằng write_set chỉ từ file thiếu.
- Đề xuất miễn trừ CHỈ wp1239 revision 4: chủ kho chấp nhận descriptor thủ công trong chính bytes spec này thay nguồn policy chưa có. Không áp dụng packet khác, không thay protocol hoặc bộ kiểm.
- Ngoại lệ hết hiệu lực khi P0 kết thúc hoặc policy canonical xuất hiện, tùy mốc đến trước. Khi policy xuất hiện, pause, đo lại closure/conflict/gates và revision theo protocol trước tiếp tục; không tự giữ descriptor cũ.
- Các giá trị bên dưới là ĐỀ XUẤT của dispatcher, chưa phải quyền ghi trước quyết định chủ kho. Giá trị đổi phải revision/hash mới, không sửa lease để nới scope.
```json
{
  "change_policy_sha": null,
  "effective_write_set": [
    "ops/plans/PROXIMA-PLAYWRIGHT-v1.md",
    "docs/research/2026-11-05-proxima-playwright-p0.md"
  ],
  "effective_review_class": "sensitive",
  "write_set_hash": "df7de52a9da7e047e70bdf23f07b0e79aaac059272bbbfaaa7f6fe1a063372c6",
  "write_set_hash_formula": "sha256 UTF8 of compact JSON sorted NFC+casefold exact paths",
  "required_checks": [
    "doc_integrity_N1_N4_and_manual_R1_R4_on_exact_H_tree",
    "tl_selftest_N_equals_N_before_primary_push_ADR0062",
    "git_diff_check_on_exact_H",
    "canonical_thu_hoi_admission_rc0_and_live_master_S_ancestor_of_H_before_push",
    "independent_Codex_review_exact_H_tree_sensitive_assurance",
    "canonical_ci_definition_at_bound_S_final_record_OID_and_sha256_all_applicable_Linux_required_jobs_on_exact_H",
    "branch_protection_required_checks_readback_before_merge_or_block"
  ],
  "land_obligations": []
}
```
- change_policy_sha null nghĩa policy canonical vắng; không phải một hash đã xác minh hoặc kết quả tự động của closure engine.
- land_obligations rỗng chỉ nghĩa không thêm companion/land file cho worker; toàn bộ nghĩa vụ protocol và approval exact SHA trước merge/land vẫn áp dụng. Lease không cấp merge/land/deploy.
- Tập required_checks dẫn workflow canonical nêu OID/hash ở trên; giữ mọi check bắt buộc bổ sung của branch protection. Không đọc được branch protection thì chặn merge, không đoán không có check.
- Theo chỉ đạo chủ kho: không yêu cầu CI Windows/full mutant Windows CI; test Windows tập trung vẫn được phép. Full selftest bắt buộc trên Linux, đúng H mới, trước primary/update push. Không sửa workflow ngoài scope.
- Budget đã được owner duyệt tại comment6680244818: mỗi run tối đa90 phút; tổng tối đa3 attempts, 3 review rounds và3 Codex review calls; không xin tăng thêm, không reset lịch sử; same_failure_limit 2. Review rounds 3 là giới hạn riêng thấp hơn mặc định packet_loop 10, không gọi là mặc định. Advisory spec calls trước lease không được biến thành review code; giữ lịch sử trong evidence, không xóa bộ đếm đã phát sinh.
- Dispatcher record nguồn chỉ thị chủ kho tại Mission #1238, scope/descriptor/expiry, rồi readback trước cấp lease cho Claude ở session/clone mới; recorder không là Executor, không tự làm Reviewer.
- H0/START bất biến. S_lease và tối đa một S_refresh chỉ được bind theo policy §15. Mỗi giá trị phải là canonical SHA/tree đo được và journal bền trước khi dùng; sau khi bắt đầu Codex review thì không được thay S_final/H.
- Không có quyền push worker product từ phê duyệt spec: trước push vẫn cần các điều kiện review/gate ADR-0060/0062; PR draft, không merge/land/deploy.

## 15. Continuation r4/g3 — checkpoint khi canonical tiến trước lease
- Trigger: r3 đã được duyệt/công bố đúng hash, nhưng master tiến từ12e5b36 tới08bcb51 trước cấp g3. Điều kiện stop của r3 đã kích hoạt; chưa tiêu attempt/call mới. R4 chỉ đổi cách bind integration base, giữ scope/budget/quyền g3 đã duyệt.
- Dispatcher bind S_lease=live canonical master ngay trước lease, xác minh endpoint canonical + fetch + ls-remote + ancestry từ lower-bound12e5b36. Ghi SHA/tree, source policy/classifier/CI definition OID/hash literal vào lease và assignment; worker vẫn START=H0 cố định.
- Chủ kho cho phép g3 dùng artifact H0 đã review làm đầu vào, tự xác minh M1/M2 và merge S_lease được pin. Không cherry-pick/rebase/reset/force push, không merge moving ref chưa bind.
- Cho phép tối đa MỘT refresh canonical trong g3 trước final Codex review nếu master tiến: chỉ descendant S_lease từ cùng endpoint; dispatcher ghi append-only binding S0→S1 + tree/hash/source trước merge, không ghi đè lịch sử lease. Không đổi scope/class/budget/START hoặc cấp thêm model call qua refresh.
- Worker chỉ merge SHA đã bind và sửa metadata/provenance M2 tối thiểu; dữ liệu survey lịch sử giữ nhãn/timestamp, không nhận như số đo mới. M1 nguyên byte; report≤100 dòng, tổng S_final..H≤296 additions.
- Mọi path ngoài hai Markdown phải giống byte/tree entry tại S_final. Các thay đổi inherited canonical không được sửa thủ công. Conflict hoặc path/scope bất ngờ thì stop; không sửa core/CI/config/manifest để làm gate xanh.
- Trước Codex review: đọc lại master; nếu đã dùng refresh mà master vẫn khác S_final thì stop checkpoint, không tiêu call cuối. Khóa S_final/H, chạy selftest Linux N/N, N1–N4, canonical kiem-thu-hoi-github và diff check trên exact H mới trước review.
- N3 có positive S_final→H và H0→H; negative S_final→H0 phải bị từ chối; snapshot/tree hashes đủ. Final Codex session mới, read-only, exact H/tree và S_final; verdict H0 cũ không áp cho H mới.
- Sau review: nếu master khác S_final, stop checkpoint; không đổi H, không tự gọi thêm model hay push SHA chưa review. Guard chỉ thu hẹp race đọc-master/push; CI admission vẫn là cổng bắt buộc, không hứa loại bỏ race.
- G3 giữ lịch sử H0 để update PR1261 fast-forward thông thường (push thêm thứ2 đã được owner checkpoint trong r3). Ghi SHA trước/sau, lý do/admission đỏ, source bindings và checks. Không tạo PR thay thế hoặc force push.
- Còn đúng1 attempt trong trần3, 2 review rounds trong trần3, 1 Codex call trong trần3; đã dùng2/1/2 tương ứng. Không reset/void auth failure. Mọi việc vượt giới hạn phải xin owner, không tự kéo dài.
- Trust đúng C:/Users/admin/tl-work/wp1239-r3-g3-executor đã được owner duyệt; dùng lại clone g3 đã chuẩn bị, không đổi thư mục hay xin quyền trust rộng hơn. Không chạy agent trước khi r4 đã frozen + lease g3 đã readback.
- Fence lease cũ bằng hồ sơ đối xứng trước g3; lease g3≤4 giờ, mỗi run≤90 phút. Quyền publish spec r4/path/ref và renewed manual descriptor revision4 cần owner duyệt checkpoint này; các quyền còn lại giữ quyết định r3, không xin lại.
- Không CI Windows/full mutant Windows CI; focused Windows vẫn được phép; không cài/kích hoạt Proxima/Playwright. Không merge/land/deploy. Branch-protection403 và canonical CI trước merge vẫn là blockers riêng.

## 16. Checkpoint phục hồi r5/g4 — PROPOSED, chưa cấp quyền
Mục này thay mọi giá trị revision/generation/budget hiện hành của r4 ở trên; các mô tả r3/r4/g3 còn lại là lịch sử. Objective, hai authored paths, sensitive, <=296 additions, source plan nguyên byte, START/H0, review độc lập và policy S_final giữ nguyên.
- Lượt g3 015b21ac9dff4090b8143047a350fbd8 kết thúc rc0 nhưng không tích hợp/commit: ba yêu cầu merge không nhận được quyết định dispatcher trong cửa sổ MCP. Chữ ký HMAC, nonce và hash stdout đã xác minh đúng trên ASUS. Không có H mới; H0/tree giữ nguyên. Không void/reset: global attempts_used=3, review_rounds_used=1, Codex_calls_used=2.
- Đề xuất tổng attempts_limit=4, chỉ thêm đúng một attempt cho g4; generation_attempt_limit=1. Review rounds_limit=3 và Codex_calls_limit=3 giữ nguyên (còn một Codex call), không dùng call kiểm tra auth. Cần chủ kho duyệt tăng attempt riêng; chưa duyệt thì dừng.
- Đề xuất công bố exact bytes spec r5 tại ops/specs/PROXIMA-PLAYWRIGHT-P0-r6.md trên ops/proxima-playwright-p0-spec, manual descriptor revision5 chỉ cho packet này khi policy canonical vẫn vắng; fence đối xứng g3 và cấp lease g4 <=4 giờ sau all-ref exclusion/preflight. Nếu policy xuất hiện, dừng để áp policy thật.
- Tái sử dụng đúng clone đã được trust C:/Users/admin/tl-work/wp1239-r3-g3-executor; branch mới agent/wp1239-g4-claude tại H0, scratch/state g4 riêng và ledger liên kết toàn bộ lịch sử. Không trust thư mục khác, không reset state g3. Có 7 untracked skill files được ghi hash khi thu hồi; giữ nguyên và điều tra nguồn. Nếu cần cây sạch, bảo quản chúng bằng di chuyển có manifest/readback ra scratch trước khi chạy, không xóa hay stage chúng. Không tuyên bố worktree hiện tại sạch.
- Claude CLI thực thi; Codex CLI session/context mới review exact H. Dispatcher không viết M2 thay worker. M2.new.md 98 dòng trong scratch là input chưa được áp, không phải candidate hoặc evidence test mới; worker phải tái xác minh/chỉnh nhãn r5/g4.
- Bind live canonical S_lease mới (đã quan sát d26b36f5d2f952c2d952d58517571ffe27c4f826, KHÔNG dùng giá trị quan sát này làm binding tự động). Xác minh endpoint, fetch, ancestry, class, policy và receipt trước lease. Cho một refresh trước review như r4; sau review bắt đầu H/S_final đóng băng. N4 dùng S_final..H đồng nhất N2/N3, không tính canonical inherited changes vào authored budget.
- Trước khi tiêu attempt: chạy probe không gọi model cho permission mailbox (allow/deny/hash mismatch) và thử một yêu cầu qua MCP thực tế có dispatcher trả lời; không sửa/bypass hook. Chỉ chạy khi đọc trạng thái/bằng chứng và quyết định bind exact request đều readback được. Nếu MCP mất kết nối hoặc request hết hạn, worker dừng ngay, không thử lại merge ba lần.
- Run g3 có deadline 10:04:39Z nhưng terminal ghi 10:21:02Z, 6320.895 giây; chưa xác định nguyên nhân, không coi deadline gate đã đạt. Trước g4 cần targeted Windows probe không gọi model kiểm tra launcher absolute wall deadline, thu hồi child và terminal; nếu không đạt thì dừng, mở remediation riêng, không sửa launcher ngoài scope P0. Mỗi model run <=90 phút, lease tuyệt đối vẫn bắt buộc.
- Gate trên H mới: M1 exact hash; N1-N4/negatives; semantic R1-R4; canonical kiem-thu-hoi-github rc0 trên Linux; Linux full selftest N/N; exact-H Codex độc lập; ngoài hai path bằng S_final; H0/S_final là tổ tiên; live master=S_final ngay trước normal fast-forward cập nhật draft PR1261. Quyền cập nhật PR có điều kiện giữ nguyên từ r3; không force, không merge/land/deploy. Không CI Windows/full mutant Windows; focused Windows probe được phép.
- Phê duyệt checkpoint này chỉ có hiệu lực sau exact hash/spec readback và lease g4 mới; g3 hết hạn lúc 2026-11-06T12:23:50Z, không được hồi sinh bằng chỉ thị chung hoặc quyết định Git gửi muộn.

## 17. Provider switch r6/g5 — đề xuất theo chỉ thị mới của chủ kho
Mục này thay provider/generation/budget hiện hành của r5 ở trên; các chi tiết Claude g4 là lịch sử. Hai authored paths, sensitive, nguyên byte M1, <=296 additions, report<=100 dòng, H0, một refresh canonical trước final review và mọi gate khác giữ nguyên.
- Chỉ thị chủ kho: “Nếu agy hoạt động hãy để agy làm executor”. AGY1.5.2 trên ASUS: --version rc0; models rc0 với13 model; --help và help acp rc0. Đây là availability/preflight, không nhận là inference đã thành công.
- Claude g4 run87793cb9f1b549bbba1bad4e8506c515 được dispatcher dừng theo chỉ thị mới; bắt đầu17:20:51Z, terminal da_dung17:21:35Z. Stdout rỗng, không permission request, HEAD/tree giữ H0. Native stop rc125 chưa chứng minh thu hồi cả cây; follow-up CIM đo root PID24140 vắng, không direct child và không process còn sống được tạo trong cửa sổ run lúc17:23:21Z. Không khai lệnh stop rc0; không đụng các phiên Claude khác của user.
- Bổ sung evidence thu hồi: HMAC của run.json sau official stop không còn khớp; giữ nguyên raw bytes, không ký lại/khai terminal signed. Root kiểm tra trực tiếp native process snapshot và Git riêng; không dùng record này làm bằng chứng machine void. ACP initialize protocol1 trả rc0, agent Antigravity ACP Server1.5.2, không session/new hoặc prompt/model call.
- Không void/reset lượt bị hủy theo chỉ thị: global attempts_used=4/4, review_rounds_used=1/3, Codex_calls_used=2/3. Đề xuất chủ kho tăng attempts_limit lên5 CHỈ để cấp một AGY attempt; generation_attempt_limit1. Không tăng Codex calls hoặc review rounds. Chưa được duyệt phần tăng trần thì không gọi model AGY.
- Executor=google_antigravity, execution_surface=antigravity, transport=machine/local, model_family=gemini. Chọn model tường minh gemini-4-argon-high, requested effort high, từ danh sách vừa đo. Không dùng OpenAI-family executor để né cross-family review; không tự đổi model/provider khi lỗi/quota. Chỉ nhận served identity khi runtime thực sự chứng minh; thiếu thì khai KHONG_DO_DUOC và áp đúng assurance, không suy từ requested ID.
- Reviewer vẫn Codex CLI mới/context độc lập, family openai, đúng exact H/tree, còn một call; dispatcher không tự review. Không coi AGY khả dụng là review passed hoặc lease đã cấp.
- Thiết kế transport AGY: ưu tiên ACP stdio chính thức với request_permission được dispatcher xét từng request/hash ở scratch; chỉ chọn allow_once cho hành động chính xác trong scope, từ chối always/bypass. Không --dangerously-skip-permissions; không cài/đổi plugin/MCP/hook/auth/default model/remote target. Chưa xác minh được permission protocol và launcher/tree stop thì không chạy. ACP initialize/help không gọi model; không session/new, tạo project hoặc session/prompt trước quyền thi công.
- Đề xuất external spec path ops/specs/PROXIMA-PLAYWRIGHT-P0-r6.md/ref ops/proxima-playwright-p0-spec, manual descriptor revision6 chỉ packet này nếu canonical policy còn vắng; tạo lease wp1239-r6-g5-agy<=4h, bia mộ hai chiều với g4 và kiểm all-ref exclusion. G4 không được tiếp tục dù lease timestamp cũ chưa hết. Không thêm sổ thu-hoi chưa kích hoạt vào product.
- Workspace tái dùng đúng clone đã kiểm tra C:/Users/admin/tl-work/wp1239-r3-g3-executor, branch agent/wp1239-g5-agy riêng tại H0; AGY không được xác nhận trust mới rộng hơn hoặc đổi trust Claude. Scratch/state g5 mới với ledger liên kết g1-g4; giữ state cũ bất biến và hashes. Nếu AGY đòi trust/quyền mới chưa có thì báo đúng yêu cầu.
- Bind S_lease=live canonical đo ngay trước lease, một refresh như r5, không dùng moving ref chưa bind. AGY tự tái xác minh input, tích hợp pinned canonical và viết M2 tối thiểu (r6/g5/provenance), không áp mù nháp g3, không sửa core/CI/manifest. Mọi path ngoài hai docs phải giống S_final. Có conflict/permission deny thì dừng; không mutation retry.
- Chỉ sau local H mới: Linux canonical admission rc0, Linux full selftest N/N, N1-N4/negatives/R1-R4, Codex independent exact-H, live canonical=S_final và fast-forward H0->H thì dispatcher cập nhật draft PR1261 theo quyền publication cũ. Không Windows CI/full mutant Windows; focused Windows có thể chạy. Không merge/land/deploy.
