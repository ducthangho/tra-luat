from pathlib import Path
import ast,sys,os,json,subprocess,concurrent.futures,collections,threading
R=Path(__file__).resolve().parent;root=R.parent
s=ast.parse((R/'operators5_target.py').read_text());nodes=[]
for n in s.body:
 if isinstance(n,ast.FunctionDef) and n.name=='cases':break
 nodes.append(n)
g={};exec(compile(ast.Module(body=nodes,type_ignores=[]),'operators-generator','exec'),g)
M,TARGETS=g['M'],g['TARGETS'];out=R/'operators6';out.mkdir(exist_ok=True)
def cases(path,name):
 target=TARGETS.get(name)
 if target: names=[target]
 else:names=['c46_mien_che_do','c31_che_do_duong_khac','c29_che_do_env_job','c28_che_do_env_buoc','c49_oracle_nhieu_truc']
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);rows=[]\nfor c in %r:\n rc,o=t.chay_ca(c);rows.append((c,rc,o))\n if rc==3 and o.startswith('DO:'+c+':'):break\nprint(json.dumps(rows))"%(str(root/'ops/ci_provenance_test.py'),names)
 cmd=[sys.executable,'-B','-c',code];q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(path),PYTHONDONTWRITEBYTECODE='1'),timeout=900)
 try:rs=json.loads(q.stdout)
 except Exception:rs=[('import',4,(q.stdout+q.stderr).decode())]
 return {'command':cmd,'rc':q.returncode,'cases':rs}
def one(v):
 name,src=v;p=out/(str(M.index(v))+'.py');p.write_text(src);a=cases(root/'ops/ci_provenance.py',name);b=cases(p,name)
 ks=[c for c,rc,o in b['cases'] if rc==3 and o.startswith('DO:'+c+':')];bad=[(c,rc,o) for c,rc,o in b['cases'] if rc not in (0,3)]
 return {'name':name,'source':str(p),'target':TARGETS.get(name),'baseline':a,'mutant':b,'rank':'HONG_BASE' if any(rc for c,rc,o in a['cases']) else 'GIET+NEM' if ks and bad else 'GIET' if ks else 'TIN_DUNG_GIA' if bad else 'SONG_SOT','killed':ks,'other_errors':bad}
rows=[]
with concurrent.futures.ThreadPoolExecutor(3) as ex:
 for r in ex.map(one,M):
  rows.append(r);(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(r['name'],r['rank'],flush=True)
print(collections.Counter(r['rank'] for r in rows))
