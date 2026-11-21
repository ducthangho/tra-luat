"""Offline spec audit; all writes confined to this work directory."""
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from collections import Counter

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
R = W.parent / 'repo'
OLD = W.parents[1] / 'a-6-codex/repo'
OW = OLD.parent / 'work'
os.environ['TMPDIR'] = str(W / 'tmp')
(W / 'tmp').mkdir(exist_ok=True)
E = W / 'evidence'
E.mkdir(exist_ok=True)
OUT = {'scope': 'spec r10; r9 product is a reference, not an r10 implementation', 'receipts': []}

def run(cmd, cwd=R):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    OUT['receipts'].append({'command': cmd, 'cwd': str(cwd), 'rc': p.returncode,
                            'stdout': p.stdout, 'stderr': p.stderr})
    return p

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

G = load('r9_product', OLD / 'ops/gate_output_doi_chieu.py')
import yaml

for name in ['thamchieu', 'do_loi_khai']:
    p = run([sys.executable, '-B', f'ops/reviews/wp1236-r9-soan/{name}.py', '.'])
    (W / f'{name}.stdout').write_text(p.stdout)
    expected = R / 'ops/reviews/wp1236-r9-soan' / ('do_tep.txt' if name == 'thamchieu' else 'do_loi_khai.txt')
    OUT[name] = {'rc': p.returncode, 'last_lines': p.stdout.splitlines()[-2:],
                 'byte_match': p.stdout.encode() == expected.read_bytes(),
                 'stdout_sha256': hashlib.sha256(p.stdout.encode()).hexdigest()}

ref = 'refs/remotes/origin/ops/wp1236-r9-a-lease'
prefix = 'ops/reviews/wp1236-a-r9-ma-6-codex/'
OUT['source_ref_oid'] = run(['git', 'rev-parse', ref]).stdout.strip()
names = run(['git', 'ls-tree', '-r', '--name-only', ref, prefix]).stdout.splitlines()
for name in ['make_independent.py', 'make_extra.py', 'make_order_url.py', 'complete_reason_sweep.py',
             'scan_runner.py', 'run_scan.py', 'MANIFEST_SANDBOX.sha256', 'all_independent_results.json',
             'measurement_summary.json', 'equivalence.json', 'independent_contrasts.json',
             'real_waiver_matrix.json', 'run.json']:
    p = run(['git', 'show', ref + ':' + prefix + name])
    assert p.returncode == 0
    (E / name).write_text(p.stdout)

manifest = (E / 'MANIFEST_SANDBOX.sha256').read_text()
OUT['replay_sources'] = []
all_mutants = {}
for name in ['independent_mutants.jsonl', 'independent_corrected.jsonl', 'extra_mutants.jsonl',
             'order_url_mutants.jsonl', 'reason_complete_mutants.jsonl']:
    p = OW / name
    entry = {'name': name, 'in_git': prefix + name in names, 'sandbox_exists': p.is_file()}
    if p.is_file():
        b = p.read_bytes()
        sha = hashlib.sha256(b).hexdigest()
        entry.update(sha256=sha, manifest_match=(sha + '  ./' + name) in manifest)
        rows = [json.loads(line) for line in b.decode().splitlines()]
        entry['count'] = len(rows)
        for row in rows:
            all_mutants[row['id']] = row
        # Source artifacts copied byte-for-byte; no generated attack content.
        (E / name).write_bytes(b)
    OUT['replay_sources'].append(entry)
OUT['operator_examples'] = {k: {'kind': all_mutants[k]['kind'], 'line': all_mutants[k]['line']}
                            for k in ['key_alpha_only', 'ref_any_run', 'ref_txt_wild',
                                      'phi_substring', 'phi_skip_descendants', 'waiver_head_truthy'] if k in all_mutants}
OUT['early_return_ids'] = [k for k in all_mutants if k.startswith('delete_return_')]

spec = (W.parent / 'SPEC.md').read_text()
OUT['case_counts'] = {'A': re.findall(r'^\| (A[12]-\d+) ', spec, re.M),
                      'B': re.findall(r'^\| (B\d+) ', spec, re.M),
                      'C': re.findall(r'^\| (C\d+) ', spec, re.M)}
OUT['numstat'] = run(['git', 'diff', '--numstat', '0f9aa2a2cc697129e1f5be72feddf60986286865', 'HEAD'], OLD).stdout
OUT['r9_product_lines'] = len((OLD / 'ops/gate_output_doi_chieu.py').read_text().splitlines())
OUT['r9_test_lines'] = len((OLD / 'ops/gate_output_doi_chieu_test.py').read_text().splitlines())
OUT['reference_lines'] = {n: len((R / 'ops/reviews/wp1236-r9-soan' / n).read_text().splitlines())
                          for n in ['thamchieu.py', 'do_loi_khai.py']}
OUT['generator_inventory'] = dict(Counter(hashlib.sha256(p.read_bytes()).hexdigest()
                                         for p in (R/'ops/land').rglob('danh_gia_gate.py')))
