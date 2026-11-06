import ast
import collections
import datetime
import hashlib
import importlib.util
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / 'repo'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def save(name, value):
    text = json.dumps(value, ensure_ascii=False, indent=2)
    (HERE / (name + '.json')).write_text(text + '\n', encoding='utf-8')
    return value

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def snapshot():
    files = {}
    for p in sorted(ROOT.rglob('*')):
        if p.is_symlink():
            files[str(p.relative_to(ROOT))] = {'link': str(p.readlink())}
        elif p.is_file():
            files[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    state = {'head': git('rev-parse', 'HEAD').decode().strip(),
             'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
             'status': git('status', '--porcelain', '--ignored').decode(), 'files': files}
    return state

def walk(obj, path='$'):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield path + '.' + str(k), k, v
            yield from walk(v, path + '.' + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f'{path}[{i}]')

def census():
    import yaml
    land = load('ops/kiem_ho_so_land.py', 'land')
    src = load('ops/land_evidence_nguon.py', 'src')
    base = ROOT / 'ops/land'
    counts = collections.Counter()
    details = []
    provs = []
    for p in sorted(base.glob('*-land-evidence.yaml')):
        blob = p.read_bytes()
        doc = yaml.safe_load(blob)
        claims = []
        for path, k, v in walk(doc):
            norm = ''.join(c for c in str(k).casefold() if c.isalnum())
            if 'gateoutput' not in norm or norm in {'gateoutputnguon', 'gateoutputnguonvagioihan', 'mocgateoutputrcdisposition'}:
                continue
            match = re.match(r'\s*([a-z_]+)(?=$|[\s—\-:(,.;])', v.casefold()) if isinstance(v, str) else None
            kind = match[1] if match and match[1] in {'measured', 'passed', 'not_measured'} else ('mapping' if isinstance(v, dict) else 'list' if isinstance(v, list) else 'other')
            counts['claim_' + kind] += 1
            claims.append({'path': path, 'kind': kind})
        exemption = p.name in src.MIEN_TRU_CUTOVER and hashlib.sha256(blob).hexdigest() == src.MIEN_TRU_CUTOVER[p.name]
        counts['l5_match'] += exemption
        counts['l5_lost'] += p.name in src.MIEN_TRU_CUTOVER and not exemption
        counts['records'] += 1
        counts['merge_commit_root'] += 'merge_commit' in doc
        counts['records_with_claims'] += bool(claims)
        l8_red = not exemption and any(c['kind'] != 'not_measured' for c in claims)
        counts['l8_red'] += l8_red
        status, why, landed = land._xet_mot_tep(p, yaml)
        counts['l6_' + status] += 1
        counts['landed_no_claims'] += landed and not claims
        pdir = p.with_name(p.name.removesuffix('-land-evidence.yaml') + '-provenance')
        files = []
        for q in sorted(pdir.rglob('*.yaml')):
            d = yaml.safe_load(q.read_bytes())
            if isinstance(d, dict) and d.get('schema') == 'ci_provenance/1':
                files.append(str(q.relative_to(ROOT)))
                provs.append({'path': str(q.relative_to(ROOT)), 'run': d['moc']['run'], 'jobs': len(d['moc']['gate_output']['jobs'])})
        counts['records_with_prov'] += bool(files)
        counts['prov_files'] += len(files)
        details.append({'path': p.name, 'claims': claims, 'provs': files, 'l8_red': l8_red, 'l6': status, 'l5_match': exemption})
    save('census', {'time': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'counts': dict(counts), 'details': details, 'provenance': provs,
                    'land_diff_4f03566_HEAD': git('diff', '--stat', '4f03566', 'HEAD', '--', 'ops/land').decode()})
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))

