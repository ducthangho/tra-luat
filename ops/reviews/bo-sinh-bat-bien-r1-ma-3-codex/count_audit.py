from pathlib import Path
import importlib.util,json,os,sys,collections,unicodedata,yaml
w=Path(__file__).resolve().parent;r=w/'head'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
p=r/'ops/gate_output_doi_chieu_test.py';sp=importlib.util.spec_from_file_location('a',p);a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
g=a.G();old=g.kiem_ho_so;rows=[]
for prefix in ['a124','a125','a126','a129','a131','a132','a133','a134']:
 name=next(n for n in a.CA if n.startswith(prefix+'_'));seen={};duplicates=[];total=[0]
 def collect(data,root):
  total[0]+=1
  filedata=() if Path(root)==a.ROOT else tuple(sorted((f.relative_to(root).as_posix(),f.read_bytes()) for f in Path(root).rglob('*') if f.is_file()))
  identity=(yaml.safe_dump(data,allow_unicode=False).encode('ascii'),*filedata)
  frame=sys._getframe(1)
  while frame and frame.f_code.co_name!=name:frame=frame.f_back
  tag={k:(hex(ord(v))+' '+unicodedata.category(v) if isinstance(v,str) and len(v)==1 else v) for k in ['truong','i','vi_tri','c','ky_tu'] if (v:=frame.f_locals.get(k)) is not None}
  tag['line']=frame.f_lineno
  if identity in seen:duplicates.append({'now':tag,'first':seen[identity]})
  else:seen[identity]=tag
  return old(data,root)
 g.kiem_ho_so=collect
 out=a.chay_ca(name)
 row=dict(case=name,rc=out[0],output=out[1],total=total[0],distinct=len(seen),repeated=total[0]-len(seen),duplicate_pairs=duplicates)
 rows.append(row);(w/'count-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 print(prefix,out,total[0],len(seen),len(duplicates),flush=True)
