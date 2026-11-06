# wp1239 r3 — Proxima & Playwright (đề xuất, chưa frozen)
> Tài liệu đề xuất để người giữ duyệt. Không cấp lease, không cấp quyền ghi, push, merge, land hay deploy.
> Ref authoritative dự kiến: `ops/specs/PROXIMA-PLAYWRIGHT-P0-r3.md`. Đây là ref control-plane **bên ngoài** worker product. Người giữ/dispatcher công bố ref này trước lease. Spec không được copy vào write_set. Việc chuẩn bị spec không tự tạo quyền ghi vào repo control-plane.
## 1. Định danh
packet_id: wp1239
revision: 3
packet_issue: 1239
mission_issue: 1238
status: proposed
- nguon_cap_viec: Mission #1238. Kế hoạch "Kế hoạch triển khai Proxima và Playwright bổ trợ tra-luat" v1.0, ngày 05/11/2026, UTF-8, LF, sha256 `5c0c1fa6ad465eaf2037031b79e05f3740118dbbe01fc48ce8278f27f6db9ebb`.
- baseline (immutable): commit `12e5b36225005e257026e57903f2e859a870e6f9`, tree `6bac5b200e636e92f14ff197970965a25f60e118`.
- Quan hệ base: execution/integration baseline S là OID ở trên; H mới phải chứa S và H0=ba0126bd20c99669264b788e15da2b6ebcda0fd7 làm tổ tiên. Continuation g3 bắt đầu từ H0 đã review, được chủ kho cho phép tái dùng artifact rõ ràng, rồi merge chính S; không tự cherry-pick/rebase/reset. Diff nghiệm thu tính S..H.
## 2. review_class
- **`sensitive`**, đã đo bằng `ops/lease_publish.py::_tinh_lop_tu_write_set` tại baseline `12e5b36225005e257026e57903f2e859a870e6f9`. Kết quả là `sensitive` cho đúng 2 path ở §3.
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
- **N2.** `git diff --name-only 12e5b36225005e257026e57903f2e859a870e6f9..H` cho **đúng** 2 path ở §3: không thiếu, không thừa. Spec ở ref ngoài, không nằm trong diff.
- **N3.** Kiểm tra base:
  - `git merge-base --is-ancestor 12e5b36225005e257026e57903f2e859a870e6f9 H` thành công.
  - Tree của baseline = `6bac5b200e636e92f14ff197970965a25f60e118`.
  - Nếu base dịch chuyển: có continuation authorization.
