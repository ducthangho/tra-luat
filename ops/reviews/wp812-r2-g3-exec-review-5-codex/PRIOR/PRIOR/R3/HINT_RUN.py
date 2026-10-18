#!/usr/bin/env python3
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r3-suite')
sys.path.insert(0, str(repo / '.claude/dev'))
s = importlib.util.spec_from_file_location('hint_r3_tests', repo / '.claude/dev/packet_loop_test.py')
t = importlib.util.module_from_spec(s)
sys.modules[s.name] = t
s.loader.exec_module(t)
exec(compile(Path('HINT_TESTS.py').read_text(), 'HINT_TESTS.py', 'exec'), t.__dict__)
t.CASES += [(n[5:], f) for n, f in list(t.__dict__.items()) if n.startswith('case_r812_r3_')]
names = {n for n, _ in t.CASES if n.startswith('r812_r3_')}
out = Path(tempfile.mkdtemp(prefix='review812-r3-hint-'))
r = t.chay_suite(t.CANONICAL, out / 'base', names)
print(json.dumps({'kind': 'head', 'total': len(r), 'errors': {n: v for n, v in r.items() if v is not None}}, ensure_ascii=False), flush=True)
source = t.CANONICAL.read_text()
for name, old, new, target in (
    ('sha', '("reviewed_sha", d.get("reviewed_sha") == a.reviewed_sha)', '("reviewed_sha", True)', 'r812_r3_receipt_sha'),
    ('lease_id', '("lease_id", d.get("lease_id") == nc["lease_id"])', '("lease_id", True)', 'r812_r3_receipt_lease_id'),
    ('executor_transport', '(("surface", "execution_surface"), ("transport", "transport"))', '(("surface", "execution_surface"),)', 'r812_r3_executor_transport'),
    ('dependency', '            if rc != 0 or not b:', '            if False:', 'r812_r3_dependency_absent'),
):
    assert source.count(old) == 1, name
    d = out / name
    d.mkdir()
    p = d / 'packet_loop.py'
    p.write_text(source.replace(old, new, 1))
    shutil.copyfile(t.HERE / 'launcher.py', d / 'launcher.py')
    r = t.chay_suite(p, d / 'cases', {target})
    print(json.dumps({'mutant': name, 'result': r}, ensure_ascii=False), flush=True)
