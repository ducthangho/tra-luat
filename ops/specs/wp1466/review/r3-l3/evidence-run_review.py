import os, sys, pathlib, tempfile, inspect, json, time
ROOT=pathlib.Path(__file__).resolve().parent
TREE=ROOT/'prototype'
sys.dont_write_bytecode=True
os.environ['PYTHONDONTWRITEBYTECODE']='1'
TMP=ROOT/'tmp'/sys.argv[1]; TMP.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(TMP); tempfile.tempdir=str(TMP)
sys.path.insert(0,str(TREE/'.claude/dev'));os.chdir(TREE)
import packet_loop_test as t
import packet_loop_test_manh as sh
mode=sys.argv[1]
new={n for n,f in t.CASES if n.startswith('doctrine_inv_')}
old={n for n,f in t.CASES if not n.startswith('doctrine_inv_') and (n.startswith(('doctrine_','ac18_','ac19_')) or 'doctrine' in inspect.getsource(f))}
mut_new={n for n in t.MUTANTS if n.startswith(('inv_','t1466_'))}
mut_old={n for n,v in t.MUTANTS.items() if n not in mut_new and set(v[2]) & old}
print('COUNTS',json.dumps(dict(new=len(new),old=len(old),mut_new=len(mut_new),mut_old=len(mut_old),cases=len(t.CASES),mutants=len(t.MUTANTS))),flush=True)
if mode in ('new_mutants','old_mutants'):
    cases=new|{'doctrine_scan_repo_that_sach','doctrine_scan_sach_xanh'} if mode=='new_mutants' else old
    muts=mut_new if mode=='new_mutants' else mut_old
    kq=sh.chay(t,cases,lambda names:set(names)&muts)
    print('REAL_RESULT',repr((kq[0],len(kq[1]),kq[2],kq[3])),flush=True)
    sys.exit(kq[0])
else:
    cases=old|new if mode=='cases' else {n for n,f in t.CASES if n.startswith('adr_song_')}|{'moc_dot_bien_phai_khop_DUNG_MOT_CHO'}
    results=t.chay_suite(t.CANONICAL,TMP/'cases',chi_chay=cases)
    errors={n:str(e) for n,e in results.items() if e is not None}
    print('CASES_RESULT',len(results),len(results)-len(errors),json.dumps(errors,ensure_ascii=False),flush=True)
    sys.exit(bool(errors))
