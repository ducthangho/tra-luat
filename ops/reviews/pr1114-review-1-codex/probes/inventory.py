import ast
import collections
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = ['ops/cloud_agent_creds_test.py', 'ops/cloud_agent_creds.py']
print('STATIC CALLS (head):')
def inventory(source, location):
    tree = ast.parse(source)
    for n in sorted(ast.walk(tree), key=lambda n: getattr(n, 'lineno', 0)):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and isinstance(n.func.value, ast.Name) and n.func.value.id == 'subprocess'
            and n.func.attr in ('run', 'Popen', 'check_call', 'check_output', 'call')):
            print(location + ':' + str(n.lineno), ast.unparse(n.func),
                  ast.unparse(n.args[0]) if n.args else '')
    return tree
for f in files:
    tree = inventory((root / 'cay-kho' / f).read_text(), f)
    if f.endswith('_test.py'):
        tl = next(n.value.value for n in tree.body if isinstance(n, ast.Assign)
                  and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'TL_GIA')
        tree = inventory(tl, 'TL_GIA')
        child = next(n.value.value for n in tree.body if isinstance(n, ast.Assign)
                     and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'CHAU')
        inventory(child, 'TL_GIA.CHAU')

for version in ('base', 'head'):
    rows = [json.loads(s) for s in (root / 'evidence' / (version + '-argv.jsonl')).read_text().splitlines()]
    print('\nOBSERVED', version, 'rows=' + str(len(rows)), 'actual_spawns=' + str(sum(r['kind'] == 'spawn' for r in rows)))
    groups = collections.defaultdict(list)
    for r in rows:
        if r['stack']:
            f, line, fn = r['stack'][0]
            groups[(Path(f).name, line, fn, r['kind'])].append(r)
    print('site | kind | count | max_UTF16_incl_NUL | max_arg_chars | max_input_bytes')
    for (f, line, fn, kind), rs in sorted(groups.items()):
        print(f'{f}:{line}:{fn} | {kind} | {len(rs)} | '
              f'{max(r["utf16_units_with_nul"] for r in rs)} | '
              f'{max(max(r["arg_chars"]) for r in rs)} | '
              f'{max(r["input_bytes"] for r in rs)}')
    if version == 'head':
        non_node = [r for r in rows if Path(r['executable']).name != 'node']
        longest = max(non_node, key=lambda r: r['utf16_units_with_nul'])
        print('HEAD_NON_NODE_MAX', longest['utf16_units_with_nul'], longest['stack'][0])
        gs = [r for r in rows if r['kind'] == 'run' and any(s[2] == 'chay_b' for s in r['stack'])]
        print('HEAD_CHAY_B_INPUT_MAX', max(r['input_bytes'] for r in gs))
