$W = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS'
python -X utf8 -c "import base64,hashlib;W=r'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS';b=base64.b64decode(open(W+r'\do1425b.b64').read().strip());open(W+r'\do1425b.py','wb').write(b);print('do1425b',hashlib.sha256(b).hexdigest())"
Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'do1425b.py'),$W) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $W 'do1425b.stdout.txt') -RedirectStandardError (Join-Path $W 'do1425b.stderr.txt') -PassThru | Select-Object Id
