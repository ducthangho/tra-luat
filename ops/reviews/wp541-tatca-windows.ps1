# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong, khong can gi khac):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-tatca-windows.ps1"
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
$ShaBoDo    = '0413b5b212f1f1c89e8e1130339f463affada41e25909eaffe4320a64c24572d'      # SHA-256 cua bo do Python nhung ben duoi

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
Write-Host 'WP541 - do N7 tren Windows that (mot tep, tu lo moi thu)'
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
$BoDo = Join-Path $Base 'wp541-do-n7-windows.py'
$B64 = @(
'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIiIiV1A1NDEgLSBQSEVQIERPIE43IFRSRU4gV0lORE9XUyBUSEFUIChiYW4gMzogbGll'
'dCBrZSBIRVQgY2EgZG8pLgoKQ2hheTogIHB5IHdwNTQxLWRvLW43LXdpbmRvd3MucHkgIjx0aHUtbXVjLWtobz4iIFtzaGEtbW9u'
'Z10KCk43IC0gRE9OIFZJIChsdWF0IEwxLCBiYSBsdW90IHJldmlldyBkYSBob2kpOgogIFNvIGRvbmcgdHJvbmcgb3BzL2xlYXNl'
'X3B1Ymxpc2gucHkga2hvcCBEVU5HIGNodW9pICAnaWYgbmVuX3RodWMgPT0gIndpbmRvd3MiOicKICB0cnVvYyA9IDEgID0+IG5o'
'YW5oIGdpYWkgdGhlbyBuZW4gQ09OIE5HVVlFTgogIHNhdSAgID0gMCAgPT4gZGEgdGF0IG5oYW5oIFdpbmRvd3MsIGNhIGRpY2gg'
'UEhBSSBkbwoKRkFJTC1DTE9TRTogbmVuIGRvIHNhaSA9PiBpbiBLSE9OR19ET19EVU9DLCByYyE9MCwgS0hPTkcgaW4ga2V0IGx1'
'YW4gbmFvLgpEb3QgYmllbiBjaGF5IHRyZW4gQkFOIFNBTyBUQU07IGNheSB0aGF0IGtob25nIGJpIGR1bmcgdG9pLgoKVmkgc2Fv'
'IGNvIGJhbiAzOiBiYW4gMiBsb2MgdGVuIGNhIGJhbmcgciIodFxcZCspKF9cXFMqKSIgbmVuIEJPIFNPVCBtb2kgdGVuIGRhbmcK'
'YHQwMmJfLi4uYCwgYHQ1NWFfLi4uYCAoY28gY2h1IGNhaSB0cnVvYyBnYWNoIGR1b2kpIC0gZHVuZyA1IGNhIG5odSB0aGUgdHJv'
'bmcgYm8uCkJhbiAzIGJhdCB0ZW4gREFZIERVIGBcXFMrYCwgZG9pIGNoaWV1IEhBSSBuZ3VvbiBkb2MgbGFwLCB2YSBjb24gZG9p'
'IGNoaWV1IHZvaQpTTyBIT0MgdHUgZG9uZyB0b25nIGtldC4gTGVjaCA9PiBiYW8gS0hPTkdfRE9fRFVPQyBjaG8gcGhhbiBsaWV0'
'IGtlLCBraG9uZyBpbSBsYW5nLgoiIiIKaW1wb3J0IGNvbnRleHRsaWIsIGlvLCBqc29uLCBvcywgcmUsIHNodXRpbCwgc3VicHJv'
'Y2Vzcywgc3lzLCB0ZW1wZmlsZQpmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKCm9zLmVudmlyb24uc2V0ZGVmYXVsdCgiUFlUSE9O'
'VVRGOCIsICIxIikKb3MuZW52aXJvbi5zZXRkZWZhdWx0KCJQWVRIT05JT0VOQ09ESU5HIiwgInV0Zi04IikKZm9yIF9sIGluIChz'
'eXMuc3Rkb3V0LCBzeXMuc3RkZXJyKToKICAgIHRyeTogX2wucmVjb25maWd1cmUoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJy'
'ZXBsYWNlIikKICAgIGV4Y2VwdCBFeGNlcHRpb246IHBhc3MKaWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6CiAgICB0cnk6CiAg'
'ICAgICAgaW1wb3J0IGN0eXBlcwogICAgICAgIGN0eXBlcy53aW5kbGwua2VybmVsMzIuU2V0Q29uc29sZU91dHB1dENQKDY1MDAx'
'KQogICAgICAgIGN0eXBlcy53aW5kbGwua2VybmVsMzIuU2V0Q29uc29sZUNQKDY1MDAxKQogICAgZXhjZXB0IEV4Y2VwdGlvbjog'
'cGFzcwoKZGVmIGlubigqcCk6CiAgICB2YW4gPSAiICIuam9pbihzdHIoeCkgZm9yIHggaW4gcCkKICAgIHRyeTogcHJpbnQodmFu'
'KQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICB0cnk6CiAgICAgICAgICAgIHN5cy5zdGRvdXQuYnVmZmVyLndyaXRlKHZh'
'bi5lbmNvZGUoInV0Zi04IiwgInJlcGxhY2UiKSArIGIiXG4iKTsgc3lzLnN0ZG91dC5mbHVzaCgpCiAgICAgICAgZXhjZXB0IEV4'
'Y2VwdGlvbjoKICAgICAgICAgICAgcHJpbnQodmFuLmVuY29kZSgiYXNjaWkiLCAiYmFja3NsYXNocmVwbGFjZSIpLmRlY29kZSgi'
'YXNjaWkiKSkKClNIQV9NT05HID0gc3lzLmFyZ3ZbMl0gaWYgbGVuKHN5cy5hcmd2KSA+IDIgZWxzZSAiMmY3MDg2OTAiCk1BVSA9'
'ICdpZiBuZW5fdGh1YyA9PSAid2luZG93cyI6JwpDQTE1ID0gInQxMjkgdDEzMCB0MTMxIHQxMzIgdDEzMyB0MTM2IHQxMzggdDEz'
'OSB0MTQ0IHQxNDUgdDE0NiB0MTQ3IHQxNDkgdDE1MCB0MTUxIi5zcGxpdCgpCkNBTU9JID0gInQxNjUgdDE2NiB0MTY3IHQxNjgi'
'LnNwbGl0KCkKCiMgLS0tIERvYyBsb2cgY3VhIGJvIHRlc3QuIFRlbiBjYSBsYSBcUysgREFZIERVLCBraG9uZyBnaWEgZGluaCBk'
'YW5nIHNvLiAtLS0KIyBydW5uZXIgaW46ICAiPj4+IHZhbyA8dGVuPiA8dXRjPiIgLyAiPDw8IHJhIDx0ZW4+IDxnaWF5PnMgUVVB'
'fERPfEJPX1FVQSIKIyAgICAgICAgICAgICAiISEhIGRvIDx0ZW4+IDxseSBkbz4iICAgICAgICAgICAgKG5nYXkgdGFpIGNobywg'
'QVNDSUkgdGh1YW4pCiMgICAgICAgICAgICAgIiAgRE8gIDx0ZW4+OiA8bHkgZG8+IiAgICAgICAgICAgIChjdW9pIGJvLCBjaHUg'
'RE8gY28gZGF1KQojICAgICAgICAgICAgICIgIEJPIFFVQSA8dGVuPjogPGx5IGRvPiIgICAgICAgICAoY3VvaSBibywgY2h1IEJP'
'IGNvIGRhdSkKUlhfUkEgICAgICA9IHJlLmNvbXBpbGUociIoP20pXjw8PCByYSAoXFMrKSBbMC05Ll0rcyAoXHcrKVxzKiQiKQpS'
'WF9ET19DSE8gID0gcmUuY29tcGlsZShyIig/bSleISEhIGRvIChcUyspICguKikkIikKIyBUaWVuIHRvIGNvIGRhdToga2hvYW4g'
'ZHVuZyBjaG8gY2Ega2hpIGNvbnNvbGUgbGFtIGhvbmcgYnl0ZSAtPiBcU3sxLDR9ICsgRFVORyBoYWkga2hvYW5nIHRyYW5nLgoj'
'IERvbmcgIkJPIFFVQSIgY2hpIGNvIE1PVCBraG9hbmcgdHJhbmcgc2F1IHR1IGRhdSBuZW4ga2hvbmcgbG90IHZhbyBkYXkuClJY'
'X0RPX0NVT0kgPSByZS5jb21waWxlKHIiKD9tKV4gezJ9KFxTezEsNH0pIHsyfShcUyspOiAoLiopJCIpClJYX0JPX1FVQSAgPSBy'
'ZS5jb21waWxlKHIiKD9tKV4gezJ9XFN7MSw2fSBRVUEgKFxTKyk6ICguKikkIikKUlhfVE9ORyAgICA9IHJlLmNvbXBpbGUociJs'
'ZWFzZV9wdWJsaXNoOiAoXGQrKS8oXGQrKVxiW15cbl0qPz0oXGQrKSxbXlxuXSo/PShcZCspIikKCiMgTG9wIGxvaTogbW9pIGxv'
'cCBtb3QgY2FjaCBjaHVhIEtIQUMgTkhBVSAtIGR1bmcgZ29wLgpMT1AgPSBbCiAgICAoIlBBVEgtVE9JLVRISUVVIiwgcmUuY29t'
'cGlsZShyIlBBVEggdFvhu5FvXWkgdGhpW+G7g2VddXwvdXNyL2JpbiIpKSwKICAgICgiUVVZRU4tU1lNTElOSyIsICByZS5jb21w'
'aWxlKHIiV2luRXJyb3IgMTMxNHxyZXF1aXJlZCBwcml2aWxlZ2UiKSksCiAgICAoIlFVWUVOLVRSVVktQ0FQIiwgcmUuY29tcGls'
'ZShyIldpbkVycm9yIDVcYnxBY2Nlc3MgaXMgZGVuaWVkIikpLAogICAgKCJLSE9ORy1QSEFJLUVYRSIsIHJlLmNvbXBpbGUociJX'
'aW5FcnJvciAxOTN8bm90IGEgdmFsaWQgV2luMzIiKSksCiAgICAoIlRISUVVLUNPTkctQ1UiLCAgcmUuY29tcGlsZShyIktIW8OU'
'T11ORyBbxJBEXU8gW8SQRF1bxq9VXVvhu6JPXUM6IHRoaVvhur9lXXUiKSksCiAgICAoIlVURjgtUE9MSUNZIiwgICAgcmUuY29t'
'cGlsZShyImtoW8O0b11uZyBwaFvhuqNhXWkgVVRGLTgiKSksCl0KZGVmIGxvcF9jdWEobHkpOgogICAgZm9yIHRlbiwgcnggaW4g'
'TE9QOgogICAgICAgIGlmIHJ4LnNlYXJjaChseSk6IHJldHVybiB0ZW4KICAgIHJldHVybiAiS0hBQyIKCmRlZiBzb19jYSh0ZW4p'
'OgogICAgIiIiS2hvYSBzbyBkZSBzYXAgeGVwOyBnaXUgdGVuIGRheSBkdSBsYW0gZGFuaCB0aW5oLiIiIgogICAgbSA9IHJlLm1h'
'dGNoKHIidChcZCspIiwgdGVuKQogICAgcmV0dXJuIChpbnQobS5ncm91cCgxKSkgaWYgbSBlbHNlIDEwKio2LCB0ZW4pCgpkZWYg'
'ZG9jX2RvKG91dCk6CiAgICAiIiJIRVQgY2EgZG8sIGRvYyBIQUkgbmd1b24gZG9jIGxhcCByb2kgZG9pIGNoaWV1IHZvaSBzbyBo'
'b2MuCgogICAgVHJhIChseV9kb190aGVvX3RlbiwgZ2hpX2NodV9kb2lfY2hpZXUsIGRhdF90aW5fY2F5KS4KICAgICIiIgogICAg'
'dGFpX2NobyA9IHt0OiBseS5zdHJpcCgpIGZvciB0LCBseSBpbiBSWF9ET19DSE8uZmluZGFsbChvdXQpfQogICAgYm8gPSB7dCBm'
'b3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXQpfQogICAgY3VvaSA9IHt0OiBseS5zdHJpcCgpIGZvciBfLCB0LCBseSBp'
'biBSWF9ET19DVU9JLmZpbmRhbGwob3V0KSBpZiB0IG5vdCBpbiBib30KICAgIGhvcCA9IGRpY3QoY3VvaSk7IGhvcC51cGRhdGUo'
'dGFpX2NobykgICAgICAjIHRhaV9jaG8gbGEgbmd1b24gQVNDSUksIHV1IHRpZW4KICAgIGZvciB0IGluIGN1b2k6CiAgICAgICAg'
'aG9wLnNldGRlZmF1bHQodCwgY3VvaVt0XSkKICAgIGdoaV9jaHUsIHRpbiA9IFtdLCBUcnVlCiAgICBpZiBzZXQodGFpX2Nobykg'
'IT0gc2V0KGN1b2kpOgogICAgICAgIGdoaV9jaHUuYXBwZW5kKGYiaGFpIG5ndW9uIExFQ0g6IGNoaS10YWktY2hvPXtzb3J0ZWQo'
'c2V0KHRhaV9jaG8pLXNldChjdW9pKSl9ICIKICAgICAgICAgICAgICAgICAgICAgICBmImNoaS1jdW9pLWJvPXtzb3J0ZWQoc2V0'
'KGN1b2kpLXNldCh0YWlfY2hvKSl9IikKICAgICAgICB0aW4gPSBGYWxzZQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dCkKICAg'
'IGlmIG5vdCBtOgogICAgICAgIGdoaV9jaHUuYXBwZW5kKCJLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcga2V0IC0+IGtob25nIGRv'
'aSBjaGlldSBkdW9jIHNvIGhvYyIpOyB0aW4gPSBGYWxzZQogICAgZWxzZToKICAgICAgICBkYXQsIHRyZW4gPSBpbnQobS5ncm91'
'cCgxKSksIGludChtLmdyb3VwKDIpKQogICAgICAgIGRvX3RoZW9fc29faG9jID0gdHJlbiAtIGRhdAogICAgICAgIGdoaV9jaHUu'
'YXBwZW5kKGYic28gaG9jOiB7dHJlbn0te2RhdH09e2RvX3RoZW9fc29faG9jfSBkbzsgZG9jIGR1b2Mge2xlbihob3ApfSIpCiAg'
'ICAgICAgaWYgZG9fdGhlb19zb19ob2MgIT0gbGVuKGhvcCk6CiAgICAgICAgICAgIGdoaV9jaHUuYXBwZW5kKGYiTEVDSCBTTyBI'
'T0M6IHRoaWV1IHtkb190aGVvX3NvX2hvYyAtIGxlbihob3ApfSBjYSAtPiBkYW5oIHNhY2ggS0hPTkcgZGF5IGR1IikKICAgICAg'
'ICAgICAgdGluID0gRmFsc2UKICAgIHJldHVybiBob3AsIGdoaV9jaHUsIHRpbgoKc28gPSB7fQpkZWYgZ2hpKGssIHYpOiBzb1tr'
'XSA9IHY7IHJldHVybiB2CgpkZWYgY2hheShhcmd2LCBjd2QsIHBodXQ9NDUpOgogICAgbXQgPSBkaWN0KG9zLmVudmlyb24sIFBZ'
'VEhPTlVURjg9IjEiLCBQWVRIT05JT0VOQ09ESU5HPSJ1dGYtOCIsIFBZVEhPTkRPTlRXUklURUJZVEVDT0RFPSIxIikKICAgIHAg'
'PSBzdWJwcm9jZXNzLnJ1bihbc3lzLmV4ZWN1dGFibGVdICsgYXJndiwgY3dkPXN0cihjd2QpLCBjYXB0dXJlX291dHB1dD1UcnVl'
'LAogICAgICAgICAgICAgICAgICAgICAgIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGlt'
'ZW91dD1waHV0KjYwLCBlbnY9bXQpCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpICsgKHAuc3RkZXJy'
'IG9yICIiKQoKZGVmIG1hdV9jYShvdXQsIHQpOgogICAgIiIiVHJhbmcgdGhhaSBjdWEgY2EgY28gdGllbiB0byBzbyBgdGAuIEJp'
'ZW4gZ2lvaSBgX2AgZGUgdDE1IGtob25nIG51b3QgdDE1MC4iIiIKICAgIG0gPSByZS5zZWFyY2gociIoP20pXjw8PCByYSAoIiAr'
'IHQgKyByIlthLXpdP19cUyopIFswLTkuXStzIChcdyspXHMqJCIsIG91dCkKICAgIHJldHVybiBtLmdyb3VwKDIpIGlmIG0gZWxz'
'ZSBOb25lCgpkZWYgdGVuX2RheV9kdShvdXQsIHQpOgogICAgbSA9IHJlLnNlYXJjaChyIig/bSlePDw8IHJhICgiICsgdCArIHIi'
'W2Etel0/X1xTKikgIiwgb3V0KQogICAgcmV0dXJuIG0uZ3JvdXAoMSkgaWYgbSBlbHNlIE5vbmUKCiMgLS0tLS0tLS0tLSBUVSBL'
'SUVNIEJPIERPQyAoY2hheSB0cm9uZyBtb2kgbHVvdCwgdHJlbiBtYXUgY28gc2FuKSAtLS0tLS0tLS0tCl9NQVUgPSAoCiAgICAi'
'Pj4+IHZhbyB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOX2JpX0NIQU4gMjAyNi0wOS0xOFQwMDowMDowMFpcbiIKICAgICI8'
'PDwgcmEgdDAyYl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTl9iaV9DSEFOIDAuMDEwcyBET1xuIgogICAgIiEhISBkbyB0MDJiX3Rl'
'bl9LSE9OR19DT19USEFNX1FVWUVOX2JpX0NIQU4gbG9pIGdpYSBkaW5oIEFcbiIKICAgICI+Pj4gdmFvIHQxNTBfcmV2aWV3Ml9G'
'MTBfbmd1b25fa2hvbmdfdXRmOCAyMDI2LTA5LTE4VDAwOjAwOjAxWlxuIgogICAgIjw8PCByYSB0MTUwX3JldmlldzJfRjEwX25n'
'dW9uX2tob25nX3V0ZjggMC4wMjBzIERPXG4iCiAgICAiISEhIGRvIHQxNTBfcmV2aWV3Ml9GMTBfbmd1b25fa2hvbmdfdXRmOCBU'
'cmFjZWJhY2sgV2luRXJyb3IgMTMxNCByZXF1aXJlZCBwcml2aWxlZ2VcbiIKICAgICI+Pj4gdmFvIHQxMzFfUzhfdGFtX3RyYW4g'
'MjAyNi0wOS0xOFQwMDowMDowMlpcbiIKICAgICI8PDwgcmEgdDEzMV9TOF90YW1fdHJhbiAwLjAzMHMgQk9fUVVBXG4iCiAgICAi'
'ICBC4buOIFFVQSB0MTMxX1M4X3RhbV90cmFuOiBuZW4gZml4dHVyZVxuIgogICAgIiAgxJDhu44gIHQwMmJfdGVuX0tIT05HX0NP'
'X1RIQU1fUVVZRU5fYmlfQ0hBTjogbG9pIGdpYSBkaW5oIEFcbiIKICAgICIgIMSQ4buOICB0MTUwX3JldmlldzJfRjEwX25ndW9u'
'X2tob25nX3V0Zjg6IFRyYWNlYmFjayBXaW5FcnJvciAxMzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgImxlYXNlX3B1Ymxp'
'c2g6IDEvMyDEkeG6oXQ7IMSRw6MgY2jhuqF5PTMsIGLhu48gcXVhPTFcbiIKKQpkZWYgdHVfa2llbSgpOgogICAgZG8sIGdjLCB0'
'aW4gPSBkb2NfZG8oX01BVSkKICAgIGtpZW0gPSBbCiAgICAgICAgKCJiYXQgZHUgMiBjYSBkbyIsIGxlbihkbykgPT0gMiksCiAg'
'ICAgICAgKCJiYXQgdGVuIGNvIGNodSBjYWkgKHQwMmIpIiwgYW55KHQuc3RhcnRzd2l0aCgidDAyYiIpIGZvciB0IGluIGRvKSks'
'CiAgICAgICAgKCJLSE9ORyBkZW0gY2EgQk8gUVVBIGxhIGRvIiwgbm90IGFueSh0LnN0YXJ0c3dpdGgoInQxMzEiKSBmb3IgdCBp'
'biBkbykpLAogICAgICAgICgiZG9pIGNoaWV1IHNvIGhvYyBEQVQiLCB0aW4pLAogICAgICAgICgibG9wIGxvaSBRVVlFTi1TWU1M'
'SU5LIiwgbG9wX2N1YShkb1tbdCBmb3IgdCBpbiBkbyBpZiB0LnN0YXJ0c3dpdGgoJ3QxNTAnKV1bMF1dKSA9PSAiUVVZRU4tU1lN'
'TElOSyIpLAogICAgICAgICgibWF1X2NhIGRvYyBkdW5nIiwgbWF1X2NhKF9NQVUsICJ0MTUwIikgPT0gIkRPIiksCiAgICAgICAg'
'KCJ0MTUgS0hPTkcgbnVvdCB0MTUwIiwgbWF1X2NhKF9NQVUsICJ0MTUiKSBpcyBOb25lKSwKICAgICAgICAoImJvIHF1YSBkb2Mg'
'ZHVuZyIsIFt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKF9NQVUpXSA9PSBbInQxMzFfUzhfdGFtX3RyYW4iXSksCiAg'
'ICBdCiAgICByZXR1cm4ga2llbQoKaW5uKCI9IiAqIDc4KTsgaW5uKCJXUDU0MSAtIGRvIE43IHRyZW4gV2luZG93cyB0aGF0IChi'
'YW4gMzogbGlldCBrZSBIRVQgY2EgZG8pIik7IGlubigiPSIgKiA3OCkKaW5uKCJUdSBraWVtIGJvIGRvYyBsb2c6IikKX2hvbmcg'
'PSBbdCBmb3IgdCwgayBpbiB0dV9raWVtKCkgaWYgbm90IGtdCmZvciB0LCBrIGluIHR1X2tpZW0oKTogaW5uKGYiICAgW3snREFU'
'ICcgaWYgayBlbHNlICdUUlVPVCd9XSB7dH0iKQppZiBfaG9uZzoKICAgIGlubigiIik7IGlubigiS0hPTkdfRE9fRFVPQzogYm8g'
'ZG9jIGxvZyBjdWEgY2hpbmggc2NyaXB0IG5heSBzYWkgLT4ga2hvbmcgZG8gZ2kgY2EuIikKICAgIHN5cy5leGl0KDMpCgojIC0t'
'LS0tLS0tLS0gMC4gTkVOIERPIC0tLS0tLS0tLS0KZ29jID0gUGF0aChzeXMuYXJndlsxXSkucmVzb2x2ZSgpIGlmIGxlbihzeXMu'
'YXJndikgPiAxIGVsc2UgUGF0aC5jd2QoKQppZiBub3QgKGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiKS5pc19maWxl'
'KCk6CiAgICBnMiA9IFBhdGgoX19maWxlX18pLnJlc29sdmUoKS5wYXJlbnQKICAgIGZvciB1bmcgaW4gKGcyLCBnMi5wYXJlbnQs'
'IGcyLnBhcmVudC5wYXJlbnQpOgogICAgICAgIGlmICh1bmcgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoLnB5IikuaXNfZmlsZSgp'
'OiBnb2MgPSB1bmc7IGJyZWFrCnRlcCA9IGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiCgpsb2kgPSBbXQppbm4oIiIp'
'OyBpbm4oInN5cy5wbGF0Zm9ybSAgOiIsIHN5cy5wbGF0Zm9ybSkKaW5uKCJweXRob24gICAgICAgIDoiLCBzeXMudmVyc2lvbi5z'
'cGxpdCgpWzBdKQppbm4oIm9zLnBhdGhzZXAgICAgOiIsIHJlcHIob3MucGF0aHNlcCkpCmlubigiUEFUSEVYVCAgICAgICA6Iiwg'
'cmVwcihvcy5lbnZpcm9uLmdldCgiUEFUSEVYVCIpKSkKaW5uKCJQcm9ncmFtRmlsZXMgIDoiLCByZXByKG9zLmVudmlyb24uZ2V0'
'KCJQcm9ncmFtRmlsZXMiKSkpCmlubigiU3lzdGVtUm9vdCAgICA6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiU3lzdGVtUm9vdCIp'
'KSkKaW5uKCJDT05HX0NVX0dJVCAgIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJDT05HX0NVX0dJVCIpKSkKaW5uKCJnb2Mga2hv'
'ICAgICAgIDoiLCBnb2MpCgojIC0tLSBRdXllbjogRE8gVEhBTkcsIGtob25nIGhvaSByZWdpc3RyeSByb2kgZG9hbiAtLS0KcXV5'
'ZW5fYWRtaW4gPSBOb25lCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAgIGltcG9ydCBjdHlwZXMK'
'ICAgICAgICBxdXllbl9hZG1pbiA9IGJvb2woY3R5cGVzLndpbmRsbC5zaGVsbDMyLklzVXNlckFuQWRtaW4oKSkKICAgIGV4Y2Vw'
'dCBFeGNlcHRpb246CiAgICAgICAgcXV5ZW5fYWRtaW4gPSBOb25lCmdoaSgicXV5ZW5fYWRtaW4iLCBxdXllbl9hZG1pbikKaW5u'
'KCJjaGF5IHZvaSBxdXllbiBBZG1pbmlzdHJhdG9yIDoiLCBxdXllbl9hZG1pbikKCnN5bWxpbmtfZHVvYyA9IE5vbmUKdHJ5Ogog'
'ICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGRpY2ggPSBQYXRoKHQpIC8gImRpY2gu'
'dHh0IjsgZGljaC53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICB0cnk6CiAgICAgICAgICAgIG9zLnN5'
'bWxpbmsoc3RyKGRpY2gpLCBzdHIoUGF0aCh0KSAvICJsayIpKQogICAgICAgICAgICBzeW1saW5rX2R1b2MgPSBUcnVlCiAgICAg'
'ICAgZXhjZXB0IE9TRXJyb3IgYXMgZToKICAgICAgICAgICAgc3ltbGlua19kdW9jID0gRmFsc2UKICAgICAgICAgICAgZ2hpKCJz'
'eW1saW5rX2xvaSIsIGYie3R5cGUoZSkuX19uYW1lX199OiB7ZX0iKQpleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICBnaGkoInN5'
'bWxpbmtfbG9pIiwgZiJ7dHlwZShlKS5fX25hbWVfX306IHtlfSIpCmdoaSgic3ltbGlua19kdW9jIiwgc3ltbGlua19kdW9jKQpp'
'bm4oInRhbyBzeW1saW5rIGR1b2MgICAgICAgICAgICA6Iiwgc3ltbGlua19kdW9jLAogICAgIiIgaWYgc3ltbGlua19kdW9jIGVs'
'c2UgZiIgICh7c28uZ2V0KCdzeW1saW5rX2xvaScsJycpWzo3MF19KSIpCgpnaXRfdGhhdCA9IHNodXRpbC53aGljaCgiZ2l0IikK'
'aW5uKCJ3aGljaCgnZ2l0JykgIDoiLCByZXByKGdpdF90aGF0KSkKaWYgc3lzLnBsYXRmb3JtICE9ICJ3aW4zMiI6IGxvaS5hcHBl'
'bmQoZiJLSE9ORyBwaGFpIFdpbmRvd3MgKHN5cy5wbGF0Zm9ybT17c3lzLnBsYXRmb3JtIXJ9KSIpCmlmIG5vdCB0ZXAuaXNfZmls'
'ZSgpOiAgICAgIGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB9IikKaWYgbm90IGdpdF90aGF0OiAgICAgICAgICAgbG9pLmFw'
'cGVuZCgia2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCB0aHVvbmciKQpyYywgbyA9IGNoYXkoWyItYyIsICJpbXBvcnQgc3VicHJv'
'Y2VzcztwcmludChzdWJwcm9jZXNzLnJ1bihbJ2dpdCcsJ3Jldi1wYXJzZScsJy0tc2hvcnQnLCdIRUFEJ10sIgogICAgICAgICAg'
'ICAgICAgICAgICJjYXB0dXJlX291dHB1dD1UcnVlLHRleHQ9VHJ1ZSkuc3Rkb3V0LnN0cmlwKCkpIl0sIGdvYywgNSkKaGVhZCA9'
'IChvLnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsiPyJdKVstMV0KaW5uKCJIRUFEICAgICAgICAgIDoiLCBoZWFkLCBmIihtb25n'
'IHtTSEFfTU9OR30pIikKaWYgbm90IGhlYWQuc3RhcnRzd2l0aChTSEFfTU9OR1s6N10pOiBsb2kuYXBwZW5kKGYiSEVBRD17aGVh'
'ZH0ga2hhYyB7U0hBX01PTkd9IikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigiS0hPTkdfRE9fRFVPQzogbmVuIGRvIHNhaSwg'
'S0hPTkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlubigiICAtIiwgeCkKICAgIHN5cy5leGl0KDMpCmlu'
'bigibmVuIGRvOiBEQVQiKQoKIyAtLS0tLS0tLS0tIDEuIFRSVU9DIC0tLS0tLS0tLS0KdHJ1b2MgPSB0ZXAucmVhZF90ZXh0KGVu'
'Y29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVSkKaW5uKCIiKTsgaW5uKCItIiAqIDc4KQppbm4oIk43IC0gRE9OIFZJOiBzbyBkb25n'
'IGtob3AgY2h1b2kiLCByZXByKE1BVSkpCmlubihmIiAgVFJVT0MgKGNodWEgZG90IGJpZW4pID0ge2doaSgnbjdfdHJ1b2MnLCB0'
'cnVvYyl9ICAgW21vbmcgMV0iKQppZiB0cnVvYyAhPSAxOgogICAgaW5uKCJLSE9OR19ET19EVU9DOiBtYXUgZG90IGJpZW4ga2hv'
'bmcgeHVhdCBoaWVuIGR1bmcgMSBsYW4uIik7IHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0gMi4gQk8gVEVTVCBEQVkgRFUgLS0t'
'LS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpCmlubigiQ2hheSBibyB0ZXN0IGRheSBkdSB0cmVuIGJhbiB2YSAoMTAtMzAg'
'cGh1dCkuLi4iKQpyY19uZW4sIG91dF9uZW4gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBnb2MpCmlubigi'
'ICByYyA9IiwgZ2hpKCJyY19iYW5fdmEiLCByY19uZW4pKQptID0gUlhfVE9ORy5zZWFyY2gob3V0X25lbikKaW5uKCIgIHRvbmcg'
'a2V0OiIsIG0uZ3JvdXAoMCkgaWYgbSBlbHNlICIoS0hPTkcgZG9jIGR1b2MpIikKaWYgbToKICAgIGdoaSgiZGF0IiwgaW50KG0u'
'Z3JvdXAoMSkpKTsgZ2hpKCJ0cmVuIiwgaW50KG0uZ3JvdXAoMikpKQogICAgZ2hpKCJkYV9jaGF5IiwgaW50KG0uZ3JvdXAoMykp'
'KTsgZ2hpKCJib19xdWFfc28iLCBpbnQobS5ncm91cCg0KSkpCgpkb19oZXQsIGdoaV9jaHUsIHRpbl9jYXkgPSBkb2NfZG8ob3V0'
'X25lbikKZ2hpKCJzb19jYV9kbyIsIGxlbihkb19oZXQpKTsgZ2hpKCJsaWV0X2tlX2RheV9kdSIsIHRpbl9jYXkpCmlubigiIik7'
'IGlubigiICAtLS0gZG9pIGNoaWV1IGJvIGRvYyAtLS0iKQpmb3IgZyBpbiBnaGlfY2h1OiBpbm4oIiAgICoiLCBnKQppZiBub3Qg'
'dGluX2NheToKICAgIGlubigiICAgISEgS0hPTkcgRE8gRFVPQyAoZGF5IGR1KTogZGFuaCBzYWNoIGR1b2kgZGF5IENPIFRIRSBU'
'SElFVS4gRGFuIGNhIGxvZyB0aG8gdmUuIikKCmlubigiIik7IGlubihmIiAgPT09IHtsZW4oZG9faGV0KX0gQ0EgRE8gZG9jIGR1'
'b2MsIHBoYW4gbG9haSB0aGVvIExPUCBMT0kgPT09IikKdGhlb19sb3AgPSB7fQpmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9'
'c29fY2EpOgogICAgdGhlb19sb3Auc2V0ZGVmYXVsdChsb3BfY3VhKGRvX2hldFt0XSksIFtdKS5hcHBlbmQodCkKZm9yIGxwIGlu'
'IHNvcnRlZCh0aGVvX2xvcCk6CiAgICBpbm4oZiIgICBbe2xwfV0gKHtsZW4odGhlb19sb3BbbHBdKX0pIHtbeC5zcGxpdCgnXycp'
'WzBdIGZvciB4IGluIHRoZW9fbG9wW2xwXV19IikKaW5uKCIiKQpmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgog'
'ICAgaW5uKGYiICAge3Quc3BsaXQoJ18nKVswXTo3fSBbe2xvcF9jdWEoZG9faGV0W3RdKToxNH1dIHt0fSIpCiAgICBpbm4oZiIg'
'ICAgICAgICAgIHtkb19oZXRbdF1bOjE2MF19IikKZ2hpKCJkb190aGVvX2xvcCIsIHRoZW9fbG9wKQpnaGkoImRvX2x5X2RvIiwg'
'e3Q6IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQoKYnEgPSBzb3J0ZWQoe3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVB'
'LmZpbmRhbGwob3V0X25lbil9LCBrZXk9c29fY2EpCmdoaSgiY2FfYm9fcXVhIiwgYnEpCmlubigiIik7IGlubihmIiAgY2EgQkkg'
'Qk8gUVVBICh7bGVuKGJxKX0pOiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCmlubigiIik7IGlubigiICAxNSBj'
'YSBUVU5HIERPIHRyZW4gQ0k6IikKYjE1ID0ge30KZm9yIHQgaW4gQ0ExNToKICAgIHR0ID0gdGVuX2RheV9kdShvdXRfbmVuLCB0'
'KTsgdHIgPSBtYXVfY2Eob3V0X25lbiwgdCk7IGIxNVt0XSA9IHRyCiAgICBscCA9IGYiIFt7bG9wX2N1YShkb19oZXRbdHRdKX1d'
'IiBpZiB0dCBpbiBkb19oZXQgZWxzZSAiIgogICAgaW5uKGYiICAgICB7dH06IHt0cn17bHB9IikKZ2hpKCJjYTE1IiwgYjE1KQpp'
'bm4oZiIgID0+IGNvbiBETzoge1t0IGZvciB0IGluIENBMTUgaWYgYjE1W3RdID09ICdETyddfSIpCgppbm4oIiIpOyBpbm4oIiAg'
'NCBjYSBNT0kgKE4xLU40IGN1YSBiYW4gdmEpOiIpCmI0ID0ge3Q6IG1hdV9jYShvdXRfbmVuLCB0KSBmb3IgdCBpbiBDQU1PSX07'
'IGdoaSgiY2FfbW9pIiwgYjQpCmZvciB0IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCgojIC0tLS0tLS0tLS0g'
'My4gUFJPQkUgVEhVQyBURSAtLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiUHJvYmUgdGh1YyB0ZSAoa2hv'
'bmcgcXVhIHRoYW0gc28gdGllbSk6IikKc3lzLnBhdGguaW5zZXJ0KDAsIHN0cihnb2MpKQppbXBvcnQgaW1wb3J0bGliLnV0aWwK'
'c3BlYyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscDU0MSIsIHN0cih0ZXApKQpscCA9IGltcG9y'
'dGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9kdWxlKGxwKQoKIyBfZ2l0X3dpbmRv'
'd3MgR0hJIENIQU4gRE9BTiBUSEFORyBSQSBzdGRlcnIgKGxlYXNlX3B1Ymxpc2gucHk6IHN5cy5zdGRlcnIud3JpdGUga2hpCiMg'
'JVByb2dyYW1GaWxlcyUga2hvbmcgcGhhbiBnaWFpKS4gRG8gbGEgSEFOSCBWSSBEVU5HIGN1YSBiYW4gdmEsIHZhIHBoZXAgcHJv'
'YmUgZHVvaQojIGRheSBDTyBZIHRhbyByYSBkdW5nIGNhbmggYXksIG5lbiBkb25nIGNoYW4gZG9hbiBjaGFjIGNoYW4gYmF5IHJh'
'LgojIEJhdCBubyBsYWkgdmEgR0hJIE5IQU4gdGhhbmggZHUgbGlldSwgZHVuZyBkZSBubyByb2kgcmEgc3RkZXJyIGN1YSB0aWVu'
'IHRyaW5oOgojIFdpbmRvd3MgUG93ZXJTaGVsbCA1LjEgdm9pIGAyPiYxYCArICRFcnJvckFjdGlvblByZWZlcmVuY2U9J1N0b3An'
'IGJpZW4gTU9JIGRvbmcKIyBzdGRlcnIgY3VhIHRpZW4gdHJpbmggY29uIHRoYW5oIGxvaSBDSEkgTUFORyDigJQgbW90IGRvbmcg'
'Y2hhbiBkb2FuIGdpZXQgY2EgbHVvdCBkby4KIyBEYSB4YXkgcmEgdGhhdCAxOC0wOS0yMDI2IHRyZW4gbWF5IGNodSBraG86IGJv'
'IHRlc3QgY2hheSB4b25nLCBONyBraG9uZyBiYW8gZ2lvIGNoYXkuCl9lcnIgPSBpby5TdHJpbmdJTygpCndpdGggY29udGV4dGxp'
'Yi5yZWRpcmVjdF9zdGRlcnIoX2Vycik6CiAgICB0cnk6CiAgICAgICAgZHVvbmcgPSBscC5fZ2l0X2V4ZV90b2lfdGhpZXUoKQog'
'ICAgICAgIGdoaSgiZ2lhaV90aGF0IiwgZHVvbmcpOyBnaGkoImdpYWlfdGhhdF9sYV9leGUiLCBib29sKGR1b25nKSBhbmQgZHVv'
'bmcubG93ZXIoKS5lbmRzd2l0aCgiLmV4ZSIpKQogICAgICAgIF9uZW0gPSBOb25lCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6'
'CiAgICAgICAgX25lbSA9IGYie3R5cGUoZSkuX19uYW1lX199OiB7c3RyKGUpWzoxNTBdfSIKICAgICAgICBkdW9uZyA9IE5vbmU7'
'IGdoaSgiZ2lhaV90aGF0IiwgTm9uZSk7IGdoaSgiZ2lhaV90aGF0X2xhX2V4ZSIsIEZhbHNlKQoKICAgIHdpdGggdGVtcGZpbGUu'
'VGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdG1wOgogICAgICAgIHNoaW0gPSBQYXRoKHRtcCkvInNoaW0iOyBzaGltLm1rZGlyKCkK'
'ICAgICAgICBmb3IgbiBpbiAoImdpdC5iYXQiLCJnaXQuY21kIiwiZ2l0LnB5Iik6IChzaGltL24pLndyaXRlX3RleHQoIkBlY2hv'
'IG9mZlxyXG4iLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGN3ZGsgPSBQYXRoKHRtcCkvImN3ZCI7IGN3ZGsubWtkaXIoKTsg'
'cGYgPSBQYXRoKHRtcCkvInBmIjsgcGYubWtkaXIoKQogICAgICAgIGNkMSwgY2QyID0gW10sIFtdCiAgICAgICAga3EgID0gbHAu'
'X2dpdF93aW5kb3dzKHBhdGg9c3RyKHNoaW0pLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3dkayksIGNoYW5fZG9h'
'bj1jZDEpCiAgICAgICAgKHNoaW0vImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBr'
'cTIgPSBscC5fZ2l0X3dpbmRvd3MocGF0aD1zdHIoc2hpbSksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjd2RrKSwg'
'Y2hhbl9kb2FuPWNkMikKCmlmIF9uZW06IGlubigiICBfZ2l0X2V4ZV90b2lfdGhpZXUoKSBORU0gICAgIC0+IiwgX25lbSkKZWxz'
'ZTogICAgaW5uKCIgIF9naXRfZXhlX3RvaV90aGlldSgpICAgICAgICAgLT4iLCByZXByKGR1b25nKSkKaW5uKCIgIHNoaW0tb25s'
'eSBvIFBBVEggbmdvYWkgY3dkICAgLT4iLCByZXByKGtxKSwgIihtb25nIE5vbmUpIikKZ2hpKCJ0dV9jaG9pX3NoaW0iLCBrcSBp'
'cyBOb25lKQppbm4oIiAgRE9JIENIVU5HIERVT05HOiB0aGVtIGdpdC5leGUtPiIsIHJlcHIoa3EyKSkKZ2hpKCJkb2lfY2h1bmdf'
'ZHVvbmciLCBib29sKGtxMikgYW5kIGtxMi5sb3dlcigpLmVuZHN3aXRoKCJnaXQuZXhlIikpCmdoaSgiY2hhbl9kb2FuX3Byb2Jl'
'IiwgY2QxICsgY2QyKQpnaGkoInN0ZGVycl9wcm9iZSIsIF9lcnIuZ2V0dmFsdWUoKS5zdHJpcCgpLnNwbGl0bGluZXMoKSkKaW5u'
'KCIgIGNoYW4gZG9hbiBiYW4gdmEgZ2hpIGxhaSAgICAgLT4iLCAoY2QxICsgY2QyKSBvciAiKGtob25nIGNvKSIpCgojIC0tLS0t'
'LS0tLS0gNC4gTjcgLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIk43IC0gZG90IGJpZW4gdHJlbiBCQU4g'
'U0FPIFRBTSAoY2F5IHRoYXQgS0hPTkcgYmkgZHVuZyB0b2kpIikKd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBh'
'cyB0bXA6CiAgICBzYW8gPSBQYXRoKHRtcCkvImNheSIKICAgIHNodXRpbC5jb3B5dHJlZShnb2MsIHNhbywgaWdub3JlPXNodXRp'
'bC5pZ25vcmVfcGF0dGVybnMoIi5naXQiLCJfX3B5Y2FjaGVfXyIsIioucHljIikpCiAgICBmMiA9IHNhby8ib3BzIi8ibGVhc2Vf'
'cHVibGlzaC5weSIKICAgIGYyLndyaXRlX3RleHQoZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJlcGxhY2UoTUFVLCAi'
'aWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICBzYXUgPSBmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291'
'bnQoTUFVKQogICAgaW5uKGYiICBTQVUgKGRhIGRvdCBiaWVuKSA9IHtnaGkoJ243X3NhdScsIHNhdSl9ICAgW21vbmcgMF0iKQog'
'ICAgaWYgc2F1ICE9IDA6IGlubigiS0hPTkdfRE9fRFVPQzogZG90IGJpZW4gS0hPTkcgYXAgZHVvYy4iKTsgc3lzLmV4aXQoMykK'
'ICAgIHJjX20sIG91dF9tID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgc2FvKQogICAgbTE2NSA9IG1hdV9j'
'YShvdXRfbSwgInQxNjUiKTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20pCiAgICB0MTY1ID0gdGVuX2RheV9kdShvdXRfbSwgInQx'
'NjUiKQogICAgaW5uKCIgIHJjIHNhdSBkb3QgYmllbiA6IiwgcmNfbSkKICAgIGlubigiICB0MTY1IDoiLCBtMTY1LCAifCIsIChk'
'bS5nZXQodDE2NSkgb3IgIiIpWzoxMjBdKQogICAgZ2hpKCJuN190MTY1X3NhdV9kb3RfYmllbiIsIG0xNjUpOyBnaGkoIm43X2Rh'
'dCIsIG0xNjUgPT0gIkRPIikKICAgIGdoaSgibjdfdDE2NV9seV9kbyIsIChkbS5nZXQodDE2NSkgb3IgIiIpWzoyMDBdKQoKIyAt'
'LS0tLS0tLS0tIEtFVCBMVUFOIC0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQpvayA9IChzby5nZXQoIm43X3RydW9j'
'Iik9PTEgYW5kIHNvLmdldCgibjdfc2F1Iik9PTAgYW5kIHNvLmdldCgibjdfZGF0IikKICAgICAgYW5kIHNvLmdldCgidHVfY2hv'
'aV9zaGltIikgYW5kIHNvLmdldCgiZG9pX2NodW5nX2R1b25nIikpCmlubigiTjcgKHRydW9jPTEsIHNhdT0wLCB0MTY1IERPKToi'
'LCAiREFUIiBpZiBzby5nZXQoIm43X2RhdCIpIGVsc2UgIlRSVU9UIikKaW5uKCJUdSBjaG9pIHNoaW0gbyBQQVRIIHRoYXQgICAg'
'OiIsICJEQVQiIGlmIHNvLmdldCgidHVfY2hvaV9zaGltIikgZWxzZSAiVFJVT1QiKQppbm4oIkRvaSBjaHVuZyBkdW9uZyAgICAg'
'ICAgICAgICA6IiwgIkRBVCIgaWYgc28uZ2V0KCJkb2lfY2h1bmdfZHVvbmciKSBlbHNlICJUUlVPVCIpCmlubigiUXV5ZW4gc3lt'
'bGluayAgICAgICAgICAgICAgIDoiLCBzby5nZXQoInN5bWxpbmtfZHVvYyIpLCAifCBBZG1pbmlzdHJhdG9yOiIsIHNvLmdldCgi'
'cXV5ZW5fYWRtaW4iKSkKaW5uKCJUb25nIGNhIGRvICAgICAgICAgICAgICAgICAgOiIsIHNvLmdldCgic29fY2FfZG8iKSwgIi0+'
'Iiwge2s6IGxlbih2KSBmb3IgaywgdiBpbiB0aGVvX2xvcC5pdGVtcygpfSkKaW5uKCJEYW5oIHNhY2ggZG8gREFZIERVICAgICAg'
'ICAgOiIsICJDTyIgaWYgdGluX2NheSBlbHNlICJLSE9ORyBETyBEVU9DIC0geGVtIGRvaSBjaGlldSBvIHRyZW4iKQppbm4oIiIp'
'OyBpbm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kgSlNPTiBOQVkgVkUgQ0hPIFJFVklFV0VSIC0tLSIpCmlubihqc29uLmR1bXBzKHNv'
'LCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0xLCBkZWZhdWx0PXN0cikpCnN5cy5leGl0KDAgaWYgb2sgZWxzZSAxKQo='
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
Write-Host "HEAD : $head  (mong $ShaVa)"
if ("$head" -notlike "$ShaVa*") { Dung "HEAD=$head khac $ShaVa - dang do nham ma" }

# ---------------------------------------------------------------- 5. chay
Tieu 'Chay phep do (bo test chay HAI lan - tinh 20-40 phut)'
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
& $pyCmd.Source $BoDo $Kho $ShaVa 2>&1 | Tee-Object -FilePath $Log
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
    3       { Write-Host 'KHONG DO DUOC'  -ForegroundColor Red }
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
