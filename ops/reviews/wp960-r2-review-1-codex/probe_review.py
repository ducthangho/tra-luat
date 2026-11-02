"""Review measurements: existing fixtures/cases, copied code and local Git only."""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.environ.get('WP960_REVIEW_COPY', '/tmp/wp960-r2-review-copy'))
spec = importlib.util.spec_from_file_location('review_tests', ROOT / 'ops/bien_nhan_v2_test.py')
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
b = t.bnv2

def emit(label, **values):
    print(json.dumps({'label': label, **values}, ensure_ascii=False), flush=True)

def measure(root, al, debt=frozenset()):
    try:
        rc, errors, stats = t._kiem_cau(root, al, debt)
        return dict(rc=rc, errors=errors, unknown=stats.get('chua_do'), skipped=stats.get('surface_chua_do'))
    except Exception as ex:
        return dict(exception=type(ex).__name__, detail=str(ex))

def cli(root, al, debt=frozenset()):
    old = b.ALLOWLIST_CUTOVER, b.NO_DA_DO, b.NO_CAU_LICH_SU
    out, err = io.StringIO(), io.StringIO()
    try:
        b.ALLOWLIST_CUTOVER, b.NO_DA_DO, b.NO_CAU_LICH_SU = al, {}, debt
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = b.main(['--root', str(root)])
        return dict(rc=rc, stdout=out.getvalue().strip(), stderr=err.getvalue().strip())
    except Exception as ex:
        return dict(exception=type(ex).__name__, detail=str(ex), stdout=out.getvalue(), stderr=err.getvalue())
    finally:
        b.ALLOWLIST_CUTOVER, b.NO_DA_DO, b.NO_CAU_LICH_SU = old

def boundaries():
    # Selectively make Git fail to EXECUTE; Git is real during fixture construction.
    for name, sentence in [('ordinary', 'Run 40268583940 va deadbeef chua vao master.'),
                            ('explicit', 'Commit deadbeef chua vao master.')]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            k = t._kho_cau(root)
            al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: {sentence}\n')})
            emit('git-control-'+name, result=measure(root, al))
            with tempfile.TemporaryDirectory() as no_git:
                path = os.environ.get('PATH')
                os.environ['PATH'] = no_git
                try:
                    emit('git-absent-'+name, git_result=b._git(root, 'rev-parse', '--verify', '--quiet', 'deadbeef^{commit}'), result=cli(root, al))
                finally:
                    os.environ['PATH'] = path or ''
    # A real pure-letter Git commit is an unconditional candidate, even without context.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        k = t._kho_cau(root)
        sha = t._commit_tien_to_so(root, k, str.isalpha, 'chu', 30000)
        k['g']('merge', '-q', '--no-ff', sha, '-m', 'merge')
        al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Ban {sha[:7]} chua vao master.\n')})
        emit('pure-real-control', oid=sha, result=measure(root, al))
        with tempfile.TemporaryDirectory() as no_git:
            path = os.environ.get('PATH')
            os.environ['PATH'] = no_git
            try:
                emit('pure-real-git-absent', oid=sha, result=cli(root, al))
            finally:
                os.environ['PATH'] = path or ''
    # Programming error mutation: the catch exposes its type but turns it into rc=2.
    old = b._bo_dau
    def programmer_bug(_):
        return nonexistent_local_variable  # deliberate reviewer mutation
    b._bo_dau = programmer_bug
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            k = t._kho_cau(root)
            al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Commit {k["M"][:7]} chua vao master.\n')})
            emit('programming-name-error', result=cli(root, al))
    finally:
        b._bo_dau = old

