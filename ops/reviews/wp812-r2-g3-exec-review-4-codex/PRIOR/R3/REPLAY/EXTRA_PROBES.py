#!/usr/bin/env python3
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r3-suite')
sys.path.insert(0, str(repo / '.claude/dev'))
s = importlib.util.spec_from_file_location('extra812_tests', repo / '.claude/dev/packet_loop_test.py')
t = importlib.util.module_from_spec(s)
sys.modules[s.name] = t
s.loader.exec_module(t)
yaml = __import__('yaml')
out = Path(tempfile.mkdtemp(prefix='review812-extra-'))
def mutate(w, variant):
    t._g(w, 'checkout', '-qb', 'ops/wp55-spec', 'refs/remotes/origin/ops/wp55-spec')
    p = w / 'ops/leases/l.yaml'
    l = yaml.safe_load(p.read_bytes())
    if variant == 'prefix-conflict':
        (w / 'ops/leases/other.yaml').write_text(yaml.safe_dump({**l, 'lease_id': 'competing-directory-lease', 'write_set': ['x/']}))
    elif variant == 'planned-path':
        l['write_set'] = ['planned:x/a.py']
        p.write_text(yaml.safe_dump(l))
    elif variant == 'effective-conflict':
        (w / 'ops/leases/other.yaml').write_text(yaml.safe_dump({**l, 'lease_id': 'competing-effective-lease', 'write_set': ['y/b.py'], 'effective_write_set': ['y/b.py', 'x/a.py']}))
    t._g(w, 'add', '-A')
    t._g(w, 'commit', '-qm', 'single authority-scope change')
    t._g(w, 'push', '-q', 'origin', 'ops/wp55-spec')
    t._g(w, 'checkout', '-q', 'master')
    t._g(w, 'branch', '-q', '-D', 'ops/wp55-spec')
for variant in ('prefix-conflict', 'planned-path', 'effective-conflict'):
    d = out / variant
    d.mkdir()
    c = t.Ctx(t.CANONICAL, d)
    rc, sd, e, before = t._r812(c, 'lease', truoc_lease=lambda w: mutate(w, variant))
    st = json.loads((sd / 'wp55.json').read_bytes())
    print(json.dumps(dict(probe=variant, rc=rc, state=st['state'], unchanged=(sd / 'wp55.json').read_bytes() == before, error=e.decode()), ensure_ascii=False), flush=True)
print(json.dumps({'scratch': str(out)}), flush=True)
