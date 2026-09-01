#!/usr/bin/env python3
import base64
import importlib.util
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

P = Path(__file__).with_name("session_credentials.py")
spec = importlib.util.spec_from_file_location("session_credentials", P)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


def directory_root_lock(module):
    """Exact directory roots are guarded as directories, not as file targets."""
    repository = P.resolve().parents[2]
    module.REPOSITORY_ROOT = repository
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        secrets_file = root / "bundle.enc"
        safe_home = root / "safe-home"; safe_home.mkdir()
        worktree = root / "exact-worktree"; (worktree / ".git").mkdir(parents=True)
        directory_keys = (
            "HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME",
            "GOOGLE_WORKSPACE_CLI_CONFIG_DIR", "TL_CACHE_DIR",
            "TMPDIR", "TMP", "TEMP",
        )

        # Every directory-valued input must reject the candidate itself when
        # that candidate is the worktree root.  The older file-target guard
        # began at candidate.parent and therefore missed exactly this case.
        for key in directory_keys:
            env = {"TL_MASTER_KEY": "TL_CANARY", "HOME": str(safe_home),
                   key: str(worktree)}
            with mock.patch.object(module.subprocess, "run") as child:
                result = module.tl_bootstrap("cowork", secrets_file, env=env)
            assert result == {
                "status": "rejected", "reason": "secret_destination_in_repository"
            }, (key, result)
            child.assert_not_called()

        # Bare repositories and an exact link alias have the same boundary.
        bare = root / "bare.git"
        (bare / "objects").mkdir(parents=True); (bare / "refs").mkdir()
        (bare / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        (bare / "config").write_text("[core]\n\tbare = true\n", encoding="utf-8")
        try:
            module.directory_destination(bare)
            assert False, "exact bare-repository directory root accepted"
        except module.UnsafeSecretDestination:
            pass
        with mock.patch.object(module.subprocess, "run") as child:
            result = module.tl_bootstrap("cowork", secrets_file, env={
                "TL_MASTER_KEY": "TL_CANARY", "HOME": str(bare)})
        assert result == {
            "status": "rejected", "reason": "secret_destination_in_repository"
        }, result
        child.assert_not_called()

        alias = root / "repository-alias"
        alias_available = False
        if os.name == "nt":
            alias_available = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(alias), str(worktree)],
                stdin=subprocess.DEVNULL, capture_output=True).returncode == 0
        else:
            alias.symlink_to(worktree, target_is_directory=True)
            alias_available = True
        if alias_available:
            try:
                module.directory_destination(alias)
                assert False, "exact repository link/junction alias accepted"
            except module.UnsafeSecretDestination:
                pass
            with mock.patch.object(module.subprocess, "run") as child:
                result = module.tl_bootstrap("cowork", secrets_file, env={
                    "TL_MASTER_KEY": "TL_CANARY", "HOME": str(alias)})
            assert result == {
                "status": "rejected", "reason": "secret_destination_in_repository"
            }, result
            child.assert_not_called()

        # External roots, including roots that do not exist yet, retain the
        # delegated-child behavior and are passed in canonical form.
        for key in directory_keys:
            future = root / "future" / key.lower()
            env = {"TL_MASTER_KEY": "TL_CANARY", "HOME": str(safe_home),
                   key: str(future)}
            completed = mock.Mock(returncode=0)
            with mock.patch.object(module.subprocess, "run", return_value=completed) as child:
                result = module.tl_bootstrap("cowork", secrets_file, env=env)
            assert result["status"] == "passed", (key, result)
            assert child.call_count == 1
            assert child.call_args.kwargs["env"][key] == str(future.resolve(strict=False))


def provider_home_lock(module):
    """Ambient temp roots never select or reach provider credential storage."""
    original_repository = module.REPOSITORY_ROOT
    original_tempdir = tempfile.tempdir
    with tempfile.TemporaryDirectory(prefix="provider-home-lock-") as td:
        root = Path(td)
        repo = root / "repo"; (repo / ".git").mkdir(parents=True)
        ambient = repo / "ambient-temp"; ambient.mkdir()
        module.REPOSITORY_ROOT = repo
        source = {
            "PATH": os.environ.get("PATH", ""),
            "TMPDIR": str(ambient), "TMP": str(ambient), "TEMP": str(ambient),
            "CODEX_AUTH_JSON": "CODEX_CANARY",
            "CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CANARY",
            "GITHUB_PAT": "GH_CANARY", "TL_MASTER_KEY": "TL_CANARY",
        }
        try:
            # tempfile caches its selected root.  Reset it so this is a real
            # ambient-temp attack, not a source-dict-only simulation.
            with mock.patch.dict(os.environ, {
                    "TMPDIR": str(ambient), "TMP": str(ambient), "TEMP": str(ambient)}):
                tempfile.tempdir = None
                with module._isolated_child_env(
                        source, CLAUDE_CODE_OAUTH_TOKEN="CLAUDE_CANARY") as child:
                    keys = {"HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
                            "XDG_DATA_HOME", "XDG_STATE_HOME", "TMPDIR", "TMP", "TEMP"}
                    assert keys <= set(child), child
                    resolved = [Path(child[key]).resolve(strict=True) for key in keys]
                    assert all(repo.resolve() not in (path, *path.parents) for path in resolved), child
                    assert len({child["TMPDIR"], child["TMP"], child["TEMP"]}) == 1
                    assert child["CLAUDE_CODE_OAUTH_TOKEN"] == "CLAUDE_CANARY"
                    assert not (set(module.SECRET_ENV) - {"CLAUDE_CODE_OAUTH_TOKEN"}) & set(child)

            # Allocation/permission failure is a pre-child refusal for both
            # subprocess-based provider probes.
            with mock.patch.object(module, "_private_provider_home",
                                   side_effect=OSError("fixture secure-root failure")), \
                 mock.patch.object(module.subprocess, "run") as child:
                claude = module.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S"})
                github = module.github_probe("o/r", env={"GITHUB_PAT": "S"})
            assert claude == {"status": "not_measured",
                              "reason": "provider_storage_unavailable"}
            assert github == {"status": "not_measured",
                              "reason": "provider_storage_unavailable", "endpoints": {}}
            child.assert_not_called()
        finally:
            module.REPOSITORY_ROOT = original_repository
            tempfile.tempdir = original_tempdir


