#!/usr/bin/env python3
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
repo = Path('/tmp/rv812-r4-hint2')
sys.path.insert(0, str(repo / '.claude/dev'))
s = importlib.util.spec_from_file_location('hint_r4_tests', repo / '.claude/dev/packet_loop_test.py')
t = importlib.util.module_from_spec(s); sys.modules[s.name] = t; s.loader.exec_module(t)
out = Path(tempfile.mkdtemp(prefix='review812-r4-hint-check-'))
names = {n for n,_ in t.CASES if n.startswith('r812_')}
r = t.chay_suite(t.CANONICAL, out/'baseline', names)
print(json.dumps({'baseline':len(r), 'errors':{n:v for n,v in r.items() if v is not None}},ensure_ascii=False),flush=True)
source = t.CANONICAL.read_text()
for name, (old,new,targets) in t.MUTANTS.items():
    if not name.startswith('r812_'):
        continue
    d=out/name;d.mkdir();mut=source
    for a,b in t._cap_thay_the(old,new):
        assert a in mut,(name,a)
        mut=mut.replace(a,b,1)
    p=d/'packet_loop.py';p.write_text(mut)
    shutil.copyfile(t.HERE/'launcher.py',d/'launcher.py')
    r=t.chay_suite(p,d/'cases',set(targets))
    print(json.dumps({'mutant':name,'targets':r},ensure_ascii=False),flush=True)
print(json.dumps({'scratch':str(out)}),flush=True)
