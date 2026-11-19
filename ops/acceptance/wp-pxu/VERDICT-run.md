# WP-PXU r1 — Review lượt 2/2 (bản sửa mã + kết quả native)

- **Reviewer:** Codex CLI 0.169.0, gọi với `-m gpt-6-astra`, chạy trong container điều phối, chỉ đọc. Model tự khai **`KHONG_do_duoc`**. Thời gian 02:55:03Z–02:58:07Z ngày 19/11, rc 0. Verdict gốc có sha256 `1cfb9b5b…`.
- **Đối tượng:**
  - mã tại `42fb4743a` (bản checkout `d2f86cda7` chỉ khác ở lease);
  - bộ con bằng chứng chuyển từ Desktop: zip `92756e2c…`, 25/25 tệp khớp MANIFEST `508ab7b1…` của zip đầy đủ `cdb2d062…`.

## Verdict: `request_changes` (không có P0)
| Điểm | Kết luận của reviewer |
|---|---|
| Toàn vẹn, nguồn gốc | Khớp. Băm module `7b364dc3…` trong mọi report; băm harness đúng blob ở từng commit; 18 report con có băm mutant dựng lại độc lập khớp, chạy với `tr-TR`/`tr-TR` |
| Kết quả native | N1b mặc định 29/30 ở cả hai runtime; PU28 `blocked_by=System.IO.IOException`. PU13 lỗi 1314 do môi trường, loại khỏi số đạt là đúng |
| Phản chứng | Cả 9 CU khớp **đúng** tập ca khai báo và tiền tố lý do, ở cả hai runtime. Nhưng **harness thực tế cấp tín dụng 0/9**, không phải 9/9 |
| Cài đặt bằng handle | Cấu trúc P/Invoke đúng; `FileDispositionInfo` dùng BOOL 4 byte; không còn xoá theo đường dẫn ở luồng thường; có chặn nạp lại Add-Type |
| P2 của review 1 | Đã sửa hết |
| Bản vá harness của phiên điều phối | Đúng về mặt tĩnh; **chưa chạy** |
| Hồi quy | Chỉ thấy qua tệp tóm tắt dẫn xuất: Activation 30/30 và 36/36, Manifest 12/12, Config 46/46, Control 38/38 |

**P1 (phát hiện tĩnh, chưa tái hiện native).** `ProximaInstall.psm1:504–516`: nhánh "InstallDir đã thành reparse point" gỡ liên kết **trước** khi kiểm đường dẫn cuối. Nếu `Programs` bị tráo sang một thư mục bên ngoài có sẵn junction `Proxima`, junction ngoài phạm vi ấy bị gỡ. Đích của nó còn nguyên, nhưng một mục không thuộc phạm vi đã bị xoá. Cách sửa reviewer đề xuất: đưa phép kiểm final path lên trước mọi nhánh xoá; mở rộng PU24 với junction bên ngoài, khẳng định 0 hành động và liên kết còn nguyên.

**P2.** Hai câu trong RESULTS sai, đã sửa:
- (a) PU13: phần hardlink có chạy kiểm trước khi gặp lỗi symlink;
- (b) N1b: tiến trình con có chạy; lỗi xảy ra sau đó.

## Trạng thái ngân sách: **dừng ở Review Rescue Checkpoint**
- Executor 2/2, review 2/2, native 1/1 + chạy lại 1/1 đều đã dùng hết.
- Bản sửa P1 là **mã sản phẩm**. Phiên điều phối **không tự sửa**; cần chủ kho nâng trần:
  - +1 lời gọi Executor;
  - +1 lượt native Desktop;
  - +1 review.
- Với cùng lượt đo, harness đã sửa ở HEAD sẽ có dịp chạy thật.

<details><summary>Nguyên văn verdict của reviewer (sha256 1cfb9b5b…)</summary>

