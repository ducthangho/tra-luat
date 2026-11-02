import ast
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT/'cay-kho'
sys.path.insert(0, str(Path(__file__).parent))
from probe import load, case, clean

def git(*a):
    return subprocess.check_output(['git','-C',str(REPO),*a])

def mutants(source):
    return {n.args[0].value: n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='do' and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)}

def body(source, name):
    tree = ast.parse(source)
    n = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name==name)
    n.name = 'same_name'
    if ast.get_docstring(n) is not None:
        n.body = n.body[1:]
    return ast.dump(n, include_attributes=False)

def main():
    history = []
    for commit, expected in [('5efa311',range(144,148)),('8d9e3e3',range(148,154)),('e9e0048',range(154,156))]:
        before = mutants(git('show',f'{commit}^:ops/bien_nhan_v2_test.py'))
        after = mutants(git('show',f'{commit}:ops/bien_nhan_v2_test.py'))
        added = sorted(set(after)-set(before))
        assert set(added)=={n for n in after for i in expected if n.startswith(f'm{i}_')}, added
        history.append({'commit':git('rev-parse',commit).decode().strip(),'new_mutants':added})
    old_name = 'c98_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen'
    new_name = 'c101_chon_bien_nhan_KHONG_phan_biet_hoa_thuong_tren_moi_nen'
    same_body = body(git('show','e9e0048:ops/bien_nhan_v2_test.py'),old_name)==body(git('show','HEAD:ops/bien_nhan_v2_test.py'),new_name)
    assert same_body
    print(json.dumps({'history':history,'c98_to_c101_body_equal_without_docstring':same_body},ensure_ascii=False))
    s = load()
    observations = []
    for prefix in ('c88','c89','c98','c99','c100','c101'):
        result = s._chay_1(case(s,prefix))
        assert result[0]=='qua', result
        row = {'case':case(s,prefix).__name__,'result':result}
        print(json.dumps(row,ensure_ascii=False))
        observations.append(row)
    current = mutants((REPO/'ops/bien_nhan_v2_test.py').read_bytes())
    for i in (144,145,146):
        name = next(n for n in current if n.startswith(f'm{i}_'))
        call = next(n for n in ast.walk(current[name].args[1]) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='_dot_bien_tep')
        old,new = [ast.literal_eval(n) for n in call.args[:2]]
        try:
            s._dot_bien_tep(old,new)
            result = s._chay_1(case(s,'c101'))
            control = s._sach_hoan_toan(case(s,'c18'))
            assert result[0]=='qua' and control[0], (result,control)
            row = {'mutation':name,'non_target':'c101','result':result,'control':control}
            print(json.dumps(row,ensure_ascii=False))
            observations.append(row)
        finally:
            clean(s)
    # The same suffix direction referenced as t27 is checked using its existing fixture.
    with tempfile.TemporaryDirectory(prefix='review-t27-') as t:
        path=Path(t)/'ops/lease_publish_test.py'
        path.parent.mkdir(parents=True)
        source=(REPO/'ops/lease_publish_test.py').read_text()
        path.write_text(source)
        def import_t27():
            spec=importlib.util.spec_from_file_location('lease_suffix_probe',path)
            m=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
        name='t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen'
        baseline=import_t27()
        getattr(baseline,name)()
        old='p.is_file() and p.name.lower().endswith(d)'
        new='p.is_file() and p.name.endswith(d)'
        assert source.count(old)==1
        path.write_text(source.replace(old,new))
        mutated=import_t27()
        try:
            getattr(mutated,name)()
        except AssertionError as ex:
            row={'case':name,'baseline':'qua','mutant':'assertion_failed','detail':str(ex),'old':old,'new':new}
        else:
            raise AssertionError('t27 suffix mutation survived')
        print(json.dumps(row,ensure_ascii=False))
        observations.append(row)
    (ROOT/'evidence/references.json').write_text(json.dumps({'history':history,'rename_body_equal':same_body,'observations':observations},ensure_ascii=False,indent=2))
    print('REFERENCES: history matches 1/2/3; rename AST equal; 6/6 current cases qua; c101 survives m144/145/146; t27 suffix mutant killed')

if __name__=='__main__':
    main()
