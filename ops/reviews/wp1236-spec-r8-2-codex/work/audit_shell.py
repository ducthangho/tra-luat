"""Only harmless exit-1/exit-0 programs; clean environment; exact shell argv from spec."""
import itertools, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W/'reference'))
from gram import cp
shells={None:['/bin/bash','-e'],'bash':['/bin/bash','--noprofile','--norc','-eo','pipefail'],'sh':['/bin/sh','-e']}
rows=[]
with tempfile.TemporaryDirectory(dir=W/'tmp',prefix='safe-shell-') as d:
    root=Path(d); (root/'bin').mkdir()
    os.symlink(sys.executable,root/'bin/python')
    env={'PATH':str(root/'bin')+':/usr/bin:/bin','HOME':str(root)}
    names=['x','_x','0x','a-b','ops/x','ops/../x']
    args=['','--','-e','-c','--json --strict','a=b',':','=','-','./','if then fi','time command exec','a/b:c=d_e-0.']
    for path in set(names+['ok']):
        for suffix in ['.py','.sh']:
            f=root/(path+suffix); f.parent.mkdir(exist_ok=True,parents=True)
            if suffix=='.py':
                f.write_text('from pathlib import Path\nPath("ran-python").touch()\nraise SystemExit('+('0' if path=='ok' else '1')+')\n')
            else:
                f.write_text('touch ran-bash\nexit '+('0' if path=='ok' else '1')+'\n')
    def run(body,shell):
        assert cp(body,shell) is None,body
        (root/'ran-python').unlink(missing_ok=True);(root/'ran-bash').unlink(missing_ok=True)
        (root/'body').write_text(body)
        c=subprocess.run(shells[shell]+[str(root/'body')],cwd=root,env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=10)
        assert c.returncode!=0,(body,shell,c.returncode)
        assert (root/'ran-python').exists() or (root/'ran-bash').exists(),(body,shell,c.stderr)
        return c.returncode
    for program,suffix in [('python','.py'),('bash','.sh')]:
        for path,arg,shell in itertools.product(names,args,shells):
            body=program+' '+path+suffix+(' '+arg if arg else '')
            body+='\n' if len(rows)%2 else ''
            rows.append((program,shell,run(body,shell)))
    pipes=[]
    for left,right in itertools.product(['python','bash'],repeat=2):
        ext=lambda p:'.py' if p=='python' else '.sh'
        for pos in range(3):
            body=' | '.join([f'{left} '+('x' if pos==0 else 'ok')+ext(left),
                            'python '+('x' if pos==1 else 'ok')+'.py',
                            f'{right} '+('x' if pos==2 else 'ok')+ext(right)])
            pipes.append((body,run(body,'bash')))
result={'single_commands':len(rows),'pipelines':len(pipes),'accepted_but_rc0':0,'all_programs_executed':True,'pwsh':shutil.which('pwsh')}
print(json.dumps(result))
(W/'shell.json').write_text(json.dumps(result,indent=2))
