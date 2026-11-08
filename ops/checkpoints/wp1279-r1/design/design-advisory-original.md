I've read everything I needed. Two findings change the plan before any product lease: the size estimate breaks the size cap, and the wrapper can't do remote work if it runs as its own process. Both are covered in section 6. All files were read-only; nothing was run or measured.

# PROXIMA-P1-S2 design (read-only)

**Sources read:** HEAD `efebadf`, the S1 module `ProximaConfig.psm1` and `config.example.json`, the S1 test harness (header only), the legacy `.psm1`/`.ps1`/`.psd1`, plan §6/§11, P0 research §c/g/h/i, and ADR-0044/0053. I only listed the protocol §3/4/8/10/13 headings and did not read the sections; the AGENTS.md grep for Proxima/ShouldProcess returned nothing.

## 1. Contract

**Public surface.** The module exports exactly two functions: `px` and `Invoke-ProximaOperation`. Both use `[CmdletBinding(SupportsShouldProcess, ConfirmImpact='Medium')]`. No aliases and no variables are exported.

**`px` parameters**
- `-Action`, a `ValidateSet` of: help, config, status, models, use, ask, start, stop, restart, connect, disconnect.
- Required for every action except help: `-ConfigPath`, `-RepositoryRoot`, `-TargetId`. There are no defaults, no environment-variable lookup, no current-directory lookup and no saved settings.
- Optional: `-Provider`, `-Value`, `-Model`, `-Credential`, `-Force`.
- Removed from legacy: `-ConnectionUri` and `-ConfigurationName`. They now come only from the validated config.

**Flow for every `px` call**
1. Call `Read-ProximaConfig` (S1, read-only, allowed under WhatIf). An S1 error is re-thrown with its own `ProximaConfig.*` error ID.
2. Compare `[string]::Equals(cfg.targetId, TargetId, Ordinal)`. A mismatch throws `ProximaControl.TargetMismatch`. The message never echoes either value.
3. Compute the target fingerprint: SHA-256 over a length-prefixed, fixed-order encoding of every validated field. A missing remote field is encoded as a distinct marker, so a Local config can never collide with a Remote one, and a separator character inside a value cannot forge a match.
   - The full 64-hex fingerprint is the key for all state.
   - What gets displayed is `px:<first 12 hex> "<targetId>"`. Control characters, lone surrogates and bidi characters are shown as `\uXXXX`, and the display is capped at 64 characters. No new restriction is put on targetId itself.
4. Check the arguments. This step is pure: provider maps to chatgpt/claude/gemini/perplexity, and `-Value`/`-Model` must be present where needed.
5. Call `$PSCmdlet.ShouldProcess(<safe display>, <fixed action text>)`, for every action including status and models.
   - Under WhatIf it returns a result with `dryRun=$true` and `dispatched=$false`, and does nothing else: no credential prompt, no session, no HTTP, no service call, no process query, no file access beyond the config read.
   - `-Force` is used only to bypass the pending-request guard. It never appears in a ShouldProcess condition, and the module never calls `ShouldContinue`.
   - The WhatIf text never contains the prompt, credentials, API key or URI.
6. Dispatch:
   - **Local:** call the internal endpoint function in the same process.
   - **Remote:** look up `$script:Sessions[fingerprint]`. It must exist, have `State -ceq 'Opened'`, and have a stored fingerprint that matches. Otherwise throw `NotConnected`. The module never calls `Get-PSSession` and never auto-connects.
   - The remote call is `Invoke-Command -Session $s -ScriptBlock $script:EndpointBody -ArgumentList $op`. `$script:EndpointBody` is a constant defined in the module, not something the user supplies.
   - `$op` is a hashtable with an exact set of keys: Action, BasePath, Provider, Model, Prompt, Force, TargetFingerprint, ModuleSha256, ConfigModuleSha256, ProtocolVersion, and an explicit `WhatIf=$false`.

**`Invoke-ProximaOperation` (endpoint side)**
- Parameters: `-Action` (status, models, ask, start, stop, restart, handshake), `-BasePath`, `-Provider`, `-Model`, `-Prompt`, `-Force`, `-TargetFingerprint`.
- It does not need, and never looks for, the client's config file. Its trust comes from the explicit parameters plus the remoting session's own authorisation.
- `BasePath` is re-checked with S1's own path-syntax rule. That rule is private, so it is called through S1's module scope; S1 stays byte-identical, and the coupling is pinned by the dependency hash.
- It runs its own `ShouldProcess`, so calling it directly with `-WhatIf` has no side effects whatever the ambient `$WhatIfPreference` is.

