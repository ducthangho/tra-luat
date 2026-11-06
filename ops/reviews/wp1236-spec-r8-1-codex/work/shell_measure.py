import collections, importlib.util, json, os, pathlib, shutil, subprocess, sys, tempfile
BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE/'artifacts'))
sys.dont_write_bytecode = True
import probes_r8 as q
import gram
tempfile.tempdir = str(BASE/'tmp')

with tempfile.TemporaryDirectory(prefix='shell_check_') as d:
    p=pathlib.Path(d)
    (p/'ops').mkdir(); (p/'bin').mkdir()
    (p/'bin/python').symlink_to(sys.executable)
    py='from pathlib import Path\nPath("executed").write_text("failure reached")\nraise SystemExit(1)\n'
    for name in ('fault.py','.fault.py','0.py','ops/fault-1.py','ops/hong_test.py'):
        (p/name).write_text(py)
    (p/'ops/qua.py').write_text('import sys\nsys.stdout.write(sys.stdin.read())\n')
    (p/'fault.sh').write_text('false\n')
    (p/'pass.sh').write_text('true\n')
    env={'PATH':f'{p}/bin:/usr/bin:/bin'}
    def run(body, shell):
        marker=p/'executed'
        if marker.exists(): marker.unlink()
        (p/'s.sh').write_text(body)
        r=subprocess.run(q.SHELL[shell]+[str(p/'s.sh')],cwd=p,env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=10)
        return r.returncode, marker.exists()
    observed={}
    for name,(body,shell) in q.AM.items():
        if not isinstance(body,str) or shell=='pwsh': continue
        rc,executed=run(body,shell)
        observed[name]={'rc':rc,'failing_program_executed':executed}
    zero=[n for n,r in observed.items() if r['rc']==0]
    swallowed=[n for n in zero if observed[n]['failing_program_executed']]
    no_failure=[n for n in zero if not observed[n]['failing_program_executed']]
    forms=[]
    args=['', ' --', ' -', ' .', ' /', ' =', ' :', ' PATH=x', ' a=b:c-d_e.f/g', ' --json --strict', ' -- -c --command --file']
    paths=['fault.py','./fault.py','ops/../fault.py','.fault.py','0.py','ops/fault-1.py']
    for name in paths:
        for arg in args:
            for shell in q.SHELL:
                for lf in ('','\n'):
                    body=f'python {name}{arg}{lf}'
                    assert gram.cp(body,shell) is None
                    rc,executed=run(body,shell)
                    assert rc==1 and executed,(body,shell,rc,executed)
                    forms.append(('python',shell))
    for arg in args:
        for shell in q.SHELL:
            body=f'bash fault.sh{arg}\n'
            assert gram.cp(body,shell) is None
            rc,_=run(body,shell)
            assert rc==1
            forms.append(('bash',shell))
    pipes=0
    for commands in (
        'python fault.py | python ops/qua.py',
        'python ops/qua.py | python fault.py',
        'python ops/qua.py | python fault.py | python ops/qua.py',
        'bash fault.sh | bash pass.sh',
        'bash pass.sh | bash fault.sh',
        'python fault.py | bash pass.sh',
        'bash pass.sh | python fault.py',
    ):
        assert gram.cp(commands,'bash') is None
        assert run(commands,'bash')[0]==1
        pipes+=1
    result={'negative':len(q.AM),'g_count':sum(n.startswith('g_') for n in q.AM),'kt_count':sum(n.startswith('kt_') for n in q.AM),
            'rc_zero':len(zero),'failure_executed_and_rc_zero':len(swallowed),'rc_zero_without_failure':no_failure,
            'accepted_simple_tests':len(forms),'accepted_pipeline_tests':pipes,'lost_exit_code':0,
            'pwsh_available':shutil.which('pwsh'),'negative_observations':observed}
    (BASE/'shell_measure.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='negative_observations'},ensure_ascii=False,indent=2))
