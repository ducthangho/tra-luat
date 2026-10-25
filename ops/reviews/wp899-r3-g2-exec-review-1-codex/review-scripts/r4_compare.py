import sys,runpy,json,subprocess,contextlib,io,importlib.util
from pathlib import Path
import yaml
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('tc',root/'ops/ci_provenance_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
p=subprocess.run(['git','show','9e5019ef2e3b8d59345fff2165569c3281cba3b5:ops/ci_provenance.py'],capture_output=True,check=True)
old=R/'r2-source.py'; old.write_bytes(p.stdout); oldm=runpy.run_path(str(old))
results={}
for label,folder in [('r4_F02_env_metadata','r4_env'),('r4_F02_mixed_color','r4_mixed')]:
    d=R/'real'/folder; log=(d/'actions-shaped.log').read_text(); w=(d/'workflow.yaml').read_text()
    rest=t.RestGia({'id':5,'run_attempt':1,'event':'push','head_sha':t.H,'path':'.github/workflows/ci.yml','check_suite_id':9},[t.job(1)],{1:log})
    with t.moi_tam() as moi:
        o=R/'real'/('old-'+folder)
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            rc=oldm['main'](['thu','--repo','o/r','--run','5','--attempt','1','--out',str(o)],goi=rest,git=t.GIT.get,moi_tu=moi)
        pv=yaml.safe_load((o/'provenance.yaml').read_text())
    results[label]={'r2_rc':rc,'r2_gate':t.gate(pv),'r3':json.loads((d/'result.json').read_text())}
# Variants of both collision shapes: same job/different job, order, blocked decoy.
for label,folder,decoy in [('mixed','r4_mixed','python ops/ci_provenance_test.py\npython -B .review/emit.py'),('metadata','r4_env','python -B .review/emit.py\npython ops/ci_provenance_test.py')]:
    d=R/'real'/folder; log=(d/'actions-shaped.log').read_text(); base=yaml.safe_load((d/'workflow.yaml').read_text())
    for mode in ('other_after','other_before','same_job','blocked_decoy'):
        w=yaml.safe_load(yaml.safe_dump(base)); step={'run':decoy+'\n'}
        if mode=='blocked_decoy': step['env']={'A':'1'}
        if mode=='same_job': w['jobs']['j']['steps'].append(step)
        else:
            other={'if':False,'runs-on':'x','steps':[step]}
            w['jobs']=({'k':other}|w['jobs']) if mode=='other_before' else (w['jobs']|{'k':other})
        rc,_,prov,_=t.chay([(t.job(1),log)],wf=yaml.safe_dump(w))
        results[label+'_'+mode]={'rc':rc,'gate':t.gate(prov),'workflow':w}
(R/'r4-comparison.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
for key,v in results.items():
 print(key,('r2 gate '+v['r2_gate']['trang_thai']+' → r3 gate '+v['r3']['gate']['trang_thai']) if 'r2_gate' in v else v['gate']['trang_thai'])
