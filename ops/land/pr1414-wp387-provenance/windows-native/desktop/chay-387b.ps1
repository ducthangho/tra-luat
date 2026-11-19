$W = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS'
(Get-FileHash -Algorithm SHA256 (Join-Path $W 'do387.py')).Hash
Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'do387.py'),$W) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $W 'do387.stdout.txt') -RedirectStandardError (Join-Path $W 'do387.stderr.txt') -PassThru | Select-Object Id
