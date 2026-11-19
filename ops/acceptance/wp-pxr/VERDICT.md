# WP-PXR r1 — Review độc lập (1/1)

- **Reviewer:** Codex CLI 0.169.0, `-m gpt-6-astra`, chạy trong container điều phối, chỉ đọc.
  - Model tự khai **`KHONG_do_duoc`**.
  - Chạy 09:08:41Z–09:10:37Z ngày 19/11, rc 0.
  - Verdict gốc có sha256 `e18055859439edc8d8ab1e2cdbf114973209142369eec6e9f09ffd060408599c`.
- **Đối tượng:**
  - Zip `3a1f04b1…`, chuyển nguyên byte về container. 16/16 tệp khớp MANIFEST.
  - Băm đặc tả khớp `spec_hash`.
  - Đảo rồi áp lại `patch1.py` tái tạo đúng cả hai băm driver: `26425641…` → `0834dda7…`.
  - Module mà R4 nạp đúng đường dẫn và băm `81c1164b…`.

## Verdict: `approve_scoped`, không có P0
Chấp nhận trong phạm vi **một lượt chạy thật trên Desktop** làm bằng chứng cho quy trình H.7. Đây **không** phải chấp nhận độ an toàn chung của driver.

| Điểm | Kết luận |
|---|---|
| R2/R3 | Bộ gỡ thoát mã 0. `Un_A.exe` thấy ở 0,8–5,0 s, mọi helper kết thúc ở 9,2 s. Khoá gỡ cài đặt và `Proxima.exe` đã mất. Tồn dư (thư mục cài rỗng + `installer.exe`) khớp MATRIX:191 và SKILL.md:88 |
| R4 | `WOULD_REMOVE` với 3 hành động nằm trong hai đích, rồi `CLEANED`, `ok=true`, cả hai đích `absent`. Thư mục `.pxu-<GUID>` là vùng cách ly có chủ đích, đã bị xoá, **không** phải tồn dư |
| R5–R7 | Shortcut U8 và profile (12 085 tệp / 287 185 128 byte) đã xoá. Hai `Proxima.lnk` của nhà cung cấp đã mất ngay từ R3, tức do bộ gỡ dọn |
| PowerShell | Không còn va chạm tên biến, không còn chỗ `.Count` trên kết quả hàm chưa bọc `@()`. Lỗi của dryrun-1 được ghi rõ |

**P1 (sửa trước khi dùng lại driver; không lỗi nào xảy ra ở lượt này):**
- **Đua đường dẫn ở R6:**
  - Driver kiểm đường dẫn và reparse point, rồi `Remove-Item -Recurse` theo **tên** mà không giữ handle.
  - Nếu một thư mục tổ tiên bị tráo thành junction đúng lúc đó, lệnh xoá có thể đi ra ngoài profile.
  - Chưa có phép thử đua.
- **Chốt chưa đủ:**
  - R0 ghi nhưng không kiểm host/tài khoản/máy.
  - Bộ lọc hành động ở R4 nhận chuỗi con của `proxima-updater`, nên một đường dẫn anh em cũng lọt.
  - `R4.ps1` nạp lại module và chạy thật **trước khi** kiểm băm. Nếu module bị thay giữa hai tiến trình con, lượt thật sẽ chạy mã khác. Băm thực tế lúc chạy vẫn khớp.

**P2:**
- Khoá chỉ giữ handle độc quyền lúc lấy và lúc nhả, không giữ suốt quá trình. Nếu nhả khoá thứ nhất ném lỗi thì khoá thứ hai có thể không được nhả.
- Theo dõi tiến trình bằng lấy mẫu:
  - có thể sót tiến trình sống ngắn;
  - `WaitForExit` không giới hạn thời gian;
  - mã thoát khác 0 không làm dừng bước dọn;
  - `DONE` không phải PASS tính tự động.

**Giới hạn ghi nhận:**
- Một lượt thật và hai lượt khô, quan sát tiến trình bằng lấy mẫu.
- Không đo:
  - đồng bộ OneDrive của Desktop;
  - thu hồi phiên phía provider;
  - `%TEMP%` của `Un_A.exe`;
  - khoá registry khác;
  - cache Electron ngoài `%APPDATA%\Proxima`.
- Kết quả quét secret rc 0 không chứng minh tuyệt đối không có secret.
- *Phiên điều phối tự ghi thêm, reviewer không nêu:* băm `Proxima.exe` `6990dce4…` (điều 3 của tiêu chí H.7) **không được đo lại** ngay trước khi gỡ. Băm này chỉ được đo lúc cài (U8 A1) trên cùng bản cài.

<details><summary>Nguyên văn verdict của reviewer (sha256 e1805585…)</summary>

