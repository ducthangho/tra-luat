# Ephemeral session credentials

Use `.claude/dev/session_credentials.py`; it reports only state and never a secret.

* `CODEX_HOME` is authoritative. If absent, every helper uses `~/.codex`. Codex materialization is rejected before decoding or writing when the effective `auth.json` resolves inside the repository, including through a symlinked parent.
* Capture a Claude Pro/Max subscription token with `python3 .claude/dev/session_credentials.py claude-capture --output /tmp/claude.token`. The output must resolve outside the repository. The helper checks that boundary before starting `claude setup-token`, suppresses its token-bearing output, and atomically writes mode `0600`. Load it as `CLAUDE_CODE_OAUTH_TOKEN` only for the Claude child.
* Set `GITHUB_PAT` in the session environment and run `python3 .claude/dev/session_credentials.py github-probe --repo ducthangho/tra-luat`. The PAT is mapped to `GH_TOKEN` only in the two `gh api` children (`user` and `repos/…`); it is absent from argv and reports.
* Keep `TL_MASTER_KEY` as the root for the existing encrypted Drive bundle. Run `python3 .claude/dev/session_credentials.py tl-bootstrap --env cowork --secrets-file /tmp/s.enc`; this delegates to `scripts/tl.py bootstrap` and does not duplicate GAS/GWS/NLM storage or crypto. `--secrets-file` is mandatory for both `tl-bootstrap` and the combined `bootstrap`; if absent, no provider or TL child is started.
* To perform all four steps in a single deterministic report, run `python3
  .claude/dev/session_credentials.py bootstrap --env cowork --secrets-file
  /tmp/s.enc --claude-token-file /tmp/claude.token`. This materializes
  `CODEX_AUTH_JSON` under the effective `CODEX_HOME`, passes the Claude token only
  to a minimal non-interactive Claude model probe (success requires a known marker
  in model stdout), normalizes and probes GitHub, and delegates the TL step.

Every top-level and component result uses exactly one status: `missing` means the
credential was absent; `rejected` means malformed, unsafe repository destination,
or refused (including GitHub HTTP 401/403/404); `network_error` means the GitHub transport failed;
`not_measured` means no reliable measurement was possible (missing CLI, timeout,
or local I/O failure); and `passed` requires the relevant operation to complete.
Never paste a token into an argument, issue, log, repository file, or Git history.
Do not place `CODEX_HOME`, Claude token output, or the encrypted TL bundle under
the checkout; warnings in documentation are not a substitute for the enforced
resolved-path guard.
