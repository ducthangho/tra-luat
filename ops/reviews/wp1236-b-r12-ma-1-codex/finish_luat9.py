from pathlib import Path
import json,collections,hashlib
W=Path(__file__).resolve().parent
read=lambda p:[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
ms={s:read(W/f'do-{s}/manifest.jsonl') for s in ('base','head')}
rs={s:read(W/f'do-{s}/kq.jsonl') for s in ('base','head')}
results={s:{x['id']:x for x in rs[s][1:]} for s in rs}
for side,folder in [('head','head-f4e93b3'),('base','base-f602325')]:
 assert rs[side][0]['neo']==read(W.parent/'bang_chung'/'luat9'/folder/'kq.jsonl')[0]['neo']
for s in rs:
 assert len(results[s])==len(ms[s])
 assert set(results[s])=={x['id'] for x in ms[s]}
 assert rs[s][0]['baseline']=='SONG' and rs[s][0]['tap_con'] is False
 assert len(rs[s][0]['baseline_ca_dat'])==(33 if s=='head' else 23)
 assert rs[s][0]['neo']['manifest']==hashlib.sha256((W/f'do-{s}/manifest.jsonl').read_bytes()).hexdigest()
 assert rs[s][0]['neo']['cong_cu']=='1b3e4a9e0a4608b9fd6c62e1de99bf509cfd8cb96bedb4d956bac681fc1b9c0c'
 assert all(results[s][x['id']]['sha256']==x['sha256'] for x in ms[s])
 assert int((W/f'logs/do-{s}.rc').read_text())==0
 assert 'HOAN_TAT neo=' in (W/f'logs/do-{s}.log').read_text()
kt=read(W/'inherited.jsonl'); lookup={x['sha256']:x['id'][4:] for x in kt if 'sha256' in x}
assert len(lookup)==548
ledger=[];delta=[]
for x in ms['head']:
 h=results['head'][x['id']];bid=lookup.get(x['sha256'])
 if bid:
  b=results['base'][bid]
  ledger.append({'base_id':bid,'head_id':x['id'],'sha256_head_mutant':x['sha256'],'base_rank':b['phan_hang'],'head_rank':h['phan_hang'],'base_case':b['giet'],'head_case':h['giet']})
 else:
  delta.append({'id':x['id'],'sha256':x['sha256'],'rank':h['phan_hang'],'case':h['giet'],'assertion':h['assertion']})
regress=[x for x in ledger if x['base_rank']=='GIET' and x['head_rank']!='GIET']
removed=[]
for x in kt:
 if 'sha256' in x: continue
 bid=x['id'][4:];replacement=bid.replace(':340:4',':408:4');r=results['head'][replacement]
 removed.append({'base_id':bid,'reason':x['ly_do'],'replacement':replacement,'rank':r['phan_hang'],'case':r['giet']})
summary={'base':dict(collections.Counter(x['phan_hang'] for x in rs['base'][1:])),'head':dict(collections.Counter(x['phan_hang'] for x in rs['head'][1:])),'delta':dict(collections.Counter(x['rank'] for x in delta)),'delta_total':len(delta),'inherited_total':len(ledger),'regressions':regress,'removed_base_replacements':removed,'equivalents':[],'baseline_cases':{s:len(rs[s][0]['baseline_ca_dat']) for s in rs},'neo':{s:rs[s][0]['neo'] for s in rs}}
assert len(delta)==76 and len(ledger)==548
for name,data in [('luat9-summary',summary),('delta-ledger',delta),('inherited-ledger',ledger)]: (W/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
md=['| ID base | ID head | Base | Head | Ca giết head |','|---|---|---|---|---|']
md += [f"| `{x['base_id']}` | `{x['head_id']}` | {x['base_rank']} | {x['head_rank']} | {', '.join(x['head_case'])} |" for x in ledger]
(W/'inherited-ledger.md').write_text('\n'.join(md)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
assert not regress and all(x['rank']=='GIET' and x['case'] and x['assertion'].startswith('DO:') for x in delta)
assert all(x['rank']=='GIET' and x['case'] for x in removed)
