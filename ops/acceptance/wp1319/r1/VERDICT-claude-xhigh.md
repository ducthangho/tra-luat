# WP1319 r1 — VERDICT review độc lập (chỉ đọc)

verdict: request_changes

- Reviewer: Claude, cross-review bổ sung theo §4 đặc tả ("Claude cross-review chỉ thêm khi khả dụng"). Lượt này KHÔNG thay lượt review Codex mà đặc tả chỉ định.
- Model/effort: model `claude-opus-5-5` (do system prompt của phiên khai, không có `run.json` đo độc lập) · effort: **KHONG_do_duoc** (ngữ cảnh có tham số `reasoning_effort=40`, nhưng tôi không kiểm được nó ứng với mức effort nào).
- Cách đọc: đọc tại chỗ trên Desktop `DESKTOP-T9R33P2` qua Desktop Commander, chỉ dùng lệnh đọc/băm/liệt kê (pwsh 7.6.10). Không chạy test, không ghi gì lên máy, không gọi mạng. Bảy script N5 được kéo về nguyên byte (base64) để diff. Trước khi diff, tôi khớp sha256 của chúng với MANIFEST.
- Tôi tự rút kết luận từng bước từ raw **trước**, rồi mới đọc `RESULTS.md` và `MATRIX.md`.

## 0. Toàn vẹn và neo

| Kiểm | Kết quả |
|---|---|
| sha256 đặc tả `ops/specs/wp1319-r1.md` | `deee1b43fffeae178733ff948847f05ac506976964823a9f33437635a9be42e3`. Khớp `spec_hash` của g1 và g2 |
| sha256 zip `freeze\wp1319-r1-evidence.zip` (365 726 byte) | `54506f1896a1e12d56e7d241a02179d5d75d65cc3255dd55d8aad70b5f8cf24a`. Khớp lời khai và khớp tệp `.zip.sha256` |
| `freeze\evidence` so với `MANIFEST.json` (131 mục) | 131/131 khớp size + sha256, 0 thiếu. Tệp thừa duy nhất là chính `MANIFEST.json` (`151925f3…`) |
| 132 entry trong zip (tiền tố `evidence/`) so với 132 tệp trên đĩa | 0 lệch byte, 0 thiếu |
| `W\evidence` (87 tệp) so với bản đóng băng | 87/87 có mặt trùng byte. Tệp mới nhất (`N6-ms-playwright-FINDING.txt`, 00:34:27Z) được ghi trước zip (00:34:29Z) |
| Tree của 13bf69f6 | `a4cb90571c5432ad97d62fd7409b45147acf6c2a`, khớp `N1-result.txt` |
| harness/module trong 14 report N3/N3D | Config `ee3bc46e…`, Control `75b565e5…`, Manifest `fdc107fa…`, `ProximaConfig.psm1` `59abfa86…`, `ProximaControl.psm1` `527734a0…`. Tất cả bằng blob LF tại 13bf69f6 (`eol=lf`) |

**P1 về toàn vẹn: 0.**

## 1. Kết luận từng bước (tự rút từ raw)

