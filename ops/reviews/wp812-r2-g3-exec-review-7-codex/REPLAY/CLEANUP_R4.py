#!/usr/bin/env python3
"""Read only source review; every state/fixture is under /tmp."""
import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r7-suite')
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

for name,den,kw in [('success','review',{}),('lease-reject','lease',{'bien':'h_hong'}),('review-reject','review',{'bn':{'model_reviewer_identity':{'provider': [], 'surface':'codex_cli','transport':'machine','session_run_id':'s'}}})]:
 d=out/name;d.mkdir();tmp=d/'tmpd';tmp.mkdir()
 rc,sd,e,before=t._r812(t.Ctx(t.CANONICAL,d),den,env={'TMPDIR':str(tmp)},**kw)
 w=next(d.glob('kho*/w'))
 report(name,rc,sd,e,before,remaining_canon=[x.name for x in tmp.glob('pl812-canon-*')],worktrees=t._g(w,'worktree','list','--porcelain').count('worktree '))
