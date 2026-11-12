"""Measure audit paths while loading unchanged local checker modules.

No replacement or attack content is inserted into a module. This probes Python
loading behavior and the specified path predicate, not the unimplemented A22.
"""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import py_compile
import runpy
import shutil
import subprocess
import sys

work = Path(__file__).resolve().parent
repo = work.parent / 'repo'
tree = work / 'a22-tree'

if len(sys.argv) == 1:
    (tree / 'ops').mkdir(parents=True, exist_ok=True)
    for name in ('ci_provenance', 'kiem_ho_so_land', 'land_evidence_nguon'):
        target = tree / 'ops' / (name + '.py')
        shutil.copyfile(repo / 'ops' / (name + '.py'), target)
        py_compile.compile(str(target), doraise=True)
    rows = []
    for method in ('source_spec', 'runpy_source', 'runpy_pyc', 'import_pyc', 'allowed_pyc'):
        env = dict(os.environ, TMPDIR=str(work))
        env.pop('PYTHONDONTWRITEBYTECODE', None)
        p = subprocess.run([sys.executable, str(Path(__file__).resolve()), method], env=env, capture_output=True, text=True, timeout=30)
        rows.append({'method': method, 'rc': p.returncode, 'result': json.loads(p.stdout) if p.returncode == 0 else p.stderr})
    (work / 'a22.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(json.dumps(rows, ensure_ascii=False, indent=2))
else:
    opened, loaded = [], []
    def record(event, args):
        if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
            p = Path(os.fsdecode(args[0])).resolve()
            if p.is_relative_to(tree) and p.suffix in ('.py', '.pyc'):
                opened.append(p)
    sys.addaudithook(record)
    original_exec = importlib.machinery.SourceFileLoader.exec_module
    original_spec = importlib.util.spec_from_file_location
    def exec_module(self, module):
        loaded.append(Path(self.path).resolve())
        return original_exec(self, module)
    def spec_file(name, location, *args, **kwargs):
        loaded.append(Path(location).resolve())
        return original_spec(name, location, *args, **kwargs)
    importlib.machinery.SourceFileLoader.exec_module = exec_module
    importlib.util.spec_from_file_location = spec_file
    src = tree / 'ops/kiem_ho_so_land.py'
    method = sys.argv[1]
    if method == 'source_spec':
        spec = importlib.util.spec_from_file_location('probe_checker', src)
        spec.loader.exec_module(importlib.util.module_from_spec(spec))
    elif method == 'runpy_source':
        runpy.run_path(str(src))
    elif method == 'runpy_pyc':
        runpy.run_path(importlib.util.cache_from_source(str(src)))
    else:
        sys.path.insert(0, str(tree / 'ops'))
        __import__('ci_provenance' if method == 'allowed_pyc' else 'kiem_ho_so_land')
    forbidden = {tree / 'ops' / (n + '.py') for n in ('kiem_ho_so_land', 'land_evidence_nguon')}
    module_files = [Path(v.__file__).resolve() for v in list(sys.modules.values()) if getattr(v, '__file__', None)]
    layer12 = any(p in forbidden for p in loaded + module_files)
    old_open = any(p in forbidden for p in opened)
    def allowed(p):
        rel = p.relative_to(tree).as_posix()
        return rel in ('ops/gate_output_doi_chieu.py','ops/ci_provenance.py') or any(p.match('ops/__pycache__/' + n + '.*.pyc') for n in ('gate_output_doi_chieu','ci_provenance'))
    violations = sorted({str(p.relative_to(tree)) for p in opened if not allowed(p)})
    print(json.dumps({'opened':sorted({str(p.relative_to(tree)) for p in opened}), 'layers12_caught':layer12, 'r6_audit_caught':old_open, 'r6_all_caught':layer12 or old_open, 'r7_audit_caught':bool(violations), 'r7_all_caught':layer12 or bool(violations), 'violations':violations}))
