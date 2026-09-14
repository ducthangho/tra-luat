verdict: approve
reviewed_sha: e3b997b60976acdb99ced3f87494dd351887d15d
tree: 1a6b352c0a269a9973099d5e6fbf93414489a253
base (packet): bb7013c7669da19304a8769e5b25f8c1f8951e9c
review: R26 (issue 463, revision25/generation6)
review_axes: [spec, standards_security]
assurance: cross_approved (Claude reviewing Codex executor)
model_reviewer_identity: anthropic_claude / claude-opus-4-8 / max / claude_code / machine-local
note: EXACT-SHA REVIEW — grants NO merge/land authority (per instruction). Static quality review, benign strings only; no YAML/installer/CI/network/Git-write executed.

## HEADER RATIONALE
All three review classes (installer/domain, lexer/structure, consumer/workflow) APPROVE on both the
spec and standards/security axes. The r25/gen6 change (the `<<-` heredoc tab-strip + PowerShell LF
normalization) is correct, minimal, and covered by exact killing fixtures. No product-correctness
defect was found across 8 hunt directions. One non-blocking **P3 traceability** finding (F-R26-A8) is
recorded: the in-repo spec text (≤300) lags the owner-authorized additions budget (≤1000) under which
this packet operates; the packet cannot fix it (A8 forbids a 3rd path). See caveat in F-R26-A8.

## STATUS
- [x] Ground truth (SHA/tree/clean) verified
- [x] Spec + protocol §8/§13 read
- [x] Executor evidence reproduced/checked (registry 684/684, revert mutant, Ruff, actionlint, A8 967/1000 two paths)
- [x] Class 1 — installer/domain (spec + standards)  → approve
- [x] Class 2 — lexer/structure (spec + standards) incl. `<<-` tab-strip-before-continuation → approve
- [x] Class 3 — consumer/workflow (spec + standards) → approve
- [x] Hunt 8 new directions (≥2/class)
- [x] Finalized header

## GROUND TRUTH (verified, read-only)
- HEAD = e3b997b6…d15d ✓ ; tree = 1a6b352c… ✓ ; root commit 394e9346… ✓ ; `git status --porcelain` empty (clean) ✓
- Full packet (bb7013c7..HEAD) numstat: `.claude/dev/ci_dang_ky_test.py` +841/−92 · `.github/workflows/ci.yml` +126/−6 ⇒ **967 additions, exactly 2 paths** (= lease write_set). Matches executor "A8 967/1000 two paths".
- r25/gen6 incremental (ff146f16..HEAD): only `ci_dang_ky_test.py` +38/−4 = the two r25 code paths: heredoc `<<-` tab-strip (727629e5 + e3b997b6) and PowerShell LF-only split (79b75cdb) + their fixtures.

