from pathlib import Path
import json
r=Path('.review').resolve();root=r.parent
(r/'interrupted7.json').write_text(json.dumps({'frontier6-replay':{'status':'interrupted','rc':130},'frontier7':{'status':'interrupted','rc':130},'reason':'Replace full suite on already killed mutants by exact-target replay; surviving new mutants still run every case.'},indent=2))
p=r/'frontier6.py';s=p.read_text();(r/'frontier6-before-targeting.py').write_text(s)
start=s.index('def cases(path):');end=s.index('\ndef one(v):',start)
targets={}
for folder in ('frontier6','frontier6-extra','frontier6-extra2','frontier6-extra3'):
 for z in json.loads((root/'.review-input/r4-luot6'/folder/'results.json').read_text()):
  if z.get('killed'):targets[z['name']]=z['killed'][0]
  elif z['name']!='env_only_keys_str':targets[z['name']]='c50_mien_luot6'
(r/'targets6-replay7.json').write_text(json.dumps(targets,indent=2))
replacement='''def cases(path):
 target=json.loads((R/'targets6-replay7.json').read_text()).get(path.stem)
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in %r or t.CA]))"%(str(root/'ops/ci_provenance_test.py'),[target] if target else [])
 cmd=[sys.executable,'-B','-c',code]
 p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(path)),timeout=900)
 try:res=json.loads(p.stdout)
 except Exception:res=[('import',p.returncode or 4,(p.stdout+p.stderr).decode('utf8','replace'))]
 return cmd,p,res
'''
p.write_text(s[:start]+replacement+s[end:])
p=r/'frontier7.py';s=p.read_text();(r/'frontier7-before-targeting.py').write_text(s)
a=s.index(' code="import importlib.util as u,json;');b=s.index('\n cmd=',a)
s=s[:a]+''' code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);rows=[]\\nfor c in sorted(t.CA,key=lambda c:c.startswith('c49')):\\n rc,o=t.chay_ca(c);rows.append((c,rc,o))\\n if rc==3 and o.startswith('DO:'+c+':'):break\\nprint(json.dumps(rows))"%str(root/'ops/ci_provenance_test.py')'''+s[b:]
p.write_text(s)
print('target optimization, all sources stay copies; complete-50 only asserted for new survivors')
