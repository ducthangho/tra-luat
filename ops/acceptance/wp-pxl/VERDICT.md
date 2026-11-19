# WP-PXL r1 — Review độc lập (1/1)

- **Reviewer:** Codex CLI 0.169.0, `-m gpt-6-astra`, chạy trong container điều phối, chỉ đọc. Model tự khai **`KHONG_do_duoc`**. Thời gian 06:41:38Z–06:44:37Z ngày 19/11, rc 0. Verdict gốc có sha256 `ef0ac79e…`.
- **Đối tượng:** zip Desktop `2021e183…` và zip VM `df30ce64…`, chuyển nguyên byte; 8/9 tệp khớp MANIFEST; driver `91faef1c…` giống nhau trên hai máy; artifact khớp blob git ở `9cdfeaf5b`; tính lại `artifact_sha256` cho ra `194de266…`.

## Verdict: `approve_with_fixes`, chấp nhận trong phạm vi lần cài 2 module đã ghi (không có P0)
| Điểm | Kết luận |
|---|---|
| Hàng rào | Desktop `ALLOWED` vì là máy đầu. VM `ALLOWED` nhờ receipt Desktop, hai bản giống nhau từng byte (`fb230706…`). Theo mã module, receipt thiếu, `passed=false` hay lệch artifact đều bị chặn |
| P0–P4 | Đúng như log. Phép thử `WhatIf` dùng provider rỗng trên thư mục tạm rỗng, nên an toàn |
| Gateway trước/sau | Reviewer **tự so**: 14 tiến trình (PID và thời điểm khởi động), 4 tệp `ProximaControl` 1.0.1, 3 tác vụ `TraLuat*` **giống hệt** |
| Thư mục Modules | Desktop `[] → [ProximaActivation, ProximaInstall]`; mỗi thư mục trên VM `[ProximaControl] → [ProximaActivation, ProximaControl, ProximaInstall]` |

**P1 (sửa trước khi dùng lại driver):** khoá host lấy kiểu kiểm-rồi-ghi, không nguyên tử. Nếu ghi receipt, kết quả hay log thất bại thì khoá có thể không được nhả.

**P2:**
- rollback chưa kiểm đúng tên, băm và kiểu từng tệp (rollback chưa từng chạy);
- kiểm khói chưa xét đường dẫn của `ProximaInstall` và cờ `whatif_ok`;
- **khai rộng hơn phần đo** (đã sửa): MATRIX nói service/endpoint "không đổi" dù driver không đo; RESULTS nói "chưa luồng nào gọi tới" dù không chứng minh được.

**Giới hạn ghi nhận:**
- Ảnh chụp gateway chỉ so PID, tên, thời điểm khởi động, băm 4 tệp và trạng thái tác vụ. Không so quan hệ cha-con, định nghĩa tác vụ, module đang nạp, service, endpoint hay `PSModulePath`.
- PowerShell có thể tự nạp module mới.
- Phần OneDrive đồng bộ trên Desktop chưa đo.
- Trên VM, PS 7 ở thư mục commander nạp theo tên (đặc tả §3 ghi theo đường dẫn).
- Chưa chạy ca âm của hàng rào trên máy thật.
- Kết quả parse-check trước khi chạy không được đóng băng.

<details><summary>Nguyên văn verdict của reviewer (sha256 ef0ac79e…)</summary>

