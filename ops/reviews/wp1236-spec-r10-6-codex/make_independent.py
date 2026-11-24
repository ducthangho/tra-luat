import ast,copy,json,pathlib
w=pathlib.Path(__file__).resolve().parent; src=(w.parent/'repo/ops/gate_output_doi_chieu.py').read_text(); tree=ast.parse(src); out=[]
def add(name,s,kind,line):
 if s!=src:
  compile(s,name,'exec');out.append(dict(id=name,kind=kind,line=line,src=s))
# Every reason literal, both direct and f-string prefixes; does not change data keys or expected outputs.
reasons={'khong_phai_utf8','xuong_dong_tron','cr_le','dau_tep_sai','job_lap','dong_la','thieu_moc','moc_lap','symlink','provenance_0','provenance_nhieu','bo_sinh_la','khong_phai_run_land','job_id_trung_provenance','provenance_chua_du','tap_job_lech','tap_skip_lech','job_lech:','ket_luan_lech:','log_sha_lech:','dong_skip_sai_phien_ban','moc_lech','co_job_skipped','check_bat_buoc:','url','readback','doc_readback','html_url','tac_gia','dong_mien','han','os','sha'}
# Only string values in List or JoinedStr, to leave dictionary access unchanged.
parents={c:n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
for i,n in enumerate(ast.walk(tree)):
 if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value in reasons and isinstance(parents.get(n),(ast.List,ast.JoinedStr)):
  t=copy.deepcopy(tree);nn=list(ast.walk(t))[i];nn.value+='__doi';add('reason_'+str(n.lineno)+'_'+str(n.col_offset),ast.unparse(t),'reason',n.lineno)
 if isinstance(n,ast.Compare) and any(isinstance(o,(ast.Is,ast.IsNot)) for o in n.ops):
  t=copy.deepcopy(tree);nn=list(ast.walk(t))[i];nn.ops=[ast.Eq() if isinstance(o,ast.Is) else ast.NotEq() if isinstance(o,ast.IsNot) else o for o in nn.ops]; add('identity_'+str(n.lineno)+'_'+str(n.col_offset),ast.unparse(t),'identity',n.lineno)
 if isinstance(n,ast.Return) and isinstance(parents.get(n),ast.If):
  t=copy.deepcopy(tree);nn=list(ast.walk(t))[i]
  class Del(ast.NodeTransformer):
   def visit_Return(self,x):return ast.copy_location(ast.Pass(),x) if x is nn else x
  t=Del().visit(t);ast.fix_missing_locations(t);add('delete_return_'+str(n.lineno),ast.unparse(t),'early_return',n.lineno)
# One-at-a-time mutations of every literal membership set, and producer labels.
for n in tree.body:
 if not isinstance(n,ast.Assign) or not isinstance(n.targets[0],ast.Name):continue
 name=n.targets[0].id
 if name in ('TOKEN','PHI_LOI_KHAI','CHECK_BAT_BUOC_TEN','BO_SINH'):
  values=n.value.args[0].elts if isinstance(n.value,ast.Call) else n.value.elts if isinstance(n.value,ast.Tuple) else n.value.keys
  for k in range(len(values)):
   t=copy.deepcopy(tree);q=next(q for q in t.body if isinstance(q,ast.Assign) and isinstance(q.targets[0],ast.Name) and q.targets[0].id==name)
   if isinstance(q.value,ast.Dict):del q.value.keys[k];del q.value.values[k]
   elif isinstance(q.value,ast.Call):del q.value.args[0].elts[k]
   else:del q.value.elts[k]
   add(f'set_remove_{name}_{k}',ast.unparse(t),'set',n.lineno)
  if name=='BO_SINH':
   for k in range(3):
    t=copy.deepcopy(tree);q=next(q for q in t.body if isinstance(q,ast.Assign) and isinstance(q.targets[0],ast.Name) and q.targets[0].id==name);q.value.values[k].value='v3' if k<2 else 'v2';add(f'producer_version_{k}',ast.unparse(t),'set',n.lineno)
# Regex alternatives removed and parser matching contracts weakened.
repls=[('skip_v3_partial','RE_SKIP_V3.fullmatch(d)','RE_SKIP_V3.match(d)'),('waiver_partial','RE_MIEN.fullmatch(x.strip())','RE_MIEN.match(x.strip())'),('landed_partial','RE_KHOI_LANDED.fullmatch(k)','RE_KHOI_LANDED.match(k)'),('ref_no_boundary',r'(?<![A-Za-z0-9_./-])',''),('ref_any_run',r'output-[0-9]+',r'output-[a-z0-9]+'),('ref_txt_wild',r'\.txt',r'.txt'),('token_no_casefold','RE_TOKEN.match(gia_tri.casefold())','RE_TOKEN.match(gia_tri)'),('token_no_whitespace',r'\s*([a-z_]+)',r'([a-z_]+)'),('key_no_casefold','str(k).casefold()','str(k)'),('key_alpha_only','if c.isalnum()','if c.isalpha()'),('token_expand', '"passed", "measured", "not_measured"','"passed", "measured", "pass", "not_measured"')]
for name,a,b in repls:
 assert src.count(a)==1,(name,src.count(a));add(name,src.replace(a,b), 'regex_or_set',src[:src.index(a)].count('\n')+1)
# Every punctuation admitted by TOKEN grammar, and all closed job state alternatives.
for token in ('—',r'\-',':','(',',','.',';'):
 old=r'(?=$|[\s—\-:(,.;])';new=old.replace('[\\s—\\-:(,.;]', '[\\s—\\-:(,.;]'.replace(token,''));add('token_delimiter_'+str(ord(token[-1])),src.replace(old,new),'regex',37)
# Swap independent fixed waiver conditions, preserve code and force priority tests.
start=src.index('    if "ubuntu-latest" not in m[2].split(","):');end=src.index('    return []',start)
a=src[start:end];split=a.index('    if (m[1]');add('waiver_order_os_sha',src[:start]+a[split:]+a[:split]+src[end:],'order',260)
(w/'independent_mutants.jsonl').write_text(''.join(json.dumps(m,ensure_ascii=False)+'\n' for m in out));print(len(out))
