# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
# Luot DAY DU can SAN mot python >= 3.9 CO PyYAML (pip install pyyaml): ban nhung python.org ma tep nay tu tai
# KHONG co PyYAML/pip, nen no chi du cho -ChiKichThuoc / -ChiProbe. Thieu thi dung o buoc cong cu, rc=3.
# Luot DAY DU con can `bash` (Git Bash), `actionlint`, `shellcheck` (nhan --norc) tren PATH: tep nay KHONG tu cai chung; bo do
# hoi ngay o muc 0 va dung rc=3 neu thieu (khong doi het bo test moi biet).
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
$ShaBoDo    = 'f18ccaf964e5ef838c0344a8354a6899f70799d864196f28276b9ea84f9910ed'      # SHA-256 cua bo do Python nhung ben duoi

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
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0wOS0zMGsiICAgICAgICAgICAgICAj'
'IGRvaSBNT0kga2hpIHN1YSBibyBkbyAtIGxvZyB0dSBraGFpIGJhbiBuYW8KVFJBTl9URVAsIFRSQU5fRE9ORyA9IDIsIDQw'
'MCAgICAgICAgICAjIE43JyBjdWEgc3BlYyByMwpNQVVfV0lOICA9ICdpZiBuZW5fdGh1YyA9PSAid2luZG93cyI6JwojIFdy'
'aXRlIHNldCBjdWEgcGFja2V0ICM1NDEgZzIuIERpZmYga2hvbmcgY2hhbSB0ZXAgbmFvIG8gZGF5ID0+IGRvIE5IQU0gTkhB'
'TkguCldSSVRFX1NFVF9HMiA9IHsib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJ9'
'CiMgIlR1b2kiIGNoaSBjbyBuZ2hpYSBraGkgc28gdm9pIE1BWSBDSFUgVEhBVC4gTW90IG1pcnJvciBjdWMgYm8gY3UgY3Vu'
'ZyB0cmEgbHMtcmVtb3RlID09CiMgb3JpZ2luL21hc3RlciAoZG8gZHVvYzogbWFzdGVyIGMxNmJkMzIgLT4gInZlIG5lbiBU'
'VU9JIiwgNDYgdGVwIC8gKzcxMTggY2hvIDBlYTk1ZGUpLgojIERhbmggc2FjaCBDSE8gUEhFUDsgYHJlbW90ZSBnZXQtdXJs'
'YCBkYSBraGFpIHRyaWVuIGluc3RlYWRPZiBuZW4gY2h1eWVuIGh1b25nIGN1bmcgbG8gcmEuClVSTF9LSE9fSE9QX0xFID0g'
'eyJodHRwczovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdCIsICJodHRwczovL2dpdGh1Yi5jb20vZHVjdGhhbmdo'
'by90cmEtbHVhdC5naXQiLAogICAgICAgICAgICAgICAgICAjIFNTSCB0b2kgQ1VORyBraG8gKHNhdSBfdXJsX3NhY2gpOiBg'
'dXJsLiJnaXRAZ2l0aHViLmNvbToiLmluc3RlYWRPZiAiaHR0cHM6Ly9naXRodWIuY29tLyJgCiAgICAgICAgICAgICAgICAg'
'ICMgcmF0IHBobyBiaWVuIG8gbWF5IGRldjsgdGhpZXUgaGFpIGRhbmcgbmF5IHRoaSBraG8gVEhBVCBiaSBiYW8gIktIT05H'
'IHBoYWkga2hvIHRoYXQiLgogICAgICAgICAgICAgICAgICAic3NoOi8vZ2l0aHViLmNvbS9kdWN0aGFuZ2hvL3RyYS1sdWF0'
'IiwgInNzaDovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdC5naXQiLAogICAgICAgICAgICAgICAgICAiZ2l0QGdp'
'dGh1Yi5jb206ZHVjdGhhbmdoby90cmEtbHVhdCIsICJnaXRAZ2l0aHViLmNvbTpkdWN0aGFuZ2hvL3RyYS1sdWF0LmdpdCJ9'
'CiMgYHJlbW90ZSBnZXQtdXJsYCBLSEFJIFRSSUVOIGluc3RlYWRPZiwgbWEgbWF1IGB1cmwuImh0dHBzOi8vPHRva2VuPkBn'
'aXRodWIuY29tLyIuaW5zdGVhZE9mYCByYXQgcGhvCiMgYmllbi4gSW4vZ2hpIG5ndXllbiB2YW4gbGEgZHVhIFRPS0VOIHZh'
'byBsb2cgdmEgdmFvIGtob2kgSlNPTiBwczEgYmFvIGRhbiBjaG8gcmV2aWV3ZXIgKGRvIGR1b2M6CiMgMyBkb25nIHRyb25n'
'IGtob2kgZGFuKS4gQm8gdXNlcmluZm8gVFJVT0Mga2hpIGluIHZhIFRSVU9DIGtoaSBzbyDigJQgdG9rZW4gdmFuIGxhIEdp'
'dEh1YiB0aGF0LgojIEF1dGhvcml0eSBrZXQgdGh1YyBvIGAvYCwgYD9gIGhvYWMgYCNgIERBVSBUSUVOIOKAlCBkdW5nIGx1'
'YXQgZ2l0L2N1cmwuIEJhbiBgW14vXSpAYCBudW90IGNhIGA/YC9gI2AKIyBuZW4gbW90IFVSTCB0cm8gdG9pIE1BWSBLSEFD'
'IChob3N0IGR1bmcgdHJ1b2MgYD9gLCBkdW9pIGA/YCBsYSBgQGdpdGh1Yi5jb20vPGtobz5gKSBkdW9jICJsYW0gc2FjaCIK'
'IyB0aGFuaCBkdW5nIG1vdCBtdWMgQ0hPIFBIRVAsIHRyb25nIGtoaSBnaXQgbm9pIHRvaSBtYXkga2lhIChkbyBkdW9jOiBt'
'aXJyb3IgY3UgcGh1YyB2dSBxdWEgSFRUUFMgPT4KIyAidmUgbmVuIFRVT0kiLCBUUlVPVCA0NiB0ZXAgLyArNzExOCkuIFZh'
'biBibyB0b2kgYEBgIENVT0kgdHJvbmcgYXV0aG9yaXR5OiB1c2VyaW5mbyBjbyBgQGAgdHJhbiB0aGkKIyBjdXJsIHR1IGNo'
'b2kgKCJCYWQgaG9zdG5hbWUiKSwgY29uIGtoaSBpbiB0aGkga2hvbmcgbG8gcGhhbiBzYXUgYEBgIHRodSBuaGF0LgpfUlhf'
'VVNFUklORk8gPSByZS5jb21waWxlKHIiXihbQS1aYS16XVtBLVphLXowLTkrLi1dKjovLylbXi8/I10qQCIpCmRlZiBfdXJs'
'X3NhY2godSk6IHJldHVybiBfUlhfVVNFUklORk8uc3ViKHIiXDEiLCB1IG9yICIiKSAgICAgICAgICAjIGRlIFNPIChsdWF0'
'IGdpdC9jdXJsKQojIElOIHBoYWkgY2hlIFJPTkcgaG9uIFNPOiBtYXQga2hhdSBjbyBgP2AvYCNgIFRSQU4gdGhpIGBbXi8/'
'I10qQGAga2hvbmcga2hvcCBuZW4gVVJMIHJhIGxvZyBOR1VZRU4gVkFOCiMgKGRvIGR1b2MgdHJlbiAyMDI2LTA5LTMwYjog'
'MyBkb25nIG8gLS1jaGkta2ljaC10aHVvYywgMyBkb25nIHRyb25nIGtob2kgZGFuIC0tY2hpLXByb2JlOyBiYW4gMzBhOiAw'
'KS4KIyBDaGUgdG9pIGBAYCBDVU9JIENVTkcgY3VhIENBIGNodW9pIChjbyBoYXkga2hvbmcgY28gc2NoZW1lKSwgdmEgREUg'
'REFVIGAqKipAYCBkZSBiYW4gaW4ga2hvbmcgdHUgbmhhbiBsYQojIGdpdGh1Yi5jb20ga2hpIGdpdCBub2kgdG9pIG1heSBr'
'aGFjICh2ZC4gaG9zdCB0cnVvYyBgP2ApLiBCYW4gMzBjIGNoZSAidG9pIGBAYCBjdW9pIHRydW9jIGAvYCBkYXUgdGllbiIK'
'IyBuZW4gVkFOIGxvIGtoaSBtYXQga2hhdSBjbyBgL2AgdHJhbiwgaG9hYyBVUkwgZGFuZyBzY3AgYHVzZXI6bWtAaG9zdDpk'
'dW9uZ2AgKGtob25nIHNjaGVtZSkg4oCUIGRvIHRyZW4KIyAyMDI2LTA5LTMwYzogMyBkb25nIC8gMSB0cm9uZyBraG9pIGRh'
'biAtLWNoaS1raWNoLXRodW9jLCA1IC8gMyBvIC0tY2hpLXByb2JlLCBtb2kgZGFuZy4gTW9pIGt5IHR1IERVTkcKIyBsYSBt'
'b3QgZHVvbmcgbnVhOyAidG9pIGBAYCBjdW9pIiBraG9uZyBjb24ga3kgdHUgZHVuZyBuYW8uIEhhaSBxdXkgdGFjLCBoYWkg'
'bXVjIGRpY2g6IFNPIHRoZW8gZ2l0LCBJTgojIHRoZW8gInRodWEgY29uIGhvbiBsbyIuICJDQSBjaHVvaSIgcGhhaSBkdW5n'
'IGNhIGtoaSBjaHVvaSBjbyBYVU9ORyBET05HOiBnaXQoKSBkb2MgYmFuZyB0ZXh0PVRydWUgbmVuIENSL0xGIHRyb25nIFVS'
'TAojIGRhIHRoYW5oIExGLCBtYSBgLmAga2hvbmcga2hvcCBMRi4gVG9rZW4gZG9jIHR1IHRlcCBDUkxGIChgaHR0cHM6Ly94'
'LWFjY2Vzcy10b2tlbjo8dG9rZW4+YCArIENSICsgYEBnaXRodWIuY29tLy4uLmApCiMgdGhpIGJhbiAzMGUgS0hPTkcgY2hl'
'IGdpOiBpbiBOR1VZRU4gdG9rZW4gbyBkb25nIGBvcmlnaW4gOmAgdmEgbyAib3JpZ2luX3VybCIgdHJvbmcga2hvaSBKU09O'
'IGRhbiAoZG8gdHJlbiAyMDI2LTA5LTMwZSkuCmRlZiBfdXJsX2luKHUpOiByZXR1cm4gcmUuc3ViKHIiXihbQS1aYS16XVtB'
'LVphLXowLTkrLi1dKjovLyk/LipAIiwgciJcMSoqKkAiLCB1IG9yICIiLCBmbGFncz1yZS5TKQojIFRob25nIGJhbyBsb2kg'
'Y3VhIGdpdCBDSEkgYm8gdXNlcmluZm8gdG9pIGBAYCBEQVUgVElFTjogdXNlcmluZm8gY28gYEBgIHRyYW4gKHZkLiB0ZW4g'
'ZGFuZyBuaGFwIGxhCiMgZW1haWwpIHRoaSBwaGFuIHNhdSB2YW4gcmEgc3RkZXJyIGxzLXJlbW90ZSwgbWEgc3RkZXJyIGF5'
'IGR1b2MgaW4gdmFvIGRvbmcgS0REIGN1YSBONycgKGRvIGR1b2M6CiMgMiBkb25nIHRyb25nIGxvZywgMSB0cm9uZyBraG9p'
'IGRhbikuIExhbSBzYWNoIE1PSSBVUkwgdHJvbmcgdmFuIGJhbiB0cnVvYyBraGkgaW4g4oCUIGNoZSB0b2kgYEBgIENVT0kg'
'dHJlbgojIERPTkcgKGN1bmcgbHVhdCBJTiB2b2kgX3VybF9pbjoga2hvbmcgY29uIGt5IHR1IGR1bmcgbmFvKS4gQmFuIDMw'
'ZCBkdW5nIG8gYFxzJyJgIG5lbiBwaGFuIGdpdCBkZSBsYWkgY28KIyBgJ2AvYCJgL2tob2FuZyB0cmFuZyAodmQuIGB1QHg6'
'cCc8YmkgbWF0PkBnaXRodWIuY29tYCkgVkFOIGxvIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBkOiAyIGRvbmcgLyAxIHRyb25n'
'CiMga2hvaSBkYW4gLS1jaGkta2ljaC10aHVvYywgMyAvIDIgbyAtLWNoaS1wcm9iZSwgbW9pIGRhbmcuCmRlZiBfYW5fdXNl'
'cmluZm8odCk6IHJldHVybiByZS5zdWIociIoW0EtWmEtel1bQS1aYS16MC05Ky4tXSo6Ly8pW15cbl0qQCIsIHIiXDEqKipA'
'IiwgdCBvciAiIikKIyBDYSBuZ29haSBwaGFtIHZpIHIzIMKnbmdvYWlfcGhhbV92aSDigJQgZG8gQ0hJTkggU1BFQyBraGFp'
'LCBraG9uZyBwaGFpIGJvIGRvIHR1IHF1eWV0LgojIERvIGxhIERBTkggU0FDSCBDSE8gUEhFUDogY2EgZG8gbmFvIEtIT05H'
'IG5hbSB0cm9uZyBkYXkgdmEgS0hPTkcgcGhhaSAidGhpZXUgY29uZyBjdSIKIyB0aGkgbGEgVFJVT1QuIERhbmggc2FjaCBj'
'YW0gdGhpIGJhbyBnaW8gY3VuZyB0aGlldTsgZGFuaCBzYWNoIGNobyBwaGVwIHRoaSBiaWV0IHRydW9jLgpOR09BSV9QSEFN'
'X1ZJID0gc2V0KCJ0MTMxIHQxMzIgdDE1MCB0MTI1IHQzNSB0MzYgdDM3IHQzOCB0MzkgdDQwIi5zcGxpdCgpKQojIENhIGN1'
'YSBDSElOSCBwYWNrZXQgbmF5LiBNb3QgY2EgbyBkYXkgbWEgRE8gdGhpIGtob25nIGJhbyBnaW8gZHVvYyBibyBxdWEuCkNB'
'X1BBQ0tFVCA9IHNldCgidDE2NSB0MTY2IHQxNjcgdDE2OCB0MTY5IHQxNzAgdDE3MSB0MTcyIHQxNzMiLnNwbGl0KCkpCiMg'
'Q2EgTU9JIG1hIGcyIHRoZW0gdmFvIChOOC1OMTIpLiBEb2kgdHVvbmcgZG8gcGhhaSBNQU5HIGNodW5nIHZhbzogbWVyZ2Ut'
'YmFzZSBjaHVhIGNvLCBIRUFEIGNvLgpDQV9NT0lfRzIgPSAidDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpCkNB'
'MTUgID0gInQxMjkgdDEzMCB0MTMxIHQxMzIgdDEzMyB0MTM2IHQxMzggdDEzOSB0MTQ0IHQxNDUgdDE0NiB0MTQ3IHQxNDkg'
'dDE1MCB0MTUxIi5zcGxpdCgpCkNBTU9JID0gInQxNjUgdDE2NiB0MTY3IHQxNjgiLnNwbGl0KCkKCkRBVCwgVFJVT1QsIEtE'
'RCA9ICJEQVQiLCAiVFJVT1QiLCAiS0hPTkcgRE8gRFVPQyIKc28sIGNob3QgPSB7fSwgW10KZGVmIGdoaShrLCB2KTogc29b'
'a10gPSB2OyByZXR1cm4gdgpkZWYga2V0KHRlbiwgdHJhbmdfdGhhaSwgY2hpX3RpZXQ9IiIpOgogICAgY2hvdC5hcHBlbmQo'
'KHRlbiwgdHJhbmdfdGhhaSwgY2hpX3RpZXQpKQogICAgaW5uKGYiICBbe3RyYW5nX3RoYWk6MTR9XSB7dGVufSIgKyAoZiIg'
'ICB7Y2hpX3RpZXR9IiBpZiBjaGlfdGlldCBlbHNlICIiKSkKICAgIHJldHVybiB0cmFuZ190aGFpCgojIC0tLS0tLS0tLS0t'
'LS0tLS0gZG9jIGxvZyBjdWEgYm8gdGVzdCAoYmFuIDMsIGRhIGRvIHRyZW4gbG9nIFRIQVQpIC0tLS0tLS0tLS0tLS0tLS0K'
'UlhfRE9fQ0hPICA9IHJlLmNvbXBpbGUociIoP20pXiEhISBkbyAoXFMrKSAoLiopJCIpClJYX0RPX0NVT0kgPSByZS5jb21w'
'aWxlKHIiKD9tKV4gezJ9KFxTezEsNH0pIHsyfShcUyspOiAoLiopJCIpClJYX0JPX1FVQSAgPSByZS5jb21waWxlKHIiKD9t'
'KV4gezJ9XFN7MSw2fSBRVUEgKFxTKyk6ICguKikkIikKIyBEb25nIHRvbmcga2V0IFRIQVQgbyBEQVUgZG9uZy4gQ2EgRE8g'
'Y28gdGhlIGluIGxhaSBzdGRvdXQgY3VhIG1vdCBsdW90IENPTiAodDE1NSBjaGF5IGxhaSB0MDEsIHQ3Mi90OTggY2hheQoj'
'ICJibyIpIOKAlCBkb25nIHRvbmcgTE9ORyBheSBuYW0gR0lVQSBkb25nIChkbzogMjAgZG9uZyBsb25nIGRldSBvIGdpdWEg'
'ZG9uZywgY2hpIGRvbmcgdG9uZyB0aGF0IG8gZGF1IGRvbmcpLCBtYQojIGBzZWFyY2hgIGtob25nIG5lbyBiYXQgbm8gVFJV'
'T0MuIERvIHRyZW4gMjAyNi0wOS0zMGMsIDBlYTk1ZGUgKyBkb3QgYmllbiBsYW0gdDAxIERPOiBkb2MgcmEgIjAvMSIgPT4K'
'IyAiZGFuaCBzYWNoIEtIT05HIGRheSBkdSIsICJMRUNIIFNPIEhPQzogdGhpZXUgLTIwIGNhIiwgdHJvbmcga2hpIHRvbmcg'
'dGhhdCAxNjYtMTQ1PTIxID09IDIxIGNhIGRvYyBkdW9jLgpSWF9UT05HICAgID0gcmUuY29tcGlsZShyIig/bSlebGVhc2Vf'
'cHVibGlzaDogKFxkKykvKFxkKylcYlteXG5dKj89KFxkKyksW15cbl0qPz0oXGQrKSIpCgpkZWYgc29fY2EodCk6CiAgICBt'
'ID0gcmUubWF0Y2gociJ0KFxkKykiLCB0KTsgcmV0dXJuIChpbnQobS5ncm91cCgxKSkgaWYgbSBlbHNlIDEwKio2LCB0KQoK'
'ZGVmIGRvY19kbyhvdXQpOgogICAgdGFpX2NobyA9IHt0OiBsLnN0cmlwKCkgZm9yIHQsIGwgaW4gUlhfRE9fQ0hPLmZpbmRh'
'bGwob3V0KX0KICAgIGJvID0ge3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0KX0KICAgIGN1b2kgPSB7dDog'
'bC5zdHJpcCgpIGZvciBfLCB0LCBsIGluIFJYX0RPX0NVT0kuZmluZGFsbChvdXQpIGlmIHQgbm90IGluIGJvfQogICAgaG9w'
'ID0gZGljdChjdW9pKTsgaG9wLnVwZGF0ZSh0YWlfY2hvKQogICAgZ2MsIHRpbiA9IFtdLCBUcnVlCiAgICBpZiBzZXQodGFp'
'X2NobykgIT0gc2V0KGN1b2kpOgogICAgICAgIGdjLmFwcGVuZChmImhhaSBuZ3VvbiBMRUNIOiBjaGktdGFpLWNobz17c29y'
'dGVkKHNldCh0YWlfY2hvKS1zZXQoY3VvaSkpfSBjaGktY3VvaT17c29ydGVkKHNldChjdW9pKS1zZXQodGFpX2NobykpfSIp'
'CiAgICAgICAgdGluID0gRmFsc2UKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXQpCiAgICBpZiBub3QgbToKICAgICAgICBn'
'Yy5hcHBlbmQoIktIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQiKTsgdGluID0gRmFsc2UKICAgIGVsc2U6CiAgICAgICAg'
'ZGF0LCB0cmVuID0gaW50KG0uZ3JvdXAoMSkpLCBpbnQobS5ncm91cCgyKSkKICAgICAgICBnYy5hcHBlbmQoZiJzbyBob2M6'
'IHt0cmVufS17ZGF0fT17dHJlbi1kYXR9IGRvOyBkb2MgZHVvYyB7bGVuKGhvcCl9IikKICAgICAgICBpZiB0cmVuIC0gZGF0'
'ICE9IGxlbihob3ApOgogICAgICAgICAgICBnYy5hcHBlbmQoZiJMRUNIIFNPIEhPQzogdGhpZXUge3RyZW4tZGF0LWxlbiho'
'b3ApfSBjYSIpOyB0aW4gPSBGYWxzZQogICAgcmV0dXJuIGhvcCwgZ2MsIHRpbgoKIyBNYXUgY28gZG9uZyB0b25nIExPTkcg'
'Z2l1YSBkb25nIChkYW5nIHQxNTUgaW4gbGFpIGx1b3QgY29uKTogYm8gZG9jIGJhdCBkb25nIHRvbmcgREFVIFRJRU4gbGEg'
'dHUga2llbSBETy4KX01BVSA9ICgiISEhIGRvIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU4gYSAnbGVhc2VfcHVibGlz'
'aDogMC8xIMSR4bqhdDsgxJHDoyBjaOG6oXk9MSwgYuG7jyBxdWE9MCdcbiIKICAgICAgICAiISEhIGRvIHQxNTBfeCBXaW5F'
'cnJvciAxMzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICIgIELhu44gUVVBIHQxMzFfeTogbmVuIGZpeHR1cmVc'
'biIKICAgICAgICAiICDEkOG7jiAgdDAyYl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTjogYVxuIgogICAgICAgICIgIMSQ4buO'
'ICB0MTUwX3g6IFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAgICAgImxlYXNlX3B1Ymxpc2g6IDEv'
'MyDEkeG6oXQ7IMSRw6MgY2jhuqF5PTMsIGLhu48gcXVhPTFcbiIpCgojIEJpZW4gUFlUSE9OKiBjdWEgbWF5IG5ndW9pIGRv'
'IGxvdCB2YW8gYm8gdGVzdCBsYSBET0kgSEFOSCBWSSBibyB0ZXN0OiBQWVRIT05PUFRJTUlaRSBibyBtb2kgYGFzc2VydGAg'
'KGRvIHRyZW4KIyAyMDI2LTA5LTMwYzogYGFzc2VydCBGYWxzZWAgcXVhLCByYz0wKTsgYmFuIDMwZCBjaGkgdHJ1bmcgaG9h'
'IE1PVCBiaWVuIGF5LCBjb24gUFlUSE9OREVWTU9ERT0xIGxhbSB0MTU0IERPIDIvNAojIGxhbiB0cmVuIDMuMTEgKHNhY2g6'
'IDQvNCBRVUEpID0+IHJjPTEgIlRSVU9UIE1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jIiBjaG8gdW5nIHZpZW4gc2Fj'
'aCAoZG8gdHJlbgojIDIwMjYtMDktMzBkKS4gRGFuaCBzYWNoIENBTSBsdW9uIHRoaWV1IG1vdCBiaWVuIOKAlCBuZW4gZGF5'
'IGxhIGRhbmggc2FjaCBDSE8gUEhFUDogY2hpIGdpdSBiaWVuIGRlIHRyaW5oIHRob25nCiMgZGljaCBDSEFZIHZhIHRpbSBn'
'b2kgREEgQ0FJOyBQWVRIT05QQVRIIEtIT05HIGdpdSAoQ0kga2hvbmcgY28gbm8pLiBQaGVwIGhvaSBkaWV1IGtpZW4gdGll'
'biBxdXlldCBvIG11YyAwCiMgY3VuZyBjaGF5IHF1YSBkYXksIG5lbiBubyB0aGF5IERVTkcgbW9pIHRydW9uZyBtYSBibyB0'
'ZXN0IHNlIHRoYXkuCl9QWV9HSVUgPSBmcm96ZW5zZXQoeyJQWVRIT05IT01FIiwgIlBZVEhPTlVTRVJCQVNFIiwgIlBZVEhP'
'Tk5PVVNFUlNJVEUifSkKIyBDYXUgaGluaCBnaXQgQ1VBIE5HVU9JIERPIGxvdCB2YW8gYm8gdGVzdCB5IG5odSBiaWVuIFBZ'
'VEhPTio6IGNhIHRlc3QgZ29pIGdpdCBiYW5nIGRpY3Qob3MuZW52aXJvbiksIG5lbiBkb2MgY2F1IGhpbmgKIyBjYSBuaGFu'
'IHZhIGJpZW4gR0lUXyogY3VhIG1heSBkby4gRG8gdHJlbiAyMDI2LTA5LTMwZSwgMGVhOTVkZTogYGluaXQuZGVmYXVsdEJy'
'YW5jaCA9IG1haW5gID0+IDE2My8xNjYsIHQxMzQgdDEzOSB0MTUxCiMgRE8gPT4gcmM9MSAiVFJVT1QgTW9pIGNhIERPIGRl'
'dSBnaWFpIHRoaWNoIGR1b2MiIGNobyB1bmcgdmllbiBzYWNoIChzYWNoOiAxNjYvMTY2KSDigJQgbyBwaGFtIHZpIGdsb2Jh'
'bCBMQU4gaGUgdGhvbmcuCiMgQm8gTU9JIGJpZW4gR0lUXyogdmEgdGhheSBnbG9iYWwgQ0EgTkhBTiBiYW5nIGdsb2JhbCBD'
'VUEgQ0kuIENJIEtIT05HIGNvIGdsb2JhbCByb25nOiBqb2IgYGdhdGVgIGN1YSBjaS55bWwgKGJ1b2MgIkZvcmNlIExGCiMg'
'Y2hlY2tvdXQiLCBjYSB1YnVudHUgbGFuIHdpbmRvd3MpIGRhdCBnbG9iYWwgY29yZS5hdXRvY3JsZj1mYWxzZSwgY29yZS5l'
'b2w9bGYsIGNvcmUuYWJicmV2PTcgVFJVT0MgYnVvYyBjaGF5IGJvIHRlc3Qg4oCUCiMgdmkgKGNpLnltbDo3LTggdHUga2hh'
'aSkga2hvbmcgdGF0IHRoaSBydW5uZXIgV2luZG93cyBjaGVja291dCBDUkxGOiBhdXRvY3JsZj10cnVlIGN1YSBiYW4gY2Fp'
'IEdpdCBvIEhFIFRIT05HLiBCYW4gMzBmCiMgZGF0IGdsb2JhbCA9IHJvbmcgbmVuIGJvIHRlc3QgdGhheSBhdXRvY3JsZj10'
'cnVlIGNvbiBDSSB0aGF5IGZhbHNlOiBkbyB0cmVuIDIwMjYtMDktMzBmLCAwZWE5NWRlLCBoZSB0aG9uZyBhdXRvY3JsZj10'
'cnVlCiMgKyBnbG9iYWwgbmh1IENJID0+IGJhbiAzMGUgMTY2LzE2NiwgYmFuIDMwZiAxNjUvMTY2ICh0MTUwIERPIOKAlCBj'
'aGkga2hvbmcgdGhhbmggVFJVT1QgdmkgdDE1MCB0aW5oIGNvIG5hbSB0cm9uZwojIE5HT0FJX1BIQU1fVkkpLiBHbG9iYWwg'
'bGEgVEVQIFRBTSBjaHVhIERVTkcKIyBnbG9iYWwgY3VhIENJIGNvbmcgaW5pdC5kZWZhdWx0QnJhbmNoIGdoaW0gdmUgbWFj'
'IGRpbmggY3VhIGdpdCAoZGF0IGR1b2MgY2EgbyBoZSB0aG9uZyk6IGdsb2JhbCBkZSBsZW4gaGUgdGhvbmcgbmh1IHRyZW4g'
'Q0ksCiMgY29uIGNhdSBoaW5oIENVQyBCTyBjdWEgZml4dHVyZSB2YW4gZGUgbGVuIGdsb2JhbCAoR0lUX0NPTkZJR19DT1VO'
'VCB0aGkgZGUgbGVuIGNhIGN1YyBibykuIERvaSBidW9jIGF5IHRyb25nIGNpLnltbCB0aGkKIyBkb2kgX0dJVF9HTE9CQUxf'
'Q0kuIEdJVF9DT05GSUdfR0xPQkFMIGNoaSB0aGF5IFRFUCBDT05GSUc6IGlnbm9yZS9hdHRyaWJ1dGVzIG1hYyBkaW5oICgk'
'WERHX0NPTkZJR19IT01FIGhvYWMgfi8uY29uZmlnL2dpdC8KIyBpZ25vcmV8YXR0cmlidXRlcykgY3VhIG5ndW9pIGRvIFZB'
'TiBhcCBjaG8gZ2l0IGNvbiAoZG8gdHJlbiAyMDI2LTA5LTMwZywgMGVhOTVkZTogfi8uY29uZmlnL2dpdC9pZ25vcmUgYCou'
'eWFtbGAgPT4gYmFuIDMwZwojIDE1NC8xNjYsIDExIGNhICJsYSIpOyBDSSBraG9uZyBjbyB0ZXAgbmFvIG8gZG8gPT4gWERH'
'X0NPTkZJR19IT01FIHRybyB2YW8gdGh1IG11YyBUQU0gUk9ORy4gQ29uIGxhaSAoa2hvYSBoZSB0aG9uZyBraGFjKQojIGxh'
'IGdpb2kgaGFuIGRhIGJpZXQsIGtob25nIHBoYWkgZGEgZG9uZy4KIyBDYXUgaGluaCBzaGVsbGNoZWNrIENVQSBOR1VPSSBE'
'TyBsb3QgdmFvIGJvIHRlc3QgeSBuaHUgZ2l0OiB0MTM3IGdvaSBzaGVsbGNoZWNrIFRIQU5HLCB0MzMvdDEzNyBnb2kgYWN0'
'aW9ubGludCAtPiBzaGVsbGNoZWNrLAojIGNhIGhhaSBkb2MgU0hFTExDSEVDS19PUFRTLCB2YSB0MTM3IGRvYyB+Ly5zaGVs'
'bGNoZWNrcmMgKFhER19DT05GSUdfSE9NRSB0YW0gS0hPTkcgY2hlIGR1b2M7IGNobyB0ZXAgcmMgdHJlbiBXaW5kb3dzOiBL'
'SE9ORyBETyBEVU9DKS4KIyBEbyB0cmVuIDIwMjYtMDktMzBoLCAwZWE5NWRlOiBTSEVMTENIRUNLX09QVFM9LS1lbmFibGU9'
'YWxsID0+IHQzMyArIHQxMzcgRE87IH4vLnNoZWxsY2hlY2tyYyBgZW5hYmxlPWFsbGAgPT4gdDEzNyBETyDigJQgY2EgImxh'
'IgojID0+IFRSVU9UIGNobyB1bmcgdmllbiBzYWNoLiBDSSBraG9uZyBjbyBjYSBoYWkuIFNIRUxMQ0hFQ0tfT1BUUz0tLW5v'
'cmMgZGUgbGVuIGJpZW4gY3VhIG5ndW9pIGRvIFZBIHRhdCBtb2kgdGVwIHJjIChzaGVsbGNoZWNrCiMgcGhhaSBOSEFOIC0t'
'bm9yYyDigJQgbXVjIDAgaG9pIHRydW9jKS4gQkFTSF9FTlYgKGtlIGNhIGBzZXQgLWV1byBwaXBlZmFpbGApIGRvOiAxNjYv'
'MTY2LCBraG9uZyBsb3QuCl9HSVRfR0xPQkFMX0NJID0gIltpbml0XVxuXHRkZWZhdWx0QnJhbmNoID0gbWFzdGVyXG5bY29y'
'ZV1cblx0YXV0b2NybGYgPSBmYWxzZVxuXHRlb2wgPSBsZlxuXHRhYmJyZXYgPSA3XG4iCmRlZiBjaGF5KGFyZ3YsIGN3ZCwg'
'cGh1dD02MCk6CiAgICBmZCwgZ2MgPSB0ZW1wZmlsZS5ta3N0ZW1wKHByZWZpeD0id3A1NDEtZ2l0Y29uZmlnLWNpLSIsIHN1'
'ZmZpeD0iLmluaSIpCiAgICB4ZGcgPSBOb25lCiAgICB0cnk6CiAgICAgICAgeGRnID0gdGVtcGZpbGUubWtkdGVtcChwcmVm'
'aXg9IndwNTQxLXhkZy0iKQogICAgICAgIHdpdGggb3MuZmRvcGVuKGZkLCAidyIsIGVuY29kaW5nPSJhc2NpaSIsIG5ld2xp'
'bmU9IlxuIikgYXMgZjogZi53cml0ZShfR0lUX0dMT0JBTF9DSSkKICAgICAgICBtdCA9IHtrOiB2IGZvciBrLCB2IGluIG9z'
'LmVudmlyb24uaXRlbXMoKQogICAgICAgICAgICAgIGlmIG5vdCBrLnVwcGVyKCkuc3RhcnRzd2l0aCgiR0lUXyIpIGFuZCAo'
'bm90IGsudXBwZXIoKS5zdGFydHN3aXRoKCJQWVRIT04iKSBvciBrLnVwcGVyKCkgaW4gX1BZX0dJVSl9CiAgICAgICAgbXQu'
'dXBkYXRlKFBZVEhPTlVURjg9IjEiLCBQWVRIT05JT0VOQ09ESU5HPSJ1dGYtOCIsIFBZVEhPTkRPTlRXUklURUJZVEVDT0RF'
'PSIxIiwgUFlUSE9OVU5CVUZGRVJFRD0iMSIsCiAgICAgICAgICAgICAgICAgIEdJVF9DT05GSUdfR0xPQkFMPWdjLCBYREdf'
'Q09ORklHX0hPTUU9eGRnLCBTSEVMTENIRUNLX09QVFM9Ii0tbm9yYyIpCiAgICAgICAgcCA9IHN1YnByb2Nlc3MucnVuKFtz'
'eXMuZXhlY3V0YWJsZV0gKyBhcmd2LCBjd2Q9c3RyKGN3ZCksIGNhcHR1cmVfb3V0cHV0PVRydWUsCiAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD1waHV0'
'KjYwLCBlbnY9bXQpCiAgICBmaW5hbGx5OgogICAgICAgIHRyeTogb3MucmVtb3ZlKGdjKQogICAgICAgIGV4Y2VwdCBPU0Vy'
'cm9yOiBwYXNzCiAgICAgICAgaWYgeGRnOiBzaHV0aWwucm10cmVlKHhkZywgaWdub3JlX2Vycm9ycz1UcnVlKQogICAgcmV0'
'dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rkb3V0IG9yICIiKSArIChwLnN0ZGVyciBvciAiIikKCmRlZiBtYXVfY2Eob3V0LCB0'
'KToKICAgIG0gPSByZS5zZWFyY2gociIoP20pXjw8PCByYSAoIiArIHQgKyByIlthLXpdP19cUyopIFswLTkuXStzIChcdysp'
'XHMqJCIsIG91dCkKICAgIHJldHVybiBtLmdyb3VwKDIpIGlmIG0gZWxzZSBOb25lCgpkZWYgZ2l0KGdvYywgKmEsIHBodXQ9'
'NSk6CiAgICBwID0gc3VicHJvY2Vzcy5ydW4oWyJnaXQiLCAiLUMiLCBzdHIoZ29jKSwgKmFdLCBjYXB0dXJlX291dHB1dD1U'
'cnVlLCB0ZXh0PVRydWUsCiAgICAgICAgICAgICAgICAgICAgICAgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNl'
'IiwgdGltZW91dD1waHV0KjYwKQogICAgcmV0dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rkb3V0IG9yICIiKS5zdHJpcCgpLCAo'
'cC5zdGRlcnIgb3IgIiIpLnN0cmlwKCkKCgojID09PT09PT09PT09PT09PT09IE5BTSBQUk9CRSwgdmlldCB0aGFuaCBIQU0g'
'VEhVQU4gZGUgVFUgS0lFTSBkdW9jID09PT09PT09PT09PT09PT09CiMgTW9pIGhhbSB0cmEgKHRyYW5nX3RoYWksIGNoaV90'
'aWV0LCBkdV9saWV1KS4gS0hPTkcgaW4sIEtIT05HIHRob2F0IOKAlCBuaG8gdmF5IGNodW5nCiMgY2hheSBkdW9jIHRyZW4g'
'bmVuIEJBVCBLWSwgdmEgYC0tdHUta2llbS1wcm9iZWAgZ29pIHRoYW5nIGNodW5nIGRlIGtpZW0gY2hpbmggYm8gZG8uCgpk'
'ZWYgX3Nhbih0KToKICAgIGQgPSBQYXRoKHQpLyJkIjsgZC5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGly'
'KCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICByZXR1cm4gZCwgY3csIHBmCgpkZWYgZG9fbjgoZ29pLCBz'
'aWcsIHRlcHQpOgogICAgIiIiQnVvYyAxIChDT05HX0NVX0dJVCkgY2hpIGR1b2MgbmhhbiBnaXQuZXhlLiBEb2kgY2h1bmcg'
'ZHVvbmc6IGdpdC5leGUgVkFOIHBoYWkgbmhhbi4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5'
'RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgZm9yIHRlbiBpbiAoImdpdC5l'
'eGUiLCAiZ2l0LmJhdCIsICJnaXQuY21kIiwgImdpdC5weSIsICJraG9uZy1waGFpLWdpdC50eHQiKToKICAgICAgICAgICAg'
'ZiA9IGQvdGVuOyBmLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBfID0gZ29pKGNv'
'bmdfY3VfZ2l0PXN0cihmKSwgcGF0aD0iIiwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAg'
'ICAga3FbZiJDT05HX0NVX0dJVD17dGVufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiVFUgQ0hPSSIKICAgIGxvdCA9IFtrIGZv'
'ciBrLCB2IGluIGtxLml0ZW1zKCkgaWYgdiA9PSAiTkhBTiIgYW5kIG5vdCBrLmVuZHN3aXRoKCJnaXQuZXhlIildCiAgICBp'
'ZiBrcS5nZXQoIkNPTkdfQ1VfR0lUPWdpdC5leGUiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVu'
'ZyBkdW9uZyBob25nOiBnaXQuZXhlIGhvcCBsZSBtYSBiaSB0dSBjaG9pIiwga3EKICAgIHJldHVybiAoREFUIGlmIG5vdCBs'
'b3QgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgbG90IGVsc2UgZiJjb24gbmhhbjoge2xvdH0iKSwga3EKCmRlZiBkb19uOShn'
'b2ksIHNpZywgdGVwdCk6CiAgICAiIiJNdWMgUEFUSCBib2MgbmhheSBrZXAgcGhhaSBOSEFOOyBtdWMgcm9uZyAvIHRvYW4g'
'a2hvYW5nIHRyYW5nIHBoYWkgYm8gcXVhLCBraG9uZyBuZW0uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRl'
'bXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgodCkvImNvIGdpdCI7IGQubWtkaXIoKTsgY3cgPSBQ'
'YXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgICAgIChkLyJnaXQu'
'ZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgZm9yIG5oYW4sIG11YyBpbiAoKCJraG9u'
'ZyBuaGF5Iiwgc3RyKGQpKSwgKCJjbyBuaGF5IGtlcCIsIGYnIntkfSInKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAo'
'InJvbmciLCAiIiksICgiY2hpIGtob2FuZyB0cmFuZyIsICIgICAiKSk6CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAg'
'ICAgIHIsIF8gPSBnb2kocGF0aD1tdWMsIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAg'
'ICAgICBrcVtmIlBBVEgge25oYW59Il0gPSAiTkhBTiIgaWYgciBlbHNlICJOb25lIgogICAgICAgICAgICBleGNlcHQgRXhj'
'ZXB0aW9uIGFzIGU6CiAgICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59Il0gPSBmIk5FTSB7dHlwZShlKS5fX25hbWVf'
'X30iCiAgICBpZiBrcS5nZXQoIlBBVEgga2hvbmcgbmhheSIpICE9ICJOSEFOIjoKICAgICAgICByZXR1cm4gS0RELCAiZG9p'
'IGNodW5nIGR1b25nIGhvbmc6IG11YyBQQVRIIHRodW9uZyBtYSBraG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICBvayA9'
'IChrcS5nZXQoIlBBVEggY28gbmhheSBrZXAiKSA9PSAiTkhBTiIKICAgICAgICAgIGFuZCBrcS5nZXQoIlBBVEggcm9uZyIp'
'ID09ICJOb25lIiBhbmQga3EuZ2V0KCJQQVRIIGNoaSBraG9hbmcgdHJhbmciKSA9PSAiTm9uZSIpCiAgICByZXR1cm4gKERB'
'VCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgojIERhdSBwaGFuIGNhY2ggZHVu'
'ZyBERSBUSFUuIFBoYWkgS0hBQyBvcy5wYXRoc2VwIHRyZW4gQ0EgSEFJIG5lbiAoJzsnIFdpbmRvd3MsICc6JyBQT1NJWCkK'
'IyB0aGkgaGFpIGdpYSB0aHV5ZXQgInRhY2ggdGhlbyBkYXUgZHVvYyB0cnV5ZW4iIHZhICJ0YWNoIHRoZW8gb3MucGF0aHNl'
'cCIgbW9pIHJvaSByYSBuaGF1LgpUSFVfTjEwID0gInwiCgpkZWYgZG9fbjEwKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkhh'
'bSBwaGFpIHRhY2ggUEFUSCB0aGVvIGRhdSBwaGFuIGNhY2ggRFVPQyBUUlVZRU4sIGtob25nIHRoZW8gb3MucGF0aHNlcCBj'
'dWEgbmVuLgoKICAgIEJhbiBjdSBkbyAibW90IGRhdSAnOycgdHJvbmcgVEVOIHRodSBtdWMiIHZhIGRhdCBEQVQgdHJlbiBX'
'aW5kb3dzIGR1IGhhbSBzYWkuIE5vCiAgICBkZWdlbmVyYXRlOiB0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycs'
'IG5lbiAnQzovYTtiJyB0aGF0IHN1IENPIE5HSElBIGxhIGhhaQogICAgbXVjIOKAlCAidGFjaCBkdW5nIiB2YSAidGFjaCBz'
'YWkiIGNobyByYSBjdW5nIGtldCBxdWEsIHBoZXAgZG8ga2hvbmcgdGhlIGRvIG5hby4gTm8KICAgIGRhIGNoYW0gREFUIGNo'
'byA5NTgzMTY4NSB0cm9uZyBraGkgdDE3MSBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1bmcga2h1eWV0IHRhdCBheS4K'
'ICAgIE1vdCBjb25nIGtob25nIHRoZSBkbyB0aGkga2hvbmcgcGhhaSBjb25nLgogICAgIiIiCiAgICB0ZW5fc2VwID0gbmV4'
'dCgoayBmb3IgayBpbiAoInBoYW5fY2FjaCIsICJkYXVfcGhhbl9jYWNoIiwgInNlcCIpIGlmIGsgaW4gc2lnLnBhcmFtZXRl'
'cnMpLCBOb25lKQogICAgaWYgdGVuX3NlcCBpcyBOb25lOgogICAgICAgICMgS2hvbmcgY28gdGhhbSBzbyB0aGkgdHJlbiBX'
'aW5kb3dzIEtIT05HIGNvbiBkdW9uZyBuYW8gdGFjaCBoYWkgZ2lhIHRodXlldC4KICAgICAgICBpZiBvcy5wYXRoc2VwID09'
'ICI7IjoKICAgICAgICAgICAgcmV0dXJuIChLREQsICJ0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgdmEgaGFt'
'IGtob25nIG5oYW4gdGhhbSBzbyBkYXUgcGhhbiBjYWNoICIKICAgICAgICAgICAgICAgICAgICAgICAgICItPiBraG9uZyB0'
'YWNoIGR1b2MgaGFpIGdpYSB0aHV5ZXQiLAogICAgICAgICAgICAgICAgICAgIHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAs'
'ICJ0aGFtIHNvIHNlcCI6IE5vbmV9KQogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoK'
'ICAgICAgICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUiOyBsYS5ta2RpcigpCiAgICAgICAgICAgIGQsIGN3LCBwZiA9IF9z'
'YW4odCkKICAgICAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAg'
'ICAgICAgciwgXyAgPSBnb2kocGF0aD1zdHIobGEpICsgb3MucGF0aHNlcCArIHN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIo'
'cGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAgcjAsIF8gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3Ry'
'KHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAga3EgPSB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAi'
'OiBOb25lLAogICAgICAgICAgICAgICJjbyBtdWMgY2h1YSAnOyciOiAiTkhBTiIgaWYgciBlbHNlICJOb25lIiwKICAgICAg'
'ICAgICAgICAiZG9pIGNodW5nIGR1b25nIChraG9uZyBjbyAnOycpIjogIk5IQU4iIGlmIHIwIGVsc2UgIk5vbmUifQogICAg'
'ICAgIGlmIG5vdCByMDoKICAgICAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nIiwga3EKICAgICAg'
'ICByZXR1cm4gKERBVCBpZiByIGVsc2UgVFJVT1QpLCAoIiIgaWYgciBlbHNlICJtdWMgZ2l0LmV4ZSBob3AgbGUgYmkgTUFU'
'IiksIGtxCgogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGxhID0gUGF0aCh0'
'KS8iY287ZGF1IjsgbGEubWtkaXIoKSAgICAgICAgICAjICc7JyBuYW0gdHJvbmcgVEVOLCBraG9uZyBwaGFpIGRhdSBwaGFu'
'IGNhY2gKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4Iiwg'
'ZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBub2kgPSBzdHIobGEpICsgVEhVX04xMCArIHN0cihkKQogICAgICAgIGt3ID0g'
'ZGljdChwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgIHJfY2hpbmgsIF8gPSBnb2kocGF0aD1u'
'b2ksICAgICAgKip7dGVuX3NlcDogVEhVX04xMH0sICAgKiprdykgICAjIHRhY2ggZHVuZyAgLT4gTkhBTgogICAgICAgIHJf'
'ZHVvbmcsIF8gPSBnb2kocGF0aD1zdHIoZCksICAgKip7dGVuX3NlcDogVEhVX04xMH0sICAgKiprdykgICAjIGRvaSBjaHVu'
'ZyBkdW9uZwogICAgICAgIHJfcGhhbmJpZXQsIF8gPSBnb2kocGF0aD1ub2ksICAgKip7dGVuX3NlcDogb3MucGF0aHNlcH0s'
'ICoqa3cpICAjIHRhY2ggdGhlbyBvcy5wYXRoc2VwIC0+IG1hdAogICAga3EgPSB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2Vw'
'LCAidGhhbSBzbyBzZXAiOiB0ZW5fc2VwLCAiZGF1IHRodSI6IFRIVV9OMTAsCiAgICAgICAgICBmIm5vaSBiYW5nIHtUSFVf'
'TjEwIXJ9LCB7dGVuX3NlcH09e1RIVV9OMTAhcn0iOiAgICAgICAiTkhBTiIgaWYgcl9jaGluaCBlbHNlICJOb25lIiwKICAg'
'ICAgICAgIGYiZG9pIGNodW5nIGR1b25nIChtb3QgbXVjLCB7dGVuX3NlcH09e1RIVV9OMTAhcn0pIjogICJOSEFOIiBpZiBy'
'X2R1b25nIGVsc2UgIk5vbmUiLAogICAgICAgICAgZiJwaGFuIGJpZXQ6IG5vaSBiYW5nIHtUSFVfTjEwIXJ9LCB7dGVuX3Nl'
'cH09e29zLnBhdGhzZXAhcn0iOiAiTkhBTiIgaWYgcl9waGFuYmlldCBlbHNlICJOb25lIn0KICAgIGlmIG5vdCByX2R1b25n'
'OgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogbW90IG11YyBob3AgbGUgbWEga2hvbmcgdGlt'
'IHJhIGdpdC5leGUiLCBrcQogICAgIyBDb25nIHBoYWkgQ08gVEhFIGRvLiBOZXUgY2EgaGFpIGRhdSBwaGFuIGNhY2ggZGV1'
'IHJhIE5IQU4gdGhpIHBoZXAgZG8ga2hvbmcgcGhhbgogICAgIyBiaWV0IGR1b2MgZ2kg4oCUIGR1bmcgYmFvIERBVCwgYmFv'
'IHRoYW5nIGxhIGtob25nIGRvIGR1b2MuCiAgICBpZiByX3BoYW5iaWV0OgogICAgICAgIHJldHVybiAoS0RELCBmInBoZXAg'
'ZG8gS0hPTkcgcGhhbiBiaWV0IGR1b2M6IG5vaSBiYW5nIHtUSFVfTjEwIXJ9IG1hIHRhY2ggdGhlbyAiCiAgICAgICAgICAg'
'ICAgICAgICAgIGYie29zLnBhdGhzZXAhcn0gVkFOIHRpbSByYSBnaXQuZXhlIiwga3EpCiAgICByZXR1cm4gKChEQVQsICIi'
'LCBrcSkgaWYgcl9jaGluaCBlbHNlCiAgICAgICAgICAgIChUUlVPVCwgZiJ0YWNoIHRoZW8gb3MucGF0aHNlcCB0aGF5IHZp'
'IHRoZW8ge3Rlbl9zZXB9IGR1b2MgdHJ1eWVuIiwga3EpKQoKCmRlZiBkb19uMTEoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIi'
'VHJ1eWVuIGNoYW5fZG9hbiA9PiB0aHUgZHVvYyB0aG9uZyBiYW8gVkEgc3RkZXJyIElNLiBLaG9uZyB0cnV5ZW4gPT4gc3Rk'
'ZXJyIFZBTiBjby4iIiIKICAgIGlmICJjaGFuX2RvYW4iIG5vdCBpbiBzaWcucGFyYW1ldGVyczoKICAgICAgICByZXR1cm4g'
'S0RELCAiX2dpdF93aW5kb3dzIGtob25nIG5oYW4gdGhhbSBzbyBjaGFuX2RvYW4iLCB7InRoYW0gc28iOiBsaXN0KHNpZy5w'
'YXJhbWV0ZXJzKX0KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkLCBjdywg'
'cGYgPSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAg'
'ICAgICBjZCA9IFtdCiAgICAgICAgXywgZV9jbyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBj'
'd2Q9c3RyKGN3KSwgY2hhbl9kb2FuPWNkKQogICAgICAgIF8sIGVfa2ggPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmls'
'ZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICBrcSA9IHsiY2hhbl9kb2FuIHRodSBkdW9jIChtdWMpIjogbGVuKGNkKSwK'
'ICAgICAgICAgICJzdGRlcnIga2hpIENPIGNoYW5fZG9hbiAoYnl0ZSkiOiBsZW4oZV9jby5lbmNvZGUoKSksCiAgICAgICAg'
'ICAic3RkZXJyIGtoaSBLSE9ORyB0cnV5ZW4gKGJ5dGUpIjogbGVuKGVfa2guZW5jb2RlKCkpfQogICAgaWYgbGVuKGNkKSA9'
'PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPT0gMDoKICAgICAgICByZXR1cm4gS0RELCAibmhhbmggJVByb2dyYW1GaWxl'
'cyUga2hvbmcgcGhhbiBnaWFpIEtIT05HIGJheSByYSBjaGFuIGRvYW4gbmFvIC0+IGNodWEgZG8gZHVvYyIsIGtxCiAgICBv'
'ayA9IGxlbihjZCkgPiAwIGFuZCBsZW4oZV9jby5lbmNvZGUoKSkgPT0gMCBhbmQgbGVuKGVfa2guZW5jb2RlKCkpID4gMAog'
'ICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKZGVmIGRv'
'X24xMihnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW5nIHNlbnRpbmVsIGdpdF9wYXRoIHRyb25nIGZpeHR1cmUgcGhhaSB0'
'dXlldCBkb2kgdHJlbiBDQSBIQUkgbmVuLiIiIgogICAgbmQgPSB0ZXB0LnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiLCBl'
'cnJvcnM9InJlcGxhY2UiKQogICAgaGFuZyA9IHNvcnRlZChzZXQocmUuZmluZGFsbChyJ2dpdF9wYXRoXHMqPVxzKiIoW14i'
'XSspIicsIG5kKSkpCiAgICB4YXUgPSBbaCBmb3IgaCBpbiBoYW5nIGlmIG5vdCAoUHVyZVBvc2l4UGF0aChoKS5pc19hYnNv'
'bHV0ZSgpIGFuZCBQdXJlV2luZG93c1BhdGgoaCkuaXNfYWJzb2x1dGUoKSldCiAgICBrcSA9IHsiaGFuZyBnaXRfcGF0aCB0'
'aW0gdGhheSI6IGhhbmcsICJjaGkgdHV5ZXQgZG9pIE1PVCBuZW4iOiB4YXV9CiAgICBpZiBub3QgaGFuZzoKICAgICAgICBy'
'ZXR1cm4gS0RELCAia2hvbmcgdGltIHRoYXkgaGFuZyBnaXRfcGF0aCBuYW8gdHJvbmcgZml4dHVyZSAtPiBtYXUgZG9jIGNv'
'IHRoZSBkYSBkb2kiLCBrcQogICAgcmV0dXJuIChEQVQgaWYgbm90IHhhdSBlbHNlIFRSVU9UKSwgKCIiIGlmIG5vdCB4YXUg'
'ZWxzZSBmImNoaS1tb3QtbmVuOiB7eGF1fSIpLCBrcQoKUFJPQkUgPSBbKCJOOCBidW9jIDEgY2hpIG5oYW4gZ2l0LmV4ZSIs'
'IGRvX244KSwKICAgICAgICAgKCJOOSBib2MgbmhheSBrZXAgbyBtdWMgUEFUSCIsIGRvX245KSwKICAgICAgICAgKCJOMTAg'
'ZGF1ICc7JyB0cm9uZyB0ZW4gdGh1IG11YyIsIGRvX24xMCksCiAgICAgICAgICgiTjExIGNoYW4gZG9hbiBkb2kga2VuaCIs'
'IGRvX24xMSksCiAgICAgICAgICgiTjEyIGhhbmcgc2VudGluZWwgdHV5ZXQgZG9pIENBIEhBSSBuZW4iLCBkb19uMTIpXQoK'
'IyAtLS0gY2hlIGRvIFRVIEtJRU06IGNoYXkgbmFtIHByb2JlIHRyZW4gbW90IGNheSBiYXQga3ksIG5lbiBiYXQga3kgLS0t'
'CmlmICItLXR1LWtpZW0tcHJvYmUiIGluIHN5cy5hcmd2OgogICAgX2cgPSBQYXRoKHN5cy5hcmd2W3N5cy5hcmd2LmluZGV4'
'KCItLXR1LWtpZW0tcHJvYmUiKSArIDFdKS5yZXNvbHZlKCkKICAgIF9zcCA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9m'
'aWxlX2xvY2F0aW9uKCJscF90ayIsIHN0cihfZy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQogICAgX2xwID0gaW1wb3J0'
'bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3ApOyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9scCkKICAgIF9zaWcgPSBp'
'bnNwZWN0LnNpZ25hdHVyZShfbHAuX2dpdF93aW5kb3dzKQogICAgZGVmIF9nb2koKiprdyk6CiAgICAgICAgZSA9IGlvLlN0'
'cmluZ0lPKCkKICAgICAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgogICAgICAgICAgICByZXR1cm4g'
'X2xwLl9naXRfd2luZG93cygqKmt3KSwgZS5nZXR2YWx1ZSgpCiAgICBwcmludChmIlRVIEtJRU0gUFJPQkUgdHJlbiB7X2d9'
'ICAobmVuIHtzeXMucGxhdGZvcm19KSIpCiAgICBmb3IgX3RlbiwgX2YgaW4gUFJPQkU6CiAgICAgICAgX3R0LCBfY3QsIF9k'
'bCA9IF9mKF9nb2ksIF9zaWcsIF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIHByaW50KGYiICBb'
'e190dDoxNH1dIHtfdGVufSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgICAgIGZvciBfaywgX3YgaW4g'
'KF9kbCBvciB7fSkuaXRlbXMoKTogcHJpbnQoZiIgICAgICAgIHtfazozNH06IHtfdn0iKQogICAgc3lzLmV4aXQoMCkKCiMg'
'LS0tIGNoZSBkbyBLSUVNIERPTkcgQk86IHRlcCAucHkgbmF5IHBoYWkgVFJVTkcgVFVORyBCWVRFIHZvaSBiYW4gbmh1bmcg'
'dHJvbmcgcHMxIC0tLQojIEtob25nIGNvbmcgbmFvIGJ1b2MgaGFpIGJhbiBzYW8ga2hvcDogZG8gZHVvYywgbm9pIHRyYW4g'
'Mi80MDAgLT4gOTkvOTk5OTkgQ0hJIHRyb25nIC5weQojIHRoaSBjaV9kYW5nX2t5IGxhbiB0MjYvdDI3IHZhbiB4YW5oLCBj'
'b24gY2hvdCBTSEEgY3VhIHBzMSBjaGkgc28gYmFuIG5odW5nIHZvaSBoYW5nIHNvCiMgY3VhIENISU5IIG5vLiBDaGF5OiBw'
'eXRob24gd3A1NDEtZG8tZzItd2luZG93cy5weSAtLWtpZW0tZG9uZy1ibyB3cDU0MS1kby1nMi5wczEgIChyYyAwfDMpCmlm'
'ICItLWtpZW0tZG9uZy1ibyIgaW4gc3lzLmFyZ3Y6CiAgICBpbXBvcnQgYmFzZTY0CiAgICBfcHMgPSBQYXRoKHN5cy5hcmd2'
'W3N5cy5hcmd2LmluZGV4KCItLWtpZW0tZG9uZy1ibyIpICsgMV0pLnJlYWRfdGV4dChlbmNvZGluZz0iYXNjaWkiKQogICAg'
'X20gPSByZS5zZWFyY2gociIoP21zKV5cJEI2NCA9IEBcKCguKj8pXlwpIiwgX3BzKQogICAgX2sgPSByZS5zZWFyY2gociIo'
'P20pXlwkU2hhQm9Eb1xzKj1ccyonKFswLTlhLWZdezY0fSknIiwgX3BzKQogICAgX25odW5nID0gYmFzZTY0LmI2NGRlY29k'
'ZSgiIi5qb2luKHJlLmZpbmRhbGwociInKFtBLVphLXowLTkrLz1dKiknIiwgX20uZ3JvdXAoMSkpKSkgaWYgX20gZWxzZSBi'
'IiIKICAgIF90b2kgPSBQYXRoKF9fZmlsZV9fKS5yZWFkX2J5dGVzKCkKICAgIF9vayA9IGJvb2woX20gYW5kIF9rKSBhbmQg'
'X25odW5nID09IF90b2kgYW5kIGhhc2hsaWIuc2hhMjU2KF90b2kpLmhleGRpZ2VzdCgpID09IF9rLmdyb3VwKDEpCiAgICBp'
'bm4oZiJLSUVNIERPTkcgQk86IHtEQVQgaWYgX29rIGVsc2UgS0REfSAgKG5odW5nIHtsZW4oX25odW5nKX0gYnl0ZSwgdGVw'
'IHtsZW4oX3RvaSl9IGJ5dGUpIikKICAgIHN5cy5leGl0KDAgaWYgX29rIGVsc2UgMykKCmlubigiPSIgKiA3OCk7IGlubigi'
'V1A1NDEgZzIgLSBwaGVwIGRvIHRyZW4gV2luZG93cyB0aGF0IChzcGVjIHIzOiBOMS1ONCwgTjgtTjEyLCBONywga2ljaCB0'
'aHVvYykiKTsgaW5uKCI9IiAqIDc4KQoKIyAtLS0tLS0tLS0tLS0tLS0tIHR1IGtpZW0gYm8gZG9jIC0tLS0tLS0tLS0tLS0t'
'LS0KX2QsIF9nLCBfdCA9IGRvY19kbyhfTUFVKQpfb2sgPSAobGVuKF9kKSA9PSAyIGFuZCBhbnkoeC5zdGFydHN3aXRoKCJ0'
'MDJiIikgZm9yIHggaW4gX2QpCiAgICAgICBhbmQgbm90IGFueSh4LnN0YXJ0c3dpdGgoInQxMzEiKSBmb3IgeCBpbiBfZCkg'
'YW5kIF90KQppbm4oIlR1IGtpZW0gYm8gZG9jIGxvZzoiLCBEQVQgaWYgX29rIGVsc2UgVFJVT1QpCmlmIG5vdCBfb2s6CiAg'
'ICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IGJvIGRvYyBsb2cgY3VhIGNoaW5oIHNjcmlwdCBuYXkgc2FpIC0+IGto'
'b25nIGRvIGdpIGNhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDAuIG5lbiBkbyAtLS0tLS0tLS0tLS0t'
'LS0tCmdvYyA9IFBhdGgoc3lzLmFyZ3ZbMV0pLnJlc29sdmUoKSBpZiBsZW4oc3lzLmFyZ3YpID4gMSBlbHNlIFBhdGguY3dk'
'KCkKdGVwLCB0ZXB0ID0gZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaC5weSIsIGdvYyAvICJvcHMiIC8gImxlYXNlX3B1'
'Ymxpc2hfdGVzdC5weSIKaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIwLiBORU4gRE8iKQojIE1PSSBMT0cgUEhBSSBU'
'VSBLSEFJIG5vIGRvIENBSSBHSSBiYW5nIEJPIERPIE5BTy4gQmFpIGhvYyAxOS0wOS0yMDI2OiBtb3QgbHVvdCBkbwojIGd1'
'aSB2ZSBkdW9jIGRvYyBuaHUga2V0IHF1YSBjdWEgYmFuIHZhIGRhbmcgeGV0LCBuaHVuZyB0aGF0IHJhIGxhIGJhbiBkbyBD'
'VSBjaGF5CiMgdHJlbiBuaGFuaCBLSEFDLiBEb2MgcmEgdGhpIG1hdCBtb3Qgdm9uZzsgbG9nIHR1IGtoYWkgdGhpIHRoYXkg'
'bmdheSBkb25nIGRhdS4KdHJ5OgogICAgX3R1ID0gaGFzaGxpYi5zaGEyNTYoUGF0aChfX2ZpbGVfXykucmVhZF9ieXRlcygp'
'KS5oZXhkaWdlc3QoKQpleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAgX3R1ID0gZiJraG9uZyB0dSBiYW0gZHVvYzoge19l'
'fSIKZ2hpKCJib19kb19zaGEyNTYiLCBfdHUpCmlubihmIiAgQk8gRE8gICAgICAgIDogc2hhMjU2IHtfdHVbOjE2XX0gIChi'
'YW4ge0JBTl9CT19ET30pIikKaW5uKCIgIHN5cy5wbGF0Zm9ybSA6Iiwgc3lzLnBsYXRmb3JtLCAifCBweXRob24iLCBzeXMu'
'dmVyc2lvbi5zcGxpdCgpWzBdKQppbm4oIiAgb3MucGF0aHNlcCAgIDoiLCByZXByKG9zLnBhdGhzZXApLCAifCBQQVRIRVhU'
'OiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlBBVEhFWFQiKSlbOjYwXSkKaW5uKCIgIFByb2dyYW1GaWxlcyA6IiwgcmVwcihv'
'cy5lbnZpcm9uLmdldCgiUHJvZ3JhbUZpbGVzIikpLCAifCBTeXN0ZW1Sb290OiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlN5'
'c3RlbVJvb3QiKSkpCmlubigiICBDT05HX0NVX0dJVCAgOiIsIHJlcHIoX0NPTkdfQ1VfR0lUX05HVU9JX0RPKQogICAgKyAo'
'IiAgLT4gREEgQk8ga2hvaSBsdW90IGRvIChDSSBraG9uZyBkYXQgYmllbiBuYXk7IHhlbSBkYXUgdGVwKSIgaWYgX0NPTkdf'
'Q1VfR0lUX05HVU9JX0RPIGlzIG5vdCBOb25lIGVsc2UgIiIpKQpnaGkoImNvbmdfY3VfZ2l0X25ndW9pX2RvIiwgX0NPTkdf'
'Q1VfR0lUX05HVU9JX0RPKQppbm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5vbmUKaWYgc3lzLnBsYXRm'
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
'MTY2KS4KaWYgbm90ICgiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Ygb3IgIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJn'
'dik6CiAgICBfcmNfZGssIF9yYV9kayA9IGNoYXkoWyItYyIsICJpbXBvcnQgc3lzOyBzeXMuZXhpdCg5KSBpZiBzeXMudmVy'
'c2lvbl9pbmZvIDwgKDMsIDkpIGVsc2UgTm9uZTsgaW1wb3J0IHlhbWw7IgogICAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAiIHlhbWwuc2FmZV9kdW1wKHlhbWwuc2FmZV9sb2FkKCdhOiAxJykpIl0sCiAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgZ29jIC8gIm9wcyIgaWYgKGdvYyAvICJvcHMiKS5pc19kaXIoKSBlbHNlIFBhdGguY3dkKCksIHBodXQ9MikKICAgIGlm'
'IF9yY19kayA9PSA5OgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24ge3N5cy52ZXJzaW9uLnNwbGl0KClbMF19IDwgMy45'
'OiBibyB0ZXN0IGN1YSB1bmcgdmllbiBkdW5nIHN0ci5yZW1vdmVwcmVmaXggKDMuOSkgbHVjIENIQVkiKQogICAgZWxpZiBf'
'cmNfZGs6CiAgICAgICAgbG9pLmFwcGVuZChmInB5dGhvbiBuYXkgS0hPTkcgY28gUHlZQU1MIGR1bmcgZHVvYyAoeyhfcmFf'
'ZGsuc3RyaXAoKS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFdWzo5MF19KToiCiAgICAgICAgICAgICAgICAgICBmIiBcIntz'
'eXMuZXhlY3V0YWJsZX1cIiAtbSBwaXAgaW5zdGFsbCBweXlhbWwiCiAgICAgICAgICAgICAgICAgICAiIChiYW4gbmh1bmcg'
'cHMxIHR1IHRhaSBLSE9ORyBjbyBwaXA6IGNoYXkgbGFpIHZvaSAtUHkgPHB5dGhvbiBkYSBjbyBQeVlBTUw+KSIpCiAgICAj'
'IEJvIHRlc3QgY29uIGdvaSBgc2h1dGlsLndoaWNoYCBjaG8gYmFzaC9hY3Rpb25saW50L3NoZWxsY2hlY2sgKDBlYTk1ZGU6'
'IHQzMyB0MTM3IHQxNTkgY2FuIGFjdGlvbmxpbnQsIHQxMzcgY2FuCiAgICAjIHNoZWxsY2hlY2ssIGNhYyBjYSBjaGF5IG9w'
'cy9jYWlfYWN0aW9ubGludC5zaCBjYW4gYmFzaCkuIFRoaWV1IHRoaSBjYWMgY2EgYXkgaW4gIktIT05HIERPIERVT0M6IHRo'
'aWV1IGAuLi5gIiB2YSBibyBkbyByYQogICAgIyByYz0zIOKAlCBuaHVuZyBjaGkgU0FVIGNhIGJvIHRlc3QgbGFuIE43IChk'
'byB0cmVuIDIwMjYtMDktMzBnLCBQQVRIIHRoaWV1IGFjdGlvbmxpbnQ6IGBDb25nIGN1IGRheSBkdSBkZSBkb2AgS0RELCBy'
'Yz0zCiAgICAjIHNhdSAyIGx1b3QgYm8gdGVzdCkuIEN1bmcgbHkgZG8gUHlZQU1MIGR1b2MgaG9pIG8gZGF5OiBob2kgVFJV'
'T0MsIGN1bmcgUEFUSCBtYSBjaGF5KCkgdHJ1eWVuIGNobyBibyB0ZXN0LgogICAgX3RoaWV1X2NjID0gW2MgZm9yIGMgaW4g'
'KCJiYXNoIiwgImFjdGlvbmxpbnQiLCAic2hlbGxjaGVjayIpIGlmIG5vdCBzaHV0aWwud2hpY2goYyldCiAgICBpZiBfdGhp'
'ZXVfY2M6CiAgICAgICAgbG9pLmFwcGVuZChmInRoaWV1IGNvbmcgY3UgYm8gdGVzdCBnb2kgcXVhIFBBVEg6IHtfdGhpZXVf'
'Y2N9IChhY3Rpb25saW50OiBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggdm9pIEFMX1ZFUjsiCiAgICAgICAgICAgICAgICAgICAi'
'IGJhc2g6IEdpdCBCYXNoLCBraG9uZyBwaGFpIGJhc2guZXhlIGN1YSBXU0wpIikKICAgICMgc2hlbGxjaGVjayBLSE9ORyBu'
'aGFuIC0tbm9yYyB0aGkgYWN0aW9ubGludCAxLjcuNyAodHUgdHJ1eWVuIC0tbm9yYykgbGFtIHQzMyBETywgdmEgU0hFTExD'
'SEVDS19PUFRTPS0tbm9yYyBjdWEgY2hheSgpIGxhbQogICAgIyB0MTM3IERPIOKAlCBjYSAibGEiID0+IFRSVU9UIGdpYSAo'
'ZG8gdHJlbiAyMDI2LTA5LTMwaCwgc2hlbGxjaGVjayBnaWEgdHUgY2hvaSAtLW5vcmM6IGJhbiAzMGggcmM9MSBgbGE6IFsn'
'dDMzJ11gIHNhdSBjYQogICAgIyBibyB0ZXN0KS4gYHdoaWNoYCBjaGkgaG9pIENPIE1BVDsgbyBkYXkgaG9pIERVTkcgRFVP'
'Qy4gTmd1b25nIGRvIHRyZW4gc2hlbGxjaGVjayBUSEFUOiAwLjQuNy8wLjUuMC8wLjYuMCB0dSBjaG9pIC0tbm9yYwogICAg'
'IyAocmM9MyksIDAuNy4wIHRybyBsZW4gbmhhbi4gUGhlcCBob2kgcGhhaSB0aGF5IERVTkcgU0hFTExDSEVDS19PUFRTIG1h'
'IGNoYXkoKSBkYXQgY2hvIGx1b3QgY29uOiBiYW4gMzBpIGhvaSB2b2kgYmllbiBDVUEKICAgICMgTkdVT0kgRE8g4oCUIGRv'
'IHRyZW4gMjAyNi0wOS0zMGksIHNoZWxsY2hlY2sgMC45LjAgKyBTSEVMTENIRUNLX09QVFM9LS1leHRlbmRlZC1hbmFseXNp'
'cz10cnVlIChjbyBjdWEgMC4xMCk6IHJjPTMgImtob25nIG5oYW4KICAgICMgLS1ub3JjOiBjYXAgbmhhdCBzaGVsbGNoZWNr'
'IiB0cm9uZyBraGkgdDMzL3QxMzcgcXVhIGNoYXkoKSBkZXUgMS8xLiBHb2kgVEhBTkcgKGtob25nIHF1YSBjaGF5KCkpOiBx'
'dWEgaGFuIHRoaSBydW4oKSBnaWV0CiAgICAjIGR1bmcgc2hlbGxjaGVjazsgcXVhIGNoYXkoKSB0aGkgY2hpIGdpZXQgcHl0'
'aG9uIGNvbiwgc2hlbGxjaGVjayB0cmVvIG8gbGFpIG1vIGNvaSAoZG8gdHJlbiAyMDI2LTA5LTMwaTogMS8xIGNvbiBzb25n'
'KS4KICAgIGVsaWYgc3VicHJvY2Vzcy5ydW4oW3NodXRpbC53aGljaCgic2hlbGxjaGVjayIpLCAiLS1ub3JjIiwgIi0tdmVy'
'c2lvbiJdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0aW1lb3V0PTYwLAogICAgICAgICAgICAgICAgICAgICAgICBlbnY9ZGlj'
'dChvcy5lbnZpcm9uLCBTSEVMTENIRUNLX09QVFM9Ii0tbm9yYyIpKS5yZXR1cm5jb2RlOgogICAgICAgIGxvaS5hcHBlbmQo'
'InNoZWxsY2hlY2sgdHJlbiBQQVRIIGtob25nIG5oYW4gLS1ub3JjIChhY3Rpb25saW50IDEuNy43IHZhIGNoYXkoKSBkZXUg'
'dHJ1eWVuIGNvIGF5KTogY2FwIG5oYXQgc2hlbGxjaGVjayIpCiAgICAjIGFjdGlvbmxpbnQgY3VuZyBwaGFpIERVTkcgRFVP'
'Qywga2hvbmcgY2hpIENPIE1BVDogdDMzL3QxMzcvdDE1OSBnb2kgbm8gVEhBTkcsIHZhIG1vdCBhY3Rpb25saW50IGtob25n'
'IGNoYXkgKHNhaSBraWVuIHRydWMsCiAgICAjIGhvbmcpIGxhbSBjYSBiYSBETyAiYWN0aW9ubGludCBETyAocmM9Li4uKSIg'
'4oCUIGNhICJsYSIgPT4gVFJVT1QgZ2lhIHNhdSBjYSBibyB0ZXN0IChkbyB0cmVuIDIwMjYtMDktMzBqOiBhY3Rpb25saW50'
'IGdpYQogICAgIyByYz0xID0+IG11YyAwIGltIGxhbmcsIHQzMyAibGEiKS4gQmFuIFRIQVQgMS42LjI3LzEuNy43LzEuNy44'
'LzEuNy4xMiBkZXUgcmM9MCB2YSBkZXUgY2hvIHQzMy90MTM3L3QxNTkgUVVBIHRyZW4gMGVhOTVkZS4KICAgICMgYmFzaCBD'
'SEkgaG9pIENPIE1BVCwgY28gY2h1IGRpY2g6IGJhc2ggV1NMIChTeXN0ZW0zMikgbGFtIHQzNS10NDAgRE8gbmh1bmcgY2Eg'
'c2F1IGRldSBOR09BSV9QSEFNX1ZJLCBjb24gdDMyL3QxNTIgdHUgY2hvbgogICAgIyBHaXQgQmFzaCAoX2Jhc2hfcG9zaXgg'
'Y3VhIHVuZyB2aWVuKSDigJQgZG8gdHJlbiAyMDI2LTA5LTMwajogYmFzaCBraWV1IFdTTCA9PiB0MzUtdDQwIERPLCBkZXUg'
'cm9pIHZhbyBuZ29haSBwaGFtIHZpLgogICAgaWYgbm90IF90aGlldV9jYyBhbmQgc3VicHJvY2Vzcy5ydW4oW3NodXRpbC53'
'aGljaCgiYWN0aW9ubGludCIpLCAiLXZlcnNpb24iXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwKICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgIHRpbWVvdXQ9NjApLnJldHVybmNvZGU6CiAgICAgICAgbG9pLmFwcGVuZCgiYWN0aW9u'
'bGludCB0cmVuIFBBVEggY28gbWF0IG5odW5nIGBhY3Rpb25saW50IC12ZXJzaW9uYCByYyE9MCAoa2hvbmcgY2hheSBkdW9j'
'KTogY2FpIGxhaSBiYW4gZ2hpbSBBTF9WRVIiKQoKcmMsIGhlYWQsIF8gPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIkhFQUQi'
'KQppZiByYzogbG9pLmFwcGVuZCgia2hvbmcgZG9jIGR1b2MgSEVBRCIpCmdoaSgiaGVhZCIsIGhlYWQpCnJjX2EsIF8sIF8g'
'PSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICItLWlzLWFuY2VzdG9yIiwgU0hBX0cxLCBoZWFkIG9yICJIRUFEIikKbGFfaGF1'
'X2R1ZSA9IChyY19hID09IDApCmlmIGhlYWQgPT0gU0hBX0cxOgogICAgdGhlX2hlID0gImcxIjsgaW5uKGYiICBIRUFEID0g'
'e2hlYWRbOjhdfSAtPiBEQVkgTEEgZzEuIENIVUEgY28gYmFuIHZhIGcyOyBrZXQgcXVhIGR1b2kgbGEgTkVOIERPLiIpCmVs'
'aWYgbGFfaGF1X2R1ZToKICAgIHRoZV9oZSA9ICJnMiI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gaGF1IGR1ZSBj'
'dWEgZzEgKHtTSEFfRzFbOjhdfSk7IHVuZyB2aWVuIGcyIGhheSBraG9uZzogTjcnIChtdWMgMSkgZGluaCBkYW5oLiIpCmVs'
'c2U6CiAgICB0aGVfaGUgPSAiPyI7IGxvaS5hcHBlbmQoZiJIRUFEPXtoZWFkWzo4XX0gS0hPTkcgcGhhaSBnMSB2YSBLSE9O'
'RyBwaGFpIGhhdSBkdWUgY3VhIHtTSEFfRzFbOjhdfSDigJQgcmViYXNlPyBuaGFtIG5oYW5oPyIpCmdoaSgidGhlX2hlIiwg'
'dGhlX2hlKQpyY19yLCByZWZzLCBfID0gZ2l0KGdvYywgImZvci1lYWNoLXJlZiIsICItLXBvaW50cy1hdCIsIGhlYWQgb3Ig'
'IkhFQUQiLAogICAgICAgICAgICAgICAgICAgICItLWZvcm1hdD0lKHJlZm5hbWU6c2hvcnQpIikKZHNyID0gW3ggZm9yIHgg'
'aW4gcmVmcy5zcGxpdGxpbmVzKCkgaWYgeC5zdHJpcCgpIGFuZCB4LnN0cmlwKCkgIT0gImRvLXRhbSJdCmdoaSgicmVmX3Ry'
'b190b2lfaGVhZCIsIGRzcikKaW5uKGYiICByZWYgdHJvIHRvaSBIRUFEOiB7JywgJy5qb2luKGRzcikgaWYgZHNyIGVsc2Ug'
'JyhraG9uZyByZWYgbmFvIC0gSEVBRCByb2kgdHUgZG8pJ30iKQoKaWYgbG9pOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBE'
'TyBEVU9DOiBuZW4gZG8gc2FpLCBLSE9ORyBpbiBrZXQgbHVhbiBuYW8uIikKICAgIGZvciB4IGluIGxvaTogaW5uKCIgIC0i'
'LCB4KQogICAgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAxLiBraWNoIHRodW9jIChONycgY3VhIHNwZWMgcjMp'
'IC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIxLiBLSUNIIFRIVU9DIOKAlCB0cmFuIHNw'
'ZWMgcjM6IDw9IDIgdGVwIHZhIDw9IDQwMCBkb25nIHRoZW0iKQojIFZFIE5FTiBQSEFJIFRVT0kg4oCUIHZhIHBoYWkgQ0hV'
'TkcgTUlOSCBkdW9jIGxhIHR1b2ksIGtob25nIHBoYWkgZ2lhIGRpbmguCiMgQmFpIGhvYyB0cmEgZ2lhIDE5LTA5LTIwMjY6'
'IGNsb25lIHRhaSBkdW5nIGNoaSBmZXRjaCBuaGFuaCBiYW4gdmEsIGBvcmlnaW4vbWFzdGVyYAojIGR1bmcgeWVuIHR1IDE0'
'LTA5IChjMTZiZDMyLCBzYXUgOTcgY29tbWl0KS4gbWVyZ2UtYmFzZSByb2kgdmUgZHVuZyBkaW5oIG1hc3RlciBjdSwKIyBu'
'ZW4gZGlmZiBOVU9UIGNhIDk3IGNvbW1pdCBtYXN0ZXI6IGRvIHJhIDQ2IHRlcCAvICs3MTE4IHRoYXkgdmkgMiB0ZXAgLyAr'
'Mzk3IOKAlAojIENVTkcgTU9UIENPTU1JVCAwZWE5NWRlLiBNb3QgdGlldSBjaGkgREVMVEEgbWEgdmUgbmVuIGtob25nIHR1'
'b2kgdGhpIGtob25nIHNhaQojIGxlY2ggbW90IGNodXQsIG5vIHNhaSBjYSBtb3QgYmFjIGRvIGxvbi4KIyBDaG8gbmVuOiBu'
'ZW4ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGxhIHR1b2kgPT4gS0hPTkcgRE8gRFVPQyAocmM9MyksIEtIT05HIHBoYWkgVFJV'
'T1QuCiMgVFJVT1QgbGEgbW90IFBIQU4gUVVZRVQgdmUgYmFuIHZhOyBwaGFuIHF1eWV0IGNoaSBkdW9jIHBoZXAgcGhhdCBy'
'YSBraGkgZGEgZG8gZHVvYy4KZXIgPSAiIgpyY191LCB1cmxfdGhvLCBfID0gZ2l0KGdvYywgInJlbW90ZSIsICJnZXQtdXJs'
'IiwgIm9yaWdpbiIpCnVybF9vLCB1cmxfaW4gPSBfdXJsX3NhY2godXJsX3RobyksIF91cmxfaW4odXJsX3RobykKZ2hpKCJv'
'cmlnaW5fdXJsIiwgdXJsX2luKTsgaW5uKGYiICBvcmlnaW4gICAgICAgOiB7dXJsX2luIG9yICcoa2hvbmcgZG9jIGR1b2Mp'
'J30iKQp1cmxfb2sgPSAobm90IHJjX3UpIGFuZCB1cmxfby5yc3RyaXAoIi8iKSBpbiBVUkxfS0hPX0hPUF9MRQpyY19sciwg'
'b3V0X2xyLCBlcl9sciA9IGdpdChnb2MsICJscy1yZW1vdGUiLCAib3JpZ2luIiwgInJlZnMvaGVhZHMvbWFzdGVyIikgaWYg'
'dXJsX29rIGVsc2UgKDEsICIiLCAiIikKZXJfbHIgPSBfYW5fdXNlcmluZm8oZXJfbHIpCnJjX2xtLCBsbSwgZXJfbG0gICAg'
'ID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJvcmlnaW4vbWFzdGVyIikKcm0gPSBvdXRfbHIuc3BsaXQoKVswXSBpZiAobm90'
'IHJjX2xyIGFuZCBvdXRfbHIuc3RyaXAoKSkgZWxzZSAiIgppZiBub3QgdXJsX29rOgogICAga2V0KCJONycga2ljaCB0aHVv'
'YyIsIEtERCwgZiJvcmlnaW49e3VybF9pbiFyfSBLSE9ORyBwaGFpIGtobyB0aGF0IOKAlCAndHVvaScgc28gdm9pIG5vIGto'
'b25nIGNodW5nIG1pbmggZHVvYyBnaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIG5vdCBy'
'bToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJraG9uZyBob2kgZHVvYyBtYXN0ZXIgdHJlbiBy'
'ZW1vdGUgKGxzLXJlbW90ZSByYz17cmNfbHJ9KToge2VyX2xyWzo2MF19ICIKICAgICAgICBmIuKAlCBraG9uZyBjaHVuZyBt'
'aW5oIGR1b2MgdmUgbmVuIGNvbiB0dW9pIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgcmNf'
'bG0gb3Igbm90IGxtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyBkb2MgZHVvYyBvcmlnaW4vbWFz'
'dGVyIHRyb25nIGNsb25lOiB7ZXJfbG1bOjYwXX0iKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxp'
'ZiBsbSAhPSBybToKICAgICMgRGVtIHhlbSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRlbSBkdW9jIOKAlCBjb24gc28gbmF5IG5v'
'aSBybyBtdWMgZG8gc2FpIGxlY2guCiAgICByY19jLCBzYXUsIF8gPSBnaXQoZ29jLCAicmV2LWxpc3QiLCAiLS1jb3VudCIs'
'IGYie2xtfS4ue3JtfSIpCiAgICB4YSA9IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1pdCIgaWYgKG5vdCByY19jIGFuZCBzYXUu'
'c3RyaXAoKS5pc2RpZ2l0KCkpIGVsc2UgIiIKICAgIGlubihmIiAgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZSA6IHtsbVs6'
'MTJdfSIpCiAgICBpbm4oZiIgIG1hc3RlciB0cmVuIHJlbW90ZSAgICAgICAgOiB7cm1bOjEyXX17eGF9IikKICAgIGdoaSgi'
'bWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBL'
'REQsCiAgICAgICAgZiJ2ZSBuZW4gQ1U6IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19ICE9IHJlbW90ZT17cm1bOjEyXX17eGF9'
'ICIKICAgICAgICBmIuKAlCBjaGF5IGBnaXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2luIG1hc3RlcmAgcm9pIGRvIGxhaSIpCiAg'
'ICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbHNlOgogICAgaW5uKGYiICB2ZSBuZW4gVFVPSTogb3JpZ2lu'
'L21hc3RlciA9IHtsbVs6MTJdfSA9PSBtYXN0ZXIgdHJlbiByZW1vdGUiKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7'
'IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAgcmNfbWIsIG1iLCBlcl9tYiA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwg'
'Im9yaWdpbi9tYXN0ZXIiLCBoZWFkKQppZiByY19tYiBvciBub3QgbWI6CiAgICBpZiBtYiA9PSAiIiBhbmQgcm0gYW5kIGxt'
'ID09IHJtOgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9jIG1lcmdlLWJhc2Ug'
'dm9pIG9yaWdpbi9tYXN0ZXI6IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgogICAgZ2hpKCJtZXJn'
'ZV9iYXNlIiwgbWIpCiAgICBpbm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7bWJbOjEyXX0iKQog'
'ICAgaWYgbWIgIT0gU0hBX0JBU0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2UgbWEgc3BlYyByMyBr'
'aGFpICh7U0hBX0JBU0VfU1BFQ1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQogICAgICAgIGlubigi'
'ICAgICAgICAgRG8gc28gYmFzZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcgdmFvLiBEdW5nIG1lcmdlLWJhc2UgbW9p'
'IGxhIHZpZWMgY3VhIGV4ZWN1dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJkaWZmLXRyZWUiLCAi'
'LXIiLCAiLU0iLCAiLS1kaWZmLWFsZ29yaXRobT1teWVycyIsICItLW51bXN0YXQiLCBTSEFfQkFTRV9TUEVDLCBoZWFkKQog'
'ICAgICAgIGlmIG5vdCByY194OgogICAgICAgICAgICBoID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnNfeC5zcGxpdGxp'
'bmVzKCkgaWYgbC5zdHJpcCgpXQogICAgICAgICAgICBhID0gc3VtKGludCh4WzBdKSBmb3IgeCBpbiBoIGlmIHhbMF0uaXNk'
'aWdpdCgpKQogICAgICAgICAgICBnaGkoIm51bXN0YXRfdGhlb19iYXNlX3NwZWMiLCB7InRlcCI6IGxlbihoKSwgInRoZW0i'
'OiBhfSkKICAgICAgICAgICAgaW5uKGYiICAgICAgICAgKGRvaSBjaGlldTogc28gYmFzZSBzcGVjID0ge2xlbihoKX0gdGVw'
'IC8gK3thfSDigJQgY29uIHNvIGF5IEtIT05HIGR1bmcgZGUgY2hhbSkiKQogICAgIyBQTFVNQklORywga2hvbmcgUE9SQ0VM'
'QUlOOiBgZ2l0IGRpZmZgIGRvYyBjYXUgaGluaCBVSSBDVUEgTkdVT0kgRE8gKGRpZmYuYWxnb3JpdGhtLCBkaWZmLnJlbmFt'
'ZXMsIGRpZmYub3JkZXJGaWxlLAogICAgIyBjb2xvci5kaWZmKSwgdmEgZ2lhIHRyaSBIT1AgTEUgZG9pIGx1b24gU08gZG9u'
'ZyBtYSB2YW4gcmEgY2h1IHNvIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBpOiB1bmcgdmllbiB0b25nIGhvcCAobXllcnMgKzQw'
'MSkgPT4KICAgICMgYmFuIDMwaSBEQVQgMiB0ZXAgLyArNDAwIGR1b2kgYGRpZmYuYWxnb3JpdGhtID0gaGlzdG9ncmFtYCBo'
'b2FjIGBwYXRpZW5jZWAsIFRSVU9UICs0MDEga2hpIG1hYyBkaW5oOyAxMC83NSBjb21taXQgY2hhbQogICAgIyB3cml0ZSBz'
'ZXQgY28gc28gZG9uZyBkb2kgdGhlbyB0aHVhdCB0b2FuLiBgZGlmZi10cmVlIC1yIC1NYCA9IG1hYyBkaW5oIGN1YSBgZ2l0'
'IGRpZmZgIChyZW5hbWVzIGJhdCkgdmEgS0hPTkcgZG9jIGNhYyBraG9hCiAgICAjIGF5LiBUaHVhdCB0b2FuIHBoYWkgVFVP'
'TkcgTUlOSDogZGlmZi48ZHJpdmVyPi5hbGdvcml0aG0gKHF1YSBjb3JlLmF0dHJpYnV0ZXNGaWxlIGN1YSBuZ3VvaSBkbykg'
'VkFOIGxvdCB2YW8gcGx1bWJpbmcg4oCUCiAgICAjIGRvIHRyZW4gMjAyNi0wOS0zMGksIGAqLnB5IGRpZmY9YWxnYCArIGRp'
'ZmYuYWxnLmFsZ29yaXRobT1oaXN0b2dyYW06IGRpZmYtdHJlZSArNDAxIGNobyB1bmcgdmllbiBteWVycyArNDAwOyBjbyB0'
'dW9uZyBtaW5oCiAgICAjIHRoYW5nIGtob2EgYXkuIGF0dHJpYnV0ZXMgYC1kaWZmYC9jb3JlLmJpZ0ZpbGVUaHJlc2hvbGQg'
'dmFuIGFwID0+IGAtYCA9PiBLSE9ORyBETyBEVU9DIChjaG90IGR1b2kpLgogICAgcmMsIG5zLCBlciA9IGdpdChnb2MsICJk'
'aWZmLXRyZWUiLCAiLXIiLCAiLU0iLCAiLS1kaWZmLWFsZ29yaXRobT1teWVycyIsICItLW51bXN0YXQiLCBtYiwgaGVhZCkK'
'aWYgcmM6CiAgICBwYXNzCmVsc2U6CiAgICBoYW5nID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnMuc3BsaXRsaW5lcygp'
'IGlmIGwuc3RyaXAoKV0KICAgIHRoZW0gPSBzdW0oaW50KGhbMF0pIGZvciBoIGluIGhhbmcgaWYgaFswXS5pc2RpZ2l0KCkp'
'CiAgICB4b2EgID0gc3VtKGludChoWzFdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMV0uaXNkaWdpdCgpKQogICAgZ2hpKCJzb190'
'ZXAiLCBsZW4oaGFuZykpOyBnaGkoImRvbmdfdGhlbSIsIHRoZW0pOyBnaGkoImRvbmdfeG9hIiwgeG9hKQogICAgZm9yIGgg'
'aW4gaGFuZzogaW5uKGYiICAgIHtoWzJdOjM0fSAre2hbMF06PDV9IC17aFsxXX0iKQogICAgaW5uKGYiICAgIFRPTkc6IHts'
'ZW4oaGFuZyl9IHRlcCwgK3t0aGVtfSwgLXt4b2F9ICAgKHRyYW46IHtUUkFOX1RFUH0gdGVwIC8ge1RSQU5fRE9OR30gZG9u'
'ZyB0aGVtKSIpCiAgICBjaGFtID0gc29ydGVkKHtoWzJdIGZvciBoIGluIGhhbmd9ICYgV1JJVEVfU0VUX0cyKTsgZ2hpKCJj'
'aGFtX3dyaXRlX3NldCIsIGNoYW0pCiAgICBkZWYgX2NhX21vaV9jbyhyZXYpOgogICAgICAgICMgY2F0LWZpbGUsIGtob25n'
'IGBzaG93YDogYGdpdCBzaG93YCBjaGV0IHZvaSBjYXUgaGluaCBVSSBnbyBzYWkgKGRvIHRyZW4gMjAyNi0wOS0zMGk6IGxv'
'Zy5kYXRlIGdvIHNhaSA9PiBiYW4gMzBpIGdvaQogICAgICAgICMgMGVhOTVkZSBsYSAia2hvbmcgcGhhaSB1bmcgdmllbiAu'
'Li4gTm9uZSDigJQgZGEgbGFuZD8gbmhhbSBuaGFuaD8iKS4KICAgICAgICByXywgbmRfLCBfID0gZ2l0KGdvYywgImNhdC1m'
'aWxlIiwgIi1wIiwgZiJ7cmV2fTpvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICByZXR1cm4gTm9uZSBpZiBy'
'XyBlbHNlIHt0IGZvciB0IGluIENBX01PSV9HMiBpZiByZS5zZWFyY2gociIoP20pXmRlZiAiICsgdCArIHIiW2Etel0/XyIs'
'IG5kXyl9CiAgICBvX21iLCBvX2ggPSBfY2FfbW9pX2NvKG1iKSwgX2NhX21vaV9jbyhoZWFkKQogICAgbWFuZyA9IHNvcnRl'
'ZChvX2ggLSBvX21iLCBrZXk9c29fY2EpIGlmIChvX21iIGlzIG5vdCBOb25lIGFuZCBvX2ggaXMgbm90IE5vbmUpIGVsc2Ug'
'Tm9uZQogICAgZ2hpKCJjYV9tb2lfZzJfbWFuZ192YW8iLCBtYW5nKQogICAgaWYgbm90IG1hbmc6CiAgICAgICAgIyBEbyBS'
'T05HIChkYSBsYW5kLCBjaGluaCBtYXN0ZXIpLCBuaGFtIG5oYW5oLCBoYXkgbmhhbmggY3VhIHBhY2tldCBLSEFDIGNoYW0g'
'Y3VuZyB0ZXA6CiAgICAgICAgIyBraG9uZyBtYW5nIGNhIG1vaSBuYW8gY3VhIGcyIHRoaSBraG9uZyBwaGFpIHVuZyB2aWVu'
'LiBEb2Mga2hvbmcgZHVvYyAoTm9uZSkgY3VuZyB2YXkuCiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJk'
'b2kgdHVvbmcga2hvbmcgcGhhaSB1bmcgdmllbjoge2xlbihoYW5nKX0gdGVwLCBjaGFtIHtjaGFtfSwgY2EgbW9pICIKICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBmImcyIG1hbmcgdmFvIHttYW5nIXJ9IOKAlCBkYSBsYW5kPyBuaGFt'
'IG5oYW5oPyBwYWNrZXQga2hhYz8iKQogICAgZWxzZToKICAgICAgICAjIG51bXN0YXQgaW4gYC1gIChraG9uZyBjbyBzbyBk'
'b25nKSBjaG8gdGVwIGJpbmFyeS8tZGlmZiB0aGVvIGF0dHJpYnV0ZXMg4oCUIGtlIGNhIGF0dHJpYnV0ZXMgQ1VBIE5HVU9J'
'IERPIChkbyB0cmVuCiAgICAgICAgIyAyMDI2LTA5LTMwZzogY29yZS5hdHRyaWJ1dGVzRmlsZSBgKi5weSAtZGlmZmAgPT4g'
'IjIgdGVwIC8gKzAiIERBVCBjaG8gMGVhOTVkZSwgdGhhdCArMzk3KS4gYC1gIGxhIEtIT05HIERPIERVT0MsCiAgICAgICAg'
'IyBraG9uZyBwaGFpIDA7IFRSVU9UIHRoZW8gc28gdGVwIC8gc28gZG9uZyBEQSBkZW0gZHVvYyB2YW4gZ2l1IChxdWFuIHNh'
'dCB0cnVjIHRpZXApLgogICAgICAgIGtob25nX3NvID0gW2hbMl0gZm9yIGggaW4gaGFuZyBpZiBub3QgKGhbMF0uaXNkaWdp'
'dCgpIGFuZCBoWzFdLmlzZGlnaXQoKSldOyBnaGkoInRlcF9raG9uZ19zb19kb25nIiwga2hvbmdfc28pCiAgICAgICAgdnVv'
'dCA9IGxlbihoYW5nKSA+IFRSQU5fVEVQIG9yIHRoZW0gPiBUUkFOX0RPTkcKICAgICAgICBrZXQoIk43JyBraWNoIHRodW9j'
'IiwgVFJVT1QgaWYgdnVvdCBlbHNlIChLREQgaWYga2hvbmdfc28gZWxzZSBEQVQpLAogICAgICAgICAgICBmIntsZW4oaGFu'
'Zyl9IHRlcCAvICt7dGhlbX0iICsgKGYiIOKAlCBudW1zdGF0IEtIT05HIGNvIHNvIGRvbmcgY2hvIHtraG9uZ19zb30iIGlm'
'IGtob25nX3NvIGVsc2UgIiIpKQoKIyBDb25nIGtpY2ggdGh1b2MgUEhBSSBkZSBsYWkgTU9UIGtldCBxdWEuIExlbmggbnVt'
'c3RhdCBob25nIHRoaSBuaGFuaCBgaWYgcmM6IHBhc3NgIGtob25nIGdoaSBnaSwgdmEgdmFuZyBtYXQgbyBkYXkKIyB0aGFu'
'aCBEQVQgbyBibyBnb3A6IGNhdSBoaW5oIGRpZmYgQ1VBIE5HVU9JIERPIGhvbmcgKGRpZmYub3JkZXJGaWxlIHRybyB0ZXAg'
'a2hvbmcgY28sIGRpZmYuYWxnb3JpdGhtIGdvIHNhaSA9PiByYz0xMjgpIGNobwojIC0tY2hpLWtpY2gtdGh1b2MgcmM9MCB2'
'b2kgMCBjaG90LCBsdW90IGRheSBkdSAiREFUIDExIiByYz0wIChkbyB0cmVuIDIwMjYtMDktMzBoLCAwZWE5NWRlKS4gVmFu'
'ZyBtYXQgbGEgS0hPTkcgRE8gRFVPQy4KIyBUdSAzMGogbnVtc3RhdCBsYSBkaWZmLXRyZWUgKGtob25nIGRvYyBoYWkga2hv'
'YSBheSk7IGR1b25nIGNvbiBsYWkgZG8gZHVvYzogZGlmZi5yZW5hbWVMaW1pdCBnbyBzYWkgPT4gcmM9MTI4LgppZiBub3Qg'
'YW55KGNbMF0gPT0gIk43JyBraWNoIHRodW9jIiBmb3IgYyBpbiBjaG90KToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBL'
'REQsIGYiY29uZyBLSE9ORyByYSBrZXQgcXVhIChnaXQgZGlmZi10cmVlIC0tbnVtc3RhdCByYz17cmN9KToge19hbl91c2Vy'
'aW5mbyhlcilbOjcwXX0iKQoKIyBEaW5oIGRhbmggVEhBVCBuYW0gbyBONycgKGNhIG1vaSBnMiBtYW5nIHZhbyksIEtIT05H'
'IG8gImhhdSBkdWUgZzEiOiBnMSBkYSBsYW5kIG5lbiBtb2kgbmhhbmggZGV1CiMgbGEgaGF1IGR1ZS4gRG9uZyBkYXUga2hv'
'aSBkYW4gcGhhaSB0dSBraGFpIHRoZW8ga2V0IHF1YSBheSAoZG8gZHVvYzogbWFzdGVyIDQ0NjIwZTggbW8ga2hvaSBiYW5n'
'CiMgIlRIRSBIRSBETyBEVU9DOiBnMiIsIEpTT04gInRoZV9oZSI6ICJnMiIsIHRyb25nIGtoaSBONycgZGEga2V0IGx1YW4g'
'Imtob25nIHBoYWkgdW5nIHZpZW4iKS4KIyBOaGFuIGNoaSBkdW9jIG5vaSBEVU5HIGNhaSBkbyBkdW9jOiBgW11gIGtob25n'
'IHRhY2ggImRhIGxhbmQiIGtob2kgIm5oYW0gbmhhbmgiLyJwYWNrZXQga2hhYyIgKGRvCiMgZHVvYyB0cmVuIDIwMjYtMDkt'
'MzBiOiB1bmcgdmllbiAyYTY3OTY4IERBIExBTkQgYmkgZ29pICJLSE9ORyBwaGFpIHVuZyB2aWVuIGcyIikuCmlmIHRoZV9o'
'ZSA9PSAiZzIiIGFuZCBub3Qgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKToKICAgIHRoZV9oZSA9ICgiS0hPTkcgbWFu'
'ZyBjYSBtb2kgZzIgbmFvIChkYSBsYW5kPyBuaGFtIG5oYW5oPyBwYWNrZXQga2hhYz8pIiBpZiBzby5nZXQoImNhX21vaV9n'
'Ml9tYW5nX3ZhbyIpID09IFtdCiAgICAgICAgICAgICAgZWxzZSAiZzI/IChDSFVBIGRpbmggZGFuaCBkdW9jIGRvaSB0dW9u'
'ZykiKQogICAgZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCgojIENvbmcgbmhhbmg6IGRvIFJJRU5HIGtpY2ggdGh1b2MgKHZhaSBn'
'aWF5KSByb2kgZHVuZy4gRHVuZyBraGkgY2FuIHhhYyBtaW5oIGxhaQojIHZlIG5lbiBtYSBraG9uZyBtdW9uIHRyYSAyMC00'
'NSBwaHV0IGNobyBjYSBibyB0ZXN0LgppZiAiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Y6CiAgICBpbm4oIiIpOyBp'
'bm4oIj0iICogNzgpCiAgICBpbm4oIi0tY2hpLWtpY2gtdGh1b2M6IENISSBkbyBjb25nIGtpY2ggdGh1b2MuIERheSBLSE9O'
'RyBwaGFpIG1vdCBsdW90IG5naGllbSB0aHUuIikKICAgIGlubigiLSIgKiA3OCkKICAgIGZvciBfdCwgX3R0LCBfY3QgaW4g'
'Y2hvdDogaW5uKGYiICB7X3R0OjE0fSB7X3R9IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICBfayA9IHN1'
'bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCiAgICBfciA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3Qg'
'aWYgdCA9PSBUUlVPVCkKICAgIHN5cy5leGl0KDMgaWYgX2sgZWxzZSAoMSBpZiBfciBlbHNlIDApKQoKQ0hJX1BST0JFID0g'
'Ii0tY2hpLXByb2JlIiBpbiBzeXMuYXJndiAgICAjIGJvIHF1YSBibyB0ZXN0ICsgTjc7IGdpdSAwLCAxLCAzCiMgLS0tLS0t'
'LS0tLS0tLS0tLSAyLiBibyB0ZXN0IGRheSBkdSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4o'
'IiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjIuIEJPIFRFU1QgREFZIERVICgxMC00MCBwaHV0KSIpCiAgICByY19uLCBvdXRf'
'biA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIGdvYykKICAgIGdoaSgicmNfc3VpdGUiLCByY19uKQog'
'ICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dF9uKQogICAgaW5uKCIgIHJjID0iLCByY19uLCAifCIsIG0uZ3JvdXAoMCkgaWYg'
'bSBlbHNlICIoS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCkiKQogICAgaWYgbToKICAgICAgICBnaGkoImRhdCIsIGlu'
'dChtLmdyb3VwKDEpKSk7IGdoaSgidHJlbiIsIGludChtLmdyb3VwKDIpKSk7IGdoaSgiYm9fcXVhX3NvIiwgaW50KG0uZ3Jv'
'dXAoNCkpKQogICAgZG9faGV0LCBnYywgdGluID0gZG9jX2RvKG91dF9uKQogICAgZ2hpKCJzb19jYV9kbyIsIGxlbihkb19o'
'ZXQpKTsgZ2hpKCJsaWV0X2tlX2RheV9kdSIsIHRpbikKICAgIGZvciBnIGluIGdjOiBpbm4oIiAgICoiLCBnKQogICAgaW5u'
'KCIiKTsgaW5uKGYiICA9PT0ge2xlbihkb19oZXQpfSBDQSBETyA9PT0iKQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwg'
'a2V5PXNvX2NhKToKICAgICAgICBpbm4oZiIgICB7dC5zcGxpdCgnXycpWzBdOjd9IHt0fSIpOyBpbm4oZiIgICAgICAgICAg'
'IHtkb19oZXRbdF1bOjE1MF19IikKICAgIGdoaSgiZG9fbHlfZG8iLCB7dDogZG9faGV0W3RdWzozMDBdIGZvciB0IGluIGRv'
'X2hldH0pCiAgICAjIC0tLS0gQ0hPVDogbW9pIGNhIERPIHBoYWkgR0lBSSBUSElDSCBEVU9DIC0tLS0KICAgICMgVGhpZXUg'
'Y2hvdCBuYXksIGJvIGRvIGluIGRhbmggc2FjaCBkbyByb2kgdmFuIHRob2F0IHJjPTAuIERvIGR1bmcgbGEgbG9pIGRhIHhh'
'eSByYToKICAgICMgbHVvdCBXaW5kb3dzIDE5LTA5IGNvIHQxNzEgRE8gbWEgYm8gZG8gYmFvICJEQVQgMTAgfCBUUlVPVCAw'
'IiB2YSByYz0wLgogICAgZGVmIF9raG9hKHQpOiByZXR1cm4gdC5zcGxpdCgiXyIpWzBdCiAgICBkb19wYWNrZXQsIGRvX2xh'
'LCBkb190aGlldV9jb25nX2N1ID0gW10sIFtdLCBbXQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToK'
'ICAgICAgICBrLCBseSA9IF9raG9hKHQpLCBkb19oZXRbdF0KICAgICAgICBpZiBrIGluIENBX1BBQ0tFVDogICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICBkb19wYWNrZXQuYXBwZW5kKHQpCiAgICAgICAgZWxpZiAiS0jDlE5HIMSQTyDEkMav4bui'
'QyIgaW4gbHkgb3IgInRoaeG6v3UgYCIgaW4gbHk6ICBkb190aGlldV9jb25nX2N1LmFwcGVuZCh0KQogICAgICAgIGVsaWYg'
'ayBpbiBOR09BSV9QSEFNX1ZJOiAgICAgICAgICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICBlbHNlOiAgICAgICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb19sYS5hcHBlbmQodCkKICAgIGdoaSgiZG9fcGFja2V0IiwgZG9f'
'cGFja2V0KTsgZ2hpKCJkb19sYSIsIGRvX2xhKTsgZ2hpKCJkb190aGlldV9jb25nX2N1IiwgZG9fdGhpZXVfY29uZ19jdSkK'
'ICAgIGlubigiIikKICAgIGlubihmIiAgY2EgRE8gdGh1b2MgQ0hJTkggcGFja2V0IG5heSA6IHtbX2tob2EoeCkgZm9yIHgg'
'aW4gZG9fcGFja2V0XSBvciAna2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERPIG5nb2FpIHBoYW0gdmkgKHIzIGtoYWkp'
'OiB7W19raG9hKHgpIGZvciB4IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSkgaWYgX2tob2EoeCkgaW4gTkdPQUlfUEhB'
'TV9WSV19IikKICAgIGlubihmIiAgY2EgRE8gdmkgVEhJRVUgQ09ORyBDVSAgICAgICA6IHtbX2tob2EoeCkgZm9yIHggaW4g'
'ZG9fdGhpZXVfY29uZ19jdV0gb3IgJ2tob25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBMQSAoa2hvbmcgZ2lhaSB0aGlj'
'aCBkdW9jKToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV0gb3IgJ2tob25nIGNvJ30iKQogICAgIyAtLS0tIENIT1Q6IHBo'
'ZXAgZG8gcGhhaSBUUk9OIHRydW9jIGtoaSBtb3QgY2h1IERBVCBuYW8gZHVvYyBwaGF0IC0tLS0KICAgICMgQmFuIHRydW9j'
'IGNoaSBJTiBgdGluYC9gcmNfc3VpdGVgOiBibyB0ZXN0IGNoZXQgZ2l1YSB0MTcxIChyYz0xMzQsIGtob25nIGRvbmcgdG9u'
'ZykKICAgICMgdmFuIHJhICJEQVQgMTIgfCBUUlVPVCAwIiByYz0wOyBjYSBQQUNLRVQgdmFuZyBtYXQgaGF5IGJpIEJPIFFV'
'QSBjdW5nIGR1b2MgY2hhbSBuaHUKICAgICMgImtob25nIGRvIi4gVmFuZyBtYXQga2hvbmcgcGhhaSAia2hvbmcgZG8iIOKA'
'lCBsYSBLSE9ORyBETyBEVU9DLgogICAgdmFuZyA9IFt0IGZvciB0IGluIHNvcnRlZChDQV9QQUNLRVQsIGtleT1zb19jYSkg'
'aWYgbWF1X2NhKG91dF9uLCB0KSBub3QgaW4gKCJRVUEiLCAiRE8iKV0KICAgIGx5X2tkZCA9IFtdCiAgICBpZiBub3QgdGlu'
'OiBseV9rZGQuYXBwZW5kKCJkYW5oIHNhY2ggZG8gS0hPTkcgZGF5IGR1IikKICAgIGlmIHJjX24gbm90IGluICgwLCAxKSBv'
'ciAocmNfbiA9PSAxKSAhPSBib29sKGRvX2hldCk6CiAgICAgICAgbHlfa2RkLmFwcGVuZChmInJjIGJvIHRlc3Q9e3JjX259'
'IGtob25nIGtob3Age2xlbihkb19oZXQpfSBjYSBETyBkb2MgZHVvYyIpCiAgICBpZiB2YW5nOiBseV9rZGQuYXBwZW5kKGYi'
'Y2EgUEFDS0VUIHZhbmcvYm8gcXVhOiB7dmFuZ30iKQogICAgZ2hpKCJjYV9wYWNrZXRfdmFuZyIsIHZhbmcpOyBnaGkoImx5'
'X2RvX2NodWFfdHJvbiIsIGx5X2tkZCkKICAgIGlmIGx5X2tkZDoga2V0KCJCbyB0ZXN0IGNoYXkgVFJPTiB2YSBkb2MgRFUi'
'LCBLREQsICI7ICIuam9pbihseV9rZGQpKQogICAgY2h1YV90cm9uID0gS0REIGlmIGx5X2tkZCBlbHNlIERBVAogICAga2V0'
'KCJLaG9uZyBjYSBuYW8gY3VhIFBBQ0tFVCBiaSBETyIsIGNodWFfdHJvbiBpZiBub3QgZG9fcGFja2V0IGVsc2UgVFJVT1Qs'
'CiAgICAgICAgIiIgaWYgbm90IGRvX3BhY2tldCBlbHNlIGYiRE86IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XX0g'
'4oCUIGJhbiB2YSBDSFVBIHhvbmciKQogICAga2V0KCJNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIsIGNodWFfdHJv'
'biBpZiBub3QgZG9fbGEgZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9fbGEgZWxzZSBmImxhOiB7W19raG9hKHgp'
'IGZvciB4IGluIGRvX2xhXX0iKQogICAgaWYgZG9fdGhpZXVfY29uZ19jdToKICAgICAgICBrZXQoIkNvbmcgY3UgZGF5IGR1'
'IGRlIGRvIiwgS0RELCBmInRoaWV1IGNvbmcgY3UgY2hvIHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV19'
'IikKCiAgICBicSA9IHNvcnRlZCh7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXRfbil9LCBrZXk9c29fY2Ep'
'OyBnaGkoImNhX2JvX3F1YSIsIGJxKQogICAgaW5uKCIiKTsgaW5uKGYiICBCTyBRVUEgKHtsZW4oYnEpfSk6IHtbeC5zcGxp'
'dCgnXycpWzBdIGZvciB4IGluIGJxXX0iKQoKICAgIGlubigiIik7IGlubigiICBOMS1ONCAodDE2NS10MTY4KSwgdGlldSBj'
'aGkgbmdoaWVtIHRodSBjdWEgcjIsIG5heSBsYSBjaGkgYmFvIGhvaSBxdXk6IikKICAgIGI0ID0ge3Q6IG1hdV9jYShvdXRf'
'biwgdCkgZm9yIHQgaW4gQ0FNT0l9OyBnaGkoImNhX21vaSIsIGI0KQogICAgZm9yIHQgaW4gQ0FNT0k6IGlubihmIiAgICAg'
'e3R9OiB7YjRbdF19IikKICAgICMgQk9fUVVBL3ZhbmcgbGEgQ0hVQSBDSEFZLCBraG9uZyBwaGFpIERPOiBjaGkgbW90IGNh'
'IERPIG1vaSBkdW9jIHBoYXQgVFJVT1QuCiAgICBrZXQoIk4xLU40ICh0MTY1LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJR'
'VUEiIGZvciB2IGluIGI0LnZhbHVlcygpKQogICAgICAgIGVsc2UgKFRSVU9UIGlmIGFueSh2ID09ICJETyIgZm9yIHYgaW4g'
'YjQudmFsdWVzKCkpIGVsc2UgS0REKSwgc3RyKGI0KSkKCiAgICBpbm4oIiIpOyBpbm4oIiAgMTUgY2EgdHVuZyBkbyB0cmVu'
'IENJOiIpCiAgICBiMTUgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQog'
'ICAgaW5uKCIgICAgIiArICIgICIuam9pbihmInt0fTp7YjE1W3RdfSIgZm9yIHQgaW4gQ0ExNSkpCgogICAgIyB0MTM2IOKA'
'lCBOMTIgZG8gR0lBTiBUSUVQIHF1YSBrZXQgcXVhIGNhCiAgICB0MTM2X3RlbiA9IG5leHQoKHQgZm9yIHQgaW4gZG9faGV0'
'IGlmIHQuc3RhcnRzd2l0aCgidDEzNiIpKSwgTm9uZSkKICAgIGlmIGIxNS5nZXQoInQxMzYiKSA9PSAiUVVBIjoKICAgICAg'
'ICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBEQVQsICJ0MTM2IFFVQSIpCiAgICBlbGlmIGIxNS5nZXQoInQx'
'MzYiKSAhPSAiRE8iOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIEtERCwgZiJ0MTM2ID0ge2Ix'
'NS5nZXQoJ3QxMzYnKSFyfSDigJQga2hvbmcgY2hheS9raG9uZyB0aGF5IikKICAgIGVsc2U6CiAgICAgICAgbHkgPSBkb19o'
'ZXQuZ2V0KHQxMzZfdGVuLCAiIikKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBUUlVPVCwgZiJE'
'Tzoge2x5Wzo5MF19IikKCiMgLS0tLS0tLS0tLS0tLS0tLSAzLiBwcm9iZSBUSEFORyB2YW8gaGFtIC0tLS0tLS0tLS0tLS0t'
'LS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIzLiBQUk9CRSBUSEFORyDigJQgZ29pIF9naXRfd2luZG93cyB2b2kg'
'dGhhbSBzbyB0aWVtIikKc3BlYyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscDU0MSIsIHN0'
'cih0ZXApKQpscCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9k'
'dWxlKGxwKQpzaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShscC5fZ2l0X3dpbmRvd3MpCmdoaSgidGhhbV9zb19fZ2l0X3dpbmRv'
'd3MiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKaW5uKCIgIHRoYW0gc28gY3VhIF9naXRfd2luZG93czoiLCBsaXN0KHNpZy5w'
'YXJhbWV0ZXJzKSkKCmRlZiBnb2koKiprdyk6CiAgICAiIiJHb2kgX2dpdF93aW5kb3dzLCBCQVQgc3RkZXJyIGRlIG1vdCBk'
'b25nIGNoYW4gZG9hbiBraG9uZyBnaWV0IGx1b3QgZG8uIiIiCiAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgd2l0aCBjb250'
'ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICByID0gbHAuX2dpdF93aW5kb3dzKCoqa3cpCiAgICByZXR1cm4g'
'ciwgZS5nZXR2YWx1ZSgpCgojIC0tLSBkb2kgY2h1bmcgcmlnOiBwaGFpIHRyYSBsb2kgZHVuZyBtb3QgY2EgdGEgQklFVCBU'
'UlVPQyBkYXAgYW4gLS0tCndpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgIG5nb2FpID0gUGF0'
'aCh0KS8ibmdvYWkiOyBuZ29haS5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0'
'KS8icGYiOyBwZi5ta2RpcigpCiAgICAobmdvYWkvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04'
'IikKICAgIHIxLCBfID0gZ29pKHBhdGg9c3RyKG5nb2FpKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkK'
'ICAgIChjdy8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjIsIF8gPSBnb2kocGF0'
'aD1zdHIoY3cpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQpyaWdfb2sgPSBib29sKHIxKSBhbmQgcjIg'
'aXMgTm9uZQpnaGkoInJpZ19kb2lfY2h1bmciLCByaWdfb2spCmtldCgiUklHIGRvaSBjaHVuZyAoYmlldCB0cnVvYyBkYXAg'
'YW4pIiwgREFUIGlmIHJpZ19vayBlbHNlIEtERCwKICAgIGYibmdvYWktY3dkLT57J05IQU4nIGlmIHIxIGVsc2UgJ05vbmUn'
'fSB8IHRyb25nLWN3ZC0+eydOSEFOJyBpZiByMiBlbHNlICdOb25lJ30iKQppZiBub3QgcmlnX29rOgogICAgaW5uKCIiKTsg'
'aW5uKCJLSE9ORyBETyBEVU9DOiByaWcgc2FpLCBtb2kgY2hvdCBkdW9pIHNlIHZvIG5naGlhLiIpOyBzeXMuZXhpdCgzKQoK'
'IyAtLS0gTU9JIENPTkcgUEhBSSBUVSBDSFVORyBNSU5IIE5PIENPIFRIRSBETyAtLS0KIyBCYWkgaG9jIGRhdCBuaGF0IGN1'
'YSBwYWNrZXQgbmF5OiBkb19uMTAgYmFuIGN1IGNoYW0gREFUIGNobyA5NTgzMTY4NSB0cm9uZyBraGkgdDE3MQojIGN1YSBj'
'aGluaCBiYW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQgdGF0IG1hIE4xMCBzaW5oIHJhIGRlIGJhdC4gTm8gZGVnZW5lcmF0'
'ZSDigJQKIyB0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgbmVuICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIg'
'Y2hvIGN1bmcga2V0IHF1YS4KIyBNb3QgY29uZyBraG9uZyB0aGUgRE8gdGhpIGtob25nIHBoYWkgY29uZywgdmEgbm8gbmd1'
'eSBoaWVtIGhvbiBraG9uZyBjbyBjb25nOiBubwojIHBoYXQgcmEgbW90IGNodSBEQVQuCiMKIyBOZW4gdHJ1b2Mga2hpIERV'
'TkcgbmFtIGNvbmcgbmF5IGRlIHBoYW4gcXV5ZXQsIGJhdCB0dW5nIGNvbmcgZ2lldCBtb3QgZG90IGJpZW4gZGEKIyBiaWV0'
'IHRyb25nLiBDb25nIG5hbyBraG9uZyBnaWV0IGR1b2MgdGhpIGNodSBEQVQgY3VhIG5vIGJpIEhBIHh1b25nIEtIT05HIERP'
'IERVT0M7CiMgVFJVT1QgZ2l1IG5ndXllbiAocXVhbiBzYXQgdHJ1YyB0aWVwLCB2ZC4gZzEgdmFuIG5oYW4gZ2l0LmJhdCku'
'IERvdCBiaWVuIGNoYXkgdHJlbiBCQU4gU0FPIFRBTTsgY2F5IHRoYXQga2hvbmcgYmkKIyBkdW5nIHRvaSAoY3VuZyBreSBs'
'dWF0IG5odSBONykuCkRPVF9CSUVOX1RVX0tJRU0gPSBbCiAgICAoIk44IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAg'
'ICAnaWYgY2hpX2RpbmggYW5kIFBhdGgoY2hpX2RpbmgpLm5hbWUubG93ZXIoKSA9PSAiZ2l0LmV4ZSIgYW5kIGhvcF9sZShj'
'aGlfZGluaCk6JywKICAgICAiaWYgY2hpX2RpbmggYW5kIGhvcF9sZShjaGlfZGluaCk6IiksCiAgICAoIk45IiwgIm9wcy9s'
'ZWFzZV9wdWJsaXNoLnB5IiwKICAgICAiZCA9IGRfcmF3LnN0cmlwKCkuc3RyaXAoJ1wiJykiLCAiZCA9IGRfcmF3LnN0cmlw'
'KCkiKSwKICAgICgiTjEwIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAic2VwID0gb3MucGF0aHNlcCBpZiBwaGFu'
'X2NhY2ggaXMgTm9uZSBlbHNlIHBoYW5fY2FjaCIsICJzZXAgPSBvcy5wYXRoc2VwIiksCiAgICAoIk4xMSIsICJvcHMvbGVh'
'c2VfcHVibGlzaC5weSIsICJpZiBjaGFuX2RvYW4gaXMgbm90IE5vbmU6IiwgImlmIEZhbHNlOiIpLAogICAgKCJOMTIiLCAi'
'b3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSIsCiAgICAgJ2dpdF9wYXRoPSIvL2tob25nLWNvL2dpdCInLCAnZ2l0X3BhdGg9'
'Ii9raG9uZy1jby9naXQiJyksCl0KaW5uKCIiKTsgaW5uKCIgIHR1IGtpZW0gY29uZyDigJQgbW9pIGNvbmcgcGhhaSBnaWV0'
'IGR1b2MgbW90IGRvdCBiaWVuIGRhIGJpZXQ6IikKZ2lldCA9IHt9CmZvciBtYSwgZHVvbmcsIHRpbSwgdGhheSBpbiBET1Rf'
'QklFTl9UVV9LSUVNOgogICAgX3RlbiwgX2hhbSA9IG5leHQoKChhLCBiKSBmb3IgYSwgYiBpbiBQUk9CRSBpZiBhLnN0YXJ0'
'c3dpdGgobWEgKyAiICIpKSwgKE5vbmUsIE5vbmUpKQogICAgaWYgX2hhbSBpcyBOb25lOgogICAgICAgIGdpZXRbbWFdID0g'
'Tm9uZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBraG9uZyB0aW0gdGhheSBwcm9iZSB0ZW4gJ3ttYX0gLi4u'
'JyIpOyBjb250aW51ZQogICAgdHJ5OgogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgX3Q6'
'CiAgICAgICAgICAgIF9jID0gUGF0aChfdCkvImNheSI7IHNodXRpbC5jb3B5dHJlZShnb2MvIm9wcyIsIF9jLyJvcHMiKQog'
'ICAgICAgICAgICBfZiA9IF9jL2R1b25nOyBfbmQgPSBfZi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAg'
'ICAgaWYgX25kLmNvdW50KHRpbSkgIT0gMToKICAgICAgICAgICAgICAgIGdpZXRbbWFdID0gTm9uZQogICAgICAgICAgICAg'
'ICAgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBtYXUgZG90IGJpZW4ga2hvcCB7X25kLmNvdW50KHRpbSl9IGxh'
'biAobW9uZyAxKSIKICAgICAgICAgICAgICAgICAgICBmIiDigJQgbWEgbmd1b24gZGEgZG9pLCBkb3QgYmllbiBuYXkgaGV0'
'IHkgbmdoaWEiKTsgY29udGludWUKICAgICAgICAgICAgX2Yud3JpdGVfdGV4dChfbmQucmVwbGFjZSh0aW0sIHRoYXksIDEp'
'LCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2Nh'
'dGlvbigibHBfZGJfIiArIG1hLCBzdHIoX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgICAgICAgICAgX20gPSBp'
'bXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX20pCiAgICAgICAg'
'ICAgIGRlZiBfZ29pX2RiKCoqa3cpOgogICAgICAgICAgICAgICAgX2UgPSBpby5TdHJpbmdJTygpCiAgICAgICAgICAgICAg'
'ICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKF9lKToKICAgICAgICAgICAgICAgICAgICByZXR1cm4gX20uX2dp'
'dF93aW5kb3dzKCoqa3cpLCBfZS5nZXR2YWx1ZSgpCiAgICAgICAgICAgIF90dCwgX2N0LCBfID0gX2hhbShfZ29pX2RiLCBp'
'bnNwZWN0LnNpZ25hdHVyZShfbS5fZ2l0X3dpbmRvd3MpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgX2MvIm9w'
'cyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgZ2lldFttYV0gPSAoX3R0ID09IFRSVU9UKQogICAgICAgIGlu'
'bihmIiAgICB7bWE6NH0gZG90IGJpZW4gLT4ge190dDoxNH0geydHSUVUIERVT0MnIGlmIF90dCA9PSBUUlVPVCBlbHNlICdT'
'T05HIFNPVCd9IgogICAgICAgICAgICArIChmIiAgICh7X2N0fSkiIGlmIF9jdCBlbHNlICIiKSkKICAgIGV4Y2VwdCBFeGNl'
'cHRpb24gYXMgX2U6CiAgICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IHt0'
'eXBlKF9lKS5fX25hbWVfX306IHtfZX0iKQpnaGkoImNvbmdfZ2lldF9kdW9jX2RvdF9iaWVuIiwgZ2lldCkKCmZvciB0ZW4s'
'ICh0dCwgY3QsIGRsKSBpbiBbKHQsIGYoZ29pLCBzaWcsIHRlcHQpKSBmb3IgdCwgZiBpbiBQUk9CRV06CiAgICBnaGkoInBy'
'b2JlXyIgKyB0ZW4uc3BsaXQoKVswXS5sb3dlcigpLCBkbCkKICAgIGlmIGlzaW5zdGFuY2UoZGwsIGRpY3QpOgogICAgICAg'
'IGZvciBrLCB2IGluIGRsLml0ZW1zKCk6IGlubihmIiAgICB7azozNH06IHt2fSIpCiAgICBtYSA9IHRlbi5zcGxpdCgpWzBd'
'CiAgICBpZiBnaWV0LmdldChtYSkgaXMgbm90IFRydWUgYW5kIHR0ID09IERBVDoKICAgICAgICAjIERBVCB0dSBtb3QgY29u'
'ZyBjaHVhIGNodW5nIG1pbmggZHVvYyBsYSBiaWV0IERPIHRoaSBraG9uZyBkYW5nIHRpbiBob24gS0RELgogICAgICAgIGtl'
'dCh0ZW4sIEtERCwgZiJjb25nIEtIT05HIGdpZXQgZHVvYyBkb3QgYmllbiBjdWEgY2hpbmggbm8gKHtnaWV0LmdldChtYSkh'
'cn0pIgogICAgICAgICAgICAgICAgICAgICAgZiIgLT4gY2h1IERBVCBuYXkga2hvbmcgY28gZ2lhIHRyaSIpCiAgICBlbHNl'
'OgogICAgICAgIGtldCh0ZW4sIHR0LCBjdCkKCiMgLS0tLS0tLS0tLS0tLS0tLSA0LiBONyBkb3QgYmllbiB0cmVuIEJBTiBT'
'QU8gVEFNIC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlu'
'bigiNC4gTjcg4oCUIGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gKGNheSB0aGF0IEtIT05HIGJpIGR1bmcgdG9pKSIpCiAg'
'ICB0cnVvYyA9IHRlcC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTikKICAgIGdoaSgibjdfdHJ1'
'b2MiLCB0cnVvYyk7IGlubihmIiAgc28gZG9uZyBraG9wIHtNQVVfV0lOIXJ9OiBUUlVPQyA9IHt0cnVvY30gW21vbmcgMV0i'
'KQogICAgaWYgdHJ1b2MgIT0gMToKICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsIGYibWF1'
'IHh1YXQgaGllbiB7dHJ1b2N9IGxhbiwga2hvbmcgcGhhaSAxIikKICAgIGVsc2U6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5U'
'ZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0bXA6CiAgICAgICAgICAgIHNhbyA9IFBhdGgodG1wKS8iY2F5IgogICAgICAgICAg'
'ICBzaHV0aWwuY29weXRyZWUoZ29jLCBzYW8sIGlnbm9yZT1zaHV0aWwuaWdub3JlX3BhdHRlcm5zKCIuZ2l0IiwgIl9fcHlj'
'YWNoZV9fIiwgIioucHljIikpCiAgICAgICAgICAgIGYyID0gc2FvLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IgogICAgICAg'
'ICAgICBmMi53cml0ZV90ZXh0KGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5yZXBsYWNlKE1BVV9XSU4sICJpZiBG'
'YWxzZToiKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgc2F1ID0gZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYt'
'OCIpLmNvdW50KE1BVV9XSU4pOyBnaGkoIm43X3NhdSIsIHNhdSkKICAgICAgICAgICAgaW5uKGYiICBTQVUgKGRhIGRvdCBi'
'aWVuKSA9IHtzYXV9IFttb25nIDBdIikKICAgICAgICAgICAgaWYgc2F1ICE9IDA6CiAgICAgICAgICAgICAgICBrZXQoIk43'
'IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsICJkb3QgYmllbiBLSE9ORyBhcCBkdW9jIikKICAgICAgICAgICAgZWxz'
'ZToKICAgICAgICAgICAgICAgIHJjX20sIG91dF9tID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgc2Fv'
'KQogICAgICAgICAgICAgICAgbTE2NSA9IG1hdV9jYShvdXRfbSwgInQxNjUiKTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20p'
'CiAgICAgICAgICAgICAgICB0ZW4xNjUgPSBuZXh0KCh0IGZvciB0IGluIGRtIGlmIHQuc3RhcnRzd2l0aCgidDE2NSIpKSwg'
'Tm9uZSkKICAgICAgICAgICAgICAgIGx5ID0gKGRtLmdldCh0ZW4xNjUpIG9yICIiKQogICAgICAgICAgICAgICAgZ2hpKCJu'
'N190MTY1IiwgbTE2NSk7IGdoaSgibjdfbHlfZG8iLCBseVs6MjAwXSkKICAgICAgICAgICAgICAgIGlubihmIiAgdDE2NSBz'
'YXUgZG90IGJpZW46IHttMTY1fSB8IHtseVs6MTEwXX0iKQogICAgICAgICAgICAgICAgZHVuZ19seV9kbyA9ICJQQVRIIHQi'
'IGluIGx5IG9yICIvdXNyL2JpbiIgaW4gbHkKICAgICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93'
'cyIsIERBVCBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKSBlbHNlCiAgICAgICAgICAgICAgICAgICAgKFRSVU9U'
'IGlmIG0xNjUgPT0gIkRPIiBlbHNlIEtERCksCiAgICAgICAgICAgICAgICAgICAgImdpZXQgZHVuZyBseSBkbyIgaWYgKG0x'
'NjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykKICAgICAgICAgICAgICAgICAgICBlbHNlICgiRE8gbmh1bmcgS0hPTkcgZHVu'
'ZyBseSBkbyAtPiB0aW4gZHVuZyBnaWEiIGlmIG0xNjUgPT0gIkRPIiBlbHNlICJraG9uZyBkb2MgZHVvYyB0MTY1IikpCgoj'
'IC0tLS0tLS0tLS0tLS0tLS0gS0VUIExVQU4gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIj0iICogNzgpCmlubihm'
'IlRIRSBIRSBETyBEVU9DOiB7dGhlX2hlfSAgIEhFQUQ9e2hlYWRbOjEyXX0iKQojIEtob2kgZGFuIGNobyByZXZpZXdlciBi'
'YXQgZGF1IG8gZG9uZyB0cmVuLCBuZW4gQ0hFIERPIHBoYWkgbmFtIE5HQVkgZHVvaSBubzoga2hvbmcgY28gZG9uZyBuYXkK'
'IyB0aGkgbW90IGx1b3QgLS1jaGktcHJvYmUgaW4gIkRBVCA3IHwgVFJVT1QgMCB8IEtIT05HIERPIERVT0MgMCIgcmM9MCBt'
'YSBraG9uZyBub2kgbGEgY2h1YSBjaGF5IGJvIHRlc3QuCmdoaSgiY2hlX2RvIiwgImNoaS1wcm9iZSIgaWYgQ0hJX1BST0JF'
'IGVsc2UgImRheS1kdSIpCmlmIENISV9QUk9CRToKICAgIGlubigiLS1jaGktcHJvYmU6IENISSBkbyBtdWMgMCwgMSwgMy4g'
'Qm8gdGVzdCwgTjEtTjQsIHQxMzYsIE43IEtIT05HIGNoYXkgLSBkYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1'
'LiIpCmlmIHRoZV9oZSA9PSAiZzEiOgogICAgaW5uKCJMVVUgWTogZGF5IGxhIE5FTiBETyAoZzEpLCBLSE9ORyBwaGFpIG5n'
'aGllbSB0aHUgZzIuIENhYyBjaG90IE44LU4xMiBkdW9pIGRheSIpCiAgICBpbm4oIiAgICAgICBUUlVPVCBsYSBEVU5HIE5I'
'VSBNT05HIOKAlCBjaHVuZyBsYSBuaHVuZyBsbyBnMiBzaW5oIHJhIGRlIHbDoS4iKQppbm4oIi0iICogNzgpCmZvciB0ZW4s'
'IHR0LCBjdCBpbiBjaG90OgogICAgaW5uKGYiICB7dHQ6MTR9IHt0ZW59IiArIChmIiAgIHtjdH0iIGlmIGN0IGVsc2UgIiIp'
'KQpuX2tkZCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCm5fdHJ1b3QgPSBzdW0oMSBmb3IgXywg'
'dCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCmlubigiLSIgKiA3OCkKaW5uKGYiICBEQVQge3N1bSgxIGZvciBfLHQsXyBp'
'biBjaG90IGlmIHQ9PURBVCl9IHwgVFJVT1Qge25fdHJ1b3R9IHwgS0hPTkcgRE8gRFVPQyB7bl9rZGR9IikKaW5uKGYiICBU'
'b25nIGNhIGRvOiB7c28uZ2V0KCdzb19jYV9kbycpfSB8IGRhbmggc2FjaCBkYXkgZHU6IHsnQ08nIGlmIHNvLmdldCgnbGll'
'dF9rZV9kYXlfZHUnKSBlbHNlICdLSE9ORyBETyBEVU9DJ30iKQppbm4oZiIgIEFkbWluaXN0cmF0b3I6IHtzby5nZXQoJ3F1'
'eWVuX2FkbWluJyl9IHwgc3ltbGluazoge3NvLmdldCgnc3ltbGlua19kdW9jJyl9IikKaW5uKCIiKTsgaW5uKCItLS0gREFO'
'IE5HVVlFTiBLSE9JIEpTT04gTkFZIFZFIENITyBSRVZJRVdFUiAtLS0iKQpnaGkoImNob3QiLCBbeyJ0ZW4iOiBhLCAidHJh'
'bmdfdGhhaSI6IGIsICJjaGlfdGlldCI6IGN9IGZvciBhLCBiLCBjIGluIGNob3RdKQppbm4oanNvbi5kdW1wcyhzbywgZW5z'
'dXJlX2FzY2lpPUZhbHNlLCBpbmRlbnQ9MSwgZGVmYXVsdD1zdHIpKQojIHJjOiAwID0gbW9pIGNob3QgREFUIHwgMSA9IGNv'
'IGNob3QgVFJVT1QgfCAzID0gY28gY2hvdCBLSE9ORyBETyBEVU9DICh1dSB0aWVuIGJhbyBkb25nKQpzeXMuZXhpdCgzIGlm'
'IG5fa2RkIGVsc2UgKDEgaWYgbl90cnVvdCBlbHNlIDApKQo='
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
