from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1];out=[]
for mode in ['rg-equal','rg-newer','shellcheck-newer','actionlint-newer','rg-upgrade','rg-badpost','actionlint-equal']:
 log=r/'evidence'/(mode+'.json');cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/zip-target.ps1'),'-Mode',mode,'-Log',str(log)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);(r/'evidence'/(mode+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text());pre=json.loads(Path(str(log)+'.precheck.json').read_text())
 good=mode not in ['rg-newer','shellcheck-newer','rg-badpost']
 row=dict(mode=mode,contract_holds=d['ok']==good and p.returncode==(0 if good else 1),product_rc=p.returncode,ok=d['ok'],rows=d['ket_qua'],direct_before=pre)
 print(json.dumps(row,ensure_ascii=False),flush=True);out.append(dict(command=cmd,summary=row))
(r/'evidence/zip-target-oracle.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(f"ZIP target oracle: {sum(x['summary']['contract_holds'] for x in out)}/{len(out)} PASS")
raise SystemExit(0 if all(x['summary']['contract_holds'] for x in out) else 1)
