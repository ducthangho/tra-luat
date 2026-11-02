param([string]$Product = "$PSScriptRoot/../copies/head/ops/vm/cap-nhat-cong-cu.ps1")
$ErrorActionPreference='Stop'
$e=$null;$t=$null;$a=[Management.Automation.Language.Parser]::ParseFile((Resolve-Path $Product),[ref]$t,[ref]$e)
"parse_errors=$($e.Count); pwsh=$($PSVersionTable.PSVersion); os=$([Runtime.InteropServices.RuntimeInformation]::OSDescription)"
foreach($f in @('Invoke-Icacls','New-ThuMucTai','Register-LichCapNhat','Invoke-TangHeThong','Invoke-TangNguoiDung')) {
  $fn=$a.FindAll({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $f},$true)[0]
  "FUNCTION $f"
  $fn.FindAll({param($n) $n -is [Management.Automation.Language.CommandAst] -and $n.Extent.Text -match 'icacls|Invoke-Icacls|Start-Process|Install-Msi|Save-CoKiemBam|ScheduledTask|Copy-Item|Get-Acl|Get-FileHash|Set-Content|Invoke-WebRequest|Invoke-RestMethod'},$true)|ForEach-Object { "$($_.Extent.StartLineNumber): $($_.Extent.Text)" }
}
$readme=Get-Content "$PSScriptRoot/../copies/head/ops/vm/README.md" -Raw
"README_native_acl_commands=$(@($readme -split "`n" | Where-Object {$_ -match '^\s*(?:&\s+)?icacls\b'}).Count)"
