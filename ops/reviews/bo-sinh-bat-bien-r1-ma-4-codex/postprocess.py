from pathlib import Path
import json,re,collections,hashlib,subprocess
w=Path(__file__).resolve().parent
rows=json.loads((w/'measure.json').read_text());pairs=[]
for kind,n,limit in [('A',3,5),('B',2,30)]:
 for i in range(1,n+1):
  x={v['side']:v for v in rows if v.get('kind')==kind and v.get('sample')==i}
  if len(x)==2:pairs.append(dict(kind=kind,sample=i,base=x['base']['seconds'],head=x['head']['seconds'],delta=x['head']['seconds']-x['base']['seconds'],limit=limit,base_rc=x['base']['rc'],head_rc=x['head']['rc']))
spreads={kind:{side:max(v['seconds'] for v in rows if v.get('kind')==kind and v.get('side')==side)-min(v['seconds'] for v in rows if v.get('kind')==kind and v.get('side')==side) for side in ['base','head']} for kind in ['A','B'] if any(v.get('kind')==kind for v in rows)}
gates=[]
for row in rows:
 p=w/(row['label']+'.log')
 if not p.exists():continue
 data=p.read_bytes();lines=data.decode('utf-8','replace').splitlines()
 positive=[s for s in lines if re.search(r'CA:|DOT BIEN:|TU KIEM|TONG:|TỔNG:|RUFF CI:|PHẢN CHỨNG:|PHAN CHUNG:|tl selftest|All checks',s)]
 gates.append(dict(**row,log=str(p),sha256=hashlib.sha256(data).hexdigest(),positive=positive))
selftest={s:(w/(s+'-selftest.log')).read_text().splitlines() for s in ['base','head']}
failed={s:[x for x in ls if '[FAIL]' in x] for s,ls in selftest.items()}
trace=json.loads((w/'trace-v2.json').read_text());summary={}
for outer in dict.fromkeys(x['outer'] for x in trace['calls']):
 calls=[x for x in trace['calls'] if x['outer']==outer and x['case']!=outer];cnt=collections.Counter(x['rc'] for x in calls)
 summary[outer]=dict(counts=dict(cnt),wrong_do=[x for x in calls if x['rc']==3 and not x['output'].startswith('DO:'+x['case']+':')])
(w/'results-summary.json').write_text(json.dumps(dict(pairs=pairs,spreads=spreads,gates=gates,selftest_failed=failed,selftest_failed_same=failed['base']==failed['head'],trace=summary),ensure_ascii=False,indent=2));print(json.dumps(dict(pairs=pairs,spreads=spreads,selftest_failed=failed,trace=summary),ensure_ascii=False,indent=2))
