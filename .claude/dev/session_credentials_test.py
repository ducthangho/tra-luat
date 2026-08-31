#!/usr/bin/env python3
import base64
import importlib.util
import io
import json
import os
import stat
import tempfile
from pathlib import Path
from unittest import mock

P = Path(__file__).with_name("session_credentials.py")
spec = importlib.util.spec_from_file_location("session_credentials", P)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


def run():
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
        assert result["status"] == "passed" and target.read_bytes() == auth
        assert stat.S_IMODE(target.stat().st_mode) == 0o600 and "private" not in repr(result)
        assert m.materialize_codex(env={})["status"] == "missing"
        assert m.materialize_codex(env={"CODEX_AUTH_JSON": "!"})["status"] == "rejected"

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
        assert all("CANARY" not in repr(x[0]) and x[1]["env"] == {
            "PATH": "/bin", "GH_TOKEN": "GH_CANARY"} for x in seen)
        for code in (401, 403, 404):
            denied = mock.Mock(returncode=1, stdout="", stderr=f"HTTP {code}")
            with mock.patch.object(m.subprocess, "run", return_value=denied):
                assert m.github_probe("o/r", env={"GITHUB_PAT": "S"})["status"] == "rejected"
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
        assert "CANARY" not in repr(command) and kwargs["env"] == {
            "HOME": "/home/test", "CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CANARY"}
        no_marker = mock.Mock(returncode=0, stdout="done\n", stderr="")
        with mock.patch.object(m.subprocess, "run", return_value=no_marker):
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S"})["status"] == "rejected"
        refused = mock.Mock(returncode=1, stdout="", stderr="401 unauthorized")
        with mock.patch.object(m.subprocess, "run", return_value=refused):
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S"})["status"] == "rejected"
        with mock.patch.object(m.subprocess, "run", side_effect=m.subprocess.TimeoutExpired("claude", 1)):
            assert m.claude_probe(env={"CLAUDE_CODE_OAUTH_TOKEN": "S"})["status"] == "not_measured"

        with mock.patch.object(m.subprocess, "run", return_value=mock.Mock(returncode=0)) as run_child:
            result = m.tl_bootstrap("cowork", None, env={
                "TL_MASTER_KEY": "TL_CANARY", "CODEX_AUTH_JSON": "CODEX_CANARY",
                "CLAUDE_CODE_OAUTH_TOKEN": "CLAUDE_CANARY", "GITHUB_PAT": "GH_CANARY",
                "OPENAI_API_KEY": "VENDOR_CANARY", "TMPDIR": "/tmp/test"})
        assert result["status"] == "passed"
        assert run_child.call_args.kwargs["env"] == {
            "TMPDIR": "/tmp/test", "TL_MASTER_KEY": "TL_CANARY"}

        calls = []
        def component(name, status="passed"):
            def f(*args, **kwargs): calls.append(name); return {"status": status}
            return f
        with mock.patch.object(m, "materialize_codex", side_effect=component("codex")), \
             mock.patch.object(m, "claude_probe", side_effect=component("claude")), \
             mock.patch.object(m, "github_probe", side_effect=component("github")), \
             mock.patch.object(m, "tl_bootstrap", side_effect=component("tl")):
            combined = m.bootstrap_session("o/r", "cowork", None, None, env={})
        assert combined["status"] == "passed" and calls == ["codex", "claude", "github", "tl"]
        assert set(combined["components"]) == {"codex", "claude", "github", "tl"}
        assert m.tl_bootstrap("cowork", None, env={})["status"] == "missing"
    print("PASS session_credentials_test")


if __name__ == "__main__": run()
