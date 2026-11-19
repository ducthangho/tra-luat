# WP-NSIS r1 — Review độc lập lượt N2 (1/1)

- **Reviewer:** Codex CLI 0.155.1 chạy trên ASUS, gọi với `-m gpt-6-astra`, sandbox chỉ ghi được vào `out`. Model tự khai "GPT-6 (Codex); exact serving variant unavailable", nên ghi **`KHONG_do_duoc`**.
- **Thời gian:** 00:12:46Z–00:14:48Z ngày 19/11, rc 0.
- **Đối tượng:** bộ con chuyển từ Desktop (relay `283dcd14…`, MANIFEST `003f54f3…` của zip `6084f4a7…`) gồm progress log, result.json, kết quả quét secret và driver `NSIS-N2.ps1`.

## Verdict: `request_changes`

| Bước | Phân loại | Ghi chú |
|---|---|---|
| Toàn vẹn bộ con | measured_pass | Bộ con và MANIFEST khớp |
| S0 trong phạm vi driver | measured_pass | Chỉ phủ các đường dẫn, registry và tên tiến trình mà driver chọn |
| S0 "không có gì Proxima" | not_measured | Không có kiểm kê toàn diện, không xét user khác |
| S1 | measured_pass | 161 754 969 byte, đúng sha256, `NotSigned` |
| S2 cài + exe | measured_pass | rc 0, đúng sha256 exe, có bộ gỡ, có shortcut |
| S2 "khoá HKCU có location" | not_measured | Driver không ghi hive registry và `InstallLocation` thô; location suy từ `QuietUninstallString` |
| S2/S4a "không khởi chạy" | not_measured | Chỉ lấy mẫu sau khi cài, không theo dõi việc tạo tiến trình suốt quá trình cài |
| S3 gỡ | **measured_fail** | Gỡ xong (khoá, shortcut, exe đều hết), nhưng còn thư mục rỗng và `installer.exe` 161 754 969 byte |
| S4a cài lại | measured_pass | 3226 tệp; manifest trùng S2 (`2537b108…`), so trên máy chủ |
| S4b gỡ lần 2 | **measured_fail** | Tồn dư y hệt S3 |
| Dọn tay sau đo | not_measured | Không có snapshot kiểm kê sau khi dọn |

**P1**
- **Tiêu chí đóng băng không đạt:** S3/S4 để lại thư mục và `proxima-updater\installer.exe`. Việc dọn tay không đổi FAIL thành PASS. Danh tính `installer.exe` là bản sao bộ cài mới chỉ do operator báo (khi dọn có kiểm băm `959c14c1`), N2 không đo băm của nó.
- **Phép đo còn hở:** `Keys` gộp HKCU và HKLM, không ghi đường dẫn registry; `Loc` dựa vào `QuietUninstallString`; kiểm tiến trình chỉ là lấy mẫu; khi helper của bước cài quá hạn thì driver không báo lỗi.

**P2**
- Hoàn tất bất đồng bộ được tách đúng khỏi tồn dư: ở S4b, lúc `t+5s` vẫn còn `Un_A.exe`, đến 8 s thì sạch. Đây là cận lấy mẫu, không theo dõi cây tiến trình con.
- `NotSigned` là phép đo, không phải tiêu chí FAIL của đặc tả.
- Không chứng minh: cài per-machine, nâng cấp từ bản cũ, rollback, lần chạy đầu tiên, và kiểm kê thay đổi toàn hệ thống.

## Xử lý
- Kết quả FAIL S3/S4 là **hành vi của sản phẩm**: bộ gỡ chính thức để tồn dư. Ghi lại như vậy, không sửa được ở phía operator, trừ khi bổ sung bước dọn có kiểm soát vào quy trình gỡ.
- Phép đo hở ở P1 cần lượt đo mới. Ngân sách native của g2 đã dùng hết, nên cần chủ kho quyết định.

---

# Review độc lập lượt N3 (lease g3, 1/1)

- **Reviewer:** Codex CLI 0.169.0, gọi với `-m gpt-6-astra`, sandbox `workspace-write` chỉ ghi vào thư mục `out` riêng. Model tự khai không xác nhận được bản đang phục vụ, nên ghi **`KHONG_do_duoc`**. Thời gian 01:41:24Z–01:43:03Z ngày 19/11, rc 0. Bản verdict gốc có sha256 `2113f51dd594eb15dc3a820ba7ab9b9f930cac7d7ace64b46aa03ca97cb91e87`.
- **Lệch so với lease g3:** lease ghi reviewer "trên máy Windows", nhưng lượt này chạy **trong container Linux của phiên điều phối**, vì ASUS offline từ khoảng 00:40Z. Reviewer chỉ đọc bằng chứng đã đóng băng, không cần OS Windows. Đổi lại, nó không kiểm được trạng thái thật của Desktop.
- **Đối tượng:** bộ con chuyển từ Desktop. Chép từng khúc base64 và kiểm sha từng khúc; zip con `c410816f…` khớp. MANIFEST `502b4913…` thuộc zip `fede4bda…`. Gồm progress log, result.json, kết quả quét secret và driver `NSIS-N3.ps1` (`9191fe1f…`). Hai manifest cây cài 554 589 byte và bộ cài **không** được chuyển.

