import pathlib,subprocess,sys,os,tempfile,json
W=pathlib.Path(__file__).resolve().parent;R=W.parent/'repo'
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['TMPDIR']=str(W/'tmp');tempfile.tempdir=str(W/'tmp')
sys.path.insert(0,str(R/'.claude/dev'));import packet_loop_test as T
res={}
for rev in ('f602325','HEAD'):
 d=W/'legacy'/rev;d.mkdir(parents=True,exist_ok=True)
 for n in ('launcher.py','packet_loop.py'):(d/n).write_bytes(subprocess.check_output(['git','show',rev+':.claude/dev/'+n],cwd=R))
 names={n for n,_ in T.CASES if n.startswith('cong_c_d') or n=='cong_c_fixture_crlf'}
 k=T.chay_suite(d/'packet_loop.py',d/'suite',chi_chay=names)
 res[rev]={n:None if v is None else str(v) for n,v in k.items()}
 print(rev,len(k),sum(v is None for v in k.values()),flush=True)
(W/'legacy.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
sys.exit(any(v is not None for r in res.values() for v in r.values()))
