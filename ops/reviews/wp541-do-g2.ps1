# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
# Luot DAY DU can SAN mot python >= 3.9 CO PyYAML >= 5.1 (pip install -U pyyaml): ban nhung python.org ma tep nay tu tai
# KHONG co PyYAML/pip, nen no chi du cho -ChiKichThuoc / -ChiProbe. Thieu thi dung o buoc cong cu, rc=3.
# Luot DAY DU con can `git` >= 2.36, `bash` (Git Bash), `actionlint` >= 1.7.7 (ban ghim CI), `shellcheck` (nhan --norc)
# tren PATH: tep nay KHONG tu cai chung (MinGit chi tai khi THIEU git); bo do hoi ngay o muc 0 va dung rc=3 neu thieu
# hoac cu hon (khong doi het bo test moi biet).
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
$ShaBoDo    = '3e74470baf6358a48cfb1be40ec587b291da9c0c876a58a2ed98301ebe7be215'      # SHA-256 cua bo do Python nhung ben duoi

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
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0xMC0wMWEiICAgICAgICAgICAgICAj'
'IGRvaSBNT0kga2hpIHN1YSBibyBkbyAtIGxvZyB0dSBraGFpIGJhbiBuYW8KVFJBTl9URVAsIFRSQU5fRE9ORyA9IDIsIDQw'
'MCAgICAgICAgICAjIE43JyBjdWEgc3BlYyByMwpBTF9TQU4gPSAoMSwgNywgNykgICAgICAgICAgICAgICAgICAgICMgc2Fu'
'IGFjdGlvbmxpbnQgPSBiYW4gZ2hpbSBDSTogQUxfVkVSIGN1YSBjaS55bWwgPSBiYW5fZ2hpbSBjdWEgb3BzL2NvbmdfY3Uu'
'eWFtbApHSVRfU0FOID0gKDIsIDM2LCAwKSAgICAgICAgICAgICAgICAgICMgc2FuIGdpdDogdW5nIHZpZW4gZ29pIGBnaXQg'
'd29ya3RyZWUgbGlzdCAtLXBvcmNlbGFpbiAtemAgKGNvIGAtemAgdHUgMi4zNik7IGJhbl9naGltIGdpdCA9IG51bGwKTUFV'
'X1dJTiAgPSAnaWYgbmVuX3RodWMgPT0gIndpbmRvd3MiOicKIyBXcml0ZSBzZXQgY3VhIHBhY2tldCAjNTQxIGcyLiBEaWZm'
'IGtob25nIGNoYW0gdGVwIG5hbyBvIGRheSA9PiBkbyBOSEFNIE5IQU5ILgpXUklURV9TRVRfRzIgPSB7Im9wcy9sZWFzZV9w'
'dWJsaXNoLnB5IiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkifQojICJUdW9pIiBjaGkgY28gbmdoaWEga2hpIHNvIHZv'
'aSBNQVkgQ0hVIFRIQVQuIE1vdCBtaXJyb3IgY3VjIGJvIGN1IGN1bmcgdHJhIGxzLXJlbW90ZSA9PQojIG9yaWdpbi9tYXN0'
'ZXIgKGRvIGR1b2M6IG1hc3RlciBjMTZiZDMyIC0+ICJ2ZSBuZW4gVFVPSSIsIDQ2IHRlcCAvICs3MTE4IGNobyAwZWE5NWRl'
'KS4KIyBEYW5oIHNhY2ggQ0hPIFBIRVA7IGByZW1vdGUgZ2V0LXVybGAgZGEga2hhaSB0cmllbiBpbnN0ZWFkT2YgbmVuIGNo'
'dXllbiBodW9uZyBjdW5nIGxvIHJhLgpVUkxfS0hPX0hPUF9MRSA9IHsiaHR0cHM6Ly9naXRodWIuY29tL2R1Y3RoYW5naG8v'
'dHJhLWx1YXQiLCAiaHR0cHM6Ly9naXRodWIuY29tL2R1Y3RoYW5naG8vdHJhLWx1YXQuZ2l0IiwKICAgICAgICAgICAgICAg'
'ICAgIyBTU0ggdG9pIENVTkcga2hvIChzYXUgX3VybF9zYWNoKTogYHVybC4iZ2l0QGdpdGh1Yi5jb206Ii5pbnN0ZWFkT2Yg'
'Imh0dHBzOi8vZ2l0aHViLmNvbS8iYAogICAgICAgICAgICAgICAgICAjIHJhdCBwaG8gYmllbiBvIG1heSBkZXY7IHRoaWV1'
'IGhhaSBkYW5nIG5heSB0aGkga2hvIFRIQVQgYmkgYmFvICJLSE9ORyBwaGFpIGtobyB0aGF0Ii4KICAgICAgICAgICAgICAg'
'ICAgInNzaDovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdCIsICJzc2g6Ly9naXRodWIuY29tL2R1Y3RoYW5naG8v'
'dHJhLWx1YXQuZ2l0IiwKICAgICAgICAgICAgICAgICAgImdpdEBnaXRodWIuY29tOmR1Y3RoYW5naG8vdHJhLWx1YXQiLCAi'
'Z2l0QGdpdGh1Yi5jb206ZHVjdGhhbmdoby90cmEtbHVhdC5naXQifQojIGByZW1vdGUgZ2V0LXVybGAgS0hBSSBUUklFTiBp'
'bnN0ZWFkT2YsIG1hIG1hdSBgdXJsLiJodHRwczovLzx0b2tlbj5AZ2l0aHViLmNvbS8iLmluc3RlYWRPZmAgcmF0IHBobwoj'
'IGJpZW4uIEluL2doaSBuZ3V5ZW4gdmFuIGxhIGR1YSBUT0tFTiB2YW8gbG9nIHZhIHZhbyBraG9pIEpTT04gcHMxIGJhbyBk'
'YW4gY2hvIHJldmlld2VyIChkbyBkdW9jOgojIDMgZG9uZyB0cm9uZyBraG9pIGRhbikuIEJvIHVzZXJpbmZvIFRSVU9DIGto'
'aSBpbiB2YSBUUlVPQyBraGkgc28g4oCUIHRva2VuIHZhbiBsYSBHaXRIdWIgdGhhdC4KIyBBdXRob3JpdHkga2V0IHRodWMg'
'byBgL2AsIGA/YCBob2FjIGAjYCBEQVUgVElFTiDigJQgZHVuZyBsdWF0IGdpdC9jdXJsLiBCYW4gYFteL10qQGAgbnVvdCBj'
'YSBgP2AvYCNgCiMgbmVuIG1vdCBVUkwgdHJvIHRvaSBNQVkgS0hBQyAoaG9zdCBkdW5nIHRydW9jIGA/YCwgZHVvaSBgP2Ag'
'bGEgYEBnaXRodWIuY29tLzxraG8+YCkgZHVvYyAibGFtIHNhY2giCiMgdGhhbmggZHVuZyBtb3QgbXVjIENITyBQSEVQLCB0'
'cm9uZyBraGkgZ2l0IG5vaSB0b2kgbWF5IGtpYSAoZG8gZHVvYzogbWlycm9yIGN1IHBodWMgdnUgcXVhIEhUVFBTID0+CiMg'
'InZlIG5lbiBUVU9JIiwgVFJVT1QgNDYgdGVwIC8gKzcxMTgpLiBWYW4gYm8gdG9pIGBAYCBDVU9JIHRyb25nIGF1dGhvcml0'
'eTogdXNlcmluZm8gY28gYEBgIHRyYW4gdGhpCiMgY3VybCB0dSBjaG9pICgiQmFkIGhvc3RuYW1lIiksIGNvbiBraGkgaW4g'
'dGhpIGtob25nIGxvIHBoYW4gc2F1IGBAYCB0aHUgbmhhdC4KX1JYX1VTRVJJTkZPID0gcmUuY29tcGlsZShyIl4oW0EtWmEt'
'el1bQS1aYS16MC05Ky4tXSo6Ly8pW14vPyNdKkAiKQpkZWYgX3VybF9zYWNoKHUpOiByZXR1cm4gX1JYX1VTRVJJTkZPLnN1'
'YihyIlwxIiwgdSBvciAiIikgICAgICAgICAgIyBkZSBTTyAobHVhdCBnaXQvY3VybCkKIyBJTiBwaGFpIGNoZSBST05HIGhv'
'biBTTzogbWF0IGtoYXUgY28gYD9gL2AjYCBUUkFOIHRoaSBgW14vPyNdKkBgIGtob25nIGtob3AgbmVuIFVSTCByYSBsb2cg'
'TkdVWUVOIFZBTgojIChkbyBkdW9jIHRyZW4gMjAyNi0wOS0zMGI6IDMgZG9uZyBvIC0tY2hpLWtpY2gtdGh1b2MsIDMgZG9u'
'ZyB0cm9uZyBraG9pIGRhbiAtLWNoaS1wcm9iZTsgYmFuIDMwYTogMCkuCiMgQ2hlIHRvaSBgQGAgQ1VPSSBDVU5HIGN1YSBD'
'QSBjaHVvaSAoY28gaGF5IGtob25nIGNvIHNjaGVtZSksIHZhIERFIERBVSBgKioqQGAgZGUgYmFuIGluIGtob25nIHR1IG5o'
'YW4gbGEKIyBnaXRodWIuY29tIGtoaSBnaXQgbm9pIHRvaSBtYXkga2hhYyAodmQuIGhvc3QgdHJ1b2MgYD9gKS4gQmFuIDMw'
'YyBjaGUgInRvaSBgQGAgY3VvaSB0cnVvYyBgL2AgZGF1IHRpZW4iCiMgbmVuIFZBTiBsbyBraGkgbWF0IGtoYXUgY28gYC9g'
'IHRyYW4sIGhvYWMgVVJMIGRhbmcgc2NwIGB1c2VyOm1rQGhvc3Q6ZHVvbmdgIChraG9uZyBzY2hlbWUpIOKAlCBkbyB0cmVu'
'CiMgMjAyNi0wOS0zMGM6IDMgZG9uZyAvIDEgdHJvbmcga2hvaSBkYW4gLS1jaGkta2ljaC10aHVvYywgNSAvIDMgbyAtLWNo'
'aS1wcm9iZSwgbW9pIGRhbmcuIE1vaSBreSB0dSBEVU5HCiMgbGEgbW90IGR1b25nIG51YTsgInRvaSBgQGAgY3VvaSIga2hv'
'bmcgY29uIGt5IHR1IGR1bmcgbmFvLiBIYWkgcXV5IHRhYywgaGFpIG11YyBkaWNoOiBTTyB0aGVvIGdpdCwgSU4KIyB0aGVv'
'ICJ0aHVhIGNvbiBob24gbG8iLiAiQ0EgY2h1b2kiIHBoYWkgZHVuZyBjYSBraGkgY2h1b2kgY28gWFVPTkcgRE9ORzogZ2l0'
'KCkgZG9jIGJhbmcgdGV4dD1UcnVlIG5lbiBDUi9MRiB0cm9uZyBVUkwKIyBkYSB0aGFuaCBMRiwgbWEgYC5gIGtob25nIGto'
'b3AgTEYuIFRva2VuIGRvYyB0dSB0ZXAgQ1JMRiAoYGh0dHBzOi8veC1hY2Nlc3MtdG9rZW46PHRva2VuPmAgKyBDUiArIGBA'
'Z2l0aHViLmNvbS8uLi5gKQojIHRoaSBiYW4gMzBlIEtIT05HIGNoZSBnaTogaW4gTkdVWUVOIHRva2VuIG8gZG9uZyBgb3Jp'
'Z2luIDpgIHZhIG8gIm9yaWdpbl91cmwiIHRyb25nIGtob2kgSlNPTiBkYW4gKGRvIHRyZW4gMjAyNi0wOS0zMGUpLgpkZWYg'
'X3VybF9pbih1KTogcmV0dXJuIHJlLnN1YihyIl4oW0EtWmEtel1bQS1aYS16MC05Ky4tXSo6Ly8pPy4qQCIsIHIiXDEqKipA'
'IiwgdSBvciAiIiwgZmxhZ3M9cmUuUykKIyBUaG9uZyBiYW8gbG9pIGN1YSBnaXQgQ0hJIGJvIHVzZXJpbmZvIHRvaSBgQGAg'
'REFVIFRJRU46IHVzZXJpbmZvIGNvIGBAYCB0cmFuICh2ZC4gdGVuIGRhbmcgbmhhcCBsYQojIGVtYWlsKSB0aGkgcGhhbiBz'
'YXUgdmFuIHJhIHN0ZGVyciBscy1yZW1vdGUsIG1hIHN0ZGVyciBheSBkdW9jIGluIHZhbyBkb25nIEtERCBjdWEgTjcnIChk'
'byBkdW9jOgojIDIgZG9uZyB0cm9uZyBsb2csIDEgdHJvbmcga2hvaSBkYW4pLiBMYW0gc2FjaCBNT0kgVVJMIHRyb25nIHZh'
'biBiYW4gdHJ1b2Mga2hpIGluIOKAlCBjaGUgdG9pIGBAYCBDVU9JIHRyZW4KIyBET05HIChjdW5nIGx1YXQgSU4gdm9pIF91'
'cmxfaW46IGtob25nIGNvbiBreSB0dSBkdW5nIG5hbykuIEJhbiAzMGQgZHVuZyBvIGBccyciYCBuZW4gcGhhbiBnaXQgZGUg'
'bGFpIGNvCiMgYCdgL2AiYC9raG9hbmcgdHJhbmcgKHZkLiBgdUB4OnAnPGJpIG1hdD5AZ2l0aHViLmNvbWApIFZBTiBsbyDi'
'gJQgZG8gdHJlbiAyMDI2LTA5LTMwZDogMiBkb25nIC8gMSB0cm9uZwojIGtob2kgZGFuIC0tY2hpLWtpY2gtdGh1b2MsIDMg'
'LyAyIG8gLS1jaGktcHJvYmUsIG1vaSBkYW5nLgpkZWYgX2FuX3VzZXJpbmZvKHQpOiByZXR1cm4gcmUuc3ViKHIiKFtBLVph'
'LXpdW0EtWmEtejAtOSsuLV0qOi8vKVteXG5dKkAiLCByIlwxKioqQCIsIHQgb3IgIiIpCiMgQ2EgbmdvYWkgcGhhbSB2aSBy'
'MyDCp25nb2FpX3BoYW1fdmkg4oCUIGRvIENISU5IIFNQRUMga2hhaSwga2hvbmcgcGhhaSBibyBkbyB0dSBxdXlldC4KIyBE'
'byBsYSBEQU5IIFNBQ0ggQ0hPIFBIRVA6IGNhIGRvIG5hbyBLSE9ORyBuYW0gdHJvbmcgZGF5IHZhIEtIT05HIHBoYWkgInRo'
'aWV1IGNvbmcgY3UiCiMgdGhpIGxhIFRSVU9ULiBEYW5oIHNhY2ggY2FtIHRoaSBiYW8gZ2lvIGN1bmcgdGhpZXU7IGRhbmgg'
'c2FjaCBjaG8gcGhlcCB0aGkgYmlldCB0cnVvYy4KTkdPQUlfUEhBTV9WSSA9IHNldCgidDEzMSB0MTMyIHQxNTAgdDEyNSB0'
'MzUgdDM2IHQzNyB0MzggdDM5IHQ0MCIuc3BsaXQoKSkKIyBDYSBjdWEgQ0hJTkggcGFja2V0IG5heS4gTW90IGNhIG8gZGF5'
'IG1hIERPIHRoaSBraG9uZyBiYW8gZ2lvIGR1b2MgYm8gcXVhLgpDQV9QQUNLRVQgPSBzZXQoInQxNjUgdDE2NiB0MTY3IHQx'
'NjggdDE2OSB0MTcwIHQxNzEgdDE3MiB0MTczIi5zcGxpdCgpKQojIENhIE1PSSBtYSBnMiB0aGVtIHZhbyAoTjgtTjEyKS4g'
'RG9pIHR1b25nIGRvIHBoYWkgTUFORyBjaHVuZyB2YW86IG1lcmdlLWJhc2UgY2h1YSBjbywgSEVBRCBjby4KQ0FfTU9JX0cy'
'ID0gInQxNjkgdDE3MCB0MTcxIHQxNzIgdDE3MyIuc3BsaXQoKQpDQTE1ICA9ICJ0MTI5IHQxMzAgdDEzMSB0MTMyIHQxMzMg'
'dDEzNiB0MTM4IHQxMzkgdDE0NCB0MTQ1IHQxNDYgdDE0NyB0MTQ5IHQxNTAgdDE1MSIuc3BsaXQoKQpDQU1PSSA9ICJ0MTY1'
'IHQxNjYgdDE2NyB0MTY4Ii5zcGxpdCgpCgpEQVQsIFRSVU9ULCBLREQgPSAiREFUIiwgIlRSVU9UIiwgIktIT05HIERPIERV'
'T0MiCnNvLCBjaG90ID0ge30sIFtdCmRlZiBnaGkoaywgdik6IHNvW2tdID0gdjsgcmV0dXJuIHYKZGVmIGtldCh0ZW4sIHRy'
'YW5nX3RoYWksIGNoaV90aWV0PSIiKToKICAgIGNob3QuYXBwZW5kKCh0ZW4sIHRyYW5nX3RoYWksIGNoaV90aWV0KSkKICAg'
'IGlubihmIiAgW3t0cmFuZ190aGFpOjE0fV0ge3Rlbn0iICsgKGYiICAge2NoaV90aWV0fSIgaWYgY2hpX3RpZXQgZWxzZSAi'
'IikpCiAgICByZXR1cm4gdHJhbmdfdGhhaQoKIyAtLS0tLS0tLS0tLS0tLS0tIGRvYyBsb2cgY3VhIGJvIHRlc3QgKGJhbiAz'
'LCBkYSBkbyB0cmVuIGxvZyBUSEFUKSAtLS0tLS0tLS0tLS0tLS0tClJYX0RPX0NITyAgPSByZS5jb21waWxlKHIiKD9tKV4h'
'ISEgZG8gKFxTKykgKC4qKSQiKQpSWF9ET19DVU9JID0gcmUuY29tcGlsZShyIig/bSleIHsyfShcU3sxLDR9KSB7Mn0oXFMr'
'KTogKC4qKSQiKQpSWF9CT19RVUEgID0gcmUuY29tcGlsZShyIig/bSleIHsyfVxTezEsNn0gUVVBIChcUyspOiAoLiopJCIp'
'CiMgRG9uZyB0b25nIGtldCBUSEFUIG8gREFVIGRvbmcuIENhIERPIGNvIHRoZSBpbiBsYWkgc3Rkb3V0IGN1YSBtb3QgbHVv'
'dCBDT04gKHQxNTUgY2hheSBsYWkgdDAxLCB0NzIvdDk4IGNoYXkKIyAiYm8iKSDigJQgZG9uZyB0b25nIExPTkcgYXkgbmFt'
'IEdJVUEgZG9uZyAoZG86IDIwIGRvbmcgbG9uZyBkZXUgbyBnaXVhIGRvbmcsIGNoaSBkb25nIHRvbmcgdGhhdCBvIGRhdSBk'
'b25nKSwgbWEKIyBgc2VhcmNoYCBraG9uZyBuZW8gYmF0IG5vIFRSVU9DLiBEbyB0cmVuIDIwMjYtMDktMzBjLCAwZWE5NWRl'
'ICsgZG90IGJpZW4gbGFtIHQwMSBETzogZG9jIHJhICIwLzEiID0+CiMgImRhbmggc2FjaCBLSE9ORyBkYXkgZHUiLCAiTEVD'
'SCBTTyBIT0M6IHRoaWV1IC0yMCBjYSIsIHRyb25nIGtoaSB0b25nIHRoYXQgMTY2LTE0NT0yMSA9PSAyMSBjYSBkb2MgZHVv'
'Yy4KUlhfVE9ORyAgICA9IHJlLmNvbXBpbGUociIoP20pXmxlYXNlX3B1Ymxpc2g6IChcZCspLyhcZCspXGJbXlxuXSo/PShc'
'ZCspLFteXG5dKj89KFxkKykiKQoKZGVmIHNvX2NhKHQpOgogICAgbSA9IHJlLm1hdGNoKHIidChcZCspIiwgdCk7IHJldHVy'
'biAoaW50KG0uZ3JvdXAoMSkpIGlmIG0gZWxzZSAxMCoqNiwgdCkKCmRlZiBkb2NfZG8ob3V0KToKICAgIHRhaV9jaG8gPSB7'
'dDogbC5zdHJpcCgpIGZvciB0LCBsIGluIFJYX0RPX0NITy5maW5kYWxsKG91dCl9CiAgICBibyA9IHt0IGZvciB0LCBfIGlu'
'IFJYX0JPX1FVQS5maW5kYWxsKG91dCl9CiAgICBjdW9pID0ge3Q6IGwuc3RyaXAoKSBmb3IgXywgdCwgbCBpbiBSWF9ET19D'
'VU9JLmZpbmRhbGwob3V0KSBpZiB0IG5vdCBpbiBib30KICAgIGhvcCA9IGRpY3QoY3VvaSk7IGhvcC51cGRhdGUodGFpX2No'
'bykKICAgIGdjLCB0aW4gPSBbXSwgVHJ1ZQogICAgaWYgc2V0KHRhaV9jaG8pICE9IHNldChjdW9pKToKICAgICAgICBnYy5h'
'cHBlbmQoZiJoYWkgbmd1b24gTEVDSDogY2hpLXRhaS1jaG89e3NvcnRlZChzZXQodGFpX2Nobyktc2V0KGN1b2kpKX0gY2hp'
'LWN1b2k9e3NvcnRlZChzZXQoY3VvaSktc2V0KHRhaV9jaG8pKX0iKQogICAgICAgIHRpbiA9IEZhbHNlCiAgICBtID0gUlhf'
'VE9ORy5zZWFyY2gob3V0KQogICAgaWYgbm90IG06CiAgICAgICAgZ2MuYXBwZW5kKCJLSE9ORyBkb2MgZHVvYyBkb25nIHRv'
'bmcga2V0Iik7IHRpbiA9IEZhbHNlCiAgICBlbHNlOgogICAgICAgIGRhdCwgdHJlbiA9IGludChtLmdyb3VwKDEpKSwgaW50'
'KG0uZ3JvdXAoMikpCiAgICAgICAgZ2MuYXBwZW5kKGYic28gaG9jOiB7dHJlbn0te2RhdH09e3RyZW4tZGF0fSBkbzsgZG9j'
'IGR1b2Mge2xlbihob3ApfSIpCiAgICAgICAgaWYgdHJlbiAtIGRhdCAhPSBsZW4oaG9wKToKICAgICAgICAgICAgZ2MuYXBw'
'ZW5kKGYiTEVDSCBTTyBIT0M6IHRoaWV1IHt0cmVuLWRhdC1sZW4oaG9wKX0gY2EiKTsgdGluID0gRmFsc2UKICAgIHJldHVy'
'biBob3AsIGdjLCB0aW4KCiMgTWF1IGNvIGRvbmcgdG9uZyBMT05HIGdpdWEgZG9uZyAoZGFuZyB0MTU1IGluIGxhaSBsdW90'
'IGNvbik6IGJvIGRvYyBiYXQgZG9uZyB0b25nIERBVSBUSUVOIGxhIHR1IGtpZW0gRE8uCl9NQVUgPSAoIiEhISBkbyB0MDJi'
'X3Rlbl9LSE9OR19DT19USEFNX1FVWUVOIGEgJ2xlYXNlX3B1Ymxpc2g6IDAvMSDEkeG6oXQ7IMSRw6MgY2jhuqF5PTEsIGLh'
'u48gcXVhPTAnXG4iCiAgICAgICAgIiEhISBkbyB0MTUwX3ggV2luRXJyb3IgMTMxNCByZXF1aXJlZCBwcml2aWxlZ2VcbiIK'
'ICAgICAgICAiICBC4buOIFFVQSB0MTMxX3k6IG5lbiBmaXh0dXJlXG4iCiAgICAgICAgIiAgxJDhu44gIHQwMmJfdGVuX0tI'
'T05HX0NPX1RIQU1fUVVZRU46IGFcbiIKICAgICAgICAiICDEkOG7jiAgdDE1MF94OiBXaW5FcnJvciAxMzE0IHJlcXVpcmVk'
'IHByaXZpbGVnZVxuIgogICAgICAgICJsZWFzZV9wdWJsaXNoOiAxLzMgxJHhuqF0OyDEkcOjIGNo4bqheT0zLCBi4buPIHF1'
'YT0xXG4iKQoKIyBCaWVuIFBZVEhPTiogY3VhIG1heSBuZ3VvaSBkbyBsb3QgdmFvIGJvIHRlc3QgbGEgRE9JIEhBTkggVkkg'
'Ym8gdGVzdDogUFlUSE9OT1BUSU1JWkUgYm8gbW9pIGBhc3NlcnRgIChkbyB0cmVuCiMgMjAyNi0wOS0zMGM6IGBhc3NlcnQg'
'RmFsc2VgIHF1YSwgcmM9MCk7IGJhbiAzMGQgY2hpIHRydW5nIGhvYSBNT1QgYmllbiBheSwgY29uIFBZVEhPTkRFVk1PREU9'
'MSBsYW0gdDE1NCBETyAyLzQKIyBsYW4gdHJlbiAzLjExIChzYWNoOiA0LzQgUVVBKSA9PiByYz0xICJUUlVPVCBNb2kgY2Eg'
'RE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIgY2hvIHVuZyB2aWVuIHNhY2ggKGRvIHRyZW4KIyAyMDI2LTA5LTMwZCkuIERhbmgg'
'c2FjaCBDQU0gbHVvbiB0aGlldSBtb3QgYmllbiDigJQgbmVuIGRheSBsYSBkYW5oIHNhY2ggQ0hPIFBIRVA6IGNoaSBnaXUg'
'YmllbiBkZSB0cmluaCB0aG9uZwojIGRpY2ggQ0hBWSB2YSB0aW0gZ29pIERBIENBSTsgUFlUSE9OUEFUSCBLSE9ORyBnaXUg'
'KENJIGtob25nIGNvIG5vKS4gUGhlcCBob2kgZGlldSBraWVuIHRpZW4gcXV5ZXQgbyBtdWMgMAojIGN1bmcgY2hheSBxdWEg'
'ZGF5LCBuZW4gbm8gdGhheSBEVU5HIG1vaSB0cnVvbmcgbWEgYm8gdGVzdCBzZSB0aGF5LgpfUFlfR0lVID0gZnJvemVuc2V0'
'KHsiUFlUSE9OSE9NRSIsICJQWVRIT05VU0VSQkFTRSIsICJQWVRIT05OT1VTRVJTSVRFIn0pCiMgQ2F1IGhpbmggZ2l0IENV'
'QSBOR1VPSSBETyBsb3QgdmFvIGJvIHRlc3QgeSBuaHUgYmllbiBQWVRIT04qOiBjYSB0ZXN0IGdvaSBnaXQgYmFuZyBkaWN0'
'KG9zLmVudmlyb24pLCBuZW4gZG9jIGNhdSBoaW5oCiMgY2EgbmhhbiB2YSBiaWVuIEdJVF8qIGN1YSBtYXkgZG8uIERvIHRy'
'ZW4gMjAyNi0wOS0zMGUsIDBlYTk1ZGU6IGBpbml0LmRlZmF1bHRCcmFuY2ggPSBtYWluYCA9PiAxNjMvMTY2LCB0MTM0IHQx'
'MzkgdDE1MQojIERPID0+IHJjPTEgIlRSVU9UIE1vaSBjYSBETyBkZXUgZ2lhaSB0aGljaCBkdW9jIiBjaG8gdW5nIHZpZW4g'
'c2FjaCAoc2FjaDogMTY2LzE2Nikg4oCUIG8gcGhhbSB2aSBnbG9iYWwgTEFOIGhlIHRob25nLgojIEJvIE1PSSBiaWVuIEdJ'
'VF8qIHZhIHRoYXkgZ2xvYmFsIENBIE5IQU4gYmFuZyBnbG9iYWwgQ1VBIENJLiBDSSBLSE9ORyBjbyBnbG9iYWwgcm9uZzog'
'am9iIGBnYXRlYCBjdWEgY2kueW1sIChidW9jICJGb3JjZSBMRgojIGNoZWNrb3V0IiwgY2EgdWJ1bnR1IGxhbiB3aW5kb3dz'
'KSBkYXQgZ2xvYmFsIGNvcmUuYXV0b2NybGY9ZmFsc2UsIGNvcmUuZW9sPWxmLCBjb3JlLmFiYnJldj03IFRSVU9DIGJ1b2Mg'
'Y2hheSBibyB0ZXN0IOKAlAojIHZpIChjaS55bWw6Ny04IHR1IGtoYWkpIGtob25nIHRhdCB0aGkgcnVubmVyIFdpbmRvd3Mg'
'Y2hlY2tvdXQgQ1JMRjogYXV0b2NybGY9dHJ1ZSBjdWEgYmFuIGNhaSBHaXQgbyBIRSBUSE9ORy4gQmFuIDMwZgojIGRhdCBn'
'bG9iYWwgPSByb25nIG5lbiBibyB0ZXN0IHRoYXkgYXV0b2NybGY9dHJ1ZSBjb24gQ0kgdGhheSBmYWxzZTogZG8gdHJlbiAy'
'MDI2LTA5LTMwZiwgMGVhOTVkZSwgaGUgdGhvbmcgYXV0b2NybGY9dHJ1ZQojICsgZ2xvYmFsIG5odSBDSSA9PiBiYW4gMzBl'
'IDE2Ni8xNjYsIGJhbiAzMGYgMTY1LzE2NiAodDE1MCBETyDigJQgY2hpIGtob25nIHRoYW5oIFRSVU9UIHZpIHQxNTAgdGlu'
'aCBjbyBuYW0gdHJvbmcKIyBOR09BSV9QSEFNX1ZJKS4gR2xvYmFsIGxhIFRFUCBUQU0gY2h1YSBEVU5HCiMgZ2xvYmFsIGN1'
'YSBDSSBjb25nIGluaXQuZGVmYXVsdEJyYW5jaCBnaGltIHZlIG1hYyBkaW5oIGN1YSBnaXQgKGRhdCBkdW9jIGNhIG8gaGUg'
'dGhvbmcpOiBnbG9iYWwgZGUgbGVuIGhlIHRob25nIG5odSB0cmVuIENJLAojIGNvbiBjYXUgaGluaCBDVUMgQk8gY3VhIGZp'
'eHR1cmUgdmFuIGRlIGxlbiBnbG9iYWwgKEdJVF9DT05GSUdfQ09VTlQgdGhpIGRlIGxlbiBjYSBjdWMgYm8pLiBEb2kgYnVv'
'YyBheSB0cm9uZyBjaS55bWwgdGhpCiMgZG9pIF9HSVRfR0xPQkFMX0NJLiBHSVRfQ09ORklHX0dMT0JBTCBjaGkgdGhheSBU'
'RVAgQ09ORklHOiBpZ25vcmUvYXR0cmlidXRlcyBtYWMgZGluaCAoJFhER19DT05GSUdfSE9NRSBob2FjIH4vLmNvbmZpZy9n'
'aXQvCiMgaWdub3JlfGF0dHJpYnV0ZXMpIGN1YSBuZ3VvaSBkbyBWQU4gYXAgY2hvIGdpdCBjb24gKGRvIHRyZW4gMjAyNi0w'
'OS0zMGcsIDBlYTk1ZGU6IH4vLmNvbmZpZy9naXQvaWdub3JlIGAqLnlhbWxgID0+IGJhbiAzMGcKIyAxNTQvMTY2LCAxMSBj'
'YSAibGEiKTsgQ0kga2hvbmcgY28gdGVwIG5hbyBvIGRvID0+IFhER19DT05GSUdfSE9NRSB0cm8gdmFvIHRodSBtdWMgVEFN'
'IFJPTkcuIENvbiBsYWkgKGtob2EgaGUgdGhvbmcga2hhYykKIyBsYSBnaW9pIGhhbiBkYSBiaWV0LCBraG9uZyBwaGFpIGRh'
'IGRvbmcuCiMgQ2F1IGhpbmggc2hlbGxjaGVjayBDVUEgTkdVT0kgRE8gbG90IHZhbyBibyB0ZXN0IHkgbmh1IGdpdDogdDEz'
'NyBnb2kgc2hlbGxjaGVjayBUSEFORywgdDMzL3QxMzcgZ29pIGFjdGlvbmxpbnQgLT4gc2hlbGxjaGVjaywKIyBjYSBoYWkg'
'ZG9jIFNIRUxMQ0hFQ0tfT1BUUywgdmEgdDEzNyBkb2Mgfi8uc2hlbGxjaGVja3JjIChYREdfQ09ORklHX0hPTUUgdGFtIEtI'
'T05HIGNoZSBkdW9jOyBjaG8gdGVwIHJjIHRyZW4gV2luZG93czogS0hPTkcgRE8gRFVPQykuCiMgRG8gdHJlbiAyMDI2LTA5'
'LTMwaCwgMGVhOTVkZTogU0hFTExDSEVDS19PUFRTPS0tZW5hYmxlPWFsbCA9PiB0MzMgKyB0MTM3IERPOyB+Ly5zaGVsbGNo'
'ZWNrcmMgYGVuYWJsZT1hbGxgID0+IHQxMzcgRE8g4oCUIGNhICJsYSIKIyA9PiBUUlVPVCBjaG8gdW5nIHZpZW4gc2FjaC4g'
'Q0kga2hvbmcgY28gY2EgaGFpLiBTSEVMTENIRUNLX09QVFM9LS1ub3JjIGRlIGxlbiBiaWVuIGN1YSBuZ3VvaSBkbyBWQSB0'
'YXQgbW9pIHRlcCByYyAoc2hlbGxjaGVjawojIHBoYWkgTkhBTiAtLW5vcmMg4oCUIG11YyAwIGhvaSB0cnVvYykuIEJBU0hf'
'RU5WIChrZSBjYSBgc2V0IC1ldW8gcGlwZWZhaWxgKSBkbzogMTY2LzE2Niwga2hvbmcgbG90LgpfR0lUX0dMT0JBTF9DSSA9'
'ICJbaW5pdF1cblx0ZGVmYXVsdEJyYW5jaCA9IG1hc3RlclxuW2NvcmVdXG5cdGF1dG9jcmxmID0gZmFsc2Vcblx0ZW9sID0g'
'bGZcblx0YWJicmV2ID0gN1xuIgpkZWYgY2hheShhcmd2LCBjd2QsIHBodXQ9NjApOgogICAgZmQsIGdjID0gdGVtcGZpbGUu'
'bWtzdGVtcChwcmVmaXg9IndwNTQxLWdpdGNvbmZpZy1jaS0iLCBzdWZmaXg9Ii5pbmkiKQogICAgeGRnID0gTm9uZQogICAg'
'dHJ5OgogICAgICAgIHhkZyA9IHRlbXBmaWxlLm1rZHRlbXAocHJlZml4PSJ3cDU0MS14ZGctIikKICAgICAgICB3aXRoIG9z'
'LmZkb3BlbihmZCwgInciLCBlbmNvZGluZz0iYXNjaWkiLCBuZXdsaW5lPSJcbiIpIGFzIGY6IGYud3JpdGUoX0dJVF9HTE9C'
'QUxfQ0kpCiAgICAgICAgbXQgPSB7azogdiBmb3IgaywgdiBpbiBvcy5lbnZpcm9uLml0ZW1zKCkKICAgICAgICAgICAgICBp'
'ZiBub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIkdJVF8iKSBhbmQgKG5vdCBrLnVwcGVyKCkuc3RhcnRzd2l0aCgiUFlUSE9O'
'Iikgb3Igay51cHBlcigpIGluIF9QWV9HSVUpfQogICAgICAgIG10LnVwZGF0ZShQWVRIT05VVEY4PSIxIiwgUFlUSE9OSU9F'
'TkNPRElORz0idXRmLTgiLCBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0iMSIsIFBZVEhPTlVOQlVGRkVSRUQ9IjEiLAogICAg'
'ICAgICAgICAgICAgICBHSVRfQ09ORklHX0dMT0JBTD1nYywgWERHX0NPTkZJR19IT01FPXhkZywgU0hFTExDSEVDS19PUFRT'
'PSItLW5vcmMiKQogICAgICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbc3lzLmV4ZWN1dGFibGVdICsgYXJndiwgY3dkPXN0cihj'
'd2QpLCBjYXB0dXJlX291dHB1dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICB0ZXh0PVRydWUsIGVuY29kaW5n'
'PSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCwgZW52PW10KQogICAgZmluYWxseToKICAgICAg'
'ICB0cnk6IG9zLnJlbW92ZShnYykKICAgICAgICBleGNlcHQgT1NFcnJvcjogcGFzcwogICAgICAgIGlmIHhkZzogc2h1dGls'
'LnJtdHJlZSh4ZGcsIGlnbm9yZV9lcnJvcnM9VHJ1ZSkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAi'
'IikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1X2NhKG91dCwgdCk6CiAgICBtID0gcmUuc2VhcmNoKHIiKD9tKV48PDwg'
'cmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSBbMC05Ll0rcyAoXHcrKVxzKiQiLCBvdXQpCiAgICByZXR1cm4gbS5ncm91cCgy'
'KSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdpdChnb2MsICphLCBwaHV0PTUpOgogICAgcCA9IHN1YnByb2Nlc3MucnVuKFsiZ2l0'
'IiwgIi1DIiwgc3RyKGdvYyksICphXSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLAogICAgICAgICAgICAgICAg'
'ICAgICAgIGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCkKICAgIHJldHVybiBw'
'LnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikuc3RyaXAoKSwgKHAuc3RkZXJyIG9yICIiKS5zdHJpcCgpCgoKIyA9PT09'
'PT09PT09PT09PT09PSBOQU0gUFJPQkUsIHZpZXQgdGhhbmggSEFNIFRIVUFOIGRlIFRVIEtJRU0gZHVvYyA9PT09PT09PT09'
'PT09PT09PQojIE1vaSBoYW0gdHJhICh0cmFuZ190aGFpLCBjaGlfdGlldCwgZHVfbGlldSkuIEtIT05HIGluLCBLSE9ORyB0'
'aG9hdCDigJQgbmhvIHZheSBjaHVuZwojIGNoYXkgZHVvYyB0cmVuIG5lbiBCQVQgS1ksIHZhIGAtLXR1LWtpZW0tcHJvYmVg'
'IGdvaSB0aGFuZyBjaHVuZyBkZSBraWVtIGNoaW5oIGJvIGRvLgoKZGVmIF9zYW4odCk6CiAgICBkID0gUGF0aCh0KS8iZCI7'
'IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIo'
'KQogICAgcmV0dXJuIGQsIGN3LCBwZgoKZGVmIGRvX244KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkJ1b2MgMSAoQ09OR19D'
'VV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0LmV4ZS4gRG9pIGNodW5nIGR1b25nOiBnaXQuZXhlIFZBTiBwaGFpIG5oYW4uIiIi'
'CiAgICBrcSA9IHt9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3cs'
'IHBmID0gX3Nhbih0KQogICAgICAgIGZvciB0ZW4gaW4gKCJnaXQuZXhlIiwgImdpdC5iYXQiLCAiZ2l0LmNtZCIsICJnaXQu'
'cHkiLCAia2hvbmctcGhhaS1naXQudHh0Iik6CiAgICAgICAgICAgIGYgPSBkL3RlbjsgZi53cml0ZV90ZXh0KCJ4IiwgZW5j'
'b2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgciwgXyA9IGdvaShjb25nX2N1X2dpdD1zdHIoZiksIHBhdGg9IiIsIHByb2dy'
'YW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIGtxW2YiQ09OR19DVV9HSVQ9e3Rlbn0iXSA9ICJO'
'SEFOIiBpZiByIGVsc2UgIlRVIENIT0kiCiAgICBsb3QgPSBbayBmb3IgaywgdiBpbiBrcS5pdGVtcygpIGlmIHYgPT0gIk5I'
'QU4iIGFuZCBub3Qgay5lbmRzd2l0aCgiZ2l0LmV4ZSIpXQogICAgaWYga3EuZ2V0KCJDT05HX0NVX0dJVD1naXQuZXhlIikg'
'IT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogZ2l0LmV4ZSBob3AgbGUgbWEg'
'YmkgdHUgY2hvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgbG90IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IGxvdCBl'
'bHNlIGYiY29uIG5oYW46IHtsb3R9IiksIGtxCgpkZWYgZG9fbjkoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiTXVjIFBBVEgg'
'Ym9jIG5oYXkga2VwIHBoYWkgTkhBTjsgbXVjIHJvbmcgLyB0b2FuIGtob2FuZyB0cmFuZyBwaGFpIGJvIHF1YSwga2hvbmcg'
'bmVtLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAg'
'IGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQ'
'YXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0i'
'dXRmLTgiKQogICAgICAgIGZvciBuaGFuLCBtdWMgaW4gKCgia2hvbmcgbmhheSIsIHN0cihkKSksICgiY28gbmhheSBrZXAi'
'LCBmJyJ7ZH0iJyksCiAgICAgICAgICAgICAgICAgICAgICAgICAgKCJyb25nIiwgIiIpLCAoImNoaSBraG9hbmcgdHJhbmci'
'LCAiICAgIikpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICByLCBfID0gZ29pKHBhdGg9bXVjLCBwcm9ncmFt'
'X2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gIk5IQU4i'
'IGlmIHIgZWxzZSAiTm9uZSIKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgICAga3Fb'
'ZiJQQVRIIHtuaGFufSJdID0gZiJORU0ge3R5cGUoZSkuX19uYW1lX199IgogICAgaWYga3EuZ2V0KCJQQVRIIGtob25nIG5o'
'YXkiKSAhPSAiTkhBTiI6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBtdWMgUEFUSCB0aHVv'
'bmcgbWEga2hvbmcgdGltIHJhIGdpdC5leGUiLCBrcQogICAgb2sgPSAoa3EuZ2V0KCJQQVRIIGNvIG5oYXkga2VwIikgPT0g'
'Ik5IQU4iCiAgICAgICAgICBhbmQga3EuZ2V0KCJQQVRIIHJvbmciKSA9PSAiTm9uZSIgYW5kIGtxLmdldCgiUEFUSCBjaGkg'
'a2hvYW5nIHRyYW5nIikgPT0gIk5vbmUiKQogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBpZiBvayBl'
'bHNlICJ4ZW0gYmFuZyIpLCBrcQoKIyBEYXUgcGhhbiBjYWNoIGR1bmcgREUgVEhVLiBQaGFpIEtIQUMgb3MucGF0aHNlcCB0'
'cmVuIENBIEhBSSBuZW4gKCc7JyBXaW5kb3dzLCAnOicgUE9TSVgpCiMgdGhpIGhhaSBnaWEgdGh1eWV0ICJ0YWNoIHRoZW8g'
'ZGF1IGR1b2MgdHJ1eWVuIiB2YSAidGFjaCB0aGVvIG9zLnBhdGhzZXAiIG1vaSByb2kgcmEgbmhhdS4KVEhVX04xMCA9ICJ8'
'IgoKZGVmIGRvX24xMChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW0gcGhhaSB0YWNoIFBBVEggdGhlbyBkYXUgcGhhbiBj'
'YWNoIERVT0MgVFJVWUVOLCBraG9uZyB0aGVvIG9zLnBhdGhzZXAgY3VhIG5lbi4KCiAgICBCYW4gY3UgZG8gIm1vdCBkYXUg'
'JzsnIHRyb25nIFRFTiB0aHUgbXVjIiB2YSBkYXQgREFUIHRyZW4gV2luZG93cyBkdSBoYW0gc2FpLiBObwogICAgZGVnZW5l'
'cmF0ZTogdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnLCBuZW4gJ0M6L2E7YicgdGhhdCBzdSBDTyBOR0hJQSBs'
'YSBoYWkKICAgIG11YyDigJQgInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gcmEgY3VuZyBrZXQgcXVhLCBwaGVwIGRv'
'IGtob25nIHRoZSBkbyBuYW8uIE5vCiAgICBkYSBjaGFtIERBVCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEgY3VhIGNo'
'aW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQgYXkuCiAgICBNb3QgY29uZyBraG9uZyB0aGUgZG8gdGhpIGto'
'b25nIHBoYWkgY29uZy4KICAgICIiIgogICAgdGVuX3NlcCA9IG5leHQoKGsgZm9yIGsgaW4gKCJwaGFuX2NhY2giLCAiZGF1'
'X3BoYW5fY2FjaCIsICJzZXAiKSBpZiBrIGluIHNpZy5wYXJhbWV0ZXJzKSwgTm9uZSkKICAgIGlmIHRlbl9zZXAgaXMgTm9u'
'ZToKICAgICAgICAjIEtob25nIGNvIHRoYW0gc28gdGhpIHRyZW4gV2luZG93cyBLSE9ORyBjb24gZHVvbmcgbmFvIHRhY2gg'
'aGFpIGdpYSB0aHV5ZXQuCiAgICAgICAgaWYgb3MucGF0aHNlcCA9PSAiOyI6CiAgICAgICAgICAgIHJldHVybiAoS0RELCAi'
'dHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEgbGEgJzsnIHZhIGhhbSBraG9uZyBuaGFuIHRoYW0gc28gZGF1IHBoYW4gY2Fj'
'aCAiCiAgICAgICAgICAgICAgICAgICAgICAgICAiLT4ga2hvbmcgdGFjaCBkdW9jIGhhaSBnaWEgdGh1eWV0IiwKICAgICAg'
'ICAgICAgICAgICAgICB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiBOb25lfSkKICAgICAgICB3'
'aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgICAgIGxhID0gUGF0aCh0KS8iY287ZGF1'
'IjsgbGEubWtkaXIoKQogICAgICAgICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgICAgIChkLyJnaXQuZXhlIiku'
'd3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8gID0gZ29pKHBhdGg9c3RyKGxhKSAr'
'IG9zLnBhdGhzZXAgKyBzdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIHIw'
'LCBfID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgIGtxID0g'
'eyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZSwKICAgICAgICAgICAgICAiY28gbXVjIGNo'
'dWEgJzsnIjogIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIsCiAgICAgICAgICAgICAgImRvaSBjaHVuZyBkdW9uZyAoa2hvbmcg'
'Y28gJzsnKSI6ICJOSEFOIiBpZiByMCBlbHNlICJOb25lIn0KICAgICAgICBpZiBub3QgcjA6CiAgICAgICAgICAgIHJldHVy'
'biBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZyIsIGtxCiAgICAgICAgcmV0dXJuIChEQVQgaWYgciBlbHNlIFRSVU9UKSwg'
'KCIiIGlmIHIgZWxzZSAibXVjIGdpdC5leGUgaG9wIGxlIGJpIE1BVCIpLCBrcQoKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9y'
'YXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkgICAgICAgICAg'
'IyAnOycgbmFtIHRyb25nIFRFTiwga2hvbmcgcGhhaSBkYXUgcGhhbiBjYWNoCiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0'
'KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgbm9pID0g'
'c3RyKGxhKSArIFRIVV9OMTAgKyBzdHIoZCkKICAgICAgICBrdyA9IGRpY3QocHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9'
'c3RyKGN3KSkKICAgICAgICByX2NoaW5oLCBfID0gZ29pKHBhdGg9bm9pLCAgICAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAg'
'ICoqa3cpICAgIyB0YWNoIGR1bmcgIC0+IE5IQU4KICAgICAgICByX2R1b25nLCBfID0gZ29pKHBhdGg9c3RyKGQpLCAgICoq'
'e3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyBkb2kgY2h1bmcgZHVvbmcKICAgICAgICByX3BoYW5iaWV0LCBfID0g'
'Z29pKHBhdGg9bm9pLCAgICoqe3Rlbl9zZXA6IG9zLnBhdGhzZXB9LCAqKmt3KSAgIyB0YWNoIHRoZW8gb3MucGF0aHNlcCAt'
'PiBtYXQKICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogdGVuX3NlcCwgImRhdSB0'
'aHUiOiBUSFVfTjEwLAogICAgICAgICAgZiJub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9Ijog'
'ICAgICAgIk5IQU4iIGlmIHJfY2hpbmggZWxzZSAiTm9uZSIsCiAgICAgICAgICBmImRvaSBjaHVuZyBkdW9uZyAobW90IG11'
'Yywge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9KSI6ICAiTkhBTiIgaWYgcl9kdW9uZyBlbHNlICJOb25lIiwKICAgICAgICAgIGYi'
'cGhhbiBiaWV0OiBub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtvcy5wYXRoc2VwIXJ9IjogIk5IQU4iIGlmIHJf'
'cGhhbmJpZXQgZWxzZSAiTm9uZSJ9CiAgICBpZiBub3Qgcl9kdW9uZzoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5n'
'IGR1b25nIGhvbmc6IG1vdCBtdWMgaG9wIGxlIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EKICAgICMgQ29uZyBwaGFp'
'IENPIFRIRSBkby4gTmV1IGNhIGhhaSBkYXUgcGhhbiBjYWNoIGRldSByYSBOSEFOIHRoaSBwaGVwIGRvIGtob25nIHBoYW4K'
'ICAgICMgYmlldCBkdW9jIGdpIOKAlCBkdW5nIGJhbyBEQVQsIGJhbyB0aGFuZyBsYSBraG9uZyBkbyBkdW9jLgogICAgaWYg'
'cl9waGFuYmlldDoKICAgICAgICByZXR1cm4gKEtERCwgZiJwaGVwIGRvIEtIT05HIHBoYW4gYmlldCBkdW9jOiBub2kgYmFu'
'ZyB7VEhVX04xMCFyfSBtYSB0YWNoIHRoZW8gIgogICAgICAgICAgICAgICAgICAgICBmIntvcy5wYXRoc2VwIXJ9IFZBTiB0'
'aW0gcmEgZ2l0LmV4ZSIsIGtxKQogICAgcmV0dXJuICgoREFULCAiIiwga3EpIGlmIHJfY2hpbmggZWxzZQogICAgICAgICAg'
'ICAoVFJVT1QsIGYidGFjaCB0aGVvIG9zLnBhdGhzZXAgdGhheSB2aSB0aGVvIHt0ZW5fc2VwfSBkdW9jIHRydXllbiIsIGtx'
'KSkKCgpkZWYgZG9fbjExKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIlRydXllbiBjaGFuX2RvYW4gPT4gdGh1IGR1b2MgdGhv'
'bmcgYmFvIFZBIHN0ZGVyciBJTS4gS2hvbmcgdHJ1eWVuID0+IHN0ZGVyciBWQU4gY28uIiIiCiAgICBpZiAiY2hhbl9kb2Fu'
'IiBub3QgaW4gc2lnLnBhcmFtZXRlcnM6CiAgICAgICAgcmV0dXJuIEtERCwgIl9naXRfd2luZG93cyBraG9uZyBuaGFuIHRo'
'YW0gc28gY2hhbl9kb2FuIiwgeyJ0aGFtIHNvIjogbGlzdChzaWcucGFyYW1ldGVycyl9CiAgICB3aXRoIHRlbXBmaWxlLlRl'
'bXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhl'
'Iikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgY2QgPSBbXQogICAgICAgIF8sIGVfY28gPSBn'
'b2kocGF0aD1zdHIoZCksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdyksIGNoYW5fZG9hbj1jZCkKICAgICAg'
'ICBfLCBlX2toID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAga3Eg'
'PSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAobXVjKSI6IGxlbihjZCksCiAgICAgICAgICAic3RkZXJyIGtoaSBDTyBjaGFuX2Rv'
'YW4gKGJ5dGUpIjogbGVuKGVfY28uZW5jb2RlKCkpLAogICAgICAgICAgInN0ZGVyciBraGkgS0hPTkcgdHJ1eWVuIChieXRl'
'KSI6IGxlbihlX2toLmVuY29kZSgpKX0KICAgIGlmIGxlbihjZCkgPT0gMCBhbmQgbGVuKGVfa2guZW5jb2RlKCkpID09IDA6'
'CiAgICAgICAgcmV0dXJuIEtERCwgIm5oYW5oICVQcm9ncmFtRmlsZXMlIGtob25nIHBoYW4gZ2lhaSBLSE9ORyBiYXkgcmEg'
'Y2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRvIGR1b2MiLCBrcQogICAgb2sgPSBsZW4oY2QpID4gMCBhbmQgbGVuKGVfY28uZW5j'
'b2RlKCkpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA+IDAKICAgIHJldHVybiAoREFUIGlmIG9rIGVsc2UgVFJVT1Qp'
'LCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCmRlZiBkb19uMTIoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiSGFu'
'ZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9uZyBmaXh0dXJlIHBoYWkgdHV5ZXQgZG9pIHRyZW4gQ0EgSEFJIG5lbi4iIiIKICAg'
'IG5kID0gdGVwdC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIikKICAgIGhhbmcgPSBzb3J0'
'ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRfcGF0aFxzKj1ccyoiKFteIl0rKSInLCBuZCkpKQogICAgeGF1ID0gW2ggZm9yIGgg'
'aW4gaGFuZyBpZiBub3QgKFB1cmVQb3NpeFBhdGgoaCkuaXNfYWJzb2x1dGUoKSBhbmQgUHVyZVdpbmRvd3NQYXRoKGgpLmlz'
'X2Fic29sdXRlKCkpXQogICAga3EgPSB7ImhhbmcgZ2l0X3BhdGggdGltIHRoYXkiOiBoYW5nLCAiY2hpIHR1eWV0IGRvaSBN'
'T1QgbmVuIjogeGF1fQogICAgaWYgbm90IGhhbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImtob25nIHRpbSB0aGF5IGhhbmcg'
'Z2l0X3BhdGggbmFvIHRyb25nIGZpeHR1cmUgLT4gbWF1IGRvYyBjbyB0aGUgZGEgZG9pIiwga3EKICAgIHJldHVybiAoREFU'
'IGlmIG5vdCB4YXUgZWxzZSBUUlVPVCksICgiIiBpZiBub3QgeGF1IGVsc2UgZiJjaGktbW90LW5lbjoge3hhdX0iKSwga3EK'
'ClBST0JFID0gWygiTjggYnVvYyAxIGNoaSBuaGFuIGdpdC5leGUiLCBkb19uOCksCiAgICAgICAgICgiTjkgYm9jIG5oYXkg'
'a2VwIG8gbXVjIFBBVEgiLCBkb19uOSksCiAgICAgICAgICgiTjEwIGRhdSAnOycgdHJvbmcgdGVuIHRodSBtdWMiLCBkb19u'
'MTApLAogICAgICAgICAoIk4xMSBjaGFuIGRvYW4gZG9pIGtlbmgiLCBkb19uMTEpLAogICAgICAgICAoIk4xMiBoYW5nIHNl'
'bnRpbmVsIHR1eWV0IGRvaSBDQSBIQUkgbmVuIiwgZG9fbjEyKV0KCiMgLS0tIGNoZSBkbyBUVSBLSUVNOiBjaGF5IG5hbSBw'
'cm9iZSB0cmVuIG1vdCBjYXkgYmF0IGt5LCBuZW4gYmF0IGt5IC0tLQppZiAiLS10dS1raWVtLXByb2JlIiBpbiBzeXMuYXJn'
'djoKICAgIF9nID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS10dS1raWVtLXByb2JlIikgKyAxXSkucmVzb2x2'
'ZSgpCiAgICBfc3AgPSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfdGsiLCBzdHIoX2cvIm9w'
'cyIvImxlYXNlX3B1Ymxpc2gucHkiKSkKICAgIF9scCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsg'
'X3NwLmxvYWRlci5leGVjX21vZHVsZShfbHApCiAgICBfc2lnID0gaW5zcGVjdC5zaWduYXR1cmUoX2xwLl9naXRfd2luZG93'
'cykKICAgIGRlZiBfZ29pKCoqa3cpOgogICAgICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICAgICAgd2l0aCBjb250ZXh0bGli'
'LnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICAgICAgcmV0dXJuIF9scC5fZ2l0X3dpbmRvd3MoKiprdyksIGUuZ2V0dmFs'
'dWUoKQogICAgcHJpbnQoZiJUVSBLSUVNIFBST0JFIHRyZW4ge19nfSAgKG5lbiB7c3lzLnBsYXRmb3JtfSkiKQogICAgZm9y'
'IF90ZW4sIF9mIGluIFBST0JFOgogICAgICAgIF90dCwgX2N0LCBfZGwgPSBfZihfZ29pLCBfc2lnLCBfZy8ib3BzIi8ibGVh'
'c2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBwcmludChmIiAgW3tfdHQ6MTR9XSB7X3Rlbn0iICsgKGYiICAge19jdH0i'
'IGlmIF9jdCBlbHNlICIiKSkKICAgICAgICBmb3IgX2ssIF92IGluIChfZGwgb3Ige30pLml0ZW1zKCk6IHByaW50KGYiICAg'
'ICAgICB7X2s6MzR9OiB7X3Z9IikKICAgIHN5cy5leGl0KDApCgojIC0tLSBjaGUgZG8gS0lFTSBET05HIEJPOiB0ZXAgLnB5'
'IG5heSBwaGFpIFRSVU5HIFRVTkcgQllURSB2b2kgYmFuIG5odW5nIHRyb25nIHBzMSAtLS0KIyBLaG9uZyBjb25nIG5hbyBi'
'dW9jIGhhaSBiYW4gc2FvIGtob3A6IGRvIGR1b2MsIG5vaSB0cmFuIDIvNDAwIC0+IDk5Lzk5OTk5IENISSB0cm9uZyAucHkK'
'IyB0aGkgY2lfZGFuZ19reSBsYW4gdDI2L3QyNyB2YW4geGFuaCwgY29uIGNob3QgU0hBIGN1YSBwczEgY2hpIHNvIGJhbiBu'
'aHVuZyB2b2kgaGFuZyBzbwojIGN1YSBDSElOSCBuby4gQ2hheTogcHl0aG9uIHdwNTQxLWRvLWcyLXdpbmRvd3MucHkgLS1r'
'aWVtLWRvbmctYm8gd3A1NDEtZG8tZzIucHMxICAocmMgMHwzKQppZiAiLS1raWVtLWRvbmctYm8iIGluIHN5cy5hcmd2Ogog'
'ICAgaW1wb3J0IGJhc2U2NAogICAgX3BzID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS1raWVtLWRvbmctYm8i'
'KSArIDFdKS5yZWFkX3RleHQoZW5jb2Rpbmc9ImFzY2lpIikKICAgIF9tID0gcmUuc2VhcmNoKHIiKD9tcyleXCRCNjQgPSBA'
'XCgoLio/KV5cKSIsIF9wcykKICAgIF9rID0gcmUuc2VhcmNoKHIiKD9tKV5cJFNoYUJvRG9ccyo9XHMqJyhbMC05YS1mXXs2'
'NH0pJyIsIF9wcykKICAgIF9uaHVuZyA9IGJhc2U2NC5iNjRkZWNvZGUoIiIuam9pbihyZS5maW5kYWxsKHIiJyhbQS1aYS16'
'MC05Ky89XSopJyIsIF9tLmdyb3VwKDEpKSkpIGlmIF9tIGVsc2UgYiIiCiAgICBfdG9pID0gUGF0aChfX2ZpbGVfXykucmVh'
'ZF9ieXRlcygpCiAgICBfb2sgPSBib29sKF9tIGFuZCBfaykgYW5kIF9uaHVuZyA9PSBfdG9pIGFuZCBoYXNobGliLnNoYTI1'
'NihfdG9pKS5oZXhkaWdlc3QoKSA9PSBfay5ncm91cCgxKQogICAgaW5uKGYiS0lFTSBET05HIEJPOiB7REFUIGlmIF9vayBl'
'bHNlIEtERH0gIChuaHVuZyB7bGVuKF9uaHVuZyl9IGJ5dGUsIHRlcCB7bGVuKF90b2kpfSBieXRlKSIpCiAgICBzeXMuZXhp'
'dCgwIGlmIF9vayBlbHNlIDMpCgppbm4oIj0iICogNzgpOyBpbm4oIldQNTQxIGcyIC0gcGhlcCBkbyB0cmVuIFdpbmRvd3Mg'
'dGhhdCAoc3BlYyByMzogTjEtTjQsIE44LU4xMiwgTjcsIGtpY2ggdGh1b2MpIik7IGlubigiPSIgKiA3OCkKCiMgLS0tLS0t'
'LS0tLS0tLS0tLSB0dSBraWVtIGJvIGRvYyAtLS0tLS0tLS0tLS0tLS0tCl9kLCBfZywgX3QgPSBkb2NfZG8oX01BVSkKX29r'
'ID0gKGxlbihfZCkgPT0gMiBhbmQgYW55KHguc3RhcnRzd2l0aCgidDAyYiIpIGZvciB4IGluIF9kKQogICAgICAgYW5kIG5v'
'dCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMxIikgZm9yIHggaW4gX2QpIGFuZCBfdCkKaW5uKCJUdSBraWVtIGJvIGRvYyBsb2c6'
'IiwgREFUIGlmIF9vayBlbHNlIFRSVU9UKQppZiBub3QgX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBi'
'byBkb2MgbG9nIGN1YSBjaGluaCBzY3JpcHQgbmF5IHNhaSAtPiBraG9uZyBkbyBnaSBjYS4iKTsgc3lzLmV4aXQoMykKCiMg'
'LS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4gZG8gLS0tLS0tLS0tLS0tLS0tLQpnb2MgPSBQYXRoKHN5cy5hcmd2WzFdKS5yZXNv'
'bHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQYXRoLmN3ZCgpCnRlcCwgdGVwdCA9IGdvYyAvICJvcHMiIC8gImxl'
'YXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiCmlubigiIik7IGlubigiLSIg'
'KiA3OCk7IGlubigiMC4gTkVOIERPIikKIyBNT0kgTE9HIFBIQUkgVFUgS0hBSSBubyBkbyBDQUkgR0kgYmFuZyBCTyBETyBO'
'QU8uIEJhaSBob2MgMTktMDktMjAyNjogbW90IGx1b3QgZG8KIyBndWkgdmUgZHVvYyBkb2Mgbmh1IGtldCBxdWEgY3VhIGJh'
'biB2YSBkYW5nIHhldCwgbmh1bmcgdGhhdCByYSBsYSBiYW4gZG8gQ1UgY2hheQojIHRyZW4gbmhhbmggS0hBQy4gRG9jIHJh'
'IHRoaSBtYXQgbW90IHZvbmc7IGxvZyB0dSBraGFpIHRoaSB0aGF5IG5nYXkgZG9uZyBkYXUuCnRyeToKICAgIF90dSA9IGhh'
'c2hsaWIuc2hhMjU2KFBhdGgoX19maWxlX18pLnJlYWRfYnl0ZXMoKSkuaGV4ZGlnZXN0KCkKZXhjZXB0IEV4Y2VwdGlvbiBh'
'cyBfZToKICAgIF90dSA9IGYia2hvbmcgdHUgYmFtIGR1b2M6IHtfZX0iCmdoaSgiYm9fZG9fc2hhMjU2IiwgX3R1KQppbm4o'
'ZiIgIEJPIERPICAgICAgICA6IHNoYTI1NiB7X3R1WzoxNl19ICAoYmFuIHtCQU5fQk9fRE99KSIpCmlubigiICBzeXMucGxh'
'dGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwgInwgcHl0aG9uIiwgc3lzLnZlcnNpb24uc3BsaXQoKVswXSkKaW5uKCIgIG9zLnBh'
'dGhzZXAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSwgInwgUEFUSEVYVDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQQVRIRVhU'
'IikpWzo2MF0pCmlubigiICBQcm9ncmFtRmlsZXMgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlByb2dyYW1GaWxlcyIpKSwg'
'InwgU3lzdGVtUm9vdDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290IikpKQppbm4oIiAgQ09OR19DVV9HSVQg'
'IDoiLCByZXByKF9DT05HX0NVX0dJVF9OR1VPSV9ETykKICAgICsgKCIgIC0+IERBIEJPIGtob2kgbHVvdCBkbyAoQ0kga2hv'
'bmcgZGF0IGJpZW4gbmF5OyB4ZW0gZGF1IHRlcCkiIGlmIF9DT05HX0NVX0dJVF9OR1VPSV9ETyBpcyBub3QgTm9uZSBlbHNl'
'ICIiKSkKZ2hpKCJjb25nX2N1X2dpdF9uZ3VvaV9kbyIsIF9DT05HX0NVX0dJVF9OR1VPSV9ETykKaW5uKCIgIGdvYyBraG8g'
'ICAgICA6IiwgZ29jKQoKcXV5ZW4gPSBOb25lCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAg'
'IGltcG9ydCBjdHlwZXM7IHF1eWVuID0gYm9vbChjdHlwZXMud2luZGxsLnNoZWxsMzIuSXNVc2VyQW5BZG1pbigpKQogICAg'
'ZXhjZXB0IEV4Y2VwdGlvbjogcXV5ZW4gPSBOb25lCmdoaSgicXV5ZW5fYWRtaW4iLCBxdXllbikKc3ltbGlua19kdW9jID0g'
'Tm9uZQp0cnk6CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgo'
'dCkvImEudHh0IjsgZC53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICB0cnk6IG9zLnN5bWxpbmso'
'c3RyKGQpLCBzdHIoUGF0aCh0KS8ibGsiKSk7IHN5bWxpbmtfZHVvYyA9IFRydWUKICAgICAgICBleGNlcHQgT1NFcnJvciBh'
'cyBlOiBzeW1saW5rX2R1b2MgPSBGYWxzZTsgZ2hpKCJzeW1saW5rX2xvaSIsIGYie3R5cGUoZSkuX19uYW1lX199OiB7ZX0i'
'KQpleGNlcHQgRXhjZXB0aW9uIGFzIGU6IGdoaSgic3ltbGlua19sb2kiLCBzdHIoZSkpCmdoaSgic3ltbGlua19kdW9jIiwg'
'c3ltbGlua19kdW9jKQppbm4oIiAgQWRtaW5pc3RyYXRvcjoiLCBxdXllbiwgInwgdGFvIHN5bWxpbmsgZHVvYzoiLCBzeW1s'
'aW5rX2R1b2MpCgpsb2kgPSBbXQojIENvbmcga2ljaCB0aHVvYyBsYSBwaGVwIGRvIHRyZW4gTElDSCBTVSBHSVQsIGtob25n'
'IGRpbmggZ2kgZGVuIG5lbi4gQ2hvIHBoZXAKIyAtLWNoaS1raWNoLXRodW9jIGNoYXkgbyBtb2kgbmVuIGRlIGNvbiBUVSBL'
'SUVNIGR1b2MgY2hpbmggY29uZyBuYXkgKGRhIGR1bmcKIyBkZSB0YWkgZHVuZyBjYSBoYWkgdmUgY3VhIHN1IGNvIG5lbi1j'
'dSAxOS0wOSkuIE1vaSBjaG90IENIVUMgTkFORyB2YW4gZG9pIFdpbmRvd3MuCmlmIHN5cy5wbGF0Zm9ybSAhPSAid2luMzIi'
'IGFuZCAiLS1jaGkta2ljaC10aHVvYyIgbm90IGluIHN5cy5hcmd2OgogICAgbG9pLmFwcGVuZChmIktIT05HIHBoYWkgV2lu'
'ZG93cyAoc3lzLnBsYXRmb3JtPXtzeXMucGxhdGZvcm0hcn0pIikKaWYgbm90IHRlcC5pc19maWxlKCk6ICBsb2kuYXBwZW5k'
'KGYia2hvbmcgdGhheSB7dGVwfSIpCmlmIG5vdCB0ZXB0LmlzX2ZpbGUoKTogbG9pLmFwcGVuZChmImtob25nIHRoYXkge3Rl'
'cHR9IikKaWYgbm90IHNodXRpbC53aGljaCgiZ2l0Iik6IGxvaS5hcHBlbmQoImtob25nIGNvIGBnaXRgIHRyb25nIFBBVEgi'
'KQojIEJvIHRlc3QgKG11YyAyIHZhIE43KSBjYW4gUHlZQU1MOiB0aGlldSBubywgMGVhOTVkZSByYSA5Ni8xNjYgY2EgRE8g'
'KDg5IGJhbyB0aGFuZyAiTm8gbW9kdWxlIG5hbWVkICd5YW1sJyIsCiMgNyBxdWEgbHVvdCBjb247IGNvIFB5WUFNTDogMTY2'
'LzE2NiBRVUEpLiBCbyBkbyBnb2kgY2h1bmcgbGEgImNhIERPIExBIiByb2kgcGhhdCBUUlVPVCDigJQgZG8gdHJlbiAyMDI2'
'LTA5LTMwYy4KIyBEaWV1IGtpZW4gdGllbiBxdXlldCBwaGFpIGhvaSBiYW5nIENISU5IIHRpZW4gdHJpbmggY29uIHNlIGNo'
'YXkgYm8gdGVzdCAoY2hheSgpOiBjdW5nIG1vaSB0cnVvbmc7IGN3ZCA9IG9wcy8gPQojIHN5cy5wYXRoWzBdIGN1YSBibyB0'
'ZXN0KSB2YSBob2kgRFVORyBEVU9DIGNodSBraG9uZyBob2kgQ08gTUFULiBCYW4gMzBkIGhvaSBgZmluZF9zcGVjKCJ5YW1s'
'IilgIG8gdGllbiB0cmluaAojIE5BWSB2YSBuZ3VvbmcgMy44IHN1eSB0dSBOR1UgUEhBUCAoYDo9YCkg4oCUIGRvIHRyZW4g'
'MjAyNi0wOS0zMGQsIGNhIGhhaSByYSByYz0xIFRSVU9UIGNobyB1bmcgdmllbiBzYWNoOgojIHRodSBtdWMgZHUgbGlldSBg'
'eWFtbC9gIHRyZW4gUFlUSE9OUEFUSCBxdWEgZmluZF9zcGVjIG1hIGB5YW1sLnNhZmVfZHVtcGAga2hvbmcgY28gKDg3IGNh'
'ICJsYSIpOyBweXRob24gMy44LjIwCiMgVEhBVCBjbyBQeVlBTUwsIGJvIHRlc3QgZHVuZyBgc3RyLnJlbW92ZXByZWZpeGAg'
'KDMuOSkgbHVjIENIQVkgKDMzIGNhICJsYSI7IDMuOS4yMzogMTY2LzE2NikuCiMgIkR1bmcgZHVvYyIgbmdoaWEgbGEgZHVu'
'ZyBEVU5HIEFQSSBibyB0ZXN0IGdvaTogdmlldCgpICg0MyBsb2kgZ29pKSB2YSBsZWFzZV9wdWJsaXNoLnB5IGdvaSBzYWZl'
'X2R1bXAoLi4uLCBhbGxvd191bmljb2RlPVRydWUsCiMgc29ydF9rZXlzPUZhbHNlKSwgbWEgYHNvcnRfa2V5c2AgY2hpIGNv'
'IHR1IFB5WUFNTCA1LjEuIERvIHRyZW4gMjAyNi0wOS0zMGwsIDBlYTk1ZGU6IHB5dGhvbiAzLjkuMjMgKyBQeVlBTUwgMy4x'
'MyBUSEFUIHF1YSBwcm9iZQojIGN1IChyYz0wKSwgYm8gdGVzdCAxMDkvMTY2IOKAlCA1NiBjYSAibGEiOiA1MiBgdW5leHBl'
'Y3RlZCBrZXl3b3JkIGFyZ3VtZW50ICdzb3J0X2tleXMnYCwgdDI2L3QyNyBgUmVhZGVyRXJyb3JgIChreSB0dSBuZ29haSBC'
'TVApLAojIHQxMjQvdDE1MyBETyB0aGVvIGx1b3QgY29uIOKAlCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWA7IFB5WUFN'
'TCA1LjE6IDE2Ni8xNjYgKGRvIGxhaSAyMDI2LTEwLTAxOiBjdW5nIHNvKS4KIyAoUHl0aG9uID49IDMuMTAgKyBQeVlBTUwg'
'My4xMyBkYSB0cnVvdCBwcm9iZSBjdSB2aSBgY29sbGVjdGlvbnMuSGFzaGFibGVgLikgUHJvYmUgY3VhIHBzMSAoJG1hVGh1'
'KSBwaGFpIEdJT05HIEhFVCBkb25nIGR1b2kuCmlmIG5vdCAoIi0tY2hpLWtpY2gtdGh1b2MiIGluIHN5cy5hcmd2IG9yICIt'
'LWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YpOgogICAgX3JjX2RrLCBfcmFfZGsgPSBjaGF5KFsiLWMiLCAiaW1wb3J0IHN5czsg'
'c3lzLmV4aXQoOSkgaWYgc3lzLnZlcnNpb25faW5mbyA8ICgzLCA5KSBlbHNlIE5vbmU7IGltcG9ydCB5YW1sOyIKICAgICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgIiB5YW1sLnNhZmVfZHVtcCh5YW1sLnNhZmVfbG9hZCgnYTogMScpLCBhbGxv'
'd191bmljb2RlPVRydWUsIHNvcnRfa2V5cz1GYWxzZSkiXSwKICAgICAgICAgICAgICAgICAgICAgICAgICBnb2MgLyAib3Bz'
'IiBpZiAoZ29jIC8gIm9wcyIpLmlzX2RpcigpIGVsc2UgUGF0aC5jd2QoKSwgcGh1dD0yKQogICAgaWYgX3JjX2RrID09IDk6'
'CiAgICAgICAgbG9pLmFwcGVuZChmInB5dGhvbiB7c3lzLnZlcnNpb24uc3BsaXQoKVswXX0gPCAzLjk6IGJvIHRlc3QgY3Vh'
'IHVuZyB2aWVuIGR1bmcgc3RyLnJlbW92ZXByZWZpeCAoMy45KSBsdWMgQ0hBWSIpCiAgICBlbGlmIF9yY19kazoKICAgICAg'
'ICBsb2kuYXBwZW5kKGYicHl0aG9uIG5heSBLSE9ORyBjbyBQeVlBTUwgZHVuZyBkdW9jICh7KF9yYV9kay5zdHJpcCgpLnNw'
'bGl0bGluZXMoKSBvciBbJyddKVstMV1bOjkwXX0pOiIKICAgICAgICAgICAgICAgICAgIGYiIFwie3N5cy5leGVjdXRhYmxl'
'fVwiIC1tIHBpcCBpbnN0YWxsIC1VIHB5eWFtbCIKICAgICAgICAgICAgICAgICAgICIgKGJhbiBuaHVuZyBwczEgdHUgdGFp'
'IEtIT05HIGNvIHBpcDogY2hheSBsYWkgdm9pIC1QeSA8cHl0aG9uIGRhIGNvIFB5WUFNTD4pIikKICAgICMgQm8gdGVzdCBj'
'b24gZ29pIGBzaHV0aWwud2hpY2hgIGNobyBiYXNoL2FjdGlvbmxpbnQvc2hlbGxjaGVjayAoMGVhOTVkZTogdDMzIHQxMzcg'
'dDE1OSBjYW4gYWN0aW9ubGludCwgdDEzNyBjYW4KICAgICMgc2hlbGxjaGVjaywgY2FjIGNhIGNoYXkgb3BzL2NhaV9hY3Rp'
'b25saW50LnNoIGNhbiBiYXNoKS4gVGhpZXUgdGhpIGNhYyBjYSBheSBpbiAiS0hPTkcgRE8gRFVPQzogdGhpZXUgYC4uLmAi'
'IHZhIGJvIGRvIHJhCiAgICAjIHJjPTMg4oCUIG5odW5nIGNoaSBTQVUgY2EgYm8gdGVzdCBsYW4gTjcgKGRvIHRyZW4gMjAy'
'Ni0wOS0zMGcsIFBBVEggdGhpZXUgYWN0aW9ubGludDogYENvbmcgY3UgZGF5IGR1IGRlIGRvYCBLREQsIHJjPTMKICAgICMg'
'c2F1IDIgbHVvdCBibyB0ZXN0KS4gQ3VuZyBseSBkbyBQeVlBTUwgZHVvYyBob2kgbyBkYXk6IGhvaSBUUlVPQywgY3VuZyBQ'
'QVRIIG1hIGNoYXkoKSB0cnV5ZW4gY2hvIGJvIHRlc3QuCiAgICAjIFZBIGN1bmcgQ0hPIGJvIHRlc3QgZHVuZzogdHJlbiBX'
'aW5kb3dzIGBzaHV0aWwud2hpY2hgIHRyYSBUSFUgTVVDIEhJRU4gSEFOSCBUUlVPQyBQQVRILCBtYSBibyB0ZXN0IGNoYXkg'
'dm9pIGN3ZCA9IGdvYyBjb24KICAgICMgdGllbiB0cmluaCBuYXkgZHVuZyBvIGN3ZCBDVUEgTkdVT0kgRE8gKG5vaSBnb2kg'
'cHMxLCB2ZC4gRG93bmxvYWRzIOKAlCBkdW5nIG5vaSBnaWFpIG5lbiBhY3Rpb25saW50LmV4ZSkuIERvIHRyZW4gMjAyNi0w'
'OS0zMGsKICAgICMgKG5oYW5oIHdpbjMyIFRIQVQgY3VhIHNodXRpbC53aGljaCk6IGFjdGlvbmxpbnQgdG90IG8gY3dkIG5n'
'dW9pIGRvICsgYmFuIGhvbmcgZGF1IFBBVEggPT4gbXVjIDAgaG9pIGJhbiBvIGN3ZCAocmM9MCksIGJvIHRlc3QKICAgICMg'
'ZHVuZyBiYW4gdHJlbiBQQVRIID0+IHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgLCBgbGE6IFsndDMzJywgJ3QxMzcnLCAndDE1'
'OSddYC4gR2lhaSB0ZW4gdm9pIGN3ZCA9IGdvYyByb2kgZ29pIFRIQU5HIGJhbmcgZHVvbmcKICAgICMgVFVZRVQgRE9JIGRh'
'IGdpYWkgKHF1YSBoYW4gdGhpIHJ1bigpIGdpZXQgZHVuZyB0aWVuIHRyaW5oIOKAlCBseSBkbyBiYW4gMzBpIGtob25nIGhv'
'aSBxdWEgY2hheSgpKS4KICAgIF9jd2Rfbmd1b2lfZG8gPSBvcy5nZXRjd2QoKQogICAgdHJ5OgogICAgICAgIGlmIGdvYy5p'
'c19kaXIoKTogb3MuY2hkaXIoZ29jKQogICAgICAgIF9jYyA9IHtjOiAob3MucGF0aC5hYnNwYXRoKHApIGlmIHAgZWxzZSBO'
'b25lKSBmb3IgYywgcCBpbgogICAgICAgICAgICAgICAoKGMsIHNodXRpbC53aGljaChjKSkgZm9yIGMgaW4gKCJiYXNoIiwg'
'ImFjdGlvbmxpbnQiLCAic2hlbGxjaGVjayIpKX0KICAgIGZpbmFsbHk6CiAgICAgICAgb3MuY2hkaXIoX2N3ZF9uZ3VvaV9k'
'bykKICAgIF90aGlldV9jYyA9IFtjIGZvciBjLCBwIGluIF9jYy5pdGVtcygpIGlmIG5vdCBwXQogICAgaWYgX3RoaWV1X2Nj'
'OgogICAgICAgIGxvaS5hcHBlbmQoZiJ0aGlldSBjb25nIGN1IGJvIHRlc3QgZ29pIHF1YSBQQVRIOiB7X3RoaWV1X2NjfSAo'
'YWN0aW9ubGludDogb3BzL2NhaV9hY3Rpb25saW50LnNoIHZvaSBBTF9WRVI7IgogICAgICAgICAgICAgICAgICAgIiBiYXNo'
'OiBHaXQgQmFzaCwga2hvbmcgcGhhaSBiYXNoLmV4ZSBjdWEgV1NMKSIpCiAgICAjIHNoZWxsY2hlY2sgS0hPTkcgbmhhbiAt'
'LW5vcmMgdGhpIGFjdGlvbmxpbnQgMS43LjcgKHR1IHRydXllbiAtLW5vcmMpIGxhbSB0MzMgRE8sIHZhIFNIRUxMQ0hFQ0tf'
'T1BUUz0tLW5vcmMgY3VhIGNoYXkoKSBsYW0KICAgICMgdDEzNyBETyDigJQgY2EgImxhIiA9PiBUUlVPVCBnaWEgKGRvIHRy'
'ZW4gMjAyNi0wOS0zMGgsIHNoZWxsY2hlY2sgZ2lhIHR1IGNob2kgLS1ub3JjOiBiYW4gMzBoIHJjPTEgYGxhOiBbJ3QzMydd'
'YCBzYXUgY2EKICAgICMgYm8gdGVzdCkuIGB3aGljaGAgY2hpIGhvaSBDTyBNQVQ7IG8gZGF5IGhvaSBEVU5HIERVT0MuIE5n'
'dW9uZyBkbyB0cmVuIHNoZWxsY2hlY2sgVEhBVDogMC40LjcvMC41LjAvMC42LjAgdHUgY2hvaSAtLW5vcmMKICAgICMgKHJj'
'PTMpLCAwLjcuMCB0cm8gbGVuIG5oYW4uIFBoZXAgaG9pIHBoYWkgdGhheSBEVU5HIFNIRUxMQ0hFQ0tfT1BUUyBtYSBjaGF5'
'KCkgZGF0IGNobyBsdW90IGNvbjogYmFuIDMwaSBob2kgdm9pIGJpZW4gQ1VBCiAgICAjIE5HVU9JIERPIOKAlCBkbyB0cmVu'
'IDIwMjYtMDktMzBpLCBzaGVsbGNoZWNrIDAuOS4wICsgU0hFTExDSEVDS19PUFRTPS0tZXh0ZW5kZWQtYW5hbHlzaXM9dHJ1'
'ZSAoY28gY3VhIDAuMTApOiByYz0zICJraG9uZyBuaGFuCiAgICAjIC0tbm9yYzogY2FwIG5oYXQgc2hlbGxjaGVjayIgdHJv'
'bmcga2hpIHQzMy90MTM3IHF1YSBjaGF5KCkgZGV1IDEvMS4gR29pIFRIQU5HIChraG9uZyBxdWEgY2hheSgpKTogcXVhIGhh'
'biB0aGkgcnVuKCkgZ2lldAogICAgIyBkdW5nIHNoZWxsY2hlY2s7IHF1YSBjaGF5KCkgdGhpIGNoaSBnaWV0IHB5dGhvbiBj'
'b24sIHNoZWxsY2hlY2sgdHJlbyBvIGxhaSBtbyBjb2kgKGRvIHRyZW4gMjAyNi0wOS0zMGk6IDEvMSBjb24gc29uZykuCiAg'
'ICBlbGlmIHN1YnByb2Nlc3MucnVuKFtfY2NbInNoZWxsY2hlY2siXSwgIi0tbm9yYyIsICItLXZlcnNpb24iXSwgY2FwdHVy'
'ZV9vdXRwdXQ9VHJ1ZSwgdGltZW91dD02MCwKICAgICAgICAgICAgICAgICAgICAgICAgZW52PWRpY3Qob3MuZW52aXJvbiwg'
'U0hFTExDSEVDS19PUFRTPSItLW5vcmMiKSkucmV0dXJuY29kZToKICAgICAgICBsb2kuYXBwZW5kKCJzaGVsbGNoZWNrIHRy'
'ZW4gUEFUSCBraG9uZyBuaGFuIC0tbm9yYyAoYWN0aW9ubGludCAxLjcuNyB2YSBjaGF5KCkgZGV1IHRydXllbiBjbyBheSk6'
'IGNhcCBuaGF0IHNoZWxsY2hlY2siKQogICAgIyBhY3Rpb25saW50IGN1bmcgcGhhaSBEVU5HIERVT0MsIGtob25nIGNoaSBD'
'TyBNQVQ6IHQzMy90MTM3L3QxNTkgZ29pIG5vIFRIQU5HLCB2YSBtb3QgYWN0aW9ubGludCBraG9uZyBjaGF5IChzYWkga2ll'
'biB0cnVjLAogICAgIyBob25nKSBsYW0gY2EgYmEgRE8gImFjdGlvbmxpbnQgRE8gKHJjPS4uLikiIOKAlCBjYSAibGEiID0+'
'IFRSVU9UIGdpYSBzYXUgY2EgYm8gdGVzdCAoZG8gdHJlbiAyMDI2LTA5LTMwajogYWN0aW9ubGludCBnaWEKICAgICMgcmM9'
'MSA9PiBtdWMgMCBpbSBsYW5nLCB0MzMgImxhIikuIEJhbiBUSEFUIDEuNi4yNy8xLjcuNy8xLjcuOC8xLjcuMTIgZGV1IHJj'
'PTAgdmEgZGV1IGNobyB0MzMvdDEzNy90MTU5IFFVQSB0cmVuIDBlYTk1ZGUuCiAgICAjIGJhc2ggQ0hJIGhvaSBDTyBNQVQs'
'IGNvIGNodSBkaWNoOiBiYXNoIFdTTCAoU3lzdGVtMzIpIGxhbSB0MzUtdDQwIERPIG5odW5nIGNhIHNhdSBkZXUgTkdPQUlf'
'UEhBTV9WSSwgY29uIHQzMi90MTUyIHR1IGNob24KICAgICMgR2l0IEJhc2ggKF9iYXNoX3Bvc2l4IGN1YSB1bmcgdmllbikg'
'4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGo6IGJhc2gga2lldSBXU0wgPT4gdDM1LXQ0MCBETywgZGV1IHJvaSB2YW8gbmdvYWkg'
'cGhhbSB2aS4KICAgICMgQ0hBWSBEVU9DIGNodWEgcGhhaSBEVU5HIERVT0M6IGRvIHRyZW4gMjAyNi0wOS0zMGssIDBlYTk1'
'ZGUsIGFjdGlvbmxpbnQgVEhBVCAxLjQuMy8xLjUuMC8xLjUuMy8xLjYuMC8xLjYuOC8xLjYuMTUvMS42LjIwLwogICAgIyAx'
'LjYuMjIgZGV1IGAtdmVyc2lvbmAgcmM9MCwgbWEgY2EgdGFtIGxhbSB0MTM3L3QxNTkgRE8gKGBwcm9wZXJ0eSAicnVuX2F0'
'dGVtcHQiLyJ3b3JrZmxvd19zaGEiIGlzIG5vdCBkZWZpbmVkYCksIDEuNC4zLzEuNS4wCiAgICAjIHRoZW0gdDMzIChgbXVz'
'dCBiZSBjb250YWluZWQgd2l0aGluICR7eyB9fWApIOKAlCBlMmUgMS42LjIyOiByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCwg'
'YGxhOiBbJ3QxMzcnLCAndDE1OSddYCBjaG8gdW5nIHZpZW4KICAgICMgc2FjaDsgMS42LjIzLzEuNi4yNC8xLjYuMjYvMS42'
'LjI3LzEuNy4wLzEuNy42LzEuNy43LzEuNy4xMiBRVUEgY2EgYmEuIFNhbiBsYSBiYW4KICAgICMgZ2hpbSBDSSAoQUxfU0FO'
'KSwgS0hPTkcgcGhhaSAxLjYuMjMgZG8gdHJlbiBNT1QgdW5nIHZpZW46IHdvcmtmbG93IGN1YSB1bmcgdmllbiBzYXUgY28g'
'dGhlIGR1bmcgY3UgcGhhcCBtb2kgaG9uLCBtYSBDSSBjaGkgZG8KICAgICMgYmFuZyBiYW4gZ2hpbS4gQ3UgaG9uIHNhbiA9'
'PiBLSE9ORyBETyBEVU9DIChjaGFuIGNhIDEuNi4yMy0xLjcuNiBkYW5nIFFVQTogZmFpbC1jbG9zZSwga2hvbmcgcGhhaSBw'
'aGFuIHF1eWV0KS4gYHZgIGRhdTogYmFuCiAgICAjIGBnbyBpbnN0YWxsYCBpbiBgdjEuNy43YDsga2hvbmcgZG9jIGR1b2Mg'
'c28gKHZkLiBgKGRldmVsKWApID0+IEtIT05HIERPIERVT0MuCiAgICBpZiBub3QgX3RoaWV1X2NjOgogICAgICAgIF9hbCA9'
'IHN1YnByb2Nlc3MucnVuKFtfY2NbImFjdGlvbmxpbnQiXSwgIi12ZXJzaW9uIl0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRl'
'eHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICBlcnJvcnM9InJlcGxhY2Ui'
'LCB0aW1lb3V0PTYwKQogICAgICAgIF9hbF92ID0gcmUuc2VhcmNoKHIiKD9tKV52PyhcZCspXC4oXGQrKVwuKFxkKykiLCBf'
'YWwuc3Rkb3V0IG9yICIiKQogICAgICAgIGlmIF9hbC5yZXR1cm5jb2RlOgogICAgICAgICAgICBsb2kuYXBwZW5kKCJhY3Rp'
'b25saW50IHRyZW4gUEFUSCBjbyBtYXQgbmh1bmcgYGFjdGlvbmxpbnQgLXZlcnNpb25gIHJjIT0wIChraG9uZyBjaGF5IGR1'
'b2MpOiBjYWkgbGFpIGJhbiBnaGltIEFMX1ZFUiIpCiAgICAgICAgZWxpZiBub3QgX2FsX3Ygb3IgdHVwbGUoaW50KHgpIGZv'
'ciB4IGluIF9hbF92Lmdyb3VwcygpKSA8IEFMX1NBTjoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImFjdGlvbmxpbnQge19h'
'bF92Lmdyb3VwKDApIGlmIF9hbF92IGVsc2UgJyhraG9uZyBkb2MgZHVvYyBwaGllbiBiYW4pJ30gY3UgaG9uIGJhbiBnaGlt'
'IENJICIKICAgICAgICAgICAgICAgICAgICAgICBmInsnLicuam9pbihtYXAoc3RyLCBBTF9TQU4pKX0gKEFMX1ZFUik6IGJh'
'biBjdSBsYW0gdDEzNy90MTU5IERPICdsYScgdHJlbiB1bmcgdmllbiBzYWNoIOKAlCIKICAgICAgICAgICAgICAgICAgICAg'
'ICAiIGNhaSBiYW4gZ2hpbSAob3BzL2NhaV9hY3Rpb25saW50LnNoIHZvaSBBTF9WRVIpIikKICAgICAgICAjIGdpdCBjdW5n'
'IHRoZTogQ08gTUFUIGtob25nIHBoYWkgRFVORyBEVU9DLCB2YSBnaXQgQ1UgbGEgY29uZyBjdSBQSE8gQklFTiBuaGF0IHRy'
'b25nIGJvbi4gRG8gdHJlbiAyMDI2LTA5LTMwbCwgMGVhOTVkZSwgZ2l0CiAgICAgICAgIyBUSEFUIHF1YSBjdW5nIGNoYXko'
'KTogMi4yNS4xID0+IDE0MC8xNjYgKDIzIGNhICJsYSI6IGBpbml0IC1iYC4uLiksIDIuMzQuMSB2YSAyLjM1LjEgPT4gMTYz'
'LzE2NiAodDEwOSB0MTEwIHQxMTE6IGBnaXQKICAgICAgICAjIHdvcmt0cmVlIGxpc3QgLS1wb3JjZWxhaW4gLXpgIHJjPTEy'
'OSBgdW5rbm93biBzd2l0Y2ggemApLCBlMmUgMi4zNS4xIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgOyAyLjM2LjEgPT4gMTY2'
'LzE2Ni4gU2FuIGxheQogICAgICAgICMgdHUgdGluaCBuYW5nIG1hIENISU5IIG1hIGR1b2MgZG8gZ29pIChvcHMvY29uZ19j'
'dS55YW1sIGRlIGJhbl9naGltIGdpdCA9IG51bGwgbmVuIGtob25nIGNvIGJhbiBnaGltIENJIGRlIGR1YSB2YW8pLgogICAg'
'ICAgICMgYGdpdCB2ZXJzaW9uIDIuNDcuMS53aW5kb3dzLjFgIChHaXQgZm9yIFdpbmRvd3MpIHZhIGAyLjM5LjMgKEFwcGxl'
'IEdpdC0xNDYpYCBkZXUgZG9jIGR1b2MgYmEgc28gZGF1LgogICAgICAgICMgVmEgcGhhaSBob2kgRFVORyBnaXQgbWEgYm8g'
'dGVzdCBTRSBHT0kuIEJvIHRlc3QgS0hPTkcgYHNodXRpbC53aGljaCgiZ2l0IilgIG5odSBiYSBjb25nIGN1IHRyZW46IEdP'
'SV9HSVQgY3VhIHVuZyB2aWVuIHZhIG1vaQogICAgICAgICMgZml4dHVyZSBnb2kgYGdpdGAgVFJBTiDigJQgdHJlbiBXaW5k'
'b3dzIGxhIENyZWF0ZVByb2Nlc3NXOiBDSEkgdHUgdGhlbSBgLmV4ZWAgKEtIT05HIFBBVEhFWFQpLCB0cmEgdGh1IG11YyBw'
'eXRob24uZXhlLCBjd2QKICAgICAgICAjIHZhIFN5c3RlbTMyIFRSVU9DIFBBVEguIGB3aGljaGAgdGhpIHRyYSBQQVRIRVhU'
'LCBuZW4gbW90IGBnaXQuY21kYC9gZ2l0LmJhdGAgZHVuZyB0cnVvYyBgZ2l0LmV4ZWAgQ1UgdHJlbiBQQVRIIGR1b2MgaG9p'
'CiAgICAgICAgIyBUSEFZIG5vIOKAlCBkbyB0cmVuIDIwMjYtMTAtMDEgKG5oYW5oIHdpbjMyIFRIQVQgY3VhIHNodXRpbC53'
'aGljaDsgc2hpbSBgZ2l0LkNNRGAgbW9pIHRydW9jIGdpdCAyLjM1LjEgVEhBVCk6IGJhbiAzMG0gbXVjIDAKICAgICAgICAj'
'IGltLCBlMmUgcmM9MSBgREFUIDExIHwgVFJVT1QgMWAsIGBsYTogWyd0MTA5JywgJ3QxMTAnLCAndDExMSddYC4gTmVuIGhv'
'aSBiYW5nIENISU5IIGR1b25nIGF5OiB0aWVuIHRyaW5oIGNvbiBjdWEgY2hheSgpCiAgICAgICAgIyAoY3VuZyBweXRob24s'
'IGN1bmcgbW9pIHRydW9uZywgY3dkID0gZ29jIG5odSBibyB0ZXN0KSBnb2kgYGdpdCAtLXZlcnNpb25gIFRSQU4uCiAgICAg'
'ICAgX3JjX2d2LCBfcmFfZ3YgPSBjaGF5KFsiLWMiLCAiaW1wb3J0IHN1YnByb2Nlc3MsIHN5czsgcCA9IHN1YnByb2Nlc3Mu'
'cnVuKFsnZ2l0JywgJy0tdmVyc2lvbiddLCBjYXB0dXJlX291dHB1dD1UcnVlLCIKICAgICAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICAgICIgdGV4dD1UcnVlLCB0aW1lb3V0PTYwKTsgcHJpbnQocC5zdGRvdXQpOyBzeXMuZXhpdChwLnJldHVy'
'bmNvZGUpIl0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGdvYyBpZiBnb2MuaXNfZGlyKCkgZWxzZSBQYXRoLmN3'
'ZCgpLCBwaHV0PTIpCiAgICAgICAgX2d2X20gPSByZS5zZWFyY2gociIoP20pXmdpdCB2ZXJzaW9uXHMrKFxkKylcLihcZCsp'
'XC4oXGQrKSIsIF9yYV9ndikKICAgICAgICBnaGkoImdpdF9ib190ZXN0IiwgX2d2X20uZ3JvdXAoMCkgaWYgX2d2X20gZWxz'
'ZSBOb25lKQogICAgICAgIGlubigiICBnaXQgYm8gdGVzdCAgOiIsIF9ndl9tLmdyb3VwKDApIGlmIF9ndl9tIGVsc2UgZiIo'
'a2hvbmcgZG9jIGR1b2MgcGhpZW4gYmFuLCByYz17X3JjX2d2fSkiKQogICAgICAgIGlmIF9yY19ndjoKICAgICAgICAgICAg'
'bG9pLmFwcGVuZChmImBnaXQgLS12ZXJzaW9uYCBnb2kgVFJBTiBuaHUgYm8gdGVzdCByYyE9MCAoeyhfcmFfZ3Yuc3RyaXAo'
'KS5zcGxpdGxpbmVzKCkgb3IgWycnXSlbLTFdWzo5MF19KTogY2FpIGxhaSBnaXQiKQogICAgICAgIGVsaWYgbm90IF9ndl9t'
'IG9yIHR1cGxlKGludCh4KSBmb3IgeCBpbiBfZ3ZfbS5ncm91cHMoKSkgPCBHSVRfU0FOOgogICAgICAgICAgICBsb2kuYXBw'
'ZW5kKGYiZ2l0IHsnLicuam9pbihfZ3ZfbS5ncm91cHMoKSkgaWYgX2d2X20gZWxzZSAnKGtob25nIGRvYyBkdW9jIHBoaWVu'
'IGJhbiknfSBjdSBob24gIgogICAgICAgICAgICAgICAgICAgICAgIGYieycuJy5qb2luKG1hcChzdHIsIEdJVF9TQU4pKX0g'
'KHVuZyB2aWVuIGdvaSBgZ2l0IHdvcmt0cmVlIGxpc3QgLS1wb3JjZWxhaW4gLXpgKTogY2FwIG5oYXQgZ2l0IikKCnJjLCBo'
'ZWFkLCBfID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxvaS5hcHBlbmQoImtob25nIGRvYyBkdW9j'
'IEhFQUQiKQpnaGkoImhlYWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAiLS1pcy1hbmNl'
'c3RvciIsIFNIQV9HMSwgaGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNfYSA9PSAwKQppZiBoZWFkID09IFNIQV9H'
'MToKICAgIHRoZV9oZSA9ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gREFZIExBIGcxLiBDSFVBIGNvIGJh'
'biB2YSBnMjsga2V0IHF1YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9kdWU6CiAgICB0aGVfaGUgPSAiZzIiOyBp'
'bm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hBX0cxWzo4XX0pOyB1bmcgdmllbiBnMiBo'
'YXkga2hvbmc6IE43JyAobXVjIDEpIGRpbmggZGFuaC4iKQplbHNlOgogICAgdGhlX2hlID0gIj8iOyBsb2kuYXBwZW5kKGYi'
'SEVBRD17aGVhZFs6OF19IEtIT05HIHBoYWkgZzEgdmEgS0hPTkcgcGhhaSBoYXUgZHVlIGN1YSB7U0hBX0cxWzo4XX0g4oCU'
'IHJlYmFzZT8gbmhhbSBuaGFuaD8iKQpnaGkoInRoZV9oZSIsIHRoZV9oZSkKcmNfciwgcmVmcywgXyA9IGdpdChnb2MsICJm'
'b3ItZWFjaC1yZWYiLCAiLS1wb2ludHMtYXQiLCBoZWFkIG9yICJIRUFEIiwKICAgICAgICAgICAgICAgICAgICAiLS1mb3Jt'
'YXQ9JShyZWZuYW1lOnNob3J0KSIpCmRzciA9IFt4IGZvciB4IGluIHJlZnMuc3BsaXRsaW5lcygpIGlmIHguc3RyaXAoKSBh'
'bmQgeC5zdHJpcCgpICE9ICJkby10YW0iXQpnaGkoInJlZl90cm9fdG9pX2hlYWQiLCBkc3IpCmlubihmIiAgcmVmIHRybyB0'
'b2kgSEVBRDogeycsICcuam9pbihkc3IpIGlmIGRzciBlbHNlICcoa2hvbmcgcmVmIG5hbyAtIEhFQUQgcm9pIHR1IGRvKSd9'
'IikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogbmVuIGRvIHNhaSwgS0hPTkcgaW4ga2V0IGx1'
'YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlubigiICAtIiwgeCkKICAgIHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0t'
'LS0tLS0gMS4ga2ljaCB0aHVvYyAoTjcnIGN1YSBzcGVjIHIzKSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIg'
'KiA3OCk7IGlubigiMS4gS0lDSCBUSFVPQyDigJQgdHJhbiBzcGVjIHIzOiA8PSAyIHRlcCB2YSA8PSA0MDAgZG9uZyB0aGVt'
'IikKIyBWRSBORU4gUEhBSSBUVU9JIOKAlCB2YSBwaGFpIENIVU5HIE1JTkggZHVvYyBsYSB0dW9pLCBraG9uZyBwaGFpIGdp'
'YSBkaW5oLgojIEJhaSBob2MgdHJhIGdpYSAxOS0wOS0yMDI2OiBjbG9uZSB0YWkgZHVuZyBjaGkgZmV0Y2ggbmhhbmggYmFu'
'IHZhLCBgb3JpZ2luL21hc3RlcmAKIyBkdW5nIHllbiB0dSAxNC0wOSAoYzE2YmQzMiwgc2F1IDk3IGNvbW1pdCkuIG1lcmdl'
'LWJhc2Ugcm9pIHZlIGR1bmcgZGluaCBtYXN0ZXIgY3UsCiMgbmVuIGRpZmYgTlVPVCBjYSA5NyBjb21taXQgbWFzdGVyOiBk'
'byByYSA0NiB0ZXAgLyArNzExOCB0aGF5IHZpIDIgdGVwIC8gKzM5NyDigJQKIyBDVU5HIE1PVCBDT01NSVQgMGVhOTVkZS4g'
'TW90IHRpZXUgY2hpIERFTFRBIG1hIHZlIG5lbiBraG9uZyB0dW9pIHRoaSBraG9uZyBzYWkKIyBsZWNoIG1vdCBjaHV0LCBu'
'byBzYWkgY2EgbW90IGJhYyBkbyBsb24uCiMgQ2hvIG5lbjogbmVuIGtob25nIGNodW5nIG1pbmggZHVvYyBsYSB0dW9pID0+'
'IEtIT05HIERPIERVT0MgKHJjPTMpLCBLSE9ORyBwaGFpIFRSVU9ULgojIFRSVU9UIGxhIG1vdCBQSEFOIFFVWUVUIHZlIGJh'
'biB2YTsgcGhhbiBxdXlldCBjaGkgZHVvYyBwaGVwIHBoYXQgcmEga2hpIGRhIGRvIGR1b2MuCmVyID0gIiIKcmNfdSwgdXJs'
'X3RobywgXyA9IGdpdChnb2MsICJyZW1vdGUiLCAiZ2V0LXVybCIsICJvcmlnaW4iKQp1cmxfbywgdXJsX2luID0gX3VybF9z'
'YWNoKHVybF90aG8pLCBfdXJsX2luKHVybF90aG8pCmdoaSgib3JpZ2luX3VybCIsIHVybF9pbik7IGlubihmIiAgb3JpZ2lu'
'ICAgICAgIDoge3VybF9pbiBvciAnKGtob25nIGRvYyBkdW9jKSd9IikKdXJsX29rID0gKG5vdCByY191KSBhbmQgdXJsX28u'
'cnN0cmlwKCIvIikgaW4gVVJMX0tIT19IT1BfTEUKcmNfbHIsIG91dF9sciwgZXJfbHIgPSBnaXQoZ29jLCAibHMtcmVtb3Rl'
'IiwgIm9yaWdpbiIsICJyZWZzL2hlYWRzL21hc3RlciIpIGlmIHVybF9vayBlbHNlICgxLCAiIiwgIiIpCmVyX2xyID0gX2Fu'
'X3VzZXJpbmZvKGVyX2xyKQpyY19sbSwgbG0sIGVyX2xtICAgICA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAib3JpZ2luL21h'
'c3RlciIpCnJtID0gb3V0X2xyLnNwbGl0KClbMF0gaWYgKG5vdCByY19sciBhbmQgb3V0X2xyLnN0cmlwKCkpIGVsc2UgIiIK'
'aWYgbm90IHVybF9vazoKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYib3JpZ2luPXt1cmxfaW4hcn0gS0hPTkcg'
'cGhhaSBraG8gdGhhdCDigJQgJ3R1b2knIHNvIHZvaSBubyBraG9uZyBjaHVuZyBtaW5oIGR1b2MgZ2kiKQogICAgcmNfbWIs'
'IG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBub3Qgcm06CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAog'
'ICAgICAgIGYia2hvbmcgaG9pIGR1b2MgbWFzdGVyIHRyZW4gcmVtb3RlIChscy1yZW1vdGUgcmM9e3JjX2xyfSk6IHtlcl9s'
'cls6NjBdfSAiCiAgICAgICAgZiLigJQga2hvbmcgY2h1bmcgbWluaCBkdW9jIHZlIG5lbiBjb24gdHVvaSIpCiAgICByY19t'
'YiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIHJjX2xtIG9yIG5vdCBsbToKICAgIGtldCgiTjcnIGtpY2ggdGh1'
'b2MiLCBLREQsIGYia2hvbmcgZG9jIGR1b2Mgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZToge2VyX2xtWzo2MF19IikKICAg'
'IHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbG0gIT0gcm06CiAgICAjIERlbSB4ZW0gdHV0IGxhaSBi'
'YW8geGEsIG5ldSBkZW0gZHVvYyDigJQgY29uIHNvIG5heSBub2kgcm8gbXVjIGRvIHNhaSBsZWNoLgogICAgcmNfYywgc2F1'
'LCBfID0gZ2l0KGdvYywgInJldi1saXN0IiwgIi0tY291bnQiLCBmIntsbX0uLntybX0iKQogICAgeGEgPSBmIiwgdHV0IGxh'
'aSB7c2F1fSBjb21taXQiIGlmIChub3QgcmNfYyBhbmQgc2F1LnN0cmlwKCkuaXNkaWdpdCgpKSBlbHNlICIiCiAgICBpbm4o'
'ZiIgIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmUgOiB7bG1bOjEyXX0iKQogICAgaW5uKGYiICBtYXN0ZXIgdHJlbiByZW1v'
'dGUgICAgICAgIDoge3JtWzoxMl19e3hhfSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVt'
'b3RlIiwgcm0pCiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAogICAgICAgIGYidmUgbmVuIENVOiBvcmlnaW4vbWFz'
'dGVyPXtsbVs6MTJdfSAhPSByZW1vdGU9e3JtWzoxMl19e3hhfSAiCiAgICAgICAgZiLigJQgY2hheSBgZ2l0IC1DIDxraG8+'
'IGZldGNoIG9yaWdpbiBtYXN0ZXJgIHJvaSBkbyBsYWkiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEK'
'ZWxzZToKICAgIGlubihmIiAgdmUgbmVuIFRVT0k6IG9yaWdpbi9tYXN0ZXIgPSB7bG1bOjEyXX0gPT0gbWFzdGVyIHRyZW4g'
'cmVtb3RlIikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIHJjX21i'
'LCBtYiwgZXJfbWIgPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICJvcmlnaW4vbWFzdGVyIiwgaGVhZCkKaWYgcmNfbWIgb3Ig'
'bm90IG1iOgogICAgaWYgbWIgPT0gIiIgYW5kIHJtIGFuZCBsbSA9PSBybToKICAgICAgICBrZXQoIk43JyBraWNoIHRodW9j'
'IiwgS0RELCBmImtob25nIHRpbmggZHVvYyBtZXJnZS1iYXNlIHZvaSBvcmlnaW4vbWFzdGVyOiB7ZXJfbWJbOjcwXX0iKQog'
'ICAgbnMsIHJjID0gIiIsIDEKZWxzZToKICAgIGdoaSgibWVyZ2VfYmFzZSIsIG1iKQogICAgaW5uKGYiICBtZXJnZS1iYXNl'
'KG9yaWdpbi9tYXN0ZXIsIEhFQUQpID0ge21iWzoxMl19IikKICAgIGlmIG1iICE9IFNIQV9CQVNFX1NQRUM6CiAgICAgICAg'
'aW5uKGYiICBMVVUgWToga2hhYyBiYXNlIG1hIHNwZWMgcjMga2hhaSAoe1NIQV9CQVNFX1NQRUNbOjEyXX0pIOKAlCB2aSBu'
'aGFuaCBkYSBtZXJnZSBtYXN0ZXIuIikKICAgICAgICBpbm4oIiAgICAgICAgIERvIHNvIGJhc2UgY3Ugc2UgTlVPVCBwaGFu'
'IG1hc3RlciBtYW5nIHZhby4gRHVuZyBtZXJnZS1iYXNlIG1vaSBsYSB2aWVjIGN1YSBleGVjdXRvci4iKQogICAgICAgIHJj'
'X3gsIG5zX3gsIF8gPSBnaXQoZ29jLCAiZGlmZi10cmVlIiwgIi1yIiwgIi1NIiwgIi0tZGlmZi1hbGdvcml0aG09bXllcnMi'
'LCAiLS1udW1zdGF0IiwgU0hBX0JBU0VfU1BFQywgaGVhZCkKICAgICAgICBpZiBub3QgcmNfeDoKICAgICAgICAgICAgaCA9'
'IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zX3guc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgICAgICAgICAgYSA9'
'IHN1bShpbnQoeFswXSkgZm9yIHggaW4gaCBpZiB4WzBdLmlzZGlnaXQoKSkKICAgICAgICAgICAgZ2hpKCJudW1zdGF0X3Ro'
'ZW9fYmFzZV9zcGVjIiwgeyJ0ZXAiOiBsZW4oaCksICJ0aGVtIjogYX0pCiAgICAgICAgICAgIGlubihmIiAgICAgICAgIChk'
'b2kgY2hpZXU6IHNvIGJhc2Ugc3BlYyA9IHtsZW4oaCl9IHRlcCAvICt7YX0g4oCUIGNvbiBzbyBheSBLSE9ORyBkdW5nIGRl'
'IGNoYW0pIikKICAgICMgUExVTUJJTkcsIGtob25nIFBPUkNFTEFJTjogYGdpdCBkaWZmYCBkb2MgY2F1IGhpbmggVUkgQ1VB'
'IE5HVU9JIERPIChkaWZmLmFsZ29yaXRobSwgZGlmZi5yZW5hbWVzLCBkaWZmLm9yZGVyRmlsZSwKICAgICMgY29sb3IuZGlm'
'ZiksIHZhIGdpYSB0cmkgSE9QIExFIGRvaSBsdW9uIFNPIGRvbmcgbWEgdmFuIHJhIGNodSBzbyDigJQgZG8gdHJlbiAyMDI2'
'LTA5LTMwaTogdW5nIHZpZW4gdG9uZyBob3AgKG15ZXJzICs0MDEpID0+CiAgICAjIGJhbiAzMGkgREFUIDIgdGVwIC8gKzQw'
'MCBkdW9pIGBkaWZmLmFsZ29yaXRobSA9IGhpc3RvZ3JhbWAgaG9hYyBgcGF0aWVuY2VgLCBUUlVPVCArNDAxIGtoaSBtYWMg'
'ZGluaDsgMTAvNzUgY29tbWl0IGNoYW0KICAgICMgd3JpdGUgc2V0IGNvIHNvIGRvbmcgZG9pIHRoZW8gdGh1YXQgdG9hbi4g'
'YGRpZmYtdHJlZSAtciAtTWAgPSBtYWMgZGluaCBjdWEgYGdpdCBkaWZmYCAocmVuYW1lcyBiYXQpIHZhIEtIT05HIGRvYyBj'
'YWMga2hvYQogICAgIyBheS4gVGh1YXQgdG9hbiBwaGFpIFRVT05HIE1JTkg6IGRpZmYuPGRyaXZlcj4uYWxnb3JpdGhtIChx'
'dWEgY29yZS5hdHRyaWJ1dGVzRmlsZSBjdWEgbmd1b2kgZG8pIFZBTiBsb3QgdmFvIHBsdW1iaW5nIOKAlAogICAgIyBkbyB0'
'cmVuIDIwMjYtMDktMzBpLCBgKi5weSBkaWZmPWFsZ2AgKyBkaWZmLmFsZy5hbGdvcml0aG09aGlzdG9ncmFtOiBkaWZmLXRy'
'ZWUgKzQwMSBjaG8gdW5nIHZpZW4gbXllcnMgKzQwMDsgY28gdHVvbmcgbWluaAogICAgIyB0aGFuZyBraG9hIGF5LiBhdHRy'
'aWJ1dGVzIGAtZGlmZmAvY29yZS5iaWdGaWxlVGhyZXNob2xkIHZhbiBhcCA9PiBgLWAgPT4gS0hPTkcgRE8gRFVPQyAoY2hv'
'dCBkdW9pKS4KICAgIHJjLCBucywgZXIgPSBnaXQoZ29jLCAiZGlmZi10cmVlIiwgIi1yIiwgIi1NIiwgIi0tZGlmZi1hbGdv'
'cml0aG09bXllcnMiLCAiLS1udW1zdGF0IiwgbWIsIGhlYWQpCmlmIHJjOgogICAgcGFzcwplbHNlOgogICAgaGFuZyA9IFts'
'LnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICB0aGVtID0gc3VtKGludCho'
'WzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdpdCgpKQogICAgeG9hICA9IHN1bShpbnQoaFsxXSkgZm9yIGggaW4g'
'aGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgic29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hpKCJkb25nX3RoZW0iLCB0'
'aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZvciBoIGluIGhhbmc6IGlubihmIiAgICB7aFsyXTozNH0gK3toWzBd'
'Ojw1fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05HOiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17eG9hfSAgICh0'
'cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcgdGhlbSkiKQogICAgY2hhbSA9IHNvcnRlZCh7aFsyXSBm'
'b3IgaCBpbiBoYW5nfSAmIFdSSVRFX1NFVF9HMik7IGdoaSgiY2hhbV93cml0ZV9zZXQiLCBjaGFtKQogICAgZGVmIF9jYV9t'
'b2lfY28ocmV2KToKICAgICAgICAjIGNhdC1maWxlLCBraG9uZyBgc2hvd2A6IGBnaXQgc2hvd2AgY2hldCB2b2kgY2F1IGhp'
'bmggVUkgZ28gc2FpIChkbyB0cmVuIDIwMjYtMDktMzBpOiBsb2cuZGF0ZSBnbyBzYWkgPT4gYmFuIDMwaSBnb2kKICAgICAg'
'ICAjIDBlYTk1ZGUgbGEgImtob25nIHBoYWkgdW5nIHZpZW4gLi4uIE5vbmUg4oCUIGRhIGxhbmQ/IG5oYW0gbmhhbmg/Iiku'
'CiAgICAgICAgcl8sIG5kXywgXyA9IGdpdChnb2MsICJjYXQtZmlsZSIsICItcCIsIGYie3Jldn06b3BzL2xlYXNlX3B1Ymxp'
'c2hfdGVzdC5weSIpCiAgICAgICAgcmV0dXJuIE5vbmUgaWYgcl8gZWxzZSB7dCBmb3IgdCBpbiBDQV9NT0lfRzIgaWYgcmUu'
'c2VhcmNoKHIiKD9tKV5kZWYgIiArIHQgKyByIlthLXpdP18iLCBuZF8pfQogICAgb19tYiwgb19oID0gX2NhX21vaV9jbyht'
'YiksIF9jYV9tb2lfY28oaGVhZCkKICAgIG1hbmcgPSBzb3J0ZWQob19oIC0gb19tYiwga2V5PXNvX2NhKSBpZiAob19tYiBp'
'cyBub3QgTm9uZSBhbmQgb19oIGlzIG5vdCBOb25lKSBlbHNlIE5vbmUKICAgIGdoaSgiY2FfbW9pX2cyX21hbmdfdmFvIiwg'
'bWFuZykKICAgIGlmIG5vdCBtYW5nOgogICAgICAgICMgRG8gUk9ORyAoZGEgbGFuZCwgY2hpbmggbWFzdGVyKSwgbmhhbSBu'
'aGFuaCwgaGF5IG5oYW5oIGN1YSBwYWNrZXQgS0hBQyBjaGFtIGN1bmcgdGVwOgogICAgICAgICMga2hvbmcgbWFuZyBjYSBt'
'b2kgbmFvIGN1YSBnMiB0aGkga2hvbmcgcGhhaSB1bmcgdmllbi4gRG9jIGtob25nIGR1b2MgKE5vbmUpIGN1bmcgdmF5Lgog'
'ICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYiZG9pIHR1b25nIGtob25nIHBoYWkgdW5nIHZpZW46IHtsZW4o'
'aGFuZyl9IHRlcCwgY2hhbSB7Y2hhbX0sIGNhIG1vaSAiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJn'
'MiBtYW5nIHZhbyB7bWFuZyFyfSDigJQgZGEgbGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/IikKICAgIGVsc2U6CiAg'
'ICAgICAgIyBudW1zdGF0IGluIGAtYCAoa2hvbmcgY28gc28gZG9uZykgY2hvIHRlcCBiaW5hcnkvLWRpZmYgdGhlbyBhdHRy'
'aWJ1dGVzIOKAlCBrZSBjYSBhdHRyaWJ1dGVzIENVQSBOR1VPSSBETyAoZG8gdHJlbgogICAgICAgICMgMjAyNi0wOS0zMGc6'
'IGNvcmUuYXR0cmlidXRlc0ZpbGUgYCoucHkgLWRpZmZgID0+ICIyIHRlcCAvICswIiBEQVQgY2hvIDBlYTk1ZGUsIHRoYXQg'
'KzM5NykuIGAtYCBsYSBLSE9ORyBETyBEVU9DLAogICAgICAgICMga2hvbmcgcGhhaSAwOyBUUlVPVCB0aGVvIHNvIHRlcCAv'
'IHNvIGRvbmcgREEgZGVtIGR1b2MgdmFuIGdpdSAocXVhbiBzYXQgdHJ1YyB0aWVwKS4KICAgICAgICBraG9uZ19zbyA9IFto'
'WzJdIGZvciBoIGluIGhhbmcgaWYgbm90IChoWzBdLmlzZGlnaXQoKSBhbmQgaFsxXS5pc2RpZ2l0KCkpXTsgZ2hpKCJ0ZXBf'
'a2hvbmdfc29fZG9uZyIsIGtob25nX3NvKQogICAgICAgIHZ1b3QgPSBsZW4oaGFuZykgPiBUUkFOX1RFUCBvciB0aGVtID4g'
'VFJBTl9ET05HCiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIFRSVU9UIGlmIHZ1b3QgZWxzZSAoS0REIGlmIGtob25n'
'X3NvIGVsc2UgREFUKSwKICAgICAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IiArIChmIiDigJQgbnVtc3Rh'
'dCBLSE9ORyBjbyBzbyBkb25nIGNobyB7a2hvbmdfc299IiBpZiBraG9uZ19zbyBlbHNlICIiKSkKCiMgQ29uZyBraWNoIHRo'
'dW9jIFBIQUkgZGUgbGFpIE1PVCBrZXQgcXVhLiBMZW5oIG51bXN0YXQgaG9uZyB0aGkgbmhhbmggYGlmIHJjOiBwYXNzYCBr'
'aG9uZyBnaGkgZ2ksIHZhIHZhbmcgbWF0IG8gZGF5CiMgdGhhbmggREFUIG8gYm8gZ29wOiBjYXUgaGluaCBkaWZmIENVQSBO'
'R1VPSSBETyBob25nIChkaWZmLm9yZGVyRmlsZSB0cm8gdGVwIGtob25nIGNvLCBkaWZmLmFsZ29yaXRobSBnbyBzYWkgPT4g'
'cmM9MTI4KSBjaG8KIyAtLWNoaS1raWNoLXRodW9jIHJjPTAgdm9pIDAgY2hvdCwgbHVvdCBkYXkgZHUgIkRBVCAxMSIgcmM9'
'MCAoZG8gdHJlbiAyMDI2LTA5LTMwaCwgMGVhOTVkZSkuIFZhbmcgbWF0IGxhIEtIT05HIERPIERVT0MuCiMgVHUgMzBqIG51'
'bXN0YXQgbGEgZGlmZi10cmVlIChraG9uZyBkb2MgaGFpIGtob2EgYXkpOyBkdW9uZyBjb24gbGFpIGRvIGR1b2M6IGRpZmYu'
'cmVuYW1lTGltaXQgZ28gc2FpID0+IHJjPTEyOC4KaWYgbm90IGFueShjWzBdID09ICJONycga2ljaCB0aHVvYyIgZm9yIGMg'
'aW4gY2hvdCk6CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImNvbmcgS0hPTkcgcmEga2V0IHF1YSAoZ2l0IGRp'
'ZmYtdHJlZSAtLW51bXN0YXQgcmM9e3JjfSk6IHtfYW5fdXNlcmluZm8oZXIpWzo3MF19IikKCiMgRGluaCBkYW5oIFRIQVQg'
'bmFtIG8gTjcnIChjYSBtb2kgZzIgbWFuZyB2YW8pLCBLSE9ORyBvICJoYXUgZHVlIGcxIjogZzEgZGEgbGFuZCBuZW4gbW9p'
'IG5oYW5oIGRldQojIGxhIGhhdSBkdWUuIERvbmcgZGF1IGtob2kgZGFuIHBoYWkgdHUga2hhaSB0aGVvIGtldCBxdWEgYXkg'
'KGRvIGR1b2M6IG1hc3RlciA0NDYyMGU4IG1vIGtob2kgYmFuZwojICJUSEUgSEUgRE8gRFVPQzogZzIiLCBKU09OICJ0aGVf'
'aGUiOiAiZzIiLCB0cm9uZyBraGkgTjcnIGRhIGtldCBsdWFuICJraG9uZyBwaGFpIHVuZyB2aWVuIikuCiMgTmhhbiBjaGkg'
'ZHVvYyBub2kgRFVORyBjYWkgZG8gZHVvYzogYFtdYCBraG9uZyB0YWNoICJkYSBsYW5kIiBraG9pICJuaGFtIG5oYW5oIi8i'
'cGFja2V0IGtoYWMiIChkbwojIGR1b2MgdHJlbiAyMDI2LTA5LTMwYjogdW5nIHZpZW4gMmE2Nzk2OCBEQSBMQU5EIGJpIGdv'
'aSAiS0hPTkcgcGhhaSB1bmcgdmllbiBnMiIpLgppZiB0aGVfaGUgPT0gImcyIiBhbmQgbm90IHNvLmdldCgiY2FfbW9pX2cy'
'X21hbmdfdmFvIik6CiAgICB0aGVfaGUgPSAoIktIT05HIG1hbmcgY2EgbW9pIGcyIG5hbyAoZGEgbGFuZD8gbmhhbSBuaGFu'
'aD8gcGFja2V0IGtoYWM/KSIgaWYgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKSA9PSBbXQogICAgICAgICAgICAgIGVs'
'c2UgImcyPyAoQ0hVQSBkaW5oIGRhbmggZHVvYyBkb2kgdHVvbmcpIikKICAgIGdoaSgidGhlX2hlIiwgdGhlX2hlKQoKIyBD'
'b25nIG5oYW5oOiBkbyBSSUVORyBraWNoIHRodW9jICh2YWkgZ2lheSkgcm9pIGR1bmcuIER1bmcga2hpIGNhbiB4YWMgbWlu'
'aCBsYWkKIyB2ZSBuZW4gbWEga2hvbmcgbXVvbiB0cmEgMjAtNDUgcGh1dCBjaG8gY2EgYm8gdGVzdC4KaWYgIi0tY2hpLWtp'
'Y2gtdGh1b2MiIGluIHN5cy5hcmd2OgogICAgaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQogICAgaW5uKCItLWNoaS1raWNoLXRo'
'dW9jOiBDSEkgZG8gY29uZyBraWNoIHRodW9jLiBEYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCiAgICBp'
'bm4oIi0iICogNzgpCiAgICBmb3IgX3QsIF90dCwgX2N0IGluIGNob3Q6IGlubihmIiAge190dDoxNH0ge190fSIgKyAoZiIg'
'ICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgX2sgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0RE'
'KQogICAgX3IgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCiAgICBzeXMuZXhpdCgzIGlmIF9r'
'IGVsc2UgKDEgaWYgX3IgZWxzZSAwKSkKCkNISV9QUk9CRSA9ICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YgICAgIyBibyBx'
'dWEgYm8gdGVzdCArIE43OyBnaXUgMCwgMSwgMwojIC0tLS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVzdCBkYXkgZHUgLS0tLS0t'
'LS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIyLiBCTyBURVNU'
'IERBWSBEVSAoMTAtNDAgcGh1dCkiKQogICAgcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5w'
'eSJdLCBnb2MpCiAgICBnaGkoInJjX3N1aXRlIiwgcmNfbikKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXRfbikKICAgIGlu'
'bigiICByYyA9IiwgcmNfbiwgInwiLCBtLmdyb3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBr'
'ZXQpIikKICAgIGlmIG06CiAgICAgICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGkoInRyZW4iLCBpbnQobS5n'
'cm91cCgyKSkpOyBnaGkoImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKICAgIGRvX2hldCwgZ2MsIHRpbiA9IGRvY19k'
'byhvdXRfbikKICAgIGdoaSgic29fY2FfZG8iLCBsZW4oZG9faGV0KSk7IGdoaSgibGlldF9rZV9kYXlfZHUiLCB0aW4pCiAg'
'ICBmb3IgZyBpbiBnYzogaW5uKCIgICAqIiwgZykKICAgIGlubigiIik7IGlubihmIiAgPT09IHtsZW4oZG9faGV0KX0gQ0Eg'
'RE8gPT09IikKICAgIGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaW5uKGYiICAge3Quc3Bs'
'aXQoJ18nKVswXTo3fSB7dH0iKTsgaW5uKGYiICAgICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCiAgICBnaGkoImRvX2x5'
'X2RvIiwge3Q6IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQogICAgIyAtLS0tIENIT1Q6IG1vaSBjYSBETyBw'
'aGFpIEdJQUkgVEhJQ0ggRFVPQyAtLS0tCiAgICAjIFRoaWV1IGNob3QgbmF5LCBibyBkbyBpbiBkYW5oIHNhY2ggZG8gcm9p'
'IHZhbiB0aG9hdCByYz0wLiBEbyBkdW5nIGxhIGxvaSBkYSB4YXkgcmE6CiAgICAjIGx1b3QgV2luZG93cyAxOS0wOSBjbyB0'
'MTcxIERPIG1hIGJvIGRvIGJhbyAiREFUIDEwIHwgVFJVT1QgMCIgdmEgcmM9MC4KICAgIGRlZiBfa2hvYSh0KTogcmV0dXJu'
'IHQuc3BsaXQoIl8iKVswXQogICAgZG9fcGFja2V0LCBkb19sYSwgZG9fdGhpZXVfY29uZ19jdSA9IFtdLCBbXSwgW10KICAg'
'IGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaywgbHkgPSBfa2hvYSh0KSwgZG9faGV0W3Rd'
'CiAgICAgICAgaWYgayBpbiBDQV9QQUNLRVQ6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fcGFja2V0LmFwcGVu'
'ZCh0KQogICAgICAgIGVsaWYgIktIw5RORyDEkE8gxJDGr+G7okMiIGluIGx5IG9yICJ0aGnhur91IGAiIGluIGx5OiAgZG9f'
'dGhpZXVfY29uZ19jdS5hcHBlbmQodCkKICAgICAgICBlbGlmIGsgaW4gTkdPQUlfUEhBTV9WSTogICAgICAgICAgICAgICAg'
'ICAgICAgICBwYXNzCiAgICAgICAgZWxzZTogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9f'
'bGEuYXBwZW5kKHQpCiAgICBnaGkoImRvX3BhY2tldCIsIGRvX3BhY2tldCk7IGdoaSgiZG9fbGEiLCBkb19sYSk7IGdoaSgi'
'ZG9fdGhpZXVfY29uZ19jdSIsIGRvX3RoaWV1X2NvbmdfY3UpCiAgICBpbm4oIiIpCiAgICBpbm4oZiIgIGNhIERPIHRodW9j'
'IENISU5IIHBhY2tldCBuYXkgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF0gb3IgJ2tob25nIGNvJ30iKQogICAg'
'aW5uKGYiICBjYSBETyBuZ29haSBwaGFtIHZpIChyMyBraGFpKToge1tfa2hvYSh4KSBmb3IgeCBpbiBzb3J0ZWQoZG9faGV0'
'LCBrZXk9c29fY2EpIGlmIF9raG9hKHgpIGluIE5HT0FJX1BIQU1fVkldfSIpCiAgICBpbm4oZiIgIGNhIERPIHZpIFRISUVV'
'IENPTkcgQ1UgICAgICAgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9yICdraG9uZyBjbyd9IikK'
'ICAgIGlubihmIiAgY2EgRE8gTEEgKGtob25nIGdpYWkgdGhpY2ggZHVvYyk6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFd'
'IG9yICdraG9uZyBjbyd9IikKICAgICMgLS0tLSBDSE9UOiBwaGVwIGRvIHBoYWkgVFJPTiB0cnVvYyBraGkgbW90IGNodSBE'
'QVQgbmFvIGR1b2MgcGhhdCAtLS0tCiAgICAjIEJhbiB0cnVvYyBjaGkgSU4gYHRpbmAvYHJjX3N1aXRlYDogYm8gdGVzdCBj'
'aGV0IGdpdWEgdDE3MSAocmM9MTM0LCBraG9uZyBkb25nIHRvbmcpCiAgICAjIHZhbiByYSAiREFUIDEyIHwgVFJVT1QgMCIg'
'cmM9MDsgY2EgUEFDS0VUIHZhbmcgbWF0IGhheSBiaSBCTyBRVUEgY3VuZyBkdW9jIGNoYW0gbmh1CiAgICAjICJraG9uZyBk'
'byIuIFZhbmcgbWF0IGtob25nIHBoYWkgImtob25nIGRvIiDigJQgbGEgS0hPTkcgRE8gRFVPQy4KICAgIHZhbmcgPSBbdCBm'
'b3IgdCBpbiBzb3J0ZWQoQ0FfUEFDS0VULCBrZXk9c29fY2EpIGlmIG1hdV9jYShvdXRfbiwgdCkgbm90IGluICgiUVVBIiwg'
'IkRPIildCiAgICBseV9rZGQgPSBbXQogICAgaWYgbm90IHRpbjogbHlfa2RkLmFwcGVuZCgiZGFuaCBzYWNoIGRvIEtIT05H'
'IGRheSBkdSIpCiAgICBpZiByY19uIG5vdCBpbiAoMCwgMSkgb3IgKHJjX24gPT0gMSkgIT0gYm9vbChkb19oZXQpOgogICAg'
'ICAgIGx5X2tkZC5hcHBlbmQoZiJyYyBibyB0ZXN0PXtyY19ufSBraG9uZyBraG9wIHtsZW4oZG9faGV0KX0gY2EgRE8gZG9j'
'IGR1b2MiKQogICAgaWYgdmFuZzogbHlfa2RkLmFwcGVuZChmImNhIFBBQ0tFVCB2YW5nL2JvIHF1YToge3Zhbmd9IikKICAg'
'IGdoaSgiY2FfcGFja2V0X3ZhbmciLCB2YW5nKTsgZ2hpKCJseV9kb19jaHVhX3Ryb24iLCBseV9rZGQpCiAgICBpZiBseV9r'
'ZGQ6IGtldCgiQm8gdGVzdCBjaGF5IFRST04gdmEgZG9jIERVIiwgS0RELCAiOyAiLmpvaW4obHlfa2RkKSkKICAgIGNodWFf'
'dHJvbiA9IEtERCBpZiBseV9rZGQgZWxzZSBEQVQKICAgIGtldCgiS2hvbmcgY2EgbmFvIGN1YSBQQUNLRVQgYmkgRE8iLCBj'
'aHVhX3Ryb24gaWYgbm90IGRvX3BhY2tldCBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBm'
'IkRPOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF19IOKAlCBiYW4gdmEgQ0hVQSB4b25nIikKICAgIGtldCgiTW9p'
'IGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MiLCBjaHVhX3Ryb24gaWYgbm90IGRvX2xhIGVsc2UgVFJVT1QsCiAgICAgICAg'
'IiIgaWYgbm90IGRvX2xhIGVsc2UgZiJsYToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV19IikKICAgIGlmIGRvX3RoaWV1'
'X2NvbmdfY3U6CiAgICAgICAga2V0KCJDb25nIGN1IGRheSBkdSBkZSBkbyIsIEtERCwgZiJ0aGlldSBjb25nIGN1IGNobyB7'
'W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdfSIpCgogICAgYnEgPSBzb3J0ZWQoe3QgZm9yIHQsIF8gaW4g'
'UlhfQk9fUVVBLmZpbmRhbGwob3V0X24pfSwga2V5PXNvX2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBicSkKICAgIGlubigiIik7'
'IGlubihmIiAgQk8gUVVBICh7bGVuKGJxKX0pOiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCiAgICBpbm4o'
'IiIpOyBpbm4oIiAgTjEtTjQgKHQxNjUtdDE2OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBuYXkgbGEgY2hpIGJh'
'byBob2kgcXV5OiIpCiAgICBiNCA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBTU9JfTsgZ2hpKCJjYV9tb2ki'
'LCBiNCkKICAgIGZvciB0IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCiAgICAjIEJPX1FVQS92YW5nIGxh'
'IENIVUEgQ0hBWSwga2hvbmcgcGhhaSBETzogY2hpIG1vdCBjYSBETyBtb2kgZHVvYyBwaGF0IFRSVU9ULgogICAga2V0KCJO'
'MS1ONCAodDE2NS10MTY4KSIsIERBVCBpZiBhbGwodiA9PSAiUVVBIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkKICAgICAgICBl'
'bHNlIChUUlVPVCBpZiBhbnkodiA9PSAiRE8iIGZvciB2IGluIGI0LnZhbHVlcygpKSBlbHNlIEtERCksIHN0cihiNCkpCgog'
'ICAgaW5uKCIiKTsgaW5uKCIgIDE1IGNhIHR1bmcgZG8gdHJlbiBDSToiKQogICAgYjE1ID0ge3Q6IG1hdV9jYShvdXRfbiwg'
'dCkgZm9yIHQgaW4gQ0ExNX07IGdoaSgiY2ExNSIsIGIxNSkKICAgIGlubigiICAgICIgKyAiICAiLmpvaW4oZiJ7dH06e2Ix'
'NVt0XX0iIGZvciB0IGluIENBMTUpKQoKICAgICMgdDEzNiDigJQgTjEyIGRvIEdJQU4gVElFUCBxdWEga2V0IHF1YSBjYQog'
'ICAgdDEzNl90ZW4gPSBuZXh0KCh0IGZvciB0IGluIGRvX2hldCBpZiB0LnN0YXJ0c3dpdGgoInQxMzYiKSksIE5vbmUpCiAg'
'ICBpZiBiMTUuZ2V0KCJ0MTM2IikgPT0gIlFVQSI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwg'
'REFULCAidDEzNiBRVUEiKQogICAgZWxpZiBiMTUuZ2V0KCJ0MTM2IikgIT0gIkRPIjoKICAgICAgICBrZXQoIk4xMiB0MTM2'
'IChxdWEga2V0IHF1YSBjYSkiLCBLREQsIGYidDEzNiA9IHtiMTUuZ2V0KCd0MTM2Jykhcn0g4oCUIGtob25nIGNoYXkva2hv'
'bmcgdGhheSIpCiAgICBlbHNlOgogICAgICAgIGx5ID0gZG9faGV0LmdldCh0MTM2X3RlbiwgIiIpCiAgICAgICAga2V0KCJO'
'MTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgVFJVT1QsIGYiRE86IHtseVs6OTBdfSIpCgojIC0tLS0tLS0tLS0tLS0tLS0g'
'My4gcHJvYmUgVEhBTkcgdmFvIGhhbSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMy4g'
'UFJPQkUgVEhBTkcg4oCUIGdvaSBfZ2l0X3dpbmRvd3Mgdm9pIHRoYW0gc28gdGllbSIpCnNwZWMgPSBpbXBvcnRsaWIudXRp'
'bC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHA1NDEiLCBzdHIodGVwKSkKbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVf'
'ZnJvbV9zcGVjKHNwZWMpOyBzcGVjLmxvYWRlci5leGVjX21vZHVsZShscCkKc2lnID0gaW5zcGVjdC5zaWduYXR1cmUobHAu'
'X2dpdF93aW5kb3dzKQpnaGkoInRoYW1fc29fX2dpdF93aW5kb3dzIiwgbGlzdChzaWcucGFyYW1ldGVycykpCmlubigiICB0'
'aGFtIHNvIGN1YSBfZ2l0X3dpbmRvd3M6IiwgbGlzdChzaWcucGFyYW1ldGVycykpCgpkZWYgZ29pKCoqa3cpOgogICAgIiIi'
'R29pIF9naXRfd2luZG93cywgQkFUIHN0ZGVyciBkZSBtb3QgZG9uZyBjaGFuIGRvYW4ga2hvbmcgZ2lldCBsdW90IGRvLiIi'
'IgogICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAg'
'ciA9IGxwLl9naXRfd2luZG93cygqKmt3KQogICAgcmV0dXJuIHIsIGUuZ2V0dmFsdWUoKQoKIyAtLS0gZG9pIGNodW5nIHJp'
'ZzogcGhhaSB0cmEgbG9pIGR1bmcgbW90IGNhIHRhIEJJRVQgVFJVT0MgZGFwIGFuIC0tLQp3aXRoIHRlbXBmaWxlLlRlbXBv'
'cmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICBuZ29haSA9IFBhdGgodCkvIm5nb2FpIjsgbmdvYWkubWtkaXIoKTsgY3cgPSBQ'
'YXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgKG5nb2FpLyJnaXQu'
'ZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMSwgXyA9IGdvaShwYXRoPXN0cihuZ29haSks'
'IHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAoY3cvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4Iiwg'
'ZW5jb2Rpbmc9InV0Zi04IikKICAgIHIyLCBfID0gZ29pKHBhdGg9c3RyKGN3KSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBj'
'd2Q9c3RyKGN3KSkKcmlnX29rID0gYm9vbChyMSkgYW5kIHIyIGlzIE5vbmUKZ2hpKCJyaWdfZG9pX2NodW5nIiwgcmlnX29r'
'KQprZXQoIlJJRyBkb2kgY2h1bmcgKGJpZXQgdHJ1b2MgZGFwIGFuKSIsIERBVCBpZiByaWdfb2sgZWxzZSBLREQsCiAgICBm'
'Im5nb2FpLWN3ZC0+eydOSEFOJyBpZiByMSBlbHNlICdOb25lJ30gfCB0cm9uZy1jd2QtPnsnTkhBTicgaWYgcjIgZWxzZSAn'
'Tm9uZSd9IikKaWYgbm90IHJpZ19vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogcmlnIHNhaSwgbW9pIGNo'
'b3QgZHVvaSBzZSB2byBuZ2hpYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tIE1PSSBDT05HIFBIQUkgVFUgQ0hVTkcgTUlOSCBO'
'TyBDTyBUSEUgRE8gLS0tCiMgQmFpIGhvYyBkYXQgbmhhdCBjdWEgcGFja2V0IG5heTogZG9fbjEwIGJhbiBjdSBjaGFtIERB'
'VCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEKIyBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1bmcga2h1eWV0IHRh'
'dCBtYSBOMTAgc2luaCByYSBkZSBiYXQuIE5vIGRlZ2VuZXJhdGUg4oCUCiMgdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEg'
'bGEgJzsnIG5lbiAidGFjaCBkdW5nIiB2YSAidGFjaCBzYWkiIGNobyBjdW5nIGtldCBxdWEuCiMgTW90IGNvbmcga2hvbmcg'
'dGhlIERPIHRoaSBraG9uZyBwaGFpIGNvbmcsIHZhIG5vIG5ndXkgaGllbSBob24ga2hvbmcgY28gY29uZzogbm8KIyBwaGF0'
'IHJhIG1vdCBjaHUgREFULgojCiMgTmVuIHRydW9jIGtoaSBEVU5HIG5hbSBjb25nIG5heSBkZSBwaGFuIHF1eWV0LCBiYXQg'
'dHVuZyBjb25nIGdpZXQgbW90IGRvdCBiaWVuIGRhCiMgYmlldCB0cm9uZy4gQ29uZyBuYW8ga2hvbmcgZ2lldCBkdW9jIHRo'
'aSBjaHUgREFUIGN1YSBubyBiaSBIQSB4dW9uZyBLSE9ORyBETyBEVU9DOwojIFRSVU9UIGdpdSBuZ3V5ZW4gKHF1YW4gc2F0'
'IHRydWMgdGllcCwgdmQuIGcxIHZhbiBuaGFuIGdpdC5iYXQpLiBEb3QgYmllbiBjaGF5IHRyZW4gQkFOIFNBTyBUQU07IGNh'
'eSB0aGF0IGtob25nIGJpCiMgZHVuZyB0b2kgKGN1bmcga3kgbHVhdCBuaHUgTjcpLgpET1RfQklFTl9UVV9LSUVNID0gWwog'
'ICAgKCJOOCIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgJ2lmIGNoaV9kaW5oIGFuZCBQYXRoKGNoaV9kaW5oKS5u'
'YW1lLmxvd2VyKCkgPT0gImdpdC5leGUiIGFuZCBob3BfbGUoY2hpX2RpbmgpOicsCiAgICAgImlmIGNoaV9kaW5oIGFuZCBo'
'b3BfbGUoY2hpX2RpbmgpOiIpLAogICAgKCJOOSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgImQgPSBkX3Jhdy5z'
'dHJpcCgpLnN0cmlwKCdcIicpIiwgImQgPSBkX3Jhdy5zdHJpcCgpIiksCiAgICAoIk4xMCIsICJvcHMvbGVhc2VfcHVibGlz'
'aC5weSIsCiAgICAgInNlcCA9IG9zLnBhdGhzZXAgaWYgcGhhbl9jYWNoIGlzIE5vbmUgZWxzZSBwaGFuX2NhY2giLCAic2Vw'
'ID0gb3MucGF0aHNlcCIpLAogICAgKCJOMTEiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAiaWYgY2hhbl9kb2FuIGlzIG5v'
'dCBOb25lOiIsICJpZiBGYWxzZToiKSwKICAgICgiTjEyIiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiLAogICAgICdn'
'aXRfcGF0aD0iLy9raG9uZy1jby9naXQiJywgJ2dpdF9wYXRoPSIva2hvbmctY28vZ2l0IicpLApdCmlubigiIik7IGlubigi'
'ICB0dSBraWVtIGNvbmcg4oCUIG1vaSBjb25nIHBoYWkgZ2lldCBkdW9jIG1vdCBkb3QgYmllbiBkYSBiaWV0OiIpCmdpZXQg'
'PSB7fQpmb3IgbWEsIGR1b25nLCB0aW0sIHRoYXkgaW4gRE9UX0JJRU5fVFVfS0lFTToKICAgIF90ZW4sIF9oYW0gPSBuZXh0'
'KCgoYSwgYikgZm9yIGEsIGIgaW4gUFJPQkUgaWYgYS5zdGFydHN3aXRoKG1hICsgIiAiKSksIChOb25lLCBOb25lKSkKICAg'
'IGlmIF9oYW0gaXMgTm9uZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVP'
'Qzoga2hvbmcgdGltIHRoYXkgcHJvYmUgdGVuICd7bWF9IC4uLiciKTsgY29udGludWUKICAgIHRyeToKICAgICAgICB3aXRo'
'IHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIF90OgogICAgICAgICAgICBfYyA9IFBhdGgoX3QpLyJjYXkiOyBz'
'aHV0aWwuY29weXRyZWUoZ29jLyJvcHMiLCBfYy8ib3BzIikKICAgICAgICAgICAgX2YgPSBfYy9kdW9uZzsgX25kID0gX2Yu'
'cmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIGlmIF9uZC5jb3VudCh0aW0pICE9IDE6CiAgICAgICAg'
'ICAgICAgICBnaWV0W21hXSA9IE5vbmUKICAgICAgICAgICAgICAgIGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzog'
'bWF1IGRvdCBiaWVuIGtob3Age19uZC5jb3VudCh0aW0pfSBsYW4gKG1vbmcgMSkiCiAgICAgICAgICAgICAgICAgICAgZiIg'
'4oCUIG1hIG5ndW9uIGRhIGRvaSwgZG90IGJpZW4gbmF5IGhldCB5IG5naGlhIik7IGNvbnRpbnVlCiAgICAgICAgICAgIF9m'
'LndyaXRlX3RleHQoX25kLnJlcGxhY2UodGltLCB0aGF5LCAxKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgX3Nw'
'ID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX2RiXyIgKyBtYSwgc3RyKF9jLyJvcHMiLyJs'
'ZWFzZV9wdWJsaXNoLnB5IikpCiAgICAgICAgICAgIF9tID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3Ap'
'OyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9tKQogICAgICAgICAgICBkZWYgX2dvaV9kYigqKmt3KToKICAgICAgICAgICAg'
'ICAgIF9lID0gaW8uU3RyaW5nSU8oKQogICAgICAgICAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihf'
'ZSk6CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIF9tLl9naXRfd2luZG93cygqKmt3KSwgX2UuZ2V0dmFsdWUoKQogICAg'
'ICAgICAgICBfdHQsIF9jdCwgXyA9IF9oYW0oX2dvaV9kYiwgaW5zcGVjdC5zaWduYXR1cmUoX20uX2dpdF93aW5kb3dzKSwK'
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAg'
'IGdpZXRbbWFdID0gKF90dCA9PSBUUlVPVCkKICAgICAgICBpbm4oZiIgICAge21hOjR9IGRvdCBiaWVuIC0+IHtfdHQ6MTR9'
'IHsnR0lFVCBEVU9DJyBpZiBfdHQgPT0gVFJVT1QgZWxzZSAnU09ORyBTT1QnfSIKICAgICAgICAgICAgKyAoZiIgICAoe19j'
'dH0pIiBpZiBfY3QgZWxzZSAiIikpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAgICAgIGdpZXRbbWFdID0gTm9u'
'ZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiB7dHlwZShfZSkuX19uYW1lX199OiB7X2V9IikKZ2hpKCJjb25n'
'X2dpZXRfZHVvY19kb3RfYmllbiIsIGdpZXQpCgpmb3IgdGVuLCAodHQsIGN0LCBkbCkgaW4gWyh0LCBmKGdvaSwgc2lnLCB0'
'ZXB0KSkgZm9yIHQsIGYgaW4gUFJPQkVdOgogICAgZ2hpKCJwcm9iZV8iICsgdGVuLnNwbGl0KClbMF0ubG93ZXIoKSwgZGwp'
'CiAgICBpZiBpc2luc3RhbmNlKGRsLCBkaWN0KToKICAgICAgICBmb3IgaywgdiBpbiBkbC5pdGVtcygpOiBpbm4oZiIgICAg'
'e2s6MzR9OiB7dn0iKQogICAgbWEgPSB0ZW4uc3BsaXQoKVswXQogICAgaWYgZ2lldC5nZXQobWEpIGlzIG5vdCBUcnVlIGFu'
'ZCB0dCA9PSBEQVQ6CiAgICAgICAgIyBEQVQgdHUgbW90IGNvbmcgY2h1YSBjaHVuZyBtaW5oIGR1b2MgbGEgYmlldCBETyB0'
'aGkga2hvbmcgZGFuZyB0aW4gaG9uIEtERC4KICAgICAgICBrZXQodGVuLCBLREQsIGYiY29uZyBLSE9ORyBnaWV0IGR1b2Mg'
'ZG90IGJpZW4gY3VhIGNoaW5oIG5vICh7Z2lldC5nZXQobWEpIXJ9KSIKICAgICAgICAgICAgICAgICAgICAgIGYiIC0+IGNo'
'dSBEQVQgbmF5IGtob25nIGNvIGdpYSB0cmkiKQogICAgZWxzZToKICAgICAgICBrZXQodGVuLCB0dCwgY3QpCgojIC0tLS0t'
'LS0tLS0tLS0tLS0gNC4gTjcgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElf'
'UFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjQuIE43IOKAlCBkb3QgYmllbiB0cmVuIEJBTiBTQU8g'
'VEFNIChjYXkgdGhhdCBLSE9ORyBiaSBkdW5nIHRvaSkiKQogICAgdHJ1b2MgPSB0ZXAucmVhZF90ZXh0KGVuY29kaW5nPSJ1'
'dGYtOCIpLmNvdW50KE1BVV9XSU4pCiAgICBnaGkoIm43X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIgIHNvIGRvbmcga2hvcCB7'
'TUFVX1dJTiFyfTogVFJVT0MgPSB7dHJ1b2N9IFttb25nIDFdIikKICAgIGlmIHRydW9jICE9IDE6CiAgICAgICAga2V0KCJO'
'NyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCBmIm1hdSB4dWF0IGhpZW4ge3RydW9jfSBsYW4sIGtob25nIHBoYWkg'
'MSIpCiAgICBlbHNlOgogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdG1wOgogICAgICAg'
'ICAgICBzYW8gPSBQYXRoKHRtcCkvImNheSIKICAgICAgICAgICAgc2h1dGlsLmNvcHl0cmVlKGdvYywgc2FvLCBpZ25vcmU9'
'c2h1dGlsLmlnbm9yZV9wYXR0ZXJucygiLmdpdCIsICJfX3B5Y2FjaGVfXyIsICIqLnB5YyIpKQogICAgICAgICAgICBmMiA9'
'IHNhby8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIKICAgICAgICAgICAgZjIud3JpdGVfdGV4dChmMi5yZWFkX3RleHQoZW5j'
'b2Rpbmc9InV0Zi04IikucmVwbGFjZShNQVVfV0lOLCAiaWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAg'
'ICAgIHNhdSA9IGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKTsgZ2hpKCJuN19zYXUiLCBz'
'YXUpCiAgICAgICAgICAgIGlubihmIiAgU0FVIChkYSBkb3QgYmllbikgPSB7c2F1fSBbbW9uZyAwXSIpCiAgICAgICAgICAg'
'IGlmIHNhdSAhPSAwOgogICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCAiZG90'
'IGJpZW4gS0hPTkcgYXAgZHVvYyIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICByY19tLCBvdXRfbSA9IGNo'
'YXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIHNhbykKICAgICAgICAgICAgICAgIG0xNjUgPSBtYXVfY2Eob3V0'
'X20sICJ0MTY1Iik7IGRtLCBfLCBfID0gZG9jX2RvKG91dF9tKQogICAgICAgICAgICAgICAgdGVuMTY1ID0gbmV4dCgodCBm'
'b3IgdCBpbiBkbSBpZiB0LnN0YXJ0c3dpdGgoInQxNjUiKSksIE5vbmUpCiAgICAgICAgICAgICAgICBseSA9IChkbS5nZXQo'
'dGVuMTY1KSBvciAiIikKICAgICAgICAgICAgICAgIGdoaSgibjdfdDE2NSIsIG0xNjUpOyBnaGkoIm43X2x5X2RvIiwgbHlb'
'OjIwMF0pCiAgICAgICAgICAgICAgICBpbm4oZiIgIHQxNjUgc2F1IGRvdCBiaWVuOiB7bTE2NX0gfCB7bHlbOjExMF19IikK'
'ICAgICAgICAgICAgICAgIGR1bmdfbHlfZG8gPSAiUEFUSCB0IiBpbiBseSBvciAiL3Vzci9iaW4iIGluIGx5CiAgICAgICAg'
'ICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBEQVQgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19s'
'eV9kbykgZWxzZQogICAgICAgICAgICAgICAgICAgIChUUlVPVCBpZiBtMTY1ID09ICJETyIgZWxzZSBLREQpLAogICAgICAg'
'ICAgICAgICAgICAgICJnaWV0IGR1bmcgbHkgZG8iIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pCiAgICAgICAg'
'ICAgICAgICAgICAgZWxzZSAoIkRPIG5odW5nIEtIT05HIGR1bmcgbHkgZG8gLT4gdGluIGR1bmcgZ2lhIiBpZiBtMTY1ID09'
'ICJETyIgZWxzZSAia2hvbmcgZG9jIGR1b2MgdDE2NSIpKQoKIyAtLS0tLS0tLS0tLS0tLS0tIEtFVCBMVUFOIC0tLS0tLS0t'
'LS0tLS0tLS0KaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQppbm4oZiJUSEUgSEUgRE8gRFVPQzoge3RoZV9oZX0gICBIRUFEPXto'
'ZWFkWzoxMl19IikKIyBLaG9pIGRhbiBjaG8gcmV2aWV3ZXIgYmF0IGRhdSBvIGRvbmcgdHJlbiwgbmVuIENIRSBETyBwaGFp'
'IG5hbSBOR0FZIGR1b2kgbm86IGtob25nIGNvIGRvbmcgbmF5CiMgdGhpIG1vdCBsdW90IC0tY2hpLXByb2JlIGluICJEQVQg'
'NyB8IFRSVU9UIDAgfCBLSE9ORyBETyBEVU9DIDAiIHJjPTAgbWEga2hvbmcgbm9pIGxhIGNodWEgY2hheSBibyB0ZXN0Lgpn'
'aGkoImNoZV9kbyIsICJjaGktcHJvYmUiIGlmIENISV9QUk9CRSBlbHNlICJkYXktZHUiKQppZiBDSElfUFJPQkU6CiAgICBp'
'bm4oIi0tY2hpLXByb2JlOiBDSEkgZG8gbXVjIDAsIDEsIDMuIEJvIHRlc3QsIE4xLU40LCB0MTM2LCBONyBLSE9ORyBjaGF5'
'IC0gZGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQppZiB0aGVfaGUgPT0gImcxIjoKICAgIGlubigiTFVV'
'IFk6IGRheSBsYSBORU4gRE8gKGcxKSwgS0hPTkcgcGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hvdCBOOC1OMTIgZHVvaSBk'
'YXkiKQogICAgaW5uKCIgICAgICAgVFJVT1QgbGEgRFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEgbmh1bmcgbG8gZzIgc2lu'
'aCByYSBkZSB2w6EuIikKaW5uKCItIiAqIDc4KQpmb3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAgIGlubihmIiAge3R0OjE0'
'fSB7dGVufSIgKyAoZiIgICB7Y3R9IiBpZiBjdCBlbHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90'
'IGlmIHQgPT0gS0REKQpuX3RydW90ID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQppbm4oIi0i'
'ICogNzgpCmlubihmIiAgREFUIHtzdW0oMSBmb3IgXyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8IFRSVU9UIHtuX3RydW90'
'fSB8IEtIT05HIERPIERVT0Mge25fa2RkfSIpCmlubihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgnc29fY2FfZG8nKX0gfCBk'
'YW5oIHNhY2ggZGF5IGR1OiB7J0NPJyBpZiBzby5nZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAnS0hPTkcgRE8gRFVPQyd9'
'IikKaW5uKGYiICBBZG1pbmlzdHJhdG9yOiB7c28uZ2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxpbms6IHtzby5nZXQoJ3N5'
'bWxpbmtfZHVvYycpfSIpCmlubigiIik7IGlubigiLS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5BWSBWRSBDSE8gUkVWSUVX'
'RVIgLS0tIikKZ2hpKCJjaG90IiwgW3sidGVuIjogYSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3RpZXQiOiBjfSBmb3IgYSwg'
'YiwgYyBpbiBjaG90XSkKaW5uKGpzb24uZHVtcHMoc28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50PTEsIGRlZmF1bHQ9'
'c3RyKSkKIyByYzogMCA9IG1vaSBjaG90IERBVCB8IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNvIGNob3QgS0hPTkcgRE8g'
'RFVPQyAodXUgdGllbiBiYW8gZG9uZykKc3lzLmV4aXQoMyBpZiBuX2tkZCBlbHNlICgxIGlmIG5fdHJ1b3QgZWxzZSAwKSkK'
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
