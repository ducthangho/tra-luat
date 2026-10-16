import json,pathlib
out=pathlib.Path(__file__).resolve().parent
read=lambda p:[json.loads(s) for s in (out/p).read_text().splitlines()]
summary={}
for v in ('3.10','3.11','3.12','3.13'):
 rows=read('runtime_isolated-'+v+'.stdout');depth=read('runtime_depth-'+v+'.stdout');receipt=read('focused_controls-'+v+'.stdout')
 fuzz=next(x for x in rows if x['kind']=='runtime_fuzz');samples=[x for x in rows if x['kind']=='runtime']
 assert fuzz['total']==592 and not fuzz['errors']
 assert len(samples)==16 and all('result' in x['api'] and json.loads(x['stdout'])==x['api']['result'] and x['rc'] in (0,12,2) and not x['stderr'] for x in samples)
 assert len(depth)==6 and all('exception' not in x['api'] and json.loads(x['stdout'])==x['api'] and x['rc'] in (0,12,2) and not x['stderr'] for x in depth)
 assert receipt[0]['fixture_equal'] and receipt[0]['result']['ok'] and receipt[1]['rc']==0
 summary[v]={'api_count':fuzz['total'],'api_errors':fuzz['errors'],'samples_api_cli_equal':len(samples),'depths_api_cli_equal':[x['depth'] for x in depth],'receipt_fixture_equal':True,'receipt_api_ok':True,'receipt_cli_rc':0}
(out/'runtime-summary.json').write_text(json.dumps(summary,indent=2));print('runtime',summary)
rows=[]
for p in sorted(out.glob('*.json')):
 d=json.loads(p.read_text())
 if isinstance(d,dict) and 'command' in d:
  assert d['rc']==0 and not d['timeout'],(p.name,d)
  rows.append(dict(label=p.stem,**d))
(out/'commands.json').write_text(json.dumps(rows,indent=2));print('logged_commands',len(rows),'all_driver_or_head_commands_rc0')
for label in ('suite-3.10','suite-3.11','suite-3.12','suite-3.13','suite-zero','suite-x640'):
 s=(out/(label+'.stdout')).read_text();assert s=='nghia vu: witness_killed 162 · equivalent_verified 9 · unresolved 0\ndoc_receipt_thu_hoi tests: 156/156 ca QUA · 162/162 dot bien GIET\n';print(label,s.strip())
num=[s.split('\t') for s in (out/'numstat.txt').read_text().splitlines()]
print('numstat',len(num),'files',sum(int(s[0]) for s in num),'added',sum(int(s[1]) for s in num),'removed')
print('product',[(s[2],int(s[0])) for s in num if s[2].startswith('.claude/')])
reg=(out/'registry.stdout').read_text();print('registry',reg.splitlines()[:4]+reg.splitlines()[-2:])
for d in read('ruff-delta.stdout'):
 if 'delta_equal' in d:print('ruff',d)
for d in read('ghim.stdout'):
 if d.get('kind')=='child_pinning':print('pinning',d['children'],d['all_pinned'])
print('original_inputs_match',len(json.loads((out/'input-identity.json').read_text())))
