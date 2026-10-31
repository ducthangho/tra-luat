param([string]$Product="$PSScriptRoot/../copies/head/ops/vm/cap-nhat-cong-cu.ps1")
$ErrorActionPreference='Stop';$t=$null;$e=$null
$ast=[Management.Automation.Language.Parser]::ParseFile((Resolve-Path $Product),[ref]$t,[ref]$e)
$cmds=@($ast.FindAll({param($n) $n -is [Management.Automation.Language.CommandAst] -and $n.GetCommandName() -eq 'Add-KetQua'},$true))
$nonloi=@($cmds | Where-Object { $_.CommandElements[4].Extent.Text -ne "'loi'" } | ForEach-Object {
 $p=$_.Parent;while($p -and $p -isnot [Management.Automation.Language.FunctionDefinitionAst]){$p=$p.Parent}
 [pscustomobject]@{line=$_.Extent.StartLineNumber;function=$p.Name;action=$_.CommandElements[4].Extent.Text;command=$_.Extent.Text}
})
$test=Join-Path (Split-Path $Product) 'cap-nhat-cong-cu_test.ps1'
$a=[Management.Automation.Language.Parser]::ParseFile((Resolve-Path $test),[ref]$t,[ref]$e)
$cases=@($a.FindAll({param($n) $n -is [Management.Automation.Language.CommandAst] -and $n.GetCommandName() -eq 'Ca'},$true) | ForEach-Object {
 [pscustomobject]@{line=$_.Extent.StartLineNumber;name=$_.CommandElements[1].Value}
})
[ordered]@{parse_errors=$e.Count;add_count=$cmds.Count;nonloi_count=$nonloi.Count;nonloi=$nonloi;case_count=$cases.Count;unique_case_names=@($cases.name|Sort-Object -Unique).Count;cases=$cases} | ConvertTo-Json -Depth 5
