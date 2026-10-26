from pathlib import Path
p=Path('.review/frontier_cases.py');s=p.read_text();anchor=" if label=='number_bool_metadata':"
s=s.replace(anchor,""" if label=='run_trailing_space':
  w=t.wf_tu(x+'  ');lg=t.buoc(x+'  ','THU: 4/4 dat')
 elif label=='metadata_post_infix':w=t.wf_tu(x,buoc_them={'name':'Check Post result'})
 elif label=='shell_prefix_space_missing':
  lg=[d.replace('shell: /usr','shell:/usr') for d in lg];marker=None
 elif label in ('defaults_job_empty','defaults_wf_empty'):
  w=t.wf_tu(x,**{'job_them' if label=='defaults_job_empty' else 'goc_them':{'defaults':{}}});marker='not_measured'
 elif label in ('env_job_false','env_wf_list'):
  w=t.wf_tu(x,**{'job_them' if label=='env_job_false' else 'goc_them':{'env':False if label=='env_job_false' else []}});marker='not_measured'
 elif label=='number_bool_metadata':""")
p.write_text(s)
p=Path('.review/prove_frontier.py');s=p.read_text().replace("('rest_number_bool','number_bool_metadata')", "('run_rstrip_all','run_trailing_space'),('metadata_post_anywhere','metadata_post_infix'),('log_shell_suffix','shell_prefix_space_missing'),('mode_defaults_job_truthy','defaults_job_empty'),('mode_defaults_wf_truthy','defaults_wf_empty'),('mode_env_truthy','env_job_false'),('mode_env_string_only','env_wf_list'),('rest_number_bool','number_bool_metadata')")
s=s.replace("if source and not source.exists():continue", "if source and not source.exists():\n   source=R/'frontier2'/(mut+'.py')\n   if not source.exists():continue")
p.write_text(s)
