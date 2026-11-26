import ast, json, sys, unicodedata, hashlib
from pathlib import Path
root=Path(sys.argv[1]); scratch=Path(sys.argv[2]); source=root/'ops/gate_output_doi_chieu_test.py'
tree=ast.parse(source.read_text(encoding='utf-8'))
names={'_mau_loai_unicode','_mien_doi_so','_bo_sinh_nho','kiem_bo_sinh'}
constants={'LOAI_UNICODE','BO_SINH_MONG','_NHO_BO_SINH'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constants for t in n.targets)]
def bang(ok,msg):
 if not ok: raise AssertionError(msg)
ns={'Path':Path,'__file__':str(source),'bang':bang}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
mien=ns['_mien_doi_so'](); rows=[]
for cam,bo,n,vang in ns['BO_SINH_MONG']:
 out=ns['_mau_loai_unicode'](cam,bo); rows.append({'cam':cam,'bo':bo,'codepoints':[ord(c) for c in out],'categories':[unicodedata.category(c) for c in out]})
ns['kiem_bo_sinh'](ns['_mau_loai_unicode'])
crlf=scratch/('source-crlf-'+sys.version.split()[0]+'.py'); crlf.write_bytes(source.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))
ns['__file__']=str(crlf); assert ns['_mien_doi_so']()==mien
ns['kiem_bo_sinh'](ns['_mau_loai_unicode'])
healthy=ns['_mau_loai_unicode']; bad=lambda cam,bo=():healthy(cam,bo)[:-1]
ns['kiem_bo_sinh'](lambda cam,bo=():ns['_bo_sinh_nho'](healthy,cam,bo))
try: ns['kiem_bo_sinh'](lambda cam,bo=():ns['_bo_sinh_nho'](bad,cam,bo))
except AssertionError as e: cache_negative=str(e)
else: raise AssertionError('bad generator hidden by warmed cache')
result={'python':sys.version,'unicode':unicodedata.unidata_version,'domain_count':len(mien),'rows':rows,'crlf_domain_equal':True,'controls_passed':True,'warm_cache_bad_generator_rejected':cache_negative,'scope':'Extracted exact generator/check/cache/AST definitions; no full suite or Windows emulation.'}
print(json.dumps(result,ensure_ascii=True,indent=2))
