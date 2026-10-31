import json,pathlib,subprocess
r=pathlib.Path(__file__).resolve().parents[1];results=[]
for mode in ['success','npm-cannot-start','pip-fails','py-disappears','venv-disappears','nlm-pip-fails','nlm-disappears','nlm-status-broken-json','nlm-status-other','check-only','cli-version-stderr-fails','nlm-version-fails']:
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/user-extra.ps1'),'-Mode',mode]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
 (r/f'evidence/user-extra-{mode}.log').write_text(p.stdout+p.stderr)
 d=json.loads(p.stdout.splitlines()[-1]) if p.returncode==0 else None
 results.append(dict(mode=mode,command=cmd,returncode=p.returncode,data=d,stderr=p.stderr))
 summary=dict(mode=mode,rc=p.returncode)
 if d:summary.update(error=d['error'],errors=d['error_rows'],rows=len(d['results']),restored=d['profile_restored'],last=d['results'][-1],native_installs=sum(1 for x in d['events'] if 'install' in x['argv']))
 print(json.dumps(summary,ensure_ascii=False),flush=True)
 (r/'evidence/user-extra.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
