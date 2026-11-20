import ast, collections, hashlib, json, os, subprocess, sys, time
from pathlib import Path
from review_measure import W,R,C,save,sha
Q=R/'ops/reviews/wp1236-r10-soan/quet_dot_bien.py'; D=R/'ops/reviews/wp1236-r10-soan'; SRC=C/'ops/gate_output_doi_chieu.py'
(W/'tmp').mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp'))
receipts=[]
for name,args in [('m1',['sinh',str(SRC),'--ra',str(W/'m1.jsonl')]),('m2',['sinh',str(SRC),'--ra',str(W/'m2.jsonl')]),('h',['hoi-quy',str(D/'kho_dot_bien_reviewer_luot6.jsonl'),'-',str(SRC),'--ra',str(W/'h.jsonl')])]:
 t=time.monotonic(); cmd=[sys.executable,'-B',str(Q),*args];p=subprocess.run(cmd,capture_output=True,env=env,cwd=W)
 (W/f'{name}.stdout').write_bytes(p.stdout);(W/f'{name}.stderr').write_bytes(p.stderr)
 receipts.append({'command':cmd,'rc':p.returncode,'stdout_sha256':sha(p.stdout),'seconds':time.monotonic()-t});print(name,p.returncode,p.stdout.decode().strip(),flush=True)
 assert p.returncode==0
save('generation_receipts.json',receipts)
M=[json.loads(x) for x in (W/'m1.jsonl').read_text().splitlines()]; H=[json.loads(x) for x in (W/'h.jsonl').read_text().splitlines()]; P=[json.loads(x) for x in (D/'pilot_c2d606b_kq.jsonl').read_text().splitlines()]
rows={x['id']:x for x in M+H}; pilot={x['id']:x for x in P}
ref='refs/remotes/origin/ops/wp1236-r9-a-lease:ops/reviews/wp1236-a-r9-ma-6-codex/'
for n in ['measurement_summary.json','equivalence.json','all_independent_results.json','independent_final.json','make_independent.py','make_extra.py','make_order_url.py','complete_reason_sweep.py','MANIFEST_SANDBOX.sha256']:
 p=subprocess.run(['git','-C',str(R),'show',ref+n],capture_output=True);assert p.returncode==0
 (W/n).write_bytes(p.stdout)
summary=json.loads((W/'measurement_summary.json').read_text())
# All 34 regression survivors include the 25 non-equivalent and nine equivalents.
selection=[x for x in H if not pilot[x['id']]['giet']]
selected={x['id'] for x in selection}
# At least one killed mutant per generated operator plus every error-only case.
for op in sorted({x['op'] for x in M}):
 matches=[x for x in M if x['op']==op and pilot[x['id']]['giet']]
 if matches: selection.append(matches[0]); selected.add(matches[0]['id'])
for x in M+H:
 if not pilot[x['id']]['giet'] and pilot[x['id']]['hong'] and x['id'] not in selected:selection.append(x);selected.add(x['id'])
(W/'pilot_subset.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in selection))
out={'deterministic_bytes':(W/'m1.jsonl').read_bytes()==(W/'m2.jsonl').read_bytes(),'m_sha256':sha((W/'m1.jsonl').read_bytes()),'manifest':len(M),'regressions':len(H),'applied':sum('src' in x for x in H),'pilot_count':len(P),'ids_match':set(rows)==set(pilot),'hash_mismatches':[k for k in rows if rows[k]['sha256']!=pilot[k]['sha256']],'classification':dict(collections.Counter('GIET' if x['giet'] else 'HONG' if x['hong'] else 'SONG_SACH' for x in P)),'rc_nonzero':[x for x in P if x['rc']],'kills_after_hong':[x for x in P if x['giet'] and x['hong']],'subset_count':len(selection),'subset_ids':[x['id'] for x in selection],'per_op':dict(collections.Counter(x['op'] for x in M))}
save('generation_audit.json',out)
print('GENERATION_AUDIT_COMPLETE',json.dumps({k:v for k,v in out.items() if k not in ['subset_ids','kills_after_hong']},ensure_ascii=False),flush=True)
