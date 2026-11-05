# Dot-source this file from a PowerShell profile or an interactive session:
#   . 'C:\path\to\tra-luat\ops\environment\login-windows.ps1'
# It only adds existing user CLI directories to this session's PATH and sets TL_REPO.
# It never installs software, edits profiles, logs in, or reads/stores TL_MASTER_KEY.
if ($MyInvocation.InvocationName -ne '.') {
    Write-Warning 'login-windows.ps1 must be dot-sourced: . .\ops\environment\login-windows.ps1'
    return
}
& {
    $repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
    $candidates = @(
        (Join-Path $HOME '.local\bin'),
        $(if ($env:APPDATA) { Join-Path $env:APPDATA 'npm' }),
        $(if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'agy\bin' }),
        $(if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'tra-luat-tools\venv\Scripts' }),
        (Join-Path $HOME '.cargo\bin')
    ) | Where-Object { $_ }
    foreach ($dir in $candidates) {
        $present = @($env:Path -split ';' | Where-Object { $_ -and $_.TrimEnd('\') -ieq $dir.TrimEnd('\') })
        if ((Test-Path -LiteralPath $dir -PathType Container) -and -not $present.Count) {
            if ($env:LOCALAPPDATA -and $dir -ieq (Join-Path $env:LOCALAPPDATA 'tra-luat-tools\venv\Scripts')) {
                # Expose uv without replacing the caller's baseline Python with the tool venv.
                $env:Path = "$env:Path;$dir"
            } else { $env:Path = "$dir;$env:Path" }
        }
    }
    $env:TL_REPO = $repo
    Write-Host "tra-luat session: $repo"
    Write-Host 'Check: pwsh -File ops/environment/update-windows.ps1 -Repo .'
    Write-Host 'Health: python scripts/tl.py doctor --offline'
}
