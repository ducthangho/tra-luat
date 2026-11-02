from pathlib import Path
import subprocess,json,shutil
r=Path(__file__).resolve().parents[1]
s=(r/'probes/third-paths.ps1').read_text();needle="if a==['--version']:\n";assert s.count(needle)==1
s=s.replace(needle,"if a==['--version'] and name in ['claude.cmd','codex.cmd'] and os.environ['REVIEW_USER_MODE']=='cli-suffix':\n print('1.0.0-rc.7');sys.exit(0)\n"+needle)
(r/'probes/cli-version-identity.ps1').write_text(s)
rows=[]
for mode in ['cli-stable-control','cli-suffix']:
 fixture=r/'fixtures'/('identity-'+mode);log=r/'evidence'/('identity-'+mode+'.json')
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/cli-version-identity.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=60);(r/'evidence'/('identity-'+mode+'.log')).write_text(p.stdout+p.stderr);d=json.loads(log.read_text())
 direct=[]
 for name in ['claude.cmd','codex.cmd']:
  q=subprocess.run([str(fixture/'Tools/npm'/name),'--version'],capture_output=True,text=True,env={**__import__('os').environ,'REVIEW_USER_MODE':mode,'REVIEW_USER_LOG':str(fixture/'native.jsonl')});direct.append(dict(name=name,rc=q.returncode,stdout=q.stdout))
 x=dict(mode=mode,product_rc=p.returncode,ok=d['ok'],rows=[v for v in d['ket_qua'] if v['cong_cu'] in ['claude','codex']],direct=direct);rows.append(dict(command=cmd,summary=x));print(json.dumps(x,ensure_ascii=False),flush=True);shutil.rmtree(fixture)
(r/'evidence/cli-version-identity-oracle.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));assert all(x['summary']['product_rc']==0 and x['summary']['ok'] for x in rows);print('CLI identity: stable control PASS; prerelease FALSE SUCCESS reproduced')
