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
$ShaBoDo    = '46898ee8e39180b711761cb01a1e80c446d247e71a898447b2d306a22cebb5be'      # SHA-256 cua bo do Python nhung ben duoi

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
'LCAiMSIpCm9zLmVudmlyb24uc2V0ZGVmYXVsdCgiUFlUSE9OSU9FTkNPRElORyIsICJ1dGYtOCIpCiMgQ09OR19DVV9HSVQg'
'bGEgYmllbiBESUVVIEtISUVOIGN1YSBDSElOSCBtYSBkdW9jIGRvOiBfZ2l0X3dpbmRvd3MgKGJ1b2MgMSkgZG9jIG9zLmVu'
'dmlyb24ga2hpIEtIT05HIGR1b2MgdHJ1eWVuIGNvbmdfY3VfZ2l0LAojIG1hIHJpZyBkb2kgY2h1bmcgKyBwcm9iZSBOOS1O'
'MTEgKG11YyAzLCBjaGF5IFRST05HIHRpZW4gdHJpbmggbmF5KSB2YSBjYWMgY2EgTjEtTjMvTjktTjExIGN1YSBibyB0ZXN0'
'IChxdWEgY2hheSgpLCB2b24gY2hpIGJvCiMgR0lUXyovUFlUSE9OKikgZGV1IGtob25nIHRydXllbi4gQ0kgS0hPTkcgZGF0'
'IGJpZW4gbmF5LiBEbyB0cmVuIDIwMjYtMDktMzBqLCAwZWE5NWRlLCBDT05HX0NVX0dJVCB0cm8gbW90IGdpdC5leGUgaG9w'
'IGxlOiBibwojIHRlc3QgMTYwLzE2NiwgNiBjYSBQQUNLRVQgRE8gKHQxNjUgdDE2NiB0MTY3IHQxNzAgdDE3MSB0MTcyKSA9'
'PiAiS2hvbmcgY2EgbmFvIGN1YSBQQUNLRVQgYmkgRE8iIFRSVU9UICJiYW4gdmEgQ0hVQSB4b25nIiwgcm9pCiMgUklHIGRv'
'aSBjaHVuZyBLREQgInJpZyBzYWkiIHJjPTMgc2F1IGNhIGJvIHRlc3QgKGNoaSByaWcgVk8gVElOSCBjaGFuIHBoYW4gcXV5'
'ZXQgc2FpKTsgLS10dS1raWVtLXByb2JlOiBOOSBUUlVPVCwgTjEwL04xMSBLREQuCiMgQm8gbyBHT0Mg4oCUIHRpZW4gdHJp'
'bmggbmF5IHZhIG1vaSB0aWVuIHRyaW5oIGNvbiBjdW5nIHRoYXkgbmh1IENJIOKAlCB2YSBHSEkgTEFJIGdpYSB0cmkgZGUg'
'bXVjIDAgdHUga2hhaS4KX0NPTkdfQ1VfR0lUX05HVU9JX0RPID0gb3MuZW52aXJvbi5wb3AoIkNPTkdfQ1VfR0lUIiwgTm9u'
'ZSkKZm9yIF9sIGluIChzeXMuc3Rkb3V0LCBzeXMuc3RkZXJyKToKICAgIHRyeTogX2wucmVjb25maWd1cmUoZW5jb2Rpbmc9'
'InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIikKICAgIGV4Y2VwdCBFeGNlcHRpb246IHBhc3MKaWYgc3lzLnBsYXRmb3JtID09'
'ICJ3aW4zMiI6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlcwogICAgICAgIGN0eXBlcy53aW5kbGwua2VybmVsMzIu'
'U2V0Q29uc29sZU91dHB1dENQKDY1MDAxKQogICAgICAgIGN0eXBlcy53aW5kbGwua2VybmVsMzIuU2V0Q29uc29sZUNQKDY1'
'MDAxKQogICAgZXhjZXB0IEV4Y2VwdGlvbjogcGFzcwoKZGVmIGlubigqcCk6CiAgICB2YW4gPSAiICIuam9pbihzdHIoeCkg'
'Zm9yIHggaW4gcCkKICAgIHRyeTogcHJpbnQodmFuLCBmbHVzaD1UcnVlKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAg'
'ICB0cnk6IHN5cy5zdGRvdXQuYnVmZmVyLndyaXRlKHZhbi5lbmNvZGUoInV0Zi04IiwgInJlcGxhY2UiKSArIGIiXG4iKTsg'
'c3lzLnN0ZG91dC5mbHVzaCgpCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjogcHJpbnQodmFuLmVuY29kZSgiYXNjaWkiLCAi'
'YmFja3NsYXNocmVwbGFjZSIpLmRlY29kZSgiYXNjaWkiKSwgZmx1c2g9VHJ1ZSkKCiMgTmdvYWkgbGUgS0hPTkcgYmF0ID0+'
'IFB5dGhvbiB0aG9hdCByYz0xLCBtYSByYz0xIG8gZGF5IERBIENPIE5HSElBICJjbyBjaG90IFRSVU9UIiAoZG9uZwojIGN1'
'b2kgdGVwKSDigJQgZHVuZyBseSBkbyBwczEgZGF0IGB0cmFwYCAtPiByYz0zLiBEbyBkdW9jOiBnaXQgdmFuZyBQQVRIIChk'
'b25nIGBnaXQoZ29jLAojICJyZXYtcGFyc2UiKWAgY2hheSBUUlVPQyBgaWYgbG9pOmApLCBibyB0ZXN0IHF1YSBoYW4sIHVu'
'ZyB2aWVuIHRoaWV1IF9naXRfd2luZG93cywgcHJvYmUKIyB0aGF0IG5lbSBuZ29haSBsZSDigJQgY2EgYm9uIHR1bmcgcmEg'
'cmM9MSBtYSBwaGVwIGRvIENIVUEgSEUgY2hheSB4b25nLgojIERvbmcgS0VUIExVQU4gaW4gVFJVT0MgdHJhY2ViYWNrLCBj'
'dW5nIGtlbmggc3Rkb3V0OiBraG9pIHBzMSBkYW4gY2hvIHJldmlld2VyIGJhdCBkYXUgVFUgZG9uZwojIG5heSwgbmVuIGlu'
'IHRyYWNlYmFjayB0cnVvYyB0aGkgbm8gbmFtIE5HT0FJIGtob2kgKGRvIHRyZW4gcHdzaCA3LjQ6IGtob2kgMiBkb25nLCAw'
'IGRvbmcKIyB0cmFjZWJhY2spLiB0cnkvZmluYWxseTogaG9vayBUVSBIT05HICh2ZC4gc3Rkb3V0IGxhIG9uZyBkYSBkb25n'
'KSB0aGkgUHl0aG9uIHRyYSByYz0xIOKAlCBkdW5nCiMgbWEgImNvIGNob3QgVFJVT1QiIChkbyBkdW9jOiBCcm9rZW5QaXBl'
'IHRyb25nIGhvb2sgPT4gcmM9MSkuCmRlZiBfbmdvYWlfbGVfbGFfS0REKGtpZXUsIGd0LCB2ZXQpOgogICAgdHJ5OgogICAg'
'ICAgIGltcG9ydCB0cmFjZWJhY2sKICAgICAgICBpbm4oIiIpOyBpbm4oZiJLSE9ORyBETyBEVU9DOiBuZ29haSBsZSBraG9u'
'ZyBsdW9uZyB0cnVvYyB7a2lldS5fX25hbWVfX306IHtndH0iKQogICAgICAgIGlubigiIi5qb2luKHRyYWNlYmFjay5mb3Jt'
'YXRfZXhjZXB0aW9uKGtpZXUsIGd0LCB2ZXQpKS5yc3RyaXAoKSkKICAgICAgICBpbm4oIlBoZXAgZG8gQ0hVQSBjaGF5IHhv'
'bmcuIEtob25nIGtldCBsdWFuIGdpLiIpCiAgICAgICAgZm9yIF9sIGluIChzeXMuc3Rkb3V0LCBzeXMuc3RkZXJyKToKICAg'
'ICAgICAgICAgdHJ5OiBfbC5mbHVzaCgpCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb246IHBhc3MKICAgIGZpbmFsbHk6'
'CiAgICAgICAgb3MuX2V4aXQoMykKc3lzLmV4Y2VwdGhvb2sgPSBfbmdvYWlfbGVfbGFfS0RECgpTSEFfRzEgICA9ICIyZjcw'
'ODY5YTA1Mzc4NDNlOWNhZTc4NjE4ZWU3YWU4YzI2MWQ5NzJkIgojIEtIT05HIGdoaW0gYmFzZS4gU3BlYyByMyBONicga2hh'
'aSBkbyBudW1zdGF0IHNvIGQ3MDU2MjMg4oCUIE5IVU5HIHNwZWMgQ1VORyBiYW8gZXhlY3V0b3IKIyBgZ2l0IG1lcmdlIG9y'
'aWdpbi9tYXN0ZXJgLiBTYXUgbWVyZ2UsIHBoZXAgZG8gc28gZDcwNTYyMyBOVU9UIGNhIHBoYW4gbWFzdGVyIG1hbmcgdmFv'
'OgojIGRvIHRoYXQgMTgtMDkgdHJlbiBiYW4gdmEgZzIgY3VhIGFneSBjaG8gNSB0ZXAgLyArODEyLCB0cm9uZyBraGkgdmll'
'YyBjdWEgYWd5IGxhIDIgdGVwIC8gKzM1My4KIyBNb3QgY2hvdCBuaHUgdGhlIHNlIGJhbyAidnVvdCB0cmFuIiBjaG8gbW90'
'IGJhbiB2YSBLSE9ORyB2dW90LiBCYXNlIGR1bmcgbGEgTUVSR0UtQkFTRS4KU0hBX0JBU0VfU1BFQyA9ICJkNzA1NjIzMTYy'
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0xMC0wMWQiICAgICAgICAgICAgICAj'
'IGRvaSBNT0kga2hpIHN1YSBibyBkbyAtIGxvZyB0dSBraGFpIGJhbiBuYW8KVFJBTl9URVAsIFRSQU5fRE9ORyA9IDIsIDQw'
'MCAgICAgICAgICAjIE43JyBjdWEgc3BlYyByMwpBTF9TQU4gPSAoMSwgNywgNykgICAgICAgICAgICAgICAgICAgICMgc2Fu'
'IGFjdGlvbmxpbnQgPSBiYW4gZ2hpbSBDSTogQUxfVkVSIGN1YSBjaS55bWwgPSBiYW5fZ2hpbSBjdWEgb3BzL2NvbmdfY3Uu'
'eWFtbApHSVRfU0FOID0gKDIsIDM2LCAwKSAgICAgICAgICAgICAgICAgICMgc2FuIGdpdDogdW5nIHZpZW4gZ29pIGBnaXQg'
'd29ya3RyZWUgbGlzdCAtLXBvcmNlbGFpbiAtemAgKGNvIGAtemAgdHUgMi4zNik7IGJhbl9naGltIGdpdCA9IG51bGwKR0lU'
'X1NBTl9CQVNIID0gKDIsIDMxLCAwKSAgICAgICAgICAgICAjIHNhbiBnaXQgVFJPTkcgYmFzaCBjdWEgYm8gdGVzdDogdDE1'
'MiBkdW5nIEdJVF9DT05GSUdfQ09VTlQgKGNvIHR1IDIuMzEpCk1BVV9XSU4gID0gJ2lmIG5lbl90aHVjID09ICJ3aW5kb3dz'
'IjonCiMgV3JpdGUgc2V0IGN1YSBwYWNrZXQgIzU0MSBnMi4gRGlmZiBraG9uZyBjaGFtIHRlcCBuYW8gbyBkYXkgPT4gZG8g'
'TkhBTSBOSEFOSC4KV1JJVEVfU0VUX0cyID0geyJvcHMvbGVhc2VfcHVibGlzaC5weSIsICJvcHMvbGVhc2VfcHVibGlzaF90'
'ZXN0LnB5In0KIyAiVHVvaSIgY2hpIGNvIG5naGlhIGtoaSBzbyB2b2kgTUFZIENIVSBUSEFULiBNb3QgbWlycm9yIGN1YyBi'
'byBjdSBjdW5nIHRyYSBscy1yZW1vdGUgPT0KIyBvcmlnaW4vbWFzdGVyIChkbyBkdW9jOiBtYXN0ZXIgYzE2YmQzMiAtPiAi'
'dmUgbmVuIFRVT0kiLCA0NiB0ZXAgLyArNzExOCBjaG8gMGVhOTVkZSkuCiMgRGFuaCBzYWNoIENITyBQSEVQOyBgcmVtb3Rl'
'IGdldC11cmxgIGRhIGtoYWkgdHJpZW4gaW5zdGVhZE9mIG5lbiBjaHV5ZW4gaHVvbmcgY3VuZyBsbyByYS4KVVJMX0tIT19I'
'T1BfTEUgPSB7Imh0dHBzOi8vZ2l0aHViLmNvbS9kdWN0aGFuZ2hvL3RyYS1sdWF0IiwgImh0dHBzOi8vZ2l0aHViLmNvbS9k'
'dWN0aGFuZ2hvL3RyYS1sdWF0LmdpdCIsCiAgICAgICAgICAgICAgICAgICMgU1NIIHRvaSBDVU5HIGtobyAoc2F1IF91cmxf'
'c2FjaCk6IGB1cmwuImdpdEBnaXRodWIuY29tOiIuaW5zdGVhZE9mICJodHRwczovL2dpdGh1Yi5jb20vImAKICAgICAgICAg'
'ICAgICAgICAgIyByYXQgcGhvIGJpZW4gbyBtYXkgZGV2OyB0aGlldSBoYWkgZGFuZyBuYXkgdGhpIGtobyBUSEFUIGJpIGJh'
'byAiS0hPTkcgcGhhaSBraG8gdGhhdCIuCiAgICAgICAgICAgICAgICAgICJzc2g6Ly9naXRodWIuY29tL2R1Y3RoYW5naG8v'
'dHJhLWx1YXQiLCAic3NoOi8vZ2l0aHViLmNvbS9kdWN0aGFuZ2hvL3RyYS1sdWF0LmdpdCIsCiAgICAgICAgICAgICAgICAg'
'ICJnaXRAZ2l0aHViLmNvbTpkdWN0aGFuZ2hvL3RyYS1sdWF0IiwgImdpdEBnaXRodWIuY29tOmR1Y3RoYW5naG8vdHJhLWx1'
'YXQuZ2l0In0KIyBgcmVtb3RlIGdldC11cmxgIEtIQUkgVFJJRU4gaW5zdGVhZE9mLCBtYSBtYXUgYHVybC4iaHR0cHM6Ly88'
'dG9rZW4+QGdpdGh1Yi5jb20vIi5pbnN0ZWFkT2ZgIHJhdCBwaG8KIyBiaWVuLiBJbi9naGkgbmd1eWVuIHZhbiBsYSBkdWEg'
'VE9LRU4gdmFvIGxvZyB2YSB2YW8ga2hvaSBKU09OIHBzMSBiYW8gZGFuIGNobyByZXZpZXdlciAoZG8gZHVvYzoKIyAzIGRv'
'bmcgdHJvbmcga2hvaSBkYW4pLiBCbyB1c2VyaW5mbyBUUlVPQyBraGkgaW4gdmEgVFJVT0Mga2hpIHNvIOKAlCB0b2tlbiB2'
'YW4gbGEgR2l0SHViIHRoYXQuCiMgQXV0aG9yaXR5IGtldCB0aHVjIG8gYC9gLCBgP2AgaG9hYyBgI2AgREFVIFRJRU4g4oCU'
'IGR1bmcgbHVhdCBnaXQvY3VybC4gQmFuIGBbXi9dKkBgIG51b3QgY2EgYD9gL2AjYAojIG5lbiBtb3QgVVJMIHRybyB0b2kg'
'TUFZIEtIQUMgKGhvc3QgZHVuZyB0cnVvYyBgP2AsIGR1b2kgYD9gIGxhIGBAZ2l0aHViLmNvbS88a2hvPmApIGR1b2MgImxh'
'bSBzYWNoIgojIHRoYW5oIGR1bmcgbW90IG11YyBDSE8gUEhFUCwgdHJvbmcga2hpIGdpdCBub2kgdG9pIG1heSBraWEgKGRv'
'IGR1b2M6IG1pcnJvciBjdSBwaHVjIHZ1IHF1YSBIVFRQUyA9PgojICJ2ZSBuZW4gVFVPSSIsIFRSVU9UIDQ2IHRlcCAvICs3'
'MTE4KS4gVmFuIGJvIHRvaSBgQGAgQ1VPSSB0cm9uZyBhdXRob3JpdHk6IHVzZXJpbmZvIGNvIGBAYCB0cmFuIHRoaQojIGN1'
'cmwgdHUgY2hvaSAoIkJhZCBob3N0bmFtZSIpLCBjb24ga2hpIGluIHRoaSBraG9uZyBsbyBwaGFuIHNhdSBgQGAgdGh1IG5o'
'YXQuCl9SWF9VU0VSSU5GTyA9IHJlLmNvbXBpbGUociJeKFtBLVphLXpdW0EtWmEtejAtOSsuLV0qOi8vKVteLz8jXSpAIikK'
'ZGVmIF91cmxfc2FjaCh1KTogcmV0dXJuIF9SWF9VU0VSSU5GTy5zdWIociJcMSIsIHUgb3IgIiIpICAgICAgICAgICMgZGUg'
'U08gKGx1YXQgZ2l0L2N1cmwpCiMgSU4gcGhhaSBjaGUgUk9ORyBob24gU086IG1hdCBraGF1IGNvIGA/YC9gI2AgVFJBTiB0'
'aGkgYFteLz8jXSpAYCBraG9uZyBraG9wIG5lbiBVUkwgcmEgbG9nIE5HVVlFTiBWQU4KIyAoZG8gZHVvYyB0cmVuIDIwMjYt'
'MDktMzBiOiAzIGRvbmcgbyAtLWNoaS1raWNoLXRodW9jLCAzIGRvbmcgdHJvbmcga2hvaSBkYW4gLS1jaGktcHJvYmU7IGJh'
'biAzMGE6IDApLgojIENoZSB0b2kgYEBgIENVT0kgQ1VORyBjdWEgQ0EgY2h1b2kgKGNvIGhheSBraG9uZyBjbyBzY2hlbWUp'
'LCB2YSBERSBEQVUgYCoqKkBgIGRlIGJhbiBpbiBraG9uZyB0dSBuaGFuIGxhCiMgZ2l0aHViLmNvbSBraGkgZ2l0IG5vaSB0'
'b2kgbWF5IGtoYWMgKHZkLiBob3N0IHRydW9jIGA/YCkuIEJhbiAzMGMgY2hlICJ0b2kgYEBgIGN1b2kgdHJ1b2MgYC9gIGRh'
'dSB0aWVuIgojIG5lbiBWQU4gbG8ga2hpIG1hdCBraGF1IGNvIGAvYCB0cmFuLCBob2FjIFVSTCBkYW5nIHNjcCBgdXNlcjpt'
'a0Bob3N0OmR1b25nYCAoa2hvbmcgc2NoZW1lKSDigJQgZG8gdHJlbgojIDIwMjYtMDktMzBjOiAzIGRvbmcgLyAxIHRyb25n'
'IGtob2kgZGFuIC0tY2hpLWtpY2gtdGh1b2MsIDUgLyAzIG8gLS1jaGktcHJvYmUsIG1vaSBkYW5nLiBNb2kga3kgdHUgRFVO'
'RwojIGxhIG1vdCBkdW9uZyBudWE7ICJ0b2kgYEBgIGN1b2kiIGtob25nIGNvbiBreSB0dSBkdW5nIG5hby4gSGFpIHF1eSB0'
'YWMsIGhhaSBtdWMgZGljaDogU08gdGhlbyBnaXQsIElOCiMgdGhlbyAidGh1YSBjb24gaG9uIGxvIi4gIkNBIGNodW9pIiBw'
'aGFpIGR1bmcgY2Ega2hpIGNodW9pIGNvIFhVT05HIERPTkc6IGdpdCgpIGRvYyBiYW5nIHRleHQ9VHJ1ZSBuZW4gQ1IvTEYg'
'dHJvbmcgVVJMCiMgZGEgdGhhbmggTEYsIG1hIGAuYCBraG9uZyBraG9wIExGLiBUb2tlbiBkb2MgdHUgdGVwIENSTEYgKGBo'
'dHRwczovL3gtYWNjZXNzLXRva2VuOjx0b2tlbj5gICsgQ1IgKyBgQGdpdGh1Yi5jb20vLi4uYCkKIyB0aGkgYmFuIDMwZSBL'
'SE9ORyBjaGUgZ2k6IGluIE5HVVlFTiB0b2tlbiBvIGRvbmcgYG9yaWdpbiA6YCB2YSBvICJvcmlnaW5fdXJsIiB0cm9uZyBr'
'aG9pIEpTT04gZGFuIChkbyB0cmVuIDIwMjYtMDktMzBlKS4KZGVmIF91cmxfaW4odSk6IHJldHVybiByZS5zdWIociJeKFtB'
'LVphLXpdW0EtWmEtejAtOSsuLV0qOi8vKT8uKkAiLCByIlwxKioqQCIsIHUgb3IgIiIsIGZsYWdzPXJlLlMpCiMgVGhvbmcg'
'YmFvIGxvaSBjdWEgZ2l0IENISSBibyB1c2VyaW5mbyB0b2kgYEBgIERBVSBUSUVOOiB1c2VyaW5mbyBjbyBgQGAgdHJhbiAo'
'dmQuIHRlbiBkYW5nIG5oYXAgbGEKIyBlbWFpbCkgdGhpIHBoYW4gc2F1IHZhbiByYSBzdGRlcnIgbHMtcmVtb3RlLCBtYSBz'
'dGRlcnIgYXkgZHVvYyBpbiB2YW8gZG9uZyBLREQgY3VhIE43JyAoZG8gZHVvYzoKIyAyIGRvbmcgdHJvbmcgbG9nLCAxIHRy'
'b25nIGtob2kgZGFuKS4gTGFtIHNhY2ggTU9JIFVSTCB0cm9uZyB2YW4gYmFuIHRydW9jIGtoaSBpbiDigJQgY2hlIHRvaSBg'
'QGAgQ1VPSSB0cmVuCiMgRE9ORyAoY3VuZyBsdWF0IElOIHZvaSBfdXJsX2luOiBraG9uZyBjb24ga3kgdHUgZHVuZyBuYW8p'
'LiBCYW4gMzBkIGR1bmcgbyBgXHMnImAgbmVuIHBoYW4gZ2l0IGRlIGxhaSBjbwojIGAnYC9gImAva2hvYW5nIHRyYW5nICh2'
'ZC4gYHVAeDpwJzxiaSBtYXQ+QGdpdGh1Yi5jb21gKSBWQU4gbG8g4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGQ6IDIgZG9uZyAv'
'IDEgdHJvbmcKIyBraG9pIGRhbiAtLWNoaS1raWNoLXRodW9jLCAzIC8gMiBvIC0tY2hpLXByb2JlLCBtb2kgZGFuZy4KZGVm'
'IF9hbl91c2VyaW5mbyh0KTogcmV0dXJuIHJlLnN1YihyIihbQS1aYS16XVtBLVphLXowLTkrLi1dKjovLylbXlxuXSpAIiwg'
'ciJcMSoqKkAiLCB0IG9yICIiKQojIENhIG5nb2FpIHBoYW0gdmkgcjMgwqduZ29haV9waGFtX3ZpIOKAlCBkbyBDSElOSCBT'
'UEVDIGtoYWksIGtob25nIHBoYWkgYm8gZG8gdHUgcXV5ZXQuCiMgRG8gbGEgREFOSCBTQUNIIENITyBQSEVQOiBjYSBkbyBu'
'YW8gS0hPTkcgbmFtIHRyb25nIGRheSB2YSBLSE9ORyBwaGFpICJ0aGlldSBjb25nIGN1IgojIHRoaSBsYSBUUlVPVC4gRGFu'
'aCBzYWNoIGNhbSB0aGkgYmFvIGdpbyBjdW5nIHRoaWV1OyBkYW5oIHNhY2ggY2hvIHBoZXAgdGhpIGJpZXQgdHJ1b2MuCk5H'
'T0FJX1BIQU1fVkkgPSBzZXQoInQxMzEgdDEzMiB0MTUwIHQxMjUgdDM1IHQzNiB0MzcgdDM4IHQzOSB0NDAiLnNwbGl0KCkp'
'CiMgQ2EgY3VhIENISU5IIHBhY2tldCBuYXkuIE1vdCBjYSBvIGRheSBtYSBETyB0aGkga2hvbmcgYmFvIGdpbyBkdW9jIGJv'
'IHF1YS4KQ0FfUEFDS0VUID0gc2V0KCJ0MTY1IHQxNjYgdDE2NyB0MTY4IHQxNjkgdDE3MCB0MTcxIHQxNzIgdDE3MyIuc3Bs'
'aXQoKSkKIyBDYSBNT0kgbWEgZzIgdGhlbSB2YW8gKE44LU4xMikuIERvaSB0dW9uZyBkbyBwaGFpIE1BTkcgY2h1bmcgdmFv'
'OiBtZXJnZS1iYXNlIGNodWEgY28sIEhFQUQgY28uCkNBX01PSV9HMiA9ICJ0MTY5IHQxNzAgdDE3MSB0MTcyIHQxNzMiLnNw'
'bGl0KCkKQ0ExNSAgPSAidDEyOSB0MTMwIHQxMzEgdDEzMiB0MTMzIHQxMzYgdDEzOCB0MTM5IHQxNDQgdDE0NSB0MTQ2IHQx'
'NDcgdDE0OSB0MTUwIHQxNTEiLnNwbGl0KCkKQ0FNT0kgPSAidDE2NSB0MTY2IHQxNjcgdDE2OCIuc3BsaXQoKQoKREFULCBU'
'UlVPVCwgS0REID0gIkRBVCIsICJUUlVPVCIsICJLSE9ORyBETyBEVU9DIgpzbywgY2hvdCA9IHt9LCBbXQpkZWYgZ2hpKGss'
'IHYpOiBzb1trXSA9IHY7IHJldHVybiB2CmRlZiBrZXQodGVuLCB0cmFuZ190aGFpLCBjaGlfdGlldD0iIik6CiAgICBjaG90'
'LmFwcGVuZCgodGVuLCB0cmFuZ190aGFpLCBjaGlfdGlldCkpCiAgICBpbm4oZiIgIFt7dHJhbmdfdGhhaToxNH1dIHt0ZW59'
'IiArIChmIiAgIHtjaGlfdGlldH0iIGlmIGNoaV90aWV0IGVsc2UgIiIpKQogICAgcmV0dXJuIHRyYW5nX3RoYWkKCiMgLS0t'
'LS0tLS0tLS0tLS0tLSBkb2MgbG9nIGN1YSBibyB0ZXN0IChiYW4gMywgZGEgZG8gdHJlbiBsb2cgVEhBVCkgLS0tLS0tLS0t'
'LS0tLS0tLQpSWF9ET19DSE8gID0gcmUuY29tcGlsZShyIig/bSleISEhIGRvIChcUyspICguKikkIikKUlhfRE9fQ1VPSSA9'
'IHJlLmNvbXBpbGUociIoP20pXiB7Mn0oXFN7MSw0fSkgezJ9KFxTKyk6ICguKikkIikKUlhfQk9fUVVBICA9IHJlLmNvbXBp'
'bGUociIoP20pXiB7Mn1cU3sxLDZ9IFFVQSAoXFMrKTogKC4qKSQiKQojIERvbmcgdG9uZyBrZXQgVEhBVCBvIERBVSBkb25n'
'LiBDYSBETyBjbyB0aGUgaW4gbGFpIHN0ZG91dCBjdWEgbW90IGx1b3QgQ09OICh0MTU1IGNoYXkgbGFpIHQwMSwgdDcyL3Q5'
'OCBjaGF5CiMgImJvIikg4oCUIGRvbmcgdG9uZyBMT05HIGF5IG5hbSBHSVVBIGRvbmcgKGRvOiAyMCBkb25nIGxvbmcgZGV1'
'IG8gZ2l1YSBkb25nLCBjaGkgZG9uZyB0b25nIHRoYXQgbyBkYXUgZG9uZyksIG1hCiMgYHNlYXJjaGAga2hvbmcgbmVvIGJh'
'dCBubyBUUlVPQy4gRG8gdHJlbiAyMDI2LTA5LTMwYywgMGVhOTVkZSArIGRvdCBiaWVuIGxhbSB0MDEgRE86IGRvYyByYSAi'
'MC8xIiA9PgojICJkYW5oIHNhY2ggS0hPTkcgZGF5IGR1IiwgIkxFQ0ggU08gSE9DOiB0aGlldSAtMjAgY2EiLCB0cm9uZyBr'
'aGkgdG9uZyB0aGF0IDE2Ni0xNDU9MjEgPT0gMjEgY2EgZG9jIGR1b2MuClJYX1RPTkcgICAgPSByZS5jb21waWxlKHIiKD9t'
'KV5sZWFzZV9wdWJsaXNoOiAoXGQrKS8oXGQrKVxiW15cbl0qPz0oXGQrKSxbXlxuXSo/PShcZCspIikKCmRlZiBzb19jYSh0'
'KToKICAgIG0gPSByZS5tYXRjaChyInQoXGQrKSIsIHQpOyByZXR1cm4gKGludChtLmdyb3VwKDEpKSBpZiBtIGVsc2UgMTAq'
'KjYsIHQpCgpkZWYgZG9jX2RvKG91dCk6CiAgICB0YWlfY2hvID0ge3Q6IGwuc3RyaXAoKSBmb3IgdCwgbCBpbiBSWF9ET19D'
'SE8uZmluZGFsbChvdXQpfQogICAgYm8gPSB7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXQpfQogICAgY3Vv'
'aSA9IHt0OiBsLnN0cmlwKCkgZm9yIF8sIHQsIGwgaW4gUlhfRE9fQ1VPSS5maW5kYWxsKG91dCkgaWYgdCBub3QgaW4gYm99'
'CiAgICBob3AgPSBkaWN0KGN1b2kpOyBob3AudXBkYXRlKHRhaV9jaG8pCiAgICBnYywgdGluID0gW10sIFRydWUKICAgIGlm'
'IHNldCh0YWlfY2hvKSAhPSBzZXQoY3VvaSk6CiAgICAgICAgZ2MuYXBwZW5kKGYiaGFpIG5ndW9uIExFQ0g6IGNoaS10YWkt'
'Y2hvPXtzb3J0ZWQoc2V0KHRhaV9jaG8pLXNldChjdW9pKSl9IGNoaS1jdW9pPXtzb3J0ZWQoc2V0KGN1b2kpLXNldCh0YWlf'
'Y2hvKSl9IikKICAgICAgICB0aW4gPSBGYWxzZQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dCkKICAgIGlmIG5vdCBtOgog'
'ICAgICAgIGdjLmFwcGVuZCgiS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCIpOyB0aW4gPSBGYWxzZQogICAgZWxzZToK'
'ICAgICAgICBkYXQsIHRyZW4gPSBpbnQobS5ncm91cCgxKSksIGludChtLmdyb3VwKDIpKQogICAgICAgIGdjLmFwcGVuZChm'
'InNvIGhvYzoge3RyZW59LXtkYXR9PXt0cmVuLWRhdH0gZG87IGRvYyBkdW9jIHtsZW4oaG9wKX0iKQogICAgICAgIGlmIHRy'
'ZW4gLSBkYXQgIT0gbGVuKGhvcCk6CiAgICAgICAgICAgIGdjLmFwcGVuZChmIkxFQ0ggU08gSE9DOiB0aGlldSB7dHJlbi1k'
'YXQtbGVuKGhvcCl9IGNhIik7IHRpbiA9IEZhbHNlCiAgICByZXR1cm4gaG9wLCBnYywgdGluCgojIE1hdSBjbyBkb25nIHRv'
'bmcgTE9ORyBnaXVhIGRvbmcgKGRhbmcgdDE1NSBpbiBsYWkgbHVvdCBjb24pOiBibyBkb2MgYmF0IGRvbmcgdG9uZyBEQVUg'
'VElFTiBsYSB0dSBraWVtIERPLgpfTUFVID0gKCIhISEgZG8gdDAyYl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTiBhICdsZWFz'
'ZV9wdWJsaXNoOiAwLzEgxJHhuqF0OyDEkcOjIGNo4bqheT0xLCBi4buPIHF1YT0wJ1xuIgogICAgICAgICIhISEgZG8gdDE1'
'MF94IFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAgICAgIiAgQuG7jiBRVUEgdDEzMV95OiBuZW4g'
'Zml4dHVyZVxuIgogICAgICAgICIgIMSQ4buOICB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOOiBhXG4iCiAgICAgICAg'
'IiAgxJDhu44gIHQxNTBfeDogV2luRXJyb3IgMTMxNCByZXF1aXJlZCBwcml2aWxlZ2VcbiIKICAgICAgICAibGVhc2VfcHVi'
'bGlzaDogMS8zIMSR4bqhdDsgxJHDoyBjaOG6oXk9MywgYuG7jyBxdWE9MVxuIikKCiMgQmllbiBQWVRIT04qIGN1YSBtYXkg'
'bmd1b2kgZG8gbG90IHZhbyBibyB0ZXN0IGxhIERPSSBIQU5IIFZJIGJvIHRlc3Q6IFBZVEhPTk9QVElNSVpFIGJvIG1vaSBg'
'YXNzZXJ0YCAoZG8gdHJlbgojIDIwMjYtMDktMzBjOiBgYXNzZXJ0IEZhbHNlYCBxdWEsIHJjPTApOyBiYW4gMzBkIGNoaSB0'
'cnVuZyBob2EgTU9UIGJpZW4gYXksIGNvbiBQWVRIT05ERVZNT0RFPTEgbGFtIHQxNTQgRE8gMi80CiMgbGFuIHRyZW4gMy4x'
'MSAoc2FjaDogNC80IFFVQSkgPT4gcmM9MSAiVFJVT1QgTW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MiIGNobyB1bmcg'
'dmllbiBzYWNoIChkbyB0cmVuCiMgMjAyNi0wOS0zMGQpLiBEYW5oIHNhY2ggQ0FNIGx1b24gdGhpZXUgbW90IGJpZW4g4oCU'
'IG5lbiBkYXkgbGEgZGFuaCBzYWNoIENITyBQSEVQOiBjaGkgZ2l1IGJpZW4gZGUgdHJpbmggdGhvbmcKIyBkaWNoIENIQVkg'
'dmEgdGltIGdvaSBEQSBDQUk7IFBZVEhPTlBBVEggS0hPTkcgZ2l1IChDSSBraG9uZyBjbyBubykuIFBoZXAgaG9pIGRpZXUg'
'a2llbiB0aWVuIHF1eWV0IG8gbXVjIDAKIyBjdW5nIGNoYXkgcXVhIGRheSwgbmVuIG5vIHRoYXkgRFVORyBtb2kgdHJ1b25n'
'IG1hIGJvIHRlc3Qgc2UgdGhheS4KX1BZX0dJVSA9IGZyb3plbnNldCh7IlBZVEhPTkhPTUUiLCAiUFlUSE9OVVNFUkJBU0Ui'
'LCAiUFlUSE9OTk9VU0VSU0lURSJ9KQojIENhdSBoaW5oIGdpdCBDVUEgTkdVT0kgRE8gbG90IHZhbyBibyB0ZXN0IHkgbmh1'
'IGJpZW4gUFlUSE9OKjogY2EgdGVzdCBnb2kgZ2l0IGJhbmcgZGljdChvcy5lbnZpcm9uKSwgbmVuIGRvYyBjYXUgaGluaAoj'
'IGNhIG5oYW4gdmEgYmllbiBHSVRfKiBjdWEgbWF5IGRvLiBEbyB0cmVuIDIwMjYtMDktMzBlLCAwZWE5NWRlOiBgaW5pdC5k'
'ZWZhdWx0QnJhbmNoID0gbWFpbmAgPT4gMTYzLzE2NiwgdDEzNCB0MTM5IHQxNTEKIyBETyA9PiByYz0xICJUUlVPVCBNb2kg'
'Y2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIgY2hvIHVuZyB2aWVuIHNhY2ggKHNhY2g6IDE2Ni8xNjYpIOKAlCBvIHBoYW0g'
'dmkgZ2xvYmFsIExBTiBoZSB0aG9uZy4KIyBCbyBNT0kgYmllbiBHSVRfKiB2YSB0aGF5IGdsb2JhbCBDQSBOSEFOIGJhbmcg'
'Z2xvYmFsIENVQSBDSS4gQ0kgS0hPTkcgY28gZ2xvYmFsIHJvbmc6IGpvYiBgZ2F0ZWAgY3VhIGNpLnltbCAoYnVvYyAiRm9y'
'Y2UgTEYKIyBjaGVja291dCIsIGNhIHVidW50dSBsYW4gd2luZG93cykgZGF0IGdsb2JhbCBjb3JlLmF1dG9jcmxmPWZhbHNl'
'LCBjb3JlLmVvbD1sZiwgY29yZS5hYmJyZXY9NyBUUlVPQyBidW9jIGNoYXkgYm8gdGVzdCDigJQKIyB2aSAoY2kueW1sOjct'
'OCB0dSBraGFpKSBraG9uZyB0YXQgdGhpIHJ1bm5lciBXaW5kb3dzIGNoZWNrb3V0IENSTEY6IGF1dG9jcmxmPXRydWUgY3Vh'
'IGJhbiBjYWkgR2l0IG8gSEUgVEhPTkcuIEJhbiAzMGYKIyBkYXQgZ2xvYmFsID0gcm9uZyBuZW4gYm8gdGVzdCB0aGF5IGF1'
'dG9jcmxmPXRydWUgY29uIENJIHRoYXkgZmFsc2U6IGRvIHRyZW4gMjAyNi0wOS0zMGYsIDBlYTk1ZGUsIGhlIHRob25nIGF1'
'dG9jcmxmPXRydWUKIyArIGdsb2JhbCBuaHUgQ0kgPT4gYmFuIDMwZSAxNjYvMTY2LCBiYW4gMzBmIDE2NS8xNjYgKHQxNTAg'
'RE8g4oCUIGNoaSBraG9uZyB0aGFuaCBUUlVPVCB2aSB0MTUwIHRpbmggY28gbmFtIHRyb25nCiMgTkdPQUlfUEhBTV9WSSku'
'IEdsb2JhbCBsYSBURVAgVEFNIGNodWEgRFVORwojIGdsb2JhbCBjdWEgQ0kgY29uZyBpbml0LmRlZmF1bHRCcmFuY2ggZ2hp'
'bSB2ZSBtYWMgZGluaCBjdWEgZ2l0IChkYXQgZHVvYyBjYSBvIGhlIHRob25nKTogZ2xvYmFsIGRlIGxlbiBoZSB0aG9uZyBu'
'aHUgdHJlbiBDSSwKIyBjb24gY2F1IGhpbmggQ1VDIEJPIGN1YSBmaXh0dXJlIHZhbiBkZSBsZW4gZ2xvYmFsIChHSVRfQ09O'
'RklHX0NPVU5UIHRoaSBkZSBsZW4gY2EgY3VjIGJvKS4gRG9pIGJ1b2MgYXkgdHJvbmcgY2kueW1sIHRoaQojIGRvaSBfR0lU'
'X0dMT0JBTF9DSS4gR0lUX0NPTkZJR19HTE9CQUwgY2hpIHRoYXkgVEVQIENPTkZJRzogaWdub3JlL2F0dHJpYnV0ZXMgbWFj'
'IGRpbmggKCRYREdfQ09ORklHX0hPTUUgaG9hYyB+Ly5jb25maWcvZ2l0LwojIGlnbm9yZXxhdHRyaWJ1dGVzKSBjdWEgbmd1'
'b2kgZG8gVkFOIGFwIGNobyBnaXQgY29uIChkbyB0cmVuIDIwMjYtMDktMzBnLCAwZWE5NWRlOiB+Ly5jb25maWcvZ2l0L2ln'
'bm9yZSBgKi55YW1sYCA9PiBiYW4gMzBnCiMgMTU0LzE2NiwgMTEgY2EgImxhIik7IENJIGtob25nIGNvIHRlcCBuYW8gbyBk'
'byA9PiBYREdfQ09ORklHX0hPTUUgdHJvIHZhbyB0aHUgbXVjIFRBTSBST05HLiBDb24gbGFpIChraG9hIGhlIHRob25nIGto'
'YWMpCiMgbGEgZ2lvaSBoYW4gZGEgYmlldCwga2hvbmcgcGhhaSBkYSBkb25nLgojIENhdSBoaW5oIHNoZWxsY2hlY2sgQ1VB'
'IE5HVU9JIERPIGxvdCB2YW8gYm8gdGVzdCB5IG5odSBnaXQ6IHQxMzcgZ29pIHNoZWxsY2hlY2sgVEhBTkcsIHQzMy90MTM3'
'IGdvaSBhY3Rpb25saW50IC0+IHNoZWxsY2hlY2ssCiMgY2EgaGFpIGRvYyBTSEVMTENIRUNLX09QVFMsIHZhIHQxMzcgZG9j'
'IH4vLnNoZWxsY2hlY2tyYyAoWERHX0NPTkZJR19IT01FIHRhbSBLSE9ORyBjaGUgZHVvYzsgY2hvIHRlcCByYyB0cmVuIFdp'
'bmRvd3M6IEtIT05HIERPIERVT0MpLgojIERvIHRyZW4gMjAyNi0wOS0zMGgsIDBlYTk1ZGU6IFNIRUxMQ0hFQ0tfT1BUUz0t'
'LWVuYWJsZT1hbGwgPT4gdDMzICsgdDEzNyBETzsgfi8uc2hlbGxjaGVja3JjIGBlbmFibGU9YWxsYCA9PiB0MTM3IERPIOKA'
'lCBjYSAibGEiCiMgPT4gVFJVT1QgY2hvIHVuZyB2aWVuIHNhY2guIENJIGtob25nIGNvIGNhIGhhaS4gU0hFTExDSEVDS19P'
'UFRTPS0tbm9yYyBkZSBsZW4gYmllbiBjdWEgbmd1b2kgZG8gVkEgdGF0IG1vaSB0ZXAgcmMgKHNoZWxsY2hlY2sKIyBwaGFp'
'IE5IQU4gLS1ub3JjIOKAlCBtdWMgMCBob2kgdHJ1b2MpLiBCQVNIX0VOViAoa2UgY2EgYHNldCAtZXVvIHBpcGVmYWlsYCkg'
'ZG86IDE2Ni8xNjY7IEJBU0hfRU5WIGluIGJ5dGUgbmdvYWkgVVRGLTggdGhpCiMgdDMyL3Q1MS10NjggRE8gKDE1Mi8xNjYs'
'IGRvIDIwMjYtMTAtMDEpIOKAlCBtdWMgMCBob2kgYmFzaCB0cm9uZyBDSElOSCBtb2kgdHJ1b25nIGF5IChjaG90IGBfYmFz'
'aF9wb3NpeCgpYCBkdW9pKS4KX0dJVF9HTE9CQUxfQ0kgPSAiW2luaXRdXG5cdGRlZmF1bHRCcmFuY2ggPSBtYXN0ZXJcbltj'
'b3JlXVxuXHRhdXRvY3JsZiA9IGZhbHNlXG5cdGVvbCA9IGxmXG5cdGFiYnJldiA9IDdcbiIKZGVmIGNoYXkoYXJndiwgY3dk'
'LCBwaHV0PTYwKToKICAgIGZkLCBnYyA9IHRlbXBmaWxlLm1rc3RlbXAocHJlZml4PSJ3cDU0MS1naXRjb25maWctY2ktIiwg'
'c3VmZml4PSIuaW5pIikKICAgIHhkZyA9IE5vbmUKICAgIHRyeToKICAgICAgICB4ZGcgPSB0ZW1wZmlsZS5ta2R0ZW1wKHBy'
'ZWZpeD0id3A1NDEteGRnLSIpCiAgICAgICAgd2l0aCBvcy5mZG9wZW4oZmQsICJ3IiwgZW5jb2Rpbmc9ImFzY2lpIiwgbmV3'
'bGluZT0iXG4iKSBhcyBmOiBmLndyaXRlKF9HSVRfR0xPQkFMX0NJKQogICAgICAgIG10ID0ge2s6IHYgZm9yIGssIHYgaW4g'
'b3MuZW52aXJvbi5pdGVtcygpCiAgICAgICAgICAgICAgaWYgbm90IGsudXBwZXIoKS5zdGFydHN3aXRoKCJHSVRfIikgYW5k'
'IChub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIlBZVEhPTiIpIG9yIGsudXBwZXIoKSBpbiBfUFlfR0lVKX0KICAgICAgICBt'
'dC51cGRhdGUoUFlUSE9OVVRGOD0iMSIsIFBZVEhPTklPRU5DT0RJTkc9InV0Zi04IiwgUFlUSE9ORE9OVFdSSVRFQllURUNP'
'REU9IjEiLCBQWVRIT05VTkJVRkZFUkVEPSIxIiwKICAgICAgICAgICAgICAgICAgR0lUX0NPTkZJR19HTE9CQUw9Z2MsIFhE'
'R19DT05GSUdfSE9NRT14ZGcsIFNIRUxMQ0hFQ0tfT1BUUz0iLS1ub3JjIikKICAgICAgICBwID0gc3VicHJvY2Vzcy5ydW4o'
'W3N5cy5leGVjdXRhYmxlXSArIGFyZ3YsIGN3ZD1zdHIoY3dkKSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwKICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgdGV4dD1UcnVlLCBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBo'
'dXQqNjAsIGVudj1tdCkKICAgIGZpbmFsbHk6CiAgICAgICAgdHJ5OiBvcy5yZW1vdmUoZ2MpCiAgICAgICAgZXhjZXB0IE9T'
'RXJyb3I6IHBhc3MKICAgICAgICBpZiB4ZGc6IHNodXRpbC5ybXRyZWUoeGRnLCBpZ25vcmVfZXJyb3JzPVRydWUpCiAgICBy'
'ZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpICsgKHAuc3RkZXJyIG9yICIiKQoKZGVmIG1hdV9jYShvdXQs'
'IHQpOgogICAgbSA9IHJlLnNlYXJjaChyIig/bSlePDw8IHJhICgiICsgdCArIHIiW2Etel0/X1xTKikgWzAtOS5dK3MgKFx3'
'KylccyokIiwgb3V0KQogICAgcmV0dXJuIG0uZ3JvdXAoMikgaWYgbSBlbHNlIE5vbmUKCmRlZiBnaXQoZ29jLCAqYSwgcGh1'
'dD01KToKICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbImdpdCIsICItQyIsIHN0cihnb2MpLCAqYV0sIGNhcHR1cmVfb3V0cHV0'
'PVRydWUsIHRleHQ9VHJ1ZSwKICAgICAgICAgICAgICAgICAgICAgICBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxh'
'Y2UiLCB0aW1lb3V0PXBodXQqNjApCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpLnN0cmlwKCks'
'IChwLnN0ZGVyciBvciAiIikuc3RyaXAoKQoKCiMgPT09PT09PT09PT09PT09PT0gTkFNIFBST0JFLCB2aWV0IHRoYW5oIEhB'
'TSBUSFVBTiBkZSBUVSBLSUVNIGR1b2MgPT09PT09PT09PT09PT09PT0KIyBNb2kgaGFtIHRyYSAodHJhbmdfdGhhaSwgY2hp'
'X3RpZXQsIGR1X2xpZXUpLiBLSE9ORyBpbiwgS0hPTkcgdGhvYXQg4oCUIG5obyB2YXkgY2h1bmcKIyBjaGF5IGR1b2MgdHJl'
'biBuZW4gQkFUIEtZLCB2YSBgLS10dS1raWVtLXByb2JlYCBnb2kgdGhhbmcgY2h1bmcgZGUga2llbSBjaGluaCBibyBkby4K'
'CmRlZiBfc2FuKHQpOgogICAgZCA9IFBhdGgodCkvImQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtk'
'aXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIHJldHVybiBkLCBjdywgcGYKCmRlZiBkb19uOChnb2ks'
'IHNpZywgdGVwdCk6CiAgICAiIiJCdW9jIDEgKENPTkdfQ1VfR0lUKSBjaGkgZHVvYyBuaGFuIGdpdC5leGUuIERvaSBjaHVu'
'ZyBkdW9uZzogZ2l0LmV4ZSBWQU4gcGhhaSBuaGFuLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3Jh'
'cnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICBmb3IgdGVuIGluICgiZ2l0'
'LmV4ZSIsICJnaXQuYmF0IiwgImdpdC5jbWQiLCAiZ2l0LnB5IiwgImtob25nLXBoYWktZ2l0LnR4dCIpOgogICAgICAgICAg'
'ICBmID0gZC90ZW47IGYud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8gPSBnb2ko'
'Y29uZ19jdV9naXQ9c3RyKGYpLCBwYXRoPSIiLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAg'
'ICAgICBrcVtmIkNPTkdfQ1VfR0lUPXt0ZW59Il0gPSAiTkhBTiIgaWYgciBlbHNlICJUVSBDSE9JIgogICAgbG90ID0gW2sg'
'Zm9yIGssIHYgaW4ga3EuaXRlbXMoKSBpZiB2ID09ICJOSEFOIiBhbmQgbm90IGsuZW5kc3dpdGgoImdpdC5leGUiKV0KICAg'
'IGlmIGtxLmdldCgiQ09OR19DVV9HSVQ9Z2l0LmV4ZSIpICE9ICJOSEFOIjoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNo'
'dW5nIGR1b25nIGhvbmc6IGdpdC5leGUgaG9wIGxlIG1hIGJpIHR1IGNob2kiLCBrcQogICAgcmV0dXJuIChEQVQgaWYgbm90'
'IGxvdCBlbHNlIFRSVU9UKSwgKCIiIGlmIG5vdCBsb3QgZWxzZSBmImNvbiBuaGFuOiB7bG90fSIpLCBrcQoKZGVmIGRvX245'
'KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIk11YyBQQVRIIGJvYyBuaGF5IGtlcCBwaGFpIE5IQU47IG11YyByb25nIC8gdG9h'
'biBraG9hbmcgdHJhbmcgcGhhaSBibyBxdWEsIGtob25nIG5lbS4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVtcGZpbGUu'
'VGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8iY28gZ2l0IjsgZC5ta2RpcigpOyBjdyA9'
'IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAgICAgKGQvImdp'
'dC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBmb3IgbmhhbiwgbXVjIGluICgoImto'
'b25nIG5oYXkiLCBzdHIoZCkpLCAoImNvIG5oYXkga2VwIiwgZicie2R9IicpLAogICAgICAgICAgICAgICAgICAgICAgICAg'
'ICgicm9uZyIsICIiKSwgKCJjaGkga2hvYW5nIHRyYW5nIiwgIiAgICIpKToKICAgICAgICAgICAgdHJ5OgogICAgICAgICAg'
'ICAgICAgciwgXyA9IGdvaShwYXRoPW11YywgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAg'
'ICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIk5vbmUiCiAgICAgICAgICAgIGV4Y2VwdCBF'
'eGNlcHRpb24gYXMgZToKICAgICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9IGYiTkVNIHt0eXBlKGUpLl9fbmFt'
'ZV9ffSIKICAgIGlmIGtxLmdldCgiUEFUSCBraG9uZyBuaGF5IikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJk'
'b2kgY2h1bmcgZHVvbmcgaG9uZzogbXVjIFBBVEggdGh1b25nIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EKICAgIG9r'
'ID0gKGtxLmdldCgiUEFUSCBjbyBuaGF5IGtlcCIpID09ICJOSEFOIgogICAgICAgICAgYW5kIGtxLmdldCgiUEFUSCByb25n'
'IikgPT0gIk5vbmUiIGFuZCBrcS5nZXQoIlBBVEggY2hpIGtob2FuZyB0cmFuZyIpID09ICJOb25lIikKICAgIHJldHVybiAo'
'REFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCiMgRGF1IHBoYW4gY2FjaCBk'
'dW5nIERFIFRIVS4gUGhhaSBLSEFDIG9zLnBhdGhzZXAgdHJlbiBDQSBIQUkgbmVuICgnOycgV2luZG93cywgJzonIFBPU0lY'
'KQojIHRoaSBoYWkgZ2lhIHRodXlldCAidGFjaCB0aGVvIGRhdSBkdW9jIHRydXllbiIgdmEgInRhY2ggdGhlbyBvcy5wYXRo'
'c2VwIiBtb2kgcm9pIHJhIG5oYXUuClRIVV9OMTAgPSAifCIKCmRlZiBkb19uMTAoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIi'
'SGFtIHBoYWkgdGFjaCBQQVRIIHRoZW8gZGF1IHBoYW4gY2FjaCBEVU9DIFRSVVlFTiwga2hvbmcgdGhlbyBvcy5wYXRoc2Vw'
'IGN1YSBuZW4uCgogICAgQmFuIGN1IGRvICJtb3QgZGF1ICc7JyB0cm9uZyBURU4gdGh1IG11YyIgdmEgZGF0IERBVCB0cmVu'
'IFdpbmRvd3MgZHUgaGFtIHNhaS4gTm8KICAgIGRlZ2VuZXJhdGU6IHRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7'
'JywgbmVuICdDOi9hO2InIHRoYXQgc3UgQ08gTkdISUEgbGEgaGFpCiAgICBtdWMg4oCUICJ0YWNoIGR1bmciIHZhICJ0YWNo'
'IHNhaSIgY2hvIHJhIGN1bmcga2V0IHF1YSwgcGhlcCBkbyBraG9uZyB0aGUgZG8gbmFvLiBObwogICAgZGEgY2hhbSBEQVQg'
'Y2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQgdGF0IGF5'
'LgogICAgTW90IGNvbmcga2hvbmcgdGhlIGRvIHRoaSBraG9uZyBwaGFpIGNvbmcuCiAgICAiIiIKICAgIHRlbl9zZXAgPSBu'
'ZXh0KChrIGZvciBrIGluICgicGhhbl9jYWNoIiwgImRhdV9waGFuX2NhY2giLCAic2VwIikgaWYgayBpbiBzaWcucGFyYW1l'
'dGVycyksIE5vbmUpCiAgICBpZiB0ZW5fc2VwIGlzIE5vbmU6CiAgICAgICAgIyBLaG9uZyBjbyB0aGFtIHNvIHRoaSB0cmVu'
'IFdpbmRvd3MgS0hPTkcgY29uIGR1b25nIG5hbyB0YWNoIGhhaSBnaWEgdGh1eWV0LgogICAgICAgIGlmIG9zLnBhdGhzZXAg'
'PT0gIjsiOgogICAgICAgICAgICByZXR1cm4gKEtERCwgInRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyB2YSBo'
'YW0ga2hvbmcgbmhhbiB0aGFtIHNvIGRhdSBwaGFuIGNhY2ggIgogICAgICAgICAgICAgICAgICAgICAgICAgIi0+IGtob25n'
'IHRhY2ggZHVvYyBoYWkgZ2lhIHRodXlldCIsCiAgICAgICAgICAgICAgICAgICAgeyJvcy5wYXRoc2VwIjogb3MucGF0aHNl'
'cCwgInRoYW0gc28gc2VwIjogTm9uZX0pCiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0'
'OgogICAgICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkKICAgICAgICAgICAgZCwgY3csIHBmID0g'
'X3Nhbih0KQogICAgICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAg'
'ICAgICAgICByLCBfICA9IGdvaShwYXRoPXN0cihsYSkgKyBvcy5wYXRoc2VwICsgc3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0'
'cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICByMCwgXyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1z'
'dHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICBrcSA9IHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNl'
'cCI6IE5vbmUsCiAgICAgICAgICAgICAgImNvIG11YyBjaHVhICc7JyI6ICJOSEFOIiBpZiByIGVsc2UgIk5vbmUiLAogICAg'
'ICAgICAgICAgICJkb2kgY2h1bmcgZHVvbmcgKGtob25nIGNvICc7JykiOiAiTkhBTiIgaWYgcjAgZWxzZSAiTm9uZSJ9CiAg'
'ICAgICAgaWYgbm90IHIwOgogICAgICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmciLCBrcQogICAg'
'ICAgIHJldHVybiAoREFUIGlmIHIgZWxzZSBUUlVPVCksICgiIiBpZiByIGVsc2UgIm11YyBnaXQuZXhlIGhvcCBsZSBiaSBN'
'QVQiKSwga3EKCiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgbGEgPSBQYXRo'
'KHQpLyJjbztkYXUiOyBsYS5ta2RpcigpICAgICAgICAgICMgJzsnIG5hbSB0cm9uZyBURU4sIGtob25nIHBoYWkgZGF1IHBo'
'YW4gY2FjaAogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngi'
'LCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIG5vaSA9IHN0cihsYSkgKyBUSFVfTjEwICsgc3RyKGQpCiAgICAgICAga3cg'
'PSBkaWN0KHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgcl9jaGluaCwgXyA9IGdvaShwYXRo'
'PW5vaSwgICAgICAqKnt0ZW5fc2VwOiBUSFVfTjEwfSwgICAqKmt3KSAgICMgdGFjaCBkdW5nICAtPiBOSEFOCiAgICAgICAg'
'cl9kdW9uZywgXyA9IGdvaShwYXRoPXN0cihkKSwgICAqKnt0ZW5fc2VwOiBUSFVfTjEwfSwgICAqKmt3KSAgICMgZG9pIGNo'
'dW5nIGR1b25nCiAgICAgICAgcl9waGFuYmlldCwgXyA9IGdvaShwYXRoPW5vaSwgICAqKnt0ZW5fc2VwOiBvcy5wYXRoc2Vw'
'fSwgKiprdykgICMgdGFjaCB0aGVvIG9zLnBhdGhzZXAgLT4gbWF0CiAgICBrcSA9IHsib3MucGF0aHNlcCI6IG9zLnBhdGhz'
'ZXAsICJ0aGFtIHNvIHNlcCI6IHRlbl9zZXAsICJkYXUgdGh1IjogVEhVX04xMCwKICAgICAgICAgIGYibm9pIGJhbmcge1RI'
'VV9OMTAhcn0sIHt0ZW5fc2VwfT17VEhVX04xMCFyfSI6ICAgICAgICJOSEFOIiBpZiByX2NoaW5oIGVsc2UgIk5vbmUiLAog'
'ICAgICAgICAgZiJkb2kgY2h1bmcgZHVvbmcgKG1vdCBtdWMsIHt0ZW5fc2VwfT17VEhVX04xMCFyfSkiOiAgIk5IQU4iIGlm'
'IHJfZHVvbmcgZWxzZSAiTm9uZSIsCiAgICAgICAgICBmInBoYW4gYmlldDogbm9pIGJhbmcge1RIVV9OMTAhcn0sIHt0ZW5f'
'c2VwfT17b3MucGF0aHNlcCFyfSI6ICJOSEFOIiBpZiByX3BoYW5iaWV0IGVsc2UgIk5vbmUifQogICAgaWYgbm90IHJfZHVv'
'bmc6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBtb3QgbXVjIGhvcCBsZSBtYSBraG9uZyB0'
'aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICAjIENvbmcgcGhhaSBDTyBUSEUgZG8uIE5ldSBjYSBoYWkgZGF1IHBoYW4gY2FjaCBk'
'ZXUgcmEgTkhBTiB0aGkgcGhlcCBkbyBraG9uZyBwaGFuCiAgICAjIGJpZXQgZHVvYyBnaSDigJQgZHVuZyBiYW8gREFULCBi'
'YW8gdGhhbmcgbGEga2hvbmcgZG8gZHVvYy4KICAgIGlmIHJfcGhhbmJpZXQ6CiAgICAgICAgcmV0dXJuIChLREQsIGYicGhl'
'cCBkbyBLSE9ORyBwaGFuIGJpZXQgZHVvYzogbm9pIGJhbmcge1RIVV9OMTAhcn0gbWEgdGFjaCB0aGVvICIKICAgICAgICAg'
'ICAgICAgICAgICAgZiJ7b3MucGF0aHNlcCFyfSBWQU4gdGltIHJhIGdpdC5leGUiLCBrcSkKICAgIHJldHVybiAoKERBVCwg'
'IiIsIGtxKSBpZiByX2NoaW5oIGVsc2UKICAgICAgICAgICAgKFRSVU9ULCBmInRhY2ggdGhlbyBvcy5wYXRoc2VwIHRoYXkg'
'dmkgdGhlbyB7dGVuX3NlcH0gZHVvYyB0cnV5ZW4iLCBrcSkpCgoKZGVmIGRvX24xMShnb2ksIHNpZywgdGVwdCk6CiAgICAi'
'IiJUcnV5ZW4gY2hhbl9kb2FuID0+IHRodSBkdW9jIHRob25nIGJhbyBWQSBzdGRlcnIgSU0uIEtob25nIHRydXllbiA9PiBz'
'dGRlcnIgVkFOIGNvLiIiIgogICAgaWYgImNoYW5fZG9hbiIgbm90IGluIHNpZy5wYXJhbWV0ZXJzOgogICAgICAgIHJldHVy'
'biBLREQsICJfZ2l0X3dpbmRvd3Mga2hvbmcgbmhhbiB0aGFtIHNvIGNoYW5fZG9hbiIsIHsidGhhbSBzbyI6IGxpc3Qoc2ln'
'LnBhcmFtZXRlcnMpfQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3'
'LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQog'
'ICAgICAgIGNkID0gW10KICAgICAgICBfLCBlX2NvID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiks'
'IGN3ZD1zdHIoY3cpLCBjaGFuX2RvYW49Y2QpCiAgICAgICAgXywgZV9raCA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9m'
'aWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIGtxID0geyJjaGFuX2RvYW4gdGh1IGR1b2MgKG11YykiOiBsZW4oY2Qp'
'LAogICAgICAgICAgInN0ZGVyciBraGkgQ08gY2hhbl9kb2FuIChieXRlKSI6IGxlbihlX2NvLmVuY29kZSgpKSwKICAgICAg'
'ICAgICJzdGRlcnIga2hpIEtIT05HIHRydXllbiAoYnl0ZSkiOiBsZW4oZV9raC5lbmNvZGUoKSl9CiAgICBpZiBsZW4oY2Qp'
'ID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA9PSAwOgogICAgICAgIHJldHVybiBLREQsICJuaGFuaCAlUHJvZ3JhbUZp'
'bGVzJSBraG9uZyBwaGFuIGdpYWkgS0hPTkcgYmF5IHJhIGNoYW4gZG9hbiBuYW8gLT4gY2h1YSBkbyBkdW9jIiwga3EKICAg'
'IG9rID0gbGVuKGNkKSA+IDAgYW5kIGxlbihlX2NvLmVuY29kZSgpKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPiAw'
'CiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgpkZWYg'
'ZG9fbjEyKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkhhbmcgc2VudGluZWwgZ2l0X3BhdGggdHJvbmcgZml4dHVyZSBwaGFp'
'IHR1eWV0IGRvaSB0cmVuIENBIEhBSSBuZW4uIiIiCiAgICBuZCA9IHRlcHQucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIs'
'IGVycm9ycz0icmVwbGFjZSIpCiAgICBoYW5nID0gc29ydGVkKHNldChyZS5maW5kYWxsKHInZ2l0X3BhdGhccyo9XHMqIihb'
'XiJdKykiJywgbmQpKSkKICAgIHhhdSA9IFtoIGZvciBoIGluIGhhbmcgaWYgbm90IChQdXJlUG9zaXhQYXRoKGgpLmlzX2Fi'
'c29sdXRlKCkgYW5kIFB1cmVXaW5kb3dzUGF0aChoKS5pc19hYnNvbHV0ZSgpKV0KICAgIGtxID0geyJoYW5nIGdpdF9wYXRo'
'IHRpbSB0aGF5IjogaGFuZywgImNoaSB0dXlldCBkb2kgTU9UIG5lbiI6IHhhdX0KICAgIGlmIG5vdCBoYW5nOgogICAgICAg'
'IHJldHVybiBLREQsICJraG9uZyB0aW0gdGhheSBoYW5nIGdpdF9wYXRoIG5hbyB0cm9uZyBmaXh0dXJlIC0+IG1hdSBkb2Mg'
'Y28gdGhlIGRhIGRvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgeGF1IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IHhh'
'dSBlbHNlIGYiY2hpLW1vdC1uZW46IHt4YXV9IiksIGtxCgpQUk9CRSA9IFsoIk44IGJ1b2MgMSBjaGkgbmhhbiBnaXQuZXhl'
'IiwgZG9fbjgpLAogICAgICAgICAoIk45IGJvYyBuaGF5IGtlcCBvIG11YyBQQVRIIiwgZG9fbjkpLAogICAgICAgICAoIk4x'
'MCBkYXUgJzsnIHRyb25nIHRlbiB0aHUgbXVjIiwgZG9fbjEwKSwKICAgICAgICAgKCJOMTEgY2hhbiBkb2FuIGRvaSBrZW5o'
'IiwgZG9fbjExKSwKICAgICAgICAgKCJOMTIgaGFuZyBzZW50aW5lbCB0dXlldCBkb2kgQ0EgSEFJIG5lbiIsIGRvX24xMild'
'CgojIC0tLSBjaGUgZG8gVFUgS0lFTTogY2hheSBuYW0gcHJvYmUgdHJlbiBtb3QgY2F5IGJhdCBreSwgbmVuIGJhdCBreSAt'
'LS0KaWYgIi0tdHUta2llbS1wcm9iZSIgaW4gc3lzLmFyZ3Y6CiAgICBfZyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5k'
'ZXgoIi0tdHUta2llbS1wcm9iZSIpICsgMV0pLnJlc29sdmUoKQogICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9t'
'X2ZpbGVfbG9jYXRpb24oImxwX3RrIiwgc3RyKF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICBfbHAgPSBpbXBv'
'cnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX2xwKQogICAgX3NpZyA9'
'IGluc3BlY3Quc2lnbmF0dXJlKF9scC5fZ2l0X3dpbmRvd3MpCiAgICBkZWYgX2dvaSgqKmt3KToKICAgICAgICBlID0gaW8u'
'U3RyaW5nSU8oKQogICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgICAgIHJldHVy'
'biBfbHAuX2dpdF93aW5kb3dzKCoqa3cpLCBlLmdldHZhbHVlKCkKICAgIHByaW50KGYiVFUgS0lFTSBQUk9CRSB0cmVuIHtf'
'Z30gIChuZW4ge3N5cy5wbGF0Zm9ybX0pIikKICAgIGZvciBfdGVuLCBfZiBpbiBQUk9CRToKICAgICAgICBfdHQsIF9jdCwg'
'X2RsID0gX2YoX2dvaSwgX3NpZywgX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcHJpbnQoZiIg'
'IFt7X3R0OjE0fV0ge190ZW59IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICAgICAgZm9yIF9rLCBfdiBp'
'biAoX2RsIG9yIHt9KS5pdGVtcygpOiBwcmludChmIiAgICAgICAge19rOjM0fToge192fSIpCiAgICBzeXMuZXhpdCgwKQoK'
'IyAtLS0gY2hlIGRvIEtJRU0gRE9ORyBCTzogdGVwIC5weSBuYXkgcGhhaSBUUlVORyBUVU5HIEJZVEUgdm9pIGJhbiBuaHVu'
'ZyB0cm9uZyBwczEgLS0tCiMgS2hvbmcgY29uZyBuYW8gYnVvYyBoYWkgYmFuIHNhbyBraG9wOiBkbyBkdW9jLCBub2kgdHJh'
'biAyLzQwMCAtPiA5OS85OTk5OSBDSEkgdHJvbmcgLnB5CiMgdGhpIGNpX2Rhbmdfa3kgbGFuIHQyNi90MjcgdmFuIHhhbmgs'
'IGNvbiBjaG90IFNIQSBjdWEgcHMxIGNoaSBzbyBiYW4gbmh1bmcgdm9pIGhhbmcgc28KIyBjdWEgQ0hJTkggbm8uIENoYXk6'
'IHB5dGhvbiB3cDU0MS1kby1nMi13aW5kb3dzLnB5IC0ta2llbS1kb25nLWJvIHdwNTQxLWRvLWcyLnBzMSAgKHJjIDB8MykK'
'aWYgIi0ta2llbS1kb25nLWJvIiBpbiBzeXMuYXJndjoKICAgIGltcG9ydCBiYXNlNjQKICAgIF9wcyA9IFBhdGgoc3lzLmFy'
'Z3Zbc3lzLmFyZ3YuaW5kZXgoIi0ta2llbS1kb25nLWJvIikgKyAxXSkucmVhZF90ZXh0KGVuY29kaW5nPSJhc2NpaSIpCiAg'
'ICBfbSA9IHJlLnNlYXJjaChyIig/bXMpXlwkQjY0ID0gQFwoKC4qPyleXCkiLCBfcHMpCiAgICBfayA9IHJlLnNlYXJjaChy'
'Iig/bSleXCRTaGFCb0RvXHMqPVxzKicoWzAtOWEtZl17NjR9KSciLCBfcHMpCiAgICBfbmh1bmcgPSBiYXNlNjQuYjY0ZGVj'
'b2RlKCIiLmpvaW4ocmUuZmluZGFsbChyIicoW0EtWmEtejAtOSsvPV0qKSciLCBfbS5ncm91cCgxKSkpKSBpZiBfbSBlbHNl'
'IGIiIgogICAgX3RvaSA9IFBhdGgoX19maWxlX18pLnJlYWRfYnl0ZXMoKQogICAgX29rID0gYm9vbChfbSBhbmQgX2spIGFu'
'ZCBfbmh1bmcgPT0gX3RvaSBhbmQgaGFzaGxpYi5zaGEyNTYoX3RvaSkuaGV4ZGlnZXN0KCkgPT0gX2suZ3JvdXAoMSkKICAg'
'IGlubihmIktJRU0gRE9ORyBCTzoge0RBVCBpZiBfb2sgZWxzZSBLRER9ICAobmh1bmcge2xlbihfbmh1bmcpfSBieXRlLCB0'
'ZXAge2xlbihfdG9pKX0gYnl0ZSkiKQogICAgc3lzLmV4aXQoMCBpZiBfb2sgZWxzZSAzKQoKaW5uKCI9IiAqIDc4KTsgaW5u'
'KCJXUDU0MSBnMiAtIHBoZXAgZG8gdHJlbiBXaW5kb3dzIHRoYXQgKHNwZWMgcjM6IE4xLU40LCBOOC1OMTIsIE43LCBraWNo'
'IHRodW9jKSIpOyBpbm4oIj0iICogNzgpCgojIC0tLS0tLS0tLS0tLS0tLS0gdHUga2llbSBibyBkb2MgLS0tLS0tLS0tLS0t'
'LS0tLQpfZCwgX2csIF90ID0gZG9jX2RvKF9NQVUpCl9vayA9IChsZW4oX2QpID09IDIgYW5kIGFueSh4LnN0YXJ0c3dpdGgo'
'InQwMmIiKSBmb3IgeCBpbiBfZCkKICAgICAgIGFuZCBub3QgYW55KHguc3RhcnRzd2l0aCgidDEzMSIpIGZvciB4IGluIF9k'
'KSBhbmQgX3QpCmlubigiVHUga2llbSBibyBkb2MgbG9nOiIsIERBVCBpZiBfb2sgZWxzZSBUUlVPVCkKaWYgbm90IF9vazoK'
'ICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogYm8gZG9jIGxvZyBjdWEgY2hpbmggc2NyaXB0IG5heSBzYWkgLT4g'
'a2hvbmcgZG8gZ2kgY2EuIik7IHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMC4gbmVuIGRvIC0tLS0tLS0tLS0t'
'LS0tLS0KZ29jID0gUGF0aChzeXMuYXJndlsxXSkucmVzb2x2ZSgpIGlmIGxlbihzeXMuYXJndikgPiAxIGVsc2UgUGF0aC5j'
'd2QoKQp0ZXAsIHRlcHQgPSBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoLnB5IiwgZ29jIC8gIm9wcyIgLyAibGVhc2Vf'
'cHVibGlzaF90ZXN0LnB5Igppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjAuIE5FTiBETyIpCiMgTU9JIExPRyBQSEFJ'
'IFRVIEtIQUkgbm8gZG8gQ0FJIEdJIGJhbmcgQk8gRE8gTkFPLiBCYWkgaG9jIDE5LTA5LTIwMjY6IG1vdCBsdW90IGRvCiMg'
'Z3VpIHZlIGR1b2MgZG9jIG5odSBrZXQgcXVhIGN1YSBiYW4gdmEgZGFuZyB4ZXQsIG5odW5nIHRoYXQgcmEgbGEgYmFuIGRv'
'IENVIGNoYXkKIyB0cmVuIG5oYW5oIEtIQUMuIERvYyByYSB0aGkgbWF0IG1vdCB2b25nOyBsb2cgdHUga2hhaSB0aGkgdGhh'
'eSBuZ2F5IGRvbmcgZGF1Lgp0cnk6CiAgICBfdHUgPSBoYXNobGliLnNoYTI1NihQYXRoKF9fZmlsZV9fKS5yZWFkX2J5dGVz'
'KCkpLmhleGRpZ2VzdCgpCmV4Y2VwdCBFeGNlcHRpb24gYXMgX2U6CiAgICBfdHUgPSBmImtob25nIHR1IGJhbSBkdW9jOiB7'
'X2V9IgpnaGkoImJvX2RvX3NoYTI1NiIsIF90dSkKaW5uKGYiICBCTyBETyAgICAgICAgOiBzaGEyNTYge190dVs6MTZdfSAg'
'KGJhbiB7QkFOX0JPX0RPfSkiKQppbm4oIiAgc3lzLnBsYXRmb3JtIDoiLCBzeXMucGxhdGZvcm0sICJ8IHB5dGhvbiIsIHN5'
'cy52ZXJzaW9uLnNwbGl0KClbMF0pCmlubigiICBvcy5wYXRoc2VwICAgOiIsIHJlcHIob3MucGF0aHNlcCksICJ8IFBBVEhF'
'WFQ6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUEFUSEVYVCIpKVs6NjBdKQppbm4oIiAgUHJvZ3JhbUZpbGVzIDoiLCByZXBy'
'KG9zLmVudmlyb24uZ2V0KCJQcm9ncmFtRmlsZXMiKSksICJ8IFN5c3RlbVJvb3Q6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgi'
'U3lzdGVtUm9vdCIpKSkKaW5uKCIgIENPTkdfQ1VfR0lUICA6IiwgcmVwcihfQ09OR19DVV9HSVRfTkdVT0lfRE8pCiAgICAr'
'ICgiICAtPiBEQSBCTyBraG9pIGx1b3QgZG8gKENJIGtob25nIGRhdCBiaWVuIG5heTsgeGVtIGRhdSB0ZXApIiBpZiBfQ09O'
'R19DVV9HSVRfTkdVT0lfRE8gaXMgbm90IE5vbmUgZWxzZSAiIikpCmdoaSgiY29uZ19jdV9naXRfbmd1b2lfZG8iLCBfQ09O'
'R19DVV9HSVRfTkdVT0lfRE8pCmlubigiICBnb2Mga2hvICAgICAgOiIsIGdvYykKCnF1eWVuID0gTm9uZQppZiBzeXMucGxh'
'dGZvcm0gPT0gIndpbjMyIjoKICAgIHRyeToKICAgICAgICBpbXBvcnQgY3R5cGVzOyBxdXllbiA9IGJvb2woY3R5cGVzLndp'
'bmRsbC5zaGVsbDMyLklzVXNlckFuQWRtaW4oKSkKICAgIGV4Y2VwdCBFeGNlcHRpb246IHF1eWVuID0gTm9uZQpnaGkoInF1'
'eWVuX2FkbWluIiwgcXV5ZW4pCnN5bWxpbmtfZHVvYyA9IE5vbmUKdHJ5OgogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlE'
'aXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJhLnR4dCI7IGQud3JpdGVfdGV4dCgieCIsIGVuY29kaW5n'
'PSJ1dGYtOCIpCiAgICAgICAgdHJ5OiBvcy5zeW1saW5rKHN0cihkKSwgc3RyKFBhdGgodCkvImxrIikpOyBzeW1saW5rX2R1'
'b2MgPSBUcnVlCiAgICAgICAgZXhjZXB0IE9TRXJyb3IgYXMgZTogc3ltbGlua19kdW9jID0gRmFsc2U7IGdoaSgic3ltbGlu'
'a19sb2kiLCBmInt0eXBlKGUpLl9fbmFtZV9ffToge2V9IikKZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOiBnaGkoInN5bWxpbmtf'
'bG9pIiwgc3RyKGUpKQpnaGkoInN5bWxpbmtfZHVvYyIsIHN5bWxpbmtfZHVvYykKaW5uKCIgIEFkbWluaXN0cmF0b3I6Iiwg'
'cXV5ZW4sICJ8IHRhbyBzeW1saW5rIGR1b2M6Iiwgc3ltbGlua19kdW9jKQoKbG9pID0gW10KIyBDb25nIGtpY2ggdGh1b2Mg'
'bGEgcGhlcCBkbyB0cmVuIExJQ0ggU1UgR0lULCBraG9uZyBkaW5oIGdpIGRlbiBuZW4uIENobyBwaGVwCiMgLS1jaGkta2lj'
'aC10aHVvYyBjaGF5IG8gbW9pIG5lbiBkZSBjb24gVFUgS0lFTSBkdW9jIGNoaW5oIGNvbmcgbmF5IChkYSBkdW5nCiMgZGUg'
'dGFpIGR1bmcgY2EgaGFpIHZlIGN1YSBzdSBjbyBuZW4tY3UgMTktMDkpLiBNb2kgY2hvdCBDSFVDIE5BTkcgdmFuIGRvaSBX'
'aW5kb3dzLgppZiBzeXMucGxhdGZvcm0gIT0gIndpbjMyIiBhbmQgIi0tY2hpLWtpY2gtdGh1b2MiIG5vdCBpbiBzeXMuYXJn'
'djoKICAgIGxvaS5hcHBlbmQoZiJLSE9ORyBwaGFpIFdpbmRvd3MgKHN5cy5wbGF0Zm9ybT17c3lzLnBsYXRmb3JtIXJ9KSIp'
'CmlmIG5vdCB0ZXAuaXNfZmlsZSgpOiAgbG9pLmFwcGVuZChmImtob25nIHRoYXkge3RlcH0iKQppZiBub3QgdGVwdC5pc19m'
'aWxlKCk6IGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB0fSIpCmlmIG5vdCBzaHV0aWwud2hpY2goImdpdCIpOiBsb2ku'
'YXBwZW5kKCJraG9uZyBjbyBgZ2l0YCB0cm9uZyBQQVRIIikKIyBCbyB0ZXN0IChtdWMgMiB2YSBONykgY2FuIFB5WUFNTDog'
'dGhpZXUgbm8sIDBlYTk1ZGUgcmEgOTYvMTY2IGNhIERPICg4OSBiYW8gdGhhbmcgIk5vIG1vZHVsZSBuYW1lZCAneWFtbCci'
'LAojIDcgcXVhIGx1b3QgY29uOyBjbyBQeVlBTUw6IDE2Ni8xNjYgUVVBKS4gQm8gZG8gZ29pIGNodW5nIGxhICJjYSBETyBM'
'QSIgcm9pIHBoYXQgVFJVT1Qg4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGMuCiMgRGlldSBraWVuIHRpZW4gcXV5ZXQgcGhhaSBo'
'b2kgYmFuZyBDSElOSCB0aWVuIHRyaW5oIGNvbiBzZSBjaGF5IGJvIHRlc3QgKGNoYXkoKTogY3VuZyBtb2kgdHJ1b25nOyBj'
'd2QgPSBvcHMvID0KIyBzeXMucGF0aFswXSBjdWEgYm8gdGVzdCkgdmEgaG9pIERVTkcgRFVPQyBjaHUga2hvbmcgaG9pIENP'
'IE1BVC4gQmFuIDMwZCBob2kgYGZpbmRfc3BlYygieWFtbCIpYCBvIHRpZW4gdHJpbmgKIyBOQVkgdmEgbmd1b25nIDMuOCBz'
'dXkgdHUgTkdVIFBIQVAgKGA6PWApIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBkLCBjYSBoYWkgcmEgcmM9MSBUUlVPVCBjaG8g'
'dW5nIHZpZW4gc2FjaDoKIyB0aHUgbXVjIGR1IGxpZXUgYHlhbWwvYCB0cmVuIFBZVEhPTlBBVEggcXVhIGZpbmRfc3BlYyBt'
'YSBgeWFtbC5zYWZlX2R1bXBgIGtob25nIGNvICg4NyBjYSAibGEiKTsgcHl0aG9uIDMuOC4yMAojIFRIQVQgY28gUHlZQU1M'
'LCBibyB0ZXN0IGR1bmcgYHN0ci5yZW1vdmVwcmVmaXhgICgzLjkpIGx1YyBDSEFZICgzMyBjYSAibGEiOyAzLjkuMjM6IDE2'
'Ni8xNjYpLgojICJEdW5nIGR1b2MiIG5naGlhIGxhIGR1bmcgRFVORyBBUEkgYm8gdGVzdCBnb2k6IHZpZXQoKSAoNDMgbG9p'
'IGdvaSkgdmEgbGVhc2VfcHVibGlzaC5weSBnb2kgc2FmZV9kdW1wKC4uLiwgYWxsb3dfdW5pY29kZT1UcnVlLAojIHNvcnRf'
'a2V5cz1GYWxzZSksIG1hIGBzb3J0X2tleXNgIGNoaSBjbyB0dSBQeVlBTUwgNS4xLiBEbyB0cmVuIDIwMjYtMDktMzBsLCAw'
'ZWE5NWRlOiBweXRob24gMy45LjIzICsgUHlZQU1MIDMuMTMgVEhBVCBxdWEgcHJvYmUKIyBjdSAocmM9MCksIGJvIHRlc3Qg'
'MTA5LzE2NiDigJQgNTYgY2EgImxhIjogNTIgYHVuZXhwZWN0ZWQga2V5d29yZCBhcmd1bWVudCAnc29ydF9rZXlzJ2AsIHQy'
'Ni90MjcgYFJlYWRlckVycm9yYCAoa3kgdHUgbmdvYWkgQk1QKSwKIyB0MTI0L3QxNTMgRE8gdGhlbyBsdW90IGNvbiDigJQg'
'ZTJlIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgOyBQeVlBTUwgNS4xOiAxNjYvMTY2IChkbyBsYWkgMjAyNi0xMC0wMTogY3Vu'
'ZyBzbykuCiMgKFB5dGhvbiA+PSAzLjEwICsgUHlZQU1MIDMuMTMgZGEgdHJ1b3QgcHJvYmUgY3UgdmkgYGNvbGxlY3Rpb25z'
'Lkhhc2hhYmxlYC4pIFByb2JlIGN1YSBwczEgKCRtYVRodSkgcGhhaSBHSU9ORyBIRVQgZG9uZyBkdW9pLgppZiBub3QgKCIt'
'LWNoaS1raWNoLXRodW9jIiBpbiBzeXMuYXJndiBvciAiLS1jaGktcHJvYmUiIGluIHN5cy5hcmd2KToKICAgIF9yY19kaywg'
'X3JhX2RrID0gY2hheShbIi1jIiwgImltcG9ydCBzeXM7IHN5cy5leGl0KDkpIGlmIHN5cy52ZXJzaW9uX2luZm8gPCAoMywg'
'OSkgZWxzZSBOb25lOyBpbXBvcnQgeWFtbDsiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgeWFtbC5zYWZl'
'X2R1bXAoeWFtbC5zYWZlX2xvYWQoJ2E6IDEnKSwgYWxsb3dfdW5pY29kZT1UcnVlLCBzb3J0X2tleXM9RmFsc2UpIl0sCiAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgZ29jIC8gIm9wcyIgaWYgKGdvYyAvICJvcHMiKS5pc19kaXIoKSBlbHNlIFBhdGgu'
'Y3dkKCksIHBodXQ9MikKICAgIGlmIF9yY19kayA9PSA5OgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24ge3N5cy52ZXJz'
'aW9uLnNwbGl0KClbMF19IDwgMy45OiBibyB0ZXN0IGN1YSB1bmcgdmllbiBkdW5nIHN0ci5yZW1vdmVwcmVmaXggKDMuOSkg'
'bHVjIENIQVkiKQogICAgZWxpZiBfcmNfZGs6CiAgICAgICAgbG9pLmFwcGVuZChmInB5dGhvbiBuYXkgS0hPTkcgY28gUHlZ'
'QU1MIGR1bmcgZHVvYyAoeyhfcmFfZGsuc3RyaXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFdWzo5MF19KToiCiAgICAg'
'ICAgICAgICAgICAgICBmIiBcIntzeXMuZXhlY3V0YWJsZX1cIiAtbSBwaXAgaW5zdGFsbCAtVSBweXlhbWwiCiAgICAgICAg'
'ICAgICAgICAgICAiIChiYW4gbmh1bmcgcHMxIHR1IHRhaSBLSE9ORyBjbyBwaXA6IGNoYXkgbGFpIHZvaSAtUHkgPHB5dGhv'
'biBkYSBjbyBQeVlBTUw+KSIpCiAgICAjIEJvIHRlc3QgY29uIGdvaSBgc2h1dGlsLndoaWNoYCBjaG8gYmFzaC9hY3Rpb25s'
'aW50L3NoZWxsY2hlY2sgKDBlYTk1ZGU6IHQzMyB0MTM3IHQxNTkgY2FuIGFjdGlvbmxpbnQsIHQxMzcgY2FuCiAgICAjIHNo'
'ZWxsY2hlY2ssIGNhYyBjYSBjaGF5IG9wcy9jYWlfYWN0aW9ubGludC5zaCBjYW4gYmFzaCkuIFRoaWV1IHRoaSBjYWMgY2Eg'
'YXkgaW4gIktIT05HIERPIERVT0M6IHRoaWV1IGAuLi5gIiB2YSBibyBkbyByYQogICAgIyByYz0zIOKAlCBuaHVuZyBjaGkg'
'U0FVIGNhIGJvIHRlc3QgbGFuIE43IChkbyB0cmVuIDIwMjYtMDktMzBnLCBQQVRIIHRoaWV1IGFjdGlvbmxpbnQ6IGBDb25n'
'IGN1IGRheSBkdSBkZSBkb2AgS0RELCByYz0zCiAgICAjIHNhdSAyIGx1b3QgYm8gdGVzdCkuIEN1bmcgbHkgZG8gUHlZQU1M'
'IGR1b2MgaG9pIG8gZGF5OiBob2kgVFJVT0MsIGN1bmcgUEFUSCBtYSBjaGF5KCkgdHJ1eWVuIGNobyBibyB0ZXN0LgogICAg'
'IyBWQSBjdW5nIENITyBibyB0ZXN0IGR1bmc6IHRyZW4gV2luZG93cyBgc2h1dGlsLndoaWNoYCB0cmEgVEhVIE1VQyBISUVO'
'IEhBTkggVFJVT0MgUEFUSCwgbWEgYm8gdGVzdCBjaGF5IHZvaSBjd2QgPSBnb2MgY29uCiAgICAjIHRpZW4gdHJpbmggbmF5'
'IGR1bmcgbyBjd2QgQ1VBIE5HVU9JIERPIChub2kgZ29pIHBzMSwgdmQuIERvd25sb2FkcyDigJQgZHVuZyBub2kgZ2lhaSBu'
'ZW4gYWN0aW9ubGludC5leGUpLiBEbyB0cmVuIDIwMjYtMDktMzBrCiAgICAjIChuaGFuaCB3aW4zMiBUSEFUIGN1YSBzaHV0'
'aWwud2hpY2gpOiBhY3Rpb25saW50IHRvdCBvIGN3ZCBuZ3VvaSBkbyArIGJhbiBob25nIGRhdSBQQVRIID0+IG11YyAwIGhv'
'aSBiYW4gbyBjd2QgKHJjPTApLCBibyB0ZXN0CiAgICAjIGR1bmcgYmFuIHRyZW4gUEFUSCA9PiByYz0xIGBEQVQgMTEgfCBU'
'UlVPVCAxYCwgYGxhOiBbJ3QzMycsICd0MTM3JywgJ3QxNTknXWAuIEdpYWkgdGVuIHZvaSBjd2QgPSBnb2Mgcm9pIGdvaSBU'
'SEFORyBiYW5nIGR1b25nCiAgICAjIFRVWUVUIERPSSBkYSBnaWFpIChxdWEgaGFuIHRoaSBydW4oKSBnaWV0IGR1bmcgdGll'
'biB0cmluaCDigJQgbHkgZG8gYmFuIDMwaSBraG9uZyBob2kgcXVhIGNoYXkoKSkuCiAgICBfY3dkX25ndW9pX2RvID0gb3Mu'
'Z2V0Y3dkKCkKICAgIHRyeToKICAgICAgICBpZiBnb2MuaXNfZGlyKCk6IG9zLmNoZGlyKGdvYykKICAgICAgICBfY2MgPSB7'
'YzogKG9zLnBhdGguYWJzcGF0aChwKSBpZiBwIGVsc2UgTm9uZSkgZm9yIGMsIHAgaW4KICAgICAgICAgICAgICAgKChjLCBz'
'aHV0aWwud2hpY2goYykpIGZvciBjIGluICgiYmFzaCIsICJhY3Rpb25saW50IiwgInNoZWxsY2hlY2siKSl9CiAgICBmaW5h'
'bGx5OgogICAgICAgIG9zLmNoZGlyKF9jd2Rfbmd1b2lfZG8pCiAgICBfdGhpZXVfY2MgPSBbYyBmb3IgYywgcCBpbiBfY2Mu'
'aXRlbXMoKSBpZiBub3QgcF0KICAgIGlmIF90aGlldV9jYzoKICAgICAgICBsb2kuYXBwZW5kKGYidGhpZXUgY29uZyBjdSBi'
'byB0ZXN0IGdvaSBxdWEgUEFUSDoge190aGlldV9jY30gKGFjdGlvbmxpbnQ6IG9wcy9jYWlfYWN0aW9ubGludC5zaCB2b2kg'
'QUxfVkVSOyIKICAgICAgICAgICAgICAgICAgICIgYmFzaDogR2l0IEJhc2gsIGtob25nIHBoYWkgYmFzaC5leGUgY3VhIFdT'
'TCkiKQogICAgIyBzaGVsbGNoZWNrIEtIT05HIG5oYW4gLS1ub3JjIHRoaSBhY3Rpb25saW50IDEuNy43ICh0dSB0cnV5ZW4g'
'LS1ub3JjKSBsYW0gdDMzIERPLCB2YSBTSEVMTENIRUNLX09QVFM9LS1ub3JjIGN1YSBjaGF5KCkgbGFtCiAgICAjIHQxMzcg'
'RE8g4oCUIGNhICJsYSIgPT4gVFJVT1QgZ2lhIChkbyB0cmVuIDIwMjYtMDktMzBoLCBzaGVsbGNoZWNrIGdpYSB0dSBjaG9p'
'IC0tbm9yYzogYmFuIDMwaCByYz0xIGBsYTogWyd0MzMnXWAgc2F1IGNhCiAgICAjIGJvIHRlc3QpLiBgd2hpY2hgIGNoaSBo'
'b2kgQ08gTUFUOyBvIGRheSBob2kgRFVORyBEVU9DLiBOZ3VvbmcgZG8gdHJlbiBzaGVsbGNoZWNrIFRIQVQ6IDAuNC43LzAu'
'NS4wLzAuNi4wIHR1IGNob2kgLS1ub3JjCiAgICAjIChyYz0zKSwgMC43LjAgdHJvIGxlbiBuaGFuLiBQaGVwIGhvaSBwaGFp'
'IHRoYXkgRFVORyBTSEVMTENIRUNLX09QVFMgbWEgY2hheSgpIGRhdCBjaG8gbHVvdCBjb246IGJhbiAzMGkgaG9pIHZvaSBi'
'aWVuIENVQQogICAgIyBOR1VPSSBETyDigJQgZG8gdHJlbiAyMDI2LTA5LTMwaSwgc2hlbGxjaGVjayAwLjkuMCArIFNIRUxM'
'Q0hFQ0tfT1BUUz0tLWV4dGVuZGVkLWFuYWx5c2lzPXRydWUgKGNvIGN1YSAwLjEwKTogcmM9MyAia2hvbmcgbmhhbgogICAg'
'IyAtLW5vcmM6IGNhcCBuaGF0IHNoZWxsY2hlY2siIHRyb25nIGtoaSB0MzMvdDEzNyBxdWEgY2hheSgpIGRldSAxLzEuIEdv'
'aSBUSEFORyAoa2hvbmcgcXVhIGNoYXkoKSk6IHF1YSBoYW4gdGhpIHJ1bigpIGdpZXQKICAgICMgZHVuZyBzaGVsbGNoZWNr'
'OyBxdWEgY2hheSgpIHRoaSBjaGkgZ2lldCBweXRob24gY29uLCBzaGVsbGNoZWNrIHRyZW8gbyBsYWkgbW8gY29pIChkbyB0'
'cmVuIDIwMjYtMDktMzBpOiAxLzEgY29uIHNvbmcpLgogICAgZWxpZiBzdWJwcm9jZXNzLnJ1bihbX2NjWyJzaGVsbGNoZWNr'
'Il0sICItLW5vcmMiLCAiLS12ZXJzaW9uIl0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRpbWVvdXQ9NjAsCiAgICAgICAgICAg'
'ICAgICAgICAgICAgIGVudj1kaWN0KG9zLmVudmlyb24sIFNIRUxMQ0hFQ0tfT1BUUz0iLS1ub3JjIikpLnJldHVybmNvZGU6'
'CiAgICAgICAgbG9pLmFwcGVuZCgic2hlbGxjaGVjayB0cmVuIFBBVEgga2hvbmcgbmhhbiAtLW5vcmMgKGFjdGlvbmxpbnQg'
'MS43LjcgdmEgY2hheSgpIGRldSB0cnV5ZW4gY28gYXkpOiBjYXAgbmhhdCBzaGVsbGNoZWNrIikKICAgICMgYWN0aW9ubGlu'
'dCBjdW5nIHBoYWkgRFVORyBEVU9DLCBraG9uZyBjaGkgQ08gTUFUOiB0MzMvdDEzNy90MTU5IGdvaSBubyBUSEFORywgdmEg'
'bW90IGFjdGlvbmxpbnQga2hvbmcgY2hheSAoc2FpIGtpZW4gdHJ1YywKICAgICMgaG9uZykgbGFtIGNhIGJhIERPICJhY3Rp'
'b25saW50IERPIChyYz0uLi4pIiDigJQgY2EgImxhIiA9PiBUUlVPVCBnaWEgc2F1IGNhIGJvIHRlc3QgKGRvIHRyZW4gMjAy'
'Ni0wOS0zMGo6IGFjdGlvbmxpbnQgZ2lhCiAgICAjIHJjPTEgPT4gbXVjIDAgaW0gbGFuZywgdDMzICJsYSIpLiBCYW4gVEhB'
'VCAxLjYuMjcvMS43LjcvMS43LjgvMS43LjEyIGRldSByYz0wIHZhIGRldSBjaG8gdDMzL3QxMzcvdDE1OSBRVUEgdHJlbiAw'
'ZWE5NWRlLgogICAgIyBiYXNoIHF1YSBgd2hpY2hgIENISSBob2kgQ08gTUFULCBjbyBjaHUgZGljaDogdDM1LXQ0MCBnb2kg'
'YGJhc2hgIFRSQU4gKGJhc2ggV1NMIGxhbSBjaHVuZyBETywgZGV1IE5HT0FJX1BIQU1fVkkg4oCUIGRvIHRyZW4KICAgICMg'
'MjAyNi0wOS0zMGopLiA5IGNhIFRST05HIHBoYW0gdmkgS0hPTkcgZ29pIGJhc2ggcXVhIGB3aGljaGAg4oCUIHhlbSBjaG90'
'IGBfYmFzaF9wb3NpeCgpYCBkdW9pIGNob3QgZ2l0LgogICAgIyBDSEFZIERVT0MgY2h1YSBwaGFpIERVTkcgRFVPQzogZG8g'
'dHJlbiAyMDI2LTA5LTMwaywgMGVhOTVkZSwgYWN0aW9ubGludCBUSEFUIDEuNC4zLzEuNS4wLzEuNS4zLzEuNi4wLzEuNi44'
'LzEuNi4xNS8xLjYuMjAvCiAgICAjIDEuNi4yMiBkZXUgYC12ZXJzaW9uYCByYz0wLCBtYSBjYSB0YW0gbGFtIHQxMzcvdDE1'
'OSBETyAoYHByb3BlcnR5ICJydW5fYXR0ZW1wdCIvIndvcmtmbG93X3NoYSIgaXMgbm90IGRlZmluZWRgKSwgMS40LjMvMS41'
'LjAKICAgICMgdGhlbSB0MzMgKGBtdXN0IGJlIGNvbnRhaW5lZCB3aXRoaW4gJHt7IH19YCkg4oCUIGUyZSAxLjYuMjI6IHJj'
'PTEgYERBVCAxMSB8IFRSVU9UIDFgLCBgbGE6IFsndDEzNycsICd0MTU5J11gIGNobyB1bmcgdmllbgogICAgIyBzYWNoOyAx'
'LjYuMjMvMS42LjI0LzEuNi4yNi8xLjYuMjcvMS43LjAvMS43LjYvMS43LjcvMS43LjEyIFFVQSBjYSBiYS4gU2FuIGxhIGJh'
'bgogICAgIyBnaGltIENJIChBTF9TQU4pLCBLSE9ORyBwaGFpIDEuNi4yMyBkbyB0cmVuIE1PVCB1bmcgdmllbjogd29ya2Zs'
'b3cgY3VhIHVuZyB2aWVuIHNhdSBjbyB0aGUgZHVuZyBjdSBwaGFwIG1vaSBob24sIG1hIENJIGNoaSBkbwogICAgIyBiYW5n'
'IGJhbiBnaGltLiBDdSBob24gc2FuID0+IEtIT05HIERPIERVT0MgKGNoYW4gY2EgMS42LjIzLTEuNy42IGRhbmcgUVVBOiBm'
'YWlsLWNsb3NlLCBraG9uZyBwaGFpIHBoYW4gcXV5ZXQpLiBgdmAgZGF1OiBiYW4KICAgICMgYGdvIGluc3RhbGxgIGluIGB2'
'MS43LjdgOyBraG9uZyBkb2MgZHVvYyBzbyAodmQuIGAoZGV2ZWwpYCkgPT4gS0hPTkcgRE8gRFVPQy4KICAgIGlmIG5vdCBf'
'dGhpZXVfY2M6CiAgICAgICAgX2FsID0gc3VicHJvY2Vzcy5ydW4oW19jY1siYWN0aW9ubGludCJdLCAiLXZlcnNpb24iXSwg'
'Y2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLCBlbmNvZGluZz0idXRmLTgiLAogICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9NjApCiAgICAgICAgX2FsX3YgPSByZS5zZWFyY2gociIoP20pXnY/'
'KFxkKylcLihcZCspXC4oXGQrKSIsIF9hbC5zdGRvdXQgb3IgIiIpCiAgICAgICAgaWYgX2FsLnJldHVybmNvZGU6CiAgICAg'
'ICAgICAgIGxvaS5hcHBlbmQoImFjdGlvbmxpbnQgdHJlbiBQQVRIIGNvIG1hdCBuaHVuZyBgYWN0aW9ubGludCAtdmVyc2lv'
'bmAgcmMhPTAgKGtob25nIGNoYXkgZHVvYyk6IGNhaSBsYWkgYmFuIGdoaW0gQUxfVkVSIikKICAgICAgICBlbGlmIG5vdCBf'
'YWxfdiBvciB0dXBsZShpbnQoeCkgZm9yIHggaW4gX2FsX3YuZ3JvdXBzKCkpIDwgQUxfU0FOOgogICAgICAgICAgICBsb2ku'
'YXBwZW5kKGYiYWN0aW9ubGludCB7X2FsX3YuZ3JvdXAoMCkgaWYgX2FsX3YgZWxzZSAnKGtob25nIGRvYyBkdW9jIHBoaWVu'
'IGJhbiknfSBjdSBob24gYmFuIGdoaW0gQ0kgIgogICAgICAgICAgICAgICAgICAgICAgIGYieycuJy5qb2luKG1hcChzdHIs'
'IEFMX1NBTikpfSAoQUxfVkVSKTogYmFuIGN1IGxhbSB0MTM3L3QxNTkgRE8gJ2xhJyB0cmVuIHVuZyB2aWVuIHNhY2gg4oCU'
'IgogICAgICAgICAgICAgICAgICAgICAgICIgY2FpIGJhbiBnaGltIChvcHMvY2FpX2FjdGlvbmxpbnQuc2ggdm9pIEFMX1ZF'
'UikiKQogICAgICAgICMgZ2l0IGN1bmcgdGhlOiBDTyBNQVQga2hvbmcgcGhhaSBEVU5HIERVT0MsIHZhIGdpdCBDVSBsYSBj'
'b25nIGN1IFBITyBCSUVOIG5oYXQgdHJvbmcgYm9uLiBEbyB0cmVuIDIwMjYtMDktMzBsLCAwZWE5NWRlLCBnaXQKICAgICAg'
'ICAjIFRIQVQgcXVhIGN1bmcgY2hheSgpOiAyLjI1LjEgPT4gMTQwLzE2NiAoMjMgY2EgImxhIjogYGluaXQgLWJgLi4uKSwg'
'Mi4zNC4xIHZhIDIuMzUuMSA9PiAxNjMvMTY2ICh0MTA5IHQxMTAgdDExMTogYGdpdAogICAgICAgICMgd29ya3RyZWUgbGlz'
'dCAtLXBvcmNlbGFpbiAtemAgcmM9MTI5IGB1bmtub3duIHN3aXRjaCB6YCksIGUyZSAyLjM1LjEgcmM9MSBgREFUIDExIHwg'
'VFJVT1QgMWA7IDIuMzYuMSA9PiAxNjYvMTY2LiBTYW4gbGF5CiAgICAgICAgIyB0dSB0aW5oIG5hbmcgbWEgQ0hJTkggbWEg'
'ZHVvYyBkbyBnb2kgKG9wcy9jb25nX2N1LnlhbWwgZGUgYmFuX2doaW0gZ2l0ID0gbnVsbCBuZW4ga2hvbmcgY28gYmFuIGdo'
'aW0gQ0kgZGUgZHVhIHZhbykuCiAgICAgICAgIyBgZ2l0IHZlcnNpb24gMi40Ny4xLndpbmRvd3MuMWAgKEdpdCBmb3IgV2lu'
'ZG93cykgdmEgYDIuMzkuMyAoQXBwbGUgR2l0LTE0NilgIGRldSBkb2MgZHVvYyBiYSBzbyBkYXUuCiAgICAgICAgIyBWYSBw'
'aGFpIGhvaSBEVU5HIGdpdCBtYSBibyB0ZXN0IFNFIEdPSS4gQm8gdGVzdCBLSE9ORyBgc2h1dGlsLndoaWNoKCJnaXQiKWAg'
'bmh1IGJhIGNvbmcgY3UgdHJlbjogR09JX0dJVCBjdWEgdW5nIHZpZW4gdmEgbW9pCiAgICAgICAgIyBmaXh0dXJlIGdvaSBg'
'Z2l0YCBUUkFOIOKAlCB0cmVuIFdpbmRvd3MgbGEgQ3JlYXRlUHJvY2Vzc1c6IENISSB0dSB0aGVtIGAuZXhlYCAoS0hPTkcg'
'UEFUSEVYVCksIHRyYSB0aHUgbXVjIHB5dGhvbi5leGUsIGN3ZAogICAgICAgICMgdmEgU3lzdGVtMzIgVFJVT0MgUEFUSC4g'
'YHdoaWNoYCB0aGkgdHJhIFBBVEhFWFQsIG5lbiBtb3QgYGdpdC5jbWRgL2BnaXQuYmF0YCBkdW5nIHRydW9jIGBnaXQuZXhl'
'YCBDVSB0cmVuIFBBVEggZHVvYyBob2kKICAgICAgICAjIFRIQVkgbm8g4oCUIGRvIHRyZW4gMjAyNi0xMC0wMSAobmhhbmgg'
'd2luMzIgVEhBVCBjdWEgc2h1dGlsLndoaWNoOyBzaGltIGBnaXQuQ01EYCBtb2kgdHJ1b2MgZ2l0IDIuMzUuMSBUSEFUKTog'
'YmFuIDMwbSBtdWMgMAogICAgICAgICMgaW0sIGUyZSByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCwgYGxhOiBbJ3QxMDknLCAn'
'dDExMCcsICd0MTExJ11gLiBOZW4gaG9pIGJhbmcgQ0hJTkggZHVvbmcgYXk6IHRpZW4gdHJpbmggY29uIGN1YSBjaGF5KCkK'
'ICAgICAgICAjIChjdW5nIHB5dGhvbiwgY3VuZyBtb2kgdHJ1b25nLCBjd2QgPSBnb2Mgbmh1IGJvIHRlc3QpIGdvaSBgZ2l0'
'IC0tdmVyc2lvbmAgVFJBTi4KICAgICAgICBfcmNfZ3YsIF9yYV9ndiA9IGNoYXkoWyItYyIsICJpbXBvcnQgc3VicHJvY2Vz'
'cywgc3lzOyBwID0gc3VicHJvY2Vzcy5ydW4oWydnaXQnLCAnLS12ZXJzaW9uJ10sIGNhcHR1cmVfb3V0cHV0PVRydWUsIgog'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiB0ZXh0PVRydWUsIHRpbWVvdXQ9NjApOyBwcmludChwLnN0'
'ZG91dCk7IHN5cy5leGl0KHAucmV0dXJuY29kZSkiXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZ29jIGlmIGdv'
'Yy5pc19kaXIoKSBlbHNlIFBhdGguY3dkKCksIHBodXQ9MikKICAgICAgICBfZ3ZfbSA9IHJlLnNlYXJjaChyIig/bSleZ2l0'
'IHZlcnNpb25ccysoXGQrKVwuKFxkKylcLihcZCspIiwgX3JhX2d2KQogICAgICAgIGdoaSgiZ2l0X2JvX3Rlc3QiLCBfZ3Zf'
'bS5ncm91cCgwKSBpZiBfZ3ZfbSBlbHNlIE5vbmUpCiAgICAgICAgaW5uKCIgIGdpdCBibyB0ZXN0ICA6IiwgX2d2X20uZ3Jv'
'dXAoMCkgaWYgX2d2X20gZWxzZSBmIihraG9uZyBkb2MgZHVvYyBwaGllbiBiYW4sIHJjPXtfcmNfZ3Z9KSIpCiAgICAgICAg'
'aWYgX3JjX2d2OgogICAgICAgICAgICBsb2kuYXBwZW5kKGYiYGdpdCAtLXZlcnNpb25gIGdvaSBUUkFOIG5odSBibyB0ZXN0'
'IHJjIT0wICh7KF9yYV9ndi5zdHJpcCgpLnNwbGl0bGluZXMoKSBvciBbJyddKVstMV1bOjkwXX0pOiBjYWkgbGFpIGdpdCIp'
'CiAgICAgICAgZWxpZiBub3QgX2d2X20gb3IgdHVwbGUoaW50KHgpIGZvciB4IGluIF9ndl9tLmdyb3VwcygpKSA8IEdJVF9T'
'QU46CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJnaXQgeycuJy5qb2luKF9ndl9tLmdyb3VwcygpKSBpZiBfZ3ZfbSBlbHNl'
'ICcoa2hvbmcgZG9jIGR1b2MgcGhpZW4gYmFuKSd9IGN1IGhvbiAiCiAgICAgICAgICAgICAgICAgICAgICAgZiJ7Jy4nLmpv'
'aW4obWFwKHN0ciwgR0lUX1NBTikpfSAodW5nIHZpZW4gZ29pIGBnaXQgd29ya3RyZWUgbGlzdCAtLXBvcmNlbGFpbiAtemAp'
'OiBjYXAgbmhhdCBnaXQiKQogICAgICAgICMgYmFzaCBjdW5nIEhPSSBTQUkgQ0hPIG5odSBnaXQ6IDkgY2EgVFJPTkcgcGhh'
'bSB2aSAodDMyIHQ1MSB0NTkgdDYwIHQ2MiB0NjMgdDY2IHQ2OCB0MTUyKSBjaGF5IGJhc2ggYmFuZyBgX2Jhc2hfcG9zaXgo'
'KWAKICAgICAgICAjIGN1YSB1bmcgdmllbiDigJQgR2l0IEJhc2ggbyBkdW9uZyBDTyBESU5IIGBDOlxQcm9ncmFtIEZpbGVz'
'XEdpdFxiaW5cYmFzaC5leGVgICh2YSBgKHg4NilgLCBgdXNyXGJpbmApLCByb2kKICAgICAgICAjIGB3aGljaCgiYmFzaCIp'
'YCBOSFVORyBsb2FpIGtldCBxdWEgdHJvbmcgU3lzdGVtMzIgKFdTTCk7IGtob25nIHRoYXkgdGhpIHRyYSAiIi4gTWF5IGNv'
'IFdTTCBtYSBHaXQga2hvbmcgbyBQcm9ncmFtIEZpbGVzCiAgICAgICAgIyAoTWluR2l0IGRvIENISU5IIHBzMSB0dSB0YWkg'
'4oCUIE1pbkdpdCBLSE9ORyBjbyBiYXNoOyBzY29vcDsgY2FpIHBlci11c2VyKSBxdWEgY2hvdCBgd2hpY2hgIG8gdHJlbiwg'
'cm9pIGBfYmFzaF9wb3NpeCgpYAogICAgICAgICMgPT0gIiI6IHQzMiAiS0hPTkcgRE8gRFVPQyIgKyA4IGNhICJsYSIgYHN1'
'YnByb2Nlc3MucnVuKFsiIi4uLl0pYCwgY2hpIGxvIHJhIFNBVSBjYSBoYWkgbHVvdCBibyB0ZXN0LiBEbyB0cmVuIDIwMjYt'
'MTAtMDE6CiAgICAgICAgIyBoYW0gVEhBVCwgbmhhbmggb3MubmFtZT0nbnQnIChXU0wgKyBNaW5HaXQvc2Nvb3AvcGVyLXVz'
'ZXIpID0+ICcnOyBibyB0ZXN0IHZvaSBnaWEgdHJpIGF5IDE1Ny8xNjY7IGUyZSAod2luMzIgZ2lhKSByYz0zCiAgICAgICAg'
'IyBzYXUgMzQ3IHMsIGBUUlVPVCBNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyAgbGE6IFsndDUxJywgJ3Q1OScsICd0'
'NjAnLCAndDYyJywgJ3Q2MycsICd0NjYnLCAndDY4JywgJ3QxNTInXWAuIFBoZXAKICAgICAgICAjIGRvIDMwaiBjaGF5IHRy'
'ZW4gTGludXgsIG5vaSBgX2Jhc2hfcG9zaXgoKWAgbHVvbiB0cmEgImJhc2giLCBuZW4ga2hvbmcgdGhlIHRoYXkgZHVvbmcg'
'bmF5LgogICAgICAgICMgVmEgYGdpdGAgVFJPTkcgYmFzaCBheSBsYSBnaXQgVEhVIEJBOiBgR2l0XGJpblxiYXNoLmV4ZWAg'
'bGEgY29tcGF0LWJhc2ggY3VhIGdpdC13cmFwcGVyLCBgc2V0dXBfZW52aXJvbm1lbnQoKWAgZGF5CiAgICAgICAgIyBgPGdv'
'YyBHaXQ+XG1pbmd3NjRcYmluOzxnb2MgR2l0Plx1c3JcYmluYCBsZW4gREFVIFBBVEggKGdpdC1mb3Itd2luZG93cy9NSU5H'
'Vy1wYWNrYWdlczogZ2l0LXdyYXBwZXIuYyArIGNvbXBhdC1iYXNoLnJjLAogICAgICAgICMga2hvbmcgY28gTUlOSU1BTF9Q'
'QVRIKSDigJQgdHVjIGdpdCBESSBLRU0gYmFuIEdpdCBheSwgS0hPTkcgcGhhaSBnaXQgVFJBTiBkYSBob2kgbyB0cmVuLiB0'
'MTUyIGNoYXkgR0lUX0NPTkZJR19DT1VOVCAoZ2l0CiAgICAgICAgIyAyLjMxKSB0cm9uZyBiYXNoIGF5LiBEbyB0cmVuIDIw'
'MjYtMTAtMDEgKGJhc2ggYm9jIGRheSBnaXQgZGkga2VtIGxlbiBkYXUgUEFUSCwgZ2l0IFRSQU4gMi40Myk6IGdpdCBkaSBr'
'ZW0gMi4zMC4yIFRIQVQgPT4KICAgICAgICAjIDE2NS8xNjYsIGUyZSByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCwgYGxhOiBb'
'J3QxNTInXWAgY2hvIHVuZyB2aWVuIHNhY2g7IDIuMzEuMCBUSEFUID0+IDE2Ni8xNjYuIEhvaSBDSElOSCBoYW0gYXkgdmEK'
'ICAgICAgICAjIENISU5IIGJhc2ggYXkgdHJvbmcgdGllbiB0cmluaCBjb24gY3VhIGNoYXkoKSAoY3VuZyBweXRob24sIGN1'
'bmcgbW9pIHRydW9uZywgY3dkID0gZ29jKTsgdW5nIHZpZW4ga2hvbmcgY28gaGFtIHRoaSBraG9uZwogICAgICAgICMgaG9p'
'IChnaXUgY2hvdCBDTyBNQVQpLgogICAgICAgICMgRG9jIGRvbmcgYGdpdCB2ZXJzaW9uYCBDVU9JIGN1YSBzdGRvdXQsIEtI'
'T05HIGRvYyBkb25nIERBVTogYmFzaCBuYXAgQkFTSF9FTlYgVFJVT0MgbGVuaCAtYyAoYmFuIDAxYjogQkFTSF9FTlYgYGVj'
'aG9gIG1vdAogICAgICAgICMgZG9uZyA9PiBtdWMgMCBLREQgb2FuLCBibyB0ZXN0IDE2Ni8xNjYpLiBCYXNoIHRyZW8gdGhp'
'IGJhdCBuZ29haSBsZSBUUk9ORyBjb24gKGJhbiAwMWIgZG8gbG9pIGNobyBgX2Jhc2hfcG9zaXgoKWApIHZhCiAgICAgICAg'
'IyBEVU5HIGx1b24gKGtob25nIGhvaSBsYW4gaGFpOiBnaXUgdHJhbiA2MCBzIHZhIG1vdCB0aWVuIHRyaW5oIG1vIGNvaSBu'
'aHUgYmFuIDAxYykuCiAgICAgICAgIyBWYSBob2kgSEFJIGxhbiwgZHVuZyBIQUkgbW9pIHRydW9uZyBibyB0ZXN0IFRIQVQg'
'ZHVuZzogMyBsb2kgZ29pIGBfYmFzaF9wb3NpeCgpYCBjdWEgdW5nIHZpZW4gY2hheSBiYXNoIHZvaSAyIG1vaSB0cnVvbmcg'
'4oCUCiAgICAgICAgIyB0MzIvdDUxLXQ2OCBgZGljdChvcy5lbnZpcm9uLCAuLi4pYCAoQ08gQkFTSF9FTlYpLCBjb24gdDE1'
'MiAoY2EgRFVZIE5IQVQgY2FuIHNhbiAyLjMxKSBgZGljdChQQVRIPW9zLmVudmlyb25bIlBBVEgiXSwKICAgICAgICAjIFRM'
'XyosIEdJVF9DT05GSUdfKilgIChLSE9ORyBCQVNIX0VOVikuIEJhbiAwMWMgaG9pIG8gbW9pIHRydW9uZyBUSFUgTkhBVCBy'
'b2kgYXAgc2FuIGN1YSB0MTUyIOKAlCBkbyB0cmVuIDIwMjYtMTAtMDE6IGdpdCBkaQogICAgICAgICMga2VtIDIuMzAuMiBU'
'SEFUICsgQkFTSF9FTlYgZGF5IGdpdCAyLjQzIGxlbiBkYXUgUEFUSCA9PiBtdWMgMCB0aGF5IDIuNDMsIGUyZSByYz0xIGBE'
'QVQgMTEgfCBUUlVPVCAxYCwgYGxhOiBbJ3QxNTInXWAgY2hvCiAgICAgICAgIyB1bmcgdmllbiBzYWNoOyBCQVNIX0VOViBk'
'YXkgZ2l0IDIuMzAuMiA9PiBtdWMgMCBLREQsIGJvIHRlc3QgMTY2LzE2Ni4gTW9pIHRydW9uZyB0aHUgbmhhdCBWQU4gcGhh'
'aSBob2k6IEJBU0hfRU5WIGluIGJ5dGUKICAgICAgICAjIG5nb2FpIFVURi04ID0+IGJvIHRlc3QgMTUyLzE2NiAodDMyL3Q1'
'MS10NjggYFVuaWNvZGVEZWNvZGVFcnJvcmApLiBCQVNIX0dJVCA9IG1vaSB0cnVvbmcgdDMyL3Q1MS10NjggKGRvaSBDSEFZ'
'IGR1b2MpOwogICAgICAgICMgQkFTSF9HSVRfVDE1MiA9IG1vaSB0cnVvbmcgdDE1MiAoZG9pIHNhbiBHSVRfU0FOX0JBU0gp'
'LgogICAgICAgIF9yY19icCwgX3JhX2JwID0gY2hheShbIi1jIiwgImltcG9ydCBvcywgc3VicHJvY2Vzcywgc3lzXG5zeXMu'
'cGF0aC5pbnNlcnQoMCwgJ29wcycpXG5pbXBvcnQgbGVhc2VfcHVibGlzaF90ZXN0IGFzIFRcbiIKICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICJmID0gZ2V0YXR0cihULCAnX2Jhc2hfcG9zaXgnLCBOb25lKVxuYiA9ICc/JyBpZiBm'
'IGlzIE5vbmUgZWxzZSBmKClcbnByaW50KCdCQVNIX1BPU0lYPScgKyBiKVxuIgogICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgImlmIGIgYW5kIGIgIT0gJz8nOlxuICBmb3IgayBpbiAoJ0JBU0hfR0lUJywgJ0JBU0hfR0lUX1QxNTIn'
'KTpcbiAgICB0cnk6XG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiICAgICAgcCA9IHN1YnByb2Nl'
'c3MucnVuKFtiLCAnLS1ub3Byb2ZpbGUnLCAnLS1ub3JjJywgJy1jJywgJ2dpdCAtLXZlcnNpb24nXSwiCiAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAiIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwgdGltZW91dD02MCwi'
'CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiIGVudj1Ob25lIGlmIGsgPT0gJ0JBU0hfR0lUJyBlbHNl'
'IHsnUEFUSCc6IG9zLmVudmlyb25bJ1BBVEgnXX0pXG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAi'
'ICAgICAgdiA9IFt4IGZvciB4IGluIHAuc3Rkb3V0LnNwbGl0bGluZXMoKSBpZiB4LnN0YXJ0c3dpdGgoJ2dpdCB2ZXJzaW9u'
'JyldIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiBvciBwLnN0ZG91dC5zdHJpcCgpLnNwbGl0bGlu'
'ZXMoKSBvciBbJyddXG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiICAgICAgcHJpbnQoayArICc9'
'JyArIHZbLTFdICsgJyByYz0nICsgc3RyKHAucmV0dXJuY29kZSkpXG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAiICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZTpcbiAgICAgIHByaW50KGsgKyAnPSgnICsgdHlwZShlKS5fX25h'
'bWVfXyArICcpIHJjPS0xJylcbiIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgICAgICBicmVha1xu'
'Il0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGdvYyBpZiBnb2MuaXNfZGlyKCkgZWxzZSBQYXRoLmN3ZCgpLCBw'
'aHV0PTMpCiAgICAgICAgX2JwX20gPSByZS5zZWFyY2gociIoP20pXkJBU0hfUE9TSVg9KC4qKSQiLCBfcmFfYnApCiAgICAg'
'ICAgX2JwID0gX2JwX20uZ3JvdXAoMSkuc3RyaXAoKSBpZiAoX2JwX20gYW5kIG5vdCBfcmNfYnApIGVsc2UgTm9uZQogICAg'
'ICAgIF9iZ19tID0gcmUuc2VhcmNoKHIiKD9tKV5CQVNIX0dJVD1naXQgdmVyc2lvblxzKyhcZCspXC4oXGQrKVwuKFxkKylb'
'XlxuXSpcc3JjPTAkIiwgX3JhX2JwKQogICAgICAgIF9idF9tID0gcmUuc2VhcmNoKHIiKD9tKV5CQVNIX0dJVF9UMTUyPWdp'
'dCB2ZXJzaW9uXHMrKFxkKylcLihcZCspXC4oXGQrKVteXG5dKlxzcmM9MCQiLCBfcmFfYnApCiAgICAgICAgZ2hpKCJiYXNo'
'X2JvX3Rlc3QiLCBfYnApOyBnaGkoImdpdF90cm9uZ19iYXNoX2JvX3Rlc3QiLCBfYmdfbS5ncm91cCgwKVs5Ol0gaWYgX2Jn'
'X20gZWxzZSBOb25lKQogICAgICAgIGdoaSgiZ2l0X3Ryb25nX2Jhc2hfdDE1MiIsIF9idF9tLmdyb3VwKDApWzE0Ol0gaWYg'
'X2J0X20gZWxzZSBOb25lKQogICAgICAgIGlubigiICBiYXNoIGJvIHRlc3QgOiIsIHJlcHIoX2JwKSBpZiBfYnAgaXMgbm90'
'IE5vbmUgZWxzZSBmIihraG9uZyBob2kgZHVvYywgcmM9e19yY19icH0pIiwKICAgICAgICAgICAgInwgZ2l0IHRyb25nIGJh'
'c2g6IiwgX2JnX20uZ3JvdXAoMClbOTpdIGlmIF9iZ19tIGVsc2UgIihraG9uZyBkb2MgZHVvYykiLAogICAgICAgICAgICAi'
'fCBtb2kgdHJ1b25nIHQxNTI6IiwgX2J0X20uZ3JvdXAoMClbMTQ6XSBpZiBfYnRfbSBlbHNlICIoa2hvbmcgZG9jIGR1b2Mp'
'IikKICAgICAgICBpZiBfYnAgaXMgTm9uZToKICAgICAgICAgICAgbG9pLmFwcGVuZChmImtob25nIGhvaSBkdW9jIGBfYmFz'
'aF9wb3NpeCgpYCBjdWEgYm8gdGVzdCAocmM9e19yY19icH06IgogICAgICAgICAgICAgICAgICAgICAgIGYiIHsoX3JhX2Jw'
'LnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10pWy0xXVs6OTBdfSkiKQogICAgICAgIGVsaWYgbm90IF9icDoKICAgICAg'
'ICAgICAgbG9pLmFwcGVuZChmImBfYmFzaF9wb3NpeCgpYCBjdWEgYm8gdGVzdCBLSE9ORyB0aGF5IGJhc2ggUE9TSVggKGB3'
'aGljaGA6IHtfY2NbJ2Jhc2gnXX07IFN5c3RlbTMyID0gV1NMIGJpIGxvYWkpOiIKICAgICAgICAgICAgICAgICAgICAgICAi'
'IGNhaSBHaXQgZm9yIFdpbmRvd3MgdmFvIEM6XFxQcm9ncmFtIEZpbGVzXFxHaXQsIGhvYWMgZGF0IHRodSBtdWMgR2l0XFxi'
'aW4gbGVuIERBVSBQQVRIICh0cnVvYyBTeXN0ZW0zMikiKQogICAgICAgIGVsaWYgX2JwICE9ICI/IiBhbmQgbm90IChfYmdf'
'bSBhbmQgX2J0X20pOgogICAgICAgICAgICBfZG9uZ19iZyA9IFt4Wzo5MF0gZm9yIHggaW4gcmUuZmluZGFsbChyIig/bSle'
'KEJBU0hfR0lUKD86X1QxNTIpPz0uKikkIiwgX3JhX2JwKV0gb3IgWyIoa2hvbmcgY28gZG9uZyBCQVNIX0dJVCkiXQogICAg'
'ICAgICAgICBsb2kuYXBwZW5kKGYiYGdpdCAtLXZlcnNpb25gIFRST05HIGJhc2ggY3VhIGJvIHRlc3QgKHtfYnB9KSBraG9u'
'ZyBjaGF5L2tob25nIGRvYyBkdW9jIHBoaWVuIGJhbjogeycgfCAnLmpvaW4oX2RvbmdfYmcpfSIpCiAgICAgICAgZWxpZiBf'
'YnAgIT0gIj8iIGFuZCB0dXBsZShpbnQoeCkgZm9yIHggaW4gX2J0X20uZ3JvdXBzKCkpIDwgR0lUX1NBTl9CQVNIOgogICAg'
'ICAgICAgICBsb2kuYXBwZW5kKGYiZ2l0IHsnLicuam9pbihfYnRfbS5ncm91cHMoKSl9IFRST05HIGJhc2ggY3VhIGJvIHRl'
'c3QgKHtfYnB9OyBtb2kgdHJ1b25nIHQxNTI6IGNoaSBQQVRILCBraG9uZyBCQVNIX0VOVikgY3UiCiAgICAgICAgICAgICAg'
'ICAgICAgICAgZiIgaG9uIHsnLicuam9pbihtYXAoc3RyLCBHSVRfU0FOX0JBU0gpKX0gKHQxNTIgZHVuZyBHSVRfQ09ORklH'
'X0NPVU5UKTogY2FwIG5oYXQgYmFuIEdpdCBjaHVhIGJhc2ggYXkiKQoKcmMsIGhlYWQsIF8gPSBnaXQoZ29jLCAicmV2LXBh'
'cnNlIiwgIkhFQUQiKQppZiByYzogbG9pLmFwcGVuZCgia2hvbmcgZG9jIGR1b2MgSEVBRCIpCmdoaSgiaGVhZCIsIGhlYWQp'
'CnJjX2EsIF8sIF8gPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICItLWlzLWFuY2VzdG9yIiwgU0hBX0cxLCBoZWFkIG9yICJI'
'RUFEIikKbGFfaGF1X2R1ZSA9IChyY19hID09IDApCmlmIGhlYWQgPT0gU0hBX0cxOgogICAgdGhlX2hlID0gImcxIjsgaW5u'
'KGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBEQVkgTEEgZzEuIENIVUEgY28gYmFuIHZhIGcyOyBrZXQgcXVhIGR1b2kgbGEg'
'TkVOIERPLiIpCmVsaWYgbGFfaGF1X2R1ZToKICAgIHRoZV9oZSA9ICJnMiI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0g'
'LT4gaGF1IGR1ZSBjdWEgZzEgKHtTSEFfRzFbOjhdfSk7IHVuZyB2aWVuIGcyIGhheSBraG9uZzogTjcnIChtdWMgMSkgZGlu'
'aCBkYW5oLiIpCmVsc2U6CiAgICB0aGVfaGUgPSAiPyI7IGxvaS5hcHBlbmQoZiJIRUFEPXtoZWFkWzo4XX0gS0hPTkcgcGhh'
'aSBnMSB2YSBLSE9ORyBwaGFpIGhhdSBkdWUgY3VhIHtTSEFfRzFbOjhdfSDigJQgcmViYXNlPyBuaGFtIG5oYW5oPyIpCmdo'
'aSgidGhlX2hlIiwgdGhlX2hlKQpyY19yLCByZWZzLCBfID0gZ2l0KGdvYywgImZvci1lYWNoLXJlZiIsICItLXBvaW50cy1h'
'dCIsIGhlYWQgb3IgIkhFQUQiLAogICAgICAgICAgICAgICAgICAgICItLWZvcm1hdD0lKHJlZm5hbWU6c2hvcnQpIikKZHNy'
'ID0gW3ggZm9yIHggaW4gcmVmcy5zcGxpdGxpbmVzKCkgaWYgeC5zdHJpcCgpIGFuZCB4LnN0cmlwKCkgIT0gImRvLXRhbSJd'
'CmdoaSgicmVmX3Ryb190b2lfaGVhZCIsIGRzcikKaW5uKGYiICByZWYgdHJvIHRvaSBIRUFEOiB7JywgJy5qb2luKGRzcikg'
'aWYgZHNyIGVsc2UgJyhraG9uZyByZWYgbmFvIC0gSEVBRCByb2kgdHUgZG8pJ30iKQoKaWYgbG9pOgogICAgaW5uKCIiKTsg'
'aW5uKCJLSE9ORyBETyBEVU9DOiBuZW4gZG8gc2FpLCBLSE9ORyBpbiBrZXQgbHVhbiBuYW8uIikKICAgIGZvciB4IGluIGxv'
'aTogaW5uKCIgIC0iLCB4KQogICAgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAxLiBraWNoIHRodW9jIChONycg'
'Y3VhIHNwZWMgcjMpIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIxLiBLSUNIIFRIVU9D'
'IOKAlCB0cmFuIHNwZWMgcjM6IDw9IDIgdGVwIHZhIDw9IDQwMCBkb25nIHRoZW0iKQojIFZFIE5FTiBQSEFJIFRVT0kg4oCU'
'IHZhIHBoYWkgQ0hVTkcgTUlOSCBkdW9jIGxhIHR1b2ksIGtob25nIHBoYWkgZ2lhIGRpbmguCiMgQmFpIGhvYyB0cmEgZ2lh'
'IDE5LTA5LTIwMjY6IGNsb25lIHRhaSBkdW5nIGNoaSBmZXRjaCBuaGFuaCBiYW4gdmEsIGBvcmlnaW4vbWFzdGVyYAojIGR1'
'bmcgeWVuIHR1IDE0LTA5IChjMTZiZDMyLCBzYXUgOTcgY29tbWl0KS4gbWVyZ2UtYmFzZSByb2kgdmUgZHVuZyBkaW5oIG1h'
'c3RlciBjdSwKIyBuZW4gZGlmZiBOVU9UIGNhIDk3IGNvbW1pdCBtYXN0ZXI6IGRvIHJhIDQ2IHRlcCAvICs3MTE4IHRoYXkg'
'dmkgMiB0ZXAgLyArMzk3IOKAlAojIENVTkcgTU9UIENPTU1JVCAwZWE5NWRlLiBNb3QgdGlldSBjaGkgREVMVEEgbWEgdmUg'
'bmVuIGtob25nIHR1b2kgdGhpIGtob25nIHNhaQojIGxlY2ggbW90IGNodXQsIG5vIHNhaSBjYSBtb3QgYmFjIGRvIGxvbi4K'
'IyBDaG8gbmVuOiBuZW4ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGxhIHR1b2kgPT4gS0hPTkcgRE8gRFVPQyAocmM9MyksIEtI'
'T05HIHBoYWkgVFJVT1QuCiMgVFJVT1QgbGEgbW90IFBIQU4gUVVZRVQgdmUgYmFuIHZhOyBwaGFuIHF1eWV0IGNoaSBkdW9j'
'IHBoZXAgcGhhdCByYSBraGkgZGEgZG8gZHVvYy4KZXIgPSAiIgpyY191LCB1cmxfdGhvLCBfID0gZ2l0KGdvYywgInJlbW90'
'ZSIsICJnZXQtdXJsIiwgIm9yaWdpbiIpCnVybF9vLCB1cmxfaW4gPSBfdXJsX3NhY2godXJsX3RobyksIF91cmxfaW4odXJs'
'X3RobykKZ2hpKCJvcmlnaW5fdXJsIiwgdXJsX2luKTsgaW5uKGYiICBvcmlnaW4gICAgICAgOiB7dXJsX2luIG9yICcoa2hv'
'bmcgZG9jIGR1b2MpJ30iKQp1cmxfb2sgPSAobm90IHJjX3UpIGFuZCB1cmxfby5yc3RyaXAoIi8iKSBpbiBVUkxfS0hPX0hP'
'UF9MRQpyY19sciwgb3V0X2xyLCBlcl9sciA9IGdpdChnb2MsICJscy1yZW1vdGUiLCAib3JpZ2luIiwgInJlZnMvaGVhZHMv'
'bWFzdGVyIikgaWYgdXJsX29rIGVsc2UgKDEsICIiLCAiIikKZXJfbHIgPSBfYW5fdXNlcmluZm8oZXJfbHIpCnJjX2xtLCBs'
'bSwgZXJfbG0gICAgID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJvcmlnaW4vbWFzdGVyIikKcm0gPSBvdXRfbHIuc3BsaXQo'
'KVswXSBpZiAobm90IHJjX2xyIGFuZCBvdXRfbHIuc3RyaXAoKSkgZWxzZSAiIgppZiBub3QgdXJsX29rOgogICAga2V0KCJO'
'Nycga2ljaCB0aHVvYyIsIEtERCwgZiJvcmlnaW49e3VybF9pbiFyfSBLSE9ORyBwaGFpIGtobyB0aGF0IOKAlCAndHVvaScg'
'c28gdm9pIG5vIGtob25nIGNodW5nIG1pbmggZHVvYyBnaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwg'
'MQplbGlmIG5vdCBybToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJraG9uZyBob2kgZHVvYyBt'
'YXN0ZXIgdHJlbiByZW1vdGUgKGxzLXJlbW90ZSByYz17cmNfbHJ9KToge2VyX2xyWzo2MF19ICIKICAgICAgICBmIuKAlCBr'
'aG9uZyBjaHVuZyBtaW5oIGR1b2MgdmUgbmVuIGNvbiB0dW9pIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIi'
'LCAxCmVsaWYgcmNfbG0gb3Igbm90IGxtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyBkb2MgZHVv'
'YyBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25lOiB7ZXJfbG1bOjYwXX0iKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAi'
'IiwgIiIsIDEKZWxpZiBsbSAhPSBybToKICAgICMgRGVtIHhlbSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRlbSBkdW9jIOKAlCBj'
'b24gc28gbmF5IG5vaSBybyBtdWMgZG8gc2FpIGxlY2guCiAgICByY19jLCBzYXUsIF8gPSBnaXQoZ29jLCAicmV2LWxpc3Qi'
'LCAiLS1jb3VudCIsIGYie2xtfS4ue3JtfSIpCiAgICB4YSA9IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1pdCIgaWYgKG5vdCBy'
'Y19jIGFuZCBzYXUuc3RyaXAoKS5pc2RpZ2l0KCkpIGVsc2UgIiIKICAgIGlubihmIiAgb3JpZ2luL21hc3RlciB0cm9uZyBj'
'bG9uZSA6IHtsbVs6MTJdfSIpCiAgICBpbm4oZiIgIG1hc3RlciB0cmVuIHJlbW90ZSAgICAgICAgOiB7cm1bOjEyXX17eGF9'
'IikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIGtldCgiTjcnIGtp'
'Y2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJ2ZSBuZW4gQ1U6IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19ICE9IHJlbW90ZT17'
'cm1bOjEyXX17eGF9ICIKICAgICAgICBmIuKAlCBjaGF5IGBnaXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2luIG1hc3RlcmAgcm9p'
'IGRvIGxhaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbHNlOgogICAgaW5uKGYiICB2ZSBuZW4g'
'VFVPSTogb3JpZ2luL21hc3RlciA9IHtsbVs6MTJdfSA9PSBtYXN0ZXIgdHJlbiByZW1vdGUiKQogICAgZ2hpKCJtYXN0ZXJf'
'Y2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAgcmNfbWIsIG1iLCBlcl9tYiA9IGdpdChnb2MsICJt'
'ZXJnZS1iYXNlIiwgIm9yaWdpbi9tYXN0ZXIiLCBoZWFkKQppZiByY19tYiBvciBub3QgbWI6CiAgICBpZiBtYiA9PSAiIiBh'
'bmQgcm0gYW5kIGxtID09IHJtOgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9j'
'IG1lcmdlLWJhc2Ugdm9pIG9yaWdpbi9tYXN0ZXI6IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgog'
'ICAgZ2hpKCJtZXJnZV9iYXNlIiwgbWIpCiAgICBpbm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7'
'bWJbOjEyXX0iKQogICAgaWYgbWIgIT0gU0hBX0JBU0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2Ug'
'bWEgc3BlYyByMyBraGFpICh7U0hBX0JBU0VfU1BFQ1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQog'
'ICAgICAgIGlubigiICAgICAgICAgRG8gc28gYmFzZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcgdmFvLiBEdW5nIG1l'
'cmdlLWJhc2UgbW9pIGxhIHZpZWMgY3VhIGV4ZWN1dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJk'
'aWZmLXRyZWUiLCAiLXIiLCAiLU0iLCAiLS1kaWZmLWFsZ29yaXRobT1teWVycyIsICItLW51bXN0YXQiLCBTSEFfQkFTRV9T'
'UEVDLCBoZWFkKQogICAgICAgIGlmIG5vdCByY194OgogICAgICAgICAgICBoID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4g'
'bnNfeC5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAgICAgICAgICBhID0gc3VtKGludCh4WzBdKSBmb3IgeCBpbiBo'
'IGlmIHhbMF0uaXNkaWdpdCgpKQogICAgICAgICAgICBnaGkoIm51bXN0YXRfdGhlb19iYXNlX3NwZWMiLCB7InRlcCI6IGxl'
'bihoKSwgInRoZW0iOiBhfSkKICAgICAgICAgICAgaW5uKGYiICAgICAgICAgKGRvaSBjaGlldTogc28gYmFzZSBzcGVjID0g'
'e2xlbihoKX0gdGVwIC8gK3thfSDigJQgY29uIHNvIGF5IEtIT05HIGR1bmcgZGUgY2hhbSkiKQogICAgIyBQTFVNQklORywg'
'a2hvbmcgUE9SQ0VMQUlOOiBgZ2l0IGRpZmZgIGRvYyBjYXUgaGluaCBVSSBDVUEgTkdVT0kgRE8gKGRpZmYuYWxnb3JpdGht'
'LCBkaWZmLnJlbmFtZXMsIGRpZmYub3JkZXJGaWxlLAogICAgIyBjb2xvci5kaWZmKSwgdmEgZ2lhIHRyaSBIT1AgTEUgZG9p'
'IGx1b24gU08gZG9uZyBtYSB2YW4gcmEgY2h1IHNvIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBpOiB1bmcgdmllbiB0b25nIGhv'
'cCAobXllcnMgKzQwMSkgPT4KICAgICMgYmFuIDMwaSBEQVQgMiB0ZXAgLyArNDAwIGR1b2kgYGRpZmYuYWxnb3JpdGhtID0g'
'aGlzdG9ncmFtYCBob2FjIGBwYXRpZW5jZWAsIFRSVU9UICs0MDEga2hpIG1hYyBkaW5oOyAxMC83NSBjb21taXQgY2hhbQog'
'ICAgIyB3cml0ZSBzZXQgY28gc28gZG9uZyBkb2kgdGhlbyB0aHVhdCB0b2FuLiBgZGlmZi10cmVlIC1yIC1NYCA9IG1hYyBk'
'aW5oIGN1YSBgZ2l0IGRpZmZgIChyZW5hbWVzIGJhdCkgdmEgS0hPTkcgZG9jIGNhYyBraG9hCiAgICAjIGF5LiBUaHVhdCB0'
'b2FuIHBoYWkgVFVPTkcgTUlOSDogZGlmZi48ZHJpdmVyPi5hbGdvcml0aG0gKHF1YSBjb3JlLmF0dHJpYnV0ZXNGaWxlIGN1'
'YSBuZ3VvaSBkbykgVkFOIGxvdCB2YW8gcGx1bWJpbmcg4oCUCiAgICAjIGRvIHRyZW4gMjAyNi0wOS0zMGksIGAqLnB5IGRp'
'ZmY9YWxnYCArIGRpZmYuYWxnLmFsZ29yaXRobT1oaXN0b2dyYW06IGRpZmYtdHJlZSArNDAxIGNobyB1bmcgdmllbiBteWVy'
'cyArNDAwOyBjbyB0dW9uZyBtaW5oCiAgICAjIHRoYW5nIGtob2EgYXkuIGF0dHJpYnV0ZXMgYC1kaWZmYC9jb3JlLmJpZ0Zp'
'bGVUaHJlc2hvbGQgdmFuIGFwID0+IGAtYCA9PiBLSE9ORyBETyBEVU9DIChjaG90IGR1b2kpLgogICAgcmMsIG5zLCBlciA9'
'IGdpdChnb2MsICJkaWZmLXRyZWUiLCAiLXIiLCAiLU0iLCAiLS1kaWZmLWFsZ29yaXRobT1teWVycyIsICItLW51bXN0YXQi'
'LCBtYiwgaGVhZCkKaWYgcmM6CiAgICBwYXNzCmVsc2U6CiAgICBoYW5nID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnMu'
'c3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgIHRoZW0gPSBzdW0oaW50KGhbMF0pIGZvciBoIGluIGhhbmcgaWYgaFsw'
'XS5pc2RpZ2l0KCkpCiAgICB4b2EgID0gc3VtKGludChoWzFdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMV0uaXNkaWdpdCgpKQog'
'ICAgZ2hpKCJzb190ZXAiLCBsZW4oaGFuZykpOyBnaGkoImRvbmdfdGhlbSIsIHRoZW0pOyBnaGkoImRvbmdfeG9hIiwgeG9h'
'KQogICAgZm9yIGggaW4gaGFuZzogaW5uKGYiICAgIHtoWzJdOjM0fSAre2hbMF06PDV9IC17aFsxXX0iKQogICAgaW5uKGYi'
'ICAgIFRPTkc6IHtsZW4oaGFuZyl9IHRlcCwgK3t0aGVtfSwgLXt4b2F9ICAgKHRyYW46IHtUUkFOX1RFUH0gdGVwIC8ge1RS'
'QU5fRE9OR30gZG9uZyB0aGVtKSIpCiAgICBjaGFtID0gc29ydGVkKHtoWzJdIGZvciBoIGluIGhhbmd9ICYgV1JJVEVfU0VU'
'X0cyKTsgZ2hpKCJjaGFtX3dyaXRlX3NldCIsIGNoYW0pCiAgICBkZWYgX2NhX21vaV9jbyhyZXYpOgogICAgICAgICMgY2F0'
'LWZpbGUsIGtob25nIGBzaG93YDogYGdpdCBzaG93YCBjaGV0IHZvaSBjYXUgaGluaCBVSSBnbyBzYWkgKGRvIHRyZW4gMjAy'
'Ni0wOS0zMGk6IGxvZy5kYXRlIGdvIHNhaSA9PiBiYW4gMzBpIGdvaQogICAgICAgICMgMGVhOTVkZSBsYSAia2hvbmcgcGhh'
'aSB1bmcgdmllbiAuLi4gTm9uZSDigJQgZGEgbGFuZD8gbmhhbSBuaGFuaD8iKS4KICAgICAgICByXywgbmRfLCBfID0gZ2l0'
'KGdvYywgImNhdC1maWxlIiwgIi1wIiwgZiJ7cmV2fTpvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICByZXR1'
'cm4gTm9uZSBpZiByXyBlbHNlIHt0IGZvciB0IGluIENBX01PSV9HMiBpZiByZS5zZWFyY2gociIoP20pXmRlZiAiICsgdCAr'
'IHIiW2Etel0/XyIsIG5kXyl9CiAgICBvX21iLCBvX2ggPSBfY2FfbW9pX2NvKG1iKSwgX2NhX21vaV9jbyhoZWFkKQogICAg'
'bWFuZyA9IHNvcnRlZChvX2ggLSBvX21iLCBrZXk9c29fY2EpIGlmIChvX21iIGlzIG5vdCBOb25lIGFuZCBvX2ggaXMgbm90'
'IE5vbmUpIGVsc2UgTm9uZQogICAgZ2hpKCJjYV9tb2lfZzJfbWFuZ192YW8iLCBtYW5nKQogICAgaWYgbm90IG1hbmc6CiAg'
'ICAgICAgIyBEbyBST05HIChkYSBsYW5kLCBjaGluaCBtYXN0ZXIpLCBuaGFtIG5oYW5oLCBoYXkgbmhhbmggY3VhIHBhY2tl'
'dCBLSEFDIGNoYW0gY3VuZyB0ZXA6CiAgICAgICAgIyBraG9uZyBtYW5nIGNhIG1vaSBuYW8gY3VhIGcyIHRoaSBraG9uZyBw'
'aGFpIHVuZyB2aWVuLiBEb2Mga2hvbmcgZHVvYyAoTm9uZSkgY3VuZyB2YXkuCiAgICAgICAga2V0KCJONycga2ljaCB0aHVv'
'YyIsIEtERCwgZiJkb2kgdHVvbmcga2hvbmcgcGhhaSB1bmcgdmllbjoge2xlbihoYW5nKX0gdGVwLCBjaGFtIHtjaGFtfSwg'
'Y2EgbW9pICIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBmImcyIG1hbmcgdmFvIHttYW5nIXJ9IOKAlCBk'
'YSBsYW5kPyBuaGFtIG5oYW5oPyBwYWNrZXQga2hhYz8iKQogICAgZWxzZToKICAgICAgICAjIG51bXN0YXQgaW4gYC1gIChr'
'aG9uZyBjbyBzbyBkb25nKSBjaG8gdGVwIGJpbmFyeS8tZGlmZiB0aGVvIGF0dHJpYnV0ZXMg4oCUIGtlIGNhIGF0dHJpYnV0'
'ZXMgQ1VBIE5HVU9JIERPIChkbyB0cmVuCiAgICAgICAgIyAyMDI2LTA5LTMwZzogY29yZS5hdHRyaWJ1dGVzRmlsZSBgKi5w'
'eSAtZGlmZmAgPT4gIjIgdGVwIC8gKzAiIERBVCBjaG8gMGVhOTVkZSwgdGhhdCArMzk3KS4gYC1gIGxhIEtIT05HIERPIERV'
'T0MsCiAgICAgICAgIyBraG9uZyBwaGFpIDA7IFRSVU9UIHRoZW8gc28gdGVwIC8gc28gZG9uZyBEQSBkZW0gZHVvYyB2YW4g'
'Z2l1IChxdWFuIHNhdCB0cnVjIHRpZXApLgogICAgICAgIGtob25nX3NvID0gW2hbMl0gZm9yIGggaW4gaGFuZyBpZiBub3Qg'
'KGhbMF0uaXNkaWdpdCgpIGFuZCBoWzFdLmlzZGlnaXQoKSldOyBnaGkoInRlcF9raG9uZ19zb19kb25nIiwga2hvbmdfc28p'
'CiAgICAgICAgdnVvdCA9IGxlbihoYW5nKSA+IFRSQU5fVEVQIG9yIHRoZW0gPiBUUkFOX0RPTkcKICAgICAgICBrZXQoIk43'
'JyBraWNoIHRodW9jIiwgVFJVT1QgaWYgdnVvdCBlbHNlIChLREQgaWYga2hvbmdfc28gZWxzZSBEQVQpLAogICAgICAgICAg'
'ICBmIntsZW4oaGFuZyl9IHRlcCAvICt7dGhlbX0iICsgKGYiIOKAlCBudW1zdGF0IEtIT05HIGNvIHNvIGRvbmcgY2hvIHtr'
'aG9uZ19zb30iIGlmIGtob25nX3NvIGVsc2UgIiIpKQoKIyBDb25nIGtpY2ggdGh1b2MgUEhBSSBkZSBsYWkgTU9UIGtldCBx'
'dWEuIExlbmggbnVtc3RhdCBob25nIHRoaSBuaGFuaCBgaWYgcmM6IHBhc3NgIGtob25nIGdoaSBnaSwgdmEgdmFuZyBtYXQg'
'byBkYXkKIyB0aGFuaCBEQVQgbyBibyBnb3A6IGNhdSBoaW5oIGRpZmYgQ1VBIE5HVU9JIERPIGhvbmcgKGRpZmYub3JkZXJG'
'aWxlIHRybyB0ZXAga2hvbmcgY28sIGRpZmYuYWxnb3JpdGhtIGdvIHNhaSA9PiByYz0xMjgpIGNobwojIC0tY2hpLWtpY2gt'
'dGh1b2MgcmM9MCB2b2kgMCBjaG90LCBsdW90IGRheSBkdSAiREFUIDExIiByYz0wIChkbyB0cmVuIDIwMjYtMDktMzBoLCAw'
'ZWE5NWRlKS4gVmFuZyBtYXQgbGEgS0hPTkcgRE8gRFVPQy4KIyBUdSAzMGogbnVtc3RhdCBsYSBkaWZmLXRyZWUgKGtob25n'
'IGRvYyBoYWkga2hvYSBheSk7IGR1b25nIGNvbiBsYWkgZG8gZHVvYzogZGlmZi5yZW5hbWVMaW1pdCBnbyBzYWkgPT4gcmM9'
'MTI4LgppZiBub3QgYW55KGNbMF0gPT0gIk43JyBraWNoIHRodW9jIiBmb3IgYyBpbiBjaG90KToKICAgIGtldCgiTjcnIGtp'
'Y2ggdGh1b2MiLCBLREQsIGYiY29uZyBLSE9ORyByYSBrZXQgcXVhIChnaXQgZGlmZi10cmVlIC0tbnVtc3RhdCByYz17cmN9'
'KToge19hbl91c2VyaW5mbyhlcilbOjcwXX0iKQoKIyBEaW5oIGRhbmggVEhBVCBuYW0gbyBONycgKGNhIG1vaSBnMiBtYW5n'
'IHZhbyksIEtIT05HIG8gImhhdSBkdWUgZzEiOiBnMSBkYSBsYW5kIG5lbiBtb2kgbmhhbmggZGV1CiMgbGEgaGF1IGR1ZS4g'
'RG9uZyBkYXUga2hvaSBkYW4gcGhhaSB0dSBraGFpIHRoZW8ga2V0IHF1YSBheSAoZG8gZHVvYzogbWFzdGVyIDQ0NjIwZTgg'
'bW8ga2hvaSBiYW5nCiMgIlRIRSBIRSBETyBEVU9DOiBnMiIsIEpTT04gInRoZV9oZSI6ICJnMiIsIHRyb25nIGtoaSBONycg'
'ZGEga2V0IGx1YW4gImtob25nIHBoYWkgdW5nIHZpZW4iKS4KIyBOaGFuIGNoaSBkdW9jIG5vaSBEVU5HIGNhaSBkbyBkdW9j'
'OiBgW11gIGtob25nIHRhY2ggImRhIGxhbmQiIGtob2kgIm5oYW0gbmhhbmgiLyJwYWNrZXQga2hhYyIgKGRvCiMgZHVvYyB0'
'cmVuIDIwMjYtMDktMzBiOiB1bmcgdmllbiAyYTY3OTY4IERBIExBTkQgYmkgZ29pICJLSE9ORyBwaGFpIHVuZyB2aWVuIGcy'
'IikuCmlmIHRoZV9oZSA9PSAiZzIiIGFuZCBub3Qgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKToKICAgIHRoZV9oZSA9'
'ICgiS0hPTkcgbWFuZyBjYSBtb2kgZzIgbmFvIChkYSBsYW5kPyBuaGFtIG5oYW5oPyBwYWNrZXQga2hhYz8pIiBpZiBzby5n'
'ZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpID09IFtdCiAgICAgICAgICAgICAgZWxzZSAiZzI/IChDSFVBIGRpbmggZGFuaCBk'
'dW9jIGRvaSB0dW9uZykiKQogICAgZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCgojIENvbmcgbmhhbmg6IGRvIFJJRU5HIGtpY2gg'
'dGh1b2MgKHZhaSBnaWF5KSByb2kgZHVuZy4gRHVuZyBraGkgY2FuIHhhYyBtaW5oIGxhaQojIHZlIG5lbiBtYSBraG9uZyBt'
'dW9uIHRyYSAyMC00NSBwaHV0IGNobyBjYSBibyB0ZXN0LgppZiAiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Y6CiAg'
'ICBpbm4oIiIpOyBpbm4oIj0iICogNzgpCiAgICBpbm4oIi0tY2hpLWtpY2gtdGh1b2M6IENISSBkbyBjb25nIGtpY2ggdGh1'
'b2MuIERheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5naGllbSB0aHUuIikKICAgIGlubigiLSIgKiA3OCkKICAgIGZvciBfdCwg'
'X3R0LCBfY3QgaW4gY2hvdDogaW5uKGYiICB7X3R0OjE0fSB7X3R9IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikp'
'CiAgICBfayA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCiAgICBfciA9IHN1bSgxIGZvciBfLCB0'
'LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKICAgIHN5cy5leGl0KDMgaWYgX2sgZWxzZSAoMSBpZiBfciBlbHNlIDApKQoK'
'Q0hJX1BST0JFID0gIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndiAgICAjIGJvIHF1YSBibyB0ZXN0ICsgTjc7IGdpdSAwLCAx'
'LCAzCiMgLS0tLS0tLS0tLS0tLS0tLSAyLiBibyB0ZXN0IGRheSBkdSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElfUFJP'
'QkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjIuIEJPIFRFU1QgREFZIERVICgxMC00MCBwaHV0KSIpCiAg'
'ICByY19uLCBvdXRfbiA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIGdvYykKICAgIGdoaSgicmNfc3Vp'
'dGUiLCByY19uKQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dF9uKQogICAgaW5uKCIgIHJjID0iLCByY19uLCAifCIsIG0u'
'Z3JvdXAoMCkgaWYgbSBlbHNlICIoS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCkiKQogICAgaWYgbToKICAgICAgICBn'
'aGkoImRhdCIsIGludChtLmdyb3VwKDEpKSk7IGdoaSgidHJlbiIsIGludChtLmdyb3VwKDIpKSk7IGdoaSgiYm9fcXVhX3Nv'
'IiwgaW50KG0uZ3JvdXAoNCkpKQogICAgZG9faGV0LCBnYywgdGluID0gZG9jX2RvKG91dF9uKQogICAgZ2hpKCJzb19jYV9k'
'byIsIGxlbihkb19oZXQpKTsgZ2hpKCJsaWV0X2tlX2RheV9kdSIsIHRpbikKICAgIGZvciBnIGluIGdjOiBpbm4oIiAgICoi'
'LCBnKQogICAgaW5uKCIiKTsgaW5uKGYiICA9PT0ge2xlbihkb19oZXQpfSBDQSBETyA9PT0iKQogICAgZm9yIHQgaW4gc29y'
'dGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAgICBpbm4oZiIgICB7dC5zcGxpdCgnXycpWzBdOjd9IHt0fSIpOyBpbm4o'
'ZiIgICAgICAgICAgIHtkb19oZXRbdF1bOjE1MF19IikKICAgIGdoaSgiZG9fbHlfZG8iLCB7dDogZG9faGV0W3RdWzozMDBd'
'IGZvciB0IGluIGRvX2hldH0pCiAgICAjIC0tLS0gQ0hPVDogbW9pIGNhIERPIHBoYWkgR0lBSSBUSElDSCBEVU9DIC0tLS0K'
'ICAgICMgVGhpZXUgY2hvdCBuYXksIGJvIGRvIGluIGRhbmggc2FjaCBkbyByb2kgdmFuIHRob2F0IHJjPTAuIERvIGR1bmcg'
'bGEgbG9pIGRhIHhheSByYToKICAgICMgbHVvdCBXaW5kb3dzIDE5LTA5IGNvIHQxNzEgRE8gbWEgYm8gZG8gYmFvICJEQVQg'
'MTAgfCBUUlVPVCAwIiB2YSByYz0wLgogICAgZGVmIF9raG9hKHQpOiByZXR1cm4gdC5zcGxpdCgiXyIpWzBdCiAgICBkb19w'
'YWNrZXQsIGRvX2xhLCBkb190aGlldV9jb25nX2N1ID0gW10sIFtdLCBbXQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwg'
'a2V5PXNvX2NhKToKICAgICAgICBrLCBseSA9IF9raG9hKHQpLCBkb19oZXRbdF0KICAgICAgICBpZiBrIGluIENBX1BBQ0tF'
'VDogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb19wYWNrZXQuYXBwZW5kKHQpCiAgICAgICAgZWxpZiAiS0jDlE5H'
'IMSQTyDEkMav4buiQyIgaW4gbHkgb3IgInRoaeG6v3UgYCIgaW4gbHk6ICBkb190aGlldV9jb25nX2N1LmFwcGVuZCh0KQog'
'ICAgICAgIGVsaWYgayBpbiBOR09BSV9QSEFNX1ZJOiAgICAgICAgICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICBlbHNl'
'OiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb19sYS5hcHBlbmQodCkKICAgIGdoaSgiZG9f'
'cGFja2V0IiwgZG9fcGFja2V0KTsgZ2hpKCJkb19sYSIsIGRvX2xhKTsgZ2hpKCJkb190aGlldV9jb25nX2N1IiwgZG9fdGhp'
'ZXVfY29uZ19jdSkKICAgIGlubigiIikKICAgIGlubihmIiAgY2EgRE8gdGh1b2MgQ0hJTkggcGFja2V0IG5heSA6IHtbX2to'
'b2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XSBvciAna2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERPIG5nb2FpIHBoYW0g'
'dmkgKHIzIGtoYWkpOiB7W19raG9hKHgpIGZvciB4IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSkgaWYgX2tob2EoeCkg'
'aW4gTkdPQUlfUEhBTV9WSV19IikKICAgIGlubihmIiAgY2EgRE8gdmkgVEhJRVUgQ09ORyBDVSAgICAgICA6IHtbX2tob2Eo'
'eCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV0gb3IgJ2tob25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBMQSAoa2hv'
'bmcgZ2lhaSB0aGljaCBkdW9jKToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV0gb3IgJ2tob25nIGNvJ30iKQogICAgIyAt'
'LS0tIENIT1Q6IHBoZXAgZG8gcGhhaSBUUk9OIHRydW9jIGtoaSBtb3QgY2h1IERBVCBuYW8gZHVvYyBwaGF0IC0tLS0KICAg'
'ICMgQmFuIHRydW9jIGNoaSBJTiBgdGluYC9gcmNfc3VpdGVgOiBibyB0ZXN0IGNoZXQgZ2l1YSB0MTcxIChyYz0xMzQsIGto'
'b25nIGRvbmcgdG9uZykKICAgICMgdmFuIHJhICJEQVQgMTIgfCBUUlVPVCAwIiByYz0wOyBjYSBQQUNLRVQgdmFuZyBtYXQg'
'aGF5IGJpIEJPIFFVQSBjdW5nIGR1b2MgY2hhbSBuaHUKICAgICMgImtob25nIGRvIi4gVmFuZyBtYXQga2hvbmcgcGhhaSAi'
'a2hvbmcgZG8iIOKAlCBsYSBLSE9ORyBETyBEVU9DLgogICAgdmFuZyA9IFt0IGZvciB0IGluIHNvcnRlZChDQV9QQUNLRVQs'
'IGtleT1zb19jYSkgaWYgbWF1X2NhKG91dF9uLCB0KSBub3QgaW4gKCJRVUEiLCAiRE8iKV0KICAgIGx5X2tkZCA9IFtdCiAg'
'ICBpZiBub3QgdGluOiBseV9rZGQuYXBwZW5kKCJkYW5oIHNhY2ggZG8gS0hPTkcgZGF5IGR1IikKICAgIGlmIHJjX24gbm90'
'IGluICgwLCAxKSBvciAocmNfbiA9PSAxKSAhPSBib29sKGRvX2hldCk6CiAgICAgICAgbHlfa2RkLmFwcGVuZChmInJjIGJv'
'IHRlc3Q9e3JjX259IGtob25nIGtob3Age2xlbihkb19oZXQpfSBjYSBETyBkb2MgZHVvYyIpCiAgICBpZiB2YW5nOiBseV9r'
'ZGQuYXBwZW5kKGYiY2EgUEFDS0VUIHZhbmcvYm8gcXVhOiB7dmFuZ30iKQogICAgZ2hpKCJjYV9wYWNrZXRfdmFuZyIsIHZh'
'bmcpOyBnaGkoImx5X2RvX2NodWFfdHJvbiIsIGx5X2tkZCkKICAgIGlmIGx5X2tkZDoga2V0KCJCbyB0ZXN0IGNoYXkgVFJP'
'TiB2YSBkb2MgRFUiLCBLREQsICI7ICIuam9pbihseV9rZGQpKQogICAgY2h1YV90cm9uID0gS0REIGlmIGx5X2tkZCBlbHNl'
'IERBVAogICAga2V0KCJLaG9uZyBjYSBuYW8gY3VhIFBBQ0tFVCBiaSBETyIsIGNodWFfdHJvbiBpZiBub3QgZG9fcGFja2V0'
'IGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX3BhY2tldCBlbHNlIGYiRE86IHtbX2tob2EoeCkgZm9yIHggaW4g'
'ZG9fcGFja2V0XX0g4oCUIGJhbiB2YSBDSFVBIHhvbmciKQogICAga2V0KCJNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVv'
'YyIsIGNodWFfdHJvbiBpZiBub3QgZG9fbGEgZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9fbGEgZWxzZSBmImxh'
'OiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXX0iKQogICAgaWYgZG9fdGhpZXVfY29uZ19jdToKICAgICAgICBrZXQoIkNv'
'bmcgY3UgZGF5IGR1IGRlIGRvIiwgS0RELCBmInRoaWV1IGNvbmcgY3UgY2hvIHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhp'
'ZXVfY29uZ19jdV19IikKCiAgICBicSA9IHNvcnRlZCh7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXRfbil9'
'LCBrZXk9c29fY2EpOyBnaGkoImNhX2JvX3F1YSIsIGJxKQogICAgaW5uKCIiKTsgaW5uKGYiICBCTyBRVUEgKHtsZW4oYnEp'
'fSk6IHtbeC5zcGxpdCgnXycpWzBdIGZvciB4IGluIGJxXX0iKQoKICAgIGlubigiIik7IGlubigiICBOMS1ONCAodDE2NS10'
'MTY4KSwgdGlldSBjaGkgbmdoaWVtIHRodSBjdWEgcjIsIG5heSBsYSBjaGkgYmFvIGhvaSBxdXk6IikKICAgIGI0ID0ge3Q6'
'IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0FNT0l9OyBnaGkoImNhX21vaSIsIGI0KQogICAgZm9yIHQgaW4gQ0FNT0k6'
'IGlubihmIiAgICAge3R9OiB7YjRbdF19IikKICAgICMgQk9fUVVBL3ZhbmcgbGEgQ0hVQSBDSEFZLCBraG9uZyBwaGFpIERP'
'OiBjaGkgbW90IGNhIERPIG1vaSBkdW9jIHBoYXQgVFJVT1QuCiAgICBrZXQoIk4xLU40ICh0MTY1LXQxNjgpIiwgREFUIGlm'
'IGFsbCh2ID09ICJRVUEiIGZvciB2IGluIGI0LnZhbHVlcygpKQogICAgICAgIGVsc2UgKFRSVU9UIGlmIGFueSh2ID09ICJE'
'TyIgZm9yIHYgaW4gYjQudmFsdWVzKCkpIGVsc2UgS0REKSwgc3RyKGI0KSkKCiAgICBpbm4oIiIpOyBpbm4oIiAgMTUgY2Eg'
'dHVuZyBkbyB0cmVuIENJOiIpCiAgICBiMTUgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQTE1fTsgZ2hpKCJj'
'YTE1IiwgYjE1KQogICAgaW5uKCIgICAgIiArICIgICIuam9pbihmInt0fTp7YjE1W3RdfSIgZm9yIHQgaW4gQ0ExNSkpCgog'
'ICAgIyB0MTM2IOKAlCBOMTIgZG8gR0lBTiBUSUVQIHF1YSBrZXQgcXVhIGNhCiAgICB0MTM2X3RlbiA9IG5leHQoKHQgZm9y'
'IHQgaW4gZG9faGV0IGlmIHQuc3RhcnRzd2l0aCgidDEzNiIpKSwgTm9uZSkKICAgIGlmIGIxNS5nZXQoInQxMzYiKSA9PSAi'
'UVVBIjoKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBEQVQsICJ0MTM2IFFVQSIpCiAgICBlbGlm'
'IGIxNS5nZXQoInQxMzYiKSAhPSAiRE8iOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIEtERCwg'
'ZiJ0MTM2ID0ge2IxNS5nZXQoJ3QxMzYnKSFyfSDigJQga2hvbmcgY2hheS9raG9uZyB0aGF5IikKICAgIGVsc2U6CiAgICAg'
'ICAgbHkgPSBkb19oZXQuZ2V0KHQxMzZfdGVuLCAiIikKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSki'
'LCBUUlVPVCwgZiJETzoge2x5Wzo5MF19IikKCiMgLS0tLS0tLS0tLS0tLS0tLSAzLiBwcm9iZSBUSEFORyB2YW8gaGFtIC0t'
'LS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIzLiBQUk9CRSBUSEFORyDigJQgZ29pIF9naXRf'
'd2luZG93cyB2b2kgdGhhbSBzbyB0aWVtIikKc3BlYyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9u'
'KCJscDU0MSIsIHN0cih0ZXApKQpscCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9h'
'ZGVyLmV4ZWNfbW9kdWxlKGxwKQpzaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShscC5fZ2l0X3dpbmRvd3MpCmdoaSgidGhhbV9z'
'b19fZ2l0X3dpbmRvd3MiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKaW5uKCIgIHRoYW0gc28gY3VhIF9naXRfd2luZG93czoi'
'LCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKCmRlZiBnb2koKiprdyk6CiAgICAiIiJHb2kgX2dpdF93aW5kb3dzLCBCQVQgc3Rk'
'ZXJyIGRlIG1vdCBkb25nIGNoYW4gZG9hbiBraG9uZyBnaWV0IGx1b3QgZG8uIiIiCiAgICBlID0gaW8uU3RyaW5nSU8oKQog'
'ICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICByID0gbHAuX2dpdF93aW5kb3dzKCoqa3cp'
'CiAgICByZXR1cm4gciwgZS5nZXR2YWx1ZSgpCgojIC0tLSBkb2kgY2h1bmcgcmlnOiBwaGFpIHRyYSBsb2kgZHVuZyBtb3Qg'
'Y2EgdGEgQklFVCBUUlVPQyBkYXAgYW4gLS0tCndpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAg'
'IG5nb2FpID0gUGF0aCh0KS8ibmdvYWkiOyBuZ29haS5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7'
'IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAobmdvYWkvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5j'
'b2Rpbmc9InV0Zi04IikKICAgIHIxLCBfID0gZ29pKHBhdGg9c3RyKG5nb2FpKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBj'
'd2Q9c3RyKGN3KSkKICAgIChjdy8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjIs'
'IF8gPSBnb2kocGF0aD1zdHIoY3cpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQpyaWdfb2sgPSBib29s'
'KHIxKSBhbmQgcjIgaXMgTm9uZQpnaGkoInJpZ19kb2lfY2h1bmciLCByaWdfb2spCmtldCgiUklHIGRvaSBjaHVuZyAoYmll'
'dCB0cnVvYyBkYXAgYW4pIiwgREFUIGlmIHJpZ19vayBlbHNlIEtERCwKICAgIGYibmdvYWktY3dkLT57J05IQU4nIGlmIHIx'
'IGVsc2UgJ05vbmUnfSB8IHRyb25nLWN3ZC0+eydOSEFOJyBpZiByMiBlbHNlICdOb25lJ30iKQppZiBub3QgcmlnX29rOgog'
'ICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiByaWcgc2FpLCBtb2kgY2hvdCBkdW9pIHNlIHZvIG5naGlhLiIpOyBz'
'eXMuZXhpdCgzKQoKIyAtLS0gTU9JIENPTkcgUEhBSSBUVSBDSFVORyBNSU5IIE5PIENPIFRIRSBETyAtLS0KIyBCYWkgaG9j'
'IGRhdCBuaGF0IGN1YSBwYWNrZXQgbmF5OiBkb19uMTAgYmFuIGN1IGNoYW0gREFUIGNobyA5NTgzMTY4NSB0cm9uZyBraGkg'
'dDE3MQojIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQgdGF0IG1hIE4xMCBzaW5oIHJhIGRlIGJhdC4g'
'Tm8gZGVnZW5lcmF0ZSDigJQKIyB0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgbmVuICJ0YWNoIGR1bmciIHZh'
'ICJ0YWNoIHNhaSIgY2hvIGN1bmcga2V0IHF1YS4KIyBNb3QgY29uZyBraG9uZyB0aGUgRE8gdGhpIGtob25nIHBoYWkgY29u'
'ZywgdmEgbm8gbmd1eSBoaWVtIGhvbiBraG9uZyBjbyBjb25nOiBubwojIHBoYXQgcmEgbW90IGNodSBEQVQuCiMKIyBOZW4g'
'dHJ1b2Mga2hpIERVTkcgbmFtIGNvbmcgbmF5IGRlIHBoYW4gcXV5ZXQsIGJhdCB0dW5nIGNvbmcgZ2lldCBtb3QgZG90IGJp'
'ZW4gZGEKIyBiaWV0IHRyb25nLiBDb25nIG5hbyBraG9uZyBnaWV0IGR1b2MgdGhpIGNodSBEQVQgY3VhIG5vIGJpIEhBIHh1'
'b25nIEtIT05HIERPIERVT0M7CiMgVFJVT1QgZ2l1IG5ndXllbiAocXVhbiBzYXQgdHJ1YyB0aWVwLCB2ZC4gZzEgdmFuIG5o'
'YW4gZ2l0LmJhdCkuIERvdCBiaWVuIGNoYXkgdHJlbiBCQU4gU0FPIFRBTTsgY2F5IHRoYXQga2hvbmcgYmkKIyBkdW5nIHRv'
'aSAoY3VuZyBreSBsdWF0IG5odSBONykuCkRPVF9CSUVOX1RVX0tJRU0gPSBbCiAgICAoIk44IiwgIm9wcy9sZWFzZV9wdWJs'
'aXNoLnB5IiwKICAgICAnaWYgY2hpX2RpbmggYW5kIFBhdGgoY2hpX2RpbmgpLm5hbWUubG93ZXIoKSA9PSAiZ2l0LmV4ZSIg'
'YW5kIGhvcF9sZShjaGlfZGluaCk6JywKICAgICAiaWYgY2hpX2RpbmggYW5kIGhvcF9sZShjaGlfZGluaCk6IiksCiAgICAo'
'Ik45IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAiZCA9IGRfcmF3LnN0cmlwKCkuc3RyaXAoJ1wiJykiLCAiZCA9'
'IGRfcmF3LnN0cmlwKCkiKSwKICAgICgiTjEwIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAic2VwID0gb3MucGF0'
'aHNlcCBpZiBwaGFuX2NhY2ggaXMgTm9uZSBlbHNlIHBoYW5fY2FjaCIsICJzZXAgPSBvcy5wYXRoc2VwIiksCiAgICAoIk4x'
'MSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsICJpZiBjaGFuX2RvYW4gaXMgbm90IE5vbmU6IiwgImlmIEZhbHNlOiIpLAog'
'ICAgKCJOMTIiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSIsCiAgICAgJ2dpdF9wYXRoPSIvL2tob25nLWNvL2dpdCIn'
'LCAnZ2l0X3BhdGg9Ii9raG9uZy1jby9naXQiJyksCl0KaW5uKCIiKTsgaW5uKCIgIHR1IGtpZW0gY29uZyDigJQgbW9pIGNv'
'bmcgcGhhaSBnaWV0IGR1b2MgbW90IGRvdCBiaWVuIGRhIGJpZXQ6IikKZ2lldCA9IHt9CmZvciBtYSwgZHVvbmcsIHRpbSwg'
'dGhheSBpbiBET1RfQklFTl9UVV9LSUVNOgogICAgX3RlbiwgX2hhbSA9IG5leHQoKChhLCBiKSBmb3IgYSwgYiBpbiBQUk9C'
'RSBpZiBhLnN0YXJ0c3dpdGgobWEgKyAiICIpKSwgKE5vbmUsIE5vbmUpKQogICAgaWYgX2hhbSBpcyBOb25lOgogICAgICAg'
'IGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBraG9uZyB0aW0gdGhheSBwcm9iZSB0'
'ZW4gJ3ttYX0gLi4uJyIpOyBjb250aW51ZQogICAgdHJ5OgogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0'
'b3J5KCkgYXMgX3Q6CiAgICAgICAgICAgIF9jID0gUGF0aChfdCkvImNheSI7IHNodXRpbC5jb3B5dHJlZShnb2MvIm9wcyIs'
'IF9jLyJvcHMiKQogICAgICAgICAgICBfZiA9IF9jL2R1b25nOyBfbmQgPSBfZi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04'
'IikKICAgICAgICAgICAgaWYgX25kLmNvdW50KHRpbSkgIT0gMToKICAgICAgICAgICAgICAgIGdpZXRbbWFdID0gTm9uZQog'
'ICAgICAgICAgICAgICAgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBtYXUgZG90IGJpZW4ga2hvcCB7X25kLmNv'
'dW50KHRpbSl9IGxhbiAobW9uZyAxKSIKICAgICAgICAgICAgICAgICAgICBmIiDigJQgbWEgbmd1b24gZGEgZG9pLCBkb3Qg'
'YmllbiBuYXkgaGV0IHkgbmdoaWEiKTsgY29udGludWUKICAgICAgICAgICAgX2Yud3JpdGVfdGV4dChfbmQucmVwbGFjZSh0'
'aW0sIHRoYXksIDEpLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zy'
'b21fZmlsZV9sb2NhdGlvbigibHBfZGJfIiArIG1hLCBzdHIoX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgICAg'
'ICAgICAgX20gPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUo'
'X20pCiAgICAgICAgICAgIGRlZiBfZ29pX2RiKCoqa3cpOgogICAgICAgICAgICAgICAgX2UgPSBpby5TdHJpbmdJTygpCiAg'
'ICAgICAgICAgICAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKF9lKToKICAgICAgICAgICAgICAgICAgICBy'
'ZXR1cm4gX20uX2dpdF93aW5kb3dzKCoqa3cpLCBfZS5nZXR2YWx1ZSgpCiAgICAgICAgICAgIF90dCwgX2N0LCBfID0gX2hh'
'bShfZ29pX2RiLCBpbnNwZWN0LnNpZ25hdHVyZShfbS5fZ2l0X3dpbmRvd3MpLAogICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgZ2lldFttYV0gPSAoX3R0ID09IFRSVU9U'
'KQogICAgICAgIGlubihmIiAgICB7bWE6NH0gZG90IGJpZW4gLT4ge190dDoxNH0geydHSUVUIERVT0MnIGlmIF90dCA9PSBU'
'UlVPVCBlbHNlICdTT05HIFNPVCd9IgogICAgICAgICAgICArIChmIiAgICh7X2N0fSkiIGlmIF9jdCBlbHNlICIiKSkKICAg'
'IGV4Y2VwdCBFeGNlcHRpb24gYXMgX2U6CiAgICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05H'
'IERPIERVT0M6IHt0eXBlKF9lKS5fX25hbWVfX306IHtfZX0iKQpnaGkoImNvbmdfZ2lldF9kdW9jX2RvdF9iaWVuIiwgZ2ll'
'dCkKCmZvciB0ZW4sICh0dCwgY3QsIGRsKSBpbiBbKHQsIGYoZ29pLCBzaWcsIHRlcHQpKSBmb3IgdCwgZiBpbiBQUk9CRV06'
'CiAgICBnaGkoInByb2JlXyIgKyB0ZW4uc3BsaXQoKVswXS5sb3dlcigpLCBkbCkKICAgIGlmIGlzaW5zdGFuY2UoZGwsIGRp'
'Y3QpOgogICAgICAgIGZvciBrLCB2IGluIGRsLml0ZW1zKCk6IGlubihmIiAgICB7azozNH06IHt2fSIpCiAgICBtYSA9IHRl'
'bi5zcGxpdCgpWzBdCiAgICBpZiBnaWV0LmdldChtYSkgaXMgbm90IFRydWUgYW5kIHR0ID09IERBVDoKICAgICAgICAjIERB'
'VCB0dSBtb3QgY29uZyBjaHVhIGNodW5nIG1pbmggZHVvYyBsYSBiaWV0IERPIHRoaSBraG9uZyBkYW5nIHRpbiBob24gS0RE'
'LgogICAgICAgIGtldCh0ZW4sIEtERCwgZiJjb25nIEtIT05HIGdpZXQgZHVvYyBkb3QgYmllbiBjdWEgY2hpbmggbm8gKHtn'
'aWV0LmdldChtYSkhcn0pIgogICAgICAgICAgICAgICAgICAgICAgZiIgLT4gY2h1IERBVCBuYXkga2hvbmcgY28gZ2lhIHRy'
'aSIpCiAgICBlbHNlOgogICAgICAgIGtldCh0ZW4sIHR0LCBjdCkKCiMgLS0tLS0tLS0tLS0tLS0tLSA0LiBONyBkb3QgYmll'
'biB0cmVuIEJBTiBTQU8gVEFNIC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigi'
'LSIgKiA3OCk7IGlubigiNC4gTjcg4oCUIGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gKGNheSB0aGF0IEtIT05HIGJpIGR1'
'bmcgdG9pKSIpCiAgICB0cnVvYyA9IHRlcC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTikKICAg'
'IGdoaSgibjdfdHJ1b2MiLCB0cnVvYyk7IGlubihmIiAgc28gZG9uZyBraG9wIHtNQVVfV0lOIXJ9OiBUUlVPQyA9IHt0cnVv'
'Y30gW21vbmcgMV0iKQogICAgaWYgdHJ1b2MgIT0gMToKICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3Mi'
'LCBLREQsIGYibWF1IHh1YXQgaGllbiB7dHJ1b2N9IGxhbiwga2hvbmcgcGhhaSAxIikKICAgIGVsc2U6CiAgICAgICAgd2l0'
'aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0bXA6CiAgICAgICAgICAgIHNhbyA9IFBhdGgodG1wKS8iY2F5'
'IgogICAgICAgICAgICBzaHV0aWwuY29weXRyZWUoZ29jLCBzYW8sIGlnbm9yZT1zaHV0aWwuaWdub3JlX3BhdHRlcm5zKCIu'
'Z2l0IiwgIl9fcHljYWNoZV9fIiwgIioucHljIikpCiAgICAgICAgICAgIGYyID0gc2FvLyJvcHMiLyJsZWFzZV9wdWJsaXNo'
'LnB5IgogICAgICAgICAgICBmMi53cml0ZV90ZXh0KGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5yZXBsYWNlKE1B'
'VV9XSU4sICJpZiBGYWxzZToiKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgc2F1ID0gZjIucmVhZF90ZXh0KGVu'
'Y29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4pOyBnaGkoIm43X3NhdSIsIHNhdSkKICAgICAgICAgICAgaW5uKGYiICBT'
'QVUgKGRhIGRvdCBiaWVuKSA9IHtzYXV9IFttb25nIDBdIikKICAgICAgICAgICAgaWYgc2F1ICE9IDA6CiAgICAgICAgICAg'
'ICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsICJkb3QgYmllbiBLSE9ORyBhcCBkdW9jIikKICAg'
'ICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHJjX20sIG91dF9tID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rl'
'c3QucHkiXSwgc2FvKQogICAgICAgICAgICAgICAgbTE2NSA9IG1hdV9jYShvdXRfbSwgInQxNjUiKTsgZG0sIF8sIF8gPSBk'
'b2NfZG8ob3V0X20pCiAgICAgICAgICAgICAgICB0ZW4xNjUgPSBuZXh0KCh0IGZvciB0IGluIGRtIGlmIHQuc3RhcnRzd2l0'
'aCgidDE2NSIpKSwgTm9uZSkKICAgICAgICAgICAgICAgIGx5ID0gKGRtLmdldCh0ZW4xNjUpIG9yICIiKQogICAgICAgICAg'
'ICAgICAgZ2hpKCJuN190MTY1IiwgbTE2NSk7IGdoaSgibjdfbHlfZG8iLCBseVs6MjAwXSkKICAgICAgICAgICAgICAgIGlu'
'bihmIiAgdDE2NSBzYXUgZG90IGJpZW46IHttMTY1fSB8IHtseVs6MTEwXX0iKQogICAgICAgICAgICAgICAgZHVuZ19seV9k'
'byA9ICJQQVRIIHQiIGluIGx5IG9yICIvdXNyL2JpbiIgaW4gbHkKICAgICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4g'
'bmhhbmggV2luZG93cyIsIERBVCBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKSBlbHNlCiAgICAgICAgICAgICAg'
'ICAgICAgKFRSVU9UIGlmIG0xNjUgPT0gIkRPIiBlbHNlIEtERCksCiAgICAgICAgICAgICAgICAgICAgImdpZXQgZHVuZyBs'
'eSBkbyIgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykKICAgICAgICAgICAgICAgICAgICBlbHNlICgiRE8gbmh1'
'bmcgS0hPTkcgZHVuZyBseSBkbyAtPiB0aW4gZHVuZyBnaWEiIGlmIG0xNjUgPT0gIkRPIiBlbHNlICJraG9uZyBkb2MgZHVv'
'YyB0MTY1IikpCgojIC0tLS0tLS0tLS0tLS0tLS0gS0VUIExVQU4gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIj0i'
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
