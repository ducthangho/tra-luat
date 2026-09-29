from pathlib import Path
import subprocess, json, os, datetime, hashlib

ROOT = Path(__file__).resolve().parents[1]
TREE = ROOT / 'cay-kho'
OUT = ROOT / 'do-review10'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

def run(args, cwd=TREE):
    if args == ['git', 'ls-remote', '--heads', 'origin']:
        args = ['git', 'ls-remote', '--heads', str(ROOT / 'kho.git')]
    p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=55)
    return {'argv': args, 'cwd': str(cwd.relative_to(ROOT)), 'rc': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}

result = {'measured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'scope': 'Offline sandbox snapshot only. ls-remote receives the absolute local kho.git path. Lease CLI measurements are in leases.json.'}
result['git'] = {key: run(['git', *args]) for key,args in {
    'head':['rev-parse','HEAD'], 'tree':['rev-parse','HEAD^{tree}'],
    'status':['status','--porcelain'], 'diff_numstat':['diff','--numstat','0bc6e56..c43347d'],
    'refs':['for-each-ref','--format=%(refname) %(objectname)','refs/heads','refs/remotes'],
    'snapshot_heads':['ls-remote','--heads','origin']}.items()}
result['manifests'] = []
for manifest in sorted((TREE / 'ops/reviews').rglob('*.sha256')):
    check = run(['sha256sum','--check',manifest.name], manifest.parent)
    check['path'] = str(manifest.relative_to(TREE))
    check['ok'] = sum(line.endswith(': OK') for line in check['stdout'].splitlines())
    check['entries'] = len(manifest.read_text().splitlines())
    check['manifest_sha256'] = hashlib.sha256(manifest.read_bytes()).hexdigest()
    result['manifests'].append(check)
(OUT / 'static.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'measured_at_utc':result['measured_at_utc'],
    'manifests':[{k:r[k] for k in ['path','rc','ok','entries']} for r in result['manifests']]},ensure_ascii=False,indent=2))
