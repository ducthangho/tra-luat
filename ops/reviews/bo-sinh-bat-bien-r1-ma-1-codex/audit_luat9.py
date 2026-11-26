from pathlib import Path
import importlib.util,json,hashlib,collections,os,sys,subprocess
w=Path(__file__).resolve().parent;r=w.parent/'repo'; ev=w.parent/'bang_chung/luat9'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
p=r/'ops/reviews/wp1236-r10-soan/quet_dot_bien.py'
spec=importlib.util.spec_from_file_location('q',p);q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
assert q._sha(p.read_bytes())=='1b3e4a9e0a4608b9fd6c62e1de99bf509cfd8cb96bedb4d956bac681fc1b9c0c'
summary={}
for cap,mod in [('B','land_evidence_nguon'),('A','gate_output_doi_chieu')]:
 out=w/('luat9-'+cap);out.mkdir(exist_ok=True)
 ms=q.sinh((r/f'ops/{mod}.py').read_text())
 (out/'manifest.jsonl').write_text(''.join(json.dumps(m,ensure_ascii=False)+'\n' for m in ms))
 kho=ev/('kho_rong.jsonl' if cap=='B' else 'kho_A.jsonl')
 q.hoi_quy(kho,'-',r/f'ops/{mod}.py',out/'hoi_quy.jsonl')
 (out/'tat_ca.jsonl').write_bytes((out/'manifest.jsonl').read_bytes()+(out/'hoi_quy.jsonl').read_bytes())
 variants=[json.loads(x) for x in (out/'tat_ca.jsonl').read_text().splitlines() if 'src' in json.loads(x)]
 byid={m['id']:m for m in variants}
 allrows=[];hashchecks=[]
 for side,clone in [('nen','base'),('sau','head')]:
  src=ev/(cap+'-'+side)
  rows=[json.loads(x) for x in (src/'kq.jsonl').read_text().splitlines()]
  for line in (src/'SHA256SUMS-D').read_text().splitlines():
   sha,name=line.split();file=src/name if (src/name).exists() else out/name
   actual=q._sha(file.read_bytes());hashchecks.append([side,name,sha==actual]);assert sha==actual,(cap,side,name)
  neo=rows[0]['neo']; assert neo['goc']==q._sha((w/clone/f'ops/{mod}.py').read_bytes())
  assert neo['test']==q._sha((w/clone/f'ops/{mod}_test.py').read_bytes())
  assert neo['manifest']==q._sha((out/'tat_ca.jsonl').read_bytes())
  assert neo['kho']==q._sha(kho.read_bytes())
  assert [(x['id'],x['sha256']) for x in rows[1:]]==[(m['id'],m['sha256']) for m in variants]
  assert rows[0]['baseline']=='SONG' and rows[0]['tap_con']==False
  allrows.append(rows)
 before,after=allrows
 changes=[x['id'] for x,y in zip(before[1:],after[1:]) if x['phan_hang']=='GIET' and y['phan_hang']!='GIET']
 summary[cap]={'count':len(variants),'hashchecks':hashchecks,'base_counts':dict(collections.Counter(x['phan_hang'] for x in before[1:])),'head_counts':dict(collections.Counter(x['phan_hang'] for x in after[1:])),'regressions':changes,'baseline_cases':[len(x[0]['baseline_ca_dat']) for x in allrows]}
 print('AUDIT',cap,json.dumps(summary[cap]),flush=True)
 # Two distinct killers: an early guard and the changed/reused domain consumer.
 target='c36' if cap=='B' else 'a129'
 selected=[next(x for x in after[1:] if x['phan_hang']=='GIET'),next((x for x in after[1:] if any(t.startswith(target+'_') for t in x['giet'])), next(x for x in reversed(after[1:]) if x['phan_hang']=='GIET'))]
 subset=out/'sample.jsonl';subset.write_text(''.join(json.dumps(byid[x['id']],ensure_ascii=False)+'\n' for x in selected))
 summary[cap]['sample_ids']=[x['id'] for x in selected]
 for side in ['base','head']:
  cmd=[sys.executable,'-B',str(p),'chay',str(subset),str(w/side/f'ops/{mod}_test.py'),'--goc',str(w/side/f'ops/{mod}.py'),'--ra',str(out/(side+'-sample.jsonl')),'--song-song','1']
  with (out/(side+'-sample.log')).open('w') as f:res=subprocess.run(cmd,cwd=w/side,stdout=f,stderr=subprocess.STDOUT)
  print('SAMPLE',cap,side,'rc',res.returncode,flush=True);summary[cap][side+'_sample_rc']=res.returncode
 (w/'luat9-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
