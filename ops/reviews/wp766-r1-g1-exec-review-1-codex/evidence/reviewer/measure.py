"""Keep the review commands and their actual outputs outside the reviewed tree."""
import datetime
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

OUT = Path(__file__).resolve().parent
LOG = OUT / "evidence"
LOG.mkdir(exist_ok=True)
label, cwd, *argv = sys.argv[1:]
if argv and argv[0] == "--":
    argv.pop(0)
record = {"label": label, "cwd": cwd, "argv": argv,
          "command": shlex.join(argv), "started": datetime.datetime.now(datetime.UTC).isoformat()}
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1")
with (LOG / f"{label}.log").open("w", encoding="utf-8") as stream:
    result = subprocess.run(argv, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT)
record.update(rc=result.returncode, finished=datetime.datetime.now(datetime.UTC).isoformat(),
              output=f"evidence/{label}.log")
with (LOG / "commands.jsonl").open("a", encoding="utf-8") as stream:
    stream.write(json.dumps(record, ensure_ascii=False) + "\n")
print(json.dumps(record, ensure_ascii=False), flush=True)
lines = (LOG / f"{label}.log").read_text(encoding="utf-8", errors="replace").splitlines()
print("\n".join(lines[-22:]), flush=True)
sys.exit(result.returncode if result.returncode >= 0 else 1)
