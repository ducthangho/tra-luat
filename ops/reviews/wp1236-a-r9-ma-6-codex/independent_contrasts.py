import pathlib,json,importlib.util,sys,tempfile,shutil,copy,yaml
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo'
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(r/'ops/gate_output_doi_chieu_test.py','tests');g=load(r/'ops/gate_output_doi_chieu.py','prod'); variants={m['id']:m for m in map(json.loads,(w/'independent_mutants.jsonl').read_text().splitlines())};results=[]
mods=w/'contrast_modules';mods.mkdir(exist_ok=True)
def mutant(n):
 p=mods/(n+'.py');p.write_text(variants[n]['src']);return load(p,n)
def rec(n,original,changed):
 row={'id':n,'original':original,'mutant':changed,'different':original!=changed};results.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
for n in [x for x in variants if x.startswith('identity_219_')]+['landed_partial']:
 if n not in variants:continue
 m=mutant(n)
 for key in ['root','packet','block','suffix']:
  doc={'root':{'landed':1},'packet':{'trang_thai_packet':{'landed':1}},'block':{'landed_20261120':{'landed':1}},'suffix':{'landed_20261120_tail':{'landed':True}}}[key]
  rec(n+':'+key,g.kiem_ho_so(doc,w),m.kiem_ho_so(doc,w))
for n in ['waiver_partial','waiver_order_os_sha']:
 m=mutant(n)
 with tempfile.TemporaryDirectory() as d:
  d=pathlib.Path(d);rb=t.rb(t.DONG)
  if n=='waiver_partial':rb['body']+=' suffix'
  else:rb['body']=rb['body'].replace('ubuntu-latest','windows-latest').replace(t.SHA,'0'*40)
  (d/'readback-probe-issuecomment-123.json').write_text(json.dumps(rb));v=f'owner_waived — {t.URL} {t.SHA}'
  rec(n,g.kiem_mien(v,d,None),m.kiem_mien(v,d,None))
for n in ['ref_any_run','ref_txt_wild','token_expand','key_alpha_only']+[x for x in variants if x.startswith('token_delimiter_')]:
 m=mutant(n)
 with t.ho_so_tam() as d:
  ref=t.ten_tep('T-v3-pass');key='gate_output';value='measured — '+ref
  if n in ('ref_any_run','ref_txt_wild'):
   new=ref.replace('44669622916','a') if n=='ref_any_run' else ref.replace('.txt','Xtxt');shutil.copy(d/ref,d/new);value='measured — '+new
  if n=='token_expand':value='pass — '+ref
  if n=='key_alpha_only':key='gate1output';value='measured — missing.txt'
  if n.startswith('token_delimiter_'):value='passed'+chr(int(n.split('_')[-1]))+' '+ref
  doc={key:value};rec(n,g.kiem_ho_so(doc,d),m.kiem_ho_so(doc,d))
n='skip_v3_partial';m=mutant(n);ft,fp=t._them_skip('v3','MOC_GATE_OUTPUT: not_measured (39/40 job co dau hieu duong)')
with t.mini('T-v3-pass',lambda x:ft(x).replace('(khong suy pass)','(khong suy pass) suffix'),fp) as (f,d):rec(n,g.kiem_tep(f,d),m.kiem_tep(f,d))
(w/'independent_contrasts.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