def errors():
    # Four B2 sources, with/without corresponding debt; use existing builders unchanged.
    for kind in ('receipt-directory', 'json-invalid', 'branch-tree', 'alias-cycle', 'receipt-utf8', 'receipt-yaml', 'json-utf8', 'run-directory'):
        for has_debt in (False, True):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                if kind in ('json-invalid', 'json-utf8', 'run-directory'):
                    d, _ = t._bn_surface('ops/reviews/v/run.json', '')
                    al = t._kho_surface(root, d, '{bad json' if kind == 'json-invalid' else '{"execution_surface":"codex_cli"}',
                                        'provider: openai_codex\nexecution_surface: codex_service\n')
                    key = ('r.receipt.yaml', 'verdict_path', b.LUAT_SURFACE)
                    if kind == 'json-utf8':
                        (root/'ops/reviews/v/run.json').write_bytes(b'{"execution_surface":"\xff"}')
                    elif kind == 'run-directory':
                        (root/'ops/reviews/v/run.json').unlink()
                        (root/'ops/reviews/v/run.json').mkdir()
                else:
                    k = t._kho_cau(root)
                    text = t._bn_cau(1, 'cycle: &self [*self]\n' if kind == 'alias-cycle' else f'anchor:\n    mo_ta: Commit {k["M"][:7]} chua vao master.\n')
                    al = t._ghi_bn_cau(root, k, {'r.receipt.yaml': text})
                    key = ('r.receipt.yaml', 'anchor.mo_ta', b.LUAT_ANCESTRY)
                    p = root/b.THU_MUC/'r.receipt.yaml'
                    if kind == 'receipt-directory':
                        p.unlink(); p.mkdir()
                    elif kind == 'receipt-utf8':
                        p.write_bytes(b'schema_version: 1\nx: \xff\n')
                    elif kind == 'receipt-yaml':
                        p.write_text('schema_version: [bad\n', encoding='utf-8')
                debt = frozenset({key}) if has_debt else frozenset()
                old = b._nhanh_mac_dinh
                if kind == 'branch-tree':
                    tree = k['g']('rev-parse', 'HEAD^{tree}')
                    b._nhanh_mac_dinh = lambda _: tree
                try:
                    result = cli(root, al, debt)
                    emit(kind, has_debt=has_debt, result=result,
                         traceback='Traceback' in result.get('stderr', ''), dead='NỢ CHẾT' in result.get('stderr', ''))
                finally:
                    b._nhanh_mac_dinh = old

def b2coverage():
    old = b.kiem
    for fn in (t.c77_run_json_CO_ma_HONG_la_KHONG_DO_DUOC_khong_phai_no_chet,
               t.c82_alias_VONG_la_KHONG_DO_DUOC_alias_dung_lai_van_duyet,
               t.c84_merge_base_HONG_la_KHONG_DO_DUOC_khong_phai_vi_pham,
               t.c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback,
               t.c90_B2_MOT_BIEN_loi_do_khong_traceback_khong_no_chet):
        calls = []
        def spy(root, **kw):
            calls.append({'debt': sorted(kw.get('no_cau_lich_su') or []), 'explicit_debt_arg': 'no_cau_lich_su' in kw})
            return old(root, **kw)
        b.kiem = spy
        try:
            result = t._chay_1(fn)
        finally:
            b.kiem = old
        emit('coverage', case=fn.__name__, result=result, calls=calls)

def auxiliary():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp); k=t._kho_cau(root)
        al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,'x: 1\n')})
        (root/b.THU_MUC/'directory.receipt.yaml').mkdir()
        for flag in ('--sinh-no','--sinh-no-cau-lich-su'):
            out,err=io.StringIO(),io.StringIO()
            result={}
            try:
                with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
                    result['rc']=b.main(['--root',str(root),flag])
            except Exception as ex:
                result={'exception':type(ex).__name__,'detail':str(ex)}
            emit('auxiliary',flag=flag,result=result,stdout=out.getvalue(),stderr=err.getvalue())
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp); k=t._kho_cau(root)
        al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Commit {k["M"][:7]} chua vao master.\n')})
        tree=k['g']('rev-parse','HEAD^{tree}')
        k['g']('update-ref','refs/remotes/origin/master',tree)
        try:
            chosen=b._nhanh_mac_dinh(root); failure=None
        except Exception as ex:
            chosen=None;failure=type(ex).__name__+': '+str(ex)
        emit('default-tree-fallback',canonical=tree,chosen=chosen,selection_error=failure,local_master=k['g']('rev-parse','master'),result=cli(root,al))

