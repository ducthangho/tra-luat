from pathlib import Path
import sys,importlib.util,json,collections,yaml
root=Path.cwd();R=root/'.review'
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rd=t.random.Random(899);rows=[];cs=collections.Counter();markers=collections.Counter();max_alias=0;non_ascii=0;skipped_missing=0
for n in range(250):
 w,ten,st,lg,them,gh,expect=t.kich_ban(rd,n);wf=yaml.safe_load(w)
 cs[gh]+=1
 for v in expect or []:markers[v[0]+('/'+v[1] if v[1] else '')]+=1
 for j in wf['jobs'].values():
  if 'name' in j:max_alias=max(max_alias,len(j['name']))
 if any(ord(c)>127 for c in ten):non_ascii+=1
 skipped_missing+=sum(x.get('conclusion')=='skipped' and (x.get('started_at') is None or x.get('completed_at') is None) for x in st)
 rows.append({'scenario':n,'rest_name':ten,'expected_ghep':gh,'marker_count':len(expect or []),'rest_numbers':[x['number'] for x in st]})
d={'scenarios':250,'ghep':dict(cs),'markers':dict(markers),'max_yaml_job_alias_length':max_alias,'non_ascii_rest_names':non_ascii,'skipped_steps_with_missing_times':skipped_missing,'rows':rows}
(R/'generator6-results.json').write_text(json.dumps(d,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in d.items() if k!='rows'},ensure_ascii=False,indent=2))
