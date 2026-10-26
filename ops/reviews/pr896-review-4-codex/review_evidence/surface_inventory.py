import hashlib, json, re
from pathlib import Path
import yaml
root = Path('cay-kho')
rd = root/'ops/reviews'
receipts = {}
for p in rd.glob('*.receipt.yaml'):
    d = yaml.safe_load(p.read_text())
    receipts[d['verdict_path']] = d
files = sorted(set(rd.rglob('*-verdict.md')) | set(rd.rglob('VERDICT.md')))
pattern = re.compile(r'codex_service|codex service|service/api|execution.surface|bề mặt|be mat|surface:', re.I)
explicit = re.compile(r'codex_service|codex service|service/api', re.I)
seen = {}
for p in files:
    raw = p.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    seen.setdefault(digest, []).append(p)
print('verdict_files=', len(files), 'distinct_content=', len(seen))
for group in seen.values():
    p = next((p for p in group if p.name.endswith('-verdict.md')), group[0])
    lines = p.read_text().splitlines()
    found = [(i,l) for i,l in enumerate(lines,1) if pattern.search(l) and (i <= 35 or explicit.search(l))]
    if not found:
        continue
    d = receipts.get(str(p.relative_to(root)), {})
    c = d.get('verdict_usage_caveats') or []
    ids = [x.get('id') for x in c if re.search('SURFACE|surface|BE-MAT|be-mat|RUNTIME|runtime', x.get('id',''))]
    print('\nFILE',p,'copies=',len(group), 'receipt_surface=',d.get('model_reviewer_identity',{}).get('surface'), 'caveats=',ids)
    for i,l in found:
        print(str(i)+': '+l[:400])
runs = []
for p in root.rglob('run.json'):
    try:
        r=json.loads(p.read_text()); runs.append((p,r))
    except (OSError,ValueError):
        pass
compared=0
for p,d in receipts.items():
    identity=d.get('model_reviewer_identity') or {}
    rid=str(identity.get('session_run_id',''))
    if not rid: continue
    matching=[(q,r) for q,r in runs if str(r.get('run_id','')).startswith(rid)]
    for q,r in matching:
        compared+=1
        if identity.get('surface') != r.get('execution_surface'):
            print('RECEIPT_RUNTIME_DIFFERENCE',p,identity.get('surface'),q,r.get('execution_surface'))
print('\nreceipt_runtime_pairs_compared=',compared)
