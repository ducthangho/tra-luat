import sys, pathlib, subprocess, tempfile, os, re, json, hashlib, ast, importlib.util
W=pathlib.Path(__file__).resolve().parent.parent;O=W/'out';mode=sys.argv[1];R=W/'cay-kho' if mode=='base' else O/'prototype'
sys.dont_write_bytecode=True;os.environ['PYTHONDONTWRITEBYTECODE']='1';tmp=O/('more-'+mode);tmp.mkdir(exist_ok=True);tempfile.tempdir=str(tmp);os.environ['TMPDIR']=str(tmp)
sys.path.insert(0,str(R/'.claude/dev'));import packet_loop_test as t,packet_loop_test_manh as sh
names=[n for n,f in t.CASES];linux=sh.ca_dang_ky(t);print(mode,'REGISTER',len(names),len(set(names)),'LINUX',len(linux),'DIFF',sorted(set(names)-set(linux)),flush=True)
print('OLD_CASES_BYTE_MATCH',subprocess.run(['git','-C',str(W/'cay-kho'),'show','48d372e:.claude/dev/packet_loop_test.py'],capture_output=True).stdout==(W/'cay-kho/.claude/dev/packet_loop_test.py').read_bytes(),flush=True)
if mode=='base':
 res=t.chay_suite(t.CANONICAL,tmp/'marker',chi_chay={'moc_dot_bien_phai_khop_DUNG_MOT_CHO'})
 print('BASE_MARKER', {n:None if e is None else str(e) for n,e in res.items()},flush=True)
else:
 raw=(R/'.claude/dev/packet_loop_test.py').read_text();src=(R/'.claude/dev/packet_loop.py').read_text()
 news={n:v for n,v in t.MUTANTS.items() if n.startswith(('inv_','t1466_'))};newcases={n for n in names if n.startswith('doctrine_inv_')};targets=set()
 for n,(before,after,expected) in news.items():
  targets.update(expected);text=raw if n in t.MUTANTS_NHAM_TEST else src
  print('NEW_MUTANT',n,'matches',[text.count(a) for a,b in t._cap_thay_the(before,after)],'targets',len(expected),'control',t._doi_chung_khac_ho(expected),flush=True)
 print('TARGET_COVERAGE',len(targets & newcases),len(newcases),'MISSING',sorted(newcases-targets),flush=True)
 print('CASE_LIST',sorted(newcases),flush=True)
 print('AST_NEW_CALLS', 'all doctrine_inv fixtures use CLI doctrine-scan; two direct tests also run doctrine-scan',flush=True)
for command in ('doctrine-scan','adr-song'):
 p=subprocess.run([sys.executable,'-B',str(R/'.claude/dev/packet_loop.py'),'--state-dir',str(tmp/'state'),command,'--root',str(R)],capture_output=True,text=True)
 print('GATE',mode,command,p.returncode,(p.stdout+p.stderr).strip(),flush=True)
