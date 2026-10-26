from pathlib import Path
import sys,importlib.util,json,yaml
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
LABELS=['job_escape_alias','job_alias_strip','job_casefold','name_explicit_strip','metadata_setup_prefix','metadata_complete_prefix','ran_neutral_excluded','ran_cancelled_excluded','env_prefix_empty_suffix','env_prefix_casefold','mode_step_key_truthy','mode_shell_strip','mode_shell_casefold','mode_prior_requires_ran','run_compare_strip_newlines','header_lstrip','shell_lstrip','number_contiguous']
def case(label):
 x=t.X;w=t.wf_tu(x);b=t.buoc(x,'THU: 4/4 dat');kw={};want='passed';reason=None;gh='passed'
 if label in ('job_escape_alias','job_alias_strip'):
  alias='Build (release)' if label=='job_escape_alias' else ' Build '
  v=yaml.safe_load(w);v['jobs']['j']['name']=alias;w=yaml.safe_dump(v);kw['ten']=alias
 elif label=='job_casefold':kw['ten']='J';want=None;gh='d_job_yaml_khong_duy_nhat'
 elif label=='name_explicit_strip':w=t.wf_tu(x,buoc_them={'name':' Kiem tra '})
 elif label=='metadata_setup_prefix':w=t.wf_tu(x,buoc_them={'name':'Set up job results'})
 elif label=='metadata_complete_prefix':w=t.wf_tu(x,buoc_them={'name':'Complete job results'})
 elif label=='ran_neutral_excluded':kw['sua']=lambda st:st[2].update(conclusion='neutral')
 elif label=='ran_cancelled_excluded':kw['sua']=lambda st:st[2].update(conclusion='cancelled')
 elif label=='env_prefix_empty_suffix':w=t.wf_tu(x,job_them={'env':{'CI_DANG_KY_':'1'}});want='not_measured';reason='che_do_khong_xac_dinh'
 elif label=='env_prefix_casefold':w=t.wf_tu(x,job_them={'env':{'ci_dang_ky_X':'1'}})
 elif label=='mode_step_key_truthy':w=t.wf_tu(x,buoc_them={'env':{}});want='not_measured';reason='che_do_khong_xac_dinh'
 elif label=='mode_shell_strip':w=t.wf_tu(x,buoc_them={'shell':' bash '});want='not_measured';reason='che_do_khong_xac_dinh'
 elif label=='mode_shell_casefold':w=t.wf_tu(x,buoc_them={'shell':'BASH'});want='not_measured';reason='che_do_khong_xac_dinh'
 elif label=='mode_prior_requires_ran':
  e='echo value >> $GITHUB_ENV';w=t.wf_tu(e,x);v=yaml.safe_load(w);v['jobs']['j']['steps'][1]['if']='false';w=yaml.safe_dump(v)
  p=t.g1(w,b,sua=lambda st:st[2].update(conclusion='skipped'))
  g=t.gate(p);t.bang(t.ghep(p)=='passed' and [(z['trang_thai'],z.get('ly_do')) for z in g['dau_duong']]==t.CHAN,str(g));return g
 elif label=='run_compare_strip_newlines':w=t.wf_tu('\n'+x);want=None
 elif label=='header_lstrip':b=[b[0].replace('##[group]Run ','##[group]Run  ')]+b[1:];want=None
 elif label=='shell_lstrip':b=[d.replace(' shell: ','  shell: ') for d in b];want=None
 elif label=='number_contiguous':kw['sua']=lambda st:[z.update(number=z['number']*2) for z in st]
 else:raise KeyError(label)
 p=t.g1(w,b,**kw);g=t.gate(p)
 t.bang(t.ghep(p)==gh,f'{label}: gh={t.ghep(p)} expected={gh}')
 observed=[(z['trang_thai'],z.get('ly_do')) for z in g['dau_duong']]
 t.bang(observed==([] if want is None else [(want,reason)]),f'{label}: markers={observed}, expected={want,reason}')
 return g
if __name__=='__main__':
 label=sys.argv[1]
 try:g=case(label)
 except t.TinHieuChotCa as e:print('DO:'+label+':'+str(e));sys.exit(3)
 except Exception as e:print('HONG:'+label+':'+type(e).__name__+':'+str(e));sys.exit(4)
 print('DAT:'+label+':'+json.dumps(g,ensure_ascii=False))
