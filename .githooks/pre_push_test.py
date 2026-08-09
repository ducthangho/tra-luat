# -*- coding: utf-8 -*-
"""wp52 — behavior tests for the real pre-push hook and a real bare remote."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

SOURCE_ROOT = Path(__file__).resolve().parent.parent
HOOK_SOURCE = SOURCE_ROOT / ".githooks" / "pre-push"
EOL_BASE = "1880346d2be3c0be9a93de7624ee108d99b6c88c"
GIT_EXE = shutil.which("git")

if not GIT_EXE:
    raise RuntimeError("git executable is required")


def _run(args, *, cwd, env=None, check=False):
    proc = subprocess.run(
        [str(part) for part in args],
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            "command failed rc=%d: %s\nstdout:\n%s\nstderr:\n%s"
            % (proc.returncode, " ".join(map(str, args)), proc.stdout, proc.stderr)
        )
    return proc


class PushFixture:
    def __init__(self, root):
        self.root = root
        self.work = root / "work"
        self.remote = root / "remote.git"
        _run(["git", "init", "--quiet", "--initial-branch=main", str(self.work)], cwd=root, check=True)
        _run(["git", "init", "--bare", "--quiet", str(self.remote)], cwd=root, check=True)
        _run(["git", "config", "user.email", "wp52@example.invalid"], cwd=self.work, check=True)
        _run(["git", "config", "user.name", "wp52 pre-push test"], cwd=self.work, check=True)
        (self.work / "history.txt").write_text("legacy\n", encoding="utf-8", newline="\n")
        _run(["git", "add", "history.txt"], cwd=self.work, check=True)
        _run(["git", "commit", "--quiet", "-m", "legacy"], cwd=self.work, check=True)
        self.legacy = _run(["git", "rev-parse", "HEAD"], cwd=self.work, check=True).stdout.strip()
        (self.work / "history.txt").write_text("legacy\neol\n", encoding="utf-8", newline="\n")
        _run(["git", "commit", "--quiet", "-am", "eol base"], cwd=self.work, check=True)
        self.eol_base = _run(["git", "rev-parse", "HEAD"], cwd=self.work, check=True).stdout.strip()
        (self.work / "history.txt").write_text("legacy\neol\ncurrent\n", encoding="utf-8", newline="\n")
        _run(["git", "commit", "--quiet", "-am", "current"], cwd=self.work, check=True)
        if not HOOK_SOURCE.is_file():
            raise AssertionError("pre-push hook is missing")
        hook = self.work / ".githooks" / "pre-push"
        source = HOOK_SOURCE.read_text(encoding="utf-8")
        if source.count(EOL_BASE) != 1:
            raise AssertionError("production hook must pin the exact EOL base once")
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text(source.replace(EOL_BASE, self.eol_base), encoding="utf-8", newline="\n")
        hook.chmod(0o755)
        _run(["git", "config", "core.hooksPath", ".githooks"], cwd=self.work, check=True)
        _run(["git", "remote", "add", "origin", str(self.remote)], cwd=self.work, check=True)

    def push(self, *refspecs, env=None):
        return _run([GIT_EXE, "push", "origin", *refspecs], cwd=self.work, env=env)

    def remote_ref(self, ref):
        return _run(["git", "--git-dir", str(self.remote), "rev-parse", "--verify", ref], cwd=self.root)

    def replace_required_base(self, replacement):
        hook = self.work / ".githooks" / "pre-push"
        source = hook.read_text(encoding="utf-8")
        if source.count(self.eol_base) != 1:
            raise AssertionError("fixture hook must contain its required base exactly once")
        hook.write_text(
            source.replace(self.eol_base, replacement), encoding="utf-8", newline="\n"
        )

    def install_gate_stubs(self):
        scripts = self.work / "scripts"
        checks = self.work / ".github" / "checks"
        hooks = self.work / ".githooks"
        scripts.mkdir(parents=True, exist_ok=True)
        checks.mkdir(parents=True, exist_ok=True)
        hooks.mkdir(parents=True, exist_ok=True)
        core = scripts / "tl_core"
        core.mkdir(parents=True, exist_ok=True)
        tl_stub = """\
import json
import os
import pathlib
import subprocess
import sys
import tempfile

if os.environ.get("WP52_GATE_CRASH"):
    raise RuntimeError("fixture gate crash")
if os.environ.get("WP52_GATE_FAIL") and "--selftest" in sys.argv:
    print("0/1 dat")
    raise SystemExit(9)
if os.environ.get("WP52_GATE_SILENT") and "--selftest" in sys.argv:
    raise SystemExit(0)
