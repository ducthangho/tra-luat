function Invoke-PwGhi([string]$Ten, [string[]]$Argv, [switch]$PhaiLoi) {
  $all = @($env:TL_PW_CLI, "--session=$env:TL_PW_SESSION") + $Argv + '--json'
  Need (-not ($all | Where-Object { $_ -match '"' -or $_ -match '\\$' })) 'đối số có dấu nháy kép hoặc \ ở cuối'
  $line = ($all | ForEach-Object { '"' + $_ + '"' }) -join ' '; $t0 = [DateTime]::UtcNow.ToString('o')
  Add-Content -LiteralPath "$env:TL_PW_RUN\commands.tsv" -Encoding UTF8 -ErrorAction Stop `
    -Value "$t0`t$Ten`t$env:TL_PW_NODE $line`trc=PENDING"
  $p = $null
  try {
    $p = Start-Process -FilePath $env:TL_PW_NODE -ArgumentList $line -WorkingDirectory "$env:TL_PW_ROOT\work" -NoNewWindow `
      -PassThru -RedirectStandardOutput "$env:TL_PW_RUN\$Ten.json" -RedirectStandardError "$env:TL_PW_RUN\$Ten.err" -ErrorAction Stop
  } catch {
    Add-Content -LiteralPath "$env:TL_PW_RUN\commands.tsv" -Encoding UTF8 -ErrorAction Stop `
      -Value "$t0`t$Ten`t$env:TL_PW_NODE $line`trc=NOT_MEASURED`tstart_failed=$($_.Exception.Message)"
    throw
  }
  Need ($p -is [Diagnostics.Process]) "$Ten thiếu process thật"
  $null = $p.Handle; $p.WaitForExit()
  $rc = $p.ExitCode; Need ($p.HasExited -and $rc -is [int]) "$Ten thiếu exit code thật"
  Add-Content -LiteralPath "$env:TL_PW_RUN\commands.tsv" -Encoding UTF8 -ErrorAction Stop `
    -Value "$t0`t$Ten`t$env:TL_PW_NODE $line`trc=$rc`t$([DateTime]::UtcNow.ToString('o'))"
  $expectedRc = 0; if ($PhaiLoi) { $expectedRc = 1 }
  Need ($rc -eq $expectedRc) "$Ten rc=$rc — chạy Cleanup" }