```text
VERDICT: request_changes

Model: KHONG_do_duoc. Provider: OpenAI; surface: Codex/Linux tools; transport: tool-mediated. Independent, read-only review; no network or native execution.

Reviewed `42fb4743a3355b961769f09095c5515a2016d1c0`, tree `bd723204cee4a8a94fa4f1f70db1c35cc8d12df5`. Actual checkout: `d2f86cda7fb5e6ed9f60175cdd52997d758adb30`, same branch; only lease bookkeeping differs. Code/spec inspected are identical.

References: M/T/S = `.agents/skills/proxima-control/{scripts/ProximaInstall.psm1,tests/ProximaInstall.Tests.ps1,SKILL.md}`. E = supplied EVID; D = E/evidence-pxu. JSON case references select by `id`. Mutation-table references use T at `b0ce2443b`; other code references use reviewed SHA.

| Check | Result and evidence |
|---|---|
| Integrity | Spec SHA matches `4c37b3b5…db914`. Subset ZIP SHA: `92756e2cb8a1e933a3b677c1be5ed52dc050d2d309568024814969545f581271`. MANIFEST SHA matches supplied `508ab7b1…31f89`. All 25 manifest-listed extracted files match size/hash; ZIP members match extraction. MANIFEST itself and derived summary have no rows. Full 63-file ZIP unavailable: its hash cannot be independently attested. |
| Report provenance | All four supplied parent reports’ `$.source_hashes` match git module SHA `7b364dc361661000c967f9f7697d7a78f864cdbf5b655e3078db6180b7a129d0`, unchanged across three commits. `$.harness_sha256`: N1=`49f23361…e599`, N1b=`d2d9bc19…a12c`, matching respective git blobs; reviewed harness=`c1522d0a…6b3a5`. |
| Child provenance | All 18 `children-N1/*report.json`: module hash equals parent mutation record and independently reconstructed mutant; nine distinct hashes, consistent across runtimes. Harness hash equals parent; edition matches; culture/start/end=`tr-TR`. See local `audit.py` and `audit-results.txt`. |
| Native positives | Both N1b default reports: 29/30, failed/skipped empty. `$.cases`: PU01–PU12, PU14–PU28 including PU21b/c each passed; PU18=`refused=22`, PU22=single export, PU26=`forms=14`, PU28=`blocked_by=System.IO.IOException`. N1 counterexample parents contain the same 29 baseline passes under tr-TR. N1 default counts are available only through derived summary lines 10/17. |
| PU13 | `$.cases[id=PU13]` reports symlink creation error 1314/administrator privilege required: environment-limited setup failure, correctly excluded from passed. Hardlink qualification below. |
| Handle implementation | M:72–147 uses SafeFileHandle, DELETE/read-attributes/synchronize plus GENERIC_READ for files; OPEN_EXISTING, OPEN_REPARSE_POINT, directory BACKUP_SEMANTICS; no delete sharing, files also deny writes. FileDispositionInfo=4 with four-byte BOOL=1 is correct, not a pointer-sized structure. No evident ABI-width defect. |
| Deletion/restoration | Ordinary InstallDir, verified installer, quarantine use handle dispositions (M:527,538,551); no production path-based deletion. Hash uses the deletion handle. Error 145 is distinguished from other failures; quarantine retention is recorded. Handles close in finally; restoration never overwrites (M:423–597,743). Add-Type has re-import guard (M:154). Final paths strip device/UNC prefixes, compare OrdinalIgnoreCase against canonical root (M:132,226,663). **P1 exception below.** |
| Review-1 P2 fixes | Late direct junction unlink implemented; UNC classifier, empty process snapshot, untrimmed DisplayName, numeric-string long conversion corrected (M:241,273,294,607). All-output Git ancestor checks include `.git` files (T:75–88,397–400). CU06 requires cause/state; child culture propagated/checked (T:287,330). Quarantine error reporting and S:100–107 corrected. |
| Dispatcher patch | T:322–370 is statically sound for requested credit safeguards: completed parent cases only; rejects global setup, skips, ID errors, unknown/target setup IDs; requires actual declared failures with matching reasons. Cannot credit zero measurement or later-added parent setup failures. Matching setup IDs does not independently establish environmental causation. **Unexecuted.** |
| Legacy/docs | Derived, unmanifested D/N1-all-reports-summary.txt: both runtimes Activation 30/30 and 36/36, Manifest 12/12, Config 46/46, Control 38/38. Raw legacy reports absent. S preserves PM05 version-regex and PM07 import/token/reference constraints; workflow/result descriptions otherwise align, except P1 undermines S:108–111. |

Each row below matches **both** child reports’ exact failed set and every declared reason prefix; no mismatches. Ignoring exit-code disqualification, all satisfy the original credit predicates. Actual N1 harness credit: **0/9 per runtime**, not 9/9 (`$.counterexamples[*].verdict`).

| CU | Failed cases |
|---|---|
| CU01 | PU05, PU06, PU17, PU21b |
| CU02 | PU08, PU25 |
| CU03 | PU07, PU10, PU21 |
| CU04 | PU11 |
| CU05 | PU14 |
| CU06 | PU05, PU21, PU21b, PU25, PU28; DirectoryNotFoundException plus present=False matches |
| CU07 | PU21, PU25, PU28 |
| CU08 | PU24 |
| CU09 | PU28 |

No P0 identified.

**P1 — Outside junction can be deleted, M:504–516.** After preliminary checks, swap Programs for a junction to an outside directory containing its own Proxima junction. Open follows the intermediate junction; the reparse branch marks the outside Proxima link for deletion **before** canonical-path validation. Its destination survives, but an unauthorized outside entry is removed. Thus review-1 P1 is incompletely fixed. Move final-path validation before every deletion branch; extend PU24 with an outside junction and assert zero actions plus link preservation. This is a static counterexample, not a native reproduction.

**P2 — Evidence narrative inaccuracies, ops/acceptance/wp-pxu/RESULTS.md:22,27.** T:571–589 runs hardlink assertions before symlink failure at T:595; only its specific outcome emission at T:600 is lost. Also child launch/wait precedes the erroneous N1b `$report.cases` access: “before any child ran” is unsupported. Correct both claims.

Exact limits to record: §4 literal PASS is unmet: setup_error_ids is nonempty, defaults are 29/30, and counterexamples lack native harness credit. Legacy counts meet numeric criteria only through derived evidence; reviewed artifacts contain no real installer/uninstaller execution. PU13 symlink behavior is unmeasured; hardlink assertions completed by control-flow evidence, but its accepted/refused outcome lacks standalone reporting. Corrected harness is unexecuted; UNC evidence covers classification only. These limits do **not** support approve_scoped while P1 remains.
```
</details>

---

# Review lease g2 (1/1): bản sửa P1 + kết quả N2

- **Reviewer:** Codex CLI 0.169.0, `-m gpt-6-astra`, chạy trong container điều phối, chỉ đọc. Model tự khai **`KHONG_do_duoc`**. Thời gian 03:31:51Z–03:34:18Z ngày 19/11, rc 0. Verdict gốc có sha256 `7c1d8af2…`.
- **Đối tượng:**
  - mã tại `9cdfeaf5b` (HEAD lúc review là `95bf31e17`, chỉ khác sổ sách);
  - bộ con N2: zip `6152f3d9…`, MANIFEST `c03c1235…` của zip đầy đủ `64efd2de…`.

## Verdict: **`approve_scoped`**. Không còn P0/P1; P1 của review 2 đã đóng.
| Điểm | Kết luận |
|---|---|
| Nguồn gốc | Băm module `81c1164b…` và harness `b2627283…` khớp blob git trong cả 4 report |
| Sửa P1 | `M:507` kiểm final path **trước cả hai** nhánh xoá (`M:512`, `M:529`). PU23 xác nhận trên máy thật rằng junction trực tiếp ở InstallDir vẫn được gỡ; PU24/PU29 từ chối khi `Programs` bị tráo |
| Thứ tự xoá, khôi phục | Không thấy lỗi mới |
| Test | PU29 đúng kịch bản; PU13 tách hardlink/symlink; `requiredIds` 32/42; CU08 và CU10 khai báo đúng; bản vá rc-2 không đổi so với `42fb4743a` và đúng |
| Native | 31/32 · 31/32 · 41/42 · 41/42; `setup_error_ids=[PU13s]`; 10/10 CU `killed` ở cả hai runtime, khớp đúng tập ca; reviewer dựng lại độc lập 20 băm đột biến |

**P2 (câu chữ):** RESULTS dòng 52 vẫn ghi hardlink "chưa đo"; dòng 29 và 53 còn lời khai đã cũ. **Đã sửa**, có ghi rõ là đã được thay thế và giữ lại lịch sử.

**Giới hạn phải ghi:** xem mục "Kết luận" cuối `RESULTS.md`.

<details><summary>Nguyên văn verdict của reviewer (sha256 7c1d8af2…)</summary>

```text
VERDICT: approve_scoped

Model: KHONG_do_duoc. Provider: OpenAI; surface: Codex/Linux tools; transport: tool-mediated. Independent review; no network, native execution, repository modifications, or git writes.

Reviewed HEAD `95bf31e17bd0e542b75751db4382599eea9bfc62`, tree `59b977a5dbff83774bf970e24cb74e8066428a60`, branch `ccr-8ee03d7f-vnmqk0`. Native source: `9cdfeaf5b1eb17d0d75eb4ce6defe5a29ba69e7a`; subsequent changes affect only RESULTS and lease bookkeeping. Worktree clean.

References: M/T = `.agents/skills/proxima-control/{scripts/ProximaInstall.psm1,tests/ProximaInstall.Tests.ps1}`; R = `ops/acceptance/wp-pxu/RESULTS.md`; E = supplied EVID; D = E/evidence-pxu2. Report names below have prefix `PXU-N2-` and suffix `-report.json`. JSON selectors identify cases by `id`.

| Check | Evidence and conclusion |
|---|---|
| Integrity | Frozen spec SHA matches `4c37b3b5…db914`. Subset ZIP SHA matches `6152f3d9565b5911147708c9487be4e0420620f48d0801117525b2d5f7759d60`; MANIFEST matches `c03c123505751a0d85752000ccd724996123d234d49bf8b1d22110153513c5fb`. All six relayed manifest-listed files match sizes/hashes; all seven ZIP files match extraction, including MANIFEST. |
| Source provenance | Each report’s `$.source_hashes['scripts/ProximaInstall.psm1']` equals git-blob SHA256 `81c1164bf913b181ae5e8e88a04b4498abd592d1ff2e3a25f6cf24d7ed57a82a`; `$.harness_sha256` equals `b26272831150b072a1149eb1fff771a60edfd3a5ad190a1027e9010fb7692cae`. |
| P1 fix | M:507 validates final path before BOTH deletions, M:512 and M:529. OPEN_REPARSE_POINT opens the final link itself (M:103); PU23 passes with empty/nonempty destinations and requires unlink plus preserved destination (T:776–802). This supports the link’s own-path behavior on the measured host. PU24/PU29 reject objects reached through swapped Programs. |
| Removal/restoration | M:454–492 atomically renames updater, validates held directory/file paths and types, hashes through the deletion handle. M:529–574 deletes InstallDir, verified installer, then nonrecursively deletes quarantine. M:580–599 closes handles before restoration; M:430–447 never overwrites an occupied original name. Post-installer failures retain/report quarantine. No new deletion-order defect identified. |
| Tests | T:828–859 implements review-2’s scenario: outside junction remains a reparse point, marker exists, RESIDUE_CHANGED, zero actions. T:567–604 separates measurable hardlink from privileged symlink. T:40–42 requires 32 baseline/42 counterexample IDs. CU08 targets PU24+PU29; CU10 reproduces validation bypass only for reparse objects, targeting PU29 (T:1013–1023). |
| Dispatcher | Entire Invoke-Counterexample is byte-identical to 42fb4743a. T:322–369 correctly uses completed parent cases, checks provenance/culture, rejects global setup/skip/ID errors and unknown or target setup failures, then requires exact target failures with declared reason prefixes. Matching setup IDs alone does not prove environmental causation. |
| ps51-Install-default | Desktop, en-AU, 31/32. |
| ps7-Install-default | Core, en-AU, 31/32. |
| ps51-Install-cx-trTR | Desktop, tr-TR, 41/42. |
| ps7-Install-cx-trTR | Core, tr-TR, 41/42. |
| Common native fields | All four: `$.failed_ids=[]`, `$.setup_error_ids=[PU13s]`, `$.id_errors=[]`, no skips/global setup error; ending culture matches starting culture. `$.cases[PU13].reason=hardlink=CLEANED`; PU23/PU24/PU29 passed; PU28 reports `blocked_by=System.IO.IOException`. |
| Counterexamples | Both `$.counterexamples` arrays contain ten killed mutants, rc=2, exact declared failure sets and matching reasons. CU08={PU24,PU29}; CU10={PU29}; others match T:960–1032. Every env_limited_ids={PU13s}, subset of parent setup errors and disjoint from targets; child_culture=tr-TR. All 20 mutation hashes independently reproduced from recorded edits. |

P0/P1: none outstanding identified; review-2 P1 closed.

P2, nonblocking narrative inconsistency: R:22 and R:27 correct both specific review-2 errors, but R:52 still calls hardlink unmeasured; R:29/53 retain stale “HEAD/unexecuted” wording. Reading the historical summary alone misstates coverage. Change R:52 to symlink only and explicitly date/supersede the harness statements with N2. Cross-check against R:69–71; documentation-only correction risks accidentally erasing historical failures, so preserve those results.

Exact limits to record:

- Literal spec §4 PASS remains unmet: PU13s has setup_error 1314, not pass; default runs are en-AU, although baseline cases also execute within tr-TR counterexample runs. H.7 keeps symlink behavior unmeasured; it does not waive PASS.
- Legacy harnesses were not rerun at 9cdfeaf5b. Carry-forward is reasonable static scope evidence: only Install module/harness changed since N1; legacy imports and SKILL are unchanged. Manifest hashes the whole add-on but compares before/after, not frozen Install bytes (ProximaManifest.Tests.ps1:105,426). Historical counts are not newly verified native passes; raw legacy reports are absent.
- UNC coverage is classification only (T:888–903). Full ZIP, omitted files, child reports/logs and parser outputs were unavailable. Parent records substantiate counterexample credit; full-ZIP hash cannot be independently attested. Secret-scan.json reports rc=0, not an independent rescan.
- No real installer/uninstaller execution is evidenced here. This approval covers the measured cleanup behavior, not full §4 acceptance or the end-to-end uninstall criterion still pending under MATRIX.md:215.
```
</details>