OUT['base_land_diff'] = run(['git', 'diff', '--name-only', '8048551a9b1eb886c126d2a1a4df0f95fb285964', 'HEAD', '--', 'ops/land']).stdout

dg = R/'ops/land/pr1440-wp1319-provenance/danh-gia-gate-output-44669622916.txt'
pv = R/'ops/land/pr1440-wp1319-provenance/ci-provenance-44669622916/provenance.yaml'
b = dg.read_bytes()
y = yaml.safe_load(pv.read_text())

def fixture(name, transform=None, data=None):
    d = W/'tmp'/name
    d.mkdir(exist_ok=True)
    (d/dg.name).write_bytes(b if data is None else data)
    obj = copy.deepcopy(y)
    if transform:
        transform(obj)
    (d/'provenance.yaml').write_text(yaml.safe_dump(obj, allow_unicode=True, sort_keys=False))
    return d, G.kiem_tep(d/dg.name, d)

healthy, res = fixture('healthy')
OUT['fixture_control'] = res
OUT['parser'] = {}
lines = b.decode().splitlines()
job = next(x for x in lines if x.startswith('JOB '))
jid = job.split()[1]
skip = f'JOB {jid} {job.split(" [")[0].split(" ", 2)[2]}: skipped -> not_measured (khong suy pass)'
for name, pair in [('job_job',[job,job]),('skip_skip',[skip,skip]),('skip_job',[skip,job]),('job_skip',[job,skip])]:
    text = '\n'.join([lines[0], *pair, lines[-1]]) + '\n'
    OUT['parser'][name] = G.doc_danh_gia(text.encode())[1]
OUT['parser']['LF'] = G.kiem_tep(dg, dg.parent)
OUT['parser']['CRLF'] = fixture('crlf', data=b.replace(b'\n', b'\r\n'))[1]
OUT['parser']['CR_mixed'] = G.doc_danh_gia(b.replace(b'\n', b'\r\n', 2))[1]
OUT['parser']['CR_lone'] = G.doc_danh_gia(b.replace(b'-> passed:', b'-> passed: x\r', 1))[1]
OUT['duplicate_provenance'] = fixture('dup_p', lambda q:q['moc']['gate_output']['jobs'].append(copy.deepcopy(q['moc']['gate_output']['jobs'][0])))[1]

OUT['malformed'] = {}
for name, fn in [
    ('jobs_append_scalar', lambda q:q['moc']['gate_output']['jobs'].append(7)),
    ('jobs_replace_scalar', lambda q:q['moc']['gate_output']['jobs'].__setitem__(0, 7)),
    ('tap_jobs_string', lambda q:q['moc']['gate_output'].__setitem__('tap_jobs','x')),
    ('checkout_number', lambda q:q['moc'].__setitem__('checkout',7)),
    ('checkout_string_item', lambda q:q['moc']['checkout'].__setitem__(0,'x')),
    ('checkout_empty', lambda q:q['moc'].__setitem__('checkout',[])),
    ('labels_null', lambda q:q['moc']['gate_output']['jobs'][0].__setitem__('labels',None)),
]:
    OUT['malformed'][name] = fixture(name, fn)[1]

OUT['dot_path'] = {}
for p in [dg.name, './'+dg.name, '../'+dg.name]:
    OUT['dot_path'][p] = G.kiem_ho_so({'gate_output':'measured — '+p}, healthy)

sys.path.insert(0, str(R/'ops'))
K = load('kiem_land_audit', R/'ops/kiem_ho_so_land.py')
parity=[]; tokens=[]
for f in sorted((R/'ops/land').glob('*-land-evidence.yaml')):
    doc=yaml.safe_load(f.read_text())
    parity.append((f.name,G.la_landed(doc),K._xet_mot_tep(f,yaml)[2]))
    for path,val in G.loi_khai(doc):
        if isinstance(val,str):
            for name in G.tep_danh_gia(val):
                t=f.parent/(f.name[:-len('-land-evidence.yaml')]+'-provenance')/name
                tokens.append((f.name,name,t.is_file()))
OUT['landed_parity']={'total':len(parity),'landed':sum(x[1] for x in parity),'mismatch':[x for x in parity if x[1]!=x[2]]}
OUT['claim_paths']={'total':len(tokens),'found':sum(x[2] for x in tokens),'missing':[x for x in tokens if not x[2]]}
OUT['attempt_types']=[{'value':repr(v),'valid':type(v) is int and v>=1,'matches_header_1':type(v) is int and v==1} for v in [None,True,1,2,1.0,0]]

# Keep command output as evidence but omit large git source blobs from summary.
receipts=OUT.pop('receipts')
(W/'audit_receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
(W/'audit_r5.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
print('AUDIT_R5_COMPLETE')
print(json.dumps({k:OUT[k] for k in ['thamchieu','do_loi_khai','case_counts','numstat','replay_sources','landed_parity','claim_paths','malformed']},ensure_ascii=False,indent=2))
