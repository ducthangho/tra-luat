#!/usr/bin/env python3
"""Offline reviewer probes. All source mutations live outside cay/."""
import ast
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'ket-qua'
SRC = ROOT / 'cay/ops/lease_publish_test.py'
SOURCE = SRC.read_text()
sys.dont_write_bytecode = True
os.environ['PATH'] = str(ROOT / 'cong-cu') + os.pathsep + os.environ['PATH']
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

def module(source=SOURCE, path=SRC):
    m = type(sys)('review_lpt')
    m.__file__ = str(path)
    exec(compile(source, str(path), 'exec'), m.__dict__)
    return m

M = module()

def mutate(source, old, new):
    changed, count = M._dot_bien_nguon_512(source, old, new)
    assert count == 1 and changed is not None, (count, old)
    return changed

def remove_guard(source, fragment, func='_doc_kenh_xac_thuc'):
    tree = ast.parse(source)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == func)
    found = [n for n in ast.walk(fn) if isinstance(n, ast.If)
             and fragment in ast.get_source_segment(source, n)]
    node = min(found, key=lambda n: n.end_lineno-n.lineno)
    lines = source.splitlines(keepends=True)
    old = ''.join(lines[node.lineno-1:node.end_lineno])
    return mutate(source, old, ' ' * node.col_offset + 'pass  # reviewer: remove one guard\n')

def scratch(source, name):
    d = M._cay_mut_512(name)
    p = d / 'ops/lease_publish_test.py'
    p.write_text(source)
    return d, p

def run_case(source, case, name, extra_env=None):
    d, p = scratch(source, name)
    env = dict(os.environ)
    env.pop('GITHUB_ACTOR', None)
    for key in (M.KENH_ENV, M.DAU_PHIEN_ENV, M.MUTANT_ENV, M.LAN_THU_ENV, M.CO_KQ_JSON, M.CO_TU_KIEM_CTRL):
        env.pop(key, None)
    env.update(extra_env or {})
    try:
        r = subprocess.run([sys.executable, '-B', str(p), '--chi-ca='+case],
                           capture_output=True, env=env, timeout=1000)
        out = r.stdout.decode('utf-8', 'replace')
        (OUT / (name+'.log')).write_bytes(r.stdout + b'\nSTDERR\n' + r.stderr)
        summary = [s for s in out.splitlines() if any(x in s for x in
                   ('tự kiểm bộ chấm', 'tukiem', 'lease_publish:', 'chốt fail-close', '!!! do', 'catalog 512:', 'control 512:'))]
        print(name, 'rc='+str(r.returncode), *summary, sep='\n', flush=True)
        return r, d
    finally:
        shutil.rmtree(d)

def real_channel(name, signal=False):
    s = SOURCE
    if signal:
        c = M.CONTROL_512[-2]
        s = mutate(s, c[2], c[3])
    p = OUT / (name+'.jsonl')
    p.unlink(missing_ok=True)
    r, _ = run_case(s, 't160', name, {M.KENH_ENV:str(p), M.DAU_PHIEN_ENV:'dp',
                       M.MUTANT_ENV:'mt', M.LAN_THU_ENV:'1'})
    return p, r.returncode

def absorption():
    p, rc = real_channel('absorption-live', True)
    rows = [json.loads(l) for l in p.read_text().splitlines()]
    case, closing = rows
    target = (case['ca'],)
    # Recombine existing case/closing fixtures, retaining a real prior case record.
    mixed = dict(closing, ca=case['ca'])
    q = OUT / 'absorption-mixed.jsonl'
    q.write_text('\n'.join(json.dumps(x) for x in [case, mixed])+'\n')
    removed = module(remove_guard(SOURCE, 'bản ghi vừa mang tên ca vừa khai đóng lượt'))
    print('mixed-record original=', M.doc_kenh(q,'dp','mt',1,target,'t160',rc), flush=True)
    print('mixed-record guard-removed=', removed.doc_kenh(q,'dp','mt',1,target,'t160',rc), flush=True)
    run_case(remove_guard(SOURCE, 'bản ghi vừa mang tên ca vừa khai đóng lượt'), 't164', 'absorption-t164-mixed')
    # Reuse t164's non-object list as a label value to reach the outer exception boundary.
    bad = dict(case, nhan=[1, 2])
    q = OUT / 'absorption-unhashable.jsonl'
    q.write_text('\n'.join(json.dumps(x) for x in [bad,closing])+'\n')
    without_catch = mutate(SOURCE, '    except Exception as exc:                  # noqa: BLE001 — fail-close CÓ CHỦ ĐÍCH',
                          '    except KeyError as exc:  # reviewer: do not catch TypeError')
    print('outer-wrapper original=', M.doc_kenh(q,'dp','mt',1,target,'t160',rc), flush=True)
    try:
        print('outer-wrapper guard-removed=', module(without_catch).doc_kenh(q,'dp','mt',1,target,'t160',rc), flush=True)
    except Exception as exc:
        print('outer-wrapper guard-removed ESCAPED', type(exc).__name__, str(exc), flush=True)
    run_case(without_catch, 't164', 'absorption-t164-wrapper')

