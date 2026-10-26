from pathlib import Path
import sys,importlib.util,json,copy
import yaml
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
def calc(label):
 x=t.X;w=t.wf_tu(x);lg=t.buoc(x,'THU: 4/4 dat');kwargs={}
 expected='passed';marker='passed'
 if label=='nonstr_no_throw':
  w=t.wf_tu(x,buoc_them={'name':'K','run':5})
  try:p=t.g1(w,t.buoc('5','THU: 4/4 dat'),sua=lambda st:st[2].update(name='K'),w_rest=t.wf_tu(x))
  except Exception as e:t.bang(False,'non-string run must remain unverified without throwing: '+type(e).__name__)
  g=t.gate(p);t.bang(t.ghep(p)=='passed' and g['dau_duong']==[] and g['kich_ban']['buoc_xac_thuc']==0,str(g));return g
 elif label=='run_trailing_space':
  w=t.wf_tu(x+'  ');lg=t.buoc(x+'  ','THU: 4/4 dat')
 elif label=='metadata_post_infix':w=t.wf_tu(x,buoc_them={'name':'Check Post result'})
 elif label=='shell_prefix_space_missing':
  lg=[d.replace('shell: /usr','shell:/usr') for d in lg];marker=None
 elif label in ('defaults_job_empty','defaults_wf_empty'):
  w=t.wf_tu(x,**{'job_them' if label=='defaults_job_empty' else 'goc_them':{'defaults':{}}});marker='not_measured'
 elif label in ('env_job_false','env_wf_list'):
  w=t.wf_tu(x,**{'job_them' if label=='env_job_false' else 'goc_them':{'env':False if label=='env_job_false' else []}});marker='not_measured'
 elif label=='number_bool_metadata':kwargs['sua']=lambda st:st[0].update(number=True);expected='steps_rest_sai_dang';marker=None
 elif label=='number_float':kwargs['sua']=lambda st:st[2].update(number=3.0);expected='steps_rest_sai_dang';marker=None
 elif label=='job_alias_exact':
  ww=yaml.safe_load(w);ww['jobs']['j']['name']='Build';w=yaml.safe_dump(ww);kwargs['ten']='Build'
 elif label=='matrix_empty':kwargs['ten']='j ()'
 elif label=='job_suffix_newline':kwargs['ten']='j (a\nb)';expected='d_job_yaml_khong_duy_nhat';marker=None
 elif label in ('shell_pwsh','shell_sh','shell_null'):
  sh={'shell_pwsh':'pwsh','shell_sh':'sh','shell_null':None}[label];w=t.wf_tu(x,buoc_them={'shell':sh})
  if sh is None:marker='not_measured'
 elif label.startswith('key_'):
  k=label[4:];v={'id':'step1','if':'true','timeout-minutes':2,'continue-on-error':True}[k];w=t.wf_tu(x,buoc_them={k:v})
 elif label in ('env_job_string','env_wf_string','env_wf_empty'):
  v='${{ inputs.e }}' if label!='env_wf_empty' else {};args={'job_them' if label=='env_job_string' else 'goc_them':{'env':v}};w=t.wf_tu(x,**args)
  if label!='env_wf_empty':marker='not_measured'
 elif label=='prior_first_step':
  ww=yaml.safe_load(w);ww['jobs']['j']['steps'][0]={'run':'echo $GITHUB_PATH\n'};w=yaml.safe_dump(ww)
  lg0=t.log_voi(t.buoc('echo $GITHUB_PATH'),lg,nen='\n'.join(t.LINUX.splitlines()[:-1])+'\n');st=t.buoc_rest(lg0,w)
  p=t.chay([(t.job(1,steps=st),lg0)],wf=w)[2];g=t.gate(p)
  t.bang(t.ghep(p)=='passed' and [(z['trang_thai'],z.get('ly_do')) for z in g['dau_duong']]==t.CHAN,str(g));return g
 elif label=='prior_nonadjacent':
  w=t.wf_tu('echo $GITHUB_ENV','echo x',x);p=t.g1(w,t.buoc('echo $GITHUB_ENV'),t.buoc('echo x'),lg);g=t.gate(p)
  t.bang(t.ghep(p)=='passed' and [(z['trang_thai'],z.get('ly_do')) for z in g['dau_duong']]==t.CHAN,str(g));return g
 else:raise KeyError(label)
 p=t.g1(w,lg,**kwargs);g=t.gate(p)
 t.bang(t.ghep(p)==expected, 'ghep '+expected+' got '+str(g))
 if marker is None:t.bang(g['dau_duong']==[] and g['trang_thai']!='passed','no marker '+str(g))
 else:
  t.bang([z['trang_thai'] for z in g['dau_duong']]==[marker], 'marker '+marker+' got '+str(g))
  if marker=='not_measured':t.bang(g['dau_duong'][0].get('ly_do')=='che_do_khong_xac_dinh',str(g))
 return g
if __name__=='__main__':
 label=sys.argv[1]
 try:g=calc(label)
 except t.TinHieuChotCa as e:print('DO:'+label+':'+str(e));sys.exit(3)
 except Exception as e:print('HONG:'+label+':'+type(e).__name__+':'+str(e));sys.exit(4)
 print('DAT:'+label+':'+json.dumps(g,ensure_ascii=False))
