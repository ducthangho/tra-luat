import ast,json
from pathlib import Path
import probe_r3 as h
t=h.t
want={76,78,84,92,103,104,105,106,107,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124}
mod=ast.parse((h.COPY/'ops/bien_nhan_v2_test.py').read_text());fn=next(n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name=='_dot_bien')
class Filter(ast.NodeTransformer):
 def visit_Expr(self,n):
  if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='do':
   name=n.value.args[0].value;number=''.join(c for c in name.split('_')[0][1:] if c.isdigit())
   if not number or int(number) not in want:return None
  return n
fn=Filter().visit(fn);ast.fix_missing_locations(fn)
exec(compile(ast.Module(body=[fn],type_ignores=[]),'selected_original_mutants','exec'),t.__dict__)
orig=t._chay_1
seen=[]
def record(fn):
 ans=orig(fn);seen.append((fn.__name__,*ans));h.log(case=fn.__name__,status=ans[0],detail=ans[1]);return ans
t._chay_1=record
result=t._dot_bien();h.log(result=result)
