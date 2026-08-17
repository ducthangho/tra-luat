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
| `sourcepin.py` | the one authoritative source-pin structure, read by validation and evidence alike |
| `registry.py` | the single registry of all 125 case IDs and their required check |
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

## Review round 2 — eight findings, and the pattern behind them

Round 1 closed six findings and the suite went green over all of them. Round 2 found eight more, and
five were in the round-1 repairs themselves. The pattern is worth naming: **a control that names the
right property can still measure the wrong thing**, and a green suite cannot tell the difference.

| finding | what was still wrong after round 1 | closed by |
|---|---|---|
| `WP125-RV-003` | authorization was a module-private sentinel plus a `provenance` string — both fields the caller fills in. `from launcher.preflight import _SEAL` minted a real claim in one import | controller-held provenance keyed to witnessed observations, plus live re-validation at the commit point: the pin is re-read and the lease re-checked when the durable object is created |
| `WP125-RV-006` | exact-name structural verification passed a set that was structurally perfect and semantically stale — generation-1 authority, an empty delegation payload, a red matrix | generation-2 authority bound by value into every class, plus payload predicates: a green matrix must be green, a delegation receipt must carry an executed test with a real return code |
| `WP125-RV-007` | executable, working directory, variable arguments and prompt were ordinary values in the caller's context mapping | all consumed from a sealed input outside the candidate tree, hash-pinned, and compared byte for byte at final binding |
| `WP125-RV-008` | orchestration launched the full Reviewer vector regardless of surface, so a run that had *proved* no Windows sandbox existed still minted and invoked the local model command | routing on the selected surface; the delegated surface dispatches only the closed `run_test` job and records `model_command_invoked: false` |
| `WP125-RV-009` | the lease stop was a caller parameter, giving the fence a second clock nothing compared against the one preflight validated | the parameter is gone; the deadline is derived from the lease observation the trusted preflight bound |
| `WP125-RV-010` | every failure between `CreateProcess` and job adoption raised without touching a child that had been created **suspended** — the one path reporting "containment failed" was the one leaking a process | the direct handle is opened first and retained, the child is terminated unconditionally, waited on, and proven gone against the live process table before the red is returned |
| `SPEC-G2-001` | the permission screen only inspected switch-*shaped* tokens, so a bare `auto` walked past it in either argument run | every token screened case-folded in every prefix and trailing position, both duplicate spellings refused |
| `WP125-G2-GATE-001` | the read-only root fixture was built under an ASCII path only | the exact-root clone now lives behind a Vietnamese directory, and git identity is verified through that Unicode gitdir |

`WP125-RV-010` is the one to read twice. The first repair opened the direct handle *after* the
`OpenProcess` call it was meant to survive, so when that call was the injected failure there was no
handle left to kill with — and the new case caught it, red, before the repair shipped. The
terminator of last resort is the handle `Popen` already holds from creation, which cannot fail to
exist.

## Review round 3 — seven clusters, and where the boundaries actually were

Round 2 closed eight findings; round 3 found seven more, six of them one field outside a round-2
repair. The lesson compounds: **a control repaired at the wrong radius is still a control that
measures the wrong thing.**

| cluster | what round 2 still left open | closed by |
|---|---|---|
| `RV-003-R2` | authorization was a module-private sentinel plus a caller-filled `provenance`, then a module-level table — all candidate-visible. It signed only the *observations*, so the plan, environment and surface the claim licences sat outside the signature | a keyed digest over the whole binding (observations **and** plan, environment, surface) under a per-process secret held in a closure. No table to write into, and a genuine token does not verify against swapped content |
| `RV-006-R2` | the wrapper was checked, the payload was not: a correct generation-2 header around generation-1 semantics passed | nested authority validation (packet/revision/generation/spec/ref/lease) plus a recursive stale-marker walk over the payload itself |
| `RV-007-R2` | the SHA-256 anchors were checked `if expected_sha` — opt-in, and the party they protect against fills in the context | anchors mandatory; byte-for-byte readback immediately before the claim **and** again immediately before spawn or dispatch |
| `RV-008-R2` | the delegated surface pulled `commands[0]` out of the job and ran it directly, skipping the Linux identity check, the read-only-root proof, the credential probe, the per-test return codes and the cleanup receipt | the surface routes through `delegation.run_job`, the complete existing validator and runner, and an unknown or partial job is refused before any claim exists |
| `RV-009-R2` | routing was validated *after* the claim, so an invalid delegated job left a durable claim behind | all surface, job, root, identity and deadline validation completes before the transactional commit |
| `RV-010-R2` | `terminated: True` was written unconditionally — it recorded that a kill had been *attempted* | every field is an observation: what the API returned, what the wait returned, what an independent census says. `proven_gone` requires all four legs, so an unidentifiable child is named red rather than assumed clean |
| `GATE-001` | the clone sat under a Unicode path, but the *linked source gitdir* did not | a detached linked checkout whose `.git` file points into a Unicode gitdir, with the full suite run from it under both interpreters |

Three defects surfaced only because the gates were built to catch them, and each was a live bug in
this package rather than in the test:

