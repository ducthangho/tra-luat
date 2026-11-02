from pathlib import Path
import subprocess,json,shutil
r=Path(__file__).resolve().parents[1];results=[]
for mode in ['check-only','check-python','check-cli','check-nlm','metadata-fails','check-metadata']:
 log=r/f'evidence/new-oracle-{mode}.json'; fixture=r/'fixtures'/mode
 if fixture.exists():shutil.rmtree(fixture)
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/new-paths.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);(r/f'evidence/new-oracle-{mode}.log').write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text()) if log.exists() else None;rows={x['cong_cu']:x for x in d['ket_qua']} if d else {}
 targets={'check-python':['python'],'check-cli':['claude','codex'],'check-nlm':['nlm'],'metadata-fails':['pip','PyYAML','jsonschema'],'check-metadata':['pip','PyYAML','jsonschema']}.get(mode,[])
 expected_rc=0 if mode=='check-only' else 1
 ok=bool(d and p.returncode==expected_rc and d['ok']==(mode=='check-only') and all(rows.get(t,{}).get('hanh_dong')=='loi' for t in targets))
 trace=fixture/'native.jsonl';events=[json.loads(l) for l in trace.read_text().splitlines()] if trace.exists() else []
 out=dict(mode=mode,command=cmd,returncode=p.returncode,expected_returncode=expected_rc,passed=ok,data=d,native_events=events);results.append(out)
 (r/'evidence/new-paths-oracle.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 print(json.dumps(dict(mode=mode,passed=ok,rc=p.returncode,**({k:d[k] for k in ['chi_kiem','loi','ok','tong']} if d else {})),ensure_ascii=False),flush=True)
 shutil.rmtree(fixture)
print(f"Remaining native paths oracle: {sum(x['passed'] for x in results)}/{len(results)} PASS")
raise SystemExit(0 if all(x['passed'] for x in results) else 1)
