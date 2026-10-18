#!/usr/bin/env python3
"""Full executor identity baseline, followed by one-field changes."""
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
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m
t = load('identity_ab_tests', repo / '.claude/dev/packet_loop_test.py')
v = load('identity_ab_validator', repo / 'ops/bien_nhan_v2.py')
yaml = __import__('yaml')
d = Path(tempfile.mkdtemp(prefix='review812-identity-ab-'))
rc, sd, e, before = t._r812(t.Ctx(t.CANONICAL, d), 'review')
assert rc == 0, e
p = d / 'bn.yaml'
bn = yaml.safe_load(p.read_bytes())
bn['model_executor_identity'] = dict(model_family='claude', model_evidence='do_may', model_evidence_ref='r', surface='claude_code', transport='machine/local')
for name, field, value in [('positive-full-tuple', None, None), ('executor-provider-one-field', 'executor_provider', 'google_antigravity'), ('executor-surface-one-field', 'surface', 'codex_cli'), ('executor-transport-one-field', 'transport', 'human')]:
    b = copy.deepcopy(bn)
    if field:
        (b if field == 'executor_provider' else b['model_executor_identity'])[field] = value
    assert v._thieu(b) == []
    assert v._neo_git(d / 'kho/w', p.name, b) == ([], [])
    p.write_text(yaml.safe_dump(b))
    (sd / 'wp55.json').write_bytes(before)
    rc, _, e = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'codex', '--verdict', 'approve', '--reviewed-sha', bn['reviewed_sha'], '--codex-call', 'g1', '--bien-nhan', p, '--root', d / 'kho/w'], sd)
    print(json.dumps(dict(probe=name, changed_field=field, rc=rc, state=json.loads((sd / 'wp55.json').read_bytes())['state'], error=e.decode()), ensure_ascii=False), flush=True)
