# PX-LOC-MARKUP r1 — `proxima-control` lọc khối `<ElicitationsGroup>` (kết quả thi công)

**Căn cứ:** đặc tả `ops/specs/px-loc-markup-r1.md` (sha256 `631a8bebbc22ba281312ae468142fee0892f302914ed8fb1c25eae41f6b8ecb6`),
lease `ops/leases/px-loc-markup-r1-g1-claude.yaml`, Issue #1529.

## 1. Thay đổi (base `d0868db`)
| tệp | +/− | nội dung |
|---|---|---|
| `scripts/ProximaControl.psm1` | +33/−2 | `Find-PxcOpenTag`, `Remove-PxcElicitation`; `Invoke-PxcAsk` lọc `answer`, thêm `answerMarkup`, `answerMarkupRemoved`; help của `px` |
| `scripts/ProximaControl.psd1` | +1/−1 | `ModuleVersion` 2.1.0 → 2.2.0 |
| `SKILL.md` | +9/−2 | phiên bản 2.2.0; mô tả hai trường mới; hướng dẫn `gemini:auto`; hệ quả handshake Remote |
| `tests/ProximaControl.Tests.ps1` | +38/−7 | ca bắt buộc `X5-11` (27 → 28); `CX14`, `CX15`; giả lập `Chat` cho POST |
| `tests/ProximaManifest.Tests.ps1` | +2/−2 | `$Want` và `CX04` theo 2.2.0 |

Đường dẫn trong bảng tính từ `.agents/skills/proxima-control/`. Số dòng đo bằng `git diff --numstat` trước commit, 25-11-2026.

## 2. Nghiệm thu
| tiêu chí | trạng thái | bằng chứng |
|---|---|---|
| N1 hành vi lọc (`X5-11`) | **chưa đo** trên harness | Chỉ chạy được trên Windows (N6). Phép thử phụ dưới đây không thay N1. |
| N2 `CX14`, `CX15` | **chưa đo** trên harness | Như trên. |
| N3 không hồi quy (27 ca cũ, `CX00`–`CX13`) | **chưa đo** | Như trên. |
| N4 manifest 2.2.0 | **chưa đo** | Như trên. |
| N5 tài liệu `SKILL.md` | xem mục 3 | |
| N6 ma trận Windows | **chưa đo** — chờ chủ kho chạy trên ASUS tại SHA ứng viên | |
| N7 gate kho | xem mục 3 | |
| N8 phạm vi diff ⊆ write set | xem mục 3 | |

## 3. Phép đo trong phiên Linux (không thay N6)
- Phân tích cú pháp bằng PowerShell 7.4.6 (Linux, `[Parser]::ParseFile`): `ProximaControl.psm1`, `ProximaControl.psd1`,
  `ProximaControl.Tests.ps1`, `ProximaManifest.Tests.ps1` — 0 lỗi mỗi tệp.
- `ProximaControl.psm1` chỉ chứa byte ASCII (`grep -P '[^\x00-\x7F]'` ⇒ 0 dòng), khớp ca `SOURCE_NOT_ASCII` của harness.
- Thử riêng `Remove-PxcElicitation` qua `Import-Module` (script tạm ngoài kho, không mạng, không dịch vụ): 8/8 ca đúng —
  không khối, một khối, hai khối, khối cụt, khối lồng, tên `ElicitationsGroupX`, tên viết thường, thẻ mở cụt ở cuối chuỗi.
  Đột biến `CX15` (so tên thẻ `OrdinalIgnoreCase`) trên bản sao thư mục `scripts`: 7/8, đúng ca tên viết thường đổi sang
  `unterminated`. Đột biến `CX14` nằm trong `Invoke-PxcAsk`, phép thử phụ này không đo được nó.
- **N5** (đo trên `SKILL.md` đã nối dòng theo từng đoạn): câu hướng dẫn `gemini:auto` có ở 1 đoạn; `answerMarkup` và
  `answerMarkupRemoved` mỗi tên có ở 1 đoạn; frontmatter `2.1.0` = 0, `2.2.0` = 1; mục *Phiên bản* `2.1.0` = 0, `2.2.0` = 2. **Đạt.**
- **N8**: `git diff --name-only d0868db..HEAD` cho đúng 8 đường dẫn, cả 8 thuộc `write_set`. **Đạt.**

## 4. Gate trước push (N7)
Trên commit thi công `651de87e96e35c32baffe08bdd8bf6587f7363b9` (`core.abbrev` = 7):
- `python3 scripts/tl.py --selftest` ⇒ `1789/1789`.
- `git diff --check` trên phần thay đổi ⇒ sạch.
- `ops/lease_publish.py check ops/leases/px-loc-markup-r1-g1-claude.yaml` ⇒ đăng được.
Commit chứa bản RESULTS này chạy lại gate trước push; số ghi ở PR.
