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
$ShaBoDo    = '451cb305d273ba248e55f11826fa27d34b89a52745f362f91122761ec0f9f889'      # SHA-256 cua bo do Python nhung ben duoi

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
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0xMC0wMWciICAgICAgICAgICAgICAj'
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
'Z2xvYmFsIENVQSBDSS4gQ0kgS0hPTkcgY28gZ2xvYmFsIHJvbmc6IGpvYiBgZ2F0ZS1vcHNgIGN1YSBjaS55bWwgKG5vaSBj'
'aGF5IGJvIHRlc3QsCiMgdGFjaCBraG9pIGBnYXRlYCB0dSAjNjYwOyBidW9jICJGb3JjZSBMRiBjaGVja291dCIgZ2lvbmcg'
'aGV0IG8gYGdhdGVgLCBjYSB1YnVudHUgbGFuIHdpbmRvd3MpIGRhdCBnbG9iYWwgY29yZS5hdXRvY3JsZj1mYWxzZSwKIyBj'
'b3JlLmVvbD1sZiwgY29yZS5hYmJyZXY9NyBUUlVPQyBidW9jIGNoYXkgYm8gdGVzdCDigJQKIyB2aSAoY2kueW1sOjctOCB0'
'dSBraGFpKSBraG9uZyB0YXQgdGhpIHJ1bm5lciBXaW5kb3dzIGNoZWNrb3V0IENSTEY6IGF1dG9jcmxmPXRydWUgY3VhIGJh'
'biBjYWkgR2l0IG8gSEUgVEhPTkcuIEJhbiAzMGYKIyBkYXQgZ2xvYmFsID0gcm9uZyBuZW4gYm8gdGVzdCB0aGF5IGF1dG9j'
'cmxmPXRydWUgY29uIENJIHRoYXkgZmFsc2U6IGRvIHRyZW4gMjAyNi0wOS0zMGYsIDBlYTk1ZGUsIGhlIHRob25nIGF1dG9j'
'cmxmPXRydWUKIyArIGdsb2JhbCBuaHUgQ0kgPT4gYmFuIDMwZSAxNjYvMTY2LCBiYW4gMzBmIDE2NS8xNjYgKHQxNTAgRE8g'
'4oCUIGNoaSBraG9uZyB0aGFuaCBUUlVPVCB2aSB0MTUwIHRpbmggY28gbmFtIHRyb25nCiMgTkdPQUlfUEhBTV9WSSkuIEds'
'b2JhbCBsYSBURVAgVEFNIGNodWEgRFVORwojIGdsb2JhbCBjdWEgQ0kgY29uZyBpbml0LmRlZmF1bHRCcmFuY2ggZ2hpbSB2'
'ZSBtYWMgZGluaCBjdWEgZ2l0IChkYXQgZHVvYyBjYSBvIGhlIHRob25nKTogZ2xvYmFsIGRlIGxlbiBoZSB0aG9uZyBuaHUg'
'dHJlbiBDSSwKIyBjb24gY2F1IGhpbmggQ1VDIEJPIGN1YSBmaXh0dXJlIHZhbiBkZSBsZW4gZ2xvYmFsIChHSVRfQ09ORklH'
'X0NPVU5UIHRoaSBkZSBsZW4gY2EgY3VjIGJvKS4gRG9pIGJ1b2MgYXkgdHJvbmcgY2kueW1sIHRoaQojIGRvaSBfR0lUX0dM'
'T0JBTF9DSS4gR0lUX0NPTkZJR19HTE9CQUwgY2hpIHRoYXkgVEVQIENPTkZJRzogaWdub3JlL2F0dHJpYnV0ZXMgbWFjIGRp'
'bmggKCRYREdfQ09ORklHX0hPTUUgaG9hYyB+Ly5jb25maWcvZ2l0LwojIGlnbm9yZXxhdHRyaWJ1dGVzKSBjdWEgbmd1b2kg'
'ZG8gVkFOIGFwIGNobyBnaXQgY29uIChkbyB0cmVuIDIwMjYtMDktMzBnLCAwZWE5NWRlOiB+Ly5jb25maWcvZ2l0L2lnbm9y'
'ZSBgKi55YW1sYCA9PiBiYW4gMzBnCiMgMTU0LzE2NiwgMTEgY2EgImxhIik7IENJIGtob25nIGNvIHRlcCBuYW8gbyBkbyA9'
'PiBYREdfQ09ORklHX0hPTUUgdHJvIHZhbyB0aHUgbXVjIFRBTSBST05HLiBDb24gbGFpIChraG9hIGhlIHRob25nIGtoYWMp'
'CiMgbGEgZ2lvaSBoYW4gZGEgYmlldCwga2hvbmcgcGhhaSBkYSBkb25nLgojIENhdSBoaW5oIHNoZWxsY2hlY2sgQ1VBIE5H'
'VU9JIERPIGxvdCB2YW8gYm8gdGVzdCB5IG5odSBnaXQ6IHQxMzcgZ29pIHNoZWxsY2hlY2sgVEhBTkcsIHQzMy90MTM3IGdv'
'aSBhY3Rpb25saW50IC0+IHNoZWxsY2hlY2ssCiMgY2EgaGFpIGRvYyBTSEVMTENIRUNLX09QVFMsIHZhIHQxMzcgZG9jIH4v'
'LnNoZWxsY2hlY2tyYyAoWERHX0NPTkZJR19IT01FIHRhbSBLSE9ORyBjaGUgZHVvYzsgY2hvIHRlcCByYyB0cmVuIFdpbmRv'
'd3M6IEtIT05HIERPIERVT0MpLgojIERvIHRyZW4gMjAyNi0wOS0zMGgsIDBlYTk1ZGU6IFNIRUxMQ0hFQ0tfT1BUUz0tLWVu'
'YWJsZT1hbGwgPT4gdDMzICsgdDEzNyBETzsgfi8uc2hlbGxjaGVja3JjIGBlbmFibGU9YWxsYCA9PiB0MTM3IERPIOKAlCBj'
'YSAibGEiCiMgPT4gVFJVT1QgY2hvIHVuZyB2aWVuIHNhY2guIENJIGtob25nIGNvIGNhIGhhaS4gU0hFTExDSEVDS19PUFRT'
'PS0tbm9yYyBkZSBsZW4gYmllbiBjdWEgbmd1b2kgZG8gVkEgdGF0IG1vaSB0ZXAgcmMgKHNoZWxsY2hlY2sKIyBwaGFpIE5I'
'QU4gLS1ub3JjIOKAlCBtdWMgMCBob2kgdHJ1b2MpLgojIEJpZW4gS0hPSSBET05HIGN1YSBiYXNoIENVQSBOR1VPSSBETyBs'
'b3QgdmFvIGJvIHRlc3QgeSBuaHUgYmEgbmhvbSB0cmVuOiB0MzIvdDUxLXQ2OCBjaGF5IGJhc2ggdm9pIGRpY3Qob3MuZW52'
'aXJvbiwgLi4uKS4gRG8KIyB0cmVuIDIwMjYtMTAtMDEgKGJhbiAwMWQpLCAwZWE5NWRlOiBTSEVMTE9QVFM9bm9jbG9iYmVy'
'LCBob2FjIEJBU0hfRU5WIGNodWEgYHNldCAtbyBub2Nsb2JiZXJgID0+IHQzMiB0NTEgdDYwIHQ2MiB0NjMgdDY2IHQ2OCBE'
'TwojICJjYW5ub3Qgb3ZlcndyaXRlIGV4aXN0aW5nIGZpbGUiIOKAlCBjYSAibGEiID0+IFRSVU9UIGNobyB1bmcgdmllbiBz'
'YWNoIOKAlCB0cm9uZyBraGkgbXVjIDAgY2hvIHF1YTogbm8gaG9pIGBnaXQgLS12ZXJzaW9uYAojIHRyb25nIGJhc2gsIGNh'
'dSBIRVAgaG9uIGNhdSBibyB0ZXN0IGNhbi4gQkFTSF9FTlYgaW4gYnl0ZSBuZ29haSBVVEYtOCA9PiAxNTIvMTY2LiBDSSBr'
'aG9uZyBkYXQgYmllbiBuYW8gdHJvbmcgbmhvbSBuYXkuIEJvCiMgdGhlbyBUQVAgYmFzaCgxKSBkb2Mga2hpIGNoYXkgc2Ny'
'aXB0OiBtb2kgdGVuIGJhdCBkYXUgYEJBU0hgIChCQVNIX0VOViBCQVNIT1BUUyBCQVNIX0ZVTkNfKiBCQVNIX1hUUkFDRUZE'
'IEJBU0hfQ09NUEFUIC4uLikgY29uZwojIF9CQVNIX0tIT0lfRE9ORy4gVHJvbmcgbmhvbSBURU4sIGNoaSBoYWkgbXVjIHRy'
'ZW4gRE8gRFVPQyBsYW0gRE8gKGN1YSBTU0hfQ0xJRU5UIHZhIHN0ZGluOiB4ZW0gZHVvaSk7IGNhYyB0ZW4gY29uIGxhaSBi'
'byB2aSBDSQojIGtob25nIGRhdCwgS0hPTkcgdmkgZGEgdGhheSBETyAoZG8gMjAyNi0xMC0wMTogU0hFTExPUFRTIHh0cmFj'
'ZS9ub3Vuc2V0L3BpcGVmYWlsL25vZ2xvYi9hbGxleHBvcnQsIEJBU0hPUFRTIGZhaWxnbG9iL251bGxnbG9iLwojIHhwZ19l'
'Y2hvLCBQT1NJWExZX0NPUlJFQ1QsIENEUEFUSCwgRlVOQ05FU1Q9MSwgVE1PVVQ9MSA9PiA5LzkgY2EgYmFzaCkuIElGUyBi'
'YXNoIEtIT05HIG5oYW4gdHUgbW9pIHRydW9uZy4gdDE1MiB2b24gY2hpIHRydXllbgojIFBBVEggbmVuIGtob25nIGRvaS4g'
'TXVjIDAgdHUga2hhaSBURU4gKGtob25nIGluIGdpYSB0cmkpLgojIFRBUCBheSBjb24gbW90IGN1YSBLSE9ORyBtYW5nIHRl'
'biBiaWVuIGtob2kgZG9uZzogYmFzaCgxKSBJTlZPQ0FUSU9OIOKAlCBzdGRpbiBsYSBTT0NLRVQgKHJzaGQpLCBob2FjIFNT'
'SF9DTElFTlQvU1NIMl9DTElFTlQgdHJvbmcKIyBtb2kgdHJ1b25nIChiYW4gZGljaCBiYXQgU1NIX1NPVVJDRV9CQVNIUkM6'
'IEdpdCBmb3IgV2luZG93cyBiYXQgY2Egbm8gbGFuIFNZU19CQVNIUkMg4oCUIDAwMDEtYmFzaC00LjQtY3lnd2luLnBhdGNo'
'IHN1YSBjb25maWctdG9wLmg7CiMgYmFzaCBVYnVudHUgY3VuZyBiYXQpLCBjb25nIFNITFZMIHJvbmcvMCA9PiBgYmFzaCAt'
'Y2AgbmFwIC9ldGMvYmFzaC5iYXNocmMgdmEgfi8uYmFzaHJjIENVQSBOR1VPSSBETywgdmEgQk8gUVVBIEJBU0hfRU5WLiBD'
'SSBjaGF5CiMgYm8gdGVzdCBxdWEgYGJhc2ggb3BzL2NoYXlfbGVhc2VfcHVibGlzaF90ZXN0LnNoYCAoam9iIGBnYXRlLW9w'
'c2AsIGJ1b2MgYHNoZWxsOiBiYXNoYCk6IHdyYXBwZXIgYGV4ZWNgIHB5dGhvbiBuZW4gcHl0aG9uIHRoYXkgU0hMVkw9MQoj'
'IChleGVjIGdpYW0gU0hMVkw7IGRvIDIwMjYtMTAtMDkgdHJlbiBjaHVvaSBidW9jIC0+IGBiYXNoIHdyYXBwZXJgIC0+IGBl'
'eGVjIHB5dGhvbmA6IDEsIHdyYXBwZXIgS0hPTkcgZXhlYzogMikgdmEgYGJhc2ggLWNgIGN1YSBibwojIHRlc3QgdGhheSAy'
'IOKAlCBEVU5HIG5ndW9uZyBgPCAyYCAoYmllbiAwKTogYnVvYyBjaGF5IGJhbmcgYGJhc2ggLWNgIG1vdCBkb25nIHRoaSBw'
'eXRob24gdGhheSAwIHZhIGR1b25nIG5heSBNTy4gTmVuIGR1b25nIG5heSBUQVQKIyB0cmVuIENJOyBwd3NoL2NtZCBraG9u'
'ZyBkYXQgU0hMVkwgbmVuIHRyZW4gbWF5IGRvIG5vIE1PLiBEbyB0cmVuIDIwMjYtMTAtMDEgKGJhbiAwMWUsIGJhc2ggNS4y'
'LjIxKSwKIyAwZWE5NWRlOiBTU0hfQ0xJRU5UICsgfi8uYmFzaHJjIGBzZXQgLW8gbm9jbG9iYmVyYCA9PiB0MzIgdDUxIHQ2'
'MCB0NjIgdDYzIHQ2NiB0NjggRE8sIGUyZSByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCAoMTU5LzE2Nik7CiMgfi8uYmFzaHJj'
'IGBjZCAiJEhPTUUiYCA9PiA4IGNhICh0aGVtIHQ1OSk7IHN0ZGluIFNPQ0tFVCArIG5vY2xvYmJlciA9PiBjdW5nIDcgY2Eu'
'IE11YyAwIGtob25nIHRoYXkgKHByb2JlIGdvaSBgLS1ub3JjYCwgbWEgLS1ub3JjCiMgdGF0IGR1b25nIG5heSk6IG8gYmFu'
'IDAxZSBubyB0dSBraGFpICJiaWVuIGJhc2g6IChraG9uZyBjbykiOyB0dSBiYW4gMDFmIG11YyAwIGtoYWkgVEVOIFNTSF9D'
'TElFTlQgbmV1IGNvLCBjb24gc3RkaW4gU09DS0VUIHRoaQojIEtIT05HIGNvIHRlbiBuYW8gZGUga2hhaSAoY2hvdDogREVW'
'TlVMTCB0cm9uZyBjaGF5KCkpLiBQaGllbiBTU0ggdmFvIG1heSBXaW5kb3dzIGRvIGxhIGN1YSB2YW8gKFdpbmRvd3MgVEhB'
'VDogS0hPTkcgRE8gRFVPQykuIEJvIEhBSQojIGJpZW4gYXkgKENJIGtob25nIGRhdCkgVkEgY2hvIGx1b3QgY29uIHN0ZGlu'
'ID0gREVWTlVMTCDigJQgaGFpIGNvIGNoZSByaWVuZywgaGFpIGNob3Qgcmllbmc7IHQxNTIgKGVudiBjaGkgUEFUSCkgdGh1'
'YSBrZSBzdGRpbiBheSBuZW4KIyBjdW5nIGRvbmcuCl9CQVNIX0tIT0lfRE9ORyA9IGZyb3plbnNldCh7IlNIRUxMT1BUUyIs'
'ICJFTlYiLCAiUE9TSVhMWV9DT1JSRUNUIiwgIkNEUEFUSCIsICJHTE9CSUdOT1JFIiwgIkdMT0JTT1JUIiwgIkVYRUNJR05P'
'UkUiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICJGVU5DTkVTVCIsICJUTU9VVCIsICJTU0hfQ0xJRU5UIiwgIlNT'
'SDJfQ0xJRU5UIn0pCmRlZiBfYmllbl9iYXNoKGspOiByZXR1cm4gay51cHBlcigpLnN0YXJ0c3dpdGgoIkJBU0giKSBvciBr'
'LnVwcGVyKCkgaW4gX0JBU0hfS0hPSV9ET05HCl9HSVRfR0xPQkFMX0NJID0gIltpbml0XVxuXHRkZWZhdWx0QnJhbmNoID0g'
'bWFzdGVyXG5bY29yZV1cblx0YXV0b2NybGYgPSBmYWxzZVxuXHRlb2wgPSBsZlxuXHRhYmJyZXYgPSA3XG4iCmRlZiBjaGF5'
'KGFyZ3YsIGN3ZCwgcGh1dD02MCk6CiAgICBmZCwgZ2MgPSB0ZW1wZmlsZS5ta3N0ZW1wKHByZWZpeD0id3A1NDEtZ2l0Y29u'
'ZmlnLWNpLSIsIHN1ZmZpeD0iLmluaSIpCiAgICB4ZGcgPSBOb25lCiAgICB0cnk6CiAgICAgICAgeGRnID0gdGVtcGZpbGUu'
'bWtkdGVtcChwcmVmaXg9IndwNTQxLXhkZy0iKQogICAgICAgIHdpdGggb3MuZmRvcGVuKGZkLCAidyIsIGVuY29kaW5nPSJh'
'c2NpaSIsIG5ld2xpbmU9IlxuIikgYXMgZjogZi53cml0ZShfR0lUX0dMT0JBTF9DSSkKICAgICAgICBtdCA9IHtrOiB2IGZv'
'ciBrLCB2IGluIG9zLmVudmlyb24uaXRlbXMoKQogICAgICAgICAgICAgIGlmIG5vdCBrLnVwcGVyKCkuc3RhcnRzd2l0aCgi'
'R0lUXyIpIGFuZCBub3QgX2JpZW5fYmFzaChrKQogICAgICAgICAgICAgIGFuZCAobm90IGsudXBwZXIoKS5zdGFydHN3aXRo'
'KCJQWVRIT04iKSBvciBrLnVwcGVyKCkgaW4gX1BZX0dJVSl9CiAgICAgICAgbXQudXBkYXRlKFBZVEhPTlVURjg9IjEiLCBQ'
'WVRIT05JT0VOQ09ESU5HPSJ1dGYtOCIsIFBZVEhPTkRPTlRXUklURUJZVEVDT0RFPSIxIiwgUFlUSE9OVU5CVUZGRVJFRD0i'
'MSIsCiAgICAgICAgICAgICAgICAgIEdJVF9DT05GSUdfR0xPQkFMPWdjLCBYREdfQ09ORklHX0hPTUU9eGRnLCBTSEVMTENI'
'RUNLX09QVFM9Ii0tbm9yYyIpCiAgICAgICAgcCA9IHN1YnByb2Nlc3MucnVuKFtzeXMuZXhlY3V0YWJsZV0gKyBhcmd2LCBj'
'd2Q9c3RyKGN3ZCksIGNhcHR1cmVfb3V0cHV0PVRydWUsIHN0ZGluPXN1YnByb2Nlc3MuREVWTlVMTCwKICAgICAgICAgICAg'
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
'R19DVV9HSVRfTkdVT0lfRE8pCl9iYXNoX2JvID0gZ2hpKCJiaWVuX2Jhc2hfbmd1b2lfZG9fZGFfYm8iLCBzb3J0ZWQoayBm'
'b3IgayBpbiBvcy5lbnZpcm9uIGlmIF9iaWVuX2Jhc2goaykpKQppbm4oIiAgYmllbiBiYXNoICAgIDoiLCAoIiwgIi5qb2lu'
'KF9iYXNoX2JvKSArICIgIC0+IERBIEJPIGtob2kgbHVvdCBjb24gKENJIGtob25nIGRhdDsgeGVtIGNoYXkoKSkiKSBpZiBf'
'YmFzaF9ibyBlbHNlICIoa2hvbmcgY28pIikKaW5uKCIgIGdvYyBraG8gICAgICA6IiwgZ29jKQoKcXV5ZW4gPSBOb25lCmlm'
'IHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAgIGltcG9ydCBjdHlwZXM7IHF1eWVuID0gYm9vbChj'
'dHlwZXMud2luZGxsLnNoZWxsMzIuSXNVc2VyQW5BZG1pbigpKQogICAgZXhjZXB0IEV4Y2VwdGlvbjogcXV5ZW4gPSBOb25l'
'CmdoaSgicXV5ZW5fYWRtaW4iLCBxdXllbikKc3ltbGlua19kdW9jID0gTm9uZQp0cnk6CiAgICB3aXRoIHRlbXBmaWxlLlRl'
'bXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgodCkvImEudHh0IjsgZC53cml0ZV90ZXh0KCJ4Iiwg'
'ZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICB0cnk6IG9zLnN5bWxpbmsoc3RyKGQpLCBzdHIoUGF0aCh0KS8ibGsiKSk7IHN5'
'bWxpbmtfZHVvYyA9IFRydWUKICAgICAgICBleGNlcHQgT1NFcnJvciBhcyBlOiBzeW1saW5rX2R1b2MgPSBGYWxzZTsgZ2hp'
'KCJzeW1saW5rX2xvaSIsIGYie3R5cGUoZSkuX19uYW1lX199OiB7ZX0iKQpleGNlcHQgRXhjZXB0aW9uIGFzIGU6IGdoaSgi'
'c3ltbGlua19sb2kiLCBzdHIoZSkpCmdoaSgic3ltbGlua19kdW9jIiwgc3ltbGlua19kdW9jKQppbm4oIiAgQWRtaW5pc3Ry'
'YXRvcjoiLCBxdXllbiwgInwgdGFvIHN5bWxpbmsgZHVvYzoiLCBzeW1saW5rX2R1b2MpCgpsb2kgPSBbXQojIENvbmcga2lj'
'aCB0aHVvYyBsYSBwaGVwIGRvIHRyZW4gTElDSCBTVSBHSVQsIGtob25nIGRpbmggZ2kgZGVuIG5lbi4gQ2hvIHBoZXAKIyAt'
'LWNoaS1raWNoLXRodW9jIGNoYXkgbyBtb2kgbmVuIGRlIGNvbiBUVSBLSUVNIGR1b2MgY2hpbmggY29uZyBuYXkgKGRhIGR1'
'bmcKIyBkZSB0YWkgZHVuZyBjYSBoYWkgdmUgY3VhIHN1IGNvIG5lbi1jdSAxOS0wOSkuIE1vaSBjaG90IENIVUMgTkFORyB2'
'YW4gZG9pIFdpbmRvd3MuCmlmIHN5cy5wbGF0Zm9ybSAhPSAid2luMzIiIGFuZCAiLS1jaGkta2ljaC10aHVvYyIgbm90IGlu'
'IHN5cy5hcmd2OgogICAgbG9pLmFwcGVuZChmIktIT05HIHBoYWkgV2luZG93cyAoc3lzLnBsYXRmb3JtPXtzeXMucGxhdGZv'
'cm0hcn0pIikKaWYgbm90IHRlcC5pc19maWxlKCk6ICBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwfSIpCmlmIG5vdCB0'
'ZXB0LmlzX2ZpbGUoKTogbG9pLmFwcGVuZChmImtob25nIHRoYXkge3RlcHR9IikKaWYgbm90IHNodXRpbC53aGljaCgiZ2l0'
'Iik6IGxvaS5hcHBlbmQoImtob25nIGNvIGBnaXRgIHRyb25nIFBBVEgiKQojIEJvIHRlc3QgKG11YyAyIHZhIE43KSBjYW4g'
'UHlZQU1MOiB0aGlldSBubywgMGVhOTVkZSByYSA5Ni8xNjYgY2EgRE8gKDg5IGJhbyB0aGFuZyAiTm8gbW9kdWxlIG5hbWVk'
'ICd5YW1sJyIsCiMgNyBxdWEgbHVvdCBjb247IGNvIFB5WUFNTDogMTY2LzE2NiBRVUEpLiBCbyBkbyBnb2kgY2h1bmcgbGEg'
'ImNhIERPIExBIiByb2kgcGhhdCBUUlVPVCDigJQgZG8gdHJlbiAyMDI2LTA5LTMwYy4KIyBEaWV1IGtpZW4gdGllbiBxdXll'
'dCBwaGFpIGhvaSBiYW5nIENISU5IIHRpZW4gdHJpbmggY29uIHNlIGNoYXkgYm8gdGVzdCAoY2hheSgpOiBjdW5nIG1vaSB0'
'cnVvbmc7IGN3ZCA9IG9wcy8gPQojIHN5cy5wYXRoWzBdIGN1YSBibyB0ZXN0KSB2YSBob2kgRFVORyBEVU9DIGNodSBraG9u'
'ZyBob2kgQ08gTUFULiBCYW4gMzBkIGhvaSBgZmluZF9zcGVjKCJ5YW1sIilgIG8gdGllbiB0cmluaAojIE5BWSB2YSBuZ3Vv'
'bmcgMy44IHN1eSB0dSBOR1UgUEhBUCAoYDo9YCkg4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGQsIGNhIGhhaSByYSByYz0xIFRS'
'VU9UIGNobyB1bmcgdmllbiBzYWNoOgojIHRodSBtdWMgZHUgbGlldSBgeWFtbC9gIHRyZW4gUFlUSE9OUEFUSCBxdWEgZmlu'
'ZF9zcGVjIG1hIGB5YW1sLnNhZmVfZHVtcGAga2hvbmcgY28gKDg3IGNhICJsYSIpOyBweXRob24gMy44LjIwCiMgVEhBVCBj'
'byBQeVlBTUwsIGJvIHRlc3QgZHVuZyBgc3RyLnJlbW92ZXByZWZpeGAgKDMuOSkgbHVjIENIQVkgKDMzIGNhICJsYSI7IDMu'
'OS4yMzogMTY2LzE2NikuCiMgIkR1bmcgZHVvYyIgbmdoaWEgbGEgZHVuZyBEVU5HIEFQSSBibyB0ZXN0IGdvaTogdmlldCgp'
'ICg0MyBsb2kgZ29pKSB2YSBsZWFzZV9wdWJsaXNoLnB5IGdvaSBzYWZlX2R1bXAoLi4uLCBhbGxvd191bmljb2RlPVRydWUs'
'CiMgc29ydF9rZXlzPUZhbHNlKSwgbWEgYHNvcnRfa2V5c2AgY2hpIGNvIHR1IFB5WUFNTCA1LjEuIERvIHRyZW4gMjAyNi0w'
'OS0zMGwsIDBlYTk1ZGU6IHB5dGhvbiAzLjkuMjMgKyBQeVlBTUwgMy4xMyBUSEFUIHF1YSBwcm9iZQojIGN1IChyYz0wKSwg'
'Ym8gdGVzdCAxMDkvMTY2IOKAlCA1NiBjYSAibGEiOiA1MiBgdW5leHBlY3RlZCBrZXl3b3JkIGFyZ3VtZW50ICdzb3J0X2tl'
'eXMnYCwgdDI2L3QyNyBgUmVhZGVyRXJyb3JgIChreSB0dSBuZ29haSBCTVApLAojIHQxMjQvdDE1MyBETyB0aGVvIGx1b3Qg'
'Y29uIOKAlCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWA7IFB5WUFNTCA1LjE6IDE2Ni8xNjYgKGRvIGxhaSAyMDI2LTEw'
'LTAxOiBjdW5nIHNvKS4KIyAoUHl0aG9uID49IDMuMTAgKyBQeVlBTUwgMy4xMyBkYSB0cnVvdCBwcm9iZSBjdSB2aSBgY29s'
'bGVjdGlvbnMuSGFzaGFibGVgLikgUHJvYmUgY3VhIHBzMSAoJG1hVGh1KSBwaGFpIEdJT05HIEhFVCBkb25nIGR1b2kuCmlm'
'IG5vdCAoIi0tY2hpLWtpY2gtdGh1b2MiIGluIHN5cy5hcmd2IG9yICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YpOgogICAg'
'X3JjX2RrLCBfcmFfZGsgPSBjaGF5KFsiLWMiLCAiaW1wb3J0IHN5czsgc3lzLmV4aXQoOSkgaWYgc3lzLnZlcnNpb25faW5m'
'byA8ICgzLCA5KSBlbHNlIE5vbmU7IGltcG9ydCB5YW1sOyIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiB5'
'YW1sLnNhZmVfZHVtcCh5YW1sLnNhZmVfbG9hZCgnYTogMScpLCBhbGxvd191bmljb2RlPVRydWUsIHNvcnRfa2V5cz1GYWxz'
'ZSkiXSwKICAgICAgICAgICAgICAgICAgICAgICAgICBnb2MgLyAib3BzIiBpZiAoZ29jIC8gIm9wcyIpLmlzX2RpcigpIGVs'
'c2UgUGF0aC5jd2QoKSwgcGh1dD0yKQogICAgaWYgX3JjX2RrID09IDk6CiAgICAgICAgbG9pLmFwcGVuZChmInB5dGhvbiB7'
'c3lzLnZlcnNpb24uc3BsaXQoKVswXX0gPCAzLjk6IGJvIHRlc3QgY3VhIHVuZyB2aWVuIGR1bmcgc3RyLnJlbW92ZXByZWZp'
'eCAoMy45KSBsdWMgQ0hBWSIpCiAgICBlbGlmIF9yY19kazoKICAgICAgICBsb2kuYXBwZW5kKGYicHl0aG9uIG5heSBLSE9O'
'RyBjbyBQeVlBTUwgZHVuZyBkdW9jICh7KF9yYV9kay5zdHJpcCgpLnNwbGl0bGluZXMoKSBvciBbJyddKVstMV1bOjkwXX0p'
'OiIKICAgICAgICAgICAgICAgICAgIGYiIFwie3N5cy5leGVjdXRhYmxlfVwiIC1tIHBpcCBpbnN0YWxsIC1VIHB5eWFtbCIK'
'ICAgICAgICAgICAgICAgICAgICIgKGJhbiBuaHVuZyBwczEgdHUgdGFpIEtIT05HIGNvIHBpcDogY2hheSBsYWkgdm9pIC1Q'
'eSA8cHl0aG9uIGRhIGNvIFB5WUFNTD4pIikKICAgICMgQm8gdGVzdCBjb24gZ29pIGBzaHV0aWwud2hpY2hgIGNobyBiYXNo'
'L2FjdGlvbmxpbnQvc2hlbGxjaGVjayAoMGVhOTVkZTogdDMzIHQxMzcgdDE1OSBjYW4gYWN0aW9ubGludCwgdDEzNyBjYW4K'
'ICAgICMgc2hlbGxjaGVjaywgY2FjIGNhIGNoYXkgb3BzL2NhaV9hY3Rpb25saW50LnNoIGNhbiBiYXNoKS4gVGhpZXUgdGhp'
'IGNhYyBjYSBheSBpbiAiS0hPTkcgRE8gRFVPQzogdGhpZXUgYC4uLmAiIHZhIGJvIGRvIHJhCiAgICAjIHJjPTMg4oCUIG5o'
'dW5nIGNoaSBTQVUgY2EgYm8gdGVzdCBsYW4gTjcgKGRvIHRyZW4gMjAyNi0wOS0zMGcsIFBBVEggdGhpZXUgYWN0aW9ubGlu'
'dDogYENvbmcgY3UgZGF5IGR1IGRlIGRvYCBLREQsIHJjPTMKICAgICMgc2F1IDIgbHVvdCBibyB0ZXN0KS4gQ3VuZyBseSBk'
'byBQeVlBTUwgZHVvYyBob2kgbyBkYXk6IGhvaSBUUlVPQywgY3VuZyBQQVRIIG1hIGNoYXkoKSB0cnV5ZW4gY2hvIGJvIHRl'
'c3QuCiAgICAjIFZBIGN1bmcgQ0hPIGJvIHRlc3QgZHVuZzogdHJlbiBXaW5kb3dzIGBzaHV0aWwud2hpY2hgIHRyYSBUSFUg'
'TVVDIEhJRU4gSEFOSCBUUlVPQyBQQVRILCBtYSBibyB0ZXN0IGNoYXkgdm9pIGN3ZCA9IGdvYyBjb24KICAgICMgdGllbiB0'
'cmluaCBuYXkgZHVuZyBvIGN3ZCBDVUEgTkdVT0kgRE8gKG5vaSBnb2kgcHMxLCB2ZC4gRG93bmxvYWRzIOKAlCBkdW5nIG5v'
'aSBnaWFpIG5lbiBhY3Rpb25saW50LmV4ZSkuIERvIHRyZW4gMjAyNi0wOS0zMGsKICAgICMgKG5oYW5oIHdpbjMyIFRIQVQg'
'Y3VhIHNodXRpbC53aGljaCk6IGFjdGlvbmxpbnQgdG90IG8gY3dkIG5ndW9pIGRvICsgYmFuIGhvbmcgZGF1IFBBVEggPT4g'
'bXVjIDAgaG9pIGJhbiBvIGN3ZCAocmM9MCksIGJvIHRlc3QKICAgICMgZHVuZyBiYW4gdHJlbiBQQVRIID0+IHJjPTEgYERB'
'VCAxMSB8IFRSVU9UIDFgLCBgbGE6IFsndDMzJywgJ3QxMzcnLCAndDE1OSddYC4gR2lhaSB0ZW4gdm9pIGN3ZCA9IGdvYyBy'
'b2kgZ29pIFRIQU5HIGJhbmcgZHVvbmcKICAgICMgVFVZRVQgRE9JIGRhIGdpYWkgKHF1YSBoYW4gdGhpIHJ1bigpIGdpZXQg'
'ZHVuZyB0aWVuIHRyaW5oIOKAlCBseSBkbyBiYW4gMzBpIGtob25nIGhvaSBxdWEgY2hheSgpKS4KICAgIF9jd2Rfbmd1b2lf'
'ZG8gPSBvcy5nZXRjd2QoKQogICAgdHJ5OgogICAgICAgIGlmIGdvYy5pc19kaXIoKTogb3MuY2hkaXIoZ29jKQogICAgICAg'
'IF9jYyA9IHtjOiAob3MucGF0aC5hYnNwYXRoKHApIGlmIHAgZWxzZSBOb25lKSBmb3IgYywgcCBpbgogICAgICAgICAgICAg'
'ICAoKGMsIHNodXRpbC53aGljaChjKSkgZm9yIGMgaW4gKCJiYXNoIiwgImFjdGlvbmxpbnQiLCAic2hlbGxjaGVjayIpKX0K'
'ICAgIGZpbmFsbHk6CiAgICAgICAgb3MuY2hkaXIoX2N3ZF9uZ3VvaV9kbykKICAgIF90aGlldV9jYyA9IFtjIGZvciBjLCBw'
'IGluIF9jYy5pdGVtcygpIGlmIG5vdCBwXQogICAgaWYgX3RoaWV1X2NjOgogICAgICAgIGxvaS5hcHBlbmQoZiJ0aGlldSBj'
'b25nIGN1IGJvIHRlc3QgZ29pIHF1YSBQQVRIOiB7X3RoaWV1X2NjfSAoYWN0aW9ubGludDogb3BzL2NhaV9hY3Rpb25saW50'
'LnNoIHZvaSBBTF9WRVI7IgogICAgICAgICAgICAgICAgICAgIiBiYXNoOiBHaXQgQmFzaCwga2hvbmcgcGhhaSBiYXNoLmV4'
'ZSBjdWEgV1NMKSIpCiAgICAjIHNoZWxsY2hlY2sgS0hPTkcgbmhhbiAtLW5vcmMgdGhpIGFjdGlvbmxpbnQgMS43LjcgKHR1'
'IHRydXllbiAtLW5vcmMpIGxhbSB0MzMgRE8sIHZhIFNIRUxMQ0hFQ0tfT1BUUz0tLW5vcmMgY3VhIGNoYXkoKSBsYW0KICAg'
'ICMgdDEzNyBETyDigJQgY2EgImxhIiA9PiBUUlVPVCBnaWEgKGRvIHRyZW4gMjAyNi0wOS0zMGgsIHNoZWxsY2hlY2sgZ2lh'
'IHR1IGNob2kgLS1ub3JjOiBiYW4gMzBoIHJjPTEgYGxhOiBbJ3QzMyddYCBzYXUgY2EKICAgICMgYm8gdGVzdCkuIGB3aGlj'
'aGAgY2hpIGhvaSBDTyBNQVQ7IG8gZGF5IGhvaSBEVU5HIERVT0MuIE5ndW9uZyBkbyB0cmVuIHNoZWxsY2hlY2sgVEhBVDog'
'MC40LjcvMC41LjAvMC42LjAgdHUgY2hvaSAtLW5vcmMKICAgICMgKHJjPTMpLCAwLjcuMCB0cm8gbGVuIG5oYW4uIFBoZXAg'
'aG9pIHBoYWkgdGhheSBEVU5HIFNIRUxMQ0hFQ0tfT1BUUyBtYSBjaGF5KCkgZGF0IGNobyBsdW90IGNvbjogYmFuIDMwaSBo'
'b2kgdm9pIGJpZW4gQ1VBCiAgICAjIE5HVU9JIERPIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBpLCBzaGVsbGNoZWNrIDAuOS4w'
'ICsgU0hFTExDSEVDS19PUFRTPS0tZXh0ZW5kZWQtYW5hbHlzaXM9dHJ1ZSAoY28gY3VhIDAuMTApOiByYz0zICJraG9uZyBu'
'aGFuCiAgICAjIC0tbm9yYzogY2FwIG5oYXQgc2hlbGxjaGVjayIgdHJvbmcga2hpIHQzMy90MTM3IHF1YSBjaGF5KCkgZGV1'
'IDEvMS4gR29pIFRIQU5HIChraG9uZyBxdWEgY2hheSgpKTogcXVhIGhhbiB0aGkgcnVuKCkgZ2lldAogICAgIyBkdW5nIHNo'
'ZWxsY2hlY2s7IHF1YSBjaGF5KCkgdGhpIGNoaSBnaWV0IHB5dGhvbiBjb24sIHNoZWxsY2hlY2sgdHJlbyBvIGxhaSBtbyBj'
'b2kgKGRvIHRyZW4gMjAyNi0wOS0zMGk6IDEvMSBjb24gc29uZykuCiAgICBlbGlmIHN1YnByb2Nlc3MucnVuKFtfY2NbInNo'
'ZWxsY2hlY2siXSwgIi0tbm9yYyIsICItLXZlcnNpb24iXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGltZW91dD02MCwKICAg'
'ICAgICAgICAgICAgICAgICAgICAgZW52PWRpY3Qob3MuZW52aXJvbiwgU0hFTExDSEVDS19PUFRTPSItLW5vcmMiKSkucmV0'
'dXJuY29kZToKICAgICAgICBsb2kuYXBwZW5kKCJzaGVsbGNoZWNrIHRyZW4gUEFUSCBraG9uZyBuaGFuIC0tbm9yYyAoYWN0'
'aW9ubGludCAxLjcuNyB2YSBjaGF5KCkgZGV1IHRydXllbiBjbyBheSk6IGNhcCBuaGF0IHNoZWxsY2hlY2siKQogICAgIyBh'
'Y3Rpb25saW50IGN1bmcgcGhhaSBEVU5HIERVT0MsIGtob25nIGNoaSBDTyBNQVQ6IHQzMy90MTM3L3QxNTkgZ29pIG5vIFRI'
'QU5HLCB2YSBtb3QgYWN0aW9ubGludCBraG9uZyBjaGF5IChzYWkga2llbiB0cnVjLAogICAgIyBob25nKSBsYW0gY2EgYmEg'
'RE8gImFjdGlvbmxpbnQgRE8gKHJjPS4uLikiIOKAlCBjYSAibGEiID0+IFRSVU9UIGdpYSBzYXUgY2EgYm8gdGVzdCAoZG8g'
'dHJlbiAyMDI2LTA5LTMwajogYWN0aW9ubGludCBnaWEKICAgICMgcmM9MSA9PiBtdWMgMCBpbSBsYW5nLCB0MzMgImxhIiku'
'IEJhbiBUSEFUIDEuNi4yNy8xLjcuNy8xLjcuOC8xLjcuMTIgZGV1IHJjPTAgdmEgZGV1IGNobyB0MzMvdDEzNy90MTU5IFFV'
'QSB0cmVuIDBlYTk1ZGUuCiAgICAjIGJhc2ggcXVhIGB3aGljaGAgQ0hJIGhvaSBDTyBNQVQsIGNvIGNodSBkaWNoOiB0MzUt'
'dDQwIGdvaSBgYmFzaGAgVFJBTiAoYmFzaCBXU0wgbGFtIGNodW5nIERPLCBkZXUgTkdPQUlfUEhBTV9WSSDigJQgZG8gdHJl'
'bgogICAgIyAyMDI2LTA5LTMwaikuIDkgY2EgVFJPTkcgcGhhbSB2aSBLSE9ORyBnb2kgYmFzaCBxdWEgYHdoaWNoYCDigJQg'
'eGVtIGNob3QgYF9iYXNoX3Bvc2l4KClgIGR1b2kgY2hvdCBnaXQuCiAgICAjIENIQVkgRFVPQyBjaHVhIHBoYWkgRFVORyBE'
'VU9DOiBkbyB0cmVuIDIwMjYtMDktMzBrLCAwZWE5NWRlLCBhY3Rpb25saW50IFRIQVQgMS40LjMvMS41LjAvMS41LjMvMS42'
'LjAvMS42LjgvMS42LjE1LzEuNi4yMC8KICAgICMgMS42LjIyIGRldSBgLXZlcnNpb25gIHJjPTAsIG1hIGNhIHRhbSBsYW0g'
'dDEzNy90MTU5IERPIChgcHJvcGVydHkgInJ1bl9hdHRlbXB0Ii8id29ya2Zsb3dfc2hhIiBpcyBub3QgZGVmaW5lZGApLCAx'
'LjQuMy8xLjUuMAogICAgIyB0aGVtIHQzMyAoYG11c3QgYmUgY29udGFpbmVkIHdpdGhpbiAke3sgfX1gKSDigJQgZTJlIDEu'
'Ni4yMjogcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0MTM3JywgJ3QxNTknXWAgY2hvIHVuZyB2aWVuCiAgICAj'
'IHNhY2g7IDEuNi4yMy8xLjYuMjQvMS42LjI2LzEuNi4yNy8xLjcuMC8xLjcuNi8xLjcuNy8xLjcuMTIgUVVBIGNhIGJhLiBT'
'YW4gbGEgYmFuCiAgICAjIGdoaW0gQ0kgKEFMX1NBTiksIEtIT05HIHBoYWkgMS42LjIzIGRvIHRyZW4gTU9UIHVuZyB2aWVu'
'OiB3b3JrZmxvdyBjdWEgdW5nIHZpZW4gc2F1IGNvIHRoZSBkdW5nIGN1IHBoYXAgbW9pIGhvbiwgbWEgQ0kgY2hpIGRvCiAg'
'ICAjIGJhbmcgYmFuIGdoaW0uIEN1IGhvbiBzYW4gPT4gS0hPTkcgRE8gRFVPQyAoY2hhbiBjYSAxLjYuMjMtMS43LjYgZGFu'
'ZyBRVUE6IGZhaWwtY2xvc2UsIGtob25nIHBoYWkgcGhhbiBxdXlldCkuIGB2YCBkYXU6IGJhbgogICAgIyBgZ28gaW5zdGFs'
'bGAgaW4gYHYxLjcuN2A7IGtob25nIGRvYyBkdW9jIHNvICh2ZC4gYChkZXZlbClgKSA9PiBLSE9ORyBETyBEVU9DLgogICAg'
'aWYgbm90IF90aGlldV9jYzoKICAgICAgICBfYWwgPSBzdWJwcm9jZXNzLnJ1bihbX2NjWyJhY3Rpb25saW50Il0sICItdmVy'
'c2lvbiJdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsIGVuY29kaW5nPSJ1dGYtOCIsCiAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD02MCkKICAgICAgICBfYWxfdiA9IHJlLnNlYXJjaChy'
'Iig/bSledj8oXGQrKVwuKFxkKylcLihcZCspIiwgX2FsLnN0ZG91dCBvciAiIikKICAgICAgICBpZiBfYWwucmV0dXJuY29k'
'ZToKICAgICAgICAgICAgbG9pLmFwcGVuZCgiYWN0aW9ubGludCB0cmVuIFBBVEggY28gbWF0IG5odW5nIGBhY3Rpb25saW50'
'IC12ZXJzaW9uYCByYyE9MCAoa2hvbmcgY2hheSBkdW9jKTogY2FpIGxhaSBiYW4gZ2hpbSBBTF9WRVIiKQogICAgICAgIGVs'
'aWYgbm90IF9hbF92IG9yIHR1cGxlKGludCh4KSBmb3IgeCBpbiBfYWxfdi5ncm91cHMoKSkgPCBBTF9TQU46CiAgICAgICAg'
'ICAgIGxvaS5hcHBlbmQoZiJhY3Rpb25saW50IHtfYWxfdi5ncm91cCgwKSBpZiBfYWxfdiBlbHNlICcoa2hvbmcgZG9jIGR1'
'b2MgcGhpZW4gYmFuKSd9IGN1IGhvbiBiYW4gZ2hpbSBDSSAiCiAgICAgICAgICAgICAgICAgICAgICAgZiJ7Jy4nLmpvaW4o'
'bWFwKHN0ciwgQUxfU0FOKSl9IChBTF9WRVIpOiBiYW4gY3UgbGFtIHQxMzcvdDE1OSBETyAnbGEnIHRyZW4gdW5nIHZpZW4g'
'c2FjaCDigJQiCiAgICAgICAgICAgICAgICAgICAgICAgIiBjYWkgYmFuIGdoaW0gKG9wcy9jYWlfYWN0aW9ubGludC5zaCB2'
'b2kgQUxfVkVSKSIpCiAgICAgICAgIyBnaXQgY3VuZyB0aGU6IENPIE1BVCBraG9uZyBwaGFpIERVTkcgRFVPQywgdmEgZ2l0'
'IENVIGxhIGNvbmcgY3UgUEhPIEJJRU4gbmhhdCB0cm9uZyBib24uIERvIHRyZW4gMjAyNi0wOS0zMGwsIDBlYTk1ZGUsIGdp'
'dAogICAgICAgICMgVEhBVCBxdWEgY3VuZyBjaGF5KCk6IDIuMjUuMSA9PiAxNDAvMTY2ICgyMyBjYSAibGEiOiBgaW5pdCAt'
'YmAuLi4pLCAyLjM0LjEgdmEgMi4zNS4xID0+IDE2My8xNjYgKHQxMDkgdDExMCB0MTExOiBgZ2l0CiAgICAgICAgIyB3b3Jr'
'dHJlZSBsaXN0IC0tcG9yY2VsYWluIC16YCByYz0xMjkgYHVua25vd24gc3dpdGNoIHpgKSwgZTJlIDIuMzUuMSByYz0xIGBE'
'QVQgMTEgfCBUUlVPVCAxYDsgMi4zNi4xID0+IDE2Ni8xNjYuIFNhbiBsYXkKICAgICAgICAjIHR1IHRpbmggbmFuZyBtYSBD'
'SElOSCBtYSBkdW9jIGRvIGdvaSAob3BzL2NvbmdfY3UueWFtbCBkZSBiYW5fZ2hpbSBnaXQgPSBudWxsIG5lbiBraG9uZyBj'
'byBiYW4gZ2hpbSBDSSBkZSBkdWEgdmFvKS4KICAgICAgICAjIGBnaXQgdmVyc2lvbiAyLjQ3LjEud2luZG93cy4xYCAoR2l0'
'IGZvciBXaW5kb3dzKSB2YSBgMi4zOS4zIChBcHBsZSBHaXQtMTQ2KWAgZGV1IGRvYyBkdW9jIGJhIHNvIGRhdS4KICAgICAg'
'ICAjIFZhIHBoYWkgaG9pIERVTkcgZ2l0IG1hIGJvIHRlc3QgU0UgR09JLiBCbyB0ZXN0IEtIT05HIGBzaHV0aWwud2hpY2go'
'ImdpdCIpYCBuaHUgYmEgY29uZyBjdSB0cmVuOiBHT0lfR0lUIGN1YSB1bmcgdmllbiB2YSBtb2kKICAgICAgICAjIGZpeHR1'
'cmUgZ29pIGBnaXRgIFRSQU4g4oCUIHRyZW4gV2luZG93cyBsYSBDcmVhdGVQcm9jZXNzVzogQ0hJIHR1IHRoZW0gYC5leGVg'
'IChLSE9ORyBQQVRIRVhUKSwgdHJhIHRodSBtdWMgcHl0aG9uLmV4ZSwgY3dkCiAgICAgICAgIyB2YSBTeXN0ZW0zMiBUUlVP'
'QyBQQVRILiBgd2hpY2hgIHRoaSB0cmEgUEFUSEVYVCwgbmVuIG1vdCBgZ2l0LmNtZGAvYGdpdC5iYXRgIGR1bmcgdHJ1b2Mg'
'YGdpdC5leGVgIENVIHRyZW4gUEFUSCBkdW9jIGhvaQogICAgICAgICMgVEhBWSBubyDigJQgZG8gdHJlbiAyMDI2LTEwLTAx'
'IChuaGFuaCB3aW4zMiBUSEFUIGN1YSBzaHV0aWwud2hpY2g7IHNoaW0gYGdpdC5DTURgIG1vaSB0cnVvYyBnaXQgMi4zNS4x'
'IFRIQVQpOiBiYW4gMzBtIG11YyAwCiAgICAgICAgIyBpbSwgZTJlIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgLCBgbGE6IFsn'
'dDEwOScsICd0MTEwJywgJ3QxMTEnXWAuIE5lbiBob2kgYmFuZyBDSElOSCBkdW9uZyBheTogdGllbiB0cmluaCBjb24gY3Vh'
'IGNoYXkoKQogICAgICAgICMgKGN1bmcgcHl0aG9uLCBjdW5nIG1vaSB0cnVvbmcsIGN3ZCA9IGdvYyBuaHUgYm8gdGVzdCkg'
'Z29pIGBnaXQgLS12ZXJzaW9uYCBUUkFOLgogICAgICAgIF9yY19ndiwgX3JhX2d2ID0gY2hheShbIi1jIiwgImltcG9ydCBz'
'dWJwcm9jZXNzLCBzeXM7IHAgPSBzdWJwcm9jZXNzLnJ1bihbJ2dpdCcsICctLXZlcnNpb24nXSwgY2FwdHVyZV9vdXRwdXQ9'
'VHJ1ZSwiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiIHRleHQ9VHJ1ZSwgdGltZW91dD02MCk7IHBy'
'aW50KHAuc3Rkb3V0KTsgc3lzLmV4aXQocC5yZXR1cm5jb2RlKSJdLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBn'
'b2MgaWYgZ29jLmlzX2RpcigpIGVsc2UgUGF0aC5jd2QoKSwgcGh1dD0yKQogICAgICAgIF9ndl9tID0gcmUuc2VhcmNoKHIi'
'KD9tKV5naXQgdmVyc2lvblxzKyhcZCspXC4oXGQrKVwuKFxkKykiLCBfcmFfZ3YpCiAgICAgICAgZ2hpKCJnaXRfYm9fdGVz'
'dCIsIF9ndl9tLmdyb3VwKDApIGlmIF9ndl9tIGVsc2UgTm9uZSkKICAgICAgICBpbm4oIiAgZ2l0IGJvIHRlc3QgIDoiLCBf'
'Z3ZfbS5ncm91cCgwKSBpZiBfZ3ZfbSBlbHNlIGYiKGtob25nIGRvYyBkdW9jIHBoaWVuIGJhbiwgcmM9e19yY19ndn0pIikK'
'ICAgICAgICBpZiBfcmNfZ3Y6CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJgZ2l0IC0tdmVyc2lvbmAgZ29pIFRSQU4gbmh1'
'IGJvIHRlc3QgcmMhPTAgKHsoX3JhX2d2LnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10pWy0xXVs6OTBdfSk6IGNhaSBs'
'YWkgZ2l0IikKICAgICAgICBlbGlmIG5vdCBfZ3ZfbSBvciB0dXBsZShpbnQoeCkgZm9yIHggaW4gX2d2X20uZ3JvdXBzKCkp'
'IDwgR0lUX1NBTjoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImdpdCB7Jy4nLmpvaW4oX2d2X20uZ3JvdXBzKCkpIGlmIF9n'
'dl9tIGVsc2UgJyhraG9uZyBkb2MgZHVvYyBwaGllbiBiYW4pJ30gY3UgaG9uICIKICAgICAgICAgICAgICAgICAgICAgICBm'
'InsnLicuam9pbihtYXAoc3RyLCBHSVRfU0FOKSl9ICh1bmcgdmllbiBnb2kgYGdpdCB3b3JrdHJlZSBsaXN0IC0tcG9yY2Vs'
'YWluIC16YCk6IGNhcCBuaGF0IGdpdCIpCiAgICAgICAgIyBiYXNoIGN1bmcgSE9JIFNBSSBDSE8gbmh1IGdpdDogOSBjYSBU'
'Uk9ORyBwaGFtIHZpICh0MzIgdDUxIHQ1OSB0NjAgdDYyIHQ2MyB0NjYgdDY4IHQxNTIpIGNoYXkgYmFzaCBiYW5nIGBfYmFz'
'aF9wb3NpeCgpYAogICAgICAgICMgY3VhIHVuZyB2aWVuIOKAlCBHaXQgQmFzaCBvIGR1b25nIENPIERJTkggYEM6XFByb2dy'
'YW0gRmlsZXNcR2l0XGJpblxiYXNoLmV4ZWAgKHZhIGAoeDg2KWAsIGB1c3JcYmluYCksIHJvaQogICAgICAgICMgYHdoaWNo'
'KCJiYXNoIilgIE5IVU5HIGxvYWkga2V0IHF1YSB0cm9uZyBTeXN0ZW0zMiAoV1NMKTsga2hvbmcgdGhheSB0aGkgdHJhICIi'
'LiBNYXkgY28gV1NMIG1hIEdpdCBraG9uZyBvIFByb2dyYW0gRmlsZXMKICAgICAgICAjIChNaW5HaXQgZG8gQ0hJTkggcHMx'
'IHR1IHRhaSDigJQgTWluR2l0IEtIT05HIGNvIGJhc2g7IHNjb29wOyBjYWkgcGVyLXVzZXIpIHF1YSBjaG90IGB3aGljaGAg'
'byB0cmVuLCByb2kgYF9iYXNoX3Bvc2l4KClgCiAgICAgICAgIyA9PSAiIjogdDMyICJLSE9ORyBETyBEVU9DIiArIDggY2Eg'
'ImxhIiBgc3VicHJvY2Vzcy5ydW4oWyIiLi4uXSlgLCBjaGkgbG8gcmEgU0FVIGNhIGhhaSBsdW90IGJvIHRlc3QuIERvIHRy'
'ZW4gMjAyNi0xMC0wMToKICAgICAgICAjIGhhbSBUSEFULCBuaGFuaCBvcy5uYW1lPSdudCcgKFdTTCArIE1pbkdpdC9zY29v'
'cC9wZXItdXNlcikgPT4gJyc7IGJvIHRlc3Qgdm9pIGdpYSB0cmkgYXkgMTU3LzE2NjsgZTJlICh3aW4zMiBnaWEpIHJjPTMK'
'ICAgICAgICAjIHNhdSAzNDcgcywgYFRSVU9UIE1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jICBsYTogWyd0NTEnLCAn'
'dDU5JywgJ3Q2MCcsICd0NjInLCAndDYzJywgJ3Q2NicsICd0NjgnLCAndDE1MiddYC4gUGhlcAogICAgICAgICMgZG8gMzBq'
'IGNoYXkgdHJlbiBMaW51eCwgbm9pIGBfYmFzaF9wb3NpeCgpYCBsdW9uIHRyYSAiYmFzaCIsIG5lbiBraG9uZyB0aGUgdGhh'
'eSBkdW9uZyBuYXkuCiAgICAgICAgIyBWYSBgZ2l0YCBUUk9ORyBiYXNoIGF5IGxhIGdpdCBUSFUgQkE6IGBHaXRcYmluXGJh'
'c2guZXhlYCBsYSBjb21wYXQtYmFzaCBjdWEgZ2l0LXdyYXBwZXIsIGBzZXR1cF9lbnZpcm9ubWVudCgpYCBkYXkKICAgICAg'
'ICAjIGA8Z29jIEdpdD5cbWluZ3c2NFxiaW47PGdvYyBHaXQ+XHVzclxiaW5gIGxlbiBEQVUgUEFUSCAoZ2l0LWZvci13aW5k'
'b3dzL01JTkdXLXBhY2thZ2VzOiBnaXQtd3JhcHBlci5jICsgY29tcGF0LWJhc2gucmMsCiAgICAgICAgIyBraG9uZyBjbyBN'
'SU5JTUFMX1BBVEgpIOKAlCB0dWMgZ2l0IERJIEtFTSBiYW4gR2l0IGF5LCBLSE9ORyBwaGFpIGdpdCBUUkFOIGRhIGhvaSBv'
'IHRyZW4uIHQxNTIgY2hheSBHSVRfQ09ORklHX0NPVU5UIChnaXQKICAgICAgICAjIDIuMzEpIHRyb25nIGJhc2ggYXkuIERv'
'IHRyZW4gMjAyNi0xMC0wMSAoYmFzaCBib2MgZGF5IGdpdCBkaSBrZW0gbGVuIGRhdSBQQVRILCBnaXQgVFJBTiAyLjQzKTog'
'Z2l0IGRpIGtlbSAyLjMwLjIgVEhBVCA9PgogICAgICAgICMgMTY1LzE2NiwgZTJlIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFg'
'LCBgbGE6IFsndDE1MiddYCBjaG8gdW5nIHZpZW4gc2FjaDsgMi4zMS4wIFRIQVQgPT4gMTY2LzE2Ni4gSG9pIENISU5IIGhh'
'bSBheSB2YQogICAgICAgICMgQ0hJTkggYmFzaCBheSB0cm9uZyB0aWVuIHRyaW5oIGNvbiBjdWEgY2hheSgpIChjdW5nIHB5'
'dGhvbiwgY3VuZyBtb2kgdHJ1b25nLCBjd2QgPSBnb2MpOyB1bmcgdmllbiBraG9uZyBjbyBoYW0gdGhpIGtob25nCiAgICAg'
'ICAgIyBob2kgKGdpdSBjaG90IENPIE1BVCkuCiAgICAgICAgIyBEb2MgZG9uZyBgZ2l0IHZlcnNpb25gIENVT0kgY3VhIHN0'
'ZG91dCwgS0hPTkcgZG9jIGRvbmcgREFVIChiYW4gMDFiOiBCQVNIX0VOViBgZWNob2AgbW90IGRvbmcgPT4gbXVjIDAgS0RE'
'IG9hbjsgdHUgYmFuIDAxZQogICAgICAgICMgY2hheSgpIGJvIEJBU0hfRU5WLCBjYWNoIGRvYyBuYXkgZ2l1IGxhaSB2aSB2'
'byBoYWkpLiBCYXNoIHRyZW8gdGhpIGJhdCBuZ29haSBsZSBUUk9ORyBjb24gKGJhbiAwMWIgZG8gbG9pIGNobwogICAgICAg'
'ICMgYF9iYXNoX3Bvc2l4KClgKSB2YSBEVU5HIGx1b24gKGtob25nIGhvaSBsYW4gaGFpOiBnaXUgdHJhbiA2MCBzIHZhIG1v'
'dCB0aWVuIHRyaW5oIG1vIGNvaSBuaHUgYmFuIDAxYykuCiAgICAgICAgIyBWYSBob2kgSEFJIGxhbiwgZHVuZyBIQUkgbW9p'
'IHRydW9uZyBibyB0ZXN0IFRIQVQgZHVuZzogMyBsb2kgZ29pIGBfYmFzaF9wb3NpeCgpYCBjdWEgdW5nIHZpZW4gY2hheSBi'
'YXNoIHZvaSAyIG1vaSB0cnVvbmcg4oCUCiAgICAgICAgIyB0MzIvdDUxLXQ2OCBgZGljdChvcy5lbnZpcm9uLCAuLi4pYCAo'
'bW9pIHRydW9uZyBjdWEgY2hheSgpKSwgY29uIHQxNTIgKGNhIERVWSBOSEFUIGNhbiBzYW4gMi4zMSkKICAgICAgICAjIGBk'
'aWN0KFBBVEg9b3MuZW52aXJvblsiUEFUSCJdLCBUTF8qLCBHSVRfQ09ORklHXyopYC4gQmFuIDAxYyBob2kgbyBtb2kgdHJ1'
'b25nIFRIVSBOSEFUIHJvaSBhcCBzYW4gY3VhIHQxNTIg4oCUIGRvIHRyZW4KICAgICAgICAjIDIwMjYtMTAtMDE6IGdpdCBk'
'aSBrZW0gMi4zMC4yIFRIQVQgKyBCQVNIX0VOViBkYXkgZ2l0IDIuNDMgbGVuIGRhdSBQQVRIID0+IG11YyAwIHRoYXkgMi40'
'MywgZTJlIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgLAogICAgICAgICMgYGxhOiBbJ3QxNTInXWAgY2hvIHVuZyB2aWVuIHNh'
'Y2guIFR1IGJhbiAwMWUgY2hheSgpIGJvIEJBU0hfRU5WIG5lbiBkdW9uZyBheSBkb25nIG8gR09DOyBoYWkgbGFuIGhvaSBn'
'aXUgbGFpIHZpIGhhaSBtb2kKICAgICAgICAjIHRydW9uZyBWQU4ga2hhYyBuaGF1LiBMYW4gaG9pIG8gbW9pIHRydW9uZyB0'
'aHUgbmhhdCBDSEkgY2h1bmcgbWluaCBnaXQgQ0hBWSBkdW9jIHRyb25nIGJhc2ggYXksIEtIT05HIGNodW5nIG1pbmggYmFz'
'aAogICAgICAgICMgImR1bmcgZHVvYyIgY2hvIHQzMi90NTEtdDY4IChkbzogbm9jbG9iYmVyIHF1YSBjYXUgaG9pIG5heSBt'
'YSBsYW0gNyBjYSBETyDigJQgdmkgdmF5IGNoYXkoKSBibyBiaWVuIGtob2kgZG9uZyBiYXNoLCB4ZW0KICAgICAgICAjIHRy'
'ZW4pLiBCQVNIX0dJVCA9IG1vaSB0cnVvbmcgdDMyL3Q1MS10NjggKGRvaSBDSEFZIGR1b2MpOyBCQVNIX0dJVF9UMTUyID0g'
'bW9pIHRydW9uZyB0MTUyIChkb2kgc2FuIEdJVF9TQU5fQkFTSCkuCiAgICAgICAgX3JjX2JwLCBfcmFfYnAgPSBjaGF5KFsi'
'LWMiLCAiaW1wb3J0IG9zLCBzdWJwcm9jZXNzLCBzeXNcbnN5cy5wYXRoLmluc2VydCgwLCAnb3BzJylcbmltcG9ydCBsZWFz'
'ZV9wdWJsaXNoX3Rlc3QgYXMgVFxuIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgImYgPSBnZXRhdHRy'
'KFQsICdfYmFzaF9wb3NpeCcsIE5vbmUpXG5iID0gJz8nIGlmIGYgaXMgTm9uZSBlbHNlIGYoKVxucHJpbnQoJ0JBU0hfUE9T'
'SVg9JyArIGIpXG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiaWYgYiBhbmQgYiAhPSAnPyc6XG4g'
'IGZvciBrIGluICgnQkFTSF9HSVQnLCAnQkFTSF9HSVRfVDE1MicpOlxuICAgIHRyeTpcbiIKICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICIgICAgICBwID0gc3VicHJvY2Vzcy5ydW4oW2IsICctLW5vcHJvZmlsZScsICctLW5vcmMn'
'LCAnLWMnLCAnZ2l0IC0tdmVyc2lvbiddLCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgY2FwdHVy'
'ZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLCB0aW1lb3V0PTYwLCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICIgZW52PU5vbmUgaWYgayA9PSAnQkFTSF9HSVQnIGVsc2UgeydQQVRIJzogb3MuZW52aXJvblsnUEFUSCddfSlcbiIK'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgICAgICB2ID0gW3ggZm9yIHggaW4gcC5zdGRvdXQuc3Bs'
'aXRsaW5lcygpIGlmIHguc3RhcnRzd2l0aCgnZ2l0IHZlcnNpb24nKV0iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAiIG9yIHAuc3Rkb3V0LnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ11cbiIKICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICIgICAgICBwcmludChrICsgJz0nICsgdlstMV0gKyAnIHJjPScgKyBzdHIocC5yZXR1cm5j'
'b2RlKSlcbiIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBl'
'OlxuICAgICAgcHJpbnQoayArICc9KCcgKyB0eXBlKGUpLl9fbmFtZV9fICsgJykgcmM9LTEnKVxuIgogICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgIiAgICAgIGJyZWFrXG4iXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'Z29jIGlmIGdvYy5pc19kaXIoKSBlbHNlIFBhdGguY3dkKCksIHBodXQ9MykKICAgICAgICBfYnBfbSA9IHJlLnNlYXJjaChy'
'Iig/bSleQkFTSF9QT1NJWD0oLiopJCIsIF9yYV9icCkKICAgICAgICBfYnAgPSBfYnBfbS5ncm91cCgxKS5zdHJpcCgpIGlm'
'IChfYnBfbSBhbmQgbm90IF9yY19icCkgZWxzZSBOb25lCiAgICAgICAgX2JnX20gPSByZS5zZWFyY2gociIoP20pXkJBU0hf'
'R0lUPWdpdCB2ZXJzaW9uXHMrKFxkKylcLihcZCspXC4oXGQrKVteXG5dKlxzcmM9MCQiLCBfcmFfYnApCiAgICAgICAgX2J0'
'X20gPSByZS5zZWFyY2gociIoP20pXkJBU0hfR0lUX1QxNTI9Z2l0IHZlcnNpb25ccysoXGQrKVwuKFxkKylcLihcZCspW15c'
'bl0qXHNyYz0wJCIsIF9yYV9icCkKICAgICAgICBnaGkoImJhc2hfYm9fdGVzdCIsIF9icCk7IGdoaSgiZ2l0X3Ryb25nX2Jh'
'c2hfYm9fdGVzdCIsIF9iZ19tLmdyb3VwKDApWzk6XSBpZiBfYmdfbSBlbHNlIE5vbmUpCiAgICAgICAgZ2hpKCJnaXRfdHJv'
'bmdfYmFzaF90MTUyIiwgX2J0X20uZ3JvdXAoMClbMTQ6XSBpZiBfYnRfbSBlbHNlIE5vbmUpCiAgICAgICAgaW5uKCIgIGJh'
'c2ggYm8gdGVzdCA6IiwgcmVwcihfYnApIGlmIF9icCBpcyBub3QgTm9uZSBlbHNlIGYiKGtob25nIGhvaSBkdW9jLCByYz17'
'X3JjX2JwfSkiLAogICAgICAgICAgICAifCBnaXQgdHJvbmcgYmFzaDoiLCBfYmdfbS5ncm91cCgwKVs5Ol0gaWYgX2JnX20g'
'ZWxzZSAiKGtob25nIGRvYyBkdW9jKSIsCiAgICAgICAgICAgICJ8IG1vaSB0cnVvbmcgdDE1MjoiLCBfYnRfbS5ncm91cCgw'
'KVsxNDpdIGlmIF9idF9tIGVsc2UgIihraG9uZyBkb2MgZHVvYykiKQogICAgICAgIGlmIF9icCBpcyBOb25lOgogICAgICAg'
'ICAgICBsb2kuYXBwZW5kKGYia2hvbmcgaG9pIGR1b2MgYF9iYXNoX3Bvc2l4KClgIGN1YSBibyB0ZXN0IChyYz17X3JjX2Jw'
'fToiCiAgICAgICAgICAgICAgICAgICAgICAgZiIgeyhfcmFfYnAuc3RyaXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFd'
'Wzo5MF19KSIpCiAgICAgICAgZWxpZiBub3QgX2JwOgogICAgICAgICAgICBsb2kuYXBwZW5kKGYiYF9iYXNoX3Bvc2l4KClg'
'IGN1YSBibyB0ZXN0IEtIT05HIHRoYXkgYmFzaCBQT1NJWCAoYHdoaWNoYDoge19jY1snYmFzaCddfTsgU3lzdGVtMzIgPSBX'
'U0wgYmkgbG9haSk6IgogICAgICAgICAgICAgICAgICAgICAgICIgY2FpIEdpdCBmb3IgV2luZG93cyB2YW8gQzpcXFByb2dy'
'YW0gRmlsZXNcXEdpdCwgaG9hYyBkYXQgdGh1IG11YyBHaXRcXGJpbiBsZW4gREFVIFBBVEggKHRydW9jIFN5c3RlbTMyKSIp'
'CiAgICAgICAgZWxpZiBfYnAgIT0gIj8iIGFuZCBub3QgKF9iZ19tIGFuZCBfYnRfbSk6CiAgICAgICAgICAgIF9kb25nX2Jn'
'ID0gW3hbOjkwXSBmb3IgeCBpbiByZS5maW5kYWxsKHIiKD9tKV4oQkFTSF9HSVQoPzpfVDE1Mik/PS4qKSQiLCBfcmFfYnAp'
'XSBvciBbIihraG9uZyBjbyBkb25nIEJBU0hfR0lUKSJdCiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJgZ2l0IC0tdmVyc2lv'
'bmAgVFJPTkcgYmFzaCBjdWEgYm8gdGVzdCAoe19icH0pIGtob25nIGNoYXkva2hvbmcgZG9jIGR1b2MgcGhpZW4gYmFuOiB7'
'JyB8ICcuam9pbihfZG9uZ19iZyl9IikKICAgICAgICBlbGlmIF9icCAhPSAiPyIgYW5kIHR1cGxlKGludCh4KSBmb3IgeCBp'
'biBfYnRfbS5ncm91cHMoKSkgPCBHSVRfU0FOX0JBU0g6CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJnaXQgeycuJy5qb2lu'
'KF9idF9tLmdyb3VwcygpKX0gVFJPTkcgYmFzaCBjdWEgYm8gdGVzdCAoe19icH07IG1vaSB0cnVvbmcgdDE1MjogY2hpIFBB'
'VEgsIGtob25nIEJBU0hfRU5WKSBjdSIKICAgICAgICAgICAgICAgICAgICAgICBmIiBob24geycuJy5qb2luKG1hcChzdHIs'
'IEdJVF9TQU5fQkFTSCkpfSAodDE1MiBkdW5nIEdJVF9DT05GSUdfQ09VTlQpOiBjYXAgbmhhdCBiYW4gR2l0IGNodWEgYmFz'
'aCBheSIpCgpyYywgaGVhZCwgXyA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAiSEVBRCIpCmlmIHJjOiBsb2kuYXBwZW5kKCJr'
'aG9uZyBkb2MgZHVvYyBIRUFEIikKZ2hpKCJoZWFkIiwgaGVhZCkKcmNfYSwgXywgXyA9IGdpdChnb2MsICJtZXJnZS1iYXNl'
'IiwgIi0taXMtYW5jZXN0b3IiLCBTSEFfRzEsIGhlYWQgb3IgIkhFQUQiKQpsYV9oYXVfZHVlID0gKHJjX2EgPT0gMCkKaWYg'
'aGVhZCA9PSBTSEFfRzE6CiAgICB0aGVfaGUgPSAiZzEiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IERBWSBMQSBn'
'MS4gQ0hVQSBjbyBiYW4gdmEgZzI7IGtldCBxdWEgZHVvaSBsYSBORU4gRE8uIikKZWxpZiBsYV9oYXVfZHVlOgogICAgdGhl'
'X2hlID0gImcyIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBoYXUgZHVlIGN1YSBnMSAoe1NIQV9HMVs6OF19KTsg'
'dW5nIHZpZW4gZzIgaGF5IGtob25nOiBONycgKG11YyAxKSBkaW5oIGRhbmguIikKZWxzZToKICAgIHRoZV9oZSA9ICI/Ijsg'
'bG9pLmFwcGVuZChmIkhFQUQ9e2hlYWRbOjhdfSBLSE9ORyBwaGFpIGcxIHZhIEtIT05HIHBoYWkgaGF1IGR1ZSBjdWEge1NI'
'QV9HMVs6OF19IOKAlCByZWJhc2U/IG5oYW0gbmhhbmg/IikKZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCnJjX3IsIHJlZnMsIF8g'
'PSBnaXQoZ29jLCAiZm9yLWVhY2gtcmVmIiwgIi0tcG9pbnRzLWF0IiwgaGVhZCBvciAiSEVBRCIsCiAgICAgICAgICAgICAg'
'ICAgICAgIi0tZm9ybWF0PSUocmVmbmFtZTpzaG9ydCkiKQpkc3IgPSBbeCBmb3IgeCBpbiByZWZzLnNwbGl0bGluZXMoKSBp'
'ZiB4LnN0cmlwKCkgYW5kIHguc3RyaXAoKSAhPSAiZG8tdGFtIl0KZ2hpKCJyZWZfdHJvX3RvaV9oZWFkIiwgZHNyKQppbm4o'
'ZiIgIHJlZiB0cm8gdG9pIEhFQUQ6IHsnLCAnLmpvaW4oZHNyKSBpZiBkc3IgZWxzZSAnKGtob25nIHJlZiBuYW8gLSBIRUFE'
'IHJvaSB0dSBkbyknfSIpCgppZiBsb2k6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IG5lbiBkbyBzYWksIEtI'
'T05HIGluIGtldCBsdWFuIG5hby4iKQogICAgZm9yIHggaW4gbG9pOiBpbm4oIiAgLSIsIHgpCiAgICBzeXMuZXhpdCgzKQoK'
'IyAtLS0tLS0tLS0tLS0tLS0tIDEuIGtpY2ggdGh1b2MgKE43JyBjdWEgc3BlYyByMykgLS0tLS0tLS0tLS0tLS0tLQppbm4o'
'IiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjEuIEtJQ0ggVEhVT0Mg4oCUIHRyYW4gc3BlYyByMzogPD0gMiB0ZXAgdmEgPD0g'
'NDAwIGRvbmcgdGhlbSIpCiMgVkUgTkVOIFBIQUkgVFVPSSDigJQgdmEgcGhhaSBDSFVORyBNSU5IIGR1b2MgbGEgdHVvaSwg'
'a2hvbmcgcGhhaSBnaWEgZGluaC4KIyBCYWkgaG9jIHRyYSBnaWEgMTktMDktMjAyNjogY2xvbmUgdGFpIGR1bmcgY2hpIGZl'
'dGNoIG5oYW5oIGJhbiB2YSwgYG9yaWdpbi9tYXN0ZXJgCiMgZHVuZyB5ZW4gdHUgMTQtMDkgKGMxNmJkMzIsIHNhdSA5NyBj'
'b21taXQpLiBtZXJnZS1iYXNlIHJvaSB2ZSBkdW5nIGRpbmggbWFzdGVyIGN1LAojIG5lbiBkaWZmIE5VT1QgY2EgOTcgY29t'
'bWl0IG1hc3RlcjogZG8gcmEgNDYgdGVwIC8gKzcxMTggdGhheSB2aSAyIHRlcCAvICszOTcg4oCUCiMgQ1VORyBNT1QgQ09N'
'TUlUIDBlYTk1ZGUuIE1vdCB0aWV1IGNoaSBERUxUQSBtYSB2ZSBuZW4ga2hvbmcgdHVvaSB0aGkga2hvbmcgc2FpCiMgbGVj'
'aCBtb3QgY2h1dCwgbm8gc2FpIGNhIG1vdCBiYWMgZG8gbG9uLgojIENobyBuZW46IG5lbiBraG9uZyBjaHVuZyBtaW5oIGR1'
'b2MgbGEgdHVvaSA9PiBLSE9ORyBETyBEVU9DIChyYz0zKSwgS0hPTkcgcGhhaSBUUlVPVC4KIyBUUlVPVCBsYSBtb3QgUEhB'
'TiBRVVlFVCB2ZSBiYW4gdmE7IHBoYW4gcXV5ZXQgY2hpIGR1b2MgcGhlcCBwaGF0IHJhIGtoaSBkYSBkbyBkdW9jLgplciA9'
'ICIiCnJjX3UsIHVybF90aG8sIF8gPSBnaXQoZ29jLCAicmVtb3RlIiwgImdldC11cmwiLCAib3JpZ2luIikKdXJsX28sIHVy'
'bF9pbiA9IF91cmxfc2FjaCh1cmxfdGhvKSwgX3VybF9pbih1cmxfdGhvKQpnaGkoIm9yaWdpbl91cmwiLCB1cmxfaW4pOyBp'
'bm4oZiIgIG9yaWdpbiAgICAgICA6IHt1cmxfaW4gb3IgJyhraG9uZyBkb2MgZHVvYyknfSIpCnVybF9vayA9IChub3QgcmNf'
'dSkgYW5kIHVybF9vLnJzdHJpcCgiLyIpIGluIFVSTF9LSE9fSE9QX0xFCnJjX2xyLCBvdXRfbHIsIGVyX2xyID0gZ2l0KGdv'
'YywgImxzLXJlbW90ZSIsICJvcmlnaW4iLCAicmVmcy9oZWFkcy9tYXN0ZXIiKSBpZiB1cmxfb2sgZWxzZSAoMSwgIiIsICIi'
'KQplcl9sciA9IF9hbl91c2VyaW5mbyhlcl9scikKcmNfbG0sIGxtLCBlcl9sbSAgICAgPSBnaXQoZ29jLCAicmV2LXBhcnNl'
'IiwgIm9yaWdpbi9tYXN0ZXIiKQpybSA9IG91dF9sci5zcGxpdCgpWzBdIGlmIChub3QgcmNfbHIgYW5kIG91dF9sci5zdHJp'
'cCgpKSBlbHNlICIiCmlmIG5vdCB1cmxfb2s6CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmIm9yaWdpbj17dXJs'
'X2luIXJ9IEtIT05HIHBoYWkga2hvIHRoYXQg4oCUICd0dW9pJyBzbyB2b2kgbm8ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGdp'
'IikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbm90IHJtOgogICAga2V0KCJONycga2ljaCB0'
'aHVvYyIsIEtERCwKICAgICAgICBmImtob25nIGhvaSBkdW9jIG1hc3RlciB0cmVuIHJlbW90ZSAobHMtcmVtb3RlIHJjPXty'
'Y19scn0pOiB7ZXJfbHJbOjYwXX0gIgogICAgICAgIGYi4oCUIGtob25nIGNodW5nIG1pbmggZHVvYyB2ZSBuZW4gY29uIHR1'
'b2kiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiByY19sbSBvciBub3QgbG06CiAgICBrZXQo'
'Ik43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25nIGRvYyBkdW9jIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmU6IHtlcl9s'
'bVs6NjBdfSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIGxtICE9IHJtOgogICAgIyBEZW0g'
'eGVtIHR1dCBsYWkgYmFvIHhhLCBuZXUgZGVtIGR1b2Mg4oCUIGNvbiBzbyBuYXkgbm9pIHJvIG11YyBkbyBzYWkgbGVjaC4K'
'ICAgIHJjX2MsIHNhdSwgXyA9IGdpdChnb2MsICJyZXYtbGlzdCIsICItLWNvdW50IiwgZiJ7bG19Li57cm19IikKICAgIHhh'
'ID0gZiIsIHR1dCBsYWkge3NhdX0gY29tbWl0IiBpZiAobm90IHJjX2MgYW5kIHNhdS5zdHJpcCgpLmlzZGlnaXQoKSkgZWxz'
'ZSAiIgogICAgaW5uKGYiICBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25lIDoge2xtWzoxMl19IikKICAgIGlubihmIiAgbWFz'
'dGVyIHRyZW4gcmVtb3RlICAgICAgICA6IHtybVs6MTJdfXt4YX0iKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdo'
'aSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwKICAgICAgICBmInZlIG5lbiBD'
'VTogb3JpZ2luL21hc3Rlcj17bG1bOjEyXX0gIT0gcmVtb3RlPXtybVs6MTJdfXt4YX0gIgogICAgICAgIGYi4oCUIGNoYXkg'
'YGdpdCAtQyA8a2hvPiBmZXRjaCBvcmlnaW4gbWFzdGVyYCByb2kgZG8gbGFpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0g'
'MSwgIiIsICIiLCAxCmVsc2U6CiAgICBpbm4oZiIgIHZlIG5lbiBUVU9JOiBvcmlnaW4vbWFzdGVyID0ge2xtWzoxMl19ID09'
'IG1hc3RlciB0cmVuIHJlbW90ZSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwg'
'cm0pCiAgICByY19tYiwgbWIsIGVyX21iID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAib3JpZ2luL21hc3RlciIsIGhlYWQp'
'CmlmIHJjX21iIG9yIG5vdCBtYjoKICAgIGlmIG1iID09ICIiIGFuZCBybSBhbmQgbG0gPT0gcm06CiAgICAgICAga2V0KCJO'
'Nycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyB0aW5oIGR1b2MgbWVyZ2UtYmFzZSB2b2kgb3JpZ2luL21hc3Rlcjoge2Vy'
'X21iWzo3MF19IikKICAgIG5zLCByYyA9ICIiLCAxCmVsc2U6CiAgICBnaGkoIm1lcmdlX2Jhc2UiLCBtYikKICAgIGlubihm'
'IiAgbWVyZ2UtYmFzZShvcmlnaW4vbWFzdGVyLCBIRUFEKSA9IHttYls6MTJdfSIpCiAgICBpZiBtYiAhPSBTSEFfQkFTRV9T'
'UEVDOgogICAgICAgIGlubihmIiAgTFVVIFk6IGtoYWMgYmFzZSBtYSBzcGVjIHIzIGtoYWkgKHtTSEFfQkFTRV9TUEVDWzox'
'Ml19KSDigJQgdmkgbmhhbmggZGEgbWVyZ2UgbWFzdGVyLiIpCiAgICAgICAgaW5uKCIgICAgICAgICBEbyBzbyBiYXNlIGN1'
'IHNlIE5VT1QgcGhhbiBtYXN0ZXIgbWFuZyB2YW8uIER1bmcgbWVyZ2UtYmFzZSBtb2kgbGEgdmllYyBjdWEgZXhlY3V0b3Iu'
'IikKICAgICAgICByY194LCBuc194LCBfID0gZ2l0KGdvYywgImRpZmYtdHJlZSIsICItciIsICItTSIsICItLWRpZmYtYWxn'
'b3JpdGhtPW15ZXJzIiwgIi0tbnVtc3RhdCIsIFNIQV9CQVNFX1NQRUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAg'
'ICAgICAgICAgIGggPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBuc194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAg'
'ICAgICAgICAgIGEgPSBzdW0oaW50KHhbMF0pIGZvciB4IGluIGggaWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdo'
'aSgibnVtc3RhdF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVwIjogbGVuKGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBpbm4o'
'ZiIgICAgICAgICAoZG9pIGNoaWV1OiBzbyBiYXNlIHNwZWMgPSB7bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkg'
'S0hPTkcgZHVuZyBkZSBjaGFtKSIpCiAgICAjIFBMVU1CSU5HLCBraG9uZyBQT1JDRUxBSU46IGBnaXQgZGlmZmAgZG9jIGNh'
'dSBoaW5oIFVJIENVQSBOR1VPSSBETyAoZGlmZi5hbGdvcml0aG0sIGRpZmYucmVuYW1lcywgZGlmZi5vcmRlckZpbGUsCiAg'
'ICAjIGNvbG9yLmRpZmYpLCB2YSBnaWEgdHJpIEhPUCBMRSBkb2kgbHVvbiBTTyBkb25nIG1hIHZhbiByYSBjaHUgc28g4oCU'
'IGRvIHRyZW4gMjAyNi0wOS0zMGk6IHVuZyB2aWVuIHRvbmcgaG9wIChteWVycyArNDAxKSA9PgogICAgIyBiYW4gMzBpIERB'
'VCAyIHRlcCAvICs0MDAgZHVvaSBgZGlmZi5hbGdvcml0aG0gPSBoaXN0b2dyYW1gIGhvYWMgYHBhdGllbmNlYCwgVFJVT1Qg'
'KzQwMSBraGkgbWFjIGRpbmg7IDEwLzc1IGNvbW1pdCBjaGFtCiAgICAjIHdyaXRlIHNldCBjbyBzbyBkb25nIGRvaSB0aGVv'
'IHRodWF0IHRvYW4uIGBkaWZmLXRyZWUgLXIgLU1gID0gbWFjIGRpbmggY3VhIGBnaXQgZGlmZmAgKHJlbmFtZXMgYmF0KSB2'
'YSBLSE9ORyBkb2MgY2FjIGtob2EKICAgICMgYXkuIFRodWF0IHRvYW4gcGhhaSBUVU9ORyBNSU5IOiBkaWZmLjxkcml2ZXI+'
'LmFsZ29yaXRobSAocXVhIGNvcmUuYXR0cmlidXRlc0ZpbGUgY3VhIG5ndW9pIGRvKSBWQU4gbG90IHZhbyBwbHVtYmluZyDi'
'gJQKICAgICMgZG8gdHJlbiAyMDI2LTA5LTMwaSwgYCoucHkgZGlmZj1hbGdgICsgZGlmZi5hbGcuYWxnb3JpdGhtPWhpc3Rv'
'Z3JhbTogZGlmZi10cmVlICs0MDEgY2hvIHVuZyB2aWVuIG15ZXJzICs0MDA7IGNvIHR1b25nIG1pbmgKICAgICMgdGhhbmcg'
'a2hvYSBheS4gYXR0cmlidXRlcyBgLWRpZmZgL2NvcmUuYmlnRmlsZVRocmVzaG9sZCB2YW4gYXAgPT4gYC1gID0+IEtIT05H'
'IERPIERVT0MgKGNob3QgZHVvaSkuCiAgICByYywgbnMsIGVyID0gZ2l0KGdvYywgImRpZmYtdHJlZSIsICItciIsICItTSIs'
'ICItLWRpZmYtYWxnb3JpdGhtPW15ZXJzIiwgIi0tbnVtc3RhdCIsIG1iLCBoZWFkKQppZiByYzoKICAgIHBhc3MKZWxzZToK'
'ICAgIGhhbmcgPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBucy5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAgdGhl'
'bSA9IHN1bShpbnQoaFswXSkgZm9yIGggaW4gaGFuZyBpZiBoWzBdLmlzZGlnaXQoKSkKICAgIHhvYSAgPSBzdW0oaW50KGhb'
'MV0pIGZvciBoIGluIGhhbmcgaWYgaFsxXS5pc2RpZ2l0KCkpCiAgICBnaGkoInNvX3RlcCIsIGxlbihoYW5nKSk7IGdoaSgi'
'ZG9uZ190aGVtIiwgdGhlbSk7IGdoaSgiZG9uZ194b2EiLCB4b2EpCiAgICBmb3IgaCBpbiBoYW5nOiBpbm4oZiIgICAge2hb'
'Ml06MzR9ICt7aFswXTo8NX0gLXtoWzFdfSIpCiAgICBpbm4oZiIgICAgVE9ORzoge2xlbihoYW5nKX0gdGVwLCAre3RoZW19'
'LCAte3hvYX0gICAodHJhbjoge1RSQU5fVEVQfSB0ZXAgLyB7VFJBTl9ET05HfSBkb25nIHRoZW0pIikKICAgIGNoYW0gPSBz'
'b3J0ZWQoe2hbMl0gZm9yIGggaW4gaGFuZ30gJiBXUklURV9TRVRfRzIpOyBnaGkoImNoYW1fd3JpdGVfc2V0IiwgY2hhbSkK'
'ICAgIGRlZiBfY2FfbW9pX2NvKHJldik6CiAgICAgICAgIyBjYXQtZmlsZSwga2hvbmcgYHNob3dgOiBgZ2l0IHNob3dgIGNo'
'ZXQgdm9pIGNhdSBoaW5oIFVJIGdvIHNhaSAoZG8gdHJlbiAyMDI2LTA5LTMwaTogbG9nLmRhdGUgZ28gc2FpID0+IGJhbiAz'
'MGkgZ29pCiAgICAgICAgIyAwZWE5NWRlIGxhICJraG9uZyBwaGFpIHVuZyB2aWVuIC4uLiBOb25lIOKAlCBkYSBsYW5kPyBu'
'aGFtIG5oYW5oPyIpLgogICAgICAgIHJfLCBuZF8sIF8gPSBnaXQoZ29jLCAiY2F0LWZpbGUiLCAiLXAiLCBmIntyZXZ9Om9w'
'cy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIHJldHVybiBOb25lIGlmIHJfIGVsc2Uge3QgZm9yIHQgaW4gQ0Ff'
'TU9JX0cyIGlmIHJlLnNlYXJjaChyIig/bSleZGVmICIgKyB0ICsgciJbYS16XT9fIiwgbmRfKX0KICAgIG9fbWIsIG9faCA9'
'IF9jYV9tb2lfY28obWIpLCBfY2FfbW9pX2NvKGhlYWQpCiAgICBtYW5nID0gc29ydGVkKG9faCAtIG9fbWIsIGtleT1zb19j'
'YSkgaWYgKG9fbWIgaXMgbm90IE5vbmUgYW5kIG9faCBpcyBub3QgTm9uZSkgZWxzZSBOb25lCiAgICBnaGkoImNhX21vaV9n'
'Ml9tYW5nX3ZhbyIsIG1hbmcpCiAgICBpZiBub3QgbWFuZzoKICAgICAgICAjIERvIFJPTkcgKGRhIGxhbmQsIGNoaW5oIG1h'
'c3RlciksIG5oYW0gbmhhbmgsIGhheSBuaGFuaCBjdWEgcGFja2V0IEtIQUMgY2hhbSBjdW5nIHRlcDoKICAgICAgICAjIGto'
'b25nIG1hbmcgY2EgbW9pIG5hbyBjdWEgZzIgdGhpIGtob25nIHBoYWkgdW5nIHZpZW4uIERvYyBraG9uZyBkdW9jIChOb25l'
'KSBjdW5nIHZheS4KICAgICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImRvaSB0dW9uZyBraG9uZyBwaGFpIHVu'
'ZyB2aWVuOiB7bGVuKGhhbmcpfSB0ZXAsIGNoYW0ge2NoYW19LCBjYSBtb2kgIgogICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgIGYiZzIgbWFuZyB2YW8ge21hbmchcn0g4oCUIGRhIGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPyIp'
'CiAgICBlbHNlOgogICAgICAgICMgbnVtc3RhdCBpbiBgLWAgKGtob25nIGNvIHNvIGRvbmcpIGNobyB0ZXAgYmluYXJ5Ly1k'
'aWZmIHRoZW8gYXR0cmlidXRlcyDigJQga2UgY2EgYXR0cmlidXRlcyBDVUEgTkdVT0kgRE8gKGRvIHRyZW4KICAgICAgICAj'
'IDIwMjYtMDktMzBnOiBjb3JlLmF0dHJpYnV0ZXNGaWxlIGAqLnB5IC1kaWZmYCA9PiAiMiB0ZXAgLyArMCIgREFUIGNobyAw'
'ZWE5NWRlLCB0aGF0ICszOTcpLiBgLWAgbGEgS0hPTkcgRE8gRFVPQywKICAgICAgICAjIGtob25nIHBoYWkgMDsgVFJVT1Qg'
'dGhlbyBzbyB0ZXAgLyBzbyBkb25nIERBIGRlbSBkdW9jIHZhbiBnaXUgKHF1YW4gc2F0IHRydWMgdGllcCkuCiAgICAgICAg'
'a2hvbmdfc28gPSBbaFsyXSBmb3IgaCBpbiBoYW5nIGlmIG5vdCAoaFswXS5pc2RpZ2l0KCkgYW5kIGhbMV0uaXNkaWdpdCgp'
'KV07IGdoaSgidGVwX2tob25nX3NvX2RvbmciLCBraG9uZ19zbykKICAgICAgICB2dW90ID0gbGVuKGhhbmcpID4gVFJBTl9U'
'RVAgb3IgdGhlbSA+IFRSQU5fRE9ORwogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBUUlVPVCBpZiB2dW90IGVsc2Ug'
'KEtERCBpZiBraG9uZ19zbyBlbHNlIERBVCksCiAgICAgICAgICAgIGYie2xlbihoYW5nKX0gdGVwIC8gK3t0aGVtfSIgKyAo'
'ZiIg4oCUIG51bXN0YXQgS0hPTkcgY28gc28gZG9uZyBjaG8ge2tob25nX3NvfSIgaWYga2hvbmdfc28gZWxzZSAiIikpCgoj'
'IENvbmcga2ljaCB0aHVvYyBQSEFJIGRlIGxhaSBNT1Qga2V0IHF1YS4gTGVuaCBudW1zdGF0IGhvbmcgdGhpIG5oYW5oIGBp'
'ZiByYzogcGFzc2Aga2hvbmcgZ2hpIGdpLCB2YSB2YW5nIG1hdCBvIGRheQojIHRoYW5oIERBVCBvIGJvIGdvcDogY2F1IGhp'
'bmggZGlmZiBDVUEgTkdVT0kgRE8gaG9uZyAoZGlmZi5vcmRlckZpbGUgdHJvIHRlcCBraG9uZyBjbywgZGlmZi5hbGdvcml0'
'aG0gZ28gc2FpID0+IHJjPTEyOCkgY2hvCiMgLS1jaGkta2ljaC10aHVvYyByYz0wIHZvaSAwIGNob3QsIGx1b3QgZGF5IGR1'
'ICJEQVQgMTEiIHJjPTAgKGRvIHRyZW4gMjAyNi0wOS0zMGgsIDBlYTk1ZGUpLiBWYW5nIG1hdCBsYSBLSE9ORyBETyBEVU9D'
'LgojIFR1IDMwaiBudW1zdGF0IGxhIGRpZmYtdHJlZSAoa2hvbmcgZG9jIGhhaSBraG9hIGF5KTsgZHVvbmcgY29uIGxhaSBk'
'byBkdW9jOiBkaWZmLnJlbmFtZUxpbWl0IGdvIHNhaSA9PiByYz0xMjguCmlmIG5vdCBhbnkoY1swXSA9PSAiTjcnIGtpY2gg'
'dGh1b2MiIGZvciBjIGluIGNob3QpOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJjb25nIEtIT05HIHJhIGtl'
'dCBxdWEgKGdpdCBkaWZmLXRyZWUgLS1udW1zdGF0IHJjPXtyY30pOiB7X2FuX3VzZXJpbmZvKGVyKVs6NzBdfSIpCgojIERp'
'bmggZGFuaCBUSEFUIG5hbSBvIE43JyAoY2EgbW9pIGcyIG1hbmcgdmFvKSwgS0hPTkcgbyAiaGF1IGR1ZSBnMSI6IGcxIGRh'
'IGxhbmQgbmVuIG1vaSBuaGFuaCBkZXUKIyBsYSBoYXUgZHVlLiBEb25nIGRhdSBraG9pIGRhbiBwaGFpIHR1IGtoYWkgdGhl'
'byBrZXQgcXVhIGF5IChkbyBkdW9jOiBtYXN0ZXIgNDQ2MjBlOCBtbyBraG9pIGJhbmcKIyAiVEhFIEhFIERPIERVT0M6IGcy'
'IiwgSlNPTiAidGhlX2hlIjogImcyIiwgdHJvbmcga2hpIE43JyBkYSBrZXQgbHVhbiAia2hvbmcgcGhhaSB1bmcgdmllbiIp'
'LgojIE5oYW4gY2hpIGR1b2Mgbm9pIERVTkcgY2FpIGRvIGR1b2M6IGBbXWAga2hvbmcgdGFjaCAiZGEgbGFuZCIga2hvaSAi'
'bmhhbSBuaGFuaCIvInBhY2tldCBraGFjIiAoZG8KIyBkdW9jIHRyZW4gMjAyNi0wOS0zMGI6IHVuZyB2aWVuIDJhNjc5Njgg'
'REEgTEFORCBiaSBnb2kgIktIT05HIHBoYWkgdW5nIHZpZW4gZzIiKS4KaWYgdGhlX2hlID09ICJnMiIgYW5kIG5vdCBzby5n'
'ZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpOgogICAgdGhlX2hlID0gKCJLSE9ORyBtYW5nIGNhIG1vaSBnMiBuYW8gKGRhIGxh'
'bmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPykiIGlmIHNvLmdldCgiY2FfbW9pX2cyX21hbmdfdmFvIikgPT0gW10KICAg'
'ICAgICAgICAgICBlbHNlICJnMj8gKENIVUEgZGluaCBkYW5oIGR1b2MgZG9pIHR1b25nKSIpCiAgICBnaGkoInRoZV9oZSIs'
'IHRoZV9oZSkKCiMgQ29uZyBuaGFuaDogZG8gUklFTkcga2ljaCB0aHVvYyAodmFpIGdpYXkpIHJvaSBkdW5nLiBEdW5nIGto'
'aSBjYW4geGFjIG1pbmggbGFpCiMgdmUgbmVuIG1hIGtob25nIG11b24gdHJhIDIwLTQ1IHBodXQgY2hvIGNhIGJvIHRlc3Qu'
'CmlmICItLWNoaS1raWNoLXRodW9jIiBpbiBzeXMuYXJndjoKICAgIGlubigiIik7IGlubigiPSIgKiA3OCkKICAgIGlubigi'
'LS1jaGkta2ljaC10aHVvYzogQ0hJIGRvIGNvbmcga2ljaCB0aHVvYy4gRGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVt'
'IHRodS4iKQogICAgaW5uKCItIiAqIDc4KQogICAgZm9yIF90LCBfdHQsIF9jdCBpbiBjaG90OiBpbm4oZiIgIHtfdHQ6MTR9'
'IHtfdH0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgIF9rID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hv'
'dCBpZiB0ID09IEtERCkKICAgIF9yID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQogICAgc3lz'
'LmV4aXQoMyBpZiBfayBlbHNlICgxIGlmIF9yIGVsc2UgMCkpCgpDSElfUFJPQkUgPSAiLS1jaGktcHJvYmUiIGluIHN5cy5h'
'cmd2ICAgICMgYm8gcXVhIGJvIHRlc3QgKyBONzsgZ2l1IDAsIDEsIDMKIyAtLS0tLS0tLS0tLS0tLS0tIDIuIGJvIHRlc3Qg'
'ZGF5IGR1IC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlu'
'bigiMi4gQk8gVEVTVCBEQVkgRFUgKDEwLTQwIHBodXQpIikKICAgIHJjX24sIG91dF9uID0gY2hheShbIm9wcy9sZWFzZV9w'
'dWJsaXNoX3Rlc3QucHkiXSwgZ29jKQogICAgZ2hpKCJyY19zdWl0ZSIsIHJjX24pCiAgICBtID0gUlhfVE9ORy5zZWFyY2go'
'b3V0X24pCiAgICBpbm4oIiAgcmMgPSIsIHJjX24sICJ8IiwgbS5ncm91cCgwKSBpZiBtIGVsc2UgIihLSE9ORyBkb2MgZHVv'
'YyBkb25nIHRvbmcga2V0KSIpCiAgICBpZiBtOgogICAgICAgIGdoaSgiZGF0IiwgaW50KG0uZ3JvdXAoMSkpKTsgZ2hpKCJ0'
'cmVuIiwgaW50KG0uZ3JvdXAoMikpKTsgZ2hpKCJib19xdWFfc28iLCBpbnQobS5ncm91cCg0KSkpCiAgICBkb19oZXQsIGdj'
'LCB0aW4gPSBkb2NfZG8ob3V0X24pCiAgICBnaGkoInNvX2NhX2RvIiwgbGVuKGRvX2hldCkpOyBnaGkoImxpZXRfa2VfZGF5'
'X2R1IiwgdGluKQogICAgZm9yIGcgaW4gZ2M6IGlubigiICAgKiIsIGcpCiAgICBpbm4oIiIpOyBpbm4oZiIgID09PSB7bGVu'
'KGRvX2hldCl9IENBIERPID09PSIpCiAgICBmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGlu'
'bihmIiAgIHt0LnNwbGl0KCdfJylbMF06N30ge3R9Iik7IGlubihmIiAgICAgICAgICAge2RvX2hldFt0XVs6MTUwXX0iKQog'
'ICAgZ2hpKCJkb19seV9kbyIsIHt0OiBkb19oZXRbdF1bOjMwMF0gZm9yIHQgaW4gZG9faGV0fSkKICAgICMgLS0tLSBDSE9U'
'OiBtb2kgY2EgRE8gcGhhaSBHSUFJIFRISUNIIERVT0MgLS0tLQogICAgIyBUaGlldSBjaG90IG5heSwgYm8gZG8gaW4gZGFu'
'aCBzYWNoIGRvIHJvaSB2YW4gdGhvYXQgcmM9MC4gRG8gZHVuZyBsYSBsb2kgZGEgeGF5IHJhOgogICAgIyBsdW90IFdpbmRv'
'd3MgMTktMDkgY28gdDE3MSBETyBtYSBibyBkbyBiYW8gIkRBVCAxMCB8IFRSVU9UIDAiIHZhIHJjPTAuCiAgICBkZWYgX2to'
'b2EodCk6IHJldHVybiB0LnNwbGl0KCJfIilbMF0KICAgIGRvX3BhY2tldCwgZG9fbGEsIGRvX3RoaWV1X2NvbmdfY3UgPSBb'
'XSwgW10sIFtdCiAgICBmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGssIGx5ID0gX2tob2Eo'
'dCksIGRvX2hldFt0XQogICAgICAgIGlmIGsgaW4gQ0FfUEFDS0VUOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRv'
'X3BhY2tldC5hcHBlbmQodCkKICAgICAgICBlbGlmICJLSMOUTkcgxJBPIMSQxq/hu6JDIiBpbiBseSBvciAidGhp4bq/dSBg'
'IiBpbiBseTogIGRvX3RoaWV1X2NvbmdfY3UuYXBwZW5kKHQpCiAgICAgICAgZWxpZiBrIGluIE5HT0FJX1BIQU1fVkk6ICAg'
'ICAgICAgICAgICAgICAgICAgICAgcGFzcwogICAgICAgIGVsc2U6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgIGRvX2xhLmFwcGVuZCh0KQogICAgZ2hpKCJkb19wYWNrZXQiLCBkb19wYWNrZXQpOyBnaGkoImRvX2xhIiwg'
'ZG9fbGEpOyBnaGkoImRvX3RoaWV1X2NvbmdfY3UiLCBkb190aGlldV9jb25nX2N1KQogICAgaW5uKCIiKQogICAgaW5uKGYi'
'ICBjYSBETyB0aHVvYyBDSElOSCBwYWNrZXQgbmF5IDoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdIG9yICdraG9u'
'ZyBjbyd9IikKICAgIGlubihmIiAgY2EgRE8gbmdvYWkgcGhhbSB2aSAocjMga2hhaSk6IHtbX2tob2EoeCkgZm9yIHggaW4g'
'c29ydGVkKGRvX2hldCwga2V5PXNvX2NhKSBpZiBfa2hvYSh4KSBpbiBOR09BSV9QSEFNX1ZJXX0iKQogICAgaW5uKGYiICBj'
'YSBETyB2aSBUSElFVSBDT05HIENVICAgICAgIDoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XSBvciAn'
'a2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERPIExBIChraG9uZyBnaWFpIHRoaWNoIGR1b2MpOiB7W19raG9hKHgpIGZv'
'ciB4IGluIGRvX2xhXSBvciAna2hvbmcgY28nfSIpCiAgICAjIC0tLS0gQ0hPVDogcGhlcCBkbyBwaGFpIFRST04gdHJ1b2Mg'
'a2hpIG1vdCBjaHUgREFUIG5hbyBkdW9jIHBoYXQgLS0tLQogICAgIyBCYW4gdHJ1b2MgY2hpIElOIGB0aW5gL2ByY19zdWl0'
'ZWA6IGJvIHRlc3QgY2hldCBnaXVhIHQxNzEgKHJjPTEzNCwga2hvbmcgZG9uZyB0b25nKQogICAgIyB2YW4gcmEgIkRBVCAx'
'MiB8IFRSVU9UIDAiIHJjPTA7IGNhIFBBQ0tFVCB2YW5nIG1hdCBoYXkgYmkgQk8gUVVBIGN1bmcgZHVvYyBjaGFtIG5odQog'
'ICAgIyAia2hvbmcgZG8iLiBWYW5nIG1hdCBraG9uZyBwaGFpICJraG9uZyBkbyIg4oCUIGxhIEtIT05HIERPIERVT0MuCiAg'
'ICB2YW5nID0gW3QgZm9yIHQgaW4gc29ydGVkKENBX1BBQ0tFVCwga2V5PXNvX2NhKSBpZiBtYXVfY2Eob3V0X24sIHQpIG5v'
'dCBpbiAoIlFVQSIsICJETyIpXQogICAgbHlfa2RkID0gW10KICAgIGlmIG5vdCB0aW46IGx5X2tkZC5hcHBlbmQoImRhbmgg'
'c2FjaCBkbyBLSE9ORyBkYXkgZHUiKQogICAgaWYgcmNfbiBub3QgaW4gKDAsIDEpIG9yIChyY19uID09IDEpICE9IGJvb2wo'
'ZG9faGV0KToKICAgICAgICBseV9rZGQuYXBwZW5kKGYicmMgYm8gdGVzdD17cmNfbn0ga2hvbmcga2hvcCB7bGVuKGRvX2hl'
'dCl9IGNhIERPIGRvYyBkdW9jIikKICAgIGlmIHZhbmc6IGx5X2tkZC5hcHBlbmQoZiJjYSBQQUNLRVQgdmFuZy9ibyBxdWE6'
'IHt2YW5nfSIpCiAgICBnaGkoImNhX3BhY2tldF92YW5nIiwgdmFuZyk7IGdoaSgibHlfZG9fY2h1YV90cm9uIiwgbHlfa2Rk'
'KQogICAgaWYgbHlfa2RkOiBrZXQoIkJvIHRlc3QgY2hheSBUUk9OIHZhIGRvYyBEVSIsIEtERCwgIjsgIi5qb2luKGx5X2tk'
'ZCkpCiAgICBjaHVhX3Ryb24gPSBLREQgaWYgbHlfa2RkIGVsc2UgREFUCiAgICBrZXQoIktob25nIGNhIG5hbyBjdWEgUEFD'
'S0VUIGJpIERPIiwgY2h1YV90cm9uIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9f'
'cGFja2V0IGVsc2UgZiJETzoge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdfSDigJQgYmFuIHZhIENIVUEgeG9uZyIp'
'CiAgICBrZXQoIk1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jIiwgY2h1YV90cm9uIGlmIG5vdCBkb19sYSBlbHNlIFRS'
'VU9ULAogICAgICAgICIiIGlmIG5vdCBkb19sYSBlbHNlIGYibGE6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdfSIpCiAg'
'ICBpZiBkb190aGlldV9jb25nX2N1OgogICAgICAgIGtldCgiQ29uZyBjdSBkYXkgZHUgZGUgZG8iLCBLREQsIGYidGhpZXUg'
'Y29uZyBjdSBjaG8ge1tfa2hvYSh4KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XX0iKQoKICAgIGJxID0gc29ydGVkKHt0'
'IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91dF9uKX0sIGtleT1zb19jYSk7IGdoaSgiY2FfYm9fcXVhIiwgYnEp'
'CiAgICBpbm4oIiIpOyBpbm4oZiIgIEJPIFFVQSAoe2xlbihicSl9KToge1t4LnNwbGl0KCdfJylbMF0gZm9yIHggaW4gYnFd'
'fSIpCgogICAgaW5uKCIiKTsgaW5uKCIgIE4xLU40ICh0MTY1LXQxNjgpLCB0aWV1IGNoaSBuZ2hpZW0gdGh1IGN1YSByMiwg'
'bmF5IGxhIGNoaSBiYW8gaG9pIHF1eToiKQogICAgYjQgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQU1PSX07'
'IGdoaSgiY2FfbW9pIiwgYjQpCiAgICBmb3IgdCBpbiBDQU1PSTogaW5uKGYiICAgICB7dH06IHtiNFt0XX0iKQogICAgIyBC'
'T19RVUEvdmFuZyBsYSBDSFVBIENIQVksIGtob25nIHBoYWkgRE86IGNoaSBtb3QgY2EgRE8gbW9pIGR1b2MgcGhhdCBUUlVP'
'VC4KICAgIGtldCgiTjEtTjQgKHQxNjUtdDE2OCkiLCBEQVQgaWYgYWxsKHYgPT0gIlFVQSIgZm9yIHYgaW4gYjQudmFsdWVz'
'KCkpCiAgICAgICAgZWxzZSAoVFJVT1QgaWYgYW55KHYgPT0gIkRPIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkgZWxzZSBLREQp'
'LCBzdHIoYjQpKQoKICAgIGlubigiIik7IGlubigiICAxNSBjYSB0dW5nIGRvIHRyZW4gQ0k6IikKICAgIGIxNSA9IHt0OiBt'
'YXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBMTV9OyBnaGkoImNhMTUiLCBiMTUpCiAgICBpbm4oIiAgICAiICsgIiAgIi5q'
'b2luKGYie3R9OntiMTVbdF19IiBmb3IgdCBpbiBDQTE1KSkKCiAgICAjIHQxMzYg4oCUIE4xMiBkbyBHSUFOIFRJRVAgcXVh'
'IGtldCBxdWEgY2EKICAgIHQxMzZfdGVuID0gbmV4dCgodCBmb3IgdCBpbiBkb19oZXQgaWYgdC5zdGFydHN3aXRoKCJ0MTM2'
'IikpLCBOb25lKQogICAgaWYgYjE1LmdldCgidDEzNiIpID09ICJRVUEiOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBr'
'ZXQgcXVhIGNhKSIsIERBVCwgInQxMzYgUVVBIikKICAgIGVsaWYgYjE1LmdldCgidDEzNiIpICE9ICJETyI6CiAgICAgICAg'
'a2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgS0RELCBmInQxMzYgPSB7YjE1LmdldCgndDEzNicpIXJ9IOKAlCBr'
'aG9uZyBjaGF5L2tob25nIHRoYXkiKQogICAgZWxzZToKICAgICAgICBseSA9IGRvX2hldC5nZXQodDEzNl90ZW4sICIiKQog'
'ICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIFRSVU9ULCBmIkRPOiB7bHlbOjkwXX0iKQoKIyAtLS0t'
'LS0tLS0tLS0tLS0tIDMuIHByb2JlIFRIQU5HIHZhbyBoYW0gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICog'
'NzgpOyBpbm4oIjMuIFBST0JFIFRIQU5HIOKAlCBnb2kgX2dpdF93aW5kb3dzIHZvaSB0aGFtIHNvIHRpZW0iKQpzcGVjID0g'
'aW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwNTQxIiwgc3RyKHRlcCkpCmxwID0gaW1wb3J0bGli'
'LnV0aWwubW9kdWxlX2Zyb21fc3BlYyhzcGVjKTsgc3BlYy5sb2FkZXIuZXhlY19tb2R1bGUobHApCnNpZyA9IGluc3BlY3Qu'
'c2lnbmF0dXJlKGxwLl9naXRfd2luZG93cykKZ2hpKCJ0aGFtX3NvX19naXRfd2luZG93cyIsIGxpc3Qoc2lnLnBhcmFtZXRl'
'cnMpKQppbm4oIiAgdGhhbSBzbyBjdWEgX2dpdF93aW5kb3dzOiIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQoKZGVmIGdvaSgq'
'Kmt3KToKICAgICIiIkdvaSBfZ2l0X3dpbmRvd3MsIEJBVCBzdGRlcnIgZGUgbW90IGRvbmcgY2hhbiBkb2FuIGtob25nIGdp'
'ZXQgbHVvdCBkby4iIiIKICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJy'
'KGUpOgogICAgICAgIHIgPSBscC5fZ2l0X3dpbmRvd3MoKiprdykKICAgIHJldHVybiByLCBlLmdldHZhbHVlKCkKCiMgLS0t'
'IGRvaSBjaHVuZyByaWc6IHBoYWkgdHJhIGxvaSBkdW5nIG1vdCBjYSB0YSBCSUVUIFRSVU9DIGRhcCBhbiAtLS0Kd2l0aCB0'
'ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgbmdvYWkgPSBQYXRoKHQpLyJuZ29haSI7IG5nb2FpLm1r'
'ZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAg'
'IChuZ29haS8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjEsIF8gPSBnb2kocGF0'
'aD1zdHIobmdvYWkpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgKGN3LyJnaXQuZXhlIikud3Jp'
'dGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMiwgXyA9IGdvaShwYXRoPXN0cihjdyksIHByb2dyYW1fZmls'
'ZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCnJpZ19vayA9IGJvb2wocjEpIGFuZCByMiBpcyBOb25lCmdoaSgicmlnX2RvaV9j'
'aHVuZyIsIHJpZ19vaykKa2V0KCJSSUcgZG9pIGNodW5nIChiaWV0IHRydW9jIGRhcCBhbikiLCBEQVQgaWYgcmlnX29rIGVs'
'c2UgS0RELAogICAgZiJuZ29haS1jd2QtPnsnTkhBTicgaWYgcjEgZWxzZSAnTm9uZSd9IHwgdHJvbmctY3dkLT57J05IQU4n'
'IGlmIHIyIGVsc2UgJ05vbmUnfSIpCmlmIG5vdCByaWdfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IHJp'
'ZyBzYWksIG1vaSBjaG90IGR1b2kgc2Ugdm8gbmdoaWEuIik7IHN5cy5leGl0KDMpCgojIC0tLSBNT0kgQ09ORyBQSEFJIFRV'
'IENIVU5HIE1JTkggTk8gQ08gVEhFIERPIC0tLQojIEJhaSBob2MgZGF0IG5oYXQgY3VhIHBhY2tldCBuYXk6IGRvX24xMCBi'
'YW4gY3UgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxCiMgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBk'
'dW5nIGtodXlldCB0YXQgbWEgTjEwIHNpbmggcmEgZGUgYmF0LiBObyBkZWdlbmVyYXRlIOKAlAojIHRyZW4gV2luZG93cyBv'
'cy5wYXRoc2VwIERBIGxhICc7JyBuZW4gInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gY3VuZyBrZXQgcXVhLgojIE1v'
'dCBjb25nIGtob25nIHRoZSBETyB0aGkga2hvbmcgcGhhaSBjb25nLCB2YSBubyBuZ3V5IGhpZW0gaG9uIGtob25nIGNvIGNv'
'bmc6IG5vCiMgcGhhdCByYSBtb3QgY2h1IERBVC4KIwojIE5lbiB0cnVvYyBraGkgRFVORyBuYW0gY29uZyBuYXkgZGUgcGhh'
'biBxdXlldCwgYmF0IHR1bmcgY29uZyBnaWV0IG1vdCBkb3QgYmllbiBkYQojIGJpZXQgdHJvbmcuIENvbmcgbmFvIGtob25n'
'IGdpZXQgZHVvYyB0aGkgY2h1IERBVCBjdWEgbm8gYmkgSEEgeHVvbmcgS0hPTkcgRE8gRFVPQzsKIyBUUlVPVCBnaXUgbmd1'
'eWVuIChxdWFuIHNhdCB0cnVjIHRpZXAsIHZkLiBnMSB2YW4gbmhhbiBnaXQuYmF0KS4gRG90IGJpZW4gY2hheSB0cmVuIEJB'
'TiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaQojIGR1bmcgdG9pIChjdW5nIGt5IGx1YXQgbmh1IE43KS4KRE9UX0JJRU5f'
'VFVfS0lFTSA9IFsKICAgICgiTjgiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICdpZiBjaGlfZGluaCBhbmQgUGF0'
'aChjaGlfZGluaCkubmFtZS5sb3dlcigpID09ICJnaXQuZXhlIiBhbmQgaG9wX2xlKGNoaV9kaW5oKTonLAogICAgICJpZiBj'
'aGlfZGluaCBhbmQgaG9wX2xlKGNoaV9kaW5oKToiKSwKICAgICgiTjkiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAg'
'ICJkID0gZF9yYXcuc3RyaXAoKS5zdHJpcCgnXCInKSIsICJkID0gZF9yYXcuc3RyaXAoKSIpLAogICAgKCJOMTAiLCAib3Bz'
'L2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJzZXAgPSBvcy5wYXRoc2VwIGlmIHBoYW5fY2FjaCBpcyBOb25lIGVsc2UgcGhh'
'bl9jYWNoIiwgInNlcCA9IG9zLnBhdGhzZXAiKSwKICAgICgiTjExIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwgImlmIGNo'
'YW5fZG9hbiBpcyBub3QgTm9uZToiLCAiaWYgRmFsc2U6IiksCiAgICAoIk4xMiIsICJvcHMvbGVhc2VfcHVibGlzaF90ZXN0'
'LnB5IiwKICAgICAnZ2l0X3BhdGg9Ii8va2hvbmctY28vZ2l0IicsICdnaXRfcGF0aD0iL2tob25nLWNvL2dpdCInKSwKXQpp'
'bm4oIiIpOyBpbm4oIiAgdHUga2llbSBjb25nIOKAlCBtb2kgY29uZyBwaGFpIGdpZXQgZHVvYyBtb3QgZG90IGJpZW4gZGEg'
'YmlldDoiKQpnaWV0ID0ge30KZm9yIG1hLCBkdW9uZywgdGltLCB0aGF5IGluIERPVF9CSUVOX1RVX0tJRU06CiAgICBfdGVu'
'LCBfaGFtID0gbmV4dCgoKGEsIGIpIGZvciBhLCBiIGluIFBST0JFIGlmIGEuc3RhcnRzd2l0aChtYSArICIgIikpLCAoTm9u'
'ZSwgTm9uZSkpCiAgICBpZiBfaGFtIGlzIE5vbmU6CiAgICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9'
'IEtIT05HIERPIERVT0M6IGtob25nIHRpbSB0aGF5IHByb2JlIHRlbiAne21hfSAuLi4nIik7IGNvbnRpbnVlCiAgICB0cnk6'
'CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyBfdDoKICAgICAgICAgICAgX2MgPSBQYXRo'
'KF90KS8iY2F5Ijsgc2h1dGlsLmNvcHl0cmVlKGdvYy8ib3BzIiwgX2MvIm9wcyIpCiAgICAgICAgICAgIF9mID0gX2MvZHVv'
'bmc7IF9uZCA9IF9mLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBpZiBfbmQuY291bnQodGltKSAh'
'PSAxOgogICAgICAgICAgICAgICAgZ2lldFttYV0gPSBOb25lCiAgICAgICAgICAgICAgICBpbm4oZiIgICAge21hOjR9IEtI'
'T05HIERPIERVT0M6IG1hdSBkb3QgYmllbiBraG9wIHtfbmQuY291bnQodGltKX0gbGFuIChtb25nIDEpIgogICAgICAgICAg'
'ICAgICAgICAgIGYiIOKAlCBtYSBuZ3VvbiBkYSBkb2ksIGRvdCBiaWVuIG5heSBoZXQgeSBuZ2hpYSIpOyBjb250aW51ZQog'
'ICAgICAgICAgICBfZi53cml0ZV90ZXh0KF9uZC5yZXBsYWNlKHRpbSwgdGhheSwgMSksIGVuY29kaW5nPSJ1dGYtOCIpCiAg'
'ICAgICAgICAgIF9zcCA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF9kYl8iICsgbWEsIHN0'
'cihfYy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQogICAgICAgICAgICBfbSA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9m'
'cm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbSkKICAgICAgICAgICAgZGVmIF9nb2lfZGIoKiprdyk6'
'CiAgICAgICAgICAgICAgICBfZSA9IGlvLlN0cmluZ0lPKCkKICAgICAgICAgICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRp'
'cmVjdF9zdGRlcnIoX2UpOgogICAgICAgICAgICAgICAgICAgIHJldHVybiBfbS5fZ2l0X3dpbmRvd3MoKiprdyksIF9lLmdl'
'dHZhbHVlKCkKICAgICAgICAgICAgX3R0LCBfY3QsIF8gPSBfaGFtKF9nb2lfZGIsIGluc3BlY3Quc2lnbmF0dXJlKF9tLl9n'
'aXRfd2luZG93cyksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBfYy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0'
'LnB5IikKICAgICAgICBnaWV0W21hXSA9IChfdHQgPT0gVFJVT1QpCiAgICAgICAgaW5uKGYiICAgIHttYTo0fSBkb3QgYmll'
'biAtPiB7X3R0OjE0fSB7J0dJRVQgRFVPQycgaWYgX3R0ID09IFRSVU9UIGVsc2UgJ1NPTkcgU09UJ30iCiAgICAgICAgICAg'
'ICsgKGYiICAgKHtfY3R9KSIgaWYgX2N0IGVsc2UgIiIpKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgICAgICBn'
'aWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzoge3R5cGUoX2UpLl9fbmFtZV9ffToge19l'
'fSIpCmdoaSgiY29uZ19naWV0X2R1b2NfZG90X2JpZW4iLCBnaWV0KQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwpIGluIFsodCwg'
'Zihnb2ksIHNpZywgdGVwdCkpIGZvciB0LCBmIGluIFBST0JFXToKICAgIGdoaSgicHJvYmVfIiArIHRlbi5zcGxpdCgpWzBd'
'Lmxvd2VyKCksIGRsKQogICAgaWYgaXNpbnN0YW5jZShkbCwgZGljdCk6CiAgICAgICAgZm9yIGssIHYgaW4gZGwuaXRlbXMo'
'KTogaW5uKGYiICAgIHtrOjM0fToge3Z9IikKICAgIG1hID0gdGVuLnNwbGl0KClbMF0KICAgIGlmIGdpZXQuZ2V0KG1hKSBp'
'cyBub3QgVHJ1ZSBhbmQgdHQgPT0gREFUOgogICAgICAgICMgREFUIHR1IG1vdCBjb25nIGNodWEgY2h1bmcgbWluaCBkdW9j'
'IGxhIGJpZXQgRE8gdGhpIGtob25nIGRhbmcgdGluIGhvbiBLREQuCiAgICAgICAga2V0KHRlbiwgS0RELCBmImNvbmcgS0hP'
'TkcgZ2lldCBkdW9jIGRvdCBiaWVuIGN1YSBjaGluaCBubyAoe2dpZXQuZ2V0KG1hKSFyfSkiCiAgICAgICAgICAgICAgICAg'
'ICAgICBmIiAtPiBjaHUgREFUIG5heSBraG9uZyBjbyBnaWEgdHJpIikKICAgIGVsc2U6CiAgICAgICAga2V0KHRlbiwgdHQs'
'IGN0KQoKIyAtLS0tLS0tLS0tLS0tLS0tIDQuIE43IGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gLS0tLS0tLS0tLS0tLS0t'
'LQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCI0LiBONyDigJQgZG90IGJpZW4g'
'dHJlbiBCQU4gU0FPIFRBTSAoY2F5IHRoYXQgS0hPTkcgYmkgZHVuZyB0b2kpIikKICAgIHRydW9jID0gdGVwLnJlYWRfdGV4'
'dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKQogICAgZ2hpKCJuN190cnVvYyIsIHRydW9jKTsgaW5uKGYiICBz'
'byBkb25nIGtob3Age01BVV9XSU4hcn06IFRSVU9DID0ge3RydW9jfSBbbW9uZyAxXSIpCiAgICBpZiB0cnVvYyAhPSAxOgog'
'ICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgZiJtYXUgeHVhdCBoaWVuIHt0cnVvY30gbGFu'
'LCBraG9uZyBwaGFpIDEiKQogICAgZWxzZToKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFz'
'IHRtcDoKICAgICAgICAgICAgc2FvID0gUGF0aCh0bXApLyJjYXkiCiAgICAgICAgICAgIHNodXRpbC5jb3B5dHJlZShnb2Ms'
'IHNhbywgaWdub3JlPXNodXRpbC5pZ25vcmVfcGF0dGVybnMoIi5naXQiLCAiX19weWNhY2hlX18iLCAiKi5weWMiKSkKICAg'
'ICAgICAgICAgZjIgPSBzYW8vIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiCiAgICAgICAgICAgIGYyLndyaXRlX3RleHQoZjIu'
'cmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJlcGxhY2UoTUFVX1dJTiwgImlmIEZhbHNlOiIpLCBlbmNvZGluZz0idXRm'
'LTgiKQogICAgICAgICAgICBzYXUgPSBmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTik7IGdo'
'aSgibjdfc2F1Iiwgc2F1KQogICAgICAgICAgICBpbm4oZiIgIFNBVSAoZGEgZG90IGJpZW4pID0ge3NhdX0gW21vbmcgMF0i'
'KQogICAgICAgICAgICBpZiBzYXUgIT0gMDoKICAgICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93'
'cyIsIEtERCwgImRvdCBiaWVuIEtIT05HIGFwIGR1b2MiKQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmNf'
'bSwgb3V0X20gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJdLCBzYW8pCiAgICAgICAgICAgICAgICBtMTY1'
'ID0gbWF1X2NhKG91dF9tLCAidDE2NSIpOyBkbSwgXywgXyA9IGRvY19kbyhvdXRfbSkKICAgICAgICAgICAgICAgIHRlbjE2'
'NSA9IG5leHQoKHQgZm9yIHQgaW4gZG0gaWYgdC5zdGFydHN3aXRoKCJ0MTY1IikpLCBOb25lKQogICAgICAgICAgICAgICAg'
'bHkgPSAoZG0uZ2V0KHRlbjE2NSkgb3IgIiIpCiAgICAgICAgICAgICAgICBnaGkoIm43X3QxNjUiLCBtMTY1KTsgZ2hpKCJu'
'N19seV9kbyIsIGx5WzoyMDBdKQogICAgICAgICAgICAgICAgaW5uKGYiICB0MTY1IHNhdSBkb3QgYmllbjoge20xNjV9IHwg'
'e2x5WzoxMTBdfSIpCiAgICAgICAgICAgICAgICBkdW5nX2x5X2RvID0gIlBBVEggdCIgaW4gbHkgb3IgIi91c3IvYmluIiBp'
'biBseQogICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgREFUIGlmIChtMTY1ID09ICJE'
'TyIgYW5kIGR1bmdfbHlfZG8pIGVsc2UKICAgICAgICAgICAgICAgICAgICAoVFJVT1QgaWYgbTE2NSA9PSAiRE8iIGVsc2Ug'
'S0REKSwKICAgICAgICAgICAgICAgICAgICAiZ2lldCBkdW5nIGx5IGRvIiBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5'
'X2RvKQogICAgICAgICAgICAgICAgICAgIGVsc2UgKCJETyBuaHVuZyBLSE9ORyBkdW5nIGx5IGRvIC0+IHRpbiBkdW5nIGdp'
'YSIgaWYgbTE2NSA9PSAiRE8iIGVsc2UgImtob25nIGRvYyBkdW9jIHQxNjUiKSkKCiMgLS0tLS0tLS0tLS0tLS0tLSBLRVQg'
'TFVBTiAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiPSIgKiA3OCkKaW5uKGYiVEhFIEhFIERPIERVT0M6IHt0aGVf'
'aGV9ICAgSEVBRD17aGVhZFs6MTJdfSIpCiMgS2hvaSBkYW4gY2hvIHJldmlld2VyIGJhdCBkYXUgbyBkb25nIHRyZW4sIG5l'
'biBDSEUgRE8gcGhhaSBuYW0gTkdBWSBkdW9pIG5vOiBraG9uZyBjbyBkb25nIG5heQojIHRoaSBtb3QgbHVvdCAtLWNoaS1w'
'cm9iZSBpbiAiREFUIDcgfCBUUlVPVCAwIHwgS0hPTkcgRE8gRFVPQyAwIiByYz0wIG1hIGtob25nIG5vaSBsYSBjaHVhIGNo'
'YXkgYm8gdGVzdC4KZ2hpKCJjaGVfZG8iLCAiY2hpLXByb2JlIiBpZiBDSElfUFJPQkUgZWxzZSAiZGF5LWR1IikKaWYgQ0hJ'
'X1BST0JFOgogICAgaW5uKCItLWNoaS1wcm9iZTogQ0hJIGRvIG11YyAwLCAxLCAzLiBCbyB0ZXN0LCBOMS1ONCwgdDEzNiwg'
'TjcgS0hPTkcgY2hheSAtIGRheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5naGllbSB0aHUuIikKaWYgdGhlX2hlID09ICJnMSI6'
'CiAgICBpbm4oIkxVVSBZOiBkYXkgbGEgTkVOIERPIChnMSksIEtIT05HIHBoYWkgbmdoaWVtIHRodSBnMi4gQ2FjIGNob3Qg'
'TjgtTjEyIGR1b2kgZGF5IikKICAgIGlubigiICAgICAgIFRSVU9UIGxhIERVTkcgTkhVIE1PTkcg4oCUIGNodW5nIGxhIG5o'
'dW5nIGxvIGcyIHNpbmggcmEgZGUgdsOhLiIpCmlubigiLSIgKiA3OCkKZm9yIHRlbiwgdHQsIGN0IGluIGNob3Q6CiAgICBp'
'bm4oZiIgIHt0dDoxNH0ge3Rlbn0iICsgKGYiICAge2N0fSIgaWYgY3QgZWxzZSAiIikpCm5fa2RkID0gc3VtKDEgZm9yIF8s'
'IHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKbl90cnVvdCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBU'
'UlVPVCkKaW5uKCItIiAqIDc4KQppbm4oZiIgIERBVCB7c3VtKDEgZm9yIF8sdCxfIGluIGNob3QgaWYgdD09REFUKX0gfCBU'
'UlVPVCB7bl90cnVvdH0gfCBLSE9ORyBETyBEVU9DIHtuX2tkZH0iKQppbm4oZiIgIFRvbmcgY2EgZG86IHtzby5nZXQoJ3Nv'
'X2NhX2RvJyl9IHwgZGFuaCBzYWNoIGRheSBkdTogeydDTycgaWYgc28uZ2V0KCdsaWV0X2tlX2RheV9kdScpIGVsc2UgJ0tI'
'T05HIERPIERVT0MnfSIpCmlubihmIiAgQWRtaW5pc3RyYXRvcjoge3NvLmdldCgncXV5ZW5fYWRtaW4nKX0gfCBzeW1saW5r'
'OiB7c28uZ2V0KCdzeW1saW5rX2R1b2MnKX0iKQppbm4oIiIpOyBpbm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kgSlNPTiBOQVkg'
'VkUgQ0hPIFJFVklFV0VSIC0tLSIpCmdoaSgiY2hvdCIsIFt7InRlbiI6IGEsICJ0cmFuZ190aGFpIjogYiwgImNoaV90aWV0'
'IjogY30gZm9yIGEsIGIsIGMgaW4gY2hvdF0pCmlubihqc29uLmR1bXBzKHNvLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVu'
'dD0xLCBkZWZhdWx0PXN0cikpCiMgcmM6IDAgPSBtb2kgY2hvdCBEQVQgfCAxID0gY28gY2hvdCBUUlVPVCB8IDMgPSBjbyBj'
'aG90IEtIT05HIERPIERVT0MgKHV1IHRpZW4gYmFvIGRvbmcpCnN5cy5leGl0KDMgaWYgbl9rZGQgZWxzZSAoMSBpZiBuX3Ry'
'dW90IGVsc2UgMCkpCg=='
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