```text
VERDICT: approve_scoped

Approval covers the recorded single Desktop run and H.7 procedure evidence, not general driver safety. I performed local read-only inspection/hash checks; no Windows operation or network access. Model: KHONG_do_duoc. Provider: OpenAI; surface: Codex tool session; evidence transport: frozen local relay.

Reviewed branch `ccr-8ee03d7f-vnmqk0`, HEAD `bd5966bb5d581d84fb45dbcc6d4ce7a6e734280d`, tree `376354c9ae191f13ea5882d6c7ccf5a41145703a`; lease base `dde32804e7d31384ea59c456550ac4a10fe5b7ab` is an ancestor. Below, `E` means `../ex2`, `D` means `E/PXR.ps1`, `J` means `E/evidence/PXR-result.json`, and repo paths are relative to `/home/user/tra-luat`.

| Check | Result and evidence |
|---|---|
| Integrity | ZIP SHA256 `3a1f04b1f8466014b84d051e6ad9e02a318f50da51d804d821263e73206664c8`; every ZIP member matches extraction; all 16 `E/MANIFEST.json:$.files` sizes/hashes match. |
| Contract | Spec SHA256 `5da780284704ff021f852b9e4bea85576d0a40bc4f3054ae75b5b3287046fb04` equals lease `$.spec_hash`. |
| Driver history | Reversing/reapplying all seven `evidence/patch1.py:3` replacements exactly reproduces pre-patch `26425641a36b3e88fdf41a5477ceaafffd0bb97766441de9d0af8ec0922df979` and final `0834dda72b4a5804e80782dfd5f76c67dc5e3c4651661949d50a31fad57c6db1`; respective dry-run/real `$.driver_sha256` match. |
| Loaded module | Both R4 JSONs `$.info` report the specified OneDrive Documents module path and SHA256 `81c1164bf913b181ae5e8e88a04b4498abd592d1ff2e3a25f6cf24d7ed57a82a`, matching the 39,070-byte repo module and WP-PXL. Import-by-name: `E/evidence/R4.ps1:6`. |
| Scope/prechecks | Direct deletions target only residue, U8 shortcut and profile; vendor shortcuts are only inspected. D:101–117 checks §1 registry, counts/bytes, hashes, process absence and profile reparses; host identity caveat below. No profile contents/names emitted. |
| R2/R3 | `J:$.steps.R2`: exit 0, helpers_done=true, 9.2s; Un_A.exe PID 16168 observed at 0.8–5.0s. R3: key/executable gone, empty install directory, installer.exe retained. Matches `MATRIX.md:191` and skill `SKILL.md:88`. |
| R4 | `J:$.steps.R4_whatif.result`: WOULD_REMOVE, three actions confined to targets; Real: CLEANED, ok=true, both after.kind=absent, quarantined=[]. Temporary `.pxu-<GUID>` is expected handle-verified quarantine, subsequently deleted (`ProximaInstall.psm1:454,540,552,572`), not leftover residue. |
| R5–R7 | D:159–173 implements shortcut type/reparse/target/argument checks and profile lexical equality/under-u8/reparse/process checks. `J:$.steps.R5,R6,R7`: both deleted; profile previously 12,085 files/287,185,128 bytes; final targets, APPDATA\\Proxima and watched processes absent. Vendor shortcuts already absent in R3: attributable to uninstaller. |
| PowerShell/history | No case-insensitive automatic-variable collision or remaining unwrapped collection-result `.Count` found. Null command lines become empty strings. Dryrun-1 explicitly records PRECHECK_FAILED before R2; dryrun-2 records DRYRUN_OK/STILL_INSTALLED. Dry runs still write evidence/locks. No separate parse-check receipt supplied. |

Findings (reuse hardening; no observed run failure):

- **P0:** None identified.
- **P1 — Path race:** D:167–172 checks lexical paths and reparses, then recursively deletes by pathname without held identity/ancestor handles. An ancestor swapped to a junction can redirect deletion outside the profile. PS7 link handling does not establish atomic safety; a newly encountered link need not imply recursive traversal of its target. No Windows race test performed.
- **P1 — Incomplete gates:** D:91 records but never validates host/account/device; a matching cloned host can pass R0. D:153 accepts updater-prefix substrings, including sibling paths; null actions also pass. `R4.ps1:6–8` imports anew and invokes Real before validating its hash: replacement between children could execute another module. Actual outputs match.
- **P2 — Locks:** D:75–88 uses exclusive handles only during take/release, not throughout work. Cooperative content locking and exact case-sensitive release are present; D:183 finally releases both successfully in the log. An exception releasing one could skip the other/result serialization.
- **P2 — Observation/control:** D:35–39,129–142 misses short-lived processes, aliases and null-command-line profile users; timeline records last sighting, not exit. WaitForExit is unbounded; nonzero exit does not halt cleanup. D:179 DONE is not computed PASS.

Record limits: one real run, two dry runs; sampled process observations, no race proof. OneDrive Desktop synchronization, server-side session revocation, `%TEMP%` Un_A.exe leftovers, other registry keys, and Electron caches outside APPDATA\\Proxima were not measured. Secret scan reports rc=0; not proof of universal absence.

H.7 wording: “passed (scoped Desktop, Proxima 5.5.0 per-user, one run): official uninstall → observed helper completion → promoted residue cleanup; U8 shortcut/profile removed.” Preserve vendor-uninstall failure and existing WP-PXU unmeasured cases.
```

</details>
