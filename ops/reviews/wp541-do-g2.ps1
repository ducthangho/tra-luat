# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong, khong can gi khac):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
#
# Do RIENG cong kich thuoc (vai giay, khong chay bo test 20-45 phut):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1" -ChiKichThuoc
#
# Nhanh mac dinh la claude/va-541-t171-20260919 (ban va dang do). Doi nhanh khac:
#     ... -Nhanh fix_issue_541
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
    [string]$Nhanh   = 'claude/va-541-t171-20260919',  # nhanh mang ban va can do
    [switch]$ChiGiaiNen,       # chi ghi bo do Python ra dia roi dung (de doc/kiem)
    [switch]$ChiKichThuoc,     # CHI do cong kich thuoc (vai giay) roi dung - khong chay bo test
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
$ShaBoDo    = '2c3ca45755f821e5a8c7347ec3aa8b97f78c2749ac2b05464038e238fc6e7ba2'      # SHA-256 cua bo do Python nhung ben duoi

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
'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIiIiV1A1NDEgZzIgLSBQSEVQIERPIFRSRU4gV0lORE9XUyBUSEFUIGNobyBzcGVj',
'IHIzIChOMS1ONCArIE44LU4xMiArIE43ICsga2ljaCB0aHVvYykuCgpDaGF5OiAgcHkgd3A1NDEtZG8tZzItd2luZG93cy5w',
'eSAiPHRodS1tdWMta2hvPiIKCktIT05HIGdoaW0gU0hBLiBObyBkbyBCQVQgS1kgZGF1IG5hbyBkYW5nIG8gdHJlbiBuaGFu',
'aCwgcm9pIFRVIFBIQU4gTE9BSToKICBoZWFkID09IDJmNzA4NjlhICAtPiBkYXkgbGEgZzEsIENIVUEgY28gYmFuIHZhIGcy',
'LiBWYW4gZG8sIG5odW5nIG5oYW4gbGEgTkVOIERPLgogIGhlYWQgbGEgaGF1IGR1ZSAgICAtPiB1bmcgdmllbiBnMi4KICBr',
'aGFjICAgICAgICAgICAgICAgLT4gS0hPTkcgRE8gRFVPQyAocmViYXNlPyBuaGFtIG5oYW5oPykgLT4gcmM9Mywga2hvbmcg',
'a2V0IGx1YW4uCgpCQSBUUkFORyBUSEFJIG8gbW9pIGNob3Q6IERBVCAvIFRSVU9UIC8gS0hPTkcgRE8gRFVPQy4gQ2FpIHRo',
'dSBiYSBLSE9ORyBkdW9jIGxhbmcgbGUKdGhhbmggbW90IHRyb25nIGhhaSBjYWkga2lhIOKAlCBkbyBsYSBjYSBkb2N0cmlu',
'ZSBgTm9uZSAhPSBGYWxzZWAgY3VhIGtoby4KCk1PSSBjaG90IGFtIGRldSBjbyBET0kgQ0hVTkcgRFVPTkcuIE1vdCBjaG90',
'IGNoaSBkbyBjaGlldSAicGhhaSB0dSBjaG9pIiB0aGkgbW90IGhhbQpgcmV0dXJuIE5vbmVgIHZvIGRpZXUga2llbiBjdW5n',
'IHF1YSBkdW9jIG5vLgoKRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaSBkdW5nIHRv',
'aS4KIiIiCmltcG9ydCBjb250ZXh0bGliLCBpbXBvcnRsaWIudXRpbCwgaW5zcGVjdCwgaW8sIGpzb24sIG9zLCByZSwgc2h1',
'dGlsLCBzdWJwcm9jZXNzLCBzeXMsIHRlbXBmaWxlCmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aCwgUHVyZVBvc2l4UGF0aCwg',
'UHVyZVdpbmRvd3NQYXRoCgpvcy5lbnZpcm9uLnNldGRlZmF1bHQoIlBZVEhPTlVURjgiLCAiMSIpCm9zLmVudmlyb24uc2V0',
'ZGVmYXVsdCgiUFlUSE9OSU9FTkNPRElORyIsICJ1dGYtOCIpCmZvciBfbCBpbiAoc3lzLnN0ZG91dCwgc3lzLnN0ZGVycik6',
'CiAgICB0cnk6IF9sLnJlY29uZmlndXJlKGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIpCiAgICBleGNlcHQg',
'RXhjZXB0aW9uOiBwYXNzCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAgIGltcG9ydCBjdHlw',
'ZXMKICAgICAgICBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlNldENvbnNvbGVPdXRwdXRDUCg2NTAwMSkKICAgICAgICBjdHlw',
'ZXMud2luZGxsLmtlcm5lbDMyLlNldENvbnNvbGVDUCg2NTAwMSkKICAgIGV4Y2VwdCBFeGNlcHRpb246IHBhc3MKCmRlZiBp',
'bm4oKnApOgogICAgdmFuID0gIiAiLmpvaW4oc3RyKHgpIGZvciB4IGluIHApCiAgICB0cnk6IHByaW50KHZhbiwgZmx1c2g9',
'VHJ1ZSkKICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgdHJ5OiBzeXMuc3Rkb3V0LmJ1ZmZlci53cml0ZSh2YW4uZW5j',
'b2RlKCJ1dGYtOCIsICJyZXBsYWNlIikgKyBiIlxuIik7IHN5cy5zdGRvdXQuZmx1c2goKQogICAgICAgIGV4Y2VwdCBFeGNl',
'cHRpb246IHByaW50KHZhbi5lbmNvZGUoImFzY2lpIiwgImJhY2tzbGFzaHJlcGxhY2UiKS5kZWNvZGUoImFzY2lpIiksIGZs',
'dXNoPVRydWUpCgpTSEFfRzEgICA9ICIyZjcwODY5YTA1Mzc4NDNlOWNhZTc4NjE4ZWU3YWU4YzI2MWQ5NzJkIgojIEtIT05H',
'IGdoaW0gYmFzZS4gU3BlYyByMyBONicga2hhaSBkbyBudW1zdGF0IHNvIGQ3MDU2MjMg4oCUIE5IVU5HIHNwZWMgQ1VORyBi',
'YW8gZXhlY3V0b3IKIyBgZ2l0IG1lcmdlIG9yaWdpbi9tYXN0ZXJgLiBTYXUgbWVyZ2UsIHBoZXAgZG8gc28gZDcwNTYyMyBO',
'VU9UIGNhIHBoYW4gbWFzdGVyIG1hbmcgdmFvOgojIGRvIHRoYXQgMTgtMDkgdHJlbiBiYW4gdmEgZzIgY3VhIGFneSBjaG8g',
'NSB0ZXAgLyArODEyLCB0cm9uZyBraGkgdmllYyBjdWEgYWd5IGxhIDIgdGVwIC8gKzM1My4KIyBNb3QgY2hvdCBuaHUgdGhl',
'IHNlIGJhbyAidnVvdCB0cmFuIiBjaG8gbW90IGJhbiB2YSBLSE9ORyB2dW90LiBCYXNlIGR1bmcgbGEgTUVSR0UtQkFTRS4K',
'U0hBX0JBU0VfU1BFQyA9ICJkNzA1NjIzMTYyYjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpUUkFOX1RFUCwgVFJB',
'Tl9ET05HID0gMiwgNDAwICAgICAgICAgICMgTjcnIGN1YSBzcGVjIHIzCk1BVV9XSU4gID0gJ2lmIG5lbl90aHVjID09ICJ3',
'aW5kb3dzIjonCiMgQ2EgbmdvYWkgcGhhbSB2aSByMyDCp25nb2FpX3BoYW1fdmkg4oCUIGRvIENISU5IIFNQRUMga2hhaSwg',
'a2hvbmcgcGhhaSBibyBkbyB0dSBxdXlldC4KIyBEbyBsYSBEQU5IIFNBQ0ggQ0hPIFBIRVA6IGNhIGRvIG5hbyBLSE9ORyBu',
'YW0gdHJvbmcgZGF5IHZhIEtIT05HIHBoYWkgInRoaWV1IGNvbmcgY3UiCiMgdGhpIGxhIFRSVU9ULiBEYW5oIHNhY2ggY2Ft',
'IHRoaSBiYW8gZ2lvIGN1bmcgdGhpZXU7IGRhbmggc2FjaCBjaG8gcGhlcCB0aGkgYmlldCB0cnVvYy4KTkdPQUlfUEhBTV9W',
'SSA9IHNldCgidDEzMSB0MTMyIHQxNTAgdDEyNSB0MzUgdDM2IHQzNyB0MzggdDM5IHQ0MCIuc3BsaXQoKSkKIyBDYSBjdWEg',
'Q0hJTkggcGFja2V0IG5heS4gTW90IGNhIG8gZGF5IG1hIERPIHRoaSBraG9uZyBiYW8gZ2lvIGR1b2MgYm8gcXVhLgpDQV9Q',
'QUNLRVQgPSBzZXQoInQxNjUgdDE2NiB0MTY3IHQxNjggdDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpKQpDQTE1',
'ICA9ICJ0MTI5IHQxMzAgdDEzMSB0MTMyIHQxMzMgdDEzNiB0MTM4IHQxMzkgdDE0NCB0MTQ1IHQxNDYgdDE0NyB0MTQ5IHQx',
'NTAgdDE1MSIuc3BsaXQoKQpDQU1PSSA9ICJ0MTY1IHQxNjYgdDE2NyB0MTY4Ii5zcGxpdCgpCgpEQVQsIFRSVU9ULCBLREQg',
'PSAiREFUIiwgIlRSVU9UIiwgIktIT05HIERPIERVT0MiCnNvLCBjaG90ID0ge30sIFtdCmRlZiBnaGkoaywgdik6IHNvW2td',
'ID0gdjsgcmV0dXJuIHYKZGVmIGtldCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0PSIiKToKICAgIGNob3QuYXBwZW5kKCh0',
'ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0KSkKICAgIGlubihmIiAgW3t0cmFuZ190aGFpOjE0fV0ge3Rlbn0iICsgKGYiICAg',
'e2NoaV90aWV0fSIgaWYgY2hpX3RpZXQgZWxzZSAiIikpCiAgICByZXR1cm4gdHJhbmdfdGhhaQoKIyAtLS0tLS0tLS0tLS0t',
'LS0tIGRvYyBsb2cgY3VhIGJvIHRlc3QgKGJhbiAzLCBkYSBkbyB0cmVuIGxvZyBUSEFUKSAtLS0tLS0tLS0tLS0tLS0tClJY',
'X0RPX0NITyAgPSByZS5jb21waWxlKHIiKD9tKV4hISEgZG8gKFxTKykgKC4qKSQiKQpSWF9ET19DVU9JID0gcmUuY29tcGls',
'ZShyIig/bSleIHsyfShcU3sxLDR9KSB7Mn0oXFMrKTogKC4qKSQiKQpSWF9CT19RVUEgID0gcmUuY29tcGlsZShyIig/bSle',
'IHsyfVxTezEsNn0gUVVBIChcUyspOiAoLiopJCIpClJYX1RPTkcgICAgPSByZS5jb21waWxlKHIibGVhc2VfcHVibGlzaDog',
'KFxkKykvKFxkKylcYlteXG5dKj89KFxkKyksW15cbl0qPz0oXGQrKSIpCgpkZWYgc29fY2EodCk6CiAgICBtID0gcmUubWF0',
'Y2gociJ0KFxkKykiLCB0KTsgcmV0dXJuIChpbnQobS5ncm91cCgxKSkgaWYgbSBlbHNlIDEwKio2LCB0KQoKZGVmIGRvY19k',
'byhvdXQpOgogICAgdGFpX2NobyA9IHt0OiBsLnN0cmlwKCkgZm9yIHQsIGwgaW4gUlhfRE9fQ0hPLmZpbmRhbGwob3V0KX0K',
'ICAgIGJvID0ge3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0KX0KICAgIGN1b2kgPSB7dDogbC5zdHJpcCgp',
'IGZvciBfLCB0LCBsIGluIFJYX0RPX0NVT0kuZmluZGFsbChvdXQpIGlmIHQgbm90IGluIGJvfQogICAgaG9wID0gZGljdChj',
'dW9pKTsgaG9wLnVwZGF0ZSh0YWlfY2hvKQogICAgZ2MsIHRpbiA9IFtdLCBUcnVlCiAgICBpZiBzZXQodGFpX2NobykgIT0g',
'c2V0KGN1b2kpOgogICAgICAgIGdjLmFwcGVuZChmImhhaSBuZ3VvbiBMRUNIOiBjaGktdGFpLWNobz17c29ydGVkKHNldCh0',
'YWlfY2hvKS1zZXQoY3VvaSkpfSBjaGktY3VvaT17c29ydGVkKHNldChjdW9pKS1zZXQodGFpX2NobykpfSIpCiAgICAgICAg',
'dGluID0gRmFsc2UKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXQpCiAgICBpZiBub3QgbToKICAgICAgICBnYy5hcHBlbmQo',
'IktIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQiKTsgdGluID0gRmFsc2UKICAgIGVsc2U6CiAgICAgICAgZGF0LCB0cmVu',
'ID0gaW50KG0uZ3JvdXAoMSkpLCBpbnQobS5ncm91cCgyKSkKICAgICAgICBnYy5hcHBlbmQoZiJzbyBob2M6IHt0cmVufS17',
'ZGF0fT17dHJlbi1kYXR9IGRvOyBkb2MgZHVvYyB7bGVuKGhvcCl9IikKICAgICAgICBpZiB0cmVuIC0gZGF0ICE9IGxlbiho',
'b3ApOgogICAgICAgICAgICBnYy5hcHBlbmQoZiJMRUNIIFNPIEhPQzogdGhpZXUge3RyZW4tZGF0LWxlbihob3ApfSBjYSIp',
'OyB0aW4gPSBGYWxzZQogICAgcmV0dXJuIGhvcCwgZ2MsIHRpbgoKX01BVSA9ICgiISEhIGRvIHQwMmJfdGVuX0tIT05HX0NP',
'X1RIQU1fUVVZRU4gYVxuIgogICAgICAgICIhISEgZG8gdDE1MF94IFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdl',
'XG4iCiAgICAgICAgIiAgQuG7jiBRVUEgdDEzMV95OiBuZW4gZml4dHVyZVxuIgogICAgICAgICIgIMSQ4buOICB0MDJiX3Rl',
'bl9LSE9OR19DT19USEFNX1FVWUVOOiBhXG4iCiAgICAgICAgIiAgxJDhu44gIHQxNTBfeDogV2luRXJyb3IgMTMxNCByZXF1',
'aXJlZCBwcml2aWxlZ2VcbiIKICAgICAgICAibGVhc2VfcHVibGlzaDogMS8zIMSR4bqhdDsgxJHDoyBjaOG6oXk9MywgYuG7',
'jyBxdWE9MVxuIikKCmRlZiBjaGF5KGFyZ3YsIGN3ZCwgcGh1dD02MCk6CiAgICBtdCA9IGRpY3Qob3MuZW52aXJvbiwgUFlU',
'SE9OVVRGOD0iMSIsIFBZVEhPTklPRU5DT0RJTkc9InV0Zi04IiwKICAgICAgICAgICAgICBQWVRIT05ET05UV1JJVEVCWVRF',
'Q09ERT0iMSIsIFBZVEhPTlVOQlVGRkVSRUQ9IjEiKQogICAgcCA9IHN1YnByb2Nlc3MucnVuKFtzeXMuZXhlY3V0YWJsZV0g',
'KyBhcmd2LCBjd2Q9c3RyKGN3ZCksIGNhcHR1cmVfb3V0cHV0PVRydWUsCiAgICAgICAgICAgICAgICAgICAgICAgdGV4dD1U',
'cnVlLCBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjAsIGVudj1tdCkKICAgIHJl',
'dHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1X2NhKG91dCwg',
'dCk6CiAgICBtID0gcmUuc2VhcmNoKHIiKD9tKV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSBbMC05Ll0rcyAoXHcr',
'KVxzKiQiLCBvdXQpCiAgICByZXR1cm4gbS5ncm91cCgyKSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdpdChnb2MsICphLCBwaHV0',
'PTUpOgogICAgcCA9IHN1YnByb2Nlc3MucnVuKFsiZ2l0IiwgIi1DIiwgc3RyKGdvYyksICphXSwgY2FwdHVyZV9vdXRwdXQ9',
'VHJ1ZSwgdGV4dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFj',
'ZSIsIHRpbWVvdXQ9cGh1dCo2MCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikuc3RyaXAoKSwg',
'KHAuc3RkZXJyIG9yICIiKS5zdHJpcCgpCgoKIyA9PT09PT09PT09PT09PT09PSBOQU0gUFJPQkUsIHZpZXQgdGhhbmggSEFN',
'IFRIVUFOIGRlIFRVIEtJRU0gZHVvYyA9PT09PT09PT09PT09PT09PQojIE1vaSBoYW0gdHJhICh0cmFuZ190aGFpLCBjaGlf',
'dGlldCwgZHVfbGlldSkuIEtIT05HIGluLCBLSE9ORyB0aG9hdCDigJQgbmhvIHZheSBjaHVuZwojIGNoYXkgZHVvYyB0cmVu',
'IG5lbiBCQVQgS1ksIHZhIGAtLXR1LWtpZW0tcHJvYmVgIGdvaSB0aGFuZyBjaHVuZyBkZSBraWVtIGNoaW5oIGJvIGRvLgoK',
'ZGVmIF9zYW4odCk6CiAgICBkID0gUGF0aCh0KS8iZCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2Rp',
'cigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgcmV0dXJuIGQsIGN3LCBwZgoKZGVmIGRvX244KGdvaSwg',
'c2lnLCB0ZXB0KToKICAgICIiIkJ1b2MgMSAoQ09OR19DVV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0LmV4ZS4gRG9pIGNodW5n',
'IGR1b25nOiBnaXQuZXhlIFZBTiBwaGFpIG5oYW4uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFy',
'eURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIGZvciB0ZW4gaW4gKCJnaXQu',
'ZXhlIiwgImdpdC5iYXQiLCAiZ2l0LmNtZCIsICJnaXQucHkiLCAia2hvbmctcGhhaS1naXQudHh0Iik6CiAgICAgICAgICAg',
'IGYgPSBkL3RlbjsgZi53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyA9IGdvaShj',
'b25nX2N1X2dpdD1zdHIoZiksIHBhdGg9IiIsIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAg',
'ICAgIGtxW2YiQ09OR19DVV9HSVQ9e3Rlbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIlRVIENIT0kiCiAgICBsb3QgPSBbayBm',
'b3IgaywgdiBpbiBrcS5pdGVtcygpIGlmIHYgPT0gIk5IQU4iIGFuZCBub3Qgay5lbmRzd2l0aCgiZ2l0LmV4ZSIpXQogICAg',
'aWYga3EuZ2V0KCJDT05HX0NVX0dJVD1naXQuZXhlIikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1',
'bmcgZHVvbmcgaG9uZzogZ2l0LmV4ZSBob3AgbGUgbWEgYmkgdHUgY2hvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3Qg',
'bG90IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IGxvdCBlbHNlIGYiY29uIG5oYW46IHtsb3R9IiksIGtxCgpkZWYgZG9fbjko',
'Z29pLCBzaWcsIHRlcHQpOgogICAgIiIiTXVjIFBBVEggYm9jIG5oYXkga2VwIHBoYWkgTkhBTjsgbXVjIHJvbmcgLyB0b2Fu',
'IGtob2FuZyB0cmFuZyBwaGFpIGJvIHF1YSwga2hvbmcgbmVtLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5U',
'ZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBkLm1rZGlyKCk7IGN3ID0g',
'UGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgICAgICAoZC8iZ2l0',
'LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGZvciBuaGFuLCBtdWMgaW4gKCgia2hv',
'bmcgbmhheSIsIHN0cihkKSksICgiY28gbmhheSBrZXAiLCBmJyJ7ZH0iJyksCiAgICAgICAgICAgICAgICAgICAgICAgICAg',
'KCJyb25nIiwgIiIpLCAoImNoaSBraG9hbmcgdHJhbmciLCAiICAgIikpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAg',
'ICAgICByLCBfID0gZ29pKHBhdGg9bXVjLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAg',
'ICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIKICAgICAgICAgICAgZXhjZXB0IEV4',
'Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gZiJORU0ge3R5cGUoZSkuX19uYW1l',
'X199IgogICAgaWYga3EuZ2V0KCJQQVRIIGtob25nIG5oYXkiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRv',
'aSBjaHVuZyBkdW9uZyBob25nOiBtdWMgUEFUSCB0aHVvbmcgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgb2sg',
'PSAoa3EuZ2V0KCJQQVRIIGNvIG5oYXkga2VwIikgPT0gIk5IQU4iCiAgICAgICAgICBhbmQga3EuZ2V0KCJQQVRIIHJvbmci',
'KSA9PSAiTm9uZSIgYW5kIGtxLmdldCgiUEFUSCBjaGkga2hvYW5nIHRyYW5nIikgPT0gIk5vbmUiKQogICAgcmV0dXJuIChE',
'QVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKZGVmIGRvX24xMChnb2ksIHNp',
'ZywgdGVwdCk6CiAgICAiIiJNb3QgZGF1ICc7JyB0cm9uZyBURU4gdGh1IG11YyBraG9uZyBkdW9jIGxhbSBtYXQgbXVjIGdp',
'dC5leGUgaG9wIGxlIG8gbXVjIGtpYS4iIiIKICAgIGNvX3NlcCA9IGFueSgoImNhY2giIGluIGspIG9yICgic2VwIiBpbiBr',
'Lmxvd2VyKCkpIGZvciBrIGluIHNpZy5wYXJhbWV0ZXJzKQogICAgaWYgb3MucGF0aHNlcCA9PSAiOyIgYW5kIG5vdCBjb19z',
'ZXA6CiAgICAgICAgcmV0dXJuIChLREQsICJ0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgdmEgaGFtIGtob25n',
'IG5oYW4gdGhhbSBzbyBkYXUgcGhhbiBjYWNoICIKICAgICAgICAgICAgICAgICAgICAgIi0+IGtob25nIHRhY2ggZHVvYyBo',
'YWkgZ2lhIHRodXlldCIsIHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJjbyB0aGFtIHNvIHNlcCI6IGNvX3NlcH0pCiAg',
'ICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUi',
'OyBsYS5ta2RpcigpCiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4',
'dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgciwgXyA9IGdvaShwYXRoPXN0cihsYSkgKyBvcy5wYXRoc2VwICsg',
'c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgIHIwLCBfID0gZ29pKHBhdGg9c3Ry',
'KGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKSAgICAgIyBkb2kgY2h1bmcgZHVvbmcKICAgIGtxID0g',
'eyJjbyBtdWMgY2h1YSAnOyciOiAiTkhBTiIgaWYgciBlbHNlICJOb25lIiwgImRvaSBjaHVuZyAoa2hvbmcgY28gJzsnKSI6',
'ICJOSEFOIiBpZiByMCBlbHNlICJOb25lIn0KICAgIGlmIG5vdCByMDoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5n',
'IGR1b25nIGhvbmciLCBrcQogICAgcmV0dXJuIChEQVQgaWYgciBlbHNlIFRSVU9UKSwgKCIiIGlmIHIgZWxzZSAibXVjIGdp',
'dC5leGUgaG9wIGxlIGJpIE1BVCIpLCBrcQoKZGVmIGRvX24xMShnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJUcnV5ZW4gY2hh',
'bl9kb2FuID0+IHRodSBkdW9jIHRob25nIGJhbyBWQSBzdGRlcnIgSU0uIEtob25nIHRydXllbiA9PiBzdGRlcnIgVkFOIGNv',
'LiIiIgogICAgaWYgImNoYW5fZG9hbiIgbm90IGluIHNpZy5wYXJhbWV0ZXJzOgogICAgICAgIHJldHVybiBLREQsICJfZ2l0',
'X3dpbmRvd3Mga2hvbmcgbmhhbiB0aGFtIHNvIGNoYW5fZG9hbiIsIHsidGhhbSBzbyI6IGxpc3Qoc2lnLnBhcmFtZXRlcnMp',
'fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4o',
'dCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGNkID0g',
'W10KICAgICAgICBfLCBlX2NvID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cp',
'LCBjaGFuX2RvYW49Y2QpCiAgICAgICAgXywgZV9raCA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYp',
'LCBjd2Q9c3RyKGN3KSkKICAgIGtxID0geyJjaGFuX2RvYW4gdGh1IGR1b2MgKG11YykiOiBsZW4oY2QpLAogICAgICAgICAg',
'InN0ZGVyciBraGkgQ08gY2hhbl9kb2FuIChieXRlKSI6IGxlbihlX2NvLmVuY29kZSgpKSwKICAgICAgICAgICJzdGRlcnIg',
'a2hpIEtIT05HIHRydXllbiAoYnl0ZSkiOiBsZW4oZV9raC5lbmNvZGUoKSl9CiAgICBpZiBsZW4oY2QpID09IDAgYW5kIGxl',
'bihlX2toLmVuY29kZSgpKSA9PSAwOgogICAgICAgIHJldHVybiBLREQsICJuaGFuaCAlUHJvZ3JhbUZpbGVzJSBraG9uZyBw',
'aGFuIGdpYWkgS0hPTkcgYmF5IHJhIGNoYW4gZG9hbiBuYW8gLT4gY2h1YSBkbyBkdW9jIiwga3EKICAgIG9rID0gbGVuKGNk',
'KSA+IDAgYW5kIGxlbihlX2NvLmVuY29kZSgpKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPiAwCiAgICByZXR1cm4g',
'KERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgpkZWYgZG9fbjEyKGdvaSwg',
'c2lnLCB0ZXB0KToKICAgICIiIkhhbmcgc2VudGluZWwgZ2l0X3BhdGggdHJvbmcgZml4dHVyZSBwaGFpIHR1eWV0IGRvaSB0',
'cmVuIENBIEhBSSBuZW4uIiIiCiAgICBuZCA9IHRlcHQucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVw',
'bGFjZSIpCiAgICBoYW5nID0gc29ydGVkKHNldChyZS5maW5kYWxsKHInZ2l0X3BhdGhccyo9XHMqIihbXiJdKykiJywgbmQp',
'KSkKICAgIHhhdSA9IFtoIGZvciBoIGluIGhhbmcgaWYgbm90IChQdXJlUG9zaXhQYXRoKGgpLmlzX2Fic29sdXRlKCkgYW5k',
'IFB1cmVXaW5kb3dzUGF0aChoKS5pc19hYnNvbHV0ZSgpKV0KICAgIGtxID0geyJoYW5nIGdpdF9wYXRoIHRpbSB0aGF5Ijog',
'aGFuZywgImNoaSB0dXlldCBkb2kgTU9UIG5lbiI6IHhhdX0KICAgIGlmIG5vdCBoYW5nOgogICAgICAgIHJldHVybiBLREQs',
'ICJraG9uZyB0aW0gdGhheSBoYW5nIGdpdF9wYXRoIG5hbyB0cm9uZyBmaXh0dXJlIC0+IG1hdSBkb2MgY28gdGhlIGRhIGRv',
'aSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgeGF1IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IHhhdSBlbHNlIGYiY2hp',
'LW1vdC1uZW46IHt4YXV9IiksIGtxCgpQUk9CRSA9IFsoIk44IGJ1b2MgMSBjaGkgbmhhbiBnaXQuZXhlIiwgZG9fbjgpLAog',
'ICAgICAgICAoIk45IGJvYyBuaGF5IGtlcCBvIG11YyBQQVRIIiwgZG9fbjkpLAogICAgICAgICAoIk4xMCBkYXUgJzsnIHRy',
'b25nIHRlbiB0aHUgbXVjIiwgZG9fbjEwKSwKICAgICAgICAgKCJOMTEgY2hhbiBkb2FuIGRvaSBrZW5oIiwgZG9fbjExKSwK',
'ICAgICAgICAgKCJOMTIgaGFuZyBzZW50aW5lbCB0dXlldCBkb2kgQ0EgSEFJIG5lbiIsIGRvX24xMildCgojIC0tLSBjaGUg',
'ZG8gVFUgS0lFTTogY2hheSBuYW0gcHJvYmUgdHJlbiBtb3QgY2F5IGJhdCBreSwgbmVuIGJhdCBreSAtLS0KaWYgIi0tdHUt',
'a2llbS1wcm9iZSIgaW4gc3lzLmFyZ3Y6CiAgICBfZyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0tdHUta2ll',
'bS1wcm9iZSIpICsgMV0pLnJlc29sdmUoKQogICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRp',
'b24oImxwX3RrIiwgc3RyKF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICBfbHAgPSBpbXBvcnRsaWIudXRpbC5t',
'b2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX2xwKQogICAgX3NpZyA9IGluc3BlY3Quc2ln',
'bmF0dXJlKF9scC5fZ2l0X3dpbmRvd3MpCiAgICBkZWYgX2dvaSgqKmt3KToKICAgICAgICBlID0gaW8uU3RyaW5nSU8oKQog',
'ICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgICAgIHJldHVybiBfbHAuX2dpdF93',
'aW5kb3dzKCoqa3cpLCBlLmdldHZhbHVlKCkKICAgIHByaW50KGYiVFUgS0lFTSBQUk9CRSB0cmVuIHtfZ30gIChuZW4ge3N5',
'cy5wbGF0Zm9ybX0pIikKICAgIGZvciBfdGVuLCBfZiBpbiBQUk9CRToKICAgICAgICBfdHQsIF9jdCwgX2RsID0gX2YoX2dv',
'aSwgX3NpZywgX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcHJpbnQoZiIgIFt7X3R0OjE0fV0g',
'e190ZW59IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICAgICAgZm9yIF9rLCBfdiBpbiAoX2RsIG9yIHt9',
'KS5pdGVtcygpOiBwcmludChmIiAgICAgICAge19rOjM0fToge192fSIpCiAgICBzeXMuZXhpdCgwKQoKaW5uKCI9IiAqIDc4',
'KTsgaW5uKCJXUDU0MSBnMiAtIHBoZXAgZG8gdHJlbiBXaW5kb3dzIHRoYXQgKHNwZWMgcjM6IE4xLU40LCBOOC1OMTIsIE43',
'LCBraWNoIHRodW9jKSIpOyBpbm4oIj0iICogNzgpCgojIC0tLS0tLS0tLS0tLS0tLS0gdHUga2llbSBibyBkb2MgLS0tLS0t',
'LS0tLS0tLS0tLQpfZCwgX2csIF90ID0gZG9jX2RvKF9NQVUpCl9vayA9IChsZW4oX2QpID09IDIgYW5kIGFueSh4LnN0YXJ0',
'c3dpdGgoInQwMmIiKSBmb3IgeCBpbiBfZCkKICAgICAgIGFuZCBub3QgYW55KHguc3RhcnRzd2l0aCgidDEzMSIpIGZvciB4',
'IGluIF9kKSBhbmQgX3QpCmlubigiVHUga2llbSBibyBkb2MgbG9nOiIsIERBVCBpZiBfb2sgZWxzZSBUUlVPVCkKaWYgbm90',
'IF9vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogYm8gZG9jIGxvZyBjdWEgY2hpbmggc2NyaXB0IG5heSBz',
'YWkgLT4ga2hvbmcgZG8gZ2kgY2EuIik7IHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMC4gbmVuIGRvIC0tLS0t',
'LS0tLS0tLS0tLS0KZ29jID0gUGF0aChzeXMuYXJndlsxXSkucmVzb2x2ZSgpIGlmIGxlbihzeXMuYXJndikgPiAxIGVsc2Ug',
'UGF0aC5jd2QoKQp0ZXAsIHRlcHQgPSBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoLnB5IiwgZ29jIC8gIm9wcyIgLyAi',
'bGVhc2VfcHVibGlzaF90ZXN0LnB5Igppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjAuIE5FTiBETyIpCmlubigiICBz',
'eXMucGxhdGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwgInwgcHl0aG9uIiwgc3lzLnZlcnNpb24uc3BsaXQoKVswXSkKaW5uKCIg',
'IG9zLnBhdGhzZXAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSwgInwgUEFUSEVYVDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQ',
'QVRIRVhUIikpWzo2MF0pCmlubigiICBQcm9ncmFtRmlsZXMgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlByb2dyYW1GaWxl',
'cyIpKSwgInwgU3lzdGVtUm9vdDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290IikpKQppbm4oIiAgQ09OR19D',
'VV9HSVQgIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJDT05HX0NVX0dJVCIpKSkKaW5uKCIgIGdvYyBraG8gICAgICA6Iiwg',
'Z29jKQoKcXV5ZW4gPSBOb25lCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAgIGltcG9ydCBj',
'dHlwZXM7IHF1eWVuID0gYm9vbChjdHlwZXMud2luZGxsLnNoZWxsMzIuSXNVc2VyQW5BZG1pbigpKQogICAgZXhjZXB0IEV4',
'Y2VwdGlvbjogcXV5ZW4gPSBOb25lCmdoaSgicXV5ZW5fYWRtaW4iLCBxdXllbikKc3ltbGlua19kdW9jID0gTm9uZQp0cnk6',
'CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgodCkvImEudHh0',
'IjsgZC53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICB0cnk6IG9zLnN5bWxpbmsoc3RyKGQpLCBz',
'dHIoUGF0aCh0KS8ibGsiKSk7IHN5bWxpbmtfZHVvYyA9IFRydWUKICAgICAgICBleGNlcHQgT1NFcnJvciBhcyBlOiBzeW1s',
'aW5rX2R1b2MgPSBGYWxzZTsgZ2hpKCJzeW1saW5rX2xvaSIsIGYie3R5cGUoZSkuX19uYW1lX199OiB7ZX0iKQpleGNlcHQg',
'RXhjZXB0aW9uIGFzIGU6IGdoaSgic3ltbGlua19sb2kiLCBzdHIoZSkpCmdoaSgic3ltbGlua19kdW9jIiwgc3ltbGlua19k',
'dW9jKQppbm4oIiAgQWRtaW5pc3RyYXRvcjoiLCBxdXllbiwgInwgdGFvIHN5bWxpbmsgZHVvYzoiLCBzeW1saW5rX2R1b2Mp',
'Cgpsb2kgPSBbXQojIENvbmcga2ljaCB0aHVvYyBsYSBwaGVwIGRvIHRyZW4gTElDSCBTVSBHSVQsIGtob25nIGRpbmggZ2kg',
'ZGVuIG5lbi4gQ2hvIHBoZXAKIyAtLWNoaS1raWNoLXRodW9jIGNoYXkgbyBtb2kgbmVuIGRlIGNvbiBUVSBLSUVNIGR1b2Mg',
'Y2hpbmggY29uZyBuYXkgKGRhIGR1bmcKIyBkZSB0YWkgZHVuZyBjYSBoYWkgdmUgY3VhIHN1IGNvIG5lbi1jdSAxOS0wOSku',
'IE1vaSBjaG90IENIVUMgTkFORyB2YW4gZG9pIFdpbmRvd3MuCmlmIHN5cy5wbGF0Zm9ybSAhPSAid2luMzIiIGFuZCAiLS1j',
'aGkta2ljaC10aHVvYyIgbm90IGluIHN5cy5hcmd2OgogICAgbG9pLmFwcGVuZChmIktIT05HIHBoYWkgV2luZG93cyAoc3lz',
'LnBsYXRmb3JtPXtzeXMucGxhdGZvcm0hcn0pIikKaWYgbm90IHRlcC5pc19maWxlKCk6ICBsb2kuYXBwZW5kKGYia2hvbmcg',
'dGhheSB7dGVwfSIpCmlmIG5vdCB0ZXB0LmlzX2ZpbGUoKTogbG9pLmFwcGVuZChmImtob25nIHRoYXkge3RlcHR9IikKaWYg',
'bm90IHNodXRpbC53aGljaCgiZ2l0Iik6IGxvaS5hcHBlbmQoImtob25nIGNvIGBnaXRgIHRyb25nIFBBVEgiKQoKcmMsIGhl',
'YWQsIF8gPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIkhFQUQiKQppZiByYzogbG9pLmFwcGVuZCgia2hvbmcgZG9jIGR1b2Mg',
'SEVBRCIpCmdoaSgiaGVhZCIsIGhlYWQpCnJjX2EsIF8sIF8gPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICItLWlzLWFuY2Vz',
'dG9yIiwgU0hBX0cxLCBoZWFkIG9yICJIRUFEIikKbGFfaGF1X2R1ZSA9IChyY19hID09IDApCmlmIGhlYWQgPT0gU0hBX0cx',
'OgogICAgdGhlX2hlID0gImcxIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBEQVkgTEEgZzEuIENIVUEgY28gYmFu',
'IHZhIGcyOyBrZXQgcXVhIGR1b2kgbGEgTkVOIERPLiIpCmVsaWYgbGFfaGF1X2R1ZToKICAgIHRoZV9oZSA9ICJnMiI7IGlu',
'bihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gaGF1IGR1ZSBjdWEgZzEgKHtTSEFfRzFbOjhdfSk6IHVuZyB2aWVuIGcyLiIp',
'CmVsc2U6CiAgICB0aGVfaGUgPSAiPyI7IGxvaS5hcHBlbmQoZiJIRUFEPXtoZWFkWzo4XX0gS0hPTkcgcGhhaSBnMSB2YSBL',
'SE9ORyBwaGFpIGhhdSBkdWUgY3VhIHtTSEFfRzFbOjhdfSDigJQgcmViYXNlPyBuaGFtIG5oYW5oPyIpCmdoaSgidGhlX2hl',
'IiwgdGhlX2hlKQoKaWYgbG9pOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBuZW4gZG8gc2FpLCBLSE9ORyBp',
'biBrZXQgbHVhbiBuYW8uIikKICAgIGZvciB4IGluIGxvaTogaW5uKCIgIC0iLCB4KQogICAgc3lzLmV4aXQoMykKCiMgLS0t',
'LS0tLS0tLS0tLS0tLSAxLiBraWNoIHRodW9jIChONycgY3VhIHNwZWMgcjMpIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsg',
'aW5uKCItIiAqIDc4KTsgaW5uKCIxLiBLSUNIIFRIVU9DIOKAlCB0cmFuIHNwZWMgcjM6IDw9IDIgdGVwIHZhIDw9IDQwMCBk',
'b25nIHRoZW0iKQojIFZFIE5FTiBQSEFJIFRVT0kg4oCUIHZhIHBoYWkgQ0hVTkcgTUlOSCBkdW9jIGxhIHR1b2ksIGtob25n',
'IHBoYWkgZ2lhIGRpbmguCiMgQmFpIGhvYyB0cmEgZ2lhIDE5LTA5LTIwMjY6IGNsb25lIHRhaSBkdW5nIGNoaSBmZXRjaCBu',
'aGFuaCBiYW4gdmEsIGBvcmlnaW4vbWFzdGVyYAojIGR1bmcgeWVuIHR1IDE0LTA5IChjMTZiZDMyLCBzYXUgOTcgY29tbWl0',
'KS4gbWVyZ2UtYmFzZSByb2kgdmUgZHVuZyBkaW5oIG1hc3RlciBjdSwKIyBuZW4gZGlmZiBOVU9UIGNhIDk3IGNvbW1pdCBt',
'YXN0ZXI6IGRvIHJhIDQ2IHRlcCAvICs3MTE4IHRoYXkgdmkgMiB0ZXAgLyArMzk3IOKAlAojIENVTkcgTU9UIENPTU1JVCAw',
'ZWE5NWRlLiBNb3QgdGlldSBjaGkgREVMVEEgbWEgdmUgbmVuIGtob25nIHR1b2kgdGhpIGtob25nIHNhaQojIGxlY2ggbW90',
'IGNodXQsIG5vIHNhaSBjYSBtb3QgYmFjIGRvIGxvbi4KIyBDaG8gbmVuOiBuZW4ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGxh',
'IHR1b2kgPT4gS0hPTkcgRE8gRFVPQyAocmM9MyksIEtIT05HIHBoYWkgVFJVT1QuCiMgVFJVT1QgbGEgbW90IFBIQU4gUVVZ',
'RVQgdmUgYmFuIHZhOyBwaGFuIHF1eWV0IGNoaSBkdW9jIHBoZXAgcGhhdCByYSBraGkgZGEgZG8gZHVvYy4KcmNfbHIsIG91',
'dF9sciwgZXJfbHIgPSBnaXQoZ29jLCAibHMtcmVtb3RlIiwgIm9yaWdpbiIsICJyZWZzL2hlYWRzL21hc3RlciIpCnJjX2xt',
'LCBsbSwgZXJfbG0gICAgID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJvcmlnaW4vbWFzdGVyIikKcm0gPSBvdXRfbHIuc3Bs',
'aXQoKVswXSBpZiAobm90IHJjX2xyIGFuZCBvdXRfbHIuc3RyaXAoKSkgZWxzZSAiIgppZiBub3Qgcm06CiAgICBrZXQoIk43',
'JyBraWNoIHRodW9jIiwgS0RELAogICAgICAgIGYia2hvbmcgaG9pIGR1b2MgbWFzdGVyIHRyZW4gcmVtb3RlIChscy1yZW1v',
'dGUgcmM9e3JjX2xyfSk6IHtlcl9scls6NjBdfSAiCiAgICAgICAgZiLigJQga2hvbmcgY2h1bmcgbWluaCBkdW9jIHZlIG5l',
'biBjb24gdHVvaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIHJjX2xtIG9yIG5vdCBsbToK',
'ICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgZG9jIGR1b2Mgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9u',
'ZToge2VyX2xtWzo2MF19IikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbG0gIT0gcm06CiAg',
'ICAjIERlbSB4ZW0gdHV0IGxhaSBiYW8geGEsIG5ldSBkZW0gZHVvYyDigJQgY29uIHNvIG5heSBub2kgcm8gbXVjIGRvIHNh',
'aSBsZWNoLgogICAgcmNfYywgc2F1LCBfID0gZ2l0KGdvYywgInJldi1saXN0IiwgIi0tY291bnQiLCBmIntsbX0uLntybX0i',
'KQogICAgeGEgPSBmIiwgdHV0IGxhaSB7c2F1fSBjb21taXQiIGlmIChub3QgcmNfYyBhbmQgc2F1LnN0cmlwKCkuaXNkaWdp',
'dCgpKSBlbHNlICIiCiAgICBpbm4oZiIgIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmUgOiB7bG1bOjEyXX0iKQogICAgaW5u',
'KGYiICBtYXN0ZXIgdHJlbiByZW1vdGUgICAgICAgIDoge3JtWzoxMl19e3hhfSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIs',
'IGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAogICAgICAgIGYi',
'dmUgbmVuIENVOiBvcmlnaW4vbWFzdGVyPXtsbVs6MTJdfSAhPSByZW1vdGU9e3JtWzoxMl19e3hhfSAiCiAgICAgICAgZiLi',
'gJQgY2hheSBgZ2l0IC1DIDxraG8+IGZldGNoIG9yaWdpbiBtYXN0ZXJgIHJvaSBkbyBsYWkiKQogICAgcmNfbWIsIG1iLCBu',
'cywgcmMgPSAxLCAiIiwgIiIsIDEKZWxzZToKICAgIGlubihmIiAgdmUgbmVuIFRVT0k6IG9yaWdpbi9tYXN0ZXIgPSB7bG1b',
'OjEyXX0gPT0gbWFzdGVyIHRyZW4gcmVtb3RlIikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9y',
'ZW1vdGUiLCBybSkKICAgIHJjX21iLCBtYiwgZXJfbWIgPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICJvcmlnaW4vbWFzdGVy',
'IiwgaGVhZCkKaWYgcmNfbWIgb3Igbm90IG1iOgogICAgaWYgbWIgPT0gIiIgYW5kIHJtIGFuZCBsbSA9PSBybToKICAgICAg',
'ICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25nIHRpbmggZHVvYyBtZXJnZS1iYXNlIHZvaSBvcmlnaW4vbWFz',
'dGVyOiB7ZXJfbWJbOjcwXX0iKQogICAgbnMsIHJjID0gIiIsIDEKZWxzZToKICAgIGdoaSgibWVyZ2VfYmFzZSIsIG1iKQog',
'ICAgaW5uKGYiICBtZXJnZS1iYXNlKG9yaWdpbi9tYXN0ZXIsIEhFQUQpID0ge21iWzoxMl19IikKICAgIGlmIG1iICE9IFNI',
'QV9CQVNFX1NQRUM6CiAgICAgICAgaW5uKGYiICBMVVUgWToga2hhYyBiYXNlIG1hIHNwZWMgcjMga2hhaSAoe1NIQV9CQVNF',
'X1NQRUNbOjEyXX0pIOKAlCB2aSBuaGFuaCBkYSBtZXJnZSBtYXN0ZXIuIikKICAgICAgICBpbm4oZiIgICAgICAgICBEbyBz',
'byBiYXNlIGN1IHNlIE5VT1QgcGhhbiBtYXN0ZXIgbWFuZyB2YW8uIER1bmcgbWVyZ2UtYmFzZSBtb2kgbGEgdmllYyBjdWEg',
'ZXhlY3V0b3IuIikKICAgICAgICByY194LCBuc194LCBfID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgU0hBX0JB',
'U0VfU1BFQywgaGVhZCkKICAgICAgICBpZiBub3QgcmNfeDoKICAgICAgICAgICAgaCA9IFtsLnNwbGl0KCJcdCIpIGZvciBs',
'IGluIG5zX3guc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgICAgICAgICAgYSA9IHN1bShpbnQoeFswXSkgZm9yIHgg',
'aW4gaCBpZiB4WzBdLmlzZGlnaXQoKSkKICAgICAgICAgICAgZ2hpKCJudW1zdGF0X3RoZW9fYmFzZV9zcGVjIiwgeyJ0ZXAi',
'OiBsZW4oaCksICJ0aGVtIjogYX0pCiAgICAgICAgICAgIGlubihmIiAgICAgICAgIChkb2kgY2hpZXU6IHNvIGJhc2Ugc3Bl',
'YyA9IHtsZW4oaCl9IHRlcCAvICt7YX0g4oCUIGNvbiBzbyBheSBLSE9ORyBkdW5nIGRlIGNoYW0pIikKICAgIHJjLCBucywg',
'ZXIgPSBnaXQoZ29jLCAiZGlmZiIsICItLW51bXN0YXQiLCBtYiwgaGVhZCkKaWYgcmM6CiAgICBwYXNzCmVsc2U6CiAgICBo',
'YW5nID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnMuc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgIHRoZW0gPSBz',
'dW0oaW50KGhbMF0pIGZvciBoIGluIGhhbmcgaWYgaFswXS5pc2RpZ2l0KCkpCiAgICB4b2EgID0gc3VtKGludChoWzFdKSBm',
'b3IgaCBpbiBoYW5nIGlmIGhbMV0uaXNkaWdpdCgpKQogICAgZ2hpKCJzb190ZXAiLCBsZW4oaGFuZykpOyBnaGkoImRvbmdf',
'dGhlbSIsIHRoZW0pOyBnaGkoImRvbmdfeG9hIiwgeG9hKQogICAgZm9yIGggaW4gaGFuZzogaW5uKGYiICAgIHtoWzJdOjM0',
'fSAre2hbMF06PDV9IC17aFsxXX0iKQogICAgaW5uKGYiICAgIFRPTkc6IHtsZW4oaGFuZyl9IHRlcCwgK3t0aGVtfSwgLXt4',
'b2F9ICAgKHRyYW46IHtUUkFOX1RFUH0gdGVwIC8ge1RSQU5fRE9OR30gZG9uZyB0aGVtKSIpCiAgICBrZXQoIk43JyBraWNo',
'IHRodW9jIiwgREFUIGlmIChsZW4oaGFuZykgPD0gVFJBTl9URVAgYW5kIHRoZW0gPD0gVFJBTl9ET05HKSBlbHNlIFRSVU9U',
'LAogICAgICAgIGYie2xlbihoYW5nKX0gdGVwIC8gK3t0aGVtfSIpCgojIENvbmcgbmhhbmg6IGRvIFJJRU5HIGtpY2ggdGh1',
'b2MgKHZhaSBnaWF5KSByb2kgZHVuZy4gRHVuZyBraGkgY2FuIHhhYyBtaW5oIGxhaQojIHZlIG5lbiBtYSBraG9uZyBtdW9u',
'IHRyYSAyMC00NSBwaHV0IGNobyBjYSBibyB0ZXN0LgppZiAiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Y6CiAgICBp',
'bm4oIiIpOyBpbm4oIj0iICogNzgpCiAgICBpbm4oIi0tY2hpLWtpY2gtdGh1b2M6IENISSBkbyBjb25nIGtpY2ggdGh1b2Mu',
'IERheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5naGllbSB0aHUuIikKICAgIGlubigiLSIgKiA3OCkKICAgIGZvciBfdCwgX3R0',
'LCBfY3QgaW4gY2hvdDogaW5uKGYiICB7X3R0OjE0fSB7X3R9IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAg',
'ICBfayA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCiAgICBfciA9IHN1bSgxIGZvciBfLCB0LCBf',
'IGluIGNob3QgaWYgdCA9PSBUUlVPVCkKICAgIHN5cy5leGl0KDMgaWYgX2sgZWxzZSAoMSBpZiBfciBlbHNlIDApKQoKIyAt',
'LS0tLS0tLS0tLS0tLS0tIDIuIGJvIHRlc3QgZGF5IGR1IC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4',
'KTsgaW5uKCIyLiBCTyBURVNUIERBWSBEVSAoMTAtNDAgcGh1dCkiKQpyY19uLCBvdXRfbiA9IGNoYXkoWyJvcHMvbGVhc2Vf',
'cHVibGlzaF90ZXN0LnB5Il0sIGdvYykKZ2hpKCJyY19zdWl0ZSIsIHJjX24pCm0gPSBSWF9UT05HLnNlYXJjaChvdXRfbikK',
'aW5uKCIgIHJjID0iLCByY19uLCAifCIsIG0uZ3JvdXAoMCkgaWYgbSBlbHNlICIoS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25n',
'IGtldCkiKQppZiBtOgogICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGkoInRyZW4iLCBpbnQobS5ncm91cCgy',
'KSkpOyBnaGkoImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKZG9faGV0LCBnYywgdGluID0gZG9jX2RvKG91dF9uKQpn',
'aGkoInNvX2NhX2RvIiwgbGVuKGRvX2hldCkpOyBnaGkoImxpZXRfa2VfZGF5X2R1IiwgdGluKQpmb3IgZyBpbiBnYzogaW5u',
'KCIgICAqIiwgZykKaW5uKCIiKTsgaW5uKGYiICA9PT0ge2xlbihkb19oZXQpfSBDQSBETyA9PT0iKQpmb3IgdCBpbiBzb3J0',
'ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgaW5uKGYiICAge3Quc3BsaXQoJ18nKVswXTo3fSB7dH0iKTsgaW5uKGYiICAg',
'ICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCmdoaSgiZG9fbHlfZG8iLCB7dDogZG9faGV0W3RdWzozMDBdIGZvciB0IGlu',
'IGRvX2hldH0pCiMgLS0tLSBDSE9UOiBtb2kgY2EgRE8gcGhhaSBHSUFJIFRISUNIIERVT0MgLS0tLQojIFRoaWV1IGNob3Qg',
'bmF5LCBibyBkbyBpbiBkYW5oIHNhY2ggZG8gcm9pIHZhbiB0aG9hdCByYz0wLiBEbyBkdW5nIGxhIGxvaSBkYSB4YXkgcmE6',
'CiMgbHVvdCBXaW5kb3dzIDE5LTA5IGNvIHQxNzEgRE8gbWEgYm8gZG8gYmFvICJEQVQgMTAgfCBUUlVPVCAwIiB2YSByYz0w',
'LgpkZWYgX2tob2EodCk6IHJldHVybiB0LnNwbGl0KCJfIilbMF0KZG9fcGFja2V0LCBkb19sYSwgZG9fdGhpZXVfY29uZ19j',
'dSA9IFtdLCBbXSwgW10KZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgIGssIGx5ID0gX2tob2EodCks',
'IGRvX2hldFt0XQogICAgaWYgayBpbiBDQV9QQUNLRVQ6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fcGFja2V0',
'LmFwcGVuZCh0KQogICAgZWxpZiAiS0jDlE5HIMSQTyDEkMav4buiQyIgaW4gbHkgb3IgInRoaeG6v3UgYCIgaW4gbHk6ICBk',
'b190aGlldV9jb25nX2N1LmFwcGVuZCh0KQogICAgZWxpZiBrIGluIE5HT0FJX1BIQU1fVkk6ICAgICAgICAgICAgICAgICAg',
'ICAgICAgcGFzcwogICAgZWxzZTogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fbGEuYXBw',
'ZW5kKHQpCmdoaSgiZG9fcGFja2V0IiwgZG9fcGFja2V0KTsgZ2hpKCJkb19sYSIsIGRvX2xhKTsgZ2hpKCJkb190aGlldV9j',
'b25nX2N1IiwgZG9fdGhpZXVfY29uZ19jdSkKaW5uKCIiKQppbm4oZiIgIGNhIERPIHRodW9jIENISU5IIHBhY2tldCBuYXkg',
'OiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF0gb3IgJ2tob25nIGNvJ30iKQppbm4oZiIgIGNhIERPIG5nb2FpIHBo',
'YW0gdmkgKHIzIGtoYWkpOiB7W19raG9hKHgpIGZvciB4IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSkgaWYgX2tob2Eo',
'eCkgaW4gTkdPQUlfUEhBTV9WSV19IikKaW5uKGYiICBjYSBETyB2aSBUSElFVSBDT05HIENVICAgICAgIDoge1tfa2hvYSh4',
'KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XSBvciAna2hvbmcgY28nfSIpCmlubihmIiAgY2EgRE8gTEEgKGtob25nIGdp',
'YWkgdGhpY2ggZHVvYyk6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdIG9yICdraG9uZyBjbyd9IikKa2V0KCJLaG9uZyBj',
'YSBuYW8gY3VhIFBBQ0tFVCBiaSBETyIsIERBVCBpZiBub3QgZG9fcGFja2V0IGVsc2UgVFJVT1QsCiAgICAiIiBpZiBub3Qg',
'ZG9fcGFja2V0IGVsc2UgZiJETzoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdfSDigJQgYmFuIHZhIENIVUEgeG9u',
'ZyIpCmtldCgiTW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MiLCBEQVQgaWYgbm90IGRvX2xhIGVsc2UgVFJVT1QsCiAg',
'ICAiIiBpZiBub3QgZG9fbGEgZWxzZSBmImxhOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXX0iKQppZiBkb190aGlldV9j',
'b25nX2N1OgogICAga2V0KCJDb25nIGN1IGRheSBkdSBkZSBkbyIsIEtERCwgZiJ0aGlldSBjb25nIGN1IGNobyB7W19raG9h',
'KHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdfSIpCgpicSA9IHNvcnRlZCh7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEu',
'ZmluZGFsbChvdXRfbil9LCBrZXk9c29fY2EpOyBnaGkoImNhX2JvX3F1YSIsIGJxKQppbm4oIiIpOyBpbm4oZiIgIEJPIFFV',
'QSAoe2xlbihicSl9KToge1t4LnNwbGl0KCdfJylbMF0gZm9yIHggaW4gYnFdfSIpCgppbm4oIiIpOyBpbm4oIiAgTjEtTjQg',
'KHQxNjUtdDE2OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBuYXkgbGEgY2hpIGJhbyBob2kgcXV5OiIpCmI0ID0g',
'e3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0FNT0l9OyBnaGkoImNhX21vaSIsIGI0KQpmb3IgdCBpbiBDQU1PSTog',
'aW5uKGYiICAgICB7dH06IHtiNFt0XX0iKQprZXQoIk4xLU40ICh0MTY1LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJRVUEi',
'IGZvciB2IGluIGI0LnZhbHVlcygpKQogICAgZWxzZSAoS0REIGlmIGFueSh2IGlzIE5vbmUgZm9yIHYgaW4gYjQudmFsdWVz',
'KCkpIGVsc2UgVFJVT1QpLCBzdHIoYjQpKQoKaW5uKCIiKTsgaW5uKCIgIDE1IGNhIHR1bmcgZG8gdHJlbiBDSToiKQpiMTUg',
'PSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQppbm4oIiAgICAiICsgIiAg',
'Ii5qb2luKGYie3R9OntiMTVbdF19IiBmb3IgdCBpbiBDQTE1KSkKCiMgdDEzNiDigJQgTjEyIGRvIEdJQU4gVElFUCBxdWEg',
'a2V0IHF1YSBjYQp0MTM2X3RlbiA9IG5leHQoKHQgZm9yIHQgaW4gZG9faGV0IGlmIHQuc3RhcnRzd2l0aCgidDEzNiIpKSwg',
'Tm9uZSkKaWYgYjE1LmdldCgidDEzNiIpID09ICJRVUEiOgogICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwg',
'REFULCAidDEzNiBRVUEiKQplbGlmIGIxNS5nZXQoInQxMzYiKSBpcyBOb25lOgogICAga2V0KCJOMTIgdDEzNiAocXVhIGtl',
'dCBxdWEgY2EpIiwgS0RELCAia2hvbmcgdGhheSB0MTM2IHRyb25nIGxvZyIpCmVsc2U6CiAgICBseSA9IGRvX2hldC5nZXQo',
'dDEzNl90ZW4sICIiKQogICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgVFJVT1QsIGYiRE86IHtseVs6OTBd',
'fSIpCgojIC0tLS0tLS0tLS0tLS0tLS0gMy4gcHJvYmUgVEhBTkcgdmFvIGhhbSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7',
'IGlubigiLSIgKiA3OCk7IGlubigiMy4gUFJPQkUgVEhBTkcg4oCUIGdvaSBfZ2l0X3dpbmRvd3Mgdm9pIHRoYW0gc28gdGll',
'bSIpCnNwZWMgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHA1NDEiLCBzdHIodGVwKSkKbHAg',
'PSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMpOyBzcGVjLmxvYWRlci5leGVjX21vZHVsZShscCkKc2ln',
'ID0gaW5zcGVjdC5zaWduYXR1cmUobHAuX2dpdF93aW5kb3dzKQpnaGkoInRoYW1fc29fX2dpdF93aW5kb3dzIiwgbGlzdChz',
'aWcucGFyYW1ldGVycykpCmlubigiICB0aGFtIHNvIGN1YSBfZ2l0X3dpbmRvd3M6IiwgbGlzdChzaWcucGFyYW1ldGVycykp',
'CgpkZWYgZ29pKCoqa3cpOgogICAgIiIiR29pIF9naXRfd2luZG93cywgQkFUIHN0ZGVyciBkZSBtb3QgZG9uZyBjaGFuIGRv',
'YW4ga2hvbmcgZ2lldCBsdW90IGRvLiIiIgogICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgIHdpdGggY29udGV4dGxpYi5yZWRp',
'cmVjdF9zdGRlcnIoZSk6CiAgICAgICAgciA9IGxwLl9naXRfd2luZG93cygqKmt3KQogICAgcmV0dXJuIHIsIGUuZ2V0dmFs',
'dWUoKQoKIyAtLS0gZG9pIGNodW5nIHJpZzogcGhhaSB0cmEgbG9pIGR1bmcgbW90IGNhIHRhIEJJRVQgVFJVT0MgZGFwIGFu',
'IC0tLQp3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICBuZ29haSA9IFBhdGgodCkvIm5nb2Fp',
'IjsgbmdvYWkubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYu',
'bWtkaXIoKQogICAgKG5nb2FpLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMSwg',
'XyA9IGdvaShwYXRoPXN0cihuZ29haSksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAoY3cvImdp',
'dC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIyLCBfID0gZ29pKHBhdGg9c3RyKGN3KSwg',
'cHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKcmlnX29rID0gYm9vbChyMSkgYW5kIHIyIGlzIE5vbmUKZ2hp',
'KCJyaWdfZG9pX2NodW5nIiwgcmlnX29rKQprZXQoIlJJRyBkb2kgY2h1bmcgKGJpZXQgdHJ1b2MgZGFwIGFuKSIsIERBVCBp',
'ZiByaWdfb2sgZWxzZSBLREQsCiAgICBmIm5nb2FpLWN3ZC0+eydOSEFOJyBpZiByMSBlbHNlICdOb25lJ30gfCB0cm9uZy1j',
'd2QtPnsnTkhBTicgaWYgcjIgZWxzZSAnTm9uZSd9IikKaWYgbm90IHJpZ19vazoKICAgIGlubigiIik7IGlubigiS0hPTkcg',
'RE8gRFVPQzogcmlnIHNhaSwgbW9pIGNob3QgZHVvaSBzZSB2byBuZ2hpYS4iKTsgc3lzLmV4aXQoMykKCmZvciB0ZW4sICh0',
'dCwgY3QsIGRsKSBpbiBbKHQsIGYoZ29pLCBzaWcsIHRlcHQpKSBmb3IgdCwgZiBpbiBQUk9CRV06CiAgICBnaGkoInByb2Jl',
'XyIgKyB0ZW4uc3BsaXQoKVswXS5sb3dlcigpLCBkbCkKICAgIGlmIGlzaW5zdGFuY2UoZGwsIGRpY3QpOgogICAgICAgIGZv',
'ciBrLCB2IGluIGRsLml0ZW1zKCk6IGlubihmIiAgICB7azozNH06IHt2fSIpCiAgICBrZXQodGVuLCB0dCwgY3QpCgojIC0t',
'LS0tLS0tLS0tLS0tLS0gNC4gTjcgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7',
'IGlubigiLSIgKiA3OCk7IGlubigiNC4gTjcg4oCUIGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gKGNheSB0aGF0IEtIT05H',
'IGJpIGR1bmcgdG9pKSIpCnRydW9jID0gdGVwLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKQpn',
'aGkoIm43X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIgIHNvIGRvbmcga2hvcCB7TUFVX1dJTiFyfTogVFJVT0MgPSB7dHJ1b2N9',
'IFttb25nIDFdIikKaWYgdHJ1b2MgIT0gMToKICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgZiJt',
'YXUgeHVhdCBoaWVuIHt0cnVvY30gbGFuLCBraG9uZyBwaGFpIDEiKQplbHNlOgogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3Jh',
'cnlEaXJlY3RvcnkoKSBhcyB0bXA6CiAgICAgICAgc2FvID0gUGF0aCh0bXApLyJjYXkiCiAgICAgICAgc2h1dGlsLmNvcHl0',
'cmVlKGdvYywgc2FvLCBpZ25vcmU9c2h1dGlsLmlnbm9yZV9wYXR0ZXJucygiLmdpdCIsICJfX3B5Y2FjaGVfXyIsICIqLnB5',
'YyIpKQogICAgICAgIGYyID0gc2FvLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IgogICAgICAgIGYyLndyaXRlX3RleHQoZjIu',
'cmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJlcGxhY2UoTUFVX1dJTiwgImlmIEZhbHNlOiIpLCBlbmNvZGluZz0idXRm',
'LTgiKQogICAgICAgIHNhdSA9IGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKTsgZ2hpKCJu',
'N19zYXUiLCBzYXUpCiAgICAgICAgaW5uKGYiICBTQVUgKGRhIGRvdCBiaWVuKSA9IHtzYXV9IFttb25nIDBdIikKICAgICAg',
'ICBpZiBzYXUgIT0gMDoKICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCAiZG90IGJp',
'ZW4gS0hPTkcgYXAgZHVvYyIpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgcmNfbSwgb3V0X20gPSBjaGF5KFsib3BzL2xl',
'YXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBzYW8pCiAgICAgICAgICAgIG0xNjUgPSBtYXVfY2Eob3V0X20sICJ0MTY1Iik7IGRt',
'LCBfLCBfID0gZG9jX2RvKG91dF9tKQogICAgICAgICAgICB0ZW4xNjUgPSBuZXh0KCh0IGZvciB0IGluIGRtIGlmIHQuc3Rh',
'cnRzd2l0aCgidDE2NSIpKSwgTm9uZSkKICAgICAgICAgICAgbHkgPSAoZG0uZ2V0KHRlbjE2NSkgb3IgIiIpCiAgICAgICAg',
'ICAgIGdoaSgibjdfdDE2NSIsIG0xNjUpOyBnaGkoIm43X2x5X2RvIiwgbHlbOjIwMF0pCiAgICAgICAgICAgIGlubihmIiAg',
'dDE2NSBzYXUgZG90IGJpZW46IHttMTY1fSB8IHtseVs6MTEwXX0iKQogICAgICAgICAgICBkdW5nX2x5X2RvID0gIlBBVEgg',
'dCIgaW4gbHkgb3IgIi91c3IvYmluIiBpbiBseQogICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3Mi',
'LCBEQVQgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykgZWxzZQogICAgICAgICAgICAgICAgKFRSVU9UIGlmIG0x',
'NjUgPT0gIkRPIiBlbHNlIEtERCksCiAgICAgICAgICAgICAgICAiZ2lldCBkdW5nIGx5IGRvIiBpZiAobTE2NSA9PSAiRE8i',
'IGFuZCBkdW5nX2x5X2RvKQogICAgICAgICAgICAgICAgZWxzZSAoIkRPIG5odW5nIEtIT05HIGR1bmcgbHkgZG8gLT4gdGlu',
'IGR1bmcgZ2lhIiBpZiBtMTY1ID09ICJETyIgZWxzZSAia2hvbmcgZG9jIGR1b2MgdDE2NSIpKQoKIyAtLS0tLS0tLS0tLS0t',
'LS0tIEtFVCBMVUFOIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQppbm4oZiJUSEUgSEUgRE8gRFVP',
'Qzoge3RoZV9oZX0gICBIRUFEPXtoZWFkWzoxMl19IikKaWYgdGhlX2hlID09ICJnMSI6CiAgICBpbm4oIkxVVSBZOiBkYXkg',
'bGEgTkVOIERPIChnMSksIEtIT05HIHBoYWkgbmdoaWVtIHRodSBnMi4gQ2FjIGNob3QgTjgtTjEyIGR1b2kgZGF5IikKICAg',
'IGlubigiICAgICAgIFRSVU9UIGxhIERVTkcgTkhVIE1PTkcg4oCUIGNodW5nIGxhIG5odW5nIGxvIGcyIHNpbmggcmEgZGUg',
'dsOhLiIpCmlubigiLSIgKiA3OCkKZm9yIHRlbiwgdHQsIGN0IGluIGNob3Q6CiAgICBpbm4oZiIgIHt0dDoxNH0ge3Rlbn0i',
'ICsgKGYiICAge2N0fSIgaWYgY3QgZWxzZSAiIikpCm5fa2RkID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09',
'IEtERCkKbl90cnVvdCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKaW5uKCItIiAqIDc4KQpp',
'bm4oZiIgIERBVCB7c3VtKDEgZm9yIF8sdCxfIGluIGNob3QgaWYgdD09REFUKX0gfCBUUlVPVCB7bl90cnVvdH0gfCBLSE9O',
'RyBETyBEVU9DIHtuX2tkZH0iKQppbm4oZiIgIFRvbmcgY2EgZG86IHtzby5nZXQoJ3NvX2NhX2RvJyl9IHwgZGFuaCBzYWNo',
'IGRheSBkdTogeydDTycgaWYgc28uZ2V0KCdsaWV0X2tlX2RheV9kdScpIGVsc2UgJ0tIT05HIERPIERVT0MnfSIpCmlubihm',
'IiAgQWRtaW5pc3RyYXRvcjoge3NvLmdldCgncXV5ZW5fYWRtaW4nKX0gfCBzeW1saW5rOiB7c28uZ2V0KCdzeW1saW5rX2R1',
'b2MnKX0iKQppbm4oIiIpOyBpbm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kgSlNPTiBOQVkgVkUgQ0hPIFJFVklFV0VSIC0tLSIp',
'CmdoaSgiY2hvdCIsIFt7InRlbiI6IGEsICJ0cmFuZ190aGFpIjogYiwgImNoaV90aWV0IjogY30gZm9yIGEsIGIsIGMgaW4g',
'Y2hvdF0pCmlubihqc29uLmR1bXBzKHNvLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0xLCBkZWZhdWx0PXN0cikpCiMg',
'cmM6IDAgPSBtb2kgY2hvdCBEQVQgfCAxID0gY28gY2hvdCBUUlVPVCB8IDMgPSBjbyBjaG90IEtIT05HIERPIERVT0MgKHV1',
'IHRpZW4gYmFvIGRvbmcpCnN5cy5leGl0KDMgaWYgbl9rZGQgZWxzZSAoMSBpZiBuX3RydW90IGVsc2UgMCkpCg=='
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

