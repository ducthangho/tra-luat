import json,subprocess,sys,os,time
from review_measure import W,R,C,save,sha
Q=R/'ops/reviews/wp1236-r10-soan/quet_dot_bien.py';D=R/'ops/reviews/wp1236-r10-soan'
pilot=[json.loads(x) for x in (D/'pilot_c2d606b_kq.jsonl').read_text().splitlines()];old=next(x for x in pilot if x['giet'])
# Benign original source (known 36/36) replaces the previous mutant at the same id.
source=(C/'ops/gate_output_doi_chieu.py').read_text();m={'id':old['id'],'op':old['op'],'sha256':sha(source.encode()),'src':source}
(W/'resume_manifest.jsonl').write_text(json.dumps(m)+'\n');(W/'resume_kq.jsonl').write_text(json.dumps(old)+'\n')
env=dict(os.environ,TMPDIR=str(W/'tmp'),PYTHONDONTWRITEBYTECODE='1');out=[]
for name,result,test in [('resume',W/'resume_kq.jsonl',C/'ops/gate_output_doi_chieu_test.py'),('missing_test',W/'missing_test_kq.jsonl',W/'test_does_not_exist.py')]:
 cmd=[sys.executable,'-B',str(Q),'chay',str(W/'resume_manifest.jsonl'),str(test),'--ra',str(result),'--song-song','1']
 t=time.monotonic();p=subprocess.run(cmd,capture_output=True,env=env,cwd=W)
 (W/f'{name}.stdout').write_bytes(p.stdout);(W/f'{name}.stderr').write_bytes(p.stderr)
 out.append({'name':name,'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'seconds':time.monotonic()-t,'input_sha256':m['sha256'],'result':json.loads(result.read_text())})
save('runner_audit.json',out);print('RUNNER_AUDIT_COMPLETE',json.dumps(out,ensure_ascii=False))
