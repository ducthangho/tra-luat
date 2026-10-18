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

def nested(w):
    t._g(w, 'checkout', '-qb', 'ops/wp55-spec', 'refs/remotes/origin/ops/wp55-spec')
    p = w / 'ops/leases/l.yaml'
    l = yaml.safe_load(p.read_bytes())
    p.write_text(yaml.safe_dump(l) + 'extra: ' + '[' * 700 + '0' + ']' * 700 + '\n')
    t._g(w, 'add', '-A'); t._g(w, 'commit', '-qm', 'ordinary nested metadata'); t._g(w, 'push', '-q', 'origin', 'ops/wp55-spec')
    t._g(w, 'checkout', '-q', 'master'); t._g(w, 'branch', '-q', '-D', 'ops/wp55-spec')
d=out/'deep-lease';d.mkdir()
rc,sd,e,before=t._r812(t.Ctx(t.CANONICAL,d),'lease',truoc_lease=nested)
report('deep-lease-input',rc,sd,e,before)