# origin PHAI tro ve GitHub ke ca tren duong "clone do da co": lan chay dau co the da
# clone tu mot kho cuc bo ($Nguon), va fetch tu do thi "tuoi" chi tuoi bang kho cuc bo ay.
G -C "$Kho" remote set-url origin "$Url" | Out-Null
Write-Host "fetch ban va $Nhanh + nen master ..."
G -C "$Kho" fetch --quiet origin $Nhanh | Out-Null
# FETCH CA master. Bai hoc 19-09-2026: clone tai dung chi fetch nhanh ban va, nen
# `origin/master` dung yen tu 14-09; merge-base roi ve dinh master cu va cong kich thuoc
# do ra 46 tep / +7118 thay cho 2 tep / +397 - CUNG MOT COMMIT. Bo do nay gio fail-close
# (nen cu => KHONG DO DUOC chu khong phan quyet TRUOT), va day la ve con lai: lam nen tuoi.
G -C "$Kho" fetch --quiet origin '+refs/heads/master:refs/remotes/origin/master' | Out-Null
$mLoc = (G -C "$Kho" rev-parse --short=12 origin/master) | Select-Object -First 1
Write-Host "nen  : origin/master = $mLoc"
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
$tieuDe = 'Chay phep do g2 (bo test chay HAI lan - tinh 20-45 phut)'
if ($ChiKichThuoc) { $tieuDe = 'Chi do KICH THUOC (vai giay)' }
Tieu $tieuDe
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
$doiSo = @($BoDo, $Kho)
if ($ChiKichThuoc) { $doiSo += '--chi-kich-thuoc' }
& $pyCmd.Source @doiSo 2>&1 | Tee-Object -FilePath $Log
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
