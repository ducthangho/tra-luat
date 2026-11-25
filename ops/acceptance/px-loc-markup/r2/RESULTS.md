# PX-LOC-MARKUP r2 — `proxima-control` lọc khối `<ElicitationsGroup>` (kết quả thi công)

**Căn cứ:** đặc tả `ops/specs/px-loc-markup-r2.md` (sha256 `5584a9f19b257de5e9896bc000e957945123d026305e3f7f23746ee783b91876`,
duyệt https://github.com/ducthangho/tra-luat/issues/1529#issuecomment-7172132991), lease `ops/leases/px-loc-markup-r2-g1-claude.yaml`,
Issue #1529.

## 1. Lịch sử packet
- r1: đặc tả `631a8beb…` (commit `b01f3dd`), lease r1 chỉ có trên nhánh cục bộ, ứng viên `8a33ddb`. Review offline §8.3 lượt 1:
  `changes_requested`, 5 lớp P2 (`issuecomment-7171976816`). Bốn lớp sửa trong mã/test/tài liệu; lớp
  `sensitive-diff-exceeds-file-cap` xử bằng `nang_tran` 6 → 8 tệp của đặc tả r2 (chủ kho, `issuecomment-7172063543`).
- Lease r1 rút hạn từ 22:45:09Z về 19:25:58Z theo chỉ thị chủ kho (`issuecomment-7172238820`), khối `thu_hoi_bang_rut_han` ở commit
  `6cba176` (sau rebase). Đặc tả, lease và RESULTS của r1 gỡ khỏi nhánh trước push; bản r1 tra được qua commit và comment trên #1529.
- `ai-dang-giu` cho 8 đường dẫn write set r2 sau 19:26Z: `NGƯỜI_GIỮ 0` cả 8 (một lần đo bị `ls-remote` từ chối đăng nhập, đo lại ra 0).

## 2. Thay đổi so với `origin/master`
Đường dẫn tính từ `.agents/skills/proxima-control/`.
| tệp | nội dung |
|---|---|
| `scripts/ProximaControl.psm1` | `Find-PxcOpenTag`, `Find-PxcOpenEnd`, `Remove-PxcElicitation`, `Test-PxcReportedModel`; `Invoke-PxcAsk` lọc `answer`, thêm `answerMarkup`, `answerMarkupRemoved`, chỉ trả `reportedModel` khi là model id thuần; help của `px` |
| `scripts/ProximaControl.psd1` | `ModuleVersion` 2.1.0 → 2.2.0 |
| `SKILL.md` | 2.2.0; hai trường mới, luật cắt đuôi, luật `reportedModel`; hướng dẫn `gemini:auto` neo đúng mức lời khai #1457 r2; hệ quả handshake Remote |
| `tests/ProximaControl.Tests.ps1` | ca bắt buộc `X5-11` (27 → 28, 14 ca con; không rò rỉ chứng minh bằng CẤU TRÚC: đúng một đối tượng trên mọi luồng, đúng tập khoá/giá trị của kết quả và của bản ghi, đúng một tệp journal); `CX14`, `CX15`, `CX16`; giả lập `Chat` |
| `tests/ProximaManifest.Tests.ps1` | `$Want` và `CX04` theo 2.2.0 |

## 3. Nghiệm thu
| tiêu chí | trạng thái |
|---|---|
| N1 `X5-11` | **chưa đo** trên harness — chỉ chạy được trên Windows (N6). Phép thử phụ ở mục 4 không thay N1. |
| N2 `CX14`, `CX15` | **chưa đo** trên harness (N6). |
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

## 6. Lượt Windows: N6 của đặc tả cộng điều kiện A/B của ADR-0060 M3
Đặc tả r2 (đóng băng) định nghĩa N6 chỉ trên SHA ứng viên. Packet áp ADR-0060, nên lượt Windows còn phải đạt M3(a)–(c); hai yêu cầu
cùng có hiệu lực, không cái nào thay cái nào (review lượt 2, lớp `windows-m3-baseline-omitted`). Biên nhận Windows ghi đủ cả hai vế:
- **Nền B** = `base_sha` của lease r2; **ứng viên H** = head của PR tại lúc chạy. Cùng một máy Windows của chủ kho, dựng trong **một** lệnh:
  hai cây Git riêng (B và H). **Mỗi vế chạy harness của CHÍNH cây ấy** (chép ra thư mục ngoài cây), trỏ `-ModulePath`/`-AddonRoot` vào
  cây ấy — để mọi id của tập bắt buộc ở mỗi vế được thực thi thật. (Cách cũ dùng harness H cho module B: `ProximaManifest` dừng ở PM02 vì
  B là 2.1.0 nên PM03/PM04/PM06 chỉ ghi `NOT_EXECUTED`, và `X5-11` dừng ở ca đầu vì B không có `answerMarkup` — review lượt 3 đo được.)
- **Ma trận mỗi vế**: `ProximaControl.Tests.ps1` với PS 7 và PS 5.1, mỗi bản `en-US` và `tr-TR`; `-Counterexamples` ở PS 7 `en-US`;
  `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1. Mỗi lượt lưu báo cáo JSON ngoài cây, ghi sha256 và danh sách id kèm kết quả.
- **Đạt** khi đồng thời: (N6) mọi lượt của H rc 0, `passed == total`, mọi CX của H `credited`; (M3a) không thiếu lượt nào ở cả hai vế,
  không lỗi setup, không ca bắt buộc `skipped`/`not_run`/`NOT_EXECUTED`; (M3b) trên các id CHUNG của hai vế (27 id `X*` và `PM01`–`PM07`,
  `CX00`–`CX13`), tập đỏ của H ⊆ tập đỏ của B; id chỉ H có (`X5-11`, `CX14`–`CX16`) xét theo N6; (M3c) H có ca đỏ thuộc write set thì
  chủ kho quyết.
- Trạng thái: **chưa đo**.

## 7. Đính chính mốc hạn lease r1 (review lượt 2, lớp `lease-expiry-prerequisite-stale`)
Đặc tả r2 (đóng băng, `luat_dung`) ghi lease r2 cấp sau khi lease r1 hết hạn **lúc 2026-11-25T22:45:09Z** — đó là hạn GỐC. Chủ kho
sau đó rút hạn lease r1 (`issuecomment-7172238820`): hạn CÓ HIỆU LỰC là **2026-11-25T19:25:58Z** (`lease_expires_at_utc` và
`thu_hoi_bang_rut_han.han_moi_utc` của blob lease r1 ở commit `6cba176`). Lease r2 cấp lúc **2026-11-25T19:28:04Z**: sau hạn có hiệu lực
126 giây; trước hạn gốc 3 giờ 17 phút 05 giây. Điều kiện của đặc tả ("cấp sau khi lease r1 hết hạn") được giữ theo hạn có hiệu lực;
chỉ mốc ghi trong đặc tả đã cũ. Đặc tả không sửa đè; đính chính ở đây.
