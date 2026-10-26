import ast, hashlib, importlib.util, json, pathlib
R=pathlib.Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t9',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text();rows=[]
for k,prefix in [(0,'c32'),(1,'c52')]:
 tr=ast.parse(src);f=next(n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name=='doc_wf')
 nodes=list(ast.walk(f))[1:];j,n=next((j,n) for j,n in enumerate(nodes) if isinstance(n,ast.ExceptHandler));ops=dict(t._toan_tu(n))
 op=f'bo_ngoai_le{k}';assert op in ops;ops[op](n);v=ast.unparse(ast.fix_missing_locations(tr));p=R/(op+'.py');p.write_text(v)
 c=next(c for c in t.CA if c.split('_')[0]==prefix)
 for label,ma in [('head',root/'ops/ci_provenance.py'),('mutant',p)]:
  rc,ra=t.chay_con(c,ma);rows.append({'mutant_id':f'doc_wf#{j}:{op}','case':c,'source':label,'source_sha256':hashlib.sha256(ma.read_bytes()).hexdigest(),'rc':rc,'output':ra,'rank':t.phan_hang(rc,ra,c)})
print(json.dumps(rows,ensure_ascii=False,indent=2));(R/'patch9-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
assert all(x['rc']==(0 if x['source']=='head' else 3) for x in rows)
