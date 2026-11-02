from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1];out=[]
for mode in ['clean','acl-reject','hash-reject','install-ancestor-link','install-child-link']:
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/registration.ps1'),'-Mode',mode]
 p=subprocess.run(cmd,text=True,capture_output=True,timeout=35);(r/'evidence'/('register-head-'+mode+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(p.stdout.splitlines()[-1]) if p.returncode==0 else None
 passed=bool(d and len(d['tasks'])==(1 if mode=='clean' else 0) and d['tool_acl_calls']==0)
 summary=dict(mode=mode,passed=passed,rc=p.returncode,**({k:d[k] for k in ['error','icacls_count','tool_acl_calls','audit_count']} if d else {}),tasks=len(d['tasks']) if d else None)
 out.append(dict(command=cmd,summary=summary,data=d));print(json.dumps(summary),flush=True)
(r/'evidence/registration-head.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
assert all(x['summary']['passed'] for x in out)
