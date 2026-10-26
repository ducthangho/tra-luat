from pathlib import Path
import ast,sys,os,json,subprocess
R=Path(__file__).resolve().parent;root=R.parent
src=(root/'ops/ci_provenance.py').read_text();d=R/'proof-mutants6';d.mkdir(exist_ok=True)
M={}
for n in ast.walk(ast.parse((R/'frontier6.py').read_text())):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='add':
  try:name,old,new=[ast.literal_eval(x) for x in n.args]
  except Exception:continue
  if src.count(old)==1:M[name]=(old,new)
names=['job_ascii_suffix','job_alias_truncate','job_requires_nonempty_steps','job_nonempty_rest_required','rest_number_under_100','rest_number_order_contiguous','rest_skipped_time_required','time_require_same_day','time_reject_leap_day','time_reject_year_before_2000','time_accept_invalid_leap_day','prior_entire_step_instead_run','prior_uses_preferred','prior_ignore_if_empty_env','prior_only_last_two','log_first_output_line','log_last_output_line','log_output_strip','log_reverse_output','log_reject_metadata_after_shell','log_uncolored_metadata_add_to_echo','log_shell_nonempty','log_color_prefix_only','log_color_without_timestamp','run_blank_lines_disallowed','rest_also_skip_null','yaml_empty_workflow_reject']
rows=[]
for name in names:
 old,new=M[name];p=d/(name+'.py');p.write_text(src.replace(old,new));pair=[]
 for tag,path in [('head',root/'ops/ci_provenance.py'),('mutant',p)]:
  c=[sys.executable,'-B',str(R/'cases6.py'),name];q=subprocess.run(c,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(path),PYTHONDONTWRITEBYTECODE='1'));pair.append({'source':tag,'path':str(path),'command':c,'rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
 rec={'name':name,'old':old,'new':new,'pair':pair,'proven':pair[0]['rc']==0 and pair[1]['rc']==3 and pair[1]['output'].startswith('DO:'+name+':')};rows.append(rec)
 (R/'proof-all6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(name,pair[0]['rc'],pair[1]['rc'],rec['proven'],flush=True)
