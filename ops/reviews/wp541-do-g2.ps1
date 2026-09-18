# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong, khong can gi khac):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
#
# Khong can tai them tep nao. Bo do Python nam NGAY TRONG tep nay (base64) va
# duoc kiem toan ven bang SHA-256 truoc khi chay.
#
# rc:  0 = moi chot dat | 1 = co chot truot | 3 = KHONG DO DUOC (nen do sai)
#
# Toan tep la ASCII thuan, co chu de bo giai ma cua PowerShell 5.1 khong lam hong
# ky tu nao. Duong dan co dau tieng Viet van chay binh thuong (xu ly luc chay).

param(
    [string]$Base    = '',     # thu muc lam viec. Mac dinh: thu muc chua chinh tep nay
    [string]$Nguon   = '',     # kho co san dung lam nguon clone (nhanh hon). Mac dinh: <Base>\tl546
    [string]$Kho     = '',     # clone RIENG de do.                            Mac dinh: <Base>\tl541-do
    [string]$Py      = '',     # duong dan python neu muon chi dinh
    [switch]$ChiGiaiNen,       # chi ghi bo do Python ra dia roi dung (de doc/kiem)
    [switch]$BoQuaTaiCongCu    # khong tu tai git/python; thieu la dung han
)

$ErrorActionPreference = 'Stop'
try { chcp 65001 > $null } catch {}
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}
try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch {}
$ProgressPreference = 'SilentlyContinue'   # Invoke-WebRequest nhanh hon nhieu khi tat thanh tien do
$script:GitExe = $null                     # duong dan git DA RESOLVE, dat o buoc cong cu

# Bat MOI loi khong luong truoc -> rc=3. Vi sao khong de mac dinh: PowerShell tra rc=1
# khi script chet vi ngoai le, ma rc=1 o day DA CO NGHIA "co chot truot". Hai thu khac
# han nhau - mot ben la phep do chay xong va truot, mot ben la phep do chua he chay.
trap {
    Write-Host ''
    Write-Host "KHONG DO DUOC: loi khong luong truoc - $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  tai: $($_.InvocationInfo.ScriptLineNumber): $($_.InvocationInfo.Line.Trim())" -ForegroundColor Red
    Write-Host 'Khong ket luan gi.' -ForegroundColor Red
    exit 3
}

# ---------------------------------------------------------------- hang so DA DO
$Url        = 'https://github.com/ducthangho/tra-luat'
$ShaVa      = '2f70869'        # HEAD mong cua ban va (nhanh fix_issue_541)
$ShaBoDo    = 'f11f071cb25b6774b06a2f9eef663eb7fb97a791bc368ec9a680f6a7070cb1b6'      # SHA-256 cua bo do Python nhung ben duoi

# Hai goi nay da DO tu container review 18-09-2026: tai duoc, va bam dung nhu ghi.
# Chung CHI duoc tai khi may ban THIEU cong cu do. May ban da co ca hai o luot truoc,
# nen duong nay nhieu kha nang khong chay lan nao.
$GitUrl     = 'https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/MinGit-2.47.1-64-bit.zip'
$GitSha     = '50b04b55425b5c465d076cdb184f63a0cd0f86f6ec8bb4d5860114a713d2c29a'
$PyUrl      = 'https://www.python.org/ftp/python/3.12.7/python-3.12.7-embed-amd64.zip'
$PySha      = '0d57bb6cb078b74d23dbfe91f77d6780d45bed328911609f1f7ee2ba1606bf44'

# ---------------------------------------------------------------- tien ich
function Dung($ly_do) {
    Write-Host ''
    Write-Host "KHONG DO DUOC: $ly_do" -ForegroundColor Red
    Write-Host 'Khong chay phep do. Khong ket luan gi.' -ForegroundColor Red
    exit 3
}
function Tieu($van) {
    Write-Host ''
    Write-Host ('-' * 70) -ForegroundColor DarkGray
    Write-Host $van -ForegroundColor Cyan
}
function G {
    # Chay git; doc rc TRUC TIEP, khong qua pipe.
    # Goi bang DUONG DAN DA RESOLVE chu khong bang ten tran: CreateProcessW chi tu
    # them ".exe", con Get-Command thi tra PATHEXT - hai luat khac nhau, va kho nay
    # da tra gia mot lan vi cho no la mot (bai hoc "launcher.py run khong tu giai shim").
    $out = & $script:GitExe @args 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host ($out | Out-String)
        Dung "git $($args -join ' ') => rc=$LASTEXITCODE"
    }
    return $out
}
function Bam($tep) { (Get-FileHash -Algorithm SHA256 -LiteralPath $tep).Hash.ToLower() }

function Tai-Va-Bung($ten, $url, $shaMong, $dich) {
    # Tai -> kiem bam -> bung. Bam lech thi DUNG HAN, khong bung.
    if (Test-Path -LiteralPath $dich) { Remove-Item -Recurse -Force -LiteralPath $dich }
    $zip = Join-Path $env:TEMP ("wp541-$ten-" + [guid]::NewGuid().ToString('N') + '.zip')
    Write-Host "  tai $ten ..."
    try { Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing }
    catch { Dung "khong tai duoc $ten tu $url : $($_.Exception.Message)" }
    $b = Bam $zip
    Write-Host "  bam $ten : $b"
    if ($b -ne $shaMong) { Remove-Item -Force -LiteralPath $zip; Dung "bam $ten LECH (mong $shaMong) - khong bung goi la" }
    New-Item -ItemType Directory -Force -Path $dich | Out-Null
    Expand-Archive -LiteralPath $zip -DestinationPath $dich -Force
    Remove-Item -Force -LiteralPath $zip
}

# ---------------------------------------------------------------- 0. thu muc
if (-not $Base) { $Base = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path } }
if (-not (Test-Path -LiteralPath $Base)) { Dung "khong thay thu muc lam viec: $Base" }
$Base = (Resolve-Path -LiteralPath $Base).Path
if (-not $Nguon) { $Nguon = Join-Path $Base 'tl546' }
if (-not $Kho)   { $Kho   = Join-Path $Base 'tl541-do' }
$CongCu = Join-Path $Base '_congcu-wp541'
$Log    = Join-Path $Base ('wp541-n7-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.log')

Write-Host ('=' * 70)
Write-Host 'WP541 g2 - do ban va tren Windows that (mot tep, tu lo moi thu)'
Write-Host ('=' * 70)
Write-Host "thu muc lam viec : $Base"

# ---------------------------------------------------------------- 1. quyen
$admin = $false
try {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $admin = (New-Object Security.Principal.WindowsPrincipal($id)).IsInRole(
                 [Security.Principal.WindowsBuiltInRole]::Administrator)
} catch {}
if ($admin) {
    Write-Host 'quyen Administrator : CO' -ForegroundColor Green
} else {
    Write-Host 'quyen Administrator : KHONG' -ForegroundColor Yellow
    Write-Host '  -> cac ca can tao symlink se DO vi thieu quyen, khong phai vi ban va.' -ForegroundColor Yellow
    Write-Host '  -> muon tach hai nguyen nhan ay: dong cua so nay, mo PowerShell bang' -ForegroundColor Yellow
    Write-Host '     "Run as administrator" roi chay lai dung lenh cu.' -ForegroundColor Yellow
    Write-Host '  Van chay tiep duoc; bo do se GHI LAI la no chay khong co quyen.' -ForegroundColor Yellow
}

# ---------------------------------------------------------------- 2. cong cu
Tieu 'Cong cu'
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if ($gitCmd) {
    $script:GitExe = $gitCmd.Source
} else {
    if ($BoQuaTaiCongCu) { Dung 'khong co git trong PATH (va -BoQuaTaiCongCu dang bat)' }
    Write-Host 'khong thay git -> tu tai MinGit'
    $gd = Join-Path $CongCu 'mingit'
    Tai-Va-Bung 'mingit' $GitUrl $GitSha $gd
    $script:GitExe = Join-Path $gd (Join-Path 'cmd' 'git.exe')
    if (-not (Test-Path -LiteralPath $script:GitExe)) { Dung "bung MinGit xong khong thay $script:GitExe" }
    $env:PATH = (Join-Path $gd 'cmd') + [IO.Path]::PathSeparator + $env:PATH
}
Write-Host "git : $script:GitExe"
try { $gv = & $script:GitExe --version 2>&1 } catch { Dung "khong khoi dong duoc git: $($_.Exception.Message)" }
if ($LASTEXITCODE -ne 0) { Dung "git co mat nhung khong chay duoc: $gv" }
Write-Host "      $($gv -join ' ')"

