from pathlib import Path
import json, shutil, subprocess, argparse

r = Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('--prototype',action='store_true'); a=ap.parse_args()
label='-prototype' if a.prototype else ''
out = []
for mode in ['check-zip-control', 'check-zip-outdated', 'check-zip-missing-rg', 'check-zip-rc9']:
    fixture = r/'fixtures'/(mode+label)
    log = r/'evidence'/(mode+label+'.json')
    cmd = [str(r/'pwsh/pwsh'), '-NoProfile', '-File', str(r/'probes/portable-check.ps1'),
           '-Mode', mode, '-Log', str(log), '-FixtureRoot', str(fixture)]
    if a.prototype: cmd += ['-Product',str(r/'hint-prototype/ops/vm/cap-nhat-cong-cu.ps1')]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
    (r/'evidence'/(mode+label+'.log')).write_text(p.stdout+p.stderr)
    d = json.loads(log.read_text()) if log.exists() else None
    events = [json.loads(x) for x in (fixture/'native.jsonl').read_text().splitlines()] if (fixture/'native.jsonl').exists() else []
    rows = {x['cong_cu']:x for x in d['ket_qua']} if d else {}
    targets = ['rg', 'shellcheck', 'actionlint'] if mode=='check-zip-rc9' else ['rg']
    control = mode in ['check-zip-control', 'check-zip-outdated']
    ok = bool(d and d['tong']==11 and d['ok']==control and
              p.returncode==(0 if control else 1) and
              (all(rows[x]['hanh_dong']=='loi' for x in targets) if not control else d['loi']==0))
    summary = dict(mode=mode, passed=ok, rc=p.returncode, ok=d['ok'] if d else None,
                   errors=d['loi'] if d else None, rows=d['tong'] if d else None,
                   portable={x:rows[x] for x in ['rg', 'shellcheck', 'actionlint']} if d else None,
                   installs=sum('install' in x['argv'] for x in events))
    out.append(dict(command=cmd, summary=summary, data=d, events=events))
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    shutil.rmtree(fixture)
(r/('evidence/portable-check-oracle'+label+'.json')).write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(f"Portable ChiKiem oracle: {sum(x['summary']['passed'] for x in out)}/{len(out)} PASS")
raise SystemExit(0 if all(x['summary']['passed'] for x in out) else 1)
