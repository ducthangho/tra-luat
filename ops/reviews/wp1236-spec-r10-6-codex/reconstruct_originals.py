import json,sys,subprocess,collections
from review_measure import W,R,C,save,sha
O=W/'reconstructed';O.mkdir(exist_ok=True);src=C/'ops/gate_output_doi_chieu.py'
receipts=[]
for n in ['make_independent.py','make_extra.py','make_order_url.py','complete_reason_sweep.py']:
 s=(W/n).read_text().replace("w.parent/'repo/ops/gate_output_doi_chieu.py'",repr(str(src)))
 # Parentheses around the original pathlib expression now need a Path value.
 s=s.replace('('+repr(str(src))+').read_text()', 'pathlib.Path('+repr(str(src))+').read_text()')
 if n=='complete_reason_sweep.py':
  # Duplicate corrected identities do not affect the seen-AST set; reconstruct their exact rows from prior inventory.
  inv=json.loads((R/'ops/reviews/wp1236-spec-r10-5-codex/replay_inventory.json').read_text()); ids={x['id'] for x in inv['duplicate_ids']}
  rows=[json.loads(x) for x in (O/'independent_mutants.jsonl').read_text().splitlines()];(O/'independent_corrected.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows if x['id'] in ids))
 (O/n).write_text(s);p=subprocess.run([sys.executable,'-B',str(O/n)],cwd=O,capture_output=True);receipts.append({'script':n,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()});print(n,p.returncode,p.stdout.decode(),flush=True)
 assert p.returncode==0
rows={};count=0
for n in ['independent_mutants.jsonl','independent_corrected.jsonl','extra_mutants.jsonl','order_url_mutants.jsonl','reason_complete_mutants.jsonl']:
 for l in (O/n).read_text().splitlines():
  x=json.loads(l);count+=1;rows[x['id']]=x
H={x['id'].removeprefix('kho:'):x for x in map(json.loads,(W/'h.jsonl').read_text().splitlines())}
errors=[{'id':k,'reconstructed':sha(v['src'].encode()),'hoi_quy':H.get(k,{}).get('sha256')} for k,v in rows.items() if k not in H or sha(v['src'].encode())!=H[k]['sha256']]
save('reconstruction_audit.json',{'receipts':receipts,'count':count,'unique':len(rows),'id_diff':sorted(set(H)^set(rows)),'hash_mismatches':errors,'limits':'Original five raw JSONL files were not supplied; regenerated using archived original generators; duplicate identities inferred from frozen round5 inventory.'});print('RECONSTRUCTION_COMPLETE',count,len(rows),'mismatches',len(errors),flush=True)
