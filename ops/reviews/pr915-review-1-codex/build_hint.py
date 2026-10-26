from pathlib import Path
import difflib,tempfile,shutil,contextlib,io
import review_probe as p
files={}
id_='VERDICT-KHAI-SAI-EXECUTION-SURFACE'
for n in p.NAMES[:2]:
 short={'pr870-review-2-codex':'2699e2d8','pr889-review-2-codex':'d955f9ef'}[n]
 desc=(f'Verdict dong 9 tu khai `codex_service`, nhung run.json {short} ghi lenh.chuong_trinh=codex va execution_surface=codex_cli; header CLI cung ghi OpenAI Codex v0.163.0. '
       + ('Cau "khong chay qua codex exec/Desktop" trong verdict khong khop hien vat launcher. ' if n.startswith('pr889') else '')
       +'Dinh chinh be mat thanh codex_cli; giu nguyen byte verdict lich su. Day khong phai chung thuc model/effort da phuc vu.')
 rel=f'ops/reviews/{n}-verdict.receipt.yaml';s=(p.ROOT/rel).read_text()
 neo='verdict_usage_caveats:\n';assert s.count(neo)==1
 block=f'  - id: {id_}\n    muc: P1\n    mo_ta: >-\n      {desc}\n'
 files[rel]=s.replace(neo,neo+block,1)
 readme_rel='ops/reviews/README.md';s=files.get(readme_rel,(p.ROOT/readme_rel).read_text())
 neo=f'| `{n}-verdict.md` | `HO-MODEL-REVIEWER-KHONG-DO-DUOC` |';assert s.count(neo)==1
 new=f'| `{n}-verdict.md` | `{id_}` | {desc} |\n'
 files[readme_rel]=s.replace(neo,new+neo,1)
patch='# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n'
for rel,new in sorted(files.items()):
 old=(p.ROOT/rel).read_text()
 patch+=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=rel,tofile=rel))
(p.BASE/'HINT.patch').write_text(patch)
print('HINT.patch files='+str(len(files))+'; paths='+repr(sorted(files)))
with tempfile.TemporaryDirectory(prefix='pr915-hint-check-') as tmp:
 root=Path(tmp);dr=root/'ops/reviews';dr.mkdir(parents=True)
 # Individual immutable file symlinks provide the full historical index for t26/t27.
 for original in (p.ROOT/'ops/reviews').iterdir():
  (dr/original.name).symlink_to(original,target_is_directory=original.is_dir())
 for rel in files:
  f=root/rel;f.unlink();shutil.copyfile(p.ROOT/rel,f)
 r=p.run(['patch','--dry-run','-p0','--fuzz=0','-i',str(p.BASE/'HINT.patch')],root)
 print('patch --dry-run -p0 --fuzz=0 rc='+str(r.returncode)+'; '+repr(r.stdout))
 assert r.returncode==0
 r=p.run(['patch','-p0','--fuzz=0','-i',str(p.BASE/'HINT.patch')],root)
 print('patch -p0 --fuzz=0 rc='+str(r.returncode));assert r.returncode==0
 for rel,new in files.items(): assert (root/rel).read_text()==new
 m=p.load_module('pr915_hint_lease',p.ROOT/'ops/lease_publish_test.py');m.HERE=root/'ops'
 for prefix in ['t26_','t27_']:
  name=next(k for k in vars(m) if k.startswith(prefix));getattr(m,name)();print(name+': DAT tren ban sao da ap hint')
 # t27 detects removal of either correction from README while retaining receipt.
 rd=root/'ops/reviews/README.md';full=rd.read_text()
 for n in p.NAMES[:2]:
  lines=[s for s in full.splitlines(True) if not (n+'-verdict.md' in s and id_ in s)]
  assert len(lines)==len(full.splitlines())-1;rd.write_text(''.join(lines))
  try:m.t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()
  except AssertionError as e:
   print('remove_new_README_caveat '+n+': t27 FAIL; '+str(e));assert id_ in str(e)
  else:raise AssertionError('mutant survived')
  rd.write_text(full)
 print('KET_LUAN: patch hop le; t26/t27 nen xanh; hai dot bien bo canh bao deu do; khong sua hien vat verdict/hash.')