## Verdict: `request_changes`

| Bước | Phân loại |
|---|---|
| S0 | not_measured: driver tiền kiểm hẹp hơn đặc tả |
| S1 | measured_pass |
| S2 / S4a | measured_fail, **chỉ** vì tiêu chí chữ "khoá HKCU có `InstallLocation`". Reviewer xác nhận tiêu chí này **sai** với electron-builder per-user; mọi điểm khác đều đạt |
| S3 / S4b | measured_fail: bộ gỡ của nhà cung cấp không sạch |
| S3c / S4c | not_measured so với tiêu chí đóng băng (chưa có tiêu chí cho bước dọn); đạt trong phạm vi bước dọn |

**P1 (tóm tắt)**
1. Tiêu chí đóng băng "gỡ sạch" **vẫn không đạt**. "Gỡ + dọn có kiểm soát" chỉ thoả một tiêu chí đã sửa. Lease g3 cho phép **thử**, không cho phép thay tiêu chí PASS. Cờ `passed=True` của driver (D:69) không được dùng khi chưa sửa tiêu chí.
2. Đặc tả F:43 đòi `InstallLocation`. Nay đã đo được là vắng mặt, nên đây là kỳ vọng **sai** của đặc tả. Tiêu chí sửa nên nhận thư mục suy từ `QuietUninstallString` sau khi kiểm hợp lệ.
3. Tiền kiểm và snapshot của driver hẹp hơn đặc tả. Driver chỉ xét một thư mục, một shortcut Start menu và đúng tên tiến trình `Proxima`. Đặc tả đòi thêm: `Programs\proxima*`, shortcut Desktop, `Proxima*`, `%APPDATA%\Proxima`, và tải máy.
4. **Bước dọn không an toàn trước đua.** Thư mục cài được xoá không đệ quy (an toàn). Riêng updater bị xoá **đệ quy** dựa trên ảnh chụp trước đó: tệp thêm vào sau lúc chụp sẽ bị xoá theo. Không có kiểm reparse point ở thư mục tổ tiên. **Lỗi này là của driver do phiên điều phối viết.**

**P2:** việc theo dõi tiến trình là lấy mẫu 500 ms cộng thời gian truy vấn, không bắt sự kiện liên tục. Khoá host lấy không nguyên tử và lấy trước `try`. Tính lặp lại chỉ được ghi bằng băm, reviewer không tự dựng lại. Chưa đo: per-machine, nâng cấp, rollback, lần chạy đầu, user khác, kiểm kê toàn hệ thống. `NotSigned` không có trường chứng chỉ/timestamp.

## Xử lý
- Ngân sách g3 đã hết: native 1/1, review 1/1. **Không đo lại.**
- Kết luận ghi sổ:
  - **Gỡ của nhà cung cấp: FAIL (hành vi sản phẩm)**, chắc chắn sau ba lượt N1b/N2/N3.
  - **Cài per-user: đạt** trong phạm vi đã đo. Ngoại lệ duy nhất là tiêu chí `InstallLocation` sai của đặc tả.
- **Cần chủ kho quyết định:** có sửa tiêu chí NSIS thành "gỡ của nhà cung cấp + dọn tồn dư có kiểm soát" hay không. Nếu sửa, quy trình phải dùng hàm an toàn của packet WP-PXU (`ops/specs/wp-pxu-r1.md`), **không dùng lại** đoạn dọn trong driver N3. P1 số 4 đã được đưa vào đặc tả WP-PXU dưới dạng ràng buộc bắt buộc: cô lập bằng đổi tên nguyên tử, xoá không đệ quy, kiểm tổ tiên.

<details><summary>Nguyên văn verdict của reviewer (sha256 2113f51d…)</summary>

