# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong, khong can gi khac):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
#
# Do RIENG cong kich thuoc (vai giay, khong chay bo test 20-45 phut):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1" -ChiKichThuoc
#
# Do RIENG probe + tu kiem cong (vai giay, khong chay bo test):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1" -ChiProbe
#
# Nhanh mac dinh la fix_issue_541 - nhanh mang ung vien g2 (lease g2 khai dung nhanh
# nay). Ung vien nay gio la mot merge commit: 0ea95de + origin/master. Doi nhanh khac:
#     ... -Nhanh <ten-nhanh>
#
# Khong can tai them tep nao. Bo do Python nam NGAY TRONG tep nay (base64) va
# duoc kiem toan ven bang SHA-256 truoc khi chay.
#
# rc:  0 = moi chot dat | 1 = co chot truot | 3 = KHONG DO DUOC (nen do sai)
#
# Toan tep la ASCII thuan, co chu de bo giai ma cua PowerShell 5.1 khong lam hong
# ky tu nao. Duong dan co dau tieng Viet van chay binh thuong (xu ly luc chay).

param(
    [string]$Base    = '',     # thu muc lam viec. Mac dinh: thu muc chua chinh tep nay (TAI CHO trong kho: %TEMP%\wp541-do)
    [string]$Nguon   = '',     # kho co san dung lam nguon clone (nhanh hon). Mac dinh: <Base>\tl546
    [string]$Kho     = '',     # clone RIENG de do.                            Mac dinh: <Base>\tl541-do
    [string]$Py      = '',     # duong dan python neu muon chi dinh
    [string]$Nhanh   = 'fix_issue_541',       # nhanh mang ban va can do
    [switch]$ChiGiaiNen,       # chi ghi bo do Python ra dia roi dung (de doc/kiem)
    [switch]$ChiKichThuoc,     # CHI do cong kich thuoc (vai giay) roi dung - khong chay bo test
    [switch]$ChiProbe,         # CHI do muc 0,1,3 (vai giay): tu kiem cong + probe thang
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
$ShaBoDo    = 'becb29d7efd7d8ddb09a7c23c637fb20b166b9e765dabe0a826e5c7ec9b7a059'      # SHA-256 cua bo do Python nhung ben duoi

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
# Chay TAI CHO trong kho = ps1 nam o <goc>\ops\reviews VA <goc>\.git co that (tep hoac thu muc).
# Chi "ong co .git" thi KHONG du: HOME la kho dotfiles + ps1 o HOME\Downloads\wp541 cung khop (do
# tren pwsh 7.4: .py cu canh ps1 => rc=3 "hai ban sao da troi" oan).
$GocTaiCho = $null
if ($PSScriptRoot) {
    # GetDirectoryName tra $null o goc o dia, KHONG nem (Split-Path -Parent '' nem, do tren pwsh 7.4).
    $cha = [IO.Path]::GetDirectoryName($PSScriptRoot)
    $ong = if ($cha) { [IO.Path]::GetDirectoryName($cha) } else { $null }
    if ($ong -and ([IO.Path]::GetFileName($PSScriptRoot) -eq 'reviews') -and ([IO.Path]::GetFileName($cha) -eq 'ops') -and
        (Test-Path -LiteralPath (Join-Path $ong '.git'))) { $GocTaiCho = $ong }
}
# Tai cho: clone do, log va _congcu KHONG duoc nam trong cay dang theo doi (do tren pwsh 7.4: ba muc
# `??`, va `git add -A` them tl541-do lam embedded repository). Dat ra TEMP.
if (-not $Base) {
    if ($GocTaiCho) { $Base = Join-Path ([IO.Path]::GetTempPath()) 'wp541-do'; New-Item -ItemType Directory -Force -Path $Base | Out-Null }
    else { $Base = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path } }
}
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
    # Bo do can Python >= 3.7 (f-string 3.6, capture_output 3.7). 3.6 nem TypeError -> excepthook -> rc=3 (dung);
    # <= 3.5 / 2.7 thi SyntaxError TRUOC khi excepthook kip dat -> rc=1 = "CO CHOT TRUOT" cho luot CHUA HE CHAY
    # (do tren pwsh 7.4, trinh thong dich mo hinh 3.5: rc=1, CO CHOT TRUOT). Doi phien ban NGAY o probe.
    try { $thu = & $pyCmd.Source -c "import sys;assert sys.version_info>=(3,7),sys.version;print(sys.version.split()[0])" 2>&1 } catch { $ok = $false; $thu = $_.Exception.Message }
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
# Giai nen vao thu muc CONG CU, KHONG vao $Base: $Base co the la thu muc cua ps1 (-Base tro vao
# ops/reviews, hoac ban ps1 truoc 2026-09-30b chay tai cho), va `Move-Item -Force` ban cu DE THANG
# tep .py dang duoc theo doi.
New-Item -ItemType Directory -Force -Path $CongCu | Out-Null
$BoDo = Join-Path $CongCu 'wp541-do-g2-windows.py'
# Tep .py canh ps1 chi la BAN SAO THU HAI khi chay TAI CHO trong kho ($GocTaiCho, buoc 0). Lech ban
# nhung => DUNG: khong cong nao trong kho buoc hai ban khop (kiem tren Linux: --kiem-dong-bo). NGOAI
# kho (vd. Downloads) tep canh ps1 la RAC do ban ps1 CU de lai (ban cu giai nen vao $Base) - chan o day
# la chan nham dung duong nang cap (do tren pwsh 7.4: ps1 moi + .py cua aa2be9a canh no => rc=3).
$Canh = $null
if ($GocTaiCho) {
    $Canh = Join-Path $PSScriptRoot 'wp541-do-g2-windows.py'
} elseif ($PSScriptRoot -and (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'wp541-do-g2-windows.py'))) {
    Write-Host '  bo qua wp541-do-g2-windows.py canh ps1: ngoai kho, la ban giai nen cua ps1 cu'
}
if ($Canh -and (Test-Path -LiteralPath $Canh) -and ((Bam $Canh) -ne $ShaBoDo)) {
    Dung "tep canh ps1 ($Canh) LECH ban nhung - hai ban sao da troi. Xoa tep cu, hoac dong bo lai ca hai"
}
$B64 = @(
'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIiIiV1A1NDEgZzIgLSBQSEVQIERPIFRSRU4gV0lORE9XUyBUSEFUIGNobyBzcGVj',
'IHIzIChOMS1ONCArIE44LU4xMiArIE43ICsga2ljaCB0aHVvYykuCgpDaGF5OiAgcHkgd3A1NDEtZG8tZzItd2luZG93cy5w',
'eSAiPHRodS1tdWMta2hvPiIKCktIT05HIGdoaW0gU0hBLiBObyBkbyBCQVQgS1kgZGF1IG5hbyBkYW5nIG8gdHJlbiBuaGFu',
'aCwgcm9pIFRVIFBIQU4gTE9BSToKICBoZWFkID09IDJmNzA4NjlhICAtPiBkYXkgbGEgZzEsIENIVUEgY28gYmFuIHZhIGcy',
'LiBQcm9iZSB2YW4gaW4gKGxhbSBORU4gRE8pIG5odW5nIE43JyByYQogICAgICAgICAgICAgICAgICAgICAgIEtIT05HIERP',
'IERVT0MgKGcxIGRhIGxhbmQsIGRpZmYgcm9uZykgbmVuIHJjPTMuCiAgaGVhZCBsYSBoYXUgZHVlICAgIC0+IHVuZyB2aWVu',
'IGcyLgogIGtoYWMgICAgICAgICAgICAgICAtPiBLSE9ORyBETyBEVU9DIChyZWJhc2U/IG5oYW0gbmhhbmg/KSAtPiByYz0z',
'LCBraG9uZyBrZXQgbHVhbi4KVHUgMjAtMDkgZzEgREEgTEFORCB2YW8gbWFzdGVyLCBuZW4gImhhdSBkdWUgY3VhIGcxIiBL',
'SE9ORyBjb24gbG9haSBkdW9jIG5oYW5oIG5hbyAoZG8gZHVvYzoKbWFzdGVyIDQ0NjIwZTggdmEgbW90IG5oYW5oIGJvb2tr',
'ZWVwaW5nIGRldSByYSAidW5nIHZpZW4gZzIiLCBEQVQgcmM9MCkuIFZpIHZheSBkb2kgdHVvbmcgY29uCnBoYWkgKGEpIGNv',
'IHRoYXkgZG9pIHNvIHZvaSBtZXJnZS1iYXNlIHZhIChjKSBNQU5HIFZBTyBpdCBuaGF0IG1vdCBjYSBNT0kgY3VhIGcyIChD',
'QV9NT0lfRzI6Cm1lcmdlLWJhc2UgY2h1YSBjbywgSEVBRCBjbykg4oCUIGtob25nIHRoaSBLSE9ORyBETyBEVU9DLiBDaGkg',
'IihiKSBjaGFtIFdSSVRFX1NFVF9HMiIgdGhpIEtIT05HIGR1OgpzYXUgZzIgZGEgY28gNiBwYWNrZXQga2hhYyBjaGFtIG9w',
'cy9sZWFzZV9wdWJsaXNoKi5weSAoZG8gZHVvYzogbmhhbmggIzYwNyA4MDNjMjQ4IHJhICJUSEUgSEUgRE8KRFVPQzogZzIi',
'LCBONycgREFUIDIgdGVwIC8gKzUzLCBEQVQgMTIgcmM9MCkuIChjKSBrZW8gdGhlbyAoYiksIG5lbiAoYikgY2hpIGNvbiBk',
'dW9jIEdISSwga2hvbmcgY2hhbS4KCkJBIFRSQU5HIFRIQUkgbyBtb2kgY2hvdDogREFUIC8gVFJVT1QgLyBLSE9ORyBETyBE',
'VU9DLiBDYWkgdGh1IGJhIEtIT05HIGR1b2MgbGFuZyBsZQp0aGFuaCBtb3QgdHJvbmcgaGFpIGNhaSBraWEg4oCUIGRvIGxh',
'IGNhIGRvY3RyaW5lIGBOb25lICE9IEZhbHNlYCBjdWEga2hvLgoKTU9JIGNob3QgYW0gZGV1IGNvIERPSSBDSFVORyBEVU9O',
'Ry4gTW90IGNob3QgY2hpIGRvIGNoaWV1ICJwaGFpIHR1IGNob2kiIHRoaSBtb3QgaGFtCmByZXR1cm4gTm9uZWAgdm8gZGll',
'dSBraWVuIGN1bmcgcXVhIGR1b2Mgbm8uCgpEb3QgYmllbiBjaGF5IHRyZW4gQkFOIFNBTyBUQU07IGNheSB0aGF0IGtob25n',
'IGJpIGR1bmcgdG9pLgoiIiIKaW1wb3J0IGNvbnRleHRsaWIsIGhhc2hsaWIsIGltcG9ydGxpYi51dGlsLCBpbnNwZWN0LCBp',
'bywganNvbiwgb3MsIHJlLCBzaHV0aWwsIHN1YnByb2Nlc3MsIHN5cywgdGVtcGZpbGUKZnJvbSBwYXRobGliIGltcG9ydCBQ',
'YXRoLCBQdXJlUG9zaXhQYXRoLCBQdXJlV2luZG93c1BhdGgKCm9zLmVudmlyb24uc2V0ZGVmYXVsdCgiUFlUSE9OVVRGOCIs',
'ICIxIikKb3MuZW52aXJvbi5zZXRkZWZhdWx0KCJQWVRIT05JT0VOQ09ESU5HIiwgInV0Zi04IikKZm9yIF9sIGluIChzeXMu',
'c3Rkb3V0LCBzeXMuc3RkZXJyKToKICAgIHRyeTogX2wucmVjb25maWd1cmUoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJy',
'ZXBsYWNlIikKICAgIGV4Y2VwdCBFeGNlcHRpb246IHBhc3MKaWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6CiAgICB0cnk6',
'CiAgICAgICAgaW1wb3J0IGN0eXBlcwogICAgICAgIGN0eXBlcy53aW5kbGwua2VybmVsMzIuU2V0Q29uc29sZU91dHB1dENQ',
'KDY1MDAxKQogICAgICAgIGN0eXBlcy53aW5kbGwua2VybmVsMzIuU2V0Q29uc29sZUNQKDY1MDAxKQogICAgZXhjZXB0IEV4',
'Y2VwdGlvbjogcGFzcwoKZGVmIGlubigqcCk6CiAgICB2YW4gPSAiICIuam9pbihzdHIoeCkgZm9yIHggaW4gcCkKICAgIHRy',
'eTogcHJpbnQodmFuLCBmbHVzaD1UcnVlKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICB0cnk6IHN5cy5zdGRvdXQu',
'YnVmZmVyLndyaXRlKHZhbi5lbmNvZGUoInV0Zi04IiwgInJlcGxhY2UiKSArIGIiXG4iKTsgc3lzLnN0ZG91dC5mbHVzaCgp',
'CiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjogcHJpbnQodmFuLmVuY29kZSgiYXNjaWkiLCAiYmFja3NsYXNocmVwbGFjZSIp',
'LmRlY29kZSgiYXNjaWkiKSwgZmx1c2g9VHJ1ZSkKCiMgTmdvYWkgbGUgS0hPTkcgYmF0ID0+IFB5dGhvbiB0aG9hdCByYz0x',
'LCBtYSByYz0xIG8gZGF5IERBIENPIE5HSElBICJjbyBjaG90IFRSVU9UIiAoZG9uZwojIGN1b2kgdGVwKSDigJQgZHVuZyBs',
'eSBkbyBwczEgZGF0IGB0cmFwYCAtPiByYz0zLiBEbyBkdW9jOiBnaXQgdmFuZyBQQVRIIChkb25nIGBnaXQoZ29jLAojICJy',
'ZXYtcGFyc2UiKWAgY2hheSBUUlVPQyBgaWYgbG9pOmApLCBibyB0ZXN0IHF1YSBoYW4sIHVuZyB2aWVuIHRoaWV1IF9naXRf',
'd2luZG93cywgcHJvYmUKIyB0aGF0IG5lbSBuZ29haSBsZSDigJQgY2EgYm9uIHR1bmcgcmEgcmM9MSBtYSBwaGVwIGRvIENI',
'VUEgSEUgY2hheSB4b25nLgojIERvbmcgS0VUIExVQU4gaW4gVFJVT0MgdHJhY2ViYWNrLCBjdW5nIGtlbmggc3Rkb3V0OiBr',
'aG9pIHBzMSBkYW4gY2hvIHJldmlld2VyIGJhdCBkYXUgVFUgZG9uZwojIG5heSwgbmVuIGluIHRyYWNlYmFjayB0cnVvYyB0',
'aGkgbm8gbmFtIE5HT0FJIGtob2kgKGRvIHRyZW4gcHdzaCA3LjQ6IGtob2kgMiBkb25nLCAwIGRvbmcKIyB0cmFjZWJhY2sp',
'LiB0cnkvZmluYWxseTogaG9vayBUVSBIT05HICh2ZC4gc3Rkb3V0IGxhIG9uZyBkYSBkb25nKSB0aGkgUHl0aG9uIHRyYSBy',
'Yz0xIOKAlCBkdW5nCiMgbWEgImNvIGNob3QgVFJVT1QiIChkbyBkdW9jOiBCcm9rZW5QaXBlIHRyb25nIGhvb2sgPT4gcmM9',
'MSkuCmRlZiBfbmdvYWlfbGVfbGFfS0REKGtpZXUsIGd0LCB2ZXQpOgogICAgdHJ5OgogICAgICAgIGltcG9ydCB0cmFjZWJh',
'Y2sKICAgICAgICBpbm4oIiIpOyBpbm4oZiJLSE9ORyBETyBEVU9DOiBuZ29haSBsZSBraG9uZyBsdW9uZyB0cnVvYyB7a2ll',
'dS5fX25hbWVfX306IHtndH0iKQogICAgICAgIGlubigiIi5qb2luKHRyYWNlYmFjay5mb3JtYXRfZXhjZXB0aW9uKGtpZXUs',
'IGd0LCB2ZXQpKS5yc3RyaXAoKSkKICAgICAgICBpbm4oIlBoZXAgZG8gQ0hVQSBjaGF5IHhvbmcuIEtob25nIGtldCBsdWFu',
'IGdpLiIpCiAgICAgICAgZm9yIF9sIGluIChzeXMuc3Rkb3V0LCBzeXMuc3RkZXJyKToKICAgICAgICAgICAgdHJ5OiBfbC5m',
'bHVzaCgpCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb246IHBhc3MKICAgIGZpbmFsbHk6CiAgICAgICAgb3MuX2V4aXQo',
'MykKc3lzLmV4Y2VwdGhvb2sgPSBfbmdvYWlfbGVfbGFfS0RECgpTSEFfRzEgICA9ICIyZjcwODY5YTA1Mzc4NDNlOWNhZTc4',
'NjE4ZWU3YWU4YzI2MWQ5NzJkIgojIEtIT05HIGdoaW0gYmFzZS4gU3BlYyByMyBONicga2hhaSBkbyBudW1zdGF0IHNvIGQ3',
'MDU2MjMg4oCUIE5IVU5HIHNwZWMgQ1VORyBiYW8gZXhlY3V0b3IKIyBgZ2l0IG1lcmdlIG9yaWdpbi9tYXN0ZXJgLiBTYXUg',
'bWVyZ2UsIHBoZXAgZG8gc28gZDcwNTYyMyBOVU9UIGNhIHBoYW4gbWFzdGVyIG1hbmcgdmFvOgojIGRvIHRoYXQgMTgtMDkg',
'dHJlbiBiYW4gdmEgZzIgY3VhIGFneSBjaG8gNSB0ZXAgLyArODEyLCB0cm9uZyBraGkgdmllYyBjdWEgYWd5IGxhIDIgdGVw',
'IC8gKzM1My4KIyBNb3QgY2hvdCBuaHUgdGhlIHNlIGJhbyAidnVvdCB0cmFuIiBjaG8gbW90IGJhbiB2YSBLSE9ORyB2dW90',
'LiBCYXNlIGR1bmcgbGEgTUVSR0UtQkFTRS4KU0hBX0JBU0VfU1BFQyA9ICJkNzA1NjIzMTYyYjc1YjczNDBlZTdjY2E1NGFj',
'MmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0wOS0zMGMiICAgICAgICAgICAgICAjIGRvaSBNT0kga2hpIHN1YSBi',
'byBkbyAtIGxvZyB0dSBraGFpIGJhbiBuYW8KVFJBTl9URVAsIFRSQU5fRE9ORyA9IDIsIDQwMCAgICAgICAgICAjIE43JyBj',
'dWEgc3BlYyByMwpNQVVfV0lOICA9ICdpZiBuZW5fdGh1YyA9PSAid2luZG93cyI6JwojIFdyaXRlIHNldCBjdWEgcGFja2V0',
'ICM1NDEgZzIuIERpZmYga2hvbmcgY2hhbSB0ZXAgbmFvIG8gZGF5ID0+IGRvIE5IQU0gTkhBTkguCldSSVRFX1NFVF9HMiA9',
'IHsib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJ9CiMgIlR1b2kiIGNoaSBjbyBu',
'Z2hpYSBraGkgc28gdm9pIE1BWSBDSFUgVEhBVC4gTW90IG1pcnJvciBjdWMgYm8gY3UgY3VuZyB0cmEgbHMtcmVtb3RlID09',
'CiMgb3JpZ2luL21hc3RlciAoZG8gZHVvYzogbWFzdGVyIGMxNmJkMzIgLT4gInZlIG5lbiBUVU9JIiwgNDYgdGVwIC8gKzcx',
'MTggY2hvIDBlYTk1ZGUpLgojIERhbmggc2FjaCBDSE8gUEhFUDsgYHJlbW90ZSBnZXQtdXJsYCBkYSBraGFpIHRyaWVuIGlu',
'c3RlYWRPZiBuZW4gY2h1eWVuIGh1b25nIGN1bmcgbG8gcmEuClVSTF9LSE9fSE9QX0xFID0geyJodHRwczovL2dpdGh1Yi5j',
'b20vZHVjdGhhbmdoby90cmEtbHVhdCIsICJodHRwczovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdC5naXQiLAog',
'ICAgICAgICAgICAgICAgICAjIFNTSCB0b2kgQ1VORyBraG8gKHNhdSBfdXJsX3NhY2gpOiBgdXJsLiJnaXRAZ2l0aHViLmNv',
'bToiLmluc3RlYWRPZiAiaHR0cHM6Ly9naXRodWIuY29tLyJgCiAgICAgICAgICAgICAgICAgICMgcmF0IHBobyBiaWVuIG8g',
'bWF5IGRldjsgdGhpZXUgaGFpIGRhbmcgbmF5IHRoaSBraG8gVEhBVCBiaSBiYW8gIktIT05HIHBoYWkga2hvIHRoYXQiLgog',
'ICAgICAgICAgICAgICAgICAic3NoOi8vZ2l0aHViLmNvbS9kdWN0aGFuZ2hvL3RyYS1sdWF0IiwgInNzaDovL2dpdGh1Yi5j',
'b20vZHVjdGhhbmdoby90cmEtbHVhdC5naXQiLAogICAgICAgICAgICAgICAgICAiZ2l0QGdpdGh1Yi5jb206ZHVjdGhhbmdo',
'by90cmEtbHVhdCIsICJnaXRAZ2l0aHViLmNvbTpkdWN0aGFuZ2hvL3RyYS1sdWF0LmdpdCJ9CiMgYHJlbW90ZSBnZXQtdXJs',
'YCBLSEFJIFRSSUVOIGluc3RlYWRPZiwgbWEgbWF1IGB1cmwuImh0dHBzOi8vPHRva2VuPkBnaXRodWIuY29tLyIuaW5zdGVh',
'ZE9mYCByYXQgcGhvCiMgYmllbi4gSW4vZ2hpIG5ndXllbiB2YW4gbGEgZHVhIFRPS0VOIHZhbyBsb2cgdmEgdmFvIGtob2kg',
'SlNPTiBwczEgYmFvIGRhbiBjaG8gcmV2aWV3ZXIgKGRvIGR1b2M6CiMgMyBkb25nIHRyb25nIGtob2kgZGFuKS4gQm8gdXNl',
'cmluZm8gVFJVT0Mga2hpIGluIHZhIFRSVU9DIGtoaSBzbyDigJQgdG9rZW4gdmFuIGxhIEdpdEh1YiB0aGF0LgojIEF1dGhv',
'cml0eSBrZXQgdGh1YyBvIGAvYCwgYD9gIGhvYWMgYCNgIERBVSBUSUVOIOKAlCBkdW5nIGx1YXQgZ2l0L2N1cmwuIEJhbiBg',
'W14vXSpAYCBudW90IGNhIGA/YC9gI2AKIyBuZW4gbW90IFVSTCB0cm8gdG9pIE1BWSBLSEFDIChob3N0IGR1bmcgdHJ1b2Mg',
'YD9gLCBkdW9pIGA/YCBsYSBgQGdpdGh1Yi5jb20vPGtobz5gKSBkdW9jICJsYW0gc2FjaCIKIyB0aGFuaCBkdW5nIG1vdCBt',
'dWMgQ0hPIFBIRVAsIHRyb25nIGtoaSBnaXQgbm9pIHRvaSBtYXkga2lhIChkbyBkdW9jOiBtaXJyb3IgY3UgcGh1YyB2dSBx',
'dWEgSFRUUFMgPT4KIyAidmUgbmVuIFRVT0kiLCBUUlVPVCA0NiB0ZXAgLyArNzExOCkuIFZhbiBibyB0b2kgYEBgIENVT0kg',
'dHJvbmcgYXV0aG9yaXR5OiB1c2VyaW5mbyBjbyBgQGAgdHJhbiB0aGkKIyBjdXJsIHR1IGNob2kgKCJCYWQgaG9zdG5hbWUi',
'KSwgY29uIGtoaSBpbiB0aGkga2hvbmcgbG8gcGhhbiBzYXUgYEBgIHRodSBuaGF0LgpfUlhfVVNFUklORk8gPSByZS5jb21w',
'aWxlKHIiXihbQS1aYS16XVtBLVphLXowLTkrLi1dKjovLylbXi8/I10qQCIpCmRlZiBfdXJsX3NhY2godSk6IHJldHVybiBf',
'UlhfVVNFUklORk8uc3ViKHIiXDEiLCB1IG9yICIiKSAgICAgICAgICAjIGRlIFNPIChsdWF0IGdpdC9jdXJsKQojIElOIHBo',
'YWkgY2hlIFJPTkcgaG9uIFNPOiBtYXQga2hhdSBjbyBgP2AvYCNgIFRSQU4gdGhpIGBbXi8/I10qQGAga2hvbmcga2hvcCBu',
'ZW4gVVJMIHJhIGxvZyBOR1VZRU4gVkFOCiMgKGRvIGR1b2MgdHJlbiAyMDI2LTA5LTMwYjogMyBkb25nIG8gLS1jaGkta2lj',
'aC10aHVvYywgMyBkb25nIHRyb25nIGtob2kgZGFuIC0tY2hpLXByb2JlOyBiYW4gMzBhOiAwKS4KIyBDaGUgdG9pIGBAYCBD',
'VU9JIHRydW9jIGAvYCBkYXUgdGllbiwgdmEgREUgREFVIGAqKipAYCBkZSBiYW4gaW4ga2hvbmcgdHUgbmhhbiBsYSBnaXRo',
'dWIuY29tIGtoaSBnaXQgbm9pCiMgdG9pIG1heSBraGFjICh2ZC4gaG9zdCB0cnVvYyBgP2ApLiBIYWkgcXV5IHRhYywgaGFp',
'IG11YyBkaWNoOiBTTyB0aGVvIGdpdCwgSU4gdGhlbyAidGh1YSBjb24gaG9uIGxvIi4KZGVmIF91cmxfaW4odSk6IHJldHVy',
'biByZS5zdWIociJeKFtBLVphLXpdW0EtWmEtejAtOSsuLV0qOi8vKVteL10qQCIsIHIiXDEqKipAIiwgdSBvciAiIikKIyBU',
'aG9uZyBiYW8gbG9pIGN1YSBnaXQgQ0hJIGJvIHVzZXJpbmZvIHRvaSBgQGAgREFVIFRJRU46IHVzZXJpbmZvIGNvIGBAYCB0',
'cmFuICh2ZC4gdGVuIGRhbmcgbmhhcCBsYQojIGVtYWlsKSB0aGkgcGhhbiBzYXUgdmFuIHJhIHN0ZGVyciBscy1yZW1vdGUs',
'IG1hIHN0ZGVyciBheSBkdW9jIGluIHZhbyBkb25nIEtERCBjdWEgTjcnIChkbyBkdW9jOgojIDIgZG9uZyB0cm9uZyBsb2cs',
'IDEgdHJvbmcga2hvaSBkYW4pLiBMYW0gc2FjaCBNT0kgVVJMIHRyb25nIHZhbiBiYW4gdHJ1b2Mga2hpIGluLgpkZWYgX2Fu',
'X3VzZXJpbmZvKHQpOiByZXR1cm4gcmUuc3ViKHIiKFtBLVphLXpdW0EtWmEtejAtOSsuLV0qOi8vKVteXHMvPyMnXCJdKkAi',
'LCByIlwxIiwgdCBvciAiIikKIyBDYSBuZ29haSBwaGFtIHZpIHIzIMKnbmdvYWlfcGhhbV92aSDigJQgZG8gQ0hJTkggU1BF',
'QyBraGFpLCBraG9uZyBwaGFpIGJvIGRvIHR1IHF1eWV0LgojIERvIGxhIERBTkggU0FDSCBDSE8gUEhFUDogY2EgZG8gbmFv',
'IEtIT05HIG5hbSB0cm9uZyBkYXkgdmEgS0hPTkcgcGhhaSAidGhpZXUgY29uZyBjdSIKIyB0aGkgbGEgVFJVT1QuIERhbmgg',
'c2FjaCBjYW0gdGhpIGJhbyBnaW8gY3VuZyB0aGlldTsgZGFuaCBzYWNoIGNobyBwaGVwIHRoaSBiaWV0IHRydW9jLgpOR09B',
'SV9QSEFNX1ZJID0gc2V0KCJ0MTMxIHQxMzIgdDE1MCB0MTI1IHQzNSB0MzYgdDM3IHQzOCB0MzkgdDQwIi5zcGxpdCgpKQoj',
'IENhIGN1YSBDSElOSCBwYWNrZXQgbmF5LiBNb3QgY2EgbyBkYXkgbWEgRE8gdGhpIGtob25nIGJhbyBnaW8gZHVvYyBibyBx',
'dWEuCkNBX1BBQ0tFVCA9IHNldCgidDE2NSB0MTY2IHQxNjcgdDE2OCB0MTY5IHQxNzAgdDE3MSB0MTcyIHQxNzMiLnNwbGl0',
'KCkpCiMgQ2EgTU9JIG1hIGcyIHRoZW0gdmFvIChOOC1OMTIpLiBEb2kgdHVvbmcgZG8gcGhhaSBNQU5HIGNodW5nIHZhbzog',
'bWVyZ2UtYmFzZSBjaHVhIGNvLCBIRUFEIGNvLgpDQV9NT0lfRzIgPSAidDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxp',
'dCgpCkNBMTUgID0gInQxMjkgdDEzMCB0MTMxIHQxMzIgdDEzMyB0MTM2IHQxMzggdDEzOSB0MTQ0IHQxNDUgdDE0NiB0MTQ3',
'IHQxNDkgdDE1MCB0MTUxIi5zcGxpdCgpCkNBTU9JID0gInQxNjUgdDE2NiB0MTY3IHQxNjgiLnNwbGl0KCkKCkRBVCwgVFJV',
'T1QsIEtERCA9ICJEQVQiLCAiVFJVT1QiLCAiS0hPTkcgRE8gRFVPQyIKc28sIGNob3QgPSB7fSwgW10KZGVmIGdoaShrLCB2',
'KTogc29ba10gPSB2OyByZXR1cm4gdgpkZWYga2V0KHRlbiwgdHJhbmdfdGhhaSwgY2hpX3RpZXQ9IiIpOgogICAgY2hvdC5h',
'cHBlbmQoKHRlbiwgdHJhbmdfdGhhaSwgY2hpX3RpZXQpKQogICAgaW5uKGYiICBbe3RyYW5nX3RoYWk6MTR9XSB7dGVufSIg',
'KyAoZiIgICB7Y2hpX3RpZXR9IiBpZiBjaGlfdGlldCBlbHNlICIiKSkKICAgIHJldHVybiB0cmFuZ190aGFpCgojIC0tLS0t',
'LS0tLS0tLS0tLS0gZG9jIGxvZyBjdWEgYm8gdGVzdCAoYmFuIDMsIGRhIGRvIHRyZW4gbG9nIFRIQVQpIC0tLS0tLS0tLS0t',
'LS0tLS0KUlhfRE9fQ0hPICA9IHJlLmNvbXBpbGUociIoP20pXiEhISBkbyAoXFMrKSAoLiopJCIpClJYX0RPX0NVT0kgPSBy',
'ZS5jb21waWxlKHIiKD9tKV4gezJ9KFxTezEsNH0pIHsyfShcUyspOiAoLiopJCIpClJYX0JPX1FVQSAgPSByZS5jb21waWxl',
'KHIiKD9tKV4gezJ9XFN7MSw2fSBRVUEgKFxTKyk6ICguKikkIikKUlhfVE9ORyAgICA9IHJlLmNvbXBpbGUociJsZWFzZV9w',
'dWJsaXNoOiAoXGQrKS8oXGQrKVxiW15cbl0qPz0oXGQrKSxbXlxuXSo/PShcZCspIikKCmRlZiBzb19jYSh0KToKICAgIG0g',
'PSByZS5tYXRjaChyInQoXGQrKSIsIHQpOyByZXR1cm4gKGludChtLmdyb3VwKDEpKSBpZiBtIGVsc2UgMTAqKjYsIHQpCgpk',
'ZWYgZG9jX2RvKG91dCk6CiAgICB0YWlfY2hvID0ge3Q6IGwuc3RyaXAoKSBmb3IgdCwgbCBpbiBSWF9ET19DSE8uZmluZGFs',
'bChvdXQpfQogICAgYm8gPSB7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXQpfQogICAgY3VvaSA9IHt0OiBs',
'LnN0cmlwKCkgZm9yIF8sIHQsIGwgaW4gUlhfRE9fQ1VPSS5maW5kYWxsKG91dCkgaWYgdCBub3QgaW4gYm99CiAgICBob3Ag',
'PSBkaWN0KGN1b2kpOyBob3AudXBkYXRlKHRhaV9jaG8pCiAgICBnYywgdGluID0gW10sIFRydWUKICAgIGlmIHNldCh0YWlf',
'Y2hvKSAhPSBzZXQoY3VvaSk6CiAgICAgICAgZ2MuYXBwZW5kKGYiaGFpIG5ndW9uIExFQ0g6IGNoaS10YWktY2hvPXtzb3J0',
'ZWQoc2V0KHRhaV9jaG8pLXNldChjdW9pKSl9IGNoaS1jdW9pPXtzb3J0ZWQoc2V0KGN1b2kpLXNldCh0YWlfY2hvKSl9IikK',
'ICAgICAgICB0aW4gPSBGYWxzZQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dCkKICAgIGlmIG5vdCBtOgogICAgICAgIGdj',
'LmFwcGVuZCgiS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCIpOyB0aW4gPSBGYWxzZQogICAgZWxzZToKICAgICAgICBk',
'YXQsIHRyZW4gPSBpbnQobS5ncm91cCgxKSksIGludChtLmdyb3VwKDIpKQogICAgICAgIGdjLmFwcGVuZChmInNvIGhvYzog',
'e3RyZW59LXtkYXR9PXt0cmVuLWRhdH0gZG87IGRvYyBkdW9jIHtsZW4oaG9wKX0iKQogICAgICAgIGlmIHRyZW4gLSBkYXQg',
'IT0gbGVuKGhvcCk6CiAgICAgICAgICAgIGdjLmFwcGVuZChmIkxFQ0ggU08gSE9DOiB0aGlldSB7dHJlbi1kYXQtbGVuKGhv',
'cCl9IGNhIik7IHRpbiA9IEZhbHNlCiAgICByZXR1cm4gaG9wLCBnYywgdGluCgpfTUFVID0gKCIhISEgZG8gdDAyYl90ZW5f',
'S0hPTkdfQ09fVEhBTV9RVVlFTiBhXG4iCiAgICAgICAgIiEhISBkbyB0MTUwX3ggV2luRXJyb3IgMTMxNCByZXF1aXJlZCBw',
'cml2aWxlZ2VcbiIKICAgICAgICAiICBC4buOIFFVQSB0MTMxX3k6IG5lbiBmaXh0dXJlXG4iCiAgICAgICAgIiAgxJDhu44g',
'IHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU46IGFcbiIKICAgICAgICAiICDEkOG7jiAgdDE1MF94OiBXaW5FcnJvciAx',
'MzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICJsZWFzZV9wdWJsaXNoOiAxLzMgxJHhuqF0OyDEkcOjIGNo4bqh',
'eT0zLCBi4buPIHF1YT0xXG4iKQoKZGVmIGNoYXkoYXJndiwgY3dkLCBwaHV0PTYwKToKICAgIG10ID0gZGljdChvcy5lbnZp',
'cm9uLCBQWVRIT05VVEY4PSIxIiwgUFlUSE9OSU9FTkNPRElORz0idXRmLTgiLAogICAgICAgICAgICAgIFBZVEhPTkRPTlRX',
'UklURUJZVEVDT0RFPSIxIiwgUFlUSE9OVU5CVUZGRVJFRD0iMSIpCiAgICBwID0gc3VicHJvY2Vzcy5ydW4oW3N5cy5leGVj',
'dXRhYmxlXSArIGFyZ3YsIGN3ZD1zdHIoY3dkKSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwKICAgICAgICAgICAgICAgICAgICAg',
'ICB0ZXh0PVRydWUsIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCwgZW52PW10',
'KQogICAgcmV0dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rkb3V0IG9yICIiKSArIChwLnN0ZGVyciBvciAiIikKCmRlZiBtYXVf',
'Y2Eob3V0LCB0KToKICAgIG0gPSByZS5zZWFyY2gociIoP20pXjw8PCByYSAoIiArIHQgKyByIlthLXpdP19cUyopIFswLTku',
'XStzIChcdyspXHMqJCIsIG91dCkKICAgIHJldHVybiBtLmdyb3VwKDIpIGlmIG0gZWxzZSBOb25lCgpkZWYgZ2l0KGdvYywg',
'KmEsIHBodXQ9NSk6CiAgICBwID0gc3VicHJvY2Vzcy5ydW4oWyJnaXQiLCAiLUMiLCBzdHIoZ29jKSwgKmFdLCBjYXB0dXJl',
'X291dHB1dD1UcnVlLCB0ZXh0PVRydWUsCiAgICAgICAgICAgICAgICAgICAgICAgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3Jz',
'PSJyZXBsYWNlIiwgdGltZW91dD1waHV0KjYwKQogICAgcmV0dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rkb3V0IG9yICIiKS5z',
'dHJpcCgpLCAocC5zdGRlcnIgb3IgIiIpLnN0cmlwKCkKCgojID09PT09PT09PT09PT09PT09IE5BTSBQUk9CRSwgdmlldCB0',
'aGFuaCBIQU0gVEhVQU4gZGUgVFUgS0lFTSBkdW9jID09PT09PT09PT09PT09PT09CiMgTW9pIGhhbSB0cmEgKHRyYW5nX3Ro',
'YWksIGNoaV90aWV0LCBkdV9saWV1KS4gS0hPTkcgaW4sIEtIT05HIHRob2F0IOKAlCBuaG8gdmF5IGNodW5nCiMgY2hheSBk',
'dW9jIHRyZW4gbmVuIEJBVCBLWSwgdmEgYC0tdHUta2llbS1wcm9iZWAgZ29pIHRoYW5nIGNodW5nIGRlIGtpZW0gY2hpbmgg',
'Ym8gZG8uCgpkZWYgX3Nhbih0KToKICAgIGQgPSBQYXRoKHQpLyJkIjsgZC5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7',
'IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICByZXR1cm4gZCwgY3csIHBmCgpkZWYgZG9f',
'bjgoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiQnVvYyAxIChDT05HX0NVX0dJVCkgY2hpIGR1b2MgbmhhbiBnaXQuZXhlLiBE',
'b2kgY2h1bmcgZHVvbmc6IGdpdC5leGUgVkFOIHBoYWkgbmhhbi4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVtcGZpbGUu',
'VGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgZm9yIHRlbiBp',
'biAoImdpdC5leGUiLCAiZ2l0LmJhdCIsICJnaXQuY21kIiwgImdpdC5weSIsICJraG9uZy1waGFpLWdpdC50eHQiKToKICAg',
'ICAgICAgICAgZiA9IGQvdGVuOyBmLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBf',
'ID0gZ29pKGNvbmdfY3VfZ2l0PXN0cihmKSwgcGF0aD0iIiwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkK',
'ICAgICAgICAgICAga3FbZiJDT05HX0NVX0dJVD17dGVufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiVFUgQ0hPSSIKICAgIGxv',
'dCA9IFtrIGZvciBrLCB2IGluIGtxLml0ZW1zKCkgaWYgdiA9PSAiTkhBTiIgYW5kIG5vdCBrLmVuZHN3aXRoKCJnaXQuZXhl',
'IildCiAgICBpZiBrcS5nZXQoIkNPTkdfQ1VfR0lUPWdpdC5leGUiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwg',
'ImRvaSBjaHVuZyBkdW9uZyBob25nOiBnaXQuZXhlIGhvcCBsZSBtYSBiaSB0dSBjaG9pIiwga3EKICAgIHJldHVybiAoREFU',
'IGlmIG5vdCBsb3QgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgbG90IGVsc2UgZiJjb24gbmhhbjoge2xvdH0iKSwga3EKCmRl',
'ZiBkb19uOShnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJNdWMgUEFUSCBib2MgbmhheSBrZXAgcGhhaSBOSEFOOyBtdWMgcm9u',
'ZyAvIHRvYW4ga2hvYW5nIHRyYW5nIHBoYWkgYm8gcXVhLCBraG9uZyBuZW0uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRl',
'bXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgodCkvImNvIGdpdCI7IGQubWtkaXIo',
'KTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgICAg',
'IChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgZm9yIG5oYW4sIG11YyBp',
'biAoKCJraG9uZyBuaGF5Iiwgc3RyKGQpKSwgKCJjbyBuaGF5IGtlcCIsIGYnIntkfSInKSwKICAgICAgICAgICAgICAgICAg',
'ICAgICAgICAoInJvbmciLCAiIiksICgiY2hpIGtob2FuZyB0cmFuZyIsICIgICAiKSk6CiAgICAgICAgICAgIHRyeToKICAg',
'ICAgICAgICAgICAgIHIsIF8gPSBnb2kocGF0aD1tdWMsIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAg',
'ICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59Il0gPSAiTkhBTiIgaWYgciBlbHNlICJOb25lIgogICAgICAgICAgICBl',
'eGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59Il0gPSBmIk5FTSB7dHlwZShl',
'KS5fX25hbWVfX30iCiAgICBpZiBrcS5nZXQoIlBBVEgga2hvbmcgbmhheSIpICE9ICJOSEFOIjoKICAgICAgICByZXR1cm4g',
'S0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG11YyBQQVRIIHRodW9uZyBtYSBraG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtx',
'CiAgICBvayA9IChrcS5nZXQoIlBBVEggY28gbmhheSBrZXAiKSA9PSAiTkhBTiIKICAgICAgICAgIGFuZCBrcS5nZXQoIlBB',
'VEggcm9uZyIpID09ICJOb25lIiBhbmQga3EuZ2V0KCJQQVRIIGNoaSBraG9hbmcgdHJhbmciKSA9PSAiTm9uZSIpCiAgICBy',
'ZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgojIERhdSBwaGFu',
'IGNhY2ggZHVuZyBERSBUSFUuIFBoYWkgS0hBQyBvcy5wYXRoc2VwIHRyZW4gQ0EgSEFJIG5lbiAoJzsnIFdpbmRvd3MsICc6',
'JyBQT1NJWCkKIyB0aGkgaGFpIGdpYSB0aHV5ZXQgInRhY2ggdGhlbyBkYXUgZHVvYyB0cnV5ZW4iIHZhICJ0YWNoIHRoZW8g',
'b3MucGF0aHNlcCIgbW9pIHJvaSByYSBuaGF1LgpUSFVfTjEwID0gInwiCgpkZWYgZG9fbjEwKGdvaSwgc2lnLCB0ZXB0KToK',
'ICAgICIiIkhhbSBwaGFpIHRhY2ggUEFUSCB0aGVvIGRhdSBwaGFuIGNhY2ggRFVPQyBUUlVZRU4sIGtob25nIHRoZW8gb3Mu',
'cGF0aHNlcCBjdWEgbmVuLgoKICAgIEJhbiBjdSBkbyAibW90IGRhdSAnOycgdHJvbmcgVEVOIHRodSBtdWMiIHZhIGRhdCBE',
'QVQgdHJlbiBXaW5kb3dzIGR1IGhhbSBzYWkuIE5vCiAgICBkZWdlbmVyYXRlOiB0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBE',
'QSBsYSAnOycsIG5lbiAnQzovYTtiJyB0aGF0IHN1IENPIE5HSElBIGxhIGhhaQogICAgbXVjIOKAlCAidGFjaCBkdW5nIiB2',
'YSAidGFjaCBzYWkiIGNobyByYSBjdW5nIGtldCBxdWEsIHBoZXAgZG8ga2hvbmcgdGhlIGRvIG5hby4gTm8KICAgIGRhIGNo',
'YW0gREFUIGNobyA5NTgzMTY4NSB0cm9uZyBraGkgdDE3MSBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1bmcga2h1eWV0',
'IHRhdCBheS4KICAgIE1vdCBjb25nIGtob25nIHRoZSBkbyB0aGkga2hvbmcgcGhhaSBjb25nLgogICAgIiIiCiAgICB0ZW5f',
'c2VwID0gbmV4dCgoayBmb3IgayBpbiAoInBoYW5fY2FjaCIsICJkYXVfcGhhbl9jYWNoIiwgInNlcCIpIGlmIGsgaW4gc2ln',
'LnBhcmFtZXRlcnMpLCBOb25lKQogICAgaWYgdGVuX3NlcCBpcyBOb25lOgogICAgICAgICMgS2hvbmcgY28gdGhhbSBzbyB0',
'aGkgdHJlbiBXaW5kb3dzIEtIT05HIGNvbiBkdW9uZyBuYW8gdGFjaCBoYWkgZ2lhIHRodXlldC4KICAgICAgICBpZiBvcy5w',
'YXRoc2VwID09ICI7IjoKICAgICAgICAgICAgcmV0dXJuIChLREQsICJ0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAn',
'OycgdmEgaGFtIGtob25nIG5oYW4gdGhhbSBzbyBkYXUgcGhhbiBjYWNoICIKICAgICAgICAgICAgICAgICAgICAgICAgICIt',
'PiBraG9uZyB0YWNoIGR1b2MgaGFpIGdpYSB0aHV5ZXQiLAogICAgICAgICAgICAgICAgICAgIHsib3MucGF0aHNlcCI6IG9z',
'LnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IE5vbmV9KQogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5',
'KCkgYXMgdDoKICAgICAgICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUiOyBsYS5ta2RpcigpCiAgICAgICAgICAgIGQsIGN3',
'LCBwZiA9IF9zYW4odCkKICAgICAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04',
'IikKICAgICAgICAgICAgciwgXyAgPSBnb2kocGF0aD1zdHIobGEpICsgb3MucGF0aHNlcCArIHN0cihkKSwgcHJvZ3JhbV9m',
'aWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAgcjAsIF8gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1f',
'ZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAga3EgPSB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhh',
'bSBzbyBzZXAiOiBOb25lLAogICAgICAgICAgICAgICJjbyBtdWMgY2h1YSAnOyciOiAiTkhBTiIgaWYgciBlbHNlICJOb25l',
'IiwKICAgICAgICAgICAgICAiZG9pIGNodW5nIGR1b25nIChraG9uZyBjbyAnOycpIjogIk5IQU4iIGlmIHIwIGVsc2UgIk5v',
'bmUifQogICAgICAgIGlmIG5vdCByMDoKICAgICAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nIiwg',
'a3EKICAgICAgICByZXR1cm4gKERBVCBpZiByIGVsc2UgVFJVT1QpLCAoIiIgaWYgciBlbHNlICJtdWMgZ2l0LmV4ZSBob3Ag',
'bGUgYmkgTUFUIiksIGtxCgogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGxh',
'ID0gUGF0aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKSAgICAgICAgICAjICc7JyBuYW0gdHJvbmcgVEVOLCBraG9uZyBwaGFp',
'IGRhdSBwaGFuIGNhY2gKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90',
'ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBub2kgPSBzdHIobGEpICsgVEhVX04xMCArIHN0cihkKQogICAg',
'ICAgIGt3ID0gZGljdChwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgIHJfY2hpbmgsIF8gPSBn',
'b2kocGF0aD1ub2ksICAgICAgKip7dGVuX3NlcDogVEhVX04xMH0sICAgKiprdykgICAjIHRhY2ggZHVuZyAgLT4gTkhBTgog',
'ICAgICAgIHJfZHVvbmcsIF8gPSBnb2kocGF0aD1zdHIoZCksICAgKip7dGVuX3NlcDogVEhVX04xMH0sICAgKiprdykgICAj',
'IGRvaSBjaHVuZyBkdW9uZwogICAgICAgIHJfcGhhbmJpZXQsIF8gPSBnb2kocGF0aD1ub2ksICAgKip7dGVuX3NlcDogb3Mu',
'cGF0aHNlcH0sICoqa3cpICAjIHRhY2ggdGhlbyBvcy5wYXRoc2VwIC0+IG1hdAogICAga3EgPSB7Im9zLnBhdGhzZXAiOiBv',
'cy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiB0ZW5fc2VwLCAiZGF1IHRodSI6IFRIVV9OMTAsCiAgICAgICAgICBmIm5vaSBi',
'YW5nIHtUSFVfTjEwIXJ9LCB7dGVuX3NlcH09e1RIVV9OMTAhcn0iOiAgICAgICAiTkhBTiIgaWYgcl9jaGluaCBlbHNlICJO',
'b25lIiwKICAgICAgICAgIGYiZG9pIGNodW5nIGR1b25nIChtb3QgbXVjLCB7dGVuX3NlcH09e1RIVV9OMTAhcn0pIjogICJO',
'SEFOIiBpZiByX2R1b25nIGVsc2UgIk5vbmUiLAogICAgICAgICAgZiJwaGFuIGJpZXQ6IG5vaSBiYW5nIHtUSFVfTjEwIXJ9',
'LCB7dGVuX3NlcH09e29zLnBhdGhzZXAhcn0iOiAiTkhBTiIgaWYgcl9waGFuYmlldCBlbHNlICJOb25lIn0KICAgIGlmIG5v',
'dCByX2R1b25nOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogbW90IG11YyBob3AgbGUgbWEg',
'a2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgIyBDb25nIHBoYWkgQ08gVEhFIGRvLiBOZXUgY2EgaGFpIGRhdSBwaGFu',
'IGNhY2ggZGV1IHJhIE5IQU4gdGhpIHBoZXAgZG8ga2hvbmcgcGhhbgogICAgIyBiaWV0IGR1b2MgZ2kg4oCUIGR1bmcgYmFv',
'IERBVCwgYmFvIHRoYW5nIGxhIGtob25nIGRvIGR1b2MuCiAgICBpZiByX3BoYW5iaWV0OgogICAgICAgIHJldHVybiAoS0RE',
'LCBmInBoZXAgZG8gS0hPTkcgcGhhbiBiaWV0IGR1b2M6IG5vaSBiYW5nIHtUSFVfTjEwIXJ9IG1hIHRhY2ggdGhlbyAiCiAg',
'ICAgICAgICAgICAgICAgICAgIGYie29zLnBhdGhzZXAhcn0gVkFOIHRpbSByYSBnaXQuZXhlIiwga3EpCiAgICByZXR1cm4g',
'KChEQVQsICIiLCBrcSkgaWYgcl9jaGluaCBlbHNlCiAgICAgICAgICAgIChUUlVPVCwgZiJ0YWNoIHRoZW8gb3MucGF0aHNl',
'cCB0aGF5IHZpIHRoZW8ge3Rlbl9zZXB9IGR1b2MgdHJ1eWVuIiwga3EpKQoKCmRlZiBkb19uMTEoZ29pLCBzaWcsIHRlcHQp',
'OgogICAgIiIiVHJ1eWVuIGNoYW5fZG9hbiA9PiB0aHUgZHVvYyB0aG9uZyBiYW8gVkEgc3RkZXJyIElNLiBLaG9uZyB0cnV5',
'ZW4gPT4gc3RkZXJyIFZBTiBjby4iIiIKICAgIGlmICJjaGFuX2RvYW4iIG5vdCBpbiBzaWcucGFyYW1ldGVyczoKICAgICAg',
'ICByZXR1cm4gS0RELCAiX2dpdF93aW5kb3dzIGtob25nIG5oYW4gdGhhbSBzbyBjaGFuX2RvYW4iLCB7InRoYW0gc28iOiBs',
'aXN0KHNpZy5wYXJhbWV0ZXJzKX0KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAg',
'ICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0',
'Zi04IikKICAgICAgICBjZCA9IFtdCiAgICAgICAgXywgZV9jbyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1z',
'dHIocGYpLCBjd2Q9c3RyKGN3KSwgY2hhbl9kb2FuPWNkKQogICAgICAgIF8sIGVfa2ggPSBnb2kocGF0aD1zdHIoZCksIHBy',
'b2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICBrcSA9IHsiY2hhbl9kb2FuIHRodSBkdW9jIChtdWMpIjog',
'bGVuKGNkKSwKICAgICAgICAgICJzdGRlcnIga2hpIENPIGNoYW5fZG9hbiAoYnl0ZSkiOiBsZW4oZV9jby5lbmNvZGUoKSks',
'CiAgICAgICAgICAic3RkZXJyIGtoaSBLSE9ORyB0cnV5ZW4gKGJ5dGUpIjogbGVuKGVfa2guZW5jb2RlKCkpfQogICAgaWYg',
'bGVuKGNkKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPT0gMDoKICAgICAgICByZXR1cm4gS0RELCAibmhhbmggJVBy',
'b2dyYW1GaWxlcyUga2hvbmcgcGhhbiBnaWFpIEtIT05HIGJheSByYSBjaGFuIGRvYW4gbmFvIC0+IGNodWEgZG8gZHVvYyIs',
'IGtxCiAgICBvayA9IGxlbihjZCkgPiAwIGFuZCBsZW4oZV9jby5lbmNvZGUoKSkgPT0gMCBhbmQgbGVuKGVfa2guZW5jb2Rl',
'KCkpID4gMAogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBr',
'cQoKZGVmIGRvX24xMihnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW5nIHNlbnRpbmVsIGdpdF9wYXRoIHRyb25nIGZpeHR1',
'cmUgcGhhaSB0dXlldCBkb2kgdHJlbiBDQSBIQUkgbmVuLiIiIgogICAgbmQgPSB0ZXB0LnJlYWRfdGV4dChlbmNvZGluZz0i',
'dXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiKQogICAgaGFuZyA9IHNvcnRlZChzZXQocmUuZmluZGFsbChyJ2dpdF9wYXRoXHMq',
'PVxzKiIoW14iXSspIicsIG5kKSkpCiAgICB4YXUgPSBbaCBmb3IgaCBpbiBoYW5nIGlmIG5vdCAoUHVyZVBvc2l4UGF0aCho',
'KS5pc19hYnNvbHV0ZSgpIGFuZCBQdXJlV2luZG93c1BhdGgoaCkuaXNfYWJzb2x1dGUoKSldCiAgICBrcSA9IHsiaGFuZyBn',
'aXRfcGF0aCB0aW0gdGhheSI6IGhhbmcsICJjaGkgdHV5ZXQgZG9pIE1PVCBuZW4iOiB4YXV9CiAgICBpZiBub3QgaGFuZzoK',
'ICAgICAgICByZXR1cm4gS0RELCAia2hvbmcgdGltIHRoYXkgaGFuZyBnaXRfcGF0aCBuYW8gdHJvbmcgZml4dHVyZSAtPiBt',
'YXUgZG9jIGNvIHRoZSBkYSBkb2kiLCBrcQogICAgcmV0dXJuIChEQVQgaWYgbm90IHhhdSBlbHNlIFRSVU9UKSwgKCIiIGlm',
'IG5vdCB4YXUgZWxzZSBmImNoaS1tb3QtbmVuOiB7eGF1fSIpLCBrcQoKUFJPQkUgPSBbKCJOOCBidW9jIDEgY2hpIG5oYW4g',
'Z2l0LmV4ZSIsIGRvX244KSwKICAgICAgICAgKCJOOSBib2MgbmhheSBrZXAgbyBtdWMgUEFUSCIsIGRvX245KSwKICAgICAg',
'ICAgKCJOMTAgZGF1ICc7JyB0cm9uZyB0ZW4gdGh1IG11YyIsIGRvX24xMCksCiAgICAgICAgICgiTjExIGNoYW4gZG9hbiBk',
'b2kga2VuaCIsIGRvX24xMSksCiAgICAgICAgICgiTjEyIGhhbmcgc2VudGluZWwgdHV5ZXQgZG9pIENBIEhBSSBuZW4iLCBk',
'b19uMTIpXQoKIyAtLS0gY2hlIGRvIFRVIEtJRU06IGNoYXkgbmFtIHByb2JlIHRyZW4gbW90IGNheSBiYXQga3ksIG5lbiBi',
'YXQga3kgLS0tCmlmICItLXR1LWtpZW0tcHJvYmUiIGluIHN5cy5hcmd2OgogICAgX2cgPSBQYXRoKHN5cy5hcmd2W3N5cy5h',
'cmd2LmluZGV4KCItLXR1LWtpZW0tcHJvYmUiKSArIDFdKS5yZXNvbHZlKCkKICAgIF9zcCA9IGltcG9ydGxpYi51dGlsLnNw',
'ZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF90ayIsIHN0cihfZy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQogICAgX2xw',
'ID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3ApOyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9scCkKICAg',
'IF9zaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShfbHAuX2dpdF93aW5kb3dzKQogICAgZGVmIF9nb2koKiprdyk6CiAgICAgICAg',
'ZSA9IGlvLlN0cmluZ0lPKCkKICAgICAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgogICAgICAgICAg',
'ICByZXR1cm4gX2xwLl9naXRfd2luZG93cygqKmt3KSwgZS5nZXR2YWx1ZSgpCiAgICBwcmludChmIlRVIEtJRU0gUFJPQkUg',
'dHJlbiB7X2d9ICAobmVuIHtzeXMucGxhdGZvcm19KSIpCiAgICBmb3IgX3RlbiwgX2YgaW4gUFJPQkU6CiAgICAgICAgX3R0',
'LCBfY3QsIF9kbCA9IF9mKF9nb2ksIF9zaWcsIF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIHBy',
'aW50KGYiICBbe190dDoxNH1dIHtfdGVufSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgICAgIGZvciBf',
'aywgX3YgaW4gKF9kbCBvciB7fSkuaXRlbXMoKTogcHJpbnQoZiIgICAgICAgIHtfazozNH06IHtfdn0iKQogICAgc3lzLmV4',
'aXQoMCkKCiMgLS0tIGNoZSBkbyBLSUVNIERPTkcgQk86IHRlcCAucHkgbmF5IHBoYWkgVFJVTkcgVFVORyBCWVRFIHZvaSBi',
'YW4gbmh1bmcgdHJvbmcgcHMxIC0tLQojIEtob25nIGNvbmcgbmFvIGJ1b2MgaGFpIGJhbiBzYW8ga2hvcDogZG8gZHVvYywg',
'bm9pIHRyYW4gMi80MDAgLT4gOTkvOTk5OTkgQ0hJIHRyb25nIC5weQojIHRoaSBjaV9kYW5nX2t5IGxhbiB0MjYvdDI3IHZh',
'biB4YW5oLCBjb24gY2hvdCBTSEEgY3VhIHBzMSBjaGkgc28gYmFuIG5odW5nIHZvaSBoYW5nIHNvCiMgY3VhIENISU5IIG5v',
'LiBDaGF5OiBweXRob24gd3A1NDEtZG8tZzItd2luZG93cy5weSAtLWtpZW0tZG9uZy1ibyB3cDU0MS1kby1nMi5wczEgIChy',
'YyAwfDMpCmlmICItLWtpZW0tZG9uZy1ibyIgaW4gc3lzLmFyZ3Y6CiAgICBpbXBvcnQgYmFzZTY0CiAgICBfcHMgPSBQYXRo',
'KHN5cy5hcmd2W3N5cy5hcmd2LmluZGV4KCItLWtpZW0tZG9uZy1ibyIpICsgMV0pLnJlYWRfdGV4dChlbmNvZGluZz0iYXNj',
'aWkiKQogICAgX20gPSByZS5zZWFyY2gociIoP21zKV5cJEI2NCA9IEBcKCguKj8pXlwpIiwgX3BzKQogICAgX2sgPSByZS5z',
'ZWFyY2gociIoP20pXlwkU2hhQm9Eb1xzKj1ccyonKFswLTlhLWZdezY0fSknIiwgX3BzKQogICAgX25odW5nID0gYmFzZTY0',
'LmI2NGRlY29kZSgiIi5qb2luKHJlLmZpbmRhbGwociInKFtBLVphLXowLTkrLz1dKiknIiwgX20uZ3JvdXAoMSkpKSkgaWYg',
'X20gZWxzZSBiIiIKICAgIF90b2kgPSBQYXRoKF9fZmlsZV9fKS5yZWFkX2J5dGVzKCkKICAgIF9vayA9IGJvb2woX20gYW5k',
'IF9rKSBhbmQgX25odW5nID09IF90b2kgYW5kIGhhc2hsaWIuc2hhMjU2KF90b2kpLmhleGRpZ2VzdCgpID09IF9rLmdyb3Vw',
'KDEpCiAgICBpbm4oZiJLSUVNIERPTkcgQk86IHtEQVQgaWYgX29rIGVsc2UgS0REfSAgKG5odW5nIHtsZW4oX25odW5nKX0g',
'Ynl0ZSwgdGVwIHtsZW4oX3RvaSl9IGJ5dGUpIikKICAgIHN5cy5leGl0KDAgaWYgX29rIGVsc2UgMykKCmlubigiPSIgKiA3',
'OCk7IGlubigiV1A1NDEgZzIgLSBwaGVwIGRvIHRyZW4gV2luZG93cyB0aGF0IChzcGVjIHIzOiBOMS1ONCwgTjgtTjEyLCBO',
'Nywga2ljaCB0aHVvYykiKTsgaW5uKCI9IiAqIDc4KQoKIyAtLS0tLS0tLS0tLS0tLS0tIHR1IGtpZW0gYm8gZG9jIC0tLS0t',
'LS0tLS0tLS0tLS0KX2QsIF9nLCBfdCA9IGRvY19kbyhfTUFVKQpfb2sgPSAobGVuKF9kKSA9PSAyIGFuZCBhbnkoeC5zdGFy',
'dHN3aXRoKCJ0MDJiIikgZm9yIHggaW4gX2QpCiAgICAgICBhbmQgbm90IGFueSh4LnN0YXJ0c3dpdGgoInQxMzEiKSBmb3Ig',
'eCBpbiBfZCkgYW5kIF90KQppbm4oIlR1IGtpZW0gYm8gZG9jIGxvZzoiLCBEQVQgaWYgX29rIGVsc2UgVFJVT1QpCmlmIG5v',
'dCBfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IGJvIGRvYyBsb2cgY3VhIGNoaW5oIHNjcmlwdCBuYXkg',
'c2FpIC0+IGtob25nIGRvIGdpIGNhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDAuIG5lbiBkbyAtLS0t',
'LS0tLS0tLS0tLS0tCmdvYyA9IFBhdGgoc3lzLmFyZ3ZbMV0pLnJlc29sdmUoKSBpZiBsZW4oc3lzLmFyZ3YpID4gMSBlbHNl',
'IFBhdGguY3dkKCkKdGVwLCB0ZXB0ID0gZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaC5weSIsIGdvYyAvICJvcHMiIC8g',
'ImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIKaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIwLiBORU4gRE8iKQojIE1PSSBM',
'T0cgUEhBSSBUVSBLSEFJIG5vIGRvIENBSSBHSSBiYW5nIEJPIERPIE5BTy4gQmFpIGhvYyAxOS0wOS0yMDI2OiBtb3QgbHVv',
'dCBkbwojIGd1aSB2ZSBkdW9jIGRvYyBuaHUga2V0IHF1YSBjdWEgYmFuIHZhIGRhbmcgeGV0LCBuaHVuZyB0aGF0IHJhIGxh',
'IGJhbiBkbyBDVSBjaGF5CiMgdHJlbiBuaGFuaCBLSEFDLiBEb2MgcmEgdGhpIG1hdCBtb3Qgdm9uZzsgbG9nIHR1IGtoYWkg',
'dGhpIHRoYXkgbmdheSBkb25nIGRhdS4KdHJ5OgogICAgX3R1ID0gaGFzaGxpYi5zaGEyNTYoUGF0aChfX2ZpbGVfXykucmVh',
'ZF9ieXRlcygpKS5oZXhkaWdlc3QoKQpleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAgX3R1ID0gZiJraG9uZyB0dSBiYW0g',
'ZHVvYzoge19lfSIKZ2hpKCJib19kb19zaGEyNTYiLCBfdHUpCmlubihmIiAgQk8gRE8gICAgICAgIDogc2hhMjU2IHtfdHVb',
'OjE2XX0gIChiYW4ge0JBTl9CT19ET30pIikKaW5uKCIgIHN5cy5wbGF0Zm9ybSA6Iiwgc3lzLnBsYXRmb3JtLCAifCBweXRo',
'b24iLCBzeXMudmVyc2lvbi5zcGxpdCgpWzBdKQppbm4oIiAgb3MucGF0aHNlcCAgIDoiLCByZXByKG9zLnBhdGhzZXApLCAi',
'fCBQQVRIRVhUOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlBBVEhFWFQiKSlbOjYwXSkKaW5uKCIgIFByb2dyYW1GaWxlcyA6',
'IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUHJvZ3JhbUZpbGVzIikpLCAifCBTeXN0ZW1Sb290OiIsIHJlcHIob3MuZW52aXJv',
'bi5nZXQoIlN5c3RlbVJvb3QiKSkpCmlubigiICBDT05HX0NVX0dJVCAgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIkNPTkdf',
'Q1VfR0lUIikpKQppbm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5vbmUKaWYgc3lzLnBsYXRmb3JtID09',
'ICJ3aW4zMiI6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4gPSBib29sKGN0eXBlcy53aW5kbGwuc2hl',
'bGwzMi5Jc1VzZXJBbkFkbWluKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXllbiA9IE5vbmUKZ2hpKCJxdXllbl9hZG1p',
'biIsIHF1eWVuKQpzeW1saW5rX2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5',
'KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgi',
'KQogICAgICAgIHRyeTogb3Muc3ltbGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJsayIpKTsgc3ltbGlua19kdW9jID0gVHJ1',
'ZQogICAgICAgIGV4Y2VwdCBPU0Vycm9yIGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZhbHNlOyBnaGkoInN5bWxpbmtfbG9pIiwg',
'ZiJ7dHlwZShlKS5fX25hbWVfX306IHtlfSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZTogZ2hpKCJzeW1saW5rX2xvaSIsIHN0',
'cihlKSkKZ2hpKCJzeW1saW5rX2R1b2MiLCBzeW1saW5rX2R1b2MpCmlubigiICBBZG1pbmlzdHJhdG9yOiIsIHF1eWVuLCAi',
'fCB0YW8gc3ltbGluayBkdW9jOiIsIHN5bWxpbmtfZHVvYykKCmxvaSA9IFtdCiMgQ29uZyBraWNoIHRodW9jIGxhIHBoZXAg',
'ZG8gdHJlbiBMSUNIIFNVIEdJVCwga2hvbmcgZGluaCBnaSBkZW4gbmVuLiBDaG8gcGhlcAojIC0tY2hpLWtpY2gtdGh1b2Mg',
'Y2hheSBvIG1vaSBuZW4gZGUgY29uIFRVIEtJRU0gZHVvYyBjaGluaCBjb25nIG5heSAoZGEgZHVuZwojIGRlIHRhaSBkdW5n',
'IGNhIGhhaSB2ZSBjdWEgc3UgY28gbmVuLWN1IDE5LTA5KS4gTW9pIGNob3QgQ0hVQyBOQU5HIHZhbiBkb2kgV2luZG93cy4K',
'aWYgc3lzLnBsYXRmb3JtICE9ICJ3aW4zMiIgYW5kICItLWNoaS1raWNoLXRodW9jIiBub3QgaW4gc3lzLmFyZ3Y6CiAgICBs',
'b2kuYXBwZW5kKGYiS0hPTkcgcGhhaSBXaW5kb3dzIChzeXMucGxhdGZvcm09e3N5cy5wbGF0Zm9ybSFyfSkiKQppZiBub3Qg',
'dGVwLmlzX2ZpbGUoKTogIGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB9IikKaWYgbm90IHRlcHQuaXNfZmlsZSgpOiBs',
'b2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwdH0iKQppZiBub3Qgc2h1dGlsLndoaWNoKCJnaXQiKTogbG9pLmFwcGVuZCgi',
'a2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCIpCgpyYywgaGVhZCwgXyA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAiSEVBRCIp',
'CmlmIHJjOiBsb2kuYXBwZW5kKCJraG9uZyBkb2MgZHVvYyBIRUFEIikKZ2hpKCJoZWFkIiwgaGVhZCkKcmNfYSwgXywgXyA9',
'IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIi0taXMtYW5jZXN0b3IiLCBTSEFfRzEsIGhlYWQgb3IgIkhFQUQiKQpsYV9oYXVf',
'ZHVlID0gKHJjX2EgPT0gMCkKaWYgaGVhZCA9PSBTSEFfRzE6CiAgICB0aGVfaGUgPSAiZzEiOyBpbm4oZiIgIEhFQUQgPSB7',
'aGVhZFs6OF19IC0+IERBWSBMQSBnMS4gQ0hVQSBjbyBiYW4gdmEgZzI7IGtldCBxdWEgZHVvaSBsYSBORU4gRE8uIikKZWxp',
'ZiBsYV9oYXVfZHVlOgogICAgdGhlX2hlID0gImcyIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBoYXUgZHVlIGN1',
'YSBnMSAoe1NIQV9HMVs6OF19KTsgdW5nIHZpZW4gZzIgaGF5IGtob25nOiBONycgKG11YyAxKSBkaW5oIGRhbmguIikKZWxz',
'ZToKICAgIHRoZV9oZSA9ICI/IjsgbG9pLmFwcGVuZChmIkhFQUQ9e2hlYWRbOjhdfSBLSE9ORyBwaGFpIGcxIHZhIEtIT05H',
'IHBoYWkgaGF1IGR1ZSBjdWEge1NIQV9HMVs6OF19IOKAlCByZWJhc2U/IG5oYW0gbmhhbmg/IikKZ2hpKCJ0aGVfaGUiLCB0',
'aGVfaGUpCnJjX3IsIHJlZnMsIF8gPSBnaXQoZ29jLCAiZm9yLWVhY2gtcmVmIiwgIi0tcG9pbnRzLWF0IiwgaGVhZCBvciAi',
'SEVBRCIsCiAgICAgICAgICAgICAgICAgICAgIi0tZm9ybWF0PSUocmVmbmFtZTpzaG9ydCkiKQpkc3IgPSBbeCBmb3IgeCBp',
'biByZWZzLnNwbGl0bGluZXMoKSBpZiB4LnN0cmlwKCkgYW5kIHguc3RyaXAoKSAhPSAiZG8tdGFtIl0KZ2hpKCJyZWZfdHJv',
'X3RvaV9oZWFkIiwgZHNyKQppbm4oZiIgIHJlZiB0cm8gdG9pIEhFQUQ6IHsnLCAnLmpvaW4oZHNyKSBpZiBkc3IgZWxzZSAn',
'KGtob25nIHJlZiBuYW8gLSBIRUFEIHJvaSB0dSBkbyknfSIpCgppZiBsb2k6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERP',
'IERVT0M6IG5lbiBkbyBzYWksIEtIT05HIGluIGtldCBsdWFuIG5hby4iKQogICAgZm9yIHggaW4gbG9pOiBpbm4oIiAgLSIs',
'IHgpCiAgICBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDEuIGtpY2ggdGh1b2MgKE43JyBjdWEgc3BlYyByMykg',
'LS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjEuIEtJQ0ggVEhVT0Mg4oCUIHRyYW4gc3Bl',
'YyByMzogPD0gMiB0ZXAgdmEgPD0gNDAwIGRvbmcgdGhlbSIpCiMgVkUgTkVOIFBIQUkgVFVPSSDigJQgdmEgcGhhaSBDSFVO',
'RyBNSU5IIGR1b2MgbGEgdHVvaSwga2hvbmcgcGhhaSBnaWEgZGluaC4KIyBCYWkgaG9jIHRyYSBnaWEgMTktMDktMjAyNjog',
'Y2xvbmUgdGFpIGR1bmcgY2hpIGZldGNoIG5oYW5oIGJhbiB2YSwgYG9yaWdpbi9tYXN0ZXJgCiMgZHVuZyB5ZW4gdHUgMTQt',
'MDkgKGMxNmJkMzIsIHNhdSA5NyBjb21taXQpLiBtZXJnZS1iYXNlIHJvaSB2ZSBkdW5nIGRpbmggbWFzdGVyIGN1LAojIG5l',
'biBkaWZmIE5VT1QgY2EgOTcgY29tbWl0IG1hc3RlcjogZG8gcmEgNDYgdGVwIC8gKzcxMTggdGhheSB2aSAyIHRlcCAvICsz',
'OTcg4oCUCiMgQ1VORyBNT1QgQ09NTUlUIDBlYTk1ZGUuIE1vdCB0aWV1IGNoaSBERUxUQSBtYSB2ZSBuZW4ga2hvbmcgdHVv',
'aSB0aGkga2hvbmcgc2FpCiMgbGVjaCBtb3QgY2h1dCwgbm8gc2FpIGNhIG1vdCBiYWMgZG8gbG9uLgojIENobyBuZW46IG5l',
'biBraG9uZyBjaHVuZyBtaW5oIGR1b2MgbGEgdHVvaSA9PiBLSE9ORyBETyBEVU9DIChyYz0zKSwgS0hPTkcgcGhhaSBUUlVP',
'VC4KIyBUUlVPVCBsYSBtb3QgUEhBTiBRVVlFVCB2ZSBiYW4gdmE7IHBoYW4gcXV5ZXQgY2hpIGR1b2MgcGhlcCBwaGF0IHJh',
'IGtoaSBkYSBkbyBkdW9jLgpyY191LCB1cmxfdGhvLCBfID0gZ2l0KGdvYywgInJlbW90ZSIsICJnZXQtdXJsIiwgIm9yaWdp',
'biIpCnVybF9vLCB1cmxfaW4gPSBfdXJsX3NhY2godXJsX3RobyksIF91cmxfaW4odXJsX3RobykKZ2hpKCJvcmlnaW5fdXJs',
'IiwgdXJsX2luKTsgaW5uKGYiICBvcmlnaW4gICAgICAgOiB7dXJsX2luIG9yICcoa2hvbmcgZG9jIGR1b2MpJ30iKQp1cmxf',
'b2sgPSAobm90IHJjX3UpIGFuZCB1cmxfby5yc3RyaXAoIi8iKSBpbiBVUkxfS0hPX0hPUF9MRQpyY19sciwgb3V0X2xyLCBl',
'cl9sciA9IGdpdChnb2MsICJscy1yZW1vdGUiLCAib3JpZ2luIiwgInJlZnMvaGVhZHMvbWFzdGVyIikgaWYgdXJsX29rIGVs',
'c2UgKDEsICIiLCAiIikKZXJfbHIgPSBfYW5fdXNlcmluZm8oZXJfbHIpCnJjX2xtLCBsbSwgZXJfbG0gICAgID0gZ2l0KGdv',
'YywgInJldi1wYXJzZSIsICJvcmlnaW4vbWFzdGVyIikKcm0gPSBvdXRfbHIuc3BsaXQoKVswXSBpZiAobm90IHJjX2xyIGFu',
'ZCBvdXRfbHIuc3RyaXAoKSkgZWxzZSAiIgppZiBub3QgdXJsX29rOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwg',
'ZiJvcmlnaW49e3VybF9pbiFyfSBLSE9ORyBwaGFpIGtobyB0aGF0IOKAlCAndHVvaScgc28gdm9pIG5vIGtob25nIGNodW5n',
'IG1pbmggZHVvYyBnaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIG5vdCBybToKICAgIGtl',
'dCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJraG9uZyBob2kgZHVvYyBtYXN0ZXIgdHJlbiByZW1vdGUgKGxz',
'LXJlbW90ZSByYz17cmNfbHJ9KToge2VyX2xyWzo2MF19ICIKICAgICAgICBmIuKAlCBraG9uZyBjaHVuZyBtaW5oIGR1b2Mg',
'dmUgbmVuIGNvbiB0dW9pIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgcmNfbG0gb3Igbm90',
'IGxtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyBkb2MgZHVvYyBvcmlnaW4vbWFzdGVyIHRyb25n',
'IGNsb25lOiB7ZXJfbG1bOjYwXX0iKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBsbSAhPSBy',
'bToKICAgICMgRGVtIHhlbSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRlbSBkdW9jIOKAlCBjb24gc28gbmF5IG5vaSBybyBtdWMg',
'ZG8gc2FpIGxlY2guCiAgICByY19jLCBzYXUsIF8gPSBnaXQoZ29jLCAicmV2LWxpc3QiLCAiLS1jb3VudCIsIGYie2xtfS4u',
'e3JtfSIpCiAgICB4YSA9IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1pdCIgaWYgKG5vdCByY19jIGFuZCBzYXUuc3RyaXAoKS5p',
'c2RpZ2l0KCkpIGVsc2UgIiIKICAgIGlubihmIiAgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZSA6IHtsbVs6MTJdfSIpCiAg',
'ICBpbm4oZiIgIG1hc3RlciB0cmVuIHJlbW90ZSAgICAgICAgOiB7cm1bOjEyXX17eGF9IikKICAgIGdoaSgibWFzdGVyX2Ns',
'b25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAg',
'ICAgZiJ2ZSBuZW4gQ1U6IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19ICE9IHJlbW90ZT17cm1bOjEyXX17eGF9ICIKICAgICAg',
'ICBmIuKAlCBjaGF5IGBnaXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2luIG1hc3RlcmAgcm9pIGRvIGxhaSIpCiAgICByY19tYiwg',
'bWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbHNlOgogICAgaW5uKGYiICB2ZSBuZW4gVFVPSTogb3JpZ2luL21hc3RlciA9',
'IHtsbVs6MTJdfSA9PSBtYXN0ZXIgdHJlbiByZW1vdGUiKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFz',
'dGVyX3JlbW90ZSIsIHJtKQogICAgcmNfbWIsIG1iLCBlcl9tYiA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIm9yaWdpbi9t',
'YXN0ZXIiLCBoZWFkKQppZiByY19tYiBvciBub3QgbWI6CiAgICBpZiBtYiA9PSAiIiBhbmQgcm0gYW5kIGxtID09IHJtOgog',
'ICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9jIG1lcmdlLWJhc2Ugdm9pIG9yaWdp',
'bi9tYXN0ZXI6IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgogICAgZ2hpKCJtZXJnZV9iYXNlIiwg',
'bWIpCiAgICBpbm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7bWJbOjEyXX0iKQogICAgaWYgbWIg',
'IT0gU0hBX0JBU0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2UgbWEgc3BlYyByMyBraGFpICh7U0hB',
'X0JBU0VfU1BFQ1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQogICAgICAgIGlubigiICAgICAgICAg',
'RG8gc28gYmFzZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcgdmFvLiBEdW5nIG1lcmdlLWJhc2UgbW9pIGxhIHZpZWMg',
'Y3VhIGV4ZWN1dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJkaWZmIiwgIi0tbnVtc3RhdCIsIFNI',
'QV9CQVNFX1NQRUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAgICAgICAgICAgIGggPSBbbC5zcGxpdCgiXHQiKSBm',
'b3IgbCBpbiBuc194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICAgICAgICAgIGEgPSBzdW0oaW50KHhbMF0pIGZv',
'ciB4IGluIGggaWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdoaSgibnVtc3RhdF90aGVvX2Jhc2Vfc3BlYyIsIHsi',
'dGVwIjogbGVuKGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBpbm4oZiIgICAgICAgICAoZG9pIGNoaWV1OiBzbyBiYXNl',
'IHNwZWMgPSB7bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkgS0hPTkcgZHVuZyBkZSBjaGFtKSIpCiAgICByYywg',
'bnMsIGVyID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgbWIsIGhlYWQpCmlmIHJjOgogICAgcGFzcwplbHNlOgog',
'ICAgaGFuZyA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICB0aGVt',
'ID0gc3VtKGludChoWzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdpdCgpKQogICAgeG9hICA9IHN1bShpbnQoaFsx',
'XSkgZm9yIGggaW4gaGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgic29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hpKCJk',
'b25nX3RoZW0iLCB0aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZvciBoIGluIGhhbmc6IGlubihmIiAgICB7aFsy',
'XTozNH0gK3toWzBdOjw1fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05HOiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhlbX0s',
'IC17eG9hfSAgICh0cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcgdGhlbSkiKQogICAgY2hhbSA9IHNv',
'cnRlZCh7aFsyXSBmb3IgaCBpbiBoYW5nfSAmIFdSSVRFX1NFVF9HMik7IGdoaSgiY2hhbV93cml0ZV9zZXQiLCBjaGFtKQog',
'ICAgZGVmIF9jYV9tb2lfY28ocmV2KToKICAgICAgICByXywgbmRfLCBfID0gZ2l0KGdvYywgInNob3ciLCBmIntyZXZ9Om9w',
'cy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIHJldHVybiBOb25lIGlmIHJfIGVsc2Uge3QgZm9yIHQgaW4gQ0Ff',
'TU9JX0cyIGlmIHJlLnNlYXJjaChyIig/bSleZGVmICIgKyB0ICsgciJbYS16XT9fIiwgbmRfKX0KICAgIG9fbWIsIG9faCA9',
'IF9jYV9tb2lfY28obWIpLCBfY2FfbW9pX2NvKGhlYWQpCiAgICBtYW5nID0gc29ydGVkKG9faCAtIG9fbWIsIGtleT1zb19j',
'YSkgaWYgKG9fbWIgaXMgbm90IE5vbmUgYW5kIG9faCBpcyBub3QgTm9uZSkgZWxzZSBOb25lCiAgICBnaGkoImNhX21vaV9n',
'Ml9tYW5nX3ZhbyIsIG1hbmcpCiAgICBpZiBub3QgbWFuZzoKICAgICAgICAjIERvIFJPTkcgKGRhIGxhbmQsIGNoaW5oIG1h',
'c3RlciksIG5oYW0gbmhhbmgsIGhheSBuaGFuaCBjdWEgcGFja2V0IEtIQUMgY2hhbSBjdW5nIHRlcDoKICAgICAgICAjIGto',
'b25nIG1hbmcgY2EgbW9pIG5hbyBjdWEgZzIgdGhpIGtob25nIHBoYWkgdW5nIHZpZW4uIERvYyBraG9uZyBkdW9jIChOb25l',
'KSBjdW5nIHZheS4KICAgICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImRvaSB0dW9uZyBraG9uZyBwaGFpIHVu',
'ZyB2aWVuOiB7bGVuKGhhbmcpfSB0ZXAsIGNoYW0ge2NoYW19LCBjYSBtb2kgIgogICAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgICAgIGYiZzIgbWFuZyB2YW8ge21hbmchcn0g4oCUIGRhIGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPyIp',
'CiAgICBlbHNlOgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBEQVQgaWYgKGxlbihoYW5nKSA8PSBUUkFOX1RFUCBh',
'bmQgdGhlbSA8PSBUUkFOX0RPTkcpIGVsc2UgVFJVT1QsCiAgICAgICAgICAgIGYie2xlbihoYW5nKX0gdGVwIC8gK3t0aGVt',
'fSIpCgojIERpbmggZGFuaCBUSEFUIG5hbSBvIE43JyAoY2EgbW9pIGcyIG1hbmcgdmFvKSwgS0hPTkcgbyAiaGF1IGR1ZSBn',
'MSI6IGcxIGRhIGxhbmQgbmVuIG1vaSBuaGFuaCBkZXUKIyBsYSBoYXUgZHVlLiBEb25nIGRhdSBraG9pIGRhbiBwaGFpIHR1',
'IGtoYWkgdGhlbyBrZXQgcXVhIGF5IChkbyBkdW9jOiBtYXN0ZXIgNDQ2MjBlOCBtbyBraG9pIGJhbmcKIyAiVEhFIEhFIERP',
'IERVT0M6IGcyIiwgSlNPTiAidGhlX2hlIjogImcyIiwgdHJvbmcga2hpIE43JyBkYSBrZXQgbHVhbiAia2hvbmcgcGhhaSB1',
'bmcgdmllbiIpLgojIE5oYW4gY2hpIGR1b2Mgbm9pIERVTkcgY2FpIGRvIGR1b2M6IGBbXWAga2hvbmcgdGFjaCAiZGEgbGFu',
'ZCIga2hvaSAibmhhbSBuaGFuaCIvInBhY2tldCBraGFjIiAoZG8KIyBkdW9jIHRyZW4gMjAyNi0wOS0zMGI6IHVuZyB2aWVu',
'IDJhNjc5NjggREEgTEFORCBiaSBnb2kgIktIT05HIHBoYWkgdW5nIHZpZW4gZzIiKS4KaWYgdGhlX2hlID09ICJnMiIgYW5k',
'IG5vdCBzby5nZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpOgogICAgdGhlX2hlID0gKCJLSE9ORyBtYW5nIGNhIG1vaSBnMiBu',
'YW8gKGRhIGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPykiIGlmIHNvLmdldCgiY2FfbW9pX2cyX21hbmdfdmFvIikg',
'PT0gW10KICAgICAgICAgICAgICBlbHNlICJnMj8gKENIVUEgZGluaCBkYW5oIGR1b2MgZG9pIHR1b25nKSIpCiAgICBnaGko',
'InRoZV9oZSIsIHRoZV9oZSkKCiMgQ29uZyBuaGFuaDogZG8gUklFTkcga2ljaCB0aHVvYyAodmFpIGdpYXkpIHJvaSBkdW5n',
'LiBEdW5nIGtoaSBjYW4geGFjIG1pbmggbGFpCiMgdmUgbmVuIG1hIGtob25nIG11b24gdHJhIDIwLTQ1IHBodXQgY2hvIGNh',
'IGJvIHRlc3QuCmlmICItLWNoaS1raWNoLXRodW9jIiBpbiBzeXMuYXJndjoKICAgIGlubigiIik7IGlubigiPSIgKiA3OCkK',
'ICAgIGlubigiLS1jaGkta2ljaC10aHVvYzogQ0hJIGRvIGNvbmcga2ljaCB0aHVvYy4gRGF5IEtIT05HIHBoYWkgbW90IGx1',
'b3QgbmdoaWVtIHRodS4iKQogICAgaW5uKCItIiAqIDc4KQogICAgZm9yIF90LCBfdHQsIF9jdCBpbiBjaG90OiBpbm4oZiIg',
'IHtfdHQ6MTR9IHtfdH0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgIF9rID0gc3VtKDEgZm9yIF8sIHQs',
'IF8gaW4gY2hvdCBpZiB0ID09IEtERCkKICAgIF9yID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9U',
'KQogICAgc3lzLmV4aXQoMyBpZiBfayBlbHNlICgxIGlmIF9yIGVsc2UgMCkpCgpDSElfUFJPQkUgPSAiLS1jaGktcHJvYmUi',
'IGluIHN5cy5hcmd2ICAgICMgYm8gcXVhIGJvIHRlc3QgKyBONzsgZ2l1IDAsIDEsIDMKIyAtLS0tLS0tLS0tLS0tLS0tIDIu',
'IGJvIHRlc3QgZGF5IGR1IC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIg',
'KiA3OCk7IGlubigiMi4gQk8gVEVTVCBEQVkgRFUgKDEwLTQwIHBodXQpIikKICAgIHJjX24sIG91dF9uID0gY2hheShbIm9w',
'cy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgZ29jKQogICAgZ2hpKCJyY19zdWl0ZSIsIHJjX24pCiAgICBtID0gUlhfVE9O',
'Ry5zZWFyY2gob3V0X24pCiAgICBpbm4oIiAgcmMgPSIsIHJjX24sICJ8IiwgbS5ncm91cCgwKSBpZiBtIGVsc2UgIihLSE9O',
'RyBkb2MgZHVvYyBkb25nIHRvbmcga2V0KSIpCiAgICBpZiBtOgogICAgICAgIGdoaSgiZGF0IiwgaW50KG0uZ3JvdXAoMSkp',
'KTsgZ2hpKCJ0cmVuIiwgaW50KG0uZ3JvdXAoMikpKTsgZ2hpKCJib19xdWFfc28iLCBpbnQobS5ncm91cCg0KSkpCiAgICBk',
'b19oZXQsIGdjLCB0aW4gPSBkb2NfZG8ob3V0X24pCiAgICBnaGkoInNvX2NhX2RvIiwgbGVuKGRvX2hldCkpOyBnaGkoImxp',
'ZXRfa2VfZGF5X2R1IiwgdGluKQogICAgZm9yIGcgaW4gZ2M6IGlubigiICAgKiIsIGcpCiAgICBpbm4oIiIpOyBpbm4oZiIg',
'ID09PSB7bGVuKGRvX2hldCl9IENBIERPID09PSIpCiAgICBmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgog',
'ICAgICAgIGlubihmIiAgIHt0LnNwbGl0KCdfJylbMF06N30ge3R9Iik7IGlubihmIiAgICAgICAgICAge2RvX2hldFt0XVs6',
'MTUwXX0iKQogICAgZ2hpKCJkb19seV9kbyIsIHt0OiBkb19oZXRbdF1bOjMwMF0gZm9yIHQgaW4gZG9faGV0fSkKICAgICMg',
'LS0tLSBDSE9UOiBtb2kgY2EgRE8gcGhhaSBHSUFJIFRISUNIIERVT0MgLS0tLQogICAgIyBUaGlldSBjaG90IG5heSwgYm8g',
'ZG8gaW4gZGFuaCBzYWNoIGRvIHJvaSB2YW4gdGhvYXQgcmM9MC4gRG8gZHVuZyBsYSBsb2kgZGEgeGF5IHJhOgogICAgIyBs',
'dW90IFdpbmRvd3MgMTktMDkgY28gdDE3MSBETyBtYSBibyBkbyBiYW8gIkRBVCAxMCB8IFRSVU9UIDAiIHZhIHJjPTAuCiAg',
'ICBkZWYgX2tob2EodCk6IHJldHVybiB0LnNwbGl0KCJfIilbMF0KICAgIGRvX3BhY2tldCwgZG9fbGEsIGRvX3RoaWV1X2Nv',
'bmdfY3UgPSBbXSwgW10sIFtdCiAgICBmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGssIGx5',
'ID0gX2tob2EodCksIGRvX2hldFt0XQogICAgICAgIGlmIGsgaW4gQ0FfUEFDS0VUOiAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgIGRvX3BhY2tldC5hcHBlbmQodCkKICAgICAgICBlbGlmICJLSMOUTkcgxJBPIMSQxq/hu6JDIiBpbiBseSBvciAi',
'dGhp4bq/dSBgIiBpbiBseTogIGRvX3RoaWV1X2NvbmdfY3UuYXBwZW5kKHQpCiAgICAgICAgZWxpZiBrIGluIE5HT0FJX1BI',
'QU1fVkk6ICAgICAgICAgICAgICAgICAgICAgICAgcGFzcwogICAgICAgIGVsc2U6ICAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgICAgICAgICAgICAgIGRvX2xhLmFwcGVuZCh0KQogICAgZ2hpKCJkb19wYWNrZXQiLCBkb19wYWNrZXQpOyBnaGko',
'ImRvX2xhIiwgZG9fbGEpOyBnaGkoImRvX3RoaWV1X2NvbmdfY3UiLCBkb190aGlldV9jb25nX2N1KQogICAgaW5uKCIiKQog',
'ICAgaW5uKGYiICBjYSBETyB0aHVvYyBDSElOSCBwYWNrZXQgbmF5IDoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRd',
'IG9yICdraG9uZyBjbyd9IikKICAgIGlubihmIiAgY2EgRE8gbmdvYWkgcGhhbSB2aSAocjMga2hhaSk6IHtbX2tob2EoeCkg',
'Zm9yIHggaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKSBpZiBfa2hvYSh4KSBpbiBOR09BSV9QSEFNX1ZJXX0iKQogICAg',
'aW5uKGYiICBjYSBETyB2aSBUSElFVSBDT05HIENVICAgICAgIDoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb190aGlldV9jb25n',
'X2N1XSBvciAna2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERPIExBIChraG9uZyBnaWFpIHRoaWNoIGR1b2MpOiB7W19r',
'aG9hKHgpIGZvciB4IGluIGRvX2xhXSBvciAna2hvbmcgY28nfSIpCiAgICAjIC0tLS0gQ0hPVDogcGhlcCBkbyBwaGFpIFRS',
'T04gdHJ1b2Mga2hpIG1vdCBjaHUgREFUIG5hbyBkdW9jIHBoYXQgLS0tLQogICAgIyBCYW4gdHJ1b2MgY2hpIElOIGB0aW5g',
'L2ByY19zdWl0ZWA6IGJvIHRlc3QgY2hldCBnaXVhIHQxNzEgKHJjPTEzNCwga2hvbmcgZG9uZyB0b25nKQogICAgIyB2YW4g',
'cmEgIkRBVCAxMiB8IFRSVU9UIDAiIHJjPTA7IGNhIFBBQ0tFVCB2YW5nIG1hdCBoYXkgYmkgQk8gUVVBIGN1bmcgZHVvYyBj',
'aGFtIG5odQogICAgIyAia2hvbmcgZG8iLiBWYW5nIG1hdCBraG9uZyBwaGFpICJraG9uZyBkbyIg4oCUIGxhIEtIT05HIERP',
'IERVT0MuCiAgICB2YW5nID0gW3QgZm9yIHQgaW4gc29ydGVkKENBX1BBQ0tFVCwga2V5PXNvX2NhKSBpZiBtYXVfY2Eob3V0',
'X24sIHQpIG5vdCBpbiAoIlFVQSIsICJETyIpXQogICAgbHlfa2RkID0gW10KICAgIGlmIG5vdCB0aW46IGx5X2tkZC5hcHBl',
'bmQoImRhbmggc2FjaCBkbyBLSE9ORyBkYXkgZHUiKQogICAgaWYgcmNfbiBub3QgaW4gKDAsIDEpIG9yIChyY19uID09IDEp',
'ICE9IGJvb2woZG9faGV0KToKICAgICAgICBseV9rZGQuYXBwZW5kKGYicmMgYm8gdGVzdD17cmNfbn0ga2hvbmcga2hvcCB7',
'bGVuKGRvX2hldCl9IGNhIERPIGRvYyBkdW9jIikKICAgIGlmIHZhbmc6IGx5X2tkZC5hcHBlbmQoZiJjYSBQQUNLRVQgdmFu',
'Zy9ibyBxdWE6IHt2YW5nfSIpCiAgICBnaGkoImNhX3BhY2tldF92YW5nIiwgdmFuZyk7IGdoaSgibHlfZG9fY2h1YV90cm9u',
'IiwgbHlfa2RkKQogICAgaWYgbHlfa2RkOiBrZXQoIkJvIHRlc3QgY2hheSBUUk9OIHZhIGRvYyBEVSIsIEtERCwgIjsgIi5q',
'b2luKGx5X2tkZCkpCiAgICBjaHVhX3Ryb24gPSBLREQgaWYgbHlfa2RkIGVsc2UgREFUCiAgICBrZXQoIktob25nIGNhIG5h',
'byBjdWEgUEFDS0VUIGJpIERPIiwgY2h1YV90cm9uIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBUUlVPVCwKICAgICAgICAiIiBp',
'ZiBub3QgZG9fcGFja2V0IGVsc2UgZiJETzoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdfSDigJQgYmFuIHZhIENI',
'VUEgeG9uZyIpCiAgICBrZXQoIk1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jIiwgY2h1YV90cm9uIGlmIG5vdCBkb19s',
'YSBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19sYSBlbHNlIGYibGE6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9f',
'bGFdfSIpCiAgICBpZiBkb190aGlldV9jb25nX2N1OgogICAgICAgIGtldCgiQ29uZyBjdSBkYXkgZHUgZGUgZG8iLCBLREQs',
'IGYidGhpZXUgY29uZyBjdSBjaG8ge1tfa2hvYSh4KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XX0iKQoKICAgIGJxID0g',
'c29ydGVkKHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91dF9uKX0sIGtleT1zb19jYSk7IGdoaSgiY2FfYm9f',
'cXVhIiwgYnEpCiAgICBpbm4oIiIpOyBpbm4oZiIgIEJPIFFVQSAoe2xlbihicSl9KToge1t4LnNwbGl0KCdfJylbMF0gZm9y',
'IHggaW4gYnFdfSIpCgogICAgaW5uKCIiKTsgaW5uKCIgIE4xLU40ICh0MTY1LXQxNjgpLCB0aWV1IGNoaSBuZ2hpZW0gdGh1',
'IGN1YSByMiwgbmF5IGxhIGNoaSBiYW8gaG9pIHF1eToiKQogICAgYjQgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBp',
'biBDQU1PSX07IGdoaSgiY2FfbW9pIiwgYjQpCiAgICBmb3IgdCBpbiBDQU1PSTogaW5uKGYiICAgICB7dH06IHtiNFt0XX0i',
'KQogICAgIyBCT19RVUEvdmFuZyBsYSBDSFVBIENIQVksIGtob25nIHBoYWkgRE86IGNoaSBtb3QgY2EgRE8gbW9pIGR1b2Mg',
'cGhhdCBUUlVPVC4KICAgIGtldCgiTjEtTjQgKHQxNjUtdDE2OCkiLCBEQVQgaWYgYWxsKHYgPT0gIlFVQSIgZm9yIHYgaW4g',
'YjQudmFsdWVzKCkpCiAgICAgICAgZWxzZSAoVFJVT1QgaWYgYW55KHYgPT0gIkRPIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkg',
'ZWxzZSBLREQpLCBzdHIoYjQpKQoKICAgIGlubigiIik7IGlubigiICAxNSBjYSB0dW5nIGRvIHRyZW4gQ0k6IikKICAgIGIx',
'NSA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBMTV9OyBnaGkoImNhMTUiLCBiMTUpCiAgICBpbm4oIiAgICAi',
'ICsgIiAgIi5qb2luKGYie3R9OntiMTVbdF19IiBmb3IgdCBpbiBDQTE1KSkKCiAgICAjIHQxMzYg4oCUIE4xMiBkbyBHSUFO',
'IFRJRVAgcXVhIGtldCBxdWEgY2EKICAgIHQxMzZfdGVuID0gbmV4dCgodCBmb3IgdCBpbiBkb19oZXQgaWYgdC5zdGFydHN3',
'aXRoKCJ0MTM2IikpLCBOb25lKQogICAgaWYgYjE1LmdldCgidDEzNiIpID09ICJRVUEiOgogICAgICAgIGtldCgiTjEyIHQx',
'MzYgKHF1YSBrZXQgcXVhIGNhKSIsIERBVCwgInQxMzYgUVVBIikKICAgIGVsaWYgYjE1LmdldCgidDEzNiIpICE9ICJETyI6',
'CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgS0RELCBmInQxMzYgPSB7YjE1LmdldCgndDEzNicp',
'IXJ9IOKAlCBraG9uZyBjaGF5L2tob25nIHRoYXkiKQogICAgZWxzZToKICAgICAgICBseSA9IGRvX2hldC5nZXQodDEzNl90',
'ZW4sICIiKQogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIFRSVU9ULCBmIkRPOiB7bHlbOjkwXX0i',
'KQoKIyAtLS0tLS0tLS0tLS0tLS0tIDMuIHByb2JlIFRIQU5HIHZhbyBoYW0gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBp',
'bm4oIi0iICogNzgpOyBpbm4oIjMuIFBST0JFIFRIQU5HIOKAlCBnb2kgX2dpdF93aW5kb3dzIHZvaSB0aGFtIHNvIHRpZW0i',
'KQpzcGVjID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwNTQxIiwgc3RyKHRlcCkpCmxwID0g',
'aW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhzcGVjKTsgc3BlYy5sb2FkZXIuZXhlY19tb2R1bGUobHApCnNpZyA9',
'IGluc3BlY3Quc2lnbmF0dXJlKGxwLl9naXRfd2luZG93cykKZ2hpKCJ0aGFtX3NvX19naXRfd2luZG93cyIsIGxpc3Qoc2ln',
'LnBhcmFtZXRlcnMpKQppbm4oIiAgdGhhbSBzbyBjdWEgX2dpdF93aW5kb3dzOiIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQoK',
'ZGVmIGdvaSgqKmt3KToKICAgICIiIkdvaSBfZ2l0X3dpbmRvd3MsIEJBVCBzdGRlcnIgZGUgbW90IGRvbmcgY2hhbiBkb2Fu',
'IGtob25nIGdpZXQgbHVvdCBkby4iIiIKICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJl',
'Y3Rfc3RkZXJyKGUpOgogICAgICAgIHIgPSBscC5fZ2l0X3dpbmRvd3MoKiprdykKICAgIHJldHVybiByLCBlLmdldHZhbHVl',
'KCkKCiMgLS0tIGRvaSBjaHVuZyByaWc6IHBoYWkgdHJhIGxvaSBkdW5nIG1vdCBjYSB0YSBCSUVUIFRSVU9DIGRhcCBhbiAt',
'LS0Kd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgbmdvYWkgPSBQYXRoKHQpLyJuZ29haSI7',
'IG5nb2FpLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1r',
'ZGlyKCkKICAgIChuZ29haS8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjEsIF8g',
'PSBnb2kocGF0aD1zdHIobmdvYWkpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgKGN3LyJnaXQu',
'ZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMiwgXyA9IGdvaShwYXRoPXN0cihjdyksIHBy',
'b2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCnJpZ19vayA9IGJvb2wocjEpIGFuZCByMiBpcyBOb25lCmdoaSgi',
'cmlnX2RvaV9jaHVuZyIsIHJpZ19vaykKa2V0KCJSSUcgZG9pIGNodW5nIChiaWV0IHRydW9jIGRhcCBhbikiLCBEQVQgaWYg',
'cmlnX29rIGVsc2UgS0RELAogICAgZiJuZ29haS1jd2QtPnsnTkhBTicgaWYgcjEgZWxzZSAnTm9uZSd9IHwgdHJvbmctY3dk',
'LT57J05IQU4nIGlmIHIyIGVsc2UgJ05vbmUnfSIpCmlmIG5vdCByaWdfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERP',
'IERVT0M6IHJpZyBzYWksIG1vaSBjaG90IGR1b2kgc2Ugdm8gbmdoaWEuIik7IHN5cy5leGl0KDMpCgojIC0tLSBNT0kgQ09O',
'RyBQSEFJIFRVIENIVU5HIE1JTkggTk8gQ08gVEhFIERPIC0tLQojIEJhaSBob2MgZGF0IG5oYXQgY3VhIHBhY2tldCBuYXk6',
'IGRvX24xMCBiYW4gY3UgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxCiMgY3VhIGNoaW5oIGJhbiB2YSBh',
'eSBETyB2aSBkdW5nIGtodXlldCB0YXQgbWEgTjEwIHNpbmggcmEgZGUgYmF0LiBObyBkZWdlbmVyYXRlIOKAlAojIHRyZW4g',
'V2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyBuZW4gInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gY3VuZyBrZXQg',
'cXVhLgojIE1vdCBjb25nIGtob25nIHRoZSBETyB0aGkga2hvbmcgcGhhaSBjb25nLCB2YSBubyBuZ3V5IGhpZW0gaG9uIGto',
'b25nIGNvIGNvbmc6IG5vCiMgcGhhdCByYSBtb3QgY2h1IERBVC4KIwojIE5lbiB0cnVvYyBraGkgRFVORyBuYW0gY29uZyBu',
'YXkgZGUgcGhhbiBxdXlldCwgYmF0IHR1bmcgY29uZyBnaWV0IG1vdCBkb3QgYmllbiBkYQojIGJpZXQgdHJvbmcuIENvbmcg',
'bmFvIGtob25nIGdpZXQgZHVvYyB0aGkgY2h1IERBVCBjdWEgbm8gYmkgSEEgeHVvbmcgS0hPTkcgRE8gRFVPQzsKIyBUUlVP',
'VCBnaXUgbmd1eWVuIChxdWFuIHNhdCB0cnVjIHRpZXAsIHZkLiBnMSB2YW4gbmhhbiBnaXQuYmF0KS4gRG90IGJpZW4gY2hh',
'eSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaQojIGR1bmcgdG9pIChjdW5nIGt5IGx1YXQgbmh1IE43KS4K',
'RE9UX0JJRU5fVFVfS0lFTSA9IFsKICAgICgiTjgiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICdpZiBjaGlfZGlu',
'aCBhbmQgUGF0aChjaGlfZGluaCkubmFtZS5sb3dlcigpID09ICJnaXQuZXhlIiBhbmQgaG9wX2xlKGNoaV9kaW5oKTonLAog',
'ICAgICJpZiBjaGlfZGluaCBhbmQgaG9wX2xlKGNoaV9kaW5oKToiKSwKICAgICgiTjkiLCAib3BzL2xlYXNlX3B1Ymxpc2gu',
'cHkiLAogICAgICJkID0gZF9yYXcuc3RyaXAoKS5zdHJpcCgnXCInKSIsICJkID0gZF9yYXcuc3RyaXAoKSIpLAogICAgKCJO',
'MTAiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJzZXAgPSBvcy5wYXRoc2VwIGlmIHBoYW5fY2FjaCBpcyBOb25l',
'IGVsc2UgcGhhbl9jYWNoIiwgInNlcCA9IG9zLnBhdGhzZXAiKSwKICAgICgiTjExIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5',
'IiwgImlmIGNoYW5fZG9hbiBpcyBub3QgTm9uZToiLCAiaWYgRmFsc2U6IiksCiAgICAoIk4xMiIsICJvcHMvbGVhc2VfcHVi',
'bGlzaF90ZXN0LnB5IiwKICAgICAnZ2l0X3BhdGg9Ii8va2hvbmctY28vZ2l0IicsICdnaXRfcGF0aD0iL2tob25nLWNvL2dp',
'dCInKSwKXQppbm4oIiIpOyBpbm4oIiAgdHUga2llbSBjb25nIOKAlCBtb2kgY29uZyBwaGFpIGdpZXQgZHVvYyBtb3QgZG90',
'IGJpZW4gZGEgYmlldDoiKQpnaWV0ID0ge30KZm9yIG1hLCBkdW9uZywgdGltLCB0aGF5IGluIERPVF9CSUVOX1RVX0tJRU06',
'CiAgICBfdGVuLCBfaGFtID0gbmV4dCgoKGEsIGIpIGZvciBhLCBiIGluIFBST0JFIGlmIGEuc3RhcnRzd2l0aChtYSArICIg',
'IikpLCAoTm9uZSwgTm9uZSkpCiAgICBpZiBfaGFtIGlzIE5vbmU6CiAgICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIg',
'ICAge21hOjR9IEtIT05HIERPIERVT0M6IGtob25nIHRpbSB0aGF5IHByb2JlIHRlbiAne21hfSAuLi4nIik7IGNvbnRpbnVl',
'CiAgICB0cnk6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyBfdDoKICAgICAgICAgICAg',
'X2MgPSBQYXRoKF90KS8iY2F5Ijsgc2h1dGlsLmNvcHl0cmVlKGdvYy8ib3BzIiwgX2MvIm9wcyIpCiAgICAgICAgICAgIF9m',
'ID0gX2MvZHVvbmc7IF9uZCA9IF9mLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBpZiBfbmQuY291',
'bnQodGltKSAhPSAxOgogICAgICAgICAgICAgICAgZ2lldFttYV0gPSBOb25lCiAgICAgICAgICAgICAgICBpbm4oZiIgICAg',
'e21hOjR9IEtIT05HIERPIERVT0M6IG1hdSBkb3QgYmllbiBraG9wIHtfbmQuY291bnQodGltKX0gbGFuIChtb25nIDEpIgog',
'ICAgICAgICAgICAgICAgICAgIGYiIOKAlCBtYSBuZ3VvbiBkYSBkb2ksIGRvdCBiaWVuIG5heSBoZXQgeSBuZ2hpYSIpOyBj',
'b250aW51ZQogICAgICAgICAgICBfZi53cml0ZV90ZXh0KF9uZC5yZXBsYWNlKHRpbSwgdGhheSwgMSksIGVuY29kaW5nPSJ1',
'dGYtOCIpCiAgICAgICAgICAgIF9zcCA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF9kYl8i',
'ICsgbWEsIHN0cihfYy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQogICAgICAgICAgICBfbSA9IGltcG9ydGxpYi51dGls',
'Lm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbSkKICAgICAgICAgICAgZGVmIF9nb2lf',
'ZGIoKiprdyk6CiAgICAgICAgICAgICAgICBfZSA9IGlvLlN0cmluZ0lPKCkKICAgICAgICAgICAgICAgIHdpdGggY29udGV4',
'dGxpYi5yZWRpcmVjdF9zdGRlcnIoX2UpOgogICAgICAgICAgICAgICAgICAgIHJldHVybiBfbS5fZ2l0X3dpbmRvd3MoKipr',
'dyksIF9lLmdldHZhbHVlKCkKICAgICAgICAgICAgX3R0LCBfY3QsIF8gPSBfaGFtKF9nb2lfZGIsIGluc3BlY3Quc2lnbmF0',
'dXJlKF9tLl9naXRfd2luZG93cyksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBfYy8ib3BzIi8ibGVhc2VfcHVi',
'bGlzaF90ZXN0LnB5IikKICAgICAgICBnaWV0W21hXSA9IChfdHQgPT0gVFJVT1QpCiAgICAgICAgaW5uKGYiICAgIHttYTo0',
'fSBkb3QgYmllbiAtPiB7X3R0OjE0fSB7J0dJRVQgRFVPQycgaWYgX3R0ID09IFRSVU9UIGVsc2UgJ1NPTkcgU09UJ30iCiAg',
'ICAgICAgICAgICsgKGYiICAgKHtfY3R9KSIgaWYgX2N0IGVsc2UgIiIpKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToK',
'ICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzoge3R5cGUoX2UpLl9fbmFt',
'ZV9ffToge19lfSIpCmdoaSgiY29uZ19naWV0X2R1b2NfZG90X2JpZW4iLCBnaWV0KQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwp',
'IGluIFsodCwgZihnb2ksIHNpZywgdGVwdCkpIGZvciB0LCBmIGluIFBST0JFXToKICAgIGdoaSgicHJvYmVfIiArIHRlbi5z',
'cGxpdCgpWzBdLmxvd2VyKCksIGRsKQogICAgaWYgaXNpbnN0YW5jZShkbCwgZGljdCk6CiAgICAgICAgZm9yIGssIHYgaW4g',
'ZGwuaXRlbXMoKTogaW5uKGYiICAgIHtrOjM0fToge3Z9IikKICAgIG1hID0gdGVuLnNwbGl0KClbMF0KICAgIGlmIGdpZXQu',
'Z2V0KG1hKSBpcyBub3QgVHJ1ZSBhbmQgdHQgPT0gREFUOgogICAgICAgICMgREFUIHR1IG1vdCBjb25nIGNodWEgY2h1bmcg',
'bWluaCBkdW9jIGxhIGJpZXQgRE8gdGhpIGtob25nIGRhbmcgdGluIGhvbiBLREQuCiAgICAgICAga2V0KHRlbiwgS0RELCBm',
'ImNvbmcgS0hPTkcgZ2lldCBkdW9jIGRvdCBiaWVuIGN1YSBjaGluaCBubyAoe2dpZXQuZ2V0KG1hKSFyfSkiCiAgICAgICAg',
'ICAgICAgICAgICAgICBmIiAtPiBjaHUgREFUIG5heSBraG9uZyBjbyBnaWEgdHJpIikKICAgIGVsc2U6CiAgICAgICAga2V0',
'KHRlbiwgdHQsIGN0KQoKIyAtLS0tLS0tLS0tLS0tLS0tIDQuIE43IGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gLS0tLS0t',
'LS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCI0LiBONyDigJQg',
'ZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAoY2F5IHRoYXQgS0hPTkcgYmkgZHVuZyB0b2kpIikKICAgIHRydW9jID0gdGVw',
'LnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKQogICAgZ2hpKCJuN190cnVvYyIsIHRydW9jKTsg',
'aW5uKGYiICBzbyBkb25nIGtob3Age01BVV9XSU4hcn06IFRSVU9DID0ge3RydW9jfSBbbW9uZyAxXSIpCiAgICBpZiB0cnVv',
'YyAhPSAxOgogICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgZiJtYXUgeHVhdCBoaWVuIHt0',
'cnVvY30gbGFuLCBraG9uZyBwaGFpIDEiKQogICAgZWxzZToKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVj',
'dG9yeSgpIGFzIHRtcDoKICAgICAgICAgICAgc2FvID0gUGF0aCh0bXApLyJjYXkiCiAgICAgICAgICAgIHNodXRpbC5jb3B5',
'dHJlZShnb2MsIHNhbywgaWdub3JlPXNodXRpbC5pZ25vcmVfcGF0dGVybnMoIi5naXQiLCAiX19weWNhY2hlX18iLCAiKi5w',
'eWMiKSkKICAgICAgICAgICAgZjIgPSBzYW8vIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiCiAgICAgICAgICAgIGYyLndyaXRl',
'X3RleHQoZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJlcGxhY2UoTUFVX1dJTiwgImlmIEZhbHNlOiIpLCBlbmNv',
'ZGluZz0idXRmLTgiKQogICAgICAgICAgICBzYXUgPSBmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFV',
'X1dJTik7IGdoaSgibjdfc2F1Iiwgc2F1KQogICAgICAgICAgICBpbm4oZiIgIFNBVSAoZGEgZG90IGJpZW4pID0ge3NhdX0g',
'W21vbmcgMF0iKQogICAgICAgICAgICBpZiBzYXUgIT0gMDoKICAgICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhh',
'bmggV2luZG93cyIsIEtERCwgImRvdCBiaWVuIEtIT05HIGFwIGR1b2MiKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAg',
'ICAgICAgcmNfbSwgb3V0X20gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBzYW8pCiAgICAgICAgICAg',
'ICAgICBtMTY1ID0gbWF1X2NhKG91dF9tLCAidDE2NSIpOyBkbSwgXywgXyA9IGRvY19kbyhvdXRfbSkKICAgICAgICAgICAg',
'ICAgIHRlbjE2NSA9IG5leHQoKHQgZm9yIHQgaW4gZG0gaWYgdC5zdGFydHN3aXRoKCJ0MTY1IikpLCBOb25lKQogICAgICAg',
'ICAgICAgICAgbHkgPSAoZG0uZ2V0KHRlbjE2NSkgb3IgIiIpCiAgICAgICAgICAgICAgICBnaGkoIm43X3QxNjUiLCBtMTY1',
'KTsgZ2hpKCJuN19seV9kbyIsIGx5WzoyMDBdKQogICAgICAgICAgICAgICAgaW5uKGYiICB0MTY1IHNhdSBkb3QgYmllbjog',
'e20xNjV9IHwge2x5WzoxMTBdfSIpCiAgICAgICAgICAgICAgICBkdW5nX2x5X2RvID0gIlBBVEggdCIgaW4gbHkgb3IgIi91',
'c3IvYmluIiBpbiBseQogICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgREFUIGlmICht',
'MTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pIGVsc2UKICAgICAgICAgICAgICAgICAgICAoVFJVT1QgaWYgbTE2NSA9PSAi',
'RE8iIGVsc2UgS0REKSwKICAgICAgICAgICAgICAgICAgICAiZ2lldCBkdW5nIGx5IGRvIiBpZiAobTE2NSA9PSAiRE8iIGFu',
'ZCBkdW5nX2x5X2RvKQogICAgICAgICAgICAgICAgICAgIGVsc2UgKCJETyBuaHVuZyBLSE9ORyBkdW5nIGx5IGRvIC0+IHRp',
'biBkdW5nIGdpYSIgaWYgbTE2NSA9PSAiRE8iIGVsc2UgImtob25nIGRvYyBkdW9jIHQxNjUiKSkKCiMgLS0tLS0tLS0tLS0t',
'LS0tLSBLRVQgTFVBTiAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiPSIgKiA3OCkKaW5uKGYiVEhFIEhFIERPIERV',
'T0M6IHt0aGVfaGV9ICAgSEVBRD17aGVhZFs6MTJdfSIpCiMgS2hvaSBkYW4gY2hvIHJldmlld2VyIGJhdCBkYXUgbyBkb25n',
'IHRyZW4sIG5lbiBDSEUgRE8gcGhhaSBuYW0gTkdBWSBkdW9pIG5vOiBraG9uZyBjbyBkb25nIG5heQojIHRoaSBtb3QgbHVv',
'dCAtLWNoaS1wcm9iZSBpbiAiREFUIDcgfCBUUlVPVCAwIHwgS0hPTkcgRE8gRFVPQyAwIiByYz0wIG1hIGtob25nIG5vaSBs',
'YSBjaHVhIGNoYXkgYm8gdGVzdC4KZ2hpKCJjaGVfZG8iLCAiY2hpLXByb2JlIiBpZiBDSElfUFJPQkUgZWxzZSAiZGF5LWR1',
'IikKaWYgQ0hJX1BST0JFOgogICAgaW5uKCItLWNoaS1wcm9iZTogQ0hJIGRvIG11YyAwLCAxLCAzLiBCbyB0ZXN0LCBOMS1O',
'NCwgdDEzNiwgTjcgS0hPTkcgY2hheSAtIGRheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5naGllbSB0aHUuIikKaWYgdGhlX2hl',
'ID09ICJnMSI6CiAgICBpbm4oIkxVVSBZOiBkYXkgbGEgTkVOIERPIChnMSksIEtIT05HIHBoYWkgbmdoaWVtIHRodSBnMi4g',
'Q2FjIGNob3QgTjgtTjEyIGR1b2kgZGF5IikKICAgIGlubigiICAgICAgIFRSVU9UIGxhIERVTkcgTkhVIE1PTkcg4oCUIGNo',
'dW5nIGxhIG5odW5nIGxvIGcyIHNpbmggcmEgZGUgdsOhLiIpCmlubigiLSIgKiA3OCkKZm9yIHRlbiwgdHQsIGN0IGluIGNo',
'b3Q6CiAgICBpbm4oZiIgIHt0dDoxNH0ge3Rlbn0iICsgKGYiICAge2N0fSIgaWYgY3QgZWxzZSAiIikpCm5fa2RkID0gc3Vt',
'KDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKbl90cnVvdCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3Qg',
'aWYgdCA9PSBUUlVPVCkKaW5uKCItIiAqIDc4KQppbm4oZiIgIERBVCB7c3VtKDEgZm9yIF8sdCxfIGluIGNob3QgaWYgdD09',
'REFUKX0gfCBUUlVPVCB7bl90cnVvdH0gfCBLSE9ORyBETyBEVU9DIHtuX2tkZH0iKQppbm4oZiIgIFRvbmcgY2EgZG86IHtz',
'by5nZXQoJ3NvX2NhX2RvJyl9IHwgZGFuaCBzYWNoIGRheSBkdTogeydDTycgaWYgc28uZ2V0KCdsaWV0X2tlX2RheV9kdScp',
'IGVsc2UgJ0tIT05HIERPIERVT0MnfSIpCmlubihmIiAgQWRtaW5pc3RyYXRvcjoge3NvLmdldCgncXV5ZW5fYWRtaW4nKX0g',
'fCBzeW1saW5rOiB7c28uZ2V0KCdzeW1saW5rX2R1b2MnKX0iKQppbm4oIiIpOyBpbm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kg',
'SlNPTiBOQVkgVkUgQ0hPIFJFVklFV0VSIC0tLSIpCmdoaSgiY2hvdCIsIFt7InRlbiI6IGEsICJ0cmFuZ190aGFpIjogYiwg',
'ImNoaV90aWV0IjogY30gZm9yIGEsIGIsIGMgaW4gY2hvdF0pCmlubihqc29uLmR1bXBzKHNvLCBlbnN1cmVfYXNjaWk9RmFs',
'c2UsIGluZGVudD0xLCBkZWZhdWx0PXN0cikpCiMgcmM6IDAgPSBtb2kgY2hvdCBEQVQgfCAxID0gY28gY2hvdCBUUlVPVCB8',
'IDMgPSBjbyBjaG90IEtIT05HIERPIERVT0MgKHV1IHRpZW4gYmFvIGRvbmcpCnN5cy5leGl0KDMgaWYgbl9rZGQgZWxzZSAo',
'MSBpZiBuX3RydW90IGVsc2UgMCkpCg=='
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
# FETCH CA master. Bai hoc 19-09-2026 (a): clone tai dung chi fetch nhanh ban va, nen
# `origin/master` dung yen tu 14-09; merge-base roi ve dinh master cu va cong kich thuoc
# do ra 46 tep / +7118 thay cho 2 tep / +397 - CUNG MOT COMMIT. Bo do gio fail-close
# (nen cu => KHONG DO DUOC chu khong phan quyet TRUOT); day la ve con lai: lam nen tuoi.
#
# Bai hoc 19-09-2026 (b), tra gia ngay trong lan sua (a): KHONG dung FETCH_HEAD nua.
# FETCH_HEAD la trang thai NGAM do lan fetch CUOI CUNG de lai. Them mot lenh fetch phia
# tren no - dung mot dong, khong dong gi den dong checkout - da lam `checkout FETCH_HEAD`
# lay master thay vi nhanh ban va, va luot do di do nham cay. Fetch thang vao ref CO TEN
# roi checkout chinh ref do: khong con thu tu nao doi duoc ket qua.
G -C "$Kho" fetch --quiet origin "+refs/heads/master:refs/remotes/origin/master" | Out-Null
G -C "$Kho" fetch --quiet origin "+refs/heads/${Nhanh}:refs/remotes/origin/${Nhanh}" | Out-Null
$mLoc = (G -C "$Kho" rev-parse --short=12 origin/master) | Select-Object -First 1
Write-Host "nen  : origin/master = $mLoc"
G -C "$Kho" checkout --quiet -B do-tam "refs/remotes/origin/$Nhanh" | Out-Null
G -C "$Kho" reset --hard --quiet "refs/remotes/origin/$Nhanh" | Out-Null
# Chot ngay tai day, truoc khi tra 20-45 phut: cay dang o dung nhanh duoc yeu cau chua?
$hNhanh = (G -C "$Kho" rev-parse "refs/remotes/origin/$Nhanh") | Select-Object -First 1
$hHead  = (G -C "$Kho" rev-parse HEAD) | Select-Object -First 1
if ($hHead -ne $hNhanh) {
    Dung "checkout SAI CAY: HEAD=$hHead nhung $Nhanh=$hNhanh - dung lai, khong do"
}

$head = (G -C "$Kho" rev-parse --short HEAD) | Select-Object -First 1
# KHONG ghim SHA. Ban va g2 chua ton tai luc viet tep nay, va ghim mot SHA se lam
# bootstrap tu choi chay dung luc agy vua day xong. Bo do TU PHAN LOAI the he:
#   head == 2f70869a  -> g1, chua co ban va g2 (van do, nhan la NEN DO)
#   head la hau due   -> ung vien g2
#   khac              -> KHONG DO DUOC, rc=3
Write-Host "HEAD : $head   (g1 = 2f70869; bo do se tu phan loai the he)"

# ---------------------------------------------------------------- 5. chay
$tieuDe = 'Chay phep do g2 (bo test chay HAI lan - tinh 20-45 phut)'
# Bo do xet --chi-kich-thuoc TRUOC va dung o do, nen bat ca hai co thi KICH THUOC thang: tieu de phai
# theo dung thu tu ay (do tren pwsh 7.4: tieu de bao PROBE ma bo do chi do kich thuoc).
if ($ChiProbe)     { $tieuDe = 'Chi do PROBE + tu kiem cong (vai giay)' }
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
if ($ChiProbe)     { $doiSo += '--chi-probe' }
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
# In lai phan ket luan: tu dong KET LUAN cua bo do tro di. Khong tim thay thi in ca log.
# Mau cu ('CA DO doc duoc|KHONG_DO_DUOC|doi chieu bo doc') khong khop dong nao bo do
# tung in (0/8 log do duoc) nen nhanh `else` - in CA log - la nhanh duy nhat tung chay.
$dong = @(Get-Content -LiteralPath $Log -Encoding UTF8)
$i = -1
for ($k = 0; $k -lt $dong.Count; $k++) {
    if ($dong[$k] -match '^(THE HE DO DUOC:|--chi-kich-thuoc: CHI do|KHONG DO DUOC:)') { $i = $k; break }
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
