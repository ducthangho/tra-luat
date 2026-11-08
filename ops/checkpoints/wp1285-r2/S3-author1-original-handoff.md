I wrote the three new files and touched nothing else, but none of the tests have been run. I had no shell in this session, so every behaviour below is designed and reviewed by reading only.

## Handoff — Packet #1285 / P1-S3, r1 / g1 (first author attempt)

**What I read first:** the spec at `/workspace/scratch/wp1285-spec-publish/ops/specs/wp1285-r1.md` (I did not check its sha256 myself), `AGENTS.md`, `CLAUDE.md`, the S2 module `ProximaControl.psm1`, the wrapper `Run-Px.ps1`, the S2 test harness, the S1 file header, `config.example.json`, the `.agents` release exclusion in `tl_core/release.py`, and the doctrine-scan rules.

**Size:** 447 lines added (SKILL.md 64, manifest 13, harness 370), measured by counting lines in the new files rather than with `git diff`. That is under the 450 cap. To get there I shortened prose and merged short statements onto one line; a few lines are now about 170–200 characters, similar to the existing S2 harness. Nothing is minified.

### Files
1. **`.agents/skills/proxima-control/scripts/ProximaControl.psd1`** — a data-only manifest with exactly the nine allowed keys: `RootModule` (the sibling `.psm1`), `ModuleVersion` 2.0.0, the GUID from the spec, PowerShell 5.1, Desktop and Core editions, the two exported functions, and three empty export arrays. There are no nested modules, required modules or pre-run scripts, so S1 still loads only through the existing S2 hash-before-import check. It has two comment lines and is plain ASCII.

2. **`.agents/skills/proxima-control/SKILL.md`** — Vietnamese, with frontmatter `name`, `description` and `version: 2.0.0`. It has six headings tagged (Scope), (Entry points), (Target), (WhatIf), (Versions) and (Limits). It covers:
   - that the add-on is optional, published in the repository only, and kept out of the core Package by `_RELEASE_EXCLUDE_DIRS`;
   - loading via the manifest or via the wrapper, with `<RepoRoot>` placeholders;
   - that state lives only in the current process, the wrapper reuses an already-loaded module only from its own path or stops with `ModuleConflict`, and reloading with `-Force` loses state;
   - that every action except `help` needs ConfigPath, RepositoryRoot and TargetId, and a credential is accepted only for `connect`;
   - no guessing, fallback or retry examples, and that WhatIf/Confirm always apply while `-Force` never overrides WhatIf;
   - the three version domains, with the gateway's FileVersion marked NOT_MEASURED and left to P4;
   - known limits (snapshot, hash-then-import and listener races; WinRM not measured), that AI/web output is untrusted, and links to the root SKILL and the protocol instead of copying them.

3. **`.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1`** — a self-contained harness (no Pester, ASCII only). Parameters: `-AddonRoot`, `-ScratchRoot`, `-ReportPath`, `-Counterexamples`.
   - **Checks before any import:**
     - **PM01:** parse the manifest and require exactly one hashtable of literal values, with no `#requires`, blocks, using statements or traps, read with the parser's safe-value method.
     - **PM02:** exact key list (case-sensitive), exact values, and wildcard exports rejected explicitly.
   - **Runtime checks:** these run only if PM01 and PM02 pass, and only in fresh child processes. The parent never loads a Proxima module and refuses to start if one is already loaded.
     - One child covers **PM03** (Test-ModuleManifest, real import, exactly two exports, `px help` works, actual module path recorded) and **PM06** (the unchanged `Run-Px.ps1 help` in the same process must reuse the same module instance with a test-owned in-memory marker intact; a `ModuleConflict` that leaves both untouched is also accepted).
     - A second child covers **PM04**: a private copy whose `ProximaConfig.psm1` gets one harmless sentinel line must be rejected with `DependencyMismatch` before that line runs, and the original S1 file must be unchanged.
   - **PM05** checks the doc structure and that versions match in both directions: frontmatter and Versions section against the manifest, no stray x.y.z versions other than 2.0.0 and 1.0.1, the three version domains, and consistent placeholders. A deleted or blank SKILL fails.
   - **PM07** runs last. It checks the isolation statement, a small deny-list of forbidden content, that every example line parses and has valid arguments, that file references resolve, and that every add-on file (including all S1/S2 files) is byte-identical before and after the whole run.
   - **On baseline B:** all seven IDs still run and fail with MANIFEST_ABSENT/SKILL_ABSENT, exit code 1. A setup or unavailable runtime gives exit code 2 and is never counted as a property result.
   - **Counterexamples:** CX00 (unchanged copy must pass 7/7 with exit 0), CX01 pre-run script and CX03 nested module (both must fail PM02 with zero runtime children and PM04 reported not executed), CX02 wildcard export (PM02), CX04 wrong documented version (PM05). Credit is given only for a child exit code of 1 with the named reason in the named case.
   - **Evidence:** everything goes under `<ScratchRoot>\pm-<run>` — child scripts, arguments, command lines, raw stdout/stderr bytes, outputs, private copies, mutated sources and records. Nothing is deleted, and every file, including nested counterexample evidence, is re-hashed at the end. Child processes inherit the caller's execution policy; the harness never sets one.

