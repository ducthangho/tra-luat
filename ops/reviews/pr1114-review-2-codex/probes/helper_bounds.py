import importlib.util,json,pathlib,subprocess,time
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review_bounds',root/'work/head/ops/cloud_agent_creds_test.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=[]
for label,lifetime,kw in [('default_live_30s',30,{}),('zero_live_30s',30,{'cho_chet':0}),('default_self_exit_1s',1,{})]:
 p=subprocess.Popen(['sleep',str(lifetime)]);t=time.monotonic()
 result=m._song_roi_don([None,p.pid], **kw);elapsed=time.monotonic()-t
 rc=p.wait(timeout=2)
 row=dict(label=label,seconds=round(elapsed,6),reported_alive=(p.pid in result),returncode=rc)
 rows.append(row);print(json.dumps(row),flush=True)
(root/'evidence/helper-bounds.json').write_text(json.dumps(rows,indent=2)+'\n')
