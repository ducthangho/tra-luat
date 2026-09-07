import ast, contextlib, io, json, pathlib, re, subprocess, types
from harness import BASE, ROOT, OUT, C, H, BASE_MOI, replay
result={}
# Historical formatter counts are independent of H; current captured green output can be measured.
real=json.loads((OUT/'real-results.json').read_text())
rerun=json.loads((OUT/'nhanh-rerun.json').read_text())
result['formatter_measurements']=[]
for row in real:
    p=row['path'];f=OUT/row['output'];z=row
    if p==rerun['path']:
        f=OUT/'outputs/nhanh_don_duoc_test.rerun.stdout';z=rerun
    text=f.read_text(); m=re.search(BASE_MOI[p],text,re.M)
    result['formatter_measurements'].append({'path':p,'rc':z['rc'],'H_red':z['H_red'],'span_chars':len(m[0]) if m else None,'span_utf8_bytes':len(m[0].encode()) if m else None,'groups':re.compile(BASE_MOI[p]).groups,
     'pairs_in_span':len(re.findall(r'\d+/\d+',m[0])) if m else None,
     'captured_pairs_in_TONG':sum(re.compile(g).groups//2 for _,g in H['TONG'][p])})
# Mutation checks on the SAME attack corpus, not the unprovided 311 historic rows.
rows=json.loads((OUT/'attack-h-cases.json').read_text())
src=(OUT/'h_predicate.py').read_text()
mutants={'no_positions':('if covered != actual:', 'if False:'), 'no_unique':('if len(hits) != 1:', 'if not hits:'),
  'no_positive':('int(a) == int(b) > 0','int(a) == int(b)'), 'remove_dead_bool':('return bool(cap) and all(', 'return all(')}
mutations=[]
for name,(before,after) in mutants.items():
    assert before in src
    ns={'re':re};exec(src.replace(before,after),ns)
    old=C.bang_chung_xanh;C.bang_chung_xanh=ns['bang_chung_xanh']
    changed=[];exceptions=[]
    try:
        for i,row in enumerate(rows):
            try: got=replay(row['path'],row['text'],mau=row['mau'],windows=row['windows'])
            except Exception as e: exceptions.append({'case':row['name'],'exception':type(e).__name__}); continue
            if got!=row['actual_red']: changed.append(row['name'])
    finally:C.bang_chung_xanh=old
    mutations.append({'name':name,'changed_count':len(changed),'changed_cases':changed,'exception_count':len(exceptions),'exceptions':exceptions})
result['mutants_on_1213']=mutations
# Compare old/more recent samples' scope, not a substitute for absent timing records.
commits=['8ce02fd','82e01a4','1b3caa1','c0f18ac','28cb898','b912e5f','cacaba3','d28c4b1','62a6385','771c6ed','0c3405f']
import yaml
result['job_workload_at_11_heads']=[]
for rev in commits:
    raw=subprocess.check_output(['git','show',rev+':.github/workflows/ci.yml'],cwd=ROOT,text=True)
    steps=yaml.safe_load(raw)['jobs']['gate']['steps']
    result['job_workload_at_11_heads'].append({'sha':rev,'steps':len(steps),'has_receipt_v2':any('bien-nhan v2' in s.get('name','') for s in steps)})
(OUT/'extra-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'formatters':result['formatter_measurements'], 'mutants':[{k:v for k,v in m.items() if k not in ('changed_cases','exceptions')} for m in mutations], 'workloads':result['job_workload_at_11_heads']},ensure_ascii=False,indent=2))
