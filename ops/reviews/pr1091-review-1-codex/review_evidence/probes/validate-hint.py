from pathlib import Path
import concurrent.futures
import json
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'ops/vm/cap-nhat-cong-cu.ps1'
TEST = 'ops/vm/cap-nhat-cong-cu_test.ps1'
PATHS = [PRODUCT, TEST, 'ops/vm/README.md', 'ops/cong_cu.yaml', 'requirements.txt']
hint = (ROOT/'copies/hint'/TEST).read_text()

def run(name):
    folder = ROOT/'copies'/f'hint-{name}'
    for path in PATHS:
        dest = folder/path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/'cay-kho'/path, dest)
    if name == 'control':
        proc = subprocess.run(['patch', '-p0', '--batch', '--input', str(ROOT/'HINT.patch')], cwd=folder, capture_output=True, text=True)
        (ROOT/'evidence/hint-patch-apply.log').write_text(proc.stdout+proc.stderr)
        assert proc.returncode == 0
        assert (folder/TEST).read_text() == hint
    else:
        tests = hint
        if name == 'model_reset_noop':
            anchor = "if ($DoiSo -contains '/reset') { $node.Access = @($Script:AclGia[(Split-Path -Parent $key)].Access); continue }"
            assert tests.count(anchor) == 1
            tests = tests.replace(anchor, "if ($DoiSo -contains '/reset') { continue }")
        else:
            shutil.copyfile(ROOT/'copies'/name/PRODUCT, folder/PRODUCT)
        (folder/TEST).write_text(tests)
    env = dict(os.environ, TL_TEST_PYTHON='python3', PYTHONDONTWRITEBYTECODE='1')
    proc = subprocess.run([str(ROOT/'pwsh/pwsh'), '-NoProfile', '-File', str(folder/TEST)], env=env, capture_output=True, text=True, timeout=180)
    output = proc.stdout+proc.stderr
    (ROOT/'evidence'/f'hint-{name}.log').write_text(output)
    row = dict(name=name, rc=proc.returncode, summary=re.findall(r'cap-nhat-cong-cu tests: (\d+)/(\d+) ca QUA', output), failed=re.findall(r'  DO  (.+)', output), parser_error='ParserError' in output)
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, ['control', 'reset_no_T', 'reset_after_copy_cached_condition', 'model_reset_noop']))
(ROOT/'evidence/hint-validation.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
