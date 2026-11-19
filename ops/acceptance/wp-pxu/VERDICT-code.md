# WP-PXU r1 — Review mã lượt 1/2 (trước khi đo)

- **Reviewer:** Codex CLI 0.169.0, gọi với `-m gpt-6-astra`, chạy trong container của phiên điều phối, chỉ đọc, sandbox chỉ ghi được vào thư mục riêng. Model tự khai **`KHONG_do_duoc`**. Thời gian 02:02:19Z–02:04:28Z ngày 19/11, rc 0. Verdict gốc có sha256 `7f938fcd…`.
- **Đối tượng:** commit `ebd625c31` (tree `4ace93a7…`). `ProximaInstall.psm1` `55b16912…`, `ProximaInstall.Tests.ps1` `e0e35ba5…`, SKILL.md `b471c43b…`. Review tĩnh, không chạy PowerShell.

## Verdict: `request_changes` (không có P0)

| Mức | Finding | Xử lý |
|---|---|---|
| P1 | Sau khi kiểm vẫn xoá **theo đường dẫn**. Tráo junction trung gian (quarantine, `Programs`) hoặc thay `installer.exe` sau khi kiểm thì sẽ xoá nhầm đối tượng chưa kiểm | **Sửa bằng handle** (phiên điều phối chọn, không thu hẹp hợp đồng). Mở bằng `OPEN_REPARSE_POINT`, kiểm đường dẫn cuối bằng `GetFinalPathNameByHandle`, băm qua chính handle, xoá bằng `SetFileInformationByHandle(FileDispositionInfo)` |
| P2 | Junction xuất hiện muộn ở `InstallDir` lệch đặc tả (đặc tả: chỉ gỡ liên kết, báo `RESIDUE_CHANGED`) | Làm đúng đặc tả qua handle |
| P2 | Ràng buộc thêm ngoài §1.1: từ chối UNC; snapshot tiến trình rỗng thành `NOT_MEASURED`; cắt khoảng trắng `DisplayName`; `-InstallerBytes` không nhận chuỗi số | Căn theo đặc tả |
| P2 | Harness chỉ từ chối scratch/report nằm trong cây git của AddonRoot | Kiểm mọi tổ tiên của đường xuất ra |
| P2 | CU06 được tính chỉ vì có `NOT_MEASURED`; tiến trình con không mang culture của cha | Đòi đúng nguyên nhân; truyền và đối chiếu culture |
| P2 | Báo lỗi xoá quarantine quá mức; tiêu đề SKILL.md "trước khi xoá bất cứ thứ gì" không đúng | Tách hai trường hợp; sửa câu chữ |

Gửi Executor lượt 2/2 (Fable). Bản sửa phải qua đo native trên Desktop, rồi review lượt 2/2 (gộp kiểm bản sửa và kết quả đo).

<details><summary>Nguyên văn verdict của reviewer (sha256 7f938fcd…)</summary>

