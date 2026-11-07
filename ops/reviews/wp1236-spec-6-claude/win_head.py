import yaml
from pathlib import Path
for p in sorted(Path('ops/land').rglob('*.yaml')):
    try: x = yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception: continue
    if not (isinstance(x, dict) and x.get('schema') == 'ci_provenance/1'): continue
    r = x['moc']['run']
    if r['loi_khai_rest_path'].endswith('ci.yml') and r['event'] == 'push': continue
    hs = p.relative_to('ops/land').parts[0].removesuffix('-provenance')
    ev = Path('ops/land') / f'{hs}-land-evidence.yaml'
    e = yaml.safe_load(ev.read_text(encoding='utf-8')) if ev.exists() else {}
    H = {e.get('merge_commit')} | {q.get('merge_commit') for q in (e.get('prs') or []) if isinstance(q, dict)}
    H.discard(None)
    print(f"{hs:45} {r['loi_khai_rest_path'].split('/')[-1]:22} {r['event']:18} run={r['run_id']} head_in_H={r['head_sha'] in H}")
