import sys, os, json, importlib.util, subprocess, hashlib
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('test_audit',root/'ops/ci_provenance_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
out=R/'mutants'; out.mkdir(exist_ok=True)
src=(root/'ops/ci_provenance.py').read_text(); original=out/'original.py'; original.write_text(src)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(R/'tmp'),TEMP=str(R/'tmp'),TMP=str(R/'tmp'))
def run(case,path,label):
    cmd=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--mot-ca',case]
    p=subprocess.run(cmd,capture_output=True,env=dict(env,CI_PROVENANCE_MA=str(path)),timeout=300)
    b=p.stdout+p.stderr; (out/f'{label}.txt').write_bytes(b)
    return {'command':cmd,'source':str(path),'rc':p.returncode,'output':b.decode('utf8','replace'),'sha256_output':hashlib.sha256(b).hexdigest()}
cache={}; results=[]
for name,old,new,prefix,*expected in list(t.DOT_BIEN)+list(t.TU_KIEM):
    case=next(c for c in t.CA if c.split('_')[0]==prefix)
    if case not in cache: cache[case]=run(case,original,'baseline-'+case)
    rec={'name':name,'case':case,'old':old,'new':new,'baseline':cache[case],'expected':expected[0] if expected else 'GIET'}
    if src.count(old)!=1: rec.update(rank='HONG',anchor_count=src.count(old))
    else:
        path=out/(name+'.py'); path.write_text(src.replace(old,new)); rec['mutant']=run(case,path,name)
        rec['rank']=t.phan_hang(rec['mutant']['rc'],rec['mutant']['output'],case) if rec['baseline']['rc']==0 else 'HONG'
    results.append(rec); (out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(name,rec['rank'],flush=True)
print('TOTAL',len(results),{x:sum(y['rank']==x for y in results) for x in ('GIET','SONG_SOT','TIN_DUNG_GIA','HONG')})
