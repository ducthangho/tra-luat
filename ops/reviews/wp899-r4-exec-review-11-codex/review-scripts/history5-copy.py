from pathlib import Path
import sys,importlib.util,json,yaml
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
def dd(p):return [(x['trang_thai'],x.get('ly_do')) for x in t.gate(p)['dau_duong']]
def assertp(p,expected,gh='passed'):
 t.bang(t.ghep(p)==gh and dd(p)==expected,f'gh={t.ghep(p)} marker={dd(p)} expected={gh,expected}')
 return t.gate(p)
def case(label):
 b=t.buoc(t.X,'THU: 4/4 dat');ok=[('passed',None)]
 if label in ('wf_env_dict_only','wf_env_nonempty_only'):
  v='${{ fromJSON(needs.setup.outputs.env) }}' if label=='wf_env_dict_only' else []
  return assertp(t.g1(t.wf_tu(t.X,goc_them={'env':v}),b),t.CHAN)
 if label in ('job_env_only_first_key','job_env_only_last_key','env_prefix_value_only'):
  env={'A':'1','CI_DANG_KY_X':'1'} if label=='job_env_only_first_key' else {'CI_DANG_KY_X':'1','Z':'1'}
  if label=='env_prefix_value_only':env={'CI_DANG_KY_X':''}
  return assertp(t.g1(t.wf_tu(t.X,job_them={'env':env}),b),t.CHAN)
 if label in ('env_false_accept','env_int_accept','env_empty_str_accept'):
  env={'env_false_accept':False,'env_int_accept':0,'env_empty_str_accept':''}[label]
  return assertp(t.g1(t.wf_tu(t.X,job_them={'env':env}),b),t.CHAN)
 if label in ('mode_last_step','mode_first_run_step'):
  w=yaml.safe_load(t.wf_tu(t.X,t.X));w['jobs']['j']['steps'][1 if label=='mode_last_step' else 2]['env']={'A':'1'}
  p=t.g1(yaml.safe_dump(w),b,b)
  return assertp(p,t.CHAN+ok if label=='mode_last_step' else ok+t.CHAN)
 if label in ('mode_first_job','dd_first_job'):
  if label=='mode_first_job':w=t.wf_job(a=({'env':{'CI_DANG_KY_X':'1'}},None),z=({},None));expected=ok
  else:w=t.wf_job(a=({}, {'run':'python ops/other.py\n'}),z=({},None));expected=ok
  return assertp(t.g1(w,b,ten='z'),expected)
 if label=='job_match_exact_preference':
  w=t.wf_job(j=({},None),z=({'name':'j'},None));return assertp(t.g1(w,b),[], 'd_job_yaml_khong_duy_nhat')
 if label=='job_first_prefix_only':
  alias='Release '+'component '*12;w=t.wf_job(j=({'name':alias},None));return assertp(t.g1(w,b,ten=alias),ok)
 if label=='rest_sort_lexical':
  return assertp(t.g1(t.wf_tu(t.X),b,sua=lambda st:[v.update(number=n) for v,n in zip(st,[1,2,10,11,12])]),ok)
 if label=='rest_number_integral_float':
  return assertp(t.g1(t.wf_tu(t.X),b,sua=lambda st:st[2].update(number=3.0)),[],'steps_rest_sai_dang')
 if label=='ghep_zero_groups_reject':
  w=t.wf_tu(t.X);return assertp(t.g1(w,sua=lambda st:[v.update(conclusion='skipped') for v in st if v['name'] not in ('Set up job','Complete job') and not v['name'].startswith('Post ')],nen=t.LINUX_KHONG_SETUP),[])
 if label in ('time_only_first_group','time_only_last_group','time_name_first_key','time_name_last_key'):
  w=t.wf_tu(t.X,t.X);which=3 if label in ('time_only_first_group','time_name_last_key') else 1
  change={'started_at':'2026-10-19T23:45:05Z','completed_at':'2026-10-19T23:45:06Z'} if label!='time_name_last_key' else {'started_at':'2026-10-19T23:45:03Z','completed_at':'2026-10-19T23:45:03Z'}
  if label=='time_name_first_key':which=3;change={'started_at':'2026-10-19T23:45:05Z','completed_at':'2026-10-19T23:45:06Z'}
  if label=='time_name_last_key':which=2
  return assertp(t.g1(w,b,b,sua=lambda st:st[which].update(change)),[],'c_gio_header_ngoai_cua_so')
 if label in ('name_skip_first_yaml','name_skip_last_yaml'):
  idx=1 if label=='name_skip_first_yaml' else 2
  return assertp(t.g1(t.wf_tu(t.X),b,sua=lambda st:st[idx].update(name='A different name')),[],'b_ten_buoc_lech')
 if label=='prior_run_only_strings':
  e='echo GITHUB_ENV';w=yaml.safe_load(t.wf_tu(e,t.X));w['jobs']['j']['steps'][1]={'name':'Before','run':['GITHUB_ENV']}
  return assertp(t.g1(yaml.safe_dump(w),t.buoc(e),b,w_rest=t.wf_tu(e,t.X),sua=lambda st:st[2].update(name='Before')),t.CHAN)
 if label=='prior_path_suffix':
  e='echo GITHUB_PATH here';return assertp(t.g1(t.wf_tu(e,t.X),t.buoc(e),b),t.CHAN)
 if label=='prior_env_word_boundary':
  e='echo BEFORE_GITHUB_ENV_AFTER';return assertp(t.g1(t.wf_tu(e,t.X),t.buoc(e),b),t.CHAN)
 if label=='run_trailing_lf_exact':
  w=t.wf_tu(t.X,buoc_them={'run':t.X+'\n\n'});return assertp(t.g1(w,b),ok)
 if label=='run_blank_tail_only':
  return assertp(t.g1(t.wf_tu(t.X),t.khoi([t.X,''],'THU: 4/4 dat')),[])
 if label=='header_colored_exact':
  b[1]=b[1].replace('\x1b[0m','');return assertp(t.g1(t.wf_tu(t.X),b),ok)
 if label=='minimal_reverse_lines':
  y='python ops/other.py';w=t.wf_tu(t.X+'\n'+y)
  return assertp(t.g1(w,t.khoi([t.X,y],'THU: 4/4 dat')),ok+[('not_measured','khong_co_trong_MOI')])
 if label=='name_uses_strip':
  w=yaml.safe_load(t.wf_tu(t.X));w['jobs']['j']['steps'][1]={'uses':' ./a '}
  p=t.g1(yaml.safe_dump(w),b,w_rest=t.wf_tu(t.X),sua=lambda st:st[2].update(name='Run  ./a '))
  return assertp(p,[])
 if label=='name_run_prefer_uses':
  return assertp(t.g1(t.wf_tu(t.X,buoc_them={'uses':'./a'}),b),[])
 raise KeyError(label)
if __name__=='__main__':
 label=sys.argv[1]
 try:g=case(label)
 except t.TinHieuChotCa as e:print('DO:'+label+':'+str(e));sys.exit(3)
 except Exception as e:print('HONG:'+label+':'+type(e).__name__+':'+str(e));sys.exit(4)
 print('DAT:'+label+':'+json.dumps(g,ensure_ascii=False))
