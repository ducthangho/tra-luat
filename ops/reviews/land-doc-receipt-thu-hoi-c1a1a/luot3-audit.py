import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
sys.dont_write_bytecode = True
ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
DEV = ROOT / '.claude/dev'
SRC = (DEV / 'doc_receipt_thu_hoi.py').read_text()
def load(p, n):
    spec = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
T = load(DEV/'doc_receipt_thu_hoi_test.py','audit_test')
M = load(DEV/'doc_receipt_thu_hoi.py','audit_module')
def emit(**d): print(json.dumps(d, ensure_ascii=False), flush=True)
def edit(old, new):
    assert SRC.count(old)==1, (old,SRC.count(old))
    return SRC.replace(old,new)
def call(m, raw):
    return m.kiem_json(raw,kho=T.KHO,nhanh='master',base_hien_hanh=T.S,head_hien_hanh=T.H)
def target(m,p,name):
    try: T.chay_ca(m,p,{name}); return 'pass'
    except Exception as e: return type(e).__name__+': '+str(e)
def suite(name,source,raw=None):
    d=OUT/name/'.claude/dev';d.mkdir(parents=True,exist_ok=True)
    p=d/'doc_receipt_thu_hoi.py';p.write_text(source)
    for f in ('doc_receipt_thu_hoi_test.py','ci_dang_ky_test.py'):(d/f).write_bytes((DEV/f).read_bytes())
    cmd=[sys.executable,'-B',str(d/'doc_receipt_thu_hoi_test.py')]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
    (OUT/(name+'.log')).write_text(r.stdout+r.stderr)
    m=load(p,name)
    emit(kind='suite',name=name,command=cmd,rc=r.returncode,output=r.stdout,stderr=r.stderr)
    if raw is not None: emit(kind='behavior',name=name,baseline=call(M,raw),mutant=call(m,raw))
    return m,p

def census():
    rows=T.DB+T._theo_truong()
    emit(kind='counts',CA=len(T.CA),DB=len(T.DB),fields=len(T._theo_truong()),total=len(rows),unique=len({r[0] for r in rows}),GIO=len(T.GIO))
    real=json.loads((ROOT.parent/'receipt589_for_review.json').read_bytes())
    emit(kind='fixture',equal=real==T.FIX,keys=len(real),types_equal=all(type(real[k]) is type(T.FIX[k]) for k in real))
    for r in rows:
        disp=T.chay_dot_bien(SRC,r)
        # Measure target separately: positive baselines and exact failure, not just aggregate count.
        baseline='TD' if r[5].startswith('TD:') else target(M,DEV/'doc_receipt_thu_hoi.py',r[5])
        failure='registry' if r[5]=='dang_ky' else None
        if not r[5].startswith('TD:') and r[5]!='dang_ky':
            p=OUT/'census_mutant.py';p.write_text(edit(r[3],r[4]));m=load(p,'census_mutant')
            failure=target(m,p,r[5])
        emit(kind='row',id=r[0],description=r[1],case=r[5],a1=r[7] if len(r)>7 else 'duong_fixture',baseline=baseline,target=failure,disposition=disp)

def attacks():
    # No path escapes. All writes are to a literal, owned scratch file.
    old='    luat, ly_do = {}, []'
    experiments=[
      ('pure_sys_list', edit(old,old+'\n    sys.path.append("c1a1a-review-probe")')),
      ('pure_module_list',edit(old,old+'\n    _REVIEW_LOG.append(len(raw))').replace('BOM = b','_REVIEW_LOG = []\nBOM = b')),
      ('pure_io_file',edit(old,old+'\n    with __import__("io").open("/tmp/review650-r3/purity-marker.txt", "w") as f:\n        f.write("side-effect")')),
    ]
    for name,src in experiments:
        m,p=suite(name,src)
        path_before=list(sys.path); content_before=list(getattr(m,'_REVIEW_LOG',[]))
        marker=OUT/'purity-marker.txt'
        if name=='pure_io_file':marker.write_text('before')
        state=target(m,p,'tinh')
        emit(kind='purity',name=name,oracle=state,sys_list_delta=len(sys.path)-len(path_before),module_list_before=content_before,module_list_after=getattr(m,'_REVIEW_LOG',None),file_after=marker.read_text() if marker.exists() else None)
        sys.path[:]=path_before
    # A matrix cell can be missing even when a generic oracle catches the behavior.
    for name,replacement in [('shape_k1_ok',T._TRA1.replace('"ok": False','"ok": 0')),
                              ('shape_k1_keys',T._TRA1.replace('"ly_do": ly_do}', '"ly_do": ly_do, "extra": 1}'))]:
        p=OUT/(name+'.py');p.write_text(edit(T._TRA1,replacement));m=load(p,name)
        emit(kind='missing_cell',name=name,baseline=target(M,DEV/'doc_receipt_thu_hoi.py','bom'),mutant=target(m,p,'bom'))
    # Declared hex64 fullmatch/str dimensions; preserve existing mutation anchors.
    suite('hex64_partial_match',edit('def _khop(mau):','def _khop(mau):\n    if mau == "[0-9a-f]{64}":\n        return lambda v: type(v) is str and re.match(mau, v) is not None'),T.ma({**T.FIX,'workflow_definition_sha256':T.X64+'x'}))
    suite('hex64_number_coerce',edit('def _khop(mau):','def _khop(mau):\n    if mau == "[0-9a-f]{64}":\n        return lambda v: re.fullmatch(mau, str(v)) is not None'),T.ma({**T.FIX,'workflow_definition_sha256':int('1'*64)}))

