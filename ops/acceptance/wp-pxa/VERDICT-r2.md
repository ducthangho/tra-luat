# WP-PXA r2 — Review offline K4 (ADR-0060), 2/2 lời gọi Codex do chủ kho cấp (E2)

- **Căn cứ:** finding P2 của connector Codex trên PR #1378, head `953ba9d8` (review `5972629197`, comment `4626897634`). Đặc tả `ops/specs/wp-pxa-r2.md`, lease `ops/leases/wp-pxa-r2-g1-executor.yaml`.
- **Ngân sách:** PR #1378 đã vượt trần lời gọi Codex mặc định (E2, ADR-0067). Chủ kho cấp **2 lời gọi** qua AskUserQuestion ngày 19/11, khoảng 09:55Z.
- **Reviewer:** Codex CLI 0.169.0, `-m gpt-6-astra`, chạy qua `.claude/dev/launcher.py run`, chỉ đọc, trên ứng viên cục bộ **trước khi đẩy** (ADR-0060 M12).
  - `run.json` của cả hai lượt ghi `model_phuc_vu_trang_thai = DO_DUOC`; mọi khung response đều là `gpt-6-astra`.
  - Reviewer tự khai model là `KHONG_do_duoc`.

| Lượt | Head | `run.json` | Thời lượng | Kết luận |
|---|---|---|---|---|
| 1 (`315c2e65`) | `9a495967e3a80910148092cdf67510e7f54ce96e` | `trang_thai xong`, `ma_thoat 0`, `stdout_sha256 715a16c6…` | 121,9 s | `KET_LUAN: approve`. Mở 1 P3: RESULTS khai rộng ("luôn" truyền culture; khái quát "các lượt trước") |
| 2 (`b4dcb23d`) | `1cf535fddbd81f343872c81582b301f08bd79f45` | `trang_thai xong`, `ma_thoat 0`, `stdout_sha256 1ddb3cfa…` | 118,3 s | `KET_LUAN: approve`. P3 lượt 1 đã đóng. Mở P3 mới, hẹp hơn: chưa có liên kết băm nối 12 report "N2" với lượt N2 trong bảng RESULTS |

**P3 còn mở của lượt 2** có mã `offline-k4b-P3-1`. Chủ kho miễn, neo đúng SHA: https://github.com/ducthangho/tra-luat/pull/1378#issuecomment-7006027112.

**Connector trên head `1cf535fd`:** "Didn't find any major issues" (issue comment `7006080824`, `has_any_findings=false`).

**Land:** `kiem-merge` báo ĐỦ ĐIỀU KIỆN trên `1cf535fd`. Merge commit `96b6a33d`, xem `ops/land/pr1378-wp1319-land-evidence.yaml`.

<details><summary>Nguyên văn stdout lượt 1 (sha256 715a16c67a19665b8acb9474a4b130bb0814a17df012a7494710932f95968d64)</summary>