$pyCmd = $null
if ($Py) { $pyCmd = Get-Command $Py -ErrorAction SilentlyContinue }
foreach ($ten in @('py','python','python3')) {
    if ($pyCmd) { break }
    $pyCmd = Get-Command $ten -ErrorAction SilentlyContinue
}
if ($pyCmd) {
    # "CO MAT" khac "DUNG DUOC": py launcher khong co ban nao thi goi la gay.
    $ok = $true
    try { $thu = & $pyCmd.Source -c "import sys;print(sys.version.split()[0])" 2>&1 } catch { $ok = $false; $thu = $_.Exception.Message }
    if (-not $ok -or $LASTEXITCODE -ne 0) { Write-Host "  $($pyCmd.Name) co mat nhung khong chay duoc ($thu) -> bo qua"; $pyCmd = $null }
}
if (-not $pyCmd) {
    if ($BoQuaTaiCongCu) { Dung 'khong co python dung duoc (va -BoQuaTaiCongCu dang bat)' }
    Write-Host 'khong co python dung duoc -> tu tai ban nhung cua python.org'
    $pd = Join-Path $CongCu 'python'
    Tai-Va-Bung 'python' $PyUrl $PySha $pd
    $pe = Join-Path $pd 'python.exe'
    if (-not (Test-Path -LiteralPath $pe)) { Dung 'bung python xong khong thay python.exe' }
    $pyCmd = Get-Command $pe -ErrorAction SilentlyContinue
    if (-not $pyCmd) { Dung 'khong goi duoc python vua bung' }
}
Write-Host "py  : $($pyCmd.Source)"
Write-Host "      $((& $pyCmd.Source -c "import sys;print(sys.version.split()[0])") -join ' ')"

