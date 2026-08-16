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
| `registry.py` | the single registry of all 64 case IDs and their required check |
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
