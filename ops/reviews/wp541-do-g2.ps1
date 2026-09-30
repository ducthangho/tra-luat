# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
# Luot DAY DU can SAN mot python >= 3.9 CO PyYAML (pip install pyyaml): ban nhung python.org ma tep nay tu tai
# KHONG co PyYAML/pip, nen no chi du cho -ChiKichThuoc / -ChiProbe. Thieu thi dung o buoc cong cu, rc=3.
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
# Bien PYTHON* bi bo o buoc cong cu, de TRA LAI o MOI loi ra (Dung, trap, -ChiGiaiNen, cuoi tep). Goi bang `& .\wp541-do-g2.ps1`
# trong mot phien PowerShell DANG MO thi env cua tien trinh nay LA env cua phien ay: ban 30f xoa luon PYTHONPATH/PYTHONSTARTUP/
# PYTHONUTF8 cua phien nguoi do (do tren pwsh 7.4, 2026-09-30f: sau lenh ca ba deu RONG; ban 30e: giu nguyen).
$script:PyEnvCu = @{}
function TraMoiTruong { foreach ($k in @($script:PyEnvCu.Keys)) { Set-Item -LiteralPath ('Env:' + $k) -Value $script:PyEnvCu[$k] } }

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
$ShaBoDo    = '90e61be2d1c8da771eb06b610a2e3581eff8cb2006046184b8e7593042aed788'      # SHA-256 cua bo do Python nhung ben duoi

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
@(Get-ChildItem Env:) | Where-Object { $_.Name -like 'PYTHON*' -and $_.Name -notin @('PYTHONHOME','PYTHONUSERBASE','PYTHONNOUSERSITE') } |
    ForEach-Object { $script:PyEnvCu[$_.Name] = $_.Value; Remove-Item -LiteralPath ('Env:' + $_.Name) }
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
'YzJkMmFiYmRkYmI2ZiIKQkFOX0JPX0RPID0gIjIwMjYtMDktMzBnIiAgICAgICAgICAgICAgIyBkb2kgTU9JIGtoaSBzdWEg',
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
'dWMgYm8pLiBEb2kgYnVvYyBheSB0cm9uZyBjaS55bWwgdGhpCiMgZG9pIF9HSVRfR0xPQkFMX0NJLiBDb24gbGFpIChraG9h',
'IGhlIHRob25nIGtoYWMpIGxhIGdpb2kgaGFuIGRhIGJpZXQsIGtob25nIHBoYWkgZGEgZG9uZy4KX0dJVF9HTE9CQUxfQ0kg',
'PSAiW2luaXRdXG5cdGRlZmF1bHRCcmFuY2ggPSBtYXN0ZXJcbltjb3JlXVxuXHRhdXRvY3JsZiA9IGZhbHNlXG5cdGVvbCA9',
'IGxmXG5cdGFiYnJldiA9IDdcbiIKZGVmIGNoYXkoYXJndiwgY3dkLCBwaHV0PTYwKToKICAgIGZkLCBnYyA9IHRlbXBmaWxl',
'Lm1rc3RlbXAocHJlZml4PSJ3cDU0MS1naXRjb25maWctY2ktIiwgc3VmZml4PSIuaW5pIikKICAgIHRyeToKICAgICAgICB3',
'aXRoIG9zLmZkb3BlbihmZCwgInciLCBlbmNvZGluZz0iYXNjaWkiLCBuZXdsaW5lPSJcbiIpIGFzIGY6IGYud3JpdGUoX0dJ',
'VF9HTE9CQUxfQ0kpCiAgICAgICAgbXQgPSB7azogdiBmb3IgaywgdiBpbiBvcy5lbnZpcm9uLml0ZW1zKCkKICAgICAgICAg',
'ICAgICBpZiBub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIkdJVF8iKSBhbmQgKG5vdCBrLnVwcGVyKCkuc3RhcnRzd2l0aCgi',
'UFlUSE9OIikgb3Igay51cHBlcigpIGluIF9QWV9HSVUpfQogICAgICAgIG10LnVwZGF0ZShQWVRIT05VVEY4PSIxIiwgUFlU',
'SE9OSU9FTkNPRElORz0idXRmLTgiLCBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0iMSIsIFBZVEhPTlVOQlVGRkVSRUQ9IjEi',
'LAogICAgICAgICAgICAgICAgICBHSVRfQ09ORklHX0dMT0JBTD1nYykKICAgICAgICBwID0gc3VicHJvY2Vzcy5ydW4oW3N5',
'cy5leGVjdXRhYmxlXSArIGFyZ3YsIGN3ZD1zdHIoY3dkKSwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwKICAgICAgICAgICAgICAg',
'ICAgICAgICAgICAgdGV4dD1UcnVlLCBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQq',
'NjAsIGVudj1tdCkKICAgIGZpbmFsbHk6CiAgICAgICAgdHJ5OiBvcy5yZW1vdmUoZ2MpCiAgICAgICAgZXhjZXB0IE9TRXJy',
'b3I6IHBhc3MKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpk',
'ZWYgbWF1X2NhKG91dCwgdCk6CiAgICBtID0gcmUuc2VhcmNoKHIiKD9tKV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMq',
'KSBbMC05Ll0rcyAoXHcrKVxzKiQiLCBvdXQpCiAgICByZXR1cm4gbS5ncm91cCgyKSBpZiBtIGVsc2UgTm9uZQoKZGVmIGdp',
'dChnb2MsICphLCBwaHV0PTUpOgogICAgcCA9IHN1YnByb2Nlc3MucnVuKFsiZ2l0IiwgIi1DIiwgc3RyKGdvYyksICphXSwg',
'Y2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgIGVuY29kaW5nPSJ1dGYtOCIs',
'IGVycm9ycz0icmVwbGFjZSIsIHRpbWVvdXQ9cGh1dCo2MCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBv',
'ciAiIikuc3RyaXAoKSwgKHAuc3RkZXJyIG9yICIiKS5zdHJpcCgpCgoKIyA9PT09PT09PT09PT09PT09PSBOQU0gUFJPQkUs',
'IHZpZXQgdGhhbmggSEFNIFRIVUFOIGRlIFRVIEtJRU0gZHVvYyA9PT09PT09PT09PT09PT09PQojIE1vaSBoYW0gdHJhICh0',
'cmFuZ190aGFpLCBjaGlfdGlldCwgZHVfbGlldSkuIEtIT05HIGluLCBLSE9ORyB0aG9hdCDigJQgbmhvIHZheSBjaHVuZwoj',
'IGNoYXkgZHVvYyB0cmVuIG5lbiBCQVQgS1ksIHZhIGAtLXR1LWtpZW0tcHJvYmVgIGdvaSB0aGFuZyBjaHVuZyBkZSBraWVt',
'IGNoaW5oIGJvIGRvLgoKZGVmIF9zYW4odCk6CiAgICBkID0gUGF0aCh0KS8iZCI7IGQubWtkaXIoKTsgY3cgPSBQYXRoKHQp',
'LyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgcmV0dXJuIGQsIGN3LCBwZgoK',
'ZGVmIGRvX244KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkJ1b2MgMSAoQ09OR19DVV9HSVQpIGNoaSBkdW9jIG5oYW4gZ2l0',
'LmV4ZS4gRG9pIGNodW5nIGR1b25nOiBnaXQuZXhlIFZBTiBwaGFpIG5oYW4uIiIiCiAgICBrcSA9IHt9CiAgICB3aXRoIHRl',
'bXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIGZv',
'ciB0ZW4gaW4gKCJnaXQuZXhlIiwgImdpdC5iYXQiLCAiZ2l0LmNtZCIsICJnaXQucHkiLCAia2hvbmctcGhhaS1naXQudHh0',
'Iik6CiAgICAgICAgICAgIGYgPSBkL3RlbjsgZi53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAg',
'ICAgciwgXyA9IGdvaShjb25nX2N1X2dpdD1zdHIoZiksIHBhdGg9IiIsIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0',
'cihjdykpCiAgICAgICAgICAgIGtxW2YiQ09OR19DVV9HSVQ9e3Rlbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIlRVIENIT0ki',
'CiAgICBsb3QgPSBbayBmb3IgaywgdiBpbiBrcS5pdGVtcygpIGlmIHYgPT0gIk5IQU4iIGFuZCBub3Qgay5lbmRzd2l0aCgi',
'Z2l0LmV4ZSIpXQogICAgaWYga3EuZ2V0KCJDT05HX0NVX0dJVD1naXQuZXhlIikgIT0gIk5IQU4iOgogICAgICAgIHJldHVy',
'biBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogZ2l0LmV4ZSBob3AgbGUgbWEgYmkgdHUgY2hvaSIsIGtxCiAgICByZXR1',
'cm4gKERBVCBpZiBub3QgbG90IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IGxvdCBlbHNlIGYiY29uIG5oYW46IHtsb3R9Iiks',
'IGtxCgpkZWYgZG9fbjkoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiTXVjIFBBVEggYm9jIG5oYXkga2VwIHBoYWkgTkhBTjsg',
'bXVjIHJvbmcgLyB0b2FuIGtob2FuZyB0cmFuZyBwaGFpIGJvIHF1YSwga2hvbmcgbmVtLiIiIgogICAga3EgPSB7fQogICAg',
'd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJjbyBnaXQiOyBk',
'Lm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkK',
'ICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGZvciBuaGFu',
'LCBtdWMgaW4gKCgia2hvbmcgbmhheSIsIHN0cihkKSksICgiY28gbmhheSBrZXAiLCBmJyJ7ZH0iJyksCiAgICAgICAgICAg',
'ICAgICAgICAgICAgICAgKCJyb25nIiwgIiIpLCAoImNoaSBraG9hbmcgdHJhbmciLCAiICAgIikpOgogICAgICAgICAgICB0',
'cnk6CiAgICAgICAgICAgICAgICByLCBfID0gZ29pKHBhdGg9bXVjLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIo',
'Y3cpKQogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIKICAgICAg',
'ICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgICAga3FbZiJQQVRIIHtuaGFufSJdID0gZiJORU0g',
'e3R5cGUoZSkuX19uYW1lX199IgogICAgaWYga3EuZ2V0KCJQQVRIIGtob25nIG5oYXkiKSAhPSAiTkhBTiI6CiAgICAgICAg',
'cmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBtdWMgUEFUSCB0aHVvbmcgbWEga2hvbmcgdGltIHJhIGdpdC5l',
'eGUiLCBrcQogICAgb2sgPSAoa3EuZ2V0KCJQQVRIIGNvIG5oYXkga2VwIikgPT0gIk5IQU4iCiAgICAgICAgICBhbmQga3Eu',
'Z2V0KCJQQVRIIHJvbmciKSA9PSAiTm9uZSIgYW5kIGtxLmdldCgiUEFUSCBjaGkga2hvYW5nIHRyYW5nIikgPT0gIk5vbmUi',
'KQogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIpLCBrcQoKIyBE',
'YXUgcGhhbiBjYWNoIGR1bmcgREUgVEhVLiBQaGFpIEtIQUMgb3MucGF0aHNlcCB0cmVuIENBIEhBSSBuZW4gKCc7JyBXaW5k',
'b3dzLCAnOicgUE9TSVgpCiMgdGhpIGhhaSBnaWEgdGh1eWV0ICJ0YWNoIHRoZW8gZGF1IGR1b2MgdHJ1eWVuIiB2YSAidGFj',
'aCB0aGVvIG9zLnBhdGhzZXAiIG1vaSByb2kgcmEgbmhhdS4KVEhVX04xMCA9ICJ8IgoKZGVmIGRvX24xMChnb2ksIHNpZywg',
'dGVwdCk6CiAgICAiIiJIYW0gcGhhaSB0YWNoIFBBVEggdGhlbyBkYXUgcGhhbiBjYWNoIERVT0MgVFJVWUVOLCBraG9uZyB0',
'aGVvIG9zLnBhdGhzZXAgY3VhIG5lbi4KCiAgICBCYW4gY3UgZG8gIm1vdCBkYXUgJzsnIHRyb25nIFRFTiB0aHUgbXVjIiB2',
'YSBkYXQgREFUIHRyZW4gV2luZG93cyBkdSBoYW0gc2FpLiBObwogICAgZGVnZW5lcmF0ZTogdHJlbiBXaW5kb3dzIG9zLnBh',
'dGhzZXAgREEgbGEgJzsnLCBuZW4gJ0M6L2E7YicgdGhhdCBzdSBDTyBOR0hJQSBsYSBoYWkKICAgIG11YyDigJQgInRhY2gg',
'ZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gcmEgY3VuZyBrZXQgcXVhLCBwaGVwIGRvIGtob25nIHRoZSBkbyBuYW8uIE5vCiAg',
'ICBkYSBjaGFtIERBVCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5n',
'IGtodXlldCB0YXQgYXkuCiAgICBNb3QgY29uZyBraG9uZyB0aGUgZG8gdGhpIGtob25nIHBoYWkgY29uZy4KICAgICIiIgog',
'ICAgdGVuX3NlcCA9IG5leHQoKGsgZm9yIGsgaW4gKCJwaGFuX2NhY2giLCAiZGF1X3BoYW5fY2FjaCIsICJzZXAiKSBpZiBr',
'IGluIHNpZy5wYXJhbWV0ZXJzKSwgTm9uZSkKICAgIGlmIHRlbl9zZXAgaXMgTm9uZToKICAgICAgICAjIEtob25nIGNvIHRo',
'YW0gc28gdGhpIHRyZW4gV2luZG93cyBLSE9ORyBjb24gZHVvbmcgbmFvIHRhY2ggaGFpIGdpYSB0aHV5ZXQuCiAgICAgICAg',
'aWYgb3MucGF0aHNlcCA9PSAiOyI6CiAgICAgICAgICAgIHJldHVybiAoS0RELCAidHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAg',
'REEgbGEgJzsnIHZhIGhhbSBraG9uZyBuaGFuIHRoYW0gc28gZGF1IHBoYW4gY2FjaCAiCiAgICAgICAgICAgICAgICAgICAg',
'ICAgICAiLT4ga2hvbmcgdGFjaCBkdW9jIGhhaSBnaWEgdGh1eWV0IiwKICAgICAgICAgICAgICAgICAgICB7Im9zLnBhdGhz',
'ZXAiOiBvcy5wYXRoc2VwLCAidGhhbSBzbyBzZXAiOiBOb25lfSkKICAgICAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURp',
'cmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgICAgIGxhID0gUGF0aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKQogICAgICAgICAg',
'ICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5n',
'PSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8gID0gZ29pKHBhdGg9c3RyKGxhKSArIG9zLnBhdGhzZXAgKyBzdHIoZCksIHBy',
'b2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgICAgIHIwLCBfID0gZ29pKHBhdGg9c3RyKGQpLCBw',
'cm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgIGtxID0geyJvcy5wYXRoc2VwIjogb3MucGF0aHNl',
'cCwgInRoYW0gc28gc2VwIjogTm9uZSwKICAgICAgICAgICAgICAiY28gbXVjIGNodWEgJzsnIjogIk5IQU4iIGlmIHIgZWxz',
'ZSAiTm9uZSIsCiAgICAgICAgICAgICAgImRvaSBjaHVuZyBkdW9uZyAoa2hvbmcgY28gJzsnKSI6ICJOSEFOIiBpZiByMCBl',
'bHNlICJOb25lIn0KICAgICAgICBpZiBub3QgcjA6CiAgICAgICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcg',
'aG9uZyIsIGtxCiAgICAgICAgcmV0dXJuIChEQVQgaWYgciBlbHNlIFRSVU9UKSwgKCIiIGlmIHIgZWxzZSAibXVjIGdpdC5l',
'eGUgaG9wIGxlIGJpIE1BVCIpLCBrcQoKICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAg',
'ICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkgICAgICAgICAgIyAnOycgbmFtIHRyb25nIFRFTiwga2hv',
'bmcgcGhhaSBkYXUgcGhhbiBjYWNoCiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIiku',
'd3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgbm9pID0gc3RyKGxhKSArIFRIVV9OMTAgKyBzdHIo',
'ZCkKICAgICAgICBrdyA9IGRpY3QocHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICByX2NoaW5o',
'LCBfID0gZ29pKHBhdGg9bm9pLCAgICAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoqa3cpICAgIyB0YWNoIGR1bmcgIC0+',
'IE5IQU4KICAgICAgICByX2R1b25nLCBfID0gZ29pKHBhdGg9c3RyKGQpLCAgICoqe3Rlbl9zZXA6IFRIVV9OMTB9LCAgICoq',
'a3cpICAgIyBkb2kgY2h1bmcgZHVvbmcKICAgICAgICByX3BoYW5iaWV0LCBfID0gZ29pKHBhdGg9bm9pLCAgICoqe3Rlbl9z',
'ZXA6IG9zLnBhdGhzZXB9LCAqKmt3KSAgIyB0YWNoIHRoZW8gb3MucGF0aHNlcCAtPiBtYXQKICAgIGtxID0geyJvcy5wYXRo',
'c2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogdGVuX3NlcCwgImRhdSB0aHUiOiBUSFVfTjEwLAogICAgICAgICAg',
'ZiJub2kgYmFuZyB7VEhVX04xMCFyfSwge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9IjogICAgICAgIk5IQU4iIGlmIHJfY2hpbmgg',
'ZWxzZSAiTm9uZSIsCiAgICAgICAgICBmImRvaSBjaHVuZyBkdW9uZyAobW90IG11Yywge3Rlbl9zZXB9PXtUSFVfTjEwIXJ9',
'KSI6ICAiTkhBTiIgaWYgcl9kdW9uZyBlbHNlICJOb25lIiwKICAgICAgICAgIGYicGhhbiBiaWV0OiBub2kgYmFuZyB7VEhV',
'X04xMCFyfSwge3Rlbl9zZXB9PXtvcy5wYXRoc2VwIXJ9IjogIk5IQU4iIGlmIHJfcGhhbmJpZXQgZWxzZSAiTm9uZSJ9CiAg',
'ICBpZiBub3Qgcl9kdW9uZzoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IG1vdCBtdWMgaG9w',
'IGxlIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EKICAgICMgQ29uZyBwaGFpIENPIFRIRSBkby4gTmV1IGNhIGhhaSBk',
'YXUgcGhhbiBjYWNoIGRldSByYSBOSEFOIHRoaSBwaGVwIGRvIGtob25nIHBoYW4KICAgICMgYmlldCBkdW9jIGdpIOKAlCBk',
'dW5nIGJhbyBEQVQsIGJhbyB0aGFuZyBsYSBraG9uZyBkbyBkdW9jLgogICAgaWYgcl9waGFuYmlldDoKICAgICAgICByZXR1',
'cm4gKEtERCwgZiJwaGVwIGRvIEtIT05HIHBoYW4gYmlldCBkdW9jOiBub2kgYmFuZyB7VEhVX04xMCFyfSBtYSB0YWNoIHRo',
'ZW8gIgogICAgICAgICAgICAgICAgICAgICBmIntvcy5wYXRoc2VwIXJ9IFZBTiB0aW0gcmEgZ2l0LmV4ZSIsIGtxKQogICAg',
'cmV0dXJuICgoREFULCAiIiwga3EpIGlmIHJfY2hpbmggZWxzZQogICAgICAgICAgICAoVFJVT1QsIGYidGFjaCB0aGVvIG9z',
'LnBhdGhzZXAgdGhheSB2aSB0aGVvIHt0ZW5fc2VwfSBkdW9jIHRydXllbiIsIGtxKSkKCgpkZWYgZG9fbjExKGdvaSwgc2ln',
'LCB0ZXB0KToKICAgICIiIlRydXllbiBjaGFuX2RvYW4gPT4gdGh1IGR1b2MgdGhvbmcgYmFvIFZBIHN0ZGVyciBJTS4gS2hv',
'bmcgdHJ1eWVuID0+IHN0ZGVyciBWQU4gY28uIiIiCiAgICBpZiAiY2hhbl9kb2FuIiBub3QgaW4gc2lnLnBhcmFtZXRlcnM6',
'CiAgICAgICAgcmV0dXJuIEtERCwgIl9naXRfd2luZG93cyBraG9uZyBuaGFuIHRoYW0gc28gY2hhbl9kb2FuIiwgeyJ0aGFt',
'IHNvIjogbGlzdChzaWcucGFyYW1ldGVycyl9CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6',
'CiAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgIChkLyJnaXQuZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29k',
'aW5nPSJ1dGYtOCIpCiAgICAgICAgY2QgPSBbXQogICAgICAgIF8sIGVfY28gPSBnb2kocGF0aD1zdHIoZCksIHByb2dyYW1f',
'ZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdyksIGNoYW5fZG9hbj1jZCkKICAgICAgICBfLCBlX2toID0gZ29pKHBhdGg9c3Ry',
'KGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAga3EgPSB7ImNoYW5fZG9hbiB0aHUgZHVvYyAo',
'bXVjKSI6IGxlbihjZCksCiAgICAgICAgICAic3RkZXJyIGtoaSBDTyBjaGFuX2RvYW4gKGJ5dGUpIjogbGVuKGVfY28uZW5j',
'b2RlKCkpLAogICAgICAgICAgInN0ZGVyciBraGkgS0hPTkcgdHJ1eWVuIChieXRlKSI6IGxlbihlX2toLmVuY29kZSgpKX0K',
'ICAgIGlmIGxlbihjZCkgPT0gMCBhbmQgbGVuKGVfa2guZW5jb2RlKCkpID09IDA6CiAgICAgICAgcmV0dXJuIEtERCwgIm5o',
'YW5oICVQcm9ncmFtRmlsZXMlIGtob25nIHBoYW4gZ2lhaSBLSE9ORyBiYXkgcmEgY2hhbiBkb2FuIG5hbyAtPiBjaHVhIGRv',
'IGR1b2MiLCBrcQogICAgb2sgPSBsZW4oY2QpID4gMCBhbmQgbGVuKGVfY28uZW5jb2RlKCkpID09IDAgYW5kIGxlbihlX2to',
'LmVuY29kZSgpKSA+IDAKICAgIHJldHVybiAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJh',
'bmciKSwga3EKCmRlZiBkb19uMTIoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiSGFuZyBzZW50aW5lbCBnaXRfcGF0aCB0cm9u',
'ZyBmaXh0dXJlIHBoYWkgdHV5ZXQgZG9pIHRyZW4gQ0EgSEFJIG5lbi4iIiIKICAgIG5kID0gdGVwdC5yZWFkX3RleHQoZW5j',
'b2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIikKICAgIGhhbmcgPSBzb3J0ZWQoc2V0KHJlLmZpbmRhbGwocidnaXRf',
'cGF0aFxzKj1ccyoiKFteIl0rKSInLCBuZCkpKQogICAgeGF1ID0gW2ggZm9yIGggaW4gaGFuZyBpZiBub3QgKFB1cmVQb3Np',
'eFBhdGgoaCkuaXNfYWJzb2x1dGUoKSBhbmQgUHVyZVdpbmRvd3NQYXRoKGgpLmlzX2Fic29sdXRlKCkpXQogICAga3EgPSB7',
'ImhhbmcgZ2l0X3BhdGggdGltIHRoYXkiOiBoYW5nLCAiY2hpIHR1eWV0IGRvaSBNT1QgbmVuIjogeGF1fQogICAgaWYgbm90',
'IGhhbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImtob25nIHRpbSB0aGF5IGhhbmcgZ2l0X3BhdGggbmFvIHRyb25nIGZpeHR1',
'cmUgLT4gbWF1IGRvYyBjbyB0aGUgZGEgZG9pIiwga3EKICAgIHJldHVybiAoREFUIGlmIG5vdCB4YXUgZWxzZSBUUlVPVCks',
'ICgiIiBpZiBub3QgeGF1IGVsc2UgZiJjaGktbW90LW5lbjoge3hhdX0iKSwga3EKClBST0JFID0gWygiTjggYnVvYyAxIGNo',
'aSBuaGFuIGdpdC5leGUiLCBkb19uOCksCiAgICAgICAgICgiTjkgYm9jIG5oYXkga2VwIG8gbXVjIFBBVEgiLCBkb19uOSks',
'CiAgICAgICAgICgiTjEwIGRhdSAnOycgdHJvbmcgdGVuIHRodSBtdWMiLCBkb19uMTApLAogICAgICAgICAoIk4xMSBjaGFu',
'IGRvYW4gZG9pIGtlbmgiLCBkb19uMTEpLAogICAgICAgICAoIk4xMiBoYW5nIHNlbnRpbmVsIHR1eWV0IGRvaSBDQSBIQUkg',
'bmVuIiwgZG9fbjEyKV0KCiMgLS0tIGNoZSBkbyBUVSBLSUVNOiBjaGF5IG5hbSBwcm9iZSB0cmVuIG1vdCBjYXkgYmF0IGt5',
'LCBuZW4gYmF0IGt5IC0tLQppZiAiLS10dS1raWVtLXByb2JlIiBpbiBzeXMuYXJndjoKICAgIF9nID0gUGF0aChzeXMuYXJn',
'dltzeXMuYXJndi5pbmRleCgiLS10dS1raWVtLXByb2JlIikgKyAxXSkucmVzb2x2ZSgpCiAgICBfc3AgPSBpbXBvcnRsaWIu',
'dXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfdGsiLCBzdHIoX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiKSkK',
'ICAgIF9scCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVsZShf',
'bHApCiAgICBfc2lnID0gaW5zcGVjdC5zaWduYXR1cmUoX2xwLl9naXRfd2luZG93cykKICAgIGRlZiBfZ29pKCoqa3cpOgog',
'ICAgICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAg',
'ICAgICAgICAgcmV0dXJuIF9scC5fZ2l0X3dpbmRvd3MoKiprdyksIGUuZ2V0dmFsdWUoKQogICAgcHJpbnQoZiJUVSBLSUVN',
'IFBST0JFIHRyZW4ge19nfSAgKG5lbiB7c3lzLnBsYXRmb3JtfSkiKQogICAgZm9yIF90ZW4sIF9mIGluIFBST0JFOgogICAg',
'ICAgIF90dCwgX2N0LCBfZGwgPSBfZihfZ29pLCBfc2lnLCBfZy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAg',
'ICAgICBwcmludChmIiAgW3tfdHQ6MTR9XSB7X3Rlbn0iICsgKGYiICAge19jdH0iIGlmIF9jdCBlbHNlICIiKSkKICAgICAg',
'ICBmb3IgX2ssIF92IGluIChfZGwgb3Ige30pLml0ZW1zKCk6IHByaW50KGYiICAgICAgICB7X2s6MzR9OiB7X3Z9IikKICAg',
'IHN5cy5leGl0KDApCgojIC0tLSBjaGUgZG8gS0lFTSBET05HIEJPOiB0ZXAgLnB5IG5heSBwaGFpIFRSVU5HIFRVTkcgQllU',
'RSB2b2kgYmFuIG5odW5nIHRyb25nIHBzMSAtLS0KIyBLaG9uZyBjb25nIG5hbyBidW9jIGhhaSBiYW4gc2FvIGtob3A6IGRv',
'IGR1b2MsIG5vaSB0cmFuIDIvNDAwIC0+IDk5Lzk5OTk5IENISSB0cm9uZyAucHkKIyB0aGkgY2lfZGFuZ19reSBsYW4gdDI2',
'L3QyNyB2YW4geGFuaCwgY29uIGNob3QgU0hBIGN1YSBwczEgY2hpIHNvIGJhbiBuaHVuZyB2b2kgaGFuZyBzbwojIGN1YSBD',
'SElOSCBuby4gQ2hheTogcHl0aG9uIHdwNTQxLWRvLWcyLXdpbmRvd3MucHkgLS1raWVtLWRvbmctYm8gd3A1NDEtZG8tZzIu',
'cHMxICAocmMgMHwzKQppZiAiLS1raWVtLWRvbmctYm8iIGluIHN5cy5hcmd2OgogICAgaW1wb3J0IGJhc2U2NAogICAgX3Bz',
'ID0gUGF0aChzeXMuYXJndltzeXMuYXJndi5pbmRleCgiLS1raWVtLWRvbmctYm8iKSArIDFdKS5yZWFkX3RleHQoZW5jb2Rp',
'bmc9ImFzY2lpIikKICAgIF9tID0gcmUuc2VhcmNoKHIiKD9tcyleXCRCNjQgPSBAXCgoLio/KV5cKSIsIF9wcykKICAgIF9r',
'ID0gcmUuc2VhcmNoKHIiKD9tKV5cJFNoYUJvRG9ccyo9XHMqJyhbMC05YS1mXXs2NH0pJyIsIF9wcykKICAgIF9uaHVuZyA9',
'IGJhc2U2NC5iNjRkZWNvZGUoIiIuam9pbihyZS5maW5kYWxsKHIiJyhbQS1aYS16MC05Ky89XSopJyIsIF9tLmdyb3VwKDEp',
'KSkpIGlmIF9tIGVsc2UgYiIiCiAgICBfdG9pID0gUGF0aChfX2ZpbGVfXykucmVhZF9ieXRlcygpCiAgICBfb2sgPSBib29s',
'KF9tIGFuZCBfaykgYW5kIF9uaHVuZyA9PSBfdG9pIGFuZCBoYXNobGliLnNoYTI1NihfdG9pKS5oZXhkaWdlc3QoKSA9PSBf',
'ay5ncm91cCgxKQogICAgaW5uKGYiS0lFTSBET05HIEJPOiB7REFUIGlmIF9vayBlbHNlIEtERH0gIChuaHVuZyB7bGVuKF9u',
'aHVuZyl9IGJ5dGUsIHRlcCB7bGVuKF90b2kpfSBieXRlKSIpCiAgICBzeXMuZXhpdCgwIGlmIF9vayBlbHNlIDMpCgppbm4o',
'Ij0iICogNzgpOyBpbm4oIldQNTQxIGcyIC0gcGhlcCBkbyB0cmVuIFdpbmRvd3MgdGhhdCAoc3BlYyByMzogTjEtTjQsIE44',
'LU4xMiwgTjcsIGtpY2ggdGh1b2MpIik7IGlubigiPSIgKiA3OCkKCiMgLS0tLS0tLS0tLS0tLS0tLSB0dSBraWVtIGJvIGRv',
'YyAtLS0tLS0tLS0tLS0tLS0tCl9kLCBfZywgX3QgPSBkb2NfZG8oX01BVSkKX29rID0gKGxlbihfZCkgPT0gMiBhbmQgYW55',
'KHguc3RhcnRzd2l0aCgidDAyYiIpIGZvciB4IGluIF9kKQogICAgICAgYW5kIG5vdCBhbnkoeC5zdGFydHN3aXRoKCJ0MTMx',
'IikgZm9yIHggaW4gX2QpIGFuZCBfdCkKaW5uKCJUdSBraWVtIGJvIGRvYyBsb2c6IiwgREFUIGlmIF9vayBlbHNlIFRSVU9U',
'KQppZiBub3QgX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBibyBkb2MgbG9nIGN1YSBjaGluaCBzY3Jp',
'cHQgbmF5IHNhaSAtPiBraG9uZyBkbyBnaSBjYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLS0tLS0tLSAwLiBuZW4g',
'ZG8gLS0tLS0tLS0tLS0tLS0tLQpnb2MgPSBQYXRoKHN5cy5hcmd2WzFdKS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+',
'IDEgZWxzZSBQYXRoLmN3ZCgpCnRlcCwgdGVwdCA9IGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiLCBnb2MgLyAi',
'b3BzIiAvICJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMC4gTkVOIERPIikK',
'IyBNT0kgTE9HIFBIQUkgVFUgS0hBSSBubyBkbyBDQUkgR0kgYmFuZyBCTyBETyBOQU8uIEJhaSBob2MgMTktMDktMjAyNjog',
'bW90IGx1b3QgZG8KIyBndWkgdmUgZHVvYyBkb2Mgbmh1IGtldCBxdWEgY3VhIGJhbiB2YSBkYW5nIHhldCwgbmh1bmcgdGhh',
'dCByYSBsYSBiYW4gZG8gQ1UgY2hheQojIHRyZW4gbmhhbmggS0hBQy4gRG9jIHJhIHRoaSBtYXQgbW90IHZvbmc7IGxvZyB0',
'dSBraGFpIHRoaSB0aGF5IG5nYXkgZG9uZyBkYXUuCnRyeToKICAgIF90dSA9IGhhc2hsaWIuc2hhMjU2KFBhdGgoX19maWxl',
'X18pLnJlYWRfYnl0ZXMoKSkuaGV4ZGlnZXN0KCkKZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgIF90dSA9IGYia2hvbmcg',
'dHUgYmFtIGR1b2M6IHtfZX0iCmdoaSgiYm9fZG9fc2hhMjU2IiwgX3R1KQppbm4oZiIgIEJPIERPICAgICAgICA6IHNoYTI1',
'NiB7X3R1WzoxNl19ICAoYmFuIHtCQU5fQk9fRE99KSIpCmlubigiICBzeXMucGxhdGZvcm0gOiIsIHN5cy5wbGF0Zm9ybSwg',
'InwgcHl0aG9uIiwgc3lzLnZlcnNpb24uc3BsaXQoKVswXSkKaW5uKCIgIG9zLnBhdGhzZXAgICA6IiwgcmVwcihvcy5wYXRo',
'c2VwKSwgInwgUEFUSEVYVDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQQVRIRVhUIikpWzo2MF0pCmlubigiICBQcm9ncmFt',
'RmlsZXMgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlByb2dyYW1GaWxlcyIpKSwgInwgU3lzdGVtUm9vdDoiLCByZXByKG9z',
'LmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290IikpKQppbm4oIiAgQ09OR19DVV9HSVQgIDoiLCByZXByKG9zLmVudmlyb24uZ2V0',
'KCJDT05HX0NVX0dJVCIpKSkKaW5uKCIgIGdvYyBraG8gICAgICA6IiwgZ29jKQoKcXV5ZW4gPSBOb25lCmlmIHN5cy5wbGF0',
'Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAgIGltcG9ydCBjdHlwZXM7IHF1eWVuID0gYm9vbChjdHlwZXMud2lu',
'ZGxsLnNoZWxsMzIuSXNVc2VyQW5BZG1pbigpKQogICAgZXhjZXB0IEV4Y2VwdGlvbjogcXV5ZW4gPSBOb25lCmdoaSgicXV5',
'ZW5fYWRtaW4iLCBxdXllbikKc3ltbGlua19kdW9jID0gTm9uZQp0cnk6CiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURp',
'cmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZCA9IFBhdGgodCkvImEudHh0IjsgZC53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9',
'InV0Zi04IikKICAgICAgICB0cnk6IG9zLnN5bWxpbmsoc3RyKGQpLCBzdHIoUGF0aCh0KS8ibGsiKSk7IHN5bWxpbmtfZHVv',
'YyA9IFRydWUKICAgICAgICBleGNlcHQgT1NFcnJvciBhcyBlOiBzeW1saW5rX2R1b2MgPSBGYWxzZTsgZ2hpKCJzeW1saW5r',
'X2xvaSIsIGYie3R5cGUoZSkuX19uYW1lX199OiB7ZX0iKQpleGNlcHQgRXhjZXB0aW9uIGFzIGU6IGdoaSgic3ltbGlua19s',
'b2kiLCBzdHIoZSkpCmdoaSgic3ltbGlua19kdW9jIiwgc3ltbGlua19kdW9jKQppbm4oIiAgQWRtaW5pc3RyYXRvcjoiLCBx',
'dXllbiwgInwgdGFvIHN5bWxpbmsgZHVvYzoiLCBzeW1saW5rX2R1b2MpCgpsb2kgPSBbXQojIENvbmcga2ljaCB0aHVvYyBs',
'YSBwaGVwIGRvIHRyZW4gTElDSCBTVSBHSVQsIGtob25nIGRpbmggZ2kgZGVuIG5lbi4gQ2hvIHBoZXAKIyAtLWNoaS1raWNo',
'LXRodW9jIGNoYXkgbyBtb2kgbmVuIGRlIGNvbiBUVSBLSUVNIGR1b2MgY2hpbmggY29uZyBuYXkgKGRhIGR1bmcKIyBkZSB0',
'YWkgZHVuZyBjYSBoYWkgdmUgY3VhIHN1IGNvIG5lbi1jdSAxOS0wOSkuIE1vaSBjaG90IENIVUMgTkFORyB2YW4gZG9pIFdp',
'bmRvd3MuCmlmIHN5cy5wbGF0Zm9ybSAhPSAid2luMzIiIGFuZCAiLS1jaGkta2ljaC10aHVvYyIgbm90IGluIHN5cy5hcmd2',
'OgogICAgbG9pLmFwcGVuZChmIktIT05HIHBoYWkgV2luZG93cyAoc3lzLnBsYXRmb3JtPXtzeXMucGxhdGZvcm0hcn0pIikK',
'aWYgbm90IHRlcC5pc19maWxlKCk6ICBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwfSIpCmlmIG5vdCB0ZXB0LmlzX2Zp',
'bGUoKTogbG9pLmFwcGVuZChmImtob25nIHRoYXkge3RlcHR9IikKaWYgbm90IHNodXRpbC53aGljaCgiZ2l0Iik6IGxvaS5h',
'cHBlbmQoImtob25nIGNvIGBnaXRgIHRyb25nIFBBVEgiKQojIEJvIHRlc3QgKG11YyAyIHZhIE43KSBjYW4gUHlZQU1MOiB0',
'aGlldSBubywgMGVhOTVkZSByYSA5Ni8xNjYgY2EgRE8gKDg5IGJhbyB0aGFuZyAiTm8gbW9kdWxlIG5hbWVkICd5YW1sJyIs',
'CiMgNyBxdWEgbHVvdCBjb247IGNvIFB5WUFNTDogMTY2LzE2NiBRVUEpLiBCbyBkbyBnb2kgY2h1bmcgbGEgImNhIERPIExB',
'IiByb2kgcGhhdCBUUlVPVCDigJQgZG8gdHJlbiAyMDI2LTA5LTMwYy4KIyBEaWV1IGtpZW4gdGllbiBxdXlldCBwaGFpIGhv',
'aSBiYW5nIENISU5IIHRpZW4gdHJpbmggY29uIHNlIGNoYXkgYm8gdGVzdCAoY2hheSgpOiBjdW5nIG1vaSB0cnVvbmc7IGN3',
'ZCA9IG9wcy8gPQojIHN5cy5wYXRoWzBdIGN1YSBibyB0ZXN0KSB2YSBob2kgRFVORyBEVU9DIGNodSBraG9uZyBob2kgQ08g',
'TUFULiBCYW4gMzBkIGhvaSBgZmluZF9zcGVjKCJ5YW1sIilgIG8gdGllbiB0cmluaAojIE5BWSB2YSBuZ3VvbmcgMy44IHN1',
'eSB0dSBOR1UgUEhBUCAoYDo9YCkg4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGQsIGNhIGhhaSByYSByYz0xIFRSVU9UIGNobyB1',
'bmcgdmllbiBzYWNoOgojIHRodSBtdWMgZHUgbGlldSBgeWFtbC9gIHRyZW4gUFlUSE9OUEFUSCBxdWEgZmluZF9zcGVjIG1h',
'IGB5YW1sLnNhZmVfZHVtcGAga2hvbmcgY28gKDg3IGNhICJsYSIpOyBweXRob24gMy44LjIwCiMgVEhBVCBjbyBQeVlBTUws',
'IGJvIHRlc3QgZHVuZyBgc3RyLnJlbW92ZXByZWZpeGAgKDMuOSkgbHVjIENIQVkgKDMzIGNhICJsYSI7IDMuOS4yMzogMTY2',
'LzE2NikuCmlmIG5vdCAoIi0tY2hpLWtpY2gtdGh1b2MiIGluIHN5cy5hcmd2IG9yICItLWNoaS1wcm9iZSIgaW4gc3lzLmFy',
'Z3YpOgogICAgX3JjX2RrLCBfcmFfZGsgPSBjaGF5KFsiLWMiLCAiaW1wb3J0IHN5czsgc3lzLmV4aXQoOSkgaWYgc3lzLnZl',
'cnNpb25faW5mbyA8ICgzLCA5KSBlbHNlIE5vbmU7IGltcG9ydCB5YW1sOyIKICAgICAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgIiB5YW1sLnNhZmVfZHVtcCh5YW1sLnNhZmVfbG9hZCgnYTogMScpKSJdLAogICAgICAgICAgICAgICAgICAgICAg',
'ICAgIGdvYyAvICJvcHMiIGlmIChnb2MgLyAib3BzIikuaXNfZGlyKCkgZWxzZSBQYXRoLmN3ZCgpLCBwaHV0PTIpCiAgICBp',
'ZiBfcmNfZGsgPT0gOToKICAgICAgICBsb2kuYXBwZW5kKGYicHl0aG9uIHtzeXMudmVyc2lvbi5zcGxpdCgpWzBdfSA8IDMu',
'OTogYm8gdGVzdCBjdWEgdW5nIHZpZW4gZHVuZyBzdHIucmVtb3ZlcHJlZml4ICgzLjkpIGx1YyBDSEFZIikKICAgIGVsaWYg',
'X3JjX2RrOgogICAgICAgIGxvaS5hcHBlbmQoZiJweXRob24gbmF5IEtIT05HIGNvIFB5WUFNTCBkdW5nIGR1b2MgKHsoX3Jh',
'X2RrLnN0cmlwKCkuc3BsaXRsaW5lcygpIG9yIFsnJ10pWy0xXVs6OTBdfSk6IgogICAgICAgICAgICAgICAgICAgZiIgXCJ7',
'c3lzLmV4ZWN1dGFibGV9XCIgLW0gcGlwIGluc3RhbGwgcHl5YW1sIgogICAgICAgICAgICAgICAgICAgIiAoYmFuIG5odW5n',
'IHBzMSB0dSB0YWkgS0hPTkcgY28gcGlwOiBjaGF5IGxhaSB2b2kgLVB5IDxweXRob24gZGEgY28gUHlZQU1MPikiKQoKcmMs',
'IGhlYWQsIF8gPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIkhFQUQiKQppZiByYzogbG9pLmFwcGVuZCgia2hvbmcgZG9jIGR1',
'b2MgSEVBRCIpCmdoaSgiaGVhZCIsIGhlYWQpCnJjX2EsIF8sIF8gPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICItLWlzLWFu',
'Y2VzdG9yIiwgU0hBX0cxLCBoZWFkIG9yICJIRUFEIikKbGFfaGF1X2R1ZSA9IChyY19hID09IDApCmlmIGhlYWQgPT0gU0hB',
'X0cxOgogICAgdGhlX2hlID0gImcxIjsgaW5uKGYiICBIRUFEID0ge2hlYWRbOjhdfSAtPiBEQVkgTEEgZzEuIENIVUEgY28g',
'YmFuIHZhIGcyOyBrZXQgcXVhIGR1b2kgbGEgTkVOIERPLiIpCmVsaWYgbGFfaGF1X2R1ZToKICAgIHRoZV9oZSA9ICJnMiI7',
'IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gaGF1IGR1ZSBjdWEgZzEgKHtTSEFfRzFbOjhdfSk7IHVuZyB2aWVuIGcy',
'IGhheSBraG9uZzogTjcnIChtdWMgMSkgZGluaCBkYW5oLiIpCmVsc2U6CiAgICB0aGVfaGUgPSAiPyI7IGxvaS5hcHBlbmQo',
'ZiJIRUFEPXtoZWFkWzo4XX0gS0hPTkcgcGhhaSBnMSB2YSBLSE9ORyBwaGFpIGhhdSBkdWUgY3VhIHtTSEFfRzFbOjhdfSDi',
'gJQgcmViYXNlPyBuaGFtIG5oYW5oPyIpCmdoaSgidGhlX2hlIiwgdGhlX2hlKQpyY19yLCByZWZzLCBfID0gZ2l0KGdvYywg',
'ImZvci1lYWNoLXJlZiIsICItLXBvaW50cy1hdCIsIGhlYWQgb3IgIkhFQUQiLAogICAgICAgICAgICAgICAgICAgICItLWZv',
'cm1hdD0lKHJlZm5hbWU6c2hvcnQpIikKZHNyID0gW3ggZm9yIHggaW4gcmVmcy5zcGxpdGxpbmVzKCkgaWYgeC5zdHJpcCgp',
'IGFuZCB4LnN0cmlwKCkgIT0gImRvLXRhbSJdCmdoaSgicmVmX3Ryb190b2lfaGVhZCIsIGRzcikKaW5uKGYiICByZWYgdHJv',
'IHRvaSBIRUFEOiB7JywgJy5qb2luKGRzcikgaWYgZHNyIGVsc2UgJyhraG9uZyByZWYgbmFvIC0gSEVBRCByb2kgdHUgZG8p',
'J30iKQoKaWYgbG9pOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiBuZW4gZG8gc2FpLCBLSE9ORyBpbiBrZXQg',
'bHVhbiBuYW8uIikKICAgIGZvciB4IGluIGxvaTogaW5uKCIgIC0iLCB4KQogICAgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0t',
'LS0tLS0tLSAxLiBraWNoIHRodW9jIChONycgY3VhIHNwZWMgcjMpIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCIt',
'IiAqIDc4KTsgaW5uKCIxLiBLSUNIIFRIVU9DIOKAlCB0cmFuIHNwZWMgcjM6IDw9IDIgdGVwIHZhIDw9IDQwMCBkb25nIHRo',
'ZW0iKQojIFZFIE5FTiBQSEFJIFRVT0kg4oCUIHZhIHBoYWkgQ0hVTkcgTUlOSCBkdW9jIGxhIHR1b2ksIGtob25nIHBoYWkg',
'Z2lhIGRpbmguCiMgQmFpIGhvYyB0cmEgZ2lhIDE5LTA5LTIwMjY6IGNsb25lIHRhaSBkdW5nIGNoaSBmZXRjaCBuaGFuaCBi',
'YW4gdmEsIGBvcmlnaW4vbWFzdGVyYAojIGR1bmcgeWVuIHR1IDE0LTA5IChjMTZiZDMyLCBzYXUgOTcgY29tbWl0KS4gbWVy',
'Z2UtYmFzZSByb2kgdmUgZHVuZyBkaW5oIG1hc3RlciBjdSwKIyBuZW4gZGlmZiBOVU9UIGNhIDk3IGNvbW1pdCBtYXN0ZXI6',
'IGRvIHJhIDQ2IHRlcCAvICs3MTE4IHRoYXkgdmkgMiB0ZXAgLyArMzk3IOKAlAojIENVTkcgTU9UIENPTU1JVCAwZWE5NWRl',
'LiBNb3QgdGlldSBjaGkgREVMVEEgbWEgdmUgbmVuIGtob25nIHR1b2kgdGhpIGtob25nIHNhaQojIGxlY2ggbW90IGNodXQs',
'IG5vIHNhaSBjYSBtb3QgYmFjIGRvIGxvbi4KIyBDaG8gbmVuOiBuZW4ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGxhIHR1b2kg',
'PT4gS0hPTkcgRE8gRFVPQyAocmM9MyksIEtIT05HIHBoYWkgVFJVT1QuCiMgVFJVT1QgbGEgbW90IFBIQU4gUVVZRVQgdmUg',
'YmFuIHZhOyBwaGFuIHF1eWV0IGNoaSBkdW9jIHBoZXAgcGhhdCByYSBraGkgZGEgZG8gZHVvYy4KcmNfdSwgdXJsX3Robywg',
'XyA9IGdpdChnb2MsICJyZW1vdGUiLCAiZ2V0LXVybCIsICJvcmlnaW4iKQp1cmxfbywgdXJsX2luID0gX3VybF9zYWNoKHVy',
'bF90aG8pLCBfdXJsX2luKHVybF90aG8pCmdoaSgib3JpZ2luX3VybCIsIHVybF9pbik7IGlubihmIiAgb3JpZ2luICAgICAg',
'IDoge3VybF9pbiBvciAnKGtob25nIGRvYyBkdW9jKSd9IikKdXJsX29rID0gKG5vdCByY191KSBhbmQgdXJsX28ucnN0cmlw',
'KCIvIikgaW4gVVJMX0tIT19IT1BfTEUKcmNfbHIsIG91dF9sciwgZXJfbHIgPSBnaXQoZ29jLCAibHMtcmVtb3RlIiwgIm9y',
'aWdpbiIsICJyZWZzL2hlYWRzL21hc3RlciIpIGlmIHVybF9vayBlbHNlICgxLCAiIiwgIiIpCmVyX2xyID0gX2FuX3VzZXJp',
'bmZvKGVyX2xyKQpyY19sbSwgbG0sIGVyX2xtICAgICA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAib3JpZ2luL21hc3RlciIp',
'CnJtID0gb3V0X2xyLnNwbGl0KClbMF0gaWYgKG5vdCByY19sciBhbmQgb3V0X2xyLnN0cmlwKCkpIGVsc2UgIiIKaWYgbm90',
'IHVybF9vazoKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYib3JpZ2luPXt1cmxfaW4hcn0gS0hPTkcgcGhhaSBr',
'aG8gdGhhdCDigJQgJ3R1b2knIHNvIHZvaSBubyBraG9uZyBjaHVuZyBtaW5oIGR1b2MgZ2kiKQogICAgcmNfbWIsIG1iLCBu',
'cywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBub3Qgcm06CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAogICAgICAg',
'IGYia2hvbmcgaG9pIGR1b2MgbWFzdGVyIHRyZW4gcmVtb3RlIChscy1yZW1vdGUgcmM9e3JjX2xyfSk6IHtlcl9scls6NjBd',
'fSAiCiAgICAgICAgZiLigJQga2hvbmcgY2h1bmcgbWluaCBkdW9jIHZlIG5lbiBjb24gdHVvaSIpCiAgICByY19tYiwgbWIs',
'IG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIHJjX2xtIG9yIG5vdCBsbToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBL',
'REQsIGYia2hvbmcgZG9jIGR1b2Mgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZToge2VyX2xtWzo2MF19IikKICAgIHJjX21i',
'LCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbG0gIT0gcm06CiAgICAjIERlbSB4ZW0gdHV0IGxhaSBiYW8geGEs',
'IG5ldSBkZW0gZHVvYyDigJQgY29uIHNvIG5heSBub2kgcm8gbXVjIGRvIHNhaSBsZWNoLgogICAgcmNfYywgc2F1LCBfID0g',
'Z2l0KGdvYywgInJldi1saXN0IiwgIi0tY291bnQiLCBmIntsbX0uLntybX0iKQogICAgeGEgPSBmIiwgdHV0IGxhaSB7c2F1',
'fSBjb21taXQiIGlmIChub3QgcmNfYyBhbmQgc2F1LnN0cmlwKCkuaXNkaWdpdCgpKSBlbHNlICIiCiAgICBpbm4oZiIgIG9y',
'aWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmUgOiB7bG1bOjEyXX0iKQogICAgaW5uKGYiICBtYXN0ZXIgdHJlbiByZW1vdGUgICAg',
'ICAgIDoge3JtWzoxMl19e3hhfSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwg',
'cm0pCiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELAogICAgICAgIGYidmUgbmVuIENVOiBvcmlnaW4vbWFzdGVyPXts',
'bVs6MTJdfSAhPSByZW1vdGU9e3JtWzoxMl19e3hhfSAiCiAgICAgICAgZiLigJQgY2hheSBgZ2l0IC1DIDxraG8+IGZldGNo',
'IG9yaWdpbiBtYXN0ZXJgIHJvaSBkbyBsYWkiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxzZToK',
'ICAgIGlubihmIiAgdmUgbmVuIFRVT0k6IG9yaWdpbi9tYXN0ZXIgPSB7bG1bOjEyXX0gPT0gbWFzdGVyIHRyZW4gcmVtb3Rl',
'IikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIHJjX21iLCBtYiwg',
'ZXJfbWIgPSBnaXQoZ29jLCAibWVyZ2UtYmFzZSIsICJvcmlnaW4vbWFzdGVyIiwgaGVhZCkKaWYgcmNfbWIgb3Igbm90IG1i',
'OgogICAgaWYgbWIgPT0gIiIgYW5kIHJtIGFuZCBsbSA9PSBybToKICAgICAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RE',
'LCBmImtob25nIHRpbmggZHVvYyBtZXJnZS1iYXNlIHZvaSBvcmlnaW4vbWFzdGVyOiB7ZXJfbWJbOjcwXX0iKQogICAgbnMs',
'IHJjID0gIiIsIDEKZWxzZToKICAgIGdoaSgibWVyZ2VfYmFzZSIsIG1iKQogICAgaW5uKGYiICBtZXJnZS1iYXNlKG9yaWdp',
'bi9tYXN0ZXIsIEhFQUQpID0ge21iWzoxMl19IikKICAgIGlmIG1iICE9IFNIQV9CQVNFX1NQRUM6CiAgICAgICAgaW5uKGYi',
'ICBMVVUgWToga2hhYyBiYXNlIG1hIHNwZWMgcjMga2hhaSAoe1NIQV9CQVNFX1NQRUNbOjEyXX0pIOKAlCB2aSBuaGFuaCBk',
'YSBtZXJnZSBtYXN0ZXIuIikKICAgICAgICBpbm4oIiAgICAgICAgIERvIHNvIGJhc2UgY3Ugc2UgTlVPVCBwaGFuIG1hc3Rl',
'ciBtYW5nIHZhby4gRHVuZyBtZXJnZS1iYXNlIG1vaSBsYSB2aWVjIGN1YSBleGVjdXRvci4iKQogICAgICAgIHJjX3gsIG5z',
'X3gsIF8gPSBnaXQoZ29jLCAiZGlmZiIsICItLW51bXN0YXQiLCBTSEFfQkFTRV9TUEVDLCBoZWFkKQogICAgICAgIGlmIG5v',
'dCByY194OgogICAgICAgICAgICBoID0gW2wuc3BsaXQoIlx0IikgZm9yIGwgaW4gbnNfeC5zcGxpdGxpbmVzKCkgaWYgbC5z',
'dHJpcCgpXQogICAgICAgICAgICBhID0gc3VtKGludCh4WzBdKSBmb3IgeCBpbiBoIGlmIHhbMF0uaXNkaWdpdCgpKQogICAg',
'ICAgICAgICBnaGkoIm51bXN0YXRfdGhlb19iYXNlX3NwZWMiLCB7InRlcCI6IGxlbihoKSwgInRoZW0iOiBhfSkKICAgICAg',
'ICAgICAgaW5uKGYiICAgICAgICAgKGRvaSBjaGlldTogc28gYmFzZSBzcGVjID0ge2xlbihoKX0gdGVwIC8gK3thfSDigJQg',
'Y29uIHNvIGF5IEtIT05HIGR1bmcgZGUgY2hhbSkiKQogICAgcmMsIG5zLCBlciA9IGdpdChnb2MsICJkaWZmIiwgIi0tbnVt',
'c3RhdCIsIG1iLCBoZWFkKQppZiByYzoKICAgIHBhc3MKZWxzZToKICAgIGhhbmcgPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBp',
'biBucy5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAgdGhlbSA9IHN1bShpbnQoaFswXSkgZm9yIGggaW4gaGFuZyBp',
'ZiBoWzBdLmlzZGlnaXQoKSkKICAgIHhvYSAgPSBzdW0oaW50KGhbMV0pIGZvciBoIGluIGhhbmcgaWYgaFsxXS5pc2RpZ2l0',
'KCkpCiAgICBnaGkoInNvX3RlcCIsIGxlbihoYW5nKSk7IGdoaSgiZG9uZ190aGVtIiwgdGhlbSk7IGdoaSgiZG9uZ194b2Ei',
'LCB4b2EpCiAgICBmb3IgaCBpbiBoYW5nOiBpbm4oZiIgICAge2hbMl06MzR9ICt7aFswXTo8NX0gLXtoWzFdfSIpCiAgICBp',
'bm4oZiIgICAgVE9ORzoge2xlbihoYW5nKX0gdGVwLCAre3RoZW19LCAte3hvYX0gICAodHJhbjoge1RSQU5fVEVQfSB0ZXAg',
'LyB7VFJBTl9ET05HfSBkb25nIHRoZW0pIikKICAgIGNoYW0gPSBzb3J0ZWQoe2hbMl0gZm9yIGggaW4gaGFuZ30gJiBXUklU',
'RV9TRVRfRzIpOyBnaGkoImNoYW1fd3JpdGVfc2V0IiwgY2hhbSkKICAgIGRlZiBfY2FfbW9pX2NvKHJldik6CiAgICAgICAg',
'cl8sIG5kXywgXyA9IGdpdChnb2MsICJzaG93IiwgZiJ7cmV2fTpvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAg',
'ICByZXR1cm4gTm9uZSBpZiByXyBlbHNlIHt0IGZvciB0IGluIENBX01PSV9HMiBpZiByZS5zZWFyY2gociIoP20pXmRlZiAi',
'ICsgdCArIHIiW2Etel0/XyIsIG5kXyl9CiAgICBvX21iLCBvX2ggPSBfY2FfbW9pX2NvKG1iKSwgX2NhX21vaV9jbyhoZWFk',
'KQogICAgbWFuZyA9IHNvcnRlZChvX2ggLSBvX21iLCBrZXk9c29fY2EpIGlmIChvX21iIGlzIG5vdCBOb25lIGFuZCBvX2gg',
'aXMgbm90IE5vbmUpIGVsc2UgTm9uZQogICAgZ2hpKCJjYV9tb2lfZzJfbWFuZ192YW8iLCBtYW5nKQogICAgaWYgbm90IG1h',
'bmc6CiAgICAgICAgIyBEbyBST05HIChkYSBsYW5kLCBjaGluaCBtYXN0ZXIpLCBuaGFtIG5oYW5oLCBoYXkgbmhhbmggY3Vh',
'IHBhY2tldCBLSEFDIGNoYW0gY3VuZyB0ZXA6CiAgICAgICAgIyBraG9uZyBtYW5nIGNhIG1vaSBuYW8gY3VhIGcyIHRoaSBr',
'aG9uZyBwaGFpIHVuZyB2aWVuLiBEb2Mga2hvbmcgZHVvYyAoTm9uZSkgY3VuZyB2YXkuCiAgICAgICAga2V0KCJONycga2lj',
'aCB0aHVvYyIsIEtERCwgZiJkb2kgdHVvbmcga2hvbmcgcGhhaSB1bmcgdmllbjoge2xlbihoYW5nKX0gdGVwLCBjaGFtIHtj',
'aGFtfSwgY2EgbW9pICIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBmImcyIG1hbmcgdmFvIHttYW5nIXJ9',
'IOKAlCBkYSBsYW5kPyBuaGFtIG5oYW5oPyBwYWNrZXQga2hhYz8iKQogICAgZWxzZToKICAgICAgICBrZXQoIk43JyBraWNo',
'IHRodW9jIiwgREFUIGlmIChsZW4oaGFuZykgPD0gVFJBTl9URVAgYW5kIHRoZW0gPD0gVFJBTl9ET05HKSBlbHNlIFRSVU9U',
'LAogICAgICAgICAgICBmIntsZW4oaGFuZyl9IHRlcCAvICt7dGhlbX0iKQoKIyBEaW5oIGRhbmggVEhBVCBuYW0gbyBONycg',
'KGNhIG1vaSBnMiBtYW5nIHZhbyksIEtIT05HIG8gImhhdSBkdWUgZzEiOiBnMSBkYSBsYW5kIG5lbiBtb2kgbmhhbmggZGV1',
'CiMgbGEgaGF1IGR1ZS4gRG9uZyBkYXUga2hvaSBkYW4gcGhhaSB0dSBraGFpIHRoZW8ga2V0IHF1YSBheSAoZG8gZHVvYzog',
'bWFzdGVyIDQ0NjIwZTggbW8ga2hvaSBiYW5nCiMgIlRIRSBIRSBETyBEVU9DOiBnMiIsIEpTT04gInRoZV9oZSI6ICJnMiIs',
'IHRyb25nIGtoaSBONycgZGEga2V0IGx1YW4gImtob25nIHBoYWkgdW5nIHZpZW4iKS4KIyBOaGFuIGNoaSBkdW9jIG5vaSBE',
'VU5HIGNhaSBkbyBkdW9jOiBgW11gIGtob25nIHRhY2ggImRhIGxhbmQiIGtob2kgIm5oYW0gbmhhbmgiLyJwYWNrZXQga2hh',
'YyIgKGRvCiMgZHVvYyB0cmVuIDIwMjYtMDktMzBiOiB1bmcgdmllbiAyYTY3OTY4IERBIExBTkQgYmkgZ29pICJLSE9ORyBw',
'aGFpIHVuZyB2aWVuIGcyIikuCmlmIHRoZV9oZSA9PSAiZzIiIGFuZCBub3Qgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8i',
'KToKICAgIHRoZV9oZSA9ICgiS0hPTkcgbWFuZyBjYSBtb2kgZzIgbmFvIChkYSBsYW5kPyBuaGFtIG5oYW5oPyBwYWNrZXQg',
'a2hhYz8pIiBpZiBzby5nZXQoImNhX21vaV9nMl9tYW5nX3ZhbyIpID09IFtdCiAgICAgICAgICAgICAgZWxzZSAiZzI/IChD',
'SFVBIGRpbmggZGFuaCBkdW9jIGRvaSB0dW9uZykiKQogICAgZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCgojIENvbmcgbmhhbmg6',
'IGRvIFJJRU5HIGtpY2ggdGh1b2MgKHZhaSBnaWF5KSByb2kgZHVuZy4gRHVuZyBraGkgY2FuIHhhYyBtaW5oIGxhaQojIHZl',
'IG5lbiBtYSBraG9uZyBtdW9uIHRyYSAyMC00NSBwaHV0IGNobyBjYSBibyB0ZXN0LgppZiAiLS1jaGkta2ljaC10aHVvYyIg',
'aW4gc3lzLmFyZ3Y6CiAgICBpbm4oIiIpOyBpbm4oIj0iICogNzgpCiAgICBpbm4oIi0tY2hpLWtpY2gtdGh1b2M6IENISSBk',
'byBjb25nIGtpY2ggdGh1b2MuIERheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5naGllbSB0aHUuIikKICAgIGlubigiLSIgKiA3',
'OCkKICAgIGZvciBfdCwgX3R0LCBfY3QgaW4gY2hvdDogaW5uKGYiICB7X3R0OjE0fSB7X3R9IiArIChmIiAgIHtfY3R9IiBp',
'ZiBfY3QgZWxzZSAiIikpCiAgICBfayA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCiAgICBfciA9',
'IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKICAgIHN5cy5leGl0KDMgaWYgX2sgZWxzZSAoMSBp',
'ZiBfciBlbHNlIDApKQoKQ0hJX1BST0JFID0gIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndiAgICAjIGJvIHF1YSBibyB0ZXN0',
'ICsgTjc7IGdpdSAwLCAxLCAzCiMgLS0tLS0tLS0tLS0tLS0tLSAyLiBibyB0ZXN0IGRheSBkdSAtLS0tLS0tLS0tLS0tLS0t',
'CmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjIuIEJPIFRFU1QgREFZIERVICgx',
'MC00MCBwaHV0KSIpCiAgICByY19uLCBvdXRfbiA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIGdvYykK',
'ICAgIGdoaSgicmNfc3VpdGUiLCByY19uKQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dF9uKQogICAgaW5uKCIgIHJjID0i',
'LCByY19uLCAifCIsIG0uZ3JvdXAoMCkgaWYgbSBlbHNlICIoS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtldCkiKQogICAg',
'aWYgbToKICAgICAgICBnaGkoImRhdCIsIGludChtLmdyb3VwKDEpKSk7IGdoaSgidHJlbiIsIGludChtLmdyb3VwKDIpKSk7',
'IGdoaSgiYm9fcXVhX3NvIiwgaW50KG0uZ3JvdXAoNCkpKQogICAgZG9faGV0LCBnYywgdGluID0gZG9jX2RvKG91dF9uKQog',
'ICAgZ2hpKCJzb19jYV9kbyIsIGxlbihkb19oZXQpKTsgZ2hpKCJsaWV0X2tlX2RheV9kdSIsIHRpbikKICAgIGZvciBnIGlu',
'IGdjOiBpbm4oIiAgICoiLCBnKQogICAgaW5uKCIiKTsgaW5uKGYiICA9PT0ge2xlbihkb19oZXQpfSBDQSBETyA9PT0iKQog',
'ICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAgICBpbm4oZiIgICB7dC5zcGxpdCgnXycpWzBd',
'Ojd9IHt0fSIpOyBpbm4oZiIgICAgICAgICAgIHtkb19oZXRbdF1bOjE1MF19IikKICAgIGdoaSgiZG9fbHlfZG8iLCB7dDog',
'ZG9faGV0W3RdWzozMDBdIGZvciB0IGluIGRvX2hldH0pCiAgICAjIC0tLS0gQ0hPVDogbW9pIGNhIERPIHBoYWkgR0lBSSBU',
'SElDSCBEVU9DIC0tLS0KICAgICMgVGhpZXUgY2hvdCBuYXksIGJvIGRvIGluIGRhbmggc2FjaCBkbyByb2kgdmFuIHRob2F0',
'IHJjPTAuIERvIGR1bmcgbGEgbG9pIGRhIHhheSByYToKICAgICMgbHVvdCBXaW5kb3dzIDE5LTA5IGNvIHQxNzEgRE8gbWEg',
'Ym8gZG8gYmFvICJEQVQgMTAgfCBUUlVPVCAwIiB2YSByYz0wLgogICAgZGVmIF9raG9hKHQpOiByZXR1cm4gdC5zcGxpdCgi',
'XyIpWzBdCiAgICBkb19wYWNrZXQsIGRvX2xhLCBkb190aGlldV9jb25nX2N1ID0gW10sIFtdLCBbXQogICAgZm9yIHQgaW4g',
'c29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAgICBrLCBseSA9IF9raG9hKHQpLCBkb19oZXRbdF0KICAgICAgICBp',
'ZiBrIGluIENBX1BBQ0tFVDogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb19wYWNrZXQuYXBwZW5kKHQpCiAgICAg',
'ICAgZWxpZiAiS0jDlE5HIMSQTyDEkMav4buiQyIgaW4gbHkgb3IgInRoaeG6v3UgYCIgaW4gbHk6ICBkb190aGlldV9jb25n',
'X2N1LmFwcGVuZCh0KQogICAgICAgIGVsaWYgayBpbiBOR09BSV9QSEFNX1ZJOiAgICAgICAgICAgICAgICAgICAgICAgIHBh',
'c3MKICAgICAgICBlbHNlOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb19sYS5hcHBlbmQo',
'dCkKICAgIGdoaSgiZG9fcGFja2V0IiwgZG9fcGFja2V0KTsgZ2hpKCJkb19sYSIsIGRvX2xhKTsgZ2hpKCJkb190aGlldV9j',
'b25nX2N1IiwgZG9fdGhpZXVfY29uZ19jdSkKICAgIGlubigiIikKICAgIGlubihmIiAgY2EgRE8gdGh1b2MgQ0hJTkggcGFj',
'a2V0IG5heSA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XSBvciAna2hvbmcgY28nfSIpCiAgICBpbm4oZiIgIGNh',
'IERPIG5nb2FpIHBoYW0gdmkgKHIzIGtoYWkpOiB7W19raG9hKHgpIGZvciB4IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19j',
'YSkgaWYgX2tob2EoeCkgaW4gTkdPQUlfUEhBTV9WSV19IikKICAgIGlubihmIiAgY2EgRE8gdmkgVEhJRVUgQ09ORyBDVSAg',
'ICAgICA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV0gb3IgJ2tob25nIGNvJ30iKQogICAgaW5uKGYi',
'ICBjYSBETyBMQSAoa2hvbmcgZ2lhaSB0aGljaCBkdW9jKToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV0gb3IgJ2tob25n',
'IGNvJ30iKQogICAgIyAtLS0tIENIT1Q6IHBoZXAgZG8gcGhhaSBUUk9OIHRydW9jIGtoaSBtb3QgY2h1IERBVCBuYW8gZHVv',
'YyBwaGF0IC0tLS0KICAgICMgQmFuIHRydW9jIGNoaSBJTiBgdGluYC9gcmNfc3VpdGVgOiBibyB0ZXN0IGNoZXQgZ2l1YSB0',
'MTcxIChyYz0xMzQsIGtob25nIGRvbmcgdG9uZykKICAgICMgdmFuIHJhICJEQVQgMTIgfCBUUlVPVCAwIiByYz0wOyBjYSBQ',
'QUNLRVQgdmFuZyBtYXQgaGF5IGJpIEJPIFFVQSBjdW5nIGR1b2MgY2hhbSBuaHUKICAgICMgImtob25nIGRvIi4gVmFuZyBt',
'YXQga2hvbmcgcGhhaSAia2hvbmcgZG8iIOKAlCBsYSBLSE9ORyBETyBEVU9DLgogICAgdmFuZyA9IFt0IGZvciB0IGluIHNv',
'cnRlZChDQV9QQUNLRVQsIGtleT1zb19jYSkgaWYgbWF1X2NhKG91dF9uLCB0KSBub3QgaW4gKCJRVUEiLCAiRE8iKV0KICAg',
'IGx5X2tkZCA9IFtdCiAgICBpZiBub3QgdGluOiBseV9rZGQuYXBwZW5kKCJkYW5oIHNhY2ggZG8gS0hPTkcgZGF5IGR1IikK',
'ICAgIGlmIHJjX24gbm90IGluICgwLCAxKSBvciAocmNfbiA9PSAxKSAhPSBib29sKGRvX2hldCk6CiAgICAgICAgbHlfa2Rk',
'LmFwcGVuZChmInJjIGJvIHRlc3Q9e3JjX259IGtob25nIGtob3Age2xlbihkb19oZXQpfSBjYSBETyBkb2MgZHVvYyIpCiAg',
'ICBpZiB2YW5nOiBseV9rZGQuYXBwZW5kKGYiY2EgUEFDS0VUIHZhbmcvYm8gcXVhOiB7dmFuZ30iKQogICAgZ2hpKCJjYV9w',
'YWNrZXRfdmFuZyIsIHZhbmcpOyBnaGkoImx5X2RvX2NodWFfdHJvbiIsIGx5X2tkZCkKICAgIGlmIGx5X2tkZDoga2V0KCJC',
'byB0ZXN0IGNoYXkgVFJPTiB2YSBkb2MgRFUiLCBLREQsICI7ICIuam9pbihseV9rZGQpKQogICAgY2h1YV90cm9uID0gS0RE',
'IGlmIGx5X2tkZCBlbHNlIERBVAogICAga2V0KCJLaG9uZyBjYSBuYW8gY3VhIFBBQ0tFVCBiaSBETyIsIGNodWFfdHJvbiBp',
'ZiBub3QgZG9fcGFja2V0IGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX3BhY2tldCBlbHNlIGYiRE86IHtbX2to',
'b2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XX0g4oCUIGJhbiB2YSBDSFVBIHhvbmciKQogICAga2V0KCJNb2kgY2EgRE8gZGV1',
'IGdpYWkgdGhpY2ggZHVvYyIsIGNodWFfdHJvbiBpZiBub3QgZG9fbGEgZWxzZSBUUlVPVCwKICAgICAgICAiIiBpZiBub3Qg',
'ZG9fbGEgZWxzZSBmImxhOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXX0iKQogICAgaWYgZG9fdGhpZXVfY29uZ19jdToK',
'ICAgICAgICBrZXQoIkNvbmcgY3UgZGF5IGR1IGRlIGRvIiwgS0RELCBmInRoaWV1IGNvbmcgY3UgY2hvIHtbX2tob2EoeCkg',
'Zm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV19IikKCiAgICBicSA9IHNvcnRlZCh7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEu',
'ZmluZGFsbChvdXRfbil9LCBrZXk9c29fY2EpOyBnaGkoImNhX2JvX3F1YSIsIGJxKQogICAgaW5uKCIiKTsgaW5uKGYiICBC',
'TyBRVUEgKHtsZW4oYnEpfSk6IHtbeC5zcGxpdCgnXycpWzBdIGZvciB4IGluIGJxXX0iKQoKICAgIGlubigiIik7IGlubigi',
'ICBOMS1ONCAodDE2NS10MTY4KSwgdGlldSBjaGkgbmdoaWVtIHRodSBjdWEgcjIsIG5heSBsYSBjaGkgYmFvIGhvaSBxdXk6',
'IikKICAgIGI0ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0FNT0l9OyBnaGkoImNhX21vaSIsIGI0KQogICAg',
'Zm9yIHQgaW4gQ0FNT0k6IGlubihmIiAgICAge3R9OiB7YjRbdF19IikKICAgICMgQk9fUVVBL3ZhbmcgbGEgQ0hVQSBDSEFZ',
'LCBraG9uZyBwaGFpIERPOiBjaGkgbW90IGNhIERPIG1vaSBkdW9jIHBoYXQgVFJVT1QuCiAgICBrZXQoIk4xLU40ICh0MTY1',
'LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJRVUEiIGZvciB2IGluIGI0LnZhbHVlcygpKQogICAgICAgIGVsc2UgKFRSVU9U',
'IGlmIGFueSh2ID09ICJETyIgZm9yIHYgaW4gYjQudmFsdWVzKCkpIGVsc2UgS0REKSwgc3RyKGI0KSkKCiAgICBpbm4oIiIp',
'OyBpbm4oIiAgMTUgY2EgdHVuZyBkbyB0cmVuIENJOiIpCiAgICBiMTUgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBp',
'biBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQogICAgaW5uKCIgICAgIiArICIgICIuam9pbihmInt0fTp7YjE1W3RdfSIgZm9y',
'IHQgaW4gQ0ExNSkpCgogICAgIyB0MTM2IOKAlCBOMTIgZG8gR0lBTiBUSUVQIHF1YSBrZXQgcXVhIGNhCiAgICB0MTM2X3Rl',
'biA9IG5leHQoKHQgZm9yIHQgaW4gZG9faGV0IGlmIHQuc3RhcnRzd2l0aCgidDEzNiIpKSwgTm9uZSkKICAgIGlmIGIxNS5n',
'ZXQoInQxMzYiKSA9PSAiUVVBIjoKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBEQVQsICJ0MTM2',
'IFFVQSIpCiAgICBlbGlmIGIxNS5nZXQoInQxMzYiKSAhPSAiRE8iOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQg',
'cXVhIGNhKSIsIEtERCwgZiJ0MTM2ID0ge2IxNS5nZXQoJ3QxMzYnKSFyfSDigJQga2hvbmcgY2hheS9raG9uZyB0aGF5IikK',
'ICAgIGVsc2U6CiAgICAgICAgbHkgPSBkb19oZXQuZ2V0KHQxMzZfdGVuLCAiIikKICAgICAgICBrZXQoIk4xMiB0MTM2IChx',
'dWEga2V0IHF1YSBjYSkiLCBUUlVPVCwgZiJETzoge2x5Wzo5MF19IikKCiMgLS0tLS0tLS0tLS0tLS0tLSAzLiBwcm9iZSBU',
'SEFORyB2YW8gaGFtIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIzLiBQUk9CRSBUSEFO',
'RyDigJQgZ29pIF9naXRfd2luZG93cyB2b2kgdGhhbSBzbyB0aWVtIikKc3BlYyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJv',
'bV9maWxlX2xvY2F0aW9uKCJscDU0MSIsIHN0cih0ZXApKQpscCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMo',
'c3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9kdWxlKGxwKQpzaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShscC5fZ2l0X3dpbmRv',
'd3MpCmdoaSgidGhhbV9zb19fZ2l0X3dpbmRvd3MiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKaW5uKCIgIHRoYW0gc28gY3Vh',
'IF9naXRfd2luZG93czoiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKCmRlZiBnb2koKiprdyk6CiAgICAiIiJHb2kgX2dpdF93',
'aW5kb3dzLCBCQVQgc3RkZXJyIGRlIG1vdCBkb25nIGNoYW4gZG9hbiBraG9uZyBnaWV0IGx1b3QgZG8uIiIiCiAgICBlID0g',
'aW8uU3RyaW5nSU8oKQogICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICByID0gbHAuX2dp',
'dF93aW5kb3dzKCoqa3cpCiAgICByZXR1cm4gciwgZS5nZXR2YWx1ZSgpCgojIC0tLSBkb2kgY2h1bmcgcmlnOiBwaGFpIHRy',
'YSBsb2kgZHVuZyBtb3QgY2EgdGEgQklFVCBUUlVPQyBkYXAgYW4gLS0tCndpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0',
'b3J5KCkgYXMgdDoKICAgIG5nb2FpID0gUGF0aCh0KS8ibmdvYWkiOyBuZ29haS5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3',
'ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAobmdvYWkvImdpdC5leGUiKS53cml0',
'ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIxLCBfID0gZ29pKHBhdGg9c3RyKG5nb2FpKSwgcHJvZ3JhbV9m',
'aWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIChjdy8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0i',
'dXRmLTgiKQogICAgcjIsIF8gPSBnb2kocGF0aD1zdHIoY3cpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cp',
'KQpyaWdfb2sgPSBib29sKHIxKSBhbmQgcjIgaXMgTm9uZQpnaGkoInJpZ19kb2lfY2h1bmciLCByaWdfb2spCmtldCgiUklH',
'IGRvaSBjaHVuZyAoYmlldCB0cnVvYyBkYXAgYW4pIiwgREFUIGlmIHJpZ19vayBlbHNlIEtERCwKICAgIGYibmdvYWktY3dk',
'LT57J05IQU4nIGlmIHIxIGVsc2UgJ05vbmUnfSB8IHRyb25nLWN3ZC0+eydOSEFOJyBpZiByMiBlbHNlICdOb25lJ30iKQpp',
'ZiBub3QgcmlnX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiByaWcgc2FpLCBtb2kgY2hvdCBkdW9pIHNl',
'IHZvIG5naGlhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0gTU9JIENPTkcgUEhBSSBUVSBDSFVORyBNSU5IIE5PIENPIFRIRSBE',
'TyAtLS0KIyBCYWkgaG9jIGRhdCBuaGF0IGN1YSBwYWNrZXQgbmF5OiBkb19uMTAgYmFuIGN1IGNoYW0gREFUIGNobyA5NTgz',
'MTY4NSB0cm9uZyBraGkgdDE3MQojIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQgdGF0IG1hIE4xMCBz',
'aW5oIHJhIGRlIGJhdC4gTm8gZGVnZW5lcmF0ZSDigJQKIyB0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBsYSAnOycgbmVu',
'ICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIGN1bmcga2V0IHF1YS4KIyBNb3QgY29uZyBraG9uZyB0aGUgRE8gdGhp',
'IGtob25nIHBoYWkgY29uZywgdmEgbm8gbmd1eSBoaWVtIGhvbiBraG9uZyBjbyBjb25nOiBubwojIHBoYXQgcmEgbW90IGNo',
'dSBEQVQuCiMKIyBOZW4gdHJ1b2Mga2hpIERVTkcgbmFtIGNvbmcgbmF5IGRlIHBoYW4gcXV5ZXQsIGJhdCB0dW5nIGNvbmcg',
'Z2lldCBtb3QgZG90IGJpZW4gZGEKIyBiaWV0IHRyb25nLiBDb25nIG5hbyBraG9uZyBnaWV0IGR1b2MgdGhpIGNodSBEQVQg',
'Y3VhIG5vIGJpIEhBIHh1b25nIEtIT05HIERPIERVT0M7CiMgVFJVT1QgZ2l1IG5ndXllbiAocXVhbiBzYXQgdHJ1YyB0aWVw',
'LCB2ZC4gZzEgdmFuIG5oYW4gZ2l0LmJhdCkuIERvdCBiaWVuIGNoYXkgdHJlbiBCQU4gU0FPIFRBTTsgY2F5IHRoYXQga2hv',
'bmcgYmkKIyBkdW5nIHRvaSAoY3VuZyBreSBsdWF0IG5odSBONykuCkRPVF9CSUVOX1RVX0tJRU0gPSBbCiAgICAoIk44Iiwg',
'Im9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAnaWYgY2hpX2RpbmggYW5kIFBhdGgoY2hpX2RpbmgpLm5hbWUubG93ZXIo',
'KSA9PSAiZ2l0LmV4ZSIgYW5kIGhvcF9sZShjaGlfZGluaCk6JywKICAgICAiaWYgY2hpX2RpbmggYW5kIGhvcF9sZShjaGlf',
'ZGluaCk6IiksCiAgICAoIk45IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAiZCA9IGRfcmF3LnN0cmlwKCkuc3Ry',
'aXAoJ1wiJykiLCAiZCA9IGRfcmF3LnN0cmlwKCkiKSwKICAgICgiTjEwIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAg',
'ICAic2VwID0gb3MucGF0aHNlcCBpZiBwaGFuX2NhY2ggaXMgTm9uZSBlbHNlIHBoYW5fY2FjaCIsICJzZXAgPSBvcy5wYXRo',
'c2VwIiksCiAgICAoIk4xMSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsICJpZiBjaGFuX2RvYW4gaXMgbm90IE5vbmU6Iiwg',
'ImlmIEZhbHNlOiIpLAogICAgKCJOMTIiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSIsCiAgICAgJ2dpdF9wYXRoPSIv',
'L2tob25nLWNvL2dpdCInLCAnZ2l0X3BhdGg9Ii9raG9uZy1jby9naXQiJyksCl0KaW5uKCIiKTsgaW5uKCIgIHR1IGtpZW0g',
'Y29uZyDigJQgbW9pIGNvbmcgcGhhaSBnaWV0IGR1b2MgbW90IGRvdCBiaWVuIGRhIGJpZXQ6IikKZ2lldCA9IHt9CmZvciBt',
'YSwgZHVvbmcsIHRpbSwgdGhheSBpbiBET1RfQklFTl9UVV9LSUVNOgogICAgX3RlbiwgX2hhbSA9IG5leHQoKChhLCBiKSBm',
'b3IgYSwgYiBpbiBQUk9CRSBpZiBhLnN0YXJ0c3dpdGgobWEgKyAiICIpKSwgKE5vbmUsIE5vbmUpKQogICAgaWYgX2hhbSBp',
'cyBOb25lOgogICAgICAgIGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBraG9uZyB0',
'aW0gdGhheSBwcm9iZSB0ZW4gJ3ttYX0gLi4uJyIpOyBjb250aW51ZQogICAgdHJ5OgogICAgICAgIHdpdGggdGVtcGZpbGUu',
'VGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgX3Q6CiAgICAgICAgICAgIF9jID0gUGF0aChfdCkvImNheSI7IHNodXRpbC5jb3B5',
'dHJlZShnb2MvIm9wcyIsIF9jLyJvcHMiKQogICAgICAgICAgICBfZiA9IF9jL2R1b25nOyBfbmQgPSBfZi5yZWFkX3RleHQo',
'ZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgaWYgX25kLmNvdW50KHRpbSkgIT0gMToKICAgICAgICAgICAgICAgIGdp',
'ZXRbbWFdID0gTm9uZQogICAgICAgICAgICAgICAgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBtYXUgZG90IGJp',
'ZW4ga2hvcCB7X25kLmNvdW50KHRpbSl9IGxhbiAobW9uZyAxKSIKICAgICAgICAgICAgICAgICAgICBmIiDigJQgbWEgbmd1',
'b24gZGEgZG9pLCBkb3QgYmllbiBuYXkgaGV0IHkgbmdoaWEiKTsgY29udGludWUKICAgICAgICAgICAgX2Yud3JpdGVfdGV4',
'dChfbmQucmVwbGFjZSh0aW0sIHRoYXksIDEpLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBfc3AgPSBpbXBvcnRs',
'aWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfZGJfIiArIG1hLCBzdHIoX2MvIm9wcyIvImxlYXNlX3B1Ymxp',
'c2gucHkiKSkKICAgICAgICAgICAgX20gPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2Fk',
'ZXIuZXhlY19tb2R1bGUoX20pCiAgICAgICAgICAgIGRlZiBfZ29pX2RiKCoqa3cpOgogICAgICAgICAgICAgICAgX2UgPSBp',
'by5TdHJpbmdJTygpCiAgICAgICAgICAgICAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKF9lKToKICAgICAg',
'ICAgICAgICAgICAgICByZXR1cm4gX20uX2dpdF93aW5kb3dzKCoqa3cpLCBfZS5nZXR2YWx1ZSgpCiAgICAgICAgICAgIF90',
'dCwgX2N0LCBfID0gX2hhbShfZ29pX2RiLCBpbnNwZWN0LnNpZ25hdHVyZShfbS5fZ2l0X3dpbmRvd3MpLAogICAgICAgICAg',
'ICAgICAgICAgICAgICAgICAgICAgX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgZ2lldFttYV0g',
'PSAoX3R0ID09IFRSVU9UKQogICAgICAgIGlubihmIiAgICB7bWE6NH0gZG90IGJpZW4gLT4ge190dDoxNH0geydHSUVUIERV',
'T0MnIGlmIF90dCA9PSBUUlVPVCBlbHNlICdTT05HIFNPVCd9IgogICAgICAgICAgICArIChmIiAgICh7X2N0fSkiIGlmIF9j',
'dCBlbHNlICIiKSkKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgX2U6CiAgICAgICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIg',
'ICAge21hOjR9IEtIT05HIERPIERVT0M6IHt0eXBlKF9lKS5fX25hbWVfX306IHtfZX0iKQpnaGkoImNvbmdfZ2lldF9kdW9j',
'X2RvdF9iaWVuIiwgZ2lldCkKCmZvciB0ZW4sICh0dCwgY3QsIGRsKSBpbiBbKHQsIGYoZ29pLCBzaWcsIHRlcHQpKSBmb3Ig',
'dCwgZiBpbiBQUk9CRV06CiAgICBnaGkoInByb2JlXyIgKyB0ZW4uc3BsaXQoKVswXS5sb3dlcigpLCBkbCkKICAgIGlmIGlz',
'aW5zdGFuY2UoZGwsIGRpY3QpOgogICAgICAgIGZvciBrLCB2IGluIGRsLml0ZW1zKCk6IGlubihmIiAgICB7azozNH06IHt2',
'fSIpCiAgICBtYSA9IHRlbi5zcGxpdCgpWzBdCiAgICBpZiBnaWV0LmdldChtYSkgaXMgbm90IFRydWUgYW5kIHR0ID09IERB',
'VDoKICAgICAgICAjIERBVCB0dSBtb3QgY29uZyBjaHVhIGNodW5nIG1pbmggZHVvYyBsYSBiaWV0IERPIHRoaSBraG9uZyBk',
'YW5nIHRpbiBob24gS0RELgogICAgICAgIGtldCh0ZW4sIEtERCwgZiJjb25nIEtIT05HIGdpZXQgZHVvYyBkb3QgYmllbiBj',
'dWEgY2hpbmggbm8gKHtnaWV0LmdldChtYSkhcn0pIgogICAgICAgICAgICAgICAgICAgICAgZiIgLT4gY2h1IERBVCBuYXkg',
'a2hvbmcgY28gZ2lhIHRyaSIpCiAgICBlbHNlOgogICAgICAgIGtldCh0ZW4sIHR0LCBjdCkKCiMgLS0tLS0tLS0tLS0tLS0t',
'LSA0LiBONyBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENISV9QUk9CRToKICAg',
'IGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiNC4gTjcg4oCUIGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBUQU0gKGNheSB0',
'aGF0IEtIT05HIGJpIGR1bmcgdG9pKSIpCiAgICB0cnVvYyA9IHRlcC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikuY291',
'bnQoTUFVX1dJTikKICAgIGdoaSgibjdfdHJ1b2MiLCB0cnVvYyk7IGlubihmIiAgc28gZG9uZyBraG9wIHtNQVVfV0lOIXJ9',
'OiBUUlVPQyA9IHt0cnVvY30gW21vbmcgMV0iKQogICAgaWYgdHJ1b2MgIT0gMToKICAgICAgICBrZXQoIk43IGRvdCBiaWVu',
'IG5oYW5oIFdpbmRvd3MiLCBLREQsIGYibWF1IHh1YXQgaGllbiB7dHJ1b2N9IGxhbiwga2hvbmcgcGhhaSAxIikKICAgIGVs',
'c2U6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0bXA6CiAgICAgICAgICAgIHNhbyA9',
'IFBhdGgodG1wKS8iY2F5IgogICAgICAgICAgICBzaHV0aWwuY29weXRyZWUoZ29jLCBzYW8sIGlnbm9yZT1zaHV0aWwuaWdu',
'b3JlX3BhdHRlcm5zKCIuZ2l0IiwgIl9fcHljYWNoZV9fIiwgIioucHljIikpCiAgICAgICAgICAgIGYyID0gc2FvLyJvcHMi',
'LyJsZWFzZV9wdWJsaXNoLnB5IgogICAgICAgICAgICBmMi53cml0ZV90ZXh0KGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRm',
'LTgiKS5yZXBsYWNlKE1BVV9XSU4sICJpZiBGYWxzZToiKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgc2F1ID0g',
'ZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4pOyBnaGkoIm43X3NhdSIsIHNhdSkKICAgICAg',
'ICAgICAgaW5uKGYiICBTQVUgKGRhIGRvdCBiaWVuKSA9IHtzYXV9IFttb25nIDBdIikKICAgICAgICAgICAgaWYgc2F1ICE9',
'IDA6CiAgICAgICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsICJkb3QgYmllbiBLSE9O',
'RyBhcCBkdW9jIikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHJjX20sIG91dF9tID0gY2hheShbIm9wcy9s',
'ZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgc2FvKQogICAgICAgICAgICAgICAgbTE2NSA9IG1hdV9jYShvdXRfbSwgInQxNjUi',
'KTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20pCiAgICAgICAgICAgICAgICB0ZW4xNjUgPSBuZXh0KCh0IGZvciB0IGluIGRt',
'IGlmIHQuc3RhcnRzd2l0aCgidDE2NSIpKSwgTm9uZSkKICAgICAgICAgICAgICAgIGx5ID0gKGRtLmdldCh0ZW4xNjUpIG9y',
'ICIiKQogICAgICAgICAgICAgICAgZ2hpKCJuN190MTY1IiwgbTE2NSk7IGdoaSgibjdfbHlfZG8iLCBseVs6MjAwXSkKICAg',
'ICAgICAgICAgICAgIGlubihmIiAgdDE2NSBzYXUgZG90IGJpZW46IHttMTY1fSB8IHtseVs6MTEwXX0iKQogICAgICAgICAg',
'ICAgICAgZHVuZ19seV9kbyA9ICJQQVRIIHQiIGluIGx5IG9yICIvdXNyL2JpbiIgaW4gbHkKICAgICAgICAgICAgICAgIGtl',
'dCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIERBVCBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKSBlbHNl',
'CiAgICAgICAgICAgICAgICAgICAgKFRSVU9UIGlmIG0xNjUgPT0gIkRPIiBlbHNlIEtERCksCiAgICAgICAgICAgICAgICAg',
'ICAgImdpZXQgZHVuZyBseSBkbyIgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykKICAgICAgICAgICAgICAgICAg',
'ICBlbHNlICgiRE8gbmh1bmcgS0hPTkcgZHVuZyBseSBkbyAtPiB0aW4gZHVuZyBnaWEiIGlmIG0xNjUgPT0gIkRPIiBlbHNl',
'ICJraG9uZyBkb2MgZHVvYyB0MTY1IikpCgojIC0tLS0tLS0tLS0tLS0tLS0gS0VUIExVQU4gLS0tLS0tLS0tLS0tLS0tLQpp',
'bm4oIiIpOyBpbm4oIj0iICogNzgpCmlubihmIlRIRSBIRSBETyBEVU9DOiB7dGhlX2hlfSAgIEhFQUQ9e2hlYWRbOjEyXX0i',
'KQojIEtob2kgZGFuIGNobyByZXZpZXdlciBiYXQgZGF1IG8gZG9uZyB0cmVuLCBuZW4gQ0hFIERPIHBoYWkgbmFtIE5HQVkg',
'ZHVvaSBubzoga2hvbmcgY28gZG9uZyBuYXkKIyB0aGkgbW90IGx1b3QgLS1jaGktcHJvYmUgaW4gIkRBVCA3IHwgVFJVT1Qg',
'MCB8IEtIT05HIERPIERVT0MgMCIgcmM9MCBtYSBraG9uZyBub2kgbGEgY2h1YSBjaGF5IGJvIHRlc3QuCmdoaSgiY2hlX2Rv',
'IiwgImNoaS1wcm9iZSIgaWYgQ0hJX1BST0JFIGVsc2UgImRheS1kdSIpCmlmIENISV9QUk9CRToKICAgIGlubigiLS1jaGkt',
'cHJvYmU6IENISSBkbyBtdWMgMCwgMSwgMy4gQm8gdGVzdCwgTjEtTjQsIHQxMzYsIE43IEtIT05HIGNoYXkgLSBkYXkgS0hP',
'TkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCmlmIHRoZV9oZSA9PSAiZzEiOgogICAgaW5uKCJMVVUgWTogZGF5IGxh',
'IE5FTiBETyAoZzEpLCBLSE9ORyBwaGFpIG5naGllbSB0aHUgZzIuIENhYyBjaG90IE44LU4xMiBkdW9pIGRheSIpCiAgICBp',
'bm4oIiAgICAgICBUUlVPVCBsYSBEVU5HIE5IVSBNT05HIOKAlCBjaHVuZyBsYSBuaHVuZyBsbyBnMiBzaW5oIHJhIGRlIHbD',
'oS4iKQppbm4oIi0iICogNzgpCmZvciB0ZW4sIHR0LCBjdCBpbiBjaG90OgogICAgaW5uKGYiICB7dHQ6MTR9IHt0ZW59IiAr',
'IChmIiAgIHtjdH0iIGlmIGN0IGVsc2UgIiIpKQpuX2tkZCA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBL',
'REQpCm5fdHJ1b3QgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCmlubigiLSIgKiA3OCkKaW5u',
'KGYiICBEQVQge3N1bSgxIGZvciBfLHQsXyBpbiBjaG90IGlmIHQ9PURBVCl9IHwgVFJVT1Qge25fdHJ1b3R9IHwgS0hPTkcg',
'RE8gRFVPQyB7bl9rZGR9IikKaW5uKGYiICBUb25nIGNhIGRvOiB7c28uZ2V0KCdzb19jYV9kbycpfSB8IGRhbmggc2FjaCBk',
'YXkgZHU6IHsnQ08nIGlmIHNvLmdldCgnbGlldF9rZV9kYXlfZHUnKSBlbHNlICdLSE9ORyBETyBEVU9DJ30iKQppbm4oZiIg',
'IEFkbWluaXN0cmF0b3I6IHtzby5nZXQoJ3F1eWVuX2FkbWluJyl9IHwgc3ltbGluazoge3NvLmdldCgnc3ltbGlua19kdW9j',
'Jyl9IikKaW5uKCIiKTsgaW5uKCItLS0gREFOIE5HVVlFTiBLSE9JIEpTT04gTkFZIFZFIENITyBSRVZJRVdFUiAtLS0iKQpn',
'aGkoImNob3QiLCBbeyJ0ZW4iOiBhLCAidHJhbmdfdGhhaSI6IGIsICJjaGlfdGlldCI6IGN9IGZvciBhLCBiLCBjIGluIGNo',
'b3RdKQppbm4oanNvbi5kdW1wcyhzbywgZW5zdXJlX2FzY2lpPUZhbHNlLCBpbmRlbnQ9MSwgZGVmYXVsdD1zdHIpKQojIHJj',
'OiAwID0gbW9pIGNob3QgREFUIHwgMSA9IGNvIGNob3QgVFJVT1QgfCAzID0gY28gY2hvdCBLSE9ORyBETyBEVU9DICh1dSB0',
'aWVuIGJhbyBkb25nKQpzeXMuZXhpdCgzIGlmIG5fa2RkIGVsc2UgKDEgaWYgbl90cnVvdCBlbHNlIDApKQo='
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
