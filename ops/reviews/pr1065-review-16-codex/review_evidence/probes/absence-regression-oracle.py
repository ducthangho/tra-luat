from pathlib import Path
import subprocess,json,shutil,argparse
r=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('--prototype',action='store_true');a=ap.parse_args();label='prototype' if a.prototype else 'head';product=r/('hint-prototype' if a.prototype else 'copies/head')/'ops/vm/cap-nhat-cong-cu.ps1';out=[]
for mode in ['check-only','check-missing-nlm-exe','check-missing-nlm-python','check-missing-nlm-all']:
 log=r/f'evidence/absence-regression-{label}-{mode}.json';fixture=r/f'fixtures/absence-regression-{label}-{mode}'
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/absence-and-metadata.ps1'),'-Product',str(product),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);(r/f'evidence/absence-regression-{label}-{mode}.log').write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text()) if log.exists() else None;nlm=next((x for x in d['ket_qua'] if x['cong_cu']=='nlm'),{}) if d else {};control=mode=='check-only'
 events=[json.loads(x) for x in (fixture/'native.jsonl').read_text().splitlines()] if (fixture/'native.jsonl').exists() else []
 ok=bool(d and d['tong']==11 and d['ok']==control and d['loi']==(0 if control else 1) and nlm.get('hanh_dong')==('kiem' if control else 'loi') and p.returncode==(0 if control else 1) and not any('install' in x['argv'] for x in events))
 row=dict(mode=mode,passed=ok,rc=p.returncode,ok=d['ok'] if d else None,nlm=nlm.get('hanh_dong'),errors=d['loi'] if d else None);out.append(dict(command=cmd,result=row,data=d,events=events));print(json.dumps(row,ensure_ascii=False),flush=True);shutil.rmtree(fixture)
(r/f'evidence/absence-regression-{label}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(f'NLM prerequisite oracle ({label}): {sum(x["result"]["passed"] for x in out)}/4 PASS',flush=True)
raise SystemExit(0 if all(x['result']['passed'] for x in out) else 1)
