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


def _fixture_bound(module, name):
    """Bind a real inert absolute executable for classifier-only tests."""
    executable = Path(sys.executable).resolve(strict=True)
    identity = module._provider_file_identity(executable)
    return module._BoundProviderExecutable(
        provider=name,
        kind="direct",
        executable=executable,
        launch_support=(),
        identities=((executable, identity),),
        sanitized_path=str(executable.parent),
    )


def _safe_executable_directory():
    """Allocate outside both this repository and the process temp tree."""
    return tempfile.TemporaryDirectory(
        prefix="wp433-provider-executable-", dir=P.resolve().parents[3])


def _write_executable(path: Path, body: str = "#!/bin/sh\nexit 0\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8", newline="\n")
    path.chmod(0o755)
    return path


def provider_executable_lock(module):
    """Provider credentials cross only one absolute, identity-bound executable."""
    original_repository = module.REPOSITORY_ROOT
    with _safe_executable_directory() as safe_raw:
        safe = Path(safe_raw)
        module.REPOSITORY_ROOT = P.resolve().parents[2]
        try:
            if os.name == "nt":
                node = _write_executable(safe / "node.exe", "inert-node-fixture\n")
                cli = _write_executable(
                    safe / "node_modules" / "claude" / "cli.js",
                    "inert-cli-fixture\n")
                npm_body = ('@ECHO off\n"%dp0%\\node.exe" '
                            '"%dp0%\\node_modules\\claude\\cli.js" %*\n')
                claude = _write_executable(safe / "claude.cmd", npm_body)
                gh = _write_executable(safe / "gh.exe", "fixture\n")
                path_env = str(safe)
                common = {"PATH": path_env, "PATHEXT": ".EXE;.CMD"}
            else:
                real = _write_executable(safe / "claude-real")
                claude = safe / "claude"
                claude.symlink_to(real)
                gh = _write_executable(safe / "gh")
                common = {"PATH": str(safe)}

            marker = "TRALUAT-CLAUDE-CREDENTIAL-OK"
            completed = mock.Mock(returncode=0, stdout=marker + "\n", stderr="")
            with mock.patch.object(module.subprocess, "run", return_value=completed) as child:
                result = module.claude_probe(env={
                    **common, "CLAUDE_CODE_OAUTH_TOKEN": "INERT_FIXTURE"})
            assert result["status"] == "passed", result
            argv = child.call_args.args[0]
            assert Path(argv[0]).is_absolute(), argv
            assert argv[0].lower() != "claude", argv
            assert "INERT_FIXTURE" not in repr(argv)
            if os.name == "nt":
                assert Path(argv[0]).resolve() == node.resolve(), argv
                assert Path(argv[1]).resolve() == cli.resolve(), argv
                assert str(claude.resolve()).lower() not in repr(argv).lower(), argv
            else:
                assert Path(argv[0]).is_absolute(), argv
                assert Path(argv[-3]).resolve() == real.resolve(), argv

            ok = mock.Mock(returncode=0, stdout="", stderr="")
            with mock.patch.object(module.subprocess, "run", return_value=ok) as child:
                result = module.github_probe(
                    "o/r", env={**common, "GITHUB_PAT": "INERT_FIXTURE"})
            assert result["status"] == "passed", result
            assert child.call_count == 2
            assert all(Path(call.args[0][0]).is_absolute()
                       and call.args[0][0].lower() != "gh"
                       and "INERT_FIXTURE" not in repr(call.args[0])
                       for call in child.call_args_list)

            # Invalid discovery roots are rejected before the credential key
            # is even read.  A mapping that explodes on that read proves order.
            class CredentialTripwire(dict):
                def get(self, key, default=None):
                    if key in ("CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_PAT"):
                        raise AssertionError("credential read before executable validation")
                    return super().get(key, default)

            # The interpreter/script is launch authority too.  Replacing a
            # bound support file must fail before the credential-bearing child.
            if os.name == "nt":
                support_common = common
                support_bound = module._bind_provider_executable(
                    "claude", support_common)
                assert support_bound.kind == "npm-cmd"
                assert len(support_bound.launch_support) == 2
                support_target = support_bound.launch_support[0]
                support_target.unlink()
                _write_executable(support_target, "malicious-node-fixture\n")
            else:
                _write_executable(real, "#!/usr/bin/env node\n")
                support_target = _write_executable(safe / "node")
                support_common = {"PATH": str(safe)}
                support_bound = module._bind_provider_executable(
                    "claude", support_common)
                assert support_bound.kind == "posix-script"
                assert len(support_bound.launch_support) == 1
                support_argv = module._provider_argv(
                    support_bound, ["--inert-fixture"])
                assert Path(support_argv[0]).resolve() == support_target.resolve()
                assert Path(support_argv[1]).resolve() == real.resolve()
                assert support_argv[2:] == ["--inert-fixture"]
                support_target.unlink()
                _write_executable(support_target, "#!/bin/sh\nexit 9\n")
            with mock.patch.object(
                    module, "_bind_provider_executable",
                    return_value=support_bound), \
                 mock.patch.object(module.subprocess, "run") as child:
                support_changed = module.claude_probe(env={
                    **support_common,
                    "CLAUDE_CODE_OAUTH_TOKEN": "INERT_FIXTURE"})
            assert support_changed["status"] == "not_measured", support_changed
            child.assert_not_called()
            if os.name == "nt":
                _write_executable(node, "inert-node-fixture\n")
            else:
                _write_executable(real)

                # Two PATH-resolved interpreters are ambiguity; the credential
                # key tripwire proves neither unbound node can receive it.
                _write_executable(real, "#!/usr/bin/env node\n")
                malicious = safe / "malicious"; malicious.mkdir()
                _write_executable(malicious / "node", "#!/bin/sh\nexit 9\n")
                ambiguous_support = CredentialTripwire(
                    PATH=os.pathsep.join((str(safe), str(malicious))))
                with mock.patch.object(module.subprocess, "run") as child:
                    assert module.claude_probe(
                        env=ambiguous_support)["status"] == "not_measured"
                child.assert_not_called()
                _write_executable(real)

            invalid_sources = (
                CredentialTripwire(PATH=""),
                CredentialTripwire(PATH="."),
                CredentialTripwire(PATH=str(module.REPOSITORY_ROOT)),
            )
            with mock.patch.object(module.subprocess, "run") as child:
                for source in invalid_sources:
                    assert module.claude_probe(env=source)["status"] == "not_measured"
                    assert module.github_probe("o/r", env=source)["status"] == "not_measured"
            child.assert_not_called()

            # PATH is an authority declaration, not shell syntax.  In
            # particular, a raw relative tilde must not be expanded through
            # the launcher's ambient HOME before the credential tripwire.
            tilde_home = safe / "tilde-home"
            tilde_bin = tilde_home / "bin"
            _write_executable(
                tilde_bin / ("claude.exe" if os.name == "nt" else "claude"))
            tilde_source = CredentialTripwire(
                PATH=str(Path("~") / "bin"),
                **({"PATHEXT": ".EXE"} if os.name == "nt" else {}))
            with mock.patch.dict(os.environ, {
                    "HOME": str(tilde_home), "USERPROFILE": str(tilde_home)}), \
                 mock.patch.object(module.subprocess, "run") as child:
                result = module.claude_probe(env=tilde_source)
            assert result["status"] == "not_measured", result
            child.assert_not_called()

            with tempfile.TemporaryDirectory(prefix="wp433-provider-temp-") as temp_raw:
                temp_root = Path(temp_raw)
                _write_executable(temp_root / ("claude.cmd" if os.name == "nt" else "claude"))
                temp_source = CredentialTripwire(
                    PATH=str(temp_root), **({"PATHEXT": ".CMD"} if os.name == "nt" else {}))
                with mock.patch.object(module.subprocess, "run") as child:
                    assert module.claude_probe(env=temp_source)["status"] == "not_measured"
                child.assert_not_called()

            # More than one trusted candidate is ambiguity, not PATH priority.
            other = safe / "other"; other.mkdir()
            _write_executable(other / ("claude.exe" if os.name == "nt" else "claude"))
            ambiguous = {**common, "PATH": os.pathsep.join((str(safe), str(other))),
                         "CLAUDE_CODE_OAUTH_TOKEN": "INERT_FIXTURE"}
            with mock.patch.object(module.subprocess, "run") as child:
                assert module.claude_probe(env=ambiguous)["status"] == "not_measured"
            child.assert_not_called()

            # Replacement after binding but before spawn must start no child.
            bound = module._bind_provider_executable("claude", common)
            bound.executable.unlink()
            replacement_body = (npm_body.replace("@ECHO off", "@ECHO off\n@REM upgraded")
                                if os.name == "nt" else "#!/bin/sh\nexit 9\n")
            replacement = _write_executable(bound.executable, replacement_body)
            assert replacement.exists()
            with mock.patch.object(module, "_bind_provider_executable", return_value=bound), \
                 mock.patch.object(module.subprocess, "run") as child:
                changed = module.claude_probe(env={
                    **common, "CLAUDE_CODE_OAUTH_TOKEN": "INERT_FIXTURE"})
            assert changed["status"] == "not_measured", changed
            child.assert_not_called()

            # A separate invocation discovers the replacement as a normal
            # provider upgrade and binds its new identity.
            with mock.patch.object(
                    module.subprocess, "run", return_value=completed) as child:
                upgraded = module.claude_probe(env={
                    **common, "CLAUDE_CODE_OAUTH_TOKEN": "INERT_FIXTURE"})
            assert upgraded["status"] == "passed", upgraded
            child.assert_called_once()
        finally:
            module.REPOSITORY_ROOT = original_repository


