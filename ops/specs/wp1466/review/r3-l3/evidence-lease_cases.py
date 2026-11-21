from pathlib import Path
import sys,os,tempfile,json
O=Path(__file__).resolve().parent;P=O/'prototype';T=O/'lease-case-tmp';T.mkdir(exist_ok=True)
sys.dont_write_bytecode=True;os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['TMPDIR']=str(T);tempfile.tempdir=str(T);sys.path.insert(0,str(P/'.claude/dev'))
import packet_loop_test as t
cases={'r812_nguoi_giu_prefix_giao_nhau','r812_r8_symlink_hoa_thuong_doi_chung'}
print('SELECTED',cases,'FOUND',cases & {n for n,f in t.CASES},flush=True)
r=t.chay_suite(t.CANONICAL,T/'run',chi_chay=cases)
print('RESULT',{n:None if e is None else str(e) for n,e in r.items()},flush=True)
sys.exit(int(set(r)!=cases or any(e is not None for e in r.values())))
