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
$ShaBoDo    = '477cfda2f4273b35f2726ab092ff9d6fb407bbe23df98c9170f23998c990efde'      # SHA-256 cua bo do Python nhung ben duoi

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
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0xMC0wMWUiICAgICAgICAgICAgICAj'
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
'IE5IQU4gLS1ub3JjIOKAlCBtdWMgMCBob2kgdHJ1b2MpLgojIEJpZW4gS0hPSSBET05HIGN1YSBiYXNoIENVQSBOR1VPSSBE'
'TyBsb3QgdmFvIGJvIHRlc3QgeSBuaHUgYmEgbmhvbSB0cmVuOiB0MzIvdDUxLXQ2OCBjaGF5IGJhc2ggdm9pIGRpY3Qob3Mu'
'ZW52aXJvbiwgLi4uKS4gRG8KIyB0cmVuIDIwMjYtMTAtMDEgKGJhbiAwMWQpLCAwZWE5NWRlOiBTSEVMTE9QVFM9bm9jbG9i'
'YmVyLCBob2FjIEJBU0hfRU5WIGNodWEgYHNldCAtbyBub2Nsb2JiZXJgID0+IHQzMiB0NTEgdDYwIHQ2MiB0NjMgdDY2IHQ2'
'OCBETwojICJjYW5ub3Qgb3ZlcndyaXRlIGV4aXN0aW5nIGZpbGUiIOKAlCBjYSAibGEiID0+IFRSVU9UIGNobyB1bmcgdmll'
'biBzYWNoIOKAlCB0cm9uZyBraGkgbXVjIDAgY2hvIHF1YTogbm8gaG9pIGBnaXQgLS12ZXJzaW9uYAojIHRyb25nIGJhc2gs'
'IGNhdSBIRVAgaG9uIGNhdSBibyB0ZXN0IGNhbi4gQkFTSF9FTlYgaW4gYnl0ZSBuZ29haSBVVEYtOCA9PiAxNTIvMTY2LiBD'
'SSBraG9uZyBkYXQgYmllbiBuYW8gdHJvbmcgbmhvbSBuYXkuIEJvCiMgdGhlbyBUQVAgYmFzaCgxKSBkb2Mga2hpIGNoYXkg'
'c2NyaXB0OiBtb2kgdGVuIGJhdCBkYXUgYEJBU0hgIChCQVNIX0VOViBCQVNIT1BUUyBCQVNIX0ZVTkNfKiBCQVNIX1hUUkFD'
'RUZEIEJBU0hfQ09NUEFUIC4uLikgY29uZwojIF9CQVNIX0tIT0lfRE9ORy4gQ2hpIGhhaSBtdWMgdHJlbiBETyBEVU9DIGxh'
'bSBETzsgY2FjIHRlbiBjb24gbGFpIGJvIHZpIENJIGtob25nIGRhdCwgS0hPTkcgdmkgZGEgdGhheSBETyAoZG8gMjAyNi0x'
'MC0wMTogU0hFTExPUFRTCiMgeHRyYWNlL25vdW5zZXQvcGlwZWZhaWwvbm9nbG9iL2FsbGV4cG9ydCwgQkFTSE9QVFMgZmFp'
'bGdsb2IvbnVsbGdsb2IveHBnX2VjaG8sIFBPU0lYTFlfQ09SUkVDVCwgQ0RQQVRILCBGVU5DTkVTVD0xLCBUTU9VVD0xID0+'
'CiMgOS85IGNhIGJhc2gpLiBJRlMgYmFzaCBLSE9ORyBuaGFuIHR1IG1vaSB0cnVvbmcuIHQxNTIgdm9uIGNoaSB0cnV5ZW4g'
'UEFUSCBuZW4ga2hvbmcgZG9pLiBNdWMgMCB0dSBraGFpIFRFTiAoa2hvbmcgaW4gZ2lhIHRyaSkuCl9CQVNIX0tIT0lfRE9O'
'RyA9IGZyb3plbnNldCh7IlNIRUxMT1BUUyIsICJFTlYiLCAiUE9TSVhMWV9DT1JSRUNUIiwgIkNEUEFUSCIsICJHTE9CSUdO'
'T1JFIiwgIkdMT0JTT1JUIiwgIkVYRUNJR05PUkUiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICJGVU5DTkVTVCIs'
'ICJUTU9VVCJ9KQpkZWYgX2JpZW5fYmFzaChrKTogcmV0dXJuIGsudXBwZXIoKS5zdGFydHN3aXRoKCJCQVNIIikgb3Igay51'
'cHBlcigpIGluIF9CQVNIX0tIT0lfRE9ORwpfR0lUX0dMT0JBTF9DSSA9ICJbaW5pdF1cblx0ZGVmYXVsdEJyYW5jaCA9IG1h'
'c3RlclxuW2NvcmVdXG5cdGF1dG9jcmxmID0gZmFsc2Vcblx0ZW9sID0gbGZcblx0YWJicmV2ID0gN1xuIgpkZWYgY2hheShh'
'cmd2LCBjd2QsIHBodXQ9NjApOgogICAgZmQsIGdjID0gdGVtcGZpbGUubWtzdGVtcChwcmVmaXg9IndwNTQxLWdpdGNvbmZp'
'Zy1jaS0iLCBzdWZmaXg9Ii5pbmkiKQogICAgeGRnID0gTm9uZQogICAgdHJ5OgogICAgICAgIHhkZyA9IHRlbXBmaWxlLm1r'
'ZHRlbXAocHJlZml4PSJ3cDU0MS14ZGctIikKICAgICAgICB3aXRoIG9zLmZkb3BlbihmZCwgInciLCBlbmNvZGluZz0iYXNj'
'aWkiLCBuZXdsaW5lPSJcbiIpIGFzIGY6IGYud3JpdGUoX0dJVF9HTE9CQUxfQ0kpCiAgICAgICAgbXQgPSB7azogdiBmb3Ig'
'aywgdiBpbiBvcy5lbnZpcm9uLml0ZW1zKCkKICAgICAgICAgICAgICBpZiBub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIkdJ'
'VF8iKSBhbmQgbm90IF9iaWVuX2Jhc2goaykKICAgICAgICAgICAgICBhbmQgKG5vdCBrLnVwcGVyKCkuc3RhcnRzd2l0aCgi'
'UFlUSE9OIikgb3Igay51cHBlcigpIGluIF9QWV9HSVUpfQogICAgICAgIG10LnVwZGF0ZShQWVRIT05VVEY4PSIxIiwgUFlU'
'SE9OSU9FTkNPRElORz0idXRmLTgiLCBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0iMSIsIFBZVEhPTlVOQlVGRkVSRUQ9IjEi'
'LAogICAgICAgICAgICAgICAgICBHSVRfQ09ORklHX0dMT0JBTD1nYywgWERHX0NPTkZJR19IT01FPXhkZywgU0hFTExDSEVD'
'S19PUFRTPSItLW5vcmMiKQogICAgICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbc3lzLmV4ZWN1dGFibGVdICsgYXJndiwgY3dk'
'PXN0cihjd2QpLCBjYXB0dXJlX291dHB1dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICB0ZXh0PVRydWUsIGVu'
'Y29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCwgZW52PW10KQogICAgZmluYWxseToK'
'ICAgICAgICB0cnk6IG9zLnJlbW92ZShnYykKICAgICAgICBleGNlcHQgT1NFcnJvcjogcGFzcwogICAgICAgIGlmIHhkZzog'
'c2h1dGlsLnJtdHJlZSh4ZGcsIGlnbm9yZV9lcnJvcnM9VHJ1ZSkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91'
'dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1X2NhKG91dCwgdCk6CiAgICBtID0gcmUuc2VhcmNoKHIiKD9t'
'KV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSBbMC05Ll0rcyAoXHcrKVxzKiQiLCBvdXQpCiAgICByZXR1cm4gbS5n'
'cm91cCgyKSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdpdChnb2MsICphLCBwaHV0PTUpOgogICAgcCA9IHN1YnByb2Nlc3MucnVu'
'KFsiZ2l0IiwgIi1DIiwgc3RyKGdvYyksICphXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLAogICAgICAgICAg'
'ICAgICAgICAgICAgIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCkKICAgIHJl'
'dHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikuc3RyaXAoKSwgKHAuc3RkZXJyIG9yICIiKS5zdHJpcCgpCgoK'
'IyA9PT09PT09PT09PT09PT09PSBOQU0gUFJPQkUsIHZpZXQgdGhhbmggSEFNIFRIVUFOIGRlIFRVIEtJRU0gZHVvYyA9PT09'
'PT09PT09PT09PT09PQojIE1vaSBoYW0gdHJhICh0cmFuZ190aGFpLCBjaGlfdGlldCwgZHVfbGlldSkuIEtIT05HIGluLCBL'
'SE9ORyB0aG9hdCDigJQgbmhvIHZheSBjaHVuZwojIGNoYXkgZHVvYyB0cmVuIG5lbiBCQVQgS1ksIHZhIGAtLXR1LWtpZW0t'
'cHJvYmVgIGdvaSB0aGFuZyBjaHVuZyBkZSBraWVtIGNoaW5oIGJvIGRvLgoKZGVmIF9zYW4odCk6CiAgICBkID0gUGF0aCh0'
'KS8iZCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYu'
'bWtkaXIoKQogICAgcmV0dXJuIGQsIGN3LCBwZgoKZGVmIGRvX244KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkJ1b2MgMSAo'
'Q09OR19DVV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0LmV4ZS4gRG9pIGNodW5nIGR1b25nOiBnaXQuZXhlIFZBTiBwaGFpIG5o'
'YW4uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAg'
'ZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIGZvciB0ZW4gaW4gKCJnaXQuZXhlIiwgImdpdC5iYXQiLCAiZ2l0LmNtZCIs'
'ICJnaXQucHkiLCAia2hvbmctcGhhaS1naXQudHh0Iik6CiAgICAgICAgICAgIGYgPSBkL3RlbjsgZi53cml0ZV90ZXh0KCJ4'
'IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyA9IGdvaShjb25nX2N1X2dpdD1zdHIoZiksIHBhdGg9IiIs'
'IHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIGtxW2YiQ09OR19DVV9HSVQ9e3Rlbn0i'
'XSA9ICJOSEFOIiBpZiByIGVsc2UgIlRVIENIT0kiCiAgICBsb3QgPSBbayBmb3IgaywgdiBpbiBrcS5pdGVtcygpIGlmIHYg'
'PT0gIk5IQU4iIGFuZCBub3Qgay5lbmRzd2l0aCgiZ2l0LmV4ZSIpXQogICAgaWYga3EuZ2V0KCJDT05HX0NVX0dJVD1naXQu'
'ZXhlIikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogZ2l0LmV4ZSBob3Ag'
'bGUgbWEgYmkgdHUgY2hvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgbG90IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90'
'IGxvdCBlbHNlIGYiY29uIG5oYW46IHtsb3R9IiksIGtxCgpkZWYgZG9fbjkoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiTXVj'
'IFBBVEggYm9jIG5oYXkga2VwIHBoYWkgTkhBTjsgbXVjIHJvbmcgLyB0b2FuIGtob2FuZyB0cmFuZyBwaGFpIGJvIHF1YSwg'
'a2hvbmcgbmVtLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0Ogog'
'ICAgICAgIGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsg'
'cGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNv'
'ZGluZz0idXRmLTgiKQogICAgICAgIGZvciBuaGFuLCBtdWMgaW4gKCgia2hvbmcgbmhheSIsIHN0cihkKSksICgiY28gbmhh'
'eSBrZXAiLCBmJyJ7ZH0iJyksCiAgICAgICAgICAgICAgICAgICAgICAgICAgKCJyb25nIiwgIiIpLCAoImNoaSBraG9hbmcg'
'dHJhbmciLCAiICAgIikpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICByLCBfID0gZ29pKHBhdGg9bXVjLCBw'
'cm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0g'
'Ik5IQU4iIGlmIHIgZWxzZSAiTm9uZSIKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAg'
'ICAga3FbZiJQQVRIIHtuaGFufSJdID0gZiJORU0ge3R5cGUoZSkuX19uYW1lX199IgogICAgaWYga3EuZ2V0KCJQQVRIIGto'
'b25nIG5oYXkiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBtdWMgUEFU'
'SCB0aHVvbmcgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgb2sgPSAoa3EuZ2V0KCJQQVRIIGNvIG5oYXkga2Vw'
'IikgPT0gIk5IQU4iCiAgICAgICAgICBhbmQga3EuZ2V0KCJQQVRIIHJvbmciKSA9PSAiTm9uZSIgYW5kIGtxLmdldCgiUEFU'
'SCBjaGkga2hvYW5nIHRyYW5nIikgPT0gIk5vbmUiKQogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBp'
'ZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKIyBEYXUgcGhhbiBjYWNoIGR1bmcgREUgVEhVLiBQaGFpIEtIQUMgb3MucGF0'
'aHNlcCB0cmVuIENBIEhBSSBuZW4gKCc7JyBXaW5kb3dzLCAnOicgUE9TSVgpCiMgdGhpIGhhaSBnaWEgdGh1eWV0ICJ0YWNo'
'IHRoZW8gZGF1IGR1b2MgdHJ1eWVuIiB2YSAidGFjaCB0aGVvIG9zLnBhdGhzZXAiIG1vaSByb2kgcmEgbmhhdS4KVEhVX04x'
'MCA9ICJ8IgoKZGVmIGRvX24xMChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW0gcGhhaSB0YWNoIFBBVEggdGhlbyBkYXUg'
'cGhhbiBjYWNoIERVT0MgVFJVWUVOLCBraG9uZyB0aGVvIG9zLnBhdGhzZXAgY3VhIG5lbi4KCiAgICBCYW4gY3UgZG8gIm1v'
'dCBkYXUgJzsnIHRyb25nIFRFTiB0aHUgbXVjIiB2YSBkYXQgREFUIHRyZW4gV2luZG93cyBkdSBoYW0gc2FpLiBObwogICAg'
'ZGVnZW5lcmF0ZTogdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnLCBuZW4gJ0M6L2E7YicgdGhhdCBzdSBDTyBO'
'R0hJQSBsYSBoYWkKICAgIG11YyDigJQgInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gcmEgY3VuZyBrZXQgcXVhLCBw'
'aGVwIGRvIGtob25nIHRoZSBkbyBuYW8uIE5vCiAgICBkYSBjaGFtIERBVCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEg'
'Y3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQgYXkuCiAgICBNb3QgY29uZyBraG9uZyB0aGUgZG8g'
'dGhpIGtob25nIHBoYWkgY29uZy4KICAgICIiIgogICAgdGVuX3NlcCA9IG5leHQoKGsgZm9yIGsgaW4gKCJwaGFuX2NhY2gi'
'LCAiZGF1X3BoYW5fY2FjaCIsICJzZXAiKSBpZiBrIGluIHNpZy5wYXJhbWV0ZXJzKSwgTm9uZSkKICAgIGlmIHRlbl9zZXAg'
'aXMgTm9uZToKICAgICAgICAjIEtob25nIGNvIHRoYW0gc28gdGhpIHRyZW4gV2luZG93cyBLSE9ORyBjb24gZHVvbmcgbmFv'
'IHRhY2ggaGFpIGdpYSB0aHV5ZXQuCiAgICAgICAgaWYgb3MucGF0aHNlcCA9PSAiOyI6CiAgICAgICAgICAgIHJldHVybiAo'
'S0RELCAidHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIHZhIGhhbSBraG9uZyBuaGFuIHRoYW0gc28gZGF1IHBo'
'YW4gY2FjaCAiCiAgICAgICAgICAgICAgICAgICAgICAgICAiLT4ga2hvbmcgdGFjaCBkdW9jIGhhaSBnaWEgdGh1eWV0IiwK'
'ICAgICAgICAgICAgICAgICAgICB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiBOb25lfSkKICAg'
'ICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgICAgIGxhID0gUGF0aCh0KS8i'
'Y287ZGF1IjsgbGEubWtkaXIoKQogICAgICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgICAgIChkLyJnaXQu'
'ZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8gID0gZ29pKHBhdGg9c3Ry'
'KGxhKSArIG9zLnBhdGhzZXAgKyBzdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAg'
'ICAgIHIwLCBfID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAg'
'IGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZSwKICAgICAgICAgICAgICAiY28g'
'bXVjIGNodWEgJzsnIjogIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIsCiAgICAgICAgICAgICAgImRvaSBjaHVuZyBkdW9uZyAo'
'a2hvbmcgY28gJzsnKSI6ICJOSEFOIiBpZiByMCBlbHNlICJOb25lIn0KICAgICAgICBpZiBub3QgcjA6CiAgICAgICAgICAg'
'IHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZyIsIGtxCiAgICAgICAgcmV0dXJuIChEQVQgaWYgciBlbHNlIFRS'
'VU9UKSwgKCIiIGlmIHIgZWxzZSAibXVjIGdpdC5leGUgaG9wIGxlIGJpIE1BVCIpLCBrcQoKICAgIHdpdGggdGVtcGZpbGUu'
'VGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkgICAg'
'ICAgICAgIyAnOycgbmFtIHRyb25nIFRFTiwga2hvbmcgcGhhaSBkYXUgcGhhbiBjYWNoCiAgICAgICAgZCwgY3csIHBmID0g'
'X3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAg'
'bm9pID0gc3RyKGxhKSArIFRIVV9OMTAgKyBzdHIoZCkKICAgICAgICBrdyA9IGRpY3QocHJvZ3JhbV9maWxlcz1zdHIocGYp'
'LCBjd2Q9c3RyKGN3KSkKICAgICAgICByX2NoaW5oLCBfID0gZ29pKHBhdGg9bm9pLCAgICAgICoqe3Rlbl9zZXA6IFRIVV9O'
'MTB9LCAgICoqa3cpICAgIyB0YWNoIGR1bmcgIC0+IE5IQU4KICAgICAgICByX2R1b25nLCBfID0gZ29pKHBhdGg9c3RyKGQp'
'LCAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyBkb2kgY2h1bmcgZHVvbmcKICAgICAgICByX3BoYW5iaWV0'
'LCBfID0gZ29pKHBhdGg9bm9pLCAgICoqe3Rlbl9zZXA6IG9zLnBhdGhzZXB9LCAqKmt3KSAgIyB0YWNoIHRoZW8gb3MucGF0'
'aHNlcCAtPiBtYXQKICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogdGVuX3NlcCwg'
'ImRhdSB0aHUiOiBUSFVfTjEwLAogICAgICAgICAgZiJub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtUSFVfTjEw'
'IXJ9IjogICAgICAgIk5IQU4iIGlmIHJfY2hpbmggZWxzZSAiTm9uZSIsCiAgICAgICAgICBmImRvaSBjaHVuZyBkdW9uZyAo'
'bW90IG11Yywge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9KSI6ICAiTkhBTiIgaWYgcl9kdW9uZyBlbHNlICJOb25lIiwKICAgICAg'
'ICAgIGYicGhhbiBiaWV0OiBub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtvcy5wYXRoc2VwIXJ9IjogIk5IQU4i'
'IGlmIHJfcGhhbmJpZXQgZWxzZSAiTm9uZSJ9CiAgICBpZiBub3Qgcl9kdW9uZzoKICAgICAgICByZXR1cm4gS0RELCAiZG9p'
'IGNodW5nIGR1b25nIGhvbmc6IG1vdCBtdWMgaG9wIGxlIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EKICAgICMgQ29u'
'ZyBwaGFpIENPIFRIRSBkby4gTmV1IGNhIGhhaSBkYXUgcGhhbiBjYWNoIGRldSByYSBOSEFOIHRoaSBwaGVwIGRvIGtob25n'
'IHBoYW4KICAgICMgYmlldCBkdW9jIGdpIOKAlCBkdW5nIGJhbyBEQVQsIGJhbyB0aGFuZyBsYSBraG9uZyBkbyBkdW9jLgog'
'ICAgaWYgcl9waGFuYmlldDoKICAgICAgICByZXR1cm4gKEtERCwgZiJwaGVwIGRvIEtIT05HIHBoYW4gYmlldCBkdW9jOiBu'
'b2kgYmFuZyB7VEhVX04xMCFyfSBtYSB0YWNoIHRoZW8gIgogICAgICAgICAgICAgICAgICAgICBmIntvcy5wYXRoc2VwIXJ9'
'IFZBTiB0aW0gcmEgZ2l0LmV4ZSIsIGtxKQogICAgcmV0dXJuICgoREFULCAiIiwga3EpIGlmIHJfY2hpbmggZWxzZQogICAg'
'ICAgICAgICAoVFJVT1QsIGYidGFjaCB0aGVvIG9zLnBhdGhzZXAgdGhheSB2aSB0aGVvIHt0ZW5fc2VwfSBkdW9jIHRydXll'
'biIsIGtxKSkKCgpkZWYgZG9fbjExKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIlRydXllbiBjaGFuX2RvYW4gPT4gdGh1IGR1'
'b2MgdGhvbmcgYmFvIFZBIHN0ZGVyciBJTS4gS2hvbmcgdHJ1eWVuID0+IHN0ZGVyciBWQU4gY28uIiIiCiAgICBpZiAiY2hh'
'bl9kb2FuIiBub3QgaW4gc2lnLnBhcmFtZXRlcnM6CiAgICAgICAgcmV0dXJuIEtERCwgIl9naXRfd2luZG93cyBraG9uZyBu'
'aGFuIHRoYW0gc28gY2hhbl9kb2FuIiwgeyJ0aGFtIHNvIjogbGlzdChzaWcucGFyYW1ldGVycyl9CiAgICB3aXRoIHRlbXBm'
'aWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJn'
'aXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgY2QgPSBbXQogICAgICAgIF8sIGVf'
'Y28gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdyksIGNoYW5fZG9hbj1jZCkK'
'ICAgICAgICBfLCBlX2toID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQog'
'ICAga3EgPSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAobXVjKSI6IGxlbihjZCksCiAgICAgICAgICAic3RkZXJyIGtoaSBDTyBj'
'aGFuX2RvYW4gKGJ5dGUpIjogbGVuKGVfY28uZW5jb2RlKCkpLAogICAgICAgICAgInN0ZGVyciBraGkgS0hPTkcgdHJ1eWVu'
'IChieXRlKSI6IGxlbihlX2toLmVuY29kZSgpKX0KICAgIGlmIGxlbihjZCkgPT0gMCBhbmQgbGVuKGVfa2guZW5jb2RlKCkp'
'ID09IDA6CiAgICAgICAgcmV0dXJuIEtERCwgIm5oYW5oICVQcm9ncmFtRmlsZXMlIGtob25nIHBoYW4gZ2lhaSBLSE9ORyBi'
'YXkgcmEgY2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRvIGR1b2MiLCBrcQogICAgb2sgPSBsZW4oY2QpID4gMCBhbmQgbGVuKGVf'
'Y28uZW5jb2RlKCkpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA+IDAKICAgIHJldHVybiAoREFUIGlmIG9rIGVsc2Ug'
'VFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCmRlZiBkb19uMTIoZ29pLCBzaWcsIHRlcHQpOgogICAg'
'IiIiSGFuZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9uZyBmaXh0dXJlIHBoYWkgdHV5ZXQgZG9pIHRyZW4gQ0EgSEFJIG5lbi4i'
'IiIKICAgIG5kID0gdGVwdC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIikKICAgIGhhbmcg'
'PSBzb3J0ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRfcGF0aFxzKj1ccyoiKFteIl0rKSInLCBuZCkpKQogICAgeGF1ID0gW2gg'
'Zm9yIGggaW4gaGFuZyBpZiBub3QgKFB1cmVQb3NpeFBhdGgoaCkuaXNfYWJzb2x1dGUoKSBhbmQgUHVyZVdpbmRvd3NQYXRo'
'KGgpLmlzX2Fic29sdXRlKCkpXQogICAga3EgPSB7ImhhbmcgZ2l0X3BhdGggdGltIHRoYXkiOiBoYW5nLCAiY2hpIHR1eWV0'
'IGRvaSBNT1QgbmVuIjogeGF1fQogICAgaWYgbm90IGhhbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImtob25nIHRpbSB0aGF5'
'IGhhbmcgZ2l0X3BhdGggbmFvIHRyb25nIGZpeHR1cmUgLT4gbWF1IGRvYyBjbyB0aGUgZGEgZG9pIiwga3EKICAgIHJldHVy'
'biAoREFUIGlmIG5vdCB4YXUgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgeGF1IGVsc2UgZiJjaGktbW90LW5lbjoge3hhdX0i'
'KSwga3EKClBST0JFID0gWygiTjggYnVvYyAxIGNoaSBuaGFuIGdpdC5leGUiLCBkb19uOCksCiAgICAgICAgICgiTjkgYm9j'
'IG5oYXkga2VwIG8gbXVjIFBBVEgiLCBkb19uOSksCiAgICAgICAgICgiTjEwIGRhdSAnOycgdHJvbmcgdGVuIHRodSBtdWMi'
'LCBkb19uMTApLAogICAgICAgICAoIk4xMSBjaGFuIGRvYW4gZG9pIGtlbmgiLCBkb19uMTEpLAogICAgICAgICAoIk4xMiBo'
'YW5nIHNlbnRpbmVsIHR1eWV0IGRvaSBDQSBIQUkgbmVuIiwgZG9fbjEyKV0KCiMgLS0tIGNoZSBkbyBUVSBLSUVNOiBjaGF5'
'IG5hbSBwcm9iZSB0cmVuIG1vdCBjYXkgYmF0IGt5LCBuZW4gYmF0IGt5IC0tLQppZiAiLS10dS1raWVtLXByb2JlIiBpbiBz'
'eXMuYXJndjoKICAgIF9nID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS10dS1raWVtLXByb2JlIikgKyAxXSku'
'cmVzb2x2ZSgpCiAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfdGsiLCBzdHIo'
'X2cvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgIF9scCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMo'
'X3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbHApCiAgICBfc2lnID0gaW5zcGVjdC5zaWduYXR1cmUoX2xwLl9naXRf'
'd2luZG93cykKICAgIGRlZiBfZ29pKCoqa3cpOgogICAgICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICAgICAgd2l0aCBjb250'
'ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICAgICAgcmV0dXJuIF9scC5fZ2l0X3dpbmRvd3MoKiprdyksIGUu'
'Z2V0dmFsdWUoKQogICAgcHJpbnQoZiJUVSBLSUVNIFBST0JFIHRyZW4ge19nfSAgKG5lbiB7c3lzLnBsYXRmb3JtfSkiKQog'
'ICAgZm9yIF90ZW4sIF9mIGluIFBST0JFOgogICAgICAgIF90dCwgX2N0LCBfZGwgPSBfZihfZ29pLCBfc2lnLCBfZy8ib3Bz'
'Ii8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBwcmludChmIiAgW3tfdHQ6MTR9XSB7X3Rlbn0iICsgKGYiICAg'
'e19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgICAgICBmb3IgX2ssIF92IGluIChfZGwgb3Ige30pLml0ZW1zKCk6IHByaW50'
'KGYiICAgICAgICB7X2s6MzR9OiB7X3Z9IikKICAgIHN5cy5leGl0KDApCgojIC0tLSBjaGUgZG8gS0lFTSBET05HIEJPOiB0'
'ZXAgLnB5IG5heSBwaGFpIFRSVU5HIFRVTkcgQllURSB2b2kgYmFuIG5odW5nIHRyb25nIHBzMSAtLS0KIyBLaG9uZyBjb25n'
'IG5hbyBidW9jIGhhaSBiYW4gc2FvIGtob3A6IGRvIGR1b2MsIG5vaSB0cmFuIDIvNDAwIC0+IDk5Lzk5OTk5IENISSB0cm9u'
'ZyAucHkKIyB0aGkgY2lfZGFuZ19reSBsYW4gdDI2L3QyNyB2YW4geGFuaCwgY29uIGNob3QgU0hBIGN1YSBwczEgY2hpIHNv'
'IGJhbiBuaHVuZyB2b2kgaGFuZyBzbwojIGN1YSBDSElOSCBuby4gQ2hheTogcHl0aG9uIHdwNTQxLWRvLWcyLXdpbmRvd3Mu'
'cHkgLS1raWVtLWRvbmctYm8gd3A1NDEtZG8tZzIucHMxICAocmMgMHwzKQppZiAiLS1raWVtLWRvbmctYm8iIGluIHN5cy5h'
'cmd2OgogICAgaW1wb3J0IGJhc2U2NAogICAgX3BzID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS1raWVtLWRv'
'bmctYm8iKSArIDFdKS5yZWFkX3RleHQoZW5jb2Rpbmc9ImFzY2lpIikKICAgIF9tID0gcmUuc2VhcmNoKHIiKD9tcyleXCRC'
'NjQgPSBAXCgoLio/KV5cKSIsIF9wcykKICAgIF9rID0gcmUuc2VhcmNoKHIiKD9tKV5cJFNoYUJvRG9ccyo9XHMqJyhbMC05'
'YS1mXXs2NH0pJyIsIF9wcykKICAgIF9uaHVuZyA9IGJhc2U2NC5iNjRkZWNvZGUoIiIuam9pbihyZS5maW5kYWxsKHIiJyhb'
'QS1aYS16MC05Ky89XSopJyIsIF9tLmdyb3VwKDEpKSkpIGlmIF9tIGVsc2UgYiIiCiAgICBfdG9pID0gUGF0aChfX2ZpbGVf'
'XykucmVhZF9ieXRlcygpCiAgICBfb2sgPSBib29sKF9tIGFuZCBfaykgYW5kIF9uaHVuZyA9PSBfdG9pIGFuZCBoYXNobGli'
'LnNoYTI1NihfdG9pKS5oZXhkaWdlc3QoKSA9PSBfay5ncm91cCgxKQogICAgaW5uKGYiS0lFTSBET05HIEJPOiB7REFUIGlm'
'IF9vayBlbHNlIEtERH0gIChuaHVuZyB7bGVuKF9uaHVuZyl9IGJ5dGUsIHRlcCB7bGVuKF90b2kpfSBieXRlKSIpCiAgICBz'
'eXMuZXhpdCgwIGlmIF9vayBlbHNlIDMpCgppbm4oIj0iICogNzgpOyBpbm4oIldQNTQxIGcyIC0gcGhlcCBkbyB0cmVuIFdp'
'bmRvd3MgdGhhdCAoc3BlYyByMzogTjEtTjQsIE44LU4xMiwgTjcsIGtpY2ggdGh1b2MpIik7IGlubigiPSIgKiA3OCkKCiMg'
'LS0tLS0tLS0tLS0tLS0tLSB0dSBraWVtIGJvIGRvYyAtLS0tLS0tLS0tLS0tLS0tCl9kLCBfZywgX3QgPSBkb2NfZG8oX01B'
'VSkKX29rID0gKGxlbihfZCkgPT0gMiBhbmQgYW55KHguc3RhcnRzd2l0aCgidDAyYiIpIGZvciB4IGluIF9kKQogICAgICAg'
'YW5kIG5vdCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMxIikgZm9yIHggaW4gX2QpIGFuZCBfdCkKaW5uKCJUdSBraWVtIGJvIGRv'
'YyBsb2c6IiwgREFUIGlmIF9vayBlbHNlIFRSVU9UKQppZiBub3QgX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBE'
'VU9DOiBibyBkb2MgbG9nIGN1YSBjaGluaCBzY3JpcHQgbmF5IHNhaSAtPiBraG9uZyBkbyBnaSBjYS4iKTsgc3lzLmV4aXQo'
'MykKCiMgLS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4gZG8gLS0tLS0tLS0tLS0tLS0tLQpnb2MgPSBQYXRoKHN5cy5hcmd2WzFd'
'KS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQYXRoLmN3ZCgpCnRlcCwgdGVwdCA9IGdvYyAvICJvcHMi'
'IC8gImxlYXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiCmlubigiIik7IGlu'
'bigiLSIgKiA3OCk7IGlubigiMC4gTkVOIERPIikKIyBNT0kgTE9HIFBIQUkgVFUgS0hBSSBubyBkbyBDQUkgR0kgYmFuZyBC'
'TyBETyBOQU8uIEJhaSBob2MgMTktMDktMjAyNjogbW90IGx1b3QgZG8KIyBndWkgdmUgZHVvYyBkb2Mgbmh1IGtldCBxdWEg'
'Y3VhIGJhbiB2YSBkYW5nIHhldCwgbmh1bmcgdGhhdCByYSBsYSBiYW4gZG8gQ1UgY2hheQojIHRyZW4gbmhhbmggS0hBQy4g'
'RG9jIHJhIHRoaSBtYXQgbW90IHZvbmc7IGxvZyB0dSBraGFpIHRoaSB0aGF5IG5nYXkgZG9uZyBkYXUuCnRyeToKICAgIF90'
'dSA9IGhhc2hsaWIuc2hhMjU2KFBhdGgoX19maWxlX18pLnJlYWRfYnl0ZXMoKSkuaGV4ZGlnZXN0KCkKZXhjZXB0IEV4Y2Vw'
'dGlvbiBhcyBfZToKICAgIF90dSA9IGYia2hvbmcgdHUgYmFtIGR1b2M6IHtfZX0iCmdoaSgiYm9fZG9fc2hhMjU2IiwgX3R1'
'KQppbm4oZiIgIEJPIERPICAgICAgICA6IHNoYTI1NiB7X3R1WzoxNl19ICAoYmFuIHtCQU5fQk9fRE99KSIpCmlubigiICBz'
'eXMucGxhdGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwgInwgcHl0aG9uIiwgc3lzLnZlcnNpb24uc3BsaXQoKVswXSkKaW5uKCIg'
'IG9zLnBhdGhzZXAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSwgInwgUEFUSEVYVDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQ'
'QVRIRVhUIikpWzo2MF0pCmlubigiICBQcm9ncmFtRmlsZXMgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlByb2dyYW1GaWxl'
'cyIpKSwgInwgU3lzdGVtUm9vdDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290IikpKQppbm4oIiAgQ09OR19D'
'VV9HSVQgIDoiLCByZXByKF9DT05HX0NVX0dJVF9OR1VPSV9ETykKICAgICsgKCIgIC0+IERBIEJPIGtob2kgbHVvdCBkbyAo'
'Q0kga2hvbmcgZGF0IGJpZW4gbmF5OyB4ZW0gZGF1IHRlcCkiIGlmIF9DT05HX0NVX0dJVF9OR1VPSV9ETyBpcyBub3QgTm9u'
'ZSBlbHNlICIiKSkKZ2hpKCJjb25nX2N1X2dpdF9uZ3VvaV9kbyIsIF9DT05HX0NVX0dJVF9OR1VPSV9ETykKX2Jhc2hfYm8g'
'PSBnaGkoImJpZW5fYmFzaF9uZ3VvaV9kb19kYV9ibyIsIHNvcnRlZChrIGZvciBrIGluIG9zLmVudmlyb24gaWYgX2JpZW5f'
'YmFzaChrKSkpCmlubigiICBiaWVuIGJhc2ggICAgOiIsICgiLCAiLmpvaW4oX2Jhc2hfYm8pICsgIiAgLT4gREEgQk8ga2hv'
'aSBsdW90IGNvbiAoQ0kga2hvbmcgZGF0OyB4ZW0gY2hheSgpKSIpIGlmIF9iYXNoX2JvIGVsc2UgIihraG9uZyBjbykiKQpp'
'bm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5vbmUKaWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6CiAg'
'ICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4gPSBib29sKGN0eXBlcy53aW5kbGwuc2hlbGwzMi5Jc1VzZXJB'
'bkFkbWluKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXllbiA9IE5vbmUKZ2hpKCJxdXllbl9hZG1pbiIsIHF1eWVuKQpz'
'eW1saW5rX2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAg'
'ICAgICBkID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHRy'
'eTogb3Muc3ltbGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJsayIpKTsgc3ltbGlua19kdW9jID0gVHJ1ZQogICAgICAgIGV4'
'Y2VwdCBPU0Vycm9yIGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZhbHNlOyBnaGkoInN5bWxpbmtfbG9pIiwgZiJ7dHlwZShlKS5f'
'X25hbWVfX306IHtlfSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZTogZ2hpKCJzeW1saW5rX2xvaSIsIHN0cihlKSkKZ2hpKCJz'
'eW1saW5rX2R1b2MiLCBzeW1saW5rX2R1b2MpCmlubigiICBBZG1pbmlzdHJhdG9yOiIsIHF1eWVuLCAifCB0YW8gc3ltbGlu'
'ayBkdW9jOiIsIHN5bWxpbmtfZHVvYykKCmxvaSA9IFtdCiMgQ29uZyBraWNoIHRodW9jIGxhIHBoZXAgZG8gdHJlbiBMSUNI'
'IFNVIEdJVCwga2hvbmcgZGluaCBnaSBkZW4gbmVuLiBDaG8gcGhlcAojIC0tY2hpLWtpY2gtdGh1b2MgY2hheSBvIG1vaSBu'
'ZW4gZGUgY29uIFRVIEtJRU0gZHVvYyBjaGluaCBjb25nIG5heSAoZGEgZHVuZwojIGRlIHRhaSBkdW5nIGNhIGhhaSB2ZSBj'
'dWEgc3UgY28gbmVuLWN1IDE5LTA5KS4gTW9pIGNob3QgQ0hVQyBOQU5HIHZhbiBkb2kgV2luZG93cy4KaWYgc3lzLnBsYXRm'
'b3JtICE9ICJ3aW4zMiIgYW5kICItLWNoaS1raWNoLXRodW9jIiBub3QgaW4gc3lzLmFyZ3Y6CiAgICBsb2kuYXBwZW5kKGYi'
'S0hPTkcgcGhhaSBXaW5kb3dzIChzeXMucGxhdGZvcm09e3N5cy5wbGF0Zm9ybSFyfSkiKQppZiBub3QgdGVwLmlzX2ZpbGUo'
'KTogIGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB9IikKaWYgbm90IHRlcHQuaXNfZmlsZSgpOiBsb2kuYXBwZW5kKGYi'
'a2hvbmcgdGhheSB7dGVwdH0iKQppZiBub3Qgc2h1dGlsLndoaWNoKCJnaXQiKTogbG9pLmFwcGVuZCgia2hvbmcgY28gYGdp'
'dGAgdHJvbmcgUEFUSCIpCiMgQm8gdGVzdCAobXVjIDIgdmEgTjcpIGNhbiBQeVlBTUw6IHRoaWV1IG5vLCAwZWE5NWRlIHJh'
'IDk2LzE2NiBjYSBETyAoODkgYmFvIHRoYW5nICJObyBtb2R1bGUgbmFtZWQgJ3lhbWwnIiwKIyA3IHF1YSBsdW90IGNvbjsg'
'Y28gUHlZQU1MOiAxNjYvMTY2IFFVQSkuIEJvIGRvIGdvaSBjaHVuZyBsYSAiY2EgRE8gTEEiIHJvaSBwaGF0IFRSVU9UIOKA'
'lCBkbyB0cmVuIDIwMjYtMDktMzBjLgojIERpZXUga2llbiB0aWVuIHF1eWV0IHBoYWkgaG9pIGJhbmcgQ0hJTkggdGllbiB0'
'cmluaCBjb24gc2UgY2hheSBibyB0ZXN0IChjaGF5KCk6IGN1bmcgbW9pIHRydW9uZzsgY3dkID0gb3BzLyA9CiMgc3lzLnBh'
'dGhbMF0gY3VhIGJvIHRlc3QpIHZhIGhvaSBEVU5HIERVT0MgY2h1IGtob25nIGhvaSBDTyBNQVQuIEJhbiAzMGQgaG9pIGBm'
'aW5kX3NwZWMoInlhbWwiKWAgbyB0aWVuIHRyaW5oCiMgTkFZIHZhIG5ndW9uZyAzLjggc3V5IHR1IE5HVSBQSEFQIChgOj1g'
'KSDigJQgZG8gdHJlbiAyMDI2LTA5LTMwZCwgY2EgaGFpIHJhIHJjPTEgVFJVT1QgY2hvIHVuZyB2aWVuIHNhY2g6CiMgdGh1'
'IG11YyBkdSBsaWV1IGB5YW1sL2AgdHJlbiBQWVRIT05QQVRIIHF1YSBmaW5kX3NwZWMgbWEgYHlhbWwuc2FmZV9kdW1wYCBr'
'aG9uZyBjbyAoODcgY2EgImxhIik7IHB5dGhvbiAzLjguMjAKIyBUSEFUIGNvIFB5WUFNTCwgYm8gdGVzdCBkdW5nIGBzdHIu'
'cmVtb3ZlcHJlZml4YCAoMy45KSBsdWMgQ0hBWSAoMzMgY2EgImxhIjsgMy45LjIzOiAxNjYvMTY2KS4KIyAiRHVuZyBkdW9j'
'IiBuZ2hpYSBsYSBkdW5nIERVTkcgQVBJIGJvIHRlc3QgZ29pOiB2aWV0KCkgKDQzIGxvaSBnb2kpIHZhIGxlYXNlX3B1Ymxp'
'c2gucHkgZ29pIHNhZmVfZHVtcCguLi4sIGFsbG93X3VuaWNvZGU9VHJ1ZSwKIyBzb3J0X2tleXM9RmFsc2UpLCBtYSBgc29y'
'dF9rZXlzYCBjaGkgY28gdHUgUHlZQU1MIDUuMS4gRG8gdHJlbiAyMDI2LTA5LTMwbCwgMGVhOTVkZTogcHl0aG9uIDMuOS4y'
'MyArIFB5WUFNTCAzLjEzIFRIQVQgcXVhIHByb2JlCiMgY3UgKHJjPTApLCBibyB0ZXN0IDEwOS8xNjYg4oCUIDU2IGNhICJs'
'YSI6IDUyIGB1bmV4cGVjdGVkIGtleXdvcmQgYXJndW1lbnQgJ3NvcnRfa2V5cydgLCB0MjYvdDI3IGBSZWFkZXJFcnJvcmAg'
'KGt5IHR1IG5nb2FpIEJNUCksCiMgdDEyNC90MTUzIERPIHRoZW8gbHVvdCBjb24g4oCUIGUyZSByYz0xIGBEQVQgMTEgfCBU'
'UlVPVCAxYDsgUHlZQU1MIDUuMTogMTY2LzE2NiAoZG8gbGFpIDIwMjYtMTAtMDE6IGN1bmcgc28pLgojIChQeXRob24gPj0g'
'My4xMCArIFB5WUFNTCAzLjEzIGRhIHRydW90IHByb2JlIGN1IHZpIGBjb2xsZWN0aW9ucy5IYXNoYWJsZWAuKSBQcm9iZSBj'
'dWEgcHMxICgkbWFUaHUpIHBoYWkgR0lPTkcgSEVUIGRvbmcgZHVvaS4KaWYgbm90ICgiLS1jaGkta2ljaC10aHVvYyIgaW4g'
'c3lzLmFyZ3Ygb3IgIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndik6CiAgICBfcmNfZGssIF9yYV9kayA9IGNoYXkoWyItYyIs'
'ICJpbXBvcnQgc3lzOyBzeXMuZXhpdCg5KSBpZiBzeXMudmVyc2lvbl9pbmZvIDwgKDMsIDkpIGVsc2UgTm9uZTsgaW1wb3J0'
'IHlhbWw7IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiIHlhbWwuc2FmZV9kdW1wKHlhbWwuc2FmZV9sb2Fk'
'KCdhOiAxJyksIGFsbG93X3VuaWNvZGU9VHJ1ZSwgc29ydF9rZXlzPUZhbHNlKSJdLAogICAgICAgICAgICAgICAgICAgICAg'
'ICAgIGdvYyAvICJvcHMiIGlmIChnb2MgLyAib3BzIikuaXNfZGlyKCkgZWxzZSBQYXRoLmN3ZCgpLCBwaHV0PTIpCiAgICBp'
'ZiBfcmNfZGsgPT0gOToKICAgICAgICBsb2kuYXBwZW5kKGYicHl0aG9uIHtzeXMudmVyc2lvbi5zcGxpdCgpWzBdfSA8IDMu'
'OTogYm8gdGVzdCBjdWEgdW5nIHZpZW4gZHVuZyBzdHIucmVtb3ZlcHJlZml4ICgzLjkpIGx1YyBDSEFZIikKICAgIGVsaWYg'
'X3JjX2RrOgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24gbmF5IEtIT05HIGNvIFB5WUFNTCBkdW5nIGR1b2MgKHsoX3Jh'
'X2RrLnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10pWy0xXVs6OTBdfSk6IgogICAgICAgICAgICAgICAgICAgZiIgXCJ7'
'c3lzLmV4ZWN1dGFibGV9XCIgLW0gcGlwIGluc3RhbGwgLVUgcHl5YW1sIgogICAgICAgICAgICAgICAgICAgIiAoYmFuIG5o'
'dW5nIHBzMSB0dSB0YWkgS0hPTkcgY28gcGlwOiBjaGF5IGxhaSB2b2kgLVB5IDxweXRob24gZGEgY28gUHlZQU1MPikiKQog'
'ICAgIyBCbyB0ZXN0IGNvbiBnb2kgYHNodXRpbC53aGljaGAgY2hvIGJhc2gvYWN0aW9ubGludC9zaGVsbGNoZWNrICgwZWE5'
'NWRlOiB0MzMgdDEzNyB0MTU5IGNhbiBhY3Rpb25saW50LCB0MTM3IGNhbgogICAgIyBzaGVsbGNoZWNrLCBjYWMgY2EgY2hh'
'eSBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggY2FuIGJhc2gpLiBUaGlldSB0aGkgY2FjIGNhIGF5IGluICJLSE9ORyBETyBEVU9D'
'OiB0aGlldSBgLi4uYCIgdmEgYm8gZG8gcmEKICAgICMgcmM9MyDigJQgbmh1bmcgY2hpIFNBVSBjYSBibyB0ZXN0IGxhbiBO'
'NyAoZG8gdHJlbiAyMDI2LTA5LTMwZywgUEFUSCB0aGlldSBhY3Rpb25saW50OiBgQ29uZyBjdSBkYXkgZHUgZGUgZG9gIEtE'
'RCwgcmM9MwogICAgIyBzYXUgMiBsdW90IGJvIHRlc3QpLiBDdW5nIGx5IGRvIFB5WUFNTCBkdW9jIGhvaSBvIGRheTogaG9p'
'IFRSVU9DLCBjdW5nIFBBVEggbWEgY2hheSgpIHRydXllbiBjaG8gYm8gdGVzdC4KICAgICMgVkEgY3VuZyBDSE8gYm8gdGVz'
'dCBkdW5nOiB0cmVuIFdpbmRvd3MgYHNodXRpbC53aGljaGAgdHJhIFRIVSBNVUMgSElFTiBIQU5IIFRSVU9DIFBBVEgsIG1h'
'IGJvIHRlc3QgY2hheSB2b2kgY3dkID0gZ29jIGNvbgogICAgIyB0aWVuIHRyaW5oIG5heSBkdW5nIG8gY3dkIENVQSBOR1VP'
'SSBETyAobm9pIGdvaSBwczEsIHZkLiBEb3dubG9hZHMg4oCUIGR1bmcgbm9pIGdpYWkgbmVuIGFjdGlvbmxpbnQuZXhlKS4g'
'RG8gdHJlbiAyMDI2LTA5LTMwawogICAgIyAobmhhbmggd2luMzIgVEhBVCBjdWEgc2h1dGlsLndoaWNoKTogYWN0aW9ubGlu'
'dCB0b3QgbyBjd2Qgbmd1b2kgZG8gKyBiYW4gaG9uZyBkYXUgUEFUSCA9PiBtdWMgMCBob2kgYmFuIG8gY3dkIChyYz0wKSwg'
'Ym8gdGVzdAogICAgIyBkdW5nIGJhbiB0cmVuIFBBVEggPT4gcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0MzMn'
'LCAndDEzNycsICd0MTU5J11gLiBHaWFpIHRlbiB2b2kgY3dkID0gZ29jIHJvaSBnb2kgVEhBTkcgYmFuZyBkdW9uZwogICAg'
'IyBUVVlFVCBET0kgZGEgZ2lhaSAocXVhIGhhbiB0aGkgcnVuKCkgZ2lldCBkdW5nIHRpZW4gdHJpbmgg4oCUIGx5IGRvIGJh'
'biAzMGkga2hvbmcgaG9pIHF1YSBjaGF5KCkpLgogICAgX2N3ZF9uZ3VvaV9kbyA9IG9zLmdldGN3ZCgpCiAgICB0cnk6CiAg'
'ICAgICAgaWYgZ29jLmlzX2RpcigpOiBvcy5jaGRpcihnb2MpCiAgICAgICAgX2NjID0ge2M6IChvcy5wYXRoLmFic3BhdGgo'
'cCkgaWYgcCBlbHNlIE5vbmUpIGZvciBjLCBwIGluCiAgICAgICAgICAgICAgICgoYywgc2h1dGlsLndoaWNoKGMpKSBmb3Ig'
'YyBpbiAoImJhc2giLCAiYWN0aW9ubGludCIsICJzaGVsbGNoZWNrIikpfQogICAgZmluYWxseToKICAgICAgICBvcy5jaGRp'
'cihfY3dkX25ndW9pX2RvKQogICAgX3RoaWV1X2NjID0gW2MgZm9yIGMsIHAgaW4gX2NjLml0ZW1zKCkgaWYgbm90IHBdCiAg'
'ICBpZiBfdGhpZXVfY2M6CiAgICAgICAgbG9pLmFwcGVuZChmInRoaWV1IGNvbmcgY3UgYm8gdGVzdCBnb2kgcXVhIFBBVEg6'
'IHtfdGhpZXVfY2N9IChhY3Rpb25saW50OiBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggdm9pIEFMX1ZFUjsiCiAgICAgICAgICAg'
'ICAgICAgICAiIGJhc2g6IEdpdCBCYXNoLCBraG9uZyBwaGFpIGJhc2guZXhlIGN1YSBXU0wpIikKICAgICMgc2hlbGxjaGVj'
'ayBLSE9ORyBuaGFuIC0tbm9yYyB0aGkgYWN0aW9ubGludCAxLjcuNyAodHUgdHJ1eWVuIC0tbm9yYykgbGFtIHQzMyBETywg'
'dmEgU0hFTExDSEVDS19PUFRTPS0tbm9yYyBjdWEgY2hheSgpIGxhbQogICAgIyB0MTM3IERPIOKAlCBjYSAibGEiID0+IFRS'
'VU9UIGdpYSAoZG8gdHJlbiAyMDI2LTA5LTMwaCwgc2hlbGxjaGVjayBnaWEgdHUgY2hvaSAtLW5vcmM6IGJhbiAzMGggcmM9'
'MSBgbGE6IFsndDMzJ11gIHNhdSBjYQogICAgIyBibyB0ZXN0KS4gYHdoaWNoYCBjaGkgaG9pIENPIE1BVDsgbyBkYXkgaG9p'
'IERVTkcgRFVPQy4gTmd1b25nIGRvIHRyZW4gc2hlbGxjaGVjayBUSEFUOiAwLjQuNy8wLjUuMC8wLjYuMCB0dSBjaG9pIC0t'
'bm9yYwogICAgIyAocmM9MyksIDAuNy4wIHRybyBsZW4gbmhhbi4gUGhlcCBob2kgcGhhaSB0aGF5IERVTkcgU0hFTExDSEVD'
'S19PUFRTIG1hIGNoYXkoKSBkYXQgY2hvIGx1b3QgY29uOiBiYW4gMzBpIGhvaSB2b2kgYmllbiBDVUEKICAgICMgTkdVT0kg'
'RE8g4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGksIHNoZWxsY2hlY2sgMC45LjAgKyBTSEVMTENIRUNLX09QVFM9LS1leHRlbmRl'
'ZC1hbmFseXNpcz10cnVlIChjbyBjdWEgMC4xMCk6IHJjPTMgImtob25nIG5oYW4KICAgICMgLS1ub3JjOiBjYXAgbmhhdCBz'
'aGVsbGNoZWNrIiB0cm9uZyBraGkgdDMzL3QxMzcgcXVhIGNoYXkoKSBkZXUgMS8xLiBHb2kgVEhBTkcgKGtob25nIHF1YSBj'
'aGF5KCkpOiBxdWEgaGFuIHRoaSBydW4oKSBnaWV0CiAgICAjIGR1bmcgc2hlbGxjaGVjazsgcXVhIGNoYXkoKSB0aGkgY2hp'
'IGdpZXQgcHl0aG9uIGNvbiwgc2hlbGxjaGVjayB0cmVvIG8gbGFpIG1vIGNvaSAoZG8gdHJlbiAyMDI2LTA5LTMwaTogMS8x'
'IGNvbiBzb25nKS4KICAgIGVsaWYgc3VicHJvY2Vzcy5ydW4oW19jY1sic2hlbGxjaGVjayJdLCAiLS1ub3JjIiwgIi0tdmVy'
'c2lvbiJdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0aW1lb3V0PTYwLAogICAgICAgICAgICAgICAgICAgICAgICBlbnY9ZGlj'
'dChvcy5lbnZpcm9uLCBTSEVMTENIRUNLX09QVFM9Ii0tbm9yYyIpKS5yZXR1cm5jb2RlOgogICAgICAgIGxvaS5hcHBlbmQo'
'InNoZWxsY2hlY2sgdHJlbiBQQVRIIGtob25nIG5oYW4gLS1ub3JjIChhY3Rpb25saW50IDEuNy43IHZhIGNoYXkoKSBkZXUg'
'dHJ1eWVuIGNvIGF5KTogY2FwIG5oYXQgc2hlbGxjaGVjayIpCiAgICAjIGFjdGlvbmxpbnQgY3VuZyBwaGFpIERVTkcgRFVP'
'Qywga2hvbmcgY2hpIENPIE1BVDogdDMzL3QxMzcvdDE1OSBnb2kgbm8gVEhBTkcsIHZhIG1vdCBhY3Rpb25saW50IGtob25n'
'IGNoYXkgKHNhaSBraWVuIHRydWMsCiAgICAjIGhvbmcpIGxhbSBjYSBiYSBETyAiYWN0aW9ubGludCBETyAocmM9Li4uKSIg'
'4oCUIGNhICJsYSIgPT4gVFJVT1QgZ2lhIHNhdSBjYSBibyB0ZXN0IChkbyB0cmVuIDIwMjYtMDktMzBqOiBhY3Rpb25saW50'
'IGdpYQogICAgIyByYz0xID0+IG11YyAwIGltIGxhbmcsIHQzMyAibGEiKS4gQmFuIFRIQVQgMS42LjI3LzEuNy43LzEuNy44'
'LzEuNy4xMiBkZXUgcmM9MCB2YSBkZXUgY2hvIHQzMy90MTM3L3QxNTkgUVVBIHRyZW4gMGVhOTVkZS4KICAgICMgYmFzaCBx'
'dWEgYHdoaWNoYCBDSEkgaG9pIENPIE1BVCwgY28gY2h1IGRpY2g6IHQzNS10NDAgZ29pIGBiYXNoYCBUUkFOIChiYXNoIFdT'
'TCBsYW0gY2h1bmcgRE8sIGRldSBOR09BSV9QSEFNX1ZJIOKAlCBkbyB0cmVuCiAgICAjIDIwMjYtMDktMzBqKS4gOSBjYSBU'
'Uk9ORyBwaGFtIHZpIEtIT05HIGdvaSBiYXNoIHF1YSBgd2hpY2hgIOKAlCB4ZW0gY2hvdCBgX2Jhc2hfcG9zaXgoKWAgZHVv'
'aSBjaG90IGdpdC4KICAgICMgQ0hBWSBEVU9DIGNodWEgcGhhaSBEVU5HIERVT0M6IGRvIHRyZW4gMjAyNi0wOS0zMGssIDBl'
'YTk1ZGUsIGFjdGlvbmxpbnQgVEhBVCAxLjQuMy8xLjUuMC8xLjUuMy8xLjYuMC8xLjYuOC8xLjYuMTUvMS42LjIwLwogICAg'
'IyAxLjYuMjIgZGV1IGAtdmVyc2lvbmAgcmM9MCwgbWEgY2EgdGFtIGxhbSB0MTM3L3QxNTkgRE8gKGBwcm9wZXJ0eSAicnVu'
'X2F0dGVtcHQiLyJ3b3JrZmxvd19zaGEiIGlzIG5vdCBkZWZpbmVkYCksIDEuNC4zLzEuNS4wCiAgICAjIHRoZW0gdDMzIChg'
'bXVzdCBiZSBjb250YWluZWQgd2l0aGluICR7eyB9fWApIOKAlCBlMmUgMS42LjIyOiByYz0xIGBEQVQgMTEgfCBUUlVPVCAx'
'YCwgYGxhOiBbJ3QxMzcnLCAndDE1OSddYCBjaG8gdW5nIHZpZW4KICAgICMgc2FjaDsgMS42LjIzLzEuNi4yNC8xLjYuMjYv'
'MS42LjI3LzEuNy4wLzEuNy42LzEuNy43LzEuNy4xMiBRVUEgY2EgYmEuIFNhbiBsYSBiYW4KICAgICMgZ2hpbSBDSSAoQUxf'
'U0FOKSwgS0hPTkcgcGhhaSAxLjYuMjMgZG8gdHJlbiBNT1QgdW5nIHZpZW46IHdvcmtmbG93IGN1YSB1bmcgdmllbiBzYXUg'
'Y28gdGhlIGR1bmcgY3UgcGhhcCBtb2kgaG9uLCBtYSBDSSBjaGkgZG8KICAgICMgYmFuZyBiYW4gZ2hpbS4gQ3UgaG9uIHNh'
'biA9PiBLSE9ORyBETyBEVU9DIChjaGFuIGNhIDEuNi4yMy0xLjcuNiBkYW5nIFFVQTogZmFpbC1jbG9zZSwga2hvbmcgcGhh'
'aSBwaGFuIHF1eWV0KS4gYHZgIGRhdTogYmFuCiAgICAjIGBnbyBpbnN0YWxsYCBpbiBgdjEuNy43YDsga2hvbmcgZG9jIGR1'
'b2Mgc28gKHZkLiBgKGRldmVsKWApID0+IEtIT05HIERPIERVT0MuCiAgICBpZiBub3QgX3RoaWV1X2NjOgogICAgICAgIF9h'
'bCA9IHN1YnByb2Nlc3MucnVuKFtfY2NbImFjdGlvbmxpbnQiXSwgIi12ZXJzaW9uIl0sIGNhcHR1cmVfb3V0cHV0PVRydWUs'
'IHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICBlcnJvcnM9InJlcGxh'
'Y2UiLCB0aW1lb3V0PTYwKQogICAgICAgIF9hbF92ID0gcmUuc2VhcmNoKHIiKD9tKV52PyhcZCspXC4oXGQrKVwuKFxkKyki'
'LCBfYWwuc3Rkb3V0IG9yICIiKQogICAgICAgIGlmIF9hbC5yZXR1cm5jb2RlOgogICAgICAgICAgICBsb2kuYXBwZW5kKCJh'
'Y3Rpb25saW50IHRyZW4gUEFUSCBjbyBtYXQgbmh1bmcgYGFjdGlvbmxpbnQgLXZlcnNpb25gIHJjIT0wIChraG9uZyBjaGF5'
'IGR1b2MpOiBjYWkgbGFpIGJhbiBnaGltIEFMX1ZFUiIpCiAgICAgICAgZWxpZiBub3QgX2FsX3Ygb3IgdHVwbGUoaW50KHgp'
'IGZvciB4IGluIF9hbF92Lmdyb3VwcygpKSA8IEFMX1NBTjoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImFjdGlvbmxpbnQg'
'e19hbF92Lmdyb3VwKDApIGlmIF9hbF92IGVsc2UgJyhraG9uZyBkb2MgZHVvYyBwaGllbiBiYW4pJ30gY3UgaG9uIGJhbiBn'
'aGltIENJICIKICAgICAgICAgICAgICAgICAgICAgICBmInsnLicuam9pbihtYXAoc3RyLCBBTF9TQU4pKX0gKEFMX1ZFUik6'
'IGJhbiBjdSBsYW0gdDEzNy90MTU5IERPICdsYScgdHJlbiB1bmcgdmllbiBzYWNoIOKAlCIKICAgICAgICAgICAgICAgICAg'
'ICAgICAiIGNhaSBiYW4gZ2hpbSAob3BzL2NhaV9hY3Rpb25saW50LnNoIHZvaSBBTF9WRVIpIikKICAgICAgICAjIGdpdCBj'
'dW5nIHRoZTogQ08gTUFUIGtob25nIHBoYWkgRFVORyBEVU9DLCB2YSBnaXQgQ1UgbGEgY29uZyBjdSBQSE8gQklFTiBuaGF0'
'IHRyb25nIGJvbi4gRG8gdHJlbiAyMDI2LTA5LTMwbCwgMGVhOTVkZSwgZ2l0CiAgICAgICAgIyBUSEFUIHF1YSBjdW5nIGNo'
'YXkoKTogMi4yNS4xID0+IDE0MC8xNjYgKDIzIGNhICJsYSI6IGBpbml0IC1iYC4uLiksIDIuMzQuMSB2YSAyLjM1LjEgPT4g'
'MTYzLzE2NiAodDEwOSB0MTEwIHQxMTE6IGBnaXQKICAgICAgICAjIHdvcmt0cmVlIGxpc3QgLS1wb3JjZWxhaW4gLXpgIHJj'
'PTEyOSBgdW5rbm93biBzd2l0Y2ggemApLCBlMmUgMi4zNS4xIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgOyAyLjM2LjEgPT4g'
'MTY2LzE2Ni4gU2FuIGxheQogICAgICAgICMgdHUgdGluaCBuYW5nIG1hIENISU5IIG1hIGR1b2MgZG8gZ29pIChvcHMvY29u'
'Z19jdS55YW1sIGRlIGJhbl9naGltIGdpdCA9IG51bGwgbmVuIGtob25nIGNvIGJhbiBnaGltIENJIGRlIGR1YSB2YW8pLgog'
'ICAgICAgICMgYGdpdCB2ZXJzaW9uIDIuNDcuMS53aW5kb3dzLjFgIChHaXQgZm9yIFdpbmRvd3MpIHZhIGAyLjM5LjMgKEFw'
'cGxlIEdpdC0xNDYpYCBkZXUgZG9jIGR1b2MgYmEgc28gZGF1LgogICAgICAgICMgVmEgcGhhaSBob2kgRFVORyBnaXQgbWEg'
'Ym8gdGVzdCBTRSBHT0kuIEJvIHRlc3QgS0hPTkcgYHNodXRpbC53aGljaCgiZ2l0IilgIG5odSBiYSBjb25nIGN1IHRyZW46'
'IEdPSV9HSVQgY3VhIHVuZyB2aWVuIHZhIG1vaQogICAgICAgICMgZml4dHVyZSBnb2kgYGdpdGAgVFJBTiDigJQgdHJlbiBX'
'aW5kb3dzIGxhIENyZWF0ZVByb2Nlc3NXOiBDSEkgdHUgdGhlbSBgLmV4ZWAgKEtIT05HIFBBVEhFWFQpLCB0cmEgdGh1IG11'
'YyBweXRob24uZXhlLCBjd2QKICAgICAgICAjIHZhIFN5c3RlbTMyIFRSVU9DIFBBVEguIGB3aGljaGAgdGhpIHRyYSBQQVRI'
'RVhULCBuZW4gbW90IGBnaXQuY21kYC9gZ2l0LmJhdGAgZHVuZyB0cnVvYyBgZ2l0LmV4ZWAgQ1UgdHJlbiBQQVRIIGR1b2Mg'
'aG9pCiAgICAgICAgIyBUSEFZIG5vIOKAlCBkbyB0cmVuIDIwMjYtMTAtMDEgKG5oYW5oIHdpbjMyIFRIQVQgY3VhIHNodXRp'
'bC53aGljaDsgc2hpbSBgZ2l0LkNNRGAgbW9pIHRydW9jIGdpdCAyLjM1LjEgVEhBVCk6IGJhbiAzMG0gbXVjIDAKICAgICAg'
'ICAjIGltLCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0MTA5JywgJ3QxMTAnLCAndDExMSddYC4gTmVu'
'IGhvaSBiYW5nIENISU5IIGR1b25nIGF5OiB0aWVuIHRyaW5oIGNvbiBjdWEgY2hheSgpCiAgICAgICAgIyAoY3VuZyBweXRo'
'b24sIGN1bmcgbW9pIHRydW9uZywgY3dkID0gZ29jIG5odSBibyB0ZXN0KSBnb2kgYGdpdCAtLXZlcnNpb25gIFRSQU4uCiAg'
'ICAgICAgX3JjX2d2LCBfcmFfZ3YgPSBjaGF5KFsiLWMiLCAiaW1wb3J0IHN1YnByb2Nlc3MsIHN5czsgcCA9IHN1YnByb2Nl'
'c3MucnVuKFsnZ2l0JywgJy0tdmVyc2lvbiddLCBjYXB0dXJlX291dHB1dD1UcnVlLCIKICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICIgdGV4dD1UcnVlLCB0aW1lb3V0PTYwKTsgcHJpbnQocC5zdGRvdXQpOyBzeXMuZXhpdChwLnJl'
'dHVybmNvZGUpIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGdvYyBpZiBnb2MuaXNfZGlyKCkgZWxzZSBQYXRo'
'LmN3ZCgpLCBwaHV0PTIpCiAgICAgICAgX2d2X20gPSByZS5zZWFyY2gociIoP20pXmdpdCB2ZXJzaW9uXHMrKFxkKylcLihc'
'ZCspXC4oXGQrKSIsIF9yYV9ndikKICAgICAgICBnaGkoImdpdF9ib190ZXN0IiwgX2d2X20uZ3JvdXAoMCkgaWYgX2d2X20g'
'ZWxzZSBOb25lKQogICAgICAgIGlubigiICBnaXQgYm8gdGVzdCAgOiIsIF9ndl9tLmdyb3VwKDApIGlmIF9ndl9tIGVsc2Ug'
'ZiIoa2hvbmcgZG9jIGR1b2MgcGhpZW4gYmFuLCByYz17X3JjX2d2fSkiKQogICAgICAgIGlmIF9yY19ndjoKICAgICAgICAg'
'ICAgbG9pLmFwcGVuZChmImBnaXQgLS12ZXJzaW9uYCBnb2kgVFJBTiBuaHUgYm8gdGVzdCByYyE9MCAoeyhfcmFfZ3Yuc3Ry'
'aXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFdWzo5MF19KTogY2FpIGxhaSBnaXQiKQogICAgICAgIGVsaWYgbm90IF9n'
'dl9tIG9yIHR1cGxlKGludCh4KSBmb3IgeCBpbiBfZ3ZfbS5ncm91cHMoKSkgPCBHSVRfU0FOOgogICAgICAgICAgICBsb2ku'
'YXBwZW5kKGYiZ2l0IHsnLicuam9pbihfZ3ZfbS5ncm91cHMoKSkgaWYgX2d2X20gZWxzZSAnKGtob25nIGRvYyBkdW9jIHBo'
'aWVuIGJhbiknfSBjdSBob24gIgogICAgICAgICAgICAgICAgICAgICAgIGYieycuJy5qb2luKG1hcChzdHIsIEdJVF9TQU4p'
'KX0gKHVuZyB2aWVuIGdvaSBgZ2l0IHdvcmt0cmVlIGxpc3QgLS1wb3JjZWxhaW4gLXpgKTogY2FwIG5oYXQgZ2l0IikKICAg'
'ICAgICAjIGJhc2ggY3VuZyBIT0kgU0FJIENITyBuaHUgZ2l0OiA5IGNhIFRST05HIHBoYW0gdmkgKHQzMiB0NTEgdDU5IHQ2'
'MCB0NjIgdDYzIHQ2NiB0NjggdDE1MikgY2hheSBiYXNoIGJhbmcgYF9iYXNoX3Bvc2l4KClgCiAgICAgICAgIyBjdWEgdW5n'
'IHZpZW4g4oCUIEdpdCBCYXNoIG8gZHVvbmcgQ08gRElOSCBgQzpcUHJvZ3JhbSBGaWxlc1xHaXRcYmluXGJhc2guZXhlYCAo'
'dmEgYCh4ODYpYCwgYHVzclxiaW5gKSwgcm9pCiAgICAgICAgIyBgd2hpY2goImJhc2giKWAgTkhVTkcgbG9haSBrZXQgcXVh'
'IHRyb25nIFN5c3RlbTMyIChXU0wpOyBraG9uZyB0aGF5IHRoaSB0cmEgIiIuIE1heSBjbyBXU0wgbWEgR2l0IGtob25nIG8g'
'UHJvZ3JhbSBGaWxlcwogICAgICAgICMgKE1pbkdpdCBkbyBDSElOSCBwczEgdHUgdGFpIOKAlCBNaW5HaXQgS0hPTkcgY28g'
'YmFzaDsgc2Nvb3A7IGNhaSBwZXItdXNlcikgcXVhIGNob3QgYHdoaWNoYCBvIHRyZW4sIHJvaSBgX2Jhc2hfcG9zaXgoKWAK'
'ICAgICAgICAjID09ICIiOiB0MzIgIktIT05HIERPIERVT0MiICsgOCBjYSAibGEiIGBzdWJwcm9jZXNzLnJ1bihbIiIuLi5d'
'KWAsIGNoaSBsbyByYSBTQVUgY2EgaGFpIGx1b3QgYm8gdGVzdC4gRG8gdHJlbiAyMDI2LTEwLTAxOgogICAgICAgICMgaGFt'
'IFRIQVQsIG5oYW5oIG9zLm5hbWU9J250JyAoV1NMICsgTWluR2l0L3Njb29wL3Blci11c2VyKSA9PiAnJzsgYm8gdGVzdCB2'
'b2kgZ2lhIHRyaSBheSAxNTcvMTY2OyBlMmUgKHdpbjMyIGdpYSkgcmM9MwogICAgICAgICMgc2F1IDM0NyBzLCBgVFJVT1Qg'
'TW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MgIGxhOiBbJ3Q1MScsICd0NTknLCAndDYwJywgJ3Q2MicsICd0NjMnLCAn'
'dDY2JywgJ3Q2OCcsICd0MTUyJ11gLiBQaGVwCiAgICAgICAgIyBkbyAzMGogY2hheSB0cmVuIExpbnV4LCBub2kgYF9iYXNo'
'X3Bvc2l4KClgIGx1b24gdHJhICJiYXNoIiwgbmVuIGtob25nIHRoZSB0aGF5IGR1b25nIG5heS4KICAgICAgICAjIFZhIGBn'
'aXRgIFRST05HIGJhc2ggYXkgbGEgZ2l0IFRIVSBCQTogYEdpdFxiaW5cYmFzaC5leGVgIGxhIGNvbXBhdC1iYXNoIGN1YSBn'
'aXQtd3JhcHBlciwgYHNldHVwX2Vudmlyb25tZW50KClgIGRheQogICAgICAgICMgYDxnb2MgR2l0PlxtaW5ndzY0XGJpbjs8'
'Z29jIEdpdD5cdXNyXGJpbmAgbGVuIERBVSBQQVRIIChnaXQtZm9yLXdpbmRvd3MvTUlOR1ctcGFja2FnZXM6IGdpdC13cmFw'
'cGVyLmMgKyBjb21wYXQtYmFzaC5yYywKICAgICAgICAjIGtob25nIGNvIE1JTklNQUxfUEFUSCkg4oCUIHR1YyBnaXQgREkg'
'S0VNIGJhbiBHaXQgYXksIEtIT05HIHBoYWkgZ2l0IFRSQU4gZGEgaG9pIG8gdHJlbi4gdDE1MiBjaGF5IEdJVF9DT05GSUdf'
'Q09VTlQgKGdpdAogICAgICAgICMgMi4zMSkgdHJvbmcgYmFzaCBheS4gRG8gdHJlbiAyMDI2LTEwLTAxIChiYXNoIGJvYyBk'
'YXkgZ2l0IGRpIGtlbSBsZW4gZGF1IFBBVEgsIGdpdCBUUkFOIDIuNDMpOiBnaXQgZGkga2VtIDIuMzAuMiBUSEFUID0+CiAg'
'ICAgICAgIyAxNjUvMTY2LCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0MTUyJ11gIGNobyB1bmcgdmll'
'biBzYWNoOyAyLjMxLjAgVEhBVCA9PiAxNjYvMTY2LiBIb2kgQ0hJTkggaGFtIGF5IHZhCiAgICAgICAgIyBDSElOSCBiYXNo'
'IGF5IHRyb25nIHRpZW4gdHJpbmggY29uIGN1YSBjaGF5KCkgKGN1bmcgcHl0aG9uLCBjdW5nIG1vaSB0cnVvbmcsIGN3ZCA9'
'IGdvYyk7IHVuZyB2aWVuIGtob25nIGNvIGhhbSB0aGkga2hvbmcKICAgICAgICAjIGhvaSAoZ2l1IGNob3QgQ08gTUFUKS4K'
'ICAgICAgICAjIERvYyBkb25nIGBnaXQgdmVyc2lvbmAgQ1VPSSBjdWEgc3Rkb3V0LCBLSE9ORyBkb2MgZG9uZyBEQVUgKGJh'
'biAwMWI6IEJBU0hfRU5WIGBlY2hvYCBtb3QgZG9uZyA9PiBtdWMgMCBLREQgb2FuOyB0dSBiYW4gMDFlCiAgICAgICAgIyBj'
'aGF5KCkgYm8gQkFTSF9FTlYsIGNhY2ggZG9jIG5heSBnaXUgbGFpIHZpIHZvIGhhaSkuIEJhc2ggdHJlbyB0aGkgYmF0IG5n'
'b2FpIGxlIFRST05HIGNvbiAoYmFuIDAxYiBkbyBsb2kgY2hvCiAgICAgICAgIyBgX2Jhc2hfcG9zaXgoKWApIHZhIERVTkcg'
'bHVvbiAoa2hvbmcgaG9pIGxhbiBoYWk6IGdpdSB0cmFuIDYwIHMgdmEgbW90IHRpZW4gdHJpbmggbW8gY29pIG5odSBiYW4g'
'MDFjKS4KICAgICAgICAjIFZhIGhvaSBIQUkgbGFuLCBkdW5nIEhBSSBtb2kgdHJ1b25nIGJvIHRlc3QgVEhBVCBkdW5nOiAz'
'IGxvaSBnb2kgYF9iYXNoX3Bvc2l4KClgIGN1YSB1bmcgdmllbiBjaGF5IGJhc2ggdm9pIDIgbW9pIHRydW9uZyDigJQKICAg'
'ICAgICAjIHQzMi90NTEtdDY4IGBkaWN0KG9zLmVudmlyb24sIC4uLilgIChtb2kgdHJ1b25nIGN1YSBjaGF5KCkpLCBjb24g'
'dDE1MiAoY2EgRFVZIE5IQVQgY2FuIHNhbiAyLjMxKQogICAgICAgICMgYGRpY3QoUEFUSD1vcy5lbnZpcm9uWyJQQVRIIl0s'
'IFRMXyosIEdJVF9DT05GSUdfKilgLiBCYW4gMDFjIGhvaSBvIG1vaSB0cnVvbmcgVEhVIE5IQVQgcm9pIGFwIHNhbiBjdWEg'
'dDE1MiDigJQgZG8gdHJlbgogICAgICAgICMgMjAyNi0xMC0wMTogZ2l0IGRpIGtlbSAyLjMwLjIgVEhBVCArIEJBU0hfRU5W'
'IGRheSBnaXQgMi40MyBsZW4gZGF1IFBBVEggPT4gbXVjIDAgdGhheSAyLjQzLCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1Qg'
'MWAsCiAgICAgICAgIyBgbGE6IFsndDE1MiddYCBjaG8gdW5nIHZpZW4gc2FjaC4gVHUgYmFuIDAxZSBjaGF5KCkgYm8gQkFT'
'SF9FTlYgbmVuIGR1b25nIGF5IGRvbmcgbyBHT0M7IGhhaSBsYW4gaG9pIGdpdSBsYWkgdmkgaGFpIG1vaQogICAgICAgICMg'
'dHJ1b25nIFZBTiBraGFjIG5oYXUuIExhbiBob2kgbyBtb2kgdHJ1b25nIHRodSBuaGF0IENISSBjaHVuZyBtaW5oIGdpdCBD'
'SEFZIGR1b2MgdHJvbmcgYmFzaCBheSwgS0hPTkcgY2h1bmcgbWluaCBiYXNoCiAgICAgICAgIyAiZHVuZyBkdW9jIiBjaG8g'
'dDMyL3Q1MS10NjggKGRvOiBub2Nsb2JiZXIgcXVhIGNhdSBob2kgbmF5IG1hIGxhbSA3IGNhIERPIOKAlCB2aSB2YXkgY2hh'
'eSgpIGJvIGJpZW4ga2hvaSBkb25nIGJhc2gsIHhlbQogICAgICAgICMgdHJlbikuIEJBU0hfR0lUID0gbW9pIHRydW9uZyB0'
'MzIvdDUxLXQ2OCAoZG9pIENIQVkgZHVvYyk7IEJBU0hfR0lUX1QxNTIgPSBtb2kgdHJ1b25nIHQxNTIgKGRvaSBzYW4gR0lU'
'X1NBTl9CQVNIKS4KICAgICAgICBfcmNfYnAsIF9yYV9icCA9IGNoYXkoWyItYyIsICJpbXBvcnQgb3MsIHN1YnByb2Nlc3Ms'
'IHN5c1xuc3lzLnBhdGguaW5zZXJ0KDAsICdvcHMnKVxuaW1wb3J0IGxlYXNlX3B1Ymxpc2hfdGVzdCBhcyBUXG4iCiAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZiA9IGdldGF0dHIoVCwgJ19iYXNoX3Bvc2l4JywgTm9uZSlcbmIg'
'PSAnPycgaWYgZiBpcyBOb25lIGVsc2UgZigpXG5wcmludCgnQkFTSF9QT1NJWD0nICsgYilcbiIKICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICJpZiBiIGFuZCBiICE9ICc/JzpcbiAgZm9yIGsgaW4gKCdCQVNIX0dJVCcsICdCQVNI'
'X0dJVF9UMTUyJyk6XG4gICAgdHJ5OlxuIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiAgICAgIHAg'
'PSBzdWJwcm9jZXNzLnJ1bihbYiwgJy0tbm9wcm9maWxlJywgJy0tbm9yYycsICctYycsICdnaXQgLS12ZXJzaW9uJ10sIgog'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiBjYXB0dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsIHRp'
'bWVvdXQ9NjAsIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiBlbnY9Tm9uZSBpZiBrID09ICdCQVNI'
'X0dJVCcgZWxzZSB7J1BBVEgnOiBvcy5lbnZpcm9uWydQQVRIJ119KVxuIgogICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgIiAgICAgIHYgPSBbeCBmb3IgeCBpbiBwLnN0ZG91dC5zcGxpdGxpbmVzKCkgaWYgeC5zdGFydHN3aXRoKCdn'
'aXQgdmVyc2lvbicpXSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgb3IgcC5zdGRvdXQuc3RyaXAo'
'KS5zcGxpdGxpbmVzKCkgb3IgWycnXVxuIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiAgICAgIHBy'
'aW50KGsgKyAnPScgKyB2Wy0xXSArICcgcmM9JyArIHN0cihwLnJldHVybmNvZGUpKVxuIgogICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgIiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6XG4gICAgICBwcmludChrICsgJz0oJyArIHR5'
'cGUoZSkuX19uYW1lX18gKyAnKSByYz0tMScpXG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiICAg'
'ICAgYnJlYWtcbiJdLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBnb2MgaWYgZ29jLmlzX2RpcigpIGVsc2UgUGF0'
'aC5jd2QoKSwgcGh1dD0zKQogICAgICAgIF9icF9tID0gcmUuc2VhcmNoKHIiKD9tKV5CQVNIX1BPU0lYPSguKikkIiwgX3Jh'
'X2JwKQogICAgICAgIF9icCA9IF9icF9tLmdyb3VwKDEpLnN0cmlwKCkgaWYgKF9icF9tIGFuZCBub3QgX3JjX2JwKSBlbHNl'
'IE5vbmUKICAgICAgICBfYmdfbSA9IHJlLnNlYXJjaChyIig/bSleQkFTSF9HSVQ9Z2l0IHZlcnNpb25ccysoXGQrKVwuKFxk'
'KylcLihcZCspW15cbl0qXHNyYz0wJCIsIF9yYV9icCkKICAgICAgICBfYnRfbSA9IHJlLnNlYXJjaChyIig/bSleQkFTSF9H'
'SVRfVDE1Mj1naXQgdmVyc2lvblxzKyhcZCspXC4oXGQrKVwuKFxkKylbXlxuXSpcc3JjPTAkIiwgX3JhX2JwKQogICAgICAg'
'IGdoaSgiYmFzaF9ib190ZXN0IiwgX2JwKTsgZ2hpKCJnaXRfdHJvbmdfYmFzaF9ib190ZXN0IiwgX2JnX20uZ3JvdXAoMClb'
'OTpdIGlmIF9iZ19tIGVsc2UgTm9uZSkKICAgICAgICBnaGkoImdpdF90cm9uZ19iYXNoX3QxNTIiLCBfYnRfbS5ncm91cCgw'
'KVsxNDpdIGlmIF9idF9tIGVsc2UgTm9uZSkKICAgICAgICBpbm4oIiAgYmFzaCBibyB0ZXN0IDoiLCByZXByKF9icCkgaWYg'
'X2JwIGlzIG5vdCBOb25lIGVsc2UgZiIoa2hvbmcgaG9pIGR1b2MsIHJjPXtfcmNfYnB9KSIsCiAgICAgICAgICAgICJ8IGdp'
'dCB0cm9uZyBiYXNoOiIsIF9iZ19tLmdyb3VwKDApWzk6XSBpZiBfYmdfbSBlbHNlICIoa2hvbmcgZG9jIGR1b2MpIiwKICAg'
'ICAgICAgICAgInwgbW9pIHRydW9uZyB0MTUyOiIsIF9idF9tLmdyb3VwKDApWzE0Ol0gaWYgX2J0X20gZWxzZSAiKGtob25n'
'IGRvYyBkdW9jKSIpCiAgICAgICAgaWYgX2JwIGlzIE5vbmU6CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJraG9uZyBob2kg'
'ZHVvYyBgX2Jhc2hfcG9zaXgoKWAgY3VhIGJvIHRlc3QgKHJjPXtfcmNfYnB9OiIKICAgICAgICAgICAgICAgICAgICAgICBm'
'IiB7KF9yYV9icC5zdHJpcCgpLnNwbGl0bGluZXMoKSBvciBbJyddKVstMV1bOjkwXX0pIikKICAgICAgICBlbGlmIG5vdCBf'
'YnA6CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJgX2Jhc2hfcG9zaXgoKWAgY3VhIGJvIHRlc3QgS0hPTkcgdGhheSBiYXNo'
'IFBPU0lYIChgd2hpY2hgOiB7X2NjWydiYXNoJ119OyBTeXN0ZW0zMiA9IFdTTCBiaSBsb2FpKToiCiAgICAgICAgICAgICAg'
'ICAgICAgICAgIiBjYWkgR2l0IGZvciBXaW5kb3dzIHZhbyBDOlxcUHJvZ3JhbSBGaWxlc1xcR2l0LCBob2FjIGRhdCB0aHUg'
'bXVjIEdpdFxcYmluIGxlbiBEQVUgUEFUSCAodHJ1b2MgU3lzdGVtMzIpIikKICAgICAgICBlbGlmIF9icCAhPSAiPyIgYW5k'
'IG5vdCAoX2JnX20gYW5kIF9idF9tKToKICAgICAgICAgICAgX2RvbmdfYmcgPSBbeFs6OTBdIGZvciB4IGluIHJlLmZpbmRh'
'bGwociIoP20pXihCQVNIX0dJVCg/Ol9UMTUyKT89LiopJCIsIF9yYV9icCldIG9yIFsiKGtob25nIGNvIGRvbmcgQkFTSF9H'
'SVQpIl0KICAgICAgICAgICAgbG9pLmFwcGVuZChmImBnaXQgLS12ZXJzaW9uYCBUUk9ORyBiYXNoIGN1YSBibyB0ZXN0ICh7'
'X2JwfSkga2hvbmcgY2hheS9raG9uZyBkb2MgZHVvYyBwaGllbiBiYW46IHsnIHwgJy5qb2luKF9kb25nX2JnKX0iKQogICAg'
'ICAgIGVsaWYgX2JwICE9ICI/IiBhbmQgdHVwbGUoaW50KHgpIGZvciB4IGluIF9idF9tLmdyb3VwcygpKSA8IEdJVF9TQU5f'
'QkFTSDoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImdpdCB7Jy4nLmpvaW4oX2J0X20uZ3JvdXBzKCkpfSBUUk9ORyBiYXNo'
'IGN1YSBibyB0ZXN0ICh7X2JwfTsgbW9pIHRydW9uZyB0MTUyOiBjaGkgUEFUSCwga2hvbmcgQkFTSF9FTlYpIGN1IgogICAg'
'ICAgICAgICAgICAgICAgICAgIGYiIGhvbiB7Jy4nLmpvaW4obWFwKHN0ciwgR0lUX1NBTl9CQVNIKSl9ICh0MTUyIGR1bmcg'
'R0lUX0NPTkZJR19DT1VOVCk6IGNhcCBuaGF0IGJhbiBHaXQgY2h1YSBiYXNoIGF5IikKCnJjLCBoZWFkLCBfID0gZ2l0KGdv'
'YywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxvaS5hcHBlbmQoImtob25nIGRvYyBkdW9jIEhFQUQiKQpnaGkoImhl'
'YWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAiLS1pcy1hbmNlc3RvciIsIFNIQV9HMSwg'
'aGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNfYSA9PSAwKQppZiBoZWFkID09IFNIQV9HMToKICAgIHRoZV9oZSA9'
'ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gREFZIExBIGcxLiBDSFVBIGNvIGJhbiB2YSBnMjsga2V0IHF1'
'YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9kdWU6CiAgICB0aGVfaGUgPSAiZzIiOyBpbm4oZiIgIEhFQUQgPSB7'
'aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hBX0cxWzo4XX0pOyB1bmcgdmllbiBnMiBoYXkga2hvbmc6IE43JyAo'
'bXVjIDEpIGRpbmggZGFuaC4iKQplbHNlOgogICAgdGhlX2hlID0gIj8iOyBsb2kuYXBwZW5kKGYiSEVBRD17aGVhZFs6OF19'
'IEtIT05HIHBoYWkgZzEgdmEgS0hPTkcgcGhhaSBoYXUgZHVlIGN1YSB7U0hBX0cxWzo4XX0g4oCUIHJlYmFzZT8gbmhhbSBu'
'aGFuaD8iKQpnaGkoInRoZV9oZSIsIHRoZV9oZSkKcmNfciwgcmVmcywgXyA9IGdpdChnb2MsICJmb3ItZWFjaC1yZWYiLCAi'
'LS1wb2ludHMtYXQiLCBoZWFkIG9yICJIRUFEIiwKICAgICAgICAgICAgICAgICAgICAiLS1mb3JtYXQ9JShyZWZuYW1lOnNo'
'b3J0KSIpCmRzciA9IFt4IGZvciB4IGluIHJlZnMuc3BsaXRsaW5lcygpIGlmIHguc3RyaXAoKSBhbmQgeC5zdHJpcCgpICE9'
'ICJkby10YW0iXQpnaGkoInJlZl90cm9fdG9pX2hlYWQiLCBkc3IpCmlubihmIiAgcmVmIHRybyB0b2kgSEVBRDogeycsICcu'
'am9pbihkc3IpIGlmIGRzciBlbHNlICcoa2hvbmcgcmVmIG5hbyAtIEhFQUQgcm9pIHR1IGRvKSd9IikKCmlmIGxvaToKICAg'
'IGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogbmVuIGRvIHNhaSwgS0hPTkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBm'
'b3IgeCBpbiBsb2k6IGlubigiICAtIiwgeCkKICAgIHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMS4ga2ljaCB0'
'aHVvYyAoTjcnIGN1YSBzcGVjIHIzKSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMS4g'
'S0lDSCBUSFVPQyDigJQgdHJhbiBzcGVjIHIzOiA8PSAyIHRlcCB2YSA8PSA0MDAgZG9uZyB0aGVtIikKIyBWRSBORU4gUEhB'
'SSBUVU9JIOKAlCB2YSBwaGFpIENIVU5HIE1JTkggZHVvYyBsYSB0dW9pLCBraG9uZyBwaGFpIGdpYSBkaW5oLgojIEJhaSBo'
'b2MgdHJhIGdpYSAxOS0wOS0yMDI2OiBjbG9uZSB0YWkgZHVuZyBjaGkgZmV0Y2ggbmhhbmggYmFuIHZhLCBgb3JpZ2luL21h'
'c3RlcmAKIyBkdW5nIHllbiB0dSAxNC0wOSAoYzE2YmQzMiwgc2F1IDk3IGNvbW1pdCkuIG1lcmdlLWJhc2Ugcm9pIHZlIGR1'
'bmcgZGluaCBtYXN0ZXIgY3UsCiMgbmVuIGRpZmYgTlVPVCBjYSA5NyBjb21taXQgbWFzdGVyOiBkbyByYSA0NiB0ZXAgLyAr'
'NzExOCB0aGF5IHZpIDIgdGVwIC8gKzM5NyDigJQKIyBDVU5HIE1PVCBDT01NSVQgMGVhOTVkZS4gTW90IHRpZXUgY2hpIERF'
'TFRBIG1hIHZlIG5lbiBraG9uZyB0dW9pIHRoaSBraG9uZyBzYWkKIyBsZWNoIG1vdCBjaHV0LCBubyBzYWkgY2EgbW90IGJh'
'YyBkbyBsb24uCiMgQ2hvIG5lbjogbmVuIGtob25nIGNodW5nIG1pbmggZHVvYyBsYSB0dW9pID0+IEtIT05HIERPIERVT0Mg'
'KHJjPTMpLCBLSE9ORyBwaGFpIFRSVU9ULgojIFRSVU9UIGxhIG1vdCBQSEFOIFFVWUVUIHZlIGJhbiB2YTsgcGhhbiBxdXll'
'dCBjaGkgZHVvYyBwaGVwIHBoYXQgcmEga2hpIGRhIGRvIGR1b2MuCmVyID0gIiIKcmNfdSwgdXJsX3RobywgXyA9IGdpdChn'
'b2MsICJyZW1vdGUiLCAiZ2V0LXVybCIsICJvcmlnaW4iKQp1cmxfbywgdXJsX2luID0gX3VybF9zYWNoKHVybF90aG8pLCBf'
'dXJsX2luKHVybF90aG8pCmdoaSgib3JpZ2luX3VybCIsIHVybF9pbik7IGlubihmIiAgb3JpZ2luICAgICAgIDoge3VybF9p'
'biBvciAnKGtob25nIGRvYyBkdW9jKSd9IikKdXJsX29rID0gKG5vdCByY191KSBhbmQgdXJsX28ucnN0cmlwKCIvIikgaW4g'
'VVJMX0tIT19IT1BfTEUKcmNfbHIsIG91dF9sciwgZXJfbHIgPSBnaXQoZ29jLCAibHMtcmVtb3RlIiwgIm9yaWdpbiIsICJy'
'ZWZzL2hlYWRzL21hc3RlciIpIGlmIHVybF9vayBlbHNlICgxLCAiIiwgIiIpCmVyX2xyID0gX2FuX3VzZXJpbmZvKGVyX2xy'
'KQpyY19sbSwgbG0sIGVyX2xtICAgICA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAib3JpZ2luL21hc3RlciIpCnJtID0gb3V0'
'X2xyLnNwbGl0KClbMF0gaWYgKG5vdCByY19sciBhbmQgb3V0X2xyLnN0cmlwKCkpIGVsc2UgIiIKaWYgbm90IHVybF9vazoK'
'ICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYib3JpZ2luPXt1cmxfaW4hcn0gS0hPTkcgcGhhaSBraG8gdGhhdCDi'
'gJQgJ3R1b2knIHNvIHZvaSBubyBraG9uZyBjaHVuZyBtaW5oIGR1b2MgZ2kiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAx'
'LCAiIiwgIiIsIDEKZWxpZiBub3Qgcm06CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAogICAgICAgIGYia2hvbmcg'
'aG9pIGR1b2MgbWFzdGVyIHRyZW4gcmVtb3RlIChscy1yZW1vdGUgcmM9e3JjX2xyfSk6IHtlcl9scls6NjBdfSAiCiAgICAg'
'ICAgZiLigJQga2hvbmcgY2h1bmcgbWluaCBkdW9jIHZlIG5lbiBjb24gdHVvaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9'
'IDEsICIiLCAiIiwgMQplbGlmIHJjX2xtIG9yIG5vdCBsbToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hv'
'bmcgZG9jIGR1b2Mgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZToge2VyX2xtWzo2MF19IikKICAgIHJjX21iLCBtYiwgbnMs'
'IHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbG0gIT0gcm06CiAgICAjIERlbSB4ZW0gdHV0IGxhaSBiYW8geGEsIG5ldSBkZW0g'
'ZHVvYyDigJQgY29uIHNvIG5heSBub2kgcm8gbXVjIGRvIHNhaSBsZWNoLgogICAgcmNfYywgc2F1LCBfID0gZ2l0KGdvYywg'
'InJldi1saXN0IiwgIi0tY291bnQiLCBmIntsbX0uLntybX0iKQogICAgeGEgPSBmIiwgdHV0IGxhaSB7c2F1fSBjb21taXQi'
'IGlmIChub3QgcmNfYyBhbmQgc2F1LnN0cmlwKCkuaXNkaWdpdCgpKSBlbHNlICIiCiAgICBpbm4oZiIgIG9yaWdpbi9tYXN0'
'ZXIgdHJvbmcgY2xvbmUgOiB7bG1bOjEyXX0iKQogICAgaW5uKGYiICBtYXN0ZXIgdHJlbiByZW1vdGUgICAgICAgIDoge3Jt'
'WzoxMl19e3hhfSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICBr'
'ZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAogICAgICAgIGYidmUgbmVuIENVOiBvcmlnaW4vbWFzdGVyPXtsbVs6MTJdfSAh'
'PSByZW1vdGU9e3JtWzoxMl19e3hhfSAiCiAgICAgICAgZiLigJQgY2hheSBgZ2l0IC1DIDxraG8+IGZldGNoIG9yaWdpbiBt'
'YXN0ZXJgIHJvaSBkbyBsYWkiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxzZToKICAgIGlubihm'
'IiAgdmUgbmVuIFRVT0k6IG9yaWdpbi9tYXN0ZXIgPSB7bG1bOjEyXX0gPT0gbWFzdGVyIHRyZW4gcmVtb3RlIikKICAgIGdo'
'aSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIHJjX21iLCBtYiwgZXJfbWIgPSBn'
'aXQoZ29jLCAibWVyZ2UtYmFzZSIsICJvcmlnaW4vbWFzdGVyIiwgaGVhZCkKaWYgcmNfbWIgb3Igbm90IG1iOgogICAgaWYg'
'bWIgPT0gIiIgYW5kIHJtIGFuZCBsbSA9PSBybToKICAgICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25n'
'IHRpbmggZHVvYyBtZXJnZS1iYXNlIHZvaSBvcmlnaW4vbWFzdGVyOiB7ZXJfbWJbOjcwXX0iKQogICAgbnMsIHJjID0gIiIs'
'IDEKZWxzZToKICAgIGdoaSgibWVyZ2VfYmFzZSIsIG1iKQogICAgaW5uKGYiICBtZXJnZS1iYXNlKG9yaWdpbi9tYXN0ZXIs'
'IEhFQUQpID0ge21iWzoxMl19IikKICAgIGlmIG1iICE9IFNIQV9CQVNFX1NQRUM6CiAgICAgICAgaW5uKGYiICBMVVUgWTog'
'a2hhYyBiYXNlIG1hIHNwZWMgcjMga2hhaSAoe1NIQV9CQVNFX1NQRUNbOjEyXX0pIOKAlCB2aSBuaGFuaCBkYSBtZXJnZSBt'
'YXN0ZXIuIikKICAgICAgICBpbm4oIiAgICAgICAgIERvIHNvIGJhc2UgY3Ugc2UgTlVPVCBwaGFuIG1hc3RlciBtYW5nIHZh'
'by4gRHVuZyBtZXJnZS1iYXNlIG1vaSBsYSB2aWVjIGN1YSBleGVjdXRvci4iKQogICAgICAgIHJjX3gsIG5zX3gsIF8gPSBn'
'aXQoZ29jLCAiZGlmZi10cmVlIiwgIi1yIiwgIi1NIiwgIi0tZGlmZi1hbGdvcml0aG09bXllcnMiLCAiLS1udW1zdGF0Iiwg'
'U0hBX0JBU0VfU1BFQywgaGVhZCkKICAgICAgICBpZiBub3QgcmNfeDoKICAgICAgICAgICAgaCA9IFtsLnNwbGl0KCJcdCIp'
'IGZvciBsIGluIG5zX3guc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgICAgICAgICAgYSA9IHN1bShpbnQoeFswXSkg'
'Zm9yIHggaW4gaCBpZiB4WzBdLmlzZGlnaXQoKSkKICAgICAgICAgICAgZ2hpKCJudW1zdGF0X3RoZW9fYmFzZV9zcGVjIiwg'
'eyJ0ZXAiOiBsZW4oaCksICJ0aGVtIjogYX0pCiAgICAgICAgICAgIGlubihmIiAgICAgICAgIChkb2kgY2hpZXU6IHNvIGJh'
'c2Ugc3BlYyA9IHtsZW4oaCl9IHRlcCAvICt7YX0g4oCUIGNvbiBzbyBheSBLSE9ORyBkdW5nIGRlIGNoYW0pIikKICAgICMg'
'UExVTUJJTkcsIGtob25nIFBPUkNFTEFJTjogYGdpdCBkaWZmYCBkb2MgY2F1IGhpbmggVUkgQ1VBIE5HVU9JIERPIChkaWZm'
'LmFsZ29yaXRobSwgZGlmZi5yZW5hbWVzLCBkaWZmLm9yZGVyRmlsZSwKICAgICMgY29sb3IuZGlmZiksIHZhIGdpYSB0cmkg'
'SE9QIExFIGRvaSBsdW9uIFNPIGRvbmcgbWEgdmFuIHJhIGNodSBzbyDigJQgZG8gdHJlbiAyMDI2LTA5LTMwaTogdW5nIHZp'
'ZW4gdG9uZyBob3AgKG15ZXJzICs0MDEpID0+CiAgICAjIGJhbiAzMGkgREFUIDIgdGVwIC8gKzQwMCBkdW9pIGBkaWZmLmFs'
'Z29yaXRobSA9IGhpc3RvZ3JhbWAgaG9hYyBgcGF0aWVuY2VgLCBUUlVPVCArNDAxIGtoaSBtYWMgZGluaDsgMTAvNzUgY29t'
'bWl0IGNoYW0KICAgICMgd3JpdGUgc2V0IGNvIHNvIGRvbmcgZG9pIHRoZW8gdGh1YXQgdG9hbi4gYGRpZmYtdHJlZSAtciAt'
'TWAgPSBtYWMgZGluaCBjdWEgYGdpdCBkaWZmYCAocmVuYW1lcyBiYXQpIHZhIEtIT05HIGRvYyBjYWMga2hvYQogICAgIyBh'
'eS4gVGh1YXQgdG9hbiBwaGFpIFRVT05HIE1JTkg6IGRpZmYuPGRyaXZlcj4uYWxnb3JpdGhtIChxdWEgY29yZS5hdHRyaWJ1'
'dGVzRmlsZSBjdWEgbmd1b2kgZG8pIFZBTiBsb3QgdmFvIHBsdW1iaW5nIOKAlAogICAgIyBkbyB0cmVuIDIwMjYtMDktMzBp'
'LCBgKi5weSBkaWZmPWFsZ2AgKyBkaWZmLmFsZy5hbGdvcml0aG09aGlzdG9ncmFtOiBkaWZmLXRyZWUgKzQwMSBjaG8gdW5n'
'IHZpZW4gbXllcnMgKzQwMDsgY28gdHVvbmcgbWluaAogICAgIyB0aGFuZyBraG9hIGF5LiBhdHRyaWJ1dGVzIGAtZGlmZmAv'
'Y29yZS5iaWdGaWxlVGhyZXNob2xkIHZhbiBhcCA9PiBgLWAgPT4gS0hPTkcgRE8gRFVPQyAoY2hvdCBkdW9pKS4KICAgIHJj'
'LCBucywgZXIgPSBnaXQoZ29jLCAiZGlmZi10cmVlIiwgIi1yIiwgIi1NIiwgIi0tZGlmZi1hbGdvcml0aG09bXllcnMiLCAi'
'LS1udW1zdGF0IiwgbWIsIGhlYWQpCmlmIHJjOgogICAgcGFzcwplbHNlOgogICAgaGFuZyA9IFtsLnNwbGl0KCJcdCIpIGZv'
'ciBsIGluIG5zLnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICB0aGVtID0gc3VtKGludChoWzBdKSBmb3IgaCBpbiBo'
'YW5nIGlmIGhbMF0uaXNkaWdpdCgpKQogICAgeG9hICA9IHN1bShpbnQoaFsxXSkgZm9yIGggaW4gaGFuZyBpZiBoWzFdLmlz'
'ZGlnaXQoKSkKICAgIGdoaSgic29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hpKCJkb25nX3RoZW0iLCB0aGVtKTsgZ2hpKCJkb25n'
'X3hvYSIsIHhvYSkKICAgIGZvciBoIGluIGhhbmc6IGlubihmIiAgICB7aFsyXTozNH0gK3toWzBdOjw1fSAte2hbMV19IikK'
'ICAgIGlubihmIiAgICBUT05HOiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17eG9hfSAgICh0cmFuOiB7VFJBTl9URVB9'
'IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcgdGhlbSkiKQogICAgY2hhbSA9IHNvcnRlZCh7aFsyXSBmb3IgaCBpbiBoYW5nfSAm'
'IFdSSVRFX1NFVF9HMik7IGdoaSgiY2hhbV93cml0ZV9zZXQiLCBjaGFtKQogICAgZGVmIF9jYV9tb2lfY28ocmV2KToKICAg'
'ICAgICAjIGNhdC1maWxlLCBraG9uZyBgc2hvd2A6IGBnaXQgc2hvd2AgY2hldCB2b2kgY2F1IGhpbmggVUkgZ28gc2FpIChk'
'byB0cmVuIDIwMjYtMDktMzBpOiBsb2cuZGF0ZSBnbyBzYWkgPT4gYmFuIDMwaSBnb2kKICAgICAgICAjIDBlYTk1ZGUgbGEg'
'Imtob25nIHBoYWkgdW5nIHZpZW4gLi4uIE5vbmUg4oCUIGRhIGxhbmQ/IG5oYW0gbmhhbmg/IikuCiAgICAgICAgcl8sIG5k'
'XywgXyA9IGdpdChnb2MsICJjYXQtZmlsZSIsICItcCIsIGYie3Jldn06b3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAg'
'ICAgICAgcmV0dXJuIE5vbmUgaWYgcl8gZWxzZSB7dCBmb3IgdCBpbiBDQV9NT0lfRzIgaWYgcmUuc2VhcmNoKHIiKD9tKV5k'
'ZWYgIiArIHQgKyByIlthLXpdP18iLCBuZF8pfQogICAgb19tYiwgb19oID0gX2NhX21vaV9jbyhtYiksIF9jYV9tb2lfY28o'
'aGVhZCkKICAgIG1hbmcgPSBzb3J0ZWQob19oIC0gb19tYiwga2V5PXNvX2NhKSBpZiAob19tYiBpcyBub3QgTm9uZSBhbmQg'
'b19oIGlzIG5vdCBOb25lKSBlbHNlIE5vbmUKICAgIGdoaSgiY2FfbW9pX2cyX21hbmdfdmFvIiwgbWFuZykKICAgIGlmIG5v'
'dCBtYW5nOgogICAgICAgICMgRG8gUk9ORyAoZGEgbGFuZCwgY2hpbmggbWFzdGVyKSwgbmhhbSBuaGFuaCwgaGF5IG5oYW5o'
'IGN1YSBwYWNrZXQgS0hBQyBjaGFtIGN1bmcgdGVwOgogICAgICAgICMga2hvbmcgbWFuZyBjYSBtb2kgbmFvIGN1YSBnMiB0'
'aGkga2hvbmcgcGhhaSB1bmcgdmllbi4gRG9jIGtob25nIGR1b2MgKE5vbmUpIGN1bmcgdmF5LgogICAgICAgIGtldCgiTjcn'
'IGtpY2ggdGh1b2MiLCBLREQsIGYiZG9pIHR1b25nIGtob25nIHBoYWkgdW5nIHZpZW46IHtsZW4oaGFuZyl9IHRlcCwgY2hh'
'bSB7Y2hhbX0sIGNhIG1vaSAiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJnMiBtYW5nIHZhbyB7bWFu'
'ZyFyfSDigJQgZGEgbGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/IikKICAgIGVsc2U6CiAgICAgICAgIyBudW1zdGF0'
'IGluIGAtYCAoa2hvbmcgY28gc28gZG9uZykgY2hvIHRlcCBiaW5hcnkvLWRpZmYgdGhlbyBhdHRyaWJ1dGVzIOKAlCBrZSBj'
'YSBhdHRyaWJ1dGVzIENVQSBOR1VPSSBETyAoZG8gdHJlbgogICAgICAgICMgMjAyNi0wOS0zMGc6IGNvcmUuYXR0cmlidXRl'
'c0ZpbGUgYCoucHkgLWRpZmZgID0+ICIyIHRlcCAvICswIiBEQVQgY2hvIDBlYTk1ZGUsIHRoYXQgKzM5NykuIGAtYCBsYSBL'
'SE9ORyBETyBEVU9DLAogICAgICAgICMga2hvbmcgcGhhaSAwOyBUUlVPVCB0aGVvIHNvIHRlcCAvIHNvIGRvbmcgREEgZGVt'
'IGR1b2MgdmFuIGdpdSAocXVhbiBzYXQgdHJ1YyB0aWVwKS4KICAgICAgICBraG9uZ19zbyA9IFtoWzJdIGZvciBoIGluIGhh'
'bmcgaWYgbm90IChoWzBdLmlzZGlnaXQoKSBhbmQgaFsxXS5pc2RpZ2l0KCkpXTsgZ2hpKCJ0ZXBfa2hvbmdfc29fZG9uZyIs'
'IGtob25nX3NvKQogICAgICAgIHZ1b3QgPSBsZW4oaGFuZykgPiBUUkFOX1RFUCBvciB0aGVtID4gVFJBTl9ET05HCiAgICAg'
'ICAga2V0KCJONycga2ljaCB0aHVvYyIsIFRSVU9UIGlmIHZ1b3QgZWxzZSAoS0REIGlmIGtob25nX3NvIGVsc2UgREFUKSwK'
'ICAgICAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IiArIChmIiDigJQgbnVtc3RhdCBLSE9ORyBjbyBzbyBk'
'b25nIGNobyB7a2hvbmdfc299IiBpZiBraG9uZ19zbyBlbHNlICIiKSkKCiMgQ29uZyBraWNoIHRodW9jIFBIQUkgZGUgbGFp'
'IE1PVCBrZXQgcXVhLiBMZW5oIG51bXN0YXQgaG9uZyB0aGkgbmhhbmggYGlmIHJjOiBwYXNzYCBraG9uZyBnaGkgZ2ksIHZh'
'IHZhbmcgbWF0IG8gZGF5CiMgdGhhbmggREFUIG8gYm8gZ29wOiBjYXUgaGluaCBkaWZmIENVQSBOR1VPSSBETyBob25nIChk'
'aWZmLm9yZGVyRmlsZSB0cm8gdGVwIGtob25nIGNvLCBkaWZmLmFsZ29yaXRobSBnbyBzYWkgPT4gcmM9MTI4KSBjaG8KIyAt'
'LWNoaS1raWNoLXRodW9jIHJjPTAgdm9pIDAgY2hvdCwgbHVvdCBkYXkgZHUgIkRBVCAxMSIgcmM9MCAoZG8gdHJlbiAyMDI2'
'LTA5LTMwaCwgMGVhOTVkZSkuIFZhbmcgbWF0IGxhIEtIT05HIERPIERVT0MuCiMgVHUgMzBqIG51bXN0YXQgbGEgZGlmZi10'
'cmVlIChraG9uZyBkb2MgaGFpIGtob2EgYXkpOyBkdW9uZyBjb24gbGFpIGRvIGR1b2M6IGRpZmYucmVuYW1lTGltaXQgZ28g'
'c2FpID0+IHJjPTEyOC4KaWYgbm90IGFueShjWzBdID09ICJONycga2ljaCB0aHVvYyIgZm9yIGMgaW4gY2hvdCk6CiAgICBr'
'ZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImNvbmcgS0hPTkcgcmEga2V0IHF1YSAoZ2l0IGRpZmYtdHJlZSAtLW51bXN0'
'YXQgcmM9e3JjfSk6IHtfYW5fdXNlcmluZm8oZXIpWzo3MF19IikKCiMgRGluaCBkYW5oIFRIQVQgbmFtIG8gTjcnIChjYSBt'
'b2kgZzIgbWFuZyB2YW8pLCBLSE9ORyBvICJoYXUgZHVlIGcxIjogZzEgZGEgbGFuZCBuZW4gbW9pIG5oYW5oIGRldQojIGxh'
'IGhhdSBkdWUuIERvbmcgZGF1IGtob2kgZGFuIHBoYWkgdHUga2hhaSB0aGVvIGtldCBxdWEgYXkgKGRvIGR1b2M6IG1hc3Rl'
'ciA0NDYyMGU4IG1vIGtob2kgYmFuZwojICJUSEUgSEUgRE8gRFVPQzogZzIiLCBKU09OICJ0aGVfaGUiOiAiZzIiLCB0cm9u'
'ZyBraGkgTjcnIGRhIGtldCBsdWFuICJraG9uZyBwaGFpIHVuZyB2aWVuIikuCiMgTmhhbiBjaGkgZHVvYyBub2kgRFVORyBj'
'YWkgZG8gZHVvYzogYFtdYCBraG9uZyB0YWNoICJkYSBsYW5kIiBraG9pICJuaGFtIG5oYW5oIi8icGFja2V0IGtoYWMiIChk'
'bwojIGR1b2MgdHJlbiAyMDI2LTA5LTMwYjogdW5nIHZpZW4gMmE2Nzk2OCBEQSBMQU5EIGJpIGdvaSAiS0hPTkcgcGhhaSB1'
'bmcgdmllbiBnMiIpLgppZiB0aGVfaGUgPT0gImcyIiBhbmQgbm90IHNvLmdldCgiY2FfbW9pX2cyX21hbmdfdmFvIik6CiAg'
'ICB0aGVfaGUgPSAoIktIT05HIG1hbmcgY2EgbW9pIGcyIG5hbyAoZGEgbGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/'
'KSIgaWYgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKSA9PSBbXQogICAgICAgICAgICAgIGVsc2UgImcyPyAoQ0hVQSBk'
'aW5oIGRhbmggZHVvYyBkb2kgdHVvbmcpIikKICAgIGdoaSgidGhlX2hlIiwgdGhlX2hlKQoKIyBDb25nIG5oYW5oOiBkbyBS'
'SUVORyBraWNoIHRodW9jICh2YWkgZ2lheSkgcm9pIGR1bmcuIER1bmcga2hpIGNhbiB4YWMgbWluaCBsYWkKIyB2ZSBuZW4g'
'bWEga2hvbmcgbXVvbiB0cmEgMjAtNDUgcGh1dCBjaG8gY2EgYm8gdGVzdC4KaWYgIi0tY2hpLWtpY2gtdGh1b2MiIGluIHN5'
'cy5hcmd2OgogICAgaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQogICAgaW5uKCItLWNoaS1raWNoLXRodW9jOiBDSEkgZG8gY29u'
'ZyBraWNoIHRodW9jLiBEYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCiAgICBpbm4oIi0iICogNzgpCiAg'
'ICBmb3IgX3QsIF90dCwgX2N0IGluIGNob3Q6IGlubihmIiAge190dDoxNH0ge190fSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0'
'IGVsc2UgIiIpKQogICAgX2sgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQogICAgX3IgPSBzdW0o'
'MSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCiAgICBzeXMuZXhpdCgzIGlmIF9rIGVsc2UgKDEgaWYgX3Ig'
'ZWxzZSAwKSkKCkNISV9QUk9CRSA9ICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YgICAgIyBibyBxdWEgYm8gdGVzdCArIE43'
'OyBnaXUgMCwgMSwgMwojIC0tLS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVzdCBkYXkgZHUgLS0tLS0tLS0tLS0tLS0tLQppZiBu'
'b3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIyLiBCTyBURVNUIERBWSBEVSAoMTAtNDAg'
'cGh1dCkiKQogICAgcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBnb2MpCiAgICBn'
'aGkoInJjX3N1aXRlIiwgcmNfbikKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXRfbikKICAgIGlubigiICByYyA9IiwgcmNf'
'biwgInwiLCBtLmdyb3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQpIikKICAgIGlmIG06'
'CiAgICAgICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGkoInRyZW4iLCBpbnQobS5ncm91cCgyKSkpOyBnaGko'
'ImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKICAgIGRvX2hldCwgZ2MsIHRpbiA9IGRvY19kbyhvdXRfbikKICAgIGdo'
'aSgic29fY2FfZG8iLCBsZW4oZG9faGV0KSk7IGdoaSgibGlldF9rZV9kYXlfZHUiLCB0aW4pCiAgICBmb3IgZyBpbiBnYzog'
'aW5uKCIgICAqIiwgZykKICAgIGlubigiIik7IGlubihmIiAgPT09IHtsZW4oZG9faGV0KX0gQ0EgRE8gPT09IikKICAgIGZv'
'ciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaW5uKGYiICAge3Quc3BsaXQoJ18nKVswXTo3fSB7'
'dH0iKTsgaW5uKGYiICAgICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCiAgICBnaGkoImRvX2x5X2RvIiwge3Q6IGRvX2hl'
'dFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQogICAgIyAtLS0tIENIT1Q6IG1vaSBjYSBETyBwaGFpIEdJQUkgVEhJQ0gg'
'RFVPQyAtLS0tCiAgICAjIFRoaWV1IGNob3QgbmF5LCBibyBkbyBpbiBkYW5oIHNhY2ggZG8gcm9pIHZhbiB0aG9hdCByYz0w'
'LiBEbyBkdW5nIGxhIGxvaSBkYSB4YXkgcmE6CiAgICAjIGx1b3QgV2luZG93cyAxOS0wOSBjbyB0MTcxIERPIG1hIGJvIGRv'
'IGJhbyAiREFUIDEwIHwgVFJVT1QgMCIgdmEgcmM9MC4KICAgIGRlZiBfa2hvYSh0KTogcmV0dXJuIHQuc3BsaXQoIl8iKVsw'
'XQogICAgZG9fcGFja2V0LCBkb19sYSwgZG9fdGhpZXVfY29uZ19jdSA9IFtdLCBbXSwgW10KICAgIGZvciB0IGluIHNvcnRl'
'ZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaywgbHkgPSBfa2hvYSh0KSwgZG9faGV0W3RdCiAgICAgICAgaWYgayBp'
'biBDQV9QQUNLRVQ6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fcGFja2V0LmFwcGVuZCh0KQogICAgICAgIGVs'
'aWYgIktIw5RORyDEkE8gxJDGr+G7okMiIGluIGx5IG9yICJ0aGnhur91IGAiIGluIGx5OiAgZG9fdGhpZXVfY29uZ19jdS5h'
'cHBlbmQodCkKICAgICAgICBlbGlmIGsgaW4gTkdPQUlfUEhBTV9WSTogICAgICAgICAgICAgICAgICAgICAgICBwYXNzCiAg'
'ICAgICAgZWxzZTogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fbGEuYXBwZW5kKHQpCiAg'
'ICBnaGkoImRvX3BhY2tldCIsIGRvX3BhY2tldCk7IGdoaSgiZG9fbGEiLCBkb19sYSk7IGdoaSgiZG9fdGhpZXVfY29uZ19j'
'dSIsIGRvX3RoaWV1X2NvbmdfY3UpCiAgICBpbm4oIiIpCiAgICBpbm4oZiIgIGNhIERPIHRodW9jIENISU5IIHBhY2tldCBu'
'YXkgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF0gb3IgJ2tob25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBu'
'Z29haSBwaGFtIHZpIChyMyBraGFpKToge1tfa2hvYSh4KSBmb3IgeCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpIGlm'
'IF9raG9hKHgpIGluIE5HT0FJX1BIQU1fVkldfSIpCiAgICBpbm4oZiIgIGNhIERPIHZpIFRISUVVIENPTkcgQ1UgICAgICAg'
'OiB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9yICdraG9uZyBjbyd9IikKICAgIGlubihmIiAgY2Eg'
'RE8gTEEgKGtob25nIGdpYWkgdGhpY2ggZHVvYyk6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdIG9yICdraG9uZyBjbyd9'
'IikKICAgICMgLS0tLSBDSE9UOiBwaGVwIGRvIHBoYWkgVFJPTiB0cnVvYyBraGkgbW90IGNodSBEQVQgbmFvIGR1b2MgcGhh'
'dCAtLS0tCiAgICAjIEJhbiB0cnVvYyBjaGkgSU4gYHRpbmAvYHJjX3N1aXRlYDogYm8gdGVzdCBjaGV0IGdpdWEgdDE3MSAo'
'cmM9MTM0LCBraG9uZyBkb25nIHRvbmcpCiAgICAjIHZhbiByYSAiREFUIDEyIHwgVFJVT1QgMCIgcmM9MDsgY2EgUEFDS0VU'
'IHZhbmcgbWF0IGhheSBiaSBCTyBRVUEgY3VuZyBkdW9jIGNoYW0gbmh1CiAgICAjICJraG9uZyBkbyIuIFZhbmcgbWF0IGto'
'b25nIHBoYWkgImtob25nIGRvIiDigJQgbGEgS0hPTkcgRE8gRFVPQy4KICAgIHZhbmcgPSBbdCBmb3IgdCBpbiBzb3J0ZWQo'
'Q0FfUEFDS0VULCBrZXk9c29fY2EpIGlmIG1hdV9jYShvdXRfbiwgdCkgbm90IGluICgiUVVBIiwgIkRPIildCiAgICBseV9r'
'ZGQgPSBbXQogICAgaWYgbm90IHRpbjogbHlfa2RkLmFwcGVuZCgiZGFuaCBzYWNoIGRvIEtIT05HIGRheSBkdSIpCiAgICBp'
'ZiByY19uIG5vdCBpbiAoMCwgMSkgb3IgKHJjX24gPT0gMSkgIT0gYm9vbChkb19oZXQpOgogICAgICAgIGx5X2tkZC5hcHBl'
'bmQoZiJyYyBibyB0ZXN0PXtyY19ufSBraG9uZyBraG9wIHtsZW4oZG9faGV0KX0gY2EgRE8gZG9jIGR1b2MiKQogICAgaWYg'
'dmFuZzogbHlfa2RkLmFwcGVuZChmImNhIFBBQ0tFVCB2YW5nL2JvIHF1YToge3Zhbmd9IikKICAgIGdoaSgiY2FfcGFja2V0'
'X3ZhbmciLCB2YW5nKTsgZ2hpKCJseV9kb19jaHVhX3Ryb24iLCBseV9rZGQpCiAgICBpZiBseV9rZGQ6IGtldCgiQm8gdGVz'
'dCBjaGF5IFRST04gdmEgZG9jIERVIiwgS0RELCAiOyAiLmpvaW4obHlfa2RkKSkKICAgIGNodWFfdHJvbiA9IEtERCBpZiBs'
'eV9rZGQgZWxzZSBEQVQKICAgIGtldCgiS2hvbmcgY2EgbmFvIGN1YSBQQUNLRVQgYmkgRE8iLCBjaHVhX3Ryb24gaWYgbm90'
'IGRvX3BhY2tldCBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBmIkRPOiB7W19raG9hKHgp'
'IGZvciB4IGluIGRvX3BhY2tldF19IOKAlCBiYW4gdmEgQ0hVQSB4b25nIikKICAgIGtldCgiTW9pIGNhIERPIGRldSBnaWFp'
'IHRoaWNoIGR1b2MiLCBjaHVhX3Ryb24gaWYgbm90IGRvX2xhIGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX2xh'
'IGVsc2UgZiJsYToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV19IikKICAgIGlmIGRvX3RoaWV1X2NvbmdfY3U6CiAgICAg'
'ICAga2V0KCJDb25nIGN1IGRheSBkdSBkZSBkbyIsIEtERCwgZiJ0aGlldSBjb25nIGN1IGNobyB7W19raG9hKHgpIGZvciB4'
'IGluIGRvX3RoaWV1X2NvbmdfY3VdfSIpCgogICAgYnEgPSBzb3J0ZWQoe3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRh'
'bGwob3V0X24pfSwga2V5PXNvX2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBicSkKICAgIGlubigiIik7IGlubihmIiAgQk8gUVVB'
'ICh7bGVuKGJxKX0pOiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCiAgICBpbm4oIiIpOyBpbm4oIiAgTjEt'
'TjQgKHQxNjUtdDE2OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBuYXkgbGEgY2hpIGJhbyBob2kgcXV5OiIpCiAg'
'ICBiNCA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBTU9JfTsgZ2hpKCJjYV9tb2kiLCBiNCkKICAgIGZvciB0'
'IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCiAgICAjIEJPX1FVQS92YW5nIGxhIENIVUEgQ0hBWSwga2hv'
'bmcgcGhhaSBETzogY2hpIG1vdCBjYSBETyBtb2kgZHVvYyBwaGF0IFRSVU9ULgogICAga2V0KCJOMS1ONCAodDE2NS10MTY4'
'KSIsIERBVCBpZiBhbGwodiA9PSAiUVVBIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkKICAgICAgICBlbHNlIChUUlVPVCBpZiBh'
'bnkodiA9PSAiRE8iIGZvciB2IGluIGI0LnZhbHVlcygpKSBlbHNlIEtERCksIHN0cihiNCkpCgogICAgaW5uKCIiKTsgaW5u'
'KCIgIDE1IGNhIHR1bmcgZG8gdHJlbiBDSToiKQogICAgYjE1ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0Ex'
'NX07IGdoaSgiY2ExNSIsIGIxNSkKICAgIGlubigiICAgICIgKyAiICAiLmpvaW4oZiJ7dH06e2IxNVt0XX0iIGZvciB0IGlu'
'IENBMTUpKQoKICAgICMgdDEzNiDigJQgTjEyIGRvIEdJQU4gVElFUCBxdWEga2V0IHF1YSBjYQogICAgdDEzNl90ZW4gPSBu'
'ZXh0KCh0IGZvciB0IGluIGRvX2hldCBpZiB0LnN0YXJ0c3dpdGgoInQxMzYiKSksIE5vbmUpCiAgICBpZiBiMTUuZ2V0KCJ0'
'MTM2IikgPT0gIlFVQSI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgREFULCAidDEzNiBRVUEi'
'KQogICAgZWxpZiBiMTUuZ2V0KCJ0MTM2IikgIT0gIkRPIjoKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBj'
'YSkiLCBLREQsIGYidDEzNiA9IHtiMTUuZ2V0KCd0MTM2Jykhcn0g4oCUIGtob25nIGNoYXkva2hvbmcgdGhheSIpCiAgICBl'
'bHNlOgogICAgICAgIGx5ID0gZG9faGV0LmdldCh0MTM2X3RlbiwgIiIpCiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtl'
'dCBxdWEgY2EpIiwgVFJVT1QsIGYiRE86IHtseVs6OTBdfSIpCgojIC0tLS0tLS0tLS0tLS0tLS0gMy4gcHJvYmUgVEhBTkcg'
'dmFvIGhhbSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMy4gUFJPQkUgVEhBTkcg4oCU'
'IGdvaSBfZ2l0X3dpbmRvd3Mgdm9pIHRoYW0gc28gdGllbSIpCnNwZWMgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmls'
'ZV9sb2NhdGlvbigibHA1NDEiLCBzdHIodGVwKSkKbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMp'
'OyBzcGVjLmxvYWRlci5leGVjX21vZHVsZShscCkKc2lnID0gaW5zcGVjdC5zaWduYXR1cmUobHAuX2dpdF93aW5kb3dzKQpn'
'aGkoInRoYW1fc29fX2dpdF93aW5kb3dzIiwgbGlzdChzaWcucGFyYW1ldGVycykpCmlubigiICB0aGFtIHNvIGN1YSBfZ2l0'
'X3dpbmRvd3M6IiwgbGlzdChzaWcucGFyYW1ldGVycykpCgpkZWYgZ29pKCoqa3cpOgogICAgIiIiR29pIF9naXRfd2luZG93'
'cywgQkFUIHN0ZGVyciBkZSBtb3QgZG9uZyBjaGFuIGRvYW4ga2hvbmcgZ2lldCBsdW90IGRvLiIiIgogICAgZSA9IGlvLlN0'
'cmluZ0lPKCkKICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgciA9IGxwLl9naXRfd2lu'
'ZG93cygqKmt3KQogICAgcmV0dXJuIHIsIGUuZ2V0dmFsdWUoKQoKIyAtLS0gZG9pIGNodW5nIHJpZzogcGhhaSB0cmEgbG9p'
'IGR1bmcgbW90IGNhIHRhIEJJRVQgVFJVT0MgZGFwIGFuIC0tLQp3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgp'
'IGFzIHQ6CiAgICBuZ29haSA9IFBhdGgodCkvIm5nb2FpIjsgbmdvYWkubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBj'
'dy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgKG5nb2FpLyJnaXQuZXhlIikud3JpdGVfdGV4'
'dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMSwgXyA9IGdvaShwYXRoPXN0cihuZ29haSksIHByb2dyYW1fZmlsZXM9'
'c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAoY3cvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04'
'IikKICAgIHIyLCBfID0gZ29pKHBhdGg9c3RyKGN3KSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKcmln'
'X29rID0gYm9vbChyMSkgYW5kIHIyIGlzIE5vbmUKZ2hpKCJyaWdfZG9pX2NodW5nIiwgcmlnX29rKQprZXQoIlJJRyBkb2kg'
'Y2h1bmcgKGJpZXQgdHJ1b2MgZGFwIGFuKSIsIERBVCBpZiByaWdfb2sgZWxzZSBLREQsCiAgICBmIm5nb2FpLWN3ZC0+eydO'
'SEFOJyBpZiByMSBlbHNlICdOb25lJ30gfCB0cm9uZy1jd2QtPnsnTkhBTicgaWYgcjIgZWxzZSAnTm9uZSd9IikKaWYgbm90'
'IHJpZ19vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogcmlnIHNhaSwgbW9pIGNob3QgZHVvaSBzZSB2byBu'
'Z2hpYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tIE1PSSBDT05HIFBIQUkgVFUgQ0hVTkcgTUlOSCBOTyBDTyBUSEUgRE8gLS0t'
'CiMgQmFpIGhvYyBkYXQgbmhhdCBjdWEgcGFja2V0IG5heTogZG9fbjEwIGJhbiBjdSBjaGFtIERBVCBjaG8gOTU4MzE2ODUg'
'dHJvbmcga2hpIHQxNzEKIyBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1bmcga2h1eWV0IHRhdCBtYSBOMTAgc2luaCBy'
'YSBkZSBiYXQuIE5vIGRlZ2VuZXJhdGUg4oCUCiMgdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIG5lbiAidGFj'
'aCBkdW5nIiB2YSAidGFjaCBzYWkiIGNobyBjdW5nIGtldCBxdWEuCiMgTW90IGNvbmcga2hvbmcgdGhlIERPIHRoaSBraG9u'
'ZyBwaGFpIGNvbmcsIHZhIG5vIG5ndXkgaGllbSBob24ga2hvbmcgY28gY29uZzogbm8KIyBwaGF0IHJhIG1vdCBjaHUgREFU'
'LgojCiMgTmVuIHRydW9jIGtoaSBEVU5HIG5hbSBjb25nIG5heSBkZSBwaGFuIHF1eWV0LCBiYXQgdHVuZyBjb25nIGdpZXQg'
'bW90IGRvdCBiaWVuIGRhCiMgYmlldCB0cm9uZy4gQ29uZyBuYW8ga2hvbmcgZ2lldCBkdW9jIHRoaSBjaHUgREFUIGN1YSBu'
'byBiaSBIQSB4dW9uZyBLSE9ORyBETyBEVU9DOwojIFRSVU9UIGdpdSBuZ3V5ZW4gKHF1YW4gc2F0IHRydWMgdGllcCwgdmQu'
'IGcxIHZhbiBuaGFuIGdpdC5iYXQpLiBEb3QgYmllbiBjaGF5IHRyZW4gQkFOIFNBTyBUQU07IGNheSB0aGF0IGtob25nIGJp'
'CiMgZHVuZyB0b2kgKGN1bmcga3kgbHVhdCBuaHUgTjcpLgpET1RfQklFTl9UVV9LSUVNID0gWwogICAgKCJOOCIsICJvcHMv'
'bGVhc2VfcHVibGlzaC5weSIsCiAgICAgJ2lmIGNoaV9kaW5oIGFuZCBQYXRoKGNoaV9kaW5oKS5uYW1lLmxvd2VyKCkgPT0g'
'ImdpdC5leGUiIGFuZCBob3BfbGUoY2hpX2RpbmgpOicsCiAgICAgImlmIGNoaV9kaW5oIGFuZCBob3BfbGUoY2hpX2Rpbmgp'
'OiIpLAogICAgKCJOOSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgImQgPSBkX3Jhdy5zdHJpcCgpLnN0cmlwKCdc'
'IicpIiwgImQgPSBkX3Jhdy5zdHJpcCgpIiksCiAgICAoIk4xMCIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgInNl'
'cCA9IG9zLnBhdGhzZXAgaWYgcGhhbl9jYWNoIGlzIE5vbmUgZWxzZSBwaGFuX2NhY2giLCAic2VwID0gb3MucGF0aHNlcCIp'
'LAogICAgKCJOMTEiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAiaWYgY2hhbl9kb2FuIGlzIG5vdCBOb25lOiIsICJpZiBG'
'YWxzZToiKSwKICAgICgiTjEyIiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiLAogICAgICdnaXRfcGF0aD0iLy9raG9u'
'Zy1jby9naXQiJywgJ2dpdF9wYXRoPSIva2hvbmctY28vZ2l0IicpLApdCmlubigiIik7IGlubigiICB0dSBraWVtIGNvbmcg'
'4oCUIG1vaSBjb25nIHBoYWkgZ2lldCBkdW9jIG1vdCBkb3QgYmllbiBkYSBiaWV0OiIpCmdpZXQgPSB7fQpmb3IgbWEsIGR1'
'b25nLCB0aW0sIHRoYXkgaW4gRE9UX0JJRU5fVFVfS0lFTToKICAgIF90ZW4sIF9oYW0gPSBuZXh0KCgoYSwgYikgZm9yIGEs'
'IGIgaW4gUFJPQkUgaWYgYS5zdGFydHN3aXRoKG1hICsgIiAiKSksIChOb25lLCBOb25lKSkKICAgIGlmIF9oYW0gaXMgTm9u'
'ZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzoga2hvbmcgdGltIHRo'
'YXkgcHJvYmUgdGVuICd7bWF9IC4uLiciKTsgY29udGludWUKICAgIHRyeToKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBv'
'cmFyeURpcmVjdG9yeSgpIGFzIF90OgogICAgICAgICAgICBfYyA9IFBhdGgoX3QpLyJjYXkiOyBzaHV0aWwuY29weXRyZWUo'
'Z29jLyJvcHMiLCBfYy8ib3BzIikKICAgICAgICAgICAgX2YgPSBfYy9kdW9uZzsgX25kID0gX2YucmVhZF90ZXh0KGVuY29k'
'aW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIGlmIF9uZC5jb3VudCh0aW0pICE9IDE6CiAgICAgICAgICAgICAgICBnaWV0W21h'
'XSA9IE5vbmUKICAgICAgICAgICAgICAgIGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzogbWF1IGRvdCBiaWVuIGto'
'b3Age19uZC5jb3VudCh0aW0pfSBsYW4gKG1vbmcgMSkiCiAgICAgICAgICAgICAgICAgICAgZiIg4oCUIG1hIG5ndW9uIGRh'
'IGRvaSwgZG90IGJpZW4gbmF5IGhldCB5IG5naGlhIik7IGNvbnRpbnVlCiAgICAgICAgICAgIF9mLndyaXRlX3RleHQoX25k'
'LnJlcGxhY2UodGltLCB0aGF5LCAxKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgX3NwID0gaW1wb3J0bGliLnV0'
'aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX2RiXyIgKyBtYSwgc3RyKF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5'
'IikpCiAgICAgICAgICAgIF9tID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3ApOyBfc3AubG9hZGVyLmV4'
'ZWNfbW9kdWxlKF9tKQogICAgICAgICAgICBkZWYgX2dvaV9kYigqKmt3KToKICAgICAgICAgICAgICAgIF9lID0gaW8uU3Ry'
'aW5nSU8oKQogICAgICAgICAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihfZSk6CiAgICAgICAgICAg'
'ICAgICAgICAgcmV0dXJuIF9tLl9naXRfd2luZG93cygqKmt3KSwgX2UuZ2V0dmFsdWUoKQogICAgICAgICAgICBfdHQsIF9j'
'dCwgXyA9IF9oYW0oX2dvaV9kYiwgaW5zcGVjdC5zaWduYXR1cmUoX20uX2dpdF93aW5kb3dzKSwKICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgIF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIGdpZXRbbWFdID0gKF90'
'dCA9PSBUUlVPVCkKICAgICAgICBpbm4oZiIgICAge21hOjR9IGRvdCBiaWVuIC0+IHtfdHQ6MTR9IHsnR0lFVCBEVU9DJyBp'
'ZiBfdHQgPT0gVFJVT1QgZWxzZSAnU09ORyBTT1QnfSIKICAgICAgICAgICAgKyAoZiIgICAoe19jdH0pIiBpZiBfY3QgZWxz'
'ZSAiIikpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAgICAgIGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHtt'
'YTo0fSBLSE9ORyBETyBEVU9DOiB7dHlwZShfZSkuX19uYW1lX199OiB7X2V9IikKZ2hpKCJjb25nX2dpZXRfZHVvY19kb3Rf'
'YmllbiIsIGdpZXQpCgpmb3IgdGVuLCAodHQsIGN0LCBkbCkgaW4gWyh0LCBmKGdvaSwgc2lnLCB0ZXB0KSkgZm9yIHQsIGYg'
'aW4gUFJPQkVdOgogICAgZ2hpKCJwcm9iZV8iICsgdGVuLnNwbGl0KClbMF0ubG93ZXIoKSwgZGwpCiAgICBpZiBpc2luc3Rh'
'bmNlKGRsLCBkaWN0KToKICAgICAgICBmb3IgaywgdiBpbiBkbC5pdGVtcygpOiBpbm4oZiIgICAge2s6MzR9OiB7dn0iKQog'
'ICAgbWEgPSB0ZW4uc3BsaXQoKVswXQogICAgaWYgZ2lldC5nZXQobWEpIGlzIG5vdCBUcnVlIGFuZCB0dCA9PSBEQVQ6CiAg'
'ICAgICAgIyBEQVQgdHUgbW90IGNvbmcgY2h1YSBjaHVuZyBtaW5oIGR1b2MgbGEgYmlldCBETyB0aGkga2hvbmcgZGFuZyB0'
'aW4gaG9uIEtERC4KICAgICAgICBrZXQodGVuLCBLREQsIGYiY29uZyBLSE9ORyBnaWV0IGR1b2MgZG90IGJpZW4gY3VhIGNo'
'aW5oIG5vICh7Z2lldC5nZXQobWEpIXJ9KSIKICAgICAgICAgICAgICAgICAgICAgIGYiIC0+IGNodSBEQVQgbmF5IGtob25n'
'IGNvIGdpYSB0cmkiKQogICAgZWxzZToKICAgICAgICBrZXQodGVuLCB0dCwgY3QpCgojIC0tLS0tLS0tLS0tLS0tLS0gNC4g'
'TjcgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4o'
'IiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjQuIE43IOKAlCBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIChjYXkgdGhhdCBL'
'SE9ORyBiaSBkdW5nIHRvaSkiKQogICAgdHJ1b2MgPSB0ZXAucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1B'
'VV9XSU4pCiAgICBnaGkoIm43X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIgIHNvIGRvbmcga2hvcCB7TUFVX1dJTiFyfTogVFJV'
'T0MgPSB7dHJ1b2N9IFttb25nIDFdIikKICAgIGlmIHRydW9jICE9IDE6CiAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFu'
'aCBXaW5kb3dzIiwgS0RELCBmIm1hdSB4dWF0IGhpZW4ge3RydW9jfSBsYW4sIGtob25nIHBoYWkgMSIpCiAgICBlbHNlOgog'
'ICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdG1wOgogICAgICAgICAgICBzYW8gPSBQYXRo'
'KHRtcCkvImNheSIKICAgICAgICAgICAgc2h1dGlsLmNvcHl0cmVlKGdvYywgc2FvLCBpZ25vcmU9c2h1dGlsLmlnbm9yZV9w'
'YXR0ZXJucygiLmdpdCIsICJfX3B5Y2FjaGVfXyIsICIqLnB5YyIpKQogICAgICAgICAgICBmMiA9IHNhby8ib3BzIi8ibGVh'
'c2VfcHVibGlzaC5weSIKICAgICAgICAgICAgZjIud3JpdGVfdGV4dChmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04Iiku'
'cmVwbGFjZShNQVVfV0lOLCAiaWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHNhdSA9IGYyLnJl'
'YWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKTsgZ2hpKCJuN19zYXUiLCBzYXUpCiAgICAgICAgICAg'
'IGlubihmIiAgU0FVIChkYSBkb3QgYmllbikgPSB7c2F1fSBbbW9uZyAwXSIpCiAgICAgICAgICAgIGlmIHNhdSAhPSAwOgog'
'ICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCAiZG90IGJpZW4gS0hPTkcgYXAg'
'ZHVvYyIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICByY19tLCBvdXRfbSA9IGNoYXkoWyJvcHMvbGVhc2Vf'
'cHVibGlzaF90ZXN0LnB5Il0sIHNhbykKICAgICAgICAgICAgICAgIG0xNjUgPSBtYXVfY2Eob3V0X20sICJ0MTY1Iik7IGRt'
'LCBfLCBfID0gZG9jX2RvKG91dF9tKQogICAgICAgICAgICAgICAgdGVuMTY1ID0gbmV4dCgodCBmb3IgdCBpbiBkbSBpZiB0'
'LnN0YXJ0c3dpdGgoInQxNjUiKSksIE5vbmUpCiAgICAgICAgICAgICAgICBseSA9IChkbS5nZXQodGVuMTY1KSBvciAiIikK'
'ICAgICAgICAgICAgICAgIGdoaSgibjdfdDE2NSIsIG0xNjUpOyBnaGkoIm43X2x5X2RvIiwgbHlbOjIwMF0pCiAgICAgICAg'
'ICAgICAgICBpbm4oZiIgIHQxNjUgc2F1IGRvdCBiaWVuOiB7bTE2NX0gfCB7bHlbOjExMF19IikKICAgICAgICAgICAgICAg'
'IGR1bmdfbHlfZG8gPSAiUEFUSCB0IiBpbiBseSBvciAiL3Vzci9iaW4iIGluIGx5CiAgICAgICAgICAgICAgICBrZXQoIk43'
'IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBEQVQgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykgZWxzZQogICAg'
'ICAgICAgICAgICAgICAgIChUUlVPVCBpZiBtMTY1ID09ICJETyIgZWxzZSBLREQpLAogICAgICAgICAgICAgICAgICAgICJn'
'aWV0IGR1bmcgbHkgZG8iIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pCiAgICAgICAgICAgICAgICAgICAgZWxz'
'ZSAoIkRPIG5odW5nIEtIT05HIGR1bmcgbHkgZG8gLT4gdGluIGR1bmcgZ2lhIiBpZiBtMTY1ID09ICJETyIgZWxzZSAia2hv'
'bmcgZG9jIGR1b2MgdDE2NSIpKQoKIyAtLS0tLS0tLS0tLS0tLS0tIEtFVCBMVUFOIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIi'
'KTsgaW5uKCI9IiAqIDc4KQppbm4oZiJUSEUgSEUgRE8gRFVPQzoge3RoZV9oZX0gICBIRUFEPXtoZWFkWzoxMl19IikKIyBL'
'aG9pIGRhbiBjaG8gcmV2aWV3ZXIgYmF0IGRhdSBvIGRvbmcgdHJlbiwgbmVuIENIRSBETyBwaGFpIG5hbSBOR0FZIGR1b2kg'
'bm86IGtob25nIGNvIGRvbmcgbmF5CiMgdGhpIG1vdCBsdW90IC0tY2hpLXByb2JlIGluICJEQVQgNyB8IFRSVU9UIDAgfCBL'
'SE9ORyBETyBEVU9DIDAiIHJjPTAgbWEga2hvbmcgbm9pIGxhIGNodWEgY2hheSBibyB0ZXN0LgpnaGkoImNoZV9kbyIsICJj'
'aGktcHJvYmUiIGlmIENISV9QUk9CRSBlbHNlICJkYXktZHUiKQppZiBDSElfUFJPQkU6CiAgICBpbm4oIi0tY2hpLXByb2Jl'
'OiBDSEkgZG8gbXVjIDAsIDEsIDMuIEJvIHRlc3QsIE4xLU40LCB0MTM2LCBONyBLSE9ORyBjaGF5IC0gZGF5IEtIT05HIHBo'
'YWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQppZiB0aGVfaGUgPT0gImcxIjoKICAgIGlubigiTFVVIFk6IGRheSBsYSBORU4g'
'RE8gKGcxKSwgS0hPTkcgcGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hvdCBOOC1OMTIgZHVvaSBkYXkiKQogICAgaW5uKCIg'
'ICAgICAgVFJVT1QgbGEgRFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEgbmh1bmcgbG8gZzIgc2luaCByYSBkZSB2w6EuIikK'
'aW5uKCItIiAqIDc4KQpmb3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAgIGlubihmIiAge3R0OjE0fSB7dGVufSIgKyAoZiIg'
'ICB7Y3R9IiBpZiBjdCBlbHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQpu'
'X3RydW90ID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQppbm4oIi0iICogNzgpCmlubihmIiAg'
'REFUIHtzdW0oMSBmb3IgXyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8IFRSVU9UIHtuX3RydW90fSB8IEtIT05HIERPIERV'
'T0Mge25fa2RkfSIpCmlubihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgnc29fY2FfZG8nKX0gfCBkYW5oIHNhY2ggZGF5IGR1'
'OiB7J0NPJyBpZiBzby5nZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAnS0hPTkcgRE8gRFVPQyd9IikKaW5uKGYiICBBZG1p'
'bmlzdHJhdG9yOiB7c28uZ2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxpbms6IHtzby5nZXQoJ3N5bWxpbmtfZHVvYycpfSIp'
'CmlubigiIik7IGlubigiLS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5BWSBWRSBDSE8gUkVWSUVXRVIgLS0tIikKZ2hpKCJj'
'aG90IiwgW3sidGVuIjogYSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3RpZXQiOiBjfSBmb3IgYSwgYiwgYyBpbiBjaG90XSkK'
'aW5uKGpzb24uZHVtcHMoc28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50PTEsIGRlZmF1bHQ9c3RyKSkKIyByYzogMCA9'
'IG1vaSBjaG90IERBVCB8IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNvIGNob3QgS0hPTkcgRE8gRFVPQyAodXUgdGllbiBi'
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