**Results** use one schema (`px.result.v1`): action, targetFingerprint, targetDisplay, mode, dryRun, dispatched, outcome, plus action-specific fields:
- **status** (this is also the healthcheck): gateway, version, providers, `service='not_queried'`, `authentication='not_verified_by_status'`.
- **models:** a list of `{id, owner, availability='advertised_not_execution_tested'}`.
- **ask:** requestId, requestedModel, reportedModel, answer, recordState.
- **config:** the validated fields plus the fingerprint.

There is no separate healthcheck action.

**Errors** use `ProximaControl.<Code>` with a fixed message. Inner exception messages are never copied out. For remote errors, the client keeps a code only if it matches `^ProximaControl\.[A-Za-z]{1,40}$`; anything else becomes `RemoteFailed`.

**Wrapper `Run-Px.ps1`**
- `#requires -Version 5.1`, with `SupportsShouldProcess`. Parameters mirror `px`.
- It imports the module from its sibling path. If a `ProximaControl` loaded from a different path is already present, it fails closed rather than replacing it.
- It forwards only parameters that were actually bound, and always passes `-WhatIf:$WhatIfPreference` explicitly. That explicit pass is the real fix for the legacy bug: a module function does not inherit the calling script's preference variables.
- Connect is only ever the explicit `-Action connect`.

## 2. State (no new persistent contract)

- `$script:Selection` maps fingerprint → provider → exact model ID, using Ordinal comparison.
- `$script:Sessions` maps fingerprint → `{Session, Uri, ConfigurationName}`.
- Both are session-only and are lost on re-import or in a new process. This is declared, not hidden. Nothing is written to settings, config or profile, and the S1 schema is not extended.
- An `OnRemove` handler removes every session the module owns when it unloads.

## 3. connect / disconnect / use / ask

**connect** works only when `mode='Remote'`, and `-Credential` is required. With no credential it fails with `CredentialRequired`; the module never calls `Get-Credential`.
1. ShouldProcess.
2. `New-PSSession` with the config's URI and configuration name, `-Authentication Negotiate`, and a session option that sets the CA, CN and revocation checks explicitly to `$false`.
3. A handshake through the same endpoint body. It makes no HTTP call; it only checks hashes and the protocol version.
4. If any step after `New-PSSession` fails, a `finally` block removes the new session and the old one is left alone.
5. Only on success is the stored session swapped. The old session is removed afterwards; if that removal fails, the result says `previousSessionRemoval='failed'` instead of throwing.
6. Sessions for other fingerprints are never touched.

**disconnect** works only on the current fingerprint and goes through ShouldProcess.

A session made under an older config is unreachable once the config changes (the fingerprint no longer matches). It stays open until the module unloads; that is declared.

**use:** ShouldProcess, then exactly one GET `/v1/models` on the target, then an Ordinal check of the exact ID and provider prefix, then the selection is stored. Under WhatIf there is no query and nothing changes.

**ask:** the model comes from `-Model`, otherwise from the selection for this fingerprint. If neither exists it fails with `NoModelSelected`; there is no fallback.

## 4. Endpoint body (works on PS5.1)

1. `Set-StrictMode`, `$ErrorActionPreference='Stop'`, check the shape of `$op`.
2. Read `<BasePath>\control\ProximaControl.psm1` and `ProximaConfig.psm1` and hash them with .NET SHA-256 (not `Import-PowerShellDataFile`, which was unavailable on device 810). If either hash differs from the client's, fail with `EndpointIncompatible` before importing anything. Old legacy code is therefore rejected.
3. `Import-Module <exact path> -Force -PassThru`. Check that the loaded module's path and `ProtocolVersion` match, then call the export through that module object so an older module already loaded in the session cannot be picked up by name.

**Limitations**
- Hashing and then importing reads the file twice. This narrows the race window; it does not close it.
- The hash check only proves the endpoint code is compatible, and is not a security boundary. A hostile endpoint can lie about its hashes.
- Authentication is entirely WinRM Negotiate plus HTTPS certificate validation. Real authentication to the gateway (U11) stays unmeasured until P3.
- The psd1 manifest belongs to S3; S2 imports the psm1 directly.