```text
VERDICT: request_changes

Model: KHONG_do_duoc. Provider: OpenAI; surface: Codex tool session, Linux; transport: tool-mediated. Independent static review only; no network, PowerShell execution, repository modifications, or git writes.

Reviewed HEAD: `ebd625c31bb3bb0fb70bffad02e018168a29b604`; tree: `4ace93a758679745fac35fab4834e997102b7320`; branch: `ccr-8ee03d7f-vnmqk0`. All three supplied SHA-256 values match. References below: M = `.agents/skills/proxima-control/scripts/ProximaInstall.psm1`; T = `.agents/skills/proxima-control/tests/ProximaInstall.Tests.ps1`; S = `.agents/skills/proxima-control/SKILL.md`, relative to `/home/user/tra-luat`.

No P0 identified.

- **P1 — Deletion can escape verified objects. M:185, M:402, M:424, M:440.** Verification closes the installer handle before deletion; ancestor checks also precede deletion. After quarantine verification, another process can move that directory aside and replace its name with a junction to an unrelated directory containing `installer.exe`; `File.Delete(quarantineItem)` then follows the intermediate junction and deletes that unrelated file. Similarly, swapping `Programs` after line 402 can redirect deletion to an outside empty `Proxima` directory. Even without junctions, replacing the verified installer can cause deletion of an unverified file. Atomic rename prevents the original N3 stale-snapshot recursive deletion, but does not bind subsequent operations to verified objects. Hold appropriate directory/file handles against replacement through deletion, or establish an explicitly approved narrower concurrency contract. S:108 documents only process/registry snapshots, not these filesystem races.

- **P2 — InstallDir junction race violates the required result/behavior. M:406–409, M:422–437.** A junction introduced by TestHook is retained with `RESIDUE_CHANGED`; frozen §1.1 requires unlinking it. That conservative choice protects its destination but remains a contract deviation. A junction introduced after the last check is unlinked by the nonrecursive delete, recorded as an empty-directory removal, and can yield `CLEANED` instead of mandatory `RESIDUE_CHANGED`. Add both timing cases and object-identity evidence.

- **P2 — Additional argument/provider restrictions are not in §1.1. M:84–86, M:107, M:132, M:337–342.** An existing ordinary absolute UNC directory is rejected solely for lacking a drive letter. An injected empty process snapshot returns `NOT_MEASURED` although it contains no blocker. Leading whitespace is stripped from DisplayName, so `' Proxima'` blocks despite not starting with `Proxima`. Numeric strings convertible to the specified `<long>` parameter are rejected. These conservative choices need contract agreement or implementation alignment; drive-letter-only support is not implied by “absolute.”

- **P2 — Output can enter an unrelated Git tree. T:350–360.** Protection checks only ancestors of AddonRoot and the harness. Passing scratch/report under another repository succeeds, contrary to the blanket Git-tree refusal. Walk output ancestors for `.git` before permitting either write, including a `.git` worktree file.

- **P2 — Counterexample evidence is insufficiently specific. T:268–307, T:321, T:759.** CU06 accepts PU21 merely for returning `NOT_MEASURED`; it never verifies that the error is the expected hook write into the prematurely deleted updater. A different PU21-only exception producing that code can receive credit. Assert the declared exception/cause and relevant filesystem evidence. Child startup also neither propagates parent thread culture nor compares reported culture: a parent explicitly set to tr-TR can credit children running in the OS default culture.

- **P2 — Failure reporting overstates observations. M:445–452; S:100–102.** Any IOException while deleting an existing quarantine is described as newly gained entries without checking its contents; a sharing violation on an empty directory produces the same report. Distinguish measured change from unexpected I/O failure (`NOT_MEASURED`). Documentation lists that code under refusal “before deleting anything,” although the outer catch can return it after InstallDir deletion; the parenthetical caveat does not make that heading accurate.

Static conformance otherwise: defaults match (§1.1; M:9–10, M:302–306); targets are fixed (M:350–352); OS providers, process-name normalization and three preconditions are present (M:15–39, M:103–136, M:355–369). Both preliminary checks precede removal; hidden/system entries count, and updater name/type/size/hash are checked (M:139–191, M:371–380). Quarantine uses same-parent Directory.Move and re-verifies; refusal restores or records retention without overwriting an occupied original name (M:252–296). Midway exceptions attempt restoration before installer deletion, retain/report quarantine afterwards (M:468–479). No production recursive delete exists.

`WOULD_REMOVE` with `ok=false` is correct; hardlink acceptance is expressly permitted and its other name is checked (T:525–550). WhatIf performs preliminary checks without mutation; hook is hidden and called once on an actual removal path, zero times for preview/no-op. Result mapping, unexpected-error catch and single export are otherwise present (M:385–483).

PU01–PU22, including PU21b/c, have explicit assertions, without success-by-early-return. Junction/hardlink fixtures need no elevation; symlinks require Developer Mode or elevation, with failure classified setup_error. All eight CU anchors are unique; mutations affect scratch copies. Child parse/setup errors receive rc=2 and cannot be credited; undeclared failed cases are rejected. No apparent variable collision, bracket-wildcard, Get-Content/null, missing-Force, or unavailable Framework API issue; comparisons use Ordinal/invariant casing. Add-Type/PInvoke remains unmeasured.

S:87–108 otherwise describes the workflow accurately. PM05’s version regex sees only allowed existing versions; PM07 receives no extra Import-Module example or forbidden token, and new file references exist. This is static evidence, not a legacy-test pass.

Native verification required:

- PS5.1/.NET 4.8 and PS7, StrictMode 3, tr-TR in parent **and children**: 24/24 baseline, 31/31 counterexamples, no setup errors.
- Junction swaps, post-verification replacements, occupied restore destination, sharing/ACL failures, hidden/system entries, PInvoke fallback and hardlink preservation.
- Legacy Activation 30/30 and 36/36; Manifest 12/12; Config 46/46; Control 38/38. No real installer/uninstaller execution.
```
</details>
