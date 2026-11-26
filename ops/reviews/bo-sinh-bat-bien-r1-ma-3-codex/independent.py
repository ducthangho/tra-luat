from pathlib import Path
import subprocess,sys,json,time,os
w=Path(__file__).resolve().parent;r=w/'independent-copy';subprocess.run(['git','clone','-q',str(w/'head'),str(r)],check=True)
A='ops/gate_output_doi_chieu_test.py';B='ops/land_evidence_nguon_test.py'
a136='a136_a135_do_khi_bo_sinh_lech_mien';c40='c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o';c39='c39_c37_do_khi_bo_sinh_lech_mien'
source={p:(r/p).read_text() for p in (A,B)}
rows=[]
# Independently authored, not derived from M; extra dimensions deliberately include wiring, projection and cache.
changes=[
 ('a135-final-remove',A,'bang(not lech, f"bộ sinh','bang(True, f"bộ sinh',a136,'fixed/drop'),
 ('a135-final-invert',A,'bang(not lech, f"bộ sinh','bang(lech, f"bộ sinh',a136,'fixed/not'),
 ('c36-domain-invert',B,'if tru is not None:','if tru is None:',c40,'fixed/not'),
 ('c36-skip-domain',B,'if tru is not None:','if False:',c40,'fixed/drop branch'),
 ('c36-ascii-boundary',B,'if ord(c) > 127}','if ord(c) > 128}',c40,'fixed/+1'),
 ('a135-lower-plus2',A,'all(ord(c) >= 0x80 for c in ra)','all(ord(c) >= 0x82 for c in ra)',a136,'outside/+2'),
 ('a135-last-index',A,'ord(ra[-1]) > 0xFFFF','ord(ra[-2]) > 0xFFFF',a136,'outside/index'),
 ('c37-subset-reverse',B,'bmp.count(loai) != (loai != "Cs")','(loai != "Cs") != bmp.count(loai)',c39,'outside/swap-equivalent'),
 ('c36-unique-minus2',B,'len(van_tay) == mong - lap','len(van_tay) == mong - lap - 2',c40,'outside/-2'),
 ('a135-omit-fourth',A,'for cam, bo_loai, so, vang in BO_SINH_MONG:','for cam, bo_loai, so, vang in BO_SINH_MONG[:3] + BO_SINH_MONG[4:]:',a136,'outside/mandatory fourth argument'),
 ('a135-omit-fifth',A,'for cam, bo_loai, so, vang in BO_SINH_MONG:','for cam, bo_loai, so, vang in BO_SINH_MONG[:-1]:',a136,'outside/mandatory fifth argument'),
 ('a135-first-call-only',A,'for cam, bo_loai, so, vang in BO_SINH_MONG:','for cam, bo_loai, so, vang in BO_SINH_MONG[:1]:',a136,'outside/argument inventory'),
 ('c40-remove-own-assert',B,'bang((rc, dong) == ((0, "") if dau is None else (3, f"DO:{c36}:{dau}")),','bang(True,',c40,'fixed/meta-assert drop'),
 ('yaml-hit-test-negated',B,'if khoa in NHO_YAML else','if khoa not in NHO_YAML else',c40,'fixed/not in'),
 ('yaml-deepcopy-remove',B,'return copy.deepcopy(NHO_YAML[khoa] if khoa in NHO_YAML else NHO_YAML.setdefault(khoa, ham(x, **k)))','return NHO_YAML[khoa] if khoa in NHO_YAML else NHO_YAML.setdefault(khoa, ham(x, **k))',c40,'outside/cache copy'),
 ('a129-replace-unique-cell',A,'    kiem(dau + " [khong khop]" + duoi, ten_goc + " [khong khop]")\n','    kiem(dong + " ", ten_goc)\n','a129_ten_job_lazy_qua_ho_so','outside/structure'),
]
for label,p,old,new,case,kind in changes:
 assert source[p].count(old)==1,(label,source[p].count(old));assert old!=new
 try:
  (r/p).write_text(source[p].replace(old,new));t=time.monotonic()
  q=subprocess.run([sys.executable,'-B',p,'--mot-ca',case],cwd=r,capture_output=True,text=True)
  row=dict(id=label,kind=kind,path=p,cu=old,moi=new,case=case,rc=q.returncode,stdout=q.stdout,stderr=q.stderr,seconds=time.monotonic()-t)
  row['classification']='GIET' if q.returncode==3 and q.stdout.startswith('DO:'+case+':') else 'SONG' if q.returncode==0 else 'HONG'
  rows.append(row);(w/'independent.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(row,flush=True)
  if label=='a129-replace-unique-cell':
   q=subprocess.run([sys.executable,'-B',B,'--mot-ca','c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a'],cwd=r,capture_output=True,text=True)
   rows.append(dict(id=label+'-L8',rc=q.returncode,stdout=q.stdout,stderr=q.stderr));(w/'independent.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 finally:(r/p).write_text(source[p])
# Independent witness: bad only at fifth SPEC argument, with original vs truncated argument inventory.
import importlib.util
from unittest.mock import patch
witness=[]
for label,s in [('original',source[A]),('omit-fifth',source[A].replace('for cam, bo_loai, so, vang in BO_SINH_MONG:','for cam, bo_loai, so, vang in BO_SINH_MONG[:-1]:'))]:
 spec=importlib.util.spec_from_file_location('witness_a',r/A);m=importlib.util.module_from_spec(spec);exec(compile(s,str(r/A),'exec'),m.__dict__)
 that=m._mau_loai_unicode
 for kind in ['healthy','bad-only-fifth']:
  calls=[]
  def gen(cam,bo=()):
   calls.append([cam,list(bo)]);seq=that(cam,bo)
   return seq[:-1] if kind=='bad-only-fifth' and cam=='\r\n' and tuple(bo)==('Cs',) else seq
  with patch.dict(m.__dict__,{'_mau_loai_unicode':gen}):out=m.chay_ca('a135_bo_sinh_dung_mien_dac_ta')
  row=dict(guard=label,generator=kind,rc=out[0],output=out[1],arguments=calls);witness.append(row);print(row,flush=True)
(w/'fifth-witness.json').write_text(json.dumps(witness,ensure_ascii=False,indent=2))
# Same lost-inventory mutation checked against all four repository counterexample cases.
try:
 (r/A).write_text(source[A].replace('for cam, bo_loai, so, vang in BO_SINH_MONG:','for cam, bo_loai, so, vang in BO_SINH_MONG[:-1]:'))
 allmeta=[]
 for p,c in [(B,'c38_c36_do_khi_bang_cua_dot_a_mat_ca'),(B,c39),(B,c40),(A,a136)]:
  q=subprocess.run([sys.executable,'-B',p,'--mot-ca',c],cwd=r,capture_output=True,text=True)
  allmeta.append(dict(case=c,rc=q.returncode,stdout=q.stdout,stderr=q.stderr));print('fifth-allmeta',allmeta[-1],flush=True)
 (w/'fifth-allmeta.json').write_text(json.dumps(allmeta,ensure_ascii=False,indent=2))
finally:(r/A).write_text(source[A])
fourth=[]
for label,s in [('original',source[A]),('omit-fourth',source[A].replace('for cam, bo_loai, so, vang in BO_SINH_MONG:','for cam, bo_loai, so, vang in BO_SINH_MONG[:3] + BO_SINH_MONG[4:]:'))]:
 spec=importlib.util.spec_from_file_location('witness_fourth',r/A);m=importlib.util.module_from_spec(spec);exec(compile(s,str(r/A),'exec'),m.__dict__);that=m._mau_loai_unicode
 for kind in ['healthy','bad-only-fourth']:
  calls=[]
  def gen(cam,bo=()):
   calls.append([cam,list(bo)]);seq=that(cam,bo)
   return seq[:-1] if kind=='bad-only-fourth' and cam=='' and not bo else seq
  with patch.dict(m.__dict__,{'_mau_loai_unicode':gen}):out=m.chay_ca('a135_bo_sinh_dung_mien_dac_ta')
  row=dict(guard=label,generator=kind,rc=out[0],output=out[1],arguments=calls);fourth.append(row);print(row,flush=True)
(w/'fourth-witness.json').write_text(json.dumps(fourth,ensure_ascii=False,indent=2))
