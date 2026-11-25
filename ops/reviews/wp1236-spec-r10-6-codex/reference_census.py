import os,sys,subprocess,concurrent.futures,collections
from review_measure import W,R,C,save,sha
E=R/'ops/reviews/wp1236-r9-soan'
def run(name):
 cmd=[sys.executable,'-B',str(E/(name+'.py')),'.'];p=subprocess.run(cmd,cwd=R,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp')))
 (W/(name+'.stdout')).write_bytes(p.stdout);(W/(name+'.stderr')).write_bytes(p.stderr)
 want=E/('do_tep.txt' if name=='thamchieu' else 'do_loi_khai.txt')
 return {'command':cmd,'cwd':str(R),'rc':p.returncode,'stdout_sha256':sha(p.stdout),'matches_frozen':p.stdout==want.read_bytes(),'last_lines':p.stdout.decode().splitlines()[-2:]}
with concurrent.futures.ThreadPoolExecutor(2) as ex: out=list(ex.map(run,['thamchieu','do_loi_khai']))
files=list((R/'ops/land').rglob('danh_gia_gate.py'))
save('reference_census.json',{'receipts':out,'generator_files':len(files),'generator_hash_counts':dict(collections.Counter(sha(p.read_bytes()) for p in files))})
print('REFERENCE_CENSUS_COMPLETE',out,flush=True)
