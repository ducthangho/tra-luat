"""Mô hình hẹp các vị từ mới trong đặc tả; không thay cho test mã A1/D chưa có."""
from collections import Counter
import copy
import json
import re
from pathlib import Path
from measure import BASE, ROOT, OUT, save
import yaml

def la_run_land(provenance):
    run=provenance.get('moc',{}).get('run',{})
    return run.get('loi_khai_rest_path')=='.github/workflows/ci.yml' and run.get('event')=='push'

def tap_head_land(doc):
    values=[doc.get('merge_commit')]+[p.get('merge_commit') for p in doc.get('prs',[]) if isinstance(p,dict)]
    return {v for v in values if isinstance(v,str) and re.fullmatch('[0-9a-f]{40}',v)}

files=json.loads((OUT/'census.json').read_text())['files']
counts=Counter()
changed=[]
for entry in files:
    p=yaml.safe_load((ROOT/entry['file']).read_bytes())
    is_land=la_run_land(p)
    no_event=p['moc']['run']['loi_khai_rest_path']=='.github/workflows/ci.yml'
    counts['la_run_land_true' if is_land else 'la_run_land_false']+=1
    if is_land!=no_event:
        changed.append(entry['file'])

heads=[]
for p in (ROOT/'ops/land').glob('*-land-evidence.yaml'):
    doc=yaml.safe_load(p.read_bytes())
    if doc.get('prs'):
        h=tap_head_land(doc)
        heads.append({'file':p.name,'H':sorted(h),'root_only_count':int(isinstance(doc.get('merge_commit'),str) and bool(re.fullmatch('[0-9a-f]{40}',doc['merge_commit'])))})

# Giữ tiền đề D10: kiem == passed, run/attempt/head cùng biên bản;
# chỉ đánh giá chốt la_run_land mới, không sinh hồ sơ chứng cứ hay M8 giả.
valid=copy.deepcopy(yaml.safe_load((ROOT/'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_bytes()))
d10=[]
for event in ('push','workflow_dispatch'):
    valid['moc']['run']['event']=event
    d10.append({'event':event,'d2b_model_rc':0 if la_run_land(valid) else 12,'without_la_run_land_model_rc':0})

quick=json.loads((ROOT/'ops/land/pr1055-wp1052-provenance/readback-jobs-41397205258.json').read_text())
jobs=quick['jobs'] if isinstance(quick,dict) else quick
quick_j=[j for j in jobs if j['conclusion']!='skipped' and 'ubuntu-latest' in j['labels'] and j['name']!='chuan-bi']
gate_loop=next(j for j in quick_j if j['name'].startswith('gate-packet-loop'))
full=yaml.safe_load((ROOT/'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_bytes())
full_job=next(j for j in full['moc']['gate_output']['jobs'] if j['name']==gate_loop['name'])
missing=[b['name'] for b in full_job['buoc'] if b['conclusion']=='success' and 'packet-loop selftest' in b['name']
         and not any(x['name']==b['name'] and x['conclusion']=='success' for x in gate_loop['steps'])]
result=save('contracts',{'kind':'spec_contract_model_not_implementation','classification':dict(counts),
                        'without_event_changes':changed,'head_union':heads,'d10':d10,
                        'quick_run':{'J':len(quick_j),'missing_day_du_step':missing}})
print(json.dumps(result,ensure_ascii=False,indent=2))