| Bước | Kết luận | Marker dương trích nguyên văn (hoặc marker âm) | Tệp nguồn | sha256 |
|---|---|---|---|---|
| N1 | **passed** | `head=13bf69f6eb797e859619a2062e7c9577e6a9cc0b` · `tree=a4cb90571c5432ad97d62fd7409b45147acf6c2a` · `status_lines=0` · `clone_rc=0` · `checkout_rc=0`. Tôi đối chiếu tree độc lập bằng `git rev-parse` | `N1-result.txt` | `c9a0489df4da4960737adcaa8bef653bb7bac34457192ebba85a65ec34e5cb59` |
| N2 | **passed** | `== tl selftest 1777/1777 ==` (dòng cuối, cả 4 log cùng băm) · `O0 selftest rc=0 seconds=314 marker=[== tl selftest 1777/1777 ==]`, tương tự O3/O1/O2 (317/319/315 s) · `static_refs=0` ×4. Tôi tự đếm bằng `git grep` tại 13bf69f6 cũng ra 0 | `N2-O{0,1,2,3}-selftest.log` · `N2-progress.log` | `655f2c83933f16e8a51079a1df907438d9259bc1ae94e8690de41d031c203df0` (×4) · `e642f5e8dc300166905cb650bb0705a339285b55f8d41e7ea5442ca934bdddcf` |
| N3 | **failed** (theo luật đặc tả "rc 1 = FAIL sản phẩm"; xem F3) | Âm: `RESULT 45/46 passed; failed_ids=[CX-cultural-reserved-device]; … cleanup=ok []; rc=1` trên **cả PS5.1 lẫn PS7** (O3 Config, en-US). Phần đạt: O3 Manifest `RESULT 12/12 passed; … rc=0`, O3 Control `RESULT 38/38 passed; … rc=0` (`prim_replaced=10/10 asserted before any product call`), O1 Manifest 7/7, Config 21/21, Control 26/26 rc 0, nhưng O1 **không** có `-Counterexamples` (F2) | `N3-O3-ps51-Config.log` · `N3-O3-ps7-Config.log` · `N3-O3-*-Manifest.log` · `N3-O3-ps51/ps7-Control.log` | `697de7be79e8791c002ee77f11f5628eadfcb8ea5668952586989356079ee679` · `1d7f745efd776b634beabdf1772db886a6502f0b97c7faa9fa01a9e4da39b864` · `3f8489fa376274d038ad25f09eee51f3c6de5d7a0000d561b9a9399df37be3d0` · `a3d8f5aac6e8de92b1a4d82d8288e5e859704a1f9c01918fbc47ac46791c054c` / `d58e8a05b9906df6bac66f404720843ceeb253329ea0d33ab0c46a64b74bc083` |
| N3D (bổ sung, ngoài đặc tả) | **passed**, chỉ là thông tin bổ sung, không thay N3 | `RESULT 46/46 passed; failed_ids=[]; setup_error_ids=[]; unavailable_ids=[A3-07,A3-08,CX-ignore-mount-topology]; api_state=present; setup_error=; cleanup=ok []; rc=0` (PS5.1 + PS7). Report ghi `test_culture=tr-TR` và `cx_credited=23/25` | `N3D-O3-ps51-Config-trTR.log` = `N3D-O3-ps7-Config-trTR.log` · report ps51 / ps7 | `107e93bf6a7d9fceace7059237c754874136bbbbe5e4d4a2fc21808412262ffd` · `9daefedd3cf56e533390c788cdc44395d0e317fadcde205064b5b7897e6d3c2d` / `fbc352b73be2f6b7ed1b07ea2f0b89a8d1a7592f563d8a398da77468923af732` |
| N4 | **passed**, chỉ trong phạm vi cấu hình mẫu | `What if: Performing the operation "status" on target "px target acc95f18bf75".` cùng `dryRun : True` · `dispatched : False` · `outcome : whatif` (restart và stop tương tự) · T1 `ProximaControl: operation rejected: ArgumentMissing.` · T2 `ProximaControl: operation rejected: TargetMismatch.` · `N4-ps51 snapshot_equal=True` · `N4-ps7 snapshot_equal=True` | `N4-ps51-W1-status-whatif.log` · `N4-ps51-W2-restart-whatif.log` · `N4-ps51-T1-no-target.log` · `N4-ps51-T2-wrong-target.log` · `N4-progress.log` · snapshot ×4 | `411d0f6470abe51d0ffc251150edf2c3eac8cee05e0954fe35d75b2f19ae8351` · `6158a08c226a3c51a5d13b5862f946dab28088668889e5f874fed15d1857e1cf` · `79a97e261588f68d2a9a499b7b9bbae51f45d292538f9e77f94d9d42f126eb06` · `4d9a52cd483ff71ecff7f2ee0af21edcbf3d87028750871a4ee31f395f21660b` · `8e11ec8e2d3f5088224c6d5aa7fa63fe460ee0f4b99c8cced3c3024861e33dbc` · `a1f58abf5756b24e08cbf66ad3aa5411c3b732b987d73c9b1833d78d9a45d0a0` (ps7: W1 `615fb5c7…`, W2 `0d6d2c78…`, W3 `18173bdc…`, T1 `e1797f5d…`, T2 `dedc8e45…`) |
| N5 | **passed** cho O2 trên pwsh 7. Bước con "O3 chỉ kiểm pin" là **not_run**: được thay bằng so băm lock (F9) | `SETUP OK` · `PIN OK` (dòng cuối `00-pins.log`; `node v26.13.0`, `npm 11.20.0`, `cli 0.1.23`, `browser 157.0.8103.15`) · `CLEANUP OK` · `"status": "closed"` · `"deleted": false` · `"error": "The browser 'tl-pw-316f64e80925' is not open, please run open first"` · `commands.tsv`: rc=0 ×9, `10-verify` rc=1 đúng mẫu · không còn tiến trình: `processes_using_install=0` (N6, ~4 phút sau Cleanup) | `N5-A-transcript.txt` · `N5-runs/…/00-pins.log` · `N5-B-transcript.txt` · `08-close.json` · `09-delete-data.json` · `10-verify.json` · `commands.tsv` | `90e2de10c2c7370322c7fc6f0154e418d9021c208852c59a1fd12b8301de6082` · `af72f585c85fa68c71206a077d73d4efd8d7c272bffe860d3bd67b9cd37f80f9` · `08b2f8309b371f19b1118ddca7540d4e76e8aa918e1ec74b2fb22f5250483284` · `f0dcd28f5861fa560814b3645b4df43ce4adc6aaf3c05da56d385a469ba5a0a2` · `e794ad9901aa67ae6bd8cb91172578fa02f20ba39bb35a2b3f519fb44de5e45b` · `338157755be0da914efce0e5ac3f006e8b7cb56c2b49a921b86637ac5c3ebbf2` · `08d4abc02cc789488ba9617c8ef11384f0268d6f4294325fcb382dc30c8a2973` |
| N6 | **failed** | Âm: `ms_playwright_unchanged=False before=11 after=12` (tiêu chí đặc tả "Kiểm LOCALAPPDATA\ms-playwright không đổi"). `W\pw` không bị xoá: còn `npm-cache` 28 tệp / 40 070 226 byte, `runs/`, `install\0.1.0.lock.sha256`, `npmrc-empty`, `TARGET_ID`, thư mục rỗng `browsers` và `work` (tôi liệt kê chỉ đọc trên host). Phần đạt: `removed …\pw\install\0.1.0 exists_after=False` · `removed …\pw\browsers\0.1.0 exists_after=False` · `processes_using_install=0` · `lock O2=0DA56E1E… O3=0DA56E1E… installed=0DA56E1E… equal=True` | `N6-progress.log` · `N6-ms-playwright-before.txt` / `-after.txt` / `-tree-after.txt` | `091eab4fe9fdb3434e84732ac2367f71b43373b1cd3ad213978373cb69e7fd80` · `cb41051f13f1d981b7718eff058e0c59d248462516453798b0c2fff79088a48a` / `4a9d3f2352d2c193b18d4be0c04e2a0e5220d7f68314b8bb2bddbb3b96dc25b3` / `be3043d8be6162d98f396b16f822b085300a3e9bd6b7e65b13f3d34d8c9f3a48` |
| N7 | **failed**: lỗi ở bằng chứng, không phải bắt được secret | Đạt: zip `54506f18…` và MANIFEST 131/131 (mục 0). Không đạt: quét `pkg_secret_scan.py` có `secret-scan.out` và `.err` **0 byte**, còn `secret_scan_rc` chỉ được in ra console của `N7-freeze.ps1`, không tệp nào giữ nó ⇒ không có marker dương. Not_run: commit "MANIFEST đã lọc" (kho chỉ có DESIGN, MATRIX, RESULTS, REVIEW-PROMPT). Quét độc lập của tôi: 0 secret (F6) | `freeze\secret-scan.out` · `freeze\secret-scan.err` · `scripts/N7-freeze.ps1` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (×2) · `276b44ea9ab4b2d61a28a969adb97fcd77e13d82ac2851bb64a5ce594b497695` |

