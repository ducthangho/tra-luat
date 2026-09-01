# Ephemeral session credentials

Use `.claude/dev/session_credentials.py`; it reports only state and never a secret.

* `CODEX_HOME` is authoritative. If absent, every helper uses `~/.codex`. `codex-destination-check` validates it before the session hook invokes Codex at all; an already-readable login does not bypass the check. A refusal exports `TRA_LUAT_CODEX_BLOCKED=1`, which every launcher Codex path honors, including `launcher.py run -- codex …`, version, live-auth, prepare, and final doctor probes. Generic `run` recognizes the raw executable and its PATH-resolved basename, including absolute paths and Windows `.exe`/`.cmd`/`.bat`/`.com` shims, and reads the refusal both before its capability probe and immediately before final execution. Materialization is rejected before decoding or writing when the effective `auth.json` resolves inside the repository, including through a symlinked parent.
* Every secret write uses an **actual opened parent capability**. The helper walks and validates that opened ancestry, then performs create, mode change, sync, target inspection, replace, cleanup, and final verification relative to the same capability. It never falls back to a pathname after validation. This guarantee prevents a pathname alias swap from substituting a different directory. It does not claim to defeat a concurrent actor with permission to reparent the already-open directory object itself after validation: the capability remains bound to that same inode, so moving it under a repository moves the subsequent write there too. Environments that include that stronger attacker need OS namespace/permission confinement. POSIX supplies the required primitives. On Windows, where this runtime does not expose equivalent handle-relative primitives, the operation fails closed before child launch or write and reports `not_measured`.
* Capture a Claude Pro/Max subscription token with `python3 .claude/dev/session_credentials.py claude-capture --output /tmp/claude.token`. The output must resolve outside the repository. The helper checks that boundary before starting `claude setup-token`, suppresses its token-bearing output, and atomically writes mode `0600`. Provider children receive a minimal environment plus a process-created private HOME/XDG state directory; only the credential needed by that provider is added. Load the token as `CLAUDE_CODE_OAUTH_TOKEN` only for the Claude child.
* Set `GITHUB_PAT` in the session environment and run `python3 .claude/dev/session_credentials.py github-probe --repo ducthangho/tra-luat`. The PAT is mapped to `GH_TOKEN` only in the two `gh api` children (`user` and `repos/…`); it is absent from argv and reports.
* Keep `TL_MASTER_KEY` as the root for the existing encrypted Drive bundle. Run `python3 .claude/dev/session_credentials.py tl-bootstrap --env cowork --secrets-file /tmp/s.enc`; this rejects a direct or parent-linked repository bundle, invokes the repository's canonical `scripts/tl.py` with the repository root as its fixed working directory, and does not duplicate GAS/GWS/NLM storage or crypto. Before dispatch it canonicalizes and validates each directory candidate itself plus every ancestor for `HOME`, XDG, GWS, TL-cache, and temporary roots because the delegated child writes decrypted GAS/GWS/NLM state below them. An exact worktree root, bare-repository root, or link/junction alias is rejected before child start; permitted external roots may be nonexistent and are delegated in canonical form. `--secrets-file` is mandatory for both `tl-bootstrap` and the combined `bootstrap`; if absent, no provider or TL child is started.
* Codex device authorization always runs with a process-created private `CODEX_HOME`; `lay` has no caller-selected home. Successful auth is copied out only through the same guarded writer, and the private storage is destroyed when the process ends.
* NLM auth restoration accepts a closed relative schema only: `auth.json`, `profiles/default/cookies.json`, and `profiles/default/metadata.json`. Traversal, absolute paths, backslashes, extra profile paths, non-text payloads, and nested link/junction/reparse destinations are rejected before the first write.
* To perform all four steps in a single deterministic report, run `python3
  .claude/dev/session_credentials.py bootstrap --env cowork --secrets-file
  /tmp/s.enc --claude-token-file /tmp/claude.token`. This materializes
  `CODEX_AUTH_JSON` under the effective `CODEX_HOME`, passes the Claude token only
  to a minimal non-interactive Claude model probe (success requires a known marker
  in model stdout), normalizes and probes GitHub, and delegates the TL step.

Every top-level and component result uses exactly one status: `missing` means the
credential was absent; `rejected` means malformed, unsafe repository destination,
or evidence-backed refusal (GitHub HTTP 401/403/404 only when GitHub response headers identify the server); `network_error` means the GitHub transport failed;
`not_measured` means no reliable measurement was possible (missing CLI, timeout,
or local I/O failure); and `passed` requires the relevant operation to complete.
Never paste a token into an argument, issue, log, repository file, or Git history.
Do not place `CODEX_HOME`, Claude token output, or the encrypted TL bundle under
the checkout; warnings in documentation are not a substitute for the enforced
resolved-path guard.
