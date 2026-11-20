# WP1319 r11 — Review độc lập cuối cho packet #1319

**Căn cứ:** đặc tả `ops/specs/wp1319-r11.md`, lease `ops/leases/wp1319-r11-g1-operator.yaml`. Ngân sách: tối đa 2 lời gọi Codex, do chủ kho cấp ngày 20/11.

## Lượt 1/2
| Mục | Giá trị |
|---|---|
| Reviewer | Codex CLI, `-m gpt-6-astra`, qua `.claude/dev/launcher.py run` (run `c0939197`) |
| Đối tượng | master `c3ab4aa5bfd9f1f5494e2efab1718fc2095f908c` (sau PR #1438), bản clone chỉ đọc |
| `run.json` | `trang_thai xong`, `ma_thoat 0`, `head c3ab4aa5…`, prompt sha256 `20bee765…`, 197,4 s, `model_phuc_vu_trang_thai DO_DUOC`, 14/14 response là `gpt-6-astra` |
| stdout | 5 451 byte, sha256 `228892711edfbb07baf721428851f4212aafb1e0a5ab71e505666f2567e8671a` |
| Kết luận | `KET_LUAN: request_changes`: 2 P2, 3 P3, không có P0/P1 |

Reviewer cũng tự tính lại 13 băm đã chép trong r5–r8 và báo **13/13 khớp**.

### Xử lý từng finding
| Finding | Đối chiếu | Xử lý |
|---|---|---|
| **P2:** MATRIX §11 #12 ghi "r1–r5 và mọi WP: **passed**", gộp việc có review với kết quả review | Đúng: NSIS là `request_changes`; review U8 chỉ phủ tập con; r5–r10 chỉ có connector | Viết lại hàng #12: liệt kê verdict và phạm vi từng lượt; ghi rõ "có review" chưa phải "đạt" |
| **P2:** lease `wp1319-r10-g1-operator` còn hạn (tới 05:26:54Z) lúc review | Đúng trên master `c3ab4aa` | Đã thu hồi trong r11 (commit `07ff150`; tệp lease r10 nằm trong write set của r11) |
| **P3:** r9 sửa lease r8 ngoài write set | Đã khắc phục ở `53801a7` (PR #1437), đúng như reviewer ghi | Không cần sửa thêm |
| **P3:** chỉ mục đóng WP thiếu #1416 | Đúng, và sâu hơn: #1416 đóng 19/11 09:11Z mà **không có** biên bản M8 nào | Đăng M8 bổ sung lên #1416 (`issuecomment-7029053418`), đọc lại khớp byte (sha256 `ed855045…`), `kiem-dong-wp` đạt. Thêm vào mục việc còn mở số 5 |
| **P3:** câu về nguyên nhân firewall (M:260, M:301) dứt khoát hơn nguồn | Đúng: r9 dựa vào lời khai của chủ kho; network và tag của instance chưa đo | Thêm điều kiện ấy vào §11 #2 và mục việc còn mở số 3 |

<details><summary>Nguyên văn stdout lượt 1 (sha256 228892711edfbb07…)</summary>

```text
#1319 is not yet closable as “acceptance complete with recorded owner waivers”: two P2 items remain below.

Reviewed SHA: `c3ab4aa5bfd9f1f5494e2efab1718fc2095f908c`; tree: `d93f190ec460f836c92590aaa33c0f444be4bea1`. Read-only checkout; no network or git writes. Model: `KHONG_do_duoc`; provider OpenAI, Codex tool session, local shell/file transport.

References: `M` = `ops/acceptance/wp1319/MATRIX.md`; `R<n>` = `ops/acceptance/wp1319/r<n>/RESULTS.md`. Other paths are repository-relative. “Matches” includes the stated limitations, not unrestricted product acceptance.

| Check / matrix row | Source checked; assessment |
|---|---|
| I.1 #1, M:259 | M:138; matches Desktop scope. |
| #2, M:260 | M:36, M:107, R9:94, R10:26; partial/waiver matches; attribution caveat below. |
| #3, M:261 | M:137, R10:27; fake backend and gateway waiver match. |
| #4, M:262 | M:141; `ops/acceptance/wp-u8/VERDICT.md:38`; scan limitation retained. |
| #5, M:263 | M:140, R10:29; scoped pins and accepted F1 match. |
| #6, M:264 | M:175; unintegrated guard limitation retained. |
| #7, M:265 | M:156, M:176; fixture busy-stop/operator-only locking retained. |
| #8, M:266 | M:238; positive LIVE promotion, negative test-only scope matches. |
| #9, M:267 | M:90, M:232, R10:30; data result/binary waiver match. |
| #10, M:268 | M:124, R7:11; primitive/fixture distinction retained. |
| #11, M:269 | M:92; 180-sample test-profile soak matches. |
| #12, M:270 | Review coverage overstatement; P2 below. |
| I.2 U1, M:275 | M:139, R10:28; matches. |
| U2, M:276 | R5:16; f728 only, offline 810 unresolved. |
| U3, M:277 | M:137; matches, referring to #3 limitations. |
| U4, M:278 | M:155, R10:31; integrity-rejection branch only. |
| U5, M:279 | M:184, R7:9; digest policy, NotSigned retained. |
| U6, M:280 | M:57; owner license declaration, not legal verification. |
| U7, M:281 | M:94, R10:32; partial/waiver matches. |
| U8, M:282 | M:232, M:233, R10:33; narrow data result and owner observation retained. |
| U9, M:283 | R5:17, R5:49, R6:18; capacities/cache locations match. |
| U10, M:284 | M:113, M:140; scoped pin results match. |
| U11, M:285 | R9:108, R9:115; waiver, testimony and absent auth proof retained. |
| U12, M:286 | M:96, R7:9; partial provenance/accepted risk matches. |
| I.3 daily release, M:291 | M:69, R5:18, R10:34; matches. |
| NSIS install, M:292 | M:190; matches Desktop scope. |
| Vendor uninstall, M:293 | M:191, M:247; measured failure retained. |
| Uninstall procedure, M:294 | M:246; scoped result matches, including missing immediate executable rehash. |
| Migration, M:295 | M:194, R10:35; unmeasured/waived. |
| LIVE, M:296 | M:239; two modules only. |
| Completeness | All 12 criteria at `ops/plans/PROXIMA-PLAYWRIGHT-v1.md:157` and U1–U12 at `docs/research/2026-11-05-proxima-playwright-p0.md:78` have rows. No missing cited section/file found. |
| Hash integrity | Python recomputation: 13/13 match. JSON CRLF-between-lines + terminal LF: R5:70/91/112, R6:107, R7:121/158, R8:53/78. Scripts LF including terminal LF: R6:60, R7:406/433, R8:171/208. Details: `hash-checks.json:1`. R9:15 explicitly supplies no host hash. |
| Leases/history | Compared revision commits with all ten r5–r10 lease write sets; spec/write-set hashes match. r5/r6 withdrawn, r7 expired, r8/r9 withdrawn; r10 exception below. |

Findings:

- **P2 — Review assurance overstated, M:270.** “r1–r5 and every WP: passed” on frozen packages conflates review occurrence with scope. NSIS review remains `request_changes` and checked a subset (`ops/acceptance/wp-nsis/VERDICT.md:42`, :44, :89); U8 lacks main drivers/manifests/full ZIP (`ops/acceptance/wp-u8/VERDICT.md:4`, :102). r5 specifies connector-only review (`ops/specs/wp1319-r5.md:45`), without a local frozen-package verdict. A closer could mistake this for complete raw review. Split coverage, actual verdict and limitations; do not imply failed measurements passed.
- **P2 — Active lease at review time.** At 2026-11-20 03:00:55Z, `ops/leases/wp1319-r10-g1-operator.yaml:31` grants through 05:26:54Z, without withdrawal. Closure would leave active write authority over the frozen record. Withdraw it or verify expiration before closure.
- **P3 — Historical scope violation, resolved.** Commit `3cc2ef2f` edited r8’s lease outside r9’s write set (`ops/leases/wp1319-r9-g1-operator.yaml:16`). `53801a7b` reverted it; `ops/specs/wp1319-r9.md:21` records the correction. r10 subsequently authorizes that withdrawal (:20 of its lease). r7’s r6 withdrawal likewise lies outside r7’s set, but within r6’s own set (`ops/leases/wp1319-r6-g2-operator.yaml:20`). No surviving unauthorized change identified.
- **P3 — Closure index omits #1416.** M:303/R7:17 list five children; R10:8 says six. H.12 records PXR execution/review, not its M8 pointer. Add the sixth closure reference; GitHub closure itself was not independently checked.
- **P3 — Attribution compression, M:260/M:301.** Firewall causality is stated categorically although R9:95–99 relies on owner testimony and unmeasured instance network/tags. Preserve those qualifications as M:285 does; this does not invalidate the recorded waiver.

No open P0/P1 identified. Owner decisions retain wording, scope and measured facts (R7:5, R9:102, R10:5); they do not establish auth, quota, legal verification or controller PASS. Closure requires the two P2 corrections and final M8 (M:304).

KET_LUAN: request_changes
```
</details>

## Lượt 2/2 (lời gọi cuối cùng được cấp)
| Mục | Giá trị |
|---|---|
| Reviewer | Codex CLI, `-m gpt-6-astra`, qua `.claude/dev/launcher.py run` (run `71689c97`) |
| Đối tượng | ứng viên `ff1cf890eb41a2de85975ca39c54fa7c11610dd4`, tức master `c3ab4aa5` cộng các commit r11 (đã sửa theo lượt 1), bản clone chỉ đọc |
| `run.json` | `trang_thai xong`, `ma_thoat 0`, `head ff1cf890…`, prompt sha256 `492293c1…`, 160,8 s, `model_phuc_vu_trang_thai DO_DUOC`, 15/15 response là `gpt-6-astra` |
| stdout | 5 022 byte, sha256 `33cdf463baf5115436af11155baf713294ad28da91c2e6171be016a1fcc27746` |
| Kết luận | **`KET_LUAN: approve`**: không có P0/P1/P2, 1 P3 |

Kết quả chính:
- 5 finding của lượt 1 đều được xác nhận đã xử lý.
- Mọi hàng mục I khớp nguồn; đủ 12 tiêu chí §11 và U1–U12.
- Băm 13/13 khớp.
- Write set của lease r5–r10 khớp với tệp đã sửa; không còn ghi ngoài phạm vi nào tồn tại.

### Xử lý finding lượt 2
| Finding | Đối chiếu | Xử lý |
|---|---|---|
| **P3:** M:270 ghi "r4-code … (sửa ở WP-PXA)", ghi nhầm chỗ sửa | Đúng: `r4/VERDICT-code.md:31` giao 18 mục cho Executor ở r4; `r4/VERDICT-run.md:6` xác nhận FIX1/FIX2 có mặt. WP-PXA sửa các finding sản phẩm/chốt kích hoạt (`wp-pxa/RESULTS.md`) | Sửa câu ở hàng §11 #12. Phạm vi nghiệm thu không đổi (reviewer cũng ghi vậy) |

Hết ngân sách review (2/2). Bản sửa P3 sau lượt 2 chỉ đổi đúng một câu chỉ chỗ sửa trong hàng §11 #12; không có lời gọi review nào sau bản sửa này ngoài connector trên PR.

<details><summary>Nguyên văn stdout lượt 2 (sha256 33cdf463baf51154…)</summary>

```text
#1319 can close as “acceptance complete with recorded owner waivers” after recording this review and final M8. No open P0/P1/P2; one P3 attribution correction remains.

Reviewed SHA: `ff1cf890eb41a2de85975ca39c54fa7c11610dd4`; tree: `49865de4c2398249a31b3200655131b3d583b10f`. Read-only checkout; no network or git writes. Model: `KHONG_do_duoc`; provider OpenAI, Codex tool session, local shell/file transport.

References: `M` = `ops/acceptance/wp1319/MATRIX.md`; `R<n>` = `ops/acceptance/wp1319/r<n>/RESULTS.md`; `L<n>g<g>` = `ops/leases/wp1319-r<n>-g<g>-operator.yaml`. Other paths are repository-relative. “Matches” means only the recorded scope.

| Review-1 finding | Candidate disposition and evidence |
|---|---|
| P2 review assurance | Resolved: M:270 separates verdicts, subsets and connector-only review. Minor attribution below. |
| P2 active r10 lease | Resolved: L10g1:38 records withdrawal; r11 authorizes it (`ops/specs/wp1319-r11.md:35`). |
| P3 r9 scope violation | Resolved historically: `53801a7b` reverses `3cc2ef2f`; `ops/specs/wp1319-r9.md:21`. Later withdrawal authorized by L10g1:20. |
| P3 missing #1416 | Resolved in repository: M:303 records supplemental M8 `7029053418`; `ops/acceptance/wp1319/r11/VERDICT.md:24` records digest `ed855045…`. GitHub unverified. |
| P3 firewall attribution | Resolved: M:260 and M:301 retain testimony and unmeasured network/tags, matching R9:95. |

| Section I row | Opened source; assessment |
|---|---|
| I.1 #1, M:259 | M:138; matches Desktop scope. |
| #2, M:260 | M:36, M:107, R9:94, R10:26; partial/waiver matches. |
| #3, M:261 | M:137, R10:27; fake backend/gateway waiver matches. |
| #4, M:262 | M:141; `ops/acceptance/wp-u8/VERDICT.md:38`; scan limits retained. |
| #5, M:263 | M:140, R10:29; scoped pins/F1 acceptance matches. |
| #6, M:264 | M:175; unintegrated guard limitation retained. |
| #7, M:265 | M:156, M:176; fixture stop/operator locking distinguished. |
| #8, M:266 | M:238; positive LIVE promotion; negative test-only. |
| #9, M:267 | M:90, M:232, R10:30; data/binary distinction matches. |
| #10, M:268 | M:124, R7:11; primitive/fixture distinction matches. |
| #11, M:269 | M:92; scoped 180-sample soak matches. |
| #12, M:270 | Verdicts/scopes match; remediation attribution P3 below. |
| I.2 U1, M:275 | M:139, R10:28; matches. |
| U2, M:276 | R5:16; f728 only; offline 810 unresolved. |
| U3, M:277 | M:137; inherits #3 limitations. |
| U4, M:278 | M:155, R10:31; integrity-rejection only. |
| U5, M:279 | M:184, R7:9; NotSigned and digest policy retained. |
| U6, M:280 | M:57; owner declaration, not legal verification. |
| U7, M:281 | M:94, R10:32; partial/waiver matches. |
| U8, M:282 | M:232, M:233, R10:33; narrow data result/owner observation. |
| U9, M:283 | R5:17, R5:49, R6:18; capacities/cache locations match. |
| U10, M:284 | M:113, M:140; scoped pin results match. |
| U11, M:285 | R9:108, R9:115; waiver, no auth proof. |
| U12, M:286 | M:96, R7:9; partial provenance/accepted risk. |
| I.3 daily release, M:291 | M:69, R5:18, R10:34; matches. |
| NSIS install, M:292 | M:190; Desktop scope matches. |
| Vendor uninstall, M:293 | M:191, M:247; failure retained. |
| Uninstall procedure, M:294 | M:246; scoped result, missing immediate executable rehash disclosed. |
| Migration, M:295 | M:194, R10:35; unmeasured/waived. |
| LIVE, M:296 | M:239; two modules only. |

All twelve plan criteria (`ops/plans/PROXIMA-PLAYWRIGHT-v1.md:157`) and U1–U12 (`docs/research/2026-11-05-proxima-playwright-p0.md:78`) have rows. No missing cited source or stronger status/scope found. Owner wording, scope and unchanged facts remain recorded (R7:5, R9:102, R10:5). No fixture, transcript, observation or status call becomes auth, quota, legal verification or controller PASS.

Hash recomputation: **13/13 match**. JSON blocks use CRLF between lines plus terminal LF: R5:70/91/112, R6:107, R7:121/158, R8:53/78. Scripts use LF including terminal LF: R6:60, R7:406/433, R8:171/208. Results: `hash-checks.json:1`. R9:15 explicitly has no host hash.

Compared revision commit file lists with all ten lease write sets; spec/write-set hashes match. r5 withdrawals: L5g1:39, L5g2:36, L5g3:35, L5g4:35; r6: L6g1:37, L6g2:37; r7 expired: L7g1:34; r8–r10 withdrawn: L8g1:38, L9g1:36, L10g1:38. r7’s r6 withdrawal lies outside r7’s set but within r6’s own set (L6g2:20). Only historical unauthorized write identified is the reverted r9→r8 edit above; none survives.

Finding: **P3 — Incorrect remediation attribution, M:270.** “r4-code … fixed in WP-PXA” can send an auditor to the wrong repair evidence. The 18 harness findings were repaired within r4 (`ops/acceptance/wp1319/r4/VERDICT-code.md:31`; `r4/VERDICT-run.md:6` under the same directory). WP-PXA addresses the separate product/guard findings (`ops/acceptance/wp-pxa/RESULTS.md:26`). Correct that attribution; acceptance scope is unaffected.

Final M8 remains procedural work (M:304); repository acceptance has no blocking finding.

KET_LUAN: approve
```
</details>
