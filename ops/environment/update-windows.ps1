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
function Sync-ToolPath([string]$baselineTool = '') {
    # Fixed installation locations only; never import a child PATH or installer stdout.
    $directories = @(
        (Join-Path $env:USERPROFILE '.local\bin'),
        (Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Links'),
        (Join-Path $env:ProgramData 'chocolatey\bin'),
        (Join-Path $env:ProgramFiles 'nodejs'),
        (Join-Path $env:ProgramFiles 'GitHub CLI'),
        (Join-Path $env:APPDATA 'npm'),
        (Join-Path $env:LOCALAPPDATA 'tra-luat-tools\venv\Scripts'),
        (Join-Path $env:LOCALAPPDATA 'agy\bin')
    )
    $choco = Get-Command choco -CommandType Application -ErrorAction SilentlyContinue
    if ($choco) { $directories += Split-Path $choco.Source -Parent }
    foreach ($directory in $directories) {
        if (-not (Test-Path -LiteralPath $directory -PathType Container)) { continue }
        # Add a known bin for unresolved tools, or promote a checker-verified repaired baseline.
        foreach ($tool in @('rg','shellcheck','actionlint','gh','node','npm','uv','claude','codex','nlm','gws','agy')) {
            if ($baselineTool -cne $tool -and (Get-Command $tool -ErrorAction SilentlyContinue)) { continue }
            if ((Test-Path -LiteralPath (Join-Path $directory "$tool.exe") -PathType Leaf) -or
                (Test-Path -LiteralPath (Join-Path $directory "$tool.cmd") -PathType Leaf)) {
                if ($baselineTool -ceq $tool) {
                    $previousPath = $env:Path
                    $accepted = $false
                    try {
                        $env:Path = "$directory;$previousPath"
                        $json = @(& python $checker kiem-tra --chi $tool --json)
                        $rc = $LASTEXITCODE
                        $result = ($json -join [Environment]::NewLine) | ConvertFrom-Json
                        $entries = @($result.cong_cu)
                        $accepted = $rc -eq 0 -and $entries.Count -eq 1 -and
                            $entries[0].ten -ceq $tool -and $entries[0].trang_thai -ceq 'DAT'
                    } finally { $env:Path = $previousPath }
                    if (-not $accepted) { continue }
                    $remaining = @($env:Path -split ';' | Where-Object { $_ -and -not (Test-PathListContains $_ $directory) })
                    $env:Path = (@($directory) + $remaining) -join ';'
                } elseif (-not (Test-PathListContains $env:Path $directory)) {
                    # Append supplemental bins so the uv venv's python cannot shadow the baseline Python.
                    $env:Path = "$env:Path;$directory"
                }
            }
        }
    }
    # A promoted user bin must not shadow Git Bash with another bash.exe.
    Sync-GitBashPath
}
function Assert-ChocoReady {
    if (-not (Get-Command choco -CommandType Application -ErrorAction SilentlyContinue)) {
        throw 'This installation needs existing Chocolatey. Provision it separately, then rerun; this script does not bootstrap a package manager.'
    }
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    try { $admin = ([Security.Principal.WindowsPrincipal]::new($identity)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator) }
    finally { $identity.Dispose() }
    if (-not $admin) { throw 'Chocolatey system packages require an already elevated PowerShell. No elevation will be requested automatically.' }
}
function Test-ToolReady([string]$name) {
    $command = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $command) { return $false }
    $output = @(& $command.Source --version 2>$null)
    return ($LASTEXITCODE -eq 0 -and ($output -join '').Trim().Length -gt 0)
}
function Get-AgyVersion([string]$executable) {
    $lines = @(& $executable --version 2>$null)
    if ($LASTEXITCODE -ne 0) { return $null }
    $versions = @($lines | ForEach-Object {
        if ([string]$_ -cmatch '^\s*(?:version:\s*|agy\s+|antigravity\s+)?v?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)\s*$') { $Matches[1] }
    })
    if ($versions.Count -eq 1) { return $versions[0] }
    return $null
}
function Install-AgyVerified {
    $arch = switch ([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()) {
        'X64' { 'x64' }
        'Arm64' { 'arm64' }
        default { throw 'Unsupported AGY CPU architecture' }
    }
    $release = Invoke-RestMethod -Uri 'https://api.github.com/repos/google-antigravity/antigravity-cli/releases/latest' -Headers @{ 'User-Agent'='tra-luat-env-setup' } -TimeoutSec 30
    $tag = [string]$release.tag_name
    if ($tag -cnotmatch '^v?\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$') { throw 'Invalid AGY release tag' }
    $target = $tag -creplace '^v',''
    $assets = @($release.assets | Where-Object { $_.name -ceq "agy_cli_windows_$arch.zip" })
    if ($assets.Count -ne 1) { throw 'Expected exactly one AGY Windows release asset' }
    $asset = $assets[0]
    if ([string]$asset.digest -cnotmatch '^sha256:[0-9a-f]{64}$') { throw 'AGY release has no valid SHA256 digest' }
    $expectedUrl = "https://github.com/google-antigravity/antigravity-cli/releases/download/$tag/$($asset.name)"
    if ([string]$asset.browser_download_url -cne $expectedUrl) { throw 'Unexpected AGY asset URL' }
    $bin = Join-Path $env:LOCALAPPDATA 'agy\bin'
    $destination = Join-Path $bin 'agy.exe'
    $current = Get-Command agy -ErrorAction SilentlyContinue
    if ($current -and (Get-AgyVersion $current.Source) -ceq $target) { return }
    # Refuse reparse points in the installation path rather than following a redirected user bin.
    for ($parent = $destination; $parent; $parent = Split-Path $parent -Parent) {
        if ((Test-Path -LiteralPath $parent) -and
            ((Get-Item -LiteralPath $parent -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "AGY install path contains a reparse point: $parent"
        }
    }
    $tmp = Join-Path ([IO.Path]::GetTempPath()) ("tra-luat-agy-" + [guid]::NewGuid().ToString('N'))
    $staged = $null
    New-Item -ItemType Directory -Path $tmp | Out-Null
    try {
        $archive = Join-Path $tmp 'release.zip'
        Invoke-WebRequest -Uri $expectedUrl -OutFile $archive -TimeoutSec 120
        if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -cne ([string]$asset.digest).Substring(7)) {
            throw 'AGY SHA256 mismatch'
        }
        $zip = [IO.Compression.ZipFile]::OpenRead($archive)
        try {
            # Only one regular root executable is accepted; no paths, duplicates, links or extra files.
            if ($zip.Entries.Count -ne 1) { throw 'Unexpected AGY archive layout' }
            $entry = $zip.Entries[0]
            $unixType = ($entry.ExternalAttributes -shr 16) -band 0xF000
            if ($entry.FullName -cne 'antigravity.exe' -or $entry.Length -le 0 -or
                $unixType -notin @(0, 0x8000) -or ($entry.ExternalAttributes -band 0x410)) {
                throw 'Unexpected AGY archive entry'
            }
            $candidate = Join-Path $tmp 'agy.exe'
            [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $candidate, $false)
        } finally { $zip.Dispose() }
        if ((Get-AgyVersion $candidate) -cne $target) { throw "AGY archive binary did not report $target" }
        New-Item -ItemType Directory -Path $bin -Force | Out-Null
        # Stage on the destination volume; Replace/Move publish a complete binary atomically.
        $staged = Join-Path $bin ('.agy-' + [guid]::NewGuid().ToString('N') + '.exe')
        [IO.File]::Copy($candidate, $staged, $false)
        if (Test-Path -LiteralPath $destination) { [IO.File]::Replace($staged, $destination, $null) }
        else { [IO.File]::Move($staged, $destination) }
        if (-not (Test-PathListContains $env:Path $bin)) { $env:Path = "$bin;$env:Path" }
        $resolved = Get-Command agy -ErrorAction Stop
        if ($resolved.Source -ine $destination) { throw 'AGY is shadowed on PATH' }
        if ((Get-AgyVersion $destination) -cne $target) { throw "AGY did not reach $target" }
    } finally {
        if ($staged -and (Test-Path -LiteralPath $staged)) { Remove-Item -LiteralPath $staged -Force }
        Remove-Item -LiteralPath $tmp -Recurse -Force
    }
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
function Sync-GitBashPath {
    # Python's checker also resolves bare bash through the parent's process PATH.
    # Promote the Git bin even when already present later, ahead of a WSL launcher.
    $directory = Split-Path $gitBash -Parent
    $remaining = @($env:Path -split ';' | Where-Object { $_ -and -not (Test-PathListContains $_ $directory) })
    $env:Path = (@($directory) + $remaining) -join ';'
}
$repoPath = (Resolve-Path -LiteralPath $Repo).Path
$manifest = Join-Path $repoPath 'ops\cong_cu.yaml'
$checker = Join-Path $repoPath 'ops\cong_cu.py'
$installer = Join-Path $repoPath 'ops\cai_cong_cu.sh'
$gitExe = (Get-Command git -ErrorAction Stop).Source
foreach ($path in @($manifest, $checker, $installer)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing repository file: $path" }
}
# Resolve before check-only too; change only this process's PATH, never persistent PATH.
$gitBash = Resolve-GitTool $gitExe 'bin\bash.exe'
if (-not $gitBash) { throw "Git Bash not found near $gitExe" }
Sync-GitBashPath
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
# Only apply needs path translation for the shared installer.
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
    Sync-ToolPath
    # Plan missing system prerequisites before any package mutation. Never self-elevate.
    $missingNode = -not (Test-ToolReady 'node')
    $missingNpm = -not (Test-ToolReady 'npm')
    if (-not $missingNode -and $missingNpm) {
        throw 'Node is present but npm is missing or broken. Repair that Node installation first; refusing to replace an existing Node major.'
    }
    $systemPackages = @()
    if (-not (Test-ToolReady 'gh')) { $systemPackages += 'gh' }
    if ($missingNode) { $systemPackages += 'nodejs-lts' }
    if ($systemPackages.Count -or ($Latest -and @($Tools | Where-Object { $_ -in @('git','python','rg','shellcheck','gh','node','pwsh') }).Count)) {
        Assert-ChocoReady
    }
    & python -c 'import yaml' 2>$null
    if ($LASTEXITCODE -ne 0) { Run 'python' @('-m','pip','install','PyYAML==6.0.3') }
    # Preserve sufficient baseline versions. ShellCheck must precede the actionlint canary.
    foreach ($baseline in @('git','python','PyYAML','jsonschema','shellcheck','rg','bash','actionlint')) {
        $json = @(& python $checker kiem-tra --chi $baseline --json)
        $probeExit = $LASTEXITCODE
        $probe = ($json -join [Environment]::NewLine) | ConvertFrom-Json
        $entries = @($probe.cong_cu)
        if ($entries.Count -ne 1 -or $entries[0].ten -cne $baseline) { throw "Invalid baseline probe: $baseline" }
        if ($probeExit -eq 0 -and $entries[0].trang_thai -ceq 'DAT') { continue }
        if ($baseline -in @('git','python','shellcheck','rg','bash')) { Assert-ChocoReady }
        $previousActionlintDir = $env:AL_DICH
        try {
            if ($baseline -ceq 'actionlint') {
                # The shared default is a child-only temp bin; use a known parent candidate.
                $userBin = Join-Path $env:USERPROFILE '.local\bin'
                $translated = @(& $cygpath -u $userBin)
                if ($LASTEXITCODE -ne 0 -or $translated.Count -ne 1 -or
                    [string]::IsNullOrWhiteSpace([string]$translated[0])) {
                    throw 'Could not translate actionlint user bin for Git Bash'
                }
                $env:AL_DICH = ([string]$translated[0]).Trim()
            }
            & $gitBash $unixInstaller $baseline
            if ($LASTEXITCODE -ne 0) { throw "Base tool installer for $baseline exited $LASTEXITCODE" }
        } finally { $env:AL_DICH = $previousActionlintDir }
        Sync-ToolPath $baseline
        # Measure in the parent, which does not inherit the Git Bash installer's PATH.
        $json = @(& python $checker kiem-tra --chi $baseline --json)
        $probeExit = $LASTEXITCODE
        $probe = ($json -join [Environment]::NewLine) | ConvertFrom-Json
        $entries = @($probe.cong_cu)
        if ($probeExit -ne 0 -or $entries.Count -ne 1 -or $entries[0].ten -cne $baseline -or
            $entries[0].trang_thai -cne 'DAT') { throw "Baseline tool not DAT in PowerShell parent: $baseline" }
    }
    foreach ($package in $systemPackages) {
        Run 'choco' @('install', $package, '--yes', '--no-progress')
        Sync-ToolPath
    }
    foreach ($prerequisite in @('gh','node','npm')) {
        if (-not (Test-ToolReady $prerequisite)) { throw "Supplemental prerequisite not usable: $prerequisite" }
    }
    if (-not (Test-ToolReady 'uv')) {
        $toolVenv = Join-Path $env:LOCALAPPDATA 'tra-luat-tools\venv'
        $venvPython = Join-Path $toolVenv 'Scripts\python.exe'
        if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) { Run 'python' @('-m','venv',$toolVenv) }
        & $venvPython -m pip install --disable-pip-version-check uv
        if ($LASTEXITCODE -ne 0) { throw "uv installation exited $LASTEXITCODE" }
        Sync-ToolPath
    }
    if (-not (Test-ToolReady 'uv')) { throw 'uv is not usable after installation' }
    foreach ($cli in @('claude','codex','gws')) {
        if (Test-ToolReady $cli) { continue }
        $package = @{ claude='@anthropic-ai/claude-code'; codex='@openai/codex'; gws='@googleworkspace/cli' }[$cli]
        Run 'npm' @('install','--global','--prefix',(Join-Path $env:APPDATA 'npm'),$package,'--no-fund','--no-audit')
        Sync-ToolPath
        if (-not (Test-ToolReady $cli)) { throw "$cli is not usable after installation (check PATH shadowing)" }
    }
    if (-not (Test-ToolReady 'nlm')) {
        Run 'uv' @('tool','install','notebooklm-mcp-cli')
        Sync-ToolPath
        if (-not (Test-ToolReady 'nlm')) { throw 'nlm is not usable after installation (check uv tool directory and PATH shadowing)' }
    }
    if (-not (Test-ToolReady 'agy')) { Install-AgyVerified }
    if ($PersistPath) {
        $npmCommand = Get-Command npm -ErrorAction SilentlyContinue
        foreach ($directory in @((Join-Path $env:USERPROFILE '.local\bin'),
            (Join-Path $env:LOCALAPPDATA 'agy\bin'), (Join-Path $env:APPDATA 'npm'),
            (Join-Path $env:LOCALAPPDATA 'tra-luat-tools\venv\Scripts'),
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
                    $target = ((Invoke-RestMethod -Uri 'https://api.github.com/repos/anthropics/claude-code/releases/latest' -TimeoutSec 20).tag_name -replace '^v','')
                    if (((Version 'claude' @('--version')) -split '\s+')[0] -cne $target) { Run 'claude' @('update') }
                    if (((Version 'claude' @('--version')) -split '\s+')[0] -cne $target) { throw "Claude did not reach $target" }
                }
                'agy' { Install-AgyVerified }
                'nlm' {
                    $target = (Invoke-RestMethod -Uri 'https://pypi.org/pypi/notebooklm-mcp-cli/json' -TimeoutSec 20).info.version
                    if (((Version 'nlm' @('--version')) -split '\s+')[-1] -cne $target) { Run 'uv' @('tool', 'upgrade', 'notebooklm-mcp-cli') }
                    if (((Version 'nlm' @('--version')) -split '\s+')[-1] -cne $target) { throw "nlm did not reach $target" }
                }
                { $_ -in @('git','python','rg','shellcheck','gh','node','pwsh') } {
                    $package = @{ git='git'; python='python'; rg='ripgrep'; shellcheck='shellcheck'; gh='gh'; node='nodejs-lts'; pwsh='powershell-core' }[$item]
                    Run 'choco' @('upgrade', $package, '--yes', '--no-progress')
                }
                'uv' {
                    $target = (Invoke-RestMethod -Uri 'https://pypi.org/pypi/uv/json' -TimeoutSec 20).info.version
                    if (((Version 'uv' @('--version')) -split '\s+')[1] -cne $target) {
                        $managedPython = Join-Path $env:LOCALAPPDATA 'tra-luat-tools\venv\Scripts\python.exe'
                        $managedUv = Join-Path $env:LOCALAPPDATA 'tra-luat-tools\venv\Scripts\uv.exe'
                        if ((Get-Command uv).Source -ieq $managedUv) {
                            & $managedPython -m pip install --disable-pip-version-check --upgrade "uv==$target"
                            if ($LASTEXITCODE -ne 0) { throw "uv upgrade exited $LASTEXITCODE" }
                        } else { Run 'python' @('-m','pip','install','--upgrade',"uv==$target") }
                    }
                    if (((Version 'uv' @('--version')) -split '\s+')[1] -cne $target) { throw "uv did not reach $target" }
                }
                'npm' { Run 'npm' @('install','-g','npm@latest','--no-fund','--no-audit') }
            }
        }
    }
    Sync-ToolPath
    foreach ($required in @('git','python','rg','shellcheck','actionlint','gh','node','npm','pwsh','uv','claude','codex','agy','nlm','gws')) {
        if (-not (Get-Command $required -ErrorAction SilentlyContinue)) { throw "Required executor/reviewer tool missing: $required" }
    }
    Write-Host 'Versions after update:'
    foreach ($name in @('claude','codex','agy','nlm','gws')) {
        '{0,-8} {1}' -f $name, (Version $name @('--version'))
    }
    Run 'python' @($checker, 'kiem-tra', '--json')
} finally { Pop-Location }
