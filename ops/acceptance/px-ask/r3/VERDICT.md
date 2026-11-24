# PX-ASK-SONG r3 — review độc lập Codex offline (2/2 lời gọi): approve

**Căn cứ:** đặc tả `ops/specs/px-ask-r3.md` §4, lease `ops/leases/px-ask-r3-g1-claude.yaml` (`review_calls_limit: 2`).

## Các lượt
| lượt | run (`launcher.py run`) | head review | prompt sha256 | kết luận | sandbox | model phục vụ |
|---|---|---|---|---|---|---|
| 1 | `f42c8527`, 06:44:24Z → 06:46:08Z, `ma_thoat` 0 | `94c425d3e2f7740ac573335175e80d6a01f5ad10` | `a3cb9a6b…c28f` | **approve**, 2 P3 | `DO_DUOC` (bwrap `--unshare-net`, workspace-write) | `gpt-6-astra` (`DO_DUOC`, 10 response) |
| 2 | `1065dd67`, 06:47:48Z → 07:06:35Z, `ma_thoat` 0 | `981f7616efcdd85ff56b9815821b674fce79b8d5` (delta từ `94c425d`) | `4839f57d…f85c` | **approve**, 0 finding mới; 2 P3 lượt 1 đã đóng | `KHONG_DO_DUOC` | `gpt-6-astra` (`DO_DUOC`, 11 response) |

- Lệnh, cả hai lượt: `python3 .claude/dev/launcher.py run --workspace <clone tại head> --expected-repo ducthangho/tra-luat
  --expected-root-commit e13f74bb… --expected-head <head> --prompt-file <p> --expected-prompt-sha256 <sha> -- /opt/node22/bin/codex exec
  -m gpt-6-astra --sandbox workspace-write --skip-git-repo-check -C <thư mục review> "…{PROMPT_FILE}…"`. Workspace là clone dưới `/tmp`.
- `effort`: không ghi trong `run.json` (null), cả hai lượt.
- Lượt 2: `sandbox_trang_thai` = `KHONG_DO_DUOC` theo `run.json`, tức launcher không quan sát được tiến trình sandbox ở lượt này. Ghi đúng như
  vậy, không suy ra từ lượt 1.
- Reviewer không chạy được PowerShell; kết luận về test là **đọc mã**. Phép đo Windows nằm ở `RESULTS.md`.

## Xử lý finding lượt 1
| finding | xử lý | bằng chứng |
|---|---|---|
| P3-1: đột biến so không phân biệt hoa thường ở `Test-PxcModelOf` sống sót | thêm 4 ca provider sai hoa thường (`GW`, `Prov`, `AUTO`), kiểm `px models GW` rỗng, thêm counterexample `CX13` (`OrdinalIgnoreCase` ở nhánh `P:`) | commit `981f761`; lượt 2 xác nhận cả 3 nhánh × 2 kiểu so đều đỏ; `CX13 credited=True` trên Windows (`RESULTS.md`) |
| P3-2: chú thích đầu module còn ghi luật `P/` | sửa thành luật ba dạng | commit `981f761`; lượt 2 xác nhận |

## VERDICT lượt 1 (nguyên văn, sha256 `b66458dd…6f62`)
Review: packet #1446 r3, commit `94c425d3e2f7740ac573335175e80d6a01f5ad10` against `b9ade4e2f3d489fe7e65c4ea928086fe627ec0c4`. Read-only, offline source review; no PowerShell execution or Windows-test attestation.

References below are repository-relative. Abbreviations: `M` = `.agents/skills/proxima-control/scripts/ProximaControl.psm1`; `T` = `.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1`; `MT` = `.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1`; `S` = `.agents/skills/proxima-control/SKILL.md`.

