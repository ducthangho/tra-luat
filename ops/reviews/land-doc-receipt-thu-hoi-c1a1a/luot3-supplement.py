import contextlib
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path(sys.argv[1]).resolve()
OUT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('audit',OUT/'audit.py')
A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
T=A.T

def cli_laws():
    for n in range(1,6):
        old='    print(json.dumps(kq, '
        cond=f'kq["luat"]["K{n}"] == "do"'+(' and kq["luat"]["K1"] == "qua"' if n>1 else '')
        new=f'    if {cond}:\n        kq = {{"ok": True, "luat": dict.fromkeys(kq["luat"], "qua"), "ly_do": []}}\n'+old
        p=OUT/f'isolated_cli_K{n}.py';p.write_text(A.edit(old,new));m=A.load(p,'iso')
        A.emit(kind='isolated_cli',id=f'M1z.K{n}',baseline=A.target(A.M,A.DEV/'doc_receipt_thu_hoi.py','cli'),target=A.target(m,p,'cli'))

def registry():
    c=A.load(A.DEV/'ci_dang_ky_test.py','registry')
    path='.claude/dev/doc_receipt_thu_hoi_test.py';mau=c.MOI[path]
    for ca,db in [('3/3','2/2'),('3/4','2/2'),('3/3','1/2'),('3/4','1/2'),('0/0','2/2'),('3/3','0/0'),('0/0','0/0')]:
        line=f'doc_receipt_thu_hoi tests: {ca} ca QUA · {db} dot bien GIET\n'
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf): rc=c.chay_moi(moi={path:mau},cach_ly={},chay_mot=lambda _: (0,line),doc_moi_truong=lambda:None,doc_trong_ci=lambda:False,doc_nen_windows=lambda:False)
        A.emit(kind='registry_consumer',ca=ca,db=db,rc=rc,output=buf.getvalue())
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):rc=c.chay_moi(moi={path:mau},cach_ly={})
    A.emit(kind='registry_actual_suite',rc=rc,output=buf.getvalue())
    d=OUT/'registry_missing';d.mkdir(exist_ok=True)
    source=(A.DEV/'ci_dang_ky_test.py').read_text()
    line=next(x for x in source.splitlines(True) if path in x and x.lstrip().startswith('"'+path+'"'))
    (d/'ci_dang_ky_test.py').write_text(source.replace(line,''))
    t=A.load(A.DEV/'doc_receipt_thu_hoi_test.py','reg_t');t.GOC=d
    try:t.ca_dang_ky('dang_ky');result='pass'
    except Exception as e:result=type(e).__name__+': '+str(e)
    A.emit(kind='registry_remove_registration',result=result)

def ruff():
    rows=[]
    for ref in ('HEAD','origin/master'):
        src=subprocess.check_output(['git','show',ref+':scripts/tl.py'],cwd=ROOT)
        cmd=[sys.executable,'-m','ruff','check','--no-cache','--select','F','--output-format','json','--stdin-filename',str(ROOT/'scripts/tl.py'),'-']
        r=subprocess.run(cmd,input=src,capture_output=True)
        (OUT/('ruff-tl-'+ref.replace('/','-')+'.json')).write_bytes(r.stdout)
        rows.append(json.loads(r.stdout));A.emit(kind='ruff_tl',ref=ref,command=cmd,rc=r.returncode,count=len(rows[-1]),codes=[x['code'] for x in rows[-1]])
    A.emit(kind='ruff_delta',equal=rows[0]==rows[1],delta=len(rows[0])-len(rows[1]))

def extra():
    # This uses no network and spawns only the same Python interpreter running pass.
    old='    luat, ly_do = {}, []'
    src=A.edit(old,old+'\n    if raw == b"{":\n        _os = __import__("os")\n        _pid = _os.posix_spawn(sys.executable, [sys.executable, "-c", "pass"], _os.environ)\n        _os.waitpid(_pid, 0)')
    m,p=A.suite('pure_posix_spawn',src)
    events=[];original=os.posix_spawn
    def record(*a,**kw):events.append(a[1]);return original(*a,**kw)
    os.posix_spawn=record
    try:result=A.target(m,p,'tinh')
    finally:os.posix_spawn=original
    A.emit(kind='process_probe',oracle=result,spawn_calls=events)
    # Debt inherited from the round-2 audit; K4 message semantics has no dimension in the closed catalog.
    A.suite('debt_stale_message',A.edit('stale, chay lai','fresh, khong can chay lai'),T.ma(T.FIX).replace(T.S.encode(),T.X40.encode()))
if __name__=='__main__':globals()[sys.argv[2]]()
