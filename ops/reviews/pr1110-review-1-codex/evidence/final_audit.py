import re
from audit_common import *

errors = []
before = json.loads((E / 'original-snapshot.json').read_text())
after = snapshot()
if before != after:
    errors.append('original repository snapshot changed')
state = {}
for name, root in [('cay-kho', REPO)] + [(x, S / 'work' / x) for x in ['head', 'base', 'mutant']]:
    status = git('status', '--porcelain=v1', '--untracked-files=all', '--ignored', cwd=root).decode()
    head = git('rev-parse', 'HEAD', cwd=root).decode().strip()
    tree = git('rev-parse', 'HEAD^{tree}', cwd=root).decode().strip()
    state[name] = dict(status=status, head=head, tree=tree)
    if status or head != (BASE if name == 'base' else HEAD):
        errors.append('head/status mismatch: ' + name)
gates = {}
for label in ['head', 'base']:
    data = json.loads((E / f'{label}-gates.json').read_text())
    gates[label] = {x['name']: x['rc'] for x in data}
    if any(x['rc'] for x in data):
        errors.append('failed gate: ' + label)
same_logs = {}
for gate in ['land', 'direct', 'doctrine', 'diff-check']:
    same_logs[gate] = (E / f'head-{gate}.stdout').read_bytes() == (E / f'base-{gate}.stdout').read_bytes()
    if not same_logs[gate]:
        errors.append('unexpected output delta: ' + gate)
warning_head = (E / 'head-direct.stderr').read_text().replace(str(S / 'work/head'), '<checkout>')
warning_base = (E / 'base-direct.stderr').read_text().replace(str(S / 'work/base'), '<checkout>')
warnings_equal = warning_head == warning_base
if not warnings_equal:
    errors.append('unexpected warnings delta')
mutation = json.loads((E / 'mutation.json').read_text())
if mutation['bien-nhan']['rc'] != 1 or mutation['direct']['rc'] != 1 or not mutation['restored_bytewise'] or mutation['status_after']:
    errors.append('mutation incomplete')
for path in ['archive.json', 'receipt.json', 'readme.json']:
    if json.loads((E / path).read_text())['errors']:
        errors.append('errors in ' + path)
out = dict(original_snapshot_files=len(before), original_snapshot_equal=before == after,
           states=state, gate_rcs=gates, stdout_equal=same_logs,
           syntax_warnings_equal=warnings_equal, mutation_restored=mutation['restored_bytewise'], errors=errors)
save('final-integrity.json', out)
print(json.dumps(out, ensure_ascii=False, indent=2))
assert not errors
