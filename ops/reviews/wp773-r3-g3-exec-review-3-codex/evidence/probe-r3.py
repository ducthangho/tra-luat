import importlib.util,pathlib,re,subprocess,sys,contextlib,io
R=pathlib.Path('/tmp/rv778-review')
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(R/'ops/land_evidence_nguon_test.py','t');g=load(R/'.claude/dev/ci_dang_ky_test.py','g')
name='c15_c11_tu_kiem_qua_dau_ra_gia'
print('c15 original',t.chay_ca(name))
src=(R/'ops/land_evidence_nguon_test.py').read_text()
for label,old,new in [('bound','and int(m.group(1)) <= n',''),('strict','<= n','< n'),('equal','<= n','== n'),('rc','rc == 0 and bool(m)','bool(m)'),('denominator','/{n} miễn trừ','/\\d+ miễn trừ'),('missing','bool(m) and int(m.group(1)) <= n','(not m or int(m.group(1)) <= n)')]:
 ns=dict(t.__dict__);exec(compile(src.replace(old,new),str(R/'ops/land_evidence_nguon_test.py'),'exec'),ns);print('mutant',label,ns['chay_ca'](name))
p='ops/land_evidence_nguon_test.py';pat=g.MOI[p]
a='CA: 15/15 dat\nDOT BIEN: 37/37 bi giet dung ly do\nTU KIEM PHAN HANG: DAT (2 dot bien)\nTONG: DAT\n'
print('groups',re.compile(pat).groups)
cases={'valid':a,'bad_total':a.replace('TONG: DAT','TONG: DO'),'partial':a.replace('15/15','13/14'),'zero_ca':a.replace('15/15','0/0'),'zero_mut':a.replace('37/37','0/0'),'survivor':a.replace('37/37','36/37'),'missing_mut':a.replace(a.splitlines(True)[1],''),'extra_end':a+'log\n','extra_middle':a.replace('DOT BIEN:','log\nDOT BIEN:'),'order':'\n'.join(reversed(a.splitlines())),'do_before':'TONG: DO\n'+a,'self_do':'TU KIEM PHAN HANG: DO\n'+a,'nhe':a.replace('37/37 bi giet dung ly do','37 muc CHE DO NHE'),'prefix':''.join('CI '+x+'\n' for x in a.splitlines()),'raw_crlf':a.replace('\n','\r\n'),'neutral_before':'log\n'+a}
for k,v in cases.items():
 with contextlib.redirect_stdout(io.StringIO()): rc=g.chay_moi(moi={p:pat},cach_ly={},chay_mot=lambda _: (0,v),doc_moi_truong=lambda: g.MOI_TRUONG_CI)
 print('regex',k,g.bang_chung_xanh(v,pat),'consumer',rc)
r=subprocess.run([sys.executable,'-c','import sys;sys.stdout.buffer.write('+repr(a.replace('\n','\r\n').encode())+')'],capture_output=True,text=True);print('normalized_crlf',g.bang_chung_xanh(r.stdout,pat))
print('regex_mut_no_DO',g.bang_chung_xanh('TONG: DO\n'+a,pat.replace(r'(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b)','')))
print('regex_mut_no_end',g.bang_chung_xanh(a+'log\n',pat.replace(r'\Z','')))
print('mode',g.ke_hoach(set()).get(p,(g.DAY_DU,)),g.env_theo_che_do(p,g.DAY_DU))
print('real',t.kiem(t.nap(),pathlib.Path('/home/user/rv773')))
# benign future record and changed exempt record, solely in temporary copy
f=R/'ops/land/pr99999-probe-land-evidence.yaml';f.write_text('x: ok\n');print('future_valid',t.chay_ca('c11_cay_that_dat_va_mien_tru_du'));f.unlink()
m=t.nap();f=R/'ops/land'/next(iter(m.MIEN_TRU_CUTOVER));old=f.read_bytes();f.write_bytes(old+b'\n');print('exempt_changed',t.chay_ca('c11_cay_that_dat_va_mien_tru_du'));f.write_bytes(old)
