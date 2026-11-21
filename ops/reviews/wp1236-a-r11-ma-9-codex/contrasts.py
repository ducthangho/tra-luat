from review_common import *
from table_replay import TABLE,replay
import tempfile, yaml, copy, functools, re
# Cache SafeLoader results only; no parser semantics change, deepcopy isolates tests.
orig=yaml.safe_load
@functools.lru_cache(maxsize=4096)
def cached(x):return orig(x)
yaml.safe_load=lambda x:copy.deepcopy(cached(x)) if isinstance(x,(str,bytes)) else orig(x)
s=load(R/'ops/gate_output_doi_chieu_test.py','contrast_suite');g=s.G()
pool=[json.loads(x) for x in (W/'kho_dot_bien_reviewer_luot9.jsonl').read_text().splitlines()]
def uni(x):return ''.join(chr(ord(c)+0xFEE0) if '0'<=c<='9' else c for c in x)
def fixture_contrast(m,kind):
 fx='T-v3-pass';f=TABLE['hat_giong']['fixture'][fx];txt=(R/f['tep']).read_text();prov=yaml.safe_load((R/f['provenance']).read_bytes())
 t=txt
 if kind in ('header_run','header_attempt'):
  a=0 if kind=='header_run' else 1
  h=t.splitlines()[0];matches=list(re.finditer(r'\d+',h));mm=matches[a];new=h[:mm.start()]+uni(mm[0])+h[mm.end():];t=t.replace(h,new,1)
 elif kind=='job_id':
  mm=re.search(r'JOB (\d+)',t);t=t[:mm.start(1)]+uni(mm[1])+t[mm.end(1):]
 elif kind in ('moc_numerator','moc_denominator'):
  mm=re.search(r'MOC_GATE_OUTPUT: \w+ \((\d+)/(\d+) ',t);a=1 if kind=='moc_numerator' else 2;t=t[:mm.start(a)]+uni(mm[a])+t[mm.end(a):]
 elif kind in ('skip_old','skip_new'):
  fx='T-v2-pass' if kind=='skip_old' else 'T-v3-pass'
  t=(R/s.FX[fx][0]).read_text();prov=yaml.safe_load((R/s.FX[fx][1]).read_bytes());total=next(x for x in t.splitlines() if x.startswith('MOC_GATE_OUTPUT'))
  if kind=='skip_new':total='MOC_GATE_OUTPUT: not_measured (39/40 job co dau hieu duong)'
  ft,fp=s._them_skip('cu' if kind=='skip_old' else 'v3',total);t=ft(t);fp(prov)
  mm=next(re.finditer(r'JOB (\d+) [^\n]+: skipped',t));t=t[:mm.start(1)]+uni(mm[1])+t[mm.end(1):]
 elif kind=='event_tab':prov['moc']['run']['event']='push\t'
 elif kind=='name_inner_spaces':
  q=next(q for q in prov['moc']['gate_output']['jobs'] if q['job_id']==s.JOB_V3);q['name']=q['name'].replace(' ','  ',1)
 elif kind=='schema_case':prov['schema']=prov['schema'].swapcase()
 elif kind=='log_nfkc':
  k=s.JOB_V3;h=prov['log_day_du'][k]['sha256'];prov['log_day_du'][k]['sha256']=s._fw(h)
 with tempfile.TemporaryDirectory() as td:
  root=pathlib.Path(td);p=root/'danh-gia-gate-output-1.txt';p.write_text(t);(root/'p.yaml').write_text(yaml.safe_dump(prov,allow_unicode=True,sort_keys=False));doc={'moc_gate_output':'measured — '+p.name}
  return {'leaf':g.kiem_tep(p,root),'consumer':g.kiem_ho_so(doc,root)},{'leaf':m.kiem_tep(p,root),'consumer':m.kiem_ho_so(doc,root)}
def other_contrast(m,kind):
 with tempfile.TemporaryDirectory() as td:
  root=pathlib.Path(td)
  if kind=='landed':
   doc={'landed_'+uni('20261120'):{'landed':True}}
   return {'leaf':g.la_landed(doc),'consumer':g.kiem_ho_so(doc,root)},{'leaf':m.la_landed(doc),'consumer':m.kiem_ho_so(doc,root)}
  if kind in ('token_leading','token_separator'):
   claim='\tpassed' if kind=='token_leading' else 'passed\ttext'
   return {'leaf':g.token(claim),'consumer':g.kiem_ho_so({'gate_output':claim},root)},{'leaf':m.token(claim),'consumer':m.kiem_ho_so({'gate_output':claim},root)}
  if kind=='reason_spaces':
   h=TABLE['hat_giong']['mien'];d=copy.deepcopy(h['readback']);d['body']=re.sub(r'ly_do=.*? han=', 'ly_do=kiem thu hai tu han=',h['dong']);(root/h['ten_readback']).write_text(json.dumps(d));claim=h['loi_khai'].format(url=h['url'],sha=h['sha'])
   return {'leaf':g.kiem_mien(claim,root,None),'consumer':g.kiem_ho_so({'gate_output':claim},root)},{'leaf':m.kiem_mien(claim,root,None),'consumer':m.kiem_ho_so({'gate_output':claim},root)}
reports=json.loads((W/'independent_contrasts.json').read_text()) if (W/'independent_contrasts.json').exists() else []
for d in pool:
 if d['id'] in {x['id'] for x in reports}:continue
 m=load(W/'mutants_new'/f"{d['id']}.py",d['id'])
 kind=d['witness'];a,b=other_contrast(m,kind) if kind in ('landed','token_leading','token_separator','reason_spaces') else fixture_contrast(m,kind)
 assert a!=b,(d['id'],a,b)
 differentiators=[];baseline_errors=[]
 for o in TABLE['o']:
  la,hs=replay(g,o)
  if la!=o['la'] or hs!=o['ho_so']:baseline_errors.append(o['id'])
  lm,hm=replay(m,o)
  if (lm,hm)!=(la,hs):differentiators.append(o['id'])
 assert not baseline_errors
 z=dict(id=d['id'],witness=kind,original=a,mutant=b,differentiating_cells=differentiators,classification=d['classification_if_survives'])
 if z['classification']=='pending_law6':z['classification']='law6_P2' if differentiators else 'ngoai_bang_dong_P3'
 reports.append(z);save('independent_contrasts.json',reports)
 print(d['id'],z['classification'],len(differentiators),flush=True)
print('HOAN_TAT_CONTRAST15',flush=True)
