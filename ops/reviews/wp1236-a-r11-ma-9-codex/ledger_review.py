from review_common import *
import ast, collections
pool=[json.loads(x) for x in (W.parent/'bang_chung/kho_dot_bien_reviewer_luot6_7_8.jsonl').read_text().splitlines()]
ledger=[json.loads(x) for x in (W.parent/'bang_chung/ledger_kho_152_2719f81.jsonl').read_text().splitlines()]
assert len({x['id'] for x in pool})==len(pool)==152
assert {x['id'] for x in pool}=={x['id'] for x in ledger} and len(ledger)==152
src=ast.unparse(ast.parse((R/'ops/gate_output_doi_chieu.py').read_text()))+'\n'
byid={x['id']:x for x in ledger}
out=[]
(W/'ledger_remeasure.jsonl').write_text('')
for d in pool:
 l=byid[d['id']]; rec={'id':d['id'],'ledger':l['ledger'],'anchor_count':src.count(d['cu'])}
 if rec['anchor_count']==1:
  p=W/'mutants_ledger'/f"{d['id']}.py"; p.parent.mkdir(exist_ok=True); p.write_text(src.replace(d['cu'],d['moi']),encoding='utf8')
  if l['ledger']=='GIET':
   p0=subprocess.run([sys.executable,'-B',str(W/'scan_worker.py'),str(p),json.dumps(l['ca'])],cwd=R,capture_output=True)
   rec.update(child_rc=p0.returncode,stdout=p0.stdout.decode(),stderr=p0.stderr.decode())
   assert p0.returncode==0 and p0.stdout.rstrip().endswith(b'XONG_CON'),rec
   res=json.loads(next(x[len('REVIEW_RESULT '):] for x in p0.stdout.decode().splitlines() if x.startswith('REVIEW_RESULT ')))
   rec['target_killed']=all(x['rc']==3 and x['message'].startswith('DO:'+x['case']+':') for x in res)
   assert rec['target_killed'],rec
 else: assert l['ledger']=='KHONG_AP_DUNG',rec
 out.append(rec)
 with (W/'ledger_remeasure.jsonl').open('a',encoding='utf8') as f: f.write(json.dumps(rec,ensure_ascii=False)+'\n')
 print(d['id'],l['ledger'],rec.get('target_killed','scope-proof'),flush=True)
save('ledger_summary.json',dict(counts=dict(collections.Counter(x['ledger'] for x in ledger)),anchors=dict(collections.Counter(x['anchor_count'] for x in out)),total=len(out)))
print('HOAN_TAT_LEDGER152',flush=True)
