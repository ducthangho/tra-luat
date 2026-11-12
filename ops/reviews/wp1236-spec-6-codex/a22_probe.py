"""Quan sát bốn cách nạp tệp hiện có; không sửa module hay tạo payload."""
import importlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'repo'
TARGET = ROOT / 'ops/kiem_ho_so_land.py'
FORBIDDEN = {TARGET.resolve(), (ROOT/'ops/land_evidence_nguon.py').resolve()}

def child(mode):
    loader_seen, spec_seen, open_seen = [], [], []
    old_exec = importlib.machinery.SourceFileLoader.exec_module
    old_spec = importlib.util.spec_from_file_location
    def track_exec(loader, module):
        loader_seen.append(str(Path(loader.path).resolve()))
        return old_exec(loader, module)
    def track_spec(name, location, *a, **kw):
        if location is not None:
            spec_seen.append(str(Path(location).resolve()))
        return old_spec(name, location, *a, **kw)
    def track_open(event, args):
        if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
            p=Path(os.fsdecode(args[0])).resolve()
            if p in FORBIDDEN:
                open_seen.append(str(p))
    importlib.machinery.SourceFileLoader.exec_module = track_exec
    importlib.util.spec_from_file_location = track_spec
    sys.addaudithook(track_open)
    sys.path.insert(0,str(ROOT))
    if mode=='package':
        importlib.import_module('ops.kiem_ho_so_land')
    elif mode=='spec':
        spec=importlib.util.spec_from_file_location('diagnostic_load',TARGET)
        spec.loader.exec_module(importlib.util.module_from_spec(spec))
    elif mode=='runpy':
        runpy.run_path(str(TARGET))
    elif mode=='read_compile':
        with TARGET.open() as f:
            code=compile(f.read(),str(TARGET),'exec')
        exec(code,{'__name__':'diagnostic_load','__file__':str(TARGET)})
    elif mode=='allowed':
        importlib.import_module('ops.ci_provenance')
    modules_seen=[str(Path(p).resolve()) for m in list(sys.modules.values())
                  if isinstance(p:=getattr(m,'__file__',None),str)]
    old_detected=any(Path(p) in FORBIDDEN for p in loader_seen+spec_seen+modules_seen)
    print(json.dumps({'mode':mode,'r5_detected':old_detected,'audit_detected':bool(open_seen),
                      'r6_detected':old_detected or bool(open_seen),'audit_events':len(open_seen)}))

if __name__=='__main__':
    if len(sys.argv)>1:
        child(sys.argv[1])
    else:
        results=[]
        for mode in ['allowed','package','spec','runpy','read_compile']:
            proc=subprocess.run([sys.executable,'-B',__file__,mode],capture_output=True,text=True)
            row={'rc':proc.returncode,**json.loads(proc.stdout)}
            results.append(row)
        (BASE/'work/a22.json').write_text(json.dumps(results,indent=2))
        print(json.dumps(results,indent=2))
