from pathlib import Path
import json,ast,sys,os,subprocess,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent
src=(root/'ops/ci_provenance.py').read_text(); out=R/'historical-targets6';out.mkdir(exist_ok=True)
# Keep every unique historical anchor/replacement; link duplicates to the first measurement.
known={}
for parent in ('r4-luot3','r4-luot4','r4-luot5'):
 for prod in ('frontier','frontier2','new-frontier','frontier5'):
  p=root/'.review-input'/parent/prod/'results.json'
  if not p.exists():continue
  for z in json.loads(p.read_text()):
   if z.get('killed'):known[(z.get('old'),z.get('new'))]=z['killed'][0]
M=[];inventory=[]
for name in ('frontier.py','frontier2.py','new_frontier.py'):
 tree=ast.parse((R/name).read_text());vals=None
 for a in tree.body:
  if isinstance(a,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='M' for x in a.targets) and isinstance(a.value,ast.List):vals=ast.literal_eval(a.value);break
 assert vals is not None,name
 for ident,old,new in vals:
  case=known.get((old,new))
  # Signature-only env anchor repairs are applied to the scratch measurement and recorded.
  if name=='frontier.py':
   old=old.replace('for k in v','for k in d["env"]').replace('type(v)','type(d["env"])')
   new=new.replace('for k in v','for k in d["env"]').replace('bool(v)','bool(d["env"])').replace('type(v)','type(d["env"])')
  inventory.append({'producer':name,'name':ident,'old':old,'new':new,'previous_target':case})
  if (old,new) in {(x['old'],x['new']) for x in M}:continue
  M.append({'producer':name,'name':ident,'old':old,'new':new,'target':case})
(R/'historical-target-inventory6.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
def run(path,case):
 # If no historical valid target exists, use the independent current oracle c49 first,
 # then the whole catalogue until one exact case kills. No credit for an unrelated exception.
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);names=%r;rows=[]\nfor c in names or list(t.CA):\n r,o=t.chay_ca(c);rows.append((c,r,o))\n if r==3 and o.startswith('DO:'+c+':'):break\nprint(json.dumps(rows))"%(str(root/'ops/ci_provenance_test.py'),[case] if case else [])
 cmd=[sys.executable,'-B','-c',code];q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(path),PYTHONDONTWRITEBYTECODE='1'),timeout=900)
 try:rs=json.loads(q.stdout)
 except Exception:rs=[('import',4,(q.stdout+q.stderr).decode())]
 return {'command':cmd,'rc':q.returncode,'cases':rs}
def one(z):
 if src.count(z['old'])!=1:return z|{'rank':'HONG_NEO','count':src.count(z['old'])}
 path=out/(z['name']+'.py');path.write_text(src.replace(z['old'],z['new']));b=run(root/'ops/ci_provenance.py',z['target']);r=run(path,z['target']);ks=[c for c,v,o in r['cases'] if v==3 and o.startswith('DO:'+c+':')];bad=[(c,v,o) for c,v,o in r['cases'] if v not in (0,3)]
 rank='HONG_BASE' if any(v for c,v,o in b['cases']) else 'GIET' if ks else 'TIN_DUNG_GIA' if bad else 'SONG_SOT'
 return z|{'path':str(path),'baseline':b,'mutant':r,'killed':ks,'other_errors':bad,'rank':rank}
rows=[]
with concurrent.futures.ThreadPoolExecutor(3) as ex:
 for z in ex.map(one,M):
  rows.append(z);(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(z['name'],z['rank'],flush=True)
print(collections.Counter(z['rank'] for z in rows))
