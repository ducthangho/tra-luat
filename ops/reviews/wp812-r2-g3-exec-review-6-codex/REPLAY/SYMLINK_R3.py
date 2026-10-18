#!/usr/bin/env python3
"""Benign alias wholly inside a disposable fixture; no path leaves that fixture."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path('/tmp/wp812-r6-suite')
sys.path.insert(0, str(repo / '.claude/dev'))
s = importlib.util.spec_from_file_location('symlink_r3_tests', repo / '.claude/dev/packet_loop_test.py')
t = importlib.util.module_from_spec(s)
sys.modules[s.name] = t
s.loader.exec_module(t)
d = Path(tempfile.mkdtemp(prefix='review812-r3-alias-'))


def mutate(w, competing):
    (w / 'x').mkdir()
    (w / 'x/a.py').write_text('a = 1\n')
    (w / 'alias').symlink_to('x', target_is_directory=True)
    assert (w / 'alias/a.py').resolve() == (w / 'x/a.py').resolve()
    t._g(w, 'add', '-A')
    t._g(w, 'commit', '-qm', 'in-repository alias fixture')
    t._g(w, 'push', '-q', 'origin', 'master')
    t._r812_doi_lease(w, {}, (lambda l: {'other.yaml': {**l, 'lease_id': 'alias-holder', 'write_set': ['alias/a.py']}}) if competing else None)


for competing in (False, True):
    dd = d / str(competing)
    dd.mkdir()
    rc, sd, e, before = t._r812(t.Ctx(t.CANONICAL, dd), 'lease', truoc_lease=lambda w: mutate(w, competing))
    print(json.dumps({'probe': 'in-repository-symlink-conflict' if competing else 'in-repository-symlink-baseline', 'rc': rc,
        'state': json.loads((sd / 'wp55.json').read_bytes())['state'],
        'unchanged': before == (sd / 'wp55.json').read_bytes(), 'error': e.decode(), 'scratch': str(dd)}, ensure_ascii=False))
