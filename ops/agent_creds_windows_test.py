#!/usr/bin/env python3
"""WP1170 fake-only checks. --scratch MUST be outside the checkout.

Linux: --logic-only measures parser/payload logic, never claims NTFS evidence.
Windows default: real NTFS objects, DACL/AccessCheck/readback, races and links.
No imports or calls to a real credential loader; all homes/keys/bundles are fake.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import tl_gws as g  # noqa: E402
import gws_cred_store as store  # noqa: E402

CANARY = "wp1170_FAKE_ONLY_never_print_this_7c9f"
MASTER = "wp1170_fake_master_0123456789abcdef"
SCRATCH = None
KILL_POINTS = ("created", "partial_write", "after_write", "after_flush",
               "after_readback", "before_publish", "after_publish", "before_close", "after_close")


def payload():
    return {"schema": 1, "rev": 1, "codex_auth": {"tokens": {
        "access_token": CANARY, "refresh_token": CANARY, "id_token": CANARY},
        "last_refresh": "2026-11-01T00:00:00Z"},
        "claude_oauth_token": "FAKE_CLAUDE_UNUSED", "antigravity_api_key": "FAKE_GEMINI_UNUSED",
        "gws_cred": "FAKE_GWS_UNUSED", "nlm_auth": "FAKE_NLM_UNUSED", "token": "FAKE_GAS_UNUSED"}


def encrypted(p=None):
    return store.encrypt(json.dumps(payload() if p is None else p).encode(), MASTER)


class Logic(unittest.TestCase):
    def test_payload_roundtrip_codex_only(self):
        out = json.loads(g._codex_restore_payload(encrypted(), MASTER))
        self.assertTrue(out == payload()["codex_auth"])
        self.assertFalse(any(k in out for k in ("gws_cred", "nlm_auth", "token", "claude_oauth_token")))

    def test_bad_schema_missing_tokens_and_authentication(self):
        for p in ({}, {"schema": True}, {"schema": 2}, {"schema": 1, "codex_auth": {}},
                  {"schema": 1, "codex_auth": {"tokens": {}}},
                  {"schema": 1, "codex_auth": {"tokens": {"access_token": "x"}}}):
            with self.assertRaises(ValueError):
                g._codex_restore_payload(encrypted(p), MASTER)
        for b, key in ((encrypted(), MASTER + "wrong"), (b"not encrypted", MASTER)):
            with self.assertRaises(ValueError):
                g._codex_restore_payload(b, key)

    def test_duplicate_json_keys_rejected(self):
        blob = store.encrypt(b'{"schema":1,"schema":1}', MASTER)
        with self.assertRaises(ValueError):
            g._codex_restore_payload(blob, MASTER)

    def test_path_aliases_rejected_before_normalization(self):
        for raw in ("relative", "C:relative", "C:\\", "\\\\server\\share\\home", "\\\\?\\C:\\home",
                    "C:/a/../home", "C:/a/./home", "C:/home ", "C:/home.", "C:/NUL",
                    "C:/COM1.txt", "C:/COM¹", "C:/home:stream", "C:/a//home", "C:/a\x00/home"):
            with self.assertRaises(ValueError, msg="unsafe alias accepted"):
                g._codex_restore_home(raw)

    def test_parser_confirmation_and_lazy_dispatch(self):
        import tl
        ap = tl.build_parser()
        a = ap.parse_args(["agent-creds-restore", "--codex"])
        self.assertFalse(a.apply)
        self.assertIs(a.fn, g.cmd_agent_creds_restore)
        self.assertIn("agent-creds-restore", tl._CREDS_LAZY_CMDS)
        with mock.patch.object(tl, "load_creds", side_effect=AssertionError("config touched")), \
             mock.patch.object(g, "_CodexRestoreWindows", side_effect=AssertionError("should not enter")), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tl.main(["agent-creds-restore", "--codex", "--apply"]), 2)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            ap.parse_args(["agent-creds-restore", "--codex", "--force"])

    def test_non_windows_fails_closed(self):
        if os.name == "nt":
            # Platform guard itself is deterministic; native operations tested below.
            with mock.patch.object(g.os, "name", "posix"), self.assertRaises(OSError):
                g._CodexRestoreWindows()
        else:
            with self.assertRaises(OSError):
                g._CodexRestoreWindows()


class Windows(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="wp1170-", dir=SCRATCH)
        self.root = Path(self.tmp.name)
        self.home = self.root / "codex-home"
        self.bundle = self.root / "fake-agent.enc"
        self.bundle.write_bytes(encrypted())
        self.env = mock.patch.dict(os.environ, {"CODEX_HOME": str(self.home), "TL_MASTER_KEY": MASTER})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def command(self, *, apply=False, confirm=None):
        a = SimpleNamespace(codex=True, apply=apply, confirm=confirm, bundle_file=str(self.bundle))
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = g.cmd_agent_creds_restore(a)
        logs = out.getvalue() + err.getvalue()
        self.assertNotIn(CANARY, logs)
        self.assertNotIn(MASTER, logs)
        return rc, logs

    def make_home(self):
        with g._CodexRestoreWindows() as fs:
            self.assertFalse(fs.prepare(self.home, True))

    def test_dry_run_confirmation_apply_dacl_effective_readback(self):
        self.assertEqual(self.command()[0], 0)
        self.assertFalse(self.home.exists())
        self.assertEqual(self.command(apply=True)[0], 2)
        self.assertFalse(self.home.exists())
        self.assertEqual(self.command(apply=True, confirm="yes")[0], 0)
        self.assertTrue(json.loads((self.home / "auth.json").read_bytes()) == payload()["codex_auth"])
        with g._CodexRestoreWindows() as fs:
            fs.private(fs.directory(self.home))
            h = fs.open(str(self.home / "auth.json"), 0x20000, 1, None, 3, 0x200000, None)
            self.assertNotEqual(h, fs.c.c_void_p(-1).value)
            try:
                fs.private(h)  # owner, protected DACL, exact ACE, real AccessCheck
            finally:
                fs.close(h)
        self.assertEqual(sorted(p.name for p in self.home.iterdir()), ["auth.json"])

    def test_existing_auth_never_read_or_bundle_loaded(self):
        self.home.mkdir()
        target = self.home / "auth.json"
        target.write_bytes(b"FAKE_EXISTING_UNPARSEABLE")
        before = target.stat()
        self.bundle.unlink()
        with mock.patch.object(g, "_master_key", side_effect=AssertionError("key read")), \
             mock.patch.object(g, "_codex_restore_payload", side_effect=AssertionError("decrypt called")):
            self.assertEqual(self.command(apply=True, confirm="yes")[0], 0)
        after = target.stat()
        self.assertTrue(target.read_bytes() == b"FAKE_EXISTING_UNPARSEABLE")
        self.assertEqual((before.st_size, before.st_mtime_ns), (after.st_size, after.st_mtime_ns))

    def test_wp1170_repeat_apply_is_noop_without_secret_reads(self):
        self.assertEqual(self.command(apply=True, confirm="yes")[0], 0)
        target = self.home / "auth.json"
        before = target.stat()
        original = target.read_bytes()
        self.bundle.write_bytes(b"FAKE_STALE_CORRUPT_BUNDLE")
        # Repeating a successful restore must not inspect auth contents, the key,
        # or the now-invalid source. Keep metadata and the sole link unchanged.
        with mock.patch("builtins.open", side_effect=AssertionError("file read")), \
             mock.patch.object(g, "_master_key", side_effect=AssertionError("key read")), \
             mock.patch.object(g, "_codex_restore_payload", side_effect=AssertionError("decrypt called")), \
             mock.patch.object(g, "_public_curl_bytes", side_effect=AssertionError("network called")):
            for apply in (False, True):
                self.assertEqual(self.command(apply=apply, confirm="yes")[0], 0)
        after = target.stat()
        self.assertTrue(target.read_bytes() == original)
        self.assertEqual((before.st_ino, before.st_size, before.st_mtime_ns, before.st_nlink),
                         (after.st_ino, after.st_size, after.st_mtime_ns, after.st_nlink))
        self.assertEqual(sorted(p.name for p in self.home.iterdir()), ["auth.json"])

    def test_weak_existing_home_refused_without_acl_repair(self):
        self.home.mkdir()
        self.assertEqual(self.command(apply=True, confirm="yes")[0], 4)
        self.assertFalse((self.home / "auth.json").exists())
        self.assertEqual(list(self.home.iterdir()), [])

    def test_no_replace_competitor_wins_and_staging_cleaned(self):
        self.make_home()
        original = g._CodexRestoreWindows.publish
        def race(fs, home, data):
            (home / "auth.json").write_bytes(b"FAKE_RACE_WINNER")
            return original(fs, home, data)
        with mock.patch.object(g._CodexRestoreWindows, "publish", race):
            self.assertEqual(self.command(apply=True, confirm="yes")[0], 4)
        self.assertTrue((self.home / "auth.json").read_bytes() == b"FAKE_RACE_WINNER")
        self.assertEqual(sorted(p.name for p in self.home.iterdir()), ["auth.json"])

    def test_concurrent_publish_exactly_one_wins(self):
        self.make_home()
        barrier = threading.Barrier(2)
        results = []
        def writer(data):
            try:
                with g._CodexRestoreWindows() as fs:
                    fs.prepare(self.home, True)
                    barrier.wait(timeout=10)
                    fs.publish(self.home, data)
                results.append("created")
            except OSError:
                results.append("collision")
        threads = [threading.Thread(target=writer, args=(v,)) for v in (b"FAKE_A", b"FAKE_B")]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=20)
        self.assertEqual(sorted(results), ["collision", "created"])
        self.assertTrue((self.home / "auth.json").read_bytes() in (b"FAKE_A", b"FAKE_B"))
        self.assertEqual(sorted(p.name for p in self.home.iterdir()), ["auth.json"])

    def test_wp1170_abrupt_termination_kernel_cleans_staging(self):
        # Parent really invokes TerminateProcess via Popen.kill; child cannot run
        # Python finally/atexit. Checkpoints wrap native calls, not product hooks.
        for point in KILL_POINTS:
            with self.subTest(point=point):
                home = self.root / point
                env = {k: os.environ[k] for k in ("SystemRoot", "WINDIR", "COMSPEC", "PATH") if k in os.environ}
                env.update({"USERPROFILE": str(self.root), "HOME": str(self.root),
                            "CODEX_HOME": str(home), "TEMP": str(SCRATCH), "TMP": str(SCRATCH),
                            "APPDATA": str(self.root / "appdata"), "LOCALAPPDATA": str(self.root / "local"),
                            "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"})
                cmd = [sys.executable, "-B", str(Path(__file__).resolve()), "--scratch", str(SCRATCH),
                       "--kill-child", point, "--child-home", str(home)]
                p = subprocess.Popen(cmd, cwd=self.root, env=env, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                line = queue.Queue()
                reader = threading.Thread(target=lambda: line.put(p.stdout.readline()), daemon=True)
                reader.start()
                try:
                    try:
                        marker = line.get(timeout=30)
                    except queue.Empty:
                        self.fail("fake child did not reach kill checkpoint: " + point)
                    self.assertEqual(marker, ("WP1170_KILL:" + point + "\n").encode())
                    self.assertIsNone(p.poll(), "child must still be inside native-operation checkpoint")
                    p.kill()
                    out, err = p.communicate(timeout=30)
                    self.assertNotEqual(p.returncode, 0)
                    self.assertNotIn(CANARY.encode(), marker + out + err)
                    self.assertNotIn(MASTER.encode(), marker + out + err)
                    self.assertEqual(list(home.glob(".codex-restore-*")), [], "orphaned plaintext staging")
                    committed = point in ("after_publish", "before_close", "after_close")
                    self.assertEqual((home / "auth.json").exists(), committed)
                    if committed:
                        self.assertEqual((home / "auth.json").read_bytes(),
                                         g._codex_restore_payload(encrypted(), MASTER))
                        self.assertEqual(sorted(p.name for p in home.iterdir()), ["auth.json"])
                    else:
                        self.assertEqual(list(home.iterdir()), [])
                    print(f"WP1170_KILL {point}: child_rc={p.returncode}; staging=0; auth={committed}", flush=True)
                finally:
                    if p.poll() is None:
                        p.kill()
                    p.communicate(timeout=30)
                    reader.join(timeout=5)

    def test_wp1170_short_write_and_failed_link_cleanup(self):
        self.make_home()
        with g._CodexRestoreWindows() as fs:
            fs.prepare(self.home, True)
            original = fs.write
            def short(handle, data, size, written, overlapped):
                return original(handle, data, min(size, 7), written, overlapped)
            fs.write = short
            with self.assertRaises(OSError):
                fs.publish(self.home, CANARY.encode())
        self.assertEqual(list(self.home.iterdir()), [])
        with g._CodexRestoreWindows() as fs:
            fs.prepare(self.home, True)
            fs.link_info = lambda *args: -1073741790  # STATUS_ACCESS_DENIED
            with self.assertRaises(OSError):
                fs.publish(self.home, CANARY.encode())
        self.assertEqual(list(self.home.iterdir()), [])

    def test_wp1170_destination_created_at_publication_never_replaced(self):
        self.make_home()
        with g._CodexRestoreWindows() as fs:
            fs.prepare(self.home, True)
            original = fs.link_info
            def race(*args):
                (self.home / "auth.json").write_bytes(b"FAKE_LATE_RACE_WINNER")
                return original(*args)
            fs.link_info = race
            with self.assertRaises(OSError):
                fs.publish(self.home, CANARY.encode())
        self.assertEqual((self.home / "auth.json").read_bytes(), b"FAKE_LATE_RACE_WINNER")
        self.assertEqual(sorted(p.name for p in self.home.iterdir()), ["auth.json"])

    def test_real_junction_parent_home_and_existing_leaf(self):
        other = self.root / "other"
        other.mkdir()
        junction = self.root / "junction"
        p = subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(other)], capture_output=True)
        self.assertEqual(p.returncode, 0, "junction capability required")
        try:
            with mock.patch.dict(os.environ, {"CODEX_HOME": str(junction / "home")}):
                self.assertEqual(self.command(apply=True, confirm="yes")[0], 4)
            with mock.patch.dict(os.environ, {"CODEX_HOME": str(junction)}):
                self.assertEqual(self.command(apply=True, confirm="yes")[0], 4)
            self.assertEqual(list(other.iterdir()), [])
        finally:
            junction.rmdir()
        # Leaf is never dereferenced/read even when it is an existing link.
        self.make_home()
        leaf = self.home / "auth.json"
        p = subprocess.run(["cmd", "/c", "mklink", "/J", str(leaf), str(other)], capture_output=True)
        self.assertEqual(p.returncode, 0, "leaf junction capability required")
        try:
            self.assertEqual(self.command(apply=True, confirm="yes")[0], 0)
            self.assertFalse((other / "absent").exists())
        finally:
            leaf.rmdir()

    def test_pinned_home_cannot_be_renamed_and_ancestor_reparse_write_blocked(self):
        self.make_home()
        with g._CodexRestoreWindows() as fs:
            fs.prepare(self.home, True)
            with self.assertRaises(OSError):
                self.home.rename(self.root / "moved")
            h = fs.open(str(self.root), 0x40000000, 7, None, 3, 0x02200000, None)
            self.assertEqual(h, fs.c.c_void_p(-1).value)
            self.assertEqual(fs.c.get_last_error(), 32)  # ERROR_SHARING_VIOLATION

    def test_canary_errors_and_no_touch_other_auth_config(self):
        sentinels = [self.root / n for n in ("gas", "gws", "nlm", "config")]
        for p in sentinels:
            p.write_bytes(b"FAKE_SENTINEL")
        before = [(p.read_bytes(), p.stat().st_mtime_ns) for p in sentinels]
        with mock.patch.object(g, "_bootstrap_agent_creds", side_effect=AssertionError("bootstrap")), \
             mock.patch.object(g, "_secrets_fetch", side_effect=AssertionError("secrets")), \
             mock.patch.object(g, "_public_curl_bytes", side_effect=AssertionError("network")):
            self.assertEqual(self.command(apply=True, confirm="yes")[0], 0)
        self.assertTrue(before == [(p.read_bytes(), p.stat().st_mtime_ns) for p in sentinels])
        fresh = self.root / "another-home"
        with mock.patch.dict(os.environ, {"CODEX_HOME": str(fresh)}), \
             mock.patch.object(g, "_codex_restore_payload", side_effect=ValueError(CANARY + MASTER)):
            self.assertEqual(self.command(apply=True, confirm="yes")[0], 4)
        self.assertFalse(fresh.exists())

    def test_real_cli_fake_environment_no_other_file_changes(self):
        # Fresh process exercises tl.py dispatch; it receives no real secret env.
        env = {k: os.environ[k] for k in ("SystemRoot", "WINDIR", "COMSPEC", "PATH") if k in os.environ}
        env.update({"CODEX_HOME": str(self.home), "TL_MASTER_KEY": MASTER,
                    "USERPROFILE": str(self.root), "HOME": str(self.root),
                    "APPDATA": str(self.root / "appdata"), "LOCALAPPDATA": str(self.root / "local"),
                    "TEMP": str(SCRATCH), "TMP": str(SCRATCH),
                    "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"})
        for name in (".config/gws/credentials.json", ".notebooklm-mcp-cli/storage_state.json",
                     "tra_luat_config.v2.json", "gas-config.json"):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"FAKE_SENTINEL_DO_NOT_PARSE")
        def snapshot():
            return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns)
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        cmd = [sys.executable, "-B", str(ROOT / "scripts/tl.py"), "agent-creds-restore", "--codex",
               "--bundle-file", str(self.bundle)]
        for flags, marker in (([], "dry-run"), (["--apply", "--confirm", "yes"], "created")):
            p = subprocess.run(cmd + flags, cwd=self.root, env=env, capture_output=True, timeout=60)
            self.assertEqual(p.returncode, 0, "fake CLI did not succeed")
            self.assertIn(marker.encode(), p.stdout)
            self.assertNotIn(CANARY.encode(), p.stdout + p.stderr)
            self.assertNotIn(MASTER.encode(), p.stdout + p.stderr)
            if not flags:
                self.assertTrue(before == snapshot())
        after = snapshot()
        self.assertEqual(set(after) - set(before), {"codex-home/auth.json".replace("/", os.sep)})
        self.assertTrue(all(after[k] == v for k, v in before.items()))


def kill_child(point, home):
    """Only fake plaintext, in the caller's external scratch; no credentials read."""
    if os.name != "nt" or home.parent != SCRATCH and SCRATCH not in home.parents:
        raise ValueError("Windows child home must be below scratch")
    def checkpoint(name):
        if point == name:
            sys.stdout.buffer.write(("WP1170_KILL:" + name + "\n").encode())
            sys.stdout.buffer.flush()
            sys.stdin.buffer.read(1)  # parent kills us here; no finally is allowed
            raise RuntimeError("checkpoint unexpectedly resumed")
    with g._CodexRestoreWindows() as fs:
        fs.prepare(home, True)
        original_open, original_write = fs.open, fs.write
        original_flush, original_read = fs.flush, fs.read
        original_link, original_close = fs.link_info, fs.close
        staging = None
        def open_file(*args):
            nonlocal staging
            h = original_open(*args)
            if h != fs.c.c_void_p(-1).value and args[5] & 0x04000000:
                staging = h
                checkpoint("created")
            return h
        def write(handle, data, size, written, overlapped):
            if point == "partial_write":
                ok = original_write(handle, data, min(size, 17), written, overlapped)
                fs.check(ok)
                if fs.w.DWORD.from_address(fs.c.cast(written, fs.c.c_void_p).value).value != 17:
                    raise RuntimeError("partial write did not happen")
                checkpoint("partial_write")
            ok = original_write(handle, data, size, written, overlapped)
            fs.check(ok)
            checkpoint("after_write")
            return ok
        def flush(*args):
            ok = original_flush(*args)
            fs.check(ok)
            checkpoint("after_flush")
            return ok
        def read(*args):
            ok = original_read(*args)
            fs.check(ok)
            checkpoint("after_readback")
            return ok
        def link(*args):
            checkpoint("before_publish")
            rc = original_link(*args)
            if rc < 0:
                raise fs.c.WinError(fs.nt_error(rc))
            checkpoint("after_publish")
            return rc
        def close(handle):
            if handle == staging:
                checkpoint("before_close")
            ok = original_close(handle)
            if handle == staging:
                fs.check(ok)
                checkpoint("after_close")
            return ok
        fs.open, fs.write, fs.flush, fs.read = open_file, write, flush, read
        fs.link_info, fs.close = link, close
        data = (json.dumps(payload()["codex_auth"], ensure_ascii=False, allow_nan=False) + "\n").encode()
        fs.publish(home, data)
    raise RuntimeError("checkpoint was not reached")


def main():
    global SCRATCH
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--logic-only", action="store_true")
    ap.add_argument("--kill-child", choices=KILL_POINTS, help=argparse.SUPPRESS)
    ap.add_argument("--child-home", help=argparse.SUPPRESS)
    args = ap.parse_args()
    SCRATCH = Path(args.scratch).resolve(strict=True)
    if SCRATCH == ROOT or ROOT in SCRATCH.parents:
        ap.error("scratch must be outside repository")
    if args.kill_child:
        if not args.child_home:
            ap.error("child home required")
        return kill_child(args.kill_child, Path(args.child_home).resolve())
    if not args.logic_only and os.name != "nt":
        ap.error("Windows NTFS required; use --logic-only for Linux logic evidence")
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(Logic))
    if not args.logic_only:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Windows))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"WP1170 {'LOGIC' if args.logic_only else 'WINDOWS_NTFS'}: "
          f"{result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}; "
          f"ok={result.wasSuccessful()}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
