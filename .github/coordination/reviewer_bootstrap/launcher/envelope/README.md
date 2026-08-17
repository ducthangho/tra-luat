# RA-04A launch envelope — WP149

This package turns a sealed controller plan into one immutable description of a Claude Reviewer
launch: an executable path, a structured argument tuple carrying exactly one
`--permission-mode dontAsk`, a working directory, a closed child environment with automatic memory
disabled, a stdin binding for the prompt, and evidence digests.

It is side-effect-free. Nothing here performs a process spawn, mints a claim, renews a lease, runs
a watchdog, opens a Job Object, calls GitHub, writes durable state, or performs any delegation or
transport. `boundary.py` refuses the capability statically and `selftest.py` proves the scan fires
by running hostile snippets through it.

## Interface

```python
from launcher.envelope import build_launch_envelope, verify_launch_envelope

envelope = build_launch_envelope(controller_root, "launch plan.json")
verify_launch_envelope(envelope)   # raises unless it is authentic AND still matches disk
envelope.arguments                 # tuple of whole tokens, never a shell string
envelope.environment               # read-only mapping built from an empty starting point
envelope.sealed_inputs             # verified byte snapshots plus (device, inode, size) identity
envelope.stdin_path                # the sealed prompt; never an argument
envelope.as_evidence()             # fresh canonical-JSON copy of the retained evidence
```

There is deliberately **no `is_sealed()`**. A boolean an object answers about its own
trustworthiness is worth exactly as much as the object, and an instance forged with
`object.__new__` answered it happily. `verify_launch_envelope` instead consults a record held
outside the instance (`attestation.py`), re-derives the payload digest from the fields as they
stand now, and re-reads the controller's sealed files. No authority token is exported, so there is
nothing a candidate can mint or present.

The candidate checkout is derived from `__file__`, not passed in. The interface takes no command,
no environment extras, no boolean trust claim, no pre-computed observation, no shell text and no
callback.

`launcher/` is an implicit namespace package with no `__init__.py`, because this Packet's write set
is the `launcher/envelope/` prefix exactly. Put `.github/coordination/reviewer_bootstrap` on
`sys.path` before importing.

## Sealed plan (schema 2)

Every input lives outside the candidate checkout and must be absolute, regular, read-only,
single-link, with a read-only parent and no link anywhere in its ancestry.

```json
{
  "schema_version": 2,
  "permission_mode": "dontAsk",
  "binding": {
    "artifact": "wp149-ra04a-launch-envelope",
    "source_pin_sha256": "<64 lowercase hex>",
    "run_id": "<bounded identifier>",
    "head": "<40 hex>",
    "tree": "<40 hex>"
  },
  "trusted_roots": ["<absolute directory>"],
  "executable": {"path": "<absolute>", "sha256": "<64 lowercase hex>"},
  "settings":   {"path": "<absolute>", "sha256": "<64 lowercase hex>"},
  "prompt":     {"path": "<absolute>", "sha256": "<64 lowercase hex>"},
  "working_directory": "<absolute directory>",
  "environment": {"PATH": ["<absolute directory>"], "LANG": "vi_VN.UTF-8"}
}
```

Identity bindings — artifact, source pin, run, HEAD and tree — come from this sealed block and
never from a caller field, and their SHA-256 is carried in the evidence. `trusted_roots` is the set
of directories the controller vouched for; every sealed input, working directory and search-path
entry must sit inside one. The plan only ever *agrees* with `permission_mode`; the value that
reaches the argument vector is a module constant.

`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` is injected here and cannot be declared by the plan in any
spelling. Sealed inputs are digest-verified, their bytes retained, and re-read after assembly.

### Environment names deliberately omitted