def windows_pre313_provider_binding_lock(module):
    """Windows 3.11 can bind provider identity without allocating secret storage."""
    if os.name != "nt":
        print("SKIP windows_pre313_provider_binding_lock (Windows-only behavior)")
        return
    provider_module = sys.modules[module.bind_provider_executable.__module__]
    with _safe_executable_directory() as safe_raw:
        safe = Path(safe_raw)
        executable = _write_executable(safe / "gh.exe", "inert-gh-fixture\n")
        source = {"PATH": str(safe), "PATHEXT": ".EXE"}
        with mock.patch.object(provider_module.sys, "version_info", (3, 11, 9)):
            bound = module.bind_provider_executable(
                "gh", source, repository_root=P.resolve().parents[2])
        assert bound.kind == "direct", bound
        assert bound.executable == executable.resolve(strict=True), bound
        assert bound.identities == ((bound.executable,
                                     module._provider_file_identity(bound.executable)),)


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
                 mock.patch.object(module, "_bind_provider_executable",
                                   side_effect=lambda name, _source:
                                       _fixture_bound(module, name)), \
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


def provider_private_acl_unavailable_lock(module):
    """Unavailable private ACL semantics refuse before allocation or credential child."""
    with mock.patch.object(
            module, "_private_provider_directory_acl_available",
            return_value=False), \
         mock.patch.object(module, "_bind_provider_executable",
                           return_value=_fixture_bound(module, "claude")), \
         mock.patch.object(module.tempfile, "mkdtemp") as allocate, \
         mock.patch.object(module.subprocess, "run") as child:
        result = module.claude_probe(env={
            "PATH": str(Path(sys.executable).resolve().parent),
            "CLAUDE_CODE_OAUTH_TOKEN": "INERT_FIXTURE",
        })
    assert result == {"status": "not_measured",
                      "reason": "provider_storage_unavailable"}, result
    allocate.assert_not_called()
    child.assert_not_called()


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
                 mock.patch.object(module, "_bind_provider_executable",
                                   return_value=_fixture_bound(module, "claude")), \
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
                 mock.patch.object(module, "_bind_provider_executable",
                                   return_value=_fixture_bound(module, "claude")), \
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
                 mock.patch.object(module, "_bind_provider_executable",
                                   return_value=_fixture_bound(module, "claude")), \
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


