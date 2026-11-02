from pathlib import Path
import subprocess,json,shutil
r=Path(__file__).resolve().parents[1];out=[]
for mode in ['system-control','system-rc9','system-garbage','system-missing','system-cannot-start','system-no-lts']:
 fixture=r/'fixtures'/mode;log=r/'evidence'/(mode+'.json')
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/system-check.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,text=True,capture_output=True,timeout=40);(r/'evidence'/(mode+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text()) if log.exists() else None
 events=[json.loads(x) for x in Path(str(log)+'.native.jsonl').read_text().splitlines()] if Path(str(log)+'.native.jsonl').exists() else []
 control=mode in ['system-control','system-no-lts'];expected_rc=0 if control else 1
 passed=bool(d and d['ok']==control and p.returncode==expected_rc and d['loi']==(0 if control else 4) and all(x['truoc'] for x in d['ket_qua'] if x['hanh_dong']!='loi'))
 summary=dict(mode=mode,passed=passed,rc=p.returncode,ok=d['ok'] if d else None,errors=d['loi'] if d else None,rows=[(x['cong_cu'],x['hanh_dong'],x['truoc']) for x in d['ket_qua']] if d else None,native_calls=len(events),native_rcs=[x['rc'] for x in events])
 out.append(dict(command=cmd,summary=summary,data=d,events=events));print(json.dumps(summary),flush=True);shutil.rmtree(fixture,ignore_errors=True)
(r/'evidence/system-check-oracle.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(f"System ChiKiem oracle: {sum(x['summary']['passed'] for x in out)}/{len(out)} PASS")
raise SystemExit(0 if all(x['summary']['passed'] for x in out) else 1)
