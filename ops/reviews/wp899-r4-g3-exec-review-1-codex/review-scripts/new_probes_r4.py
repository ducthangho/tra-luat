import sys, pathlib, importlib.util,json,copy,os
import yaml
R=pathlib.Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('t4',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
m=t.nap(); result={};x=t.X

def probe(label,w=None,rows=None,mut=None,ten='j'):
 w=w or t.wf_tu(x);rows=rows or t.buoc(x,'THU: 4/4 dat')
 try:
  p=t.g1(w,rows,sua=mut,ten=ten);result[label]={'gate':t.gate(p),'checkout':t.co(p)}
 except Exception as e:result[label]={'exception':type(e).__name__,'message':str(e)}
 return result[label]
probe('control')
# Each probe holds the workflow fixed; mutate only log/REST evidence.
for label,v in [('absent_start',None),('fraction_start',t.T),('offset_start','2026-10-19T23:45:04+00:00'),('bad_date_start','2026-02-30T00:00:00Z'),('bad_hour_start','2026-10-19T99:00:00Z')]:
 probe(label,mut=lambda st,v=v:st[2].update(started_at=v))
for label,fn in [('duplicate_number',lambda st:st[2].update(number=st[1]['number'])),('missing_number',lambda st:st[2].pop('number')),('bool_number',lambda st:st[2].update(number=True)),('unordered_list',lambda st:st.reverse()),('skipped_between',None)]:
 if fn:probe(label,mut=fn)
for label,when in [('bad_day','2026-02-30T23:45:04'),('bad_month','2026-13-19T23:45:04'),('bad_hour','2026-10-19T99:45:04'),('bad_minute','2026-10-19T23:99:04'),('bad_second','2026-10-19T23:45:99'),('year_zero','0000-10-19T23:45:04')]:
 rows=[r.replace(t.T,when+'.8553236Z') for r in t.buoc(x,'THU: 4/4 dat')]
 probe(label,rows=rows,mut=lambda st,when=when:st[2].update(started_at=when+'Z',completed_at=when+'Z'))
probe('missing_header_time',rows=[r.replace(t.T+' ','',1) if '##[group]Run' in r else r for r in t.buoc(x,'THU: 4/4 dat')])
probe('empty_run_first_line',w=t.wf_tu('\n'+x),rows=t.khoi(['',x],'THU: 4/4 dat'))
for label,v in [('name_number',7),('name_null',None),('name_expression','${{ matrix.step }}')]:probe(label,w=t.wf_tu(x,buoc_them={'name':v}))
w=yaml.safe_load(t.wf_tu(x)); w['jobs']['other']={'name':'${{ matrix.name }}','steps':[{'run':x}]};probe('other_job_expression',w=yaml.safe_dump(w))
for label,position in [('skipped_before',1),('skipped_between_two',2)]:
 w=t.wf_tu(x,x); lg=t.log_voi(t.buoc(x,'THU: 4/4 dat'));st=t.buoc_rest(lg,w); st[2 if position==1 else 3]['conclusion']='skipped'
 p=t.chay([(t.job(1,steps=st),lg)],wf=w)[2];result[label]={'gate':t.gate(p)}
for custom in ('Set up job','Post Test'):
 probe('reserved_'+custom,w=t.wf_tu(x,buoc_them={'name':custom}))
probe('continue_on_error',w=t.wf_tu(x,buoc_them={'continue-on-error':True}),rows=t.buoc(x,'THU: 3/4 dat'))
# Q6 inside versus outside the metadata group.
b=t.buoc(x,'THU: 4/4 dat')
probe('nested_before_shell',rows=[*b[:2],t.T+' ##[group]details',*b[2:]])
probe('nested_after_shell',rows=[*b[:3],t.T+' ##[group]details',*b[3:]])
probe('nested_in_output',rows=[*b[:4],t.T+' ##[group]details',b[4],t.T+' ##[endgroup]'])
# Both composite mechanisms with REST steps having number/name/window and matching metadata.
for outer in (True,False):
 for follow in (False,True):
  w=yaml.safe_load(t.wf_job(j=({},None),k=({'if':False},None)))
  w['jobs']['j']['steps'][1:] = [{'uses':'./c'}]+([{'run':x+'\n'}] if follow else [])
  groups=([[t.T+' ##[group]Run ./c',t.T+' ##[endgroup]']] if outer else [])+[t.buoc(x,'THU: 4/4 dat')]+([t.buoc(x,'THU: 3/4 dat')] if follow else [])
  p=t.g1(yaml.safe_dump(w),*groups)
  result[f'composite_outer{outer}_follow{follow}']={'gate':t.gate(p)}
(R/'new-r4-probes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
for k,v in result.items():
 g=v.get('gate',{});print(k,v.get('exception',''),g.get('ghep_buoc'),g.get('trang_thai'),g.get('dau_duong'))
