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
$ShaBoDo    = '0d66106d88b49bbfdc498cef147528137e53be856076198b0fbd371260196b05'      # SHA-256 cua bo do Python nhung ben duoi

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
'MmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0wOS0zMGIiICAgICAgICAgICAgICAjIGRvaSBNT0kga2hpIHN1YSBi',
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
'UlhfVVNFUklORk8uc3ViKHIiXDEiLCB1IG9yICIiKQojIFRob25nIGJhbyBsb2kgY3VhIGdpdCBDSEkgYm8gdXNlcmluZm8g',
'dG9pIGBAYCBEQVUgVElFTjogdXNlcmluZm8gY28gYEBgIHRyYW4gKHZkLiB0ZW4gZGFuZyBuaGFwIGxhCiMgZW1haWwpIHRo',
'aSBwaGFuIHNhdSB2YW4gcmEgc3RkZXJyIGxzLXJlbW90ZSwgbWEgc3RkZXJyIGF5IGR1b2MgaW4gdmFvIGRvbmcgS0REIGN1',
'YSBONycgKGRvIGR1b2M6CiMgMiBkb25nIHRyb25nIGxvZywgMSB0cm9uZyBraG9pIGRhbikuIExhbSBzYWNoIE1PSSBVUkwg',
'dHJvbmcgdmFuIGJhbiB0cnVvYyBraGkgaW4uCmRlZiBfYW5fdXNlcmluZm8odCk6IHJldHVybiByZS5zdWIociIoW0EtWmEt',
'el1bQS1aYS16MC05Ky4tXSo6Ly8pW15ccy8/IydcIl0qQCIsIHIiXDEiLCB0IG9yICIiKQojIENhIG5nb2FpIHBoYW0gdmkg',
'cjMgwqduZ29haV9waGFtX3ZpIOKAlCBkbyBDSElOSCBTUEVDIGtoYWksIGtob25nIHBoYWkgYm8gZG8gdHUgcXV5ZXQuCiMg',
'RG8gbGEgREFOSCBTQUNIIENITyBQSEVQOiBjYSBkbyBuYW8gS0hPTkcgbmFtIHRyb25nIGRheSB2YSBLSE9ORyBwaGFpICJ0',
'aGlldSBjb25nIGN1IgojIHRoaSBsYSBUUlVPVC4gRGFuaCBzYWNoIGNhbSB0aGkgYmFvIGdpbyBjdW5nIHRoaWV1OyBkYW5o',
'IHNhY2ggY2hvIHBoZXAgdGhpIGJpZXQgdHJ1b2MuCk5HT0FJX1BIQU1fVkkgPSBzZXQoInQxMzEgdDEzMiB0MTUwIHQxMjUg',
'dDM1IHQzNiB0MzcgdDM4IHQzOSB0NDAiLnNwbGl0KCkpCiMgQ2EgY3VhIENISU5IIHBhY2tldCBuYXkuIE1vdCBjYSBvIGRh',
'eSBtYSBETyB0aGkga2hvbmcgYmFvIGdpbyBkdW9jIGJvIHF1YS4KQ0FfUEFDS0VUID0gc2V0KCJ0MTY1IHQxNjYgdDE2NyB0',
'MTY4IHQxNjkgdDE3MCB0MTcxIHQxNzIgdDE3MyIuc3BsaXQoKSkKIyBDYSBNT0kgbWEgZzIgdGhlbSB2YW8gKE44LU4xMiku',
'IERvaSB0dW9uZyBkbyBwaGFpIE1BTkcgY2h1bmcgdmFvOiBtZXJnZS1iYXNlIGNodWEgY28sIEhFQUQgY28uCkNBX01PSV9H',
'MiA9ICJ0MTY5IHQxNzAgdDE3MSB0MTcyIHQxNzMiLnNwbGl0KCkKQ0ExNSAgPSAidDEyOSB0MTMwIHQxMzEgdDEzMiB0MTMz',
'IHQxMzYgdDEzOCB0MTM5IHQxNDQgdDE0NSB0MTQ2IHQxNDcgdDE0OSB0MTUwIHQxNTEiLnNwbGl0KCkKQ0FNT0kgPSAidDE2',
'NSB0MTY2IHQxNjcgdDE2OCIuc3BsaXQoKQoKREFULCBUUlVPVCwgS0REID0gIkRBVCIsICJUUlVPVCIsICJLSE9ORyBETyBE',
'VU9DIgpzbywgY2hvdCA9IHt9LCBbXQpkZWYgZ2hpKGssIHYpOiBzb1trXSA9IHY7IHJldHVybiB2CmRlZiBrZXQodGVuLCB0',
'cmFuZ190aGFpLCBjaGlfdGlldD0iIik6CiAgICBjaG90LmFwcGVuZCgodGVuLCB0cmFuZ190aGFpLCBjaGlfdGlldCkpCiAg',
'ICBpbm4oZiIgIFt7dHJhbmdfdGhhaToxNH1dIHt0ZW59IiArIChmIiAgIHtjaGlfdGlldH0iIGlmIGNoaV90aWV0IGVsc2Ug',
'IiIpKQogICAgcmV0dXJuIHRyYW5nX3RoYWkKCiMgLS0tLS0tLS0tLS0tLS0tLSBkb2MgbG9nIGN1YSBibyB0ZXN0IChiYW4g',
'MywgZGEgZG8gdHJlbiBsb2cgVEhBVCkgLS0tLS0tLS0tLS0tLS0tLQpSWF9ET19DSE8gID0gcmUuY29tcGlsZShyIig/bSle',
'ISEhIGRvIChcUyspICguKikkIikKUlhfRE9fQ1VPSSA9IHJlLmNvbXBpbGUociIoP20pXiB7Mn0oXFN7MSw0fSkgezJ9KFxT',
'Kyk6ICguKikkIikKUlhfQk9fUVVBICA9IHJlLmNvbXBpbGUociIoP20pXiB7Mn1cU3sxLDZ9IFFVQSAoXFMrKTogKC4qKSQi',
'KQpSWF9UT05HICAgID0gcmUuY29tcGlsZShyImxlYXNlX3B1Ymxpc2g6IChcZCspLyhcZCspXGJbXlxuXSo/PShcZCspLFte',
'XG5dKj89KFxkKykiKQoKZGVmIHNvX2NhKHQpOgogICAgbSA9IHJlLm1hdGNoKHIidChcZCspIiwgdCk7IHJldHVybiAoaW50',
'KG0uZ3JvdXAoMSkpIGlmIG0gZWxzZSAxMCoqNiwgdCkKCmRlZiBkb2NfZG8ob3V0KToKICAgIHRhaV9jaG8gPSB7dDogbC5z',
'dHJpcCgpIGZvciB0LCBsIGluIFJYX0RPX0NITy5maW5kYWxsKG91dCl9CiAgICBibyA9IHt0IGZvciB0LCBfIGluIFJYX0JP',
'X1FVQS5maW5kYWxsKG91dCl9CiAgICBjdW9pID0ge3Q6IGwuc3RyaXAoKSBmb3IgXywgdCwgbCBpbiBSWF9ET19DVU9JLmZp',
'bmRhbGwob3V0KSBpZiB0IG5vdCBpbiBib30KICAgIGhvcCA9IGRpY3QoY3VvaSk7IGhvcC51cGRhdGUodGFpX2NobykKICAg',
'IGdjLCB0aW4gPSBbXSwgVHJ1ZQogICAgaWYgc2V0KHRhaV9jaG8pICE9IHNldChjdW9pKToKICAgICAgICBnYy5hcHBlbmQo',
'ZiJoYWkgbmd1b24gTEVDSDogY2hpLXRhaS1jaG89e3NvcnRlZChzZXQodGFpX2Nobyktc2V0KGN1b2kpKX0gY2hpLWN1b2k9',
'e3NvcnRlZChzZXQoY3VvaSktc2V0KHRhaV9jaG8pKX0iKQogICAgICAgIHRpbiA9IEZhbHNlCiAgICBtID0gUlhfVE9ORy5z',
'ZWFyY2gob3V0KQogICAgaWYgbm90IG06CiAgICAgICAgZ2MuYXBwZW5kKCJLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcga2V0',
'Iik7IHRpbiA9IEZhbHNlCiAgICBlbHNlOgogICAgICAgIGRhdCwgdHJlbiA9IGludChtLmdyb3VwKDEpKSwgaW50KG0uZ3Jv',
'dXAoMikpCiAgICAgICAgZ2MuYXBwZW5kKGYic28gaG9jOiB7dHJlbn0te2RhdH09e3RyZW4tZGF0fSBkbzsgZG9jIGR1b2Mg',
'e2xlbihob3ApfSIpCiAgICAgICAgaWYgdHJlbiAtIGRhdCAhPSBsZW4oaG9wKToKICAgICAgICAgICAgZ2MuYXBwZW5kKGYi',
'TEVDSCBTTyBIT0M6IHRoaWV1IHt0cmVuLWRhdC1sZW4oaG9wKX0gY2EiKTsgdGluID0gRmFsc2UKICAgIHJldHVybiBob3As',
'IGdjLCB0aW4KCl9NQVUgPSAoIiEhISBkbyB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOIGFcbiIKICAgICAgICAiISEh',
'IGRvIHQxNTBfeCBXaW5FcnJvciAxMzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICIgIELhu44gUVVBIHQxMzFf',
'eTogbmVuIGZpeHR1cmVcbiIKICAgICAgICAiICDEkOG7jiAgdDAyYl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTjogYVxuIgog',
'ICAgICAgICIgIMSQ4buOICB0MTUwX3g6IFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAgICAgImxl',
'YXNlX3B1Ymxpc2g6IDEvMyDEkeG6oXQ7IMSRw6MgY2jhuqF5PTMsIGLhu48gcXVhPTFcbiIpCgpkZWYgY2hheShhcmd2LCBj',
'd2QsIHBodXQ9NjApOgogICAgbXQgPSBkaWN0KG9zLmVudmlyb24sIFBZVEhPTlVURjg9IjEiLCBQWVRIT05JT0VOQ09ESU5H',
'PSJ1dGYtOCIsCiAgICAgICAgICAgICAgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9IjEiLCBQWVRIT05VTkJVRkZFUkVEPSIx',
'IikKICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbc3lzLmV4ZWN1dGFibGVdICsgYXJndiwgY3dkPXN0cihjd2QpLCBjYXB0dXJl',
'X291dHB1dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3Jz',
'PSJyZXBsYWNlIiwgdGltZW91dD1waHV0KjYwLCBlbnY9bXQpCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQg',
'b3IgIiIpICsgKHAuc3RkZXJyIG9yICIiKQoKZGVmIG1hdV9jYShvdXQsIHQpOgogICAgbSA9IHJlLnNlYXJjaChyIig/bSle',
'PDw8IHJhICgiICsgdCArIHIiW2Etel0/X1xTKikgWzAtOS5dK3MgKFx3KylccyokIiwgb3V0KQogICAgcmV0dXJuIG0uZ3Jv',
'dXAoMikgaWYgbSBlbHNlIE5vbmUKCmRlZiBnaXQoZ29jLCAqYSwgcGh1dD01KToKICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihb',
'ImdpdCIsICItQyIsIHN0cihnb2MpLCAqYV0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwKICAgICAgICAgICAg',
'ICAgICAgICAgICBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjApCiAgICByZXR1',
'cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpLnN0cmlwKCksIChwLnN0ZGVyciBvciAiIikuc3RyaXAoKQoKCiMg',
'PT09PT09PT09PT09PT09PT0gTkFNIFBST0JFLCB2aWV0IHRoYW5oIEhBTSBUSFVBTiBkZSBUVSBLSUVNIGR1b2MgPT09PT09',
'PT09PT09PT09PT0KIyBNb2kgaGFtIHRyYSAodHJhbmdfdGhhaSwgY2hpX3RpZXQsIGR1X2xpZXUpLiBLSE9ORyBpbiwgS0hP',
'TkcgdGhvYXQg4oCUIG5obyB2YXkgY2h1bmcKIyBjaGF5IGR1b2MgdHJlbiBuZW4gQkFUIEtZLCB2YSBgLS10dS1raWVtLXBy',
'b2JlYCBnb2kgdGhhbmcgY2h1bmcgZGUga2llbSBjaGluaCBibyBkby4KCmRlZiBfc2FuKHQpOgogICAgZCA9IFBhdGgodCkv',
'ImQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1r',
'ZGlyKCkKICAgIHJldHVybiBkLCBjdywgcGYKCmRlZiBkb19uOChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJCdW9jIDEgKENP',
'TkdfQ1VfR0lUKSBjaGkgZHVvYyBuaGFuIGdpdC5leGUuIERvaSBjaHVuZyBkdW9uZzogZ2l0LmV4ZSBWQU4gcGhhaSBuaGFu',
'LiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQs',
'IGN3LCBwZiA9IF9zYW4odCkKICAgICAgICBmb3IgdGVuIGluICgiZ2l0LmV4ZSIsICJnaXQuYmF0IiwgImdpdC5jbWQiLCAi',
'Z2l0LnB5IiwgImtob25nLXBoYWktZ2l0LnR4dCIpOgogICAgICAgICAgICBmID0gZC90ZW47IGYud3JpdGVfdGV4dCgieCIs',
'IGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8gPSBnb2koY29uZ19jdV9naXQ9c3RyKGYpLCBwYXRoPSIiLCBw',
'cm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICBrcVtmIkNPTkdfQ1VfR0lUPXt0ZW59Il0g',
'PSAiTkhBTiIgaWYgciBlbHNlICJUVSBDSE9JIgogICAgbG90ID0gW2sgZm9yIGssIHYgaW4ga3EuaXRlbXMoKSBpZiB2ID09',
'ICJOSEFOIiBhbmQgbm90IGsuZW5kc3dpdGgoImdpdC5leGUiKV0KICAgIGlmIGtxLmdldCgiQ09OR19DVV9HSVQ9Z2l0LmV4',
'ZSIpICE9ICJOSEFOIjoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IGdpdC5leGUgaG9wIGxl',
'IG1hIGJpIHR1IGNob2kiLCBrcQogICAgcmV0dXJuIChEQVQgaWYgbm90IGxvdCBlbHNlIFRSVU9UKSwgKCIiIGlmIG5vdCBs',
'b3QgZWxzZSBmImNvbiBuaGFuOiB7bG90fSIpLCBrcQoKZGVmIGRvX245KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIk11YyBQ',
'QVRIIGJvYyBuaGF5IGtlcCBwaGFpIE5IQU47IG11YyByb25nIC8gdG9hbiBraG9hbmcgdHJhbmcgcGhhaSBibyBxdWEsIGto',
'b25nIG5lbS4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAg',
'ICAgICBkID0gUGF0aCh0KS8iY28gZ2l0IjsgZC5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBm',
'ID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rp',
'bmc9InV0Zi04IikKICAgICAgICBmb3IgbmhhbiwgbXVjIGluICgoImtob25nIG5oYXkiLCBzdHIoZCkpLCAoImNvIG5oYXkg',
'a2VwIiwgZicie2R9IicpLAogICAgICAgICAgICAgICAgICAgICAgICAgICgicm9uZyIsICIiKSwgKCJjaGkga2hvYW5nIHRy',
'YW5nIiwgIiAgICIpKToKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgciwgXyA9IGdvaShwYXRoPW11YywgcHJv',
'Z3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9ICJO',
'SEFOIiBpZiByIGVsc2UgIk5vbmUiCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgICAg',
'IGtxW2YiUEFUSCB7bmhhbn0iXSA9IGYiTkVNIHt0eXBlKGUpLl9fbmFtZV9ffSIKICAgIGlmIGtxLmdldCgiUEFUSCBraG9u',
'ZyBuaGF5IikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogbXVjIFBBVEgg',
'dGh1b25nIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EKICAgIG9rID0gKGtxLmdldCgiUEFUSCBjbyBuaGF5IGtlcCIp',
'ID09ICJOSEFOIgogICAgICAgICAgYW5kIGtxLmdldCgiUEFUSCByb25nIikgPT0gIk5vbmUiIGFuZCBrcS5nZXQoIlBBVEgg',
'Y2hpIGtob2FuZyB0cmFuZyIpID09ICJOb25lIikKICAgIHJldHVybiAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYg',
'b2sgZWxzZSAieGVtIGJhbmciKSwga3EKCiMgRGF1IHBoYW4gY2FjaCBkdW5nIERFIFRIVS4gUGhhaSBLSEFDIG9zLnBhdGhz',
'ZXAgdHJlbiBDQSBIQUkgbmVuICgnOycgV2luZG93cywgJzonIFBPU0lYKQojIHRoaSBoYWkgZ2lhIHRodXlldCAidGFjaCB0',
'aGVvIGRhdSBkdW9jIHRydXllbiIgdmEgInRhY2ggdGhlbyBvcy5wYXRoc2VwIiBtb2kgcm9pIHJhIG5oYXUuClRIVV9OMTAg',
'PSAifCIKCmRlZiBkb19uMTAoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiSGFtIHBoYWkgdGFjaCBQQVRIIHRoZW8gZGF1IHBo',
'YW4gY2FjaCBEVU9DIFRSVVlFTiwga2hvbmcgdGhlbyBvcy5wYXRoc2VwIGN1YSBuZW4uCgogICAgQmFuIGN1IGRvICJtb3Qg',
'ZGF1ICc7JyB0cm9uZyBURU4gdGh1IG11YyIgdmEgZGF0IERBVCB0cmVuIFdpbmRvd3MgZHUgaGFtIHNhaS4gTm8KICAgIGRl',
'Z2VuZXJhdGU6IHRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JywgbmVuICdDOi9hO2InIHRoYXQgc3UgQ08gTkdI',
'SUEgbGEgaGFpCiAgICBtdWMg4oCUICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIHJhIGN1bmcga2V0IHF1YSwgcGhl',
'cCBkbyBraG9uZyB0aGUgZG8gbmFvLiBObwogICAgZGEgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxIGN1',
'YSBjaGluaCBiYW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQgdGF0IGF5LgogICAgTW90IGNvbmcga2hvbmcgdGhlIGRvIHRo',
'aSBraG9uZyBwaGFpIGNvbmcuCiAgICAiIiIKICAgIHRlbl9zZXAgPSBuZXh0KChrIGZvciBrIGluICgicGhhbl9jYWNoIiwg',
'ImRhdV9waGFuX2NhY2giLCAic2VwIikgaWYgayBpbiBzaWcucGFyYW1ldGVycyksIE5vbmUpCiAgICBpZiB0ZW5fc2VwIGlz',
'IE5vbmU6CiAgICAgICAgIyBLaG9uZyBjbyB0aGFtIHNvIHRoaSB0cmVuIFdpbmRvd3MgS0hPTkcgY29uIGR1b25nIG5hbyB0',
'YWNoIGhhaSBnaWEgdGh1eWV0LgogICAgICAgIGlmIG9zLnBhdGhzZXAgPT0gIjsiOgogICAgICAgICAgICByZXR1cm4gKEtE',
'RCwgInRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyB2YSBoYW0ga2hvbmcgbmhhbiB0aGFtIHNvIGRhdSBwaGFu',
'IGNhY2ggIgogICAgICAgICAgICAgICAgICAgICAgICAgIi0+IGtob25nIHRhY2ggZHVvYyBoYWkgZ2lhIHRodXlldCIsCiAg',
'ICAgICAgICAgICAgICAgICAgeyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZX0pCiAgICAg',
'ICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgICAgICBsYSA9IFBhdGgodCkvImNv',
'O2RhdSI7IGxhLm1rZGlyKCkKICAgICAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgICAgICAoZC8iZ2l0LmV4',
'ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBfICA9IGdvaShwYXRoPXN0cihs',
'YSkgKyBvcy5wYXRoc2VwICsgc3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAg',
'ICByMCwgXyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICBr',
'cSA9IHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IE5vbmUsCiAgICAgICAgICAgICAgImNvIG11',
'YyBjaHVhICc7JyI6ICJOSEFOIiBpZiByIGVsc2UgIk5vbmUiLAogICAgICAgICAgICAgICJkb2kgY2h1bmcgZHVvbmcgKGto',
'b25nIGNvICc7JykiOiAiTkhBTiIgaWYgcjAgZWxzZSAiTm9uZSJ9CiAgICAgICAgaWYgbm90IHIwOgogICAgICAgICAgICBy',
'ZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmciLCBrcQogICAgICAgIHJldHVybiAoREFUIGlmIHIgZWxzZSBUUlVP',
'VCksICgiIiBpZiByIGVsc2UgIm11YyBnaXQuZXhlIGhvcCBsZSBiaSBNQVQiKSwga3EKCiAgICB3aXRoIHRlbXBmaWxlLlRl',
'bXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUiOyBsYS5ta2RpcigpICAgICAg',
'ICAgICMgJzsnIG5hbSB0cm9uZyBURU4sIGtob25nIHBoYWkgZGF1IHBoYW4gY2FjaAogICAgICAgIGQsIGN3LCBwZiA9IF9z',
'YW4odCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIG5v',
'aSA9IHN0cihsYSkgKyBUSFVfTjEwICsgc3RyKGQpCiAgICAgICAga3cgPSBkaWN0KHByb2dyYW1fZmlsZXM9c3RyKHBmKSwg',
'Y3dkPXN0cihjdykpCiAgICAgICAgcl9jaGluaCwgXyA9IGdvaShwYXRoPW5vaSwgICAgICAqKnt0ZW5fc2VwOiBUSFVfTjEw',
'fSwgICAqKmt3KSAgICMgdGFjaCBkdW5nICAtPiBOSEFOCiAgICAgICAgcl9kdW9uZywgXyA9IGdvaShwYXRoPXN0cihkKSwg',
'ICAqKnt0ZW5fc2VwOiBUSFVfTjEwfSwgICAqKmt3KSAgICMgZG9pIGNodW5nIGR1b25nCiAgICAgICAgcl9waGFuYmlldCwg',
'XyA9IGdvaShwYXRoPW5vaSwgICAqKnt0ZW5fc2VwOiBvcy5wYXRoc2VwfSwgKiprdykgICMgdGFjaCB0aGVvIG9zLnBhdGhz',
'ZXAgLT4gbWF0CiAgICBrcSA9IHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IHRlbl9zZXAsICJk',
'YXUgdGh1IjogVEhVX04xMCwKICAgICAgICAgIGYibm9pIGJhbmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17VEhVX04xMCFy',
'fSI6ICAgICAgICJOSEFOIiBpZiByX2NoaW5oIGVsc2UgIk5vbmUiLAogICAgICAgICAgZiJkb2kgY2h1bmcgZHVvbmcgKG1v',
'dCBtdWMsIHt0ZW5fc2VwfT17VEhVX04xMCFyfSkiOiAgIk5IQU4iIGlmIHJfZHVvbmcgZWxzZSAiTm9uZSIsCiAgICAgICAg',
'ICBmInBoYW4gYmlldDogbm9pIGJhbmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17b3MucGF0aHNlcCFyfSI6ICJOSEFOIiBp',
'ZiByX3BoYW5iaWV0IGVsc2UgIk5vbmUifQogICAgaWYgbm90IHJfZHVvbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBj',
'aHVuZyBkdW9uZyBob25nOiBtb3QgbXVjIGhvcCBsZSBtYSBraG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICAjIENvbmcg',
'cGhhaSBDTyBUSEUgZG8uIE5ldSBjYSBoYWkgZGF1IHBoYW4gY2FjaCBkZXUgcmEgTkhBTiB0aGkgcGhlcCBkbyBraG9uZyBw',
'aGFuCiAgICAjIGJpZXQgZHVvYyBnaSDigJQgZHVuZyBiYW8gREFULCBiYW8gdGhhbmcgbGEga2hvbmcgZG8gZHVvYy4KICAg',
'IGlmIHJfcGhhbmJpZXQ6CiAgICAgICAgcmV0dXJuIChLREQsIGYicGhlcCBkbyBLSE9ORyBwaGFuIGJpZXQgZHVvYzogbm9p',
'IGJhbmcge1RIVV9OMTAhcn0gbWEgdGFjaCB0aGVvICIKICAgICAgICAgICAgICAgICAgICAgZiJ7b3MucGF0aHNlcCFyfSBW',
'QU4gdGltIHJhIGdpdC5leGUiLCBrcSkKICAgIHJldHVybiAoKERBVCwgIiIsIGtxKSBpZiByX2NoaW5oIGVsc2UKICAgICAg',
'ICAgICAgKFRSVU9ULCBmInRhY2ggdGhlbyBvcy5wYXRoc2VwIHRoYXkgdmkgdGhlbyB7dGVuX3NlcH0gZHVvYyB0cnV5ZW4i',
'LCBrcSkpCgoKZGVmIGRvX24xMShnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJUcnV5ZW4gY2hhbl9kb2FuID0+IHRodSBkdW9j',
'IHRob25nIGJhbyBWQSBzdGRlcnIgSU0uIEtob25nIHRydXllbiA9PiBzdGRlcnIgVkFOIGNvLiIiIgogICAgaWYgImNoYW5f',
'ZG9hbiIgbm90IGluIHNpZy5wYXJhbWV0ZXJzOgogICAgICAgIHJldHVybiBLREQsICJfZ2l0X3dpbmRvd3Mga2hvbmcgbmhh',
'biB0aGFtIHNvIGNoYW5fZG9hbiIsIHsidGhhbSBzbyI6IGxpc3Qoc2lnLnBhcmFtZXRlcnMpfQogICAgd2l0aCB0ZW1wZmls',
'ZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0',
'LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGNkID0gW10KICAgICAgICBfLCBlX2Nv',
'ID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpLCBjaGFuX2RvYW49Y2QpCiAg',
'ICAgICAgXywgZV9raCA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAg',
'IGtxID0geyJjaGFuX2RvYW4gdGh1IGR1b2MgKG11YykiOiBsZW4oY2QpLAogICAgICAgICAgInN0ZGVyciBraGkgQ08gY2hh',
'bl9kb2FuIChieXRlKSI6IGxlbihlX2NvLmVuY29kZSgpKSwKICAgICAgICAgICJzdGRlcnIga2hpIEtIT05HIHRydXllbiAo',
'Ynl0ZSkiOiBsZW4oZV9raC5lbmNvZGUoKSl9CiAgICBpZiBsZW4oY2QpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA9',
'PSAwOgogICAgICAgIHJldHVybiBLREQsICJuaGFuaCAlUHJvZ3JhbUZpbGVzJSBraG9uZyBwaGFuIGdpYWkgS0hPTkcgYmF5',
'IHJhIGNoYW4gZG9hbiBuYW8gLT4gY2h1YSBkbyBkdW9jIiwga3EKICAgIG9rID0gbGVuKGNkKSA+IDAgYW5kIGxlbihlX2Nv',
'LmVuY29kZSgpKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPiAwCiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRS',
'VU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgpkZWYgZG9fbjEyKGdvaSwgc2lnLCB0ZXB0KToKICAgICIi',
'Ikhhbmcgc2VudGluZWwgZ2l0X3BhdGggdHJvbmcgZml4dHVyZSBwaGFpIHR1eWV0IGRvaSB0cmVuIENBIEhBSSBuZW4uIiIi',
'CiAgICBuZCA9IHRlcHQucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIpCiAgICBoYW5nID0g',
'c29ydGVkKHNldChyZS5maW5kYWxsKHInZ2l0X3BhdGhccyo9XHMqIihbXiJdKykiJywgbmQpKSkKICAgIHhhdSA9IFtoIGZv',
'ciBoIGluIGhhbmcgaWYgbm90IChQdXJlUG9zaXhQYXRoKGgpLmlzX2Fic29sdXRlKCkgYW5kIFB1cmVXaW5kb3dzUGF0aCho',
'KS5pc19hYnNvbHV0ZSgpKV0KICAgIGtxID0geyJoYW5nIGdpdF9wYXRoIHRpbSB0aGF5IjogaGFuZywgImNoaSB0dXlldCBk',
'b2kgTU9UIG5lbiI6IHhhdX0KICAgIGlmIG5vdCBoYW5nOgogICAgICAgIHJldHVybiBLREQsICJraG9uZyB0aW0gdGhheSBo',
'YW5nIGdpdF9wYXRoIG5hbyB0cm9uZyBmaXh0dXJlIC0+IG1hdSBkb2MgY28gdGhlIGRhIGRvaSIsIGtxCiAgICByZXR1cm4g',
'KERBVCBpZiBub3QgeGF1IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IHhhdSBlbHNlIGYiY2hpLW1vdC1uZW46IHt4YXV9Iiks',
'IGtxCgpQUk9CRSA9IFsoIk44IGJ1b2MgMSBjaGkgbmhhbiBnaXQuZXhlIiwgZG9fbjgpLAogICAgICAgICAoIk45IGJvYyBu',
'aGF5IGtlcCBvIG11YyBQQVRIIiwgZG9fbjkpLAogICAgICAgICAoIk4xMCBkYXUgJzsnIHRyb25nIHRlbiB0aHUgbXVjIiwg',
'ZG9fbjEwKSwKICAgICAgICAgKCJOMTEgY2hhbiBkb2FuIGRvaSBrZW5oIiwgZG9fbjExKSwKICAgICAgICAgKCJOMTIgaGFu',
'ZyBzZW50aW5lbCB0dXlldCBkb2kgQ0EgSEFJIG5lbiIsIGRvX24xMildCgojIC0tLSBjaGUgZG8gVFUgS0lFTTogY2hheSBu',
'YW0gcHJvYmUgdHJlbiBtb3QgY2F5IGJhdCBreSwgbmVuIGJhdCBreSAtLS0KaWYgIi0tdHUta2llbS1wcm9iZSIgaW4gc3lz',
'LmFyZ3Y6CiAgICBfZyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0tdHUta2llbS1wcm9iZSIpICsgMV0pLnJl',
'c29sdmUoKQogICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX3RrIiwgc3RyKF9n',
'LyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICBfbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9z',
'cCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX2xwKQogICAgX3NpZyA9IGluc3BlY3Quc2lnbmF0dXJlKF9scC5fZ2l0X3dp',
'bmRvd3MpCiAgICBkZWYgX2dvaSgqKmt3KToKICAgICAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgICAgIHdpdGggY29udGV4',
'dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgICAgIHJldHVybiBfbHAuX2dpdF93aW5kb3dzKCoqa3cpLCBlLmdl',
'dHZhbHVlKCkKICAgIHByaW50KGYiVFUgS0lFTSBQUk9CRSB0cmVuIHtfZ30gIChuZW4ge3N5cy5wbGF0Zm9ybX0pIikKICAg',
'IGZvciBfdGVuLCBfZiBpbiBQUk9CRToKICAgICAgICBfdHQsIF9jdCwgX2RsID0gX2YoX2dvaSwgX3NpZywgX2cvIm9wcyIv',
'ImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcHJpbnQoZiIgIFt7X3R0OjE0fV0ge190ZW59IiArIChmIiAgIHtf',
'Y3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICAgICAgZm9yIF9rLCBfdiBpbiAoX2RsIG9yIHt9KS5pdGVtcygpOiBwcmludChm',
'IiAgICAgICAge19rOjM0fToge192fSIpCiAgICBzeXMuZXhpdCgwKQoKIyAtLS0gY2hlIGRvIEtJRU0gRE9ORyBCTzogdGVw',
'IC5weSBuYXkgcGhhaSBUUlVORyBUVU5HIEJZVEUgdm9pIGJhbiBuaHVuZyB0cm9uZyBwczEgLS0tCiMgS2hvbmcgY29uZyBu',
'YW8gYnVvYyBoYWkgYmFuIHNhbyBraG9wOiBkbyBkdW9jLCBub2kgdHJhbiAyLzQwMCAtPiA5OS85OTk5OSBDSEkgdHJvbmcg',
'LnB5CiMgdGhpIGNpX2Rhbmdfa3kgbGFuIHQyNi90MjcgdmFuIHhhbmgsIGNvbiBjaG90IFNIQSBjdWEgcHMxIGNoaSBzbyBi',
'YW4gbmh1bmcgdm9pIGhhbmcgc28KIyBjdWEgQ0hJTkggbm8uIENoYXk6IHB5dGhvbiB3cDU0MS1kby1nMi13aW5kb3dzLnB5',
'IC0ta2llbS1kb25nLWJvIHdwNTQxLWRvLWcyLnBzMSAgKHJjIDB8MykKaWYgIi0ta2llbS1kb25nLWJvIiBpbiBzeXMuYXJn',
'djoKICAgIGltcG9ydCBiYXNlNjQKICAgIF9wcyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0ta2llbS1kb25n',
'LWJvIikgKyAxXSkucmVhZF90ZXh0KGVuY29kaW5nPSJhc2NpaSIpCiAgICBfbSA9IHJlLnNlYXJjaChyIig/bXMpXlwkQjY0',
'ID0gQFwoKC4qPyleXCkiLCBfcHMpCiAgICBfayA9IHJlLnNlYXJjaChyIig/bSleXCRTaGFCb0RvXHMqPVxzKicoWzAtOWEt',
'Zl17NjR9KSciLCBfcHMpCiAgICBfbmh1bmcgPSBiYXNlNjQuYjY0ZGVjb2RlKCIiLmpvaW4ocmUuZmluZGFsbChyIicoW0Et',
'WmEtejAtOSsvPV0qKSciLCBfbS5ncm91cCgxKSkpKSBpZiBfbSBlbHNlIGIiIgogICAgX3RvaSA9IFBhdGgoX19maWxlX18p',
'LnJlYWRfYnl0ZXMoKQogICAgX29rID0gYm9vbChfbSBhbmQgX2spIGFuZCBfbmh1bmcgPT0gX3RvaSBhbmQgaGFzaGxpYi5z',
'aGEyNTYoX3RvaSkuaGV4ZGlnZXN0KCkgPT0gX2suZ3JvdXAoMSkKICAgIGlubihmIktJRU0gRE9ORyBCTzoge0RBVCBpZiBf',
'b2sgZWxzZSBLRER9ICAobmh1bmcge2xlbihfbmh1bmcpfSBieXRlLCB0ZXAge2xlbihfdG9pKX0gYnl0ZSkiKQogICAgc3lz',
'LmV4aXQoMCBpZiBfb2sgZWxzZSAzKQoKaW5uKCI9IiAqIDc4KTsgaW5uKCJXUDU0MSBnMiAtIHBoZXAgZG8gdHJlbiBXaW5k',
'b3dzIHRoYXQgKHNwZWMgcjM6IE4xLU40LCBOOC1OMTIsIE43LCBraWNoIHRodW9jKSIpOyBpbm4oIj0iICogNzgpCgojIC0t',
'LS0tLS0tLS0tLS0tLS0gdHUga2llbSBibyBkb2MgLS0tLS0tLS0tLS0tLS0tLQpfZCwgX2csIF90ID0gZG9jX2RvKF9NQVUp',
'Cl9vayA9IChsZW4oX2QpID09IDIgYW5kIGFueSh4LnN0YXJ0c3dpdGgoInQwMmIiKSBmb3IgeCBpbiBfZCkKICAgICAgIGFu',
'ZCBub3QgYW55KHguc3RhcnRzd2l0aCgidDEzMSIpIGZvciB4IGluIF9kKSBhbmQgX3QpCmlubigiVHUga2llbSBibyBkb2Mg',
'bG9nOiIsIERBVCBpZiBfb2sgZWxzZSBUUlVPVCkKaWYgbm90IF9vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVP',
'QzogYm8gZG9jIGxvZyBjdWEgY2hpbmggc2NyaXB0IG5heSBzYWkgLT4ga2hvbmcgZG8gZ2kgY2EuIik7IHN5cy5leGl0KDMp',
'CgojIC0tLS0tLS0tLS0tLS0tLS0gMC4gbmVuIGRvIC0tLS0tLS0tLS0tLS0tLS0KZ29jID0gUGF0aChzeXMuYXJndlsxXSku',
'cmVzb2x2ZSgpIGlmIGxlbihzeXMuYXJndikgPiAxIGVsc2UgUGF0aC5jd2QoKQp0ZXAsIHRlcHQgPSBnb2MgLyAib3BzIiAv',
'ICJsZWFzZV9wdWJsaXNoLnB5IiwgZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaF90ZXN0LnB5Igppbm4oIiIpOyBpbm4o',
'Ii0iICogNzgpOyBpbm4oIjAuIE5FTiBETyIpCiMgTU9JIExPRyBQSEFJIFRVIEtIQUkgbm8gZG8gQ0FJIEdJIGJhbmcgQk8g',
'RE8gTkFPLiBCYWkgaG9jIDE5LTA5LTIwMjY6IG1vdCBsdW90IGRvCiMgZ3VpIHZlIGR1b2MgZG9jIG5odSBrZXQgcXVhIGN1',
'YSBiYW4gdmEgZGFuZyB4ZXQsIG5odW5nIHRoYXQgcmEgbGEgYmFuIGRvIENVIGNoYXkKIyB0cmVuIG5oYW5oIEtIQUMuIERv',
'YyByYSB0aGkgbWF0IG1vdCB2b25nOyBsb2cgdHUga2hhaSB0aGkgdGhheSBuZ2F5IGRvbmcgZGF1Lgp0cnk6CiAgICBfdHUg',
'PSBoYXNobGliLnNoYTI1NihQYXRoKF9fZmlsZV9fKS5yZWFkX2J5dGVzKCkpLmhleGRpZ2VzdCgpCmV4Y2VwdCBFeGNlcHRp',
'b24gYXMgX2U6CiAgICBfdHUgPSBmImtob25nIHR1IGJhbSBkdW9jOiB7X2V9IgpnaGkoImJvX2RvX3NoYTI1NiIsIF90dSkK',
'aW5uKGYiICBCTyBETyAgICAgICAgOiBzaGEyNTYge190dVs6MTZdfSAgKGJhbiB7QkFOX0JPX0RPfSkiKQppbm4oIiAgc3lz',
'LnBsYXRmb3JtIDoiLCBzeXMucGxhdGZvcm0sICJ8IHB5dGhvbiIsIHN5cy52ZXJzaW9uLnNwbGl0KClbMF0pCmlubigiICBv',
'cy5wYXRoc2VwICAgOiIsIHJlcHIob3MucGF0aHNlcCksICJ8IFBBVEhFWFQ6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUEFU',
'SEVYVCIpKVs6NjBdKQppbm4oIiAgUHJvZ3JhbUZpbGVzIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQcm9ncmFtRmlsZXMi',
'KSksICJ8IFN5c3RlbVJvb3Q6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiU3lzdGVtUm9vdCIpKSkKaW5uKCIgIENPTkdfQ1Vf',
'R0lUICA6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiQ09OR19DVV9HSVQiKSkpCmlubigiICBnb2Mga2hvICAgICAgOiIsIGdv',
'YykKCnF1eWVuID0gTm9uZQppZiBzeXMucGxhdGZvcm0gPT0gIndpbjMyIjoKICAgIHRyeToKICAgICAgICBpbXBvcnQgY3R5',
'cGVzOyBxdXllbiA9IGJvb2woY3R5cGVzLndpbmRsbC5zaGVsbDMyLklzVXNlckFuQWRtaW4oKSkKICAgIGV4Y2VwdCBFeGNl',
'cHRpb246IHF1eWVuID0gTm9uZQpnaGkoInF1eWVuX2FkbWluIiwgcXV5ZW4pCnN5bWxpbmtfZHVvYyA9IE5vbmUKdHJ5Ogog',
'ICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJhLnR4dCI7',
'IGQud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgdHJ5OiBvcy5zeW1saW5rKHN0cihkKSwgc3Ry',
'KFBhdGgodCkvImxrIikpOyBzeW1saW5rX2R1b2MgPSBUcnVlCiAgICAgICAgZXhjZXB0IE9TRXJyb3IgYXMgZTogc3ltbGlu',
'a19kdW9jID0gRmFsc2U7IGdoaSgic3ltbGlua19sb2kiLCBmInt0eXBlKGUpLl9fbmFtZV9ffToge2V9IikKZXhjZXB0IEV4',
'Y2VwdGlvbiBhcyBlOiBnaGkoInN5bWxpbmtfbG9pIiwgc3RyKGUpKQpnaGkoInN5bWxpbmtfZHVvYyIsIHN5bWxpbmtfZHVv',
'YykKaW5uKCIgIEFkbWluaXN0cmF0b3I6IiwgcXV5ZW4sICJ8IHRhbyBzeW1saW5rIGR1b2M6Iiwgc3ltbGlua19kdW9jKQoK',
'bG9pID0gW10KIyBDb25nIGtpY2ggdGh1b2MgbGEgcGhlcCBkbyB0cmVuIExJQ0ggU1UgR0lULCBraG9uZyBkaW5oIGdpIGRl',
'biBuZW4uIENobyBwaGVwCiMgLS1jaGkta2ljaC10aHVvYyBjaGF5IG8gbW9pIG5lbiBkZSBjb24gVFUgS0lFTSBkdW9jIGNo',
'aW5oIGNvbmcgbmF5IChkYSBkdW5nCiMgZGUgdGFpIGR1bmcgY2EgaGFpIHZlIGN1YSBzdSBjbyBuZW4tY3UgMTktMDkpLiBN',
'b2kgY2hvdCBDSFVDIE5BTkcgdmFuIGRvaSBXaW5kb3dzLgppZiBzeXMucGxhdGZvcm0gIT0gIndpbjMyIiBhbmQgIi0tY2hp',
'LWtpY2gtdGh1b2MiIG5vdCBpbiBzeXMuYXJndjoKICAgIGxvaS5hcHBlbmQoZiJLSE9ORyBwaGFpIFdpbmRvd3MgKHN5cy5w',
'bGF0Zm9ybT17c3lzLnBsYXRmb3JtIXJ9KSIpCmlmIG5vdCB0ZXAuaXNfZmlsZSgpOiAgbG9pLmFwcGVuZChmImtob25nIHRo',
'YXkge3RlcH0iKQppZiBub3QgdGVwdC5pc19maWxlKCk6IGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB0fSIpCmlmIG5v',
'dCBzaHV0aWwud2hpY2goImdpdCIpOiBsb2kuYXBwZW5kKCJraG9uZyBjbyBgZ2l0YCB0cm9uZyBQQVRIIikKCnJjLCBoZWFk',
'LCBfID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxvaS5hcHBlbmQoImtob25nIGRvYyBkdW9jIEhF',
'QUQiKQpnaGkoImhlYWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAiLS1pcy1hbmNlc3Rv',
'ciIsIFNIQV9HMSwgaGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNfYSA9PSAwKQppZiBoZWFkID09IFNIQV9HMToK',
'ICAgIHRoZV9oZSA9ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gREFZIExBIGcxLiBDSFVBIGNvIGJhbiB2',
'YSBnMjsga2V0IHF1YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9kdWU6CiAgICB0aGVfaGUgPSAiZzIiOyBpbm4o',
'ZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hBX0cxWzo4XX0pOiB1bmcgdmllbiBnMi4iKQpl',
'bHNlOgogICAgdGhlX2hlID0gIj8iOyBsb2kuYXBwZW5kKGYiSEVBRD17aGVhZFs6OF19IEtIT05HIHBoYWkgZzEgdmEgS0hP',
'TkcgcGhhaSBoYXUgZHVlIGN1YSB7U0hBX0cxWzo4XX0g4oCUIHJlYmFzZT8gbmhhbSBuaGFuaD8iKQpnaGkoInRoZV9oZSIs',
'IHRoZV9oZSkKcmNfciwgcmVmcywgXyA9IGdpdChnb2MsICJmb3ItZWFjaC1yZWYiLCAiLS1wb2ludHMtYXQiLCBoZWFkIG9y',
'ICJIRUFEIiwKICAgICAgICAgICAgICAgICAgICAiLS1mb3JtYXQ9JShyZWZuYW1lOnNob3J0KSIpCmRzciA9IFt4IGZvciB4',
'IGluIHJlZnMuc3BsaXRsaW5lcygpIGlmIHguc3RyaXAoKSBhbmQgeC5zdHJpcCgpICE9ICJkby10YW0iXQpnaGkoInJlZl90',
'cm9fdG9pX2hlYWQiLCBkc3IpCmlubihmIiAgcmVmIHRybyB0b2kgSEVBRDogeycsICcuam9pbihkc3IpIGlmIGRzciBlbHNl',
'ICcoa2hvbmcgcmVmIG5hbyAtIEhFQUQgcm9pIHR1IGRvKSd9IikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigiS0hPTkcg',
'RE8gRFVPQzogbmVuIGRvIHNhaSwgS0hPTkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlubigiICAt',
'IiwgeCkKICAgIHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMS4ga2ljaCB0aHVvYyAoTjcnIGN1YSBzcGVjIHIz',
'KSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMS4gS0lDSCBUSFVPQyDigJQgdHJhbiBz',
'cGVjIHIzOiA8PSAyIHRlcCB2YSA8PSA0MDAgZG9uZyB0aGVtIikKIyBWRSBORU4gUEhBSSBUVU9JIOKAlCB2YSBwaGFpIENI',
'VU5HIE1JTkggZHVvYyBsYSB0dW9pLCBraG9uZyBwaGFpIGdpYSBkaW5oLgojIEJhaSBob2MgdHJhIGdpYSAxOS0wOS0yMDI2',
'OiBjbG9uZSB0YWkgZHVuZyBjaGkgZmV0Y2ggbmhhbmggYmFuIHZhLCBgb3JpZ2luL21hc3RlcmAKIyBkdW5nIHllbiB0dSAx',
'NC0wOSAoYzE2YmQzMiwgc2F1IDk3IGNvbW1pdCkuIG1lcmdlLWJhc2Ugcm9pIHZlIGR1bmcgZGluaCBtYXN0ZXIgY3UsCiMg',
'bmVuIGRpZmYgTlVPVCBjYSA5NyBjb21taXQgbWFzdGVyOiBkbyByYSA0NiB0ZXAgLyArNzExOCB0aGF5IHZpIDIgdGVwIC8g',
'KzM5NyDigJQKIyBDVU5HIE1PVCBDT01NSVQgMGVhOTVkZS4gTW90IHRpZXUgY2hpIERFTFRBIG1hIHZlIG5lbiBraG9uZyB0',
'dW9pIHRoaSBraG9uZyBzYWkKIyBsZWNoIG1vdCBjaHV0LCBubyBzYWkgY2EgbW90IGJhYyBkbyBsb24uCiMgQ2hvIG5lbjog',
'bmVuIGtob25nIGNodW5nIG1pbmggZHVvYyBsYSB0dW9pID0+IEtIT05HIERPIERVT0MgKHJjPTMpLCBLSE9ORyBwaGFpIFRS',
'VU9ULgojIFRSVU9UIGxhIG1vdCBQSEFOIFFVWUVUIHZlIGJhbiB2YTsgcGhhbiBxdXlldCBjaGkgZHVvYyBwaGVwIHBoYXQg',
'cmEga2hpIGRhIGRvIGR1b2MuCnJjX3UsIHVybF9vLCBfID0gZ2l0KGdvYywgInJlbW90ZSIsICJnZXQtdXJsIiwgIm9yaWdp',
'biIpCnVybF9vID0gX3VybF9zYWNoKHVybF9vKQpnaGkoIm9yaWdpbl91cmwiLCB1cmxfbyk7IGlubihmIiAgb3JpZ2luICAg',
'ICAgIDoge3VybF9vIG9yICcoa2hvbmcgZG9jIGR1b2MpJ30iKQp1cmxfb2sgPSAobm90IHJjX3UpIGFuZCB1cmxfby5yc3Ry',
'aXAoIi8iKSBpbiBVUkxfS0hPX0hPUF9MRQpyY19sciwgb3V0X2xyLCBlcl9sciA9IGdpdChnb2MsICJscy1yZW1vdGUiLCAi',
'b3JpZ2luIiwgInJlZnMvaGVhZHMvbWFzdGVyIikgaWYgdXJsX29rIGVsc2UgKDEsICIiLCAiIikKZXJfbHIgPSBfYW5fdXNl',
'cmluZm8oZXJfbHIpCnJjX2xtLCBsbSwgZXJfbG0gICAgID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJvcmlnaW4vbWFzdGVy',
'IikKcm0gPSBvdXRfbHIuc3BsaXQoKVswXSBpZiAobm90IHJjX2xyIGFuZCBvdXRfbHIuc3RyaXAoKSkgZWxzZSAiIgppZiBu',
'b3QgdXJsX29rOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJvcmlnaW49e3VybF9vIXJ9IEtIT05HIHBoYWkg',
'a2hvIHRoYXQg4oCUICd0dW9pJyBzbyB2b2kgbm8ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGdpIikKICAgIHJjX21iLCBtYiwg',
'bnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbm90IHJtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwKICAgICAg',
'ICBmImtob25nIGhvaSBkdW9jIG1hc3RlciB0cmVuIHJlbW90ZSAobHMtcmVtb3RlIHJjPXtyY19scn0pOiB7ZXJfbHJbOjYw',
'XX0gIgogICAgICAgIGYi4oCUIGtob25nIGNodW5nIG1pbmggZHVvYyB2ZSBuZW4gY29uIHR1b2kiKQogICAgcmNfbWIsIG1i',
'LCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiByY19sbSBvciBub3QgbG06CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwg',
'S0RELCBmImtob25nIGRvYyBkdW9jIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmU6IHtlcl9sbVs6NjBdfSIpCiAgICByY19t',
'YiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIGxtICE9IHJtOgogICAgIyBEZW0geGVtIHR1dCBsYWkgYmFvIHhh',
'LCBuZXUgZGVtIGR1b2Mg4oCUIGNvbiBzbyBuYXkgbm9pIHJvIG11YyBkbyBzYWkgbGVjaC4KICAgIHJjX2MsIHNhdSwgXyA9',
'IGdpdChnb2MsICJyZXYtbGlzdCIsICItLWNvdW50IiwgZiJ7bG19Li57cm19IikKICAgIHhhID0gZiIsIHR1dCBsYWkge3Nh',
'dX0gY29tbWl0IiBpZiAobm90IHJjX2MgYW5kIHNhdS5zdHJpcCgpLmlzZGlnaXQoKSkgZWxzZSAiIgogICAgaW5uKGYiICBv',
'cmlnaW4vbWFzdGVyIHRyb25nIGNsb25lIDoge2xtWzoxMl19IikKICAgIGlubihmIiAgbWFzdGVyIHRyZW4gcmVtb3RlICAg',
'ICAgICA6IHtybVs6MTJdfXt4YX0iKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90ZSIs',
'IHJtKQogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwKICAgICAgICBmInZlIG5lbiBDVTogb3JpZ2luL21hc3Rlcj17',
'bG1bOjEyXX0gIT0gcmVtb3RlPXtybVs6MTJdfXt4YX0gIgogICAgICAgIGYi4oCUIGNoYXkgYGdpdCAtQyA8a2hvPiBmZXRj',
'aCBvcmlnaW4gbWFzdGVyYCByb2kgZG8gbGFpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsc2U6',
'CiAgICBpbm4oZiIgIHZlIG5lbiBUVU9JOiBvcmlnaW4vbWFzdGVyID0ge2xtWzoxMl19ID09IG1hc3RlciB0cmVuIHJlbW90',
'ZSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICByY19tYiwgbWIs',
'IGVyX21iID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAib3JpZ2luL21hc3RlciIsIGhlYWQpCmlmIHJjX21iIG9yIG5vdCBt',
'YjoKICAgIGlmIG1iID09ICIiIGFuZCBybSBhbmQgbG0gPT0gcm06CiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtE',
'RCwgZiJraG9uZyB0aW5oIGR1b2MgbWVyZ2UtYmFzZSB2b2kgb3JpZ2luL21hc3Rlcjoge2VyX21iWzo3MF19IikKICAgIG5z',
'LCByYyA9ICIiLCAxCmVsc2U6CiAgICBnaGkoIm1lcmdlX2Jhc2UiLCBtYikKICAgIGlubihmIiAgbWVyZ2UtYmFzZShvcmln',
'aW4vbWFzdGVyLCBIRUFEKSA9IHttYls6MTJdfSIpCiAgICBpZiBtYiAhPSBTSEFfQkFTRV9TUEVDOgogICAgICAgIGlubihm',
'IiAgTFVVIFk6IGtoYWMgYmFzZSBtYSBzcGVjIHIzIGtoYWkgKHtTSEFfQkFTRV9TUEVDWzoxMl19KSDigJQgdmkgbmhhbmgg',
'ZGEgbWVyZ2UgbWFzdGVyLiIpCiAgICAgICAgaW5uKCIgICAgICAgICBEbyBzbyBiYXNlIGN1IHNlIE5VT1QgcGhhbiBtYXN0',
'ZXIgbWFuZyB2YW8uIER1bmcgbWVyZ2UtYmFzZSBtb2kgbGEgdmllYyBjdWEgZXhlY3V0b3IuIikKICAgICAgICByY194LCBu',
'c194LCBfID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgU0hBX0JBU0VfU1BFQywgaGVhZCkKICAgICAgICBpZiBu',
'b3QgcmNfeDoKICAgICAgICAgICAgaCA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zX3guc3BsaXRsaW5lcygpIGlmIGwu',
'c3RyaXAoKV0KICAgICAgICAgICAgYSA9IHN1bShpbnQoeFswXSkgZm9yIHggaW4gaCBpZiB4WzBdLmlzZGlnaXQoKSkKICAg',
'ICAgICAgICAgZ2hpKCJudW1zdGF0X3RoZW9fYmFzZV9zcGVjIiwgeyJ0ZXAiOiBsZW4oaCksICJ0aGVtIjogYX0pCiAgICAg',
'ICAgICAgIGlubihmIiAgICAgICAgIChkb2kgY2hpZXU6IHNvIGJhc2Ugc3BlYyA9IHtsZW4oaCl9IHRlcCAvICt7YX0g4oCU',
'IGNvbiBzbyBheSBLSE9ORyBkdW5nIGRlIGNoYW0pIikKICAgIHJjLCBucywgZXIgPSBnaXQoZ29jLCAiZGlmZiIsICItLW51',
'bXN0YXQiLCBtYiwgaGVhZCkKaWYgcmM6CiAgICBwYXNzCmVsc2U6CiAgICBoYW5nID0gW2wuc3BsaXQoIlx0IikgZm9yIGwg',
'aW4gbnMuc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgIHRoZW0gPSBzdW0oaW50KGhbMF0pIGZvciBoIGluIGhhbmcg',
'aWYgaFswXS5pc2RpZ2l0KCkpCiAgICB4b2EgID0gc3VtKGludChoWzFdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMV0uaXNkaWdp',
'dCgpKQogICAgZ2hpKCJzb190ZXAiLCBsZW4oaGFuZykpOyBnaGkoImRvbmdfdGhlbSIsIHRoZW0pOyBnaGkoImRvbmdfeG9h',
'IiwgeG9hKQogICAgZm9yIGggaW4gaGFuZzogaW5uKGYiICAgIHtoWzJdOjM0fSAre2hbMF06PDV9IC17aFsxXX0iKQogICAg',
'aW5uKGYiICAgIFRPTkc6IHtsZW4oaGFuZyl9IHRlcCwgK3t0aGVtfSwgLXt4b2F9ICAgKHRyYW46IHtUUkFOX1RFUH0gdGVw',
'IC8ge1RSQU5fRE9OR30gZG9uZyB0aGVtKSIpCiAgICBjaGFtID0gc29ydGVkKHtoWzJdIGZvciBoIGluIGhhbmd9ICYgV1JJ',
'VEVfU0VUX0cyKTsgZ2hpKCJjaGFtX3dyaXRlX3NldCIsIGNoYW0pCiAgICBkZWYgX2NhX21vaV9jbyhyZXYpOgogICAgICAg',
'IHJfLCBuZF8sIF8gPSBnaXQoZ29jLCAic2hvdyIsIGYie3Jldn06b3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAg',
'ICAgcmV0dXJuIE5vbmUgaWYgcl8gZWxzZSB7dCBmb3IgdCBpbiBDQV9NT0lfRzIgaWYgcmUuc2VhcmNoKHIiKD9tKV5kZWYg',
'IiArIHQgKyByIlthLXpdP18iLCBuZF8pfQogICAgb19tYiwgb19oID0gX2NhX21vaV9jbyhtYiksIF9jYV9tb2lfY28oaGVh',
'ZCkKICAgIG1hbmcgPSBzb3J0ZWQob19oIC0gb19tYiwga2V5PXNvX2NhKSBpZiAob19tYiBpcyBub3QgTm9uZSBhbmQgb19o',
'IGlzIG5vdCBOb25lKSBlbHNlIE5vbmUKICAgIGdoaSgiY2FfbW9pX2cyX21hbmdfdmFvIiwgbWFuZykKICAgIGlmIG5vdCBt',
'YW5nOgogICAgICAgICMgRG8gUk9ORyAoZGEgbGFuZCwgY2hpbmggbWFzdGVyKSwgbmhhbSBuaGFuaCwgaGF5IG5oYW5oIGN1',
'YSBwYWNrZXQgS0hBQyBjaGFtIGN1bmcgdGVwOgogICAgICAgICMga2hvbmcgbWFuZyBjYSBtb2kgbmFvIGN1YSBnMiB0aGkg',
'a2hvbmcgcGhhaSB1bmcgdmllbi4gRG9jIGtob25nIGR1b2MgKE5vbmUpIGN1bmcgdmF5LgogICAgICAgIGtldCgiTjcnIGtp',
'Y2ggdGh1b2MiLCBLREQsIGYiZG9pIHR1b25nIGtob25nIHBoYWkgdW5nIHZpZW46IHtsZW4oaGFuZyl9IHRlcCwgY2hhbSB7',
'Y2hhbX0sIGNhIG1vaSAiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJnMiBtYW5nIHZhbyB7bWFuZyFy',
'fSDigJQgZGEgbGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/IikKICAgIGVsc2U6CiAgICAgICAga2V0KCJONycga2lj',
'aCB0aHVvYyIsIERBVCBpZiAobGVuKGhhbmcpIDw9IFRSQU5fVEVQIGFuZCB0aGVtIDw9IFRSQU5fRE9ORykgZWxzZSBUUlVP',
'VCwKICAgICAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IikKCiMgRGluaCBkYW5oIFRIQVQgbmFtIG8gTjcn',
'IChjYSBtb2kgZzIgbWFuZyB2YW8pLCBLSE9ORyBvICJoYXUgZHVlIGcxIjogZzEgZGEgbGFuZCBuZW4gbW9pIG5oYW5oIGRl',
'dQojIGxhIGhhdSBkdWUuIERvbmcgZGF1IGtob2kgZGFuIHBoYWkgdHUga2hhaSB0aGVvIGtldCBxdWEgYXkgKGRvIGR1b2M6',
'IG1hc3RlciA0NDYyMGU4IG1vIGtob2kgYmFuZwojICJUSEUgSEUgRE8gRFVPQzogZzIiLCBKU09OICJ0aGVfaGUiOiAiZzIi',
'LCB0cm9uZyBraGkgTjcnIGRhIGtldCBsdWFuICJraG9uZyBwaGFpIHVuZyB2aWVuIikuCmlmIHRoZV9oZSA9PSAiZzIiIGFu',
'ZCBub3Qgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKToKICAgIHRoZV9oZSA9ICgiS0hPTkcgcGhhaSB1bmcgdmllbiBn',
'MiIgaWYgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKSA9PSBbXQogICAgICAgICAgICAgIGVsc2UgImcyPyAoQ0hVQSBk',
'aW5oIGRhbmggZHVvYyBkb2kgdHVvbmcpIikKICAgIGdoaSgidGhlX2hlIiwgdGhlX2hlKQoKIyBDb25nIG5oYW5oOiBkbyBS',
'SUVORyBraWNoIHRodW9jICh2YWkgZ2lheSkgcm9pIGR1bmcuIER1bmcga2hpIGNhbiB4YWMgbWluaCBsYWkKIyB2ZSBuZW4g',
'bWEga2hvbmcgbXVvbiB0cmEgMjAtNDUgcGh1dCBjaG8gY2EgYm8gdGVzdC4KaWYgIi0tY2hpLWtpY2gtdGh1b2MiIGluIHN5',
'cy5hcmd2OgogICAgaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQogICAgaW5uKCItLWNoaS1raWNoLXRodW9jOiBDSEkgZG8gY29u',
'ZyBraWNoIHRodW9jLiBEYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCiAgICBpbm4oIi0iICogNzgpCiAg',
'ICBmb3IgX3QsIF90dCwgX2N0IGluIGNob3Q6IGlubihmIiAge190dDoxNH0ge190fSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0',
'IGVsc2UgIiIpKQogICAgX2sgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQogICAgX3IgPSBzdW0o',
'MSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCiAgICBzeXMuZXhpdCgzIGlmIF9rIGVsc2UgKDEgaWYgX3Ig',
'ZWxzZSAwKSkKCkNISV9QUk9CRSA9ICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YgICAgIyBibyBxdWEgYm8gdGVzdCArIE43',
'OyBnaXUgMCwgMSwgMwojIC0tLS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVzdCBkYXkgZHUgLS0tLS0tLS0tLS0tLS0tLQppZiBu',
'b3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIyLiBCTyBURVNUIERBWSBEVSAoMTAtNDAg',
'cGh1dCkiKQogICAgcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBnb2MpCiAgICBn',
'aGkoInJjX3N1aXRlIiwgcmNfbikKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXRfbikKICAgIGlubigiICByYyA9IiwgcmNf',
'biwgInwiLCBtLmdyb3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQpIikKICAgIGlmIG06',
'CiAgICAgICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGkoInRyZW4iLCBpbnQobS5ncm91cCgyKSkpOyBnaGko',
'ImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKICAgIGRvX2hldCwgZ2MsIHRpbiA9IGRvY19kbyhvdXRfbikKICAgIGdo',
'aSgic29fY2FfZG8iLCBsZW4oZG9faGV0KSk7IGdoaSgibGlldF9rZV9kYXlfZHUiLCB0aW4pCiAgICBmb3IgZyBpbiBnYzog',
'aW5uKCIgICAqIiwgZykKICAgIGlubigiIik7IGlubihmIiAgPT09IHtsZW4oZG9faGV0KX0gQ0EgRE8gPT09IikKICAgIGZv',
'ciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaW5uKGYiICAge3Quc3BsaXQoJ18nKVswXTo3fSB7',
'dH0iKTsgaW5uKGYiICAgICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCiAgICBnaGkoImRvX2x5X2RvIiwge3Q6IGRvX2hl',
'dFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQogICAgIyAtLS0tIENIT1Q6IG1vaSBjYSBETyBwaGFpIEdJQUkgVEhJQ0gg',
'RFVPQyAtLS0tCiAgICAjIFRoaWV1IGNob3QgbmF5LCBibyBkbyBpbiBkYW5oIHNhY2ggZG8gcm9pIHZhbiB0aG9hdCByYz0w',
'LiBEbyBkdW5nIGxhIGxvaSBkYSB4YXkgcmE6CiAgICAjIGx1b3QgV2luZG93cyAxOS0wOSBjbyB0MTcxIERPIG1hIGJvIGRv',
'IGJhbyAiREFUIDEwIHwgVFJVT1QgMCIgdmEgcmM9MC4KICAgIGRlZiBfa2hvYSh0KTogcmV0dXJuIHQuc3BsaXQoIl8iKVsw',
'XQogICAgZG9fcGFja2V0LCBkb19sYSwgZG9fdGhpZXVfY29uZ19jdSA9IFtdLCBbXSwgW10KICAgIGZvciB0IGluIHNvcnRl',
'ZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaywgbHkgPSBfa2hvYSh0KSwgZG9faGV0W3RdCiAgICAgICAgaWYgayBp',
'biBDQV9QQUNLRVQ6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fcGFja2V0LmFwcGVuZCh0KQogICAgICAgIGVs',
'aWYgIktIw5RORyDEkE8gxJDGr+G7okMiIGluIGx5IG9yICJ0aGnhur91IGAiIGluIGx5OiAgZG9fdGhpZXVfY29uZ19jdS5h',
'cHBlbmQodCkKICAgICAgICBlbGlmIGsgaW4gTkdPQUlfUEhBTV9WSTogICAgICAgICAgICAgICAgICAgICAgICBwYXNzCiAg',
'ICAgICAgZWxzZTogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fbGEuYXBwZW5kKHQpCiAg',
'ICBnaGkoImRvX3BhY2tldCIsIGRvX3BhY2tldCk7IGdoaSgiZG9fbGEiLCBkb19sYSk7IGdoaSgiZG9fdGhpZXVfY29uZ19j',
'dSIsIGRvX3RoaWV1X2NvbmdfY3UpCiAgICBpbm4oIiIpCiAgICBpbm4oZiIgIGNhIERPIHRodW9jIENISU5IIHBhY2tldCBu',
'YXkgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF0gb3IgJ2tob25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBu',
'Z29haSBwaGFtIHZpIChyMyBraGFpKToge1tfa2hvYSh4KSBmb3IgeCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpIGlm',
'IF9raG9hKHgpIGluIE5HT0FJX1BIQU1fVkldfSIpCiAgICBpbm4oZiIgIGNhIERPIHZpIFRISUVVIENPTkcgQ1UgICAgICAg',
'OiB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9yICdraG9uZyBjbyd9IikKICAgIGlubihmIiAgY2Eg',
'RE8gTEEgKGtob25nIGdpYWkgdGhpY2ggZHVvYyk6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdIG9yICdraG9uZyBjbyd9',
'IikKICAgICMgLS0tLSBDSE9UOiBwaGVwIGRvIHBoYWkgVFJPTiB0cnVvYyBraGkgbW90IGNodSBEQVQgbmFvIGR1b2MgcGhh',
'dCAtLS0tCiAgICAjIEJhbiB0cnVvYyBjaGkgSU4gYHRpbmAvYHJjX3N1aXRlYDogYm8gdGVzdCBjaGV0IGdpdWEgdDE3MSAo',
'cmM9MTM0LCBraG9uZyBkb25nIHRvbmcpCiAgICAjIHZhbiByYSAiREFUIDEyIHwgVFJVT1QgMCIgcmM9MDsgY2EgUEFDS0VU',
'IHZhbmcgbWF0IGhheSBiaSBCTyBRVUEgY3VuZyBkdW9jIGNoYW0gbmh1CiAgICAjICJraG9uZyBkbyIuIFZhbmcgbWF0IGto',
'b25nIHBoYWkgImtob25nIGRvIiDigJQgbGEgS0hPTkcgRE8gRFVPQy4KICAgIHZhbmcgPSBbdCBmb3IgdCBpbiBzb3J0ZWQo',
'Q0FfUEFDS0VULCBrZXk9c29fY2EpIGlmIG1hdV9jYShvdXRfbiwgdCkgbm90IGluICgiUVVBIiwgIkRPIildCiAgICBseV9r',
'ZGQgPSBbXQogICAgaWYgbm90IHRpbjogbHlfa2RkLmFwcGVuZCgiZGFuaCBzYWNoIGRvIEtIT05HIGRheSBkdSIpCiAgICBp',
'ZiByY19uIG5vdCBpbiAoMCwgMSkgb3IgKHJjX24gPT0gMSkgIT0gYm9vbChkb19oZXQpOgogICAgICAgIGx5X2tkZC5hcHBl',
'bmQoZiJyYyBibyB0ZXN0PXtyY19ufSBraG9uZyBraG9wIHtsZW4oZG9faGV0KX0gY2EgRE8gZG9jIGR1b2MiKQogICAgaWYg',
'dmFuZzogbHlfa2RkLmFwcGVuZChmImNhIFBBQ0tFVCB2YW5nL2JvIHF1YToge3Zhbmd9IikKICAgIGdoaSgiY2FfcGFja2V0',
'X3ZhbmciLCB2YW5nKTsgZ2hpKCJseV9kb19jaHVhX3Ryb24iLCBseV9rZGQpCiAgICBpZiBseV9rZGQ6IGtldCgiQm8gdGVz',
'dCBjaGF5IFRST04gdmEgZG9jIERVIiwgS0RELCAiOyAiLmpvaW4obHlfa2RkKSkKICAgIGNodWFfdHJvbiA9IEtERCBpZiBs',
'eV9rZGQgZWxzZSBEQVQKICAgIGtldCgiS2hvbmcgY2EgbmFvIGN1YSBQQUNLRVQgYmkgRE8iLCBjaHVhX3Ryb24gaWYgbm90',
'IGRvX3BhY2tldCBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBmIkRPOiB7W19raG9hKHgp',
'IGZvciB4IGluIGRvX3BhY2tldF19IOKAlCBiYW4gdmEgQ0hVQSB4b25nIikKICAgIGtldCgiTW9pIGNhIERPIGRldSBnaWFp',
'IHRoaWNoIGR1b2MiLCBjaHVhX3Ryb24gaWYgbm90IGRvX2xhIGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX2xh',
'IGVsc2UgZiJsYToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV19IikKICAgIGlmIGRvX3RoaWV1X2NvbmdfY3U6CiAgICAg',
'ICAga2V0KCJDb25nIGN1IGRheSBkdSBkZSBkbyIsIEtERCwgZiJ0aGlldSBjb25nIGN1IGNobyB7W19raG9hKHgpIGZvciB4',
'IGluIGRvX3RoaWV1X2NvbmdfY3VdfSIpCgogICAgYnEgPSBzb3J0ZWQoe3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRh',
'bGwob3V0X24pfSwga2V5PXNvX2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBicSkKICAgIGlubigiIik7IGlubihmIiAgQk8gUVVB',
'ICh7bGVuKGJxKX0pOiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCiAgICBpbm4oIiIpOyBpbm4oIiAgTjEt',
'TjQgKHQxNjUtdDE2OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBuYXkgbGEgY2hpIGJhbyBob2kgcXV5OiIpCiAg',
'ICBiNCA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBTU9JfTsgZ2hpKCJjYV9tb2kiLCBiNCkKICAgIGZvciB0',
'IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCiAgICAjIEJPX1FVQS92YW5nIGxhIENIVUEgQ0hBWSwga2hv',
'bmcgcGhhaSBETzogY2hpIG1vdCBjYSBETyBtb2kgZHVvYyBwaGF0IFRSVU9ULgogICAga2V0KCJOMS1ONCAodDE2NS10MTY4',
'KSIsIERBVCBpZiBhbGwodiA9PSAiUVVBIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkKICAgICAgICBlbHNlIChUUlVPVCBpZiBh',
'bnkodiA9PSAiRE8iIGZvciB2IGluIGI0LnZhbHVlcygpKSBlbHNlIEtERCksIHN0cihiNCkpCgogICAgaW5uKCIiKTsgaW5u',
'KCIgIDE1IGNhIHR1bmcgZG8gdHJlbiBDSToiKQogICAgYjE1ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0Ex',
'NX07IGdoaSgiY2ExNSIsIGIxNSkKICAgIGlubigiICAgICIgKyAiICAiLmpvaW4oZiJ7dH06e2IxNVt0XX0iIGZvciB0IGlu',
'IENBMTUpKQoKICAgICMgdDEzNiDigJQgTjEyIGRvIEdJQU4gVElFUCBxdWEga2V0IHF1YSBjYQogICAgdDEzNl90ZW4gPSBu',
'ZXh0KCh0IGZvciB0IGluIGRvX2hldCBpZiB0LnN0YXJ0c3dpdGgoInQxMzYiKSksIE5vbmUpCiAgICBpZiBiMTUuZ2V0KCJ0',
'MTM2IikgPT0gIlFVQSI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgREFULCAidDEzNiBRVUEi',
'KQogICAgZWxpZiBiMTUuZ2V0KCJ0MTM2IikgIT0gIkRPIjoKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBj',
'YSkiLCBLREQsIGYidDEzNiA9IHtiMTUuZ2V0KCd0MTM2Jykhcn0g4oCUIGtob25nIGNoYXkva2hvbmcgdGhheSIpCiAgICBl',
'bHNlOgogICAgICAgIGx5ID0gZG9faGV0LmdldCh0MTM2X3RlbiwgIiIpCiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtl',
'dCBxdWEgY2EpIiwgVFJVT1QsIGYiRE86IHtseVs6OTBdfSIpCgojIC0tLS0tLS0tLS0tLS0tLS0gMy4gcHJvYmUgVEhBTkcg',
'dmFvIGhhbSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMy4gUFJPQkUgVEhBTkcg4oCU',
'IGdvaSBfZ2l0X3dpbmRvd3Mgdm9pIHRoYW0gc28gdGllbSIpCnNwZWMgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmls',
'ZV9sb2NhdGlvbigibHA1NDEiLCBzdHIodGVwKSkKbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMp',
'OyBzcGVjLmxvYWRlci5leGVjX21vZHVsZShscCkKc2lnID0gaW5zcGVjdC5zaWduYXR1cmUobHAuX2dpdF93aW5kb3dzKQpn',
'aGkoInRoYW1fc29fX2dpdF93aW5kb3dzIiwgbGlzdChzaWcucGFyYW1ldGVycykpCmlubigiICB0aGFtIHNvIGN1YSBfZ2l0',
'X3dpbmRvd3M6IiwgbGlzdChzaWcucGFyYW1ldGVycykpCgpkZWYgZ29pKCoqa3cpOgogICAgIiIiR29pIF9naXRfd2luZG93',
'cywgQkFUIHN0ZGVyciBkZSBtb3QgZG9uZyBjaGFuIGRvYW4ga2hvbmcgZ2lldCBsdW90IGRvLiIiIgogICAgZSA9IGlvLlN0',
'cmluZ0lPKCkKICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgciA9IGxwLl9naXRfd2lu',
'ZG93cygqKmt3KQogICAgcmV0dXJuIHIsIGUuZ2V0dmFsdWUoKQoKIyAtLS0gZG9pIGNodW5nIHJpZzogcGhhaSB0cmEgbG9p',
'IGR1bmcgbW90IGNhIHRhIEJJRVQgVFJVT0MgZGFwIGFuIC0tLQp3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgp',
'IGFzIHQ6CiAgICBuZ29haSA9IFBhdGgodCkvIm5nb2FpIjsgbmdvYWkubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBj',
'dy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgKG5nb2FpLyJnaXQuZXhlIikud3JpdGVfdGV4',
'dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMSwgXyA9IGdvaShwYXRoPXN0cihuZ29haSksIHByb2dyYW1fZmlsZXM9',
'c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAoY3cvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04',
'IikKICAgIHIyLCBfID0gZ29pKHBhdGg9c3RyKGN3KSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKcmln',
'X29rID0gYm9vbChyMSkgYW5kIHIyIGlzIE5vbmUKZ2hpKCJyaWdfZG9pX2NodW5nIiwgcmlnX29rKQprZXQoIlJJRyBkb2kg',
'Y2h1bmcgKGJpZXQgdHJ1b2MgZGFwIGFuKSIsIERBVCBpZiByaWdfb2sgZWxzZSBLREQsCiAgICBmIm5nb2FpLWN3ZC0+eydO',
'SEFOJyBpZiByMSBlbHNlICdOb25lJ30gfCB0cm9uZy1jd2QtPnsnTkhBTicgaWYgcjIgZWxzZSAnTm9uZSd9IikKaWYgbm90',
'IHJpZ19vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogcmlnIHNhaSwgbW9pIGNob3QgZHVvaSBzZSB2byBu',
'Z2hpYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tIE1PSSBDT05HIFBIQUkgVFUgQ0hVTkcgTUlOSCBOTyBDTyBUSEUgRE8gLS0t',
'CiMgQmFpIGhvYyBkYXQgbmhhdCBjdWEgcGFja2V0IG5heTogZG9fbjEwIGJhbiBjdSBjaGFtIERBVCBjaG8gOTU4MzE2ODUg',
'dHJvbmcga2hpIHQxNzEKIyBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1bmcga2h1eWV0IHRhdCBtYSBOMTAgc2luaCBy',
'YSBkZSBiYXQuIE5vIGRlZ2VuZXJhdGUg4oCUCiMgdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIG5lbiAidGFj',
'aCBkdW5nIiB2YSAidGFjaCBzYWkiIGNobyBjdW5nIGtldCBxdWEuCiMgTW90IGNvbmcga2hvbmcgdGhlIERPIHRoaSBraG9u',
'ZyBwaGFpIGNvbmcsIHZhIG5vIG5ndXkgaGllbSBob24ga2hvbmcgY28gY29uZzogbm8KIyBwaGF0IHJhIG1vdCBjaHUgREFU',
'LgojCiMgTmVuIHRydW9jIGtoaSBEVU5HIG5hbSBjb25nIG5heSBkZSBwaGFuIHF1eWV0LCBiYXQgdHVuZyBjb25nIGdpZXQg',
'bW90IGRvdCBiaWVuIGRhCiMgYmlldCB0cm9uZy4gQ29uZyBuYW8ga2hvbmcgZ2lldCBkdW9jIHRoaSBjaHUgREFUIGN1YSBu',
'byBiaSBIQSB4dW9uZyBLSE9ORyBETyBEVU9DOwojIFRSVU9UIGdpdSBuZ3V5ZW4gKHF1YW4gc2F0IHRydWMgdGllcCwgdmQu',
'IGcxIHZhbiBuaGFuIGdpdC5iYXQpLiBEb3QgYmllbiBjaGF5IHRyZW4gQkFOIFNBTyBUQU07IGNheSB0aGF0IGtob25nIGJp',
'CiMgZHVuZyB0b2kgKGN1bmcga3kgbHVhdCBuaHUgTjcpLgpET1RfQklFTl9UVV9LSUVNID0gWwogICAgKCJOOCIsICJvcHMv',
'bGVhc2VfcHVibGlzaC5weSIsCiAgICAgJ2lmIGNoaV9kaW5oIGFuZCBQYXRoKGNoaV9kaW5oKS5uYW1lLmxvd2VyKCkgPT0g',
'ImdpdC5leGUiIGFuZCBob3BfbGUoY2hpX2RpbmgpOicsCiAgICAgImlmIGNoaV9kaW5oIGFuZCBob3BfbGUoY2hpX2Rpbmgp',
'OiIpLAogICAgKCJOOSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgImQgPSBkX3Jhdy5zdHJpcCgpLnN0cmlwKCdc',
'IicpIiwgImQgPSBkX3Jhdy5zdHJpcCgpIiksCiAgICAoIk4xMCIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgInNl',
'cCA9IG9zLnBhdGhzZXAgaWYgcGhhbl9jYWNoIGlzIE5vbmUgZWxzZSBwaGFuX2NhY2giLCAic2VwID0gb3MucGF0aHNlcCIp',
'LAogICAgKCJOMTEiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAiaWYgY2hhbl9kb2FuIGlzIG5vdCBOb25lOiIsICJpZiBG',
'YWxzZToiKSwKICAgICgiTjEyIiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiLAogICAgICdnaXRfcGF0aD0iLy9raG9u',
'Zy1jby9naXQiJywgJ2dpdF9wYXRoPSIva2hvbmctY28vZ2l0IicpLApdCmlubigiIik7IGlubigiICB0dSBraWVtIGNvbmcg',
'4oCUIG1vaSBjb25nIHBoYWkgZ2lldCBkdW9jIG1vdCBkb3QgYmllbiBkYSBiaWV0OiIpCmdpZXQgPSB7fQpmb3IgbWEsIGR1',
'b25nLCB0aW0sIHRoYXkgaW4gRE9UX0JJRU5fVFVfS0lFTToKICAgIF90ZW4sIF9oYW0gPSBuZXh0KCgoYSwgYikgZm9yIGEs',
'IGIgaW4gUFJPQkUgaWYgYS5zdGFydHN3aXRoKG1hICsgIiAiKSksIChOb25lLCBOb25lKSkKICAgIGlmIF9oYW0gaXMgTm9u',
'ZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzoga2hvbmcgdGltIHRo',
'YXkgcHJvYmUgdGVuICd7bWF9IC4uLiciKTsgY29udGludWUKICAgIHRyeToKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBv',
'cmFyeURpcmVjdG9yeSgpIGFzIF90OgogICAgICAgICAgICBfYyA9IFBhdGgoX3QpLyJjYXkiOyBzaHV0aWwuY29weXRyZWUo',
'Z29jLyJvcHMiLCBfYy8ib3BzIikKICAgICAgICAgICAgX2YgPSBfYy9kdW9uZzsgX25kID0gX2YucmVhZF90ZXh0KGVuY29k',
'aW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIGlmIF9uZC5jb3VudCh0aW0pICE9IDE6CiAgICAgICAgICAgICAgICBnaWV0W21h',
'XSA9IE5vbmUKICAgICAgICAgICAgICAgIGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzogbWF1IGRvdCBiaWVuIGto',
'b3Age19uZC5jb3VudCh0aW0pfSBsYW4gKG1vbmcgMSkiCiAgICAgICAgICAgICAgICAgICAgZiIg4oCUIG1hIG5ndW9uIGRh',
'IGRvaSwgZG90IGJpZW4gbmF5IGhldCB5IG5naGlhIik7IGNvbnRpbnVlCiAgICAgICAgICAgIF9mLndyaXRlX3RleHQoX25k',
'LnJlcGxhY2UodGltLCB0aGF5LCAxKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgX3NwID0gaW1wb3J0bGliLnV0',
'aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX2RiXyIgKyBtYSwgc3RyKF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5',
'IikpCiAgICAgICAgICAgIF9tID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3ApOyBfc3AubG9hZGVyLmV4',
'ZWNfbW9kdWxlKF9tKQogICAgICAgICAgICBkZWYgX2dvaV9kYigqKmt3KToKICAgICAgICAgICAgICAgIF9lID0gaW8uU3Ry',
'aW5nSU8oKQogICAgICAgICAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihfZSk6CiAgICAgICAgICAg',
'ICAgICAgICAgcmV0dXJuIF9tLl9naXRfd2luZG93cygqKmt3KSwgX2UuZ2V0dmFsdWUoKQogICAgICAgICAgICBfdHQsIF9j',
'dCwgXyA9IF9oYW0oX2dvaV9kYiwgaW5zcGVjdC5zaWduYXR1cmUoX20uX2dpdF93aW5kb3dzKSwKICAgICAgICAgICAgICAg',
'ICAgICAgICAgICAgICAgIF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIGdpZXRbbWFdID0gKF90',
'dCA9PSBUUlVPVCkKICAgICAgICBpbm4oZiIgICAge21hOjR9IGRvdCBiaWVuIC0+IHtfdHQ6MTR9IHsnR0lFVCBEVU9DJyBp',
'ZiBfdHQgPT0gVFJVT1QgZWxzZSAnU09ORyBTT1QnfSIKICAgICAgICAgICAgKyAoZiIgICAoe19jdH0pIiBpZiBfY3QgZWxz',
'ZSAiIikpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAgICAgIGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHtt',
'YTo0fSBLSE9ORyBETyBEVU9DOiB7dHlwZShfZSkuX19uYW1lX199OiB7X2V9IikKZ2hpKCJjb25nX2dpZXRfZHVvY19kb3Rf',
'YmllbiIsIGdpZXQpCgpmb3IgdGVuLCAodHQsIGN0LCBkbCkgaW4gWyh0LCBmKGdvaSwgc2lnLCB0ZXB0KSkgZm9yIHQsIGYg',
'aW4gUFJPQkVdOgogICAgZ2hpKCJwcm9iZV8iICsgdGVuLnNwbGl0KClbMF0ubG93ZXIoKSwgZGwpCiAgICBpZiBpc2luc3Rh',
'bmNlKGRsLCBkaWN0KToKICAgICAgICBmb3IgaywgdiBpbiBkbC5pdGVtcygpOiBpbm4oZiIgICAge2s6MzR9OiB7dn0iKQog',
'ICAgbWEgPSB0ZW4uc3BsaXQoKVswXQogICAgaWYgZ2lldC5nZXQobWEpIGlzIG5vdCBUcnVlIGFuZCB0dCA9PSBEQVQ6CiAg',
'ICAgICAgIyBEQVQgdHUgbW90IGNvbmcgY2h1YSBjaHVuZyBtaW5oIGR1b2MgbGEgYmlldCBETyB0aGkga2hvbmcgZGFuZyB0',
'aW4gaG9uIEtERC4KICAgICAgICBrZXQodGVuLCBLREQsIGYiY29uZyBLSE9ORyBnaWV0IGR1b2MgZG90IGJpZW4gY3VhIGNo',
'aW5oIG5vICh7Z2lldC5nZXQobWEpIXJ9KSIKICAgICAgICAgICAgICAgICAgICAgIGYiIC0+IGNodSBEQVQgbmF5IGtob25n',
'IGNvIGdpYSB0cmkiKQogICAgZWxzZToKICAgICAgICBrZXQodGVuLCB0dCwgY3QpCgojIC0tLS0tLS0tLS0tLS0tLS0gNC4g',
'TjcgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4o',
'IiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjQuIE43IOKAlCBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIChjYXkgdGhhdCBL',
'SE9ORyBiaSBkdW5nIHRvaSkiKQogICAgdHJ1b2MgPSB0ZXAucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1B',
'VV9XSU4pCiAgICBnaGkoIm43X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIgIHNvIGRvbmcga2hvcCB7TUFVX1dJTiFyfTogVFJV',
'T0MgPSB7dHJ1b2N9IFttb25nIDFdIikKICAgIGlmIHRydW9jICE9IDE6CiAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFu',
'aCBXaW5kb3dzIiwgS0RELCBmIm1hdSB4dWF0IGhpZW4ge3RydW9jfSBsYW4sIGtob25nIHBoYWkgMSIpCiAgICBlbHNlOgog',
'ICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdG1wOgogICAgICAgICAgICBzYW8gPSBQYXRo',
'KHRtcCkvImNheSIKICAgICAgICAgICAgc2h1dGlsLmNvcHl0cmVlKGdvYywgc2FvLCBpZ25vcmU9c2h1dGlsLmlnbm9yZV9w',
'YXR0ZXJucygiLmdpdCIsICJfX3B5Y2FjaGVfXyIsICIqLnB5YyIpKQogICAgICAgICAgICBmMiA9IHNhby8ib3BzIi8ibGVh',
'c2VfcHVibGlzaC5weSIKICAgICAgICAgICAgZjIud3JpdGVfdGV4dChmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04Iiku',
'cmVwbGFjZShNQVVfV0lOLCAiaWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHNhdSA9IGYyLnJl',
'YWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKTsgZ2hpKCJuN19zYXUiLCBzYXUpCiAgICAgICAgICAg',
'IGlubihmIiAgU0FVIChkYSBkb3QgYmllbikgPSB7c2F1fSBbbW9uZyAwXSIpCiAgICAgICAgICAgIGlmIHNhdSAhPSAwOgog',
'ICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCAiZG90IGJpZW4gS0hPTkcgYXAg',
'ZHVvYyIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICByY19tLCBvdXRfbSA9IGNoYXkoWyJvcHMvbGVhc2Vf',
'cHVibGlzaF90ZXN0LnB5Il0sIHNhbykKICAgICAgICAgICAgICAgIG0xNjUgPSBtYXVfY2Eob3V0X20sICJ0MTY1Iik7IGRt',
'LCBfLCBfID0gZG9jX2RvKG91dF9tKQogICAgICAgICAgICAgICAgdGVuMTY1ID0gbmV4dCgodCBmb3IgdCBpbiBkbSBpZiB0',
'LnN0YXJ0c3dpdGgoInQxNjUiKSksIE5vbmUpCiAgICAgICAgICAgICAgICBseSA9IChkbS5nZXQodGVuMTY1KSBvciAiIikK',
'ICAgICAgICAgICAgICAgIGdoaSgibjdfdDE2NSIsIG0xNjUpOyBnaGkoIm43X2x5X2RvIiwgbHlbOjIwMF0pCiAgICAgICAg',
'ICAgICAgICBpbm4oZiIgIHQxNjUgc2F1IGRvdCBiaWVuOiB7bTE2NX0gfCB7bHlbOjExMF19IikKICAgICAgICAgICAgICAg',
'IGR1bmdfbHlfZG8gPSAiUEFUSCB0IiBpbiBseSBvciAiL3Vzci9iaW4iIGluIGx5CiAgICAgICAgICAgICAgICBrZXQoIk43',
'IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBEQVQgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykgZWxzZQogICAg',
'ICAgICAgICAgICAgICAgIChUUlVPVCBpZiBtMTY1ID09ICJETyIgZWxzZSBLREQpLAogICAgICAgICAgICAgICAgICAgICJn',
'aWV0IGR1bmcgbHkgZG8iIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pCiAgICAgICAgICAgICAgICAgICAgZWxz',
'ZSAoIkRPIG5odW5nIEtIT05HIGR1bmcgbHkgZG8gLT4gdGluIGR1bmcgZ2lhIiBpZiBtMTY1ID09ICJETyIgZWxzZSAia2hv',
'bmcgZG9jIGR1b2MgdDE2NSIpKQoKIyAtLS0tLS0tLS0tLS0tLS0tIEtFVCBMVUFOIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIi',
'KTsgaW5uKCI9IiAqIDc4KQppbm4oZiJUSEUgSEUgRE8gRFVPQzoge3RoZV9oZX0gICBIRUFEPXtoZWFkWzoxMl19IikKIyBL',
'aG9pIGRhbiBjaG8gcmV2aWV3ZXIgYmF0IGRhdSBvIGRvbmcgdHJlbiwgbmVuIENIRSBETyBwaGFpIG5hbSBOR0FZIGR1b2kg',
'bm86IGtob25nIGNvIGRvbmcgbmF5CiMgdGhpIG1vdCBsdW90IC0tY2hpLXByb2JlIGluICJEQVQgNyB8IFRSVU9UIDAgfCBL',
'SE9ORyBETyBEVU9DIDAiIHJjPTAgbWEga2hvbmcgbm9pIGxhIGNodWEgY2hheSBibyB0ZXN0LgpnaGkoImNoZV9kbyIsICJj',
'aGktcHJvYmUiIGlmIENISV9QUk9CRSBlbHNlICJkYXktZHUiKQppZiBDSElfUFJPQkU6CiAgICBpbm4oIi0tY2hpLXByb2Jl',
'OiBDSEkgZG8gbXVjIDAsIDEsIDMuIEJvIHRlc3QsIE4xLU40LCB0MTM2LCBONyBLSE9ORyBjaGF5IC0gZGF5IEtIT05HIHBo',
'YWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQppZiB0aGVfaGUgPT0gImcxIjoKICAgIGlubigiTFVVIFk6IGRheSBsYSBORU4g',
'RE8gKGcxKSwgS0hPTkcgcGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hvdCBOOC1OMTIgZHVvaSBkYXkiKQogICAgaW5uKCIg',
'ICAgICAgVFJVT1QgbGEgRFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEgbmh1bmcgbG8gZzIgc2luaCByYSBkZSB2w6EuIikK',
'aW5uKCItIiAqIDc4KQpmb3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAgIGlubihmIiAge3R0OjE0fSB7dGVufSIgKyAoZiIg',
'ICB7Y3R9IiBpZiBjdCBlbHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQpu',
'X3RydW90ID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQppbm4oIi0iICogNzgpCmlubihmIiAg',
'REFUIHtzdW0oMSBmb3IgXyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8IFRSVU9UIHtuX3RydW90fSB8IEtIT05HIERPIERV',
'T0Mge25fa2RkfSIpCmlubihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgnc29fY2FfZG8nKX0gfCBkYW5oIHNhY2ggZGF5IGR1',
'OiB7J0NPJyBpZiBzby5nZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAnS0hPTkcgRE8gRFVPQyd9IikKaW5uKGYiICBBZG1p',
'bmlzdHJhdG9yOiB7c28uZ2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxpbms6IHtzby5nZXQoJ3N5bWxpbmtfZHVvYycpfSIp',
'CmlubigiIik7IGlubigiLS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5BWSBWRSBDSE8gUkVWSUVXRVIgLS0tIikKZ2hpKCJj',
'aG90IiwgW3sidGVuIjogYSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3RpZXQiOiBjfSBmb3IgYSwgYiwgYyBpbiBjaG90XSkK',
'aW5uKGpzb24uZHVtcHMoc28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50PTEsIGRlZmF1bHQ9c3RyKSkKIyByYzogMCA9',
'IG1vaSBjaG90IERBVCB8IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNvIGNob3QgS0hPTkcgRE8gRFVPQyAodXUgdGllbiBi',
'YW8gZG9uZykKc3lzLmV4aXQoMyBpZiBuX2tkZCBlbHNlICgxIGlmIG5fdHJ1b3QgZWxzZSAwKSkK'
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
