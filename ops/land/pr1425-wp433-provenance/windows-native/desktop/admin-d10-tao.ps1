$OUT = 'F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS\wp433c1-out-20261119T151704Z\ADMIN-D10-TAO.txt'
"bat_dau=" + (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ') + " admin=" + ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator) | Out-File -Encoding utf8 $OUT
"`$ fsutil 8dot3name query F:" | Out-File -Append -Encoding utf8 $OUT
fsutil 8dot3name query F: 2>&1 | Out-File -Append -Encoding utf8 $OUT
"rc=$LASTEXITCODE" | Out-File -Append -Encoding utf8 $OUT
"`$ net share wp433c1=... /grant:desktop-t9r33p2\thanghd,FULL" | Out-File -Append -Encoding utf8 $OUT
net share "wp433c1=F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS\tmp433c1-20261119T151704Z\wp433c1-d10-223323-4qb2fu4p" '/grant:desktop-t9r33p2\thanghd,FULL' 2>&1 | Out-File -Append -Encoding utf8 $OUT
"rc=$LASTEXITCODE" | Out-File -Append -Encoding utf8 $OUT
"ket_thuc=" + (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ') | Out-File -Append -Encoding utf8 $OUT
