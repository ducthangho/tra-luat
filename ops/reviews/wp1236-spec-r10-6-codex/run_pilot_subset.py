import os, subprocess, sys, time
from review_measure import W,R,C,save,sha
cmd=[sys.executable,'-B',str(R/'ops/reviews/wp1236-r10-soan/quet_dot_bien.py'),'chay',str(W/'pilot_subset.jsonl'),str(C/'ops/gate_output_doi_chieu_test.py'),'--ra',str(W/'pilot_subset_kq.jsonl'),'--song-song','4']
t=time.monotonic()
with (W/'pilot_subset.stdout').open('wb') as out,(W/'pilot_subset.stderr').open('wb') as err:
 p=subprocess.run(cmd,cwd=W,stdout=out,stderr=err,env=dict(os.environ,TMPDIR=str(W/'tmp'),PYTHONDONTWRITEBYTECODE='1'))
save('pilot_subset_receipt.json',{'command':cmd,'rc':p.returncode,'seconds':time.monotonic()-t,'stdout_sha256':sha((W/'pilot_subset.stdout').read_bytes()),'stderr_sha256':sha((W/'pilot_subset.stderr').read_bytes())})
print('PILOT_SUBSET_DONE',p.returncode,(W/'pilot_subset.stdout').read_text(),flush=True)
