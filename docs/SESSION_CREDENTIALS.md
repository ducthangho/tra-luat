# Ephemeral session credentials

Use `.claude/dev/session_credentials.py`; it reports only state and never a secret.

* `CODEX_HOME` is authoritative. If absent, every helper uses `~/.codex`.
* Capture a Claude Pro/Max subscription token with `python3 .claude/dev/session_credentials.py claude-capture --output /tmp/claude.token`. The helper runs `claude setup-token`, suppresses its token-bearing output, and atomically writes mode `0600`. Load it as `CLAUDE_CODE_OAUTH_TOKEN` only for the Claude child.
* Set `GITHUB_PAT` in the session environment and run `python3 .claude/dev/session_credentials.py github-probe --repo ducthangho/tra-luat`. The PAT is mapped to `GH_TOKEN` only in the two `gh api` children (`user` and `repos/…`); it is absent from argv and reports.
* Keep `TL_MASTER_KEY` as the root for the existing encrypted Drive bundle. Run `python3 .claude/dev/session_credentials.py tl-bootstrap --env cowork --secrets-file /tmp/s.enc`; this delegates to `scripts/tl.py bootstrap` and does not duplicate GAS/GWS/NLM storage or crypto.

Statuses are `missing`, `rejected`, `network_error`, `not_measured`, and `passed`.
Never paste a token into an argument, issue, log, repository file, or Git history.
