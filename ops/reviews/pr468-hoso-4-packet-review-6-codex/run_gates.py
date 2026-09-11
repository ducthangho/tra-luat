from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import datetime, json, os, subprocess, sys, time
BASE=Path(__file__).resolve().parents[1]; ROOT=BASE/'cay-kho'; OUT=BASE/'do-review'
CASES={
 'doctrine-scan':[sys.executable,'.claude/dev/packet_loop.py','doctrine-scan','--root','.'],
 'adr-song':[sys.executable,'.claude/dev/packet_loop.py','adr-song'],
 'doc-claims':[sys.executable,'scripts/tl.py','doc-claims-check','--strict','--json'],
 'ci-dang-ky':[sys.executable,'.claude/dev/ci_dang_ky_test.py'],
 'lease-check':[sys.executable,'ops/lease_publish.py','check','ops/leases/gate-tach-job-cat-chi-phi-exec-1-claude-20260906.yaml'],
 'lease-holder-ci':[sys.executable,'ops/lease_publish.py','ai-dang-giu','.github/workflows/ci.yml'],
 'lease-holder-registry':[sys.executable,'ops/lease_publish.py','ai-dang-giu','.claude/dev/ci_dang_ky_test.py'],
}
def run(k):
 t=time.monotonic(); start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.run(CASES[k],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'TMPDIR':str(OUT/'tmp'),'GIT_ALLOW_PROTOCOL':'file'},timeout=240)
 (OUT/(k+'.log')).write_text(p.stdout+p.stderr)
 row={'name':k,'command':CASES[k],'start_utc':start,'seconds':time.monotonic()-t,'rc':p.returncode}
 (OUT/(k+'.json')).write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(row,ensure_ascii=False),flush=True)
with ThreadPoolExecutor(max_workers=3) as pool: list(pool.map(run, CASES))
