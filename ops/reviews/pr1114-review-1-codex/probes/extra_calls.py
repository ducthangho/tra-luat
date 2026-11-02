import ast
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
from unittest import mock

root = Path(__file__).resolve().parents[1]
path = root / 'copies/head/ops/cloud_agent_creds_test.py'
spec = importlib.util.spec_from_file_location('review_extra', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
real_run = subprocess.run
def size(argv):
    line = subprocess.list2cmdline([str(a) for a in argv])
    return len(line.encode('utf-16-le')) // 2 + 1
def run(argv, **kw):
    result = real_run(argv, **kw)
    print('CO_MUSL', 'argv=' + repr(argv), 'units=' + str(size(argv)), 'rc=' + str(result.returncode))
    return result
helper = m.nap_mod()
with mock.patch.object(helper.subprocess, 'run', run):
    print('CO_MUSL_RESULT', helper._co_musl())

attempts = []
def no_spawn(argv, **kw):
    attempts.append((argv, size(argv)))
    raise OSError('review measurement: deliberate pre-spawn failure')
helper.GOC = m.HERE.parent
with mock.patch.object(helper.subprocess, 'Popen', no_spawn), contextlib.redirect_stdout(io.StringIO()):
    helper.nap({'TL_MASTER_KEY': 'synthetic-review-key'})
    helper._ban_khop(Path('/khong-co-agy'))
for argv, n in attempts:
    print('MOCKED_PRE_SPAWN', repr(argv), 'units=' + str(n))

targets = {
    'scripts/tl_gws.py': ['_public_curl_bytes', '_last_refresh_key'],
    'scripts/gws_cred_store.py': ['encrypt', 'decrypt'],
    'scripts/_fallback/gas.py': ['get', 'post'],
}
for file, names in targets.items():
    source = (root / 'cay-kho' / file).read_text()
    tree = ast.parse(source)
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name in names:
            calls = [ast.unparse(x.func) for x in ast.walk(n) if isinstance(x, ast.Call)]
            spawn = [x for x in calls if x.startswith(('subprocess.', '_sp.'))]
            print('HELPER_AST', file + ':' + str(n.lineno), n.name, 'subprocess_calls=' + repr(spawn))
            assert not spawn
print('EXTRA_CALLS=PASS')
