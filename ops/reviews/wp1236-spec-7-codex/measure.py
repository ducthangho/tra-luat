import ast
import collections
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / 'repo'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True)

def save(name, obj):
    obj = {'measured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), **obj}
    (HERE / (name + '.json')).write_text(json.dumps(obj, ensure_ascii=False, indent=2))
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def names():
    required5 = [f'{x} (ubuntu-latest)' for x in ['gate', 'gate-cong-cu-gop', 'gate-ops', 'gate-packet-loop', 'gate-registry']]
    required = required5 + ['gate-nhanh-gop (ubuntu-latest)'] + [f'{x} (ubuntu-latest, {i})' for x in ['gate-cong-cu', 'gate-nhanh-manh'] for i in range(8)]
    return required5, required

def jobs_j(jobs):
    return [j for j in jobs if j['conclusion'] != 'skipped' and 'ubuntu-latest' in (j.get('labels') or []) and j['name'] != 'chuan-bi']

def head_land(d):
    vals = [d.get('merge_commit')] + [v.get('merge_commit') for v in (d.get('prs') or []) if isinstance(v, dict)]
    return {x for x in vals if isinstance(x, str) and len(x) == 40}

def census():
    _, required = names()
    ps = []
    owners = set()
    windows = []
    records = sorted((ROOT / 'ops/land').glob('*-land-evidence.yaml'))
    for p in records:
        d = yaml.safe_load(p.read_text())
        h = head_land(d)
        subdir = p.with_name(p.name.replace('-land-evidence.yaml', '-provenance'))
        for f in sorted(subdir.rglob('*.yaml')):
            v = yaml.safe_load(f.read_text())
            if not isinstance(v, dict) or v.get('schema') != 'ci_provenance/1':
                continue
            owners.add(p.name)
            run = v['moc']['run']
            jobs = v['moc']['gate_output']['jobs']
            j = jobs_j(jobs)
            c = collections.Counter(x['name'] for x in j)
            ps.append({'path': str(f.relative_to(ROOT)), 'run': run['run_id'], 'event': run['event'], 'workflow': run['loi_khai_rest_path'], 'T': sum(x['conclusion'] != 'skipped' for x in jobs), 'J': len(j), 'missing': sorted(set(required)-set(c)), 'extra': sorted(set(c)-set(required)), 'duplicates': {k:n for k,n in c.items() if n > 1}})
            w = [x for x in jobs if x['conclusion'] != 'skipped' and 'windows-latest' in (x.get('labels') or [])]
            if w:
                windows.append({'record': p.name, 'run': run['run_id'], 'windows_jobs': len(w), 'event': run['event'], 'workflow': run['loi_khai_rest_path'], 'head': run['head_sha'], 'head_in_H': run['head_sha'] in h})
    pushci = [p for p in ps if p['event'] == 'push' and p['workflow'] == '.github/workflows/ci.yml']
    save('census', {'records': len(records), 'provenance_records': len(owners), 'provenance_files': len(ps), 'groups': dict(collections.Counter(p['event'] + ' ' + p['workflow'] for p in ps)), 'required_names': required, 'pushci_count': len(pushci), 'pushci_bad': [p for p in pushci if p['J'] != 22 or p['missing'] or p['extra'] or p['duplicates']], 'earliest_pushci': min(pushci, key=lambda p: p['run']), 'windows': windows, 'windows_heads_records': sorted({w['record'] for w in windows if w['head_in_H']})})
    (HERE / 'provenance-rows.json').write_text(json.dumps(ps, ensure_ascii=False, indent=2))

def load_ci():
    spec = importlib.util.spec_from_file_location('ci', ROOT / 'ops/ci_provenance.py')
    m = importlib.util.module_from_spec(spec)
    sys.modules['ci'] = m
    spec.loader.exec_module(m)
    return m

def law():
    src = ROOT / 'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py'
    env = {}
    for node in ast.parse(src.read_text()).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('JSON_OK', 'TL_SELFTEST', 'TL_SELFTEST_PATS', 'LUAT'):
            env[node.targets[0].id] = eval(compile(ast.Expression(node.value), str(src), 'eval'), {'__builtins__': {}}, env)
    return env['LUAT']

def candidate_steps(ci, job_key, wf, label):
    ys = [s for s in wf['jobs'][job_key]['steps'] if label in s.get('run', '') or label == '== tl selftest' and 'tl.py --selftest' in s.get('run', '')]
    # The law covers full Ubuntu push; these are alternate PR/Windows steps,
    # not ambiguous names in K7. Keep selection independent of REST outcome.
    return [s for s in ys if "runner.os != 'Linux'" not in s.get('if', '') and "github.event_name == 'pull_request'" not in s.get('if', '')]

def workflow():
    ci = load_ci()
    laws = law()
    prov = yaml.safe_load((ROOT / 'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_text())
    sha = {x['sha'] for x in prov['moc']['checkout'] if x['trang_thai'] == 'passed'}
    wf = ci.doc_wf(git('show', next(iter(sha)) + ':.github/workflows/ci.yml'))
    allrows = []
    missing = []
    env_keys = set()
    for job in jobs_j(prov['moc']['gate_output']['jobs']):
        k = ci.ghep_job(job['name'], wf)
        env_keys |= set(wf.get('env', {})) | set(wf['jobs'][k].get('env', {}))
        matches = [steps for prefix, steps in laws if job['name'].startswith(prefix)]
        if len(matches) != 1:
            missing.append(job['name'])
            continue
        for label, pats in matches[0]:
            ys = candidate_steps(ci, k, wf, label)
            rest = [s for s in job['buoc'] if len(ys) == 1 and s['name'] == ci.ten_du_kien(ys[0])]
            allrows.append({'job':job['name'], 'label': label, 'yaml_count': len(ys), 'rest': rest, 'step_name': ci.ten_du_kien(ys[0]) if len(ys) == 1 else None})
    base = ROOT / 'ops/land/pr1055-wp1052-provenance'
    run = json.loads((base / 'readback-run-41397205258.json').read_text())
    jobs = json.loads((base / 'readback-jobs-41397205258.json').read_text())['jobs']
    j = jobs_j(jobs)
    short_wf = ci.doc_wf(git('show', run['head_sha'] + ':.github/workflows/ci.yml'))
    missing_steps = {}
    for job in j:
        k = ci.ghep_job(job['name'], short_wf)
        matches = [steps for prefix, steps in laws if job['name'].startswith(prefix)]
        absent = []
        for label, pats in matches[0]:
            ys = candidate_steps(ci, k, short_wf, label)
            if len(ys) != 1 or not any(s['name'] == ci.ten_du_kien(ys[0]) and s['conclusion'] == 'success' for s in job['steps']):
                absent.append(label)
        if absent:
            missing_steps[job['name']] = absent
    _, required = names()
    save('workflow', {'F_ok_T': len(prov['log_day_du']), 'F_ok_J':len(jobs_j(prov['moc']['gate_output']['jobs'])), 'checkout_sha': sorted(sha), 'law_steps':len(allrows), 'bad_law_prefix': missing, 'bad_step_match':[r for r in allrows if r['yaml_count'] != 1 or len(r['rest']) != 1 or r['rest'][0]['conclusion'] != 'success'], 'env_job_keys':sorted(env_keys), 'short_run': {k: run[k] for k in ('id','run_attempt','event','head_sha')}, 'short_J':len(j), 'short_missing_jobs': sorted(set(required)-{x['name'] for x in j}), 'short_skipped':[{k: x.get(k) for k in ('name','conclusion','labels','runner_id','steps')} for x in jobs if x['conclusion'] == 'skipped'], 'short_jobs_missing_steps':len(missing_steps), 'short_missing_steps':missing_steps})
    (HERE / 'workflow-step-rows.json').write_text(json.dumps(allrows, ensure_ascii=False, indent=2))

def sizes():
    paths = ['ops/ci_provenance.py', 'ops/ci_provenance_test.py', 'ops/land_evidence_nguon.py', 'ops/land_evidence_nguon_test.py', 'ops/kiem_ho_so_land.py', 'ops/kiem_ho_so_land_test.py']
    rows = []
    for p in paths:
        commit = git('log', '--diff-filter=A', '--format=%H', '--', p).splitlines()[-1]
        rows.append({'path':p, 'commit':commit, 'numstat':git('show', '--format=', '--numstat', commit, '--', p).strip()})
    prototypes = {p:len((ROOT/p).read_text().splitlines()) for p in ['ops/land/pr1231-wp1105-provenance/danh_gia_gate.py', 'ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py']}
    save('sizes', {'created':rows, 'prototypes': prototypes, 'r7_component_sum':290+600+1, 'r7_deltas_module':40, 'r7_deltas_test':40+75+15+25, 'r6_component_plus_r7_deltas':250+450+1+40+40+75+15+25, 'upper_margin':950-900})

if __name__ == '__main__':
    globals()[sys.argv[1]]()
