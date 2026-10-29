"""Run selected existing mutations unchanged; preserve full target failure text."""
import ast
import inspect
import json
import re
import probe_review as p

t=p.t
wanted={76,78,84,*range(103,114)}
a=ast.parse(inspect.getsource(t._dot_bien));fn=a.body[0]
body=[]
for n in fn.body:
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='do':
  name=n.value.args[0].value
  number=int(re.match(r'm(\d+)',name).group(1))
  if number not in wanted:continue
 body.append(n)
fn.body=body
ns=t.__dict__
old=t._chay_1
failures=[]
def spy(fn):
 state,detail=old(fn)
 if state!='qua':failures.append(dict(case=fn.__name__,state=state,detail=detail))
 return state,detail
ns['_chay_1']=spy
exec(compile(ast.fix_missing_locations(a),'existing-selected-mutants','exec'),ns)
rows=ns['_dot_bien']()
for row,f in zip(rows,failures):print(json.dumps(dict(mutation=row[0],result=row[2:5],target_failure=f),ensure_ascii=False),flush=True)
print('ROWS',len(rows),'FAILURES',len(failures))
