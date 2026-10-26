import hashlib, json, os, pathlib, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / '.review'
TMP = OUT / 'tmp'
TMP.mkdir(exist_ok=True)
def snapshot(label):
    files = {}
    for p in ROOT.rglob('*'):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in ('.git', '.review') or not p.is_file():
            continue
        b = p.read_bytes()
        files[str(rel)] = [len(b), hashlib.sha256(b).hexdigest()]
    git = {}
    for key, args in {'head':['rev-parse','HEAD'], 'tree':['rev-parse','HEAD^{tree}'], 'status':['status','--porcelain=v1','--untracked-files=all','--ignored=matching'], 'diff':['diff','--binary'], 'index':['diff','--cached','--binary']}.items():
        r = subprocess.run(['git',*args],cwd=ROOT,capture_output=True)
        git[key] = {'rc':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()}
    (OUT / (label+'.json')).write_text(json.dumps({'files':files,'git':git},ensure_ascii=False,indent=1))
    print(label, len(files), git['head']['stdout'].strip(), flush=True)
def run(label, cmd):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(TMP), TMP=str(TMP), TEMP=str(TMP), XDG_CACHE_HOME=str(OUT/'cache'))
    env.pop('CIP_DONG_TIEP',None)
    start=time.time()
    with (OUT/(label+'.stdout.txt')).open('wb') as out, (OUT/(label+'.stderr.txt')).open('wb') as err:
        r=subprocess.run(cmd,cwd=ROOT,env=env,stdout=out,stderr=err)
    info={'command':cmd,'rc':r.returncode,'elapsed':time.time()-start}
    for kind in ('stdout','stderr'):
        p=OUT/(label+'.'+kind+'.txt'); b=p.read_bytes()
        info[kind]={'path':str(p),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    (OUT/(label+'.json')).write_text(json.dumps(info,ensure_ascii=False,indent=2))
    print(json.dumps(info,ensure_ascii=False),flush=True)
    return r.returncode
if __name__=='__main__':
    if sys.argv[1]=='snapshot': snapshot(sys.argv[2])
    else: sys.exit(run(sys.argv[1],sys.argv[2:]))
