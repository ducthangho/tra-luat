"""Independent reading of all five A14-S0 clauses; harmless Unicode path witnesses."""
import ast
import copy
import json
from pathlib import Path
import re
import sys
import types

W = Path(__file__).resolve().parent
sys.path.insert(0, str(W / 'soan'))
import gram
import khoa_ast_r8 as author
import probes_r8
import sinh_r8

blocks = re.findall(r'```python\n(.*?)\n```', (W.parent / 'SPEC.md').read_text(), re.S)
constants = next(b for b in blocks if b.startswith('P = r'))
function = next(b for b in blocks if b.startswith('def cu_phap_run('))
core = 'import re\n' + constants + '\n' + function + '\n'
plain_call = '\ndef kiem(b):\n    return cu_phap_run(b.get("run"), b.get("shell"))\n'
normalise = '''
import unicodedata
_original = cu_phap_run
def _normalise(run, shell):
    if type(run) is str:
        run = unicodedata.normalize("NFC", run)
    return _original(run, shell)
cu_phap_run = _normalise
'''
normalise_call = '''
import unicodedata
def kiem(b):
    b = dict(b)
    if type(b.get("run")) is str:
        b["run"] = unicodedata.normalize("NFC", b["run"])
    return cu_phap_run(b.get("run"), b.get("shell"))
'''

def ast_function(src):
    functions = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == 'cu_phap_run']
    assert len(functions) == 1
    f = copy.deepcopy(functions[0])
    if (f.body and isinstance(f.body[0], ast.Expr) and isinstance(f.body[0].value, ast.Constant)
            and type(f.body[0].value.value) is str):
        f.body.pop(0)
    return ast.dump(f, include_attributes=False)

def check(src):
    mod = types.ModuleType('candidate')
    exec(compile(src, 'candidate', 'exec'), vars(mod))
    ns = vars(mod)
    clauses = []
    clauses.append(all(ns[h] == getattr(gram, h) for h in ('P','W','DANG','LENH')))
    clauses.append(all(type(ns[h]) is re.Pattern and ns[h].pattern == getattr(gram,h).pattern
                       and ns[h].flags == re.compile('', re.ASCII).flags for h in ('RE_DON','RE_ONG')))
    clauses.append(ns['cu_phap_run'].__globals__ is ns and not ({'type','str'} & ns.keys()))
    clauses.append(ast_function(src) == ast_function(function))
    calls = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == 'cu_phap_run']
    try:
        step_name = calls[0].args[0].func.value.id if len(calls) == 1 else 'b'
        expected = ast.parse(f'cu_phap_run({step_name}.get("run"), {step_name}.get("shell"))', mode='eval').body
        clauses.append(len(calls) == 1 and ast.dump(calls[0], include_attributes=False) == ast.dump(expected, include_attributes=False))
    except (AttributeError, IndexError):
        clauses.append(False)
    return mod, clauses

table = list(probes_r8.AM.values()) + list(probes_r8.DUONG.values())
for path in ('g1/rv-a1-8/work/probes.py','g1/rv-a1-9/work/extra_shell_probes.py'):
    tree = ast.parse((W/'soan'/path).read_text())
    node = next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and getattr(n.targets[0],'id',None)=='cases')
    cmd = 'python .claude/dev/packet_loop_test.py'
    rows = eval(compile(ast.Expression(node),'cases','eval'),{'CMD':cmd,'PIPE':cmd+' | cat'})
    table += [(c[2]+'\n',c[1]) if 'rv-a1-8' in path else (c[1]+'\n',c[2]) for c in rows]
corpus = [(run,sh) for body in sinh_r8.kho() for sh in sinh_r8.SHELL for run in (body,body+'\n')]
out = {'table_n':len(table),'corpus_n':len(corpus),'variants':{}}
variants = {'baseline':core+plain_call,
            'comment_docstring':core.replace('    if type(run)', '    # comment\n    if type(run)')
                .replace('def cu_phap_run(run, shell):','def cu_phap_run(run, shell):\n    """docstring"""')+plain_call,
            'rebound_callable':core+normalise+plain_call,
            'normalised_step':core+normalise_call}
witness = 'python ops/\u212a.py'
for name, src in variants.items():
    mod, clauses = check(src)
    (W/(name+'.py')).write_text(src)
    result = {'A14_S0_clauses':clauses,'author_s0':author.kiem_s0(src),
              'direct_table_mismatches':sum(mod.cu_phap_run(r,s)!=gram.cp(r,s) for r,s in table),
              'direct_corpus_mismatches':sum(mod.cu_phap_run(r,s)!=gram.cp(r,s) for r,s in corpus),
              'caller_table_mismatches':sum(mod.kiem({'run':r,'shell':s})!=gram.cp(r,s) for r,s in table),
              'caller_corpus_mismatches':sum(mod.kiem({'run':r,'shell':s})!=gram.cp(r,s) for r,s in corpus),
              'witness':{'run':witness,'reference':gram.cp(witness,None),
                         'direct':mod.cu_phap_run(witness,None),'caller':mod.kiem({'run':witness,'shell':None})}}
    out['variants'][name] = result
    assert all(clauses) and not result['author_s0']
    assert all(result[k] == 0 for k in result if k.endswith('_mismatches'))
assert out['variants']['rebound_callable']['witness']['direct'] is None
assert out['variants']['normalised_step']['witness']['caller'] is None
(W/'audit_s0.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
