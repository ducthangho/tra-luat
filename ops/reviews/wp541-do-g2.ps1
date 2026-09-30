# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
# Luot DAY DU can SAN mot python >= 3.9 CO PyYAML (pip install pyyaml): ban nhung python.org ma tep nay tu tai
# KHONG co PyYAML/pip, nen no chi du cho -ChiKichThuoc / -ChiProbe. Thieu thi dung o buoc cong cu, rc=3.
#
# Do RIENG cong kich thuoc (vai giay, khong chay bo test 20-45 phut):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1" -ChiKichThuoc
#
# Do RIENG probe + tu kiem cong (vai giay, khong chay bo test):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1" -ChiProbe
#
# Nhanh mac dinh la fix_issue_541 - nhanh lease g2 khai. Ung vien tren do (2a67968 = merge 0ea95de +
# master dc85dd0) DA LAND vao master, va 30-09-2026 nhanh KHONG con tren may chu (ls-remote --heads: 458
# ref, khong co no): chay mac dinh dung o buoc fetch, rc=3 (do tren pwsh 7.4). Do ung vien khac:
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
$ShaBoDo    = 'f08990b8e9829f96f80e1c61d358435e84856e4cd52b18521bab1d3f86ee9677'      # SHA-256 cua bo do Python nhung ben duoi

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
# Thu TUNG ung vien (-Py truoc) va lay cai DAU TIEN dung duoc. Ban 30c chi probe cai tim thay dau tien: `py` cu
# che mat `python` 3.11 ngay sau no => "khong co python dung duoc" (do tren pwsh 7.4, -BoQuaTaiCongCu: rc=3).
# -Py hong thi thu tiep PATH, y nhu ban cu da lam khi -Py KHONG tim thay; ban duoc chon in o dong `py  :`.
# Luot DAY DU con doi PyYAML DUNG DUOC ngay o probe: ban 30d chi doi phien ban nen `py` thieu PyYAML che mat
# `python` co PyYAML ngay sau no => bo do dung o muc 0 "THIEU PyYAML" (do tren pwsh 7.4, 2026-09-30d: rc=3).
$ungVien = @('py','python','python3')
if ($Py) { $ungVien = @($Py) + $ungVien }
$luotDayDu = -not ($ChiKichThuoc -or $ChiProbe)
$maThu = 'import sys;print(sys.version.split()[0]);sys.exit(0 if sys.version_info>=(3,9) else 9)'
if ($luotDayDu) { $maThu = "import sys;print(sys.version.split()[0]);sys.exit(9) if sys.version_info<(3,9) else None;import yaml;yaml.safe_dump(yaml.safe_load('a: 1'))" }
foreach ($ten in $ungVien) {
    $c = Get-Command $ten -ErrorAction SilentlyContinue
    if (-not $c) { continue }
    # "CO MAT" khac "DUNG DUOC": py launcher khong co ban nao thi goi la gay.
    # Can Python >= 3.9: bo do can 3.7 (f-string 3.6, capture_output 3.7); bo test cua ung vien NGU PHAP 3.8 (`:=`)
    # nhung luc CHAY dung `str.removeprefix` (3.9): 3.8.20 THAT co PyYAML ra rc=1 "CO CHOT TRUOT" (33 ca "la"),
    # 3.9.23: 166/166 (do 2026-09-30d). Nguong suy tu ngu phap la nguong SAI.
    # <= 3.5 / 2.7 thi SyntaxError TRUOC khi excepthook kip dat -> rc=1 = "CO CHOT TRUOT" cho luot CHUA HE CHAY.
    # Doi phien ban bang MA THOAT, KHONG bang `assert`: PYTHONOPTIMIZE=1 xoa assert, probe 30c qua voi mo hinh 3.5
    # roi luot do ra rc=1 "CO CHOT TRUOT" (do tren pwsh 7.4).
    $ok = $true
    try { $thu = & $c.Source -c $maThu 2>&1 } catch { $ok = $false; $thu = $_.Exception.Message }
    if ($ok -and $LASTEXITCODE -eq 0) { $pyCmd = $c; break }
    Write-Host "  $($c.Name) co mat nhung khong dung duoc ($thu) -> thu ung vien ke"
}
if (-not $pyCmd) {
    if ($BoQuaTaiCongCu) { Dung 'khong co python dung duoc (va -BoQuaTaiCongCu dang bat)' }
    # Ban nhung KHONG co PyYAML/pip: chi du cho -ChiKichThuoc/-ChiProbe. Luot DAY DU dung NGAY o day, TRUOC khi
    # tai goi va clone kho (ban 30d tai + clone xong bo do moi bao "THIEU PyYAML").
    if ($luotDayDu) { Dung 'khong co python >= 3.9 CO PyYAML dung duoc cho luot DAY DU (ban nhung python.org khong co PyYAML/pip): cai pyyaml cho mot python roi chay lai, hoac -Py <python co PyYAML>; -ChiKichThuoc / -ChiProbe van chay duoc voi ban nhung' }
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
'IERVT0MgKGcxIGRhIGxhbmQsIGRpZmYgcm9uZykgbmVuIHJjPTMuCiAgaGVhZCBsYSBoYXUgZHVlICAgIC0+IENIVUEgZGlu',
'aCBkYW5oOiBjaGkgTjcnIChjYSBtb2kgZzIgbWFuZyB2YW8sIHhlbSBkdW9pKSBtb2kgbm9pIHVuZyB2aWVuIGcyIGhheSBr',
'aG9uZy4KICBraGFjICAgICAgICAgICAgICAgLT4gS0hPTkcgRE8gRFVPQyAocmViYXNlPyBuaGFtIG5oYW5oPykgLT4gcmM9',
'Mywga2hvbmcga2V0IGx1YW4uClR1IDIwLTA5IGcxIERBIExBTkQgdmFvIG1hc3RlciwgbmVuICJoYXUgZHVlIGN1YSBnMSIg',
'S0hPTkcgY29uIGxvYWkgZHVvYyBuaGFuaCBuYW8gKGRvIGR1b2M6Cm1hc3RlciA0NDYyMGU4IHZhIG1vdCBuaGFuaCBib29r',
'a2VlcGluZyBkZXUgcmEgInVuZyB2aWVuIGcyIiwgREFUIHJjPTApLiBWaSB2YXkgZG9pIHR1b25nIGNvbgpwaGFpIChhKSBj',
'byB0aGF5IGRvaSBzbyB2b2kgbWVyZ2UtYmFzZSB2YSAoYykgTUFORyBWQU8gaXQgbmhhdCBtb3QgY2EgTU9JIGN1YSBnMiAo',
'Q0FfTU9JX0cyOgptZXJnZS1iYXNlIGNodWEgY28sIEhFQUQgY28pIOKAlCBraG9uZyB0aGkgS0hPTkcgRE8gRFVPQy4gQ2hp',
'ICIoYikgY2hhbSBXUklURV9TRVRfRzIiIHRoaSBLSE9ORyBkdToKc2F1IGcyIGRhIGNvIDYgcGFja2V0IGtoYWMgY2hhbSBv',
'cHMvbGVhc2VfcHVibGlzaCoucHkgKGRvIGR1b2M6IG5oYW5oICM2MDcgODAzYzI0OCByYSAiVEhFIEhFIERPCkRVT0M6IGcy',
'IiwgTjcnIERBVCAyIHRlcCAvICs1MywgREFUIDEyIHJjPTApLiAoYykga2VvIHRoZW8gKGIpLCBuZW4gKGIpIGNoaSBjb24g',
'ZHVvYyBHSEksIGtob25nIGNoYW0uCgpCQSBUUkFORyBUSEFJIG8gbW9pIGNob3Q6IERBVCAvIFRSVU9UIC8gS0hPTkcgRE8g',
'RFVPQy4gQ2FpIHRodSBiYSBLSE9ORyBkdW9jIGxhbmcgbGUKdGhhbmggbW90IHRyb25nIGhhaSBjYWkga2lhIOKAlCBkbyBs',
'YSBjYSBkb2N0cmluZSBgTm9uZSAhPSBGYWxzZWAgY3VhIGtoby4KCk1PSSBjaG90IGFtIGRldSBjbyBET0kgQ0hVTkcgRFVP',
'TkcuIE1vdCBjaG90IGNoaSBkbyBjaGlldSAicGhhaSB0dSBjaG9pIiB0aGkgbW90IGhhbQpgcmV0dXJuIE5vbmVgIHZvIGRp',
'ZXUga2llbiBjdW5nIHF1YSBkdW9jIG5vLgoKRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9u',
'ZyBiaSBkdW5nIHRvaS4KIiIiCmltcG9ydCBjb250ZXh0bGliLCBoYXNobGliLCBpbXBvcnRsaWIudXRpbCwgaW5zcGVjdCwg',
'aW8sIGpzb24sIG9zLCByZSwgc2h1dGlsLCBzdWJwcm9jZXNzLCBzeXMsIHRlbXBmaWxlCmZyb20gcGF0aGxpYiBpbXBvcnQg',
'UGF0aCwgUHVyZVBvc2l4UGF0aCwgUHVyZVdpbmRvd3NQYXRoCgpvcy5lbnZpcm9uLnNldGRlZmF1bHQoIlBZVEhPTlVURjgi',
'LCAiMSIpCm9zLmVudmlyb24uc2V0ZGVmYXVsdCgiUFlUSE9OSU9FTkNPRElORyIsICJ1dGYtOCIpCmZvciBfbCBpbiAoc3lz',
'LnN0ZG91dCwgc3lzLnN0ZGVycik6CiAgICB0cnk6IF9sLnJlY29uZmlndXJlKGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0i',
'cmVwbGFjZSIpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBwYXNzCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5',
'OgogICAgICAgIGltcG9ydCBjdHlwZXMKICAgICAgICBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlNldENvbnNvbGVPdXRwdXRD',
'UCg2NTAwMSkKICAgICAgICBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlNldENvbnNvbGVDUCg2NTAwMSkKICAgIGV4Y2VwdCBF',
'eGNlcHRpb246IHBhc3MKCmRlZiBpbm4oKnApOgogICAgdmFuID0gIiAiLmpvaW4oc3RyKHgpIGZvciB4IGluIHApCiAgICB0',
'cnk6IHByaW50KHZhbiwgZmx1c2g9VHJ1ZSkKICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgdHJ5OiBzeXMuc3Rkb3V0',
'LmJ1ZmZlci53cml0ZSh2YW4uZW5jb2RlKCJ1dGYtOCIsICJyZXBsYWNlIikgKyBiIlxuIik7IHN5cy5zdGRvdXQuZmx1c2go',
'KQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb246IHByaW50KHZhbi5lbmNvZGUoImFzY2lpIiwgImJhY2tzbGFzaHJlcGxhY2Ui',
'KS5kZWNvZGUoImFzY2lpIiksIGZsdXNoPVRydWUpCgojIE5nb2FpIGxlIEtIT05HIGJhdCA9PiBQeXRob24gdGhvYXQgcmM9',
'MSwgbWEgcmM9MSBvIGRheSBEQSBDTyBOR0hJQSAiY28gY2hvdCBUUlVPVCIgKGRvbmcKIyBjdW9pIHRlcCkg4oCUIGR1bmcg',
'bHkgZG8gcHMxIGRhdCBgdHJhcGAgLT4gcmM9My4gRG8gZHVvYzogZ2l0IHZhbmcgUEFUSCAoZG9uZyBgZ2l0KGdvYywKIyAi',
'cmV2LXBhcnNlIilgIGNoYXkgVFJVT0MgYGlmIGxvaTpgKSwgYm8gdGVzdCBxdWEgaGFuLCB1bmcgdmllbiB0aGlldSBfZ2l0',
'X3dpbmRvd3MsIHByb2JlCiMgdGhhdCBuZW0gbmdvYWkgbGUg4oCUIGNhIGJvbiB0dW5nIHJhIHJjPTEgbWEgcGhlcCBkbyBD',
'SFVBIEhFIGNoYXkgeG9uZy4KIyBEb25nIEtFVCBMVUFOIGluIFRSVU9DIHRyYWNlYmFjaywgY3VuZyBrZW5oIHN0ZG91dDog',
'a2hvaSBwczEgZGFuIGNobyByZXZpZXdlciBiYXQgZGF1IFRVIGRvbmcKIyBuYXksIG5lbiBpbiB0cmFjZWJhY2sgdHJ1b2Mg',
'dGhpIG5vIG5hbSBOR09BSSBraG9pIChkbyB0cmVuIHB3c2ggNy40OiBraG9pIDIgZG9uZywgMCBkb25nCiMgdHJhY2ViYWNr',
'KS4gdHJ5L2ZpbmFsbHk6IGhvb2sgVFUgSE9ORyAodmQuIHN0ZG91dCBsYSBvbmcgZGEgZG9uZykgdGhpIFB5dGhvbiB0cmEg',
'cmM9MSDigJQgZHVuZwojIG1hICJjbyBjaG90IFRSVU9UIiAoZG8gZHVvYzogQnJva2VuUGlwZSB0cm9uZyBob29rID0+IHJj',
'PTEpLgpkZWYgX25nb2FpX2xlX2xhX0tERChraWV1LCBndCwgdmV0KToKICAgIHRyeToKICAgICAgICBpbXBvcnQgdHJhY2Vi',
'YWNrCiAgICAgICAgaW5uKCIiKTsgaW5uKGYiS0hPTkcgRE8gRFVPQzogbmdvYWkgbGUga2hvbmcgbHVvbmcgdHJ1b2Mge2tp',
'ZXUuX19uYW1lX199OiB7Z3R9IikKICAgICAgICBpbm4oIiIuam9pbih0cmFjZWJhY2suZm9ybWF0X2V4Y2VwdGlvbihraWV1',
'LCBndCwgdmV0KSkucnN0cmlwKCkpCiAgICAgICAgaW5uKCJQaGVwIGRvIENIVUEgY2hheSB4b25nLiBLaG9uZyBrZXQgbHVh',
'biBnaS4iKQogICAgICAgIGZvciBfbCBpbiAoc3lzLnN0ZG91dCwgc3lzLnN0ZGVycik6CiAgICAgICAgICAgIHRyeTogX2wu',
'Zmx1c2goKQogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uOiBwYXNzCiAgICBmaW5hbGx5OgogICAgICAgIG9zLl9leGl0',
'KDMpCnN5cy5leGNlcHRob29rID0gX25nb2FpX2xlX2xhX0tERAoKU0hBX0cxICAgPSAiMmY3MDg2OWEwNTM3ODQzZTljYWU3',
'ODYxOGVlN2FlOGMyNjFkOTcyZCIKIyBLSE9ORyBnaGltIGJhc2UuIFNwZWMgcjMgTjYnIGtoYWkgZG8gbnVtc3RhdCBzbyBk',
'NzA1NjIzIOKAlCBOSFVORyBzcGVjIENVTkcgYmFvIGV4ZWN1dG9yCiMgYGdpdCBtZXJnZSBvcmlnaW4vbWFzdGVyYC4gU2F1',
'IG1lcmdlLCBwaGVwIGRvIHNvIGQ3MDU2MjMgTlVPVCBjYSBwaGFuIG1hc3RlciBtYW5nIHZhbzoKIyBkbyB0aGF0IDE4LTA5',
'IHRyZW4gYmFuIHZhIGcyIGN1YSBhZ3kgY2hvIDUgdGVwIC8gKzgxMiwgdHJvbmcga2hpIHZpZWMgY3VhIGFneSBsYSAyIHRl',
'cCAvICszNTMuCiMgTW90IGNob3Qgbmh1IHRoZSBzZSBiYW8gInZ1b3QgdHJhbiIgY2hvIG1vdCBiYW4gdmEgS0hPTkcgdnVv',
'dC4gQmFzZSBkdW5nIGxhIE1FUkdFLUJBU0UuClNIQV9CQVNFX1NQRUMgPSAiZDcwNTYyMzE2MmI3NWI3MzQwZWU3Y2NhNTRh',
'YzJkMmFiYmRkYmI2ZiIKQkFOX0JPX0RPID0gIjIwMjYtMDktMzBlIiAgICAgICAgICAgICAgIyBkb2kgTU9JIGtoaSBzdWEg',
'Ym8gZG8gLSBsb2cgdHUga2hhaSBiYW4gbmFvClRSQU5fVEVQLCBUUkFOX0RPTkcgPSAyLCA0MDAgICAgICAgICAgIyBONycg',
'Y3VhIHNwZWMgcjMKTUFVX1dJTiAgPSAnaWYgbmVuX3RodWMgPT0gIndpbmRvd3MiOicKIyBXcml0ZSBzZXQgY3VhIHBhY2tl',
'dCAjNTQxIGcyLiBEaWZmIGtob25nIGNoYW0gdGVwIG5hbyBvIGRheSA9PiBkbyBOSEFNIE5IQU5ILgpXUklURV9TRVRfRzIg',
'PSB7Im9wcy9sZWFzZV9wdWJsaXNoLnB5IiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkifQojICJUdW9pIiBjaGkgY28g',
'bmdoaWEga2hpIHNvIHZvaSBNQVkgQ0hVIFRIQVQuIE1vdCBtaXJyb3IgY3VjIGJvIGN1IGN1bmcgdHJhIGxzLXJlbW90ZSA9',
'PQojIG9yaWdpbi9tYXN0ZXIgKGRvIGR1b2M6IG1hc3RlciBjMTZiZDMyIC0+ICJ2ZSBuZW4gVFVPSSIsIDQ2IHRlcCAvICs3',
'MTE4IGNobyAwZWE5NWRlKS4KIyBEYW5oIHNhY2ggQ0hPIFBIRVA7IGByZW1vdGUgZ2V0LXVybGAgZGEga2hhaSB0cmllbiBp',
'bnN0ZWFkT2YgbmVuIGNodXllbiBodW9uZyBjdW5nIGxvIHJhLgpVUkxfS0hPX0hPUF9MRSA9IHsiaHR0cHM6Ly9naXRodWIu',
'Y29tL2R1Y3RoYW5naG8vdHJhLWx1YXQiLCAiaHR0cHM6Ly9naXRodWIuY29tL2R1Y3RoYW5naG8vdHJhLWx1YXQuZ2l0IiwK',
'ICAgICAgICAgICAgICAgICAgIyBTU0ggdG9pIENVTkcga2hvIChzYXUgX3VybF9zYWNoKTogYHVybC4iZ2l0QGdpdGh1Yi5j',
'b206Ii5pbnN0ZWFkT2YgImh0dHBzOi8vZ2l0aHViLmNvbS8iYAogICAgICAgICAgICAgICAgICAjIHJhdCBwaG8gYmllbiBv',
'IG1heSBkZXY7IHRoaWV1IGhhaSBkYW5nIG5heSB0aGkga2hvIFRIQVQgYmkgYmFvICJLSE9ORyBwaGFpIGtobyB0aGF0Ii4K',
'ICAgICAgICAgICAgICAgICAgInNzaDovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdCIsICJzc2g6Ly9naXRodWIu',
'Y29tL2R1Y3RoYW5naG8vdHJhLWx1YXQuZ2l0IiwKICAgICAgICAgICAgICAgICAgImdpdEBnaXRodWIuY29tOmR1Y3RoYW5n',
'aG8vdHJhLWx1YXQiLCAiZ2l0QGdpdGh1Yi5jb206ZHVjdGhhbmdoby90cmEtbHVhdC5naXQifQojIGByZW1vdGUgZ2V0LXVy',
'bGAgS0hBSSBUUklFTiBpbnN0ZWFkT2YsIG1hIG1hdSBgdXJsLiJodHRwczovLzx0b2tlbj5AZ2l0aHViLmNvbS8iLmluc3Rl',
'YWRPZmAgcmF0IHBobwojIGJpZW4uIEluL2doaSBuZ3V5ZW4gdmFuIGxhIGR1YSBUT0tFTiB2YW8gbG9nIHZhIHZhbyBraG9p',
'IEpTT04gcHMxIGJhbyBkYW4gY2hvIHJldmlld2VyIChkbyBkdW9jOgojIDMgZG9uZyB0cm9uZyBraG9pIGRhbikuIEJvIHVz',
'ZXJpbmZvIFRSVU9DIGtoaSBpbiB2YSBUUlVPQyBraGkgc28g4oCUIHRva2VuIHZhbiBsYSBHaXRIdWIgdGhhdC4KIyBBdXRo',
'b3JpdHkga2V0IHRodWMgbyBgL2AsIGA/YCBob2FjIGAjYCBEQVUgVElFTiDigJQgZHVuZyBsdWF0IGdpdC9jdXJsLiBCYW4g',
'YFteL10qQGAgbnVvdCBjYSBgP2AvYCNgCiMgbmVuIG1vdCBVUkwgdHJvIHRvaSBNQVkgS0hBQyAoaG9zdCBkdW5nIHRydW9j',
'IGA/YCwgZHVvaSBgP2AgbGEgYEBnaXRodWIuY29tLzxraG8+YCkgZHVvYyAibGFtIHNhY2giCiMgdGhhbmggZHVuZyBtb3Qg',
'bXVjIENITyBQSEVQLCB0cm9uZyBraGkgZ2l0IG5vaSB0b2kgbWF5IGtpYSAoZG8gZHVvYzogbWlycm9yIGN1IHBodWMgdnUg',
'cXVhIEhUVFBTID0+CiMgInZlIG5lbiBUVU9JIiwgVFJVT1QgNDYgdGVwIC8gKzcxMTgpLiBWYW4gYm8gdG9pIGBAYCBDVU9J',
'IHRyb25nIGF1dGhvcml0eTogdXNlcmluZm8gY28gYEBgIHRyYW4gdGhpCiMgY3VybCB0dSBjaG9pICgiQmFkIGhvc3RuYW1l',
'IiksIGNvbiBraGkgaW4gdGhpIGtob25nIGxvIHBoYW4gc2F1IGBAYCB0aHUgbmhhdC4KX1JYX1VTRVJJTkZPID0gcmUuY29t',
'cGlsZShyIl4oW0EtWmEtel1bQS1aYS16MC05Ky4tXSo6Ly8pW14vPyNdKkAiKQpkZWYgX3VybF9zYWNoKHUpOiByZXR1cm4g',
'X1JYX1VTRVJJTkZPLnN1YihyIlwxIiwgdSBvciAiIikgICAgICAgICAgIyBkZSBTTyAobHVhdCBnaXQvY3VybCkKIyBJTiBw',
'aGFpIGNoZSBST05HIGhvbiBTTzogbWF0IGtoYXUgY28gYD9gL2AjYCBUUkFOIHRoaSBgW14vPyNdKkBgIGtob25nIGtob3Ag',
'bmVuIFVSTCByYSBsb2cgTkdVWUVOIFZBTgojIChkbyBkdW9jIHRyZW4gMjAyNi0wOS0zMGI6IDMgZG9uZyBvIC0tY2hpLWtp',
'Y2gtdGh1b2MsIDMgZG9uZyB0cm9uZyBraG9pIGRhbiAtLWNoaS1wcm9iZTsgYmFuIDMwYTogMCkuCiMgQ2hlIHRvaSBgQGAg',
'Q1VPSSBDVU5HIGN1YSBDQSBjaHVvaSAoY28gaGF5IGtob25nIGNvIHNjaGVtZSksIHZhIERFIERBVSBgKioqQGAgZGUgYmFu',
'IGluIGtob25nIHR1IG5oYW4gbGEKIyBnaXRodWIuY29tIGtoaSBnaXQgbm9pIHRvaSBtYXkga2hhYyAodmQuIGhvc3QgdHJ1',
'b2MgYD9gKS4gQmFuIDMwYyBjaGUgInRvaSBgQGAgY3VvaSB0cnVvYyBgL2AgZGF1IHRpZW4iCiMgbmVuIFZBTiBsbyBraGkg',
'bWF0IGtoYXUgY28gYC9gIHRyYW4sIGhvYWMgVVJMIGRhbmcgc2NwIGB1c2VyOm1rQGhvc3Q6ZHVvbmdgIChraG9uZyBzY2hl',
'bWUpIOKAlCBkbyB0cmVuCiMgMjAyNi0wOS0zMGM6IDMgZG9uZyAvIDEgdHJvbmcga2hvaSBkYW4gLS1jaGkta2ljaC10aHVv',
'YywgNSAvIDMgbyAtLWNoaS1wcm9iZSwgbW9pIGRhbmcuIE1vaSBreSB0dSBEVU5HCiMgbGEgbW90IGR1b25nIG51YTsgInRv',
'aSBgQGAgY3VvaSIga2hvbmcgY29uIGt5IHR1IGR1bmcgbmFvLiBIYWkgcXV5IHRhYywgaGFpIG11YyBkaWNoOiBTTyB0aGVv',
'IGdpdCwgSU4KIyB0aGVvICJ0aHVhIGNvbiBob24gbG8iLgpkZWYgX3VybF9pbih1KTogcmV0dXJuIHJlLnN1YihyIl4oW0Et',
'WmEtel1bQS1aYS16MC05Ky4tXSo6Ly8pPy4qQCIsIHIiXDEqKipAIiwgdSBvciAiIikKIyBUaG9uZyBiYW8gbG9pIGN1YSBn',
'aXQgQ0hJIGJvIHVzZXJpbmZvIHRvaSBgQGAgREFVIFRJRU46IHVzZXJpbmZvIGNvIGBAYCB0cmFuICh2ZC4gdGVuIGRhbmcg',
'bmhhcCBsYQojIGVtYWlsKSB0aGkgcGhhbiBzYXUgdmFuIHJhIHN0ZGVyciBscy1yZW1vdGUsIG1hIHN0ZGVyciBheSBkdW9j',
'IGluIHZhbyBkb25nIEtERCBjdWEgTjcnIChkbyBkdW9jOgojIDIgZG9uZyB0cm9uZyBsb2csIDEgdHJvbmcga2hvaSBkYW4p',
'LiBMYW0gc2FjaCBNT0kgVVJMIHRyb25nIHZhbiBiYW4gdHJ1b2Mga2hpIGluIOKAlCBjaGUgdG9pIGBAYCBDVU9JIHRyZW4K',
'IyBET05HIChjdW5nIGx1YXQgSU4gdm9pIF91cmxfaW46IGtob25nIGNvbiBreSB0dSBkdW5nIG5hbykuIEJhbiAzMGQgZHVu',
'ZyBvIGBccyciYCBuZW4gcGhhbiBnaXQgZGUgbGFpIGNvCiMgYCdgL2AiYC9raG9hbmcgdHJhbmcgKHZkLiBgdUB4OnAnPGJp',
'IG1hdD5AZ2l0aHViLmNvbWApIFZBTiBsbyDigJQgZG8gdHJlbiAyMDI2LTA5LTMwZDogMiBkb25nIC8gMSB0cm9uZwojIGto',
'b2kgZGFuIC0tY2hpLWtpY2gtdGh1b2MsIDMgLyAyIG8gLS1jaGktcHJvYmUsIG1vaSBkYW5nLgpkZWYgX2FuX3VzZXJpbmZv',
'KHQpOiByZXR1cm4gcmUuc3ViKHIiKFtBLVphLXpdW0EtWmEtejAtOSsuLV0qOi8vKVteXG5dKkAiLCByIlwxKioqQCIsIHQg',
'b3IgIiIpCiMgQ2EgbmdvYWkgcGhhbSB2aSByMyDCp25nb2FpX3BoYW1fdmkg4oCUIGRvIENISU5IIFNQRUMga2hhaSwga2hv',
'bmcgcGhhaSBibyBkbyB0dSBxdXlldC4KIyBEbyBsYSBEQU5IIFNBQ0ggQ0hPIFBIRVA6IGNhIGRvIG5hbyBLSE9ORyBuYW0g',
'dHJvbmcgZGF5IHZhIEtIT05HIHBoYWkgInRoaWV1IGNvbmcgY3UiCiMgdGhpIGxhIFRSVU9ULiBEYW5oIHNhY2ggY2FtIHRo',
'aSBiYW8gZ2lvIGN1bmcgdGhpZXU7IGRhbmggc2FjaCBjaG8gcGhlcCB0aGkgYmlldCB0cnVvYy4KTkdPQUlfUEhBTV9WSSA9',
'IHNldCgidDEzMSB0MTMyIHQxNTAgdDEyNSB0MzUgdDM2IHQzNyB0MzggdDM5IHQ0MCIuc3BsaXQoKSkKIyBDYSBjdWEgQ0hJ',
'TkggcGFja2V0IG5heS4gTW90IGNhIG8gZGF5IG1hIERPIHRoaSBraG9uZyBiYW8gZ2lvIGR1b2MgYm8gcXVhLgpDQV9QQUNL',
'RVQgPSBzZXQoInQxNjUgdDE2NiB0MTY3IHQxNjggdDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpKQojIENhIE1P',
'SSBtYSBnMiB0aGVtIHZhbyAoTjgtTjEyKS4gRG9pIHR1b25nIGRvIHBoYWkgTUFORyBjaHVuZyB2YW86IG1lcmdlLWJhc2Ug',
'Y2h1YSBjbywgSEVBRCBjby4KQ0FfTU9JX0cyID0gInQxNjkgdDE3MCB0MTcxIHQxNzIgdDE3MyIuc3BsaXQoKQpDQTE1ICA9',
'ICJ0MTI5IHQxMzAgdDEzMSB0MTMyIHQxMzMgdDEzNiB0MTM4IHQxMzkgdDE0NCB0MTQ1IHQxNDYgdDE0NyB0MTQ5IHQxNTAg',
'dDE1MSIuc3BsaXQoKQpDQU1PSSA9ICJ0MTY1IHQxNjYgdDE2NyB0MTY4Ii5zcGxpdCgpCgpEQVQsIFRSVU9ULCBLREQgPSAi',
'REFUIiwgIlRSVU9UIiwgIktIT05HIERPIERVT0MiCnNvLCBjaG90ID0ge30sIFtdCmRlZiBnaGkoaywgdik6IHNvW2tdID0g',
'djsgcmV0dXJuIHYKZGVmIGtldCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0PSIiKToKICAgIGNob3QuYXBwZW5kKCh0ZW4s',
'IHRyYW5nX3RoYWksIGNoaV90aWV0KSkKICAgIGlubihmIiAgW3t0cmFuZ190aGFpOjE0fV0ge3Rlbn0iICsgKGYiICAge2No',
'aV90aWV0fSIgaWYgY2hpX3RpZXQgZWxzZSAiIikpCiAgICByZXR1cm4gdHJhbmdfdGhhaQoKIyAtLS0tLS0tLS0tLS0tLS0t',
'IGRvYyBsb2cgY3VhIGJvIHRlc3QgKGJhbiAzLCBkYSBkbyB0cmVuIGxvZyBUSEFUKSAtLS0tLS0tLS0tLS0tLS0tClJYX0RP',
'X0NITyAgPSByZS5jb21waWxlKHIiKD9tKV4hISEgZG8gKFxTKykgKC4qKSQiKQpSWF9ET19DVU9JID0gcmUuY29tcGlsZShy',
'Iig/bSleIHsyfShcU3sxLDR9KSB7Mn0oXFMrKTogKC4qKSQiKQpSWF9CT19RVUEgID0gcmUuY29tcGlsZShyIig/bSleIHsy',
'fVxTezEsNn0gUVVBIChcUyspOiAoLiopJCIpCiMgRG9uZyB0b25nIGtldCBUSEFUIG8gREFVIGRvbmcuIENhIERPIGNvIHRo',
'ZSBpbiBsYWkgc3Rkb3V0IGN1YSBtb3QgbHVvdCBDT04gKHQxNTUgY2hheSBsYWkgdDAxLCB0NzIvdDk4IGNoYXkKIyAiYm8i',
'KSDigJQgZG9uZyB0b25nIExPTkcgYXkgbmFtIEdJVUEgZG9uZyAoZG86IDIwIGRvbmcgbG9uZyBkZXUgbyBnaXVhIGRvbmcs',
'IGNoaSBkb25nIHRvbmcgdGhhdCBvIGRhdSBkb25nKSwgbWEKIyBgc2VhcmNoYCBraG9uZyBuZW8gYmF0IG5vIFRSVU9DLiBE',
'byB0cmVuIDIwMjYtMDktMzBjLCAwZWE5NWRlICsgZG90IGJpZW4gbGFtIHQwMSBETzogZG9jIHJhICIwLzEiID0+CiMgImRh',
'bmggc2FjaCBLSE9ORyBkYXkgZHUiLCAiTEVDSCBTTyBIT0M6IHRoaWV1IC0yMCBjYSIsIHRyb25nIGtoaSB0b25nIHRoYXQg',
'MTY2LTE0NT0yMSA9PSAyMSBjYSBkb2MgZHVvYy4KUlhfVE9ORyAgICA9IHJlLmNvbXBpbGUociIoP20pXmxlYXNlX3B1Ymxp',
'c2g6IChcZCspLyhcZCspXGJbXlxuXSo/PShcZCspLFteXG5dKj89KFxkKykiKQoKZGVmIHNvX2NhKHQpOgogICAgbSA9IHJl',
'Lm1hdGNoKHIidChcZCspIiwgdCk7IHJldHVybiAoaW50KG0uZ3JvdXAoMSkpIGlmIG0gZWxzZSAxMCoqNiwgdCkKCmRlZiBk',
'b2NfZG8ob3V0KToKICAgIHRhaV9jaG8gPSB7dDogbC5zdHJpcCgpIGZvciB0LCBsIGluIFJYX0RPX0NITy5maW5kYWxsKG91',
'dCl9CiAgICBibyA9IHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91dCl9CiAgICBjdW9pID0ge3Q6IGwuc3Ry',
'aXAoKSBmb3IgXywgdCwgbCBpbiBSWF9ET19DVU9JLmZpbmRhbGwob3V0KSBpZiB0IG5vdCBpbiBib30KICAgIGhvcCA9IGRp',
'Y3QoY3VvaSk7IGhvcC51cGRhdGUodGFpX2NobykKICAgIGdjLCB0aW4gPSBbXSwgVHJ1ZQogICAgaWYgc2V0KHRhaV9jaG8p',
'ICE9IHNldChjdW9pKToKICAgICAgICBnYy5hcHBlbmQoZiJoYWkgbmd1b24gTEVDSDogY2hpLXRhaS1jaG89e3NvcnRlZChz',
'ZXQodGFpX2Nobyktc2V0KGN1b2kpKX0gY2hpLWN1b2k9e3NvcnRlZChzZXQoY3VvaSktc2V0KHRhaV9jaG8pKX0iKQogICAg',
'ICAgIHRpbiA9IEZhbHNlCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0KQogICAgaWYgbm90IG06CiAgICAgICAgZ2MuYXBw',
'ZW5kKCJLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcga2V0Iik7IHRpbiA9IEZhbHNlCiAgICBlbHNlOgogICAgICAgIGRhdCwg',
'dHJlbiA9IGludChtLmdyb3VwKDEpKSwgaW50KG0uZ3JvdXAoMikpCiAgICAgICAgZ2MuYXBwZW5kKGYic28gaG9jOiB7dHJl',
'bn0te2RhdH09e3RyZW4tZGF0fSBkbzsgZG9jIGR1b2Mge2xlbihob3ApfSIpCiAgICAgICAgaWYgdHJlbiAtIGRhdCAhPSBs',
'ZW4oaG9wKToKICAgICAgICAgICAgZ2MuYXBwZW5kKGYiTEVDSCBTTyBIT0M6IHRoaWV1IHt0cmVuLWRhdC1sZW4oaG9wKX0g',
'Y2EiKTsgdGluID0gRmFsc2UKICAgIHJldHVybiBob3AsIGdjLCB0aW4KCiMgTWF1IGNvIGRvbmcgdG9uZyBMT05HIGdpdWEg',
'ZG9uZyAoZGFuZyB0MTU1IGluIGxhaSBsdW90IGNvbik6IGJvIGRvYyBiYXQgZG9uZyB0b25nIERBVSBUSUVOIGxhIHR1IGtp',
'ZW0gRE8uCl9NQVUgPSAoIiEhISBkbyB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOIGEgJ2xlYXNlX3B1Ymxpc2g6IDAv',
'MSDEkeG6oXQ7IMSRw6MgY2jhuqF5PTEsIGLhu48gcXVhPTAnXG4iCiAgICAgICAgIiEhISBkbyB0MTUwX3ggV2luRXJyb3Ig',
'MTMxNCByZXF1aXJlZCBwcml2aWxlZ2VcbiIKICAgICAgICAiICBC4buOIFFVQSB0MTMxX3k6IG5lbiBmaXh0dXJlXG4iCiAg',
'ICAgICAgIiAgxJDhu44gIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU46IGFcbiIKICAgICAgICAiICDEkOG7jiAgdDE1',
'MF94OiBXaW5FcnJvciAxMzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICJsZWFzZV9wdWJsaXNoOiAxLzMgxJHh',
'uqF0OyDEkcOjIGNo4bqheT0zLCBi4buPIHF1YT0xXG4iKQoKIyBCaWVuIFBZVEhPTiogY3VhIG1heSBuZ3VvaSBkbyBsb3Qg',
'dmFvIGJvIHRlc3QgbGEgRE9JIEhBTkggVkkgYm8gdGVzdDogUFlUSE9OT1BUSU1JWkUgYm8gbW9pIGBhc3NlcnRgIChkbyB0',
'cmVuCiMgMjAyNi0wOS0zMGM6IGBhc3NlcnQgRmFsc2VgIHF1YSwgcmM9MCk7IGJhbiAzMGQgY2hpIHRydW5nIGhvYSBNT1Qg',
'YmllbiBheSwgY29uIFBZVEhPTkRFVk1PREU9MSBsYW0gdDE1NCBETyAyLzQKIyBsYW4gdHJlbiAzLjExIChzYWNoOiA0LzQg',
'UVVBKSA9PiByYz0xICJUUlVPVCBNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIgY2hvIHVuZyB2aWVuIHNhY2ggKGRv',
'IHRyZW4KIyAyMDI2LTA5LTMwZCkuIERhbmggc2FjaCBDQU0gbHVvbiB0aGlldSBtb3QgYmllbiDigJQgbmVuIGRheSBsYSBk',
'YW5oIHNhY2ggQ0hPIFBIRVA6IGNoaSBnaXUgYmllbiBkZSB0cmluaCB0aG9uZwojIGRpY2ggQ0hBWSB2YSB0aW0gZ29pIERB',
'IENBSTsgUFlUSE9OUEFUSCBLSE9ORyBnaXUgKENJIGtob25nIGNvIG5vKS4gUGhlcCBob2kgZGlldSBraWVuIHRpZW4gcXV5',
'ZXQgbyBtdWMgMAojIGN1bmcgY2hheSBxdWEgZGF5LCBuZW4gbm8gdGhheSBEVU5HIG1vaSB0cnVvbmcgbWEgYm8gdGVzdCBz',
'ZSB0aGF5LgpfUFlfR0lVID0gZnJvemVuc2V0KHsiUFlUSE9OSE9NRSIsICJQWVRIT05VU0VSQkFTRSIsICJQWVRIT05OT1VT',
'RVJTSVRFIn0pCmRlZiBjaGF5KGFyZ3YsIGN3ZCwgcGh1dD02MCk6CiAgICBtdCA9IHtrOiB2IGZvciBrLCB2IGluIG9zLmVu',
'dmlyb24uaXRlbXMoKSBpZiBub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIlBZVEhPTiIpIG9yIGsudXBwZXIoKSBpbiBfUFlf',
'R0lVfQogICAgbXQudXBkYXRlKFBZVEhPTlVURjg9IjEiLCBQWVRIT05JT0VOQ09ESU5HPSJ1dGYtOCIsIFBZVEhPTkRPTlRX',
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
'a2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCIpCiMgQm8gdGVzdCAobXVjIDIgdmEgTjcpIGNhbiBQeVlBTUw6IHRoaWV1IG5v',
'LCAwZWE5NWRlIHJhIDk2LzE2NiBjYSBETyAoODkgYmFvIHRoYW5nICJObyBtb2R1bGUgbmFtZWQgJ3lhbWwnIiwKIyA3IHF1',
'YSBsdW90IGNvbjsgY28gUHlZQU1MOiAxNjYvMTY2IFFVQSkuIEJvIGRvIGdvaSBjaHVuZyBsYSAiY2EgRE8gTEEiIHJvaSBw',
'aGF0IFRSVU9UIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBjLgojIERpZXUga2llbiB0aWVuIHF1eWV0IHBoYWkgaG9pIGJhbmcg',
'Q0hJTkggdGllbiB0cmluaCBjb24gc2UgY2hheSBibyB0ZXN0IChjaGF5KCk6IGN1bmcgbW9pIHRydW9uZzsgY3dkID0gb3Bz',
'LyA9CiMgc3lzLnBhdGhbMF0gY3VhIGJvIHRlc3QpIHZhIGhvaSBEVU5HIERVT0MgY2h1IGtob25nIGhvaSBDTyBNQVQuIEJh',
'biAzMGQgaG9pIGBmaW5kX3NwZWMoInlhbWwiKWAgbyB0aWVuIHRyaW5oCiMgTkFZIHZhIG5ndW9uZyAzLjggc3V5IHR1IE5H',
'VSBQSEFQIChgOj1gKSDigJQgZG8gdHJlbiAyMDI2LTA5LTMwZCwgY2EgaGFpIHJhIHJjPTEgVFJVT1QgY2hvIHVuZyB2aWVu',
'IHNhY2g6CiMgdGh1IG11YyBkdSBsaWV1IGB5YW1sL2AgdHJlbiBQWVRIT05QQVRIIHF1YSBmaW5kX3NwZWMgbWEgYHlhbWwu',
'c2FmZV9kdW1wYCBraG9uZyBjbyAoODcgY2EgImxhIik7IHB5dGhvbiAzLjguMjAKIyBUSEFUIGNvIFB5WUFNTCwgYm8gdGVz',
'dCBkdW5nIGBzdHIucmVtb3ZlcHJlZml4YCAoMy45KSBsdWMgQ0hBWSAoMzMgY2EgImxhIjsgMy45LjIzOiAxNjYvMTY2KS4K',
'aWYgbm90ICgiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Ygb3IgIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndik6CiAg',
'ICBfcmNfZGssIF9yYV9kayA9IGNoYXkoWyItYyIsICJpbXBvcnQgc3lzOyBzeXMuZXhpdCg5KSBpZiBzeXMudmVyc2lvbl9p',
'bmZvIDwgKDMsIDkpIGVsc2UgTm9uZTsgaW1wb3J0IHlhbWw7IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAi',
'IHlhbWwuc2FmZV9kdW1wKHlhbWwuc2FmZV9sb2FkKCdhOiAxJykpIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgZ29j',
'IC8gIm9wcyIgaWYgKGdvYyAvICJvcHMiKS5pc19kaXIoKSBlbHNlIFBhdGguY3dkKCksIHBodXQ9MikKICAgIGlmIF9yY19k',
'ayA9PSA5OgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24ge3N5cy52ZXJzaW9uLnNwbGl0KClbMF19IDwgMy45OiBibyB0',
'ZXN0IGN1YSB1bmcgdmllbiBkdW5nIHN0ci5yZW1vdmVwcmVmaXggKDMuOSkgbHVjIENIQVkiKQogICAgZWxpZiBfcmNfZGs6',
'CiAgICAgICAgbG9pLmFwcGVuZChmInB5dGhvbiBuYXkgS0hPTkcgY28gUHlZQU1MIGR1bmcgZHVvYyAoeyhfcmFfZGsuc3Ry',
'aXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFdWzo5MF19KToiCiAgICAgICAgICAgICAgICAgICBmIiBcIntzeXMuZXhl',
'Y3V0YWJsZX1cIiAtbSBwaXAgaW5zdGFsbCBweXlhbWwiCiAgICAgICAgICAgICAgICAgICAiIChiYW4gbmh1bmcgcHMxIHR1',
'IHRhaSBLSE9ORyBjbyBwaXA6IGNoYXkgbGFpIHZvaSAtUHkgPHB5dGhvbiBkYSBjbyBQeVlBTUw+KSIpCgpyYywgaGVhZCwg',
'XyA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAiSEVBRCIpCmlmIHJjOiBsb2kuYXBwZW5kKCJraG9uZyBkb2MgZHVvYyBIRUFE',
'IikKZ2hpKCJoZWFkIiwgaGVhZCkKcmNfYSwgXywgXyA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIi0taXMtYW5jZXN0b3Ii',
'LCBTSEFfRzEsIGhlYWQgb3IgIkhFQUQiKQpsYV9oYXVfZHVlID0gKHJjX2EgPT0gMCkKaWYgaGVhZCA9PSBTSEFfRzE6CiAg',
'ICB0aGVfaGUgPSAiZzEiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IERBWSBMQSBnMS4gQ0hVQSBjbyBiYW4gdmEg',
'ZzI7IGtldCBxdWEgZHVvaSBsYSBORU4gRE8uIikKZWxpZiBsYV9oYXVfZHVlOgogICAgdGhlX2hlID0gImcyIjsgaW5uKGYi',
'ICBIRUFEID0ge2hlYWRbOjhdfSAtPiBoYXUgZHVlIGN1YSBnMSAoe1NIQV9HMVs6OF19KTsgdW5nIHZpZW4gZzIgaGF5IGto',
'b25nOiBONycgKG11YyAxKSBkaW5oIGRhbmguIikKZWxzZToKICAgIHRoZV9oZSA9ICI/IjsgbG9pLmFwcGVuZChmIkhFQUQ9',
'e2hlYWRbOjhdfSBLSE9ORyBwaGFpIGcxIHZhIEtIT05HIHBoYWkgaGF1IGR1ZSBjdWEge1NIQV9HMVs6OF19IOKAlCByZWJh',
'c2U/IG5oYW0gbmhhbmg/IikKZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCnJjX3IsIHJlZnMsIF8gPSBnaXQoZ29jLCAiZm9yLWVh',
'Y2gtcmVmIiwgIi0tcG9pbnRzLWF0IiwgaGVhZCBvciAiSEVBRCIsCiAgICAgICAgICAgICAgICAgICAgIi0tZm9ybWF0PSUo',
'cmVmbmFtZTpzaG9ydCkiKQpkc3IgPSBbeCBmb3IgeCBpbiByZWZzLnNwbGl0bGluZXMoKSBpZiB4LnN0cmlwKCkgYW5kIHgu',
'c3RyaXAoKSAhPSAiZG8tdGFtIl0KZ2hpKCJyZWZfdHJvX3RvaV9oZWFkIiwgZHNyKQppbm4oZiIgIHJlZiB0cm8gdG9pIEhF',
'QUQ6IHsnLCAnLmpvaW4oZHNyKSBpZiBkc3IgZWxzZSAnKGtob25nIHJlZiBuYW8gLSBIRUFEIHJvaSB0dSBkbyknfSIpCgpp',
'ZiBsb2k6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IG5lbiBkbyBzYWksIEtIT05HIGluIGtldCBsdWFuIG5h',
'by4iKQogICAgZm9yIHggaW4gbG9pOiBpbm4oIiAgLSIsIHgpCiAgICBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0t',
'IDEuIGtpY2ggdGh1b2MgKE43JyBjdWEgc3BlYyByMykgLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgp',
'OyBpbm4oIjEuIEtJQ0ggVEhVT0Mg4oCUIHRyYW4gc3BlYyByMzogPD0gMiB0ZXAgdmEgPD0gNDAwIGRvbmcgdGhlbSIpCiMg',
'VkUgTkVOIFBIQUkgVFVPSSDigJQgdmEgcGhhaSBDSFVORyBNSU5IIGR1b2MgbGEgdHVvaSwga2hvbmcgcGhhaSBnaWEgZGlu',
'aC4KIyBCYWkgaG9jIHRyYSBnaWEgMTktMDktMjAyNjogY2xvbmUgdGFpIGR1bmcgY2hpIGZldGNoIG5oYW5oIGJhbiB2YSwg',
'YG9yaWdpbi9tYXN0ZXJgCiMgZHVuZyB5ZW4gdHUgMTQtMDkgKGMxNmJkMzIsIHNhdSA5NyBjb21taXQpLiBtZXJnZS1iYXNl',
'IHJvaSB2ZSBkdW5nIGRpbmggbWFzdGVyIGN1LAojIG5lbiBkaWZmIE5VT1QgY2EgOTcgY29tbWl0IG1hc3RlcjogZG8gcmEg',
'NDYgdGVwIC8gKzcxMTggdGhheSB2aSAyIHRlcCAvICszOTcg4oCUCiMgQ1VORyBNT1QgQ09NTUlUIDBlYTk1ZGUuIE1vdCB0',
'aWV1IGNoaSBERUxUQSBtYSB2ZSBuZW4ga2hvbmcgdHVvaSB0aGkga2hvbmcgc2FpCiMgbGVjaCBtb3QgY2h1dCwgbm8gc2Fp',
'IGNhIG1vdCBiYWMgZG8gbG9uLgojIENobyBuZW46IG5lbiBraG9uZyBjaHVuZyBtaW5oIGR1b2MgbGEgdHVvaSA9PiBLSE9O',
'RyBETyBEVU9DIChyYz0zKSwgS0hPTkcgcGhhaSBUUlVPVC4KIyBUUlVPVCBsYSBtb3QgUEhBTiBRVVlFVCB2ZSBiYW4gdmE7',
'IHBoYW4gcXV5ZXQgY2hpIGR1b2MgcGhlcCBwaGF0IHJhIGtoaSBkYSBkbyBkdW9jLgpyY191LCB1cmxfdGhvLCBfID0gZ2l0',
'KGdvYywgInJlbW90ZSIsICJnZXQtdXJsIiwgIm9yaWdpbiIpCnVybF9vLCB1cmxfaW4gPSBfdXJsX3NhY2godXJsX3Robyks',
'IF91cmxfaW4odXJsX3RobykKZ2hpKCJvcmlnaW5fdXJsIiwgdXJsX2luKTsgaW5uKGYiICBvcmlnaW4gICAgICAgOiB7dXJs',
'X2luIG9yICcoa2hvbmcgZG9jIGR1b2MpJ30iKQp1cmxfb2sgPSAobm90IHJjX3UpIGFuZCB1cmxfby5yc3RyaXAoIi8iKSBp',
'biBVUkxfS0hPX0hPUF9MRQpyY19sciwgb3V0X2xyLCBlcl9sciA9IGdpdChnb2MsICJscy1yZW1vdGUiLCAib3JpZ2luIiwg',
'InJlZnMvaGVhZHMvbWFzdGVyIikgaWYgdXJsX29rIGVsc2UgKDEsICIiLCAiIikKZXJfbHIgPSBfYW5fdXNlcmluZm8oZXJf',
'bHIpCnJjX2xtLCBsbSwgZXJfbG0gICAgID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJvcmlnaW4vbWFzdGVyIikKcm0gPSBv',
'dXRfbHIuc3BsaXQoKVswXSBpZiAobm90IHJjX2xyIGFuZCBvdXRfbHIuc3RyaXAoKSkgZWxzZSAiIgppZiBub3QgdXJsX29r',
'OgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJvcmlnaW49e3VybF9pbiFyfSBLSE9ORyBwaGFpIGtobyB0aGF0',
'IOKAlCAndHVvaScgc28gdm9pIG5vIGtob25nIGNodW5nIG1pbmggZHVvYyBnaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9',
'IDEsICIiLCAiIiwgMQplbGlmIG5vdCBybToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJraG9u',
'ZyBob2kgZHVvYyBtYXN0ZXIgdHJlbiByZW1vdGUgKGxzLXJlbW90ZSByYz17cmNfbHJ9KToge2VyX2xyWzo2MF19ICIKICAg',
'ICAgICBmIuKAlCBraG9uZyBjaHVuZyBtaW5oIGR1b2MgdmUgbmVuIGNvbiB0dW9pIikKICAgIHJjX21iLCBtYiwgbnMsIHJj',
'ID0gMSwgIiIsICIiLCAxCmVsaWYgcmNfbG0gb3Igbm90IGxtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJr',
'aG9uZyBkb2MgZHVvYyBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25lOiB7ZXJfbG1bOjYwXX0iKQogICAgcmNfbWIsIG1iLCBu',
'cywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBsbSAhPSBybToKICAgICMgRGVtIHhlbSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRl',
'bSBkdW9jIOKAlCBjb24gc28gbmF5IG5vaSBybyBtdWMgZG8gc2FpIGxlY2guCiAgICByY19jLCBzYXUsIF8gPSBnaXQoZ29j',
'LCAicmV2LWxpc3QiLCAiLS1jb3VudCIsIGYie2xtfS4ue3JtfSIpCiAgICB4YSA9IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1p',
'dCIgaWYgKG5vdCByY19jIGFuZCBzYXUuc3RyaXAoKS5pc2RpZ2l0KCkpIGVsc2UgIiIKICAgIGlubihmIiAgb3JpZ2luL21h',
'c3RlciB0cm9uZyBjbG9uZSA6IHtsbVs6MTJdfSIpCiAgICBpbm4oZiIgIG1hc3RlciB0cmVuIHJlbW90ZSAgICAgICAgOiB7',
'cm1bOjEyXX17eGF9IikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAg',
'IGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJ2ZSBuZW4gQ1U6IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19',
'ICE9IHJlbW90ZT17cm1bOjEyXX17eGF9ICIKICAgICAgICBmIuKAlCBjaGF5IGBnaXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2lu',
'IG1hc3RlcmAgcm9pIGRvIGxhaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbHNlOgogICAgaW5u',
'KGYiICB2ZSBuZW4gVFVPSTogb3JpZ2luL21hc3RlciA9IHtsbVs6MTJdfSA9PSBtYXN0ZXIgdHJlbiByZW1vdGUiKQogICAg',
'Z2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAgcmNfbWIsIG1iLCBlcl9tYiA9',
'IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIm9yaWdpbi9tYXN0ZXIiLCBoZWFkKQppZiByY19tYiBvciBub3QgbWI6CiAgICBp',
'ZiBtYiA9PSAiIiBhbmQgcm0gYW5kIGxtID09IHJtOgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hv',
'bmcgdGluaCBkdW9jIG1lcmdlLWJhc2Ugdm9pIG9yaWdpbi9tYXN0ZXI6IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAi',
'IiwgMQplbHNlOgogICAgZ2hpKCJtZXJnZV9iYXNlIiwgbWIpCiAgICBpbm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3Rl',
'ciwgSEVBRCkgPSB7bWJbOjEyXX0iKQogICAgaWYgbWIgIT0gU0hBX0JBU0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZ',
'OiBraGFjIGJhc2UgbWEgc3BlYyByMyBraGFpICh7U0hBX0JBU0VfU1BFQ1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdl',
'IG1hc3Rlci4iKQogICAgICAgIGlubigiICAgICAgICAgRG8gc28gYmFzZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcg',
'dmFvLiBEdW5nIG1lcmdlLWJhc2UgbW9pIGxhIHZpZWMgY3VhIGV4ZWN1dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9',
'IGdpdChnb2MsICJkaWZmIiwgIi0tbnVtc3RhdCIsIFNIQV9CQVNFX1NQRUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6',
'CiAgICAgICAgICAgIGggPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBuc194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCld',
'CiAgICAgICAgICAgIGEgPSBzdW0oaW50KHhbMF0pIGZvciB4IGluIGggaWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAg',
'IGdoaSgibnVtc3RhdF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVwIjogbGVuKGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBp',
'bm4oZiIgICAgICAgICAoZG9pIGNoaWV1OiBzbyBiYXNlIHNwZWMgPSB7bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28g',
'YXkgS0hPTkcgZHVuZyBkZSBjaGFtKSIpCiAgICByYywgbnMsIGVyID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0Iiwg',
'bWIsIGhlYWQpCmlmIHJjOgogICAgcGFzcwplbHNlOgogICAgaGFuZyA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNw',
'bGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICB0aGVtID0gc3VtKGludChoWzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0u',
'aXNkaWdpdCgpKQogICAgeG9hICA9IHN1bShpbnQoaFsxXSkgZm9yIGggaW4gaGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAg',
'IGdoaSgic29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hpKCJkb25nX3RoZW0iLCB0aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkK',
'ICAgIGZvciBoIGluIGhhbmc6IGlubihmIiAgICB7aFsyXTozNH0gK3toWzBdOjw1fSAte2hbMV19IikKICAgIGlubihmIiAg',
'ICBUT05HOiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17eG9hfSAgICh0cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFO',
'X0RPTkd9IGRvbmcgdGhlbSkiKQogICAgY2hhbSA9IHNvcnRlZCh7aFsyXSBmb3IgaCBpbiBoYW5nfSAmIFdSSVRFX1NFVF9H',
'Mik7IGdoaSgiY2hhbV93cml0ZV9zZXQiLCBjaGFtKQogICAgZGVmIF9jYV9tb2lfY28ocmV2KToKICAgICAgICByXywgbmRf',
'LCBfID0gZ2l0KGdvYywgInNob3ciLCBmIntyZXZ9Om9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIHJldHVy',
'biBOb25lIGlmIHJfIGVsc2Uge3QgZm9yIHQgaW4gQ0FfTU9JX0cyIGlmIHJlLnNlYXJjaChyIig/bSleZGVmICIgKyB0ICsg',
'ciJbYS16XT9fIiwgbmRfKX0KICAgIG9fbWIsIG9faCA9IF9jYV9tb2lfY28obWIpLCBfY2FfbW9pX2NvKGhlYWQpCiAgICBt',
'YW5nID0gc29ydGVkKG9faCAtIG9fbWIsIGtleT1zb19jYSkgaWYgKG9fbWIgaXMgbm90IE5vbmUgYW5kIG9faCBpcyBub3Qg',
'Tm9uZSkgZWxzZSBOb25lCiAgICBnaGkoImNhX21vaV9nMl9tYW5nX3ZhbyIsIG1hbmcpCiAgICBpZiBub3QgbWFuZzoKICAg',
'ICAgICAjIERvIFJPTkcgKGRhIGxhbmQsIGNoaW5oIG1hc3RlciksIG5oYW0gbmhhbmgsIGhheSBuaGFuaCBjdWEgcGFja2V0',
'IEtIQUMgY2hhbSBjdW5nIHRlcDoKICAgICAgICAjIGtob25nIG1hbmcgY2EgbW9pIG5hbyBjdWEgZzIgdGhpIGtob25nIHBo',
'YWkgdW5nIHZpZW4uIERvYyBraG9uZyBkdW9jIChOb25lKSBjdW5nIHZheS4KICAgICAgICBrZXQoIk43JyBraWNoIHRodW9j',
'IiwgS0RELCBmImRvaSB0dW9uZyBraG9uZyBwaGFpIHVuZyB2aWVuOiB7bGVuKGhhbmcpfSB0ZXAsIGNoYW0ge2NoYW19LCBj',
'YSBtb2kgIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiZzIgbWFuZyB2YW8ge21hbmchcn0g4oCUIGRh',
'IGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPyIpCiAgICBlbHNlOgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2Mi',
'LCBEQVQgaWYgKGxlbihoYW5nKSA8PSBUUkFOX1RFUCBhbmQgdGhlbSA8PSBUUkFOX0RPTkcpIGVsc2UgVFJVT1QsCiAgICAg',
'ICAgICAgIGYie2xlbihoYW5nKX0gdGVwIC8gK3t0aGVtfSIpCgojIERpbmggZGFuaCBUSEFUIG5hbSBvIE43JyAoY2EgbW9p',
'IGcyIG1hbmcgdmFvKSwgS0hPTkcgbyAiaGF1IGR1ZSBnMSI6IGcxIGRhIGxhbmQgbmVuIG1vaSBuaGFuaCBkZXUKIyBsYSBo',
'YXUgZHVlLiBEb25nIGRhdSBraG9pIGRhbiBwaGFpIHR1IGtoYWkgdGhlbyBrZXQgcXVhIGF5IChkbyBkdW9jOiBtYXN0ZXIg',
'NDQ2MjBlOCBtbyBraG9pIGJhbmcKIyAiVEhFIEhFIERPIERVT0M6IGcyIiwgSlNPTiAidGhlX2hlIjogImcyIiwgdHJvbmcg',
'a2hpIE43JyBkYSBrZXQgbHVhbiAia2hvbmcgcGhhaSB1bmcgdmllbiIpLgojIE5oYW4gY2hpIGR1b2Mgbm9pIERVTkcgY2Fp',
'IGRvIGR1b2M6IGBbXWAga2hvbmcgdGFjaCAiZGEgbGFuZCIga2hvaSAibmhhbSBuaGFuaCIvInBhY2tldCBraGFjIiAoZG8K',
'IyBkdW9jIHRyZW4gMjAyNi0wOS0zMGI6IHVuZyB2aWVuIDJhNjc5NjggREEgTEFORCBiaSBnb2kgIktIT05HIHBoYWkgdW5n',
'IHZpZW4gZzIiKS4KaWYgdGhlX2hlID09ICJnMiIgYW5kIG5vdCBzby5nZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpOgogICAg',
'dGhlX2hlID0gKCJLSE9ORyBtYW5nIGNhIG1vaSBnMiBuYW8gKGRhIGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPyki',
'IGlmIHNvLmdldCgiY2FfbW9pX2cyX21hbmdfdmFvIikgPT0gW10KICAgICAgICAgICAgICBlbHNlICJnMj8gKENIVUEgZGlu',
'aCBkYW5oIGR1b2MgZG9pIHR1b25nKSIpCiAgICBnaGkoInRoZV9oZSIsIHRoZV9oZSkKCiMgQ29uZyBuaGFuaDogZG8gUklF',
'Tkcga2ljaCB0aHVvYyAodmFpIGdpYXkpIHJvaSBkdW5nLiBEdW5nIGtoaSBjYW4geGFjIG1pbmggbGFpCiMgdmUgbmVuIG1h',
'IGtob25nIG11b24gdHJhIDIwLTQ1IHBodXQgY2hvIGNhIGJvIHRlc3QuCmlmICItLWNoaS1raWNoLXRodW9jIiBpbiBzeXMu',
'YXJndjoKICAgIGlubigiIik7IGlubigiPSIgKiA3OCkKICAgIGlubigiLS1jaGkta2ljaC10aHVvYzogQ0hJIGRvIGNvbmcg',
'a2ljaCB0aHVvYy4gRGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQogICAgaW5uKCItIiAqIDc4KQogICAg',
'Zm9yIF90LCBfdHQsIF9jdCBpbiBjaG90OiBpbm4oZiIgIHtfdHQ6MTR9IHtfdH0iICsgKGYiICAge19jdH0iIGlmIF9jdCBl',
'bHNlICIiKSkKICAgIF9rID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKICAgIF9yID0gc3VtKDEg',
'Zm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQogICAgc3lzLmV4aXQoMyBpZiBfayBlbHNlICgxIGlmIF9yIGVs',
'c2UgMCkpCgpDSElfUFJPQkUgPSAiLS1jaGktcHJvYmUiIGluIHN5cy5hcmd2ICAgICMgYm8gcXVhIGJvIHRlc3QgKyBONzsg',
'Z2l1IDAsIDEsIDMKIyAtLS0tLS0tLS0tLS0tLS0tIDIuIGJvIHRlc3QgZGF5IGR1IC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90',
'IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMi4gQk8gVEVTVCBEQVkgRFUgKDEwLTQwIHBo',
'dXQpIikKICAgIHJjX24sIG91dF9uID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgZ29jKQogICAgZ2hp',
'KCJyY19zdWl0ZSIsIHJjX24pCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0X24pCiAgICBpbm4oIiAgcmMgPSIsIHJjX24s',
'ICJ8IiwgbS5ncm91cCgwKSBpZiBtIGVsc2UgIihLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcga2V0KSIpCiAgICBpZiBtOgog',
'ICAgICAgIGdoaSgiZGF0IiwgaW50KG0uZ3JvdXAoMSkpKTsgZ2hpKCJ0cmVuIiwgaW50KG0uZ3JvdXAoMikpKTsgZ2hpKCJi',
'b19xdWFfc28iLCBpbnQobS5ncm91cCg0KSkpCiAgICBkb19oZXQsIGdjLCB0aW4gPSBkb2NfZG8ob3V0X24pCiAgICBnaGko',
'InNvX2NhX2RvIiwgbGVuKGRvX2hldCkpOyBnaGkoImxpZXRfa2VfZGF5X2R1IiwgdGluKQogICAgZm9yIGcgaW4gZ2M6IGlu',
'bigiICAgKiIsIGcpCiAgICBpbm4oIiIpOyBpbm4oZiIgID09PSB7bGVuKGRvX2hldCl9IENBIERPID09PSIpCiAgICBmb3Ig',
'dCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGlubihmIiAgIHt0LnNwbGl0KCdfJylbMF06N30ge3R9',
'Iik7IGlubihmIiAgICAgICAgICAge2RvX2hldFt0XVs6MTUwXX0iKQogICAgZ2hpKCJkb19seV9kbyIsIHt0OiBkb19oZXRb',
'dF1bOjMwMF0gZm9yIHQgaW4gZG9faGV0fSkKICAgICMgLS0tLSBDSE9UOiBtb2kgY2EgRE8gcGhhaSBHSUFJIFRISUNIIERV',
'T0MgLS0tLQogICAgIyBUaGlldSBjaG90IG5heSwgYm8gZG8gaW4gZGFuaCBzYWNoIGRvIHJvaSB2YW4gdGhvYXQgcmM9MC4g',
'RG8gZHVuZyBsYSBsb2kgZGEgeGF5IHJhOgogICAgIyBsdW90IFdpbmRvd3MgMTktMDkgY28gdDE3MSBETyBtYSBibyBkbyBi',
'YW8gIkRBVCAxMCB8IFRSVU9UIDAiIHZhIHJjPTAuCiAgICBkZWYgX2tob2EodCk6IHJldHVybiB0LnNwbGl0KCJfIilbMF0K',
'ICAgIGRvX3BhY2tldCwgZG9fbGEsIGRvX3RoaWV1X2NvbmdfY3UgPSBbXSwgW10sIFtdCiAgICBmb3IgdCBpbiBzb3J0ZWQo',
'ZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGssIGx5ID0gX2tob2EodCksIGRvX2hldFt0XQogICAgICAgIGlmIGsgaW4g',
'Q0FfUEFDS0VUOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRvX3BhY2tldC5hcHBlbmQodCkKICAgICAgICBlbGlm',
'ICJLSMOUTkcgxJBPIMSQxq/hu6JDIiBpbiBseSBvciAidGhp4bq/dSBgIiBpbiBseTogIGRvX3RoaWV1X2NvbmdfY3UuYXBw',
'ZW5kKHQpCiAgICAgICAgZWxpZiBrIGluIE5HT0FJX1BIQU1fVkk6ICAgICAgICAgICAgICAgICAgICAgICAgcGFzcwogICAg',
'ICAgIGVsc2U6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRvX2xhLmFwcGVuZCh0KQogICAg',
'Z2hpKCJkb19wYWNrZXQiLCBkb19wYWNrZXQpOyBnaGkoImRvX2xhIiwgZG9fbGEpOyBnaGkoImRvX3RoaWV1X2NvbmdfY3Ui',
'LCBkb190aGlldV9jb25nX2N1KQogICAgaW5uKCIiKQogICAgaW5uKGYiICBjYSBETyB0aHVvYyBDSElOSCBwYWNrZXQgbmF5',
'IDoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdIG9yICdraG9uZyBjbyd9IikKICAgIGlubihmIiAgY2EgRE8gbmdv',
'YWkgcGhhbSB2aSAocjMga2hhaSk6IHtbX2tob2EoeCkgZm9yIHggaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKSBpZiBf',
'a2hvYSh4KSBpbiBOR09BSV9QSEFNX1ZJXX0iKQogICAgaW5uKGYiICBjYSBETyB2aSBUSElFVSBDT05HIENVICAgICAgIDog',
'e1tfa2hvYSh4KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XSBvciAna2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERP',
'IExBIChraG9uZyBnaWFpIHRoaWNoIGR1b2MpOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXSBvciAna2hvbmcgY28nfSIp',
'CiAgICAjIC0tLS0gQ0hPVDogcGhlcCBkbyBwaGFpIFRST04gdHJ1b2Mga2hpIG1vdCBjaHUgREFUIG5hbyBkdW9jIHBoYXQg',
'LS0tLQogICAgIyBCYW4gdHJ1b2MgY2hpIElOIGB0aW5gL2ByY19zdWl0ZWA6IGJvIHRlc3QgY2hldCBnaXVhIHQxNzEgKHJj',
'PTEzNCwga2hvbmcgZG9uZyB0b25nKQogICAgIyB2YW4gcmEgIkRBVCAxMiB8IFRSVU9UIDAiIHJjPTA7IGNhIFBBQ0tFVCB2',
'YW5nIG1hdCBoYXkgYmkgQk8gUVVBIGN1bmcgZHVvYyBjaGFtIG5odQogICAgIyAia2hvbmcgZG8iLiBWYW5nIG1hdCBraG9u',
'ZyBwaGFpICJraG9uZyBkbyIg4oCUIGxhIEtIT05HIERPIERVT0MuCiAgICB2YW5nID0gW3QgZm9yIHQgaW4gc29ydGVkKENB',
'X1BBQ0tFVCwga2V5PXNvX2NhKSBpZiBtYXVfY2Eob3V0X24sIHQpIG5vdCBpbiAoIlFVQSIsICJETyIpXQogICAgbHlfa2Rk',
'ID0gW10KICAgIGlmIG5vdCB0aW46IGx5X2tkZC5hcHBlbmQoImRhbmggc2FjaCBkbyBLSE9ORyBkYXkgZHUiKQogICAgaWYg',
'cmNfbiBub3QgaW4gKDAsIDEpIG9yIChyY19uID09IDEpICE9IGJvb2woZG9faGV0KToKICAgICAgICBseV9rZGQuYXBwZW5k',
'KGYicmMgYm8gdGVzdD17cmNfbn0ga2hvbmcga2hvcCB7bGVuKGRvX2hldCl9IGNhIERPIGRvYyBkdW9jIikKICAgIGlmIHZh',
'bmc6IGx5X2tkZC5hcHBlbmQoZiJjYSBQQUNLRVQgdmFuZy9ibyBxdWE6IHt2YW5nfSIpCiAgICBnaGkoImNhX3BhY2tldF92',
'YW5nIiwgdmFuZyk7IGdoaSgibHlfZG9fY2h1YV90cm9uIiwgbHlfa2RkKQogICAgaWYgbHlfa2RkOiBrZXQoIkJvIHRlc3Qg',
'Y2hheSBUUk9OIHZhIGRvYyBEVSIsIEtERCwgIjsgIi5qb2luKGx5X2tkZCkpCiAgICBjaHVhX3Ryb24gPSBLREQgaWYgbHlf',
'a2RkIGVsc2UgREFUCiAgICBrZXQoIktob25nIGNhIG5hbyBjdWEgUEFDS0VUIGJpIERPIiwgY2h1YV90cm9uIGlmIG5vdCBk',
'b19wYWNrZXQgZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9fcGFja2V0IGVsc2UgZiJETzoge1tfa2hvYSh4KSBm',
'b3IgeCBpbiBkb19wYWNrZXRdfSDigJQgYmFuIHZhIENIVUEgeG9uZyIpCiAgICBrZXQoIk1vaSBjYSBETyBkZXUgZ2lhaSB0',
'aGljaCBkdW9jIiwgY2h1YV90cm9uIGlmIG5vdCBkb19sYSBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19sYSBl',
'bHNlIGYibGE6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdfSIpCiAgICBpZiBkb190aGlldV9jb25nX2N1OgogICAgICAg',
'IGtldCgiQ29uZyBjdSBkYXkgZHUgZGUgZG8iLCBLREQsIGYidGhpZXUgY29uZyBjdSBjaG8ge1tfa2hvYSh4KSBmb3IgeCBp',
'biBkb190aGlldV9jb25nX2N1XX0iKQoKICAgIGJxID0gc29ydGVkKHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxs',
'KG91dF9uKX0sIGtleT1zb19jYSk7IGdoaSgiY2FfYm9fcXVhIiwgYnEpCiAgICBpbm4oIiIpOyBpbm4oZiIgIEJPIFFVQSAo',
'e2xlbihicSl9KToge1t4LnNwbGl0KCdfJylbMF0gZm9yIHggaW4gYnFdfSIpCgogICAgaW5uKCIiKTsgaW5uKCIgIE4xLU40',
'ICh0MTY1LXQxNjgpLCB0aWV1IGNoaSBuZ2hpZW0gdGh1IGN1YSByMiwgbmF5IGxhIGNoaSBiYW8gaG9pIHF1eToiKQogICAg',
'YjQgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQU1PSX07IGdoaSgiY2FfbW9pIiwgYjQpCiAgICBmb3IgdCBp',
'biBDQU1PSTogaW5uKGYiICAgICB7dH06IHtiNFt0XX0iKQogICAgIyBCT19RVUEvdmFuZyBsYSBDSFVBIENIQVksIGtob25n',
'IHBoYWkgRE86IGNoaSBtb3QgY2EgRE8gbW9pIGR1b2MgcGhhdCBUUlVPVC4KICAgIGtldCgiTjEtTjQgKHQxNjUtdDE2OCki',
'LCBEQVQgaWYgYWxsKHYgPT0gIlFVQSIgZm9yIHYgaW4gYjQudmFsdWVzKCkpCiAgICAgICAgZWxzZSAoVFJVT1QgaWYgYW55',
'KHYgPT0gIkRPIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkgZWxzZSBLREQpLCBzdHIoYjQpKQoKICAgIGlubigiIik7IGlubigi',
'ICAxNSBjYSB0dW5nIGRvIHRyZW4gQ0k6IikKICAgIGIxNSA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBMTV9',
'OyBnaGkoImNhMTUiLCBiMTUpCiAgICBpbm4oIiAgICAiICsgIiAgIi5qb2luKGYie3R9OntiMTVbdF19IiBmb3IgdCBpbiBD',
'QTE1KSkKCiAgICAjIHQxMzYg4oCUIE4xMiBkbyBHSUFOIFRJRVAgcXVhIGtldCBxdWEgY2EKICAgIHQxMzZfdGVuID0gbmV4',
'dCgodCBmb3IgdCBpbiBkb19oZXQgaWYgdC5zdGFydHN3aXRoKCJ0MTM2IikpLCBOb25lKQogICAgaWYgYjE1LmdldCgidDEz',
'NiIpID09ICJRVUEiOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIERBVCwgInQxMzYgUVVBIikK',
'ICAgIGVsaWYgYjE1LmdldCgidDEzNiIpICE9ICJETyI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2Ep',
'IiwgS0RELCBmInQxMzYgPSB7YjE1LmdldCgndDEzNicpIXJ9IOKAlCBraG9uZyBjaGF5L2tob25nIHRoYXkiKQogICAgZWxz',
'ZToKICAgICAgICBseSA9IGRvX2hldC5nZXQodDEzNl90ZW4sICIiKQogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQg',
'cXVhIGNhKSIsIFRSVU9ULCBmIkRPOiB7bHlbOjkwXX0iKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDMuIHByb2JlIFRIQU5HIHZh',
'byBoYW0gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjMuIFBST0JFIFRIQU5HIOKAlCBn',
'b2kgX2dpdF93aW5kb3dzIHZvaSB0aGFtIHNvIHRpZW0iKQpzcGVjID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVf',
'bG9jYXRpb24oImxwNTQxIiwgc3RyKHRlcCkpCmxwID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhzcGVjKTsg',
'c3BlYy5sb2FkZXIuZXhlY19tb2R1bGUobHApCnNpZyA9IGluc3BlY3Quc2lnbmF0dXJlKGxwLl9naXRfd2luZG93cykKZ2hp',
'KCJ0aGFtX3NvX19naXRfd2luZG93cyIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQppbm4oIiAgdGhhbSBzbyBjdWEgX2dpdF93',
'aW5kb3dzOiIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQoKZGVmIGdvaSgqKmt3KToKICAgICIiIkdvaSBfZ2l0X3dpbmRvd3Ms',
'IEJBVCBzdGRlcnIgZGUgbW90IGRvbmcgY2hhbiBkb2FuIGtob25nIGdpZXQgbHVvdCBkby4iIiIKICAgIGUgPSBpby5TdHJp',
'bmdJTygpCiAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgogICAgICAgIHIgPSBscC5fZ2l0X3dpbmRv',
'd3MoKiprdykKICAgIHJldHVybiByLCBlLmdldHZhbHVlKCkKCiMgLS0tIGRvaSBjaHVuZyByaWc6IHBoYWkgdHJhIGxvaSBk',
'dW5nIG1vdCBjYSB0YSBCSUVUIFRSVU9DIGRhcCBhbiAtLS0Kd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBh',
'cyB0OgogICAgbmdvYWkgPSBQYXRoKHQpLyJuZ29haSI7IG5nb2FpLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cu',
'bWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIChuZ29haS8iZ2l0LmV4ZSIpLndyaXRlX3RleHQo',
'IngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjEsIF8gPSBnb2kocGF0aD1zdHIobmdvYWkpLCBwcm9ncmFtX2ZpbGVzPXN0',
'cihwZiksIGN3ZD1zdHIoY3cpKQogICAgKGN3LyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIp',
'CiAgICByMiwgXyA9IGdvaShwYXRoPXN0cihjdyksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCnJpZ19v',
'ayA9IGJvb2wocjEpIGFuZCByMiBpcyBOb25lCmdoaSgicmlnX2RvaV9jaHVuZyIsIHJpZ19vaykKa2V0KCJSSUcgZG9pIGNo',
'dW5nIChiaWV0IHRydW9jIGRhcCBhbikiLCBEQVQgaWYgcmlnX29rIGVsc2UgS0RELAogICAgZiJuZ29haS1jd2QtPnsnTkhB',
'TicgaWYgcjEgZWxzZSAnTm9uZSd9IHwgdHJvbmctY3dkLT57J05IQU4nIGlmIHIyIGVsc2UgJ05vbmUnfSIpCmlmIG5vdCBy',
'aWdfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IHJpZyBzYWksIG1vaSBjaG90IGR1b2kgc2Ugdm8gbmdo',
'aWEuIik7IHN5cy5leGl0KDMpCgojIC0tLSBNT0kgQ09ORyBQSEFJIFRVIENIVU5HIE1JTkggTk8gQ08gVEhFIERPIC0tLQoj',
'IEJhaSBob2MgZGF0IG5oYXQgY3VhIHBhY2tldCBuYXk6IGRvX24xMCBiYW4gY3UgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRy',
'b25nIGtoaSB0MTcxCiMgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQgbWEgTjEwIHNpbmggcmEg',
'ZGUgYmF0LiBObyBkZWdlbmVyYXRlIOKAlAojIHRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyBuZW4gInRhY2gg',
'ZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gY3VuZyBrZXQgcXVhLgojIE1vdCBjb25nIGtob25nIHRoZSBETyB0aGkga2hvbmcg',
'cGhhaSBjb25nLCB2YSBubyBuZ3V5IGhpZW0gaG9uIGtob25nIGNvIGNvbmc6IG5vCiMgcGhhdCByYSBtb3QgY2h1IERBVC4K',
'IwojIE5lbiB0cnVvYyBraGkgRFVORyBuYW0gY29uZyBuYXkgZGUgcGhhbiBxdXlldCwgYmF0IHR1bmcgY29uZyBnaWV0IG1v',
'dCBkb3QgYmllbiBkYQojIGJpZXQgdHJvbmcuIENvbmcgbmFvIGtob25nIGdpZXQgZHVvYyB0aGkgY2h1IERBVCBjdWEgbm8g',
'YmkgSEEgeHVvbmcgS0hPTkcgRE8gRFVPQzsKIyBUUlVPVCBnaXUgbmd1eWVuIChxdWFuIHNhdCB0cnVjIHRpZXAsIHZkLiBn',
'MSB2YW4gbmhhbiBnaXQuYmF0KS4gRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaQoj',
'IGR1bmcgdG9pIChjdW5nIGt5IGx1YXQgbmh1IE43KS4KRE9UX0JJRU5fVFVfS0lFTSA9IFsKICAgICgiTjgiLCAib3BzL2xl',
'YXNlX3B1Ymxpc2gucHkiLAogICAgICdpZiBjaGlfZGluaCBhbmQgUGF0aChjaGlfZGluaCkubmFtZS5sb3dlcigpID09ICJn',
'aXQuZXhlIiBhbmQgaG9wX2xlKGNoaV9kaW5oKTonLAogICAgICJpZiBjaGlfZGluaCBhbmQgaG9wX2xlKGNoaV9kaW5oKToi',
'KSwKICAgICgiTjkiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJkID0gZF9yYXcuc3RyaXAoKS5zdHJpcCgnXCIn',
'KSIsICJkID0gZF9yYXcuc3RyaXAoKSIpLAogICAgKCJOMTAiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJzZXAg',
'PSBvcy5wYXRoc2VwIGlmIHBoYW5fY2FjaCBpcyBOb25lIGVsc2UgcGhhbl9jYWNoIiwgInNlcCA9IG9zLnBhdGhzZXAiKSwK',
'ICAgICgiTjExIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwgImlmIGNoYW5fZG9hbiBpcyBub3QgTm9uZToiLCAiaWYgRmFs',
'c2U6IiksCiAgICAoIk4xMiIsICJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IiwKICAgICAnZ2l0X3BhdGg9Ii8va2hvbmct',
'Y28vZ2l0IicsICdnaXRfcGF0aD0iL2tob25nLWNvL2dpdCInKSwKXQppbm4oIiIpOyBpbm4oIiAgdHUga2llbSBjb25nIOKA',
'lCBtb2kgY29uZyBwaGFpIGdpZXQgZHVvYyBtb3QgZG90IGJpZW4gZGEgYmlldDoiKQpnaWV0ID0ge30KZm9yIG1hLCBkdW9u',
'ZywgdGltLCB0aGF5IGluIERPVF9CSUVOX1RVX0tJRU06CiAgICBfdGVuLCBfaGFtID0gbmV4dCgoKGEsIGIpIGZvciBhLCBi',
'IGluIFBST0JFIGlmIGEuc3RhcnRzd2l0aChtYSArICIgIikpLCAoTm9uZSwgTm9uZSkpCiAgICBpZiBfaGFtIGlzIE5vbmU6',
'CiAgICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IGtob25nIHRpbSB0aGF5',
'IHByb2JlIHRlbiAne21hfSAuLi4nIik7IGNvbnRpbnVlCiAgICB0cnk6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3Jh',
'cnlEaXJlY3RvcnkoKSBhcyBfdDoKICAgICAgICAgICAgX2MgPSBQYXRoKF90KS8iY2F5Ijsgc2h1dGlsLmNvcHl0cmVlKGdv',
'Yy8ib3BzIiwgX2MvIm9wcyIpCiAgICAgICAgICAgIF9mID0gX2MvZHVvbmc7IF9uZCA9IF9mLnJlYWRfdGV4dChlbmNvZGlu',
'Zz0idXRmLTgiKQogICAgICAgICAgICBpZiBfbmQuY291bnQodGltKSAhPSAxOgogICAgICAgICAgICAgICAgZ2lldFttYV0g',
'PSBOb25lCiAgICAgICAgICAgICAgICBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IG1hdSBkb3QgYmllbiBraG9w',
'IHtfbmQuY291bnQodGltKX0gbGFuIChtb25nIDEpIgogICAgICAgICAgICAgICAgICAgIGYiIOKAlCBtYSBuZ3VvbiBkYSBk',
'b2ksIGRvdCBiaWVuIG5heSBoZXQgeSBuZ2hpYSIpOyBjb250aW51ZQogICAgICAgICAgICBfZi53cml0ZV90ZXh0KF9uZC5y',
'ZXBsYWNlKHRpbSwgdGhheSwgMSksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIF9zcCA9IGltcG9ydGxpYi51dGls',
'LnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF9kYl8iICsgbWEsIHN0cihfYy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIp',
'KQogICAgICAgICAgICBfbSA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVj',
'X21vZHVsZShfbSkKICAgICAgICAgICAgZGVmIF9nb2lfZGIoKiprdyk6CiAgICAgICAgICAgICAgICBfZSA9IGlvLlN0cmlu',
'Z0lPKCkKICAgICAgICAgICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoX2UpOgogICAgICAgICAgICAg',
'ICAgICAgIHJldHVybiBfbS5fZ2l0X3dpbmRvd3MoKiprdyksIF9lLmdldHZhbHVlKCkKICAgICAgICAgICAgX3R0LCBfY3Qs',
'IF8gPSBfaGFtKF9nb2lfZGIsIGluc3BlY3Quc2lnbmF0dXJlKF9tLl9naXRfd2luZG93cyksCiAgICAgICAgICAgICAgICAg',
'ICAgICAgICAgICAgICBfYy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBnaWV0W21hXSA9IChfdHQg',
'PT0gVFJVT1QpCiAgICAgICAgaW5uKGYiICAgIHttYTo0fSBkb3QgYmllbiAtPiB7X3R0OjE0fSB7J0dJRVQgRFVPQycgaWYg',
'X3R0ID09IFRSVU9UIGVsc2UgJ1NPTkcgU09UJ30iCiAgICAgICAgICAgICsgKGYiICAgKHtfY3R9KSIgaWYgX2N0IGVsc2Ug',
'IiIpKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6',
'NH0gS0hPTkcgRE8gRFVPQzoge3R5cGUoX2UpLl9fbmFtZV9ffToge19lfSIpCmdoaSgiY29uZ19naWV0X2R1b2NfZG90X2Jp',
'ZW4iLCBnaWV0KQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwpIGluIFsodCwgZihnb2ksIHNpZywgdGVwdCkpIGZvciB0LCBmIGlu',
'IFBST0JFXToKICAgIGdoaSgicHJvYmVfIiArIHRlbi5zcGxpdCgpWzBdLmxvd2VyKCksIGRsKQogICAgaWYgaXNpbnN0YW5j',
'ZShkbCwgZGljdCk6CiAgICAgICAgZm9yIGssIHYgaW4gZGwuaXRlbXMoKTogaW5uKGYiICAgIHtrOjM0fToge3Z9IikKICAg',
'IG1hID0gdGVuLnNwbGl0KClbMF0KICAgIGlmIGdpZXQuZ2V0KG1hKSBpcyBub3QgVHJ1ZSBhbmQgdHQgPT0gREFUOgogICAg',
'ICAgICMgREFUIHR1IG1vdCBjb25nIGNodWEgY2h1bmcgbWluaCBkdW9jIGxhIGJpZXQgRE8gdGhpIGtob25nIGRhbmcgdGlu',
'IGhvbiBLREQuCiAgICAgICAga2V0KHRlbiwgS0RELCBmImNvbmcgS0hPTkcgZ2lldCBkdW9jIGRvdCBiaWVuIGN1YSBjaGlu',
'aCBubyAoe2dpZXQuZ2V0KG1hKSFyfSkiCiAgICAgICAgICAgICAgICAgICAgICBmIiAtPiBjaHUgREFUIG5heSBraG9uZyBj',
'byBnaWEgdHJpIikKICAgIGVsc2U6CiAgICAgICAga2V0KHRlbiwgdHQsIGN0KQoKIyAtLS0tLS0tLS0tLS0tLS0tIDQuIE43',
'IGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gLS0tLS0tLS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIi',
'KTsgaW5uKCItIiAqIDc4KTsgaW5uKCI0LiBONyDigJQgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAoY2F5IHRoYXQgS0hP',
'TkcgYmkgZHVuZyB0b2kpIikKICAgIHRydW9jID0gdGVwLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVf',
'V0lOKQogICAgZ2hpKCJuN190cnVvYyIsIHRydW9jKTsgaW5uKGYiICBzbyBkb25nIGtob3Age01BVV9XSU4hcn06IFRSVU9D',
'ID0ge3RydW9jfSBbbW9uZyAxXSIpCiAgICBpZiB0cnVvYyAhPSAxOgogICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmgg',
'V2luZG93cyIsIEtERCwgZiJtYXUgeHVhdCBoaWVuIHt0cnVvY30gbGFuLCBraG9uZyBwaGFpIDEiKQogICAgZWxzZToKICAg',
'ICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHRtcDoKICAgICAgICAgICAgc2FvID0gUGF0aCh0',
'bXApLyJjYXkiCiAgICAgICAgICAgIHNodXRpbC5jb3B5dHJlZShnb2MsIHNhbywgaWdub3JlPXNodXRpbC5pZ25vcmVfcGF0',
'dGVybnMoIi5naXQiLCAiX19weWNhY2hlX18iLCAiKi5weWMiKSkKICAgICAgICAgICAgZjIgPSBzYW8vIm9wcyIvImxlYXNl',
'X3B1Ymxpc2gucHkiCiAgICAgICAgICAgIGYyLndyaXRlX3RleHQoZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJl',
'cGxhY2UoTUFVX1dJTiwgImlmIEZhbHNlOiIpLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBzYXUgPSBmMi5yZWFk',
'X3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTik7IGdoaSgibjdfc2F1Iiwgc2F1KQogICAgICAgICAgICBp',
'bm4oZiIgIFNBVSAoZGEgZG90IGJpZW4pID0ge3NhdX0gW21vbmcgMF0iKQogICAgICAgICAgICBpZiBzYXUgIT0gMDoKICAg',
'ICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgImRvdCBiaWVuIEtIT05HIGFwIGR1',
'b2MiKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmNfbSwgb3V0X20gPSBjaGF5KFsib3BzL2xlYXNlX3B1',
'Ymxpc2hfdGVzdC5weSJdLCBzYW8pCiAgICAgICAgICAgICAgICBtMTY1ID0gbWF1X2NhKG91dF9tLCAidDE2NSIpOyBkbSwg',
'XywgXyA9IGRvY19kbyhvdXRfbSkKICAgICAgICAgICAgICAgIHRlbjE2NSA9IG5leHQoKHQgZm9yIHQgaW4gZG0gaWYgdC5z',
'dGFydHN3aXRoKCJ0MTY1IikpLCBOb25lKQogICAgICAgICAgICAgICAgbHkgPSAoZG0uZ2V0KHRlbjE2NSkgb3IgIiIpCiAg',
'ICAgICAgICAgICAgICBnaGkoIm43X3QxNjUiLCBtMTY1KTsgZ2hpKCJuN19seV9kbyIsIGx5WzoyMDBdKQogICAgICAgICAg',
'ICAgICAgaW5uKGYiICB0MTY1IHNhdSBkb3QgYmllbjoge20xNjV9IHwge2x5WzoxMTBdfSIpCiAgICAgICAgICAgICAgICBk',
'dW5nX2x5X2RvID0gIlBBVEggdCIgaW4gbHkgb3IgIi91c3IvYmluIiBpbiBseQogICAgICAgICAgICAgICAga2V0KCJONyBk',
'b3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgREFUIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pIGVsc2UKICAgICAg',
'ICAgICAgICAgICAgICAoVFJVT1QgaWYgbTE2NSA9PSAiRE8iIGVsc2UgS0REKSwKICAgICAgICAgICAgICAgICAgICAiZ2ll',
'dCBkdW5nIGx5IGRvIiBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKQogICAgICAgICAgICAgICAgICAgIGVsc2Ug',
'KCJETyBuaHVuZyBLSE9ORyBkdW5nIGx5IGRvIC0+IHRpbiBkdW5nIGdpYSIgaWYgbTE2NSA9PSAiRE8iIGVsc2UgImtob25n',
'IGRvYyBkdW9jIHQxNjUiKSkKCiMgLS0tLS0tLS0tLS0tLS0tLSBLRVQgTFVBTiAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7',
'IGlubigiPSIgKiA3OCkKaW5uKGYiVEhFIEhFIERPIERVT0M6IHt0aGVfaGV9ICAgSEVBRD17aGVhZFs6MTJdfSIpCiMgS2hv',
'aSBkYW4gY2hvIHJldmlld2VyIGJhdCBkYXUgbyBkb25nIHRyZW4sIG5lbiBDSEUgRE8gcGhhaSBuYW0gTkdBWSBkdW9pIG5v',
'OiBraG9uZyBjbyBkb25nIG5heQojIHRoaSBtb3QgbHVvdCAtLWNoaS1wcm9iZSBpbiAiREFUIDcgfCBUUlVPVCAwIHwgS0hP',
'TkcgRE8gRFVPQyAwIiByYz0wIG1hIGtob25nIG5vaSBsYSBjaHVhIGNoYXkgYm8gdGVzdC4KZ2hpKCJjaGVfZG8iLCAiY2hp',
'LXByb2JlIiBpZiBDSElfUFJPQkUgZWxzZSAiZGF5LWR1IikKaWYgQ0hJX1BST0JFOgogICAgaW5uKCItLWNoaS1wcm9iZTog',
'Q0hJIGRvIG11YyAwLCAxLCAzLiBCbyB0ZXN0LCBOMS1ONCwgdDEzNiwgTjcgS0hPTkcgY2hheSAtIGRheSBLSE9ORyBwaGFp',
'IG1vdCBsdW90IG5naGllbSB0aHUuIikKaWYgdGhlX2hlID09ICJnMSI6CiAgICBpbm4oIkxVVSBZOiBkYXkgbGEgTkVOIERP',
'IChnMSksIEtIT05HIHBoYWkgbmdoaWVtIHRodSBnMi4gQ2FjIGNob3QgTjgtTjEyIGR1b2kgZGF5IikKICAgIGlubigiICAg',
'ICAgIFRSVU9UIGxhIERVTkcgTkhVIE1PTkcg4oCUIGNodW5nIGxhIG5odW5nIGxvIGcyIHNpbmggcmEgZGUgdsOhLiIpCmlu',
'bigiLSIgKiA3OCkKZm9yIHRlbiwgdHQsIGN0IGluIGNob3Q6CiAgICBpbm4oZiIgIHt0dDoxNH0ge3Rlbn0iICsgKGYiICAg',
'e2N0fSIgaWYgY3QgZWxzZSAiIikpCm5fa2RkID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKbl90',
'cnVvdCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKaW5uKCItIiAqIDc4KQppbm4oZiIgIERB',
'VCB7c3VtKDEgZm9yIF8sdCxfIGluIGNob3QgaWYgdD09REFUKX0gfCBUUlVPVCB7bl90cnVvdH0gfCBLSE9ORyBETyBEVU9D',
'IHtuX2tkZH0iKQppbm4oZiIgIFRvbmcgY2EgZG86IHtzby5nZXQoJ3NvX2NhX2RvJyl9IHwgZGFuaCBzYWNoIGRheSBkdTog',
'eydDTycgaWYgc28uZ2V0KCdsaWV0X2tlX2RheV9kdScpIGVsc2UgJ0tIT05HIERPIERVT0MnfSIpCmlubihmIiAgQWRtaW5p',
'c3RyYXRvcjoge3NvLmdldCgncXV5ZW5fYWRtaW4nKX0gfCBzeW1saW5rOiB7c28uZ2V0KCdzeW1saW5rX2R1b2MnKX0iKQpp',
'bm4oIiIpOyBpbm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kgSlNPTiBOQVkgVkUgQ0hPIFJFVklFV0VSIC0tLSIpCmdoaSgiY2hv',
'dCIsIFt7InRlbiI6IGEsICJ0cmFuZ190aGFpIjogYiwgImNoaV90aWV0IjogY30gZm9yIGEsIGIsIGMgaW4gY2hvdF0pCmlu',
'bihqc29uLmR1bXBzKHNvLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0xLCBkZWZhdWx0PXN0cikpCiMgcmM6IDAgPSBt',
'b2kgY2hvdCBEQVQgfCAxID0gY28gY2hvdCBUUlVPVCB8IDMgPSBjbyBjaG90IEtIT05HIERPIERVT0MgKHV1IHRpZW4gYmFv',
'IGRvbmcpCnN5cy5leGl0KDMgaWYgbl9rZGQgZWxzZSAoMSBpZiBuX3RydW90IGVsc2UgMCkpCg=='
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
#   head la hau due   -> CHUA dinh danh: N7' (ca moi g2 mang vao) moi noi ung vien g2 hay khong
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