| Check | Result and evidence |
|---|---|
| Predicate | PASS. `M:78`, `M:82`, `M:219`, `M:220` implement exactly equality OR `P:` OR `P/`, with Ordinal membership and advertised-id equality, as required by `ops/specs/px-ask-r3.md:12`. No cross-provider acceptance or legitimate-id rejection found under this contract. |
| Edge inputs | PASS. Empty providers fail use/ask; empty models fail use/ask, while empty provider means unfiltered models (`M:483`, `M:485`, `M:506`, `M:519`). NUL is compared literally, not ignored; case and Turkish dotless-i aliases cannot match (`M:82`, `M:220`). Advertised `P::x`, `P:x/y`, and `P/x:y` belong to P by the specified prefix rule. A bare full id can itself be its provider; a full id containing either separator cannot (`M:78`). |
| Client call sites | PASS. `px use` validates provider/model presence (`M:483`), obtains filtered advertisements and calls `Test-PxcModel` (`M:494`, `M:496`). `px ask` validates provider (`M:484`), resolves explicit/selected model (`M:504`), then dispatches (`M:507`); Local dispatch reaches the shared ask implementation (`M:428`, `M:360`, `M:286`). |
| Endpoint/filter/Remote | PASS. `Invoke-PxcAsk` calls `Test-PxcModel` before journaling/POST (`M:286`). `px models` uses `Test-PxcModelOf` (`M:357`). `Invoke-ProximaOperation` validates provider/model arguments then delegates (`M:519`, `M:522`). Remote envelope validation checks types, not membership, and forwards strings to that operation (`M:383`, `M:407`). No executable slash-only membership path remains. |
| Regressions | PASS, with intentional compatibility changes. Former providers such as `gw:fast` with model `gw:fast/m1` now fail, explicitly required by `ops/specs/px-ask-r3.md:18`. Ordinary legacy slash ids remain accepted (`M:82`). Selection stays fingerprint-keyed with Ordinal provider keys (`M:108`, `M:498`); journal/body serialization preserves model strings (`M:291`, `M:293`, `M:129`). Remote hash consequence is accurate: self-hash changes, endpoint checks it before import, and connect fails handshake (`M:67`, `M:401`, `M:444`, `M:450`). |
| X5-10 | PASS for required coverage. Calls exported public px via `T:219`, `T:252`; four accepts, four use/ask rejects with zero POST, colon-provider rejection, exact filtered list, and one POST with exact model are asserted at `T:1049`, `T:1052`, `T:1058`, `T:1060`, `T:1063`. |
| CX12/mutants | CX12 admits advertised `gwz`, so use emits the exact named token (`T:1048`, `T:1054`, `T:1137`). `Get-Kill` splits once and uses literal Contains, so brackets are not wildcards (`T:1142`); credit additionally requires rc 1 and clean evidence (`T:1152`, `T:1161`). Dropping equality, dropping slash, or removing the provider colon check is caught by `T:1049` or `T:1058`. Survivors are detailed below. |
| Docs/version | PASS. Help and SKILL describe all three forms (`M:41`, `S:40`). Version 2.1.0 agrees across manifest `scripts/ProximaControl.psd1:5` (under the same add-on), `S:4`, `S:56`, `MT:14`, and `MT:363`. SKILL’s only other semver is permitted historical 1.0.1; PM05 allows it (`MT:339`). |
| Scope | PASS. All seven changed paths are explicitly in `ops/leases/px-ask-r3-g1-claude.yaml:23`; no out-of-lease changes. |

Findings:

- **P3 — Membership comparison mutants survive.** `T:1052` tests variant casing, while `T:846` changes both provider and model casing. Exact advertisement matching at `M:220` therefore masks membership errors. Changing any/all comparisons at `M:82` to OrdinalIgnoreCase survives these cases. Add advertised `gw:fast` with provider `GW`, bare `gw` with provider `GW`, and `prov/m1` with provider `Prov`; assert rejection and empty filtered results. Include dotless-i and embedded-NUL provider variants to test culture-sensitive mutants independently of advertisement equality.
- **P3 — Stale contract comment.** `M:21` still says membership requires `P/`, contradicting `M:82`. A maintainer following it could incorrectly restore slash-only validation; update it to the three-form rule.

No open P0, P1, or P2 findings. Model id: `KHONG_do_duoc`.

KET_LUAN: approve

