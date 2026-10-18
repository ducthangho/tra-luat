#!/usr/bin/env python3
"""Read only source review; every state/fixture is under /tmp."""
import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path('/tmp/wp812-r6-suite')
sys.path.insert(0, str(repo / '.claude/dev'))
def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m
t = load('probe_r4_tests', repo / '.claude/dev/packet_loop_test.py')
v = load('probe_r4_validator', repo / 'ops/bien_nhan_v2.py')
import yaml
out = Path(tempfile.mkdtemp(prefix='review812-r4-own-'))
def report(name, rc, sd, e, before, **extra):
    raw = (sd / 'wp55.json').read_bytes()
    print(json.dumps(dict(probe=name, rc=rc, state=json.loads(raw)['state'], unchanged=raw == before,
        traceback=b'Traceback' in e, error=e.decode('utf-8', 'replace'), **extra), ensure_ascii=False), flush=True)
def lease(name, changes, other=None):
    d = out / name
    d.mkdir()
    rc, sd, e, before = t._r812(t.Ctx(t.CANONICAL, d), 'lease', truoc_lease=lambda w: t._r812_doi_lease(
        w, changes, (lambda l: {'other.yaml': {**l, 'lease_id': 'other-lease', **other}}) if other else None))
    report(name, rc, sd, e, before)
lease('effective-disjoint-baseline', {'effective_write_set': ['y/b.py']})
lease('effective-omits-declared-conflict', {'effective_write_set': ['y/b.py']}, {'write_set': ['x/'], 'effective_write_set': ['x/']})
lease('empty-declared', {'write_set': [], 'effective_write_set': ['x/a.py']})
lease('own-dot', {'write_set': ['./x/a.py']})
lease('own-parent', {'effective_write_set': ['x/../y/b.py']})
lease('own-glob', {'write_set': ['x/*.py']})
lease('own-glob-conflict', {'write_set': ['x/*.py']}, {'write_set': ['x/a.py']})
lease('wrong-provider-type', {'provider': []})

d = out / 'receipt'; d.mkdir()
rc, sd, e, before = t._r812(t.Ctx(t.CANONICAL, d), 'review')
assert rc == 0, e
p = d / 'bn.yaml'; bn = yaml.safe_load(p.read_bytes()); w = d / 'kho/w'
assert v._thieu(bn) == [] and v._neo_git(w, 'bn.yaml', bn) == ([], [])
report('positive-H', rc, sd, e, before, thieu=[], neo=[[], []])
def review(name, b=None, st=None):
    raw = before if st is None else json.dumps(st).encode()
    (sd / 'wp55.json').write_bytes(raw)
    p.write_text(yaml.safe_dump(bn if b is None else b))
    rc, _, e = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'codex', '--verdict', 'approve',
        '--reviewed-sha', bn['reviewed_sha'], '--codex-call', 'g1', '--bien-nhan', p, '--root', w], sd)
    report(name, rc, sd, e, raw)
for key in ('model_family', 'ho_model', 'canonical_model', 'model', 'executor_model_family', 'executor_ho_model',
            'executor_canonical_model', 'executor_model', 'bang_chung_model', 'executor_bang_chung_model', 'model_executor_identity'):
    for val in ([], {}, False):
        b = copy.deepcopy(bn); b[key] = val
        review(key + '-' + type(val).__name__, b)
for vai in ('reviewer', 'executor'):
    for field in ('bang_chung_model', 'model_evidence_ref', 'telemetry_path'):
        b = copy.deepcopy(bn)
        b.setdefault('model_' + vai + '_identity', {})[field] = []
        review(vai + '-' + field + '-list', b)
for key, val in [('schema_version', 2.0), ('bang_lop', [{'slug':'same','hang':'P3'}, {'slug':'same','hang':'P3'}])]:
    b = copy.deepcopy(bn); b[key] = val; review(key + '-domain', b)
for vai in ('executor', 'reviewer'):
    for field in ('provider', 'model_family', 'execution_surface', 'transport'):
        st = json.loads(before); st['ngu_canh_lease'][vai][field] = []
        review('context-' + vai + '-' + field, st=st)
print(json.dumps({'scratch': str(out)}), flush=True)