# ---------------------------------------------------------------- 3. bo do Python
Tieu 'Bo do Python (nhung trong chinh tep nay)'
$BoDo = Join-Path $Base 'wp541-do-g2-windows.py'
$B64 = @(
'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIiIiV1A1NDEgZzIgLSBQSEVQIERPIFRSRU4gV0lORE9XUyBUSEFUIGNobyBzcGVjIHIz'
'IChOMS1ONCArIE44LU4xMiArIE43ICsga2ljaCB0aHVvYykuCgpDaGF5OiAgcHkgd3A1NDEtZG8tZzItd2luZG93cy5weSAiPHRo'
'dS1tdWMta2hvPiIKCktIT05HIGdoaW0gU0hBLiBObyBkbyBCQVQgS1kgZGF1IG5hbyBkYW5nIG8gdHJlbiBuaGFuaCwgcm9pIFRV'
'IFBIQU4gTE9BSToKICBoZWFkID09IDJmNzA4NjlhICAtPiBkYXkgbGEgZzEsIENIVUEgY28gYmFuIHZhIGcyLiBWYW4gZG8sIG5o'
'dW5nIG5oYW4gbGEgTkVOIERPLgogIGhlYWQgbGEgaGF1IGR1ZSAgICAtPiB1bmcgdmllbiBnMi4KICBraGFjICAgICAgICAgICAg'
'ICAgLT4gS0hPTkcgRE8gRFVPQyAocmViYXNlPyBuaGFtIG5oYW5oPykgLT4gcmM9Mywga2hvbmcga2V0IGx1YW4uCgpCQSBUUkFO'
'RyBUSEFJIG8gbW9pIGNob3Q6IERBVCAvIFRSVU9UIC8gS0hPTkcgRE8gRFVPQy4gQ2FpIHRodSBiYSBLSE9ORyBkdW9jIGxhbmcg'
'bGUKdGhhbmggbW90IHRyb25nIGhhaSBjYWkga2lhIOKAlCBkbyBsYSBjYSBkb2N0cmluZSBgTm9uZSAhPSBGYWxzZWAgY3VhIGto'
'by4KCk1PSSBjaG90IGFtIGRldSBjbyBET0kgQ0hVTkcgRFVPTkcuIE1vdCBjaG90IGNoaSBkbyBjaGlldSAicGhhaSB0dSBjaG9p'
'IiB0aGkgbW90IGhhbQpgcmV0dXJuIE5vbmVgIHZvIGRpZXUga2llbiBjdW5nIHF1YSBkdW9jIG5vLgoKRG90IGJpZW4gY2hheSB0'
'cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaSBkdW5nIHRvaS4KIiIiCmltcG9ydCBjb250ZXh0bGliLCBpbXBvcnRs'
'aWIudXRpbCwgaW5zcGVjdCwgaW8sIGpzb24sIG9zLCByZSwgc2h1dGlsLCBzdWJwcm9jZXNzLCBzeXMsIHRlbXBmaWxlCmZyb20g'
'cGF0aGxpYiBpbXBvcnQgUGF0aCwgUHVyZVBvc2l4UGF0aCwgUHVyZVdpbmRvd3NQYXRoCgpvcy5lbnZpcm9uLnNldGRlZmF1bHQo'
'IlBZVEhPTlVURjgiLCAiMSIpCm9zLmVudmlyb24uc2V0ZGVmYXVsdCgiUFlUSE9OSU9FTkNPRElORyIsICJ1dGYtOCIpCmZvciBf'
'bCBpbiAoc3lzLnN0ZG91dCwgc3lzLnN0ZGVycik6CiAgICB0cnk6IF9sLnJlY29uZmlndXJlKGVuY29kaW5nPSJ1dGYtOCIsIGVy'
'cm9ycz0icmVwbGFjZSIpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBwYXNzCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAg'
'dHJ5OgogICAgICAgIGltcG9ydCBjdHlwZXMKICAgICAgICBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlNldENvbnNvbGVPdXRwdXRD'
'UCg2NTAwMSkKICAgICAgICBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlNldENvbnNvbGVDUCg2NTAwMSkKICAgIGV4Y2VwdCBFeGNl'
'cHRpb246IHBhc3MKCmRlZiBpbm4oKnApOgogICAgdmFuID0gIiAiLmpvaW4oc3RyKHgpIGZvciB4IGluIHApCiAgICB0cnk6IHBy'
'aW50KHZhbiwgZmx1c2g9VHJ1ZSkKICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgdHJ5OiBzeXMuc3Rkb3V0LmJ1ZmZlci53'
'cml0ZSh2YW4uZW5jb2RlKCJ1dGYtOCIsICJyZXBsYWNlIikgKyBiIlxuIik7IHN5cy5zdGRvdXQuZmx1c2goKQogICAgICAgIGV4'
'Y2VwdCBFeGNlcHRpb246IHByaW50KHZhbi5lbmNvZGUoImFzY2lpIiwgImJhY2tzbGFzaHJlcGxhY2UiKS5kZWNvZGUoImFzY2lp'
'IiksIGZsdXNoPVRydWUpCgpTSEFfRzEgICA9ICIyZjcwODY5YTA1Mzc4NDNlOWNhZTc4NjE4ZWU3YWU4YzI2MWQ5NzJkIgojIEtI'
'T05HIGdoaW0gYmFzZS4gU3BlYyByMyBONicga2hhaSBkbyBudW1zdGF0IHNvIGQ3MDU2MjMg4oCUIE5IVU5HIHNwZWMgQ1VORyBi'
'YW8gZXhlY3V0b3IKIyBgZ2l0IG1lcmdlIG9yaWdpbi9tYXN0ZXJgLiBTYXUgbWVyZ2UsIHBoZXAgZG8gc28gZDcwNTYyMyBOVU9U'
'IGNhIHBoYW4gbWFzdGVyIG1hbmcgdmFvOgojIGRvIHRoYXQgMTgtMDkgdHJlbiBiYW4gdmEgZzIgY3VhIGFneSBjaG8gNSB0ZXAg'
'LyArODEyLCB0cm9uZyBraGkgdmllYyBjdWEgYWd5IGxhIDIgdGVwIC8gKzM1My4KIyBNb3QgY2hvdCBuaHUgdGhlIHNlIGJhbyAi'
'dnVvdCB0cmFuIiBjaG8gbW90IGJhbiB2YSBLSE9ORyB2dW90LiBCYXNlIGR1bmcgbGEgTUVSR0UtQkFTRS4KU0hBX0JBU0VfU1BF'
'QyA9ICJkNzA1NjIzMTYyYjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpUUkFOX1RFUCwgVFJBTl9ET05HID0gMiwgNDAw'
'ICAgICAgICAgICMgTjcnIGN1YSBzcGVjIHIzCk1BVV9XSU4gID0gJ2lmIG5lbl90aHVjID09ICJ3aW5kb3dzIjonCkNBMTUgID0g'
'InQxMjkgdDEzMCB0MTMxIHQxMzIgdDEzMyB0MTM2IHQxMzggdDEzOSB0MTQ0IHQxNDUgdDE0NiB0MTQ3IHQxNDkgdDE1MCB0MTUx'
'Ii5zcGxpdCgpCkNBTU9JID0gInQxNjUgdDE2NiB0MTY3IHQxNjgiLnNwbGl0KCkKCkRBVCwgVFJVT1QsIEtERCA9ICJEQVQiLCAi'
'VFJVT1QiLCAiS0hPTkcgRE8gRFVPQyIKc28sIGNob3QgPSB7fSwgW10KZGVmIGdoaShrLCB2KTogc29ba10gPSB2OyByZXR1cm4g'
'dgpkZWYga2V0KHRlbiwgdHJhbmdfdGhhaSwgY2hpX3RpZXQ9IiIpOgogICAgY2hvdC5hcHBlbmQoKHRlbiwgdHJhbmdfdGhhaSwg'
'Y2hpX3RpZXQpKQogICAgaW5uKGYiICBbe3RyYW5nX3RoYWk6MTR9XSB7dGVufSIgKyAoZiIgICB7Y2hpX3RpZXR9IiBpZiBjaGlf'
'dGlldCBlbHNlICIiKSkKICAgIHJldHVybiB0cmFuZ190aGFpCgojIC0tLS0tLS0tLS0tLS0tLS0gZG9jIGxvZyBjdWEgYm8gdGVz'
'dCAoYmFuIDMsIGRhIGRvIHRyZW4gbG9nIFRIQVQpIC0tLS0tLS0tLS0tLS0tLS0KUlhfRE9fQ0hPICA9IHJlLmNvbXBpbGUociIo'
'P20pXiEhISBkbyAoXFMrKSAoLiopJCIpClJYX0RPX0NVT0kgPSByZS5jb21waWxlKHIiKD9tKV4gezJ9KFxTezEsNH0pIHsyfShc'
'UyspOiAoLiopJCIpClJYX0JPX1FVQSAgPSByZS5jb21waWxlKHIiKD9tKV4gezJ9XFN7MSw2fSBRVUEgKFxTKyk6ICguKikkIikK'
'UlhfVE9ORyAgICA9IHJlLmNvbXBpbGUociJsZWFzZV9wdWJsaXNoOiAoXGQrKS8oXGQrKVxiW15cbl0qPz0oXGQrKSxbXlxuXSo/'
'PShcZCspIikKCmRlZiBzb19jYSh0KToKICAgIG0gPSByZS5tYXRjaChyInQoXGQrKSIsIHQpOyByZXR1cm4gKGludChtLmdyb3Vw'
'KDEpKSBpZiBtIGVsc2UgMTAqKjYsIHQpCgpkZWYgZG9jX2RvKG91dCk6CiAgICB0YWlfY2hvID0ge3Q6IGwuc3RyaXAoKSBmb3Ig'
'dCwgbCBpbiBSWF9ET19DSE8uZmluZGFsbChvdXQpfQogICAgYm8gPSB7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChv'
'dXQpfQogICAgY3VvaSA9IHt0OiBsLnN0cmlwKCkgZm9yIF8sIHQsIGwgaW4gUlhfRE9fQ1VPSS5maW5kYWxsKG91dCkgaWYgdCBu'
'b3QgaW4gYm99CiAgICBob3AgPSBkaWN0KGN1b2kpOyBob3AudXBkYXRlKHRhaV9jaG8pCiAgICBnYywgdGluID0gW10sIFRydWUK'
'ICAgIGlmIHNldCh0YWlfY2hvKSAhPSBzZXQoY3VvaSk6CiAgICAgICAgZ2MuYXBwZW5kKGYiaGFpIG5ndW9uIExFQ0g6IGNoaS10'
'YWktY2hvPXtzb3J0ZWQoc2V0KHRhaV9jaG8pLXNldChjdW9pKSl9IGNoaS1jdW9pPXtzb3J0ZWQoc2V0KGN1b2kpLXNldCh0YWlf'
'Y2hvKSl9IikKICAgICAgICB0aW4gPSBGYWxzZQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dCkKICAgIGlmIG5vdCBtOgogICAg'
'ICAgIGdjLmFwcGVuZCgiS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCIpOyB0aW4gPSBGYWxzZQogICAgZWxzZToKICAgICAg'
'ICBkYXQsIHRyZW4gPSBpbnQobS5ncm91cCgxKSksIGludChtLmdyb3VwKDIpKQogICAgICAgIGdjLmFwcGVuZChmInNvIGhvYzog'
'e3RyZW59LXtkYXR9PXt0cmVuLWRhdH0gZG87IGRvYyBkdW9jIHtsZW4oaG9wKX0iKQogICAgICAgIGlmIHRyZW4gLSBkYXQgIT0g'
'bGVuKGhvcCk6CiAgICAgICAgICAgIGdjLmFwcGVuZChmIkxFQ0ggU08gSE9DOiB0aGlldSB7dHJlbi1kYXQtbGVuKGhvcCl9IGNh'
'Iik7IHRpbiA9IEZhbHNlCiAgICByZXR1cm4gaG9wLCBnYywgdGluCgpfTUFVID0gKCIhISEgZG8gdDAyYl90ZW5fS0hPTkdfQ09f'
'VEhBTV9RVVlFTiBhXG4iCiAgICAgICAgIiEhISBkbyB0MTUwX3ggV2luRXJyb3IgMTMxNCByZXF1aXJlZCBwcml2aWxlZ2VcbiIK'
'ICAgICAgICAiICBC4buOIFFVQSB0MTMxX3k6IG5lbiBmaXh0dXJlXG4iCiAgICAgICAgIiAgxJDhu44gIHQwMmJfdGVuX0tIT05H'
'X0NPX1RIQU1fUVVZRU46IGFcbiIKICAgICAgICAiICDEkOG7jiAgdDE1MF94OiBXaW5FcnJvciAxMzE0IHJlcXVpcmVkIHByaXZp'
'bGVnZVxuIgogICAgICAgICJsZWFzZV9wdWJsaXNoOiAxLzMgxJHhuqF0OyDEkcOjIGNo4bqheT0zLCBi4buPIHF1YT0xXG4iKQoK'
'ZGVmIGNoYXkoYXJndiwgY3dkLCBwaHV0PTYwKToKICAgIG10ID0gZGljdChvcy5lbnZpcm9uLCBQWVRIT05VVEY4PSIxIiwgUFlU'
'SE9OSU9FTkNPRElORz0idXRmLTgiLAogICAgICAgICAgICAgIFBZVEhPTkRPTlRXUklURUJZVEVDT0RFPSIxIiwgUFlUSE9OVU5C'
'VUZGRVJFRD0iMSIpCiAgICBwID0gc3VicHJvY2Vzcy5ydW4oW3N5cy5leGVjdXRhYmxlXSArIGFyZ3YsIGN3ZD1zdHIoY3dkKSwg'
'Y2FwdHVyZV9vdXRwdXQ9VHJ1ZSwKICAgICAgICAgICAgICAgICAgICAgICB0ZXh0PVRydWUsIGVuY29kaW5nPSJ1dGYtOCIsIGVy'
'cm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCwgZW52PW10KQogICAgcmV0dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rkb3V0'
'IG9yICIiKSArIChwLnN0ZGVyciBvciAiIikKCmRlZiBtYXVfY2Eob3V0LCB0KToKICAgIG0gPSByZS5zZWFyY2gociIoP20pXjw8'
'PCByYSAoIiArIHQgKyByIlthLXpdP19cUyopIFswLTkuXStzIChcdyspXHMqJCIsIG91dCkKICAgIHJldHVybiBtLmdyb3VwKDIp'
'IGlmIG0gZWxzZSBOb25lCgpkZWYgZ2l0KGdvYywgKmEsIHBodXQ9NSk6CiAgICBwID0gc3VicHJvY2Vzcy5ydW4oWyJnaXQiLCAi'
'LUMiLCBzdHIoZ29jKSwgKmFdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsCiAgICAgICAgICAgICAgICAgICAgICAg'
'ZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD1waHV0KjYwKQogICAgcmV0dXJuIHAucmV0dXJuY29k'
'ZSwgKHAuc3Rkb3V0IG9yICIiKS5zdHJpcCgpLCAocC5zdGRlcnIgb3IgIiIpLnN0cmlwKCkKCgojID09PT09PT09PT09PT09PT09'
'IE5BTSBQUk9CRSwgdmlldCB0aGFuaCBIQU0gVEhVQU4gZGUgVFUgS0lFTSBkdW9jID09PT09PT09PT09PT09PT09CiMgTW9pIGhh'
'bSB0cmEgKHRyYW5nX3RoYWksIGNoaV90aWV0LCBkdV9saWV1KS4gS0hPTkcgaW4sIEtIT05HIHRob2F0IOKAlCBuaG8gdmF5IGNo'
'dW5nCiMgY2hheSBkdW9jIHRyZW4gbmVuIEJBVCBLWSwgdmEgYC0tdHUta2llbS1wcm9iZWAgZ29pIHRoYW5nIGNodW5nIGRlIGtp'
'ZW0gY2hpbmggYm8gZG8uCgpkZWYgX3Nhbih0KToKICAgIGQgPSBQYXRoKHQpLyJkIjsgZC5ta2RpcigpOyBjdyA9IFBhdGgodCkv'
'ImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICByZXR1cm4gZCwgY3csIHBmCgpkZWYg'
'ZG9fbjgoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiQnVvYyAxIChDT05HX0NVX0dJVCkgY2hpIGR1b2MgbmhhbiBnaXQuZXhlLiBE'
'b2kgY2h1bmcgZHVvbmc6IGdpdC5leGUgVkFOIHBoYWkgbmhhbi4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVtcGZpbGUuVGVt'
'cG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgZm9yIHRlbiBpbiAoImdp'
'dC5leGUiLCAiZ2l0LmJhdCIsICJnaXQuY21kIiwgImdpdC5weSIsICJraG9uZy1waGFpLWdpdC50eHQiKToKICAgICAgICAgICAg'
'ZiA9IGQvdGVuOyBmLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBfID0gZ29pKGNvbmdf'
'Y3VfZ2l0PXN0cihmKSwgcGF0aD0iIiwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAga3Fb'
'ZiJDT05HX0NVX0dJVD17dGVufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiVFUgQ0hPSSIKICAgIGxvdCA9IFtrIGZvciBrLCB2IGlu'
'IGtxLml0ZW1zKCkgaWYgdiA9PSAiTkhBTiIgYW5kIG5vdCBrLmVuZHN3aXRoKCJnaXQuZXhlIildCiAgICBpZiBrcS5nZXQoIkNP'
'TkdfQ1VfR0lUPWdpdC5leGUiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBn'
'aXQuZXhlIGhvcCBsZSBtYSBiaSB0dSBjaG9pIiwga3EKICAgIHJldHVybiAoREFUIGlmIG5vdCBsb3QgZWxzZSBUUlVPVCksICgi'
'IiBpZiBub3QgbG90IGVsc2UgZiJjb24gbmhhbjoge2xvdH0iKSwga3EKCmRlZiBkb19uOShnb2ksIHNpZywgdGVwdCk6CiAgICAi'
'IiJNdWMgUEFUSCBib2MgbmhheSBrZXAgcGhhaSBOSEFOOyBtdWMgcm9uZyAvIHRvYW4ga2hvYW5nIHRyYW5nIHBoYWkgYm8gcXVh'
'LCBraG9uZyBuZW0uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAg'
'ICAgICAgZCA9IFBhdGgodCkvImNvIGdpdCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9'
'IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1'
'dGYtOCIpCiAgICAgICAgZm9yIG5oYW4sIG11YyBpbiAoKCJraG9uZyBuaGF5Iiwgc3RyKGQpKSwgKCJjbyBuaGF5IGtlcCIsIGYn'
'IntkfSInKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAoInJvbmciLCAiIiksICgiY2hpIGtob2FuZyB0cmFuZyIsICIgICAi'
'KSk6CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIHIsIF8gPSBnb2kocGF0aD1tdWMsIHByb2dyYW1fZmlsZXM9c3Ry'
'KHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59Il0gPSAiTkhBTiIgaWYgciBlbHNlICJO'
'b25lIgogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59Il0g'
'PSBmIk5FTSB7dHlwZShlKS5fX25hbWVfX30iCiAgICBpZiBrcS5nZXQoIlBBVEgga2hvbmcgbmhheSIpICE9ICJOSEFOIjoKICAg'
'ICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG11YyBQQVRIIHRodW9uZyBtYSBraG9uZyB0aW0gcmEgZ2l0'
'LmV4ZSIsIGtxCiAgICBvayA9IChrcS5nZXQoIlBBVEggY28gbmhheSBrZXAiKSA9PSAiTkhBTiIKICAgICAgICAgIGFuZCBrcS5n'
'ZXQoIlBBVEggcm9uZyIpID09ICJOb25lIiBhbmQga3EuZ2V0KCJQQVRIIGNoaSBraG9hbmcgdHJhbmciKSA9PSAiTm9uZSIpCiAg'
'ICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgpkZWYgZG9fbjEw'
'KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIk1vdCBkYXUgJzsnIHRyb25nIFRFTiB0aHUgbXVjIGtob25nIGR1b2MgbGFtIG1hdCBt'
'dWMgZ2l0LmV4ZSBob3AgbGUgbyBtdWMga2lhLiIiIgogICAgY29fc2VwID0gYW55KCgiY2FjaCIgaW4gaykgb3IgKCJzZXAiIGlu'
'IGsubG93ZXIoKSkgZm9yIGsgaW4gc2lnLnBhcmFtZXRlcnMpCiAgICBpZiBvcy5wYXRoc2VwID09ICI7IiBhbmQgbm90IGNvX3Nl'
'cDoKICAgICAgICByZXR1cm4gKEtERCwgInRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyB2YSBoYW0ga2hvbmcgbmhh'
'biB0aGFtIHNvIGRhdSBwaGFuIGNhY2ggIgogICAgICAgICAgICAgICAgICAgICAiLT4ga2hvbmcgdGFjaCBkdW9jIGhhaSBnaWEg'
'dGh1eWV0IiwgeyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgImNvIHRoYW0gc28gc2VwIjogY29fc2VwfSkKICAgIHdpdGggdGVt'
'cGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkK'
'ICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9'
'InV0Zi04IikKICAgICAgICByLCBfID0gZ29pKHBhdGg9c3RyKGxhKSArIG9zLnBhdGhzZXAgKyBzdHIoZCksIHByb2dyYW1fZmls'
'ZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgcjAsIF8gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3Ry'
'KHBmKSwgY3dkPXN0cihjdykpICAgICAjIGRvaSBjaHVuZyBkdW9uZwogICAga3EgPSB7ImNvIG11YyBjaHVhICc7JyI6ICJOSEFO'
'IiBpZiByIGVsc2UgIk5vbmUiLCAiZG9pIGNodW5nIChraG9uZyBjbyAnOycpIjogIk5IQU4iIGlmIHIwIGVsc2UgIk5vbmUifQog'
'ICAgaWYgbm90IHIwOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZyIsIGtxCiAgICByZXR1cm4gKERB'
'VCBpZiByIGVsc2UgVFJVT1QpLCAoIiIgaWYgciBlbHNlICJtdWMgZ2l0LmV4ZSBob3AgbGUgYmkgTUFUIiksIGtxCgpkZWYgZG9f'
'bjExKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIlRydXllbiBjaGFuX2RvYW4gPT4gdGh1IGR1b2MgdGhvbmcgYmFvIFZBIHN0ZGVy'
'ciBJTS4gS2hvbmcgdHJ1eWVuID0+IHN0ZGVyciBWQU4gY28uIiIiCiAgICBpZiAiY2hhbl9kb2FuIiBub3QgaW4gc2lnLnBhcmFt'
'ZXRlcnM6CiAgICAgICAgcmV0dXJuIEtERCwgIl9naXRfd2luZG93cyBraG9uZyBuaGFuIHRoYW0gc28gY2hhbl9kb2FuIiwgeyJ0'
'aGFtIHNvIjogbGlzdChzaWcucGFyYW1ldGVycyl9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6'
'CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5n'
'PSJ1dGYtOCIpCiAgICAgICAgY2QgPSBbXQogICAgICAgIF8sIGVfY28gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9'
'c3RyKHBmKSwgY3dkPXN0cihjdyksIGNoYW5fZG9hbj1jZCkKICAgICAgICBfLCBlX2toID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9n'
'cmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAga3EgPSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAobXVjKSI6IGxlbihj'
'ZCksCiAgICAgICAgICAic3RkZXJyIGtoaSBDTyBjaGFuX2RvYW4gKGJ5dGUpIjogbGVuKGVfY28uZW5jb2RlKCkpLAogICAgICAg'
'ICAgInN0ZGVyciBraGkgS0hPTkcgdHJ1eWVuIChieXRlKSI6IGxlbihlX2toLmVuY29kZSgpKX0KICAgIGlmIGxlbihjZCkgPT0g'
'MCBhbmQgbGVuKGVfa2guZW5jb2RlKCkpID09IDA6CiAgICAgICAgcmV0dXJuIEtERCwgIm5oYW5oICVQcm9ncmFtRmlsZXMlIGto'
'b25nIHBoYW4gZ2lhaSBLSE9ORyBiYXkgcmEgY2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRvIGR1b2MiLCBrcQogICAgb2sgPSBsZW4o'
'Y2QpID4gMCBhbmQgbGVuKGVfY28uZW5jb2RlKCkpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA+IDAKICAgIHJldHVybiAo'
'REFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCmRlZiBkb19uMTIoZ29pLCBzaWcs'
'IHRlcHQpOgogICAgIiIiSGFuZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9uZyBmaXh0dXJlIHBoYWkgdHV5ZXQgZG9pIHRyZW4gQ0Eg'
'SEFJIG5lbi4iIiIKICAgIG5kID0gdGVwdC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIikKICAg'
'IGhhbmcgPSBzb3J0ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRfcGF0aFxzKj1ccyoiKFteIl0rKSInLCBuZCkpKQogICAgeGF1ID0g'
'W2ggZm9yIGggaW4gaGFuZyBpZiBub3QgKFB1cmVQb3NpeFBhdGgoaCkuaXNfYWJzb2x1dGUoKSBhbmQgUHVyZVdpbmRvd3NQYXRo'
'KGgpLmlzX2Fic29sdXRlKCkpXQogICAga3EgPSB7ImhhbmcgZ2l0X3BhdGggdGltIHRoYXkiOiBoYW5nLCAiY2hpIHR1eWV0IGRv'
'aSBNT1QgbmVuIjogeGF1fQogICAgaWYgbm90IGhhbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImtob25nIHRpbSB0aGF5IGhhbmcg'
'Z2l0X3BhdGggbmFvIHRyb25nIGZpeHR1cmUgLT4gbWF1IGRvYyBjbyB0aGUgZGEgZG9pIiwga3EKICAgIHJldHVybiAoREFUIGlm'
'IG5vdCB4YXUgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgeGF1IGVsc2UgZiJjaGktbW90LW5lbjoge3hhdX0iKSwga3EKClBST0JF'
'ID0gWygiTjggYnVvYyAxIGNoaSBuaGFuIGdpdC5leGUiLCBkb19uOCksCiAgICAgICAgICgiTjkgYm9jIG5oYXkga2VwIG8gbXVj'
'IFBBVEgiLCBkb19uOSksCiAgICAgICAgICgiTjEwIGRhdSAnOycgdHJvbmcgdGVuIHRodSBtdWMiLCBkb19uMTApLAogICAgICAg'
'ICAoIk4xMSBjaGFuIGRvYW4gZG9pIGtlbmgiLCBkb19uMTEpLAogICAgICAgICAoIk4xMiBoYW5nIHNlbnRpbmVsIHR1eWV0IGRv'
'aSBDQSBIQUkgbmVuIiwgZG9fbjEyKV0KCiMgLS0tIGNoZSBkbyBUVSBLSUVNOiBjaGF5IG5hbSBwcm9iZSB0cmVuIG1vdCBjYXkg'
'YmF0IGt5LCBuZW4gYmF0IGt5IC0tLQppZiAiLS10dS1raWVtLXByb2JlIiBpbiBzeXMuYXJndjoKICAgIF9nID0gUGF0aChzeXMu'
'YXJndltzeXMuYXJndi5pbmRleCgiLS10dS1raWVtLXByb2JlIikgKyAxXSkucmVzb2x2ZSgpCiAgICBfc3AgPSBpbXBvcnRsaWIu'
'dXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfdGsiLCBzdHIoX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAg'
'IF9scCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbHApCiAg'
'ICBfc2lnID0gaW5zcGVjdC5zaWduYXR1cmUoX2xwLl9naXRfd2luZG93cykKICAgIGRlZiBfZ29pKCoqa3cpOgogICAgICAgIGUg'
'PSBpby5TdHJpbmdJTygpCiAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICAgICAgcmV0'
'dXJuIF9scC5fZ2l0X3dpbmRvd3MoKiprdyksIGUuZ2V0dmFsdWUoKQogICAgcHJpbnQoZiJUVSBLSUVNIFBST0JFIHRyZW4ge19n'
'fSAgKG5lbiB7c3lzLnBsYXRmb3JtfSkiKQogICAgZm9yIF90ZW4sIF9mIGluIFBST0JFOgogICAgICAgIF90dCwgX2N0LCBfZGwg'
'PSBfZihfZ29pLCBfc2lnLCBfZy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBwcmludChmIiAgW3tfdHQ6'
'MTR9XSB7X3Rlbn0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgICAgICBmb3IgX2ssIF92IGluIChfZGwgb3Ig'
'e30pLml0ZW1zKCk6IHByaW50KGYiICAgICAgICB7X2s6MzR9OiB7X3Z9IikKICAgIHN5cy5leGl0KDApCgppbm4oIj0iICogNzgp'
'OyBpbm4oIldQNTQxIGcyIC0gcGhlcCBkbyB0cmVuIFdpbmRvd3MgdGhhdCAoc3BlYyByMzogTjEtTjQsIE44LU4xMiwgTjcsIGtp'
'Y2ggdGh1b2MpIik7IGlubigiPSIgKiA3OCkKCiMgLS0tLS0tLS0tLS0tLS0tLSB0dSBraWVtIGJvIGRvYyAtLS0tLS0tLS0tLS0t'
'LS0tCl9kLCBfZywgX3QgPSBkb2NfZG8oX01BVSkKX29rID0gKGxlbihfZCkgPT0gMiBhbmQgYW55KHguc3RhcnRzd2l0aCgidDAy'
'YiIpIGZvciB4IGluIF9kKQogICAgICAgYW5kIG5vdCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMxIikgZm9yIHggaW4gX2QpIGFuZCBf'
'dCkKaW5uKCJUdSBraWVtIGJvIGRvYyBsb2c6IiwgREFUIGlmIF9vayBlbHNlIFRSVU9UKQppZiBub3QgX29rOgogICAgaW5uKCIi'
'KTsgaW5uKCJLSE9ORyBETyBEVU9DOiBibyBkb2MgbG9nIGN1YSBjaGluaCBzY3JpcHQgbmF5IHNhaSAtPiBraG9uZyBkbyBnaSBj'
'YS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4gZG8gLS0tLS0tLS0tLS0tLS0tLQpnb2MgPSBQYXRo'
'KHN5cy5hcmd2WzFdKS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQYXRoLmN3ZCgpCnRlcCwgdGVwdCA9IGdv'
'YyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiCmlubigi'
'Iik7IGlubigiLSIgKiA3OCk7IGlubigiMC4gTkVOIERPIikKaW5uKCIgIHN5cy5wbGF0Zm9ybSA6Iiwgc3lzLnBsYXRmb3JtLCAi'
'fCBweXRob24iLCBzeXMudmVyc2lvbi5zcGxpdCgpWzBdKQppbm4oIiAgb3MucGF0aHNlcCAgIDoiLCByZXByKG9zLnBhdGhzZXAp'
'LCAifCBQQVRIRVhUOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlBBVEhFWFQiKSlbOjYwXSkKaW5uKCIgIFByb2dyYW1GaWxlcyA6'
'IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUHJvZ3JhbUZpbGVzIikpLCAifCBTeXN0ZW1Sb290OiIsIHJlcHIob3MuZW52aXJvbi5n'
'ZXQoIlN5c3RlbVJvb3QiKSkpCmlubigiICBDT05HX0NVX0dJVCAgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIkNPTkdfQ1VfR0lU'
'IikpKQppbm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5vbmUKaWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6'
'CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4gPSBib29sKGN0eXBlcy53aW5kbGwuc2hlbGwzMi5Jc1VzZXJB'
'bkFkbWluKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXllbiA9IE5vbmUKZ2hpKCJxdXllbl9hZG1pbiIsIHF1eWVuKQpzeW1s'
'aW5rX2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBk'
'ID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHRyeTogb3Muc3lt'
'bGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJsayIpKTsgc3ltbGlua19kdW9jID0gVHJ1ZQogICAgICAgIGV4Y2VwdCBPU0Vycm9y'
'IGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZhbHNlOyBnaGkoInN5bWxpbmtfbG9pIiwgZiJ7dHlwZShlKS5fX25hbWVfX306IHtlfSIp'
'CmV4Y2VwdCBFeGNlcHRpb24gYXMgZTogZ2hpKCJzeW1saW5rX2xvaSIsIHN0cihlKSkKZ2hpKCJzeW1saW5rX2R1b2MiLCBzeW1s'
'aW5rX2R1b2MpCmlubigiICBBZG1pbmlzdHJhdG9yOiIsIHF1eWVuLCAifCB0YW8gc3ltbGluayBkdW9jOiIsIHN5bWxpbmtfZHVv'
'YykKCmxvaSA9IFtdCmlmIHN5cy5wbGF0Zm9ybSAhPSAid2luMzIiOiBsb2kuYXBwZW5kKGYiS0hPTkcgcGhhaSBXaW5kb3dzIChz'
'eXMucGxhdGZvcm09e3N5cy5wbGF0Zm9ybSFyfSkiKQppZiBub3QgdGVwLmlzX2ZpbGUoKTogIGxvaS5hcHBlbmQoZiJraG9uZyB0'
'aGF5IHt0ZXB9IikKaWYgbm90IHRlcHQuaXNfZmlsZSgpOiBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwdH0iKQppZiBub3Qg'
'c2h1dGlsLndoaWNoKCJnaXQiKTogbG9pLmFwcGVuZCgia2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCIpCgpyYywgaGVhZCwgXyA9'
'IGdpdChnb2MsICJyZXYtcGFyc2UiLCAiSEVBRCIpCmlmIHJjOiBsb2kuYXBwZW5kKCJraG9uZyBkb2MgZHVvYyBIRUFEIikKZ2hp'
'KCJoZWFkIiwgaGVhZCkKcmNfYSwgXywgXyA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIi0taXMtYW5jZXN0b3IiLCBTSEFfRzEs'
'IGhlYWQgb3IgIkhFQUQiKQpsYV9oYXVfZHVlID0gKHJjX2EgPT0gMCkKaWYgaGVhZCA9PSBTSEFfRzE6CiAgICB0aGVfaGUgPSAi'
'ZzEiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IERBWSBMQSBnMS4gQ0hVQSBjbyBiYW4gdmEgZzI7IGtldCBxdWEgZHVv'
'aSBsYSBORU4gRE8uIikKZWxpZiBsYV9oYXVfZHVlOgogICAgdGhlX2hlID0gImcyIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhd'
'fSAtPiBoYXUgZHVlIGN1YSBnMSAoe1NIQV9HMVs6OF19KTogdW5nIHZpZW4gZzIuIikKZWxzZToKICAgIHRoZV9oZSA9ICI/Ijsg'
'bG9pLmFwcGVuZChmIkhFQUQ9e2hlYWRbOjhdfSBLSE9ORyBwaGFpIGcxIHZhIEtIT05HIHBoYWkgaGF1IGR1ZSBjdWEge1NIQV9H'
'MVs6OF19IOKAlCByZWJhc2U/IG5oYW0gbmhhbmg/IikKZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCgppZiBsb2k6CiAgICBpbm4oIiIp'
'OyBpbm4oIktIT05HIERPIERVT0M6IG5lbiBkbyBzYWksIEtIT05HIGluIGtldCBsdWFuIG5hby4iKQogICAgZm9yIHggaW4gbG9p'
'OiBpbm4oIiAgLSIsIHgpCiAgICBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDEuIGtpY2ggdGh1b2MgKE43JyBjdWEg'
'c3BlYyByMykgLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjEuIEtJQ0ggVEhVT0Mg4oCUIHRy'
'YW4gc3BlYyByMzogPD0gMiB0ZXAgdmEgPD0gNDAwIGRvbmcgdGhlbSIpCnJjX21iLCBtYiwgZXJfbWIgPSBnaXQoZ29jLCAibWVy'
'Z2UtYmFzZSIsICJvcmlnaW4vbWFzdGVyIiwgaGVhZCkKaWYgcmNfbWIgb3Igbm90IG1iOgogICAga2V0KCJONycga2ljaCB0aHVv'
'YyIsIEtERCwgZiJraG9uZyB0aW5oIGR1b2MgbWVyZ2UtYmFzZSB2b2kgb3JpZ2luL21hc3Rlcjoge2VyX21iWzo3MF19IikKICAg'
'IG5zLCByYyA9ICIiLCAxCmVsc2U6CiAgICBnaGkoIm1lcmdlX2Jhc2UiLCBtYikKICAgIGlubihmIiAgbWVyZ2UtYmFzZShvcmln'
'aW4vbWFzdGVyLCBIRUFEKSA9IHttYls6MTJdfSIpCiAgICBpZiBtYiAhPSBTSEFfQkFTRV9TUEVDOgogICAgICAgIGlubihmIiAg'
'TFVVIFk6IGtoYWMgYmFzZSBtYSBzcGVjIHIzIGtoYWkgKHtTSEFfQkFTRV9TUEVDWzoxMl19KSDigJQgdmkgbmhhbmggZGEgbWVy'
'Z2UgbWFzdGVyLiIpCiAgICAgICAgaW5uKGYiICAgICAgICAgRG8gc28gYmFzZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcg'
'dmFvLiBEdW5nIG1lcmdlLWJhc2UgbW9pIGxhIHZpZWMgY3VhIGV4ZWN1dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdp'
'dChnb2MsICJkaWZmIiwgIi0tbnVtc3RhdCIsIFNIQV9CQVNFX1NQRUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAgICAg'
'ICAgICAgIGggPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBuc194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICAgICAg'
'ICAgIGEgPSBzdW0oaW50KHhbMF0pIGZvciB4IGluIGggaWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdoaSgibnVtc3Rh'
'dF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVwIjogbGVuKGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBpbm4oZiIgICAgICAgICAo'
'ZG9pIGNoaWV1OiBzbyBiYXNlIHNwZWMgPSB7bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkgS0hPTkcgZHVuZyBkZSBj'
'aGFtKSIpCiAgICByYywgbnMsIGVyID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgbWIsIGhlYWQpCmlmIHJjOgogICAg'
'cGFzcwplbHNlOgogICAgaGFuZyA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCld'
'CiAgICB0aGVtID0gc3VtKGludChoWzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdpdCgpKQogICAgeG9hICA9IHN1bShp'
'bnQoaFsxXSkgZm9yIGggaW4gaGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgic29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hp'
'KCJkb25nX3RoZW0iLCB0aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZvciBoIGluIGhhbmc6IGlubihmIiAgICB7aFsy'
'XTozNH0gK3toWzBdOjw1fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05HOiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17'
'eG9hfSAgICh0cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcgdGhlbSkiKQogICAga2V0KCJONycga2ljaCB0'
'aHVvYyIsIERBVCBpZiAobGVuKGhhbmcpIDw9IFRSQU5fVEVQIGFuZCB0aGVtIDw9IFRSQU5fRE9ORykgZWxzZSBUUlVPVCwKICAg'
'ICAgICBmIntsZW4oaGFuZyl9IHRlcCAvICt7dGhlbX0iKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDIuIGJvIHRlc3QgZGF5IGR1IC0t'
'LS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIyLiBCTyBURVNUIERBWSBEVSAoMTAtNDAgcGh1dCki'
'KQpyY19uLCBvdXRfbiA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIGdvYykKZ2hpKCJyY19zdWl0ZSIsIHJj'
'X24pCm0gPSBSWF9UT05HLnNlYXJjaChvdXRfbikKaW5uKCIgIHJjID0iLCByY19uLCAifCIsIG0uZ3JvdXAoMCkgaWYgbSBlbHNl'
'ICIoS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCkiKQppZiBtOgogICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBn'
'aGkoInRyZW4iLCBpbnQobS5ncm91cCgyKSkpOyBnaGkoImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKZG9faGV0LCBnYywg'
'dGluID0gZG9jX2RvKG91dF9uKQpnaGkoInNvX2NhX2RvIiwgbGVuKGRvX2hldCkpOyBnaGkoImxpZXRfa2VfZGF5X2R1IiwgdGlu'
'KQpmb3IgZyBpbiBnYzogaW5uKCIgICAqIiwgZykKaW5uKCIiKTsgaW5uKGYiICA9PT0ge2xlbihkb19oZXQpfSBDQSBETyA9PT0i'
'KQpmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgaW5uKGYiICAge3Quc3BsaXQoJ18nKVswXTo3fSB7dH0i'
'KTsgaW5uKGYiICAgICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCmdoaSgiZG9fbHlfZG8iLCB7dDogZG9faGV0W3RdWzozMDBd'
'IGZvciB0IGluIGRvX2hldH0pCmJxID0gc29ydGVkKHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91dF9uKX0sIGtl'
'eT1zb19jYSk7IGdoaSgiY2FfYm9fcXVhIiwgYnEpCmlubigiIik7IGlubihmIiAgQk8gUVVBICh7bGVuKGJxKX0pOiB7W3guc3Bs'
'aXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCmlubigiIik7IGlubigiICBOMS1ONCAodDE2NS10MTY4KSwgdGlldSBjaGkgbmdo'
'aWVtIHRodSBjdWEgcjIsIG5heSBsYSBjaGkgYmFvIGhvaSBxdXk6IikKYjQgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBp'
'biBDQU1PSX07IGdoaSgiY2FfbW9pIiwgYjQpCmZvciB0IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCmtldCgi'
'TjEtTjQgKHQxNjUtdDE2OCkiLCBEQVQgaWYgYWxsKHYgPT0gIlFVQSIgZm9yIHYgaW4gYjQudmFsdWVzKCkpCiAgICBlbHNlIChL'
'REQgaWYgYW55KHYgaXMgTm9uZSBmb3IgdiBpbiBiNC52YWx1ZXMoKSkgZWxzZSBUUlVPVCksIHN0cihiNCkpCgppbm4oIiIpOyBp'
'bm4oIiAgMTUgY2EgdHVuZyBkbyB0cmVuIENJOiIpCmIxNSA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBMTV9OyBn'
'aGkoImNhMTUiLCBiMTUpCmlubigiICAgICIgKyAiICAiLmpvaW4oZiJ7dH06e2IxNVt0XX0iIGZvciB0IGluIENBMTUpKQoKIyB0'
'MTM2IOKAlCBOMTIgZG8gR0lBTiBUSUVQIHF1YSBrZXQgcXVhIGNhCnQxMzZfdGVuID0gbmV4dCgodCBmb3IgdCBpbiBkb19oZXQg'
'aWYgdC5zdGFydHN3aXRoKCJ0MTM2IikpLCBOb25lKQppZiBiMTUuZ2V0KCJ0MTM2IikgPT0gIlFVQSI6CiAgICBrZXQoIk4xMiB0'
'MTM2IChxdWEga2V0IHF1YSBjYSkiLCBEQVQsICJ0MTM2IFFVQSIpCmVsaWYgYjE1LmdldCgidDEzNiIpIGlzIE5vbmU6CiAgICBr'
'ZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBLREQsICJraG9uZyB0aGF5IHQxMzYgdHJvbmcgbG9nIikKZWxzZToKICAg'
'IGx5ID0gZG9faGV0LmdldCh0MTM2X3RlbiwgIiIpCiAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBUUlVPVCwg'
'ZiJETzoge2x5Wzo5MF19IikKCiMgLS0tLS0tLS0tLS0tLS0tLSAzLiBwcm9iZSBUSEFORyB2YW8gaGFtIC0tLS0tLS0tLS0tLS0t'
'LS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIzLiBQUk9CRSBUSEFORyDigJQgZ29pIF9naXRfd2luZG93cyB2b2kgdGhh'
'bSBzbyB0aWVtIikKc3BlYyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscDU0MSIsIHN0cih0ZXAp'
'KQpscCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9kdWxlKGxwKQpz'
'aWcgPSBpbnNwZWN0LnNpZ25hdHVyZShscC5fZ2l0X3dpbmRvd3MpCmdoaSgidGhhbV9zb19fZ2l0X3dpbmRvd3MiLCBsaXN0KHNp'
'Zy5wYXJhbWV0ZXJzKSkKaW5uKCIgIHRoYW0gc28gY3VhIF9naXRfd2luZG93czoiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKCmRl'
'ZiBnb2koKiprdyk6CiAgICAiIiJHb2kgX2dpdF93aW5kb3dzLCBCQVQgc3RkZXJyIGRlIG1vdCBkb25nIGNoYW4gZG9hbiBraG9u'
'ZyBnaWV0IGx1b3QgZG8uIiIiCiAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVy'
'cihlKToKICAgICAgICByID0gbHAuX2dpdF93aW5kb3dzKCoqa3cpCiAgICByZXR1cm4gciwgZS5nZXR2YWx1ZSgpCgojIC0tLSBk'
'b2kgY2h1bmcgcmlnOiBwaGFpIHRyYSBsb2kgZHVuZyBtb3QgY2EgdGEgQklFVCBUUlVPQyBkYXAgYW4gLS0tCndpdGggdGVtcGZp'
'bGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgIG5nb2FpID0gUGF0aCh0KS8ibmdvYWkiOyBuZ29haS5ta2RpcigpOyBj'
'dyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAobmdvYWkvImdp'
'dC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIxLCBfID0gZ29pKHBhdGg9c3RyKG5nb2FpKSwg'
'cHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIChjdy8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNv'
'ZGluZz0idXRmLTgiKQogICAgcjIsIF8gPSBnb2kocGF0aD1zdHIoY3cpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIo'
'Y3cpKQpyaWdfb2sgPSBib29sKHIxKSBhbmQgcjIgaXMgTm9uZQpnaGkoInJpZ19kb2lfY2h1bmciLCByaWdfb2spCmtldCgiUklH'
'IGRvaSBjaHVuZyAoYmlldCB0cnVvYyBkYXAgYW4pIiwgREFUIGlmIHJpZ19vayBlbHNlIEtERCwKICAgIGYibmdvYWktY3dkLT57'
'J05IQU4nIGlmIHIxIGVsc2UgJ05vbmUnfSB8IHRyb25nLWN3ZC0+eydOSEFOJyBpZiByMiBlbHNlICdOb25lJ30iKQppZiBub3Qg'
'cmlnX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiByaWcgc2FpLCBtb2kgY2hvdCBkdW9pIHNlIHZvIG5naGlh'
'LiIpOyBzeXMuZXhpdCgzKQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwpIGluIFsodCwgZihnb2ksIHNpZywgdGVwdCkpIGZvciB0LCBm'
'IGluIFBST0JFXToKICAgIGdoaSgicHJvYmVfIiArIHRlbi5zcGxpdCgpWzBdLmxvd2VyKCksIGRsKQogICAgaWYgaXNpbnN0YW5j'
'ZShkbCwgZGljdCk6CiAgICAgICAgZm9yIGssIHYgaW4gZGwuaXRlbXMoKTogaW5uKGYiICAgIHtrOjM0fToge3Z9IikKICAgIGtl'
'dCh0ZW4sIHR0LCBjdCkKCiMgLS0tLS0tLS0tLS0tLS0tLSA0LiBONyBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIC0tLS0tLS0t'
'LS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCI0LiBONyDigJQgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAo'
'Y2F5IHRoYXQgS0hPTkcgYmkgZHVuZyB0b2kpIikKdHJ1b2MgPSB0ZXAucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50'
'KE1BVV9XSU4pCmdoaSgibjdfdHJ1b2MiLCB0cnVvYyk7IGlubihmIiAgc28gZG9uZyBraG9wIHtNQVVfV0lOIXJ9OiBUUlVPQyA9'
'IHt0cnVvY30gW21vbmcgMV0iKQppZiB0cnVvYyAhPSAxOgogICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RE'
'LCBmIm1hdSB4dWF0IGhpZW4ge3RydW9jfSBsYW4sIGtob25nIHBoYWkgMSIpCmVsc2U6CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBv'
'cmFyeURpcmVjdG9yeSgpIGFzIHRtcDoKICAgICAgICBzYW8gPSBQYXRoKHRtcCkvImNheSIKICAgICAgICBzaHV0aWwuY29weXRy'
'ZWUoZ29jLCBzYW8sIGlnbm9yZT1zaHV0aWwuaWdub3JlX3BhdHRlcm5zKCIuZ2l0IiwgIl9fcHljYWNoZV9fIiwgIioucHljIikp'
'CiAgICAgICAgZjIgPSBzYW8vIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiCiAgICAgICAgZjIud3JpdGVfdGV4dChmMi5yZWFkX3Rl'
'eHQoZW5jb2Rpbmc9InV0Zi04IikucmVwbGFjZShNQVVfV0lOLCAiaWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAg'
'ICAgc2F1ID0gZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4pOyBnaGkoIm43X3NhdSIsIHNhdSkK'
'ICAgICAgICBpbm4oZiIgIFNBVSAoZGEgZG90IGJpZW4pID0ge3NhdX0gW21vbmcgMF0iKQogICAgICAgIGlmIHNhdSAhPSAwOgog'
'ICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsICJkb3QgYmllbiBLSE9ORyBhcCBkdW9jIikK'
'ICAgICAgICBlbHNlOgogICAgICAgICAgICByY19tLCBvdXRfbSA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0s'
'IHNhbykKICAgICAgICAgICAgbTE2NSA9IG1hdV9jYShvdXRfbSwgInQxNjUiKTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20pCiAg'
'ICAgICAgICAgIHRlbjE2NSA9IG5leHQoKHQgZm9yIHQgaW4gZG0gaWYgdC5zdGFydHN3aXRoKCJ0MTY1IikpLCBOb25lKQogICAg'
'ICAgICAgICBseSA9IChkbS5nZXQodGVuMTY1KSBvciAiIikKICAgICAgICAgICAgZ2hpKCJuN190MTY1IiwgbTE2NSk7IGdoaSgi'
'bjdfbHlfZG8iLCBseVs6MjAwXSkKICAgICAgICAgICAgaW5uKGYiICB0MTY1IHNhdSBkb3QgYmllbjoge20xNjV9IHwge2x5Wzox'
'MTBdfSIpCiAgICAgICAgICAgIGR1bmdfbHlfZG8gPSAiUEFUSCB0IiBpbiBseSBvciAiL3Vzci9iaW4iIGluIGx5CiAgICAgICAg'
'ICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIERBVCBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKSBl'
'bHNlCiAgICAgICAgICAgICAgICAoVFJVT1QgaWYgbTE2NSA9PSAiRE8iIGVsc2UgS0REKSwKICAgICAgICAgICAgICAgICJnaWV0'
'IGR1bmcgbHkgZG8iIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pCiAgICAgICAgICAgICAgICBlbHNlICgiRE8gbmh1'
'bmcgS0hPTkcgZHVuZyBseSBkbyAtPiB0aW4gZHVuZyBnaWEiIGlmIG0xNjUgPT0gIkRPIiBlbHNlICJraG9uZyBkb2MgZHVvYyB0'
'MTY1IikpCgojIC0tLS0tLS0tLS0tLS0tLS0gS0VUIExVQU4gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIj0iICogNzgp'
'CmlubihmIlRIRSBIRSBETyBEVU9DOiB7dGhlX2hlfSAgIEhFQUQ9e2hlYWRbOjEyXX0iKQppZiB0aGVfaGUgPT0gImcxIjoKICAg'
'IGlubigiTFVVIFk6IGRheSBsYSBORU4gRE8gKGcxKSwgS0hPTkcgcGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hvdCBOOC1OMTIg'
'ZHVvaSBkYXkiKQogICAgaW5uKCIgICAgICAgVFJVT1QgbGEgRFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEgbmh1bmcgbG8gZzIg'
'c2luaCByYSBkZSB2w6EuIikKaW5uKCItIiAqIDc4KQpmb3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAgIGlubihmIiAge3R0OjE0'
'fSB7dGVufSIgKyAoZiIgICB7Y3R9IiBpZiBjdCBlbHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlm'
'IHQgPT0gS0REKQpuX3RydW90ID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQppbm4oIi0iICogNzgp'
'CmlubihmIiAgREFUIHtzdW0oMSBmb3IgXyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8IFRSVU9UIHtuX3RydW90fSB8IEtIT05H'
'IERPIERVT0Mge25fa2RkfSIpCmlubihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgnc29fY2FfZG8nKX0gfCBkYW5oIHNhY2ggZGF5'
'IGR1OiB7J0NPJyBpZiBzby5nZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAnS0hPTkcgRE8gRFVPQyd9IikKaW5uKGYiICBBZG1p'
'bmlzdHJhdG9yOiB7c28uZ2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxpbms6IHtzby5nZXQoJ3N5bWxpbmtfZHVvYycpfSIpCmlu'
'bigiIik7IGlubigiLS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5BWSBWRSBDSE8gUkVWSUVXRVIgLS0tIikKZ2hpKCJjaG90Iiwg'
'W3sidGVuIjogYSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3RpZXQiOiBjfSBmb3IgYSwgYiwgYyBpbiBjaG90XSkKaW5uKGpzb24u'
'ZHVtcHMoc28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50PTEsIGRlZmF1bHQ9c3RyKSkKIyByYzogMCA9IG1vaSBjaG90IERB'
'VCB8IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNvIGNob3QgS0hPTkcgRE8gRFVPQyAodXUgdGllbiBiYW8gZG9uZykKc3lzLmV4'
'aXQoMyBpZiBuX2tkZCBlbHNlICgxIGlmIG5fdHJ1b3QgZWxzZSAwKSkK'
)
$goi  = ($B64 -join '')
try { $byte = [Convert]::FromBase64String($goi) } catch { Dung "giai base64 hong: $($_.Exception.Message)" }
# Ghi ra tep TAM roi moi kiem bam, dat thi mo i chuyen vao cho. Ghi thang vao dich
# roi kiem sau nghia la mot goi hong VAN de lai rac dung ten that tren dia - va lan
# chay sau co the doc phai no. Do duoc: doi mot ky tu base64 => bam lech, rc=3.
$tam = "$BoDo.tam"
[IO.File]::WriteAllBytes($tam, $byte)
$bd = Bam $tam
Write-Host "sha256 : $bd"
Write-Host "mong   : $ShaBoDo"
if ($bd -ne $ShaBoDo) { Remove-Item -Force -LiteralPath $tam; Dung 'bo do Python LECH bam - khong ghi, khong chay' }
Move-Item -Force -LiteralPath $tam -Destination $BoDo
Write-Host "ghi ra : $BoDo  ($($byte.Length) byte)"
Write-Host 'toan ven: DAT' -ForegroundColor Green
if ($ChiGiaiNen) { Write-Host ''; Write-Host 'Chi giai nen theo yeu cau. Dung tai day.'; exit 0 }