def provider_cleanup_lock(module):
    """Cleanup failure/residual/swap can never leave a provider probe passed."""
    marker = "TRALUAT-CLAUDE-CREDENTIAL-OK"
    good = mock.Mock(returncode=0, stdout=marker + "\n", stderr="")
    real_rmtree = module.shutil.rmtree
    real_subprocess_run = subprocess.run

    def private_base(root: Path) -> Path:
        base = root / "trusted-provider-base"
        base.mkdir(mode=0o700)
        return base

    def remove_fixture(entry: Path) -> None:
        try:
            info = entry.lstat()
        except FileNotFoundError:
            return
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if stat.S_ISLNK(info.st_mode):
            entry.unlink()
        elif reparse and getattr(info, "st_file_attributes", 0) & reparse:
            os.rmdir(entry)
        else:
            real_rmtree(entry)

    # Positive control: the allocated exact root and cleanup tombstones vanish.
    with tempfile.TemporaryDirectory(prefix="provider-cleanup-positive-") as raw:
        base = private_base(Path(raw))
        with mock.patch.object(module, "_trusted_provider_temp_base", return_value=base):
            with module._private_provider_home() as home:
                allocated = Path(home).parent
                assert allocated.is_dir()
        assert not allocated.exists() and list(base.iterdir()) == []

    # A raising delete already must be surfaced as not_measured, never passed.
    with tempfile.TemporaryDirectory(prefix="provider-cleanup-raise-") as raw:
        base = private_base(Path(raw))
        try:
            with mock.patch.object(module, "_trusted_provider_temp_base", return_value=base), \
                 mock.patch.object(module.shutil, "rmtree",
                                   side_effect=OSError("fixture delete failure")), \
                 mock.patch.object(module.subprocess, "run", return_value=good):
                result = module.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "FIXTURE"})
            assert result["status"] == "not_measured", result
        finally:
            for entry in list(base.iterdir()):
                remove_fixture(entry)

    # The old ignore_errors path converts a silent residual into a false pass.
    with tempfile.TemporaryDirectory(prefix="provider-cleanup-residual-") as raw:
        base = private_base(Path(raw))
        try:
            with mock.patch.object(module, "_trusted_provider_temp_base", return_value=base), \
                 mock.patch.object(module.shutil, "rmtree", return_value=None), \
                 mock.patch.object(module.subprocess, "run", return_value=good):
                result = module.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "FIXTURE"})
            assert result["status"] == "not_measured", \
                f"silent cleanup residual was reported as {result}"
            assert list(base.iterdir()), "fixture did not leave the required residual root"
        finally:
            for entry in list(base.iterdir()):
                remove_fixture(entry)

    # Swap the exact allocated name to an external link/junction while the
    # child runs. Cleanup must reject it before asking rmtree to touch it.
    with tempfile.TemporaryDirectory(prefix="provider-cleanup-swap-") as raw:
        fixture = Path(raw)
        base = private_base(fixture)
        victim = fixture / "external-victim"
        victim.mkdir()
        marker_file = victim / "MUST_SURVIVE"
        marker_file.write_text("UNCHANGED", encoding="utf-8")
        moved = base / "allocated-before-swap"
        cleanup_calls = []

        def swapped_root(info):
            reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
            return (stat.S_ISLNK(info.st_mode)
                    or bool(reparse and getattr(info, "st_file_attributes", 0) & reparse))

        def child_run(_cmd, **kwargs):
            allocated_root = Path(kwargs["env"]["HOME"]).parent
            allocated_root.rename(moved)
            if os.name == "nt":
                made = real_subprocess_run(
                    ["cmd.exe", "/d", "/c", "mklink", "/J",
                     str(allocated_root), str(victim)],
                    stdin=subprocess.DEVNULL, capture_output=True).returncode == 0
                assert made, "could not construct cleanup junction swap fixture"
            else:
                allocated_root.symlink_to(victim, target_is_directory=True)
            return good

        def observed_rmtree(path, *args, **kwargs):
            candidate = Path(path)
            if swapped_root(candidate.lstat()):
                cleanup_calls.append(candidate)
                return None  # mutation witness: never follow the external link
            return real_rmtree(path, *args, **kwargs)

        try:
            with mock.patch.object(module, "_trusted_provider_temp_base", return_value=base), \
                 mock.patch.object(module.shutil, "rmtree", side_effect=observed_rmtree), \
                 mock.patch.object(module.subprocess, "run", side_effect=child_run):
                result = module.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "FIXTURE"})
            assert result["status"] == "not_measured", result
            assert cleanup_calls == [], \
                f"cleanup handed a swapped root link to rmtree: {cleanup_calls}"
            assert marker_file.read_text(encoding="utf-8") == "UNCHANGED"
        finally:
            for entry in list(base.iterdir()):
                remove_fixture(entry)