### Đối chiếu khối SKILL N5
- Tôi tự trích 5 khối ```` ```powershell ```` của `.agents/skills/playwright-browser/SKILL.md` @13bf69f6 (blob `678ba2f0…`, sha256 `1799c2bd…`, khớp header các script) ở các dòng 73–126, 147–166, 193–229, 247–259, 314–346.
- Diff (bỏ dòng header chú thích đầu mỗi tệp):
  - `N5-2-pin.ps1` và `N5-5-cleanup.ps1`: **trùng khít**.
  - `N5-1-setup.ps1`: chỉ khác 4 dòng placeholder (`TL_PW_TARGET_ID`, `TL_PW_ROOT`, `TL_PW_NODE`, `TL_PW_NPM_CLI`, `TL_PW_SRC`).
  - `N5-3-capture-a.ps1`: chỉ khác `TL_PW_URL = 'https://example.com/'`.
  - `N5-4-capture-b.ps1`: chỉ dòng `TL_PW_IDX` bị thay bằng chú thích, đúng như đã khai.
  - Cả bảy tệp không có CR.
- **0 khác biệt ngoài placeholder.**
- `N5-A-driver.ps1` và `N5-B-driver.ps1` chỉ làm bốn việc: dot-source/tách khối tại mốc chú thích `# Chạy khối Kiểm pin` có sẵn trong SKILL, Tee pin vào `00-pins.log` đúng dạng SKILL chỉ, lưu/nạp `TL_PW_URL`/`SESSION`/`RUN` qua `N5-state.txt`, và `Start-Transcript`. Hai driver **không thêm logic sản phẩm**.
- Chỉ số IDX=1 đúng quy tắc SKILL: có đúng một dòng `(current)` `https://example.com/`, và đúng một dòng 2xx mang URL đó (`1. [GET] https://example.com/ => [200]`).
- Mọi băm trong `SHA256SUMS.csv` (lập lúc Cleanup) khớp MANIFEST, tức run không bị đổi sau Cleanup.

