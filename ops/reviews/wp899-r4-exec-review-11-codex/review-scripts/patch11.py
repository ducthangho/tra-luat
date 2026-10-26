import ast, copy, hashlib, importlib.util, json, pathlib, sys
from unittest import mock

R = pathlib.Path(__file__).resolve().parent
root = R.parent
def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
t = load(root / 'ops/ci_provenance_test.py', 'test11')
src = (root / 'ops/ci_provenance.py').read_text()
tree = ast.parse(src)
fn = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'doc_wf')
tr = next(x for x in fn.body if isinstance(x, ast.Try))
assert len(tr.body) == 1 and isinstance(tr.body[0], ast.Assign)
assert ast.unparse(tr.body[0].value) == 'yaml.safe_load(van)'
assert ast.unparse(tr.handlers[0].type) == 'Exception'
m = load(root / 'ops/ci_provenance.py', 'product11')
rows = []
class ParserFault(Exception): pass
for err in (OverflowError, LookupError, TypeError, RuntimeError, OSError, ParserFault):
    with mock.patch.object(m.yaml, 'safe_load', side_effect=err('fixture injection')):
        answer = m.doc_wf('jobs: {}')
    rows.append({'test': 'parse_exception', 'class': err.__name__, 'answer': answer})
    assert answer is None
for err in (KeyboardInterrupt, SystemExit):
    with mock.patch.object(m.yaml, 'safe_load', side_effect=err('fixture injection')):
        try: m.doc_wf('jobs: {}')
        except BaseException as e: answer = type(e).__name__
        else: answer = 'swallowed'
    rows.append({'test': 'base_exception', 'class': err.__name__, 'answer': answer})
    assert answer == err.__name__
class DictSubclass(dict): pass
for value in (None, [], 'jobs', 4, {}, {'jobs': []}, {'jobs': None}, DictSubclass(jobs={}), {'jobs': DictSubclass()}, {'jobs': {}}):
    with mock.patch.object(m.yaml, 'safe_load', return_value=value):
        answer = m.doc_wf('jobs: {}')
    expected = value if type(value) is dict and type(value.get('jobs')) is dict else None
    assert answer is expected
    rows.append({'test': 'type_gate', 'input_repr': repr(value), 'input_type': type(value).__name__, 'answer': answer})
case = next(c for c in t.CA if c.startswith('c52_'))
baseline = t.chay_con(case, root / 'ops/ci_provenance.py')
assert baseline[0] == 0
mutants = []
handlers = ['yaml.YAMLError', 'RecursionError', 'ValueError', 'KeyError', 'IndexError', 'AttributeError', 'OverflowError',
            'LookupError', 'TypeError', '(yaml.YAMLError, RecursionError, ValueError, KeyError, IndexError, AttributeError)']
for i, catch in enumerate(handlers):
    changed = copy.deepcopy(tree)
    cf = next(x for x in changed.body if isinstance(x, ast.FunctionDef) and x.name == 'doc_wf')
    ct = next(x for x in cf.body if isinstance(x, ast.Try))
    ct.handlers[0].type = ast.parse(catch, mode='eval').body
    source = ast.unparse(ast.fix_missing_locations(changed))
    p = R / f'patch-catch-{i}.py'
    p.write_text(source)
    rc, output = t.chay_con(case, p)
    rank = t.phan_hang(rc, output, case)
    mutants.append({'catch': catch, 'path': p.name, 'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                    'case': case, 'rc': rc, 'output': output, 'rank': rank})
    assert rank == 'GIET', mutants[-1]

# Supplemental executable test for the boundary of the try block: an error in
# validation after safe_load must remain observable. No new malformed YAML.
changed = copy.deepcopy(tree)
cf = next(x for x in changed.body if isinstance(x, ast.FunctionDef) and x.name == 'doc_wf')
ct = next(x for x in cf.body if isinstance(x, ast.Try))
ret = cf.body.pop()
ct.body.append(ret)
source = ast.unparse(ast.fix_missing_locations(changed))
p = R / 'patch-wide-try.py'
p.write_text(source)
class ValidationFault(Exception): pass
def fail_type(_): raise ValidationFault('outside parsing')
scope = []
for label, path in [('head', root / 'ops/ci_provenance.py'), ('mutant', p)]:
    mod = load(path, 'scope_' + label)
    mod.type = fail_type
    try: result = mod.doc_wf('jobs: {}')
    except ValidationFault: result = 'ValidationFault'
    scope.append({'source': label, 'answer': result})
assert scope == [{'source': 'head', 'answer': 'ValidationFault'}, {'source': 'mutant', 'answer': None}]
t.CA['r11_scope_outside_parse'] = lambda: t.bang(scope[1]['answer'] == 'ValidationFault', 'validation exception swallowed')
scope_rc, scope_output = t.chay_ca('r11_scope_outside_parse')
assert scope_rc == 3 and scope_output.startswith('DO:r11_scope_outside_parse:')
mutants.append({'mutation': 'widen try to include the type gate', 'path': p.name,
                'case': 'r11_scope_outside_parse', 'case_rc': scope_rc,
                'output': scope_output, 'rank': t.phan_hang(scope_rc, scope_output, 'r11_scope_outside_parse'),
                'independent_test_not_repository_case': True, 'observations': scope})
report = {'single_parse_call': True, 'baseline': baseline, 'injections_and_types': rows, 'mutants': mutants}
(R / 'patch11-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
print('PATCH11: single parse call; 18 fault/type controls; 10 narrowing mutants killed in c52; wide-try killed by supplemental boundary test')