def run_mutations():
    """Kill each packet-named mutant with only its focused lock test."""
    source = P.read_text(encoding="utf-8")
    mutants = [
        ("directory_guard_skips_candidate_itself",
         "    return _guard_destination(path, include_candidate=True)",
         "    return _guard_destination(path, include_candidate=False)", directory_root_lock),
        ("provider_home_honors_ambient_temp_root",
         '        root = Path(tempfile.mkdtemp(prefix="tl-provider-home-", dir=base))',
         '        root = Path(tempfile.mkdtemp(prefix="tl-provider-home-", dir=None))',
         provider_home_lock),
        ("provider_cleanup_failure_is_silently_ignored",
         "            _checked_provider_cleanup(root, root_identity)",
         "            shutil.rmtree(root, ignore_errors=True)",
         provider_cleanup_lock),
    ]
    killed = 0
    with tempfile.TemporaryDirectory(prefix="session-credential-mutant-") as td:
        for index, (name, old, new, lock) in enumerate(mutants):
            assert source.count(old) == 1, f"{name} site missing"
            mutant_path = Path(td) / f"session_credentials_{index}.py"
            mutant_path.write_text(source.replace(old, new), encoding="utf-8", newline="\n")
            mutant_spec = importlib.util.spec_from_file_location(
                f"session_credentials_mutant_{index}", mutant_path)
            mutant = importlib.util.module_from_spec(mutant_spec)
            mutant_spec.loader.exec_module(mutant)
            try:
                lock(mutant)
            except (AssertionError, OSError):
                killed += 1
                print(f"PASS {name} (killed 1/1)")
                continue
            raise AssertionError(f"{name} survived")
    print(f"PASS session credential mutations (killed {killed}/{len(mutants)})")


