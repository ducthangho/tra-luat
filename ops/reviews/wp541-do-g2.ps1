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
$ShaBoDo    = '5e402b5d4e7365863fb59804479689e5b181cf5932d4623ab9f31c8a10ff56be'      # SHA-256 cua bo do Python nhung ben duoi

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
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0xMC0wMWYiICAgICAgICAgICAgICAj'
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
'UEFUSCBuZW4ga2hvbmcgZG9pLiBNdWMgMCB0dSBraGFpIFRFTiAoa2hvbmcgaW4gZ2lhIHRyaSkuCiMgVEFQIGF5IGNvbiBt'
'b3QgY3VhIEtIT05HIG1hbmcgdGVuIGJpZW4ga2hvaSBkb25nOiBiYXNoKDEpIElOVk9DQVRJT04g4oCUIHN0ZGluIGxhIFNP'
'Q0tFVCAocnNoZCksIGhvYWMgU1NIX0NMSUVOVC9TU0gyX0NMSUVOVCB0cm9uZwojIG1vaSB0cnVvbmcgKGJhbiBkaWNoIGJh'
'dCBTU0hfU09VUkNFX0JBU0hSQzogR2l0IGZvciBXaW5kb3dzIGJhdCBjYSBubyBsYW4gU1lTX0JBU0hSQyDigJQgMDAwMS1i'
'YXNoLTQuNC1jeWd3aW4ucGF0Y2ggc3VhIGNvbmZpZy10b3AuaDsKIyBiYXNoIFVidW50dSBjdW5nIGJhdCksIGNvbmcgU0hM'
'Vkwgcm9uZy8wID0+IGBiYXNoIC1jYCBuYXAgL2V0Yy9iYXNoLmJhc2hyYyB2YSB+Ly5iYXNocmMgQ1VBIE5HVU9JIERPLCB2'
'YSBCTyBRVUEgQkFTSF9FTlYuIENJIGNoYXkKIyBibyB0ZXN0IHF1YSBgYmFzaCBvcHMvY2hheV9sZWFzZV9wdWJsaXNoX3Rl'
'c3Quc2hgIHRyb25nIGJ1b2MgYHNoZWxsOiBiYXNoYCA9PiBTSExWTD0yIChkbyB0cmVuIGNodW9pIGdpYSBsYXAgYnVvYyAt'
'PiBzY3JpcHQgLT4KIyBweXRob24pIG5lbiBkdW9uZyBuYXkgVEFUIHRyZW4gQ0k7IHB3c2gvY21kIGtob25nIGRhdCBTSExW'
'TCBuZW4gdHJlbiBtYXkgZG8gbm8gTU8uIERvIHRyZW4gMjAyNi0xMC0wMSAoYmFuIDAxZSwgYmFzaCA1LjIuMjEpLAojIDBl'
'YTk1ZGU6IFNTSF9DTElFTlQgKyB+Ly5iYXNocmMgYHNldCAtbyBub2Nsb2JiZXJgID0+IHQzMiB0NTEgdDYwIHQ2MiB0NjMg'
'dDY2IHQ2OCBETywgZTJlIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgICgxNTkvMTY2KTsKIyB+Ly5iYXNocmMgYGNkICIkSE9N'
'RSJgID0+IDggY2EgKHRoZW0gdDU5KTsgc3RkaW4gU09DS0VUICsgbm9jbG9iYmVyID0+IGN1bmcgNyBjYS4gTXVjIDAga2hv'
'bmcgdGhheSAocHJvYmUgZ29pIGAtLW5vcmNgLCBtYSAtLW5vcmMKIyB0YXQgZHVvbmcgbmF5KSB2YSB0dSBraGFpICJiaWVu'
'IGJhc2g6IChraG9uZyBjbykiLiBQaGllbiBTU0ggdmFvIG1heSBXaW5kb3dzIGRvIGxhIGR1b25nIHZhbyAoV2luZG93cyBU'
'SEFUOiBLSE9ORyBETyBEVU9DKS4gQm8gSEFJCiMgYmllbiBheSAoQ0kga2hvbmcgZGF0KSBWQSBjaG8gbHVvdCBjb24gc3Rk'
'aW4gPSBERVZOVUxMIOKAlCBoYWkgY28gY2hlIHJpZW5nLCBoYWkgY2hvdCByaWVuZzsgdDE1MiAoZW52IGNoaSBQQVRIKSB0'
'aHVhIGtlIHN0ZGluIGF5IG5lbgojIGN1bmcgZG9uZy4KX0JBU0hfS0hPSV9ET05HID0gZnJvemVuc2V0KHsiU0hFTExPUFRT'
'IiwgIkVOViIsICJQT1NJWExZX0NPUlJFQ1QiLCAiQ0RQQVRIIiwgIkdMT0JJR05PUkUiLCAiR0xPQlNPUlQiLCAiRVhFQ0lH'
'Tk9SRSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIkZVTkNORVNUIiwgIlRNT1VUIiwgIlNTSF9DTElFTlQiLCAi'
'U1NIMl9DTElFTlQifSkKZGVmIF9iaWVuX2Jhc2goayk6IHJldHVybiBrLnVwcGVyKCkuc3RhcnRzd2l0aCgiQkFTSCIpIG9y'
'IGsudXBwZXIoKSBpbiBfQkFTSF9LSE9JX0RPTkcKX0dJVF9HTE9CQUxfQ0kgPSAiW2luaXRdXG5cdGRlZmF1bHRCcmFuY2gg'
'PSBtYXN0ZXJcbltjb3JlXVxuXHRhdXRvY3JsZiA9IGZhbHNlXG5cdGVvbCA9IGxmXG5cdGFiYnJldiA9IDdcbiIKZGVmIGNo'
'YXkoYXJndiwgY3dkLCBwaHV0PTYwKToKICAgIGZkLCBnYyA9IHRlbXBmaWxlLm1rc3RlbXAocHJlZml4PSJ3cDU0MS1naXRj'
'b25maWctY2ktIiwgc3VmZml4PSIuaW5pIikKICAgIHhkZyA9IE5vbmUKICAgIHRyeToKICAgICAgICB4ZGcgPSB0ZW1wZmls'
'ZS5ta2R0ZW1wKHByZWZpeD0id3A1NDEteGRnLSIpCiAgICAgICAgd2l0aCBvcy5mZG9wZW4oZmQsICJ3IiwgZW5jb2Rpbmc9'
'ImFzY2lpIiwgbmV3bGluZT0iXG4iKSBhcyBmOiBmLndyaXRlKF9HSVRfR0xPQkFMX0NJKQogICAgICAgIG10ID0ge2s6IHYg'
'Zm9yIGssIHYgaW4gb3MuZW52aXJvbi5pdGVtcygpCiAgICAgICAgICAgICAgaWYgbm90IGsudXBwZXIoKS5zdGFydHN3aXRo'
'KCJHSVRfIikgYW5kIG5vdCBfYmllbl9iYXNoKGspCiAgICAgICAgICAgICAgYW5kIChub3Qgay51cHBlcigpLnN0YXJ0c3dp'
'dGgoIlBZVEhPTiIpIG9yIGsudXBwZXIoKSBpbiBfUFlfR0lVKX0KICAgICAgICBtdC51cGRhdGUoUFlUSE9OVVRGOD0iMSIs'
'IFBZVEhPTklPRU5DT0RJTkc9InV0Zi04IiwgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9IjEiLCBQWVRIT05VTkJVRkZFUkVE'
'PSIxIiwKICAgICAgICAgICAgICAgICAgR0lUX0NPTkZJR19HTE9CQUw9Z2MsIFhER19DT05GSUdfSE9NRT14ZGcsIFNIRUxM'
'Q0hFQ0tfT1BUUz0iLS1ub3JjIikKICAgICAgICBwID0gc3VicHJvY2Vzcy5ydW4oW3N5cy5leGVjdXRhYmxlXSArIGFyZ3Ys'
'IGN3ZD1zdHIoY3dkKSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgc3RkaW49c3VicHJvY2Vzcy5ERVZOVUxMLAogICAgICAgICAg'
'ICAgICAgICAgICAgICAgICB0ZXh0PVRydWUsIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9'
'cGh1dCo2MCwgZW52PW10KQogICAgZmluYWxseToKICAgICAgICB0cnk6IG9zLnJlbW92ZShnYykKICAgICAgICBleGNlcHQg'
'T1NFcnJvcjogcGFzcwogICAgICAgIGlmIHhkZzogc2h1dGlsLnJtdHJlZSh4ZGcsIGlnbm9yZV9lcnJvcnM9VHJ1ZSkKICAg'
'IHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1X2NhKG91'
'dCwgdCk6CiAgICBtID0gcmUuc2VhcmNoKHIiKD9tKV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSBbMC05Ll0rcyAo'
'XHcrKVxzKiQiLCBvdXQpCiAgICByZXR1cm4gbS5ncm91cCgyKSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdpdChnb2MsICphLCBw'
'aHV0PTUpOgogICAgcCA9IHN1YnByb2Nlc3MucnVuKFsiZ2l0IiwgIi1DIiwgc3RyKGdvYyksICphXSwgY2FwdHVyZV9vdXRw'
'dXQ9VHJ1ZSwgdGV4dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVw'
'bGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikuc3RyaXAo'
'KSwgKHAuc3RkZXJyIG9yICIiKS5zdHJpcCgpCgoKIyA9PT09PT09PT09PT09PT09PSBOQU0gUFJPQkUsIHZpZXQgdGhhbmgg'
'SEFNIFRIVUFOIGRlIFRVIEtJRU0gZHVvYyA9PT09PT09PT09PT09PT09PQojIE1vaSBoYW0gdHJhICh0cmFuZ190aGFpLCBj'
'aGlfdGlldCwgZHVfbGlldSkuIEtIT05HIGluLCBLSE9ORyB0aG9hdCDigJQgbmhvIHZheSBjaHVuZwojIGNoYXkgZHVvYyB0'
'cmVuIG5lbiBCQVQgS1ksIHZhIGAtLXR1LWtpZW0tcHJvYmVgIGdvaSB0aGFuZyBjaHVuZyBkZSBraWVtIGNoaW5oIGJvIGRv'
'LgoKZGVmIF9zYW4odCk6CiAgICBkID0gUGF0aCh0KS8iZCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5t'
'a2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgcmV0dXJuIGQsIGN3LCBwZgoKZGVmIGRvX244KGdv'
'aSwgc2lnLCB0ZXB0KToKICAgICIiIkJ1b2MgMSAoQ09OR19DVV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0LmV4ZS4gRG9pIGNo'
'dW5nIGR1b25nOiBnaXQuZXhlIFZBTiBwaGFpIG5oYW4uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBv'
'cmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIGZvciB0ZW4gaW4gKCJn'
'aXQuZXhlIiwgImdpdC5iYXQiLCAiZ2l0LmNtZCIsICJnaXQucHkiLCAia2hvbmctcGhhaS1naXQudHh0Iik6CiAgICAgICAg'
'ICAgIGYgPSBkL3RlbjsgZi53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyA9IGdv'
'aShjb25nX2N1X2dpdD1zdHIoZiksIHBhdGg9IiIsIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAg'
'ICAgICAgIGtxW2YiQ09OR19DVV9HSVQ9e3Rlbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIlRVIENIT0kiCiAgICBsb3QgPSBb'
'ayBmb3IgaywgdiBpbiBrcS5pdGVtcygpIGlmIHYgPT0gIk5IQU4iIGFuZCBub3Qgay5lbmRzd2l0aCgiZ2l0LmV4ZSIpXQog'
'ICAgaWYga3EuZ2V0KCJDT05HX0NVX0dJVD1naXQuZXhlIikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kg'
'Y2h1bmcgZHVvbmcgaG9uZzogZ2l0LmV4ZSBob3AgbGUgbWEgYmkgdHUgY2hvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBu'
'b3QgbG90IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IGxvdCBlbHNlIGYiY29uIG5oYW46IHtsb3R9IiksIGtxCgpkZWYgZG9f'
'bjkoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiTXVjIFBBVEggYm9jIG5oYXkga2VwIHBoYWkgTkhBTjsgbXVjIHJvbmcgLyB0'
'b2FuIGtob2FuZyB0cmFuZyBwaGFpIGJvIHF1YSwga2hvbmcgbmVtLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmls'
'ZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBkLm1rZGlyKCk7IGN3'
'ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgICAgICAoZC8i'
'Z2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGZvciBuaGFuLCBtdWMgaW4gKCgi'
'a2hvbmcgbmhheSIsIHN0cihkKSksICgiY28gbmhheSBrZXAiLCBmJyJ7ZH0iJyksCiAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgKCJyb25nIiwgIiIpLCAoImNoaSBraG9hbmcgdHJhbmciLCAiICAgIikpOgogICAgICAgICAgICB0cnk6CiAgICAgICAg'
'ICAgICAgICByLCBfID0gZ29pKHBhdGg9bXVjLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAg'
'ICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIKICAgICAgICAgICAgZXhjZXB0'
'IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gZiJORU0ge3R5cGUoZSkuX19u'
'YW1lX199IgogICAgaWYga3EuZ2V0KCJQQVRIIGtob25nIG5oYXkiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwg'
'ImRvaSBjaHVuZyBkdW9uZyBob25nOiBtdWMgUEFUSCB0aHVvbmcgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAg'
'b2sgPSAoa3EuZ2V0KCJQQVRIIGNvIG5oYXkga2VwIikgPT0gIk5IQU4iCiAgICAgICAgICBhbmQga3EuZ2V0KCJQQVRIIHJv'
'bmciKSA9PSAiTm9uZSIgYW5kIGtxLmdldCgiUEFUSCBjaGkga2hvYW5nIHRyYW5nIikgPT0gIk5vbmUiKQogICAgcmV0dXJu'
'IChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKIyBEYXUgcGhhbiBjYWNo'
'IGR1bmcgREUgVEhVLiBQaGFpIEtIQUMgb3MucGF0aHNlcCB0cmVuIENBIEhBSSBuZW4gKCc7JyBXaW5kb3dzLCAnOicgUE9T'
'SVgpCiMgdGhpIGhhaSBnaWEgdGh1eWV0ICJ0YWNoIHRoZW8gZGF1IGR1b2MgdHJ1eWVuIiB2YSAidGFjaCB0aGVvIG9zLnBh'
'dGhzZXAiIG1vaSByb2kgcmEgbmhhdS4KVEhVX04xMCA9ICJ8IgoKZGVmIGRvX24xMChnb2ksIHNpZywgdGVwdCk6CiAgICAi'
'IiJIYW0gcGhhaSB0YWNoIFBBVEggdGhlbyBkYXUgcGhhbiBjYWNoIERVT0MgVFJVWUVOLCBraG9uZyB0aGVvIG9zLnBhdGhz'
'ZXAgY3VhIG5lbi4KCiAgICBCYW4gY3UgZG8gIm1vdCBkYXUgJzsnIHRyb25nIFRFTiB0aHUgbXVjIiB2YSBkYXQgREFUIHRy'
'ZW4gV2luZG93cyBkdSBoYW0gc2FpLiBObwogICAgZGVnZW5lcmF0ZTogdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEg'
'JzsnLCBuZW4gJ0M6L2E7YicgdGhhdCBzdSBDTyBOR0hJQSBsYSBoYWkKICAgIG11YyDigJQgInRhY2ggZHVuZyIgdmEgInRh'
'Y2ggc2FpIiBjaG8gcmEgY3VuZyBrZXQgcXVhLCBwaGVwIGRvIGtob25nIHRoZSBkbyBuYW8uIE5vCiAgICBkYSBjaGFtIERB'
'VCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQg'
'YXkuCiAgICBNb3QgY29uZyBraG9uZyB0aGUgZG8gdGhpIGtob25nIHBoYWkgY29uZy4KICAgICIiIgogICAgdGVuX3NlcCA9'
'IG5leHQoKGsgZm9yIGsgaW4gKCJwaGFuX2NhY2giLCAiZGF1X3BoYW5fY2FjaCIsICJzZXAiKSBpZiBrIGluIHNpZy5wYXJh'
'bWV0ZXJzKSwgTm9uZSkKICAgIGlmIHRlbl9zZXAgaXMgTm9uZToKICAgICAgICAjIEtob25nIGNvIHRoYW0gc28gdGhpIHRy'
'ZW4gV2luZG93cyBLSE9ORyBjb24gZHVvbmcgbmFvIHRhY2ggaGFpIGdpYSB0aHV5ZXQuCiAgICAgICAgaWYgb3MucGF0aHNl'
'cCA9PSAiOyI6CiAgICAgICAgICAgIHJldHVybiAoS0RELCAidHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIHZh'
'IGhhbSBraG9uZyBuaGFuIHRoYW0gc28gZGF1IHBoYW4gY2FjaCAiCiAgICAgICAgICAgICAgICAgICAgICAgICAiLT4ga2hv'
'bmcgdGFjaCBkdW9jIGhhaSBnaWEgdGh1eWV0IiwKICAgICAgICAgICAgICAgICAgICB7Im9zLnBhdGhzZXAiOiBvcy5wYXRo'
'c2VwLCAidGhhbSBzbyBzZXAiOiBOb25lfSkKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFz'
'IHQ6CiAgICAgICAgICAgIGxhID0gUGF0aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKQogICAgICAgICAgICBkLCBjdywgcGYg'
'PSBfc2FuKHQpCiAgICAgICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAg'
'ICAgICAgICAgIHIsIF8gID0gZ29pKHBhdGg9c3RyKGxhKSArIG9zLnBhdGhzZXAgKyBzdHIoZCksIHByb2dyYW1fZmlsZXM9'
'c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIHIwLCBfID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVz'
'PXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28g'
'c2VwIjogTm9uZSwKICAgICAgICAgICAgICAiY28gbXVjIGNodWEgJzsnIjogIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIsCiAg'
'ICAgICAgICAgICAgImRvaSBjaHVuZyBkdW9uZyAoa2hvbmcgY28gJzsnKSI6ICJOSEFOIiBpZiByMCBlbHNlICJOb25lIn0K'
'ICAgICAgICBpZiBub3QgcjA6CiAgICAgICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZyIsIGtxCiAg'
'ICAgICAgcmV0dXJuIChEQVQgaWYgciBlbHNlIFRSVU9UKSwgKCIiIGlmIHIgZWxzZSAibXVjIGdpdC5leGUgaG9wIGxlIGJp'
'IE1BVCIpLCBrcQoKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBsYSA9IFBh'
'dGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkgICAgICAgICAgIyAnOycgbmFtIHRyb25nIFRFTiwga2hvbmcgcGhhaSBkYXUg'
'cGhhbiBjYWNoCiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgi'
'eCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgbm9pID0gc3RyKGxhKSArIFRIVV9OMTAgKyBzdHIoZCkKICAgICAgICBr'
'dyA9IGRpY3QocHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICByX2NoaW5oLCBfID0gZ29pKHBh'
'dGg9bm9pLCAgICAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyB0YWNoIGR1bmcgIC0+IE5IQU4KICAgICAg'
'ICByX2R1b25nLCBfID0gZ29pKHBhdGg9c3RyKGQpLCAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyBkb2kg'
'Y2h1bmcgZHVvbmcKICAgICAgICByX3BoYW5iaWV0LCBfID0gZ29pKHBhdGg9bm9pLCAgICoqe3Rlbl9zZXA6IG9zLnBhdGhz'
'ZXB9LCAqKmt3KSAgIyB0YWNoIHRoZW8gb3MucGF0aHNlcCAtPiBtYXQKICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0'
'aHNlcCwgInRoYW0gc28gc2VwIjogdGVuX3NlcCwgImRhdSB0aHUiOiBUSFVfTjEwLAogICAgICAgICAgZiJub2kgYmFuZyB7'
'VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9IjogICAgICAgIk5IQU4iIGlmIHJfY2hpbmggZWxzZSAiTm9uZSIs'
'CiAgICAgICAgICBmImRvaSBjaHVuZyBkdW9uZyAobW90IG11Yywge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9KSI6ICAiTkhBTiIg'
'aWYgcl9kdW9uZyBlbHNlICJOb25lIiwKICAgICAgICAgIGYicGhhbiBiaWV0OiBub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rl'
'bl9zZXB9PXtvcy5wYXRoc2VwIXJ9IjogIk5IQU4iIGlmIHJfcGhhbmJpZXQgZWxzZSAiTm9uZSJ9CiAgICBpZiBub3Qgcl9k'
'dW9uZzoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG1vdCBtdWMgaG9wIGxlIG1hIGtob25n'
'IHRpbSByYSBnaXQuZXhlIiwga3EKICAgICMgQ29uZyBwaGFpIENPIFRIRSBkby4gTmV1IGNhIGhhaSBkYXUgcGhhbiBjYWNo'
'IGRldSByYSBOSEFOIHRoaSBwaGVwIGRvIGtob25nIHBoYW4KICAgICMgYmlldCBkdW9jIGdpIOKAlCBkdW5nIGJhbyBEQVQs'
'IGJhbyB0aGFuZyBsYSBraG9uZyBkbyBkdW9jLgogICAgaWYgcl9waGFuYmlldDoKICAgICAgICByZXR1cm4gKEtERCwgZiJw'
'aGVwIGRvIEtIT05HIHBoYW4gYmlldCBkdW9jOiBub2kgYmFuZyB7VEhVX04xMCFyfSBtYSB0YWNoIHRoZW8gIgogICAgICAg'
'ICAgICAgICAgICAgICBmIntvcy5wYXRoc2VwIXJ9IFZBTiB0aW0gcmEgZ2l0LmV4ZSIsIGtxKQogICAgcmV0dXJuICgoREFU'
'LCAiIiwga3EpIGlmIHJfY2hpbmggZWxzZQogICAgICAgICAgICAoVFJVT1QsIGYidGFjaCB0aGVvIG9zLnBhdGhzZXAgdGhh'
'eSB2aSB0aGVvIHt0ZW5fc2VwfSBkdW9jIHRydXllbiIsIGtxKSkKCgpkZWYgZG9fbjExKGdvaSwgc2lnLCB0ZXB0KToKICAg'
'ICIiIlRydXllbiBjaGFuX2RvYW4gPT4gdGh1IGR1b2MgdGhvbmcgYmFvIFZBIHN0ZGVyciBJTS4gS2hvbmcgdHJ1eWVuID0+'
'IHN0ZGVyciBWQU4gY28uIiIiCiAgICBpZiAiY2hhbl9kb2FuIiBub3QgaW4gc2lnLnBhcmFtZXRlcnM6CiAgICAgICAgcmV0'
'dXJuIEtERCwgIl9naXRfd2luZG93cyBraG9uZyBuaGFuIHRoYW0gc28gY2hhbl9kb2FuIiwgeyJ0aGFtIHNvIjogbGlzdChz'
'aWcucGFyYW1ldGVycyl9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwg'
'Y3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIp'
'CiAgICAgICAgY2QgPSBbXQogICAgICAgIF8sIGVfY28gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBm'
'KSwgY3dkPXN0cihjdyksIGNoYW5fZG9hbj1jZCkKICAgICAgICBfLCBlX2toID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFt'
'X2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAga3EgPSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAobXVjKSI6IGxlbihj'
'ZCksCiAgICAgICAgICAic3RkZXJyIGtoaSBDTyBjaGFuX2RvYW4gKGJ5dGUpIjogbGVuKGVfY28uZW5jb2RlKCkpLAogICAg'
'ICAgICAgInN0ZGVyciBraGkgS0hPTkcgdHJ1eWVuIChieXRlKSI6IGxlbihlX2toLmVuY29kZSgpKX0KICAgIGlmIGxlbihj'
'ZCkgPT0gMCBhbmQgbGVuKGVfa2guZW5jb2RlKCkpID09IDA6CiAgICAgICAgcmV0dXJuIEtERCwgIm5oYW5oICVQcm9ncmFt'
'RmlsZXMlIGtob25nIHBoYW4gZ2lhaSBLSE9ORyBiYXkgcmEgY2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRvIGR1b2MiLCBrcQog'
'ICAgb2sgPSBsZW4oY2QpID4gMCBhbmQgbGVuKGVfY28uZW5jb2RlKCkpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA+'
'IDAKICAgIHJldHVybiAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCmRl'
'ZiBkb19uMTIoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiSGFuZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9uZyBmaXh0dXJlIHBo'
'YWkgdHV5ZXQgZG9pIHRyZW4gQ0EgSEFJIG5lbi4iIiIKICAgIG5kID0gdGVwdC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04'
'IiwgZXJyb3JzPSJyZXBsYWNlIikKICAgIGhhbmcgPSBzb3J0ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRfcGF0aFxzKj1ccyoi'
'KFteIl0rKSInLCBuZCkpKQogICAgeGF1ID0gW2ggZm9yIGggaW4gaGFuZyBpZiBub3QgKFB1cmVQb3NpeFBhdGgoaCkuaXNf'
'YWJzb2x1dGUoKSBhbmQgUHVyZVdpbmRvd3NQYXRoKGgpLmlzX2Fic29sdXRlKCkpXQogICAga3EgPSB7ImhhbmcgZ2l0X3Bh'
'dGggdGltIHRoYXkiOiBoYW5nLCAiY2hpIHR1eWV0IGRvaSBNT1QgbmVuIjogeGF1fQogICAgaWYgbm90IGhhbmc6CiAgICAg'
'ICAgcmV0dXJuIEtERCwgImtob25nIHRpbSB0aGF5IGhhbmcgZ2l0X3BhdGggbmFvIHRyb25nIGZpeHR1cmUgLT4gbWF1IGRv'
'YyBjbyB0aGUgZGEgZG9pIiwga3EKICAgIHJldHVybiAoREFUIGlmIG5vdCB4YXUgZWxzZSBUUlVPVCksICgiIiBpZiBub3Qg'
'eGF1IGVsc2UgZiJjaGktbW90LW5lbjoge3hhdX0iKSwga3EKClBST0JFID0gWygiTjggYnVvYyAxIGNoaSBuaGFuIGdpdC5l'
'eGUiLCBkb19uOCksCiAgICAgICAgICgiTjkgYm9jIG5oYXkga2VwIG8gbXVjIFBBVEgiLCBkb19uOSksCiAgICAgICAgICgi'
'TjEwIGRhdSAnOycgdHJvbmcgdGVuIHRodSBtdWMiLCBkb19uMTApLAogICAgICAgICAoIk4xMSBjaGFuIGRvYW4gZG9pIGtl'
'bmgiLCBkb19uMTEpLAogICAgICAgICAoIk4xMiBoYW5nIHNlbnRpbmVsIHR1eWV0IGRvaSBDQSBIQUkgbmVuIiwgZG9fbjEy'
'KV0KCiMgLS0tIGNoZSBkbyBUVSBLSUVNOiBjaGF5IG5hbSBwcm9iZSB0cmVuIG1vdCBjYXkgYmF0IGt5LCBuZW4gYmF0IGt5'
'IC0tLQppZiAiLS10dS1raWVtLXByb2JlIiBpbiBzeXMuYXJndjoKICAgIF9nID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5p'
'bmRleCgiLS10dS1raWVtLXByb2JlIikgKyAxXSkucmVzb2x2ZSgpCiAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zy'
'b21fZmlsZV9sb2NhdGlvbigibHBfdGsiLCBzdHIoX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgIF9scCA9IGlt'
'cG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbHApCiAgICBfc2ln'
'ID0gaW5zcGVjdC5zaWduYXR1cmUoX2xwLl9naXRfd2luZG93cykKICAgIGRlZiBfZ29pKCoqa3cpOgogICAgICAgIGUgPSBp'
'by5TdHJpbmdJTygpCiAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICAgICAgcmV0'
'dXJuIF9scC5fZ2l0X3dpbmRvd3MoKiprdyksIGUuZ2V0dmFsdWUoKQogICAgcHJpbnQoZiJUVSBLSUVNIFBST0JFIHRyZW4g'
'e19nfSAgKG5lbiB7c3lzLnBsYXRmb3JtfSkiKQogICAgZm9yIF90ZW4sIF9mIGluIFBST0JFOgogICAgICAgIF90dCwgX2N0'
'LCBfZGwgPSBfZihfZ29pLCBfc2lnLCBfZy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBwcmludChm'
'IiAgW3tfdHQ6MTR9XSB7X3Rlbn0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgICAgICBmb3IgX2ssIF92'
'IGluIChfZGwgb3Ige30pLml0ZW1zKCk6IHByaW50KGYiICAgICAgICB7X2s6MzR9OiB7X3Z9IikKICAgIHN5cy5leGl0KDAp'
'CgojIC0tLSBjaGUgZG8gS0lFTSBET05HIEJPOiB0ZXAgLnB5IG5heSBwaGFpIFRSVU5HIFRVTkcgQllURSB2b2kgYmFuIG5o'
'dW5nIHRyb25nIHBzMSAtLS0KIyBLaG9uZyBjb25nIG5hbyBidW9jIGhhaSBiYW4gc2FvIGtob3A6IGRvIGR1b2MsIG5vaSB0'
'cmFuIDIvNDAwIC0+IDk5Lzk5OTk5IENISSB0cm9uZyAucHkKIyB0aGkgY2lfZGFuZ19reSBsYW4gdDI2L3QyNyB2YW4geGFu'
'aCwgY29uIGNob3QgU0hBIGN1YSBwczEgY2hpIHNvIGJhbiBuaHVuZyB2b2kgaGFuZyBzbwojIGN1YSBDSElOSCBuby4gQ2hh'
'eTogcHl0aG9uIHdwNTQxLWRvLWcyLXdpbmRvd3MucHkgLS1raWVtLWRvbmctYm8gd3A1NDEtZG8tZzIucHMxICAocmMgMHwz'
'KQppZiAiLS1raWVtLWRvbmctYm8iIGluIHN5cy5hcmd2OgogICAgaW1wb3J0IGJhc2U2NAogICAgX3BzID0gUGF0aChzeXMu'
'YXJndltzeXMuYXJndi5pbmRleCgiLS1raWVtLWRvbmctYm8iKSArIDFdKS5yZWFkX3RleHQoZW5jb2Rpbmc9ImFzY2lpIikK'
'ICAgIF9tID0gcmUuc2VhcmNoKHIiKD9tcyleXCRCNjQgPSBAXCgoLio/KV5cKSIsIF9wcykKICAgIF9rID0gcmUuc2VhcmNo'
'KHIiKD9tKV5cJFNoYUJvRG9ccyo9XHMqJyhbMC05YS1mXXs2NH0pJyIsIF9wcykKICAgIF9uaHVuZyA9IGJhc2U2NC5iNjRk'
'ZWNvZGUoIiIuam9pbihyZS5maW5kYWxsKHIiJyhbQS1aYS16MC05Ky89XSopJyIsIF9tLmdyb3VwKDEpKSkpIGlmIF9tIGVs'
'c2UgYiIiCiAgICBfdG9pID0gUGF0aChfX2ZpbGVfXykucmVhZF9ieXRlcygpCiAgICBfb2sgPSBib29sKF9tIGFuZCBfaykg'
'YW5kIF9uaHVuZyA9PSBfdG9pIGFuZCBoYXNobGliLnNoYTI1NihfdG9pKS5oZXhkaWdlc3QoKSA9PSBfay5ncm91cCgxKQog'
'ICAgaW5uKGYiS0lFTSBET05HIEJPOiB7REFUIGlmIF9vayBlbHNlIEtERH0gIChuaHVuZyB7bGVuKF9uaHVuZyl9IGJ5dGUs'
'IHRlcCB7bGVuKF90b2kpfSBieXRlKSIpCiAgICBzeXMuZXhpdCgwIGlmIF9vayBlbHNlIDMpCgppbm4oIj0iICogNzgpOyBp'
'bm4oIldQNTQxIGcyIC0gcGhlcCBkbyB0cmVuIFdpbmRvd3MgdGhhdCAoc3BlYyByMzogTjEtTjQsIE44LU4xMiwgTjcsIGtp'
'Y2ggdGh1b2MpIik7IGlubigiPSIgKiA3OCkKCiMgLS0tLS0tLS0tLS0tLS0tLSB0dSBraWVtIGJvIGRvYyAtLS0tLS0tLS0t'
'LS0tLS0tCl9kLCBfZywgX3QgPSBkb2NfZG8oX01BVSkKX29rID0gKGxlbihfZCkgPT0gMiBhbmQgYW55KHguc3RhcnRzd2l0'
'aCgidDAyYiIpIGZvciB4IGluIF9kKQogICAgICAgYW5kIG5vdCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMxIikgZm9yIHggaW4g'
'X2QpIGFuZCBfdCkKaW5uKCJUdSBraWVtIGJvIGRvYyBsb2c6IiwgREFUIGlmIF9vayBlbHNlIFRSVU9UKQppZiBub3QgX29r'
'OgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBibyBkb2MgbG9nIGN1YSBjaGluaCBzY3JpcHQgbmF5IHNhaSAt'
'PiBraG9uZyBkbyBnaSBjYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4gZG8gLS0tLS0tLS0t'
'LS0tLS0tLQpnb2MgPSBQYXRoKHN5cy5hcmd2WzFdKS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQYXRo'
'LmN3ZCgpCnRlcCwgdGVwdCA9IGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAib3BzIiAvICJsZWFz'
'ZV9wdWJsaXNoX3Rlc3QucHkiCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMC4gTkVOIERPIikKIyBNT0kgTE9HIFBI'
'QUkgVFUgS0hBSSBubyBkbyBDQUkgR0kgYmFuZyBCTyBETyBOQU8uIEJhaSBob2MgMTktMDktMjAyNjogbW90IGx1b3QgZG8K'
'IyBndWkgdmUgZHVvYyBkb2Mgbmh1IGtldCBxdWEgY3VhIGJhbiB2YSBkYW5nIHhldCwgbmh1bmcgdGhhdCByYSBsYSBiYW4g'
'ZG8gQ1UgY2hheQojIHRyZW4gbmhhbmggS0hBQy4gRG9jIHJhIHRoaSBtYXQgbW90IHZvbmc7IGxvZyB0dSBraGFpIHRoaSB0'
'aGF5IG5nYXkgZG9uZyBkYXUuCnRyeToKICAgIF90dSA9IGhhc2hsaWIuc2hhMjU2KFBhdGgoX19maWxlX18pLnJlYWRfYnl0'
'ZXMoKSkuaGV4ZGlnZXN0KCkKZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgIF90dSA9IGYia2hvbmcgdHUgYmFtIGR1b2M6'
'IHtfZX0iCmdoaSgiYm9fZG9fc2hhMjU2IiwgX3R1KQppbm4oZiIgIEJPIERPICAgICAgICA6IHNoYTI1NiB7X3R1WzoxNl19'
'ICAoYmFuIHtCQU5fQk9fRE99KSIpCmlubigiICBzeXMucGxhdGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwgInwgcHl0aG9uIiwg'
'c3lzLnZlcnNpb24uc3BsaXQoKVswXSkKaW5uKCIgIG9zLnBhdGhzZXAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSwgInwgUEFU'
'SEVYVDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQQVRIRVhUIikpWzo2MF0pCmlubigiICBQcm9ncmFtRmlsZXMgOiIsIHJl'
'cHIob3MuZW52aXJvbi5nZXQoIlByb2dyYW1GaWxlcyIpKSwgInwgU3lzdGVtUm9vdDoiLCByZXByKG9zLmVudmlyb24uZ2V0'
'KCJTeXN0ZW1Sb290IikpKQppbm4oIiAgQ09OR19DVV9HSVQgIDoiLCByZXByKF9DT05HX0NVX0dJVF9OR1VPSV9ETykKICAg'
'ICsgKCIgIC0+IERBIEJPIGtob2kgbHVvdCBkbyAoQ0kga2hvbmcgZGF0IGJpZW4gbmF5OyB4ZW0gZGF1IHRlcCkiIGlmIF9D'
'T05HX0NVX0dJVF9OR1VPSV9ETyBpcyBub3QgTm9uZSBlbHNlICIiKSkKZ2hpKCJjb25nX2N1X2dpdF9uZ3VvaV9kbyIsIF9D'
'T05HX0NVX0dJVF9OR1VPSV9ETykKX2Jhc2hfYm8gPSBnaGkoImJpZW5fYmFzaF9uZ3VvaV9kb19kYV9ibyIsIHNvcnRlZChr'
'IGZvciBrIGluIG9zLmVudmlyb24gaWYgX2JpZW5fYmFzaChrKSkpCmlubigiICBiaWVuIGJhc2ggICAgOiIsICgiLCAiLmpv'
'aW4oX2Jhc2hfYm8pICsgIiAgLT4gREEgQk8ga2hvaSBsdW90IGNvbiAoQ0kga2hvbmcgZGF0OyB4ZW0gY2hheSgpKSIpIGlm'
'IF9iYXNoX2JvIGVsc2UgIihraG9uZyBjbykiKQppbm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5vbmUK'
'aWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4gPSBib29s'
'KGN0eXBlcy53aW5kbGwuc2hlbGwzMi5Jc1VzZXJBbkFkbWluKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXllbiA9IE5v'
'bmUKZ2hpKCJxdXllbl9hZG1pbiIsIHF1eWVuKQpzeW1saW5rX2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVtcGZpbGUu'
'VGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3RleHQoIngi'
'LCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHRyeTogb3Muc3ltbGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJsayIpKTsg'
'c3ltbGlua19kdW9jID0gVHJ1ZQogICAgICAgIGV4Y2VwdCBPU0Vycm9yIGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZhbHNlOyBn'
'aGkoInN5bWxpbmtfbG9pIiwgZiJ7dHlwZShlKS5fX25hbWVfX306IHtlfSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZTogZ2hp'
'KCJzeW1saW5rX2xvaSIsIHN0cihlKSkKZ2hpKCJzeW1saW5rX2R1b2MiLCBzeW1saW5rX2R1b2MpCmlubigiICBBZG1pbmlz'
'dHJhdG9yOiIsIHF1eWVuLCAifCB0YW8gc3ltbGluayBkdW9jOiIsIHN5bWxpbmtfZHVvYykKCmxvaSA9IFtdCiMgQ29uZyBr'
'aWNoIHRodW9jIGxhIHBoZXAgZG8gdHJlbiBMSUNIIFNVIEdJVCwga2hvbmcgZGluaCBnaSBkZW4gbmVuLiBDaG8gcGhlcAoj'
'IC0tY2hpLWtpY2gtdGh1b2MgY2hheSBvIG1vaSBuZW4gZGUgY29uIFRVIEtJRU0gZHVvYyBjaGluaCBjb25nIG5heSAoZGEg'
'ZHVuZwojIGRlIHRhaSBkdW5nIGNhIGhhaSB2ZSBjdWEgc3UgY28gbmVuLWN1IDE5LTA5KS4gTW9pIGNob3QgQ0hVQyBOQU5H'
'IHZhbiBkb2kgV2luZG93cy4KaWYgc3lzLnBsYXRmb3JtICE9ICJ3aW4zMiIgYW5kICItLWNoaS1raWNoLXRodW9jIiBub3Qg'
'aW4gc3lzLmFyZ3Y6CiAgICBsb2kuYXBwZW5kKGYiS0hPTkcgcGhhaSBXaW5kb3dzIChzeXMucGxhdGZvcm09e3N5cy5wbGF0'
'Zm9ybSFyfSkiKQppZiBub3QgdGVwLmlzX2ZpbGUoKTogIGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB9IikKaWYgbm90'
'IHRlcHQuaXNfZmlsZSgpOiBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwdH0iKQppZiBub3Qgc2h1dGlsLndoaWNoKCJn'
'aXQiKTogbG9pLmFwcGVuZCgia2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCIpCiMgQm8gdGVzdCAobXVjIDIgdmEgTjcpIGNh'
'biBQeVlBTUw6IHRoaWV1IG5vLCAwZWE5NWRlIHJhIDk2LzE2NiBjYSBETyAoODkgYmFvIHRoYW5nICJObyBtb2R1bGUgbmFt'
'ZWQgJ3lhbWwnIiwKIyA3IHF1YSBsdW90IGNvbjsgY28gUHlZQU1MOiAxNjYvMTY2IFFVQSkuIEJvIGRvIGdvaSBjaHVuZyBs'
'YSAiY2EgRE8gTEEiIHJvaSBwaGF0IFRSVU9UIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBjLgojIERpZXUga2llbiB0aWVuIHF1'
'eWV0IHBoYWkgaG9pIGJhbmcgQ0hJTkggdGllbiB0cmluaCBjb24gc2UgY2hheSBibyB0ZXN0IChjaGF5KCk6IGN1bmcgbW9p'
'IHRydW9uZzsgY3dkID0gb3BzLyA9CiMgc3lzLnBhdGhbMF0gY3VhIGJvIHRlc3QpIHZhIGhvaSBEVU5HIERVT0MgY2h1IGto'
'b25nIGhvaSBDTyBNQVQuIEJhbiAzMGQgaG9pIGBmaW5kX3NwZWMoInlhbWwiKWAgbyB0aWVuIHRyaW5oCiMgTkFZIHZhIG5n'
'dW9uZyAzLjggc3V5IHR1IE5HVSBQSEFQIChgOj1gKSDigJQgZG8gdHJlbiAyMDI2LTA5LTMwZCwgY2EgaGFpIHJhIHJjPTEg'
'VFJVT1QgY2hvIHVuZyB2aWVuIHNhY2g6CiMgdGh1IG11YyBkdSBsaWV1IGB5YW1sL2AgdHJlbiBQWVRIT05QQVRIIHF1YSBm'
'aW5kX3NwZWMgbWEgYHlhbWwuc2FmZV9kdW1wYCBraG9uZyBjbyAoODcgY2EgImxhIik7IHB5dGhvbiAzLjguMjAKIyBUSEFU'
'IGNvIFB5WUFNTCwgYm8gdGVzdCBkdW5nIGBzdHIucmVtb3ZlcHJlZml4YCAoMy45KSBsdWMgQ0hBWSAoMzMgY2EgImxhIjsg'
'My45LjIzOiAxNjYvMTY2KS4KIyAiRHVuZyBkdW9jIiBuZ2hpYSBsYSBkdW5nIERVTkcgQVBJIGJvIHRlc3QgZ29pOiB2aWV0'
'KCkgKDQzIGxvaSBnb2kpIHZhIGxlYXNlX3B1Ymxpc2gucHkgZ29pIHNhZmVfZHVtcCguLi4sIGFsbG93X3VuaWNvZGU9VHJ1'
'ZSwKIyBzb3J0X2tleXM9RmFsc2UpLCBtYSBgc29ydF9rZXlzYCBjaGkgY28gdHUgUHlZQU1MIDUuMS4gRG8gdHJlbiAyMDI2'
'LTA5LTMwbCwgMGVhOTVkZTogcHl0aG9uIDMuOS4yMyArIFB5WUFNTCAzLjEzIFRIQVQgcXVhIHByb2JlCiMgY3UgKHJjPTAp'
'LCBibyB0ZXN0IDEwOS8xNjYg4oCUIDU2IGNhICJsYSI6IDUyIGB1bmV4cGVjdGVkIGtleXdvcmQgYXJndW1lbnQgJ3NvcnRf'
'a2V5cydgLCB0MjYvdDI3IGBSZWFkZXJFcnJvcmAgKGt5IHR1IG5nb2FpIEJNUCksCiMgdDEyNC90MTUzIERPIHRoZW8gbHVv'
'dCBjb24g4oCUIGUyZSByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYDsgUHlZQU1MIDUuMTogMTY2LzE2NiAoZG8gbGFpIDIwMjYt'
'MTAtMDE6IGN1bmcgc28pLgojIChQeXRob24gPj0gMy4xMCArIFB5WUFNTCAzLjEzIGRhIHRydW90IHByb2JlIGN1IHZpIGBj'
'b2xsZWN0aW9ucy5IYXNoYWJsZWAuKSBQcm9iZSBjdWEgcHMxICgkbWFUaHUpIHBoYWkgR0lPTkcgSEVUIGRvbmcgZHVvaS4K'
'aWYgbm90ICgiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Ygb3IgIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndik6CiAg'
'ICBfcmNfZGssIF9yYV9kayA9IGNoYXkoWyItYyIsICJpbXBvcnQgc3lzOyBzeXMuZXhpdCg5KSBpZiBzeXMudmVyc2lvbl9p'
'bmZvIDwgKDMsIDkpIGVsc2UgTm9uZTsgaW1wb3J0IHlhbWw7IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAi'
'IHlhbWwuc2FmZV9kdW1wKHlhbWwuc2FmZV9sb2FkKCdhOiAxJyksIGFsbG93X3VuaWNvZGU9VHJ1ZSwgc29ydF9rZXlzPUZh'
'bHNlKSJdLAogICAgICAgICAgICAgICAgICAgICAgICAgIGdvYyAvICJvcHMiIGlmIChnb2MgLyAib3BzIikuaXNfZGlyKCkg'
'ZWxzZSBQYXRoLmN3ZCgpLCBwaHV0PTIpCiAgICBpZiBfcmNfZGsgPT0gOToKICAgICAgICBsb2kuYXBwZW5kKGYicHl0aG9u'
'IHtzeXMudmVyc2lvbi5zcGxpdCgpWzBdfSA8IDMuOTogYm8gdGVzdCBjdWEgdW5nIHZpZW4gZHVuZyBzdHIucmVtb3ZlcHJl'
'Zml4ICgzLjkpIGx1YyBDSEFZIikKICAgIGVsaWYgX3JjX2RrOgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24gbmF5IEtI'
'T05HIGNvIFB5WUFNTCBkdW5nIGR1b2MgKHsoX3JhX2RrLnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10pWy0xXVs6OTBd'
'fSk6IgogICAgICAgICAgICAgICAgICAgZiIgXCJ7c3lzLmV4ZWN1dGFibGV9XCIgLW0gcGlwIGluc3RhbGwgLVUgcHl5YW1s'
'IgogICAgICAgICAgICAgICAgICAgIiAoYmFuIG5odW5nIHBzMSB0dSB0YWkgS0hPTkcgY28gcGlwOiBjaGF5IGxhaSB2b2kg'
'LVB5IDxweXRob24gZGEgY28gUHlZQU1MPikiKQogICAgIyBCbyB0ZXN0IGNvbiBnb2kgYHNodXRpbC53aGljaGAgY2hvIGJh'
'c2gvYWN0aW9ubGludC9zaGVsbGNoZWNrICgwZWE5NWRlOiB0MzMgdDEzNyB0MTU5IGNhbiBhY3Rpb25saW50LCB0MTM3IGNh'
'bgogICAgIyBzaGVsbGNoZWNrLCBjYWMgY2EgY2hheSBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggY2FuIGJhc2gpLiBUaGlldSB0'
'aGkgY2FjIGNhIGF5IGluICJLSE9ORyBETyBEVU9DOiB0aGlldSBgLi4uYCIgdmEgYm8gZG8gcmEKICAgICMgcmM9MyDigJQg'
'bmh1bmcgY2hpIFNBVSBjYSBibyB0ZXN0IGxhbiBONyAoZG8gdHJlbiAyMDI2LTA5LTMwZywgUEFUSCB0aGlldSBhY3Rpb25s'
'aW50OiBgQ29uZyBjdSBkYXkgZHUgZGUgZG9gIEtERCwgcmM9MwogICAgIyBzYXUgMiBsdW90IGJvIHRlc3QpLiBDdW5nIGx5'
'IGRvIFB5WUFNTCBkdW9jIGhvaSBvIGRheTogaG9pIFRSVU9DLCBjdW5nIFBBVEggbWEgY2hheSgpIHRydXllbiBjaG8gYm8g'
'dGVzdC4KICAgICMgVkEgY3VuZyBDSE8gYm8gdGVzdCBkdW5nOiB0cmVuIFdpbmRvd3MgYHNodXRpbC53aGljaGAgdHJhIFRI'
'VSBNVUMgSElFTiBIQU5IIFRSVU9DIFBBVEgsIG1hIGJvIHRlc3QgY2hheSB2b2kgY3dkID0gZ29jIGNvbgogICAgIyB0aWVu'
'IHRyaW5oIG5heSBkdW5nIG8gY3dkIENVQSBOR1VPSSBETyAobm9pIGdvaSBwczEsIHZkLiBEb3dubG9hZHMg4oCUIGR1bmcg'
'bm9pIGdpYWkgbmVuIGFjdGlvbmxpbnQuZXhlKS4gRG8gdHJlbiAyMDI2LTA5LTMwawogICAgIyAobmhhbmggd2luMzIgVEhB'
'VCBjdWEgc2h1dGlsLndoaWNoKTogYWN0aW9ubGludCB0b3QgbyBjd2Qgbmd1b2kgZG8gKyBiYW4gaG9uZyBkYXUgUEFUSCA9'
'PiBtdWMgMCBob2kgYmFuIG8gY3dkIChyYz0wKSwgYm8gdGVzdAogICAgIyBkdW5nIGJhbiB0cmVuIFBBVEggPT4gcmM9MSBg'
'REFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0MzMnLCAndDEzNycsICd0MTU5J11gLiBHaWFpIHRlbiB2b2kgY3dkID0gZ29j'
'IHJvaSBnb2kgVEhBTkcgYmFuZyBkdW9uZwogICAgIyBUVVlFVCBET0kgZGEgZ2lhaSAocXVhIGhhbiB0aGkgcnVuKCkgZ2ll'
'dCBkdW5nIHRpZW4gdHJpbmgg4oCUIGx5IGRvIGJhbiAzMGkga2hvbmcgaG9pIHF1YSBjaGF5KCkpLgogICAgX2N3ZF9uZ3Vv'
'aV9kbyA9IG9zLmdldGN3ZCgpCiAgICB0cnk6CiAgICAgICAgaWYgZ29jLmlzX2RpcigpOiBvcy5jaGRpcihnb2MpCiAgICAg'
'ICAgX2NjID0ge2M6IChvcy5wYXRoLmFic3BhdGgocCkgaWYgcCBlbHNlIE5vbmUpIGZvciBjLCBwIGluCiAgICAgICAgICAg'
'ICAgICgoYywgc2h1dGlsLndoaWNoKGMpKSBmb3IgYyBpbiAoImJhc2giLCAiYWN0aW9ubGludCIsICJzaGVsbGNoZWNrIikp'
'fQogICAgZmluYWxseToKICAgICAgICBvcy5jaGRpcihfY3dkX25ndW9pX2RvKQogICAgX3RoaWV1X2NjID0gW2MgZm9yIGMs'
'IHAgaW4gX2NjLml0ZW1zKCkgaWYgbm90IHBdCiAgICBpZiBfdGhpZXVfY2M6CiAgICAgICAgbG9pLmFwcGVuZChmInRoaWV1'
'IGNvbmcgY3UgYm8gdGVzdCBnb2kgcXVhIFBBVEg6IHtfdGhpZXVfY2N9IChhY3Rpb25saW50OiBvcHMvY2FpX2FjdGlvbmxp'
'bnQuc2ggdm9pIEFMX1ZFUjsiCiAgICAgICAgICAgICAgICAgICAiIGJhc2g6IEdpdCBCYXNoLCBraG9uZyBwaGFpIGJhc2gu'
'ZXhlIGN1YSBXU0wpIikKICAgICMgc2hlbGxjaGVjayBLSE9ORyBuaGFuIC0tbm9yYyB0aGkgYWN0aW9ubGludCAxLjcuNyAo'
'dHUgdHJ1eWVuIC0tbm9yYykgbGFtIHQzMyBETywgdmEgU0hFTExDSEVDS19PUFRTPS0tbm9yYyBjdWEgY2hheSgpIGxhbQog'
'ICAgIyB0MTM3IERPIOKAlCBjYSAibGEiID0+IFRSVU9UIGdpYSAoZG8gdHJlbiAyMDI2LTA5LTMwaCwgc2hlbGxjaGVjayBn'
'aWEgdHUgY2hvaSAtLW5vcmM6IGJhbiAzMGggcmM9MSBgbGE6IFsndDMzJ11gIHNhdSBjYQogICAgIyBibyB0ZXN0KS4gYHdo'
'aWNoYCBjaGkgaG9pIENPIE1BVDsgbyBkYXkgaG9pIERVTkcgRFVPQy4gTmd1b25nIGRvIHRyZW4gc2hlbGxjaGVjayBUSEFU'
'OiAwLjQuNy8wLjUuMC8wLjYuMCB0dSBjaG9pIC0tbm9yYwogICAgIyAocmM9MyksIDAuNy4wIHRybyBsZW4gbmhhbi4gUGhl'
'cCBob2kgcGhhaSB0aGF5IERVTkcgU0hFTExDSEVDS19PUFRTIG1hIGNoYXkoKSBkYXQgY2hvIGx1b3QgY29uOiBiYW4gMzBp'
'IGhvaSB2b2kgYmllbiBDVUEKICAgICMgTkdVT0kgRE8g4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGksIHNoZWxsY2hlY2sgMC45'
'LjAgKyBTSEVMTENIRUNLX09QVFM9LS1leHRlbmRlZC1hbmFseXNpcz10cnVlIChjbyBjdWEgMC4xMCk6IHJjPTMgImtob25n'
'IG5oYW4KICAgICMgLS1ub3JjOiBjYXAgbmhhdCBzaGVsbGNoZWNrIiB0cm9uZyBraGkgdDMzL3QxMzcgcXVhIGNoYXkoKSBk'
'ZXUgMS8xLiBHb2kgVEhBTkcgKGtob25nIHF1YSBjaGF5KCkpOiBxdWEgaGFuIHRoaSBydW4oKSBnaWV0CiAgICAjIGR1bmcg'
'c2hlbGxjaGVjazsgcXVhIGNoYXkoKSB0aGkgY2hpIGdpZXQgcHl0aG9uIGNvbiwgc2hlbGxjaGVjayB0cmVvIG8gbGFpIG1v'
'IGNvaSAoZG8gdHJlbiAyMDI2LTA5LTMwaTogMS8xIGNvbiBzb25nKS4KICAgIGVsaWYgc3VicHJvY2Vzcy5ydW4oW19jY1si'
'c2hlbGxjaGVjayJdLCAiLS1ub3JjIiwgIi0tdmVyc2lvbiJdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0aW1lb3V0PTYwLAog'
'ICAgICAgICAgICAgICAgICAgICAgICBlbnY9ZGljdChvcy5lbnZpcm9uLCBTSEVMTENIRUNLX09QVFM9Ii0tbm9yYyIpKS5y'
'ZXR1cm5jb2RlOgogICAgICAgIGxvaS5hcHBlbmQoInNoZWxsY2hlY2sgdHJlbiBQQVRIIGtob25nIG5oYW4gLS1ub3JjIChh'
'Y3Rpb25saW50IDEuNy43IHZhIGNoYXkoKSBkZXUgdHJ1eWVuIGNvIGF5KTogY2FwIG5oYXQgc2hlbGxjaGVjayIpCiAgICAj'
'IGFjdGlvbmxpbnQgY3VuZyBwaGFpIERVTkcgRFVPQywga2hvbmcgY2hpIENPIE1BVDogdDMzL3QxMzcvdDE1OSBnb2kgbm8g'
'VEhBTkcsIHZhIG1vdCBhY3Rpb25saW50IGtob25nIGNoYXkgKHNhaSBraWVuIHRydWMsCiAgICAjIGhvbmcpIGxhbSBjYSBi'
'YSBETyAiYWN0aW9ubGludCBETyAocmM9Li4uKSIg4oCUIGNhICJsYSIgPT4gVFJVT1QgZ2lhIHNhdSBjYSBibyB0ZXN0IChk'
'byB0cmVuIDIwMjYtMDktMzBqOiBhY3Rpb25saW50IGdpYQogICAgIyByYz0xID0+IG11YyAwIGltIGxhbmcsIHQzMyAibGEi'
'KS4gQmFuIFRIQVQgMS42LjI3LzEuNy43LzEuNy44LzEuNy4xMiBkZXUgcmM9MCB2YSBkZXUgY2hvIHQzMy90MTM3L3QxNTkg'
'UVVBIHRyZW4gMGVhOTVkZS4KICAgICMgYmFzaCBxdWEgYHdoaWNoYCBDSEkgaG9pIENPIE1BVCwgY28gY2h1IGRpY2g6IHQz'
'NS10NDAgZ29pIGBiYXNoYCBUUkFOIChiYXNoIFdTTCBsYW0gY2h1bmcgRE8sIGRldSBOR09BSV9QSEFNX1ZJIOKAlCBkbyB0'
'cmVuCiAgICAjIDIwMjYtMDktMzBqKS4gOSBjYSBUUk9ORyBwaGFtIHZpIEtIT05HIGdvaSBiYXNoIHF1YSBgd2hpY2hgIOKA'
'lCB4ZW0gY2hvdCBgX2Jhc2hfcG9zaXgoKWAgZHVvaSBjaG90IGdpdC4KICAgICMgQ0hBWSBEVU9DIGNodWEgcGhhaSBEVU5H'
'IERVT0M6IGRvIHRyZW4gMjAyNi0wOS0zMGssIDBlYTk1ZGUsIGFjdGlvbmxpbnQgVEhBVCAxLjQuMy8xLjUuMC8xLjUuMy8x'
'LjYuMC8xLjYuOC8xLjYuMTUvMS42LjIwLwogICAgIyAxLjYuMjIgZGV1IGAtdmVyc2lvbmAgcmM9MCwgbWEgY2EgdGFtIGxh'
'bSB0MTM3L3QxNTkgRE8gKGBwcm9wZXJ0eSAicnVuX2F0dGVtcHQiLyJ3b3JrZmxvd19zaGEiIGlzIG5vdCBkZWZpbmVkYCks'
'IDEuNC4zLzEuNS4wCiAgICAjIHRoZW0gdDMzIChgbXVzdCBiZSBjb250YWluZWQgd2l0aGluICR7eyB9fWApIOKAlCBlMmUg'
'MS42LjIyOiByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCwgYGxhOiBbJ3QxMzcnLCAndDE1OSddYCBjaG8gdW5nIHZpZW4KICAg'
'ICMgc2FjaDsgMS42LjIzLzEuNi4yNC8xLjYuMjYvMS42LjI3LzEuNy4wLzEuNy42LzEuNy43LzEuNy4xMiBRVUEgY2EgYmEu'
'IFNhbiBsYSBiYW4KICAgICMgZ2hpbSBDSSAoQUxfU0FOKSwgS0hPTkcgcGhhaSAxLjYuMjMgZG8gdHJlbiBNT1QgdW5nIHZp'
'ZW46IHdvcmtmbG93IGN1YSB1bmcgdmllbiBzYXUgY28gdGhlIGR1bmcgY3UgcGhhcCBtb2kgaG9uLCBtYSBDSSBjaGkgZG8K'
'ICAgICMgYmFuZyBiYW4gZ2hpbS4gQ3UgaG9uIHNhbiA9PiBLSE9ORyBETyBEVU9DIChjaGFuIGNhIDEuNi4yMy0xLjcuNiBk'
'YW5nIFFVQTogZmFpbC1jbG9zZSwga2hvbmcgcGhhaSBwaGFuIHF1eWV0KS4gYHZgIGRhdTogYmFuCiAgICAjIGBnbyBpbnN0'
'YWxsYCBpbiBgdjEuNy43YDsga2hvbmcgZG9jIGR1b2Mgc28gKHZkLiBgKGRldmVsKWApID0+IEtIT05HIERPIERVT0MuCiAg'
'ICBpZiBub3QgX3RoaWV1X2NjOgogICAgICAgIF9hbCA9IHN1YnByb2Nlc3MucnVuKFtfY2NbImFjdGlvbmxpbnQiXSwgIi12'
'ZXJzaW9uIl0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwKICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PTYwKQogICAgICAgIF9hbF92ID0gcmUuc2VhcmNo'
'KHIiKD9tKV52PyhcZCspXC4oXGQrKVwuKFxkKykiLCBfYWwuc3Rkb3V0IG9yICIiKQogICAgICAgIGlmIF9hbC5yZXR1cm5j'
'b2RlOgogICAgICAgICAgICBsb2kuYXBwZW5kKCJhY3Rpb25saW50IHRyZW4gUEFUSCBjbyBtYXQgbmh1bmcgYGFjdGlvbmxp'
'bnQgLXZlcnNpb25gIHJjIT0wIChraG9uZyBjaGF5IGR1b2MpOiBjYWkgbGFpIGJhbiBnaGltIEFMX1ZFUiIpCiAgICAgICAg'
'ZWxpZiBub3QgX2FsX3Ygb3IgdHVwbGUoaW50KHgpIGZvciB4IGluIF9hbF92Lmdyb3VwcygpKSA8IEFMX1NBTjoKICAgICAg'
'ICAgICAgbG9pLmFwcGVuZChmImFjdGlvbmxpbnQge19hbF92Lmdyb3VwKDApIGlmIF9hbF92IGVsc2UgJyhraG9uZyBkb2Mg'
'ZHVvYyBwaGllbiBiYW4pJ30gY3UgaG9uIGJhbiBnaGltIENJICIKICAgICAgICAgICAgICAgICAgICAgICBmInsnLicuam9p'
'bihtYXAoc3RyLCBBTF9TQU4pKX0gKEFMX1ZFUik6IGJhbiBjdSBsYW0gdDEzNy90MTU5IERPICdsYScgdHJlbiB1bmcgdmll'
'biBzYWNoIOKAlCIKICAgICAgICAgICAgICAgICAgICAgICAiIGNhaSBiYW4gZ2hpbSAob3BzL2NhaV9hY3Rpb25saW50LnNo'
'IHZvaSBBTF9WRVIpIikKICAgICAgICAjIGdpdCBjdW5nIHRoZTogQ08gTUFUIGtob25nIHBoYWkgRFVORyBEVU9DLCB2YSBn'
'aXQgQ1UgbGEgY29uZyBjdSBQSE8gQklFTiBuaGF0IHRyb25nIGJvbi4gRG8gdHJlbiAyMDI2LTA5LTMwbCwgMGVhOTVkZSwg'
'Z2l0CiAgICAgICAgIyBUSEFUIHF1YSBjdW5nIGNoYXkoKTogMi4yNS4xID0+IDE0MC8xNjYgKDIzIGNhICJsYSI6IGBpbml0'
'IC1iYC4uLiksIDIuMzQuMSB2YSAyLjM1LjEgPT4gMTYzLzE2NiAodDEwOSB0MTEwIHQxMTE6IGBnaXQKICAgICAgICAjIHdv'
'cmt0cmVlIGxpc3QgLS1wb3JjZWxhaW4gLXpgIHJjPTEyOSBgdW5rbm93biBzd2l0Y2ggemApLCBlMmUgMi4zNS4xIHJjPTEg'
'YERBVCAxMSB8IFRSVU9UIDFgOyAyLjM2LjEgPT4gMTY2LzE2Ni4gU2FuIGxheQogICAgICAgICMgdHUgdGluaCBuYW5nIG1h'
'IENISU5IIG1hIGR1b2MgZG8gZ29pIChvcHMvY29uZ19jdS55YW1sIGRlIGJhbl9naGltIGdpdCA9IG51bGwgbmVuIGtob25n'
'IGNvIGJhbiBnaGltIENJIGRlIGR1YSB2YW8pLgogICAgICAgICMgYGdpdCB2ZXJzaW9uIDIuNDcuMS53aW5kb3dzLjFgIChH'
'aXQgZm9yIFdpbmRvd3MpIHZhIGAyLjM5LjMgKEFwcGxlIEdpdC0xNDYpYCBkZXUgZG9jIGR1b2MgYmEgc28gZGF1LgogICAg'
'ICAgICMgVmEgcGhhaSBob2kgRFVORyBnaXQgbWEgYm8gdGVzdCBTRSBHT0kuIEJvIHRlc3QgS0hPTkcgYHNodXRpbC53aGlj'
'aCgiZ2l0IilgIG5odSBiYSBjb25nIGN1IHRyZW46IEdPSV9HSVQgY3VhIHVuZyB2aWVuIHZhIG1vaQogICAgICAgICMgZml4'
'dHVyZSBnb2kgYGdpdGAgVFJBTiDigJQgdHJlbiBXaW5kb3dzIGxhIENyZWF0ZVByb2Nlc3NXOiBDSEkgdHUgdGhlbSBgLmV4'
'ZWAgKEtIT05HIFBBVEhFWFQpLCB0cmEgdGh1IG11YyBweXRob24uZXhlLCBjd2QKICAgICAgICAjIHZhIFN5c3RlbTMyIFRS'
'VU9DIFBBVEguIGB3aGljaGAgdGhpIHRyYSBQQVRIRVhULCBuZW4gbW90IGBnaXQuY21kYC9gZ2l0LmJhdGAgZHVuZyB0cnVv'
'YyBgZ2l0LmV4ZWAgQ1UgdHJlbiBQQVRIIGR1b2MgaG9pCiAgICAgICAgIyBUSEFZIG5vIOKAlCBkbyB0cmVuIDIwMjYtMTAt'
'MDEgKG5oYW5oIHdpbjMyIFRIQVQgY3VhIHNodXRpbC53aGljaDsgc2hpbSBgZ2l0LkNNRGAgbW9pIHRydW9jIGdpdCAyLjM1'
'LjEgVEhBVCk6IGJhbiAzMG0gbXVjIDAKICAgICAgICAjIGltLCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTog'
'Wyd0MTA5JywgJ3QxMTAnLCAndDExMSddYC4gTmVuIGhvaSBiYW5nIENISU5IIGR1b25nIGF5OiB0aWVuIHRyaW5oIGNvbiBj'
'dWEgY2hheSgpCiAgICAgICAgIyAoY3VuZyBweXRob24sIGN1bmcgbW9pIHRydW9uZywgY3dkID0gZ29jIG5odSBibyB0ZXN0'
'KSBnb2kgYGdpdCAtLXZlcnNpb25gIFRSQU4uCiAgICAgICAgX3JjX2d2LCBfcmFfZ3YgPSBjaGF5KFsiLWMiLCAiaW1wb3J0'
'IHN1YnByb2Nlc3MsIHN5czsgcCA9IHN1YnByb2Nlc3MucnVuKFsnZ2l0JywgJy0tdmVyc2lvbiddLCBjYXB0dXJlX291dHB1'
'dD1UcnVlLCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICIgdGV4dD1UcnVlLCB0aW1lb3V0PTYwKTsg'
'cHJpbnQocC5zdGRvdXQpOyBzeXMuZXhpdChwLnJldHVybmNvZGUpIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'IGdvYyBpZiBnb2MuaXNfZGlyKCkgZWxzZSBQYXRoLmN3ZCgpLCBwaHV0PTIpCiAgICAgICAgX2d2X20gPSByZS5zZWFyY2go'
'ciIoP20pXmdpdCB2ZXJzaW9uXHMrKFxkKylcLihcZCspXC4oXGQrKSIsIF9yYV9ndikKICAgICAgICBnaGkoImdpdF9ib190'
'ZXN0IiwgX2d2X20uZ3JvdXAoMCkgaWYgX2d2X20gZWxzZSBOb25lKQogICAgICAgIGlubigiICBnaXQgYm8gdGVzdCAgOiIs'
'IF9ndl9tLmdyb3VwKDApIGlmIF9ndl9tIGVsc2UgZiIoa2hvbmcgZG9jIGR1b2MgcGhpZW4gYmFuLCByYz17X3JjX2d2fSki'
'KQogICAgICAgIGlmIF9yY19ndjoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImBnaXQgLS12ZXJzaW9uYCBnb2kgVFJBTiBu'
'aHUgYm8gdGVzdCByYyE9MCAoeyhfcmFfZ3Yuc3RyaXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFdWzo5MF19KTogY2Fp'
'IGxhaSBnaXQiKQogICAgICAgIGVsaWYgbm90IF9ndl9tIG9yIHR1cGxlKGludCh4KSBmb3IgeCBpbiBfZ3ZfbS5ncm91cHMo'
'KSkgPCBHSVRfU0FOOgogICAgICAgICAgICBsb2kuYXBwZW5kKGYiZ2l0IHsnLicuam9pbihfZ3ZfbS5ncm91cHMoKSkgaWYg'
'X2d2X20gZWxzZSAnKGtob25nIGRvYyBkdW9jIHBoaWVuIGJhbiknfSBjdSBob24gIgogICAgICAgICAgICAgICAgICAgICAg'
'IGYieycuJy5qb2luKG1hcChzdHIsIEdJVF9TQU4pKX0gKHVuZyB2aWVuIGdvaSBgZ2l0IHdvcmt0cmVlIGxpc3QgLS1wb3Jj'
'ZWxhaW4gLXpgKTogY2FwIG5oYXQgZ2l0IikKICAgICAgICAjIGJhc2ggY3VuZyBIT0kgU0FJIENITyBuaHUgZ2l0OiA5IGNh'
'IFRST05HIHBoYW0gdmkgKHQzMiB0NTEgdDU5IHQ2MCB0NjIgdDYzIHQ2NiB0NjggdDE1MikgY2hheSBiYXNoIGJhbmcgYF9i'
'YXNoX3Bvc2l4KClgCiAgICAgICAgIyBjdWEgdW5nIHZpZW4g4oCUIEdpdCBCYXNoIG8gZHVvbmcgQ08gRElOSCBgQzpcUHJv'
'Z3JhbSBGaWxlc1xHaXRcYmluXGJhc2guZXhlYCAodmEgYCh4ODYpYCwgYHVzclxiaW5gKSwgcm9pCiAgICAgICAgIyBgd2hp'
'Y2goImJhc2giKWAgTkhVTkcgbG9haSBrZXQgcXVhIHRyb25nIFN5c3RlbTMyIChXU0wpOyBraG9uZyB0aGF5IHRoaSB0cmEg'
'IiIuIE1heSBjbyBXU0wgbWEgR2l0IGtob25nIG8gUHJvZ3JhbSBGaWxlcwogICAgICAgICMgKE1pbkdpdCBkbyBDSElOSCBw'
'czEgdHUgdGFpIOKAlCBNaW5HaXQgS0hPTkcgY28gYmFzaDsgc2Nvb3A7IGNhaSBwZXItdXNlcikgcXVhIGNob3QgYHdoaWNo'
'YCBvIHRyZW4sIHJvaSBgX2Jhc2hfcG9zaXgoKWAKICAgICAgICAjID09ICIiOiB0MzIgIktIT05HIERPIERVT0MiICsgOCBj'
'YSAibGEiIGBzdWJwcm9jZXNzLnJ1bihbIiIuLi5dKWAsIGNoaSBsbyByYSBTQVUgY2EgaGFpIGx1b3QgYm8gdGVzdC4gRG8g'
'dHJlbiAyMDI2LTEwLTAxOgogICAgICAgICMgaGFtIFRIQVQsIG5oYW5oIG9zLm5hbWU9J250JyAoV1NMICsgTWluR2l0L3Nj'
'b29wL3Blci11c2VyKSA9PiAnJzsgYm8gdGVzdCB2b2kgZ2lhIHRyaSBheSAxNTcvMTY2OyBlMmUgKHdpbjMyIGdpYSkgcmM9'
'MwogICAgICAgICMgc2F1IDM0NyBzLCBgVFJVT1QgTW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MgIGxhOiBbJ3Q1MScs'
'ICd0NTknLCAndDYwJywgJ3Q2MicsICd0NjMnLCAndDY2JywgJ3Q2OCcsICd0MTUyJ11gLiBQaGVwCiAgICAgICAgIyBkbyAz'
'MGogY2hheSB0cmVuIExpbnV4LCBub2kgYF9iYXNoX3Bvc2l4KClgIGx1b24gdHJhICJiYXNoIiwgbmVuIGtob25nIHRoZSB0'
'aGF5IGR1b25nIG5heS4KICAgICAgICAjIFZhIGBnaXRgIFRST05HIGJhc2ggYXkgbGEgZ2l0IFRIVSBCQTogYEdpdFxiaW5c'
'YmFzaC5leGVgIGxhIGNvbXBhdC1iYXNoIGN1YSBnaXQtd3JhcHBlciwgYHNldHVwX2Vudmlyb25tZW50KClgIGRheQogICAg'
'ICAgICMgYDxnb2MgR2l0PlxtaW5ndzY0XGJpbjs8Z29jIEdpdD5cdXNyXGJpbmAgbGVuIERBVSBQQVRIIChnaXQtZm9yLXdp'
'bmRvd3MvTUlOR1ctcGFja2FnZXM6IGdpdC13cmFwcGVyLmMgKyBjb21wYXQtYmFzaC5yYywKICAgICAgICAjIGtob25nIGNv'
'IE1JTklNQUxfUEFUSCkg4oCUIHR1YyBnaXQgREkgS0VNIGJhbiBHaXQgYXksIEtIT05HIHBoYWkgZ2l0IFRSQU4gZGEgaG9p'
'IG8gdHJlbi4gdDE1MiBjaGF5IEdJVF9DT05GSUdfQ09VTlQgKGdpdAogICAgICAgICMgMi4zMSkgdHJvbmcgYmFzaCBheS4g'
'RG8gdHJlbiAyMDI2LTEwLTAxIChiYXNoIGJvYyBkYXkgZ2l0IGRpIGtlbSBsZW4gZGF1IFBBVEgsIGdpdCBUUkFOIDIuNDMp'
'OiBnaXQgZGkga2VtIDIuMzAuMiBUSEFUID0+CiAgICAgICAgIyAxNjUvMTY2LCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1Qg'
'MWAsIGBsYTogWyd0MTUyJ11gIGNobyB1bmcgdmllbiBzYWNoOyAyLjMxLjAgVEhBVCA9PiAxNjYvMTY2LiBIb2kgQ0hJTkgg'
'aGFtIGF5IHZhCiAgICAgICAgIyBDSElOSCBiYXNoIGF5IHRyb25nIHRpZW4gdHJpbmggY29uIGN1YSBjaGF5KCkgKGN1bmcg'
'cHl0aG9uLCBjdW5nIG1vaSB0cnVvbmcsIGN3ZCA9IGdvYyk7IHVuZyB2aWVuIGtob25nIGNvIGhhbSB0aGkga2hvbmcKICAg'
'ICAgICAjIGhvaSAoZ2l1IGNob3QgQ08gTUFUKS4KICAgICAgICAjIERvYyBkb25nIGBnaXQgdmVyc2lvbmAgQ1VPSSBjdWEg'
'c3Rkb3V0LCBLSE9ORyBkb2MgZG9uZyBEQVUgKGJhbiAwMWI6IEJBU0hfRU5WIGBlY2hvYCBtb3QgZG9uZyA9PiBtdWMgMCBL'
'REQgb2FuOyB0dSBiYW4gMDFlCiAgICAgICAgIyBjaGF5KCkgYm8gQkFTSF9FTlYsIGNhY2ggZG9jIG5heSBnaXUgbGFpIHZp'
'IHZvIGhhaSkuIEJhc2ggdHJlbyB0aGkgYmF0IG5nb2FpIGxlIFRST05HIGNvbiAoYmFuIDAxYiBkbyBsb2kgY2hvCiAgICAg'
'ICAgIyBgX2Jhc2hfcG9zaXgoKWApIHZhIERVTkcgbHVvbiAoa2hvbmcgaG9pIGxhbiBoYWk6IGdpdSB0cmFuIDYwIHMgdmEg'
'bW90IHRpZW4gdHJpbmggbW8gY29pIG5odSBiYW4gMDFjKS4KICAgICAgICAjIFZhIGhvaSBIQUkgbGFuLCBkdW5nIEhBSSBt'
'b2kgdHJ1b25nIGJvIHRlc3QgVEhBVCBkdW5nOiAzIGxvaSBnb2kgYF9iYXNoX3Bvc2l4KClgIGN1YSB1bmcgdmllbiBjaGF5'
'IGJhc2ggdm9pIDIgbW9pIHRydW9uZyDigJQKICAgICAgICAjIHQzMi90NTEtdDY4IGBkaWN0KG9zLmVudmlyb24sIC4uLilg'
'IChtb2kgdHJ1b25nIGN1YSBjaGF5KCkpLCBjb24gdDE1MiAoY2EgRFVZIE5IQVQgY2FuIHNhbiAyLjMxKQogICAgICAgICMg'
'YGRpY3QoUEFUSD1vcy5lbnZpcm9uWyJQQVRIIl0sIFRMXyosIEdJVF9DT05GSUdfKilgLiBCYW4gMDFjIGhvaSBvIG1vaSB0'
'cnVvbmcgVEhVIE5IQVQgcm9pIGFwIHNhbiBjdWEgdDE1MiDigJQgZG8gdHJlbgogICAgICAgICMgMjAyNi0xMC0wMTogZ2l0'
'IGRpIGtlbSAyLjMwLjIgVEhBVCArIEJBU0hfRU5WIGRheSBnaXQgMi40MyBsZW4gZGF1IFBBVEggPT4gbXVjIDAgdGhheSAy'
'LjQzLCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsCiAgICAgICAgIyBgbGE6IFsndDE1MiddYCBjaG8gdW5nIHZpZW4g'
'c2FjaC4gVHUgYmFuIDAxZSBjaGF5KCkgYm8gQkFTSF9FTlYgbmVuIGR1b25nIGF5IGRvbmcgbyBHT0M7IGhhaSBsYW4gaG9p'
'IGdpdSBsYWkgdmkgaGFpIG1vaQogICAgICAgICMgdHJ1b25nIFZBTiBraGFjIG5oYXUuIExhbiBob2kgbyBtb2kgdHJ1b25n'
'IHRodSBuaGF0IENISSBjaHVuZyBtaW5oIGdpdCBDSEFZIGR1b2MgdHJvbmcgYmFzaCBheSwgS0hPTkcgY2h1bmcgbWluaCBi'
'YXNoCiAgICAgICAgIyAiZHVuZyBkdW9jIiBjaG8gdDMyL3Q1MS10NjggKGRvOiBub2Nsb2JiZXIgcXVhIGNhdSBob2kgbmF5'
'IG1hIGxhbSA3IGNhIERPIOKAlCB2aSB2YXkgY2hheSgpIGJvIGJpZW4ga2hvaSBkb25nIGJhc2gsIHhlbQogICAgICAgICMg'
'dHJlbikuIEJBU0hfR0lUID0gbW9pIHRydW9uZyB0MzIvdDUxLXQ2OCAoZG9pIENIQVkgZHVvYyk7IEJBU0hfR0lUX1QxNTIg'
'PSBtb2kgdHJ1b25nIHQxNTIgKGRvaSBzYW4gR0lUX1NBTl9CQVNIKS4KICAgICAgICBfcmNfYnAsIF9yYV9icCA9IGNoYXko'
'WyItYyIsICJpbXBvcnQgb3MsIHN1YnByb2Nlc3MsIHN5c1xuc3lzLnBhdGguaW5zZXJ0KDAsICdvcHMnKVxuaW1wb3J0IGxl'
'YXNlX3B1Ymxpc2hfdGVzdCBhcyBUXG4iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZiA9IGdldGF0'
'dHIoVCwgJ19iYXNoX3Bvc2l4JywgTm9uZSlcbmIgPSAnPycgaWYgZiBpcyBOb25lIGVsc2UgZigpXG5wcmludCgnQkFTSF9Q'
'T1NJWD0nICsgYilcbiIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpZiBiIGFuZCBiICE9ICc/Jzpc'
'biAgZm9yIGsgaW4gKCdCQVNIX0dJVCcsICdCQVNIX0dJVF9UMTUyJyk6XG4gICAgdHJ5OlxuIgogICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgIiAgICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbYiwgJy0tbm9wcm9maWxlJywgJy0tbm9y'
'YycsICctYycsICdnaXQgLS12ZXJzaW9uJ10sIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiBjYXB0'
'dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsIHRpbWVvdXQ9NjAsIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgIiBlbnY9Tm9uZSBpZiBrID09ICdCQVNIX0dJVCcgZWxzZSB7J1BBVEgnOiBvcy5lbnZpcm9uWydQQVRIJ119KVxu'
'IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiAgICAgIHYgPSBbeCBmb3IgeCBpbiBwLnN0ZG91dC5z'
'cGxpdGxpbmVzKCkgaWYgeC5zdGFydHN3aXRoKCdnaXQgdmVyc2lvbicpXSIKICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICIgb3IgcC5zdGRvdXQuc3RyaXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXVxuIgogICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgIiAgICAgIHByaW50KGsgKyAnPScgKyB2Wy0xXSArICcgcmM9JyArIHN0cihwLnJldHVy'
'bmNvZGUpKVxuIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiAgICBleGNlcHQgRXhjZXB0aW9uIGFz'
'IGU6XG4gICAgICBwcmludChrICsgJz0oJyArIHR5cGUoZSkuX19uYW1lX18gKyAnKSByYz0tMScpXG4iCiAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAiICAgICAgYnJlYWtcbiJdLAogICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICBnb2MgaWYgZ29jLmlzX2RpcigpIGVsc2UgUGF0aC5jd2QoKSwgcGh1dD0zKQogICAgICAgIF9icF9tID0gcmUuc2VhcmNo'
'KHIiKD9tKV5CQVNIX1BPU0lYPSguKikkIiwgX3JhX2JwKQogICAgICAgIF9icCA9IF9icF9tLmdyb3VwKDEpLnN0cmlwKCkg'
'aWYgKF9icF9tIGFuZCBub3QgX3JjX2JwKSBlbHNlIE5vbmUKICAgICAgICBfYmdfbSA9IHJlLnNlYXJjaChyIig/bSleQkFT'
'SF9HSVQ9Z2l0IHZlcnNpb25ccysoXGQrKVwuKFxkKylcLihcZCspW15cbl0qXHNyYz0wJCIsIF9yYV9icCkKICAgICAgICBf'
'YnRfbSA9IHJlLnNlYXJjaChyIig/bSleQkFTSF9HSVRfVDE1Mj1naXQgdmVyc2lvblxzKyhcZCspXC4oXGQrKVwuKFxkKylb'
'XlxuXSpcc3JjPTAkIiwgX3JhX2JwKQogICAgICAgIGdoaSgiYmFzaF9ib190ZXN0IiwgX2JwKTsgZ2hpKCJnaXRfdHJvbmdf'
'YmFzaF9ib190ZXN0IiwgX2JnX20uZ3JvdXAoMClbOTpdIGlmIF9iZ19tIGVsc2UgTm9uZSkKICAgICAgICBnaGkoImdpdF90'
'cm9uZ19iYXNoX3QxNTIiLCBfYnRfbS5ncm91cCgwKVsxNDpdIGlmIF9idF9tIGVsc2UgTm9uZSkKICAgICAgICBpbm4oIiAg'
'YmFzaCBibyB0ZXN0IDoiLCByZXByKF9icCkgaWYgX2JwIGlzIG5vdCBOb25lIGVsc2UgZiIoa2hvbmcgaG9pIGR1b2MsIHJj'
'PXtfcmNfYnB9KSIsCiAgICAgICAgICAgICJ8IGdpdCB0cm9uZyBiYXNoOiIsIF9iZ19tLmdyb3VwKDApWzk6XSBpZiBfYmdf'
'bSBlbHNlICIoa2hvbmcgZG9jIGR1b2MpIiwKICAgICAgICAgICAgInwgbW9pIHRydW9uZyB0MTUyOiIsIF9idF9tLmdyb3Vw'
'KDApWzE0Ol0gaWYgX2J0X20gZWxzZSAiKGtob25nIGRvYyBkdW9jKSIpCiAgICAgICAgaWYgX2JwIGlzIE5vbmU6CiAgICAg'
'ICAgICAgIGxvaS5hcHBlbmQoZiJraG9uZyBob2kgZHVvYyBgX2Jhc2hfcG9zaXgoKWAgY3VhIGJvIHRlc3QgKHJjPXtfcmNf'
'YnB9OiIKICAgICAgICAgICAgICAgICAgICAgICBmIiB7KF9yYV9icC5zdHJpcCgpLnNwbGl0bGluZXMoKSBvciBbJyddKVst'
'MV1bOjkwXX0pIikKICAgICAgICBlbGlmIG5vdCBfYnA6CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJgX2Jhc2hfcG9zaXgo'
'KWAgY3VhIGJvIHRlc3QgS0hPTkcgdGhheSBiYXNoIFBPU0lYIChgd2hpY2hgOiB7X2NjWydiYXNoJ119OyBTeXN0ZW0zMiA9'
'IFdTTCBiaSBsb2FpKToiCiAgICAgICAgICAgICAgICAgICAgICAgIiBjYWkgR2l0IGZvciBXaW5kb3dzIHZhbyBDOlxcUHJv'
'Z3JhbSBGaWxlc1xcR2l0LCBob2FjIGRhdCB0aHUgbXVjIEdpdFxcYmluIGxlbiBEQVUgUEFUSCAodHJ1b2MgU3lzdGVtMzIp'
'IikKICAgICAgICBlbGlmIF9icCAhPSAiPyIgYW5kIG5vdCAoX2JnX20gYW5kIF9idF9tKToKICAgICAgICAgICAgX2Rvbmdf'
'YmcgPSBbeFs6OTBdIGZvciB4IGluIHJlLmZpbmRhbGwociIoP20pXihCQVNIX0dJVCg/Ol9UMTUyKT89LiopJCIsIF9yYV9i'
'cCldIG9yIFsiKGtob25nIGNvIGRvbmcgQkFTSF9HSVQpIl0KICAgICAgICAgICAgbG9pLmFwcGVuZChmImBnaXQgLS12ZXJz'
'aW9uYCBUUk9ORyBiYXNoIGN1YSBibyB0ZXN0ICh7X2JwfSkga2hvbmcgY2hheS9raG9uZyBkb2MgZHVvYyBwaGllbiBiYW46'
'IHsnIHwgJy5qb2luKF9kb25nX2JnKX0iKQogICAgICAgIGVsaWYgX2JwICE9ICI/IiBhbmQgdHVwbGUoaW50KHgpIGZvciB4'
'IGluIF9idF9tLmdyb3VwcygpKSA8IEdJVF9TQU5fQkFTSDoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImdpdCB7Jy4nLmpv'
'aW4oX2J0X20uZ3JvdXBzKCkpfSBUUk9ORyBiYXNoIGN1YSBibyB0ZXN0ICh7X2JwfTsgbW9pIHRydW9uZyB0MTUyOiBjaGkg'
'UEFUSCwga2hvbmcgQkFTSF9FTlYpIGN1IgogICAgICAgICAgICAgICAgICAgICAgIGYiIGhvbiB7Jy4nLmpvaW4obWFwKHN0'
'ciwgR0lUX1NBTl9CQVNIKSl9ICh0MTUyIGR1bmcgR0lUX0NPTkZJR19DT1VOVCk6IGNhcCBuaGF0IGJhbiBHaXQgY2h1YSBi'
'YXNoIGF5IikKCnJjLCBoZWFkLCBfID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxvaS5hcHBlbmQo'
'Imtob25nIGRvYyBkdW9jIEhFQUQiKQpnaGkoImhlYWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywgIm1lcmdlLWJh'
'c2UiLCAiLS1pcy1hbmNlc3RvciIsIFNIQV9HMSwgaGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNfYSA9PSAwKQpp'
'ZiBoZWFkID09IFNIQV9HMToKICAgIHRoZV9oZSA9ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gREFZIExB'
'IGcxLiBDSFVBIGNvIGJhbiB2YSBnMjsga2V0IHF1YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9kdWU6CiAgICB0'
'aGVfaGUgPSAiZzIiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hBX0cxWzo4XX0p'
'OyB1bmcgdmllbiBnMiBoYXkga2hvbmc6IE43JyAobXVjIDEpIGRpbmggZGFuaC4iKQplbHNlOgogICAgdGhlX2hlID0gIj8i'
'OyBsb2kuYXBwZW5kKGYiSEVBRD17aGVhZFs6OF19IEtIT05HIHBoYWkgZzEgdmEgS0hPTkcgcGhhaSBoYXUgZHVlIGN1YSB7'
'U0hBX0cxWzo4XX0g4oCUIHJlYmFzZT8gbmhhbSBuaGFuaD8iKQpnaGkoInRoZV9oZSIsIHRoZV9oZSkKcmNfciwgcmVmcywg'
'XyA9IGdpdChnb2MsICJmb3ItZWFjaC1yZWYiLCAiLS1wb2ludHMtYXQiLCBoZWFkIG9yICJIRUFEIiwKICAgICAgICAgICAg'
'ICAgICAgICAiLS1mb3JtYXQ9JShyZWZuYW1lOnNob3J0KSIpCmRzciA9IFt4IGZvciB4IGluIHJlZnMuc3BsaXRsaW5lcygp'
'IGlmIHguc3RyaXAoKSBhbmQgeC5zdHJpcCgpICE9ICJkby10YW0iXQpnaGkoInJlZl90cm9fdG9pX2hlYWQiLCBkc3IpCmlu'
'bihmIiAgcmVmIHRybyB0b2kgSEVBRDogeycsICcuam9pbihkc3IpIGlmIGRzciBlbHNlICcoa2hvbmcgcmVmIG5hbyAtIEhF'
'QUQgcm9pIHR1IGRvKSd9IikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogbmVuIGRvIHNhaSwg'
'S0hPTkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlubigiICAtIiwgeCkKICAgIHN5cy5leGl0KDMp'
'CgojIC0tLS0tLS0tLS0tLS0tLS0gMS4ga2ljaCB0aHVvYyAoTjcnIGN1YSBzcGVjIHIzKSAtLS0tLS0tLS0tLS0tLS0tCmlu'
'bigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMS4gS0lDSCBUSFVPQyDigJQgdHJhbiBzcGVjIHIzOiA8PSAyIHRlcCB2YSA8'
'PSA0MDAgZG9uZyB0aGVtIikKIyBWRSBORU4gUEhBSSBUVU9JIOKAlCB2YSBwaGFpIENIVU5HIE1JTkggZHVvYyBsYSB0dW9p'
'LCBraG9uZyBwaGFpIGdpYSBkaW5oLgojIEJhaSBob2MgdHJhIGdpYSAxOS0wOS0yMDI2OiBjbG9uZSB0YWkgZHVuZyBjaGkg'
'ZmV0Y2ggbmhhbmggYmFuIHZhLCBgb3JpZ2luL21hc3RlcmAKIyBkdW5nIHllbiB0dSAxNC0wOSAoYzE2YmQzMiwgc2F1IDk3'
'IGNvbW1pdCkuIG1lcmdlLWJhc2Ugcm9pIHZlIGR1bmcgZGluaCBtYXN0ZXIgY3UsCiMgbmVuIGRpZmYgTlVPVCBjYSA5NyBj'
'b21taXQgbWFzdGVyOiBkbyByYSA0NiB0ZXAgLyArNzExOCB0aGF5IHZpIDIgdGVwIC8gKzM5NyDigJQKIyBDVU5HIE1PVCBD'
'T01NSVQgMGVhOTVkZS4gTW90IHRpZXUgY2hpIERFTFRBIG1hIHZlIG5lbiBraG9uZyB0dW9pIHRoaSBraG9uZyBzYWkKIyBs'
'ZWNoIG1vdCBjaHV0LCBubyBzYWkgY2EgbW90IGJhYyBkbyBsb24uCiMgQ2hvIG5lbjogbmVuIGtob25nIGNodW5nIG1pbmgg'
'ZHVvYyBsYSB0dW9pID0+IEtIT05HIERPIERVT0MgKHJjPTMpLCBLSE9ORyBwaGFpIFRSVU9ULgojIFRSVU9UIGxhIG1vdCBQ'
'SEFOIFFVWUVUIHZlIGJhbiB2YTsgcGhhbiBxdXlldCBjaGkgZHVvYyBwaGVwIHBoYXQgcmEga2hpIGRhIGRvIGR1b2MuCmVy'
'ID0gIiIKcmNfdSwgdXJsX3RobywgXyA9IGdpdChnb2MsICJyZW1vdGUiLCAiZ2V0LXVybCIsICJvcmlnaW4iKQp1cmxfbywg'
'dXJsX2luID0gX3VybF9zYWNoKHVybF90aG8pLCBfdXJsX2luKHVybF90aG8pCmdoaSgib3JpZ2luX3VybCIsIHVybF9pbik7'
'IGlubihmIiAgb3JpZ2luICAgICAgIDoge3VybF9pbiBvciAnKGtob25nIGRvYyBkdW9jKSd9IikKdXJsX29rID0gKG5vdCBy'
'Y191KSBhbmQgdXJsX28ucnN0cmlwKCIvIikgaW4gVVJMX0tIT19IT1BfTEUKcmNfbHIsIG91dF9sciwgZXJfbHIgPSBnaXQo'
'Z29jLCAibHMtcmVtb3RlIiwgIm9yaWdpbiIsICJyZWZzL2hlYWRzL21hc3RlciIpIGlmIHVybF9vayBlbHNlICgxLCAiIiwg'
'IiIpCmVyX2xyID0gX2FuX3VzZXJpbmZvKGVyX2xyKQpyY19sbSwgbG0sIGVyX2xtICAgICA9IGdpdChnb2MsICJyZXYtcGFy'
'c2UiLCAib3JpZ2luL21hc3RlciIpCnJtID0gb3V0X2xyLnNwbGl0KClbMF0gaWYgKG5vdCByY19sciBhbmQgb3V0X2xyLnN0'
'cmlwKCkpIGVsc2UgIiIKaWYgbm90IHVybF9vazoKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYib3JpZ2luPXt1'
'cmxfaW4hcn0gS0hPTkcgcGhhaSBraG8gdGhhdCDigJQgJ3R1b2knIHNvIHZvaSBubyBraG9uZyBjaHVuZyBtaW5oIGR1b2Mg'
'Z2kiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBub3Qgcm06CiAgICBrZXQoIk43JyBraWNo'
'IHRodW9jIiwgS0RELAogICAgICAgIGYia2hvbmcgaG9pIGR1b2MgbWFzdGVyIHRyZW4gcmVtb3RlIChscy1yZW1vdGUgcmM9'
'e3JjX2xyfSk6IHtlcl9scls6NjBdfSAiCiAgICAgICAgZiLigJQga2hvbmcgY2h1bmcgbWluaCBkdW9jIHZlIG5lbiBjb24g'
'dHVvaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIHJjX2xtIG9yIG5vdCBsbToKICAgIGtl'
'dCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgZG9jIGR1b2Mgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZToge2Vy'
'X2xtWzo2MF19IikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbG0gIT0gcm06CiAgICAjIERl'
'bSB4ZW0gdHV0IGxhaSBiYW8geGEsIG5ldSBkZW0gZHVvYyDigJQgY29uIHNvIG5heSBub2kgcm8gbXVjIGRvIHNhaSBsZWNo'
'LgogICAgcmNfYywgc2F1LCBfID0gZ2l0KGdvYywgInJldi1saXN0IiwgIi0tY291bnQiLCBmIntsbX0uLntybX0iKQogICAg'
'eGEgPSBmIiwgdHV0IGxhaSB7c2F1fSBjb21taXQiIGlmIChub3QgcmNfYyBhbmQgc2F1LnN0cmlwKCkuaXNkaWdpdCgpKSBl'
'bHNlICIiCiAgICBpbm4oZiIgIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmUgOiB7bG1bOjEyXX0iKQogICAgaW5uKGYiICBt'
'YXN0ZXIgdHJlbiByZW1vdGUgICAgICAgIDoge3JtWzoxMl19e3hhfSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsg'
'Z2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAogICAgICAgIGYidmUgbmVu'
'IENVOiBvcmlnaW4vbWFzdGVyPXtsbVs6MTJdfSAhPSByZW1vdGU9e3JtWzoxMl19e3hhfSAiCiAgICAgICAgZiLigJQgY2hh'
'eSBgZ2l0IC1DIDxraG8+IGZldGNoIG9yaWdpbiBtYXN0ZXJgIHJvaSBkbyBsYWkiKQogICAgcmNfbWIsIG1iLCBucywgcmMg'
'PSAxLCAiIiwgIiIsIDEKZWxzZToKICAgIGlubihmIiAgdmUgbmVuIFRVT0k6IG9yaWdpbi9tYXN0ZXIgPSB7bG1bOjEyXX0g'
'PT0gbWFzdGVyIHRyZW4gcmVtb3RlIikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUi'
'LCBybSkKICAgIHJjX21iLCBtYiwgZXJfbWIgPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICJvcmlnaW4vbWFzdGVyIiwgaGVh'
'ZCkKaWYgcmNfbWIgb3Igbm90IG1iOgogICAgaWYgbWIgPT0gIiIgYW5kIHJtIGFuZCBsbSA9PSBybToKICAgICAgICBrZXQo'
'Ik43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25nIHRpbmggZHVvYyBtZXJnZS1iYXNlIHZvaSBvcmlnaW4vbWFzdGVyOiB7'
'ZXJfbWJbOjcwXX0iKQogICAgbnMsIHJjID0gIiIsIDEKZWxzZToKICAgIGdoaSgibWVyZ2VfYmFzZSIsIG1iKQogICAgaW5u'
'KGYiICBtZXJnZS1iYXNlKG9yaWdpbi9tYXN0ZXIsIEhFQUQpID0ge21iWzoxMl19IikKICAgIGlmIG1iICE9IFNIQV9CQVNF'
'X1NQRUM6CiAgICAgICAgaW5uKGYiICBMVVUgWToga2hhYyBiYXNlIG1hIHNwZWMgcjMga2hhaSAoe1NIQV9CQVNFX1NQRUNb'
'OjEyXX0pIOKAlCB2aSBuaGFuaCBkYSBtZXJnZSBtYXN0ZXIuIikKICAgICAgICBpbm4oIiAgICAgICAgIERvIHNvIGJhc2Ug'
'Y3Ugc2UgTlVPVCBwaGFuIG1hc3RlciBtYW5nIHZhby4gRHVuZyBtZXJnZS1iYXNlIG1vaSBsYSB2aWVjIGN1YSBleGVjdXRv'
'ci4iKQogICAgICAgIHJjX3gsIG5zX3gsIF8gPSBnaXQoZ29jLCAiZGlmZi10cmVlIiwgIi1yIiwgIi1NIiwgIi0tZGlmZi1h'
'bGdvcml0aG09bXllcnMiLCAiLS1udW1zdGF0IiwgU0hBX0JBU0VfU1BFQywgaGVhZCkKICAgICAgICBpZiBub3QgcmNfeDoK'
'ICAgICAgICAgICAgaCA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zX3guc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0K'
'ICAgICAgICAgICAgYSA9IHN1bShpbnQoeFswXSkgZm9yIHggaW4gaCBpZiB4WzBdLmlzZGlnaXQoKSkKICAgICAgICAgICAg'
'Z2hpKCJudW1zdGF0X3RoZW9fYmFzZV9zcGVjIiwgeyJ0ZXAiOiBsZW4oaCksICJ0aGVtIjogYX0pCiAgICAgICAgICAgIGlu'
'bihmIiAgICAgICAgIChkb2kgY2hpZXU6IHNvIGJhc2Ugc3BlYyA9IHtsZW4oaCl9IHRlcCAvICt7YX0g4oCUIGNvbiBzbyBh'
'eSBLSE9ORyBkdW5nIGRlIGNoYW0pIikKICAgICMgUExVTUJJTkcsIGtob25nIFBPUkNFTEFJTjogYGdpdCBkaWZmYCBkb2Mg'
'Y2F1IGhpbmggVUkgQ1VBIE5HVU9JIERPIChkaWZmLmFsZ29yaXRobSwgZGlmZi5yZW5hbWVzLCBkaWZmLm9yZGVyRmlsZSwK'
'ICAgICMgY29sb3IuZGlmZiksIHZhIGdpYSB0cmkgSE9QIExFIGRvaSBsdW9uIFNPIGRvbmcgbWEgdmFuIHJhIGNodSBzbyDi'
'gJQgZG8gdHJlbiAyMDI2LTA5LTMwaTogdW5nIHZpZW4gdG9uZyBob3AgKG15ZXJzICs0MDEpID0+CiAgICAjIGJhbiAzMGkg'
'REFUIDIgdGVwIC8gKzQwMCBkdW9pIGBkaWZmLmFsZ29yaXRobSA9IGhpc3RvZ3JhbWAgaG9hYyBgcGF0aWVuY2VgLCBUUlVP'
'VCArNDAxIGtoaSBtYWMgZGluaDsgMTAvNzUgY29tbWl0IGNoYW0KICAgICMgd3JpdGUgc2V0IGNvIHNvIGRvbmcgZG9pIHRo'
'ZW8gdGh1YXQgdG9hbi4gYGRpZmYtdHJlZSAtciAtTWAgPSBtYWMgZGluaCBjdWEgYGdpdCBkaWZmYCAocmVuYW1lcyBiYXQp'
'IHZhIEtIT05HIGRvYyBjYWMga2hvYQogICAgIyBheS4gVGh1YXQgdG9hbiBwaGFpIFRVT05HIE1JTkg6IGRpZmYuPGRyaXZl'
'cj4uYWxnb3JpdGhtIChxdWEgY29yZS5hdHRyaWJ1dGVzRmlsZSBjdWEgbmd1b2kgZG8pIFZBTiBsb3QgdmFvIHBsdW1iaW5n'
'IOKAlAogICAgIyBkbyB0cmVuIDIwMjYtMDktMzBpLCBgKi5weSBkaWZmPWFsZ2AgKyBkaWZmLmFsZy5hbGdvcml0aG09aGlz'
'dG9ncmFtOiBkaWZmLXRyZWUgKzQwMSBjaG8gdW5nIHZpZW4gbXllcnMgKzQwMDsgY28gdHVvbmcgbWluaAogICAgIyB0aGFu'
'ZyBraG9hIGF5LiBhdHRyaWJ1dGVzIGAtZGlmZmAvY29yZS5iaWdGaWxlVGhyZXNob2xkIHZhbiBhcCA9PiBgLWAgPT4gS0hP'
'TkcgRE8gRFVPQyAoY2hvdCBkdW9pKS4KICAgIHJjLCBucywgZXIgPSBnaXQoZ29jLCAiZGlmZi10cmVlIiwgIi1yIiwgIi1N'
'IiwgIi0tZGlmZi1hbGdvcml0aG09bXllcnMiLCAiLS1udW1zdGF0IiwgbWIsIGhlYWQpCmlmIHJjOgogICAgcGFzcwplbHNl'
'OgogICAgaGFuZyA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICB0'
'aGVtID0gc3VtKGludChoWzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdpdCgpKQogICAgeG9hICA9IHN1bShpbnQo'
'aFsxXSkgZm9yIGggaW4gaGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgic29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hp'
'KCJkb25nX3RoZW0iLCB0aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZvciBoIGluIGhhbmc6IGlubihmIiAgICB7'
'aFsyXTozNH0gK3toWzBdOjw1fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05HOiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhl'
'bX0sIC17eG9hfSAgICh0cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcgdGhlbSkiKQogICAgY2hhbSA9'
'IHNvcnRlZCh7aFsyXSBmb3IgaCBpbiBoYW5nfSAmIFdSSVRFX1NFVF9HMik7IGdoaSgiY2hhbV93cml0ZV9zZXQiLCBjaGFt'
'KQogICAgZGVmIF9jYV9tb2lfY28ocmV2KToKICAgICAgICAjIGNhdC1maWxlLCBraG9uZyBgc2hvd2A6IGBnaXQgc2hvd2Ag'
'Y2hldCB2b2kgY2F1IGhpbmggVUkgZ28gc2FpIChkbyB0cmVuIDIwMjYtMDktMzBpOiBsb2cuZGF0ZSBnbyBzYWkgPT4gYmFu'
'IDMwaSBnb2kKICAgICAgICAjIDBlYTk1ZGUgbGEgImtob25nIHBoYWkgdW5nIHZpZW4gLi4uIE5vbmUg4oCUIGRhIGxhbmQ/'
'IG5oYW0gbmhhbmg/IikuCiAgICAgICAgcl8sIG5kXywgXyA9IGdpdChnb2MsICJjYXQtZmlsZSIsICItcCIsIGYie3Jldn06'
'b3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcmV0dXJuIE5vbmUgaWYgcl8gZWxzZSB7dCBmb3IgdCBpbiBD'
'QV9NT0lfRzIgaWYgcmUuc2VhcmNoKHIiKD9tKV5kZWYgIiArIHQgKyByIlthLXpdP18iLCBuZF8pfQogICAgb19tYiwgb19o'
'ID0gX2NhX21vaV9jbyhtYiksIF9jYV9tb2lfY28oaGVhZCkKICAgIG1hbmcgPSBzb3J0ZWQob19oIC0gb19tYiwga2V5PXNv'
'X2NhKSBpZiAob19tYiBpcyBub3QgTm9uZSBhbmQgb19oIGlzIG5vdCBOb25lKSBlbHNlIE5vbmUKICAgIGdoaSgiY2FfbW9p'
'X2cyX21hbmdfdmFvIiwgbWFuZykKICAgIGlmIG5vdCBtYW5nOgogICAgICAgICMgRG8gUk9ORyAoZGEgbGFuZCwgY2hpbmgg'
'bWFzdGVyKSwgbmhhbSBuaGFuaCwgaGF5IG5oYW5oIGN1YSBwYWNrZXQgS0hBQyBjaGFtIGN1bmcgdGVwOgogICAgICAgICMg'
'a2hvbmcgbWFuZyBjYSBtb2kgbmFvIGN1YSBnMiB0aGkga2hvbmcgcGhhaSB1bmcgdmllbi4gRG9jIGtob25nIGR1b2MgKE5v'
'bmUpIGN1bmcgdmF5LgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYiZG9pIHR1b25nIGtob25nIHBoYWkg'
'dW5nIHZpZW46IHtsZW4oaGFuZyl9IHRlcCwgY2hhbSB7Y2hhbX0sIGNhIG1vaSAiCiAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgZiJnMiBtYW5nIHZhbyB7bWFuZyFyfSDigJQgZGEgbGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/'
'IikKICAgIGVsc2U6CiAgICAgICAgIyBudW1zdGF0IGluIGAtYCAoa2hvbmcgY28gc28gZG9uZykgY2hvIHRlcCBiaW5hcnkv'
'LWRpZmYgdGhlbyBhdHRyaWJ1dGVzIOKAlCBrZSBjYSBhdHRyaWJ1dGVzIENVQSBOR1VPSSBETyAoZG8gdHJlbgogICAgICAg'
'ICMgMjAyNi0wOS0zMGc6IGNvcmUuYXR0cmlidXRlc0ZpbGUgYCoucHkgLWRpZmZgID0+ICIyIHRlcCAvICswIiBEQVQgY2hv'
'IDBlYTk1ZGUsIHRoYXQgKzM5NykuIGAtYCBsYSBLSE9ORyBETyBEVU9DLAogICAgICAgICMga2hvbmcgcGhhaSAwOyBUUlVP'
'VCB0aGVvIHNvIHRlcCAvIHNvIGRvbmcgREEgZGVtIGR1b2MgdmFuIGdpdSAocXVhbiBzYXQgdHJ1YyB0aWVwKS4KICAgICAg'
'ICBraG9uZ19zbyA9IFtoWzJdIGZvciBoIGluIGhhbmcgaWYgbm90IChoWzBdLmlzZGlnaXQoKSBhbmQgaFsxXS5pc2RpZ2l0'
'KCkpXTsgZ2hpKCJ0ZXBfa2hvbmdfc29fZG9uZyIsIGtob25nX3NvKQogICAgICAgIHZ1b3QgPSBsZW4oaGFuZykgPiBUUkFO'
'X1RFUCBvciB0aGVtID4gVFJBTl9ET05HCiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIFRSVU9UIGlmIHZ1b3QgZWxz'
'ZSAoS0REIGlmIGtob25nX3NvIGVsc2UgREFUKSwKICAgICAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IiAr'
'IChmIiDigJQgbnVtc3RhdCBLSE9ORyBjbyBzbyBkb25nIGNobyB7a2hvbmdfc299IiBpZiBraG9uZ19zbyBlbHNlICIiKSkK'
'CiMgQ29uZyBraWNoIHRodW9jIFBIQUkgZGUgbGFpIE1PVCBrZXQgcXVhLiBMZW5oIG51bXN0YXQgaG9uZyB0aGkgbmhhbmgg'
'YGlmIHJjOiBwYXNzYCBraG9uZyBnaGkgZ2ksIHZhIHZhbmcgbWF0IG8gZGF5CiMgdGhhbmggREFUIG8gYm8gZ29wOiBjYXUg'
'aGluaCBkaWZmIENVQSBOR1VPSSBETyBob25nIChkaWZmLm9yZGVyRmlsZSB0cm8gdGVwIGtob25nIGNvLCBkaWZmLmFsZ29y'
'aXRobSBnbyBzYWkgPT4gcmM9MTI4KSBjaG8KIyAtLWNoaS1raWNoLXRodW9jIHJjPTAgdm9pIDAgY2hvdCwgbHVvdCBkYXkg'
'ZHUgIkRBVCAxMSIgcmM9MCAoZG8gdHJlbiAyMDI2LTA5LTMwaCwgMGVhOTVkZSkuIFZhbmcgbWF0IGxhIEtIT05HIERPIERV'
'T0MuCiMgVHUgMzBqIG51bXN0YXQgbGEgZGlmZi10cmVlIChraG9uZyBkb2MgaGFpIGtob2EgYXkpOyBkdW9uZyBjb24gbGFp'
'IGRvIGR1b2M6IGRpZmYucmVuYW1lTGltaXQgZ28gc2FpID0+IHJjPTEyOC4KaWYgbm90IGFueShjWzBdID09ICJONycga2lj'
'aCB0aHVvYyIgZm9yIGMgaW4gY2hvdCk6CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImNvbmcgS0hPTkcgcmEg'
'a2V0IHF1YSAoZ2l0IGRpZmYtdHJlZSAtLW51bXN0YXQgcmM9e3JjfSk6IHtfYW5fdXNlcmluZm8oZXIpWzo3MF19IikKCiMg'
'RGluaCBkYW5oIFRIQVQgbmFtIG8gTjcnIChjYSBtb2kgZzIgbWFuZyB2YW8pLCBLSE9ORyBvICJoYXUgZHVlIGcxIjogZzEg'
'ZGEgbGFuZCBuZW4gbW9pIG5oYW5oIGRldQojIGxhIGhhdSBkdWUuIERvbmcgZGF1IGtob2kgZGFuIHBoYWkgdHUga2hhaSB0'
'aGVvIGtldCBxdWEgYXkgKGRvIGR1b2M6IG1hc3RlciA0NDYyMGU4IG1vIGtob2kgYmFuZwojICJUSEUgSEUgRE8gRFVPQzog'
'ZzIiLCBKU09OICJ0aGVfaGUiOiAiZzIiLCB0cm9uZyBraGkgTjcnIGRhIGtldCBsdWFuICJraG9uZyBwaGFpIHVuZyB2aWVu'
'IikuCiMgTmhhbiBjaGkgZHVvYyBub2kgRFVORyBjYWkgZG8gZHVvYzogYFtdYCBraG9uZyB0YWNoICJkYSBsYW5kIiBraG9p'
'ICJuaGFtIG5oYW5oIi8icGFja2V0IGtoYWMiIChkbwojIGR1b2MgdHJlbiAyMDI2LTA5LTMwYjogdW5nIHZpZW4gMmE2Nzk2'
'OCBEQSBMQU5EIGJpIGdvaSAiS0hPTkcgcGhhaSB1bmcgdmllbiBnMiIpLgppZiB0aGVfaGUgPT0gImcyIiBhbmQgbm90IHNv'
'LmdldCgiY2FfbW9pX2cyX21hbmdfdmFvIik6CiAgICB0aGVfaGUgPSAoIktIT05HIG1hbmcgY2EgbW9pIGcyIG5hbyAoZGEg'
'bGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/KSIgaWYgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKSA9PSBbXQog'
'ICAgICAgICAgICAgIGVsc2UgImcyPyAoQ0hVQSBkaW5oIGRhbmggZHVvYyBkb2kgdHVvbmcpIikKICAgIGdoaSgidGhlX2hl'
'IiwgdGhlX2hlKQoKIyBDb25nIG5oYW5oOiBkbyBSSUVORyBraWNoIHRodW9jICh2YWkgZ2lheSkgcm9pIGR1bmcuIER1bmcg'
'a2hpIGNhbiB4YWMgbWluaCBsYWkKIyB2ZSBuZW4gbWEga2hvbmcgbXVvbiB0cmEgMjAtNDUgcGh1dCBjaG8gY2EgYm8gdGVz'
'dC4KaWYgIi0tY2hpLWtpY2gtdGh1b2MiIGluIHN5cy5hcmd2OgogICAgaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQogICAgaW5u'
'KCItLWNoaS1raWNoLXRodW9jOiBDSEkgZG8gY29uZyBraWNoIHRodW9jLiBEYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hp'
'ZW0gdGh1LiIpCiAgICBpbm4oIi0iICogNzgpCiAgICBmb3IgX3QsIF90dCwgX2N0IGluIGNob3Q6IGlubihmIiAge190dDox'
'NH0ge190fSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgX2sgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBj'
'aG90IGlmIHQgPT0gS0REKQogICAgX3IgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCiAgICBz'
'eXMuZXhpdCgzIGlmIF9rIGVsc2UgKDEgaWYgX3IgZWxzZSAwKSkKCkNISV9QUk9CRSA9ICItLWNoaS1wcm9iZSIgaW4gc3lz'
'LmFyZ3YgICAgIyBibyBxdWEgYm8gdGVzdCArIE43OyBnaXUgMCwgMSwgMwojIC0tLS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVz'
'dCBkYXkgZHUgLS0tLS0tLS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsg'
'aW5uKCIyLiBCTyBURVNUIERBWSBEVSAoMTAtNDAgcGh1dCkiKQogICAgcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNl'
'X3B1Ymxpc2hfdGVzdC5weSJdLCBnb2MpCiAgICBnaGkoInJjX3N1aXRlIiwgcmNfbikKICAgIG0gPSBSWF9UT05HLnNlYXJj'
'aChvdXRfbikKICAgIGlubigiICByYyA9IiwgcmNfbiwgInwiLCBtLmdyb3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBk'
'dW9jIGRvbmcgdG9uZyBrZXQpIikKICAgIGlmIG06CiAgICAgICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGko'
'InRyZW4iLCBpbnQobS5ncm91cCgyKSkpOyBnaGkoImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKICAgIGRvX2hldCwg'
'Z2MsIHRpbiA9IGRvY19kbyhvdXRfbikKICAgIGdoaSgic29fY2FfZG8iLCBsZW4oZG9faGV0KSk7IGdoaSgibGlldF9rZV9k'
'YXlfZHUiLCB0aW4pCiAgICBmb3IgZyBpbiBnYzogaW5uKCIgICAqIiwgZykKICAgIGlubigiIik7IGlubihmIiAgPT09IHts'
'ZW4oZG9faGV0KX0gQ0EgRE8gPT09IikKICAgIGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAg'
'aW5uKGYiICAge3Quc3BsaXQoJ18nKVswXTo3fSB7dH0iKTsgaW5uKGYiICAgICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIp'
'CiAgICBnaGkoImRvX2x5X2RvIiwge3Q6IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQogICAgIyAtLS0tIENI'
'T1Q6IG1vaSBjYSBETyBwaGFpIEdJQUkgVEhJQ0ggRFVPQyAtLS0tCiAgICAjIFRoaWV1IGNob3QgbmF5LCBibyBkbyBpbiBk'
'YW5oIHNhY2ggZG8gcm9pIHZhbiB0aG9hdCByYz0wLiBEbyBkdW5nIGxhIGxvaSBkYSB4YXkgcmE6CiAgICAjIGx1b3QgV2lu'
'ZG93cyAxOS0wOSBjbyB0MTcxIERPIG1hIGJvIGRvIGJhbyAiREFUIDEwIHwgVFJVT1QgMCIgdmEgcmM9MC4KICAgIGRlZiBf'
'a2hvYSh0KTogcmV0dXJuIHQuc3BsaXQoIl8iKVswXQogICAgZG9fcGFja2V0LCBkb19sYSwgZG9fdGhpZXVfY29uZ19jdSA9'
'IFtdLCBbXSwgW10KICAgIGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaywgbHkgPSBfa2hv'
'YSh0KSwgZG9faGV0W3RdCiAgICAgICAgaWYgayBpbiBDQV9QQUNLRVQ6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ZG9fcGFja2V0LmFwcGVuZCh0KQogICAgICAgIGVsaWYgIktIw5RORyDEkE8gxJDGr+G7okMiIGluIGx5IG9yICJ0aGnhur91'
'IGAiIGluIGx5OiAgZG9fdGhpZXVfY29uZ19jdS5hcHBlbmQodCkKICAgICAgICBlbGlmIGsgaW4gTkdPQUlfUEhBTV9WSTog'
'ICAgICAgICAgICAgICAgICAgICAgICBwYXNzCiAgICAgICAgZWxzZTogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgZG9fbGEuYXBwZW5kKHQpCiAgICBnaGkoImRvX3BhY2tldCIsIGRvX3BhY2tldCk7IGdoaSgiZG9fbGEi'
'LCBkb19sYSk7IGdoaSgiZG9fdGhpZXVfY29uZ19jdSIsIGRvX3RoaWV1X2NvbmdfY3UpCiAgICBpbm4oIiIpCiAgICBpbm4o'
'ZiIgIGNhIERPIHRodW9jIENISU5IIHBhY2tldCBuYXkgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF0gb3IgJ2to'
'b25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBuZ29haSBwaGFtIHZpIChyMyBraGFpKToge1tfa2hvYSh4KSBmb3IgeCBp'
'biBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpIGlmIF9raG9hKHgpIGluIE5HT0FJX1BIQU1fVkldfSIpCiAgICBpbm4oZiIg'
'IGNhIERPIHZpIFRISUVVIENPTkcgQ1UgICAgICAgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9y'
'ICdraG9uZyBjbyd9IikKICAgIGlubihmIiAgY2EgRE8gTEEgKGtob25nIGdpYWkgdGhpY2ggZHVvYyk6IHtbX2tob2EoeCkg'
'Zm9yIHggaW4gZG9fbGFdIG9yICdraG9uZyBjbyd9IikKICAgICMgLS0tLSBDSE9UOiBwaGVwIGRvIHBoYWkgVFJPTiB0cnVv'
'YyBraGkgbW90IGNodSBEQVQgbmFvIGR1b2MgcGhhdCAtLS0tCiAgICAjIEJhbiB0cnVvYyBjaGkgSU4gYHRpbmAvYHJjX3N1'
'aXRlYDogYm8gdGVzdCBjaGV0IGdpdWEgdDE3MSAocmM9MTM0LCBraG9uZyBkb25nIHRvbmcpCiAgICAjIHZhbiByYSAiREFU'
'IDEyIHwgVFJVT1QgMCIgcmM9MDsgY2EgUEFDS0VUIHZhbmcgbWF0IGhheSBiaSBCTyBRVUEgY3VuZyBkdW9jIGNoYW0gbmh1'
'CiAgICAjICJraG9uZyBkbyIuIFZhbmcgbWF0IGtob25nIHBoYWkgImtob25nIGRvIiDigJQgbGEgS0hPTkcgRE8gRFVPQy4K'
'ICAgIHZhbmcgPSBbdCBmb3IgdCBpbiBzb3J0ZWQoQ0FfUEFDS0VULCBrZXk9c29fY2EpIGlmIG1hdV9jYShvdXRfbiwgdCkg'
'bm90IGluICgiUVVBIiwgIkRPIildCiAgICBseV9rZGQgPSBbXQogICAgaWYgbm90IHRpbjogbHlfa2RkLmFwcGVuZCgiZGFu'
'aCBzYWNoIGRvIEtIT05HIGRheSBkdSIpCiAgICBpZiByY19uIG5vdCBpbiAoMCwgMSkgb3IgKHJjX24gPT0gMSkgIT0gYm9v'
'bChkb19oZXQpOgogICAgICAgIGx5X2tkZC5hcHBlbmQoZiJyYyBibyB0ZXN0PXtyY19ufSBraG9uZyBraG9wIHtsZW4oZG9f'
'aGV0KX0gY2EgRE8gZG9jIGR1b2MiKQogICAgaWYgdmFuZzogbHlfa2RkLmFwcGVuZChmImNhIFBBQ0tFVCB2YW5nL2JvIHF1'
'YToge3Zhbmd9IikKICAgIGdoaSgiY2FfcGFja2V0X3ZhbmciLCB2YW5nKTsgZ2hpKCJseV9kb19jaHVhX3Ryb24iLCBseV9r'
'ZGQpCiAgICBpZiBseV9rZGQ6IGtldCgiQm8gdGVzdCBjaGF5IFRST04gdmEgZG9jIERVIiwgS0RELCAiOyAiLmpvaW4obHlf'
'a2RkKSkKICAgIGNodWFfdHJvbiA9IEtERCBpZiBseV9rZGQgZWxzZSBEQVQKICAgIGtldCgiS2hvbmcgY2EgbmFvIGN1YSBQ'
'QUNLRVQgYmkgRE8iLCBjaHVhX3Ryb24gaWYgbm90IGRvX3BhY2tldCBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBk'
'b19wYWNrZXQgZWxzZSBmIkRPOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF19IOKAlCBiYW4gdmEgQ0hVQSB4b25n'
'IikKICAgIGtldCgiTW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MiLCBjaHVhX3Ryb24gaWYgbm90IGRvX2xhIGVsc2Ug'
'VFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX2xhIGVsc2UgZiJsYToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV19IikK'
'ICAgIGlmIGRvX3RoaWV1X2NvbmdfY3U6CiAgICAgICAga2V0KCJDb25nIGN1IGRheSBkdSBkZSBkbyIsIEtERCwgZiJ0aGll'
'dSBjb25nIGN1IGNobyB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdfSIpCgogICAgYnEgPSBzb3J0ZWQo'
'e3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0X24pfSwga2V5PXNvX2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBi'
'cSkKICAgIGlubigiIik7IGlubihmIiAgQk8gUVVBICh7bGVuKGJxKX0pOiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBi'
'cV19IikKCiAgICBpbm4oIiIpOyBpbm4oIiAgTjEtTjQgKHQxNjUtdDE2OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIy'
'LCBuYXkgbGEgY2hpIGJhbyBob2kgcXV5OiIpCiAgICBiNCA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBTU9J'
'fTsgZ2hpKCJjYV9tb2kiLCBiNCkKICAgIGZvciB0IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCiAgICAj'
'IEJPX1FVQS92YW5nIGxhIENIVUEgQ0hBWSwga2hvbmcgcGhhaSBETzogY2hpIG1vdCBjYSBETyBtb2kgZHVvYyBwaGF0IFRS'
'VU9ULgogICAga2V0KCJOMS1ONCAodDE2NS10MTY4KSIsIERBVCBpZiBhbGwodiA9PSAiUVVBIiBmb3IgdiBpbiBiNC52YWx1'
'ZXMoKSkKICAgICAgICBlbHNlIChUUlVPVCBpZiBhbnkodiA9PSAiRE8iIGZvciB2IGluIGI0LnZhbHVlcygpKSBlbHNlIEtE'
'RCksIHN0cihiNCkpCgogICAgaW5uKCIiKTsgaW5uKCIgIDE1IGNhIHR1bmcgZG8gdHJlbiBDSToiKQogICAgYjE1ID0ge3Q6'
'IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0ExNX07IGdoaSgiY2ExNSIsIGIxNSkKICAgIGlubigiICAgICIgKyAiICAi'
'LmpvaW4oZiJ7dH06e2IxNVt0XX0iIGZvciB0IGluIENBMTUpKQoKICAgICMgdDEzNiDigJQgTjEyIGRvIEdJQU4gVElFUCBx'
'dWEga2V0IHF1YSBjYQogICAgdDEzNl90ZW4gPSBuZXh0KCh0IGZvciB0IGluIGRvX2hldCBpZiB0LnN0YXJ0c3dpdGgoInQx'
'MzYiKSksIE5vbmUpCiAgICBpZiBiMTUuZ2V0KCJ0MTM2IikgPT0gIlFVQSI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVh'
'IGtldCBxdWEgY2EpIiwgREFULCAidDEzNiBRVUEiKQogICAgZWxpZiBiMTUuZ2V0KCJ0MTM2IikgIT0gIkRPIjoKICAgICAg'
'ICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBLREQsIGYidDEzNiA9IHtiMTUuZ2V0KCd0MTM2Jykhcn0g4oCU'
'IGtob25nIGNoYXkva2hvbmcgdGhheSIpCiAgICBlbHNlOgogICAgICAgIGx5ID0gZG9faGV0LmdldCh0MTM2X3RlbiwgIiIp'
'CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgVFJVT1QsIGYiRE86IHtseVs6OTBdfSIpCgojIC0t'
'LS0tLS0tLS0tLS0tLS0gMy4gcHJvYmUgVEhBTkcgdmFvIGhhbSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIg'
'KiA3OCk7IGlubigiMy4gUFJPQkUgVEhBTkcg4oCUIGdvaSBfZ2l0X3dpbmRvd3Mgdm9pIHRoYW0gc28gdGllbSIpCnNwZWMg'
'PSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHA1NDEiLCBzdHIodGVwKSkKbHAgPSBpbXBvcnRs'
'aWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKHNwZWMpOyBzcGVjLmxvYWRlci5leGVjX21vZHVsZShscCkKc2lnID0gaW5zcGVj'
'dC5zaWduYXR1cmUobHAuX2dpdF93aW5kb3dzKQpnaGkoInRoYW1fc29fX2dpdF93aW5kb3dzIiwgbGlzdChzaWcucGFyYW1l'
'dGVycykpCmlubigiICB0aGFtIHNvIGN1YSBfZ2l0X3dpbmRvd3M6IiwgbGlzdChzaWcucGFyYW1ldGVycykpCgpkZWYgZ29p'
'KCoqa3cpOgogICAgIiIiR29pIF9naXRfd2luZG93cywgQkFUIHN0ZGVyciBkZSBtb3QgZG9uZyBjaGFuIGRvYW4ga2hvbmcg'
'Z2lldCBsdW90IGRvLiIiIgogICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRl'
'cnIoZSk6CiAgICAgICAgciA9IGxwLl9naXRfd2luZG93cygqKmt3KQogICAgcmV0dXJuIHIsIGUuZ2V0dmFsdWUoKQoKIyAt'
'LS0gZG9pIGNodW5nIHJpZzogcGhhaSB0cmEgbG9pIGR1bmcgbW90IGNhIHRhIEJJRVQgVFJVT0MgZGFwIGFuIC0tLQp3aXRo'
'IHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICBuZ29haSA9IFBhdGgodCkvIm5nb2FpIjsgbmdvYWku'
'bWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQog'
'ICAgKG5nb2FpLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMSwgXyA9IGdvaShw'
'YXRoPXN0cihuZ29haSksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAoY3cvImdpdC5leGUiKS53'
'cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIyLCBfID0gZ29pKHBhdGg9c3RyKGN3KSwgcHJvZ3JhbV9m'
'aWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKcmlnX29rID0gYm9vbChyMSkgYW5kIHIyIGlzIE5vbmUKZ2hpKCJyaWdfZG9p'
'X2NodW5nIiwgcmlnX29rKQprZXQoIlJJRyBkb2kgY2h1bmcgKGJpZXQgdHJ1b2MgZGFwIGFuKSIsIERBVCBpZiByaWdfb2sg'
'ZWxzZSBLREQsCiAgICBmIm5nb2FpLWN3ZC0+eydOSEFOJyBpZiByMSBlbHNlICdOb25lJ30gfCB0cm9uZy1jd2QtPnsnTkhB'
'TicgaWYgcjIgZWxzZSAnTm9uZSd9IikKaWYgbm90IHJpZ19vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzog'
'cmlnIHNhaSwgbW9pIGNob3QgZHVvaSBzZSB2byBuZ2hpYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tIE1PSSBDT05HIFBIQUkg'
'VFUgQ0hVTkcgTUlOSCBOTyBDTyBUSEUgRE8gLS0tCiMgQmFpIGhvYyBkYXQgbmhhdCBjdWEgcGFja2V0IG5heTogZG9fbjEw'
'IGJhbiBjdSBjaGFtIERBVCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEKIyBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZp'
'IGR1bmcga2h1eWV0IHRhdCBtYSBOMTAgc2luaCByYSBkZSBiYXQuIE5vIGRlZ2VuZXJhdGUg4oCUCiMgdHJlbiBXaW5kb3dz'
'IG9zLnBhdGhzZXAgREEgbGEgJzsnIG5lbiAidGFjaCBkdW5nIiB2YSAidGFjaCBzYWkiIGNobyBjdW5nIGtldCBxdWEuCiMg'
'TW90IGNvbmcga2hvbmcgdGhlIERPIHRoaSBraG9uZyBwaGFpIGNvbmcsIHZhIG5vIG5ndXkgaGllbSBob24ga2hvbmcgY28g'
'Y29uZzogbm8KIyBwaGF0IHJhIG1vdCBjaHUgREFULgojCiMgTmVuIHRydW9jIGtoaSBEVU5HIG5hbSBjb25nIG5heSBkZSBw'
'aGFuIHF1eWV0LCBiYXQgdHVuZyBjb25nIGdpZXQgbW90IGRvdCBiaWVuIGRhCiMgYmlldCB0cm9uZy4gQ29uZyBuYW8ga2hv'
'bmcgZ2lldCBkdW9jIHRoaSBjaHUgREFUIGN1YSBubyBiaSBIQSB4dW9uZyBLSE9ORyBETyBEVU9DOwojIFRSVU9UIGdpdSBu'
'Z3V5ZW4gKHF1YW4gc2F0IHRydWMgdGllcCwgdmQuIGcxIHZhbiBuaGFuIGdpdC5iYXQpLiBEb3QgYmllbiBjaGF5IHRyZW4g'
'QkFOIFNBTyBUQU07IGNheSB0aGF0IGtob25nIGJpCiMgZHVuZyB0b2kgKGN1bmcga3kgbHVhdCBuaHUgTjcpLgpET1RfQklF'
'Tl9UVV9LSUVNID0gWwogICAgKCJOOCIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgJ2lmIGNoaV9kaW5oIGFuZCBQ'
'YXRoKGNoaV9kaW5oKS5uYW1lLmxvd2VyKCkgPT0gImdpdC5leGUiIGFuZCBob3BfbGUoY2hpX2RpbmgpOicsCiAgICAgImlm'
'IGNoaV9kaW5oIGFuZCBob3BfbGUoY2hpX2RpbmgpOiIpLAogICAgKCJOOSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAg'
'ICAgImQgPSBkX3Jhdy5zdHJpcCgpLnN0cmlwKCdcIicpIiwgImQgPSBkX3Jhdy5zdHJpcCgpIiksCiAgICAoIk4xMCIsICJv'
'cHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgInNlcCA9IG9zLnBhdGhzZXAgaWYgcGhhbl9jYWNoIGlzIE5vbmUgZWxzZSBw'
'aGFuX2NhY2giLCAic2VwID0gb3MucGF0aHNlcCIpLAogICAgKCJOMTEiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAiaWYg'
'Y2hhbl9kb2FuIGlzIG5vdCBOb25lOiIsICJpZiBGYWxzZToiKSwKICAgICgiTjEyIiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rl'
'c3QucHkiLAogICAgICdnaXRfcGF0aD0iLy9raG9uZy1jby9naXQiJywgJ2dpdF9wYXRoPSIva2hvbmctY28vZ2l0IicpLApd'
'CmlubigiIik7IGlubigiICB0dSBraWVtIGNvbmcg4oCUIG1vaSBjb25nIHBoYWkgZ2lldCBkdW9jIG1vdCBkb3QgYmllbiBk'
'YSBiaWV0OiIpCmdpZXQgPSB7fQpmb3IgbWEsIGR1b25nLCB0aW0sIHRoYXkgaW4gRE9UX0JJRU5fVFVfS0lFTToKICAgIF90'
'ZW4sIF9oYW0gPSBuZXh0KCgoYSwgYikgZm9yIGEsIGIgaW4gUFJPQkUgaWYgYS5zdGFydHN3aXRoKG1hICsgIiAiKSksIChO'
'b25lLCBOb25lKSkKICAgIGlmIF9oYW0gaXMgTm9uZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6'
'NH0gS0hPTkcgRE8gRFVPQzoga2hvbmcgdGltIHRoYXkgcHJvYmUgdGVuICd7bWF9IC4uLiciKTsgY29udGludWUKICAgIHRy'
'eToKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIF90OgogICAgICAgICAgICBfYyA9IFBh'
'dGgoX3QpLyJjYXkiOyBzaHV0aWwuY29weXRyZWUoZ29jLyJvcHMiLCBfYy8ib3BzIikKICAgICAgICAgICAgX2YgPSBfYy9k'
'dW9uZzsgX25kID0gX2YucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIGlmIF9uZC5jb3VudCh0aW0p'
'ICE9IDE6CiAgICAgICAgICAgICAgICBnaWV0W21hXSA9IE5vbmUKICAgICAgICAgICAgICAgIGlubihmIiAgICB7bWE6NH0g'
'S0hPTkcgRE8gRFVPQzogbWF1IGRvdCBiaWVuIGtob3Age19uZC5jb3VudCh0aW0pfSBsYW4gKG1vbmcgMSkiCiAgICAgICAg'
'ICAgICAgICAgICAgZiIg4oCUIG1hIG5ndW9uIGRhIGRvaSwgZG90IGJpZW4gbmF5IGhldCB5IG5naGlhIik7IGNvbnRpbnVl'
'CiAgICAgICAgICAgIF9mLndyaXRlX3RleHQoX25kLnJlcGxhY2UodGltLCB0aGF5LCAxKSwgZW5jb2Rpbmc9InV0Zi04IikK'
'ICAgICAgICAgICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX2RiXyIgKyBtYSwg'
'c3RyKF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICAgICAgICAgIF9tID0gaW1wb3J0bGliLnV0aWwubW9kdWxl'
'X2Zyb21fc3BlYyhfc3ApOyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9tKQogICAgICAgICAgICBkZWYgX2dvaV9kYigqKmt3'
'KToKICAgICAgICAgICAgICAgIF9lID0gaW8uU3RyaW5nSU8oKQogICAgICAgICAgICAgICAgd2l0aCBjb250ZXh0bGliLnJl'
'ZGlyZWN0X3N0ZGVycihfZSk6CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIF9tLl9naXRfd2luZG93cygqKmt3KSwgX2Uu'
'Z2V0dmFsdWUoKQogICAgICAgICAgICBfdHQsIF9jdCwgXyA9IF9oYW0oX2dvaV9kYiwgaW5zcGVjdC5zaWduYXR1cmUoX20u'
'X2dpdF93aW5kb3dzKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rl'
'c3QucHkiKQogICAgICAgIGdpZXRbbWFdID0gKF90dCA9PSBUUlVPVCkKICAgICAgICBpbm4oZiIgICAge21hOjR9IGRvdCBi'
'aWVuIC0+IHtfdHQ6MTR9IHsnR0lFVCBEVU9DJyBpZiBfdHQgPT0gVFJVT1QgZWxzZSAnU09ORyBTT1QnfSIKICAgICAgICAg'
'ICAgKyAoZiIgICAoe19jdH0pIiBpZiBfY3QgZWxzZSAiIikpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAgICAg'
'IGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiB7dHlwZShfZSkuX19uYW1lX199OiB7'
'X2V9IikKZ2hpKCJjb25nX2dpZXRfZHVvY19kb3RfYmllbiIsIGdpZXQpCgpmb3IgdGVuLCAodHQsIGN0LCBkbCkgaW4gWyh0'
'LCBmKGdvaSwgc2lnLCB0ZXB0KSkgZm9yIHQsIGYgaW4gUFJPQkVdOgogICAgZ2hpKCJwcm9iZV8iICsgdGVuLnNwbGl0KClb'
'MF0ubG93ZXIoKSwgZGwpCiAgICBpZiBpc2luc3RhbmNlKGRsLCBkaWN0KToKICAgICAgICBmb3IgaywgdiBpbiBkbC5pdGVt'
'cygpOiBpbm4oZiIgICAge2s6MzR9OiB7dn0iKQogICAgbWEgPSB0ZW4uc3BsaXQoKVswXQogICAgaWYgZ2lldC5nZXQobWEp'
'IGlzIG5vdCBUcnVlIGFuZCB0dCA9PSBEQVQ6CiAgICAgICAgIyBEQVQgdHUgbW90IGNvbmcgY2h1YSBjaHVuZyBtaW5oIGR1'
'b2MgbGEgYmlldCBETyB0aGkga2hvbmcgZGFuZyB0aW4gaG9uIEtERC4KICAgICAgICBrZXQodGVuLCBLREQsIGYiY29uZyBL'
'SE9ORyBnaWV0IGR1b2MgZG90IGJpZW4gY3VhIGNoaW5oIG5vICh7Z2lldC5nZXQobWEpIXJ9KSIKICAgICAgICAgICAgICAg'
'ICAgICAgIGYiIC0+IGNodSBEQVQgbmF5IGtob25nIGNvIGdpYSB0cmkiKQogICAgZWxzZToKICAgICAgICBrZXQodGVuLCB0'
'dCwgY3QpCgojIC0tLS0tLS0tLS0tLS0tLS0gNC4gTjcgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAtLS0tLS0tLS0tLS0t'
'LS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjQuIE43IOKAlCBkb3QgYmll'
'biB0cmVuIEJBTiBTQU8gVEFNIChjYXkgdGhhdCBLSE9ORyBiaSBkdW5nIHRvaSkiKQogICAgdHJ1b2MgPSB0ZXAucmVhZF90'
'ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4pCiAgICBnaGkoIm43X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIg'
'IHNvIGRvbmcga2hvcCB7TUFVX1dJTiFyfTogVFJVT0MgPSB7dHJ1b2N9IFttb25nIDFdIikKICAgIGlmIHRydW9jICE9IDE6'
'CiAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCBmIm1hdSB4dWF0IGhpZW4ge3RydW9jfSBs'
'YW4sIGtob25nIHBoYWkgMSIpCiAgICBlbHNlOgogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkg'
'YXMgdG1wOgogICAgICAgICAgICBzYW8gPSBQYXRoKHRtcCkvImNheSIKICAgICAgICAgICAgc2h1dGlsLmNvcHl0cmVlKGdv'
'Yywgc2FvLCBpZ25vcmU9c2h1dGlsLmlnbm9yZV9wYXR0ZXJucygiLmdpdCIsICJfX3B5Y2FjaGVfXyIsICIqLnB5YyIpKQog'
'ICAgICAgICAgICBmMiA9IHNhby8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIKICAgICAgICAgICAgZjIud3JpdGVfdGV4dChm'
'Mi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikucmVwbGFjZShNQVVfV0lOLCAiaWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1'
'dGYtOCIpCiAgICAgICAgICAgIHNhdSA9IGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKTsg'
'Z2hpKCJuN19zYXUiLCBzYXUpCiAgICAgICAgICAgIGlubihmIiAgU0FVIChkYSBkb3QgYmllbikgPSB7c2F1fSBbbW9uZyAw'
'XSIpCiAgICAgICAgICAgIGlmIHNhdSAhPSAwOgogICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5k'
'b3dzIiwgS0RELCAiZG90IGJpZW4gS0hPTkcgYXAgZHVvYyIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBy'
'Y19tLCBvdXRfbSA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIHNhbykKICAgICAgICAgICAgICAgIG0x'
'NjUgPSBtYXVfY2Eob3V0X20sICJ0MTY1Iik7IGRtLCBfLCBfID0gZG9jX2RvKG91dF9tKQogICAgICAgICAgICAgICAgdGVu'
'MTY1ID0gbmV4dCgodCBmb3IgdCBpbiBkbSBpZiB0LnN0YXJ0c3dpdGgoInQxNjUiKSksIE5vbmUpCiAgICAgICAgICAgICAg'
'ICBseSA9IChkbS5nZXQodGVuMTY1KSBvciAiIikKICAgICAgICAgICAgICAgIGdoaSgibjdfdDE2NSIsIG0xNjUpOyBnaGko'
'Im43X2x5X2RvIiwgbHlbOjIwMF0pCiAgICAgICAgICAgICAgICBpbm4oZiIgIHQxNjUgc2F1IGRvdCBiaWVuOiB7bTE2NX0g'
'fCB7bHlbOjExMF19IikKICAgICAgICAgICAgICAgIGR1bmdfbHlfZG8gPSAiUEFUSCB0IiBpbiBseSBvciAiL3Vzci9iaW4i'
'IGluIGx5CiAgICAgICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBEQVQgaWYgKG0xNjUgPT0g'
'IkRPIiBhbmQgZHVuZ19seV9kbykgZWxzZQogICAgICAgICAgICAgICAgICAgIChUUlVPVCBpZiBtMTY1ID09ICJETyIgZWxz'
'ZSBLREQpLAogICAgICAgICAgICAgICAgICAgICJnaWV0IGR1bmcgbHkgZG8iIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdf'
'bHlfZG8pCiAgICAgICAgICAgICAgICAgICAgZWxzZSAoIkRPIG5odW5nIEtIT05HIGR1bmcgbHkgZG8gLT4gdGluIGR1bmcg'
'Z2lhIiBpZiBtMTY1ID09ICJETyIgZWxzZSAia2hvbmcgZG9jIGR1b2MgdDE2NSIpKQoKIyAtLS0tLS0tLS0tLS0tLS0tIEtF'
'VCBMVUFOIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQppbm4oZiJUSEUgSEUgRE8gRFVPQzoge3Ro'
'ZV9oZX0gICBIRUFEPXtoZWFkWzoxMl19IikKIyBLaG9pIGRhbiBjaG8gcmV2aWV3ZXIgYmF0IGRhdSBvIGRvbmcgdHJlbiwg'
'bmVuIENIRSBETyBwaGFpIG5hbSBOR0FZIGR1b2kgbm86IGtob25nIGNvIGRvbmcgbmF5CiMgdGhpIG1vdCBsdW90IC0tY2hp'
'LXByb2JlIGluICJEQVQgNyB8IFRSVU9UIDAgfCBLSE9ORyBETyBEVU9DIDAiIHJjPTAgbWEga2hvbmcgbm9pIGxhIGNodWEg'
'Y2hheSBibyB0ZXN0LgpnaGkoImNoZV9kbyIsICJjaGktcHJvYmUiIGlmIENISV9QUk9CRSBlbHNlICJkYXktZHUiKQppZiBD'
'SElfUFJPQkU6CiAgICBpbm4oIi0tY2hpLXByb2JlOiBDSEkgZG8gbXVjIDAsIDEsIDMuIEJvIHRlc3QsIE4xLU40LCB0MTM2'
'LCBONyBLSE9ORyBjaGF5IC0gZGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQppZiB0aGVfaGUgPT0gImcx'
'IjoKICAgIGlubigiTFVVIFk6IGRheSBsYSBORU4gRE8gKGcxKSwgS0hPTkcgcGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hv'
'dCBOOC1OMTIgZHVvaSBkYXkiKQogICAgaW5uKCIgICAgICAgVFJVT1QgbGEgRFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEg'
'bmh1bmcgbG8gZzIgc2luaCByYSBkZSB2w6EuIikKaW5uKCItIiAqIDc4KQpmb3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAg'
'IGlubihmIiAge3R0OjE0fSB7dGVufSIgKyAoZiIgICB7Y3R9IiBpZiBjdCBlbHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3Ig'
'XywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQpuX3RydW90ID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09'
'IFRSVU9UKQppbm4oIi0iICogNzgpCmlubihmIiAgREFUIHtzdW0oMSBmb3IgXyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8'
'IFRSVU9UIHtuX3RydW90fSB8IEtIT05HIERPIERVT0Mge25fa2RkfSIpCmlubihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgn'
'c29fY2FfZG8nKX0gfCBkYW5oIHNhY2ggZGF5IGR1OiB7J0NPJyBpZiBzby5nZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAn'
'S0hPTkcgRE8gRFVPQyd9IikKaW5uKGYiICBBZG1pbmlzdHJhdG9yOiB7c28uZ2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxp'
'bms6IHtzby5nZXQoJ3N5bWxpbmtfZHVvYycpfSIpCmlubigiIik7IGlubigiLS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5B'
'WSBWRSBDSE8gUkVWSUVXRVIgLS0tIikKZ2hpKCJjaG90IiwgW3sidGVuIjogYSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3Rp'
'ZXQiOiBjfSBmb3IgYSwgYiwgYyBpbiBjaG90XSkKaW5uKGpzb24uZHVtcHMoc28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5k'
'ZW50PTEsIGRlZmF1bHQ9c3RyKSkKIyByYzogMCA9IG1vaSBjaG90IERBVCB8IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNv'
'IGNob3QgS0hPTkcgRE8gRFVPQyAodXUgdGllbiBiYW8gZG9uZykKc3lzLmV4aXQoMyBpZiBuX2tkZCBlbHNlICgxIGlmIG5f'
'dHJ1b3QgZWxzZSAwKSkK'
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
