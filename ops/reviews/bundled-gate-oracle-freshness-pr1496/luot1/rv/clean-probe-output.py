"""Dọn đúng tệp ignored do các phép đo sinh trong clone reviewer."""
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
HEADS = {
    "nen": "e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8",
    "sau": "4f648e5b784aa4e19f0385eee68cd75e69e1dd18",
}
PREFIXES = ("references/golden/fixtures/", "scripts/.tl_state/")


def git(repo, *args):
    return subprocess.check_output(["git", "--no-optional-locks", "-C", str(repo), *args])


def outputs():
    result = []
    for lane, expected in HEADS.items():
        repo = ROOT / lane
        assert git(repo, "rev-parse", "HEAD").decode().strip() == expected
        status = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignored")
        for raw in status.split(b"\0"):
            if not raw:
                continue
            entry = os.fsdecode(raw)
            assert entry.startswith("!! "), entry
            rel = entry[3:]
            assert rel.startswith(PREFIXES), rel
            path = repo / rel
            assert path.resolve() == path and path.is_file(), path
            result.append((lane, path))
    return result


for lane, path in outputs():
    print(f"{lane}: {path.relative_to(ROOT / lane)}")
    path.unlink()
