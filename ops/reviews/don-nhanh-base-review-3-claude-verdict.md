Repo remains untouched (only pre-existing untracked `nhiem_vu.txt`), HEAD unchanged. Here is the review:

```
verdict: changes_requested
reviewed_sha: 0ce4d4917afb955c76b17df44657e88eccc6a39f
assurance: same_provider_approved

## Danh sách đóng được của lượt 2

ĐÓNG. Đã ĐO lại độc lập, không tin số người vá báo:

- `pwsh` không có sẵn trong container này (khác doctor output đã đo trước đó cho phiên
  khác) — tải trực tiếp PowerShell 7.4.6 linux-x64 từ GitHub release chính thức vào
  scratchpad, `chmod +x`, dùng qua PATH. `TMPDIR=/dev/shm` như dặn.
- Bản `1511dd75a5a4f65c623738f2dc91e384b96bad9a` (script cũ) + bộ test HEAD (có t14/t15):
  tái lập ĐỘC LẬP hồi quy — `14/15`, đỏ đúng `t14`, log cho thấy đúng cơ chế: dòng cảnh báo
  stderr làm `ConvertFrom-Json` chết → "TU CHOI XOA" oan dù danh sách PR đọc được thật.
- M7 (gộp `$het` thay vì `$raGh` cho `$vanBan`, tức lùi lại đúng lỗi lượt 2): `14/15`, đỏ
  đúng `t14`. Khớp số người vá báo.
- M8 (bỏ `if ($ghRc -ne 0) { throw ... }`): `13/15`, đỏ đúng `t10` và `t15`. Khớp số người
  vá báo.
- Ba vế của phép thử #1 (cảnh báo stderr + `[]`, rc=0) chạy trên **script HEAD thật** qua
  kịch bản end-to-end riêng (không chỉ chạy lại `t14` có sẵn): `rc=0` ✓, base
  `nen/tichhop` được giữ ✓, nhánh rác `ops/rac` bị xoá ✓ — cả ba vế đúng như lease đòi.
- Đo phụ trợ người vá dùng làm căn cứ chọn cách tách luồng (`gh` in cảnh báo + `[]`, rc=0
  ⇒ `$het.Count=2`, 1 ErrorRecord + 1 String, `$vanBan` nối lại = `"[]"`, parse OK): tái lập
  ĐÚNG y hệt bằng script độc lập của tôi.

## Findings

### 1. Đột biến SỐNG SÓT trong đúng hai tệp — `scripts/don-nhanh.ps1`, dòng đổi bởi patch này
(hunk `$vanBan = ($raGh -join "\`n").Trim(); if ([string]::IsNullOrWhiteSpace($vanBan)) { throw 'gh rc=0 nhung STDOUT rong' }`)

Trả lời câu hỏi 3: **có cái thứ tư.** Đổi phép kiểm RỖNG từ kiểm NỘI DUNG (`$vanBan`, đã
tách stderr) sang kiểm SỐ DÒNG THÔ (`$het.Count -eq 0`) — tức đúng kiểu lỗi mà cả patch này
đang sửa (dùng luồng chưa tách sạch) — vẫn cho **15/15** trên bộ test HEAD. Lý do: `t12`
(ca duy nhất kiểm "rc=0 + rỗng") dùng `-ThoNguyen ''`, tức `gh` giả không in GÌ CẢ kể cả
stderr, nên `$het.Count` ở đó CŨNG bằng 0 — hai cách kiểm trùng nhau đúng ở ca đó, nên
không ca nào phân biệt được chúng.

Hậu quả THẬT khi chạy end-to-end (không chỉ theo lý thuyết) trên kịch bản "rc=0, stdout
rỗng, stderr có 1 dòng cảnh báo" — đúng ca mục 2 của muc_kiem, đã tự dựng vì không có sẵn
trong bộ 15:
- Script HEAD (đúng): `rc=13`, "gh rc=0 nhung STDOUT rong", base `nen/tichhop` **được giữ**,
  `ops/rac` **được giữ** (từ chối toàn bộ, đúng fail-close).
- Script với đột biến trên: `rc=0`, in "giu them 0 ref cua 1 PR dang mo" rồi **XOÁ THẬT**
  `nen/tichhop` (base của PR đang mở) lẫn `ops/rac`. Cơ chế: `ConvertFrom-Json ''` không
  ném lỗi (dù `$ErrorActionPreference='Stop'`) mà trả `$null`; `@($null)` trong PowerShell
  có `.Count = 1` (KHÔNG phải 0) — bẫy y hệt bẫy `@($null)`/mảng-đơn CLAUDE.md đã ghi ở chỗ
  khác trong chính hàm này. `$doDuocPR` thành `$true` với danh sách giữ rỗng.

Đây KHÔNG phải bug trong mã đã gửi — dòng thật ở HEAD kiểm `$vanBan` (nội dung), không kiểm
`$het.Count`, nên hành vi hiện tại ĐÚNG (đã xác nhận ở trên). Đây là **lỗ trong bộ test**:
không có ca nào khoá riêng "rc=0, stdout rỗng SAU KHI tách, nhưng có cảnh báo trên stderr"
— một khúc code refactor hợp lý trong tương lai (đổi cách kiểm rỗng, coi `$het.Count` là
tương đương `$vanBan` rỗng) có thể lùi lại đúng loại lỗi hai lượt trước đã tìm, mà `15/15`
vẫn xanh.

Đây là lần THỨ BA hàm này cần một ca test/patch để đóng một cách hành vi RỖNG/MƠ HỒ của
`gh` bị hiểu sai (lượt 1: rc≠0 nhưng JSON hợp lệ; lượt 2/patch này: stderr trộn vào JSON;
nay: đếm dòng thay vì đếm nội dung) — đúng hình dạng CLAUDE.md gọi là "lặp ba lần trở lên
thì câu hỏi đúng là có nên làm việc này không". Tôi không đủ căn cứ để nói kiến trúc PHẢI
đổi ngay (bản vá lần này không sai), nhưng khuyến nghị cụ thể, tối thiểu: thêm `t16` ghim
đúng ca "rc=0, `$raGh` rỗng, `$loiGh` không rỗng" để lỗ này không còn là lỗ.

## Nợ khai báo

Không có nợ mới ngoài danh sách đã khai (`-BoQuaLopPR`, phụ thuộc `gh`, `.cmd` chỉ chạy
Windows, `tl selftest` KHÔNG ĐO ĐƯỢC — giữ nguyên "chưa ai đo", lease ngoài cây checkout).

## Phép đo đã chạy

- `git rev-parse HEAD` = khớp neo; `git status --porcelain` rỗng trước/sau (chỉ
  `nhiem_vu.txt` chưa track, có sẵn từ đầu, không đụng).
- `git diff 1511dd7..HEAD -- scripts/` = đúng 2 tệp, đúng +21/−4 và +39/−1 như lease.
- pwsh KHÔNG có sẵn trong container này → tải PowerShell 7.4.6 linux-x64 chính thức từ
  GitHub release vào scratchpad, `TMPDIR=/dev/shm`.
- `pwsh scripts/don-nhanh_test.ps1` trên HEAD: **15/15**.
- `-LapCa t14...` và `-LapCa t15...` riêng lẻ trên HEAD: mỗi ca **1/1**.
- Script cũ (`1511dd7`) + test HEAD trong thư mục scratch riêng: **14/15**, đỏ `t14` — hồi
  quy tái lập độc lập.
- M7 (gộp luồng): **14/15**, đỏ `t14`. M8 (bỏ kiểm rc): **13/15**, đỏ `t10`+`t15`. Cả hai
  khớp số người vá báo.
- M9 (đột biến của tôi — đổi kiểm rỗng từ `$vanBan` sang `$het.Count -eq 0`): **15/15** —
  sống sót. Đo tiếp end-to-end trên kịch bản "rc=0, stdout rỗng, stderr có cảnh báo" (không
  có sẵn trong 15 ca): HEAD từ chối đúng (base+rác đều giữ); M9 xoá thật base của PR đang
  mở.
- Bốn ca biên của câu hỏi 2, mỗi ca dựng script pwsh riêng chạy `& gh ... 2>&1` thật rồi đối
  chiếu với logic tách luồng của HEAD:
  - JSON nhiều dòng + cảnh báo XEN GIỮA: `het.Count=4`, tách đúng, `ConvertFrom-Json`
    thành công, count=1.
  - Cảnh báo in SAU JSON: `het.Count=2`, tách đúng, parse OK, count=0 (mảng rỗng hợp lệ).
  - stdout rỗng + stderr có nội dung, rc=0: `$vanBan` rỗng đúng (`IsNullOrWhiteSpace=True`)
    → sẽ ném lỗi đúng nhánh throw (xem M9 ở trên để thấy hậu quả nếu KHÔNG ném).
  - `gh` tồn tại trên PATH nhưng KHÔNG executable: `Get-Command gh -ErrorAction
    SilentlyContinue` trên pwsh/Linux VẪN tìm thấy nó (không lọc theo bit thực thi) →
    `& gh ...` némLỗi .NET chấm dứt ("Program 'gh' failed to run… No such file or
    directory") NGOÀI luồng `2>&1` — nhưng khối `try { ... } catch { ... }` bao quanh toàn
    bộ lời gọi `gh` (đã có từ trước patch này, không đổi trong diff) bắt được, nên vẫn fail-
    close đúng: chạy end-to-end cho `rc=13`, base+rác đều giữ.
- Đo lại phép đo phụ trợ của người vá (cảnh báo + `[]`, rc=0 ⇒ `het.Count=2`, nối lại
  `"[]"`, parse OK count=0): khớp từng chữ.
- `actionlint`/`eol`/`lease_publish`/`release-verify`/`golden`/`file_count` mà người vá báo:
  KHÔNG đo lại — ngoài phạm vi đóng băng (2 tệp `scripts/`), không đụng `ci.yml` hay các
  cổng đó trong delta đang xét.
```
