# WP1319 r3 — VERDICT review độc lập (chỉ đọc)

verdict: approve_scoped

Phạm vi được duyệt: bốn bước R3-N3, R3-N5, R3-N6, R3-N7 của `ops/specs/wp1319-r3.md` (sha256 `77a6f24b314b65e88c53032b7a71bbeada15311d874984057e1e199e8fa2bf85`, khớp `spec_hash` của lease `wp1319-r3-g1-operator`), đo trên Desktop `DESKTOP-T9R33P2` tại master `13bf69f6eb797e859619a2062e7c9577e6a9cc0b`. Duyệt này không mở rộng sang N1, N2, N4 (r3 không chạy lại chúng) và không mở rộng sang những gì liệt kê ở mục 5.

- Reviewer: Claude, lượt review độc lập, chỉ đọc, context mới.
- Model/effort quan sát được: model `claude-opus-5-5` (do system prompt khai, không có `run.json` đo độc lập) · effort: **KHONG_do_duoc**.
- Cách đọc: Desktop Commander, `pwsh` 7.6.10 trên host. Tôi chỉ dùng lệnh đọc, liệt kê, băm, và `git --no-optional-locks status`. Tôi không chạy test, không chạy mã sản phẩm, không giải nén ra đĩa (đọc entry zip trong bộ nhớ), không gọi mạng, không gọi model, không ghi gì lên host hay GitHub. Lệnh ngoài danh mục đọc duy nhất là `python --version`, để ghi phiên bản trình thông dịch đã chạy bộ quét.
- Tôi tự rút kết luận từ raw. Tôi **không** đọc `r1/RESULTS.md` và không đọc bản tóm tắt nào của operator r3. Dòng `C:\tl-win\do-luong.csv` của r3 chỉ được dùng để xác nhận nó có tồn tại.

## 1. Toàn vẹn

