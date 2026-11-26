from pathlib import Path
import subprocess,sys,json,os,ast,importlib.util
from unittest.mock import patch
w=Path(__file__).resolve().parent;r=Path(__import__('tempfile').mkdtemp(dir=w/'tmp',prefix='ast-review-'))/'repo';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
subprocess.run(['git','clone','-q',str(w/'head'),str(r)],check=True)
A='ops/gate_output_doi_chieu_test.py';B='ops/land_evidence_nguon_test.py';a135='a135_bo_sinh_dung_mien_dac_ta';a136='a136_a135_do_khi_bo_sinh_lech_mien';c40='c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o';c39='c39_c37_do_khi_bo_sinh_lech_mien'
src=(r/A).read_text();rows=[]
def run(label,s,cases=(a135,a136),kind='AST'):
 (r/A).write_text(s)
 try:
  for ca in cases:
   p=A if ca[0]=='a' else B
   q=subprocess.run([sys.executable,'-B',p,'--mot-ca',ca],cwd=r,capture_output=True,text=True)
   row=dict(id=label,kind=kind,case=ca,rc=q.returncode,stdout=q.stdout,stderr=q.stderr);rows.append(row)
   (w/'ast-review.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(row,flush=True)
 finally:(r/A).write_text(src)
def change(old,new):
 assert src.count(old)==1,(old,src.count(old));return src.replace(old,new)
for label,old,new in [
 ('filter-out-a129','("a135", "a136")','("a129", "a135", "a136")'),
 ('prefix-b','f.name[0] == "a"','f.name[0] == "b"'),
 ('include-meta',' and f.name.split("_")[0] not in ("a135", "a136")',''),
 ('return-empty','    return ra\n','    return set()\n'),
 ('alias-fifth','    for ky_tu in _mau_loai_unicode("\\r\\n", {"Cs"}):','    alias = _mau_loai_unicode\n    for ky_tu in alias("\\r\\n", {"Cs"}):'),
 ('partial-fifth','    for ky_tu in _mau_loai_unicode("\\r\\n", {"Cs"}):','    from functools import partial\n    gen = partial(_mau_loai_unicode, "\\r\\n", {"Cs"})\n    for ky_tu in gen():'),
 ('kwargs-fifth','_mau_loai_unicode("\\r\\n", {"Cs"})','_mau_loai_unicode(**{"cam": "\\r\\n", "bo_loai": {"Cs"}})'),
 ('named-fifth','    for ky_tu in _mau_loai_unicode("\\r\\n", {"Cs"}):','    CAM = "\\r\\n"\n    for ky_tu in _mau_loai_unicode(CAM, {"Cs"}):'),
 ('reorder-keywords','_mau_loai_unicode("\\r\\n", {"Cs"})','_mau_loai_unicode(bo_loai={"Cs"}, cam="\\r\\n")'),
 ('only-call-fifth-drift','_mau_loai_unicode("\\r\\n", {"Cs"})','_mau_loai_unicode("\\r", {"Cs"})'),
 ('only-expected-fifth-drift','("\\r\\n", ("Cs",), 30, ("Cs",))','("\\r", ("Cs",), 30, ("Cs",))'),
 ('last-index','ord(ra[-1]) > 0xFFFF','ord(ra[-2]) > 0xFFFF'),
 ('lower-bound-plus2','all(ord(c) >= 0x80 for c in ra)','all(ord(c) >= 0x82 for c in ra)'),
 ('swap-last-two','ra = tuple(bo_sinh(cam, bo_loai))','ra = tuple(bo_sinh(cam, bo_loai)); ra = (*ra[:-2], ra[-1], ra[-2])'),
]:run(label,change(old,new))
# Mandatory fifth argument changed in both data sources: neither contains SPEC's CR+LF pair now.
s=src.replace('_mau_loai_unicode("\\r\\n", {"Cs"})','_mau_loai_unicode("\\r", {"Cs"})').replace('("\\r\\n", ("Cs",), 30, ("Cs",))','("\\r", ("Cs",), 30, ("Cs",))')
assert s!=src
(w/'co-drift.patch').write_text(__import__('difflib').unified_diff(src.splitlines(True),s.splitlines(True)).__str__() if False else ''.join(__import__('difflib').unified_diff(src.splitlines(True),s.splitlines(True),fromfile=A,tofile=A)))
run('co-drift-fifth-CR-only',s,(a135,a136,c39,c40,'c38_c36_do_khi_bang_cua_dot_a_mat_ca'),'outside/fixed mandatory value SPEC 2.3.1')
# Functional witness: generator wrong only at the original SPEC fifth argument.
witness=[]
for label,source in [('original',src),('co-drift',s)]:
 (r/A).write_text(source)
 try:
  for typ in ['healthy','bad-only-original-fifth']:
   sp=importlib.util.spec_from_file_location('identity_witness',r/A);m=importlib.util.module_from_spec(sp);exec(compile(source,str(r/A),'exec'),m.__dict__);real=m._mau_loai_unicode;calls=[]
   def gen(cam,bo=()):
    calls.append((cam,tuple(bo)));seq=real(cam,bo)
    return seq[:-1] if typ=='bad-only-original-fifth' and cam=='\r\n' and tuple(bo)==('Cs',) else seq
   with patch.dict(m.__dict__,{'_mau_loai_unicode':gen}):out=m.chay_ca(a135)
   witness.append(dict(guard=label,generator=typ,rc=out[0],output=out[1],calls=calls));print(witness[-1],flush=True)
 finally:(r/A).write_text(src)
(w/'co-drift-witness.json').write_text(json.dumps(witness,ensure_ascii=False,indent=2))

# Sweep co-drift across all other mandatory argument identities, not just fifth.
for label,edits in [
 ('co-drift-first', [('_mau_loai_unicode("—")', '_mau_loai_unicode("–")'), ('BO_SINH_MONG = (("—", (), 31, ())', 'BO_SINH_MONG = (("–", (), 31, ())')]),
 ('co-drift-second', [('_mau_loai_unicode("", bo_loai=("Cs",))', '_mau_loai_unicode("x", bo_loai=("Cs",))'), ('("", ("Cs",), 30, ("Cs",))', '("x", ("Cs",), 30, ("Cs",))')]),
 ('co-drift-third', [('_mau_loai_unicode("\\n\\r\\v\\f\\x1c\\x1d\\x1e\\x85\\u2028\\u2029 \\t")', '_mau_loai_unicode("\\n\\r\\v\\f\\x1c\\x1d\\x1e\\x85\\u2028\\u2029 ")'), ('+ " \\t", (), 29,', '+ " ", (), 29,')]),
 ('co-drift-fourth', [('_mau_loai_unicode("")', '_mau_loai_unicode("x")'), ('("", (), 31, ())', '("x", (), 31, ())')])]:
 candidate=src
 for old,new in edits:
  # Literal source escapes above are unescaped once for backslash-containing source patterns.
  old=old.replace(chr(92)*2,chr(92));new=new.replace(chr(92)*2,chr(92))
  assert old in candidate,(label,old)
  candidate=candidate.replace(old,new)
 run(label,candidate)

# Same-domain healthy function replacement, constant return, and AST read failures.
def load(source):
 sp=importlib.util.spec_from_file_location('ast_unit',r/A);m=importlib.util.module_from_spec(sp);exec(compile(source,str(r/A),'exec'),m.__dict__);return m
m=load(src);fixed=repr(m._mien_doi_so());run('AST-return-constant',change('    return ra\n','    return '+fixed+'\n'))
run('rename-generator-consistent',src.replace('_mau_loai_unicode','_generator_renamed'))
run('rename-without-detector-update',src.replace('_mau_loai_unicode','_generator_renamed').replace('== "_generator_renamed"','== "_mau_loai_unicode"'))
unit=[]
for typ in ['unreadable','syntax_error']:
 m=load(src)
 with patch.object(m.Path,'read_text',side_effect=OSError('injected unreadable')) if typ=='unreadable' else patch.object(m.Path,'read_text',return_value='def broken(:'):
  for ca in [a135,a136]:
   rc,out=m.chay_ca(ca);unit.append(dict(id=typ,case=ca,rc=rc,output=out))
(w/'ast-failure.json').write_text(json.dumps(unit,ensure_ascii=False,indent=2))
print(unit)