def materialization():
    p, rc = real_channel('materialization-live', False)
    target = M._ten_day_du_512('t160')
    old, new = M.DOT_BIEN_TU_KIEM_512[-1][2][1]
    b = module(mutate(SOURCE, old, new))
    print('direct original', M.doc_kenh(p,'dp','mt',1,iter(target),'t160',rc), flush=True)
    print('direct remove-B', b.doc_kenh(p,'dp','mt',1,iter(target),'t160',rc), flush=True)
    old, new = M.DOT_BIEN_TU_KIEM_512[-1][2][0]
    a = module(mutate(SOURCE, old, new))
    ctrl = M.CONTROL_512[-2]
    for label, mod in [('original',M), ('remove-A',a)]:
        seen=[]
        def retry(*args):
            actual=mod.doc_kenh(*args)
            seen.append(actual)
            return (mod.KHONG_DO_DUOC,'reviewer exercises retry') if len(seen)==1 else actual
        result=mod._chay_mot_mutant_512(*ctrl[:4], SOURCE, doc=retry)
        print('retry',label,'readings=',seen,'result=',result,flush=True)

def m5_falsecredit():
    old='    chot(not lech, f"control LỆCH phân hạng: {lech}")'
    new=('    if lech and any(t == KHONG_DO_DUOC and t != m for (_, t, _), m in zip(ra, mong)):\n'
         '        raise Exception(f"control LỆCH phân hạng: {lech}")\n'+old)
    changed=mutate(SOURCE,old,new)
    run_case(changed,'t163','m5-kdd-unrelated')
    # Inspect the actual child channel for the except-order case.
    item=M.DOT_BIEN_TU_KIEM_512[1]
    for old,new in item[2]:
        changed=mutate(changed,old,new)
    p=OUT/'m5-unrelated-real.jsonl'; p.unlink(missing_ok=True)
    run_case(changed,'t162','m5-unrelated-child',{M.CO_TU_KIEM_CTRL:item[1],M.KENH_ENV:str(p),
        M.DAU_PHIEN_ENV:'dp',M.MUTANT_ENV:'mt',M.LAN_THU_ENV:'1',M.CO_KQ_JSON:str(OUT/'m5-unrelated-results.json')})
    print('actual child records',p.read_text(),flush=True)

