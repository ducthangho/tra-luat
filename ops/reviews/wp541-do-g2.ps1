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
$ShaBoDo    = '3f3ff5e5845578c8341ae1c62def96d6eabcb5beeac830d7d19eedcc48ca1719'      # SHA-256 cua bo do Python nhung ben duoi

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
'IiksIGZsdXNoPVRydWUpCgpTSEFfRzEgICA9ICIyZjcwODY5YTA1Mzc4NDNlOWNhZTc4NjE4ZWU3YWU4YzI2MWQ5NzJkIgpTSEFf'
'QkFTRSA9ICJkNzA1NjIzMTYyYjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpUUkFOX1RFUCwgVFJBTl9ET05HID0gMiwg'
'NDAwICAgICAgICAgICMgTjcnIGN1YSBzcGVjIHIzCk1BVV9XSU4gID0gJ2lmIG5lbl90aHVjID09ICJ3aW5kb3dzIjonCkNBMTUg'
'ID0gInQxMjkgdDEzMCB0MTMxIHQxMzIgdDEzMyB0MTM2IHQxMzggdDEzOSB0MTQ0IHQxNDUgdDE0NiB0MTQ3IHQxNDkgdDE1MCB0'
'MTUxIi5zcGxpdCgpCkNBTU9JID0gInQxNjUgdDE2NiB0MTY3IHQxNjgiLnNwbGl0KCkKCkRBVCwgVFJVT1QsIEtERCA9ICJEQVQi'
'LCAiVFJVT1QiLCAiS0hPTkcgRE8gRFVPQyIKc28sIGNob3QgPSB7fSwgW10KZGVmIGdoaShrLCB2KTogc29ba10gPSB2OyByZXR1'
'cm4gdgpkZWYga2V0KHRlbiwgdHJhbmdfdGhhaSwgY2hpX3RpZXQ9IiIpOgogICAgY2hvdC5hcHBlbmQoKHRlbiwgdHJhbmdfdGhh'
'aSwgY2hpX3RpZXQpKQogICAgaW5uKGYiICBbe3RyYW5nX3RoYWk6MTR9XSB7dGVufSIgKyAoZiIgICB7Y2hpX3RpZXR9IiBpZiBj'
'aGlfdGlldCBlbHNlICIiKSkKICAgIHJldHVybiB0cmFuZ190aGFpCgojIC0tLS0tLS0tLS0tLS0tLS0gZG9jIGxvZyBjdWEgYm8g'
'dGVzdCAoYmFuIDMsIGRhIGRvIHRyZW4gbG9nIFRIQVQpIC0tLS0tLS0tLS0tLS0tLS0KUlhfRE9fQ0hPICA9IHJlLmNvbXBpbGUo'
'ciIoP20pXiEhISBkbyAoXFMrKSAoLiopJCIpClJYX0RPX0NVT0kgPSByZS5jb21waWxlKHIiKD9tKV4gezJ9KFxTezEsNH0pIHsy'
'fShcUyspOiAoLiopJCIpClJYX0JPX1FVQSAgPSByZS5jb21waWxlKHIiKD9tKV4gezJ9XFN7MSw2fSBRVUEgKFxTKyk6ICguKikk'
'IikKUlhfVE9ORyAgICA9IHJlLmNvbXBpbGUociJsZWFzZV9wdWJsaXNoOiAoXGQrKS8oXGQrKVxiW15cbl0qPz0oXGQrKSxbXlxu'
'XSo/PShcZCspIikKCmRlZiBzb19jYSh0KToKICAgIG0gPSByZS5tYXRjaChyInQoXGQrKSIsIHQpOyByZXR1cm4gKGludChtLmdy'
'b3VwKDEpKSBpZiBtIGVsc2UgMTAqKjYsIHQpCgpkZWYgZG9jX2RvKG91dCk6CiAgICB0YWlfY2hvID0ge3Q6IGwuc3RyaXAoKSBm'
'b3IgdCwgbCBpbiBSWF9ET19DSE8uZmluZGFsbChvdXQpfQogICAgYm8gPSB7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFs'
'bChvdXQpfQogICAgY3VvaSA9IHt0OiBsLnN0cmlwKCkgZm9yIF8sIHQsIGwgaW4gUlhfRE9fQ1VPSS5maW5kYWxsKG91dCkgaWYg'
'dCBub3QgaW4gYm99CiAgICBob3AgPSBkaWN0KGN1b2kpOyBob3AudXBkYXRlKHRhaV9jaG8pCiAgICBnYywgdGluID0gW10sIFRy'
'dWUKICAgIGlmIHNldCh0YWlfY2hvKSAhPSBzZXQoY3VvaSk6CiAgICAgICAgZ2MuYXBwZW5kKGYiaGFpIG5ndW9uIExFQ0g6IGNo'
'aS10YWktY2hvPXtzb3J0ZWQoc2V0KHRhaV9jaG8pLXNldChjdW9pKSl9IGNoaS1jdW9pPXtzb3J0ZWQoc2V0KGN1b2kpLXNldCh0'
'YWlfY2hvKSl9IikKICAgICAgICB0aW4gPSBGYWxzZQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dCkKICAgIGlmIG5vdCBtOgog'
'ICAgICAgIGdjLmFwcGVuZCgiS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCIpOyB0aW4gPSBGYWxzZQogICAgZWxzZToKICAg'
'ICAgICBkYXQsIHRyZW4gPSBpbnQobS5ncm91cCgxKSksIGludChtLmdyb3VwKDIpKQogICAgICAgIGdjLmFwcGVuZChmInNvIGhv'
'Yzoge3RyZW59LXtkYXR9PXt0cmVuLWRhdH0gZG87IGRvYyBkdW9jIHtsZW4oaG9wKX0iKQogICAgICAgIGlmIHRyZW4gLSBkYXQg'
'IT0gbGVuKGhvcCk6CiAgICAgICAgICAgIGdjLmFwcGVuZChmIkxFQ0ggU08gSE9DOiB0aGlldSB7dHJlbi1kYXQtbGVuKGhvcCl9'
'IGNhIik7IHRpbiA9IEZhbHNlCiAgICByZXR1cm4gaG9wLCBnYywgdGluCgpfTUFVID0gKCIhISEgZG8gdDAyYl90ZW5fS0hPTkdf'
'Q09fVEhBTV9RVVlFTiBhXG4iCiAgICAgICAgIiEhISBkbyB0MTUwX3ggV2luRXJyb3IgMTMxNCByZXF1aXJlZCBwcml2aWxlZ2Vc'
'biIKICAgICAgICAiICBC4buOIFFVQSB0MTMxX3k6IG5lbiBmaXh0dXJlXG4iCiAgICAgICAgIiAgxJDhu44gIHQwMmJfdGVuX0tI'
'T05HX0NPX1RIQU1fUVVZRU46IGFcbiIKICAgICAgICAiICDEkOG7jiAgdDE1MF94OiBXaW5FcnJvciAxMzE0IHJlcXVpcmVkIHBy'
'aXZpbGVnZVxuIgogICAgICAgICJsZWFzZV9wdWJsaXNoOiAxLzMgxJHhuqF0OyDEkcOjIGNo4bqheT0zLCBi4buPIHF1YT0xXG4i'
'KQoKZGVmIGNoYXkoYXJndiwgY3dkLCBwaHV0PTYwKToKICAgIG10ID0gZGljdChvcy5lbnZpcm9uLCBQWVRIT05VVEY4PSIxIiwg'
'UFlUSE9OSU9FTkNPRElORz0idXRmLTgiLAogICAgICAgICAgICAgIFBZVEhPTkRPTlRXUklURUJZVEVDT0RFPSIxIiwgUFlUSE9O'
'VU5CVUZGRVJFRD0iMSIpCiAgICBwID0gc3VicHJvY2Vzcy5ydW4oW3N5cy5leGVjdXRhYmxlXSArIGFyZ3YsIGN3ZD1zdHIoY3dk'
'KSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwKICAgICAgICAgICAgICAgICAgICAgICB0ZXh0PVRydWUsIGVuY29kaW5nPSJ1dGYtOCIs'
'IGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCwgZW52PW10KQogICAgcmV0dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rk'
'b3V0IG9yICIiKSArIChwLnN0ZGVyciBvciAiIikKCmRlZiBtYXVfY2Eob3V0LCB0KToKICAgIG0gPSByZS5zZWFyY2gociIoP20p'
'Xjw8PCByYSAoIiArIHQgKyByIlthLXpdP19cUyopIFswLTkuXStzIChcdyspXHMqJCIsIG91dCkKICAgIHJldHVybiBtLmdyb3Vw'
'KDIpIGlmIG0gZWxzZSBOb25lCgpkZWYgZ2l0KGdvYywgKmEsIHBodXQ9NSk6CiAgICBwID0gc3VicHJvY2Vzcy5ydW4oWyJnaXQi'
'LCAiLUMiLCBzdHIoZ29jKSwgKmFdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsCiAgICAgICAgICAgICAgICAgICAg'
'ICAgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD1waHV0KjYwKQogICAgcmV0dXJuIHAucmV0dXJu'
'Y29kZSwgKHAuc3Rkb3V0IG9yICIiKS5zdHJpcCgpLCAocC5zdGRlcnIgb3IgIiIpLnN0cmlwKCkKCgojID09PT09PT09PT09PT09'
'PT09IE5BTSBQUk9CRSwgdmlldCB0aGFuaCBIQU0gVEhVQU4gZGUgVFUgS0lFTSBkdW9jID09PT09PT09PT09PT09PT09CiMgTW9p'
'IGhhbSB0cmEgKHRyYW5nX3RoYWksIGNoaV90aWV0LCBkdV9saWV1KS4gS0hPTkcgaW4sIEtIT05HIHRob2F0IOKAlCBuaG8gdmF5'
'IGNodW5nCiMgY2hheSBkdW9jIHRyZW4gbmVuIEJBVCBLWSwgdmEgYC0tdHUta2llbS1wcm9iZWAgZ29pIHRoYW5nIGNodW5nIGRl'
'IGtpZW0gY2hpbmggYm8gZG8uCgpkZWYgX3Nhbih0KToKICAgIGQgPSBQYXRoKHQpLyJkIjsgZC5ta2RpcigpOyBjdyA9IFBhdGgo'
'dCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICByZXR1cm4gZCwgY3csIHBmCgpk'
'ZWYgZG9fbjgoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiQnVvYyAxIChDT05HX0NVX0dJVCkgY2hpIGR1b2MgbmhhbiBnaXQuZXhl'
'LiBEb2kgY2h1bmcgZHVvbmc6IGdpdC5leGUgVkFOIHBoYWkgbmhhbi4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVtcGZpbGUu'
'VGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgZm9yIHRlbiBpbiAo'
'ImdpdC5leGUiLCAiZ2l0LmJhdCIsICJnaXQuY21kIiwgImdpdC5weSIsICJraG9uZy1waGFpLWdpdC50eHQiKToKICAgICAgICAg'
'ICAgZiA9IGQvdGVuOyBmLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBfID0gZ29pKGNv'
'bmdfY3VfZ2l0PXN0cihmKSwgcGF0aD0iIiwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAg'
'a3FbZiJDT05HX0NVX0dJVD17dGVufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiVFUgQ0hPSSIKICAgIGxvdCA9IFtrIGZvciBrLCB2'
'IGluIGtxLml0ZW1zKCkgaWYgdiA9PSAiTkhBTiIgYW5kIG5vdCBrLmVuZHN3aXRoKCJnaXQuZXhlIildCiAgICBpZiBrcS5nZXQo'
'IkNPTkdfQ1VfR0lUPWdpdC5leGUiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25n'
'OiBnaXQuZXhlIGhvcCBsZSBtYSBiaSB0dSBjaG9pIiwga3EKICAgIHJldHVybiAoREFUIGlmIG5vdCBsb3QgZWxzZSBUUlVPVCks'
'ICgiIiBpZiBub3QgbG90IGVsc2UgZiJjb24gbmhhbjoge2xvdH0iKSwga3EKCmRlZiBkb19uOShnb2ksIHNpZywgdGVwdCk6CiAg'
'ICAiIiJNdWMgUEFUSCBib2MgbmhheSBrZXAgcGhhaSBOSEFOOyBtdWMgcm9uZyAvIHRvYW4ga2hvYW5nIHRyYW5nIHBoYWkgYm8g'
'cXVhLCBraG9uZyBuZW0uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6'
'CiAgICAgICAgZCA9IFBhdGgodCkvImNvIGdpdCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBw'
'ZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5n'
'PSJ1dGYtOCIpCiAgICAgICAgZm9yIG5oYW4sIG11YyBpbiAoKCJraG9uZyBuaGF5Iiwgc3RyKGQpKSwgKCJjbyBuaGF5IGtlcCIs'
'IGYnIntkfSInKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAoInJvbmciLCAiIiksICgiY2hpIGtob2FuZyB0cmFuZyIsICIg'
'ICAiKSk6CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIHIsIF8gPSBnb2kocGF0aD1tdWMsIHByb2dyYW1fZmlsZXM9'
'c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59Il0gPSAiTkhBTiIgaWYgciBlbHNl'
'ICJOb25lIgogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59'
'Il0gPSBmIk5FTSB7dHlwZShlKS5fX25hbWVfX30iCiAgICBpZiBrcS5nZXQoIlBBVEgga2hvbmcgbmhheSIpICE9ICJOSEFOIjoK'
'ICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG11YyBQQVRIIHRodW9uZyBtYSBraG9uZyB0aW0gcmEg'
'Z2l0LmV4ZSIsIGtxCiAgICBvayA9IChrcS5nZXQoIlBBVEggY28gbmhheSBrZXAiKSA9PSAiTkhBTiIKICAgICAgICAgIGFuZCBr'
'cS5nZXQoIlBBVEggcm9uZyIpID09ICJOb25lIiBhbmQga3EuZ2V0KCJQQVRIIGNoaSBraG9hbmcgdHJhbmciKSA9PSAiTm9uZSIp'
'CiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgpkZWYgZG9f'
'bjEwKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIk1vdCBkYXUgJzsnIHRyb25nIFRFTiB0aHUgbXVjIGtob25nIGR1b2MgbGFtIG1h'
'dCBtdWMgZ2l0LmV4ZSBob3AgbGUgbyBtdWMga2lhLiIiIgogICAgY29fc2VwID0gYW55KCgiY2FjaCIgaW4gaykgb3IgKCJzZXAi'
'IGluIGsubG93ZXIoKSkgZm9yIGsgaW4gc2lnLnBhcmFtZXRlcnMpCiAgICBpZiBvcy5wYXRoc2VwID09ICI7IiBhbmQgbm90IGNv'
'X3NlcDoKICAgICAgICByZXR1cm4gKEtERCwgInRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyB2YSBoYW0ga2hvbmcg'
'bmhhbiB0aGFtIHNvIGRhdSBwaGFuIGNhY2ggIgogICAgICAgICAgICAgICAgICAgICAiLT4ga2hvbmcgdGFjaCBkdW9jIGhhaSBn'
'aWEgdGh1eWV0IiwgeyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgImNvIHRoYW0gc28gc2VwIjogY29fc2VwfSkKICAgIHdpdGgg'
'dGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGly'
'KCkKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rp'
'bmc9InV0Zi04IikKICAgICAgICByLCBfID0gZ29pKHBhdGg9c3RyKGxhKSArIG9zLnBhdGhzZXAgKyBzdHIoZCksIHByb2dyYW1f'
'ZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgcjAsIF8gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9'
'c3RyKHBmKSwgY3dkPXN0cihjdykpICAgICAjIGRvaSBjaHVuZyBkdW9uZwogICAga3EgPSB7ImNvIG11YyBjaHVhICc7JyI6ICJO'
'SEFOIiBpZiByIGVsc2UgIk5vbmUiLCAiZG9pIGNodW5nIChraG9uZyBjbyAnOycpIjogIk5IQU4iIGlmIHIwIGVsc2UgIk5vbmUi'
'fQogICAgaWYgbm90IHIwOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZyIsIGtxCiAgICByZXR1cm4g'
'KERBVCBpZiByIGVsc2UgVFJVT1QpLCAoIiIgaWYgciBlbHNlICJtdWMgZ2l0LmV4ZSBob3AgbGUgYmkgTUFUIiksIGtxCgpkZWYg'
'ZG9fbjExKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIlRydXllbiBjaGFuX2RvYW4gPT4gdGh1IGR1b2MgdGhvbmcgYmFvIFZBIHN0'
'ZGVyciBJTS4gS2hvbmcgdHJ1eWVuID0+IHN0ZGVyciBWQU4gY28uIiIiCiAgICBpZiAiY2hhbl9kb2FuIiBub3QgaW4gc2lnLnBh'
'cmFtZXRlcnM6CiAgICAgICAgcmV0dXJuIEtERCwgIl9naXRfd2luZG93cyBraG9uZyBuaGFuIHRoYW0gc28gY2hhbl9kb2FuIiwg'
'eyJ0aGFtIHNvIjogbGlzdChzaWcucGFyYW1ldGVycyl9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFz'
'IHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29k'
'aW5nPSJ1dGYtOCIpCiAgICAgICAgY2QgPSBbXQogICAgICAgIF8sIGVfY28gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmls'
'ZXM9c3RyKHBmKSwgY3dkPXN0cihjdyksIGNoYW5fZG9hbj1jZCkKICAgICAgICBfLCBlX2toID0gZ29pKHBhdGg9c3RyKGQpLCBw'
'cm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAga3EgPSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAobXVjKSI6IGxl'
'bihjZCksCiAgICAgICAgICAic3RkZXJyIGtoaSBDTyBjaGFuX2RvYW4gKGJ5dGUpIjogbGVuKGVfY28uZW5jb2RlKCkpLAogICAg'
'ICAgICAgInN0ZGVyciBraGkgS0hPTkcgdHJ1eWVuIChieXRlKSI6IGxlbihlX2toLmVuY29kZSgpKX0KICAgIGlmIGxlbihjZCkg'
'PT0gMCBhbmQgbGVuKGVfa2guZW5jb2RlKCkpID09IDA6CiAgICAgICAgcmV0dXJuIEtERCwgIm5oYW5oICVQcm9ncmFtRmlsZXMl'
'IGtob25nIHBoYW4gZ2lhaSBLSE9ORyBiYXkgcmEgY2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRvIGR1b2MiLCBrcQogICAgb2sgPSBs'
'ZW4oY2QpID4gMCBhbmQgbGVuKGVfY28uZW5jb2RlKCkpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA+IDAKICAgIHJldHVy'
'biAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCmRlZiBkb19uMTIoZ29pLCBz'
'aWcsIHRlcHQpOgogICAgIiIiSGFuZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9uZyBmaXh0dXJlIHBoYWkgdHV5ZXQgZG9pIHRyZW4g'
'Q0EgSEFJIG5lbi4iIiIKICAgIG5kID0gdGVwdC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIikK'
'ICAgIGhhbmcgPSBzb3J0ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRfcGF0aFxzKj1ccyoiKFteIl0rKSInLCBuZCkpKQogICAgeGF1'
'ID0gW2ggZm9yIGggaW4gaGFuZyBpZiBub3QgKFB1cmVQb3NpeFBhdGgoaCkuaXNfYWJzb2x1dGUoKSBhbmQgUHVyZVdpbmRvd3NQ'
'YXRoKGgpLmlzX2Fic29sdXRlKCkpXQogICAga3EgPSB7ImhhbmcgZ2l0X3BhdGggdGltIHRoYXkiOiBoYW5nLCAiY2hpIHR1eWV0'
'IGRvaSBNT1QgbmVuIjogeGF1fQogICAgaWYgbm90IGhhbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImtob25nIHRpbSB0aGF5IGhh'
'bmcgZ2l0X3BhdGggbmFvIHRyb25nIGZpeHR1cmUgLT4gbWF1IGRvYyBjbyB0aGUgZGEgZG9pIiwga3EKICAgIHJldHVybiAoREFU'
'IGlmIG5vdCB4YXUgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgeGF1IGVsc2UgZiJjaGktbW90LW5lbjoge3hhdX0iKSwga3EKClBS'
'T0JFID0gWygiTjggYnVvYyAxIGNoaSBuaGFuIGdpdC5leGUiLCBkb19uOCksCiAgICAgICAgICgiTjkgYm9jIG5oYXkga2VwIG8g'
'bXVjIFBBVEgiLCBkb19uOSksCiAgICAgICAgICgiTjEwIGRhdSAnOycgdHJvbmcgdGVuIHRodSBtdWMiLCBkb19uMTApLAogICAg'
'ICAgICAoIk4xMSBjaGFuIGRvYW4gZG9pIGtlbmgiLCBkb19uMTEpLAogICAgICAgICAoIk4xMiBoYW5nIHNlbnRpbmVsIHR1eWV0'
'IGRvaSBDQSBIQUkgbmVuIiwgZG9fbjEyKV0KCiMgLS0tIGNoZSBkbyBUVSBLSUVNOiBjaGF5IG5hbSBwcm9iZSB0cmVuIG1vdCBj'
'YXkgYmF0IGt5LCBuZW4gYmF0IGt5IC0tLQppZiAiLS10dS1raWVtLXByb2JlIiBpbiBzeXMuYXJndjoKICAgIF9nID0gUGF0aChz'
'eXMuYXJndltzeXMuYXJndi5pbmRleCgiLS10dS1raWVtLXByb2JlIikgKyAxXSkucmVzb2x2ZSgpCiAgICBfc3AgPSBpbXBvcnRs'
'aWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfdGsiLCBzdHIoX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkK'
'ICAgIF9scCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbHAp'
'CiAgICBfc2lnID0gaW5zcGVjdC5zaWduYXR1cmUoX2xwLl9naXRfd2luZG93cykKICAgIGRlZiBfZ29pKCoqa3cpOgogICAgICAg'
'IGUgPSBpby5TdHJpbmdJTygpCiAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICAgICAg'
'cmV0dXJuIF9scC5fZ2l0X3dpbmRvd3MoKiprdyksIGUuZ2V0dmFsdWUoKQogICAgcHJpbnQoZiJUVSBLSUVNIFBST0JFIHRyZW4g'
'e19nfSAgKG5lbiB7c3lzLnBsYXRmb3JtfSkiKQogICAgZm9yIF90ZW4sIF9mIGluIFBST0JFOgogICAgICAgIF90dCwgX2N0LCBf'
'ZGwgPSBfZihfZ29pLCBfc2lnLCBfZy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBwcmludChmIiAgW3tf'
'dHQ6MTR9XSB7X3Rlbn0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgICAgICBmb3IgX2ssIF92IGluIChfZGwg'
'b3Ige30pLml0ZW1zKCk6IHByaW50KGYiICAgICAgICB7X2s6MzR9OiB7X3Z9IikKICAgIHN5cy5leGl0KDApCgppbm4oIj0iICog'
'NzgpOyBpbm4oIldQNTQxIGcyIC0gcGhlcCBkbyB0cmVuIFdpbmRvd3MgdGhhdCAoc3BlYyByMzogTjEtTjQsIE44LU4xMiwgTjcs'
'IGtpY2ggdGh1b2MpIik7IGlubigiPSIgKiA3OCkKCiMgLS0tLS0tLS0tLS0tLS0tLSB0dSBraWVtIGJvIGRvYyAtLS0tLS0tLS0t'
'LS0tLS0tCl9kLCBfZywgX3QgPSBkb2NfZG8oX01BVSkKX29rID0gKGxlbihfZCkgPT0gMiBhbmQgYW55KHguc3RhcnRzd2l0aCgi'
'dDAyYiIpIGZvciB4IGluIF9kKQogICAgICAgYW5kIG5vdCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMxIikgZm9yIHggaW4gX2QpIGFu'
'ZCBfdCkKaW5uKCJUdSBraWVtIGJvIGRvYyBsb2c6IiwgREFUIGlmIF9vayBlbHNlIFRSVU9UKQppZiBub3QgX29rOgogICAgaW5u'
'KCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBibyBkb2MgbG9nIGN1YSBjaGluaCBzY3JpcHQgbmF5IHNhaSAtPiBraG9uZyBkbyBn'
'aSBjYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4gZG8gLS0tLS0tLS0tLS0tLS0tLQpnb2MgPSBQ'
'YXRoKHN5cy5hcmd2WzFdKS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQYXRoLmN3ZCgpCnRlcCwgdGVwdCA9'
'IGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiCmlu'
'bigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMC4gTkVOIERPIikKaW5uKCIgIHN5cy5wbGF0Zm9ybSA6Iiwgc3lzLnBsYXRmb3Jt'
'LCAifCBweXRob24iLCBzeXMudmVyc2lvbi5zcGxpdCgpWzBdKQppbm4oIiAgb3MucGF0aHNlcCAgIDoiLCByZXByKG9zLnBhdGhz'
'ZXApLCAifCBQQVRIRVhUOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlBBVEhFWFQiKSlbOjYwXSkKaW5uKCIgIFByb2dyYW1GaWxl'
'cyA6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUHJvZ3JhbUZpbGVzIikpLCAifCBTeXN0ZW1Sb290OiIsIHJlcHIob3MuZW52aXJv'
'bi5nZXQoIlN5c3RlbVJvb3QiKSkpCmlubigiICBDT05HX0NVX0dJVCAgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIkNPTkdfQ1Vf'
'R0lUIikpKQppbm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5vbmUKaWYgc3lzLnBsYXRmb3JtID09ICJ3aW4z'
'MiI6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4gPSBib29sKGN0eXBlcy53aW5kbGwuc2hlbGwzMi5Jc1Vz'
'ZXJBbkFkbWluKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXllbiA9IE5vbmUKZ2hpKCJxdXllbl9hZG1pbiIsIHF1eWVuKQpz'
'eW1saW5rX2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAg'
'ICBkID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHRyeTogb3Mu'
'c3ltbGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJsayIpKTsgc3ltbGlua19kdW9jID0gVHJ1ZQogICAgICAgIGV4Y2VwdCBPU0Vy'
'cm9yIGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZhbHNlOyBnaGkoInN5bWxpbmtfbG9pIiwgZiJ7dHlwZShlKS5fX25hbWVfX306IHtl'
'fSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZTogZ2hpKCJzeW1saW5rX2xvaSIsIHN0cihlKSkKZ2hpKCJzeW1saW5rX2R1b2MiLCBz'
'eW1saW5rX2R1b2MpCmlubigiICBBZG1pbmlzdHJhdG9yOiIsIHF1eWVuLCAifCB0YW8gc3ltbGluayBkdW9jOiIsIHN5bWxpbmtf'
'ZHVvYykKCmxvaSA9IFtdCmlmIHN5cy5wbGF0Zm9ybSAhPSAid2luMzIiOiBsb2kuYXBwZW5kKGYiS0hPTkcgcGhhaSBXaW5kb3dz'
'IChzeXMucGxhdGZvcm09e3N5cy5wbGF0Zm9ybSFyfSkiKQppZiBub3QgdGVwLmlzX2ZpbGUoKTogIGxvaS5hcHBlbmQoZiJraG9u'
'ZyB0aGF5IHt0ZXB9IikKaWYgbm90IHRlcHQuaXNfZmlsZSgpOiBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwdH0iKQppZiBu'
'b3Qgc2h1dGlsLndoaWNoKCJnaXQiKTogbG9pLmFwcGVuZCgia2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCIpCgpyYywgaGVhZCwg'
'XyA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAiSEVBRCIpCmlmIHJjOiBsb2kuYXBwZW5kKCJraG9uZyBkb2MgZHVvYyBIRUFEIikK'
'Z2hpKCJoZWFkIiwgaGVhZCkKcmNfYSwgXywgXyA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIi0taXMtYW5jZXN0b3IiLCBTSEFf'
'RzEsIGhlYWQgb3IgIkhFQUQiKQpsYV9oYXVfZHVlID0gKHJjX2EgPT0gMCkKaWYgaGVhZCA9PSBTSEFfRzE6CiAgICB0aGVfaGUg'
'PSAiZzEiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IERBWSBMQSBnMS4gQ0hVQSBjbyBiYW4gdmEgZzI7IGtldCBxdWEg'
'ZHVvaSBsYSBORU4gRE8uIikKZWxpZiBsYV9oYXVfZHVlOgogICAgdGhlX2hlID0gImcyIjsgaW5uKGYiICBIRUFEID0ge2hlYWRb'
'OjhdfSAtPiBoYXUgZHVlIGN1YSBnMSAoe1NIQV9HMVs6OF19KTogdW5nIHZpZW4gZzIuIikKZWxzZToKICAgIHRoZV9oZSA9ICI/'
'IjsgbG9pLmFwcGVuZChmIkhFQUQ9e2hlYWRbOjhdfSBLSE9ORyBwaGFpIGcxIHZhIEtIT05HIHBoYWkgaGF1IGR1ZSBjdWEge1NI'
'QV9HMVs6OF19IOKAlCByZWJhc2U/IG5oYW0gbmhhbmg/IikKZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCgppZiBsb2k6CiAgICBpbm4o'
'IiIpOyBpbm4oIktIT05HIERPIERVT0M6IG5lbiBkbyBzYWksIEtIT05HIGluIGtldCBsdWFuIG5hby4iKQogICAgZm9yIHggaW4g'
'bG9pOiBpbm4oIiAgLSIsIHgpCiAgICBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDEuIGtpY2ggdGh1b2MgKE43JyBj'
'dWEgc3BlYyByMykgLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjEuIEtJQ0ggVEhVT0Mg4oCU'
'IHRyYW4gc3BlYyByMzogPD0gMiB0ZXAgdmEgPD0gNDAwIGRvbmcgdGhlbSIpCnJjLCBucywgZXIgPSBnaXQoZ29jLCAiZGlmZiIs'
'ICItLW51bXN0YXQiLCBTSEFfQkFTRSwgaGVhZCkKaWYgcmM6CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImdpdCBk'
'aWZmIGxvaToge2VyWzo4MF19IikKZWxzZToKICAgIGhhbmcgPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBucy5zcGxpdGxpbmVz'
'KCkgaWYgbC5zdHJpcCgpXQogICAgdGhlbSA9IHN1bShpbnQoaFswXSkgZm9yIGggaW4gaGFuZyBpZiBoWzBdLmlzZGlnaXQoKSkK'
'ICAgIHhvYSAgPSBzdW0oaW50KGhbMV0pIGZvciBoIGluIGhhbmcgaWYgaFsxXS5pc2RpZ2l0KCkpCiAgICBnaGkoInNvX3RlcCIs'
'IGxlbihoYW5nKSk7IGdoaSgiZG9uZ190aGVtIiwgdGhlbSk7IGdoaSgiZG9uZ194b2EiLCB4b2EpCiAgICBmb3IgaCBpbiBoYW5n'
'OiBpbm4oZiIgICAge2hbMl06MzR9ICt7aFswXTo8NX0gLXtoWzFdfSIpCiAgICBpbm4oZiIgICAgVE9ORzoge2xlbihoYW5nKX0g'
'dGVwLCAre3RoZW19LCAte3hvYX0gICAodHJhbjoge1RSQU5fVEVQfSB0ZXAgLyB7VFJBTl9ET05HfSBkb25nIHRoZW0pIikKICAg'
'IGtldCgiTjcnIGtpY2ggdGh1b2MiLCBEQVQgaWYgKGxlbihoYW5nKSA8PSBUUkFOX1RFUCBhbmQgdGhlbSA8PSBUUkFOX0RPTkcp'
'IGVsc2UgVFJVT1QsCiAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IikKCiMgLS0tLS0tLS0tLS0tLS0tLSAyLiBi'
'byB0ZXN0IGRheSBkdSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMi4gQk8gVEVTVCBEQVkg'
'RFUgKDEwLTQwIHBodXQpIikKcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBnb2MpCmdo'
'aSgicmNfc3VpdGUiLCByY19uKQptID0gUlhfVE9ORy5zZWFyY2gob3V0X24pCmlubigiICByYyA9IiwgcmNfbiwgInwiLCBtLmdy'
'b3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQpIikKaWYgbToKICAgIGdoaSgiZGF0IiwgaW50'
'KG0uZ3JvdXAoMSkpKTsgZ2hpKCJ0cmVuIiwgaW50KG0uZ3JvdXAoMikpKTsgZ2hpKCJib19xdWFfc28iLCBpbnQobS5ncm91cCg0'
'KSkpCmRvX2hldCwgZ2MsIHRpbiA9IGRvY19kbyhvdXRfbikKZ2hpKCJzb19jYV9kbyIsIGxlbihkb19oZXQpKTsgZ2hpKCJsaWV0'
'X2tlX2RheV9kdSIsIHRpbikKZm9yIGcgaW4gZ2M6IGlubigiICAgKiIsIGcpCmlubigiIik7IGlubihmIiAgPT09IHtsZW4oZG9f'
'aGV0KX0gQ0EgRE8gPT09IikKZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgIGlubihmIiAgIHt0LnNwbGl0'
'KCdfJylbMF06N30ge3R9Iik7IGlubihmIiAgICAgICAgICAge2RvX2hldFt0XVs6MTUwXX0iKQpnaGkoImRvX2x5X2RvIiwge3Q6'
'IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQpicSA9IHNvcnRlZCh7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmlu'
'ZGFsbChvdXRfbil9LCBrZXk9c29fY2EpOyBnaGkoImNhX2JvX3F1YSIsIGJxKQppbm4oIiIpOyBpbm4oZiIgIEJPIFFVQSAoe2xl'
'bihicSl9KToge1t4LnNwbGl0KCdfJylbMF0gZm9yIHggaW4gYnFdfSIpCgppbm4oIiIpOyBpbm4oIiAgTjEtTjQgKHQxNjUtdDE2'
'OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBuYXkgbGEgY2hpIGJhbyBob2kgcXV5OiIpCmI0ID0ge3Q6IG1hdV9jYShv'
'dXRfbiwgdCkgZm9yIHQgaW4gQ0FNT0l9OyBnaGkoImNhX21vaSIsIGI0KQpmb3IgdCBpbiBDQU1PSTogaW5uKGYiICAgICB7dH06'
'IHtiNFt0XX0iKQprZXQoIk4xLU40ICh0MTY1LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJRVUEiIGZvciB2IGluIGI0LnZhbHVl'
'cygpKQogICAgZWxzZSAoS0REIGlmIGFueSh2IGlzIE5vbmUgZm9yIHYgaW4gYjQudmFsdWVzKCkpIGVsc2UgVFJVT1QpLCBzdHIo'
'YjQpKQoKaW5uKCIiKTsgaW5uKCIgIDE1IGNhIHR1bmcgZG8gdHJlbiBDSToiKQpiMTUgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBm'
'b3IgdCBpbiBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQppbm4oIiAgICAiICsgIiAgIi5qb2luKGYie3R9OntiMTVbdF19IiBmb3Ig'
'dCBpbiBDQTE1KSkKCiMgdDEzNiDigJQgTjEyIGRvIEdJQU4gVElFUCBxdWEga2V0IHF1YSBjYQp0MTM2X3RlbiA9IG5leHQoKHQg'
'Zm9yIHQgaW4gZG9faGV0IGlmIHQuc3RhcnRzd2l0aCgidDEzNiIpKSwgTm9uZSkKaWYgYjE1LmdldCgidDEzNiIpID09ICJRVUEi'
'OgogICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgREFULCAidDEzNiBRVUEiKQplbGlmIGIxNS5nZXQoInQxMzYi'
'KSBpcyBOb25lOgogICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgS0RELCAia2hvbmcgdGhheSB0MTM2IHRyb25n'
'IGxvZyIpCmVsc2U6CiAgICBseSA9IGRvX2hldC5nZXQodDEzNl90ZW4sICIiKQogICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBx'
'dWEgY2EpIiwgVFJVT1QsIGYiRE86IHtseVs6OTBdfSIpCgojIC0tLS0tLS0tLS0tLS0tLS0gMy4gcHJvYmUgVEhBTkcgdmFvIGhh'
'bSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMy4gUFJPQkUgVEhBTkcg4oCUIGdvaSBfZ2l0'
'X3dpbmRvd3Mgdm9pIHRoYW0gc28gdGllbSIpCnNwZWMgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigi'
'bHA1NDEiLCBzdHIodGVwKSkKbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMpOyBzcGVjLmxvYWRlci5l'
'eGVjX21vZHVsZShscCkKc2lnID0gaW5zcGVjdC5zaWduYXR1cmUobHAuX2dpdF93aW5kb3dzKQpnaGkoInRoYW1fc29fX2dpdF93'
'aW5kb3dzIiwgbGlzdChzaWcucGFyYW1ldGVycykpCmlubigiICB0aGFtIHNvIGN1YSBfZ2l0X3dpbmRvd3M6IiwgbGlzdChzaWcu'
'cGFyYW1ldGVycykpCgpkZWYgZ29pKCoqa3cpOgogICAgIiIiR29pIF9naXRfd2luZG93cywgQkFUIHN0ZGVyciBkZSBtb3QgZG9u'
'ZyBjaGFuIGRvYW4ga2hvbmcgZ2lldCBsdW90IGRvLiIiIgogICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgIHdpdGggY29udGV4dGxp'
'Yi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgciA9IGxwLl9naXRfd2luZG93cygqKmt3KQogICAgcmV0dXJuIHIsIGUuZ2V0'
'dmFsdWUoKQoKIyAtLS0gZG9pIGNodW5nIHJpZzogcGhhaSB0cmEgbG9pIGR1bmcgbW90IGNhIHRhIEJJRVQgVFJVT0MgZGFwIGFu'
'IC0tLQp3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICBuZ29haSA9IFBhdGgodCkvIm5nb2FpIjsg'
'bmdvYWkubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIo'
'KQogICAgKG5nb2FpLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMSwgXyA9IGdvaShw'
'YXRoPXN0cihuZ29haSksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAoY3cvImdpdC5leGUiKS53cml0'
'ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIyLCBfID0gZ29pKHBhdGg9c3RyKGN3KSwgcHJvZ3JhbV9maWxlcz1z'
'dHIocGYpLCBjd2Q9c3RyKGN3KSkKcmlnX29rID0gYm9vbChyMSkgYW5kIHIyIGlzIE5vbmUKZ2hpKCJyaWdfZG9pX2NodW5nIiwg'
'cmlnX29rKQprZXQoIlJJRyBkb2kgY2h1bmcgKGJpZXQgdHJ1b2MgZGFwIGFuKSIsIERBVCBpZiByaWdfb2sgZWxzZSBLREQsCiAg'
'ICBmIm5nb2FpLWN3ZC0+eydOSEFOJyBpZiByMSBlbHNlICdOb25lJ30gfCB0cm9uZy1jd2QtPnsnTkhBTicgaWYgcjIgZWxzZSAn'
'Tm9uZSd9IikKaWYgbm90IHJpZ19vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogcmlnIHNhaSwgbW9pIGNob3Qg'
'ZHVvaSBzZSB2byBuZ2hpYS4iKTsgc3lzLmV4aXQoMykKCmZvciB0ZW4sICh0dCwgY3QsIGRsKSBpbiBbKHQsIGYoZ29pLCBzaWcs'
'IHRlcHQpKSBmb3IgdCwgZiBpbiBQUk9CRV06CiAgICBnaGkoInByb2JlXyIgKyB0ZW4uc3BsaXQoKVswXS5sb3dlcigpLCBkbCkK'
'ICAgIGlmIGlzaW5zdGFuY2UoZGwsIGRpY3QpOgogICAgICAgIGZvciBrLCB2IGluIGRsLml0ZW1zKCk6IGlubihmIiAgICB7azoz'
'NH06IHt2fSIpCiAgICBrZXQodGVuLCB0dCwgY3QpCgojIC0tLS0tLS0tLS0tLS0tLS0gNC4gTjcgZG90IGJpZW4gdHJlbiBCQU4g'
'U0FPIFRBTSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiNC4gTjcg4oCUIGRvdCBiaWVuIHRy'
'ZW4gQkFOIFNBTyBUQU0gKGNheSB0aGF0IEtIT05HIGJpIGR1bmcgdG9pKSIpCnRydW9jID0gdGVwLnJlYWRfdGV4dChlbmNvZGlu'
'Zz0idXRmLTgiKS5jb3VudChNQVVfV0lOKQpnaGkoIm43X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIgIHNvIGRvbmcga2hvcCB7TUFV'
'X1dJTiFyfTogVFJVT0MgPSB7dHJ1b2N9IFttb25nIDFdIikKaWYgdHJ1b2MgIT0gMToKICAgIGtldCgiTjcgZG90IGJpZW4gbmhh'
'bmggV2luZG93cyIsIEtERCwgZiJtYXUgeHVhdCBoaWVuIHt0cnVvY30gbGFuLCBraG9uZyBwaGFpIDEiKQplbHNlOgogICAgd2l0'
'aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0bXA6CiAgICAgICAgc2FvID0gUGF0aCh0bXApLyJjYXkiCiAgICAg'
'ICAgc2h1dGlsLmNvcHl0cmVlKGdvYywgc2FvLCBpZ25vcmU9c2h1dGlsLmlnbm9yZV9wYXR0ZXJucygiLmdpdCIsICJfX3B5Y2Fj'
'aGVfXyIsICIqLnB5YyIpKQogICAgICAgIGYyID0gc2FvLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IgogICAgICAgIGYyLndyaXRl'
'X3RleHQoZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJlcGxhY2UoTUFVX1dJTiwgImlmIEZhbHNlOiIpLCBlbmNvZGlu'
'Zz0idXRmLTgiKQogICAgICAgIHNhdSA9IGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKTsgZ2hp'
'KCJuN19zYXUiLCBzYXUpCiAgICAgICAgaW5uKGYiICBTQVUgKGRhIGRvdCBiaWVuKSA9IHtzYXV9IFttb25nIDBdIikKICAgICAg'
'ICBpZiBzYXUgIT0gMDoKICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCAiZG90IGJpZW4g'
'S0hPTkcgYXAgZHVvYyIpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgcmNfbSwgb3V0X20gPSBjaGF5KFsib3BzL2xlYXNlX3B1'
'Ymxpc2hfdGVzdC5weSJdLCBzYW8pCiAgICAgICAgICAgIG0xNjUgPSBtYXVfY2Eob3V0X20sICJ0MTY1Iik7IGRtLCBfLCBfID0g'
'ZG9jX2RvKG91dF9tKQogICAgICAgICAgICB0ZW4xNjUgPSBuZXh0KCh0IGZvciB0IGluIGRtIGlmIHQuc3RhcnRzd2l0aCgidDE2'
'NSIpKSwgTm9uZSkKICAgICAgICAgICAgbHkgPSAoZG0uZ2V0KHRlbjE2NSkgb3IgIiIpCiAgICAgICAgICAgIGdoaSgibjdfdDE2'
'NSIsIG0xNjUpOyBnaGkoIm43X2x5X2RvIiwgbHlbOjIwMF0pCiAgICAgICAgICAgIGlubihmIiAgdDE2NSBzYXUgZG90IGJpZW46'
'IHttMTY1fSB8IHtseVs6MTEwXX0iKQogICAgICAgICAgICBkdW5nX2x5X2RvID0gIlBBVEggdCIgaW4gbHkgb3IgIi91c3IvYmlu'
'IiBpbiBseQogICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBEQVQgaWYgKG0xNjUgPT0gIkRPIiBh'
'bmQgZHVuZ19seV9kbykgZWxzZQogICAgICAgICAgICAgICAgKFRSVU9UIGlmIG0xNjUgPT0gIkRPIiBlbHNlIEtERCksCiAgICAg'
'ICAgICAgICAgICAiZ2lldCBkdW5nIGx5IGRvIiBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKQogICAgICAgICAgICAg'
'ICAgZWxzZSAoIkRPIG5odW5nIEtIT05HIGR1bmcgbHkgZG8gLT4gdGluIGR1bmcgZ2lhIiBpZiBtMTY1ID09ICJETyIgZWxzZSAi'
'a2hvbmcgZG9jIGR1b2MgdDE2NSIpKQoKIyAtLS0tLS0tLS0tLS0tLS0tIEtFVCBMVUFOIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIi'
'KTsgaW5uKCI9IiAqIDc4KQppbm4oZiJUSEUgSEUgRE8gRFVPQzoge3RoZV9oZX0gICBIRUFEPXtoZWFkWzoxMl19IikKaWYgdGhl'
'X2hlID09ICJnMSI6CiAgICBpbm4oIkxVVSBZOiBkYXkgbGEgTkVOIERPIChnMSksIEtIT05HIHBoYWkgbmdoaWVtIHRodSBnMi4g'
'Q2FjIGNob3QgTjgtTjEyIGR1b2kgZGF5IikKICAgIGlubigiICAgICAgIFRSVU9UIGxhIERVTkcgTkhVIE1PTkcg4oCUIGNodW5n'
'IGxhIG5odW5nIGxvIGcyIHNpbmggcmEgZGUgdsOhLiIpCmlubigiLSIgKiA3OCkKZm9yIHRlbiwgdHQsIGN0IGluIGNob3Q6CiAg'
'ICBpbm4oZiIgIHt0dDoxNH0ge3Rlbn0iICsgKGYiICAge2N0fSIgaWYgY3QgZWxzZSAiIikpCm5fa2RkID0gc3VtKDEgZm9yIF8s'
'IHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKbl90cnVvdCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVP'
'VCkKaW5uKCItIiAqIDc4KQppbm4oZiIgIERBVCB7c3VtKDEgZm9yIF8sdCxfIGluIGNob3QgaWYgdD09REFUKX0gfCBUUlVPVCB7'
'bl90cnVvdH0gfCBLSE9ORyBETyBEVU9DIHtuX2tkZH0iKQppbm4oZiIgIFRvbmcgY2EgZG86IHtzby5nZXQoJ3NvX2NhX2RvJyl9'
'IHwgZGFuaCBzYWNoIGRheSBkdTogeydDTycgaWYgc28uZ2V0KCdsaWV0X2tlX2RheV9kdScpIGVsc2UgJ0tIT05HIERPIERVT0Mn'
'fSIpCmlubihmIiAgQWRtaW5pc3RyYXRvcjoge3NvLmdldCgncXV5ZW5fYWRtaW4nKX0gfCBzeW1saW5rOiB7c28uZ2V0KCdzeW1s'
'aW5rX2R1b2MnKX0iKQppbm4oIiIpOyBpbm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kgSlNPTiBOQVkgVkUgQ0hPIFJFVklFV0VSIC0t'
'LSIpCmdoaSgiY2hvdCIsIFt7InRlbiI6IGEsICJ0cmFuZ190aGFpIjogYiwgImNoaV90aWV0IjogY30gZm9yIGEsIGIsIGMgaW4g'
'Y2hvdF0pCmlubihqc29uLmR1bXBzKHNvLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0xLCBkZWZhdWx0PXN0cikpCiMgcmM6'
'IDAgPSBtb2kgY2hvdCBEQVQgfCAxID0gY28gY2hvdCBUUlVPVCB8IDMgPSBjbyBjaG90IEtIT05HIERPIERVT0MgKHV1IHRpZW4g'
'YmFvIGRvbmcpCnN5cy5leGl0KDMgaWYgbl9rZGQgZWxzZSAoMSBpZiBuX3RydW90IGVsc2UgMCkpCg=='
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
