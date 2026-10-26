import ast, collections, copy, hashlib, importlib.util, json, pathlib
R=pathlib.Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('test8',root/'ops/ci_provenance_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
src=(root/'ops/ci_provenance.py').read_text(); tree=ast.parse(src)
counts=collections.Counter(); per={}; emitted=[]; invalid=[]; same=[]; types={}
canon=ast.unparse(tree)
for f in tree.body:
    if not isinstance(f,ast.FunctionDef) or f.name not in t.HAM_DONG: continue
    c=collections.Counter(type(n).__name__ for n in ast.walk(f)); counts.update(c); per[f.name]=dict(c)
    doc={id(x.value) for x in ast.walk(f) if isinstance(x,ast.Expr) and isinstance(x.value,ast.Constant)}
    for j,n in enumerate(list(ast.walk(f))[1:]):
        if id(n) in doc: continue
        ops=list(t._toan_tu(n)); z=types.setdefault(type(n).__name__,{'nodes':0,'with_operator':0,'operators':set()});z['nodes']+=1;z['with_operator']+=bool(ops);z['operators'].update(a for a,_ in ops)
        for name,fn in ops:
            tr=ast.parse(src); ff=next(x for x in tr.body if isinstance(x,ast.FunctionDef) and x.name==f.name)
            target=list(ast.walk(ff))[1:][j];fn(target); mid=f'{f.name}#{j}:{name}'
            try: val=ast.unparse(ast.fix_missing_locations(tr));compile(val,'<db>','exec')
            except (SyntaxError,ValueError,TypeError,IndexError) as e:
                invalid.append([mid,type(e).__name__,str(e)]);continue
            if val==canon:same.append(mid)
            else:emitted.append([mid,val])
actual=t.sinh_dot_bien_dong(src)
assert emitted==[list(x) for x in actual]
assert len({x[0] for x in emitted})==len(emitted)
changed=t.sinh_dot_bien_dong('UNRELATED=1\n'+src+'\nUNRELATED_2=2\n')
assert [m for m,_ in actual]==[m for m,_ in changed]
sources=collections.defaultdict(list)
for m,v in actual:sources[hashlib.sha256(v.encode()).hexdigest()].append(m)
for z in types.values():z['operators']=sorted(z['operators'])
report={'total':len(actual),'raw_valid':len(emitted),'invalid_skipped':invalid,'no_effect':same,'id_collisions':len(emitted)-len(set(x[0] for x in emitted)),'source_duplicates':[v for v in sources.values() if len(v)>1],'ids_stable_outside_functions':True,'counts':dict(counts),'per_function':per,'types':types,'mutants':[{'id':m,'sha256':hashlib.sha256(v.encode()).hexdigest()} for m,v in actual],'equivalence':t.TUONG_DUONG}
(R/'audit9-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ('mutants','per_function','source_duplicates')},ensure_ascii=False,indent=2))
print('duplicate source groups',len(report['source_duplicates']))
