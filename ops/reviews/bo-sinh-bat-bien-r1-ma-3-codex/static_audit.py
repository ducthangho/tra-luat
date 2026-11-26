from pathlib import Path
import subprocess,hashlib,json,ast
w=Path(__file__).resolve().parent;r=w.parent/'repo';base='a89c83acf998008caecba9084a7d295845bf1976';out={}
for p in ['ops/land_evidence_nguon.py','ops/gate_output_doi_chieu.py']:
 before=subprocess.check_output(['git','-C',str(r),'show',base+':'+p]);after=(r/p).read_bytes()
 out[p]={'identical':before==after,'base_sha256':hashlib.sha256(before).hexdigest(),'head_sha256':hashlib.sha256(after).hexdigest()}
(w/'product-identical.json').write_text(json.dumps(out,indent=2));print(out)
diff=subprocess.check_output(['git','-C',str(r),'diff',base,'HEAD'],text=True)
lines=[l for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')]
triggers=[l for l in lines if any(x in l for x in ['os.name','sys.platform','platform.system','subprocess','encoding=','os.sep','pathlib'])]
(w/'m3-lines.json').write_text(json.dumps(triggers,ensure_ascii=False,indent=2));print('M3',triggers)
# All anchors and mutation byte deltas checked independently without running the table.
ns={'__name__':'table_static'};exec(compile((w/'bang_toan_tu.py').read_text(),str(w/'bang_toan_tu.py'),'exec'),ns)
rows=[]
for mid,p,ca,old,ops in ns['M']:
 src=(r/p).read_text()
 for op,new in ops.items():
  mutated=src.replace(old,new)
  row=dict(id=mid,op=op,anchor_count=src.count(old),different=mutated!=src)
  try:ast.parse(mutated);row['syntax_valid']=True
  except SyntaxError as e:row.update(syntax_valid=False,error=str(e))
  rows.append(row)
(w/'table-static.json').write_text(json.dumps(rows,indent=2));print('Anchors',len(rows),'valid',all(x['anchor_count']==1 and x['different'] and x['syntax_valid'] for x in rows))
