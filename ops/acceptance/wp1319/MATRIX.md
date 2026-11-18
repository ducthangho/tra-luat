# WP1319 — Ma trận nghiệm thu bổ sung Mission #1238 (khung, 2026-11-17)

Trạng thái: **khung — chưa có raw 13/11**. Lượt native r1 trên Desktop đã đóng băng (zip `54506f18…`); review độc lập trả **request_changes** (`r1/VERDICT-claude-xhigh.md`). Không hàng nào được nâng lên `passed` nhờ r1. Mọi hàng dưới đây chỉ dựa trên bản chiếu công khai.
Không hàng nào là audit raw PASS, human audit hay product review mới.

## Neo
- master đọc: `13bf69f6eb797e859619a2062e7c9577e6a9cc0b` (tree `a4cb90571c5432ad97d62fd7409b45147acf6c2a`).
- Nguồn add-on trên master trùng blob với merge P2 `b0b5480807dd70a367a306c158cc1df08b70fc25`:
  `.agents/skills/proxima-control/SKILL.md` `88f0376e…` · `.agents/skills/playwright-browser/SKILL.md` `678ba2f0…` ·
  `.agents/skills/playwright-browser/package-lock.json` `8b234cfa…`.
- Tiêu chí: `ops/plans/PROXIMA-PLAYWRIGHT-v1.md` §11 (blob `9800531f…`); U1–U12: `docs/research/2026-11-05-proxima-playwright-p0.md` (blob `087aff05…`).
- Bản chiếu công khai: M8 P2 [#1287 c6815845097](https://github.com/ducthangho/tra-luat/issues/1287#issuecomment-6815845097) ·
  P3 [c6843286540](https://github.com/ducthangho/tra-luat/issues/1297#issuecomment-6843286540) ·
  P4 [c6843288240](https://github.com/ducthangho/tra-luat/issues/1298#issuecomment-6843288240) ·
  P5 [c6843291545](https://github.com/ducthangho/tra-luat/issues/1299#issuecomment-6843291545) ·
  P6 [c6843293734](https://github.com/ducthangho/tra-luat/issues/1300#issuecomment-6843293734) ·
  closeout [#1238 c6843361361](https://github.com/ducthangho/tra-luat/issues/1238#issuecomment-6843361361).
- Gói raw cuối 13/11: **chưa có**. Xem phần Blocker.

## Loại bằng chứng (cột `loai`)
`direct_raw` — phiên này tự đọc và kiểm hash bản gốc ·
`ci_artifact` — artifact CI có digest GitHub ·
`carry_forward` — kế thừa tương đương byte theo quyết định owner ·
`fixture` — controlled fixture, không phải hành vi thật ·
`public_projection_only` — chỉ có lời khai trong comment công khai ·
`direct_live_17_11` — phiên này đo trực tiếp ngày 17/11 (chỉ đọc) · `direct_native_desktop_r1` — lượt native r1 trên Desktop (17–18/11), zip `54506f18…`, xem `r1/RESULTS.md` và `r1/VERDICT-claude-xhigh.md` · `cho_review` — có raw trực tiếp nhưng chưa có verdict approve ·
`not_run` / `not_measured`.

Cột `ket_luan`: `passed` · `failed` · `skipped` · `not_run` · `cho_raw` (đã có lời khai PASS nhưng chưa đối chiếu raw) · `gioi_han` (ngoài phạm vi, đã khai là giới hạn).

## A. §11 — 12 tiêu chí

| # | Tiêu chí | Lời khai công khai (nguồn) | loai | ket_luan | Còn thiếu để nghiệm thu |
|---|---|---|---|---|---|
| 1 | Bốn lựa chọn cài hoạt động; thiếu add-on không phá core | P2 M8: `lifecycle_reuse`, `Linux_literal_flow` passed; P5: VM PS5.1/PS7 4 bước browser, status/WhatIf 4/4. **[r1](r1/RESULTS.md) Desktop 18/11: O0/O1/O2/O3 selftest 1777/1777 ×4; proxima harness O1+O3; playwright O2** | ci_artifact (P2) + public_projection_only (P5) + **direct_native_desktop_r1** | **cho_review** (Desktop) | Ma trận 4 lựa chọn (không cài / chỉ Proxima / chỉ Playwright / cả hai) × host × PS5.1/PS7 với rc, marker từng ca. Chưa thấy bằng chứng tách riêng cả 4 lựa chọn ở mức host |
| 2 | Đúng target; không fallback/retry inference | P3: "actual authorized DC target execution and 4 status/WhatIf". **[r1](r1/RESULTS.md): từ chối thiếu/sai TargetId (`ArgumentMissing`, `TargetMismatch`) PS5.1+PS7** | public_projection_only + **direct_native_desktop_r1** (cấu hình mẫu) | cho_raw (gateway thật) · **cho_review** (chốt target) | Raw log target, bằng chứng 0 lần retry/fallback |
| 3 | WhatIf không mutation ngoài artifact dry-run | P3/P5: status/WhatIf 4/4; P1-S2 (U1/U3). **[r1](r1/RESULTS.md): status/restart/stop -WhatIf rc0, snapshot trước=sau, PS5.1+PS7** | public_projection_only + **direct_native_desktop_r1** (cấu hình mẫu, backend không thật) | **cho_review** | Snapshot trước/sau của WhatIf, PS5.1 + PS7 |
| 4 | Không secrets/profile trong repo và báo cáo | Closeout: "no profile contents or credentials published" | public_projection_only | cho_raw | Quét secrets trên chính gói raw trước khi đóng băng |
| 5 | Profile riêng; package/browser/cache nhất quán | P4: 251 dependency/exe/installer exact pins; P2 lockfile. **[r1](r1/RESULTS.md): PIN OK Windows (cli 0.1.23, Chromium 1252) với O2; phần O3 not_run; lời khai chữ ký/attestation npm KHÔNG có raw; F1 dư lượng `ms-playwright\daemon` ngoài TL_PW_ROOT; N6 failed** | ci_artifact + public_projection_only + **direct_native_desktop_r1** | **cho_review**, kèm finding F1 | Manifest pin + cache path theo máy; U9 ASUS |
| 6 | Artifact sai nguồn/hỏng không được kích hoạt | P4 coverage: artifact/download/cache/metadata → fault-injection | public_projection_only + fixture | cho_raw | Tách ca native thật và ca fixture; raw FAIL induced phải giữ nguyên |
| 7 | Máy bận hoãn, updater trùng bị khóa | P4: busy/dual lock; VM `wp1298-operator-unit-20261112/verified-result.json` (helper-only) | public_projection_only + fixture | cho_raw | Ca native trên host đích; receipt VM tự nói không thay ASUS activation |
| 8 | Desktop lỗi chặn ASUS/VM (promotion fence) | P5: "ASUS passed before VM canary" | public_projection_only | cho_raw | Owner đã đổi Desktop→ASUS làm máy đầu; cần raw chứng minh fence chặn khi máy đầu FAIL, không chỉ thứ tự đã chạy |
| 9 | Phục hồi binary và dữ liệu được kiểm thử | P4: 7957 matching files restored; 1 fault/1 restore/1 baseline restart | public_projection_only | cho_raw | Xem U8: chưa thấy bằng chứng phiên/đăng nhập được giữ |
| 10 | File khóa, đĩa đầy, rollback thất bại | P4 coverage: filelock/reserve/partialcopy/rollbackfailure | public_projection_only + fixture | cho_raw | Tách realOS / inert-consumer / fault-injection theo từng ca |
| 11 | Healthcheck không inference | P3/P5 status; closeout: "No upstream model identity/quota inferred from status" | public_projection_only | cho_raw | Raw request log chứng minh 0 inference |
| 12 | Review độc lập đúng head/tree + evidence | P2: full_H4 + delta_H6 approve (Claude), connector clean; P3–P6: reduced evidence-consistency review | ci_artifact (P2) + public_projection_only (P3–P6) | P2: passed (nguồn) · P3–P6: gioi_han | Review P3–P6 tự khai *không* phải raw/human audit. Cần reviewer độc lập đọc gói raw đóng băng |

## B. U1–U12

| U | Hạng mục | Lời khai công khai | loai | ket_luan | Ghi chú |
|---|---|---|---|---|---|
| U1 | PS5.1 endpoint | P2: ASUS PS5.1/PS7 carry-forward; P3 4 bước mỗi bản rc0 | carry_forward + public_projection_only + **direct_native_desktop_r1** | **cho_review** | [r1](r1/RESULTS.md): trên PS5.1.26100 Desktop, backend giả: S2 Control 38/38 và S3 Manifest 12/12 kèm counterexamples đạt. S1 Config **rc 1** dưới `en-US` (45/46, lỗi đặc tả/harness), dưới `tr-TR` thì 46/46 (ngoài đặc tả) |
| U2 | Danh tính VM f728/810 | P6 "U1–U12 per datum reconciled" | public_projection_only | cho_raw | 17/11: `f7281f27` online, `810f79bb` offline 116h (direct_live_17_11) |
| U3 | WhatIf | như §11 #3 | public_projection_only | cho_raw | |
| U4 | Updater thực tế | P4 post_runtime: ASAR bằng nhau, 4 mục metadata đổi | public_projection_only | cho_raw | |
| U5 | Provenance artifact | P3 "source G1… controlled fixture only" | fixture + public_projection_only | cho_raw | G1 không phải xác minh pháp lý |
| U6 | License fit | Owner xác nhận personal/noncommercial | owner_decision | passed | Theo chỉ thị handoff 17/11 |
| U7 | Retention/soak/theo dõi | P4 normal 1800s/180 mẫu | public_projection_only | cho_raw | Ngưỡng/owner phải có trong raw |
| U8 | Restore profile/đăng nhập | P4 7957 file restored | public_projection_only | **mở** | Không có bằng chứng phiên đăng nhập còn hiệu lực. Không được ghi PASS. Xem DESIGN.md §U8 |
| U9 | Cache/ACL ổ D ASUS | — | not_measured | cho_raw | ASUS offline 17/11 |
| U10 | Playwright CLI ghim | P2 lockfile + CI | ci_artifact + **direct_native_desktop_r1** | passed (nguồn) · **cho_review** (Windows) | `package-lock.json` blob `8b234cfa…`; [r1](r1/RESULTS.md) PIN OK |
| U11 | Auth remote f728 | P3 "actual authorized DC target" | public_projection_only | cho_raw | Status không chứng minh model auth/quota |
| U12 | Binary 5.5.0 ↔ upstream | P6 daily check 5.5.0/same asset digest | public_projection_only | cho_raw | |

## C. Hạng mục chéo

| Hạng mục | Hiện trạng | loai | ket_luan |
|---|---|---|---|
| Kiểm release hằng ngày | P6: chạy tay 13/11, không scheduler. 17/11: VM không có task Proxima/Playwright; 2 task `TraLuat-CapNhatCongCu-*` 14 ngày/lần, script 0 dòng `proxima\|playwright`; Desktop không có task ngoài MS/OneDrive; ASUS không đo | direct_live_17_11 + public_projection_only | **not_present** (2/3 máy) · ASUS not_measured |
| NSIS thực | Closeout tự khai giới hạn | not_run | gioi_han → DESIGN.md |
| Migration khác phiên bản | Closeout tự khai giới hạn | not_run | gioi_han → DESIGN.md |
| Runtime promotion / LIVE | Closeout: không LIVE | not_run | gioi_han → DESIGN.md |
| Dọn dẹp / khóa | 17/11 16:26Z: KHOA.txt 0 byte trên Desktop `C:\tl-win`, `F:\tl-win`, VM `C:\tl-win`. VM: Proxima + ProximaGateway chạy từ 13/11 04:04Z | direct_live_17_11 | Lúc đo không ai giữ khóa. Chưa chứng minh dọn dẹp đã xong |

## Blocker
1. ~~Gói raw cuối 13/11 không tìm thấy~~ → **18/11: đã định vị raw P3 + P4 trên ASUS** (xem `RAW-1311-POINTERS.md`, zip P4 `97e9b78f…`, zip P3 `147714ad…`, khớp băm tự khai). Vẫn thiếu raw P5 (VM) và hồ sơ P6 (ma trận ca/runbook/review/quyết định). Chưa review độc lập trên raw này.
2. VM chỉ còn ~1,67 GB trống ở C: — chặn mọi native run trên VM cho tới khi có quyết định dọn đĩa.
3. Chưa có spec/lease cho thi công bổ sung.

## D. Review độc lập raw P4 cuối 13/11 (18/11, `RAW-1311-VERDICT-claude-xhigh.md`)

Verdict tổng: **request_changes**. Toàn vẹn P4: khớp 41/41 entry, không có P1. Nội dung P3 chưa đọc được, vì ASUS ngừng phản hồi từ ~04:54Z.
Bảng này **thay** cột `ket_luan` của các hàng tương ứng ở mục A và B. Reviewer: Claude, context mới, chỉ đọc; effort KHONG_do_duoc.

| Hàng | Kết luận từ raw | Lý do chính |
|---|---|---|
| §11 #6 artifact sai/hỏng không kích hoạt | **partial** | Chỉ kiểm băm của artifact đúng (OS thật). Không có ca native nào đưa vào artifact sai hoặc hỏng |
| §11 #7 máy bận / updater trùng | **partial** | Khóa hai bên trên OS thật nằm ngoài zip. "Máy bận" chỉ dẫn tới dừng (assert), không hoãn, và chưa từng kích hoạt |
| §11 #8 promotion fence | **not_evidenced** | Raw chỉ có một máy |
| §11 #9 phục hồi binary + dữ liệu | **partial** | Dữ liệu: 7957 tệp khôi phục khớp byte (OS thật). "Rollback binary" chỉ là đổi sang thư mục baseline đặt song song |
| §11 #10 file lock / đĩa đầy / rollback thất bại | **not_evidenced** | Các ca này chỉ có trong mã test, không có kết quả chạy |
| §11 #11 healthcheck không inference | **passed (scoped)** | 180 mẫu `/v1/stats`, `totalRequests` 0, egress bị chặn. Chỉ trong phạm vi soak P4 trên profile thử |
| U4 updater thực tế | **partial** | Đã chứng minh trỏ được về feed owned. Nhánh có bản mới hơn (tải về, kiểm integrity, cài khi thoát) chưa từng chạy |
| U7 soak / retention | **partial** | Ngưỡng soak chỉ nằm trong mã. Không có retention, owner hay cửa sổ theo dõi |
| U8 restore profile/đăng nhập | **partial** | Vế dữ liệu đạt. Vế đăng nhập không đo được: profile thử chưa từng đăng nhập |
| U12 binary ↔ upstream | **partial** | Có digest của bộ cài release. Không có chữ ký, attestation hay provenance tới commit. Soak chạy trên biến thể `repaired` |

Còn thiếu: raw P5 trên VM (không có tệp nào trên VM); hồ sơ P6 (ma trận ca, runbook, review, retention); scheduler; NSIS thật; migration; kết quả chạy `test_recovery` trên Windows; các ca âm của updater và artifact; chữ ký; phiên đăng nhập.

## E. Review độc lập raw P3 (18/11, `RAW-P3-VERDICT-claude-xhigh.md`)

Verdict: **request_changes**. Toàn vẹn sạch: zip 118 entry khớp.

| Hàng | Từ raw P3 | Ghi chú |
|---|---|---|
| §11 #1 | partial | Raw có đúng **một** lựa chọn: add-on Playwright trên ASUS, chạy PS5.1 và PS7 |
| §11 #2 | partial | Target là chính máy cục bộ (`TL_PW_TARGET_ID`). Không có đích từ xa |
| §11 #3 / U3 | not_evidenced | Không có WhatIf trong raw P3 |
| §11 #4 | passed (zip 118 entry) | Reviewer tự quét: không có secret hay profile |
| §11 #5 | partial | Lock khớp và `audit signatures` đạt. Cache trình duyệt được seed bằng cách chép từ lượt trước |
| §11 #11 | not_evidenced | P3 không có healthcheck. Các cờ `no_inference` là hằng gán sẵn |
| U1 | partial | Fragment PowerShell của Playwright chạy thật trên PS5.1. Raw không có endpoint Proxima |
| U10 | passed (ASUS, PS5.1 + PS7) | `PIN OK`, lock `0DA56E1E…` |
| U11 | not_evidenced | `real_VM_WinRM_auth: not_measured` |

Hai lời khai công khai của P3 **không có trong raw**: "selected_remote authorized DC target + 4 status/WhatIf" và "guards 6 prior native cases via 4-module equivalence" (finding F1, F2).

## F. r2: bộ test operator P4 chạy trên ASUS (18/11, `r2/VERDICT-claude-xhigh.md`: **approve_scoped**)

Zip `74f02bd3…`. Mã đúng bằng mã P4 (`97e9b78f…`), không đổi sau khi chạy. `test_recovery.py` 19/19 trên win32; `test_native_lock` 4/4; `test_operator_safety` và `test_dependency_pins` đạt. Quét secret rc 0, lưu trong tệp.

| Hàng | Trước r2 | Sau r2 | Điều kiện đọc |
|---|---|---|---|
| §11 #10 file khoá / đĩa đầy / rollback thất bại | not_evidenced | **partial** | File khoá: `real_os` ở mức primitive Windows, trên dữ liệu tổng hợp. Đĩa đầy, chép dở, promotion-failure, restart-failure: **fixture** (`passed_fixture_scope`). "Đĩa đầy" là kiểm dự trữ khi hàm đo dung lượng bị giả về 0, **không phải ổ đầy thật** |
| §11 #7 máy bận / updater trùng | partial | partial | Khoá trùng nay có raw đóng băng. Ca `busy` nghĩa là "chưa xác minh chủ sở hữu đã đóng", **không** nâng được vế "máy bận thì hoãn" (vẫn not_evidenced). Khoá trùng của electron-updater vẫn not_evidenced |
| §11 #9 phục hồi | partial | partial | Thêm các ca âm ở phạm vi fixture. Rollback binary vẫn yếu |
| §11 #6 vế âm, §11 #8, U4, U8 | — | không đổi | Chưa có ca native trên Proxima/Electron thật |

Giới hạn sản phẩm quan sát được (P3 #7): sau promotion-failure, thư mục `profile` bị vắng; sau ca native locked profile, staging còn sót lại. Giao dịch chỉ chạy một lần nên cần người can thiệp.

## G. r3: chạy lại có chỉnh trên Desktop (18/11, `r3/VERDICT-claude-xhigh.md`: **approve_scoped**)

Zip `ad9a8a6e…`. Bốn finding chính của review r1 (N3, raw N5, N6, N7) **đã giải quyết**.

| Hàng | Cập nhật | Điều kiện đọc |
|---|---|---|
| §11 #3 WhatIf + U3 | **passed (scoped)** | r1 N4 12/12 trên cấu hình mẫu. Harness S2 Control 38/38 kèm counterexamples dưới `tr-TR` (r3), PS5.1 + PS7. Backend là đồ giả: **không** chứng minh trên gateway thật |
| §11 #1 bốn lựa chọn cài | **passed (scoped Desktop)** | r1 N2: selftest lõi 1777/1777 ×4 (không add-on / chỉ Proxima / chỉ Playwright / cả hai). r3: harness proxima-control đạt trên O1 (chỉ Proxima) và O3 (cả hai); Playwright đạt trên O2. Chỉ Desktop, PS7 cho Playwright |
| U1 PS5.1 | **passed (scoped)** | S1, S2, S3 đạt trên PS5.1.26100 kèm counterexamples dưới `tr-TR`, backend giả |
| §11 #5 / U10 pin Playwright | **passed (scoped Desktop + ASUS)** | Raw npm "3 verified registry signatures / 3 verified attestations" (r3). `PIN OK`. Kèm finding F1: dư lượng `ms-playwright\daemon` (P3-4, cần quyết sửa SKILL hay ghi nhận) |
| §11 #4 không secret | **passed (scoped gói r1/r2/r3/P3)** | Quét secret rc 0 lưu trong tệp, cộng quét bổ sung của reviewer |

Không đổi: §11 #2 (gateway thật / không fallback chưa đo), §11 #6–#10, U2, U4, U7, U8, U11, U12 (xem mục D, E, F).


## H. Quyết định của chủ kho 18/11 và r4 (đang thi công)

- **§11 #7, vế "máy bận"**: chủ kho **chấp nhận "dừng"** (`HOST_BUSY`: dừng, chờ người chạy lại) thay cho "tự hoãn". Lấy qua AskUserQuestion trong phiên `session_015GtxrapMSm976JLC7Fp1HM`. Vế này đọc theo nghĩa mới: mã P4 dừng đúng như vậy (`run_activation.py` dòng 23), và r2 đã có raw cho khoá trùng ở mức fixture. Vế "updater chạy trùng bị khoá" vẫn chờ R4-D.
- **r4** (đặc tả `ops/specs/wp1319-r4.md`, lease `ops/leases/wp1319-r4-g1-operator.yaml`): R4-A/B (§11 #6 vế âm), R4-C (U4), R4-D (§11 #7 vế updater trùng). Chủ kho duyệt "R4-A..D đủ". Kết quả sẽ ghi ở `r4/RESULTS.md`.

### H.1 Kết quả r4 (review 2/2 `approve_scoped`, `r4/VERDICT-run.md`, zip ASUS `cf712bc1…`)
| Hàng | Trước r4 | Sau r4 | Điều kiện đọc |
|---|---|---|---|
| §11 #6 vế âm (artifact hỏng hoặc sai nguồn) | not_evidenced | **partial (real_os)** | Sửa 1 byte (A) hoặc đổi kích thước (B1) thì bị chặn trước khi spawn. **Tệp thừa cạnh `Proxima.exe` (B2) KHÔNG bị chặn**: lỗi của đường kiểm P4 (P1-2) |
| U4 updater có bản mới | not_evidenced | **passed (scoped, real_os), chỉ nhánh sai integrity** | Proxima 5.5.0 (`baseline`, electron-updater gốc) thấy 5.5.1, tải về, từ chối vì `sha512 checksum mismatch`, không cài, binary và ASAR trùng byte. Chưa đo: cài thật khi bản tải hợp lệ, chữ ký số, biến thể `repaired` |
| §11 #7 máy bận | partial | **passed (scoped) theo quyết định "dừng"** | Khoá host trùng bị chặn trên OS thật (D1 `winerror 32`); khoá có nội dung thì `HOST_BUSY` (D2, fixture) |
| §11 #7 updater chạy trùng | not_evidenced | **partial** | Chỉ khoá của operator chặn được. **Proxima không có single-instance (D3):** lần chạy thứ hai cùng profile vẫn chạy updater song song và ghi đè `rest-port.json`, `ipc-port.json` và `settings.json` của profile (P1-1, P1-3) |

Finding sản phẩm cần chủ kho quyết định (không tự sửa):
- **P1-2:** đường kiểm trước khi spawn phải từ chối tệp ngoài manifest (DLL-planting).
- **P1-3:** cần `requestSingleInstanceLock` theo profile, hoặc chấp nhận rằng chỉ khoá operator bảo vệ.

### H.2 Quyết định của chủ kho, 18/11 tối
- **Quyền thi công**, chủ kho xác nhận "theo đề xuất":
  - **NSIS** được cài thật trên Desktop (máy thử), per-user, phải gỡ sạch sau khi đo.
  - **U8**: chủ kho tự đăng nhập/2FA trên profile thử; phiên điều phối không chạm credential, chỉ đo việc giữ phiên qua backup/restore.
  - **LIVE promote sang VM (gateway) chưa làm.** Chỉ làm sau khi WP-PXA (#1401) land và có kế hoạch promote, và phải hỏi xác nhận riêng cho đúng thao tác đó.
- **Raw P5 / hồ sơ P6 không thể khôi phục.** Chủ kho xác nhận không giữ bản nào. Đã tìm trên ASUS, Desktop và VM ngày 18/11 nhưng không thấy. Chưa đọc được `C:\Users\tladmin` (VM) và `C:\Users\ADMIN` (Desktop) vì bị từ chối quyền.
  - Mọi hàng chỉ dựa vào P5/P6 (§11 #8 "ASUS passed before VM canary", U2, U12 "P6 daily check", phần P5 của §11 #1/#3/#11) **không được tính là đạt dựa trên P5/P6**. Các hàng này phải đo lại hoặc giữ `not_evidenced`.
- **WP-PXA (#1401)** sửa P1-2 (tệp thừa) và P1-3 (khoá profile ở operator), và làm §11 #8 (promotion fence) ở mức hàm và test. Đã đối chứng trên cây Proxima thật ở ASUS: cây sạch cho `OK`; thêm `version.dll` thì bị chặn với `ARTIFACT_EXTRA`; gỡ ra thì lại `OK`. Còn chờ review 2/2 (Codex `gpt-6-astra` trên ASUS).
