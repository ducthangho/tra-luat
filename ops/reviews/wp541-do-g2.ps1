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
$ShaBoDo    = 'b4276653664ae63c184b6a57878252bf2b0d7f4cc547639ea38ee25d3c7dfb98'      # SHA-256 cua bo do Python nhung ben duoi

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
'Yjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5fQk9fRE8gPSAiMjAyNi0wOS0zMG0iICAgICAgICAgICAgICAj'
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
'MyBUSEFUIHF1YSBwcm9iZQojIGN1IChyYz0wKSwgYm8gdGVzdCAxMDkvMTY2ICg1NiBjYSAibGEiIGB1bmV4cGVjdGVkIGtl'
'eXdvcmQgYXJndW1lbnQgJ3NvcnRfa2V5cydgKSwgZTJlIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgOyBQeVlBTUwgNS4xOiAx'
'NjYvMTY2LgojIChQeXRob24gPj0gMy4xMCArIFB5WUFNTCAzLjEzIGRhIHRydW90IHByb2JlIGN1IHZpIGBjb2xsZWN0aW9u'
'cy5IYXNoYWJsZWAuKSBQcm9iZSBjdWEgcHMxICgkbWFUaHUpIHBoYWkgR0lPTkcgSEVUIGRvbmcgZHVvaS4KaWYgbm90ICgi'
'LS1jaGkta2ljaC10aHVvYyIgaW4gc3lzLmFyZ3Ygb3IgIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndik6CiAgICBfcmNfZGss'
'IF9yYV9kayA9IGNoYXkoWyItYyIsICJpbXBvcnQgc3lzOyBzeXMuZXhpdCg5KSBpZiBzeXMudmVyc2lvbl9pbmZvIDwgKDMs'
'IDkpIGVsc2UgTm9uZTsgaW1wb3J0IHlhbWw7IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiIHlhbWwuc2Fm'
'ZV9kdW1wKHlhbWwuc2FmZV9sb2FkKCdhOiAxJyksIGFsbG93X3VuaWNvZGU9VHJ1ZSwgc29ydF9rZXlzPUZhbHNlKSJdLAog'
'ICAgICAgICAgICAgICAgICAgICAgICAgIGdvYyAvICJvcHMiIGlmIChnb2MgLyAib3BzIikuaXNfZGlyKCkgZWxzZSBQYXRo'
'LmN3ZCgpLCBwaHV0PTIpCiAgICBpZiBfcmNfZGsgPT0gOToKICAgICAgICBsb2kuYXBwZW5kKGYicHl0aG9uIHtzeXMudmVy'
'c2lvbi5zcGxpdCgpWzBdfSA8IDMuOTogYm8gdGVzdCBjdWEgdW5nIHZpZW4gZHVuZyBzdHIucmVtb3ZlcHJlZml4ICgzLjkp'
'IGx1YyBDSEFZIikKICAgIGVsaWYgX3JjX2RrOgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24gbmF5IEtIT05HIGNvIFB5'
'WUFNTCBkdW5nIGR1b2MgKHsoX3JhX2RrLnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10pWy0xXVs6OTBdfSk6IgogICAg'
'ICAgICAgICAgICAgICAgZiIgXCJ7c3lzLmV4ZWN1dGFibGV9XCIgLW0gcGlwIGluc3RhbGwgLVUgcHl5YW1sIgogICAgICAg'
'ICAgICAgICAgICAgIiAoYmFuIG5odW5nIHBzMSB0dSB0YWkgS0hPTkcgY28gcGlwOiBjaGF5IGxhaSB2b2kgLVB5IDxweXRo'
'b24gZGEgY28gUHlZQU1MPikiKQogICAgIyBCbyB0ZXN0IGNvbiBnb2kgYHNodXRpbC53aGljaGAgY2hvIGJhc2gvYWN0aW9u'
'bGludC9zaGVsbGNoZWNrICgwZWE5NWRlOiB0MzMgdDEzNyB0MTU5IGNhbiBhY3Rpb25saW50LCB0MTM3IGNhbgogICAgIyBz'
'aGVsbGNoZWNrLCBjYWMgY2EgY2hheSBvcHMvY2FpX2FjdGlvbmxpbnQuc2ggY2FuIGJhc2gpLiBUaGlldSB0aGkgY2FjIGNh'
'IGF5IGluICJLSE9ORyBETyBEVU9DOiB0aGlldSBgLi4uYCIgdmEgYm8gZG8gcmEKICAgICMgcmM9MyDigJQgbmh1bmcgY2hp'
'IFNBVSBjYSBibyB0ZXN0IGxhbiBONyAoZG8gdHJlbiAyMDI2LTA5LTMwZywgUEFUSCB0aGlldSBhY3Rpb25saW50OiBgQ29u'
'ZyBjdSBkYXkgZHUgZGUgZG9gIEtERCwgcmM9MwogICAgIyBzYXUgMiBsdW90IGJvIHRlc3QpLiBDdW5nIGx5IGRvIFB5WUFN'
'TCBkdW9jIGhvaSBvIGRheTogaG9pIFRSVU9DLCBjdW5nIFBBVEggbWEgY2hheSgpIHRydXllbiBjaG8gYm8gdGVzdC4KICAg'
'ICMgVkEgY3VuZyBDSE8gYm8gdGVzdCBkdW5nOiB0cmVuIFdpbmRvd3MgYHNodXRpbC53aGljaGAgdHJhIFRIVSBNVUMgSElF'
'TiBIQU5IIFRSVU9DIFBBVEgsIG1hIGJvIHRlc3QgY2hheSB2b2kgY3dkID0gZ29jIGNvbgogICAgIyB0aWVuIHRyaW5oIG5h'
'eSBkdW5nIG8gY3dkIENVQSBOR1VPSSBETyAobm9pIGdvaSBwczEsIHZkLiBEb3dubG9hZHMg4oCUIGR1bmcgbm9pIGdpYWkg'
'bmVuIGFjdGlvbmxpbnQuZXhlKS4gRG8gdHJlbiAyMDI2LTA5LTMwawogICAgIyAobmhhbmggd2luMzIgVEhBVCBjdWEgc2h1'
'dGlsLndoaWNoKTogYWN0aW9ubGludCB0b3QgbyBjd2Qgbmd1b2kgZG8gKyBiYW4gaG9uZyBkYXUgUEFUSCA9PiBtdWMgMCBo'
'b2kgYmFuIG8gY3dkIChyYz0wKSwgYm8gdGVzdAogICAgIyBkdW5nIGJhbiB0cmVuIFBBVEggPT4gcmM9MSBgREFUIDExIHwg'
'VFJVT1QgMWAsIGBsYTogWyd0MzMnLCAndDEzNycsICd0MTU5J11gLiBHaWFpIHRlbiB2b2kgY3dkID0gZ29jIHJvaSBnb2kg'
'VEhBTkcgYmFuZyBkdW9uZwogICAgIyBUVVlFVCBET0kgZGEgZ2lhaSAocXVhIGhhbiB0aGkgcnVuKCkgZ2lldCBkdW5nIHRp'
'ZW4gdHJpbmgg4oCUIGx5IGRvIGJhbiAzMGkga2hvbmcgaG9pIHF1YSBjaGF5KCkpLgogICAgX2N3ZF9uZ3VvaV9kbyA9IG9z'
'LmdldGN3ZCgpCiAgICB0cnk6CiAgICAgICAgaWYgZ29jLmlzX2RpcigpOiBvcy5jaGRpcihnb2MpCiAgICAgICAgX2NjID0g'
'e2M6IChvcy5wYXRoLmFic3BhdGgocCkgaWYgcCBlbHNlIE5vbmUpIGZvciBjLCBwIGluCiAgICAgICAgICAgICAgICgoYywg'
'c2h1dGlsLndoaWNoKGMpKSBmb3IgYyBpbiAoImJhc2giLCAiYWN0aW9ubGludCIsICJzaGVsbGNoZWNrIiwgImdpdCIpKX0K'
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
'QSB0cmVuIDBlYTk1ZGUuCiAgICAjIGJhc2ggQ0hJIGhvaSBDTyBNQVQsIGNvIGNodSBkaWNoOiBiYXNoIFdTTCAoU3lzdGVt'
'MzIpIGxhbSB0MzUtdDQwIERPIG5odW5nIGNhIHNhdSBkZXUgTkdPQUlfUEhBTV9WSSwgY29uIHQzMi90MTUyIHR1IGNob24K'
'ICAgICMgR2l0IEJhc2ggKF9iYXNoX3Bvc2l4IGN1YSB1bmcgdmllbikg4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGo6IGJhc2gg'
'a2lldSBXU0wgPT4gdDM1LXQ0MCBETywgZGV1IHJvaSB2YW8gbmdvYWkgcGhhbSB2aS4KICAgICMgQ0hBWSBEVU9DIGNodWEg'
'cGhhaSBEVU5HIERVT0M6IGRvIHRyZW4gMjAyNi0wOS0zMGssIDBlYTk1ZGUsIGFjdGlvbmxpbnQgVEhBVCAxLjQuMy8xLjUu'
'MC8xLjUuMy8xLjYuMC8xLjYuOC8xLjYuMTUvMS42LjIwLwogICAgIyAxLjYuMjIgZGV1IGAtdmVyc2lvbmAgcmM9MCwgbWEg'
'Y2EgdGFtIGxhbSB0MTM3L3QxNTkgRE8gKGBwcm9wZXJ0eSAicnVuX2F0dGVtcHQiLyJ3b3JrZmxvd19zaGEiIGlzIG5vdCBk'
'ZWZpbmVkYCksIDEuNC4zLzEuNS4wCiAgICAjIHRoZW0gdDMzIChgbXVzdCBiZSBjb250YWluZWQgd2l0aGluICR7eyB9fWAp'
'IOKAlCBlMmUgMS42LjIyOiByYz0xIGBEQVQgMTEgfCBUUlVPVCAxYCwgYGxhOiBbJ3QxMzcnLCAndDE1OSddYCBjaG8gdW5n'
'IHZpZW4KICAgICMgc2FjaDsgMS42LjIzLzEuNi4yNC8xLjYuMjYvMS42LjI3LzEuNy4wLzEuNy42LzEuNy43LzEuNy4xMiBR'
'VUEgY2EgYmEuIFNhbiBsYSBiYW4KICAgICMgZ2hpbSBDSSAoQUxfU0FOKSwgS0hPTkcgcGhhaSAxLjYuMjMgZG8gdHJlbiBN'
'T1QgdW5nIHZpZW46IHdvcmtmbG93IGN1YSB1bmcgdmllbiBzYXUgY28gdGhlIGR1bmcgY3UgcGhhcCBtb2kgaG9uLCBtYSBD'
'SSBjaGkgZG8KICAgICMgYmFuZyBiYW4gZ2hpbS4gQ3UgaG9uIHNhbiA9PiBLSE9ORyBETyBEVU9DIChjaGFuIGNhIDEuNi4y'
'My0xLjcuNiBkYW5nIFFVQTogZmFpbC1jbG9zZSwga2hvbmcgcGhhaSBwaGFuIHF1eWV0KS4gYHZgIGRhdTogYmFuCiAgICAj'
'IGBnbyBpbnN0YWxsYCBpbiBgdjEuNy43YDsga2hvbmcgZG9jIGR1b2Mgc28gKHZkLiBgKGRldmVsKWApID0+IEtIT05HIERP'
'IERVT0MuCiAgICBpZiBub3QgX3RoaWV1X2NjOgogICAgICAgIF9hbCA9IHN1YnByb2Nlc3MucnVuKFtfY2NbImFjdGlvbmxp'
'bnQiXSwgIi12ZXJzaW9uIl0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwKICAg'
'ICAgICAgICAgICAgICAgICAgICAgICAgICBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PTYwKQogICAgICAgIF9hbF92ID0g'
'cmUuc2VhcmNoKHIiKD9tKV52PyhcZCspXC4oXGQrKVwuKFxkKykiLCBfYWwuc3Rkb3V0IG9yICIiKQogICAgICAgIGlmIF9h'
'bC5yZXR1cm5jb2RlOgogICAgICAgICAgICBsb2kuYXBwZW5kKCJhY3Rpb25saW50IHRyZW4gUEFUSCBjbyBtYXQgbmh1bmcg'
'YGFjdGlvbmxpbnQgLXZlcnNpb25gIHJjIT0wIChraG9uZyBjaGF5IGR1b2MpOiBjYWkgbGFpIGJhbiBnaGltIEFMX1ZFUiIp'
'CiAgICAgICAgZWxpZiBub3QgX2FsX3Ygb3IgdHVwbGUoaW50KHgpIGZvciB4IGluIF9hbF92Lmdyb3VwcygpKSA8IEFMX1NB'
'TjoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImFjdGlvbmxpbnQge19hbF92Lmdyb3VwKDApIGlmIF9hbF92IGVsc2UgJyhr'
'aG9uZyBkb2MgZHVvYyBwaGllbiBiYW4pJ30gY3UgaG9uIGJhbiBnaGltIENJICIKICAgICAgICAgICAgICAgICAgICAgICBm'
'InsnLicuam9pbihtYXAoc3RyLCBBTF9TQU4pKX0gKEFMX1ZFUik6IGJhbiBjdSBsYW0gdDEzNy90MTU5IERPICdsYScgdHJl'
'biB1bmcgdmllbiBzYWNoIOKAlCIKICAgICAgICAgICAgICAgICAgICAgICAiIGNhaSBiYW4gZ2hpbSAob3BzL2NhaV9hY3Rp'
'b25saW50LnNoIHZvaSBBTF9WRVIpIikKICAgICAgICAjIGdpdCBjdW5nIHRoZTogQ08gTUFUIGtob25nIHBoYWkgRFVORyBE'
'VU9DLCB2YSBnaXQgQ1UgbGEgY29uZyBjdSBQSE8gQklFTiBuaGF0IHRyb25nIGJvbi4gRG8gdHJlbiAyMDI2LTA5LTMwbCwg'
'MGVhOTVkZSwgZ2l0CiAgICAgICAgIyBUSEFUIHF1YSBjdW5nIGNoYXkoKTogMi4yNS4xID0+IDE0MC8xNjYgKDIzIGNhICJs'
'YSI6IGBpbml0IC1iYC4uLiksIDIuMzQuMSB2YSAyLjM1LjEgPT4gMTYzLzE2NiAodDEwOSB0MTEwIHQxMTE6IGBnaXQKICAg'
'ICAgICAjIHdvcmt0cmVlIGxpc3QgLS1wb3JjZWxhaW4gLXpgIHJjPTEyOSBgdW5rbm93biBzd2l0Y2ggemApLCBlMmUgMi4z'
'NS4xIHJjPTEgYERBVCAxMSB8IFRSVU9UIDFgOyAyLjM2LjEgPT4gMTY2LzE2Ni4gU2FuIGxheQogICAgICAgICMgdHUgdGlu'
'aCBuYW5nIG1hIENISU5IIG1hIGR1b2MgZG8gZ29pIChvcHMvY29uZ19jdS55YW1sIGRlIGJhbl9naGltIGdpdCA9IG51bGwg'
'bmVuIGtob25nIGNvIGJhbiBnaGltIENJIGRlIGR1YSB2YW8pLgogICAgICAgICMgYGdpdCB2ZXJzaW9uIDIuNDcuMS53aW5k'
'b3dzLjFgIChHaXQgZm9yIFdpbmRvd3MpIHZhIGAyLjM5LjMgKEFwcGxlIEdpdC0xNDYpYCBkZXUgZG9jIGR1b2MgYmEgc28g'
'ZGF1LgogICAgICAgIF9ndiA9IHN1YnByb2Nlc3MucnVuKFtfY2NbImdpdCJdLCAiLS12ZXJzaW9uIl0sIGNhcHR1cmVfb3V0'
'cHV0PVRydWUsIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICBlcnJv'
'cnM9InJlcGxhY2UiLCB0aW1lb3V0PTYwKQogICAgICAgIF9ndl9tID0gcmUuc2VhcmNoKHIiKD9tKV5naXQgdmVyc2lvblxz'
'KyhcZCspXC4oXGQrKVwuKFxkKykiLCBfZ3Yuc3Rkb3V0IG9yICIiKQogICAgICAgIGlmIF9ndi5yZXR1cm5jb2RlOgogICAg'
'ICAgICAgICBsb2kuYXBwZW5kKCJnaXQgdHJlbiBQQVRIIGNvIG1hdCBuaHVuZyBgZ2l0IC0tdmVyc2lvbmAgcmMhPTAgKGto'
'b25nIGNoYXkgZHVvYyk6IGNhaSBsYWkgZ2l0IikKICAgICAgICBlbGlmIG5vdCBfZ3ZfbSBvciB0dXBsZShpbnQoeCkgZm9y'
'IHggaW4gX2d2X20uZ3JvdXBzKCkpIDwgR0lUX1NBTjoKICAgICAgICAgICAgbG9pLmFwcGVuZChmImdpdCB7Jy4nLmpvaW4o'
'X2d2X20uZ3JvdXBzKCkpIGlmIF9ndl9tIGVsc2UgJyhraG9uZyBkb2MgZHVvYyBwaGllbiBiYW4pJ30gY3UgaG9uICIKICAg'
'ICAgICAgICAgICAgICAgICAgICBmInsnLicuam9pbihtYXAoc3RyLCBHSVRfU0FOKSl9ICh1bmcgdmllbiBnb2kgYGdpdCB3'
'b3JrdHJlZSBsaXN0IC0tcG9yY2VsYWluIC16YCk6IGNhcCBuaGF0IGdpdCIpCgpyYywgaGVhZCwgXyA9IGdpdChnb2MsICJy'
'ZXYtcGFyc2UiLCAiSEVBRCIpCmlmIHJjOiBsb2kuYXBwZW5kKCJraG9uZyBkb2MgZHVvYyBIRUFEIikKZ2hpKCJoZWFkIiwg'
'aGVhZCkKcmNfYSwgXywgXyA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIi0taXMtYW5jZXN0b3IiLCBTSEFfRzEsIGhlYWQg'
'b3IgIkhFQUQiKQpsYV9oYXVfZHVlID0gKHJjX2EgPT0gMCkKaWYgaGVhZCA9PSBTSEFfRzE6CiAgICB0aGVfaGUgPSAiZzEi'
'OyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IERBWSBMQSBnMS4gQ0hVQSBjbyBiYW4gdmEgZzI7IGtldCBxdWEgZHVv'
'aSBsYSBORU4gRE8uIikKZWxpZiBsYV9oYXVfZHVlOgogICAgdGhlX2hlID0gImcyIjsgaW5uKGYiICBIRUFEID0ge2hlYWRb'
'OjhdfSAtPiBoYXUgZHVlIGN1YSBnMSAoe1NIQV9HMVs6OF19KTsgdW5nIHZpZW4gZzIgaGF5IGtob25nOiBONycgKG11YyAx'
'KSBkaW5oIGRhbmguIikKZWxzZToKICAgIHRoZV9oZSA9ICI/IjsgbG9pLmFwcGVuZChmIkhFQUQ9e2hlYWRbOjhdfSBLSE9O'
'RyBwaGFpIGcxIHZhIEtIT05HIHBoYWkgaGF1IGR1ZSBjdWEge1NIQV9HMVs6OF19IOKAlCByZWJhc2U/IG5oYW0gbmhhbmg/'
'IikKZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCnJjX3IsIHJlZnMsIF8gPSBnaXQoZ29jLCAiZm9yLWVhY2gtcmVmIiwgIi0tcG9p'
'bnRzLWF0IiwgaGVhZCBvciAiSEVBRCIsCiAgICAgICAgICAgICAgICAgICAgIi0tZm9ybWF0PSUocmVmbmFtZTpzaG9ydCki'
'KQpkc3IgPSBbeCBmb3IgeCBpbiByZWZzLnNwbGl0bGluZXMoKSBpZiB4LnN0cmlwKCkgYW5kIHguc3RyaXAoKSAhPSAiZG8t'
'dGFtIl0KZ2hpKCJyZWZfdHJvX3RvaV9oZWFkIiwgZHNyKQppbm4oZiIgIHJlZiB0cm8gdG9pIEhFQUQ6IHsnLCAnLmpvaW4o'
'ZHNyKSBpZiBkc3IgZWxzZSAnKGtob25nIHJlZiBuYW8gLSBIRUFEIHJvaSB0dSBkbyknfSIpCgppZiBsb2k6CiAgICBpbm4o'
'IiIpOyBpbm4oIktIT05HIERPIERVT0M6IG5lbiBkbyBzYWksIEtIT05HIGluIGtldCBsdWFuIG5hby4iKQogICAgZm9yIHgg'
'aW4gbG9pOiBpbm4oIiAgLSIsIHgpCiAgICBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDEuIGtpY2ggdGh1b2Mg'
'KE43JyBjdWEgc3BlYyByMykgLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjEuIEtJQ0gg'
'VEhVT0Mg4oCUIHRyYW4gc3BlYyByMzogPD0gMiB0ZXAgdmEgPD0gNDAwIGRvbmcgdGhlbSIpCiMgVkUgTkVOIFBIQUkgVFVP'
'SSDigJQgdmEgcGhhaSBDSFVORyBNSU5IIGR1b2MgbGEgdHVvaSwga2hvbmcgcGhhaSBnaWEgZGluaC4KIyBCYWkgaG9jIHRy'
'YSBnaWEgMTktMDktMjAyNjogY2xvbmUgdGFpIGR1bmcgY2hpIGZldGNoIG5oYW5oIGJhbiB2YSwgYG9yaWdpbi9tYXN0ZXJg'
'CiMgZHVuZyB5ZW4gdHUgMTQtMDkgKGMxNmJkMzIsIHNhdSA5NyBjb21taXQpLiBtZXJnZS1iYXNlIHJvaSB2ZSBkdW5nIGRp'
'bmggbWFzdGVyIGN1LAojIG5lbiBkaWZmIE5VT1QgY2EgOTcgY29tbWl0IG1hc3RlcjogZG8gcmEgNDYgdGVwIC8gKzcxMTgg'
'dGhheSB2aSAyIHRlcCAvICszOTcg4oCUCiMgQ1VORyBNT1QgQ09NTUlUIDBlYTk1ZGUuIE1vdCB0aWV1IGNoaSBERUxUQSBt'
'YSB2ZSBuZW4ga2hvbmcgdHVvaSB0aGkga2hvbmcgc2FpCiMgbGVjaCBtb3QgY2h1dCwgbm8gc2FpIGNhIG1vdCBiYWMgZG8g'
'bG9uLgojIENobyBuZW46IG5lbiBraG9uZyBjaHVuZyBtaW5oIGR1b2MgbGEgdHVvaSA9PiBLSE9ORyBETyBEVU9DIChyYz0z'
'KSwgS0hPTkcgcGhhaSBUUlVPVC4KIyBUUlVPVCBsYSBtb3QgUEhBTiBRVVlFVCB2ZSBiYW4gdmE7IHBoYW4gcXV5ZXQgY2hp'
'IGR1b2MgcGhlcCBwaGF0IHJhIGtoaSBkYSBkbyBkdW9jLgplciA9ICIiCnJjX3UsIHVybF90aG8sIF8gPSBnaXQoZ29jLCAi'
'cmVtb3RlIiwgImdldC11cmwiLCAib3JpZ2luIikKdXJsX28sIHVybF9pbiA9IF91cmxfc2FjaCh1cmxfdGhvKSwgX3VybF9p'
'bih1cmxfdGhvKQpnaGkoIm9yaWdpbl91cmwiLCB1cmxfaW4pOyBpbm4oZiIgIG9yaWdpbiAgICAgICA6IHt1cmxfaW4gb3Ig'
'JyhraG9uZyBkb2MgZHVvYyknfSIpCnVybF9vayA9IChub3QgcmNfdSkgYW5kIHVybF9vLnJzdHJpcCgiLyIpIGluIFVSTF9L'
'SE9fSE9QX0xFCnJjX2xyLCBvdXRfbHIsIGVyX2xyID0gZ2l0KGdvYywgImxzLXJlbW90ZSIsICJvcmlnaW4iLCAicmVmcy9o'
'ZWFkcy9tYXN0ZXIiKSBpZiB1cmxfb2sgZWxzZSAoMSwgIiIsICIiKQplcl9sciA9IF9hbl91c2VyaW5mbyhlcl9scikKcmNf'
'bG0sIGxtLCBlcl9sbSAgICAgPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIm9yaWdpbi9tYXN0ZXIiKQpybSA9IG91dF9sci5z'
'cGxpdCgpWzBdIGlmIChub3QgcmNfbHIgYW5kIG91dF9sci5zdHJpcCgpKSBlbHNlICIiCmlmIG5vdCB1cmxfb2s6CiAgICBr'
'ZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmIm9yaWdpbj17dXJsX2luIXJ9IEtIT05HIHBoYWkga2hvIHRoYXQg4oCUICd0'
'dW9pJyBzbyB2b2kgbm8ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGdpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIs'
'ICIiLCAxCmVsaWYgbm90IHJtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwKICAgICAgICBmImtob25nIGhvaSBk'
'dW9jIG1hc3RlciB0cmVuIHJlbW90ZSAobHMtcmVtb3RlIHJjPXtyY19scn0pOiB7ZXJfbHJbOjYwXX0gIgogICAgICAgIGYi'
'4oCUIGtob25nIGNodW5nIG1pbmggZHVvYyB2ZSBuZW4gY29uIHR1b2kiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAi'
'IiwgIiIsIDEKZWxpZiByY19sbSBvciBub3QgbG06CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25nIGRv'
'YyBkdW9jIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmU6IHtlcl9sbVs6NjBdfSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9'
'IDEsICIiLCAiIiwgMQplbGlmIGxtICE9IHJtOgogICAgIyBEZW0geGVtIHR1dCBsYWkgYmFvIHhhLCBuZXUgZGVtIGR1b2Mg'
'4oCUIGNvbiBzbyBuYXkgbm9pIHJvIG11YyBkbyBzYWkgbGVjaC4KICAgIHJjX2MsIHNhdSwgXyA9IGdpdChnb2MsICJyZXYt'
'bGlzdCIsICItLWNvdW50IiwgZiJ7bG19Li57cm19IikKICAgIHhhID0gZiIsIHR1dCBsYWkge3NhdX0gY29tbWl0IiBpZiAo'
'bm90IHJjX2MgYW5kIHNhdS5zdHJpcCgpLmlzZGlnaXQoKSkgZWxzZSAiIgogICAgaW5uKGYiICBvcmlnaW4vbWFzdGVyIHRy'
'b25nIGNsb25lIDoge2xtWzoxMl19IikKICAgIGlubihmIiAgbWFzdGVyIHRyZW4gcmVtb3RlICAgICAgICA6IHtybVs6MTJd'
'fXt4YX0iKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAga2V0KCJO'
'Nycga2ljaCB0aHVvYyIsIEtERCwKICAgICAgICBmInZlIG5lbiBDVTogb3JpZ2luL21hc3Rlcj17bG1bOjEyXX0gIT0gcmVt'
'b3RlPXtybVs6MTJdfXt4YX0gIgogICAgICAgIGYi4oCUIGNoYXkgYGdpdCAtQyA8a2hvPiBmZXRjaCBvcmlnaW4gbWFzdGVy'
'YCByb2kgZG8gbGFpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsc2U6CiAgICBpbm4oZiIgIHZl'
'IG5lbiBUVU9JOiBvcmlnaW4vbWFzdGVyID0ge2xtWzoxMl19ID09IG1hc3RlciB0cmVuIHJlbW90ZSIpCiAgICBnaGkoIm1h'
'c3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICByY19tYiwgbWIsIGVyX21iID0gZ2l0KGdv'
'YywgIm1lcmdlLWJhc2UiLCAib3JpZ2luL21hc3RlciIsIGhlYWQpCmlmIHJjX21iIG9yIG5vdCBtYjoKICAgIGlmIG1iID09'
'ICIiIGFuZCBybSBhbmQgbG0gPT0gcm06CiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyB0aW5o'
'IGR1b2MgbWVyZ2UtYmFzZSB2b2kgb3JpZ2luL21hc3Rlcjoge2VyX21iWzo3MF19IikKICAgIG5zLCByYyA9ICIiLCAxCmVs'
'c2U6CiAgICBnaGkoIm1lcmdlX2Jhc2UiLCBtYikKICAgIGlubihmIiAgbWVyZ2UtYmFzZShvcmlnaW4vbWFzdGVyLCBIRUFE'
'KSA9IHttYls6MTJdfSIpCiAgICBpZiBtYiAhPSBTSEFfQkFTRV9TUEVDOgogICAgICAgIGlubihmIiAgTFVVIFk6IGtoYWMg'
'YmFzZSBtYSBzcGVjIHIzIGtoYWkgKHtTSEFfQkFTRV9TUEVDWzoxMl19KSDigJQgdmkgbmhhbmggZGEgbWVyZ2UgbWFzdGVy'
'LiIpCiAgICAgICAgaW5uKCIgICAgICAgICBEbyBzbyBiYXNlIGN1IHNlIE5VT1QgcGhhbiBtYXN0ZXIgbWFuZyB2YW8uIER1'
'bmcgbWVyZ2UtYmFzZSBtb2kgbGEgdmllYyBjdWEgZXhlY3V0b3IuIikKICAgICAgICByY194LCBuc194LCBfID0gZ2l0KGdv'
'YywgImRpZmYtdHJlZSIsICItciIsICItTSIsICItLWRpZmYtYWxnb3JpdGhtPW15ZXJzIiwgIi0tbnVtc3RhdCIsIFNIQV9C'
'QVNFX1NQRUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAgICAgICAgICAgIGggPSBbbC5zcGxpdCgiXHQiKSBmb3Ig'
'bCBpbiBuc194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICAgICAgICAgIGEgPSBzdW0oaW50KHhbMF0pIGZvciB4'
'IGluIGggaWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdoaSgibnVtc3RhdF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVw'
'IjogbGVuKGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBpbm4oZiIgICAgICAgICAoZG9pIGNoaWV1OiBzbyBiYXNlIHNw'
'ZWMgPSB7bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkgS0hPTkcgZHVuZyBkZSBjaGFtKSIpCiAgICAjIFBMVU1C'
'SU5HLCBraG9uZyBQT1JDRUxBSU46IGBnaXQgZGlmZmAgZG9jIGNhdSBoaW5oIFVJIENVQSBOR1VPSSBETyAoZGlmZi5hbGdv'
'cml0aG0sIGRpZmYucmVuYW1lcywgZGlmZi5vcmRlckZpbGUsCiAgICAjIGNvbG9yLmRpZmYpLCB2YSBnaWEgdHJpIEhPUCBM'
'RSBkb2kgbHVvbiBTTyBkb25nIG1hIHZhbiByYSBjaHUgc28g4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGk6IHVuZyB2aWVuIHRv'
'bmcgaG9wIChteWVycyArNDAxKSA9PgogICAgIyBiYW4gMzBpIERBVCAyIHRlcCAvICs0MDAgZHVvaSBgZGlmZi5hbGdvcml0'
'aG0gPSBoaXN0b2dyYW1gIGhvYWMgYHBhdGllbmNlYCwgVFJVT1QgKzQwMSBraGkgbWFjIGRpbmg7IDEwLzc1IGNvbW1pdCBj'
'aGFtCiAgICAjIHdyaXRlIHNldCBjbyBzbyBkb25nIGRvaSB0aGVvIHRodWF0IHRvYW4uIGBkaWZmLXRyZWUgLXIgLU1gID0g'
'bWFjIGRpbmggY3VhIGBnaXQgZGlmZmAgKHJlbmFtZXMgYmF0KSB2YSBLSE9ORyBkb2MgY2FjIGtob2EKICAgICMgYXkuIFRo'
'dWF0IHRvYW4gcGhhaSBUVU9ORyBNSU5IOiBkaWZmLjxkcml2ZXI+LmFsZ29yaXRobSAocXVhIGNvcmUuYXR0cmlidXRlc0Zp'
'bGUgY3VhIG5ndW9pIGRvKSBWQU4gbG90IHZhbyBwbHVtYmluZyDigJQKICAgICMgZG8gdHJlbiAyMDI2LTA5LTMwaSwgYCou'
'cHkgZGlmZj1hbGdgICsgZGlmZi5hbGcuYWxnb3JpdGhtPWhpc3RvZ3JhbTogZGlmZi10cmVlICs0MDEgY2hvIHVuZyB2aWVu'
'IG15ZXJzICs0MDA7IGNvIHR1b25nIG1pbmgKICAgICMgdGhhbmcga2hvYSBheS4gYXR0cmlidXRlcyBgLWRpZmZgL2NvcmUu'
'YmlnRmlsZVRocmVzaG9sZCB2YW4gYXAgPT4gYC1gID0+IEtIT05HIERPIERVT0MgKGNob3QgZHVvaSkuCiAgICByYywgbnMs'
'IGVyID0gZ2l0KGdvYywgImRpZmYtdHJlZSIsICItciIsICItTSIsICItLWRpZmYtYWxnb3JpdGhtPW15ZXJzIiwgIi0tbnVt'
'c3RhdCIsIG1iLCBoZWFkKQppZiByYzoKICAgIHBhc3MKZWxzZToKICAgIGhhbmcgPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBp'
'biBucy5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAgdGhlbSA9IHN1bShpbnQoaFswXSkgZm9yIGggaW4gaGFuZyBp'
'ZiBoWzBdLmlzZGlnaXQoKSkKICAgIHhvYSAgPSBzdW0oaW50KGhbMV0pIGZvciBoIGluIGhhbmcgaWYgaFsxXS5pc2RpZ2l0'
'KCkpCiAgICBnaGkoInNvX3RlcCIsIGxlbihoYW5nKSk7IGdoaSgiZG9uZ190aGVtIiwgdGhlbSk7IGdoaSgiZG9uZ194b2Ei'
'LCB4b2EpCiAgICBmb3IgaCBpbiBoYW5nOiBpbm4oZiIgICAge2hbMl06MzR9ICt7aFswXTo8NX0gLXtoWzFdfSIpCiAgICBp'
'bm4oZiIgICAgVE9ORzoge2xlbihoYW5nKX0gdGVwLCAre3RoZW19LCAte3hvYX0gICAodHJhbjoge1RSQU5fVEVQfSB0ZXAg'
'LyB7VFJBTl9ET05HfSBkb25nIHRoZW0pIikKICAgIGNoYW0gPSBzb3J0ZWQoe2hbMl0gZm9yIGggaW4gaGFuZ30gJiBXUklU'
'RV9TRVRfRzIpOyBnaGkoImNoYW1fd3JpdGVfc2V0IiwgY2hhbSkKICAgIGRlZiBfY2FfbW9pX2NvKHJldik6CiAgICAgICAg'
'IyBjYXQtZmlsZSwga2hvbmcgYHNob3dgOiBgZ2l0IHNob3dgIGNoZXQgdm9pIGNhdSBoaW5oIFVJIGdvIHNhaSAoZG8gdHJl'
'biAyMDI2LTA5LTMwaTogbG9nLmRhdGUgZ28gc2FpID0+IGJhbiAzMGkgZ29pCiAgICAgICAgIyAwZWE5NWRlIGxhICJraG9u'
'ZyBwaGFpIHVuZyB2aWVuIC4uLiBOb25lIOKAlCBkYSBsYW5kPyBuaGFtIG5oYW5oPyIpLgogICAgICAgIHJfLCBuZF8sIF8g'
'PSBnaXQoZ29jLCAiY2F0LWZpbGUiLCAiLXAiLCBmIntyZXZ9Om9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAg'
'IHJldHVybiBOb25lIGlmIHJfIGVsc2Uge3QgZm9yIHQgaW4gQ0FfTU9JX0cyIGlmIHJlLnNlYXJjaChyIig/bSleZGVmICIg'
'KyB0ICsgciJbYS16XT9fIiwgbmRfKX0KICAgIG9fbWIsIG9faCA9IF9jYV9tb2lfY28obWIpLCBfY2FfbW9pX2NvKGhlYWQp'
'CiAgICBtYW5nID0gc29ydGVkKG9faCAtIG9fbWIsIGtleT1zb19jYSkgaWYgKG9fbWIgaXMgbm90IE5vbmUgYW5kIG9faCBp'
'cyBub3QgTm9uZSkgZWxzZSBOb25lCiAgICBnaGkoImNhX21vaV9nMl9tYW5nX3ZhbyIsIG1hbmcpCiAgICBpZiBub3QgbWFu'
'ZzoKICAgICAgICAjIERvIFJPTkcgKGRhIGxhbmQsIGNoaW5oIG1hc3RlciksIG5oYW0gbmhhbmgsIGhheSBuaGFuaCBjdWEg'
'cGFja2V0IEtIQUMgY2hhbSBjdW5nIHRlcDoKICAgICAgICAjIGtob25nIG1hbmcgY2EgbW9pIG5hbyBjdWEgZzIgdGhpIGto'
'b25nIHBoYWkgdW5nIHZpZW4uIERvYyBraG9uZyBkdW9jIChOb25lKSBjdW5nIHZheS4KICAgICAgICBrZXQoIk43JyBraWNo'
'IHRodW9jIiwgS0RELCBmImRvaSB0dW9uZyBraG9uZyBwaGFpIHVuZyB2aWVuOiB7bGVuKGhhbmcpfSB0ZXAsIGNoYW0ge2No'
'YW19LCBjYSBtb2kgIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGYiZzIgbWFuZyB2YW8ge21hbmchcn0g'
'4oCUIGRhIGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPyIpCiAgICBlbHNlOgogICAgICAgICMgbnVtc3RhdCBpbiBg'
'LWAgKGtob25nIGNvIHNvIGRvbmcpIGNobyB0ZXAgYmluYXJ5Ly1kaWZmIHRoZW8gYXR0cmlidXRlcyDigJQga2UgY2EgYXR0'
'cmlidXRlcyBDVUEgTkdVT0kgRE8gKGRvIHRyZW4KICAgICAgICAjIDIwMjYtMDktMzBnOiBjb3JlLmF0dHJpYnV0ZXNGaWxl'
'IGAqLnB5IC1kaWZmYCA9PiAiMiB0ZXAgLyArMCIgREFUIGNobyAwZWE5NWRlLCB0aGF0ICszOTcpLiBgLWAgbGEgS0hPTkcg'
'RE8gRFVPQywKICAgICAgICAjIGtob25nIHBoYWkgMDsgVFJVT1QgdGhlbyBzbyB0ZXAgLyBzbyBkb25nIERBIGRlbSBkdW9j'
'IHZhbiBnaXUgKHF1YW4gc2F0IHRydWMgdGllcCkuCiAgICAgICAga2hvbmdfc28gPSBbaFsyXSBmb3IgaCBpbiBoYW5nIGlm'
'IG5vdCAoaFswXS5pc2RpZ2l0KCkgYW5kIGhbMV0uaXNkaWdpdCgpKV07IGdoaSgidGVwX2tob25nX3NvX2RvbmciLCBraG9u'
'Z19zbykKICAgICAgICB2dW90ID0gbGVuKGhhbmcpID4gVFJBTl9URVAgb3IgdGhlbSA+IFRSQU5fRE9ORwogICAgICAgIGtl'
'dCgiTjcnIGtpY2ggdGh1b2MiLCBUUlVPVCBpZiB2dW90IGVsc2UgKEtERCBpZiBraG9uZ19zbyBlbHNlIERBVCksCiAgICAg'
'ICAgICAgIGYie2xlbihoYW5nKX0gdGVwIC8gK3t0aGVtfSIgKyAoZiIg4oCUIG51bXN0YXQgS0hPTkcgY28gc28gZG9uZyBj'
'aG8ge2tob25nX3NvfSIgaWYga2hvbmdfc28gZWxzZSAiIikpCgojIENvbmcga2ljaCB0aHVvYyBQSEFJIGRlIGxhaSBNT1Qg'
'a2V0IHF1YS4gTGVuaCBudW1zdGF0IGhvbmcgdGhpIG5oYW5oIGBpZiByYzogcGFzc2Aga2hvbmcgZ2hpIGdpLCB2YSB2YW5n'
'IG1hdCBvIGRheQojIHRoYW5oIERBVCBvIGJvIGdvcDogY2F1IGhpbmggZGlmZiBDVUEgTkdVT0kgRE8gaG9uZyAoZGlmZi5v'
'cmRlckZpbGUgdHJvIHRlcCBraG9uZyBjbywgZGlmZi5hbGdvcml0aG0gZ28gc2FpID0+IHJjPTEyOCkgY2hvCiMgLS1jaGkt'
'a2ljaC10aHVvYyByYz0wIHZvaSAwIGNob3QsIGx1b3QgZGF5IGR1ICJEQVQgMTEiIHJjPTAgKGRvIHRyZW4gMjAyNi0wOS0z'
'MGgsIDBlYTk1ZGUpLiBWYW5nIG1hdCBsYSBLSE9ORyBETyBEVU9DLgojIFR1IDMwaiBudW1zdGF0IGxhIGRpZmYtdHJlZSAo'
'a2hvbmcgZG9jIGhhaSBraG9hIGF5KTsgZHVvbmcgY29uIGxhaSBkbyBkdW9jOiBkaWZmLnJlbmFtZUxpbWl0IGdvIHNhaSA9'
'PiByYz0xMjguCmlmIG5vdCBhbnkoY1swXSA9PSAiTjcnIGtpY2ggdGh1b2MiIGZvciBjIGluIGNob3QpOgogICAga2V0KCJO'
'Nycga2ljaCB0aHVvYyIsIEtERCwgZiJjb25nIEtIT05HIHJhIGtldCBxdWEgKGdpdCBkaWZmLXRyZWUgLS1udW1zdGF0IHJj'
'PXtyY30pOiB7X2FuX3VzZXJpbmZvKGVyKVs6NzBdfSIpCgojIERpbmggZGFuaCBUSEFUIG5hbSBvIE43JyAoY2EgbW9pIGcy'
'IG1hbmcgdmFvKSwgS0hPTkcgbyAiaGF1IGR1ZSBnMSI6IGcxIGRhIGxhbmQgbmVuIG1vaSBuaGFuaCBkZXUKIyBsYSBoYXUg'
'ZHVlLiBEb25nIGRhdSBraG9pIGRhbiBwaGFpIHR1IGtoYWkgdGhlbyBrZXQgcXVhIGF5IChkbyBkdW9jOiBtYXN0ZXIgNDQ2'
'MjBlOCBtbyBraG9pIGJhbmcKIyAiVEhFIEhFIERPIERVT0M6IGcyIiwgSlNPTiAidGhlX2hlIjogImcyIiwgdHJvbmcga2hp'
'IE43JyBkYSBrZXQgbHVhbiAia2hvbmcgcGhhaSB1bmcgdmllbiIpLgojIE5oYW4gY2hpIGR1b2Mgbm9pIERVTkcgY2FpIGRv'
'IGR1b2M6IGBbXWAga2hvbmcgdGFjaCAiZGEgbGFuZCIga2hvaSAibmhhbSBuaGFuaCIvInBhY2tldCBraGFjIiAoZG8KIyBk'
'dW9jIHRyZW4gMjAyNi0wOS0zMGI6IHVuZyB2aWVuIDJhNjc5NjggREEgTEFORCBiaSBnb2kgIktIT05HIHBoYWkgdW5nIHZp'
'ZW4gZzIiKS4KaWYgdGhlX2hlID09ICJnMiIgYW5kIG5vdCBzby5nZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpOgogICAgdGhl'
'X2hlID0gKCJLSE9ORyBtYW5nIGNhIG1vaSBnMiBuYW8gKGRhIGxhbmQ/IG5oYW0gbmhhbmg/IHBhY2tldCBraGFjPykiIGlm'
'IHNvLmdldCgiY2FfbW9pX2cyX21hbmdfdmFvIikgPT0gW10KICAgICAgICAgICAgICBlbHNlICJnMj8gKENIVUEgZGluaCBk'
'YW5oIGR1b2MgZG9pIHR1b25nKSIpCiAgICBnaGkoInRoZV9oZSIsIHRoZV9oZSkKCiMgQ29uZyBuaGFuaDogZG8gUklFTkcg'
'a2ljaCB0aHVvYyAodmFpIGdpYXkpIHJvaSBkdW5nLiBEdW5nIGtoaSBjYW4geGFjIG1pbmggbGFpCiMgdmUgbmVuIG1hIGto'
'b25nIG11b24gdHJhIDIwLTQ1IHBodXQgY2hvIGNhIGJvIHRlc3QuCmlmICItLWNoaS1raWNoLXRodW9jIiBpbiBzeXMuYXJn'
'djoKICAgIGlubigiIik7IGlubigiPSIgKiA3OCkKICAgIGlubigiLS1jaGkta2ljaC10aHVvYzogQ0hJIGRvIGNvbmcga2lj'
'aCB0aHVvYy4gRGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQogICAgaW5uKCItIiAqIDc4KQogICAgZm9y'
'IF90LCBfdHQsIF9jdCBpbiBjaG90OiBpbm4oZiIgIHtfdHQ6MTR9IHtfdH0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNl'
'ICIiKSkKICAgIF9rID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKICAgIF9yID0gc3VtKDEgZm9y'
'IF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQogICAgc3lzLmV4aXQoMyBpZiBfayBlbHNlICgxIGlmIF9yIGVsc2Ug'
'MCkpCgpDSElfUFJPQkUgPSAiLS1jaGktcHJvYmUiIGluIHN5cy5hcmd2ICAgICMgYm8gcXVhIGJvIHRlc3QgKyBONzsgZ2l1'
'IDAsIDEsIDMKIyAtLS0tLS0tLS0tLS0tLS0tIDIuIGJvIHRlc3QgZGF5IGR1IC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENI'
'SV9QUk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMi4gQk8gVEVTVCBEQVkgRFUgKDEwLTQwIHBodXQp'
'IikKICAgIHJjX24sIG91dF9uID0gY2hheShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgZ29jKQogICAgZ2hpKCJy'
'Y19zdWl0ZSIsIHJjX24pCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0X24pCiAgICBpbm4oIiAgcmMgPSIsIHJjX24sICJ8'
'IiwgbS5ncm91cCgwKSBpZiBtIGVsc2UgIihLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcga2V0KSIpCiAgICBpZiBtOgogICAg'
'ICAgIGdoaSgiZGF0IiwgaW50KG0uZ3JvdXAoMSkpKTsgZ2hpKCJ0cmVuIiwgaW50KG0uZ3JvdXAoMikpKTsgZ2hpKCJib19x'
'dWFfc28iLCBpbnQobS5ncm91cCg0KSkpCiAgICBkb19oZXQsIGdjLCB0aW4gPSBkb2NfZG8ob3V0X24pCiAgICBnaGkoInNv'
'X2NhX2RvIiwgbGVuKGRvX2hldCkpOyBnaGkoImxpZXRfa2VfZGF5X2R1IiwgdGluKQogICAgZm9yIGcgaW4gZ2M6IGlubigi'
'ICAgKiIsIGcpCiAgICBpbm4oIiIpOyBpbm4oZiIgID09PSB7bGVuKGRvX2hldCl9IENBIERPID09PSIpCiAgICBmb3IgdCBp'
'biBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgICAgIGlubihmIiAgIHt0LnNwbGl0KCdfJylbMF06N30ge3R9Iik7'
'IGlubihmIiAgICAgICAgICAge2RvX2hldFt0XVs6MTUwXX0iKQogICAgZ2hpKCJkb19seV9kbyIsIHt0OiBkb19oZXRbdF1b'
'OjMwMF0gZm9yIHQgaW4gZG9faGV0fSkKICAgICMgLS0tLSBDSE9UOiBtb2kgY2EgRE8gcGhhaSBHSUFJIFRISUNIIERVT0Mg'
'LS0tLQogICAgIyBUaGlldSBjaG90IG5heSwgYm8gZG8gaW4gZGFuaCBzYWNoIGRvIHJvaSB2YW4gdGhvYXQgcmM9MC4gRG8g'
'ZHVuZyBsYSBsb2kgZGEgeGF5IHJhOgogICAgIyBsdW90IFdpbmRvd3MgMTktMDkgY28gdDE3MSBETyBtYSBibyBkbyBiYW8g'
'IkRBVCAxMCB8IFRSVU9UIDAiIHZhIHJjPTAuCiAgICBkZWYgX2tob2EodCk6IHJldHVybiB0LnNwbGl0KCJfIilbMF0KICAg'
'IGRvX3BhY2tldCwgZG9fbGEsIGRvX3RoaWV1X2NvbmdfY3UgPSBbXSwgW10sIFtdCiAgICBmb3IgdCBpbiBzb3J0ZWQoZG9f'
'aGV0LCBrZXk9c29fY2EpOgogICAgICAgIGssIGx5ID0gX2tob2EodCksIGRvX2hldFt0XQogICAgICAgIGlmIGsgaW4gQ0Ff'
'UEFDS0VUOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRvX3BhY2tldC5hcHBlbmQodCkKICAgICAgICBlbGlmICJL'
'SMOUTkcgxJBPIMSQxq/hu6JDIiBpbiBseSBvciAidGhp4bq/dSBgIiBpbiBseTogIGRvX3RoaWV1X2NvbmdfY3UuYXBwZW5k'
'KHQpCiAgICAgICAgZWxpZiBrIGluIE5HT0FJX1BIQU1fVkk6ICAgICAgICAgICAgICAgICAgICAgICAgcGFzcwogICAgICAg'
'IGVsc2U6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRvX2xhLmFwcGVuZCh0KQogICAgZ2hp'
'KCJkb19wYWNrZXQiLCBkb19wYWNrZXQpOyBnaGkoImRvX2xhIiwgZG9fbGEpOyBnaGkoImRvX3RoaWV1X2NvbmdfY3UiLCBk'
'b190aGlldV9jb25nX2N1KQogICAgaW5uKCIiKQogICAgaW5uKGYiICBjYSBETyB0aHVvYyBDSElOSCBwYWNrZXQgbmF5IDog'
'e1tfa2hvYSh4KSBmb3IgeCBpbiBkb19wYWNrZXRdIG9yICdraG9uZyBjbyd9IikKICAgIGlubihmIiAgY2EgRE8gbmdvYWkg'
'cGhhbSB2aSAocjMga2hhaSk6IHtbX2tob2EoeCkgZm9yIHggaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKSBpZiBfa2hv'
'YSh4KSBpbiBOR09BSV9QSEFNX1ZJXX0iKQogICAgaW5uKGYiICBjYSBETyB2aSBUSElFVSBDT05HIENVICAgICAgIDoge1tf'
'a2hvYSh4KSBmb3IgeCBpbiBkb190aGlldV9jb25nX2N1XSBvciAna2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNhIERPIExB'
'IChraG9uZyBnaWFpIHRoaWNoIGR1b2MpOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXSBvciAna2hvbmcgY28nfSIpCiAg'
'ICAjIC0tLS0gQ0hPVDogcGhlcCBkbyBwaGFpIFRST04gdHJ1b2Mga2hpIG1vdCBjaHUgREFUIG5hbyBkdW9jIHBoYXQgLS0t'
'LQogICAgIyBCYW4gdHJ1b2MgY2hpIElOIGB0aW5gL2ByY19zdWl0ZWA6IGJvIHRlc3QgY2hldCBnaXVhIHQxNzEgKHJjPTEz'
'NCwga2hvbmcgZG9uZyB0b25nKQogICAgIyB2YW4gcmEgIkRBVCAxMiB8IFRSVU9UIDAiIHJjPTA7IGNhIFBBQ0tFVCB2YW5n'
'IG1hdCBoYXkgYmkgQk8gUVVBIGN1bmcgZHVvYyBjaGFtIG5odQogICAgIyAia2hvbmcgZG8iLiBWYW5nIG1hdCBraG9uZyBw'
'aGFpICJraG9uZyBkbyIg4oCUIGxhIEtIT05HIERPIERVT0MuCiAgICB2YW5nID0gW3QgZm9yIHQgaW4gc29ydGVkKENBX1BB'
'Q0tFVCwga2V5PXNvX2NhKSBpZiBtYXVfY2Eob3V0X24sIHQpIG5vdCBpbiAoIlFVQSIsICJETyIpXQogICAgbHlfa2RkID0g'
'W10KICAgIGlmIG5vdCB0aW46IGx5X2tkZC5hcHBlbmQoImRhbmggc2FjaCBkbyBLSE9ORyBkYXkgZHUiKQogICAgaWYgcmNf'
'biBub3QgaW4gKDAsIDEpIG9yIChyY19uID09IDEpICE9IGJvb2woZG9faGV0KToKICAgICAgICBseV9rZGQuYXBwZW5kKGYi'
'cmMgYm8gdGVzdD17cmNfbn0ga2hvbmcga2hvcCB7bGVuKGRvX2hldCl9IGNhIERPIGRvYyBkdW9jIikKICAgIGlmIHZhbmc6'
'IGx5X2tkZC5hcHBlbmQoZiJjYSBQQUNLRVQgdmFuZy9ibyBxdWE6IHt2YW5nfSIpCiAgICBnaGkoImNhX3BhY2tldF92YW5n'
'IiwgdmFuZyk7IGdoaSgibHlfZG9fY2h1YV90cm9uIiwgbHlfa2RkKQogICAgaWYgbHlfa2RkOiBrZXQoIkJvIHRlc3QgY2hh'
'eSBUUk9OIHZhIGRvYyBEVSIsIEtERCwgIjsgIi5qb2luKGx5X2tkZCkpCiAgICBjaHVhX3Ryb24gPSBLREQgaWYgbHlfa2Rk'
'IGVsc2UgREFUCiAgICBrZXQoIktob25nIGNhIG5hbyBjdWEgUEFDS0VUIGJpIERPIiwgY2h1YV90cm9uIGlmIG5vdCBkb19w'
'YWNrZXQgZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3QgZG9fcGFja2V0IGVsc2UgZiJETzoge1tfa2hvYSh4KSBmb3Ig'
'eCBpbiBkb19wYWNrZXRdfSDigJQgYmFuIHZhIENIVUEgeG9uZyIpCiAgICBrZXQoIk1vaSBjYSBETyBkZXUgZ2lhaSB0aGlj'
'aCBkdW9jIiwgY2h1YV90cm9uIGlmIG5vdCBkb19sYSBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19sYSBlbHNl'
'IGYibGE6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdfSIpCiAgICBpZiBkb190aGlldV9jb25nX2N1OgogICAgICAgIGtl'
'dCgiQ29uZyBjdSBkYXkgZHUgZGUgZG8iLCBLREQsIGYidGhpZXUgY29uZyBjdSBjaG8ge1tfa2hvYSh4KSBmb3IgeCBpbiBk'
'b190aGlldV9jb25nX2N1XX0iKQoKICAgIGJxID0gc29ydGVkKHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91'
'dF9uKX0sIGtleT1zb19jYSk7IGdoaSgiY2FfYm9fcXVhIiwgYnEpCiAgICBpbm4oIiIpOyBpbm4oZiIgIEJPIFFVQSAoe2xl'
'bihicSl9KToge1t4LnNwbGl0KCdfJylbMF0gZm9yIHggaW4gYnFdfSIpCgogICAgaW5uKCIiKTsgaW5uKCIgIE4xLU40ICh0'
'MTY1LXQxNjgpLCB0aWV1IGNoaSBuZ2hpZW0gdGh1IGN1YSByMiwgbmF5IGxhIGNoaSBiYW8gaG9pIHF1eToiKQogICAgYjQg'
'PSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQU1PSX07IGdoaSgiY2FfbW9pIiwgYjQpCiAgICBmb3IgdCBpbiBD'
'QU1PSTogaW5uKGYiICAgICB7dH06IHtiNFt0XX0iKQogICAgIyBCT19RVUEvdmFuZyBsYSBDSFVBIENIQVksIGtob25nIHBo'
'YWkgRE86IGNoaSBtb3QgY2EgRE8gbW9pIGR1b2MgcGhhdCBUUlVPVC4KICAgIGtldCgiTjEtTjQgKHQxNjUtdDE2OCkiLCBE'
'QVQgaWYgYWxsKHYgPT0gIlFVQSIgZm9yIHYgaW4gYjQudmFsdWVzKCkpCiAgICAgICAgZWxzZSAoVFJVT1QgaWYgYW55KHYg'
'PT0gIkRPIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkgZWxzZSBLREQpLCBzdHIoYjQpKQoKICAgIGlubigiIik7IGlubigiICAx'
'NSBjYSB0dW5nIGRvIHRyZW4gQ0k6IikKICAgIGIxNSA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBMTV9OyBn'
'aGkoImNhMTUiLCBiMTUpCiAgICBpbm4oIiAgICAiICsgIiAgIi5qb2luKGYie3R9OntiMTVbdF19IiBmb3IgdCBpbiBDQTE1'
'KSkKCiAgICAjIHQxMzYg4oCUIE4xMiBkbyBHSUFOIFRJRVAgcXVhIGtldCBxdWEgY2EKICAgIHQxMzZfdGVuID0gbmV4dCgo'
'dCBmb3IgdCBpbiBkb19oZXQgaWYgdC5zdGFydHN3aXRoKCJ0MTM2IikpLCBOb25lKQogICAgaWYgYjE1LmdldCgidDEzNiIp'
'ID09ICJRVUEiOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIERBVCwgInQxMzYgUVVBIikKICAg'
'IGVsaWYgYjE1LmdldCgidDEzNiIpICE9ICJETyI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwg'
'S0RELCBmInQxMzYgPSB7YjE1LmdldCgndDEzNicpIXJ9IOKAlCBraG9uZyBjaGF5L2tob25nIHRoYXkiKQogICAgZWxzZToK'
'ICAgICAgICBseSA9IGRvX2hldC5nZXQodDEzNl90ZW4sICIiKQogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVh'
'IGNhKSIsIFRSVU9ULCBmIkRPOiB7bHlbOjkwXX0iKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDMuIHByb2JlIFRIQU5HIHZhbyBo'
'YW0gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjMuIFBST0JFIFRIQU5HIOKAlCBnb2kg'
'X2dpdF93aW5kb3dzIHZvaSB0aGFtIHNvIHRpZW0iKQpzcGVjID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9j'
'YXRpb24oImxwNTQxIiwgc3RyKHRlcCkpCmxwID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhzcGVjKTsgc3Bl'
'Yy5sb2FkZXIuZXhlY19tb2R1bGUobHApCnNpZyA9IGluc3BlY3Quc2lnbmF0dXJlKGxwLl9naXRfd2luZG93cykKZ2hpKCJ0'
'aGFtX3NvX19naXRfd2luZG93cyIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQppbm4oIiAgdGhhbSBzbyBjdWEgX2dpdF93aW5k'
'b3dzOiIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQoKZGVmIGdvaSgqKmt3KToKICAgICIiIkdvaSBfZ2l0X3dpbmRvd3MsIEJB'
'VCBzdGRlcnIgZGUgbW90IGRvbmcgY2hhbiBkb2FuIGtob25nIGdpZXQgbHVvdCBkby4iIiIKICAgIGUgPSBpby5TdHJpbmdJ'
'TygpCiAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgogICAgICAgIHIgPSBscC5fZ2l0X3dpbmRvd3Mo'
'KiprdykKICAgIHJldHVybiByLCBlLmdldHZhbHVlKCkKCiMgLS0tIGRvaSBjaHVuZyByaWc6IHBoYWkgdHJhIGxvaSBkdW5n'
'IG1vdCBjYSB0YSBCSUVUIFRSVU9DIGRhcCBhbiAtLS0Kd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0'
'OgogICAgbmdvYWkgPSBQYXRoKHQpLyJuZ29haSI7IG5nb2FpLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtk'
'aXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIChuZ29haS8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngi'
'LCBlbmNvZGluZz0idXRmLTgiKQogICAgcjEsIF8gPSBnb2kocGF0aD1zdHIobmdvYWkpLCBwcm9ncmFtX2ZpbGVzPXN0cihw'
'ZiksIGN3ZD1zdHIoY3cpKQogICAgKGN3LyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAg'
'ICByMiwgXyA9IGdvaShwYXRoPXN0cihjdyksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCnJpZ19vayA9'
'IGJvb2wocjEpIGFuZCByMiBpcyBOb25lCmdoaSgicmlnX2RvaV9jaHVuZyIsIHJpZ19vaykKa2V0KCJSSUcgZG9pIGNodW5n'
'IChiaWV0IHRydW9jIGRhcCBhbikiLCBEQVQgaWYgcmlnX29rIGVsc2UgS0RELAogICAgZiJuZ29haS1jd2QtPnsnTkhBTicg'
'aWYgcjEgZWxzZSAnTm9uZSd9IHwgdHJvbmctY3dkLT57J05IQU4nIGlmIHIyIGVsc2UgJ05vbmUnfSIpCmlmIG5vdCByaWdf'
'b2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IHJpZyBzYWksIG1vaSBjaG90IGR1b2kgc2Ugdm8gbmdoaWEu'
'Iik7IHN5cy5leGl0KDMpCgojIC0tLSBNT0kgQ09ORyBQSEFJIFRVIENIVU5HIE1JTkggTk8gQ08gVEhFIERPIC0tLQojIEJh'
'aSBob2MgZGF0IG5oYXQgY3VhIHBhY2tldCBuYXk6IGRvX24xMCBiYW4gY3UgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25n'
'IGtoaSB0MTcxCiMgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGtodXlldCB0YXQgbWEgTjEwIHNpbmggcmEgZGUg'
'YmF0LiBObyBkZWdlbmVyYXRlIOKAlAojIHRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyBuZW4gInRhY2ggZHVu'
'ZyIgdmEgInRhY2ggc2FpIiBjaG8gY3VuZyBrZXQgcXVhLgojIE1vdCBjb25nIGtob25nIHRoZSBETyB0aGkga2hvbmcgcGhh'
'aSBjb25nLCB2YSBubyBuZ3V5IGhpZW0gaG9uIGtob25nIGNvIGNvbmc6IG5vCiMgcGhhdCByYSBtb3QgY2h1IERBVC4KIwoj'
'IE5lbiB0cnVvYyBraGkgRFVORyBuYW0gY29uZyBuYXkgZGUgcGhhbiBxdXlldCwgYmF0IHR1bmcgY29uZyBnaWV0IG1vdCBk'
'b3QgYmllbiBkYQojIGJpZXQgdHJvbmcuIENvbmcgbmFvIGtob25nIGdpZXQgZHVvYyB0aGkgY2h1IERBVCBjdWEgbm8gYmkg'
'SEEgeHVvbmcgS0hPTkcgRE8gRFVPQzsKIyBUUlVPVCBnaXUgbmd1eWVuIChxdWFuIHNhdCB0cnVjIHRpZXAsIHZkLiBnMSB2'
'YW4gbmhhbiBnaXQuYmF0KS4gRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaQojIGR1'
'bmcgdG9pIChjdW5nIGt5IGx1YXQgbmh1IE43KS4KRE9UX0JJRU5fVFVfS0lFTSA9IFsKICAgICgiTjgiLCAib3BzL2xlYXNl'
'X3B1Ymxpc2gucHkiLAogICAgICdpZiBjaGlfZGluaCBhbmQgUGF0aChjaGlfZGluaCkubmFtZS5sb3dlcigpID09ICJnaXQu'
'ZXhlIiBhbmQgaG9wX2xlKGNoaV9kaW5oKTonLAogICAgICJpZiBjaGlfZGluaCBhbmQgaG9wX2xlKGNoaV9kaW5oKToiKSwK'
'ICAgICgiTjkiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJkID0gZF9yYXcuc3RyaXAoKS5zdHJpcCgnXCInKSIs'
'ICJkID0gZF9yYXcuc3RyaXAoKSIpLAogICAgKCJOMTAiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJzZXAgPSBv'
'cy5wYXRoc2VwIGlmIHBoYW5fY2FjaCBpcyBOb25lIGVsc2UgcGhhbl9jYWNoIiwgInNlcCA9IG9zLnBhdGhzZXAiKSwKICAg'
'ICgiTjExIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwgImlmIGNoYW5fZG9hbiBpcyBub3QgTm9uZToiLCAiaWYgRmFsc2U6'
'IiksCiAgICAoIk4xMiIsICJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IiwKICAgICAnZ2l0X3BhdGg9Ii8va2hvbmctY28v'
'Z2l0IicsICdnaXRfcGF0aD0iL2tob25nLWNvL2dpdCInKSwKXQppbm4oIiIpOyBpbm4oIiAgdHUga2llbSBjb25nIOKAlCBt'
'b2kgY29uZyBwaGFpIGdpZXQgZHVvYyBtb3QgZG90IGJpZW4gZGEgYmlldDoiKQpnaWV0ID0ge30KZm9yIG1hLCBkdW9uZywg'
'dGltLCB0aGF5IGluIERPVF9CSUVOX1RVX0tJRU06CiAgICBfdGVuLCBfaGFtID0gbmV4dCgoKGEsIGIpIGZvciBhLCBiIGlu'
'IFBST0JFIGlmIGEuc3RhcnRzd2l0aChtYSArICIgIikpLCAoTm9uZSwgTm9uZSkpCiAgICBpZiBfaGFtIGlzIE5vbmU6CiAg'
'ICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IGtob25nIHRpbSB0aGF5IHBy'
'b2JlIHRlbiAne21hfSAuLi4nIik7IGNvbnRpbnVlCiAgICB0cnk6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlE'
'aXJlY3RvcnkoKSBhcyBfdDoKICAgICAgICAgICAgX2MgPSBQYXRoKF90KS8iY2F5Ijsgc2h1dGlsLmNvcHl0cmVlKGdvYy8i'
'b3BzIiwgX2MvIm9wcyIpCiAgICAgICAgICAgIF9mID0gX2MvZHVvbmc7IF9uZCA9IF9mLnJlYWRfdGV4dChlbmNvZGluZz0i'
'dXRmLTgiKQogICAgICAgICAgICBpZiBfbmQuY291bnQodGltKSAhPSAxOgogICAgICAgICAgICAgICAgZ2lldFttYV0gPSBO'
'b25lCiAgICAgICAgICAgICAgICBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IG1hdSBkb3QgYmllbiBraG9wIHtf'
'bmQuY291bnQodGltKX0gbGFuIChtb25nIDEpIgogICAgICAgICAgICAgICAgICAgIGYiIOKAlCBtYSBuZ3VvbiBkYSBkb2ks'
'IGRvdCBiaWVuIG5heSBoZXQgeSBuZ2hpYSIpOyBjb250aW51ZQogICAgICAgICAgICBfZi53cml0ZV90ZXh0KF9uZC5yZXBs'
'YWNlKHRpbSwgdGhheSwgMSksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIF9zcCA9IGltcG9ydGxpYi51dGlsLnNw'
'ZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF9kYl8iICsgbWEsIHN0cihfYy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQog'
'ICAgICAgICAgICBfbSA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21v'
'ZHVsZShfbSkKICAgICAgICAgICAgZGVmIF9nb2lfZGIoKiprdyk6CiAgICAgICAgICAgICAgICBfZSA9IGlvLlN0cmluZ0lP'
'KCkKICAgICAgICAgICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoX2UpOgogICAgICAgICAgICAgICAg'
'ICAgIHJldHVybiBfbS5fZ2l0X3dpbmRvd3MoKiprdyksIF9lLmdldHZhbHVlKCkKICAgICAgICAgICAgX3R0LCBfY3QsIF8g'
'PSBfaGFtKF9nb2lfZGIsIGluc3BlY3Quc2lnbmF0dXJlKF9tLl9naXRfd2luZG93cyksCiAgICAgICAgICAgICAgICAgICAg'
'ICAgICAgICAgICBfYy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBnaWV0W21hXSA9IChfdHQgPT0g'
'VFJVT1QpCiAgICAgICAgaW5uKGYiICAgIHttYTo0fSBkb3QgYmllbiAtPiB7X3R0OjE0fSB7J0dJRVQgRFVPQycgaWYgX3R0'
'ID09IFRSVU9UIGVsc2UgJ1NPTkcgU09UJ30iCiAgICAgICAgICAgICsgKGYiICAgKHtfY3R9KSIgaWYgX2N0IGVsc2UgIiIp'
'KQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0g'
'S0hPTkcgRE8gRFVPQzoge3R5cGUoX2UpLl9fbmFtZV9ffToge19lfSIpCmdoaSgiY29uZ19naWV0X2R1b2NfZG90X2JpZW4i'
'LCBnaWV0KQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwpIGluIFsodCwgZihnb2ksIHNpZywgdGVwdCkpIGZvciB0LCBmIGluIFBS'
'T0JFXToKICAgIGdoaSgicHJvYmVfIiArIHRlbi5zcGxpdCgpWzBdLmxvd2VyKCksIGRsKQogICAgaWYgaXNpbnN0YW5jZShk'
'bCwgZGljdCk6CiAgICAgICAgZm9yIGssIHYgaW4gZGwuaXRlbXMoKTogaW5uKGYiICAgIHtrOjM0fToge3Z9IikKICAgIG1h'
'ID0gdGVuLnNwbGl0KClbMF0KICAgIGlmIGdpZXQuZ2V0KG1hKSBpcyBub3QgVHJ1ZSBhbmQgdHQgPT0gREFUOgogICAgICAg'
'ICMgREFUIHR1IG1vdCBjb25nIGNodWEgY2h1bmcgbWluaCBkdW9jIGxhIGJpZXQgRE8gdGhpIGtob25nIGRhbmcgdGluIGhv'
'biBLREQuCiAgICAgICAga2V0KHRlbiwgS0RELCBmImNvbmcgS0hPTkcgZ2lldCBkdW9jIGRvdCBiaWVuIGN1YSBjaGluaCBu'
'byAoe2dpZXQuZ2V0KG1hKSFyfSkiCiAgICAgICAgICAgICAgICAgICAgICBmIiAtPiBjaHUgREFUIG5heSBraG9uZyBjbyBn'
'aWEgdHJpIikKICAgIGVsc2U6CiAgICAgICAga2V0KHRlbiwgdHQsIGN0KQoKIyAtLS0tLS0tLS0tLS0tLS0tIDQuIE43IGRv'
'dCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gLS0tLS0tLS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsg'
'aW5uKCItIiAqIDc4KTsgaW5uKCI0LiBONyDigJQgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAoY2F5IHRoYXQgS0hPTkcg'
'YmkgZHVuZyB0b2kpIikKICAgIHRydW9jID0gdGVwLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lO'
'KQogICAgZ2hpKCJuN190cnVvYyIsIHRydW9jKTsgaW5uKGYiICBzbyBkb25nIGtob3Age01BVV9XSU4hcn06IFRSVU9DID0g'
'e3RydW9jfSBbbW9uZyAxXSIpCiAgICBpZiB0cnVvYyAhPSAxOgogICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2lu'
'ZG93cyIsIEtERCwgZiJtYXUgeHVhdCBoaWVuIHt0cnVvY30gbGFuLCBraG9uZyBwaGFpIDEiKQogICAgZWxzZToKICAgICAg'
'ICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHRtcDoKICAgICAgICAgICAgc2FvID0gUGF0aCh0bXAp'
'LyJjYXkiCiAgICAgICAgICAgIHNodXRpbC5jb3B5dHJlZShnb2MsIHNhbywgaWdub3JlPXNodXRpbC5pZ25vcmVfcGF0dGVy'
'bnMoIi5naXQiLCAiX19weWNhY2hlX18iLCAiKi5weWMiKSkKICAgICAgICAgICAgZjIgPSBzYW8vIm9wcyIvImxlYXNlX3B1'
'Ymxpc2gucHkiCiAgICAgICAgICAgIGYyLndyaXRlX3RleHQoZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJlcGxh'
'Y2UoTUFVX1dJTiwgImlmIEZhbHNlOiIpLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBzYXUgPSBmMi5yZWFkX3Rl'
'eHQoZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTik7IGdoaSgibjdfc2F1Iiwgc2F1KQogICAgICAgICAgICBpbm4o'
'ZiIgIFNBVSAoZGEgZG90IGJpZW4pID0ge3NhdX0gW21vbmcgMF0iKQogICAgICAgICAgICBpZiBzYXUgIT0gMDoKICAgICAg'
'ICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgImRvdCBiaWVuIEtIT05HIGFwIGR1b2Mi'
'KQogICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmNfbSwgb3V0X20gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxp'
'c2hfdGVzdC5weSJdLCBzYW8pCiAgICAgICAgICAgICAgICBtMTY1ID0gbWF1X2NhKG91dF9tLCAidDE2NSIpOyBkbSwgXywg'
'XyA9IGRvY19kbyhvdXRfbSkKICAgICAgICAgICAgICAgIHRlbjE2NSA9IG5leHQoKHQgZm9yIHQgaW4gZG0gaWYgdC5zdGFy'
'dHN3aXRoKCJ0MTY1IikpLCBOb25lKQogICAgICAgICAgICAgICAgbHkgPSAoZG0uZ2V0KHRlbjE2NSkgb3IgIiIpCiAgICAg'
'ICAgICAgICAgICBnaGkoIm43X3QxNjUiLCBtMTY1KTsgZ2hpKCJuN19seV9kbyIsIGx5WzoyMDBdKQogICAgICAgICAgICAg'
'ICAgaW5uKGYiICB0MTY1IHNhdSBkb3QgYmllbjoge20xNjV9IHwge2x5WzoxMTBdfSIpCiAgICAgICAgICAgICAgICBkdW5n'
'X2x5X2RvID0gIlBBVEggdCIgaW4gbHkgb3IgIi91c3IvYmluIiBpbiBseQogICAgICAgICAgICAgICAga2V0KCJONyBkb3Qg'
'YmllbiBuaGFuaCBXaW5kb3dzIiwgREFUIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pIGVsc2UKICAgICAgICAg'
'ICAgICAgICAgICAoVFJVT1QgaWYgbTE2NSA9PSAiRE8iIGVsc2UgS0REKSwKICAgICAgICAgICAgICAgICAgICAiZ2lldCBk'
'dW5nIGx5IGRvIiBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKQogICAgICAgICAgICAgICAgICAgIGVsc2UgKCJE'
'TyBuaHVuZyBLSE9ORyBkdW5nIGx5IGRvIC0+IHRpbiBkdW5nIGdpYSIgaWYgbTE2NSA9PSAiRE8iIGVsc2UgImtob25nIGRv'
'YyBkdW9jIHQxNjUiKSkKCiMgLS0tLS0tLS0tLS0tLS0tLSBLRVQgTFVBTiAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlu'
'bigiPSIgKiA3OCkKaW5uKGYiVEhFIEhFIERPIERVT0M6IHt0aGVfaGV9ICAgSEVBRD17aGVhZFs6MTJdfSIpCiMgS2hvaSBk'
'YW4gY2hvIHJldmlld2VyIGJhdCBkYXUgbyBkb25nIHRyZW4sIG5lbiBDSEUgRE8gcGhhaSBuYW0gTkdBWSBkdW9pIG5vOiBr'
'aG9uZyBjbyBkb25nIG5heQojIHRoaSBtb3QgbHVvdCAtLWNoaS1wcm9iZSBpbiAiREFUIDcgfCBUUlVPVCAwIHwgS0hPTkcg'
'RE8gRFVPQyAwIiByYz0wIG1hIGtob25nIG5vaSBsYSBjaHVhIGNoYXkgYm8gdGVzdC4KZ2hpKCJjaGVfZG8iLCAiY2hpLXBy'
'b2JlIiBpZiBDSElfUFJPQkUgZWxzZSAiZGF5LWR1IikKaWYgQ0hJX1BST0JFOgogICAgaW5uKCItLWNoaS1wcm9iZTogQ0hJ'
'IGRvIG11YyAwLCAxLCAzLiBCbyB0ZXN0LCBOMS1ONCwgdDEzNiwgTjcgS0hPTkcgY2hheSAtIGRheSBLSE9ORyBwaGFpIG1v'
'dCBsdW90IG5naGllbSB0aHUuIikKaWYgdGhlX2hlID09ICJnMSI6CiAgICBpbm4oIkxVVSBZOiBkYXkgbGEgTkVOIERPIChn'
'MSksIEtIT05HIHBoYWkgbmdoaWVtIHRodSBnMi4gQ2FjIGNob3QgTjgtTjEyIGR1b2kgZGF5IikKICAgIGlubigiICAgICAg'
'IFRSVU9UIGxhIERVTkcgTkhVIE1PTkcg4oCUIGNodW5nIGxhIG5odW5nIGxvIGcyIHNpbmggcmEgZGUgdsOhLiIpCmlubigi'
'LSIgKiA3OCkKZm9yIHRlbiwgdHQsIGN0IGluIGNob3Q6CiAgICBpbm4oZiIgIHt0dDoxNH0ge3Rlbn0iICsgKGYiICAge2N0'
'fSIgaWYgY3QgZWxzZSAiIikpCm5fa2RkID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKbl90cnVv'
'dCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKaW5uKCItIiAqIDc4KQppbm4oZiIgIERBVCB7'
'c3VtKDEgZm9yIF8sdCxfIGluIGNob3QgaWYgdD09REFUKX0gfCBUUlVPVCB7bl90cnVvdH0gfCBLSE9ORyBETyBEVU9DIHtu'
'X2tkZH0iKQppbm4oZiIgIFRvbmcgY2EgZG86IHtzby5nZXQoJ3NvX2NhX2RvJyl9IHwgZGFuaCBzYWNoIGRheSBkdTogeydD'
'TycgaWYgc28uZ2V0KCdsaWV0X2tlX2RheV9kdScpIGVsc2UgJ0tIT05HIERPIERVT0MnfSIpCmlubihmIiAgQWRtaW5pc3Ry'
'YXRvcjoge3NvLmdldCgncXV5ZW5fYWRtaW4nKX0gfCBzeW1saW5rOiB7c28uZ2V0KCdzeW1saW5rX2R1b2MnKX0iKQppbm4o'
'IiIpOyBpbm4oIi0tLSBEQU4gTkdVWUVOIEtIT0kgSlNPTiBOQVkgVkUgQ0hPIFJFVklFV0VSIC0tLSIpCmdoaSgiY2hvdCIs'
'IFt7InRlbiI6IGEsICJ0cmFuZ190aGFpIjogYiwgImNoaV90aWV0IjogY30gZm9yIGEsIGIsIGMgaW4gY2hvdF0pCmlubihq'
'c29uLmR1bXBzKHNvLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0xLCBkZWZhdWx0PXN0cikpCiMgcmM6IDAgPSBtb2kg'
'Y2hvdCBEQVQgfCAxID0gY28gY2hvdCBUUlVPVCB8IDMgPSBjbyBjaG90IEtIT05HIERPIERVT0MgKHV1IHRpZW4gYmFvIGRv'
'bmcpCnN5cy5leGl0KDMgaWYgbl9rZGQgZWxzZSAoMSBpZiBuX3RydW90IGVsc2UgMCkpCg=='
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