def missing_parent_capability_lock(module):
    """A missing component cannot become a pathname redirection seam."""
    with tempfile.TemporaryDirectory(prefix="secret-parent-capability-") as td:
        root = Path(td)
        ordinary = root / "ordinary" / "nested" / "auth.json"
        if os.name == "posix":
            module._atomic_secret(ordinary, b"POSITIVE_FIXTURE")
            assert ordinary.read_bytes() == b"POSITIVE_FIXTURE"
            assert stat.S_IMODE(ordinary.stat().st_mode) == 0o600
        else:
            try:
                module._atomic_secret(ordinary, b"POSITIVE_FIXTURE")
                assert False, "Windows writer used a pathname fallback"
            except OSError as exc:
                assert "handle-relative" in str(exc)
            assert not ordinary.exists()
            return

        missing = root / "missing-component"
        external = root / "substituted-external"
        external.mkdir()
        attacked = missing / "nested" / "auth.json"
        original_destination = module.secret_destination

        def substitute_missing_component(path):
            canonical = original_destination(path)
            missing.symlink_to(external, target_is_directory=True)
            return canonical

        with mock.patch.object(
                module, "secret_destination",
                side_effect=substitute_missing_component):
            try:
                module._atomic_secret(attacked, b"RACE_FIXTURE")
                assert False, "missing-parent substitution redirected the writer"
            except OSError:
                pass
        assert not (external / "nested" / "auth.json").exists(), \
            "secret bytes reached the substituted directory"


