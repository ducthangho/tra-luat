import ast,json,unicodedata,sys,hashlib
from pathlib import Path
w=Path(__file__).resolve().parent
s=(w/'head/ops/gate_output_doi_chieu_test.py').read_text()
t=ast.parse(s);fn=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_mau_loai_unicode')
g={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<actual-generator>','exec'),g)
rows=[]
for cam,bo in [('—',()),('',('Cs',)),('\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029 \t',()),('',()),('\r\n',('Cs',))]:
 d=g['_mau_loai_unicode'](cam,bo)
 rows.append({'cam':cam,'bo':bo,'members':[[hex(ord(c)),unicodedata.category(c),c.isspace(),c.isdecimal()] for c in d],'count':len(d),'LN':sum(unicodedata.category(c)[0] in 'LN' for c in d),'Nd':sum(unicodedata.category(c)=='Nd' for c in d),'space':sum(c.isspace() for c in d)})
out={'python':sys.version,'unicode':unicodedata.unidata_version,'domains':rows,'non_ascii_whitespace':[hex(i) for i in range(128,0x110000) if chr(i).isspace()]}
print(json.dumps(out,ensure_ascii=True,indent=2))
