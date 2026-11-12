import collections, hashlib, importlib.util, json, os, re, subprocess, sys
from pathlib import Path
import yaml

W = Path(__file__).resolve().parent
R = W.parent / 'repo'
sys.dont_write_bytecode = True
sys.path.insert(0, str(W / 'reference'))
from gram import cp

def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args])

sp = importlib.util.spec_from_file_location('g1', W / 'gate_output_doi_chieu.py')
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
p = yaml.safe_load((R / 'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_text())
wf = yaml.safe_load(git('show', 'fe84620:.github/workflows/ci.yml'))
rows, uses_before, old_block, new_block = [], [], set(), []
for j in p['moc']['gate_output']['jobs']:
    if j['conclusion'] == 'skipped' or j['name'] == 'chuan-bi' or 'ubuntu-latest' not in (j['labels'] or []):
        continue
    k = m.cp.ghep_job(j['name'], wf)
    rules = m._muc(m.LUAT_v1, j['name'])
    assert len(rules) == 1
    indexes = []
    for rule in rules[0]['buoc']:
        rest = [b for b in j['buoc'] if b['name'] in rule['ten'] and b['conclusion'] == 'success']
        assert len(rest) == 1, rest
        name = rest[0]['name']
        hits = [(i, s) for i, s in enumerate(wf['jobs'][k]['steps']) if m.cp.ten_du_kien(s) == name]
        assert len(hits) == 1
        i, s = hits[0]; indexes.append(i)
        rows.append((j['name'], name, cp(s.get('run'), s.get('shell'))))
        block = m.chan_k7(wf, k, i, rule['env'], m.LUAT_v1['ENV_JOB_CHO_PHEP'])
        if block: new_block.append((j['name'], name, block))
        if m.cp.chan_buoc(wf, k, i): old_block.add(j['name'])
    prior = wf['jobs'][k]['steps'][:min(indexes)]
    uses_before.append((j['name'], any(s.get('uses') == 'actions/setup-python@v5' for s in prior)))
names = set((name, reason) for _, name, reason in rows)
result = {'head': git('rev-parse', 'HEAD').decode().strip(), 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
    'A15': {'instances': len(rows), 'accepted': sum(x[2] is None for x in rows), 'rejected': sum(x[2] is not None for x in rows),
            'names': len(names), 'accepted_names': sum(x[1] is None for x in names), 'rejected_names': sum(x[1] is not None for x in names),
            'affected_jobs': len({x[0] for x in rows if x[2]}), 'chan_k7': new_block, 'chan_buoc_affected_jobs': len(old_block)},
    'uses_before_first_rule': [sum(v for _, v in uses_before), len(uses_before)],
    'checkout_sha': sorted({v['sha'] for v in p['moc']['checkout'] if v['trang_thai'] == 'passed'}),
    'all_checkout_jobs': len(p['moc']['checkout']), 'luat_sha256': m.bam(m.LUAT_v1)}
for script in ('ops/cai_cong_cu.sh', 'ops/cai_actionlint.sh'):
    result[script] = [i for i, line in enumerate(git('show', 'fe84620:' + script).decode().splitlines(), 1) if 'GITHUB_PATH' in line]
result['before_rule_scripts'] = {}
for target in ('ops/cai_cong_cu.sh', 'ops/cai_actionlint.sh'):
    ks = []
    for k, job in wf['jobs'].items():
        rule_names = {n for rule in m.LUAT_v1['MUC'] for b in rule['buoc'] for n in b['ten']}
        indexes = [i for i, s in enumerate(job.get('steps', [])) if s.get('name') in rule_names]
        if indexes and any(target in str(s.get('run', '')) for s in job['steps'][:min(indexes)]): ks.append(k)
    result['before_rule_scripts'][target] = ks
prov = []
for path in git('ls-tree', '-r', '--name-only', 'b796259', '--', 'ops/land').decode().splitlines():
    if '-provenance/' not in path or not path.endswith('.yaml'): continue
    data = yaml.safe_load(git('show', 'b796259:' + path))
    if not isinstance(data, dict) or data.get('schema') != 'ci_provenance/1': continue
    run = data['moc']['run']
    if run.get('event') == 'push' and run.get('loi_khai_rest_path') == '.github/workflows/ci.yml':
        jobs = [j for j in data['moc']['gate_output']['jobs'] if j['conclusion'] != 'skipped' and 'ubuntu-latest' in (j['labels'] or []) and j['name'] != 'chuan-bi']
        prov.append((run['run_id'], path, sorted(j['name'] for j in jobs) == sorted(m.LUAT_v1['JOB_BAT_BUOC'])))
result['r7_provenance'] = {'count': len(prov), 'matching': sum(x[2] for x in prov), 'earliest': min(prov)}
nums = [line.split('\t') for line in git('diff', '--numstat', '08bcb51...508d678').decode().splitlines()]
result['gen1_size'] = {'files': len(nums), 'added': sum(int(x[0]) for x in nums), 'deleted': sum(int(x[1]) for x in nums)}
result['estimate_arithmetic'] = 1620 + (25 - 15) + (-40 + 120 + 55 + 45 + 65 + 40 + 20 + 20)
source_hashes = []
d = W / 'reference/g1'
for sha, path in re.findall(r'^([0-9a-f]{64})  (.+)$', (d / 'README.md').read_text(), re.M):
    source_hashes.append((path, hashlib.sha256((d/path).read_bytes()).hexdigest() == sha))
result['g1_hashes'] = source_hashes
probes = json.loads((W / 'reference/probes_r8.json').read_text())
result['probes'] = {'reasons': dict(collections.Counter(v['grammar'] for v in probes['am'].values())),
    'rc0_not_run': [k for k,v in probes['am'].items() if v['rc_bash'] == 0 and not v['da_chay_ct_hong']],
    'not_executed_by_harness': [k for k,v in probes['am'].items() if v['rc_bash'] is None],
    'rc_nonzero': sum(v['rc_bash'] is not None and v['rc_bash'] != 0 for v in probes['am'].values())}
print(json.dumps(result, ensure_ascii=False, indent=2))
(W / 'metadata.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
