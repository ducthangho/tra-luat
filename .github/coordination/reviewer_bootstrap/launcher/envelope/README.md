# RA-04A launch envelope — WP149

This package turns a sealed controller plan into one immutable description of a Claude Reviewer
launch: an executable path, a structured argument tuple carrying exactly one
`--permission-mode dontAsk`, a working directory, a closed child environment with automatic memory
disabled, a stdin binding for the prompt, and evidence digests.

It is deliberately side-effect-free. Nothing here spawns a process, mints a claim, renews a lease,
supervises a watchdog, opens a Job Object, calls GitHub, writes durable state or dispatches Linux
work. The static boundary scan in `boundary.py` refuses the capability to do any of those, and
`selftest.py` proves the scan itself fires by running hostile snippets through it.

## Interface

```python
from launcher.envelope import build_launch_envelope

envelope = build_launch_envelope(controller_root, "launch plan.json")
envelope.arguments            # tuple of whole tokens, never a shell string
envelope.environment          # read-only mapping built from an empty starting point
envelope.stdin_path           # the sealed prompt; never an argument
envelope.as_evidence()        # fresh canonical-JSON copy of the retained evidence
```

The candidate checkout is derived from `__file__`, not passed in. The interface takes no command,
no environment extras, no boolean trust claim, no pre-computed observation, no shell text and no
callback: each of those would let a caller decide the answer this package exists to compute.

`launcher/` is an implicit namespace package with no `__init__.py`, because this Packet's write set
is the `launcher/envelope/` prefix exactly. Put `.github/coordination/reviewer_bootstrap` on
`sys.path` before importing, as the RA-01/RA-02/RA-03 packages already require.

## Sealed plan

The plan lives outside the candidate checkout and must be absolute, regular, read-only and
single-link, like every file it points at.

```json
{
  "schema_version": 1,
  "permission_mode": "dontAsk",
  "executable": {"path": "<absolute>", "sha256": "<64 lowercase hex>"},
  "settings":   {"path": "<absolute>", "sha256": "<64 lowercase hex>"},
  "prompt":     {"path": "<absolute>", "sha256": "<64 lowercase hex>"},
  "working_directory": "<absolute directory>",
  "environment": {"PATH": ["<absolute>", "..."], "TEMP": "<absolute>", "LANG": "vi_VN.UTF-8"}
}
```

The plan only ever AGREES with `permission_mode`; the value that reaches the argument vector is a
module constant. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` is injected here and cannot be declared by the
plan in any spelling. Every sealed input is read, digest-checked, and then read AGAIN once the
envelope is otherwise complete, so a path or content swap during assembly cannot ride out on an
envelope that was already approved.

## Declared non-coverage

Writing down the edges is part of the deliverable, not an apology for it.

- **"Untrusted config-loading path"** is enforced as `PATH` entries that are inside the candidate
  tree, relative, empty, current-directory, separator-smuggling or hostile in spelling. Whether an
  absolute directory outside the candidate is writable by another local principal is an ACL
  question this offline module cannot answer, so it does not pretend to.
- **The static scan** is a smoke alarm, not a wall; `boundary.COVERAGE["not_covered"]` names what
  it cannot see, including capability reached through a computed `getattr` or a runtime-built
  string. The real boundary is the Packet write set plus independent review.
- **Colons inside path names** are refused on every platform, not only where they mean an alternate
  data stream. That is stricter than POSIX requires and is the deliberate choice.
- **The executable is hashed in full.** For a large launcher binary that is real work; the
  alternative is an envelope that pins a path but not the bytes behind it.
- **A sealed input whose read-back length disagrees with its own `st_size` is refused** as
  `sealed_input_short_read` rather than hashed. The shared hardened reader in `oracle/safe_io.py`
  opens without `O_BINARY`, so on Windows a file containing CRLF would otherwise produce a
  confident digest of bytes that are not on disk. Fixing the shared reader is outside this
  Packet's write set; refusing the ambiguous read is not.

## Running the matrix

```text
python .github/coordination/reviewer_bootstrap/launcher/envelope/selftest.py
python -O .github/coordination/reviewer_bootstrap/launcher/envelope/selftest.py
```

Both runs schedule the same denominator and report scheduled, executed, passed, failed, skipped
and not-run. Any nonzero failed, skipped or not-run count is red, and a shrinking `scheduled` is
red as well — `WP149-POS-020` fails if a required check loses its last case. Security branches are
explicit `if`/`raise`, never `assert`, so `python -O` executes the same teeth; `WP149-POS-011`
measures that on the source instead of restating it.

The Packet's four remaining required checks — repository selftest, strict release verification,
release-bundle determinism and `git diff --check` — are repository gates run outside this file.
They are named in `selftest.EXTERNAL_GATES` so the report says which checks it does not cover.