def rawcli():
    import shutil
    from probe_mutations import MUTATIONS
    runner='''import importlib.util,json,sys
sp=importlib.util.spec_from_file_location('gate',sys.argv[1]);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
c=json.loads(sys.argv[2]);m.ALLOWLIST_CUTOVER=c['allow'];m.NO_DA_DO={};m.NO_CAU_LICH_SU=frozenset(tuple(x) for x in c['debt'])
raise SystemExit(m.main(sys.argv[3:]))
'''
    def run(root,al,args=(),source=None,env=None):
        p=subprocess.run([sys.executable,'-c',runner,str(source or ROOT/'ops/bien_nhan_v2.py'),
                          json.dumps({'allow':al,'debt':[]}), '--root',str(root),*args],capture_output=True,text=True,env=env)
        return dict(rc=p.returncode,traceback='Traceback' in p.stderr,stdout=p.stdout.strip(),stderr=p.stderr.strip())
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);k=t._kho_cau(root)
        al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,'x: 1\n')})
        (root/b.THU_MUC/'directory.receipt.yaml').mkdir()
        for flag in ('--sinh-no','--sinh-no-cau-lich-su'):
            emit('subprocess',flag=flag,result=run(root,al,(flag,)))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);k=t._kho_cau(root)
        sha=t._commit_tien_to_so(root,k,str.isalpha,'chu',30000)
        k['g']('merge','-q','--no-ff',sha,'-m','merge')
        al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Ban {sha[:7]} chua vao master.\n')})
        emit('subprocess-pure-real',result=run(root,al))
        with tempfile.TemporaryDirectory() as missing:
            emit('subprocess-pure-real-no-git',result=run(root,al,env=dict(os.environ,PATH=missing)))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);k=t._kho_cau(root)
        al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,'x: 1\n')})
        (root/b.THU_MUC/'r.receipt.yaml').write_bytes(b'schema_version: 1\nx: \xff\n')
        emit('subprocess-utf8-control',result=run(root,al))
        old,cong=t.bnv2,t.CONG
        try:
            t._dot_bien_tep(*MUTATIONS['r8-receipt-encoding'])
            emit('subprocess-utf8-mutant',result=run(root,al,source=t.CONG))
        finally:
            t.bnv2,t.CONG=old,cong
            while t._TAM_DOT_BIEN:shutil.rmtree(t._TAM_DOT_BIEN.pop(),ignore_errors=True)

def witnesses():
    import shutil
    from probe_mutations import MUTATIONS
    global b
    for name,text in (
        ('r2-commit-boundary','Precommit 1234567 chua vao master.'),
        ('r3-commit-adjacent','Commit phien nay so 1234567 chua vao master.'),
        ('r4-backtick-close','Ban `abcdefa chua vao master.'),
        ('r5-provider-boundary','notprovider: openai_codex\nexecution_surface: codex_service\n'),
        ('r6-window-next','execution_surface: codex_service\nprovider: openai_codex\n'),
        ('r8-receipt-encoding','')):
        old_b,old_cong=b,t.CONG
        results=[]
        for changed in (False,True):
            if changed:
                t._dot_bien_tep(*MUTATIONS[name]);b=t.bnv2
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    root=Path(tmp)
                    if name in ('r5-provider-boundary','r6-window-next'):
                        d,_=t._bn_surface('ops/reviews/v/run.json','')
                        al=t._kho_surface(root,d,'{"execution_surface":"codex_cli"}',text)
                    else:
                        k=t._kho_cau(root)
                        al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: {text or "x"}\n')})
                        if name=='r8-receipt-encoding':
                            (root/b.THU_MUC/'r.receipt.yaml').write_bytes(b'schema_version: 1\nx: \xff\n')
                    results.append({'changed':changed,'result':cli(root,al)})
            finally:
                if changed:
                    b=t.bnv2=old_b;t.CONG=old_cong
                    while t._TAM_DOT_BIEN:shutil.rmtree(t._TAM_DOT_BIEN.pop(),ignore_errors=True)
        emit('mutant-witness',mutation=name,text=text,results=results)

def baseline():
    basepath = Path('/tmp/wp960-r2-base-repo')
    sp = importlib.util.spec_from_file_location('base_gate', basepath/'ops/bien_nhan_v2.py')
    bm = importlib.util.module_from_spec(sp); sp.loader.exec_module(bm)
    old_module, old_bang, old_kiem = t.bnv2, t.bang, t._kiem_cau
    t.bnv2 = bm
    t.bang = lambda condition, message: None
    for fn in (t.c86_B1_moc_dung_tai_KHONG_con_mien, t.c87_B3_OID_khong_tra_duoc_theo_NGU_CANH,
               t.c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan,
               t.c83_MOI_khai_bao_surface_tren_cung_dong_deu_duoc_xet,
               t.c71_A2_cau_ancestry_do_bang_merge_base,
               t.c78_OID_viet_tat_TOAN_CHU_SO_van_duoc_tra):
        results=[]
        def wrap(root, al, no=frozenset()):
            rc, errs, tk = old_kiem(root, al, no)
            results.append({'rc':rc,'errors':errs,'unknown':tk.get('chua_do')})
            return rc, errs, tk
        t._kiem_cau = wrap
        emit('base-case', case=fn.__name__, status=t._chay_1(fn), results=results)
    t.bnv2, t.bang, t._kiem_cau = old_module, old_bang, old_kiem

if __name__ == '__main__':
    globals()[sys.argv[1]]()
