from pathlib import Path
import importlib.util,sys,json,yaml
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t7',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
x=t.X

def eq(p,gh='passed',markers=[('passed',None)],lines=None,paths=None,count=None):
 g=t.gate(p);dd=[(z['trang_thai'],z.get('ly_do')) for z in g['dau_duong']]
 t.bang(t.ghep(p)==gh and dd==markers,f'ghep={t.ghep(p)} marker={dd}; expected={gh,markers}')
 if lines is not None:t.bang([z.get('dong_khop') for z in g['dau_duong']]==lines,f'dong_khop={g["dau_duong"]}; expected={lines}')
 if paths is not None:t.bang([z['duong_dan'] for z in g['dau_duong']]==paths,f'duong_dan={g["dau_duong"]}; expected={paths}')
 if count is not None:t.bang(g['kich_ban']['buoc_xac_thuc']==count,f'count={g["kich_ban"]}, expected={count}')

def call(w=None,bs=None,**kw):return t.g1(w if w is not None else t.wf_tu(x),*(bs if bs is not None else [t.buoc(x,'THU: 4/4 dat')]),**kw)

def time_case(stamp=t.T,change=None):
 b=[z.replace(t.T,stamp) for z in t.buoc(x,'THU: 4/4 dat')]
 return call(bs=[b],sua=(lambda st:st[2].update(change)) if change else None)

