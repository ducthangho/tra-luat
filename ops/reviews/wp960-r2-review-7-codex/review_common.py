import importlib.util
import json
import os
import subprocess
from pathlib import Path

WORK = Path(__file__).resolve().parent
SOURCE = WORK / 'cay-kho'
SCRATCH = Path('/tmp/wp960-r7-review')
HEAD = SCRATCH / 'head'
SHA = '057abc816169688e894f64bbe637ea63d6bd9791'
BASE = '44884446f71c89e25f9a72ac58e4f597db63c1ba'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'


def emit(**v):
    print(json.dumps(v, ensure_ascii=False, default=str), flush=True)


def run(args, cwd=SOURCE, **kw):
    p = subprocess.run([str(x) for x in args], cwd=cwd, text=True,
                       capture_output=True, **kw)
    emit(command=[str(x) for x in args], cwd=cwd, rc=p.returncode,
         stdout=p.stdout, stderr=p.stderr)
    return p


def load_tests(root=HEAD):
    p = root / 'ops/bien_nhan_v2_test.py'
    spec = importlib.util.spec_from_file_location('review_tests', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def case(t, prefix):
    found = [fn for fn in t.CA if fn.__name__.startswith(prefix + '_')]
    assert len(found) == 1, (prefix, found)
    return found[0]


def invoke(t, prefix):
    fn = case(t, prefix)
    state, message = t._chay_1(fn)
    emit(case=fn.__name__, state=state, message=message)
    return state, message
