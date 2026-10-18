#!/usr/bin/env python3
"""Independent offline r2 probes; all mutations occur in /tmp."""
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r2-suite')
sys.path.insert(0, str(repo / '.claude/dev'))
def load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    sp.loader.exec_module(m)
    return m
t = load('review812_tests', repo / '.claude/dev/packet_loop_test.py')
yaml = __import__('yaml')
scratch = Path(tempfile.mkdtemp(prefix='review812-r2-probes-'))
def ctx(name):
    p = scratch / name
    p.mkdir()
    return t.Ctx(t.CANONICAL, p)
def report(name, rc, sd, err, before, **extra):
    raw = (sd / 'wp55.json').read_bytes()
    st = json.loads(raw)
    print(json.dumps(dict(probe=name, rc=rc, state=st['state'], unchanged=raw == before,
        error=err.decode('utf-8', 'replace'), **extra), ensure_ascii=False), flush=True)

c = ctx('review')
rc, sd, err, before = t._r812(c, 'review')
assert rc == 0, err
w = c.tmp / 'kho/w'
bn_path = c.tmp / 'bn.yaml'
bn = yaml.safe_load(bn_path.read_bytes())
st = json.loads(before)
h = st['reviewing_head_sha']
validator = load('review812_receipt', repo / 'ops/bien_nhan_v2.py')
assert validator.PROVIDER_NGUON_HONG is None
assert validator._thieu(bn) == []
assert validator._neo_git(w, 'bn.yaml', bn) == ([], [])
report('positive-review-real-H', rc, sd, err, before, thieu=[], neo=[[], []])

def review(name, receipt=None, state=None, verdict='approve', ids=(), extra=()):
    raw_state = json.dumps(state).encode() if state is not None else before
    (sd / 'wp55.json').write_bytes(raw_state)
    bn_path.write_text(yaml.safe_dump(bn if receipt is None else receipt))
    rc, _, e = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'codex', '--verdict', verdict,
        '--reviewed-sha', h, '--codex-call', 'g1', '--bien-nhan', bn_path, '--root', w,
        *(x for i in ids for x in ('--finding-id', i)), *extra], sd)
    report(name, rc, sd, e, raw_state)
    return rc, json.loads((sd / 'wp55.json').read_bytes())

# Applicable exact r1 probes, with r2's genuine-H fixture.
for name, changes in [
    ('r1-chatgpt-as-codex', {'model_reviewer_identity': {**bn['model_reviewer_identity'], 'provider': 'openai_chatgpt'}}),
    ('r1-wrong-transport', {'model_reviewer_identity': {**bn['model_reviewer_identity'], 'transport': 'human'}}),
    ('r1-absent-git-anchor', {'verdict_path': 'ops/reviews/absent.md', 'evidence_url': 'https://github.com/o/r/blob/' + 'f' * 40 + '/ops/reviews/absent.md'}),
    ('r1-invalid-slug-newline', {'bang_lop': [{'slug': 'a\n', 'hang': 'P3'}]}),
]:
    review(name, {**bn, **changes})
(sd / 'wp55.json').write_bytes(before)
rc, _, e = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'codex', '--verdict', 'changes_requested',
    '--reviewed-sha', h, '--codex-call', 'g1', '--finding-id', 'executor-invented-class'], sd)
report('r1-negative-review-without-H', rc, sd, e, before)

# I4/I5: bad review at round cap; a valid closing review still records its result.
cap = copy.deepcopy(st)
cap['review_rounds_limit'] = 1
prior = dict(attempt=1, provider='codex', verdict='changes_requested', reviewed_sha=h, finding_ids=['old-class'], finding_descs=[])
cap['reviews'] = [prior]
cap['finding_counts'] = {'old-class': 1}
cap['review_rounds_used'] = 1
cap['codex_review_calls_used'] = 2
review('bad-H-at-round-cap', {**bn, 'verdict_sha256': 'b' * 64}, state=cap)
review('valid-close-at-round-cap', state=cap)
rc, closed = review('negative-close-at-round-cap', {**bn, 'verdict': 'changes_requested', 'bang_lop': [{'slug': 'a-b', 'hang': 'P2'}]}, state=cap, verdict='changes_requested', ids=['a-b'])
print(json.dumps({'probe': 'negative-close-ledger', 'reviews': len(closed['reviews']), 'attempt_open': closed['attempt_open']}, ensure_ascii=False), flush=True)
good_negative = {**bn, 'verdict': 'changes_requested', 'bang_lop': [{'slug': 'a-b', 'hang': 'P2'}]}
rc, closed = review('negative-valid-for-attempt-probe', good_negative, verdict='changes_requested', ids=['a-b'])
closed['attempts_limit'] = closed['attempts_used']
raw = json.dumps(closed).encode()
(sd / 'wp55.json').write_bytes(raw)
rc, _, e = t.run(t.CANONICAL, ['begin-attempt', '--packet', 55, '--provider', 'claude', '--bang-chung-moi-truong', scratch / 'absent.json'], sd)
report('r1-bad-doctor-at-attempt-cap', rc, sd, e, raw)