# ---------------------------------------------------------------- 4. kho do
Tieu 'Kho do'
if (Test-Path -LiteralPath (Join-Path $Kho '.git')) {
    Write-Host "clone do da co: $Kho"
} elseif (Test-Path -LiteralPath (Join-Path $Nguon '.git')) {
    Write-Host "dung clone do tu kho san co: $Nguon"
    G clone --no-single-branch --quiet -- "$Nguon" "$Kho" | Out-Null
    G -C "$Kho" remote set-url origin "$Url" | Out-Null
} else {
    Write-Host "khong thay kho san co -> clone thang tu $Url (vai phut)"
    G clone --no-single-branch --quiet -- "$Url" "$Kho" | Out-Null
}
# core.abbrev = 7: khong ghim thi mot so cong do bam ngan khac di va do lech.
G -C "$Kho" config core.abbrev 7 | Out-Null
# refspec RONG: clone --depth / --single-branch siet refspec lai mot nhanh, va do la
# cach "quet moi ref" bien thanh quet dung mot ref (bai hoc da tra gia cua kho nay).
G -C "$Kho" config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' | Out-Null

Write-Host 'fetch ban va fix_issue_541 ...'
G -C "$Kho" fetch --quiet origin fix_issue_541 | Out-Null
G -C "$Kho" checkout --quiet -B fix_issue_541 FETCH_HEAD | Out-Null
G -C "$Kho" reset --hard --quiet FETCH_HEAD | Out-Null