- **N4.** Cả hai tệp tồn tại tại H và không rỗng.
  - Cả hai tệp là UTF-8, chỉ dùng LF, không có BOM.
  - `git diff --check 12e5b36225005e257026e57903f2e859a870e6f9..H` trả rc 0. Ghi output thực tế, kèm số path/dòng đã kiểm (positive check count). Không ghi pass khi chưa chạy.
  - Additions theo `git diff --numstat 12e5b36225005e257026e57903f2e859a870e6f9..H` có tổng ≤296 trên 2 tệp. Reviewer đối chiếu giới hạn ≤296 additions trên output thực.
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
- r3 thay r2 chỉ sau quyết định chủ kho cho exact hash r3; hiện proposed. Giữ r1/r2 nguyên byte. r2 source: 5dfb0e724ff7dc92f9aa54204a6981c5e4715948, SHA256 c8eabf2c900b4416f8c4e289a667a59cf511a0f96fbd80ecde5fc823857d8ee3.
- r1 source: commit 11fb77c07f848b957aa5eb0c4b8d90c972af2c26; SHA256 76bc8cf9ad5e21add3b5b7a23fbed6ac7c2f9bd3c63e04e1aec44e104960c631.
- Lý do: protocol §3.2/§5 đòi closure từ policy canonical nhưng policy và schema chưa tồn tại tại canonical đo được. Không được suy closure bằng write_set chỉ từ file thiếu.
- Đề xuất miễn trừ CHỈ wp1239 revision 3: chủ kho chấp nhận descriptor thủ công trong chính bytes spec này thay nguồn policy chưa có. Không áp dụng packet khác, không thay protocol hoặc bộ kiểm.
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
    "canonical_ci_yml_at_12e5b36225005e257026e57903f2e859a870e6f9_sha256_aed785d6f1911f390fe1190d5caa575de58a5531252afc6f83981ca19681be67_all_applicable_Linux_required_jobs_on_exact_H",
    "branch_protection_required_checks_readback_before_merge_or_block"
  ],
  "land_obligations": []
}
```
- change_policy_sha null nghĩa policy canonical vắng; không phải một hash đã xác minh hoặc kết quả tự động của closure engine.
- land_obligations rỗng chỉ nghĩa không thêm companion/land file cho worker; toàn bộ nghĩa vụ protocol và approval exact SHA trước merge/land vẫn áp dụng. Lease không cấp merge/land/deploy.
- Tập required_checks dẫn workflow canonical nêu OID/hash ở trên; giữ mọi check bắt buộc bổ sung của branch protection. Không đọc được branch protection thì chặn merge, không đoán không có check.
- Theo chỉ đạo chủ kho: không yêu cầu CI Windows/full mutant Windows CI; test Windows tập trung vẫn được phép. Full selftest bắt buộc trên Linux, đúng H mới, trước primary/update push. Không sửa workflow ngoài scope.
- Budget đề xuất: mỗi run tối đa 90 phút; tối đa 3 attempts, 3 review rounds và 3 Codex review calls (đề nghị tăng tổng trần 2→3, không reset lịch sử); same_failure_limit 2. Review rounds 3 là giới hạn riêng thấp hơn mặc định packet_loop 10, không gọi là mặc định. Advisory spec calls trước lease không được biến thành review code; giữ lịch sử trong evidence, không xóa bộ đếm đã phát sinh.
- Dispatcher record nguồn chỉ thị chủ kho tại Mission #1238, scope/descriptor/expiry, rồi readback trước cấp lease cho Claude ở session/clone mới; recorder không là Executor, không tự làm Reviewer.
- r3 đóng băng baseline S=12e5b36225005e257026e57903f2e859a870e6f9; baseline r2 fe84620f897913c7f6c2ce5a0c7316a49655e82f vẫn giữ trong hồ sơ lịch sử. Continuation g3 được đề xuất là H0=ba0126bd20c99669264b788e15da2b6ebcda0fd7; cần owner approve r3/g3 rõ ràng. Không đổi S trong một run.
- Không có quyền push worker product từ phê duyệt spec: trước push vẫn cần các điều kiện review/gate ADR-0060/0062; PR draft, không merge/land/deploy.

## 15. Continuation r3/g3 để sửa admission trên PR #1261
- Trigger đo được: thu-hoi run42174613023 rc12 vì S hiện hành không là ancestor H0. Không tắt, sửa hay miễn cổng này.
- H0 đã cross_approved chỉ là nguồn tham khảo; verdict cũ KHÔNG áp cho H mới. Git history H0 được giữ bằng merge tiến, không force push.
- G3 fresh Claude session/clone: preflight đúng START=H0, S tồn tại/hash đúng; merge canonical S được pin, không thay bằng nhánh moving master. Nếu có conflict hoặc scope bất ngờ thì dừng.
- Các thay đổi inherited từ S phải trùng byte với S. Sau merge/commit, mọi path ngoài hai Markdown ở §3 phải trùng S; tuyệt đối không sửa core/CI/manifest/config để chữa admission.
- M1 vẫn nguyên byte nguồn. M2 sửa tối thiểu metadata r3/g3/base/lease và provenance integration; dữ liệu lịch sử vẫn gắn nhãn/timestamp cũ, không nhận thành phép đo mới. Giữ ≤100 dòng và tổng S..H ≤296 additions.
- N3 thêm: S và H0 đều là ancestor H; baseline tree S đúng; phản chứng S→H0 phải bị từ chối (rc1). Chạy canonical kiem-thu-hoi-github tại chỗ với S/H mới đạt rc0 trước review và trước push.
- Trước review/push đọc lại canonical master. Nếu master khác S, dừng checkpoint, không đổi H sau review hoặc tự tiêu thêm lượt model.
- Tạo H mới với H0 là ancestor để update PR #1261 bằng fast-forward thông thường. Không amend/rebase/reset/force push, không đóng/mở PR thay thế.
- Checkpoint owner cần: revision3 exact bytes + publish refs/heads/ops/proxima-playwright-p0-spec/path r3; generation3 lease cho Claude; phép tiếp tục từ H0/mergeS; tổng Codex calls2→3; update push thứ2 trên PR sau gates/review đạt; trust đúng clone g3 đã kiểm.
- Toàn Packet đã dùng attempts2/3, review rounds1/3, Codex calls2/2 (gồm một auth failure trước model). Sau tăng trần còn đúng 1 attempt, 2 review rounds, 1 Codex call. Không reset hoặc bỏ auth failure; mọi lượt ngoài trần phải checkpoint.
- Fence các lease g2 hoàn tất/hết hạn bằng hồ sơ đối xứng trước lease g3; reader lease đang còn hạn không được giao chồng lên worker mới. g3 tối đa4 giờ, mỗi run≤90 phút; Codex review fresh read-only trên exact H mới.
- Sau approve offline + Linux selftest N/N + N1–N4/admission/diff check trên H mới, dispatcher update remote head PR1261 bằng fast-forward, tự động CI Linux. Mọi push thêm vẫn cần checkpoint ADR0060/0062.
- Chưa có merge/land/deploy authority; branch-protection readback403 vẫn chặn merge tới khi đọc được. P1–P6 chưa mở trong r3.
