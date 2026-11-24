import sys,pathlib,json,importlib.util,subprocess,ast,difflib,collections
R=pathlib.Path(__file__).resolve().parent.parent/'repo';W=R.parent/'work';sys.path.insert(0,str(R/'.claude/dev'));import packet_loop_test as T
out=[]
# Reuse an existing legal path fixture; no new link/traversal payloads are authored.
p=W/'more';p.mkdir(exist_ok=True);c=T.Ctx(T.CANONICAL,p);x=T._d1106_kho(c,o=T._d2b_cay)
for label,change in [('C5c',T._NG(tep='ops/khac/pr1440-wp1319-provenance/'+T._D2B_F)),('newline_diagnostic',T._NG(tep='ops/land/dong\nmoi-provenance/'+T._D2B_F))]:
 rc,o,e=T._d1106_chay(c,x,change);out.append(dict(label=label,rc=rc,stdout=o.decode(),stderr=e.decode()))
# Measure declared mC11's exact downstream behavior, and the outside-block import.
source=T.CANONICAL.read_text()
for label,pair in [('mC11',T.MUTANTS['d2b_mC11_bo_mode'][:2]),('outside_import',('import tarfile\n',''))]:
 d=W/'more'/label;d.mkdir(exist_ok=True);assert source.count(pair[0])==1
 script=d/'packet_loop.py';script.write_text(source.replace(*pair),encoding='utf-8');(d/'launcher.py').write_bytes((T.HERE/'launcher.py').read_bytes())
 c2=T.Ctx(script,d)
 if label=='mC11':
  rc,o,e=T._d1106_chay(c2,x,T._NG(tep=T._D2B_PROV+'/danh-gia-gate-output-1.txt'))
  out.append(dict(label=label,rc=rc,stdout=o.decode(),stderr=e.decode()))
 else:
  case='cong_d2b_c1_passed_dat';v=T.chay_suite(script,d/'tests',chi_chay={case})[case]
  out.append(dict(label=label,case=case,classification=T._phan_loai_giet(v),detail=str(v)))
# Ruff comparison: normalize diagnostic location and compare code/message/source, not just totals.
ruff={k:json.loads((W/f'ruff_{k}.json').read_text()) for k in ('base','head')}
canon=lambda v:collections.Counter((pathlib.Path(z['filename']).name,z['code'],z['message']) for z in v)
out.append(dict(label='ruff_delta',base_count=len(ruff['base']),head_count=len(ruff['head']),new=list((canon(ruff['head'])-canon(ruff['base'])).elements()),removed=list((canon(ruff['base'])-canon(ruff['head'])).elements()),version=subprocess.check_output([sys.executable,'-m','ruff','--version'],text=True).strip()))
# The only semantic classifier edit adds a disjoint name prefix. Exhaust all actual legacy target names and representative exception categories.
base=subprocess.check_output(['git','show','f602325:.claude/dev/packet_loop_test.py'],text=True)
def body(src):
 n=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='chay_suite');return ast.get_source_segment(src,n)
old=body(base);new=body(pathlib.Path(T.__file__).read_text())
out.append(dict(label='classifier_source_diff',diff='\n'.join(difflib.unified_diff(old.splitlines(),new.splitlines())),legacy_cases_outside_new_prefix=sum(not n.startswith('cong_d2b_') for n,_ in T.CASES)))
(W/'more.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
