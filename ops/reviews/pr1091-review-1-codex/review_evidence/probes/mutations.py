from pathlib import Path
import concurrent.futures
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'cay-kho'
PRODUCT = 'ops/vm/cap-nhat-cong-cu.ps1'
TEST = 'ops/vm/cap-nhat-cong-cu_test.ps1'
PATHS = [PRODUCT, TEST, 'ops/vm/README.md', 'ops/cong_cu.yaml', 'requirements.txt']
original = (SOURCE / PRODUCT).read_text()
test = (SOURCE / TEST).read_text()
grant = next(line for line in original.splitlines() if 'Invoke-Icacls' in line and "'/grant:r'" in line and '$Script:ThuMucCaiDat' in line)
reset = next(line for line in original.splitlines() if 'Invoke-Icacls' in line and "'/reset'" in line)
block = "    if (@(Get-ChildItem -LiteralPath $Script:ThuMucCaiDat -Force).Count) {\n" + reset + '\n    }\n'
owner = "    Invoke-Icacls @($Script:ThuMucCaiDat, '/setowner', '*S-1-5-32-544', '/T', '/C', '/L', '/Q')"
assert original.count(block) == 1 and original.count(owner) == 2

def one(text, before, after):
    assert text.count(before) == 1, (before, text.count(before))
    return text.replace(before, after)

mutants = {
    'control': (original, test),
    'old_T_no_reset': (one(one(original, grant, grant.replace("'/C'", "'/T', '/C'")), block, ''), test),
    'no_reset': (one(original, block, ''), test),
    'reset_no_T': (one(original, reset, reset.replace("'/T', ", '')), test),
    'reset_no_L': (one(original, reset, reset.replace("'/L', ", '')), test),
    'reset_before_grant': (one(one(original, block, ''), grant, block.rstrip() + '\n' + grant), test),
    'reset_after_copy': (one(one(original, block, ''), '    # Tệp vừa chép có thể mang chủ', block + '    # Tệp vừa chép có thể mang chủ'), test),
    'reset_after_copy_cached_condition': (one(one(original, block, '    $coConCanReset = @(Get-ChildItem -LiteralPath $Script:ThuMucCaiDat -Force).Count\n'), '    # Tệp vừa chép có thể mang chủ', block.replace('if (@(Get-ChildItem -LiteralPath $Script:ThuMucCaiDat -Force).Count)', 'if ($coConCanReset)') + '    # Tệp vừa chép có thể mang chủ'), test),
    'grant_with_T_and_reset': (one(original, grant, grant.replace("'/C'", "'/T', '/C'")), test),
    'reset_root_instead_of_children': (one(original, reset, reset.replace("(Join-Path $Script:ThuMucCaiDat '*')", '$Script:ThuMucCaiDat')), test),
    'no_final_setowner': (original[:original.rindex(owner)] + original[original.rindex(owner):].replace(owner, '    # MUTANT no final setowner', 1), test),
    'users_modify': (one(original, grant, grant.replace('545:(OI)(CI)RX', '545:(OI)(CI)M')), test),
    'model_reset_noop': (original, one(test, "if ($DoiSo -contains '/reset') { $node.Access = @($Script:AclGia[$goc].Access); continue }", "if ($DoiSo -contains '/reset') { continue }")),
    'model_copy_no_denial': (original, one(test, "if ($cu -and -not @($cu.Access | Where-Object { $_.IdentityReference -eq 'BUILTIN\\Administrators' -and $_.FileSystemRights -eq 'FullControl' }).Count)", 'if ($false)')),
}

def run(item):
    name, (product, tests) = item
    directory = ROOT / 'copies' / name
    for path in PATHS:
        dest = directory / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / path, dest)
    (directory / PRODUCT).write_text(product)
    (directory / TEST).write_text(tests)
    delta = ''.join(difflib.unified_diff(original.splitlines(True), product.splitlines(True), fromfile=PRODUCT, tofile=PRODUCT))
    delta += ''.join(difflib.unified_diff(test.splitlines(True), tests.splitlines(True), fromfile=TEST, tofile=TEST))
    (ROOT / 'evidence' / f'{name}.patch').write_text(delta)
    env = dict(os.environ, TL_TEST_PYTHON='python3', PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run([str(ROOT/'pwsh/pwsh'), '-NoProfile', '-File', str(directory/TEST)], env=env, capture_output=True, text=True, timeout=180)
    output = result.stdout + result.stderr
    (ROOT / 'evidence' / f'{name}.log').write_text(output)
    summary = re.findall(r'cap-nhat-cong-cu tests: (\d+)/(\d+) ca QUA', output)
    record = dict(name=name, rc=result.returncode, summary=summary, failed=re.findall(r'  DO  (.+)', output), parser_error='ParserError' in output, product_sha256=hashlib.sha256(product.encode()).hexdigest(), test_sha256=hashlib.sha256(tests.encode()).hexdigest())
    print(json.dumps(record, ensure_ascii=False), flush=True)
    return record

if __name__ == '__main__':
    import sys
    selected = {key: value for key, value in mutants.items() if not sys.argv[1:] or key in sys.argv[1:]}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, selected.items()))
    filename = 'mutations-extra.json' if sys.argv[1:] else 'mutations.json'
    (ROOT / 'evidence' / filename).write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