def run():
    directory_root_lock(m)
    provider_home_lock(m)
    provider_cleanup_lock(m)
    expected_repository = P.resolve().parents[2]
    assert m.REPOSITORY_ROOT == expected_repository
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        assert m.codex_home({"CODEX_HOME": str(root / "custom")}) == root / "custom"
        with mock.patch.object(m.Path, "home", return_value=root):
            assert m.codex_home({}) == root / ".codex"

        auth = json.dumps({"tokens": {"access_token": "private"}}).encode()
        encoded = base64.b64encode(auth).decode()
        result = m.materialize_codex(env={"CODEX_AUTH_JSON": encoded,
                                          "CODEX_HOME": str(root / "codex")})
        target = root / "codex" / "auth.json"
        if os.name == "nt":
            assert result == {"status": "not_measured", "reason": "write_failed"}
            assert not target.exists(), "Windows pathname fallback wrote a secret"
        else:
            assert result["status"] == "passed" and target.read_bytes() == auth
            assert stat.S_IMODE(target.stat().st_mode) == 0o600 and "private" not in repr(result)
        blocked_codex_home = expected_repository / "docs" / ".blocked-codex-home"
        blocked_auth = blocked_codex_home / "auth.json"
        assert not blocked_auth.exists()
        with mock.patch.object(m, "_atomic_secret") as writer:
            blocked = m.materialize_codex(env={"CODEX_AUTH_JSON": encoded,
                "CODEX_HOME": str(blocked_codex_home)})
        assert blocked == {"status": "rejected",
                           "reason": "secret_destination_in_repository"}
        writer.assert_not_called()
        assert not blocked_auth.exists()
        with mock.patch.object(m, "secret_destination", side_effect=OSError("lookup failed")):
            unresolved = m.materialize_codex(env={"CODEX_AUTH_JSON": encoded,
                                                  "CODEX_HOME": str(root / "unresolved")})
        assert unresolved == {"status": "not_measured", "reason": "write_failed"}
        assert m.materialize_codex(env={})["status"] == "missing"
        malformed = m.materialize_codex(env={"CODEX_AUTH_JSON": "!"})
        assert malformed["status"] == ("not_measured" if os.name == "nt" else "rejected")
        no_tokens = base64.b64encode(b'{"not_tokens":{}}').decode()
        no_tokens_result = m.materialize_codex(env={"CODEX_AUTH_JSON": no_tokens,
                                        "CODEX_HOME": str(root / "no-tokens")})
        if os.name == "nt":
            assert no_tokens_result == {"status": "not_measured", "reason": "write_failed"}
        else:
            assert no_tokens_result == {
                "status": "rejected", "reason": "malformed_CODEX_AUTH_JSON"}
        assert not (root / "no-tokens" / "auth.json").exists()

        if os.name != "nt":
            # A newer timestamp on malformed/stale disk state is not authority:
            # only a complete credential document may suppress materialization.
            stale_home = root / "stale-invalid"
            stale_home.mkdir()
            stale_target = stale_home / "auth.json"
            stale_target.write_text(json.dumps({
                "tokens": {}, "last_refresh": "2099-01-01T00:00:00Z"}),
                encoding="utf-8")
            fresh = json.dumps({
                "tokens": {"access_token": "fresh"},
                "last_refresh": "2026-01-01T00:00:00Z"}).encode()
            stale_result = m.materialize_codex(env={
                "CODEX_AUTH_JSON": base64.b64encode(fresh).decode(),
                "CODEX_HOME": str(stale_home)})
            assert stale_result["status"] == "passed" and stale_result["changed"] is True
            assert stale_target.read_bytes() == fresh

        # Public materialization must fail closed before a caller-controlled
        # CODEX_HOME can place auth.json anywhere in this checkout.
        repo = expected_repository
        with tempfile.TemporaryDirectory(prefix="credential-direct-", dir=repo) as rd:
            repo_home = Path(rd) / ".codex"
            result = m.materialize_codex(env={"CODEX_AUTH_JSON": encoded,
                                                "CODEX_HOME": str(repo_home)})
            assert result == {"status": "rejected", "reason": "secret_destination_in_repository"}
            assert not (repo_home / "auth.json").exists()

        # Resolving only the final filename is insufficient: an innocent-looking
        # external parent can itself be a symlink back into the checkout.
        if os.name != "nt":
            with tempfile.TemporaryDirectory(prefix="credential-linked-", dir=repo) as rd:
                repo_slot = Path(rd)
                linked_parent = root / "linked-parent"
                linked_parent.symlink_to(repo_slot, target_is_directory=True)
                linked_home = linked_parent / ".codex"
                result = m.materialize_codex(env={"CODEX_AUTH_JSON": encoded,
                                                    "CODEX_HOME": str(linked_home)})
                assert result == {"status": "rejected", "reason": "secret_destination_in_repository"}
                assert not (repo_slot / ".codex" / "auth.json").exists()

        direct_output = expected_repository / "docs" / ".blocked-claude-token"
        assert not direct_output.exists()
        with mock.patch.object(m.subprocess, "Popen", side_effect=OSError("must not spawn")) as popen:
            blocked = m.capture_claude(direct_output, timeout=1, env={},
                input_stream=io.StringIO(), output_stream=io.StringIO())
        assert blocked == {"status": "rejected",
                           "reason": "secret_destination_in_repository"}
        popen.assert_not_called()
        assert not direct_output.exists()

        with mock.patch.object(m, "secret_destination", side_effect=OSError("lookup failed")), \
             mock.patch.object(m.subprocess, "Popen") as popen:
            unresolved = m.capture_claude(root / "unresolved-claude", timeout=1, env={},
                input_stream=io.StringIO(), output_stream=io.StringIO())
        assert unresolved == {"status": "not_measured", "reason": "write_failed"}
        popen.assert_not_called()

        if os.name != "nt":
            repo_link = root / "repo-parent-link"
            repo_link.symlink_to(expected_repository, target_is_directory=True)
            linked_output = repo_link / "docs" / ".blocked-parent-token"
            with mock.patch.object(m.subprocess, "Popen", side_effect=OSError("must not spawn")) as popen:
                blocked = m.capture_claude(linked_output, timeout=1, env={},
                    input_stream=io.StringIO(), output_stream=io.StringIO())
            assert blocked == {"status": "rejected",
                               "reason": "secret_destination_in_repository"}
            popen.assert_not_called()
            assert not linked_output.exists()
            atomic_linked_output = repo_link / "AGENTS.md" / "auth.json"
            try:
                m._atomic_secret(atomic_linked_output, b"not-a-secret")
                assert False
            except OSError as exc:
                assert str(exc).startswith("refusing repository secret destination:")

        # The value returned by the guard is the write capability.  If a
        # caller-controlled parent link changes immediately after validation,
        # the writer must stay on the canonical directory that was validated.
        if os.name != "nt":
            safe_slot = root / "safe-slot"; safe_slot.mkdir()
            with tempfile.TemporaryDirectory(prefix="credential-race-", dir=repo) as rd:
                repo_slot = Path(rd)
                moving_parent = root / "moving-parent"
                moving_parent.symlink_to(safe_slot, target_is_directory=True)
                original_guard = m.secret_destination

                def validate_then_swap(path):
                    canonical = original_guard(path)
                    if Path(path) == moving_parent / "auth.json":
                        moving_parent.unlink()
                        moving_parent.symlink_to(repo_slot, target_is_directory=True)
                    return canonical

                with mock.patch.object(m, "secret_destination", side_effect=validate_then_swap):
                    m._atomic_secret(moving_parent / "auth.json", b"FIXTURE_ONLY")
                assert (safe_slot / "auth.json").read_bytes() == b"FIXTURE_ONLY"
                assert not (repo_slot / "auth.json").exists(), \
                    "post-validation parent swap redirected secret into repository"

            # Python 3.14 does not advertise working os.replace(dir_fd=...)
            # support in os.supports_dir_fd.  The writer must call the primitive
            # and fail only if that actual call is unsupported.
            advertised = root / "supports-registry" / "auth.json"
            with mock.patch.object(m.os, "supports_dir_fd", set()):
                m._atomic_secret(advertised, b"FIXTURE_ONLY")
            assert advertised.read_bytes() == b"FIXTURE_ONLY"

            # Swap an ancestor of the canonical path after path preflight but
            # before open.  Validation must classify the directory actually
            # opened, not the name that was checked earlier.
            ancestor = root / "ancestor"; (ancestor / "parent").mkdir(parents=True)
            moved_ancestor = root / "ancestor-before-swap"
            with tempfile.TemporaryDirectory(prefix="credential-ancestor-", dir=repo) as rd:
                repo_parent = Path(rd) / "parent"; repo_parent.mkdir()
                original_guard = m.secret_destination
                def swap_ancestor(path):
                    canonical = original_guard(path)
                    ancestor.rename(moved_ancestor)
                    ancestor.symlink_to(Path(rd), target_is_directory=True)
                    return canonical
                with mock.patch.object(m, "secret_destination", side_effect=swap_ancestor):
                    try:
                        m._atomic_secret(ancestor / "parent" / "auth.json", b"FIXTURE_ONLY")
                        assert False, "actual opened repository parent was trusted"
                    except m.UnsafeSecretDestination:
                        pass
                assert not (repo_parent / "auth.json").exists()

            # Swap the parent name only after its descriptor has passed the
            # ancestry walk.  All remaining operations must stay on that fd.
            held_parent = root / "held-parent"; held_parent.mkdir()
            moved_parent = root / "held-parent-opened"
            with tempfile.TemporaryDirectory(prefix="credential-parent-", dir=repo) as rd:
                original_validate = m._validate_parent_capability
                swapped = False
                def validate_then_swap(directory_fd):
                    nonlocal swapped
                    original_validate(directory_fd)
                    if not swapped:
                        swapped = True
                        held_parent.rename(moved_parent)
                        held_parent.symlink_to(Path(rd), target_is_directory=True)
                with mock.patch.object(m, "_validate_parent_capability",
                                       side_effect=validate_then_swap):
                    m._atomic_secret(held_parent / "auth.json", b"FIXTURE_ONLY")
                assert (moved_parent / "auth.json").read_bytes() == b"FIXTURE_ONLY"
                assert not (Path(rd) / "auth.json").exists()

            # Threat-model decision: a concurrent actor that can REPARENT the
            # already-open directory object is not swapping the pathname to a
            # different target.  The capability deliberately remains bound to
            # the same inode, so moving that inode under a repository also
            # moves the eventual write there.  This is outside the supported
            # pathname-race boundary and must stay explicit in the docs.
            decision_repo = root / "reparent-repository"
            (decision_repo / ".git").mkdir(parents=True)
            reparented = root / "opened-parent-reparented"; reparented.mkdir()
            moved_under_repo = decision_repo / "same-opened-directory"
            original_validate = m._validate_parent_capability
            def validate_then_reparent(directory_fd):
                original_validate(directory_fd)
                reparented.rename(moved_under_repo)
            with mock.patch.object(m, "_validate_parent_capability",
                                   side_effect=validate_then_reparent):
                m._atomic_secret(reparented / "auth.json", b"FIXTURE_ONLY")
            assert (moved_under_repo / "auth.json").read_bytes() == b"FIXTURE_ONLY"
            assert not (reparented / "auth.json").exists()

            # A target symlink created at the last instant is replaced as a
            # directory entry; it is never followed to the repository victim.
            target_parent = root / "target-parent"; target_parent.mkdir()
            with tempfile.TemporaryDirectory(prefix="credential-target-", dir=repo) as rd:
                victim = Path(rd) / "victim"; victim.write_bytes(b"UNCHANGED")
                target_path = target_parent / "auth.json"
                original_replace = m.os.replace
                def install_target_link(src, dst, **kwargs):
                    target_path.symlink_to(victim)
                    return original_replace(src, dst, **kwargs)
                with mock.patch.object(m.os, "replace", side_effect=install_target_link):
                    m._atomic_secret(target_path, b"FIXTURE_ONLY")
                assert victim.read_bytes() == b"UNCHANGED"
                assert target_path.read_bytes() == b"FIXTURE_ONLY"
                assert not target_path.is_symlink()

            # Mutation witness: deleting the actual-capability ancestry check
            # makes the ancestor attack above write into the repository.  This
            # proves the race case is sensitive to the control it claims.
            mutant_alias = root / "mutant-parent"; (mutant_alias / "nested").mkdir(parents=True)
            mutant_moved = root / "mutant-parent-before-swap"
            mutant_repo = root / "mutant-repo"; (mutant_repo / ".git").mkdir(parents=True)
            (mutant_repo / "nested").mkdir()
            original_guard = m.secret_destination
            def mutant_swap(path):
                canonical = original_guard(path)
                mutant_alias.rename(mutant_moved)
                mutant_alias.symlink_to(mutant_repo, target_is_directory=True)
                return canonical
            with mock.patch.object(m, "secret_destination", side_effect=mutant_swap), \
                 mock.patch.object(m, "_validate_parent_capability", return_value=None):
                m._atomic_secret(mutant_alias / "nested" / "auth.json", b"FIXTURE_ONLY")
            assert (mutant_repo / "nested" / "auth.json").read_bytes() == b"FIXTURE_ONLY", \
                "mutation witness did not reach the vulnerable behavior"

        # Bare repositories are repositories too; there is no `.git` entry to
        # save a worktree-only boundary check.
        bare = root / "bare.git"
        (bare / "objects").mkdir(parents=True); (bare / "refs").mkdir()
        (bare / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        (bare / "config").write_text("[core]\n\tbare = true\n", encoding="utf-8")
        try:
            m._atomic_secret(bare / "credential", b"FIXTURE_ONLY")
            assert False, "bare repository destination accepted"
        except m.UnsafeSecretDestination:
            pass

        if os.name == "nt":
            # Windows stdlib has no handle-relative create+rename primitive.
            # The contract is an early, side-effect-free refusal: never regress
            # to a held handle followed by pathname mkstemp/os.replace.
            safe = root / "windows-safe" / "auth.json"
            try:
                m._atomic_secret(safe, b"FIXTURE_ONLY")
                assert False, "Windows pathname fallback became reachable"
            except OSError as exc:
                assert "handle-relative" in str(exc)
            assert not safe.exists()

            with mock.patch.object(m.subprocess, "Popen") as popen:
                refused = m.capture_claude(root / "windows-claude.token", timeout=1,
                    env={}, input_stream=io.StringIO(), output_stream=io.StringIO())
            assert refused == {"status": "not_measured", "reason": "write_failed"}
            popen.assert_not_called()

            # A junction is a directory reparse point.  Both an already-hostile
            # parent and a post-preflight swap remain unable to create bytes.
            junction = root / "repo-junction"
            made = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(repo)],
                stdin=subprocess.DEVNULL, capture_output=True).returncode == 0
            if made:
                blocked = m.materialize_codex(env={"CODEX_AUTH_JSON": encoded,
                    "CODEX_HOME": str(junction / ".codex")})
                assert blocked["status"] == "rejected"
                assert not (repo / ".codex" / "auth.json").exists()

                safe_parent = root / "swap-parent"; safe_parent.mkdir()
                moved_parent = root / "swap-parent-opened"
                original_guard = m.secret_destination
                def swap_to_junction(path):
                    canonical = original_guard(path)
                    safe_parent.rename(moved_parent)
                    made_swap = subprocess.run(
                        ["cmd.exe", "/d", "/c", "mklink", "/J",
                         str(safe_parent), str(repo)], stdin=subprocess.DEVNULL,
                        capture_output=True).returncode == 0
                    assert made_swap
                    return canonical
                with mock.patch.object(m, "secret_destination", side_effect=swap_to_junction):
                    try:
                        m._atomic_secret(safe_parent / "auth.json", b"FIXTURE_ONLY")
                        assert False
                    except OSError:
                        pass
                assert not (repo / "auth.json").exists()
            print("PASS session_credentials_test (Windows fail-closed)")
            return

        # An actual child sees a TTY, displays an interactive prompt, consumes input,
        # and emits the credential split over writes.  The parent must stream the
        # prompt while never forwarding the credential.
        bindir = root / "bin"; bindir.mkdir()
        fake = bindir / "claude"
        fake.write_text("""#!/usr/bin/env python3
import json,os,sys,time
assert os.isatty(0) and os.isatty(1) and os.isatty(2)
open(os.path.join(os.path.dirname(__file__), 'setup-env.json'), 'w').write(json.dumps(dict(os.environ)))
os.write(1,b'Confirm setup? ')
if not sys.stdin.readline(): raise SystemExit(2)
os.write(1,b'sk-ant-oat01-' + b'A'*180); time.sleep(.02)
os.write(1,b'A'*180 + b'\\n')
""", encoding="utf-8")
        fake.chmod(0o755)
        out, displayed = root / "claude.token", io.StringIO()
        read_fd, write_fd = os.pipe(); os.write(write_fd, b"yes\n"); os.close(write_fd)
        with os.fdopen(read_fd) as user_input:
            result = m.capture_claude(out, timeout=5,
                env={"PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}",
                     "CODEX_AUTH_JSON": "CODEX_CANARY",
                     "CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CANARY",
                     "GITHUB_PAT": "GH_CANARY", "TL_MASTER_KEY": "TL_CANARY",
                     "ANTHROPIC_API_KEY": "VENDOR_CANARY"},
                input_stream=user_input, output_stream=displayed)
        assert result["status"] == "passed" and "sk-ant" not in repr(result)
        assert "Confirm setup?" in displayed.getvalue()
        assert "sk-ant" not in displayed.getvalue() and "A"*20 not in displayed.getvalue()
        assert "[REDACTED]" in displayed.getvalue()
        assert stat.S_IMODE(out.stat().st_mode) == 0o600

        # A parent can be swapped into the repository after the early preflight.
        # The use-time guard must still classify that policy refusal as rejected.
        raced_out, raced_display = root / "raced-claude.token", io.StringIO()
        read_fd, write_fd = os.pipe(); os.write(write_fd, b"yes\n"); os.close(write_fd)
        with mock.patch.object(m, "_atomic_secret",
                               side_effect=m.UnsafeSecretDestination("swapped parent")), \
             os.fdopen(read_fd) as user_input:
            raced = m.capture_claude(raced_out, timeout=5,
                env={"PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}"},
                input_stream=user_input, output_stream=raced_display)
        assert raced == {"status": "rejected", "reason": "secret_destination_in_repository"}
        assert not raced_out.exists()
        assert "sk-ant" not in raced_display.getvalue() and "A"*20 not in raced_display.getvalue()

        with tempfile.TemporaryDirectory(prefix="claude-capture-", dir=repo) as rd:
            repo_output, rejected_display = Path(rd) / "claude.token", io.StringIO()
            read_fd, write_fd = os.pipe(); os.write(write_fd, b"yes\n"); os.close(write_fd)
            with os.fdopen(read_fd) as user_input:
                result = m.capture_claude(repo_output, timeout=5,
                    env={"PATH": f"{bindir}{os.pathsep}{os.environ['PATH']}"},
                    input_stream=user_input, output_stream=rejected_display)
            assert result == {"status": "rejected", "reason": "secret_destination_in_repository"}
            assert not repo_output.exists()
            assert "sk-ant" not in rejected_display.getvalue()

        setup_env = json.loads((bindir / "setup-env.json").read_text())
        assert "PATH" in setup_env
        assert not set(m.SECRET_ENV) & set(setup_env)
        assert not any("CANARY" in value for value in setup_env.values())
        link = root / "link"; link.symlink_to(out)
        try: m._atomic_secret(link, b"x"); assert False
        except OSError: pass

        seen = []
        def fake_run(cmd, **kw):
            seen.append((cmd, kw)); return mock.Mock(returncode=0, stdout="", stderr="")
        with mock.patch.object(m.subprocess, "run", side_effect=fake_run):
            result = m.github_probe("o/r", env={"GITHUB_PAT": "GH_CANARY",
                "CODEX_AUTH_JSON": "CODEX_CANARY", "CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CANARY",
                "TL_MASTER_KEY": "TL_CANARY", "GITHUB_TOKEN": "OTHER_GH_CANARY",
                "PATH": "/bin", "X": "1"})
        assert result["status"] == "passed" and len(seen) == 2
        assert all("CANARY" not in repr(x[0])
                   and x[1]["env"].get("PATH") == "/bin"
                   and x[1]["env"].get("GH_TOKEN") == "GH_CANARY"
                   and set(x[1]["env"]) == {"PATH", "HOME", "XDG_CONFIG_HOME",
                                              "XDG_CACHE_HOME", "XDG_DATA_HOME",
                                              "XDG_STATE_HOME", "TMPDIR", "TMP", "TEMP",
                                              "GH_TOKEN"}
                   for x in seen)
        for code in (401, 403, 404):
            denied = mock.Mock(returncode=1,
                stdout=f"HTTP/2 {code}\nX-GitHub-Request-Id: FIXTURE\n", stderr="")
            with mock.patch.object(m.subprocess, "run", return_value=denied):
                assert m.github_probe("o/r", env={"GITHUB_PAT": "S"})["status"] == "rejected"
        proxy_403 = mock.Mock(returncode=1, stdout="HTTP/1.1 403 Forbidden\n", stderr="")
        with mock.patch.object(m.subprocess, "run", return_value=proxy_403):
            assert m.github_probe("o/r", env={"GITHUB_PAT": "S"})["status"] == "network_error"
        assert m.github_probe("o/r", env={})["status"] == "missing"

        marker = "TRALUAT-CLAUDE-CREDENTIAL-OK"
        good = mock.Mock(returncode=0, stdout=marker + "\n", stderr="")
        with mock.patch.object(m.subprocess, "run", return_value=good) as run_child:
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CANARY",
                "CODEX_AUTH_JSON": "CODEX_CANARY", "GITHUB_PAT": "GH_CANARY",
                "TL_MASTER_KEY": "TL_CANARY", "ANTHROPIC_API_KEY": "VENDOR_CANARY",
                "HOME": "/home/test"})["status"] == "passed"
        command, kwargs = run_child.call_args
        assert command[0][1] == "-p" and kwargs["stdin"] is m.subprocess.DEVNULL
        assert "CANARY" not in repr(command)
        assert kwargs["env"].get("CLAUDE_CODE_OAUTH_TOKEN") == "CLAUDE_CANARY"
        assert kwargs["env"]["HOME"] != "/home/test"
        assert set(kwargs["env"]) == {"HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
                                      "XDG_DATA_HOME", "XDG_STATE_HOME",
                                      "TMPDIR", "TMP", "TEMP",
                                      "CLAUDE_CODE_OAUTH_TOKEN"}
        no_marker = mock.Mock(returncode=0, stdout="done\n", stderr="")
        with mock.patch.object(m.subprocess, "run", return_value=no_marker):
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S"})["status"] == "rejected"
        refused = mock.Mock(returncode=1, stdout="", stderr="401 unauthorized")
        with mock.patch.object(m.subprocess, "run", return_value=refused):
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S"})["status"] == "rejected"
        with mock.patch.object(m.subprocess, "run", side_effect=m.subprocess.TimeoutExpired("claude", 1)):
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S"})["status"] == "not_measured"

        with mock.patch.object(m.subprocess, "run") as run_child:
            missing_file = m.tl_bootstrap("cowork", None, env={
                "TL_MASTER_KEY": "TL_CANARY", "TMPDIR": "/tmp/test"})
        assert missing_file == {"status": "missing", "reason": "secrets_file"}
        run_child.assert_not_called()

        for argv, target in ((["tl-bootstrap", "--env", "cowork"], "tl_bootstrap"),
                             (["bootstrap", "--env", "cowork"], "bootstrap_session")):
            with mock.patch.object(m, target, side_effect=AssertionError("must not dispatch")) as dispatch, \
                 mock.patch.object(m.sys, "stdout", io.StringIO()), \
                 mock.patch.object(m.sys, "stderr", io.StringIO()):
                try:
                    m.main(argv)
                    assert False
                except SystemExit as exc:
                    assert exc.code == 2
            dispatch.assert_not_called()

        secrets_file = root / "s.enc"
        safe_home = root / "safe-home"; safe_home.mkdir()
        safe_xdg = root / "safe-xdg"; safe_xdg.mkdir()
        safe_tmp = root / "safe-tmp"; safe_tmp.mkdir()

        # The encrypted input and every delegated storage root are part of the
        # same repository boundary.  Refusal must happen before TL is spawned.
        with tempfile.TemporaryDirectory(prefix="tl-boundary-", dir=repo) as rd:
            repo_slot = Path(rd)
            unsafe_cases = [
                (repo_slot / "s.enc", {"HOME": str(safe_home)}),
                (secrets_file, {"HOME": str(repo_slot)}),
                (secrets_file, {"HOME": str(safe_home),
                                "XDG_CONFIG_HOME": str(repo_slot / "xdg")}),
                (secrets_file, {"HOME": str(safe_home),
                                "TMPDIR": str(repo_slot / "tmp")}),
            ]
            linked_bundle_parent = root / "tl-repo-link"
            if os.name != "nt":
                linked_bundle_parent.symlink_to(repo_slot, target_is_directory=True)
                unsafe_cases.append((linked_bundle_parent / "linked.enc",
                                     {"HOME": str(safe_home)}))
            for bundle, extra_env in unsafe_cases:
                with mock.patch.object(m.subprocess, "run") as run_child:
                    rejected = m.tl_bootstrap("cowork", bundle, env={
                        "TL_MASTER_KEY": "TL_CANARY", **extra_env})
                assert rejected["status"] == "rejected", (bundle, extra_env, rejected)
                run_child.assert_not_called()

        hostile = root / "hostile"; (hostile / "scripts").mkdir(parents=True)
        hostile_marker = hostile / "fake-tl-ran"
        (hostile / "scripts" / "tl.py").write_text(
            f"from pathlib import Path\nPath({str(hostile_marker)!r}).write_text('ran')\n",
            encoding="utf-8")
        relative_secrets = Path(os.path.relpath(secrets_file, hostile))
        previous_cwd = Path.cwd()
        try:
            os.chdir(hostile)
            with mock.patch.object(m.subprocess, "run", return_value=mock.Mock(returncode=0)) as run_child:
                result = m.tl_bootstrap("cowork", relative_secrets, env={
                    "TL_MASTER_KEY": "TL_CANARY", "CODEX_AUTH_JSON": "CODEX_CANARY",
                    "CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CANARY", "GITHUB_PAT": "GH_CANARY",
                    "OPENAI_API_KEY": "VENDOR_CANARY", "HOME": str(safe_home),
                    "XDG_CONFIG_HOME": str(safe_xdg), "TMPDIR": str(safe_tmp)})
        finally:
            os.chdir(previous_cwd)
        assert result["status"] == "passed"
        child_argv = run_child.call_args.args[0]
        assert Path(child_argv[1]).resolve() == expected_repository / "scripts" / "tl.py"
        assert child_argv[-2:] == ["--secrets-file", str(secrets_file.resolve())]
        assert run_child.call_args.kwargs["cwd"] == expected_repository
        assert run_child.call_args.kwargs["env"] == {
            "HOME": str(safe_home.resolve()),
            "XDG_CONFIG_HOME": str(safe_xdg.resolve()),
            "TMPDIR": str(safe_tmp.resolve()),
            "TL_MASTER_KEY": "TL_CANARY"}
        assert not hostile_marker.exists()

        calls = []
        def component(name, status="passed"):
            def f(*args, **kwargs): calls.append(name); return {"status": status}
            return f
        with mock.patch.object(m, "materialize_codex", side_effect=component("codex")), \
             mock.patch.object(m, "claude_probe", side_effect=component("claude")), \
             mock.patch.object(m, "github_probe", side_effect=component("github")), \
             mock.patch.object(m, "tl_bootstrap", side_effect=component("tl")):
            missing_combined = m.bootstrap_session("o/r", "cowork", None, None, env={})
        assert missing_combined == {"status": "missing", "reason": "secrets_file"}
        assert calls == []
        with mock.patch.object(m, "materialize_codex", side_effect=component("codex")), \
             mock.patch.object(m, "claude_probe", side_effect=component("claude")), \
             mock.patch.object(m, "github_probe", side_effect=component("github")), \
             mock.patch.object(m, "tl_bootstrap", side_effect=component("tl")):
            combined = m.bootstrap_session("o/r", "cowork", root / "secrets.enc", None, env={})
        assert combined["status"] == "passed" and calls == ["codex", "claude", "github", "tl"]
        assert set(combined["components"]) == {"codex", "claude", "github", "tl"}
        # Both public orchestration commands reject the incomplete invocation
        # at argument parsing, before any provider component can run.
        for argv in (["tl-bootstrap", "--env", "cowork"],
                     ["bootstrap", "--env", "cowork"]):
            try:
                m.main(argv)
            except SystemExit as exc:
                assert exc.code == 2
            else:
                raise AssertionError(f"missing --secrets-file accepted: {argv}")
    print("PASS session_credentials_test")


if __name__ == "__main__":
    if sys.argv[1:] == ["--dot-bien"]:
        run_mutations()
    elif sys.argv[1:]:
        raise SystemExit("usage: session_credentials_test.py [--dot-bien]")
    else:
        run()
