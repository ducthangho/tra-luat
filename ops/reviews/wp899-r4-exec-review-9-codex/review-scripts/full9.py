import hashlib, importlib.util, json, os, pathlib, subprocess, sys, time
R=pathlib.Path(__file__).resolve().parent;root=R.parent
while not (R/'closed-sample.json').exists():time.sleep(1)
receipt=json.loads((R/'closed-sample.json').read_text());assert receipt['rc']==0
s=importlib.util.spec_from_file_location('test9',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
ds=dict(t.sinh_dot_bien_dong((root/'ops/ci_provenance.py').read_text()))
rows=json.loads((R/'closed8-results.json').read_text());lines=[]
for row in rows:
 assert hashlib.sha256(ds[row['id']].encode()).hexdigest()==row['source_sha256']
 detail=json.loads((R/row['evidence']).read_text());assert detail['process_rc']==0 and detail['rank']==row['rank']
 lines.append(f"[KQ] {row['id']} {row['source_sha256'][:16]} {row['rank']}\n")
p=R/'own-resume9.txt';p.write_text(''.join(lines))
print('CURRENT_SESSION_MEASURED',len(lines),'REMAINING',len(ds)-len(lines),flush=True)
cmd=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--dot-bien-dong','8']
env=dict(os.environ,CIP_DONG_TIEP=str(p),PYTHONDONTWRITEBYTECODE='1')
with (R/'full-closed.raw.stdout.txt').open('wb') as out,(R/'full-closed.raw.stderr.txt').open('wb') as err:
 z=subprocess.run(cmd,stdout=out,stderr=err,env=env)
(R/'full-closed-command9.json').write_text(json.dumps({'command':cmd,'rc':z.returncode,'reused_own_current_session':len(rows),
 'resume_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'total':len(ds)},indent=2))
print((R/'full-closed.raw.stdout.txt').read_text()[-1800:]);sys.exit(z.returncode)