1. **`text=True` decodes subprocess pipes through the console code page.** On this host that is
   cp1258, and git quotes the Unicode path in its messages, so the reader thread died and `stderr`
   arrived as `None` — surfacing as `'NoneType' object is not subscriptable`, which reads like a
   broken assertion rather than a decoding fault. Every git call around a Unicode path now captures
   bytes and decodes UTF-8 explicitly, including `verify_read_only_root` via `binary=True`.
2. **`git worktree add` writes into the source's `.git/worktrees/`.** The read-only root is
   deny-ACLed, so it cannot also be the linked source. The two fixtures want opposite things from
   one directory and now get two.
3. **A parent-table walk from a *dead* root harvests unrelated processes.** Windows reuses a pid the
   moment it is free, and `th32ParentProcessID` keeps pointing at the number. Measured: ten
   "survivors" while the Job Object census said zero active. Cleanup now walks descendants only from
   roots that are still alive — the job is the authority for the tree, which is why it exists.

## Review round 4 — six clusters, and the one that was never executed

| cluster | what round 3 still left open | closed by |
|---|---|---|
| `RV-006-R3` | **`SEMANTIC_REQUIREMENTS` had `authority_input.json` twice.** Python keeps the last entry, so the permissive `_nonempty` replaced the strict predicate and every nested authority check written in round 3 was dead code. Measured: `{"authority": "anything"}` verified green | one key, one composed strict predicate covering Mission revision/plan hash, Packet issue/revision/generation/attempt/spec hash, candidate ref/start head/tree and lease identity — plus a build-time guard that refuses a table which does not cover the classes exactly once |
| `RV-003-R3` | the binding signed environment *names* and the memory flag, so `PATH` could be repointed between preflight and claim while the signature still verified. And the mint closure was bound to a module-level name, leaving the capability importable | the blob covers every allowlisted name **and value**; the signing authority is an instance guarded by a capability token, so there is no module-callable mint |
| `RV-008-R3` | the job was checked against *itself* — internally consistent and entirely fabricated passed | an eligible Linux runner is required and read from the machine, every command is reconstructed from the closed test-ID map and compared, the root is re-probed live, and the candidate identity is re-measured |
| `RV-009-R3` | — | the same sealed job is authenticated again immediately before dispatch, and every negative proves zero claims, children and jobs |
| `RV-010-R3` | `killpg(getpgid(root))` asks the root for its group at kill time, which fails with `ESRCH` exactly when the root has already exited — the orphaned-group case | pgid and session are captured at adoption and retained independently; the group is terminated and censused by that identity, and a Windows "not applicable" census is never accepted as POSIX cleanup proof |
| `GATE-001-R3` | the linked Unicode gitdir needed an ownership declaration | per-command `-c safe.directory=` for both the worktree and its linked gitdir; neither global nor repository git configuration is written, and the case asserts both remain unmutated |

The duplicate-key finding is the one worth carrying forward. Nothing failed, nothing warned, and the
code read correctly at every review — a validator can be written, reviewed, committed and never once
executed, and the only thing that would have caught it is asking the table *which function it
actually holds*. That question is now a registered case.

One consequence is worth stating plainly rather than hiding in a diff: after `RV-008-R3` the
delegated surface requires a real Linux runner, so on this Windows host the contract-correct outcome
is a **refusal before any operation**. `WP125-RV-008-delegated-surface-dispatches-only-run-test`
asserts exactly that here and asserts the dispatch on a Linux runner. Fabricating a Linux dispatch on
Windows is what §7 forbids, so the case branches on the measured runner rather than skipping.

## Review round 5 — what the Unicode gate was actually about

The round-4 evidence reported 107/122 from a fresh detached Unicode linked-worktree while direct
`rev-parse` was green. Reproducing that split, with `GIT_TEST_ASSUME_DIFFERENT_OWNER=1` to make the
ownership check fire on a machine where the runner owns everything, produced three measurements that
between them explain it — and two of them contradicted the obvious reading:

1. **`-c safe.directory=` does work** for the process it configures. That is why round 3's direct
   verification was green, and why the green said nothing about anything else. An earlier probe here
   suggested git ignored it entirely; that probe only ever tested clones, and the case now pins the
   true behaviour so the note cannot drift back.
2. **The grant does not reach the transport child.** `file://` starts `upload-pack` *inside the
   source repository*, and that process performs its own ownership check. Neither `-c` nor an
   ephemeral `GIT_CONFIG_GLOBAL` rescues it: the clone dies with "Could not read from remote
   repository."
3. **The trust set was incomplete anyway.** A linked worktree's gitdir holds refs and HEAD; the
   objects live in the **common** gitdir. Measured here: the source gitdir is
   `D:/Quốc hội/tra-luat/.git/worktrees/<name>` and the common dir is `D:/Quốc hội/tra-luat/.git` —
   both non-ASCII, and only the first was ever declared.

