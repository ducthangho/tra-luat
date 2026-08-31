#!/usr/bin/env python3
import importlib.util, os, stat, tempfile
from pathlib import Path
from unittest import mock

P = Path(__file__).with_name("session_credentials.py")
spec = importlib.util.spec_from_file_location("session_credentials", P); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def run():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        assert m.codex_home({"CODEX_HOME": str(root / "custom")}) == root / "custom"
        with mock.patch.object(m.Path, "home", return_value=root): assert m.codex_home({}) == root / ".codex"
        out = root / "claude.token"
        good = mock.Mock(returncode=0, stdout="created sk-ant-oat01-" + "A"*24, stderr="")
        with mock.patch.object(m.subprocess, "run", return_value=good): r=m.capture_claude(out, env={})
        assert r["status"] == "passed" and "sk-ant" not in repr(r)
        assert stat.S_IMODE(out.stat().st_mode) == 0o600
        link=root/"link"; link.symlink_to(out)
        try: m._atomic_secret(link,b"x"); assert False
        except OSError: pass
        bad=mock.Mock(returncode=0,stdout="no token",stderr="")
        with mock.patch.object(m.subprocess,"run",return_value=bad): assert m.capture_claude(root/"x")["status"]=="malformed"
        seen=[]
        def fake(cmd,**kw):
            seen.append((cmd,kw)); return mock.Mock(returncode=0,stdout="",stderr="")
        with mock.patch.object(m.subprocess,"run",side_effect=fake): r=m.github_probe("o/r",env={"GITHUB_PAT":"SECRET","X":"1"})
        assert r["status"]=="passed" and len(seen)==2
        assert all("SECRET" not in repr(x[0]) and x[1]["env"]["GH_TOKEN"]=="SECRET" and "GITHUB_PAT" not in x[1]["env"] for x in seen)
        assert m.github_probe("o/r",env={})["status"]=="missing"
        with mock.patch.object(m.subprocess,"run",side_effect=m.subprocess.TimeoutExpired("gh",1)): assert m.github_probe("o/r",env={"GITHUB_PAT":"S"})["status"]=="network_error"
        assert m.tl_bootstrap("cowork",None,env={})["status"]=="missing"
    print("PASS session_credentials_test")
if __name__ == "__main__": run()
