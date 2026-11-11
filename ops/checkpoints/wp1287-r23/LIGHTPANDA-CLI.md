# Lightpanda CLI acceptance feasibility follow-up

Owner directs continued VM experiments toward acceptance, without WSL2. Read-only Windows VM OS probe confirms Windows Server kernel10.0.20348; the official Lightpanda binary remains Linux ELF, with no official Windows executable. Running inside a Windows VM does not change that ABI. Linux cloud execution works without WSL2. No WSL/system installation, new browser launch on Windows, model call or product source mutation.

## Actual measured flow

Lightpanda1.1.0-nightly.11975+bfa07e3e4, verified asset729819668 SHA256409897defad03f4dd4ddf28860c42a3605bd6fdbd444a348e91927dfd758b8dc. Existing @playwright/cli0.1.23/playwright1.65.0-alpha-2026-10-30 used unchanged. Dedicated loopback Lightpanda CDP server, private config browser.cdpEndpoint, no user cookies/profile or model agent mode; telemetry disabled. This is a distinct connection configuration, not CFT launch configuration.

Sixteen sequential CLI checks passed:

1. Open session A on controlled redirect302→200 fixture.
2. tab-list proves final URL.
3. requests --static supplies actual200 response index.
4. response-body writes byte-identical original HTTP HTML.
5. screenshot writes valid PNG1280x55.
6. pdf writes parseable PDF containing JS-updated ASYNC_CLI_OK.
7. Open session B on about:blank.
8. B has no A fixture tab.
9. A still has its original tab.
10. Close B.
11. Delete B data; deleted=false is a valid boolean result for this transient setup.
12. B tab-list returns rc1 and exact not-open error naming B.
13. A still works after B closes.
14. Close A.
15. Delete A data.
16. A tab-list returns rc1 and exact not-open error naming A.

Four additional finally close/delete commands are auxiliary cleanup, not four extra acceptance checks. Separate raw validation confirms close.status=closed, matching session, delete boolean, and exact expected not-open payload for each session; stderr empty. Owned Lightpanda server terminated/reaped. Tab separation and independent close are measured; cookie/storage isolation not measured. HTML raw bytes preserved separately from DOM/Markdown. PNG/PDF are text-only and do not prove CSS visual fidelity.

Private reproducible operator /workspace/mission1238-policy-fix/lightpanda/cli-acceptance.py and raw artifacts cli-acceptance/. ZIP cli-evidence.zip18981bytes, SHA256705a869998d48b90fc6401dce48b97777fc39bbaa8d0b3a0f4a1b1f74f9b35d9, archive entries verified against per-file manifest. This file is a source-only projection; raw operational data remains private.

## Integration direction and gates

Content engine: Lightpanda on Linux VM, official Playwright CLI via owned CDP endpoint, raw-body provenance, DOM/text extraction, text-only export explicitly labeled. This works locally without WSL2. A native Windows Node/CLI client may connect to a Linux Lightpanda service over CDP, but that cross-host deployment has not been tested and requires a restricted authenticated transport; no public unauthenticated CDP exposure is introduced here. There is no configured private route between current cloud and Windows VM.

Visual engine: keep full Chromium for CSS/layout screenshots and browser-native visual PDF. Lightpanda text output is not a replacement for those postconditions. Windows full-CFT U10 remains failed/not measured as recorded in CHECKPOINT.md. Exact H4/source tree unchanged, all review caps preserved. No product approval, scope waiver, issue closure or downstream dependency release is inferred.

Next implementation boundary is a separate optional Linux/CDP content-engine contract: pin binary digest/revision, explicit owned server lifecycle, fail-closed connection errors, raw-vs-derived artifacts, session data isolation and real-site compatibility tests. Existing P2 acceptance cannot be rewritten retroactively to call its native Windows failure a pass.
