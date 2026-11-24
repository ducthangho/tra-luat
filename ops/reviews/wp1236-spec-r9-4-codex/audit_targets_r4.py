import ast,copy,hashlib,json,pathlib,re,sys,yaml
R=pathlib.Path.cwd(); W=R.parent/'work'; S=R/'ops/reviews/wp1236-r9-soan'
sys.dont_write_bytecode=True; sys.path[:0]=[str(S),str(R/'ops')]
import thamchieu as t
n={'__file__':str(S/'do_loi_khai.py')}; exec(compile((S/'do_loi_khai.py').read_text().split('root = Path(sys.argv[1]);')[0],str(S/'do_loi_khai.py'),'exec'),n)
out={}
# Contract input variants drawn by reducing copies of the real landed records.
root_record=yaml.safe_load((R/'ops/land/pr1378-wp1319-land-evidence.yaml').read_bytes())
block_record=yaml.safe_load((R/'ops/land/pr1055-wp1052-land-evidence.yaml').read_bytes())
cases={'root':root_record,'dated':block_record,'false':dict(root_record,landed=False)}
wrapped=copy.deepcopy(root_record); wrapped['trang_thai_packet']={'landed':True}; cases['wrapped']=wrapped
out['landed_shapes']={k:n['la_landed'](v) for k,v in cases.items()}
out['positive_claim_contract']={}
for k,v in cases.items():
 # Remove all structured gateoutput claims in a copy; remaining prose is not the trigger.
 def remove(obj):
  if isinstance(obj,dict): return {key:remove(val) for key,val in obj.items() if 'gateoutput' not in n['chuan'](str(key))}
  if isinstance(obj,list): return [remove(x) for x in obj]
  return obj
 doc=remove(v); out['positive_claim_contract'][k]={'landed':n['la_landed'](doc),'claim_count':len(list(n['loi_khai'](doc))),'required_landed_error':n['la_landed'](doc)}
# m50 equivalent scoped to empty checkout, four tests plus healthy control.
d=W/'fixtures/parser'; p=d/'danh-gia-gate-output-44669622916.txt'; q,orig=t.tim_prov(d)[0]
src=(S/'thamchieu.py').read_text(); mutant=src.replace('for c in y["moc"].get("checkout") or [None]','for c in y["moc"].get("checkout") or []')
assert mutant!=src
m={'__name__':'m50','__file__':str(S/'thamchieu.py')}; exec(compile(mutant,'m50','exec'),m)
out['m50']={}
for tag in ['healthy','a','b','c','d']:
 v=copy.deepcopy(orig)
 if tag=='a':v['moc']['run']['trang_thai']='not_measured'
 if tag=='b':v['moc']['gate_output']['tap_jobs']['trang_thai']='failed'
 if tag=='c':v['moc']['checkout'][0]['trang_thai']='not_measured'
 if tag=='d':v['moc']['checkout']=[]
 q.write_text(yaml.safe_dump(v,sort_keys=False,allow_unicode=True));out['m50'][tag]={'base':t.kiem_tep(p,d),'mutant':m['kiem_tep'](p,d)}
q.write_text(yaml.safe_dump(orig,sort_keys=False,allow_unicode=True))
# Verify the extraction prescription for the inherited CHECK_BAT_BUOC constant.
a=ast.parse((R/'.claude/dev/packet_loop.py').read_text()); node=next(n for n in a.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='CHECK_BAT_BUOC' for x in n.targets))
jobs=eval(compile(ast.Expression(node.value),'<ast-check>','eval'),{'__builtins__':{'tuple':tuple}})
out['required_jobs']={'count':len(jobs),'names':[x[1] for x in jobs],'matches_reference':set(x[1] for x in jobs)==set(t.CHECK_BAT_BUOC)}
# Verify post-M8 consequences from immutable supplied local data.
ms=sorted((R/'ops/land').glob('*/bien-ban-m8*.yaml')); out['m8']={'files':len(ms),'with_run_attempt':0,'waived':[],'descendant_cases':[]}
for f in ms:
 bb=yaml.safe_load(f.read_bytes())
 if not isinstance(bb,dict):continue
 if 'run_attempt' in (bb.get('ci_master') or {}):out['m8']['with_run_attempt']+=1
 if (bb.get('moc_10_2_2') or {}).get('gate_output')=='owner_waived':
  out['m8']['waived'].append(str(f.relative_to(R)))
 if f.parent.name.startswith(('pr1392-','pr1406-','pr1415-')):
  out['m8']['descendant_cases'].append({'file':str(f.relative_to(R)),'merge':bb.get('merge_commit'),'ci_master':bb.get('ci_master')})
(W/'audit_targets_r4.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2)); print('TARGETS_R4_COMPLETE')
