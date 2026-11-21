$W = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS'
[string]$k = Get-Content -Raw 'F:\tl-win\KHOA.txt'
if ($null -eq $k) { $k = '' }
if ($k.Trim() -ne '') { "KHOA BAN: $k"; exit 3 }
python -X utf8 -c "import base64,hashlib;W=r'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS';b=base64.b64decode(open(W+r'\do1441.b64').read().strip());open(W+r'\do1441.py','wb').write(b);print('do1441',hashlib.sha256(b).hexdigest());print('rigb64',hashlib.sha256(open(W+r'\rig441.b64','rb').read().strip()).hexdigest())"
if ($args.Count -gt 0 -and $args[0] -eq 'chay') {
  Start-Process -FilePath python -ArgumentList @('-X','utf8','-B',(Join-Path $W 'do1441.py'),$W) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $W 'do1441.stdout.txt') -RedirectStandardError (Join-Path $W 'do1441.stderr.txt') -PassThru | Select-Object Id
}
