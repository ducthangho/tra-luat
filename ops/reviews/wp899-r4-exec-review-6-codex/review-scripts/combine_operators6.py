from pathlib import Path
import json,collections
R=Path('.review');a=json.loads((R/'operators6/results.json').read_text());extra=json.loads((R/'operator-errors6-results.json').read_text());by=collections.defaultdict(list)
for r in extra:by[r['name']].append(r)
for r in a:
 r['additional_error_probes']=by[r['name']]
 if any(z['rank']=='TIN_DUNG_GIA' for z in r['additional_error_probes']):r['rank']='GIET+NEM'
 r['measurement_scope']='original exact target (or signature-changed fallback targets) plus only kq8-listed error cases, max3 per operator; not all49 per operator'
(R/'operators6-combined.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));print(len(a),dict(collections.Counter(r['rank'] for r in a)))
