from pathlib import Path
import json,subprocess,shutil
r=Path(__file__).resolve().parents[1];out=[]
for mode in ['check-only','check-missing-cli','check-missing-nlm-exe','check-missing-nlm-python','check-missing-nlm-all','check-missing-venv','check-metadata-empty','check-metadata-garbage','metadata-recover']:
 log=r/f'evidence/absence-{mode}.json';fixture=r/f'fixtures/absence-{mode}'
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/absence-and-metadata.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);(r/f'evidence/absence-{mode}.log').write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text()) if log.exists() else None
 events=[json.loads(x) for x in (fixture/'native.jsonl').read_text().splitlines()] if (fixture/'native.jsonl').exists() else []
 summary=dict(mode=mode,rc=p.returncode,ok=d['ok'] if d else None,errors=d['loi'] if d else None,rows=d['tong'] if d else None,actions={x['cong_cu']:x['hanh_dong'] for x in d['ket_qua']} if d else None,installs=sum('install' in x['argv'] for x in events))
 print(json.dumps(summary,ensure_ascii=False),flush=True);out.append(dict(command=cmd,summary=summary,data=d,events=events))
 shutil.rmtree(fixture)
(r/'evidence/absence-oracle.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
assert all(x['data'] is not None for x in out)
