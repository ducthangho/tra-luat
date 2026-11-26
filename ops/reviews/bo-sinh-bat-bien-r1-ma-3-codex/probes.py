# Same-run lock: execute the historical probes once; queue invocation reuses their completed receipt.
import fcntl
from pathlib import Path
import sys,json,time
_pw=Path(__file__).resolve().parent
_plock=(_pw/'probes.lock').open('w')
fcntl.flock(_plock,fcntl.LOCK_EX)
if (_pw/'probes-complete.json').exists():
 print('Already completed in this review run; see probes-complete.json and probes.json',flush=True)
 sys.exit(0)
_started=time.monotonic()
from pathlib import Path
import os,sys,subprocess,json,time
w=Path(__file__).resolve().parent;r=w/'mut'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
A='ops/gate_output_doi_chieu_test.py';B='ops/land_evidence_nguon_test.py'
orig={p:(r/p).read_text() for p in [A,B]}
rows=[]
def run(label,p,case=None):
 cmd=[sys.executable,'-B',p]+(['--mot-ca',case] if case else [])
 t=time.monotonic();x=subprocess.run(cmd,cwd=r,env=env,capture_output=True,text=True)
 row=dict(label=label,command=cmd,rc=x.returncode,seconds=time.monotonic()-t,stdout=x.stdout,stderr=x.stderr)
 rows.append(row);(w/'probes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps(row,ensure_ascii=False),flush=True)
def edit(p,a,b):
 assert orig[p].count(a)==1,(a,orig[p].count(a));(r/p).write_text(orig[p].replace(a,b))
def restore():
 for p,s in orig.items():(r/p).write_text(s)
c39='c39_c37_do_khi_bo_sinh_lech_mien';c40='c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o';a136='a136_a135_do_khi_bo_sinh_lech_mien'
for p,c in [(B,c39),(B,c40),(A,a136),(B,'c38_c36_do_khi_bang_cua_dot_a_mat_ca')]:run('control-'+c,p,c)
C='bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158 and not lech,'
changes=[('c36-count',B,'bang(rc == 0 and dem[0] - truoc == mong,','bang(rc == 0,',c40),('c36-category',B,'bang(not thieu,','bang(True,',c40),('c36-BMP',B,'bang(any(ord(c) > 0xFFFF for c in thay),','bang(True,',c40),('c37-total-executor',B,C,'bang(len(set(vu_tru)) == len(vu_tru) and not lech,',c39),('c37-total-literal',B,C,'bang(len(set(vu_tru)) == 158 and not lech,',c39),('c37-distinct',B,C,'bang(len(vu_tru) == 158 and not lech,',c39),('c37-category',B,C,'bang(len(vu_tru) == 158 and len(set(vu_tru)) == 158,',c39),('c37-648',B,'bang(len(o) == 648,','bang(True,',c39)]
changes.append(('c36-distinct',B,'bang(len(van_tay) == mong - lap,','bang(True,',c40))
changes += [(f'a135-{n}',A,f'("{n}", ',f'("{n}", True or ',a136) for n in ['so_phan_tu','category_vang','lap_category','thuoc_cam','tu_0080','cuoi_ngoai_bmp']]
for label,p,a,b,c in changes:
 try:edit(p,a,b);run(label,p,c)
 finally:restore()
(w/'probes-complete.json').write_text(json.dumps({'status':'complete','rows':len(rows),'seconds':time.monotonic()-_started},indent=2))
