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
| `scripts/ProximaControl.psm1` | `Find-PxcOpenTag`, `Find-PxcOpenEnd`, `Remove-PxcElicitation`; `Invoke-PxcAsk` lọc `answer`, thêm `answerMarkup`, `answerMarkupRemoved`; help của `px` |
| `scripts/ProximaControl.psd1` | `ModuleVersion` 2.1.0 → 2.2.0 |
| `SKILL.md` | 2.2.0; hai trường mới và luật cắt đuôi; hướng dẫn `gemini:auto` neo đúng mức lời khai #1457 r2; hệ quả handshake Remote |
| `tests/ProximaControl.Tests.ps1` | ca bắt buộc `X5-11` (27 → 28, 13 ca con, đo rò rỉ trên đối tượng thô mọi luồng, journal bắt buộc); `CX14`, `CX15`; giả lập `Chat` |
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
