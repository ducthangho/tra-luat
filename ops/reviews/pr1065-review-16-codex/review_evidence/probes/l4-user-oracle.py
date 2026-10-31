import json,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[1]
results=[]
for mode in ['success','npm-disappears','nlm-status-fails']:
 cmd=[str(root/'pwsh/pwsh'),'-NoProfile','-File',str(root/'probes/l4-user-errors.ps1'),'-Mode',mode]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
 d=json.loads(p.stdout.splitlines()[-1]) if p.returncode==0 else None
 names={r['cong_cu'] for r in d['results']} if d else set()
 if mode=='success':ok=d and d['error'] is None and d['error_rows']==0 and len(d['results'])==11
 elif mode=='npm-disappears':ok=d and d['error'] is None and d['error_rows']>=1 and {'rg','shellcheck','actionlint','nlm'}<=names
 else:ok=d and d['error'] is None and any(r['cong_cu']=='nlm' and r['hanh_dong']=='loi' for r in d['results'])
 results.append({'mode':mode,'passed':bool(ok),'command':cmd,'returncode':p.returncode,'data':d})
 print(('PASS' if ok else 'FAIL')+' '+mode)
(root/'evidence/l4-user-oracle.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
passed=sum(x['passed'] for x in results)
print(f'User native error oracle: {passed}/{len(results)} PASS')
raise SystemExit(0 if passed==len(results) else 1)
