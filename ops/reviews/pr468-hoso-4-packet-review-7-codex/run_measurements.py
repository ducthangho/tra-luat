import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

BASE = pathlib.Path(__file__).resolve().parents[1]
ROOT = BASE / 'cay-kho'
OUT = BASE / 'do-review7'
TMP = OUT / 'tmp'
TMP.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(TMP), TMP=str(TMP), TEMP=str(TMP),
           PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
           GIT_ALLOW_PROTOCOL='file')

groups = {
    'lease-rerun': [('lease-publish-test-rerun', ['ops/lease_publish_test.py'])],
    'real': [('pretooluse', ['.claude/hooks/pretooluse_guard_test.py']),
             ('mcp-gh', ['.claude/dev/mcp_gh_test.py'])],
    'gates': [('doctrine-scan', ['.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.']),
              ('adr-song', ['.claude/dev/packet_loop.py', 'adr-song', '--root', '.']),
              ('doc-claims', ['scripts/tl.py', 'doc-claims-check', '--strict', '--json']),
              ('ci-dang-ky', ['.claude/dev/ci_dang_ky_test.py']),
              ('lease-publish-test', ['ops/lease_publish_test.py']),
              ('bien-nhan-v2', ['ops/bien_nhan_v2.py', '--root', '.']),
              ('lease-check', ['ops/lease_publish.py', 'check', 'ops/leases/gate-tach-job-cat-chi-phi-exec-1-claude-20260906.yaml'])],
}
rows = []
for name, args in groups[sys.argv[1]]:
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print('START', name, start, flush=True)
    t = time.monotonic()
    with (OUT / (name + '.stdout')).open('wb') as stdout, (OUT / (name + '.stderr')).open('wb') as stderr:
        p = subprocess.run([sys.executable, '-B', *args], cwd=ROOT, env=env,
                           stdout=stdout, stderr=stderr, timeout=1000)
    data = (OUT / (name + '.stdout')).read_bytes()
    row = dict(name=name, command=[sys.executable, '-B', *args], start_utc=start,
               seconds=round(time.monotonic() - t, 3), rc=p.returncode,
               bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    rows.append(row)
    (OUT / (sys.argv[1] + '-results.json')).write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(row, ensure_ascii=False), flush=True)