```text
VERDICT: approve_with_fixes

Scoped approval of the recorded two-module installation; fix the reporting and driver weaknesses below before reuse. No promotion, PowerShell, inference, network access, repository modification, or git write performed by this reviewer. Local Python integrity/result assertions passed (exit 0).

Model: **KHONG_do_duoc** (exact model ID unattestable). Provider: OpenAI; surface: Codex tool session; transport: local shell/file reads. This does not attest the lease’s named `gpt-6-astra` identity.

Reviewed HEAD: `bf8505b981793df59c5557b3f6bb0c6801776ee4`; tree: `80c2b1ecfb8f82f3f04d5e33ad010ad625715f0d`; branch matches. Artifact commit: `9cdfeaf5b1eb17d0d75eb4ce6defe5a29ba69e7a`; `.agents/` unchanged through HEAD. Spec hash matches lease line 20.

References: `D`/`V` = `../relay/{desktop,vm}-ex`; `P` = `D/PXL.ps1`; `DR`/`VR` = respective `evidence-*/PXL-<host>-result.json`; repository paths below are relative to `/home/user/tra-luat`. Local module copies preserve frozen blob line numbers.

| Check | Evidence and conclusion |
|---|---|
| ZIP integrity | Desktop `2021e18376d60f90bc394bac0d32f5c0a95c0890ffa6ca80ffe1d79940e2036e`; VM `df30ce64ac6175c9998752ce8836927fa5983abf8f227d401774aadbb0b51d57`. Both match supplied hashes; ZIP members equal extracted bytes; all 8/9 `MANIFEST.json:$.files` entries match size/hash, without extras except manifest itself. |
| Artifact/driver | Identical driver SHA `91faef1c46d60212bbef104712749d5f0c6199e6613e3e3d2ca1dbcf4f5a83c1`. Git blobs match P:16–17 sizes/hashes. Recomputed spec §1 tab/LF formula gives `194de2661beac7804ff77aec7397ff652220a2a6f8cf30212d77baf9b3510b86`. |
| Scope/order | P:37–59 checks source before import/copy; rejects existing destinations; non-Force directory creation. Fence precedes installation, **not all writes**: evidence/receipt directories, locks/logs precede it (18,31–34). Creates only module payload directories plus Desktop root chain; ancillary evidence/temp/receipt writes also occur. |
| Fence | DR/VR `$.steps.P1`: Desktop first-host ALLOWED; VM ALLOWED with Desktop receipt. Both receipt copies byte-identical, SHA `fb230706f18823a24d256274e5a51ef12a642d01fa4523e2b3fe6359db2417a7`; schema, host, artifact, Boolean passed=true and timestamp valid. `ProximaActivation.psm1:567–600` blocks missing/failed/mismatched receipts with corresponding FENCE codes; invalid schema/host also blocked. |
| P0–P4 | D/V `evidence-*/PXL-progress.log:2–9/2–11` agree with DR/VR `$.steps`: CPU 3%/0%, correct source HEAD; 2/4 installed hashes; 2/4 fresh PS7/5.1 probes rc=0; exact exports, NOTHING_TO_DO, zero actions, ALLOWED. Empty temporary root and empty injected providers make WhatIf safely synthetic (P:67–69; `ProximaInstall.psm1:698–706`). |
| Postcheck | Independently compared VR `$.steps.P0.gateway_before` against `$.steps.P4.gateway_after`: all three arrays identical. Full before/after arrays: [gateway-arrays.json](/tmp/claude-0/-home-user-tra-luat/f4490c54-3763-505a-8947-c8e0d9e7d368/scratchpad/pxl/review/gateway-arrays.json). Root arrays: Desktop `[] → [ProximaActivation,ProximaInstall]`; each VM root `[ProximaControl] → [ProximaActivation,ProximaControl,ProximaInstall]`. Both receipts passed=true; logs show locks released. |

VM before = after arrays:

```text
procs = [
436:Proxima.exe:2026-11-18T14:39:01.8333930Z,
540:Proxima.exe:2026-11-18T14:39:28.8583870Z,
1580:Proxima.exe:2026-11-18T14:39:44.1247540Z,
2716:Proxima.exe:2026-11-18T14:39:44.1590460Z,
3264:Proxima.exe:2026-11-18T14:39:10.7248990Z,
3332:Proxima.exe:2026-11-18T14:39:16.5571910Z,
3352:Proxima.exe:2026-11-18T14:39:10.8953980Z,
4496:Proxima.exe:2026-11-18T14:39:58.6971390Z,
4852:Proxima.exe:2026-11-18T14:39:19.8173530Z,
5268:ProximaGateway.exe:2026-11-18T14:38:59.2898030Z,
5324:Proxima.exe:2026-11-18T14:39:20.6561280Z,
5404:Proxima.exe:2026-11-18T14:39:21.6910120Z,
5432:Proxima.exe:2026-11-19T06:34:00.5564440Z,
5776:Proxima.exe:2026-11-18T14:39:11.6234030Z
]
proximacontrol_files = [
C:\ProgramData\TraLuatCommander\profile\Documents\PowerShell\Modules\ProximaControl\1.0.1\ProximaControl.psd1:401:3f2ac59e201128f03d047da69698567b75675917687d75e8312fd7e34f14ee77,
C:\ProgramData\TraLuatCommander\profile\Documents\PowerShell\Modules\ProximaControl\1.0.1\ProximaControl.psm1:12138:ef4821cc14ba7234705c42b470d502ceea93982c379871e292d7e7f830ca1344,
C:\Users\tlcommander\Documents\PowerShell\Modules\ProximaControl\1.0.1\ProximaControl.psd1:401:3f2ac59e201128f03d047da69698567b75675917687d75e8312fd7e34f14ee77,
C:\Users\tlcommander\Documents\PowerShell\Modules\ProximaControl\1.0.1\ProximaControl.psm1:12138:ef4821cc14ba7234705c42b470d502ceea93982c379871e292d7e7f830ca1344
]
tasks = [
TraLuat-CapNhatCongCu-HeThong:Ready,
TraLuat-CapNhatCongCu-NguoiDung:Ready,
TraLuatRemoteCommander:Running
]
```

Findings (static failure scenarios; not observed failures):

- **P0:** None identified.
- **P1 — lock safety:** P:31–33 checks then overwrites lock files non-atomically; concurrent operators can both enter. P:102–105 receipt/result/log failure prevents lock release. Use exclusive acquisition and independently protected cleanup before reuse.
- **P2 — rollback accuracy:** P:98 accepts either artifact hash under any filename, records skipped directories as `rolled_back`, and hashing a directory can abort remaining cleanup. Validate exact expected filename/hash/type per directory, isolate cleanup failures, and report actual removals. Partial/mismatched copies remain for intervention; rollback was not exercised.
- **P2 — smoke validation:** P:79 omits ProximaInstall path and `whatif_ok` validation; Activation uses a prefix check. A shadow Install module could pass. Missing-property/null handling is incomplete without StrictMode; missing actions can resemble zero. Frozen outputs independently satisfy intended checks. No case-insensitive variable collision found; `$HOSTID`/`$mroot` avoid `$Host`/`$R` collisions.
- **P2 — overclaim:** `ops/acceptance/wp1319/MATRIX.md:239` says services/endpoints were measured unchanged; P:22–26 measures neither. `ops/acceptance/wp-pxl/RESULTS.md:38` cannot prove no running flow imports these modules. Correct both claims.

Limits to record: gateway snapshots compare PID/name/start, four file hashes and task names/states, not ancestry, task definitions, transient activity, loaded modules, services, endpoints or PSModulePath. Auto-import remains possible. `only_two_new_dirs` compares child names, not all content. Desktop gateway=true is vacuous. CreateRoot/OneDrive deviation is honestly recorded (RESULTS:26; DR `$.steps.P2a`); synchronization completion is unmeasured. VM commander PS7 actually used name import despite spec:57. Negative live fence leg is honestly unrun (MATRIX:238); no inference appears in driver. Secret-scan rc=0 covers listed evidence files, not the entire ZIP. Parser-run claims lack frozen transcripts.
```
</details>

