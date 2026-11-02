import ast
import copy
import contextlib
import io
import itertools
from pathlib import Path
import subprocess
import yaml

def git(*a):
    return subprocess.check_output(['git', *a], text=True)

for sha in ('e63961f', '816f43988eb3012726120ad00166a989cc2b9af6'):
    wf = yaml.safe_load(git('show', f'{sha}:.github/workflows/ci.yml'))
    jobs = wf['jobs']
    print(f'COMMIT {sha}')
    print('ci triggers:', wf.get('on', wf.get(True)))
    print('gate* count:', len([k for k in jobs if k.startswith('gate')]))
    for name, j in jobs.items():
        if name.startswith('gate'):
            ma = j.get('strategy', {}).get('matrix', {})
            print(f'  {name}: os={ma.get("os")}; exclude={ma.get("exclude")}; job-if={j.get("if")}')
    for name in ('gate-cong-cu', 'gate-cong-cu-gop'):
        ma = jobs[name]['strategy']['matrix']
        pairs = [dict(os=o, **({'manh':k} if k is not None else {})) for o, k in itertools.product(['ubuntu-latest','windows-latest'], ma.get('manh', [None]))]
        pairs = [p for p in pairs if not any(all(p.get(k) == v for k,v in x.items()) for x in ma.get('exclude', []))]
        print(f'expanded {name}: {pairs}')
    conditions = [(n, s.get('name', s.get('uses')), s['if']) for n,j in jobs.items() for s in j.get('steps',[]) if 'runner.os' in str(s.get('if',''))]
    print('step conditions using runner.os:', len(conditions), conditions)
    eol = next(s for s in jobs['gate']['steps'] if s.get('name') == 'PR head contains required EOL base')
    print('EOL step:', eol['if'])
    launch = yaml.safe_load(git('show', f'{sha}:.github/workflows/launcher-windows.yml'))
    print('launcher triggers:', launch.get('on', launch.get(True)))
    print('launcher matrix:', launch['jobs']['launcher']['strategy']['matrix'])
    print('launcher if:', launch['jobs']['launcher'].get('if'))
    paths = git('ls-tree', '-r', '--name-only', sha, '.github/workflows').splitlines()
    for p in paths:
        d = yaml.safe_load(git('show', f'{sha}:{p}'))
        runner = {n:j.get('runs-on') for n,j in d.get('jobs',{}).items()}
        print(f'workflow {p}: runs-on={runner}')

# Execute exactly the selected product functions, substituting only external inputs.
source = Path('ops/cong_cu_test.py').read_text()
tree = ast.parse(source)
names = {'nen_bo_qua_dot_bien', 'dat_windows', 'dong_windows', 'main'}
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
print('AST extracted:', [(n.name,n.lineno,n.end_lineno) for n in nodes])
class Skip(Exception): pass
def good(): pass
def skipped(): raise Skip('fixture: missing capability')
def bad(): raise AssertionError('fixture: baseline failed')
for label, ca, pre_skip, expected in (
    ('two pass + one skip', [good,good,skipped], False, 0),
    ('one failure', [good,bad,skipped], False, 1),
    ('all skipped', [skipped,skipped], False, 1),
    ('precheck skip', [good,good], True, 1),
):
    g = {'os':__import__('os'), '_TEN_NEN':'nt', 'CA':ca, 'DOT_BIEN':{'mutation':None},
         'BoQuaMoiTruong':Skip, 'batch_behavior_test':'batch', 'python_alias_behavior_test':'python',
         '_doc_che_do': lambda env: ('manh',(0,8,None)),
         '_chay_tien_kiem': lambda mod: (mod, 'fixture: unavailable') if pre_skip and mod == 'batch' else None}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), 'ops/cong_cu_test.py', 'exec'), g)
    with contextlib.redirect_stdout(io.StringIO()) as out:
        rc = g['main']()
    print(f'MAIN Windows simulated {label}: rc={rc}; ' + out.getvalue().strip().replace('\n',' | '))
    assert rc == expected
print('nen_bo_qua_dot_bien:', {x:g['nen_bo_qua_dot_bien'](x) for x in ('nt','posix','java')})
print('Windows runner thật: KHÔNG ĐO ĐƯỢC (môi trường Linux, không gọi mạng).')
