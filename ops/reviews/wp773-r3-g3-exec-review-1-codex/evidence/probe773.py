import importlib.util, re, contextlib, io, json, time
from pathlib import Path
s=importlib.util.spec_from_file_location('reg','/tmp/review773/.claude/dev/ci_dang_ky_test.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
p='ops/land_evidence_nguon_test.py'; m=r.MOI[p]
good='CA: 14/14 dat\nDOT BIEN: 37/37 bi giet dung ly do\nTU KIEM PHAN HANG: DAT (2 dot bien)\nTONG: DAT\n'
cases={'good':good,'TONG_DO':good.replace('TONG: DAT','TONG: DO'),'CA_13_14':good.replace('14/14','13/14'),'DB_0_0':good.replace('37/37','0/0'),'missing_DB':good.replace('DOT BIEN: 37/37 bi giet dung ly do\n',''),'reordered':good.replace('CA: 14/14 dat\n','')+'CA: 14/14 dat\n','CA_0_0':good.replace('14/14','0/0'),'NHE':good.replace('37/37 bi giet dung ly do','37 muc CHE DO NHE'),'CRLF':good.replace('\n','\r\n'),'CI_prefix':''.join('LOG '+x+'\n' for x in good.splitlines()),'DB_36_37':good.replace('37/37','36/37'),'extra_error':good+'TONG: DO\n','DO_then_DAT':good.replace('TONG: DAT','TONG: DO\nTONG: DAT'),'selfcheck_DO':good.replace('PHAN HANG: DAT','PHAN HANG: DO'),'extra_line':good.replace('DOT BIEN:', 'unrelated\nDOT BIEN:')}
print('groups',re.compile(m,re.M).groups)
for n,out in cases.items():
    with contextlib.redirect_stdout(io.StringIO()) as b:
        rc=r.chay_moi(moi={p:m},cach_ly={},chay_mot=lambda _: (0,out),so_worker=1)
    print(n, 'bang_chung_xanh=',r.bang_chung_xanh(out,m),'chay_moi_rc=',rc)
print('groups_real',re.search(m,good,re.M).groups())
print('plan_present',p in r.ke_hoach(set()),'NHE',p in r.NHE,'env',r.env_theo_che_do(p,r.CHE_DO_NHE))
for kind,pat in [('removed',None),('wrong_path',m),('wrong_pattern','NEVER_MATCH'),('permissive_pattern','.*')]:
    if kind in ('removed','wrong_path'):
        reg=set(r.DANG_KY)-{p}
        if kind=='wrong_path':reg.add('ops/land_evidence_nguon_typo_test.py')
        print('mutation',kind,r.kiem(registry=reg)[0])
    else:
        print('mutation',kind,'kiem_errors=',r.kiem()[0], 'evidence_good=',r.bang_chung_xanh(good,pat),'evidence_bad=',r.bang_chung_xanh(cases['TONG_DO'],pat))
start=time.monotonic()
with contextlib.redirect_stdout(io.StringIO()) as b:
    rc=r.chay_moi(moi={p:m},cach_ly={},so_worker=2)
print('REAL_CHAY_MOI',rc,'seconds',round(time.monotonic()-start,2));print(b.getvalue())
