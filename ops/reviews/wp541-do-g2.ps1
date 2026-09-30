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
$ShaBoDo    = '7868d9aadd37701396ff67a06ca9148ddb61d42dfd1a1314cb71346337f8f9b2'      # SHA-256 cua bo do Python nhung ben duoi

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
'YzJkMmFiYmRkYmI2ZiIKQkFOX0JPX0RPID0gIjIwMjYtMDktMzBqIiAgICAgICAgICAgICAgIyBkb2kgTU9JIGtoaSBzdWEg',
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
'LCBraG9uZyBwaGFpIGRhIGRvbmcuCiMgQ2F1IGhpbmggc2hlbGxjaGVjayBDVUEgTkdVT0kgRE8gbG90IHZhbyBibyB0ZXN0',
'IHkgbmh1IGdpdDogdDEzNyBnb2kgc2hlbGxjaGVjayBUSEFORywgdDMzL3QxMzcgZ29pIGFjdGlvbmxpbnQgLT4gc2hlbGxj',
'aGVjaywKIyBjYSBoYWkgZG9jIFNIRUxMQ0hFQ0tfT1BUUywgdmEgdDEzNyBkb2Mgfi8uc2hlbGxjaGVja3JjIChYREdfQ09O',
'RklHX0hPTUUgdGFtIEtIT05HIGNoZSBkdW9jOyBjaG8gdGVwIHJjIHRyZW4gV2luZG93czogS0hPTkcgRE8gRFVPQykuCiMg',
'RG8gdHJlbiAyMDI2LTA5LTMwaCwgMGVhOTVkZTogU0hFTExDSEVDS19PUFRTPS0tZW5hYmxlPWFsbCA9PiB0MzMgKyB0MTM3',
'IERPOyB+Ly5zaGVsbGNoZWNrcmMgYGVuYWJsZT1hbGxgID0+IHQxMzcgRE8g4oCUIGNhICJsYSIKIyA9PiBUUlVPVCBjaG8g',
'dW5nIHZpZW4gc2FjaC4gQ0kga2hvbmcgY28gY2EgaGFpLiBTSEVMTENIRUNLX09QVFM9LS1ub3JjIGRlIGxlbiBiaWVuIGN1',
'YSBuZ3VvaSBkbyBWQSB0YXQgbW9pIHRlcCByYyAoc2hlbGxjaGVjawojIHBoYWkgTkhBTiAtLW5vcmMg4oCUIG11YyAwIGhv',
'aSB0cnVvYykuIEJBU0hfRU5WIChrZSBjYSBgc2V0IC1ldW8gcGlwZWZhaWxgKSBkbzogMTY2LzE2Niwga2hvbmcgbG90Lgpf',
'R0lUX0dMT0JBTF9DSSA9ICJbaW5pdF1cblx0ZGVmYXVsdEJyYW5jaCA9IG1hc3RlclxuW2NvcmVdXG5cdGF1dG9jcmxmID0g',
'ZmFsc2Vcblx0ZW9sID0gbGZcblx0YWJicmV2ID0gN1xuIgpkZWYgY2hheShhcmd2LCBjd2QsIHBodXQ9NjApOgogICAgZmQs',
'IGdjID0gdGVtcGZpbGUubWtzdGVtcChwcmVmaXg9IndwNTQxLWdpdGNvbmZpZy1jaS0iLCBzdWZmaXg9Ii5pbmkiKQogICAg',
'eGRnID0gTm9uZQogICAgdHJ5OgogICAgICAgIHhkZyA9IHRlbXBmaWxlLm1rZHRlbXAocHJlZml4PSJ3cDU0MS14ZGctIikK',
'ICAgICAgICB3aXRoIG9zLmZkb3BlbihmZCwgInciLCBlbmNvZGluZz0iYXNjaWkiLCBuZXdsaW5lPSJcbiIpIGFzIGY6IGYu',
'd3JpdGUoX0dJVF9HTE9CQUxfQ0kpCiAgICAgICAgbXQgPSB7azogdiBmb3IgaywgdiBpbiBvcy5lbnZpcm9uLml0ZW1zKCkK',
'ICAgICAgICAgICAgICBpZiBub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIkdJVF8iKSBhbmQgKG5vdCBrLnVwcGVyKCkuc3Rh',
'cnRzd2l0aCgiUFlUSE9OIikgb3Igay51cHBlcigpIGluIF9QWV9HSVUpfQogICAgICAgIG10LnVwZGF0ZShQWVRIT05VVEY4',
'PSIxIiwgUFlUSE9OSU9FTkNPRElORz0idXRmLTgiLCBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0iMSIsIFBZVEhPTlVOQlVG',
'RkVSRUQ9IjEiLAogICAgICAgICAgICAgICAgICBHSVRfQ09ORklHX0dMT0JBTD1nYywgWERHX0NPTkZJR19IT01FPXhkZywg',
'U0hFTExDSEVDS19PUFRTPSItLW5vcmMiKQogICAgICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbc3lzLmV4ZWN1dGFibGVdICsg',
'YXJndiwgY3dkPXN0cihjd2QpLCBjYXB0dXJlX291dHB1dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICB0ZXh0',
'PVRydWUsIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCwgZW52PW10KQogICAg',
'ZmluYWxseToKICAgICAgICB0cnk6IG9zLnJlbW92ZShnYykKICAgICAgICBleGNlcHQgT1NFcnJvcjogcGFzcwogICAgICAg',
'IGlmIHhkZzogc2h1dGlsLnJtdHJlZSh4ZGcsIGlnbm9yZV9lcnJvcnM9VHJ1ZSkKICAgIHJldHVybiBwLnJldHVybmNvZGUs',
'IChwLnN0ZG91dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1X2NhKG91dCwgdCk6CiAgICBtID0gcmUuc2Vh',
'cmNoKHIiKD9tKV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSBbMC05Ll0rcyAoXHcrKVxzKiQiLCBvdXQpCiAgICBy',
'ZXR1cm4gbS5ncm91cCgyKSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdpdChnb2MsICphLCBwaHV0PTUpOgogICAgcCA9IHN1YnBy',
'b2Nlc3MucnVuKFsiZ2l0IiwgIi1DIiwgc3RyKGdvYyksICphXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLAog',
'ICAgICAgICAgICAgICAgICAgICAgIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2',
'MCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikuc3RyaXAoKSwgKHAuc3RkZXJyIG9yICIiKS5z',
'dHJpcCgpCgoKIyA9PT09PT09PT09PT09PT09PSBOQU0gUFJPQkUsIHZpZXQgdGhhbmggSEFNIFRIVUFOIGRlIFRVIEtJRU0g',
'ZHVvYyA9PT09PT09PT09PT09PT09PQojIE1vaSBoYW0gdHJhICh0cmFuZ190aGFpLCBjaGlfdGlldCwgZHVfbGlldSkuIEtI',
'T05HIGluLCBLSE9ORyB0aG9hdCDigJQgbmhvIHZheSBjaHVuZwojIGNoYXkgZHVvYyB0cmVuIG5lbiBCQVQgS1ksIHZhIGAt',
'LXR1LWtpZW0tcHJvYmVgIGdvaSB0aGFuZyBjaHVuZyBkZSBraWVtIGNoaW5oIGJvIGRvLgoKZGVmIF9zYW4odCk6CiAgICBk',
'ID0gUGF0aCh0KS8iZCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkv',
'InBmIjsgcGYubWtkaXIoKQogICAgcmV0dXJuIGQsIGN3LCBwZgoKZGVmIGRvX244KGdvaSwgc2lnLCB0ZXB0KToKICAgICIi',
'IkJ1b2MgMSAoQ09OR19DVV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0LmV4ZS4gRG9pIGNodW5nIGR1b25nOiBnaXQuZXhlIFZB',
'TiBwaGFpIG5oYW4uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6',
'CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIGZvciB0ZW4gaW4gKCJnaXQuZXhlIiwgImdpdC5iYXQiLCAi',
'Z2l0LmNtZCIsICJnaXQucHkiLCAia2hvbmctcGhhaS1naXQudHh0Iik6CiAgICAgICAgICAgIGYgPSBkL3RlbjsgZi53cml0',
'ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyA9IGdvaShjb25nX2N1X2dpdD1zdHIoZiks',
'IHBhdGg9IiIsIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIGtxW2YiQ09OR19DVV9H',
'SVQ9e3Rlbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIlRVIENIT0kiCiAgICBsb3QgPSBbayBmb3IgaywgdiBpbiBrcS5pdGVt',
'cygpIGlmIHYgPT0gIk5IQU4iIGFuZCBub3Qgay5lbmRzd2l0aCgiZ2l0LmV4ZSIpXQogICAgaWYga3EuZ2V0KCJDT05HX0NV',
'X0dJVD1naXQuZXhlIikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogZ2l0',
'LmV4ZSBob3AgbGUgbWEgYmkgdHUgY2hvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgbG90IGVsc2UgVFJVT1QpLCAo',
'IiIgaWYgbm90IGxvdCBlbHNlIGYiY29uIG5oYW46IHtsb3R9IiksIGtxCgpkZWYgZG9fbjkoZ29pLCBzaWcsIHRlcHQpOgog',
'ICAgIiIiTXVjIFBBVEggYm9jIG5oYXkga2VwIHBoYWkgTkhBTjsgbXVjIHJvbmcgLyB0b2FuIGtob2FuZyB0cmFuZyBwaGFp',
'IGJvIHF1YSwga2hvbmcgbmVtLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3Rvcnko',
'KSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cu',
'bWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQo',
'IngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGZvciBuaGFuLCBtdWMgaW4gKCgia2hvbmcgbmhheSIsIHN0cihkKSks',
'ICgiY28gbmhheSBrZXAiLCBmJyJ7ZH0iJyksCiAgICAgICAgICAgICAgICAgICAgICAgICAgKCJyb25nIiwgIiIpLCAoImNo',
'aSBraG9hbmcgdHJhbmciLCAiICAgIikpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICByLCBfID0gZ29pKHBh',
'dGg9bXVjLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtu',
'aGFufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAg',
'ICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gZiJORU0ge3R5cGUoZSkuX19uYW1lX199IgogICAgaWYga3EuZ2V0',
'KCJQQVRIIGtob25nIG5oYXkiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25n',
'OiBtdWMgUEFUSCB0aHVvbmcgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgb2sgPSAoa3EuZ2V0KCJQQVRIIGNv',
'IG5oYXkga2VwIikgPT0gIk5IQU4iCiAgICAgICAgICBhbmQga3EuZ2V0KCJQQVRIIHJvbmciKSA9PSAiTm9uZSIgYW5kIGtx',
'LmdldCgiUEFUSCBjaGkga2hvYW5nIHRyYW5nIikgPT0gIk5vbmUiKQogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVP',
'VCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKIyBEYXUgcGhhbiBjYWNoIGR1bmcgREUgVEhVLiBQaGFpIEtI',
'QUMgb3MucGF0aHNlcCB0cmVuIENBIEhBSSBuZW4gKCc7JyBXaW5kb3dzLCAnOicgUE9TSVgpCiMgdGhpIGhhaSBnaWEgdGh1',
'eWV0ICJ0YWNoIHRoZW8gZGF1IGR1b2MgdHJ1eWVuIiB2YSAidGFjaCB0aGVvIG9zLnBhdGhzZXAiIG1vaSByb2kgcmEgbmhh',
'dS4KVEhVX04xMCA9ICJ8IgoKZGVmIGRvX24xMChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW0gcGhhaSB0YWNoIFBBVEgg',
'dGhlbyBkYXUgcGhhbiBjYWNoIERVT0MgVFJVWUVOLCBraG9uZyB0aGVvIG9zLnBhdGhzZXAgY3VhIG5lbi4KCiAgICBCYW4g',
'Y3UgZG8gIm1vdCBkYXUgJzsnIHRyb25nIFRFTiB0aHUgbXVjIiB2YSBkYXQgREFUIHRyZW4gV2luZG93cyBkdSBoYW0gc2Fp',
'LiBObwogICAgZGVnZW5lcmF0ZTogdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnLCBuZW4gJ0M6L2E7YicgdGhh',
'dCBzdSBDTyBOR0hJQSBsYSBoYWkKICAgIG11YyDigJQgInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gcmEgY3VuZyBr',
'ZXQgcXVhLCBwaGVwIGRvIGtob25nIHRoZSBkbyBuYW8uIE5vCiAgICBkYSBjaGFtIERBVCBjaG8gOTU4MzE2ODUgdHJvbmcg',
'a2hpIHQxNzEgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQgYXkuCiAgICBNb3QgY29uZyBraG9u',
'ZyB0aGUgZG8gdGhpIGtob25nIHBoYWkgY29uZy4KICAgICIiIgogICAgdGVuX3NlcCA9IG5leHQoKGsgZm9yIGsgaW4gKCJw',
'aGFuX2NhY2giLCAiZGF1X3BoYW5fY2FjaCIsICJzZXAiKSBpZiBrIGluIHNpZy5wYXJhbWV0ZXJzKSwgTm9uZSkKICAgIGlm',
'IHRlbl9zZXAgaXMgTm9uZToKICAgICAgICAjIEtob25nIGNvIHRoYW0gc28gdGhpIHRyZW4gV2luZG93cyBLSE9ORyBjb24g',
'ZHVvbmcgbmFvIHRhY2ggaGFpIGdpYSB0aHV5ZXQuCiAgICAgICAgaWYgb3MucGF0aHNlcCA9PSAiOyI6CiAgICAgICAgICAg',
'IHJldHVybiAoS0RELCAidHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIHZhIGhhbSBraG9uZyBuaGFuIHRoYW0g',
'c28gZGF1IHBoYW4gY2FjaCAiCiAgICAgICAgICAgICAgICAgICAgICAgICAiLT4ga2hvbmcgdGFjaCBkdW9jIGhhaSBnaWEg',
'dGh1eWV0IiwKICAgICAgICAgICAgICAgICAgICB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiBO',
'b25lfSkKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgICAgIGxhID0g',
'UGF0aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKQogICAgICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgICAg',
'IChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8gID0gZ29p',
'KHBhdGg9c3RyKGxhKSArIG9zLnBhdGhzZXAgKyBzdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykp',
'CiAgICAgICAgICAgIHIwLCBfID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cp',
'KQogICAgICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZSwKICAgICAgICAg',
'ICAgICAiY28gbXVjIGNodWEgJzsnIjogIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIsCiAgICAgICAgICAgICAgImRvaSBjaHVu',
'ZyBkdW9uZyAoa2hvbmcgY28gJzsnKSI6ICJOSEFOIiBpZiByMCBlbHNlICJOb25lIn0KICAgICAgICBpZiBub3QgcjA6CiAg',
'ICAgICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZyIsIGtxCiAgICAgICAgcmV0dXJuIChEQVQgaWYg',
'ciBlbHNlIFRSVU9UKSwgKCIiIGlmIHIgZWxzZSAibXVjIGdpdC5leGUgaG9wIGxlIGJpIE1BVCIpLCBrcQoKICAgIHdpdGgg',
'dGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1r',
'ZGlyKCkgICAgICAgICAgIyAnOycgbmFtIHRyb25nIFRFTiwga2hvbmcgcGhhaSBkYXUgcGhhbiBjYWNoCiAgICAgICAgZCwg',
'Y3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIp',
'CiAgICAgICAgbm9pID0gc3RyKGxhKSArIFRIVV9OMTAgKyBzdHIoZCkKICAgICAgICBrdyA9IGRpY3QocHJvZ3JhbV9maWxl',
'cz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICByX2NoaW5oLCBfID0gZ29pKHBhdGg9bm9pLCAgICAgICoqe3Rlbl9z',
'ZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyB0YWNoIGR1bmcgIC0+IE5IQU4KICAgICAgICByX2R1b25nLCBfID0gZ29pKHBh',
'dGg9c3RyKGQpLCAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyBkb2kgY2h1bmcgZHVvbmcKICAgICAgICBy',
'X3BoYW5iaWV0LCBfID0gZ29pKHBhdGg9bm9pLCAgICoqe3Rlbl9zZXA6IG9zLnBhdGhzZXB9LCAqKmt3KSAgIyB0YWNoIHRo',
'ZW8gb3MucGF0aHNlcCAtPiBtYXQKICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjog',
'dGVuX3NlcCwgImRhdSB0aHUiOiBUSFVfTjEwLAogICAgICAgICAgZiJub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9',
'PXtUSFVfTjEwIXJ9IjogICAgICAgIk5IQU4iIGlmIHJfY2hpbmggZWxzZSAiTm9uZSIsCiAgICAgICAgICBmImRvaSBjaHVu',
'ZyBkdW9uZyAobW90IG11Yywge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9KSI6ICAiTkhBTiIgaWYgcl9kdW9uZyBlbHNlICJOb25l',
'IiwKICAgICAgICAgIGYicGhhbiBiaWV0OiBub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtvcy5wYXRoc2VwIXJ9',
'IjogIk5IQU4iIGlmIHJfcGhhbmJpZXQgZWxzZSAiTm9uZSJ9CiAgICBpZiBub3Qgcl9kdW9uZzoKICAgICAgICByZXR1cm4g',
'S0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG1vdCBtdWMgaG9wIGxlIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EK',
'ICAgICMgQ29uZyBwaGFpIENPIFRIRSBkby4gTmV1IGNhIGhhaSBkYXUgcGhhbiBjYWNoIGRldSByYSBOSEFOIHRoaSBwaGVw',
'IGRvIGtob25nIHBoYW4KICAgICMgYmlldCBkdW9jIGdpIOKAlCBkdW5nIGJhbyBEQVQsIGJhbyB0aGFuZyBsYSBraG9uZyBk',
'byBkdW9jLgogICAgaWYgcl9waGFuYmlldDoKICAgICAgICByZXR1cm4gKEtERCwgZiJwaGVwIGRvIEtIT05HIHBoYW4gYmll',
'dCBkdW9jOiBub2kgYmFuZyB7VEhVX04xMCFyfSBtYSB0YWNoIHRoZW8gIgogICAgICAgICAgICAgICAgICAgICBmIntvcy5w',
'YXRoc2VwIXJ9IFZBTiB0aW0gcmEgZ2l0LmV4ZSIsIGtxKQogICAgcmV0dXJuICgoREFULCAiIiwga3EpIGlmIHJfY2hpbmgg',
'ZWxzZQogICAgICAgICAgICAoVFJVT1QsIGYidGFjaCB0aGVvIG9zLnBhdGhzZXAgdGhheSB2aSB0aGVvIHt0ZW5fc2VwfSBk',
'dW9jIHRydXllbiIsIGtxKSkKCgpkZWYgZG9fbjExKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIlRydXllbiBjaGFuX2RvYW4g',
'PT4gdGh1IGR1b2MgdGhvbmcgYmFvIFZBIHN0ZGVyciBJTS4gS2hvbmcgdHJ1eWVuID0+IHN0ZGVyciBWQU4gY28uIiIiCiAg',
'ICBpZiAiY2hhbl9kb2FuIiBub3QgaW4gc2lnLnBhcmFtZXRlcnM6CiAgICAgICAgcmV0dXJuIEtERCwgIl9naXRfd2luZG93',
'cyBraG9uZyBuaGFuIHRoYW0gc28gY2hhbl9kb2FuIiwgeyJ0aGFtIHNvIjogbGlzdChzaWcucGFyYW1ldGVycyl9CiAgICB3',
'aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAg',
'ICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgY2QgPSBbXQogICAg',
'ICAgIF8sIGVfY28gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdyksIGNoYW5f',
'ZG9hbj1jZCkKICAgICAgICBfLCBlX2toID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1z',
'dHIoY3cpKQogICAga3EgPSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAobXVjKSI6IGxlbihjZCksCiAgICAgICAgICAic3RkZXJy',
'IGtoaSBDTyBjaGFuX2RvYW4gKGJ5dGUpIjogbGVuKGVfY28uZW5jb2RlKCkpLAogICAgICAgICAgInN0ZGVyciBraGkgS0hP',
'TkcgdHJ1eWVuIChieXRlKSI6IGxlbihlX2toLmVuY29kZSgpKX0KICAgIGlmIGxlbihjZCkgPT0gMCBhbmQgbGVuKGVfa2gu',
'ZW5jb2RlKCkpID09IDA6CiAgICAgICAgcmV0dXJuIEtERCwgIm5oYW5oICVQcm9ncmFtRmlsZXMlIGtob25nIHBoYW4gZ2lh',
'aSBLSE9ORyBiYXkgcmEgY2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRvIGR1b2MiLCBrcQogICAgb2sgPSBsZW4oY2QpID4gMCBh',
'bmQgbGVuKGVfY28uZW5jb2RlKCkpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA+IDAKICAgIHJldHVybiAoREFUIGlm',
'IG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCmRlZiBkb19uMTIoZ29pLCBzaWcsIHRl',
'cHQpOgogICAgIiIiSGFuZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9uZyBmaXh0dXJlIHBoYWkgdHV5ZXQgZG9pIHRyZW4gQ0Eg',
'SEFJIG5lbi4iIiIKICAgIG5kID0gdGVwdC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIikK',
'ICAgIGhhbmcgPSBzb3J0ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRfcGF0aFxzKj1ccyoiKFteIl0rKSInLCBuZCkpKQogICAg',
'eGF1ID0gW2ggZm9yIGggaW4gaGFuZyBpZiBub3QgKFB1cmVQb3NpeFBhdGgoaCkuaXNfYWJzb2x1dGUoKSBhbmQgUHVyZVdp',
'bmRvd3NQYXRoKGgpLmlzX2Fic29sdXRlKCkpXQogICAga3EgPSB7ImhhbmcgZ2l0X3BhdGggdGltIHRoYXkiOiBoYW5nLCAi',
'Y2hpIHR1eWV0IGRvaSBNT1QgbmVuIjogeGF1fQogICAgaWYgbm90IGhhbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImtob25n',
'IHRpbSB0aGF5IGhhbmcgZ2l0X3BhdGggbmFvIHRyb25nIGZpeHR1cmUgLT4gbWF1IGRvYyBjbyB0aGUgZGEgZG9pIiwga3EK',
'ICAgIHJldHVybiAoREFUIGlmIG5vdCB4YXUgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgeGF1IGVsc2UgZiJjaGktbW90LW5l',
'bjoge3hhdX0iKSwga3EKClBST0JFID0gWygiTjggYnVvYyAxIGNoaSBuaGFuIGdpdC5leGUiLCBkb19uOCksCiAgICAgICAg',
'ICgiTjkgYm9jIG5oYXkga2VwIG8gbXVjIFBBVEgiLCBkb19uOSksCiAgICAgICAgICgiTjEwIGRhdSAnOycgdHJvbmcgdGVu',
'IHRodSBtdWMiLCBkb19uMTApLAogICAgICAgICAoIk4xMSBjaGFuIGRvYW4gZG9pIGtlbmgiLCBkb19uMTEpLAogICAgICAg',
'ICAoIk4xMiBoYW5nIHNlbnRpbmVsIHR1eWV0IGRvaSBDQSBIQUkgbmVuIiwgZG9fbjEyKV0KCiMgLS0tIGNoZSBkbyBUVSBL',
'SUVNOiBjaGF5IG5hbSBwcm9iZSB0cmVuIG1vdCBjYXkgYmF0IGt5LCBuZW4gYmF0IGt5IC0tLQppZiAiLS10dS1raWVtLXBy',
'b2JlIiBpbiBzeXMuYXJndjoKICAgIF9nID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS10dS1raWVtLXByb2Jl',
'IikgKyAxXSkucmVzb2x2ZSgpCiAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBf',
'dGsiLCBzdHIoX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgIF9scCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9m',
'cm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShfbHApCiAgICBfc2lnID0gaW5zcGVjdC5zaWduYXR1cmUo',
'X2xwLl9naXRfd2luZG93cykKICAgIGRlZiBfZ29pKCoqa3cpOgogICAgICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICAgICAg',
'd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICAgICAgcmV0dXJuIF9scC5fZ2l0X3dpbmRvd3Mo',
'KiprdyksIGUuZ2V0dmFsdWUoKQogICAgcHJpbnQoZiJUVSBLSUVNIFBST0JFIHRyZW4ge19nfSAgKG5lbiB7c3lzLnBsYXRm',
'b3JtfSkiKQogICAgZm9yIF90ZW4sIF9mIGluIFBST0JFOgogICAgICAgIF90dCwgX2N0LCBfZGwgPSBfZihfZ29pLCBfc2ln',
'LCBfZy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBwcmludChmIiAgW3tfdHQ6MTR9XSB7X3Rlbn0i',
'ICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgICAgICBmb3IgX2ssIF92IGluIChfZGwgb3Ige30pLml0ZW1z',
'KCk6IHByaW50KGYiICAgICAgICB7X2s6MzR9OiB7X3Z9IikKICAgIHN5cy5leGl0KDApCgojIC0tLSBjaGUgZG8gS0lFTSBE',
'T05HIEJPOiB0ZXAgLnB5IG5heSBwaGFpIFRSVU5HIFRVTkcgQllURSB2b2kgYmFuIG5odW5nIHRyb25nIHBzMSAtLS0KIyBL',
'aG9uZyBjb25nIG5hbyBidW9jIGhhaSBiYW4gc2FvIGtob3A6IGRvIGR1b2MsIG5vaSB0cmFuIDIvNDAwIC0+IDk5Lzk5OTk5',
'IENISSB0cm9uZyAucHkKIyB0aGkgY2lfZGFuZ19reSBsYW4gdDI2L3QyNyB2YW4geGFuaCwgY29uIGNob3QgU0hBIGN1YSBw',
'czEgY2hpIHNvIGJhbiBuaHVuZyB2b2kgaGFuZyBzbwojIGN1YSBDSElOSCBuby4gQ2hheTogcHl0aG9uIHdwNTQxLWRvLWcy',
'LXdpbmRvd3MucHkgLS1raWVtLWRvbmctYm8gd3A1NDEtZG8tZzIucHMxICAocmMgMHwzKQppZiAiLS1raWVtLWRvbmctYm8i',
'IGluIHN5cy5hcmd2OgogICAgaW1wb3J0IGJhc2U2NAogICAgX3BzID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgi',
'LS1raWVtLWRvbmctYm8iKSArIDFdKS5yZWFkX3RleHQoZW5jb2Rpbmc9ImFzY2lpIikKICAgIF9tID0gcmUuc2VhcmNoKHIi',
'KD9tcyleXCRCNjQgPSBAXCgoLio/KV5cKSIsIF9wcykKICAgIF9rID0gcmUuc2VhcmNoKHIiKD9tKV5cJFNoYUJvRG9ccyo9',
'XHMqJyhbMC05YS1mXXs2NH0pJyIsIF9wcykKICAgIF9uaHVuZyA9IGJhc2U2NC5iNjRkZWNvZGUoIiIuam9pbihyZS5maW5k',
'YWxsKHIiJyhbQS1aYS16MC05Ky89XSopJyIsIF9tLmdyb3VwKDEpKSkpIGlmIF9tIGVsc2UgYiIiCiAgICBfdG9pID0gUGF0',
'aChfX2ZpbGVfXykucmVhZF9ieXRlcygpCiAgICBfb2sgPSBib29sKF9tIGFuZCBfaykgYW5kIF9uaHVuZyA9PSBfdG9pIGFu',
'ZCBoYXNobGliLnNoYTI1NihfdG9pKS5oZXhkaWdlc3QoKSA9PSBfay5ncm91cCgxKQogICAgaW5uKGYiS0lFTSBET05HIEJP',
'OiB7REFUIGlmIF9vayBlbHNlIEtERH0gIChuaHVuZyB7bGVuKF9uaHVuZyl9IGJ5dGUsIHRlcCB7bGVuKF90b2kpfSBieXRl',
'KSIpCiAgICBzeXMuZXhpdCgwIGlmIF9vayBlbHNlIDMpCgppbm4oIj0iICogNzgpOyBpbm4oIldQNTQxIGcyIC0gcGhlcCBk',
'byB0cmVuIFdpbmRvd3MgdGhhdCAoc3BlYyByMzogTjEtTjQsIE44LU4xMiwgTjcsIGtpY2ggdGh1b2MpIik7IGlubigiPSIg',
'KiA3OCkKCiMgLS0tLS0tLS0tLS0tLS0tLSB0dSBraWVtIGJvIGRvYyAtLS0tLS0tLS0tLS0tLS0tCl9kLCBfZywgX3QgPSBk',
'b2NfZG8oX01BVSkKX29rID0gKGxlbihfZCkgPT0gMiBhbmQgYW55KHguc3RhcnRzd2l0aCgidDAyYiIpIGZvciB4IGluIF9k',
'KQogICAgICAgYW5kIG5vdCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMxIikgZm9yIHggaW4gX2QpIGFuZCBfdCkKaW5uKCJUdSBr',
'aWVtIGJvIGRvYyBsb2c6IiwgREFUIGlmIF9vayBlbHNlIFRSVU9UKQppZiBub3QgX29rOgogICAgaW5uKCIiKTsgaW5uKCJL',
'SE9ORyBETyBEVU9DOiBibyBkb2MgbG9nIGN1YSBjaGluaCBzY3JpcHQgbmF5IHNhaSAtPiBraG9uZyBkbyBnaSBjYS4iKTsg',
'c3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4gZG8gLS0tLS0tLS0tLS0tLS0tLQpnb2MgPSBQYXRoKHN5',
'cy5hcmd2WzFdKS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQYXRoLmN3ZCgpCnRlcCwgdGVwdCA9IGdv',
'YyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiCmlu',
'bigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMC4gTkVOIERPIikKIyBNT0kgTE9HIFBIQUkgVFUgS0hBSSBubyBkbyBDQUkg',
'R0kgYmFuZyBCTyBETyBOQU8uIEJhaSBob2MgMTktMDktMjAyNjogbW90IGx1b3QgZG8KIyBndWkgdmUgZHVvYyBkb2Mgbmh1',
'IGtldCBxdWEgY3VhIGJhbiB2YSBkYW5nIHhldCwgbmh1bmcgdGhhdCByYSBsYSBiYW4gZG8gQ1UgY2hheQojIHRyZW4gbmhh',
'bmggS0hBQy4gRG9jIHJhIHRoaSBtYXQgbW90IHZvbmc7IGxvZyB0dSBraGFpIHRoaSB0aGF5IG5nYXkgZG9uZyBkYXUuCnRy',
'eToKICAgIF90dSA9IGhhc2hsaWIuc2hhMjU2KFBhdGgoX19maWxlX18pLnJlYWRfYnl0ZXMoKSkuaGV4ZGlnZXN0KCkKZXhj',
'ZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgIF90dSA9IGYia2hvbmcgdHUgYmFtIGR1b2M6IHtfZX0iCmdoaSgiYm9fZG9fc2hh',
'MjU2IiwgX3R1KQppbm4oZiIgIEJPIERPICAgICAgICA6IHNoYTI1NiB7X3R1WzoxNl19ICAoYmFuIHtCQU5fQk9fRE99KSIp',
'CmlubigiICBzeXMucGxhdGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwgInwgcHl0aG9uIiwgc3lzLnZlcnNpb24uc3BsaXQoKVsw',
'XSkKaW5uKCIgIG9zLnBhdGhzZXAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSwgInwgUEFUSEVYVDoiLCByZXByKG9zLmVudmly',
'b24uZ2V0KCJQQVRIRVhUIikpWzo2MF0pCmlubigiICBQcm9ncmFtRmlsZXMgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlBy',
'b2dyYW1GaWxlcyIpKSwgInwgU3lzdGVtUm9vdDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290IikpKQppbm4o',
'IiAgQ09OR19DVV9HSVQgIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJDT05HX0NVX0dJVCIpKSkKaW5uKCIgIGdvYyBraG8g',
'ICAgICA6IiwgZ29jKQoKcXV5ZW4gPSBOb25lCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAg',
'IGltcG9ydCBjdHlwZXM7IHF1eWVuID0gYm9vbChjdHlwZXMud2luZGxsLnNoZWxsMzIuSXNVc2VyQW5BZG1pbigpKQogICAg',
'ZXhjZXB0IEV4Y2VwdGlvbjogcXV5ZW4gPSBOb25lCmdoaSgicXV5ZW5fYWRtaW4iLCBxdXllbikKc3ltbGlua19kdW9jID0g',
'Tm9uZQp0cnk6CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgo',
'dCkvImEudHh0IjsgZC53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICB0cnk6IG9zLnN5bWxpbmso',
'c3RyKGQpLCBzdHIoUGF0aCh0KS8ibGsiKSk7IHN5bWxpbmtfZHVvYyA9IFRydWUKICAgICAgICBleGNlcHQgT1NFcnJvciBh',
'cyBlOiBzeW1saW5rX2R1b2MgPSBGYWxzZTsgZ2hpKCJzeW1saW5rX2xvaSIsIGYie3R5cGUoZSkuX19uYW1lX199OiB7ZX0i',
'KQpleGNlcHQgRXhjZXB0aW9uIGFzIGU6IGdoaSgic3ltbGlua19sb2kiLCBzdHIoZSkpCmdoaSgic3ltbGlua19kdW9jIiwg',
'c3ltbGlua19kdW9jKQppbm4oIiAgQWRtaW5pc3RyYXRvcjoiLCBxdXllbiwgInwgdGFvIHN5bWxpbmsgZHVvYzoiLCBzeW1s',
'aW5rX2R1b2MpCgpsb2kgPSBbXQojIENvbmcga2ljaCB0aHVvYyBsYSBwaGVwIGRvIHRyZW4gTElDSCBTVSBHSVQsIGtob25n',
'IGRpbmggZ2kgZGVuIG5lbi4gQ2hvIHBoZXAKIyAtLWNoaS1raWNoLXRodW9jIGNoYXkgbyBtb2kgbmVuIGRlIGNvbiBUVSBL',
'SUVNIGR1b2MgY2hpbmggY29uZyBuYXkgKGRhIGR1bmcKIyBkZSB0YWkgZHVuZyBjYSBoYWkgdmUgY3VhIHN1IGNvIG5lbi1j',
'dSAxOS0wOSkuIE1vaSBjaG90IENIVUMgTkFORyB2YW4gZG9pIFdpbmRvd3MuCmlmIHN5cy5wbGF0Zm9ybSAhPSAid2luMzIi',
'IGFuZCAiLS1jaGkta2ljaC10aHVvYyIgbm90IGluIHN5cy5hcmd2OgogICAgbG9pLmFwcGVuZChmIktIT05HIHBoYWkgV2lu',
'ZG93cyAoc3lzLnBsYXRmb3JtPXtzeXMucGxhdGZvcm0hcn0pIikKaWYgbm90IHRlcC5pc19maWxlKCk6ICBsb2kuYXBwZW5k',
'KGYia2hvbmcgdGhheSB7dGVwfSIpCmlmIG5vdCB0ZXB0LmlzX2ZpbGUoKTogbG9pLmFwcGVuZChmImtob25nIHRoYXkge3Rl',
'cHR9IikKaWYgbm90IHNodXRpbC53aGljaCgiZ2l0Iik6IGxvaS5hcHBlbmQoImtob25nIGNvIGBnaXRgIHRyb25nIFBBVEgi',
'KQojIEJvIHRlc3QgKG11YyAyIHZhIE43KSBjYW4gUHlZQU1MOiB0aGlldSBubywgMGVhOTVkZSByYSA5Ni8xNjYgY2EgRE8g',
'KDg5IGJhbyB0aGFuZyAiTm8gbW9kdWxlIG5hbWVkICd5YW1sJyIsCiMgNyBxdWEgbHVvdCBjb247IGNvIFB5WUFNTDogMTY2',
'LzE2NiBRVUEpLiBCbyBkbyBnb2kgY2h1bmcgbGEgImNhIERPIExBIiByb2kgcGhhdCBUUlVPVCDigJQgZG8gdHJlbiAyMDI2',
'LTA5LTMwYy4KIyBEaWV1IGtpZW4gdGllbiBxdXlldCBwaGFpIGhvaSBiYW5nIENISU5IIHRpZW4gdHJpbmggY29uIHNlIGNo',
'YXkgYm8gdGVzdCAoY2hheSgpOiBjdW5nIG1vaSB0cnVvbmc7IGN3ZCA9IG9wcy8gPQojIHN5cy5wYXRoWzBdIGN1YSBibyB0',
'ZXN0KSB2YSBob2kgRFVORyBEVU9DIGNodSBraG9uZyBob2kgQ08gTUFULiBCYW4gMzBkIGhvaSBgZmluZF9zcGVjKCJ5YW1s',
'IilgIG8gdGllbiB0cmluaAojIE5BWSB2YSBuZ3VvbmcgMy44IHN1eSB0dSBOR1UgUEhBUCAoYDo9YCkg4oCUIGRvIHRyZW4g',
'MjAyNi0wOS0zMGQsIGNhIGhhaSByYSByYz0xIFRSVU9UIGNobyB1bmcgdmllbiBzYWNoOgojIHRodSBtdWMgZHUgbGlldSBg',
'eWFtbC9gIHRyZW4gUFlUSE9OUEFUSCBxdWEgZmluZF9zcGVjIG1hIGB5YW1sLnNhZmVfZHVtcGAga2hvbmcgY28gKDg3IGNh',
'ICJsYSIpOyBweXRob24gMy44LjIwCiMgVEhBVCBjbyBQeVlBTUwsIGJvIHRlc3QgZHVuZyBgc3RyLnJlbW92ZXByZWZpeGAg',
'KDMuOSkgbHVjIENIQVkgKDMzIGNhICJsYSI7IDMuOS4yMzogMTY2LzE2NikuCmlmIG5vdCAoIi0tY2hpLWtpY2gtdGh1b2Mi',
'IGluIHN5cy5hcmd2IG9yICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YpOgogICAgX3JjX2RrLCBfcmFfZGsgPSBjaGF5KFsi',
'LWMiLCAiaW1wb3J0IHN5czsgc3lzLmV4aXQoOSkgaWYgc3lzLnZlcnNpb25faW5mbyA8ICgzLCA5KSBlbHNlIE5vbmU7IGlt',
'cG9ydCB5YW1sOyIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIiB5YW1sLnNhZmVfZHVtcCh5YW1sLnNhZmVf',
'bG9hZCgnYTogMScpKSJdLAogICAgICAgICAgICAgICAgICAgICAgICAgIGdvYyAvICJvcHMiIGlmIChnb2MgLyAib3BzIiku',
'aXNfZGlyKCkgZWxzZSBQYXRoLmN3ZCgpLCBwaHV0PTIpCiAgICBpZiBfcmNfZGsgPT0gOToKICAgICAgICBsb2kuYXBwZW5k',
'KGYicHl0aG9uIHtzeXMudmVyc2lvbi5zcGxpdCgpWzBdfSA8IDMuOTogYm8gdGVzdCBjdWEgdW5nIHZpZW4gZHVuZyBzdHIu',
'cmVtb3ZlcHJlZml4ICgzLjkpIGx1YyBDSEFZIikKICAgIGVsaWYgX3JjX2RrOgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRo',
'b24gbmF5IEtIT05HIGNvIFB5WUFNTCBkdW5nIGR1b2MgKHsoX3JhX2RrLnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10p',
'Wy0xXVs6OTBdfSk6IgogICAgICAgICAgICAgICAgICAgZiIgXCJ7c3lzLmV4ZWN1dGFibGV9XCIgLW0gcGlwIGluc3RhbGwg',
'cHl5YW1sIgogICAgICAgICAgICAgICAgICAgIiAoYmFuIG5odW5nIHBzMSB0dSB0YWkgS0hPTkcgY28gcGlwOiBjaGF5IGxh',
'aSB2b2kgLVB5IDxweXRob24gZGEgY28gUHlZQU1MPikiKQogICAgIyBCbyB0ZXN0IGNvbiBnb2kgYHNodXRpbC53aGljaGAg',
'Y2hvIGJhc2gvYWN0aW9ubGludC9zaGVsbGNoZWNrICgwZWE5NWRlOiB0MzMgdDEzNyB0MTU5IGNhbiBhY3Rpb25saW50LCB0',
'MTM3IGNhbgogICAgIyBzaGVsbGNoZWNrLCBjYWMgY2EgY2hheSBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggY2FuIGJhc2gpLiBU',
'aGlldSB0aGkgY2FjIGNhIGF5IGluICJLSE9ORyBETyBEVU9DOiB0aGlldSBgLi4uYCIgdmEgYm8gZG8gcmEKICAgICMgcmM9',
'MyDigJQgbmh1bmcgY2hpIFNBVSBjYSBibyB0ZXN0IGxhbiBONyAoZG8gdHJlbiAyMDI2LTA5LTMwZywgUEFUSCB0aGlldSBh',
'Y3Rpb25saW50OiBgQ29uZyBjdSBkYXkgZHUgZGUgZG9gIEtERCwgcmM9MwogICAgIyBzYXUgMiBsdW90IGJvIHRlc3QpLiBD',
'dW5nIGx5IGRvIFB5WUFNTCBkdW9jIGhvaSBvIGRheTogaG9pIFRSVU9DLCBjdW5nIFBBVEggbWEgY2hheSgpIHRydXllbiBj',
'aG8gYm8gdGVzdC4KICAgIF90aGlldV9jYyA9IFtjIGZvciBjIGluICgiYmFzaCIsICJhY3Rpb25saW50IiwgInNoZWxsY2hl',
'Y2siKSBpZiBub3Qgc2h1dGlsLndoaWNoKGMpXQogICAgaWYgX3RoaWV1X2NjOgogICAgICAgIGxvaS5hcHBlbmQoZiJ0aGll',
'dSBjb25nIGN1IGJvIHRlc3QgZ29pIHF1YSBQQVRIOiB7X3RoaWV1X2NjfSAoYWN0aW9ubGludDogb3BzL2NhaV9hY3Rpb25s',
'aW50LnNoIHZvaSBBTF9WRVI7IgogICAgICAgICAgICAgICAgICAgIiBiYXNoOiBHaXQgQmFzaCwga2hvbmcgcGhhaSBiYXNo',
'LmV4ZSBjdWEgV1NMKSIpCiAgICAjIHNoZWxsY2hlY2sgS0hPTkcgbmhhbiAtLW5vcmMgdGhpIGFjdGlvbmxpbnQgMS43Ljcg',
'KHR1IHRydXllbiAtLW5vcmMpIGxhbSB0MzMgRE8sIHZhIFNIRUxMQ0hFQ0tfT1BUUz0tLW5vcmMgY3VhIGNoYXkoKSBsYW0K',
'ICAgICMgdDEzNyBETyDigJQgY2EgImxhIiA9PiBUUlVPVCBnaWEgKGRvIHRyZW4gMjAyNi0wOS0zMGgsIHNoZWxsY2hlY2sg',
'Z2lhIHR1IGNob2kgLS1ub3JjOiBiYW4gMzBoIHJjPTEgYGxhOiBbJ3QzMyddYCBzYXUgY2EKICAgICMgYm8gdGVzdCkuIGB3',
'aGljaGAgY2hpIGhvaSBDTyBNQVQ7IG8gZGF5IGhvaSBEVU5HIERVT0MuIE5ndW9uZyBkbyB0cmVuIHNoZWxsY2hlY2sgVEhB',
'VDogMC40LjcvMC41LjAvMC42LjAgdHUgY2hvaSAtLW5vcmMKICAgICMgKHJjPTMpLCAwLjcuMCB0cm8gbGVuIG5oYW4uIFBo',
'ZXAgaG9pIHBoYWkgdGhheSBEVU5HIFNIRUxMQ0hFQ0tfT1BUUyBtYSBjaGF5KCkgZGF0IGNobyBsdW90IGNvbjogYmFuIDMw',
'aSBob2kgdm9pIGJpZW4gQ1VBCiAgICAjIE5HVU9JIERPIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBpLCBzaGVsbGNoZWNrIDAu',
'OS4wICsgU0hFTExDSEVDS19PUFRTPS0tZXh0ZW5kZWQtYW5hbHlzaXM9dHJ1ZSAoY28gY3VhIDAuMTApOiByYz0zICJraG9u',
'ZyBuaGFuCiAgICAjIC0tbm9yYzogY2FwIG5oYXQgc2hlbGxjaGVjayIgdHJvbmcga2hpIHQzMy90MTM3IHF1YSBjaGF5KCkg',
'ZGV1IDEvMS4gR29pIFRIQU5HIChraG9uZyBxdWEgY2hheSgpKTogcXVhIGhhbiB0aGkgcnVuKCkgZ2lldAogICAgIyBkdW5n',
'IHNoZWxsY2hlY2s7IHF1YSBjaGF5KCkgdGhpIGNoaSBnaWV0IHB5dGhvbiBjb24sIHNoZWxsY2hlY2sgdHJlbyBvIGxhaSBt',
'byBjb2kgKGRvIHRyZW4gMjAyNi0wOS0zMGk6IDEvMSBjb24gc29uZykuCiAgICBlbGlmIHN1YnByb2Nlc3MucnVuKFtzaHV0',
'aWwud2hpY2goInNoZWxsY2hlY2siKSwgIi0tbm9yYyIsICItLXZlcnNpb24iXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGlt',
'ZW91dD02MCwKICAgICAgICAgICAgICAgICAgICAgICAgZW52PWRpY3Qob3MuZW52aXJvbiwgU0hFTExDSEVDS19PUFRTPSIt',
'LW5vcmMiKSkucmV0dXJuY29kZToKICAgICAgICBsb2kuYXBwZW5kKCJzaGVsbGNoZWNrIHRyZW4gUEFUSCBraG9uZyBuaGFu',
'IC0tbm9yYyAoYWN0aW9ubGludCAxLjcuNyB2YSBjaGF5KCkgZGV1IHRydXllbiBjbyBheSk6IGNhcCBuaGF0IHNoZWxsY2hl',
'Y2siKQoKcmMsIGhlYWQsIF8gPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIkhFQUQiKQppZiByYzogbG9pLmFwcGVuZCgia2hv',
'bmcgZG9jIGR1b2MgSEVBRCIpCmdoaSgiaGVhZCIsIGhlYWQpCnJjX2EsIF8sIF8gPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIs',
'ICItLWlzLWFuY2VzdG9yIiwgU0hBX0cxLCBoZWFkIG9yICJIRUFEIikKbGFfaGF1X2R1ZSA9IChyY19hID09IDApCmlmIGhl',
'YWQgPT0gU0hBX0cxOgogICAgdGhlX2hlID0gImcxIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBEQVkgTEEgZzEu',
'IENIVUEgY28gYmFuIHZhIGcyOyBrZXQgcXVhIGR1b2kgbGEgTkVOIERPLiIpCmVsaWYgbGFfaGF1X2R1ZToKICAgIHRoZV9o',
'ZSA9ICJnMiI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gaGF1IGR1ZSBjdWEgZzEgKHtTSEFfRzFbOjhdfSk7IHVu',
'ZyB2aWVuIGcyIGhheSBraG9uZzogTjcnIChtdWMgMSkgZGluaCBkYW5oLiIpCmVsc2U6CiAgICB0aGVfaGUgPSAiPyI7IGxv',
'aS5hcHBlbmQoZiJIRUFEPXtoZWFkWzo4XX0gS0hPTkcgcGhhaSBnMSB2YSBLSE9ORyBwaGFpIGhhdSBkdWUgY3VhIHtTSEFf',
'RzFbOjhdfSDigJQgcmViYXNlPyBuaGFtIG5oYW5oPyIpCmdoaSgidGhlX2hlIiwgdGhlX2hlKQpyY19yLCByZWZzLCBfID0g',
'Z2l0KGdvYywgImZvci1lYWNoLXJlZiIsICItLXBvaW50cy1hdCIsIGhlYWQgb3IgIkhFQUQiLAogICAgICAgICAgICAgICAg',
'ICAgICItLWZvcm1hdD0lKHJlZm5hbWU6c2hvcnQpIikKZHNyID0gW3ggZm9yIHggaW4gcmVmcy5zcGxpdGxpbmVzKCkgaWYg',
'eC5zdHJpcCgpIGFuZCB4LnN0cmlwKCkgIT0gImRvLXRhbSJdCmdoaSgicmVmX3Ryb190b2lfaGVhZCIsIGRzcikKaW5uKGYi',
'ICByZWYgdHJvIHRvaSBIRUFEOiB7JywgJy5qb2luKGRzcikgaWYgZHNyIGVsc2UgJyhraG9uZyByZWYgbmFvIC0gSEVBRCBy',
'b2kgdHUgZG8pJ30iKQoKaWYgbG9pOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBuZW4gZG8gc2FpLCBLSE9O',
'RyBpbiBrZXQgbHVhbiBuYW8uIikKICAgIGZvciB4IGluIGxvaTogaW5uKCIgIC0iLCB4KQogICAgc3lzLmV4aXQoMykKCiMg',
'LS0tLS0tLS0tLS0tLS0tLSAxLiBraWNoIHRodW9jIChONycgY3VhIHNwZWMgcjMpIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIi',
'KTsgaW5uKCItIiAqIDc4KTsgaW5uKCIxLiBLSUNIIFRIVU9DIOKAlCB0cmFuIHNwZWMgcjM6IDw9IDIgdGVwIHZhIDw9IDQw',
'MCBkb25nIHRoZW0iKQojIFZFIE5FTiBQSEFJIFRVT0kg4oCUIHZhIHBoYWkgQ0hVTkcgTUlOSCBkdW9jIGxhIHR1b2ksIGto',
'b25nIHBoYWkgZ2lhIGRpbmguCiMgQmFpIGhvYyB0cmEgZ2lhIDE5LTA5LTIwMjY6IGNsb25lIHRhaSBkdW5nIGNoaSBmZXRj',
'aCBuaGFuaCBiYW4gdmEsIGBvcmlnaW4vbWFzdGVyYAojIGR1bmcgeWVuIHR1IDE0LTA5IChjMTZiZDMyLCBzYXUgOTcgY29t',
'bWl0KS4gbWVyZ2UtYmFzZSByb2kgdmUgZHVuZyBkaW5oIG1hc3RlciBjdSwKIyBuZW4gZGlmZiBOVU9UIGNhIDk3IGNvbW1p',
'dCBtYXN0ZXI6IGRvIHJhIDQ2IHRlcCAvICs3MTE4IHRoYXkgdmkgMiB0ZXAgLyArMzk3IOKAlAojIENVTkcgTU9UIENPTU1J',
'VCAwZWE5NWRlLiBNb3QgdGlldSBjaGkgREVMVEEgbWEgdmUgbmVuIGtob25nIHR1b2kgdGhpIGtob25nIHNhaQojIGxlY2gg',
'bW90IGNodXQsIG5vIHNhaSBjYSBtb3QgYmFjIGRvIGxvbi4KIyBDaG8gbmVuOiBuZW4ga2hvbmcgY2h1bmcgbWluaCBkdW9j',
'IGxhIHR1b2kgPT4gS0hPTkcgRE8gRFVPQyAocmM9MyksIEtIT05HIHBoYWkgVFJVT1QuCiMgVFJVT1QgbGEgbW90IFBIQU4g',
'UVVZRVQgdmUgYmFuIHZhOyBwaGFuIHF1eWV0IGNoaSBkdW9jIHBoZXAgcGhhdCByYSBraGkgZGEgZG8gZHVvYy4KZXIgPSAi',
'IgpyY191LCB1cmxfdGhvLCBfID0gZ2l0KGdvYywgInJlbW90ZSIsICJnZXQtdXJsIiwgIm9yaWdpbiIpCnVybF9vLCB1cmxf',
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
'CiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJkaWZmLXRyZWUiLCAiLXIiLCAiLU0iLCAiLS1kaWZmLWFsZ29y',
'aXRobT1teWVycyIsICItLW51bXN0YXQiLCBTSEFfQkFTRV9TUEVDLCBoZWFkKQogICAgICAgIGlmIG5vdCByY194OgogICAg',
'ICAgICAgICBoID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnNfeC5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAg',
'ICAgICAgICBhID0gc3VtKGludCh4WzBdKSBmb3IgeCBpbiBoIGlmIHhbMF0uaXNkaWdpdCgpKQogICAgICAgICAgICBnaGko',
'Im51bXN0YXRfdGhlb19iYXNlX3NwZWMiLCB7InRlcCI6IGxlbihoKSwgInRoZW0iOiBhfSkKICAgICAgICAgICAgaW5uKGYi',
'ICAgICAgICAgKGRvaSBjaGlldTogc28gYmFzZSBzcGVjID0ge2xlbihoKX0gdGVwIC8gK3thfSDigJQgY29uIHNvIGF5IEtI',
'T05HIGR1bmcgZGUgY2hhbSkiKQogICAgIyBQTFVNQklORywga2hvbmcgUE9SQ0VMQUlOOiBgZ2l0IGRpZmZgIGRvYyBjYXUg',
'aGluaCBVSSBDVUEgTkdVT0kgRE8gKGRpZmYuYWxnb3JpdGhtLCBkaWZmLnJlbmFtZXMsIGRpZmYub3JkZXJGaWxlLAogICAg',
'IyBjb2xvci5kaWZmKSwgdmEgZ2lhIHRyaSBIT1AgTEUgZG9pIGx1b24gU08gZG9uZyBtYSB2YW4gcmEgY2h1IHNvIOKAlCBk',
'byB0cmVuIDIwMjYtMDktMzBpOiB1bmcgdmllbiB0b25nIGhvcCAobXllcnMgKzQwMSkgPT4KICAgICMgYmFuIDMwaSBEQVQg',
'MiB0ZXAgLyArNDAwIGR1b2kgYGRpZmYuYWxnb3JpdGhtID0gaGlzdG9ncmFtYCBob2FjIGBwYXRpZW5jZWAsIFRSVU9UICs0',
'MDEga2hpIG1hYyBkaW5oOyAxMC83NSBjb21taXQgY2hhbQogICAgIyB3cml0ZSBzZXQgY28gc28gZG9uZyBkb2kgdGhlbyB0',
'aHVhdCB0b2FuLiBgZGlmZi10cmVlIC1yIC1NYCA9IG1hYyBkaW5oIGN1YSBgZ2l0IGRpZmZgIChyZW5hbWVzIGJhdCkgdmEg',
'S0hPTkcgZG9jIGNhYyBraG9hCiAgICAjIGF5LiBUaHVhdCB0b2FuIHBoYWkgVFVPTkcgTUlOSDogZGlmZi48ZHJpdmVyPi5h',
'bGdvcml0aG0gKHF1YSBjb3JlLmF0dHJpYnV0ZXNGaWxlIGN1YSBuZ3VvaSBkbykgVkFOIGxvdCB2YW8gcGx1bWJpbmcg4oCU',
'CiAgICAjIGRvIHRyZW4gMjAyNi0wOS0zMGksIGAqLnB5IGRpZmY9YWxnYCArIGRpZmYuYWxnLmFsZ29yaXRobT1oaXN0b2dy',
'YW06IGRpZmYtdHJlZSArNDAxIGNobyB1bmcgdmllbiBteWVycyArNDAwOyBjbyB0dW9uZyBtaW5oCiAgICAjIHRoYW5nIGto',
'b2EgYXkuIGF0dHJpYnV0ZXMgYC1kaWZmYC9jb3JlLmJpZ0ZpbGVUaHJlc2hvbGQgdmFuIGFwID0+IGAtYCA9PiBLSE9ORyBE',
'TyBEVU9DIChjaG90IGR1b2kpLgogICAgcmMsIG5zLCBlciA9IGdpdChnb2MsICJkaWZmLXRyZWUiLCAiLXIiLCAiLU0iLCAi',
'LS1kaWZmLWFsZ29yaXRobT1teWVycyIsICItLW51bXN0YXQiLCBtYiwgaGVhZCkKaWYgcmM6CiAgICBwYXNzCmVsc2U6CiAg',
'ICBoYW5nID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnMuc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgIHRoZW0g',
'PSBzdW0oaW50KGhbMF0pIGZvciBoIGluIGhhbmcgaWYgaFswXS5pc2RpZ2l0KCkpCiAgICB4b2EgID0gc3VtKGludChoWzFd',
'KSBmb3IgaCBpbiBoYW5nIGlmIGhbMV0uaXNkaWdpdCgpKQogICAgZ2hpKCJzb190ZXAiLCBsZW4oaGFuZykpOyBnaGkoImRv',
'bmdfdGhlbSIsIHRoZW0pOyBnaGkoImRvbmdfeG9hIiwgeG9hKQogICAgZm9yIGggaW4gaGFuZzogaW5uKGYiICAgIHtoWzJd',
'OjM0fSAre2hbMF06PDV9IC17aFsxXX0iKQogICAgaW5uKGYiICAgIFRPTkc6IHtsZW4oaGFuZyl9IHRlcCwgK3t0aGVtfSwg',
'LXt4b2F9ICAgKHRyYW46IHtUUkFOX1RFUH0gdGVwIC8ge1RSQU5fRE9OR30gZG9uZyB0aGVtKSIpCiAgICBjaGFtID0gc29y',
'dGVkKHtoWzJdIGZvciBoIGluIGhhbmd9ICYgV1JJVEVfU0VUX0cyKTsgZ2hpKCJjaGFtX3dyaXRlX3NldCIsIGNoYW0pCiAg',
'ICBkZWYgX2NhX21vaV9jbyhyZXYpOgogICAgICAgICMgY2F0LWZpbGUsIGtob25nIGBzaG93YDogYGdpdCBzaG93YCBjaGV0',
'IHZvaSBjYXUgaGluaCBVSSBnbyBzYWkgKGRvIHRyZW4gMjAyNi0wOS0zMGk6IGxvZy5kYXRlIGdvIHNhaSA9PiBiYW4gMzBp',
'IGdvaQogICAgICAgICMgMGVhOTVkZSBsYSAia2hvbmcgcGhhaSB1bmcgdmllbiAuLi4gTm9uZSDigJQgZGEgbGFuZD8gbmhh',
'bSBuaGFuaD8iKS4KICAgICAgICByXywgbmRfLCBfID0gZ2l0KGdvYywgImNhdC1maWxlIiwgIi1wIiwgZiJ7cmV2fTpvcHMv',
'bGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICByZXR1cm4gTm9uZSBpZiByXyBlbHNlIHt0IGZvciB0IGluIENBX01P',
'SV9HMiBpZiByZS5zZWFyY2gociIoP20pXmRlZiAiICsgdCArIHIiW2Etel0/XyIsIG5kXyl9CiAgICBvX21iLCBvX2ggPSBf',
'Y2FfbW9pX2NvKG1iKSwgX2NhX21vaV9jbyhoZWFkKQogICAgbWFuZyA9IHNvcnRlZChvX2ggLSBvX21iLCBrZXk9c29fY2Ep',
'IGlmIChvX21iIGlzIG5vdCBOb25lIGFuZCBvX2ggaXMgbm90IE5vbmUpIGVsc2UgTm9uZQogICAgZ2hpKCJjYV9tb2lfZzJf',
'bWFuZ192YW8iLCBtYW5nKQogICAgaWYgbm90IG1hbmc6CiAgICAgICAgIyBEbyBST05HIChkYSBsYW5kLCBjaGluaCBtYXN0',
'ZXIpLCBuaGFtIG5oYW5oLCBoYXkgbmhhbmggY3VhIHBhY2tldCBLSEFDIGNoYW0gY3VuZyB0ZXA6CiAgICAgICAgIyBraG9u',
'ZyBtYW5nIGNhIG1vaSBuYW8gY3VhIGcyIHRoaSBraG9uZyBwaGFpIHVuZyB2aWVuLiBEb2Mga2hvbmcgZHVvYyAoTm9uZSkg',
'Y3VuZyB2YXkuCiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJkb2kgdHVvbmcga2hvbmcgcGhhaSB1bmcg',
'dmllbjoge2xlbihoYW5nKX0gdGVwLCBjaGFtIHtjaGFtfSwgY2EgbW9pICIKICAgICAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgICBmImcyIG1hbmcgdmFvIHttYW5nIXJ9IOKAlCBkYSBsYW5kPyBuaGFtIG5oYW5oPyBwYWNrZXQga2hhYz8iKQog',
'ICAgZWxzZToKICAgICAgICAjIG51bXN0YXQgaW4gYC1gIChraG9uZyBjbyBzbyBkb25nKSBjaG8gdGVwIGJpbmFyeS8tZGlm',
'ZiB0aGVvIGF0dHJpYnV0ZXMg4oCUIGtlIGNhIGF0dHJpYnV0ZXMgQ1VBIE5HVU9JIERPIChkbyB0cmVuCiAgICAgICAgIyAy',
'MDI2LTA5LTMwZzogY29yZS5hdHRyaWJ1dGVzRmlsZSBgKi5weSAtZGlmZmAgPT4gIjIgdGVwIC8gKzAiIERBVCBjaG8gMGVh',
'OTVkZSwgdGhhdCArMzk3KS4gYC1gIGxhIEtIT05HIERPIERVT0MsCiAgICAgICAgIyBraG9uZyBwaGFpIDA7IFRSVU9UIHRo',
'ZW8gc28gdGVwIC8gc28gZG9uZyBEQSBkZW0gZHVvYyB2YW4gZ2l1IChxdWFuIHNhdCB0cnVjIHRpZXApLgogICAgICAgIGto',
'b25nX3NvID0gW2hbMl0gZm9yIGggaW4gaGFuZyBpZiBub3QgKGhbMF0uaXNkaWdpdCgpIGFuZCBoWzFdLmlzZGlnaXQoKSld',
'OyBnaGkoInRlcF9raG9uZ19zb19kb25nIiwga2hvbmdfc28pCiAgICAgICAgdnVvdCA9IGxlbihoYW5nKSA+IFRSQU5fVEVQ',
'IG9yIHRoZW0gPiBUUkFOX0RPTkcKICAgICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgVFJVT1QgaWYgdnVvdCBlbHNlIChL',
'REQgaWYga2hvbmdfc28gZWxzZSBEQVQpLAogICAgICAgICAgICBmIntsZW4oaGFuZyl9IHRlcCAvICt7dGhlbX0iICsgKGYi',
'IOKAlCBudW1zdGF0IEtIT05HIGNvIHNvIGRvbmcgY2hvIHtraG9uZ19zb30iIGlmIGtob25nX3NvIGVsc2UgIiIpKQoKIyBD',
'b25nIGtpY2ggdGh1b2MgUEhBSSBkZSBsYWkgTU9UIGtldCBxdWEuIExlbmggbnVtc3RhdCBob25nIHRoaSBuaGFuaCBgaWYg',
'cmM6IHBhc3NgIGtob25nIGdoaSBnaSwgdmEgdmFuZyBtYXQgbyBkYXkKIyB0aGFuaCBEQVQgbyBibyBnb3A6IGNhdSBoaW5o',
'IGRpZmYgQ1VBIE5HVU9JIERPIGhvbmcgKGRpZmYub3JkZXJGaWxlIHRybyB0ZXAga2hvbmcgY28sIGRpZmYuYWxnb3JpdGht',
'IGdvIHNhaSA9PiByYz0xMjgpIGNobwojIC0tY2hpLWtpY2gtdGh1b2MgcmM9MCB2b2kgMCBjaG90LCBsdW90IGRheSBkdSAi',
'REFUIDExIiByYz0wIChkbyB0cmVuIDIwMjYtMDktMzBoLCAwZWE5NWRlKS4gVmFuZyBtYXQgbGEgS0hPTkcgRE8gRFVPQy4K',
'IyBUdSAzMGogbnVtc3RhdCBsYSBkaWZmLXRyZWUgKGtob25nIGRvYyBoYWkga2hvYSBheSk7IGR1b25nIGNvbiBsYWkgZG8g',
'ZHVvYzogZGlmZi5yZW5hbWVMaW1pdCBnbyBzYWkgPT4gcmM9MTI4LgppZiBub3QgYW55KGNbMF0gPT0gIk43JyBraWNoIHRo',
'dW9jIiBmb3IgYyBpbiBjaG90KToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYiY29uZyBLSE9ORyByYSBrZXQg',
'cXVhIChnaXQgZGlmZi10cmVlIC0tbnVtc3RhdCByYz17cmN9KToge19hbl91c2VyaW5mbyhlcilbOjcwXX0iKQoKIyBEaW5o',
'IGRhbmggVEhBVCBuYW0gbyBONycgKGNhIG1vaSBnMiBtYW5nIHZhbyksIEtIT05HIG8gImhhdSBkdWUgZzEiOiBnMSBkYSBs',
'YW5kIG5lbiBtb2kgbmhhbmggZGV1CiMgbGEgaGF1IGR1ZS4gRG9uZyBkYXUga2hvaSBkYW4gcGhhaSB0dSBraGFpIHRoZW8g',
'a2V0IHF1YSBheSAoZG8gZHVvYzogbWFzdGVyIDQ0NjIwZTggbW8ga2hvaSBiYW5nCiMgIlRIRSBIRSBETyBEVU9DOiBnMiIs',
'IEpTT04gInRoZV9oZSI6ICJnMiIsIHRyb25nIGtoaSBONycgZGEga2V0IGx1YW4gImtob25nIHBoYWkgdW5nIHZpZW4iKS4K',
'IyBOaGFuIGNoaSBkdW9jIG5vaSBEVU5HIGNhaSBkbyBkdW9jOiBgW11gIGtob25nIHRhY2ggImRhIGxhbmQiIGtob2kgIm5o',
'YW0gbmhhbmgiLyJwYWNrZXQga2hhYyIgKGRvCiMgZHVvYyB0cmVuIDIwMjYtMDktMzBiOiB1bmcgdmllbiAyYTY3OTY4IERB',
'IExBTkQgYmkgZ29pICJLSE9ORyBwaGFpIHVuZyB2aWVuIGcyIikuCmlmIHRoZV9oZSA9PSAiZzIiIGFuZCBub3Qgc28uZ2V0',
'KCJjYV9tb2lfZzJfbWFuZ192YW8iKToKICAgIHRoZV9oZSA9ICgiS0hPTkcgbWFuZyBjYSBtb2kgZzIgbmFvIChkYSBsYW5k',
'PyBuaGFtIG5oYW5oPyBwYWNrZXQga2hhYz8pIiBpZiBzby5nZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpID09IFtdCiAgICAg',
'ICAgICAgICAgZWxzZSAiZzI/IChDSFVBIGRpbmggZGFuaCBkdW9jIGRvaSB0dW9uZykiKQogICAgZ2hpKCJ0aGVfaGUiLCB0',
'aGVfaGUpCgojIENvbmcgbmhhbmg6IGRvIFJJRU5HIGtpY2ggdGh1b2MgKHZhaSBnaWF5KSByb2kgZHVuZy4gRHVuZyBraGkg',
'Y2FuIHhhYyBtaW5oIGxhaQojIHZlIG5lbiBtYSBraG9uZyBtdW9uIHRyYSAyMC00NSBwaHV0IGNobyBjYSBibyB0ZXN0Lgpp',
'ZiAiLS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Y6CiAgICBpbm4oIiIpOyBpbm4oIj0iICogNzgpCiAgICBpbm4oIi0t',
'Y2hpLWtpY2gtdGh1b2M6IENISSBkbyBjb25nIGtpY2ggdGh1b2MuIERheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5naGllbSB0',
'aHUuIikKICAgIGlubigiLSIgKiA3OCkKICAgIGZvciBfdCwgX3R0LCBfY3QgaW4gY2hvdDogaW5uKGYiICB7X3R0OjE0fSB7',
'X3R9IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICBfayA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3Qg',
'aWYgdCA9PSBLREQpCiAgICBfciA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKICAgIHN5cy5l',
'eGl0KDMgaWYgX2sgZWxzZSAoMSBpZiBfciBlbHNlIDApKQoKQ0hJX1BST0JFID0gIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJn',
'diAgICAjIGJvIHF1YSBibyB0ZXN0ICsgTjc7IGdpdSAwLCAxLCAzCiMgLS0tLS0tLS0tLS0tLS0tLSAyLiBibyB0ZXN0IGRh',
'eSBkdSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4o',
'IjIuIEJPIFRFU1QgREFZIERVICgxMC00MCBwaHV0KSIpCiAgICByY19uLCBvdXRfbiA9IGNoYXkoWyJvcHMvbGVhc2VfcHVi',
'bGlzaF90ZXN0LnB5Il0sIGdvYykKICAgIGdoaSgicmNfc3VpdGUiLCByY19uKQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91',
'dF9uKQogICAgaW5uKCIgIHJjID0iLCByY19uLCAifCIsIG0uZ3JvdXAoMCkgaWYgbSBlbHNlICIoS0hPTkcgZG9jIGR1b2Mg',
'ZG9uZyB0b25nIGtldCkiKQogICAgaWYgbToKICAgICAgICBnaGkoImRhdCIsIGludChtLmdyb3VwKDEpKSk7IGdoaSgidHJl',
'biIsIGludChtLmdyb3VwKDIpKSk7IGdoaSgiYm9fcXVhX3NvIiwgaW50KG0uZ3JvdXAoNCkpKQogICAgZG9faGV0LCBnYywg',
'dGluID0gZG9jX2RvKG91dF9uKQogICAgZ2hpKCJzb19jYV9kbyIsIGxlbihkb19oZXQpKTsgZ2hpKCJsaWV0X2tlX2RheV9k',
'dSIsIHRpbikKICAgIGZvciBnIGluIGdjOiBpbm4oIiAgICoiLCBnKQogICAgaW5uKCIiKTsgaW5uKGYiICA9PT0ge2xlbihk',
'b19oZXQpfSBDQSBETyA9PT0iKQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAgICBpbm4o',
'ZiIgICB7dC5zcGxpdCgnXycpWzBdOjd9IHt0fSIpOyBpbm4oZiIgICAgICAgICAgIHtkb19oZXRbdF1bOjE1MF19IikKICAg',
'IGdoaSgiZG9fbHlfZG8iLCB7dDogZG9faGV0W3RdWzozMDBdIGZvciB0IGluIGRvX2hldH0pCiAgICAjIC0tLS0gQ0hPVDog',
'bW9pIGNhIERPIHBoYWkgR0lBSSBUSElDSCBEVU9DIC0tLS0KICAgICMgVGhpZXUgY2hvdCBuYXksIGJvIGRvIGluIGRhbmgg',
'c2FjaCBkbyByb2kgdmFuIHRob2F0IHJjPTAuIERvIGR1bmcgbGEgbG9pIGRhIHhheSByYToKICAgICMgbHVvdCBXaW5kb3dz',
'IDE5LTA5IGNvIHQxNzEgRE8gbWEgYm8gZG8gYmFvICJEQVQgMTAgfCBUUlVPVCAwIiB2YSByYz0wLgogICAgZGVmIF9raG9h',
'KHQpOiByZXR1cm4gdC5zcGxpdCgiXyIpWzBdCiAgICBkb19wYWNrZXQsIGRvX2xhLCBkb190aGlldV9jb25nX2N1ID0gW10s',
'IFtdLCBbXQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAgICBrLCBseSA9IF9raG9hKHQp',
'LCBkb19oZXRbdF0KICAgICAgICBpZiBrIGluIENBX1BBQ0tFVDogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb19w',
'YWNrZXQuYXBwZW5kKHQpCiAgICAgICAgZWxpZiAiS0jDlE5HIMSQTyDEkMav4buiQyIgaW4gbHkgb3IgInRoaeG6v3UgYCIg',
'aW4gbHk6ICBkb190aGlldV9jb25nX2N1LmFwcGVuZCh0KQogICAgICAgIGVsaWYgayBpbiBOR09BSV9QSEFNX1ZJOiAgICAg',
'ICAgICAgICAgICAgICAgICAgIHBhc3MKICAgICAgICBlbHNlOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgICBkb19sYS5hcHBlbmQodCkKICAgIGdoaSgiZG9fcGFja2V0IiwgZG9fcGFja2V0KTsgZ2hpKCJkb19sYSIsIGRv',
'X2xhKTsgZ2hpKCJkb190aGlldV9jb25nX2N1IiwgZG9fdGhpZXVfY29uZ19jdSkKICAgIGlubigiIikKICAgIGlubihmIiAg',
'Y2EgRE8gdGh1b2MgQ0hJTkggcGFja2V0IG5heSA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XSBvciAna2hvbmcg',
'Y28nfSIpCiAgICBpbm4oZiIgIGNhIERPIG5nb2FpIHBoYW0gdmkgKHIzIGtoYWkpOiB7W19raG9hKHgpIGZvciB4IGluIHNv',
'cnRlZChkb19oZXQsIGtleT1zb19jYSkgaWYgX2tob2EoeCkgaW4gTkdPQUlfUEhBTV9WSV19IikKICAgIGlubihmIiAgY2Eg',
'RE8gdmkgVEhJRVUgQ09ORyBDVSAgICAgICA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV0gb3IgJ2to',
'b25nIGNvJ30iKQogICAgaW5uKGYiICBjYSBETyBMQSAoa2hvbmcgZ2lhaSB0aGljaCBkdW9jKToge1tfa2hvYSh4KSBmb3Ig',
'eCBpbiBkb19sYV0gb3IgJ2tob25nIGNvJ30iKQogICAgIyAtLS0tIENIT1Q6IHBoZXAgZG8gcGhhaSBUUk9OIHRydW9jIGto',
'aSBtb3QgY2h1IERBVCBuYW8gZHVvYyBwaGF0IC0tLS0KICAgICMgQmFuIHRydW9jIGNoaSBJTiBgdGluYC9gcmNfc3VpdGVg',
'OiBibyB0ZXN0IGNoZXQgZ2l1YSB0MTcxIChyYz0xMzQsIGtob25nIGRvbmcgdG9uZykKICAgICMgdmFuIHJhICJEQVQgMTIg',
'fCBUUlVPVCAwIiByYz0wOyBjYSBQQUNLRVQgdmFuZyBtYXQgaGF5IGJpIEJPIFFVQSBjdW5nIGR1b2MgY2hhbSBuaHUKICAg',
'ICMgImtob25nIGRvIi4gVmFuZyBtYXQga2hvbmcgcGhhaSAia2hvbmcgZG8iIOKAlCBsYSBLSE9ORyBETyBEVU9DLgogICAg',
'dmFuZyA9IFt0IGZvciB0IGluIHNvcnRlZChDQV9QQUNLRVQsIGtleT1zb19jYSkgaWYgbWF1X2NhKG91dF9uLCB0KSBub3Qg',
'aW4gKCJRVUEiLCAiRE8iKV0KICAgIGx5X2tkZCA9IFtdCiAgICBpZiBub3QgdGluOiBseV9rZGQuYXBwZW5kKCJkYW5oIHNh',
'Y2ggZG8gS0hPTkcgZGF5IGR1IikKICAgIGlmIHJjX24gbm90IGluICgwLCAxKSBvciAocmNfbiA9PSAxKSAhPSBib29sKGRv',
'X2hldCk6CiAgICAgICAgbHlfa2RkLmFwcGVuZChmInJjIGJvIHRlc3Q9e3JjX259IGtob25nIGtob3Age2xlbihkb19oZXQp',
'fSBjYSBETyBkb2MgZHVvYyIpCiAgICBpZiB2YW5nOiBseV9rZGQuYXBwZW5kKGYiY2EgUEFDS0VUIHZhbmcvYm8gcXVhOiB7',
'dmFuZ30iKQogICAgZ2hpKCJjYV9wYWNrZXRfdmFuZyIsIHZhbmcpOyBnaGkoImx5X2RvX2NodWFfdHJvbiIsIGx5X2tkZCkK',
'ICAgIGlmIGx5X2tkZDoga2V0KCJCbyB0ZXN0IGNoYXkgVFJPTiB2YSBkb2MgRFUiLCBLREQsICI7ICIuam9pbihseV9rZGQp',
'KQogICAgY2h1YV90cm9uID0gS0REIGlmIGx5X2tkZCBlbHNlIERBVAogICAga2V0KCJLaG9uZyBjYSBuYW8gY3VhIFBBQ0tF',
'VCBiaSBETyIsIGNodWFfdHJvbiBpZiBub3QgZG9fcGFja2V0IGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX3Bh',
'Y2tldCBlbHNlIGYiRE86IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XX0g4oCUIGJhbiB2YSBDSFVBIHhvbmciKQog',
'ICAga2V0KCJNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIsIGNodWFfdHJvbiBpZiBub3QgZG9fbGEgZWxzZSBUUlVP',
'VCwKICAgICAgICAiIiBpZiBub3QgZG9fbGEgZWxzZSBmImxhOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXX0iKQogICAg',
'aWYgZG9fdGhpZXVfY29uZ19jdToKICAgICAgICBrZXQoIkNvbmcgY3UgZGF5IGR1IGRlIGRvIiwgS0RELCBmInRoaWV1IGNv',
'bmcgY3UgY2hvIHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV19IikKCiAgICBicSA9IHNvcnRlZCh7dCBm',
'b3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXRfbil9LCBrZXk9c29fY2EpOyBnaGkoImNhX2JvX3F1YSIsIGJxKQog',
'ICAgaW5uKCIiKTsgaW5uKGYiICBCTyBRVUEgKHtsZW4oYnEpfSk6IHtbeC5zcGxpdCgnXycpWzBdIGZvciB4IGluIGJxXX0i',
'KQoKICAgIGlubigiIik7IGlubigiICBOMS1ONCAodDE2NS10MTY4KSwgdGlldSBjaGkgbmdoaWVtIHRodSBjdWEgcjIsIG5h',
'eSBsYSBjaGkgYmFvIGhvaSBxdXk6IikKICAgIGI0ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0FNT0l9OyBn',
'aGkoImNhX21vaSIsIGI0KQogICAgZm9yIHQgaW4gQ0FNT0k6IGlubihmIiAgICAge3R9OiB7YjRbdF19IikKICAgICMgQk9f',
'UVVBL3ZhbmcgbGEgQ0hVQSBDSEFZLCBraG9uZyBwaGFpIERPOiBjaGkgbW90IGNhIERPIG1vaSBkdW9jIHBoYXQgVFJVT1Qu',
'CiAgICBrZXQoIk4xLU40ICh0MTY1LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJRVUEiIGZvciB2IGluIGI0LnZhbHVlcygp',
'KQogICAgICAgIGVsc2UgKFRSVU9UIGlmIGFueSh2ID09ICJETyIgZm9yIHYgaW4gYjQudmFsdWVzKCkpIGVsc2UgS0REKSwg',
'c3RyKGI0KSkKCiAgICBpbm4oIiIpOyBpbm4oIiAgMTUgY2EgdHVuZyBkbyB0cmVuIENJOiIpCiAgICBiMTUgPSB7dDogbWF1',
'X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQogICAgaW5uKCIgICAgIiArICIgICIuam9p',
'bihmInt0fTp7YjE1W3RdfSIgZm9yIHQgaW4gQ0ExNSkpCgogICAgIyB0MTM2IOKAlCBOMTIgZG8gR0lBTiBUSUVQIHF1YSBr',
'ZXQgcXVhIGNhCiAgICB0MTM2X3RlbiA9IG5leHQoKHQgZm9yIHQgaW4gZG9faGV0IGlmIHQuc3RhcnRzd2l0aCgidDEzNiIp',
'KSwgTm9uZSkKICAgIGlmIGIxNS5nZXQoInQxMzYiKSA9PSAiUVVBIjoKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0',
'IHF1YSBjYSkiLCBEQVQsICJ0MTM2IFFVQSIpCiAgICBlbGlmIGIxNS5nZXQoInQxMzYiKSAhPSAiRE8iOgogICAgICAgIGtl',
'dCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIEtERCwgZiJ0MTM2ID0ge2IxNS5nZXQoJ3QxMzYnKSFyfSDigJQga2hv',
'bmcgY2hheS9raG9uZyB0aGF5IikKICAgIGVsc2U6CiAgICAgICAgbHkgPSBkb19oZXQuZ2V0KHQxMzZfdGVuLCAiIikKICAg',
'ICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBUUlVPVCwgZiJETzoge2x5Wzo5MF19IikKCiMgLS0tLS0t',
'LS0tLS0tLS0tLSAzLiBwcm9iZSBUSEFORyB2YW8gaGFtIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4',
'KTsgaW5uKCIzLiBQUk9CRSBUSEFORyDigJQgZ29pIF9naXRfd2luZG93cyB2b2kgdGhhbSBzbyB0aWVtIikKc3BlYyA9IGlt',
'cG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscDU0MSIsIHN0cih0ZXApKQpscCA9IGltcG9ydGxpYi51',
'dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9kdWxlKGxwKQpzaWcgPSBpbnNwZWN0LnNp',
'Z25hdHVyZShscC5fZ2l0X3dpbmRvd3MpCmdoaSgidGhhbV9zb19fZ2l0X3dpbmRvd3MiLCBsaXN0KHNpZy5wYXJhbWV0ZXJz',
'KSkKaW5uKCIgIHRoYW0gc28gY3VhIF9naXRfd2luZG93czoiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKCmRlZiBnb2koKipr',
'dyk6CiAgICAiIiJHb2kgX2dpdF93aW5kb3dzLCBCQVQgc3RkZXJyIGRlIG1vdCBkb25nIGNoYW4gZG9hbiBraG9uZyBnaWV0',
'IGx1b3QgZG8uIiIiCiAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihl',
'KToKICAgICAgICByID0gbHAuX2dpdF93aW5kb3dzKCoqa3cpCiAgICByZXR1cm4gciwgZS5nZXR2YWx1ZSgpCgojIC0tLSBk',
'b2kgY2h1bmcgcmlnOiBwaGFpIHRyYSBsb2kgZHVuZyBtb3QgY2EgdGEgQklFVCBUUlVPQyBkYXAgYW4gLS0tCndpdGggdGVt',
'cGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgIG5nb2FpID0gUGF0aCh0KS8ibmdvYWkiOyBuZ29haS5ta2Rp',
'cigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAo',
'bmdvYWkvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIxLCBfID0gZ29pKHBhdGg9',
'c3RyKG5nb2FpKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIChjdy8iZ2l0LmV4ZSIpLndyaXRl',
'X3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjIsIF8gPSBnb2kocGF0aD1zdHIoY3cpLCBwcm9ncmFtX2ZpbGVz',
'PXN0cihwZiksIGN3ZD1zdHIoY3cpKQpyaWdfb2sgPSBib29sKHIxKSBhbmQgcjIgaXMgTm9uZQpnaGkoInJpZ19kb2lfY2h1',
'bmciLCByaWdfb2spCmtldCgiUklHIGRvaSBjaHVuZyAoYmlldCB0cnVvYyBkYXAgYW4pIiwgREFUIGlmIHJpZ19vayBlbHNl',
'IEtERCwKICAgIGYibmdvYWktY3dkLT57J05IQU4nIGlmIHIxIGVsc2UgJ05vbmUnfSB8IHRyb25nLWN3ZC0+eydOSEFOJyBp',
'ZiByMiBlbHNlICdOb25lJ30iKQppZiBub3QgcmlnX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiByaWcg',
'c2FpLCBtb2kgY2hvdCBkdW9pIHNlIHZvIG5naGlhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0gTU9JIENPTkcgUEhBSSBUVSBD',
'SFVORyBNSU5IIE5PIENPIFRIRSBETyAtLS0KIyBCYWkgaG9jIGRhdCBuaGF0IGN1YSBwYWNrZXQgbmF5OiBkb19uMTAgYmFu',
'IGN1IGNoYW0gREFUIGNobyA5NTgzMTY4NSB0cm9uZyBraGkgdDE3MQojIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8gdmkgZHVu',
'ZyBraHV5ZXQgdGF0IG1hIE4xMCBzaW5oIHJhIGRlIGJhdC4gTm8gZGVnZW5lcmF0ZSDigJQKIyB0cmVuIFdpbmRvd3Mgb3Mu',
'cGF0aHNlcCBEQSBsYSAnOycgbmVuICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIGN1bmcga2V0IHF1YS4KIyBNb3Qg',
'Y29uZyBraG9uZyB0aGUgRE8gdGhpIGtob25nIHBoYWkgY29uZywgdmEgbm8gbmd1eSBoaWVtIGhvbiBraG9uZyBjbyBjb25n',
'OiBubwojIHBoYXQgcmEgbW90IGNodSBEQVQuCiMKIyBOZW4gdHJ1b2Mga2hpIERVTkcgbmFtIGNvbmcgbmF5IGRlIHBoYW4g',
'cXV5ZXQsIGJhdCB0dW5nIGNvbmcgZ2lldCBtb3QgZG90IGJpZW4gZGEKIyBiaWV0IHRyb25nLiBDb25nIG5hbyBraG9uZyBn',
'aWV0IGR1b2MgdGhpIGNodSBEQVQgY3VhIG5vIGJpIEhBIHh1b25nIEtIT05HIERPIERVT0M7CiMgVFJVT1QgZ2l1IG5ndXll',
'biAocXVhbiBzYXQgdHJ1YyB0aWVwLCB2ZC4gZzEgdmFuIG5oYW4gZ2l0LmJhdCkuIERvdCBiaWVuIGNoYXkgdHJlbiBCQU4g',
'U0FPIFRBTTsgY2F5IHRoYXQga2hvbmcgYmkKIyBkdW5nIHRvaSAoY3VuZyBreSBsdWF0IG5odSBONykuCkRPVF9CSUVOX1RV',
'X0tJRU0gPSBbCiAgICAoIk44IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAnaWYgY2hpX2RpbmggYW5kIFBhdGgo',
'Y2hpX2RpbmgpLm5hbWUubG93ZXIoKSA9PSAiZ2l0LmV4ZSIgYW5kIGhvcF9sZShjaGlfZGluaCk6JywKICAgICAiaWYgY2hp',
'X2RpbmggYW5kIGhvcF9sZShjaGlfZGluaCk6IiksCiAgICAoIk45IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAi',
'ZCA9IGRfcmF3LnN0cmlwKCkuc3RyaXAoJ1wiJykiLCAiZCA9IGRfcmF3LnN0cmlwKCkiKSwKICAgICgiTjEwIiwgIm9wcy9s',
'ZWFzZV9wdWJsaXNoLnB5IiwKICAgICAic2VwID0gb3MucGF0aHNlcCBpZiBwaGFuX2NhY2ggaXMgTm9uZSBlbHNlIHBoYW5f',
'Y2FjaCIsICJzZXAgPSBvcy5wYXRoc2VwIiksCiAgICAoIk4xMSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsICJpZiBjaGFu',
'X2RvYW4gaXMgbm90IE5vbmU6IiwgImlmIEZhbHNlOiIpLAogICAgKCJOMTIiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5w',
'eSIsCiAgICAgJ2dpdF9wYXRoPSIvL2tob25nLWNvL2dpdCInLCAnZ2l0X3BhdGg9Ii9raG9uZy1jby9naXQiJyksCl0KaW5u',
'KCIiKTsgaW5uKCIgIHR1IGtpZW0gY29uZyDigJQgbW9pIGNvbmcgcGhhaSBnaWV0IGR1b2MgbW90IGRvdCBiaWVuIGRhIGJp',
'ZXQ6IikKZ2lldCA9IHt9CmZvciBtYSwgZHVvbmcsIHRpbSwgdGhheSBpbiBET1RfQklFTl9UVV9LSUVNOgogICAgX3Rlbiwg',
'X2hhbSA9IG5leHQoKChhLCBiKSBmb3IgYSwgYiBpbiBQUk9CRSBpZiBhLnN0YXJ0c3dpdGgobWEgKyAiICIpKSwgKE5vbmUs',
'IE5vbmUpKQogICAgaWYgX2hhbSBpcyBOb25lOgogICAgICAgIGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHttYTo0fSBL',
'SE9ORyBETyBEVU9DOiBraG9uZyB0aW0gdGhheSBwcm9iZSB0ZW4gJ3ttYX0gLi4uJyIpOyBjb250aW51ZQogICAgdHJ5Ogog',
'ICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgX3Q6CiAgICAgICAgICAgIF9jID0gUGF0aChf',
'dCkvImNheSI7IHNodXRpbC5jb3B5dHJlZShnb2MvIm9wcyIsIF9jLyJvcHMiKQogICAgICAgICAgICBfZiA9IF9jL2R1b25n',
'OyBfbmQgPSBfZi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgaWYgX25kLmNvdW50KHRpbSkgIT0g',
'MToKICAgICAgICAgICAgICAgIGdpZXRbbWFdID0gTm9uZQogICAgICAgICAgICAgICAgaW5uKGYiICAgIHttYTo0fSBLSE9O',
'RyBETyBEVU9DOiBtYXUgZG90IGJpZW4ga2hvcCB7X25kLmNvdW50KHRpbSl9IGxhbiAobW9uZyAxKSIKICAgICAgICAgICAg',
'ICAgICAgICBmIiDigJQgbWEgbmd1b24gZGEgZG9pLCBkb3QgYmllbiBuYXkgaGV0IHkgbmdoaWEiKTsgY29udGludWUKICAg',
'ICAgICAgICAgX2Yud3JpdGVfdGV4dChfbmQucmVwbGFjZSh0aW0sIHRoYXksIDEpLCBlbmNvZGluZz0idXRmLTgiKQogICAg',
'ICAgICAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfZGJfIiArIG1hLCBzdHIo',
'X2MvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgICAgICAgICAgX20gPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJv',
'bV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX20pCiAgICAgICAgICAgIGRlZiBfZ29pX2RiKCoqa3cpOgog',
'ICAgICAgICAgICAgICAgX2UgPSBpby5TdHJpbmdJTygpCiAgICAgICAgICAgICAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJl',
'Y3Rfc3RkZXJyKF9lKToKICAgICAgICAgICAgICAgICAgICByZXR1cm4gX20uX2dpdF93aW5kb3dzKCoqa3cpLCBfZS5nZXR2',
'YWx1ZSgpCiAgICAgICAgICAgIF90dCwgX2N0LCBfID0gX2hhbShfZ29pX2RiLCBpbnNwZWN0LnNpZ25hdHVyZShfbS5fZ2l0',
'X3dpbmRvd3MpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5w',
'eSIpCiAgICAgICAgZ2lldFttYV0gPSAoX3R0ID09IFRSVU9UKQogICAgICAgIGlubihmIiAgICB7bWE6NH0gZG90IGJpZW4g',
'LT4ge190dDoxNH0geydHSUVUIERVT0MnIGlmIF90dCA9PSBUUlVPVCBlbHNlICdTT05HIFNPVCd9IgogICAgICAgICAgICAr',
'IChmIiAgICh7X2N0fSkiIGlmIF9jdCBlbHNlICIiKSkKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgX2U6CiAgICAgICAgZ2ll',
'dFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IHt0eXBlKF9lKS5fX25hbWVfX306IHtfZX0i',
'KQpnaGkoImNvbmdfZ2lldF9kdW9jX2RvdF9iaWVuIiwgZ2lldCkKCmZvciB0ZW4sICh0dCwgY3QsIGRsKSBpbiBbKHQsIGYo',
'Z29pLCBzaWcsIHRlcHQpKSBmb3IgdCwgZiBpbiBQUk9CRV06CiAgICBnaGkoInByb2JlXyIgKyB0ZW4uc3BsaXQoKVswXS5s',
'b3dlcigpLCBkbCkKICAgIGlmIGlzaW5zdGFuY2UoZGwsIGRpY3QpOgogICAgICAgIGZvciBrLCB2IGluIGRsLml0ZW1zKCk6',
'IGlubihmIiAgICB7azozNH06IHt2fSIpCiAgICBtYSA9IHRlbi5zcGxpdCgpWzBdCiAgICBpZiBnaWV0LmdldChtYSkgaXMg',
'bm90IFRydWUgYW5kIHR0ID09IERBVDoKICAgICAgICAjIERBVCB0dSBtb3QgY29uZyBjaHVhIGNodW5nIG1pbmggZHVvYyBs',
'YSBiaWV0IERPIHRoaSBraG9uZyBkYW5nIHRpbiBob24gS0RELgogICAgICAgIGtldCh0ZW4sIEtERCwgZiJjb25nIEtIT05H',
'IGdpZXQgZHVvYyBkb3QgYmllbiBjdWEgY2hpbmggbm8gKHtnaWV0LmdldChtYSkhcn0pIgogICAgICAgICAgICAgICAgICAg',
'ICAgZiIgLT4gY2h1IERBVCBuYXkga2hvbmcgY28gZ2lhIHRyaSIpCiAgICBlbHNlOgogICAgICAgIGtldCh0ZW4sIHR0LCBj',
'dCkKCiMgLS0tLS0tLS0tLS0tLS0tLSA0LiBONyBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIC0tLS0tLS0tLS0tLS0tLS0K',
'aWYgbm90IENISV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiNC4gTjcg4oCUIGRvdCBiaWVuIHRy',
'ZW4gQkFOIFNBTyBUQU0gKGNheSB0aGF0IEtIT05HIGJpIGR1bmcgdG9pKSIpCiAgICB0cnVvYyA9IHRlcC5yZWFkX3RleHQo',
'ZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTikKICAgIGdoaSgibjdfdHJ1b2MiLCB0cnVvYyk7IGlubihmIiAgc28g',
'ZG9uZyBraG9wIHtNQVVfV0lOIXJ9OiBUUlVPQyA9IHt0cnVvY30gW21vbmcgMV0iKQogICAgaWYgdHJ1b2MgIT0gMToKICAg',
'ICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsIGYibWF1IHh1YXQgaGllbiB7dHJ1b2N9IGxhbiwg',
'a2hvbmcgcGhhaSAxIikKICAgIGVsc2U6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0',
'bXA6CiAgICAgICAgICAgIHNhbyA9IFBhdGgodG1wKS8iY2F5IgogICAgICAgICAgICBzaHV0aWwuY29weXRyZWUoZ29jLCBz',
'YW8sIGlnbm9yZT1zaHV0aWwuaWdub3JlX3BhdHRlcm5zKCIuZ2l0IiwgIl9fcHljYWNoZV9fIiwgIioucHljIikpCiAgICAg',
'ICAgICAgIGYyID0gc2FvLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IgogICAgICAgICAgICBmMi53cml0ZV90ZXh0KGYyLnJl',
'YWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5yZXBsYWNlKE1BVV9XSU4sICJpZiBGYWxzZToiKSwgZW5jb2Rpbmc9InV0Zi04',
'IikKICAgICAgICAgICAgc2F1ID0gZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4pOyBnaGko',
'Im43X3NhdSIsIHNhdSkKICAgICAgICAgICAgaW5uKGYiICBTQVUgKGRhIGRvdCBiaWVuKSA9IHtzYXV9IFttb25nIDBdIikK',
'ICAgICAgICAgICAgaWYgc2F1ICE9IDA6CiAgICAgICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3Mi',
'LCBLREQsICJkb3QgYmllbiBLSE9ORyBhcCBkdW9jIikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHJjX20s',
'IG91dF9tID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgc2FvKQogICAgICAgICAgICAgICAgbTE2NSA9',
'IG1hdV9jYShvdXRfbSwgInQxNjUiKTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20pCiAgICAgICAgICAgICAgICB0ZW4xNjUg',
'PSBuZXh0KCh0IGZvciB0IGluIGRtIGlmIHQuc3RhcnRzd2l0aCgidDE2NSIpKSwgTm9uZSkKICAgICAgICAgICAgICAgIGx5',
'ID0gKGRtLmdldCh0ZW4xNjUpIG9yICIiKQogICAgICAgICAgICAgICAgZ2hpKCJuN190MTY1IiwgbTE2NSk7IGdoaSgibjdf',
'bHlfZG8iLCBseVs6MjAwXSkKICAgICAgICAgICAgICAgIGlubihmIiAgdDE2NSBzYXUgZG90IGJpZW46IHttMTY1fSB8IHts',
'eVs6MTEwXX0iKQogICAgICAgICAgICAgICAgZHVuZ19seV9kbyA9ICJQQVRIIHQiIGluIGx5IG9yICIvdXNyL2JpbiIgaW4g',
'bHkKICAgICAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIERBVCBpZiAobTE2NSA9PSAiRE8i',
'IGFuZCBkdW5nX2x5X2RvKSBlbHNlCiAgICAgICAgICAgICAgICAgICAgKFRSVU9UIGlmIG0xNjUgPT0gIkRPIiBlbHNlIEtE',
'RCksCiAgICAgICAgICAgICAgICAgICAgImdpZXQgZHVuZyBseSBkbyIgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9k',
'bykKICAgICAgICAgICAgICAgICAgICBlbHNlICgiRE8gbmh1bmcgS0hPTkcgZHVuZyBseSBkbyAtPiB0aW4gZHVuZyBnaWEi',
'IGlmIG0xNjUgPT0gIkRPIiBlbHNlICJraG9uZyBkb2MgZHVvYyB0MTY1IikpCgojIC0tLS0tLS0tLS0tLS0tLS0gS0VUIExV',
'QU4gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIj0iICogNzgpCmlubihmIlRIRSBIRSBETyBEVU9DOiB7dGhlX2hl',
'fSAgIEhFQUQ9e2hlYWRbOjEyXX0iKQojIEtob2kgZGFuIGNobyByZXZpZXdlciBiYXQgZGF1IG8gZG9uZyB0cmVuLCBuZW4g',
'Q0hFIERPIHBoYWkgbmFtIE5HQVkgZHVvaSBubzoga2hvbmcgY28gZG9uZyBuYXkKIyB0aGkgbW90IGx1b3QgLS1jaGktcHJv',
'YmUgaW4gIkRBVCA3IHwgVFJVT1QgMCB8IEtIT05HIERPIERVT0MgMCIgcmM9MCBtYSBraG9uZyBub2kgbGEgY2h1YSBjaGF5',
'IGJvIHRlc3QuCmdoaSgiY2hlX2RvIiwgImNoaS1wcm9iZSIgaWYgQ0hJX1BST0JFIGVsc2UgImRheS1kdSIpCmlmIENISV9Q',
'Uk9CRToKICAgIGlubigiLS1jaGktcHJvYmU6IENISSBkbyBtdWMgMCwgMSwgMy4gQm8gdGVzdCwgTjEtTjQsIHQxMzYsIE43',
'IEtIT05HIGNoYXkgLSBkYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCmlmIHRoZV9oZSA9PSAiZzEiOgog',
'ICAgaW5uKCJMVVUgWTogZGF5IGxhIE5FTiBETyAoZzEpLCBLSE9ORyBwaGFpIG5naGllbSB0aHUgZzIuIENhYyBjaG90IE44',
'LU4xMiBkdW9pIGRheSIpCiAgICBpbm4oIiAgICAgICBUUlVPVCBsYSBEVU5HIE5IVSBNT05HIOKAlCBjaHVuZyBsYSBuaHVu',
'ZyBsbyBnMiBzaW5oIHJhIGRlIHbDoS4iKQppbm4oIi0iICogNzgpCmZvciB0ZW4sIHR0LCBjdCBpbiBjaG90OgogICAgaW5u',
'KGYiICB7dHQ6MTR9IHt0ZW59IiArIChmIiAgIHtjdH0iIGlmIGN0IGVsc2UgIiIpKQpuX2tkZCA9IHN1bSgxIGZvciBfLCB0',
'LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCm5fdHJ1b3QgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJV',
'T1QpCmlubigiLSIgKiA3OCkKaW5uKGYiICBEQVQge3N1bSgxIGZvciBfLHQsXyBpbiBjaG90IGlmIHQ9PURBVCl9IHwgVFJV',
'T1Qge25fdHJ1b3R9IHwgS0hPTkcgRE8gRFVPQyB7bl9rZGR9IikKaW5uKGYiICBUb25nIGNhIGRvOiB7c28uZ2V0KCdzb19j',
'YV9kbycpfSB8IGRhbmggc2FjaCBkYXkgZHU6IHsnQ08nIGlmIHNvLmdldCgnbGlldF9rZV9kYXlfZHUnKSBlbHNlICdLSE9O',
'RyBETyBEVU9DJ30iKQppbm4oZiIgIEFkbWluaXN0cmF0b3I6IHtzby5nZXQoJ3F1eWVuX2FkbWluJyl9IHwgc3ltbGluazog',
'e3NvLmdldCgnc3ltbGlua19kdW9jJyl9IikKaW5uKCIiKTsgaW5uKCItLS0gREFOIE5HVVlFTiBLSE9JIEpTT04gTkFZIFZF',
'IENITyBSRVZJRVdFUiAtLS0iKQpnaGkoImNob3QiLCBbeyJ0ZW4iOiBhLCAidHJhbmdfdGhhaSI6IGIsICJjaGlfdGlldCI6',
'IGN9IGZvciBhLCBiLCBjIGluIGNob3RdKQppbm4oanNvbi5kdW1wcyhzbywgZW5zdXJlX2FzY2lpPUZhbHNlLCBpbmRlbnQ9',
'MSwgZGVmYXVsdD1zdHIpKQojIHJjOiAwID0gbW9pIGNob3QgREFUIHwgMSA9IGNvIGNob3QgVFJVT1QgfCAzID0gY28gY2hv',
'dCBLSE9ORyBETyBEVU9DICh1dSB0aWVuIGJhbyBkb25nKQpzeXMuZXhpdCgzIGlmIG5fa2RkIGVsc2UgKDEgaWYgbl90cnVv',
'dCBlbHNlIDApKQo='
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
