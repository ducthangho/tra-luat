from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1];results=[]
for mode in ['success','download-tamper','missing-hash','installer-failure','msi-reboot','post-version-wrong']:
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/system-install.ps1'),'-Mode',mode]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);(r/f'evidence/system-{mode}.log').write_text(p.stdout+p.stderr)
 d=json.loads(p.stdout.splitlines()[-1]) if p.returncode==0 else None
 results.append(dict(mode=mode,command=cmd,returncode=p.returncode,data=d,stderr=p.stderr))
 print(json.dumps(dict(mode=mode,rc=p.returncode,**(dict(error=d['error'],spawns=len(d['spawns']),verified=all(x['hash_matches'] for x in d['spawns']),left=d['remaining_downloads'],restart=d['commander_restart'],rows=[(x['cong_cu'],x['hanh_dong']) for x in d['results']]) if d else {})),ensure_ascii=False),flush=True)
 (r/'evidence/system-matrix.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
