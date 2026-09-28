import json,pathlib,subprocess,sys
root=pathlib.Path.cwd()
paths=['scripts/tl.py','.claude/dev/ci_dang_ky_test.py','.claude/dev/doc_receipt_thu_hoi.py','.claude/dev/doc_receipt_thu_hoi_test.py']
cmd=[sys.executable,'-m','ruff','--version'];p=subprocess.run(cmd,capture_output=True,text=True);print(json.dumps(dict(command=cmd,rc=p.returncode,stdout=p.stdout)))
for path in paths:
 data={}
 for ref in ('origin/master','HEAD'):
  read=['git','show',ref+':'+path];r=subprocess.run(read,capture_output=True)
  if r.returncode:
   data[ref]=[];print(json.dumps(dict(command=read,rc=r.returncode,status='absent_at_base')));continue
  cmd=[sys.executable,'-m','ruff','check','--no-cache','--select','F','--output-format','json','--stdin-filename',str(root/path),'-']
  p=subprocess.run(cmd,input=r.stdout,capture_output=True);rows=json.loads(p.stdout);data[ref]=rows
  print(json.dumps(dict(path=path,ref=ref,command=cmd,rc=p.returncode,diagnostics=rows)))
 print(json.dumps(dict(path=path,delta_equal=data['HEAD']==data['origin/master'],head_count=len(data['HEAD']),base_count=len(data['origin/master']))))
