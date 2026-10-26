from pathlib import Path
import ast,os,sys,json,hashlib,subprocess
R=Path('.review').resolve();root=R.parent
for p in ('suite.json','after-suite6-run.json','final-proofs6-run.json'):
 assert json.loads((R/p).read_text())['returncode']==0,p
# Merge the separately added pure leap-day boundary into the finished proof ledger.
proofs=json.loads((R/'proof-final6-results.json').read_text());more=json.loads((R/'proof6-time_reject_leap_day_safe.json').read_text());known={p['name'] for p in proofs}
for z in more:
 if z['name'] not in known:proofs.append(z)
(R/'proof-final6-results.json').write_text(json.dumps(proofs,ensure_ascii=False,indent=2))
assert all(x['proven'] for x in proofs),[(x['name'],x['pair']) for x in proofs if not x['proven']]
nodes=[n for n in ast.parse((R/'setup6.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='snapshot'];exec(compile(ast.Module(body=nodes,type_ignores=[]),'snapshot6','exec'))
a=json.loads((R/'snapshot-start.json').read_text());b=snapshot();(R/'snapshot-end.json').write_text(json.dumps(b,ensure_ascii=False,indent=2))
delta=[p for p in a['files'].keys()|b['files'].keys() if a['files'].get(p)!=b['files'].get(p)]
comp={'files_start':len(a['files']),'files_end':len(b['files']),'changed_paths':delta,'git_equal':a['git']==b['git'],'start_head':a['git']['head'],'end_head':b['git']['head'],'start_tree':a['git']['tree'],'end_tree':b['git']['tree']}
(R/'snapshot-comparison6.json').write_text(json.dumps(comp,ensure_ascii=False,indent=2));assert not delta and comp['git_equal'],comp
commands=[]
for c in [['git','status','--short'],['git','diff','--check','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'],['git','rev-parse','HEAD','HEAD^{tree}']]:
 q=subprocess.run(c,capture_output=True);commands.append({'command':c,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()});assert q.returncode==0
assert not commands[0]['stdout'] and not commands[1]['stdout']
(R/'final-checks6.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2))
q=subprocess.run([sys.executable,'-B',str(R/'report6.py')],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
(R/'report6-receipt.json').write_text(json.dumps({'command':[sys.executable,'-B',str(R/'report6.py')],'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()},ensure_ascii=False,indent=2));assert q.returncode==0,q.stderr.decode()
verdict=(R/'VERDICT.md').read_text();assert verdict.startswith('verdict: changes_requested\nreviewed_sha: 35453ff30170998ffea663801299db5876cc8e0c\n')
manifest=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name=='evidence-manifest6.json' or set(p.relative_to(R).parts)&{'tmp','cache'}:continue
 bb=p.read_bytes();manifest.append({'path':str(p.relative_to(R)),'bytes':len(bb),'sha256':hashlib.sha256(bb).hexdigest()})
(R/'evidence-manifest6.json').write_text(json.dumps({'reviewed_sha':'35453ff30170998ffea663801299db5876cc8e0c','reviewed_tree':'c5985dae1248e3e57cffdb580133e318ed27d64c','excludes':['tmp/','cache/','evidence-manifest6.json'],'files':manifest},ensure_ascii=False,indent=2))
print(q.stdout.decode().strip());print('READ_ONLY_SNAPSHOT DAT',len(a['files']),'files; git status clean; HEAD/tree unchanged');print('VERDICT_SHA256',hashlib.sha256((R/'VERDICT.md').read_bytes()).hexdigest(),'ARTIFACTS',len(manifest))