### Not run
Nothing was executed: no PowerShell 5.1 or 7 run, the S2 26-case suite was not re-run, and none of the Linux gates (selftest, Ruff delta, manifest verify, diff check, doctrine-scan, adr-song) were run. There is no candidate commit H yet.

### Uncertainties
- On PS5.1 the module path after a manifest import has not been measured. PM06 accepts either reuse or a fail-closed `ModuleConflict`, and PM03 only records the path.
- Not confirmed on PS5.1: the safe-value parsing returning an empty array for `@()`, and the PS5 parser API PM01 relies on.
- PM04 assumes a module whose load throws is not left loaded.
- Treating an execution-policy denial as a setup error rests on matching the text `UnauthorizedAccess|PSSecurityException`.
- On a timeout, PS5.1 kills only the direct child, not its child processes.
- The PM07 deny-list is narrow: it cannot catch every forbidden claim, so the main protection is the required-structure checks.
- I added `version:` to the SKILL frontmatter (the spec asks for it), but other tooling may not expect that key, and the doctrine-scan overlap check was not run.

```json
{"packet":"wp1285","revision":1,"generation":1,"provider":"anthropic","surface":"claude_code_cloud","model":"claude-opus-5-5","session":"unknown","baseline":"bf9914cb1a8e6f5047468f4d130b587015f8d73f","status":"done","changed_paths":[".agents/skills/proxima-control/scripts/ProximaControl.psd1",".agents/skills/proxima-control/SKILL.md",".agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1"],"summary":"Three new files only. 9-key data manifest (RootModule psm1, 2.0.0, fixed GUID, PS 5.1 Desktop/Core, exports px + Invoke-ProximaOperation). Vietnamese SKILL.md with Scope/Entry points/Target/WhatIf/Versions/Limits, three version domains, optional repo-only publication. Self-contained harness PM01..PM07 (static AST/schema gate before any import; fresh-child real import + px help + same-process Run-Px reuse; tampered-S1 private copy rejected with DependencyMismatch before sentinel; doc structure/version checks; isolation, example and file-ref checks; add-on bytes unchanged) plus CX00..CX04 counterexamples on copies; all evidence retained and re-hashed. Additions 447 (new-file line count, not git diff).","tests":"NOT_RUN","tests_reason":"Author session had only Read/Glob/Grep/Edit/Write scoped to the three paths; no shell, PowerShell or git. No native PS5.1/7, Linux gate or S2 normal26 run.","remaining_work":["Root creates mechanical commit H and records H, tree and B..H diff (exactly 3 new files, additions <=450, S1/S2 bytes unchanged)","Native PS5.1 and PS7 on the selected device: harness vs B (expect 7 failed, rc 1) and vs H (expect 7/7, rc 0), with -Counterexamples on H (CX00 pass, CX01..CX04 credited); S2 normal26 coexistence re-run","Linux gates at H: tl selftest N/N, Ruff F delta 0 vs B, temporary manifest strict verify, git diff --check, doctrine-scan, adr-song, documentation/release claim checks","Independent Codex review of B..H"],"requested_next_role":"operator","code_scope_uncertainties":["PS5.1 ModuleInfo.Path after manifest import not measured; PM06 accepts reuse or fail-closed ModuleConflict","Not confirmed on PS5.1: SafeGetValue returning an empty array for @() and the PS5 parser API used by PM01","PM04 assumes a module whose load throws is not left loaded","Execution-policy denial classified as setup error by text match UnauthorizedAccess|PSSecurityException","Timeout kill on PS5.1 does not kill the child's own children","PM07 deny-list is limited; required-structure checks are the main protection","SKILL frontmatter version key may not be expected by other tooling; doctrine-scan n-gram check not run","Line counts measured by counting file lines, not git diff numstat; some lines are 170-200 characters"]}
```