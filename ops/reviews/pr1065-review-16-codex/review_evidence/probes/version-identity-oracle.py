from pathlib import Path
import subprocess,json,shutil
r=Path(__file__).resolve().parents[1]
s=(r/'probes/system-target.ps1').read_text()
needle="out=above[n] if mode=='system-above-target' else new[n] if mode=='system-at-target' or installed else old[n]"
assert s.count(needle)==1
s=s.replace(needle,"out=(new[n]+'-rc.7') if mode=='suffix-before' or (mode=='suffix-after' and installed) else new[n] if mode=='stable-control' or installed else old[n]")
(r/'probes/system-version-identity.ps1').write_text(s)
s=(r/'probes/portable-check.ps1').read_text().replace("$ChiKiem = $Mode -like 'check-*'","$ChiKiem = $false")
needle="print(('ripgrep ' if n=='rg.exe' else 'version: ' if n=='shellcheck.exe' else '')+v)"
assert s.count(needle)==1
s=s.replace(needle,"raw=('ripgrep ' if n=='rg.exe' else 'version: ' if n=='shellcheck.exe' else '')+v+('-rc.7' if mode=='zip-suffix-before' else '')\nwith open(os.environ['REVIEW_USER_LOG'],'a') as f:f.write(json.dumps({'version_raw':raw,'rc':0,'exe':sys.argv[0]})+'\\n')\nprint(raw)")
(r/'probes/zip-version-identity.ps1').write_text(s)
rows=[]
for mode,script in [('stable-control','system-version-identity.ps1'),('suffix-before','system-version-identity.ps1'),('suffix-after','system-version-identity.ps1'),('zip-control','zip-version-identity.ps1'),('zip-suffix-before','zip-version-identity.ps1')]:
 fixture=r/'fixtures'/('identity-'+mode);log=r/'evidence'/('identity-'+mode+'.json')
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes'/script),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=60);(r/'evidence'/('identity-'+mode+'.log')).write_text(p.stdout+p.stderr)
 assert log.exists(),(mode,p.returncode,p.stderr)
 d=json.loads(log.read_text());native=Path(str(log)+'.native.jsonl') if script.startswith('system') else fixture/'native.jsonl';events=[json.loads(x) for x in native.read_text().splitlines()]
 targeted=[x for x in d['ket_qua'] if x['cong_cu']!='commander'] if script.startswith('system') else [x for x in d['ket_qua'] if x['cong_cu'] in ('rg','shellcheck','actionlint')]
 summary=dict(mode=mode,product_rc=p.returncode,ok=d['ok'],rows=targeted,version_events=events if script.startswith('system') else [x for x in events if 'version_raw' in x])
 print(json.dumps(summary,ensure_ascii=False),flush=True);rows.append(dict(command=cmd,summary=summary,data=d,events=events));shutil.rmtree(fixture,ignore_errors=True)
(r/'evidence/version-identity-oracle.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
assert all(x['summary']['ok'] and x['summary']['product_rc']==0 for x in rows), 'unexpected: inspect before drawing conclusion'
print('Version identity: stable controls 2/2 PASS; prerelease FALSE SUCCESS 3/3 reproduced')
