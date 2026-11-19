$W = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS'
[string]$k = Get-Content -Raw 'F:\tl-win\KHOA.txt'
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k"; exit 3 }
python -X utf8 -c "import base64,hashlib;W=r'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS';b=base64.b64decode(open(W+r'\do1425.b64').read().strip());open(W+r'\do1425.py','wb').write(b);print('do1425',hashlib.sha256(b).hexdigest());print('rigb64',hashlib.sha256(open(W+r'\rig433c1.b64','rb').read().strip()).hexdigest())"
Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'do1425.py'),$W) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $W 'do1425.stdout.txt') -RedirectStandardError (Join-Path $W 'do1425.stderr.txt') -PassThru | Select-Object Id