### Ngân sách chạy lại
- N2: 1 lần chạy lại. Lượt 1 là lỗi dựng: `N2-attempt1-O0-selftest.log` 0 byte, không có marker, progress dừng ở dòng header O0.
- N4: 1 lần chạy lại. Lượt 1: W1–W3 đạt, T1 log 0 byte.
- Cả hai nằm trong `native_step_reruns_limit: 1`.
- N5 tương tác (`N5-transcript.txt`) không chạy khối SKILL nào: transcript chỉ có `READY 7.6.10` cùng một `MethodInvocationException … ReadLine`. Vì vậy nó không phải lần chạy lại.
- N3D **không** thuộc ngân sách chạy lại (F4).

## 2. Findings

### P1
- **F1 — N6 được khai `passed` dù tiêu chí đặc tả của nó không đạt.**
  - Đặc tả N6 đòi hai điều: "Xoá W\pw" và "Kiểm LOCALAPPDATA\ms-playwright không đổi (danh sách + mtime trước/sau)".
  - Raw ghi `ms_playwright_unchanged=False before=11 after=12`: có thêm `daemon\7660722653841389\tl-pw-316f64e80925.err`, mtime của `b` và `daemon` đổi. `W\pw` còn `npm-cache` khoảng 40 MB và `runs/`.
  - Vậy mà `RESULTS.md` ghi "N6 gỡ | passed, kèm finding", hạ một tiêu chí hỏng xuống thành "F1 (P3)", và không nhắc tới `npm-cache`.
  - Đây đúng dạng lời khai "gỡ sạch dù còn dư lượng" mà prompt review yêu cầu bắt.
  - Đề xuất: đổi N6 thành `failed` và liệt kê đủ dư lượng (`ms-playwright` +1 thư mục/+1 tệp, `W\pw\npm-cache` 40 MB, `runs`, `lock.sha256`, `npmrc-empty`, `TARGET_ID`). Ghi rõ rằng việc giữ `runs/` là theo mục "Gỡ bản cài" của SKILL, tức lệch giữa đặc tả và SKILL.