## 5. Local operations (from legacy, tightened)

**Gateway lookup**
- Read `<base>\profile\rest-port.json` (read-only, size-capped, pid and port 1–65535 validated).
- The process must be named Proxima and run in session 0.
- Its path must equal `<base>\runtime\Proxima.exe`. A different path fails with `RuntimeMismatch`. An unreadable path (common for a session-0 process seen by a non-admin) is reported as `runtimeIdentity='unverified'` and not treated as verified.
- The URL is always `http://127.0.0.1:<port>`.

**HTTP**
- `HttpClientHandler` with no redirects and no proxy. Exactly one send per request, never retried. Timeouts: status 10 s, models 30 s, ask 300 s.
- Status sends no Authorization header (fixes the P0 finding). Models and ask keep the legacy behaviour of adding a Bearer header from the endpoint's `PROXIMA_API_KEY` environment variable. This is flagged for the owner (open question 4).
- A failed request reports only `HTTP <code>`. The gateway's error body is never echoed.

**ask:** one GET for models, an exact Ordinal check of the model ID (legacy `-notcontains` was case-insensitive), then exactly one POST with the model ID used verbatim.

**Request records:** `<base>\results\px-active\<guid>.json`
- Every folder from `<base>` down must be a real directory, not a reparse point (attribute `0x400`). Missing folders are created, then re-checked.
- The record is created with `CreateNew`, never overwritten, with state `pending`.
- If writing the record fails, no POST is sent.
- If finalising it after the POST fails, the answer is still returned with `recordState='finalize_failed'`, and the record stays pending, which errs toward blocking.
- This is not proof against an admin swapping folders at the same moment (ABA). That is declared.

**Pending guard (stop/restart):** a missing records folder counts as no pending requests. If the folder exists but cannot be read, or a record is malformed, pending or unknown, the action is blocked unless `-Force` is given. This fixes the legacy `SilentlyContinue` hole.

**UI guard (start/restart):** if a Proxima process exists in a non-zero session (the login UI is open), the action is refused.

**Service:** the name `ProximaGateway` is fixed. S2 cannot tell that this service is the gateway (CIM returned access denied on f728) or that `<base>` is the installed runtime (U2/U12). S2 performs no real service, process or gateway activation.

## 6. Test harness (`tests/ProximaControl.Tests.ps1`)

