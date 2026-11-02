from pathlib import Path
import subprocess,json,os,shutil
r=Path(__file__).resolve().parents[1];out=[]
for mode in ['venv-post-control','venv-pip-rc8','venv-post-rc9','venv-post-wrong-pin']:
 fixture=r/'fixtures'/mode;log=r/'evidence'/(mode+'.json')
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/install-contract.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,text=True,capture_output=True,timeout=45)
 (r/'evidence'/(mode+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text());events=[json.loads(x) for x in (fixture/'native.jsonl').read_text().splitlines()]
 env={**os.environ,'REVIEW_USER_MODE':mode,'REVIEW_USER_LOG':str(fixture/'native.jsonl'),'REVIEW_PHASE':'direct-after'}
 measured=[]
 for args in [['--version'],['-c',"import importlib.metadata as m; print(m.version('PyYAML'))"],['-c',"import importlib.metadata as m; print(m.version('jsonschema'))"]]:
  q=subprocess.run([str(fixture/'venv/Scripts/python.exe'),*args],env=env,text=True,capture_output=True)
  measured.append(dict(argv=args,rc=q.returncode,stdout=q.stdout.strip(),stderr=q.stderr.strip()))
 v=next(x for x in d['ket_qua'] if x['cong_cu']=='venv-kho');isbad=mode!='venv-post-control'
 passed=d['ok']==(not isbad) and p.returncode==(1 if isbad else 0) and v['hanh_dong']==('loi' if isbad else 'giu')
 summary=dict(mode=mode,passed=passed,product_rc=p.returncode,ok=d['ok'],errors=d['loi'],rows=d['tong'],venv=v,venv_product_calls=[x for x in events if '/venv/' in x['exe']],direct_after=measured)
 out.append(dict(command=cmd,summary=summary,data=d,events=events));print(json.dumps(summary,ensure_ascii=False),flush=True)
 shutil.rmtree(fixture)
(r/'evidence/install-contract-oracle.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(f"Install contract oracle: {sum(x['summary']['passed'] for x in out)}/{len(out)} PASS")
raise SystemExit(0 if all(x['summary']['passed'] for x in out) else 1)
