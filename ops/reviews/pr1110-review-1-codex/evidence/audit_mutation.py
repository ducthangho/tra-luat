import re
from audit_common import *

root = S / 'work/mutant'
p = root / RECEIPT
original = p.read_bytes()
changed, n = re.subn(rb'(?m)^verdict_sha256: [0-9a-f]{64}$', b'verdict_sha256: ' + b'f' * 64, original)
assert n == 1 and original != changed
assert not git('status', '--porcelain=v1', cwd=root).strip()
results = {}
try:
    p.write_bytes(changed)
    diff = git('diff', '--numstat', cwd=root).decode().strip()
    assert diff == '1\t1\t' + RECEIPT
    for name, cmd in [
        ('bien-nhan', ['python3', 'ops/bien_nhan_v2.py', '--root', '.']),
        ('direct', ['python3', str(S / 'direct_gates.py'), '.'])
    ]:
        proc = run(cmd, root)
        (E / ('mutant-' + name + '.stdout')).write_bytes(proc.stdout)
        (E / ('mutant-' + name + '.stderr')).write_bytes(proc.stderr)
        output = (proc.stdout + proc.stderr).decode()
        red = re.findall(r'^\s*ĐỎ\s+(\S+\.receipt\.yaml):', output, re.M)
        result = dict(command=cmd, rc=proc.returncode, red_receipts=red,
                      target_lines=[l for l in output.splitlines() if Path(RECEIPT).name in l])
        if name == 'direct':
            direct = json.loads(proc.stdout)
            result['results'] = direct
        results[name] = result
        print(json.dumps(dict(gate=name, **result), ensure_ascii=False), flush=True)
finally:
    p.write_bytes(original)
    results['restored_bytewise'] = p.read_bytes() == original
    results['status_after'] = git('status', '--porcelain=v1', cwd=root).decode()
    results['one_field_diff_numstat'] = diff
    save('mutation.json', results)
assert results['bien-nhan']['rc'] == 1
assert results['bien-nhan']['red_receipts'] == [Path(RECEIPT).name]
assert results['direct']['rc'] == 1
direct = results['direct']['results']
assert direct[0]['name'].startswith('t26_') and direct[0]['result'] == 'FAIL'
assert Path(RECEIPT).name in direct[0]['error'] and 'LỆCH BĂM' in direct[0]['error']
assert all(x['result'] == 'PASS' for x in direct[1:])
assert results['restored_bytewise'] and not results['status_after']
print('mutation verified, original bytes restored; rc=0', flush=True)