| Kiểm | Kết quả |
|---|---|
| sha256 `freeze\wp1319-r3-evidence.zip` (262 574 byte, mtime 09:34:14Z) | `ad9a8a6ea3af924c608ab7381218a370d4c32cc053c595fb36d362cf2fd8fbaf`. Khớp lời khai và khớp tệp `.zip.sha256` |
| `freeze\evidence` so với `MANIFEST.json` (sha256 `c84c70d61c01bdccb96f2ebbc3e5dd75ce36c9ce869e70b09824be6214ab8429`) | 80 mục / 80 khớp size + sha256, 0 thiếu. Tệp thừa duy nhất là chính `MANIFEST.json` |
| Entry trong zip (đọc trong bộ nhớ) so với tệp trên đĩa | 81 entry, đều có tiền tố `evidence/`. 81/81 trùng byte, 0 thiếu |
| `W3\evidence` (37 tệp) so với bản đóng băng | 37/37 trùng byte |
| `W3\*.ps1` (11 script) so với `freeze\evidence\scripts\` | 11/11 trùng sha256. Các driver đọc script từ `W3\`, nên bản đóng băng đúng là bản đã chạy |
| `N5-runs\…\SHA256SUMS.csv` (lập lúc Cleanup) so với tệp đóng băng | 28/28 khớp. `pw\runs` trên host (29 tệp) trùng byte bản đóng băng |
| `MANIFEST.json`: `measured_sha` | `13bf69f6eb797e859619a2062e7c9577e6a9cc0b` |

**P1 về toàn vẹn: 0.** Lưu ý về số đếm: zip có **81** entry, tức 80 mục MANIFEST cộng chính `MANIFEST.json`. Lời khai "80 tệp kể cả MANIFEST.json" lệch 1 (P3-7).

## 2. Kết luận từng bước (tự rút từ raw)

### R3-N3: passed

- HEAD:
  - `R3-N3-progress.log` ghi `O3 head=13bf69f6eb797e859619a2062e7c9577e6a9cc0b` (08:58:54Z) và `O1 head=13bf69f6eb797e859619a2062e7c9577e6a9cc0b` (09:16:41Z). Script `throw "HEAD lech"` nếu khác.
  - Script **không** kiểm `git status`. Tôi đo sau lượt chạy, bằng `git --no-optional-locks status --porcelain`:
    - O3: 0 dòng.
    - O1: đúng 3 dòng `D .agents/skills/playwright-browser/*`.
    - O2: đúng 9 dòng `D .agents/skills/proxima-control/*`.
    - Cả ba có tree `a4cb90571c5432ad97d62fd7409b45147acf6c2a`.
  - Như vậy khớp đặc tả, nhưng là đo sau, không phải đo trước (P3-1).
- Tham số: `scripts/R3-N3.ps1` (`66f6cb5be14f2a3dc5c64c889ca01bc6e806705d53648bb698e9a6cda1669dc1`):
  - Thêm `-Counterexamples` **vô điều kiện** cho cả ba harness.
  - Thêm `-EvidenceRoot … -TestCulture tr-TR` khi `$h -ne 'Manifest'`.
  - Đặt `$env:PSModulePath` = giá trị Machine trước khi gọi tiến trình con.
  - Harness chạy từ bản sao `W3\tests-O1` / `W3\tests-O3`, scratch ở `W3\scratch\<tag>`, tức ngoài cây kho.
- Manifest không có `-TestCulture`:
  - Tôi đã kiểm `param()` của `ProximaManifest.Tests.ps1` @13bf69f6: chỉ có `AddonRoot`, `ScratchRoot`, `ReportPath`, `[switch]Counterexamples`.
  - Điều này được ghi ở dòng chú thích đầu `R3-N3.ps1`.
- 12/12 rc 0 (progress log). Không có tag nào chạy hai lần.

| Lượt | total / passed / failed / unavailable | test_culture (requested → thực) | CX | Marker log | sha256 log · report |
|---|---|---|---|---|---|
| O3 ps51 Manifest | 12 / 12 / `failed_ids=[]` / — | không có tham số (`culture=en-AU`) | 5 (4 KILLED + 1 CONTROL_PASSED) | `RESULT 12/12 passed; failed_ids=[]; setup_error_ids=[]; manifest=present; skill=present; setup_error=; evidence=ok; rc=0` | `3f8489fa376274d038ad25f09eee51f3c6de5d7a0000d561b9a9399df37be3d0` · `42ca9a5ca858bfb32f8d0b77b3aa4b3ed6a0618775c28912f0262fc6836c70a5` |
| O3 ps51 Config | 46 / 46 / 0 / 3 | tr-TR → tr-TR (`lower(I)=U+0131`) | 25 bằng chứng: 23 KILLED + `CONTROL_NO_CREDIT` + `CLEANUP_FAILURE_REPORTED`. `CX-cultural-reserved-device` credited=True | `RESULT 46/46 passed; failed_ids=[]; setup_error_ids=[]; unavailable_ids=[A3-07,A3-08,CX-ignore-mount-topology]; api_state=present; setup_error=; cleanup=ok []; rc=0` | `107e93bf6a7d9fceace7059237c754874136bbbbe5e4d4a2fc21808412262ffd` · `457349a6017503dfe9cc947672d272dde2657881d96fc23168e5c1c426d779c6` |
| O3 ps51 Control | 38 / 38 / 0 / — | tr-TR → tr-TR | 12 (11 KILLED + 1 CONTROL_PASSED), `primitives_replaced=10/10 asserted before any product call` | `RESULT 38/38 passed; failed_ids=[]; setup_error_ids=[]; api_state=present; setup_error=; cleanup=ok []; rc=0` | `f80ec13485beb1df720456adec7d7a09da6fb5b2b892ab0fe9a8db13ae9e94e9` · `37f3b5710f66f6eb7b6e9fe53188f8cda18bd631bf6f2535a5c97e7548917e89` |
| O3 ps7 Manifest | 12 / 12 / [] / — | không có tham số | 5 (4+1) | như trên | `3f8489fa…` (trùng byte) · `77e6a5066e61c76c25931e0e78f65c86a8738c08c4174a0eec88948d4545f9fd` |
| O3 ps7 Config | 46 / 46 / 0 / 3 | tr-TR → tr-TR | 23 KILLED (+2 không credit theo thiết kế) | như trên | `107e93bf…` (trùng byte) · `c36affaeb1cdb898b1cd43304a5bdba7d6455149c26f0f6f06ce456c08346fbf` |
| O3 ps7 Control | 38 / 38 / 0 / — | tr-TR → tr-TR | 12 (11+1) | như trên | `6ce5a57a2216099a801809fc48d7b2981b3c45f7984b827be6d0237f514b0ee5` · `0ad01b482bc6be26594136e916c94bd6a4fc0dce156c0565ff91d64edfa3afeb` |
| O1 ps51 Manifest | 12 / 12 / [] / — | không có tham số | 5 (4+1) | như trên | `3f8489fa…` · `5ac7eb669031f041f4ae81ab11c357ef68e55b5cf1aef2ce796e4e93c6aa9cb4` |
| O1 ps51 Config | 46 / 46 / 0 / 3 | tr-TR → tr-TR | 23 KILLED | như trên | `107e93bf…` · `dcde13281698a1f875facb26fc53787939a656985467bfb203cb2d11ae4982e2` |
| O1 ps51 Control | 38 / 38 / 0 / — | tr-TR → tr-TR | 12 (11+1) | như trên | `687bcdc8b16b890cda0eb8d1982ed7335f6ff794584e3d66562d78d1c2279d04` · `d5bf42457409d65f6266e52ac2fa573e630f3d108f44b842b8c97f53c1a9f9bb` |
| O1 ps7 Manifest | 12 / 12 / [] / — | không có tham số | 5 (4+1) | như trên | `3f8489fa…` · `37eb71cdf7af25eb88eef4b09ccb10d6b8e0f176fb8e8c816150c69d69052010` |
| O1 ps7 Config | 46 / 46 / 0 / 3 | tr-TR → tr-TR | 23 KILLED | như trên | `107e93bf…` · `9ea8df80d807bbcca8f638408b8f1c0dae5b433174df0041d8a160f346299dd1` |
| O1 ps7 Control | 38 / 38 / 0 / — | tr-TR → tr-TR | 12 (11+1) | như trên | `13a862657ff4f8b4dde2bf997f99a968475e6ebdefc9c31571456ebdd45d04a5` · `ee0b3b286c20ca8acef1bd2c44148d8db99ee621247c71b1e9ff3d7ccdc80fba` |

- `ps_version` trong report: `5.1.26100.9711` / Desktop và `7.6.10` / Core.
- `R3-N3-progress.log`: `3329054882d84e9c82db952f073ffe4013a088a557f64d3208740428559eb31f`.
- Băm trong report so với blob @13bf69f6. Tôi tính sha256 trên nội dung `git show 13bf69f6:<path>` tại kho cục bộ, và cả 12 report đều khớp:

  | Trường trong report | sha256 | Tệp tại 13bf69f6 |
  |---|---|---|
  | `harness_sha256` (Manifest) | `fdc107fa980435d3e11789a621a7848c34f3943b33dc500bbc12cf097322658e` | `tests/ProximaManifest.Tests.ps1` |
  | `harness_sha256` (Config) | `ee3bc46e89cadbba56373570c6aa4ae244e997e7789240f0f1e25c5ac0031ded` | `tests/ProximaConfig.Tests.ps1` |
  | `harness_sha256` (Control) | `75b565e50cebf73f2a1a8a9787e0b8d35fe239db928253ba5c66fcde7ee1121b` | `tests/ProximaControl.Tests.ps1` |
  | `module_sha256` / `config_module_sha256` | `59abfa860e59af7c596a9e3f60829f8dc1af4a853c5d4ac197c00cc033d76e7d` | `scripts/ProximaConfig.psm1` |
  | `module_sha256` (Control) | `527734a060678f11c95b91c84a36b147f9f5faba0de4a0ff60e8874576f4f668` | `scripts/ProximaControl.psm1` |
  | `wrapper_sha256` | `03f99881494329cea213714b5e603d83776a7fb57bb153e1a4431d4acc479354` | `scripts/Run-Px.ps1` |
  | `sample_sha256` | `ddc7a15c729c579ec0d068912a8880da5ad4c0ed6e9826ba1ba60088abe1fa92` | `config.example.json` |

  Bản sao trong `W3\tests-O1` và `W3\tests-O3` cũng có đúng ba băm harness ở trên. Report Control còn ghi `git_head=13bf69f6…` và `git_tree=a4cb9057…`.
- Đọc kết quả:
  - Config log trùng byte ở cả bốn lượt (`107e93bf…`, cũng trùng log N3D của r1). Manifest log trùng byte ở cả bốn lượt.
  - Đúng ca từng làm r1 rc 1 (`CX-cultural-reserved-device`, en-US) nay **KILLED, credited=True** dưới tr-TR, ở cả O1 lẫn O3, cả PS5.1 lẫn PS7.
  - Riêng Manifest, report **không có trường `failed`**. Tôi dùng `failed_ids=[]` và `passed == total` thay cho nó (P3-6).

### R3-N5: passed (O2 add-on, pwsh 7)

- `N5-setup.out` (`f66861022a8e692b6e9f68b6023e37ad38372420db3068763e5d070085ca8d93`, 6 390 byte) có raw output của tiến trình native. `Start-Transcript` không bắt được loại output này, nên sự có mặt của nó cho thấy stdout đã được chuyển hướng ở mức tiến trình. Các dòng nguyên văn:
  - `fatal: not a git repository (or any of the parent directories): .git`. Đây là marker **dương** của chốt "TL_PW_ROOT ngoài Git" trong khối Setup, vì khối đòi `gitRc 128` cộng đúng chuỗi này.
  - `added 3 packages in 4s` (`npm ci`)
  - `audited 3 packages in 5s`
  - `3 packages have verified registry signatures`
  - `3 packages have verified attestations`
  - `Chrome for Testing 157.0.8103.15 (playwright chromium v1252) downloaded to …\wp1319-r3\pw\browsers\0.1.0\chromium-1252`. Thêm FFmpeg v1013 và Winldd v1007.
  - `SETUP OK`
  - Không có dòng `invalid` hay `missing`.
- `N5-setup.err` (`3ce551806c1654fd446ab87e726d5a071283526c1af03e59df5bb89805c6b372`, 209 byte) chỉ chứa `npm notice New major version of npm available! 11.20.0 -> 12.2.3`.
- Đối chứng ngoài zip, trên host:
  - `pw\npm-cache\_logs\2026-11-18T08_58_56_740Z-debug-0.log` (`96e75815…`): `verbose title npm ci`, đúng argv `--prefix …\install\0.1.0 --userconfig …\npmrc-empty --cache …\npm-cache --registry https://registry.npmjs.org/ ci --ignore-scripts --no-audit --no-fund`, `verbose exit 0`, `info ok`.
  - `…08_59_01_310Z-debug-0.log` (`1c397129…`): `verbose title npm audit signatures`, `verbose exit 0`, `info ok`.
  - Cả hai log ghi `node v26.13.0`, `npm v11.20.0`.
- PIN: `00-pins.log` (`171b5f0d6d1310173f9da71269d25f1bb57aa4e4191f7957251764ea54dcb268`).
  - Nội dung: `target desktop-t9r33p2-wp1319-r3` · `node v26.13.0` · `npm 11.20.0` · `lock 0DA56E1E…` · `` `-- @playwright/cli@0.1.23 `` · `playwright(-core)@1.65.0-alpha-2026-10-30` · `cli 0.1.23` · `browser 157.0.8103.15`.
  - Dòng cuối là `PIN OK`.
- Capture (`commands.tsv` `e71e6363ba1c72088f6fc078484254f90e03d540097bdf00e9dedd74db0798c7`):
  - `01-open`…`09-delete-data` đều rc=0. `10-verify` rc=1, đúng mẫu SKILL.
  - `03-tab-list.json` (`db50fec4…`): `- 0: (current) [Example Domain](https://example.com/)`.
  - `04-requests.json` (`a273ed81…`): `1. [GET] https://example.com/ => [200]` và `2. [GET] https://example.com/s.js => [200]`.
  - Như vậy có đúng 1 dòng `(current)`, đúng 1 dòng 2xx mang URL cuối, nên IDX=1 đúng quy tắc SKILL. `N5-B-transcript` ghi `… idx=1`.
  - Tệp bắt được: `source.body` 577 byte `25ddf2c8…`, `page.png` `2e8ae4db…`, `page.pdf` `f30585e7…`.
- Cleanup:
  - `08-close.json` (`8e20ebee…`): `"status": "closed"`.
  - `09-delete-data.json` (`5e00df51…`): `"deleted": false`.
  - `10-verify.json` (`ff707808…`): `"isError": true`, `"error": "The browser 'tl-pw-8a31fc66b2a1' is not open, please run open first"`.
  - `N5-B.out` (`2908a44b…`): dòng cuối là `CLEANUP OK`.
- Đối chiếu khối SKILL. `SKILL.md` của `repo-O3` trên host có sha256 `1799c2bd…`, bằng blob @13bf69f6, và 0 CR. Tôi diff từng dòng các khối ở dòng 74–125, 148–165, 194–228, 248–258, 315–345 (bỏ dòng header của mỗi script):
  - `N5-2-pin.ps1` (`4af97452…`) và `N5-5-cleanup.ps1` (`a2dbe98c…`): **trùng khít**.
  - `N5-1-setup.ps1` (`5a0611b1…`): chỉ khác 4 dòng placeholder: `TL_PW_TARGET_ID='desktop-t9r33p2-wp1319-r3'`, `TL_PW_ROOT=W3\pw`, `TL_PW_NODE`/`TL_PW_NPM_CLI` = `C:\Program Files\nodejs\…`, `TL_PW_SRC=repo-O2\.agents\skills\playwright-browser`.
  - `N5-3-capture-a.ps1` (`78684699…`): chỉ khác `TL_PW_URL='https://example.com/'`.
  - `N5-4-capture-b.ps1` (`c0878b33…`): chỉ dòng `TL_PW_IDX` bị thay bằng chú thích, như đã khai.
  - Cả năm tệp 0 CR.
  - So với script r1 cùng tên: N5-2…5 trùng khít. N5-1 chỉ đổi TargetId (`…-r1` → `…-r3`) và `TL_PW_ROOT`.
  - Gói metadata: `package-lock.json` của O2 có `0da56e1e…` và `package.json` có `d52eb046…`, cả hai bằng blob @13bf69f6.
- Driver:
  - `N5-A3-driver.ps1` (`07366d6e…`): dot-source phần **trước** `& { $ErrorActionPreference = 'Stop'` của Setup (chỉ env và hàm, không cài lại). Tách Capture tại mốc chú thích `# Chạy khối Kiểm pin` có sẵn trong SKILL. Tee Pin vào `00-pins.log`. Lưu `N5-state.txt`. Bật Transcript.
  - `N5-B-driver.ps1` (`83b219c3…`): nạp lại env và hàm như trên, cùng `Invoke-PwGhi`. Đọc `N5-state.txt`, đặt `TL_PW_IDX` từ `-Idx`. Dot-source N5-4 rồi N5-5.
  - **Không driver nào thêm logic sản phẩm**: không lệnh CLI nào, không parser, không nới chốt.
- Chỉ có một thư mục run, một thư mục phiên `daemon\8330401853492c29`, và hai log npm (ci và audit). Vì vậy không thấy dấu vết lượt native thứ hai.

### R3-N6: passed theo tiêu chí r3, kèm finding F1

- `scripts/R3-N6.ps1` (`c4f31005…`) làm đúng mục "Gỡ bản cài" của SKILL:
  - Trước tiên kiểm tiến trình bằng `Get-CimInstance Win32_Process`, theo `CommandLine`/`ExecutablePath` khớp `W3\pw`, chỉ đọc. Còn tiến trình thì `throw`.
  - Sau đó `Remove-Item` đúng hai đường dẫn. Không `npm uninstall -g`, không đụng lõi.
- `R3-N6-progress.log` (`2c3f9a468b289d6c341aa431f7396cc391f2630350b31941c0163f39ce8d9123`):
  - `processes_using_install=0`
  - `lock_installed=0DA56E1E… lock_O3=0DA56E1E… equal=True`
  - `removed …\wp1319-r3\pw\install\0.1.0 exists_after=False`
  - `removed …\wp1319-r3\pw\browsers\0.1.0 exists_after=False`
  - `kept runs=True npm-cache=True`
  - `home_playwright_cfg=False`
  - `R3-N6 DONE`
- Tôi đo lại trên host bây giờ, chỉ đọc:
  - `pw\install` chỉ còn `0.1.0.lock.sha256` (64 byte). `pw\browsers` và `pw\work` rỗng. `pw\runs` còn run `20261118T090027Z-tl-pw-8a31fc66b2a1`.
  - `npm-cache` còn 28 tệp / 40 075 698 byte, gồm 2 debug log npm.
  - `npmrc-empty` và `TARGET_ID` còn.
  - Không còn tiến trình nào ngoài tiến trình đo của chính tôi.
- **F1 (finding đo lường, không phải tiêu chí PASS)**: `ms_playwright_before=26 after=28 changed_or_new=3`.
  - Mới: `%LOCALAPPDATA%\ms-playwright\daemon\8330401853492c29` (DIR).
  - Mới: `…\daemon\8330401853492c29\tl-pw-8a31fc66b2a1.err` (0 byte).
  - Đổi: mtime của `…\daemon` (00:25:15Z → 09:00:30Z).
  - `ms-playwright\b` không đổi.
  - Tệp đo: `N6-ms-playwright-before.txt` (`efce0c95…`, ghi 08:58:54Z, **trước** `npm ci` lúc 08:58:56Z) và `N6-ms-playwright-after.txt` (`f5a32bbb…`).
  - Cleanup và "Gỡ bản cài" của SKILL để lại mục sổ phiên này. Mục Limits của SKILL có khai vị trí `%LOCALAPPDATA%\ms-playwright\daemon`, nhưng không có bước nào dọn nó.

### R3-N7: passed

- `N7-secret-scan.json` (`bc311dfa…`):
  - `"scanner": "repo-O3/scripts/pkg_secret_scan.py"`
  - `"scanner_sha256": "fbf9392b4db5ee0726d871c87d1639a8e665d5547a222fe53b181857bda46083"`, bằng `expected_sha256`. Tôi băm lại tệp trên host và băm blob @13bf69f6: cả hai bằng.
  - `"rc": 0`
  - `"target": "evidence (truoc khi ghi MANIFEST)"`
- `freeze\scan.out` và `freeze\scan.err` đều 0 byte, ghi lúc 09:34:13Z. Trường `stdout`/`stderr` = `null` là vì `Get-Content -Raw` trả `$null` trên tệp rỗng, không phải dữ liệu bị mất.
- Đối tượng quét là `freeze\evidence` sau khi copy, gồm cả `scripts\` và `N5-runs\`. Bộ quét **không** phủ `MANIFEST.json` và chính `N7-secret-scan.json`, vì hai tệp này được ghi sau. Zip được tạo sau đó, lúc 09:34:14Z.
- Python của host: 3.12.10.
- Quét bổ sung của tôi, chỉ đọc, trên toàn bộ 81 tệp kể cả MANIFEST: **0** khớp với 15 mẫu (`gh*_`, `github_pat_`, `sk-`, `AKIA`, `xox?-`, `GOCSPX-`, `AIza`, `PRIVATE KEY`, JWT, `1//0`, `Bearer`, `authorization:`, `cookie:`, `password[:=]`, `AKfycb`).
- Transcript các pha có trong gói: `N5-A/B-transcript`, `N5-setup.out/.err`, `N5-B.out/.err`, `R3-N3-progress`, `R3-N3.driver.out/.err` (0 byte), `R3-N6-progress`.

## 3. Giải quyết các finding của r1

| Finding r1 | Trạng thái ở r3 | Căn cứ |
|---|---|---|
| N3 failed (F3): Config + CX dưới en-US luôn rc 1 vì `cultural-reserved-device` không được credit | **Giải quyết** theo đặc tả r3 (tr-TR) | 4/4 Config `46/46 … rc=0`, `CX-cultural-reserved-device` KILLED, credited=True. Ghi chú: r3 **đổi** culture chứ không chứng minh en-US. Dưới en-US ca này vẫn "no credit" theo thiết kế harness |
| F2: O1 chạy không có `-Counterexamples` | **Giải quyết** | `R3-N3.ps1` thêm `-Counterexamples` vô điều kiện. Report O1 có 25 / 12 / 5 bằng chứng CX |
| F4: N3D ngoài đặc tả, chạy sau rc 1 | **Không còn áp dụng** | r3 có 12 lượt, mỗi tag 1 lần, không lượt bổ sung |
| F5: N5 khai "3/3 chữ ký + 3/3 attestation" không có raw | **Giải quyết** | `N5-setup.out` có nguyên văn `3 packages have verified registry signatures` và `3 packages have verified attestations`. Debug log npm `exit 0` đối chứng |
| N6 failed (F1 của r1): `ms-playwright` đổi, `W\pw` không xoá | **Giải quyết theo tiêu chí r3** (SKILL "Gỡ bản cài") | Xoá đúng 2 đường dẫn, giữ `runs` và `npm-cache`, 0 tiến trình. Delta `ms-playwright` được ghi đúng vai finding (F1 ở trên). Tiêu chí r1 "ms-playwright không đổi" vẫn **không** đạt: đó là đặc điểm của add-on, đặc tả r3 hạ nó xuống thành phép đo |
| F6: rc quét secret không được lưu | **Giải quyết** | `N7-secret-scan.json` `"rc": 0`, kèm băm bộ quét = `fbf9392b…` |
| F9: không chạy khối Kiểm pin trên O3 | Không xử lý (r3 không đòi) | Vẫn chỉ có `lock_installed = lock_O3` ở N6 |
| F10: playwright chỉ trên PS7 | Không xử lý (r3 chỉ định pwsh 7) | — |
| F12: thiếu nguồn gốc lệnh | **Một phần** | Script N3/N6/N7/heartbeat đã đóng băng. Vẫn thiếu lệnh sinh `N6-ms-playwright-before.txt` và lệnh khởi chạy Setup (P3-2) |
| F13: khoá / kiểm tải / sổ đo không có raw | **Một phần** | `lock-heartbeat.ps1` đã đóng băng. Hai `KHOA.txt` rỗng, mtime 09:34:32Z. Sổ `C:\tl-win\do-luong.csv` có 1 dòng r3 ghi 09:34:32Z, tức sau zip. Không có dòng `TAI_TRUOC`, không có raw lấy khoá trong gói (P3-3) |
| F15: bằng chứng con của CX không đóng băng | Không xử lý | `W3\scratch`: 2 364 tệp / 22 163 348 byte, ngoài gói |
| F16: riêng tư | **Cải thiện** | Tên tài khoản Windows chỉ còn ở header của 2 transcript (`N5-A`, `N5-B`). Hostname có ở 7 tệp |
| F14: đường Drive | Không thấy ở r3 | `W3` không có script upload nào |

## 4. Findings của lượt r3

### P1
Không có.

### P2
Không có.

### P3
- **P3-1. HEAD được kiểm trước khi chạy, `git status` thì không.** Đặc tả viết: "Các thay đổi chỉ được phép là phần add-on đã xoá… O3 phải sạch". `R3-N3.ps1` chỉ `rev-parse HEAD`. Trạng thái sạch/xoá-có-chủ-đích chỉ do tôi đo **sau** lượt chạy (O3 0 dòng, O1 3 dòng playwright, O2 9 dòng proxima). Kết quả khớp, nhưng không phải bằng chứng đóng băng của thời điểm trước khi chạy. HEAD của O2 (nguồn `TL_PW_SRC`) không được ghi trong r3. Tôi đo được `13bf69f6…`.
- **P3-2. Nguồn gốc lệnh còn hở ở hai chỗ.**
  - (a) Không có script hay transcript nào ghi lệnh khởi chạy Setup trong "tiến trình pwsh riêng". Tôi chỉ suy được từ hai dấu hiệu: raw output native có mặt trong `.out`, và cwd của npm là thư mục cài Desktop Commander. Phiên bản PowerShell của tiến trình Setup là **KHONG_do_duoc**. Đặc tả đòi "stdout+stderr … vào `N5-setup.out`", nhưng stderr nằm ở `N5-setup.err` riêng. Không mất dữ liệu: `.err` chỉ có npm notice.
  - (b) Không script nào sinh `N6-ms-playwright-before.txt`. `R3-N6.ps1` chỉ đọc nó. Định dạng khớp với tệp "after" và thời điểm 08:58:54Z hợp lý, nhưng lệnh chụp không có.
- **P3-3. Khoá, kiểm tải, chạy chồng (ADR-0057/0058/0059).**
  - Gói không có raw lấy khoá, nhịp tim, nhả khoá, cũng không có dòng kiểm tải `Win32_Process`.
  - Các pha chạy chồng: Setup N5 (08:58:56–08:59:53), N5-A (09:00:27–34), N5-B (09:01:50–53) và N6 (09:03:05) đều nằm trong lúc R3-N3 O3 ps51 Manifest/Config chạy (08:58:54–09:04:03).
  - ADR-0057 D1 cho thấy chạy chồng sinh **đỏ giả**, không sinh xanh giả. Config log của O3 (chạy chồng) và O1 (chạy riêng) trùng byte `107e93bf…`. Vì vậy tôi không thấy ảnh hưởng tới kết luận, nhưng đây là lệch không có raw giải thích.
- **P3-4. F1 là lỗ thật của add-on.** Cleanup và "Gỡ bản cài" không dọn `%LOCALAPPDATA%\ms-playwright\daemon\<hash>\<nonce>.err` cùng thư mục `<hash>`. Gỡ xong vẫn còn `install\0.1.0.lock.sha256` của revision đã xoá, `npmrc-empty`, `TARGET_ID`, và 40 MB `npm-cache`. SKILL không đòi xoá các mục này, nên đây không phải lỗi thực thi. Nó là đầu vào cho một quyết định sửa SKILL hoặc ghi nhận như đặc điểm.
- **P3-5. Nhãn cũ trong header script.** `N5-1…5` vẫn ghi `# wp1319 r1 N5 - trich NGUYEN VAN…`. `N5-B-driver.ps1` ghi `# wp1319 r1 N5 pha B`. Nội dung là r3: `W`, TargetId và ROOT đều là r3. Tên `N5-A3-driver` gợi ý có phiên bản trước. Không có dấu vết lượt chạy thừa (một run, một phiên daemon, một cặp log npm), nhưng các lần thử A trước đó, nếu dừng trước khi tạo run, thì **KHONG_do_duoc**. `Start-Transcript` không có `-Append` nên sẽ ghi đè.
- **P3-6. Tiêu chí "report có `failed` 0" không áp nguyên văn được cho Manifest**, vì schema `proxima_manifest_tests.v1` không có trường `failed`. Đọc tương đương: `failed_ids=[]`, `passed=12=total`, và log `RESULT 12/12 passed … rc=0`. Đặc tả nên ghi rõ cách đọc này.
- **P3-7. Số đếm tệp.** Gói có 80 mục MANIFEST cộng `MANIFEST.json`, tức 81 entry zip. Câu "80 tệp kể cả MANIFEST.json" lệch 1.
- **P3-8. Write set.** Đặc tả đóng băng ghi `ops/acceptance/wp1319/**`. Lease hiện tại thu hẹp xuống 3 tệp cụ thể, kèm `write_set_note_glob` (sửa ~09:40Z). Đó là tập con, nên không mâu thuẫn. Ghi lại để biết lease bị sửa sau khi cấp.

## 5. Giới hạn: r3 KHÔNG chứng minh

- **Gateway, WinRM, service thật, VM.**
  - Harness Control thay 10/10 primitive nguy hiểm bằng đồ giả (`primitives_replaced=10/10 asserted before any product call`).
  - Config dùng `config.example.json` (`ddc7a15c…`).
  - Không đăng nhập, không ACL, không LIVE.
- **Config + CX dưới en-US.** r3 chỉ đo tr-TR. Ca `CX-cultural-reserved-device` dưới en-US vẫn "no credit" theo thiết kế harness. Đặc tả r3 cố ý chọn tr-TR.
- **Ca VHD và 8.3.** `A3-07`, `A3-08`, `CX-ignore-mount-topology` là `unavailable` (không `-VhdFixture`, không có tên ngắn 8.3).
- **Bằng chứng con của CX.** Mutant, child report và output nằm ở `W3\scratch` ngoài gói. Tôi chỉ dựa vào lần tự kiểm `cleanup=ok` / `evidence=ok` của harness.
- **playwright-browser trên PS5.1, và Kiểm pin trên O3** bằng khối SKILL.
- **Xác minh pháp lý.** `example.com` chỉ là bản lưu nguồn. Không đo mạng ngoài những gì CLI ghi.
- **Việc đọc chỉ số request "bằng mắt" của người.** Tôi chỉ kiểm được rằng `Idx=1` khớp quy tắc SKILL trên raw.
- **N1, N2, N4.** r3 không chạy lại các bước này; kết quả r1 của chúng đứng nguyên theo verdict r1.
- **Tính trung thực của host.** Tôi tin `Get-FileHash`, `ZipFile` và `git` của host. Output console Desktop Commander của operator (lệnh Setup, lệnh chụp "before", lệnh khoá) là **KHONG_do_duoc**.

---
sha256 bản gốc của reviewer: `aec22dafb8659b19eff07f63b1bc20bbc2a105bbfb9e79305843793855fc9c24` (chép nguyên văn).
