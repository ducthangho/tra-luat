& { $ErrorActionPreference = 'Stop'
  $session = $env:TL_PW_SESSION
  Need ($session -cmatch '\Atl-pw-[0-9a-f]{12}\z') 'nonce không hợp lệ'
  foreach ($ten in '08-close', '09-delete-data', '10-verify') {
    foreach ($ext in 'json', 'err') {
      Need (-not (Test-Path -LiteralPath "$env:TL_PW_RUN\$ten.$ext")) "output cũ $ten.$ext, không ghi đè"
    }
  }
  # Chỉ so nguyên byte các phản hồi cố định; không phân tích JSON/trang.
  function Assert-PwCleanupOutput([string]$Ten, [string[]]$Expected) {
    $outPath = "$env:TL_PW_RUN\$Ten.json"; $errPath = "$env:TL_PW_RUN\$Ten.err"
    Need ((Test-Path -LiteralPath $outPath -PathType Leaf) -and
      (Test-Path -LiteralPath $errPath -PathType Leaf)) "$Ten thiếu output"
    Need (([IO.File]::ReadAllBytes($errPath)).Length -eq 0) "$Ten có stderr"
    $actual = [Convert]::ToBase64String([IO.File]::ReadAllBytes($outPath))
    $matchedOutputs = @($Expected | Where-Object {
      [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($_)) -ceq $actual })
    Need ($matchedOutputs.Count -eq 1) "$Ten thiếu/sai phản hồi đúng phiên"
  }
  Invoke-PwGhi 08-close @('close')
  Assert-PwCleanupOutput 08-close @("{`n  `"session`": `"$session`",`n  `"status`": `"closed`"`n}`n")
  Invoke-PwGhi 09-delete-data @('delete-data')
  Assert-PwCleanupOutput 09-delete-data @(
    "{`n  `"session`": `"$session`",`n  `"deleted`": false`n}`n",
    "{`n  `"session`": `"$session`",`n  `"deleted`": true`n}`n")
  Invoke-PwGhi 10-verify @('tab-list') -PhaiLoi
  Assert-PwCleanupOutput 10-verify @("{`n  `"isError`": true,`n  `"error`": `"The browser '$session' is not open, please run open first`"`n}`n")
  $h = Get-ChildItem -Force -File -LiteralPath $env:TL_PW_RUN | Where-Object Name -ne 'SHA256SUMS.csv' |
    Select-Object FullName, Length, @{ n = 'SHA256'; e = { (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash } }
  $h | Export-Csv -LiteralPath "$env:TL_PW_RUN\SHA256SUMS.csv" -NoTypeInformation -Encoding UTF8 -ErrorAction Stop
  'CLEANUP OK' }
