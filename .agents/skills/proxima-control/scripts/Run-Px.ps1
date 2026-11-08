#requires -Version 5.1
# Run-Px.ps1 - wp1279 r2 (PROXIMA-P1-S2). Thin wrapper over px from the SIBLING ProximaControl.psm1 (direct .psm1, no PSD1
# until S3). An already-loaded ProximaControl is reused only when it is this exact path - never re-imported with -Force,
# which would reset its session state; one loaded from any other path fails closed (ProximaControl.ModuleConflict).
# Forwards only the bound business parameters, the EFFECTIVE WhatIf (explicitly: a module does not see this script's
# preference variables, so ambient WhatIf would otherwise be lost) and a bound -Confirm. px owns ShouldProcess.
# No default target, connection, credential or environment lookup; no autoconnect. State lives in THIS PowerShell process:
# connect, then another Run-Px call in the same process reuses the session; a fresh process starts disconnected.
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium', PositionalBinding = $false)]
param([Parameter(Position = 0)][string]$Action = 'help', [Parameter(Position = 1)][string]$Provider, [Parameter(Position = 2)][string]$Value,
    [string]$ConfigPath, [string]$RepositoryRoot, [string]$TargetId, [string]$Model, [pscredential]$Credential, [switch]$Force)
Set-StrictMode -Version 3.0
$ErrorActionPreference = 'Stop'
$pxPath = [IO.Path]::GetFullPath([IO.Path]::Combine($PSScriptRoot, 'ProximaControl.psm1'))
$pxMod = $null
foreach ($loaded in @(Get-Module -Name 'ProximaControl')) {
    if (-not [string]::Equals([IO.Path]::GetFullPath($loaded.Path), $pxPath, [StringComparison]::OrdinalIgnoreCase)) {
        $PSCmdlet.ThrowTerminatingError([Management.Automation.ErrorRecord]::new([InvalidOperationException]::new('ProximaControl: operation rejected: ModuleConflict.'),
                'ProximaControl.ModuleConflict', 'InvalidOperation', $null))
    }
    $pxMod = $loaded
}
if ($null -eq $pxMod) { $pxMod = Import-Module -Name $pxPath -PassThru -DisableNameChecking -Global -ErrorAction Stop }
$pxArgs = @{}
foreach ($n in 'Action', 'Provider', 'Value', 'ConfigPath', 'RepositoryRoot', 'TargetId', 'Model', 'Credential', 'Force') {
    if ($PSBoundParameters.ContainsKey($n)) { $pxArgs[$n] = $PSBoundParameters[$n] }
}
$pxArgs['WhatIf'] = [bool]$WhatIfPreference
if ($PSBoundParameters.ContainsKey('Confirm')) { $pxArgs['Confirm'] = $PSBoundParameters['Confirm'] }
& $pxMod.ExportedCommands['px'] @pxArgs