def secret_write_cleanup_lock(module):
    """Failed writes remove only their exact created inode, never a replacement."""
    if os.name != "posix":
        print("SKIP session_partial_write_forgets_created_identity "
              "(POSIX capability primitive unavailable)")
        return

    class InjectedWriteFailure(OSError):
        pass

    class FaultingFile:
        def __init__(self, fd, stage, failure):
            self.fd = fd
            self.stage = stage
            self.failure = failure

        def __enter__(self):
            return self

        def __exit__(self, _kind, _value, _traceback):
            os.close(self.fd)

        def fileno(self):
            return self.fd

        def write(self, data):
            if self.stage == "partial_write":
                os.write(self.fd, data[:max(1, len(data) // 3)])
                raise self.failure
            os.write(self.fd, data)
            return len(data)

        def flush(self):
            if self.stage == "flush":
                raise self.failure

    def exercise_failure(root, stage, exclusive):
        target = root / f"{stage}-{'exclusive' if exclusive else 'atomic'}.json"
        failure = InjectedWriteFailure(f"fixture-{stage}")
        patches = []
        if stage in ("partial_write", "flush"):
            patches.append(mock.patch.object(
                module.os, "fdopen",
                side_effect=lambda fd, _mode: FaultingFile(fd, stage, failure)))
        elif stage == "chmod":
            patches.append(mock.patch.object(
                module.os, "fchmod", side_effect=failure))
        else:
            real_fsync = module.os.fsync
            calls = 0

            def faulting_fsync(fd):
                nonlocal calls
                calls += 1
                failure_call = 1 if stage == "file_fsync" else 2
                if calls == failure_call:
                    raise failure
                return real_fsync(fd)

            patches.append(mock.patch.object(
                module.os, "fsync", side_effect=faulting_fsync))

        try:
            with patches[0]:
                module._atomic_secret(
                    target, b"INERT_PARTIAL_WRITE_FIXTURE", exclusive=exclusive)
            assert False, f"{stage} failure was swallowed"
        except InjectedWriteFailure as caught:
            assert caught is failure, "cleanup replaced the original exception"

        assert not target.exists(), (stage, exclusive, "credential target survived")
        assert list(root.iterdir()) == [], (stage, exclusive, list(root.iterdir()))

    def exercise_replacement(root, exclusive):
        target = root / ("replacement-exclusive.json" if exclusive
                         else "replacement-atomic.json")
        failure = InjectedWriteFailure("fixture-replacement")

        class ReplacingFile(FaultingFile):
            def write(self, data):
                os.write(self.fd, data)
                entries = list(root.iterdir())
                assert len(entries) == 1, entries
                created = entries[0]
                created.unlink()
                created.write_bytes(b"ATTACKER_REPLACEMENT_FIXTURE")
                raise self.failure

        with mock.patch.object(
                module.os, "fdopen",
                side_effect=lambda fd, _mode: ReplacingFile(
                    fd, "replacement", failure)):
            try:
                module._atomic_secret(
                    target, b"INERT_REPLACED_FIXTURE", exclusive=exclusive)
                assert False, "replacement fixture failure was swallowed"
            except InjectedWriteFailure as caught:
                assert caught is failure, "cleanup replaced the original exception"

        entries = list(root.iterdir())
        assert len(entries) == 1, entries
        assert entries[0].read_bytes() == b"ATTACKER_REPLACEMENT_FIXTURE"
        if not exclusive:
            assert not target.exists(), "atomic temp replacement became final target"

    with tempfile.TemporaryDirectory(prefix="secret-write-cleanup-") as td:
        base = Path(td)
        for exclusive in (False, True):
            for stage in (
                    "chmod", "partial_write", "flush",
                    "file_fsync", "directory_fsync"):
                root = base / f"{stage}-{'x' if exclusive else 'a'}"
                root.mkdir()
                exercise_failure(root, stage, exclusive)
            replacement_root = base / f"replacement-{'x' if exclusive else 'a'}"
            replacement_root.mkdir()
            exercise_replacement(replacement_root, exclusive)

        for exclusive in (False, True):
            positive = base / f"positive-{'x' if exclusive else 'a'}" / "auth.json"
            module._atomic_secret(
                positive, b"INERT_POSITIVE_FIXTURE", exclusive=exclusive)
            assert positive.read_bytes() == b"INERT_POSITIVE_FIXTURE"
            assert stat.S_IMODE(positive.stat().st_mode) == 0o600

        # A directory durability boundary is mandatory.  Filesystems that
        # report EINVAL/ENOTSUP for directory fsync are unsupported for this
        # writer; they are not a successful write with weaker durability.
        unsupported = {errno for errno in (
            getattr(module.errno, "EINVAL", None),
            getattr(module.errno, "ENOTSUP", None),
        ) if errno is not None}
        for error_number in unsupported:
            root = base / f"unsupported-fsync-{error_number}"
            root.mkdir()
            target = root / "auth.json"
            real_fsync = module.os.fsync

            def unsupported_directory_fsync(fd, *, _errno=error_number):
                if stat.S_ISDIR(module.os.fstat(fd).st_mode):
                    raise OSError(_errno, "unsupported directory fsync fixture")
                return real_fsync(fd)

            with mock.patch.object(
                    module.os, "fsync", side_effect=unsupported_directory_fsync):
                try:
                    module._atomic_secret(target, b"INERT_UNSUPPORTED_FIXTURE")
                    assert False, f"directory fsync errno {error_number} was accepted"
                except OSError as caught:
                    assert caught.errno == error_number, caught
            assert not target.exists(), (error_number, target)
            assert list(root.iterdir()) == [], (error_number, list(root.iterdir()))

        # Cleanup is best-effort, but it must never replace the write or
        # durability exception that triggered cleanup.  The parent descriptor
        # close is still attempted and its own failure is secondary.
        root = base / "parent-close-original-precedence"
        root.mkdir()
        target = root / "auth.json"
        primary = InjectedWriteFailure("primary-directory-fsync")
        close_attempts = []
        real_fsync = module.os.fsync
        real_close = module.os.close
        real_open_parent = module._open_parent_capability
        captured_parent = [None]

        def capture_parent(*args, **kwargs):
            fd = real_open_parent(*args, **kwargs)
            captured_parent[0] = fd
            return fd

        def primary_directory_fsync(fd):
            if stat.S_ISDIR(module.os.fstat(fd).st_mode):
                raise primary
            return real_fsync(fd)

        def failing_parent_close(fd):
            is_target_parent = fd == captured_parent[0]
            close_attempts.append((fd, is_target_parent))
            real_close(fd)
            if is_target_parent:
                raise OSError("parent close fixture")

        with mock.patch.object(
                module, "_open_parent_capability", side_effect=capture_parent), \
             mock.patch.object(module.os, "fsync", side_effect=primary_directory_fsync), \
             mock.patch.object(module.os, "close", side_effect=failing_parent_close):
            try:
                module._atomic_secret(target, b"INERT_CLOSE_FIXTURE")
                assert False, "primary durability failure was swallowed"
            except InjectedWriteFailure as caught:
                assert caught is primary, "parent close replaced original exception"
        assert any(is_parent for _, is_parent in close_attempts), close_attempts
        assert not target.exists(), target


def claude_status_lock(module):
    """Claude status is evidence-based, with unknown local failure unmeasured."""
    cases = (
        (mock.Mock(returncode=1, stdout="", stderr="401 unauthorized"), "rejected"),
        (mock.Mock(returncode=1, stdout="", stderr="403 forbidden"), "rejected"),
        (mock.Mock(returncode=1, stdout="", stderr="invalid OAuth token"), "rejected"),
        (mock.Mock(returncode=1, stdout="", stderr="authentication failed: invalid credentials"),
         "rejected"),
        (mock.Mock(returncode=1, stdout="", stderr="model is not available for this account"),
         "rejected"),
        (mock.Mock(returncode=7, stdout="", stderr="connection reset by peer"),
         "network_error"),
        (mock.Mock(returncode=7, stdout="", stderr="local configuration parse failed"),
         "not_measured"),
        (mock.Mock(returncode=7, stdout="", stderr="local network profile is invalid"),
         "not_measured"),
        (mock.Mock(returncode=7, stdout="", stderr="login configuration parse failed"),
         "not_measured"),
        (mock.Mock(returncode=7, stdout="", stderr="OAuth callback configuration is malformed"),
         "not_measured"),
        (mock.Mock(returncode=7, stdout="", stderr="authentication helper crashed locally"),
         "not_measured"),
        (mock.Mock(returncode=7, stdout="", stderr="local cache record 401 is malformed"),
         "not_measured"),
        (mock.Mock(returncode=7, stdout="", stderr="local port 403 is already in use"),
         "not_measured"),
    )
    for completed, expected in cases:
        with mock.patch.object(module, "_bind_provider_executable",
                               return_value=_fixture_bound(module, "claude")), \
             mock.patch.object(module.subprocess, "run", return_value=completed):
            result = module.claude_probe(
                env={"CLAUDE_CODE_OAUTH_TOKEN": "INERT_FIXTURE"})
        assert result["status"] == expected, (completed.stderr, result)

    marker = "TRALUAT-CLAUDE-CREDENTIAL-OK"
    zero_exit_cases = (
        (mock.Mock(returncode=0, stdout="done\n", stderr=""),
         "not_measured", "marker_missing"),
        (mock.Mock(returncode=0, stdout=f"prefix-{marker}-suffix\n", stderr=""),
         "not_measured", "marker_missing"),
        (mock.Mock(returncode=0, stdout="", stderr="invalid OAuth token"),
         "rejected", None),
        (mock.Mock(returncode=0, stdout="", stderr="connection refused"),
         "network_error", None),
        (mock.Mock(returncode=0, stdout=marker + "\n", stderr=""),
         "passed", None),
    )
    for completed, expected, reason in zero_exit_cases:
        with mock.patch.object(module, "_bind_provider_executable",
                               return_value=_fixture_bound(module, "claude")), \
             mock.patch.object(module.subprocess, "run", return_value=completed):
            result = module.claude_probe(
                env={"CLAUDE_CODE_OAUTH_TOKEN": "INERT_FIXTURE"})
        assert result["status"] == expected, (completed.stderr, completed.stdout, result)
        assert result.get("reason") == reason, result


def claude_capture_status_lock(module):
    """setup-token uses the same closed refusal/transport classification."""
    if os.name != "posix":
        print("SKIP claude_capture_unknown_nonzero_becomes_rejected "
              "(POSIX PTY/capability primitive unavailable)")
        return
    cases = (
        (7, "local configuration parse failed", "not_measured"),
        (7, "login configuration parse failed", "not_measured"),
        (7, "OAuth callback configuration is malformed", "not_measured"),
        (7, "authentication helper crashed locally", "not_measured"),
        (7, "local cache record 401 is malformed", "not_measured"),
        (7, "local port 403 is already in use", "not_measured"),
        (7, "invalid OAuth token", "rejected"),
        (7, "connection reset by peer", "network_error"),
        (0, "setup completed without a token", "not_measured"),
    )
    with _safe_executable_directory() as raw, \
         tempfile.TemporaryDirectory(prefix="wp433-capture-output-") as output_raw:
        bindir = Path(raw)
        output_root = Path(output_raw)
        fake = bindir / "claude"
        for index, (returncode, evidence, expected) in enumerate(cases):
            _write_executable(
                fake,
                f"#!{sys.executable}\n"
                "import os\n"
                f"os.write(1, {evidence!r}.encode() + b'\\n')\n"
                f"raise SystemExit({returncode})\n")
            output = output_root / f"capture-{index}.token"
            result = module.capture_claude(
                output, timeout=5, env={"PATH": str(bindir)},
                input_stream=io.StringIO(), output_stream=io.StringIO())
            assert result["status"] == expected, (returncode, evidence, result)
            assert not output.exists(), (returncode, evidence, result)


def github_status_lock(module):
    """GitHub failures require GitHub auth headers or bounded transport proof."""
    passed = mock.Mock(returncode=0, stdout="", stderr="")
    cases = (
        (mock.Mock(returncode=1,
                   stdout="HTTP/2 401\nX-GitHub-Request-Id: FIXTURE\n", stderr=""),
         "rejected"),
        (mock.Mock(returncode=1,
                   stdout="HTTP/2 403\nX-GitHub-Request-Id: FIXTURE\n", stderr=""),
         "rejected"),
        (mock.Mock(returncode=1,
                   stdout="HTTP/2 404\nX-GitHub-Request-Id: FIXTURE\n", stderr=""),
         "rejected"),
        (mock.Mock(returncode=1, stdout="HTTP/1.1 403 Forbidden\n", stderr=""),
         "not_measured"),
        (mock.Mock(
            returncode=1,
            stdout=("HTTP/2 403 Forbidden\r\nServer: fixture\r\n\r\n"
                    "X-GitHub-Request-Id: BODY-SPOOF\r\n"), stderr=""),
         "not_measured"),
        (mock.Mock(returncode=1, stdout="", stderr="connection reset by peer"),
         "network_error"),
        (mock.Mock(returncode=1, stdout="", stderr="local configuration parse failed"),
         "not_measured"),
        (mock.Mock(returncode=1, stdout="", stderr="unknown failure"),
         "not_measured"),
    )
    for failed, expected in cases:
        with mock.patch.object(module, "_bind_provider_executable",
                               return_value=_fixture_bound(module, "gh")), \
             mock.patch.object(module.subprocess, "run",
                               side_effect=(passed, failed)):
            result = module.github_probe("o/r", env={"GITHUB_PAT": "INERT_FIXTURE"})
        assert result["status"] == expected, (failed.stdout, failed.stderr, result)
        assert result["endpoints"]["user"] == "passed"
        assert result["endpoints"]["repos/o/r"] == expected

    # A later proxy response without GitHub headers cannot borrow an earlier
    # GitHub header from a different HTTP block.
    mixed_block = mock.Mock(
        returncode=1,
        stdout=("HTTP/2 200\nX-GitHub-Request-Id: REAL\n\n"
                "HTTP/1.1 403 Forbidden\nServer: proxy\n"), stderr="")
    with mock.patch.object(module, "_bind_provider_executable",
                           return_value=_fixture_bound(module, "gh")), \
         mock.patch.object(module.subprocess, "run",
                           side_effect=(passed, mixed_block)):
        result = module.github_probe("o/r", env={"GITHUB_PAT": "INERT_FIXTURE"})
    assert result["status"] == "not_measured", result

    # Timeout alone proves that this bounded endpoint was not measured.  It
    # does not independently prove a network/transport failure.
    timeout = subprocess.TimeoutExpired(["gh", "api"], 20)
    with mock.patch.object(module, "_bind_provider_executable",
                           return_value=_fixture_bound(module, "gh")), \
         mock.patch.object(module.subprocess, "run",
                           side_effect=(passed, timeout)):
        result = module.github_probe("o/r", env={"GITHUB_PAT": "INERT_FIXTURE"})
    assert result["status"] == "not_measured", result
    assert result["endpoints"] == {
        "user": "passed", "repos/o/r": "not_measured"}, result


def tl_status_lock(module):
    """TL bootstrap preserves the delegated command's closed exit contract."""
    expected_by_rc = {
        0: ("passed", None),
        1: ("not_measured", "degraded"),
        2: ("not_measured", "precondition"),
        3: ("rejected", "credential_or_bundle_rejected"),
        9: ("not_measured", "unclassified_exit"),
    }
    with tempfile.TemporaryDirectory(prefix="tl-status-contract-") as td:
        root = Path(td)
        home = root / "home"
        home.mkdir()
        for returncode, (expected, reason) in expected_by_rc.items():
            completed = mock.Mock(returncode=returncode, stdout="", stderr="")
            with mock.patch.object(
                    module.subprocess, "run", return_value=completed) as child:
                result = module.tl_bootstrap(
                    "cowork", root / "fixture.enc",
                    env={"TL_MASTER_KEY": "INERT_FIXTURE", "HOME": str(home)})
            assert result["status"] == expected, (returncode, result)
            assert result["returncode"] == returncode
            assert result.get("reason") == reason, (returncode, result)
            child.assert_called_once()


def run_mutations():
    """Kill each packet-named mutant with only its focused lock test."""
    source = P.read_text(encoding="utf-8")
    mutants = [
        ("directory_guard_skips_candidate_itself",
         "    return _guard_destination(path, include_candidate=True)",
         "    return _guard_destination(path, include_candidate=False)", directory_root_lock),
        ("provider_home_allocates_without_private_acl",
         "    if not _private_provider_directory_acl_available():\n"
         "        raise OSError(\"private provider directory ACL unavailable\")\n"
         "    base = _trusted_provider_temp_base()",
         "    if False:\n"
         "        raise OSError(\"private provider directory ACL unavailable\")\n"
         "    base = _trusted_provider_temp_base()",
         provider_private_acl_unavailable_lock),
        ("provider_home_honors_ambient_temp_root",
         '        root = Path(tempfile.mkdtemp(prefix="tl-provider-home-", dir=base))',
         '        root = Path(tempfile.mkdtemp(prefix="tl-provider-home-", dir=None))',
         provider_home_lock),
        ("provider_cleanup_failure_is_silently_ignored",
         "            _checked_provider_cleanup(root, root_identity)",
         "            shutil.rmtree(root, ignore_errors=True)",
         provider_cleanup_lock),
        ("provider_probe_uses_ambient_PATH_argv0",
         "                argv = _provider_argv(\n"
         "                    bound, [\"-p\", f\"Print exactly: {marker}\"])\n"
         "                p = subprocess.run(argv,",
         "                argv = [\"claude\", \"-p\", f\"Print exactly: {marker}\"]\n"
         "                p = subprocess.run(argv,",
         provider_executable_lock),
        ("claude_local_login_config_error_becomes_rejected",
         "    if _claude_refusal_evidenced(combined):",
         "    if (_claude_refusal_evidenced(combined) or any(\n"
         "            word in combined for word in\n"
         "            (\"login\", \"oauth\", \"authentication\"))):",
         claude_status_lock),
        ("claude_bare_403_becomes_rejected",
         "    if _claude_refusal_evidenced(combined):",
         "    if (_claude_refusal_evidenced(combined) or any(\n"
         "            word in combined for word in (\"401\", \"403\"))):",
         claude_status_lock),
        ("claude_unknown_nonzero_becomes_network_error",
         "    if _transport_failure_evidenced(combined):\n"
         "        return \"network_error\"\n"
         "    return \"not_measured\"",
         "    if _transport_failure_evidenced(combined):\n"
         "        return \"network_error\"\n"
         "    return \"network_error\"",
         claude_status_lock),
        ("claude_rc0_marker_missing_becomes_rejected",
         "        if status == \"not_measured\":\n"
         "            details[\"reason\"] = \"marker_missing\"\n"
         "        return _result(status, **details)",
         "        if status == \"not_measured\":\n"
         "            return _result(\"rejected\", reason=\"marker_missing\", returncode=0)\n"
         "        return _result(status, **details)",
         claude_status_lock),
        ("github_local_config_error_becomes_network_error",
         "    if _transport_failure_evidenced(combined.lower()):\n"
         "        return \"network_error\"\n"
         "    return \"not_measured\"",
         "    if _transport_failure_evidenced(combined.lower()):\n"
         "        return \"network_error\"\n"
         "    return \"network_error\"",
         github_status_lock),
        ("github_timeout_without_transport_evidence_becomes_network_error",
         '                except subprocess.TimeoutExpired:\n'
         '                    results[endpoint] = "not_measured"',
         '                except subprocess.TimeoutExpired:\n'
         '                    results[endpoint] = "network_error"',
         github_status_lock),
        ("github_body_line_is_accepted_as_response_header",
         '        headers = block[:header_end.start()] if header_end else block',
         '        headers = block',
         github_status_lock),
        ("tl_degraded_rc1_becomes_rejected",
         '        1: ("not_measured", "degraded"),',
         '        1: ("rejected", "credential_or_bundle_rejected"),',
         tl_status_lock),
        ("tl_precondition_rc2_becomes_rejected",
         '        2: ("not_measured", "precondition"),',
         '        2: ("rejected", "credential_or_bundle_rejected"),',
         tl_status_lock),
    ]
    if os.name == "posix":
        mutants.append((
            "claude_capture_unknown_nonzero_becomes_rejected",
            "    if proc.returncode:\n"
            "        status = _claude_failure_status(combined)\n"
            "        return _result(status, reason=\"setup_failed\", returncode=proc.returncode)",
            "    if proc.returncode:\n"
            "        status = \"rejected\"\n"
            "        return _result(status, reason=\"setup_failed\", returncode=proc.returncode)",
            claude_capture_status_lock,
        ))
        mutants.append((
            "session_partial_write_forgets_created_identity",
            "                created_identity = _created_secret_identity(fd)\n"
            "                break\n"
            "            else:\n"
            "                raise OSError(\"could not allocate secret temporary file\")\n"
            "            _write_secret_fd(fd, data, created_identity)",
            "                write_identity = _created_secret_identity(fd)\n"
            "                break\n"
            "            else:\n"
            "                raise OSError(\"could not allocate secret temporary file\")\n"
            "            _write_secret_fd(fd, data, write_identity)\n"
            "            created_identity = write_identity",
            secret_write_cleanup_lock,
        ))
        mutants.append((
            "missing_parent_creation_uses_pathname_before_capability",
            "    return _walk_parent_capability(path.parent, create=create)",
            "    path.parent.mkdir(parents=True, exist_ok=True)\n"
            "    parent_fd = os.open(path.parent, _directory_flags())\n"
            "    _validate_parent_capability(parent_fd)\n"
            "    return parent_fd",
            missing_parent_capability_lock,
        ))
        mutants.extend((
            (
                "session_directory_fsync_unsupported_is_treated_as_success",
                "        os.fsync(parent_fd)\n        created_name = None",
                "        try:\n            os.fsync(parent_fd)\n"
                "        except OSError as exc:\n"
                "            if exc.errno not in (errno.EINVAL, getattr(errno, 'ENOTSUP', errno.EINVAL)):\n"
                "                raise\n        created_name = None",
                secret_write_cleanup_lock,
            ),
            (
                "session_parent_close_failure_replaces_original",
                "    if primary is not None:\n"
                "        raise primary.with_traceback(primary_traceback)\n"
                "    if close_error is not None:\n        raise close_error\n"
                "    return result",
                "    if close_error is not None:\n        raise close_error\n"
                "    if primary is not None:\n"
                "        raise primary.with_traceback(primary_traceback)\n"
                "    return result",
                secret_write_cleanup_lock,
            ),
        ))
    else:
        print("SKIP claude_capture_unknown_nonzero_becomes_rejected "
              "(POSIX PTY/capability primitive unavailable)")
        print("SKIP session_partial_write_forgets_created_identity "
              "(POSIX capability primitive unavailable)")
        print("SKIP missing_parent_creation_uses_pathname_before_capability "
              "(POSIX capability primitive unavailable)")
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
        provider_path = P.with_name("provider_exec.py")
        provider_source = provider_path.read_text(encoding="utf-8")
        provider_mutants = [(
            "provider_path_expands_relative_tilde_entry",
            "        lexical = Path(raw)\n"
            "        if not lexical.is_absolute():",
            "        lexical = Path(raw).expanduser()\n"
            "        if not lexical.is_absolute():",
            provider_executable_lock,
        )]
        if os.name == "posix":
            provider_mutants.append((
                "provider_launch_support_is_unbound",
                '        return "posix-script", (support,), (), identities',
                '        return "direct", (), (), []',
                provider_executable_lock))
        else:
            provider_mutants.extend((
                (
                    "provider_temp_lookup_requires_private_acl",
                    '    elif os.name == "nt":\n        try:',
                    '    elif os.name == "nt":\n'
                    '        if sys.version_info < (3, 13):\n'
                    '            raise OSError('
                    '"private Windows provider directory ACL unavailable")\n'
                    '        try:',
                    windows_pre313_provider_binding_lock,
                ),
                (
                    "provider_launch_support_is_unbound",
                    '    return ("npm-cmd", (node, script), (),\n'
                    '            [(node, node_identity), (script, script_identity)])',
                    '    return ("direct", (), (), [])',
                    provider_executable_lock,
                ),
            ))
        original_globals = {
            "bind_provider_executable": m.bind_provider_executable,
            "_shared_provider_argv": m._shared_provider_argv,
            "_provider_file_identity": m._provider_file_identity,
            "_BoundProviderExecutable": m._BoundProviderExecutable,
            "_ProviderExecutableError": m._ProviderExecutableError,
        }
        try:
            for index, (name, old, new, lock) in enumerate(provider_mutants):
                assert provider_source.count(old) == 1, f"{name} site missing"
                mutant_path = Path(td) / f"provider_exec_{index}.py"
                mutant_path.write_text(
                    provider_source.replace(old, new), encoding="utf-8", newline="\n")
                mutant_spec = importlib.util.spec_from_file_location(
                    f"provider_exec_mutant_{index}", mutant_path)
                mutant = importlib.util.module_from_spec(mutant_spec)
                sys.modules[mutant_spec.name] = mutant
                mutant_spec.loader.exec_module(mutant)
                m.bind_provider_executable = mutant.bind_provider_executable
                m._shared_provider_argv = mutant.provider_argv
                m._provider_file_identity = mutant.provider_file_identity
                m._BoundProviderExecutable = mutant.BoundProviderExecutable
                m._ProviderExecutableError = mutant.ProviderExecutableError
                try:
                    lock(m)
                except (AssertionError, OSError):
                    killed += 1
                    print(f"PASS {name} (killed 1/1)")
                    continue
                raise AssertionError(f"{name} survived")
        finally:
            for key, value in original_globals.items():
                setattr(m, key, value)
    total = len(mutants) + len(provider_mutants)
    print(f"PASS session credential mutations (killed {killed}/{total})")


def run():
    directory_root_lock(m)
    provider_executable_lock(m)
    windows_pre313_provider_binding_lock(m)
    provider_home_lock(m)
    provider_private_acl_unavailable_lock(m)
    provider_cleanup_lock(m)
    missing_parent_capability_lock(m)
    secret_write_cleanup_lock(m)
    claude_status_lock(m)
    claude_capture_status_lock(m)
    github_status_lock(m)
    tl_status_lock(m)
    expected_repository = P.resolve().parents[2]
    assert m.REPOSITORY_ROOT == expected_repository
    with tempfile.TemporaryDirectory() as td, _safe_executable_directory() as executable_td:
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

            # Mutation witness: reparent the already-open final component into
            # a repository immediately before the final ancestry validation.
            # Component no-follow checks cannot see this; deleting only the
            # final validator must therefore reach the vulnerable write.
            mutant_repo = root / "mutant-repo"
            (mutant_repo / ".git").mkdir(parents=True)
            original_component_check = m._fd_is_repository_root

            def exercise_reparent(*, delete_final_validator):
                source_parent = root / (
                    "mutant-parent-deleted" if delete_final_validator
                    else "mutant-parent-control")
                source_parent.mkdir()
                moved_parent = mutant_repo / source_parent.name
                identity = (source_parent.stat().st_dev, source_parent.stat().st_ino)
                moved = False

                def reparent_before_final(directory_fd):
                    nonlocal moved
                    opened = os.fstat(directory_fd)
                    if not moved and (opened.st_dev, opened.st_ino) == identity:
                        source_parent.rename(moved_parent)
                        moved = True
                    return original_component_check(directory_fd)

                patches = [mock.patch.object(
                    m, "_fd_is_repository_root", side_effect=reparent_before_final)]
                if delete_final_validator:
                    patches.append(mock.patch.object(
                        m, "_validate_parent_capability", return_value=None))
                with patches[0]:
                    if delete_final_validator:
                        with patches[1]:
                            m._atomic_secret(source_parent / "auth.json", b"FIXTURE_ONLY")
                    else:
                        try:
                            m._atomic_secret(source_parent / "auth.json", b"FIXTURE_ONLY")
                            assert False, "pre-validation reparent entered repository"
                        except m.UnsafeSecretDestination:
                            pass
                return moved_parent

            control_parent = exercise_reparent(delete_final_validator=False)
            assert not (control_parent / "auth.json").exists()
            mutant_parent = exercise_reparent(delete_final_validator=True)
            assert (mutant_parent / "auth.json").read_bytes() == b"FIXTURE_ONLY", \
                "final ancestry-validator mutant did not reach vulnerable behavior"

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
        bindir = Path(executable_td)
        fake = bindir / "claude"
        fake.write_text(f"""#!{sys.executable}
import json,os,sys,time
assert os.isatty(0) and os.isatty(1) and os.isatty(2)
open(os.path.join(os.path.dirname(__file__), 'setup-env.json'), 'w').write(json.dumps(dict(os.environ)))
os.write(1,b'Confirm setup? ')
if not sys.stdin.readline(): raise SystemExit(2)
os.write(1,b'sk-ant-oat01-' + b'A'*180); time.sleep(.02)
os.write(1,b'A'*180 + b'\\n')
""", encoding="utf-8")
        fake.chmod(0o755)
        fake_gh = bindir / "gh"
        fake_gh.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8", newline="\n")
        fake_gh.chmod(0o755)
        out, displayed = root / "claude.token", io.StringIO()
        read_fd, write_fd = os.pipe(); os.write(write_fd, b"yes\n"); os.close(write_fd)
        with os.fdopen(read_fd) as user_input:
            result = m.capture_claude(out, timeout=5,
                env={"PATH": str(bindir),
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
                env={"PATH": str(bindir)},
                input_stream=user_input, output_stream=raced_display)
        assert raced == {"status": "rejected", "reason": "secret_destination_in_repository"}
        assert not raced_out.exists()
        assert "sk-ant" not in raced_display.getvalue() and "A"*20 not in raced_display.getvalue()

        with tempfile.TemporaryDirectory(prefix="claude-capture-", dir=repo) as rd:
            repo_output, rejected_display = Path(rd) / "claude.token", io.StringIO()
            read_fd, write_fd = os.pipe(); os.write(write_fd, b"yes\n"); os.close(write_fd)
            with os.fdopen(read_fd) as user_input:
                result = m.capture_claude(repo_output, timeout=5,
                    env={"PATH": str(bindir)},
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
                "PATH": str(bindir), "X": "1"})
        assert result["status"] == "passed" and len(seen) == 2
        assert all("CANARY" not in repr(x[0])
                   and x[1]["env"].get("PATH") == str(bindir.resolve())
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
                assert m.github_probe("o/r", env={"GITHUB_PAT": "S",
                    "PATH": str(bindir)})["status"] == "rejected"
        proxy_403 = mock.Mock(returncode=1, stdout="HTTP/1.1 403 Forbidden\n", stderr="")
        with mock.patch.object(m.subprocess, "run", return_value=proxy_403):
            assert m.github_probe("o/r", env={"GITHUB_PAT": "S",
                "PATH": str(bindir)})["status"] == "not_measured"
        assert m.github_probe("o/r", env={"PATH": str(bindir)})["status"] == "missing"

        marker = "TRALUAT-CLAUDE-CREDENTIAL-OK"
        good = mock.Mock(returncode=0, stdout=marker + "\n", stderr="")
        with mock.patch.object(m.subprocess, "run", return_value=good) as run_child:
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CANARY",
                "CODEX_AUTH_JSON": "CODEX_CANARY", "GITHUB_PAT": "GH_CANARY",
                "TL_MASTER_KEY": "TL_CANARY", "ANTHROPIC_API_KEY": "VENDOR_CANARY",
                "HOME": "/home/test", "PATH": str(bindir)})["status"] == "passed"
        command, kwargs = run_child.call_args
        assert command[0][-2] == "-p" and kwargs["stdin"] is m.subprocess.DEVNULL
        assert "CANARY" not in repr(command)
        assert kwargs["env"].get("CLAUDE_CODE_OAUTH_TOKEN") == "CLAUDE_CANARY"
        assert kwargs["env"].get("PATH") == str(bindir.resolve())
        assert kwargs["env"]["HOME"] != "/home/test"
        assert set(kwargs["env"]) == {"PATH", "HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
                                      "XDG_DATA_HOME", "XDG_STATE_HOME",
                                      "TMPDIR", "TMP", "TEMP",
                                      "CLAUDE_CODE_OAUTH_TOKEN"}
        no_marker = mock.Mock(returncode=0, stdout="done\n", stderr="")
        with mock.patch.object(m.subprocess, "run", return_value=no_marker):
            missing_marker = m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S",
                "PATH": str(bindir)})
        assert missing_marker == {"status": "not_measured",
                                  "reason": "marker_missing", "returncode": 0}
        refused = mock.Mock(returncode=1, stdout="", stderr="401 unauthorized")
        with mock.patch.object(m.subprocess, "run", return_value=refused):
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S",
                "PATH": str(bindir)})["status"] == "rejected"
        with mock.patch.object(m.subprocess, "run", side_effect=m.subprocess.TimeoutExpired("claude", 1)):
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S",
                "PATH": str(bindir)})["status"] == "not_measured"

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
