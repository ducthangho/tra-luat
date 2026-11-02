$ErrorActionPreference='Stop'
. "$PSScriptRoot/../copies/head/ops/vm/cap-nhat-cong-cu.ps1" -NapHam
$base=Join-Path ([IO.Path]::GetTempPath()) ('review icacls-đường dẫn-'+[guid]::NewGuid().ToString('N'))
$previousRoot=$env:SystemRoot
New-Item -ItemType Directory -Path "$base/System32"|Out-Null
$shim=@'
#!/usr/bin/python3
import json,os,sys
with open(os.environ['REVIEW_IC_LOG'],'a') as f:
    f.write(json.dumps({'exe':sys.argv[0],'argv':sys.argv[1:]},ensure_ascii=False)+'\n')
print('stdout-shim')
print('stderr-shim',file=sys.stderr)
sys.exit(int(os.environ['REVIEW_IC_RC']))
'@
[IO.File]::WriteAllText("$base/System32/icacls.exe",$shim)
& /bin/chmod +x "$base/System32/icacls.exe"
$env:SystemRoot=$base;$env:REVIEW_IC_LOG="$base/argv.jsonl"
$wanted=@('D:\thư mục a&$`[x]\','/grant:r','*S-1-5-18:(OI)(CI)F','/L','/Q')
$results=@()
try {
 foreach($rc in @(0,1,5,1332)) {
    $env:REVIEW_IC_RC="$rc";$msg=$null
    try { Invoke-Icacls $wanted }catch{$msg=$_.Exception.Message}
    $event=Get-Content -LiteralPath $env:REVIEW_IC_LOG|Select-Object -Last 1|ConvertFrom-Json
    $results += [ordered]@{rc=$rc;threw=($null-ne$msg);message=$msg;argv=$event.argv;roundtrip=(($event.argv|ConvertTo-Json -Compress)-ceq($wanted|ConvertTo-Json -Compress));absolute_exe=$event.exe}
 }
 Remove-Item -LiteralPath "$base/System32/icacls.exe"
 $msg=$null;try{Invoke-Icacls $wanted}catch{$msg=$_.Exception.Message}
 $results += [ordered]@{case='missing_absolute_exe';threw=($null-ne$msg);message=$msg}
 $results|ConvertTo-Json -Depth 6
} finally {$env:SystemRoot=$previousRoot;Remove-Item Env:REVIEW_IC_LOG,Env:REVIEW_IC_RC -ErrorAction SilentlyContinue;Remove-Item -LiteralPath $base -Recurse -Force}
