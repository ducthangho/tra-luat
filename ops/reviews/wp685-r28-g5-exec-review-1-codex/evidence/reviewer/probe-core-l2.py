import ast
import json
import os
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
if sys.argv[2]=='without-git-pin':
    for key in ('GIT_CONFIG_COUNT','GIT_CONFIG_KEY_0','GIT_CONFIG_VALUE_0'):
        os.environ.pop(key,None)
sys.path.insert(0,str(root/'scripts'))
import tl
names=['_c226_nguong_l2_troi_theo_abbrev_va_ci_ghim','_c268_l2_trichotomy_theo_trang_thai_object']
parsed=ast.parse((root/'scripts/tl_selftest.py').read_text())
functions={n.name:n for n in ast.walk(parsed) if isinstance(n,ast.FunctionDef) and n.name in names}
assert set(functions)==set(names)
scope={'_TL_MODULE':tl,'_ROOT209':root,'Path':Path}
exec(compile(ast.fix_missing_locations(ast.Module(body=[functions[n] for n in names],type_ignores=[])),str(root/'scripts/tl_selftest.py'),'exec'),scope)
print(json.dumps({'mode':sys.argv[2],'results':{n:bool(scope[n]()) for n in names}},sort_keys=True))
