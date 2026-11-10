param([string]$Step, [string]$ArgumentsFile)
$ErrorActionPreference = 'Stop'
$env:PSModulePath=(Join-Path $PSHOME 'Modules')+';C:\Program Files\WindowsPowerShell\Modules'
function Need($Ok, $Msg) { if (-not $Ok) { throw "STOP[PLAYWRIGHT_ADDON_UNAVAILABLE]: $Msg" } }
. "$PSScriptRoot\documented-helper.ps1"
[IO.File]::WriteAllText("$env:TL_PW_RUN\shell-version-$Step.json", (@{version=$PSVersionTable.PSVersion.ToString();edition=$PSVersionTable.PSEdition}|ConvertTo-Json -Compress))
if($Step -eq 'cleanup') { . "$PSScriptRoot\documented-cleanup.ps1"; exit 0 }
$parts = [string[]]@(Get-Content -LiteralPath $ArgumentsFile -Raw -Encoding UTF8 | ConvertFrom-Json)
Invoke-PwGhi -Ten $Step -Argv $parts
exit 0