### P2
- **F2 — O1 chạy N3 KHÔNG có `-Counterexamples`, trái đặc tả, và không NOTE nào khai.**
  - Đặc tả N3 áp cho "bản O1 và O3", mỗi tệp chạy cả hai edition, có `-Counterexamples`.
  - `scripts/N3-proxima-harness.ps1` (`227d46f8…`) đặt `@{ Opt = 'O1'; Cx = $false }`. Lệch này chỉ được khai trong một chú thích trong script.
  - `RESULTS.md` ghi O1 "passed" dưới nhãn "chạy chức năng".
  - Nếu chạy đúng đặc tả, O1 Config cũng sẽ rc 1 dưới en-US, vì lý do ở F3.
  - Đề xuất: ghi O1 là lệch đặc tả, không tính là passed theo N3.
- **F3 — FAIL của N3 là FAIL theo luật đặc tả, nhưng nguyên nhân là đặc tả/harness, không phải bằng chứng lỗi sản phẩm.**
  - Harness `ProximaConfig.Tests.ps1` dòng 575: `cultural-reserved-device … (focused runs; en-US: no credit)`.
  - Với `-Counterexamples` và culture mặc định en-US, đột biến này luôn sống sót. ProximaConfig **không thể** ra rc 0, nên đặc tả N3 như đã viết là không thể đạt.
  - Operator giữ nguyên FAIL. Đúng.
  - Đề xuất: giữ `failed` cho N3. Đặc tả r2 phải chỉ định `-TestCulture tr-TR` (hoặc chạy cả hai culture) cho lượt counterexamples.
- **F4 — N3D là một lượt native ngoài đặc tả và ngoài ngân sách, chạy sau một rc 1.**
  - Đặc tả viết: "Không chạy lại một FAIL sản phẩm để lấy xanh". Ngân sách chạy lại chỉ dành cho rc 2.
  - N3D minh bạch và không thay en-US. Nhưng `MATRIX.md` hàng U1 lại ghi "harness S1/S2/S3 **đạt** trên PS5.1.26100", trong khi S1 (Config) kèm counterexamples dưới en-US ra rc 1 trên PS5.1. Lời khai "đạt" ấy chỉ đúng nhờ O1 không CX hoặc nhờ N3D.
  - Đề xuất: sửa U1, và ghi quyết định của owner về N3D.
- **F5 — Biên nhận cài đặt N5 không có trong raw; lời khai "npm: 3/3 chữ ký registry + 3/3 attestation" không có nguồn đóng băng.**
  - SKILL ghi: "Lưu nguyên output cài làm biên nhận (`npm ci`, `audit signatures` rc 0, không chữ ký invalid/missing)".
  - `N5-A-transcript.txt` chỉ có `fatal: not a git repository…` rồi `SETUP OK`. `Start-Transcript` trong chế độ `-File` không bắt stdout của tiến trình native.
  - Quét toàn bộ zip: `attestation` 0, `verified registry` 0, `audited` 0. Thứ duy nhất có căn cứ là "rc 0", suy từ `SETUP OK`, vì khối Setup có `Need ($LASTEXITCODE -eq 0) 'npm audit signatures'`.
  - Lời khai "3/3 + 3/3" xuất hiện cả ở `RESULTS.md` (cột marker "nguyên văn") lẫn `MATRIX.md` hàng #5.
  - Đề xuất: hoặc đóng băng nguồn (output console của Desktop Commander, hoặc `W\pw\npm-cache\_logs` vẫn còn trên host), hoặc hạ lời khai thành "rc 0 (suy từ SETUP OK)".
