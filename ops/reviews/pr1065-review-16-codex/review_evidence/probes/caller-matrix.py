from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1];out=[]
for mode in ['system-pre','system-post','zip-pre','zip-post']:
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/caller-null.ps1'),'-Mode',mode]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);(r/f'evidence/caller-{mode}.log').write_text(p.stdout+p.stderr)
 d=json.loads(p.stdout.splitlines()[-1]) if p.returncode==0 else None
 print(json.dumps(dict(mode=mode,rc=p.returncode,data=d),ensure_ascii=False),flush=True);out.append(dict(command=cmd,returncode=p.returncode,data=d))
(r/'evidence/caller-null.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
assert all(x['data'] is not None for x in out)