$head = (G -C "$Kho" rev-parse --short HEAD) | Select-Object -First 1
# KHONG ghim SHA. Ban va g2 chua ton tai luc viet tep nay, va ghim mot SHA se lam
# bootstrap tu choi chay dung luc agy vua day xong. Bo do TU PHAN LOAI the he:
#   head == 2f70869a  -> g1, chua co ban va g2 (van do, nhan la NEN DO)
#   head la hau due   -> ung vien g2
#   khac              -> KHONG DO DUOC, rc=3
Write-Host "HEAD : $head   (g1 = 2f70869; bo do se tu phan loai the he)"

# ---------------------------------------------------------------- 5. chay
Tieu 'Chay phep do g2 (bo test chay HAI lan - tinh 20-45 phut)'
Write-Host "log : $Log"
Write-Host ('-' * 70)
# HAI chot cho lan goi nay, ca hai deu la bai hoc tra bang mot luot do da mat:
#  (1) $ErrorActionPreference='Stop' + `2>&1` tren Windows PowerShell 5.1 bien MOI dong
#      stderr cua tien trinh con thanh loi CHI MANG. Bo test va ban va DEU ghi chan doan
#      ra stderr mot cach co chu dich, nen mot dong chan doan giet ca luot do. Da xay ra
#      that 18-09-2026: bo test chay xong ma N7 khong bao gio chay.
#  (2) rc KHAC 0 o day la KET QUA HOP LE (rc=1 nghia la "co chot truot"), khong phai loi.
#      PowerShell 7.3+ co $PSNativeCommandUseErrorActionPreference; bat len cong voi 'Stop'
#      thi mot rc=1 hop le cung thanh ngoai le. Tat tuong minh, roi tra lai nhu cu.
$eapCu = $ErrorActionPreference
$pnCu  = $null
if (Test-Path variable:PSNativeCommandUseErrorActionPreference) {
    $pnCu = $PSNativeCommandUseErrorActionPreference
    $PSNativeCommandUseErrorActionPreference = $false
}
$ErrorActionPreference = 'Continue'
$env:PYTHONUNBUFFERED = '1'   # dau ra ra THANG, de mot cu chet giua chung khong nuot sach log
& $pyCmd.Source $BoDo $Kho 2>&1 | Tee-Object -FilePath $Log
$rc = $LASTEXITCODE
$ErrorActionPreference = $eapCu
if ($null -ne $pnCu) { $PSNativeCommandUseErrorActionPreference = $pnCu }
Write-Host ('-' * 70)

