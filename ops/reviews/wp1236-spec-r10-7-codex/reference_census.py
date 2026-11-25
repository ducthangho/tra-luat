import hashlib,json,subprocess,sys,time
from generate_review import W,R,ENV
out=[]
for n,ref in [('thamchieu.py','do_tep.txt'),('do_loi_khai.py','do_loi_khai.txt')]:
 cmd=[sys.executable,'-B',str(R/'ops/reviews/wp1236-r9-soan'/n),str(R)];st=time.monotonic();p=subprocess.run(cmd,cwd=R,env=ENV,capture_output=True)
 (W/(n+'.stdout')).write_bytes(p.stdout);(W/(n+'.stderr')).write_bytes(p.stderr)
 r={'command':cmd,'rc':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'matches_frozen':p.stdout==(R/'ops/reviews/wp1236-r9-soan'/ref).read_bytes(),'seconds':time.monotonic()-st,'last_lines':p.stdout.decode().splitlines()[-2:]};out.append(r);print(r,flush=True)
(W/'reference_census.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