```text
Reviewed SHA: `9a495967e3a80910148092cdf67510e7f54ce96e`; tree: `7e3d4e778e3739937baeeac02566b5bac0376f48` (`verification.json:$.head,$.tree`). Independent, read-only offline review; provider OpenAI, surface Codex, transport local tools. Exact model ID: `KHONG_do_duoc`.

References: **H** = `.agents/skills/proxima-control/tests/ProximaActivation.Tests.ps1`; **I** = sibling `ProximaInstall.Tests.ps1`; **R** = `ops/acceptance/wp-pxa/RESULTS.md`. Evidence paths are relative to `../ex/`; `verification.json` is this review’s local audit output.

| Check | Result and evidence |
|---|---|
| Delta scope | PASS. Requested `git diff --stat` reports four files, 151 insertions, three deletions. H is the only non-`ops/` change; the module and every other `.agents` file are unchanged (`verification.json:$.delta`; H:8). |
| Frozen metadata | Spec and sorted write-set hashes match the lease (`verification.json:$.spec_sha256,$.write_set_hash`; `ops/leases/wp-pxa-r2-g1-executor.yaml:18,24`). |
| Culture initialization | PASS. H:13–18 sets thread culture/UI culture and both thread defaults before report construction or tests. Matches I:16–21. No separate `$culture` variable collides with `$Culture`; initialization uses `$requestedCulture` (H:10–18). |
| Child arguments | PASS. H:228 passes nonempty parent culture through existing `ConvertTo-ArgText` (H:81–85,230), matching I:287–289. `tr-TR` needs no quoting; spaces, quotes and trailing backslashes retain existing escaping. |
| Credit gate | PASS. Both start/end cultures use case-sensitive `-cne` (H:268–270; I:330–332), before `killed` at H:276. Mismatch throws, becomes `not_credited` (H:278–281), CX `setup_error` (H:121–126), and rc 2 (H:832). StrictMode missing-property errors also follow this rejection path; older harness reports additionally fail provenance (H:12,266–270). |
| Invariant culture | LIMITED, safe rejection. Empty parent name omits `-Culture`; explicit empty input does not select invariant culture. A child with a nonempty default is rejected; an invariant child can pass. This matches I and the nonempty-only spec (`H:13,228,269`; `ops/specs/wp-pxa-r2.md:23`). |
| Evidence integrity | PASS. All 16 listed file sizes/hashes match MANIFEST, with no unlisted payload. Zip hash is `e1d6505b…`, manifest `297d4093…`; archive bytes match extraction (`verification.json:$.manifest,$.zip_sha256,$.archive_matches_extraction`). |
| Build provenance | PASS. Six replacements replayed on the old Git blob produce byte-identical candidate H. Harness `e5cc81c1…`, module `bb96cd58…` match `evidence/R2-result.json:$.hashes`. Candidate minus exactly H:228 produces mutant `cb0e231a…` (`evidence/build.py:56`; `verification.json:$.build`). |
| Windows results | PASS, frozen evidence reviewed, not rerun. PS7/PS5.1 each 36/36, rc 0, parent start/end `tr-TR`, all six CX killed with child `tr-TR`; parse errors zero. Mutant is 30/36, rc 2, all six CX not credited for `en-AU`/`tr-TR` mismatch (`evidence/R2-result.json:$.runs,$.parse_ps7,$.parse_ps51`). Raw reports/stdout agree (`verification.json:$.reports_verified`). |

Findings: **P3 — documentation overstatement**, R:46: “always” passing culture excludes invariant parents. Scenario: an invariant-parent run on an en-AU host rejects children instead of propagating invariant culture. Qualify this as “when nonempty.” Also R:41 generalizes prior runs beyond the ten N1 CX01–CX05 children actually enumerated (`evidence/old-pxa-child-culture.txt:3–15`); restrict that assertion to inspected N1 reports. Neither weakens the verified tr-TR fix.

The original P2 is fully closed for the specified tr-TR acceptance: old children were en-AU despite tr-TR parents, and the new positive/negative evidence proves propagation and rejection. No open P0/P1/P2 or other merge blocker found in this delta (evidence cited above).

KET_LUAN: approve
```

</details>

<details><summary>Nguyên văn stdout lượt 2 (sha256 1ddb3cfa1dd6ae75472e6461ac1fa1a632150391de6c480b183bf0e4cfa0f0ac)</summary>

