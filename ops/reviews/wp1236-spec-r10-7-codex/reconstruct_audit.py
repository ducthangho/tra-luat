import ast,hashlib,json,pathlib,subprocess,sys
W=pathlib.Path(__file__).resolve().parent; R=W.parent/'repo';M=W.parent/'ma_r9_git';O=W/'originals';O.mkdir(exist_ok=True)
old=R/'ops/reviews/wp1236-spec-r10-6-codex';receipts=[]
for n in ['make_independent.py','make_extra.py','make_order_url.py','complete_reason_sweep.py']:
 s=(old/n).read_text().replace("(w.parent/'repo/ops/gate_output_doi_chieu.py').read_text()",f"pathlib.Path({str(M/'ops/gate_output_doi_chieu.py')!r}).read_text()")
 if n=='complete_reason_sweep.py':
  inv=json.loads((R/'ops/reviews/wp1236-spec-r10-5-codex/replay_inventory.json').read_text());ids={x['id'] for x in inv['duplicate_ids']}
  rows=[json.loads(x) for x in (O/'independent_mutants.jsonl').read_text().splitlines()];(O/'independent_corrected.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows if x['id'] in ids))
 (O/n).write_text(s);p=subprocess.run([sys.executable,'-B',str(O/n)],cwd=O,capture_output=True);receipts.append({'script':n,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()});assert p.returncode==0,receipts
rows={};count=0
for n in ['independent_mutants.jsonl','independent_corrected.jsonl','extra_mutants.jsonl','order_url_mutants.jsonl','reason_complete_mutants.jsonl']:
 for l in (O/n).read_text().splitlines():
  x=json.loads(l);count+=1;rows[x['id']]=x
H={x['id'].removeprefix('kho:'):x for x in map(json.loads,(W/'h.jsonl').read_text().splitlines())}
errs=[k for k,v in rows.items() if k not in H or ast.unparse(ast.parse(v['src']))!=H[k]['src']]
rep={'receipts':receipts,'rows':count,'unique':len(rows),'id_diff':sorted(set(H)^set(rows)),'normalized_mismatches':errs,'method':'Re-execute archived ma6 generators unmodified except read path, compare ast.unparse each original against current hoi-quy. No newly authored attack payload.'}
(W/'reconstruction_audit.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2));print(json.dumps(rep,ensure_ascii=False))
