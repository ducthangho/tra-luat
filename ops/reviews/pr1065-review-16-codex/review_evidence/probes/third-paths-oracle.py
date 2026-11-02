from pathlib import Path
import json, shutil, subprocess, argparse

r = Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('--prototype',action='store_true'); a=ap.parse_args()
label='-prototype' if a.prototype else ''
out = []
for mode in ['check-only', 'check-missing-venv', 'check-venv-rc9',
             'check-venv-cannot-start', 'venv-rc9', 'venv-cannot-start']:
    fixture = r/'fixtures'/('third'+label+'-'+mode)
    log = r/'evidence'/('third'+label+'-'+mode+'.json')
    cmd = [str(r/'pwsh/pwsh'), '-NoProfile', '-File', str(r/'probes/third-paths.ps1'),
           '-Mode', mode, '-Log', str(log), '-FixtureRoot', str(fixture)]
    if a.prototype: cmd += ['-Product',str(r/'hint-prototype/ops/vm/cap-nhat-cong-cu.ps1')]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
    (r/'evidence'/('third'+label+'-'+mode+'.log')).write_text(p.stdout+p.stderr)
    d = json.loads(log.read_text()) if log.exists() else None
    pre = json.loads((fixture/'precheck.json').read_text()) if (fixture/'precheck.json').exists() else None
    events = [json.loads(x) for x in (fixture/'native.jsonl').read_text().splitlines()] if (fixture/'native.jsonl').exists() else []
    venv = next((x for x in d['ket_qua'] if x['cong_cu']=='venv-kho'), {}) if d else {}
    control = mode=='check-only'
    fixture_valid = pre is None if control or mode=='check-missing-venv' else bool(pre and pre['exists'] and (pre['rc']==9 if mode.endswith('rc9') else pre['error']))
    ok = bool(fixture_valid and d and d['tong']==11 and d['ok']==control and
              d['loi']==(0 if control else 1) and p.returncode==(0 if control else 1) and
              venv.get('hanh_dong')==('kiem' if control else 'loi'))
    summary = dict(mode=mode, passed=ok, rc=p.returncode, ok=d['ok'] if d else None,
                   errors=d['loi'] if d else None, rows=d['tong'] if d else None,
                   venv=venv.get('hanh_dong'), direct_probe=pre,
                   venv_native_calls=sum('/venv/' in x['exe'] for x in events),
                   installs=sum('install' in x['argv'] for x in events))
    out.append(dict(command=cmd, summary=summary, data=d, events=events))
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    shutil.rmtree(fixture)
(r/('evidence/third-paths-oracle'+label+'.json')).write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(f"Venv runtime oracle: {sum(x['summary']['passed'] for x in out)}/{len(out)} PASS")
raise SystemExit(0 if all(x['summary']['passed'] for x in out) else 1)