## VERDICT lượt 2 (nguyên văn, sha256 `6e691be6…ffac`)
Review call 2/2, packet #1446 r3: reviewed SHA `981f7616efcdd85ff56b9815821b674fce79b8d5`, tree `bd3633bed62a02f43ccadce6611844dde4bb4a11`; base `b9ade4e2f3d489fe7e65c4ea928086fe627ec0c4`; delta from `94c425d3e2f7740ac573335175e80d6a01f5ad10`.

Read-only, offline source review. PowerShell/Windows tests and mutants were not run; RED/credit conclusions below are source-derived. Provider: OpenAI; execution surface: Codex; transport: API. Exact model id: `KHONG_do_duoc`.

Repository-relative abbreviations: `M` = `.agents/skills/proxima-control/scripts/ProximaControl.psm1`; `T` = `.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1`.

| Check | Result and evidence |
|---|---|
| P3-1: equality mutant | FIXED. `T:1048` advertises exact lowercase ids; `T:1053` supplies `GW/gw` and `AUTO/auto`. OrdinalIgnoreCase on equality at `M:83` accepts these, producing `MODEL_ID_FORM_LOOSE[provider case bare]` and `[provider case auto]` at `T:1055`. `models GW` additionally returns `gw`, failing `T:1064`. |
| P3-1: colon mutant | FIXED. `GW/gw:fast` at `T:1053` passes the mutated colon branch and unchanged advertisement equality (`M:221`), producing `MODEL_ID_FORM_LOOSE[provider case variant]` (`T:1055`). `models GW` returns `gw:fast`, producing `MODELS_FILTER_CASE_LOOSE` (`T:1063–1064`). |
| P3-1: slash mutant | FIXED. `Prov/prov/m1` at `T:1053` passes an OrdinalIgnoreCase slash branch, producing `MODEL_ID_FORM_LOOSE[provider case slash]` (`T:1055`). The empty `models GW` check alone does not catch this branch, but the use assertion does. |
| P3-1: culture mutants | FIXED for the requested CurrentCultureIgnoreCase mutations on equality, colon, or slash: the corresponding pairs above also compare equal under en-US and tr-TR. None involves Turkish I. Each branch individually, or any combination, turns X5-10 RED. Survivors among the specified mutants: none. `T:1056–1057` additionally checks ask rejection/no POST. |
| P3-2: stale comment | FIXED at `M:21–22`: equality, `P:`, legacy `P/`, Ordinal, verbatim advertisement, and separator restrictions replace the slash-only description. |
| CX13 anchor/replacement | PASS. `T:1141` replaces `$Id.StartsWith($Provider + ':', [StringComparison]::Ordinal)` with the same expression using `OrdinalIgnoreCase`. Literal source counting confirms exactly one anchor, at `M:83`; uniqueness enforcement is `T:1179–1180`. |
| CX13 credit | Would be credited on a clean child run with rc 1. Both exact named tokens at `T:1141` arise at `T:1055` and `T:1064`. Assertions accumulate rather than abort (`T:261`, `T:283`). `Get-Kill` splits once on colon and uses literal Contains, so brackets are safe (`T:1146`). Credit requires every named token, rc 1, matching source/culture, and clean retained evidence (`T:1155–1168`). |
| Shared anchor/isolation | SAFE. CX12/CX13 (`T:1140–1141`) each receive a fresh copy from `$ModDir` in a separate directory before mutation (`T:1171–1183`); mutations do not accumulate. |
| Scope/regressions | PASS. Delta touches only X5-10, CX table, test header comments (`T:6`, `T:18`), and module header comments. No executable module changes. Fixture state resets before subsequent cases (`T:223–229`, `T:279`). Both changed paths are leased at `ops/leases/px-ask-r3-g1-claude.yaml:26–27`; all seven full-change paths are within its write_set (`:23–32`). |

Findings: both prior P3 findings are closed; no new P0–P3 findings. For unchanged portions of `b9ade4e..981f761`, I rely on call 1 (`VERDICT-luot1.md`), supplemented by this delta and predicate/call-site review. The full change has no open P0/P1/P2. This is code-review approval, not Windows acceptance-test attestation.

KET_LUAN: approve