def workflow():
    import yaml
    ci = load('ops/ci_provenance.py', 'ci')
    wf = ci.doc_wf(git('show', '4f03566:.github/workflows/ci.yml').decode())
    p = yaml.safe_load((ROOT / 'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_bytes())
    jobs = [j for j in p['moc']['gate_output']['jobs'] if j['conclusion'] != 'skipped' and 'ubuntu-latest' in j['labels'] and j['name'] != 'chuan-bi']
    env = sorted(set().union(*[set(wf['jobs'][ci.ghep_job(j['name'], wf)].get('env', {})) for j in jobs]))
    checkout = [next(c for c in p['moc']['checkout'] if c['job_id'] == j['job_id']) for j in jobs]
    quick_jobs = json.loads((ROOT / 'ops/land/pr1055-wp1052-provenance/readback-jobs-41397205258.json').read_text())
    quick_jobs = quick_jobs.get('jobs', []) if isinstance(quick_jobs, dict) else quick_jobs
    quick = []
    for j in quick_jobs:
        if j['conclusion'] == 'skipped' or 'ubuntu-latest' not in j['labels'] or j['name'] == 'chuan-bi':
            continue
        key = ci.ghep_job(j['name'], wf)
        skip = [s for s in wf['jobs'][key]['steps'] if s.get('name', '').startswith('DUONG_NHANH - liet ke buoc bo qua')]
        quick.append({'name': j['name'], 'conclusion': j['conclusion'], 'yaml_skip_steps': len(skip),
                      'rest_skip_steps': len([s for s in j['steps'] if s['name'].startswith('DUONG_NHANH - liet ke buoc bo qua')]),
                      'echo_count': sum(s.get('run','').count('echo ') for s in skip)})
    special = {k: [s for s in v['steps'] if (k == 'chuan-bi' and 'ops/ci_duong_nhanh.py' in str(s.get('run', ''))) or
                  (k == 'gate-cong-cu-gop' and '--gop' in str(s.get('run', ''))) or
                  (k == 'gate-ops' and s.get('name','').startswith(('ci-duong-nhanh', 'DUONG_NHANH - kiem re', 'bien-nhan v2'))) or
                  (k == 'gate-nhanh-gop' and s.get('name', '').startswith('DUONG_NHANH - gom'))]
               for k, v in wf['jobs'].items()}
    special = {k: v for k, v in special.items() if v}
    data = {'J_pr1231': len(jobs), 'env_keys': env, 'checkout_passed': sum(c['trang_thai'] == 'passed' for c in checkout),
            'checkout_shas': sorted({c.get('sha') for c in checkout}), 'quick_J': quick, 'special_steps': special}
    save('workflow', data)
    print(json.dumps({k:v for k,v in data.items() if k != 'special_steps'}, ensure_ascii=False, indent=2))

def k7():
    import yaml
    ci = load('ops/ci_provenance.py', 'ci_k7')
    wf = ci.doc_wf(git('show', 'fe84620:.github/workflows/ci.yml').decode())
    tree = ast.parse((ROOT / 'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py').read_text())
    values = {}
    class Resolve(ast.NodeTransformer):
        def visit_Name(self, node):
            return ast.parse(repr(values[node.id]), mode='eval').body
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in {'JSON_OK', 'TL_SELFTEST', 'TL_SELFTEST_PATS', 'LUAT'}:
                values[name] = ast.literal_eval(Resolve().visit(node.value))
    p = yaml.safe_load((ROOT / 'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_bytes())
    rows = []
    env_allow = {'PYTHONIOENCODING', 'PYTHONUTF8', 'PYTHONDONTWRITEBYTECODE'}
    for job in p['moc']['gate_output']['jobs']:
        if job['conclusion'] == 'skipped' or 'ubuntu-latest' not in job['labels'] or job['name'] == 'chuan-bi':
            continue
        key = ci.ghep_job(job['name'], wf)
        job_yaml = wf['jobs'][key]
        _, rule = next(r for r in values['LUAT'] if job['name'].startswith(r[0]))
        for label, patterns in rule:
            hits = [(i, s) for i, s in enumerate(job_yaml['steps']) if (label in s.get('run', '') or
                    (label == values['TL_SELFTEST'] and s.get('name', '').startswith('tl selftest')))
                    and any(b['name'] == ci.ten_du_kien(s) and b['conclusion'] == 'success' for b in job['buoc'])]
            if len(hits) != 1:
                rows.append({'job': job['name'], 'label': label, 'hits': len(hits)})
                continue
            i, step = hits[0]
            # Step env keys are identical between F-that and the review baseline (verified Git diff).
            reasons = []
            for obj, level in ((wf, 'workflow'), (job_yaml, 'job')):
                if 'defaults' in obj or ci._env_chan(obj) or set(obj.get('env', {})) - env_allow:
                    reasons.append(level)
            if set(step) - ci.KHOA_BUOC - {'env'}:
                reasons.append('step_keys')
            if 'env' in step and not isinstance(step['env'], dict):
                reasons.append('step_env')
            if step.get('shell', 'bash') not in {'bash', 'pwsh', 'sh'}:
                reasons.append('shell')
            if step.get('continue-on-error', False) is not False:
                reasons.append('continue-on-error')
            if any(re.search('GITHUB_(ENV|PATH)', str(s.get('run', ''))) for s in job_yaml['steps'][:i]):
                reasons.append('prior_env')
            shell = shlex.shlex(step.get('run', ''), posix=False, punctuation_chars='|')
            shell.whitespace_split = True
            bare_pipe = '|' in list(shell)
            no_pipefail = bare_pipe and step.get('shell') in {None, 'sh'} and not any(
                x in step.get('run', '') for x in ('set -o pipefail', 'set -euo pipefail'))
            rows.append({'job': job['name'], 'step': step['name'], 'hits': 1,
                         'old_chan_buoc': ci.chan_buoc(wf, key, i), 'new_reasons': reasons, 'no_pipefail': no_pipefail})
    result = {'rows': rows, 'steps': len(rows), 'jobs': len({r['job'] for r in rows}),
              'bad_match': sum(r.get('hits') != 1 for r in rows),
              'old_blocked_jobs': len({r['job'] for r in rows if r.get('old_chan_buoc')}),
              'new_blocked_steps': sum(bool(r.get('new_reasons')) for r in rows),
              'no_pipefail_steps': sum(bool(r.get('no_pipefail')) for r in rows)}
    save('k7', result)
    print(json.dumps({k:v for k,v in result.items() if k != 'rows'}))

if sys.argv[1] == 'snapshot':
    out = snapshot()
    save(sys.argv[2], out)
    print('snapshot:', len(out['files']), 'files; head', out['head'], 'tree', out['tree'], 'status', repr(out['status']))
elif sys.argv[1] == 'census':
    census()
elif sys.argv[1] == 'workflow':
    workflow()
elif sys.argv[1] == 'k7':
    k7()
