import os,sys,subprocess,importlib.util,tempfile,json,hashlib,tarfile,io
from pathlib import Path
sys.dont_write_bytecode=True
K=Path('/home/user/rv773'); E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('tests',K/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
def log(name,rc,out):
 (E/(name+'.log')).write_text(f'rc={rc}\n{out}',encoding='utf8');print(name,'rc=',rc,out[-350:].replace('\n',' | '))
def cli(name,goc):
 r=subprocess.run([sys.executable,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(goc)],capture_output=True,text=True);log(name,r.returncode,r.stdout+r.stderr)
for name,hs,p in [
 ('offset-negative-after',"pre_merge_checks: ['2026-10-16T02:00:00-01:00']\n",{'readback-pr-9001.json':t.RB_PR}),
 ('offset-positive-before',"pre_merge_checks: ['2026-10-16T03:00:00+01:00']\n",{'readback-pr-9001.json':t.RB_PR}),
 ('fraction-after',"pre_merge_checks: ['2026-10-16T02:58:26.001Z']\n",{'readback-pr-9001.json':t.RB_PR}),
 ('directory-dot',"x: 'measured — ./'\n",{}),
 ('positive-number',"positive: 123\nnguon_positive: a.txt\n",{'a.txt':''}),
 ('source-number',"positive: '1/1'\nnguon_positive: 123\n",{}),
 ('duplicate-key',"x: 'measured — no source'\nx: ok\n",{}),
 ('mapping-time',"pre_merge_checks: {'2026-10-16T03:00:00+00:00': ok}\n",{'readback-pr-9001.json':t.RB_PR}),
]:
 with t.cay(hs,p) as root: cli(name,root)
# Benign internal source symlink; same-file alias must be rejected.
for name,selfref in [('symlink-source',False),('symlink-self',True)]:
 with t.cay("positive: '1/1'\nnguon_positive: alias.yaml\n",{'source.txt':'1/1'}) as root:
  prov=root/'ops/land'/t.PROV
  (prov/'alias.yaml').symlink_to(root/'ops/land'/t.TEN if selfref else prov/'source.txt')
  cli(name,root)
# Mutation of timezone normalization, all fourteen existing cases.
src=(K/'ops/land_evidence_nguon.py').read_text();old='return t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)';assert src.count(old)==1
with tempfile.TemporaryDirectory() as d:
 mutant=Path(d)/'mutant.py';mutant.write_text(src.replace(old,'return t.replace(tzinfo=datetime.timezone.utc)'))
 env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(mutant),PYTHONDONTWRITEBYTECODE='1')
 for case in t.CA:
  r=subprocess.run([sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca',case],env=env,capture_output=True,text=True);log('tz-mutation-'+case,r.returncode,r.stdout+r.stderr)
 for name,hs in [('negative',"pre_merge_checks: ['2026-10-16T02:00:00-01:00']\n"),('positive',"pre_merge_checks: ['2026-10-16T03:00:00+01:00']\n")]:
  with t.cay(hs,{'readback-pr-9001.json':t.RB_PR}) as root:
   r=subprocess.run([sys.executable,'-B',str(mutant),'--root',str(root)],capture_output=True,text=True);log('tz-mutant-probe-'+name,r.returncode,r.stdout+r.stderr)
for c in ['c6e2401','1a4c417','d60b9e6']:
 r=subprocess.run(['git','-C',str(K),'archive',c,'ops/land'],capture_output=True);assert r.returncode==0
 with tempfile.TemporaryDirectory() as d:
  with tarfile.open(fileobj=io.BytesIO(r.stdout)) as arc:arc.extractall(d,filter='data')
  r=subprocess.run([sys.executable,'-B',str(K/'ops/land_evidence_nguon.py'),'--root',d,'--tep','ops/land/pr765-wp743-land-evidence.yaml'],capture_output=True,text=True);log('history-'+c,r.returncode,r.stdout+r.stderr)
m=t.nap();m.MIEN_TRU_CUTOVER={};rc,out=t.kiem(m,K);log('no-exempt',rc,out)
paths=subprocess.check_output(['git','-C',str(K),'ls-tree','-r','--name-only','c73af7b','ops/land'],text=True).splitlines()
cut={Path(p).name:hashlib.sha256(subprocess.check_output(['git','-C',str(K),'show','c73af7b:'+p])).hexdigest() for p in paths if p.endswith(t.nap().DUOI)}
print('CUTOVER',len(cut),hashlib.sha256(json.dumps(sorted(cut.items())).encode()).hexdigest(),cut==t.nap().MIEN_TRU_CUTOVER)
# Demonstrate that two focused assertions kill by the intended c06 marker.
with tempfile.TemporaryDirectory() as d:
 mutant=Path(d)/'mutant.py';mutant.write_text(src.replace(old,'return t.replace(tzinfo=datetime.timezone.utc)'))
 tests=(K/'ops/land_evidence_nguon_test.py').read_text()
 anchor='    for pmc in ('
 additions='''    ky("pre_merge_checks: ['2026-10-16T02:00:00-01:00']\\n", p, 1, "offset am sau merge", "L3")
    ky("pre_merge_checks: ['2026-10-16T03:00:00+01:00']\\n", p, 0, "offset duong truoc merge")
'''
 assert tests.count(anchor)==1
 testfile=Path(d)/'land_evidence_nguon_test.py';testfile.write_text(tests.replace(anchor,additions+anchor))
 case='c06_l3_luot2_moc_sau_merged_at'
 for name,ma in [('original',K/'ops/land_evidence_nguon.py'),('mutant',mutant)]:
  r=subprocess.run([sys.executable,'-B',str(testfile),'--mot-ca',case],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(ma)),capture_output=True,text=True);log('extended-c06-'+name,r.returncode,r.stdout+r.stderr)
# Independent rename mutation of frozen list.
with tempfile.TemporaryDirectory() as d:
 mutant=Path(d)/'rename.py';mutant.write_text(src.replace('"plat-x8-land-evidence.yaml":','"plat-x9-land-evidence.yaml":'))
 r=subprocess.run([sys.executable,'-B',str(K/'ops/land_evidence_nguon_test.py'),'--mot-ca','c10_l5_danh_sach_dong_bang'],env=dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(mutant)),capture_output=True,text=True);log('rename-mutation',r.returncode,r.stdout+r.stderr)
