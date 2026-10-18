#!/usr/bin/env python3
"""Run every declared r812 mutant and independent weakening mutants outside KHO."""
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r2-suite')
sys.path.insert(0, str(repo / '.claude/dev'))
sp = importlib.util.spec_from_file_location('audit812_tests', repo / '.claude/dev/packet_loop_test.py')
t = importlib.util.module_from_spec(sp)
sys.modules[sp.name] = t
sp.loader.exec_module(t)
out = Path(tempfile.mkdtemp(prefix='review812-audit-mutants-'))
source = t.CANONICAL.read_text()
names = {n for n, _ in t.CASES if n.startswith('r812_')}
base = t.chay_suite(t.CANONICAL, out / 'base', names)
assert all(v is None for v in base.values()), base
print(json.dumps({'kind': 'baseline', 'passed': len(base), 'total': len(names)}, ensure_ascii=False), flush=True)
mutants = {n: (*v, False) for n, v in t.MUTANTS.items() if n.startswith('r812_')}
mutants.update({
    'audit_no_receipt_schema': ('list(bnv._thieu(d) if d else [])', '[]', sorted(names), True),
    'audit_no_land_adr_existence': ('and _git_do(root, "cat-file", "-e", f"{oid}:{ADR0054_TEP}")[0] == 0', 'and True', sorted(names), True),
    'audit_no_land_first_addition': ('and _git_do(root, "cat-file", "-e", f"{oid}^1:{ADR0054_TEP}")[0] != 0', 'and True', sorted(names), True),
    'audit_no_land_first_parent': ('and chuoi[0] == 0 and oid.encode() in chuoi[1].split()', 'and True', sorted(names), True),
    'audit_no_adr0054_round_close': ('if cua == "record-review" and a is None and st.get("luat_adr0054") is not True:', 'if cua == "record-review" and a is None:', sorted(names), True),
    'audit_bad_review_stops_before_H': ('    bn = _du_dieu_kien_approve(st, a)', '    if st["review_rounds_used"] >= st["review_rounds_limit"]:\n        _vao_rescue(state_dir, st, "vong_review", "audit before inputs")\n    bn = _du_dieu_kien_approve(st, a)', sorted(names), True),
})
for name, (old, new, targets, audit) in mutants.items():
    assert source.count(old) >= 1, name
    d = out / name
    d.mkdir()
    p = d / 'packet_loop.py'
    p.write_text(source.replace(old, new, 1))
    shutil.copyfile(t.HERE / 'launcher.py', d / 'launcher.py')
    result = t.chay_suite(p, d / 'cases', set(targets))
    errors = {n: v for n, v in result.items() if v is not None}
    print(json.dumps({'mutant': name, 'audit': audit, 'total': len(result), 'survived': [n for n,v in result.items() if v is None], 'errors': errors}, ensure_ascii=False), flush=True)
print(json.dumps({'scratch': str(out)}), flush=True)
