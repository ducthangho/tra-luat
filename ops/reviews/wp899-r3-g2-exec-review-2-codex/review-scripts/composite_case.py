import sys, json, subprocess, importlib.util, os, hashlib
from pathlib import Path
import yaml
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('composite_tests',root/'ops/ci_provenance_test.py')
t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
target='ops/ci_provenance_test.py'; call='python '+target
d=R/'composite'; d.mkdir(exist_ok=True)
wf={'name':'composite-origin-fixture','on':'push','jobs':{
 'actual':{'runs-on':'ubuntu-latest','steps':[{'uses':'./.review/composite'}]},
 'disabled':{'runs-on':'ubuntu-latest','if':False,'steps':[{'run':call+'\n'}]}}}
action={'name':'fixture-custom-shell','description':'Print stored output through a custom shell, without running the script argument.',
 'runs':{'using':'composite','steps':[{'run':call+'\n','shell':'python -B .review/emit.py {0}'}]}}
(d/'workflow.yml').write_text(yaml.safe_dump(wf))
(d/'action.yml').write_text(yaml.safe_dump(action))
(d/'runner-step.sh').write_text(call+'\n')
# Execute the shell command that a composite step requests, passing the runner
# script as {0}. The emitter prints only previously measured suite stdout.
(d/'invoke.sh').write_text('python -B .review/emit.py .review/composite/runner-step.sh\n')
cmd=['bash','-e','-x',str(d/'invoke.sh')]
proc=subprocess.run(cmd,cwd=root,capture_output=True)
(d/'stdout.txt').write_bytes(proc.stdout); (d/'trace.txt').write_bytes(proc.stderr)
rows=[f'{t.T} ##[group]Run ./.review/composite',f'{t.T} ##[endgroup]',
      f'{t.T} ##[group]Run {call}',f'{t.T} \x1b[36;1m{call}\x1b[0m',
      f'{t.T} shell: python -B .review/emit.py {{0}}',f'{t.T} ##[endgroup]']+[f'{t.T} {line}' for line in proc.stdout.decode().splitlines()]
lg=t.log_voi(rows)
(d/'actions-shaped.log').write_text(lg)
out={'source':{'path':str(t.MA),'sha256':hashlib.sha256(t.MA.read_bytes()).hexdigest()}}
for name,w in [('collision',wf),('no_collision',{'jobs':{'actual':wf['jobs']['actual']}}),
               ('blocked_collision',{'jobs':wf['jobs']|{'disabled2':{'runs-on':'ubuntu-latest','if':False,'steps':[{'run':call+'\n','env':{'A':'1'}}]}}})]:
    rc,stdout,prov,_=t.chay([(t.job(1,name='actual',steps=[{'name':'./.review/composite','conclusion':'success'}]),lg)],wf=yaml.safe_dump(w))
    out[name]={'rc':rc,'stdout':stdout,'gate':t.gate(prov)}
    (d/(name+'-provenance.yaml')).write_text(yaml.safe_dump(prov,allow_unicode=True))
out['shell']={'command':cmd,'rc':proc.returncode,'trace':proc.stderr.decode(),'stdout':proc.stdout.decode()}
(R/('composite-parent-case.json' if os.environ.get('CI_PROVENANCE_MA') else 'composite-case.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
assert proc.returncode==0 and '+ python '+target not in proc.stderr.decode()
if __name__=='__main__':
    case='F02_composite_origin_collision'
    try:
        t.bang(not any(z['duong_dan']==target and z['trang_thai']=='passed' for z in out['collision']['gate']['dau_duong']),
               'a skipped workflow run must not authenticate a composite action substep and its custom shell as execution of the target')
    except t.TinHieuChotCa as e:
        print('DO:'+case+':'+str(e)); sys.exit(3)
    print('DAT:'+case)
