import contextlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from review_checks import ROOT, TMP, record, BASE, SHA, E
from review_mutations import load, VARIANTS

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
t = load(TMP / 'head/ops/bien_nhan_v2_test.py', 'probes')

def out(**kw):
    print(json.dumps(kw, ensure_ascii=False), flush=True)

def git(dr, *args, **kw):
    p = subprocess.run(['git', '-C', str(dr), *args], capture_output=True, text=True, **kw)
    assert p.returncode == 0, (args, p.returncode, p.stderr)
    return p.stdout.strip()

def fixture(dr, token=None):
    k = t._kho_cau(dr)
    token = token or k['M'][:7]
    al = t._ghi_bn_cau(dr, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Ban {token} chua vao master.\n')})
    return k, al

def pair(dr, al, env=None):
    rows = []
    for debt in [False, True]:
        rc, err = t._chay_cli(dr, al, {('r.receipt.yaml', 'anchor.mo_ta', 'L-ANCESTRY')} if debt else (), env=env)
        rows.append(dict(debt=debt, rc=rc, dead='NỢ CHẾT' in err, traceback='Traceback' in err, stderr=err))
    return rows

def wrapper(dr, body):
    dr.mkdir(parents=True, exist_ok=True)
    p = dr / 'git'
    p.write_text('#!' + sys.executable + '\nimport os,sys\na=sys.argv[1:]\n' + body + '\nos.execv(' + repr(shutil.which('git')) + ', [' + repr(shutil.which('git')) + ']+a)\n')
    p.chmod(0o755)
    return {'PATH': str(dr) + os.pathsep + os.environ['PATH']}

def r5():
    specs = {
        'u3': ('        if gt not in ("true", "false"):\n', '        if False:\n'),
        'u4': ('"config", "--type=bool", "--get-regexp"', '"config", "--get-regexp"'),
        'u7': ('_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH"})', '_GIT_GIU = frozenset({"GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH", "GIT_DIR"})'),
    }
    allrows = {}
    for name, change in specs.items():
        t._dot_bien_tep(*change)
        mutant = t.bnv2
        with tempfile.TemporaryDirectory() as temp:
            dr = Path(temp)
            k, al = fixture(dr)
            env = {}
            if name == 'u3':
                env = wrapper(dr / '_bin', 'if "config" in a and "--type=bool" in a:\n print("remote.archive.promisor maybe"); sys.exit(0)')
            elif name == 'u4':
                k['g']('config', 'remote.archive.promisor', 'off')
            else:
                other = dr / '_khac'
                other.mkdir()
                kk = t._kho_cau(other)
                kk['g']('update-ref', 'refs/heads/master', kk['X'])
                env = {'GIT_DIR': str(other / '.git')}
                out(case=name, root_ancestry=git(dr, 'rev-parse', 'master'), other_master=kk['g']('rev-parse', 'master'), fsck_other=git(other, 'fsck', '--no-reflogs'))
            out(case=name, fsck=git(dr, 'fsck', '--no-reflogs'))
            row = {}
            for label, mod in [('head', t._BNV2_THAT), ('mutant', mutant)]:
                t.bnv2 = mod
                row[label] = pair(dr, al, env)
            allrows[name] = row
            out(case=name, **row)
        t.bnv2, t.CONG = t._BNV2_THAT, TMP / 'head/ops/bien_nhan_v2.py'
    assert [x['rc'] for x in allrows['u3']['head']] == [2, 2]
    assert [x['rc'] for x in allrows['u3']['mutant']] == [1, 0]
    assert [x['rc'] for x in allrows['u4']['head']] == [1, 0]
    assert [x['rc'] for x in allrows['u4']['mutant']] == [2, 2]
    assert [x['rc'] for x in allrows['u7']['head']] == [1, 0]
    assert [x['rc'] for x in allrows['u7']['mutant']] == [0, 1]
    record('Hướng 4 — chạy lại CHÍNH u3/u4/u7 và witness lượt 5', 'Lệnh `python3 -B -u review_probes.py r5`. Trên HEAD: u3/config trả maybe → 2/2; u4/Git thật promisor=off → 1/0; u7/master kho ngoài=X → 1/0. Trên bản sao gỡ đúng chốt: tương ứng 1/0, 2/2, 0/1 (u7 có nợ in NỢ CHẾT). fsck các fixture=0. Hai số là không nợ/có nợ trúng khóa. Log `evidence/r5-witness.log`. Không nhận các hành vi mutant là lỗi hiện hữu trên HEAD; răng test được đo riêng bằng m134–m136.')

def cases(mode):
    rows = []
    cli = t._chay_cli
    kc = t._kiem_cau
    def cli_logged(*a, **kw):
        label = inspect.currentframe().f_back.f_locals.get('ten')
        rc, err = cli(*a, **kw)
        out(call='CLI', case=label, rc=rc, stderr=err)
        return rc, err
    def kc_logged(*a, **kw):
        caller = inspect.currentframe().f_back
        ret = kc(*a, **kw)
        out(call='kiem', case=caller.f_code.co_name, variant=caller.f_locals.get('ten'), rc=ret[0], violations=ret[1], unknown=ret[2].get('chua_do'), debt=ret[2].get('no_cau'))
        return ret
    t._chay_cli, t._kiem_cau = cli_logged, kc_logged
    nums = {77, 82, 84, 89, 90, 91, 92, 94, 95, 96} if mode == 'closure' else {69, 70, 71, 72, 73, 74, 75, 78, 79, 83, 86, 87, 88}
    for fn in t.CA:
        import re
        m = re.match(r'c(\d+)_', fn.__name__)
        if m and int(m[1]) in nums:
            result = t._chay_1(fn)
            rows.append((fn.__name__, result))
            out(target=fn.__name__, result=result)
    assert all(r[1][0] == 'qua' for r in rows)
    record('Hướng ' + ('5 — biên lỗi và đóng phản chứng lượt 1–4' if mode == 'closure' else '6 — M1/M3/M4 và B1/B3/B4/B6'), f'Lệnh `python3 -B -u review_probes.py {mode}`: {len(rows)}/{len(rows)} ca có sẵn `qua`; từng lời gọi CLI/API và output rc/diagnostic được ghi thật trong `evidence/{mode}.log`. Không sửa test; chỉ gắn bộ ghi vào helper khi chạy trên bản sao. ' + ('c91 đo 17 nguồn × 2 trạng thái nợ, c77 đo JSON/UTF8 lỗi, c92 đo hai cờ sinh nợ; c94/c95/c96 đo giao thức/env/rc.' if mode == 'closure' else 'Bỏ mốc không còn miễn câu; OID thiếu theo bốn ngữ cảnh; token thuần có/không resolve; surface ba dòng/cả hai thứ tự/caveat; literal và folded.'))

def stderr():
    results = {}
    for mode in ['same-error-wrong-ancestry', 'health-error', 'health-rc3-false', 'probe-deleted-only']:
        with tempfile.TemporaryDirectory() as temp:
            dr = Path(temp)
            k, al = fixture(dr)
            if mode == 'same-error-wrong-ancestry':
                body = 'if "--git-dir" in a or "merge-base" in a:\n print("error: probe cannot inspect repository state",file=sys.stderr)\n if "merge-base" in a: sys.exit(1)'
            elif mode == 'health-error':
                body = 'if "--is-shallow-repository" in a:\n print("false"); print("error: health broken",file=sys.stderr); sys.exit(0)'
            elif mode == 'health-rc3-false':
                body = 'if "--is-shallow-repository" in a:\n print("false"); sys.exit(3)'
            else:
                body = 'if "--git-dir" in a:\n print("error: probe broken",file=sys.stderr); sys.exit(3)'
            env = wrapper(dr / '_bin', body)
            rows = pair(dr, al, env)
            results[mode] = [r['rc'] for r in rows]
            out(case=mode, results=rows)
    assert results == {'same-error-wrong-ancestry':[2,2], 'health-error':[2,2], 'health-rc3-false':[2,2], 'probe-deleted-only':[1,0]}
    record('Hướng 7 — lỗi stderr trùng probe và rc sức khỏe', 'Lệnh `python3 -B -u review_probes.py stderr`: same-error-wrong-ancestry=2/2; health-error=2/2; health rc3 dù stdout=false=2/2; chỉ lỗi ở probe --git-dir đã xóa=1/0. Đóng phản chứng nuốt stderr lượt 4 và chốt rc/probe. Đây là fault injection bằng wrapper chuyển tiếp Git thật, không khai Git tự sinh chẩn đoán giả. Log `evidence/stderr.log`.')

def batch_witness():
    for name in ['v1-batch-oid', 'v2-batch-type']:
        mutant = load(TMP / name / 'ops/bien_nhan_v2.py', name)
        with tempfile.TemporaryDirectory() as temp:
            dr = Path(temp)
            # Token thuần chữ không ngữ cảnh: stdout sai loại sẽ bị mutant coi là không phải OID.
            k = t._kho_cau(dr)
            sha = t._commit_tien_to_so(dr, k, str.isalpha, 'chu', 30000)
            k['g']('merge', '-q', '--no-ff', sha, '-m', 'merge')
            al = t._ghi_bn_cau(dr, k, {'r.receipt.yaml': t._bn_cau(1, f'anchor:\n    mo_ta: Ban {sha[:7]} chua vao master.\n')})
            body = 'if "cat-file" in a and any(x.startswith("--batch-check") for x in a):\n x=sys.stdin.read().strip()\n print(' + (repr('0'*40+' commit') if name.startswith('v1') else 'x+" nonsense"') + '); sys.exit(0)'
            env = wrapper(dr / '_bin', body)
            rows = {}
            for label, mod in [('head', t._BNV2_THAT), ('mutant', mutant)]:
                t.bnv2 = mod
                rows[label] = pair(dr, al, env)
            t.bnv2 = t._BNV2_THAT
            out(variant=name, token=sha[:7], fsck=git(dr, 'fsck', '--no-reflogs'), **rows)
            assert [x['rc'] for x in rows['head']] == [2,2]
            assert [x['rc'] for x in rows['mutant']] == ([1,0] if name.startswith('v1') else [0,1])
    record('Hướng 8 — witness độc lập cho hai guard batch-check', 'Lệnh `python3 -B -u review_probes.py batch-witness`: chỉ thay stdout cat-file, rc=0/stderr rỗng. Sai OID (v1): HEAD2/2 → mutant1/0. Sai loại nonsense (v2), token thật thuần chữ dbffbbc không ngữ cảnh: HEAD2/2 → mutant0/1, lượt có nợ in NỢ CHẾT. Kho fixture fsck=0; đây là fault injection giao thức tương tự c94, không phải trạng thái Git thật tự sinh. Đang chờ đủ93ca để xác định thiếu răng. Log `evidence/batch-witness.log`.')

def mixed_witness():
    mutant=load(TMP/'v3-mixed-context/ops/bien_nhan_v2.py','mixed')
    with tempfile.TemporaryDirectory() as temp:
        dr=Path(temp)
        k,al=fixture(dr,'12ab34c')
        assert t._BNV2_THAT._commit_cua(dr,'12ab34c') is None
        rows={}
        for label,mod in [('head',t._BNV2_THAT),('mutant',mutant)]:
            t.bnv2=mod
            rows[label]=pair(dr,al)
        t.bnv2=t._BNV2_THAT
        out(case='mixed-only-no-commit-no-backtick', token='12ab34c', fsck=git(dr,'fsck','--no-reflogs'), **rows)
        assert [x['rc'] for x in rows['head']]==[2,2]
        assert [x['rc'] for x in rows['mutant']]==[0,1]
    record('Hướng 12 — ngữ cảnh trộn số/chữ bị từ Commit che trong fixture', 'Lệnh `python3 -B -u review_probes.py mixed-witness`: fixture Git thật, câu `Ban 12ab34c chua vao master.`; token không resolve, không backtick/từ commit; fsck=0. HEAD2/2; bản sao chỉ bỏ `_oid_tron(x)` trong `_oid_bat_buoc` thành0/1, có nợ kết luận NỢ CHẾT. c71 hiện dùng `Commit 1234abc`, nên ngữ cảnh sau commit vẫn cứu được phép đo khi gỡ chốt trộn số/chữ. Đang chờ đủ93ca; log `evidence/mixed-witness.log`.')

def surface_errors():
    rows=[]
    for name,value in [('JSON-invalid',b'{bad'),('UTF8-invalid',b'\xff'),('JSON-array',b'[]'),('JSON-null',b'null'),('surface-empty',b'{"execution_surface":""}')]:
        with tempfile.TemporaryDirectory() as temp:
            dr=Path(temp)
            d,_=t._bn_surface('ops/reviews/v/run.json','')
            al=t._kho_surface(dr,d,'{"execution_surface":"codex_cli"}','provider: openai_codex\nexecution_surface: codex_service\n')
            (dr/'ops/reviews/v/run.json').write_bytes(value)
            for debt in [False,True]:
                rc,err=t._chay_cli(dr,al,{('r.receipt.yaml','verdict_path','L-SURFACE')} if debt else ())
                out(case=name,debt=debt,rc=rc,stderr=err)
                assert rc==2 and 'NỢ CHẾT' not in err and 'Traceback' not in err and 'run.json' in err
                rows.append(rc)
    record('Hướng 16 — run.json hỏng qua CLI cả hai trạng thái nợ', 'Lệnh `python3 -B -u review_probes.py surface-errors`: thay đúng run.json của fixture có sẵn thành JSON lỗi, UTF8 lỗi, JSON mảng, null, surface rỗng; **10/10 lượt CLI rc=2**, có/không nợ L-SURFACE trúng khóa, stderr nêu run.json, không Traceback/NỢ CHẾT. Bổ sung bằng chứng CLI cho c77 API. Log `evidence/surface-errors.log`.')

if __name__ == '__main__':
    modes = {'r5': r5, 'closure': lambda: cases('closure'), 'acceptance': lambda: cases('acceptance'), 'stderr': stderr, 'batch-witness': batch_witness, 'mixed-witness':mixed_witness, 'surface-errors':surface_errors}
    modes[sys.argv[1]]()