**Setup**
- Self-contained, no Pester, same pattern as S1: explicit `-ModulePath`, `-ScratchRoot`, `-ReportPath`, and `-Counterexamples`/`-EvidenceRoot`. Exit codes 0/1/2 mean the same as in S1.
- The config files and a fake base path live in scratch outside the repo. The fake base path holds a `control\` copy of the code, a `profile\rest-port.json` and `results\`.
- The mock gateway is an `HttpListener` on an ephemeral loopback port, owned by the harness, that counts requests and records headers.
- Service, process and session primitives go through a private module-level table of fully qualified commands. Only the harness child process replaces its entries, through module scope. There is no public parameter that accepts a script block.
- Remote transport is replaced by `Start-Job`, which runs the real `$script:EndpointBody` out of process with serialised arguments, with `$WhatIfPreference=$false` set in the child.
- The same test IDs run on `powershell.exe` 5.1 and `pwsh` 7.

**Baseline:** at `efebadf` the module is absent, so every test must fail with `API_ABSENT` (a real red run).

**Acceptance IDs and the mutation each one must catch**

| ID | Checks | Must catch |
|---|---|---|
| X1-01 | Exactly two exports, both `SupportsShouldProcess` | SupportsShouldProcess removed from `Invoke-ProximaOperation` |
| X1-02 | TargetId differing by case, NUL, NFC/NFD or trailing space → `TargetMismatch`, zero primitive calls | `-eq` used instead of Ordinal |
| X1-03 | A whitespace/control-character targetId is accepted and displayed escaped | Raw display |
| X2-01 | Every action × {WhatIf, WhatIf+Force, WhatIf+Confirm:$false} → zero journal entries, HTTP calls, sessions or tree changes | `if ($Force -or ShouldProcess)` |
| X2-02 | connect -WhatIf with no credential → no prompt, no session | `Get-Credential` called before ShouldProcess |
| X2-03 | `Run-Px.ps1 -WhatIf` → zero side effects | WhatIf not forwarded / legacy connect-first order |
| X2-04 | Endpoint called directly with `-WhatIf` in a subprocess with ambient `$false` → zero side effects | Endpoint body forces `WhatIf:$false` |
| X2-05 | Remote action under client WhatIf → zero transport calls | Dispatch before ShouldProcess |
| X2-06 | use -WhatIf → no GET, selection unchanged | Legacy use order |
| X2-07 | Sentinel prompt/password/key/error-body strings appear in no output stream | Gateway `error.message` echoed |
| X3-01 | Selection on target A is not visible to target B (differs only in basePath), and is lost after re-import | Selection keyed by targetId only |
| X4-01 | connect replacement: failed handshake keeps old session and removes new; success removes old | Old session removed before the new one is verified |
| X4-02 | Legacy endpoint bytes → `EndpointIncompatible`, nothing imported | Hash check skipped |
| X4-03 | Not connected → `NotConnected`, no lookup | Auto-connect / `Get-PSSession` |
| X5-01 | ask: exactly 1 POST with verbatim body; a mocked 500 leaves state `unknown` and 1 POST total | Retry loop |
| X5-02 | `GPT:x` is rejected when `gpt:x` is advertised | Case-insensitive model match |
| X5-03 | Pending, unknown, malformed or unreadable records block stop/restart | `SilentlyContinue` skip |
| X5-04 | Login UI process present blocks start/restart | UI check dropped |
| X5-05 | Junction inside `results` → `RecordPathUnsafe`, no POST | Reparse-point check skipped |
| X5-06 | status sends no Authorization header and no POST | Status goes through the shared Bearer helper |
| X6-01 | Approved positive control: exactly 1 GET for status and 1 GET + 1 POST for ask | Proves the zero counts elsewhere are not vacuous |

**Counterexamples:** 8 of these: X2-01, X2-03, X2-04, X3-01, X4-02, X5-01, X5-02, X5-03. For each, keep the child's source, rc, report, output and SHA-256. A counterexample counts as caught only when the named test fails for the named behaviour (journal count, POST count, wrong error code). A setup failure or wrong exit code earns no credit.

**Excluded:** Windows CI, the broad mutant runner, real WinRM, the real gateway and real credentials.

## 7. Size and open questions

**Estimate (not measured):** module 450–600 added lines, wrapper 40–60, harness 650–850 (the S1 harness alone is 643 lines). That is about **1,150–1,500 added lines across 3 files**.

This is over the 900-line planning figure. It is also over the size cap for a `sensitive` packet: 300 lines under ADR-0044, or 450 with an ADR-0053 declaration line. Even 900 would need an owner `nang_tran` (cap raise). I could not find S1's lease or cap evidence in this checkout.

**Smallest honest fix: choose one before the lease.**
- **(a)** The owner grants `nang_tran` for 3 files and about 1,500 lines.
- **(b)** Split the work:
  - **S2a:** Local mode, ShouldProcess, target checks, selection state, the local operations, and tests X1/X2-01..03/X2-06..07/X3/X5/X6.
  - **S2b:** remote connect, the endpoint body, the compatibility check, and tests X2-04/05 and X4. Only S2b closes U1.

**Other open questions**
1. **Wrapper vs. remote use.** A fresh `Run-Px.ps1` process can never be connected, because no auto-connect is allowed. The wrapper is therefore only useful for remote work when run in the same PowerShell session, after an explicit `-Action connect`. This needs to be stated as a documented limitation.
2. **S1 private helper.** Reusing S1's private path-syntax check through module scope couples S2 to S1 internals. The alternative is a small duplicate check, which risks the two drifting apart.
3. **Runtime path.** A runtime path that cannot be read is allowed but labelled unverified. Whether ask should refuse in that case is an owner decision.
4. **`PROXIMA_API_KEY`.** Keeping the endpoint's environment variable is a carry-over of an implicit credential. The alternative is to drop it, which may break the real gateway; unknown until measured.
5. **Not covered.** The hash-then-import race, ABA on request records, the service's identity, PS5.1 endpoint compatibility on real hosts (U1 only on isolated hosts), and authentication (U11) are not covered. Nothing here is a general security or concurrency guarantee.