def classifier():
    by={r[0]:r for r in T.DB}
    for id in ('M1o2','M1u2','M1w3','M1x2'):
        r=by[id];p=OUT/(id+'.py');p.write_text(edit(r[3],r[4]));m=load(p,id)
        controls={c[0]:target(m,p,c[0]) for c in T.CA if not c[2]}
        emit(kind='a1_none',id=id,disposition=T.chay_dot_bien(SRC,r),positive_count=len(controls),positive_pass=sum(v=='pass' for v in controls.values()),controls=controls)
    for id in ('M3w','M3x','M3y'):
        r=by[id];p=OUT/(id+'.py');p.write_text(edit(r[3],r[4]));m=load(p,id)
        emit(kind='a1_control',id=id,guard=target(m,p,r[7]),target=target(m,p,r[5]),disposition=T.chay_dot_bien(SRC,r))
    r=by['M2b3'];src=edit(r[3],r[4])
    # Chosen exception must remain specific to its unique source line.
    for name,source,row in [
      ('correct',SRC,r),
      ('wrong_type',SRC,(*r[:6],('TypeError',r[6][1]))),
      ('wrong_line',SRC,(*r[:6],(r[6][0],'r = json.loads(chuoi)'))),
      ('duplicate_line',SRC+'\ndef unreachable(raw):\n    '+r[6][1]+'\n',r),
    ]:emit(kind='exception_control',name=name,disposition=T.chay_dot_bien(source,row))
    # A wrong guard name silently passes; demonstrate as a classifier limitation on its declared A1 axis.
    r=by['M1o2']
    for guard in ('duong_fixture','not_a_case','bom'):
        emit(kind='a1_guard_validation',guard=guard,disposition=T.chay_dot_bien(SRC,(*r[:7],guard)))
    # Construct a scoped mutant retaining a separate positive control, without changing product/test files.
    old=T._TRA
    new=old.replace('"ok": all(v == "qua" for v in luat.values())','"ok": (1 if r["checkout_commit"] == SCOPE_S and all(v == "qua" for v in luat.values()) else all(v == "qua" for v in luat.values()))')
    row=('CONTROL','scoped green output','scoped_green',old,new,'duong_fixture',None,'duong_c_khac_s')
    emit(kind='a1_scoped_alternative',disposition=T.chay_dot_bien(SRC+'\nSCOPE_S = '+repr(T.S)+'\n',row))

def runtime():
    raw=T.ma(T.FIX)
    samples={'empty':b'', 'bom_only':b'\xef\xbb\xbf','utf8_bad':b'\xff','whitespace':b' \n\t','null':b'null','scalar_string':b'"x"','nan':b'NaN','infinity':b'Infinity','negative_inf':b'-Infinity',
    'trailing':raw+b'{}','lone_surrogate':raw.replace(b'KHONG_CHAY',b'\\ud800'), 'bigint_4300':T._SO(4300),'bigint_4301':T._SO(4301),'bigint_4500':T._SO(4500),
    'array1000':b'['*1000+b']'*1000,'object1000':b'{"a":'*1000+b'0'+b'}'*1000}
    values=[None,True,False,0,-1,1.5,'',[],{},[[]],{'a':[1,2]},'\ud800',float('inf'),float('nan')]
    api_total=0;errors=[]
    for k in T.FIX:
        for val in values:
            v=json.dumps({**T.FIX,k:val},ensure_ascii=True).encode();api_total+=1
            try:
                q=call(M,v)
                assert type(q) is dict and type(q['ok']) is bool and set(q)=={'ok','luat','ly_do'}
            except Exception as e:errors.append([k,repr(val),type(e).__name__,str(e)])
    # Compare nested non-scalar C values just below and across the parser recursion boundary.
    for n in range(950,1010):
        nested=b'['*n+b'0'+b']'*n
        v=raw
        for k in T.C3:v=v.replace(('"'+k+'": "'+T.S+'"').encode(),('"'+k+'": ').encode()+nested)
        try:q=call(M,v)
        except Exception as e:errors.append(['C-depth',n,type(e).__name__,str(e)]);samples['C-depth-'+str(n)]=v
        api_total+=1
    emit(kind='runtime_fuzz',total=api_total,errors=errors)
    for name,v in samples.items():
        try: q=call(M,v); api={'result':q}
        except Exception as e:api={'exception':type(e).__name__,'message':str(e)}
        try:json.loads(v);parser='parsed'
        except Exception as e:parser=type(e).__name__
        f=OUT/'runtime.json';f.write_bytes(v)
        cmd=[sys.executable,'-B',str(DEV/'doc_receipt_thu_hoi.py'),'kiem-json','--receipt',str(f),'--kho',T.KHO,'--nhanh-mac-dinh','master','--base-hien-hanh',T.S,'--head-hien-hanh',T.H]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
        emit(kind='runtime',name=name,size=len(v),parser=parser,api=api,command=cmd,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
if __name__=='__main__':globals()[sys.argv[2]]()
