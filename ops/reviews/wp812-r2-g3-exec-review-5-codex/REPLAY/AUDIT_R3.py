#!/usr/bin/env python3
"""Independent weakening mutants; every r812 case is run on each scratch mutant."""
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r5-suite')
sys.path.insert(0, str(repo / '.claude/dev'))
s = importlib.util.spec_from_file_location('audit_r3_tests', repo / '.claude/dev/packet_loop_test.py')
t = importlib.util.module_from_spec(s)
sys.modules[s.name] = t
s.loader.exec_module(t)
out = Path(tempfile.mkdtemp(prefix='review812-r3-audit-'))
source = t.CANONICAL.read_text()
names = {n for n, _ in t.CASES if n.startswith('r812_')}
targeted = {n for _, _, targets in t.MUTANTS.values() for n in targets}
print(json.dumps({'cases': len(names), 'declared_mutants': len([n for n in t.MUTANTS if n.startswith('r812_')]),
                  'untargeted': sorted(names - targeted)}), flush=True)
mutants = {
    'audit_receipt_sha_unbound': ('("reviewed_sha", d.get("reviewed_sha") == a.reviewed_sha)', '("reviewed_sha", True)'),
    'audit_receipt_lease_id_unbound': ('("lease_id", d.get("lease_id") == nc["lease_id"])', '("lease_id", True)'),
    'audit_no_executor_transport': ('(("surface", "execution_surface"), ("transport", "transport"))', '(("surface", "execution_surface"),)'),
    'audit_no_class_uniqueness': ('and len({x["slug"] for x in lop}) == len(lop)', ''),
    'audit_no_cross_family': ('("khac-ho", nc["assurance_target"] != "cross_approved" or ho_rev != ho_exec)', '("khac-ho", True)'),
    'audit_init_awaiting': ('"state": "awaiting_lease",', '"state": "leased",'),
}
for name, (old, new) in mutants.items():
    assert source.count(old) == 1, (name, source.count(old))
    d = out / name
    d.mkdir()
    p = d / 'packet_loop.py'
    p.write_text(source.replace(old, new, 1))
    shutil.copyfile(t.HERE / 'launcher.py', d / 'launcher.py')
    r = t.chay_suite(p, d / 'cases', names)
    errors = {n: v for n, v in r.items() if v is not None}
    print(json.dumps({'mutant': name, 'total': len(r), 'passed': len(r) - len(errors), 'errors': errors}, ensure_ascii=False), flush=True)
print(json.dumps({'scratch': str(out)}), flush=True)
