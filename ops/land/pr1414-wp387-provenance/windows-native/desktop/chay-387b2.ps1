$W = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS'
[string]$k = Get-Content -Raw 'F:\tl-win\KHOA.txt'
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k"; exit 3 }
python -c "import hashlib;print(hashlib.sha256(open(r'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS\do387b.py','rb').read()).hexdigest())"
Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'do387b.py'),$W) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $W 'do387b.stdout.txt') -RedirectStandardError (Join-Path $W 'do387b.stderr.txt') -PassThru | Select-Object Id
