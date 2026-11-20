import sys,os,json,pathlib,subprocess,concurrent.futures as cf
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo'
ms=[json.loads(l) for l in pathlib.Path(sys.argv[1]).read_text().splitlines()];out=pathlib.Path(sys.argv[2]); mode=sys.argv[3] if len(sys.argv)>3 else 'native'
d=w/(out.stem+'_modules');d.mkdir(exist_ok=True)
def run(m):
 key=m.get('id',m.get('k'));p=d/(str(key)+'.py');p.write_text(m['src'])
 cmd=[sys.executable,'-B',str(w/'scan_runner.py')] if mode=='native' else [sys.executable,'-B',str(w.parent/'quet/chay_ca.py'),os.environ.get('REVIEW_SCAN_TEST',str(r/'ops/gate_output_doi_chieu_test.py'))]
 env=dict(os.environ,TMPDIR=str(w/'tmp'),PYTHONDONTWRITEBYTECODE='1',GATE_OUTPUT_DOI_CHIEU_MA=str(p))
 try:
  x=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=600)
  result={k:v for k,v in m.items() if k!='src'};result.update(rc=x.returncode,stdout=x.stdout,stderr=x.stderr)
 except subprocess.TimeoutExpired as e: result={'id':key,'timeout':True}
 return result
with out.open('w') as f,cf.ThreadPoolExecutor(4) as ex:
 for i,m in enumerate(ex.map(run,ms)):
  f.write(json.dumps(m,ensure_ascii=False)+'\n');f.flush()
  if (i+1)%25==0: print(i+1,'/',len(ms),flush=True)
print('DONE',len(ms),flush=True)
