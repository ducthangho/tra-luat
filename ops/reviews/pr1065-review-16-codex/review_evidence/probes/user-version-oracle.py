from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1];results=[]
for mode in ['success','cli-version-stderr-fails','nlm-version-fails']:
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/user-extra.ps1'),'-Mode',mode]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
 d=json.loads(p.stdout.splitlines()[-1]) if p.returncode==0 else None
 rows={x['cong_cu']:x for x in d['results']} if d else {}
 targets=['claude','codex'] if mode.startswith('cli') else ['nlm']
 ok=bool(d and d['error'] is None and (d['error_rows']==0 if mode=='success' else all(rows[x]['hanh_dong']=='loi' for x in targets)))
 results.append(dict(mode=mode,passed=ok,command=cmd,returncode=p.returncode,data=d,stderr=p.stderr))
 print(('PASS ' if ok else 'FAIL ')+mode,flush=True)
(r/'evidence/user-version-oracle.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(f"Version native failure oracle: {sum(x['passed'] for x in results)}/3 PASS")
raise SystemExit(0 if all(x['passed'] for x in results) else 1)