`HOME`, `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, `PROGRAMDATA`, `PROGRAMFILES`, `COMSPEC`,
`TEMP`, `TMP`, `TMPDIR` and `TERM` are **not** in the allowlist. For the first six, a trustworthy
path is not the property that matters — they are roots from which tools load configuration,
credentials and plugins before reaching their own entry point. `COMSPEC` hands the child a shell.
The temp names request a writable scratch root, and this Packet is side-effect-free. `TERM` decides
nothing in a headless run.

## Declared non-coverage

Writing down the edges is part of the deliverable, not an apology for it.

- **Windows write permission is a read-only attribute, not an ACL.** `path_writable` and
  `path_writable_parent` are decided from `st_mode`, which on Windows reflects only the read-only
  attribute of the file or directory. ADR-0021 puts the controller and the candidate under one
  unprivileged account with no LIVE credential, so this control cannot be — and is not claimed to
  be — proof that no other principal can write. It is a measured attribute check that a controller
  can set and a reviewer can observe.
- **The read-only-parent rule applies to sealed files only.** A trusted root and a working
  directory live inside ordinary writable directories by their nature.
- **Symlink and reparse-point rejection is measured, but not always with a real link.** An
  unprivileged Windows account cannot create a symlink without Developer Mode, so
  `WP149-NEG-034` and `WP149-R1-008` fall back to a `portable_symlink_lstat` fixture that drives
  the exact `lstat` branch with a symlink-mode stat result. The case evidence names which fixture
  ran. Where a real hard link is possible the suite uses one and reports `filesystem_hard_link`.
  No claim is made that a real Windows reparse point was constructed and rejected end to end.
- **"Untrusted config-loading path"** is enforced as: inside the candidate tree, relative, empty,
  current-directory, separator-smuggling, non-existent, non-directory, a link, or outside every
  controller trusted root. Whether a directory that passes all of those is writable by some other
  local principal is the ACL question above.
- **The static scan is a smoke alarm, not a wall.** `boundary.COVERAGE["not_covered"]` names what
  it cannot see, including capability reached through a computed `getattr` or a runtime-built
  string. The real boundary is the Packet write set plus independent review.
- **Colons inside path names** are refused on every platform, not only where they mean an alternate
  data stream. That is stricter than POSIX requires and is deliberate.
- **The executable is hashed in full**, and a sealed input whose read-back length disagrees with
  its own `st_size` is refused as `sealed_input_short_read` rather than hashed: the shared reader
  in `oracle/safe_io.py` opens without `O_BINARY`, so on Windows a file containing CRLF would
  otherwise yield a confident digest of bytes that are not on disk. Fixing the shared reader is
  outside this Packet's write set; refusing the ambiguous read is not.
- **No filesystem mutation is performed or claimed.** The module never creates, chmods, moves or
  deletes anything, including the controller's inputs; `WP149-POS-016` measures that the sealed
  directory is byte- and mode-identical after a build.

## Inventory

The inventory covers **every regular file** below the prefix, at any depth, with no exclusion list
(`inventory.EXCLUDED_NAMES` is empty, and the evidence reports it). To keep that honest,
`selftest.py` sets `sys.dont_write_bytecode` before importing the package so the owned tree never
acquires a `__pycache__`, and `WP149-R1-017` fails loudly if generated cache is present anyway.

## Running the matrix

```text
python .github/coordination/reviewer_bootstrap/launcher/envelope/selftest.py
python -O .github/coordination/reviewer_bootstrap/launcher/envelope/selftest.py
```

Both runs schedule the same denominator and report scheduled, executed, passed, failed, skipped and
not-run. Any nonzero failed, skipped or not-run count is red, and a shrinking `scheduled` is red as
well — `WP149-POS-020` fails if a required check loses its last case. Security branches are explicit
`if`/`raise`, never `assert`, so `python -O` executes the same teeth; `WP149-POS-011` measures that
on the source instead of restating it.

The Packet's four remaining required checks — repository selftest, strict release verification,
release-bundle determinism and `git diff --check` — are repository gates run outside this file and
are named in `selftest.EXTERNAL_GATES`.
