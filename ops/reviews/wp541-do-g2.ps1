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
    [string]$Nhanh   = 'fix_issue_541',   # nhanh mang ban va can do
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
$ShaBoDo    = 'b2d7771b2d8db8732082a15ffd72bac71563c04680bf869bd8efe19dace34161'      # SHA-256 cua bo do Python nhung ben duoi

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
'ICAgICAgICAgICMgTjcnIGN1YSBzcGVjIHIzCk1BVV9XSU4gID0gJ2lmIG5lbl90aHVjID09ICJ3aW5kb3dzIjonCiMgQ2Egbmdv'
'YWkgcGhhbSB2aSByMyDCp25nb2FpX3BoYW1fdmkg4oCUIGRvIENISU5IIFNQRUMga2hhaSwga2hvbmcgcGhhaSBibyBkbyB0dSBx'
'dXlldC4KIyBEbyBsYSBEQU5IIFNBQ0ggQ0hPIFBIRVA6IGNhIGRvIG5hbyBLSE9ORyBuYW0gdHJvbmcgZGF5IHZhIEtIT05HIHBo'
'YWkgInRoaWV1IGNvbmcgY3UiCiMgdGhpIGxhIFRSVU9ULiBEYW5oIHNhY2ggY2FtIHRoaSBiYW8gZ2lvIGN1bmcgdGhpZXU7IGRh'
'bmggc2FjaCBjaG8gcGhlcCB0aGkgYmlldCB0cnVvYy4KTkdPQUlfUEhBTV9WSSA9IHNldCgidDEzMSB0MTMyIHQxNTAgdDEyNSB0'
'MzUgdDM2IHQzNyB0MzggdDM5IHQ0MCIuc3BsaXQoKSkKIyBDYSBjdWEgQ0hJTkggcGFja2V0IG5heS4gTW90IGNhIG8gZGF5IG1h'
'IERPIHRoaSBraG9uZyBiYW8gZ2lvIGR1b2MgYm8gcXVhLgpDQV9QQUNLRVQgPSBzZXQoInQxNjUgdDE2NiB0MTY3IHQxNjggdDE2'
'OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpKQpDQTE1ICA9ICJ0MTI5IHQxMzAgdDEzMSB0MTMyIHQxMzMgdDEzNiB0MTM4'
'IHQxMzkgdDE0NCB0MTQ1IHQxNDYgdDE0NyB0MTQ5IHQxNTAgdDE1MSIuc3BsaXQoKQpDQU1PSSA9ICJ0MTY1IHQxNjYgdDE2NyB0'
'MTY4Ii5zcGxpdCgpCgpEQVQsIFRSVU9ULCBLREQgPSAiREFUIiwgIlRSVU9UIiwgIktIT05HIERPIERVT0MiCnNvLCBjaG90ID0g'
'e30sIFtdCmRlZiBnaGkoaywgdik6IHNvW2tdID0gdjsgcmV0dXJuIHYKZGVmIGtldCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0'
'PSIiKToKICAgIGNob3QuYXBwZW5kKCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0KSkKICAgIGlubihmIiAgW3t0cmFuZ190aGFp'
'OjE0fV0ge3Rlbn0iICsgKGYiICAge2NoaV90aWV0fSIgaWYgY2hpX3RpZXQgZWxzZSAiIikpCiAgICByZXR1cm4gdHJhbmdfdGhh'
'aQoKIyAtLS0tLS0tLS0tLS0tLS0tIGRvYyBsb2cgY3VhIGJvIHRlc3QgKGJhbiAzLCBkYSBkbyB0cmVuIGxvZyBUSEFUKSAtLS0t'
'LS0tLS0tLS0tLS0tClJYX0RPX0NITyAgPSByZS5jb21waWxlKHIiKD9tKV4hISEgZG8gKFxTKykgKC4qKSQiKQpSWF9ET19DVU9J'
'ID0gcmUuY29tcGlsZShyIig/bSleIHsyfShcU3sxLDR9KSB7Mn0oXFMrKTogKC4qKSQiKQpSWF9CT19RVUEgID0gcmUuY29tcGls'
'ZShyIig/bSleIHsyfVxTezEsNn0gUVVBIChcUyspOiAoLiopJCIpClJYX1RPTkcgICAgPSByZS5jb21waWxlKHIibGVhc2VfcHVi'
'bGlzaDogKFxkKykvKFxkKylcYlteXG5dKj89KFxkKyksW15cbl0qPz0oXGQrKSIpCgpkZWYgc29fY2EodCk6CiAgICBtID0gcmUu'
'bWF0Y2gociJ0KFxkKykiLCB0KTsgcmV0dXJuIChpbnQobS5ncm91cCgxKSkgaWYgbSBlbHNlIDEwKio2LCB0KQoKZGVmIGRvY19k'
'byhvdXQpOgogICAgdGFpX2NobyA9IHt0OiBsLnN0cmlwKCkgZm9yIHQsIGwgaW4gUlhfRE9fQ0hPLmZpbmRhbGwob3V0KX0KICAg'
'IGJvID0ge3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0KX0KICAgIGN1b2kgPSB7dDogbC5zdHJpcCgpIGZvciBf'
'LCB0LCBsIGluIFJYX0RPX0NVT0kuZmluZGFsbChvdXQpIGlmIHQgbm90IGluIGJvfQogICAgaG9wID0gZGljdChjdW9pKTsgaG9w'
'LnVwZGF0ZSh0YWlfY2hvKQogICAgZ2MsIHRpbiA9IFtdLCBUcnVlCiAgICBpZiBzZXQodGFpX2NobykgIT0gc2V0KGN1b2kpOgog'
'ICAgICAgIGdjLmFwcGVuZChmImhhaSBuZ3VvbiBMRUNIOiBjaGktdGFpLWNobz17c29ydGVkKHNldCh0YWlfY2hvKS1zZXQoY3Vv'
'aSkpfSBjaGktY3VvaT17c29ydGVkKHNldChjdW9pKS1zZXQodGFpX2NobykpfSIpCiAgICAgICAgdGluID0gRmFsc2UKICAgIG0g'
'PSBSWF9UT05HLnNlYXJjaChvdXQpCiAgICBpZiBub3QgbToKICAgICAgICBnYy5hcHBlbmQoIktIT05HIGRvYyBkdW9jIGRvbmcg'
'dG9uZyBrZXQiKTsgdGluID0gRmFsc2UKICAgIGVsc2U6CiAgICAgICAgZGF0LCB0cmVuID0gaW50KG0uZ3JvdXAoMSkpLCBpbnQo'
'bS5ncm91cCgyKSkKICAgICAgICBnYy5hcHBlbmQoZiJzbyBob2M6IHt0cmVufS17ZGF0fT17dHJlbi1kYXR9IGRvOyBkb2MgZHVv'
'YyB7bGVuKGhvcCl9IikKICAgICAgICBpZiB0cmVuIC0gZGF0ICE9IGxlbihob3ApOgogICAgICAgICAgICBnYy5hcHBlbmQoZiJM'
'RUNIIFNPIEhPQzogdGhpZXUge3RyZW4tZGF0LWxlbihob3ApfSBjYSIpOyB0aW4gPSBGYWxzZQogICAgcmV0dXJuIGhvcCwgZ2Ms'
'IHRpbgoKX01BVSA9ICgiISEhIGRvIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU4gYVxuIgogICAgICAgICIhISEgZG8gdDE1'
'MF94IFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAgICAgIiAgQuG7jiBRVUEgdDEzMV95OiBuZW4gZml4'
'dHVyZVxuIgogICAgICAgICIgIMSQ4buOICB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOOiBhXG4iCiAgICAgICAgIiAgxJDh'
'u44gIHQxNTBfeDogV2luRXJyb3IgMTMxNCByZXF1aXJlZCBwcml2aWxlZ2VcbiIKICAgICAgICAibGVhc2VfcHVibGlzaDogMS8z'
'IMSR4bqhdDsgxJHDoyBjaOG6oXk9MywgYuG7jyBxdWE9MVxuIikKCmRlZiBjaGF5KGFyZ3YsIGN3ZCwgcGh1dD02MCk6CiAgICBt'
'dCA9IGRpY3Qob3MuZW52aXJvbiwgUFlUSE9OVVRGOD0iMSIsIFBZVEhPTklPRU5DT0RJTkc9InV0Zi04IiwKICAgICAgICAgICAg'
'ICBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0iMSIsIFBZVEhPTlVOQlVGRkVSRUQ9IjEiKQogICAgcCA9IHN1YnByb2Nlc3MucnVu'
'KFtzeXMuZXhlY3V0YWJsZV0gKyBhcmd2LCBjd2Q9c3RyKGN3ZCksIGNhcHR1cmVfb3V0cHV0PVRydWUsCiAgICAgICAgICAgICAg'
'ICAgICAgICAgdGV4dD1UcnVlLCBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjAsIGVu'
'dj1tdCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1'
'X2NhKG91dCwgdCk6CiAgICBtID0gcmUuc2VhcmNoKHIiKD9tKV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSBbMC05Ll0r'
'cyAoXHcrKVxzKiQiLCBvdXQpCiAgICByZXR1cm4gbS5ncm91cCgyKSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdpdChnb2MsICphLCBw'
'aHV0PTUpOgogICAgcCA9IHN1YnByb2Nlc3MucnVuKFsiZ2l0IiwgIi1DIiwgc3RyKGdvYyksICphXSwgY2FwdHVyZV9vdXRwdXQ9'
'VHJ1ZSwgdGV4dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIs'
'IHRpbWVvdXQ9cGh1dCo2MCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikuc3RyaXAoKSwgKHAuc3Rk'
'ZXJyIG9yICIiKS5zdHJpcCgpCgoKIyA9PT09PT09PT09PT09PT09PSBOQU0gUFJPQkUsIHZpZXQgdGhhbmggSEFNIFRIVUFOIGRl'
'IFRVIEtJRU0gZHVvYyA9PT09PT09PT09PT09PT09PQojIE1vaSBoYW0gdHJhICh0cmFuZ190aGFpLCBjaGlfdGlldCwgZHVfbGll'
'dSkuIEtIT05HIGluLCBLSE9ORyB0aG9hdCDigJQgbmhvIHZheSBjaHVuZwojIGNoYXkgZHVvYyB0cmVuIG5lbiBCQVQgS1ksIHZh'
'IGAtLXR1LWtpZW0tcHJvYmVgIGdvaSB0aGFuZyBjaHVuZyBkZSBraWVtIGNoaW5oIGJvIGRvLgoKZGVmIF9zYW4odCk6CiAgICBk'
'ID0gUGF0aCh0KS8iZCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBm'
'IjsgcGYubWtkaXIoKQogICAgcmV0dXJuIGQsIGN3LCBwZgoKZGVmIGRvX244KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkJ1b2Mg'
'MSAoQ09OR19DVV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0LmV4ZS4gRG9pIGNodW5nIGR1b25nOiBnaXQuZXhlIFZBTiBwaGFpIG5o'
'YW4uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwg'
'Y3csIHBmID0gX3Nhbih0KQogICAgICAgIGZvciB0ZW4gaW4gKCJnaXQuZXhlIiwgImdpdC5iYXQiLCAiZ2l0LmNtZCIsICJnaXQu'
'cHkiLCAia2hvbmctcGhhaS1naXQudHh0Iik6CiAgICAgICAgICAgIGYgPSBkL3RlbjsgZi53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rp'
'bmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyA9IGdvaShjb25nX2N1X2dpdD1zdHIoZiksIHBhdGg9IiIsIHByb2dyYW1fZmls'
'ZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIGtxW2YiQ09OR19DVV9HSVQ9e3Rlbn0iXSA9ICJOSEFOIiBpZiBy'
'IGVsc2UgIlRVIENIT0kiCiAgICBsb3QgPSBbayBmb3IgaywgdiBpbiBrcS5pdGVtcygpIGlmIHYgPT0gIk5IQU4iIGFuZCBub3Qg'
'ay5lbmRzd2l0aCgiZ2l0LmV4ZSIpXQogICAgaWYga3EuZ2V0KCJDT05HX0NVX0dJVD1naXQuZXhlIikgIT0gIk5IQU4iOgogICAg'
'ICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogZ2l0LmV4ZSBob3AgbGUgbWEgYmkgdHUgY2hvaSIsIGtxCiAg'
'ICByZXR1cm4gKERBVCBpZiBub3QgbG90IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IGxvdCBlbHNlIGYiY29uIG5oYW46IHtsb3R9'
'IiksIGtxCgpkZWYgZG9fbjkoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiTXVjIFBBVEggYm9jIG5oYXkga2VwIHBoYWkgTkhBTjsg'
'bXVjIHJvbmcgLyB0b2FuIGtob2FuZyB0cmFuZyBwaGFpIGJvIHF1YSwga2hvbmcgbmVtLiIiIgogICAga3EgPSB7fQogICAgd2l0'
'aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBkLm1rZGly'
'KCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgICAgICAo'
'ZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGZvciBuaGFuLCBtdWMgaW4gKCgi'
'a2hvbmcgbmhheSIsIHN0cihkKSksICgiY28gbmhheSBrZXAiLCBmJyJ7ZH0iJyksCiAgICAgICAgICAgICAgICAgICAgICAgICAg'
'KCJyb25nIiwgIiIpLCAoImNoaSBraG9hbmcgdHJhbmciLCAiICAgIikpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAg'
'ICByLCBfID0gZ29pKHBhdGg9bXVjLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICAgICAg'
'a3FbZiJQQVRIIHtuaGFufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBh'
'cyBlOgogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gZiJORU0ge3R5cGUoZSkuX19uYW1lX199IgogICAgaWYg'
'a3EuZ2V0KCJQQVRIIGtob25nIG5oYXkiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBo'
'b25nOiBtdWMgUEFUSCB0aHVvbmcgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgb2sgPSAoa3EuZ2V0KCJQQVRIIGNv'
'IG5oYXkga2VwIikgPT0gIk5IQU4iCiAgICAgICAgICBhbmQga3EuZ2V0KCJQQVRIIHJvbmciKSA9PSAiTm9uZSIgYW5kIGtxLmdl'
'dCgiUEFUSCBjaGkga2hvYW5nIHRyYW5nIikgPT0gIk5vbmUiKQogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgi'
'IiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKZGVmIGRvX24xMChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJNb3QgZGF1ICc7'
'JyB0cm9uZyBURU4gdGh1IG11YyBraG9uZyBkdW9jIGxhbSBtYXQgbXVjIGdpdC5leGUgaG9wIGxlIG8gbXVjIGtpYS4iIiIKICAg'
'IGNvX3NlcCA9IGFueSgoImNhY2giIGluIGspIG9yICgic2VwIiBpbiBrLmxvd2VyKCkpIGZvciBrIGluIHNpZy5wYXJhbWV0ZXJz'
'KQogICAgaWYgb3MucGF0aHNlcCA9PSAiOyIgYW5kIG5vdCBjb19zZXA6CiAgICAgICAgcmV0dXJuIChLREQsICJ0cmVuIFdpbmRv'
'd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgdmEgaGFtIGtob25nIG5oYW4gdGhhbSBzbyBkYXUgcGhhbiBjYWNoICIKICAgICAgICAg'
'ICAgICAgICAgICAgIi0+IGtob25nIHRhY2ggZHVvYyBoYWkgZ2lhIHRodXlldCIsIHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAs'
'ICJjbyB0aGFtIHNvIHNlcCI6IGNvX3NlcH0pCiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAg'
'ICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUiOyBsYS5ta2RpcigpCiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAg'
'IChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgciwgXyA9IGdvaShwYXRoPXN0'
'cihsYSkgKyBvcy5wYXRoc2VwICsgc3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgIHIw'
'LCBfID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKSAgICAgIyBkb2kgY2h1bmcg'
'ZHVvbmcKICAgIGtxID0geyJjbyBtdWMgY2h1YSAnOyciOiAiTkhBTiIgaWYgciBlbHNlICJOb25lIiwgImRvaSBjaHVuZyAoa2hv'
'bmcgY28gJzsnKSI6ICJOSEFOIiBpZiByMCBlbHNlICJOb25lIn0KICAgIGlmIG5vdCByMDoKICAgICAgICByZXR1cm4gS0RELCAi'
'ZG9pIGNodW5nIGR1b25nIGhvbmciLCBrcQogICAgcmV0dXJuIChEQVQgaWYgciBlbHNlIFRSVU9UKSwgKCIiIGlmIHIgZWxzZSAi'
'bXVjIGdpdC5leGUgaG9wIGxlIGJpIE1BVCIpLCBrcQoKZGVmIGRvX24xMShnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJUcnV5ZW4g'
'Y2hhbl9kb2FuID0+IHRodSBkdW9jIHRob25nIGJhbyBWQSBzdGRlcnIgSU0uIEtob25nIHRydXllbiA9PiBzdGRlcnIgVkFOIGNv'
'LiIiIgogICAgaWYgImNoYW5fZG9hbiIgbm90IGluIHNpZy5wYXJhbWV0ZXJzOgogICAgICAgIHJldHVybiBLREQsICJfZ2l0X3dp'
'bmRvd3Mga2hvbmcgbmhhbiB0aGFtIHNvIGNoYW5fZG9hbiIsIHsidGhhbSBzbyI6IGxpc3Qoc2lnLnBhcmFtZXRlcnMpfQogICAg'
'd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAg'
'ICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGNkID0gW10KICAgICAgICBf'
'LCBlX2NvID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpLCBjaGFuX2RvYW49Y2Qp'
'CiAgICAgICAgXywgZV9raCA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAg'
'IGtxID0geyJjaGFuX2RvYW4gdGh1IGR1b2MgKG11YykiOiBsZW4oY2QpLAogICAgICAgICAgInN0ZGVyciBraGkgQ08gY2hhbl9k'
'b2FuIChieXRlKSI6IGxlbihlX2NvLmVuY29kZSgpKSwKICAgICAgICAgICJzdGRlcnIga2hpIEtIT05HIHRydXllbiAoYnl0ZSki'
'OiBsZW4oZV9raC5lbmNvZGUoKSl9CiAgICBpZiBsZW4oY2QpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA9PSAwOgogICAg'
'ICAgIHJldHVybiBLREQsICJuaGFuaCAlUHJvZ3JhbUZpbGVzJSBraG9uZyBwaGFuIGdpYWkgS0hPTkcgYmF5IHJhIGNoYW4gZG9h'
'biBuYW8gLT4gY2h1YSBkbyBkdW9jIiwga3EKICAgIG9rID0gbGVuKGNkKSA+IDAgYW5kIGxlbihlX2NvLmVuY29kZSgpKSA9PSAw'
'IGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPiAwCiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVs'
'c2UgInhlbSBiYW5nIiksIGtxCgpkZWYgZG9fbjEyKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkhhbmcgc2VudGluZWwgZ2l0X3Bh'
'dGggdHJvbmcgZml4dHVyZSBwaGFpIHR1eWV0IGRvaSB0cmVuIENBIEhBSSBuZW4uIiIiCiAgICBuZCA9IHRlcHQucmVhZF90ZXh0'
'KGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIpCiAgICBoYW5nID0gc29ydGVkKHNldChyZS5maW5kYWxsKHInZ2l0'
'X3BhdGhccyo9XHMqIihbXiJdKykiJywgbmQpKSkKICAgIHhhdSA9IFtoIGZvciBoIGluIGhhbmcgaWYgbm90IChQdXJlUG9zaXhQ'
'YXRoKGgpLmlzX2Fic29sdXRlKCkgYW5kIFB1cmVXaW5kb3dzUGF0aChoKS5pc19hYnNvbHV0ZSgpKV0KICAgIGtxID0geyJoYW5n'
'IGdpdF9wYXRoIHRpbSB0aGF5IjogaGFuZywgImNoaSB0dXlldCBkb2kgTU9UIG5lbiI6IHhhdX0KICAgIGlmIG5vdCBoYW5nOgog'
'ICAgICAgIHJldHVybiBLREQsICJraG9uZyB0aW0gdGhheSBoYW5nIGdpdF9wYXRoIG5hbyB0cm9uZyBmaXh0dXJlIC0+IG1hdSBk'
'b2MgY28gdGhlIGRhIGRvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgeGF1IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IHhh'
'dSBlbHNlIGYiY2hpLW1vdC1uZW46IHt4YXV9IiksIGtxCgpQUk9CRSA9IFsoIk44IGJ1b2MgMSBjaGkgbmhhbiBnaXQuZXhlIiwg'
'ZG9fbjgpLAogICAgICAgICAoIk45IGJvYyBuaGF5IGtlcCBvIG11YyBQQVRIIiwgZG9fbjkpLAogICAgICAgICAoIk4xMCBkYXUg'
'JzsnIHRyb25nIHRlbiB0aHUgbXVjIiwgZG9fbjEwKSwKICAgICAgICAgKCJOMTEgY2hhbiBkb2FuIGRvaSBrZW5oIiwgZG9fbjEx'
'KSwKICAgICAgICAgKCJOMTIgaGFuZyBzZW50aW5lbCB0dXlldCBkb2kgQ0EgSEFJIG5lbiIsIGRvX24xMildCgojIC0tLSBjaGUg'
'ZG8gVFUgS0lFTTogY2hheSBuYW0gcHJvYmUgdHJlbiBtb3QgY2F5IGJhdCBreSwgbmVuIGJhdCBreSAtLS0KaWYgIi0tdHUta2ll'
'bS1wcm9iZSIgaW4gc3lzLmFyZ3Y6CiAgICBfZyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0tdHUta2llbS1wcm9i'
'ZSIpICsgMV0pLnJlc29sdmUoKQogICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX3Rr'
'Iiwgc3RyKF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICBfbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9z'
'cGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX2xwKQogICAgX3NpZyA9IGluc3BlY3Quc2lnbmF0dXJlKF9scC5fZ2l0'
'X3dpbmRvd3MpCiAgICBkZWYgX2dvaSgqKmt3KToKICAgICAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgICAgIHdpdGggY29udGV4'
'dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgICAgIHJldHVybiBfbHAuX2dpdF93aW5kb3dzKCoqa3cpLCBlLmdldHZh'
'bHVlKCkKICAgIHByaW50KGYiVFUgS0lFTSBQUk9CRSB0cmVuIHtfZ30gIChuZW4ge3N5cy5wbGF0Zm9ybX0pIikKICAgIGZvciBf'
'dGVuLCBfZiBpbiBQUk9CRToKICAgICAgICBfdHQsIF9jdCwgX2RsID0gX2YoX2dvaSwgX3NpZywgX2cvIm9wcyIvImxlYXNlX3B1'
'Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcHJpbnQoZiIgIFt7X3R0OjE0fV0ge190ZW59IiArIChmIiAgIHtfY3R9IiBpZiBfY3Qg'
'ZWxzZSAiIikpCiAgICAgICAgZm9yIF9rLCBfdiBpbiAoX2RsIG9yIHt9KS5pdGVtcygpOiBwcmludChmIiAgICAgICAge19rOjM0'
'fToge192fSIpCiAgICBzeXMuZXhpdCgwKQoKaW5uKCI9IiAqIDc4KTsgaW5uKCJXUDU0MSBnMiAtIHBoZXAgZG8gdHJlbiBXaW5k'
'b3dzIHRoYXQgKHNwZWMgcjM6IE4xLU40LCBOOC1OMTIsIE43LCBraWNoIHRodW9jKSIpOyBpbm4oIj0iICogNzgpCgojIC0tLS0t'
'LS0tLS0tLS0tLS0gdHUga2llbSBibyBkb2MgLS0tLS0tLS0tLS0tLS0tLQpfZCwgX2csIF90ID0gZG9jX2RvKF9NQVUpCl9vayA9'
'IChsZW4oX2QpID09IDIgYW5kIGFueSh4LnN0YXJ0c3dpdGgoInQwMmIiKSBmb3IgeCBpbiBfZCkKICAgICAgIGFuZCBub3QgYW55'
'KHguc3RhcnRzd2l0aCgidDEzMSIpIGZvciB4IGluIF9kKSBhbmQgX3QpCmlubigiVHUga2llbSBibyBkb2MgbG9nOiIsIERBVCBp'
'ZiBfb2sgZWxzZSBUUlVPVCkKaWYgbm90IF9vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogYm8gZG9jIGxvZyBj'
'dWEgY2hpbmggc2NyaXB0IG5heSBzYWkgLT4ga2hvbmcgZG8gZ2kgY2EuIik7IHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0t'
'LS0gMC4gbmVuIGRvIC0tLS0tLS0tLS0tLS0tLS0KZ29jID0gUGF0aChzeXMuYXJndlsxXSkucmVzb2x2ZSgpIGlmIGxlbihzeXMu'
'YXJndikgPiAxIGVsc2UgUGF0aC5jd2QoKQp0ZXAsIHRlcHQgPSBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoLnB5IiwgZ29j'
'IC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaF90ZXN0LnB5Igppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjAuIE5FTiBETyIp'
'CmlubigiICBzeXMucGxhdGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwgInwgcHl0aG9uIiwgc3lzLnZlcnNpb24uc3BsaXQoKVswXSkK'
'aW5uKCIgIG9zLnBhdGhzZXAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSwgInwgUEFUSEVYVDoiLCByZXByKG9zLmVudmlyb24uZ2V0'
'KCJQQVRIRVhUIikpWzo2MF0pCmlubigiICBQcm9ncmFtRmlsZXMgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlByb2dyYW1GaWxl'
'cyIpKSwgInwgU3lzdGVtUm9vdDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290IikpKQppbm4oIiAgQ09OR19DVV9H'
'SVQgIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJDT05HX0NVX0dJVCIpKSkKaW5uKCIgIGdvYyBraG8gICAgICA6IiwgZ29jKQoK'
'cXV5ZW4gPSBOb25lCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAgIGltcG9ydCBjdHlwZXM7IHF1'
'eWVuID0gYm9vbChjdHlwZXMud2luZGxsLnNoZWxsMzIuSXNVc2VyQW5BZG1pbigpKQogICAgZXhjZXB0IEV4Y2VwdGlvbjogcXV5'
'ZW4gPSBOb25lCmdoaSgicXV5ZW5fYWRtaW4iLCBxdXllbikKc3ltbGlua19kdW9jID0gTm9uZQp0cnk6CiAgICB3aXRoIHRlbXBm'
'aWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgodCkvImEudHh0IjsgZC53cml0ZV90ZXh0KCJ4'
'IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICB0cnk6IG9zLnN5bWxpbmsoc3RyKGQpLCBzdHIoUGF0aCh0KS8ibGsiKSk7IHN5'
'bWxpbmtfZHVvYyA9IFRydWUKICAgICAgICBleGNlcHQgT1NFcnJvciBhcyBlOiBzeW1saW5rX2R1b2MgPSBGYWxzZTsgZ2hpKCJz'
'eW1saW5rX2xvaSIsIGYie3R5cGUoZSkuX19uYW1lX199OiB7ZX0iKQpleGNlcHQgRXhjZXB0aW9uIGFzIGU6IGdoaSgic3ltbGlu'
'a19sb2kiLCBzdHIoZSkpCmdoaSgic3ltbGlua19kdW9jIiwgc3ltbGlua19kdW9jKQppbm4oIiAgQWRtaW5pc3RyYXRvcjoiLCBx'
'dXllbiwgInwgdGFvIHN5bWxpbmsgZHVvYzoiLCBzeW1saW5rX2R1b2MpCgpsb2kgPSBbXQppZiBzeXMucGxhdGZvcm0gIT0gIndp'
'bjMyIjogbG9pLmFwcGVuZChmIktIT05HIHBoYWkgV2luZG93cyAoc3lzLnBsYXRmb3JtPXtzeXMucGxhdGZvcm0hcn0pIikKaWYg'
'bm90IHRlcC5pc19maWxlKCk6ICBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwfSIpCmlmIG5vdCB0ZXB0LmlzX2ZpbGUoKTog'
'bG9pLmFwcGVuZChmImtob25nIHRoYXkge3RlcHR9IikKaWYgbm90IHNodXRpbC53aGljaCgiZ2l0Iik6IGxvaS5hcHBlbmQoImto'
'b25nIGNvIGBnaXRgIHRyb25nIFBBVEgiKQoKcmMsIGhlYWQsIF8gPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIkhFQUQiKQppZiBy'
'YzogbG9pLmFwcGVuZCgia2hvbmcgZG9jIGR1b2MgSEVBRCIpCmdoaSgiaGVhZCIsIGhlYWQpCnJjX2EsIF8sIF8gPSBnaXQoZ29j'
'LCAibWVyZ2UtYmFzZSIsICItLWlzLWFuY2VzdG9yIiwgU0hBX0cxLCBoZWFkIG9yICJIRUFEIikKbGFfaGF1X2R1ZSA9IChyY19h'
'ID09IDApCmlmIGhlYWQgPT0gU0hBX0cxOgogICAgdGhlX2hlID0gImcxIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBE'
'QVkgTEEgZzEuIENIVUEgY28gYmFuIHZhIGcyOyBrZXQgcXVhIGR1b2kgbGEgTkVOIERPLiIpCmVsaWYgbGFfaGF1X2R1ZToKICAg'
'IHRoZV9oZSA9ICJnMiI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gaGF1IGR1ZSBjdWEgZzEgKHtTSEFfRzFbOjhdfSk6'
'IHVuZyB2aWVuIGcyLiIpCmVsc2U6CiAgICB0aGVfaGUgPSAiPyI7IGxvaS5hcHBlbmQoZiJIRUFEPXtoZWFkWzo4XX0gS0hPTkcg'
'cGhhaSBnMSB2YSBLSE9ORyBwaGFpIGhhdSBkdWUgY3VhIHtTSEFfRzFbOjhdfSDigJQgcmViYXNlPyBuaGFtIG5oYW5oPyIpCmdo'
'aSgidGhlX2hlIiwgdGhlX2hlKQoKaWYgbG9pOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBuZW4gZG8gc2FpLCBL'
'SE9ORyBpbiBrZXQgbHVhbiBuYW8uIikKICAgIGZvciB4IGluIGxvaTogaW5uKCIgIC0iLCB4KQogICAgc3lzLmV4aXQoMykKCiMg'
'LS0tLS0tLS0tLS0tLS0tLSAxLiBraWNoIHRodW9jIChONycgY3VhIHNwZWMgcjMpIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsg'
'aW5uKCItIiAqIDc4KTsgaW5uKCIxLiBLSUNIIFRIVU9DIOKAlCB0cmFuIHNwZWMgcjM6IDw9IDIgdGVwIHZhIDw9IDQwMCBkb25n'
'IHRoZW0iKQpyY19tYiwgbWIsIGVyX21iID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAib3JpZ2luL21hc3RlciIsIGhlYWQpCmlm'
'IHJjX21iIG9yIG5vdCBtYjoKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9jIG1lcmdlLWJh'
'c2Ugdm9pIG9yaWdpbi9tYXN0ZXI6IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgogICAgZ2hpKCJtZXJn'
'ZV9iYXNlIiwgbWIpCiAgICBpbm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7bWJbOjEyXX0iKQogICAg'
'aWYgbWIgIT0gU0hBX0JBU0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2UgbWEgc3BlYyByMyBraGFpICh7'
'U0hBX0JBU0VfU1BFQ1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQogICAgICAgIGlubihmIiAgICAgICAg'
'IERvIHNvIGJhc2UgY3Ugc2UgTlVPVCBwaGFuIG1hc3RlciBtYW5nIHZhby4gRHVuZyBtZXJnZS1iYXNlIG1vaSBsYSB2aWVjIGN1'
'YSBleGVjdXRvci4iKQogICAgICAgIHJjX3gsIG5zX3gsIF8gPSBnaXQoZ29jLCAiZGlmZiIsICItLW51bXN0YXQiLCBTSEFfQkFT'
'RV9TUEVDLCBoZWFkKQogICAgICAgIGlmIG5vdCByY194OgogICAgICAgICAgICBoID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4g'
'bnNfeC5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAgICAgICAgICBhID0gc3VtKGludCh4WzBdKSBmb3IgeCBpbiBoIGlm'
'IHhbMF0uaXNkaWdpdCgpKQogICAgICAgICAgICBnaGkoIm51bXN0YXRfdGhlb19iYXNlX3NwZWMiLCB7InRlcCI6IGxlbihoKSwg'
'InRoZW0iOiBhfSkKICAgICAgICAgICAgaW5uKGYiICAgICAgICAgKGRvaSBjaGlldTogc28gYmFzZSBzcGVjID0ge2xlbihoKX0g'
'dGVwIC8gK3thfSDigJQgY29uIHNvIGF5IEtIT05HIGR1bmcgZGUgY2hhbSkiKQogICAgcmMsIG5zLCBlciA9IGdpdChnb2MsICJk'
'aWZmIiwgIi0tbnVtc3RhdCIsIG1iLCBoZWFkKQppZiByYzoKICAgIHBhc3MKZWxzZToKICAgIGhhbmcgPSBbbC5zcGxpdCgiXHQi'
'KSBmb3IgbCBpbiBucy5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAgdGhlbSA9IHN1bShpbnQoaFswXSkgZm9yIGggaW4g'
'aGFuZyBpZiBoWzBdLmlzZGlnaXQoKSkKICAgIHhvYSAgPSBzdW0oaW50KGhbMV0pIGZvciBoIGluIGhhbmcgaWYgaFsxXS5pc2Rp'
'Z2l0KCkpCiAgICBnaGkoInNvX3RlcCIsIGxlbihoYW5nKSk7IGdoaSgiZG9uZ190aGVtIiwgdGhlbSk7IGdoaSgiZG9uZ194b2Ei'
'LCB4b2EpCiAgICBmb3IgaCBpbiBoYW5nOiBpbm4oZiIgICAge2hbMl06MzR9ICt7aFswXTo8NX0gLXtoWzFdfSIpCiAgICBpbm4o'
'ZiIgICAgVE9ORzoge2xlbihoYW5nKX0gdGVwLCAre3RoZW19LCAte3hvYX0gICAodHJhbjoge1RSQU5fVEVQfSB0ZXAgLyB7VFJB'
'Tl9ET05HfSBkb25nIHRoZW0pIikKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBEQVQgaWYgKGxlbihoYW5nKSA8PSBUUkFOX1RF'
'UCBhbmQgdGhlbSA8PSBUUkFOX0RPTkcpIGVsc2UgVFJVT1QsCiAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IikK'
'CiMgLS0tLS0tLS0tLS0tLS0tLSAyLiBibyB0ZXN0IGRheSBkdSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3'
'OCk7IGlubigiMi4gQk8gVEVTVCBEQVkgRFUgKDEwLTQwIHBodXQpIikKcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1'
'Ymxpc2hfdGVzdC5weSJdLCBnb2MpCmdoaSgicmNfc3VpdGUiLCByY19uKQptID0gUlhfVE9ORy5zZWFyY2gob3V0X24pCmlubigi'
'ICByYyA9IiwgcmNfbiwgInwiLCBtLmdyb3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQpIikK'
'aWYgbToKICAgIGdoaSgiZGF0IiwgaW50KG0uZ3JvdXAoMSkpKTsgZ2hpKCJ0cmVuIiwgaW50KG0uZ3JvdXAoMikpKTsgZ2hpKCJi'
'b19xdWFfc28iLCBpbnQobS5ncm91cCg0KSkpCmRvX2hldCwgZ2MsIHRpbiA9IGRvY19kbyhvdXRfbikKZ2hpKCJzb19jYV9kbyIs'
'IGxlbihkb19oZXQpKTsgZ2hpKCJsaWV0X2tlX2RheV9kdSIsIHRpbikKZm9yIGcgaW4gZ2M6IGlubigiICAgKiIsIGcpCmlubigi'
'Iik7IGlubihmIiAgPT09IHtsZW4oZG9faGV0KX0gQ0EgRE8gPT09IikKZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2Nh'
'KToKICAgIGlubihmIiAgIHt0LnNwbGl0KCdfJylbMF06N30ge3R9Iik7IGlubihmIiAgICAgICAgICAge2RvX2hldFt0XVs6MTUw'
'XX0iKQpnaGkoImRvX2x5X2RvIiwge3Q6IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQojIC0tLS0gQ0hPVDogbW9p'
'IGNhIERPIHBoYWkgR0lBSSBUSElDSCBEVU9DIC0tLS0KIyBUaGlldSBjaG90IG5heSwgYm8gZG8gaW4gZGFuaCBzYWNoIGRvIHJv'
'aSB2YW4gdGhvYXQgcmM9MC4gRG8gZHVuZyBsYSBsb2kgZGEgeGF5IHJhOgojIGx1b3QgV2luZG93cyAxOS0wOSBjbyB0MTcxIERP'
'IG1hIGJvIGRvIGJhbyAiREFUIDEwIHwgVFJVT1QgMCIgdmEgcmM9MC4KZGVmIF9raG9hKHQpOiByZXR1cm4gdC5zcGxpdCgiXyIp'
'WzBdCmRvX3BhY2tldCwgZG9fbGEsIGRvX3RoaWV1X2NvbmdfY3UgPSBbXSwgW10sIFtdCmZvciB0IGluIHNvcnRlZChkb19oZXQs'
'IGtleT1zb19jYSk6CiAgICBrLCBseSA9IF9raG9hKHQpLCBkb19oZXRbdF0KICAgIGlmIGsgaW4gQ0FfUEFDS0VUOiAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgIGRvX3BhY2tldC5hcHBlbmQodCkKICAgIGVsaWYgIktIw5RORyDEkE8gxJDGr+G7okMiIGlu'
'IGx5IG9yICJ0aGnhur91IGAiIGluIGx5OiAgZG9fdGhpZXVfY29uZ19jdS5hcHBlbmQodCkKICAgIGVsaWYgayBpbiBOR09BSV9Q'
'SEFNX1ZJOiAgICAgICAgICAgICAgICAgICAgICAgIHBhc3MKICAgIGVsc2U6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgIGRvX2xhLmFwcGVuZCh0KQpnaGkoImRvX3BhY2tldCIsIGRvX3BhY2tldCk7IGdoaSgiZG9fbGEiLCBkb19s'
'YSk7IGdoaSgiZG9fdGhpZXVfY29uZ19jdSIsIGRvX3RoaWV1X2NvbmdfY3UpCmlubigiIikKaW5uKGYiICBjYSBETyB0aHVvYyBD'
'SElOSCBwYWNrZXQgbmF5IDoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdIG9yICdraG9uZyBjbyd9IikKaW5uKGYiICBj'
'YSBETyBuZ29haSBwaGFtIHZpIChyMyBraGFpKToge1tfa2hvYSh4KSBmb3IgeCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2Ep'
'IGlmIF9raG9hKHgpIGluIE5HT0FJX1BIQU1fVkldfSIpCmlubihmIiAgY2EgRE8gdmkgVEhJRVUgQ09ORyBDVSAgICAgICA6IHtb'
'X2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV0gb3IgJ2tob25nIGNvJ30iKQppbm4oZiIgIGNhIERPIExBIChraG9u'
'ZyBnaWFpIHRoaWNoIGR1b2MpOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXSBvciAna2hvbmcgY28nfSIpCmtldCgiS2hvbmcg'
'Y2EgbmFvIGN1YSBQQUNLRVQgYmkgRE8iLCBEQVQgaWYgbm90IGRvX3BhY2tldCBlbHNlIFRSVU9ULAogICAgIiIgaWYgbm90IGRv'
'X3BhY2tldCBlbHNlIGYiRE86IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XX0g4oCUIGJhbiB2YSBDSFVBIHhvbmciKQpr'
'ZXQoIk1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jIiwgREFUIGlmIG5vdCBkb19sYSBlbHNlIFRSVU9ULAogICAgIiIgaWYg'
'bm90IGRvX2xhIGVsc2UgZiJsYToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV19IikKaWYgZG9fdGhpZXVfY29uZ19jdToKICAg'
'IGtldCgiQ29uZyBjdSBkYXkgZHUgZGUgZG8iLCBLREQsIGYidGhpZXUgY29uZyBjdSBjaG8ge1tfa2hvYSh4KSBmb3IgeCBpbiBk'
'b190aGlldV9jb25nX2N1XX0iKQoKYnEgPSBzb3J0ZWQoe3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0X24pfSwg'
'a2V5PXNvX2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBicSkKaW5uKCIiKTsgaW5uKGYiICBCTyBRVUEgKHtsZW4oYnEpfSk6IHtbeC5z'
'cGxpdCgnXycpWzBdIGZvciB4IGluIGJxXX0iKQoKaW5uKCIiKTsgaW5uKCIgIE4xLU40ICh0MTY1LXQxNjgpLCB0aWV1IGNoaSBu'
'Z2hpZW0gdGh1IGN1YSByMiwgbmF5IGxhIGNoaSBiYW8gaG9pIHF1eToiKQpiNCA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0'
'IGluIENBTU9JfTsgZ2hpKCJjYV9tb2kiLCBiNCkKZm9yIHQgaW4gQ0FNT0k6IGlubihmIiAgICAge3R9OiB7YjRbdF19IikKa2V0'
'KCJOMS1ONCAodDE2NS10MTY4KSIsIERBVCBpZiBhbGwodiA9PSAiUVVBIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkKICAgIGVsc2Ug'
'KEtERCBpZiBhbnkodiBpcyBOb25lIGZvciB2IGluIGI0LnZhbHVlcygpKSBlbHNlIFRSVU9UKSwgc3RyKGI0KSkKCmlubigiIik7'
'IGlubigiICAxNSBjYSB0dW5nIGRvIHRyZW4gQ0k6IikKYjE1ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0ExNX07'
'IGdoaSgiY2ExNSIsIGIxNSkKaW5uKCIgICAgIiArICIgICIuam9pbihmInt0fTp7YjE1W3RdfSIgZm9yIHQgaW4gQ0ExNSkpCgoj'
'IHQxMzYg4oCUIE4xMiBkbyBHSUFOIFRJRVAgcXVhIGtldCBxdWEgY2EKdDEzNl90ZW4gPSBuZXh0KCh0IGZvciB0IGluIGRvX2hl'
'dCBpZiB0LnN0YXJ0c3dpdGgoInQxMzYiKSksIE5vbmUpCmlmIGIxNS5nZXQoInQxMzYiKSA9PSAiUVVBIjoKICAgIGtldCgiTjEy'
'IHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIERBVCwgInQxMzYgUVVBIikKZWxpZiBiMTUuZ2V0KCJ0MTM2IikgaXMgTm9uZToKICAg'
'IGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIEtERCwgImtob25nIHRoYXkgdDEzNiB0cm9uZyBsb2ciKQplbHNlOgog'
'ICAgbHkgPSBkb19oZXQuZ2V0KHQxMzZfdGVuLCAiIikKICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIFRSVU9U'
'LCBmIkRPOiB7bHlbOjkwXX0iKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDMuIHByb2JlIFRIQU5HIHZhbyBoYW0gLS0tLS0tLS0tLS0t'
'LS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjMuIFBST0JFIFRIQU5HIOKAlCBnb2kgX2dpdF93aW5kb3dzIHZvaSB0'
'aGFtIHNvIHRpZW0iKQpzcGVjID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwNTQxIiwgc3RyKHRl'
'cCkpCmxwID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhzcGVjKTsgc3BlYy5sb2FkZXIuZXhlY19tb2R1bGUobHAp'
'CnNpZyA9IGluc3BlY3Quc2lnbmF0dXJlKGxwLl9naXRfd2luZG93cykKZ2hpKCJ0aGFtX3NvX19naXRfd2luZG93cyIsIGxpc3Qo'
'c2lnLnBhcmFtZXRlcnMpKQppbm4oIiAgdGhhbSBzbyBjdWEgX2dpdF93aW5kb3dzOiIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQoK'
'ZGVmIGdvaSgqKmt3KToKICAgICIiIkdvaSBfZ2l0X3dpbmRvd3MsIEJBVCBzdGRlcnIgZGUgbW90IGRvbmcgY2hhbiBkb2FuIGto'
'b25nIGdpZXQgbHVvdCBkby4iIiIKICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3Rk'
'ZXJyKGUpOgogICAgICAgIHIgPSBscC5fZ2l0X3dpbmRvd3MoKiprdykKICAgIHJldHVybiByLCBlLmdldHZhbHVlKCkKCiMgLS0t'
'IGRvaSBjaHVuZyByaWc6IHBoYWkgdHJhIGxvaSBkdW5nIG1vdCBjYSB0YSBCSUVUIFRSVU9DIGRhcCBhbiAtLS0Kd2l0aCB0ZW1w'
'ZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgbmdvYWkgPSBQYXRoKHQpLyJuZ29haSI7IG5nb2FpLm1rZGlyKCk7'
'IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIChuZ29haS8i'
'Z2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjEsIF8gPSBnb2kocGF0aD1zdHIobmdvYWkp'
'LCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgKGN3LyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVu'
'Y29kaW5nPSJ1dGYtOCIpCiAgICByMiwgXyA9IGdvaShwYXRoPXN0cihjdyksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0'
'cihjdykpCnJpZ19vayA9IGJvb2wocjEpIGFuZCByMiBpcyBOb25lCmdoaSgicmlnX2RvaV9jaHVuZyIsIHJpZ19vaykKa2V0KCJS'
'SUcgZG9pIGNodW5nIChiaWV0IHRydW9jIGRhcCBhbikiLCBEQVQgaWYgcmlnX29rIGVsc2UgS0RELAogICAgZiJuZ29haS1jd2Qt'
'PnsnTkhBTicgaWYgcjEgZWxzZSAnTm9uZSd9IHwgdHJvbmctY3dkLT57J05IQU4nIGlmIHIyIGVsc2UgJ05vbmUnfSIpCmlmIG5v'
'dCByaWdfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IHJpZyBzYWksIG1vaSBjaG90IGR1b2kgc2Ugdm8gbmdo'
'aWEuIik7IHN5cy5leGl0KDMpCgpmb3IgdGVuLCAodHQsIGN0LCBkbCkgaW4gWyh0LCBmKGdvaSwgc2lnLCB0ZXB0KSkgZm9yIHQs'
'IGYgaW4gUFJPQkVdOgogICAgZ2hpKCJwcm9iZV8iICsgdGVuLnNwbGl0KClbMF0ubG93ZXIoKSwgZGwpCiAgICBpZiBpc2luc3Rh'
'bmNlKGRsLCBkaWN0KToKICAgICAgICBmb3IgaywgdiBpbiBkbC5pdGVtcygpOiBpbm4oZiIgICAge2s6MzR9OiB7dn0iKQogICAg'
'a2V0KHRlbiwgdHQsIGN0KQoKIyAtLS0tLS0tLS0tLS0tLS0tIDQuIE43IGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gLS0tLS0t'
'LS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjQuIE43IOKAlCBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFN'
'IChjYXkgdGhhdCBLSE9ORyBiaSBkdW5nIHRvaSkiKQp0cnVvYyA9IHRlcC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291'
'bnQoTUFVX1dJTikKZ2hpKCJuN190cnVvYyIsIHRydW9jKTsgaW5uKGYiICBzbyBkb25nIGtob3Age01BVV9XSU4hcn06IFRSVU9D'
'ID0ge3RydW9jfSBbbW9uZyAxXSIpCmlmIHRydW9jICE9IDE6CiAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBL'
'REQsIGYibWF1IHh1YXQgaGllbiB7dHJ1b2N9IGxhbiwga2hvbmcgcGhhaSAxIikKZWxzZToKICAgIHdpdGggdGVtcGZpbGUuVGVt'
'cG9yYXJ5RGlyZWN0b3J5KCkgYXMgdG1wOgogICAgICAgIHNhbyA9IFBhdGgodG1wKS8iY2F5IgogICAgICAgIHNodXRpbC5jb3B5'
'dHJlZShnb2MsIHNhbywgaWdub3JlPXNodXRpbC5pZ25vcmVfcGF0dGVybnMoIi5naXQiLCAiX19weWNhY2hlX18iLCAiKi5weWMi'
'KSkKICAgICAgICBmMiA9IHNhby8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIKICAgICAgICBmMi53cml0ZV90ZXh0KGYyLnJlYWRf'
'dGV4dChlbmNvZGluZz0idXRmLTgiKS5yZXBsYWNlKE1BVV9XSU4sICJpZiBGYWxzZToiKSwgZW5jb2Rpbmc9InV0Zi04IikKICAg'
'ICAgICBzYXUgPSBmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTik7IGdoaSgibjdfc2F1Iiwgc2F1'
'KQogICAgICAgIGlubihmIiAgU0FVIChkYSBkb3QgYmllbikgPSB7c2F1fSBbbW9uZyAwXSIpCiAgICAgICAgaWYgc2F1ICE9IDA6'
'CiAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgImRvdCBiaWVuIEtIT05HIGFwIGR1b2Mi'
'KQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIHJjX20sIG91dF9tID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHki'
'XSwgc2FvKQogICAgICAgICAgICBtMTY1ID0gbWF1X2NhKG91dF9tLCAidDE2NSIpOyBkbSwgXywgXyA9IGRvY19kbyhvdXRfbSkK'
'ICAgICAgICAgICAgdGVuMTY1ID0gbmV4dCgodCBmb3IgdCBpbiBkbSBpZiB0LnN0YXJ0c3dpdGgoInQxNjUiKSksIE5vbmUpCiAg'
'ICAgICAgICAgIGx5ID0gKGRtLmdldCh0ZW4xNjUpIG9yICIiKQogICAgICAgICAgICBnaGkoIm43X3QxNjUiLCBtMTY1KTsgZ2hp'
'KCJuN19seV9kbyIsIGx5WzoyMDBdKQogICAgICAgICAgICBpbm4oZiIgIHQxNjUgc2F1IGRvdCBiaWVuOiB7bTE2NX0gfCB7bHlb'
'OjExMF19IikKICAgICAgICAgICAgZHVuZ19seV9kbyA9ICJQQVRIIHQiIGluIGx5IG9yICIvdXNyL2JpbiIgaW4gbHkKICAgICAg'
'ICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgREFUIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8p'
'IGVsc2UKICAgICAgICAgICAgICAgIChUUlVPVCBpZiBtMTY1ID09ICJETyIgZWxzZSBLREQpLAogICAgICAgICAgICAgICAgImdp'
'ZXQgZHVuZyBseSBkbyIgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykKICAgICAgICAgICAgICAgIGVsc2UgKCJETyBu'
'aHVuZyBLSE9ORyBkdW5nIGx5IGRvIC0+IHRpbiBkdW5nIGdpYSIgaWYgbTE2NSA9PSAiRE8iIGVsc2UgImtob25nIGRvYyBkdW9j'
'IHQxNjUiKSkKCiMgLS0tLS0tLS0tLS0tLS0tLSBLRVQgTFVBTiAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiPSIgKiA3'
'OCkKaW5uKGYiVEhFIEhFIERPIERVT0M6IHt0aGVfaGV9ICAgSEVBRD17aGVhZFs6MTJdfSIpCmlmIHRoZV9oZSA9PSAiZzEiOgog'
'ICAgaW5uKCJMVVUgWTogZGF5IGxhIE5FTiBETyAoZzEpLCBLSE9ORyBwaGFpIG5naGllbSB0aHUgZzIuIENhYyBjaG90IE44LU4x'
'MiBkdW9pIGRheSIpCiAgICBpbm4oIiAgICAgICBUUlVPVCBsYSBEVU5HIE5IVSBNT05HIOKAlCBjaHVuZyBsYSBuaHVuZyBsbyBn'
'MiBzaW5oIHJhIGRlIHbDoS4iKQppbm4oIi0iICogNzgpCmZvciB0ZW4sIHR0LCBjdCBpbiBjaG90OgogICAgaW5uKGYiICB7dHQ6'
'MTR9IHt0ZW59IiArIChmIiAgIHtjdH0iIGlmIGN0IGVsc2UgIiIpKQpuX2tkZCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3Qg'
'aWYgdCA9PSBLREQpCm5fdHJ1b3QgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCmlubigiLSIgKiA3'
'OCkKaW5uKGYiICBEQVQge3N1bSgxIGZvciBfLHQsXyBpbiBjaG90IGlmIHQ9PURBVCl9IHwgVFJVT1Qge25fdHJ1b3R9IHwgS0hP'
'TkcgRE8gRFVPQyB7bl9rZGR9IikKaW5uKGYiICBUb25nIGNhIGRvOiB7c28uZ2V0KCdzb19jYV9kbycpfSB8IGRhbmggc2FjaCBk'
'YXkgZHU6IHsnQ08nIGlmIHNvLmdldCgnbGlldF9rZV9kYXlfZHUnKSBlbHNlICdLSE9ORyBETyBEVU9DJ30iKQppbm4oZiIgIEFk'
'bWluaXN0cmF0b3I6IHtzby5nZXQoJ3F1eWVuX2FkbWluJyl9IHwgc3ltbGluazoge3NvLmdldCgnc3ltbGlua19kdW9jJyl9IikK'
'aW5uKCIiKTsgaW5uKCItLS0gREFOIE5HVVlFTiBLSE9JIEpTT04gTkFZIFZFIENITyBSRVZJRVdFUiAtLS0iKQpnaGkoImNob3Qi'
'LCBbeyJ0ZW4iOiBhLCAidHJhbmdfdGhhaSI6IGIsICJjaGlfdGlldCI6IGN9IGZvciBhLCBiLCBjIGluIGNob3RdKQppbm4oanNv'
'bi5kdW1wcyhzbywgZW5zdXJlX2FzY2lpPUZhbHNlLCBpbmRlbnQ9MSwgZGVmYXVsdD1zdHIpKQojIHJjOiAwID0gbW9pIGNob3Qg'
'REFUIHwgMSA9IGNvIGNob3QgVFJVT1QgfCAzID0gY28gY2hvdCBLSE9ORyBETyBEVU9DICh1dSB0aWVuIGJhbyBkb25nKQpzeXMu'
'ZXhpdCgzIGlmIG5fa2RkIGVsc2UgKDEgaWYgbl90cnVvdCBlbHNlIDApKQo='
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

Write-Host "fetch ban va $Nhanh ..."
G -C "$Kho" fetch --quiet origin $Nhanh | Out-Null
G -C "$Kho" checkout --quiet -B do-tam FETCH_HEAD | Out-Null
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
