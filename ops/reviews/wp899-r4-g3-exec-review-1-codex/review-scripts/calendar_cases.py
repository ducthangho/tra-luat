import pathlib,importlib.util,json,hashlib
R=pathlib.Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('t',R.parent/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
x=t.X;w=t.wf_tu(x);lg=t.log_voi(t.buoc(x,'THU: 4/4 dat'));baseline=t.buoc_rest(lg,w);rows=[]
for label,k,v in [('invalid_day_start','started_at','2026-02-30T00:00:00Z'),('invalid_month_end','completed_at','2026-13-19T00:00:00Z'),('invalid_hour_end','completed_at','2026-10-19T24:00:00Z'),('invalid_minute_end','completed_at','2026-10-19T23:99:00Z'),('invalid_second_end','completed_at','2026-10-19T23:45:99Z'),('year_zero_start','started_at','0000-10-19T23:45:04Z')]:
 st=[dict(s) for s in baseline];st[2][k]=v
 rc,stdout,p,_=t.chay([(t.job(1,steps=st),lg)],wf=w);g=t.gate(p)
 try:t.bang(g['ghep_buoc']['trang_thai']=='not_measured' and g['dau_duong']==[],'invalid timestamp must not authenticate '+str({k:v}))
 except t.TinHieuChotCa as e:case_rc,signal=3,'DO:'+label+':'+str(e)
 else:case_rc,signal=0,'DAT:'+label
 rows.append({'case':label,'change':{k:v},'case_rc':case_rc,'signal':signal,'tool_rc':rc,'stdout':stdout,'gate':g,'workflow_sha256':hashlib.sha256(w.encode()).hexdigest(),'log_sha256':hashlib.sha256(lg.encode()).hexdigest()})
(R/'calendar-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print([(r['case'],r['case_rc'],r['tool_rc'],r['gate']['ghep_buoc'],r['gate']['trang_thai']) for r in rows])
