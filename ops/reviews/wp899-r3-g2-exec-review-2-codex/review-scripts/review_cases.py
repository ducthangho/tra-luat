import importlib.util, sys, json, subprocess
from pathlib import Path
import yaml
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('review_test',root/'ops/ci_provenance_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
TARGET='ops/ci_provenance_test.py'; CALL='python '+TARGET

def run_real(name,script,color,extra=()):
    d=R/'real'/name; d.mkdir(parents=True,exist_ok=True)
    (d/'script.sh').write_text(script+'\n')
    cmd=['bash','-e','-x',str(d/'script.sh')]
    p=subprocess.run(cmd,cwd=root,capture_output=True)
    (d/'stdout.txt').write_bytes(p.stdout); (d/'trace.txt').write_bytes(p.stderr)
    lines=script.splitlines(); rendered=[f'{t.T} ##[group]Run {lines[0]}']+[f'{t.T} '+ ('\x1b[36;1m'+line+'\x1b[0m' if i in color else line) for i,line in enumerate(lines)] + [f'{t.T} shell: /usr/bin/bash -e {{0}}',f'{t.T} ##[endgroup]']+[f'{t.T} {z}' for z in p.stdout.decode().splitlines()]
    wf=yaml.safe_load(t.wf_tu(script))
    for i,other in enumerate(extra): wf['jobs'][f'other{i}']={'runs-on':'x','if':False,'steps':[{'run':other+'\n'}]}
    wf=yaml.safe_dump(wf); log=t.log_voi(rendered)
    rc,out,prov,_=t.chay([(t.job(1),log)],wf=wf)
    (d/'workflow.yaml').write_text(wf); (d/'actions-shaped.log').write_text(log); (d/'provenance.yaml').write_text(yaml.safe_dump(prov,allow_unicode=True))
    result={'shell_command':cmd,'shell_rc':p.returncode,'trace':p.stderr.decode(),'tool_rc':rc,'stdout':out,'gate':t.gate(prov)}
    (d/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    t.bang(p.returncode==0 and '+ python '+TARGET not in p.stderr.decode(),'shell must succeed without executing target')
    return result

def r4_F02_mixed_color():
    script='if false; then\n'+CALL+'\nfi\npython -B .review/emit.py'
    r=run_real('r4_mixed',script,{1,3})
    t.bang(r['gate']['dau_duong']==[] and r['gate']['kich_ban']['buoc_xac_thuc']==0,'r4 mixed must not authenticate')

def r4_F02_env_metadata():
    script='python -B .review/emit.py'
    d=R/'real'/'r4_env'; d.mkdir(parents=True,exist_ok=True); (d/'script.sh').write_text(script+'\n')
    p=subprocess.run(['bash','-e','-x',str(d/'script.sh')],cwd=root,capture_output=True)
    rows=t.buoc(script,*p.stdout.decode().splitlines())
    at=next(i for i,z in enumerate(rows) if '##[endgroup]' in z)
    rows[at:at]=[f'{t.T} env:',f'{t.T}   DEMO_TEXT: metadata',f'{t.T} \x1b[36;1m{CALL}\x1b[0m']
    log=t.log_voi(rows); wf=t.wf_tu(script)
    rc,out,prov,_=t.chay([(t.job(1),log)],wf=wf)
    (d/'actions-shaped.log').write_text(log); (d/'workflow.yaml').write_text(wf); (d/'trace.txt').write_bytes(p.stderr); (d/'result.json').write_text(json.dumps({'shell_rc':p.returncode,'tool_rc':rc,'gate':t.gate(prov)},ensure_ascii=False,indent=2))
    t.bang(p.returncode==0 and t.gate(prov)['dau_duong']==[] and t.gate(prov)['kich_ban']['buoc_xac_thuc']==0,'r4 env must not authenticate')

def F02_collision_other_job():
    script='if false; then\n'+CALL+'\nfi\npython -B .review/emit.py'
    r=run_real('collision_other_job',script,{1,3},[CALL+'\npython -B .review/emit.py'])
    t.bang(not any(x['duong_dan']==TARGET and x['trang_thai']=='passed' for x in r['gate']['dau_duong']),'unexecuted target must not become passed through a different disabled job')

def F02_missing_endgroup():
    x='python '+t.DUONG_GIA
    log=t.log_voi(t.buoc(x,'THU: 4/4 dat')).replace(f'{t.T} ##[endgroup]\n','')
    rc,_,p,_=t.chay([(t.job(1),log)],wf=t.wf_tu(x)); g=t.gate(p)
    t.bang(rc==0 and g['dau_duong']==[] and g['kich_ban']['buoc_xac_thuc']==0,'no closing delimiter: unmeasured block must not authenticate or fail the gate')

def git_workflow_source():
    m=t.nap(); sha=t.H; path='.github/workflows/ci.yml'
    expected=subprocess.run(['git','cat-file','blob',sha+':'+path],cwd=root,capture_output=True,check=True).stdout.decode()
    actual=m.git_blob(sha,path)
    t.bang(actual==expected,'git_blob must return bytes from requested SHA/path, not current HEAD or nothing')
    t.bang(m.git_blob('0'*40,path) is None,'missing object must be unavailable')

def control_simple():
    x='python '+t.DUONG_GIA; rc,_,p,_=t.chay([(t.job(1),t.log_voi(t.buoc(x,'THU: 4/4 dat')))],wf=t.wf_tu(x))
    t.bang(rc==0 and t.gate(p)['trang_thai']=='passed','simple positive control')

CA={f.__name__:f for f in (r4_F02_mixed_color,r4_F02_env_metadata,F02_collision_other_job,F02_missing_endgroup,git_workflow_source,control_simple)}
if __name__=='__main__':
    case=sys.argv[1]
    try: CA[case]()
    except t.TinHieuChotCa as e: print(f'DO:{case}:{e}'); sys.exit(3)
    except Exception as e: print(f'HONG:{case}:{type(e).__name__}:{e}'); sys.exit(4)
    print('DAT:'+case)
