from pathlib import Path
import importlib.util,json,yaml
R=Path.cwd();W=R.parent/'work'
s=importlib.util.spec_from_file_location('t',R/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[]
def ck(label,doc,prov,rc=0,ly=(),raw=None):
 with t.cay(json.dumps(doc),prov,doi_chieu=t.DOI_CHIEU) as goc:
  if raw is not None:(goc/'ops/land'/t.PROV/t.DG).write_bytes(raw)
  actual,out=t.kiem(t.nap(),goc)
 got=t.dong_l8(out);ok=(actual,got)==(rc,list(ly))
 rows.append({'label':label,'expected_rc':rc,'actual_rc':actual,'expected':list(ly),'actual':got,'passed':ok})
 print(label,actual,got,'PASS' if ok else 'FAIL',flush=True)

# Closed grammar: expected literal token semantics are copied from SPEC, not from product regexes.
for value,good in [('ſkipped',True),('sKipped',True),('\u00a0skipped',False),('skipped\u2003x',False),('skipped𐐀',False)]:
 ck('token '+ascii(value),{'gate_output':value},None,0 if good else 1,[] if good else ['$.gate_output: dinh_dang_loi_khai'])
url=t.URL8;sha=t.SHA8;rb='readback-review-issuecomment-123.json';claim=f'owner_waived — {url} {sha}'
for label,reason,why in [('control','fixture',''),('empty','','dong_mien'),('space',' fixture','dong_mien'),('tab','\tfixture','dong_mien'),('LF','x\ny','dong_mien'),('splitlines','x\u2028y','dong_mien'),('non-BMP','𐐀',''),('surrogate','\ud800',''),('embedded-han','x han=2025-01-01 more','')]:
 body=f'mien_gate_output: {sha} os=ubuntu-latest ly_do={reason} han=2026-12-31'
 ck('waiver reason '+label,{'gate_output':claim},{rb:json.dumps({'html_url':url,'user':{'login':'ducthangho'},'author_association':'OWNER','body':body})},1 if why else 0,[f'$.gate_output: waiver_khong_co_can_cu:{why}'] if why else [])
p=t.prov_that();text=p[t.DG];doc={'gate_output':'measured — '+t.DG}
def dg(label,new,why='',pv=None,raw=None):
 ck(label,doc,(pv or p)|{t.DG:new},1 if why else 0,[f'$.gate_output: danh_gia_khong_passed:{t.DG}:not_measured:{why}'] if why else [],raw)
dg('UTF8 control',text)
dg('UTF8 invalid byte',text,'khong_phai_utf8',raw=b'\xff'+text.encode())
dg('header head hex length',text.replace(sha,sha[:-1],1),'dau_tep_sai')
dg('header Unicode Nd',text.replace('run 4','run ４',1),'dau_tep_sai')
job=next(x for x in text.splitlines() if x.startswith('JOB '));pre='JOB 136067207297 ';name='chuan-bi';tail=job[len(pre+name):]
dg('job empty name',text.replace(job,pre+tail.lstrip(),1),'dong_la')
dg('job forbidden label bracket',text.replace(job,job.replace(']',']]',1),1),'dong_la')
dg('job earliest matching suffix',text.replace(job,job+tail,1))
provkey='ci-provenance-44669622916/provenance.yaml'
for label,newname,newjob in [('job backtracks over nonmatching delimiter',name+' [khong khop]',pre+name+' [khong khop]'+tail),('job Unicode non-BMP',name+'𐐀',pre+name+'𐐀'+tail)]:
 q=yaml.safe_load(p[provkey]);next(j for j in q['moc']['gate_output']['jobs'] if j['job_id']==136067207297)['name']=newname
 dg(label,text.replace(job,newjob,1),pv=p|{provkey:yaml.safe_dump(q,allow_unicode=True)})
(W/'scope-probes.json').write_text(json.dumps(rows,ensure_ascii=True,indent=2)+'\n')
print('TOTAL',sum(r['passed'] for r in rows),'/',len(rows));assert all(r['passed'] for r in rows)
