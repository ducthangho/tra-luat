import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

work = Path(__file__).resolve().parent
repo = work.parent / 'repo'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work))
commands = [
    [sys.executable, '-B', 'ops/land_evidence_nguon.py', '--root', '.'],
    [sys.executable, '-B', 'ops/kiem_ho_so_land.py', '--root', '.'],
    [sys.executable, '-B', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
]

def run(pair):
    i, cmd = pair
    p = subprocess.run(cmd, cwd=repo, env=env, capture_output=True, timeout=90)
    raw = p.stdout + p.stderr
    (work / f'check-{i}.log').write_bytes(raw)
    return {'command': cmd, 'rc': p.returncode, 'sha256': hashlib.sha256(raw).hexdigest(), 'tail': raw.decode().splitlines()[-2:]}

with concurrent.futures.ThreadPoolExecutor() as ex:
    out = {'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'checks':list(ex.map(run, enumerate(commands)))}
(work / 'checks.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(json.dumps(out, ensure_ascii=False, indent=2))
