from pathlib import Path
import importlib.util,json,types,os
w=Path(__file__).resolve().parent;p=w/'head/ops/land_evidence_nguon_test.py';os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(w/'tmp'))
sp=importlib.util.spec_from_file_location('b',p);b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
needle='("nhan", "", dung),';m=b.nap_sua(p.name,needle,needle)
def normalize(c):
 return {k:([normalize(x) if isinstance(x,types.CodeType) else repr(x) for x in c.co_consts] if k=='co_consts' else repr(getattr(c,k))) for k in ['co_argcount','co_posonlyargcount','co_kwonlyargcount','co_nlocals','co_stacksize','co_flags','co_code','co_consts','co_names','co_varnames','co_filename','co_name','co_qualname','co_firstlineno','co_linetable','co_exceptiontable','co_freevars','co_cellvars']}
rows=[]
for n in b.CA:
 x=normalize(b.CA[n].__code__);y=normalize(m.CA[n].__code__)
 rows.append({'case':n,'code_eq':b.CA[n].__code__==m.CA[n].__code__,'differences':{k:[x[k],y[k]] for k in x if x[k]!=y[k]}})
helpers={n:normalize(f.__code__)==normalize(getattr(m,n).__code__) for n,f in vars(b).items() if isinstance(f,types.FunctionType) and f.__module__==b.__name__}
out={'declared_functions_equal':helpers,'all_declared_functions_equal':all(helpers.values()),'cases':rows,'all_normalized_equal':all(not x['differences'] for x in rows),'all_python_code_equal':all(x['code_eq'] for x in rows)}
(w/'nap-code-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('all_normalized_equal',out['all_normalized_equal'],'all_python_code_equal',out['all_python_code_equal']);print([x for x in rows if x['differences']])