# ---------------------------------------------------------------- 6. ket qua
Write-Host ''
Write-Host "rc = $rc"
switch ($rc) {
    0       { Write-Host 'MOI CHOT DAT'   -ForegroundColor Green }
    1       { Write-Host 'CO CHOT TRUOT'  -ForegroundColor Yellow }
    3       { Write-Host 'KHONG DO DUOC (co chot khong do duoc, hoac nen do sai)' -ForegroundColor Red }
    default { Write-Host "rc la $rc"      -ForegroundColor Red }
}
Write-Host ''
Write-Host ('=' * 70)
Write-Host 'DAN NGUYEN KHOI DUOI DAY VE CHO REVIEWER (tu dong ke tiep den het):'
Write-Host ('=' * 70)
# In lai phan ket luan: tu dong ke ca do dau tien tro di. Khong tim thay thi in ca log.
$dong = @(Get-Content -LiteralPath $Log -Encoding UTF8)
$i = -1
for ($k = 0; $k -lt $dong.Count; $k++) {
    if ($dong[$k] -match 'CA DO doc duoc|KHONG_DO_DUOC|doi chieu bo doc') { $i = $k; break }
}
if ($i -ge 0) { $dong[$i..($dong.Count - 1)] | ForEach-Object { Write-Host $_ } }
else          { $dong | ForEach-Object { Write-Host $_ } }
Write-Host ('=' * 70)
Write-Host "Ban day du: $Log"
if (-not $admin) {
    Write-Host ''
    Write-Host 'NHAC: luot nay chay KHONG co quyen Administrator. Cac ca can symlink se do' -ForegroundColor Yellow
    Write-Host '      vi quyen chu khong vi ban va. Chay lai bang "Run as administrator" thi' -ForegroundColor Yellow
    Write-Host '      tach duoc hai nguyen nhan ay.' -ForegroundColor Yellow
}
exit $rc
