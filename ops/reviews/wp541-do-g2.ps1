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
$ShaBoDo    = '831134ce2e97b162b20c7f2a52ec7be12139ef6a868fc3875a6a0123238ba46e'      # SHA-256 cua bo do Python nhung ben duoi

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
$ungVien = @('py','python','python3')
if ($Py) { $ungVien = @($Py) + $ungVien }
foreach ($ten in $ungVien) {
    $c = Get-Command $ten -ErrorAction SilentlyContinue
    if (-not $c) { continue }
    # "CO MAT" khac "DUNG DUOC": py launcher khong co ban nao thi goi la gay.
    # Can Python >= 3.8: bo do can 3.7 (f-string 3.6, capture_output 3.7), bo test cua ung vien dung `:=` (3.8).
    # <= 3.5 / 2.7 thi SyntaxError TRUOC khi excepthook kip dat -> rc=1 = "CO CHOT TRUOT" cho luot CHUA HE CHAY.
    # Doi phien ban bang MA THOAT, KHONG bang `assert`: PYTHONOPTIMIZE=1 xoa assert, probe 30c qua voi mo hinh 3.5
    # roi luot do ra rc=1 "CO CHOT TRUOT" (do tren pwsh 7.4).
    $ok = $true
    try { $thu = & $c.Source -c "import sys;print(sys.version.split()[0]);sys.exit(0 if sys.version_info>=(3,8) else 9)" 2>&1 } catch { $ok = $false; $thu = $_.Exception.Message }
    if ($ok -and $LASTEXITCODE -eq 0) { $pyCmd = $c; break }
    Write-Host "  $($c.Name) co mat nhung khong dung duoc ($thu) -> thu ung vien ke"
}
if (-not $pyCmd) {
    if ($BoQuaTaiCongCu) { Dung 'khong co python dung duoc (va -BoQuaTaiCongCu dang bat)' }
    # Ban nhung KHONG co PyYAML/pip: du cho -ChiKichThuoc/-ChiProbe; luot DAY DU thi bo do tu bao KHONG DO DUOC.
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
'YzJkMmFiYmRkYmI2ZiIKQkFOX0JPX0RPID0gIjIwMjYtMDktMzBkIiAgICAgICAgICAgICAgIyBkb2kgTU9JIGtoaSBzdWEg',
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
'LiBMYW0gc2FjaCBNT0kgVVJMIHRyb25nIHZhbiBiYW4gdHJ1b2Mga2hpIGluLgpkZWYgX2FuX3VzZXJpbmZvKHQpOiByZXR1',
'cm4gcmUuc3ViKHIiKFtBLVphLXpdW0EtWmEtejAtOSsuLV0qOi8vKVteXHMvPyMnXCJdKkAiLCByIlwxIiwgdCBvciAiIikK',
'IyBDYSBuZ29haSBwaGFtIHZpIHIzIMKnbmdvYWlfcGhhbV92aSDigJQgZG8gQ0hJTkggU1BFQyBraGFpLCBraG9uZyBwaGFp',
'IGJvIGRvIHR1IHF1eWV0LgojIERvIGxhIERBTkggU0FDSCBDSE8gUEhFUDogY2EgZG8gbmFvIEtIT05HIG5hbSB0cm9uZyBk',
'YXkgdmEgS0hPTkcgcGhhaSAidGhpZXUgY29uZyBjdSIKIyB0aGkgbGEgVFJVT1QuIERhbmggc2FjaCBjYW0gdGhpIGJhbyBn',
'aW8gY3VuZyB0aGlldTsgZGFuaCBzYWNoIGNobyBwaGVwIHRoaSBiaWV0IHRydW9jLgpOR09BSV9QSEFNX1ZJID0gc2V0KCJ0',
'MTMxIHQxMzIgdDE1MCB0MTI1IHQzNSB0MzYgdDM3IHQzOCB0MzkgdDQwIi5zcGxpdCgpKQojIENhIGN1YSBDSElOSCBwYWNr',
'ZXQgbmF5LiBNb3QgY2EgbyBkYXkgbWEgRE8gdGhpIGtob25nIGJhbyBnaW8gZHVvYyBibyBxdWEuCkNBX1BBQ0tFVCA9IHNl',
'dCgidDE2NSB0MTY2IHQxNjcgdDE2OCB0MTY5IHQxNzAgdDE3MSB0MTcyIHQxNzMiLnNwbGl0KCkpCiMgQ2EgTU9JIG1hIGcy',
'IHRoZW0gdmFvIChOOC1OMTIpLiBEb2kgdHVvbmcgZG8gcGhhaSBNQU5HIGNodW5nIHZhbzogbWVyZ2UtYmFzZSBjaHVhIGNv',
'LCBIRUFEIGNvLgpDQV9NT0lfRzIgPSAidDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpCkNBMTUgID0gInQxMjkg',
'dDEzMCB0MTMxIHQxMzIgdDEzMyB0MTM2IHQxMzggdDEzOSB0MTQ0IHQxNDUgdDE0NiB0MTQ3IHQxNDkgdDE1MCB0MTUxIi5z',
'cGxpdCgpCkNBTU9JID0gInQxNjUgdDE2NiB0MTY3IHQxNjgiLnNwbGl0KCkKCkRBVCwgVFJVT1QsIEtERCA9ICJEQVQiLCAi',
'VFJVT1QiLCAiS0hPTkcgRE8gRFVPQyIKc28sIGNob3QgPSB7fSwgW10KZGVmIGdoaShrLCB2KTogc29ba10gPSB2OyByZXR1',
'cm4gdgpkZWYga2V0KHRlbiwgdHJhbmdfdGhhaSwgY2hpX3RpZXQ9IiIpOgogICAgY2hvdC5hcHBlbmQoKHRlbiwgdHJhbmdf',
'dGhhaSwgY2hpX3RpZXQpKQogICAgaW5uKGYiICBbe3RyYW5nX3RoYWk6MTR9XSB7dGVufSIgKyAoZiIgICB7Y2hpX3RpZXR9',
'IiBpZiBjaGlfdGlldCBlbHNlICIiKSkKICAgIHJldHVybiB0cmFuZ190aGFpCgojIC0tLS0tLS0tLS0tLS0tLS0gZG9jIGxv',
'ZyBjdWEgYm8gdGVzdCAoYmFuIDMsIGRhIGRvIHRyZW4gbG9nIFRIQVQpIC0tLS0tLS0tLS0tLS0tLS0KUlhfRE9fQ0hPICA9',
'IHJlLmNvbXBpbGUociIoP20pXiEhISBkbyAoXFMrKSAoLiopJCIpClJYX0RPX0NVT0kgPSByZS5jb21waWxlKHIiKD9tKV4g',
'ezJ9KFxTezEsNH0pIHsyfShcUyspOiAoLiopJCIpClJYX0JPX1FVQSAgPSByZS5jb21waWxlKHIiKD9tKV4gezJ9XFN7MSw2',
'fSBRVUEgKFxTKyk6ICguKikkIikKIyBEb25nIHRvbmcga2V0IFRIQVQgbyBEQVUgZG9uZy4gQ2EgRE8gY28gdGhlIGluIGxh',
'aSBzdGRvdXQgY3VhIG1vdCBsdW90IENPTiAodDE1NSBjaGF5IGxhaSB0MDEsIHQ3Mi90OTggY2hheQojICJibyIpIOKAlCBk',
'b25nIHRvbmcgTE9ORyBheSBuYW0gR0lVQSBkb25nIChkbzogMjAgZG9uZyBsb25nIGRldSBvIGdpdWEgZG9uZywgY2hpIGRv',
'bmcgdG9uZyB0aGF0IG8gZGF1IGRvbmcpLCBtYQojIGBzZWFyY2hgIGtob25nIG5lbyBiYXQgbm8gVFJVT0MuIERvIHRyZW4g',
'MjAyNi0wOS0zMGMsIDBlYTk1ZGUgKyBkb3QgYmllbiBsYW0gdDAxIERPOiBkb2MgcmEgIjAvMSIgPT4KIyAiZGFuaCBzYWNo',
'IEtIT05HIGRheSBkdSIsICJMRUNIIFNPIEhPQzogdGhpZXUgLTIwIGNhIiwgdHJvbmcga2hpIHRvbmcgdGhhdCAxNjYtMTQ1',
'PTIxID09IDIxIGNhIGRvYyBkdW9jLgpSWF9UT05HICAgID0gcmUuY29tcGlsZShyIig/bSlebGVhc2VfcHVibGlzaDogKFxk',
'KykvKFxkKylcYlteXG5dKj89KFxkKyksW15cbl0qPz0oXGQrKSIpCgpkZWYgc29fY2EodCk6CiAgICBtID0gcmUubWF0Y2go',
'ciJ0KFxkKykiLCB0KTsgcmV0dXJuIChpbnQobS5ncm91cCgxKSkgaWYgbSBlbHNlIDEwKio2LCB0KQoKZGVmIGRvY19kbyhv',
'dXQpOgogICAgdGFpX2NobyA9IHt0OiBsLnN0cmlwKCkgZm9yIHQsIGwgaW4gUlhfRE9fQ0hPLmZpbmRhbGwob3V0KX0KICAg',
'IGJvID0ge3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0KX0KICAgIGN1b2kgPSB7dDogbC5zdHJpcCgpIGZv',
'ciBfLCB0LCBsIGluIFJYX0RPX0NVT0kuZmluZGFsbChvdXQpIGlmIHQgbm90IGluIGJvfQogICAgaG9wID0gZGljdChjdW9p',
'KTsgaG9wLnVwZGF0ZSh0YWlfY2hvKQogICAgZ2MsIHRpbiA9IFtdLCBUcnVlCiAgICBpZiBzZXQodGFpX2NobykgIT0gc2V0',
'KGN1b2kpOgogICAgICAgIGdjLmFwcGVuZChmImhhaSBuZ3VvbiBMRUNIOiBjaGktdGFpLWNobz17c29ydGVkKHNldCh0YWlf',
'Y2hvKS1zZXQoY3VvaSkpfSBjaGktY3VvaT17c29ydGVkKHNldChjdW9pKS1zZXQodGFpX2NobykpfSIpCiAgICAgICAgdGlu',
'ID0gRmFsc2UKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXQpCiAgICBpZiBub3QgbToKICAgICAgICBnYy5hcHBlbmQoIktI',
'T05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQiKTsgdGluID0gRmFsc2UKICAgIGVsc2U6CiAgICAgICAgZGF0LCB0cmVuID0g',
'aW50KG0uZ3JvdXAoMSkpLCBpbnQobS5ncm91cCgyKSkKICAgICAgICBnYy5hcHBlbmQoZiJzbyBob2M6IHt0cmVufS17ZGF0',
'fT17dHJlbi1kYXR9IGRvOyBkb2MgZHVvYyB7bGVuKGhvcCl9IikKICAgICAgICBpZiB0cmVuIC0gZGF0ICE9IGxlbihob3Ap',
'OgogICAgICAgICAgICBnYy5hcHBlbmQoZiJMRUNIIFNPIEhPQzogdGhpZXUge3RyZW4tZGF0LWxlbihob3ApfSBjYSIpOyB0',
'aW4gPSBGYWxzZQogICAgcmV0dXJuIGhvcCwgZ2MsIHRpbgoKIyBNYXUgY28gZG9uZyB0b25nIExPTkcgZ2l1YSBkb25nIChk',
'YW5nIHQxNTUgaW4gbGFpIGx1b3QgY29uKTogYm8gZG9jIGJhdCBkb25nIHRvbmcgREFVIFRJRU4gbGEgdHUga2llbSBETy4K',
'X01BVSA9ICgiISEhIGRvIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU4gYSAnbGVhc2VfcHVibGlzaDogMC8xIMSR4bqh',
'dDsgxJHDoyBjaOG6oXk9MSwgYuG7jyBxdWE9MCdcbiIKICAgICAgICAiISEhIGRvIHQxNTBfeCBXaW5FcnJvciAxMzE0IHJl',
'cXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICIgIELhu44gUVVBIHQxMzFfeTogbmVuIGZpeHR1cmVcbiIKICAgICAgICAi',
'ICDEkOG7jiAgdDAyYl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTjogYVxuIgogICAgICAgICIgIMSQ4buOICB0MTUwX3g6IFdp',
'bkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAgICAgImxlYXNlX3B1Ymxpc2g6IDEvMyDEkeG6oXQ7IMSR',
'w6MgY2jhuqF5PTMsIGLhu48gcXVhPTFcbiIpCgpkZWYgY2hheShhcmd2LCBjd2QsIHBodXQ9NjApOgogICAgIyBQWVRIT05P',
'UFRJTUlaRSBjdWEgbWF5IG5ndW9pIGRvIGxvdCB2YW8gYm8gdGVzdCB0aGkgbW9pIGBhc3NlcnRgIHRyb25nIGNhIGJpIEJP',
'IChkbyB0cmVuIDIwMjYtMDktMzBjOgogICAgIyBjaGF5KCkgKyBQWVRIT05PUFRJTUlaRT0xID0+IGBhc3NlcnQgRmFsc2Vg',
'IHF1YSwgcmM9MCkuIENodW9pIFJPTkcgPSBraG9uZyBkYXQgKHRhaSBsaWV1IENQeXRob24pLgogICAgbXQgPSBkaWN0KG9z',
'LmVudmlyb24sIFBZVEhPTlVURjg9IjEiLCBQWVRIT05JT0VOQ09ESU5HPSJ1dGYtOCIsCiAgICAgICAgICAgICAgUFlUSE9O',
'RE9OVFdSSVRFQllURUNPREU9IjEiLCBQWVRIT05VTkJVRkZFUkVEPSIxIiwgUFlUSE9OT1BUSU1JWkU9IiIpCiAgICBwID0g',
'c3VicHJvY2Vzcy5ydW4oW3N5cy5leGVjdXRhYmxlXSArIGFyZ3YsIGN3ZD1zdHIoY3dkKSwgY2FwdHVyZV9vdXRwdXQ9VHJ1',
'ZSwKICAgICAgICAgICAgICAgICAgICAgICB0ZXh0PVRydWUsIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIs',
'IHRpbWVvdXQ9cGh1dCo2MCwgZW52PW10KQogICAgcmV0dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rkb3V0IG9yICIiKSArIChw',
'LnN0ZGVyciBvciAiIikKCmRlZiBtYXVfY2Eob3V0LCB0KToKICAgIG0gPSByZS5zZWFyY2gociIoP20pXjw8PCByYSAoIiAr',
'IHQgKyByIlthLXpdP19cUyopIFswLTkuXStzIChcdyspXHMqJCIsIG91dCkKICAgIHJldHVybiBtLmdyb3VwKDIpIGlmIG0g',
'ZWxzZSBOb25lCgpkZWYgZ2l0KGdvYywgKmEsIHBodXQ9NSk6CiAgICBwID0gc3VicHJvY2Vzcy5ydW4oWyJnaXQiLCAiLUMi',
'LCBzdHIoZ29jKSwgKmFdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsCiAgICAgICAgICAgICAgICAgICAgICAg',
'ZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD1waHV0KjYwKQogICAgcmV0dXJuIHAucmV0dXJu',
'Y29kZSwgKHAuc3Rkb3V0IG9yICIiKS5zdHJpcCgpLCAocC5zdGRlcnIgb3IgIiIpLnN0cmlwKCkKCgojID09PT09PT09PT09',
'PT09PT09IE5BTSBQUk9CRSwgdmlldCB0aGFuaCBIQU0gVEhVQU4gZGUgVFUgS0lFTSBkdW9jID09PT09PT09PT09PT09PT09',
'CiMgTW9pIGhhbSB0cmEgKHRyYW5nX3RoYWksIGNoaV90aWV0LCBkdV9saWV1KS4gS0hPTkcgaW4sIEtIT05HIHRob2F0IOKA',
'lCBuaG8gdmF5IGNodW5nCiMgY2hheSBkdW9jIHRyZW4gbmVuIEJBVCBLWSwgdmEgYC0tdHUta2llbS1wcm9iZWAgZ29pIHRo',
'YW5nIGNodW5nIGRlIGtpZW0gY2hpbmggYm8gZG8uCgpkZWYgX3Nhbih0KToKICAgIGQgPSBQYXRoKHQpLyJkIjsgZC5ta2Rp',
'cigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICBy',
'ZXR1cm4gZCwgY3csIHBmCgpkZWYgZG9fbjgoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiQnVvYyAxIChDT05HX0NVX0dJVCkg',
'Y2hpIGR1b2MgbmhhbiBnaXQuZXhlLiBEb2kgY2h1bmcgZHVvbmc6IGdpdC5leGUgVkFOIHBoYWkgbmhhbi4iIiIKICAgIGtx',
'ID0ge30KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkLCBjdywgcGYgPSBf',
'c2FuKHQpCiAgICAgICAgZm9yIHRlbiBpbiAoImdpdC5leGUiLCAiZ2l0LmJhdCIsICJnaXQuY21kIiwgImdpdC5weSIsICJr',
'aG9uZy1waGFpLWdpdC50eHQiKToKICAgICAgICAgICAgZiA9IGQvdGVuOyBmLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0i',
'dXRmLTgiKQogICAgICAgICAgICByLCBfID0gZ29pKGNvbmdfY3VfZ2l0PXN0cihmKSwgcGF0aD0iIiwgcHJvZ3JhbV9maWxl',
'cz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAga3FbZiJDT05HX0NVX0dJVD17dGVufSJdID0gIk5IQU4iIGlm',
'IHIgZWxzZSAiVFUgQ0hPSSIKICAgIGxvdCA9IFtrIGZvciBrLCB2IGluIGtxLml0ZW1zKCkgaWYgdiA9PSAiTkhBTiIgYW5k',
'IG5vdCBrLmVuZHN3aXRoKCJnaXQuZXhlIildCiAgICBpZiBrcS5nZXQoIkNPTkdfQ1VfR0lUPWdpdC5leGUiKSAhPSAiTkhB',
'TiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBnaXQuZXhlIGhvcCBsZSBtYSBiaSB0dSBj',
'aG9pIiwga3EKICAgIHJldHVybiAoREFUIGlmIG5vdCBsb3QgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgbG90IGVsc2UgZiJj',
'b24gbmhhbjoge2xvdH0iKSwga3EKCmRlZiBkb19uOShnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJNdWMgUEFUSCBib2Mgbmhh',
'eSBrZXAgcGhhaSBOSEFOOyBtdWMgcm9uZyAvIHRvYW4ga2hvYW5nIHRyYW5nIHBoYWkgYm8gcXVhLCBraG9uZyBuZW0uIiIi',
'CiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBh',
'dGgodCkvImNvIGdpdCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkv',
'InBmIjsgcGYubWtkaXIoKQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIp',
'CiAgICAgICAgZm9yIG5oYW4sIG11YyBpbiAoKCJraG9uZyBuaGF5Iiwgc3RyKGQpKSwgKCJjbyBuaGF5IGtlcCIsIGYnIntk',
'fSInKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAoInJvbmciLCAiIiksICgiY2hpIGtob2FuZyB0cmFuZyIsICIgICAi',
'KSk6CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIHIsIF8gPSBnb2kocGF0aD1tdWMsIHByb2dyYW1fZmlsZXM9',
'c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59Il0gPSAiTkhBTiIgaWYgciBl',
'bHNlICJOb25lIgogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgICAgICBrcVtmIlBBVEgg',
'e25oYW59Il0gPSBmIk5FTSB7dHlwZShlKS5fX25hbWVfX30iCiAgICBpZiBrcS5nZXQoIlBBVEgga2hvbmcgbmhheSIpICE9',
'ICJOSEFOIjoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG11YyBQQVRIIHRodW9uZyBtYSBr',
'aG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICBvayA9IChrcS5nZXQoIlBBVEggY28gbmhheSBrZXAiKSA9PSAiTkhBTiIK',
'ICAgICAgICAgIGFuZCBrcS5nZXQoIlBBVEggcm9uZyIpID09ICJOb25lIiBhbmQga3EuZ2V0KCJQQVRIIGNoaSBraG9hbmcg',
'dHJhbmciKSA9PSAiTm9uZSIpCiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhl',
'bSBiYW5nIiksIGtxCgojIERhdSBwaGFuIGNhY2ggZHVuZyBERSBUSFUuIFBoYWkgS0hBQyBvcy5wYXRoc2VwIHRyZW4gQ0Eg',
'SEFJIG5lbiAoJzsnIFdpbmRvd3MsICc6JyBQT1NJWCkKIyB0aGkgaGFpIGdpYSB0aHV5ZXQgInRhY2ggdGhlbyBkYXUgZHVv',
'YyB0cnV5ZW4iIHZhICJ0YWNoIHRoZW8gb3MucGF0aHNlcCIgbW9pIHJvaSByYSBuaGF1LgpUSFVfTjEwID0gInwiCgpkZWYg',
'ZG9fbjEwKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkhhbSBwaGFpIHRhY2ggUEFUSCB0aGVvIGRhdSBwaGFuIGNhY2ggRFVP',
'QyBUUlVZRU4sIGtob25nIHRoZW8gb3MucGF0aHNlcCBjdWEgbmVuLgoKICAgIEJhbiBjdSBkbyAibW90IGRhdSAnOycgdHJv',
'bmcgVEVOIHRodSBtdWMiIHZhIGRhdCBEQVQgdHJlbiBXaW5kb3dzIGR1IGhhbSBzYWkuIE5vCiAgICBkZWdlbmVyYXRlOiB0',
'cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycsIG5lbiAnQzovYTtiJyB0aGF0IHN1IENPIE5HSElBIGxhIGhhaQog',
'ICAgbXVjIOKAlCAidGFjaCBkdW5nIiB2YSAidGFjaCBzYWkiIGNobyByYSBjdW5nIGtldCBxdWEsIHBoZXAgZG8ga2hvbmcg',
'dGhlIGRvIG5hby4gTm8KICAgIGRhIGNoYW0gREFUIGNobyA5NTgzMTY4NSB0cm9uZyBraGkgdDE3MSBjdWEgY2hpbmggYmFu',
'IHZhIGF5IERPIHZpIGR1bmcga2h1eWV0IHRhdCBheS4KICAgIE1vdCBjb25nIGtob25nIHRoZSBkbyB0aGkga2hvbmcgcGhh',
'aSBjb25nLgogICAgIiIiCiAgICB0ZW5fc2VwID0gbmV4dCgoayBmb3IgayBpbiAoInBoYW5fY2FjaCIsICJkYXVfcGhhbl9j',
'YWNoIiwgInNlcCIpIGlmIGsgaW4gc2lnLnBhcmFtZXRlcnMpLCBOb25lKQogICAgaWYgdGVuX3NlcCBpcyBOb25lOgogICAg',
'ICAgICMgS2hvbmcgY28gdGhhbSBzbyB0aGkgdHJlbiBXaW5kb3dzIEtIT05HIGNvbiBkdW9uZyBuYW8gdGFjaCBoYWkgZ2lh',
'IHRodXlldC4KICAgICAgICBpZiBvcy5wYXRoc2VwID09ICI7IjoKICAgICAgICAgICAgcmV0dXJuIChLREQsICJ0cmVuIFdp',
'bmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgdmEgaGFtIGtob25nIG5oYW4gdGhhbSBzbyBkYXUgcGhhbiBjYWNoICIKICAg',
'ICAgICAgICAgICAgICAgICAgICAgICItPiBraG9uZyB0YWNoIGR1b2MgaGFpIGdpYSB0aHV5ZXQiLAogICAgICAgICAgICAg',
'ICAgICAgIHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IE5vbmV9KQogICAgICAgIHdpdGggdGVt',
'cGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUiOyBsYS5t',
'a2RpcigpCiAgICAgICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90',
'ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyAgPSBnb2kocGF0aD1zdHIobGEpICsgb3MucGF0',
'aHNlcCArIHN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAgcjAsIF8gPSBn',
'b2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAga3EgPSB7Im9zLnBh',
'dGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiBOb25lLAogICAgICAgICAgICAgICJjbyBtdWMgY2h1YSAnOyci',
'OiAiTkhBTiIgaWYgciBlbHNlICJOb25lIiwKICAgICAgICAgICAgICAiZG9pIGNodW5nIGR1b25nIChraG9uZyBjbyAnOycp',
'IjogIk5IQU4iIGlmIHIwIGVsc2UgIk5vbmUifQogICAgICAgIGlmIG5vdCByMDoKICAgICAgICAgICAgcmV0dXJuIEtERCwg',
'ImRvaSBjaHVuZyBkdW9uZyBob25nIiwga3EKICAgICAgICByZXR1cm4gKERBVCBpZiByIGVsc2UgVFJVT1QpLCAoIiIgaWYg',
'ciBlbHNlICJtdWMgZ2l0LmV4ZSBob3AgbGUgYmkgTUFUIiksIGtxCgogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJl',
'Y3RvcnkoKSBhcyB0OgogICAgICAgIGxhID0gUGF0aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKSAgICAgICAgICAjICc7JyBu',
'YW0gdHJvbmcgVEVOLCBraG9uZyBwaGFpIGRhdSBwaGFuIGNhY2gKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAg',
'ICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBub2kgPSBzdHIobGEp',
'ICsgVEhVX04xMCArIHN0cihkKQogICAgICAgIGt3ID0gZGljdChwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cp',
'KQogICAgICAgIHJfY2hpbmgsIF8gPSBnb2kocGF0aD1ub2ksICAgICAgKip7dGVuX3NlcDogVEhVX04xMH0sICAgKiprdykg',
'ICAjIHRhY2ggZHVuZyAgLT4gTkhBTgogICAgICAgIHJfZHVvbmcsIF8gPSBnb2kocGF0aD1zdHIoZCksICAgKip7dGVuX3Nl',
'cDogVEhVX04xMH0sICAgKiprdykgICAjIGRvaSBjaHVuZyBkdW9uZwogICAgICAgIHJfcGhhbmJpZXQsIF8gPSBnb2kocGF0',
'aD1ub2ksICAgKip7dGVuX3NlcDogb3MucGF0aHNlcH0sICoqa3cpICAjIHRhY2ggdGhlbyBvcy5wYXRoc2VwIC0+IG1hdAog',
'ICAga3EgPSB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiB0ZW5fc2VwLCAiZGF1IHRodSI6IFRI',
'VV9OMTAsCiAgICAgICAgICBmIm5vaSBiYW5nIHtUSFVfTjEwIXJ9LCB7dGVuX3NlcH09e1RIVV9OMTAhcn0iOiAgICAgICAi',
'TkhBTiIgaWYgcl9jaGluaCBlbHNlICJOb25lIiwKICAgICAgICAgIGYiZG9pIGNodW5nIGR1b25nIChtb3QgbXVjLCB7dGVu',
'X3NlcH09e1RIVV9OMTAhcn0pIjogICJOSEFOIiBpZiByX2R1b25nIGVsc2UgIk5vbmUiLAogICAgICAgICAgZiJwaGFuIGJp',
'ZXQ6IG5vaSBiYW5nIHtUSFVfTjEwIXJ9LCB7dGVuX3NlcH09e29zLnBhdGhzZXAhcn0iOiAiTkhBTiIgaWYgcl9waGFuYmll',
'dCBlbHNlICJOb25lIn0KICAgIGlmIG5vdCByX2R1b25nOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcg',
'aG9uZzogbW90IG11YyBob3AgbGUgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgIyBDb25nIHBoYWkgQ08gVEhF',
'IGRvLiBOZXUgY2EgaGFpIGRhdSBwaGFuIGNhY2ggZGV1IHJhIE5IQU4gdGhpIHBoZXAgZG8ga2hvbmcgcGhhbgogICAgIyBi',
'aWV0IGR1b2MgZ2kg4oCUIGR1bmcgYmFvIERBVCwgYmFvIHRoYW5nIGxhIGtob25nIGRvIGR1b2MuCiAgICBpZiByX3BoYW5i',
'aWV0OgogICAgICAgIHJldHVybiAoS0RELCBmInBoZXAgZG8gS0hPTkcgcGhhbiBiaWV0IGR1b2M6IG5vaSBiYW5nIHtUSFVf',
'TjEwIXJ9IG1hIHRhY2ggdGhlbyAiCiAgICAgICAgICAgICAgICAgICAgIGYie29zLnBhdGhzZXAhcn0gVkFOIHRpbSByYSBn',
'aXQuZXhlIiwga3EpCiAgICByZXR1cm4gKChEQVQsICIiLCBrcSkgaWYgcl9jaGluaCBlbHNlCiAgICAgICAgICAgIChUUlVP',
'VCwgZiJ0YWNoIHRoZW8gb3MucGF0aHNlcCB0aGF5IHZpIHRoZW8ge3Rlbl9zZXB9IGR1b2MgdHJ1eWVuIiwga3EpKQoKCmRl',
'ZiBkb19uMTEoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiVHJ1eWVuIGNoYW5fZG9hbiA9PiB0aHUgZHVvYyB0aG9uZyBiYW8g',
'VkEgc3RkZXJyIElNLiBLaG9uZyB0cnV5ZW4gPT4gc3RkZXJyIFZBTiBjby4iIiIKICAgIGlmICJjaGFuX2RvYW4iIG5vdCBp',
'biBzaWcucGFyYW1ldGVyczoKICAgICAgICByZXR1cm4gS0RELCAiX2dpdF93aW5kb3dzIGtob25nIG5oYW4gdGhhbSBzbyBj',
'aGFuX2RvYW4iLCB7InRoYW0gc28iOiBsaXN0KHNpZy5wYXJhbWV0ZXJzKX0KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5',
'RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0',
'ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBjZCA9IFtdCiAgICAgICAgXywgZV9jbyA9IGdvaShwYXRo',
'PXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSwgY2hhbl9kb2FuPWNkKQogICAgICAgIF8sIGVf',
'a2ggPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICBrcSA9IHsiY2hh',
'bl9kb2FuIHRodSBkdW9jIChtdWMpIjogbGVuKGNkKSwKICAgICAgICAgICJzdGRlcnIga2hpIENPIGNoYW5fZG9hbiAoYnl0',
'ZSkiOiBsZW4oZV9jby5lbmNvZGUoKSksCiAgICAgICAgICAic3RkZXJyIGtoaSBLSE9ORyB0cnV5ZW4gKGJ5dGUpIjogbGVu',
'KGVfa2guZW5jb2RlKCkpfQogICAgaWYgbGVuKGNkKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPT0gMDoKICAgICAg',
'ICByZXR1cm4gS0RELCAibmhhbmggJVByb2dyYW1GaWxlcyUga2hvbmcgcGhhbiBnaWFpIEtIT05HIGJheSByYSBjaGFuIGRv',
'YW4gbmFvIC0+IGNodWEgZG8gZHVvYyIsIGtxCiAgICBvayA9IGxlbihjZCkgPiAwIGFuZCBsZW4oZV9jby5lbmNvZGUoKSkg',
'PT0gMCBhbmQgbGVuKGVfa2guZW5jb2RlKCkpID4gMAogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBp',
'ZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKZGVmIGRvX24xMihnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW5nIHNlbnRp',
'bmVsIGdpdF9wYXRoIHRyb25nIGZpeHR1cmUgcGhhaSB0dXlldCBkb2kgdHJlbiBDQSBIQUkgbmVuLiIiIgogICAgbmQgPSB0',
'ZXB0LnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiKQogICAgaGFuZyA9IHNvcnRlZChzZXQo',
'cmUuZmluZGFsbChyJ2dpdF9wYXRoXHMqPVxzKiIoW14iXSspIicsIG5kKSkpCiAgICB4YXUgPSBbaCBmb3IgaCBpbiBoYW5n',
'IGlmIG5vdCAoUHVyZVBvc2l4UGF0aChoKS5pc19hYnNvbHV0ZSgpIGFuZCBQdXJlV2luZG93c1BhdGgoaCkuaXNfYWJzb2x1',
'dGUoKSldCiAgICBrcSA9IHsiaGFuZyBnaXRfcGF0aCB0aW0gdGhheSI6IGhhbmcsICJjaGkgdHV5ZXQgZG9pIE1PVCBuZW4i',
'OiB4YXV9CiAgICBpZiBub3QgaGFuZzoKICAgICAgICByZXR1cm4gS0RELCAia2hvbmcgdGltIHRoYXkgaGFuZyBnaXRfcGF0',
'aCBuYW8gdHJvbmcgZml4dHVyZSAtPiBtYXUgZG9jIGNvIHRoZSBkYSBkb2kiLCBrcQogICAgcmV0dXJuIChEQVQgaWYgbm90',
'IHhhdSBlbHNlIFRSVU9UKSwgKCIiIGlmIG5vdCB4YXUgZWxzZSBmImNoaS1tb3QtbmVuOiB7eGF1fSIpLCBrcQoKUFJPQkUg',
'PSBbKCJOOCBidW9jIDEgY2hpIG5oYW4gZ2l0LmV4ZSIsIGRvX244KSwKICAgICAgICAgKCJOOSBib2MgbmhheSBrZXAgbyBt',
'dWMgUEFUSCIsIGRvX245KSwKICAgICAgICAgKCJOMTAgZGF1ICc7JyB0cm9uZyB0ZW4gdGh1IG11YyIsIGRvX24xMCksCiAg',
'ICAgICAgICgiTjExIGNoYW4gZG9hbiBkb2kga2VuaCIsIGRvX24xMSksCiAgICAgICAgICgiTjEyIGhhbmcgc2VudGluZWwg',
'dHV5ZXQgZG9pIENBIEhBSSBuZW4iLCBkb19uMTIpXQoKIyAtLS0gY2hlIGRvIFRVIEtJRU06IGNoYXkgbmFtIHByb2JlIHRy',
'ZW4gbW90IGNheSBiYXQga3ksIG5lbiBiYXQga3kgLS0tCmlmICItLXR1LWtpZW0tcHJvYmUiIGluIHN5cy5hcmd2OgogICAg',
'X2cgPSBQYXRoKHN5cy5hcmd2W3N5cy5hcmd2LmluZGV4KCItLXR1LWtpZW0tcHJvYmUiKSArIDFdKS5yZXNvbHZlKCkKICAg',
'IF9zcCA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF90ayIsIHN0cihfZy8ib3BzIi8ibGVh',
'c2VfcHVibGlzaC5weSIpKQogICAgX2xwID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3ApOyBfc3AubG9h',
'ZGVyLmV4ZWNfbW9kdWxlKF9scCkKICAgIF9zaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShfbHAuX2dpdF93aW5kb3dzKQogICAg',
'ZGVmIF9nb2koKiprdyk6CiAgICAgICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgICAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJl',
'Y3Rfc3RkZXJyKGUpOgogICAgICAgICAgICByZXR1cm4gX2xwLl9naXRfd2luZG93cygqKmt3KSwgZS5nZXR2YWx1ZSgpCiAg',
'ICBwcmludChmIlRVIEtJRU0gUFJPQkUgdHJlbiB7X2d9ICAobmVuIHtzeXMucGxhdGZvcm19KSIpCiAgICBmb3IgX3Rlbiwg',
'X2YgaW4gUFJPQkU6CiAgICAgICAgX3R0LCBfY3QsIF9kbCA9IF9mKF9nb2ksIF9zaWcsIF9nLyJvcHMiLyJsZWFzZV9wdWJs',
'aXNoX3Rlc3QucHkiKQogICAgICAgIHByaW50KGYiICBbe190dDoxNH1dIHtfdGVufSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0',
'IGVsc2UgIiIpKQogICAgICAgIGZvciBfaywgX3YgaW4gKF9kbCBvciB7fSkuaXRlbXMoKTogcHJpbnQoZiIgICAgICAgIHtf',
'azozNH06IHtfdn0iKQogICAgc3lzLmV4aXQoMCkKCiMgLS0tIGNoZSBkbyBLSUVNIERPTkcgQk86IHRlcCAucHkgbmF5IHBo',
'YWkgVFJVTkcgVFVORyBCWVRFIHZvaSBiYW4gbmh1bmcgdHJvbmcgcHMxIC0tLQojIEtob25nIGNvbmcgbmFvIGJ1b2MgaGFp',
'IGJhbiBzYW8ga2hvcDogZG8gZHVvYywgbm9pIHRyYW4gMi80MDAgLT4gOTkvOTk5OTkgQ0hJIHRyb25nIC5weQojIHRoaSBj',
'aV9kYW5nX2t5IGxhbiB0MjYvdDI3IHZhbiB4YW5oLCBjb24gY2hvdCBTSEEgY3VhIHBzMSBjaGkgc28gYmFuIG5odW5nIHZv',
'aSBoYW5nIHNvCiMgY3VhIENISU5IIG5vLiBDaGF5OiBweXRob24gd3A1NDEtZG8tZzItd2luZG93cy5weSAtLWtpZW0tZG9u',
'Zy1ibyB3cDU0MS1kby1nMi5wczEgIChyYyAwfDMpCmlmICItLWtpZW0tZG9uZy1ibyIgaW4gc3lzLmFyZ3Y6CiAgICBpbXBv',
'cnQgYmFzZTY0CiAgICBfcHMgPSBQYXRoKHN5cy5hcmd2W3N5cy5hcmd2LmluZGV4KCItLWtpZW0tZG9uZy1ibyIpICsgMV0p',
'LnJlYWRfdGV4dChlbmNvZGluZz0iYXNjaWkiKQogICAgX20gPSByZS5zZWFyY2gociIoP21zKV5cJEI2NCA9IEBcKCguKj8p',
'XlwpIiwgX3BzKQogICAgX2sgPSByZS5zZWFyY2gociIoP20pXlwkU2hhQm9Eb1xzKj1ccyonKFswLTlhLWZdezY0fSknIiwg',
'X3BzKQogICAgX25odW5nID0gYmFzZTY0LmI2NGRlY29kZSgiIi5qb2luKHJlLmZpbmRhbGwociInKFtBLVphLXowLTkrLz1d',
'KiknIiwgX20uZ3JvdXAoMSkpKSkgaWYgX20gZWxzZSBiIiIKICAgIF90b2kgPSBQYXRoKF9fZmlsZV9fKS5yZWFkX2J5dGVz',
'KCkKICAgIF9vayA9IGJvb2woX20gYW5kIF9rKSBhbmQgX25odW5nID09IF90b2kgYW5kIGhhc2hsaWIuc2hhMjU2KF90b2kp',
'LmhleGRpZ2VzdCgpID09IF9rLmdyb3VwKDEpCiAgICBpbm4oZiJLSUVNIERPTkcgQk86IHtEQVQgaWYgX29rIGVsc2UgS0RE',
'fSAgKG5odW5nIHtsZW4oX25odW5nKX0gYnl0ZSwgdGVwIHtsZW4oX3RvaSl9IGJ5dGUpIikKICAgIHN5cy5leGl0KDAgaWYg',
'X29rIGVsc2UgMykKCmlubigiPSIgKiA3OCk7IGlubigiV1A1NDEgZzIgLSBwaGVwIGRvIHRyZW4gV2luZG93cyB0aGF0IChz',
'cGVjIHIzOiBOMS1ONCwgTjgtTjEyLCBONywga2ljaCB0aHVvYykiKTsgaW5uKCI9IiAqIDc4KQoKIyAtLS0tLS0tLS0tLS0t',
'LS0tIHR1IGtpZW0gYm8gZG9jIC0tLS0tLS0tLS0tLS0tLS0KX2QsIF9nLCBfdCA9IGRvY19kbyhfTUFVKQpfb2sgPSAobGVu',
'KF9kKSA9PSAyIGFuZCBhbnkoeC5zdGFydHN3aXRoKCJ0MDJiIikgZm9yIHggaW4gX2QpCiAgICAgICBhbmQgbm90IGFueSh4',
'LnN0YXJ0c3dpdGgoInQxMzEiKSBmb3IgeCBpbiBfZCkgYW5kIF90KQppbm4oIlR1IGtpZW0gYm8gZG9jIGxvZzoiLCBEQVQg',
'aWYgX29rIGVsc2UgVFJVT1QpCmlmIG5vdCBfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IGJvIGRvYyBs',
'b2cgY3VhIGNoaW5oIHNjcmlwdCBuYXkgc2FpIC0+IGtob25nIGRvIGdpIGNhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0tLS0t',
'LS0tLS0tLS0tIDAuIG5lbiBkbyAtLS0tLS0tLS0tLS0tLS0tCmdvYyA9IFBhdGgoc3lzLmFyZ3ZbMV0pLnJlc29sdmUoKSBp',
'ZiBsZW4oc3lzLmFyZ3YpID4gMSBlbHNlIFBhdGguY3dkKCkKdGVwLCB0ZXB0ID0gZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVi',
'bGlzaC5weSIsIGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIKaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsg',
'aW5uKCIwLiBORU4gRE8iKQojIE1PSSBMT0cgUEhBSSBUVSBLSEFJIG5vIGRvIENBSSBHSSBiYW5nIEJPIERPIE5BTy4gQmFp',
'IGhvYyAxOS0wOS0yMDI2OiBtb3QgbHVvdCBkbwojIGd1aSB2ZSBkdW9jIGRvYyBuaHUga2V0IHF1YSBjdWEgYmFuIHZhIGRh',
'bmcgeGV0LCBuaHVuZyB0aGF0IHJhIGxhIGJhbiBkbyBDVSBjaGF5CiMgdHJlbiBuaGFuaCBLSEFDLiBEb2MgcmEgdGhpIG1h',
'dCBtb3Qgdm9uZzsgbG9nIHR1IGtoYWkgdGhpIHRoYXkgbmdheSBkb25nIGRhdS4KdHJ5OgogICAgX3R1ID0gaGFzaGxpYi5z',
'aGEyNTYoUGF0aChfX2ZpbGVfXykucmVhZF9ieXRlcygpKS5oZXhkaWdlc3QoKQpleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgog',
'ICAgX3R1ID0gZiJraG9uZyB0dSBiYW0gZHVvYzoge19lfSIKZ2hpKCJib19kb19zaGEyNTYiLCBfdHUpCmlubihmIiAgQk8g',
'RE8gICAgICAgIDogc2hhMjU2IHtfdHVbOjE2XX0gIChiYW4ge0JBTl9CT19ET30pIikKaW5uKCIgIHN5cy5wbGF0Zm9ybSA6',
'Iiwgc3lzLnBsYXRmb3JtLCAifCBweXRob24iLCBzeXMudmVyc2lvbi5zcGxpdCgpWzBdKQppbm4oIiAgb3MucGF0aHNlcCAg',
'IDoiLCByZXByKG9zLnBhdGhzZXApLCAifCBQQVRIRVhUOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlBBVEhFWFQiKSlbOjYw',
'XSkKaW5uKCIgIFByb2dyYW1GaWxlcyA6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUHJvZ3JhbUZpbGVzIikpLCAifCBTeXN0',
'ZW1Sb290OiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlN5c3RlbVJvb3QiKSkpCmlubigiICBDT05HX0NVX0dJVCAgOiIsIHJl',
'cHIob3MuZW52aXJvbi5nZXQoIkNPTkdfQ1VfR0lUIikpKQppbm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9',
'IE5vbmUKaWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4g',
'PSBib29sKGN0eXBlcy53aW5kbGwuc2hlbGwzMi5Jc1VzZXJBbkFkbWluKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXll',
'biA9IE5vbmUKZ2hpKCJxdXllbl9hZG1pbiIsIHF1eWVuKQpzeW1saW5rX2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVt',
'cGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3Rl',
'eHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHRyeTogb3Muc3ltbGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJs',
'ayIpKTsgc3ltbGlua19kdW9jID0gVHJ1ZQogICAgICAgIGV4Y2VwdCBPU0Vycm9yIGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZh',
'bHNlOyBnaGkoInN5bWxpbmtfbG9pIiwgZiJ7dHlwZShlKS5fX25hbWVfX306IHtlfSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMg',
'ZTogZ2hpKCJzeW1saW5rX2xvaSIsIHN0cihlKSkKZ2hpKCJzeW1saW5rX2R1b2MiLCBzeW1saW5rX2R1b2MpCmlubigiICBB',
'ZG1pbmlzdHJhdG9yOiIsIHF1eWVuLCAifCB0YW8gc3ltbGluayBkdW9jOiIsIHN5bWxpbmtfZHVvYykKCmxvaSA9IFtdCiMg',
'Q29uZyBraWNoIHRodW9jIGxhIHBoZXAgZG8gdHJlbiBMSUNIIFNVIEdJVCwga2hvbmcgZGluaCBnaSBkZW4gbmVuLiBDaG8g',
'cGhlcAojIC0tY2hpLWtpY2gtdGh1b2MgY2hheSBvIG1vaSBuZW4gZGUgY29uIFRVIEtJRU0gZHVvYyBjaGluaCBjb25nIG5h',
'eSAoZGEgZHVuZwojIGRlIHRhaSBkdW5nIGNhIGhhaSB2ZSBjdWEgc3UgY28gbmVuLWN1IDE5LTA5KS4gTW9pIGNob3QgQ0hV',
'QyBOQU5HIHZhbiBkb2kgV2luZG93cy4KaWYgc3lzLnBsYXRmb3JtICE9ICJ3aW4zMiIgYW5kICItLWNoaS1raWNoLXRodW9j',
'IiBub3QgaW4gc3lzLmFyZ3Y6CiAgICBsb2kuYXBwZW5kKGYiS0hPTkcgcGhhaSBXaW5kb3dzIChzeXMucGxhdGZvcm09e3N5',
'cy5wbGF0Zm9ybSFyfSkiKQppZiBub3QgdGVwLmlzX2ZpbGUoKTogIGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB9IikK',
'aWYgbm90IHRlcHQuaXNfZmlsZSgpOiBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwdH0iKQppZiBub3Qgc2h1dGlsLndo',
'aWNoKCJnaXQiKTogbG9pLmFwcGVuZCgia2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCIpCiMgQm8gdGVzdCAobXVjIDIgdmEg',
'TjcpIGNhbiBQeVlBTUw6IHRoaWV1IG5vLCAwZWE5NWRlIHJhIDk2LzE2NiBjYSBETyAoODkgYmFvIHRoYW5nICJObyBtb2R1',
'bGUgbmFtZWQgJ3lhbWwnIiwKIyA3IHF1YSBsdW90IGNvbjsgY28gUHlZQU1MOiAxNjYvMTY2IFFVQSkuIEJvIGRvIGdvaSBj',
'aHVuZyBsYSAiY2EgRE8gTEEiIHJvaSBwaGF0IFRSVU9UIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBjCiMgYmFuZyBweXRob24g',
'S0hPTkcgY28gUHlZQU1MIChkdW5nIG5odSBiYW4gbmh1bmcgcHMxIHR1IHRhaSk6ICJjYSBETyB2aSBUSElFVSBDT05HIENV',
'OiBraG9uZyBjbyIsIFRSVU9UICJNb2kKIyBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jIjsgcmM9MyBjaGkgbmhvIGJvIGRv',
'YyBsb2cgYmF0IG5oYW0gZG9uZyB0b25nIExPTkcgKHN1YSBibyBkb2MgdGhpIHJjPTEpLiBIb2kgVFJVT0MuCmlmIG5vdCAo',
'Ii0tY2hpLWtpY2gtdGh1b2MiIGluIHN5cy5hcmd2IG9yICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YpIGFuZCBpbXBvcnRs',
'aWIudXRpbC5maW5kX3NwZWMoInlhbWwiKSBpcyBOb25lOgogICAgbG9pLmFwcGVuZChmInB5dGhvbiBuYXkgVEhJRVUgUHlZ',
'QU1MIG1hIGJvIHRlc3QgY2FuIG5vOiBcIntzeXMuZXhlY3V0YWJsZX1cIiAtbSBwaXAgaW5zdGFsbCBweXlhbWwiCiAgICAg',
'ICAgICAgICAgICIgKGJhbiBuaHVuZyBwczEgdHUgdGFpIEtIT05HIGNvIHBpcDogY2hheSBsYWkgdm9pIC1QeSA8cHl0aG9u',
'IGRhIGNvIFB5WUFNTD4pIikKCnJjLCBoZWFkLCBfID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxv',
'aS5hcHBlbmQoImtob25nIGRvYyBkdW9jIEhFQUQiKQpnaGkoImhlYWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywg',
'Im1lcmdlLWJhc2UiLCAiLS1pcy1hbmNlc3RvciIsIFNIQV9HMSwgaGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNf',
'YSA9PSAwKQppZiBoZWFkID09IFNIQV9HMToKICAgIHRoZV9oZSA9ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0g',
'LT4gREFZIExBIGcxLiBDSFVBIGNvIGJhbiB2YSBnMjsga2V0IHF1YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9k',
'dWU6CiAgICB0aGVfaGUgPSAiZzIiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hB',
'X0cxWzo4XX0pOyB1bmcgdmllbiBnMiBoYXkga2hvbmc6IE43JyAobXVjIDEpIGRpbmggZGFuaC4iKQplbHNlOgogICAgdGhl',
'X2hlID0gIj8iOyBsb2kuYXBwZW5kKGYiSEVBRD17aGVhZFs6OF19IEtIT05HIHBoYWkgZzEgdmEgS0hPTkcgcGhhaSBoYXUg',
'ZHVlIGN1YSB7U0hBX0cxWzo4XX0g4oCUIHJlYmFzZT8gbmhhbSBuaGFuaD8iKQpnaGkoInRoZV9oZSIsIHRoZV9oZSkKcmNf',
'ciwgcmVmcywgXyA9IGdpdChnb2MsICJmb3ItZWFjaC1yZWYiLCAiLS1wb2ludHMtYXQiLCBoZWFkIG9yICJIRUFEIiwKICAg',
'ICAgICAgICAgICAgICAgICAiLS1mb3JtYXQ9JShyZWZuYW1lOnNob3J0KSIpCmRzciA9IFt4IGZvciB4IGluIHJlZnMuc3Bs',
'aXRsaW5lcygpIGlmIHguc3RyaXAoKSBhbmQgeC5zdHJpcCgpICE9ICJkby10YW0iXQpnaGkoInJlZl90cm9fdG9pX2hlYWQi',
'LCBkc3IpCmlubihmIiAgcmVmIHRybyB0b2kgSEVBRDogeycsICcuam9pbihkc3IpIGlmIGRzciBlbHNlICcoa2hvbmcgcmVm',
'IG5hbyAtIEhFQUQgcm9pIHR1IGRvKSd9IikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogbmVu',
'IGRvIHNhaSwgS0hPTkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlubigiICAtIiwgeCkKICAgIHN5',
'cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMS4ga2ljaCB0aHVvYyAoTjcnIGN1YSBzcGVjIHIzKSAtLS0tLS0tLS0t',
'LS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMS4gS0lDSCBUSFVPQyDigJQgdHJhbiBzcGVjIHIzOiA8PSAy',
'IHRlcCB2YSA8PSA0MDAgZG9uZyB0aGVtIikKIyBWRSBORU4gUEhBSSBUVU9JIOKAlCB2YSBwaGFpIENIVU5HIE1JTkggZHVv',
'YyBsYSB0dW9pLCBraG9uZyBwaGFpIGdpYSBkaW5oLgojIEJhaSBob2MgdHJhIGdpYSAxOS0wOS0yMDI2OiBjbG9uZSB0YWkg',
'ZHVuZyBjaGkgZmV0Y2ggbmhhbmggYmFuIHZhLCBgb3JpZ2luL21hc3RlcmAKIyBkdW5nIHllbiB0dSAxNC0wOSAoYzE2YmQz',
'Miwgc2F1IDk3IGNvbW1pdCkuIG1lcmdlLWJhc2Ugcm9pIHZlIGR1bmcgZGluaCBtYXN0ZXIgY3UsCiMgbmVuIGRpZmYgTlVP',
'VCBjYSA5NyBjb21taXQgbWFzdGVyOiBkbyByYSA0NiB0ZXAgLyArNzExOCB0aGF5IHZpIDIgdGVwIC8gKzM5NyDigJQKIyBD',
'VU5HIE1PVCBDT01NSVQgMGVhOTVkZS4gTW90IHRpZXUgY2hpIERFTFRBIG1hIHZlIG5lbiBraG9uZyB0dW9pIHRoaSBraG9u',
'ZyBzYWkKIyBsZWNoIG1vdCBjaHV0LCBubyBzYWkgY2EgbW90IGJhYyBkbyBsb24uCiMgQ2hvIG5lbjogbmVuIGtob25nIGNo',
'dW5nIG1pbmggZHVvYyBsYSB0dW9pID0+IEtIT05HIERPIERVT0MgKHJjPTMpLCBLSE9ORyBwaGFpIFRSVU9ULgojIFRSVU9U',
'IGxhIG1vdCBQSEFOIFFVWUVUIHZlIGJhbiB2YTsgcGhhbiBxdXlldCBjaGkgZHVvYyBwaGVwIHBoYXQgcmEga2hpIGRhIGRv',
'IGR1b2MuCnJjX3UsIHVybF90aG8sIF8gPSBnaXQoZ29jLCAicmVtb3RlIiwgImdldC11cmwiLCAib3JpZ2luIikKdXJsX28s',
'IHVybF9pbiA9IF91cmxfc2FjaCh1cmxfdGhvKSwgX3VybF9pbih1cmxfdGhvKQpnaGkoIm9yaWdpbl91cmwiLCB1cmxfaW4p',
'OyBpbm4oZiIgIG9yaWdpbiAgICAgICA6IHt1cmxfaW4gb3IgJyhraG9uZyBkb2MgZHVvYyknfSIpCnVybF9vayA9IChub3Qg',
'cmNfdSkgYW5kIHVybF9vLnJzdHJpcCgiLyIpIGluIFVSTF9LSE9fSE9QX0xFCnJjX2xyLCBvdXRfbHIsIGVyX2xyID0gZ2l0',
'KGdvYywgImxzLXJlbW90ZSIsICJvcmlnaW4iLCAicmVmcy9oZWFkcy9tYXN0ZXIiKSBpZiB1cmxfb2sgZWxzZSAoMSwgIiIs',
'ICIiKQplcl9sciA9IF9hbl91c2VyaW5mbyhlcl9scikKcmNfbG0sIGxtLCBlcl9sbSAgICAgPSBnaXQoZ29jLCAicmV2LXBh',
'cnNlIiwgIm9yaWdpbi9tYXN0ZXIiKQpybSA9IG91dF9sci5zcGxpdCgpWzBdIGlmIChub3QgcmNfbHIgYW5kIG91dF9sci5z',
'dHJpcCgpKSBlbHNlICIiCmlmIG5vdCB1cmxfb2s6CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmIm9yaWdpbj17',
'dXJsX2luIXJ9IEtIT05HIHBoYWkga2hvIHRoYXQg4oCUICd0dW9pJyBzbyB2b2kgbm8ga2hvbmcgY2h1bmcgbWluaCBkdW9j',
'IGdpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbm90IHJtOgogICAga2V0KCJONycga2lj',
'aCB0aHVvYyIsIEtERCwKICAgICAgICBmImtob25nIGhvaSBkdW9jIG1hc3RlciB0cmVuIHJlbW90ZSAobHMtcmVtb3RlIHJj',
'PXtyY19scn0pOiB7ZXJfbHJbOjYwXX0gIgogICAgICAgIGYi4oCUIGtob25nIGNodW5nIG1pbmggZHVvYyB2ZSBuZW4gY29u',
'IHR1b2kiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiByY19sbSBvciBub3QgbG06CiAgICBr',
'ZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25nIGRvYyBkdW9jIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmU6IHtl',
'cl9sbVs6NjBdfSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIGxtICE9IHJtOgogICAgIyBE',
'ZW0geGVtIHR1dCBsYWkgYmFvIHhhLCBuZXUgZGVtIGR1b2Mg4oCUIGNvbiBzbyBuYXkgbm9pIHJvIG11YyBkbyBzYWkgbGVj',
'aC4KICAgIHJjX2MsIHNhdSwgXyA9IGdpdChnb2MsICJyZXYtbGlzdCIsICItLWNvdW50IiwgZiJ7bG19Li57cm19IikKICAg',
'IHhhID0gZiIsIHR1dCBsYWkge3NhdX0gY29tbWl0IiBpZiAobm90IHJjX2MgYW5kIHNhdS5zdHJpcCgpLmlzZGlnaXQoKSkg',
'ZWxzZSAiIgogICAgaW5uKGYiICBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25lIDoge2xtWzoxMl19IikKICAgIGlubihmIiAg',
'bWFzdGVyIHRyZW4gcmVtb3RlICAgICAgICA6IHtybVs6MTJdfXt4YX0iKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7',
'IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwKICAgICAgICBmInZlIG5l',
'biBDVTogb3JpZ2luL21hc3Rlcj17bG1bOjEyXX0gIT0gcmVtb3RlPXtybVs6MTJdfXt4YX0gIgogICAgICAgIGYi4oCUIGNo',
'YXkgYGdpdCAtQyA8a2hvPiBmZXRjaCBvcmlnaW4gbWFzdGVyYCByb2kgZG8gbGFpIikKICAgIHJjX21iLCBtYiwgbnMsIHJj',
'ID0gMSwgIiIsICIiLCAxCmVsc2U6CiAgICBpbm4oZiIgIHZlIG5lbiBUVU9JOiBvcmlnaW4vbWFzdGVyID0ge2xtWzoxMl19',
'ID09IG1hc3RlciB0cmVuIHJlbW90ZSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3Rl',
'Iiwgcm0pCiAgICByY19tYiwgbWIsIGVyX21iID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAib3JpZ2luL21hc3RlciIsIGhl',
'YWQpCmlmIHJjX21iIG9yIG5vdCBtYjoKICAgIGlmIG1iID09ICIiIGFuZCBybSBhbmQgbG0gPT0gcm06CiAgICAgICAga2V0',
'KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyB0aW5oIGR1b2MgbWVyZ2UtYmFzZSB2b2kgb3JpZ2luL21hc3Rlcjog',
'e2VyX21iWzo3MF19IikKICAgIG5zLCByYyA9ICIiLCAxCmVsc2U6CiAgICBnaGkoIm1lcmdlX2Jhc2UiLCBtYikKICAgIGlu',
'bihmIiAgbWVyZ2UtYmFzZShvcmlnaW4vbWFzdGVyLCBIRUFEKSA9IHttYls6MTJdfSIpCiAgICBpZiBtYiAhPSBTSEFfQkFT',
'RV9TUEVDOgogICAgICAgIGlubihmIiAgTFVVIFk6IGtoYWMgYmFzZSBtYSBzcGVjIHIzIGtoYWkgKHtTSEFfQkFTRV9TUEVD',
'WzoxMl19KSDigJQgdmkgbmhhbmggZGEgbWVyZ2UgbWFzdGVyLiIpCiAgICAgICAgaW5uKCIgICAgICAgICBEbyBzbyBiYXNl',
'IGN1IHNlIE5VT1QgcGhhbiBtYXN0ZXIgbWFuZyB2YW8uIER1bmcgbWVyZ2UtYmFzZSBtb2kgbGEgdmllYyBjdWEgZXhlY3V0',
'b3IuIikKICAgICAgICByY194LCBuc194LCBfID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgU0hBX0JBU0VfU1BF',
'QywgaGVhZCkKICAgICAgICBpZiBub3QgcmNfeDoKICAgICAgICAgICAgaCA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5z',
'X3guc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgICAgICAgICAgYSA9IHN1bShpbnQoeFswXSkgZm9yIHggaW4gaCBp',
'ZiB4WzBdLmlzZGlnaXQoKSkKICAgICAgICAgICAgZ2hpKCJudW1zdGF0X3RoZW9fYmFzZV9zcGVjIiwgeyJ0ZXAiOiBsZW4o',
'aCksICJ0aGVtIjogYX0pCiAgICAgICAgICAgIGlubihmIiAgICAgICAgIChkb2kgY2hpZXU6IHNvIGJhc2Ugc3BlYyA9IHts',
'ZW4oaCl9IHRlcCAvICt7YX0g4oCUIGNvbiBzbyBheSBLSE9ORyBkdW5nIGRlIGNoYW0pIikKICAgIHJjLCBucywgZXIgPSBn',
'aXQoZ29jLCAiZGlmZiIsICItLW51bXN0YXQiLCBtYiwgaGVhZCkKaWYgcmM6CiAgICBwYXNzCmVsc2U6CiAgICBoYW5nID0g',
'W2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnMuc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgIHRoZW0gPSBzdW0oaW50',
'KGhbMF0pIGZvciBoIGluIGhhbmcgaWYgaFswXS5pc2RpZ2l0KCkpCiAgICB4b2EgID0gc3VtKGludChoWzFdKSBmb3IgaCBp',
'biBoYW5nIGlmIGhbMV0uaXNkaWdpdCgpKQogICAgZ2hpKCJzb190ZXAiLCBsZW4oaGFuZykpOyBnaGkoImRvbmdfdGhlbSIs',
'IHRoZW0pOyBnaGkoImRvbmdfeG9hIiwgeG9hKQogICAgZm9yIGggaW4gaGFuZzogaW5uKGYiICAgIHtoWzJdOjM0fSAre2hb',
'MF06PDV9IC17aFsxXX0iKQogICAgaW5uKGYiICAgIFRPTkc6IHtsZW4oaGFuZyl9IHRlcCwgK3t0aGVtfSwgLXt4b2F9ICAg',
'KHRyYW46IHtUUkFOX1RFUH0gdGVwIC8ge1RSQU5fRE9OR30gZG9uZyB0aGVtKSIpCiAgICBjaGFtID0gc29ydGVkKHtoWzJd',
'IGZvciBoIGluIGhhbmd9ICYgV1JJVEVfU0VUX0cyKTsgZ2hpKCJjaGFtX3dyaXRlX3NldCIsIGNoYW0pCiAgICBkZWYgX2Nh',
'X21vaV9jbyhyZXYpOgogICAgICAgIHJfLCBuZF8sIF8gPSBnaXQoZ29jLCAic2hvdyIsIGYie3Jldn06b3BzL2xlYXNlX3B1',
'Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcmV0dXJuIE5vbmUgaWYgcl8gZWxzZSB7dCBmb3IgdCBpbiBDQV9NT0lfRzIgaWYg',
'cmUuc2VhcmNoKHIiKD9tKV5kZWYgIiArIHQgKyByIlthLXpdP18iLCBuZF8pfQogICAgb19tYiwgb19oID0gX2NhX21vaV9j',
'byhtYiksIF9jYV9tb2lfY28oaGVhZCkKICAgIG1hbmcgPSBzb3J0ZWQob19oIC0gb19tYiwga2V5PXNvX2NhKSBpZiAob19t',
'YiBpcyBub3QgTm9uZSBhbmQgb19oIGlzIG5vdCBOb25lKSBlbHNlIE5vbmUKICAgIGdoaSgiY2FfbW9pX2cyX21hbmdfdmFv',
'IiwgbWFuZykKICAgIGlmIG5vdCBtYW5nOgogICAgICAgICMgRG8gUk9ORyAoZGEgbGFuZCwgY2hpbmggbWFzdGVyKSwgbmhh',
'bSBuaGFuaCwgaGF5IG5oYW5oIGN1YSBwYWNrZXQgS0hBQyBjaGFtIGN1bmcgdGVwOgogICAgICAgICMga2hvbmcgbWFuZyBj',
'YSBtb2kgbmFvIGN1YSBnMiB0aGkga2hvbmcgcGhhaSB1bmcgdmllbi4gRG9jIGtob25nIGR1b2MgKE5vbmUpIGN1bmcgdmF5',
'LgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYiZG9pIHR1b25nIGtob25nIHBoYWkgdW5nIHZpZW46IHts',
'ZW4oaGFuZyl9IHRlcCwgY2hhbSB7Y2hhbX0sIGNhIG1vaSAiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg',
'ZiJnMiBtYW5nIHZhbyB7bWFuZyFyfSDigJQgZGEgbGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/IikKICAgIGVsc2U6',
'CiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIERBVCBpZiAobGVuKGhhbmcpIDw9IFRSQU5fVEVQIGFuZCB0aGVtIDw9',
'IFRSQU5fRE9ORykgZWxzZSBUUlVPVCwKICAgICAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IikKCiMgRGlu',
'aCBkYW5oIFRIQVQgbmFtIG8gTjcnIChjYSBtb2kgZzIgbWFuZyB2YW8pLCBLSE9ORyBvICJoYXUgZHVlIGcxIjogZzEgZGEg',
'bGFuZCBuZW4gbW9pIG5oYW5oIGRldQojIGxhIGhhdSBkdWUuIERvbmcgZGF1IGtob2kgZGFuIHBoYWkgdHUga2hhaSB0aGVv',
'IGtldCBxdWEgYXkgKGRvIGR1b2M6IG1hc3RlciA0NDYyMGU4IG1vIGtob2kgYmFuZwojICJUSEUgSEUgRE8gRFVPQzogZzIi',
'LCBKU09OICJ0aGVfaGUiOiAiZzIiLCB0cm9uZyBraGkgTjcnIGRhIGtldCBsdWFuICJraG9uZyBwaGFpIHVuZyB2aWVuIiku',
'CiMgTmhhbiBjaGkgZHVvYyBub2kgRFVORyBjYWkgZG8gZHVvYzogYFtdYCBraG9uZyB0YWNoICJkYSBsYW5kIiBraG9pICJu',
'aGFtIG5oYW5oIi8icGFja2V0IGtoYWMiIChkbwojIGR1b2MgdHJlbiAyMDI2LTA5LTMwYjogdW5nIHZpZW4gMmE2Nzk2OCBE',
'QSBMQU5EIGJpIGdvaSAiS0hPTkcgcGhhaSB1bmcgdmllbiBnMiIpLgppZiB0aGVfaGUgPT0gImcyIiBhbmQgbm90IHNvLmdl',
'dCgiY2FfbW9pX2cyX21hbmdfdmFvIik6CiAgICB0aGVfaGUgPSAoIktIT05HIG1hbmcgY2EgbW9pIGcyIG5hbyAoZGEgbGFu',
'ZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/KSIgaWYgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKSA9PSBbXQogICAg',
'ICAgICAgICAgIGVsc2UgImcyPyAoQ0hVQSBkaW5oIGRhbmggZHVvYyBkb2kgdHVvbmcpIikKICAgIGdoaSgidGhlX2hlIiwg',
'dGhlX2hlKQoKIyBDb25nIG5oYW5oOiBkbyBSSUVORyBraWNoIHRodW9jICh2YWkgZ2lheSkgcm9pIGR1bmcuIER1bmcga2hp',
'IGNhbiB4YWMgbWluaCBsYWkKIyB2ZSBuZW4gbWEga2hvbmcgbXVvbiB0cmEgMjAtNDUgcGh1dCBjaG8gY2EgYm8gdGVzdC4K',
'aWYgIi0tY2hpLWtpY2gtdGh1b2MiIGluIHN5cy5hcmd2OgogICAgaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQogICAgaW5uKCIt',
'LWNoaS1raWNoLXRodW9jOiBDSEkgZG8gY29uZyBraWNoIHRodW9jLiBEYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0g',
'dGh1LiIpCiAgICBpbm4oIi0iICogNzgpCiAgICBmb3IgX3QsIF90dCwgX2N0IGluIGNob3Q6IGlubihmIiAge190dDoxNH0g',
'e190fSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgX2sgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90',
'IGlmIHQgPT0gS0REKQogICAgX3IgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCiAgICBzeXMu',
'ZXhpdCgzIGlmIF9rIGVsc2UgKDEgaWYgX3IgZWxzZSAwKSkKCkNISV9QUk9CRSA9ICItLWNoaS1wcm9iZSIgaW4gc3lzLmFy',
'Z3YgICAgIyBibyBxdWEgYm8gdGVzdCArIE43OyBnaXUgMCwgMSwgMwojIC0tLS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVzdCBk',
'YXkgZHUgLS0tLS0tLS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5u',
'KCIyLiBCTyBURVNUIERBWSBEVSAoMTAtNDAgcGh1dCkiKQogICAgcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1',
'Ymxpc2hfdGVzdC5weSJdLCBnb2MpCiAgICBnaGkoInJjX3N1aXRlIiwgcmNfbikKICAgIG0gPSBSWF9UT05HLnNlYXJjaChv',
'dXRfbikKICAgIGlubigiICByYyA9IiwgcmNfbiwgInwiLCBtLmdyb3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9j',
'IGRvbmcgdG9uZyBrZXQpIikKICAgIGlmIG06CiAgICAgICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGkoInRy',
'ZW4iLCBpbnQobS5ncm91cCgyKSkpOyBnaGkoImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKICAgIGRvX2hldCwgZ2Ms',
'IHRpbiA9IGRvY19kbyhvdXRfbikKICAgIGdoaSgic29fY2FfZG8iLCBsZW4oZG9faGV0KSk7IGdoaSgibGlldF9rZV9kYXlf',
'ZHUiLCB0aW4pCiAgICBmb3IgZyBpbiBnYzogaW5uKCIgICAqIiwgZykKICAgIGlubigiIik7IGlubihmIiAgPT09IHtsZW4o',
'ZG9faGV0KX0gQ0EgRE8gPT09IikKICAgIGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaW5u',
'KGYiICAge3Quc3BsaXQoJ18nKVswXTo3fSB7dH0iKTsgaW5uKGYiICAgICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCiAg',
'ICBnaGkoImRvX2x5X2RvIiwge3Q6IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQogICAgIyAtLS0tIENIT1Q6',
'IG1vaSBjYSBETyBwaGFpIEdJQUkgVEhJQ0ggRFVPQyAtLS0tCiAgICAjIFRoaWV1IGNob3QgbmF5LCBibyBkbyBpbiBkYW5o',
'IHNhY2ggZG8gcm9pIHZhbiB0aG9hdCByYz0wLiBEbyBkdW5nIGxhIGxvaSBkYSB4YXkgcmE6CiAgICAjIGx1b3QgV2luZG93',
'cyAxOS0wOSBjbyB0MTcxIERPIG1hIGJvIGRvIGJhbyAiREFUIDEwIHwgVFJVT1QgMCIgdmEgcmM9MC4KICAgIGRlZiBfa2hv',
'YSh0KTogcmV0dXJuIHQuc3BsaXQoIl8iKVswXQogICAgZG9fcGFja2V0LCBkb19sYSwgZG9fdGhpZXVfY29uZ19jdSA9IFtd',
'LCBbXSwgW10KICAgIGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaywgbHkgPSBfa2hvYSh0',
'KSwgZG9faGV0W3RdCiAgICAgICAgaWYgayBpbiBDQV9QQUNLRVQ6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9f',
'cGFja2V0LmFwcGVuZCh0KQogICAgICAgIGVsaWYgIktIw5RORyDEkE8gxJDGr+G7okMiIGluIGx5IG9yICJ0aGnhur91IGAi',
'IGluIGx5OiAgZG9fdGhpZXVfY29uZ19jdS5hcHBlbmQodCkKICAgICAgICBlbGlmIGsgaW4gTkdPQUlfUEhBTV9WSTogICAg',
'ICAgICAgICAgICAgICAgICAgICBwYXNzCiAgICAgICAgZWxzZTogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgICAgZG9fbGEuYXBwZW5kKHQpCiAgICBnaGkoImRvX3BhY2tldCIsIGRvX3BhY2tldCk7IGdoaSgiZG9fbGEiLCBk',
'b19sYSk7IGdoaSgiZG9fdGhpZXVfY29uZ19jdSIsIGRvX3RoaWV1X2NvbmdfY3UpCiAgICBpbm4oIiIpCiAgICBpbm4oZiIg',
'IGNhIERPIHRodW9jIENISU5IIHBhY2tldCBuYXkgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF0gb3IgJ2tob25n',
'IGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBuZ29haSBwaGFtIHZpIChyMyBraGFpKToge1tfa2hvYSh4KSBmb3IgeCBpbiBz',
'b3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpIGlmIF9raG9hKHgpIGluIE5HT0FJX1BIQU1fVkldfSIpCiAgICBpbm4oZiIgIGNh',
'IERPIHZpIFRISUVVIENPTkcgQ1UgICAgICAgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9yICdr',
'aG9uZyBjbyd9IikKICAgIGlubihmIiAgY2EgRE8gTEEgKGtob25nIGdpYWkgdGhpY2ggZHVvYyk6IHtbX2tob2EoeCkgZm9y',
'IHggaW4gZG9fbGFdIG9yICdraG9uZyBjbyd9IikKICAgICMgLS0tLSBDSE9UOiBwaGVwIGRvIHBoYWkgVFJPTiB0cnVvYyBr',
'aGkgbW90IGNodSBEQVQgbmFvIGR1b2MgcGhhdCAtLS0tCiAgICAjIEJhbiB0cnVvYyBjaGkgSU4gYHRpbmAvYHJjX3N1aXRl',
'YDogYm8gdGVzdCBjaGV0IGdpdWEgdDE3MSAocmM9MTM0LCBraG9uZyBkb25nIHRvbmcpCiAgICAjIHZhbiByYSAiREFUIDEy',
'IHwgVFJVT1QgMCIgcmM9MDsgY2EgUEFDS0VUIHZhbmcgbWF0IGhheSBiaSBCTyBRVUEgY3VuZyBkdW9jIGNoYW0gbmh1CiAg',
'ICAjICJraG9uZyBkbyIuIFZhbmcgbWF0IGtob25nIHBoYWkgImtob25nIGRvIiDigJQgbGEgS0hPTkcgRE8gRFVPQy4KICAg',
'IHZhbmcgPSBbdCBmb3IgdCBpbiBzb3J0ZWQoQ0FfUEFDS0VULCBrZXk9c29fY2EpIGlmIG1hdV9jYShvdXRfbiwgdCkgbm90',
'IGluICgiUVVBIiwgIkRPIildCiAgICBseV9rZGQgPSBbXQogICAgaWYgbm90IHRpbjogbHlfa2RkLmFwcGVuZCgiZGFuaCBz',
'YWNoIGRvIEtIT05HIGRheSBkdSIpCiAgICBpZiByY19uIG5vdCBpbiAoMCwgMSkgb3IgKHJjX24gPT0gMSkgIT0gYm9vbChk',
'b19oZXQpOgogICAgICAgIGx5X2tkZC5hcHBlbmQoZiJyYyBibyB0ZXN0PXtyY19ufSBraG9uZyBraG9wIHtsZW4oZG9faGV0',
'KX0gY2EgRE8gZG9jIGR1b2MiKQogICAgaWYgdmFuZzogbHlfa2RkLmFwcGVuZChmImNhIFBBQ0tFVCB2YW5nL2JvIHF1YTog',
'e3Zhbmd9IikKICAgIGdoaSgiY2FfcGFja2V0X3ZhbmciLCB2YW5nKTsgZ2hpKCJseV9kb19jaHVhX3Ryb24iLCBseV9rZGQp',
'CiAgICBpZiBseV9rZGQ6IGtldCgiQm8gdGVzdCBjaGF5IFRST04gdmEgZG9jIERVIiwgS0RELCAiOyAiLmpvaW4obHlfa2Rk',
'KSkKICAgIGNodWFfdHJvbiA9IEtERCBpZiBseV9rZGQgZWxzZSBEQVQKICAgIGtldCgiS2hvbmcgY2EgbmFvIGN1YSBQQUNL',
'RVQgYmkgRE8iLCBjaHVhX3Ryb24gaWYgbm90IGRvX3BhY2tldCBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19w',
'YWNrZXQgZWxzZSBmIkRPOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF19IOKAlCBiYW4gdmEgQ0hVQSB4b25nIikK',
'ICAgIGtldCgiTW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MiLCBjaHVhX3Ryb24gaWYgbm90IGRvX2xhIGVsc2UgVFJV',
'T1QsCiAgICAgICAgIiIgaWYgbm90IGRvX2xhIGVsc2UgZiJsYToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV19IikKICAg',
'IGlmIGRvX3RoaWV1X2NvbmdfY3U6CiAgICAgICAga2V0KCJDb25nIGN1IGRheSBkdSBkZSBkbyIsIEtERCwgZiJ0aGlldSBj',
'b25nIGN1IGNobyB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdfSIpCgogICAgYnEgPSBzb3J0ZWQoe3Qg',
'Zm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0X24pfSwga2V5PXNvX2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBicSkK',
'ICAgIGlubigiIik7IGlubihmIiAgQk8gUVVBICh7bGVuKGJxKX0pOiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19',
'IikKCiAgICBpbm4oIiIpOyBpbm4oIiAgTjEtTjQgKHQxNjUtdDE2OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBu',
'YXkgbGEgY2hpIGJhbyBob2kgcXV5OiIpCiAgICBiNCA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBTU9JfTsg',
'Z2hpKCJjYV9tb2kiLCBiNCkKICAgIGZvciB0IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCiAgICAjIEJP',
'X1FVQS92YW5nIGxhIENIVUEgQ0hBWSwga2hvbmcgcGhhaSBETzogY2hpIG1vdCBjYSBETyBtb2kgZHVvYyBwaGF0IFRSVU9U',
'LgogICAga2V0KCJOMS1ONCAodDE2NS10MTY4KSIsIERBVCBpZiBhbGwodiA9PSAiUVVBIiBmb3IgdiBpbiBiNC52YWx1ZXMo',
'KSkKICAgICAgICBlbHNlIChUUlVPVCBpZiBhbnkodiA9PSAiRE8iIGZvciB2IGluIGI0LnZhbHVlcygpKSBlbHNlIEtERCks',
'IHN0cihiNCkpCgogICAgaW5uKCIiKTsgaW5uKCIgIDE1IGNhIHR1bmcgZG8gdHJlbiBDSToiKQogICAgYjE1ID0ge3Q6IG1h',
'dV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0ExNX07IGdoaSgiY2ExNSIsIGIxNSkKICAgIGlubigiICAgICIgKyAiICAiLmpv',
'aW4oZiJ7dH06e2IxNVt0XX0iIGZvciB0IGluIENBMTUpKQoKICAgICMgdDEzNiDigJQgTjEyIGRvIEdJQU4gVElFUCBxdWEg',
'a2V0IHF1YSBjYQogICAgdDEzNl90ZW4gPSBuZXh0KCh0IGZvciB0IGluIGRvX2hldCBpZiB0LnN0YXJ0c3dpdGgoInQxMzYi',
'KSksIE5vbmUpCiAgICBpZiBiMTUuZ2V0KCJ0MTM2IikgPT0gIlFVQSI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtl',
'dCBxdWEgY2EpIiwgREFULCAidDEzNiBRVUEiKQogICAgZWxpZiBiMTUuZ2V0KCJ0MTM2IikgIT0gIkRPIjoKICAgICAgICBr',
'ZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBLREQsIGYidDEzNiA9IHtiMTUuZ2V0KCd0MTM2Jykhcn0g4oCUIGto',
'b25nIGNoYXkva2hvbmcgdGhheSIpCiAgICBlbHNlOgogICAgICAgIGx5ID0gZG9faGV0LmdldCh0MTM2X3RlbiwgIiIpCiAg',
'ICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgVFJVT1QsIGYiRE86IHtseVs6OTBdfSIpCgojIC0tLS0t',
'LS0tLS0tLS0tLS0gMy4gcHJvYmUgVEhBTkcgdmFvIGhhbSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3',
'OCk7IGlubigiMy4gUFJPQkUgVEhBTkcg4oCUIGdvaSBfZ2l0X3dpbmRvd3Mgdm9pIHRoYW0gc28gdGllbSIpCnNwZWMgPSBp',
'bXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHA1NDEiLCBzdHIodGVwKSkKbHAgPSBpbXBvcnRsaWIu',
'dXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMpOyBzcGVjLmxvYWRlci5leGVjX21vZHVsZShscCkKc2lnID0gaW5zcGVjdC5z',
'aWduYXR1cmUobHAuX2dpdF93aW5kb3dzKQpnaGkoInRoYW1fc29fX2dpdF93aW5kb3dzIiwgbGlzdChzaWcucGFyYW1ldGVy',
'cykpCmlubigiICB0aGFtIHNvIGN1YSBfZ2l0X3dpbmRvd3M6IiwgbGlzdChzaWcucGFyYW1ldGVycykpCgpkZWYgZ29pKCoq',
'a3cpOgogICAgIiIiR29pIF9naXRfd2luZG93cywgQkFUIHN0ZGVyciBkZSBtb3QgZG9uZyBjaGFuIGRvYW4ga2hvbmcgZ2ll',
'dCBsdW90IGRvLiIiIgogICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIo',
'ZSk6CiAgICAgICAgciA9IGxwLl9naXRfd2luZG93cygqKmt3KQogICAgcmV0dXJuIHIsIGUuZ2V0dmFsdWUoKQoKIyAtLS0g',
'ZG9pIGNodW5nIHJpZzogcGhhaSB0cmEgbG9pIGR1bmcgbW90IGNhIHRhIEJJRVQgVFJVT0MgZGFwIGFuIC0tLQp3aXRoIHRl',
'bXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICBuZ29haSA9IFBhdGgodCkvIm5nb2FpIjsgbmdvYWkubWtk',
'aXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAg',
'KG5nb2FpLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMSwgXyA9IGdvaShwYXRo',
'PXN0cihuZ29haSksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAoY3cvImdpdC5leGUiKS53cml0',
'ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIyLCBfID0gZ29pKHBhdGg9c3RyKGN3KSwgcHJvZ3JhbV9maWxl',
'cz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKcmlnX29rID0gYm9vbChyMSkgYW5kIHIyIGlzIE5vbmUKZ2hpKCJyaWdfZG9pX2No',
'dW5nIiwgcmlnX29rKQprZXQoIlJJRyBkb2kgY2h1bmcgKGJpZXQgdHJ1b2MgZGFwIGFuKSIsIERBVCBpZiByaWdfb2sgZWxz',
'ZSBLREQsCiAgICBmIm5nb2FpLWN3ZC0+eydOSEFOJyBpZiByMSBlbHNlICdOb25lJ30gfCB0cm9uZy1jd2QtPnsnTkhBTicg',
'aWYgcjIgZWxzZSAnTm9uZSd9IikKaWYgbm90IHJpZ19vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogcmln',
'IHNhaSwgbW9pIGNob3QgZHVvaSBzZSB2byBuZ2hpYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tIE1PSSBDT05HIFBIQUkgVFUg',
'Q0hVTkcgTUlOSCBOTyBDTyBUSEUgRE8gLS0tCiMgQmFpIGhvYyBkYXQgbmhhdCBjdWEgcGFja2V0IG5heTogZG9fbjEwIGJh',
'biBjdSBjaGFtIERBVCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEKIyBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1',
'bmcga2h1eWV0IHRhdCBtYSBOMTAgc2luaCByYSBkZSBiYXQuIE5vIGRlZ2VuZXJhdGUg4oCUCiMgdHJlbiBXaW5kb3dzIG9z',
'LnBhdGhzZXAgREEgbGEgJzsnIG5lbiAidGFjaCBkdW5nIiB2YSAidGFjaCBzYWkiIGNobyBjdW5nIGtldCBxdWEuCiMgTW90',
'IGNvbmcga2hvbmcgdGhlIERPIHRoaSBraG9uZyBwaGFpIGNvbmcsIHZhIG5vIG5ndXkgaGllbSBob24ga2hvbmcgY28gY29u',
'Zzogbm8KIyBwaGF0IHJhIG1vdCBjaHUgREFULgojCiMgTmVuIHRydW9jIGtoaSBEVU5HIG5hbSBjb25nIG5heSBkZSBwaGFu',
'IHF1eWV0LCBiYXQgdHVuZyBjb25nIGdpZXQgbW90IGRvdCBiaWVuIGRhCiMgYmlldCB0cm9uZy4gQ29uZyBuYW8ga2hvbmcg',
'Z2lldCBkdW9jIHRoaSBjaHUgREFUIGN1YSBubyBiaSBIQSB4dW9uZyBLSE9ORyBETyBEVU9DOwojIFRSVU9UIGdpdSBuZ3V5',
'ZW4gKHF1YW4gc2F0IHRydWMgdGllcCwgdmQuIGcxIHZhbiBuaGFuIGdpdC5iYXQpLiBEb3QgYmllbiBjaGF5IHRyZW4gQkFO',
'IFNBTyBUQU07IGNheSB0aGF0IGtob25nIGJpCiMgZHVuZyB0b2kgKGN1bmcga3kgbHVhdCBuaHUgTjcpLgpET1RfQklFTl9U',
'VV9LSUVNID0gWwogICAgKCJOOCIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgJ2lmIGNoaV9kaW5oIGFuZCBQYXRo',
'KGNoaV9kaW5oKS5uYW1lLmxvd2VyKCkgPT0gImdpdC5leGUiIGFuZCBob3BfbGUoY2hpX2RpbmgpOicsCiAgICAgImlmIGNo',
'aV9kaW5oIGFuZCBob3BfbGUoY2hpX2RpbmgpOiIpLAogICAgKCJOOSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAg',
'ImQgPSBkX3Jhdy5zdHJpcCgpLnN0cmlwKCdcIicpIiwgImQgPSBkX3Jhdy5zdHJpcCgpIiksCiAgICAoIk4xMCIsICJvcHMv',
'bGVhc2VfcHVibGlzaC5weSIsCiAgICAgInNlcCA9IG9zLnBhdGhzZXAgaWYgcGhhbl9jYWNoIGlzIE5vbmUgZWxzZSBwaGFu',
'X2NhY2giLCAic2VwID0gb3MucGF0aHNlcCIpLAogICAgKCJOMTEiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAiaWYgY2hh',
'bl9kb2FuIGlzIG5vdCBOb25lOiIsICJpZiBGYWxzZToiKSwKICAgICgiTjEyIiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3Qu',
'cHkiLAogICAgICdnaXRfcGF0aD0iLy9raG9uZy1jby9naXQiJywgJ2dpdF9wYXRoPSIva2hvbmctY28vZ2l0IicpLApdCmlu',
'bigiIik7IGlubigiICB0dSBraWVtIGNvbmcg4oCUIG1vaSBjb25nIHBoYWkgZ2lldCBkdW9jIG1vdCBkb3QgYmllbiBkYSBi',
'aWV0OiIpCmdpZXQgPSB7fQpmb3IgbWEsIGR1b25nLCB0aW0sIHRoYXkgaW4gRE9UX0JJRU5fVFVfS0lFTToKICAgIF90ZW4s',
'IF9oYW0gPSBuZXh0KCgoYSwgYikgZm9yIGEsIGIgaW4gUFJPQkUgaWYgYS5zdGFydHN3aXRoKG1hICsgIiAiKSksIChOb25l',
'LCBOb25lKSkKICAgIGlmIF9oYW0gaXMgTm9uZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0g',
'S0hPTkcgRE8gRFVPQzoga2hvbmcgdGltIHRoYXkgcHJvYmUgdGVuICd7bWF9IC4uLiciKTsgY29udGludWUKICAgIHRyeToK',
'ICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIF90OgogICAgICAgICAgICBfYyA9IFBhdGgo',
'X3QpLyJjYXkiOyBzaHV0aWwuY29weXRyZWUoZ29jLyJvcHMiLCBfYy8ib3BzIikKICAgICAgICAgICAgX2YgPSBfYy9kdW9u',
'ZzsgX25kID0gX2YucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIGlmIF9uZC5jb3VudCh0aW0pICE9',
'IDE6CiAgICAgICAgICAgICAgICBnaWV0W21hXSA9IE5vbmUKICAgICAgICAgICAgICAgIGlubihmIiAgICB7bWE6NH0gS0hP',
'TkcgRE8gRFVPQzogbWF1IGRvdCBiaWVuIGtob3Age19uZC5jb3VudCh0aW0pfSBsYW4gKG1vbmcgMSkiCiAgICAgICAgICAg',
'ICAgICAgICAgZiIg4oCUIG1hIG5ndW9uIGRhIGRvaSwgZG90IGJpZW4gbmF5IGhldCB5IG5naGlhIik7IGNvbnRpbnVlCiAg',
'ICAgICAgICAgIF9mLndyaXRlX3RleHQoX25kLnJlcGxhY2UodGltLCB0aGF5LCAxKSwgZW5jb2Rpbmc9InV0Zi04IikKICAg',
'ICAgICAgICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX2RiXyIgKyBtYSwgc3Ry',
'KF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICAgICAgICAgIF9tID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zy',
'b21fc3BlYyhfc3ApOyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9tKQogICAgICAgICAgICBkZWYgX2dvaV9kYigqKmt3KToK',
'ICAgICAgICAgICAgICAgIF9lID0gaW8uU3RyaW5nSU8oKQogICAgICAgICAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGly',
'ZWN0X3N0ZGVycihfZSk6CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIF9tLl9naXRfd2luZG93cygqKmt3KSwgX2UuZ2V0',
'dmFsdWUoKQogICAgICAgICAgICBfdHQsIF9jdCwgXyA9IF9oYW0oX2dvaV9kYiwgaW5zcGVjdC5zaWduYXR1cmUoX20uX2dp',
'dF93aW5kb3dzKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3Qu',
'cHkiKQogICAgICAgIGdpZXRbbWFdID0gKF90dCA9PSBUUlVPVCkKICAgICAgICBpbm4oZiIgICAge21hOjR9IGRvdCBiaWVu',
'IC0+IHtfdHQ6MTR9IHsnR0lFVCBEVU9DJyBpZiBfdHQgPT0gVFJVT1QgZWxzZSAnU09ORyBTT1QnfSIKICAgICAgICAgICAg',
'KyAoZiIgICAoe19jdH0pIiBpZiBfY3QgZWxzZSAiIikpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAgICAgIGdp',
'ZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiB7dHlwZShfZSkuX19uYW1lX199OiB7X2V9',
'IikKZ2hpKCJjb25nX2dpZXRfZHVvY19kb3RfYmllbiIsIGdpZXQpCgpmb3IgdGVuLCAodHQsIGN0LCBkbCkgaW4gWyh0LCBm',
'KGdvaSwgc2lnLCB0ZXB0KSkgZm9yIHQsIGYgaW4gUFJPQkVdOgogICAgZ2hpKCJwcm9iZV8iICsgdGVuLnNwbGl0KClbMF0u',
'bG93ZXIoKSwgZGwpCiAgICBpZiBpc2luc3RhbmNlKGRsLCBkaWN0KToKICAgICAgICBmb3IgaywgdiBpbiBkbC5pdGVtcygp',
'OiBpbm4oZiIgICAge2s6MzR9OiB7dn0iKQogICAgbWEgPSB0ZW4uc3BsaXQoKVswXQogICAgaWYgZ2lldC5nZXQobWEpIGlz',
'IG5vdCBUcnVlIGFuZCB0dCA9PSBEQVQ6CiAgICAgICAgIyBEQVQgdHUgbW90IGNvbmcgY2h1YSBjaHVuZyBtaW5oIGR1b2Mg',
'bGEgYmlldCBETyB0aGkga2hvbmcgZGFuZyB0aW4gaG9uIEtERC4KICAgICAgICBrZXQodGVuLCBLREQsIGYiY29uZyBLSE9O',
'RyBnaWV0IGR1b2MgZG90IGJpZW4gY3VhIGNoaW5oIG5vICh7Z2lldC5nZXQobWEpIXJ9KSIKICAgICAgICAgICAgICAgICAg',
'ICAgIGYiIC0+IGNodSBEQVQgbmF5IGtob25nIGNvIGdpYSB0cmkiKQogICAgZWxzZToKICAgICAgICBrZXQodGVuLCB0dCwg',
'Y3QpCgojIC0tLS0tLS0tLS0tLS0tLS0gNC4gTjcgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAtLS0tLS0tLS0tLS0tLS0t',
'CmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjQuIE43IOKAlCBkb3QgYmllbiB0',
'cmVuIEJBTiBTQU8gVEFNIChjYXkgdGhhdCBLSE9ORyBiaSBkdW5nIHRvaSkiKQogICAgdHJ1b2MgPSB0ZXAucmVhZF90ZXh0',
'KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4pCiAgICBnaGkoIm43X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIgIHNv',
'IGRvbmcga2hvcCB7TUFVX1dJTiFyfTogVFJVT0MgPSB7dHJ1b2N9IFttb25nIDFdIikKICAgIGlmIHRydW9jICE9IDE6CiAg',
'ICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCBmIm1hdSB4dWF0IGhpZW4ge3RydW9jfSBsYW4s',
'IGtob25nIHBoYWkgMSIpCiAgICBlbHNlOgogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMg',
'dG1wOgogICAgICAgICAgICBzYW8gPSBQYXRoKHRtcCkvImNheSIKICAgICAgICAgICAgc2h1dGlsLmNvcHl0cmVlKGdvYywg',
'c2FvLCBpZ25vcmU9c2h1dGlsLmlnbm9yZV9wYXR0ZXJucygiLmdpdCIsICJfX3B5Y2FjaGVfXyIsICIqLnB5YyIpKQogICAg',
'ICAgICAgICBmMiA9IHNhby8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIKICAgICAgICAgICAgZjIud3JpdGVfdGV4dChmMi5y',
'ZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikucmVwbGFjZShNQVVfV0lOLCAiaWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1dGYt',
'OCIpCiAgICAgICAgICAgIHNhdSA9IGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKTsgZ2hp',
'KCJuN19zYXUiLCBzYXUpCiAgICAgICAgICAgIGlubihmIiAgU0FVIChkYSBkb3QgYmllbikgPSB7c2F1fSBbbW9uZyAwXSIp',
'CiAgICAgICAgICAgIGlmIHNhdSAhPSAwOgogICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dz',
'IiwgS0RELCAiZG90IGJpZW4gS0hPTkcgYXAgZHVvYyIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICByY19t',
'LCBvdXRfbSA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIHNhbykKICAgICAgICAgICAgICAgIG0xNjUg',
'PSBtYXVfY2Eob3V0X20sICJ0MTY1Iik7IGRtLCBfLCBfID0gZG9jX2RvKG91dF9tKQogICAgICAgICAgICAgICAgdGVuMTY1',
'ID0gbmV4dCgodCBmb3IgdCBpbiBkbSBpZiB0LnN0YXJ0c3dpdGgoInQxNjUiKSksIE5vbmUpCiAgICAgICAgICAgICAgICBs',
'eSA9IChkbS5nZXQodGVuMTY1KSBvciAiIikKICAgICAgICAgICAgICAgIGdoaSgibjdfdDE2NSIsIG0xNjUpOyBnaGkoIm43',
'X2x5X2RvIiwgbHlbOjIwMF0pCiAgICAgICAgICAgICAgICBpbm4oZiIgIHQxNjUgc2F1IGRvdCBiaWVuOiB7bTE2NX0gfCB7',
'bHlbOjExMF19IikKICAgICAgICAgICAgICAgIGR1bmdfbHlfZG8gPSAiUEFUSCB0IiBpbiBseSBvciAiL3Vzci9iaW4iIGlu',
'IGx5CiAgICAgICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBEQVQgaWYgKG0xNjUgPT0gIkRP',
'IiBhbmQgZHVuZ19seV9kbykgZWxzZQogICAgICAgICAgICAgICAgICAgIChUUlVPVCBpZiBtMTY1ID09ICJETyIgZWxzZSBL',
'REQpLAogICAgICAgICAgICAgICAgICAgICJnaWV0IGR1bmcgbHkgZG8iIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlf',
'ZG8pCiAgICAgICAgICAgICAgICAgICAgZWxzZSAoIkRPIG5odW5nIEtIT05HIGR1bmcgbHkgZG8gLT4gdGluIGR1bmcgZ2lh',
'IiBpZiBtMTY1ID09ICJETyIgZWxzZSAia2hvbmcgZG9jIGR1b2MgdDE2NSIpKQoKIyAtLS0tLS0tLS0tLS0tLS0tIEtFVCBM',
'VUFOIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQppbm4oZiJUSEUgSEUgRE8gRFVPQzoge3RoZV9o',
'ZX0gICBIRUFEPXtoZWFkWzoxMl19IikKIyBLaG9pIGRhbiBjaG8gcmV2aWV3ZXIgYmF0IGRhdSBvIGRvbmcgdHJlbiwgbmVu',
'IENIRSBETyBwaGFpIG5hbSBOR0FZIGR1b2kgbm86IGtob25nIGNvIGRvbmcgbmF5CiMgdGhpIG1vdCBsdW90IC0tY2hpLXBy',
'b2JlIGluICJEQVQgNyB8IFRSVU9UIDAgfCBLSE9ORyBETyBEVU9DIDAiIHJjPTAgbWEga2hvbmcgbm9pIGxhIGNodWEgY2hh',
'eSBibyB0ZXN0LgpnaGkoImNoZV9kbyIsICJjaGktcHJvYmUiIGlmIENISV9QUk9CRSBlbHNlICJkYXktZHUiKQppZiBDSElf',
'UFJPQkU6CiAgICBpbm4oIi0tY2hpLXByb2JlOiBDSEkgZG8gbXVjIDAsIDEsIDMuIEJvIHRlc3QsIE4xLU40LCB0MTM2LCBO',
'NyBLSE9ORyBjaGF5IC0gZGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQppZiB0aGVfaGUgPT0gImcxIjoK',
'ICAgIGlubigiTFVVIFk6IGRheSBsYSBORU4gRE8gKGcxKSwgS0hPTkcgcGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hvdCBO',
'OC1OMTIgZHVvaSBkYXkiKQogICAgaW5uKCIgICAgICAgVFJVT1QgbGEgRFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEgbmh1',
'bmcgbG8gZzIgc2luaCByYSBkZSB2w6EuIikKaW5uKCItIiAqIDc4KQpmb3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAgIGlu',
'bihmIiAge3R0OjE0fSB7dGVufSIgKyAoZiIgICB7Y3R9IiBpZiBjdCBlbHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3IgXywg',
'dCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQpuX3RydW90ID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRS',
'VU9UKQppbm4oIi0iICogNzgpCmlubihmIiAgREFUIHtzdW0oMSBmb3IgXyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8IFRS',
'VU9UIHtuX3RydW90fSB8IEtIT05HIERPIERVT0Mge25fa2RkfSIpCmlubihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgnc29f',
'Y2FfZG8nKX0gfCBkYW5oIHNhY2ggZGF5IGR1OiB7J0NPJyBpZiBzby5nZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAnS0hP',
'TkcgRE8gRFVPQyd9IikKaW5uKGYiICBBZG1pbmlzdHJhdG9yOiB7c28uZ2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxpbms6',
'IHtzby5nZXQoJ3N5bWxpbmtfZHVvYycpfSIpCmlubigiIik7IGlubigiLS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5BWSBW',
'RSBDSE8gUkVWSUVXRVIgLS0tIikKZ2hpKCJjaG90IiwgW3sidGVuIjogYSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3RpZXQi',
'OiBjfSBmb3IgYSwgYiwgYyBpbiBjaG90XSkKaW5uKGpzb24uZHVtcHMoc28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50',
'PTEsIGRlZmF1bHQ9c3RyKSkKIyByYzogMCA9IG1vaSBjaG90IERBVCB8IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNvIGNo',
'b3QgS0hPTkcgRE8gRFVPQyAodXUgdGllbiBiYW8gZG9uZykKc3lzLmV4aXQoMyBpZiBuX2tkZCBlbHNlICgxIGlmIG5fdHJ1',
'b3QgZWxzZSAwKSkK'
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
