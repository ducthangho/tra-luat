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
$ShaBoDo    = '8ac72d6c2c08a5df7b9e3faaadccba8a799f43387951e4c8970ffb72b5540b24'      # SHA-256 cua bo do Python nhung ben duoi

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
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0xMC0wMWMiICAgICAgICAgICAgICAj'
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
'ZG86IDE2Ni8xNjYsIGtob25nIGxvdC4KX0dJVF9HTE9CQUxfQ0kgPSAiW2luaXRdXG5cdGRlZmF1bHRCcmFuY2ggPSBtYXN0'
'ZXJcbltjb3JlXVxuXHRhdXRvY3JsZiA9IGZhbHNlXG5cdGVvbCA9IGxmXG5cdGFiYnJldiA9IDdcbiIKZGVmIGNoYXkoYXJn'
'diwgY3dkLCBwaHV0PTYwKToKICAgIGZkLCBnYyA9IHRlbXBmaWxlLm1rc3RlbXAocHJlZml4PSJ3cDU0MS1naXRjb25maWct'
'Y2ktIiwgc3VmZml4PSIuaW5pIikKICAgIHhkZyA9IE5vbmUKICAgIHRyeToKICAgICAgICB4ZGcgPSB0ZW1wZmlsZS5ta2R0'
'ZW1wKHByZWZpeD0id3A1NDEteGRnLSIpCiAgICAgICAgd2l0aCBvcy5mZG9wZW4oZmQsICJ3IiwgZW5jb2Rpbmc9ImFzY2lp'
'IiwgbmV3bGluZT0iXG4iKSBhcyBmOiBmLndyaXRlKF9HSVRfR0xPQkFMX0NJKQogICAgICAgIG10ID0ge2s6IHYgZm9yIGss'
'IHYgaW4gb3MuZW52aXJvbi5pdGVtcygpCiAgICAgICAgICAgICAgaWYgbm90IGsudXBwZXIoKS5zdGFydHN3aXRoKCJHSVRf'
'IikgYW5kIChub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIlBZVEhPTiIpIG9yIGsudXBwZXIoKSBpbiBfUFlfR0lVKX0KICAg'
'ICAgICBtdC51cGRhdGUoUFlUSE9OVVRGOD0iMSIsIFBZVEhPTklPRU5DT0RJTkc9InV0Zi04IiwgUFlUSE9ORE9OVFdSSVRF'
'QllURUNPREU9IjEiLCBQWVRIT05VTkJVRkZFUkVEPSIxIiwKICAgICAgICAgICAgICAgICAgR0lUX0NPTkZJR19HTE9CQUw9'
'Z2MsIFhER19DT05GSUdfSE9NRT14ZGcsIFNIRUxMQ0hFQ0tfT1BUUz0iLS1ub3JjIikKICAgICAgICBwID0gc3VicHJvY2Vz'
'cy5ydW4oW3N5cy5leGVjdXRhYmxlXSArIGFyZ3YsIGN3ZD1zdHIoY3dkKSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwKICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgdGV4dD1UcnVlLCBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1l'
'b3V0PXBodXQqNjAsIGVudj1tdCkKICAgIGZpbmFsbHk6CiAgICAgICAgdHJ5OiBvcy5yZW1vdmUoZ2MpCiAgICAgICAgZXhj'
'ZXB0IE9TRXJyb3I6IHBhc3MKICAgICAgICBpZiB4ZGc6IHNodXRpbC5ybXRyZWUoeGRnLCBpZ25vcmVfZXJyb3JzPVRydWUp'
'CiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpICsgKHAuc3RkZXJyIG9yICIiKQoKZGVmIG1hdV9j'
'YShvdXQsIHQpOgogICAgbSA9IHJlLnNlYXJjaChyIig/bSlePDw8IHJhICgiICsgdCArIHIiW2Etel0/X1xTKikgWzAtOS5d'
'K3MgKFx3KylccyokIiwgb3V0KQogICAgcmV0dXJuIG0uZ3JvdXAoMikgaWYgbSBlbHNlIE5vbmUKCmRlZiBnaXQoZ29jLCAq'
'YSwgcGh1dD01KToKICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbImdpdCIsICItQyIsIHN0cihnb2MpLCAqYV0sIGNhcHR1cmVf'
'b3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwKICAgICAgICAgICAgICAgICAgICAgICBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9'
'InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjApCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpLnN0'
'cmlwKCksIChwLnN0ZGVyciBvciAiIikuc3RyaXAoKQoKCiMgPT09PT09PT09PT09PT09PT0gTkFNIFBST0JFLCB2aWV0IHRo'
'YW5oIEhBTSBUSFVBTiBkZSBUVSBLSUVNIGR1b2MgPT09PT09PT09PT09PT09PT0KIyBNb2kgaGFtIHRyYSAodHJhbmdfdGhh'
'aSwgY2hpX3RpZXQsIGR1X2xpZXUpLiBLSE9ORyBpbiwgS0hPTkcgdGhvYXQg4oCUIG5obyB2YXkgY2h1bmcKIyBjaGF5IGR1'
'b2MgdHJlbiBuZW4gQkFUIEtZLCB2YSBgLS10dS1raWVtLXByb2JlYCBnb2kgdGhhbmcgY2h1bmcgZGUga2llbSBjaGluaCBi'
'byBkby4KCmRlZiBfc2FuKHQpOgogICAgZCA9IFBhdGgodCkvImQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsg'
'Y3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIHJldHVybiBkLCBjdywgcGYKCmRlZiBkb19u'
'OChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJCdW9jIDEgKENPTkdfQ1VfR0lUKSBjaGkgZHVvYyBuaGFuIGdpdC5leGUuIERv'
'aSBjaHVuZyBkdW9uZzogZ2l0LmV4ZSBWQU4gcGhhaSBuaGFuLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5U'
'ZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICBmb3IgdGVuIGlu'
'ICgiZ2l0LmV4ZSIsICJnaXQuYmF0IiwgImdpdC5jbWQiLCAiZ2l0LnB5IiwgImtob25nLXBoYWktZ2l0LnR4dCIpOgogICAg'
'ICAgICAgICBmID0gZC90ZW47IGYud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8g'
'PSBnb2koY29uZ19jdV9naXQ9c3RyKGYpLCBwYXRoPSIiLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQog'
'ICAgICAgICAgICBrcVtmIkNPTkdfQ1VfR0lUPXt0ZW59Il0gPSAiTkhBTiIgaWYgciBlbHNlICJUVSBDSE9JIgogICAgbG90'
'ID0gW2sgZm9yIGssIHYgaW4ga3EuaXRlbXMoKSBpZiB2ID09ICJOSEFOIiBhbmQgbm90IGsuZW5kc3dpdGgoImdpdC5leGUi'
'KV0KICAgIGlmIGtxLmdldCgiQ09OR19DVV9HSVQ9Z2l0LmV4ZSIpICE9ICJOSEFOIjoKICAgICAgICByZXR1cm4gS0RELCAi'
'ZG9pIGNodW5nIGR1b25nIGhvbmc6IGdpdC5leGUgaG9wIGxlIG1hIGJpIHR1IGNob2kiLCBrcQogICAgcmV0dXJuIChEQVQg'
'aWYgbm90IGxvdCBlbHNlIFRSVU9UKSwgKCIiIGlmIG5vdCBsb3QgZWxzZSBmImNvbiBuaGFuOiB7bG90fSIpLCBrcQoKZGVm'
'IGRvX245KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIk11YyBQQVRIIGJvYyBuaGF5IGtlcCBwaGFpIE5IQU47IG11YyByb25n'
'IC8gdG9hbiBraG9hbmcgdHJhbmcgcGhhaSBibyBxdWEsIGtob25nIG5lbS4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVt'
'cGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8iY28gZ2l0IjsgZC5ta2Rpcigp'
'OyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAgICAg'
'KGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBmb3IgbmhhbiwgbXVjIGlu'
'ICgoImtob25nIG5oYXkiLCBzdHIoZCkpLCAoImNvIG5oYXkga2VwIiwgZicie2R9IicpLAogICAgICAgICAgICAgICAgICAg'
'ICAgICAgICgicm9uZyIsICIiKSwgKCJjaGkga2hvYW5nIHRyYW5nIiwgIiAgICIpKToKICAgICAgICAgICAgdHJ5OgogICAg'
'ICAgICAgICAgICAgciwgXyA9IGdvaShwYXRoPW11YywgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAg'
'ICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIk5vbmUiCiAgICAgICAgICAgIGV4'
'Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9IGYiTkVNIHt0eXBlKGUp'
'Ll9fbmFtZV9ffSIKICAgIGlmIGtxLmdldCgiUEFUSCBraG9uZyBuaGF5IikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBL'
'REQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogbXVjIFBBVEggdGh1b25nIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EK'
'ICAgIG9rID0gKGtxLmdldCgiUEFUSCBjbyBuaGF5IGtlcCIpID09ICJOSEFOIgogICAgICAgICAgYW5kIGtxLmdldCgiUEFU'
'SCByb25nIikgPT0gIk5vbmUiIGFuZCBrcS5nZXQoIlBBVEggY2hpIGtob2FuZyB0cmFuZyIpID09ICJOb25lIikKICAgIHJl'
'dHVybiAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCiMgRGF1IHBoYW4g'
'Y2FjaCBkdW5nIERFIFRIVS4gUGhhaSBLSEFDIG9zLnBhdGhzZXAgdHJlbiBDQSBIQUkgbmVuICgnOycgV2luZG93cywgJzon'
'IFBPU0lYKQojIHRoaSBoYWkgZ2lhIHRodXlldCAidGFjaCB0aGVvIGRhdSBkdW9jIHRydXllbiIgdmEgInRhY2ggdGhlbyBv'
'cy5wYXRoc2VwIiBtb2kgcm9pIHJhIG5oYXUuClRIVV9OMTAgPSAifCIKCmRlZiBkb19uMTAoZ29pLCBzaWcsIHRlcHQpOgog'
'ICAgIiIiSGFtIHBoYWkgdGFjaCBQQVRIIHRoZW8gZGF1IHBoYW4gY2FjaCBEVU9DIFRSVVlFTiwga2hvbmcgdGhlbyBvcy5w'
'YXRoc2VwIGN1YSBuZW4uCgogICAgQmFuIGN1IGRvICJtb3QgZGF1ICc7JyB0cm9uZyBURU4gdGh1IG11YyIgdmEgZGF0IERB'
'VCB0cmVuIFdpbmRvd3MgZHUgaGFtIHNhaS4gTm8KICAgIGRlZ2VuZXJhdGU6IHRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERB'
'IGxhICc7JywgbmVuICdDOi9hO2InIHRoYXQgc3UgQ08gTkdISUEgbGEgaGFpCiAgICBtdWMg4oCUICJ0YWNoIGR1bmciIHZh'
'ICJ0YWNoIHNhaSIgY2hvIHJhIGN1bmcga2V0IHF1YSwgcGhlcCBkbyBraG9uZyB0aGUgZG8gbmFvLiBObwogICAgZGEgY2hh'
'bSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQg'
'dGF0IGF5LgogICAgTW90IGNvbmcga2hvbmcgdGhlIGRvIHRoaSBraG9uZyBwaGFpIGNvbmcuCiAgICAiIiIKICAgIHRlbl9z'
'ZXAgPSBuZXh0KChrIGZvciBrIGluICgicGhhbl9jYWNoIiwgImRhdV9waGFuX2NhY2giLCAic2VwIikgaWYgayBpbiBzaWcu'
'cGFyYW1ldGVycyksIE5vbmUpCiAgICBpZiB0ZW5fc2VwIGlzIE5vbmU6CiAgICAgICAgIyBLaG9uZyBjbyB0aGFtIHNvIHRo'
'aSB0cmVuIFdpbmRvd3MgS0hPTkcgY29uIGR1b25nIG5hbyB0YWNoIGhhaSBnaWEgdGh1eWV0LgogICAgICAgIGlmIG9zLnBh'
'dGhzZXAgPT0gIjsiOgogICAgICAgICAgICByZXR1cm4gKEtERCwgInRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7'
'JyB2YSBoYW0ga2hvbmcgbmhhbiB0aGFtIHNvIGRhdSBwaGFuIGNhY2ggIgogICAgICAgICAgICAgICAgICAgICAgICAgIi0+'
'IGtob25nIHRhY2ggZHVvYyBoYWkgZ2lhIHRodXlldCIsCiAgICAgICAgICAgICAgICAgICAgeyJvcy5wYXRoc2VwIjogb3Mu'
'cGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZX0pCiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3Rvcnko'
'KSBhcyB0OgogICAgICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkKICAgICAgICAgICAgZCwgY3cs'
'IHBmID0gX3Nhbih0KQogICAgICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgi'
'KQogICAgICAgICAgICByLCBfICA9IGdvaShwYXRoPXN0cihsYSkgKyBvcy5wYXRoc2VwICsgc3RyKGQpLCBwcm9ncmFtX2Zp'
'bGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICByMCwgXyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9m'
'aWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICBrcSA9IHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFt'
'IHNvIHNlcCI6IE5vbmUsCiAgICAgICAgICAgICAgImNvIG11YyBjaHVhICc7JyI6ICJOSEFOIiBpZiByIGVsc2UgIk5vbmUi'
'LAogICAgICAgICAgICAgICJkb2kgY2h1bmcgZHVvbmcgKGtob25nIGNvICc7JykiOiAiTkhBTiIgaWYgcjAgZWxzZSAiTm9u'
'ZSJ9CiAgICAgICAgaWYgbm90IHIwOgogICAgICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmciLCBr'
'cQogICAgICAgIHJldHVybiAoREFUIGlmIHIgZWxzZSBUUlVPVCksICgiIiBpZiByIGVsc2UgIm11YyBnaXQuZXhlIGhvcCBs'
'ZSBiaSBNQVQiKSwga3EKCiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgbGEg'
'PSBQYXRoKHQpLyJjbztkYXUiOyBsYS5ta2RpcigpICAgICAgICAgICMgJzsnIG5hbSB0cm9uZyBURU4sIGtob25nIHBoYWkg'
'ZGF1IHBoYW4gY2FjaAogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3Rl'
'eHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIG5vaSA9IHN0cihsYSkgKyBUSFVfTjEwICsgc3RyKGQpCiAgICAg'
'ICAga3cgPSBkaWN0KHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgcl9jaGluaCwgXyA9IGdv'
'aShwYXRoPW5vaSwgICAgICAqKnt0ZW5fc2VwOiBUSFVfTjEwfSwgICAqKmt3KSAgICMgdGFjaCBkdW5nICAtPiBOSEFOCiAg'
'ICAgICAgcl9kdW9uZywgXyA9IGdvaShwYXRoPXN0cihkKSwgICAqKnt0ZW5fc2VwOiBUSFVfTjEwfSwgICAqKmt3KSAgICMg'
'ZG9pIGNodW5nIGR1b25nCiAgICAgICAgcl9waGFuYmlldCwgXyA9IGdvaShwYXRoPW5vaSwgICAqKnt0ZW5fc2VwOiBvcy5w'
'YXRoc2VwfSwgKiprdykgICMgdGFjaCB0aGVvIG9zLnBhdGhzZXAgLT4gbWF0CiAgICBrcSA9IHsib3MucGF0aHNlcCI6IG9z'
'LnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IHRlbl9zZXAsICJkYXUgdGh1IjogVEhVX04xMCwKICAgICAgICAgIGYibm9pIGJh'
'bmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17VEhVX04xMCFyfSI6ICAgICAgICJOSEFOIiBpZiByX2NoaW5oIGVsc2UgIk5v'
'bmUiLAogICAgICAgICAgZiJkb2kgY2h1bmcgZHVvbmcgKG1vdCBtdWMsIHt0ZW5fc2VwfT17VEhVX04xMCFyfSkiOiAgIk5I'
'QU4iIGlmIHJfZHVvbmcgZWxzZSAiTm9uZSIsCiAgICAgICAgICBmInBoYW4gYmlldDogbm9pIGJhbmcge1RIVV9OMTAhcn0s'
'IHt0ZW5fc2VwfT17b3MucGF0aHNlcCFyfSI6ICJOSEFOIiBpZiByX3BoYW5iaWV0IGVsc2UgIk5vbmUifQogICAgaWYgbm90'
'IHJfZHVvbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBtb3QgbXVjIGhvcCBsZSBtYSBr'
'aG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICAjIENvbmcgcGhhaSBDTyBUSEUgZG8uIE5ldSBjYSBoYWkgZGF1IHBoYW4g'
'Y2FjaCBkZXUgcmEgTkhBTiB0aGkgcGhlcCBkbyBraG9uZyBwaGFuCiAgICAjIGJpZXQgZHVvYyBnaSDigJQgZHVuZyBiYW8g'
'REFULCBiYW8gdGhhbmcgbGEga2hvbmcgZG8gZHVvYy4KICAgIGlmIHJfcGhhbmJpZXQ6CiAgICAgICAgcmV0dXJuIChLREQs'
'IGYicGhlcCBkbyBLSE9ORyBwaGFuIGJpZXQgZHVvYzogbm9pIGJhbmcge1RIVV9OMTAhcn0gbWEgdGFjaCB0aGVvICIKICAg'
'ICAgICAgICAgICAgICAgICAgZiJ7b3MucGF0aHNlcCFyfSBWQU4gdGltIHJhIGdpdC5leGUiLCBrcSkKICAgIHJldHVybiAo'
'KERBVCwgIiIsIGtxKSBpZiByX2NoaW5oIGVsc2UKICAgICAgICAgICAgKFRSVU9ULCBmInRhY2ggdGhlbyBvcy5wYXRoc2Vw'
'IHRoYXkgdmkgdGhlbyB7dGVuX3NlcH0gZHVvYyB0cnV5ZW4iLCBrcSkpCgoKZGVmIGRvX24xMShnb2ksIHNpZywgdGVwdCk6'
'CiAgICAiIiJUcnV5ZW4gY2hhbl9kb2FuID0+IHRodSBkdW9jIHRob25nIGJhbyBWQSBzdGRlcnIgSU0uIEtob25nIHRydXll'
'biA9PiBzdGRlcnIgVkFOIGNvLiIiIgogICAgaWYgImNoYW5fZG9hbiIgbm90IGluIHNpZy5wYXJhbWV0ZXJzOgogICAgICAg'
'IHJldHVybiBLREQsICJfZ2l0X3dpbmRvd3Mga2hvbmcgbmhhbiB0aGFtIHNvIGNoYW5fZG9hbiIsIHsidGhhbSBzbyI6IGxp'
'c3Qoc2lnLnBhcmFtZXRlcnMpfQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAg'
'IGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRm'
'LTgiKQogICAgICAgIGNkID0gW10KICAgICAgICBfLCBlX2NvID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0'
'cihwZiksIGN3ZD1zdHIoY3cpLCBjaGFuX2RvYW49Y2QpCiAgICAgICAgXywgZV9raCA9IGdvaShwYXRoPXN0cihkKSwgcHJv'
'Z3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIGtxID0geyJjaGFuX2RvYW4gdGh1IGR1b2MgKG11YykiOiBs'
'ZW4oY2QpLAogICAgICAgICAgInN0ZGVyciBraGkgQ08gY2hhbl9kb2FuIChieXRlKSI6IGxlbihlX2NvLmVuY29kZSgpKSwK'
'ICAgICAgICAgICJzdGRlcnIga2hpIEtIT05HIHRydXllbiAoYnl0ZSkiOiBsZW4oZV9raC5lbmNvZGUoKSl9CiAgICBpZiBs'
'ZW4oY2QpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA9PSAwOgogICAgICAgIHJldHVybiBLREQsICJuaGFuaCAlUHJv'
'Z3JhbUZpbGVzJSBraG9uZyBwaGFuIGdpYWkgS0hPTkcgYmF5IHJhIGNoYW4gZG9hbiBuYW8gLT4gY2h1YSBkbyBkdW9jIiwg'
'a3EKICAgIG9rID0gbGVuKGNkKSA+IDAgYW5kIGxlbihlX2NvLmVuY29kZSgpKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUo'
'KSkgPiAwCiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtx'
'CgpkZWYgZG9fbjEyKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkhhbmcgc2VudGluZWwgZ2l0X3BhdGggdHJvbmcgZml4dHVy'
'ZSBwaGFpIHR1eWV0IGRvaSB0cmVuIENBIEhBSSBuZW4uIiIiCiAgICBuZCA9IHRlcHQucmVhZF90ZXh0KGVuY29kaW5nPSJ1'
'dGYtOCIsIGVycm9ycz0icmVwbGFjZSIpCiAgICBoYW5nID0gc29ydGVkKHNldChyZS5maW5kYWxsKHInZ2l0X3BhdGhccyo9'
'XHMqIihbXiJdKykiJywgbmQpKSkKICAgIHhhdSA9IFtoIGZvciBoIGluIGhhbmcgaWYgbm90IChQdXJlUG9zaXhQYXRoKGgp'
'LmlzX2Fic29sdXRlKCkgYW5kIFB1cmVXaW5kb3dzUGF0aChoKS5pc19hYnNvbHV0ZSgpKV0KICAgIGtxID0geyJoYW5nIGdp'
'dF9wYXRoIHRpbSB0aGF5IjogaGFuZywgImNoaSB0dXlldCBkb2kgTU9UIG5lbiI6IHhhdX0KICAgIGlmIG5vdCBoYW5nOgog'
'ICAgICAgIHJldHVybiBLREQsICJraG9uZyB0aW0gdGhheSBoYW5nIGdpdF9wYXRoIG5hbyB0cm9uZyBmaXh0dXJlIC0+IG1h'
'dSBkb2MgY28gdGhlIGRhIGRvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgeGF1IGVsc2UgVFJVT1QpLCAoIiIgaWYg'
'bm90IHhhdSBlbHNlIGYiY2hpLW1vdC1uZW46IHt4YXV9IiksIGtxCgpQUk9CRSA9IFsoIk44IGJ1b2MgMSBjaGkgbmhhbiBn'
'aXQuZXhlIiwgZG9fbjgpLAogICAgICAgICAoIk45IGJvYyBuaGF5IGtlcCBvIG11YyBQQVRIIiwgZG9fbjkpLAogICAgICAg'
'ICAoIk4xMCBkYXUgJzsnIHRyb25nIHRlbiB0aHUgbXVjIiwgZG9fbjEwKSwKICAgICAgICAgKCJOMTEgY2hhbiBkb2FuIGRv'
'aSBrZW5oIiwgZG9fbjExKSwKICAgICAgICAgKCJOMTIgaGFuZyBzZW50aW5lbCB0dXlldCBkb2kgQ0EgSEFJIG5lbiIsIGRv'
'X24xMildCgojIC0tLSBjaGUgZG8gVFUgS0lFTTogY2hheSBuYW0gcHJvYmUgdHJlbiBtb3QgY2F5IGJhdCBreSwgbmVuIGJh'
'dCBreSAtLS0KaWYgIi0tdHUta2llbS1wcm9iZSIgaW4gc3lzLmFyZ3Y6CiAgICBfZyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFy'
'Z3YuaW5kZXgoIi0tdHUta2llbS1wcm9iZSIpICsgMV0pLnJlc29sdmUoKQogICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3Bl'
'Y19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX3RrIiwgc3RyKF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICBfbHAg'
'PSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX2xwKQogICAg'
'X3NpZyA9IGluc3BlY3Quc2lnbmF0dXJlKF9scC5fZ2l0X3dpbmRvd3MpCiAgICBkZWYgX2dvaSgqKmt3KToKICAgICAgICBl'
'ID0gaW8uU3RyaW5nSU8oKQogICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgICAg'
'IHJldHVybiBfbHAuX2dpdF93aW5kb3dzKCoqa3cpLCBlLmdldHZhbHVlKCkKICAgIHByaW50KGYiVFUgS0lFTSBQUk9CRSB0'
'cmVuIHtfZ30gIChuZW4ge3N5cy5wbGF0Zm9ybX0pIikKICAgIGZvciBfdGVuLCBfZiBpbiBQUk9CRToKICAgICAgICBfdHQs'
'IF9jdCwgX2RsID0gX2YoX2dvaSwgX3NpZywgX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcHJp'
'bnQoZiIgIFt7X3R0OjE0fV0ge190ZW59IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICAgICAgZm9yIF9r'
'LCBfdiBpbiAoX2RsIG9yIHt9KS5pdGVtcygpOiBwcmludChmIiAgICAgICAge19rOjM0fToge192fSIpCiAgICBzeXMuZXhp'
'dCgwKQoKIyAtLS0gY2hlIGRvIEtJRU0gRE9ORyBCTzogdGVwIC5weSBuYXkgcGhhaSBUUlVORyBUVU5HIEJZVEUgdm9pIGJh'
'biBuaHVuZyB0cm9uZyBwczEgLS0tCiMgS2hvbmcgY29uZyBuYW8gYnVvYyBoYWkgYmFuIHNhbyBraG9wOiBkbyBkdW9jLCBu'
'b2kgdHJhbiAyLzQwMCAtPiA5OS85OTk5OSBDSEkgdHJvbmcgLnB5CiMgdGhpIGNpX2Rhbmdfa3kgbGFuIHQyNi90MjcgdmFu'
'IHhhbmgsIGNvbiBjaG90IFNIQSBjdWEgcHMxIGNoaSBzbyBiYW4gbmh1bmcgdm9pIGhhbmcgc28KIyBjdWEgQ0hJTkggbm8u'
'IENoYXk6IHB5dGhvbiB3cDU0MS1kby1nMi13aW5kb3dzLnB5IC0ta2llbS1kb25nLWJvIHdwNTQxLWRvLWcyLnBzMSAgKHJj'
'IDB8MykKaWYgIi0ta2llbS1kb25nLWJvIiBpbiBzeXMuYXJndjoKICAgIGltcG9ydCBiYXNlNjQKICAgIF9wcyA9IFBhdGgo'
'c3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0ta2llbS1kb25nLWJvIikgKyAxXSkucmVhZF90ZXh0KGVuY29kaW5nPSJhc2Np'
'aSIpCiAgICBfbSA9IHJlLnNlYXJjaChyIig/bXMpXlwkQjY0ID0gQFwoKC4qPyleXCkiLCBfcHMpCiAgICBfayA9IHJlLnNl'
'YXJjaChyIig/bSleXCRTaGFCb0RvXHMqPVxzKicoWzAtOWEtZl17NjR9KSciLCBfcHMpCiAgICBfbmh1bmcgPSBiYXNlNjQu'
'YjY0ZGVjb2RlKCIiLmpvaW4ocmUuZmluZGFsbChyIicoW0EtWmEtejAtOSsvPV0qKSciLCBfbS5ncm91cCgxKSkpKSBpZiBf'
'bSBlbHNlIGIiIgogICAgX3RvaSA9IFBhdGgoX19maWxlX18pLnJlYWRfYnl0ZXMoKQogICAgX29rID0gYm9vbChfbSBhbmQg'
'X2spIGFuZCBfbmh1bmcgPT0gX3RvaSBhbmQgaGFzaGxpYi5zaGEyNTYoX3RvaSkuaGV4ZGlnZXN0KCkgPT0gX2suZ3JvdXAo'
'MSkKICAgIGlubihmIktJRU0gRE9ORyBCTzoge0RBVCBpZiBfb2sgZWxzZSBLRER9ICAobmh1bmcge2xlbihfbmh1bmcpfSBi'
'eXRlLCB0ZXAge2xlbihfdG9pKX0gYnl0ZSkiKQogICAgc3lzLmV4aXQoMCBpZiBfb2sgZWxzZSAzKQoKaW5uKCI9IiAqIDc4'
'KTsgaW5uKCJXUDU0MSBnMiAtIHBoZXAgZG8gdHJlbiBXaW5kb3dzIHRoYXQgKHNwZWMgcjM6IE4xLU40LCBOOC1OMTIsIE43'
'LCBraWNoIHRodW9jKSIpOyBpbm4oIj0iICogNzgpCgojIC0tLS0tLS0tLS0tLS0tLS0gdHUga2llbSBibyBkb2MgLS0tLS0t'
'LS0tLS0tLS0tLQpfZCwgX2csIF90ID0gZG9jX2RvKF9NQVUpCl9vayA9IChsZW4oX2QpID09IDIgYW5kIGFueSh4LnN0YXJ0'
'c3dpdGgoInQwMmIiKSBmb3IgeCBpbiBfZCkKICAgICAgIGFuZCBub3QgYW55KHguc3RhcnRzd2l0aCgidDEzMSIpIGZvciB4'
'IGluIF9kKSBhbmQgX3QpCmlubigiVHUga2llbSBibyBkb2MgbG9nOiIsIERBVCBpZiBfb2sgZWxzZSBUUlVPVCkKaWYgbm90'
'IF9vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogYm8gZG9jIGxvZyBjdWEgY2hpbmggc2NyaXB0IG5heSBz'
'YWkgLT4ga2hvbmcgZG8gZ2kgY2EuIik7IHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMC4gbmVuIGRvIC0tLS0t'
'LS0tLS0tLS0tLS0KZ29jID0gUGF0aChzeXMuYXJndlsxXSkucmVzb2x2ZSgpIGlmIGxlbihzeXMuYXJndikgPiAxIGVsc2Ug'
'UGF0aC5jd2QoKQp0ZXAsIHRlcHQgPSBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoLnB5IiwgZ29jIC8gIm9wcyIgLyAi'
'bGVhc2VfcHVibGlzaF90ZXN0LnB5Igppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjAuIE5FTiBETyIpCiMgTU9JIExP'
'RyBQSEFJIFRVIEtIQUkgbm8gZG8gQ0FJIEdJIGJhbmcgQk8gRE8gTkFPLiBCYWkgaG9jIDE5LTA5LTIwMjY6IG1vdCBsdW90'
'IGRvCiMgZ3VpIHZlIGR1b2MgZG9jIG5odSBrZXQgcXVhIGN1YSBiYW4gdmEgZGFuZyB4ZXQsIG5odW5nIHRoYXQgcmEgbGEg'
'YmFuIGRvIENVIGNoYXkKIyB0cmVuIG5oYW5oIEtIQUMuIERvYyByYSB0aGkgbWF0IG1vdCB2b25nOyBsb2cgdHUga2hhaSB0'
'aGkgdGhheSBuZ2F5IGRvbmcgZGF1Lgp0cnk6CiAgICBfdHUgPSBoYXNobGliLnNoYTI1NihQYXRoKF9fZmlsZV9fKS5yZWFk'
'X2J5dGVzKCkpLmhleGRpZ2VzdCgpCmV4Y2VwdCBFeGNlcHRpb24gYXMgX2U6CiAgICBfdHUgPSBmImtob25nIHR1IGJhbSBk'
'dW9jOiB7X2V9IgpnaGkoImJvX2RvX3NoYTI1NiIsIF90dSkKaW5uKGYiICBCTyBETyAgICAgICAgOiBzaGEyNTYge190dVs6'
'MTZdfSAgKGJhbiB7QkFOX0JPX0RPfSkiKQppbm4oIiAgc3lzLnBsYXRmb3JtIDoiLCBzeXMucGxhdGZvcm0sICJ8IHB5dGhv'
'biIsIHN5cy52ZXJzaW9uLnNwbGl0KClbMF0pCmlubigiICBvcy5wYXRoc2VwICAgOiIsIHJlcHIob3MucGF0aHNlcCksICJ8'
'IFBBVEhFWFQ6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUEFUSEVYVCIpKVs6NjBdKQppbm4oIiAgUHJvZ3JhbUZpbGVzIDoi'
'LCByZXByKG9zLmVudmlyb24uZ2V0KCJQcm9ncmFtRmlsZXMiKSksICJ8IFN5c3RlbVJvb3Q6IiwgcmVwcihvcy5lbnZpcm9u'
'LmdldCgiU3lzdGVtUm9vdCIpKSkKaW5uKCIgIENPTkdfQ1VfR0lUICA6IiwgcmVwcihfQ09OR19DVV9HSVRfTkdVT0lfRE8p'
'CiAgICArICgiICAtPiBEQSBCTyBraG9pIGx1b3QgZG8gKENJIGtob25nIGRhdCBiaWVuIG5heTsgeGVtIGRhdSB0ZXApIiBp'
'ZiBfQ09OR19DVV9HSVRfTkdVT0lfRE8gaXMgbm90IE5vbmUgZWxzZSAiIikpCmdoaSgiY29uZ19jdV9naXRfbmd1b2lfZG8i'
'LCBfQ09OR19DVV9HSVRfTkdVT0lfRE8pCmlubigiICBnb2Mga2hvICAgICAgOiIsIGdvYykKCnF1eWVuID0gTm9uZQppZiBz'
'eXMucGxhdGZvcm0gPT0gIndpbjMyIjoKICAgIHRyeToKICAgICAgICBpbXBvcnQgY3R5cGVzOyBxdXllbiA9IGJvb2woY3R5'
'cGVzLndpbmRsbC5zaGVsbDMyLklzVXNlckFuQWRtaW4oKSkKICAgIGV4Y2VwdCBFeGNlcHRpb246IHF1eWVuID0gTm9uZQpn'
'aGkoInF1eWVuX2FkbWluIiwgcXV5ZW4pCnN5bWxpbmtfZHVvYyA9IE5vbmUKdHJ5OgogICAgd2l0aCB0ZW1wZmlsZS5UZW1w'
'b3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJhLnR4dCI7IGQud3JpdGVfdGV4dCgieCIsIGVu'
'Y29kaW5nPSJ1dGYtOCIpCiAgICAgICAgdHJ5OiBvcy5zeW1saW5rKHN0cihkKSwgc3RyKFBhdGgodCkvImxrIikpOyBzeW1s'
'aW5rX2R1b2MgPSBUcnVlCiAgICAgICAgZXhjZXB0IE9TRXJyb3IgYXMgZTogc3ltbGlua19kdW9jID0gRmFsc2U7IGdoaSgi'
'c3ltbGlua19sb2kiLCBmInt0eXBlKGUpLl9fbmFtZV9ffToge2V9IikKZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOiBnaGkoInN5'
'bWxpbmtfbG9pIiwgc3RyKGUpKQpnaGkoInN5bWxpbmtfZHVvYyIsIHN5bWxpbmtfZHVvYykKaW5uKCIgIEFkbWluaXN0cmF0'
'b3I6IiwgcXV5ZW4sICJ8IHRhbyBzeW1saW5rIGR1b2M6Iiwgc3ltbGlua19kdW9jKQoKbG9pID0gW10KIyBDb25nIGtpY2gg'
'dGh1b2MgbGEgcGhlcCBkbyB0cmVuIExJQ0ggU1UgR0lULCBraG9uZyBkaW5oIGdpIGRlbiBuZW4uIENobyBwaGVwCiMgLS1j'
'aGkta2ljaC10aHVvYyBjaGF5IG8gbW9pIG5lbiBkZSBjb24gVFUgS0lFTSBkdW9jIGNoaW5oIGNvbmcgbmF5IChkYSBkdW5n'
'CiMgZGUgdGFpIGR1bmcgY2EgaGFpIHZlIGN1YSBzdSBjbyBuZW4tY3UgMTktMDkpLiBNb2kgY2hvdCBDSFVDIE5BTkcgdmFu'
'IGRvaSBXaW5kb3dzLgppZiBzeXMucGxhdGZvcm0gIT0gIndpbjMyIiBhbmQgIi0tY2hpLWtpY2gtdGh1b2MiIG5vdCBpbiBz'
'eXMuYXJndjoKICAgIGxvaS5hcHBlbmQoZiJLSE9ORyBwaGFpIFdpbmRvd3MgKHN5cy5wbGF0Zm9ybT17c3lzLnBsYXRmb3Jt'
'IXJ9KSIpCmlmIG5vdCB0ZXAuaXNfZmlsZSgpOiAgbG9pLmFwcGVuZChmImtob25nIHRoYXkge3RlcH0iKQppZiBub3QgdGVw'
'dC5pc19maWxlKCk6IGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB0fSIpCmlmIG5vdCBzaHV0aWwud2hpY2goImdpdCIp'
'OiBsb2kuYXBwZW5kKCJraG9uZyBjbyBgZ2l0YCB0cm9uZyBQQVRIIikKIyBCbyB0ZXN0IChtdWMgMiB2YSBONykgY2FuIFB5'
'WUFNTDogdGhpZXUgbm8sIDBlYTk1ZGUgcmEgOTYvMTY2IGNhIERPICg4OSBiYW8gdGhhbmcgIk5vIG1vZHVsZSBuYW1lZCAn'
'eWFtbCciLAojIDcgcXVhIGx1b3QgY29uOyBjbyBQeVlBTUw6IDE2Ni8xNjYgUVVBKS4gQm8gZG8gZ29pIGNodW5nIGxhICJj'
'YSBETyBMQSIgcm9pIHBoYXQgVFJVT1Qg4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGMuCiMgRGlldSBraWVuIHRpZW4gcXV5ZXQg'
'cGhhaSBob2kgYmFuZyBDSElOSCB0aWVuIHRyaW5oIGNvbiBzZSBjaGF5IGJvIHRlc3QgKGNoYXkoKTogY3VuZyBtb2kgdHJ1'
'b25nOyBjd2QgPSBvcHMvID0KIyBzeXMucGF0aFswXSBjdWEgYm8gdGVzdCkgdmEgaG9pIERVTkcgRFVPQyBjaHUga2hvbmcg'
'aG9pIENPIE1BVC4gQmFuIDMwZCBob2kgYGZpbmRfc3BlYygieWFtbCIpYCBvIHRpZW4gdHJpbmgKIyBOQVkgdmEgbmd1b25n'
'IDMuOCBzdXkgdHUgTkdVIFBIQVAgKGA6PWApIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBkLCBjYSBoYWkgcmEgcmM9MSBUUlVP'
'VCBjaG8gdW5nIHZpZW4gc2FjaDoKIyB0aHUgbXVjIGR1IGxpZXUgYHlhbWwvYCB0cmVuIFBZVEhPTlBBVEggcXVhIGZpbmRf'
'c3BlYyBtYSBgeWFtbC5zYWZlX2R1bXBgIGtob25nIGNvICg4NyBjYSAibGEiKTsgcHl0aG9uIDMuOC4yMAojIFRIQVQgY28g'
'UHlZQU1MLCBibyB0ZXN0IGR1bmcgYHN0ci5yZW1vdmVwcmVmaXhgICgzLjkpIGx1YyBDSEFZICgzMyBjYSAibGEiOyAzLjku'
'MjM6IDE2Ni8xNjYpLgojICJEdW5nIGR1b2MiIG5naGlhIGxhIGR1bmcgRFVORyBBUEkgYm8gdGVzdCBnb2k6IHZpZXQoKSAo'
'NDMgbG9pIGdvaSkgdmEgbGVhc2VfcHVibGlzaC5weSBnb2kgc2FmZV9kdW1wKC4uLiwgYWxsb3dfdW5pY29kZT1UcnVlLAoj'
'IHNvcnRfa2V5cz1GYWxzZSksIG1hIGBzb3J0X2tleXNgIGNoaSBjbyB0dSBQeVlBTUwgNS4xLiBEbyB0cmVuIDIwMjYtMDkt'
'MzBsLCAwZWE5NWRlOiBweXRob24gMy45LjIzICsgUHlZQU1MIDMuMTMgVEhBVCBxdWEgcHJvYmUKIyBjdSAocmM9MCksIGJv'
'IHRlc3QgMTA5LzE2NiDigJQgNTYgY2EgImxhIjogNTIgYHVuZXhwZWN0ZWQga2V5d29yZCBhcmd1bWVudCAnc29ydF9rZXlz'
'J2AsIHQyNi90MjcgYFJlYWRlckVycm9yYCAoa3kgdHUgbmdvYWkgQk1QKSwKIyB0MTI0L3QxNTMgRE8gdGhlbyBsdW90IGNv'
'biDigJQgZTJlIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgOyBQeVlBTUwgNS4xOiAxNjYvMTY2IChkbyBsYWkgMjAyNi0xMC0w'
'MTogY3VuZyBzbykuCiMgKFB5dGhvbiA+PSAzLjEwICsgUHlZQU1MIDMuMTMgZGEgdHJ1b3QgcHJvYmUgY3UgdmkgYGNvbGxl'
'Y3Rpb25zLkhhc2hhYmxlYC4pIFByb2JlIGN1YSBwczEgKCRtYVRodSkgcGhhaSBHSU9ORyBIRVQgZG9uZyBkdW9pLgppZiBu'
'b3QgKCItLWNoaS1raWNoLXRodW9jIiBpbiBzeXMuYXJndiBvciAiLS1jaGktcHJvYmUiIGluIHN5cy5hcmd2KToKICAgIF9y'
'Y19kaywgX3JhX2RrID0gY2hheShbIi1jIiwgImltcG9ydCBzeXM7IHN5cy5leGl0KDkpIGlmIHN5cy52ZXJzaW9uX2luZm8g'
'PCAoMywgOSkgZWxzZSBOb25lOyBpbXBvcnQgeWFtbDsiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgeWFt'
'bC5zYWZlX2R1bXAoeWFtbC5zYWZlX2xvYWQoJ2E6IDEnKSwgYWxsb3dfdW5pY29kZT1UcnVlLCBzb3J0X2tleXM9RmFsc2Up'
'Il0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgZ29jIC8gIm9wcyIgaWYgKGdvYyAvICJvcHMiKS5pc19kaXIoKSBlbHNl'
'IFBhdGguY3dkKCksIHBodXQ9MikKICAgIGlmIF9yY19kayA9PSA5OgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24ge3N5'
'cy52ZXJzaW9uLnNwbGl0KClbMF19IDwgMy45OiBibyB0ZXN0IGN1YSB1bmcgdmllbiBkdW5nIHN0ci5yZW1vdmVwcmVmaXgg'
'KDMuOSkgbHVjIENIQVkiKQogICAgZWxpZiBfcmNfZGs6CiAgICAgICAgbG9pLmFwcGVuZChmInB5dGhvbiBuYXkgS0hPTkcg'
'Y28gUHlZQU1MIGR1bmcgZHVvYyAoeyhfcmFfZGsuc3RyaXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFdWzo5MF19KToi'
'CiAgICAgICAgICAgICAgICAgICBmIiBcIntzeXMuZXhlY3V0YWJsZX1cIiAtbSBwaXAgaW5zdGFsbCAtVSBweXlhbWwiCiAg'
'ICAgICAgICAgICAgICAgICAiIChiYW4gbmh1bmcgcHMxIHR1IHRhaSBLSE9ORyBjbyBwaXA6IGNoYXkgbGFpIHZvaSAtUHkg'
'PHB5dGhvbiBkYSBjbyBQeVlBTUw+KSIpCiAgICAjIEJvIHRlc3QgY29uIGdvaSBgc2h1dGlsLndoaWNoYCBjaG8gYmFzaC9h'
'Y3Rpb25saW50L3NoZWxsY2hlY2sgKDBlYTk1ZGU6IHQzMyB0MTM3IHQxNTkgY2FuIGFjdGlvbmxpbnQsIHQxMzcgY2FuCiAg'
'ICAjIHNoZWxsY2hlY2ssIGNhYyBjYSBjaGF5IG9wcy9jYWlfYWN0aW9ubGludC5zaCBjYW4gYmFzaCkuIFRoaWV1IHRoaSBj'
'YWMgY2EgYXkgaW4gIktIT05HIERPIERVT0M6IHRoaWV1IGAuLi5gIiB2YSBibyBkbyByYQogICAgIyByYz0zIOKAlCBuaHVu'
'ZyBjaGkgU0FVIGNhIGJvIHRlc3QgbGFuIE43IChkbyB0cmVuIDIwMjYtMDktMzBnLCBQQVRIIHRoaWV1IGFjdGlvbmxpbnQ6'
'IGBDb25nIGN1IGRheSBkdSBkZSBkb2AgS0RELCByYz0zCiAgICAjIHNhdSAyIGx1b3QgYm8gdGVzdCkuIEN1bmcgbHkgZG8g'
'UHlZQU1MIGR1b2MgaG9pIG8gZGF5OiBob2kgVFJVT0MsIGN1bmcgUEFUSCBtYSBjaGF5KCkgdHJ1eWVuIGNobyBibyB0ZXN0'
'LgogICAgIyBWQSBjdW5nIENITyBibyB0ZXN0IGR1bmc6IHRyZW4gV2luZG93cyBgc2h1dGlsLndoaWNoYCB0cmEgVEhVIE1V'
'QyBISUVOIEhBTkggVFJVT0MgUEFUSCwgbWEgYm8gdGVzdCBjaGF5IHZvaSBjd2QgPSBnb2MgY29uCiAgICAjIHRpZW4gdHJp'
'bmggbmF5IGR1bmcgbyBjd2QgQ1VBIE5HVU9JIERPIChub2kgZ29pIHBzMSwgdmQuIERvd25sb2FkcyDigJQgZHVuZyBub2kg'
'Z2lhaSBuZW4gYWN0aW9ubGludC5leGUpLiBEbyB0cmVuIDIwMjYtMDktMzBrCiAgICAjIChuaGFuaCB3aW4zMiBUSEFUIGN1'
'YSBzaHV0aWwud2hpY2gpOiBhY3Rpb25saW50IHRvdCBvIGN3ZCBuZ3VvaSBkbyArIGJhbiBob25nIGRhdSBQQVRIID0+IG11'
'YyAwIGhvaSBiYW4gbyBjd2QgKHJjPTApLCBibyB0ZXN0CiAgICAjIGR1bmcgYmFuIHRyZW4gUEFUSCA9PiByYz0xIGBEQVQg'
'MTEgfCBUUlVPVCAxYCwgYGxhOiBbJ3QzMycsICd0MTM3JywgJ3QxNTknXWAuIEdpYWkgdGVuIHZvaSBjd2QgPSBnb2Mgcm9p'
'IGdvaSBUSEFORyBiYW5nIGR1b25nCiAgICAjIFRVWUVUIERPSSBkYSBnaWFpIChxdWEgaGFuIHRoaSBydW4oKSBnaWV0IGR1'
'bmcgdGllbiB0cmluaCDigJQgbHkgZG8gYmFuIDMwaSBraG9uZyBob2kgcXVhIGNoYXkoKSkuCiAgICBfY3dkX25ndW9pX2Rv'
'ID0gb3MuZ2V0Y3dkKCkKICAgIHRyeToKICAgICAgICBpZiBnb2MuaXNfZGlyKCk6IG9zLmNoZGlyKGdvYykKICAgICAgICBf'
'Y2MgPSB7YzogKG9zLnBhdGguYWJzcGF0aChwKSBpZiBwIGVsc2UgTm9uZSkgZm9yIGMsIHAgaW4KICAgICAgICAgICAgICAg'
'KChjLCBzaHV0aWwud2hpY2goYykpIGZvciBjIGluICgiYmFzaCIsICJhY3Rpb25saW50IiwgInNoZWxsY2hlY2siKSl9CiAg'
'ICBmaW5hbGx5OgogICAgICAgIG9zLmNoZGlyKF9jd2Rfbmd1b2lfZG8pCiAgICBfdGhpZXVfY2MgPSBbYyBmb3IgYywgcCBp'
'biBfY2MuaXRlbXMoKSBpZiBub3QgcF0KICAgIGlmIF90aGlldV9jYzoKICAgICAgICBsb2kuYXBwZW5kKGYidGhpZXUgY29u'
'ZyBjdSBibyB0ZXN0IGdvaSBxdWEgUEFUSDoge190aGlldV9jY30gKGFjdGlvbmxpbnQ6IG9wcy9jYWlfYWN0aW9ubGludC5z'
'aCB2b2kgQUxfVkVSOyIKICAgICAgICAgICAgICAgICAgICIgYmFzaDogR2l0IEJhc2gsIGtob25nIHBoYWkgYmFzaC5leGUg'
'Y3VhIFdTTCkiKQogICAgIyBzaGVsbGNoZWNrIEtIT05HIG5oYW4gLS1ub3JjIHRoaSBhY3Rpb25saW50IDEuNy43ICh0dSB0'
'cnV5ZW4gLS1ub3JjKSBsYW0gdDMzIERPLCB2YSBTSEVMTENIRUNLX09QVFM9LS1ub3JjIGN1YSBjaGF5KCkgbGFtCiAgICAj'
'IHQxMzcgRE8g4oCUIGNhICJsYSIgPT4gVFJVT1QgZ2lhIChkbyB0cmVuIDIwMjYtMDktMzBoLCBzaGVsbGNoZWNrIGdpYSB0'
'dSBjaG9pIC0tbm9yYzogYmFuIDMwaCByYz0xIGBsYTogWyd0MzMnXWAgc2F1IGNhCiAgICAjIGJvIHRlc3QpLiBgd2hpY2hg'
'IGNoaSBob2kgQ08gTUFUOyBvIGRheSBob2kgRFVORyBEVU9DLiBOZ3VvbmcgZG8gdHJlbiBzaGVsbGNoZWNrIFRIQVQ6IDAu'
'NC43LzAuNS4wLzAuNi4wIHR1IGNob2kgLS1ub3JjCiAgICAjIChyYz0zKSwgMC43LjAgdHJvIGxlbiBuaGFuLiBQaGVwIGhv'
'aSBwaGFpIHRoYXkgRFVORyBTSEVMTENIRUNLX09QVFMgbWEgY2hheSgpIGRhdCBjaG8gbHVvdCBjb246IGJhbiAzMGkgaG9p'
'IHZvaSBiaWVuIENVQQogICAgIyBOR1VPSSBETyDigJQgZG8gdHJlbiAyMDI2LTA5LTMwaSwgc2hlbGxjaGVjayAwLjkuMCAr'
'IFNIRUxMQ0hFQ0tfT1BUUz0tLWV4dGVuZGVkLWFuYWx5c2lzPXRydWUgKGNvIGN1YSAwLjEwKTogcmM9MyAia2hvbmcgbmhh'
'bgogICAgIyAtLW5vcmM6IGNhcCBuaGF0IHNoZWxsY2hlY2siIHRyb25nIGtoaSB0MzMvdDEzNyBxdWEgY2hheSgpIGRldSAx'
'LzEuIEdvaSBUSEFORyAoa2hvbmcgcXVhIGNoYXkoKSk6IHF1YSBoYW4gdGhpIHJ1bigpIGdpZXQKICAgICMgZHVuZyBzaGVs'
'bGNoZWNrOyBxdWEgY2hheSgpIHRoaSBjaGkgZ2lldCBweXRob24gY29uLCBzaGVsbGNoZWNrIHRyZW8gbyBsYWkgbW8gY29p'
'IChkbyB0cmVuIDIwMjYtMDktMzBpOiAxLzEgY29uIHNvbmcpLgogICAgZWxpZiBzdWJwcm9jZXNzLnJ1bihbX2NjWyJzaGVs'
'bGNoZWNrIl0sICItLW5vcmMiLCAiLS12ZXJzaW9uIl0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRpbWVvdXQ9NjAsCiAgICAg'
'ICAgICAgICAgICAgICAgICAgIGVudj1kaWN0KG9zLmVudmlyb24sIFNIRUxMQ0hFQ0tfT1BUUz0iLS1ub3JjIikpLnJldHVy'
'bmNvZGU6CiAgICAgICAgbG9pLmFwcGVuZCgic2hlbGxjaGVjayB0cmVuIFBBVEgga2hvbmcgbmhhbiAtLW5vcmMgKGFjdGlv'
'bmxpbnQgMS43LjcgdmEgY2hheSgpIGRldSB0cnV5ZW4gY28gYXkpOiBjYXAgbmhhdCBzaGVsbGNoZWNrIikKICAgICMgYWN0'
'aW9ubGludCBjdW5nIHBoYWkgRFVORyBEVU9DLCBraG9uZyBjaGkgQ08gTUFUOiB0MzMvdDEzNy90MTU5IGdvaSBubyBUSEFO'
'RywgdmEgbW90IGFjdGlvbmxpbnQga2hvbmcgY2hheSAoc2FpIGtpZW4gdHJ1YywKICAgICMgaG9uZykgbGFtIGNhIGJhIERP'
'ICJhY3Rpb25saW50IERPIChyYz0uLi4pIiDigJQgY2EgImxhIiA9PiBUUlVPVCBnaWEgc2F1IGNhIGJvIHRlc3QgKGRvIHRy'
'ZW4gMjAyNi0wOS0zMGo6IGFjdGlvbmxpbnQgZ2lhCiAgICAjIHJjPTEgPT4gbXVjIDAgaW0gbGFuZywgdDMzICJsYSIpLiBC'
'YW4gVEhBVCAxLjYuMjcvMS43LjcvMS43LjgvMS43LjEyIGRldSByYz0wIHZhIGRldSBjaG8gdDMzL3QxMzcvdDE1OSBRVUEg'
'dHJlbiAwZWE5NWRlLgogICAgIyBiYXNoIHF1YSBgd2hpY2hgIENISSBob2kgQ08gTUFULCBjbyBjaHUgZGljaDogdDM1LXQ0'
'MCBnb2kgYGJhc2hgIFRSQU4gKGJhc2ggV1NMIGxhbSBjaHVuZyBETywgZGV1IE5HT0FJX1BIQU1fVkkg4oCUIGRvIHRyZW4K'
'ICAgICMgMjAyNi0wOS0zMGopLiA5IGNhIFRST05HIHBoYW0gdmkgS0hPTkcgZ29pIGJhc2ggcXVhIGB3aGljaGAg4oCUIHhl'
'bSBjaG90IGBfYmFzaF9wb3NpeCgpYCBkdW9pIGNob3QgZ2l0LgogICAgIyBDSEFZIERVT0MgY2h1YSBwaGFpIERVTkcgRFVP'
'QzogZG8gdHJlbiAyMDI2LTA5LTMwaywgMGVhOTVkZSwgYWN0aW9ubGludCBUSEFUIDEuNC4zLzEuNS4wLzEuNS4zLzEuNi4w'
'LzEuNi44LzEuNi4xNS8xLjYuMjAvCiAgICAjIDEuNi4yMiBkZXUgYC12ZXJzaW9uYCByYz0wLCBtYSBjYSB0YW0gbGFtIHQx'
'MzcvdDE1OSBETyAoYHByb3BlcnR5ICJydW5fYXR0ZW1wdCIvIndvcmtmbG93X3NoYSIgaXMgbm90IGRlZmluZWRgKSwgMS40'
'LjMvMS41LjAKICAgICMgdGhlbSB0MzMgKGBtdXN0IGJlIGNvbnRhaW5lZCB3aXRoaW4gJHt7IH19YCkg4oCUIGUyZSAxLjYu'
'MjI6IHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgLCBgbGE6IFsndDEzNycsICd0MTU5J11gIGNobyB1bmcgdmllbgogICAgIyBz'
'YWNoOyAxLjYuMjMvMS42LjI0LzEuNi4yNi8xLjYuMjcvMS43LjAvMS43LjYvMS43LjcvMS43LjEyIFFVQSBjYSBiYS4gU2Fu'
'IGxhIGJhbgogICAgIyBnaGltIENJIChBTF9TQU4pLCBLSE9ORyBwaGFpIDEuNi4yMyBkbyB0cmVuIE1PVCB1bmcgdmllbjog'
'd29ya2Zsb3cgY3VhIHVuZyB2aWVuIHNhdSBjbyB0aGUgZHVuZyBjdSBwaGFwIG1vaSBob24sIG1hIENJIGNoaSBkbwogICAg'
'IyBiYW5nIGJhbiBnaGltLiBDdSBob24gc2FuID0+IEtIT05HIERPIERVT0MgKGNoYW4gY2EgMS42LjIzLTEuNy42IGRhbmcg'
'UVVBOiBmYWlsLWNsb3NlLCBraG9uZyBwaGFpIHBoYW4gcXV5ZXQpLiBgdmAgZGF1OiBiYW4KICAgICMgYGdvIGluc3RhbGxg'
'IGluIGB2MS43LjdgOyBraG9uZyBkb2MgZHVvYyBzbyAodmQuIGAoZGV2ZWwpYCkgPT4gS0hPTkcgRE8gRFVPQy4KICAgIGlm'
'IG5vdCBfdGhpZXVfY2M6CiAgICAgICAgX2FsID0gc3VicHJvY2Vzcy5ydW4oW19jY1siYWN0aW9ubGludCJdLCAiLXZlcnNp'
'b24iXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLCBlbmNvZGluZz0idXRmLTgiLAogICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9NjApCiAgICAgICAgX2FsX3YgPSByZS5zZWFyY2gociIo'
'P20pXnY/KFxkKylcLihcZCspXC4oXGQrKSIsIF9hbC5zdGRvdXQgb3IgIiIpCiAgICAgICAgaWYgX2FsLnJldHVybmNvZGU6'
'CiAgICAgICAgICAgIGxvaS5hcHBlbmQoImFjdGlvbmxpbnQgdHJlbiBQQVRIIGNvIG1hdCBuaHVuZyBgYWN0aW9ubGludCAt'
'dmVyc2lvbmAgcmMhPTAgKGtob25nIGNoYXkgZHVvYyk6IGNhaSBsYWkgYmFuIGdoaW0gQUxfVkVSIikKICAgICAgICBlbGlm'
'IG5vdCBfYWxfdiBvciB0dXBsZShpbnQoeCkgZm9yIHggaW4gX2FsX3YuZ3JvdXBzKCkpIDwgQUxfU0FOOgogICAgICAgICAg'
'ICBsb2kuYXBwZW5kKGYiYWN0aW9ubGludCB7X2FsX3YuZ3JvdXAoMCkgaWYgX2FsX3YgZWxzZSAnKGtob25nIGRvYyBkdW9j'
'IHBoaWVuIGJhbiknfSBjdSBob24gYmFuIGdoaW0gQ0kgIgogICAgICAgICAgICAgICAgICAgICAgIGYieycuJy5qb2luKG1h'
'cChzdHIsIEFMX1NBTikpfSAoQUxfVkVSKTogYmFuIGN1IGxhbSB0MTM3L3QxNTkgRE8gJ2xhJyB0cmVuIHVuZyB2aWVuIHNh'
'Y2gg4oCUIgogICAgICAgICAgICAgICAgICAgICAgICIgY2FpIGJhbiBnaGltIChvcHMvY2FpX2FjdGlvbmxpbnQuc2ggdm9p'
'IEFMX1ZFUikiKQogICAgICAgICMgZ2l0IGN1bmcgdGhlOiBDTyBNQVQga2hvbmcgcGhhaSBEVU5HIERVT0MsIHZhIGdpdCBD'
'VSBsYSBjb25nIGN1IFBITyBCSUVOIG5oYXQgdHJvbmcgYm9uLiBEbyB0cmVuIDIwMjYtMDktMzBsLCAwZWE5NWRlLCBnaXQK'
'ICAgICAgICAjIFRIQVQgcXVhIGN1bmcgY2hheSgpOiAyLjI1LjEgPT4gMTQwLzE2NiAoMjMgY2EgImxhIjogYGluaXQgLWJg'
'Li4uKSwgMi4zNC4xIHZhIDIuMzUuMSA9PiAxNjMvMTY2ICh0MTA5IHQxMTAgdDExMTogYGdpdAogICAgICAgICMgd29ya3Ry'
'ZWUgbGlzdCAtLXBvcmNlbGFpbiAtemAgcmM9MTI5IGB1bmtub3duIHN3aXRjaCB6YCksIGUyZSAyLjM1LjEgcmM9MSBgREFU'
'IDExIHwgVFJVT1QgMWA7IDIuMzYuMSA9PiAxNjYvMTY2LiBTYW4gbGF5CiAgICAgICAgIyB0dSB0aW5oIG5hbmcgbWEgQ0hJ'
'TkggbWEgZHVvYyBkbyBnb2kgKG9wcy9jb25nX2N1LnlhbWwgZGUgYmFuX2doaW0gZ2l0ID0gbnVsbCBuZW4ga2hvbmcgY28g'
'YmFuIGdoaW0gQ0kgZGUgZHVhIHZhbykuCiAgICAgICAgIyBgZ2l0IHZlcnNpb24gMi40Ny4xLndpbmRvd3MuMWAgKEdpdCBm'
'b3IgV2luZG93cykgdmEgYDIuMzkuMyAoQXBwbGUgR2l0LTE0NilgIGRldSBkb2MgZHVvYyBiYSBzbyBkYXUuCiAgICAgICAg'
'IyBWYSBwaGFpIGhvaSBEVU5HIGdpdCBtYSBibyB0ZXN0IFNFIEdPSS4gQm8gdGVzdCBLSE9ORyBgc2h1dGlsLndoaWNoKCJn'
'aXQiKWAgbmh1IGJhIGNvbmcgY3UgdHJlbjogR09JX0dJVCBjdWEgdW5nIHZpZW4gdmEgbW9pCiAgICAgICAgIyBmaXh0dXJl'
'IGdvaSBgZ2l0YCBUUkFOIOKAlCB0cmVuIFdpbmRvd3MgbGEgQ3JlYXRlUHJvY2Vzc1c6IENISSB0dSB0aGVtIGAuZXhlYCAo'
'S0hPTkcgUEFUSEVYVCksIHRyYSB0aHUgbXVjIHB5dGhvbi5leGUsIGN3ZAogICAgICAgICMgdmEgU3lzdGVtMzIgVFJVT0Mg'
'UEFUSC4gYHdoaWNoYCB0aGkgdHJhIFBBVEhFWFQsIG5lbiBtb3QgYGdpdC5jbWRgL2BnaXQuYmF0YCBkdW5nIHRydW9jIGBn'
'aXQuZXhlYCBDVSB0cmVuIFBBVEggZHVvYyBob2kKICAgICAgICAjIFRIQVkgbm8g4oCUIGRvIHRyZW4gMjAyNi0xMC0wMSAo'
'bmhhbmggd2luMzIgVEhBVCBjdWEgc2h1dGlsLndoaWNoOyBzaGltIGBnaXQuQ01EYCBtb2kgdHJ1b2MgZ2l0IDIuMzUuMSBU'
'SEFUKTogYmFuIDMwbSBtdWMgMAogICAgICAgICMgaW0sIGUyZSByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCwgYGxhOiBbJ3Qx'
'MDknLCAndDExMCcsICd0MTExJ11gLiBOZW4gaG9pIGJhbmcgQ0hJTkggZHVvbmcgYXk6IHRpZW4gdHJpbmggY29uIGN1YSBj'
'aGF5KCkKICAgICAgICAjIChjdW5nIHB5dGhvbiwgY3VuZyBtb2kgdHJ1b25nLCBjd2QgPSBnb2Mgbmh1IGJvIHRlc3QpIGdv'
'aSBgZ2l0IC0tdmVyc2lvbmAgVFJBTi4KICAgICAgICBfcmNfZ3YsIF9yYV9ndiA9IGNoYXkoWyItYyIsICJpbXBvcnQgc3Vi'
'cHJvY2Vzcywgc3lzOyBwID0gc3VicHJvY2Vzcy5ydW4oWydnaXQnLCAnLS12ZXJzaW9uJ10sIGNhcHR1cmVfb3V0cHV0PVRy'
'dWUsIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiB0ZXh0PVRydWUsIHRpbWVvdXQ9NjApOyBwcmlu'
'dChwLnN0ZG91dCk7IHN5cy5leGl0KHAucmV0dXJuY29kZSkiXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZ29j'
'IGlmIGdvYy5pc19kaXIoKSBlbHNlIFBhdGguY3dkKCksIHBodXQ9MikKICAgICAgICBfZ3ZfbSA9IHJlLnNlYXJjaChyIig/'
'bSleZ2l0IHZlcnNpb25ccysoXGQrKVwuKFxkKylcLihcZCspIiwgX3JhX2d2KQogICAgICAgIGdoaSgiZ2l0X2JvX3Rlc3Qi'
'LCBfZ3ZfbS5ncm91cCgwKSBpZiBfZ3ZfbSBlbHNlIE5vbmUpCiAgICAgICAgaW5uKCIgIGdpdCBibyB0ZXN0ICA6IiwgX2d2'
'X20uZ3JvdXAoMCkgaWYgX2d2X20gZWxzZSBmIihraG9uZyBkb2MgZHVvYyBwaGllbiBiYW4sIHJjPXtfcmNfZ3Z9KSIpCiAg'
'ICAgICAgaWYgX3JjX2d2OgogICAgICAgICAgICBsb2kuYXBwZW5kKGYiYGdpdCAtLXZlcnNpb25gIGdvaSBUUkFOIG5odSBi'
'byB0ZXN0IHJjIT0wICh7KF9yYV9ndi5zdHJpcCgpLnNwbGl0bGluZXMoKSBvciBbJyddKVstMV1bOjkwXX0pOiBjYWkgbGFp'
'IGdpdCIpCiAgICAgICAgZWxpZiBub3QgX2d2X20gb3IgdHVwbGUoaW50KHgpIGZvciB4IGluIF9ndl9tLmdyb3VwcygpKSA8'
'IEdJVF9TQU46CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJnaXQgeycuJy5qb2luKF9ndl9tLmdyb3VwcygpKSBpZiBfZ3Zf'
'bSBlbHNlICcoa2hvbmcgZG9jIGR1b2MgcGhpZW4gYmFuKSd9IGN1IGhvbiAiCiAgICAgICAgICAgICAgICAgICAgICAgZiJ7'
'Jy4nLmpvaW4obWFwKHN0ciwgR0lUX1NBTikpfSAodW5nIHZpZW4gZ29pIGBnaXQgd29ya3RyZWUgbGlzdCAtLXBvcmNlbGFp'
'biAtemApOiBjYXAgbmhhdCBnaXQiKQogICAgICAgICMgYmFzaCBjdW5nIEhPSSBTQUkgQ0hPIG5odSBnaXQ6IDkgY2EgVFJP'
'TkcgcGhhbSB2aSAodDMyIHQ1MSB0NTkgdDYwIHQ2MiB0NjMgdDY2IHQ2OCB0MTUyKSBjaGF5IGJhc2ggYmFuZyBgX2Jhc2hf'
'cG9zaXgoKWAKICAgICAgICAjIGN1YSB1bmcgdmllbiDigJQgR2l0IEJhc2ggbyBkdW9uZyBDTyBESU5IIGBDOlxQcm9ncmFt'
'IEZpbGVzXEdpdFxiaW5cYmFzaC5leGVgICh2YSBgKHg4NilgLCBgdXNyXGJpbmApLCByb2kKICAgICAgICAjIGB3aGljaCgi'
'YmFzaCIpYCBOSFVORyBsb2FpIGtldCBxdWEgdHJvbmcgU3lzdGVtMzIgKFdTTCk7IGtob25nIHRoYXkgdGhpIHRyYSAiIi4g'
'TWF5IGNvIFdTTCBtYSBHaXQga2hvbmcgbyBQcm9ncmFtIEZpbGVzCiAgICAgICAgIyAoTWluR2l0IGRvIENISU5IIHBzMSB0'
'dSB0YWkg4oCUIE1pbkdpdCBLSE9ORyBjbyBiYXNoOyBzY29vcDsgY2FpIHBlci11c2VyKSBxdWEgY2hvdCBgd2hpY2hgIG8g'
'dHJlbiwgcm9pIGBfYmFzaF9wb3NpeCgpYAogICAgICAgICMgPT0gIiI6IHQzMiAiS0hPTkcgRE8gRFVPQyIgKyA4IGNhICJs'
'YSIgYHN1YnByb2Nlc3MucnVuKFsiIi4uLl0pYCwgY2hpIGxvIHJhIFNBVSBjYSBoYWkgbHVvdCBibyB0ZXN0LiBEbyB0cmVu'
'IDIwMjYtMTAtMDE6CiAgICAgICAgIyBoYW0gVEhBVCwgbmhhbmggb3MubmFtZT0nbnQnIChXU0wgKyBNaW5HaXQvc2Nvb3Av'
'cGVyLXVzZXIpID0+ICcnOyBibyB0ZXN0IHZvaSBnaWEgdHJpIGF5IDE1Ny8xNjY7IGUyZSAod2luMzIgZ2lhKSByYz0zCiAg'
'ICAgICAgIyBzYXUgMzQ3IHMsIGBUUlVPVCBNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyAgbGE6IFsndDUxJywgJ3Q1'
'OScsICd0NjAnLCAndDYyJywgJ3Q2MycsICd0NjYnLCAndDY4JywgJ3QxNTInXWAuIFBoZXAKICAgICAgICAjIGRvIDMwaiBj'
'aGF5IHRyZW4gTGludXgsIG5vaSBgX2Jhc2hfcG9zaXgoKWAgbHVvbiB0cmEgImJhc2giLCBuZW4ga2hvbmcgdGhlIHRoYXkg'
'ZHVvbmcgbmF5LgogICAgICAgICMgVmEgYGdpdGAgVFJPTkcgYmFzaCBheSBsYSBnaXQgVEhVIEJBOiBgR2l0XGJpblxiYXNo'
'LmV4ZWAgbGEgY29tcGF0LWJhc2ggY3VhIGdpdC13cmFwcGVyLCBgc2V0dXBfZW52aXJvbm1lbnQoKWAgZGF5CiAgICAgICAg'
'IyBgPGdvYyBHaXQ+XG1pbmd3NjRcYmluOzxnb2MgR2l0Plx1c3JcYmluYCBsZW4gREFVIFBBVEggKGdpdC1mb3Itd2luZG93'
'cy9NSU5HVy1wYWNrYWdlczogZ2l0LXdyYXBwZXIuYyArIGNvbXBhdC1iYXNoLnJjLAogICAgICAgICMga2hvbmcgY28gTUlO'
'SU1BTF9QQVRIKSDigJQgdHVjIGdpdCBESSBLRU0gYmFuIEdpdCBheSwgS0hPTkcgcGhhaSBnaXQgVFJBTiBkYSBob2kgbyB0'
'cmVuLiB0MTUyIGNoYXkgR0lUX0NPTkZJR19DT1VOVCAoZ2l0CiAgICAgICAgIyAyLjMxKSB0cm9uZyBiYXNoIGF5LiBEbyB0'
'cmVuIDIwMjYtMTAtMDEgKGJhc2ggYm9jIGRheSBnaXQgZGkga2VtIGxlbiBkYXUgUEFUSCwgZ2l0IFRSQU4gMi40Myk6IGdp'
'dCBkaSBrZW0gMi4zMC4yIFRIQVQgPT4KICAgICAgICAjIDE2NS8xNjYsIGUyZSByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCwg'
'YGxhOiBbJ3QxNTInXWAgY2hvIHVuZyB2aWVuIHNhY2g7IDIuMzEuMCBUSEFUID0+IDE2Ni8xNjYuIEhvaSBDSElOSCBoYW0g'
'YXkgdmEKICAgICAgICAjIENISU5IIGJhc2ggYXkgdHJvbmcgdGllbiB0cmluaCBjb24gY3VhIGNoYXkoKSAoY3VuZyBweXRo'
'b24sIGN1bmcgbW9pIHRydW9uZywgY3dkID0gZ29jKTsgdW5nIHZpZW4ga2hvbmcgY28gaGFtIHRoaSBraG9uZwogICAgICAg'
'ICMgaG9pIChnaXUgY2hvdCBDTyBNQVQpLgogICAgICAgICMgRG9jIGRvbmcgYGdpdCB2ZXJzaW9uYCBDVU9JIGN1YSBzdGRv'
'dXQsIEtIT05HIGRvYyBkb25nIERBVTogY2hheSgpIGdpdSBCQVNIX0VOViAoYm8gdGVzdCAxNjYvMTY2IHZvaSBubywgeGVt'
'IHRyZW4pLCBtYQogICAgICAgICMgYmFzaCBuYXAgQkFTSF9FTlYgVFJVT0MgbGVuaCAtYy4gRG8gdHJlbiAyMDI2LTEwLTAx'
'IChiYW4gMDFiKSwgQkFTSF9FTlYgYGVjaG9gIG1vdCBkb25nOiBtdWMgMCBLREQgImtob25nIGRvYyBkdW9jIHBoaWVuCiAg'
'ICAgICAgIyBiYW4iIHRyb25nIGtoaSBibyB0ZXN0IDE2Ni8xNjYuIEJhc2ggdHJlby9raG9uZyBjaGF5IGR1b2MgdGhpIGJh'
'dCBuZ29haSBsZSBUUk9ORyBjb246IGJhbiAwMWIgZGUgY29uIGNoZXQgcmM9MSBuZW4gbG9pCiAgICAgICAgIyBkbyBjaG8g'
'Imtob25nIGhvaSBkdW9jIGBfYmFzaF9wb3NpeCgpYCIgKGRvOiBiYXNoIHRyZW8gPT4gVGltZW91dEV4cGlyZWQgc2F1IDYw'
'IHMpIHRyb25nIGtoaSBoYW0gYXkgZGEgdHJhIHZlLgogICAgICAgIF9yY19icCwgX3JhX2JwID0gY2hheShbIi1jIiwgImlt'
'cG9ydCBzdWJwcm9jZXNzLCBzeXNcbnN5cy5wYXRoLmluc2VydCgwLCAnb3BzJylcbmltcG9ydCBsZWFzZV9wdWJsaXNoX3Rl'
'c3QgYXMgVFxuIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgImYgPSBnZXRhdHRyKFQsICdfYmFzaF9w'
'b3NpeCcsIE5vbmUpXG5iID0gJz8nIGlmIGYgaXMgTm9uZSBlbHNlIGYoKVxucHJpbnQoJ0JBU0hfUE9TSVg9JyArIGIpXG4i'
'CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiaWYgYiBhbmQgYiAhPSAnPyc6XG4gIHRyeTpcbiIKICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgICAgcCA9IHN1YnByb2Nlc3MucnVuKFtiLCAnLS1ub3Byb2Zp'
'bGUnLCAnLS1ub3JjJywgJy1jJywgJ2dpdCAtLXZlcnNpb24nXSwiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAiIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwgdGltZW91dD02MClcbiIKICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICIgICAgdiA9IFt4IGZvciB4IGluIHAuc3Rkb3V0LnNwbGl0bGluZXMoKSBpZiB4LnN0YXJ0'
'c3dpdGgoJ2dpdCB2ZXJzaW9uJyldIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiBvciBwLnN0ZG91'
'dC5zdHJpcCgpLnNwbGl0bGluZXMoKSBvciBbJyddXG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAi'
'ICAgIHByaW50KCdCQVNIX0dJVD0nICsgdlstMV0gKyAnIHJjPScgKyBzdHIocC5yZXR1cm5jb2RlKSlcbiIKICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZTpcbiAgICBwcmludCgnQkFTSF9H'
'SVQ9KCcgKyB0eXBlKGUpLl9fbmFtZV9fICsgJykgcmM9LTEnKVxuIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'IGdvYyBpZiBnb2MuaXNfZGlyKCkgZWxzZSBQYXRoLmN3ZCgpLCBwaHV0PTIpCiAgICAgICAgX2JwX20gPSByZS5zZWFyY2go'
'ciIoP20pXkJBU0hfUE9TSVg9KC4qKSQiLCBfcmFfYnApCiAgICAgICAgX2JwID0gX2JwX20uZ3JvdXAoMSkuc3RyaXAoKSBp'
'ZiAoX2JwX20gYW5kIG5vdCBfcmNfYnApIGVsc2UgTm9uZQogICAgICAgIF9iZ19tID0gcmUuc2VhcmNoKHIiKD9tKV5CQVNI'
'X0dJVD1naXQgdmVyc2lvblxzKyhcZCspXC4oXGQrKVwuKFxkKylbXlxuXSpcc3JjPTAkIiwgX3JhX2JwKQogICAgICAgIGdo'
'aSgiYmFzaF9ib190ZXN0IiwgX2JwKTsgZ2hpKCJnaXRfdHJvbmdfYmFzaF9ib190ZXN0IiwgX2JnX20uZ3JvdXAoMClbOTpd'
'IGlmIF9iZ19tIGVsc2UgTm9uZSkKICAgICAgICBpbm4oIiAgYmFzaCBibyB0ZXN0IDoiLCByZXByKF9icCkgaWYgX2JwIGlz'
'IG5vdCBOb25lIGVsc2UgZiIoa2hvbmcgaG9pIGR1b2MsIHJjPXtfcmNfYnB9KSIsCiAgICAgICAgICAgICJ8IGdpdCB0cm9u'
'ZyBiYXNoOiIsIF9iZ19tLmdyb3VwKDApWzk6XSBpZiBfYmdfbSBlbHNlICIoa2hvbmcgZG9jIGR1b2MpIikKICAgICAgICBp'
'ZiBfYnAgaXMgTm9uZToKICAgICAgICAgICAgbG9pLmFwcGVuZChmImtob25nIGhvaSBkdW9jIGBfYmFzaF9wb3NpeCgpYCBj'
'dWEgYm8gdGVzdCAocmM9e19yY19icH06IgogICAgICAgICAgICAgICAgICAgICAgIGYiIHsoX3JhX2JwLnN0cmlwKCkuc3Bs'
'aXRsaW5lcygpIG9yIFsnJ10pWy0xXVs6OTBdfSkiKQogICAgICAgIGVsaWYgbm90IF9icDoKICAgICAgICAgICAgbG9pLmFw'
'cGVuZChmImBfYmFzaF9wb3NpeCgpYCBjdWEgYm8gdGVzdCBLSE9ORyB0aGF5IGJhc2ggUE9TSVggKGB3aGljaGA6IHtfY2Nb'
'J2Jhc2gnXX07IFN5c3RlbTMyID0gV1NMIGJpIGxvYWkpOiIKICAgICAgICAgICAgICAgICAgICAgICAiIGNhaSBHaXQgZm9y'
'IFdpbmRvd3MgdmFvIEM6XFxQcm9ncmFtIEZpbGVzXFxHaXQsIGhvYWMgZGF0IHRodSBtdWMgR2l0XFxiaW4gbGVuIERBVSBQ'
'QVRIICh0cnVvYyBTeXN0ZW0zMikiKQogICAgICAgIGVsaWYgX2JwICE9ICI/IiBhbmQgbm90IF9iZ19tOgogICAgICAgICAg'
'ICBsb2kuYXBwZW5kKGYiYGdpdCAtLXZlcnNpb25gIFRST05HIGJhc2ggY3VhIGJvIHRlc3QgKHtfYnB9KSBraG9uZyBjaGF5'
'L2tob25nIGRvYyBkdW9jIHBoaWVuIGJhbjoiCiAgICAgICAgICAgICAgICAgICAgICAgZiIgeyhyZS5maW5kYWxsKHInKD9t'
'KV5CQVNIX0dJVD0oLiopJCcsIF9yYV9icCkgb3IgWycoa2hvbmcgY28gZG9uZyBCQVNIX0dJVCknXSlbLTFdWzo5MF19IikK'
'ICAgICAgICBlbGlmIF9icCAhPSAiPyIgYW5kIHR1cGxlKGludCh4KSBmb3IgeCBpbiBfYmdfbS5ncm91cHMoKSkgPCBHSVRf'
'U0FOX0JBU0g6CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJnaXQgeycuJy5qb2luKF9iZ19tLmdyb3VwcygpKX0gVFJPTkcg'
'YmFzaCBjdWEgYm8gdGVzdCAoe19icH0pIGN1IGhvbiB7Jy4nLmpvaW4obWFwKHN0ciwgR0lUX1NBTl9CQVNIKSl9IgogICAg'
'ICAgICAgICAgICAgICAgICAgICIgKHQxNTIgZHVuZyBHSVRfQ09ORklHX0NPVU5UKTogY2FwIG5oYXQgYmFuIEdpdCBjaHVh'
'IGJhc2ggYXkiKQoKcmMsIGhlYWQsIF8gPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIkhFQUQiKQppZiByYzogbG9pLmFwcGVu'
'ZCgia2hvbmcgZG9jIGR1b2MgSEVBRCIpCmdoaSgiaGVhZCIsIGhlYWQpCnJjX2EsIF8sIF8gPSBnaXQoZ29jLCAibWVyZ2Ut'
'YmFzZSIsICItLWlzLWFuY2VzdG9yIiwgU0hBX0cxLCBoZWFkIG9yICJIRUFEIikKbGFfaGF1X2R1ZSA9IChyY19hID09IDAp'
'CmlmIGhlYWQgPT0gU0hBX0cxOgogICAgdGhlX2hlID0gImcxIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBEQVkg'
'TEEgZzEuIENIVUEgY28gYmFuIHZhIGcyOyBrZXQgcXVhIGR1b2kgbGEgTkVOIERPLiIpCmVsaWYgbGFfaGF1X2R1ZToKICAg'
'IHRoZV9oZSA9ICJnMiI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gaGF1IGR1ZSBjdWEgZzEgKHtTSEFfRzFbOjhd'
'fSk7IHVuZyB2aWVuIGcyIGhheSBraG9uZzogTjcnIChtdWMgMSkgZGluaCBkYW5oLiIpCmVsc2U6CiAgICB0aGVfaGUgPSAi'
'PyI7IGxvaS5hcHBlbmQoZiJIRUFEPXtoZWFkWzo4XX0gS0hPTkcgcGhhaSBnMSB2YSBLSE9ORyBwaGFpIGhhdSBkdWUgY3Vh'
'IHtTSEFfRzFbOjhdfSDigJQgcmViYXNlPyBuaGFtIG5oYW5oPyIpCmdoaSgidGhlX2hlIiwgdGhlX2hlKQpyY19yLCByZWZz'
'LCBfID0gZ2l0KGdvYywgImZvci1lYWNoLXJlZiIsICItLXBvaW50cy1hdCIsIGhlYWQgb3IgIkhFQUQiLAogICAgICAgICAg'
'ICAgICAgICAgICItLWZvcm1hdD0lKHJlZm5hbWU6c2hvcnQpIikKZHNyID0gW3ggZm9yIHggaW4gcmVmcy5zcGxpdGxpbmVz'
'KCkgaWYgeC5zdHJpcCgpIGFuZCB4LnN0cmlwKCkgIT0gImRvLXRhbSJdCmdoaSgicmVmX3Ryb190b2lfaGVhZCIsIGRzcikK'
'aW5uKGYiICByZWYgdHJvIHRvaSBIRUFEOiB7JywgJy5qb2luKGRzcikgaWYgZHNyIGVsc2UgJyhraG9uZyByZWYgbmFvIC0g'
'SEVBRCByb2kgdHUgZG8pJ30iKQoKaWYgbG9pOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBuZW4gZG8gc2Fp'
'LCBLSE9ORyBpbiBrZXQgbHVhbiBuYW8uIikKICAgIGZvciB4IGluIGxvaTogaW5uKCIgIC0iLCB4KQogICAgc3lzLmV4aXQo'
'MykKCiMgLS0tLS0tLS0tLS0tLS0tLSAxLiBraWNoIHRodW9jIChONycgY3VhIHNwZWMgcjMpIC0tLS0tLS0tLS0tLS0tLS0K'
'aW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIxLiBLSUNIIFRIVU9DIOKAlCB0cmFuIHNwZWMgcjM6IDw9IDIgdGVwIHZh'
'IDw9IDQwMCBkb25nIHRoZW0iKQojIFZFIE5FTiBQSEFJIFRVT0kg4oCUIHZhIHBoYWkgQ0hVTkcgTUlOSCBkdW9jIGxhIHR1'
'b2ksIGtob25nIHBoYWkgZ2lhIGRpbmguCiMgQmFpIGhvYyB0cmEgZ2lhIDE5LTA5LTIwMjY6IGNsb25lIHRhaSBkdW5nIGNo'
'aSBmZXRjaCBuaGFuaCBiYW4gdmEsIGBvcmlnaW4vbWFzdGVyYAojIGR1bmcgeWVuIHR1IDE0LTA5IChjMTZiZDMyLCBzYXUg'
'OTcgY29tbWl0KS4gbWVyZ2UtYmFzZSByb2kgdmUgZHVuZyBkaW5oIG1hc3RlciBjdSwKIyBuZW4gZGlmZiBOVU9UIGNhIDk3'
'IGNvbW1pdCBtYXN0ZXI6IGRvIHJhIDQ2IHRlcCAvICs3MTE4IHRoYXkgdmkgMiB0ZXAgLyArMzk3IOKAlAojIENVTkcgTU9U'
'IENPTU1JVCAwZWE5NWRlLiBNb3QgdGlldSBjaGkgREVMVEEgbWEgdmUgbmVuIGtob25nIHR1b2kgdGhpIGtob25nIHNhaQoj'
'IGxlY2ggbW90IGNodXQsIG5vIHNhaSBjYSBtb3QgYmFjIGRvIGxvbi4KIyBDaG8gbmVuOiBuZW4ga2hvbmcgY2h1bmcgbWlu'
'aCBkdW9jIGxhIHR1b2kgPT4gS0hPTkcgRE8gRFVPQyAocmM9MyksIEtIT05HIHBoYWkgVFJVT1QuCiMgVFJVT1QgbGEgbW90'
'IFBIQU4gUVVZRVQgdmUgYmFuIHZhOyBwaGFuIHF1eWV0IGNoaSBkdW9jIHBoZXAgcGhhdCByYSBraGkgZGEgZG8gZHVvYy4K'
'ZXIgPSAiIgpyY191LCB1cmxfdGhvLCBfID0gZ2l0KGdvYywgInJlbW90ZSIsICJnZXQtdXJsIiwgIm9yaWdpbiIpCnVybF9v'
'LCB1cmxfaW4gPSBfdXJsX3NhY2godXJsX3RobyksIF91cmxfaW4odXJsX3RobykKZ2hpKCJvcmlnaW5fdXJsIiwgdXJsX2lu'
'KTsgaW5uKGYiICBvcmlnaW4gICAgICAgOiB7dXJsX2luIG9yICcoa2hvbmcgZG9jIGR1b2MpJ30iKQp1cmxfb2sgPSAobm90'
'IHJjX3UpIGFuZCB1cmxfby5yc3RyaXAoIi8iKSBpbiBVUkxfS0hPX0hPUF9MRQpyY19sciwgb3V0X2xyLCBlcl9sciA9IGdp'
'dChnb2MsICJscy1yZW1vdGUiLCAib3JpZ2luIiwgInJlZnMvaGVhZHMvbWFzdGVyIikgaWYgdXJsX29rIGVsc2UgKDEsICIi'
'LCAiIikKZXJfbHIgPSBfYW5fdXNlcmluZm8oZXJfbHIpCnJjX2xtLCBsbSwgZXJfbG0gICAgID0gZ2l0KGdvYywgInJldi1w'
'YXJzZSIsICJvcmlnaW4vbWFzdGVyIikKcm0gPSBvdXRfbHIuc3BsaXQoKVswXSBpZiAobm90IHJjX2xyIGFuZCBvdXRfbHIu'
'c3RyaXAoKSkgZWxzZSAiIgppZiBub3QgdXJsX29rOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJvcmlnaW49'
'e3VybF9pbiFyfSBLSE9ORyBwaGFpIGtobyB0aGF0IOKAlCAndHVvaScgc28gdm9pIG5vIGtob25nIGNodW5nIG1pbmggZHVv'
'YyBnaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIG5vdCBybToKICAgIGtldCgiTjcnIGtp'
'Y2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJraG9uZyBob2kgZHVvYyBtYXN0ZXIgdHJlbiByZW1vdGUgKGxzLXJlbW90ZSBy'
'Yz17cmNfbHJ9KToge2VyX2xyWzo2MF19ICIKICAgICAgICBmIuKAlCBraG9uZyBjaHVuZyBtaW5oIGR1b2MgdmUgbmVuIGNv'
'biB0dW9pIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgcmNfbG0gb3Igbm90IGxtOgogICAg'
'a2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyBkb2MgZHVvYyBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25lOiB7'
'ZXJfbG1bOjYwXX0iKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBsbSAhPSBybToKICAgICMg'
'RGVtIHhlbSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRlbSBkdW9jIOKAlCBjb24gc28gbmF5IG5vaSBybyBtdWMgZG8gc2FpIGxl'
'Y2guCiAgICByY19jLCBzYXUsIF8gPSBnaXQoZ29jLCAicmV2LWxpc3QiLCAiLS1jb3VudCIsIGYie2xtfS4ue3JtfSIpCiAg'
'ICB4YSA9IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1pdCIgaWYgKG5vdCByY19jIGFuZCBzYXUuc3RyaXAoKS5pc2RpZ2l0KCkp'
'IGVsc2UgIiIKICAgIGlubihmIiAgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZSA6IHtsbVs6MTJdfSIpCiAgICBpbm4oZiIg'
'IG1hc3RlciB0cmVuIHJlbW90ZSAgICAgICAgOiB7cm1bOjEyXX17eGF9IikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0p'
'OyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJ2ZSBu'
'ZW4gQ1U6IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19ICE9IHJlbW90ZT17cm1bOjEyXX17eGF9ICIKICAgICAgICBmIuKAlCBj'
'aGF5IGBnaXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2luIG1hc3RlcmAgcm9pIGRvIGxhaSIpCiAgICByY19tYiwgbWIsIG5zLCBy'
'YyA9IDEsICIiLCAiIiwgMQplbHNlOgogICAgaW5uKGYiICB2ZSBuZW4gVFVPSTogb3JpZ2luL21hc3RlciA9IHtsbVs6MTJd'
'fSA9PSBtYXN0ZXIgdHJlbiByZW1vdGUiKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90'
'ZSIsIHJtKQogICAgcmNfbWIsIG1iLCBlcl9tYiA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIm9yaWdpbi9tYXN0ZXIiLCBo'
'ZWFkKQppZiByY19tYiBvciBub3QgbWI6CiAgICBpZiBtYiA9PSAiIiBhbmQgcm0gYW5kIGxtID09IHJtOgogICAgICAgIGtl'
'dCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9jIG1lcmdlLWJhc2Ugdm9pIG9yaWdpbi9tYXN0ZXI6'
'IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgogICAgZ2hpKCJtZXJnZV9iYXNlIiwgbWIpCiAgICBp'
'bm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7bWJbOjEyXX0iKQogICAgaWYgbWIgIT0gU0hBX0JB'
'U0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2UgbWEgc3BlYyByMyBraGFpICh7U0hBX0JBU0VfU1BF'
'Q1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQogICAgICAgIGlubigiICAgICAgICAgRG8gc28gYmFz'
'ZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcgdmFvLiBEdW5nIG1lcmdlLWJhc2UgbW9pIGxhIHZpZWMgY3VhIGV4ZWN1'
'dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJkaWZmLXRyZWUiLCAiLXIiLCAiLU0iLCAiLS1kaWZm'
'LWFsZ29yaXRobT1teWVycyIsICItLW51bXN0YXQiLCBTSEFfQkFTRV9TUEVDLCBoZWFkKQogICAgICAgIGlmIG5vdCByY194'
'OgogICAgICAgICAgICBoID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnNfeC5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgp'
'XQogICAgICAgICAgICBhID0gc3VtKGludCh4WzBdKSBmb3IgeCBpbiBoIGlmIHhbMF0uaXNkaWdpdCgpKQogICAgICAgICAg'
'ICBnaGkoIm51bXN0YXRfdGhlb19iYXNlX3NwZWMiLCB7InRlcCI6IGxlbihoKSwgInRoZW0iOiBhfSkKICAgICAgICAgICAg'
'aW5uKGYiICAgICAgICAgKGRvaSBjaGlldTogc28gYmFzZSBzcGVjID0ge2xlbihoKX0gdGVwIC8gK3thfSDigJQgY29uIHNv'
'IGF5IEtIT05HIGR1bmcgZGUgY2hhbSkiKQogICAgIyBQTFVNQklORywga2hvbmcgUE9SQ0VMQUlOOiBgZ2l0IGRpZmZgIGRv'
'YyBjYXUgaGluaCBVSSBDVUEgTkdVT0kgRE8gKGRpZmYuYWxnb3JpdGhtLCBkaWZmLnJlbmFtZXMsIGRpZmYub3JkZXJGaWxl'
'LAogICAgIyBjb2xvci5kaWZmKSwgdmEgZ2lhIHRyaSBIT1AgTEUgZG9pIGx1b24gU08gZG9uZyBtYSB2YW4gcmEgY2h1IHNv'
'IOKAlCBkbyB0cmVuIDIwMjYtMDktMzBpOiB1bmcgdmllbiB0b25nIGhvcCAobXllcnMgKzQwMSkgPT4KICAgICMgYmFuIDMw'
'aSBEQVQgMiB0ZXAgLyArNDAwIGR1b2kgYGRpZmYuYWxnb3JpdGhtID0gaGlzdG9ncmFtYCBob2FjIGBwYXRpZW5jZWAsIFRS'
'VU9UICs0MDEga2hpIG1hYyBkaW5oOyAxMC83NSBjb21taXQgY2hhbQogICAgIyB3cml0ZSBzZXQgY28gc28gZG9uZyBkb2kg'
'dGhlbyB0aHVhdCB0b2FuLiBgZGlmZi10cmVlIC1yIC1NYCA9IG1hYyBkaW5oIGN1YSBgZ2l0IGRpZmZgIChyZW5hbWVzIGJh'
'dCkgdmEgS0hPTkcgZG9jIGNhYyBraG9hCiAgICAjIGF5LiBUaHVhdCB0b2FuIHBoYWkgVFVPTkcgTUlOSDogZGlmZi48ZHJp'
'dmVyPi5hbGdvcml0aG0gKHF1YSBjb3JlLmF0dHJpYnV0ZXNGaWxlIGN1YSBuZ3VvaSBkbykgVkFOIGxvdCB2YW8gcGx1bWJp'
'bmcg4oCUCiAgICAjIGRvIHRyZW4gMjAyNi0wOS0zMGksIGAqLnB5IGRpZmY9YWxnYCArIGRpZmYuYWxnLmFsZ29yaXRobT1o'
'aXN0b2dyYW06IGRpZmYtdHJlZSArNDAxIGNobyB1bmcgdmllbiBteWVycyArNDAwOyBjbyB0dW9uZyBtaW5oCiAgICAjIHRo'
'YW5nIGtob2EgYXkuIGF0dHJpYnV0ZXMgYC1kaWZmYC9jb3JlLmJpZ0ZpbGVUaHJlc2hvbGQgdmFuIGFwID0+IGAtYCA9PiBL'
'SE9ORyBETyBEVU9DIChjaG90IGR1b2kpLgogICAgcmMsIG5zLCBlciA9IGdpdChnb2MsICJkaWZmLXRyZWUiLCAiLXIiLCAi'
'LU0iLCAiLS1kaWZmLWFsZ29yaXRobT1teWVycyIsICItLW51bXN0YXQiLCBtYiwgaGVhZCkKaWYgcmM6CiAgICBwYXNzCmVs'
'c2U6CiAgICBoYW5nID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnMuc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAg'
'IHRoZW0gPSBzdW0oaW50KGhbMF0pIGZvciBoIGluIGhhbmcgaWYgaFswXS5pc2RpZ2l0KCkpCiAgICB4b2EgID0gc3VtKGlu'
'dChoWzFdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMV0uaXNkaWdpdCgpKQogICAgZ2hpKCJzb190ZXAiLCBsZW4oaGFuZykpOyBn'
'aGkoImRvbmdfdGhlbSIsIHRoZW0pOyBnaGkoImRvbmdfeG9hIiwgeG9hKQogICAgZm9yIGggaW4gaGFuZzogaW5uKGYiICAg'
'IHtoWzJdOjM0fSAre2hbMF06PDV9IC17aFsxXX0iKQogICAgaW5uKGYiICAgIFRPTkc6IHtsZW4oaGFuZyl9IHRlcCwgK3t0'
'aGVtfSwgLXt4b2F9ICAgKHRyYW46IHtUUkFOX1RFUH0gdGVwIC8ge1RSQU5fRE9OR30gZG9uZyB0aGVtKSIpCiAgICBjaGFt'
'ID0gc29ydGVkKHtoWzJdIGZvciBoIGluIGhhbmd9ICYgV1JJVEVfU0VUX0cyKTsgZ2hpKCJjaGFtX3dyaXRlX3NldCIsIGNo'
'YW0pCiAgICBkZWYgX2NhX21vaV9jbyhyZXYpOgogICAgICAgICMgY2F0LWZpbGUsIGtob25nIGBzaG93YDogYGdpdCBzaG93'
'YCBjaGV0IHZvaSBjYXUgaGluaCBVSSBnbyBzYWkgKGRvIHRyZW4gMjAyNi0wOS0zMGk6IGxvZy5kYXRlIGdvIHNhaSA9PiBi'
'YW4gMzBpIGdvaQogICAgICAgICMgMGVhOTVkZSBsYSAia2hvbmcgcGhhaSB1bmcgdmllbiAuLi4gTm9uZSDigJQgZGEgbGFu'
'ZD8gbmhhbSBuaGFuaD8iKS4KICAgICAgICByXywgbmRfLCBfID0gZ2l0KGdvYywgImNhdC1maWxlIiwgIi1wIiwgZiJ7cmV2'
'fTpvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICByZXR1cm4gTm9uZSBpZiByXyBlbHNlIHt0IGZvciB0IGlu'
'IENBX01PSV9HMiBpZiByZS5zZWFyY2gociIoP20pXmRlZiAiICsgdCArIHIiW2Etel0/XyIsIG5kXyl9CiAgICBvX21iLCBv'
'X2ggPSBfY2FfbW9pX2NvKG1iKSwgX2NhX21vaV9jbyhoZWFkKQogICAgbWFuZyA9IHNvcnRlZChvX2ggLSBvX21iLCBrZXk9'
'c29fY2EpIGlmIChvX21iIGlzIG5vdCBOb25lIGFuZCBvX2ggaXMgbm90IE5vbmUpIGVsc2UgTm9uZQogICAgZ2hpKCJjYV9t'
'b2lfZzJfbWFuZ192YW8iLCBtYW5nKQogICAgaWYgbm90IG1hbmc6CiAgICAgICAgIyBEbyBST05HIChkYSBsYW5kLCBjaGlu'
'aCBtYXN0ZXIpLCBuaGFtIG5oYW5oLCBoYXkgbmhhbmggY3VhIHBhY2tldCBLSEFDIGNoYW0gY3VuZyB0ZXA6CiAgICAgICAg'
'IyBraG9uZyBtYW5nIGNhIG1vaSBuYW8gY3VhIGcyIHRoaSBraG9uZyBwaGFpIHVuZyB2aWVuLiBEb2Mga2hvbmcgZHVvYyAo'
'Tm9uZSkgY3VuZyB2YXkuCiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJkb2kgdHVvbmcga2hvbmcgcGhh'
'aSB1bmcgdmllbjoge2xlbihoYW5nKX0gdGVwLCBjaGFtIHtjaGFtfSwgY2EgbW9pICIKICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICBmImcyIG1hbmcgdmFvIHttYW5nIXJ9IOKAlCBkYSBsYW5kPyBuaGFtIG5oYW5oPyBwYWNrZXQga2hh'
'Yz8iKQogICAgZWxzZToKICAgICAgICAjIG51bXN0YXQgaW4gYC1gIChraG9uZyBjbyBzbyBkb25nKSBjaG8gdGVwIGJpbmFy'
'eS8tZGlmZiB0aGVvIGF0dHJpYnV0ZXMg4oCUIGtlIGNhIGF0dHJpYnV0ZXMgQ1VBIE5HVU9JIERPIChkbyB0cmVuCiAgICAg'
'ICAgIyAyMDI2LTA5LTMwZzogY29yZS5hdHRyaWJ1dGVzRmlsZSBgKi5weSAtZGlmZmAgPT4gIjIgdGVwIC8gKzAiIERBVCBj'
'aG8gMGVhOTVkZSwgdGhhdCArMzk3KS4gYC1gIGxhIEtIT05HIERPIERVT0MsCiAgICAgICAgIyBraG9uZyBwaGFpIDA7IFRS'
'VU9UIHRoZW8gc28gdGVwIC8gc28gZG9uZyBEQSBkZW0gZHVvYyB2YW4gZ2l1IChxdWFuIHNhdCB0cnVjIHRpZXApLgogICAg'
'ICAgIGtob25nX3NvID0gW2hbMl0gZm9yIGggaW4gaGFuZyBpZiBub3QgKGhbMF0uaXNkaWdpdCgpIGFuZCBoWzFdLmlzZGln'
'aXQoKSldOyBnaGkoInRlcF9raG9uZ19zb19kb25nIiwga2hvbmdfc28pCiAgICAgICAgdnVvdCA9IGxlbihoYW5nKSA+IFRS'
'QU5fVEVQIG9yIHRoZW0gPiBUUkFOX0RPTkcKICAgICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgVFJVT1QgaWYgdnVvdCBl'
'bHNlIChLREQgaWYga2hvbmdfc28gZWxzZSBEQVQpLAogICAgICAgICAgICBmIntsZW4oaGFuZyl9IHRlcCAvICt7dGhlbX0i'
'ICsgKGYiIOKAlCBudW1zdGF0IEtIT05HIGNvIHNvIGRvbmcgY2hvIHtraG9uZ19zb30iIGlmIGtob25nX3NvIGVsc2UgIiIp'
'KQoKIyBDb25nIGtpY2ggdGh1b2MgUEhBSSBkZSBsYWkgTU9UIGtldCBxdWEuIExlbmggbnVtc3RhdCBob25nIHRoaSBuaGFu'
'aCBgaWYgcmM6IHBhc3NgIGtob25nIGdoaSBnaSwgdmEgdmFuZyBtYXQgbyBkYXkKIyB0aGFuaCBEQVQgbyBibyBnb3A6IGNh'
'dSBoaW5oIGRpZmYgQ1VBIE5HVU9JIERPIGhvbmcgKGRpZmYub3JkZXJGaWxlIHRybyB0ZXAga2hvbmcgY28sIGRpZmYuYWxn'
'b3JpdGhtIGdvIHNhaSA9PiByYz0xMjgpIGNobwojIC0tY2hpLWtpY2gtdGh1b2MgcmM9MCB2b2kgMCBjaG90LCBsdW90IGRh'
'eSBkdSAiREFUIDExIiByYz0wIChkbyB0cmVuIDIwMjYtMDktMzBoLCAwZWE5NWRlKS4gVmFuZyBtYXQgbGEgS0hPTkcgRE8g'
'RFVPQy4KIyBUdSAzMGogbnVtc3RhdCBsYSBkaWZmLXRyZWUgKGtob25nIGRvYyBoYWkga2hvYSBheSk7IGR1b25nIGNvbiBs'
'YWkgZG8gZHVvYzogZGlmZi5yZW5hbWVMaW1pdCBnbyBzYWkgPT4gcmM9MTI4LgppZiBub3QgYW55KGNbMF0gPT0gIk43JyBr'
'aWNoIHRodW9jIiBmb3IgYyBpbiBjaG90KToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYiY29uZyBLSE9ORyBy'
'YSBrZXQgcXVhIChnaXQgZGlmZi10cmVlIC0tbnVtc3RhdCByYz17cmN9KToge19hbl91c2VyaW5mbyhlcilbOjcwXX0iKQoK'
'IyBEaW5oIGRhbmggVEhBVCBuYW0gbyBONycgKGNhIG1vaSBnMiBtYW5nIHZhbyksIEtIT05HIG8gImhhdSBkdWUgZzEiOiBn'
'MSBkYSBsYW5kIG5lbiBtb2kgbmhhbmggZGV1CiMgbGEgaGF1IGR1ZS4gRG9uZyBkYXUga2hvaSBkYW4gcGhhaSB0dSBraGFp'
'IHRoZW8ga2V0IHF1YSBheSAoZG8gZHVvYzogbWFzdGVyIDQ0NjIwZTggbW8ga2hvaSBiYW5nCiMgIlRIRSBIRSBETyBEVU9D'
'OiBnMiIsIEpTT04gInRoZV9oZSI6ICJnMiIsIHRyb25nIGtoaSBONycgZGEga2V0IGx1YW4gImtob25nIHBoYWkgdW5nIHZp'
'ZW4iKS4KIyBOaGFuIGNoaSBkdW9jIG5vaSBEVU5HIGNhaSBkbyBkdW9jOiBgW11gIGtob25nIHRhY2ggImRhIGxhbmQiIGto'
'b2kgIm5oYW0gbmhhbmgiLyJwYWNrZXQga2hhYyIgKGRvCiMgZHVvYyB0cmVuIDIwMjYtMDktMzBiOiB1bmcgdmllbiAyYTY3'
'OTY4IERBIExBTkQgYmkgZ29pICJLSE9ORyBwaGFpIHVuZyB2aWVuIGcyIikuCmlmIHRoZV9oZSA9PSAiZzIiIGFuZCBub3Qg'
'c28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKToKICAgIHRoZV9oZSA9ICgiS0hPTkcgbWFuZyBjYSBtb2kgZzIgbmFvIChk'
'YSBsYW5kPyBuaGFtIG5oYW5oPyBwYWNrZXQga2hhYz8pIiBpZiBzby5nZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpID09IFtd'
'CiAgICAgICAgICAgICAgZWxzZSAiZzI/IChDSFVBIGRpbmggZGFuaCBkdW9jIGRvaSB0dW9uZykiKQogICAgZ2hpKCJ0aGVf'
'aGUiLCB0aGVfaGUpCgojIENvbmcgbmhhbmg6IGRvIFJJRU5HIGtpY2ggdGh1b2MgKHZhaSBnaWF5KSByb2kgZHVuZy4gRHVu'
'ZyBraGkgY2FuIHhhYyBtaW5oIGxhaQojIHZlIG5lbiBtYSBraG9uZyBtdW9uIHRyYSAyMC00NSBwaHV0IGNobyBjYSBibyB0'
'ZXN0LgppZiAiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Y6CiAgICBpbm4oIiIpOyBpbm4oIj0iICogNzgpCiAgICBp'
'bm4oIi0tY2hpLWtpY2gtdGh1b2M6IENISSBkbyBjb25nIGtpY2ggdGh1b2MuIERheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5n'
'aGllbSB0aHUuIikKICAgIGlubigiLSIgKiA3OCkKICAgIGZvciBfdCwgX3R0LCBfY3QgaW4gY2hvdDogaW5uKGYiICB7X3R0'
'OjE0fSB7X3R9IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICBfayA9IHN1bSgxIGZvciBfLCB0LCBfIGlu'
'IGNob3QgaWYgdCA9PSBLREQpCiAgICBfciA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKICAg'
'IHN5cy5leGl0KDMgaWYgX2sgZWxzZSAoMSBpZiBfciBlbHNlIDApKQoKQ0hJX1BST0JFID0gIi0tY2hpLXByb2JlIiBpbiBz'
'eXMuYXJndiAgICAjIGJvIHF1YSBibyB0ZXN0ICsgTjc7IGdpdSAwLCAxLCAzCiMgLS0tLS0tLS0tLS0tLS0tLSAyLiBibyB0'
'ZXN0IGRheSBkdSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgp'
'OyBpbm4oIjIuIEJPIFRFU1QgREFZIERVICgxMC00MCBwaHV0KSIpCiAgICByY19uLCBvdXRfbiA9IGNoYXkoWyJvcHMvbGVh'
'c2VfcHVibGlzaF90ZXN0LnB5Il0sIGdvYykKICAgIGdoaSgicmNfc3VpdGUiLCByY19uKQogICAgbSA9IFJYX1RPTkcuc2Vh'
'cmNoKG91dF9uKQogICAgaW5uKCIgIHJjID0iLCByY19uLCAifCIsIG0uZ3JvdXAoMCkgaWYgbSBlbHNlICIoS0hPTkcgZG9j'
'IGR1b2MgZG9uZyB0b25nIGtldCkiKQogICAgaWYgbToKICAgICAgICBnaGkoImRhdCIsIGludChtLmdyb3VwKDEpKSk7IGdo'
'aSgidHJlbiIsIGludChtLmdyb3VwKDIpKSk7IGdoaSgiYm9fcXVhX3NvIiwgaW50KG0uZ3JvdXAoNCkpKQogICAgZG9faGV0'
'LCBnYywgdGluID0gZG9jX2RvKG91dF9uKQogICAgZ2hpKCJzb19jYV9kbyIsIGxlbihkb19oZXQpKTsgZ2hpKCJsaWV0X2tl'
'X2RheV9kdSIsIHRpbikKICAgIGZvciBnIGluIGdjOiBpbm4oIiAgICoiLCBnKQogICAgaW5uKCIiKTsgaW5uKGYiICA9PT0g'
'e2xlbihkb19oZXQpfSBDQSBETyA9PT0iKQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAg'
'ICBpbm4oZiIgICB7dC5zcGxpdCgnXycpWzBdOjd9IHt0fSIpOyBpbm4oZiIgICAgICAgICAgIHtkb19oZXRbdF1bOjE1MF19'
'IikKICAgIGdoaSgiZG9fbHlfZG8iLCB7dDogZG9faGV0W3RdWzozMDBdIGZvciB0IGluIGRvX2hldH0pCiAgICAjIC0tLS0g'
'Q0hPVDogbW9pIGNhIERPIHBoYWkgR0lBSSBUSElDSCBEVU9DIC0tLS0KICAgICMgVGhpZXUgY2hvdCBuYXksIGJvIGRvIGlu'
'IGRhbmggc2FjaCBkbyByb2kgdmFuIHRob2F0IHJjPTAuIERvIGR1bmcgbGEgbG9pIGRhIHhheSByYToKICAgICMgbHVvdCBX'
'aW5kb3dzIDE5LTA5IGNvIHQxNzEgRE8gbWEgYm8gZG8gYmFvICJEQVQgMTAgfCBUUlVPVCAwIiB2YSByYz0wLgogICAgZGVm'
'IF9raG9hKHQpOiByZXR1cm4gdC5zcGxpdCgiXyIpWzBdCiAgICBkb19wYWNrZXQsIGRvX2xhLCBkb190aGlldV9jb25nX2N1'
'ID0gW10sIFtdLCBbXQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAgICBrLCBseSA9IF9r'
'aG9hKHQpLCBkb19oZXRbdF0KICAgICAgICBpZiBrIGluIENBX1BBQ0tFVDogICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICBkb19wYWNrZXQuYXBwZW5kKHQpCiAgICAgICAgZWxpZiAiS0jDlE5HIMSQTyDEkMav4buiQyIgaW4gbHkgb3IgInRoaeG6'
'v3UgYCIgaW4gbHk6ICBkb190aGlldV9jb25nX2N1LmFwcGVuZCh0KQogICAgICAgIGVsaWYgayBpbiBOR09BSV9QSEFNX1ZJ'
'OiAgICAgICAgICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICBlbHNlOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICBkb19sYS5hcHBlbmQodCkKICAgIGdoaSgiZG9fcGFja2V0IiwgZG9fcGFja2V0KTsgZ2hpKCJkb19s'
'YSIsIGRvX2xhKTsgZ2hpKCJkb190aGlldV9jb25nX2N1IiwgZG9fdGhpZXVfY29uZ19jdSkKICAgIGlubigiIikKICAgIGlu'
'bihmIiAgY2EgRE8gdGh1b2MgQ0hJTkggcGFja2V0IG5heSA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XSBvciAn'
'a2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERPIG5nb2FpIHBoYW0gdmkgKHIzIGtoYWkpOiB7W19raG9hKHgpIGZvciB4'
'IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSkgaWYgX2tob2EoeCkgaW4gTkdPQUlfUEhBTV9WSV19IikKICAgIGlubihm'
'IiAgY2EgRE8gdmkgVEhJRVUgQ09ORyBDVSAgICAgICA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV0g'
'b3IgJ2tob25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBMQSAoa2hvbmcgZ2lhaSB0aGljaCBkdW9jKToge1tfa2hvYSh4'
'KSBmb3IgeCBpbiBkb19sYV0gb3IgJ2tob25nIGNvJ30iKQogICAgIyAtLS0tIENIT1Q6IHBoZXAgZG8gcGhhaSBUUk9OIHRy'
'dW9jIGtoaSBtb3QgY2h1IERBVCBuYW8gZHVvYyBwaGF0IC0tLS0KICAgICMgQmFuIHRydW9jIGNoaSBJTiBgdGluYC9gcmNf'
'c3VpdGVgOiBibyB0ZXN0IGNoZXQgZ2l1YSB0MTcxIChyYz0xMzQsIGtob25nIGRvbmcgdG9uZykKICAgICMgdmFuIHJhICJE'
'QVQgMTIgfCBUUlVPVCAwIiByYz0wOyBjYSBQQUNLRVQgdmFuZyBtYXQgaGF5IGJpIEJPIFFVQSBjdW5nIGR1b2MgY2hhbSBu'
'aHUKICAgICMgImtob25nIGRvIi4gVmFuZyBtYXQga2hvbmcgcGhhaSAia2hvbmcgZG8iIOKAlCBsYSBLSE9ORyBETyBEVU9D'
'LgogICAgdmFuZyA9IFt0IGZvciB0IGluIHNvcnRlZChDQV9QQUNLRVQsIGtleT1zb19jYSkgaWYgbWF1X2NhKG91dF9uLCB0'
'KSBub3QgaW4gKCJRVUEiLCAiRE8iKV0KICAgIGx5X2tkZCA9IFtdCiAgICBpZiBub3QgdGluOiBseV9rZGQuYXBwZW5kKCJk'
'YW5oIHNhY2ggZG8gS0hPTkcgZGF5IGR1IikKICAgIGlmIHJjX24gbm90IGluICgwLCAxKSBvciAocmNfbiA9PSAxKSAhPSBi'
'b29sKGRvX2hldCk6CiAgICAgICAgbHlfa2RkLmFwcGVuZChmInJjIGJvIHRlc3Q9e3JjX259IGtob25nIGtob3Age2xlbihk'
'b19oZXQpfSBjYSBETyBkb2MgZHVvYyIpCiAgICBpZiB2YW5nOiBseV9rZGQuYXBwZW5kKGYiY2EgUEFDS0VUIHZhbmcvYm8g'
'cXVhOiB7dmFuZ30iKQogICAgZ2hpKCJjYV9wYWNrZXRfdmFuZyIsIHZhbmcpOyBnaGkoImx5X2RvX2NodWFfdHJvbiIsIGx5'
'X2tkZCkKICAgIGlmIGx5X2tkZDoga2V0KCJCbyB0ZXN0IGNoYXkgVFJPTiB2YSBkb2MgRFUiLCBLREQsICI7ICIuam9pbihs'
'eV9rZGQpKQogICAgY2h1YV90cm9uID0gS0REIGlmIGx5X2tkZCBlbHNlIERBVAogICAga2V0KCJLaG9uZyBjYSBuYW8gY3Vh'
'IFBBQ0tFVCBiaSBETyIsIGNodWFfdHJvbiBpZiBub3QgZG9fcGFja2V0IGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90'
'IGRvX3BhY2tldCBlbHNlIGYiRE86IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XX0g4oCUIGJhbiB2YSBDSFVBIHhv'
'bmciKQogICAga2V0KCJNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIsIGNodWFfdHJvbiBpZiBub3QgZG9fbGEgZWxz'
'ZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9fbGEgZWxzZSBmImxhOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXX0i'
'KQogICAgaWYgZG9fdGhpZXVfY29uZ19jdToKICAgICAgICBrZXQoIkNvbmcgY3UgZGF5IGR1IGRlIGRvIiwgS0RELCBmInRo'
'aWV1IGNvbmcgY3UgY2hvIHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV19IikKCiAgICBicSA9IHNvcnRl'
'ZCh7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXRfbil9LCBrZXk9c29fY2EpOyBnaGkoImNhX2JvX3F1YSIs'
'IGJxKQogICAgaW5uKCIiKTsgaW5uKGYiICBCTyBRVUEgKHtsZW4oYnEpfSk6IHtbeC5zcGxpdCgnXycpWzBdIGZvciB4IGlu'
'IGJxXX0iKQoKICAgIGlubigiIik7IGlubigiICBOMS1ONCAodDE2NS10MTY4KSwgdGlldSBjaGkgbmdoaWVtIHRodSBjdWEg'
'cjIsIG5heSBsYSBjaGkgYmFvIGhvaSBxdXk6IikKICAgIGI0ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0FN'
'T0l9OyBnaGkoImNhX21vaSIsIGI0KQogICAgZm9yIHQgaW4gQ0FNT0k6IGlubihmIiAgICAge3R9OiB7YjRbdF19IikKICAg'
'ICMgQk9fUVVBL3ZhbmcgbGEgQ0hVQSBDSEFZLCBraG9uZyBwaGFpIERPOiBjaGkgbW90IGNhIERPIG1vaSBkdW9jIHBoYXQg'
'VFJVT1QuCiAgICBrZXQoIk4xLU40ICh0MTY1LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJRVUEiIGZvciB2IGluIGI0LnZh'
'bHVlcygpKQogICAgICAgIGVsc2UgKFRSVU9UIGlmIGFueSh2ID09ICJETyIgZm9yIHYgaW4gYjQudmFsdWVzKCkpIGVsc2Ug'
'S0REKSwgc3RyKGI0KSkKCiAgICBpbm4oIiIpOyBpbm4oIiAgMTUgY2EgdHVuZyBkbyB0cmVuIENJOiIpCiAgICBiMTUgPSB7'
'dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQogICAgaW5uKCIgICAgIiArICIg'
'ICIuam9pbihmInt0fTp7YjE1W3RdfSIgZm9yIHQgaW4gQ0ExNSkpCgogICAgIyB0MTM2IOKAlCBOMTIgZG8gR0lBTiBUSUVQ'
'IHF1YSBrZXQgcXVhIGNhCiAgICB0MTM2X3RlbiA9IG5leHQoKHQgZm9yIHQgaW4gZG9faGV0IGlmIHQuc3RhcnRzd2l0aCgi'
'dDEzNiIpKSwgTm9uZSkKICAgIGlmIGIxNS5nZXQoInQxMzYiKSA9PSAiUVVBIjoKICAgICAgICBrZXQoIk4xMiB0MTM2IChx'
'dWEga2V0IHF1YSBjYSkiLCBEQVQsICJ0MTM2IFFVQSIpCiAgICBlbGlmIGIxNS5nZXQoInQxMzYiKSAhPSAiRE8iOgogICAg'
'ICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIEtERCwgZiJ0MTM2ID0ge2IxNS5nZXQoJ3QxMzYnKSFyfSDi'
'gJQga2hvbmcgY2hheS9raG9uZyB0aGF5IikKICAgIGVsc2U6CiAgICAgICAgbHkgPSBkb19oZXQuZ2V0KHQxMzZfdGVuLCAi'
'IikKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBUUlVPVCwgZiJETzoge2x5Wzo5MF19IikKCiMg'
'LS0tLS0tLS0tLS0tLS0tLSAzLiBwcm9iZSBUSEFORyB2YW8gaGFtIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCIt'
'IiAqIDc4KTsgaW5uKCIzLiBQUk9CRSBUSEFORyDigJQgZ29pIF9naXRfd2luZG93cyB2b2kgdGhhbSBzbyB0aWVtIikKc3Bl'
'YyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscDU0MSIsIHN0cih0ZXApKQpscCA9IGltcG9y'
'dGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9kdWxlKGxwKQpzaWcgPSBpbnNw'
'ZWN0LnNpZ25hdHVyZShscC5fZ2l0X3dpbmRvd3MpCmdoaSgidGhhbV9zb19fZ2l0X3dpbmRvd3MiLCBsaXN0KHNpZy5wYXJh'
'bWV0ZXJzKSkKaW5uKCIgIHRoYW0gc28gY3VhIF9naXRfd2luZG93czoiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKCmRlZiBn'
'b2koKiprdyk6CiAgICAiIiJHb2kgX2dpdF93aW5kb3dzLCBCQVQgc3RkZXJyIGRlIG1vdCBkb25nIGNoYW4gZG9hbiBraG9u'
'ZyBnaWV0IGx1b3QgZG8uIiIiCiAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0'
'ZGVycihlKToKICAgICAgICByID0gbHAuX2dpdF93aW5kb3dzKCoqa3cpCiAgICByZXR1cm4gciwgZS5nZXR2YWx1ZSgpCgoj'
'IC0tLSBkb2kgY2h1bmcgcmlnOiBwaGFpIHRyYSBsb2kgZHVuZyBtb3QgY2EgdGEgQklFVCBUUlVPQyBkYXAgYW4gLS0tCndp'
'dGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgIG5nb2FpID0gUGF0aCh0KS8ibmdvYWkiOyBuZ29h'
'aS5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2Rpcigp'
'CiAgICAobmdvYWkvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIxLCBfID0gZ29p'
'KHBhdGg9c3RyKG5nb2FpKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIChjdy8iZ2l0LmV4ZSIp'
'LndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjIsIF8gPSBnb2kocGF0aD1zdHIoY3cpLCBwcm9ncmFt'
'X2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQpyaWdfb2sgPSBib29sKHIxKSBhbmQgcjIgaXMgTm9uZQpnaGkoInJpZ19k'
'b2lfY2h1bmciLCByaWdfb2spCmtldCgiUklHIGRvaSBjaHVuZyAoYmlldCB0cnVvYyBkYXAgYW4pIiwgREFUIGlmIHJpZ19v'
'ayBlbHNlIEtERCwKICAgIGYibmdvYWktY3dkLT57J05IQU4nIGlmIHIxIGVsc2UgJ05vbmUnfSB8IHRyb25nLWN3ZC0+eydO'
'SEFOJyBpZiByMiBlbHNlICdOb25lJ30iKQppZiBub3QgcmlnX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9D'
'OiByaWcgc2FpLCBtb2kgY2hvdCBkdW9pIHNlIHZvIG5naGlhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0gTU9JIENPTkcgUEhB'
'SSBUVSBDSFVORyBNSU5IIE5PIENPIFRIRSBETyAtLS0KIyBCYWkgaG9jIGRhdCBuaGF0IGN1YSBwYWNrZXQgbmF5OiBkb19u'
'MTAgYmFuIGN1IGNoYW0gREFUIGNobyA5NTgzMTY4NSB0cm9uZyBraGkgdDE3MQojIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8g'
'dmkgZHVuZyBraHV5ZXQgdGF0IG1hIE4xMCBzaW5oIHJhIGRlIGJhdC4gTm8gZGVnZW5lcmF0ZSDigJQKIyB0cmVuIFdpbmRv'
'd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgbmVuICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIGN1bmcga2V0IHF1YS4K'
'IyBNb3QgY29uZyBraG9uZyB0aGUgRE8gdGhpIGtob25nIHBoYWkgY29uZywgdmEgbm8gbmd1eSBoaWVtIGhvbiBraG9uZyBj'
'byBjb25nOiBubwojIHBoYXQgcmEgbW90IGNodSBEQVQuCiMKIyBOZW4gdHJ1b2Mga2hpIERVTkcgbmFtIGNvbmcgbmF5IGRl'
'IHBoYW4gcXV5ZXQsIGJhdCB0dW5nIGNvbmcgZ2lldCBtb3QgZG90IGJpZW4gZGEKIyBiaWV0IHRyb25nLiBDb25nIG5hbyBr'
'aG9uZyBnaWV0IGR1b2MgdGhpIGNodSBEQVQgY3VhIG5vIGJpIEhBIHh1b25nIEtIT05HIERPIERVT0M7CiMgVFJVT1QgZ2l1'
'IG5ndXllbiAocXVhbiBzYXQgdHJ1YyB0aWVwLCB2ZC4gZzEgdmFuIG5oYW4gZ2l0LmJhdCkuIERvdCBiaWVuIGNoYXkgdHJl'
'biBCQU4gU0FPIFRBTTsgY2F5IHRoYXQga2hvbmcgYmkKIyBkdW5nIHRvaSAoY3VuZyBreSBsdWF0IG5odSBONykuCkRPVF9C'
'SUVOX1RVX0tJRU0gPSBbCiAgICAoIk44IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAnaWYgY2hpX2RpbmggYW5k'
'IFBhdGgoY2hpX2RpbmgpLm5hbWUubG93ZXIoKSA9PSAiZ2l0LmV4ZSIgYW5kIGhvcF9sZShjaGlfZGluaCk6JywKICAgICAi'
'aWYgY2hpX2RpbmggYW5kIGhvcF9sZShjaGlfZGluaCk6IiksCiAgICAoIk45IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwK'
'ICAgICAiZCA9IGRfcmF3LnN0cmlwKCkuc3RyaXAoJ1wiJykiLCAiZCA9IGRfcmF3LnN0cmlwKCkiKSwKICAgICgiTjEwIiwg'
'Im9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAic2VwID0gb3MucGF0aHNlcCBpZiBwaGFuX2NhY2ggaXMgTm9uZSBlbHNl'
'IHBoYW5fY2FjaCIsICJzZXAgPSBvcy5wYXRoc2VwIiksCiAgICAoIk4xMSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsICJp'
'ZiBjaGFuX2RvYW4gaXMgbm90IE5vbmU6IiwgImlmIEZhbHNlOiIpLAogICAgKCJOMTIiLCAib3BzL2xlYXNlX3B1Ymxpc2hf'
'dGVzdC5weSIsCiAgICAgJ2dpdF9wYXRoPSIvL2tob25nLWNvL2dpdCInLCAnZ2l0X3BhdGg9Ii9raG9uZy1jby9naXQiJyks'
'Cl0KaW5uKCIiKTsgaW5uKCIgIHR1IGtpZW0gY29uZyDigJQgbW9pIGNvbmcgcGhhaSBnaWV0IGR1b2MgbW90IGRvdCBiaWVu'
'IGRhIGJpZXQ6IikKZ2lldCA9IHt9CmZvciBtYSwgZHVvbmcsIHRpbSwgdGhheSBpbiBET1RfQklFTl9UVV9LSUVNOgogICAg'
'X3RlbiwgX2hhbSA9IG5leHQoKChhLCBiKSBmb3IgYSwgYiBpbiBQUk9CRSBpZiBhLnN0YXJ0c3dpdGgobWEgKyAiICIpKSwg'
'KE5vbmUsIE5vbmUpKQogICAgaWYgX2hhbSBpcyBOb25lOgogICAgICAgIGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHtt'
'YTo0fSBLSE9ORyBETyBEVU9DOiBraG9uZyB0aW0gdGhheSBwcm9iZSB0ZW4gJ3ttYX0gLi4uJyIpOyBjb250aW51ZQogICAg'
'dHJ5OgogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgX3Q6CiAgICAgICAgICAgIF9jID0g'
'UGF0aChfdCkvImNheSI7IHNodXRpbC5jb3B5dHJlZShnb2MvIm9wcyIsIF9jLyJvcHMiKQogICAgICAgICAgICBfZiA9IF9j'
'L2R1b25nOyBfbmQgPSBfZi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgaWYgX25kLmNvdW50KHRp'
'bSkgIT0gMToKICAgICAgICAgICAgICAgIGdpZXRbbWFdID0gTm9uZQogICAgICAgICAgICAgICAgaW5uKGYiICAgIHttYTo0'
'fSBLSE9ORyBETyBEVU9DOiBtYXUgZG90IGJpZW4ga2hvcCB7X25kLmNvdW50KHRpbSl9IGxhbiAobW9uZyAxKSIKICAgICAg'
'ICAgICAgICAgICAgICBmIiDigJQgbWEgbmd1b24gZGEgZG9pLCBkb3QgYmllbiBuYXkgaGV0IHkgbmdoaWEiKTsgY29udGlu'
'dWUKICAgICAgICAgICAgX2Yud3JpdGVfdGV4dChfbmQucmVwbGFjZSh0aW0sIHRoYXksIDEpLCBlbmNvZGluZz0idXRmLTgi'
'KQogICAgICAgICAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfZGJfIiArIG1h'
'LCBzdHIoX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgICAgICAgICAgX20gPSBpbXBvcnRsaWIudXRpbC5tb2R1'
'bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX20pCiAgICAgICAgICAgIGRlZiBfZ29pX2RiKCoq'
'a3cpOgogICAgICAgICAgICAgICAgX2UgPSBpby5TdHJpbmdJTygpCiAgICAgICAgICAgICAgICB3aXRoIGNvbnRleHRsaWIu'
'cmVkaXJlY3Rfc3RkZXJyKF9lKToKICAgICAgICAgICAgICAgICAgICByZXR1cm4gX20uX2dpdF93aW5kb3dzKCoqa3cpLCBf'
'ZS5nZXR2YWx1ZSgpCiAgICAgICAgICAgIF90dCwgX2N0LCBfID0gX2hhbShfZ29pX2RiLCBpbnNwZWN0LnNpZ25hdHVyZShf'
'bS5fZ2l0X3dpbmRvd3MpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2hf'
'dGVzdC5weSIpCiAgICAgICAgZ2lldFttYV0gPSAoX3R0ID09IFRSVU9UKQogICAgICAgIGlubihmIiAgICB7bWE6NH0gZG90'
'IGJpZW4gLT4ge190dDoxNH0geydHSUVUIERVT0MnIGlmIF90dCA9PSBUUlVPVCBlbHNlICdTT05HIFNPVCd9IgogICAgICAg'
'ICAgICArIChmIiAgICh7X2N0fSkiIGlmIF9jdCBlbHNlICIiKSkKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgX2U6CiAgICAg'
'ICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IHt0eXBlKF9lKS5fX25hbWVfX306'
'IHtfZX0iKQpnaGkoImNvbmdfZ2lldF9kdW9jX2RvdF9iaWVuIiwgZ2lldCkKCmZvciB0ZW4sICh0dCwgY3QsIGRsKSBpbiBb'
'KHQsIGYoZ29pLCBzaWcsIHRlcHQpKSBmb3IgdCwgZiBpbiBQUk9CRV06CiAgICBnaGkoInByb2JlXyIgKyB0ZW4uc3BsaXQo'
'KVswXS5sb3dlcigpLCBkbCkKICAgIGlmIGlzaW5zdGFuY2UoZGwsIGRpY3QpOgogICAgICAgIGZvciBrLCB2IGluIGRsLml0'
'ZW1zKCk6IGlubihmIiAgICB7azozNH06IHt2fSIpCiAgICBtYSA9IHRlbi5zcGxpdCgpWzBdCiAgICBpZiBnaWV0LmdldCht'
'YSkgaXMgbm90IFRydWUgYW5kIHR0ID09IERBVDoKICAgICAgICAjIERBVCB0dSBtb3QgY29uZyBjaHVhIGNodW5nIG1pbmgg'
'ZHVvYyBsYSBiaWV0IERPIHRoaSBraG9uZyBkYW5nIHRpbiBob24gS0RELgogICAgICAgIGtldCh0ZW4sIEtERCwgZiJjb25n'
'IEtIT05HIGdpZXQgZHVvYyBkb3QgYmllbiBjdWEgY2hpbmggbm8gKHtnaWV0LmdldChtYSkhcn0pIgogICAgICAgICAgICAg'
'ICAgICAgICAgZiIgLT4gY2h1IERBVCBuYXkga2hvbmcgY28gZ2lhIHRyaSIpCiAgICBlbHNlOgogICAgICAgIGtldCh0ZW4s'
'IHR0LCBjdCkKCiMgLS0tLS0tLS0tLS0tLS0tLSA0LiBONyBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIC0tLS0tLS0tLS0t'
'LS0tLS0KaWYgbm90IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiNC4gTjcg4oCUIGRvdCBi'
'aWVuIHRyZW4gQkFOIFNBTyBUQU0gKGNheSB0aGF0IEtIT05HIGJpIGR1bmcgdG9pKSIpCiAgICB0cnVvYyA9IHRlcC5yZWFk'
'X3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTikKICAgIGdoaSgibjdfdHJ1b2MiLCB0cnVvYyk7IGlubihm'
'IiAgc28gZG9uZyBraG9wIHtNQVVfV0lOIXJ9OiBUUlVPQyA9IHt0cnVvY30gW21vbmcgMV0iKQogICAgaWYgdHJ1b2MgIT0g'
'MToKICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsIGYibWF1IHh1YXQgaGllbiB7dHJ1b2N9'
'IGxhbiwga2hvbmcgcGhhaSAxIikKICAgIGVsc2U6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3Rvcnko'
'KSBhcyB0bXA6CiAgICAgICAgICAgIHNhbyA9IFBhdGgodG1wKS8iY2F5IgogICAgICAgICAgICBzaHV0aWwuY29weXRyZWUo'
'Z29jLCBzYW8sIGlnbm9yZT1zaHV0aWwuaWdub3JlX3BhdHRlcm5zKCIuZ2l0IiwgIl9fcHljYWNoZV9fIiwgIioucHljIikp'
'CiAgICAgICAgICAgIGYyID0gc2FvLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IgogICAgICAgICAgICBmMi53cml0ZV90ZXh0'
'KGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5yZXBsYWNlKE1BVV9XSU4sICJpZiBGYWxzZToiKSwgZW5jb2Rpbmc9'
'InV0Zi04IikKICAgICAgICAgICAgc2F1ID0gZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4p'
'OyBnaGkoIm43X3NhdSIsIHNhdSkKICAgICAgICAgICAgaW5uKGYiICBTQVUgKGRhIGRvdCBiaWVuKSA9IHtzYXV9IFttb25n'
'IDBdIikKICAgICAgICAgICAgaWYgc2F1ICE9IDA6CiAgICAgICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdp'
'bmRvd3MiLCBLREQsICJkb3QgYmllbiBLSE9ORyBhcCBkdW9jIikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAg'
'IHJjX20sIG91dF9tID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgc2FvKQogICAgICAgICAgICAgICAg'
'bTE2NSA9IG1hdV9jYShvdXRfbSwgInQxNjUiKTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20pCiAgICAgICAgICAgICAgICB0'
'ZW4xNjUgPSBuZXh0KCh0IGZvciB0IGluIGRtIGlmIHQuc3RhcnRzd2l0aCgidDE2NSIpKSwgTm9uZSkKICAgICAgICAgICAg'
'ICAgIGx5ID0gKGRtLmdldCh0ZW4xNjUpIG9yICIiKQogICAgICAgICAgICAgICAgZ2hpKCJuN190MTY1IiwgbTE2NSk7IGdo'
'aSgibjdfbHlfZG8iLCBseVs6MjAwXSkKICAgICAgICAgICAgICAgIGlubihmIiAgdDE2NSBzYXUgZG90IGJpZW46IHttMTY1'
'fSB8IHtseVs6MTEwXX0iKQogICAgICAgICAgICAgICAgZHVuZ19seV9kbyA9ICJQQVRIIHQiIGluIGx5IG9yICIvdXNyL2Jp'
'biIgaW4gbHkKICAgICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIERBVCBpZiAobTE2NSA9'
'PSAiRE8iIGFuZCBkdW5nX2x5X2RvKSBlbHNlCiAgICAgICAgICAgICAgICAgICAgKFRSVU9UIGlmIG0xNjUgPT0gIkRPIiBl'
'bHNlIEtERCksCiAgICAgICAgICAgICAgICAgICAgImdpZXQgZHVuZyBseSBkbyIgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVu'
'Z19seV9kbykKICAgICAgICAgICAgICAgICAgICBlbHNlICgiRE8gbmh1bmcgS0hPTkcgZHVuZyBseSBkbyAtPiB0aW4gZHVu'
'ZyBnaWEiIGlmIG0xNjUgPT0gIkRPIiBlbHNlICJraG9uZyBkb2MgZHVvYyB0MTY1IikpCgojIC0tLS0tLS0tLS0tLS0tLS0g'
'S0VUIExVQU4gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIj0iICogNzgpCmlubihmIlRIRSBIRSBETyBEVU9DOiB7'
'dGhlX2hlfSAgIEhFQUQ9e2hlYWRbOjEyXX0iKQojIEtob2kgZGFuIGNobyByZXZpZXdlciBiYXQgZGF1IG8gZG9uZyB0cmVu'
'LCBuZW4gQ0hFIERPIHBoYWkgbmFtIE5HQVkgZHVvaSBubzoga2hvbmcgY28gZG9uZyBuYXkKIyB0aGkgbW90IGx1b3QgLS1j'
'aGktcHJvYmUgaW4gIkRBVCA3IHwgVFJVT1QgMCB8IEtIT05HIERPIERVT0MgMCIgcmM9MCBtYSBraG9uZyBub2kgbGEgY2h1'
'YSBjaGF5IGJvIHRlc3QuCmdoaSgiY2hlX2RvIiwgImNoaS1wcm9iZSIgaWYgQ0hJX1BST0JFIGVsc2UgImRheS1kdSIpCmlm'
'IENISV9QUk9CRToKICAgIGlubigiLS1jaGktcHJvYmU6IENISSBkbyBtdWMgMCwgMSwgMy4gQm8gdGVzdCwgTjEtTjQsIHQx'
'MzYsIE43IEtIT05HIGNoYXkgLSBkYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCmlmIHRoZV9oZSA9PSAi'
'ZzEiOgogICAgaW5uKCJMVVUgWTogZGF5IGxhIE5FTiBETyAoZzEpLCBLSE9ORyBwaGFpIG5naGllbSB0aHUgZzIuIENhYyBj'
'aG90IE44LU4xMiBkdW9pIGRheSIpCiAgICBpbm4oIiAgICAgICBUUlVPVCBsYSBEVU5HIE5IVSBNT05HIOKAlCBjaHVuZyBs'
'YSBuaHVuZyBsbyBnMiBzaW5oIHJhIGRlIHbDoS4iKQppbm4oIi0iICogNzgpCmZvciB0ZW4sIHR0LCBjdCBpbiBjaG90Ogog'
'ICAgaW5uKGYiICB7dHQ6MTR9IHt0ZW59IiArIChmIiAgIHtjdH0iIGlmIGN0IGVsc2UgIiIpKQpuX2tkZCA9IHN1bSgxIGZv'
'ciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCm5fdHJ1b3QgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQg'
'PT0gVFJVT1QpCmlubigiLSIgKiA3OCkKaW5uKGYiICBEQVQge3N1bSgxIGZvciBfLHQsXyBpbiBjaG90IGlmIHQ9PURBVCl9'
'IHwgVFJVT1Qge25fdHJ1b3R9IHwgS0hPTkcgRE8gRFVPQyB7bl9rZGR9IikKaW5uKGYiICBUb25nIGNhIGRvOiB7c28uZ2V0'
'KCdzb19jYV9kbycpfSB8IGRhbmggc2FjaCBkYXkgZHU6IHsnQ08nIGlmIHNvLmdldCgnbGlldF9rZV9kYXlfZHUnKSBlbHNl'
'ICdLSE9ORyBETyBEVU9DJ30iKQppbm4oZiIgIEFkbWluaXN0cmF0b3I6IHtzby5nZXQoJ3F1eWVuX2FkbWluJyl9IHwgc3lt'
'bGluazoge3NvLmdldCgnc3ltbGlua19kdW9jJyl9IikKaW5uKCIiKTsgaW5uKCItLS0gREFOIE5HVVlFTiBLSE9JIEpTT04g'
'TkFZIFZFIENITyBSRVZJRVdFUiAtLS0iKQpnaGkoImNob3QiLCBbeyJ0ZW4iOiBhLCAidHJhbmdfdGhhaSI6IGIsICJjaGlf'
'dGlldCI6IGN9IGZvciBhLCBiLCBjIGluIGNob3RdKQppbm4oanNvbi5kdW1wcyhzbywgZW5zdXJlX2FzY2lpPUZhbHNlLCBp'
'bmRlbnQ9MSwgZGVmYXVsdD1zdHIpKQojIHJjOiAwID0gbW9pIGNob3QgREFUIHwgMSA9IGNvIGNob3QgVFJVT1QgfCAzID0g'
'Y28gY2hvdCBLSE9ORyBETyBEVU9DICh1dSB0aWVuIGJhbyBkb25nKQpzeXMuZXhpdCgzIGlmIG5fa2RkIGVsc2UgKDEgaWYg'
'bl90cnVvdCBlbHNlIDApKQo='
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
