import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
env = dict(os.environ, REVIEW_REAL_NODE='/opt/node22/bin/node')
for limit in (32767, 32768):
    args = [str(root / 'bin/node'), '-e', "process.stdout.write('OK')", 'x']
    before = len(subprocess.list2cmdline(args).encode('utf-16-le')) // 2 + 1
    args[-1] += 'x' * (limit - before)
    measured = len(subprocess.list2cmdline(args).encode('utf-16-le')) // 2 + 1
    result = subprocess.run(args, env=env, capture_output=True, timeout=60)
    print('units=' + str(measured), 'rc=' + str(result.returncode),
          'stdout=' + repr(result.stdout.decode()), 'stderr=' + repr(result.stderr.decode()))
    assert result.returncode == (0 if limit == 32767 else 206)
print('WRAPPER_BOUNDARIES=PASS')
