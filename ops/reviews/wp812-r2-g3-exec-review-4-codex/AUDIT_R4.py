#!/usr/bin/env python3
"""Record exact rejection reasons for declared r812 mutations and additional weakening mutations."""
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r4-suite')
sys.path.insert(0, str(repo / '.claude/dev'))
s = importlib.util.spec_from_file_location('audit_r4_tests', repo / '.claude/dev/packet_loop_test.py')
t = importlib.util.module_from_spec(s); sys.modules[s.name] = t; s.loader.exec_module(t)
out = Path(tempfile.mkdtemp(prefix='review812-r4-audit-'))
source = t.CANONICAL.read_text()
for name, (old, new, targets) in t.MUTANTS.items():
    if not name.startswith('r812_'):
        continue
    d = out / name; d.mkdir()
    mutated = source
    for a, b in t._cap_thay_the(old, new):
        assert a in mutated, (name, a)
        mutated = mutated.replace(a, b, 1)
    p = d / 'packet_loop.py'; p.write_text(mutated)
    shutil.copyfile(t.HERE / 'launcher.py', d / 'launcher.py')
    results = t.chay_suite(p, d / 'cases', set(targets))
    print(json.dumps({'mutant': name, 'targets': results}, ensure_ascii=False), flush=True)
custom = {
    'r4_dependency_absence_guard': ('            if rc != 0 or not b:', '            if False:', ['r812_canon_vang_phu_thuoc']),
    'r4_missing_verdict_blob': ('+ neo[0] + neo[1] +', '+', ['r812_verdict_path_khong_ton_tai']),
    'r4_reject_valid_negative': ('("slug-ngoai-bang", lop_ok and set(a.finding_id or []) <= {x["slug"] for x in lop})',
        '("slug-ngoai-bang", lop_ok and not a.finding_id)', ['r812_verdict_am_dung_bang_lop']),
}
for name, (a, b, targets) in custom.items():
    assert source.count(a) == 1, (name, source.count(a))
    d = out / name; d.mkdir(); p = d / 'packet_loop.py'; p.write_text(source.replace(a,b,1))
    shutil.copyfile(t.HERE / 'launcher.py', d / 'launcher.py')
    print(json.dumps({'mutant': name, 'targets': t.chay_suite(p, d / 'cases', set(targets))}, ensure_ascii=False), flush=True)
print(json.dumps({'scratch': str(out)}), flush=True)
