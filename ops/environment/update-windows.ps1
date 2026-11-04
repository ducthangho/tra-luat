#requires -Version 7.0
<#
Windows wrapper for the tra-luat tool manifest. Run from a tra-luat checkout:
  pwsh -File ops/environment/update-windows.ps1 -Repo .           # check only; exit code = checker exit code
  pwsh -File ops/environment/update-windows.ps1 -Repo . -Apply    # install missing baseline tools
This script reports only whether TL_* variables are set; it never prints their values,
reads credential files, changes ACLs, or registers background tasks.
#>
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Repo, [switch]$Apply, [switch]$Latest, [switch]$PersistPath,
      [ValidateSet('claude','codex','agy','nlm','gws','git','python','rg','shellcheck','gh','node','pwsh','uv','npm')][string[]]$Tools = @('claude','codex','agy','nlm','gws'))
$ErrorActionPreference = 'Stop'
if (($Latest -or $PersistPath) -and -not $Apply) { throw '-Latest and -PersistPath require -Apply' }
function Show-EnvironmentStatus {
    foreach ($name in @('TL_MASTER_KEY','TL_SECRETS_FILEID','TL_AGENT_CREDS_FILEID','TL_WEBAPP','TL_TOKEN','TL_PROFILE')) {
        $processSet = -not [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($name,'Process'))
        $userSet = -not [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($name,'User'))
        '{0,-23} process={1} user={2}' -f $name, $processSet, $userSet
    }
    if (-not [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable('TL_SECRETS_FILEID','Process')) -and
        [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable('TL_MASTER_KEY','Process'))) {
        Write-Warning 'Secrets file ID exists but TL_MASTER_KEY is absent from this process.'
    }
    $webapp = -not [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable('TL_WEBAPP','Process'))
    $token = -not [string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable('TL_TOKEN','Process'))
    if ($webapp -xor $token) { Write-Warning 'Only one of TL_WEBAPP/TL_TOKEN is set; verify config precedence.' }
    Write-Host 'Secrets are never copied to WSL or written to logs by this updater.'
}
function Test-PathListContains([string]$list, [string]$directory) {
    $wanted = [Environment]::ExpandEnvironmentVariables($directory).TrimEnd('\')
    foreach ($item in @($list -split ';' | Where-Object { $_ })) {
        if ([Environment]::ExpandEnvironmentVariables($item).TrimEnd('\') -ieq $wanted) { return $true }
    }
    return $false
}
function Add-UserPath([string]$directory) {
    if (-not $directory -or -not (Test-Path -LiteralPath $directory -PathType Container)) { return }
    # Read and write HKCU\Environment\Path raw: [Environment]::Get/SetEnvironmentVariable expands
    # %VAR% entries and rewrites the value as REG_SZ, silently destroying the user's references.
    $key = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment', $true)
    if (-not $key) { throw 'Cannot open HKCU\Environment for writing' }
    try {
        $raw = [string]$key.GetValue('Path', '', [Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
        if (-not (Test-PathListContains $raw $directory)) {
            $kind = [Microsoft.Win32.RegistryValueKind]::ExpandString
            if (($key.GetValueNames() -contains 'Path') -and
                $key.GetValueKind('Path') -eq [Microsoft.Win32.RegistryValueKind]::String) {
                $kind = [Microsoft.Win32.RegistryValueKind]::String
            }
            $items = @($raw -split ';' | Where-Object { $_ }) + $directory
            $key.SetValue('Path', ($items -join ';'), $kind)
            Write-Host "Added to user PATH: $directory"
        }
    } finally { $key.Dispose() }
    if (-not (Test-PathListContains $env:Path $directory)) { $env:Path = "$env:Path;$directory" }
}
function Resolve-GitTool([string]$gitExe, [string]$relative) {
    # git.exe may live in <GitRoot>\cmd, <GitRoot>\bin or <GitRoot>\mingw64\bin.
    $dir = Split-Path $gitExe -Parent
    for ($i = 0; $i -lt 3; $i++) {
        $dir = Split-Path $dir -Parent
        if (-not $dir) { break }
        $candidate = Join-Path $dir $relative
        if (Test-Path -LiteralPath $candidate -PathType Leaf) { return $candidate }
    }
    return $null
}
$repoPath = (Resolve-Path -LiteralPath $Repo).Path
$manifest = Join-Path $repoPath 'ops\cong_cu.yaml'
$checker = Join-Path $repoPath 'ops\cong_cu.py'
$installer = Join-Path $repoPath 'ops\cai_cong_cu.sh'
$gitExe = (Get-Command git -ErrorAction Stop).Source
foreach ($path in @($manifest, $checker, $installer)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing repository file: $path" }
}
function Run([string]$name, [string[]]$arguments) {
    $cmd = Get-Command $name -ErrorAction Stop
    & $cmd.Source @arguments
    if ($LASTEXITCODE -ne 0) { throw "$name exited $LASTEXITCODE" }
}
function Version([string]$name, [string[]]$arguments) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $cmd) { return '(missing)' }
    try {
        $lines = @(& $cmd.Source @arguments 2>$null)
        $versionLine = $lines | Where-Object { $_ -match '^version:\s*\d' } | Select-Object -First 1
        if ($versionLine) { return ([string]$versionLine).Trim() }
        return ([string]($lines | Select-Object -First 1)).Trim()
    }
    catch { return '(error)' }
}
foreach ($name in @('git','python','rg','shellcheck','actionlint','gh','node','npm','pwsh','uv','claude','codex','agy','nlm','gws')) {
    $arg = if ($name -eq 'actionlint') { @('-version') } else { @('--version') }
    '{0,-12} {1}' -f $name, (Version $name $arg)
}
Show-EnvironmentStatus
if (-not $Apply) {
    & python $checker kiem-tra --json
    $checkerExit = $LASTEXITCODE
    Write-Host "Checker exit code: $checkerExit. Add -Apply after related jobs finish."
    exit $checkerExit
}
# The shared installer needs Git Bash; a bare bash.exe on PATH may be the WSL launcher instead.
$gitBash = Resolve-GitTool $gitExe 'bin\bash.exe'
if (-not $gitBash) { throw "Git Bash not found near $gitExe" }
$cygpath = Resolve-GitTool $gitExe 'usr\bin\cygpath.exe'
if (-not $cygpath) { throw "Git cygpath not found near $gitExe" }
$active = @(Get-Process -ErrorAction Stop | Where-Object {
    $_.ProcessName -match '^(claude|codex|codex-command-runner.*|agy|nlm|gws|uv|node|python|pythonw|py|wsl|wslhost|vmmemWSL)$'
})
if ($active.Count) {
    $names = ($active | Select-Object -ExpandProperty ProcessName -Unique) -join ', '
    throw "Active tool/runtime processes: $names. Finish related jobs before updating."
}
Push-Location $repoPath
try {
    $unixInstaller = (& $cygpath -u $installer | Select-Object -First 1).Trim()
    if (-not $unixInstaller) { throw 'Could not translate installer path for Git Bash' }
    & $gitBash $unixInstaller --bat-buoc
    if ($LASTEXITCODE -ne 0) { throw "Base tool installer exited $LASTEXITCODE" }
    if ($PersistPath) {
        $npmCommand = Get-Command npm -ErrorAction SilentlyContinue
        foreach ($directory in @((Join-Path $env:USERPROFILE '.local\bin'),
            (Join-Path $env:LOCALAPPDATA 'agy\bin'), (Join-Path $env:APPDATA 'npm'),
            $(if ($npmCommand) { Split-Path $npmCommand.Source -Parent }),
            (Split-Path $gitExe -Parent))) { Add-UserPath $directory }
    }
    if ($Latest) {
        foreach ($item in $Tools) {
            switch ($item) {
                'codex' {
                    $target = (& npm view '@openai/codex' version | Select-Object -First 1).Trim()
                    if ($LASTEXITCODE -ne 0 -or -not $target) { throw 'Could not resolve latest Codex version' }
                    if (((Version 'codex' @('--version')) -split '\s+')[-1] -cne $target) {
                        Run 'npm' @('install', '-g', "@openai/codex@$target", '--no-fund', '--no-audit')
                    }
                    if (((Version 'codex' @('--version')) -split '\s+')[-1] -cne $target) { throw "Codex did not reach $target" }
                }
                'gws' {
                    $target = (& npm view '@googleworkspace/cli' version | Select-Object -First 1).Trim()
                    if ($LASTEXITCODE -ne 0 -or -not $target) { throw 'Could not resolve latest gws version' }
                    if (((Version 'gws' @('--version')) -split '\s+')[-1] -cne $target) {
                        Run 'npm' @('install', '-g', "@googleworkspace/cli@$target", '--no-fund', '--no-audit')
                    }
                    if (((Version 'gws' @('--version')) -split '\s+')[-1] -cne $target) { throw "gws did not reach $target" }
                }
                'claude' {
                    Run 'claude' @('update')
                    $target = ((Invoke-RestMethod -Uri 'https://api.github.com/repos/anthropics/claude-code/releases/latest' -TimeoutSec 20).tag_name -replace '^v','')
                    if (((Version 'claude' @('--version')) -split '\s+')[0] -cne $target) { throw "Claude did not reach $target" }
                }
                'agy' {
                    Run 'agy' @('update')
                    if ((Version 'agy' @('--version')) -notmatch '^\d+\.\d+\.\d+$') { throw 'AGY version could not be verified' }
                }
                'nlm' {
                    Run 'uv' @('tool', 'upgrade', 'notebooklm-mcp-cli')
                    $target = (Invoke-RestMethod -Uri 'https://pypi.org/pypi/notebooklm-mcp-cli/json' -TimeoutSec 20).info.version
                    if (((Version 'nlm' @('--version')) -split '\s+')[-1] -cne $target) { throw "nlm did not reach $target" }
                }
                { $_ -in @('git','python','rg','shellcheck','gh','node','pwsh') } {
                    $package = @{ git='git'; python='python'; rg='ripgrep'; shellcheck='shellcheck'; gh='gh'; node='nodejs-lts'; pwsh='powershell-core' }[$item]
                    Run 'choco' @('upgrade', $package, '--yes', '--no-progress')
                }
                'uv' { Run 'python' @('-m','pip','install','--upgrade','uv') }
                'npm' { Run 'npm' @('install','-g','npm@latest','--no-fund','--no-audit') }
            }
        }
    }
    foreach ($required in @('git','python','rg','shellcheck','actionlint','gh','node','npm','pwsh','uv','claude','codex','agy','nlm','gws')) {
        if (-not (Get-Command $required -ErrorAction SilentlyContinue)) { throw "Required executor/reviewer tool missing: $required" }
    }
    Write-Host 'Versions after update:'
    foreach ($name in @('claude','codex','agy','nlm','gws')) {
        '{0,-8} {1}' -f $name, (Version $name @('--version'))
    }
    Run 'python' @($checker, 'kiem-tra', '--json')
} finally { Pop-Location }
