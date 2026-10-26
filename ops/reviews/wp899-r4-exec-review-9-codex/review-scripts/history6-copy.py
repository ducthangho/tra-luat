from pathlib import Path
import importlib.util,sys,json,yaml
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t6',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
x=t.X;b=lambda:t.buoc(x,'THU: 4/4 dat')
def eq(p,gh='passed',markers=[('passed',None)]):
 g=t.gate(p);dd=[(z['trang_thai'],z.get('ly_do')) for z in g['dau_duong']]
 t.bang(t.ghep(p)==gh and dd==markers,f'ghep={t.ghep(p)} markers={dd}; expected={gh,markers}')
def call(w,bs=None,**kw):return t.g1(w,*(bs if bs is not None else [b()]),**kw)
def time_case(stamp='2024-02-29T23:45:04.8553236Z',change=None):
 bb=[z.replace(t.T,stamp) for z in b()]
 return call(t.wf_tu(x),[bb],sua=(lambda st:st[2].update(change)) if change else None)
def probe(name):
 if name in ('job_nested_parentheses','job_nested_suffix_pure'):eq(call(t.wf_tu(x),ten='j (ubuntu (64))'))
 elif name=='names_compare_as_strings':eq(call(t.wf_tu(x,buoc_them={'name':None}),sua=lambda st:st[2].update(name='None')),gh='b_ten_buoc_lech',markers=[])
 elif name=='job_ascii_suffix':eq(call(t.wf_tu(x),ten='j (Việt Nam)'))
 elif name=='job_one_suffix_item':eq(call(t.wf_tu(x),ten='j (a, b)'))
 elif name=='job_alias_truncate':eq(call(t.wf_job(j=({'name':'Build '+'a'*40},None)),ten='Build '+'a'*40))
 elif name=='job_requires_nonempty_steps':
  wf=yaml.safe_dump({'jobs':{'j':{'steps':[]}}});eq(call(wf,[],nen=t.LINUX_KHONG_SETUP),markers=[])
 elif name=='job_nonempty_rest_required':
  wf=yaml.safe_dump({'jobs':{'j':{'steps':[]}}});eq(t.chay([(t.job(1,steps=[]),t.LINUX_KHONG_SETUP)],wf=wf)[2],markers=[])
 elif name=='rest_number_under_100':eq(call(t.wf_tu(x),sua=lambda st:[s.update(number=s['number']+100) for s in st]))
 elif name in ('rest_number_order_contiguous','rest_number_min_one_safe'):eq(call(t.wf_tu(x),sua=lambda st:[s.update(number=s['number']+1) for s in st]))
 elif name=='rest_skipped_time_required':
  w=yaml.safe_load(t.wf_tu('echo skipped',x));w['jobs']['j']['steps'][1]['if']='false'
  eq(call(yaml.safe_dump(w),sua=lambda st:st[2].update(conclusion='skipped',started_at=None,completed_at=None)))
 elif name=='time_require_same_day':eq(time_case(t.T,{'started_at':'2026-10-18T23:45:04Z','completed_at':'2026-10-20T23:45:04Z'}))
 elif name in ('time_reject_leap_day','time_reject_leap_day_safe'):eq(time_case())
 elif name=='time_reject_year_before_2000':eq(time_case('1999-12-31T23:45:04.8553236Z'))
 elif name=='time_accept_invalid_leap_day':eq(time_case('2026-03-01T23:45:04.8553236Z',{'started_at':'2026-02-29T23:45:04Z'}),'c_gio_header_ngoai_cua_so',[])
 elif name in ('prior_entire_step_instead_run','prior_uses_preferred'):
  wf=yaml.safe_load(t.wf_tu(x));wf['jobs']['j']['steps'][0]={'uses':'./GITHUB_PATH'}
  lg=t.log_voi(b()).replace('Run actions/setup-python@v5','Run ./GITHUB_PATH')
  st=t.buoc_rest(lg,yaml.safe_dump(wf));p=t.chay([(t.job(1,steps=st),lg)],wf=yaml.safe_dump(wf))[2];eq(p)
 elif name=='prior_ignore_if_empty_env':
  e='echo $GITHUB_ENV';w=yaml.safe_load(t.wf_tu(e,x));w['jobs']['j']['steps'][1]['env']={};eq(call(yaml.safe_dump(w),[t.buoc(e),b()]),markers=t.CHAN)
 elif name=='prior_only_last_two':eq(call(t.wf_tu('echo $GITHUB_ENV','echo x','echo y',x),[t.buoc('echo $GITHUB_ENV'),t.buoc('echo x'),t.buoc('echo y'),b()]),markers=t.CHAN)
 elif name=='log_first_output_line':eq(call(t.wf_tu(x),[t.buoc(x,'note before','THU: 4/4 dat')]))
 elif name=='log_last_output_line':eq(call(t.wf_tu(x),[t.buoc(x,'THU: 4/4 dat','note after')]))
 elif name=='log_output_strip':eq(call(t.wf_tu(x),[t.buoc(x,'  THU: 4/4 dat')]),markers=[('failed',None)])
 elif name=='log_reverse_output':
  # MOI can distinguish order with a multi-line regular expression; no shell interpretation.
  p=call(t.wf_tu(x),[t.buoc(x,'START','THU: 4/4 dat','END')],them={t.DUONG_GIA:r'^START\nTHU: (\d+)/(\d+) dat\nEND$'});eq(p)
 elif name in ('log_reject_metadata_after_shell','log_uncolored_metadata_add_to_echo'):
  bb=b();bb.insert(3,t.T+'   NOTE: harmless');eq(call(t.wf_tu(x),[bb]))
 elif name=='log_endgroup_need_shell_first':
  marker=t.nap().than(b()[3]);lines=[x,marker];p=call(t.wf_tu('\n'.join(lines)),[t.khoi(lines,'THU: 4/4 dat')]);t.bang(t.ghep(p)=='passed' and t.gate(p)['kich_ban']['buoc_xac_thuc']==0 and t.gate(p)['dau_duong']==[],str(t.gate(p)))
 elif name=='log_shell_nonempty':
  bb=b();bb[2]=t.T+' shell: ';eq(call(t.wf_tu(x),[bb]))
 elif name=='log_color_prefix_only':
  bb=b();bb[1]=t.T+' \x1b[0m\x1b[36;1m'+x+'\x1b[0m';eq(call(t.wf_tu(x),[bb]))
 elif name=='log_color_without_timestamp':
  bb=b();bb[1]='\x1b[36;1m'+x+'\x1b[0m';eq(call(t.wf_tu(x),[bb]))
 elif name=='run_blank_lines_disallowed':eq(call(t.wf_tu(x+'\n\n'+x),[t.khoi([x,'',x],'THU: 4/4 dat')]))
 elif name=='run_sort_calls':
  y='python ops/aaa.py';eq(call(t.wf_tu(x+'\n'+y),[t.khoi([x,y],'THU: 4/4 dat')],them={'ops/aaa.py':r'^THU: (\d+)/(\d+) dat$'}),markers=[('passed',None),('passed',None)])
 elif name=='rest_also_skip_null':
  p=call(t.wf_tu(x),sua=lambda st:st[2].update(conclusion=None));eq(p)
 elif name=='yaml_empty_workflow_reject':
  eq(call('jobs: {}',w_rest=t.wf_tu(x)),gh='d_job_yaml_khong_duy_nhat',markers=[])
 else:raise KeyError(name)
if __name__=='__main__':
 name=sys.argv[1]
 try:probe(name)
 except t.TinHieuChotCa as e:print('DO:'+name+':'+str(e));sys.exit(3)
 except Exception as e:print('HONG:'+name+':'+type(e).__name__+':'+str(e));sys.exit(4)
 print('DAT:'+name)