- **F6 — Quét secret ở N7 không có marker dương.**
  - `secret-scan.out` và `.err` đều 0 byte. Theo hợp đồng của `pkg_secret_scan.py`: rc 1 in phát hiện ra stdout, rc 2 in ra stderr, ngoại lệ in traceback ra stderr. Vì vậy hai tệp rỗng **suy loại trừ** ra rc 0.
  - Nhưng rc chỉ được in ra console (`"secret_scan_rc=$($sp.ExitCode)"`), không được đóng băng. `RESULTS.md` vẫn khai `secret_scan_rc=0` như marker.
  - Quét độc lập của tôi trên 130 tệp văn bản: 0 lần khớp các mẫu `gh*_`/`github_pat_`/`sk-`/`AKIA`/`xox?-`/`GOCSPX-`/`AIza`/`PRIVATE KEY`/JWT/`1//0`/`Bearer`/`Authorization:`/`cookie:`/`password:`/`*_token:`/`AKfycb`. 12 lần khớp mẫu "email" đều là fixture giả `u:p@gw.example.invalid` của harness. PNG/PDF không chứa tên tài khoản, hostname hay đường dẫn.
  - Bộ quét của kho chỉ có 6 mẫu thiên về Google, không phủ token GitHub hay cookie.
  - Đề xuất: lưu rc vào tệp (chạy lại lệnh quét chỉ đọc, ghi ra ngoài thư mục đóng băng), hoặc đóng băng output console. Đồng thời commit MANIFEST đã lọc, như N7 đòi.
- **F7 — MATRIX trái §6 của đặc tả.**
  - §6 đòi hàng nào đổi sang `direct_native_desktop_17_11` thì phải "trỏ tới tệp trong zip và kèm sha256". Các hàng #1, #2, #3, #5, U1, U10 chỉ trỏ `r1/RESULTS.md`, không trỏ tệp trong zip, không kèm sha256.
  - Nhãn dùng là `direct_native_desktop_18_11`, không có trong chú giải của MATRIX. N1, N2 và N4 thật ra đo ngày 17/11 (16:4x–17:1xZ).
  - Giá trị `cho_review` không có trong chú giải `ket_luan`.

### P3
- **F8 — N4 rộng hơn phép đo ở ba điểm.**
  - Ảnh chụp "hash cây W\repo-O3" thực chất là `git status --porcelain --ignored` (chỉ tên thư mục bị ignore, không đọc nội dung `scripts/.tl_state/`), cộng băm `px-cfg`, cộng tên thư mục chứa "Proxima".
  - Không có phép đo mạng. "Không có kết nối mạng nào" chỉ suy từ `dispatched : False`.
  - Cấu hình là `config.example.json` (`gateway.example.invalid`). Vì vậy không chứng minh gì về gateway thật.
  - Glue đánh giá "reject" chỉ bằng `rc -ne 0`. Raw log có mã cụ thể nên tôi chấp nhận.
  - T1 và T3 trùng byte vì sản phẩm trả cùng mã `ArgumentMissing` mà không nêu tên đối số thiếu.
- **F9 — "O3 chỉ kiểm pin" (đặc tả N5) không được chạy bằng khối Kiểm pin của SKILL.**
  - Thay vào đó là phép so `package-lock` O2 = O3 = bản đã cài, đặt ở N6.
  - Lệch này không được khai.
- **F10 — N5 chỉ có PS7.**
  - Lời khai "parse_errors 2-3 trên N5-3/4/5 (đo 16:49Z)" trong `N5-PS7-NOTE.txt` không có raw. `W\parse-check.ps1` có trên host nhưng không được đóng băng, và output của nó không được lưu.
  - SKILL ghi "PowerShell 5.1/7: dán nguyên khối". Vì vậy r1 không chứng minh SKILL chạy được trên PS5.1.
- **F11 — Ghi chú lệch với raw.**
  - `N2-attempt1-NOTE.txt` nói lượt 2 "gọi python qua cmd /c", nhưng `N2-four-options.ps1` dùng `Start-Process -RedirectStandardOutput/-Error`.
  - `N4-attempt1/NOTE.txt` nói T1 lượt 1 "từ chối đúng 'ArgumentMissing' trên stderr", nhưng `N4-attempt1/N4-ps51-T1-no-target.log` là 0 byte.
  - `N5-interactive-ABORTED-NOTE.txt` ghi PID 3976, còn `N5-transcript.txt` ghi `Process ID: 12432`.
  - F1 của operator khai "Đã có sẵn 11 tệp cùng loại", nhưng `N6-ms-playwright-tree-after.txt` có **13** tệp `.err` cũ trong 9 thư mục con. "11" là số mục ở độ sâu 1 (`before=11`).
  - Lời khai "Mâu thuẫn với lời khai thư mục RIÊNG của SKILL" quá tay: mục Limits của SKILL đã khai sổ phiên ở `%LOCALAPPDATA%\ms-playwright\daemon`. Lỗ hổng thật là Cleanup và "Gỡ bản cài" không dọn chỗ đó.
