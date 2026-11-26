# PX-LOC-MARKUP r4 — `proxima-control` lọc khối `<ElicitationsGroup>` (kết quả thi công)

**Căn cứ:** đặc tả `ops/specs/px-loc-markup-r4.md` (sha256 `a346d4542153cb7dff5ebcf1ce0bf2d1a2bbd88cfea8a1d19267f3cf73f9c51e`,
duyệt https://github.com/ducthangho/tra-luat/issues/1529#issuecomment-7180863540), lease `ops/leases/px-loc-markup-r4-g1-claude.yaml`,
Issue #1529.

## 1. Lịch sử packet
- r1: đặc tả `631a8beb…` (commit `b01f3dd`), ứng viên `8a33ddb`, review lượt 1 `changes_requested` 5 lớp P2 (`issuecomment-7171976816`).
- r2: đặc tả `5584a9f1…` (duyệt `7172132991`, `nang_tran` 6 → 8 tệp `7172063543`); lease r1 rút hạn (`7172238820`). Review lượt 2
  `c4e9711` 4/5 (`7172718120`), lượt 3 `86fc431` 1/3 (`7173165528`), lượt 4 `8060930` 0/3 (`7173867201`); dừng §12 + E1 (`7173867678`).
- r3: đặc tả `ebf6f277…` (duyệt `7174094220`), ứng viên `d0edb21`; review lượt 5 1/3 (`7174610534`); dừng §12 lần hai + E1 (`7174610982`),
  chủ kho chọn A (`7180137523`).
- r4: đặc tả `a346d454…` (duyệt `7180863540`), base `4a96ccd`. Review lượt 6 `90e7a78` 4/5 (`7181155845`, xét lại cách làm `7181159360`:
  mọi phép so chuỗi trong `X5-11` là Ordinal); lượt 7 `d9cd640` approve (`7181369591`); lượt 8 `6021106` 4 lớp hồ sơ (`7187931965`).

## 2. Thay đổi so với `origin/master`
Đường dẫn tính từ `.agents/skills/proxima-control/`.
| tệp | nội dung |
|---|---|
| `scripts/ProximaControl.psm1` | `Find-PxcOpenTag`, `Find-PxcOpenEnd`, `Remove-PxcElicitation`, `Test-PxcAdvertisedId`; `Invoke-PxcAsk` lọc `answer`, thêm `answerMarkup`, `answerMarkupRemoved`; `reportedModel` là `$null` (gán tường minh) khi đã bỏ khối, ngoài ra chỉ trả khi bằng một id trong danh sách `GET /v1/models` của chính lời gọi; help của `px` |
| `scripts/ProximaControl.psd1` | `ModuleVersion` 2.1.0 → 2.2.0 |
| `SKILL.md` | 2.2.0; hai trường mới, luật cắt đuôi, luật `reportedModel`; hướng dẫn `gemini:auto` neo đúng mức lời khai #1457 r2; hệ quả handshake Remote |
| `tests/ProximaControl.Tests.ps1` | ca bắt buộc `X5-11` (27 → 28; 17 ca con, N1 r4 chỉ đo chức năng: `answer`, `answerMarkup`, `answerMarkupRemoved`, `reportedModel`, byte của journal); `CX14`–`CX16`; móc `Chat` của HTTP giả (rỗng ⇒ body mặc định đúng như nền); `X5-01` route wire trả `prov/m2`, `X6-01` đặt `Chat` riêng trả `prov/m1` (N3) |
| `tests/ProximaManifest.Tests.ps1` | `$Want` và `CX04` theo 2.2.0 |

## 3. Nghiệm thu
| tiêu chí | trạng thái |
|---|---|
| N1 `X5-11` | **đạt** trên Windows: `X5-11` passed ở cả 5 lượt control H (4 lượt 28/28, lượt `-Counterexamples` 45/45), mục 6. |
| N2 `CX14`, `CX15`, `CX16` | **đạt** — KILLED, `credited` (mục 6). |
| N3 không hồi quy | **đạt** — 27 ca cũ đạt trên H ở cả 5 lượt control; `CX01`–`CX13` credited; diff harness đúng danh sách N3. |
| N4 manifest 2.2.0 | **đạt** — manifest H 7/7 ở PS 7 và PS 5.1 (mục 6). Đột biến tay: bản sao addon của cây H `d9cd640` với `.psd1` sửa về `2.1.0`, harness manifest của H, pwsh 7.6.10 trên `DESKTOP-T9R33P2` ⇒ rc 1, 2/7, `PM02 VALUE[ModuleVersion]` (cùng PM03–PM06 đỏ), report sha256 `a5801ba7ae12a1a2b69410cf2c0983ce14c12a7b32f21efb3f06db91aaf24f12`. |
| N5 tài liệu | mục 5 |
| N6 ma trận Windows | **đạt** (mục 6) |
| N7 gate kho | mục 5 |
| N8 phạm vi và trần | mục 5 |
| N9 review mã | review offline lượt 7 approve `d9cd640` (`issuecomment-7181369591`); connector Codex trên PR #1542: receipt `7186973192` (`Reviewed commit: 60211062d5`, "Didn't find any major issues"); comment tóm tắt `7181398228` bị sửa tại chỗ, nay ghi `6021106` completed, `has_any_findings=false`; kết quả connector trên `d9cd640` không còn readback nên không khai |

## 4. Phép đo phụ trong phiên Linux (PowerShell 7.4.6; không thay N6)
Parse 0 lỗi; `.psm1`/`.Tests.ps1` chỉ ASCII; `Remove-PxcElicitation` 14/14 và luật `reportedModel` 7/7 (kể cả qua CLIXML) qua `Import-Module`.

## 5. Gate trước push (N5, N7, N8)
Điền khi chạy trên SHA ứng viên; số ghi ở comment verdict và PR.

## 6. Lượt Windows: N6 và M3 theo đặc tả r4
Dựng trong một lệnh hai cây trên cùng máy Windows của chủ kho, nền B = `base_sha` của lease r4 (`4a96ccd`), ứng viên H = head của PR
lúc chạy; **mỗi vế chạy harness của chính cây ấy** (chép ra ngoài cây). Ma trận mỗi vế: `ProximaControl.Tests.ps1` với PS 7 và PS 5.1,
mỗi bản `en-US` và `tr-TR`, `-Counterexamples` ở PS 7 `en-US`; `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1. Báo cáo JSON lưu ngoài
cây, băm ghi vào đây. Đạt khi (N6) mọi lượt H rc 0, `passed == total`, `CX00` của H báo `CONTROL_PASSED`, mọi `CX01`–`CX16` của H
`credited`; (M3a) đủ lượt hai vế, không lỗi setup, không ca bắt buộc `skipped`/`not_run`/`NOT_EXECUTED`; (M3b) tập đỏ H ⊆ tập đỏ B;
(M3c) H đỏ thuộc write set thì chủ kho quyết.

**Lượt 1** (`issuecomment-7186739049`): H = `d9cd640`, máy `DESKTOP-T9R33P2` (Windows 10.0.26300, pwsh 7.6.10, PS 5.1.26100), theo
lệnh chủ kho, 08:03:23Z → 08:29:14Z; `run-n6.ps1` sha256 `22106228930088e2fb680eb9553ee9a418824295c179169497e5dd3ad2581583` (khớp bản đăng
`7181393257`), nguồn clone kho public; `summary.json` `1c04aceacb187142f5c29e490670d953053f156544fa9de180419d4f03adf427`. 14/14 lượt xanh.

**Lượt 2**: H = `6021106`, cùng máy, cây nguồn và B; script chỉ đổi SHA của H (sha256 `ba25d2b7e4ba92a427afbb13ee9d7fd25336ef9be02b3827c9f2074d4d8e8b29`),
09:10Z → 09:36:08Z; `summary.json` `7078bb1c7e04f29118fb58efb0d46beef3a04b02f8ff45f1e32f7c3ebd134ac0`. Kết quả theo ID của cả 14 `report.json`
(id/outcome, CX verdict/credited) ở tệp gọn sha256 `10cf0ac046fcde284ea6b795b7b5d5c54537fb6c61553755420bb89f978c1dc8` (đăng ở #1529).
Mọi lượt rc 0 (trích exit code từng lượt từ `summary.json`: `issuecomment-7188743380`), mọi ca `passed`, `failed_ids` và `setup_error_ids` rỗng; B control 27/27 ×4, `-Counterexamples` 41/41 (`CX00`
CONTROL_PASSED, `CX01`–`CX13` KILLED credited), manifest 7/7 ×2; H control 28/28 ×4, `-Counterexamples` 45/45 (`CX00` CONTROL_PASSED,
`CX01`–`CX16` KILLED credited), manifest 7/7 ×2. Băm `report.json` (B rồi H; ps51-enUS, ps51-trTR, pwsh-enUS, pwsh-enUS-cx, pwsh-trTR,
manifest-ps51, manifest-pwsh):
- B `eecf7e2868bf8c3769d792daa63210b93ab86b999524bef44a4f0f6eb7ff2bd6` `8524c9dad7e5d3fa3cdcc061402d10bed2a7566bc7dff353d5a03fc37aa30dc5`
  `d3c5a1038317a964cf57a98f4a8af033a9f6dd654bf9f4a7ce67ff2c642b3655` `1474b5077bb7c8e6124f1094a1073b119c61958e98ed8aa305f9fcb01ac5bdaa`
  `8505c1e90814429484ed7911d937892797cf6786f21ca2940b366bab819e4dc2` `a4c472a6d1bdb69284dfa6797966c265f1b2e2566c4549b0d4058f246a3e9459`
  `087ce70c46c00fb5b32b1e9bb5c550eff23fd95c397ae8dda791ce2fb6f6fe60`
- H `ebaa4dc1c533ee47dbce575be6a2d54a876ec5943dd6b22191134756b95a2304` `6a1573812e0753e274f980838770ccb786a62151cd7bccb571e90bc2f6ffb3eb`
  `80dd98033e9aea2f6154cd99b9a6e1ad1f23561a8e798fa5756dd95fda75da71` `126fd6b437c379876480a57eeefadc2809aa9b6d09514d0abf67f21f9f193deb`
  `1643bb26a126af1c6eb545487a84b434801df76ef0de2c8e8632cc497c7f55a1` `87d10209d398ee43a209a9af6ced8e7cf627c5caedde1c913d0c61a2ba3d11f8`
  `e2daf94882f4fe780b3d99773ea61057a5dd74cfa18bf99ae266496ea8bfb501`

N6 **đạt**; M3a **đạt** (đủ 7 lượt mỗi vế, không lỗi setup, không ca bắt buộc skipped/not_run/NOT_EXECUTED); M3b **đạt** (đỏ H = ∅ ⊆
đỏ B = ∅); M3c không áp dụng. Commit ghi tệp này chỉ đổi RESULTS; lượt Windows trên chính head cuối của PR ghi ở #1529 (không commit
thêm để head không đổi).

## 7. Lease
Lease g1 hết hạn 06:32:09Z. Lease kế nhiệm `px-loc-markup-r4-g2-claude` (chỉ thị chủ kho `issuecomment-7186765839`) nằm ở nhánh
`ops/px-loc-markup-r4-g2-lease` để diff PR giữ đúng write set của đặc tả; cùng write set, baseline `4a96ccd`.