if "--selftest" in sys.argv:
    with tempfile.TemporaryDirectory(prefix="wp52_abbrev_") as tmp:
        subprocess.run(["git", "init", "--quiet", tmp], check=True)
        subprocess.run(["git", "config", "core.abbrev", "8"], cwd=tmp, check=True)
        effective = subprocess.check_output(
            ["git", "config", "--get", "core.abbrev"], cwd=tmp, text=True
        ).strip()
    if effective != "8":
        print("fixture local core.abbrev override was masked: " + effective)
        raise SystemExit(10)
if "release-bundle" in sys.argv:
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(b"wp52 deterministic fixture bundle\\n")
    print(json.dumps({
        "ok": True,
        "file_count": 179,
        "reproducible": True,
        "bundle_sha256": "a" * 64,
    }))
elif "release-verify" in sys.argv:
    print(json.dumps({
        "ok": True,
        "expected_file_count": 179,
        "checked_file_count": 179,
        "failed": [],
        "extra_files": [],
        "missing_from_current_manifest": [],
        "required_missing": [],
        "errors": [],
    }))
else:
    print(json.dumps({"ok": True}))
if "--selftest" in sys.argv:
    print("1/1 dat")
"""
        (scripts / "tl.py").write_text(tl_stub, encoding="utf-8", newline="\n")
        (scripts / "tl_boot.py").write_text(
            "print('tl fixture')\n", encoding="utf-8", newline="\n"
        )
        (scripts / "gen_instructions.py").write_text(
            "print('1/1 dat')\n", encoding="utf-8", newline="\n"
        )
        for name in (
            "__init__.py", "deterministic.py", "jsonio.py", "workflow.py", "release.py",
            "live.py", "zip_ingest.py", "ocr.py", "chunking.py", "command_registry.py",
        ):
            (core / name).write_text("# gate fixture\n", encoding="utf-8", newline="\n")
        (hooks / "eol_policy.py").write_text(
            "print('{\"ok\": true, \"violations\": []}')\n",
            encoding="utf-8",
            newline="\n",
        )
        (hooks / "eol_policy_test.py").write_text(
            "print('1/1 dat')\n", encoding="utf-8", newline="\n"
        )
        (checks / "bundle_fragment_check.py").write_text(
            "print('{\"ok\": true}')\n", encoding="utf-8", newline="\n"
        )
        _run(
            ["git", "add", "scripts", ".github/checks", ".githooks/pre-push",
             ".githooks/eol_policy.py", ".githooks/eol_policy_test.py"],
            cwd=self.work,
            check=True,
        )
        _run(["git", "commit", "--quiet", "-m", "gate fixture"], cwd=self.work, check=True)


def case_writer_branch_requires_eol_ancestry(root):
    fx = PushFixture(root)
    _run(["git", "branch", "legacy", fx.legacy], cwd=fx.work, check=True)

    blocked = fx.push("legacy:refs/heads/legacy")
    if blocked.returncode == 0 or fx.remote_ref("refs/heads/legacy").returncode == 0:
        return False

    allowed = fx.push("HEAD:refs/heads/eol-writer")
    return allowed.returncode == 0 and fx.remote_ref("refs/heads/eol-writer").returncode == 0


def case_master_requires_green_full_gate(root):
    fx = PushFixture(root)
    fx.install_gate_stubs()
    red_env = os.environ.copy()
    red_env["WP52_GATE_FAIL"] = "1"
    blocked = fx.push("HEAD:refs/heads/master", env=red_env)
    if blocked.returncode == 0 or fx.remote_ref("refs/heads/master").returncode == 0:
        return False
    allowed = fx.push("HEAD:refs/heads/master")
    return allowed.returncode == 0 and fx.remote_ref("refs/heads/master").returncode == 0


def case_master_gates_exact_pushed_snapshot(root):
    fx = PushFixture(root)
    fx.install_gate_stubs()
    tl_path = fx.work / "scripts" / "tl.py"
    green_source = tl_path.read_text(encoding="utf-8")
    marker = "import tempfile\n\n"
    if green_source.count(marker) != 1:
        raise AssertionError("fixture tl.py import marker drifted")
    red_source = green_source.replace(
        marker,
        marker + "if '--selftest' in sys.argv:\n    raise SystemExit(9)\n\n",
    )
    tl_path.write_text(red_source, encoding="utf-8", newline="\n")
    _run(["git", "commit", "--quiet", "-am", "red candidate"], cwd=fx.work, check=True)
    red_candidate = _run(["git", "rev-parse", "HEAD"], cwd=fx.work, check=True).stdout.strip()
    tl_path.write_text(green_source, encoding="utf-8", newline="\n")
    _run(["git", "commit", "--quiet", "-am", "green current tree"], cwd=fx.work, check=True)

    pushed = fx.push("%s:refs/heads/master" % red_candidate)
    return (
        pushed.returncode != 0
        and fx.remote_ref("refs/heads/master").returncode != 0
    )


def case_zero_rc_without_positive_evidence_blocks_master(root):
    fx = PushFixture(root)
    fx.install_gate_stubs()
    silent_env = os.environ.copy()
    silent_env["WP52_GATE_SILENT"] = "1"
    pushed = fx.push("HEAD:refs/heads/master", env=silent_env)
    return (
        pushed.returncode != 0
        and fx.remote_ref("refs/heads/master").returncode != 0
    )


def case_absolute_git_dir_does_not_redirect_snapshot(root):
    fx = PushFixture(root)
    fx.install_gate_stubs()
    linked_env = os.environ.copy()
    linked_env["GIT_DIR"] = str(fx.work / ".git")
    pushed = fx.push("HEAD:refs/heads/master", env=linked_env)
    return (
        pushed.returncode == 0
        and fx.remote_ref("refs/heads/master").returncode == 0
    )


def case_multi_ref_is_atomic_and_delete_tag_are_ignored(root):
    fx = PushFixture(root)
    _run(["git", "branch", "legacy", fx.legacy], cwd=fx.work, check=True)

    mixed = fx.push(
        "HEAD:refs/heads/good",
        "legacy:refs/heads/bad",
    )
    if mixed.returncode == 0:
        return False
    if fx.remote_ref("refs/heads/good").returncode == 0:
        return False
    if fx.remote_ref("refs/heads/bad").returncode == 0:
        return False

    if fx.push("HEAD:refs/heads/delete-me").returncode != 0:
        return False
    if fx.push(":refs/heads/delete-me").returncode != 0:
        return False
    if fx.remote_ref("refs/heads/delete-me").returncode == 0:
        return False

    _run(["git", "tag", "legacy-tag", fx.legacy], cwd=fx.work, check=True)
    tagged = fx.push("refs/tags/legacy-tag:refs/tags/legacy-tag")
    return tagged.returncode == 0 and fx.remote_ref("refs/tags/legacy-tag").returncode == 0


def case_missing_required_object_blocks_push(root):
    fx = PushFixture(root)
    fx.replace_required_base("f" * 40)
    pushed = fx.push("HEAD:refs/heads/missing-eol-object")
    return (
        pushed.returncode != 0
        and "cannot verify EOL ancestry" in pushed.stderr
        and fx.remote_ref("refs/heads/missing-eol-object").returncode != 0
    )


def case_unexpected_gate_exception_blocks_master(root):
    fx = PushFixture(root)
    fx.install_gate_stubs()
    crash_env = os.environ.copy()
    crash_env["WP52_GATE_CRASH"] = "1"
    pushed = fx.push("HEAD:refs/heads/master", env=crash_env)
    return (
        pushed.returncode != 0
        and "gate tl selftest failed" in pushed.stderr
        and "fixture gate crash" in pushed.stderr
        and fx.remote_ref("refs/heads/master").returncode != 0
    )


def case_missing_python_blocks_with_reason(root):
    fx = PushFixture(root)
    restricted_path = root / "git-only-path"
    restricted_path.mkdir()
    git_copy = restricted_path / Path(GIT_EXE).name
    shutil.copy2(GIT_EXE, git_copy)
    no_python_env = os.environ.copy()
    no_python_env["PATH"] = str(restricted_path)
    pushed = fx.push("HEAD:refs/heads/no-python", env=no_python_env)
    return (
        pushed.returncode != 0
        and "Python is required" in pushed.stderr
        and fx.remote_ref("refs/heads/no-python").returncode != 0
    )


CASES = [
    case_writer_branch_requires_eol_ancestry,
    case_master_requires_green_full_gate,
    case_master_gates_exact_pushed_snapshot,
    case_zero_rc_without_positive_evidence_blocks_master,
    case_absolute_git_dir_does_not_redirect_snapshot,
    case_multi_ref_is_atomic_and_delete_tag_are_ignored,
    case_missing_required_object_blocks_push,
    case_unexpected_gate_exception_blocks_master,
    case_missing_python_blocks_with_reason,
]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    passed = 0
    failed = []
    for case in CASES:
        with tempfile.TemporaryDirectory(prefix="wp52_pre_push_") as tmp:
            try:
                ok = bool(case(Path(tmp)))
            except Exception as exc:  # fail loud: the suite must never skip infrastructure failures
                ok = False
                print("  ! %s: %r" % (case.__name__, exc))
        print("%s %s" % ("PASS" if ok else "FAIL", case.__name__))
        if ok:
            passed += 1
        else:
            failed.append(case.__name__)
    print("\n%d/%d dat" % (passed, len(CASES)))
    if failed:
        print("HONG: %s" % ", ".join(failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
