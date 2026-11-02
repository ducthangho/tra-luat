param([string]$Product, [string]$Evidence)
$ErrorActionPreference = 'Stop'
. $Product -NapHam
$oldSystemRoot = $env:SystemRoot
$g = Join-Path ([IO.Path]::GetTempPath()) ('review-1091-' + [guid]::NewGuid().ToString('N'))
$out = [ordered]@{ native_ntfs = 'KHONG_DO_DUOC'; checks = @() }
try {
    New-Item -ItemType Directory -Path "$g/System32", "$g/install [x]/nested" | Out-Null
    foreach ($name in '.hidden', 'noextension', 'normal.txt') {
        [IO.File]::WriteAllText((Join-Path "$g/install [x]" $name), 'data')
    }
    $ordinary = @(Get-ChildItem -LiteralPath "$g/install [x]").Count
    $forced = @(Get-ChildItem -LiteralPath "$g/install [x]" -Force).Count
    $out.checks += [ordered]@{ name='enumeration_linux'; ordinary=$ordinary; forced=$forced; names=@(Get-ChildItem -LiteralPath "$g/install [x]" -Force | ForEach-Object Name) }
    $env:SystemRoot = $g
    $env:REVIEW_ICACLS_LOG = Join-Path $g 'argv.json'
    $shim = @'
#!/usr/bin/python3
import json,os,sys
with open(os.environ['REVIEW_ICACLS_LOG'],'w') as f: json.dump(sys.argv[1:],f)
print('injected-native-rc')
sys.exit(int(os.environ['REVIEW_ICACLS_RC']))
'@
    [IO.File]::WriteAllText("$g/System32/icacls.exe", $shim)
    & chmod +x "$g/System32/icacls.exe"
    $argv = @((Join-Path "$g/install [x]" '*'), '/reset', '/T', '/C', '/L', '/Q')
    foreach ($rc in 0, 1, 5) {
        $env:REVIEW_ICACLS_RC = "$rc"
        $message = $null
        try { Invoke-Icacls $argv } catch { $message = $_.Exception.Message }
        $seen = @(Get-Content -LiteralPath $env:REVIEW_ICACLS_LOG -Raw | ConvertFrom-Json)
        $same = ($seen | ConvertTo-Json -Compress) -ceq ($argv | ConvertTo-Json -Compress)
        $out.checks += [ordered]@{ name='native_wrapper'; requested_rc=$rc; argv=$seen; exact_argv=$same; threw=($null -ne $message); error=$message }
        if (-not $same -or (($rc -ne 0) -ne ($null -ne $message))) { throw 'native wrapper assertion failed' }
    }
    if ($forced -ne 4 -or $ordinary -ne 3) { throw 'Linux enumeration assertion failed' }
    $out | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $Evidence 'native-wrapper.json') -Encoding utf8NoBOM
    Write-Host 'Wrapper/argv: 3/3 PASS; enumeration Linux: 1/1 PASS; native Windows: KHONG_DO_DUOC'
} finally {
    $env:SystemRoot = $oldSystemRoot
    Remove-Item Env:REVIEW_ICACLS_RC, Env:REVIEW_ICACLS_LOG -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $g -Recurse -Force -ErrorAction SilentlyContinue
}
