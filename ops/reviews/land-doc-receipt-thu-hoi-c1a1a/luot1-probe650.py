#!/usr/bin/env python3
"""Phản chứng reviewer #650. Chỉ ghi bản sao và log bên ngoài checkout."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
DEV = ROOT / '.claude/dev'
SOURCE = (DEV / 'doc_receipt_thu_hoi.py').read_text()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


T = load(DEV / 'doc_receipt_thu_hoi_test.py', 'test650')
M = load(DEV / 'doc_receipt_thu_hoi.py', 'module650')


def emit(kind, **data):
    print(json.dumps(dict(kind=kind, **data), ensure_ascii=False), flush=True)


def call(module, changes=None, raw=None, **params):
    args = dict(kho=T.KHO, nhanh='master', base_hien_hanh=T.S, head_hien_hanh=T.H)
    args.update(params)
    try:
        return module.kiem_json(T.ma({**T.FIX, **(changes or {})}) if raw is None else raw, **args)
    except Exception as exc:
        return dict(exception=type(exc).__name__, detail=str(exc))


def replace(source, old, new):
    assert source.count(old) == 1, (old, source.count(old))
    return source.replace(old, new)


def suite(name, source, changes=None, params=None):
    folder = OUT / name / '.claude/dev'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'doc_receipt_thu_hoi.py'
    path.write_text(source)
    for filename in ('doc_receipt_thu_hoi_test.py', 'ci_dang_ky_test.py'):
        (folder / filename).write_bytes((DEV / filename).read_bytes())
    p = subprocess.run([sys.executable, '-B', str(folder / 'doc_receipt_thu_hoi_test.py')], capture_output=True, text=True)
    (OUT / (name + '.log')).write_text(p.stdout + p.stderr)
    module = load(path, name)
    emit('mutant', name=name, rc=p.returncode, output=p.stdout.strip(), stderr=p.stderr[-500:],
         baseline=call(M, changes, **(params or {})), mutant=call(module, changes, **(params or {})),
         file=str(path))


def actual():
    receipt = json.loads((ROOT.parent / 'receipt589_for_review.json').read_bytes())
    emit('fixture', equal=receipt == T.FIX, keys=len(receipt), field_diffs=[k for k in receipt if receipt[k] != T.FIX.get(k)],
         type_diffs=[k for k in receipt if type(receipt[k]) is not type(T.FIX.get(k))],
         keys_match=set(receipt) == M.KHOA, obligations=len(T.DB + T._theo_truong()))
    for value in ([], {}, ['TAP_THU_HOI_RONG'], 1, None):
        emit('actual-ket-luan', value=value, result=call(M, dict(ket_luan=value)))
    invalid = OUT / 'ket_luan_list.json'
    invalid.write_bytes(T.ma({**T.FIX, 'ket_luan': []}))
    cmd = [sys.executable, '-B', str(DEV/'doc_receipt_thu_hoi.py'), 'kiem-json', '--receipt', str(invalid),
           '--kho', T.KHO, '--nhanh-mac-dinh', 'master', '--base-hien-hanh', T.S, '--head-hien-hanh', T.H]
    p = subprocess.run(cmd, capture_output=True, text=True)
    emit('actual-cli', command=cmd, rc=p.returncode, stdout=p.stdout, stderr=p.stderr)
    for c in T.CA:
        if c[0].startswith('utf'):
            text = c[1].decode('utf-8', 'strict')
            try: json.loads(text); outcome = 'accepted'
            except json.JSONDecodeError: outcome = 'JSONDecodeError'
            emit('utf-parser', name=c[0], decode='passed', str_parser=outcome, bytes_parser_equal=json.loads(c[1]) == T.FIX)
    emit('obligations', rows=[dict(id=r[0], clause=r[1], target=r[5], allowed_exception=r[6]) for r in T.DB+T._theo_truong()])


def mutants():
    # Mỗi mutant bảo toàn các mỏ neo DB, để chạy được CẢ suite và bộ tự đột biến.
    suite('hex_charset', replace(SOURCE, 'def _khop(mau):', 'def _khop(mau):\n    mau = mau.replace("[0-9a-f]", "[0-9a-z]")'), {'T': 'g'*40})
    suite('hex_string_guard', replace(SOURCE, 'type(v) is str and re.fullmatch', 're.fullmatch'), {'T': 123})
    suite('int_float', replace(SOURCE, 'lambda v: type(v) is int for k', 'lambda v: type(v) is int or type(v) is float for k'), {'run_id': 1.5})
    suite('hex64_length', replace(SOURCE, 'def _khop(mau):', 'def _khop(mau):\n    mau = mau.replace("{64}", "{64,65}")'), {'workflow_definition_sha256': 'a'*65})
    suite('timestamp_z', replace(SOURCE, ':[0-9]{2}Z")', ':[0-9]{2}[ZX]")'), {'thoi_diem_utc': '2026-09-25T01:25:14X'})
    suite('bom_decode_order', replace(SOURCE, '    loi, r = [], _VANG', '    try:\n        raw.decode("utf-8", "strict")\n    except UnicodeDecodeError:\n        pass\n    loi, r = [], _VANG'))
    suite('ok_not_bool', replace(SOURCE, '"ok": all(v == "qua" for v in luat.values())', '"ok": int(all(v == "qua" for v in luat.values()))'))
    suite('cli_dict_lost', replace(SOURCE, 'json.dumps(kq, ensure_ascii=True', 'json.dumps({"ok": kq["ok"]}, ensure_ascii=True'))


def credit():
    byid = {r[0]: r for r in T.DB}
    # Đột biến vô can: giữ nguyên chốt cần đo, chỉ làm hỏng ghi chẩn đoán ở K1 đỏ.
    for ident, exc in [('M2d', 'TypeError'), ("M2e'", 'KeyError'), ("M2b'", 'UnicodeDecodeError')]:
        base = byid[ident]
        expression = {'TypeError': 'len(0)', 'KeyError': '{}["unrelated"]',
                      'UnicodeDecodeError': 'b"\\x80".decode("utf-8")'}[exc]
        row = (base[0], base[1], 'noise_' + exc, '    if loi:\n', f'    if loi:\n        {expression}\n', base[5], base[6])
        emit('credit', id=ident, row=row, result=T.chay_dot_bien(SOURCE, row))
    row = ('noise-other-type', 'control', 'noise_ValueError', '    if loi:\n', '    if loi:\n        int("x")\n', 'goc_list_38_khoa', 'TypeError')
    emit('credit-control-other-type', result=T.chay_dot_bien(SOURCE, row))
    row = ('positive-red', 'control', 'positive_red', '    luat, ly_do = {}, []', '    raise RuntimeError("noise")\n    luat, ly_do = {}, []', 'goc_list_38_khoa', 'TypeError')
    emit('credit-control-positive-red', result=T.chay_dot_bien(SOURCE, row))
    row = ('positive-red-td', 'control', 'positive_red_td', '    luat, ly_do = {}, []', '    raise RuntimeError("noise")\n    luat, ly_do = {}, []', 'TD: test', None)
    emit('credit-control-positive-red-td', result=T.chay_dot_bien(SOURCE, row))


def registry():
    c = load(DEV/'ci_dang_ky_test.py', 'cdk650')
    path = '.claude/dev/doc_receipt_thu_hoi_test.py'
    mau = c.MOI[path]
    for a,b in [('3/3','2/2'), ('3/4','2/2'), ('3/3','1/2'), ('3/4','1/2'), ('0/0','0/0'), ('3/3','0/0')]:
        line = f'doc_receipt_thu_hoi tests: {a} ca QUA · {b} dot bien GIET\n'
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc=c.chay_moi(moi={path:mau}, cach_ly={}, chay_mot=lambda p:(0,line),
                         doc_moi_truong=lambda:None, doc_trong_ci=lambda:False, doc_nen_windows=lambda:False)
        emit('registry', a=a,b=b,rc=rc,output=buf.getvalue().strip())
    for old in (r'(\1)',r'(\3)'):
        try: T.ca_dang_ky('dang_ky',mau.replace(old,r'(\d+)')); outcome='survived'
        except T.TinHieuChotCa as e: outcome=str(e)
        emit('registry-mutant',old=old,result=outcome)
    # Cùng consumer thật với đúng một bộ mới, tránh chạy full CI bị cấm.
    p=subprocess.run([sys.executable,'-B',str(DEV/'doc_receipt_thu_hoi_test.py')],capture_output=True,text=True)
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc=c.chay_moi(moi={path:mau},cach_ly={},chay_mot=lambda _: (p.returncode,p.stdout),
                     doc_moi_truong=lambda:None,doc_trong_ci=lambda:False,doc_nen_windows=lambda:False)
    emit('registry-real-suite',rc=rc,output=buf.getvalue())
    errors, n, count = c.kiem(registry=c.DANG_KY - {path})
    emit('registry-remove', errors=errors, actual=n, registered=count)


def extra():
    suite('bom_order_v2', replace(SOURCE, '    loi, r = [], _VANG',
          "    try:\n        raw.decode(encoding='utf-8', errors='strict')\n    except (UnicodeDecodeError,):\n        pass\n    loi, r = [], _VANG"))
    suite('reasons_not_strings', replace(SOURCE, '        ly_do.extend(f"{k}: {x}" for x in loi)',
          '        ly_do.extend(f"{k}: {x}" for x in loi)\n        ly_do[:] = [0 for _ in ly_do]'), {'checker_rc': 1})
    # Đo thứ tự thực thi và số lần decode, không suy từ verdict K1.
    for name, path in [('baseline', DEV/'doc_receipt_thu_hoi.py'),
                       ('bom_order_v2',OUT/'bom_order_v2/.claude/dev/doc_receipt_thu_hoi.py')]:
        m=load(path,'trace_'+name)
        for with_bom in (False, True):
            events=[]
            class Raw(bytes):
                def __getitem__(self,key):
                    events.append('slice')
                    return super().__getitem__(key)
                def decode(self,*a,**kw):
                    events.append('decode')
                    return super().decode(*a,**kw)
            original_loads=m.json.loads
            def traced_loads(value,*a,**kw):
                events.append('parse:'+type(value).__name__)
                return original_loads(value,*a,**kw)
            raw=Raw((b'\xef\xbb\xbf' if with_bom else b'')+T.ma(T.FIX))
            m.json.loads=traced_loads
            try: result=call(m,raw=raw)
            finally: m.json.loads=original_loads
            emit('order',name=name,bom=with_bom,events=events,result=result)
    timestamp='٢026-09-25T01:25:14Z'
    emit('timestamp-spec',value=timestamp,spec_match=bool(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',timestamp)),
         result=call(M,{'thoi_diem_utc':timestamp}))
    cases=[]
    receipt=OUT/'positive.json'; receipt.write_bytes(T.ma(T.FIX))
    baseargs={'--receipt':str(receipt),'--kho':T.KHO,'--nhanh-mac-dinh':'master','--base-hien-hanh':T.S,'--head-hien-hanh':T.H}
    for option in ('--kho','--nhanh-mac-dinh','--base-hien-hanh','--head-hien-hanh'):
        cases.append((option,'',2))
    for option in ('--base-hien-hanh','--head-hien-hanh'):
        cases.extend((option,v,2) for v in ('a'*39,'a'*41,'A'*40,'g'*40))
    for option,val,want in cases:
        args={**baseargs,option:val}
        p=subprocess.run([sys.executable,'-B',str(DEV/'doc_receipt_thu_hoi.py'),'kiem-json',*[x for kv in args.items() for x in kv]],capture_output=True,text=True)
        emit('cli-args',option=option,value=val,rc=p.returncode,want=want)
    for ident in ['M1j','M1k']:
        row=next(r for r in T.DB if r[0]==ident)
        path=OUT/(ident+'.py'); path.write_text(replace(SOURCE,row[3],row[4]))
        option='--base-hien-hanh' if ident=='M1j' else '--head-hien-hanh'
        args={**baseargs,option:''}
        p=subprocess.run([sys.executable,'-B',str(path),'kiem-json',*[x for kv in args.items() for x in kv]],capture_output=True,text=True)
        emit('td-empty',id=ident,rc=p.returncode,stderr=p.stderr.splitlines()[-1])
    path=OUT/'cli_dict_lost/.claude/dev/doc_receipt_thu_hoi.py'
    p=subprocess.run([sys.executable,'-B',str(path),'kiem-json',*[x for kv in baseargs.items() for x in kv]],capture_output=True,text=True)
    emit('cli-dict-lost',rc=p.returncode,stdout=p.stdout)


def targeted():
    wanted=['M2c','M4g','M4h','M4i','M5a','M5b','M5c','M5d','M6a','M6b','M6c','M1e','M1f','M1g','M1h','M1i','M1l','M1m']
    for row in T.DB:
        if row[0] not in wanted: continue
        path=OUT/('target_'+row[0]+'.py'); path.write_text(replace(SOURCE,row[3],row[4]))
        m=load(path,'target_'+row[0])
        targets=['utf16-le','utf16-be','utf32-le','utf32-be'] if row[0]=='M2c' else [row[5]]
        for target in targets:
            try: T.chay_ca(m,path,{target}); outcome='SURVIVED'
            except T.TinHieuChotCa as exc: outcome=str(exc)
            emit('target',id=row[0],name=row[2],fixture_positive=call(m)['ok'],target=target,outcome=outcome)


def caller():
    suite('kho_fixed',replace(SOURCE,'    ghi("K3", [','    kho = "ducthangho/tra-luat"\n    ghi("K3", ['),
          {'repository':'other/repo','kho_canonical':'github.com/other/repo','workflow_ref':T.WFR.replace(T.KHO,'other/repo')},
          {'kho':'other/repo'})
    suite('nhanh_fixed',replace(SOURCE,'    ghi("K3", [','    nhanh = "master"\n    ghi("K3", ['),
          {'nhanh_mac_dinh':'main','workflow_ref':T.WFR[:-6]+'main'},{'nhanh':'main'})
    suite('hex_numeric_coerce',replace(SOURCE,'    return lambda v: type(v) is str and re.fullmatch(mau, v) is not None',
          '    def khop(v):\n        if type(v) is int:\n            v = str(v)\n        return type(v) is str and re.fullmatch(mau, v) is not None\n    return khop'),
          {'T':int('1'*40)})


MODES = dict(actual=actual, mutants=mutants, credit=credit, registry=registry,extra=extra,targeted=targeted,caller=caller)
if __name__ == '__main__':
    MODES[sys.argv[2]]()
