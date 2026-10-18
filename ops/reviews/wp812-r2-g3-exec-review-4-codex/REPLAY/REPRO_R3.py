#!/usr/bin/env python3
"""Offline probes on a disposable copy; never write KHO. Usage: python3 REPRO_R3.py"""
import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r4-suite')
sys.path.insert(0, str(repo / '.claude/dev'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


t = load('r3_tests', repo / '.claude/dev/packet_loop_test.py')
v = load('r3_validator', repo / 'ops/bien_nhan_v2.py')
import yaml

out = Path(tempfile.mkdtemp(prefix='review812-r3-own-'))


def report(name, rc, sd, err, before, **extra):
    raw = (sd / 'wp55.json').read_bytes()
    print(json.dumps(dict(probe=name, rc=rc, state=json.loads(raw)['state'], unchanged=raw == before,
                          traceback=b'Traceback' in err, error=err.decode('utf-8', 'replace'), **extra), ensure_ascii=False), flush=True)


def lease_probe(name, changes=None, other=None, prepare=None):
    d = out / name
    d.mkdir()
    def mutate(w):
        if prepare:
            prepare(w)
        t._r812_doi_lease(w, changes or {}, (lambda l: {'other.yaml': {**l, 'lease_id': 'other-lease', **other}}) if other else None)
    rc, sd, err, before = t._r812(t.Ctx(t.CANONICAL, d), 'lease', truoc_lease=mutate)
    report(name, rc, sd, err, before)


lease_probe('holder-baseline')
lease_probe('holder-casefold-conflict', other={'write_set': ['X/']})
lease_probe('holder-separator-conflict', other={'write_set': ['x\\a.py']})
lease_probe('holder-dot-component-conflict', other={'write_set': ['./x/a.py']})
lease_probe('holder-unicode-conflict', changes={'write_set': ['café/a.py']}, other={'write_set': ['cafe\u0301/']})
lease_probe('candidate-effective-expansion', changes={'effective_write_set': ['x/a.py', 'y/b.py']})
lease_probe('candidate-effective-omits-base', changes={'effective_write_set': ['x/z.py']})
lease_probe('lease-empty-branch', changes={'branch': ''})

d = out / 'receipt'
d.mkdir()
rc, sd, err, before = t._r812(t.Ctx(t.CANONICAL, d), 'review')
assert rc == 0, err
p = d / 'bn.yaml'
bn = yaml.safe_load(p.read_bytes())
assert v.PROVIDER_NGUON_HONG is None
assert v._thieu(bn) == []
assert v._neo_git(d / 'kho/w', 'bn.yaml', bn) == ([], [])
report('receipt-positive-real-H', rc, sd, err, before, thieu=[], neo=[[], []])


def review(name, receipt=None, state=None):
    raw = before if state is None else json.dumps(state).encode()
    (sd / 'wp55.json').write_bytes(raw)
    p.write_text(yaml.safe_dump(bn if receipt is None else receipt))
    rc, _, err = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'codex', '--verdict', 'approve',
        '--reviewed-sha', bn['reviewed_sha'], '--codex-call', 'g1', '--bien-nhan', p, '--root', d / 'kho/w'], sd)
    report(name, rc, sd, err, raw)


for key in ('provider', 'surface', 'transport', 'model_family'):
    for value in ([], {}):
        b = copy.deepcopy(bn)
        b['model_reviewer_identity'][key] = value
        review('reviewer-' + key + '-' + type(value).__name__, b)
for value in ([], {}):
    b = copy.deepcopy(bn)
    b['executor_provider'] = value
    review('executor-provider-' + type(value).__name__, b)
for key in ('anchor', 'verdict_path', 'bang_lop'):
    b = copy.deepcopy(bn)
    b[key] = ['bad']
    review('receipt-' + key + '-list', b)
for key, value in (('branch', ''), ('lease_ref', []), ('lease_path', {}), ('lease_oid', 'not-an-oid'), ('repo', 'not-a-repo'),
                   ('spec_hash', 'not-a-hash'), ('required_checks', [False])):
    st = json.loads(before)
    st['ngu_canh_lease'][key] = value
    review('state-context-' + key, state=st)
for key, value in (('execution_surface', []), ('transport', {})):
    st = json.loads(before)
    st['ngu_canh_lease']['reviewer'][key] = value
    review('state-reviewer-' + key, state=st)
print(json.dumps({'scratch': str(out)}), flush=True)
