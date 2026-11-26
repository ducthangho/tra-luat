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
- r4: đặc tả `a346d454…` (duyệt `7180863540`). Nhánh `ops/px-loc-markup-r4`, rebase lên `origin/master` `4a96ccd` (19 commit mới, không
  commit nào chạm module). `ai-dang-giu` cho 8 đường dẫn r4 lúc 02:31:48Z: `NGƯỜI_GIỮ 0`. Lease r4 cấp 02:32:09Z. Đặc tả/lease/RESULTS
  r1–r3 gỡ khỏi nhánh trước push.

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
| N1 `X5-11` | **chưa đo** trên harness — chỉ chạy được trên Windows (N6). Phép thử phụ ở mục 4 không thay N1. |
| N2 `CX14`, `CX15`, `CX16` | **chưa đo** trên harness (N6). |
| N3 không hồi quy | diff harness ngoài `X5-11`/CX mới đúng danh sách N3 (đọc diff); chạy ca cũ **chưa đo** (N6). |
| N4 manifest 2.2.0 | **chưa đo** (N6). |
| N5 tài liệu | mục 5 |
| N6 ma trận Windows | **chưa đo** — chờ chủ kho chạy trên máy Windows tại SHA ứng viên sau push |
| N7 gate kho | mục 5 |
| N8 phạm vi và trần | mục 5 |
| N9 review mã | thuộc review (offline và connector) |

## 4. Phép đo phụ trong phiên Linux (PowerShell 7.4.6; không thay N6)
- `[Parser]::ParseFile`: `ProximaControl.psm1`, `ProximaControl.Tests.ps1`, `ProximaManifest.Tests.ps1` — 0 lỗi.
- `ProximaControl.psm1` và `ProximaControl.Tests.ps1` chỉ chứa byte ASCII (`grep -cP '[^\x00-\x7F]'` ⇒ 0).
- `Remove-PxcElicitation` qua `Import-Module` (script tạm ngoài kho, không mạng/dịch vụ): 14/14 ca đúng.
- Luật `reportedModel` (đúng hai dòng của module, chạy trong phạm vi module): 7/7 ca đúng — đã bỏ khối với model quảng bá và với model
  trùng nhãn ⇒ `$null`; `none`/`unterminated` với id quảng bá ⇒ chuỗi; id không quảng bá, khác hoa/thường, không phải chuỗi ⇒ `$null`.
  Cả bảy giữ đúng giá trị sau round-trip `PSSerializer` (CLIXML, như đường Remote).

## 5. Gate trước push (N5, N7, N8)
Điền khi chạy trên SHA ứng viên; số ghi ở comment verdict và PR.

## 6. Lượt Windows: N6 và M3 theo đặc tả r4
Dựng trong một lệnh hai cây trên cùng máy Windows của chủ kho, nền B = `base_sha` của lease r4 (`4a96ccd`), ứng viên H = head của PR
lúc chạy; **mỗi vế chạy harness của chính cây ấy** (chép ra ngoài cây). Ma trận mỗi vế: `ProximaControl.Tests.ps1` với PS 7 và PS 5.1,
mỗi bản `en-US` và `tr-TR`, `-Counterexamples` ở PS 7 `en-US`; `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1. Báo cáo JSON lưu ngoài
cây, băm ghi vào đây. Đạt khi (N6) mọi lượt H rc 0, `passed == total`, `CX00` của H báo `CONTROL_PASSED`, mọi `CX01`–`CX16` của H
`credited`; (M3a) đủ lượt hai vế, không lỗi setup, không ca bắt buộc `skipped`/`not_run`/`NOT_EXECUTED`; (M3b) tập đỏ H ⊆ tập đỏ B;
(M3c) H đỏ thuộc write set thì chủ kho quyết. Trạng thái: **chưa đo**.
