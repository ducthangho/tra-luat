import pathlib,hashlib,json,subprocess,sys
R=pathlib.Path.cwd(); out=R/'.review'
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True);return {'command':['git',*args],'rc':p.returncode,'stdout':p.stdout.decode('utf-8','replace'),'stderr':p.stderr.decode('utf-8','replace')}
d={str(p.relative_to(R)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in R.rglob('*') if p.is_file() and '.git' not in p.relative_to(R).parts and '.review' not in p.relative_to(R).parts}
a={'files':d,'git':[git(*args) for args in [('rev-parse','HEAD','HEAD^{tree}'),('status','--porcelain=v1','--untracked-files=all','--ignored=matching'),('diff','--binary'),('diff','--cached','--binary')]]}
(out/('snapshot-'+sys.argv[1]+'.json')).write_text(json.dumps(a,ensure_ascii=False,indent=1))
print('snapshot',sys.argv[1],len(d),'files'); print(json.dumps(a['git'],ensure_ascii=False))
