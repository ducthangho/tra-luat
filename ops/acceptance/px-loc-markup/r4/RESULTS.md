# PX-LOC-MARKUP r3 — `proxima-control` lọc khối `<ElicitationsGroup>` (kết quả thi công)

**Căn cứ:** đặc tả `ops/specs/px-loc-markup-r3.md` (sha256 `ebf6f2779f0759a9a3168037f9877e4546a027c752e10ef006e9934e47c1adda`,
duyệt https://github.com/ducthangho/tra-luat/issues/1529#issuecomment-7174094220), lease `ops/leases/px-loc-markup-r3-g1-claude.yaml`,
Issue #1529.

## 1. Lịch sử packet
- r1: đặc tả `631a8beb…` (commit `b01f3dd`), ứng viên `8a33ddb`, review lượt 1 `changes_requested` 5 lớp P2 (`issuecomment-7171976816`).
- r2: đặc tả `5584a9f1…` (duyệt `7172132991`, `nang_tran` 6 → 8 tệp `7172063543`); lease r1 rút hạn về 19:25:58Z (`7172238820`).
  Review lượt 2 `c4e9711` 4/5 (`7172718120`), lượt 3 `86fc431` 1/3 (`7173165528`), lượt 4 `8060930` 0/3 (`7173867201`); dừng §12 + E1
  (`7173867678`), chủ kho chọn A (`7173910620`).
- r3: đặc tả `ebf6f277…` (duyệt cùng chỉ thị rút hạn lease r2 về 20:45:19Z, `7174094220`). Nhánh cục bộ đổi tên `ops/px-loc-markup-r3`
  (bản remote `ops/px-loc-markup-r1` chỉ chứa commit đặc tả r1 của PR draft #1530). `ai-dang-giu` cho 8 đường dẫn r3 sau 20:45:22Z:
  `NGƯỜI_GIỮ 0`. Lease r3 cấp 20:47:27Z. Đặc tả/lease/RESULTS r1, r2 gỡ khỏi nhánh trước push.

## 2. Thay đổi so với `origin/master`
Đường dẫn tính từ `.agents/skills/proxima-control/`.
| tệp | nội dung |
|---|---|
| `scripts/ProximaControl.psm1` | `Find-PxcOpenTag`, `Find-PxcOpenEnd`, `Remove-PxcElicitation`, `Test-PxcAdvertisedId`; `Invoke-PxcAsk` lọc `answer`, thêm `answerMarkup`, `answerMarkupRemoved`, chỉ trả `reportedModel` khi bằng một id trong danh sách `GET /v1/models` của chính lời gọi; help của `px` |
| `scripts/ProximaControl.psd1` | `ModuleVersion` 2.1.0 → 2.2.0 |
| `SKILL.md` | 2.2.0; hai trường mới, luật cắt đuôi, luật `reportedModel` (danh sách quảng bá); hướng dẫn `gemini:auto` neo đúng mức lời khai #1457 r2; hệ quả handshake Remote |
| `tests/ProximaControl.Tests.ps1` | ca bắt buộc `X5-11` (27 → 28, 16 ca con; hợp đồng N1 của r3: đúng một đối tượng trên mọi luồng, mọi khoá/giá trị kết quả so tuyệt đối kể cả `mode`, `targetFingerprint`, `recordId`, journal so từng byte); `CX14`–`CX16`; giả lập `Chat`; đổi kỳ vọng `reportedModel` của `X5-01` (`prov/m2`) và `X6-01` (`prov/m1`, kèm `model` của phản hồi giả mặc định) theo N3 |
| `tests/ProximaManifest.Tests.ps1` | `$Want` và `CX04` theo 2.2.0 |

## 3. Nghiệm thu
| tiêu chí | trạng thái |
|---|---|
| N1 `X5-11` | **chưa đo** trên harness — chỉ chạy được trên Windows (N6). Phép thử phụ ở mục 4 không thay N1. |
| N2 `CX14`, `CX15`, `CX16` | **chưa đo** trên harness (N6). |
| N3 không hồi quy | **chưa đo** (N6). |
| N4 manifest 2.2.0 | **chưa đo** (N6). |
| N5 tài liệu | mục 5 |
| N6 ma trận Windows | **chưa đo** — chờ chủ kho chạy trên ASUS tại SHA ứng viên sau push |
| N7 gate kho | mục 5 |
| N8 phạm vi và trần | mục 5 |

## 4. Phép đo phụ trong phiên Linux (PowerShell 7.4.6; không thay N6)
- `[Parser]::ParseFile`: `ProximaControl.psm1`, `ProximaControl.psd1`, `ProximaControl.Tests.ps1`, `ProximaManifest.Tests.ps1` — 0 lỗi.
- `ProximaControl.psm1` chỉ chứa byte ASCII (`grep -cP '[^\x00-\x7F]'` ⇒ 0).
- `Remove-PxcElicitation` qua `Import-Module` (script tạm ngoài kho, không mạng/dịch vụ): 14/14 ca đúng — không khối, một khối, hai khối,
  khối giữa câu với đuôi space+CRLF, đuôi NBSP, thẻ mở cụt, khối lồng, thẻ mở thiếu `>`, dấu nháy chưa đóng, thẻ tự đóng, `>` trong dấu
  nháy, tên `ElicitationsGroupX`, tên viết thường, thẻ mở cụt cuối chuỗi. Đột biến `CX15` (so tên `OrdinalIgnoreCase`) trên bản sao thư mục
  `scripts` (đo với hàm r1): đúng ca tên viết thường đổi màu. `CX14` nằm trong `Invoke-PxcAsk`, phép thử phụ này không đo được.

## 5. Gate trước push (N5, N7, N8)
Điền khi chạy trên SHA ứng viên; số ghi ở comment verdict và PR.

## 6. Lượt Windows: N6 và M3 theo đặc tả r3
Theo N6 của đặc tả r3: dựng trong một lệnh hai cây trên cùng máy Windows của chủ kho, nền B = `base_sha` của lease r3, ứng viên H = head
của PR lúc chạy; **mỗi vế chạy harness của chính cây ấy** (chép ra ngoài cây). Ma trận mỗi vế: `ProximaControl.Tests.ps1` với PS 7 và
PS 5.1, mỗi bản `en-US` và `tr-TR`, `-Counterexamples` ở PS 7 `en-US`; `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1. Báo cáo JSON lưu
ngoài cây, băm ghi vào đây. Đạt khi (N6) mọi lượt H rc 0, `passed == total`, mọi CX của H `credited`; (M3a) đủ lượt hai vế, không lỗi
setup, không ca bắt buộc `skipped`/`not_run`/`NOT_EXECUTED`; (M3b) tập đỏ H ⊆ tập đỏ B (với H 0 đỏ thì đúng trên toàn tập); (M3c) H đỏ
thuộc write set thì chủ kho quyết. Trạng thái: **chưa đo**.

## 7. Đính chính mốc hạn lease r1 (review lượt 2, lớp `lease-expiry-prerequisite-stale`)
Đặc tả r2 (đóng băng, `luat_dung`) ghi lease r2 cấp sau khi lease r1 hết hạn **lúc 2026-11-25T22:45:09Z** — đó là hạn GỐC. Chủ kho
sau đó rút hạn lease r1 (`issuecomment-7172238820`): hạn CÓ HIỆU LỰC là **2026-11-25T19:25:58Z** (`lease_expires_at_utc` và
`thu_hoi_bang_rut_han.han_moi_utc` của blob lease r1 ở commit `6cba176`). Lease r2 cấp lúc **2026-11-25T19:28:04Z**: sau hạn có hiệu lực
126 giây; trước hạn gốc 3 giờ 17 phút 05 giây. Điều kiện của đặc tả ("cấp sau khi lease r1 hết hạn") được giữ theo hạn có hiệu lực;
chỉ mốc ghi trong đặc tả đã cũ. Đặc tả không sửa đè; đính chính ở đây.
