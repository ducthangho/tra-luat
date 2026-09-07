import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

B = Path(__file__).resolve().parents[1]
O = B / 'do-review10'
temp = O / 'tmp'
temp.mkdir(exist_ok=True)
name, *command = sys.argv[1:]
env = dict(os.environ, TMPDIR=str(temp), PYTHONDONTWRITEBYTECODE='1')
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
clock = time.monotonic()
result = subprocess.run(command, cwd=B / 'cay-kho', env=env, capture_output=True)
metadata = dict(name=name, command=command, cwd='cay-kho', utc=started,
                rc=result.returncode, seconds=time.monotonic() - clock)
for channel in ['stdout', 'stderr']:
    raw = getattr(result, channel)
    (O / f'{name}.{channel}').write_bytes(raw)
    metadata[channel + '_bytes'] = len(raw)
    metadata[channel + '_sha256'] = hashlib.sha256(raw).hexdigest()
(O / f'{name}.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(metadata, ensure_ascii=False))