```text
VERDICT: request_changes

Model: KHONG_do_duoc (exact serving ID unavailable).

References: D=`../ex/NSIS-N3.ps1`; R=`../ex/evidence-n3/NSIS-N3-result.json`; L=`../ex/evidence-n3/NSIS-N3-progress.log`; M=`../ex/MANIFEST.json`; Q=`../ex/evidence-n3/secret-scan.json`; F=`../ref/wp-nsis-r1.md`.

| Step | Classification against frozen criteria | Evidence quote |
|---|---|---|
| S0 | not_measured (incomplete coverage) | L:2 “S0 clean”; R:$.steps.S0 “keys”:[], “dir”:false; omissions below |
| S1 | measured_pass | R:$.steps.S1 “bytes”:161754969, “sha256”:“959c14c1ba489deb53bdaa34e83939fb18f9d7ade58a48a03d361ad1dd12ebf8”, “passed”:true |
| S2 | measured_fail (literal InstallLocation criterion) | R:$.steps.S2 “rc”:0, “hkcu_only”:true, “exe_sha256”:“6990dce4b0b56e0d999fdc36521e9a57fe7a237348fc5c9d48e74873b742f886”, “app_processes_seen”:[]; keys[0].install_location_raw:“<absent>” |
| S3 | measured_fail | R:$.steps.S3 “rc”:0, “vendor_clean”:false; after.dir:true |
| S3c | not_measured (no frozen cleanup criterion) | R:$.steps.S3c “clean_after”:true; measured_pass for scoped cleanup only |
| S4a | measured_fail (repeats S2 requirement) | R:$.steps.S4a “rc”:0, “manifest_equal_S2”:true; keys[0].install_location_raw:“<absent>” |
| S4b | measured_fail | R:$.steps.S4b “rc”:0, “vendor_clean”:false; after.dir:true |
| S4c | not_measured (no frozen cleanup criterion) | R:$.steps.S4c “clean_after”:true; measured_pass for scoped cleanup only |

Integrity: locally recomputed `../sub.zip` SHA256=c410816fbfebb2547d4fc60e39173c5b762721ee58dadadddf2349adf5507dac; M=502b4913b878408ec3eb506d90b9e3cdc81f534b36e102ddc6180f4b12d4834c; F=04f2e4eb26811031e9c8f45400ec14bb9a1e544c23bc0dcca2ce6822efc760a9. Every present manifest-listed file matches both size and full SHA256: progress 1902 bytes, result 7417, secret-scan 138, driver 11154 (M:$.files[0,1,4,5]). M is not self-listed. Installer and two 554589-byte manifests are absent (M:$.files[2,3,6]); full frozen zip integrity cannot be independently checked. Q:$.rc and M:$.secret_scan_rc are 0; Q records scanner hash and empty stdout/stderr, **no invocation or targets**: what was scanned is unproven.

P1 — Frozen acceptance remains unmet. Vendor uninstall is **not clean**: both runs retain the empty install directory plus installer.exe matching the official hash (R:$.steps.S3.after, $.steps.S4b.after). Procedure cleanup is clean **within measured scope** (R:$.procedure_clean, $.final_snapshot), satisfying only a revised criterion, not F:35–45. Lease g3:45 authorizes experimentation, not replacement of PASS. D:69 can report “passed” despite vendor failure. Amend acceptance explicitly before using that flag.

F:43 literally requires an HKCU InstallLocation value. Its absence is now measured, not an unknown. For the reported electron-builder per-user behavior this is an incorrect expectation (REF RESULTS.md:19; R:$.steps.S2.keys[0]); a revised criterion should accept a validated directory derived from QuietUninstallString. D:16 prefers raw InstallLocation, otherwise extracts that string’s quoted uninstaller parent; it does not manufacture the missing value.

P1 — Preflight/snapshot gaps: D:13–19,59 check one exact directory, one Start-menu link, and exact Proxima process name. F:21–28 additionally requires Programs/proxima*, Desktop shortcuts, Proxima* processes, roaming AppData, and host load. A Proxima-beta installation or roaming user data can survive unnoticed. F:32,46’s broader inventories/no-other-changes remain unproven.

P1 — Cleanup is conditional, not race-safe. D:47–50 removes the install directory without recursion only after counting zero entries; updater removal recursively trusts the earlier snapshot’s single installer.exe/hash match. Extra entries present during snapshot are KEPT. Entries added afterward can be recursively deleted. No reparse-point/ancestor checks or atomic ownership protects against junction substitution. Paths are environment-derived constants, not registry-derived (D:13); validate canonical paths/reparse points and prevent concurrent mutation before general reuse.

P2 — Measurement improvements and limits: D:14–15,30 record full hive/key, query HKLM/WOW6432Node, and correctly require exactly one HKCU match; suppressed registry errors and unrecorded process bitness limit completeness. D:19,23–26 poll during install/helpers and 30 seconds afterward: 500ms sleep **plus query time**, 115/118 polls (R:$.steps.S2.watch_polls, $.steps.S4a.watch_polls). Short-lived processes, renamed executables outside the directory, unavailable executable paths, and excluded Uninstall* names can escape. This is not continuous event capture.

D:17,25,37–40 add explicit 120-second install-helper/300-second uninstall-completion errors; name matching is not process-tree tracking. D:18,47–51,72 close residue-hash/post-cleanup-snapshot gaps. D:23,36 retain Process.Handle before ExitCode; D:54 handles empty-content null; no bracketed -like pattern remains. Distinct lockText/instDir avoid case-insensitive collision; release requires exact content (D:74; L:10–11). Acquisition is non-atomic and precedes try; partial acquisition or final-snapshot failure can strand locks (D:53–57,72–74).

P2 — Repeatability is recorded, not independently reconstructed: identical manifest hashes and 3226 files (R:$.steps.S2, $.steps.S4a; M:$.files[2,3]); contents/baseline comparison unavailable. Per-machine, older-version upgrade, rollback, first launch, other users and full-system inventory are unproven (D:13–19,62–66). “NotSigned” proves no trusted signer; certificate/timestamp fields were not recorded, and signature is not PASS-gating (R:$.steps.S1; D:60; F:29).
```
</details>

