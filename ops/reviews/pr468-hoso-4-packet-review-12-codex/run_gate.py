import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import time

B = Path(__file__).resolve().parents[1]
O = B / 'do-review12'
env = dict(os.environ, TMPDIR=str(O / 'tmp'), PYTHONDONTWRITEBYTECODE='1')
name, *cmd = sys.argv[1:]
start = dt.datetime.now(dt.timezone.utc)
t = time.monotonic()
p = subprocess.run(cmd, cwd=B / 'cay-kho', env=env, capture_output=True)
(O / f'{name}.stdout').write_bytes(p.stdout)
(O / f'{name}.stderr').write_bytes(p.stderr)
data = {'command': cmd, 'cwd': 'cay-kho', 'started_utc': start.isoformat(),
        'ended_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'elapsed_seconds': time.monotonic() - t, 'rc': p.returncode,
        'stdout_bytes': len(p.stdout), 'stderr_bytes': len(p.stderr)}
(O / f'{name}.json').write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps(data))
print(p.stdout.decode(errors='replace')[-2000:])
print(p.stderr.decode(errors='replace')[-1000:])
