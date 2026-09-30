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
    [string]$Base    = '',     # thu muc lam viec. Mac dinh: thu muc chua chinh tep nay
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
$ShaBoDo    = 'ce33fbfbcc501de40353fad3eb8bc5b54da7b4c9c7ae81952480bedb711b6655'      # SHA-256 cua bo do Python nhung ben duoi

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
# Giai nen vao thu muc CONG CU, KHONG vao $Base: chay tai cho trong kho thi $Base la
# ops/reviews, va `Move-Item -Force` ban cu DE THANG tep .py dang duoc theo doi.
New-Item -ItemType Directory -Force -Path $CongCu | Out-Null
$BoDo = Join-Path $CongCu 'wp541-do-g2-windows.py'
# Tep .py canh ps1 chi la BAN SAO THU HAI khi ps1 nam DUNG cho trong kho (<goc>\ops\reviews,
# <goc>\.git co that). Lech ban nhung => DUNG: khong cong nao trong kho buoc hai ban khop
# (kiem tren Linux: --kiem-dong-bo). NGOAI kho (vd. Downloads) tep canh ps1 la RAC do ban ps1
# CU de lai (ban cu giai nen vao $Base) - chan o day la chan nham dung duong nang cap (do tren
# pwsh 7.4: ps1 moi + .py cua aa2be9a canh no => rc=3 "hai ban sao da troi").
$Canh = $null
if ($PSScriptRoot) {
    # GetDirectoryName tra $null o goc o dia, KHONG nem (Split-Path -Parent '' nem, do tren pwsh 7.4).
    $cha    = [IO.Path]::GetDirectoryName($PSScriptRoot)
    $gocKho = if ($cha) { [IO.Path]::GetDirectoryName($cha) } else { $null }
    if ($gocKho -and (Test-Path -LiteralPath (Join-Path $gocKho '.git'))) {
        $Canh = Join-Path $PSScriptRoot 'wp541-do-g2-windows.py'
    } elseif (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'wp541-do-g2-windows.py')) {
        Write-Host '  bo qua wp541-do-g2-windows.py canh ps1: ngoai kho, la ban giai nen cua ps1 cu'
    }
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
'MmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0wOS0zMGEiICAgICAgICAgICAgICAjIGRvaSBNT0kga2hpIHN1YSBi',
'byBkbyAtIGxvZyB0dSBraGFpIGJhbiBuYW8KVFJBTl9URVAsIFRSQU5fRE9ORyA9IDIsIDQwMCAgICAgICAgICAjIE43JyBj',
'dWEgc3BlYyByMwpNQVVfV0lOICA9ICdpZiBuZW5fdGh1YyA9PSAid2luZG93cyI6JwojIFdyaXRlIHNldCBjdWEgcGFja2V0',
'ICM1NDEgZzIuIERpZmYga2hvbmcgY2hhbSB0ZXAgbmFvIG8gZGF5ID0+IGRvIE5IQU0gTkhBTkguCldSSVRFX1NFVF9HMiA9',
'IHsib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJ9CiMgIlR1b2kiIGNoaSBjbyBu',
'Z2hpYSBraGkgc28gdm9pIE1BWSBDSFUgVEhBVC4gTW90IG1pcnJvciBjdWMgYm8gY3UgY3VuZyB0cmEgbHMtcmVtb3RlID09',
'CiMgb3JpZ2luL21hc3RlciAoZG8gZHVvYzogbWFzdGVyIGMxNmJkMzIgLT4gInZlIG5lbiBUVU9JIiwgNDYgdGVwIC8gKzcx',
'MTggY2hvIDBlYTk1ZGUpLgojIERhbmggc2FjaCBDSE8gUEhFUDsgYHJlbW90ZSBnZXQtdXJsYCBkYSBraGFpIHRyaWVuIGlu',
'c3RlYWRPZiBuZW4gY2h1eWVuIGh1b25nIGN1bmcgbG8gcmEuClVSTF9LSE9fSE9QX0xFID0geyJodHRwczovL2dpdGh1Yi5j',
'b20vZHVjdGhhbmdoby90cmEtbHVhdCIsICJodHRwczovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdC5naXQifQoj',
'IGByZW1vdGUgZ2V0LXVybGAgS0hBSSBUUklFTiBpbnN0ZWFkT2YsIG1hIG1hdSBgdXJsLiJodHRwczovLzx0b2tlbj5AZ2l0',
'aHViLmNvbS8iLmluc3RlYWRPZmAgcmF0IHBobwojIGJpZW4uIEluL2doaSBuZ3V5ZW4gdmFuIGxhIGR1YSBUT0tFTiB2YW8g',
'bG9nIHZhIHZhbyBraG9pIEpTT04gcHMxIGJhbyBkYW4gY2hvIHJldmlld2VyIChkbyBkdW9jOgojIDMgZG9uZyB0cm9uZyBr',
'aG9pIGRhbikuIEJvIHVzZXJpbmZvIFRSVU9DIGtoaSBpbiB2YSBUUlVPQyBraGkgc28g4oCUIHRva2VuIHZhbiBsYSBHaXRI',
'dWIgdGhhdC4KX1JYX1VTRVJJTkZPID0gcmUuY29tcGlsZShyIl4oW0EtWmEtel1bQS1aYS16MC05Ky4tXSo6Ly8pW14vXSpA',
'IikKZGVmIF91cmxfc2FjaCh1KTogcmV0dXJuIF9SWF9VU0VSSU5GTy5zdWIociJcMSIsIHUgb3IgIiIpCiMgQ2EgbmdvYWkg',
'cGhhbSB2aSByMyDCp25nb2FpX3BoYW1fdmkg4oCUIGRvIENISU5IIFNQRUMga2hhaSwga2hvbmcgcGhhaSBibyBkbyB0dSBx',
'dXlldC4KIyBEbyBsYSBEQU5IIFNBQ0ggQ0hPIFBIRVA6IGNhIGRvIG5hbyBLSE9ORyBuYW0gdHJvbmcgZGF5IHZhIEtIT05H',
'IHBoYWkgInRoaWV1IGNvbmcgY3UiCiMgdGhpIGxhIFRSVU9ULiBEYW5oIHNhY2ggY2FtIHRoaSBiYW8gZ2lvIGN1bmcgdGhp',
'ZXU7IGRhbmggc2FjaCBjaG8gcGhlcCB0aGkgYmlldCB0cnVvYy4KTkdPQUlfUEhBTV9WSSA9IHNldCgidDEzMSB0MTMyIHQx',
'NTAgdDEyNSB0MzUgdDM2IHQzNyB0MzggdDM5IHQ0MCIuc3BsaXQoKSkKIyBDYSBjdWEgQ0hJTkggcGFja2V0IG5heS4gTW90',
'IGNhIG8gZGF5IG1hIERPIHRoaSBraG9uZyBiYW8gZ2lvIGR1b2MgYm8gcXVhLgpDQV9QQUNLRVQgPSBzZXQoInQxNjUgdDE2',
'NiB0MTY3IHQxNjggdDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpKQojIENhIE1PSSBtYSBnMiB0aGVtIHZhbyAo',
'TjgtTjEyKS4gRG9pIHR1b25nIGRvIHBoYWkgTUFORyBjaHVuZyB2YW86IG1lcmdlLWJhc2UgY2h1YSBjbywgSEVBRCBjby4K',
'Q0FfTU9JX0cyID0gInQxNjkgdDE3MCB0MTcxIHQxNzIgdDE3MyIuc3BsaXQoKQpDQTE1ICA9ICJ0MTI5IHQxMzAgdDEzMSB0',
'MTMyIHQxMzMgdDEzNiB0MTM4IHQxMzkgdDE0NCB0MTQ1IHQxNDYgdDE0NyB0MTQ5IHQxNTAgdDE1MSIuc3BsaXQoKQpDQU1P',
'SSA9ICJ0MTY1IHQxNjYgdDE2NyB0MTY4Ii5zcGxpdCgpCgpEQVQsIFRSVU9ULCBLREQgPSAiREFUIiwgIlRSVU9UIiwgIktI',
'T05HIERPIERVT0MiCnNvLCBjaG90ID0ge30sIFtdCmRlZiBnaGkoaywgdik6IHNvW2tdID0gdjsgcmV0dXJuIHYKZGVmIGtl',
'dCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0PSIiKToKICAgIGNob3QuYXBwZW5kKCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90',
'aWV0KSkKICAgIGlubihmIiAgW3t0cmFuZ190aGFpOjE0fV0ge3Rlbn0iICsgKGYiICAge2NoaV90aWV0fSIgaWYgY2hpX3Rp',
'ZXQgZWxzZSAiIikpCiAgICByZXR1cm4gdHJhbmdfdGhhaQoKIyAtLS0tLS0tLS0tLS0tLS0tIGRvYyBsb2cgY3VhIGJvIHRl',
'c3QgKGJhbiAzLCBkYSBkbyB0cmVuIGxvZyBUSEFUKSAtLS0tLS0tLS0tLS0tLS0tClJYX0RPX0NITyAgPSByZS5jb21waWxl',
'KHIiKD9tKV4hISEgZG8gKFxTKykgKC4qKSQiKQpSWF9ET19DVU9JID0gcmUuY29tcGlsZShyIig/bSleIHsyfShcU3sxLDR9',
'KSB7Mn0oXFMrKTogKC4qKSQiKQpSWF9CT19RVUEgID0gcmUuY29tcGlsZShyIig/bSleIHsyfVxTezEsNn0gUVVBIChcUysp',
'OiAoLiopJCIpClJYX1RPTkcgICAgPSByZS5jb21waWxlKHIibGVhc2VfcHVibGlzaDogKFxkKykvKFxkKylcYlteXG5dKj89',
'KFxkKyksW15cbl0qPz0oXGQrKSIpCgpkZWYgc29fY2EodCk6CiAgICBtID0gcmUubWF0Y2gociJ0KFxkKykiLCB0KTsgcmV0',
'dXJuIChpbnQobS5ncm91cCgxKSkgaWYgbSBlbHNlIDEwKio2LCB0KQoKZGVmIGRvY19kbyhvdXQpOgogICAgdGFpX2NobyA9',
'IHt0OiBsLnN0cmlwKCkgZm9yIHQsIGwgaW4gUlhfRE9fQ0hPLmZpbmRhbGwob3V0KX0KICAgIGJvID0ge3QgZm9yIHQsIF8g',
'aW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0KX0KICAgIGN1b2kgPSB7dDogbC5zdHJpcCgpIGZvciBfLCB0LCBsIGluIFJYX0RP',
'X0NVT0kuZmluZGFsbChvdXQpIGlmIHQgbm90IGluIGJvfQogICAgaG9wID0gZGljdChjdW9pKTsgaG9wLnVwZGF0ZSh0YWlf',
'Y2hvKQogICAgZ2MsIHRpbiA9IFtdLCBUcnVlCiAgICBpZiBzZXQodGFpX2NobykgIT0gc2V0KGN1b2kpOgogICAgICAgIGdj',
'LmFwcGVuZChmImhhaSBuZ3VvbiBMRUNIOiBjaGktdGFpLWNobz17c29ydGVkKHNldCh0YWlfY2hvKS1zZXQoY3VvaSkpfSBj',
'aGktY3VvaT17c29ydGVkKHNldChjdW9pKS1zZXQodGFpX2NobykpfSIpCiAgICAgICAgdGluID0gRmFsc2UKICAgIG0gPSBS',
'WF9UT05HLnNlYXJjaChvdXQpCiAgICBpZiBub3QgbToKICAgICAgICBnYy5hcHBlbmQoIktIT05HIGRvYyBkdW9jIGRvbmcg',
'dG9uZyBrZXQiKTsgdGluID0gRmFsc2UKICAgIGVsc2U6CiAgICAgICAgZGF0LCB0cmVuID0gaW50KG0uZ3JvdXAoMSkpLCBp',
'bnQobS5ncm91cCgyKSkKICAgICAgICBnYy5hcHBlbmQoZiJzbyBob2M6IHt0cmVufS17ZGF0fT17dHJlbi1kYXR9IGRvOyBk',
'b2MgZHVvYyB7bGVuKGhvcCl9IikKICAgICAgICBpZiB0cmVuIC0gZGF0ICE9IGxlbihob3ApOgogICAgICAgICAgICBnYy5h',
'cHBlbmQoZiJMRUNIIFNPIEhPQzogdGhpZXUge3RyZW4tZGF0LWxlbihob3ApfSBjYSIpOyB0aW4gPSBGYWxzZQogICAgcmV0',
'dXJuIGhvcCwgZ2MsIHRpbgoKX01BVSA9ICgiISEhIGRvIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU4gYVxuIgogICAg',
'ICAgICIhISEgZG8gdDE1MF94IFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAgICAgIiAgQuG7jiBR',
'VUEgdDEzMV95OiBuZW4gZml4dHVyZVxuIgogICAgICAgICIgIMSQ4buOICB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVO',
'OiBhXG4iCiAgICAgICAgIiAgxJDhu44gIHQxNTBfeDogV2luRXJyb3IgMTMxNCByZXF1aXJlZCBwcml2aWxlZ2VcbiIKICAg',
'ICAgICAibGVhc2VfcHVibGlzaDogMS8zIMSR4bqhdDsgxJHDoyBjaOG6oXk9MywgYuG7jyBxdWE9MVxuIikKCmRlZiBjaGF5',
'KGFyZ3YsIGN3ZCwgcGh1dD02MCk6CiAgICBtdCA9IGRpY3Qob3MuZW52aXJvbiwgUFlUSE9OVVRGOD0iMSIsIFBZVEhPTklP',
'RU5DT0RJTkc9InV0Zi04IiwKICAgICAgICAgICAgICBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0iMSIsIFBZVEhPTlVOQlVG',
'RkVSRUQ9IjEiKQogICAgcCA9IHN1YnByb2Nlc3MucnVuKFtzeXMuZXhlY3V0YWJsZV0gKyBhcmd2LCBjd2Q9c3RyKGN3ZCks',
'IGNhcHR1cmVfb3V0cHV0PVRydWUsCiAgICAgICAgICAgICAgICAgICAgICAgdGV4dD1UcnVlLCBlbmNvZGluZz0idXRmLTgi',
'LCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjAsIGVudj1tdCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChw',
'LnN0ZG91dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1X2NhKG91dCwgdCk6CiAgICBtID0gcmUuc2VhcmNo',
'KHIiKD9tKV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSBbMC05Ll0rcyAoXHcrKVxzKiQiLCBvdXQpCiAgICByZXR1',
'cm4gbS5ncm91cCgyKSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdpdChnb2MsICphLCBwaHV0PTUpOgogICAgcCA9IHN1YnByb2Nl',
'c3MucnVuKFsiZ2l0IiwgIi1DIiwgc3RyKGdvYyksICphXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLAogICAg',
'ICAgICAgICAgICAgICAgICAgIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCkK',
'ICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikuc3RyaXAoKSwgKHAuc3RkZXJyIG9yICIiKS5zdHJp',
'cCgpCgoKIyA9PT09PT09PT09PT09PT09PSBOQU0gUFJPQkUsIHZpZXQgdGhhbmggSEFNIFRIVUFOIGRlIFRVIEtJRU0gZHVv',
'YyA9PT09PT09PT09PT09PT09PQojIE1vaSBoYW0gdHJhICh0cmFuZ190aGFpLCBjaGlfdGlldCwgZHVfbGlldSkuIEtIT05H',
'IGluLCBLSE9ORyB0aG9hdCDigJQgbmhvIHZheSBjaHVuZwojIGNoYXkgZHVvYyB0cmVuIG5lbiBCQVQgS1ksIHZhIGAtLXR1',
'LWtpZW0tcHJvYmVgIGdvaSB0aGFuZyBjaHVuZyBkZSBraWVtIGNoaW5oIGJvIGRvLgoKZGVmIF9zYW4odCk6CiAgICBkID0g',
'UGF0aCh0KS8iZCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBm',
'IjsgcGYubWtkaXIoKQogICAgcmV0dXJuIGQsIGN3LCBwZgoKZGVmIGRvX244KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkJ1',
'b2MgMSAoQ09OR19DVV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0LmV4ZS4gRG9pIGNodW5nIGR1b25nOiBnaXQuZXhlIFZBTiBw',
'aGFpIG5oYW4uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAg',
'ICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIGZvciB0ZW4gaW4gKCJnaXQuZXhlIiwgImdpdC5iYXQiLCAiZ2l0',
'LmNtZCIsICJnaXQucHkiLCAia2hvbmctcGhhaS1naXQudHh0Iik6CiAgICAgICAgICAgIGYgPSBkL3RlbjsgZi53cml0ZV90',
'ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyA9IGdvaShjb25nX2N1X2dpdD1zdHIoZiksIHBh',
'dGg9IiIsIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIGtxW2YiQ09OR19DVV9HSVQ9',
'e3Rlbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIlRVIENIT0kiCiAgICBsb3QgPSBbayBmb3IgaywgdiBpbiBrcS5pdGVtcygp',
'IGlmIHYgPT0gIk5IQU4iIGFuZCBub3Qgay5lbmRzd2l0aCgiZ2l0LmV4ZSIpXQogICAgaWYga3EuZ2V0KCJDT05HX0NVX0dJ',
'VD1naXQuZXhlIikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogZ2l0LmV4',
'ZSBob3AgbGUgbWEgYmkgdHUgY2hvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgbG90IGVsc2UgVFJVT1QpLCAoIiIg',
'aWYgbm90IGxvdCBlbHNlIGYiY29uIG5oYW46IHtsb3R9IiksIGtxCgpkZWYgZG9fbjkoZ29pLCBzaWcsIHRlcHQpOgogICAg',
'IiIiTXVjIFBBVEggYm9jIG5oYXkga2VwIHBoYWkgTkhBTjsgbXVjIHJvbmcgLyB0b2FuIGtob2FuZyB0cmFuZyBwaGFpIGJv',
'IHF1YSwga2hvbmcgbmVtLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBh',
'cyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtk',
'aXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngi',
'LCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGZvciBuaGFuLCBtdWMgaW4gKCgia2hvbmcgbmhheSIsIHN0cihkKSksICgi',
'Y28gbmhheSBrZXAiLCBmJyJ7ZH0iJyksCiAgICAgICAgICAgICAgICAgICAgICAgICAgKCJyb25nIiwgIiIpLCAoImNoaSBr',
'aG9hbmcgdHJhbmciLCAiICAgIikpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICByLCBfID0gZ29pKHBhdGg9',
'bXVjLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFu',
'fSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAg',
'ICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gZiJORU0ge3R5cGUoZSkuX19uYW1lX199IgogICAgaWYga3EuZ2V0KCJQ',
'QVRIIGtob25nIG5oYXkiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBt',
'dWMgUEFUSCB0aHVvbmcgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgb2sgPSAoa3EuZ2V0KCJQQVRIIGNvIG5o',
'YXkga2VwIikgPT0gIk5IQU4iCiAgICAgICAgICBhbmQga3EuZ2V0KCJQQVRIIHJvbmciKSA9PSAiTm9uZSIgYW5kIGtxLmdl',
'dCgiUEFUSCBjaGkga2hvYW5nIHRyYW5nIikgPT0gIk5vbmUiKQogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCks',
'ICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKIyBEYXUgcGhhbiBjYWNoIGR1bmcgREUgVEhVLiBQaGFpIEtIQUMg',
'b3MucGF0aHNlcCB0cmVuIENBIEhBSSBuZW4gKCc7JyBXaW5kb3dzLCAnOicgUE9TSVgpCiMgdGhpIGhhaSBnaWEgdGh1eWV0',
'ICJ0YWNoIHRoZW8gZGF1IGR1b2MgdHJ1eWVuIiB2YSAidGFjaCB0aGVvIG9zLnBhdGhzZXAiIG1vaSByb2kgcmEgbmhhdS4K',
'VEhVX04xMCA9ICJ8IgoKZGVmIGRvX24xMChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW0gcGhhaSB0YWNoIFBBVEggdGhl',
'byBkYXUgcGhhbiBjYWNoIERVT0MgVFJVWUVOLCBraG9uZyB0aGVvIG9zLnBhdGhzZXAgY3VhIG5lbi4KCiAgICBCYW4gY3Ug',
'ZG8gIm1vdCBkYXUgJzsnIHRyb25nIFRFTiB0aHUgbXVjIiB2YSBkYXQgREFUIHRyZW4gV2luZG93cyBkdSBoYW0gc2FpLiBO',
'bwogICAgZGVnZW5lcmF0ZTogdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnLCBuZW4gJ0M6L2E7YicgdGhhdCBz',
'dSBDTyBOR0hJQSBsYSBoYWkKICAgIG11YyDigJQgInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gcmEgY3VuZyBrZXQg',
'cXVhLCBwaGVwIGRvIGtob25nIHRoZSBkbyBuYW8uIE5vCiAgICBkYSBjaGFtIERBVCBjaG8gOTU4MzE2ODUgdHJvbmcga2hp',
'IHQxNzEgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQgYXkuCiAgICBNb3QgY29uZyBraG9uZyB0',
'aGUgZG8gdGhpIGtob25nIHBoYWkgY29uZy4KICAgICIiIgogICAgdGVuX3NlcCA9IG5leHQoKGsgZm9yIGsgaW4gKCJwaGFu',
'X2NhY2giLCAiZGF1X3BoYW5fY2FjaCIsICJzZXAiKSBpZiBrIGluIHNpZy5wYXJhbWV0ZXJzKSwgTm9uZSkKICAgIGlmIHRl',
'bl9zZXAgaXMgTm9uZToKICAgICAgICAjIEtob25nIGNvIHRoYW0gc28gdGhpIHRyZW4gV2luZG93cyBLSE9ORyBjb24gZHVv',
'bmcgbmFvIHRhY2ggaGFpIGdpYSB0aHV5ZXQuCiAgICAgICAgaWYgb3MucGF0aHNlcCA9PSAiOyI6CiAgICAgICAgICAgIHJl',
'dHVybiAoS0RELCAidHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIHZhIGhhbSBraG9uZyBuaGFuIHRoYW0gc28g',
'ZGF1IHBoYW4gY2FjaCAiCiAgICAgICAgICAgICAgICAgICAgICAgICAiLT4ga2hvbmcgdGFjaCBkdW9jIGhhaSBnaWEgdGh1',
'eWV0IiwKICAgICAgICAgICAgICAgICAgICB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiBOb25l',
'fSkKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgICAgIGxhID0gUGF0',
'aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKQogICAgICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgICAgIChk',
'LyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8gID0gZ29pKHBh',
'dGg9c3RyKGxhKSArIG9zLnBhdGhzZXAgKyBzdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAg',
'ICAgICAgICAgIHIwLCBfID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQog',
'ICAgICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZSwKICAgICAgICAgICAg',
'ICAiY28gbXVjIGNodWEgJzsnIjogIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIsCiAgICAgICAgICAgICAgImRvaSBjaHVuZyBk',
'dW9uZyAoa2hvbmcgY28gJzsnKSI6ICJOSEFOIiBpZiByMCBlbHNlICJOb25lIn0KICAgICAgICBpZiBub3QgcjA6CiAgICAg',
'ICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZyIsIGtxCiAgICAgICAgcmV0dXJuIChEQVQgaWYgciBl',
'bHNlIFRSVU9UKSwgKCIiIGlmIHIgZWxzZSAibXVjIGdpdC5leGUgaG9wIGxlIGJpIE1BVCIpLCBrcQoKICAgIHdpdGggdGVt',
'cGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGly',
'KCkgICAgICAgICAgIyAnOycgbmFtIHRyb25nIFRFTiwga2hvbmcgcGhhaSBkYXUgcGhhbiBjYWNoCiAgICAgICAgZCwgY3cs',
'IHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAg',
'ICAgICAgbm9pID0gc3RyKGxhKSArIFRIVV9OMTAgKyBzdHIoZCkKICAgICAgICBrdyA9IGRpY3QocHJvZ3JhbV9maWxlcz1z',
'dHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICByX2NoaW5oLCBfID0gZ29pKHBhdGg9bm9pLCAgICAgICoqe3Rlbl9zZXA6',
'IFRIVV9OMTB9LCAgICoqa3cpICAgIyB0YWNoIGR1bmcgIC0+IE5IQU4KICAgICAgICByX2R1b25nLCBfID0gZ29pKHBhdGg9',
'c3RyKGQpLCAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyBkb2kgY2h1bmcgZHVvbmcKICAgICAgICByX3Bo',
'YW5iaWV0LCBfID0gZ29pKHBhdGg9bm9pLCAgICoqe3Rlbl9zZXA6IG9zLnBhdGhzZXB9LCAqKmt3KSAgIyB0YWNoIHRoZW8g',
'b3MucGF0aHNlcCAtPiBtYXQKICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogdGVu',
'X3NlcCwgImRhdSB0aHUiOiBUSFVfTjEwLAogICAgICAgICAgZiJub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtU',
'SFVfTjEwIXJ9IjogICAgICAgIk5IQU4iIGlmIHJfY2hpbmggZWxzZSAiTm9uZSIsCiAgICAgICAgICBmImRvaSBjaHVuZyBk',
'dW9uZyAobW90IG11Yywge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9KSI6ICAiTkhBTiIgaWYgcl9kdW9uZyBlbHNlICJOb25lIiwK',
'ICAgICAgICAgIGYicGhhbiBiaWV0OiBub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtvcy5wYXRoc2VwIXJ9Ijog',
'Ik5IQU4iIGlmIHJfcGhhbmJpZXQgZWxzZSAiTm9uZSJ9CiAgICBpZiBub3Qgcl9kdW9uZzoKICAgICAgICByZXR1cm4gS0RE',
'LCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG1vdCBtdWMgaG9wIGxlIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EKICAg',
'ICMgQ29uZyBwaGFpIENPIFRIRSBkby4gTmV1IGNhIGhhaSBkYXUgcGhhbiBjYWNoIGRldSByYSBOSEFOIHRoaSBwaGVwIGRv',
'IGtob25nIHBoYW4KICAgICMgYmlldCBkdW9jIGdpIOKAlCBkdW5nIGJhbyBEQVQsIGJhbyB0aGFuZyBsYSBraG9uZyBkbyBk',
'dW9jLgogICAgaWYgcl9waGFuYmlldDoKICAgICAgICByZXR1cm4gKEtERCwgZiJwaGVwIGRvIEtIT05HIHBoYW4gYmlldCBk',
'dW9jOiBub2kgYmFuZyB7VEhVX04xMCFyfSBtYSB0YWNoIHRoZW8gIgogICAgICAgICAgICAgICAgICAgICBmIntvcy5wYXRo',
'c2VwIXJ9IFZBTiB0aW0gcmEgZ2l0LmV4ZSIsIGtxKQogICAgcmV0dXJuICgoREFULCAiIiwga3EpIGlmIHJfY2hpbmggZWxz',
'ZQogICAgICAgICAgICAoVFJVT1QsIGYidGFjaCB0aGVvIG9zLnBhdGhzZXAgdGhheSB2aSB0aGVvIHt0ZW5fc2VwfSBkdW9j',
'IHRydXllbiIsIGtxKSkKCgpkZWYgZG9fbjExKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIlRydXllbiBjaGFuX2RvYW4gPT4g',
'dGh1IGR1b2MgdGhvbmcgYmFvIFZBIHN0ZGVyciBJTS4gS2hvbmcgdHJ1eWVuID0+IHN0ZGVyciBWQU4gY28uIiIiCiAgICBp',
'ZiAiY2hhbl9kb2FuIiBub3QgaW4gc2lnLnBhcmFtZXRlcnM6CiAgICAgICAgcmV0dXJuIEtERCwgIl9naXRfd2luZG93cyBr',
'aG9uZyBuaGFuIHRoYW0gc28gY2hhbl9kb2FuIiwgeyJ0aGFtIHNvIjogbGlzdChzaWcucGFyYW1ldGVycyl9CiAgICB3aXRo',
'IHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAg',
'IChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgY2QgPSBbXQogICAgICAg',
'IF8sIGVfY28gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdyksIGNoYW5fZG9h',
'bj1jZCkKICAgICAgICBfLCBlX2toID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIo',
'Y3cpKQogICAga3EgPSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAobXVjKSI6IGxlbihjZCksCiAgICAgICAgICAic3RkZXJyIGto',
'aSBDTyBjaGFuX2RvYW4gKGJ5dGUpIjogbGVuKGVfY28uZW5jb2RlKCkpLAogICAgICAgICAgInN0ZGVyciBraGkgS0hPTkcg',
'dHJ1eWVuIChieXRlKSI6IGxlbihlX2toLmVuY29kZSgpKX0KICAgIGlmIGxlbihjZCkgPT0gMCBhbmQgbGVuKGVfa2guZW5j',
'b2RlKCkpID09IDA6CiAgICAgICAgcmV0dXJuIEtERCwgIm5oYW5oICVQcm9ncmFtRmlsZXMlIGtob25nIHBoYW4gZ2lhaSBL',
'SE9ORyBiYXkgcmEgY2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRvIGR1b2MiLCBrcQogICAgb2sgPSBsZW4oY2QpID4gMCBhbmQg',
'bGVuKGVfY28uZW5jb2RlKCkpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA+IDAKICAgIHJldHVybiAoREFUIGlmIG9r',
'IGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCmRlZiBkb19uMTIoZ29pLCBzaWcsIHRlcHQp',
'OgogICAgIiIiSGFuZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9uZyBmaXh0dXJlIHBoYWkgdHV5ZXQgZG9pIHRyZW4gQ0EgSEFJ',
'IG5lbi4iIiIKICAgIG5kID0gdGVwdC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIikKICAg',
'IGhhbmcgPSBzb3J0ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRfcGF0aFxzKj1ccyoiKFteIl0rKSInLCBuZCkpKQogICAgeGF1',
'ID0gW2ggZm9yIGggaW4gaGFuZyBpZiBub3QgKFB1cmVQb3NpeFBhdGgoaCkuaXNfYWJzb2x1dGUoKSBhbmQgUHVyZVdpbmRv',
'd3NQYXRoKGgpLmlzX2Fic29sdXRlKCkpXQogICAga3EgPSB7ImhhbmcgZ2l0X3BhdGggdGltIHRoYXkiOiBoYW5nLCAiY2hp',
'IHR1eWV0IGRvaSBNT1QgbmVuIjogeGF1fQogICAgaWYgbm90IGhhbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImtob25nIHRp',
'bSB0aGF5IGhhbmcgZ2l0X3BhdGggbmFvIHRyb25nIGZpeHR1cmUgLT4gbWF1IGRvYyBjbyB0aGUgZGEgZG9pIiwga3EKICAg',
'IHJldHVybiAoREFUIGlmIG5vdCB4YXUgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgeGF1IGVsc2UgZiJjaGktbW90LW5lbjog',
'e3hhdX0iKSwga3EKClBST0JFID0gWygiTjggYnVvYyAxIGNoaSBuaGFuIGdpdC5leGUiLCBkb19uOCksCiAgICAgICAgICgi',
'TjkgYm9jIG5oYXkga2VwIG8gbXVjIFBBVEgiLCBkb19uOSksCiAgICAgICAgICgiTjEwIGRhdSAnOycgdHJvbmcgdGVuIHRo',
'dSBtdWMiLCBkb19uMTApLAogICAgICAgICAoIk4xMSBjaGFuIGRvYW4gZG9pIGtlbmgiLCBkb19uMTEpLAogICAgICAgICAo',
'Ik4xMiBoYW5nIHNlbnRpbmVsIHR1eWV0IGRvaSBDQSBIQUkgbmVuIiwgZG9fbjEyKV0KCiMgLS0tIGNoZSBkbyBUVSBLSUVN',
'OiBjaGF5IG5hbSBwcm9iZSB0cmVuIG1vdCBjYXkgYmF0IGt5LCBuZW4gYmF0IGt5IC0tLQppZiAiLS10dS1raWVtLXByb2Jl',
'IiBpbiBzeXMuYXJndjoKICAgIF9nID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS10dS1raWVtLXByb2JlIikg',
'KyAxXSkucmVzb2x2ZSgpCiAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfdGsi',
'LCBzdHIoX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgIF9scCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9t',
'X3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbHApCiAgICBfc2lnID0gaW5zcGVjdC5zaWduYXR1cmUoX2xw',
'Ll9naXRfd2luZG93cykKICAgIGRlZiBfZ29pKCoqa3cpOgogICAgICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICAgICAgd2l0',
'aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICAgICAgcmV0dXJuIF9scC5fZ2l0X3dpbmRvd3MoKipr',
'dyksIGUuZ2V0dmFsdWUoKQogICAgcHJpbnQoZiJUVSBLSUVNIFBST0JFIHRyZW4ge19nfSAgKG5lbiB7c3lzLnBsYXRmb3Jt',
'fSkiKQogICAgZm9yIF90ZW4sIF9mIGluIFBST0JFOgogICAgICAgIF90dCwgX2N0LCBfZGwgPSBfZihfZ29pLCBfc2lnLCBf',
'Zy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBwcmludChmIiAgW3tfdHQ6MTR9XSB7X3Rlbn0iICsg',
'KGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgICAgICBmb3IgX2ssIF92IGluIChfZGwgb3Ige30pLml0ZW1zKCk6',
'IHByaW50KGYiICAgICAgICB7X2s6MzR9OiB7X3Z9IikKICAgIHN5cy5leGl0KDApCgojIC0tLSBjaGUgZG8gS0lFTSBET05H',
'IEJPOiB0ZXAgLnB5IG5heSBwaGFpIFRSVU5HIFRVTkcgQllURSB2b2kgYmFuIG5odW5nIHRyb25nIHBzMSAtLS0KIyBLaG9u',
'ZyBjb25nIG5hbyBidW9jIGhhaSBiYW4gc2FvIGtob3A6IGRvIGR1b2MsIG5vaSB0cmFuIDIvNDAwIC0+IDk5Lzk5OTk5IENI',
'SSB0cm9uZyAucHkKIyB0aGkgY2lfZGFuZ19reSBsYW4gdDI2L3QyNyB2YW4geGFuaCwgY29uIGNob3QgU0hBIGN1YSBwczEg',
'Y2hpIHNvIGJhbiBuaHVuZyB2b2kgaGFuZyBzbwojIGN1YSBDSElOSCBuby4gQ2hheTogcHl0aG9uIHdwNTQxLWRvLWcyLXdp',
'bmRvd3MucHkgLS1raWVtLWRvbmctYm8gd3A1NDEtZG8tZzIucHMxICAocmMgMHwzKQppZiAiLS1raWVtLWRvbmctYm8iIGlu',
'IHN5cy5hcmd2OgogICAgaW1wb3J0IGJhc2U2NAogICAgX3BzID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS1r',
'aWVtLWRvbmctYm8iKSArIDFdKS5yZWFkX3RleHQoZW5jb2Rpbmc9ImFzY2lpIikKICAgIF9tID0gcmUuc2VhcmNoKHIiKD9t',
'cyleXCRCNjQgPSBAXCgoLio/KV5cKSIsIF9wcykKICAgIF9rID0gcmUuc2VhcmNoKHIiKD9tKV5cJFNoYUJvRG9ccyo9XHMq',
'JyhbMC05YS1mXXs2NH0pJyIsIF9wcykKICAgIF9uaHVuZyA9IGJhc2U2NC5iNjRkZWNvZGUoIiIuam9pbihyZS5maW5kYWxs',
'KHIiJyhbQS1aYS16MC05Ky89XSopJyIsIF9tLmdyb3VwKDEpKSkpIGlmIF9tIGVsc2UgYiIiCiAgICBfdG9pID0gUGF0aChf',
'X2ZpbGVfXykucmVhZF9ieXRlcygpCiAgICBfb2sgPSBib29sKF9tIGFuZCBfaykgYW5kIF9uaHVuZyA9PSBfdG9pIGFuZCBo',
'YXNobGliLnNoYTI1NihfdG9pKS5oZXhkaWdlc3QoKSA9PSBfay5ncm91cCgxKQogICAgaW5uKGYiS0lFTSBET05HIEJPOiB7',
'REFUIGlmIF9vayBlbHNlIEtERH0gIChuaHVuZyB7bGVuKF9uaHVuZyl9IGJ5dGUsIHRlcCB7bGVuKF90b2kpfSBieXRlKSIp',
'CiAgICBzeXMuZXhpdCgwIGlmIF9vayBlbHNlIDMpCgppbm4oIj0iICogNzgpOyBpbm4oIldQNTQxIGcyIC0gcGhlcCBkbyB0',
'cmVuIFdpbmRvd3MgdGhhdCAoc3BlYyByMzogTjEtTjQsIE44LU4xMiwgTjcsIGtpY2ggdGh1b2MpIik7IGlubigiPSIgKiA3',
'OCkKCiMgLS0tLS0tLS0tLS0tLS0tLSB0dSBraWVtIGJvIGRvYyAtLS0tLS0tLS0tLS0tLS0tCl9kLCBfZywgX3QgPSBkb2Nf',
'ZG8oX01BVSkKX29rID0gKGxlbihfZCkgPT0gMiBhbmQgYW55KHguc3RhcnRzd2l0aCgidDAyYiIpIGZvciB4IGluIF9kKQog',
'ICAgICAgYW5kIG5vdCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMxIikgZm9yIHggaW4gX2QpIGFuZCBfdCkKaW5uKCJUdSBraWVt',
'IGJvIGRvYyBsb2c6IiwgREFUIGlmIF9vayBlbHNlIFRSVU9UKQppZiBub3QgX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9O',
'RyBETyBEVU9DOiBibyBkb2MgbG9nIGN1YSBjaGluaCBzY3JpcHQgbmF5IHNhaSAtPiBraG9uZyBkbyBnaSBjYS4iKTsgc3lz',
'LmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4gZG8gLS0tLS0tLS0tLS0tLS0tLQpnb2MgPSBQYXRoKHN5cy5h',
'cmd2WzFdKS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQYXRoLmN3ZCgpCnRlcCwgdGVwdCA9IGdvYyAv',
'ICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiCmlubigi',
'Iik7IGlubigiLSIgKiA3OCk7IGlubigiMC4gTkVOIERPIikKIyBNT0kgTE9HIFBIQUkgVFUgS0hBSSBubyBkbyBDQUkgR0kg',
'YmFuZyBCTyBETyBOQU8uIEJhaSBob2MgMTktMDktMjAyNjogbW90IGx1b3QgZG8KIyBndWkgdmUgZHVvYyBkb2Mgbmh1IGtl',
'dCBxdWEgY3VhIGJhbiB2YSBkYW5nIHhldCwgbmh1bmcgdGhhdCByYSBsYSBiYW4gZG8gQ1UgY2hheQojIHRyZW4gbmhhbmgg',
'S0hBQy4gRG9jIHJhIHRoaSBtYXQgbW90IHZvbmc7IGxvZyB0dSBraGFpIHRoaSB0aGF5IG5nYXkgZG9uZyBkYXUuCnRyeToK',
'ICAgIF90dSA9IGhhc2hsaWIuc2hhMjU2KFBhdGgoX19maWxlX18pLnJlYWRfYnl0ZXMoKSkuaGV4ZGlnZXN0KCkKZXhjZXB0',
'IEV4Y2VwdGlvbiBhcyBfZToKICAgIF90dSA9IGYia2hvbmcgdHUgYmFtIGR1b2M6IHtfZX0iCmdoaSgiYm9fZG9fc2hhMjU2',
'IiwgX3R1KQppbm4oZiIgIEJPIERPICAgICAgICA6IHNoYTI1NiB7X3R1WzoxNl19ICAoYmFuIHtCQU5fQk9fRE99KSIpCmlu',
'bigiICBzeXMucGxhdGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwgInwgcHl0aG9uIiwgc3lzLnZlcnNpb24uc3BsaXQoKVswXSkK',
'aW5uKCIgIG9zLnBhdGhzZXAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSwgInwgUEFUSEVYVDoiLCByZXByKG9zLmVudmlyb24u',
'Z2V0KCJQQVRIRVhUIikpWzo2MF0pCmlubigiICBQcm9ncmFtRmlsZXMgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlByb2dy',
'YW1GaWxlcyIpKSwgInwgU3lzdGVtUm9vdDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290IikpKQppbm4oIiAg',
'Q09OR19DVV9HSVQgIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJDT05HX0NVX0dJVCIpKSkKaW5uKCIgIGdvYyBraG8gICAg',
'ICA6IiwgZ29jKQoKcXV5ZW4gPSBOb25lCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAgIGlt',
'cG9ydCBjdHlwZXM7IHF1eWVuID0gYm9vbChjdHlwZXMud2luZGxsLnNoZWxsMzIuSXNVc2VyQW5BZG1pbigpKQogICAgZXhj',
'ZXB0IEV4Y2VwdGlvbjogcXV5ZW4gPSBOb25lCmdoaSgicXV5ZW5fYWRtaW4iLCBxdXllbikKc3ltbGlua19kdW9jID0gTm9u',
'ZQp0cnk6CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgodCkv',
'ImEudHh0IjsgZC53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICB0cnk6IG9zLnN5bWxpbmsoc3Ry',
'KGQpLCBzdHIoUGF0aCh0KS8ibGsiKSk7IHN5bWxpbmtfZHVvYyA9IFRydWUKICAgICAgICBleGNlcHQgT1NFcnJvciBhcyBl',
'OiBzeW1saW5rX2R1b2MgPSBGYWxzZTsgZ2hpKCJzeW1saW5rX2xvaSIsIGYie3R5cGUoZSkuX19uYW1lX199OiB7ZX0iKQpl',
'eGNlcHQgRXhjZXB0aW9uIGFzIGU6IGdoaSgic3ltbGlua19sb2kiLCBzdHIoZSkpCmdoaSgic3ltbGlua19kdW9jIiwgc3lt',
'bGlua19kdW9jKQppbm4oIiAgQWRtaW5pc3RyYXRvcjoiLCBxdXllbiwgInwgdGFvIHN5bWxpbmsgZHVvYzoiLCBzeW1saW5r',
'X2R1b2MpCgpsb2kgPSBbXQojIENvbmcga2ljaCB0aHVvYyBsYSBwaGVwIGRvIHRyZW4gTElDSCBTVSBHSVQsIGtob25nIGRp',
'bmggZ2kgZGVuIG5lbi4gQ2hvIHBoZXAKIyAtLWNoaS1raWNoLXRodW9jIGNoYXkgbyBtb2kgbmVuIGRlIGNvbiBUVSBLSUVN',
'IGR1b2MgY2hpbmggY29uZyBuYXkgKGRhIGR1bmcKIyBkZSB0YWkgZHVuZyBjYSBoYWkgdmUgY3VhIHN1IGNvIG5lbi1jdSAx',
'OS0wOSkuIE1vaSBjaG90IENIVUMgTkFORyB2YW4gZG9pIFdpbmRvd3MuCmlmIHN5cy5wbGF0Zm9ybSAhPSAid2luMzIiIGFu',
'ZCAiLS1jaGkta2ljaC10aHVvYyIgbm90IGluIHN5cy5hcmd2OgogICAgbG9pLmFwcGVuZChmIktIT05HIHBoYWkgV2luZG93',
'cyAoc3lzLnBsYXRmb3JtPXtzeXMucGxhdGZvcm0hcn0pIikKaWYgbm90IHRlcC5pc19maWxlKCk6ICBsb2kuYXBwZW5kKGYi',
'a2hvbmcgdGhheSB7dGVwfSIpCmlmIG5vdCB0ZXB0LmlzX2ZpbGUoKTogbG9pLmFwcGVuZChmImtob25nIHRoYXkge3RlcHR9',
'IikKaWYgbm90IHNodXRpbC53aGljaCgiZ2l0Iik6IGxvaS5hcHBlbmQoImtob25nIGNvIGBnaXRgIHRyb25nIFBBVEgiKQoK',
'cmMsIGhlYWQsIF8gPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIkhFQUQiKQppZiByYzogbG9pLmFwcGVuZCgia2hvbmcgZG9j',
'IGR1b2MgSEVBRCIpCmdoaSgiaGVhZCIsIGhlYWQpCnJjX2EsIF8sIF8gPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICItLWlz',
'LWFuY2VzdG9yIiwgU0hBX0cxLCBoZWFkIG9yICJIRUFEIikKbGFfaGF1X2R1ZSA9IChyY19hID09IDApCmlmIGhlYWQgPT0g',
'U0hBX0cxOgogICAgdGhlX2hlID0gImcxIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBEQVkgTEEgZzEuIENIVUEg',
'Y28gYmFuIHZhIGcyOyBrZXQgcXVhIGR1b2kgbGEgTkVOIERPLiIpCmVsaWYgbGFfaGF1X2R1ZToKICAgIHRoZV9oZSA9ICJn',
'MiI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gaGF1IGR1ZSBjdWEgZzEgKHtTSEFfRzFbOjhdfSk6IHVuZyB2aWVu',
'IGcyLiIpCmVsc2U6CiAgICB0aGVfaGUgPSAiPyI7IGxvaS5hcHBlbmQoZiJIRUFEPXtoZWFkWzo4XX0gS0hPTkcgcGhhaSBn',
'MSB2YSBLSE9ORyBwaGFpIGhhdSBkdWUgY3VhIHtTSEFfRzFbOjhdfSDigJQgcmViYXNlPyBuaGFtIG5oYW5oPyIpCmdoaSgi',
'dGhlX2hlIiwgdGhlX2hlKQpyY19yLCByZWZzLCBfID0gZ2l0KGdvYywgImZvci1lYWNoLXJlZiIsICItLXBvaW50cy1hdCIs',
'IGhlYWQgb3IgIkhFQUQiLAogICAgICAgICAgICAgICAgICAgICItLWZvcm1hdD0lKHJlZm5hbWU6c2hvcnQpIikKZHNyID0g',
'W3ggZm9yIHggaW4gcmVmcy5zcGxpdGxpbmVzKCkgaWYgeC5zdHJpcCgpIGFuZCB4LnN0cmlwKCkgIT0gImRvLXRhbSJdCmdo',
'aSgicmVmX3Ryb190b2lfaGVhZCIsIGRzcikKaW5uKGYiICByZWYgdHJvIHRvaSBIRUFEOiB7JywgJy5qb2luKGRzcikgaWYg',
'ZHNyIGVsc2UgJyhraG9uZyByZWYgbmFvIC0gSEVBRCByb2kgdHUgZG8pJ30iKQoKaWYgbG9pOgogICAgaW5uKCIiKTsgaW5u',
'KCJLSE9ORyBETyBEVU9DOiBuZW4gZG8gc2FpLCBLSE9ORyBpbiBrZXQgbHVhbiBuYW8uIikKICAgIGZvciB4IGluIGxvaTog',
'aW5uKCIgIC0iLCB4KQogICAgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAxLiBraWNoIHRodW9jIChONycgY3Vh',
'IHNwZWMgcjMpIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIxLiBLSUNIIFRIVU9DIOKA',
'lCB0cmFuIHNwZWMgcjM6IDw9IDIgdGVwIHZhIDw9IDQwMCBkb25nIHRoZW0iKQojIFZFIE5FTiBQSEFJIFRVT0kg4oCUIHZh',
'IHBoYWkgQ0hVTkcgTUlOSCBkdW9jIGxhIHR1b2ksIGtob25nIHBoYWkgZ2lhIGRpbmguCiMgQmFpIGhvYyB0cmEgZ2lhIDE5',
'LTA5LTIwMjY6IGNsb25lIHRhaSBkdW5nIGNoaSBmZXRjaCBuaGFuaCBiYW4gdmEsIGBvcmlnaW4vbWFzdGVyYAojIGR1bmcg',
'eWVuIHR1IDE0LTA5IChjMTZiZDMyLCBzYXUgOTcgY29tbWl0KS4gbWVyZ2UtYmFzZSByb2kgdmUgZHVuZyBkaW5oIG1hc3Rl',
'ciBjdSwKIyBuZW4gZGlmZiBOVU9UIGNhIDk3IGNvbW1pdCBtYXN0ZXI6IGRvIHJhIDQ2IHRlcCAvICs3MTE4IHRoYXkgdmkg',
'MiB0ZXAgLyArMzk3IOKAlAojIENVTkcgTU9UIENPTU1JVCAwZWE5NWRlLiBNb3QgdGlldSBjaGkgREVMVEEgbWEgdmUgbmVu',
'IGtob25nIHR1b2kgdGhpIGtob25nIHNhaQojIGxlY2ggbW90IGNodXQsIG5vIHNhaSBjYSBtb3QgYmFjIGRvIGxvbi4KIyBD',
'aG8gbmVuOiBuZW4ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGxhIHR1b2kgPT4gS0hPTkcgRE8gRFVPQyAocmM9MyksIEtIT05H',
'IHBoYWkgVFJVT1QuCiMgVFJVT1QgbGEgbW90IFBIQU4gUVVZRVQgdmUgYmFuIHZhOyBwaGFuIHF1eWV0IGNoaSBkdW9jIHBo',
'ZXAgcGhhdCByYSBraGkgZGEgZG8gZHVvYy4KcmNfdSwgdXJsX28sIF8gPSBnaXQoZ29jLCAicmVtb3RlIiwgImdldC11cmwi',
'LCAib3JpZ2luIikKdXJsX28gPSBfdXJsX3NhY2godXJsX28pCmdoaSgib3JpZ2luX3VybCIsIHVybF9vKTsgaW5uKGYiICBv',
'cmlnaW4gICAgICAgOiB7dXJsX28gb3IgJyhraG9uZyBkb2MgZHVvYyknfSIpCnVybF9vayA9IChub3QgcmNfdSkgYW5kIHVy',
'bF9vLnJzdHJpcCgiLyIpIGluIFVSTF9LSE9fSE9QX0xFCnJjX2xyLCBvdXRfbHIsIGVyX2xyID0gZ2l0KGdvYywgImxzLXJl',
'bW90ZSIsICJvcmlnaW4iLCAicmVmcy9oZWFkcy9tYXN0ZXIiKSBpZiB1cmxfb2sgZWxzZSAoMSwgIiIsICIiKQpyY19sbSwg',
'bG0sIGVyX2xtICAgICA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAib3JpZ2luL21hc3RlciIpCnJtID0gb3V0X2xyLnNwbGl0',
'KClbMF0gaWYgKG5vdCByY19sciBhbmQgb3V0X2xyLnN0cmlwKCkpIGVsc2UgIiIKaWYgbm90IHVybF9vazoKICAgIGtldCgi',
'TjcnIGtpY2ggdGh1b2MiLCBLREQsIGYib3JpZ2luPXt1cmxfbyFyfSBLSE9ORyBwaGFpIGtobyB0aGF0IOKAlCAndHVvaScg',
'c28gdm9pIG5vIGtob25nIGNodW5nIG1pbmggZHVvYyBnaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwg',
'MQplbGlmIG5vdCBybToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJraG9uZyBob2kgZHVvYyBt',
'YXN0ZXIgdHJlbiByZW1vdGUgKGxzLXJlbW90ZSByYz17cmNfbHJ9KToge2VyX2xyWzo2MF19ICIKICAgICAgICBmIuKAlCBr',
'aG9uZyBjaHVuZyBtaW5oIGR1b2MgdmUgbmVuIGNvbiB0dW9pIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIi',
'LCAxCmVsaWYgcmNfbG0gb3Igbm90IGxtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyBkb2MgZHVv',
'YyBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25lOiB7ZXJfbG1bOjYwXX0iKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAi',
'IiwgIiIsIDEKZWxpZiBsbSAhPSBybToKICAgICMgRGVtIHhlbSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRlbSBkdW9jIOKAlCBj',
'b24gc28gbmF5IG5vaSBybyBtdWMgZG8gc2FpIGxlY2guCiAgICByY19jLCBzYXUsIF8gPSBnaXQoZ29jLCAicmV2LWxpc3Qi',
'LCAiLS1jb3VudCIsIGYie2xtfS4ue3JtfSIpCiAgICB4YSA9IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1pdCIgaWYgKG5vdCBy',
'Y19jIGFuZCBzYXUuc3RyaXAoKS5pc2RpZ2l0KCkpIGVsc2UgIiIKICAgIGlubihmIiAgb3JpZ2luL21hc3RlciB0cm9uZyBj',
'bG9uZSA6IHtsbVs6MTJdfSIpCiAgICBpbm4oZiIgIG1hc3RlciB0cmVuIHJlbW90ZSAgICAgICAgOiB7cm1bOjEyXX17eGF9',
'IikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIGtldCgiTjcnIGtp',
'Y2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJ2ZSBuZW4gQ1U6IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19ICE9IHJlbW90ZT17',
'cm1bOjEyXX17eGF9ICIKICAgICAgICBmIuKAlCBjaGF5IGBnaXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2luIG1hc3RlcmAgcm9p',
'IGRvIGxhaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbHNlOgogICAgaW5uKGYiICB2ZSBuZW4g',
'VFVPSTogb3JpZ2luL21hc3RlciA9IHtsbVs6MTJdfSA9PSBtYXN0ZXIgdHJlbiByZW1vdGUiKQogICAgZ2hpKCJtYXN0ZXJf',
'Y2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAgcmNfbWIsIG1iLCBlcl9tYiA9IGdpdChnb2MsICJt',
'ZXJnZS1iYXNlIiwgIm9yaWdpbi9tYXN0ZXIiLCBoZWFkKQppZiByY19tYiBvciBub3QgbWI6CiAgICBpZiBtYiA9PSAiIiBh',
'bmQgcm0gYW5kIGxtID09IHJtOgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9j',
'IG1lcmdlLWJhc2Ugdm9pIG9yaWdpbi9tYXN0ZXI6IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgog',
'ICAgZ2hpKCJtZXJnZV9iYXNlIiwgbWIpCiAgICBpbm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7',
'bWJbOjEyXX0iKQogICAgaWYgbWIgIT0gU0hBX0JBU0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2Ug',
'bWEgc3BlYyByMyBraGFpICh7U0hBX0JBU0VfU1BFQ1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQog',
'ICAgICAgIGlubigiICAgICAgICAgRG8gc28gYmFzZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcgdmFvLiBEdW5nIG1l',
'cmdlLWJhc2UgbW9pIGxhIHZpZWMgY3VhIGV4ZWN1dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJk',
'aWZmIiwgIi0tbnVtc3RhdCIsIFNIQV9CQVNFX1NQRUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAgICAgICAgICAg',
'IGggPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBuc194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICAgICAgICAg',
'IGEgPSBzdW0oaW50KHhbMF0pIGZvciB4IGluIGggaWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdoaSgibnVtc3Rh',
'dF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVwIjogbGVuKGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBpbm4oZiIgICAgICAg',
'ICAoZG9pIGNoaWV1OiBzbyBiYXNlIHNwZWMgPSB7bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkgS0hPTkcgZHVu',
'ZyBkZSBjaGFtKSIpCiAgICByYywgbnMsIGVyID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgbWIsIGhlYWQpCmlm',
'IHJjOgogICAgcGFzcwplbHNlOgogICAgaGFuZyA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGluZXMoKSBp',
'ZiBsLnN0cmlwKCldCiAgICB0aGVtID0gc3VtKGludChoWzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdpdCgpKQog',
'ICAgeG9hICA9IHN1bShpbnQoaFsxXSkgZm9yIGggaW4gaGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgic29fdGVw',
'IiwgbGVuKGhhbmcpKTsgZ2hpKCJkb25nX3RoZW0iLCB0aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZvciBoIGlu',
'IGhhbmc6IGlubihmIiAgICB7aFsyXTozNH0gK3toWzBdOjw1fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05HOiB7bGVu',
'KGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17eG9hfSAgICh0cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcg',
'dGhlbSkiKQogICAgY2hhbSA9IHNvcnRlZCh7aFsyXSBmb3IgaCBpbiBoYW5nfSAmIFdSSVRFX1NFVF9HMik7IGdoaSgiY2hh',
'bV93cml0ZV9zZXQiLCBjaGFtKQogICAgZGVmIF9jYV9tb2lfY28ocmV2KToKICAgICAgICByXywgbmRfLCBfID0gZ2l0KGdv',
'YywgInNob3ciLCBmIntyZXZ9Om9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIHJldHVybiBOb25lIGlmIHJf',
'IGVsc2Uge3QgZm9yIHQgaW4gQ0FfTU9JX0cyIGlmIHJlLnNlYXJjaChyIig/bSleZGVmICIgKyB0ICsgciJbYS16XT9fIiwg',
'bmRfKX0KICAgIG9fbWIsIG9faCA9IF9jYV9tb2lfY28obWIpLCBfY2FfbW9pX2NvKGhlYWQpCiAgICBtYW5nID0gc29ydGVk',
'KG9faCAtIG9fbWIsIGtleT1zb19jYSkgaWYgKG9fbWIgaXMgbm90IE5vbmUgYW5kIG9faCBpcyBub3QgTm9uZSkgZWxzZSBO',
'b25lCiAgICBnaGkoImNhX21vaV9nMl9tYW5nX3ZhbyIsIG1hbmcpCiAgICBpZiBub3QgbWFuZzoKICAgICAgICAjIERvIFJP',
'TkcgKGRhIGxhbmQsIGNoaW5oIG1hc3RlciksIG5oYW0gbmhhbmgsIGhheSBuaGFuaCBjdWEgcGFja2V0IEtIQUMgY2hhbSBj',
'dW5nIHRlcDoKICAgICAgICAjIGtob25nIG1hbmcgY2EgbW9pIG5hbyBjdWEgZzIgdGhpIGtob25nIHBoYWkgdW5nIHZpZW4u',
'IERvYyBraG9uZyBkdW9jIChOb25lKSBjdW5nIHZheS4KICAgICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImRv',
'aSB0dW9uZyBraG9uZyBwaGFpIHVuZyB2aWVuOiB7bGVuKGhhbmcpfSB0ZXAsIGNoYW0ge2NoYW19LCBjYSBtb2kgIgogICAg',
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiZzIgbWFuZyB2YW8ge21hbmchcn0g4oCUIGRhIGxhbmQ/IG5oYW0g',
'bmhhbmg/IHBhY2tldCBraGFjPyIpCiAgICBlbHNlOgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBEQVQgaWYgKGxl',
'bihoYW5nKSA8PSBUUkFOX1RFUCBhbmQgdGhlbSA8PSBUUkFOX0RPTkcpIGVsc2UgVFJVT1QsCiAgICAgICAgICAgIGYie2xl',
'bihoYW5nKX0gdGVwIC8gK3t0aGVtfSIpCgojIENvbmcgbmhhbmg6IGRvIFJJRU5HIGtpY2ggdGh1b2MgKHZhaSBnaWF5KSBy',
'b2kgZHVuZy4gRHVuZyBraGkgY2FuIHhhYyBtaW5oIGxhaQojIHZlIG5lbiBtYSBraG9uZyBtdW9uIHRyYSAyMC00NSBwaHV0',
'IGNobyBjYSBibyB0ZXN0LgppZiAiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Y6CiAgICBpbm4oIiIpOyBpbm4oIj0i',
'ICogNzgpCiAgICBpbm4oIi0tY2hpLWtpY2gtdGh1b2M6IENISSBkbyBjb25nIGtpY2ggdGh1b2MuIERheSBLSE9ORyBwaGFp',
'IG1vdCBsdW90IG5naGllbSB0aHUuIikKICAgIGlubigiLSIgKiA3OCkKICAgIGZvciBfdCwgX3R0LCBfY3QgaW4gY2hvdDog',
'aW5uKGYiICB7X3R0OjE0fSB7X3R9IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICBfayA9IHN1bSgxIGZv',
'ciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCiAgICBfciA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9',
'PSBUUlVPVCkKICAgIHN5cy5leGl0KDMgaWYgX2sgZWxzZSAoMSBpZiBfciBlbHNlIDApKQoKQ0hJX1BST0JFID0gIi0tY2hp',
'LXByb2JlIiBpbiBzeXMuYXJndiAgICAjIGJvIHF1YSBibyB0ZXN0ICsgTjc7IGdpdSAwLCAxLCAzCiMgLS0tLS0tLS0tLS0t',
'LS0tLSAyLiBibyB0ZXN0IGRheSBkdSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4oIiIpOyBp',
'bm4oIi0iICogNzgpOyBpbm4oIjIuIEJPIFRFU1QgREFZIERVICgxMC00MCBwaHV0KSIpCiAgICByY19uLCBvdXRfbiA9IGNo',
'YXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIGdvYykKICAgIGdoaSgicmNfc3VpdGUiLCByY19uKQogICAgbSA9',
'IFJYX1RPTkcuc2VhcmNoKG91dF9uKQogICAgaW5uKCIgIHJjID0iLCByY19uLCAifCIsIG0uZ3JvdXAoMCkgaWYgbSBlbHNl',
'ICIoS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCkiKQogICAgaWYgbToKICAgICAgICBnaGkoImRhdCIsIGludChtLmdy',
'b3VwKDEpKSk7IGdoaSgidHJlbiIsIGludChtLmdyb3VwKDIpKSk7IGdoaSgiYm9fcXVhX3NvIiwgaW50KG0uZ3JvdXAoNCkp',
'KQogICAgZG9faGV0LCBnYywgdGluID0gZG9jX2RvKG91dF9uKQogICAgZ2hpKCJzb19jYV9kbyIsIGxlbihkb19oZXQpKTsg',
'Z2hpKCJsaWV0X2tlX2RheV9kdSIsIHRpbikKICAgIGZvciBnIGluIGdjOiBpbm4oIiAgICoiLCBnKQogICAgaW5uKCIiKTsg',
'aW5uKGYiICA9PT0ge2xlbihkb19oZXQpfSBDQSBETyA9PT0iKQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNv',
'X2NhKToKICAgICAgICBpbm4oZiIgICB7dC5zcGxpdCgnXycpWzBdOjd9IHt0fSIpOyBpbm4oZiIgICAgICAgICAgIHtkb19o',
'ZXRbdF1bOjE1MF19IikKICAgIGdoaSgiZG9fbHlfZG8iLCB7dDogZG9faGV0W3RdWzozMDBdIGZvciB0IGluIGRvX2hldH0p',
'CiAgICAjIC0tLS0gQ0hPVDogbW9pIGNhIERPIHBoYWkgR0lBSSBUSElDSCBEVU9DIC0tLS0KICAgICMgVGhpZXUgY2hvdCBu',
'YXksIGJvIGRvIGluIGRhbmggc2FjaCBkbyByb2kgdmFuIHRob2F0IHJjPTAuIERvIGR1bmcgbGEgbG9pIGRhIHhheSByYToK',
'ICAgICMgbHVvdCBXaW5kb3dzIDE5LTA5IGNvIHQxNzEgRE8gbWEgYm8gZG8gYmFvICJEQVQgMTAgfCBUUlVPVCAwIiB2YSBy',
'Yz0wLgogICAgZGVmIF9raG9hKHQpOiByZXR1cm4gdC5zcGxpdCgiXyIpWzBdCiAgICBkb19wYWNrZXQsIGRvX2xhLCBkb190',
'aGlldV9jb25nX2N1ID0gW10sIFtdLCBbXQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAg',
'ICBrLCBseSA9IF9raG9hKHQpLCBkb19oZXRbdF0KICAgICAgICBpZiBrIGluIENBX1BBQ0tFVDogICAgICAgICAgICAgICAg',
'ICAgICAgICAgICAgICBkb19wYWNrZXQuYXBwZW5kKHQpCiAgICAgICAgZWxpZiAiS0jDlE5HIMSQTyDEkMav4buiQyIgaW4g',
'bHkgb3IgInRoaeG6v3UgYCIgaW4gbHk6ICBkb190aGlldV9jb25nX2N1LmFwcGVuZCh0KQogICAgICAgIGVsaWYgayBpbiBO',
'R09BSV9QSEFNX1ZJOiAgICAgICAgICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICBlbHNlOiAgICAgICAgICAgICAgICAg',
'ICAgICAgICAgICAgICAgICAgICAgICAgICBkb19sYS5hcHBlbmQodCkKICAgIGdoaSgiZG9fcGFja2V0IiwgZG9fcGFja2V0',
'KTsgZ2hpKCJkb19sYSIsIGRvX2xhKTsgZ2hpKCJkb190aGlldV9jb25nX2N1IiwgZG9fdGhpZXVfY29uZ19jdSkKICAgIGlu',
'bigiIikKICAgIGlubihmIiAgY2EgRE8gdGh1b2MgQ0hJTkggcGFja2V0IG5heSA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9f',
'cGFja2V0XSBvciAna2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERPIG5nb2FpIHBoYW0gdmkgKHIzIGtoYWkpOiB7W19r',
'aG9hKHgpIGZvciB4IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSkgaWYgX2tob2EoeCkgaW4gTkdPQUlfUEhBTV9WSV19',
'IikKICAgIGlubihmIiAgY2EgRE8gdmkgVEhJRVUgQ09ORyBDVSAgICAgICA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhp',
'ZXVfY29uZ19jdV0gb3IgJ2tob25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBMQSAoa2hvbmcgZ2lhaSB0aGljaCBkdW9j',
'KToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV0gb3IgJ2tob25nIGNvJ30iKQogICAgIyAtLS0tIENIT1Q6IHBoZXAgZG8g',
'cGhhaSBUUk9OIHRydW9jIGtoaSBtb3QgY2h1IERBVCBuYW8gZHVvYyBwaGF0IC0tLS0KICAgICMgQmFuIHRydW9jIGNoaSBJ',
'TiBgdGluYC9gcmNfc3VpdGVgOiBibyB0ZXN0IGNoZXQgZ2l1YSB0MTcxIChyYz0xMzQsIGtob25nIGRvbmcgdG9uZykKICAg',
'ICMgdmFuIHJhICJEQVQgMTIgfCBUUlVPVCAwIiByYz0wOyBjYSBQQUNLRVQgdmFuZyBtYXQgaGF5IGJpIEJPIFFVQSBjdW5n',
'IGR1b2MgY2hhbSBuaHUKICAgICMgImtob25nIGRvIi4gVmFuZyBtYXQga2hvbmcgcGhhaSAia2hvbmcgZG8iIOKAlCBsYSBL',
'SE9ORyBETyBEVU9DLgogICAgdmFuZyA9IFt0IGZvciB0IGluIHNvcnRlZChDQV9QQUNLRVQsIGtleT1zb19jYSkgaWYgbWF1',
'X2NhKG91dF9uLCB0KSBub3QgaW4gKCJRVUEiLCAiRE8iKV0KICAgIGx5X2tkZCA9IFtdCiAgICBpZiBub3QgdGluOiBseV9r',
'ZGQuYXBwZW5kKCJkYW5oIHNhY2ggZG8gS0hPTkcgZGF5IGR1IikKICAgIGlmIHJjX24gbm90IGluICgwLCAxKSBvciAocmNf',
'biA9PSAxKSAhPSBib29sKGRvX2hldCk6CiAgICAgICAgbHlfa2RkLmFwcGVuZChmInJjIGJvIHRlc3Q9e3JjX259IGtob25n',
'IGtob3Age2xlbihkb19oZXQpfSBjYSBETyBkb2MgZHVvYyIpCiAgICBpZiB2YW5nOiBseV9rZGQuYXBwZW5kKGYiY2EgUEFD',
'S0VUIHZhbmcvYm8gcXVhOiB7dmFuZ30iKQogICAgZ2hpKCJjYV9wYWNrZXRfdmFuZyIsIHZhbmcpOyBnaGkoImx5X2RvX2No',
'dWFfdHJvbiIsIGx5X2tkZCkKICAgIGlmIGx5X2tkZDoga2V0KCJCbyB0ZXN0IGNoYXkgVFJPTiB2YSBkb2MgRFUiLCBLREQs',
'ICI7ICIuam9pbihseV9rZGQpKQogICAgY2h1YV90cm9uID0gS0REIGlmIGx5X2tkZCBlbHNlIERBVAogICAga2V0KCJLaG9u',
'ZyBjYSBuYW8gY3VhIFBBQ0tFVCBiaSBETyIsIGNodWFfdHJvbiBpZiBub3QgZG9fcGFja2V0IGVsc2UgVFJVT1QsCiAgICAg',
'ICAgIiIgaWYgbm90IGRvX3BhY2tldCBlbHNlIGYiRE86IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XX0g4oCUIGJh',
'biB2YSBDSFVBIHhvbmciKQogICAga2V0KCJNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIsIGNodWFfdHJvbiBpZiBu',
'b3QgZG9fbGEgZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9fbGEgZWxzZSBmImxhOiB7W19raG9hKHgpIGZvciB4',
'IGluIGRvX2xhXX0iKQogICAgaWYgZG9fdGhpZXVfY29uZ19jdToKICAgICAgICBrZXQoIkNvbmcgY3UgZGF5IGR1IGRlIGRv',
'IiwgS0RELCBmInRoaWV1IGNvbmcgY3UgY2hvIHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV19IikKCiAg',
'ICBicSA9IHNvcnRlZCh7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXRfbil9LCBrZXk9c29fY2EpOyBnaGko',
'ImNhX2JvX3F1YSIsIGJxKQogICAgaW5uKCIiKTsgaW5uKGYiICBCTyBRVUEgKHtsZW4oYnEpfSk6IHtbeC5zcGxpdCgnXycp',
'WzBdIGZvciB4IGluIGJxXX0iKQoKICAgIGlubigiIik7IGlubigiICBOMS1ONCAodDE2NS10MTY4KSwgdGlldSBjaGkgbmdo',
'aWVtIHRodSBjdWEgcjIsIG5heSBsYSBjaGkgYmFvIGhvaSBxdXk6IikKICAgIGI0ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkg',
'Zm9yIHQgaW4gQ0FNT0l9OyBnaGkoImNhX21vaSIsIGI0KQogICAgZm9yIHQgaW4gQ0FNT0k6IGlubihmIiAgICAge3R9OiB7',
'YjRbdF19IikKICAgICMgQk9fUVVBL3ZhbmcgbGEgQ0hVQSBDSEFZLCBraG9uZyBwaGFpIERPOiBjaGkgbW90IGNhIERPIG1v',
'aSBkdW9jIHBoYXQgVFJVT1QuCiAgICBrZXQoIk4xLU40ICh0MTY1LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJRVUEiIGZv',
'ciB2IGluIGI0LnZhbHVlcygpKQogICAgICAgIGVsc2UgKFRSVU9UIGlmIGFueSh2ID09ICJETyIgZm9yIHYgaW4gYjQudmFs',
'dWVzKCkpIGVsc2UgS0REKSwgc3RyKGI0KSkKCiAgICBpbm4oIiIpOyBpbm4oIiAgMTUgY2EgdHVuZyBkbyB0cmVuIENJOiIp',
'CiAgICBiMTUgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQogICAgaW5u',
'KCIgICAgIiArICIgICIuam9pbihmInt0fTp7YjE1W3RdfSIgZm9yIHQgaW4gQ0ExNSkpCgogICAgIyB0MTM2IOKAlCBOMTIg',
'ZG8gR0lBTiBUSUVQIHF1YSBrZXQgcXVhIGNhCiAgICB0MTM2X3RlbiA9IG5leHQoKHQgZm9yIHQgaW4gZG9faGV0IGlmIHQu',
'c3RhcnRzd2l0aCgidDEzNiIpKSwgTm9uZSkKICAgIGlmIGIxNS5nZXQoInQxMzYiKSA9PSAiUVVBIjoKICAgICAgICBrZXQo',
'Ik4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBEQVQsICJ0MTM2IFFVQSIpCiAgICBlbGlmIGIxNS5nZXQoInQxMzYiKSAh',
'PSAiRE8iOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIEtERCwgZiJ0MTM2ID0ge2IxNS5nZXQo',
'J3QxMzYnKSFyfSDigJQga2hvbmcgY2hheS9raG9uZyB0aGF5IikKICAgIGVsc2U6CiAgICAgICAgbHkgPSBkb19oZXQuZ2V0',
'KHQxMzZfdGVuLCAiIikKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBUUlVPVCwgZiJETzoge2x5',
'Wzo5MF19IikKCiMgLS0tLS0tLS0tLS0tLS0tLSAzLiBwcm9iZSBUSEFORyB2YW8gaGFtIC0tLS0tLS0tLS0tLS0tLS0KaW5u',
'KCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIzLiBQUk9CRSBUSEFORyDigJQgZ29pIF9naXRfd2luZG93cyB2b2kgdGhhbSBz',
'byB0aWVtIikKc3BlYyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscDU0MSIsIHN0cih0ZXAp',
'KQpscCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9kdWxlKGxw',
'KQpzaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShscC5fZ2l0X3dpbmRvd3MpCmdoaSgidGhhbV9zb19fZ2l0X3dpbmRvd3MiLCBs',
'aXN0KHNpZy5wYXJhbWV0ZXJzKSkKaW5uKCIgIHRoYW0gc28gY3VhIF9naXRfd2luZG93czoiLCBsaXN0KHNpZy5wYXJhbWV0',
'ZXJzKSkKCmRlZiBnb2koKiprdyk6CiAgICAiIiJHb2kgX2dpdF93aW5kb3dzLCBCQVQgc3RkZXJyIGRlIG1vdCBkb25nIGNo',
'YW4gZG9hbiBraG9uZyBnaWV0IGx1b3QgZG8uIiIiCiAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgd2l0aCBjb250ZXh0bGli',
'LnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICByID0gbHAuX2dpdF93aW5kb3dzKCoqa3cpCiAgICByZXR1cm4gciwgZS5n',
'ZXR2YWx1ZSgpCgojIC0tLSBkb2kgY2h1bmcgcmlnOiBwaGFpIHRyYSBsb2kgZHVuZyBtb3QgY2EgdGEgQklFVCBUUlVPQyBk',
'YXAgYW4gLS0tCndpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgIG5nb2FpID0gUGF0aCh0KS8i',
'bmdvYWkiOyBuZ29haS5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYi',
'OyBwZi5ta2RpcigpCiAgICAobmdvYWkvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAg',
'IHIxLCBfID0gZ29pKHBhdGg9c3RyKG5nb2FpKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIChj',
'dy8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjIsIF8gPSBnb2kocGF0aD1zdHIo',
'Y3cpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQpyaWdfb2sgPSBib29sKHIxKSBhbmQgcjIgaXMgTm9u',
'ZQpnaGkoInJpZ19kb2lfY2h1bmciLCByaWdfb2spCmtldCgiUklHIGRvaSBjaHVuZyAoYmlldCB0cnVvYyBkYXAgYW4pIiwg',
'REFUIGlmIHJpZ19vayBlbHNlIEtERCwKICAgIGYibmdvYWktY3dkLT57J05IQU4nIGlmIHIxIGVsc2UgJ05vbmUnfSB8IHRy',
'b25nLWN3ZC0+eydOSEFOJyBpZiByMiBlbHNlICdOb25lJ30iKQppZiBub3QgcmlnX29rOgogICAgaW5uKCIiKTsgaW5uKCJL',
'SE9ORyBETyBEVU9DOiByaWcgc2FpLCBtb2kgY2hvdCBkdW9pIHNlIHZvIG5naGlhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0g',
'TU9JIENPTkcgUEhBSSBUVSBDSFVORyBNSU5IIE5PIENPIFRIRSBETyAtLS0KIyBCYWkgaG9jIGRhdCBuaGF0IGN1YSBwYWNr',
'ZXQgbmF5OiBkb19uMTAgYmFuIGN1IGNoYW0gREFUIGNobyA5NTgzMTY4NSB0cm9uZyBraGkgdDE3MQojIGN1YSBjaGluaCBi',
'YW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQgdGF0IG1hIE4xMCBzaW5oIHJhIGRlIGJhdC4gTm8gZGVnZW5lcmF0ZSDigJQK',
'IyB0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgbmVuICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIGN1',
'bmcga2V0IHF1YS4KIyBNb3QgY29uZyBraG9uZyB0aGUgRE8gdGhpIGtob25nIHBoYWkgY29uZywgdmEgbm8gbmd1eSBoaWVt',
'IGhvbiBraG9uZyBjbyBjb25nOiBubwojIHBoYXQgcmEgbW90IGNodSBEQVQuCiMKIyBOZW4gdHJ1b2Mga2hpIERVTkcgbmFt',
'IGNvbmcgbmF5IGRlIHBoYW4gcXV5ZXQsIGJhdCB0dW5nIGNvbmcgZ2lldCBtb3QgZG90IGJpZW4gZGEKIyBiaWV0IHRyb25n',
'LiBDb25nIG5hbyBraG9uZyBnaWV0IGR1b2MgdGhpIGNodSBEQVQgY3VhIG5vIGJpIEhBIHh1b25nIEtIT05HIERPIERVT0M7',
'CiMgVFJVT1QgZ2l1IG5ndXllbiAocXVhbiBzYXQgdHJ1YyB0aWVwLCB2ZC4gZzEgdmFuIG5oYW4gZ2l0LmJhdCkuIERvdCBi',
'aWVuIGNoYXkgdHJlbiBCQU4gU0FPIFRBTTsgY2F5IHRoYXQga2hvbmcgYmkKIyBkdW5nIHRvaSAoY3VuZyBreSBsdWF0IG5o',
'dSBONykuCkRPVF9CSUVOX1RVX0tJRU0gPSBbCiAgICAoIk44IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAnaWYg',
'Y2hpX2RpbmggYW5kIFBhdGgoY2hpX2RpbmgpLm5hbWUubG93ZXIoKSA9PSAiZ2l0LmV4ZSIgYW5kIGhvcF9sZShjaGlfZGlu',
'aCk6JywKICAgICAiaWYgY2hpX2RpbmggYW5kIGhvcF9sZShjaGlfZGluaCk6IiksCiAgICAoIk45IiwgIm9wcy9sZWFzZV9w',
'dWJsaXNoLnB5IiwKICAgICAiZCA9IGRfcmF3LnN0cmlwKCkuc3RyaXAoJ1wiJykiLCAiZCA9IGRfcmF3LnN0cmlwKCkiKSwK',
'ICAgICgiTjEwIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAic2VwID0gb3MucGF0aHNlcCBpZiBwaGFuX2NhY2gg',
'aXMgTm9uZSBlbHNlIHBoYW5fY2FjaCIsICJzZXAgPSBvcy5wYXRoc2VwIiksCiAgICAoIk4xMSIsICJvcHMvbGVhc2VfcHVi',
'bGlzaC5weSIsICJpZiBjaGFuX2RvYW4gaXMgbm90IE5vbmU6IiwgImlmIEZhbHNlOiIpLAogICAgKCJOMTIiLCAib3BzL2xl',
'YXNlX3B1Ymxpc2hfdGVzdC5weSIsCiAgICAgJ2dpdF9wYXRoPSIvL2tob25nLWNvL2dpdCInLCAnZ2l0X3BhdGg9Ii9raG9u',
'Zy1jby9naXQiJyksCl0KaW5uKCIiKTsgaW5uKCIgIHR1IGtpZW0gY29uZyDigJQgbW9pIGNvbmcgcGhhaSBnaWV0IGR1b2Mg',
'bW90IGRvdCBiaWVuIGRhIGJpZXQ6IikKZ2lldCA9IHt9CmZvciBtYSwgZHVvbmcsIHRpbSwgdGhheSBpbiBET1RfQklFTl9U',
'VV9LSUVNOgogICAgX3RlbiwgX2hhbSA9IG5leHQoKChhLCBiKSBmb3IgYSwgYiBpbiBQUk9CRSBpZiBhLnN0YXJ0c3dpdGgo',
'bWEgKyAiICIpKSwgKE5vbmUsIE5vbmUpKQogICAgaWYgX2hhbSBpcyBOb25lOgogICAgICAgIGdpZXRbbWFdID0gTm9uZTsg',
'aW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBraG9uZyB0aW0gdGhheSBwcm9iZSB0ZW4gJ3ttYX0gLi4uJyIpOyBj',
'b250aW51ZQogICAgdHJ5OgogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgX3Q6CiAgICAg',
'ICAgICAgIF9jID0gUGF0aChfdCkvImNheSI7IHNodXRpbC5jb3B5dHJlZShnb2MvIm9wcyIsIF9jLyJvcHMiKQogICAgICAg',
'ICAgICBfZiA9IF9jL2R1b25nOyBfbmQgPSBfZi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgaWYg',
'X25kLmNvdW50KHRpbSkgIT0gMToKICAgICAgICAgICAgICAgIGdpZXRbbWFdID0gTm9uZQogICAgICAgICAgICAgICAgaW5u',
'KGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBtYXUgZG90IGJpZW4ga2hvcCB7X25kLmNvdW50KHRpbSl9IGxhbiAobW9u',
'ZyAxKSIKICAgICAgICAgICAgICAgICAgICBmIiDigJQgbWEgbmd1b24gZGEgZG9pLCBkb3QgYmllbiBuYXkgaGV0IHkgbmdo',
'aWEiKTsgY29udGludWUKICAgICAgICAgICAgX2Yud3JpdGVfdGV4dChfbmQucmVwbGFjZSh0aW0sIHRoYXksIDEpLCBlbmNv',
'ZGluZz0idXRmLTgiKQogICAgICAgICAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigi',
'bHBfZGJfIiArIG1hLCBzdHIoX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgICAgICAgICAgX20gPSBpbXBvcnRs',
'aWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX20pCiAgICAgICAgICAgIGRl',
'ZiBfZ29pX2RiKCoqa3cpOgogICAgICAgICAgICAgICAgX2UgPSBpby5TdHJpbmdJTygpCiAgICAgICAgICAgICAgICB3aXRo',
'IGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKF9lKToKICAgICAgICAgICAgICAgICAgICByZXR1cm4gX20uX2dpdF93aW5k',
'b3dzKCoqa3cpLCBfZS5nZXR2YWx1ZSgpCiAgICAgICAgICAgIF90dCwgX2N0LCBfID0gX2hhbShfZ29pX2RiLCBpbnNwZWN0',
'LnNpZ25hdHVyZShfbS5fZ2l0X3dpbmRvd3MpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgX2MvIm9wcyIvImxl',
'YXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgZ2lldFttYV0gPSAoX3R0ID09IFRSVU9UKQogICAgICAgIGlubihmIiAg',
'ICB7bWE6NH0gZG90IGJpZW4gLT4ge190dDoxNH0geydHSUVUIERVT0MnIGlmIF90dCA9PSBUUlVPVCBlbHNlICdTT05HIFNP',
'VCd9IgogICAgICAgICAgICArIChmIiAgICh7X2N0fSkiIGlmIF9jdCBlbHNlICIiKSkKICAgIGV4Y2VwdCBFeGNlcHRpb24g',
'YXMgX2U6CiAgICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IHt0eXBlKF9l',
'KS5fX25hbWVfX306IHtfZX0iKQpnaGkoImNvbmdfZ2lldF9kdW9jX2RvdF9iaWVuIiwgZ2lldCkKCmZvciB0ZW4sICh0dCwg',
'Y3QsIGRsKSBpbiBbKHQsIGYoZ29pLCBzaWcsIHRlcHQpKSBmb3IgdCwgZiBpbiBQUk9CRV06CiAgICBnaGkoInByb2JlXyIg',
'KyB0ZW4uc3BsaXQoKVswXS5sb3dlcigpLCBkbCkKICAgIGlmIGlzaW5zdGFuY2UoZGwsIGRpY3QpOgogICAgICAgIGZvciBr',
'LCB2IGluIGRsLml0ZW1zKCk6IGlubihmIiAgICB7azozNH06IHt2fSIpCiAgICBtYSA9IHRlbi5zcGxpdCgpWzBdCiAgICBp',
'ZiBnaWV0LmdldChtYSkgaXMgbm90IFRydWUgYW5kIHR0ID09IERBVDoKICAgICAgICAjIERBVCB0dSBtb3QgY29uZyBjaHVh',
'IGNodW5nIG1pbmggZHVvYyBsYSBiaWV0IERPIHRoaSBraG9uZyBkYW5nIHRpbiBob24gS0RELgogICAgICAgIGtldCh0ZW4s',
'IEtERCwgZiJjb25nIEtIT05HIGdpZXQgZHVvYyBkb3QgYmllbiBjdWEgY2hpbmggbm8gKHtnaWV0LmdldChtYSkhcn0pIgog',
'ICAgICAgICAgICAgICAgICAgICAgZiIgLT4gY2h1IERBVCBuYXkga2hvbmcgY28gZ2lhIHRyaSIpCiAgICBlbHNlOgogICAg',
'ICAgIGtldCh0ZW4sIHR0LCBjdCkKCiMgLS0tLS0tLS0tLS0tLS0tLSA0LiBONyBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFN',
'IC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiNC4g',
'Tjcg4oCUIGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gKGNheSB0aGF0IEtIT05HIGJpIGR1bmcgdG9pKSIpCiAgICB0cnVv',
'YyA9IHRlcC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTikKICAgIGdoaSgibjdfdHJ1b2MiLCB0',
'cnVvYyk7IGlubihmIiAgc28gZG9uZyBraG9wIHtNQVVfV0lOIXJ9OiBUUlVPQyA9IHt0cnVvY30gW21vbmcgMV0iKQogICAg',
'aWYgdHJ1b2MgIT0gMToKICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsIGYibWF1IHh1YXQg',
'aGllbiB7dHJ1b2N9IGxhbiwga2hvbmcgcGhhaSAxIikKICAgIGVsc2U6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3Jh',
'cnlEaXJlY3RvcnkoKSBhcyB0bXA6CiAgICAgICAgICAgIHNhbyA9IFBhdGgodG1wKS8iY2F5IgogICAgICAgICAgICBzaHV0',
'aWwuY29weXRyZWUoZ29jLCBzYW8sIGlnbm9yZT1zaHV0aWwuaWdub3JlX3BhdHRlcm5zKCIuZ2l0IiwgIl9fcHljYWNoZV9f',
'IiwgIioucHljIikpCiAgICAgICAgICAgIGYyID0gc2FvLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IgogICAgICAgICAgICBm',
'Mi53cml0ZV90ZXh0KGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5yZXBsYWNlKE1BVV9XSU4sICJpZiBGYWxzZToi',
'KSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgc2F1ID0gZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNv',
'dW50KE1BVV9XSU4pOyBnaGkoIm43X3NhdSIsIHNhdSkKICAgICAgICAgICAgaW5uKGYiICBTQVUgKGRhIGRvdCBiaWVuKSA9',
'IHtzYXV9IFttb25nIDBdIikKICAgICAgICAgICAgaWYgc2F1ICE9IDA6CiAgICAgICAgICAgICAgICBrZXQoIk43IGRvdCBi',
'aWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsICJkb3QgYmllbiBLSE9ORyBhcCBkdW9jIikKICAgICAgICAgICAgZWxzZToKICAg',
'ICAgICAgICAgICAgIHJjX20sIG91dF9tID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgc2FvKQogICAg',
'ICAgICAgICAgICAgbTE2NSA9IG1hdV9jYShvdXRfbSwgInQxNjUiKTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20pCiAgICAg',
'ICAgICAgICAgICB0ZW4xNjUgPSBuZXh0KCh0IGZvciB0IGluIGRtIGlmIHQuc3RhcnRzd2l0aCgidDE2NSIpKSwgTm9uZSkK',
'ICAgICAgICAgICAgICAgIGx5ID0gKGRtLmdldCh0ZW4xNjUpIG9yICIiKQogICAgICAgICAgICAgICAgZ2hpKCJuN190MTY1',
'IiwgbTE2NSk7IGdoaSgibjdfbHlfZG8iLCBseVs6MjAwXSkKICAgICAgICAgICAgICAgIGlubihmIiAgdDE2NSBzYXUgZG90',
'IGJpZW46IHttMTY1fSB8IHtseVs6MTEwXX0iKQogICAgICAgICAgICAgICAgZHVuZ19seV9kbyA9ICJQQVRIIHQiIGluIGx5',
'IG9yICIvdXNyL2JpbiIgaW4gbHkKICAgICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIERB',
'VCBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKSBlbHNlCiAgICAgICAgICAgICAgICAgICAgKFRSVU9UIGlmIG0x',
'NjUgPT0gIkRPIiBlbHNlIEtERCksCiAgICAgICAgICAgICAgICAgICAgImdpZXQgZHVuZyBseSBkbyIgaWYgKG0xNjUgPT0g',
'IkRPIiBhbmQgZHVuZ19seV9kbykKICAgICAgICAgICAgICAgICAgICBlbHNlICgiRE8gbmh1bmcgS0hPTkcgZHVuZyBseSBk',
'byAtPiB0aW4gZHVuZyBnaWEiIGlmIG0xNjUgPT0gIkRPIiBlbHNlICJraG9uZyBkb2MgZHVvYyB0MTY1IikpCgojIC0tLS0t',
'LS0tLS0tLS0tLS0gS0VUIExVQU4gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIj0iICogNzgpCmlubihmIlRIRSBI',
'RSBETyBEVU9DOiB7dGhlX2hlfSAgIEhFQUQ9e2hlYWRbOjEyXX0iKQojIEtob2kgZGFuIGNobyByZXZpZXdlciBiYXQgZGF1',
'IG8gZG9uZyB0cmVuLCBuZW4gQ0hFIERPIHBoYWkgbmFtIE5HQVkgZHVvaSBubzoga2hvbmcgY28gZG9uZyBuYXkKIyB0aGkg',
'bW90IGx1b3QgLS1jaGktcHJvYmUgaW4gIkRBVCA3IHwgVFJVT1QgMCB8IEtIT05HIERPIERVT0MgMCIgcmM9MCBtYSBraG9u',
'ZyBub2kgbGEgY2h1YSBjaGF5IGJvIHRlc3QuCmdoaSgiY2hlX2RvIiwgImNoaS1wcm9iZSIgaWYgQ0hJX1BST0JFIGVsc2Ug',
'ImRheS1kdSIpCmlmIENISV9QUk9CRToKICAgIGlubigiLS1jaGktcHJvYmU6IENISSBkbyBtdWMgMCwgMSwgMy4gQm8gdGVz',
'dCwgTjEtTjQsIHQxMzYsIE43IEtIT05HIGNoYXkgLSBkYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCmlm',
'IHRoZV9oZSA9PSAiZzEiOgogICAgaW5uKCJMVVUgWTogZGF5IGxhIE5FTiBETyAoZzEpLCBLSE9ORyBwaGFpIG5naGllbSB0',
'aHUgZzIuIENhYyBjaG90IE44LU4xMiBkdW9pIGRheSIpCiAgICBpbm4oIiAgICAgICBUUlVPVCBsYSBEVU5HIE5IVSBNT05H',
'IOKAlCBjaHVuZyBsYSBuaHVuZyBsbyBnMiBzaW5oIHJhIGRlIHbDoS4iKQppbm4oIi0iICogNzgpCmZvciB0ZW4sIHR0LCBj',
'dCBpbiBjaG90OgogICAgaW5uKGYiICB7dHQ6MTR9IHt0ZW59IiArIChmIiAgIHtjdH0iIGlmIGN0IGVsc2UgIiIpKQpuX2tk',
'ZCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCm5fdHJ1b3QgPSBzdW0oMSBmb3IgXywgdCwgXyBp',
'biBjaG90IGlmIHQgPT0gVFJVT1QpCmlubigiLSIgKiA3OCkKaW5uKGYiICBEQVQge3N1bSgxIGZvciBfLHQsXyBpbiBjaG90',
'IGlmIHQ9PURBVCl9IHwgVFJVT1Qge25fdHJ1b3R9IHwgS0hPTkcgRE8gRFVPQyB7bl9rZGR9IikKaW5uKGYiICBUb25nIGNh',
'IGRvOiB7c28uZ2V0KCdzb19jYV9kbycpfSB8IGRhbmggc2FjaCBkYXkgZHU6IHsnQ08nIGlmIHNvLmdldCgnbGlldF9rZV9k',
'YXlfZHUnKSBlbHNlICdLSE9ORyBETyBEVU9DJ30iKQppbm4oZiIgIEFkbWluaXN0cmF0b3I6IHtzby5nZXQoJ3F1eWVuX2Fk',
'bWluJyl9IHwgc3ltbGluazoge3NvLmdldCgnc3ltbGlua19kdW9jJyl9IikKaW5uKCIiKTsgaW5uKCItLS0gREFOIE5HVVlF',
'TiBLSE9JIEpTT04gTkFZIFZFIENITyBSRVZJRVdFUiAtLS0iKQpnaGkoImNob3QiLCBbeyJ0ZW4iOiBhLCAidHJhbmdfdGhh',
'aSI6IGIsICJjaGlfdGlldCI6IGN9IGZvciBhLCBiLCBjIGluIGNob3RdKQppbm4oanNvbi5kdW1wcyhzbywgZW5zdXJlX2Fz',
'Y2lpPUZhbHNlLCBpbmRlbnQ9MSwgZGVmYXVsdD1zdHIpKQojIHJjOiAwID0gbW9pIGNob3QgREFUIHwgMSA9IGNvIGNob3Qg',
'VFJVT1QgfCAzID0gY28gY2hvdCBLSE9ORyBETyBEVU9DICh1dSB0aWVuIGJhbyBkb25nKQpzeXMuZXhpdCgzIGlmIG5fa2Rk',
'IGVsc2UgKDEgaWYgbl90cnVvdCBlbHNlIDApKQo='
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
if ($ChiKichThuoc) { $tieuDe = 'Chi do KICH THUOC (vai giay)' }
if ($ChiProbe)     { $tieuDe = 'Chi do PROBE + tu kiem cong (vai giay)' }
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
