from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import yaml
from audit import BASE, ROOT, record

receipts = [(p, yaml.safe_load(p.read_text())) for p in sorted((ROOT / 'ops/reviews').glob('*.receipt.yaml'))]
readme = (ROOT / 'ops/reviews/README.md').read_text().splitlines()
runtime = []
parse_errors = []
for p in sorted(ROOT.rglob('run.json')):
    try:
        runtime.append((p, json.loads(p.read_text())))
    except Exception as e:
        parse_errors.append([str(p.relative_to(ROOT)), str(e)])

def matching(ids):
    return [(p,d) for p,d in runtime if any(re.fullmatch('[0-9a-f]{8,40}', str(i)) and (str(d.get('run_id','')).startswith(str(i)) or str(i).startswith(str(d.get('run_id','')))) for i in ids if d.get('run_id'))]

service = []
runtime_pairs = []
all_claims = []
for p,d in receipts:
    v = ROOT / d['verdict_path']
    lines = v.read_text().splitlines()
    name = v.name
    identity = d.get('model_reviewer_identity', {})
    ids = [value for key,value in identity.items() if key in ['session_run_id', 'run_id', 'run_id_day_du', 'session_id']]
    matches = matching(ids)
    for rp,rd in matches:
        runtime_pairs.append({'receipt': p.name, 'run': str(rp.relative_to(ROOT)), 'run_id': rd.get('run_id'), 'receipt_surface': identity.get('surface'), 'runtime_surface': rd.get('execution_surface'), 'same_surface': identity.get('surface') == rd.get('execution_surface')})
    hits = [(i,l) for i,l in enumerate(lines,1) if re.search(r'codex.service|service/API', l, re.I)]
    # Four review reports quote findings about others. Read those separately instead of treating the quotes as identity.
    finding_only = name in ['pr896-review-2-codex-verdict.md', 'pr896-review-3-codex-verdict.md', 'pr896-review-4-codex-verdict.md', 'pr915-review-1-codex-verdict.md']
    if hits:
        all_claims.append({'verdict': str(v.relative_to(ROOT)), 'finding_only': finding_only, 'hits': hits})
    if not hits or finding_only:
        continue
    # pr460 also mentions surface while describing a finding; its identity is the first hit.
    i,line = hits[0]
    caveats = d.get('verdict_usage_caveats', [])
    text = yaml.safe_dump(caveats, allow_unicode=True)
    has_caveat = any('SURFACE' in c.get('id','') or 'RUNTIME-KHONG-DO-DUOC' in c.get('id','') for c in caveats)
    supplement = None
    if name == 'slice-b-c-review-2-codex-verdict.md':
        ids.append('8ddb0c6f')
        matches = matching(ids)
        legacy = yaml.safe_load((ROOT / 'ops/reviews/pr896-review-4-legacy-caveats.yaml').read_text())
        supplement = next(c for c in legacy['caveats'] if c['verdict_path'] == d['verdict_path'])
        has_caveat = True
    idc = 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC'
    c = next((c for c in caveats if c.get('id') == idc), supplement)
    check = None
    if c:
        desc = c.get('mo_ta', c.get('noi_dung', ''))
        row = [l for l in readme if l.startswith('| `' + name + '` | `' + idc + '` |')]
        lineno = int(re.search(r'Verdict dong (\d+)', desc)[1])
        check = {'declared_line': lineno, 'line_matches_service_claim': any(x[0]==lineno for x in hits), 'run_ids': ids, 'run_ids_mentioned': any(str(x) in desc for x in ids), 'matching_runtime_files': [str(p.relative_to(ROOT)) for p,_ in matches], 'readme_rows': len(row), 'readme_description_matches': len(row) == 1 and desc in row[0]}
    service.append({'verdict': name, 'line': i, 'self_claim': line, 'receipt_surface': identity.get('surface'), 'has_caveat': has_caveat, 'condition': check, 'runtime_files': [str(p.relative_to(ROOT)) for p,_ in matches]})

verdicts = list((ROOT / 'ops/reviews').rglob('*-verdict.md')) + list((ROOT / 'ops/reviews').rglob('VERDICT.md'))
details = {'service_self_claims': service, 'all_service_mentions': all_claims, 'runtime_pairs': runtime_pairs, 'parse_errors': parse_errors}
(BASE / 'surfaces.json').write_text(json.dumps(details,ensure_ascii=False,indent=2)+'\n')
summary = [f'verdict_files={len(verdicts)} distinct_content={len({hashlib.sha256(p.read_bytes()).hexdigest() for p in verdicts})}', f'run_json_files={len(runtime)} parse_errors={parse_errors}', f'receipt_runtime_pairs={len(runtime_pairs)} surface_mismatches={[x for x in runtime_pairs if not x["same_surface"]]}', f'service_self_claims={len(service)} missing_caveat={[x["verdict"] for x in service if not x["has_caveat"]]}']
for x in service:
    summary.append(x['verdict']+':'+str(x['line'])+' receipt_surface='+str(x['receipt_surface'])+' has_caveat='+str(x['has_caveat'])+(' condition='+json.dumps(x['condition'],ensure_ascii=False) if x['condition'] else ' runtime_files='+str(x['runtime_files'])))
record('HƯỚNG 8 - tu khai execution surface', 'PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/surfaces.py; rg -n -i "codex.service|service/api|execution.surface|bề mặt|surface:" cay-kho/ops/reviews --glob "*-verdict.md" --glob "VERDICT.md"', '\n'.join(summary), 'KHÔNG PHẢI LỖI mới trong các tự khai đã tìm: hai thể hiện P2 cũ nay có đính chính và hàng README. Chỉ nhắc service khi mô tả finding không được tính là tự khai; API/shell chung không tự phủ nhận CLI. Không có run đúng ID cho 15 caveat thiếu runtime, không tự chọn surface thực tế; chi tiết từng câu ở surfaces.json và surface-text.log.')
