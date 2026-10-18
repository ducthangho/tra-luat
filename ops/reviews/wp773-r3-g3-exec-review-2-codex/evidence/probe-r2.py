import runpy,re,contextlib,io,subprocess,sys
from pathlib import Path
r=Path('/tmp/rv773-r2'); d=runpy.run_path(str(r/'.claude/dev/ci_dang_ky_test.py')); p='ops/land_evidence_nguon_test.py'; pat=d['MOI'][p]
s='CA: 14/14 dat\nDOT BIEN: 37/37 bi giet dung ly do\nTU KIEM PHAN HANG: DAT (2 dot bien)\nTONG: DAT\n'
variants={'good':s,'ca13':s.replace('14/14','13/14'),'ca0':s.replace('14/14','0/0'),'db0':s.replace('37/37','0/0'),'db36':s.replace('37/37','36/37'),'no_db':'\n'.join(x for x in s.split('\n') if not x.startswith('DOT BIEN:')),'DO':s.replace('TONG: DAT','TONG: DO'),'DO_before':'TONG: DO\n'+s,'DO_after':s+'TONG: DO\n','selfDO':s.replace('HANG: DAT','HANG: DO'),'extra':s+'log\n','middle':s.replace('DOT BIEN:','log\nDOT BIEN:'),'order':s.replace('CA: 14/14 dat\n','')+'CA: 14/14 dat\n','NHE':s.replace('37/37 bi giet dung ly do','37 muc CHE DO NHE'),'CRLF_raw':s.replace('\n','\r\n'),'prefix':''.join('LOG '+x+'\n' for x in s.splitlines())}
print('groups',re.compile(pat).groups)
for k,v in variants.items():
 with contextlib.redirect_stdout(io.StringIO()): rc=d['chay_moi'](moi={p:pat},chay_mot=lambda _: (0,v),doc_nen_windows=lambda:False)
 print(k,d['bang_chung_xanh'](v,pat),'consumer_rc',rc)
print('mutant_no_lookahead',d['bang_chung_xanh'](variants['DO_before'],pat.replace(r'(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b)','')))
print('mutant_no_Z',d['bang_chung_xanh'](variants['extra'],pat.replace(r'\Z','')))
# Fake bad checker summary at c11 seam, then remove bound.
t=runpy.run_path(str(r/p)); name='c11_cay_that_dat_va_mien_tru_du'
for label,src in [('original',(r/p).read_text()),('no_bound',(r/p).read_text().replace(' and int(m.group(1)) <= n',''))]:
 ns={'__file__':str(r/p),'__name__':'probe'};exec(compile(src,str(r/p),'exec'),ns)
 ns['kiem']=lambda *a:(0,'land_evidence_nguon: 0 ĐẠT · 29/28 miễn trừ')
 print('c11_fake29',label,ns['chay_ca'](name))
# exercise real c11 on valid snapshot byte change and future file
m=t['nap'](); first=next(iter(m.MIEN_TRU_CUTOVER)); f=r/'ops/land'/first; old=f.read_bytes()
try:
 f.write_bytes(old+b'\n'); print('changed_exempt',t['kiem'](m,r)[0],t['chay_ca'](name))
finally:f.write_bytes(old)
f=r/'ops/land/pr9001-thu-land-evidence.yaml'
try:
 f.write_text('x: harmless\n');print('future_valid',t['kiem'](m,r)[0],t['chay_ca'](name))
finally:f.unlink()
