from pathlib import Path
import importlib.util,collections,json,yaml
r=Path('.review');s=importlib.util.spec_from_file_location('t',Path('ops/ci_provenance_test.py'));t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rd=t.random.Random(899);phu=collections.Counter();years=set();gaps=0;same_alias=0;alias_matrix=0;row=[]
for i in range(250):
 w,ten,st,lg,them,gh,mong=t.kich_ban(rd,i);wf=yaml.safe_load(w)
 ks=list(wf['jobs']);kk=ten.split(' (')[0]
 phu.update([f'ghep:{gh}']+[x[0] if x[1] is None else x[1] for x in mong or []]+['job_dich_khong_dau']*(ks.index(kk)>0 if kk in ks else 0)+['number>=10']*(max(x['number'] for x in st)>=10))
 ns=sorted(x['number'] for x in st);gaps+=any(b-a!=1 for a,b in zip(ns,ns[1:]))
 for k,j in wf['jobs'].items():same_alias+=j.get('name')==k;alias_matrix+=isinstance(j.get('name'),str) and ten.startswith(j['name']+' (')
 for x in st:
  if isinstance(x.get('started_at'),str):years.add(x['started_at'][:4])
row={'sample_counts':dict(phu),'sample_count_min':min(phu.values()),'number_sequences_with_gaps':gaps,'jobs_with_alias_equal_key':same_alias,'rest_names_with_matrix_on_alias':alias_matrix,'rest_time_years':sorted(years),'absence_of_generated_a_count_failures':'ghep:a_so_nhom_khac_so_buoc_rest_chay not generated; c36 separately measures count failures'}
(r/'coverage7-results.json').write_text(json.dumps(row,ensure_ascii=False,indent=2));print(json.dumps(row,ensure_ascii=False,indent=2))
