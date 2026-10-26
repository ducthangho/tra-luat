from pathlib import Path
import os,sys,json,subprocess
R=Path(__file__).resolve().parent
pairs=[('run_rstrip_all','run_trailing_space'),('metadata_post_anywhere','metadata_post_infix'),('log_shell_suffix','shell_prefix_space_missing'),('mode_defaults_job_truthy','defaults_job_empty'),('mode_defaults_wf_truthy','defaults_wf_empty'),('mode_env_truthy','env_job_false'),('mode_env_string_only','env_wf_list'),('rest_number_bool','number_bool_metadata'),('rest_number_float','number_float'),('job_alias_exact_drop','job_alias_exact'),('job_matrix_nonempty','matrix_empty'),('job_dotall_add','job_suffix_newline'),('mode_shell_no_pwsh','shell_pwsh'),('mode_shell_no_sh','shell_sh'),('mode_shell_null_default','shell_null'),('mode_env_shape_drop','env_job_string'),('mode_env_shape_drop','env_wf_string'),('mode_env_presence_not_value','env_wf_empty'),('mode_key_id_drop','key_id'),('mode_key_if_drop','key_if'),('mode_key_timeout_drop','key_timeout-minutes'),('mode_key_coe_drop','key_continue-on-error'),('mode_prior_skip_first','prior_first_step'),('mode_prior_only_last','prior_nonadjacent')]
rows=[]
for mut,case in pairs:
 for source in (None,R/'frontier'/(mut+'.py')):
  if source and not source.exists():
   source=R/'frontier2'/(mut+'.py')
   if not source.exists():continue
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  if source:env['CI_PROVENANCE_MA']=str(source)
  cmd=[sys.executable,'-B',str(R/'frontier_cases.py'),case];p=subprocess.run(cmd,capture_output=True,env=env)
  rows.append({'mutant':mut,'case':case,'source':str(source) if source else 'HEAD','command':cmd,'rc':p.returncode,'output':(p.stdout+p.stderr).decode('utf8','replace')})
  print(mut,case,'mutant' if source else 'HEAD',p.returncode,flush=True)
(R/'frontier-counterexamples.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
