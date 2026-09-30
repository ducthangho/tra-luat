# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
# Luot DAY DU can SAN mot python >= 3.9 CO PyYAML (pip install pyyaml): ban nhung python.org ma tep nay tu tai
# KHONG co PyYAML/pip, nen no chi du cho -ChiKichThuoc / -ChiProbe. Thieu thi dung o buoc cong cu, rc=3.
# Luot DAY DU con can `bash` (Git Bash), `actionlint` >= 1.7.7 (ban ghim CI), `shellcheck` (nhan --norc) tren PATH: tep nay
# KHONG tu cai chung; bo do hoi ngay o muc 0 va dung rc=3 neu thieu (khong doi het bo test moi biet).
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
$ShaBoDo    = '021e240ea6ebe05fbade1d8605671a4529c8d9b681cb3ad315668dfc5e0159fa'      # SHA-256 cua bo do Python nhung ben duoi

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
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0wOS0zMGwiICAgICAgICAgICAgICAj'
'IGRvaSBNT0kga2hpIHN1YSBibyBkbyAtIGxvZyB0dSBraGFpIGJhbiBuYW8KVFJBTl9URVAsIFRSQU5fRE9ORyA9IDIsIDQw'
'MCAgICAgICAgICAjIE43JyBjdWEgc3BlYyByMwpBTF9TQU4gPSAoMSwgNywgNykgICAgICAgICAgICAgICAgICAgICMgc2Fu'
'IGFjdGlvbmxpbnQgPSBiYW4gZ2hpbSBDSTogQUxfVkVSIGN1YSBjaS55bWwgPSBiYW5fZ2hpbSBjdWEgb3BzL2NvbmdfY3Uu'
'eWFtbApNQVVfV0lOICA9ICdpZiBuZW5fdGh1YyA9PSAid2luZG93cyI6JwojIFdyaXRlIHNldCBjdWEgcGFja2V0ICM1NDEg'
'ZzIuIERpZmYga2hvbmcgY2hhbSB0ZXAgbmFvIG8gZGF5ID0+IGRvIE5IQU0gTkhBTkguCldSSVRFX1NFVF9HMiA9IHsib3Bz'
'L2xlYXNlX3B1Ymxpc2gucHkiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJ9CiMgIlR1b2kiIGNoaSBjbyBuZ2hpYSBr'
'aGkgc28gdm9pIE1BWSBDSFUgVEhBVC4gTW90IG1pcnJvciBjdWMgYm8gY3UgY3VuZyB0cmEgbHMtcmVtb3RlID09CiMgb3Jp'
'Z2luL21hc3RlciAoZG8gZHVvYzogbWFzdGVyIGMxNmJkMzIgLT4gInZlIG5lbiBUVU9JIiwgNDYgdGVwIC8gKzcxMTggY2hv'
'IDBlYTk1ZGUpLgojIERhbmggc2FjaCBDSE8gUEhFUDsgYHJlbW90ZSBnZXQtdXJsYCBkYSBraGFpIHRyaWVuIGluc3RlYWRP'
'ZiBuZW4gY2h1eWVuIGh1b25nIGN1bmcgbG8gcmEuClVSTF9LSE9fSE9QX0xFID0geyJodHRwczovL2dpdGh1Yi5jb20vZHVj'
'dGhhbmdoby90cmEtbHVhdCIsICJodHRwczovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdC5naXQiLAogICAgICAg'
'ICAgICAgICAgICAjIFNTSCB0b2kgQ1VORyBraG8gKHNhdSBfdXJsX3NhY2gpOiBgdXJsLiJnaXRAZ2l0aHViLmNvbToiLmlu'
'c3RlYWRPZiAiaHR0cHM6Ly9naXRodWIuY29tLyJgCiAgICAgICAgICAgICAgICAgICMgcmF0IHBobyBiaWVuIG8gbWF5IGRl'
'djsgdGhpZXUgaGFpIGRhbmcgbmF5IHRoaSBraG8gVEhBVCBiaSBiYW8gIktIT05HIHBoYWkga2hvIHRoYXQiLgogICAgICAg'
'ICAgICAgICAgICAic3NoOi8vZ2l0aHViLmNvbS9kdWN0aGFuZ2hvL3RyYS1sdWF0IiwgInNzaDovL2dpdGh1Yi5jb20vZHVj'
'dGhhbmdoby90cmEtbHVhdC5naXQiLAogICAgICAgICAgICAgICAgICAiZ2l0QGdpdGh1Yi5jb206ZHVjdGhhbmdoby90cmEt'
'bHVhdCIsICJnaXRAZ2l0aHViLmNvbTpkdWN0aGFuZ2hvL3RyYS1sdWF0LmdpdCJ9CiMgYHJlbW90ZSBnZXQtdXJsYCBLSEFJ'
'IFRSSUVOIGluc3RlYWRPZiwgbWEgbWF1IGB1cmwuImh0dHBzOi8vPHRva2VuPkBnaXRodWIuY29tLyIuaW5zdGVhZE9mYCBy'
'YXQgcGhvCiMgYmllbi4gSW4vZ2hpIG5ndXllbiB2YW4gbGEgZHVhIFRPS0VOIHZhbyBsb2cgdmEgdmFvIGtob2kgSlNPTiBw'
'czEgYmFvIGRhbiBjaG8gcmV2aWV3ZXIgKGRvIGR1b2M6CiMgMyBkb25nIHRyb25nIGtob2kgZGFuKS4gQm8gdXNlcmluZm8g'
'VFJVT0Mga2hpIGluIHZhIFRSVU9DIGtoaSBzbyDigJQgdG9rZW4gdmFuIGxhIEdpdEh1YiB0aGF0LgojIEF1dGhvcml0eSBr'
'ZXQgdGh1YyBvIGAvYCwgYD9gIGhvYWMgYCNgIERBVSBUSUVOIOKAlCBkdW5nIGx1YXQgZ2l0L2N1cmwuIEJhbiBgW14vXSpA'
'YCBudW90IGNhIGA/YC9gI2AKIyBuZW4gbW90IFVSTCB0cm8gdG9pIE1BWSBLSEFDIChob3N0IGR1bmcgdHJ1b2MgYD9gLCBk'
'dW9pIGA/YCBsYSBgQGdpdGh1Yi5jb20vPGtobz5gKSBkdW9jICJsYW0gc2FjaCIKIyB0aGFuaCBkdW5nIG1vdCBtdWMgQ0hP'
'IFBIRVAsIHRyb25nIGtoaSBnaXQgbm9pIHRvaSBtYXkga2lhIChkbyBkdW9jOiBtaXJyb3IgY3UgcGh1YyB2dSBxdWEgSFRU'
'UFMgPT4KIyAidmUgbmVuIFRVT0kiLCBUUlVPVCA0NiB0ZXAgLyArNzExOCkuIFZhbiBibyB0b2kgYEBgIENVT0kgdHJvbmcg'
'YXV0aG9yaXR5OiB1c2VyaW5mbyBjbyBgQGAgdHJhbiB0aGkKIyBjdXJsIHR1IGNob2kgKCJCYWQgaG9zdG5hbWUiKSwgY29u'
'IGtoaSBpbiB0aGkga2hvbmcgbG8gcGhhbiBzYXUgYEBgIHRodSBuaGF0LgpfUlhfVVNFUklORk8gPSByZS5jb21waWxlKHIi'
'XihbQS1aYS16XVtBLVphLXowLTkrLi1dKjovLylbXi8/I10qQCIpCmRlZiBfdXJsX3NhY2godSk6IHJldHVybiBfUlhfVVNF'
'UklORk8uc3ViKHIiXDEiLCB1IG9yICIiKSAgICAgICAgICAjIGRlIFNPIChsdWF0IGdpdC9jdXJsKQojIElOIHBoYWkgY2hl'
'IFJPTkcgaG9uIFNPOiBtYXQga2hhdSBjbyBgP2AvYCNgIFRSQU4gdGhpIGBbXi8/I10qQGAga2hvbmcga2hvcCBuZW4gVVJM'
'IHJhIGxvZyBOR1VZRU4gVkFOCiMgKGRvIGR1b2MgdHJlbiAyMDI2LTA5LTMwYjogMyBkb25nIG8gLS1jaGkta2ljaC10aHVv'
'YywgMyBkb25nIHRyb25nIGtob2kgZGFuIC0tY2hpLXByb2JlOyBiYW4gMzBhOiAwKS4KIyBDaGUgdG9pIGBAYCBDVU9JIENV'
'TkcgY3VhIENBIGNodW9pIChjbyBoYXkga2hvbmcgY28gc2NoZW1lKSwgdmEgREUgREFVIGAqKipAYCBkZSBiYW4gaW4ga2hv'
'bmcgdHUgbmhhbiBsYQojIGdpdGh1Yi5jb20ga2hpIGdpdCBub2kgdG9pIG1heSBraGFjICh2ZC4gaG9zdCB0cnVvYyBgP2Ap'
'LiBCYW4gMzBjIGNoZSAidG9pIGBAYCBjdW9pIHRydW9jIGAvYCBkYXUgdGllbiIKIyBuZW4gVkFOIGxvIGtoaSBtYXQga2hh'
'dSBjbyBgL2AgdHJhbiwgaG9hYyBVUkwgZGFuZyBzY3AgYHVzZXI6bWtAaG9zdDpkdW9uZ2AgKGtob25nIHNjaGVtZSkg4oCU'
'IGRvIHRyZW4KIyAyMDI2LTA5LTMwYzogMyBkb25nIC8gMSB0cm9uZyBraG9pIGRhbiAtLWNoaS1raWNoLXRodW9jLCA1IC8g'
'MyBvIC0tY2hpLXByb2JlLCBtb2kgZGFuZy4gTW9pIGt5IHR1IERVTkcKIyBsYSBtb3QgZHVvbmcgbnVhOyAidG9pIGBAYCBj'
'dW9pIiBraG9uZyBjb24ga3kgdHUgZHVuZyBuYW8uIEhhaSBxdXkgdGFjLCBoYWkgbXVjIGRpY2g6IFNPIHRoZW8gZ2l0LCBJ'
'TgojIHRoZW8gInRodWEgY29uIGhvbiBsbyIuICJDQSBjaHVvaSIgcGhhaSBkdW5nIGNhIGtoaSBjaHVvaSBjbyBYVU9ORyBE'
'T05HOiBnaXQoKSBkb2MgYmFuZyB0ZXh0PVRydWUgbmVuIENSL0xGIHRyb25nIFVSTAojIGRhIHRoYW5oIExGLCBtYSBgLmAg'
'a2hvbmcga2hvcCBMRi4gVG9rZW4gZG9jIHR1IHRlcCBDUkxGIChgaHR0cHM6Ly94LWFjY2Vzcy10b2tlbjo8dG9rZW4+YCAr'
'IENSICsgYEBnaXRodWIuY29tLy4uLmApCiMgdGhpIGJhbiAzMGUgS0hPTkcgY2hlIGdpOiBpbiBOR1VZRU4gdG9rZW4gbyBk'
'b25nIGBvcmlnaW4gOmAgdmEgbyAib3JpZ2luX3VybCIgdHJvbmcga2hvaSBKU09OIGRhbiAoZG8gdHJlbiAyMDI2LTA5LTMw'
'ZSkuCmRlZiBfdXJsX2luKHUpOiByZXR1cm4gcmUuc3ViKHIiXihbQS1aYS16XVtBLVphLXowLTkrLi1dKjovLyk/LipAIiwg'
'ciJcMSoqKkAiLCB1IG9yICIiLCBmbGFncz1yZS5TKQojIFRob25nIGJhbyBsb2kgY3VhIGdpdCBDSEkgYm8gdXNlcmluZm8g'
'dG9pIGBAYCBEQVUgVElFTjogdXNlcmluZm8gY28gYEBgIHRyYW4gKHZkLiB0ZW4gZGFuZyBuaGFwIGxhCiMgZW1haWwpIHRo'
'aSBwaGFuIHNhdSB2YW4gcmEgc3RkZXJyIGxzLXJlbW90ZSwgbWEgc3RkZXJyIGF5IGR1b2MgaW4gdmFvIGRvbmcgS0REIGN1'
'YSBONycgKGRvIGR1b2M6CiMgMiBkb25nIHRyb25nIGxvZywgMSB0cm9uZyBraG9pIGRhbikuIExhbSBzYWNoIE1PSSBVUkwg'
'dHJvbmcgdmFuIGJhbiB0cnVvYyBraGkgaW4g4oCUIGNoZSB0b2kgYEBgIENVT0kgdHJlbgojIERPTkcgKGN1bmcgbHVhdCBJ'
'TiB2b2kgX3VybF9pbjoga2hvbmcgY29uIGt5IHR1IGR1bmcgbmFvKS4gQmFuIDMwZCBkdW5nIG8gYFxzJyJgIG5lbiBwaGFu'
'IGdpdCBkZSBsYWkgY28KIyBgJ2AvYCJgL2tob2FuZyB0cmFuZyAodmQuIGB1QHg6cCc8YmkgbWF0PkBnaXRodWIuY29tYCkg'
'VkFOIGxvIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBkOiAyIGRvbmcgLyAxIHRyb25nCiMga2hvaSBkYW4gLS1jaGkta2ljaC10'
'aHVvYywgMyAvIDIgbyAtLWNoaS1wcm9iZSwgbW9pIGRhbmcuCmRlZiBfYW5fdXNlcmluZm8odCk6IHJldHVybiByZS5zdWIo'
'ciIoW0EtWmEtel1bQS1aYS16MC05Ky4tXSo6Ly8pW15cbl0qQCIsIHIiXDEqKipAIiwgdCBvciAiIikKIyBDYSBuZ29haSBw'
'aGFtIHZpIHIzIMKnbmdvYWlfcGhhbV92aSDigJQgZG8gQ0hJTkggU1BFQyBraGFpLCBraG9uZyBwaGFpIGJvIGRvIHR1IHF1'
'eWV0LgojIERvIGxhIERBTkggU0FDSCBDSE8gUEhFUDogY2EgZG8gbmFvIEtIT05HIG5hbSB0cm9uZyBkYXkgdmEgS0hPTkcg'
'cGhhaSAidGhpZXUgY29uZyBjdSIKIyB0aGkgbGEgVFJVT1QuIERhbmggc2FjaCBjYW0gdGhpIGJhbyBnaW8gY3VuZyB0aGll'
'dTsgZGFuaCBzYWNoIGNobyBwaGVwIHRoaSBiaWV0IHRydW9jLgpOR09BSV9QSEFNX1ZJID0gc2V0KCJ0MTMxIHQxMzIgdDE1'
'MCB0MTI1IHQzNSB0MzYgdDM3IHQzOCB0MzkgdDQwIi5zcGxpdCgpKQojIENhIGN1YSBDSElOSCBwYWNrZXQgbmF5LiBNb3Qg'
'Y2EgbyBkYXkgbWEgRE8gdGhpIGtob25nIGJhbyBnaW8gZHVvYyBibyBxdWEuCkNBX1BBQ0tFVCA9IHNldCgidDE2NSB0MTY2'
'IHQxNjcgdDE2OCB0MTY5IHQxNzAgdDE3MSB0MTcyIHQxNzMiLnNwbGl0KCkpCiMgQ2EgTU9JIG1hIGcyIHRoZW0gdmFvIChO'
'OC1OMTIpLiBEb2kgdHVvbmcgZG8gcGhhaSBNQU5HIGNodW5nIHZhbzogbWVyZ2UtYmFzZSBjaHVhIGNvLCBIRUFEIGNvLgpD'
'QV9NT0lfRzIgPSAidDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpCkNBMTUgID0gInQxMjkgdDEzMCB0MTMxIHQx'
'MzIgdDEzMyB0MTM2IHQxMzggdDEzOSB0MTQ0IHQxNDUgdDE0NiB0MTQ3IHQxNDkgdDE1MCB0MTUxIi5zcGxpdCgpCkNBTU9J'
'ID0gInQxNjUgdDE2NiB0MTY3IHQxNjgiLnNwbGl0KCkKCkRBVCwgVFJVT1QsIEtERCA9ICJEQVQiLCAiVFJVT1QiLCAiS0hP'
'TkcgRE8gRFVPQyIKc28sIGNob3QgPSB7fSwgW10KZGVmIGdoaShrLCB2KTogc29ba10gPSB2OyByZXR1cm4gdgpkZWYga2V0'
'KHRlbiwgdHJhbmdfdGhhaSwgY2hpX3RpZXQ9IiIpOgogICAgY2hvdC5hcHBlbmQoKHRlbiwgdHJhbmdfdGhhaSwgY2hpX3Rp'
'ZXQpKQogICAgaW5uKGYiICBbe3RyYW5nX3RoYWk6MTR9XSB7dGVufSIgKyAoZiIgICB7Y2hpX3RpZXR9IiBpZiBjaGlfdGll'
'dCBlbHNlICIiKSkKICAgIHJldHVybiB0cmFuZ190aGFpCgojIC0tLS0tLS0tLS0tLS0tLS0gZG9jIGxvZyBjdWEgYm8gdGVz'
'dCAoYmFuIDMsIGRhIGRvIHRyZW4gbG9nIFRIQVQpIC0tLS0tLS0tLS0tLS0tLS0KUlhfRE9fQ0hPICA9IHJlLmNvbXBpbGUo'
'ciIoP20pXiEhISBkbyAoXFMrKSAoLiopJCIpClJYX0RPX0NVT0kgPSByZS5jb21waWxlKHIiKD9tKV4gezJ9KFxTezEsNH0p'
'IHsyfShcUyspOiAoLiopJCIpClJYX0JPX1FVQSAgPSByZS5jb21waWxlKHIiKD9tKV4gezJ9XFN7MSw2fSBRVUEgKFxTKyk6'
'ICguKikkIikKIyBEb25nIHRvbmcga2V0IFRIQVQgbyBEQVUgZG9uZy4gQ2EgRE8gY28gdGhlIGluIGxhaSBzdGRvdXQgY3Vh'
'IG1vdCBsdW90IENPTiAodDE1NSBjaGF5IGxhaSB0MDEsIHQ3Mi90OTggY2hheQojICJibyIpIOKAlCBkb25nIHRvbmcgTE9O'
'RyBheSBuYW0gR0lVQSBkb25nIChkbzogMjAgZG9uZyBsb25nIGRldSBvIGdpdWEgZG9uZywgY2hpIGRvbmcgdG9uZyB0aGF0'
'IG8gZGF1IGRvbmcpLCBtYQojIGBzZWFyY2hgIGtob25nIG5lbyBiYXQgbm8gVFJVT0MuIERvIHRyZW4gMjAyNi0wOS0zMGMs'
'IDBlYTk1ZGUgKyBkb3QgYmllbiBsYW0gdDAxIERPOiBkb2MgcmEgIjAvMSIgPT4KIyAiZGFuaCBzYWNoIEtIT05HIGRheSBk'
'dSIsICJMRUNIIFNPIEhPQzogdGhpZXUgLTIwIGNhIiwgdHJvbmcga2hpIHRvbmcgdGhhdCAxNjYtMTQ1PTIxID09IDIxIGNh'
'IGRvYyBkdW9jLgpSWF9UT05HICAgID0gcmUuY29tcGlsZShyIig/bSlebGVhc2VfcHVibGlzaDogKFxkKykvKFxkKylcYlte'
'XG5dKj89KFxkKyksW15cbl0qPz0oXGQrKSIpCgpkZWYgc29fY2EodCk6CiAgICBtID0gcmUubWF0Y2gociJ0KFxkKykiLCB0'
'KTsgcmV0dXJuIChpbnQobS5ncm91cCgxKSkgaWYgbSBlbHNlIDEwKio2LCB0KQoKZGVmIGRvY19kbyhvdXQpOgogICAgdGFp'
'X2NobyA9IHt0OiBsLnN0cmlwKCkgZm9yIHQsIGwgaW4gUlhfRE9fQ0hPLmZpbmRhbGwob3V0KX0KICAgIGJvID0ge3QgZm9y'
'IHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0KX0KICAgIGN1b2kgPSB7dDogbC5zdHJpcCgpIGZvciBfLCB0LCBsIGlu'
'IFJYX0RPX0NVT0kuZmluZGFsbChvdXQpIGlmIHQgbm90IGluIGJvfQogICAgaG9wID0gZGljdChjdW9pKTsgaG9wLnVwZGF0'
'ZSh0YWlfY2hvKQogICAgZ2MsIHRpbiA9IFtdLCBUcnVlCiAgICBpZiBzZXQodGFpX2NobykgIT0gc2V0KGN1b2kpOgogICAg'
'ICAgIGdjLmFwcGVuZChmImhhaSBuZ3VvbiBMRUNIOiBjaGktdGFpLWNobz17c29ydGVkKHNldCh0YWlfY2hvKS1zZXQoY3Vv'
'aSkpfSBjaGktY3VvaT17c29ydGVkKHNldChjdW9pKS1zZXQodGFpX2NobykpfSIpCiAgICAgICAgdGluID0gRmFsc2UKICAg'
'IG0gPSBSWF9UT05HLnNlYXJjaChvdXQpCiAgICBpZiBub3QgbToKICAgICAgICBnYy5hcHBlbmQoIktIT05HIGRvYyBkdW9j'
'IGRvbmcgdG9uZyBrZXQiKTsgdGluID0gRmFsc2UKICAgIGVsc2U6CiAgICAgICAgZGF0LCB0cmVuID0gaW50KG0uZ3JvdXAo'
'MSkpLCBpbnQobS5ncm91cCgyKSkKICAgICAgICBnYy5hcHBlbmQoZiJzbyBob2M6IHt0cmVufS17ZGF0fT17dHJlbi1kYXR9'
'IGRvOyBkb2MgZHVvYyB7bGVuKGhvcCl9IikKICAgICAgICBpZiB0cmVuIC0gZGF0ICE9IGxlbihob3ApOgogICAgICAgICAg'
'ICBnYy5hcHBlbmQoZiJMRUNIIFNPIEhPQzogdGhpZXUge3RyZW4tZGF0LWxlbihob3ApfSBjYSIpOyB0aW4gPSBGYWxzZQog'
'ICAgcmV0dXJuIGhvcCwgZ2MsIHRpbgoKIyBNYXUgY28gZG9uZyB0b25nIExPTkcgZ2l1YSBkb25nIChkYW5nIHQxNTUgaW4g'
'bGFpIGx1b3QgY29uKTogYm8gZG9jIGJhdCBkb25nIHRvbmcgREFVIFRJRU4gbGEgdHUga2llbSBETy4KX01BVSA9ICgiISEh'
'IGRvIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1fUVVZRU4gYSAnbGVhc2VfcHVibGlzaDogMC8xIMSR4bqhdDsgxJHDoyBjaOG6'
'oXk9MSwgYuG7jyBxdWE9MCdcbiIKICAgICAgICAiISEhIGRvIHQxNTBfeCBXaW5FcnJvciAxMzE0IHJlcXVpcmVkIHByaXZp'
'bGVnZVxuIgogICAgICAgICIgIELhu44gUVVBIHQxMzFfeTogbmVuIGZpeHR1cmVcbiIKICAgICAgICAiICDEkOG7jiAgdDAy'
'Yl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTjogYVxuIgogICAgICAgICIgIMSQ4buOICB0MTUwX3g6IFdpbkVycm9yIDEzMTQg'
'cmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAgICAgImxlYXNlX3B1Ymxpc2g6IDEvMyDEkeG6oXQ7IMSRw6MgY2jhuqF5PTMs'
'IGLhu48gcXVhPTFcbiIpCgojIEJpZW4gUFlUSE9OKiBjdWEgbWF5IG5ndW9pIGRvIGxvdCB2YW8gYm8gdGVzdCBsYSBET0kg'
'SEFOSCBWSSBibyB0ZXN0OiBQWVRIT05PUFRJTUlaRSBibyBtb2kgYGFzc2VydGAgKGRvIHRyZW4KIyAyMDI2LTA5LTMwYzog'
'YGFzc2VydCBGYWxzZWAgcXVhLCByYz0wKTsgYmFuIDMwZCBjaGkgdHJ1bmcgaG9hIE1PVCBiaWVuIGF5LCBjb24gUFlUSE9O'
'REVWTU9ERT0xIGxhbSB0MTU0IERPIDIvNAojIGxhbiB0cmVuIDMuMTEgKHNhY2g6IDQvNCBRVUEpID0+IHJjPTEgIlRSVU9U'
'IE1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jIiBjaG8gdW5nIHZpZW4gc2FjaCAoZG8gdHJlbgojIDIwMjYtMDktMzBk'
'KS4gRGFuaCBzYWNoIENBTSBsdW9uIHRoaWV1IG1vdCBiaWVuIOKAlCBuZW4gZGF5IGxhIGRhbmggc2FjaCBDSE8gUEhFUDog'
'Y2hpIGdpdSBiaWVuIGRlIHRyaW5oIHRob25nCiMgZGljaCBDSEFZIHZhIHRpbSBnb2kgREEgQ0FJOyBQWVRIT05QQVRIIEtI'
'T05HIGdpdSAoQ0kga2hvbmcgY28gbm8pLiBQaGVwIGhvaSBkaWV1IGtpZW4gdGllbiBxdXlldCBvIG11YyAwCiMgY3VuZyBj'
'aGF5IHF1YSBkYXksIG5lbiBubyB0aGF5IERVTkcgbW9pIHRydW9uZyBtYSBibyB0ZXN0IHNlIHRoYXkuCl9QWV9HSVUgPSBm'
'cm96ZW5zZXQoeyJQWVRIT05IT01FIiwgIlBZVEhPTlVTRVJCQVNFIiwgIlBZVEhPTk5PVVNFUlNJVEUifSkKIyBDYXUgaGlu'
'aCBnaXQgQ1VBIE5HVU9JIERPIGxvdCB2YW8gYm8gdGVzdCB5IG5odSBiaWVuIFBZVEhPTio6IGNhIHRlc3QgZ29pIGdpdCBi'
'YW5nIGRpY3Qob3MuZW52aXJvbiksIG5lbiBkb2MgY2F1IGhpbmgKIyBjYSBuaGFuIHZhIGJpZW4gR0lUXyogY3VhIG1heSBk'
'by4gRG8gdHJlbiAyMDI2LTA5LTMwZSwgMGVhOTVkZTogYGluaXQuZGVmYXVsdEJyYW5jaCA9IG1haW5gID0+IDE2My8xNjYs'
'IHQxMzQgdDEzOSB0MTUxCiMgRE8gPT4gcmM9MSAiVFJVT1QgTW9pIGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MiIGNobyB1'
'bmcgdmllbiBzYWNoIChzYWNoOiAxNjYvMTY2KSDigJQgbyBwaGFtIHZpIGdsb2JhbCBMQU4gaGUgdGhvbmcuCiMgQm8gTU9J'
'IGJpZW4gR0lUXyogdmEgdGhheSBnbG9iYWwgQ0EgTkhBTiBiYW5nIGdsb2JhbCBDVUEgQ0kuIENJIEtIT05HIGNvIGdsb2Jh'
'bCByb25nOiBqb2IgYGdhdGVgIGN1YSBjaS55bWwgKGJ1b2MgIkZvcmNlIExGCiMgY2hlY2tvdXQiLCBjYSB1YnVudHUgbGFu'
'IHdpbmRvd3MpIGRhdCBnbG9iYWwgY29yZS5hdXRvY3JsZj1mYWxzZSwgY29yZS5lb2w9bGYsIGNvcmUuYWJicmV2PTcgVFJV'
'T0MgYnVvYyBjaGF5IGJvIHRlc3Qg4oCUCiMgdmkgKGNpLnltbDo3LTggdHUga2hhaSkga2hvbmcgdGF0IHRoaSBydW5uZXIg'
'V2luZG93cyBjaGVja291dCBDUkxGOiBhdXRvY3JsZj10cnVlIGN1YSBiYW4gY2FpIEdpdCBvIEhFIFRIT05HLiBCYW4gMzBm'
'CiMgZGF0IGdsb2JhbCA9IHJvbmcgbmVuIGJvIHRlc3QgdGhheSBhdXRvY3JsZj10cnVlIGNvbiBDSSB0aGF5IGZhbHNlOiBk'
'byB0cmVuIDIwMjYtMDktMzBmLCAwZWE5NWRlLCBoZSB0aG9uZyBhdXRvY3JsZj10cnVlCiMgKyBnbG9iYWwgbmh1IENJID0+'
'IGJhbiAzMGUgMTY2LzE2NiwgYmFuIDMwZiAxNjUvMTY2ICh0MTUwIERPIOKAlCBjaGkga2hvbmcgdGhhbmggVFJVT1Qgdmkg'
'dDE1MCB0aW5oIGNvIG5hbSB0cm9uZwojIE5HT0FJX1BIQU1fVkkpLiBHbG9iYWwgbGEgVEVQIFRBTSBjaHVhIERVTkcKIyBn'
'bG9iYWwgY3VhIENJIGNvbmcgaW5pdC5kZWZhdWx0QnJhbmNoIGdoaW0gdmUgbWFjIGRpbmggY3VhIGdpdCAoZGF0IGR1b2Mg'
'Y2EgbyBoZSB0aG9uZyk6IGdsb2JhbCBkZSBsZW4gaGUgdGhvbmcgbmh1IHRyZW4gQ0ksCiMgY29uIGNhdSBoaW5oIENVQyBC'
'TyBjdWEgZml4dHVyZSB2YW4gZGUgbGVuIGdsb2JhbCAoR0lUX0NPTkZJR19DT1VOVCB0aGkgZGUgbGVuIGNhIGN1YyBibyku'
'IERvaSBidW9jIGF5IHRyb25nIGNpLnltbCB0aGkKIyBkb2kgX0dJVF9HTE9CQUxfQ0kuIEdJVF9DT05GSUdfR0xPQkFMIGNo'
'aSB0aGF5IFRFUCBDT05GSUc6IGlnbm9yZS9hdHRyaWJ1dGVzIG1hYyBkaW5oICgkWERHX0NPTkZJR19IT01FIGhvYWMgfi8u'
'Y29uZmlnL2dpdC8KIyBpZ25vcmV8YXR0cmlidXRlcykgY3VhIG5ndW9pIGRvIFZBTiBhcCBjaG8gZ2l0IGNvbiAoZG8gdHJl'
'biAyMDI2LTA5LTMwZywgMGVhOTVkZTogfi8uY29uZmlnL2dpdC9pZ25vcmUgYCoueWFtbGAgPT4gYmFuIDMwZwojIDE1NC8x'
'NjYsIDExIGNhICJsYSIpOyBDSSBraG9uZyBjbyB0ZXAgbmFvIG8gZG8gPT4gWERHX0NPTkZJR19IT01FIHRybyB2YW8gdGh1'
'IG11YyBUQU0gUk9ORy4gQ29uIGxhaSAoa2hvYSBoZSB0aG9uZyBraGFjKQojIGxhIGdpb2kgaGFuIGRhIGJpZXQsIGtob25n'
'IHBoYWkgZGEgZG9uZy4KIyBDYXUgaGluaCBzaGVsbGNoZWNrIENVQSBOR1VPSSBETyBsb3QgdmFvIGJvIHRlc3QgeSBuaHUg'
'Z2l0OiB0MTM3IGdvaSBzaGVsbGNoZWNrIFRIQU5HLCB0MzMvdDEzNyBnb2kgYWN0aW9ubGludCAtPiBzaGVsbGNoZWNrLAoj'
'IGNhIGhhaSBkb2MgU0hFTExDSEVDS19PUFRTLCB2YSB0MTM3IGRvYyB+Ly5zaGVsbGNoZWNrcmMgKFhER19DT05GSUdfSE9N'
'RSB0YW0gS0hPTkcgY2hlIGR1b2M7IGNobyB0ZXAgcmMgdHJlbiBXaW5kb3dzOiBLSE9ORyBETyBEVU9DKS4KIyBEbyB0cmVu'
'IDIwMjYtMDktMzBoLCAwZWE5NWRlOiBTSEVMTENIRUNLX09QVFM9LS1lbmFibGU9YWxsID0+IHQzMyArIHQxMzcgRE87IH4v'
'LnNoZWxsY2hlY2tyYyBgZW5hYmxlPWFsbGAgPT4gdDEzNyBETyDigJQgY2EgImxhIgojID0+IFRSVU9UIGNobyB1bmcgdmll'
'biBzYWNoLiBDSSBraG9uZyBjbyBjYSBoYWkuIFNIRUxMQ0hFQ0tfT1BUUz0tLW5vcmMgZGUgbGVuIGJpZW4gY3VhIG5ndW9p'
'IGRvIFZBIHRhdCBtb2kgdGVwIHJjIChzaGVsbGNoZWNrCiMgcGhhaSBOSEFOIC0tbm9yYyDigJQgbXVjIDAgaG9pIHRydW9j'
'KS4gQkFTSF9FTlYgKGtlIGNhIGBzZXQgLWV1byBwaXBlZmFpbGApIGRvOiAxNjYvMTY2LCBraG9uZyBsb3QuCl9HSVRfR0xP'
'QkFMX0NJID0gIltpbml0XVxuXHRkZWZhdWx0QnJhbmNoID0gbWFzdGVyXG5bY29yZV1cblx0YXV0b2NybGYgPSBmYWxzZVxu'
'XHRlb2wgPSBsZlxuXHRhYmJyZXYgPSA3XG4iCmRlZiBjaGF5KGFyZ3YsIGN3ZCwgcGh1dD02MCk6CiAgICBmZCwgZ2MgPSB0'
'ZW1wZmlsZS5ta3N0ZW1wKHByZWZpeD0id3A1NDEtZ2l0Y29uZmlnLWNpLSIsIHN1ZmZpeD0iLmluaSIpCiAgICB4ZGcgPSBO'
'b25lCiAgICB0cnk6CiAgICAgICAgeGRnID0gdGVtcGZpbGUubWtkdGVtcChwcmVmaXg9IndwNTQxLXhkZy0iKQogICAgICAg'
'IHdpdGggb3MuZmRvcGVuKGZkLCAidyIsIGVuY29kaW5nPSJhc2NpaSIsIG5ld2xpbmU9IlxuIikgYXMgZjogZi53cml0ZShf'
'R0lUX0dMT0JBTF9DSSkKICAgICAgICBtdCA9IHtrOiB2IGZvciBrLCB2IGluIG9zLmVudmlyb24uaXRlbXMoKQogICAgICAg'
'ICAgICAgIGlmIG5vdCBrLnVwcGVyKCkuc3RhcnRzd2l0aCgiR0lUXyIpIGFuZCAobm90IGsudXBwZXIoKS5zdGFydHN3aXRo'
'KCJQWVRIT04iKSBvciBrLnVwcGVyKCkgaW4gX1BZX0dJVSl9CiAgICAgICAgbXQudXBkYXRlKFBZVEhPTlVURjg9IjEiLCBQ'
'WVRIT05JT0VOQ09ESU5HPSJ1dGYtOCIsIFBZVEhPTkRPTlRXUklURUJZVEVDT0RFPSIxIiwgUFlUSE9OVU5CVUZGRVJFRD0i'
'MSIsCiAgICAgICAgICAgICAgICAgIEdJVF9DT05GSUdfR0xPQkFMPWdjLCBYREdfQ09ORklHX0hPTUU9eGRnLCBTSEVMTENI'
'RUNLX09QVFM9Ii0tbm9yYyIpCiAgICAgICAgcCA9IHN1YnByb2Nlc3MucnVuKFtzeXMuZXhlY3V0YWJsZV0gKyBhcmd2LCBj'
'd2Q9c3RyKGN3ZCksIGNhcHR1cmVfb3V0cHV0PVRydWUsCiAgICAgICAgICAgICAgICAgICAgICAgICAgIHRleHQ9VHJ1ZSwg'
'ZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD1waHV0KjYwLCBlbnY9bXQpCiAgICBmaW5hbGx5'
'OgogICAgICAgIHRyeTogb3MucmVtb3ZlKGdjKQogICAgICAgIGV4Y2VwdCBPU0Vycm9yOiBwYXNzCiAgICAgICAgaWYgeGRn'
'OiBzaHV0aWwucm10cmVlKHhkZywgaWdub3JlX2Vycm9ycz1UcnVlKQogICAgcmV0dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rk'
'b3V0IG9yICIiKSArIChwLnN0ZGVyciBvciAiIikKCmRlZiBtYXVfY2Eob3V0LCB0KToKICAgIG0gPSByZS5zZWFyY2gociIo'
'P20pXjw8PCByYSAoIiArIHQgKyByIlthLXpdP19cUyopIFswLTkuXStzIChcdyspXHMqJCIsIG91dCkKICAgIHJldHVybiBt'
'Lmdyb3VwKDIpIGlmIG0gZWxzZSBOb25lCgpkZWYgZ2l0KGdvYywgKmEsIHBodXQ9NSk6CiAgICBwID0gc3VicHJvY2Vzcy5y'
'dW4oWyJnaXQiLCAiLUMiLCBzdHIoZ29jKSwgKmFdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsCiAgICAgICAg'
'ICAgICAgICAgICAgICAgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD1waHV0KjYwKQogICAg'
'cmV0dXJuIHAucmV0dXJuY29kZSwgKHAuc3Rkb3V0IG9yICIiKS5zdHJpcCgpLCAocC5zdGRlcnIgb3IgIiIpLnN0cmlwKCkK'
'CgojID09PT09PT09PT09PT09PT09IE5BTSBQUk9CRSwgdmlldCB0aGFuaCBIQU0gVEhVQU4gZGUgVFUgS0lFTSBkdW9jID09'
'PT09PT09PT09PT09PT09CiMgTW9pIGhhbSB0cmEgKHRyYW5nX3RoYWksIGNoaV90aWV0LCBkdV9saWV1KS4gS0hPTkcgaW4s'
'IEtIT05HIHRob2F0IOKAlCBuaG8gdmF5IGNodW5nCiMgY2hheSBkdW9jIHRyZW4gbmVuIEJBVCBLWSwgdmEgYC0tdHUta2ll'
'bS1wcm9iZWAgZ29pIHRoYW5nIGNodW5nIGRlIGtpZW0gY2hpbmggYm8gZG8uCgpkZWYgX3Nhbih0KToKICAgIGQgPSBQYXRo'
'KHQpLyJkIjsgZC5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBw'
'Zi5ta2RpcigpCiAgICByZXR1cm4gZCwgY3csIHBmCgpkZWYgZG9fbjgoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiQnVvYyAx'
'IChDT05HX0NVX0dJVCkgY2hpIGR1b2MgbmhhbiBnaXQuZXhlLiBEb2kgY2h1bmcgZHVvbmc6IGdpdC5leGUgVkFOIHBoYWkg'
'bmhhbi4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAg'
'ICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgZm9yIHRlbiBpbiAoImdpdC5leGUiLCAiZ2l0LmJhdCIsICJnaXQuY21k'
'IiwgImdpdC5weSIsICJraG9uZy1waGFpLWdpdC50eHQiKToKICAgICAgICAgICAgZiA9IGQvdGVuOyBmLndyaXRlX3RleHQo'
'IngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBfID0gZ29pKGNvbmdfY3VfZ2l0PXN0cihmKSwgcGF0aD0i'
'IiwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAga3FbZiJDT05HX0NVX0dJVD17dGVu'
'fSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiVFUgQ0hPSSIKICAgIGxvdCA9IFtrIGZvciBrLCB2IGluIGtxLml0ZW1zKCkgaWYg'
'diA9PSAiTkhBTiIgYW5kIG5vdCBrLmVuZHN3aXRoKCJnaXQuZXhlIildCiAgICBpZiBrcS5nZXQoIkNPTkdfQ1VfR0lUPWdp'
'dC5leGUiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBnaXQuZXhlIGhv'
'cCBsZSBtYSBiaSB0dSBjaG9pIiwga3EKICAgIHJldHVybiAoREFUIGlmIG5vdCBsb3QgZWxzZSBUUlVPVCksICgiIiBpZiBu'
'b3QgbG90IGVsc2UgZiJjb24gbmhhbjoge2xvdH0iKSwga3EKCmRlZiBkb19uOShnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJN'
'dWMgUEFUSCBib2MgbmhheSBrZXAgcGhhaSBOSEFOOyBtdWMgcm9uZyAvIHRvYW4ga2hvYW5nIHRyYW5nIHBoYWkgYm8gcXVh'
'LCBraG9uZyBuZW0uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6'
'CiAgICAgICAgZCA9IFBhdGgodCkvImNvIGdpdCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2Rpcigp'
'OyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVu'
'Y29kaW5nPSJ1dGYtOCIpCiAgICAgICAgZm9yIG5oYW4sIG11YyBpbiAoKCJraG9uZyBuaGF5Iiwgc3RyKGQpKSwgKCJjbyBu'
'aGF5IGtlcCIsIGYnIntkfSInKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAoInJvbmciLCAiIiksICgiY2hpIGtob2Fu'
'ZyB0cmFuZyIsICIgICAiKSk6CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIHIsIF8gPSBnb2kocGF0aD1tdWMs'
'IHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgICAgICBrcVtmIlBBVEgge25oYW59Il0g'
'PSAiTkhBTiIgaWYgciBlbHNlICJOb25lIgogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAg'
'ICAgICBrcVtmIlBBVEgge25oYW59Il0gPSBmIk5FTSB7dHlwZShlKS5fX25hbWVfX30iCiAgICBpZiBrcS5nZXQoIlBBVEgg'
'a2hvbmcgbmhheSIpICE9ICJOSEFOIjoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG11YyBQ'
'QVRIIHRodW9uZyBtYSBraG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICBvayA9IChrcS5nZXQoIlBBVEggY28gbmhheSBr'
'ZXAiKSA9PSAiTkhBTiIKICAgICAgICAgIGFuZCBrcS5nZXQoIlBBVEggcm9uZyIpID09ICJOb25lIiBhbmQga3EuZ2V0KCJQ'
'QVRIIGNoaSBraG9hbmcgdHJhbmciKSA9PSAiTm9uZSIpCiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIi'
'IGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgojIERhdSBwaGFuIGNhY2ggZHVuZyBERSBUSFUuIFBoYWkgS0hBQyBvcy5w'
'YXRoc2VwIHRyZW4gQ0EgSEFJIG5lbiAoJzsnIFdpbmRvd3MsICc6JyBQT1NJWCkKIyB0aGkgaGFpIGdpYSB0aHV5ZXQgInRh'
'Y2ggdGhlbyBkYXUgZHVvYyB0cnV5ZW4iIHZhICJ0YWNoIHRoZW8gb3MucGF0aHNlcCIgbW9pIHJvaSByYSBuaGF1LgpUSFVf'
'TjEwID0gInwiCgpkZWYgZG9fbjEwKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkhhbSBwaGFpIHRhY2ggUEFUSCB0aGVvIGRh'
'dSBwaGFuIGNhY2ggRFVPQyBUUlVZRU4sIGtob25nIHRoZW8gb3MucGF0aHNlcCBjdWEgbmVuLgoKICAgIEJhbiBjdSBkbyAi'
'bW90IGRhdSAnOycgdHJvbmcgVEVOIHRodSBtdWMiIHZhIGRhdCBEQVQgdHJlbiBXaW5kb3dzIGR1IGhhbSBzYWkuIE5vCiAg'
'ICBkZWdlbmVyYXRlOiB0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycsIG5lbiAnQzovYTtiJyB0aGF0IHN1IENP'
'IE5HSElBIGxhIGhhaQogICAgbXVjIOKAlCAidGFjaCBkdW5nIiB2YSAidGFjaCBzYWkiIGNobyByYSBjdW5nIGtldCBxdWEs'
'IHBoZXAgZG8ga2hvbmcgdGhlIGRvIG5hby4gTm8KICAgIGRhIGNoYW0gREFUIGNobyA5NTgzMTY4NSB0cm9uZyBraGkgdDE3'
'MSBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1bmcga2h1eWV0IHRhdCBheS4KICAgIE1vdCBjb25nIGtob25nIHRoZSBk'
'byB0aGkga2hvbmcgcGhhaSBjb25nLgogICAgIiIiCiAgICB0ZW5fc2VwID0gbmV4dCgoayBmb3IgayBpbiAoInBoYW5fY2Fj'
'aCIsICJkYXVfcGhhbl9jYWNoIiwgInNlcCIpIGlmIGsgaW4gc2lnLnBhcmFtZXRlcnMpLCBOb25lKQogICAgaWYgdGVuX3Nl'
'cCBpcyBOb25lOgogICAgICAgICMgS2hvbmcgY28gdGhhbSBzbyB0aGkgdHJlbiBXaW5kb3dzIEtIT05HIGNvbiBkdW9uZyBu'
'YW8gdGFjaCBoYWkgZ2lhIHRodXlldC4KICAgICAgICBpZiBvcy5wYXRoc2VwID09ICI7IjoKICAgICAgICAgICAgcmV0dXJu'
'IChLREQsICJ0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgdmEgaGFtIGtob25nIG5oYW4gdGhhbSBzbyBkYXUg'
'cGhhbiBjYWNoICIKICAgICAgICAgICAgICAgICAgICAgICAgICItPiBraG9uZyB0YWNoIGR1b2MgaGFpIGdpYSB0aHV5ZXQi'
'LAogICAgICAgICAgICAgICAgICAgIHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IE5vbmV9KQog'
'ICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICAgICAgbGEgPSBQYXRoKHQp'
'LyJjbztkYXUiOyBsYS5ta2RpcigpCiAgICAgICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAgICAgKGQvImdp'
'dC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyAgPSBnb2kocGF0aD1z'
'dHIobGEpICsgb3MucGF0aHNlcCArIHN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAg'
'ICAgICAgcjAsIF8gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAg'
'ICAga3EgPSB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiBOb25lLAogICAgICAgICAgICAgICJj'
'byBtdWMgY2h1YSAnOyciOiAiTkhBTiIgaWYgciBlbHNlICJOb25lIiwKICAgICAgICAgICAgICAiZG9pIGNodW5nIGR1b25n'
'IChraG9uZyBjbyAnOycpIjogIk5IQU4iIGlmIHIwIGVsc2UgIk5vbmUifQogICAgICAgIGlmIG5vdCByMDoKICAgICAgICAg'
'ICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nIiwga3EKICAgICAgICByZXR1cm4gKERBVCBpZiByIGVsc2Ug'
'VFJVT1QpLCAoIiIgaWYgciBlbHNlICJtdWMgZ2l0LmV4ZSBob3AgbGUgYmkgTUFUIiksIGtxCgogICAgd2l0aCB0ZW1wZmls'
'ZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGxhID0gUGF0aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKSAg'
'ICAgICAgICAjICc7JyBuYW0gdHJvbmcgVEVOLCBraG9uZyBwaGFpIGRhdSBwaGFuIGNhY2gKICAgICAgICBkLCBjdywgcGYg'
'PSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAg'
'ICBub2kgPSBzdHIobGEpICsgVEhVX04xMCArIHN0cihkKQogICAgICAgIGt3ID0gZGljdChwcm9ncmFtX2ZpbGVzPXN0cihw'
'ZiksIGN3ZD1zdHIoY3cpKQogICAgICAgIHJfY2hpbmgsIF8gPSBnb2kocGF0aD1ub2ksICAgICAgKip7dGVuX3NlcDogVEhV'
'X04xMH0sICAgKiprdykgICAjIHRhY2ggZHVuZyAgLT4gTkhBTgogICAgICAgIHJfZHVvbmcsIF8gPSBnb2kocGF0aD1zdHIo'
'ZCksICAgKip7dGVuX3NlcDogVEhVX04xMH0sICAgKiprdykgICAjIGRvaSBjaHVuZyBkdW9uZwogICAgICAgIHJfcGhhbmJp'
'ZXQsIF8gPSBnb2kocGF0aD1ub2ksICAgKip7dGVuX3NlcDogb3MucGF0aHNlcH0sICoqa3cpICAjIHRhY2ggdGhlbyBvcy5w'
'YXRoc2VwIC0+IG1hdAogICAga3EgPSB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiB0ZW5fc2Vw'
'LCAiZGF1IHRodSI6IFRIVV9OMTAsCiAgICAgICAgICBmIm5vaSBiYW5nIHtUSFVfTjEwIXJ9LCB7dGVuX3NlcH09e1RIVV9O'
'MTAhcn0iOiAgICAgICAiTkhBTiIgaWYgcl9jaGluaCBlbHNlICJOb25lIiwKICAgICAgICAgIGYiZG9pIGNodW5nIGR1b25n'
'IChtb3QgbXVjLCB7dGVuX3NlcH09e1RIVV9OMTAhcn0pIjogICJOSEFOIiBpZiByX2R1b25nIGVsc2UgIk5vbmUiLAogICAg'
'ICAgICAgZiJwaGFuIGJpZXQ6IG5vaSBiYW5nIHtUSFVfTjEwIXJ9LCB7dGVuX3NlcH09e29zLnBhdGhzZXAhcn0iOiAiTkhB'
'TiIgaWYgcl9waGFuYmlldCBlbHNlICJOb25lIn0KICAgIGlmIG5vdCByX2R1b25nOgogICAgICAgIHJldHVybiBLREQsICJk'
'b2kgY2h1bmcgZHVvbmcgaG9uZzogbW90IG11YyBob3AgbGUgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgIyBD'
'b25nIHBoYWkgQ08gVEhFIGRvLiBOZXUgY2EgaGFpIGRhdSBwaGFuIGNhY2ggZGV1IHJhIE5IQU4gdGhpIHBoZXAgZG8ga2hv'
'bmcgcGhhbgogICAgIyBiaWV0IGR1b2MgZ2kg4oCUIGR1bmcgYmFvIERBVCwgYmFvIHRoYW5nIGxhIGtob25nIGRvIGR1b2Mu'
'CiAgICBpZiByX3BoYW5iaWV0OgogICAgICAgIHJldHVybiAoS0RELCBmInBoZXAgZG8gS0hPTkcgcGhhbiBiaWV0IGR1b2M6'
'IG5vaSBiYW5nIHtUSFVfTjEwIXJ9IG1hIHRhY2ggdGhlbyAiCiAgICAgICAgICAgICAgICAgICAgIGYie29zLnBhdGhzZXAh'
'cn0gVkFOIHRpbSByYSBnaXQuZXhlIiwga3EpCiAgICByZXR1cm4gKChEQVQsICIiLCBrcSkgaWYgcl9jaGluaCBlbHNlCiAg'
'ICAgICAgICAgIChUUlVPVCwgZiJ0YWNoIHRoZW8gb3MucGF0aHNlcCB0aGF5IHZpIHRoZW8ge3Rlbl9zZXB9IGR1b2MgdHJ1'
'eWVuIiwga3EpKQoKCmRlZiBkb19uMTEoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiVHJ1eWVuIGNoYW5fZG9hbiA9PiB0aHUg'
'ZHVvYyB0aG9uZyBiYW8gVkEgc3RkZXJyIElNLiBLaG9uZyB0cnV5ZW4gPT4gc3RkZXJyIFZBTiBjby4iIiIKICAgIGlmICJj'
'aGFuX2RvYW4iIG5vdCBpbiBzaWcucGFyYW1ldGVyczoKICAgICAgICByZXR1cm4gS0RELCAiX2dpdF93aW5kb3dzIGtob25n'
'IG5oYW4gdGhhbSBzbyBjaGFuX2RvYW4iLCB7InRoYW0gc28iOiBsaXN0KHNpZy5wYXJhbWV0ZXJzKX0KICAgIHdpdGggdGVt'
'cGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgKGQv'
'ImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBjZCA9IFtdCiAgICAgICAgXywg'
'ZV9jbyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSwgY2hhbl9kb2FuPWNk'
'KQogICAgICAgIF8sIGVfa2ggPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykp'
'CiAgICBrcSA9IHsiY2hhbl9kb2FuIHRodSBkdW9jIChtdWMpIjogbGVuKGNkKSwKICAgICAgICAgICJzdGRlcnIga2hpIENP'
'IGNoYW5fZG9hbiAoYnl0ZSkiOiBsZW4oZV9jby5lbmNvZGUoKSksCiAgICAgICAgICAic3RkZXJyIGtoaSBLSE9ORyB0cnV5'
'ZW4gKGJ5dGUpIjogbGVuKGVfa2guZW5jb2RlKCkpfQogICAgaWYgbGVuKGNkKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUo'
'KSkgPT0gMDoKICAgICAgICByZXR1cm4gS0RELCAibmhhbmggJVByb2dyYW1GaWxlcyUga2hvbmcgcGhhbiBnaWFpIEtIT05H'
'IGJheSByYSBjaGFuIGRvYW4gbmFvIC0+IGNodWEgZG8gZHVvYyIsIGtxCiAgICBvayA9IGxlbihjZCkgPiAwIGFuZCBsZW4o'
'ZV9jby5lbmNvZGUoKSkgPT0gMCBhbmQgbGVuKGVfa2guZW5jb2RlKCkpID4gMAogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxz'
'ZSBUUlVPVCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKZGVmIGRvX24xMihnb2ksIHNpZywgdGVwdCk6CiAg'
'ICAiIiJIYW5nIHNlbnRpbmVsIGdpdF9wYXRoIHRyb25nIGZpeHR1cmUgcGhhaSB0dXlldCBkb2kgdHJlbiBDQSBIQUkgbmVu'
'LiIiIgogICAgbmQgPSB0ZXB0LnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiKQogICAgaGFu'
'ZyA9IHNvcnRlZChzZXQocmUuZmluZGFsbChyJ2dpdF9wYXRoXHMqPVxzKiIoW14iXSspIicsIG5kKSkpCiAgICB4YXUgPSBb'
'aCBmb3IgaCBpbiBoYW5nIGlmIG5vdCAoUHVyZVBvc2l4UGF0aChoKS5pc19hYnNvbHV0ZSgpIGFuZCBQdXJlV2luZG93c1Bh'
'dGgoaCkuaXNfYWJzb2x1dGUoKSldCiAgICBrcSA9IHsiaGFuZyBnaXRfcGF0aCB0aW0gdGhheSI6IGhhbmcsICJjaGkgdHV5'
'ZXQgZG9pIE1PVCBuZW4iOiB4YXV9CiAgICBpZiBub3QgaGFuZzoKICAgICAgICByZXR1cm4gS0RELCAia2hvbmcgdGltIHRo'
'YXkgaGFuZyBnaXRfcGF0aCBuYW8gdHJvbmcgZml4dHVyZSAtPiBtYXUgZG9jIGNvIHRoZSBkYSBkb2kiLCBrcQogICAgcmV0'
'dXJuIChEQVQgaWYgbm90IHhhdSBlbHNlIFRSVU9UKSwgKCIiIGlmIG5vdCB4YXUgZWxzZSBmImNoaS1tb3QtbmVuOiB7eGF1'
'fSIpLCBrcQoKUFJPQkUgPSBbKCJOOCBidW9jIDEgY2hpIG5oYW4gZ2l0LmV4ZSIsIGRvX244KSwKICAgICAgICAgKCJOOSBi'
'b2MgbmhheSBrZXAgbyBtdWMgUEFUSCIsIGRvX245KSwKICAgICAgICAgKCJOMTAgZGF1ICc7JyB0cm9uZyB0ZW4gdGh1IG11'
'YyIsIGRvX24xMCksCiAgICAgICAgICgiTjExIGNoYW4gZG9hbiBkb2kga2VuaCIsIGRvX24xMSksCiAgICAgICAgICgiTjEy'
'IGhhbmcgc2VudGluZWwgdHV5ZXQgZG9pIENBIEhBSSBuZW4iLCBkb19uMTIpXQoKIyAtLS0gY2hlIGRvIFRVIEtJRU06IGNo'
'YXkgbmFtIHByb2JlIHRyZW4gbW90IGNheSBiYXQga3ksIG5lbiBiYXQga3kgLS0tCmlmICItLXR1LWtpZW0tcHJvYmUiIGlu'
'IHN5cy5hcmd2OgogICAgX2cgPSBQYXRoKHN5cy5hcmd2W3N5cy5hcmd2LmluZGV4KCItLXR1LWtpZW0tcHJvYmUiKSArIDFd'
'KS5yZXNvbHZlKCkKICAgIF9zcCA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF90ayIsIHN0'
'cihfZy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQogICAgX2xwID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3Bl'
'Yyhfc3ApOyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9scCkKICAgIF9zaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShfbHAuX2dp'
'dF93aW5kb3dzKQogICAgZGVmIF9nb2koKiprdyk6CiAgICAgICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgICAgICB3aXRoIGNv'
'bnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgogICAgICAgICAgICByZXR1cm4gX2xwLl9naXRfd2luZG93cygqKmt3KSwg'
'ZS5nZXR2YWx1ZSgpCiAgICBwcmludChmIlRVIEtJRU0gUFJPQkUgdHJlbiB7X2d9ICAobmVuIHtzeXMucGxhdGZvcm19KSIp'
'CiAgICBmb3IgX3RlbiwgX2YgaW4gUFJPQkU6CiAgICAgICAgX3R0LCBfY3QsIF9kbCA9IF9mKF9nb2ksIF9zaWcsIF9nLyJv'
'cHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIHByaW50KGYiICBbe190dDoxNH1dIHtfdGVufSIgKyAoZiIg'
'ICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgICAgIGZvciBfaywgX3YgaW4gKF9kbCBvciB7fSkuaXRlbXMoKTogcHJp'
'bnQoZiIgICAgICAgIHtfazozNH06IHtfdn0iKQogICAgc3lzLmV4aXQoMCkKCiMgLS0tIGNoZSBkbyBLSUVNIERPTkcgQk86'
'IHRlcCAucHkgbmF5IHBoYWkgVFJVTkcgVFVORyBCWVRFIHZvaSBiYW4gbmh1bmcgdHJvbmcgcHMxIC0tLQojIEtob25nIGNv'
'bmcgbmFvIGJ1b2MgaGFpIGJhbiBzYW8ga2hvcDogZG8gZHVvYywgbm9pIHRyYW4gMi80MDAgLT4gOTkvOTk5OTkgQ0hJIHRy'
'b25nIC5weQojIHRoaSBjaV9kYW5nX2t5IGxhbiB0MjYvdDI3IHZhbiB4YW5oLCBjb24gY2hvdCBTSEEgY3VhIHBzMSBjaGkg'
'c28gYmFuIG5odW5nIHZvaSBoYW5nIHNvCiMgY3VhIENISU5IIG5vLiBDaGF5OiBweXRob24gd3A1NDEtZG8tZzItd2luZG93'
'cy5weSAtLWtpZW0tZG9uZy1ibyB3cDU0MS1kby1nMi5wczEgIChyYyAwfDMpCmlmICItLWtpZW0tZG9uZy1ibyIgaW4gc3lz'
'LmFyZ3Y6CiAgICBpbXBvcnQgYmFzZTY0CiAgICBfcHMgPSBQYXRoKHN5cy5hcmd2W3N5cy5hcmd2LmluZGV4KCItLWtpZW0t'
'ZG9uZy1ibyIpICsgMV0pLnJlYWRfdGV4dChlbmNvZGluZz0iYXNjaWkiKQogICAgX20gPSByZS5zZWFyY2gociIoP21zKV5c'
'JEI2NCA9IEBcKCguKj8pXlwpIiwgX3BzKQogICAgX2sgPSByZS5zZWFyY2gociIoP20pXlwkU2hhQm9Eb1xzKj1ccyonKFsw'
'LTlhLWZdezY0fSknIiwgX3BzKQogICAgX25odW5nID0gYmFzZTY0LmI2NGRlY29kZSgiIi5qb2luKHJlLmZpbmRhbGwociIn'
'KFtBLVphLXowLTkrLz1dKiknIiwgX20uZ3JvdXAoMSkpKSkgaWYgX20gZWxzZSBiIiIKICAgIF90b2kgPSBQYXRoKF9fZmls'
'ZV9fKS5yZWFkX2J5dGVzKCkKICAgIF9vayA9IGJvb2woX20gYW5kIF9rKSBhbmQgX25odW5nID09IF90b2kgYW5kIGhhc2hs'
'aWIuc2hhMjU2KF90b2kpLmhleGRpZ2VzdCgpID09IF9rLmdyb3VwKDEpCiAgICBpbm4oZiJLSUVNIERPTkcgQk86IHtEQVQg'
'aWYgX29rIGVsc2UgS0REfSAgKG5odW5nIHtsZW4oX25odW5nKX0gYnl0ZSwgdGVwIHtsZW4oX3RvaSl9IGJ5dGUpIikKICAg'
'IHN5cy5leGl0KDAgaWYgX29rIGVsc2UgMykKCmlubigiPSIgKiA3OCk7IGlubigiV1A1NDEgZzIgLSBwaGVwIGRvIHRyZW4g'
'V2luZG93cyB0aGF0IChzcGVjIHIzOiBOMS1ONCwgTjgtTjEyLCBONywga2ljaCB0aHVvYykiKTsgaW5uKCI9IiAqIDc4KQoK'
'IyAtLS0tLS0tLS0tLS0tLS0tIHR1IGtpZW0gYm8gZG9jIC0tLS0tLS0tLS0tLS0tLS0KX2QsIF9nLCBfdCA9IGRvY19kbyhf'
'TUFVKQpfb2sgPSAobGVuKF9kKSA9PSAyIGFuZCBhbnkoeC5zdGFydHN3aXRoKCJ0MDJiIikgZm9yIHggaW4gX2QpCiAgICAg'
'ICBhbmQgbm90IGFueSh4LnN0YXJ0c3dpdGgoInQxMzEiKSBmb3IgeCBpbiBfZCkgYW5kIF90KQppbm4oIlR1IGtpZW0gYm8g'
'ZG9jIGxvZzoiLCBEQVQgaWYgX29rIGVsc2UgVFJVT1QpCmlmIG5vdCBfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERP'
'IERVT0M6IGJvIGRvYyBsb2cgY3VhIGNoaW5oIHNjcmlwdCBuYXkgc2FpIC0+IGtob25nIGRvIGdpIGNhLiIpOyBzeXMuZXhp'
'dCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDAuIG5lbiBkbyAtLS0tLS0tLS0tLS0tLS0tCmdvYyA9IFBhdGgoc3lzLmFyZ3Zb'
'MV0pLnJlc29sdmUoKSBpZiBsZW4oc3lzLmFyZ3YpID4gMSBlbHNlIFBhdGguY3dkKCkKdGVwLCB0ZXB0ID0gZ29jIC8gIm9w'
'cyIgLyAibGVhc2VfcHVibGlzaC5weSIsIGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIKaW5uKCIiKTsg'
'aW5uKCItIiAqIDc4KTsgaW5uKCIwLiBORU4gRE8iKQojIE1PSSBMT0cgUEhBSSBUVSBLSEFJIG5vIGRvIENBSSBHSSBiYW5n'
'IEJPIERPIE5BTy4gQmFpIGhvYyAxOS0wOS0yMDI2OiBtb3QgbHVvdCBkbwojIGd1aSB2ZSBkdW9jIGRvYyBuaHUga2V0IHF1'
'YSBjdWEgYmFuIHZhIGRhbmcgeGV0LCBuaHVuZyB0aGF0IHJhIGxhIGJhbiBkbyBDVSBjaGF5CiMgdHJlbiBuaGFuaCBLSEFD'
'LiBEb2MgcmEgdGhpIG1hdCBtb3Qgdm9uZzsgbG9nIHR1IGtoYWkgdGhpIHRoYXkgbmdheSBkb25nIGRhdS4KdHJ5OgogICAg'
'X3R1ID0gaGFzaGxpYi5zaGEyNTYoUGF0aChfX2ZpbGVfXykucmVhZF9ieXRlcygpKS5oZXhkaWdlc3QoKQpleGNlcHQgRXhj'
'ZXB0aW9uIGFzIF9lOgogICAgX3R1ID0gZiJraG9uZyB0dSBiYW0gZHVvYzoge19lfSIKZ2hpKCJib19kb19zaGEyNTYiLCBf'
'dHUpCmlubihmIiAgQk8gRE8gICAgICAgIDogc2hhMjU2IHtfdHVbOjE2XX0gIChiYW4ge0JBTl9CT19ET30pIikKaW5uKCIg'
'IHN5cy5wbGF0Zm9ybSA6Iiwgc3lzLnBsYXRmb3JtLCAifCBweXRob24iLCBzeXMudmVyc2lvbi5zcGxpdCgpWzBdKQppbm4o'
'IiAgb3MucGF0aHNlcCAgIDoiLCByZXByKG9zLnBhdGhzZXApLCAifCBQQVRIRVhUOiIsIHJlcHIob3MuZW52aXJvbi5nZXQo'
'IlBBVEhFWFQiKSlbOjYwXSkKaW5uKCIgIFByb2dyYW1GaWxlcyA6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUHJvZ3JhbUZp'
'bGVzIikpLCAifCBTeXN0ZW1Sb290OiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlN5c3RlbVJvb3QiKSkpCmlubigiICBDT05H'
'X0NVX0dJVCAgOiIsIHJlcHIoX0NPTkdfQ1VfR0lUX05HVU9JX0RPKQogICAgKyAoIiAgLT4gREEgQk8ga2hvaSBsdW90IGRv'
'IChDSSBraG9uZyBkYXQgYmllbiBuYXk7IHhlbSBkYXUgdGVwKSIgaWYgX0NPTkdfQ1VfR0lUX05HVU9JX0RPIGlzIG5vdCBO'
'b25lIGVsc2UgIiIpKQpnaGkoImNvbmdfY3VfZ2l0X25ndW9pX2RvIiwgX0NPTkdfQ1VfR0lUX05HVU9JX0RPKQppbm4oIiAg'
'Z29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5vbmUKaWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6CiAgICB0cnk6'
'CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4gPSBib29sKGN0eXBlcy53aW5kbGwuc2hlbGwzMi5Jc1VzZXJBbkFkbWlu'
'KCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXllbiA9IE5vbmUKZ2hpKCJxdXllbl9hZG1pbiIsIHF1eWVuKQpzeW1saW5r'
'X2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBk'
'ID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHRyeTogb3Mu'
'c3ltbGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJsayIpKTsgc3ltbGlua19kdW9jID0gVHJ1ZQogICAgICAgIGV4Y2VwdCBP'
'U0Vycm9yIGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZhbHNlOyBnaGkoInN5bWxpbmtfbG9pIiwgZiJ7dHlwZShlKS5fX25hbWVf'
'X306IHtlfSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZTogZ2hpKCJzeW1saW5rX2xvaSIsIHN0cihlKSkKZ2hpKCJzeW1saW5r'
'X2R1b2MiLCBzeW1saW5rX2R1b2MpCmlubigiICBBZG1pbmlzdHJhdG9yOiIsIHF1eWVuLCAifCB0YW8gc3ltbGluayBkdW9j'
'OiIsIHN5bWxpbmtfZHVvYykKCmxvaSA9IFtdCiMgQ29uZyBraWNoIHRodW9jIGxhIHBoZXAgZG8gdHJlbiBMSUNIIFNVIEdJ'
'VCwga2hvbmcgZGluaCBnaSBkZW4gbmVuLiBDaG8gcGhlcAojIC0tY2hpLWtpY2gtdGh1b2MgY2hheSBvIG1vaSBuZW4gZGUg'
'Y29uIFRVIEtJRU0gZHVvYyBjaGluaCBjb25nIG5heSAoZGEgZHVuZwojIGRlIHRhaSBkdW5nIGNhIGhhaSB2ZSBjdWEgc3Ug'
'Y28gbmVuLWN1IDE5LTA5KS4gTW9pIGNob3QgQ0hVQyBOQU5HIHZhbiBkb2kgV2luZG93cy4KaWYgc3lzLnBsYXRmb3JtICE9'
'ICJ3aW4zMiIgYW5kICItLWNoaS1raWNoLXRodW9jIiBub3QgaW4gc3lzLmFyZ3Y6CiAgICBsb2kuYXBwZW5kKGYiS0hPTkcg'
'cGhhaSBXaW5kb3dzIChzeXMucGxhdGZvcm09e3N5cy5wbGF0Zm9ybSFyfSkiKQppZiBub3QgdGVwLmlzX2ZpbGUoKTogIGxv'
'aS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB9IikKaWYgbm90IHRlcHQuaXNfZmlsZSgpOiBsb2kuYXBwZW5kKGYia2hvbmcg'
'dGhheSB7dGVwdH0iKQppZiBub3Qgc2h1dGlsLndoaWNoKCJnaXQiKTogbG9pLmFwcGVuZCgia2hvbmcgY28gYGdpdGAgdHJv'
'bmcgUEFUSCIpCiMgQm8gdGVzdCAobXVjIDIgdmEgTjcpIGNhbiBQeVlBTUw6IHRoaWV1IG5vLCAwZWE5NWRlIHJhIDk2LzE2'
'NiBjYSBETyAoODkgYmFvIHRoYW5nICJObyBtb2R1bGUgbmFtZWQgJ3lhbWwnIiwKIyA3IHF1YSBsdW90IGNvbjsgY28gUHlZ'
'QU1MOiAxNjYvMTY2IFFVQSkuIEJvIGRvIGdvaSBjaHVuZyBsYSAiY2EgRE8gTEEiIHJvaSBwaGF0IFRSVU9UIOKAlCBkbyB0'
'cmVuIDIwMjYtMDktMzBjLgojIERpZXUga2llbiB0aWVuIHF1eWV0IHBoYWkgaG9pIGJhbmcgQ0hJTkggdGllbiB0cmluaCBj'
'b24gc2UgY2hheSBibyB0ZXN0IChjaGF5KCk6IGN1bmcgbW9pIHRydW9uZzsgY3dkID0gb3BzLyA9CiMgc3lzLnBhdGhbMF0g'
'Y3VhIGJvIHRlc3QpIHZhIGhvaSBEVU5HIERVT0MgY2h1IGtob25nIGhvaSBDTyBNQVQuIEJhbiAzMGQgaG9pIGBmaW5kX3Nw'
'ZWMoInlhbWwiKWAgbyB0aWVuIHRyaW5oCiMgTkFZIHZhIG5ndW9uZyAzLjggc3V5IHR1IE5HVSBQSEFQIChgOj1gKSDigJQg'
'ZG8gdHJlbiAyMDI2LTA5LTMwZCwgY2EgaGFpIHJhIHJjPTEgVFJVT1QgY2hvIHVuZyB2aWVuIHNhY2g6CiMgdGh1IG11YyBk'
'dSBsaWV1IGB5YW1sL2AgdHJlbiBQWVRIT05QQVRIIHF1YSBmaW5kX3NwZWMgbWEgYHlhbWwuc2FmZV9kdW1wYCBraG9uZyBj'
'byAoODcgY2EgImxhIik7IHB5dGhvbiAzLjguMjAKIyBUSEFUIGNvIFB5WUFNTCwgYm8gdGVzdCBkdW5nIGBzdHIucmVtb3Zl'
'cHJlZml4YCAoMy45KSBsdWMgQ0hBWSAoMzMgY2EgImxhIjsgMy45LjIzOiAxNjYvMTY2KS4KaWYgbm90ICgiLS1jaGkta2lj'
'aC10aHVvYyIgaW4gc3lzLmFyZ3Ygb3IgIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndik6CiAgICBfcmNfZGssIF9yYV9kayA9'
'IGNoYXkoWyItYyIsICJpbXBvcnQgc3lzOyBzeXMuZXhpdCg5KSBpZiBzeXMudmVyc2lvbl9pbmZvIDwgKDMsIDkpIGVsc2Ug'
'Tm9uZTsgaW1wb3J0IHlhbWw7IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiIHlhbWwuc2FmZV9kdW1wKHlh'
'bWwuc2FmZV9sb2FkKCdhOiAxJykpIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgZ29jIC8gIm9wcyIgaWYgKGdvYyAv'
'ICJvcHMiKS5pc19kaXIoKSBlbHNlIFBhdGguY3dkKCksIHBodXQ9MikKICAgIGlmIF9yY19kayA9PSA5OgogICAgICAgIGxv'
'aS5hcHBlbmQoZiJweXRob24ge3N5cy52ZXJzaW9uLnNwbGl0KClbMF19IDwgMy45OiBibyB0ZXN0IGN1YSB1bmcgdmllbiBk'
'dW5nIHN0ci5yZW1vdmVwcmVmaXggKDMuOSkgbHVjIENIQVkiKQogICAgZWxpZiBfcmNfZGs6CiAgICAgICAgbG9pLmFwcGVu'
'ZChmInB5dGhvbiBuYXkgS0hPTkcgY28gUHlZQU1MIGR1bmcgZHVvYyAoeyhfcmFfZGsuc3RyaXAoKS5zcGxpdGxpbmVzKCkg'
'b3IgWycnXSlbLTFdWzo5MF19KToiCiAgICAgICAgICAgICAgICAgICBmIiBcIntzeXMuZXhlY3V0YWJsZX1cIiAtbSBwaXAg'
'aW5zdGFsbCBweXlhbWwiCiAgICAgICAgICAgICAgICAgICAiIChiYW4gbmh1bmcgcHMxIHR1IHRhaSBLSE9ORyBjbyBwaXA6'
'IGNoYXkgbGFpIHZvaSAtUHkgPHB5dGhvbiBkYSBjbyBQeVlBTUw+KSIpCiAgICAjIEJvIHRlc3QgY29uIGdvaSBgc2h1dGls'
'LndoaWNoYCBjaG8gYmFzaC9hY3Rpb25saW50L3NoZWxsY2hlY2sgKDBlYTk1ZGU6IHQzMyB0MTM3IHQxNTkgY2FuIGFjdGlv'
'bmxpbnQsIHQxMzcgY2FuCiAgICAjIHNoZWxsY2hlY2ssIGNhYyBjYSBjaGF5IG9wcy9jYWlfYWN0aW9ubGludC5zaCBjYW4g'
'YmFzaCkuIFRoaWV1IHRoaSBjYWMgY2EgYXkgaW4gIktIT05HIERPIERVT0M6IHRoaWV1IGAuLi5gIiB2YSBibyBkbyByYQog'
'ICAgIyByYz0zIOKAlCBuaHVuZyBjaGkgU0FVIGNhIGJvIHRlc3QgbGFuIE43IChkbyB0cmVuIDIwMjYtMDktMzBnLCBQQVRI'
'IHRoaWV1IGFjdGlvbmxpbnQ6IGBDb25nIGN1IGRheSBkdSBkZSBkb2AgS0RELCByYz0zCiAgICAjIHNhdSAyIGx1b3QgYm8g'
'dGVzdCkuIEN1bmcgbHkgZG8gUHlZQU1MIGR1b2MgaG9pIG8gZGF5OiBob2kgVFJVT0MsIGN1bmcgUEFUSCBtYSBjaGF5KCkg'
'dHJ1eWVuIGNobyBibyB0ZXN0LgogICAgIyBWQSBjdW5nIENITyBibyB0ZXN0IGR1bmc6IHRyZW4gV2luZG93cyBgc2h1dGls'
'LndoaWNoYCB0cmEgVEhVIE1VQyBISUVOIEhBTkggVFJVT0MgUEFUSCwgbWEgYm8gdGVzdCBjaGF5IHZvaSBjd2QgPSBnb2Mg'
'Y29uCiAgICAjIHRpZW4gdHJpbmggbmF5IGR1bmcgbyBjd2QgQ1VBIE5HVU9JIERPIChub2kgZ29pIHBzMSwgdmQuIERvd25s'
'b2FkcyDigJQgZHVuZyBub2kgZ2lhaSBuZW4gYWN0aW9ubGludC5leGUpLiBEbyB0cmVuIDIwMjYtMDktMzBrCiAgICAjIChu'
'aGFuaCB3aW4zMiBUSEFUIGN1YSBzaHV0aWwud2hpY2gpOiBhY3Rpb25saW50IHRvdCBvIGN3ZCBuZ3VvaSBkbyArIGJhbiBo'
'b25nIGRhdSBQQVRIID0+IG11YyAwIGhvaSBiYW4gbyBjd2QgKHJjPTApLCBibyB0ZXN0CiAgICAjIGR1bmcgYmFuIHRyZW4g'
'UEFUSCA9PiByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCwgYGxhOiBbJ3QzMycsICd0MTM3JywgJ3QxNTknXWAuIEdpYWkgdGVu'
'IHZvaSBjd2QgPSBnb2Mgcm9pIGdvaSBUSEFORyBiYW5nIGR1b25nCiAgICAjIFRVWUVUIERPSSBkYSBnaWFpIChxdWEgaGFu'
'IHRoaSBydW4oKSBnaWV0IGR1bmcgdGllbiB0cmluaCDigJQgbHkgZG8gYmFuIDMwaSBraG9uZyBob2kgcXVhIGNoYXkoKSku'
'CiAgICBfY3dkX25ndW9pX2RvID0gb3MuZ2V0Y3dkKCkKICAgIHRyeToKICAgICAgICBpZiBnb2MuaXNfZGlyKCk6IG9zLmNo'
'ZGlyKGdvYykKICAgICAgICBfY2MgPSB7YzogKG9zLnBhdGguYWJzcGF0aChwKSBpZiBwIGVsc2UgTm9uZSkgZm9yIGMsIHAg'
'aW4KICAgICAgICAgICAgICAgKChjLCBzaHV0aWwud2hpY2goYykpIGZvciBjIGluICgiYmFzaCIsICJhY3Rpb25saW50Iiwg'
'InNoZWxsY2hlY2siKSl9CiAgICBmaW5hbGx5OgogICAgICAgIG9zLmNoZGlyKF9jd2Rfbmd1b2lfZG8pCiAgICBfdGhpZXVf'
'Y2MgPSBbYyBmb3IgYywgcCBpbiBfY2MuaXRlbXMoKSBpZiBub3QgcF0KICAgIGlmIF90aGlldV9jYzoKICAgICAgICBsb2ku'
'YXBwZW5kKGYidGhpZXUgY29uZyBjdSBibyB0ZXN0IGdvaSBxdWEgUEFUSDoge190aGlldV9jY30gKGFjdGlvbmxpbnQ6IG9w'
'cy9jYWlfYWN0aW9ubGludC5zaCB2b2kgQUxfVkVSOyIKICAgICAgICAgICAgICAgICAgICIgYmFzaDogR2l0IEJhc2gsIGto'
'b25nIHBoYWkgYmFzaC5leGUgY3VhIFdTTCkiKQogICAgIyBzaGVsbGNoZWNrIEtIT05HIG5oYW4gLS1ub3JjIHRoaSBhY3Rp'
'b25saW50IDEuNy43ICh0dSB0cnV5ZW4gLS1ub3JjKSBsYW0gdDMzIERPLCB2YSBTSEVMTENIRUNLX09QVFM9LS1ub3JjIGN1'
'YSBjaGF5KCkgbGFtCiAgICAjIHQxMzcgRE8g4oCUIGNhICJsYSIgPT4gVFJVT1QgZ2lhIChkbyB0cmVuIDIwMjYtMDktMzBo'
'LCBzaGVsbGNoZWNrIGdpYSB0dSBjaG9pIC0tbm9yYzogYmFuIDMwaCByYz0xIGBsYTogWyd0MzMnXWAgc2F1IGNhCiAgICAj'
'IGJvIHRlc3QpLiBgd2hpY2hgIGNoaSBob2kgQ08gTUFUOyBvIGRheSBob2kgRFVORyBEVU9DLiBOZ3VvbmcgZG8gdHJlbiBz'
'aGVsbGNoZWNrIFRIQVQ6IDAuNC43LzAuNS4wLzAuNi4wIHR1IGNob2kgLS1ub3JjCiAgICAjIChyYz0zKSwgMC43LjAgdHJv'
'IGxlbiBuaGFuLiBQaGVwIGhvaSBwaGFpIHRoYXkgRFVORyBTSEVMTENIRUNLX09QVFMgbWEgY2hheSgpIGRhdCBjaG8gbHVv'
'dCBjb246IGJhbiAzMGkgaG9pIHZvaSBiaWVuIENVQQogICAgIyBOR1VPSSBETyDigJQgZG8gdHJlbiAyMDI2LTA5LTMwaSwg'
'c2hlbGxjaGVjayAwLjkuMCArIFNIRUxMQ0hFQ0tfT1BUUz0tLWV4dGVuZGVkLWFuYWx5c2lzPXRydWUgKGNvIGN1YSAwLjEw'
'KTogcmM9MyAia2hvbmcgbmhhbgogICAgIyAtLW5vcmM6IGNhcCBuaGF0IHNoZWxsY2hlY2siIHRyb25nIGtoaSB0MzMvdDEz'
'NyBxdWEgY2hheSgpIGRldSAxLzEuIEdvaSBUSEFORyAoa2hvbmcgcXVhIGNoYXkoKSk6IHF1YSBoYW4gdGhpIHJ1bigpIGdp'
'ZXQKICAgICMgZHVuZyBzaGVsbGNoZWNrOyBxdWEgY2hheSgpIHRoaSBjaGkgZ2lldCBweXRob24gY29uLCBzaGVsbGNoZWNr'
'IHRyZW8gbyBsYWkgbW8gY29pIChkbyB0cmVuIDIwMjYtMDktMzBpOiAxLzEgY29uIHNvbmcpLgogICAgZWxpZiBzdWJwcm9j'
'ZXNzLnJ1bihbX2NjWyJzaGVsbGNoZWNrIl0sICItLW5vcmMiLCAiLS12ZXJzaW9uIl0sIGNhcHR1cmVfb3V0cHV0PVRydWUs'
'IHRpbWVvdXQ9NjAsCiAgICAgICAgICAgICAgICAgICAgICAgIGVudj1kaWN0KG9zLmVudmlyb24sIFNIRUxMQ0hFQ0tfT1BU'
'Uz0iLS1ub3JjIikpLnJldHVybmNvZGU6CiAgICAgICAgbG9pLmFwcGVuZCgic2hlbGxjaGVjayB0cmVuIFBBVEgga2hvbmcg'
'bmhhbiAtLW5vcmMgKGFjdGlvbmxpbnQgMS43LjcgdmEgY2hheSgpIGRldSB0cnV5ZW4gY28gYXkpOiBjYXAgbmhhdCBzaGVs'
'bGNoZWNrIikKICAgICMgYWN0aW9ubGludCBjdW5nIHBoYWkgRFVORyBEVU9DLCBraG9uZyBjaGkgQ08gTUFUOiB0MzMvdDEz'
'Ny90MTU5IGdvaSBubyBUSEFORywgdmEgbW90IGFjdGlvbmxpbnQga2hvbmcgY2hheSAoc2FpIGtpZW4gdHJ1YywKICAgICMg'
'aG9uZykgbGFtIGNhIGJhIERPICJhY3Rpb25saW50IERPIChyYz0uLi4pIiDigJQgY2EgImxhIiA9PiBUUlVPVCBnaWEgc2F1'
'IGNhIGJvIHRlc3QgKGRvIHRyZW4gMjAyNi0wOS0zMGo6IGFjdGlvbmxpbnQgZ2lhCiAgICAjIHJjPTEgPT4gbXVjIDAgaW0g'
'bGFuZywgdDMzICJsYSIpLiBCYW4gVEhBVCAxLjYuMjcvMS43LjcvMS43LjgvMS43LjEyIGRldSByYz0wIHZhIGRldSBjaG8g'
'dDMzL3QxMzcvdDE1OSBRVUEgdHJlbiAwZWE5NWRlLgogICAgIyBiYXNoIENISSBob2kgQ08gTUFULCBjbyBjaHUgZGljaDog'
'YmFzaCBXU0wgKFN5c3RlbTMyKSBsYW0gdDM1LXQ0MCBETyBuaHVuZyBjYSBzYXUgZGV1IE5HT0FJX1BIQU1fVkksIGNvbiB0'
'MzIvdDE1MiB0dSBjaG9uCiAgICAjIEdpdCBCYXNoIChfYmFzaF9wb3NpeCBjdWEgdW5nIHZpZW4pIOKAlCBkbyB0cmVuIDIw'
'MjYtMDktMzBqOiBiYXNoIGtpZXUgV1NMID0+IHQzNS10NDAgRE8sIGRldSByb2kgdmFvIG5nb2FpIHBoYW0gdmkuCiAgICAj'
'IENIQVkgRFVPQyBjaHVhIHBoYWkgRFVORyBEVU9DOiBkbyB0cmVuIDIwMjYtMDktMzBrLCAwZWE5NWRlLCBhY3Rpb25saW50'
'IFRIQVQgMS40LjMvMS41LjAvMS41LjMvMS42LjAvMS42LjgvMS42LjE1LzEuNi4yMC8KICAgICMgMS42LjIyIGRldSBgLXZl'
'cnNpb25gIHJjPTAsIG1hIGNhIHRhbSBsYW0gdDEzNy90MTU5IERPIChgcHJvcGVydHkgInJ1bl9hdHRlbXB0Ii8id29ya2Zs'
'b3dfc2hhIiBpcyBub3QgZGVmaW5lZGApLCAxLjQuMy8xLjUuMAogICAgIyB0aGVtIHQzMyAoYG11c3QgYmUgY29udGFpbmVk'
'IHdpdGhpbiAke3sgfX1gKSDigJQgZTJlIDEuNi4yMjogcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0MTM3Jywg'
'J3QxNTknXWAgY2hvIHVuZyB2aWVuCiAgICAjIHNhY2g7IDEuNi4yMy8xLjYuMjQvMS42LjI2LzEuNi4yNy8xLjcuMC8xLjcu'
'Ni8xLjcuNy8xLjcuMTIgUVVBIGNhIGJhLiBTYW4gbGEgYmFuCiAgICAjIGdoaW0gQ0kgKEFMX1NBTiksIEtIT05HIHBoYWkg'
'MS42LjIzIGRvIHRyZW4gTU9UIHVuZyB2aWVuOiB3b3JrZmxvdyBjdWEgdW5nIHZpZW4gc2F1IGNvIHRoZSBkdW5nIGN1IHBo'
'YXAgbW9pIGhvbiwgbWEgQ0kgY2hpIGRvCiAgICAjIGJhbmcgYmFuIGdoaW0uIEN1IGhvbiBzYW4gPT4gS0hPTkcgRE8gRFVP'
'QyAoY2hhbiBjYSAxLjYuMjMtMS43LjYgZGFuZyBRVUE6IGZhaWwtY2xvc2UsIGtob25nIHBoYWkgcGhhbiBxdXlldCkuIGB2'
'YCBkYXU6IGJhbgogICAgIyBgZ28gaW5zdGFsbGAgaW4gYHYxLjcuN2A7IGtob25nIGRvYyBkdW9jIHNvICh2ZC4gYChkZXZl'
'bClgKSA9PiBLSE9ORyBETyBEVU9DLgogICAgaWYgbm90IF90aGlldV9jYzoKICAgICAgICBfYWwgPSBzdWJwcm9jZXNzLnJ1'
'bihbX2NjWyJhY3Rpb25saW50Il0sICItdmVyc2lvbiJdLCBjYXB0dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsIGVuY29k'
'aW5nPSJ1dGYtOCIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD02MCkK'
'ICAgICAgICBfYWxfdiA9IHJlLnNlYXJjaChyIig/bSledj8oXGQrKVwuKFxkKylcLihcZCspIiwgX2FsLnN0ZG91dCBvciAi'
'IikKICAgICAgICBpZiBfYWwucmV0dXJuY29kZToKICAgICAgICAgICAgbG9pLmFwcGVuZCgiYWN0aW9ubGludCB0cmVuIFBB'
'VEggY28gbWF0IG5odW5nIGBhY3Rpb25saW50IC12ZXJzaW9uYCByYyE9MCAoa2hvbmcgY2hheSBkdW9jKTogY2FpIGxhaSBi'
'YW4gZ2hpbSBBTF9WRVIiKQogICAgICAgIGVsaWYgbm90IF9hbF92IG9yIHR1cGxlKGludCh4KSBmb3IgeCBpbiBfYWxfdi5n'
'cm91cHMoKSkgPCBBTF9TQU46CiAgICAgICAgICAgIGxvaS5hcHBlbmQoZiJhY3Rpb25saW50IHtfYWxfdi5ncm91cCgwKSBp'
'ZiBfYWxfdiBlbHNlICcoa2hvbmcgZG9jIGR1b2MgcGhpZW4gYmFuKSd9IGN1IGhvbiBiYW4gZ2hpbSBDSSAiCiAgICAgICAg'
'ICAgICAgICAgICAgICAgZiJ7Jy4nLmpvaW4obWFwKHN0ciwgQUxfU0FOKSl9IChBTF9WRVIpOiBiYW4gY3UgbGFtIHQxMzcv'
'dDE1OSBETyAnbGEnIHRyZW4gdW5nIHZpZW4gc2FjaCDigJQiCiAgICAgICAgICAgICAgICAgICAgICAgIiBjYWkgYmFuIGdo'
'aW0gKG9wcy9jYWlfYWN0aW9ubGludC5zaCB2b2kgQUxfVkVSKSIpCgpyYywgaGVhZCwgXyA9IGdpdChnb2MsICJyZXYtcGFy'
'c2UiLCAiSEVBRCIpCmlmIHJjOiBsb2kuYXBwZW5kKCJraG9uZyBkb2MgZHVvYyBIRUFEIikKZ2hpKCJoZWFkIiwgaGVhZCkK'
'cmNfYSwgXywgXyA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIi0taXMtYW5jZXN0b3IiLCBTSEFfRzEsIGhlYWQgb3IgIkhF'
'QUQiKQpsYV9oYXVfZHVlID0gKHJjX2EgPT0gMCkKaWYgaGVhZCA9PSBTSEFfRzE6CiAgICB0aGVfaGUgPSAiZzEiOyBpbm4o'
'ZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IERBWSBMQSBnMS4gQ0hVQSBjbyBiYW4gdmEgZzI7IGtldCBxdWEgZHVvaSBsYSBO'
'RU4gRE8uIikKZWxpZiBsYV9oYXVfZHVlOgogICAgdGhlX2hlID0gImcyIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAt'
'PiBoYXUgZHVlIGN1YSBnMSAoe1NIQV9HMVs6OF19KTsgdW5nIHZpZW4gZzIgaGF5IGtob25nOiBONycgKG11YyAxKSBkaW5o'
'IGRhbmguIikKZWxzZToKICAgIHRoZV9oZSA9ICI/IjsgbG9pLmFwcGVuZChmIkhFQUQ9e2hlYWRbOjhdfSBLSE9ORyBwaGFp'
'IGcxIHZhIEtIT05HIHBoYWkgaGF1IGR1ZSBjdWEge1NIQV9HMVs6OF19IOKAlCByZWJhc2U/IG5oYW0gbmhhbmg/IikKZ2hp'
'KCJ0aGVfaGUiLCB0aGVfaGUpCnJjX3IsIHJlZnMsIF8gPSBnaXQoZ29jLCAiZm9yLWVhY2gtcmVmIiwgIi0tcG9pbnRzLWF0'
'IiwgaGVhZCBvciAiSEVBRCIsCiAgICAgICAgICAgICAgICAgICAgIi0tZm9ybWF0PSUocmVmbmFtZTpzaG9ydCkiKQpkc3Ig'
'PSBbeCBmb3IgeCBpbiByZWZzLnNwbGl0bGluZXMoKSBpZiB4LnN0cmlwKCkgYW5kIHguc3RyaXAoKSAhPSAiZG8tdGFtIl0K'
'Z2hpKCJyZWZfdHJvX3RvaV9oZWFkIiwgZHNyKQppbm4oZiIgIHJlZiB0cm8gdG9pIEhFQUQ6IHsnLCAnLmpvaW4oZHNyKSBp'
'ZiBkc3IgZWxzZSAnKGtob25nIHJlZiBuYW8gLSBIRUFEIHJvaSB0dSBkbyknfSIpCgppZiBsb2k6CiAgICBpbm4oIiIpOyBp'
'bm4oIktIT05HIERPIERVT0M6IG5lbiBkbyBzYWksIEtIT05HIGluIGtldCBsdWFuIG5hby4iKQogICAgZm9yIHggaW4gbG9p'
'OiBpbm4oIiAgLSIsIHgpCiAgICBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDEuIGtpY2ggdGh1b2MgKE43JyBj'
'dWEgc3BlYyByMykgLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjEuIEtJQ0ggVEhVT0Mg'
'4oCUIHRyYW4gc3BlYyByMzogPD0gMiB0ZXAgdmEgPD0gNDAwIGRvbmcgdGhlbSIpCiMgVkUgTkVOIFBIQUkgVFVPSSDigJQg'
'dmEgcGhhaSBDSFVORyBNSU5IIGR1b2MgbGEgdHVvaSwga2hvbmcgcGhhaSBnaWEgZGluaC4KIyBCYWkgaG9jIHRyYSBnaWEg'
'MTktMDktMjAyNjogY2xvbmUgdGFpIGR1bmcgY2hpIGZldGNoIG5oYW5oIGJhbiB2YSwgYG9yaWdpbi9tYXN0ZXJgCiMgZHVu'
'ZyB5ZW4gdHUgMTQtMDkgKGMxNmJkMzIsIHNhdSA5NyBjb21taXQpLiBtZXJnZS1iYXNlIHJvaSB2ZSBkdW5nIGRpbmggbWFz'
'dGVyIGN1LAojIG5lbiBkaWZmIE5VT1QgY2EgOTcgY29tbWl0IG1hc3RlcjogZG8gcmEgNDYgdGVwIC8gKzcxMTggdGhheSB2'
'aSAyIHRlcCAvICszOTcg4oCUCiMgQ1VORyBNT1QgQ09NTUlUIDBlYTk1ZGUuIE1vdCB0aWV1IGNoaSBERUxUQSBtYSB2ZSBu'
'ZW4ga2hvbmcgdHVvaSB0aGkga2hvbmcgc2FpCiMgbGVjaCBtb3QgY2h1dCwgbm8gc2FpIGNhIG1vdCBiYWMgZG8gbG9uLgoj'
'IENobyBuZW46IG5lbiBraG9uZyBjaHVuZyBtaW5oIGR1b2MgbGEgdHVvaSA9PiBLSE9ORyBETyBEVU9DIChyYz0zKSwgS0hP'
'TkcgcGhhaSBUUlVPVC4KIyBUUlVPVCBsYSBtb3QgUEhBTiBRVVlFVCB2ZSBiYW4gdmE7IHBoYW4gcXV5ZXQgY2hpIGR1b2Mg'
'cGhlcCBwaGF0IHJhIGtoaSBkYSBkbyBkdW9jLgplciA9ICIiCnJjX3UsIHVybF90aG8sIF8gPSBnaXQoZ29jLCAicmVtb3Rl'
'IiwgImdldC11cmwiLCAib3JpZ2luIikKdXJsX28sIHVybF9pbiA9IF91cmxfc2FjaCh1cmxfdGhvKSwgX3VybF9pbih1cmxf'
'dGhvKQpnaGkoIm9yaWdpbl91cmwiLCB1cmxfaW4pOyBpbm4oZiIgIG9yaWdpbiAgICAgICA6IHt1cmxfaW4gb3IgJyhraG9u'
'ZyBkb2MgZHVvYyknfSIpCnVybF9vayA9IChub3QgcmNfdSkgYW5kIHVybF9vLnJzdHJpcCgiLyIpIGluIFVSTF9LSE9fSE9Q'
'X0xFCnJjX2xyLCBvdXRfbHIsIGVyX2xyID0gZ2l0KGdvYywgImxzLXJlbW90ZSIsICJvcmlnaW4iLCAicmVmcy9oZWFkcy9t'
'YXN0ZXIiKSBpZiB1cmxfb2sgZWxzZSAoMSwgIiIsICIiKQplcl9sciA9IF9hbl91c2VyaW5mbyhlcl9scikKcmNfbG0sIGxt'
'LCBlcl9sbSAgICAgPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIm9yaWdpbi9tYXN0ZXIiKQpybSA9IG91dF9sci5zcGxpdCgp'
'WzBdIGlmIChub3QgcmNfbHIgYW5kIG91dF9sci5zdHJpcCgpKSBlbHNlICIiCmlmIG5vdCB1cmxfb2s6CiAgICBrZXQoIk43'
'JyBraWNoIHRodW9jIiwgS0RELCBmIm9yaWdpbj17dXJsX2luIXJ9IEtIT05HIHBoYWkga2hvIHRoYXQg4oCUICd0dW9pJyBz'
'byB2b2kgbm8ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGdpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAx'
'CmVsaWYgbm90IHJtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwKICAgICAgICBmImtob25nIGhvaSBkdW9jIG1h'
'c3RlciB0cmVuIHJlbW90ZSAobHMtcmVtb3RlIHJjPXtyY19scn0pOiB7ZXJfbHJbOjYwXX0gIgogICAgICAgIGYi4oCUIGto'
'b25nIGNodW5nIG1pbmggZHVvYyB2ZSBuZW4gY29uIHR1b2kiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIs'
'IDEKZWxpZiByY19sbSBvciBub3QgbG06CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25nIGRvYyBkdW9j'
'IG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmU6IHtlcl9sbVs6NjBdfSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIi'
'LCAiIiwgMQplbGlmIGxtICE9IHJtOgogICAgIyBEZW0geGVtIHR1dCBsYWkgYmFvIHhhLCBuZXUgZGVtIGR1b2Mg4oCUIGNv'
'biBzbyBuYXkgbm9pIHJvIG11YyBkbyBzYWkgbGVjaC4KICAgIHJjX2MsIHNhdSwgXyA9IGdpdChnb2MsICJyZXYtbGlzdCIs'
'ICItLWNvdW50IiwgZiJ7bG19Li57cm19IikKICAgIHhhID0gZiIsIHR1dCBsYWkge3NhdX0gY29tbWl0IiBpZiAobm90IHJj'
'X2MgYW5kIHNhdS5zdHJpcCgpLmlzZGlnaXQoKSkgZWxzZSAiIgogICAgaW5uKGYiICBvcmlnaW4vbWFzdGVyIHRyb25nIGNs'
'b25lIDoge2xtWzoxMl19IikKICAgIGlubihmIiAgbWFzdGVyIHRyZW4gcmVtb3RlICAgICAgICA6IHtybVs6MTJdfXt4YX0i'
'KQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAga2V0KCJONycga2lj'
'aCB0aHVvYyIsIEtERCwKICAgICAgICBmInZlIG5lbiBDVTogb3JpZ2luL21hc3Rlcj17bG1bOjEyXX0gIT0gcmVtb3RlPXty'
'bVs6MTJdfXt4YX0gIgogICAgICAgIGYi4oCUIGNoYXkgYGdpdCAtQyA8a2hvPiBmZXRjaCBvcmlnaW4gbWFzdGVyYCByb2kg'
'ZG8gbGFpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsc2U6CiAgICBpbm4oZiIgIHZlIG5lbiBU'
'VU9JOiBvcmlnaW4vbWFzdGVyID0ge2xtWzoxMl19ID09IG1hc3RlciB0cmVuIHJlbW90ZSIpCiAgICBnaGkoIm1hc3Rlcl9j'
'bG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICByY19tYiwgbWIsIGVyX21iID0gZ2l0KGdvYywgIm1l'
'cmdlLWJhc2UiLCAib3JpZ2luL21hc3RlciIsIGhlYWQpCmlmIHJjX21iIG9yIG5vdCBtYjoKICAgIGlmIG1iID09ICIiIGFu'
'ZCBybSBhbmQgbG0gPT0gcm06CiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyB0aW5oIGR1b2Mg'
'bWVyZ2UtYmFzZSB2b2kgb3JpZ2luL21hc3Rlcjoge2VyX21iWzo3MF19IikKICAgIG5zLCByYyA9ICIiLCAxCmVsc2U6CiAg'
'ICBnaGkoIm1lcmdlX2Jhc2UiLCBtYikKICAgIGlubihmIiAgbWVyZ2UtYmFzZShvcmlnaW4vbWFzdGVyLCBIRUFEKSA9IHtt'
'Yls6MTJdfSIpCiAgICBpZiBtYiAhPSBTSEFfQkFTRV9TUEVDOgogICAgICAgIGlubihmIiAgTFVVIFk6IGtoYWMgYmFzZSBt'
'YSBzcGVjIHIzIGtoYWkgKHtTSEFfQkFTRV9TUEVDWzoxMl19KSDigJQgdmkgbmhhbmggZGEgbWVyZ2UgbWFzdGVyLiIpCiAg'
'ICAgICAgaW5uKCIgICAgICAgICBEbyBzbyBiYXNlIGN1IHNlIE5VT1QgcGhhbiBtYXN0ZXIgbWFuZyB2YW8uIER1bmcgbWVy'
'Z2UtYmFzZSBtb2kgbGEgdmllYyBjdWEgZXhlY3V0b3IuIikKICAgICAgICByY194LCBuc194LCBfID0gZ2l0KGdvYywgImRp'
'ZmYtdHJlZSIsICItciIsICItTSIsICItLWRpZmYtYWxnb3JpdGhtPW15ZXJzIiwgIi0tbnVtc3RhdCIsIFNIQV9CQVNFX1NQ'
'RUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAgICAgICAgICAgIGggPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBu'
'c194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICAgICAgICAgIGEgPSBzdW0oaW50KHhbMF0pIGZvciB4IGluIGgg'
'aWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdoaSgibnVtc3RhdF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVwIjogbGVu'
'KGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBpbm4oZiIgICAgICAgICAoZG9pIGNoaWV1OiBzbyBiYXNlIHNwZWMgPSB7'
'bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkgS0hPTkcgZHVuZyBkZSBjaGFtKSIpCiAgICAjIFBMVU1CSU5HLCBr'
'aG9uZyBQT1JDRUxBSU46IGBnaXQgZGlmZmAgZG9jIGNhdSBoaW5oIFVJIENVQSBOR1VPSSBETyAoZGlmZi5hbGdvcml0aG0s'
'IGRpZmYucmVuYW1lcywgZGlmZi5vcmRlckZpbGUsCiAgICAjIGNvbG9yLmRpZmYpLCB2YSBnaWEgdHJpIEhPUCBMRSBkb2kg'
'bHVvbiBTTyBkb25nIG1hIHZhbiByYSBjaHUgc28g4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGk6IHVuZyB2aWVuIHRvbmcgaG9w'
'IChteWVycyArNDAxKSA9PgogICAgIyBiYW4gMzBpIERBVCAyIHRlcCAvICs0MDAgZHVvaSBgZGlmZi5hbGdvcml0aG0gPSBo'
'aXN0b2dyYW1gIGhvYWMgYHBhdGllbmNlYCwgVFJVT1QgKzQwMSBraGkgbWFjIGRpbmg7IDEwLzc1IGNvbW1pdCBjaGFtCiAg'
'ICAjIHdyaXRlIHNldCBjbyBzbyBkb25nIGRvaSB0aGVvIHRodWF0IHRvYW4uIGBkaWZmLXRyZWUgLXIgLU1gID0gbWFjIGRp'
'bmggY3VhIGBnaXQgZGlmZmAgKHJlbmFtZXMgYmF0KSB2YSBLSE9ORyBkb2MgY2FjIGtob2EKICAgICMgYXkuIFRodWF0IHRv'
'YW4gcGhhaSBUVU9ORyBNSU5IOiBkaWZmLjxkcml2ZXI+LmFsZ29yaXRobSAocXVhIGNvcmUuYXR0cmlidXRlc0ZpbGUgY3Vh'
'IG5ndW9pIGRvKSBWQU4gbG90IHZhbyBwbHVtYmluZyDigJQKICAgICMgZG8gdHJlbiAyMDI2LTA5LTMwaSwgYCoucHkgZGlm'
'Zj1hbGdgICsgZGlmZi5hbGcuYWxnb3JpdGhtPWhpc3RvZ3JhbTogZGlmZi10cmVlICs0MDEgY2hvIHVuZyB2aWVuIG15ZXJz'
'ICs0MDA7IGNvIHR1b25nIG1pbmgKICAgICMgdGhhbmcga2hvYSBheS4gYXR0cmlidXRlcyBgLWRpZmZgL2NvcmUuYmlnRmls'
'ZVRocmVzaG9sZCB2YW4gYXAgPT4gYC1gID0+IEtIT05HIERPIERVT0MgKGNob3QgZHVvaSkuCiAgICByYywgbnMsIGVyID0g'
'Z2l0KGdvYywgImRpZmYtdHJlZSIsICItciIsICItTSIsICItLWRpZmYtYWxnb3JpdGhtPW15ZXJzIiwgIi0tbnVtc3RhdCIs'
'IG1iLCBoZWFkKQppZiByYzoKICAgIHBhc3MKZWxzZToKICAgIGhhbmcgPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBucy5z'
'cGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAgdGhlbSA9IHN1bShpbnQoaFswXSkgZm9yIGggaW4gaGFuZyBpZiBoWzBd'
'LmlzZGlnaXQoKSkKICAgIHhvYSAgPSBzdW0oaW50KGhbMV0pIGZvciBoIGluIGhhbmcgaWYgaFsxXS5pc2RpZ2l0KCkpCiAg'
'ICBnaGkoInNvX3RlcCIsIGxlbihoYW5nKSk7IGdoaSgiZG9uZ190aGVtIiwgdGhlbSk7IGdoaSgiZG9uZ194b2EiLCB4b2Ep'
'CiAgICBmb3IgaCBpbiBoYW5nOiBpbm4oZiIgICAge2hbMl06MzR9ICt7aFswXTo8NX0gLXtoWzFdfSIpCiAgICBpbm4oZiIg'
'ICAgVE9ORzoge2xlbihoYW5nKX0gdGVwLCAre3RoZW19LCAte3hvYX0gICAodHJhbjoge1RSQU5fVEVQfSB0ZXAgLyB7VFJB'
'Tl9ET05HfSBkb25nIHRoZW0pIikKICAgIGNoYW0gPSBzb3J0ZWQoe2hbMl0gZm9yIGggaW4gaGFuZ30gJiBXUklURV9TRVRf'
'RzIpOyBnaGkoImNoYW1fd3JpdGVfc2V0IiwgY2hhbSkKICAgIGRlZiBfY2FfbW9pX2NvKHJldik6CiAgICAgICAgIyBjYXQt'
'ZmlsZSwga2hvbmcgYHNob3dgOiBgZ2l0IHNob3dgIGNoZXQgdm9pIGNhdSBoaW5oIFVJIGdvIHNhaSAoZG8gdHJlbiAyMDI2'
'LTA5LTMwaTogbG9nLmRhdGUgZ28gc2FpID0+IGJhbiAzMGkgZ29pCiAgICAgICAgIyAwZWE5NWRlIGxhICJraG9uZyBwaGFp'
'IHVuZyB2aWVuIC4uLiBOb25lIOKAlCBkYSBsYW5kPyBuaGFtIG5oYW5oPyIpLgogICAgICAgIHJfLCBuZF8sIF8gPSBnaXQo'
'Z29jLCAiY2F0LWZpbGUiLCAiLXAiLCBmIntyZXZ9Om9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAgIHJldHVy'
'biBOb25lIGlmIHJfIGVsc2Uge3QgZm9yIHQgaW4gQ0FfTU9JX0cyIGlmIHJlLnNlYXJjaChyIig/bSleZGVmICIgKyB0ICsg'
'ciJbYS16XT9fIiwgbmRfKX0KICAgIG9fbWIsIG9faCA9IF9jYV9tb2lfY28obWIpLCBfY2FfbW9pX2NvKGhlYWQpCiAgICBt'
'YW5nID0gc29ydGVkKG9faCAtIG9fbWIsIGtleT1zb19jYSkgaWYgKG9fbWIgaXMgbm90IE5vbmUgYW5kIG9faCBpcyBub3Qg'
'Tm9uZSkgZWxzZSBOb25lCiAgICBnaGkoImNhX21vaV9nMl9tYW5nX3ZhbyIsIG1hbmcpCiAgICBpZiBub3QgbWFuZzoKICAg'
'ICAgICAjIERvIFJPTkcgKGRhIGxhbmQsIGNoaW5oIG1hc3RlciksIG5oYW0gbmhhbmgsIGhheSBuaGFuaCBjdWEgcGFja2V0'
'IEtIQUMgY2hhbSBjdW5nIHRlcDoKICAgICAgICAjIGtob25nIG1hbmcgY2EgbW9pIG5hbyBjdWEgZzIgdGhpIGtob25nIHBo'
'YWkgdW5nIHZpZW4uIERvYyBraG9uZyBkdW9jIChOb25lKSBjdW5nIHZheS4KICAgICAgICBrZXQoIk43JyBraWNoIHRodW9j'
'IiwgS0RELCBmImRvaSB0dW9uZyBraG9uZyBwaGFpIHVuZyB2aWVuOiB7bGVuKGhhbmcpfSB0ZXAsIGNoYW0ge2NoYW19LCBj'
'YSBtb2kgIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiZzIgbWFuZyB2YW8ge21hbmchcn0g4oCUIGRh'
'IGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPyIpCiAgICBlbHNlOgogICAgICAgICMgbnVtc3RhdCBpbiBgLWAgKGto'
'b25nIGNvIHNvIGRvbmcpIGNobyB0ZXAgYmluYXJ5Ly1kaWZmIHRoZW8gYXR0cmlidXRlcyDigJQga2UgY2EgYXR0cmlidXRl'
'cyBDVUEgTkdVT0kgRE8gKGRvIHRyZW4KICAgICAgICAjIDIwMjYtMDktMzBnOiBjb3JlLmF0dHJpYnV0ZXNGaWxlIGAqLnB5'
'IC1kaWZmYCA9PiAiMiB0ZXAgLyArMCIgREFUIGNobyAwZWE5NWRlLCB0aGF0ICszOTcpLiBgLWAgbGEgS0hPTkcgRE8gRFVP'
'QywKICAgICAgICAjIGtob25nIHBoYWkgMDsgVFJVT1QgdGhlbyBzbyB0ZXAgLyBzbyBkb25nIERBIGRlbSBkdW9jIHZhbiBn'
'aXUgKHF1YW4gc2F0IHRydWMgdGllcCkuCiAgICAgICAga2hvbmdfc28gPSBbaFsyXSBmb3IgaCBpbiBoYW5nIGlmIG5vdCAo'
'aFswXS5pc2RpZ2l0KCkgYW5kIGhbMV0uaXNkaWdpdCgpKV07IGdoaSgidGVwX2tob25nX3NvX2RvbmciLCBraG9uZ19zbykK'
'ICAgICAgICB2dW90ID0gbGVuKGhhbmcpID4gVFJBTl9URVAgb3IgdGhlbSA+IFRSQU5fRE9ORwogICAgICAgIGtldCgiTjcn'
'IGtpY2ggdGh1b2MiLCBUUlVPVCBpZiB2dW90IGVsc2UgKEtERCBpZiBraG9uZ19zbyBlbHNlIERBVCksCiAgICAgICAgICAg'
'IGYie2xlbihoYW5nKX0gdGVwIC8gK3t0aGVtfSIgKyAoZiIg4oCUIG51bXN0YXQgS0hPTkcgY28gc28gZG9uZyBjaG8ge2to'
'b25nX3NvfSIgaWYga2hvbmdfc28gZWxzZSAiIikpCgojIENvbmcga2ljaCB0aHVvYyBQSEFJIGRlIGxhaSBNT1Qga2V0IHF1'
'YS4gTGVuaCBudW1zdGF0IGhvbmcgdGhpIG5oYW5oIGBpZiByYzogcGFzc2Aga2hvbmcgZ2hpIGdpLCB2YSB2YW5nIG1hdCBv'
'IGRheQojIHRoYW5oIERBVCBvIGJvIGdvcDogY2F1IGhpbmggZGlmZiBDVUEgTkdVT0kgRE8gaG9uZyAoZGlmZi5vcmRlckZp'
'bGUgdHJvIHRlcCBraG9uZyBjbywgZGlmZi5hbGdvcml0aG0gZ28gc2FpID0+IHJjPTEyOCkgY2hvCiMgLS1jaGkta2ljaC10'
'aHVvYyByYz0wIHZvaSAwIGNob3QsIGx1b3QgZGF5IGR1ICJEQVQgMTEiIHJjPTAgKGRvIHRyZW4gMjAyNi0wOS0zMGgsIDBl'
'YTk1ZGUpLiBWYW5nIG1hdCBsYSBLSE9ORyBETyBEVU9DLgojIFR1IDMwaiBudW1zdGF0IGxhIGRpZmYtdHJlZSAoa2hvbmcg'
'ZG9jIGhhaSBraG9hIGF5KTsgZHVvbmcgY29uIGxhaSBkbyBkdW9jOiBkaWZmLnJlbmFtZUxpbWl0IGdvIHNhaSA9PiByYz0x'
'MjguCmlmIG5vdCBhbnkoY1swXSA9PSAiTjcnIGtpY2ggdGh1b2MiIGZvciBjIGluIGNob3QpOgogICAga2V0KCJONycga2lj'
'aCB0aHVvYyIsIEtERCwgZiJjb25nIEtIT05HIHJhIGtldCBxdWEgKGdpdCBkaWZmLXRyZWUgLS1udW1zdGF0IHJjPXtyY30p'
'OiB7X2FuX3VzZXJpbmZvKGVyKVs6NzBdfSIpCgojIERpbmggZGFuaCBUSEFUIG5hbSBvIE43JyAoY2EgbW9pIGcyIG1hbmcg'
'dmFvKSwgS0hPTkcgbyAiaGF1IGR1ZSBnMSI6IGcxIGRhIGxhbmQgbmVuIG1vaSBuaGFuaCBkZXUKIyBsYSBoYXUgZHVlLiBE'
'b25nIGRhdSBraG9pIGRhbiBwaGFpIHR1IGtoYWkgdGhlbyBrZXQgcXVhIGF5IChkbyBkdW9jOiBtYXN0ZXIgNDQ2MjBlOCBt'
'byBraG9pIGJhbmcKIyAiVEhFIEhFIERPIERVT0M6IGcyIiwgSlNPTiAidGhlX2hlIjogImcyIiwgdHJvbmcga2hpIE43JyBk'
'YSBrZXQgbHVhbiAia2hvbmcgcGhhaSB1bmcgdmllbiIpLgojIE5oYW4gY2hpIGR1b2Mgbm9pIERVTkcgY2FpIGRvIGR1b2M6'
'IGBbXWAga2hvbmcgdGFjaCAiZGEgbGFuZCIga2hvaSAibmhhbSBuaGFuaCIvInBhY2tldCBraGFjIiAoZG8KIyBkdW9jIHRy'
'ZW4gMjAyNi0wOS0zMGI6IHVuZyB2aWVuIDJhNjc5NjggREEgTEFORCBiaSBnb2kgIktIT05HIHBoYWkgdW5nIHZpZW4gZzIi'
'KS4KaWYgdGhlX2hlID09ICJnMiIgYW5kIG5vdCBzby5nZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpOgogICAgdGhlX2hlID0g'
'KCJLSE9ORyBtYW5nIGNhIG1vaSBnMiBuYW8gKGRhIGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPykiIGlmIHNvLmdl'
'dCgiY2FfbW9pX2cyX21hbmdfdmFvIikgPT0gW10KICAgICAgICAgICAgICBlbHNlICJnMj8gKENIVUEgZGluaCBkYW5oIGR1'
'b2MgZG9pIHR1b25nKSIpCiAgICBnaGkoInRoZV9oZSIsIHRoZV9oZSkKCiMgQ29uZyBuaGFuaDogZG8gUklFTkcga2ljaCB0'
'aHVvYyAodmFpIGdpYXkpIHJvaSBkdW5nLiBEdW5nIGtoaSBjYW4geGFjIG1pbmggbGFpCiMgdmUgbmVuIG1hIGtob25nIG11'
'b24gdHJhIDIwLTQ1IHBodXQgY2hvIGNhIGJvIHRlc3QuCmlmICItLWNoaS1raWNoLXRodW9jIiBpbiBzeXMuYXJndjoKICAg'
'IGlubigiIik7IGlubigiPSIgKiA3OCkKICAgIGlubigiLS1jaGkta2ljaC10aHVvYzogQ0hJIGRvIGNvbmcga2ljaCB0aHVv'
'Yy4gRGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQogICAgaW5uKCItIiAqIDc4KQogICAgZm9yIF90LCBf'
'dHQsIF9jdCBpbiBjaG90OiBpbm4oZiIgIHtfdHQ6MTR9IHtfdH0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkK'
'ICAgIF9rID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKICAgIF9yID0gc3VtKDEgZm9yIF8sIHQs'
'IF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQogICAgc3lzLmV4aXQoMyBpZiBfayBlbHNlICgxIGlmIF9yIGVsc2UgMCkpCgpD'
'SElfUFJPQkUgPSAiLS1jaGktcHJvYmUiIGluIHN5cy5hcmd2ICAgICMgYm8gcXVhIGJvIHRlc3QgKyBONzsgZ2l1IDAsIDEs'
'IDMKIyAtLS0tLS0tLS0tLS0tLS0tIDIuIGJvIHRlc3QgZGF5IGR1IC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENISV9QUk9C'
'RToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMi4gQk8gVEVTVCBEQVkgRFUgKDEwLTQwIHBodXQpIikKICAg'
'IHJjX24sIG91dF9uID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgZ29jKQogICAgZ2hpKCJyY19zdWl0'
'ZSIsIHJjX24pCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0X24pCiAgICBpbm4oIiAgcmMgPSIsIHJjX24sICJ8IiwgbS5n'
'cm91cCgwKSBpZiBtIGVsc2UgIihLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcga2V0KSIpCiAgICBpZiBtOgogICAgICAgIGdo'
'aSgiZGF0IiwgaW50KG0uZ3JvdXAoMSkpKTsgZ2hpKCJ0cmVuIiwgaW50KG0uZ3JvdXAoMikpKTsgZ2hpKCJib19xdWFfc28i'
'LCBpbnQobS5ncm91cCg0KSkpCiAgICBkb19oZXQsIGdjLCB0aW4gPSBkb2NfZG8ob3V0X24pCiAgICBnaGkoInNvX2NhX2Rv'
'IiwgbGVuKGRvX2hldCkpOyBnaGkoImxpZXRfa2VfZGF5X2R1IiwgdGluKQogICAgZm9yIGcgaW4gZ2M6IGlubigiICAgKiIs'
'IGcpCiAgICBpbm4oIiIpOyBpbm4oZiIgID09PSB7bGVuKGRvX2hldCl9IENBIERPID09PSIpCiAgICBmb3IgdCBpbiBzb3J0'
'ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGlubihmIiAgIHt0LnNwbGl0KCdfJylbMF06N30ge3R9Iik7IGlubihm'
'IiAgICAgICAgICAge2RvX2hldFt0XVs6MTUwXX0iKQogICAgZ2hpKCJkb19seV9kbyIsIHt0OiBkb19oZXRbdF1bOjMwMF0g'
'Zm9yIHQgaW4gZG9faGV0fSkKICAgICMgLS0tLSBDSE9UOiBtb2kgY2EgRE8gcGhhaSBHSUFJIFRISUNIIERVT0MgLS0tLQog'
'ICAgIyBUaGlldSBjaG90IG5heSwgYm8gZG8gaW4gZGFuaCBzYWNoIGRvIHJvaSB2YW4gdGhvYXQgcmM9MC4gRG8gZHVuZyBs'
'YSBsb2kgZGEgeGF5IHJhOgogICAgIyBsdW90IFdpbmRvd3MgMTktMDkgY28gdDE3MSBETyBtYSBibyBkbyBiYW8gIkRBVCAx'
'MCB8IFRSVU9UIDAiIHZhIHJjPTAuCiAgICBkZWYgX2tob2EodCk6IHJldHVybiB0LnNwbGl0KCJfIilbMF0KICAgIGRvX3Bh'
'Y2tldCwgZG9fbGEsIGRvX3RoaWV1X2NvbmdfY3UgPSBbXSwgW10sIFtdCiAgICBmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBr'
'ZXk9c29fY2EpOgogICAgICAgIGssIGx5ID0gX2tob2EodCksIGRvX2hldFt0XQogICAgICAgIGlmIGsgaW4gQ0FfUEFDS0VU'
'OiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRvX3BhY2tldC5hcHBlbmQodCkKICAgICAgICBlbGlmICJLSMOUTkcg'
'xJBPIMSQxq/hu6JDIiBpbiBseSBvciAidGhp4bq/dSBgIiBpbiBseTogIGRvX3RoaWV1X2NvbmdfY3UuYXBwZW5kKHQpCiAg'
'ICAgICAgZWxpZiBrIGluIE5HT0FJX1BIQU1fVkk6ICAgICAgICAgICAgICAgICAgICAgICAgcGFzcwogICAgICAgIGVsc2U6'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRvX2xhLmFwcGVuZCh0KQogICAgZ2hpKCJkb19w'
'YWNrZXQiLCBkb19wYWNrZXQpOyBnaGkoImRvX2xhIiwgZG9fbGEpOyBnaGkoImRvX3RoaWV1X2NvbmdfY3UiLCBkb190aGll'
'dV9jb25nX2N1KQogICAgaW5uKCIiKQogICAgaW5uKGYiICBjYSBETyB0aHVvYyBDSElOSCBwYWNrZXQgbmF5IDoge1tfa2hv'
'YSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdIG9yICdraG9uZyBjbyd9IikKICAgIGlubihmIiAgY2EgRE8gbmdvYWkgcGhhbSB2'
'aSAocjMga2hhaSk6IHtbX2tob2EoeCkgZm9yIHggaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKSBpZiBfa2hvYSh4KSBp'
'biBOR09BSV9QSEFNX1ZJXX0iKQogICAgaW5uKGYiICBjYSBETyB2aSBUSElFVSBDT05HIENVICAgICAgIDoge1tfa2hvYSh4'
'KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XSBvciAna2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERPIExBIChraG9u'
'ZyBnaWFpIHRoaWNoIGR1b2MpOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXSBvciAna2hvbmcgY28nfSIpCiAgICAjIC0t'
'LS0gQ0hPVDogcGhlcCBkbyBwaGFpIFRST04gdHJ1b2Mga2hpIG1vdCBjaHUgREFUIG5hbyBkdW9jIHBoYXQgLS0tLQogICAg'
'IyBCYW4gdHJ1b2MgY2hpIElOIGB0aW5gL2ByY19zdWl0ZWA6IGJvIHRlc3QgY2hldCBnaXVhIHQxNzEgKHJjPTEzNCwga2hv'
'bmcgZG9uZyB0b25nKQogICAgIyB2YW4gcmEgIkRBVCAxMiB8IFRSVU9UIDAiIHJjPTA7IGNhIFBBQ0tFVCB2YW5nIG1hdCBo'
'YXkgYmkgQk8gUVVBIGN1bmcgZHVvYyBjaGFtIG5odQogICAgIyAia2hvbmcgZG8iLiBWYW5nIG1hdCBraG9uZyBwaGFpICJr'
'aG9uZyBkbyIg4oCUIGxhIEtIT05HIERPIERVT0MuCiAgICB2YW5nID0gW3QgZm9yIHQgaW4gc29ydGVkKENBX1BBQ0tFVCwg'
'a2V5PXNvX2NhKSBpZiBtYXVfY2Eob3V0X24sIHQpIG5vdCBpbiAoIlFVQSIsICJETyIpXQogICAgbHlfa2RkID0gW10KICAg'
'IGlmIG5vdCB0aW46IGx5X2tkZC5hcHBlbmQoImRhbmggc2FjaCBkbyBLSE9ORyBkYXkgZHUiKQogICAgaWYgcmNfbiBub3Qg'
'aW4gKDAsIDEpIG9yIChyY19uID09IDEpICE9IGJvb2woZG9faGV0KToKICAgICAgICBseV9rZGQuYXBwZW5kKGYicmMgYm8g'
'dGVzdD17cmNfbn0ga2hvbmcga2hvcCB7bGVuKGRvX2hldCl9IGNhIERPIGRvYyBkdW9jIikKICAgIGlmIHZhbmc6IGx5X2tk'
'ZC5hcHBlbmQoZiJjYSBQQUNLRVQgdmFuZy9ibyBxdWE6IHt2YW5nfSIpCiAgICBnaGkoImNhX3BhY2tldF92YW5nIiwgdmFu'
'Zyk7IGdoaSgibHlfZG9fY2h1YV90cm9uIiwgbHlfa2RkKQogICAgaWYgbHlfa2RkOiBrZXQoIkJvIHRlc3QgY2hheSBUUk9O'
'IHZhIGRvYyBEVSIsIEtERCwgIjsgIi5qb2luKGx5X2tkZCkpCiAgICBjaHVhX3Ryb24gPSBLREQgaWYgbHlfa2RkIGVsc2Ug'
'REFUCiAgICBrZXQoIktob25nIGNhIG5hbyBjdWEgUEFDS0VUIGJpIERPIiwgY2h1YV90cm9uIGlmIG5vdCBkb19wYWNrZXQg'
'ZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9fcGFja2V0IGVsc2UgZiJETzoge1tfa2hvYSh4KSBmb3IgeCBpbiBk'
'b19wYWNrZXRdfSDigJQgYmFuIHZhIENIVUEgeG9uZyIpCiAgICBrZXQoIk1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9j'
'IiwgY2h1YV90cm9uIGlmIG5vdCBkb19sYSBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19sYSBlbHNlIGYibGE6'
'IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdfSIpCiAgICBpZiBkb190aGlldV9jb25nX2N1OgogICAgICAgIGtldCgiQ29u'
'ZyBjdSBkYXkgZHUgZGUgZG8iLCBLREQsIGYidGhpZXUgY29uZyBjdSBjaG8ge1tfa2hvYSh4KSBmb3IgeCBpbiBkb190aGll'
'dV9jb25nX2N1XX0iKQoKICAgIGJxID0gc29ydGVkKHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91dF9uKX0s'
'IGtleT1zb19jYSk7IGdoaSgiY2FfYm9fcXVhIiwgYnEpCiAgICBpbm4oIiIpOyBpbm4oZiIgIEJPIFFVQSAoe2xlbihicSl9'
'KToge1t4LnNwbGl0KCdfJylbMF0gZm9yIHggaW4gYnFdfSIpCgogICAgaW5uKCIiKTsgaW5uKCIgIE4xLU40ICh0MTY1LXQx'
'NjgpLCB0aWV1IGNoaSBuZ2hpZW0gdGh1IGN1YSByMiwgbmF5IGxhIGNoaSBiYW8gaG9pIHF1eToiKQogICAgYjQgPSB7dDog'
'bWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQU1PSX07IGdoaSgiY2FfbW9pIiwgYjQpCiAgICBmb3IgdCBpbiBDQU1PSTog'
'aW5uKGYiICAgICB7dH06IHtiNFt0XX0iKQogICAgIyBCT19RVUEvdmFuZyBsYSBDSFVBIENIQVksIGtob25nIHBoYWkgRE86'
'IGNoaSBtb3QgY2EgRE8gbW9pIGR1b2MgcGhhdCBUUlVPVC4KICAgIGtldCgiTjEtTjQgKHQxNjUtdDE2OCkiLCBEQVQgaWYg'
'YWxsKHYgPT0gIlFVQSIgZm9yIHYgaW4gYjQudmFsdWVzKCkpCiAgICAgICAgZWxzZSAoVFJVT1QgaWYgYW55KHYgPT0gIkRP'
'IiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkgZWxzZSBLREQpLCBzdHIoYjQpKQoKICAgIGlubigiIik7IGlubigiICAxNSBjYSB0'
'dW5nIGRvIHRyZW4gQ0k6IikKICAgIGIxNSA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBMTV9OyBnaGkoImNh'
'MTUiLCBiMTUpCiAgICBpbm4oIiAgICAiICsgIiAgIi5qb2luKGYie3R9OntiMTVbdF19IiBmb3IgdCBpbiBDQTE1KSkKCiAg'
'ICAjIHQxMzYg4oCUIE4xMiBkbyBHSUFOIFRJRVAgcXVhIGtldCBxdWEgY2EKICAgIHQxMzZfdGVuID0gbmV4dCgodCBmb3Ig'
'dCBpbiBkb19oZXQgaWYgdC5zdGFydHN3aXRoKCJ0MTM2IikpLCBOb25lKQogICAgaWYgYjE1LmdldCgidDEzNiIpID09ICJR'
'VUEiOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIERBVCwgInQxMzYgUVVBIikKICAgIGVsaWYg'
'YjE1LmdldCgidDEzNiIpICE9ICJETyI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgS0RELCBm'
'InQxMzYgPSB7YjE1LmdldCgndDEzNicpIXJ9IOKAlCBraG9uZyBjaGF5L2tob25nIHRoYXkiKQogICAgZWxzZToKICAgICAg'
'ICBseSA9IGRvX2hldC5nZXQodDEzNl90ZW4sICIiKQogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIs'
'IFRSVU9ULCBmIkRPOiB7bHlbOjkwXX0iKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDMuIHByb2JlIFRIQU5HIHZhbyBoYW0gLS0t'
'LS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjMuIFBST0JFIFRIQU5HIOKAlCBnb2kgX2dpdF93'
'aW5kb3dzIHZvaSB0aGFtIHNvIHRpZW0iKQpzcGVjID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24o'
'ImxwNTQxIiwgc3RyKHRlcCkpCmxwID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhzcGVjKTsgc3BlYy5sb2Fk'
'ZXIuZXhlY19tb2R1bGUobHApCnNpZyA9IGluc3BlY3Quc2lnbmF0dXJlKGxwLl9naXRfd2luZG93cykKZ2hpKCJ0aGFtX3Nv'
'X19naXRfd2luZG93cyIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQppbm4oIiAgdGhhbSBzbyBjdWEgX2dpdF93aW5kb3dzOiIs'
'IGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQoKZGVmIGdvaSgqKmt3KToKICAgICIiIkdvaSBfZ2l0X3dpbmRvd3MsIEJBVCBzdGRl'
'cnIgZGUgbW90IGRvbmcgY2hhbiBkb2FuIGtob25nIGdpZXQgbHVvdCBkby4iIiIKICAgIGUgPSBpby5TdHJpbmdJTygpCiAg'
'ICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgogICAgICAgIHIgPSBscC5fZ2l0X3dpbmRvd3MoKiprdykK'
'ICAgIHJldHVybiByLCBlLmdldHZhbHVlKCkKCiMgLS0tIGRvaSBjaHVuZyByaWc6IHBoYWkgdHJhIGxvaSBkdW5nIG1vdCBj'
'YSB0YSBCSUVUIFRSVU9DIGRhcCBhbiAtLS0Kd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAg'
'bmdvYWkgPSBQYXRoKHQpLyJuZ29haSI7IG5nb2FpLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsg'
'cGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIChuZ29haS8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNv'
'ZGluZz0idXRmLTgiKQogICAgcjEsIF8gPSBnb2kocGF0aD1zdHIobmdvYWkpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3'
'ZD1zdHIoY3cpKQogICAgKGN3LyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMiwg'
'XyA9IGdvaShwYXRoPXN0cihjdyksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCnJpZ19vayA9IGJvb2wo'
'cjEpIGFuZCByMiBpcyBOb25lCmdoaSgicmlnX2RvaV9jaHVuZyIsIHJpZ19vaykKa2V0KCJSSUcgZG9pIGNodW5nIChiaWV0'
'IHRydW9jIGRhcCBhbikiLCBEQVQgaWYgcmlnX29rIGVsc2UgS0RELAogICAgZiJuZ29haS1jd2QtPnsnTkhBTicgaWYgcjEg'
'ZWxzZSAnTm9uZSd9IHwgdHJvbmctY3dkLT57J05IQU4nIGlmIHIyIGVsc2UgJ05vbmUnfSIpCmlmIG5vdCByaWdfb2s6CiAg'
'ICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IHJpZyBzYWksIG1vaSBjaG90IGR1b2kgc2Ugdm8gbmdoaWEuIik7IHN5'
'cy5leGl0KDMpCgojIC0tLSBNT0kgQ09ORyBQSEFJIFRVIENIVU5HIE1JTkggTk8gQ08gVEhFIERPIC0tLQojIEJhaSBob2Mg'
'ZGF0IG5oYXQgY3VhIHBhY2tldCBuYXk6IGRvX24xMCBiYW4gY3UgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0'
'MTcxCiMgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQgbWEgTjEwIHNpbmggcmEgZGUgYmF0LiBO'
'byBkZWdlbmVyYXRlIOKAlAojIHRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyBuZW4gInRhY2ggZHVuZyIgdmEg'
'InRhY2ggc2FpIiBjaG8gY3VuZyBrZXQgcXVhLgojIE1vdCBjb25nIGtob25nIHRoZSBETyB0aGkga2hvbmcgcGhhaSBjb25n'
'LCB2YSBubyBuZ3V5IGhpZW0gaG9uIGtob25nIGNvIGNvbmc6IG5vCiMgcGhhdCByYSBtb3QgY2h1IERBVC4KIwojIE5lbiB0'
'cnVvYyBraGkgRFVORyBuYW0gY29uZyBuYXkgZGUgcGhhbiBxdXlldCwgYmF0IHR1bmcgY29uZyBnaWV0IG1vdCBkb3QgYmll'
'biBkYQojIGJpZXQgdHJvbmcuIENvbmcgbmFvIGtob25nIGdpZXQgZHVvYyB0aGkgY2h1IERBVCBjdWEgbm8gYmkgSEEgeHVv'
'bmcgS0hPTkcgRE8gRFVPQzsKIyBUUlVPVCBnaXUgbmd1eWVuIChxdWFuIHNhdCB0cnVjIHRpZXAsIHZkLiBnMSB2YW4gbmhh'
'biBnaXQuYmF0KS4gRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaQojIGR1bmcgdG9p'
'IChjdW5nIGt5IGx1YXQgbmh1IE43KS4KRE9UX0JJRU5fVFVfS0lFTSA9IFsKICAgICgiTjgiLCAib3BzL2xlYXNlX3B1Ymxp'
'c2gucHkiLAogICAgICdpZiBjaGlfZGluaCBhbmQgUGF0aChjaGlfZGluaCkubmFtZS5sb3dlcigpID09ICJnaXQuZXhlIiBh'
'bmQgaG9wX2xlKGNoaV9kaW5oKTonLAogICAgICJpZiBjaGlfZGluaCBhbmQgaG9wX2xlKGNoaV9kaW5oKToiKSwKICAgICgi'
'TjkiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJkID0gZF9yYXcuc3RyaXAoKS5zdHJpcCgnXCInKSIsICJkID0g'
'ZF9yYXcuc3RyaXAoKSIpLAogICAgKCJOMTAiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJzZXAgPSBvcy5wYXRo'
'c2VwIGlmIHBoYW5fY2FjaCBpcyBOb25lIGVsc2UgcGhhbl9jYWNoIiwgInNlcCA9IG9zLnBhdGhzZXAiKSwKICAgICgiTjEx'
'IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwgImlmIGNoYW5fZG9hbiBpcyBub3QgTm9uZToiLCAiaWYgRmFsc2U6IiksCiAg'
'ICAoIk4xMiIsICJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IiwKICAgICAnZ2l0X3BhdGg9Ii8va2hvbmctY28vZ2l0Iics'
'ICdnaXRfcGF0aD0iL2tob25nLWNvL2dpdCInKSwKXQppbm4oIiIpOyBpbm4oIiAgdHUga2llbSBjb25nIOKAlCBtb2kgY29u'
'ZyBwaGFpIGdpZXQgZHVvYyBtb3QgZG90IGJpZW4gZGEgYmlldDoiKQpnaWV0ID0ge30KZm9yIG1hLCBkdW9uZywgdGltLCB0'
'aGF5IGluIERPVF9CSUVOX1RVX0tJRU06CiAgICBfdGVuLCBfaGFtID0gbmV4dCgoKGEsIGIpIGZvciBhLCBiIGluIFBST0JF'
'IGlmIGEuc3RhcnRzd2l0aChtYSArICIgIikpLCAoTm9uZSwgTm9uZSkpCiAgICBpZiBfaGFtIGlzIE5vbmU6CiAgICAgICAg'
'Z2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IGtob25nIHRpbSB0aGF5IHByb2JlIHRl'
'biAne21hfSAuLi4nIik7IGNvbnRpbnVlCiAgICB0cnk6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3Rv'
'cnkoKSBhcyBfdDoKICAgICAgICAgICAgX2MgPSBQYXRoKF90KS8iY2F5Ijsgc2h1dGlsLmNvcHl0cmVlKGdvYy8ib3BzIiwg'
'X2MvIm9wcyIpCiAgICAgICAgICAgIF9mID0gX2MvZHVvbmc7IF9uZCA9IF9mLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgi'
'KQogICAgICAgICAgICBpZiBfbmQuY291bnQodGltKSAhPSAxOgogICAgICAgICAgICAgICAgZ2lldFttYV0gPSBOb25lCiAg'
'ICAgICAgICAgICAgICBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IG1hdSBkb3QgYmllbiBraG9wIHtfbmQuY291'
'bnQodGltKX0gbGFuIChtb25nIDEpIgogICAgICAgICAgICAgICAgICAgIGYiIOKAlCBtYSBuZ3VvbiBkYSBkb2ksIGRvdCBi'
'aWVuIG5heSBoZXQgeSBuZ2hpYSIpOyBjb250aW51ZQogICAgICAgICAgICBfZi53cml0ZV90ZXh0KF9uZC5yZXBsYWNlKHRp'
'bSwgdGhheSwgMSksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIF9zcCA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJv'
'bV9maWxlX2xvY2F0aW9uKCJscF9kYl8iICsgbWEsIHN0cihfYy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQogICAgICAg'
'ICAgICBfbSA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShf'
'bSkKICAgICAgICAgICAgZGVmIF9nb2lfZGIoKiprdyk6CiAgICAgICAgICAgICAgICBfZSA9IGlvLlN0cmluZ0lPKCkKICAg'
'ICAgICAgICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoX2UpOgogICAgICAgICAgICAgICAgICAgIHJl'
'dHVybiBfbS5fZ2l0X3dpbmRvd3MoKiprdyksIF9lLmdldHZhbHVlKCkKICAgICAgICAgICAgX3R0LCBfY3QsIF8gPSBfaGFt'
'KF9nb2lfZGIsIGluc3BlY3Quc2lnbmF0dXJlKF9tLl9naXRfd2luZG93cyksCiAgICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICBfYy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBnaWV0W21hXSA9IChfdHQgPT0gVFJVT1Qp'
'CiAgICAgICAgaW5uKGYiICAgIHttYTo0fSBkb3QgYmllbiAtPiB7X3R0OjE0fSB7J0dJRVQgRFVPQycgaWYgX3R0ID09IFRS'
'VU9UIGVsc2UgJ1NPTkcgU09UJ30iCiAgICAgICAgICAgICsgKGYiICAgKHtfY3R9KSIgaWYgX2N0IGVsc2UgIiIpKQogICAg'
'ZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcg'
'RE8gRFVPQzoge3R5cGUoX2UpLl9fbmFtZV9ffToge19lfSIpCmdoaSgiY29uZ19naWV0X2R1b2NfZG90X2JpZW4iLCBnaWV0'
'KQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwpIGluIFsodCwgZihnb2ksIHNpZywgdGVwdCkpIGZvciB0LCBmIGluIFBST0JFXToK'
'ICAgIGdoaSgicHJvYmVfIiArIHRlbi5zcGxpdCgpWzBdLmxvd2VyKCksIGRsKQogICAgaWYgaXNpbnN0YW5jZShkbCwgZGlj'
'dCk6CiAgICAgICAgZm9yIGssIHYgaW4gZGwuaXRlbXMoKTogaW5uKGYiICAgIHtrOjM0fToge3Z9IikKICAgIG1hID0gdGVu'
'LnNwbGl0KClbMF0KICAgIGlmIGdpZXQuZ2V0KG1hKSBpcyBub3QgVHJ1ZSBhbmQgdHQgPT0gREFUOgogICAgICAgICMgREFU'
'IHR1IG1vdCBjb25nIGNodWEgY2h1bmcgbWluaCBkdW9jIGxhIGJpZXQgRE8gdGhpIGtob25nIGRhbmcgdGluIGhvbiBLREQu'
'CiAgICAgICAga2V0KHRlbiwgS0RELCBmImNvbmcgS0hPTkcgZ2lldCBkdW9jIGRvdCBiaWVuIGN1YSBjaGluaCBubyAoe2dp'
'ZXQuZ2V0KG1hKSFyfSkiCiAgICAgICAgICAgICAgICAgICAgICBmIiAtPiBjaHUgREFUIG5heSBraG9uZyBjbyBnaWEgdHJp'
'IikKICAgIGVsc2U6CiAgICAgICAga2V0KHRlbiwgdHQsIGN0KQoKIyAtLS0tLS0tLS0tLS0tLS0tIDQuIE43IGRvdCBiaWVu'
'IHRyZW4gQkFOIFNBTyBUQU0gLS0tLS0tLS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCIt'
'IiAqIDc4KTsgaW5uKCI0LiBONyDigJQgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAoY2F5IHRoYXQgS0hPTkcgYmkgZHVu'
'ZyB0b2kpIikKICAgIHRydW9jID0gdGVwLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKQogICAg'
'Z2hpKCJuN190cnVvYyIsIHRydW9jKTsgaW5uKGYiICBzbyBkb25nIGtob3Age01BVV9XSU4hcn06IFRSVU9DID0ge3RydW9j'
'fSBbbW9uZyAxXSIpCiAgICBpZiB0cnVvYyAhPSAxOgogICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIs'
'IEtERCwgZiJtYXUgeHVhdCBoaWVuIHt0cnVvY30gbGFuLCBraG9uZyBwaGFpIDEiKQogICAgZWxzZToKICAgICAgICB3aXRo'
'IHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHRtcDoKICAgICAgICAgICAgc2FvID0gUGF0aCh0bXApLyJjYXki'
'CiAgICAgICAgICAgIHNodXRpbC5jb3B5dHJlZShnb2MsIHNhbywgaWdub3JlPXNodXRpbC5pZ25vcmVfcGF0dGVybnMoIi5n'
'aXQiLCAiX19weWNhY2hlX18iLCAiKi5weWMiKSkKICAgICAgICAgICAgZjIgPSBzYW8vIm9wcyIvImxlYXNlX3B1Ymxpc2gu'
'cHkiCiAgICAgICAgICAgIGYyLndyaXRlX3RleHQoZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJlcGxhY2UoTUFV'
'X1dJTiwgImlmIEZhbHNlOiIpLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBzYXUgPSBmMi5yZWFkX3RleHQoZW5j'
'b2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTik7IGdoaSgibjdfc2F1Iiwgc2F1KQogICAgICAgICAgICBpbm4oZiIgIFNB'
'VSAoZGEgZG90IGJpZW4pID0ge3NhdX0gW21vbmcgMF0iKQogICAgICAgICAgICBpZiBzYXUgIT0gMDoKICAgICAgICAgICAg'
'ICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgImRvdCBiaWVuIEtIT05HIGFwIGR1b2MiKQogICAg'
'ICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmNfbSwgb3V0X20gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVz'
'dC5weSJdLCBzYW8pCiAgICAgICAgICAgICAgICBtMTY1ID0gbWF1X2NhKG91dF9tLCAidDE2NSIpOyBkbSwgXywgXyA9IGRv'
'Y19kbyhvdXRfbSkKICAgICAgICAgICAgICAgIHRlbjE2NSA9IG5leHQoKHQgZm9yIHQgaW4gZG0gaWYgdC5zdGFydHN3aXRo'
'KCJ0MTY1IikpLCBOb25lKQogICAgICAgICAgICAgICAgbHkgPSAoZG0uZ2V0KHRlbjE2NSkgb3IgIiIpCiAgICAgICAgICAg'
'ICAgICBnaGkoIm43X3QxNjUiLCBtMTY1KTsgZ2hpKCJuN19seV9kbyIsIGx5WzoyMDBdKQogICAgICAgICAgICAgICAgaW5u'
'KGYiICB0MTY1IHNhdSBkb3QgYmllbjoge20xNjV9IHwge2x5WzoxMTBdfSIpCiAgICAgICAgICAgICAgICBkdW5nX2x5X2Rv'
'ID0gIlBBVEggdCIgaW4gbHkgb3IgIi91c3IvYmluIiBpbiBseQogICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBu'
'aGFuaCBXaW5kb3dzIiwgREFUIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pIGVsc2UKICAgICAgICAgICAgICAg'
'ICAgICAoVFJVT1QgaWYgbTE2NSA9PSAiRE8iIGVsc2UgS0REKSwKICAgICAgICAgICAgICAgICAgICAiZ2lldCBkdW5nIGx5'
'IGRvIiBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKQogICAgICAgICAgICAgICAgICAgIGVsc2UgKCJETyBuaHVu'
'ZyBLSE9ORyBkdW5nIGx5IGRvIC0+IHRpbiBkdW5nIGdpYSIgaWYgbTE2NSA9PSAiRE8iIGVsc2UgImtob25nIGRvYyBkdW9j'
'IHQxNjUiKSkKCiMgLS0tLS0tLS0tLS0tLS0tLSBLRVQgTFVBTiAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiPSIg'
'KiA3OCkKaW5uKGYiVEhFIEhFIERPIERVT0M6IHt0aGVfaGV9ICAgSEVBRD17aGVhZFs6MTJdfSIpCiMgS2hvaSBkYW4gY2hv'
'IHJldmlld2VyIGJhdCBkYXUgbyBkb25nIHRyZW4sIG5lbiBDSEUgRE8gcGhhaSBuYW0gTkdBWSBkdW9pIG5vOiBraG9uZyBj'
'byBkb25nIG5heQojIHRoaSBtb3QgbHVvdCAtLWNoaS1wcm9iZSBpbiAiREFUIDcgfCBUUlVPVCAwIHwgS0hPTkcgRE8gRFVP'
'QyAwIiByYz0wIG1hIGtob25nIG5vaSBsYSBjaHVhIGNoYXkgYm8gdGVzdC4KZ2hpKCJjaGVfZG8iLCAiY2hpLXByb2JlIiBp'
'ZiBDSElfUFJPQkUgZWxzZSAiZGF5LWR1IikKaWYgQ0hJX1BST0JFOgogICAgaW5uKCItLWNoaS1wcm9iZTogQ0hJIGRvIG11'
'YyAwLCAxLCAzLiBCbyB0ZXN0LCBOMS1ONCwgdDEzNiwgTjcgS0hPTkcgY2hheSAtIGRheSBLSE9ORyBwaGFpIG1vdCBsdW90'
'IG5naGllbSB0aHUuIikKaWYgdGhlX2hlID09ICJnMSI6CiAgICBpbm4oIkxVVSBZOiBkYXkgbGEgTkVOIERPIChnMSksIEtI'
'T05HIHBoYWkgbmdoaWVtIHRodSBnMi4gQ2FjIGNob3QgTjgtTjEyIGR1b2kgZGF5IikKICAgIGlubigiICAgICAgIFRSVU9U'
'IGxhIERVTkcgTkhVIE1PTkcg4oCUIGNodW5nIGxhIG5odW5nIGxvIGcyIHNpbmggcmEgZGUgdsOhLiIpCmlubigiLSIgKiA3'
'OCkKZm9yIHRlbiwgdHQsIGN0IGluIGNob3Q6CiAgICBpbm4oZiIgIHt0dDoxNH0ge3Rlbn0iICsgKGYiICAge2N0fSIgaWYg'
'Y3QgZWxzZSAiIikpCm5fa2RkID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKbl90cnVvdCA9IHN1'
'bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKaW5uKCItIiAqIDc4KQppbm4oZiIgIERBVCB7c3VtKDEg'
'Zm9yIF8sdCxfIGluIGNob3QgaWYgdD09REFUKX0gfCBUUlVPVCB7bl90cnVvdH0gfCBLSE9ORyBETyBEVU9DIHtuX2tkZH0i'
'KQppbm4oZiIgIFRvbmcgY2EgZG86IHtzby5nZXQoJ3NvX2NhX2RvJyl9IHwgZGFuaCBzYWNoIGRheSBkdTogeydDTycgaWYg'
'c28uZ2V0KCdsaWV0X2tlX2RheV9kdScpIGVsc2UgJ0tIT05HIERPIERVT0MnfSIpCmlubihmIiAgQWRtaW5pc3RyYXRvcjog'
'e3NvLmdldCgncXV5ZW5fYWRtaW4nKX0gfCBzeW1saW5rOiB7c28uZ2V0KCdzeW1saW5rX2R1b2MnKX0iKQppbm4oIiIpOyBp'
'bm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kgSlNPTiBOQVkgVkUgQ0hPIFJFVklFV0VSIC0tLSIpCmdoaSgiY2hvdCIsIFt7InRl'
'biI6IGEsICJ0cmFuZ190aGFpIjogYiwgImNoaV90aWV0IjogY30gZm9yIGEsIGIsIGMgaW4gY2hvdF0pCmlubihqc29uLmR1'
'bXBzKHNvLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0xLCBkZWZhdWx0PXN0cikpCiMgcmM6IDAgPSBtb2kgY2hvdCBE'
'QVQgfCAxID0gY28gY2hvdCBUUlVPVCB8IDMgPSBjbyBjaG90IEtIT05HIERPIERVT0MgKHV1IHRpZW4gYmFvIGRvbmcpCnN5'
'cy5leGl0KDMgaWYgbl9rZGQgZWxzZSAoMSBpZiBuX3RydW90IGVsc2UgMCkpCg=='
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
