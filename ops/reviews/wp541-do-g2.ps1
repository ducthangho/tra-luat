# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
# Luot DAY DU can SAN mot python >= 3.9 CO PyYAML (pip install pyyaml): ban nhung python.org ma tep nay tu tai
# KHONG co PyYAML/pip, nen no chi du cho -ChiKichThuoc / -ChiProbe. Thieu thi dung o buoc cong cu, rc=3.
# Luot DAY DU con can `bash` (Git Bash), `actionlint`, `shellcheck` tren PATH: tep nay KHONG tu cai chung; bo do hoi
# ngay o muc 0 va dung rc=3 neu thieu (khong doi het bo test moi biet).
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
# Bien PYTHON* bi bo o buoc cong cu, de TRA LAI khi ra: Dung, trap, -ChiGiaiNen, cuoi tep, VA Ctrl+C (khoi `finally` boc tu
# buoc cong cu toi het tep). Goi bang `& .\wp541-do-g2.ps1` trong mot phien PowerShell DANG MO thi env cua tien trinh nay LA
# env cua phien ay: ban 30f xoa luon PYTHONPATH/PYTHONSTARTUP/PYTHONUTF8 cua phien nguoi do (do tren pwsh 7.4, 2026-09-30f: sau
# lenh ca ba deu RONG; ban 30e: giu nguyen). Ban 30g chi tra o bon loi ra co `exit`: Ctrl+C giua luot do khong qua `trap` nen
# phien van mat ca ba, va PYTHONUNBUFFERED=1 cua buoc 5 o lai (do tren pwsh 7.4, 2026-09-30g: SIGINT cho nhom tien trinh).
# TraMoiTruong bo MOI PYTHON* (tru ba bien giu) roi dat lai DUNG ban cu, mot lan; $null = CHUA bo gi (Dung o buoc 0 khong
# duoc dung toi phien).
$script:PyEnvCu = $null
function TraMoiTruong {
    if ($null -eq $script:PyEnvCu) { return }
    @(Get-ChildItem Env:) | Where-Object { $_.Name -like 'PYTHON*' -and $_.Name -notin @('PYTHONHOME','PYTHONUSERBASE','PYTHONNOUSERSITE') } |
        ForEach-Object { Remove-Item -LiteralPath ('Env:' + $_.Name) }
    foreach ($k in @($script:PyEnvCu.Keys)) { Set-Item -LiteralPath ('Env:' + $k) -Value $script:PyEnvCu[$k] }
    $script:PyEnvCu = $null
}

# Bat MOI loi khong luong truoc -> rc=3. Vi sao khong de mac dinh: PowerShell tra rc=1
# khi script chet vi ngoai le, ma rc=1 o day DA CO NGHIA "co chot truot". Hai thu khac
# han nhau - mot ben la phep do chay xong va truot, mot ben la phep do chua he chay.
trap {
    Write-Host ''
    Write-Host "KHONG DO DUOC: loi khong luong truoc - $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  tai: $($_.InvocationInfo.ScriptLineNumber): $($_.InvocationInfo.Line.Trim())" -ForegroundColor Red
    Write-Host 'Khong ket luan gi.' -ForegroundColor Red
    TraMoiTruong
    exit 3
}

# ---------------------------------------------------------------- hang so DA DO
$Url        = 'https://github.com/ducthangho/tra-luat'
$ShaBoDo    = 'd903d263b951d44359d2f10632f81ef0f3c028f0ceec41225c2a99a370d53522'      # SHA-256 cua bo do Python nhung ben duoi

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
    TraMoiTruong
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
        # Thong bao loi cua git CHI bo userinfo toi `@` DAU TIEN: `url.<u@x:p'<bi mat>@github.com/>.insteadOf` in phan
        # sau ra man hinh (do tren pwsh 7.4, 2026-09-30e: fetch hong => 1 dong). Che toi `@` CUOI qua MOI dong truoc khi in
        # (cung luat IN voi _url_in cua bo do).
        Write-Host (($out | Out-String) -replace '(?s)([A-Za-z][A-Za-z0-9+.-]*://).*@', '$1***@')
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
# Probe PHAI hoi trong moi truong cua tien trinh con: chay() cua bo do chi cho PYTHONHOME/PYTHONUSERBASE/PYTHONNOUSERSITE
# qua. Ban 30e probe voi moi truong DAY DU: `py` co PyYAML CHI qua PYTHONPATH qua probe, roi bo do bao "KHONG co PyYAML
# dung duoc" (rc=3) du `python` ngay sau no CO PyYAML (do tren pwsh 7.4, 2026-09-30e). Bo cac bien ay khoi CHINH tien
# trinh nay: probe, bo do va tien trinh con cung thay mot moi truong. Probe cung bo thu muc hien hanh khoi sys.path: tien
# trinh con chay trong ops/ va bo do tu hoi lai o do, con `yaml.py` o thu muc goi ps1 thi khong duoc loai ung vien nao.
$script:PyEnvCu = @{}
@(Get-ChildItem Env:) | Where-Object { $_.Name -like 'PYTHON*' -and $_.Name -notin @('PYTHONHOME','PYTHONUSERBASE','PYTHONNOUSERSITE') } |
    ForEach-Object { $script:PyEnvCu[$_.Name] = $_.Value; Remove-Item -LiteralPath ('Env:' + $_.Name) }
