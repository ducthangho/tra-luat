import os,sys,json,subprocess,hashlib,pathlib,time
W=pathlib.Path(__file__).resolve().parent
R=W.parent/'repo'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
(W/'tmp').mkdir(exist_ok=True)
os.environ['TMPDIR']=str(W/'tmp')
import tempfile
tempfile.tempdir=str(W/'tmp')
sys.path.insert(0,str(R/'.claude/dev'))
import packet_loop_test as T
receipts=[]
def run(name,cmd,cwd=R):
 p=subprocess.run(cmd,cwd=cwd,capture_output=True)
 (W/(name+'.log')).write_bytes(p.stdout+p.stderr)
 receipts.append(dict(name=name,command=cmd,rc=p.returncode,sha256=hashlib.sha256(p.stdout+p.stderr).hexdigest()))
 (W/'checks_receipts.json').write_text(json.dumps(receipts,indent=2))
 print(name,p.returncode,flush=True)
if sys.argv[1]=='suite':
 names={n for n,_ in T.CASES if n.startswith('cong_d2b_')}
 result=T.chay_suite(T.CANONICAL,W/'suite',chi_chay=names)
 out={k:None if v is None else {'type':type(v).__name__,'error':str(v),'grade':T._phan_loai_giet(v)} for k,v in result.items()}
 (W/'targeted.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 print('TARGETED',sum(v is None for v in result.values()),'/',len(result),flush=True)
 sys.exit(any(v is not None for v in result.values()))
if sys.argv[1]=='mutants':
 run('declared',[sys.executable,'-B',str(W.parent/'bang_chung/cong_cu/chay_ca.py'),str(R),'db','d2b_'])