## SPEC PROVENANCE (measured) — basis of F-R26-A8
- In-repo spec `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md` at HEAD **and** at origin/master = sha256 `49844d77…`, **revision 12**, A8 additions **≤ 300** (ADR-0044; lines 91-92, 108-109, 477-478). Packet does NOT touch the spec.
- SPEC-r24.md snapshot (review root) = sha256 `79ba77c3…`, **revision 24**, A8 §616-624 additions **≤ 1000** ("only effective ceiling", owner scoped exception citing issue #463 comments 5652199891 / 5657673695). Matches lease-r24 `spec_sha256`. **This revision was never committed to the repo (absent from master and HEAD).**
- SPEC-r25.md (named in the prompt) is **not provided**. Governing acceptance spec taken as the lease-pinned revision-24 (≤1000) — the budget under which the lease (`max_additions:1000`), the prompt ("A8 967/1000"), and prior reviews R18–R23 all operate.
- ⇒ A8 = **967 ≤ 1000** under the owner-authorized exception → SATISFIED for this review. The in-repo spec text (≤300) is stale by 3.2×; see F-R26-A8.

## ĐỐI CHIẾU LƯỢT TRƯỚC (reconcile prior findings — self-measured on HEAD)
Last complete verdict = R20 (approve w/ findings); R21 timed out, R22/R23 partial-invalid but carried the
same lexer finding lineage. Executor's r25/gen6 work directly answers them.

- **F-20A / F-22A [P2] — heredoc body scanned by physical line; `<<-` tabs not stripped before the
  logical/`$(`-scan ⇒ false-green `$(pip install ruff)`** → **ĐÃ VÁ THẬT (really fixed).**
  Evidence: e3b997b6 replaces `logical = carry + line` with `scan_line = line.lstrip("\t") if tabs else line; logical = carry + scan_line` (`ci_dang_ky_test.py:297-298`). Revert-mutant (scratch/rv26/revert_mutant.py): HEAD `_dong_logic(witness)` RAISES "heredoc có command substitution ngoài miền"; reverted → NO RAISE (leak). Counter-example suite 684→**683** (exactly the fixture `heredoc-dash-tab-continuation-substitution`, want=1, flips).
- **R22 class-3 — fixture set completely missing the `<<-` branch (0 occurrences)** → **ĐÃ VÁ THẬT.**
  Evidence: 2 new `<<-` fixtures present & green — `heredoc-dash-tab-continuation-substitution` (want=1) and `heredoc-dash-space-no-strip` (want=0, `:1206-1207`); tabs=True branch now exercised.
- **F-20B [P3] — backtick / hanging-heredoc grid granularity** → **ĐÃ VÁ THẬT (addressed).**
  Evidence: `heredoc-backtick` (want=1), `heredoc-pending-at-eof` (want=1), `heredoc-unclosed` (want=1), `second-heredoc`, `heredoc-dynamic-delimiter` now in `_FX` (`:1199-1209`), all green in 684/684.
- No prior finding left CHƯA VÁ; no VÁ HỜ; no VÁ SINH LỖI MỚI observed (all 684 counter-examples green; the two new r25 paths each killed by exact fixtures — see BẢNG SĂN).

## BẢNG SĂN (8 hunt directions; commands + real output; all runnable in scratch/rv26)
```
HƯỚNG I1 (installer/domain): unknown installer families must NOT become bare KHONG
  giả thuyết : nếu pipx/poetry/conda/npm/-r ruff-install → "KHONG" thì consumer bỏ sót pin ⇒ sai
  lệnh       : hunt.py classify(...) trên 14 biến thể
  output     : pipx/poetry/conda/npm/`-r requirements.txt`/`./ruff`/`--user`/`pip download`
               → KHONG_PHAN_TICH_DUOC ; pip install ruff → KHONG_GHIM ; ==0.15.15 → GHIM
  kết luận   : KHÔNG PHẢI LỖI (lease viec_dau_tien giữ: ngoài miền ≠ KHONG)
HƯỚNG I2 (installer/domain): ruff-hiding / normalization
  giả thuyết : `ruff==0.15.15 requests`, RUFF, ruff[extra]==, hai req → có thể lách phân loại pin
  lệnh       : hunt.py classify(...)
  output     : `ruff==0.15.15 requests` → KHONG_PHAN_TICH_DUOC (len(reqs)!=1) ; RUFF==0.15.15 → GHIM
               ; ruff[extra]==0.15.15 → BAD:KHONG_PHAN_TICH_DUOC ; không ca nào rớt về bare KHONG
  kết luận   : KHÔNG PHẢI LỖI
HƯỚNG L1 (lexer): `<<-` tab stripped BEFORE logical continuation scan   [CORE của r25]
  giả thuyết : nếu tab không strip trước join, `$`+tab+`(` không thành `$(` ⇒ lọt substitution
  lệnh       : revert_mutant.py (revert e3b997b6, chạy _dong_logic + phan_chung)
  output     : HEAD 684/684 & witness RAISE ; MUTANT 683/684 & witness NO-RAISE (leak)
  kết luận   : KHÔNG PHẢI LỖI trên HEAD (fix có răng, đúng đúng-1 fixture)
HƯỚNG L2 (lexer): carry chaining nhiều dòng dưới `<<-`
  giả thuyết : `\tx $\` / `\t\` / `\t(echo data)` — nối 2 lần có thể lọt `$(echo data)`
  lệnh       : hunt.py lex("cat <<-END\n\tx $\\\n\t\\\n\t(echo data)\n\tEND\n")
  output     : REJECT(heredoc có command substitution…) — đúng như bash sẽ thực thi
  kết luận   : KHÔNG PHẢI LỖI
HƯỚNG L3 (lexer): parity backslash (lẻ/chẵn/3 dấu) và arithmetic
  giả thuyết : `x$\\\`+`(echo data)` hoặc `$((1+2))` có thể lọt hoặc chặn oan sai bash
  lệnh       : hunt.py lex(...) trên L-multi-bs-3, L-arith, L-even-backslash
  output     : `x$\\\`+`(` → ACCEPT (bash: `(` bị escape, KHÔNG substitution) ; `$((` → REJECT
               (chặn-oan arithmetic, fail-close, đúng docstring "không hỗ trợ arithmetic")
  kết luận   : KHÔNG PHẢI LỖI (parity khớp escaping của bash; chặn-oan có công bố)
HƯỚNG C1 (consumer): A7 — đọc MỌI job, không chỉ `gate`
  giả thuyết : nếu chỉ đọc jobs.gate, chuỗi hợp lệ ở job khác bị coi thiếu / unpinned lọt
  lệnh       : hunt.py loi_ruff_ci(wf([PIN,REG], job="lint-job")) và unpinned ở job "x"
  output     : valid-chain-nongate → [] (0 lỗi) ; unpinned-nongate → ["CI không chứng minh ghim…(job:['x'])"]
  kết luận   : KHÔNG PHẢI LỖI (A7 đúng: quét mọi job)
HƯỚNG C2 (consumer): install sau `if:` không được tính là bằng chứng pin
  giả thuyết : pin đặt sau step.if hoặc job.if có thể được nhận là GHIM đáng tin
  lệnh       : hunt.py loi_ruff_ci(wf([{if:…,**PIN},REG]))
  output     : ["CI không chứng minh ghim…; ngoài miền cú pháp: ['gate/bước 1']"] (buộc KHONG_PHAN_TICH_DUOC)
  kết luận   : KHÔNG PHẢI LỖI
HƯỚNG C3 (consumer): PowerShell tách theo LF, không theo splitlines   [đường r25 thứ hai]
  giả thuyết : nếu dùng splitlines(), `echo hi<CR>echo ok` / `<VT>` tách 2 dòng hợp lệ ⇒ lọt
  lệnh       : hunt.py _shell_trong_mien(...) + mutant_pwsh.py (revert split→splitlines)
  output     : HEAD: CRLF→False, VT(\x0b)→False, clean LF→True, `;`→False. MUTANT splitlines:
               684→678 (flip 6 fixture shell-carrier-alphabet-{pwsh,powershell}-1-{56,57,58})
  kết luận   : KHÔNG PHẢI LỖI trên HEAD (LF-only có răng, giết bởi 6 fixture)
```

## BẢNG ĐO (executor evidence — self-measured, không nhận lời khai)
| khẳng định (executor/prompt) | đo được | khớp? |
|---|---|---|
| exact head/tree/root/clean | e3b997b6 / 1a6b352c / 394e9346 / porcelain empty | ✓ |
| A8 = 967 additions, đúng 2 path | numstat 841+126=967; 2 path = write_set lease | ✓ (budget: xem F-R26-A8) |
| registry 684/684 | `PHẢN CHỨNG: 684/684 đỏ đúng`, `TỔNG: ĐẠT` (ĐĂNG KÝ 21/21, RUFF CI 3/3, LAUNCHER 4/4) | ✓ |
| revert mutant killed by exact fixture | revert e3b997b6 → 684→683; killer = `heredoc-dash-tab-continuation-substitution` | ✓ |
| actionlint pass | actionlint 1.7.7 on ci.yml → rc=0 | ✓ |
| Ruff pass | ruff 0.15.15: 63×E701 + 30×E702 (style-only, 0 F-code); no repo ruff config; CI probes `ruff --version`, never `ruff check` | ✓ substantively (see note) |

Note on "Ruff pass": bare `ruff check` under default config is red with 93 **stylistic** hits (deliberate
one-liner house style) — but the repo ships **no** ruff config and the workflow never runs `ruff check`
(only `pip install ruff==0.15.15` + `ruff --version` probe, which is exactly what `loi_ruff_ci` polices).
No substantive (F-code) lint defect exists in the changed file. (`git grep` also surfaced pre-existing
`Filename too long` errors under `ops/reviews/**/goi-y/cay/**` — untouched by the packet; environmental only.)

## FINDINGS

### F-R26-A8  [P3 · traceability/spec-hygiene · NON-BLOCKING]  in-repo spec budget lags owner-authorized budget
TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:477-478` (rev12, A8 ≤300) vs measured 967 additions.
VẤN ĐỀ: At the reviewed SHA (and on origin/master) the in-repo spec is **revision 12, A8 additions ≤ 300**.
  The packet is at **967** additions. The ≤1000 budget the packet operates under exists only OUT OF TREE:
  the SPEC-r24.md snapshot (rev24, §616-624 scoped exception) + lease-r24 (`max_additions:1000`, `spec_sha256=79ba77c3`)
  + owner issue-comments (5652199891 / 5657673695). A reviewer holding only the repo at this SHA would read
  A8 as red (967 ≫ 300). The authorization is real but un-landed, so the SHA is not self-describing on A8.
ĐÃ THỬ VÁ: không (không thể trong packet). A8 đòi ĐÚNG 2 path; sửa spec = path thứ 3 ⇒ tự vi phạm A8.
  Đây là việc CHỦ KHO land, không phải executor.
ĐÃ THỬ NGHIỆM: sha256 in-repo=`49844d77` (rev12, master==HEAD, untouched) vs SPEC-r24.md=`79ba77c3` (rev24);
  numstat 841+126=967; `git merge-base --is-ancestor bb7013c7 origin/master` = YES.
GỢI Ý (4 phần):
  • vá ở đâu: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md` (spec, ngoài write_set packet) — do CHỦ KHO/land-approver,
    KHÔNG do executor packet này (đúng theo §3.2 "agent không tự mở write set" + A8 hai-path).
  • vá thế nào (hướng, không patch — spec là tài liệu authority): land revision-24 (hoặc rev25) của spec vào
    master (nội dung A8 ≤1000 + khối ngoại lệ CÓ PHẠM VI trỏ issue #463) TRƯỚC/CÙNG lúc land packet, để text
    in-repo khớp ngân sách đã ủy quyền; hoặc, nếu ≤300 mới là ý định hiện hành, thì packet phải quay về ≤300
    (khi ấy 967 là P1 A8 — xem caveat).
  • ca test khoá nó: land-gate readback so `additions ≤ (A8 của spec in-repo tại land-SHA)`; nếu spec vẫn rev12
    thì gate phải ĐỎ — biến khe hợp-đồng-lệch-spec này thành cửa cứng thay vì lời khai out-of-tree.
  • có thể đẻ ra gì: nếu land mà không đồng bộ spec, mọi cross-review/audit tương lai tại SHA này đọc ≤300 và
    kết luận A8 vi phạm — đúng cái bẫy R26 suýt sa vào; và nó làm suy yếu "spec là nguồn acceptance duy nhất".
ĐỘ TIN: cao (đo trực tiếp: hai sha256 khác nhau, hai revision khác nhau, master==HEAD trên spec).
CAVEAT (quan trọng): verdict `approve` này DỰA TRÊN việc ngân sách ≤1000 là ủy quyền thật của chủ kho, được
  chứng thực ĐỘC LẬP bởi hai hiện vật (lease + SPEC-r24 snapshot, cả hai trỏ cùng issue-comment). Tôi KHÔNG
  gọi được issue để đọc nguyên văn (cấm mạng). NẾU ủy quyền ≤1000 không có/không hợp lệ thì F-R26-A8 leo lên
  **P1 (A8 vi phạm 967≫300 ⇒ changes_requested)**. Land-approver PHẢI readback ủy quyền này trước khi land.

### (Ghi chú, không phải finding) — hành vi bảo thủ đã xác nhận đúng-thiết-kế
- Arithmetic `$((…))` trong thân heredoc không-quote bị chặn (chứa chuỗi con `$(`). Fail-close, khớp docstring
  "không hỗ trợ arithmetic"; chặn-oan an toàn, không phải lỗi. (Nếu muốn nới: cần phân biệt `$((` với `$(` —
  chi phí không xứng trong miền CI hẹp này; khai thành nợ là hợp lệ.)
- `<<\END` (delimiter escape bằng backslash) bị từ chối "heredoc ngoài miền" (regex chỉ nhận quote `'`/`"`).
  Fail-close so với bash (bash coi là quoted). An toàn.

## KẾT LUẬN THEO LỚP (hai trục mỗi lớp)
| lớp | Spec | Standards/Security | verdict |
|---|---|---|---|
| 1. installer/domain | `_cai_truc_tiep` đóng họ installer trước grammar; ngoài miền ≠ KHONG (I1,I2) — đúng viec_dau_tien lease | không có false-accept; ruff-hiding/normalize kín | **approve** |
| 2. lexer/structure | `<<-` strip-trước-join (L1), carry chaining (L2), parity backslash & arithmetic (L3) đúng POSIX/fail-close | 0 false-accept; fix có răng (684→683), witness đúng | **approve** |
| 3. consumer/workflow | A7 đọc mọi job (C1), if→ngoài miền (C2), PowerShell LF-only (C3); actionlint rc=0 | LF-only chặn CR/VT injector (684→678 khi revert); teeth giữ | **approve** |

FINAL: **approve** — cả ba lớp approve trên cả hai trục; F-R26-A8 là P3 non-blocking (kèm caveat land-readback).
Exact-SHA review — KHÔNG cấp quyền merge/land. Bất kỳ commit mới nào làm verdict này hết hiệu lực.
