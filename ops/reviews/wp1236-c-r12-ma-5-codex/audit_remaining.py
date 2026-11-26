import pathlib,subprocess,json,os,collections,re,sys,hashlib
R=pathlib.Path(__file__).resolve().parent.parent/'repo';W=R.parent/'work';env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(W/'tmp')};receipts=[]
def run(cmd,log=None):
 p=subprocess.run(cmd,cwd=R,env=env,capture_output=True);receipts.append(dict(command=cmd,rc=p.returncode));
 if log:(W/log).write_bytes(p.stdout+p.stderr)
 return p
S=W/'corpus.git';p=run(['git','clone','--bare','--shared',str(R),str(S)],'corpus_setup.log');assert p.returncode==0
h=run(['git','rev-parse','HEAD']).stdout.decode().strip();assert run(['git','--git-dir',str(S),'update-ref','refs/remotes/origin/master',h]).returncode==0
for label,script in [('previous',W/'previous/packet_loop.py'),('head',R/'.claude/dev/packet_loop.py')]:
 p=run(['python3','-B',str(R.parent/'bang_chung/cong_cu/do_kho_that.py'),str(script),str(S),h,str(W/f'corpus_{label}.tsv')],f'corpus_{label}.log');print(label,p.returncode,p.stdout.decode(),flush=True)
tree=run(['git','ls-tree','-r','HEAD','--','ops/land']).stdout.decode();counts=collections.Counter(l.split()[0] for l in tree.splitlines())
base=json.loads((W/'ruff_base.json').read_text());head=json.loads((W/'ruff_head.json').read_text());canon=lambda a:collections.Counter((pathlib.Path(d['filename']).name,d['code'],re.sub(r'from line [0-9]+','from line <n>',d['message'])) for d in a)
cmd=['python3','-B','-c',"import runpy; m=runpy.run_path('.claude/dev/ci_dang_ky_test.py'); e,n=m['loi_ruff_ci'](); print('RUFF_CONTRACT',n,e); raise SystemExit(bool(e) or n==0)"]
p=run(cmd,'ruff_contract.log');print('ruff contract',p.returncode,flush=True)
sys.path.insert(0,str(R/'.claude/dev'));import packet_loop_test as T
names={n for n,_ in T.CASES if n.startswith(('cong_c_d1_','cong_c_d2_','cong_c_d3_','cong_c_d4_')) or n in ['cong_c_dong_du','cong_c_fixture_crlf']};legacy={}
for label,script in [('base',W/'base/packet_loop.py'),('head',T.CANONICAL)]:
 z=T.chay_suite(script,W/f'legacy_{label}',chi_chay=names);legacy[label]={k:None if v is None else str(v) for k,v in z.items()};print('legacy',label,len(z),sum(v is None for v in z.values()),flush=True)
audit=dict(corpus_oid=h,corpus_scope='HEAD data, synthetic origin/master in scratch bare repo only; not actual remote authority',corpus_equal=(W/'corpus_previous.tsv').read_bytes()==(W/'corpus_head.tsv').read_bytes(),ops_land_modes=counts,ruff_counts=[len(base),len(head)],ruff_new=list((canon(head)-canon(base)).elements()),ruff_removed=list((canon(base)-canon(head)).elements()),legacy=legacy,receipts=receipts)
(W/'remaining_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
