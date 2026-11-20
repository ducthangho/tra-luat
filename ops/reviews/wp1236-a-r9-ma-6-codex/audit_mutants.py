import pathlib,importlib.util,os,json,sys,subprocess,concurrent.futures as cf
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo';p=r/'ops/gate_output_doi_chieu_test.py'
s=importlib.util.spec_from_file_location('tests',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
src=(r/'ops/gate_output_doi_chieu.py').read_text(); d=w/'audit_modules';d.mkdir(exist_ok=True)
def run(x):
 name,a,b,target=x;ca=next(c for c in m.CA if c.split('_')[0]==target)
 if src.count(a)!=1:return dict(id=name,problem='anchor')
 mod=d/(name+'.py');mod.write_text(src.replace(a,b));cmd=[sys.executable,'-B',str(p),'--mot-ca',ca]
 q=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,TMPDIR=str(w/'tmp'),GATE_OUTPUT_DOI_CHIEU_MA=str(mod),PYTHONDONTWRITEBYTECODE='1'),timeout=600)
 return dict(id=name,target=ca,rc=q.returncode,stdout=q.stdout,stderr=q.stderr,classification=m.phan_hang(q.returncode,q.stdout+q.stderr,ca))
with (w/'audit_mutants.jsonl').open('w') as f,cf.ThreadPoolExecutor(4) as ex:
 for i,x in enumerate(ex.map(run,m.DOT_BIEN)):
  f.write(json.dumps(x,ensure_ascii=False)+'\n');f.flush()
  if (i+1)%20==0:print(i+1,flush=True)
print('DONE',len(m.DOT_BIEN),flush=True)