```text
Reviewed SHA: `1cf535fddbd81f343872c81582b301f08bd79f45`; tree: `efbd119cea400cca706cdcb7791c3204214fdf1c`. Independent read-only, offline review. Provider: OpenAI; surface: Codex; transport: local tools. Exact model: `KHONG_do_duoc`.

References: **H** = `.agents/skills/proxima-control/tests/ProximaActivation.Tests.ps1`; **I** = sibling `ProximaInstall.Tests.ps1`; **R** = `ops/acceptance/wp-pxa/RESULTS.md`; evidence paths below are relative to `../ex/` unless specified.

| Check | Result and evidence |
|---|---|
| Delta scope | PASS. Requested `git diff --stat 953ba9d8..1cf535fd`: four files, 152 insertions, three deletions. H is the only non-`ops/` change; module and every other `.agents` file are unchanged. Paths match `ops/leases/wp-pxa-r2-g1-executor.yaml:19–23`. |
| Spec/lease | PASS. Recomputed spec hash `99abe988…` and sorted write-set hash `20047071…` match lease lines 18,24. Spec’s pending budget is historical; lease lines 45–46 record subsequent authorization. |
| Initialization | PASS. H:13–18 sets thread culture/UI culture and both defaults before report construction and tests, matching I:16–21. `$requestedCulture` avoids a case-insensitive `$Culture`/`$culture` collision. |
| Arguments/invariant | PASS within stated scope. H:228 forwards nonempty culture through `ConvertTo-ArgText` (H:81–85,230), matching I:287. `tr-TR` needs no quoting; existing escaping handles quoted paths. Empty parent names omit the argument; empty input does not select invariant culture. Nonempty-default children are rejected; invariant children can pass (H:13,269; R:47). |
| Credit gate | PASS. Both child start/end fields use case-sensitive `-cne`, matching I:330–332 (H:268–270). Technically PowerShell string comparison is invariant-culture, not `StringComparison.Ordinal`; canonical culture names make this immaterial here. Check precedes `killed` (H:276); mismatch becomes `not_credited`, CX setup error, rc 2 (H:278–281,117–126,832). StrictMode missing-field errors also reject; older harness hashes fail provenance first (H:12,266). |
| Frozen integrity | PASS. All 16 manifest-listed files match size/SHA256; only MANIFEST itself is unlisted (`MANIFEST.json:$.files`). Archive matches extraction byte-for-byte; zip hash `e1d6505b…`, manifest `297d4093…` agree with R:62. |
| Build provenance | PASS. Replaying six `rep()` replacements on the old Git blob produces candidate H byte-for-byte (`evidence/build.py:18–55`). Harness `e5cc81c1…`, module `bb96cd58…` match `evidence/R2-result.json:$.hashes`. Removing exactly H:228 produces mutant `cb0e231a…`, matching `$.hashes.mutant`. |
| Windows results | PASS, reviewed frozen results; not rerun. PS7/PS5.1 each 36/36, rc 0; parent start/end tr-TR; CX01–CX06 killed with child tr-TR. Mutant 30/36, rc 2; all six not credited for en-AU/tr-TR mismatch. Raw reports/stdout agree (`evidence/R2-result.json:$.runs`; respective reports `$.counterexamples`). Parsers report zero errors; dry-run passed; scan rc 0 (`$.parse_ps7,$.parse_ps51`; `evidence/dryrun/R2-result.json:$.outcome`; `evidence/secret-scan.json:$.rc`). |
| Historical evidence | Ten N1 children en-AU versus tr-TR parents confirmed (`evidence/old-pxa-child-culture.txt:3–16`). Expanded list hash matches `9e77f3b5…`: N1 10, N2 12, PXU N1 12, all en-AU (`../old-child-culture-all.txt:1–34`). This is operator-relayed evidence outside the frozen zip. |

**Open P3 — unproven exact N2 association, R:41.** The list’s N2 names support the grouping, but contain no parent report, commit hash, or archive membership proving “the run claimed in the table” (R:23). Scenario: retained/relabelled scratch reports belong to another N2 invocation. Qualify that association as operator-reported, or supply a hash-linked parent/archive mapping; verify both editions’ scratch IDs against it. This documentation correction has no runtime risk.

Call 1’s nonempty-culture wording issue is closed (R:47); its historical-count overgeneralization is corrected (R:41–42), with the narrower provenance P3 above remaining. The original P2 is fully closed for specified tr-TR acceptance. No open P0/P1/P2 or other merge blocker found.

KET_LUAN: approve
```

</details>