- **F12 — Thiếu nguồn gốc lệnh.**
  - N1 không có lệnh nào được ghi. `N1-clone.log` 0 byte, và không có bằng chứng `core.abbrev 7`.
  - Không script nào trong `scripts\` sinh ra `N6-ms-playwright-before.txt` và `N6-ms-playwright-tree-after.txt`. Thời điểm chụp "before" cũng không được ghi.
- **F13 — Các mục §1 của đặc tả không có raw trong zip.**
  - Thiếu: khoá `KHOA.txt` lấy/nhịp tim/nhả (`RESULTS.md` khai "đã nhả lúc 00:35Z"), kiểm tải `Win32_Process`, dòng `F:\tl-win\do-luong.csv`.
  - `W\lock-heartbeat.ps1` có trên host nhưng không được đóng băng. Quét zip: `do-luong` 0 lần khớp.
  - Các bước chạy chồng nhau, không ghi lại: N4 (17:02–17:03Z) chạy trong lúc N2 O1 selftest (17:02–17:07Z); N6 (00:29:56Z) chạy trong lúc N3D ps7 (00:29–00:33Z).
- **F14 — Đường chuyển zip ngoài đặc tả.**
  - `W\upload-drive.ps1` (không đóng băng) đẩy zip và `.sha256` lên Google Drive qua `gws`, kèm ghi chú "Chủ kho duyệt 18/11".
  - Đặc tả N7 chỉ nói "chuyển zip về phiên điều phối". `RESULTS.md` nói "Gói nằm trên Desktop, ngoài kho" mà không nhắc Drive.
  - Script đã chạy hay chưa, và chủ kho có duyệt hay không: **KHONG_do_duoc** từ raw.
  - Nếu đã chạy, cần ghi vào hồ sơ: CLAUDE.md cấm ghi Drive khi người dùng chưa yêu cầu rõ.
- **F15 — Bằng chứng con của counterexample N3 không được đóng băng.**
  - `W\scratch` có 2770 tệp, 13,8 MB: mutant, child report, output.
  - Reviewer chỉ dựa được vào lần tự kiểm lại của harness (`cleanup=ok`, `evidence=ok`).
- **F16 — Riêng tư, không phải secret.**
  - Tên tài khoản `<tai-khoan-windows>` xuất hiện ở 10 tệp (54 dòng): transcript, `.err` của selftest, ENV-NOTE.
  - Hostname `DESKTOP-T9R33P2` ở 8 tệp. Đường dẫn OneDrive ở `ENV-NOTE.txt`.
  - Zip không được commit vào kho công khai. Hiện đang đúng như vậy.
- **F17 — Write set.** `ops/leases/wp1319-r1-g2-operator.yaml` không nằm trong write set §5 của đặc tả đóng băng. Lease g2 tự khai nó. Đây là ghi chú quản trị.

## 3. Lời khai trong RESULTS.md / MATRIX.md rộng hơn raw

1. RESULTS N6 "passed, kèm finding". Raw cho thấy tiêu chí `ms-playwright` không đạt và `W\pw` chưa xoá (F1).
2. RESULTS N5 "npm: 3/3 chữ ký registry + 3/3 attestation", và MATRIX #5 "3/3 chữ ký+attestation". Không có trong raw (F5).
3. RESULTS N7 "passed … `secret_scan_rc=0`", và đầu tệp "`pkg_secret_scan.py` trên gói trả rc 0". rc không được đóng băng (F6).
4. RESULTS N3 O1 "passed" dưới nhãn "chạy chức năng". Không khai đây là lệch đặc tả (F2).
5. MATRIX U1 "harness S1/S2/S3 đạt trên PS5.1.26100". S1 kèm counterexamples, en-US, PS5.1 là rc 1 (F3, F4).
6. MATRIX #1/#2/#3/#5/U1/U10 dùng nhãn `direct_native_desktop_18_11` mà không có tệp zip kèm sha256 (§6). Dữ liệu N2 và N4 là của 17/11 (F7).
7. RESULTS "Khoá … đã nhả lúc 00:35Z". Không có raw (F13).
8. RESULTS F1 "11 tệp cùng loại". Raw có 13 (F11).
9. RESULTS "Lỗi dựng 3: … vỡ parser PS5.1". Không có raw (F10).
10. RESULTS "Python 3.12.10" và "worker khởi động lại khoảng 17:20Z–23:58Z". Không có trong raw. Lời khai nhỏ, không ảnh hưởng kết luận.
11. RESULTS "Gói nằm trên Desktop, ngoài kho". Có thể đã có bản trên Drive (F14, KHONG_do_duoc).

Những lời khai **khớp raw**, ghi lại để cân bằng:
- N1, N2, N4 (kể cả "chỉ dùng cấu hình mẫu `gateway.example.invalid`").
- N3 O3 "failed (giữ nguyên)" và N3D "không thay kết quả en-US".
- N5 `SETUP OK` / `PIN OK` / `CLEANUP OK`, IDX=1.
- Zip 54506f18… và 131 tệp.
- Mục "r1 KHÔNG chứng minh", gồm cả "Capture example.com không phải xác minh pháp lý" và "harness thay mọi backend nguy hiểm bằng đồ giả".

## 4. Giới hạn

r1 **không** chứng minh:
- **Gateway, WinRM, service.** N3 Control thay 10/10 backend nguy hiểm bằng đồ giả. Wire case chỉ tới `127.0.0.1` do harness tự mở. N4 dùng `config.example.json` → `gateway.example.invalid` cùng `-WhatIf`.
- **Mạng ở N4.** "Không kết nối mạng" chưa được đo.
- **Xác minh pháp lý.** Capture `https://example.com/` (`source.body` 577 byte, PNG, PDF) chỉ là bản lưu nguồn.
- **playwright-browser trên PS5.1.** Chỉ có pwsh 7.6.10.
- **Kiểm pin trên bản O3.**
- **Phụ thuộc thật giữa lõi và add-on.** Selftest 1777/1777 cho ra log **trùng byte** ở cả bốn lựa chọn, và có 0 tham chiếu tĩnh. Vì vậy N2 chỉ chứng minh lõi không phụ thuộc add-on. Nó không chứng minh add-on "hoạt động" trong lõi. Một vài ca selftest tự `BỎ QUA` trên Windows, ví dụ `wp726_script_nlm_canary`.
- **Các ca VHD.** `A3-07`, `A3-08` và `CX-ignore-mount-topology` là `unavailable`, vì không bật `-VhdFixture`.
- **Phạm vi §3 đặc tả.** Updater, restore, file lock, đĩa đầy, rollback, máy bận, promotion fence (§11 #6–#10), U8, NSIS, migration, LIVE đều chưa đo.

Giới hạn của chính lượt review này:
- Tôi đọc tại chỗ trên máy của operator và tin vào `Get-FileHash` / `ZipFile` của host đó. Một host bị chiếm quyền thì nằm ngoài phạm vi.
- Tôi không có output console Desktop Commander của các lượt chạy. Mọi thứ chỉ có ở console (rc quét secret, output npm, output parse-check, upload Drive) là **KHONG_do_duoc**.
- Tôi không chạy lại test nào. Tôi không kiểm hồ sơ hay comment trên GitHub ngoài các tệp trong checkout.

---
Bản trong kho: thay tên tài khoản Windows bằng `<tai-khoan-windows>` (kho công khai). sha256 bản gốc của reviewer: `6a571269ea2646a74737aaa59299b31dbc13076900195f973d10a2bc4baebf25`.
