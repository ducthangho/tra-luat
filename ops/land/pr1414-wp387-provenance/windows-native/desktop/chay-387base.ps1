$W = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS'
[string]$k = Get-Content -Raw 'F:\tl-win\KHOA.txt'
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k"; exit 3 }
Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'do387base.py'),$W) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $W 'do387base.stdout.txt') -RedirectStandardError (Join-Path $W 'do387base.stderr.txt') -PassThru | Select-Object Id