def probe(n):
 if n in ('job_key_equals_alias_reject','job_alias_matches_duplicate_count'):eq(call(t.wf_job(j=({'name':'j'},None))))
 elif n=='job_alias_suffix_only_key':eq(call(t.wf_job(j=({'name':'Build'},None)),ten='Build (linux, 5)'))
 elif n in ('job_suffix_no_dot','job_suffix_no_dot_pure'):eq(call(ten='j (ubuntu-24.04)'))
 elif n=='job_alias_unicode_reject':eq(call(t.wf_job(j=({'name':'Xây dựng'},None)),ten='Xây dựng'))
 elif n=='job_alias_trim':eq(call(t.wf_job(j=({'name':' Build '},None)),ten=' Build '))
 elif n=='name_explicit_strip':eq(call(t.wf_tu(x,buoc_them={'name':'  Build  '})))
 elif n=='name_explicit_unicode_reject':eq(call(t.wf_tu(x,buoc_them={'name':'Xây dựng'})))
 elif n=='name_uses_whole_value':
  # A value with a newline is not a valid action reference; spec does not say how a malformed uses value is treated.
  # The probe records current/alternative behavior without promoting it to a required behavior.
  w=yaml.safe_load(t.wf_tu(x));w['jobs']['j']['steps'][0]={'uses':'./a\n./b'}
  lg=t.log_voi(t.buoc(x,'THU: 4/4 dat')).replace('Run actions/setup-python@v5','Run ./a')
  p=t.chay([(t.job(1,steps=t.buoc_rest(lg,yaml.safe_dump(w))),lg)],wf=yaml.safe_dump(w))[2];eq(p)
 elif n=='name_run_empty_first_reject':eq(call(t.wf_tu('\n'+x)),markers=[])
 elif n in ('name_run_strip_cr','name_run_crlf_first_line'):
  # REST literal CR is independently supplied, not taken from the module under review.
  w=t.wf_tu(x,buoc_them={'run':'a\r\n'+x});p=call(w,sua=lambda st:st[2].update(name='Run a\r'));eq(p,markers=[])
 elif n in ('time_same_year','time_same_month','time_24h_window'):
  eq(time_case('2026-12-31T23:45:04.8553236Z',{'started_at':'2026-12-30T00:00:00Z','completed_at':'2027-01-02T00:00:00Z'}))
 elif n=='time_century_leap_reject':eq(time_case('2000-02-29T23:45:04.8553236Z'))
 elif n=='time_year_9999_reject':eq(time_case('9999-12-31T23:45:04.8553236Z'))
 elif n=='time_year_0001_reject':eq(time_case('0001-01-01T23:45:04.8553236Z'))
 elif n=='time_date_only_compare':eq(time_case(change={'started_at':'2026-10-19T23:45:05Z'}),gh='c_gio_header_ngoai_cua_so',markers=[])
 elif n=='time_clock_only_compare':eq(time_case(change={'started_at':'2026-10-20T23:45:04Z','completed_at':'2026-10-21T23:45:04Z'}),gh='c_gio_header_ngoai_cua_so',markers=[])
 elif n=='time_whitespace_strip':eq(time_case(change={'started_at':'2026-10-19T23:45:04Z '}),gh='c_gio_header_ngoai_cua_so',markers=[])
 elif n=='time_invalid_century_accept':eq(time_case('1900-03-01T23:45:04.8553236Z',{'started_at':'1900-02-29T23:45:04Z'}),gh='c_gio_header_ngoai_cua_so',markers=[])
 elif n in ('rest_number_no_gaps','rest_number_max_as_count'):eq(call(sua=lambda st:[z.update(number=z['number']*2) for z in st]))
 elif n=='rest_number_metadata_ignored_validation':eq(call(sua=lambda st:st[0].update(number=True)),gh='steps_rest_sai_dang',markers=[])
 elif n=='rest_metadata_time_required':eq(call(sua=lambda st:[z.update(started_at=None,completed_at=None) for z in st if z['name'] in ('Set up job','Complete job') or z['name'].startswith('Post ')]))
 elif n=='rest_filter_post_number_order':
  def change(st):
   p=next(s for s in st if s['name'].startswith('Post '));p['number']=1
   for z in st:
    if z is not p:z['number']+=1
  eq(call(sua=change))
 elif n in ('rest_filter_skipped_uses_only','rest_names_only_ran'):
  w=yaml.safe_load(t.wf_tu('echo skip',x));w['jobs']['j']['steps'][1]['if']='false'
  def change(st):
   st[2].update(conclusion='skipped')
   if n=='rest_names_only_ran':st[2]['name']='Run incorrect'
  eq(call(yaml.safe_dump(w),sua=change),gh='b_ten_buoc_lech' if n=='rest_names_only_ran' else 'passed',markers=[] if n=='rest_names_only_ran' else [('passed',None)])
 elif n=='mode_env_present_values_only':eq(call(t.wf_tu(x,job_them={'env':{'CI_DANG_KY_X':None}})),markers=t.CHAN)
 elif n=='mode_env_empty_key_reject':eq(call(t.wf_tu(x,job_them={'env':{'':'abc'}})))
 elif n=='mode_env_unicode_key_reject':eq(call(t.wf_tu(x,job_them={'env':{'VIỆT':'abc'}})))
 elif n=='mode_prior_skip_uses':
  # run + uses present on the previous step: run text is still the source specified for prior writes.
  w=yaml.safe_load(t.wf_tu('echo GITHUB_ENV',x));w['jobs']['j']['steps'][1]['uses']='./a'
  eq(call(yaml.safe_dump(w),[t.buoc('echo GITHUB_ENV'),t.buoc(x,'THU: 4/4 dat')]),markers=t.CHAN)
 elif n in ('mode_prior_skip_skipped','mode_prior_only_unblocked'):
  w=yaml.safe_load(t.wf_tu('echo GITHUB_ENV',x));w['jobs']['j']['steps'][1].update({'if':'false'} if n=='mode_prior_skip_skipped' else {'env':{}})
  bs=[t.buoc(x,'THU: 4/4 dat')] if n=='mode_prior_skip_skipped' else [t.buoc('echo GITHUB_ENV'),t.buoc(x,'THU: 4/4 dat')]
  eq(call(yaml.safe_dump(w),bs,sua=(lambda st:st[2].update(conclusion='skipped')) if n=='mode_prior_skip_skipped' else None),markers=t.CHAN)
 elif n=='mode_prior_strip_empty_run':
  # Equivalent on supported prior string run; values None/False/0 never contain the two source names either.
  eq(call())
 elif n=='mode_step_shell_nonempty':eq(call(t.wf_tu(x,buoc_them={'shell':None})),markers=t.CHAN)
 elif n in ('dd_first_match_lines_only','dd_last_match_lines_only','dd_sort_match_lines'):
  rows=['START','THU: 4/4 dat','END'];eq(call(bs=[t.buoc(x,*rows)],them={t.DUONG_GIA:r'^START\nTHU: (\d+)/(\d+) dat\nEND$'}),lines=[rows])
 elif n=='dd_blank_output_lines_remove':
  eq(call(bs=[t.buoc(x,'START','','THU: 4/4 dat','END')],them={t.DUONG_GIA:r'^START\n\nTHU: (\d+)/(\d+) dat\nEND$'}))
 elif n=='dd_no_output_final_newline':eq(call(them={t.DUONG_GIA:r'^THU: (\d+)/(\d+) dat\n\Z'}))
 elif n=='dd_dedup_output_lines':eq(call(bs=[t.buoc(x,'START','START','THU: 4/4 dat')],them={t.DUONG_GIA:r'^START\nSTART\nTHU: (\d+)/(\d+) dat$'}))
 elif n=='dd_sort_output_lines':eq(call(bs=[t.buoc(x,'START','THU: 4/4 dat','END')],them={t.DUONG_GIA:r'^START\nTHU: (\d+)/(\d+) dat\nEND$'}))
 elif n=='dd_wrong_lenh_first_call':
  p=call();g=t.gate(p);t.bang([z['lenh'] for z in g['dau_duong']]==[x],f'lenh={g["dau_duong"]}')
 elif n=='dd_truncate_path':eq(call(),paths=[t.DUONG_GIA])
 elif n=='dd_step_dedup_paths':eq(call(t.wf_tu(x,x),[t.buoc(x,'THU: 4/4 dat'),t.buoc(x,'THU: 3/4 dat')]),markers=[('passed',None),('failed',None)])
 elif n=='dd_validated_step_count_calls':eq(call(t.wf_tu('echo hi'),[t.buoc('echo hi')]),markers=[],count=1)
 elif n=='log_output_ignore_indented_blank':eq(call(bs=[t.buoc(x,'THU: 4/4 dat  ')]),markers=[('failed',None)])
 elif n=='log_header_strip':eq(call(t.wf_tu(x+'  '),[t.buoc(x+'  ','THU: 4/4 dat')]))
 elif n in ('log_empty_metadata_reject','log_second_shell_reject','log_require_metadata_no_ansi'):
  b=t.buoc(x,'THU: 4/4 dat');b.insert(3,t.T+' '+{'log_empty_metadata_reject':'','log_second_shell_reject':'shell: /other','log_require_metadata_no_ansi':'\x1b[31mNOTE\x1b[0m'}[n]);eq(call(bs=[b]))
 elif n=='log_output_drop_group_lines':eq(call(bs=[t.buoc(x,'##[group]details','THU: 4/4 dat')],them={t.DUONG_GIA:r'^##\[group\]details\nTHU: (\d+)/(\d+) dat$'}))
 elif n=='log_require_output_nonempty':eq(call(bs=[t.buoc(x)]),markers=[('failed',None)],count=1)
 elif n=='log_color_run_not_contains_shell':eq(call(t.wf_tu('shell: x'),[t.buoc('shell: x')]),markers=[],count=1)
 elif n=='log_header_full_timestamp_required':eq(call())
 elif n=='log_same_header_body_len_reject':eq(call(t.wf_tu(x+'\n'+x),[t.khoi([x,x],'THU: 4/4 dat')]))
 else:raise KeyError(n)

if __name__=='__main__':
 n=sys.argv[1]
 try:probe(n)
 except t.TinHieuChotCa as e:print('DO:'+n+':'+str(e));sys.exit(3)
 except Exception as e:print('HONG:'+n+':'+type(e).__name__+':'+str(e));sys.exit(4)
 print('DAT:'+n)
