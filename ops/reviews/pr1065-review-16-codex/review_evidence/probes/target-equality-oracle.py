from pathlib import Path
import subprocess, json, shutil
r=Path(__file__).resolve().parents[1]
# Extend the native fixture, never product code. Its python metadata and manager
# query remain 0.5.0, while the executable can report a stale version.
s=(r/'probes/third-paths.ps1').read_text()
needle="if a==['--version']:\n"
extra="""if name=='nlm.exe' and a==['--version'] and os.environ['REVIEW_USER_MODE']=='nlm-cli-stale':
 print('nlm version 0.4.0');sys.exit(0)
"""
assert s.count(needle)==1
(r/'probes/nlm-target.ps1').write_text(s.replace(needle,extra+needle))
# System executable calls and rc remain native. Release/download/install/task are
# offline models inherited from the round 9 fixture.
s=(r/'probes/system-check.ps1').read_text().replace('$ChiKiem=$true','$ChiKiem=$false')
s=s.replace("out='unparseable-output' if mode=='system-garbage' else old[n]", """above={'git.exe':'git version 3.0.0','gh.exe':'gh version 3.0.0','node.exe':'v24.3.0','pwsh.exe':'7.7.0'}
out=above[n] if mode=='system-above-target' else new[n] if mode=='system-at-target' or installed else old[n]""")
(r/'probes/system-target.ps1').write_text(s)
rows=[]
for mode,script,expected in [
 ('nlm-control','nlm-target.ps1',True),('nlm-cli-stale','nlm-target.ps1',False),
 ('system-install-control','system-target.ps1',True),('system-at-target','system-target.ps1',True),('system-above-target','system-target.ps1',False)]:
 fixture=r/'fixtures'/mode; log=r/'evidence'/(mode+'.json')
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes'/script),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=45); (r/'evidence'/(mode+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text()); native=fixture/'native.jsonl' if script.startswith('nlm') else Path(str(log)+'.native.jsonl')
 events=[json.loads(x) for x in native.read_text().splitlines()]
 target_rows=[x for x in d['ket_qua'] if x['cong_cu']=='nlm'] if script.startswith('nlm') else [x for x in d['ket_qua'] if x['cong_cu']!='commander']
 is_good=d['ok']==expected and p.returncode==(0 if expected else 1)
 row=dict(mode=mode,contract_holds=is_good,product_rc=p.returncode,ok=d['ok'],errors=d['loi'],results=target_rows)
 rows.append(dict(command=cmd,summary=row,data=d,events=events)); print(json.dumps(row,ensure_ascii=False),flush=True)
 shutil.rmtree(fixture,ignore_errors=True)
(r/'evidence/target-equality.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('Target equality oracle:',sum(x['summary']['contract_holds'] for x in rows),'/',len(rows),'PASS')
raise SystemExit(0 if all(x['summary']['contract_holds'] for x in rows) else 1)
