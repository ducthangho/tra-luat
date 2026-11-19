$W = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS'
[string]$k = Get-Content -Raw 'F:\tl-win\KHOA.txt'
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k"; exit 3 }
python -X utf8 -c "import base64,zipfile,io,hashlib;W=r'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS';b=base64.b64decode(open(W+r'\pack1420.b64').read().strip());print('zip',hashlib.sha256(b).hexdigest());z=zipfile.ZipFile(io.BytesIO(b));[open(W+'\\'+n,'wb').write(z.read(n)) or print(n,hashlib.sha256(z.read(n)).hexdigest()) for n in z.namelist()]"
Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'do1420.py'),$W) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $W 'do1420.stdout.txt') -RedirectStandardError (Join-Path $W 'do1420.stderr.txt') -PassThru | Select-Object Id