# New receipt input/state classes.
for key, value in [('reviewer', {}), ('executor', None), ('generation', False), ('required_checks', False)]:
    bad = copy.deepcopy(st)
    bad['ngu_canh_lease'][key] = value
    review('malformed-context-' + key, state=bad)
for name, changes in [
    ('executor-provider-mismatch', {'executor_provider': 'google_antigravity', 'model_executor_identity': {'model_family': 'claude', 'model_evidence': 'do_may', 'model_evidence_ref': 'r'}}),
    ('executor-surface-mismatch', {'model_executor_identity': {'provider': 'claude', 'surface': 'codex_cli', 'transport': 'machine/local'}}),
    ('executor-transport-mismatch', {'model_executor_identity': {'provider': 'claude', 'surface': 'claude_code', 'transport': 'human'}}),
]:
    review(name, {**bn, **changes})

def mutate_lease(w, changes, old=None):
    t._g(w, 'checkout', '-qb', 'ops/wp55-spec', 'refs/remotes/origin/ops/wp55-spec')
    p = w / 'ops/leases/l.yaml'
    lease = yaml.safe_load(p.read_bytes())
    lease.update(changes)
    p.write_text(yaml.safe_dump(lease))
    if old is not None:
        (w / 'ops/leases/old.yaml').write_text(yaml.safe_dump(old(lease)))
    t._g(w, 'add', '-A')
    t._g(w, 'commit', '-qm', 'reviewer fixture single-factor mutation')
    t._g(w, 'push', '-q', 'origin', 'ops/wp55-spec')
    t._g(w, 'checkout', '-q', 'master')
    t._g(w, 'branch', '-q', '-D', 'ops/wp55-spec')

for name, changes in [
    ('family-false', {'model_family': False}),
    ('family-list-empty', {'model_family': []}),
    ('reviewer-family-false', {'reviewer_model_family': False}),
    ('role-unknown', {'role': 'unassigned'}),
    ('generation-negative', {'generation': -1}),
    ('assurance-unknown', {'assurance_target': 'bogus'}),
    ('canonical-provider-alias', {'provider': 'anthropic_claude', 'executor': 'anthropic_claude'}),
    ('canonical-reviewer-alias', {'reviewer': 'openai_codex'}),
    ('prompt-dot', {'prompt_path': '.'}),
]:
    c2 = ctx(name)
    rc, sd2, e, pre = t._r812(c2, 'lease', truoc_lease=lambda w, d=changes: mutate_lease(w, d))
    report(name, rc, sd2, e, pre)

c2 = ctx('replacement')
def replacement(w):
    mutate_lease(w, {'thay_the_cho': ['old-lease']}, old=lambda l: {**l, 'lease_id': 'old-lease', 'thay_the_cho': [], 'da_bi_thay_the': l['lease_id']})
    lp = load('review812_lease', repo / 'ops/lease_publish.py')
    t._g(w, 'checkout', '-q', '--detach', 'refs/remotes/origin/ops/wp55-spec')
    result = lp.kiem(yaml.safe_load((w / 'ops/leases/l.yaml').read_bytes()), w / 'ops/leases/l.yaml', w)
    print(json.dumps({'probe': 'replacement-canonical-H-on-real-snapshot', 'passed': bool(result)}, ensure_ascii=False), flush=True)
    t._g(w, 'checkout', '-q', 'master')
rc, sd2, e, pre = t._r812(c2, 'lease', truoc_lease=replacement)
report('replacement-valid', rc, sd2, e, pre)

c2 = ctx('spec-only-in-ref')
rc, sd2, e, pre = t._r812(c2, 'lease', truoc_lease=t._R812_XOA_DAC_TA)
report('r1-valid-spec-only-in-ref', rc, sd2, e, pre)
print(json.dumps({'scratch': str(scratch)}), flush=True)
