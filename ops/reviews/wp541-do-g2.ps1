# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
# Luot DAY DU can SAN mot python >= 3.9 CO PyYAML >= 5.1 (pip install -U pyyaml): ban nhung python.org ma tep nay tu tai
# KHONG co PyYAML/pip, nen no chi du cho -ChiKichThuoc / -ChiProbe. Thieu thi dung o buoc cong cu, rc=3.
# Luot DAY DU con can `git` >= 2.36, `bash` (Git Bash: o C:\Program Files\Git, hoac Git\bin dau PATH - bash WSL KHONG du;
# git DI KEM Git Bash >= 2.31), `actionlint` >= 1.7.7 (ban ghim CI), `shellcheck` (nhan --norc) tren PATH: tep nay KHONG tu
# cai chung (MinGit chi tai khi THIEU git, va MinGit KHONG co bash); bo do hoi ngay o muc 0 va dung rc=3 neu thieu hoac cu
# hon (khong doi het bo test moi biet).
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
    [string]$Kho     = '',     # clone RIENG de do (phai SACH: tep sua/chua theo doi/danh dau chi muc => rc=3). Mac dinh: <Base>\tl541-do
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
$ShaBoDo    = '1d9741d9f871443a44a3995db36e03d8b3b45a7818b7a3317d49377d6c4f03ec'      # SHA-256 cua bo do Python nhung ben duoi

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
if ($luotDayDu) { $maThu = "import sys;sys.path[:]=[x for x in sys.path if x];print(sys.version.split()[0]);sys.exit(9) if sys.version_info<(3,9) else None;import yaml;yaml.safe_dump(yaml.safe_load('a: 1'),allow_unicode=True,sort_keys=False)" }
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
'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIiIiV1A1NDEgZzIgLSBQSEVQIERPIFRSRU4gV0lORE9XUyBUSEFUIGNobyBzcGVj'
'IHIzIChOMS1ONCArIE44LU4xMiArIE43ICsga2ljaCB0aHVvYykuCgpDaGF5OiAgcHkgd3A1NDEtZG8tZzItd2luZG93cy5w'
'eSAiPHRodS1tdWMta2hvPiIKCktIT05HIGdoaW0gU0hBLiBObyBkbyBCQVQgS1kgZGF1IG5hbyBkYW5nIG8gdHJlbiBuaGFu'
'aCwgcm9pIFRVIFBIQU4gTE9BSToKICBoZWFkID09IDJmNzA4NjlhICAtPiBkYXkgbGEgZzEsIENIVUEgY28gYmFuIHZhIGcy'
'LiBQcm9iZSB2YW4gaW4gKGxhbSBORU4gRE8pIG5odW5nIE43JyByYQogICAgICAgICAgICAgICAgICAgICAgIEtIT05HIERP'
'IERVT0MgKGcxIGRhIGxhbmQsIGRpZmYgcm9uZykgbmVuIHJjPTMuCiAgaGVhZCBsYSBoYXUgZHVlICAgIC0+IENIVUEgZGlu'
'aCBkYW5oOiBjaGkgTjcnIChjYSBtb2kgZzIgbWFuZyB2YW8sIHhlbSBkdW9pKSBtb2kgbm9pIHVuZyB2aWVuIGcyIGhheSBr'
'aG9uZy4KICBraGFjICAgICAgICAgICAgICAgLT4gS0hPTkcgRE8gRFVPQyAocmViYXNlPyBuaGFtIG5oYW5oPykgLT4gcmM9'
'Mywga2hvbmcga2V0IGx1YW4uClR1IDIwLTA5IGcxIERBIExBTkQgdmFvIG1hc3RlciwgbmVuICJoYXUgZHVlIGN1YSBnMSIg'
'S0hPTkcgY29uIGxvYWkgZHVvYyBuaGFuaCBuYW8gKGRvIGR1b2M6Cm1hc3RlciA0NDYyMGU4IHZhIG1vdCBuaGFuaCBib29r'
'a2VlcGluZyBkZXUgcmEgInVuZyB2aWVuIGcyIiwgREFUIHJjPTApLiBWaSB2YXkgZG9pIHR1b25nIGNvbgpwaGFpIChhKSBj'
'byB0aGF5IGRvaSBzbyB2b2kgbWVyZ2UtYmFzZSB2YSAoYykgTUFORyBWQU8gaXQgbmhhdCBtb3QgY2EgTU9JIGN1YSBnMiAo'
'Q0FfTU9JX0cyOgptZXJnZS1iYXNlIGNodWEgY28sIEhFQUQgY28pIOKAlCBraG9uZyB0aGkgS0hPTkcgRE8gRFVPQy4gQ2hp'
'ICIoYikgY2hhbSBXUklURV9TRVRfRzIiIHRoaSBLSE9ORyBkdToKc2F1IGcyIGRhIGNvIDYgcGFja2V0IGtoYWMgY2hhbSBv'
'cHMvbGVhc2VfcHVibGlzaCoucHkgKGRvIGR1b2M6IG5oYW5oICM2MDcgODAzYzI0OCByYSAiVEhFIEhFIERPCkRVT0M6IGcy'
'IiwgTjcnIERBVCAyIHRlcCAvICs1MywgREFUIDEyIHJjPTApLiAoYykga2VvIHRoZW8gKGIpLCBuZW4gKGIpIGNoaSBjb24g'
'ZHVvYyBHSEksIGtob25nIGNoYW0uCgpCQSBUUkFORyBUSEFJIG8gbW9pIGNob3Q6IERBVCAvIFRSVU9UIC8gS0hPTkcgRE8g'
'RFVPQy4gQ2FpIHRodSBiYSBLSE9ORyBkdW9jIGxhbmcgbGUKdGhhbmggbW90IHRyb25nIGhhaSBjYWkga2lhIOKAlCBkbyBs'
'YSBjYSBkb2N0cmluZSBgTm9uZSAhPSBGYWxzZWAgY3VhIGtoby4KCk1PSSBjaG90IGFtIGRldSBjbyBET0kgQ0hVTkcgRFVP'
'TkcuIE1vdCBjaG90IGNoaSBkbyBjaGlldSAicGhhaSB0dSBjaG9pIiB0aGkgbW90IGhhbQpgcmV0dXJuIE5vbmVgIHZvIGRp'
'ZXUga2llbiBjdW5nIHF1YSBkdW9jIG5vLgoKRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9u'
'ZyBiaSBkdW5nIHRvaS4KIiIiCmltcG9ydCBjb250ZXh0bGliLCBoYXNobGliLCBpbXBvcnRsaWIudXRpbCwgaW5zcGVjdCwg'
'aW8sIGpzb24sIG9zLCByZSwgc2h1dGlsLCBzdWJwcm9jZXNzLCBzeXMsIHRlbXBmaWxlCmZyb20gcGF0aGxpYiBpbXBvcnQg'
'UGF0aCwgUHVyZVBvc2l4UGF0aCwgUHVyZVdpbmRvd3NQYXRoCgpvcy5lbnZpcm9uLnNldGRlZmF1bHQoIlBZVEhPTlVURjgi'
'LCAiMSIpCm9zLmVudmlyb24uc2V0ZGVmYXVsdCgiUFlUSE9OSU9FTkNPRElORyIsICJ1dGYtOCIpCiMgQm8gZG8gS0hPTkcg'
'ZHVvYyBkZSAucHljIHRyb25nIGNheSBkdW9jIGRvOiBtdWMgMyBpbXBvcnQgb3BzL2xlYXNlX3B1Ymxpc2gucHkgVFJPTkcg'
'dGllbiB0cmluaCBuYXkgKGdoaSBvcHMvX19weWNhY2hlX18gdmFvIGNheSksIG1hCiMgbXVjIDAgdmEga2V0IGx1YW4gZG9p'
'IGNheSBwaGFpIFNBQ0g7IC5naXRpZ25vcmUgY3VhIHVuZyB2aWVuIGN1IGNvIHRoZSBraG9uZyBsb2FpIF9fcHljYWNoZV9f'
'ICh4ZW0gQ0FZX1NBQ0gpLgpzeXMuZG9udF93cml0ZV9ieXRlY29kZSA9IFRydWUKIyBDT05HX0NVX0dJVCBsYSBiaWVuIERJ'
'RVUgS0hJRU4gY3VhIENISU5IIG1hIGR1b2MgZG86IF9naXRfd2luZG93cyAoYnVvYyAxKSBkb2Mgb3MuZW52aXJvbiBraGkg'
'S0hPTkcgZHVvYyB0cnV5ZW4gY29uZ19jdV9naXQsCiMgbWEgcmlnIGRvaSBjaHVuZyArIHByb2JlIE45LU4xMSAobXVjIDMs'
'IGNoYXkgVFJPTkcgdGllbiB0cmluaCBuYXkpIHZhIGNhYyBjYSBOMS1OMy9OOS1OMTEgY3VhIGJvIHRlc3QgKHF1YSBjaGF5'
'KCksIHZvbiBjaGkgYm8KIyBHSVRfKi9QWVRIT04qKSBkZXUga2hvbmcgdHJ1eWVuLiBDSSBLSE9ORyBkYXQgYmllbiBuYXku'
'IERvIHRyZW4gMjAyNi0wOS0zMGosIDBlYTk1ZGUsIENPTkdfQ1VfR0lUIHRybyBtb3QgZ2l0LmV4ZSBob3AgbGU6IGJvCiMg'
'dGVzdCAxNjAvMTY2LCA2IGNhIFBBQ0tFVCBETyAodDE2NSB0MTY2IHQxNjcgdDE3MCB0MTcxIHQxNzIpID0+ICJLaG9uZyBj'
'YSBuYW8gY3VhIFBBQ0tFVCBiaSBETyIgVFJVT1QgImJhbiB2YSBDSFVBIHhvbmciLCByb2kKIyBSSUcgZG9pIGNodW5nIEtE'
'RCAicmlnIHNhaSIgcmM9MyBzYXUgY2EgYm8gdGVzdCAoY2hpIHJpZyBWTyBUSU5IIGNoYW4gcGhhbiBxdXlldCBzYWkpOyAt'
'LXR1LWtpZW0tcHJvYmU6IE45IFRSVU9ULCBOMTAvTjExIEtERC4KIyBCbyBvIEdPQyDigJQgdGllbiB0cmluaCBuYXkgdmEg'
'bW9pIHRpZW4gdHJpbmggY29uIGN1bmcgdGhheSBuaHUgQ0kg4oCUIHZhIEdISSBMQUkgZ2lhIHRyaSBkZSBtdWMgMCB0dSBr'
'aGFpLgpfQ09OR19DVV9HSVRfTkdVT0lfRE8gPSBvcy5lbnZpcm9uLnBvcCgiQ09OR19DVV9HSVQiLCBOb25lKQpmb3IgX2wg'
'aW4gKHN5cy5zdGRvdXQsIHN5cy5zdGRlcnIpOgogICAgdHJ5OiBfbC5yZWNvbmZpZ3VyZShlbmNvZGluZz0idXRmLTgiLCBl'
'cnJvcnM9InJlcGxhY2UiKQogICAgZXhjZXB0IEV4Y2VwdGlvbjogcGFzcwppZiBzeXMucGxhdGZvcm0gPT0gIndpbjMyIjoK'
'ICAgIHRyeToKICAgICAgICBpbXBvcnQgY3R5cGVzCiAgICAgICAgY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5TZXRDb25zb2xl'
'T3V0cHV0Q1AoNjUwMDEpCiAgICAgICAgY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5TZXRDb25zb2xlQ1AoNjUwMDEpCiAgICBl'
'eGNlcHQgRXhjZXB0aW9uOiBwYXNzCgpkZWYgaW5uKCpwKToKICAgIHZhbiA9ICIgIi5qb2luKHN0cih4KSBmb3IgeCBpbiBw'
'KQogICAgdHJ5OiBwcmludCh2YW4sIGZsdXNoPVRydWUpCiAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgIHRyeTogc3lz'
'LnN0ZG91dC5idWZmZXIud3JpdGUodmFuLmVuY29kZSgidXRmLTgiLCAicmVwbGFjZSIpICsgYiJcbiIpOyBzeXMuc3Rkb3V0'
'LmZsdXNoKCkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uOiBwcmludCh2YW4uZW5jb2RlKCJhc2NpaSIsICJiYWNrc2xhc2hy'
'ZXBsYWNlIikuZGVjb2RlKCJhc2NpaSIpLCBmbHVzaD1UcnVlKQoKIyBOZ29haSBsZSBLSE9ORyBiYXQgPT4gUHl0aG9uIHRo'
'b2F0IHJjPTEsIG1hIHJjPTEgbyBkYXkgREEgQ08gTkdISUEgImNvIGNob3QgVFJVT1QiIChkb25nCiMgY3VvaSB0ZXApIOKA'
'lCBkdW5nIGx5IGRvIHBzMSBkYXQgYHRyYXBgIC0+IHJjPTMuIERvIGR1b2M6IGdpdCB2YW5nIFBBVEggKGRvbmcgYGdpdChn'
'b2MsCiMgInJldi1wYXJzZSIpYCBjaGF5IFRSVU9DIGBpZiBsb2k6YCksIGJvIHRlc3QgcXVhIGhhbiwgdW5nIHZpZW4gdGhp'
'ZXUgX2dpdF93aW5kb3dzLCBwcm9iZQojIHRoYXQgbmVtIG5nb2FpIGxlIOKAlCBjYSBib24gdHVuZyByYSByYz0xIG1hIHBo'
'ZXAgZG8gQ0hVQSBIRSBjaGF5IHhvbmcuCiMgRG9uZyBLRVQgTFVBTiBpbiBUUlVPQyB0cmFjZWJhY2ssIGN1bmcga2VuaCBz'
'dGRvdXQ6IGtob2kgcHMxIGRhbiBjaG8gcmV2aWV3ZXIgYmF0IGRhdSBUVSBkb25nCiMgbmF5LCBuZW4gaW4gdHJhY2ViYWNr'
'IHRydW9jIHRoaSBubyBuYW0gTkdPQUkga2hvaSAoZG8gdHJlbiBwd3NoIDcuNDoga2hvaSAyIGRvbmcsIDAgZG9uZwojIHRy'
'YWNlYmFjaykuIHRyeS9maW5hbGx5OiBob29rIFRVIEhPTkcgKHZkLiBzdGRvdXQgbGEgb25nIGRhIGRvbmcpIHRoaSBQeXRo'
'b24gdHJhIHJjPTEg4oCUIGR1bmcKIyBtYSAiY28gY2hvdCBUUlVPVCIgKGRvIGR1b2M6IEJyb2tlblBpcGUgdHJvbmcgaG9v'
'ayA9PiByYz0xKS4KZGVmIF9uZ29haV9sZV9sYV9LREQoa2lldSwgZ3QsIHZldCk6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0'
'IHRyYWNlYmFjawogICAgICAgIGlubigiIik7IGlubihmIktIT05HIERPIERVT0M6IG5nb2FpIGxlIGtob25nIGx1b25nIHRy'
'dW9jIHtraWV1Ll9fbmFtZV9ffToge2d0fSIpCiAgICAgICAgaW5uKCIiLmpvaW4odHJhY2ViYWNrLmZvcm1hdF9leGNlcHRp'
'b24oa2lldSwgZ3QsIHZldCkpLnJzdHJpcCgpKQogICAgICAgIGlubigiUGhlcCBkbyBDSFVBIGNoYXkgeG9uZy4gS2hvbmcg'
'a2V0IGx1YW4gZ2kuIikKICAgICAgICBmb3IgX2wgaW4gKHN5cy5zdGRvdXQsIHN5cy5zdGRlcnIpOgogICAgICAgICAgICB0'
'cnk6IF9sLmZsdXNoKCkKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjogcGFzcwogICAgZmluYWxseToKICAgICAgICBv'
'cy5fZXhpdCgzKQpzeXMuZXhjZXB0aG9vayA9IF9uZ29haV9sZV9sYV9LREQKClNIQV9HMSAgID0gIjJmNzA4NjlhMDUzNzg0'
'M2U5Y2FlNzg2MThlZTdhZThjMjYxZDk3MmQiCiMgS0hPTkcgZ2hpbSBiYXNlLiBTcGVjIHIzIE42JyBraGFpIGRvIG51bXN0'
'YXQgc28gZDcwNTYyMyDigJQgTkhVTkcgc3BlYyBDVU5HIGJhbyBleGVjdXRvcgojIGBnaXQgbWVyZ2Ugb3JpZ2luL21hc3Rl'
'cmAuIFNhdSBtZXJnZSwgcGhlcCBkbyBzbyBkNzA1NjIzIE5VT1QgY2EgcGhhbiBtYXN0ZXIgbWFuZyB2YW86CiMgZG8gdGhh'
'dCAxOC0wOSB0cmVuIGJhbiB2YSBnMiBjdWEgYWd5IGNobyA1IHRlcCAvICs4MTIsIHRyb25nIGtoaSB2aWVjIGN1YSBhZ3kg'
'bGEgMiB0ZXAgLyArMzUzLgojIE1vdCBjaG90IG5odSB0aGUgc2UgYmFvICJ2dW90IHRyYW4iIGNobyBtb3QgYmFuIHZhIEtI'
'T05HIHZ1b3QuIEJhc2UgZHVuZyBsYSBNRVJHRS1CQVNFLgpTSEFfQkFTRV9TUEVDID0gImQ3MDU2MjMxNjJiNzViNzM0MGVl'
'N2NjYTU0YWMyZDJhYmJkZGJiNmYiCkJBTl9CT19ETyA9ICIyMDI2LTEwLTAxaSIgICAgICAgICAgICAgICMgZG9pIE1PSSBr'
'aGkgc3VhIGJvIGRvIC0gbG9nIHR1IGtoYWkgYmFuIG5hbwpUUkFOX1RFUCwgVFJBTl9ET05HID0gMiwgNDAwICAgICAgICAg'
'ICMgTjcnIGN1YSBzcGVjIHIzCkFMX1NBTiA9ICgxLCA3LCA3KSAgICAgICAgICAgICAgICAgICAgIyBzYW4gYWN0aW9ubGlu'
'dCA9IGJhbiBnaGltIENJOiBBTF9WRVIgY3VhIGNpLnltbCA9IGJhbl9naGltIGN1YSBvcHMvY29uZ19jdS55YW1sCkdJVF9T'
'QU4gPSAoMiwgMzYsIDApICAgICAgICAgICAgICAgICAgIyBzYW4gZ2l0OiB1bmcgdmllbiBnb2kgYGdpdCB3b3JrdHJlZSBs'
'aXN0IC0tcG9yY2VsYWluIC16YCAoY28gYC16YCB0dSAyLjM2KTsgYmFuX2doaW0gZ2l0ID0gbnVsbApHSVRfU0FOX0JBU0gg'
'PSAoMiwgMzEsIDApICAgICAgICAgICAgICMgc2FuIGdpdCBUUk9ORyBiYXNoIGN1YSBibyB0ZXN0OiB0MTUyIGR1bmcgR0lU'
'X0NPTkZJR19DT1VOVCAoY28gdHUgMi4zMSkKTUFVX1dJTiAgPSAnaWYgbmVuX3RodWMgPT0gIndpbmRvd3MiOicKIyBXcml0'
'ZSBzZXQgY3VhIHBhY2tldCAjNTQxIGcyLiBEaWZmIGtob25nIGNoYW0gdGVwIG5hbyBvIGRheSA9PiBkbyBOSEFNIE5IQU5I'
'LgpXUklURV9TRVRfRzIgPSB7Im9wcy9sZWFzZV9wdWJsaXNoLnB5IiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkifQoj'
'ICJUdW9pIiBjaGkgY28gbmdoaWEga2hpIHNvIHZvaSBNQVkgQ0hVIFRIQVQuIE1vdCBtaXJyb3IgY3VjIGJvIGN1IGN1bmcg'
'dHJhIGxzLXJlbW90ZSA9PQojIG9yaWdpbi9tYXN0ZXIgKGRvIGR1b2M6IG1hc3RlciBjMTZiZDMyIC0+ICJ2ZSBuZW4gVFVP'
'SSIsIDQ2IHRlcCAvICs3MTE4IGNobyAwZWE5NWRlKS4KIyBEYW5oIHNhY2ggQ0hPIFBIRVA7IGByZW1vdGUgZ2V0LXVybGAg'
'ZGEga2hhaSB0cmllbiBpbnN0ZWFkT2YgbmVuIGNodXllbiBodW9uZyBjdW5nIGxvIHJhLgpVUkxfS0hPX0hPUF9MRSA9IHsi'
'aHR0cHM6Ly9naXRodWIuY29tL2R1Y3RoYW5naG8vdHJhLWx1YXQiLCAiaHR0cHM6Ly9naXRodWIuY29tL2R1Y3RoYW5naG8v'
'dHJhLWx1YXQuZ2l0IiwKICAgICAgICAgICAgICAgICAgIyBTU0ggdG9pIENVTkcga2hvIChzYXUgX3VybF9zYWNoKTogYHVy'
'bC4iZ2l0QGdpdGh1Yi5jb206Ii5pbnN0ZWFkT2YgImh0dHBzOi8vZ2l0aHViLmNvbS8iYAogICAgICAgICAgICAgICAgICAj'
'IHJhdCBwaG8gYmllbiBvIG1heSBkZXY7IHRoaWV1IGhhaSBkYW5nIG5heSB0aGkga2hvIFRIQVQgYmkgYmFvICJLSE9ORyBw'
'aGFpIGtobyB0aGF0Ii4KICAgICAgICAgICAgICAgICAgInNzaDovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdCIs'
'ICJzc2g6Ly9naXRodWIuY29tL2R1Y3RoYW5naG8vdHJhLWx1YXQuZ2l0IiwKICAgICAgICAgICAgICAgICAgImdpdEBnaXRo'
'dWIuY29tOmR1Y3RoYW5naG8vdHJhLWx1YXQiLCAiZ2l0QGdpdGh1Yi5jb206ZHVjdGhhbmdoby90cmEtbHVhdC5naXQifQoj'
'IGByZW1vdGUgZ2V0LXVybGAgS0hBSSBUUklFTiBpbnN0ZWFkT2YsIG1hIG1hdSBgdXJsLiJodHRwczovLzx0b2tlbj5AZ2l0'
'aHViLmNvbS8iLmluc3RlYWRPZmAgcmF0IHBobwojIGJpZW4uIEluL2doaSBuZ3V5ZW4gdmFuIGxhIGR1YSBUT0tFTiB2YW8g'
'bG9nIHZhIHZhbyBraG9pIEpTT04gcHMxIGJhbyBkYW4gY2hvIHJldmlld2VyIChkbyBkdW9jOgojIDMgZG9uZyB0cm9uZyBr'
'aG9pIGRhbikuIEJvIHVzZXJpbmZvIFRSVU9DIGtoaSBpbiB2YSBUUlVPQyBraGkgc28g4oCUIHRva2VuIHZhbiBsYSBHaXRI'
'dWIgdGhhdC4KIyBBdXRob3JpdHkga2V0IHRodWMgbyBgL2AsIGA/YCBob2FjIGAjYCBEQVUgVElFTiDigJQgZHVuZyBsdWF0'
'IGdpdC9jdXJsLiBCYW4gYFteL10qQGAgbnVvdCBjYSBgP2AvYCNgCiMgbmVuIG1vdCBVUkwgdHJvIHRvaSBNQVkgS0hBQyAo'
'aG9zdCBkdW5nIHRydW9jIGA/YCwgZHVvaSBgP2AgbGEgYEBnaXRodWIuY29tLzxraG8+YCkgZHVvYyAibGFtIHNhY2giCiMg'
'dGhhbmggZHVuZyBtb3QgbXVjIENITyBQSEVQLCB0cm9uZyBraGkgZ2l0IG5vaSB0b2kgbWF5IGtpYSAoZG8gZHVvYzogbWly'
'cm9yIGN1IHBodWMgdnUgcXVhIEhUVFBTID0+CiMgInZlIG5lbiBUVU9JIiwgVFJVT1QgNDYgdGVwIC8gKzcxMTgpLiBWYW4g'
'Ym8gdG9pIGBAYCBDVU9JIHRyb25nIGF1dGhvcml0eTogdXNlcmluZm8gY28gYEBgIHRyYW4gdGhpCiMgY3VybCB0dSBjaG9p'
'ICgiQmFkIGhvc3RuYW1lIiksIGNvbiBraGkgaW4gdGhpIGtob25nIGxvIHBoYW4gc2F1IGBAYCB0aHUgbmhhdC4KX1JYX1VT'
'RVJJTkZPID0gcmUuY29tcGlsZShyIl4oW0EtWmEtel1bQS1aYS16MC05Ky4tXSo6Ly8pW14vPyNdKkAiKQpkZWYgX3VybF9z'
'YWNoKHUpOiByZXR1cm4gX1JYX1VTRVJJTkZPLnN1YihyIlwxIiwgdSBvciAiIikgICAgICAgICAgIyBkZSBTTyAobHVhdCBn'
'aXQvY3VybCkKIyBJTiBwaGFpIGNoZSBST05HIGhvbiBTTzogbWF0IGtoYXUgY28gYD9gL2AjYCBUUkFOIHRoaSBgW14vPyNd'
'KkBgIGtob25nIGtob3AgbmVuIFVSTCByYSBsb2cgTkdVWUVOIFZBTgojIChkbyBkdW9jIHRyZW4gMjAyNi0wOS0zMGI6IDMg'
'ZG9uZyBvIC0tY2hpLWtpY2gtdGh1b2MsIDMgZG9uZyB0cm9uZyBraG9pIGRhbiAtLWNoaS1wcm9iZTsgYmFuIDMwYTogMCku'
'CiMgQ2hlIHRvaSBgQGAgQ1VPSSBDVU5HIGN1YSBDQSBjaHVvaSAoY28gaGF5IGtob25nIGNvIHNjaGVtZSksIHZhIERFIERB'
'VSBgKioqQGAgZGUgYmFuIGluIGtob25nIHR1IG5oYW4gbGEKIyBnaXRodWIuY29tIGtoaSBnaXQgbm9pIHRvaSBtYXkga2hh'
'YyAodmQuIGhvc3QgdHJ1b2MgYD9gKS4gQmFuIDMwYyBjaGUgInRvaSBgQGAgY3VvaSB0cnVvYyBgL2AgZGF1IHRpZW4iCiMg'
'bmVuIFZBTiBsbyBraGkgbWF0IGtoYXUgY28gYC9gIHRyYW4sIGhvYWMgVVJMIGRhbmcgc2NwIGB1c2VyOm1rQGhvc3Q6ZHVv'
'bmdgIChraG9uZyBzY2hlbWUpIOKAlCBkbyB0cmVuCiMgMjAyNi0wOS0zMGM6IDMgZG9uZyAvIDEgdHJvbmcga2hvaSBkYW4g'
'LS1jaGkta2ljaC10aHVvYywgNSAvIDMgbyAtLWNoaS1wcm9iZSwgbW9pIGRhbmcuIE1vaSBreSB0dSBEVU5HCiMgbGEgbW90'
'IGR1b25nIG51YTsgInRvaSBgQGAgY3VvaSIga2hvbmcgY29uIGt5IHR1IGR1bmcgbmFvLiBIYWkgcXV5IHRhYywgaGFpIG11'
'YyBkaWNoOiBTTyB0aGVvIGdpdCwgSU4KIyB0aGVvICJ0aHVhIGNvbiBob24gbG8iLiAiQ0EgY2h1b2kiIHBoYWkgZHVuZyBj'
'YSBraGkgY2h1b2kgY28gWFVPTkcgRE9ORzogZ2l0KCkgZG9jIGJhbmcgdGV4dD1UcnVlIG5lbiBDUi9MRiB0cm9uZyBVUkwK'
'IyBkYSB0aGFuaCBMRiwgbWEgYC5gIGtob25nIGtob3AgTEYuIFRva2VuIGRvYyB0dSB0ZXAgQ1JMRiAoYGh0dHBzOi8veC1h'
'Y2Nlc3MtdG9rZW46PHRva2VuPmAgKyBDUiArIGBAZ2l0aHViLmNvbS8uLi5gKQojIHRoaSBiYW4gMzBlIEtIT05HIGNoZSBn'
'aTogaW4gTkdVWUVOIHRva2VuIG8gZG9uZyBgb3JpZ2luIDpgIHZhIG8gIm9yaWdpbl91cmwiIHRyb25nIGtob2kgSlNPTiBk'
'YW4gKGRvIHRyZW4gMjAyNi0wOS0zMGUpLgpkZWYgX3VybF9pbih1KTogcmV0dXJuIHJlLnN1YihyIl4oW0EtWmEtel1bQS1a'
'YS16MC05Ky4tXSo6Ly8pPy4qQCIsIHIiXDEqKipAIiwgdSBvciAiIiwgZmxhZ3M9cmUuUykKIyBUaG9uZyBiYW8gbG9pIGN1'
'YSBnaXQgQ0hJIGJvIHVzZXJpbmZvIHRvaSBgQGAgREFVIFRJRU46IHVzZXJpbmZvIGNvIGBAYCB0cmFuICh2ZC4gdGVuIGRh'
'bmcgbmhhcCBsYQojIGVtYWlsKSB0aGkgcGhhbiBzYXUgdmFuIHJhIHN0ZGVyciBscy1yZW1vdGUsIG1hIHN0ZGVyciBheSBk'
'dW9jIGluIHZhbyBkb25nIEtERCBjdWEgTjcnIChkbyBkdW9jOgojIDIgZG9uZyB0cm9uZyBsb2csIDEgdHJvbmcga2hvaSBk'
'YW4pLiBMYW0gc2FjaCBNT0kgVVJMIHRyb25nIHZhbiBiYW4gdHJ1b2Mga2hpIGluIOKAlCBjaGUgdG9pIGBAYCBDVU9JIHRy'
'ZW4KIyBET05HIChjdW5nIGx1YXQgSU4gdm9pIF91cmxfaW46IGtob25nIGNvbiBreSB0dSBkdW5nIG5hbykuIEJhbiAzMGQg'
'ZHVuZyBvIGBccyciYCBuZW4gcGhhbiBnaXQgZGUgbGFpIGNvCiMgYCdgL2AiYC9raG9hbmcgdHJhbmcgKHZkLiBgdUB4OnAn'
'PGJpIG1hdD5AZ2l0aHViLmNvbWApIFZBTiBsbyDigJQgZG8gdHJlbiAyMDI2LTA5LTMwZDogMiBkb25nIC8gMSB0cm9uZwoj'
'IGtob2kgZGFuIC0tY2hpLWtpY2gtdGh1b2MsIDMgLyAyIG8gLS1jaGktcHJvYmUsIG1vaSBkYW5nLgpkZWYgX2FuX3VzZXJp'
'bmZvKHQpOiByZXR1cm4gcmUuc3ViKHIiKFtBLVphLXpdW0EtWmEtejAtOSsuLV0qOi8vKVteXG5dKkAiLCByIlwxKioqQCIs'
'IHQgb3IgIiIpCiMgQ2EgbmdvYWkgcGhhbSB2aSByMyDCp25nb2FpX3BoYW1fdmkg4oCUIGRvIENISU5IIFNQRUMga2hhaSwg'
'a2hvbmcgcGhhaSBibyBkbyB0dSBxdXlldC4KIyBEbyBsYSBEQU5IIFNBQ0ggQ0hPIFBIRVA6IGNhIGRvIG5hbyBLSE9ORyBu'
'YW0gdHJvbmcgZGF5IHZhIEtIT05HIHBoYWkgInRoaWV1IGNvbmcgY3UiCiMgdGhpIGxhIFRSVU9ULiBEYW5oIHNhY2ggY2Ft'
'IHRoaSBiYW8gZ2lvIGN1bmcgdGhpZXU7IGRhbmggc2FjaCBjaG8gcGhlcCB0aGkgYmlldCB0cnVvYy4KTkdPQUlfUEhBTV9W'
'SSA9IHNldCgidDEzMSB0MTMyIHQxNTAgdDEyNSB0MzUgdDM2IHQzNyB0MzggdDM5IHQ0MCIuc3BsaXQoKSkKIyBDYSBjdWEg'
'Q0hJTkggcGFja2V0IG5heS4gTW90IGNhIG8gZGF5IG1hIERPIHRoaSBraG9uZyBiYW8gZ2lvIGR1b2MgYm8gcXVhLgpDQV9Q'
'QUNLRVQgPSBzZXQoInQxNjUgdDE2NiB0MTY3IHQxNjggdDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpKQojIENh'
'IE1PSSBtYSBnMiB0aGVtIHZhbyAoTjgtTjEyKS4gRG9pIHR1b25nIGRvIHBoYWkgTUFORyBjaHVuZyB2YW86IG1lcmdlLWJh'
'c2UgY2h1YSBjbywgSEVBRCBjby4KQ0FfTU9JX0cyID0gInQxNjkgdDE3MCB0MTcxIHQxNzIgdDE3MyIuc3BsaXQoKQpDQTE1'
'ICA9ICJ0MTI5IHQxMzAgdDEzMSB0MTMyIHQxMzMgdDEzNiB0MTM4IHQxMzkgdDE0NCB0MTQ1IHQxNDYgdDE0NyB0MTQ5IHQx'
'NTAgdDE1MSIuc3BsaXQoKQpDQU1PSSA9ICJ0MTY1IHQxNjYgdDE2NyB0MTY4Ii5zcGxpdCgpCgpEQVQsIFRSVU9ULCBLREQg'
'PSAiREFUIiwgIlRSVU9UIiwgIktIT05HIERPIERVT0MiCnNvLCBjaG90ID0ge30sIFtdCmRlZiBnaGkoaywgdik6IHNvW2td'
'ID0gdjsgcmV0dXJuIHYKZGVmIGtldCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0PSIiKToKICAgIGNob3QuYXBwZW5kKCh0'
'ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0KSkKICAgIGlubihmIiAgW3t0cmFuZ190aGFpOjE0fV0ge3Rlbn0iICsgKGYiICAg'
'e2NoaV90aWV0fSIgaWYgY2hpX3RpZXQgZWxzZSAiIikpCiAgICByZXR1cm4gdHJhbmdfdGhhaQoKIyAtLS0tLS0tLS0tLS0t'
'LS0tIGRvYyBsb2cgY3VhIGJvIHRlc3QgKGJhbiAzLCBkYSBkbyB0cmVuIGxvZyBUSEFUKSAtLS0tLS0tLS0tLS0tLS0tClJY'
'X0RPX0NITyAgPSByZS5jb21waWxlKHIiKD9tKV4hISEgZG8gKFxTKykgKC4qKSQiKQpSWF9ET19DVU9JID0gcmUuY29tcGls'
'ZShyIig/bSleIHsyfShcU3sxLDR9KSB7Mn0oXFMrKTogKC4qKSQiKQpSWF9CT19RVUEgID0gcmUuY29tcGlsZShyIig/bSle'
'IHsyfVxTezEsNn0gUVVBIChcUyspOiAoLiopJCIpCiMgRG9uZyB0b25nIGtldCBUSEFUIG8gREFVIGRvbmcuIENhIERPIGNv'
'IHRoZSBpbiBsYWkgc3Rkb3V0IGN1YSBtb3QgbHVvdCBDT04gKHQxNTUgY2hheSBsYWkgdDAxLCB0NzIvdDk4IGNoYXkKIyAi'
'Ym8iKSDigJQgZG9uZyB0b25nIExPTkcgYXkgbmFtIEdJVUEgZG9uZyAoZG86IDIwIGRvbmcgbG9uZyBkZXUgbyBnaXVhIGRv'
'bmcsIGNoaSBkb25nIHRvbmcgdGhhdCBvIGRhdSBkb25nKSwgbWEKIyBgc2VhcmNoYCBraG9uZyBuZW8gYmF0IG5vIFRSVU9D'
'LiBEbyB0cmVuIDIwMjYtMDktMzBjLCAwZWE5NWRlICsgZG90IGJpZW4gbGFtIHQwMSBETzogZG9jIHJhICIwLzEiID0+CiMg'
'ImRhbmggc2FjaCBLSE9ORyBkYXkgZHUiLCAiTEVDSCBTTyBIT0M6IHRoaWV1IC0yMCBjYSIsIHRyb25nIGtoaSB0b25nIHRo'
'YXQgMTY2LTE0NT0yMSA9PSAyMSBjYSBkb2MgZHVvYy4KUlhfVE9ORyAgICA9IHJlLmNvbXBpbGUociIoP20pXmxlYXNlX3B1'
'Ymxpc2g6IChcZCspLyhcZCspXGJbXlxuXSo/PShcZCspLFteXG5dKj89KFxkKykiKQoKZGVmIHNvX2NhKHQpOgogICAgbSA9'
'IHJlLm1hdGNoKHIidChcZCspIiwgdCk7IHJldHVybiAoaW50KG0uZ3JvdXAoMSkpIGlmIG0gZWxzZSAxMCoqNiwgdCkKCmRl'
'ZiBkb2NfZG8ob3V0KToKICAgIHRhaV9jaG8gPSB7dDogbC5zdHJpcCgpIGZvciB0LCBsIGluIFJYX0RPX0NITy5maW5kYWxs'
'KG91dCl9CiAgICBibyA9IHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91dCl9CiAgICBjdW9pID0ge3Q6IGwu'
'c3RyaXAoKSBmb3IgXywgdCwgbCBpbiBSWF9ET19DVU9JLmZpbmRhbGwob3V0KSBpZiB0IG5vdCBpbiBib30KICAgIGhvcCA9'
'IGRpY3QoY3VvaSk7IGhvcC51cGRhdGUodGFpX2NobykKICAgIGdjLCB0aW4gPSBbXSwgVHJ1ZQogICAgaWYgc2V0KHRhaV9j'
'aG8pICE9IHNldChjdW9pKToKICAgICAgICBnYy5hcHBlbmQoZiJoYWkgbmd1b24gTEVDSDogY2hpLXRhaS1jaG89e3NvcnRl'
'ZChzZXQodGFpX2Nobyktc2V0KGN1b2kpKX0gY2hpLWN1b2k9e3NvcnRlZChzZXQoY3VvaSktc2V0KHRhaV9jaG8pKX0iKQog'
'ICAgICAgIHRpbiA9IEZhbHNlCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0KQogICAgaWYgbm90IG06CiAgICAgICAgZ2Mu'
'YXBwZW5kKCJLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcga2V0Iik7IHRpbiA9IEZhbHNlCiAgICBlbHNlOgogICAgICAgIGRh'
'dCwgdHJlbiA9IGludChtLmdyb3VwKDEpKSwgaW50KG0uZ3JvdXAoMikpCiAgICAgICAgZ2MuYXBwZW5kKGYic28gaG9jOiB7'
'dHJlbn0te2RhdH09e3RyZW4tZGF0fSBkbzsgZG9jIGR1b2Mge2xlbihob3ApfSIpCiAgICAgICAgaWYgdHJlbiAtIGRhdCAh'
'PSBsZW4oaG9wKToKICAgICAgICAgICAgZ2MuYXBwZW5kKGYiTEVDSCBTTyBIT0M6IHRoaWV1IHt0cmVuLWRhdC1sZW4oaG9w'
'KX0gY2EiKTsgdGluID0gRmFsc2UKICAgIHJldHVybiBob3AsIGdjLCB0aW4KCiMgTWF1IGNvIGRvbmcgdG9uZyBMT05HIGdp'
'dWEgZG9uZyAoZGFuZyB0MTU1IGluIGxhaSBsdW90IGNvbik6IGJvIGRvYyBiYXQgZG9uZyB0b25nIERBVSBUSUVOIGxhIHR1'
'IGtpZW0gRE8uCl9NQVUgPSAoIiEhISBkbyB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOIGEgJ2xlYXNlX3B1Ymxpc2g6'
'IDAvMSDEkeG6oXQ7IMSRw6MgY2jhuqF5PTEsIGLhu48gcXVhPTAnXG4iCiAgICAgICAgIiEhISBkbyB0MTUwX3ggV2luRXJy'
'b3IgMTMxNCByZXF1aXJlZCBwcml2aWxlZ2VcbiIKICAgICAgICAiICBC4buOIFFVQSB0MTMxX3k6IG5lbiBmaXh0dXJlXG4i'
'CiAgICAgICAgIiAgxJDhu44gIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU46IGFcbiIKICAgICAgICAiICDEkOG7jiAg'
'dDE1MF94OiBXaW5FcnJvciAxMzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICJsZWFzZV9wdWJsaXNoOiAxLzMg'
'xJHhuqF0OyDEkcOjIGNo4bqheT0zLCBi4buPIHF1YT0xXG4iKQoKIyBCaWVuIFBZVEhPTiogY3VhIG1heSBuZ3VvaSBkbyBs'
'b3QgdmFvIGJvIHRlc3QgbGEgRE9JIEhBTkggVkkgYm8gdGVzdDogUFlUSE9OT1BUSU1JWkUgYm8gbW9pIGBhc3NlcnRgIChk'
'byB0cmVuCiMgMjAyNi0wOS0zMGM6IGBhc3NlcnQgRmFsc2VgIHF1YSwgcmM9MCk7IGJhbiAzMGQgY2hpIHRydW5nIGhvYSBN'
'T1QgYmllbiBheSwgY29uIFBZVEhPTkRFVk1PREU9MSBsYW0gdDE1NCBETyAyLzQKIyBsYW4gdHJlbiAzLjExIChzYWNoOiA0'
'LzQgUVVBKSA9PiByYz0xICJUUlVPVCBNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIgY2hvIHVuZyB2aWVuIHNhY2gg'
'KGRvIHRyZW4KIyAyMDI2LTA5LTMwZCkuIERhbmggc2FjaCBDQU0gbHVvbiB0aGlldSBtb3QgYmllbiDigJQgbmVuIGRheSBs'
'YSBkYW5oIHNhY2ggQ0hPIFBIRVA6IGNoaSBnaXUgYmllbiBkZSB0cmluaCB0aG9uZwojIGRpY2ggQ0hBWSB2YSB0aW0gZ29p'
'IERBIENBSTsgUFlUSE9OUEFUSCBLSE9ORyBnaXUgKENJIGtob25nIGNvIG5vKS4gUGhlcCBob2kgZGlldSBraWVuIHRpZW4g'
'cXV5ZXQgbyBtdWMgMAojIGN1bmcgY2hheSBxdWEgZGF5LCBuZW4gbm8gdGhheSBEVU5HIG1vaSB0cnVvbmcgbWEgYm8gdGVz'
'dCBzZSB0aGF5LgpfUFlfR0lVID0gZnJvemVuc2V0KHsiUFlUSE9OSE9NRSIsICJQWVRIT05VU0VSQkFTRSIsICJQWVRIT05O'
'T1VTRVJTSVRFIn0pCiMgQ2F1IGhpbmggZ2l0IENVQSBOR1VPSSBETyBsb3QgdmFvIGJvIHRlc3QgeSBuaHUgYmllbiBQWVRI'
'T04qOiBjYSB0ZXN0IGdvaSBnaXQgYmFuZyBkaWN0KG9zLmVudmlyb24pLCBuZW4gZG9jIGNhdSBoaW5oCiMgY2EgbmhhbiB2'
'YSBiaWVuIEdJVF8qIGN1YSBtYXkgZG8uIERvIHRyZW4gMjAyNi0wOS0zMGUsIDBlYTk1ZGU6IGBpbml0LmRlZmF1bHRCcmFu'
'Y2ggPSBtYWluYCA9PiAxNjMvMTY2LCB0MTM0IHQxMzkgdDE1MQojIERPID0+IHJjPTEgIlRSVU9UIE1vaSBjYSBETyBkZXUg'
'Z2lhaSB0aGljaCBkdW9jIiBjaG8gdW5nIHZpZW4gc2FjaCAoc2FjaDogMTY2LzE2Nikg4oCUIG8gcGhhbSB2aSBnbG9iYWwg'
'TEFOIGhlIHRob25nLgojIEJvIE1PSSBiaWVuIEdJVF8qIHZhIHRoYXkgZ2xvYmFsIENBIE5IQU4gYmFuZyBnbG9iYWwgQ1VB'
'IENJLiBDSSBLSE9ORyBjbyBnbG9iYWwgcm9uZzogam9iIGBnYXRlLW9wc2AgY3VhIGNpLnltbCAobm9pIGNoYXkgYm8gdGVz'
'dCwKIyB0YWNoIGtob2kgYGdhdGVgIHR1ICM2NjA7IGJ1b2MgIkZvcmNlIExGIGNoZWNrb3V0IiBnaW9uZyBoZXQgbyBgZ2F0'
'ZWAsIGNhIHVidW50dSBsYW4gd2luZG93cykgZGF0IGdsb2JhbCBjb3JlLmF1dG9jcmxmPWZhbHNlLAojIGNvcmUuZW9sPWxm'
'LCBjb3JlLmFiYnJldj03IFRSVU9DIGJ1b2MgY2hheSBibyB0ZXN0IOKAlAojIHZpIChjaS55bWw6Ny04IHR1IGtoYWkpIGto'
'b25nIHRhdCB0aGkgcnVubmVyIFdpbmRvd3MgY2hlY2tvdXQgQ1JMRjogYXV0b2NybGY9dHJ1ZSBjdWEgYmFuIGNhaSBHaXQg'
'byBIRSBUSE9ORy4gQmFuIDMwZgojIGRhdCBnbG9iYWwgPSByb25nIG5lbiBibyB0ZXN0IHRoYXkgYXV0b2NybGY9dHJ1ZSBj'
'b24gQ0kgdGhheSBmYWxzZTogZG8gdHJlbiAyMDI2LTA5LTMwZiwgMGVhOTVkZSwgaGUgdGhvbmcgYXV0b2NybGY9dHJ1ZQoj'
'ICsgZ2xvYmFsIG5odSBDSSA9PiBiYW4gMzBlIDE2Ni8xNjYsIGJhbiAzMGYgMTY1LzE2NiAodDE1MCBETyDigJQgY2hpIGto'
'b25nIHRoYW5oIFRSVU9UIHZpIHQxNTAgdGluaCBjbyBuYW0gdHJvbmcKIyBOR09BSV9QSEFNX1ZJKS4gR2xvYmFsIGxhIFRF'
'UCBUQU0gY2h1YSBEVU5HCiMgZ2xvYmFsIGN1YSBDSSBjb25nIGluaXQuZGVmYXVsdEJyYW5jaCBnaGltIHZlIG1hYyBkaW5o'
'IGN1YSBnaXQgKGRhdCBkdW9jIGNhIG8gaGUgdGhvbmcpOiBnbG9iYWwgZGUgbGVuIGhlIHRob25nIG5odSB0cmVuIENJLAoj'
'IGNvbiBjYXUgaGluaCBDVUMgQk8gY3VhIGZpeHR1cmUgdmFuIGRlIGxlbiBnbG9iYWwgKEdJVF9DT05GSUdfQ09VTlQgdGhp'
'IGRlIGxlbiBjYSBjdWMgYm8pLiBEb2kgYnVvYyBheSB0cm9uZyBjaS55bWwgdGhpCiMgZG9pIF9HSVRfR0xPQkFMX0NJLiBH'
'SVRfQ09ORklHX0dMT0JBTCBjaGkgdGhheSBURVAgQ09ORklHOiBpZ25vcmUvYXR0cmlidXRlcyBtYWMgZGluaCAoJFhER19D'
'T05GSUdfSE9NRSBob2FjIH4vLmNvbmZpZy9naXQvCiMgaWdub3JlfGF0dHJpYnV0ZXMpIGN1YSBuZ3VvaSBkbyBWQU4gYXAg'
'Y2hvIGdpdCBjb24gKGRvIHRyZW4gMjAyNi0wOS0zMGcsIDBlYTk1ZGU6IH4vLmNvbmZpZy9naXQvaWdub3JlIGAqLnlhbWxg'
'ID0+IGJhbiAzMGcKIyAxNTQvMTY2LCAxMSBjYSAibGEiKTsgQ0kga2hvbmcgY28gdGVwIG5hbyBvIGRvID0+IFhER19DT05G'
'SUdfSE9NRSB0cm8gdmFvIHRodSBtdWMgVEFNIFJPTkcuIENvbiBsYWkgKGtob2EgaGUgdGhvbmcga2hhYykKIyBsYSBnaW9p'
'IGhhbiBkYSBiaWV0LCBraG9uZyBwaGFpIGRhIGRvbmcuCiMgQ2F1IGhpbmggc2hlbGxjaGVjayBDVUEgTkdVT0kgRE8gbG90'
'IHZhbyBibyB0ZXN0IHkgbmh1IGdpdDogdDEzNyBnb2kgc2hlbGxjaGVjayBUSEFORywgdDMzL3QxMzcgZ29pIGFjdGlvbmxp'
'bnQgLT4gc2hlbGxjaGVjaywKIyBjYSBoYWkgZG9jIFNIRUxMQ0hFQ0tfT1BUUywgdmEgdDEzNyBkb2Mgfi8uc2hlbGxjaGVj'
'a3JjIChYREdfQ09ORklHX0hPTUUgdGFtIEtIT05HIGNoZSBkdW9jOyBjaG8gdGVwIHJjIHRyZW4gV2luZG93czogS0hPTkcg'
'RE8gRFVPQykuCiMgRG8gdHJlbiAyMDI2LTA5LTMwaCwgMGVhOTVkZTogU0hFTExDSEVDS19PUFRTPS0tZW5hYmxlPWFsbCA9'
'PiB0MzMgKyB0MTM3IERPOyB+Ly5zaGVsbGNoZWNrcmMgYGVuYWJsZT1hbGxgID0+IHQxMzcgRE8g4oCUIGNhICJsYSIKIyA9'
'PiBUUlVPVCBjaG8gdW5nIHZpZW4gc2FjaC4gQ0kga2hvbmcgY28gY2EgaGFpLiBTSEVMTENIRUNLX09QVFM9LS1ub3JjIGRl'
'IGxlbiBiaWVuIGN1YSBuZ3VvaSBkbyBWQSB0YXQgbW9pIHRlcCByYyAoc2hlbGxjaGVjawojIHBoYWkgTkhBTiAtLW5vcmMg'
'4oCUIG11YyAwIGhvaSB0cnVvYykuCiMgQmllbiBLSE9JIERPTkcgY3VhIGJhc2ggQ1VBIE5HVU9JIERPIGxvdCB2YW8gYm8g'
'dGVzdCB5IG5odSBiYSBuaG9tIHRyZW46IHQzMi90NTEtdDY4IGNoYXkgYmFzaCB2b2kgZGljdChvcy5lbnZpcm9uLCAuLi4p'
'LiBEbwojIHRyZW4gMjAyNi0xMC0wMSAoYmFuIDAxZCksIDBlYTk1ZGU6IFNIRUxMT1BUUz1ub2Nsb2JiZXIsIGhvYWMgQkFT'
'SF9FTlYgY2h1YSBgc2V0IC1vIG5vY2xvYmJlcmAgPT4gdDMyIHQ1MSB0NjAgdDYyIHQ2MyB0NjYgdDY4IERPCiMgImNhbm5v'
'dCBvdmVyd3JpdGUgZXhpc3RpbmcgZmlsZSIg4oCUIGNhICJsYSIgPT4gVFJVT1QgY2hvIHVuZyB2aWVuIHNhY2gg4oCUIHRy'
'b25nIGtoaSBtdWMgMCBjaG8gcXVhOiBubyBob2kgYGdpdCAtLXZlcnNpb25gCiMgdHJvbmcgYmFzaCwgY2F1IEhFUCBob24g'
'Y2F1IGJvIHRlc3QgY2FuLiBCQVNIX0VOViBpbiBieXRlIG5nb2FpIFVURi04ID0+IDE1Mi8xNjYuIENJIGtob25nIGRhdCBi'
'aWVuIG5hbyB0cm9uZyBuaG9tIG5heS4gQm8KIyB0aGVvIFRBUCBiYXNoKDEpIGRvYyBraGkgY2hheSBzY3JpcHQ6IG1vaSB0'
'ZW4gYmF0IGRhdSBgQkFTSGAgKEJBU0hfRU5WIEJBU0hPUFRTIEJBU0hfRlVOQ18qIEJBU0hfWFRSQUNFRkQgQkFTSF9DT01Q'
'QVQgLi4uKSBjb25nCiMgX0JBU0hfS0hPSV9ET05HLiBUcm9uZyBuaG9tIFRFTiwgY2hpIGhhaSBtdWMgdHJlbiBETyBEVU9D'
'IGxhbSBETyAoY3VhIFNTSF9DTElFTlQgdmEgc3RkaW46IHhlbSBkdW9pKTsgY2FjIHRlbiBjb24gbGFpIGJvIHZpIENJCiMg'
'a2hvbmcgZGF0LCBLSE9ORyB2aSBkYSB0aGF5IERPIChkbyAyMDI2LTEwLTAxOiBTSEVMTE9QVFMgeHRyYWNlL25vdW5zZXQv'
'cGlwZWZhaWwvbm9nbG9iL2FsbGV4cG9ydCwgQkFTSE9QVFMgZmFpbGdsb2IvbnVsbGdsb2IvCiMgeHBnX2VjaG8sIFBPU0lY'
'TFlfQ09SUkVDVCwgQ0RQQVRILCBGVU5DTkVTVD0xLCBUTU9VVD0xID0+IDkvOSBjYSBiYXNoKS4gSUZTIGJhc2ggS0hPTkcg'
'bmhhbiB0dSBtb2kgdHJ1b25nLiB0MTUyIHZvbiBjaGkgdHJ1eWVuCiMgUEFUSCBuZW4ga2hvbmcgZG9pLiBNdWMgMCB0dSBr'
'aGFpIFRFTiAoa2hvbmcgaW4gZ2lhIHRyaSkuCiMgVEFQIGF5IGNvbiBtb3QgY3VhIEtIT05HIG1hbmcgdGVuIGJpZW4ga2hv'
'aSBkb25nOiBiYXNoKDEpIElOVk9DQVRJT04g4oCUIHN0ZGluIGxhIFNPQ0tFVCAocnNoZCksIGhvYWMgU1NIX0NMSUVOVC9T'
'U0gyX0NMSUVOVCB0cm9uZwojIG1vaSB0cnVvbmcgKGJhbiBkaWNoIGJhdCBTU0hfU09VUkNFX0JBU0hSQzogR2l0IGZvciBX'
'aW5kb3dzIGJhdCBjYSBubyBsYW4gU1lTX0JBU0hSQyDigJQgMDAwMS1iYXNoLTQuNC1jeWd3aW4ucGF0Y2ggc3VhIGNvbmZp'
'Zy10b3AuaDsKIyBiYXNoIFVidW50dSBjdW5nIGJhdCksIGNvbmcgU0hMVkwgcm9uZy8wID0+IGBiYXNoIC1jYCBuYXAgL2V0'
'Yy9iYXNoLmJhc2hyYyB2YSB+Ly5iYXNocmMgQ1VBIE5HVU9JIERPLCB2YSBCTyBRVUEgQkFTSF9FTlYuIENJIGNoYXkKIyBi'
'byB0ZXN0IHF1YSBgYmFzaCBvcHMvY2hheV9sZWFzZV9wdWJsaXNoX3Rlc3Quc2hgIChqb2IgYGdhdGUtb3BzYCwgYnVvYyBg'
'c2hlbGw6IGJhc2hgKTogd3JhcHBlciBgZXhlY2AgcHl0aG9uIG5lbiBweXRob24gdGhheSBTSExWTD0xCiMgKGV4ZWMgZ2lh'
'bSBTSExWTDsgZG8gMjAyNi0xMC0wOSB0cmVuIGNodW9pIGJ1b2MgLT4gYGJhc2ggd3JhcHBlcmAgLT4gYGV4ZWMgcHl0aG9u'
'YDogMSwgd3JhcHBlciBLSE9ORyBleGVjOiAyKSB2YSBgYmFzaCAtY2AgY3VhIGJvCiMgdGVzdCB0aGF5IDIg4oCUIERVTkcg'
'bmd1b25nIGA8IDJgIChiaWVuIDApOiBidW9jIGNoYXkgYmFuZyBgYmFzaCAtY2AgbW90IGRvbmcgdGhpIHB5dGhvbiB0aGF5'
'IDAgdmEgZHVvbmcgbmF5IE1PLiBOZW4gZHVvbmcgbmF5IFRBVAojIHRyZW4gQ0k7IHB3c2gvY21kIGtob25nIGRhdCBTSExW'
'TCBuZW4gdHJlbiBtYXkgZG8gbm8gTU8uIERvIHRyZW4gMjAyNi0xMC0wMSAoYmFuIDAxZSwgYmFzaCA1LjIuMjEpLAojIDBl'
'YTk1ZGU6IFNTSF9DTElFTlQgKyB+Ly5iYXNocmMgYHNldCAtbyBub2Nsb2JiZXJgID0+IHQzMiB0NTEgdDYwIHQ2MiB0NjMg'
'dDY2IHQ2OCBETywgZTJlIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgICgxNTkvMTY2KTsKIyB+Ly5iYXNocmMgYGNkICIkSE9N'
'RSJgID0+IDggY2EgKHRoZW0gdDU5KTsgc3RkaW4gU09DS0VUICsgbm9jbG9iYmVyID0+IGN1bmcgNyBjYS4gTXVjIDAga2hv'
'bmcgdGhheSAocHJvYmUgZ29pIGAtLW5vcmNgLCBtYSAtLW5vcmMKIyB0YXQgZHVvbmcgbmF5KTogbyBiYW4gMDFlIG5vIHR1'
'IGtoYWkgImJpZW4gYmFzaDogKGtob25nIGNvKSI7IHR1IGJhbiAwMWYgbXVjIDAga2hhaSBURU4gU1NIX0NMSUVOVCBuZXUg'
'Y28sIGNvbiBzdGRpbiBTT0NLRVQgdGhpCiMgS0hPTkcgY28gdGVuIG5hbyBkZSBraGFpIChjaG90OiBERVZOVUxMIHRyb25n'
'IGNoYXkoKSkuIFBoaWVuIFNTSCB2YW8gbWF5IFdpbmRvd3MgZG8gbGEgY3VhIHZhbyAoV2luZG93cyBUSEFUOiBLSE9ORyBE'
'TyBEVU9DKS4gQm8gSEFJCiMgYmllbiBheSAoQ0kga2hvbmcgZGF0KSBWQSBjaG8gbHVvdCBjb24gc3RkaW4gPSBERVZOVUxM'
'IOKAlCBoYWkgY28gY2hlIHJpZW5nLCBoYWkgY2hvdCByaWVuZzsgdDE1MiAoZW52IGNoaSBQQVRIKSB0aHVhIGtlIHN0ZGlu'
'IGF5IG5lbgojIGN1bmcgZG9uZy4KX0JBU0hfS0hPSV9ET05HID0gZnJvemVuc2V0KHsiU0hFTExPUFRTIiwgIkVOViIsICJQ'
'T1NJWExZX0NPUlJFQ1QiLCAiQ0RQQVRIIiwgIkdMT0JJR05PUkUiLCAiR0xPQlNPUlQiLCAiRVhFQ0lHTk9SRSIsCiAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgIkZVTkNORVNUIiwgIlRNT1VUIiwgIlNTSF9DTElFTlQiLCAiU1NIMl9DTElFTlQi'
'fSkKZGVmIF9iaWVuX2Jhc2goayk6IHJldHVybiBrLnVwcGVyKCkuc3RhcnRzd2l0aCgiQkFTSCIpIG9yIGsudXBwZXIoKSBp'
'biBfQkFTSF9LSE9JX0RPTkcKX0dJVF9HTE9CQUxfQ0kgPSAiW2luaXRdXG5cdGRlZmF1bHRCcmFuY2ggPSBtYXN0ZXJcbltj'
'b3JlXVxuXHRhdXRvY3JsZiA9IGZhbHNlXG5cdGVvbCA9IGxmXG5cdGFiYnJldiA9IDdcbiIKZGVmIGNoYXkoYXJndiwgY3dk'
'LCBwaHV0PTYwKToKICAgIGZkLCBnYyA9IHRlbXBmaWxlLm1rc3RlbXAocHJlZml4PSJ3cDU0MS1naXRjb25maWctY2ktIiwg'
'c3VmZml4PSIuaW5pIikKICAgIHhkZyA9IE5vbmUKICAgIHRyeToKICAgICAgICB4ZGcgPSB0ZW1wZmlsZS5ta2R0ZW1wKHBy'
'ZWZpeD0id3A1NDEteGRnLSIpCiAgICAgICAgd2l0aCBvcy5mZG9wZW4oZmQsICJ3IiwgZW5jb2Rpbmc9ImFzY2lpIiwgbmV3'
'bGluZT0iXG4iKSBhcyBmOiBmLndyaXRlKF9HSVRfR0xPQkFMX0NJKQogICAgICAgIG10ID0ge2s6IHYgZm9yIGssIHYgaW4g'
'b3MuZW52aXJvbi5pdGVtcygpCiAgICAgICAgICAgICAgaWYgbm90IGsudXBwZXIoKS5zdGFydHN3aXRoKCJHSVRfIikgYW5k'
'IG5vdCBfYmllbl9iYXNoKGspCiAgICAgICAgICAgICAgYW5kIChub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIlBZVEhPTiIp'
'IG9yIGsudXBwZXIoKSBpbiBfUFlfR0lVKX0KICAgICAgICBtdC51cGRhdGUoUFlUSE9OVVRGOD0iMSIsIFBZVEhPTklPRU5D'
'T0RJTkc9InV0Zi04IiwgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9IjEiLCBQWVRIT05VTkJVRkZFUkVEPSIxIiwKICAgICAg'
'ICAgICAgICAgICAgR0lUX0NPTkZJR19HTE9CQUw9Z2MsIFhER19DT05GSUdfSE9NRT14ZGcsIFNIRUxMQ0hFQ0tfT1BUUz0i'
'LS1ub3JjIikKICAgICAgICBwID0gc3VicHJvY2Vzcy5ydW4oW3N5cy5leGVjdXRhYmxlXSArIGFyZ3YsIGN3ZD1zdHIoY3dk'
'KSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgc3RkaW49c3VicHJvY2Vzcy5ERVZOVUxMLAogICAgICAgICAgICAgICAgICAgICAg'
'ICAgICB0ZXh0PVRydWUsIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCwgZW52'
'PW10KQogICAgZmluYWxseToKICAgICAgICB0cnk6IG9zLnJlbW92ZShnYykKICAgICAgICBleGNlcHQgT1NFcnJvcjogcGFz'
'cwogICAgICAgIGlmIHhkZzogc2h1dGlsLnJtdHJlZSh4ZGcsIGlnbm9yZV9lcnJvcnM9VHJ1ZSkKICAgIHJldHVybiBwLnJl'
'dHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1X2NhKG91dCwgdCk6CiAgICBt'
'ID0gcmUuc2VhcmNoKHIiKD9tKV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSBbMC05Ll0rcyAoXHcrKVxzKiQiLCBv'
'dXQpCiAgICByZXR1cm4gbS5ncm91cCgyKSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdpdChnb2MsICphLCBwaHV0PTUpOgogICAg'
'cCA9IHN1YnByb2Nlc3MucnVuKFsiZ2l0IiwgIi1DIiwgc3RyKGdvYyksICphXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4'
'dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVv'
'dXQ9cGh1dCo2MCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikuc3RyaXAoKSwgKHAuc3RkZXJy'
'IG9yICIiKS5zdHJpcCgpCgoKIyA9PT09PT09PT09PT09PT09PSBOQU0gUFJPQkUsIHZpZXQgdGhhbmggSEFNIFRIVUFOIGRl'
'IFRVIEtJRU0gZHVvYyA9PT09PT09PT09PT09PT09PQojIE1vaSBoYW0gdHJhICh0cmFuZ190aGFpLCBjaGlfdGlldCwgZHVf'
'bGlldSkuIEtIT05HIGluLCBLSE9ORyB0aG9hdCDigJQgbmhvIHZheSBjaHVuZwojIGNoYXkgZHVvYyB0cmVuIG5lbiBCQVQg'
'S1ksIHZhIGAtLXR1LWtpZW0tcHJvYmVgIGdvaSB0aGFuZyBjaHVuZyBkZSBraWVtIGNoaW5oIGJvIGRvLgoKZGVmIF9zYW4o'
'dCk6CiAgICBkID0gUGF0aCh0KS8iZCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9'
'IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgcmV0dXJuIGQsIGN3LCBwZgoKZGVmIGRvX244KGdvaSwgc2lnLCB0ZXB0'
'KToKICAgICIiIkJ1b2MgMSAoQ09OR19DVV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0LmV4ZS4gRG9pIGNodW5nIGR1b25nOiBn'
'aXQuZXhlIFZBTiBwaGFpIG5oYW4uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9y'
'eSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIGZvciB0ZW4gaW4gKCJnaXQuZXhlIiwgImdp'
'dC5iYXQiLCAiZ2l0LmNtZCIsICJnaXQucHkiLCAia2hvbmctcGhhaS1naXQudHh0Iik6CiAgICAgICAgICAgIGYgPSBkL3Rl'
'bjsgZi53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyA9IGdvaShjb25nX2N1X2dp'
'dD1zdHIoZiksIHBhdGg9IiIsIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIGtxW2Yi'
'Q09OR19DVV9HSVQ9e3Rlbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIlRVIENIT0kiCiAgICBsb3QgPSBbayBmb3IgaywgdiBp'
'biBrcS5pdGVtcygpIGlmIHYgPT0gIk5IQU4iIGFuZCBub3Qgay5lbmRzd2l0aCgiZ2l0LmV4ZSIpXQogICAgaWYga3EuZ2V0'
'KCJDT05HX0NVX0dJVD1naXQuZXhlIikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcg'
'aG9uZzogZ2l0LmV4ZSBob3AgbGUgbWEgYmkgdHUgY2hvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgbG90IGVsc2Ug'
'VFJVT1QpLCAoIiIgaWYgbm90IGxvdCBlbHNlIGYiY29uIG5oYW46IHtsb3R9IiksIGtxCgpkZWYgZG9fbjkoZ29pLCBzaWcs'
'IHRlcHQpOgogICAgIiIiTXVjIFBBVEggYm9jIG5oYXkga2VwIHBoYWkgTkhBTjsgbXVjIHJvbmcgLyB0b2FuIGtob2FuZyB0'
'cmFuZyBwaGFpIGJvIHF1YSwga2hvbmcgbmVtLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlE'
'aXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8i'
'Y3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndy'
'aXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGZvciBuaGFuLCBtdWMgaW4gKCgia2hvbmcgbmhheSIs'
'IHN0cihkKSksICgiY28gbmhheSBrZXAiLCBmJyJ7ZH0iJyksCiAgICAgICAgICAgICAgICAgICAgICAgICAgKCJyb25nIiwg'
'IiIpLCAoImNoaSBraG9hbmcgdHJhbmciLCAiICAgIikpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICByLCBf'
'ID0gZ29pKHBhdGg9bXVjLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICAgICAga3Fb'
'ZiJQQVRIIHtuaGFufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBh'
'cyBlOgogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gZiJORU0ge3R5cGUoZSkuX19uYW1lX199IgogICAg'
'aWYga3EuZ2V0KCJQQVRIIGtob25nIG5oYXkiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBk'
'dW9uZyBob25nOiBtdWMgUEFUSCB0aHVvbmcgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgb2sgPSAoa3EuZ2V0'
'KCJQQVRIIGNvIG5oYXkga2VwIikgPT0gIk5IQU4iCiAgICAgICAgICBhbmQga3EuZ2V0KCJQQVRIIHJvbmciKSA9PSAiTm9u'
'ZSIgYW5kIGtxLmdldCgiUEFUSCBjaGkga2hvYW5nIHRyYW5nIikgPT0gIk5vbmUiKQogICAgcmV0dXJuIChEQVQgaWYgb2sg'
'ZWxzZSBUUlVPVCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKIyBEYXUgcGhhbiBjYWNoIGR1bmcgREUgVEhV'
'LiBQaGFpIEtIQUMgb3MucGF0aHNlcCB0cmVuIENBIEhBSSBuZW4gKCc7JyBXaW5kb3dzLCAnOicgUE9TSVgpCiMgdGhpIGhh'
'aSBnaWEgdGh1eWV0ICJ0YWNoIHRoZW8gZGF1IGR1b2MgdHJ1eWVuIiB2YSAidGFjaCB0aGVvIG9zLnBhdGhzZXAiIG1vaSBy'
'b2kgcmEgbmhhdS4KVEhVX04xMCA9ICJ8IgoKZGVmIGRvX24xMChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW0gcGhhaSB0'
'YWNoIFBBVEggdGhlbyBkYXUgcGhhbiBjYWNoIERVT0MgVFJVWUVOLCBraG9uZyB0aGVvIG9zLnBhdGhzZXAgY3VhIG5lbi4K'
'CiAgICBCYW4gY3UgZG8gIm1vdCBkYXUgJzsnIHRyb25nIFRFTiB0aHUgbXVjIiB2YSBkYXQgREFUIHRyZW4gV2luZG93cyBk'
'dSBoYW0gc2FpLiBObwogICAgZGVnZW5lcmF0ZTogdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnLCBuZW4gJ0M6'
'L2E7YicgdGhhdCBzdSBDTyBOR0hJQSBsYSBoYWkKICAgIG11YyDigJQgInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8g'
'cmEgY3VuZyBrZXQgcXVhLCBwaGVwIGRvIGtob25nIHRoZSBkbyBuYW8uIE5vCiAgICBkYSBjaGFtIERBVCBjaG8gOTU4MzE2'
'ODUgdHJvbmcga2hpIHQxNzEgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQgYXkuCiAgICBNb3Qg'
'Y29uZyBraG9uZyB0aGUgZG8gdGhpIGtob25nIHBoYWkgY29uZy4KICAgICIiIgogICAgdGVuX3NlcCA9IG5leHQoKGsgZm9y'
'IGsgaW4gKCJwaGFuX2NhY2giLCAiZGF1X3BoYW5fY2FjaCIsICJzZXAiKSBpZiBrIGluIHNpZy5wYXJhbWV0ZXJzKSwgTm9u'
'ZSkKICAgIGlmIHRlbl9zZXAgaXMgTm9uZToKICAgICAgICAjIEtob25nIGNvIHRoYW0gc28gdGhpIHRyZW4gV2luZG93cyBL'
'SE9ORyBjb24gZHVvbmcgbmFvIHRhY2ggaGFpIGdpYSB0aHV5ZXQuCiAgICAgICAgaWYgb3MucGF0aHNlcCA9PSAiOyI6CiAg'
'ICAgICAgICAgIHJldHVybiAoS0RELCAidHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIHZhIGhhbSBraG9uZyBu'
'aGFuIHRoYW0gc28gZGF1IHBoYW4gY2FjaCAiCiAgICAgICAgICAgICAgICAgICAgICAgICAiLT4ga2hvbmcgdGFjaCBkdW9j'
'IGhhaSBnaWEgdGh1eWV0IiwKICAgICAgICAgICAgICAgICAgICB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBz'
'byBzZXAiOiBOb25lfSkKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAg'
'ICAgIGxhID0gUGF0aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKQogICAgICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAg'
'ICAgICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIs'
'IF8gID0gZ29pKHBhdGg9c3RyKGxhKSArIG9zLnBhdGhzZXAgKyBzdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dk'
'PXN0cihjdykpCiAgICAgICAgICAgIHIwLCBfID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3'
'ZD1zdHIoY3cpKQogICAgICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZSwK'
'ICAgICAgICAgICAgICAiY28gbXVjIGNodWEgJzsnIjogIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIsCiAgICAgICAgICAgICAg'
'ImRvaSBjaHVuZyBkdW9uZyAoa2hvbmcgY28gJzsnKSI6ICJOSEFOIiBpZiByMCBlbHNlICJOb25lIn0KICAgICAgICBpZiBu'
'b3QgcjA6CiAgICAgICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZyIsIGtxCiAgICAgICAgcmV0dXJu'
'IChEQVQgaWYgciBlbHNlIFRSVU9UKSwgKCIiIGlmIHIgZWxzZSAibXVjIGdpdC5leGUgaG9wIGxlIGJpIE1BVCIpLCBrcQoK'
'ICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBsYSA9IFBhdGgodCkvImNvO2Rh'
'dSI7IGxhLm1rZGlyKCkgICAgICAgICAgIyAnOycgbmFtIHRyb25nIFRFTiwga2hvbmcgcGhhaSBkYXUgcGhhbiBjYWNoCiAg'
'ICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5n'
'PSJ1dGYtOCIpCiAgICAgICAgbm9pID0gc3RyKGxhKSArIFRIVV9OMTAgKyBzdHIoZCkKICAgICAgICBrdyA9IGRpY3QocHJv'
'Z3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICByX2NoaW5oLCBfID0gZ29pKHBhdGg9bm9pLCAgICAg'
'ICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyB0YWNoIGR1bmcgIC0+IE5IQU4KICAgICAgICByX2R1b25nLCBf'
'ID0gZ29pKHBhdGg9c3RyKGQpLCAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyBkb2kgY2h1bmcgZHVvbmcK'
'ICAgICAgICByX3BoYW5iaWV0LCBfID0gZ29pKHBhdGg9bm9pLCAgICoqe3Rlbl9zZXA6IG9zLnBhdGhzZXB9LCAqKmt3KSAg'
'IyB0YWNoIHRoZW8gb3MucGF0aHNlcCAtPiBtYXQKICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0g'
'c28gc2VwIjogdGVuX3NlcCwgImRhdSB0aHUiOiBUSFVfTjEwLAogICAgICAgICAgZiJub2kgYmFuZyB7VEhVX04xMCFyfSwg'
'e3Rlbl9zZXB9PXtUSFVfTjEwIXJ9IjogICAgICAgIk5IQU4iIGlmIHJfY2hpbmggZWxzZSAiTm9uZSIsCiAgICAgICAgICBm'
'ImRvaSBjaHVuZyBkdW9uZyAobW90IG11Yywge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9KSI6ICAiTkhBTiIgaWYgcl9kdW9uZyBl'
'bHNlICJOb25lIiwKICAgICAgICAgIGYicGhhbiBiaWV0OiBub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtvcy5w'
'YXRoc2VwIXJ9IjogIk5IQU4iIGlmIHJfcGhhbmJpZXQgZWxzZSAiTm9uZSJ9CiAgICBpZiBub3Qgcl9kdW9uZzoKICAgICAg'
'ICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG1vdCBtdWMgaG9wIGxlIG1hIGtob25nIHRpbSByYSBnaXQu'
'ZXhlIiwga3EKICAgICMgQ29uZyBwaGFpIENPIFRIRSBkby4gTmV1IGNhIGhhaSBkYXUgcGhhbiBjYWNoIGRldSByYSBOSEFO'
'IHRoaSBwaGVwIGRvIGtob25nIHBoYW4KICAgICMgYmlldCBkdW9jIGdpIOKAlCBkdW5nIGJhbyBEQVQsIGJhbyB0aGFuZyBs'
'YSBraG9uZyBkbyBkdW9jLgogICAgaWYgcl9waGFuYmlldDoKICAgICAgICByZXR1cm4gKEtERCwgZiJwaGVwIGRvIEtIT05H'
'IHBoYW4gYmlldCBkdW9jOiBub2kgYmFuZyB7VEhVX04xMCFyfSBtYSB0YWNoIHRoZW8gIgogICAgICAgICAgICAgICAgICAg'
'ICBmIntvcy5wYXRoc2VwIXJ9IFZBTiB0aW0gcmEgZ2l0LmV4ZSIsIGtxKQogICAgcmV0dXJuICgoREFULCAiIiwga3EpIGlm'
'IHJfY2hpbmggZWxzZQogICAgICAgICAgICAoVFJVT1QsIGYidGFjaCB0aGVvIG9zLnBhdGhzZXAgdGhheSB2aSB0aGVvIHt0'
'ZW5fc2VwfSBkdW9jIHRydXllbiIsIGtxKSkKCgpkZWYgZG9fbjExKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIlRydXllbiBj'
'aGFuX2RvYW4gPT4gdGh1IGR1b2MgdGhvbmcgYmFvIFZBIHN0ZGVyciBJTS4gS2hvbmcgdHJ1eWVuID0+IHN0ZGVyciBWQU4g'
'Y28uIiIiCiAgICBpZiAiY2hhbl9kb2FuIiBub3QgaW4gc2lnLnBhcmFtZXRlcnM6CiAgICAgICAgcmV0dXJuIEtERCwgIl9n'
'aXRfd2luZG93cyBraG9uZyBuaGFuIHRoYW0gc28gY2hhbl9kb2FuIiwgeyJ0aGFtIHNvIjogbGlzdChzaWcucGFyYW1ldGVy'
'cyl9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nh'
'bih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgY2Qg'
'PSBbXQogICAgICAgIF8sIGVfY28gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihj'
'dyksIGNoYW5fZG9hbj1jZCkKICAgICAgICBfLCBlX2toID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihw'
'ZiksIGN3ZD1zdHIoY3cpKQogICAga3EgPSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAobXVjKSI6IGxlbihjZCksCiAgICAgICAg'
'ICAic3RkZXJyIGtoaSBDTyBjaGFuX2RvYW4gKGJ5dGUpIjogbGVuKGVfY28uZW5jb2RlKCkpLAogICAgICAgICAgInN0ZGVy'
'ciBraGkgS0hPTkcgdHJ1eWVuIChieXRlKSI6IGxlbihlX2toLmVuY29kZSgpKX0KICAgIGlmIGxlbihjZCkgPT0gMCBhbmQg'
'bGVuKGVfa2guZW5jb2RlKCkpID09IDA6CiAgICAgICAgcmV0dXJuIEtERCwgIm5oYW5oICVQcm9ncmFtRmlsZXMlIGtob25n'
'IHBoYW4gZ2lhaSBLSE9ORyBiYXkgcmEgY2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRvIGR1b2MiLCBrcQogICAgb2sgPSBsZW4o'
'Y2QpID4gMCBhbmQgbGVuKGVfY28uZW5jb2RlKCkpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA+IDAKICAgIHJldHVy'
'biAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCmRlZiBkb19uMTIoZ29p'
'LCBzaWcsIHRlcHQpOgogICAgIiIiSGFuZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9uZyBmaXh0dXJlIHBoYWkgdHV5ZXQgZG9p'
'IHRyZW4gQ0EgSEFJIG5lbi4iIiIKICAgIG5kID0gdGVwdC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJy'
'ZXBsYWNlIikKICAgIGhhbmcgPSBzb3J0ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRfcGF0aFxzKj1ccyoiKFteIl0rKSInLCBu'
'ZCkpKQogICAgeGF1ID0gW2ggZm9yIGggaW4gaGFuZyBpZiBub3QgKFB1cmVQb3NpeFBhdGgoaCkuaXNfYWJzb2x1dGUoKSBh'
'bmQgUHVyZVdpbmRvd3NQYXRoKGgpLmlzX2Fic29sdXRlKCkpXQogICAga3EgPSB7ImhhbmcgZ2l0X3BhdGggdGltIHRoYXki'
'OiBoYW5nLCAiY2hpIHR1eWV0IGRvaSBNT1QgbmVuIjogeGF1fQogICAgaWYgbm90IGhhbmc6CiAgICAgICAgcmV0dXJuIEtE'
'RCwgImtob25nIHRpbSB0aGF5IGhhbmcgZ2l0X3BhdGggbmFvIHRyb25nIGZpeHR1cmUgLT4gbWF1IGRvYyBjbyB0aGUgZGEg'
'ZG9pIiwga3EKICAgIHJldHVybiAoREFUIGlmIG5vdCB4YXUgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgeGF1IGVsc2UgZiJj'
'aGktbW90LW5lbjoge3hhdX0iKSwga3EKClBST0JFID0gWygiTjggYnVvYyAxIGNoaSBuaGFuIGdpdC5leGUiLCBkb19uOCks'
'CiAgICAgICAgICgiTjkgYm9jIG5oYXkga2VwIG8gbXVjIFBBVEgiLCBkb19uOSksCiAgICAgICAgICgiTjEwIGRhdSAnOycg'
'dHJvbmcgdGVuIHRodSBtdWMiLCBkb19uMTApLAogICAgICAgICAoIk4xMSBjaGFuIGRvYW4gZG9pIGtlbmgiLCBkb19uMTEp'
'LAogICAgICAgICAoIk4xMiBoYW5nIHNlbnRpbmVsIHR1eWV0IGRvaSBDQSBIQUkgbmVuIiwgZG9fbjEyKV0KCiMgLS0tIGNo'
'ZSBkbyBUVSBLSUVNOiBjaGF5IG5hbSBwcm9iZSB0cmVuIG1vdCBjYXkgYmF0IGt5LCBuZW4gYmF0IGt5IC0tLQppZiAiLS10'
'dS1raWVtLXByb2JlIiBpbiBzeXMuYXJndjoKICAgIF9nID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS10dS1r'
'aWVtLXByb2JlIikgKyAxXSkucmVzb2x2ZSgpCiAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2Nh'
'dGlvbigibHBfdGsiLCBzdHIoX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgIF9scCA9IGltcG9ydGxpYi51dGls'
'Lm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbHApCiAgICBfc2lnID0gaW5zcGVjdC5z'
'aWduYXR1cmUoX2xwLl9naXRfd2luZG93cykKICAgIGRlZiBfZ29pKCoqa3cpOgogICAgICAgIGUgPSBpby5TdHJpbmdJTygp'
'CiAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICAgICAgcmV0dXJuIF9scC5fZ2l0'
'X3dpbmRvd3MoKiprdyksIGUuZ2V0dmFsdWUoKQogICAgcHJpbnQoZiJUVSBLSUVNIFBST0JFIHRyZW4ge19nfSAgKG5lbiB7'
'c3lzLnBsYXRmb3JtfSkiKQogICAgZm9yIF90ZW4sIF9mIGluIFBST0JFOgogICAgICAgIF90dCwgX2N0LCBfZGwgPSBfZihf'
'Z29pLCBfc2lnLCBfZy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBwcmludChmIiAgW3tfdHQ6MTR9'
'XSB7X3Rlbn0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgICAgICBmb3IgX2ssIF92IGluIChfZGwgb3Ig'
'e30pLml0ZW1zKCk6IHByaW50KGYiICAgICAgICB7X2s6MzR9OiB7X3Z9IikKICAgIHN5cy5leGl0KDApCgojIC0tLSBjaGUg'
'ZG8gS0lFTSBET05HIEJPOiB0ZXAgLnB5IG5heSBwaGFpIFRSVU5HIFRVTkcgQllURSB2b2kgYmFuIG5odW5nIHRyb25nIHBz'
'MSAtLS0KIyBLaG9uZyBjb25nIG5hbyBidW9jIGhhaSBiYW4gc2FvIGtob3A6IGRvIGR1b2MsIG5vaSB0cmFuIDIvNDAwIC0+'
'IDk5Lzk5OTk5IENISSB0cm9uZyAucHkKIyB0aGkgY2lfZGFuZ19reSBsYW4gdDI2L3QyNyB2YW4geGFuaCwgY29uIGNob3Qg'
'U0hBIGN1YSBwczEgY2hpIHNvIGJhbiBuaHVuZyB2b2kgaGFuZyBzbwojIGN1YSBDSElOSCBuby4gQ2hheTogcHl0aG9uIHdw'
'NTQxLWRvLWcyLXdpbmRvd3MucHkgLS1raWVtLWRvbmctYm8gd3A1NDEtZG8tZzIucHMxICAocmMgMHwzKQppZiAiLS1raWVt'
'LWRvbmctYm8iIGluIHN5cy5hcmd2OgogICAgaW1wb3J0IGJhc2U2NAogICAgX3BzID0gUGF0aChzeXMuYXJndltzeXMuYXJn'
'di5pbmRleCgiLS1raWVtLWRvbmctYm8iKSArIDFdKS5yZWFkX3RleHQoZW5jb2Rpbmc9ImFzY2lpIikKICAgIF9tID0gcmUu'
'c2VhcmNoKHIiKD9tcyleXCRCNjQgPSBAXCgoLio/KV5cKSIsIF9wcykKICAgIF9rID0gcmUuc2VhcmNoKHIiKD9tKV5cJFNo'
'YUJvRG9ccyo9XHMqJyhbMC05YS1mXXs2NH0pJyIsIF9wcykKICAgIF9uaHVuZyA9IGJhc2U2NC5iNjRkZWNvZGUoIiIuam9p'
'bihyZS5maW5kYWxsKHIiJyhbQS1aYS16MC05Ky89XSopJyIsIF9tLmdyb3VwKDEpKSkpIGlmIF9tIGVsc2UgYiIiCiAgICBf'
'dG9pID0gUGF0aChfX2ZpbGVfXykucmVhZF9ieXRlcygpCiAgICBfb2sgPSBib29sKF9tIGFuZCBfaykgYW5kIF9uaHVuZyA9'
'PSBfdG9pIGFuZCBoYXNobGliLnNoYTI1NihfdG9pKS5oZXhkaWdlc3QoKSA9PSBfay5ncm91cCgxKQogICAgaW5uKGYiS0lF'
'TSBET05HIEJPOiB7REFUIGlmIF9vayBlbHNlIEtERH0gIChuaHVuZyB7bGVuKF9uaHVuZyl9IGJ5dGUsIHRlcCB7bGVuKF90'
'b2kpfSBieXRlKSIpCiAgICBzeXMuZXhpdCgwIGlmIF9vayBlbHNlIDMpCgppbm4oIj0iICogNzgpOyBpbm4oIldQNTQxIGcy'
'IC0gcGhlcCBkbyB0cmVuIFdpbmRvd3MgdGhhdCAoc3BlYyByMzogTjEtTjQsIE44LU4xMiwgTjcsIGtpY2ggdGh1b2MpIik7'
'IGlubigiPSIgKiA3OCkKCiMgLS0tLS0tLS0tLS0tLS0tLSB0dSBraWVtIGJvIGRvYyAtLS0tLS0tLS0tLS0tLS0tCl9kLCBf'
'ZywgX3QgPSBkb2NfZG8oX01BVSkKX29rID0gKGxlbihfZCkgPT0gMiBhbmQgYW55KHguc3RhcnRzd2l0aCgidDAyYiIpIGZv'
'ciB4IGluIF9kKQogICAgICAgYW5kIG5vdCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMxIikgZm9yIHggaW4gX2QpIGFuZCBfdCkK'
'aW5uKCJUdSBraWVtIGJvIGRvYyBsb2c6IiwgREFUIGlmIF9vayBlbHNlIFRSVU9UKQppZiBub3QgX29rOgogICAgaW5uKCIi'
'KTsgaW5uKCJLSE9ORyBETyBEVU9DOiBibyBkb2MgbG9nIGN1YSBjaGluaCBzY3JpcHQgbmF5IHNhaSAtPiBraG9uZyBkbyBn'
'aSBjYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4gZG8gLS0tLS0tLS0tLS0tLS0tLQpnb2Mg'
'PSBQYXRoKHN5cy5hcmd2WzFdKS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQYXRoLmN3ZCgpCnRlcCwg'
'dGVwdCA9IGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoX3Rl'
'c3QucHkiCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMC4gTkVOIERPIikKIyBNT0kgTE9HIFBIQUkgVFUgS0hBSSBu'
'byBkbyBDQUkgR0kgYmFuZyBCTyBETyBOQU8uIEJhaSBob2MgMTktMDktMjAyNjogbW90IGx1b3QgZG8KIyBndWkgdmUgZHVv'
'YyBkb2Mgbmh1IGtldCBxdWEgY3VhIGJhbiB2YSBkYW5nIHhldCwgbmh1bmcgdGhhdCByYSBsYSBiYW4gZG8gQ1UgY2hheQoj'
'IHRyZW4gbmhhbmggS0hBQy4gRG9jIHJhIHRoaSBtYXQgbW90IHZvbmc7IGxvZyB0dSBraGFpIHRoaSB0aGF5IG5nYXkgZG9u'
'ZyBkYXUuCnRyeToKICAgIF90dSA9IGhhc2hsaWIuc2hhMjU2KFBhdGgoX19maWxlX18pLnJlYWRfYnl0ZXMoKSkuaGV4ZGln'
'ZXN0KCkKZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgIF90dSA9IGYia2hvbmcgdHUgYmFtIGR1b2M6IHtfZX0iCmdoaSgi'
'Ym9fZG9fc2hhMjU2IiwgX3R1KQppbm4oZiIgIEJPIERPICAgICAgICA6IHNoYTI1NiB7X3R1WzoxNl19ICAoYmFuIHtCQU5f'
'Qk9fRE99KSIpCmlubigiICBzeXMucGxhdGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwgInwgcHl0aG9uIiwgc3lzLnZlcnNpb24u'
'c3BsaXQoKVswXSkKaW5uKCIgIG9zLnBhdGhzZXAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSwgInwgUEFUSEVYVDoiLCByZXBy'
'KG9zLmVudmlyb24uZ2V0KCJQQVRIRVhUIikpWzo2MF0pCmlubigiICBQcm9ncmFtRmlsZXMgOiIsIHJlcHIob3MuZW52aXJv'
'bi5nZXQoIlByb2dyYW1GaWxlcyIpKSwgInwgU3lzdGVtUm9vdDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290'
'IikpKQppbm4oIiAgQ09OR19DVV9HSVQgIDoiLCByZXByKF9DT05HX0NVX0dJVF9OR1VPSV9ETykKICAgICsgKCIgIC0+IERB'
'IEJPIGtob2kgbHVvdCBkbyAoQ0kga2hvbmcgZGF0IGJpZW4gbmF5OyB4ZW0gZGF1IHRlcCkiIGlmIF9DT05HX0NVX0dJVF9O'
'R1VPSV9ETyBpcyBub3QgTm9uZSBlbHNlICIiKSkKZ2hpKCJjb25nX2N1X2dpdF9uZ3VvaV9kbyIsIF9DT05HX0NVX0dJVF9O'
'R1VPSV9ETykKX2Jhc2hfYm8gPSBnaGkoImJpZW5fYmFzaF9uZ3VvaV9kb19kYV9ibyIsIHNvcnRlZChrIGZvciBrIGluIG9z'
'LmVudmlyb24gaWYgX2JpZW5fYmFzaChrKSkpCmlubigiICBiaWVuIGJhc2ggICAgOiIsICgiLCAiLmpvaW4oX2Jhc2hfYm8p'
'ICsgIiAgLT4gREEgQk8ga2hvaSBsdW90IGNvbiAoQ0kga2hvbmcgZGF0OyB4ZW0gY2hheSgpKSIpIGlmIF9iYXNoX2JvIGVs'
'c2UgIihraG9uZyBjbykiKQppbm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5vbmUKaWYgc3lzLnBsYXRm'
'b3JtID09ICJ3aW4zMiI6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4gPSBib29sKGN0eXBlcy53aW5k'
'bGwuc2hlbGwzMi5Jc1VzZXJBbkFkbWluKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXllbiA9IE5vbmUKZ2hpKCJxdXll'
'bl9hZG1pbiIsIHF1eWVuKQpzeW1saW5rX2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGly'
'ZWN0b3J5KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0i'
'dXRmLTgiKQogICAgICAgIHRyeTogb3Muc3ltbGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJsayIpKTsgc3ltbGlua19kdW9j'
'ID0gVHJ1ZQogICAgICAgIGV4Y2VwdCBPU0Vycm9yIGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZhbHNlOyBnaGkoInN5bWxpbmtf'
'bG9pIiwgZiJ7dHlwZShlKS5fX25hbWVfX306IHtlfSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZTogZ2hpKCJzeW1saW5rX2xv'
'aSIsIHN0cihlKSkKZ2hpKCJzeW1saW5rX2R1b2MiLCBzeW1saW5rX2R1b2MpCmlubigiICBBZG1pbmlzdHJhdG9yOiIsIHF1'
'eWVuLCAifCB0YW8gc3ltbGluayBkdW9jOiIsIHN5bWxpbmtfZHVvYykKCmxvaSA9IFtdCiMgQ29uZyBraWNoIHRodW9jIGxh'
'IHBoZXAgZG8gdHJlbiBMSUNIIFNVIEdJVCwga2hvbmcgZGluaCBnaSBkZW4gbmVuLiBDaG8gcGhlcAojIC0tY2hpLWtpY2gt'
'dGh1b2MgY2hheSBvIG1vaSBuZW4gZGUgY29uIFRVIEtJRU0gZHVvYyBjaGluaCBjb25nIG5heSAoZGEgZHVuZwojIGRlIHRh'
'aSBkdW5nIGNhIGhhaSB2ZSBjdWEgc3UgY28gbmVuLWN1IDE5LTA5KS4gTW9pIGNob3QgQ0hVQyBOQU5HIHZhbiBkb2kgV2lu'
'ZG93cy4KaWYgc3lzLnBsYXRmb3JtICE9ICJ3aW4zMiIgYW5kICItLWNoaS1raWNoLXRodW9jIiBub3QgaW4gc3lzLmFyZ3Y6'
'CiAgICBsb2kuYXBwZW5kKGYiS0hPTkcgcGhhaSBXaW5kb3dzIChzeXMucGxhdGZvcm09e3N5cy5wbGF0Zm9ybSFyfSkiKQpp'
'ZiBub3QgdGVwLmlzX2ZpbGUoKTogIGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB9IikKaWYgbm90IHRlcHQuaXNfZmls'
'ZSgpOiBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwdH0iKQppZiBub3Qgc2h1dGlsLndoaWNoKCJnaXQiKTogbG9pLmFw'
'cGVuZCgia2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCIpCiMgQm8gdGVzdCAobXVjIDIgdmEgTjcpIGNhbiBQeVlBTUw6IHRo'
'aWV1IG5vLCAwZWE5NWRlIHJhIDk2LzE2NiBjYSBETyAoODkgYmFvIHRoYW5nICJObyBtb2R1bGUgbmFtZWQgJ3lhbWwnIiwK'
'IyA3IHF1YSBsdW90IGNvbjsgY28gUHlZQU1MOiAxNjYvMTY2IFFVQSkuIEJvIGRvIGdvaSBjaHVuZyBsYSAiY2EgRE8gTEEi'
'IHJvaSBwaGF0IFRSVU9UIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBjLgojIERpZXUga2llbiB0aWVuIHF1eWV0IHBoYWkgaG9p'
'IGJhbmcgQ0hJTkggdGllbiB0cmluaCBjb24gc2UgY2hheSBibyB0ZXN0IChjaGF5KCk6IGN1bmcgbW9pIHRydW9uZzsgY3dk'
'ID0gb3BzLyA9CiMgc3lzLnBhdGhbMF0gY3VhIGJvIHRlc3QpIHZhIGhvaSBEVU5HIERVT0MgY2h1IGtob25nIGhvaSBDTyBN'
'QVQuIEJhbiAzMGQgaG9pIGBmaW5kX3NwZWMoInlhbWwiKWAgbyB0aWVuIHRyaW5oCiMgTkFZIHZhIG5ndW9uZyAzLjggc3V5'
'IHR1IE5HVSBQSEFQIChgOj1gKSDigJQgZG8gdHJlbiAyMDI2LTA5LTMwZCwgY2EgaGFpIHJhIHJjPTEgVFJVT1QgY2hvIHVu'
'ZyB2aWVuIHNhY2g6CiMgdGh1IG11YyBkdSBsaWV1IGB5YW1sL2AgdHJlbiBQWVRIT05QQVRIIHF1YSBmaW5kX3NwZWMgbWEg'
'YHlhbWwuc2FmZV9kdW1wYCBraG9uZyBjbyAoODcgY2EgImxhIik7IHB5dGhvbiAzLjguMjAKIyBUSEFUIGNvIFB5WUFNTCwg'
'Ym8gdGVzdCBkdW5nIGBzdHIucmVtb3ZlcHJlZml4YCAoMy45KSBsdWMgQ0hBWSAoMzMgY2EgImxhIjsgMy45LjIzOiAxNjYv'
'MTY2KS4KIyAiRHVuZyBkdW9jIiBuZ2hpYSBsYSBkdW5nIERVTkcgQVBJIGJvIHRlc3QgZ29pOiB2aWV0KCkgKDQzIGxvaSBn'
'b2kpIHZhIGxlYXNlX3B1Ymxpc2gucHkgZ29pIHNhZmVfZHVtcCguLi4sIGFsbG93X3VuaWNvZGU9VHJ1ZSwKIyBzb3J0X2tl'
'eXM9RmFsc2UpLCBtYSBgc29ydF9rZXlzYCBjaGkgY28gdHUgUHlZQU1MIDUuMS4gRG8gdHJlbiAyMDI2LTA5LTMwbCwgMGVh'
'OTVkZTogcHl0aG9uIDMuOS4yMyArIFB5WUFNTCAzLjEzIFRIQVQgcXVhIHByb2JlCiMgY3UgKHJjPTApLCBibyB0ZXN0IDEw'
'OS8xNjYg4oCUIDU2IGNhICJsYSI6IDUyIGB1bmV4cGVjdGVkIGtleXdvcmQgYXJndW1lbnQgJ3NvcnRfa2V5cydgLCB0MjYv'
'dDI3IGBSZWFkZXJFcnJvcmAgKGt5IHR1IG5nb2FpIEJNUCksCiMgdDEyNC90MTUzIERPIHRoZW8gbHVvdCBjb24g4oCUIGUy'
'ZSByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYDsgUHlZQU1MIDUuMTogMTY2LzE2NiAoZG8gbGFpIDIwMjYtMTAtMDE6IGN1bmcg'
'c28pLgojIChQeXRob24gPj0gMy4xMCArIFB5WUFNTCAzLjEzIGRhIHRydW90IHByb2JlIGN1IHZpIGBjb2xsZWN0aW9ucy5I'
'YXNoYWJsZWAuKSBQcm9iZSBjdWEgcHMxICgkbWFUaHUpIHBoYWkgR0lPTkcgSEVUIGRvbmcgZHVvaS4KaWYgbm90ICgiLS1j'
'aGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Ygb3IgIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndik6CiAgICBfcmNfZGssIF9y'
'YV9kayA9IGNoYXkoWyItYyIsICJpbXBvcnQgc3lzOyBzeXMuZXhpdCg5KSBpZiBzeXMudmVyc2lvbl9pbmZvIDwgKDMsIDkp'
'IGVsc2UgTm9uZTsgaW1wb3J0IHlhbWw7IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiIHlhbWwuc2FmZV9k'
'dW1wKHlhbWwuc2FmZV9sb2FkKCdhOiAxJyksIGFsbG93X3VuaWNvZGU9VHJ1ZSwgc29ydF9rZXlzPUZhbHNlKSJdLAogICAg'
'ICAgICAgICAgICAgICAgICAgICAgIGdvYyAvICJvcHMiIGlmIChnb2MgLyAib3BzIikuaXNfZGlyKCkgZWxzZSBQYXRoLmN3'
'ZCgpLCBwaHV0PTIpCiAgICBpZiBfcmNfZGsgPT0gOToKICAgICAgICBsb2kuYXBwZW5kKGYicHl0aG9uIHtzeXMudmVyc2lv'
'bi5zcGxpdCgpWzBdfSA8IDMuOTogYm8gdGVzdCBjdWEgdW5nIHZpZW4gZHVuZyBzdHIucmVtb3ZlcHJlZml4ICgzLjkpIGx1'
'YyBDSEFZIikKICAgIGVsaWYgX3JjX2RrOgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24gbmF5IEtIT05HIGNvIFB5WUFN'
'TCBkdW5nIGR1b2MgKHsoX3JhX2RrLnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10pWy0xXVs6OTBdfSk6IgogICAgICAg'
'ICAgICAgICAgICAgZiIgXCJ7c3lzLmV4ZWN1dGFibGV9XCIgLW0gcGlwIGluc3RhbGwgLVUgcHl5YW1sIgogICAgICAgICAg'
'ICAgICAgICAgIiAoYmFuIG5odW5nIHBzMSB0dSB0YWkgS0hPTkcgY28gcGlwOiBjaGF5IGxhaSB2b2kgLVB5IDxweXRob24g'
'ZGEgY28gUHlZQU1MPikiKQogICAgIyBCbyB0ZXN0IGNvbiBnb2kgYHNodXRpbC53aGljaGAgY2hvIGJhc2gvYWN0aW9ubGlu'
'dC9zaGVsbGNoZWNrICgwZWE5NWRlOiB0MzMgdDEzNyB0MTU5IGNhbiBhY3Rpb25saW50LCB0MTM3IGNhbgogICAgIyBzaGVs'
'bGNoZWNrLCBjYWMgY2EgY2hheSBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggY2FuIGJhc2gpLiBUaGlldSB0aGkgY2FjIGNhIGF5'
'IGluICJLSE9ORyBETyBEVU9DOiB0aGlldSBgLi4uYCIgdmEgYm8gZG8gcmEKICAgICMgcmM9MyDigJQgbmh1bmcgY2hpIFNB'
'VSBjYSBibyB0ZXN0IGxhbiBONyAoZG8gdHJlbiAyMDI2LTA5LTMwZywgUEFUSCB0aGlldSBhY3Rpb25saW50OiBgQ29uZyBj'
'dSBkYXkgZHUgZGUgZG9gIEtERCwgcmM9MwogICAgIyBzYXUgMiBsdW90IGJvIHRlc3QpLiBDdW5nIGx5IGRvIFB5WUFNTCBk'
'dW9jIGhvaSBvIGRheTogaG9pIFRSVU9DLCBjdW5nIFBBVEggbWEgY2hheSgpIHRydXllbiBjaG8gYm8gdGVzdC4KICAgICMg'
'VkEgY3VuZyBDSE8gYm8gdGVzdCBkdW5nOiB0cmVuIFdpbmRvd3MgYHNodXRpbC53aGljaGAgdHJhIFRIVSBNVUMgSElFTiBI'
'QU5IIFRSVU9DIFBBVEgsIG1hIGJvIHRlc3QgY2hheSB2b2kgY3dkID0gZ29jIGNvbgogICAgIyB0aWVuIHRyaW5oIG5heSBk'
'dW5nIG8gY3dkIENVQSBOR1VPSSBETyAobm9pIGdvaSBwczEsIHZkLiBEb3dubG9hZHMg4oCUIGR1bmcgbm9pIGdpYWkgbmVu'
'IGFjdGlvbmxpbnQuZXhlKS4gRG8gdHJlbiAyMDI2LTA5LTMwawogICAgIyAobmhhbmggd2luMzIgVEhBVCBjdWEgc2h1dGls'
'LndoaWNoKTogYWN0aW9ubGludCB0b3QgbyBjd2Qgbmd1b2kgZG8gKyBiYW4gaG9uZyBkYXUgUEFUSCA9PiBtdWMgMCBob2kg'
'YmFuIG8gY3dkIChyYz0wKSwgYm8gdGVzdAogICAgIyBkdW5nIGJhbiB0cmVuIFBBVEggPT4gcmM9MSBgREFUIDExIHwgVFJV'
'T1QgMWAsIGBsYTogWyd0MzMnLCAndDEzNycsICd0MTU5J11gLiBHaWFpIHRlbiB2b2kgY3dkID0gZ29jIHJvaSBnb2kgVEhB'
'TkcgYmFuZyBkdW9uZwogICAgIyBUVVlFVCBET0kgZGEgZ2lhaSAocXVhIGhhbiB0aGkgcnVuKCkgZ2lldCBkdW5nIHRpZW4g'
'dHJpbmgg4oCUIGx5IGRvIGJhbiAzMGkga2hvbmcgaG9pIHF1YSBjaGF5KCkpLgogICAgX2N3ZF9uZ3VvaV9kbyA9IG9zLmdl'
'dGN3ZCgpCiAgICB0cnk6CiAgICAgICAgaWYgZ29jLmlzX2RpcigpOiBvcy5jaGRpcihnb2MpCiAgICAgICAgX2NjID0ge2M6'
'IChvcy5wYXRoLmFic3BhdGgocCkgaWYgcCBlbHNlIE5vbmUpIGZvciBjLCBwIGluCiAgICAgICAgICAgICAgICgoYywgc2h1'
'dGlsLndoaWNoKGMpKSBmb3IgYyBpbiAoImJhc2giLCAiYWN0aW9ubGludCIsICJzaGVsbGNoZWNrIikpfQogICAgZmluYWxs'
'eToKICAgICAgICBvcy5jaGRpcihfY3dkX25ndW9pX2RvKQogICAgX3RoaWV1X2NjID0gW2MgZm9yIGMsIHAgaW4gX2NjLml0'
'ZW1zKCkgaWYgbm90IHBdCiAgICBpZiBfdGhpZXVfY2M6CiAgICAgICAgbG9pLmFwcGVuZChmInRoaWV1IGNvbmcgY3UgYm8g'
'dGVzdCBnb2kgcXVhIFBBVEg6IHtfdGhpZXVfY2N9IChhY3Rpb25saW50OiBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggdm9pIEFM'
'X1ZFUjsiCiAgICAgICAgICAgICAgICAgICAiIGJhc2g6IEdpdCBCYXNoLCBraG9uZyBwaGFpIGJhc2guZXhlIGN1YSBXU0wp'
'IikKICAgICMgc2hlbGxjaGVjayBLSE9ORyBuaGFuIC0tbm9yYyB0aGkgYWN0aW9ubGludCAxLjcuNyAodHUgdHJ1eWVuIC0t'
'bm9yYykgbGFtIHQzMyBETywgdmEgU0hFTExDSEVDS19PUFRTPS0tbm9yYyBjdWEgY2hheSgpIGxhbQogICAgIyB0MTM3IERP'
'IOKAlCBjYSAibGEiID0+IFRSVU9UIGdpYSAoZG8gdHJlbiAyMDI2LTA5LTMwaCwgc2hlbGxjaGVjayBnaWEgdHUgY2hvaSAt'
'LW5vcmM6IGJhbiAzMGggcmM9MSBgbGE6IFsndDMzJ11gIHNhdSBjYQogICAgIyBibyB0ZXN0KS4gYHdoaWNoYCBjaGkgaG9p'
'IENPIE1BVDsgbyBkYXkgaG9pIERVTkcgRFVPQy4gTmd1b25nIGRvIHRyZW4gc2hlbGxjaGVjayBUSEFUOiAwLjQuNy8wLjUu'
'MC8wLjYuMCB0dSBjaG9pIC0tbm9yYwogICAgIyAocmM9MyksIDAuNy4wIHRybyBsZW4gbmhhbi4gUGhlcCBob2kgcGhhaSB0'
'aGF5IERVTkcgU0hFTExDSEVDS19PUFRTIG1hIGNoYXkoKSBkYXQgY2hvIGx1b3QgY29uOiBiYW4gMzBpIGhvaSB2b2kgYmll'
'biBDVUEKICAgICMgTkdVT0kgRE8g4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGksIHNoZWxsY2hlY2sgMC45LjAgKyBTSEVMTENI'
'RUNLX09QVFM9LS1leHRlbmRlZC1hbmFseXNpcz10cnVlIChjbyBjdWEgMC4xMCk6IHJjPTMgImtob25nIG5oYW4KICAgICMg'
'LS1ub3JjOiBjYXAgbmhhdCBzaGVsbGNoZWNrIiB0cm9uZyBraGkgdDMzL3QxMzcgcXVhIGNoYXkoKSBkZXUgMS8xLiBHb2kg'
'VEhBTkcgKGtob25nIHF1YSBjaGF5KCkpOiBxdWEgaGFuIHRoaSBydW4oKSBnaWV0CiAgICAjIGR1bmcgc2hlbGxjaGVjazsg'
'cXVhIGNoYXkoKSB0aGkgY2hpIGdpZXQgcHl0aG9uIGNvbiwgc2hlbGxjaGVjayB0cmVvIG8gbGFpIG1vIGNvaSAoZG8gdHJl'
'biAyMDI2LTA5LTMwaTogMS8xIGNvbiBzb25nKS4KICAgIGVsaWYgc3VicHJvY2Vzcy5ydW4oW19jY1sic2hlbGxjaGVjayJd'
'LCAiLS1ub3JjIiwgIi0tdmVyc2lvbiJdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0aW1lb3V0PTYwLAogICAgICAgICAgICAg'
'ICAgICAgICAgICBlbnY9ZGljdChvcy5lbnZpcm9uLCBTSEVMTENIRUNLX09QVFM9Ii0tbm9yYyIpKS5yZXR1cm5jb2RlOgog'
'ICAgICAgIGxvaS5hcHBlbmQoInNoZWxsY2hlY2sgdHJlbiBQQVRIIGtob25nIG5oYW4gLS1ub3JjIChhY3Rpb25saW50IDEu'
'Ny43IHZhIGNoYXkoKSBkZXUgdHJ1eWVuIGNvIGF5KTogY2FwIG5oYXQgc2hlbGxjaGVjayIpCiAgICAjIGFjdGlvbmxpbnQg'
'Y3VuZyBwaGFpIERVTkcgRFVPQywga2hvbmcgY2hpIENPIE1BVDogdDMzL3QxMzcvdDE1OSBnb2kgbm8gVEhBTkcsIHZhIG1v'
'dCBhY3Rpb25saW50IGtob25nIGNoYXkgKHNhaSBraWVuIHRydWMsCiAgICAjIGhvbmcpIGxhbSBjYSBiYSBETyAiYWN0aW9u'
'bGludCBETyAocmM9Li4uKSIg4oCUIGNhICJsYSIgPT4gVFJVT1QgZ2lhIHNhdSBjYSBibyB0ZXN0IChkbyB0cmVuIDIwMjYt'
'MDktMzBqOiBhY3Rpb25saW50IGdpYQogICAgIyByYz0xID0+IG11YyAwIGltIGxhbmcsIHQzMyAibGEiKS4gQmFuIFRIQVQg'
'MS42LjI3LzEuNy43LzEuNy44LzEuNy4xMiBkZXUgcmM9MCB2YSBkZXUgY2hvIHQzMy90MTM3L3QxNTkgUVVBIHRyZW4gMGVh'
'OTVkZS4KICAgICMgYmFzaCBxdWEgYHdoaWNoYCBDSEkgaG9pIENPIE1BVCwgY28gY2h1IGRpY2g6IHQzNS10NDAgZ29pIGBi'
'YXNoYCBUUkFOIChiYXNoIFdTTCBsYW0gY2h1bmcgRE8sIGRldSBOR09BSV9QSEFNX1ZJIOKAlCBkbyB0cmVuCiAgICAjIDIw'
'MjYtMDktMzBqKS4gOSBjYSBUUk9ORyBwaGFtIHZpIEtIT05HIGdvaSBiYXNoIHF1YSBgd2hpY2hgIOKAlCB4ZW0gY2hvdCBg'
'X2Jhc2hfcG9zaXgoKWAgZHVvaSBjaG90IGdpdC4KICAgICMgQ0hBWSBEVU9DIGNodWEgcGhhaSBEVU5HIERVT0M6IGRvIHRy'
'ZW4gMjAyNi0wOS0zMGssIDBlYTk1ZGUsIGFjdGlvbmxpbnQgVEhBVCAxLjQuMy8xLjUuMC8xLjUuMy8xLjYuMC8xLjYuOC8x'
'LjYuMTUvMS42LjIwLwogICAgIyAxLjYuMjIgZGV1IGAtdmVyc2lvbmAgcmM9MCwgbWEgY2EgdGFtIGxhbSB0MTM3L3QxNTkg'
'RE8gKGBwcm9wZXJ0eSAicnVuX2F0dGVtcHQiLyJ3b3JrZmxvd19zaGEiIGlzIG5vdCBkZWZpbmVkYCksIDEuNC4zLzEuNS4w'
'CiAgICAjIHRoZW0gdDMzIChgbXVzdCBiZSBjb250YWluZWQgd2l0aGluICR7eyB9fWApIOKAlCBlMmUgMS42LjIyOiByYz0x'
'IGBEQVQgMTEgfCBUUlVPVCAxYCwgYGxhOiBbJ3QxMzcnLCAndDE1OSddYCBjaG8gdW5nIHZpZW4KICAgICMgc2FjaDsgMS42'
'LjIzLzEuNi4yNC8xLjYuMjYvMS42LjI3LzEuNy4wLzEuNy42LzEuNy43LzEuNy4xMiBRVUEgY2EgYmEuIFNhbiBsYSBiYW4K'
'ICAgICMgZ2hpbSBDSSAoQUxfU0FOKSwgS0hPTkcgcGhhaSAxLjYuMjMgZG8gdHJlbiBNT1QgdW5nIHZpZW46IHdvcmtmbG93'
'IGN1YSB1bmcgdmllbiBzYXUgY28gdGhlIGR1bmcgY3UgcGhhcCBtb2kgaG9uLCBtYSBDSSBjaGkgZG8KICAgICMgYmFuZyBi'
'YW4gZ2hpbS4gQ3UgaG9uIHNhbiA9PiBLSE9ORyBETyBEVU9DIChjaGFuIGNhIDEuNi4yMy0xLjcuNiBkYW5nIFFVQTogZmFp'
'bC1jbG9zZSwga2hvbmcgcGhhaSBwaGFuIHF1eWV0KS4gYHZgIGRhdTogYmFuCiAgICAjIGBnbyBpbnN0YWxsYCBpbiBgdjEu'
'Ny43YDsga2hvbmcgZG9jIGR1b2Mgc28gKHZkLiBgKGRldmVsKWApID0+IEtIT05HIERPIERVT0MuCiAgICBpZiBub3QgX3Ro'
'aWV1X2NjOgogICAgICAgIF9hbCA9IHN1YnByb2Nlc3MucnVuKFtfY2NbImFjdGlvbmxpbnQiXSwgIi12ZXJzaW9uIl0sIGNh'
'cHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwKICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PTYwKQogICAgICAgIF9hbF92ID0gcmUuc2VhcmNoKHIiKD9tKV52Pyhc'
'ZCspXC4oXGQrKVwuKFxkKykiLCBfYWwuc3Rkb3V0IG9yICIiKQogICAgICAgIGlmIF9hbC5yZXR1cm5jb2RlOgogICAgICAg'
'ICAgICBsb2kuYXBwZW5kKCJhY3Rpb25saW50IHRyZW4gUEFUSCBjbyBtYXQgbmh1bmcgYGFjdGlvbmxpbnQgLXZlcnNpb25g'
'IHJjIT0wIChraG9uZyBjaGF5IGR1b2MpOiBjYWkgbGFpIGJhbiBnaGltIEFMX1ZFUiIpCiAgICAgICAgZWxpZiBub3QgX2Fs'
'X3Ygb3IgdHVwbGUoaW50KHgpIGZvciB4IGluIF9hbF92Lmdyb3VwcygpKSA8IEFMX1NBTjoKICAgICAgICAgICAgbG9pLmFw'
'cGVuZChmImFjdGlvbmxpbnQge19hbF92Lmdyb3VwKDApIGlmIF9hbF92IGVsc2UgJyhraG9uZyBkb2MgZHVvYyBwaGllbiBi'
'YW4pJ30gY3UgaG9uIGJhbiBnaGltIENJICIKICAgICAgICAgICAgICAgICAgICAgICBmInsnLicuam9pbihtYXAoc3RyLCBB'
'TF9TQU4pKX0gKEFMX1ZFUik6IGJhbiBjdSBsYW0gdDEzNy90MTU5IERPICdsYScgdHJlbiB1bmcgdmllbiBzYWNoIOKAlCIK'
'ICAgICAgICAgICAgICAgICAgICAgICAiIGNhaSBiYW4gZ2hpbSAob3BzL2NhaV9hY3Rpb25saW50LnNoIHZvaSBBTF9WRVIp'
'IikKICAgICAgICAjIGdpdCBjdW5nIHRoZTogQ08gTUFUIGtob25nIHBoYWkgRFVORyBEVU9DLCB2YSBnaXQgQ1UgbGEgY29u'
'ZyBjdSBQSE8gQklFTiBuaGF0IHRyb25nIGJvbi4gRG8gdHJlbiAyMDI2LTA5LTMwbCwgMGVhOTVkZSwgZ2l0CiAgICAgICAg'
'IyBUSEFUIHF1YSBjdW5nIGNoYXkoKTogMi4yNS4xID0+IDE0MC8xNjYgKDIzIGNhICJsYSI6IGBpbml0IC1iYC4uLiksIDIu'
'MzQuMSB2YSAyLjM1LjEgPT4gMTYzLzE2NiAodDEwOSB0MTEwIHQxMTE6IGBnaXQKICAgICAgICAjIHdvcmt0cmVlIGxpc3Qg'
'LS1wb3JjZWxhaW4gLXpgIHJjPTEyOSBgdW5rbm93biBzd2l0Y2ggemApLCBlMmUgMi4zNS4xIHJjPTEgYERBVCAxMSB8IFRS'
'VU9UIDFgOyAyLjM2LjEgPT4gMTY2LzE2Ni4gU2FuIGxheQogICAgICAgICMgdHUgdGluaCBuYW5nIG1hIENISU5IIG1hIGR1'
'b2MgZG8gZ29pIChvcHMvY29uZ19jdS55YW1sIGRlIGJhbl9naGltIGdpdCA9IG51bGwgbmVuIGtob25nIGNvIGJhbiBnaGlt'
'IENJIGRlIGR1YSB2YW8pLgogICAgICAgICMgYGdpdCB2ZXJzaW9uIDIuNDcuMS53aW5kb3dzLjFgIChHaXQgZm9yIFdpbmRv'
'd3MpIHZhIGAyLjM5LjMgKEFwcGxlIEdpdC0xNDYpYCBkZXUgZG9jIGR1b2MgYmEgc28gZGF1LgogICAgICAgICMgVmEgcGhh'
'aSBob2kgRFVORyBnaXQgbWEgYm8gdGVzdCBTRSBHT0kuIEJvIHRlc3QgS0hPTkcgYHNodXRpbC53aGljaCgiZ2l0IilgIG5o'
'dSBiYSBjb25nIGN1IHRyZW46IEdPSV9HSVQgY3VhIHVuZyB2aWVuIHZhIG1vaQogICAgICAgICMgZml4dHVyZSBnb2kgYGdp'
'dGAgVFJBTiDigJQgdHJlbiBXaW5kb3dzIGxhIENyZWF0ZVByb2Nlc3NXOiBDSEkgdHUgdGhlbSBgLmV4ZWAgKEtIT05HIFBB'
'VEhFWFQpLCB0cmEgdGh1IG11YyBweXRob24uZXhlLCBjd2QKICAgICAgICAjIHZhIFN5c3RlbTMyIFRSVU9DIFBBVEguIGB3'
'aGljaGAgdGhpIHRyYSBQQVRIRVhULCBuZW4gbW90IGBnaXQuY21kYC9gZ2l0LmJhdGAgZHVuZyB0cnVvYyBgZ2l0LmV4ZWAg'
'Q1UgdHJlbiBQQVRIIGR1b2MgaG9pCiAgICAgICAgIyBUSEFZIG5vIOKAlCBkbyB0cmVuIDIwMjYtMTAtMDEgKG5oYW5oIHdp'
'bjMyIFRIQVQgY3VhIHNodXRpbC53aGljaDsgc2hpbSBgZ2l0LkNNRGAgbW9pIHRydW9jIGdpdCAyLjM1LjEgVEhBVCk6IGJh'
'biAzMG0gbXVjIDAKICAgICAgICAjIGltLCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0MTA5JywgJ3Qx'
'MTAnLCAndDExMSddYC4gTmVuIGhvaSBiYW5nIENISU5IIGR1b25nIGF5OiB0aWVuIHRyaW5oIGNvbiBjdWEgY2hheSgpCiAg'
'ICAgICAgIyAoY3VuZyBweXRob24sIGN1bmcgbW9pIHRydW9uZywgY3dkID0gZ29jIG5odSBibyB0ZXN0KSBnb2kgYGdpdCAt'
'LXZlcnNpb25gIFRSQU4uCiAgICAgICAgX3JjX2d2LCBfcmFfZ3YgPSBjaGF5KFsiLWMiLCAiaW1wb3J0IHN1YnByb2Nlc3Ms'
'IHN5czsgcCA9IHN1YnByb2Nlc3MucnVuKFsnZ2l0JywgJy0tdmVyc2lvbiddLCBjYXB0dXJlX291dHB1dD1UcnVlLCIKICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgdGV4dD1UcnVlLCB0aW1lb3V0PTYwKTsgcHJpbnQocC5zdGRv'
'dXQpOyBzeXMuZXhpdChwLnJldHVybmNvZGUpIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGdvYyBpZiBnb2Mu'
'aXNfZGlyKCkgZWxzZSBQYXRoLmN3ZCgpLCBwaHV0PTIpCiAgICAgICAgX2d2X20gPSByZS5zZWFyY2gociIoP20pXmdpdCB2'
'ZXJzaW9uXHMrKFxkKylcLihcZCspXC4oXGQrKSIsIF9yYV9ndikKICAgICAgICBnaGkoImdpdF9ib190ZXN0IiwgX2d2X20u'
'Z3JvdXAoMCkgaWYgX2d2X20gZWxzZSBOb25lKQogICAgICAgIGlubigiICBnaXQgYm8gdGVzdCAgOiIsIF9ndl9tLmdyb3Vw'
'KDApIGlmIF9ndl9tIGVsc2UgZiIoa2hvbmcgZG9jIGR1b2MgcGhpZW4gYmFuLCByYz17X3JjX2d2fSkiKQogICAgICAgIGlm'
'IF9yY19ndjoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImBnaXQgLS12ZXJzaW9uYCBnb2kgVFJBTiBuaHUgYm8gdGVzdCBy'
'YyE9MCAoeyhfcmFfZ3Yuc3RyaXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFdWzo5MF19KTogY2FpIGxhaSBnaXQiKQog'
'ICAgICAgIGVsaWYgbm90IF9ndl9tIG9yIHR1cGxlKGludCh4KSBmb3IgeCBpbiBfZ3ZfbS5ncm91cHMoKSkgPCBHSVRfU0FO'
'OgogICAgICAgICAgICBsb2kuYXBwZW5kKGYiZ2l0IHsnLicuam9pbihfZ3ZfbS5ncm91cHMoKSkgaWYgX2d2X20gZWxzZSAn'
'KGtob25nIGRvYyBkdW9jIHBoaWVuIGJhbiknfSBjdSBob24gIgogICAgICAgICAgICAgICAgICAgICAgIGYieycuJy5qb2lu'
'KG1hcChzdHIsIEdJVF9TQU4pKX0gKHVuZyB2aWVuIGdvaSBgZ2l0IHdvcmt0cmVlIGxpc3QgLS1wb3JjZWxhaW4gLXpgKTog'
'Y2FwIG5oYXQgZ2l0IikKICAgICAgICAjIGJhc2ggY3VuZyBIT0kgU0FJIENITyBuaHUgZ2l0OiA5IGNhIFRST05HIHBoYW0g'
'dmkgKHQzMiB0NTEgdDU5IHQ2MCB0NjIgdDYzIHQ2NiB0NjggdDE1MikgY2hheSBiYXNoIGJhbmcgYF9iYXNoX3Bvc2l4KClg'
'CiAgICAgICAgIyBjdWEgdW5nIHZpZW4g4oCUIEdpdCBCYXNoIG8gZHVvbmcgQ08gRElOSCBgQzpcUHJvZ3JhbSBGaWxlc1xH'
'aXRcYmluXGJhc2guZXhlYCAodmEgYCh4ODYpYCwgYHVzclxiaW5gKSwgcm9pCiAgICAgICAgIyBgd2hpY2goImJhc2giKWAg'
'TkhVTkcgbG9haSBrZXQgcXVhIHRyb25nIFN5c3RlbTMyIChXU0wpOyBraG9uZyB0aGF5IHRoaSB0cmEgIiIuIE1heSBjbyBX'
'U0wgbWEgR2l0IGtob25nIG8gUHJvZ3JhbSBGaWxlcwogICAgICAgICMgKE1pbkdpdCBkbyBDSElOSCBwczEgdHUgdGFpIOKA'
'lCBNaW5HaXQgS0hPTkcgY28gYmFzaDsgc2Nvb3A7IGNhaSBwZXItdXNlcikgcXVhIGNob3QgYHdoaWNoYCBvIHRyZW4sIHJv'
'aSBgX2Jhc2hfcG9zaXgoKWAKICAgICAgICAjID09ICIiOiB0MzIgIktIT05HIERPIERVT0MiICsgOCBjYSAibGEiIGBzdWJw'
'cm9jZXNzLnJ1bihbIiIuLi5dKWAsIGNoaSBsbyByYSBTQVUgY2EgaGFpIGx1b3QgYm8gdGVzdC4gRG8gdHJlbiAyMDI2LTEw'
'LTAxOgogICAgICAgICMgaGFtIFRIQVQsIG5oYW5oIG9zLm5hbWU9J250JyAoV1NMICsgTWluR2l0L3Njb29wL3Blci11c2Vy'
'KSA9PiAnJzsgYm8gdGVzdCB2b2kgZ2lhIHRyaSBheSAxNTcvMTY2OyBlMmUgKHdpbjMyIGdpYSkgcmM9MwogICAgICAgICMg'
'c2F1IDM0NyBzLCBgVFJVT1QgTW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MgIGxhOiBbJ3Q1MScsICd0NTknLCAndDYw'
'JywgJ3Q2MicsICd0NjMnLCAndDY2JywgJ3Q2OCcsICd0MTUyJ11gLiBQaGVwCiAgICAgICAgIyBkbyAzMGogY2hheSB0cmVu'
'IExpbnV4LCBub2kgYF9iYXNoX3Bvc2l4KClgIGx1b24gdHJhICJiYXNoIiwgbmVuIGtob25nIHRoZSB0aGF5IGR1b25nIG5h'
'eS4KICAgICAgICAjIFZhIGBnaXRgIFRST05HIGJhc2ggYXkgbGEgZ2l0IFRIVSBCQTogYEdpdFxiaW5cYmFzaC5leGVgIGxh'
'IGNvbXBhdC1iYXNoIGN1YSBnaXQtd3JhcHBlciwgYHNldHVwX2Vudmlyb25tZW50KClgIGRheQogICAgICAgICMgYDxnb2Mg'
'R2l0PlxtaW5ndzY0XGJpbjs8Z29jIEdpdD5cdXNyXGJpbmAgbGVuIERBVSBQQVRIIChnaXQtZm9yLXdpbmRvd3MvTUlOR1ct'
'cGFja2FnZXM6IGdpdC13cmFwcGVyLmMgKyBjb21wYXQtYmFzaC5yYywKICAgICAgICAjIGtob25nIGNvIE1JTklNQUxfUEFU'
'SCkg4oCUIHR1YyBnaXQgREkgS0VNIGJhbiBHaXQgYXksIEtIT05HIHBoYWkgZ2l0IFRSQU4gZGEgaG9pIG8gdHJlbi4gdDE1'
'MiBjaGF5IEdJVF9DT05GSUdfQ09VTlQgKGdpdAogICAgICAgICMgMi4zMSkgdHJvbmcgYmFzaCBheS4gRG8gdHJlbiAyMDI2'
'LTEwLTAxIChiYXNoIGJvYyBkYXkgZ2l0IGRpIGtlbSBsZW4gZGF1IFBBVEgsIGdpdCBUUkFOIDIuNDMpOiBnaXQgZGkga2Vt'
'IDIuMzAuMiBUSEFUID0+CiAgICAgICAgIyAxNjUvMTY2LCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0'
'MTUyJ11gIGNobyB1bmcgdmllbiBzYWNoOyAyLjMxLjAgVEhBVCA9PiAxNjYvMTY2LiBIb2kgQ0hJTkggaGFtIGF5IHZhCiAg'
'ICAgICAgIyBDSElOSCBiYXNoIGF5IHRyb25nIHRpZW4gdHJpbmggY29uIGN1YSBjaGF5KCkgKGN1bmcgcHl0aG9uLCBjdW5n'
'IG1vaSB0cnVvbmcsIGN3ZCA9IGdvYyk7IHVuZyB2aWVuIGtob25nIGNvIGhhbSB0aGkga2hvbmcKICAgICAgICAjIGhvaSAo'
'Z2l1IGNob3QgQ08gTUFUKS4KICAgICAgICAjIERvYyBkb25nIGBnaXQgdmVyc2lvbmAgQ1VPSSBjdWEgc3Rkb3V0LCBLSE9O'
'RyBkb2MgZG9uZyBEQVUgKGJhbiAwMWI6IEJBU0hfRU5WIGBlY2hvYCBtb3QgZG9uZyA9PiBtdWMgMCBLREQgb2FuOyB0dSBi'
'YW4gMDFlCiAgICAgICAgIyBjaGF5KCkgYm8gQkFTSF9FTlYsIGNhY2ggZG9jIG5heSBnaXUgbGFpIHZpIHZvIGhhaSkuIEJh'
'c2ggdHJlbyB0aGkgYmF0IG5nb2FpIGxlIFRST05HIGNvbiAoYmFuIDAxYiBkbyBsb2kgY2hvCiAgICAgICAgIyBgX2Jhc2hf'
'cG9zaXgoKWApIHZhIERVTkcgbHVvbiAoa2hvbmcgaG9pIGxhbiBoYWk6IGdpdSB0cmFuIDYwIHMgdmEgbW90IHRpZW4gdHJp'
'bmggbW8gY29pIG5odSBiYW4gMDFjKS4KICAgICAgICAjIFZhIGhvaSBIQUkgbGFuLCBkdW5nIEhBSSBtb2kgdHJ1b25nIGJv'
'IHRlc3QgVEhBVCBkdW5nOiAzIGxvaSBnb2kgYF9iYXNoX3Bvc2l4KClgIGN1YSB1bmcgdmllbiBjaGF5IGJhc2ggdm9pIDIg'
'bW9pIHRydW9uZyDigJQKICAgICAgICAjIHQzMi90NTEtdDY4IGBkaWN0KG9zLmVudmlyb24sIC4uLilgIChtb2kgdHJ1b25n'
'IGN1YSBjaGF5KCkpLCBjb24gdDE1MiAoY2EgRFVZIE5IQVQgY2FuIHNhbiAyLjMxKQogICAgICAgICMgYGRpY3QoUEFUSD1v'
'cy5lbnZpcm9uWyJQQVRIIl0sIFRMXyosIEdJVF9DT05GSUdfKilgLiBCYW4gMDFjIGhvaSBvIG1vaSB0cnVvbmcgVEhVIE5I'
'QVQgcm9pIGFwIHNhbiBjdWEgdDE1MiDigJQgZG8gdHJlbgogICAgICAgICMgMjAyNi0xMC0wMTogZ2l0IGRpIGtlbSAyLjMw'
'LjIgVEhBVCArIEJBU0hfRU5WIGRheSBnaXQgMi40MyBsZW4gZGF1IFBBVEggPT4gbXVjIDAgdGhheSAyLjQzLCBlMmUgcmM9'
'MSBgREFUIDExIHwgVFJVT1QgMWAsCiAgICAgICAgIyBgbGE6IFsndDE1MiddYCBjaG8gdW5nIHZpZW4gc2FjaC4gVHUgYmFu'
'IDAxZSBjaGF5KCkgYm8gQkFTSF9FTlYgbmVuIGR1b25nIGF5IGRvbmcgbyBHT0M7IGhhaSBsYW4gaG9pIGdpdSBsYWkgdmkg'
'aGFpIG1vaQogICAgICAgICMgdHJ1b25nIFZBTiBraGFjIG5oYXUuIExhbiBob2kgbyBtb2kgdHJ1b25nIHRodSBuaGF0IENI'
'SSBjaHVuZyBtaW5oIGdpdCBDSEFZIGR1b2MgdHJvbmcgYmFzaCBheSwgS0hPTkcgY2h1bmcgbWluaCBiYXNoCiAgICAgICAg'
'IyAiZHVuZyBkdW9jIiBjaG8gdDMyL3Q1MS10NjggKGRvOiBub2Nsb2JiZXIgcXVhIGNhdSBob2kgbmF5IG1hIGxhbSA3IGNh'
'IERPIOKAlCB2aSB2YXkgY2hheSgpIGJvIGJpZW4ga2hvaSBkb25nIGJhc2gsIHhlbQogICAgICAgICMgdHJlbikuIEJBU0hf'
'R0lUID0gbW9pIHRydW9uZyB0MzIvdDUxLXQ2OCAoZG9pIENIQVkgZHVvYyk7IEJBU0hfR0lUX1QxNTIgPSBtb2kgdHJ1b25n'
'IHQxNTIgKGRvaSBzYW4gR0lUX1NBTl9CQVNIKS4KICAgICAgICBfcmNfYnAsIF9yYV9icCA9IGNoYXkoWyItYyIsICJpbXBv'
'cnQgb3MsIHN1YnByb2Nlc3MsIHN5c1xuc3lzLnBhdGguaW5zZXJ0KDAsICdvcHMnKVxuaW1wb3J0IGxlYXNlX3B1Ymxpc2hf'
'dGVzdCBhcyBUXG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZiA9IGdldGF0dHIoVCwgJ19iYXNo'
'X3Bvc2l4JywgTm9uZSlcbmIgPSAnPycgaWYgZiBpcyBOb25lIGVsc2UgZigpXG5wcmludCgnQkFTSF9QT1NJWD0nICsgYilc'
'biIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpZiBiIGFuZCBiICE9ICc/JzpcbiAgZm9yIGsgaW4g'
'KCdCQVNIX0dJVCcsICdCQVNIX0dJVF9UMTUyJyk6XG4gICAgdHJ5OlxuIgogICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgIiAgICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbYiwgJy0tbm9wcm9maWxlJywgJy0tbm9yYycsICctYycsICdn'
'aXQgLS12ZXJzaW9uJ10sIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiBjYXB0dXJlX291dHB1dD1U'
'cnVlLCB0ZXh0PVRydWUsIHRpbWVvdXQ9NjAsIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiBlbnY9'
'Tm9uZSBpZiBrID09ICdCQVNIX0dJVCcgZWxzZSB7J1BBVEgnOiBvcy5lbnZpcm9uWydQQVRIJ119KVxuIgogICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgIiAgICAgIHYgPSBbeCBmb3IgeCBpbiBwLnN0ZG91dC5zcGxpdGxpbmVzKCkg'
'aWYgeC5zdGFydHN3aXRoKCdnaXQgdmVyc2lvbicpXSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIg'
'b3IgcC5zdGRvdXQuc3RyaXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXVxuIgogICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgIiAgICAgIHByaW50KGsgKyAnPScgKyB2Wy0xXSArICcgcmM9JyArIHN0cihwLnJldHVybmNvZGUpKVxuIgog'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6XG4gICAgICBw'
'cmludChrICsgJz0oJyArIHR5cGUoZSkuX19uYW1lX18gKyAnKSByYz0tMScpXG4iCiAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAiICAgICAgYnJlYWtcbiJdLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBnb2MgaWYgZ29j'
'LmlzX2RpcigpIGVsc2UgUGF0aC5jd2QoKSwgcGh1dD0zKQogICAgICAgIF9icF9tID0gcmUuc2VhcmNoKHIiKD9tKV5CQVNI'
'X1BPU0lYPSguKikkIiwgX3JhX2JwKQogICAgICAgIF9icCA9IF9icF9tLmdyb3VwKDEpLnN0cmlwKCkgaWYgKF9icF9tIGFu'
'ZCBub3QgX3JjX2JwKSBlbHNlIE5vbmUKICAgICAgICBfYmdfbSA9IHJlLnNlYXJjaChyIig/bSleQkFTSF9HSVQ9Z2l0IHZl'
'cnNpb25ccysoXGQrKVwuKFxkKylcLihcZCspW15cbl0qXHNyYz0wJCIsIF9yYV9icCkKICAgICAgICBfYnRfbSA9IHJlLnNl'
'YXJjaChyIig/bSleQkFTSF9HSVRfVDE1Mj1naXQgdmVyc2lvblxzKyhcZCspXC4oXGQrKVwuKFxkKylbXlxuXSpcc3JjPTAk'
'IiwgX3JhX2JwKQogICAgICAgIGdoaSgiYmFzaF9ib190ZXN0IiwgX2JwKTsgZ2hpKCJnaXRfdHJvbmdfYmFzaF9ib190ZXN0'
'IiwgX2JnX20uZ3JvdXAoMClbOTpdIGlmIF9iZ19tIGVsc2UgTm9uZSkKICAgICAgICBnaGkoImdpdF90cm9uZ19iYXNoX3Qx'
'NTIiLCBfYnRfbS5ncm91cCgwKVsxNDpdIGlmIF9idF9tIGVsc2UgTm9uZSkKICAgICAgICBpbm4oIiAgYmFzaCBibyB0ZXN0'
'IDoiLCByZXByKF9icCkgaWYgX2JwIGlzIG5vdCBOb25lIGVsc2UgZiIoa2hvbmcgaG9pIGR1b2MsIHJjPXtfcmNfYnB9KSIs'
'CiAgICAgICAgICAgICJ8IGdpdCB0cm9uZyBiYXNoOiIsIF9iZ19tLmdyb3VwKDApWzk6XSBpZiBfYmdfbSBlbHNlICIoa2hv'
'bmcgZG9jIGR1b2MpIiwKICAgICAgICAgICAgInwgbW9pIHRydW9uZyB0MTUyOiIsIF9idF9tLmdyb3VwKDApWzE0Ol0gaWYg'
'X2J0X20gZWxzZSAiKGtob25nIGRvYyBkdW9jKSIpCiAgICAgICAgaWYgX2JwIGlzIE5vbmU6CiAgICAgICAgICAgIGxvaS5h'
'cHBlbmQoZiJraG9uZyBob2kgZHVvYyBgX2Jhc2hfcG9zaXgoKWAgY3VhIGJvIHRlc3QgKHJjPXtfcmNfYnB9OiIKICAgICAg'
'ICAgICAgICAgICAgICAgICBmIiB7KF9yYV9icC5zdHJpcCgpLnNwbGl0bGluZXMoKSBvciBbJyddKVstMV1bOjkwXX0pIikK'
'ICAgICAgICBlbGlmIG5vdCBfYnA6CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJgX2Jhc2hfcG9zaXgoKWAgY3VhIGJvIHRl'
'c3QgS0hPTkcgdGhheSBiYXNoIFBPU0lYIChgd2hpY2hgOiB7X2NjWydiYXNoJ119OyBTeXN0ZW0zMiA9IFdTTCBiaSBsb2Fp'
'KToiCiAgICAgICAgICAgICAgICAgICAgICAgIiBjYWkgR2l0IGZvciBXaW5kb3dzIHZhbyBDOlxcUHJvZ3JhbSBGaWxlc1xc'
'R2l0LCBob2FjIGRhdCB0aHUgbXVjIEdpdFxcYmluIGxlbiBEQVUgUEFUSCAodHJ1b2MgU3lzdGVtMzIpIikKICAgICAgICBl'
'bGlmIF9icCAhPSAiPyIgYW5kIG5vdCAoX2JnX20gYW5kIF9idF9tKToKICAgICAgICAgICAgX2RvbmdfYmcgPSBbeFs6OTBd'
'IGZvciB4IGluIHJlLmZpbmRhbGwociIoP20pXihCQVNIX0dJVCg/Ol9UMTUyKT89LiopJCIsIF9yYV9icCldIG9yIFsiKGto'
'b25nIGNvIGRvbmcgQkFTSF9HSVQpIl0KICAgICAgICAgICAgbG9pLmFwcGVuZChmImBnaXQgLS12ZXJzaW9uYCBUUk9ORyBi'
'YXNoIGN1YSBibyB0ZXN0ICh7X2JwfSkga2hvbmcgY2hheS9raG9uZyBkb2MgZHVvYyBwaGllbiBiYW46IHsnIHwgJy5qb2lu'
'KF9kb25nX2JnKX0iKQogICAgICAgIGVsaWYgX2JwICE9ICI/IiBhbmQgdHVwbGUoaW50KHgpIGZvciB4IGluIF9idF9tLmdy'
'b3VwcygpKSA8IEdJVF9TQU5fQkFTSDoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImdpdCB7Jy4nLmpvaW4oX2J0X20uZ3Jv'
'dXBzKCkpfSBUUk9ORyBiYXNoIGN1YSBibyB0ZXN0ICh7X2JwfTsgbW9pIHRydW9uZyB0MTUyOiBjaGkgUEFUSCwga2hvbmcg'
'QkFTSF9FTlYpIGN1IgogICAgICAgICAgICAgICAgICAgICAgIGYiIGhvbiB7Jy4nLmpvaW4obWFwKHN0ciwgR0lUX1NBTl9C'
'QVNIKSl9ICh0MTUyIGR1bmcgR0lUX0NPTkZJR19DT1VOVCk6IGNhcCBuaGF0IGJhbiBHaXQgY2h1YSBiYXNoIGF5IikKCnJj'
'LCBoZWFkLCBfID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxvaS5hcHBlbmQoImtob25nIGRvYyBk'
'dW9jIEhFQUQiKQpnaGkoImhlYWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAiLS1pcy1h'
'bmNlc3RvciIsIFNIQV9HMSwgaGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNfYSA9PSAwKQppZiBoZWFkID09IFNI'
'QV9HMToKICAgIHRoZV9oZSA9ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gREFZIExBIGcxLiBDSFVBIGNv'
'IGJhbiB2YSBnMjsga2V0IHF1YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9kdWU6CiAgICB0aGVfaGUgPSAiZzIi'
'OyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hBX0cxWzo4XX0pOyB1bmcgdmllbiBn'
'MiBoYXkga2hvbmc6IE43JyAobXVjIDEpIGRpbmggZGFuaC4iKQplbHNlOgogICAgdGhlX2hlID0gIj8iOyBsb2kuYXBwZW5k'
'KGYiSEVBRD17aGVhZFs6OF19IEtIT05HIHBoYWkgZzEgdmEgS0hPTkcgcGhhaSBoYXUgZHVlIGN1YSB7U0hBX0cxWzo4XX0g'
'4oCUIHJlYmFzZT8gbmhhbSBuaGFuaD8iKQpnaGkoInRoZV9oZSIsIHRoZV9oZSkKcmNfciwgcmVmcywgXyA9IGdpdChnb2Ms'
'ICJmb3ItZWFjaC1yZWYiLCAiLS1wb2ludHMtYXQiLCBoZWFkIG9yICJIRUFEIiwKICAgICAgICAgICAgICAgICAgICAiLS1m'
'b3JtYXQ9JShyZWZuYW1lOnNob3J0KSIpCmRzciA9IFt4IGZvciB4IGluIHJlZnMuc3BsaXRsaW5lcygpIGlmIHguc3RyaXAo'
'KSBhbmQgeC5zdHJpcCgpICE9ICJkby10YW0iXQpnaGkoInJlZl90cm9fdG9pX2hlYWQiLCBkc3IpCmlubihmIiAgcmVmIHRy'
'byB0b2kgSEVBRDogeycsICcuam9pbihkc3IpIGlmIGRzciBlbHNlICcoa2hvbmcgcmVmIG5hbyAtIEhFQUQgcm9pIHR1IGRv'
'KSd9IikKIyBDYXkgZHVvYyBkbyBQSEFJIGxhIGNheSBjdWEgSEVBRC4gQm8gdGVzdCwgcHJvYmUgKG11YyAzKSwgYmFuIHNh'
'byBONyB2YSBkb3QgYmllbiBOOC1OMTIgZG9jIFRFUCB0cmVuIGRpYSwgY29uIE43JyBkZW0gdHJlbiBDT01NSVQKIyBIRUFE'
'LCBtYSBsb2cgdHUga2hhaSBgSEVBRD08c2hhPmA6IGNheSBjbyB0ZXAgdHJhY2tlZCBiaSBzdWEgaGF5IHRlcCBjaHVhIHRo'
'ZW8gZG9pIHRoaSBjYWMgY29uIHNvIGR1b2kgZG8gbWFuZyBzaGEgY3VhIG1vdCB0aHUgS0hBQwojIGNheSBkYW5nIGRvLiBE'
'byB0cmVuIDIwMjYtMTAtMTAsIDBlYTk1ZGU6IHN1YSBtb3QgZG9uZyBvcHMvbGVhc2VfcHVibGlzaC5weSAoY2h1YSBjb21t'
'aXQpID0+IGAtLWNoaS1wcm9iZWAgcmM9MSBgVFJVT1QgTjhgIGR1b2kKIyAiSEVBRD0wZWE5NWRlYiIsIHRyb25nIGtoaSBO'
'NycgdmFuIGBEQVQgMiB0ZXAgLyArMzk3YCAoaGFpIG51YSBjdWEgbW90IGtldCBsdWFuIGRvIGhhaSB0aHUga2hhYyBuaGF1'
'KS4gYHJlc2V0IC0taGFyZGAgY3VhIHBzMSBjaGkKIyBkb24gdGVwIFRSQUNLRUQsIGtob25nIGRvbiB0ZXAgY2h1YSB0aGVv'
'IGRvaSwgbWEgYm8gdGVzdCBkdXlldCBvcHMvbGVhc2VzIHZhIG9wcy9yZXZpZXdzLiAtLWNoaS1raWNoLXRodW9jIGNoaSBk'
'ZW0gQ09NTUlUIChraG9uZyBkb2MKIyB0ZXApIG5lbiBraG9uZyBkb2kgY2F5IHNhY2guIGAtYyBjb3JlLmV4Y2x1ZGVzRmls'
'ZT1gOiBpZ25vcmUgQ0EgTkhBTiBjdWEgbmd1b2kgZG8gKH4vLmNvbmZpZy9naXQvaWdub3JlIGAqLnlhbWxgKSBjaGUgdGVw'
'IGNodWEKIyB0aGVvIGRvaSBraG9pIGBnaXQgc3RhdHVzYCB0aHVvbmcgKGRvOiAwIG11YywgY28gLWM6IDEpIG1hIGJvIHRl'
'c3QgdmFuIGR1eWV0IG9wcy9sZWFzZXMvKi55YW1sOyAuZ2l0aWdub3JlIFRST05HIGNheSB0aHVvYyBjb21taXQuCmRlZiBf'
'dHJhbmdfdGhhaV9jYXkoZ29jKToKICAgICMgYGdpdCBzdGF0dXNgIE1VIHZvaSBDSEkgTVVDOiB0ZXAgdHJhY2tlZCBkYSBz'
'dWEgKyBgLS1za2lwLXdvcmt0cmVlYCAodGhlIGBTYCBjdWEgYGxzLWZpbGVzIC12YCkgaG9hYyBgLS1hc3N1bWUtdW5jaGFu'
'Z2VkYAogICAgIyAodGhlIGNodSB0aHVvbmcpID0+IHN0YXR1cyBST05HIG1hIGJvIHRlc3QvcHJvYmUgdmFuIGRvYyB0ZXAg'
'ZGEgc3VhLiBEbyB0cmVuIDIwMjYtMTAtMTAsIDBlYTk1ZGU6IGNvbW1pdCBETyAoTjggaG9uZykgKwogICAgIyBraG9pIHBo'
'dWMgdGVwIHRvdCBjaHVhIGNvbW1pdCArIG1vaSBjbyBheSA9PiBgLS1jaGktcHJvYmVgIHJjPTAgYERBVCA3IHwgVFJVT1Qg'
'MGAgZHVvaSBIRUFEIGN1YSBjb21taXQgRE8gKGNheSBzYWNoOgogICAgIyByYz0xIGBUUlVPVCBOOGA7IGtob25nIGNvOiBy'
'Yz0zKS4gYGxzLWZpbGVzIC12YCBnYW4gdGhlIGBIYCBjaG8gdGVwIGJpbmggdGh1b25nOiBtb2kgdGhlIGtoYWMgPT4gY2F5'
'IEtIQUMgY29tbWl0LiBHb3AKICAgICMgdmFvIE1PVCBjaHVvaSBkZSBjaG90IERBVSB2YSBjaG90IENVT0kgc28gY3VuZyBt'
'b3QgdGh1LiBHbyBjbyBiYW5nIEhBSSBsZW5oIHJpZW5nIChgLS1uby1hc3N1bWUtdW5jaGFuZ2VkIC0tIDx0ZXA+YCByb2kK'
'ICAgICMgYC0tbm8tc2tpcC13b3JrdHJlZSAtLSA8dGVwPmApOiBnb3AgdmFvIG1vdCBsZW5oIHRoaSBnaXQgMi40MyBLSE9O'
'RyBnbyBkdW9jIHNraXAtd29ya3RyZWUuIEdpb2kgaGFuIGRhIGJpZXQgKGRvIGN1bmcgbmdheSk6CiAgICAjIGAuZ2l0L2lu'
'Zm8vZXhjbHVkZWAgdmEgYC5naXRpZ25vcmVgIENIVUEgVEhFTyBET0kgY2h1YSBgKmAgdmFuIGNoZSB0ZXAgY2h1YSB0aGVv'
'IGRvaSBraG9pIGBzdGF0dXNgLgogICAgcmMsIHN0LCBlciA9IGdpdChnb2MsICItYyIsICJjb3JlLmV4Y2x1ZGVzRmlsZT0i'
'LCAic3RhdHVzIiwgIi0tcG9yY2VsYWluIiwgIi0tdW50cmFja2VkLWZpbGVzPWFsbCIpCiAgICByYzIsIGx2LCBlcjIgPSBn'
'aXQoZ29jLCAibHMtZmlsZXMiLCAiLXYiKQogICAgY28gPSBbImNoaS1tdWM6IiArIHggZm9yIHggaW4gbHYuc3BsaXRsaW5l'
'cygpIGlmIHggYW5kIHhbMF0gIT0gIkgiXQogICAgcmV0dXJuIChyYyBvciByYzIpLCAiXG4iLmpvaW4oeCBmb3IgeCBpbiBb'
'c3RdICsgY28gaWYgeCksIChlciBvciBlcjIpCgpDQVlfU0FDSCA9ICItLWNoaS1raWNoLXRodW9jIiBub3QgaW4gc3lzLmFy'
'Z3YKaWYgQ0FZX1NBQ0g6CiAgICByY19zdCwgc3QwLCBlcl9zdCA9IF90cmFuZ190aGFpX2NheShnb2MpCiAgICBnaGkoImNh'
'eV9zYWNoX2x1Y19kYXUiLCAobm90IHJjX3N0KSBhbmQgbm90IHN0MC5zdHJpcCgpKQogICAgaWYgcmNfc3Q6CiAgICAgICAg'
'bG9pLmFwcGVuZChmImtob25nIGRvYyBkdW9jIGBnaXQgc3RhdHVzYC9gbHMtZmlsZXNgIGN1YSBjYXkgZG8gKHtfYW5fdXNl'
'cmluZm8oZXJfc3QpWzo3MF19KToiCiAgICAgICAgICAgICAgICAgICAiIGtob25nIGNodW5nIG1pbmggZHVvYyBjYXkgdHJ1'
'bmcgSEVBRCIpCiAgICBlbGlmIHN0MC5zdHJpcCgpOgogICAgICAgIGxvaS5hcHBlbmQoZiJjYXkgZG8gS0hPTkcgdHJ1bmcg'
'SEVBRDoge2xlbihzdDAuc3BsaXRsaW5lcygpKX0gbXVjIGNodWEgY29tbWl0L2NodWEgdGhlbyBkb2kvY28gY2hpIG11YyAi'
'CiAgICAgICAgICAgICAgICAgICBmIih2ZCB7c3QwLnNwbGl0bGluZXMoKVswXVs6NjBdIXJ9KSAtIgogICAgICAgICAgICAg'
'ICAgICAgIiBibyB0ZXN0L3Byb2JlIGRvIFRFUCwgTjcnIGRvIENPTU1JVDsgY29tbWl0IGhvYWMgZG9uIChnaXQgc3Rhc2gg'
'LXUpIHJvaSBkbyBsYWk7IgogICAgICAgICAgICAgICAgICAgIiBjaGkgbXVjOiBnaXQgdXBkYXRlLWluZGV4IC0tbm8tYXNz'
'dW1lLXVuY2hhbmdlZCAtLSA8dGVwPiByb2kgLS1uby1za2lwLXdvcmt0cmVlIC0tIDx0ZXA+IikKICAgIGVsc2U6CiAgICAg'
'ICAgaW5uKCIgIGNheSBsYW0gdmllYyA6IFNBQ0ggKD09IEhFQUQpIikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigiS0hP'
'TkcgRE8gRFVPQzogbmVuIGRvIHNhaSwgS0hPTkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlubigi'
'ICAtIiwgeCkKICAgIHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMS4ga2ljaCB0aHVvYyAoTjcnIGN1YSBzcGVj'
'IHIzKSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMS4gS0lDSCBUSFVPQyDigJQgdHJh'
'biBzcGVjIHIzOiA8PSAyIHRlcCB2YSA8PSA0MDAgZG9uZyB0aGVtIikKIyBWRSBORU4gUEhBSSBUVU9JIOKAlCB2YSBwaGFp'
'IENIVU5HIE1JTkggZHVvYyBsYSB0dW9pLCBraG9uZyBwaGFpIGdpYSBkaW5oLgojIEJhaSBob2MgdHJhIGdpYSAxOS0wOS0y'
'MDI2OiBjbG9uZSB0YWkgZHVuZyBjaGkgZmV0Y2ggbmhhbmggYmFuIHZhLCBgb3JpZ2luL21hc3RlcmAKIyBkdW5nIHllbiB0'
'dSAxNC0wOSAoYzE2YmQzMiwgc2F1IDk3IGNvbW1pdCkuIG1lcmdlLWJhc2Ugcm9pIHZlIGR1bmcgZGluaCBtYXN0ZXIgY3Us'
'CiMgbmVuIGRpZmYgTlVPVCBjYSA5NyBjb21taXQgbWFzdGVyOiBkbyByYSA0NiB0ZXAgLyArNzExOCB0aGF5IHZpIDIgdGVw'
'IC8gKzM5NyDigJQKIyBDVU5HIE1PVCBDT01NSVQgMGVhOTVkZS4gTW90IHRpZXUgY2hpIERFTFRBIG1hIHZlIG5lbiBraG9u'
'ZyB0dW9pIHRoaSBraG9uZyBzYWkKIyBsZWNoIG1vdCBjaHV0LCBubyBzYWkgY2EgbW90IGJhYyBkbyBsb24uCiMgQ2hvIG5l'
'bjogbmVuIGtob25nIGNodW5nIG1pbmggZHVvYyBsYSB0dW9pID0+IEtIT05HIERPIERVT0MgKHJjPTMpLCBLSE9ORyBwaGFp'
'IFRSVU9ULgojIFRSVU9UIGxhIG1vdCBQSEFOIFFVWUVUIHZlIGJhbiB2YTsgcGhhbiBxdXlldCBjaGkgZHVvYyBwaGVwIHBo'
'YXQgcmEga2hpIGRhIGRvIGR1b2MuCmVyID0gIiIKcmNfdSwgdXJsX3RobywgXyA9IGdpdChnb2MsICJyZW1vdGUiLCAiZ2V0'
'LXVybCIsICJvcmlnaW4iKQp1cmxfbywgdXJsX2luID0gX3VybF9zYWNoKHVybF90aG8pLCBfdXJsX2luKHVybF90aG8pCmdo'
'aSgib3JpZ2luX3VybCIsIHVybF9pbik7IGlubihmIiAgb3JpZ2luICAgICAgIDoge3VybF9pbiBvciAnKGtob25nIGRvYyBk'
'dW9jKSd9IikKdXJsX29rID0gKG5vdCByY191KSBhbmQgdXJsX28ucnN0cmlwKCIvIikgaW4gVVJMX0tIT19IT1BfTEUKcmNf'
'bHIsIG91dF9sciwgZXJfbHIgPSBnaXQoZ29jLCAibHMtcmVtb3RlIiwgIm9yaWdpbiIsICJyZWZzL2hlYWRzL21hc3RlciIp'
'IGlmIHVybF9vayBlbHNlICgxLCAiIiwgIiIpCmVyX2xyID0gX2FuX3VzZXJpbmZvKGVyX2xyKQpyY19sbSwgbG0sIGVyX2xt'
'ICAgICA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAib3JpZ2luL21hc3RlciIpCnJtID0gb3V0X2xyLnNwbGl0KClbMF0gaWYg'
'KG5vdCByY19sciBhbmQgb3V0X2xyLnN0cmlwKCkpIGVsc2UgIiIKaWYgbm90IHVybF9vazoKICAgIGtldCgiTjcnIGtpY2gg'
'dGh1b2MiLCBLREQsIGYib3JpZ2luPXt1cmxfaW4hcn0gS0hPTkcgcGhhaSBraG8gdGhhdCDigJQgJ3R1b2knIHNvIHZvaSBu'
'byBraG9uZyBjaHVuZyBtaW5oIGR1b2MgZ2kiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBu'
'b3Qgcm06CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAogICAgICAgIGYia2hvbmcgaG9pIGR1b2MgbWFzdGVyIHRy'
'ZW4gcmVtb3RlIChscy1yZW1vdGUgcmM9e3JjX2xyfSk6IHtlcl9scls6NjBdfSAiCiAgICAgICAgZiLigJQga2hvbmcgY2h1'
'bmcgbWluaCBkdW9jIHZlIG5lbiBjb24gdHVvaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlm'
'IHJjX2xtIG9yIG5vdCBsbToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgZG9jIGR1b2Mgb3JpZ2lu'
'L21hc3RlciB0cm9uZyBjbG9uZToge2VyX2xtWzo2MF19IikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAx'
'CmVsaWYgbG0gIT0gcm06CiAgICAjIERlbSB4ZW0gdHV0IGxhaSBiYW8geGEsIG5ldSBkZW0gZHVvYyDigJQgY29uIHNvIG5h'
'eSBub2kgcm8gbXVjIGRvIHNhaSBsZWNoLgogICAgcmNfYywgc2F1LCBfID0gZ2l0KGdvYywgInJldi1saXN0IiwgIi0tY291'
'bnQiLCBmIntsbX0uLntybX0iKQogICAgeGEgPSBmIiwgdHV0IGxhaSB7c2F1fSBjb21taXQiIGlmIChub3QgcmNfYyBhbmQg'
'c2F1LnN0cmlwKCkuaXNkaWdpdCgpKSBlbHNlICIiCiAgICBpbm4oZiIgIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmUgOiB7'
'bG1bOjEyXX0iKQogICAgaW5uKGYiICBtYXN0ZXIgdHJlbiByZW1vdGUgICAgICAgIDoge3JtWzoxMl19e3hhfSIpCiAgICBn'
'aGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICBrZXQoIk43JyBraWNoIHRodW9j'
'IiwgS0RELAogICAgICAgIGYidmUgbmVuIENVOiBvcmlnaW4vbWFzdGVyPXtsbVs6MTJdfSAhPSByZW1vdGU9e3JtWzoxMl19'
'e3hhfSAiCiAgICAgICAgZiLigJQgY2hheSBgZ2l0IC1DIDxraG8+IGZldGNoIG9yaWdpbiBtYXN0ZXJgIHJvaSBkbyBsYWki'
'KQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxzZToKICAgIGlubihmIiAgdmUgbmVuIFRVT0k6IG9y'
'aWdpbi9tYXN0ZXIgPSB7bG1bOjEyXX0gPT0gbWFzdGVyIHRyZW4gcmVtb3RlIikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwg'
'bG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIHJjX21iLCBtYiwgZXJfbWIgPSBnaXQoZ29jLCAibWVyZ2UtYmFz'
'ZSIsICJvcmlnaW4vbWFzdGVyIiwgaGVhZCkKaWYgcmNfbWIgb3Igbm90IG1iOgogICAgaWYgbWIgPT0gIiIgYW5kIHJtIGFu'
'ZCBsbSA9PSBybToKICAgICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25nIHRpbmggZHVvYyBtZXJnZS1i'
'YXNlIHZvaSBvcmlnaW4vbWFzdGVyOiB7ZXJfbWJbOjcwXX0iKQogICAgbnMsIHJjID0gIiIsIDEKZWxzZToKICAgIGdoaSgi'
'bWVyZ2VfYmFzZSIsIG1iKQogICAgaW5uKGYiICBtZXJnZS1iYXNlKG9yaWdpbi9tYXN0ZXIsIEhFQUQpID0ge21iWzoxMl19'
'IikKICAgIGlmIG1iICE9IFNIQV9CQVNFX1NQRUM6CiAgICAgICAgaW5uKGYiICBMVVUgWToga2hhYyBiYXNlIG1hIHNwZWMg'
'cjMga2hhaSAoe1NIQV9CQVNFX1NQRUNbOjEyXX0pIOKAlCB2aSBuaGFuaCBkYSBtZXJnZSBtYXN0ZXIuIikKICAgICAgICBp'
'bm4oIiAgICAgICAgIERvIHNvIGJhc2UgY3Ugc2UgTlVPVCBwaGFuIG1hc3RlciBtYW5nIHZhby4gRHVuZyBtZXJnZS1iYXNl'
'IG1vaSBsYSB2aWVjIGN1YSBleGVjdXRvci4iKQogICAgICAgIHJjX3gsIG5zX3gsIF8gPSBnaXQoZ29jLCAiZGlmZi10cmVl'
'IiwgIi1yIiwgIi1NIiwgIi0tZGlmZi1hbGdvcml0aG09bXllcnMiLCAiLS1udW1zdGF0IiwgU0hBX0JBU0VfU1BFQywgaGVh'
'ZCkKICAgICAgICBpZiBub3QgcmNfeDoKICAgICAgICAgICAgaCA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zX3guc3Bs'
'aXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgICAgICAgICAgYSA9IHN1bShpbnQoeFswXSkgZm9yIHggaW4gaCBpZiB4WzBd'
'LmlzZGlnaXQoKSkKICAgICAgICAgICAgZ2hpKCJudW1zdGF0X3RoZW9fYmFzZV9zcGVjIiwgeyJ0ZXAiOiBsZW4oaCksICJ0'
'aGVtIjogYX0pCiAgICAgICAgICAgIGlubihmIiAgICAgICAgIChkb2kgY2hpZXU6IHNvIGJhc2Ugc3BlYyA9IHtsZW4oaCl9'
'IHRlcCAvICt7YX0g4oCUIGNvbiBzbyBheSBLSE9ORyBkdW5nIGRlIGNoYW0pIikKICAgICMgUExVTUJJTkcsIGtob25nIFBP'
'UkNFTEFJTjogYGdpdCBkaWZmYCBkb2MgY2F1IGhpbmggVUkgQ1VBIE5HVU9JIERPIChkaWZmLmFsZ29yaXRobSwgZGlmZi5y'
'ZW5hbWVzLCBkaWZmLm9yZGVyRmlsZSwKICAgICMgY29sb3IuZGlmZiksIHZhIGdpYSB0cmkgSE9QIExFIGRvaSBsdW9uIFNP'
'IGRvbmcgbWEgdmFuIHJhIGNodSBzbyDigJQgZG8gdHJlbiAyMDI2LTA5LTMwaTogdW5nIHZpZW4gdG9uZyBob3AgKG15ZXJz'
'ICs0MDEpID0+CiAgICAjIGJhbiAzMGkgREFUIDIgdGVwIC8gKzQwMCBkdW9pIGBkaWZmLmFsZ29yaXRobSA9IGhpc3RvZ3Jh'
'bWAgaG9hYyBgcGF0aWVuY2VgLCBUUlVPVCArNDAxIGtoaSBtYWMgZGluaDsgMTAvNzUgY29tbWl0IGNoYW0KICAgICMgd3Jp'
'dGUgc2V0IGNvIHNvIGRvbmcgZG9pIHRoZW8gdGh1YXQgdG9hbi4gYGRpZmYtdHJlZSAtciAtTWAgPSBtYWMgZGluaCBjdWEg'
'YGdpdCBkaWZmYCAocmVuYW1lcyBiYXQpIHZhIEtIT05HIGRvYyBjYWMga2hvYQogICAgIyBheS4gVGh1YXQgdG9hbiBwaGFp'
'IFRVT05HIE1JTkg6IGRpZmYuPGRyaXZlcj4uYWxnb3JpdGhtIChxdWEgY29yZS5hdHRyaWJ1dGVzRmlsZSBjdWEgbmd1b2kg'
'ZG8pIFZBTiBsb3QgdmFvIHBsdW1iaW5nIOKAlAogICAgIyBkbyB0cmVuIDIwMjYtMDktMzBpLCBgKi5weSBkaWZmPWFsZ2Ag'
'KyBkaWZmLmFsZy5hbGdvcml0aG09aGlzdG9ncmFtOiBkaWZmLXRyZWUgKzQwMSBjaG8gdW5nIHZpZW4gbXllcnMgKzQwMDsg'
'Y28gdHVvbmcgbWluaAogICAgIyB0aGFuZyBraG9hIGF5LiBhdHRyaWJ1dGVzIGAtZGlmZmAvY29yZS5iaWdGaWxlVGhyZXNo'
'b2xkIHZhbiBhcCA9PiBgLWAgPT4gS0hPTkcgRE8gRFVPQyAoY2hvdCBkdW9pKS4KICAgIHJjLCBucywgZXIgPSBnaXQoZ29j'
'LCAiZGlmZi10cmVlIiwgIi1yIiwgIi1NIiwgIi0tZGlmZi1hbGdvcml0aG09bXllcnMiLCAiLS1udW1zdGF0IiwgbWIsIGhl'
'YWQpCmlmIHJjOgogICAgcGFzcwplbHNlOgogICAgaGFuZyA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGlu'
'ZXMoKSBpZiBsLnN0cmlwKCldCiAgICB0aGVtID0gc3VtKGludChoWzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdp'
'dCgpKQogICAgeG9hICA9IHN1bShpbnQoaFsxXSkgZm9yIGggaW4gaGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgi'
'c29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hpKCJkb25nX3RoZW0iLCB0aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZv'
'ciBoIGluIGhhbmc6IGlubihmIiAgICB7aFsyXTozNH0gK3toWzBdOjw1fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05H'
'OiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17eG9hfSAgICh0cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9'
'IGRvbmcgdGhlbSkiKQogICAgY2hhbSA9IHNvcnRlZCh7aFsyXSBmb3IgaCBpbiBoYW5nfSAmIFdSSVRFX1NFVF9HMik7IGdo'
'aSgiY2hhbV93cml0ZV9zZXQiLCBjaGFtKQogICAgZGVmIF9jYV9tb2lfY28ocmV2KToKICAgICAgICAjIGNhdC1maWxlLCBr'
'aG9uZyBgc2hvd2A6IGBnaXQgc2hvd2AgY2hldCB2b2kgY2F1IGhpbmggVUkgZ28gc2FpIChkbyB0cmVuIDIwMjYtMDktMzBp'
'OiBsb2cuZGF0ZSBnbyBzYWkgPT4gYmFuIDMwaSBnb2kKICAgICAgICAjIDBlYTk1ZGUgbGEgImtob25nIHBoYWkgdW5nIHZp'
'ZW4gLi4uIE5vbmUg4oCUIGRhIGxhbmQ/IG5oYW0gbmhhbmg/IikuCiAgICAgICAgcl8sIG5kXywgXyA9IGdpdChnb2MsICJj'
'YXQtZmlsZSIsICItcCIsIGYie3Jldn06b3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcmV0dXJuIE5vbmUg'
'aWYgcl8gZWxzZSB7dCBmb3IgdCBpbiBDQV9NT0lfRzIgaWYgcmUuc2VhcmNoKHIiKD9tKV5kZWYgIiArIHQgKyByIlthLXpd'
'P18iLCBuZF8pfQogICAgb19tYiwgb19oID0gX2NhX21vaV9jbyhtYiksIF9jYV9tb2lfY28oaGVhZCkKICAgIG1hbmcgPSBz'
'b3J0ZWQob19oIC0gb19tYiwga2V5PXNvX2NhKSBpZiAob19tYiBpcyBub3QgTm9uZSBhbmQgb19oIGlzIG5vdCBOb25lKSBl'
'bHNlIE5vbmUKICAgIGdoaSgiY2FfbW9pX2cyX21hbmdfdmFvIiwgbWFuZykKICAgIGlmIG5vdCBtYW5nOgogICAgICAgICMg'
'RG8gUk9ORyAoZGEgbGFuZCwgY2hpbmggbWFzdGVyKSwgbmhhbSBuaGFuaCwgaGF5IG5oYW5oIGN1YSBwYWNrZXQgS0hBQyBj'
'aGFtIGN1bmcgdGVwOgogICAgICAgICMga2hvbmcgbWFuZyBjYSBtb2kgbmFvIGN1YSBnMiB0aGkga2hvbmcgcGhhaSB1bmcg'
'dmllbi4gRG9jIGtob25nIGR1b2MgKE5vbmUpIGN1bmcgdmF5LgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQs'
'IGYiZG9pIHR1b25nIGtob25nIHBoYWkgdW5nIHZpZW46IHtsZW4oaGFuZyl9IHRlcCwgY2hhbSB7Y2hhbX0sIGNhIG1vaSAi'
'CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJnMiBtYW5nIHZhbyB7bWFuZyFyfSDigJQgZGEgbGFuZD8g'
'bmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/IikKICAgIGVsc2U6CiAgICAgICAgIyBudW1zdGF0IGluIGAtYCAoa2hvbmcgY28g'
'c28gZG9uZykgY2hvIHRlcCBiaW5hcnkvLWRpZmYgdGhlbyBhdHRyaWJ1dGVzIOKAlCBrZSBjYSBhdHRyaWJ1dGVzIENVQSBO'
'R1VPSSBETyAoZG8gdHJlbgogICAgICAgICMgMjAyNi0wOS0zMGc6IGNvcmUuYXR0cmlidXRlc0ZpbGUgYCoucHkgLWRpZmZg'
'ID0+ICIyIHRlcCAvICswIiBEQVQgY2hvIDBlYTk1ZGUsIHRoYXQgKzM5NykuIGAtYCBsYSBLSE9ORyBETyBEVU9DLAogICAg'
'ICAgICMga2hvbmcgcGhhaSAwOyBUUlVPVCB0aGVvIHNvIHRlcCAvIHNvIGRvbmcgREEgZGVtIGR1b2MgdmFuIGdpdSAocXVh'
'biBzYXQgdHJ1YyB0aWVwKS4KICAgICAgICBraG9uZ19zbyA9IFtoWzJdIGZvciBoIGluIGhhbmcgaWYgbm90IChoWzBdLmlz'
'ZGlnaXQoKSBhbmQgaFsxXS5pc2RpZ2l0KCkpXTsgZ2hpKCJ0ZXBfa2hvbmdfc29fZG9uZyIsIGtob25nX3NvKQogICAgICAg'
'IHZ1b3QgPSBsZW4oaGFuZykgPiBUUkFOX1RFUCBvciB0aGVtID4gVFJBTl9ET05HCiAgICAgICAga2V0KCJONycga2ljaCB0'
'aHVvYyIsIFRSVU9UIGlmIHZ1b3QgZWxzZSAoS0REIGlmIGtob25nX3NvIGVsc2UgREFUKSwKICAgICAgICAgICAgZiJ7bGVu'
'KGhhbmcpfSB0ZXAgLyAre3RoZW19IiArIChmIiDigJQgbnVtc3RhdCBLSE9ORyBjbyBzbyBkb25nIGNobyB7a2hvbmdfc299'
'IiBpZiBraG9uZ19zbyBlbHNlICIiKSkKCiMgQ29uZyBraWNoIHRodW9jIFBIQUkgZGUgbGFpIE1PVCBrZXQgcXVhLiBMZW5o'
'IG51bXN0YXQgaG9uZyB0aGkgbmhhbmggYGlmIHJjOiBwYXNzYCBraG9uZyBnaGkgZ2ksIHZhIHZhbmcgbWF0IG8gZGF5CiMg'
'dGhhbmggREFUIG8gYm8gZ29wOiBjYXUgaGluaCBkaWZmIENVQSBOR1VPSSBETyBob25nIChkaWZmLm9yZGVyRmlsZSB0cm8g'
'dGVwIGtob25nIGNvLCBkaWZmLmFsZ29yaXRobSBnbyBzYWkgPT4gcmM9MTI4KSBjaG8KIyAtLWNoaS1raWNoLXRodW9jIHJj'
'PTAgdm9pIDAgY2hvdCwgbHVvdCBkYXkgZHUgIkRBVCAxMSIgcmM9MCAoZG8gdHJlbiAyMDI2LTA5LTMwaCwgMGVhOTVkZSku'
'IFZhbmcgbWF0IGxhIEtIT05HIERPIERVT0MuCiMgVHUgMzBqIG51bXN0YXQgbGEgZGlmZi10cmVlIChraG9uZyBkb2MgaGFp'
'IGtob2EgYXkpOyBkdW9uZyBjb24gbGFpIGRvIGR1b2M6IGRpZmYucmVuYW1lTGltaXQgZ28gc2FpID0+IHJjPTEyOC4KaWYg'
'bm90IGFueShjWzBdID09ICJONycga2ljaCB0aHVvYyIgZm9yIGMgaW4gY2hvdCk6CiAgICBrZXQoIk43JyBraWNoIHRodW9j'
'IiwgS0RELCBmImNvbmcgS0hPTkcgcmEga2V0IHF1YSAoZ2l0IGRpZmYtdHJlZSAtLW51bXN0YXQgcmM9e3JjfSk6IHtfYW5f'
'dXNlcmluZm8oZXIpWzo3MF19IikKCiMgRGluaCBkYW5oIFRIQVQgbmFtIG8gTjcnIChjYSBtb2kgZzIgbWFuZyB2YW8pLCBL'
'SE9ORyBvICJoYXUgZHVlIGcxIjogZzEgZGEgbGFuZCBuZW4gbW9pIG5oYW5oIGRldQojIGxhIGhhdSBkdWUuIERvbmcgZGF1'
'IGtob2kgZGFuIHBoYWkgdHUga2hhaSB0aGVvIGtldCBxdWEgYXkgKGRvIGR1b2M6IG1hc3RlciA0NDYyMGU4IG1vIGtob2kg'
'YmFuZwojICJUSEUgSEUgRE8gRFVPQzogZzIiLCBKU09OICJ0aGVfaGUiOiAiZzIiLCB0cm9uZyBraGkgTjcnIGRhIGtldCBs'
'dWFuICJraG9uZyBwaGFpIHVuZyB2aWVuIikuCiMgTmhhbiBjaGkgZHVvYyBub2kgRFVORyBjYWkgZG8gZHVvYzogYFtdYCBr'
'aG9uZyB0YWNoICJkYSBsYW5kIiBraG9pICJuaGFtIG5oYW5oIi8icGFja2V0IGtoYWMiIChkbwojIGR1b2MgdHJlbiAyMDI2'
'LTA5LTMwYjogdW5nIHZpZW4gMmE2Nzk2OCBEQSBMQU5EIGJpIGdvaSAiS0hPTkcgcGhhaSB1bmcgdmllbiBnMiIpLgppZiB0'
'aGVfaGUgPT0gImcyIiBhbmQgbm90IHNvLmdldCgiY2FfbW9pX2cyX21hbmdfdmFvIik6CiAgICB0aGVfaGUgPSAoIktIT05H'
'IG1hbmcgY2EgbW9pIGcyIG5hbyAoZGEgbGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/KSIgaWYgc28uZ2V0KCJjYV9t'
'b2lfZzJfbWFuZ192YW8iKSA9PSBbXQogICAgICAgICAgICAgIGVsc2UgImcyPyAoQ0hVQSBkaW5oIGRhbmggZHVvYyBkb2kg'
'dHVvbmcpIikKICAgIGdoaSgidGhlX2hlIiwgdGhlX2hlKQoKIyBDb25nIG5oYW5oOiBkbyBSSUVORyBraWNoIHRodW9jICh2'
'YWkgZ2lheSkgcm9pIGR1bmcuIER1bmcga2hpIGNhbiB4YWMgbWluaCBsYWkKIyB2ZSBuZW4gbWEga2hvbmcgbXVvbiB0cmEg'
'MjAtNDUgcGh1dCBjaG8gY2EgYm8gdGVzdC4KaWYgIi0tY2hpLWtpY2gtdGh1b2MiIGluIHN5cy5hcmd2OgogICAgaW5uKCIi'
'KTsgaW5uKCI9IiAqIDc4KQogICAgaW5uKCItLWNoaS1raWNoLXRodW9jOiBDSEkgZG8gY29uZyBraWNoIHRodW9jLiBEYXkg'
'S0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCiAgICBpbm4oIi0iICogNzgpCiAgICBmb3IgX3QsIF90dCwgX2N0'
'IGluIGNob3Q6IGlubihmIiAge190dDoxNH0ge190fSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgX2sg'
'PSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQogICAgX3IgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBj'
'aG90IGlmIHQgPT0gVFJVT1QpCiAgICBzeXMuZXhpdCgzIGlmIF9rIGVsc2UgKDEgaWYgX3IgZWxzZSAwKSkKCkNISV9QUk9C'
'RSA9ICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YgICAgIyBibyBxdWEgYm8gdGVzdCArIE43OyBnaXUgMCwgMSwgMwojIC0t'
'LS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVzdCBkYXkgZHUgLS0tLS0tLS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAg'
'aW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIyLiBCTyBURVNUIERBWSBEVSAoMTAtNDAgcGh1dCkiKQogICAgcmNfbiwg'
'b3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBnb2MpCiAgICBnaGkoInJjX3N1aXRlIiwgcmNf'
'bikKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXRfbikKICAgIGlubigiICByYyA9IiwgcmNfbiwgInwiLCBtLmdyb3VwKDAp'
'IGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQpIikKICAgIGlmIG06CiAgICAgICAgZ2hpKCJkYXQi'
'LCBpbnQobS5ncm91cCgxKSkpOyBnaGkoInRyZW4iLCBpbnQobS5ncm91cCgyKSkpOyBnaGkoImJvX3F1YV9zbyIsIGludCht'
'Lmdyb3VwKDQpKSkKICAgIGRvX2hldCwgZ2MsIHRpbiA9IGRvY19kbyhvdXRfbikKICAgIGdoaSgic29fY2FfZG8iLCBsZW4o'
'ZG9faGV0KSk7IGdoaSgibGlldF9rZV9kYXlfZHUiLCB0aW4pCiAgICBmb3IgZyBpbiBnYzogaW5uKCIgICAqIiwgZykKICAg'
'IGlubigiIik7IGlubihmIiAgPT09IHtsZW4oZG9faGV0KX0gQ0EgRE8gPT09IikKICAgIGZvciB0IGluIHNvcnRlZChkb19o'
'ZXQsIGtleT1zb19jYSk6CiAgICAgICAgaW5uKGYiICAge3Quc3BsaXQoJ18nKVswXTo3fSB7dH0iKTsgaW5uKGYiICAgICAg'
'ICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCiAgICBnaGkoImRvX2x5X2RvIiwge3Q6IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBp'
'biBkb19oZXR9KQogICAgIyAtLS0tIENIT1Q6IG1vaSBjYSBETyBwaGFpIEdJQUkgVEhJQ0ggRFVPQyAtLS0tCiAgICAjIFRo'
'aWV1IGNob3QgbmF5LCBibyBkbyBpbiBkYW5oIHNhY2ggZG8gcm9pIHZhbiB0aG9hdCByYz0wLiBEbyBkdW5nIGxhIGxvaSBk'
'YSB4YXkgcmE6CiAgICAjIGx1b3QgV2luZG93cyAxOS0wOSBjbyB0MTcxIERPIG1hIGJvIGRvIGJhbyAiREFUIDEwIHwgVFJV'
'T1QgMCIgdmEgcmM9MC4KICAgIGRlZiBfa2hvYSh0KTogcmV0dXJuIHQuc3BsaXQoIl8iKVswXQogICAgZG9fcGFja2V0LCBk'
'b19sYSwgZG9fdGhpZXVfY29uZ19jdSA9IFtdLCBbXSwgW10KICAgIGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19j'
'YSk6CiAgICAgICAgaywgbHkgPSBfa2hvYSh0KSwgZG9faGV0W3RdCiAgICAgICAgaWYgayBpbiBDQV9QQUNLRVQ6ICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgZG9fcGFja2V0LmFwcGVuZCh0KQogICAgICAgIGVsaWYgIktIw5RORyDEkE8gxJDG'
'r+G7okMiIGluIGx5IG9yICJ0aGnhur91IGAiIGluIGx5OiAgZG9fdGhpZXVfY29uZ19jdS5hcHBlbmQodCkKICAgICAgICBl'
'bGlmIGsgaW4gTkdPQUlfUEhBTV9WSTogICAgICAgICAgICAgICAgICAgICAgICBwYXNzCiAgICAgICAgZWxzZTogICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fbGEuYXBwZW5kKHQpCiAgICBnaGkoImRvX3BhY2tldCIs'
'IGRvX3BhY2tldCk7IGdoaSgiZG9fbGEiLCBkb19sYSk7IGdoaSgiZG9fdGhpZXVfY29uZ19jdSIsIGRvX3RoaWV1X2Nvbmdf'
'Y3UpCiAgICBpbm4oIiIpCiAgICBpbm4oZiIgIGNhIERPIHRodW9jIENISU5IIHBhY2tldCBuYXkgOiB7W19raG9hKHgpIGZv'
'ciB4IGluIGRvX3BhY2tldF0gb3IgJ2tob25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBuZ29haSBwaGFtIHZpIChyMyBr'
'aGFpKToge1tfa2hvYSh4KSBmb3IgeCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpIGlmIF9raG9hKHgpIGluIE5HT0FJ'
'X1BIQU1fVkldfSIpCiAgICBpbm4oZiIgIGNhIERPIHZpIFRISUVVIENPTkcgQ1UgICAgICAgOiB7W19raG9hKHgpIGZvciB4'
'IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9yICdraG9uZyBjbyd9IikKICAgIGlubihmIiAgY2EgRE8gTEEgKGtob25nIGdpYWkg'
'dGhpY2ggZHVvYyk6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdIG9yICdraG9uZyBjbyd9IikKICAgICMgLS0tLSBDSE9U'
'OiBwaGVwIGRvIHBoYWkgVFJPTiB0cnVvYyBraGkgbW90IGNodSBEQVQgbmFvIGR1b2MgcGhhdCAtLS0tCiAgICAjIEJhbiB0'
'cnVvYyBjaGkgSU4gYHRpbmAvYHJjX3N1aXRlYDogYm8gdGVzdCBjaGV0IGdpdWEgdDE3MSAocmM9MTM0LCBraG9uZyBkb25n'
'IHRvbmcpCiAgICAjIHZhbiByYSAiREFUIDEyIHwgVFJVT1QgMCIgcmM9MDsgY2EgUEFDS0VUIHZhbmcgbWF0IGhheSBiaSBC'
'TyBRVUEgY3VuZyBkdW9jIGNoYW0gbmh1CiAgICAjICJraG9uZyBkbyIuIFZhbmcgbWF0IGtob25nIHBoYWkgImtob25nIGRv'
'IiDigJQgbGEgS0hPTkcgRE8gRFVPQy4KICAgIHZhbmcgPSBbdCBmb3IgdCBpbiBzb3J0ZWQoQ0FfUEFDS0VULCBrZXk9c29f'
'Y2EpIGlmIG1hdV9jYShvdXRfbiwgdCkgbm90IGluICgiUVVBIiwgIkRPIildCiAgICBseV9rZGQgPSBbXQogICAgaWYgbm90'
'IHRpbjogbHlfa2RkLmFwcGVuZCgiZGFuaCBzYWNoIGRvIEtIT05HIGRheSBkdSIpCiAgICBpZiByY19uIG5vdCBpbiAoMCwg'
'MSkgb3IgKHJjX24gPT0gMSkgIT0gYm9vbChkb19oZXQpOgogICAgICAgIGx5X2tkZC5hcHBlbmQoZiJyYyBibyB0ZXN0PXty'
'Y19ufSBraG9uZyBraG9wIHtsZW4oZG9faGV0KX0gY2EgRE8gZG9jIGR1b2MiKQogICAgaWYgdmFuZzogbHlfa2RkLmFwcGVu'
'ZChmImNhIFBBQ0tFVCB2YW5nL2JvIHF1YToge3Zhbmd9IikKICAgIGdoaSgiY2FfcGFja2V0X3ZhbmciLCB2YW5nKTsgZ2hp'
'KCJseV9kb19jaHVhX3Ryb24iLCBseV9rZGQpCiAgICBpZiBseV9rZGQ6IGtldCgiQm8gdGVzdCBjaGF5IFRST04gdmEgZG9j'
'IERVIiwgS0RELCAiOyAiLmpvaW4obHlfa2RkKSkKICAgIGNodWFfdHJvbiA9IEtERCBpZiBseV9rZGQgZWxzZSBEQVQKICAg'
'IGtldCgiS2hvbmcgY2EgbmFvIGN1YSBQQUNLRVQgYmkgRE8iLCBjaHVhX3Ryb24gaWYgbm90IGRvX3BhY2tldCBlbHNlIFRS'
'VU9ULAogICAgICAgICIiIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBmIkRPOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tl'
'dF19IOKAlCBiYW4gdmEgQ0hVQSB4b25nIikKICAgIGtldCgiTW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MiLCBjaHVh'
'X3Ryb24gaWYgbm90IGRvX2xhIGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX2xhIGVsc2UgZiJsYToge1tfa2hv'
'YSh4KSBmb3IgeCBpbiBkb19sYV19IikKICAgIGlmIGRvX3RoaWV1X2NvbmdfY3U6CiAgICAgICAga2V0KCJDb25nIGN1IGRh'
'eSBkdSBkZSBkbyIsIEtERCwgZiJ0aGlldSBjb25nIGN1IGNobyB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2Nvbmdf'
'Y3VdfSIpCgogICAgYnEgPSBzb3J0ZWQoe3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0X24pfSwga2V5PXNv'
'X2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBicSkKICAgIGlubigiIik7IGlubihmIiAgQk8gUVVBICh7bGVuKGJxKX0pOiB7W3gu'
'c3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCiAgICBpbm4oIiIpOyBpbm4oIiAgTjEtTjQgKHQxNjUtdDE2OCksIHRp'
'ZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBuYXkgbGEgY2hpIGJhbyBob2kgcXV5OiIpCiAgICBiNCA9IHt0OiBtYXVfY2Eo'
'b3V0X24sIHQpIGZvciB0IGluIENBTU9JfTsgZ2hpKCJjYV9tb2kiLCBiNCkKICAgIGZvciB0IGluIENBTU9JOiBpbm4oZiIg'
'ICAgIHt0fToge2I0W3RdfSIpCiAgICAjIEJPX1FVQS92YW5nIGxhIENIVUEgQ0hBWSwga2hvbmcgcGhhaSBETzogY2hpIG1v'
'dCBjYSBETyBtb2kgZHVvYyBwaGF0IFRSVU9ULgogICAga2V0KCJOMS1ONCAodDE2NS10MTY4KSIsIERBVCBpZiBhbGwodiA9'
'PSAiUVVBIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkKICAgICAgICBlbHNlIChUUlVPVCBpZiBhbnkodiA9PSAiRE8iIGZvciB2'
'IGluIGI0LnZhbHVlcygpKSBlbHNlIEtERCksIHN0cihiNCkpCgogICAgaW5uKCIiKTsgaW5uKCIgIDE1IGNhIHR1bmcgZG8g'
'dHJlbiBDSToiKQogICAgYjE1ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0ExNX07IGdoaSgiY2ExNSIsIGIx'
'NSkKICAgIGlubigiICAgICIgKyAiICAiLmpvaW4oZiJ7dH06e2IxNVt0XX0iIGZvciB0IGluIENBMTUpKQoKICAgICMgdDEz'
'NiDigJQgTjEyIGRvIEdJQU4gVElFUCBxdWEga2V0IHF1YSBjYQogICAgdDEzNl90ZW4gPSBuZXh0KCh0IGZvciB0IGluIGRv'
'X2hldCBpZiB0LnN0YXJ0c3dpdGgoInQxMzYiKSksIE5vbmUpCiAgICBpZiBiMTUuZ2V0KCJ0MTM2IikgPT0gIlFVQSI6CiAg'
'ICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgREFULCAidDEzNiBRVUEiKQogICAgZWxpZiBiMTUuZ2V0'
'KCJ0MTM2IikgIT0gIkRPIjoKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBLREQsIGYidDEzNiA9'
'IHtiMTUuZ2V0KCd0MTM2Jykhcn0g4oCUIGtob25nIGNoYXkva2hvbmcgdGhheSIpCiAgICBlbHNlOgogICAgICAgIGx5ID0g'
'ZG9faGV0LmdldCh0MTM2X3RlbiwgIiIpCiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgVFJVT1Qs'
'IGYiRE86IHtseVs6OTBdfSIpCgojIC0tLS0tLS0tLS0tLS0tLS0gMy4gcHJvYmUgVEhBTkcgdmFvIGhhbSAtLS0tLS0tLS0t'
'LS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMy4gUFJPQkUgVEhBTkcg4oCUIGdvaSBfZ2l0X3dpbmRvd3Mg'
'dm9pIHRoYW0gc28gdGllbSIpCnNwZWMgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHA1NDEi'
'LCBzdHIodGVwKSkKbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMpOyBzcGVjLmxvYWRlci5leGVj'
'X21vZHVsZShscCkKc2lnID0gaW5zcGVjdC5zaWduYXR1cmUobHAuX2dpdF93aW5kb3dzKQpnaGkoInRoYW1fc29fX2dpdF93'
'aW5kb3dzIiwgbGlzdChzaWcucGFyYW1ldGVycykpCmlubigiICB0aGFtIHNvIGN1YSBfZ2l0X3dpbmRvd3M6IiwgbGlzdChz'
'aWcucGFyYW1ldGVycykpCgpkZWYgZ29pKCoqa3cpOgogICAgIiIiR29pIF9naXRfd2luZG93cywgQkFUIHN0ZGVyciBkZSBt'
'b3QgZG9uZyBjaGFuIGRvYW4ga2hvbmcgZ2lldCBsdW90IGRvLiIiIgogICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgIHdpdGgg'
'Y29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgciA9IGxwLl9naXRfd2luZG93cygqKmt3KQogICAgcmV0'
'dXJuIHIsIGUuZ2V0dmFsdWUoKQoKIyAtLS0gZG9pIGNodW5nIHJpZzogcGhhaSB0cmEgbG9pIGR1bmcgbW90IGNhIHRhIEJJ'
'RVQgVFJVT0MgZGFwIGFuIC0tLQp3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICBuZ29haSA9'
'IFBhdGgodCkvIm5nb2FpIjsgbmdvYWkubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBh'
'dGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgKG5nb2FpLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1'
'dGYtOCIpCiAgICByMSwgXyA9IGdvaShwYXRoPXN0cihuZ29haSksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihj'
'dykpCiAgICAoY3cvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIyLCBfID0gZ29p'
'KHBhdGg9c3RyKGN3KSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKcmlnX29rID0gYm9vbChyMSkgYW5k'
'IHIyIGlzIE5vbmUKZ2hpKCJyaWdfZG9pX2NodW5nIiwgcmlnX29rKQprZXQoIlJJRyBkb2kgY2h1bmcgKGJpZXQgdHJ1b2Mg'
'ZGFwIGFuKSIsIERBVCBpZiByaWdfb2sgZWxzZSBLREQsCiAgICBmIm5nb2FpLWN3ZC0+eydOSEFOJyBpZiByMSBlbHNlICdO'
'b25lJ30gfCB0cm9uZy1jd2QtPnsnTkhBTicgaWYgcjIgZWxzZSAnTm9uZSd9IikKaWYgbm90IHJpZ19vazoKICAgIGlubigi'
'Iik7IGlubigiS0hPTkcgRE8gRFVPQzogcmlnIHNhaSwgbW9pIGNob3QgZHVvaSBzZSB2byBuZ2hpYS4iKTsgc3lzLmV4aXQo'
'MykKCiMgLS0tIE1PSSBDT05HIFBIQUkgVFUgQ0hVTkcgTUlOSCBOTyBDTyBUSEUgRE8gLS0tCiMgQmFpIGhvYyBkYXQgbmhh'
'dCBjdWEgcGFja2V0IG5heTogZG9fbjEwIGJhbiBjdSBjaGFtIERBVCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEKIyBj'
'dWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1bmcga2h1eWV0IHRhdCBtYSBOMTAgc2luaCByYSBkZSBiYXQuIE5vIGRlZ2Vu'
'ZXJhdGUg4oCUCiMgdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIG5lbiAidGFjaCBkdW5nIiB2YSAidGFjaCBz'
'YWkiIGNobyBjdW5nIGtldCBxdWEuCiMgTW90IGNvbmcga2hvbmcgdGhlIERPIHRoaSBraG9uZyBwaGFpIGNvbmcsIHZhIG5v'
'IG5ndXkgaGllbSBob24ga2hvbmcgY28gY29uZzogbm8KIyBwaGF0IHJhIG1vdCBjaHUgREFULgojCiMgTmVuIHRydW9jIGto'
'aSBEVU5HIG5hbSBjb25nIG5heSBkZSBwaGFuIHF1eWV0LCBiYXQgdHVuZyBjb25nIGdpZXQgbW90IGRvdCBiaWVuIGRhCiMg'
'YmlldCB0cm9uZy4gQ29uZyBuYW8ga2hvbmcgZ2lldCBkdW9jIHRoaSBjaHUgREFUIGN1YSBubyBiaSBIQSB4dW9uZyBLSE9O'
'RyBETyBEVU9DOwojIFRSVU9UIGdpdSBuZ3V5ZW4gKHF1YW4gc2F0IHRydWMgdGllcCwgdmQuIGcxIHZhbiBuaGFuIGdpdC5i'
'YXQpLiBEb3QgYmllbiBjaGF5IHRyZW4gQkFOIFNBTyBUQU07IGNheSB0aGF0IGtob25nIGJpCiMgZHVuZyB0b2kgKGN1bmcg'
'a3kgbHVhdCBuaHUgTjcpLgpET1RfQklFTl9UVV9LSUVNID0gWwogICAgKCJOOCIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIs'
'CiAgICAgJ2lmIGNoaV9kaW5oIGFuZCBQYXRoKGNoaV9kaW5oKS5uYW1lLmxvd2VyKCkgPT0gImdpdC5leGUiIGFuZCBob3Bf'
'bGUoY2hpX2RpbmgpOicsCiAgICAgImlmIGNoaV9kaW5oIGFuZCBob3BfbGUoY2hpX2RpbmgpOiIpLAogICAgKCJOOSIsICJv'
'cHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgImQgPSBkX3Jhdy5zdHJpcCgpLnN0cmlwKCdcIicpIiwgImQgPSBkX3Jhdy5z'
'dHJpcCgpIiksCiAgICAoIk4xMCIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgInNlcCA9IG9zLnBhdGhzZXAgaWYg'
'cGhhbl9jYWNoIGlzIE5vbmUgZWxzZSBwaGFuX2NhY2giLCAic2VwID0gb3MucGF0aHNlcCIpLAogICAgKCJOMTEiLCAib3Bz'
'L2xlYXNlX3B1Ymxpc2gucHkiLCAiaWYgY2hhbl9kb2FuIGlzIG5vdCBOb25lOiIsICJpZiBGYWxzZToiKSwKICAgICgiTjEy'
'IiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiLAogICAgICdnaXRfcGF0aD0iLy9raG9uZy1jby9naXQiJywgJ2dpdF9w'
'YXRoPSIva2hvbmctY28vZ2l0IicpLApdCmlubigiIik7IGlubigiICB0dSBraWVtIGNvbmcg4oCUIG1vaSBjb25nIHBoYWkg'
'Z2lldCBkdW9jIG1vdCBkb3QgYmllbiBkYSBiaWV0OiIpCmdpZXQgPSB7fQpmb3IgbWEsIGR1b25nLCB0aW0sIHRoYXkgaW4g'
'RE9UX0JJRU5fVFVfS0lFTToKICAgIF90ZW4sIF9oYW0gPSBuZXh0KCgoYSwgYikgZm9yIGEsIGIgaW4gUFJPQkUgaWYgYS5z'
'dGFydHN3aXRoKG1hICsgIiAiKSksIChOb25lLCBOb25lKSkKICAgIGlmIF9oYW0gaXMgTm9uZToKICAgICAgICBnaWV0W21h'
'XSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzoga2hvbmcgdGltIHRoYXkgcHJvYmUgdGVuICd7bWF9'
'IC4uLiciKTsgY29udGludWUKICAgIHRyeToKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFz'
'IF90OgogICAgICAgICAgICBfYyA9IFBhdGgoX3QpLyJjYXkiOyBzaHV0aWwuY29weXRyZWUoZ29jLyJvcHMiLCBfYy8ib3Bz'
'IikKICAgICAgICAgICAgX2YgPSBfYy9kdW9uZzsgX25kID0gX2YucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpCiAgICAg'
'ICAgICAgIGlmIF9uZC5jb3VudCh0aW0pICE9IDE6CiAgICAgICAgICAgICAgICBnaWV0W21hXSA9IE5vbmUKICAgICAgICAg'
'ICAgICAgIGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzogbWF1IGRvdCBiaWVuIGtob3Age19uZC5jb3VudCh0aW0p'
'fSBsYW4gKG1vbmcgMSkiCiAgICAgICAgICAgICAgICAgICAgZiIg4oCUIG1hIG5ndW9uIGRhIGRvaSwgZG90IGJpZW4gbmF5'
'IGhldCB5IG5naGlhIik7IGNvbnRpbnVlCiAgICAgICAgICAgIF9mLndyaXRlX3RleHQoX25kLnJlcGxhY2UodGltLCB0aGF5'
'LCAxKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVf'
'bG9jYXRpb24oImxwX2RiXyIgKyBtYSwgc3RyKF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICAgICAgICAgIF9t'
'ID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3ApOyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9tKQogICAg'
'ICAgICAgICBkZWYgX2dvaV9kYigqKmt3KToKICAgICAgICAgICAgICAgIF9lID0gaW8uU3RyaW5nSU8oKQogICAgICAgICAg'
'ICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihfZSk6CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIF9t'
'Ll9naXRfd2luZG93cygqKmt3KSwgX2UuZ2V0dmFsdWUoKQogICAgICAgICAgICBfdHQsIF9jdCwgXyA9IF9oYW0oX2dvaV9k'
'YiwgaW5zcGVjdC5zaWduYXR1cmUoX20uX2dpdF93aW5kb3dzKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF9j'
'LyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIGdpZXRbbWFdID0gKF90dCA9PSBUUlVPVCkKICAgICAg'
'ICBpbm4oZiIgICAge21hOjR9IGRvdCBiaWVuIC0+IHtfdHQ6MTR9IHsnR0lFVCBEVU9DJyBpZiBfdHQgPT0gVFJVT1QgZWxz'
'ZSAnU09ORyBTT1QnfSIKICAgICAgICAgICAgKyAoZiIgICAoe19jdH0pIiBpZiBfY3QgZWxzZSAiIikpCiAgICBleGNlcHQg'
'RXhjZXB0aW9uIGFzIF9lOgogICAgICAgIGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9D'
'OiB7dHlwZShfZSkuX19uYW1lX199OiB7X2V9IikKZ2hpKCJjb25nX2dpZXRfZHVvY19kb3RfYmllbiIsIGdpZXQpCgpmb3Ig'
'dGVuLCAodHQsIGN0LCBkbCkgaW4gWyh0LCBmKGdvaSwgc2lnLCB0ZXB0KSkgZm9yIHQsIGYgaW4gUFJPQkVdOgogICAgZ2hp'
'KCJwcm9iZV8iICsgdGVuLnNwbGl0KClbMF0ubG93ZXIoKSwgZGwpCiAgICBpZiBpc2luc3RhbmNlKGRsLCBkaWN0KToKICAg'
'ICAgICBmb3IgaywgdiBpbiBkbC5pdGVtcygpOiBpbm4oZiIgICAge2s6MzR9OiB7dn0iKQogICAgbWEgPSB0ZW4uc3BsaXQo'
'KVswXQogICAgaWYgZ2lldC5nZXQobWEpIGlzIG5vdCBUcnVlIGFuZCB0dCA9PSBEQVQ6CiAgICAgICAgIyBEQVQgdHUgbW90'
'IGNvbmcgY2h1YSBjaHVuZyBtaW5oIGR1b2MgbGEgYmlldCBETyB0aGkga2hvbmcgZGFuZyB0aW4gaG9uIEtERC4KICAgICAg'
'ICBrZXQodGVuLCBLREQsIGYiY29uZyBLSE9ORyBnaWV0IGR1b2MgZG90IGJpZW4gY3VhIGNoaW5oIG5vICh7Z2lldC5nZXQo'
'bWEpIXJ9KSIKICAgICAgICAgICAgICAgICAgICAgIGYiIC0+IGNodSBEQVQgbmF5IGtob25nIGNvIGdpYSB0cmkiKQogICAg'
'ZWxzZToKICAgICAgICBrZXQodGVuLCB0dCwgY3QpCgojIC0tLS0tLS0tLS0tLS0tLS0gNC4gTjcgZG90IGJpZW4gdHJlbiBC'
'QU4gU0FPIFRBTSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgp'
'OyBpbm4oIjQuIE43IOKAlCBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIChjYXkgdGhhdCBLSE9ORyBiaSBkdW5nIHRvaSki'
'KQogICAgdHJ1b2MgPSB0ZXAucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4pCiAgICBnaGkoIm43'
'X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIgIHNvIGRvbmcga2hvcCB7TUFVX1dJTiFyfTogVFJVT0MgPSB7dHJ1b2N9IFttb25n'
'IDFdIikKICAgIGlmIHRydW9jICE9IDE6CiAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCBm'
'Im1hdSB4dWF0IGhpZW4ge3RydW9jfSBsYW4sIGtob25nIHBoYWkgMSIpCiAgICBlbHNlOgogICAgICAgIHdpdGggdGVtcGZp'
'bGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdG1wOgogICAgICAgICAgICBzYW8gPSBQYXRoKHRtcCkvImNheSIKICAgICAg'
'ICAgICAgc2h1dGlsLmNvcHl0cmVlKGdvYywgc2FvLCBpZ25vcmU9c2h1dGlsLmlnbm9yZV9wYXR0ZXJucygiLmdpdCIsICJf'
'X3B5Y2FjaGVfXyIsICIqLnB5YyIpKQogICAgICAgICAgICBmMiA9IHNhby8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIKICAg'
'ICAgICAgICAgZjIud3JpdGVfdGV4dChmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikucmVwbGFjZShNQVVfV0lOLCAi'
'aWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHNhdSA9IGYyLnJlYWRfdGV4dChlbmNvZGluZz0i'
'dXRmLTgiKS5jb3VudChNQVVfV0lOKTsgZ2hpKCJuN19zYXUiLCBzYXUpCiAgICAgICAgICAgIGlubihmIiAgU0FVIChkYSBk'
'b3QgYmllbikgPSB7c2F1fSBbbW9uZyAwXSIpCiAgICAgICAgICAgIGlmIHNhdSAhPSAwOgogICAgICAgICAgICAgICAga2V0'
'KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCAiZG90IGJpZW4gS0hPTkcgYXAgZHVvYyIpCiAgICAgICAgICAg'
'IGVsc2U6CiAgICAgICAgICAgICAgICByY19tLCBvdXRfbSA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0s'
'IHNhbykKICAgICAgICAgICAgICAgIG0xNjUgPSBtYXVfY2Eob3V0X20sICJ0MTY1Iik7IGRtLCBfLCBfID0gZG9jX2RvKG91'
'dF9tKQogICAgICAgICAgICAgICAgdGVuMTY1ID0gbmV4dCgodCBmb3IgdCBpbiBkbSBpZiB0LnN0YXJ0c3dpdGgoInQxNjUi'
'KSksIE5vbmUpCiAgICAgICAgICAgICAgICBseSA9IChkbS5nZXQodGVuMTY1KSBvciAiIikKICAgICAgICAgICAgICAgIGdo'
'aSgibjdfdDE2NSIsIG0xNjUpOyBnaGkoIm43X2x5X2RvIiwgbHlbOjIwMF0pCiAgICAgICAgICAgICAgICBpbm4oZiIgIHQx'
'NjUgc2F1IGRvdCBiaWVuOiB7bTE2NX0gfCB7bHlbOjExMF19IikKICAgICAgICAgICAgICAgIGR1bmdfbHlfZG8gPSAiUEFU'
'SCB0IiBpbiBseSBvciAiL3Vzci9iaW4iIGluIGx5CiAgICAgICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdp'
'bmRvd3MiLCBEQVQgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykgZWxzZQogICAgICAgICAgICAgICAgICAgIChU'
'UlVPVCBpZiBtMTY1ID09ICJETyIgZWxzZSBLREQpLAogICAgICAgICAgICAgICAgICAgICJnaWV0IGR1bmcgbHkgZG8iIGlm'
'IChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pCiAgICAgICAgICAgICAgICAgICAgZWxzZSAoIkRPIG5odW5nIEtIT05H'
'IGR1bmcgbHkgZG8gLT4gdGluIGR1bmcgZ2lhIiBpZiBtMTY1ID09ICJETyIgZWxzZSAia2hvbmcgZG9jIGR1b2MgdDE2NSIp'
'KQoKIyAtLS0tLS0tLS0tLS0tLS0tIEtFVCBMVUFOIC0tLS0tLS0tLS0tLS0tLS0KIyBDYXkgY28gdGhlIGRvaSBUUk9ORyBM'
'VUMgZG86IGJvIHRlc3QgMjAtNDUgcGh1dCwgTjcgdGhlbSBtb3QgbHVvdCBudWEsIG1hIHBzMSBkdW5nIGNodW5nIE1PVCBj'
'bG9uZSBtYWMgZGluaCBjaG8gbW9pIGxhbiBjaGF5IChtb3QgbGFuCiMgY2hheSB0aHUgaGFpIHZvaSAtTmhhbmgga2hhYywg'
'aG9hYyBtb3QgbGFuIHN1YSB0YXksIGRvaSB0ZXAgZHVvaSBjaGFuIGx1b3QgZGFuZyBjaGF5KS4gRG8gbGFpIEhFQUQgdmEg'
'Y2F5IHNhdSBjdW5nIGRlIGxvZyBraG9uZyBnYW4KIyBzaGEgY2hvIG1vdCB0aHUgZGEgYmkgZG9pIGdpdWEgY2h1bmcuCmlm'
'IENBWV9TQUNIOgogICAgcmNfaDIsIGhlYWQyLCBfID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKICAgIHJjX3My'
'LCBzdDIsIF8gPSBfdHJhbmdfdGhhaV9jYXkoZ29jKQogICAgZG9pID0gYm9vbChyY19oMiBvciByY19zMiBvciBoZWFkMiAh'
'PSBoZWFkIG9yIHN0MiAhPSBzdDApCiAgICBnaGkoImNheV9raG9uZ19kb2lfdHJvbmdfbHVjX2RvIiwgbm90IGRvaSkKICAg'
'IGlmIGRvaToKICAgICAgICBrZXQoIkNheSBkbyBLSE9ORyBkb2kgdHJvbmcgbHVjIGRvIiwgS0RELAogICAgICAgICAgICBm'
'IkhFQUQge2hlYWRbOjhdfSAtPiB7KGhlYWQyIG9yICc/JylbOjhdfTsgbXVjIGNodWEgY29tbWl0L2NodWEgdGhlbyBkb2kg'
'IgogICAgICAgICAgICBmIntsZW4oc3QwLnNwbGl0bGluZXMoKSl9IC0+IHtsZW4oc3QyLnNwbGl0bGluZXMoKSl9IiArIChm'
'IjsgZ2l0IHJjPXtyY19oMiBvciByY19zMn0iIGlmIHJjX2gyIG9yIHJjX3MyIGVsc2UgIiIpKQppbm4oIiIpOyBpbm4oIj0i'
'ICogNzgpCmlubihmIlRIRSBIRSBETyBEVU9DOiB7dGhlX2hlfSAgIEhFQUQ9e2hlYWRbOjEyXX0iKQojIEtob2kgZGFuIGNo'
'byByZXZpZXdlciBiYXQgZGF1IG8gZG9uZyB0cmVuLCBuZW4gQ0hFIERPIHBoYWkgbmFtIE5HQVkgZHVvaSBubzoga2hvbmcg'
'Y28gZG9uZyBuYXkKIyB0aGkgbW90IGx1b3QgLS1jaGktcHJvYmUgaW4gIkRBVCA3IHwgVFJVT1QgMCB8IEtIT05HIERPIERV'
'T0MgMCIgcmM9MCBtYSBraG9uZyBub2kgbGEgY2h1YSBjaGF5IGJvIHRlc3QuCmdoaSgiY2hlX2RvIiwgImNoaS1wcm9iZSIg'
'aWYgQ0hJX1BST0JFIGVsc2UgImRheS1kdSIpCmlmIENISV9QUk9CRToKICAgIGlubigiLS1jaGktcHJvYmU6IENISSBkbyBt'
'dWMgMCwgMSwgMy4gQm8gdGVzdCwgTjEtTjQsIHQxMzYsIE43IEtIT05HIGNoYXkgLSBkYXkgS0hPTkcgcGhhaSBtb3QgbHVv'
'dCBuZ2hpZW0gdGh1LiIpCmlmIHRoZV9oZSA9PSAiZzEiOgogICAgaW5uKCJMVVUgWTogZGF5IGxhIE5FTiBETyAoZzEpLCBL'
'SE9ORyBwaGFpIG5naGllbSB0aHUgZzIuIENhYyBjaG90IE44LU4xMiBkdW9pIGRheSIpCiAgICBpbm4oIiAgICAgICBUUlVP'
'VCBsYSBEVU5HIE5IVSBNT05HIOKAlCBjaHVuZyBsYSBuaHVuZyBsbyBnMiBzaW5oIHJhIGRlIHbDoS4iKQppbm4oIi0iICog'
'NzgpCmZvciB0ZW4sIHR0LCBjdCBpbiBjaG90OgogICAgaW5uKGYiICB7dHQ6MTR9IHt0ZW59IiArIChmIiAgIHtjdH0iIGlm'
'IGN0IGVsc2UgIiIpKQpuX2tkZCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCm5fdHJ1b3QgPSBz'
'dW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCmlubigiLSIgKiA3OCkKaW5uKGYiICBEQVQge3N1bSgx'
'IGZvciBfLHQsXyBpbiBjaG90IGlmIHQ9PURBVCl9IHwgVFJVT1Qge25fdHJ1b3R9IHwgS0hPTkcgRE8gRFVPQyB7bl9rZGR9'
'IikKaW5uKGYiICBUb25nIGNhIGRvOiB7c28uZ2V0KCdzb19jYV9kbycpfSB8IGRhbmggc2FjaCBkYXkgZHU6IHsnQ08nIGlm'
'IHNvLmdldCgnbGlldF9rZV9kYXlfZHUnKSBlbHNlICdLSE9ORyBETyBEVU9DJ30iKQppbm4oZiIgIEFkbWluaXN0cmF0b3I6'
'IHtzby5nZXQoJ3F1eWVuX2FkbWluJyl9IHwgc3ltbGluazoge3NvLmdldCgnc3ltbGlua19kdW9jJyl9IikKaW5uKCIiKTsg'
'aW5uKCItLS0gREFOIE5HVVlFTiBLSE9JIEpTT04gTkFZIFZFIENITyBSRVZJRVdFUiAtLS0iKQpnaGkoImNob3QiLCBbeyJ0'
'ZW4iOiBhLCAidHJhbmdfdGhhaSI6IGIsICJjaGlfdGlldCI6IGN9IGZvciBhLCBiLCBjIGluIGNob3RdKQppbm4oanNvbi5k'
'dW1wcyhzbywgZW5zdXJlX2FzY2lpPUZhbHNlLCBpbmRlbnQ9MSwgZGVmYXVsdD1zdHIpKQojIHJjOiAwID0gbW9pIGNob3Qg'
'REFUIHwgMSA9IGNvIGNob3QgVFJVT1QgfCAzID0gY28gY2hvdCBLSE9ORyBETyBEVU9DICh1dSB0aWVuIGJhbyBkb25nKQpz'
'eXMuZXhpdCgzIGlmIG5fa2RkIGVsc2UgKDEgaWYgbl90cnVvdCBlbHNlIDApKQo='
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
    # -Kho PHAI la clone RIENG cua phep do: `remote set-url`, `checkout -B do-tam` va `reset --hard` ben duoi GHI DE origin, nhanh do-tam
    # va thu muc lam viec cua no. Do tren pwsh 7.4 (2026-10-10): kho cua nguoi dung co sua doi chua commit tren CONTEXT.md (tep GIONG NHAU
    # o hai commit) + mot commit cuc bo tren do-tam => sau luot chay CONTEXT.md ve nguyen ban, commit cuc bo chi con trong reflog, origin bi
    # doi sang $Url; `checkout -B` chi tu choi khi tep sua KHAC giua hai commit. Chi nhan kho SACH (khong tep tracked bi sua, khong tep
    # chua theo doi): tep chua theo doi song sot `reset --hard` ma bo test duyet ops/leases va ops/reviews.
    $bn = G -C "$Kho" -c core.excludesFile= status --porcelain --untracked-files=all
    # `status` MU voi chi muc: tep tracked da sua + --skip-worktree (the `S`) hoac --assume-unchanged (chu thuong) => status rong. Do tren pwsh 7.4
    # (2026-10-10): assume-unchanged => `reset --hard` GHI DE sua doi ay (mat); skip-worktree => `reset --hard` BO QUA tep, cay do != commit.
    # `-cnotmatch`: `-notmatch` KHONG phan biet hoa thuong nen '^H ' nuot ca `h` (assume-unchanged).
    $cm = @(G -C "$Kho" ls-files -v | Where-Object { $_ -cnotmatch '^H ' })
    if (((($bn | Out-String).Trim()).Length -gt 0) -or ($cm.Count -gt 0)) {
        Dung "kho do $Kho KHONG sach (co sua doi chua commit, tep chua theo doi, hoac tep tracked danh dau --assume-unchanged / --skip-worktree) - phep do se GHI DE no. Dung -Kho tro toi mot thu muc chua co hoac mot clone RIENG chua dung toi, hoac xoa thu muc do"
    }
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
