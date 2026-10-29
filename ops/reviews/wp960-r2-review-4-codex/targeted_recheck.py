import ast
import replay_probe_recheck as h
t=h.t
wanted={103,114,125,126,127,128,129,130,131}
fn=next(n for n in ast.parse((h.COPY/'ops/bien_nhan_v2_test.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='_dot_bien')
class Filter(ast.NodeTransformer):
 def visit_Expr(self,n):
  if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='do':
   name=n.value.args[0].value;num=''.join(c for c in name.split('_')[0][1:] if c.isdigit())
   if not num or int(num) not in wanted:return None
  return n
fn=Filter().visit(fn);ast.fix_missing_locations(fn);exec(compile(ast.Module(body=[fn],type_ignores=[]),'existing_mutants_subset','exec'),t.__dict__)
result=t._dot_bien();h.log(result=result)
