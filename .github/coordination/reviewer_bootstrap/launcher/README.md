# RA-04 Windows launcher and watchdog — WP125

Headless Reviewer launcher and controller-owned watchdog for Mission 76. This Packet owns only
`.github/coordination/reviewer_bootstrap/launcher/`; it reads the integrated RA-01 core, RA-02
sandbox/oracle and RA-03 gateway and modifies none of them.

Being under `.github/**` puts it outside the release bundle (`_RELEASE_EXCLUDE_DIRS`), so it neither
consumes the 200-file ceiling nor pulls `RELEASE_MANIFEST.json` into the write set.

This is candidate code, not the privileged deployed controller. Every control runs offline against
the integrated RA-01 fake store and sealed fixtures. Operational promotion, if it is ever
authorized after Mission land, must come from an exact canonical SHA copied outside every reviewed
worktree and re-pinned before each run.

## Run

```
python .github/coordination/reviewer_bootstrap/launcher/controller.py schema
python .github/coordination/reviewer_bootstrap/launcher/controller.py coverage
python .github/coordination/reviewer_bootstrap/launcher/controller.py inventory
python .github/coordination/reviewer_bootstrap/launcher/selftest.py
python -O .github/coordination/reviewer_bootstrap/launcher/selftest.py
python .github/coordination/reviewer_bootstrap/launcher/controller.py produce --out RUNDIR --run-id r1
python .github/coordination/reviewer_bootstrap/launcher/controller.py verify --root RUNDIR
```

Return codes: `0` ok · `2` rejected by a named category · `3` verification red · `64` usage.

Both interpreters are mandatory. `python -O` deletes `assert`, so a suite that asserts its security
properties proves nothing there — every check in this Packet is an explicit branch, and
`WP125-POS-012` scans the package to keep it that way.

## Components

| file | the invariant it holds |
|---|---|
| `argv.py` | one built argument vector; `--permission-mode dontAsk` exact; `auto`, duplicates, omission and injected switches are named failures |
| `environment.py` | child environment built from a named allowlist; exactly `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; PATH entries inside the candidate tree dropped |
| `inputs.py` | sealed, read-only, single-link inputs outside the candidate tree; reparse point, ADS, DOS device and traversal refused on the path spelling |
| `preflight.py` | seven ordered checks that return **observations**, audited against a required-key table; the claim is a separate commit point |
| `watchdog.py` | Job Object containment before the first descendant; identity = (pid, creation stamp); cleanup proven by two independent paths |
| `delegation.py` | closed operation set `{run_test}`; credential-freedom probed with a planted marker, not asserted |
| `parity.py` | denominators compared before outcomes; an undeclared skip is red |
| `inventory.py` | per-file SHA-256 reduced to one digest; static boundary scan for shell strings and bare `assert` |
| `orchestrate.py` | the one trusted preflight → claim → contained launch path |
| `registry.py` | the single registry of all 94 case IDs and their required check |
| `selftest.py` | the executable matrix; separate `scheduled`/`executed`/`passed`/`failed`/`skipped`/`not_run` |

## Three things this Packet paid for

**A Windows `HANDLE` is not a `c_int`.** ctypes defaults an undeclared return type to `c_int`, which
truncates a 64-bit handle to its low 32 bits. The truncated value is usually still non-zero, so the
failure does not look like one: the code proceeds to assign a child to a "job" that is not the job,
and the fence quietly stops fencing while reporting success. Every prototype in `watchdog.py` is
declared.

**A terminated Windows process still answers `GetProcessTimes`.** Any handle keeps the process
object alive — and the supervisor holds one through `Popen` — so "the creation stamp is still
readable" is not "still running". A cleanup proof built on that alone reports a corpse as a
survivor. The liveness test is `WaitForSingleObject(handle, 0)`, which also cannot be confused by a
child that legitimately exits with 259 (`STILL_ACTIVE`).

**The stdout pipe outlives the child.** A descendant inherits the write handle, so the pipe never
reaches EOF while an orphan lives; a drain thread then blocks in `read` holding the buffer lock, and
closing the stream from the supervisor deadlocks it against its own reader. The fix is also the
more correct behaviour: tear the tree down on **every** path before proving cleanup, not only on
timeout. Proving cleanup first would have reported a green receipt over a live orphan —
`WP125-NEG-034` now witnesses the contained descendant through the job's own census, because once a
parent has exited a process-table walk cannot see its orphan at all.

## Generation 2 — the six Reviewer findings, and what each one really was

Every finding was a control that *reported* success without *measuring* it. That is the shape worth
remembering: none of them failed loudly, and the suite was green over all six.

| finding | what generation 1 actually did | closed by |
|---|---|---|
| `WP125-RV-001` | `extra` accepted any non-credential-shaped name and wrote it straight into the child, so `{"PATH": …}` replaced the sanitized PATH computed six lines earlier, and `PYTHONPATH`/`BASH_ENV`/`NODE_OPTIONS` were injectable | a closed controller extra set, refusal of overrides, case-folded collisions and execution-influencing names by name, and identifier-shaped values |
| `WP125-RV-002` | the delegated body printed a report and exited zero regardless; `test_selection` rode along in argv and was never executed, the root was never checked, the OS was never checked | a closed test-ID→command map with real exit codes, a measured writability probe, git-verified root identity, and a declared-OS check that refuses rather than simulates |
| `WP125-RV-003` | the order guard was skipped for exactly the callers that supplied their own steps, so the seven-function substitution it existed to stop was the one case it never checked; receipts were plain dataclasses anyone could build | a production entry with no `steps` parameter, a sealed receipt, an independent value-binding stage that re-reads the pin, and provenance authenticated before `mint_claim` |
| `WP125-RV-004` | every piece of preflight → claim → launch existed and nothing performed the sequence, so only tests ever ran it, each slightly differently | `orchestrate.launch_reviewer`, plus a controlled fake executable that reports the argv a real Windows process received |
| `WP125-RV-005` | `active is None or active == 0` treated a *failed* Win32 census as clean — the state where the fence has lost sight of the tree was the state it called green | a census that names its reason, red on Windows when it cannot answer, and green only on `active == 0` plus clean recorded identities |
| `WP125-RV-006` | five RA-01 categories cannot express "the sealed source pin is present"; a run that dropped a required class still sealed cleanly | a table of all fourteen required classes with per-file binding headers, verified by exact name, schema, run, head and tree |

Two fixture measurements were needed to make the RV-002 controls real rather than decorative, and
both contradicted the obvious approach. A directory `chmod`-ed to `0o555` on this host still reports
`os.access(path, os.W_OK) == True` and still accepts file creation, so a mode-bit check would have
certified a writable directory as read-only. And `icacls /deny <user>:(W)` breaks the fixture
outright: the simple right `W` expands to `FILE_GENERIC_WRITE`, which includes `SYNCHRONIZE`, so
denying it makes the directory unopenable and `git -C` fails with "Permission denied" before it can
read anything. The working form denies only `WD,AD`.

## What this launcher does not claim

- The static scan cannot see a forbidden callable reached through a name built at run time, or a
  shell string assembled from individually innocuous fragments. `controller.py coverage` prints the
  full `not_covered` list.
- The environment boundary removes credential-shaped *variables*. It does not read or remove
  credentials resident in files under `HOME`/`USERPROFILE`, which the official CLI needs to find its
  own configuration.
- Delegation evidence binds a run to a candidate commit, tree and test selection. It does not make
  the delegated runner trusted; candidate-authored summaries are recorded as data and never used as
  proof.

A control that states its limits stays usable. One that claims everything does not — the lesson
already paid for at #54, where output announced `168/168 dat` while running bare.
