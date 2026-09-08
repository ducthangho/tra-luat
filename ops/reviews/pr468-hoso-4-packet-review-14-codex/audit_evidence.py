"""Read-only evidence audit; writes only into this scratch directory. No suites/CI."""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import time
import yaml

OUT = Path(__file__).resolve().parent
SANDBOX = OUT.parent
ROOT = SANDBOX / 'cay-kho'
REV = ROOT / 'ops/reviews'
GATE = REV / 'full-gate-pr468-20260907'
P13 = REV / 'pr468-hoso-4-packet-review-13-codex'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True).stdout

def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def full_gate():
    files = {p.name: {'bytes': p.stat().st_size, 'lines': len(p.read_bytes().splitlines()),
                      'sha256': sha(p.read_bytes())} for p in GATE.iterdir() if p.is_file()}
    rc = {}
    for side in ('nen', 'sau'):
        rc[side] = []
        for line in (GATE / (side + '.rc')).read_text().splitlines():
            parts = line.split()
            rc[side].append({'suite': parts[0], **dict(p.split('=') for p in parts[1:])})
    pairs = {}
    for suffix in ('cidk.tail.txt', 'ploop.tail.txt', 'lease.norm.out', 'doc-claims.json'):
        a, b = [(GATE / f'{side}.{suffix}').read_bytes() for side in ('nen', 'sau')]
        pairs[suffix] = {'equal_bytes': a == b, 'bytes_each': [len(a), len(b)],
                         'line_count': [len(a.splitlines()), len(b.splitlines())]}
    lease = (GATE / 'nen.lease.norm.out').read_text()
    doc = json.loads((GATE / 'nen.doc-claims.json').read_bytes())
    save('full-gate.json', {'files': files, 'rc_records_only': rc, 'pairs': pairs,
         'mutant_line_count': sum('đột biến' in s for s in lease.splitlines()),
         'mutant_empty_red_count': sum('ĐỎ=[]' in s for s in lease.splitlines()),
         'failure_lines': [s for s in lease.splitlines() if s.startswith('  ĐỎ')],
         'summary': lease.splitlines()[-1],
         'doc_summary': {k: v for k, v in doc.items() if k != 'claims'},
         'normalized_stable': re.sub(r'lp_[a-z0-9_]+', 'LP', lease) == lease,
         'fullgate_script_candidates': [str(p.relative_to(ROOT)) for p in ROOT.rglob('*fullgate*') if '.git' not in p.parts],
         'normalization_counterexample': [re.sub(r'lp_[a-z0-9_]+', 'LP', s) for s in ('error=lp_bad_permission', 'error=lp_no_permission')]})

def receipt():
    receipt_path = REV / 'pr468-hoso-4-packet-review-13-codex-verdict.receipt.yaml'
    r = yaml.safe_load(receipt_path.read_text())
    v = (ROOT / r['verdict_path']).read_bytes()
    model = r['model_reviewer_identity']
    evidence_commit = r['evidence_url'].split('/blob/')[1].split('/')[0]
    prompt = (P13 / 'bundle-PROMPT.md').read_bytes()
    same_verdict = v == (SANDBOX / 'VERDICT-luot13.md').read_bytes()
    logs = []
    for p in SANDBOX.rglob('run.json'):
        if '.git' in p.parts or 'kho.git' in p.parts:
            continue
        j = json.loads(p.read_bytes())
        logs.append({'path': str(p.relative_to(SANDBOX)), 'run_id': j.get('run_id'),
                     'short_id': j.get('short_id'), 'ten': j.get('ten'), 'head': j.get('head')})
    save('receipt.json', {'parsed': r, 'verdict_actual_bytes': len(v), 'verdict_actual_sha256': sha(v),
         'bytes_match': len(v) == r['verdict_bytes'], 'sha_match': sha(v) == r['verdict_sha256'],
         'provided_verdict_same_bytes': same_verdict,
         'reviewed_sha_in_verdict': re.findall(rb'^reviewed_sha: (\w+)$', v, re.M)[0].decode(),
         'evidence_commit': evidence_commit,
         'first_commit': git('log', '--reverse', '--diff-filter=A', '--format=%H', 'HEAD', '--', r['verdict_path']).decode().splitlines()[0],
         'evidence_blob_same': git('show', evidence_commit + ':' + r['verdict_path']) == v,
         'reviewed_ancestor_rc': subprocess.run(['git', 'merge-base', '--is-ancestor', r['reviewed_sha'], evidence_commit], cwd=ROOT).returncode,
         'prompt_sha256': sha(prompt), 'prompt_hash_matches': sha(prompt) == model['prompt_sha256'],
         'prompt_hash_file_matches': sha(prompt) == (P13/'bundle-PROMPT.sha256').read_text().strip(),
         'run_json_candidates': logs,
         'restart_field_present': 'so_lan_chet_truoc_khi_xong' in model or 'so_lan_chet_truoc_khi_xong' in r,
         'model_source_sessions': [str(p.relative_to(SANDBOX)) for p in SANDBOX.rglob('*.jsonl') if '.git' not in p.parts]})

def t33_probe():
    spec = importlib.util.spec_from_file_location('lease_test_readonly', ROOT / 'ops/lease_publish_test.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    oldpath = os.environ.get('PATH', '')
    binary = SANDBOX / 'cong-cu/actionlint/actionlint'
    rows = []
    for scenario, path in [('missing_actionlint', str(OUT/'empty-path')), ('provided_actionlint', str(binary.parent) + os.pathsep + oldpath)]:
        os.environ['PATH'] = path
        start = time.monotonic()
        try:
            module.t33_workflow_dang_lease_phai_qua_actionlint()
            result = {'outcome': 'passed'}
        except AssertionError as exc:
            result = {'outcome': 'assertion_failed', 'message': str(exc)}
        finally:
            os.environ['PATH'] = oldpath
        rows.append({'scenario': scenario, 'seconds': round(time.monotonic()-start, 6), **result})
    ver = subprocess.run([str(binary), '--version'], capture_output=True, text=True)
    checks = ['ops/lease_publish_test.py', '.github/workflows/ops-publish-lease.yml',
              '.claude/dev/ci_dang_ky_test.py', '.claude/dev/packet_loop_test.py',
              '.claude/dev/packet_loop.py', 'scripts/tl.py']
    blobs = {}
    for path in checks:
        values = {ref: git('rev-parse', ref + ':' + path).decode().strip()
                  for ref in ('b416830ef2a509d60203d55552ce17950afcf67c', 'f77f19895e00835d71644d82f1c54e9b519ccfe6', 'HEAD')}
        blobs[path] = {'oids': values, 'same': len(set(values.values())) == 1}
    save('t33-probe.json', {'scope': 'Only import and call t33; no main/suite', 'cases': rows,
         'actionlint_version': {'rc': ver.returncode, 'stdout': ver.stdout, 'stderr': ver.stderr}, 'blobs': blobs})

if __name__ == '__main__':
    full_gate()
    receipt()
    t33_probe()
    print('Wrote full-gate.json, receipt.json, t33-probe.json; no full suite run.')