try {   # Ctrl+C khong qua `trap` nhung CO qua `finally`; `exit` ben trong van giu ma thoat
$ungVien = @('py','python','python3')
if ($Py) { $ungVien = @($Py) + $ungVien }
$luotDayDu = -not ($ChiKichThuoc -or $ChiProbe)
$maThu = 'import sys;print(sys.version.split()[0]);sys.exit(0 if sys.version_info>=(3,9) else 9)'
if ($luotDayDu) { $maThu = "import sys;sys.path[:]=[x for x in sys.path if x];print(sys.version.split()[0]);sys.exit(9) if sys.version_info<(3,9) else None;import yaml;yaml.safe_dump(yaml.safe_load('a: 1'))" }
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
'YzJkMmFiYmRkYmI2ZiIKQkFOX0JPX0RPID0gIjIwMjYtMDktMzBoIiAgICAgICAgICAgICAgIyBkb2kgTU9JIGtoaSBzdWEg',
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
'IGdpdCwgSU4KIyB0aGVvICJ0aHVhIGNvbiBob24gbG8iLiAiQ0EgY2h1b2kiIHBoYWkgZHVuZyBjYSBraGkgY2h1b2kgY28g',
'WFVPTkcgRE9ORzogZ2l0KCkgZG9jIGJhbmcgdGV4dD1UcnVlIG5lbiBDUi9MRiB0cm9uZyBVUkwKIyBkYSB0aGFuaCBMRiwg',
'bWEgYC5gIGtob25nIGtob3AgTEYuIFRva2VuIGRvYyB0dSB0ZXAgQ1JMRiAoYGh0dHBzOi8veC1hY2Nlc3MtdG9rZW46PHRv',
'a2VuPmAgKyBDUiArIGBAZ2l0aHViLmNvbS8uLi5gKQojIHRoaSBiYW4gMzBlIEtIT05HIGNoZSBnaTogaW4gTkdVWUVOIHRv',
'a2VuIG8gZG9uZyBgb3JpZ2luIDpgIHZhIG8gIm9yaWdpbl91cmwiIHRyb25nIGtob2kgSlNPTiBkYW4gKGRvIHRyZW4gMjAy',
'Ni0wOS0zMGUpLgpkZWYgX3VybF9pbih1KTogcmV0dXJuIHJlLnN1YihyIl4oW0EtWmEtel1bQS1aYS16MC05Ky4tXSo6Ly8p',
'Py4qQCIsIHIiXDEqKipAIiwgdSBvciAiIiwgZmxhZ3M9cmUuUykKIyBUaG9uZyBiYW8gbG9pIGN1YSBnaXQgQ0hJIGJvIHVz',
'ZXJpbmZvIHRvaSBgQGAgREFVIFRJRU46IHVzZXJpbmZvIGNvIGBAYCB0cmFuICh2ZC4gdGVuIGRhbmcgbmhhcCBsYQojIGVt',
'YWlsKSB0aGkgcGhhbiBzYXUgdmFuIHJhIHN0ZGVyciBscy1yZW1vdGUsIG1hIHN0ZGVyciBheSBkdW9jIGluIHZhbyBkb25n',
'IEtERCBjdWEgTjcnIChkbyBkdW9jOgojIDIgZG9uZyB0cm9uZyBsb2csIDEgdHJvbmcga2hvaSBkYW4pLiBMYW0gc2FjaCBN',
'T0kgVVJMIHRyb25nIHZhbiBiYW4gdHJ1b2Mga2hpIGluIOKAlCBjaGUgdG9pIGBAYCBDVU9JIHRyZW4KIyBET05HIChjdW5n',
'IGx1YXQgSU4gdm9pIF91cmxfaW46IGtob25nIGNvbiBreSB0dSBkdW5nIG5hbykuIEJhbiAzMGQgZHVuZyBvIGBccyciYCBu',
'ZW4gcGhhbiBnaXQgZGUgbGFpIGNvCiMgYCdgL2AiYC9raG9hbmcgdHJhbmcgKHZkLiBgdUB4OnAnPGJpIG1hdD5AZ2l0aHVi',
'LmNvbWApIFZBTiBsbyDigJQgZG8gdHJlbiAyMDI2LTA5LTMwZDogMiBkb25nIC8gMSB0cm9uZwojIGtob2kgZGFuIC0tY2hp',
'LWtpY2gtdGh1b2MsIDMgLyAyIG8gLS1jaGktcHJvYmUsIG1vaSBkYW5nLgpkZWYgX2FuX3VzZXJpbmZvKHQpOiByZXR1cm4g',
'cmUuc3ViKHIiKFtBLVphLXpdW0EtWmEtejAtOSsuLV0qOi8vKVteXG5dKkAiLCByIlwxKioqQCIsIHQgb3IgIiIpCiMgQ2Eg',
'bmdvYWkgcGhhbSB2aSByMyDCp25nb2FpX3BoYW1fdmkg4oCUIGRvIENISU5IIFNQRUMga2hhaSwga2hvbmcgcGhhaSBibyBk',
'byB0dSBxdXlldC4KIyBEbyBsYSBEQU5IIFNBQ0ggQ0hPIFBIRVA6IGNhIGRvIG5hbyBLSE9ORyBuYW0gdHJvbmcgZGF5IHZh',
'IEtIT05HIHBoYWkgInRoaWV1IGNvbmcgY3UiCiMgdGhpIGxhIFRSVU9ULiBEYW5oIHNhY2ggY2FtIHRoaSBiYW8gZ2lvIGN1',
'bmcgdGhpZXU7IGRhbmggc2FjaCBjaG8gcGhlcCB0aGkgYmlldCB0cnVvYy4KTkdPQUlfUEhBTV9WSSA9IHNldCgidDEzMSB0',
'MTMyIHQxNTAgdDEyNSB0MzUgdDM2IHQzNyB0MzggdDM5IHQ0MCIuc3BsaXQoKSkKIyBDYSBjdWEgQ0hJTkggcGFja2V0IG5h',
'eS4gTW90IGNhIG8gZGF5IG1hIERPIHRoaSBraG9uZyBiYW8gZ2lvIGR1b2MgYm8gcXVhLgpDQV9QQUNLRVQgPSBzZXQoInQx',
'NjUgdDE2NiB0MTY3IHQxNjggdDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpKQojIENhIE1PSSBtYSBnMiB0aGVt',
'IHZhbyAoTjgtTjEyKS4gRG9pIHR1b25nIGRvIHBoYWkgTUFORyBjaHVuZyB2YW86IG1lcmdlLWJhc2UgY2h1YSBjbywgSEVB',
'RCBjby4KQ0FfTU9JX0cyID0gInQxNjkgdDE3MCB0MTcxIHQxNzIgdDE3MyIuc3BsaXQoKQpDQTE1ICA9ICJ0MTI5IHQxMzAg',
'dDEzMSB0MTMyIHQxMzMgdDEzNiB0MTM4IHQxMzkgdDE0NCB0MTQ1IHQxNDYgdDE0NyB0MTQ5IHQxNTAgdDE1MSIuc3BsaXQo',
'KQpDQU1PSSA9ICJ0MTY1IHQxNjYgdDE2NyB0MTY4Ii5zcGxpdCgpCgpEQVQsIFRSVU9ULCBLREQgPSAiREFUIiwgIlRSVU9U',
'IiwgIktIT05HIERPIERVT0MiCnNvLCBjaG90ID0ge30sIFtdCmRlZiBnaGkoaywgdik6IHNvW2tdID0gdjsgcmV0dXJuIHYK',
'ZGVmIGtldCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0PSIiKToKICAgIGNob3QuYXBwZW5kKCh0ZW4sIHRyYW5nX3RoYWks',
'IGNoaV90aWV0KSkKICAgIGlubihmIiAgW3t0cmFuZ190aGFpOjE0fV0ge3Rlbn0iICsgKGYiICAge2NoaV90aWV0fSIgaWYg',
'Y2hpX3RpZXQgZWxzZSAiIikpCiAgICByZXR1cm4gdHJhbmdfdGhhaQoKIyAtLS0tLS0tLS0tLS0tLS0tIGRvYyBsb2cgY3Vh',
'IGJvIHRlc3QgKGJhbiAzLCBkYSBkbyB0cmVuIGxvZyBUSEFUKSAtLS0tLS0tLS0tLS0tLS0tClJYX0RPX0NITyAgPSByZS5j',
'b21waWxlKHIiKD9tKV4hISEgZG8gKFxTKykgKC4qKSQiKQpSWF9ET19DVU9JID0gcmUuY29tcGlsZShyIig/bSleIHsyfShc',
'U3sxLDR9KSB7Mn0oXFMrKTogKC4qKSQiKQpSWF9CT19RVUEgID0gcmUuY29tcGlsZShyIig/bSleIHsyfVxTezEsNn0gUVVB',
'IChcUyspOiAoLiopJCIpCiMgRG9uZyB0b25nIGtldCBUSEFUIG8gREFVIGRvbmcuIENhIERPIGNvIHRoZSBpbiBsYWkgc3Rk',
'b3V0IGN1YSBtb3QgbHVvdCBDT04gKHQxNTUgY2hheSBsYWkgdDAxLCB0NzIvdDk4IGNoYXkKIyAiYm8iKSDigJQgZG9uZyB0',
'b25nIExPTkcgYXkgbmFtIEdJVUEgZG9uZyAoZG86IDIwIGRvbmcgbG9uZyBkZXUgbyBnaXVhIGRvbmcsIGNoaSBkb25nIHRv',
'bmcgdGhhdCBvIGRhdSBkb25nKSwgbWEKIyBgc2VhcmNoYCBraG9uZyBuZW8gYmF0IG5vIFRSVU9DLiBEbyB0cmVuIDIwMjYt',
'MDktMzBjLCAwZWE5NWRlICsgZG90IGJpZW4gbGFtIHQwMSBETzogZG9jIHJhICIwLzEiID0+CiMgImRhbmggc2FjaCBLSE9O',
'RyBkYXkgZHUiLCAiTEVDSCBTTyBIT0M6IHRoaWV1IC0yMCBjYSIsIHRyb25nIGtoaSB0b25nIHRoYXQgMTY2LTE0NT0yMSA9',
'PSAyMSBjYSBkb2MgZHVvYy4KUlhfVE9ORyAgICA9IHJlLmNvbXBpbGUociIoP20pXmxlYXNlX3B1Ymxpc2g6IChcZCspLyhc',
'ZCspXGJbXlxuXSo/PShcZCspLFteXG5dKj89KFxkKykiKQoKZGVmIHNvX2NhKHQpOgogICAgbSA9IHJlLm1hdGNoKHIidChc',
'ZCspIiwgdCk7IHJldHVybiAoaW50KG0uZ3JvdXAoMSkpIGlmIG0gZWxzZSAxMCoqNiwgdCkKCmRlZiBkb2NfZG8ob3V0KToK',
'ICAgIHRhaV9jaG8gPSB7dDogbC5zdHJpcCgpIGZvciB0LCBsIGluIFJYX0RPX0NITy5maW5kYWxsKG91dCl9CiAgICBibyA9',
'IHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91dCl9CiAgICBjdW9pID0ge3Q6IGwuc3RyaXAoKSBmb3IgXywg',
'dCwgbCBpbiBSWF9ET19DVU9JLmZpbmRhbGwob3V0KSBpZiB0IG5vdCBpbiBib30KICAgIGhvcCA9IGRpY3QoY3VvaSk7IGhv',
'cC51cGRhdGUodGFpX2NobykKICAgIGdjLCB0aW4gPSBbXSwgVHJ1ZQogICAgaWYgc2V0KHRhaV9jaG8pICE9IHNldChjdW9p',
'KToKICAgICAgICBnYy5hcHBlbmQoZiJoYWkgbmd1b24gTEVDSDogY2hpLXRhaS1jaG89e3NvcnRlZChzZXQodGFpX2Nobykt',
'c2V0KGN1b2kpKX0gY2hpLWN1b2k9e3NvcnRlZChzZXQoY3VvaSktc2V0KHRhaV9jaG8pKX0iKQogICAgICAgIHRpbiA9IEZh',
'bHNlCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0KQogICAgaWYgbm90IG06CiAgICAgICAgZ2MuYXBwZW5kKCJLSE9ORyBk',
'b2MgZHVvYyBkb25nIHRvbmcga2V0Iik7IHRpbiA9IEZhbHNlCiAgICBlbHNlOgogICAgICAgIGRhdCwgdHJlbiA9IGludCht',
'Lmdyb3VwKDEpKSwgaW50KG0uZ3JvdXAoMikpCiAgICAgICAgZ2MuYXBwZW5kKGYic28gaG9jOiB7dHJlbn0te2RhdH09e3Ry',
'ZW4tZGF0fSBkbzsgZG9jIGR1b2Mge2xlbihob3ApfSIpCiAgICAgICAgaWYgdHJlbiAtIGRhdCAhPSBsZW4oaG9wKToKICAg',
'ICAgICAgICAgZ2MuYXBwZW5kKGYiTEVDSCBTTyBIT0M6IHRoaWV1IHt0cmVuLWRhdC1sZW4oaG9wKX0gY2EiKTsgdGluID0g',
'RmFsc2UKICAgIHJldHVybiBob3AsIGdjLCB0aW4KCiMgTWF1IGNvIGRvbmcgdG9uZyBMT05HIGdpdWEgZG9uZyAoZGFuZyB0',
'MTU1IGluIGxhaSBsdW90IGNvbik6IGJvIGRvYyBiYXQgZG9uZyB0b25nIERBVSBUSUVOIGxhIHR1IGtpZW0gRE8uCl9NQVUg',
'PSAoIiEhISBkbyB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOIGEgJ2xlYXNlX3B1Ymxpc2g6IDAvMSDEkeG6oXQ7IMSR',
'w6MgY2jhuqF5PTEsIGLhu48gcXVhPTAnXG4iCiAgICAgICAgIiEhISBkbyB0MTUwX3ggV2luRXJyb3IgMTMxNCByZXF1aXJl',
'ZCBwcml2aWxlZ2VcbiIKICAgICAgICAiICBC4buOIFFVQSB0MTMxX3k6IG5lbiBmaXh0dXJlXG4iCiAgICAgICAgIiAgxJDh',
'u44gIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU46IGFcbiIKICAgICAgICAiICDEkOG7jiAgdDE1MF94OiBXaW5FcnJv',
'ciAxMzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICJsZWFzZV9wdWJsaXNoOiAxLzMgxJHhuqF0OyDEkcOjIGNo',
'4bqheT0zLCBi4buPIHF1YT0xXG4iKQoKIyBCaWVuIFBZVEhPTiogY3VhIG1heSBuZ3VvaSBkbyBsb3QgdmFvIGJvIHRlc3Qg',
'bGEgRE9JIEhBTkggVkkgYm8gdGVzdDogUFlUSE9OT1BUSU1JWkUgYm8gbW9pIGBhc3NlcnRgIChkbyB0cmVuCiMgMjAyNi0w',
'OS0zMGM6IGBhc3NlcnQgRmFsc2VgIHF1YSwgcmM9MCk7IGJhbiAzMGQgY2hpIHRydW5nIGhvYSBNT1QgYmllbiBheSwgY29u',
'IFBZVEhPTkRFVk1PREU9MSBsYW0gdDE1NCBETyAyLzQKIyBsYW4gdHJlbiAzLjExIChzYWNoOiA0LzQgUVVBKSA9PiByYz0x',
'ICJUUlVPVCBNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIgY2hvIHVuZyB2aWVuIHNhY2ggKGRvIHRyZW4KIyAyMDI2',
'LTA5LTMwZCkuIERhbmggc2FjaCBDQU0gbHVvbiB0aGlldSBtb3QgYmllbiDigJQgbmVuIGRheSBsYSBkYW5oIHNhY2ggQ0hP',
'IFBIRVA6IGNoaSBnaXUgYmllbiBkZSB0cmluaCB0aG9uZwojIGRpY2ggQ0hBWSB2YSB0aW0gZ29pIERBIENBSTsgUFlUSE9O',
'UEFUSCBLSE9ORyBnaXUgKENJIGtob25nIGNvIG5vKS4gUGhlcCBob2kgZGlldSBraWVuIHRpZW4gcXV5ZXQgbyBtdWMgMAoj',
'IGN1bmcgY2hheSBxdWEgZGF5LCBuZW4gbm8gdGhheSBEVU5HIG1vaSB0cnVvbmcgbWEgYm8gdGVzdCBzZSB0aGF5LgpfUFlf',
'R0lVID0gZnJvemVuc2V0KHsiUFlUSE9OSE9NRSIsICJQWVRIT05VU0VSQkFTRSIsICJQWVRIT05OT1VTRVJTSVRFIn0pCiMg',
'Q2F1IGhpbmggZ2l0IENVQSBOR1VPSSBETyBsb3QgdmFvIGJvIHRlc3QgeSBuaHUgYmllbiBQWVRIT04qOiBjYSB0ZXN0IGdv',
'aSBnaXQgYmFuZyBkaWN0KG9zLmVudmlyb24pLCBuZW4gZG9jIGNhdSBoaW5oCiMgY2EgbmhhbiB2YSBiaWVuIEdJVF8qIGN1',
'YSBtYXkgZG8uIERvIHRyZW4gMjAyNi0wOS0zMGUsIDBlYTk1ZGU6IGBpbml0LmRlZmF1bHRCcmFuY2ggPSBtYWluYCA9PiAx',
'NjMvMTY2LCB0MTM0IHQxMzkgdDE1MQojIERPID0+IHJjPTEgIlRSVU9UIE1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9j',
'IiBjaG8gdW5nIHZpZW4gc2FjaCAoc2FjaDogMTY2LzE2Nikg4oCUIG8gcGhhbSB2aSBnbG9iYWwgTEFOIGhlIHRob25nLgoj',
'IEJvIE1PSSBiaWVuIEdJVF8qIHZhIHRoYXkgZ2xvYmFsIENBIE5IQU4gYmFuZyBnbG9iYWwgQ1VBIENJLiBDSSBLSE9ORyBj',
'byBnbG9iYWwgcm9uZzogam9iIGBnYXRlYCBjdWEgY2kueW1sIChidW9jICJGb3JjZSBMRgojIGNoZWNrb3V0IiwgY2EgdWJ1',
'bnR1IGxhbiB3aW5kb3dzKSBkYXQgZ2xvYmFsIGNvcmUuYXV0b2NybGY9ZmFsc2UsIGNvcmUuZW9sPWxmLCBjb3JlLmFiYnJl',
'dj03IFRSVU9DIGJ1b2MgY2hheSBibyB0ZXN0IOKAlAojIHZpIChjaS55bWw6Ny04IHR1IGtoYWkpIGtob25nIHRhdCB0aGkg',
'cnVubmVyIFdpbmRvd3MgY2hlY2tvdXQgQ1JMRjogYXV0b2NybGY9dHJ1ZSBjdWEgYmFuIGNhaSBHaXQgbyBIRSBUSE9ORy4g',
'QmFuIDMwZgojIGRhdCBnbG9iYWwgPSByb25nIG5lbiBibyB0ZXN0IHRoYXkgYXV0b2NybGY9dHJ1ZSBjb24gQ0kgdGhheSBm',
'YWxzZTogZG8gdHJlbiAyMDI2LTA5LTMwZiwgMGVhOTVkZSwgaGUgdGhvbmcgYXV0b2NybGY9dHJ1ZQojICsgZ2xvYmFsIG5o',
'dSBDSSA9PiBiYW4gMzBlIDE2Ni8xNjYsIGJhbiAzMGYgMTY1LzE2NiAodDE1MCBETyDigJQgY2hpIGtob25nIHRoYW5oIFRS',
'VU9UIHZpIHQxNTAgdGluaCBjbyBuYW0gdHJvbmcKIyBOR09BSV9QSEFNX1ZJKS4gR2xvYmFsIGxhIFRFUCBUQU0gY2h1YSBE',
'VU5HCiMgZ2xvYmFsIGN1YSBDSSBjb25nIGluaXQuZGVmYXVsdEJyYW5jaCBnaGltIHZlIG1hYyBkaW5oIGN1YSBnaXQgKGRh',
'dCBkdW9jIGNhIG8gaGUgdGhvbmcpOiBnbG9iYWwgZGUgbGVuIGhlIHRob25nIG5odSB0cmVuIENJLAojIGNvbiBjYXUgaGlu',
'aCBDVUMgQk8gY3VhIGZpeHR1cmUgdmFuIGRlIGxlbiBnbG9iYWwgKEdJVF9DT05GSUdfQ09VTlQgdGhpIGRlIGxlbiBjYSBj',
'dWMgYm8pLiBEb2kgYnVvYyBheSB0cm9uZyBjaS55bWwgdGhpCiMgZG9pIF9HSVRfR0xPQkFMX0NJLiBHSVRfQ09ORklHX0dM',
'T0JBTCBjaGkgdGhheSBURVAgQ09ORklHOiBpZ25vcmUvYXR0cmlidXRlcyBtYWMgZGluaCAoJFhER19DT05GSUdfSE9NRSBo',
'b2FjIH4vLmNvbmZpZy9naXQvCiMgaWdub3JlfGF0dHJpYnV0ZXMpIGN1YSBuZ3VvaSBkbyBWQU4gYXAgY2hvIGdpdCBjb24g',
'KGRvIHRyZW4gMjAyNi0wOS0zMGcsIDBlYTk1ZGU6IH4vLmNvbmZpZy9naXQvaWdub3JlIGAqLnlhbWxgID0+IGJhbiAzMGcK',
'IyAxNTQvMTY2LCAxMSBjYSAibGEiKTsgQ0kga2hvbmcgY28gdGVwIG5hbyBvIGRvID0+IFhER19DT05GSUdfSE9NRSB0cm8g',
'dmFvIHRodSBtdWMgVEFNIFJPTkcuIENvbiBsYWkgKGtob2EgaGUgdGhvbmcga2hhYykKIyBsYSBnaW9pIGhhbiBkYSBiaWV0',
'LCBraG9uZyBwaGFpIGRhIGRvbmcuCl9HSVRfR0xPQkFMX0NJID0gIltpbml0XVxuXHRkZWZhdWx0QnJhbmNoID0gbWFzdGVy',
'XG5bY29yZV1cblx0YXV0b2NybGYgPSBmYWxzZVxuXHRlb2wgPSBsZlxuXHRhYmJyZXYgPSA3XG4iCmRlZiBjaGF5KGFyZ3Ys',
'IGN3ZCwgcGh1dD02MCk6CiAgICBmZCwgZ2MgPSB0ZW1wZmlsZS5ta3N0ZW1wKHByZWZpeD0id3A1NDEtZ2l0Y29uZmlnLWNp',
'LSIsIHN1ZmZpeD0iLmluaSIpCiAgICB4ZGcgPSBOb25lCiAgICB0cnk6CiAgICAgICAgeGRnID0gdGVtcGZpbGUubWtkdGVt',
'cChwcmVmaXg9IndwNTQxLXhkZy0iKQogICAgICAgIHdpdGggb3MuZmRvcGVuKGZkLCAidyIsIGVuY29kaW5nPSJhc2NpaSIs',
'IG5ld2xpbmU9IlxuIikgYXMgZjogZi53cml0ZShfR0lUX0dMT0JBTF9DSSkKICAgICAgICBtdCA9IHtrOiB2IGZvciBrLCB2',
'IGluIG9zLmVudmlyb24uaXRlbXMoKQogICAgICAgICAgICAgIGlmIG5vdCBrLnVwcGVyKCkuc3RhcnRzd2l0aCgiR0lUXyIp',
'IGFuZCAobm90IGsudXBwZXIoKS5zdGFydHN3aXRoKCJQWVRIT04iKSBvciBrLnVwcGVyKCkgaW4gX1BZX0dJVSl9CiAgICAg',
'ICAgbXQudXBkYXRlKFBZVEhPTlVURjg9IjEiLCBQWVRIT05JT0VOQ09ESU5HPSJ1dGYtOCIsIFBZVEhPTkRPTlRXUklURUJZ',
'VEVDT0RFPSIxIiwgUFlUSE9OVU5CVUZGRVJFRD0iMSIsCiAgICAgICAgICAgICAgICAgIEdJVF9DT05GSUdfR0xPQkFMPWdj',
'LCBYREdfQ09ORklHX0hPTUU9eGRnKQogICAgICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbc3lzLmV4ZWN1dGFibGVdICsgYXJn',
'diwgY3dkPXN0cihjd2QpLCBjYXB0dXJlX291dHB1dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICB0ZXh0PVRy',
'dWUsIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCwgZW52PW10KQogICAgZmlu',
'YWxseToKICAgICAgICB0cnk6IG9zLnJlbW92ZShnYykKICAgICAgICBleGNlcHQgT1NFcnJvcjogcGFzcwogICAgICAgIGlm',
'IHhkZzogc2h1dGlsLnJtdHJlZSh4ZGcsIGlnbm9yZV9lcnJvcnM9VHJ1ZSkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChw',
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
'IikKaWYgbm90IHNodXRpbC53aGljaCgiZ2l0Iik6IGxvaS5hcHBlbmQoImtob25nIGNvIGBnaXRgIHRyb25nIFBBVEgiKQoj',
'IEJvIHRlc3QgKG11YyAyIHZhIE43KSBjYW4gUHlZQU1MOiB0aGlldSBubywgMGVhOTVkZSByYSA5Ni8xNjYgY2EgRE8gKDg5',
'IGJhbyB0aGFuZyAiTm8gbW9kdWxlIG5hbWVkICd5YW1sJyIsCiMgNyBxdWEgbHVvdCBjb247IGNvIFB5WUFNTDogMTY2LzE2',
'NiBRVUEpLiBCbyBkbyBnb2kgY2h1bmcgbGEgImNhIERPIExBIiByb2kgcGhhdCBUUlVPVCDigJQgZG8gdHJlbiAyMDI2LTA5',
'LTMwYy4KIyBEaWV1IGtpZW4gdGllbiBxdXlldCBwaGFpIGhvaSBiYW5nIENISU5IIHRpZW4gdHJpbmggY29uIHNlIGNoYXkg',
'Ym8gdGVzdCAoY2hheSgpOiBjdW5nIG1vaSB0cnVvbmc7IGN3ZCA9IG9wcy8gPQojIHN5cy5wYXRoWzBdIGN1YSBibyB0ZXN0',
'KSB2YSBob2kgRFVORyBEVU9DIGNodSBraG9uZyBob2kgQ08gTUFULiBCYW4gMzBkIGhvaSBgZmluZF9zcGVjKCJ5YW1sIilg',
'IG8gdGllbiB0cmluaAojIE5BWSB2YSBuZ3VvbmcgMy44IHN1eSB0dSBOR1UgUEhBUCAoYDo9YCkg4oCUIGRvIHRyZW4gMjAy',
'Ni0wOS0zMGQsIGNhIGhhaSByYSByYz0xIFRSVU9UIGNobyB1bmcgdmllbiBzYWNoOgojIHRodSBtdWMgZHUgbGlldSBgeWFt',
'bC9gIHRyZW4gUFlUSE9OUEFUSCBxdWEgZmluZF9zcGVjIG1hIGB5YW1sLnNhZmVfZHVtcGAga2hvbmcgY28gKDg3IGNhICJs',
'YSIpOyBweXRob24gMy44LjIwCiMgVEhBVCBjbyBQeVlBTUwsIGJvIHRlc3QgZHVuZyBgc3RyLnJlbW92ZXByZWZpeGAgKDMu',
'OSkgbHVjIENIQVkgKDMzIGNhICJsYSI7IDMuOS4yMzogMTY2LzE2NikuCmlmIG5vdCAoIi0tY2hpLWtpY2gtdGh1b2MiIGlu',
'IHN5cy5hcmd2IG9yICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YpOgogICAgX3JjX2RrLCBfcmFfZGsgPSBjaGF5KFsiLWMi',
'LCAiaW1wb3J0IHN5czsgc3lzLmV4aXQoOSkgaWYgc3lzLnZlcnNpb25faW5mbyA8ICgzLCA5KSBlbHNlIE5vbmU7IGltcG9y',
'dCB5YW1sOyIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiB5YW1sLnNhZmVfZHVtcCh5YW1sLnNhZmVfbG9h',
'ZCgnYTogMScpKSJdLAogICAgICAgICAgICAgICAgICAgICAgICAgIGdvYyAvICJvcHMiIGlmIChnb2MgLyAib3BzIikuaXNf',
'ZGlyKCkgZWxzZSBQYXRoLmN3ZCgpLCBwaHV0PTIpCiAgICBpZiBfcmNfZGsgPT0gOToKICAgICAgICBsb2kuYXBwZW5kKGYi',
'cHl0aG9uIHtzeXMudmVyc2lvbi5zcGxpdCgpWzBdfSA8IDMuOTogYm8gdGVzdCBjdWEgdW5nIHZpZW4gZHVuZyBzdHIucmVt',
'b3ZlcHJlZml4ICgzLjkpIGx1YyBDSEFZIikKICAgIGVsaWYgX3JjX2RrOgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24g',
'bmF5IEtIT05HIGNvIFB5WUFNTCBkdW5nIGR1b2MgKHsoX3JhX2RrLnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10pWy0x',
'XVs6OTBdfSk6IgogICAgICAgICAgICAgICAgICAgZiIgXCJ7c3lzLmV4ZWN1dGFibGV9XCIgLW0gcGlwIGluc3RhbGwgcHl5',
'YW1sIgogICAgICAgICAgICAgICAgICAgIiAoYmFuIG5odW5nIHBzMSB0dSB0YWkgS0hPTkcgY28gcGlwOiBjaGF5IGxhaSB2',
'b2kgLVB5IDxweXRob24gZGEgY28gUHlZQU1MPikiKQogICAgIyBCbyB0ZXN0IGNvbiBnb2kgYHNodXRpbC53aGljaGAgY2hv',
'IGJhc2gvYWN0aW9ubGludC9zaGVsbGNoZWNrICgwZWE5NWRlOiB0MzMgdDEzNyB0MTU5IGNhbiBhY3Rpb25saW50LCB0MTM3',
'IGNhbgogICAgIyBzaGVsbGNoZWNrLCBjYWMgY2EgY2hheSBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggY2FuIGJhc2gpLiBUaGll',
'dSB0aGkgY2FjIGNhIGF5IGluICJLSE9ORyBETyBEVU9DOiB0aGlldSBgLi4uYCIgdmEgYm8gZG8gcmEKICAgICMgcmM9MyDi',
'gJQgbmh1bmcgY2hpIFNBVSBjYSBibyB0ZXN0IGxhbiBONyAoZG8gdHJlbiAyMDI2LTA5LTMwZywgUEFUSCB0aGlldSBhY3Rp',
'b25saW50OiBgQ29uZyBjdSBkYXkgZHUgZGUgZG9gIEtERCwgcmM9MwogICAgIyBzYXUgMiBsdW90IGJvIHRlc3QpLiBDdW5n',
'IGx5IGRvIFB5WUFNTCBkdW9jIGhvaSBvIGRheTogaG9pIFRSVU9DLCBjdW5nIFBBVEggbWEgY2hheSgpIHRydXllbiBjaG8g',
'Ym8gdGVzdC4KICAgIF90aGlldV9jYyA9IFtjIGZvciBjIGluICgiYmFzaCIsICJhY3Rpb25saW50IiwgInNoZWxsY2hlY2si',
'KSBpZiBub3Qgc2h1dGlsLndoaWNoKGMpXQogICAgaWYgX3RoaWV1X2NjOgogICAgICAgIGxvaS5hcHBlbmQoZiJ0aGlldSBj',
'b25nIGN1IGJvIHRlc3QgZ29pIHF1YSBQQVRIOiB7X3RoaWV1X2NjfSAoYWN0aW9ubGludDogb3BzL2NhaV9hY3Rpb25saW50',
'LnNoIHZvaSBBTF9WRVI7IgogICAgICAgICAgICAgICAgICAgIiBiYXNoOiBHaXQgQmFzaCwga2hvbmcgcGhhaSBiYXNoLmV4',
'ZSBjdWEgV1NMKSIpCgpyYywgaGVhZCwgXyA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAiSEVBRCIpCmlmIHJjOiBsb2kuYXBw',
'ZW5kKCJraG9uZyBkb2MgZHVvYyBIRUFEIikKZ2hpKCJoZWFkIiwgaGVhZCkKcmNfYSwgXywgXyA9IGdpdChnb2MsICJtZXJn',
'ZS1iYXNlIiwgIi0taXMtYW5jZXN0b3IiLCBTSEFfRzEsIGhlYWQgb3IgIkhFQUQiKQpsYV9oYXVfZHVlID0gKHJjX2EgPT0g',
'MCkKaWYgaGVhZCA9PSBTSEFfRzE6CiAgICB0aGVfaGUgPSAiZzEiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IERB',
'WSBMQSBnMS4gQ0hVQSBjbyBiYW4gdmEgZzI7IGtldCBxdWEgZHVvaSBsYSBORU4gRE8uIikKZWxpZiBsYV9oYXVfZHVlOgog',
'ICAgdGhlX2hlID0gImcyIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBoYXUgZHVlIGN1YSBnMSAoe1NIQV9HMVs6',
'OF19KTsgdW5nIHZpZW4gZzIgaGF5IGtob25nOiBONycgKG11YyAxKSBkaW5oIGRhbmguIikKZWxzZToKICAgIHRoZV9oZSA9',
'ICI/IjsgbG9pLmFwcGVuZChmIkhFQUQ9e2hlYWRbOjhdfSBLSE9ORyBwaGFpIGcxIHZhIEtIT05HIHBoYWkgaGF1IGR1ZSBj',
'dWEge1NIQV9HMVs6OF19IOKAlCByZWJhc2U/IG5oYW0gbmhhbmg/IikKZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCnJjX3IsIHJl',
'ZnMsIF8gPSBnaXQoZ29jLCAiZm9yLWVhY2gtcmVmIiwgIi0tcG9pbnRzLWF0IiwgaGVhZCBvciAiSEVBRCIsCiAgICAgICAg',
'ICAgICAgICAgICAgIi0tZm9ybWF0PSUocmVmbmFtZTpzaG9ydCkiKQpkc3IgPSBbeCBmb3IgeCBpbiByZWZzLnNwbGl0bGlu',
'ZXMoKSBpZiB4LnN0cmlwKCkgYW5kIHguc3RyaXAoKSAhPSAiZG8tdGFtIl0KZ2hpKCJyZWZfdHJvX3RvaV9oZWFkIiwgZHNy',
'KQppbm4oZiIgIHJlZiB0cm8gdG9pIEhFQUQ6IHsnLCAnLmpvaW4oZHNyKSBpZiBkc3IgZWxzZSAnKGtob25nIHJlZiBuYW8g',
'LSBIRUFEIHJvaSB0dSBkbyknfSIpCgppZiBsb2k6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IG5lbiBkbyBz',
'YWksIEtIT05HIGluIGtldCBsdWFuIG5hby4iKQogICAgZm9yIHggaW4gbG9pOiBpbm4oIiAgLSIsIHgpCiAgICBzeXMuZXhp',
'dCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDEuIGtpY2ggdGh1b2MgKE43JyBjdWEgc3BlYyByMykgLS0tLS0tLS0tLS0tLS0t',
'LQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjEuIEtJQ0ggVEhVT0Mg4oCUIHRyYW4gc3BlYyByMzogPD0gMiB0ZXAg',
'dmEgPD0gNDAwIGRvbmcgdGhlbSIpCiMgVkUgTkVOIFBIQUkgVFVPSSDigJQgdmEgcGhhaSBDSFVORyBNSU5IIGR1b2MgbGEg',
'dHVvaSwga2hvbmcgcGhhaSBnaWEgZGluaC4KIyBCYWkgaG9jIHRyYSBnaWEgMTktMDktMjAyNjogY2xvbmUgdGFpIGR1bmcg',
'Y2hpIGZldGNoIG5oYW5oIGJhbiB2YSwgYG9yaWdpbi9tYXN0ZXJgCiMgZHVuZyB5ZW4gdHUgMTQtMDkgKGMxNmJkMzIsIHNh',
'dSA5NyBjb21taXQpLiBtZXJnZS1iYXNlIHJvaSB2ZSBkdW5nIGRpbmggbWFzdGVyIGN1LAojIG5lbiBkaWZmIE5VT1QgY2Eg',
'OTcgY29tbWl0IG1hc3RlcjogZG8gcmEgNDYgdGVwIC8gKzcxMTggdGhheSB2aSAyIHRlcCAvICszOTcg4oCUCiMgQ1VORyBN',
'T1QgQ09NTUlUIDBlYTk1ZGUuIE1vdCB0aWV1IGNoaSBERUxUQSBtYSB2ZSBuZW4ga2hvbmcgdHVvaSB0aGkga2hvbmcgc2Fp',
'CiMgbGVjaCBtb3QgY2h1dCwgbm8gc2FpIGNhIG1vdCBiYWMgZG8gbG9uLgojIENobyBuZW46IG5lbiBraG9uZyBjaHVuZyBt',
'aW5oIGR1b2MgbGEgdHVvaSA9PiBLSE9ORyBETyBEVU9DIChyYz0zKSwgS0hPTkcgcGhhaSBUUlVPVC4KIyBUUlVPVCBsYSBt',
'b3QgUEhBTiBRVVlFVCB2ZSBiYW4gdmE7IHBoYW4gcXV5ZXQgY2hpIGR1b2MgcGhlcCBwaGF0IHJhIGtoaSBkYSBkbyBkdW9j',
'LgpyY191LCB1cmxfdGhvLCBfID0gZ2l0KGdvYywgInJlbW90ZSIsICJnZXQtdXJsIiwgIm9yaWdpbiIpCnVybF9vLCB1cmxf',
'aW4gPSBfdXJsX3NhY2godXJsX3RobyksIF91cmxfaW4odXJsX3RobykKZ2hpKCJvcmlnaW5fdXJsIiwgdXJsX2luKTsgaW5u',
'KGYiICBvcmlnaW4gICAgICAgOiB7dXJsX2luIG9yICcoa2hvbmcgZG9jIGR1b2MpJ30iKQp1cmxfb2sgPSAobm90IHJjX3Up',
'IGFuZCB1cmxfby5yc3RyaXAoIi8iKSBpbiBVUkxfS0hPX0hPUF9MRQpyY19sciwgb3V0X2xyLCBlcl9sciA9IGdpdChnb2Ms',
'ICJscy1yZW1vdGUiLCAib3JpZ2luIiwgInJlZnMvaGVhZHMvbWFzdGVyIikgaWYgdXJsX29rIGVsc2UgKDEsICIiLCAiIikK',
'ZXJfbHIgPSBfYW5fdXNlcmluZm8oZXJfbHIpCnJjX2xtLCBsbSwgZXJfbG0gICAgID0gZ2l0KGdvYywgInJldi1wYXJzZSIs',
'ICJvcmlnaW4vbWFzdGVyIikKcm0gPSBvdXRfbHIuc3BsaXQoKVswXSBpZiAobm90IHJjX2xyIGFuZCBvdXRfbHIuc3RyaXAo',
'KSkgZWxzZSAiIgppZiBub3QgdXJsX29rOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJvcmlnaW49e3VybF9p',
'biFyfSBLSE9ORyBwaGFpIGtobyB0aGF0IOKAlCAndHVvaScgc28gdm9pIG5vIGtob25nIGNodW5nIG1pbmggZHVvYyBnaSIp',
'CiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIG5vdCBybToKICAgIGtldCgiTjcnIGtpY2ggdGh1',
'b2MiLCBLREQsCiAgICAgICAgZiJraG9uZyBob2kgZHVvYyBtYXN0ZXIgdHJlbiByZW1vdGUgKGxzLXJlbW90ZSByYz17cmNf',
'bHJ9KToge2VyX2xyWzo2MF19ICIKICAgICAgICBmIuKAlCBraG9uZyBjaHVuZyBtaW5oIGR1b2MgdmUgbmVuIGNvbiB0dW9p',
'IikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgcmNfbG0gb3Igbm90IGxtOgogICAga2V0KCJO',
'Nycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyBkb2MgZHVvYyBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25lOiB7ZXJfbG1b',
'OjYwXX0iKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBsbSAhPSBybToKICAgICMgRGVtIHhl',
'bSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRlbSBkdW9jIOKAlCBjb24gc28gbmF5IG5vaSBybyBtdWMgZG8gc2FpIGxlY2guCiAg',
'ICByY19jLCBzYXUsIF8gPSBnaXQoZ29jLCAicmV2LWxpc3QiLCAiLS1jb3VudCIsIGYie2xtfS4ue3JtfSIpCiAgICB4YSA9',
'IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1pdCIgaWYgKG5vdCByY19jIGFuZCBzYXUuc3RyaXAoKS5pc2RpZ2l0KCkpIGVsc2Ug',
'IiIKICAgIGlubihmIiAgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZSA6IHtsbVs6MTJdfSIpCiAgICBpbm4oZiIgIG1hc3Rl',
'ciB0cmVuIHJlbW90ZSAgICAgICAgOiB7cm1bOjEyXX17eGF9IikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGko',
'Im1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJ2ZSBuZW4gQ1U6',
'IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19ICE9IHJlbW90ZT17cm1bOjEyXX17eGF9ICIKICAgICAgICBmIuKAlCBjaGF5IGBn',
'aXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2luIG1hc3RlcmAgcm9pIGRvIGxhaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEs',
'ICIiLCAiIiwgMQplbHNlOgogICAgaW5uKGYiICB2ZSBuZW4gVFVPSTogb3JpZ2luL21hc3RlciA9IHtsbVs6MTJdfSA9PSBt',
'YXN0ZXIgdHJlbiByZW1vdGUiKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJt',
'KQogICAgcmNfbWIsIG1iLCBlcl9tYiA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIm9yaWdpbi9tYXN0ZXIiLCBoZWFkKQpp',
'ZiByY19tYiBvciBub3QgbWI6CiAgICBpZiBtYiA9PSAiIiBhbmQgcm0gYW5kIGxtID09IHJtOgogICAgICAgIGtldCgiTjcn',
'IGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9jIG1lcmdlLWJhc2Ugdm9pIG9yaWdpbi9tYXN0ZXI6IHtlcl9t',
'Yls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgogICAgZ2hpKCJtZXJnZV9iYXNlIiwgbWIpCiAgICBpbm4oZiIg',
'IG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7bWJbOjEyXX0iKQogICAgaWYgbWIgIT0gU0hBX0JBU0VfU1BF',
'QzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2UgbWEgc3BlYyByMyBraGFpICh7U0hBX0JBU0VfU1BFQ1s6MTJd',
'fSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQogICAgICAgIGlubigiICAgICAgICAgRG8gc28gYmFzZSBjdSBz',
'ZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcgdmFvLiBEdW5nIG1lcmdlLWJhc2UgbW9pIGxhIHZpZWMgY3VhIGV4ZWN1dG9yLiIp',
'CiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJkaWZmIiwgIi0tbnVtc3RhdCIsIFNIQV9CQVNFX1NQRUMsIGhl',
'YWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAgICAgICAgICAgIGggPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBuc194LnNw',
'bGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICAgICAgICAgIGEgPSBzdW0oaW50KHhbMF0pIGZvciB4IGluIGggaWYgeFsw',
'XS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdoaSgibnVtc3RhdF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVwIjogbGVuKGgpLCAi',
'dGhlbSI6IGF9KQogICAgICAgICAgICBpbm4oZiIgICAgICAgICAoZG9pIGNoaWV1OiBzbyBiYXNlIHNwZWMgPSB7bGVuKGgp',
'fSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkgS0hPTkcgZHVuZyBkZSBjaGFtKSIpCiAgICByYywgbnMsIGVyID0gZ2l0KGdv',
'YywgImRpZmYiLCAiLS1udW1zdGF0IiwgbWIsIGhlYWQpCmlmIHJjOgogICAgcGFzcwplbHNlOgogICAgaGFuZyA9IFtsLnNw',
'bGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICB0aGVtID0gc3VtKGludChoWzBd',
'KSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdpdCgpKQogICAgeG9hICA9IHN1bShpbnQoaFsxXSkgZm9yIGggaW4gaGFu',
'ZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgic29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hpKCJkb25nX3RoZW0iLCB0aGVt',
'KTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZvciBoIGluIGhhbmc6IGlubihmIiAgICB7aFsyXTozNH0gK3toWzBdOjw1',
'fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05HOiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17eG9hfSAgICh0cmFu',
'OiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcgdGhlbSkiKQogICAgY2hhbSA9IHNvcnRlZCh7aFsyXSBmb3Ig',
'aCBpbiBoYW5nfSAmIFdSSVRFX1NFVF9HMik7IGdoaSgiY2hhbV93cml0ZV9zZXQiLCBjaGFtKQogICAgZGVmIF9jYV9tb2lf',
'Y28ocmV2KToKICAgICAgICByXywgbmRfLCBfID0gZ2l0KGdvYywgInNob3ciLCBmIntyZXZ9Om9wcy9sZWFzZV9wdWJsaXNo',
'X3Rlc3QucHkiKQogICAgICAgIHJldHVybiBOb25lIGlmIHJfIGVsc2Uge3QgZm9yIHQgaW4gQ0FfTU9JX0cyIGlmIHJlLnNl',
'YXJjaChyIig/bSleZGVmICIgKyB0ICsgciJbYS16XT9fIiwgbmRfKX0KICAgIG9fbWIsIG9faCA9IF9jYV9tb2lfY28obWIp',
'LCBfY2FfbW9pX2NvKGhlYWQpCiAgICBtYW5nID0gc29ydGVkKG9faCAtIG9fbWIsIGtleT1zb19jYSkgaWYgKG9fbWIgaXMg',
'bm90IE5vbmUgYW5kIG9faCBpcyBub3QgTm9uZSkgZWxzZSBOb25lCiAgICBnaGkoImNhX21vaV9nMl9tYW5nX3ZhbyIsIG1h',
'bmcpCiAgICBpZiBub3QgbWFuZzoKICAgICAgICAjIERvIFJPTkcgKGRhIGxhbmQsIGNoaW5oIG1hc3RlciksIG5oYW0gbmhh',
'bmgsIGhheSBuaGFuaCBjdWEgcGFja2V0IEtIQUMgY2hhbSBjdW5nIHRlcDoKICAgICAgICAjIGtob25nIG1hbmcgY2EgbW9p',
'IG5hbyBjdWEgZzIgdGhpIGtob25nIHBoYWkgdW5nIHZpZW4uIERvYyBraG9uZyBkdW9jIChOb25lKSBjdW5nIHZheS4KICAg',
'ICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImRvaSB0dW9uZyBraG9uZyBwaGFpIHVuZyB2aWVuOiB7bGVuKGhh',
'bmcpfSB0ZXAsIGNoYW0ge2NoYW19LCBjYSBtb2kgIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiZzIg',
'bWFuZyB2YW8ge21hbmchcn0g4oCUIGRhIGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPyIpCiAgICBlbHNlOgogICAg',
'ICAgICMgbnVtc3RhdCBpbiBgLWAgKGtob25nIGNvIHNvIGRvbmcpIGNobyB0ZXAgYmluYXJ5Ly1kaWZmIHRoZW8gYXR0cmli',
'dXRlcyDigJQga2UgY2EgYXR0cmlidXRlcyBDVUEgTkdVT0kgRE8gKGRvIHRyZW4KICAgICAgICAjIDIwMjYtMDktMzBnOiBj',
'b3JlLmF0dHJpYnV0ZXNGaWxlIGAqLnB5IC1kaWZmYCA9PiAiMiB0ZXAgLyArMCIgREFUIGNobyAwZWE5NWRlLCB0aGF0ICsz',
'OTcpLiBgLWAgbGEgS0hPTkcgRE8gRFVPQywKICAgICAgICAjIGtob25nIHBoYWkgMDsgVFJVT1QgdGhlbyBzbyB0ZXAgLyBz',
'byBkb25nIERBIGRlbSBkdW9jIHZhbiBnaXUgKHF1YW4gc2F0IHRydWMgdGllcCkuCiAgICAgICAga2hvbmdfc28gPSBbaFsy',
'XSBmb3IgaCBpbiBoYW5nIGlmIG5vdCAoaFswXS5pc2RpZ2l0KCkgYW5kIGhbMV0uaXNkaWdpdCgpKV07IGdoaSgidGVwX2to',
'b25nX3NvX2RvbmciLCBraG9uZ19zbykKICAgICAgICB2dW90ID0gbGVuKGhhbmcpID4gVFJBTl9URVAgb3IgdGhlbSA+IFRS',
'QU5fRE9ORwogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBUUlVPVCBpZiB2dW90IGVsc2UgKEtERCBpZiBraG9uZ19z',
'byBlbHNlIERBVCksCiAgICAgICAgICAgIGYie2xlbihoYW5nKX0gdGVwIC8gK3t0aGVtfSIgKyAoZiIg4oCUIG51bXN0YXQg',
'S0hPTkcgY28gc28gZG9uZyBjaG8ge2tob25nX3NvfSIgaWYga2hvbmdfc28gZWxzZSAiIikpCgojIERpbmggZGFuaCBUSEFU',
'IG5hbSBvIE43JyAoY2EgbW9pIGcyIG1hbmcgdmFvKSwgS0hPTkcgbyAiaGF1IGR1ZSBnMSI6IGcxIGRhIGxhbmQgbmVuIG1v',
'aSBuaGFuaCBkZXUKIyBsYSBoYXUgZHVlLiBEb25nIGRhdSBraG9pIGRhbiBwaGFpIHR1IGtoYWkgdGhlbyBrZXQgcXVhIGF5',
'IChkbyBkdW9jOiBtYXN0ZXIgNDQ2MjBlOCBtbyBraG9pIGJhbmcKIyAiVEhFIEhFIERPIERVT0M6IGcyIiwgSlNPTiAidGhl',
'X2hlIjogImcyIiwgdHJvbmcga2hpIE43JyBkYSBrZXQgbHVhbiAia2hvbmcgcGhhaSB1bmcgdmllbiIpLgojIE5oYW4gY2hp',
'IGR1b2Mgbm9pIERVTkcgY2FpIGRvIGR1b2M6IGBbXWAga2hvbmcgdGFjaCAiZGEgbGFuZCIga2hvaSAibmhhbSBuaGFuaCIv',
'InBhY2tldCBraGFjIiAoZG8KIyBkdW9jIHRyZW4gMjAyNi0wOS0zMGI6IHVuZyB2aWVuIDJhNjc5NjggREEgTEFORCBiaSBn',
'b2kgIktIT05HIHBoYWkgdW5nIHZpZW4gZzIiKS4KaWYgdGhlX2hlID09ICJnMiIgYW5kIG5vdCBzby5nZXQoImNhX21vaV9n',
'Ml9tYW5nX3ZhbyIpOgogICAgdGhlX2hlID0gKCJLSE9ORyBtYW5nIGNhIG1vaSBnMiBuYW8gKGRhIGxhbmQ/IG5oYW0gbmhh',
'bmg/IHBhY2tldCBraGFjPykiIGlmIHNvLmdldCgiY2FfbW9pX2cyX21hbmdfdmFvIikgPT0gW10KICAgICAgICAgICAgICBl',
'bHNlICJnMj8gKENIVUEgZGluaCBkYW5oIGR1b2MgZG9pIHR1b25nKSIpCiAgICBnaGkoInRoZV9oZSIsIHRoZV9oZSkKCiMg',
'Q29uZyBuaGFuaDogZG8gUklFTkcga2ljaCB0aHVvYyAodmFpIGdpYXkpIHJvaSBkdW5nLiBEdW5nIGtoaSBjYW4geGFjIG1p',
'bmggbGFpCiMgdmUgbmVuIG1hIGtob25nIG11b24gdHJhIDIwLTQ1IHBodXQgY2hvIGNhIGJvIHRlc3QuCmlmICItLWNoaS1r',
'aWNoLXRodW9jIiBpbiBzeXMuYXJndjoKICAgIGlubigiIik7IGlubigiPSIgKiA3OCkKICAgIGlubigiLS1jaGkta2ljaC10',
'aHVvYzogQ0hJIGRvIGNvbmcga2ljaCB0aHVvYy4gRGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQogICAg',
'aW5uKCItIiAqIDc4KQogICAgZm9yIF90LCBfdHQsIF9jdCBpbiBjaG90OiBpbm4oZiIgIHtfdHQ6MTR9IHtfdH0iICsgKGYi',
'ICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgIF9rID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtE',
'RCkKICAgIF9yID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQogICAgc3lzLmV4aXQoMyBpZiBf',
'ayBlbHNlICgxIGlmIF9yIGVsc2UgMCkpCgpDSElfUFJPQkUgPSAiLS1jaGktcHJvYmUiIGluIHN5cy5hcmd2ICAgICMgYm8g',
'cXVhIGJvIHRlc3QgKyBONzsgZ2l1IDAsIDEsIDMKIyAtLS0tLS0tLS0tLS0tLS0tIDIuIGJvIHRlc3QgZGF5IGR1IC0tLS0t',
'LS0tLS0tLS0tLS0KaWYgbm90IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMi4gQk8gVEVT',
'VCBEQVkgRFUgKDEwLTQwIHBodXQpIikKICAgIHJjX24sIG91dF9uID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3Qu',
'cHkiXSwgZ29jKQogICAgZ2hpKCJyY19zdWl0ZSIsIHJjX24pCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0X24pCiAgICBp',
'bm4oIiAgcmMgPSIsIHJjX24sICJ8IiwgbS5ncm91cCgwKSBpZiBtIGVsc2UgIihLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcg',
'a2V0KSIpCiAgICBpZiBtOgogICAgICAgIGdoaSgiZGF0IiwgaW50KG0uZ3JvdXAoMSkpKTsgZ2hpKCJ0cmVuIiwgaW50KG0u',
'Z3JvdXAoMikpKTsgZ2hpKCJib19xdWFfc28iLCBpbnQobS5ncm91cCg0KSkpCiAgICBkb19oZXQsIGdjLCB0aW4gPSBkb2Nf',
'ZG8ob3V0X24pCiAgICBnaGkoInNvX2NhX2RvIiwgbGVuKGRvX2hldCkpOyBnaGkoImxpZXRfa2VfZGF5X2R1IiwgdGluKQog',
'ICAgZm9yIGcgaW4gZ2M6IGlubigiICAgKiIsIGcpCiAgICBpbm4oIiIpOyBpbm4oZiIgID09PSB7bGVuKGRvX2hldCl9IENB',
'IERPID09PSIpCiAgICBmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGlubihmIiAgIHt0LnNw',
'bGl0KCdfJylbMF06N30ge3R9Iik7IGlubihmIiAgICAgICAgICAge2RvX2hldFt0XVs6MTUwXX0iKQogICAgZ2hpKCJkb19s',
'eV9kbyIsIHt0OiBkb19oZXRbdF1bOjMwMF0gZm9yIHQgaW4gZG9faGV0fSkKICAgICMgLS0tLSBDSE9UOiBtb2kgY2EgRE8g',
'cGhhaSBHSUFJIFRISUNIIERVT0MgLS0tLQogICAgIyBUaGlldSBjaG90IG5heSwgYm8gZG8gaW4gZGFuaCBzYWNoIGRvIHJv',
'aSB2YW4gdGhvYXQgcmM9MC4gRG8gZHVuZyBsYSBsb2kgZGEgeGF5IHJhOgogICAgIyBsdW90IFdpbmRvd3MgMTktMDkgY28g',
'dDE3MSBETyBtYSBibyBkbyBiYW8gIkRBVCAxMCB8IFRSVU9UIDAiIHZhIHJjPTAuCiAgICBkZWYgX2tob2EodCk6IHJldHVy',
'biB0LnNwbGl0KCJfIilbMF0KICAgIGRvX3BhY2tldCwgZG9fbGEsIGRvX3RoaWV1X2NvbmdfY3UgPSBbXSwgW10sIFtdCiAg',
'ICBmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGssIGx5ID0gX2tob2EodCksIGRvX2hldFt0',
'XQogICAgICAgIGlmIGsgaW4gQ0FfUEFDS0VUOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRvX3BhY2tldC5hcHBl',
'bmQodCkKICAgICAgICBlbGlmICJLSMOUTkcgxJBPIMSQxq/hu6JDIiBpbiBseSBvciAidGhp4bq/dSBgIiBpbiBseTogIGRv',
'X3RoaWV1X2NvbmdfY3UuYXBwZW5kKHQpCiAgICAgICAgZWxpZiBrIGluIE5HT0FJX1BIQU1fVkk6ICAgICAgICAgICAgICAg',
'ICAgICAgICAgcGFzcwogICAgICAgIGVsc2U6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRv',
'X2xhLmFwcGVuZCh0KQogICAgZ2hpKCJkb19wYWNrZXQiLCBkb19wYWNrZXQpOyBnaGkoImRvX2xhIiwgZG9fbGEpOyBnaGko',
'ImRvX3RoaWV1X2NvbmdfY3UiLCBkb190aGlldV9jb25nX2N1KQogICAgaW5uKCIiKQogICAgaW5uKGYiICBjYSBETyB0aHVv',
'YyBDSElOSCBwYWNrZXQgbmF5IDoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdIG9yICdraG9uZyBjbyd9IikKICAg',
'IGlubihmIiAgY2EgRE8gbmdvYWkgcGhhbSB2aSAocjMga2hhaSk6IHtbX2tob2EoeCkgZm9yIHggaW4gc29ydGVkKGRvX2hl',
'dCwga2V5PXNvX2NhKSBpZiBfa2hvYSh4KSBpbiBOR09BSV9QSEFNX1ZJXX0iKQogICAgaW5uKGYiICBjYSBETyB2aSBUSElF',
'VSBDT05HIENVICAgICAgIDoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XSBvciAna2hvbmcgY28nfSIp',
'CiAgICBpbm4oZiIgIGNhIERPIExBIChraG9uZyBnaWFpIHRoaWNoIGR1b2MpOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xh',
'XSBvciAna2hvbmcgY28nfSIpCiAgICAjIC0tLS0gQ0hPVDogcGhlcCBkbyBwaGFpIFRST04gdHJ1b2Mga2hpIG1vdCBjaHUg',
'REFUIG5hbyBkdW9jIHBoYXQgLS0tLQogICAgIyBCYW4gdHJ1b2MgY2hpIElOIGB0aW5gL2ByY19zdWl0ZWA6IGJvIHRlc3Qg',
'Y2hldCBnaXVhIHQxNzEgKHJjPTEzNCwga2hvbmcgZG9uZyB0b25nKQogICAgIyB2YW4gcmEgIkRBVCAxMiB8IFRSVU9UIDAi',
'IHJjPTA7IGNhIFBBQ0tFVCB2YW5nIG1hdCBoYXkgYmkgQk8gUVVBIGN1bmcgZHVvYyBjaGFtIG5odQogICAgIyAia2hvbmcg',
'ZG8iLiBWYW5nIG1hdCBraG9uZyBwaGFpICJraG9uZyBkbyIg4oCUIGxhIEtIT05HIERPIERVT0MuCiAgICB2YW5nID0gW3Qg',
'Zm9yIHQgaW4gc29ydGVkKENBX1BBQ0tFVCwga2V5PXNvX2NhKSBpZiBtYXVfY2Eob3V0X24sIHQpIG5vdCBpbiAoIlFVQSIs',
'ICJETyIpXQogICAgbHlfa2RkID0gW10KICAgIGlmIG5vdCB0aW46IGx5X2tkZC5hcHBlbmQoImRhbmggc2FjaCBkbyBLSE9O',
'RyBkYXkgZHUiKQogICAgaWYgcmNfbiBub3QgaW4gKDAsIDEpIG9yIChyY19uID09IDEpICE9IGJvb2woZG9faGV0KToKICAg',
'ICAgICBseV9rZGQuYXBwZW5kKGYicmMgYm8gdGVzdD17cmNfbn0ga2hvbmcga2hvcCB7bGVuKGRvX2hldCl9IGNhIERPIGRv',
'YyBkdW9jIikKICAgIGlmIHZhbmc6IGx5X2tkZC5hcHBlbmQoZiJjYSBQQUNLRVQgdmFuZy9ibyBxdWE6IHt2YW5nfSIpCiAg',
'ICBnaGkoImNhX3BhY2tldF92YW5nIiwgdmFuZyk7IGdoaSgibHlfZG9fY2h1YV90cm9uIiwgbHlfa2RkKQogICAgaWYgbHlf',
'a2RkOiBrZXQoIkJvIHRlc3QgY2hheSBUUk9OIHZhIGRvYyBEVSIsIEtERCwgIjsgIi5qb2luKGx5X2tkZCkpCiAgICBjaHVh',
'X3Ryb24gPSBLREQgaWYgbHlfa2RkIGVsc2UgREFUCiAgICBrZXQoIktob25nIGNhIG5hbyBjdWEgUEFDS0VUIGJpIERPIiwg',
'Y2h1YV90cm9uIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9fcGFja2V0IGVsc2Ug',
'ZiJETzoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdfSDigJQgYmFuIHZhIENIVUEgeG9uZyIpCiAgICBrZXQoIk1v',
'aSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jIiwgY2h1YV90cm9uIGlmIG5vdCBkb19sYSBlbHNlIFRSVU9ULAogICAgICAg',
'ICIiIGlmIG5vdCBkb19sYSBlbHNlIGYibGE6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdfSIpCiAgICBpZiBkb190aGll',
'dV9jb25nX2N1OgogICAgICAgIGtldCgiQ29uZyBjdSBkYXkgZHUgZGUgZG8iLCBLREQsIGYidGhpZXUgY29uZyBjdSBjaG8g',
'e1tfa2hvYSh4KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XX0iKQoKICAgIGJxID0gc29ydGVkKHt0IGZvciB0LCBfIGlu',
'IFJYX0JPX1FVQS5maW5kYWxsKG91dF9uKX0sIGtleT1zb19jYSk7IGdoaSgiY2FfYm9fcXVhIiwgYnEpCiAgICBpbm4oIiIp',
'OyBpbm4oZiIgIEJPIFFVQSAoe2xlbihicSl9KToge1t4LnNwbGl0KCdfJylbMF0gZm9yIHggaW4gYnFdfSIpCgogICAgaW5u',
'KCIiKTsgaW5uKCIgIE4xLU40ICh0MTY1LXQxNjgpLCB0aWV1IGNoaSBuZ2hpZW0gdGh1IGN1YSByMiwgbmF5IGxhIGNoaSBi',
'YW8gaG9pIHF1eToiKQogICAgYjQgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQU1PSX07IGdoaSgiY2FfbW9p',
'IiwgYjQpCiAgICBmb3IgdCBpbiBDQU1PSTogaW5uKGYiICAgICB7dH06IHtiNFt0XX0iKQogICAgIyBCT19RVUEvdmFuZyBs',
'YSBDSFVBIENIQVksIGtob25nIHBoYWkgRE86IGNoaSBtb3QgY2EgRE8gbW9pIGR1b2MgcGhhdCBUUlVPVC4KICAgIGtldCgi',
'TjEtTjQgKHQxNjUtdDE2OCkiLCBEQVQgaWYgYWxsKHYgPT0gIlFVQSIgZm9yIHYgaW4gYjQudmFsdWVzKCkpCiAgICAgICAg',
'ZWxzZSAoVFJVT1QgaWYgYW55KHYgPT0gIkRPIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkgZWxzZSBLREQpLCBzdHIoYjQpKQoK',
'ICAgIGlubigiIik7IGlubigiICAxNSBjYSB0dW5nIGRvIHRyZW4gQ0k6IikKICAgIGIxNSA9IHt0OiBtYXVfY2Eob3V0X24s',
'IHQpIGZvciB0IGluIENBMTV9OyBnaGkoImNhMTUiLCBiMTUpCiAgICBpbm4oIiAgICAiICsgIiAgIi5qb2luKGYie3R9Onti',
'MTVbdF19IiBmb3IgdCBpbiBDQTE1KSkKCiAgICAjIHQxMzYg4oCUIE4xMiBkbyBHSUFOIFRJRVAgcXVhIGtldCBxdWEgY2EK',
'ICAgIHQxMzZfdGVuID0gbmV4dCgodCBmb3IgdCBpbiBkb19oZXQgaWYgdC5zdGFydHN3aXRoKCJ0MTM2IikpLCBOb25lKQog',
'ICAgaWYgYjE1LmdldCgidDEzNiIpID09ICJRVUEiOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIs',
'IERBVCwgInQxMzYgUVVBIikKICAgIGVsaWYgYjE1LmdldCgidDEzNiIpICE9ICJETyI6CiAgICAgICAga2V0KCJOMTIgdDEz',
'NiAocXVhIGtldCBxdWEgY2EpIiwgS0RELCBmInQxMzYgPSB7YjE1LmdldCgndDEzNicpIXJ9IOKAlCBraG9uZyBjaGF5L2to',
'b25nIHRoYXkiKQogICAgZWxzZToKICAgICAgICBseSA9IGRvX2hldC5nZXQodDEzNl90ZW4sICIiKQogICAgICAgIGtldCgi',
'TjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIFRSVU9ULCBmIkRPOiB7bHlbOjkwXX0iKQoKIyAtLS0tLS0tLS0tLS0tLS0t',
'IDMuIHByb2JlIFRIQU5HIHZhbyBoYW0gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjMu',
'IFBST0JFIFRIQU5HIOKAlCBnb2kgX2dpdF93aW5kb3dzIHZvaSB0aGFtIHNvIHRpZW0iKQpzcGVjID0gaW1wb3J0bGliLnV0',
'aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwNTQxIiwgc3RyKHRlcCkpCmxwID0gaW1wb3J0bGliLnV0aWwubW9kdWxl',
'X2Zyb21fc3BlYyhzcGVjKTsgc3BlYy5sb2FkZXIuZXhlY19tb2R1bGUobHApCnNpZyA9IGluc3BlY3Quc2lnbmF0dXJlKGxw',
'Ll9naXRfd2luZG93cykKZ2hpKCJ0aGFtX3NvX19naXRfd2luZG93cyIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQppbm4oIiAg',
'dGhhbSBzbyBjdWEgX2dpdF93aW5kb3dzOiIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQoKZGVmIGdvaSgqKmt3KToKICAgICIi',
'IkdvaSBfZ2l0X3dpbmRvd3MsIEJBVCBzdGRlcnIgZGUgbW90IGRvbmcgY2hhbiBkb2FuIGtob25nIGdpZXQgbHVvdCBkby4i',
'IiIKICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgogICAgICAg',
'IHIgPSBscC5fZ2l0X3dpbmRvd3MoKiprdykKICAgIHJldHVybiByLCBlLmdldHZhbHVlKCkKCiMgLS0tIGRvaSBjaHVuZyBy',
'aWc6IHBoYWkgdHJhIGxvaSBkdW5nIG1vdCBjYSB0YSBCSUVUIFRSVU9DIGRhcCBhbiAtLS0Kd2l0aCB0ZW1wZmlsZS5UZW1w',
'b3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgbmdvYWkgPSBQYXRoKHQpLyJuZ29haSI7IG5nb2FpLm1rZGlyKCk7IGN3ID0g',
'UGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIChuZ29haS8iZ2l0',
'LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjEsIF8gPSBnb2kocGF0aD1zdHIobmdvYWkp',
'LCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgKGN3LyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIs',
'IGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMiwgXyA9IGdvaShwYXRoPXN0cihjdyksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwg',
'Y3dkPXN0cihjdykpCnJpZ19vayA9IGJvb2wocjEpIGFuZCByMiBpcyBOb25lCmdoaSgicmlnX2RvaV9jaHVuZyIsIHJpZ19v',
'aykKa2V0KCJSSUcgZG9pIGNodW5nIChiaWV0IHRydW9jIGRhcCBhbikiLCBEQVQgaWYgcmlnX29rIGVsc2UgS0RELAogICAg',
'ZiJuZ29haS1jd2QtPnsnTkhBTicgaWYgcjEgZWxzZSAnTm9uZSd9IHwgdHJvbmctY3dkLT57J05IQU4nIGlmIHIyIGVsc2Ug',
'J05vbmUnfSIpCmlmIG5vdCByaWdfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IHJpZyBzYWksIG1vaSBj',
'aG90IGR1b2kgc2Ugdm8gbmdoaWEuIik7IHN5cy5leGl0KDMpCgojIC0tLSBNT0kgQ09ORyBQSEFJIFRVIENIVU5HIE1JTkgg',
'Tk8gQ08gVEhFIERPIC0tLQojIEJhaSBob2MgZGF0IG5oYXQgY3VhIHBhY2tldCBuYXk6IGRvX24xMCBiYW4gY3UgY2hhbSBE',
'QVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxCiMgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0',
'YXQgbWEgTjEwIHNpbmggcmEgZGUgYmF0LiBObyBkZWdlbmVyYXRlIOKAlAojIHRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERB',
'IGxhICc7JyBuZW4gInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gY3VuZyBrZXQgcXVhLgojIE1vdCBjb25nIGtob25n',
'IHRoZSBETyB0aGkga2hvbmcgcGhhaSBjb25nLCB2YSBubyBuZ3V5IGhpZW0gaG9uIGtob25nIGNvIGNvbmc6IG5vCiMgcGhh',
'dCByYSBtb3QgY2h1IERBVC4KIwojIE5lbiB0cnVvYyBraGkgRFVORyBuYW0gY29uZyBuYXkgZGUgcGhhbiBxdXlldCwgYmF0',
'IHR1bmcgY29uZyBnaWV0IG1vdCBkb3QgYmllbiBkYQojIGJpZXQgdHJvbmcuIENvbmcgbmFvIGtob25nIGdpZXQgZHVvYyB0',
'aGkgY2h1IERBVCBjdWEgbm8gYmkgSEEgeHVvbmcgS0hPTkcgRE8gRFVPQzsKIyBUUlVPVCBnaXUgbmd1eWVuIChxdWFuIHNh',
'dCB0cnVjIHRpZXAsIHZkLiBnMSB2YW4gbmhhbiBnaXQuYmF0KS4gRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBj',
'YXkgdGhhdCBraG9uZyBiaQojIGR1bmcgdG9pIChjdW5nIGt5IGx1YXQgbmh1IE43KS4KRE9UX0JJRU5fVFVfS0lFTSA9IFsK',
'ICAgICgiTjgiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICdpZiBjaGlfZGluaCBhbmQgUGF0aChjaGlfZGluaCku',
'bmFtZS5sb3dlcigpID09ICJnaXQuZXhlIiBhbmQgaG9wX2xlKGNoaV9kaW5oKTonLAogICAgICJpZiBjaGlfZGluaCBhbmQg',
'aG9wX2xlKGNoaV9kaW5oKToiKSwKICAgICgiTjkiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJkID0gZF9yYXcu',
'c3RyaXAoKS5zdHJpcCgnXCInKSIsICJkID0gZF9yYXcuc3RyaXAoKSIpLAogICAgKCJOMTAiLCAib3BzL2xlYXNlX3B1Ymxp',
'c2gucHkiLAogICAgICJzZXAgPSBvcy5wYXRoc2VwIGlmIHBoYW5fY2FjaCBpcyBOb25lIGVsc2UgcGhhbl9jYWNoIiwgInNl',
'cCA9IG9zLnBhdGhzZXAiKSwKICAgICgiTjExIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwgImlmIGNoYW5fZG9hbiBpcyBu',
'b3QgTm9uZToiLCAiaWYgRmFsc2U6IiksCiAgICAoIk4xMiIsICJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IiwKICAgICAn',
'Z2l0X3BhdGg9Ii8va2hvbmctY28vZ2l0IicsICdnaXRfcGF0aD0iL2tob25nLWNvL2dpdCInKSwKXQppbm4oIiIpOyBpbm4o',
'IiAgdHUga2llbSBjb25nIOKAlCBtb2kgY29uZyBwaGFpIGdpZXQgZHVvYyBtb3QgZG90IGJpZW4gZGEgYmlldDoiKQpnaWV0',
'ID0ge30KZm9yIG1hLCBkdW9uZywgdGltLCB0aGF5IGluIERPVF9CSUVOX1RVX0tJRU06CiAgICBfdGVuLCBfaGFtID0gbmV4',
'dCgoKGEsIGIpIGZvciBhLCBiIGluIFBST0JFIGlmIGEuc3RhcnRzd2l0aChtYSArICIgIikpLCAoTm9uZSwgTm9uZSkpCiAg',
'ICBpZiBfaGFtIGlzIE5vbmU6CiAgICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERV',
'T0M6IGtob25nIHRpbSB0aGF5IHByb2JlIHRlbiAne21hfSAuLi4nIik7IGNvbnRpbnVlCiAgICB0cnk6CiAgICAgICAgd2l0',
'aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyBfdDoKICAgICAgICAgICAgX2MgPSBQYXRoKF90KS8iY2F5Ijsg',
'c2h1dGlsLmNvcHl0cmVlKGdvYy8ib3BzIiwgX2MvIm9wcyIpCiAgICAgICAgICAgIF9mID0gX2MvZHVvbmc7IF9uZCA9IF9m',
'LnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBpZiBfbmQuY291bnQodGltKSAhPSAxOgogICAgICAg',
'ICAgICAgICAgZ2lldFttYV0gPSBOb25lCiAgICAgICAgICAgICAgICBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6',
'IG1hdSBkb3QgYmllbiBraG9wIHtfbmQuY291bnQodGltKX0gbGFuIChtb25nIDEpIgogICAgICAgICAgICAgICAgICAgIGYi',
'IOKAlCBtYSBuZ3VvbiBkYSBkb2ksIGRvdCBiaWVuIG5heSBoZXQgeSBuZ2hpYSIpOyBjb250aW51ZQogICAgICAgICAgICBf',
'Zi53cml0ZV90ZXh0KF9uZC5yZXBsYWNlKHRpbSwgdGhheSwgMSksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIF9z',
'cCA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF9kYl8iICsgbWEsIHN0cihfYy8ib3BzIi8i',
'bGVhc2VfcHVibGlzaC5weSIpKQogICAgICAgICAgICBfbSA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3Nw',
'KTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbSkKICAgICAgICAgICAgZGVmIF9nb2lfZGIoKiprdyk6CiAgICAgICAgICAg',
'ICAgICBfZSA9IGlvLlN0cmluZ0lPKCkKICAgICAgICAgICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIo',
'X2UpOgogICAgICAgICAgICAgICAgICAgIHJldHVybiBfbS5fZ2l0X3dpbmRvd3MoKiprdyksIF9lLmdldHZhbHVlKCkKICAg',
'ICAgICAgICAgX3R0LCBfY3QsIF8gPSBfaGFtKF9nb2lfZGIsIGluc3BlY3Quc2lnbmF0dXJlKF9tLl9naXRfd2luZG93cyks',
'CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBfYy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAg',
'ICBnaWV0W21hXSA9IChfdHQgPT0gVFJVT1QpCiAgICAgICAgaW5uKGYiICAgIHttYTo0fSBkb3QgYmllbiAtPiB7X3R0OjE0',
'fSB7J0dJRVQgRFVPQycgaWYgX3R0ID09IFRSVU9UIGVsc2UgJ1NPTkcgU09UJ30iCiAgICAgICAgICAgICsgKGYiICAgKHtf',
'Y3R9KSIgaWYgX2N0IGVsc2UgIiIpKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgICAgICBnaWV0W21hXSA9IE5v',
'bmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzoge3R5cGUoX2UpLl9fbmFtZV9ffToge19lfSIpCmdoaSgiY29u',
'Z19naWV0X2R1b2NfZG90X2JpZW4iLCBnaWV0KQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwpIGluIFsodCwgZihnb2ksIHNpZywg',
'dGVwdCkpIGZvciB0LCBmIGluIFBST0JFXToKICAgIGdoaSgicHJvYmVfIiArIHRlbi5zcGxpdCgpWzBdLmxvd2VyKCksIGRs',
'KQogICAgaWYgaXNpbnN0YW5jZShkbCwgZGljdCk6CiAgICAgICAgZm9yIGssIHYgaW4gZGwuaXRlbXMoKTogaW5uKGYiICAg',
'IHtrOjM0fToge3Z9IikKICAgIG1hID0gdGVuLnNwbGl0KClbMF0KICAgIGlmIGdpZXQuZ2V0KG1hKSBpcyBub3QgVHJ1ZSBh',
'bmQgdHQgPT0gREFUOgogICAgICAgICMgREFUIHR1IG1vdCBjb25nIGNodWEgY2h1bmcgbWluaCBkdW9jIGxhIGJpZXQgRE8g',
'dGhpIGtob25nIGRhbmcgdGluIGhvbiBLREQuCiAgICAgICAga2V0KHRlbiwgS0RELCBmImNvbmcgS0hPTkcgZ2lldCBkdW9j',
'IGRvdCBiaWVuIGN1YSBjaGluaCBubyAoe2dpZXQuZ2V0KG1hKSFyfSkiCiAgICAgICAgICAgICAgICAgICAgICBmIiAtPiBj',
'aHUgREFUIG5heSBraG9uZyBjbyBnaWEgdHJpIikKICAgIGVsc2U6CiAgICAgICAga2V0KHRlbiwgdHQsIGN0KQoKIyAtLS0t',
'LS0tLS0tLS0tLS0tIDQuIE43IGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gLS0tLS0tLS0tLS0tLS0tLQppZiBub3QgQ0hJ',
'X1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCI0LiBONyDigJQgZG90IGJpZW4gdHJlbiBCQU4gU0FP',
'IFRBTSAoY2F5IHRoYXQgS0hPTkcgYmkgZHVuZyB0b2kpIikKICAgIHRydW9jID0gdGVwLnJlYWRfdGV4dChlbmNvZGluZz0i',
'dXRmLTgiKS5jb3VudChNQVVfV0lOKQogICAgZ2hpKCJuN190cnVvYyIsIHRydW9jKTsgaW5uKGYiICBzbyBkb25nIGtob3Ag',
'e01BVV9XSU4hcn06IFRSVU9DID0ge3RydW9jfSBbbW9uZyAxXSIpCiAgICBpZiB0cnVvYyAhPSAxOgogICAgICAgIGtldCgi',
'TjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgZiJtYXUgeHVhdCBoaWVuIHt0cnVvY30gbGFuLCBraG9uZyBwaGFp',
'IDEiKQogICAgZWxzZToKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHRtcDoKICAgICAg',
'ICAgICAgc2FvID0gUGF0aCh0bXApLyJjYXkiCiAgICAgICAgICAgIHNodXRpbC5jb3B5dHJlZShnb2MsIHNhbywgaWdub3Jl',
'PXNodXRpbC5pZ25vcmVfcGF0dGVybnMoIi5naXQiLCAiX19weWNhY2hlX18iLCAiKi5weWMiKSkKICAgICAgICAgICAgZjIg',
'PSBzYW8vIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiCiAgICAgICAgICAgIGYyLndyaXRlX3RleHQoZjIucmVhZF90ZXh0KGVu',
'Y29kaW5nPSJ1dGYtOCIpLnJlcGxhY2UoTUFVX1dJTiwgImlmIEZhbHNlOiIpLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAg',
'ICAgICBzYXUgPSBmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTik7IGdoaSgibjdfc2F1Iiwg',
'c2F1KQogICAgICAgICAgICBpbm4oZiIgIFNBVSAoZGEgZG90IGJpZW4pID0ge3NhdX0gW21vbmcgMF0iKQogICAgICAgICAg',
'ICBpZiBzYXUgIT0gMDoKICAgICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgImRv',
'dCBiaWVuIEtIT05HIGFwIGR1b2MiKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmNfbSwgb3V0X20gPSBj',
'aGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBzYW8pCiAgICAgICAgICAgICAgICBtMTY1ID0gbWF1X2NhKG91',
'dF9tLCAidDE2NSIpOyBkbSwgXywgXyA9IGRvY19kbyhvdXRfbSkKICAgICAgICAgICAgICAgIHRlbjE2NSA9IG5leHQoKHQg',
'Zm9yIHQgaW4gZG0gaWYgdC5zdGFydHN3aXRoKCJ0MTY1IikpLCBOb25lKQogICAgICAgICAgICAgICAgbHkgPSAoZG0uZ2V0',
'KHRlbjE2NSkgb3IgIiIpCiAgICAgICAgICAgICAgICBnaGkoIm43X3QxNjUiLCBtMTY1KTsgZ2hpKCJuN19seV9kbyIsIGx5',
'WzoyMDBdKQogICAgICAgICAgICAgICAgaW5uKGYiICB0MTY1IHNhdSBkb3QgYmllbjoge20xNjV9IHwge2x5WzoxMTBdfSIp',
'CiAgICAgICAgICAgICAgICBkdW5nX2x5X2RvID0gIlBBVEggdCIgaW4gbHkgb3IgIi91c3IvYmluIiBpbiBseQogICAgICAg',
'ICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgREFUIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdf',
'bHlfZG8pIGVsc2UKICAgICAgICAgICAgICAgICAgICAoVFJVT1QgaWYgbTE2NSA9PSAiRE8iIGVsc2UgS0REKSwKICAgICAg',
'ICAgICAgICAgICAgICAiZ2lldCBkdW5nIGx5IGRvIiBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKQogICAgICAg',
'ICAgICAgICAgICAgIGVsc2UgKCJETyBuaHVuZyBLSE9ORyBkdW5nIGx5IGRvIC0+IHRpbiBkdW5nIGdpYSIgaWYgbTE2NSA9',
'PSAiRE8iIGVsc2UgImtob25nIGRvYyBkdW9jIHQxNjUiKSkKCiMgLS0tLS0tLS0tLS0tLS0tLSBLRVQgTFVBTiAtLS0tLS0t',
'LS0tLS0tLS0tCmlubigiIik7IGlubigiPSIgKiA3OCkKaW5uKGYiVEhFIEhFIERPIERVT0M6IHt0aGVfaGV9ICAgSEVBRD17',
'aGVhZFs6MTJdfSIpCiMgS2hvaSBkYW4gY2hvIHJldmlld2VyIGJhdCBkYXUgbyBkb25nIHRyZW4sIG5lbiBDSEUgRE8gcGhh',
'aSBuYW0gTkdBWSBkdW9pIG5vOiBraG9uZyBjbyBkb25nIG5heQojIHRoaSBtb3QgbHVvdCAtLWNoaS1wcm9iZSBpbiAiREFU',
'IDcgfCBUUlVPVCAwIHwgS0hPTkcgRE8gRFVPQyAwIiByYz0wIG1hIGtob25nIG5vaSBsYSBjaHVhIGNoYXkgYm8gdGVzdC4K',
'Z2hpKCJjaGVfZG8iLCAiY2hpLXByb2JlIiBpZiBDSElfUFJPQkUgZWxzZSAiZGF5LWR1IikKaWYgQ0hJX1BST0JFOgogICAg',
'aW5uKCItLWNoaS1wcm9iZTogQ0hJIGRvIG11YyAwLCAxLCAzLiBCbyB0ZXN0LCBOMS1ONCwgdDEzNiwgTjcgS0hPTkcgY2hh',
'eSAtIGRheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5naGllbSB0aHUuIikKaWYgdGhlX2hlID09ICJnMSI6CiAgICBpbm4oIkxV',
'VSBZOiBkYXkgbGEgTkVOIERPIChnMSksIEtIT05HIHBoYWkgbmdoaWVtIHRodSBnMi4gQ2FjIGNob3QgTjgtTjEyIGR1b2kg',
'ZGF5IikKICAgIGlubigiICAgICAgIFRSVU9UIGxhIERVTkcgTkhVIE1PTkcg4oCUIGNodW5nIGxhIG5odW5nIGxvIGcyIHNp',
'bmggcmEgZGUgdsOhLiIpCmlubigiLSIgKiA3OCkKZm9yIHRlbiwgdHQsIGN0IGluIGNob3Q6CiAgICBpbm4oZiIgIHt0dDox',
'NH0ge3Rlbn0iICsgKGYiICAge2N0fSIgaWYgY3QgZWxzZSAiIikpCm5fa2RkID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hv',
'dCBpZiB0ID09IEtERCkKbl90cnVvdCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKaW5uKCIt',
'IiAqIDc4KQppbm4oZiIgIERBVCB7c3VtKDEgZm9yIF8sdCxfIGluIGNob3QgaWYgdD09REFUKX0gfCBUUlVPVCB7bl90cnVv',
'dH0gfCBLSE9ORyBETyBEVU9DIHtuX2tkZH0iKQppbm4oZiIgIFRvbmcgY2EgZG86IHtzby5nZXQoJ3NvX2NhX2RvJyl9IHwg',
'ZGFuaCBzYWNoIGRheSBkdTogeydDTycgaWYgc28uZ2V0KCdsaWV0X2tlX2RheV9kdScpIGVsc2UgJ0tIT05HIERPIERVT0Mn',
'fSIpCmlubihmIiAgQWRtaW5pc3RyYXRvcjoge3NvLmdldCgncXV5ZW5fYWRtaW4nKX0gfCBzeW1saW5rOiB7c28uZ2V0KCdz',
'eW1saW5rX2R1b2MnKX0iKQppbm4oIiIpOyBpbm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kgSlNPTiBOQVkgVkUgQ0hPIFJFVklF',
'V0VSIC0tLSIpCmdoaSgiY2hvdCIsIFt7InRlbiI6IGEsICJ0cmFuZ190aGFpIjogYiwgImNoaV90aWV0IjogY30gZm9yIGEs',
'IGIsIGMgaW4gY2hvdF0pCmlubihqc29uLmR1bXBzKHNvLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0xLCBkZWZhdWx0',
'PXN0cikpCiMgcmM6IDAgPSBtb2kgY2hvdCBEQVQgfCAxID0gY28gY2hvdCBUUlVPVCB8IDMgPSBjbyBjaG90IEtIT05HIERP',
'IERVT0MgKHV1IHRpZW4gYmFvIGRvbmcpCnN5cy5leGl0KDMgaWYgbl9rZGQgZWxzZSAoMSBpZiBuX3RydW90IGVsc2UgMCkp',
'Cg=='
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
if ($ChiGiaiNen) { Write-Host ''; Write-Host 'Chi giai nen theo yeu cau. Dung tai day.'; TraMoiTruong; exit 0 }

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
TraMoiTruong
exit $rc
} finally { TraMoiTruong }
