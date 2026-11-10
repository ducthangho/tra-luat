"""Exact-source Capture/Cleanup collection tests, native PS5.1/7; no browser."""
import pathlib,sys,re,json,subprocess,os,hashlib,csv
source=pathlib.Path(sys.argv[1]).read_text(encoding='utf-8-sig');out=pathlib.Path(sys.argv[2]);out.mkdir(exist_ok=False)
blocks=re.findall(r'```powershell\n(.*?)\n```',source,re.S);assert len(blocks)==5
helpers=blocks[0][blocks[0].index('function Need'):blocks[0].index('function Test-PwEnv')]
capture=blocks[3][blocks[3].index('  $h = @('):].rsplit('}',1)[0]
cleanup=blocks[4][blocks[4].index('  $files = Get-ChildItem'):blocks[4].index("  'CLEANUP OK'")]
assert 'Get-PwHashes' in capture and 'Get-PwHashes' in cleanup
records=[];languages=[('ps51',r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',r'C:\Windows\System32\WindowsPowerShell\v1.0\Modules'),('ps7',r'C:\Program Files\PowerShell\7\pwsh.exe',r'C:\Program Files\PowerShell\7\Modules')]
cases=['valid','throw','missing-command','null-hash','invalid-hash','second-read-fails','unreadable-file']
for tag,exe,modules in languages:
 for context,fragment in [('capture',capture),('cleanup',cleanup)]:
  for case in cases+['old-calculated-property-mutant']:
   label=tag+'-'+context+'-'+case;d=out/label;d.mkdir();(d/'a.txt').write_bytes(b'alpha');(d/'b.txt').write_bytes(b'beta');manifest=d/'SHA256SUMS.csv';sentinel=b'PREVIOUS_EVIDENCE_MUST_SURVIVE_FAILURE'
   if case!='valid':manifest.write_bytes(sentinel)
   pre=''
   if case in ['throw','old-calculated-property-mutant']:pre="function Get-FileHash { throw 'CONTROLLED_REQUIRED_HASH_FAILURE' }\n"
   elif case=='missing-command':pre="function Get-FileHash { & MissingRequiredHashCommand }\n"
   elif case in ['null-hash','invalid-hash','second-read-fails']:
    value="$null" if case=='null-hash' else "'invalid'" if case=='invalid-hash' else "('A'*64)"
    pre="$global:hashCalls=0; function Get-FileHash { $global:hashCalls++; "+("if($global:hashCalls -eq 2){throw 'CONTROLLED_SECOND_HASH_FAILURE'}; " if case=='second-read-fails' else '')+"'fixture' | Select-Object @{n='Hash';e={"+value+"}} }\n"
   elif case=='unreadable-file':pre="$held=[IO.File]::Open($env:TL_PW_RUN+'\\a.txt',[IO.FileMode]::Open,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)\n"
   body=fragment
   if case=='old-calculated-property-mutant':body="  $h = Get-ChildItem -Force -File -LiteralPath $env:TL_PW_RUN | Select-Object FullName, Length, @{n='SHA256';e={(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}}\n  $h | Export-Csv -LiteralPath \"$env:TL_PW_RUN\\SHA256SUMS.csv\" -NoTypeInformation -Encoding UTF8\n"
   # Preload before doubles: PS5 module autoload otherwise replaces a double when
   # Select-Object first imports Utility, hiding a later injected failure.
   script="Import-Module Microsoft.PowerShell.Utility -ErrorAction Stop\n"+helpers+'\n'+pre+"& { $ErrorActionPreference='Stop'\n"+body+"\n'HASH_COLLECTION_OK' }\n";path=out/(label+'.ps1');path.write_text(script,encoding='utf-8-sig')
   env=os.environ.copy();env.update(TL_PW_RUN=str(d),PSModulePath=modules+r';C:\Program Files\WindowsPowerShell\Modules')
   cp=subprocess.run([exe,'-NoProfile','-NonInteractive','-File',str(path)],env=env,capture_output=True,timeout=30);(out/(label+'.stdout')).write_bytes(cp.stdout);(out/(label+'.stderr')).write_bytes(cp.stderr)
   marker=b'HASH_COLLECTION_OK' in cp.stdout;unchanged=manifest.exists() and manifest.read_bytes()==sentinel
   passed=cp.returncode!=0 and not marker and unchanged;rows=[]
   if case=='valid':
    rows=list(csv.DictReader(manifest.read_text(encoding='utf-8-sig').splitlines()));passed=cp.returncode==0 and marker and len(rows)==2 and all(x['SHA256']==hashlib.sha256(pathlib.Path(x['FullName']).read_bytes()).hexdigest().upper() for x in rows)
   if case=='old-calculated-property-mutant':
    rows=list(csv.DictReader(manifest.read_text(encoding='utf-8-sig').splitlines()));passed=cp.returncode==0 and marker and not unchanged and any(not x['SHA256'] for x in rows)
   records.append({'id':label,'rc':cp.returncode,'passed':passed,'marker':marker,'failure_preserved_manifest':unchanged,'rows':len(rows),'mutant_control':case=='old-calculated-property-mutant'})
summary={'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'tests':len(records),'passed':sum(x['passed'] for x in records),'failed':[x['id'] for x in records if not x['passed']],'records':records,'scope':'Source helper and source-extracted final collection/export fragment only; no browser or full Capture/Cleanup flow'}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='records'}));sys.exit(bool(summary['failed']))