def guard_matrix():
    fragments = [
        'kênh không tồn tại', 'bản ghi không phải object', 'có bản ghi SAU bản ghi đóng lượt',
        'bản ghi không neo đúng lượt', 'dấu đóng lượt không phải bool true',
        'bản ghi vừa mang tên ca vừa khai đóng lượt', 'bản ghi thiếu tên ca',
        'tên ca không phải chuỗi', 'bản ghi TRÙNG', 'nhãn không hợp lệ',
        'chi tiết không phải chuỗi', 'thiếu bản ghi đóng lượt',
        'bản ghi đóng lượt thiếu rc kiểu int', 'rc đóng lượt', 'kênh KHÔNG có bản ghi ca nào',
        'kênh có ca KHÔNG khớp tiền tố', 'đích RỖNG', 'đích KHÔNG có mặt trong kênh',
        'ca ĐỎ vì ngoại lệ KHÔNG phải TinHieuChotCa',
    ]
    results=[]
    for i, f in enumerate(fragments):
        if f == 'rc đóng lượt':
            changed=remove_guard(SOURCE, '!= rc tiến trình')
        else:
            changed=remove_guard(SOURCE, f)
        print('GUARD',i,f,flush=True)
        r,_=run_case(changed,'t164',f'guard-{i:02}')
        results.append({'index':i,'guard':f,'t164_rc':r.returncode})
    (OUT/'guard-matrix.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))

def kdd_teeth():
    variants=[
        ('rc-match',remove_guard(SOURCE,'!= rc tiến trình')),
        ('closing-present',remove_guard(SOURCE,'thiếu bản ghi đóng lượt')),
        ('true-flag',remove_guard(SOURCE,'dấu đóng lượt không phải bool true')),
    ]
    for label,changed in variants:
        run_case(changed,'t163','kdd-teeth-'+label)

def declared():
    result=[]
    for item in M.DOT_BIEN_TU_KIEM_512:
        if item[3]=='XANH':
            continue
        changed=SOURCE
        for old,new in item[2]: changed=mutate(changed,old,new)
        mod=module(changed)
        ctrl=next(c for c in mod._muc_control_512() if c[0]==item[1])
        actual=mod._chay_mot_mutant_512(*ctrl[:4],changed)
        row={'item':item[0],'control':item[1],'expected':ctrl[4],'actual':actual}
        result.append(row)
        print(json.dumps(row,ensure_ascii=False),flush=True)
    (OUT/'declared.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))

def unguarded():
    p,rc=real_channel('unguarded-live',True)
    case,close=[json.loads(l) for l in p.read_text().splitlines()]
    target=(case['ca'],)
    variants=[('false-close-marker','dấu đóng lượt không phải bool true',[dict(case,dong_luot=False),close],target),
              ('nontext-detail','chi tiết không phải chuỗi',[dict(case,chi_tiet=[1,2]),close],target),
              ('prefix-mismatch','kênh có ca KHÔNG khớp tiền tố',[case,close],target),
              ('target-absent','đích KHÔNG có mặt trong kênh',[case,close],(case['ca'],M._ten_day_du_512('t159')[0]))]
    combined=SOURCE
    for label,fragment,rows,targets in variants:
        q=OUT/(label+'.jsonl'); q.write_text('\n'.join(json.dumps(x) for x in rows)+'\n')
        modified=remove_guard(SOURCE,fragment)
        prefix='t159' if label=='prefix-mismatch' else 't160'
        print(label,'original=',M.doc_kenh(q,'dp','mt',1,targets,prefix,rc),
              'guard-removed=',module(modified).doc_kenh(q,'dp','mt',1,targets,prefix,rc),flush=True)
        combined=remove_guard(combined,fragment)
    for ca in ('t161','t162','t163','t164'):
        run_case(combined,ca,'unguarded-combined-'+ca)

def transport():
    ctrl=M.CONTROL_512[-2]
    changed=mutate(SOURCE,'    print(*phan, flush=True)',
                   '    sys.stdout.buffer.write(bytes([255])); sys.stdout.buffer.flush()\n    print(*phan, flush=True)')
    seen=[]
    def read(*args):
        result=M.doc_kenh(*args); seen.append(result); return result
    print('non-UTF8 stdout',M._chay_mot_mutant_512(*ctrl[:4],changed,doc=read),'readings=',seen,flush=True)
    with mock.patch.object(M.subprocess,'run',side_effect=OSError('reviewer transport')) as run:
        print('spawn OSError',M._chay_mot_mutant_512(*ctrl[:4],SOURCE),'attempts=',run.call_count,flush=True)
    for stage in ('_cay_mut_512','sinh_dau_phien'):
        with mock.patch.object(M,stage,side_effect=OSError('reviewer setup')) as call:
            try:
                print(stage,M._chay_mot_mutant_512(*ctrl[:4],SOURCE),flush=True)
            except Exception as exc:
                print(stage,'ESCAPED',type(exc).__name__,str(exc),'attempts=',call.call_count,flush=True)

def old_fixes():
    raw=('            nhan, chi_tiet_kenh = NHAN_DO_KHAC, f"AssertionError trần: {ex}"')
    widened=mutate(SOURCE,raw,'            nhan, chi_tiet_kenh = (NHAN_DO_KHAC if isinstance(ex, TinHieuChotCa) else NHAN_DO_CHOT), str(ex)')
    run_case(widened,'t162','old-fix-raw-assertion')
    false_live=mutate(SOURCE,'    if do_chot == set(dich):','    if not do_chot or do_chot == set(dich):')
    run_case(false_live,'t162','old-fix-false-live')
    # Only modify source; never disable environment isolation in the reviewer process.
    inherited=mutate(SOURCE,'        os.environ.pop(b, None)','        pass  # reviewer: remove channel isolation')
    ctrl=next(c for c in M.DOT_BIEN_512 if c[0]=='bo-chot-selector-khong-khop')
    channels=[]
    def read(*args):
        channels.append(Path(args[0]).read_text())
        result=M.doc_kenh(*args); print('inheritance reading',result,flush=True); return result
    print('inheritance result',M._chay_mot_mutant_512(*ctrl[:4],inherited,doc=read),flush=True)
    for i,ch in enumerate(channels):
        (OUT/f'inherited-{i+1}.jsonl').write_text(ch)
        rows=[json.loads(x) for x in ch.splitlines()]
        print('inheritance rows',i+1,len(rows),'cases=',[x.get('ca') for x in rows if 'ca' in x],
              'closing=',sum(x.get('dong_luot') is True for x in rows),flush=True)

def seven_before():
    from concurrent.futures import ThreadPoolExecutor
    old_source=subprocess.check_output(['git','-C',str(ROOT/'kho-guong.git'),'show',
                    'd5e7e7d:ops/lease_publish_test.py']).decode()
    tree=ast.parse(old_source)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith('t164_'))
    lines=old_source.splitlines(keepends=True)
    # Reconstruct the pre-t164 measurement boundary; source of other tests is unchanged.
    before=''.join(lines[:fn.lineno-2]+lines[fn.end_lineno:])
    assert len(module(before).CA)==158
    fragments=['có bản ghi SAU bản ghi đóng lượt','bản ghi không neo đúng lượt',
               'bản ghi vừa mang tên ca vừa khai đóng lượt','bản ghi thiếu tên ca',
               'bản ghi đóng lượt thiếu rc kiểu int','kênh KHÔNG có bản ghi ca nào']
    variants=[(str(i),remove_guard(before,f)) for i,f in enumerate(fragments)]
    variants.append(('6',mutate(before,'    except Exception as exc:                  # noqa: BLE001 — fail-close CÓ CHỦ ĐÍCH',
                                     '    except KeyError as exc:  # reviewer mutation')))
    def worker(pair):
        label,source=pair; rcs=[]
        for ca in ('t161','t162','t163'):
            r,_=run_case(source,ca,'seven-before-'+label+'-'+ca); rcs.append(r.returncode)
        return {'guard':label,'rcs':rcs}
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows=list(pool.map(worker,variants))
    print('SEVEN_BEFORE',rows,flush=True)
    (OUT/'seven-before.json').write_text(json.dumps(rows,indent=2))

def a2_reverse():
    changed=mutate(SOURCE,'        ct = r.get("chi_tiet", "")',
                   '        ct = r.get("chi_tiet", "")\n        if not ct:\n            return KHONG_DO_DUOC, "reviewer: reader depends on detail"')
    run_case(changed,'t163','a2-reverse')

def control_attempt_counts():
    allrows=[]
    for item in M.DOT_BIEN_TU_KIEM_512:
        if item[3]!='DO': continue
        source=SOURCE
        for old,new in item[2]: source=mutate(source,old,new)
        mod=module(source)
        row={'item':item[0]}
        for label,controls in [('selected',[x for x in mod._muc_control_512() if x[0]==item[1]]),
                               ('frozen10',mod.CONTROL_512),('all12',mod._muc_control_512())]:
            with mock.patch.object(mod.subprocess,'run',wraps=mod.subprocess.run) as calls:
                for c in controls: mod._chay_mot_mutant_512(*c[:4],source)
            row[label]=calls.call_count
        print(row,flush=True); allrows.append(row)
    print('SUMS',{k:sum(r[k] for r in allrows) for k in ('selected','frozen10','all12')},flush=True)
    (OUT/'control-attempt-counts.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2))

def first_oracle():
    changed=mutate(SOURCE,'            elif phan_hang != [kenh_mong]:',
                   '            elif phan_hang != [GIET]:')
    run_case(changed,'t163','first-oracle-all-giet')

if __name__ == '__main__':
    globals()[sys.argv[1]]()
