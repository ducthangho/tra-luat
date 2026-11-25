from pathlib import Path
import importlib.util,json,shutil,sys,os,time,collections
sys.dont_write_bytecode=True
r=Path.cwd();w=r.parent/'work';root=w/'adapter-copy';root.mkdir(exist_ok=True);(root/'ops').mkdir(exist_ok=True)
for f in ['land_evidence_nguon.py','land_evidence_nguon_test.py','gate_output_doi_chieu.py','gate_output_doi_chieu_test.py']:
 shutil.copyfile(r/'ops'/f,root/'ops'/f)
# Input fixtures copied as bytes; no writes or links back into the reviewed repository.
for d in ['land','specs']:
 if not (root/'ops'/d).exists():shutil.copytree(r/'ops'/d,root/'ops'/d)
s=importlib.util.spec_from_file_location('bt',root/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
c36=next(k for k in t.CA if k.startswith('c36_'));c37=next(k for k in t.CA if k.startswith('c37_'));c38=next(k for k in t.CA if k.startswith('c38_'))
a_path=root/'ops/gate_output_doi_chieu_test.py';orig=a_path.read_text();a=t.nap_a(a_path.name);chosen=t.chon_ca_a(a.CA);rows=[]
def measure(mode,source,cases):
 a_path.write_text(source)
 counts=collections.Counter();old=t.dong_l8
 def observe(out):
  f=sys._getframe(1)
  if f.f_code.co_name=='qua_l8':
   while f:
    if f.f_code.co_name.startswith(tuple(chosen)):
     counts[f.f_code.co_name]+=1;break
    f=f.f_back
  return old(out)
 t.dong_l8=observe
 for case in cases:
  start=time.monotonic();rc,out=t.chay_ca(case);row={'mode':mode,'case':case,'rc':rc,'output':out,'seconds':time.monotonic()-start,'counts':dict(counts)};rows.append(row);print(json.dumps(row,ensure_ascii=True),flush=True)
 t.dong_l8=old
 (w/'adapter-audit.json').write_text(json.dumps(rows,ensure_ascii=True,indent=2))
measure('baseline',orig,[c36,c37,c38])
for tt,ten in chosen.items():
 for mode in ['rename','drop','duplicate']:
  anchor='@ca\ndef '+ten+'():'
  assert orig.count(anchor)==1
  replacement={'rename':'@ca\ndef renamed_'+ten+'():','drop':'def '+ten+'():','duplicate':anchor}[mode]
  source=orig.replace(anchor,replacement)
  if mode=='duplicate':source+='\nCA['+repr(tt+'_ban_sao')+']=CA['+repr(ten)+']\n'
  measure(mode+'-'+tt,source,[c36])
# Independent regression probes for the floor: remove one declared representative category, and one lazy branch.
anchor='if ky_tu not in cam and loai not in bo_loai:'
assert orig.count(anchor)==1
measure('omit-category-Mn',orig.replace(anchor,'if ky_tu not in cam and loai not in bo_loai and loai != "Mn":'),[c36,c37,c38])
anchor='    kiem(dau + " [khong khop]" + duoi, ten_goc + " [khong khop]")\n'
assert orig.count(anchor)==1
measure('omit-lazy-backtracking',orig.replace(anchor,''),[c36,c38])
a_path.write_text(orig)
