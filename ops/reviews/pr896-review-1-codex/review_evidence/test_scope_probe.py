import contextlib
import copy
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import yaml

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m
    spec.loader.exec_module(m)
    return m
repo=Path.cwd()
lp=load('review_lp_scope',repo/'ops/lease_publish_test.py')
ci=load('review_ci_scope',repo/'.claude/dev/ci_dang_ky_test.py')
wf=yaml.safe_load((repo/'.github/workflows/ci.yml').read_text())
variants={'baseline':copy.deepcopy(wf), 'remove_windows_shard1_exclusion':copy.deepcopy(wf), 'remove_gop_if':copy.deepcopy(wf)}
variants['remove_windows_shard1_exclusion']['jobs']['gate-cong-cu']['strategy']['matrix']['exclude'].remove({'os':'windows-latest','manh':1})
del variants['remove_gop_if']['jobs']['gate-cong-cu-gop']['if']
with tempfile.TemporaryDirectory(prefix='pr896-scope-') as td:
    root=Path(td)
    (root/'.github/workflows').mkdir(parents=True)
    (root/'ops').mkdir()
    lp.HERE=root/'ops'
    for name,data in variants.items():
        (root/'.github/workflows/ci.yml').write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False))
        result=[]
        for fn in (lp.t161_M3_chot_nguon_duy_nhat_ma_tran_ci,lp.t162_M4_evaluator_toi_gian_chuan_bi):
            try:
                with contextlib.redirect_stdout(io.StringIO()): fn()
                result.append(fn.__name__.split('_')[0]+':PASS')
            except Exception as ex:
                result.append(fn.__name__.split('_')[0]+':FAIL '+str(ex))
        errors=ci.loi_g5_workflow(data)
        print(name, '; '.join(result), '; ci_dang_ky.loi_g5_workflow=',errors)
        if name=='baseline': assert not errors
        else:
            assert result==['t161:PASS','t162:PASS']
            assert errors
print('Scope: t162 validates chuan-bi.outputs.os; exclude/job-if are separately checked by ci_dang_ky_test.py, not t162.')
print('No assertion that the complete gate remains green on these mutants.')
