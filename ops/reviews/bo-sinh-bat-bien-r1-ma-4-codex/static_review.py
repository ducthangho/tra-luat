from pathlib import Path
import subprocess,json,hashlib,platform,sys,unicodedata
w=Path(__file__).resolve().parent;r=w.parent/'repo';rows=[]
for args in [['git','diff','--numstat','a89c83a','HEAD'],['git','diff','--check','a89c83a','HEAD'],['git','status','--porcelain=v1','--untracked-files=all','--ignored=matching'],['git','rev-parse','HEAD','HEAD^{tree}','HEAD^'],['git','config','core.abbrev'],[sys.executable,'-m','ruff','--version']]:
 p=subprocess.run(args,cwd=r,capture_output=True,text=True);rows.append(dict(command=args,rc=p.returncode,stdout=p.stdout,stderr=p.stderr))
products={}
for path in ['ops/land_evidence_nguon.py','ops/gate_output_doi_chieu.py']:
 b=subprocess.check_output(['git','show','a89c83a:'+path],cwd=r);h=(r/path).read_bytes();products[path]=dict(equal=b==h,base_sha256=hashlib.sha256(b).hexdigest(),head_sha256=hashlib.sha256(h).hexdigest())
diff=subprocess.check_output(['git','diff','a89c83a','HEAD'],cwd=r,text=True)
lines=[l for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++') and any(s in l for s in ['os.name','sys.platform','platform.system','subprocess','encoding=','os.sep','pathlib'])]
(w/'static-review.json').write_text(json.dumps(dict(commands=rows,products=products,m3_lines=lines,runtime=dict(python=sys.version,os=platform.platform(),unicode=unicodedata.unidata_version)),ensure_ascii=False,indent=2));print(json.dumps(rows,ensure_ascii=False));print(products);print(lines)
