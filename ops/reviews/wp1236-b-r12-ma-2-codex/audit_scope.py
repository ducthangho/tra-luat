from pathlib import Path
import importlib.util,json,re,collections,contextlib,io
R=Path.cwd();W=R.parent/'work'
s=importlib.util.spec_from_file_location('t',R/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[]; current=''; orig=t.chay

def traced(hs,prov=None,**kw):
 rc,out=orig(hs,prov,**kw)
 rows.append({'case':current,'doc':json.loads(hs) if hs.startswith('{') else hs,'prov':prov,'rc':rc,'l8':t.dong_l8(out)})
 return rc,out

t.chay=traced
results={}
for name in t.CA:
 if name.startswith(('c27_','c32_','c34_','c35_')):
  current=name; results[name]=t.chay_ca(name)
assert all(x[0]==0 for x in results.values())
(W/'scope-observed.json').write_text(json.dumps(rows,ensure_ascii=True,indent=2))
# Each field is classified by the test input, never by the product's answer.
waivers=[json.loads(v) for row in rows if row['case'].startswith('c34_') for k,v in (row['prov'] or {}).items() if k.endswith('.json') and v!='{']
ly_do={re.search(r'ly_do=(.*?) han=',d.get('body','')).group(1) for d in waivers if re.search(r'ly_do=(.*?) han=',d.get('body',''))}
claims=[row['doc']['a'][0]['Gate-Output'] for row in rows if row['case'].startswith('c32_') and isinstance(row['doc'],dict) and 'a' in row['doc']]
summary={'case_results':results,'cells':len(rows),'waiver_ly_do_values':sorted(ly_do),'waiver_body_non_ascii':sorted({ord(c) for d in waivers for c in d.get('body','') if ord(c)>127}),'token_non_ascii':sorted({ord(c) for v in claims if isinstance(v,str) for c in v if ord(c)>127}),'grammar_cells':sum(row['case'].startswith('c35_') for row in rows),'raw_byte_fixtures':0,'raw_byte_reason':'All c35 fixtures are str passed to cay.write_text(encoding=utf-8); no write_bytes path in c35.'}
(W/'scope-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
