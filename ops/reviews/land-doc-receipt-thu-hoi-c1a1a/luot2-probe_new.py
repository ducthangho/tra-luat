"""Reviewer r2 probes; all mutations and outputs remain beside this file."""
import contextlib
import importlib.util
import io
import json
import pathlib
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
DEV = ROOT / '.claude/dev'
SRC = (DEV / 'doc_receipt_thu_hoi.py').read_text()

def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m

T = load(DEV/'doc_receipt_thu_hoi_test.py', 'test_new')
M = load(DEV/'doc_receipt_thu_hoi.py', 'baseline_new')

def emit(**x): print(json.dumps(x, ensure_ascii=False), flush=True)
def edit(old,new):
    assert SRC.count(old)==1, (old,SRC.count(old))
    return SRC.replace(old,new)
def call(m, changes=None, raw=None, **kw):
    params=dict(kho=T.KHO,nhanh='master',base_hien_hanh=T.S,head_hien_hanh=T.H);params.update(kw)
    try: return m.kiem_json(T.ma({**T.FIX,**(changes or {})}) if raw is None else raw, **params)
    except Exception as e: return {'exception':type(e).__name__,'detail':str(e)}

def suite(name, source, changes=None, raw=None, params=None):
    folder=OUT/name/'.claude/dev';folder.mkdir(parents=True,exist_ok=True)
    path=folder/'doc_receipt_thu_hoi.py';path.write_text(source)
    for f in ('doc_receipt_thu_hoi_test.py','ci_dang_ky_test.py'): (folder/f).write_bytes((DEV/f).read_bytes())
    cmd=[sys.executable,'-B',str(folder/'doc_receipt_thu_hoi_test.py')]
    p=subprocess.run(cmd,capture_output=True,text=True)
    (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
    m=load(path,name)
    emit(kind='suite', name=name,command=cmd,rc=p.returncode,output=p.stdout.strip(),stderr=p.stderr[-1000:],baseline=call(M,changes,raw,**(params or {})),mutant=call(m,changes,raw,**(params or {})))
    return m,path

def cli(path,changes=None,params=None):
    receipt=OUT/'probe_input.json';receipt.write_bytes(T.ma({**T.FIX,**(changes or {})}))
    opts={'--receipt':str(receipt),'--kho':T.KHO,'--nhanh-mac-dinh':'master','--base-hien-hanh':T.S,'--head-hien-hanh':T.H}
    opts.update(params or {})
    p=subprocess.run([sys.executable,'-B',str(path),'kiem-json',*[x for kv in opts.items() for x in kv]],capture_output=True,text=True)
    emit(kind='cli',path=str(path),rc=p.returncode,stdout=p.stdout,stderr=p.stderr[-400:])

def credit():
    by={r[0]:r for r in T.DB}
    samples=[('M2d','if type(r) is list:\n            type(r["schema_version"]) is int'),
             ("M2e'",'if type(r) is dict:\n            [KIEU[k](r[k]) for k in ["tree_S"]]'),
             ("M2b'",'raw.decode("utf-8", "strict")')]
    for ident,code in samples:
        r=by[ident];row=(*r[:2],'unrelated_'+ident.replace("'",'p'),'    if loi:\n','    if loi:\n        '+code+'\n',r[5],r[6])
        path=OUT/('credit_'+ident.replace("'",'p')+'.py');path.write_text(edit(row[3],row[4]));m=load(path,'credit')
        try:T.chay_ca(m,path,{r[5]});trace='no failure'
        except T.TinHieuChotCa as e:trace=str(e)
        emit(kind='credit',id=ident,row=row,baseline_green=call(m)['ok'],original_guard_preserved=r[3] in path.read_text(),target_failure=trace,disposition=T.chay_dot_bien(SRC,row))
    for ident in ['M1o','M3w','M3x','M3y']:
        r=by[ident];path=OUT/('positive_'+ident+'.py');path.write_text(edit(r[3],r[4]));m=load(path,'positive')
        try:T.chay_ca(m,path,{'duong_fixture'});trace='pass'
        except T.TinHieuChotCa as e:trace=str(e)
        emit(kind='A1',id=ident,fixture=call(m),target=trace,disposition=T.chay_dot_bien(SRC,r))
    row=('NOISE','control','noise_positive','    luat, ly_do = {}, []','    raise RuntimeError("unrelated")\n    luat, ly_do = {}, []','duong_fixture','RuntimeError|raise RuntimeError')
    emit(kind='A1-control',row=row,disposition=T.chay_dot_bien(SRC,row))

def mutants():
    m,p=suite('cli_ok_int',edit('    print(json.dumps(kq,','    kq["ok"] = int(kq["ok"])\n    print(json.dumps(kq,'))
    cli(p);cli(p,params={'--head-hien-hanh':T.X40})
    suite('timestamp_width',edit('def _khop(mau):','def _khop(mau):\n    mau = mau.replace(r"\\d\\d", r"\\d+")'),{'thoi_diem_utc':'2026-9-25T1:2:3Z'})
    suite('timestamp_digit',edit('def _khop(mau):','def _khop(mau):\n    mau = mau.replace(r"\\d\\d", "..")'),{'thoi_diem_utc':'2026-aa-25T01:25:14Z'})
    suite('timestamp_year_long',edit('def _khop(mau):','def _khop(mau):\n    mau = mau.replace(r"\\d{4}", r"\\d{4,5}")'),{'thoi_diem_utc':'20266-09-25T01:25:14Z'})
    suite('k1_reason_false',edit('        ly_do.extend(f"{k}: {x}" for x in loi)',
        '        ly_do.extend(f"{k}: {x}" for x in loi)\n        ly_do[:] = [x.replace("K1 do", "K1 qua") for x in ly_do]'),raw=b'{')
    suite('purity_dynamic',edit('    luat, ly_do = {}, []',
        '    __import__("subprocess").run([sys.executable, "-c", "pass"], check=True)\n    luat, ly_do = {}, []'))
    suite('purity_state',edit('    luat, ly_do = {}, []',
        '    sys._receipt650_probe_count = getattr(sys, "_receipt650_probe_count", 0) + 1\n    luat, ly_do = {}, []'))
    emit(kind='purity_state',side_effect=getattr(sys,'_receipt650_probe_count',None))
    suite('str_normalize_after_decode',edit('            # nhận `str`,',
        '            chuoi = chuoi.strip()\n            # nhận `str`,'))
    # Passing byte content through a one-time byte normalization erases the Raw subclass.
    suite('spy_bypass_setup',edit('    loi, r = [], _VANG','    raw = bytes(raw)\n    loi, r = [], _VANG'))

def td():
    for r in T.DB+T._theo_truong():
        if not r[5].startswith('TD:'):continue
        path=OUT/(r[0]+'.py');path.write_text(edit(r[3],r[4]));m=load(path,'td')
        extra=[]
        if r[0]=='M3.schema_version':
            for v in [True,1.0,2,None]: extra.append([v,call(m,{'schema_version':v})])
        if r[0].startswith('M3.') and r[0][3:] in T.C3:
            for v in [None,7,T.S[:39]]:
                extra.append(['single',v,call(m,{r[0][3:]:v})]);extra.append(['group',v,call(m,dict.fromkeys(T.C3,v))])
        if r[0] in ['M1j','M1k']:cli(path,params={'--base-hien-hanh' if r[0]=='M1j' else '--head-hien-hanh':''})
        emit(kind='td',id=r[0],reason=r[5],disposition=T.chay_dot_bien(SRC,r),extra=extra)
    r=next(r for r in T.DB if r[0]=='M2a');path=OUT/'M2a.py';path.write_text(edit(r[3],r[4]));m=load(path,'m2a')
    try:T.chay_ca(m,path,{'bom'});bom='pass'
    except T.TinHieuChotCa as e:bom=str(e)
    try:T.chay_ca(m,path,{'thu_tu_k1'});order='pass'
    except T.TinHieuChotCa as e:order=str(e)
    emit(kind='M2a',bom_case=bom,order_case=order,disposition=T.chay_dot_bien(SRC,r))

def oracle():
    old=json.loads
    T.ca_thu_tu('thu_tu_k1',M)
    emit(kind='spy-restored-success',restored=json.loads is old)
    r=next(r for r in T.DB if r[0]=='M2h');path=OUT/'spy_failure.py';path.write_text(edit(r[3],r[4]));m=load(path,'spy_failure')
    try:T.ca_thu_tu('thu_tu_k1',m)
    except T.TinHieuChotCa as e:emit(kind='spy-restored-failure',restored=json.loads is old,message=str(e))
    # Alias captured during import bypasses the m.json.loads spy but remains valid M2 code.
    path=OUT/'parser_alias.py';path.write_text(edit('import re','parse_json = json.loads\nimport re').replace('r = json.loads(chuoi)','r = parse_json(chuoi)'));m=load(path,'parser_alias')
    try:T.ca_thu_tu('thu_tu_k1',m);out='pass'
    except T.TinHieuChotCa as e:out=str(e)
    emit(kind='spy-alias-control',result=call(m),oracle=out,restored=json.loads is old)
    # Verify parser identity oracle on input carrying leading whitespace absent from FIX encoding.
    path=OUT/'normalize.py';path.write_text(edit('            # nhận `str`,','            chuoi = chuoi.strip()\n            # nhận `str`,'));m=load(path,'normalize')
    events=[];decoded=[]
    class Raw(bytes):
        def decode(self,*a,**kw):
            v=super().decode(*a,**kw);decoded.append(v);return v
    def loads(v,*a,**kw):
        events.append({'same_identity':v is decoded[-1], 'same_value':v==decoded[-1]});return old(v,*a,**kw)
    m.json.loads=loads
    try: result=call(m,raw=Raw(b' '+T.ma(T.FIX)+b'\n'))
    finally:m.json.loads=old
    emit(kind='str-normalize',trace=events,result=result)

def followup():
    suite('k1_reason_wrong_semantic',edit('        luat[k] = "do" if loi else "qua"',
        '        luat[k] = "do" if loi else "qua"\n        loi = ["K1 qua" if x == "K1 do" else x for x in loi]'),raw=b'{')
    # CLI parity tests supply only unchanged JSON with a mismatching caller, never a changed receipt.
    m,p=suite('cli_ignores_k5',edit('    print(json.dumps(kq,',
        '    if kq["luat"]["K5"] == "do":\n        kq = {"ok": True, "luat": dict.fromkeys(kq["luat"], "qua"), "ly_do": []}\n    print(json.dumps(kq,'))
    cli(p,changes={'ket_luan':[]})
    # Machine-readable record for a real unhandled parser error, with an int allowed by M3.
    raw=T.ma(T.FIX).replace(b'36081907282',b'1'*4500)
    receipt=OUT/'bigint.json';receipt.write_bytes(raw)
    cmd=[sys.executable,'-B',str(DEV/'doc_receipt_thu_hoi.py'),'kiem-json','--receipt',str(receipt),'--kho',T.KHO,'--nhanh-mac-dinh','master','--base-hien-hanh',T.S,'--head-hien-hanh',T.H]
    p=subprocess.run(cmd,capture_output=True,text=True)
    emit(kind='actual-bigint',bytes=len(raw),api=call(M,raw=raw),command=cmd,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
    # Independent parser run with the interpreter's limit disabled only in this probe process.
    previous=sys.get_int_max_str_digits()
    try:
        sys.set_int_max_str_digits(0)
        parsed=json.loads(raw)
        emit(kind='bigint-valid-json',keys=len(parsed),type_run_id=type(parsed['run_id']).__name__,only_changed=[k for k in parsed if parsed[k]!=T.FIX[k]],result=call(M,raw=raw))
    finally:sys.set_int_max_str_digits(previous)
    # Show that the forbidden process actually runs, without starting a process during this measurement.
    m=load(OUT/'purity_dynamic/.claude/dev/doc_receipt_thu_hoi.py','pure_measure')
    old=subprocess.run;calls=[]
    subprocess.run=lambda *a,**kw:calls.append((a,kw))
    try:result=call(m)
    finally:subprocess.run=old
    emit(kind='purity-spawn',calls=calls,result=result)

if __name__=='__main__':globals()[sys.argv[2]]()
