# PX-ASK-SONG r3 — test Windows tập trung của module 2.1.0: tất cả đạt

**Căn cứ:** đặc tả `ops/specs/px-ask-r3.md` §3, lease `ops/leases/px-ask-r3-g1-claude.yaml`. Review: `VERDICT.md` (cùng thư mục).

## 1. Kết luận
Tại `981f7616efcdd85ff56b9815821b674fce79b8d5` (tree `bd3633be…4a11`):
- `ProximaControl.Tests.ps1` đạt **27/27** ở cả bốn tổ hợp {PowerShell 7.6.10, Windows PowerShell 5.1.26100} × {en-US, tr-TR}.
- Lượt PS 7 en-US kèm `-Counterexamples` đạt **41/41** (27 ca + CX00–CX13). CX00 là đối chứng không đột biến. CX01–CX13 đều
  `credited=True`, kể cả hai counterexample mới `CX12` (bỏ `:` khỏi luật tiền tố) và `CX13` (so `P:` không phân biệt hoa thường).
- `ProximaManifest.Tests.ps1` đạt **7/7** trên PS 7 và PS 5.1.

**Không gọi model.** Chỉ dùng HTTP giả của harness và listener `127.0.0.1` do harness sở hữu.

## 2. Lệch so với đặc tả
Đặc tả §3 ghi chạy trên **ASUS**. Lúc chạy, ASUS offline trên Desktop Commander (lần cuối thấy cách 19 phút), nên test chạy trên
**Desktop** `a5f7076e`. Desktop có cùng loại môi trường: PS 7.6.10 và PS 5.1.26100.9711. Phạm vi, lệnh và tiêu chí giữ nguyên.

## 3. Cách chạy
- Script `T3.ps1` (sha256 `5f7662670f4382920d9f7d81de668fa5264ead4da06dd2a36f719a06e55a2dea`) chạy trên Desktop, PS 7:
  1. `git init` + `git -c core.autocrlf=false fetch --depth 1 https://github.com/ducthangho/tra-luat.git <SHA>` + `checkout FETCH_HEAD`.
  2. Băm 5 tệp.
  3. Chạy 6 lượt nối tiếp, mỗi lượt có scratch/evidence/report riêng **ngoài** cây clone.
- Lệnh từng lượt:
  - ProximaControl: `<exe> -NoProfile -NonInteractive -ExecutionPolicy Bypass -File <clone>\…\tests\ProximaControl.Tests.ps1 -ModulePath <clone>\…\scripts\ProximaControl.psm1 -ScratchRoot <dir> -ReportPath <json> -EvidenceRoot <dir> -TestCulture <en-US|tr-TR> [-Counterexamples]`
  - ProximaManifest: `<exe> … -File <clone>\…\tests\ProximaManifest.Tests.ps1 -AddonRoot <clone>\.agents\skills\proxima-control -ScratchRoot <dir> -ReportPath <json>`
- Một lượt trước đó trên `94c425d` (head của review lượt 1) đã đạt 27/27 ở PS 7 en-US và CX00–CX03 rồi bị **dừng có chủ đích**, vì
  `981f761` thay thế nó. Đã dừng cả cây 5 tiến trình; kiểm lại thì không còn tiến trình nào sống. Lượt dừng ấy không được tính.

## 4. Băm tệp trong clone (khớp từng byte với `git show 981f761:<path>`)
| tệp | sha256 |
|---|---|
| `scripts/ProximaControl.psm1` | `8c0fe3921524b53cb525df21b01c78a7ebc8e1c17eccac5fc254b019b81b6c38` |
| `scripts/ProximaControl.psd1` | `80dd0566c2d609f31688b354188e0abf614ddce44d7045600d1400a852aebbdb` |
| `SKILL.md` | `3aa5764e4842137e6792705e904c6593e54bfb5d28c1cfce09fbadea11ffef73` |
| `tests/ProximaControl.Tests.ps1` | `889c2d0fea2d4587bacaa6e037f1991e4a5db653015d1d8da0d085fa46459801` |
| `tests/ProximaManifest.Tests.ps1` | `dfca2150c02a7d63d675a7d7e0dbc360c7595d9fe0181981580e9f1176894b61` |

## 5. Kết quả từng lượt (`summary.json` sha256 `d3a7819427b7da7a408aa27032d0df7cafcf191425e121573ebddb477d54496d`, 2026-11-20T06:55:00Z)
| lượt | exe | rc | giây | passed/total | report sha256 |
|---|---|---|---|---|---|
| control-pwsh-enUS-cx | pwsh.exe | 0 | 356 | 41/41 | `4c0c8ff04864ecb0feef56787c28574de2733cf926192ced652fdc63866feba9` |
| control-pwsh-trTR | pwsh.exe | 0 | 22 | 27/27 | `3c247eca509e135a6c033be887d4019de476e99e35cffc7851b6a8658485a795` |
| control-ps51-enUS | powershell.exe | 0 | 22 | 27/27 | `0403e30637a8b55037c69c854f791b1c983a19704d03d67fb18e2e035c060f74` |
| control-ps51-trTR | powershell.exe | 0 | 21 | 27/27 | `e112103ebaefff11d421e0d51e18e10e5dd1d55734c609902cfaa4556a19c44e` |
| manifest-pwsh | pwsh.exe | 0 | 2 | 7/7 | `3f7e073ac52ee4e3c5545f4516a12e5f2f74548b0110d271aca57da9e7015dbf` |
| manifest-ps51 | powershell.exe | 0 | 3 | 7/7 | `b4e4d5555e817bf953e5ec6435126e3980dad73a0c5fb587c533cd6e03d0b54f` |

Counterexample (lượt control-pwsh-enUS-cx): `CX00 credited=False` (đối chứng, không chấm điểm); `CX01`–`CX13` đều `credited=True`.

Báo cáo JSON và evidence thô nằm trên Desktop (`…\tl-work\px-ask-r3\run-20261120T064714Z\`). Chúng không vào kho vì có đường dẫn hồ sơ
người dùng; băm ở bảng trên.

## 6. Chưa chứng minh
- Lời gọi model thật qua `px ask` (r4, cần chủ kho chạy lệnh admin trên VM).
- Remote: băm module đổi, nên handshake với endpoint chạy bản cũ sẽ lệch. Đã khai ở đặc tả §2, không đo.
