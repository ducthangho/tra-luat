# WP1319 — Review độc lập gói raw P3 (ASUS native canary + G1 handoff)

verdict: request_changes

Phạm vi: chỉ gói raw P3 trên ASUS (`C:\Users\admin\tl-work\mission1238-asus-20261112-P3\`) và bản re-export `.b64`.
Không đọc `ops/acceptance/wp1319/r1/*`, cũng không đọc `RAW-1311-VERDICT-claude-xhigh.md`.
Trong kho chỉ đọc: `ops/plans/PROXIMA-PLAYWRIGHT-v1.md` §11, bảng U1–U12 trong `docs/research/2026-11-05-proxima-playwright-p0.md`, các hàng P3 trong `ops/acceptance/wp1319/MATRIX.md`, `RAW-1311-POINTERS.md`, và blob tại `b0b5480`.

Tóm tắt lý do: toàn vẹn sạch (không có P1). Chuỗi capture PS5.1/PS7 → G1 có raw thật và khớp từng byte.
Nhưng ba lời khai công khai của P3 không có trong raw P3:
- "selected_remote actual authorized DC target execution and 4 status/WhatIf";
- "guards 6 prior native cases via exact 4-module file equivalence";
- "config/metadata unchanged" (một phần).

Ngoài ra, các cờ `no_inference`, `new_inference_calls: 0` và `no_service_or_profile_change` là **hằng ghi cứng** trong script, không phải kết quả đo.
Nếu bản chiếu và MATRIX gỡ hoặc dời ba lời khai trên sang nguồn raw đúng (P5?), và gắn nhãn lại các cờ hằng, thì phần còn lại có thể nhận `approve_scoped` trong đúng phạm vi ở mục "Phạm vi duyệt được".

## 1. Toàn vẹn (đo 18/11/2026 qua Desktop Commander, chỉ đọc)

| Đối tượng | Kết quả |
|---|---|
| `ASUS-native-canary-evidence.zip` | `certutil` sha256 `147714ade0daaac048e51445ef5e9775e9f44008d906a093060a953b643eceff`, 155 062 byte (**khớp** tự khai) |
| `evidence-manifest.json` | `35cc813cf575652dc82462059291d8d0450eba0f4f3a8e0c88fcab8e2a8eeee7` (khớp); 117 khoá |
| `native-canary-result.json` | `3a4b91b4cf1104a820004a5a8b0d041d71f23087a18da5b2f069be125c40f420` (khớp) |
| `G1-handoff-result.json` | `05814804e9aea3f330bba85c95bbc7aca688c1c6669765f59aeff7040212ef30` (khớp) |
| `P3-evidence-export-20261113.b64` | `93bab58edc6d7f52d204639bced1bd96a821a3049c10d09eb1d281aa27ac09c2` (khớp); dài 206 804 ký tự, kết thúc bằng `==\r\n`. Giải mã trong bộ nhớ ra **155 062 byte, sha256 `147714ad…eceff`**, magic `504b0304`. **Trùng byte với zip gốc.** |
| Entry trong zip | **118** entry, 0 tên trùng, 0 tên dùng `\`, comment rỗng |
| Đối chiếu manifest (PowerShell 5.1, băm SHA256 trong bộ nhớ) | **117/117 khớp cả size lẫn sha256**. 0 sai, 0 thiếu. Thừa đúng 1 entry là `evidence-manifest.json`, sha `35cc813c…` = tệp trên đĩa |
| CRC (Python `zipfile.testzip` + `zlib.crc32` từng entry, đọc trong bộ nhớ) | `testzip=None`, **0 CRC sai / 118** |
| Mã nguồn tại M (đối chiếu với kho local) | `source\SKILL.md` `1799c2bd…`, `package.json` `d52eb046…` và `package-lock.json` `0da56e1e…` trùng blob tại `b0b5480807dd…` (tree `c8e8681e…`). 5 fragment PowerShell băm ra đúng 5 giá trị `source_fragments_sha256`. `repo\` trên ASUS: `rev-parse HEAD` = `b0b5480…`, tree `c8e8681e…`, `is-shallow=false` |

Kết luận toàn vẹn: **sạch, không có P1.**

## 2. Đánh giá từng hàng (chỉ dựa trên raw)

Ký hiệu loại bằng chứng: `real_os` = chạy thật trên OS · `fixture` = fixture có kiểm soát · `carry_forward` = kế thừa từ lượt trước.

| Hàng | Kết luận | Loại | Bằng chứng (entry · sha256 · trích nguyên văn) |
|---|---|---|---|
| §11 #1 Bốn lựa chọn cài; thiếu add-on không phá core | **partial** | real_os | P3 chỉ có **một** lựa chọn: add-on Playwright cài từ nguồn M trên ASUS, PS5.1 và PS7. `flow-ps51/01-setup.stdout` `f341cc28…`: `"3 packages have verified registry signatures"`, `"SETUP OK"`. Core (`repo\scripts\tl.py source-verify`) có chạy, nhưng chỉ để nhận output của add-on. **Không có** ca "không cài", "chỉ Proxima", "cả hai", và không có ca "thiếu add-on mà core vẫn chạy". |
| §11 #2 Đúng target; không fallback/retry | **partial** | real_os | Target là chính máy cục bộ. `flow-ps51/01-setup.ps1` `a157f58b…` so với fragment 0 chỉ khác đúng 4 dòng placeholder: `$env:TL_PW_TARGET_ID = 'ASUS-LAPTOP'`. Fragment pin kiểm lại: `flow-ps51/02-capture-init.stdout` `d75248b2…` ghi `"target ASUS-LAPTOP"`, `"PIN OK"`; PS7 `62efd87e…` y hệt. Không retry: mỗi addon chỉ có **1** thư mục `runs\`, không có `flow-*-<suffix>`. `commands.json` có 4 dòng, `timed_out` null (`8d8875b6…` / `4bc1e3e4…`). `measurement.csv` `fc7e9386…`: `literal-fullflow,4,4,0,0`. **Không có** ca âm (sai hoặc thiếu TargetId). Không có target remote hay gateway. Nhánh "retry inference" không áp dụng vì không có inference. |
| §11 #3 WhatIf không mutation | **not_evidenced** | — | Quét 118 entry: 0 lần xuất hiện `WhatIf`, `ShouldProcess`, `proxima`. |
| §11 #4 Không secrets/profile trong evidence | **passed** (trong phạm vi zip 118 entry) | real_os (reviewer tự quét) | Quét theo mẫu token/secret/cookie/bearer/API key/khoá riêng/profile: chỉ khớp tên biến trong bộ lọc env (`literal_flow.py`, `verify_handoff.py`), chuỗi `PublicKeyToken` của CLIXML (`flow-ps51/01-setup.stderr` `049b8bc2…`) và tên khoá `webapp_credentials_supplied`. `addon-ps51/runs/.../browser.json` `a281f2e0…`: `"isolated": true`. Zip không có thư mục profile hay cache trình duyệt. Xem mục 4. |
| §11 #5 Package/browser/cache nhất quán | **partial** | real_os + carry_forward | **Package:** lock tại M là `0da56e1e…` (đo lại 18/11 trên cả hai `install\0.1.0\package-lock.json`); `npm ci` chạy từ lock, `audit signatures` đạt; `@playwright/cli@0.1.23`, `playwright@1.65.0-alpha-2026-10-30`. **Browser:** `chromium-1252`, `"browser 157.0.8103.15"`; `chrome.exe` ở cả hai cache có sha `7ca0cf1b…` (đo lại 18/11), `INSTALLATION_COMPLETE` có mặt. **Cache:** mỗi addon có `PLAYWRIGHT_BROWSERS_PATH` riêng. Có điều: cache được **chép từ lượt trước**. `flow-ps51/cache-provenance.json` `5d6c0a30…`: `"official_installer_still_required": true`, và cả hai shell đều seed từ `...cleanenv-20261111\addon-ps51\browsers\0.1.0`. Chỉ băm mỗi `chrome.exe`, không băm toàn bộ thư mục. Thư mục nguồn ấy ngày 18/11 **không còn** (`Test-Path` = False). |
| §11 #11 Healthcheck không inference | **not_evidenced** | — | P3 không có healthcheck hay status nào. `native-canary-result.json` `3a4b91b4…` `"no_inference": true` và `G1-handoff-result.json` `05814804…` `"new_inference_calls": 0` là **hằng ghi cứng** trong `bootstrap_native.py` `38fea1ab…` và `verify_handoff.py` `95eb80ac…`, không phải phép đo. Phía trình duyệt chỉ ghi được 2 request tới 127.0.0.1 (`04-requests.json`); `npm` có gọi registry (xem mục P3). |
| U1 Endpoint PS5.1 | **partial** | real_os | Các fragment PowerShell của add-on Playwright chạy thật bằng `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe` (`flow-ps51/commands.json` `8d8875b6…`, argv[0]); CLIXML stderr ghi `mscorlib, Version=4.0.0.0`, tức Desktop/5.1. Cả 4 bước rc 0. PS7 cũng chạy, `pwsh.exe`, `System.Private.CoreLib 10.0.0.0`. Đây **không phải** endpoint điều khiển Proxima mà U1 nhắm tới (P1-S2). |
| U3 Lỗi WhatIf | **not_evidenced** | — | Không có WhatIf trong raw P3. |
| U10 Ghim Playwright | **passed** (trong phạm vi ASUS, PS5.1 + PS7) | real_os (+ carry_forward cho byte trình duyệt) | `addon-ps51/runs/.../00-pins.log` `c97489eb…` và PS7 `a07ab272…`: `"lock 0DA56E1E…"`, `@playwright/cli@0.1.23`, `playwright@1.65.0-alpha-2026-10-30`, `"cli 0.1.23"`, `"browser 157.0.8103.15"`, `"PIN OK"`. Lock trùng blob tại M. Revision 1252 đã thử qua capture thật. Ghi chú: bản ghim là **alpha**. |
| U11 Auth remote tới target VM | **not_evidenced**: auth **không** được thực thi, kể cả status | — | `G1-handoff-result.json` `05814804…`: `"real_VM_WinRM_auth": "not_measured"`, `"webapp_credentials_supplied": false`. `native-canary-result.json`: `"scope": "...source verification and real gateway auth are separate measured steps."` Target của P3 là `ASUS-LAPTOP` (cục bộ). Raw không có transcript Desktop Commander, không có phiên WinRM/PSSession, không có status. |

## 3. Đối chiếu lời khai công khai P3

| # | Lời khai | Kết luận | Căn cứ |
|---|---|---|---|
| 1 | PS51/PS7 mỗi bản 4 bước capture, tất cả rc 0 | **supported** | `ps51-flow.stdout`, `ps7-flow.stdout`, `flow-*/terminal.json` (`65ef32b6…`, `ff6c483c…`), `literal-steps.json`, `measurement.csv` `4,4,0,0`. Lưu ý: stderr của PS5.1 không rỗng (CLIXML progress, Write-Host của probe git, npm notice) dù rc 0. |
| 2 | Cùng nguồn ghim M | **supported** | Mọi dòng đều `candidate b0b5480…` và `source_sha256 1799c2bd…`. Reviewer tự tính lại: SKILL.md, 5 fragment, lock, package.json tại M đều khớp. `repo\` HEAD/tree = M, không shallow. Script setup đã bind chỉ khác fragment 0 ở 4 dòng placeholder; `-EncodedCommand` giải ra trùng từng byte `.ps1` trong zip (8/8). |
| 3 | Chuỗi capture URL/redirect/final URL/body bytes/hash/time/PNG/PDF → G1 gốc thật | **supported** | `04-requests.json`: `"1. [GET] http://127.0.0.1:52930/redirect => [302] Found\n2. [GET] http://127.0.0.1:52930/source.html => [200] OK"`. `03-tab-list.json`: final URL. `captures.json` (`60b5cc82…`, `6b89acfe…`). `source.body` ps51 `34d29f48…` (198 B), ps7 `4a2d6991…` (197 B). Reviewer dựng lại body từ template của `literal_flow.py` thì ra đúng sha. Thời gian lấy từ `commands.tsv` (rc và mốc giờ từng lệnh). G1: `captured_input_sha256` bằng sha của body; `content_md5` `d210dad6…` / `3468743d…` bằng md5 body reviewer tự tính. "G1 gốc" là `repo\scripts\tl.py` tại M. |
| 4 | ZIP gốc 118 entry, CRC, 117 digest | **supported** | Mục 1. |
| 5 | PNG body 1280x720, marker PDF được parse lại | **supported** | Reviewer parse lại độc lập: cả hai PNG có signature, IHDR `(1280, 720)`, IEND. Cả hai PDF có `%PDF-1.4…%%EOF`, 1 trang; giải mã ToUnicode ra `controlled-source-wp1297-M-ps51TEST FIXTURE ONLY. So: 10/2026/TT-BYT` (bản ps7 tương ứng). |
| 6 | G1: 6 đối chứng dương/âm, chỉ là fixture có kiểm soát, không phải xác minh pháp lý | **supported** | 6 dòng: matching-header rc 0 ×2, wrong-header rc 1 với `source_discrepancy: true` ×2, missing-body rc 2 ×2 (stderr `5824218b…`: `No such file or directory`). Trường scope ghi nguyên văn: *"G1 checks content/header and returns discovery links; it does not perform multi-source legal verification and is not authority to publish a legal quotation."* |
| 7 | Chặn 6 ca native trước đó bằng tương đương byte của 4 module | **not supported (bởi raw P3)** | Zip và manifest chỉ chứa **1/4** module (`literal_flow.py` `a90c410c…`). `native_flow.py` `46be9f65…` (được import làm `M`, chạy thật), `native_observer.py` `562d55dc…` và `contract.py` `edb3d772…` chỉ nằm trên đĩa và trong `operator-upload.json`. Không có bản ghi nào về "6 ca trước" hay băm module của chúng; grep kho (ngoài r1) cũng không thấy 4 băm này. |
| 8 | selected_remote: thực thi thật trên target DC đã được cấp quyền, kèm 4 status/WhatIf | **not supported** | Raw P3 không có status hay WhatIf nào, không có Proxima. Target là `ASUS-LAPTOP` cục bộ. Raw tự ghi `real_VM_WinRM_auth: not_measured`. Không có transcript Desktop Commander. |
| 9 | Config/metadata không đổi | **partly** | Có đo: `verify_handoff.py` assert `git status --porcelain` rỗng trước và sau. Thư mục `TL_STATE_DIR` (`G1-handoff\state`) không được tạo (liệt kê 18/11). Không đo: `no_service_or_profile_change: true` và `new_product_source_changed: false` là hằng trong `bootstrap_native.py`; không có snapshot trước/sau nào của config hay metadata Proxima. |
| 10 | Cleanup: 0 process sở hữu, lock đã nhả | **supported** | `terminal.json`: `"owned_live": 0`, `"lock_released": true`. Giá trị này tính bằng `M.observe()` sau cleanup và bằng cách đọc lại tệp lock. `08-close.json` `f5de0e37…`: `"status": "closed"`. `09-delete-data.json` `beb9230b…`: `"deleted": false` (spec chấp nhận). `10-verify.json` `8fe18053…`: `"The browser 'tl-pw-2d8fea678fd5' is not open, please run open first"`, rc 1 như mong đợi. Mỗi addon chỉ còn 1 thư mục run; `work\` rỗng. |

## 4. Thứ trông giống credential/token/cookie (chỉ báo có hay không)
- **Không thấy** giá trị credential, token, cookie hay khoá nào trong 118 entry.
- Các chỗ khớp mẫu đều không phải bí mật:
  - tên mẫu trong bộ lọc env (`TOKEN`, `SECRET`, `PASSWORD`, `API_KEY`) của `literal_flow.py`, `verify_handoff.py`, `bootstrap_native.py`;
  - `PublicKeyToken` của assembly .NET trong CLIXML stderr;
  - tên khoá `webapp_credentials_supplied`.
- Có **một Google Drive file id** (định danh tệp registry, không phải credential) trong `G1-handoff-result.json` và `G1-handoff/*-matching-header.stdout`. Không trích ở đây.
- Tên user Windows chỉ xuất hiện đúng như tiền tố đường dẫn đã cho (191 lần, cộng `<máy>\<user>` trong CLIXML). Không có user khác.

## 5. Phát hiện

**P1:** không có.

**P2**
- **F1. Lời khai 8 không có trong raw P3.** "selected_remote actual authorized DC target execution and 4 status/WhatIf" không có bằng chứng nào trong P3, và raw còn tự khai `real_VM_WinRM_auth: not_measured`. MATRIX không được dùng P3 làm nguồn cho §11 #2 (phần remote), #3, U3 và U11. Phải trỏ sang raw khác, có thể là P5, hoặc gỡ lời khai.
- **F2. Lời khai 7 không có trong raw P3, và gói đóng băng không bind đủ mã đã chạy.** Ba trong bốn module operator đã thực thi (`native_flow.py`, `native_observer.py`, `contract.py`) nằm ngoài zip và manifest. Hiện chỉ trên đĩa ASUS, hoặc dạng base64 trong `operator-upload.json`, cũng ngoài zip.
- **F3. Các cờ "no_*" là hằng, không phải phép đo.** Gồm `no_inference`, `new_inference_calls: 0`, `no_service_or_profile_change`, `new_product_source_changed`, `webapp_credentials_supplied`. Không được tính cho §11 #11 hay #3, cũng không cho lời khai 9.

**P3**
- **F4.** Cache trình duyệt được seed bằng cách chép từ một lượt trước; chỉ băm `chrome.exe`. Thư mục nguồn của cache, runtime node và wheel pypdf (`D:\tl-win\wp1287-r24-asus-*`) ngày 18/11 không còn trên host, nên không đối chiếu lại được.
- **F5.** `npm` vẫn in `"New major version of npm available! 11.20.0 -> 12.2.2"` dù đã đặt `NO_UPDATE_NOTIFIER=1`. Tức là có thêm một lượt gọi registry; không gây mutation.
- **F6.** Bản ghim Playwright là alpha (`1.65.0-alpha-2026-10-30`), lệch ứng viên `v1.64.1` ghi trong P0. Cần một quyết định chính sách thành văn.
- **F7.** G1 coi một trang fixture bịa ra, chỉ chứa `So: 10/2026/TT-BYT`, là khớp với một mục registry thật (`drive_id` khác null, `source_discrepancy: false`). Điều này đúng như scope đã khai, nhưng xác nhận G1 chỉ là cổng so header. Không bao giờ được dùng G1 làm cổng xác thực.
- **F8.** Truy vết: `measurement.csv` gắn nhãn `wp1287-r22-*`/`wp1287` cho lượt P3 (WP1297). `native_flow.acquire` ghi cứng `DESKTOP-T9R33P2` và bị `literal_flow` thay bằng hàm khác khi chạy trên ASUS; bản thay này không đọc lại lock sau khi ghi. Gói ghi ngày 12/11 06:29Z, còn con trỏ gọi là "raw cuối 13/11"; chỉ bản `.b64` mang ngày 13/11.

## 6. Phạm vi duyệt được (nếu F1–F3 được xử lý trong bản chiếu và MATRIX)
`approve_scoped` cho các phần sau:
- toàn vẹn gói;
- lời khai 1–6 và 10;
- §11 #4 (trong zip);
- U10 (ASUS, PS5.1 + PS7);
- capture fixture Playwright trên PS5.1 + PS7 (`real_os`, nhưng fixture là localhost).

Những phần sau giữ nguyên `partial` hoặc `not_evidenced` như bảng ở mục 2: §11 #1, #2, #3, #5, #11, U1, U3, U11.

## 7. Giới hạn
- Chỉ đọc. Thao tác trên host gồm:
  - `certutil`, `Get-ChildItem` và `Test-Path` trên đúng các đường dẫn được giao;
  - đọc entry zip trong bộ nhớ, bằng PowerShell 5.1 (`System.IO.Compression`) và Python `C:\Python313\python.exe -I -B -X utf8`, mã nạp qua stdin, không ghi tệp, không giải nén ra đĩa;
  - `git rev-parse` trong `repo\`, chỉ đọc.
- Không chạy test, không khởi động hay dừng tiến trình sản phẩm, không mở profile hay cache trình duyệt. Riêng `chrome.exe` chỉ được băm và đọc VersionInfo.
- Python trên host là thêm vào ngoài cách PowerShell được gợi ý, dùng cho CRC và parse PDF. Không dùng pypdf vì wheel đã mất; reviewer tự giải mã ToUnicode.
- Không xác minh được độc lập rằng lượt chạy 12/11 thật sự đi qua Desktop Commander, và không đo được lưu lượng mạng của `tl.py source-verify`.
- Thư mục P3 trên đĩa (khoảng 14,5k tệp) không quét đệ quy. Chỉ đọc top-level, `G1-handoff\`, `flow-ps51\`, `runs\`, `browsers\` và `work\` của hai addon.

## 8. Model và effort quan sát được
- Model: tự khai từ system prompt là `claude-opus-5-5` (Opus 5.5). Không đo được độc lập: `KHONG_do_duoc`.
- Effort: `KHONG_do_duoc`.

---
sha256 bản gốc của reviewer: `83f91ad915b69272284a9418712d0b47fbcff1e3fe02e37d9adb2104bff55a1b` (chép nguyên văn).
