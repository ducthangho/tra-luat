import os,pathlib,sys,tempfile,json,re,collections
root=pathlib.Path('cay-kho').resolve(); out=pathlib.Path('out').resolve()
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['TMPDIR']=str(out/'tmp');tempfile.tempdir=str(out/'tmp')
sys.path.insert(0,str(root/'.claude/dev'))
import packet_loop_test as t
text=(root/'ops/specs/wp1466.md').read_text(); block=re.search(r'^~~~ p2-moi\n(.*?)^~~~',text,re.S|re.M)[1]
selected=set(re.findall(r'ca: `\.claude/dev/packet_loop_test.py::([^`]+)`',block))|{n for n,f in t.CASES if n.startswith(('adr_song_','doctrine_scan_'))}|{'moc_dot_bien_phai_khop_DUNG_MOT_CHO'}
print('SELECTED',len(selected),flush=True)
results={}
for n in sorted(selected):
 r=t.chay_suite(t.CANONICAL,out/'tmp'/'selected',chi_chay={n});results.update(r);print(n,{k:None if v is None else str(v) for k,v in r.items()},flush=True)
print('RESULT',len(results),'PASS',sum(v is None for v in results.values()),'FAIL_OR_SKIP',{k:str(v) for k,v in results.items() if v is not None},flush=True)
# Exact runnable inventory, without executing the suite.
import packet_loop_test_manh as sh
print('REGISTERED',len(t.CASES),'RUNNABLE_LINUX',len(sh.ca_dang_ky(t)),flush=True)