So the repair is the transport, not the declaration: the fixtures clone by plain local path, which
spawns no `upload-pack`, and the trust set now names the worktree, the linked gitdir, the common
gitdir and the main worktree — resolving a relative `commondir` pointer rather than using it as
written. Nothing is written to global or repository configuration; where an inheritable grant is
still wanted, `GIT_CONFIG_GLOBAL` points at a scratch file that dies with the run.

| cluster | what round 4 left open | closed by |
|---|---|---|
| `GATE-001-R4` | above | plain-path clone, complete trust set, and a control that forces the ownership check on so it cannot be vacuous |
| `RV-003-R4` | the authorization object and its capability token sat side by side as module attributes — `_AUTHORITY.mint(_MINT_TOKEN, …)` minted anything | the signing capability is **gone**. The commit point rebuilds the environment and the launch plan from the sealed inputs and requires equality, so authorization is re-derivation rather than attestation and there is nothing left to steal |
| `RV-006-R4` | start head and tree were accepted as merely OID-shaped, repository equality was omitted, and the retained evidence named the *integration* commit | one typed `sourcepin.PIN` feeds production validation and retained evidence, and the repair base and the integration observation are asserted to be different commits |
| `RV-008-R4` | a local OS check is not a Windows-controller-to-Linux route | the surface requires a Dispatcher-declared transport and **fails closed as environment-unavailable** without one — which is this host's honest state |
| `RV-010-R4` | the session was captured and never used; kill and census trusted a reusable numeric pgid | the group identity is pgid *plus* session, checked before any signal or census, with a supplied-table probe so the logic executes on Windows too |

## Review round 6 — five clusters, and the two that were the same mistake

Two of the five clusters were the same defect at different altitudes: **a comparison whose two sides
came from the same place.**

`RV-003-R5` was the sharp one. A complete fault-injection receipt reached durable claim commit under
both interpreters, and every check it faced was satisfiable, because claim-time authority was
rederived from `context["expected_authority"]` — the caller's own dictionary — and compared against
observations the same caller supplied. The sealed source pin was on disk the whole time and was only
ever *hashed*. A digest answers "are these the bytes we were told about"; it answers nothing about
what the bytes say, and nobody read a field of it.

The repair has two halves and both are structural:

- **The sealed pin is parsed.** `sourcepin.PIN.validate_sealed_document` compares eighteen pinned
  fields, and the resulting table is the only expectation table the binding stage uses. A caller may
  still declare expectations; they are checked *against* the pin, so a caller who expects the wrong
  thing is refused even when its run would otherwise be correct.
- **The commit capability left the package.** There is no `mint_claim`; no launcher module imports a
  durable store; `launch_reviewer` takes a required `commit_capability` with no default, no factory
  and no registry. The importable path produces a `ClaimVerification` and cannot create a claim. And
  because hiding a capability has failed three rounds running, the forgery defence is not a hidden
  name at all: `verify_claim_authorization` re-runs the **trusted** step map over the same context
  and requires the presented receipt to reproduce it, modulo the one declared volatile field. A
  fabricated receipt differs; a receipt that does not differ is the trusted path's own output.

`RV-006-R5` was the same shape one level out: the retained semantic check verified a hand-written
list of fields, so it proved exactly the fields somebody remembered to write down — repository,
absolute lease stop and integration observation were all absent from it, and a nested payload that
was valid and wrong verified green. The comparison is now a **total leaf walk** against a document
rebuilt by the same builder `produce` uses, with only the run-dependent leaves (runner, raw outcomes,
surface) excepted by name and checked for meaning instead.

| cluster | what round 5 left open | closed by |
|---|---|---|
| `GATE-001-R5` | the Unicode gate re-ran the whole suite twice, nested, each nested run rebuilding its own clones — 770.9 s measured, and the Reviewer's optimized matrix was cut off past 14 minutes with no denominator. The ACL command's exit code was treated as proof of a read-only root | every fixture operation carries a controller-owned deadline; the gate uses a **bounded non-recursive probe** and the complete matrix from that boundary is a controller gate rather than a case inside itself; the root proves itself by **attempting a write** and fails closed when the write succeeds |
| `RV-003-R5` | above | above |
| `RV-006-R5` | above | above |
| `RV-008-R5` | the declared Linux transport was only checked for truthiness and never invoked; execution stayed local and the runner OS was read from `platform.system()` on the *controller* | a sealed transport envelope bound to the pin digest, **actually called** with a closed request carrying no command line and no credential; the answer's OS, root, head, tree, selection and return codes are re-derived here before anything is retained; unconfigured is `environment_unavailable` and the evidence names `production_linux` or `offline_test_double` so the two can never be one green |
| `RV-010-R5` | leader creation identity was absent and an unreadable member session counted as agreement | leader **and** member identity are pid *plus* creation stamp, captured at adoption and revalidated before every signal and census; unreadable is fail-closed; the orphaned group stays nameable after the root exits because the identity is not a naked pgid |

The honest statement about `RV-008-R5` on this host: **no authenticated production Linux transport is
configured here, so the production path fails closed.** The offline double proves the contract is
called and that wrong answers are refused; it is not Linux evidence and the retained receipt says so.

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
