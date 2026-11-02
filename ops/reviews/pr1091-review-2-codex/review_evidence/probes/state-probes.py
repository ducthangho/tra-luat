from pathlib import Path
import json,subprocess,os
ROOT=Path(__file__).resolve().parents[1]
P='ops/vm/cap-nhat-cong-cu.ps1'
cases=[
 ('head_empty','control','dacl-rong','head'),
 ('no_reset_empty','no_reset','dacl-rong','head'),
 ('after_copy_empty','reset_after_copy','dacl-rong','head'),
 ('after_copy_cached_empty','reset_after_copy_cached_condition','dacl-rong','head'),
 ('head_nested','control','cay-long','head'),
 ('no_T_nested_head_model','reset_no_T','cay-long','head'),
 ('no_T_nested_original_model','reset_no_T','cay-long','original'),
 ('no_T_nested_recursive_model','reset_no_T','cay-long','recursive'),
 ('head_nested_previous_recursive','control','cay-long','recursive'),
]
results=[]
for name,variant,mode,model in cases:
 script=ROOT/'probes/state-head-model.ps1' if model=='head' else ROOT/f'luot1/probes/state-{model}-model.ps1'
 out=ROOT/f'evidence/{name}.json'
 args=[str(ROOT/'pwsh/pwsh'),'-NoProfile','-File',str(script),'-Product',str(ROOT/'copies'/variant/P),'-Mode',mode,'-OutFile',str(out)]
 proc=subprocess.run(args,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=60)
 (ROOT/f'evidence/{name}.log').write_text(proc.stdout+proc.stderr)
 assert proc.returncode==0,(name,proc.stdout,proc.stderr)
 d=json.loads(out.read_text())
 row=dict(name=name,rc=proc.returncode,mode=mode,model=model,error=d['error'],tasks=d['tasks'],nodes=len(d['states']),bad_nodes=sum(bool(n['violations']) for n in d['states']),command=args)
 results.append(row); print(json.dumps({k:v for k,v in row.items() if k!='command'},ensure_ascii=False),flush=True)
(ROOT/'evidence/state-probes.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
