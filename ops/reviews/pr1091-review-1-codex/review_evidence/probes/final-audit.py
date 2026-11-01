from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
repo = ROOT/'cay-kho'
evidence = ROOT/'evidence'

def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

pre = json.loads((evidence/'preflight.json').read_text())
checks = {}
checks['head'] = git('rev-parse', 'HEAD').decode().strip()
checks['tree'] = git('rev-parse', 'HEAD^{tree}').decode().strip()
checks['base'] = git('rev-parse', 'origin/master').decode().strip()
assert checks['head'] == pre['head'] == 'd58d649ff061ff125bc004414ed4a0787de8e5f3'
assert checks['tree'] == pre['tree']
assert checks['base'] == pre['base']
checks['status'] = git('status', '--porcelain=v1', '--untracked-files=all', '--ignored').decode()
assert checks['status'] == ''
for name, args in [('tracked', ['diff', '--binary', 'HEAD']), ('index', ['diff', '--cached', '--binary']), ('untracked', ['ls-files', '--others', '--exclude-standard']), ('ignored', ['ls-files', '--others', '--ignored', '--exclude-standard'])]:
    data = git(*args)
    (evidence/f'final-{name}.snapshot').write_bytes(data)
    assert data == b'', name
checks['source_files'] = {}
for path, expected in pre['files'].items():
    data = (repo/path).read_bytes()
    assert data == git('show', f"{checks['head']}:{path}")
    digest = hashlib.sha256(data).hexdigest()
    assert digest == expected
    checks['source_files'][path] = digest
assert git('diff', 'origin/master...HEAD') == (ROOT/'diff.patch').read_bytes()
assert (ROOT/'PROMPT.md').read_bytes() == (ROOT/'runs/6fd13df4/prompt.snapshot').read_bytes()
assert (evidence/'head-tests.rc').read_text().strip() == '0'
assert (evidence/'head-tests.log').read_text().strip() == 'cap-nhat-cong-cu tests: 116/116 ca QUA'
checks['head_tests'] = '116/116 rc0'

mutations = json.loads((evidence/'mutations.json').read_text()) + json.loads((evidence/'mutations-extra.json').read_text())
assert len(mutations) == 14 and len({v['name'] for v in mutations}) == 14
assert all(v['summary'] and not v['parser_error'] for v in mutations)
variants = [v for v in mutations if v['name'] != 'control']
assert len({(v['product_sha256'], v['test_sha256']) for v in mutations}) == 14
checks['mutations'] = dict(total=len(variants), killed=sum(v['rc'] != 0 for v in variants), survived=[v['name'] for v in variants if v['rc'] == 0])
assert checks['mutations']['killed'] == 9

hint_results = json.loads((evidence/'hint-validation.json').read_text())
assert len(hint_results) == 4
by_name = {v['name']: v for v in hint_results}
assert by_name['control']['summary'] == [['118', '118']] and by_name['control']['rc'] == 0
assert by_name['reset_no_T']['failed'] == ['dk_chay_reset_ca_cay_long_va_tep_an']
assert by_name['reset_after_copy_cached_condition']['failed'] == ['dk_chay_sua_tep_dacl_rong_truoc_khi_chep']
assert set(by_name['model_reset_noop']['failed']) == {'dk_chay_sua_tep_dacl_rong_truoc_khi_chep', 'dk_chay_reset_ca_cay_long_va_tep_an'}
assert all(v['rc'] == 1 and not v['parser_error'] for n,v in by_name.items() if n != 'control')
checks['hint_tests'] = '118/118 rc0; 3/3 target mutants killed'

def state(name):
    return json.loads((evidence/f'{name}.json').read_text())

head_empty = state('head_empty')
assert head_empty['tasks'] == 1 and head_empty['error'] == 'OFFLINE-DUNG-TRUOC-MAT-KHAU'
assert len(head_empty['states']) == 4
for node in head_empty['states']:
    assert len(node['access']) == 3 and node['violations'] == []
    assert node['owner'] == 'BUILTIN\\Administrators'
for name in ['no_reset_empty', 'after_copy_empty', 'after_copy_cached_empty']:
    data = state(name)
    assert data['tasks'] == 0 and 'denied' in data['error']
    assert not [e for e in data['events'] if e['type'] == 'do_acl']
assert sum(bool(n['violations']) for n in state('head_nested')['states']) == 0
assert sum(bool(n['violations']) for n in state('no_T_nested_original_model')['states']) == 0
assert sum(bool(n['violations']) for n in state('no_T_nested_recursive_model')['states']) == 3
checks['state_oracles'] = '7/7 expected outcomes; abstract ACL only'

native = state('native-wrapper')
assert native['native_ntfs'] == 'KHONG_DO_DUOC'
assert len(native['checks']) == 4
assert all(c['exact_argv'] for c in native['checks'][1:])
checks['native_wrapper'] = '3/3 argv/rc; enumeration Linux 1/1; Windows not measured'

hint_paths = re.findall(r'^\+\+\+ (.+)$', (ROOT/'HINT.patch').read_text(), re.M)
assert hint_paths == ['ops/vm/cap-nhat-cong-cu_test.ps1']
checks['hint_paths'] = hint_paths
checks['hint_sha256'] = hashlib.sha256((ROOT/'HINT.patch').read_bytes()).hexdigest()
checks['artifact_manifest'] = {}
for folder in ['evidence', 'probes']:
    for p in sorted((ROOT/folder).iterdir()):
        if p.is_file() and p.name not in ['final-audit.json', 'final-audit.log']:
            checks['artifact_manifest'][str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
(evidence/'final-audit.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ['source_files','artifact_manifest']}, ensure_ascii=False, indent=2))
print('Final audit: PASS; reviewed tree unchanged; exact head/base/diff and recorded oracles agree.')
