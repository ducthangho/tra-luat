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

# Bat MOI loi khong luong truoc -> rc=3. Vi sao khong de mac dinh: PowerShell tra rc=1
# khi script chet vi ngoai le, ma rc=1 o day DA CO NGHIA "co chot truot". Hai thu khac
# han nhau - mot ben la phep do chay xong va truot, mot ben la phep do chua he chay.
trap {
    Write-Host ''
    Write-Host "KHONG DO DUOC: loi khong luong truoc - $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  tai: $($_.InvocationInfo.ScriptLineNumber): $($_.InvocationInfo.Line.Trim())" -ForegroundColor Red
    Write-Host 'Khong ket luan gi.' -ForegroundColor Red
    exit 3
}

# ---------------------------------------------------------------- hang so DA DO
$Url        = 'https://github.com/ducthangho/tra-luat'
$ShaBoDo    = 'ab57df7a06c20239b77b5c10701092c95ddde1dbf4e7b76d1fe5a105fd679dec'      # SHA-256 cua bo do Python nhung ben duoi

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
    ForEach-Object { Remove-Item -LiteralPath ('Env:' + $_.Name) }
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
'YzJkMmFiYmRkYmI2ZiIKQkFOX0JPX0RPID0gIjIwMjYtMDktMzBmIiAgICAgICAgICAgICAgIyBkb2kgTU9JIGtoaSBzdWEg',
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
'IENJIGtob25nIGNvIGNhdSBoaW5oIENBIE5IQU46IGJvIE1PSSBiaWVuIEdJVF8qLCBnbG9iYWwgPSByb25nIChjdW5nIGdp',
'YSB0cmkgbGVhc2VfcHVibGlzaC5weSBkYXQgY2hvIGdpdCBjb24gY3VhIG5vKTsKIyBHSVUgY2F1IGhpbmggSEUgVEhPTkcg',
'KGJhbiBjYWkgR2l0IOKAlCBDSSBXaW5kb3dzIGN1bmcgY28pLCByaWVuZyBpbml0LmRlZmF1bHRCcmFuY2ggR0hJTSB2ZSBt',
'YWMgZGluaCBjdWEgZ2l0IHZpIG5vIGRhdAojIGR1b2MgY2EgbyBoZSB0aG9uZy4gQ29uIGxhaSAoa2hvYSBoZSB0aG9uZyBr',
'aGFjKSBsYSBnaW9pIGhhbiBkYSBiaWV0LCBraG9uZyBwaGFpIGRhIGRvbmcuCmRlZiBjaGF5KGFyZ3YsIGN3ZCwgcGh1dD02',
'MCk6CiAgICBtdCA9IHtrOiB2IGZvciBrLCB2IGluIG9zLmVudmlyb24uaXRlbXMoKQogICAgICAgICAgaWYgbm90IGsudXBw',
'ZXIoKS5zdGFydHN3aXRoKCJHSVRfIikgYW5kIChub3Qgay51cHBlcigpLnN0YXJ0c3dpdGgoIlBZVEhPTiIpIG9yIGsudXBw',
'ZXIoKSBpbiBfUFlfR0lVKX0KICAgIG10LnVwZGF0ZShQWVRIT05VVEY4PSIxIiwgUFlUSE9OSU9FTkNPRElORz0idXRmLTgi',
'LCBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0iMSIsIFBZVEhPTlVOQlVGRkVSRUQ9IjEiLAogICAgICAgICAgICAgIEdJVF9D',
'T05GSUdfR0xPQkFMPW9zLmRldm51bGwsIEdJVF9DT05GSUdfQ09VTlQ9IjEiLAogICAgICAgICAgICAgIEdJVF9DT05GSUdf',
'S0VZXzA9ImluaXQuZGVmYXVsdEJyYW5jaCIsIEdJVF9DT05GSUdfVkFMVUVfMD0ibWFzdGVyIikKICAgIHAgPSBzdWJwcm9j',
'ZXNzLnJ1bihbc3lzLmV4ZWN1dGFibGVdICsgYXJndiwgY3dkPXN0cihjd2QpLCBjYXB0dXJlX291dHB1dD1UcnVlLAogICAg',
'ICAgICAgICAgICAgICAgICAgIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91',
'dD1waHV0KjYwLCBlbnY9bXQpCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpICsgKHAuc3RkZXJy',
'IG9yICIiKQoKZGVmIG1hdV9jYShvdXQsIHQpOgogICAgbSA9IHJlLnNlYXJjaChyIig/bSlePDw8IHJhICgiICsgdCArIHIi',
'W2Etel0/X1xTKikgWzAtOS5dK3MgKFx3KylccyokIiwgb3V0KQogICAgcmV0dXJuIG0uZ3JvdXAoMikgaWYgbSBlbHNlIE5v',
'bmUKCmRlZiBnaXQoZ29jLCAqYSwgcGh1dD01KToKICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbImdpdCIsICItQyIsIHN0cihn',
'b2MpLCAqYV0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwKICAgICAgICAgICAgICAgICAgICAgICBlbmNvZGlu',
'Zz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjApCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAo',
'cC5zdGRvdXQgb3IgIiIpLnN0cmlwKCksIChwLnN0ZGVyciBvciAiIikuc3RyaXAoKQoKCiMgPT09PT09PT09PT09PT09PT0g',
'TkFNIFBST0JFLCB2aWV0IHRoYW5oIEhBTSBUSFVBTiBkZSBUVSBLSUVNIGR1b2MgPT09PT09PT09PT09PT09PT0KIyBNb2kg',
'aGFtIHRyYSAodHJhbmdfdGhhaSwgY2hpX3RpZXQsIGR1X2xpZXUpLiBLSE9ORyBpbiwgS0hPTkcgdGhvYXQg4oCUIG5obyB2',
'YXkgY2h1bmcKIyBjaGF5IGR1b2MgdHJlbiBuZW4gQkFUIEtZLCB2YSBgLS10dS1raWVtLXByb2JlYCBnb2kgdGhhbmcgY2h1',
'bmcgZGUga2llbSBjaGluaCBibyBkby4KCmRlZiBfc2FuKHQpOgogICAgZCA9IFBhdGgodCkvImQiOyBkLm1rZGlyKCk7IGN3',
'ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIHJldHVybiBk',
'LCBjdywgcGYKCmRlZiBkb19uOChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJCdW9jIDEgKENPTkdfQ1VfR0lUKSBjaGkgZHVv',
'YyBuaGFuIGdpdC5leGUuIERvaSBjaHVuZyBkdW9uZzogZ2l0LmV4ZSBWQU4gcGhhaSBuaGFuLiIiIgogICAga3EgPSB7fQog',
'ICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkK',
'ICAgICAgICBmb3IgdGVuIGluICgiZ2l0LmV4ZSIsICJnaXQuYmF0IiwgImdpdC5jbWQiLCAiZ2l0LnB5IiwgImtob25nLXBo',
'YWktZ2l0LnR4dCIpOgogICAgICAgICAgICBmID0gZC90ZW47IGYud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIp',
'CiAgICAgICAgICAgIHIsIF8gPSBnb2koY29uZ19jdV9naXQ9c3RyKGYpLCBwYXRoPSIiLCBwcm9ncmFtX2ZpbGVzPXN0cihw',
'ZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICBrcVtmIkNPTkdfQ1VfR0lUPXt0ZW59Il0gPSAiTkhBTiIgaWYgciBlbHNl',
'ICJUVSBDSE9JIgogICAgbG90ID0gW2sgZm9yIGssIHYgaW4ga3EuaXRlbXMoKSBpZiB2ID09ICJOSEFOIiBhbmQgbm90IGsu',
'ZW5kc3dpdGgoImdpdC5leGUiKV0KICAgIGlmIGtxLmdldCgiQ09OR19DVV9HSVQ9Z2l0LmV4ZSIpICE9ICJOSEFOIjoKICAg',
'ICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IGdpdC5leGUgaG9wIGxlIG1hIGJpIHR1IGNob2kiLCBr',
'cQogICAgcmV0dXJuIChEQVQgaWYgbm90IGxvdCBlbHNlIFRSVU9UKSwgKCIiIGlmIG5vdCBsb3QgZWxzZSBmImNvbiBuaGFu',
'OiB7bG90fSIpLCBrcQoKZGVmIGRvX245KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIk11YyBQQVRIIGJvYyBuaGF5IGtlcCBw',
'aGFpIE5IQU47IG11YyByb25nIC8gdG9hbiBraG9hbmcgdHJhbmcgcGhhaSBibyBxdWEsIGtob25nIG5lbS4iIiIKICAgIGtx',
'ID0ge30KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8i',
'Y28gZ2l0IjsgZC5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBw',
'Zi5ta2RpcigpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAg',
'ICBmb3IgbmhhbiwgbXVjIGluICgoImtob25nIG5oYXkiLCBzdHIoZCkpLCAoImNvIG5oYXkga2VwIiwgZicie2R9IicpLAog',
'ICAgICAgICAgICAgICAgICAgICAgICAgICgicm9uZyIsICIiKSwgKCJjaGkga2hvYW5nIHRyYW5nIiwgIiAgICIpKToKICAg',
'ICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgciwgXyA9IGdvaShwYXRoPW11YywgcHJvZ3JhbV9maWxlcz1zdHIocGYp',
'LCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIk5v',
'bmUiCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0i',
'XSA9IGYiTkVNIHt0eXBlKGUpLl9fbmFtZV9ffSIKICAgIGlmIGtxLmdldCgiUEFUSCBraG9uZyBuaGF5IikgIT0gIk5IQU4i',
'OgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogbXVjIFBBVEggdGh1b25nIG1hIGtob25nIHRp',
'bSByYSBnaXQuZXhlIiwga3EKICAgIG9rID0gKGtxLmdldCgiUEFUSCBjbyBuaGF5IGtlcCIpID09ICJOSEFOIgogICAgICAg',
'ICAgYW5kIGtxLmdldCgiUEFUSCByb25nIikgPT0gIk5vbmUiIGFuZCBrcS5nZXQoIlBBVEggY2hpIGtob2FuZyB0cmFuZyIp',
'ID09ICJOb25lIikKICAgIHJldHVybiAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmci',
'KSwga3EKCiMgRGF1IHBoYW4gY2FjaCBkdW5nIERFIFRIVS4gUGhhaSBLSEFDIG9zLnBhdGhzZXAgdHJlbiBDQSBIQUkgbmVu',
'ICgnOycgV2luZG93cywgJzonIFBPU0lYKQojIHRoaSBoYWkgZ2lhIHRodXlldCAidGFjaCB0aGVvIGRhdSBkdW9jIHRydXll',
'biIgdmEgInRhY2ggdGhlbyBvcy5wYXRoc2VwIiBtb2kgcm9pIHJhIG5oYXUuClRIVV9OMTAgPSAifCIKCmRlZiBkb19uMTAo',
'Z29pLCBzaWcsIHRlcHQpOgogICAgIiIiSGFtIHBoYWkgdGFjaCBQQVRIIHRoZW8gZGF1IHBoYW4gY2FjaCBEVU9DIFRSVVlF',
'Tiwga2hvbmcgdGhlbyBvcy5wYXRoc2VwIGN1YSBuZW4uCgogICAgQmFuIGN1IGRvICJtb3QgZGF1ICc7JyB0cm9uZyBURU4g',
'dGh1IG11YyIgdmEgZGF0IERBVCB0cmVuIFdpbmRvd3MgZHUgaGFtIHNhaS4gTm8KICAgIGRlZ2VuZXJhdGU6IHRyZW4gV2lu',
'ZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JywgbmVuICdDOi9hO2InIHRoYXQgc3UgQ08gTkdISUEgbGEgaGFpCiAgICBtdWMg',
'4oCUICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIHJhIGN1bmcga2V0IHF1YSwgcGhlcCBkbyBraG9uZyB0aGUgZG8g',
'bmFvLiBObwogICAgZGEgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxIGN1YSBjaGluaCBiYW4gdmEgYXkg',
'RE8gdmkgZHVuZyBraHV5ZXQgdGF0IGF5LgogICAgTW90IGNvbmcga2hvbmcgdGhlIGRvIHRoaSBraG9uZyBwaGFpIGNvbmcu',
'CiAgICAiIiIKICAgIHRlbl9zZXAgPSBuZXh0KChrIGZvciBrIGluICgicGhhbl9jYWNoIiwgImRhdV9waGFuX2NhY2giLCAi',
'c2VwIikgaWYgayBpbiBzaWcucGFyYW1ldGVycyksIE5vbmUpCiAgICBpZiB0ZW5fc2VwIGlzIE5vbmU6CiAgICAgICAgIyBL',
'aG9uZyBjbyB0aGFtIHNvIHRoaSB0cmVuIFdpbmRvd3MgS0hPTkcgY29uIGR1b25nIG5hbyB0YWNoIGhhaSBnaWEgdGh1eWV0',
'LgogICAgICAgIGlmIG9zLnBhdGhzZXAgPT0gIjsiOgogICAgICAgICAgICByZXR1cm4gKEtERCwgInRyZW4gV2luZG93cyBv',
'cy5wYXRoc2VwIERBIGxhICc7JyB2YSBoYW0ga2hvbmcgbmhhbiB0aGFtIHNvIGRhdSBwaGFuIGNhY2ggIgogICAgICAgICAg',
'ICAgICAgICAgICAgICAgIi0+IGtob25nIHRhY2ggZHVvYyBoYWkgZ2lhIHRodXlldCIsCiAgICAgICAgICAgICAgICAgICAg',
'eyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZX0pCiAgICAgICAgd2l0aCB0ZW1wZmlsZS5U',
'ZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkK',
'ICAgICAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngi',
'LCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBfICA9IGdvaShwYXRoPXN0cihsYSkgKyBvcy5wYXRoc2VwICsg',
'c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICByMCwgXyA9IGdvaShwYXRo',
'PXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICBrcSA9IHsib3MucGF0aHNlcCI6',
'IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IE5vbmUsCiAgICAgICAgICAgICAgImNvIG11YyBjaHVhICc7JyI6ICJOSEFO',
'IiBpZiByIGVsc2UgIk5vbmUiLAogICAgICAgICAgICAgICJkb2kgY2h1bmcgZHVvbmcgKGtob25nIGNvICc7JykiOiAiTkhB',
'TiIgaWYgcjAgZWxzZSAiTm9uZSJ9CiAgICAgICAgaWYgbm90IHIwOgogICAgICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNo',
'dW5nIGR1b25nIGhvbmciLCBrcQogICAgICAgIHJldHVybiAoREFUIGlmIHIgZWxzZSBUUlVPVCksICgiIiBpZiByIGVsc2Ug',
'Im11YyBnaXQuZXhlIGhvcCBsZSBiaSBNQVQiKSwga3EKCiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgp',
'IGFzIHQ6CiAgICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUiOyBsYS5ta2RpcigpICAgICAgICAgICMgJzsnIG5hbSB0cm9u',
'ZyBURU4sIGtob25nIHBoYWkgZGF1IHBoYW4gY2FjaAogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8i',
'Z2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIG5vaSA9IHN0cihsYSkgKyBUSFVf',
'TjEwICsgc3RyKGQpCiAgICAgICAga3cgPSBkaWN0KHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAg',
'ICAgcl9jaGluaCwgXyA9IGdvaShwYXRoPW5vaSwgICAgICAqKnt0ZW5fc2VwOiBUSFVfTjEwfSwgICAqKmt3KSAgICMgdGFj',
'aCBkdW5nICAtPiBOSEFOCiAgICAgICAgcl9kdW9uZywgXyA9IGdvaShwYXRoPXN0cihkKSwgICAqKnt0ZW5fc2VwOiBUSFVf',
'TjEwfSwgICAqKmt3KSAgICMgZG9pIGNodW5nIGR1b25nCiAgICAgICAgcl9waGFuYmlldCwgXyA9IGdvaShwYXRoPW5vaSwg',
'ICAqKnt0ZW5fc2VwOiBvcy5wYXRoc2VwfSwgKiprdykgICMgdGFjaCB0aGVvIG9zLnBhdGhzZXAgLT4gbWF0CiAgICBrcSA9',
'IHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IHRlbl9zZXAsICJkYXUgdGh1IjogVEhVX04xMCwK',
'ICAgICAgICAgIGYibm9pIGJhbmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17VEhVX04xMCFyfSI6ICAgICAgICJOSEFOIiBp',
'ZiByX2NoaW5oIGVsc2UgIk5vbmUiLAogICAgICAgICAgZiJkb2kgY2h1bmcgZHVvbmcgKG1vdCBtdWMsIHt0ZW5fc2VwfT17',
'VEhVX04xMCFyfSkiOiAgIk5IQU4iIGlmIHJfZHVvbmcgZWxzZSAiTm9uZSIsCiAgICAgICAgICBmInBoYW4gYmlldDogbm9p',
'IGJhbmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17b3MucGF0aHNlcCFyfSI6ICJOSEFOIiBpZiByX3BoYW5iaWV0IGVsc2Ug',
'Ik5vbmUifQogICAgaWYgbm90IHJfZHVvbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBt',
'b3QgbXVjIGhvcCBsZSBtYSBraG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICAjIENvbmcgcGhhaSBDTyBUSEUgZG8uIE5l',
'dSBjYSBoYWkgZGF1IHBoYW4gY2FjaCBkZXUgcmEgTkhBTiB0aGkgcGhlcCBkbyBraG9uZyBwaGFuCiAgICAjIGJpZXQgZHVv',
'YyBnaSDigJQgZHVuZyBiYW8gREFULCBiYW8gdGhhbmcgbGEga2hvbmcgZG8gZHVvYy4KICAgIGlmIHJfcGhhbmJpZXQ6CiAg',
'ICAgICAgcmV0dXJuIChLREQsIGYicGhlcCBkbyBLSE9ORyBwaGFuIGJpZXQgZHVvYzogbm9pIGJhbmcge1RIVV9OMTAhcn0g',
'bWEgdGFjaCB0aGVvICIKICAgICAgICAgICAgICAgICAgICAgZiJ7b3MucGF0aHNlcCFyfSBWQU4gdGltIHJhIGdpdC5leGUi',
'LCBrcSkKICAgIHJldHVybiAoKERBVCwgIiIsIGtxKSBpZiByX2NoaW5oIGVsc2UKICAgICAgICAgICAgKFRSVU9ULCBmInRh',
'Y2ggdGhlbyBvcy5wYXRoc2VwIHRoYXkgdmkgdGhlbyB7dGVuX3NlcH0gZHVvYyB0cnV5ZW4iLCBrcSkpCgoKZGVmIGRvX24x',
'MShnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJUcnV5ZW4gY2hhbl9kb2FuID0+IHRodSBkdW9jIHRob25nIGJhbyBWQSBzdGRl',
'cnIgSU0uIEtob25nIHRydXllbiA9PiBzdGRlcnIgVkFOIGNvLiIiIgogICAgaWYgImNoYW5fZG9hbiIgbm90IGluIHNpZy5w',
'YXJhbWV0ZXJzOgogICAgICAgIHJldHVybiBLREQsICJfZ2l0X3dpbmRvd3Mga2hvbmcgbmhhbiB0aGFtIHNvIGNoYW5fZG9h',
'biIsIHsidGhhbSBzbyI6IGxpc3Qoc2lnLnBhcmFtZXRlcnMpfQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3Rv',
'cnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQo',
'IngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGNkID0gW10KICAgICAgICBfLCBlX2NvID0gZ29pKHBhdGg9c3RyKGQp',
'LCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpLCBjaGFuX2RvYW49Y2QpCiAgICAgICAgXywgZV9raCA9IGdv',
'aShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIGtxID0geyJjaGFuX2RvYW4g',
'dGh1IGR1b2MgKG11YykiOiBsZW4oY2QpLAogICAgICAgICAgInN0ZGVyciBraGkgQ08gY2hhbl9kb2FuIChieXRlKSI6IGxl',
'bihlX2NvLmVuY29kZSgpKSwKICAgICAgICAgICJzdGRlcnIga2hpIEtIT05HIHRydXllbiAoYnl0ZSkiOiBsZW4oZV9raC5l',
'bmNvZGUoKSl9CiAgICBpZiBsZW4oY2QpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA9PSAwOgogICAgICAgIHJldHVy',
'biBLREQsICJuaGFuaCAlUHJvZ3JhbUZpbGVzJSBraG9uZyBwaGFuIGdpYWkgS0hPTkcgYmF5IHJhIGNoYW4gZG9hbiBuYW8g',
'LT4gY2h1YSBkbyBkdW9jIiwga3EKICAgIG9rID0gbGVuKGNkKSA+IDAgYW5kIGxlbihlX2NvLmVuY29kZSgpKSA9PSAwIGFu',
'ZCBsZW4oZV9raC5lbmNvZGUoKSkgPiAwCiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVs',
'c2UgInhlbSBiYW5nIiksIGtxCgpkZWYgZG9fbjEyKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkhhbmcgc2VudGluZWwgZ2l0',
'X3BhdGggdHJvbmcgZml4dHVyZSBwaGFpIHR1eWV0IGRvaSB0cmVuIENBIEhBSSBuZW4uIiIiCiAgICBuZCA9IHRlcHQucmVh',
'ZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIpCiAgICBoYW5nID0gc29ydGVkKHNldChyZS5maW5k',
'YWxsKHInZ2l0X3BhdGhccyo9XHMqIihbXiJdKykiJywgbmQpKSkKICAgIHhhdSA9IFtoIGZvciBoIGluIGhhbmcgaWYgbm90',
'IChQdXJlUG9zaXhQYXRoKGgpLmlzX2Fic29sdXRlKCkgYW5kIFB1cmVXaW5kb3dzUGF0aChoKS5pc19hYnNvbHV0ZSgpKV0K',
'ICAgIGtxID0geyJoYW5nIGdpdF9wYXRoIHRpbSB0aGF5IjogaGFuZywgImNoaSB0dXlldCBkb2kgTU9UIG5lbiI6IHhhdX0K',
'ICAgIGlmIG5vdCBoYW5nOgogICAgICAgIHJldHVybiBLREQsICJraG9uZyB0aW0gdGhheSBoYW5nIGdpdF9wYXRoIG5hbyB0',
'cm9uZyBmaXh0dXJlIC0+IG1hdSBkb2MgY28gdGhlIGRhIGRvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgeGF1IGVs',
'c2UgVFJVT1QpLCAoIiIgaWYgbm90IHhhdSBlbHNlIGYiY2hpLW1vdC1uZW46IHt4YXV9IiksIGtxCgpQUk9CRSA9IFsoIk44',
'IGJ1b2MgMSBjaGkgbmhhbiBnaXQuZXhlIiwgZG9fbjgpLAogICAgICAgICAoIk45IGJvYyBuaGF5IGtlcCBvIG11YyBQQVRI',
'IiwgZG9fbjkpLAogICAgICAgICAoIk4xMCBkYXUgJzsnIHRyb25nIHRlbiB0aHUgbXVjIiwgZG9fbjEwKSwKICAgICAgICAg',
'KCJOMTEgY2hhbiBkb2FuIGRvaSBrZW5oIiwgZG9fbjExKSwKICAgICAgICAgKCJOMTIgaGFuZyBzZW50aW5lbCB0dXlldCBk',
'b2kgQ0EgSEFJIG5lbiIsIGRvX24xMildCgojIC0tLSBjaGUgZG8gVFUgS0lFTTogY2hheSBuYW0gcHJvYmUgdHJlbiBtb3Qg',
'Y2F5IGJhdCBreSwgbmVuIGJhdCBreSAtLS0KaWYgIi0tdHUta2llbS1wcm9iZSIgaW4gc3lzLmFyZ3Y6CiAgICBfZyA9IFBh',
'dGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0tdHUta2llbS1wcm9iZSIpICsgMV0pLnJlc29sdmUoKQogICAgX3NwID0g',
'aW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX3RrIiwgc3RyKF9nLyJvcHMiLyJsZWFzZV9wdWJs',
'aXNoLnB5IikpCiAgICBfbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhl',
'Y19tb2R1bGUoX2xwKQogICAgX3NpZyA9IGluc3BlY3Quc2lnbmF0dXJlKF9scC5fZ2l0X3dpbmRvd3MpCiAgICBkZWYgX2dv',
'aSgqKmt3KToKICAgICAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRl',
'cnIoZSk6CiAgICAgICAgICAgIHJldHVybiBfbHAuX2dpdF93aW5kb3dzKCoqa3cpLCBlLmdldHZhbHVlKCkKICAgIHByaW50',
'KGYiVFUgS0lFTSBQUk9CRSB0cmVuIHtfZ30gIChuZW4ge3N5cy5wbGF0Zm9ybX0pIikKICAgIGZvciBfdGVuLCBfZiBpbiBQ',
'Uk9CRToKICAgICAgICBfdHQsIF9jdCwgX2RsID0gX2YoX2dvaSwgX3NpZywgX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVz',
'dC5weSIpCiAgICAgICAgcHJpbnQoZiIgIFt7X3R0OjE0fV0ge190ZW59IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAi',
'IikpCiAgICAgICAgZm9yIF9rLCBfdiBpbiAoX2RsIG9yIHt9KS5pdGVtcygpOiBwcmludChmIiAgICAgICAge19rOjM0fTog',
'e192fSIpCiAgICBzeXMuZXhpdCgwKQoKIyAtLS0gY2hlIGRvIEtJRU0gRE9ORyBCTzogdGVwIC5weSBuYXkgcGhhaSBUUlVO',
'RyBUVU5HIEJZVEUgdm9pIGJhbiBuaHVuZyB0cm9uZyBwczEgLS0tCiMgS2hvbmcgY29uZyBuYW8gYnVvYyBoYWkgYmFuIHNh',
'byBraG9wOiBkbyBkdW9jLCBub2kgdHJhbiAyLzQwMCAtPiA5OS85OTk5OSBDSEkgdHJvbmcgLnB5CiMgdGhpIGNpX2Rhbmdf',
'a3kgbGFuIHQyNi90MjcgdmFuIHhhbmgsIGNvbiBjaG90IFNIQSBjdWEgcHMxIGNoaSBzbyBiYW4gbmh1bmcgdm9pIGhhbmcg',
'c28KIyBjdWEgQ0hJTkggbm8uIENoYXk6IHB5dGhvbiB3cDU0MS1kby1nMi13aW5kb3dzLnB5IC0ta2llbS1kb25nLWJvIHdw',
'NTQxLWRvLWcyLnBzMSAgKHJjIDB8MykKaWYgIi0ta2llbS1kb25nLWJvIiBpbiBzeXMuYXJndjoKICAgIGltcG9ydCBiYXNl',
'NjQKICAgIF9wcyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0ta2llbS1kb25nLWJvIikgKyAxXSkucmVhZF90',
'ZXh0KGVuY29kaW5nPSJhc2NpaSIpCiAgICBfbSA9IHJlLnNlYXJjaChyIig/bXMpXlwkQjY0ID0gQFwoKC4qPyleXCkiLCBf',
'cHMpCiAgICBfayA9IHJlLnNlYXJjaChyIig/bSleXCRTaGFCb0RvXHMqPVxzKicoWzAtOWEtZl17NjR9KSciLCBfcHMpCiAg',
'ICBfbmh1bmcgPSBiYXNlNjQuYjY0ZGVjb2RlKCIiLmpvaW4ocmUuZmluZGFsbChyIicoW0EtWmEtejAtOSsvPV0qKSciLCBf',
'bS5ncm91cCgxKSkpKSBpZiBfbSBlbHNlIGIiIgogICAgX3RvaSA9IFBhdGgoX19maWxlX18pLnJlYWRfYnl0ZXMoKQogICAg',
'X29rID0gYm9vbChfbSBhbmQgX2spIGFuZCBfbmh1bmcgPT0gX3RvaSBhbmQgaGFzaGxpYi5zaGEyNTYoX3RvaSkuaGV4ZGln',
'ZXN0KCkgPT0gX2suZ3JvdXAoMSkKICAgIGlubihmIktJRU0gRE9ORyBCTzoge0RBVCBpZiBfb2sgZWxzZSBLRER9ICAobmh1',
'bmcge2xlbihfbmh1bmcpfSBieXRlLCB0ZXAge2xlbihfdG9pKX0gYnl0ZSkiKQogICAgc3lzLmV4aXQoMCBpZiBfb2sgZWxz',
'ZSAzKQoKaW5uKCI9IiAqIDc4KTsgaW5uKCJXUDU0MSBnMiAtIHBoZXAgZG8gdHJlbiBXaW5kb3dzIHRoYXQgKHNwZWMgcjM6',
'IE4xLU40LCBOOC1OMTIsIE43LCBraWNoIHRodW9jKSIpOyBpbm4oIj0iICogNzgpCgojIC0tLS0tLS0tLS0tLS0tLS0gdHUg',
'a2llbSBibyBkb2MgLS0tLS0tLS0tLS0tLS0tLQpfZCwgX2csIF90ID0gZG9jX2RvKF9NQVUpCl9vayA9IChsZW4oX2QpID09',
'IDIgYW5kIGFueSh4LnN0YXJ0c3dpdGgoInQwMmIiKSBmb3IgeCBpbiBfZCkKICAgICAgIGFuZCBub3QgYW55KHguc3RhcnRz',
'd2l0aCgidDEzMSIpIGZvciB4IGluIF9kKSBhbmQgX3QpCmlubigiVHUga2llbSBibyBkb2MgbG9nOiIsIERBVCBpZiBfb2sg',
'ZWxzZSBUUlVPVCkKaWYgbm90IF9vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogYm8gZG9jIGxvZyBjdWEg',
'Y2hpbmggc2NyaXB0IG5heSBzYWkgLT4ga2hvbmcgZG8gZ2kgY2EuIik7IHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0t',
'LS0gMC4gbmVuIGRvIC0tLS0tLS0tLS0tLS0tLS0KZ29jID0gUGF0aChzeXMuYXJndlsxXSkucmVzb2x2ZSgpIGlmIGxlbihz',
'eXMuYXJndikgPiAxIGVsc2UgUGF0aC5jd2QoKQp0ZXAsIHRlcHQgPSBnb2MgLyAib3BzIiAvICJsZWFzZV9wdWJsaXNoLnB5',
'IiwgZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaF90ZXN0LnB5Igppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjAu',
'IE5FTiBETyIpCiMgTU9JIExPRyBQSEFJIFRVIEtIQUkgbm8gZG8gQ0FJIEdJIGJhbmcgQk8gRE8gTkFPLiBCYWkgaG9jIDE5',
'LTA5LTIwMjY6IG1vdCBsdW90IGRvCiMgZ3VpIHZlIGR1b2MgZG9jIG5odSBrZXQgcXVhIGN1YSBiYW4gdmEgZGFuZyB4ZXQs',
'IG5odW5nIHRoYXQgcmEgbGEgYmFuIGRvIENVIGNoYXkKIyB0cmVuIG5oYW5oIEtIQUMuIERvYyByYSB0aGkgbWF0IG1vdCB2',
'b25nOyBsb2cgdHUga2hhaSB0aGkgdGhheSBuZ2F5IGRvbmcgZGF1Lgp0cnk6CiAgICBfdHUgPSBoYXNobGliLnNoYTI1NihQ',
'YXRoKF9fZmlsZV9fKS5yZWFkX2J5dGVzKCkpLmhleGRpZ2VzdCgpCmV4Y2VwdCBFeGNlcHRpb24gYXMgX2U6CiAgICBfdHUg',
'PSBmImtob25nIHR1IGJhbSBkdW9jOiB7X2V9IgpnaGkoImJvX2RvX3NoYTI1NiIsIF90dSkKaW5uKGYiICBCTyBETyAgICAg',
'ICAgOiBzaGEyNTYge190dVs6MTZdfSAgKGJhbiB7QkFOX0JPX0RPfSkiKQppbm4oIiAgc3lzLnBsYXRmb3JtIDoiLCBzeXMu',
'cGxhdGZvcm0sICJ8IHB5dGhvbiIsIHN5cy52ZXJzaW9uLnNwbGl0KClbMF0pCmlubigiICBvcy5wYXRoc2VwICAgOiIsIHJl',
'cHIob3MucGF0aHNlcCksICJ8IFBBVEhFWFQ6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUEFUSEVYVCIpKVs6NjBdKQppbm4o',
'IiAgUHJvZ3JhbUZpbGVzIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQcm9ncmFtRmlsZXMiKSksICJ8IFN5c3RlbVJvb3Q6',
'IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiU3lzdGVtUm9vdCIpKSkKaW5uKCIgIENPTkdfQ1VfR0lUICA6IiwgcmVwcihvcy5l',
'bnZpcm9uLmdldCgiQ09OR19DVV9HSVQiKSkpCmlubigiICBnb2Mga2hvICAgICAgOiIsIGdvYykKCnF1eWVuID0gTm9uZQpp',
'ZiBzeXMucGxhdGZvcm0gPT0gIndpbjMyIjoKICAgIHRyeToKICAgICAgICBpbXBvcnQgY3R5cGVzOyBxdXllbiA9IGJvb2wo',
'Y3R5cGVzLndpbmRsbC5zaGVsbDMyLklzVXNlckFuQWRtaW4oKSkKICAgIGV4Y2VwdCBFeGNlcHRpb246IHF1eWVuID0gTm9u',
'ZQpnaGkoInF1eWVuX2FkbWluIiwgcXV5ZW4pCnN5bWxpbmtfZHVvYyA9IE5vbmUKdHJ5OgogICAgd2l0aCB0ZW1wZmlsZS5U',
'ZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJhLnR4dCI7IGQud3JpdGVfdGV4dCgieCIs',
'IGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgdHJ5OiBvcy5zeW1saW5rKHN0cihkKSwgc3RyKFBhdGgodCkvImxrIikpOyBz',
'eW1saW5rX2R1b2MgPSBUcnVlCiAgICAgICAgZXhjZXB0IE9TRXJyb3IgYXMgZTogc3ltbGlua19kdW9jID0gRmFsc2U7IGdo',
'aSgic3ltbGlua19sb2kiLCBmInt0eXBlKGUpLl9fbmFtZV9ffToge2V9IikKZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOiBnaGko',
'InN5bWxpbmtfbG9pIiwgc3RyKGUpKQpnaGkoInN5bWxpbmtfZHVvYyIsIHN5bWxpbmtfZHVvYykKaW5uKCIgIEFkbWluaXN0',
'cmF0b3I6IiwgcXV5ZW4sICJ8IHRhbyBzeW1saW5rIGR1b2M6Iiwgc3ltbGlua19kdW9jKQoKbG9pID0gW10KIyBDb25nIGtp',
'Y2ggdGh1b2MgbGEgcGhlcCBkbyB0cmVuIExJQ0ggU1UgR0lULCBraG9uZyBkaW5oIGdpIGRlbiBuZW4uIENobyBwaGVwCiMg',
'LS1jaGkta2ljaC10aHVvYyBjaGF5IG8gbW9pIG5lbiBkZSBjb24gVFUgS0lFTSBkdW9jIGNoaW5oIGNvbmcgbmF5IChkYSBk',
'dW5nCiMgZGUgdGFpIGR1bmcgY2EgaGFpIHZlIGN1YSBzdSBjbyBuZW4tY3UgMTktMDkpLiBNb2kgY2hvdCBDSFVDIE5BTkcg',
'dmFuIGRvaSBXaW5kb3dzLgppZiBzeXMucGxhdGZvcm0gIT0gIndpbjMyIiBhbmQgIi0tY2hpLWtpY2gtdGh1b2MiIG5vdCBp',
'biBzeXMuYXJndjoKICAgIGxvaS5hcHBlbmQoZiJLSE9ORyBwaGFpIFdpbmRvd3MgKHN5cy5wbGF0Zm9ybT17c3lzLnBsYXRm',
'b3JtIXJ9KSIpCmlmIG5vdCB0ZXAuaXNfZmlsZSgpOiAgbG9pLmFwcGVuZChmImtob25nIHRoYXkge3RlcH0iKQppZiBub3Qg',
'dGVwdC5pc19maWxlKCk6IGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB0fSIpCmlmIG5vdCBzaHV0aWwud2hpY2goImdp',
'dCIpOiBsb2kuYXBwZW5kKCJraG9uZyBjbyBgZ2l0YCB0cm9uZyBQQVRIIikKIyBCbyB0ZXN0IChtdWMgMiB2YSBONykgY2Fu',
'IFB5WUFNTDogdGhpZXUgbm8sIDBlYTk1ZGUgcmEgOTYvMTY2IGNhIERPICg4OSBiYW8gdGhhbmcgIk5vIG1vZHVsZSBuYW1l',
'ZCAneWFtbCciLAojIDcgcXVhIGx1b3QgY29uOyBjbyBQeVlBTUw6IDE2Ni8xNjYgUVVBKS4gQm8gZG8gZ29pIGNodW5nIGxh',
'ICJjYSBETyBMQSIgcm9pIHBoYXQgVFJVT1Qg4oCUIGRvIHRyZW4gMjAyNi0wOS0zMGMuCiMgRGlldSBraWVuIHRpZW4gcXV5',
'ZXQgcGhhaSBob2kgYmFuZyBDSElOSCB0aWVuIHRyaW5oIGNvbiBzZSBjaGF5IGJvIHRlc3QgKGNoYXkoKTogY3VuZyBtb2kg',
'dHJ1b25nOyBjd2QgPSBvcHMvID0KIyBzeXMucGF0aFswXSBjdWEgYm8gdGVzdCkgdmEgaG9pIERVTkcgRFVPQyBjaHUga2hv',
'bmcgaG9pIENPIE1BVC4gQmFuIDMwZCBob2kgYGZpbmRfc3BlYygieWFtbCIpYCBvIHRpZW4gdHJpbmgKIyBOQVkgdmEgbmd1',
'b25nIDMuOCBzdXkgdHUgTkdVIFBIQVAgKGA6PWApIOKAlCBkbyB0cmVuIDIwMjYtMDktMzBkLCBjYSBoYWkgcmEgcmM9MSBU',
'UlVPVCBjaG8gdW5nIHZpZW4gc2FjaDoKIyB0aHUgbXVjIGR1IGxpZXUgYHlhbWwvYCB0cmVuIFBZVEhPTlBBVEggcXVhIGZp',
'bmRfc3BlYyBtYSBgeWFtbC5zYWZlX2R1bXBgIGtob25nIGNvICg4NyBjYSAibGEiKTsgcHl0aG9uIDMuOC4yMAojIFRIQVQg',
'Y28gUHlZQU1MLCBibyB0ZXN0IGR1bmcgYHN0ci5yZW1vdmVwcmVmaXhgICgzLjkpIGx1YyBDSEFZICgzMyBjYSAibGEiOyAz',
'LjkuMjM6IDE2Ni8xNjYpLgppZiBub3QgKCItLWNoaS1raWNoLXRodW9jIiBpbiBzeXMuYXJndiBvciAiLS1jaGktcHJvYmUi',
'IGluIHN5cy5hcmd2KToKICAgIF9yY19kaywgX3JhX2RrID0gY2hheShbIi1jIiwgImltcG9ydCBzeXM7IHN5cy5leGl0KDkp',
'IGlmIHN5cy52ZXJzaW9uX2luZm8gPCAoMywgOSkgZWxzZSBOb25lOyBpbXBvcnQgeWFtbDsiCiAgICAgICAgICAgICAgICAg',
'ICAgICAgICAgICAgICAgICIgeWFtbC5zYWZlX2R1bXAoeWFtbC5zYWZlX2xvYWQoJ2E6IDEnKSkiXSwKICAgICAgICAgICAg',
'ICAgICAgICAgICAgICBnb2MgLyAib3BzIiBpZiAoZ29jIC8gIm9wcyIpLmlzX2RpcigpIGVsc2UgUGF0aC5jd2QoKSwgcGh1',
'dD0yKQogICAgaWYgX3JjX2RrID09IDk6CiAgICAgICAgbG9pLmFwcGVuZChmInB5dGhvbiB7c3lzLnZlcnNpb24uc3BsaXQo',
'KVswXX0gPCAzLjk6IGJvIHRlc3QgY3VhIHVuZyB2aWVuIGR1bmcgc3RyLnJlbW92ZXByZWZpeCAoMy45KSBsdWMgQ0hBWSIp',
'CiAgICBlbGlmIF9yY19kazoKICAgICAgICBsb2kuYXBwZW5kKGYicHl0aG9uIG5heSBLSE9ORyBjbyBQeVlBTUwgZHVuZyBk',
'dW9jICh7KF9yYV9kay5zdHJpcCgpLnNwbGl0bGluZXMoKSBvciBbJyddKVstMV1bOjkwXX0pOiIKICAgICAgICAgICAgICAg',
'ICAgIGYiIFwie3N5cy5leGVjdXRhYmxlfVwiIC1tIHBpcCBpbnN0YWxsIHB5eWFtbCIKICAgICAgICAgICAgICAgICAgICIg',
'KGJhbiBuaHVuZyBwczEgdHUgdGFpIEtIT05HIGNvIHBpcDogY2hheSBsYWkgdm9pIC1QeSA8cHl0aG9uIGRhIGNvIFB5WUFN',
'TD4pIikKCnJjLCBoZWFkLCBfID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxvaS5hcHBlbmQoImto',
'b25nIGRvYyBkdW9jIEhFQUQiKQpnaGkoImhlYWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywgIm1lcmdlLWJhc2Ui',
'LCAiLS1pcy1hbmNlc3RvciIsIFNIQV9HMSwgaGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNfYSA9PSAwKQppZiBo',
'ZWFkID09IFNIQV9HMToKICAgIHRoZV9oZSA9ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gREFZIExBIGcx',
'LiBDSFVBIGNvIGJhbiB2YSBnMjsga2V0IHF1YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9kdWU6CiAgICB0aGVf',
'aGUgPSAiZzIiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hBX0cxWzo4XX0pOyB1',
'bmcgdmllbiBnMiBoYXkga2hvbmc6IE43JyAobXVjIDEpIGRpbmggZGFuaC4iKQplbHNlOgogICAgdGhlX2hlID0gIj8iOyBs',
'b2kuYXBwZW5kKGYiSEVBRD17aGVhZFs6OF19IEtIT05HIHBoYWkgZzEgdmEgS0hPTkcgcGhhaSBoYXUgZHVlIGN1YSB7U0hB',
'X0cxWzo4XX0g4oCUIHJlYmFzZT8gbmhhbSBuaGFuaD8iKQpnaGkoInRoZV9oZSIsIHRoZV9oZSkKcmNfciwgcmVmcywgXyA9',
'IGdpdChnb2MsICJmb3ItZWFjaC1yZWYiLCAiLS1wb2ludHMtYXQiLCBoZWFkIG9yICJIRUFEIiwKICAgICAgICAgICAgICAg',
'ICAgICAiLS1mb3JtYXQ9JShyZWZuYW1lOnNob3J0KSIpCmRzciA9IFt4IGZvciB4IGluIHJlZnMuc3BsaXRsaW5lcygpIGlm',
'IHguc3RyaXAoKSBhbmQgeC5zdHJpcCgpICE9ICJkby10YW0iXQpnaGkoInJlZl90cm9fdG9pX2hlYWQiLCBkc3IpCmlubihm',
'IiAgcmVmIHRybyB0b2kgSEVBRDogeycsICcuam9pbihkc3IpIGlmIGRzciBlbHNlICcoa2hvbmcgcmVmIG5hbyAtIEhFQUQg',
'cm9pIHR1IGRvKSd9IikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogbmVuIGRvIHNhaSwgS0hP',
'TkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlubigiICAtIiwgeCkKICAgIHN5cy5leGl0KDMpCgoj',
'IC0tLS0tLS0tLS0tLS0tLS0gMS4ga2ljaCB0aHVvYyAoTjcnIGN1YSBzcGVjIHIzKSAtLS0tLS0tLS0tLS0tLS0tCmlubigi',
'Iik7IGlubigiLSIgKiA3OCk7IGlubigiMS4gS0lDSCBUSFVPQyDigJQgdHJhbiBzcGVjIHIzOiA8PSAyIHRlcCB2YSA8PSA0',
'MDAgZG9uZyB0aGVtIikKIyBWRSBORU4gUEhBSSBUVU9JIOKAlCB2YSBwaGFpIENIVU5HIE1JTkggZHVvYyBsYSB0dW9pLCBr',
'aG9uZyBwaGFpIGdpYSBkaW5oLgojIEJhaSBob2MgdHJhIGdpYSAxOS0wOS0yMDI2OiBjbG9uZSB0YWkgZHVuZyBjaGkgZmV0',
'Y2ggbmhhbmggYmFuIHZhLCBgb3JpZ2luL21hc3RlcmAKIyBkdW5nIHllbiB0dSAxNC0wOSAoYzE2YmQzMiwgc2F1IDk3IGNv',
'bW1pdCkuIG1lcmdlLWJhc2Ugcm9pIHZlIGR1bmcgZGluaCBtYXN0ZXIgY3UsCiMgbmVuIGRpZmYgTlVPVCBjYSA5NyBjb21t',
'aXQgbWFzdGVyOiBkbyByYSA0NiB0ZXAgLyArNzExOCB0aGF5IHZpIDIgdGVwIC8gKzM5NyDigJQKIyBDVU5HIE1PVCBDT01N',
'SVQgMGVhOTVkZS4gTW90IHRpZXUgY2hpIERFTFRBIG1hIHZlIG5lbiBraG9uZyB0dW9pIHRoaSBraG9uZyBzYWkKIyBsZWNo',
'IG1vdCBjaHV0LCBubyBzYWkgY2EgbW90IGJhYyBkbyBsb24uCiMgQ2hvIG5lbjogbmVuIGtob25nIGNodW5nIG1pbmggZHVv',
'YyBsYSB0dW9pID0+IEtIT05HIERPIERVT0MgKHJjPTMpLCBLSE9ORyBwaGFpIFRSVU9ULgojIFRSVU9UIGxhIG1vdCBQSEFO',
'IFFVWUVUIHZlIGJhbiB2YTsgcGhhbiBxdXlldCBjaGkgZHVvYyBwaGVwIHBoYXQgcmEga2hpIGRhIGRvIGR1b2MuCnJjX3Us',
'IHVybF90aG8sIF8gPSBnaXQoZ29jLCAicmVtb3RlIiwgImdldC11cmwiLCAib3JpZ2luIikKdXJsX28sIHVybF9pbiA9IF91',
'cmxfc2FjaCh1cmxfdGhvKSwgX3VybF9pbih1cmxfdGhvKQpnaGkoIm9yaWdpbl91cmwiLCB1cmxfaW4pOyBpbm4oZiIgIG9y',
'aWdpbiAgICAgICA6IHt1cmxfaW4gb3IgJyhraG9uZyBkb2MgZHVvYyknfSIpCnVybF9vayA9IChub3QgcmNfdSkgYW5kIHVy',
'bF9vLnJzdHJpcCgiLyIpIGluIFVSTF9LSE9fSE9QX0xFCnJjX2xyLCBvdXRfbHIsIGVyX2xyID0gZ2l0KGdvYywgImxzLXJl',
'bW90ZSIsICJvcmlnaW4iLCAicmVmcy9oZWFkcy9tYXN0ZXIiKSBpZiB1cmxfb2sgZWxzZSAoMSwgIiIsICIiKQplcl9sciA9',
'IF9hbl91c2VyaW5mbyhlcl9scikKcmNfbG0sIGxtLCBlcl9sbSAgICAgPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIm9yaWdp',
'bi9tYXN0ZXIiKQpybSA9IG91dF9sci5zcGxpdCgpWzBdIGlmIChub3QgcmNfbHIgYW5kIG91dF9sci5zdHJpcCgpKSBlbHNl',
'ICIiCmlmIG5vdCB1cmxfb2s6CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmIm9yaWdpbj17dXJsX2luIXJ9IEtI',
'T05HIHBoYWkga2hvIHRoYXQg4oCUICd0dW9pJyBzbyB2b2kgbm8ga2hvbmcgY2h1bmcgbWluaCBkdW9jIGdpIikKICAgIHJj',
'X21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgbm90IHJtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtE',
'RCwKICAgICAgICBmImtob25nIGhvaSBkdW9jIG1hc3RlciB0cmVuIHJlbW90ZSAobHMtcmVtb3RlIHJjPXtyY19scn0pOiB7',
'ZXJfbHJbOjYwXX0gIgogICAgICAgIGYi4oCUIGtob25nIGNodW5nIG1pbmggZHVvYyB2ZSBuZW4gY29uIHR1b2kiKQogICAg',
'cmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiByY19sbSBvciBub3QgbG06CiAgICBrZXQoIk43JyBraWNo',
'IHRodW9jIiwgS0RELCBmImtob25nIGRvYyBkdW9jIG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmU6IHtlcl9sbVs6NjBdfSIp',
'CiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIGxtICE9IHJtOgogICAgIyBEZW0geGVtIHR1dCBs',
'YWkgYmFvIHhhLCBuZXUgZGVtIGR1b2Mg4oCUIGNvbiBzbyBuYXkgbm9pIHJvIG11YyBkbyBzYWkgbGVjaC4KICAgIHJjX2Ms',
'IHNhdSwgXyA9IGdpdChnb2MsICJyZXYtbGlzdCIsICItLWNvdW50IiwgZiJ7bG19Li57cm19IikKICAgIHhhID0gZiIsIHR1',
'dCBsYWkge3NhdX0gY29tbWl0IiBpZiAobm90IHJjX2MgYW5kIHNhdS5zdHJpcCgpLmlzZGlnaXQoKSkgZWxzZSAiIgogICAg',
'aW5uKGYiICBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25lIDoge2xtWzoxMl19IikKICAgIGlubihmIiAgbWFzdGVyIHRyZW4g',
'cmVtb3RlICAgICAgICA6IHtybVs6MTJdfXt4YX0iKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVy',
'X3JlbW90ZSIsIHJtKQogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwKICAgICAgICBmInZlIG5lbiBDVTogb3JpZ2lu',
'L21hc3Rlcj17bG1bOjEyXX0gIT0gcmVtb3RlPXtybVs6MTJdfXt4YX0gIgogICAgICAgIGYi4oCUIGNoYXkgYGdpdCAtQyA8',
'a2hvPiBmZXRjaCBvcmlnaW4gbWFzdGVyYCByb2kgZG8gbGFpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIi',
'LCAxCmVsc2U6CiAgICBpbm4oZiIgIHZlIG5lbiBUVU9JOiBvcmlnaW4vbWFzdGVyID0ge2xtWzoxMl19ID09IG1hc3RlciB0',
'cmVuIHJlbW90ZSIpCiAgICBnaGkoIm1hc3Rlcl9jbG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICBy',
'Y19tYiwgbWIsIGVyX21iID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAib3JpZ2luL21hc3RlciIsIGhlYWQpCmlmIHJjX21i',
'IG9yIG5vdCBtYjoKICAgIGlmIG1iID09ICIiIGFuZCBybSBhbmQgbG0gPT0gcm06CiAgICAgICAga2V0KCJONycga2ljaCB0',
'aHVvYyIsIEtERCwgZiJraG9uZyB0aW5oIGR1b2MgbWVyZ2UtYmFzZSB2b2kgb3JpZ2luL21hc3Rlcjoge2VyX21iWzo3MF19',
'IikKICAgIG5zLCByYyA9ICIiLCAxCmVsc2U6CiAgICBnaGkoIm1lcmdlX2Jhc2UiLCBtYikKICAgIGlubihmIiAgbWVyZ2Ut',
'YmFzZShvcmlnaW4vbWFzdGVyLCBIRUFEKSA9IHttYls6MTJdfSIpCiAgICBpZiBtYiAhPSBTSEFfQkFTRV9TUEVDOgogICAg',
'ICAgIGlubihmIiAgTFVVIFk6IGtoYWMgYmFzZSBtYSBzcGVjIHIzIGtoYWkgKHtTSEFfQkFTRV9TUEVDWzoxMl19KSDigJQg',
'dmkgbmhhbmggZGEgbWVyZ2UgbWFzdGVyLiIpCiAgICAgICAgaW5uKCIgICAgICAgICBEbyBzbyBiYXNlIGN1IHNlIE5VT1Qg',
'cGhhbiBtYXN0ZXIgbWFuZyB2YW8uIER1bmcgbWVyZ2UtYmFzZSBtb2kgbGEgdmllYyBjdWEgZXhlY3V0b3IuIikKICAgICAg',
'ICByY194LCBuc194LCBfID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgU0hBX0JBU0VfU1BFQywgaGVhZCkKICAg',
'ICAgICBpZiBub3QgcmNfeDoKICAgICAgICAgICAgaCA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zX3guc3BsaXRsaW5l',
'cygpIGlmIGwuc3RyaXAoKV0KICAgICAgICAgICAgYSA9IHN1bShpbnQoeFswXSkgZm9yIHggaW4gaCBpZiB4WzBdLmlzZGln',
'aXQoKSkKICAgICAgICAgICAgZ2hpKCJudW1zdGF0X3RoZW9fYmFzZV9zcGVjIiwgeyJ0ZXAiOiBsZW4oaCksICJ0aGVtIjog',
'YX0pCiAgICAgICAgICAgIGlubihmIiAgICAgICAgIChkb2kgY2hpZXU6IHNvIGJhc2Ugc3BlYyA9IHtsZW4oaCl9IHRlcCAv',
'ICt7YX0g4oCUIGNvbiBzbyBheSBLSE9ORyBkdW5nIGRlIGNoYW0pIikKICAgIHJjLCBucywgZXIgPSBnaXQoZ29jLCAiZGlm',
'ZiIsICItLW51bXN0YXQiLCBtYiwgaGVhZCkKaWYgcmM6CiAgICBwYXNzCmVsc2U6CiAgICBoYW5nID0gW2wuc3BsaXQoIlx0',
'IikgZm9yIGwgaW4gbnMuc3BsaXRsaW5lcygpIGlmIGwuc3RyaXAoKV0KICAgIHRoZW0gPSBzdW0oaW50KGhbMF0pIGZvciBo',
'IGluIGhhbmcgaWYgaFswXS5pc2RpZ2l0KCkpCiAgICB4b2EgID0gc3VtKGludChoWzFdKSBmb3IgaCBpbiBoYW5nIGlmIGhb',
'MV0uaXNkaWdpdCgpKQogICAgZ2hpKCJzb190ZXAiLCBsZW4oaGFuZykpOyBnaGkoImRvbmdfdGhlbSIsIHRoZW0pOyBnaGko',
'ImRvbmdfeG9hIiwgeG9hKQogICAgZm9yIGggaW4gaGFuZzogaW5uKGYiICAgIHtoWzJdOjM0fSAre2hbMF06PDV9IC17aFsx',
'XX0iKQogICAgaW5uKGYiICAgIFRPTkc6IHtsZW4oaGFuZyl9IHRlcCwgK3t0aGVtfSwgLXt4b2F9ICAgKHRyYW46IHtUUkFO',
'X1RFUH0gdGVwIC8ge1RSQU5fRE9OR30gZG9uZyB0aGVtKSIpCiAgICBjaGFtID0gc29ydGVkKHtoWzJdIGZvciBoIGluIGhh',
'bmd9ICYgV1JJVEVfU0VUX0cyKTsgZ2hpKCJjaGFtX3dyaXRlX3NldCIsIGNoYW0pCiAgICBkZWYgX2NhX21vaV9jbyhyZXYp',
'OgogICAgICAgIHJfLCBuZF8sIF8gPSBnaXQoZ29jLCAic2hvdyIsIGYie3Jldn06b3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5w',
'eSIpCiAgICAgICAgcmV0dXJuIE5vbmUgaWYgcl8gZWxzZSB7dCBmb3IgdCBpbiBDQV9NT0lfRzIgaWYgcmUuc2VhcmNoKHIi',
'KD9tKV5kZWYgIiArIHQgKyByIlthLXpdP18iLCBuZF8pfQogICAgb19tYiwgb19oID0gX2NhX21vaV9jbyhtYiksIF9jYV9t',
'b2lfY28oaGVhZCkKICAgIG1hbmcgPSBzb3J0ZWQob19oIC0gb19tYiwga2V5PXNvX2NhKSBpZiAob19tYiBpcyBub3QgTm9u',
'ZSBhbmQgb19oIGlzIG5vdCBOb25lKSBlbHNlIE5vbmUKICAgIGdoaSgiY2FfbW9pX2cyX21hbmdfdmFvIiwgbWFuZykKICAg',
'IGlmIG5vdCBtYW5nOgogICAgICAgICMgRG8gUk9ORyAoZGEgbGFuZCwgY2hpbmggbWFzdGVyKSwgbmhhbSBuaGFuaCwgaGF5',
'IG5oYW5oIGN1YSBwYWNrZXQgS0hBQyBjaGFtIGN1bmcgdGVwOgogICAgICAgICMga2hvbmcgbWFuZyBjYSBtb2kgbmFvIGN1',
'YSBnMiB0aGkga2hvbmcgcGhhaSB1bmcgdmllbi4gRG9jIGtob25nIGR1b2MgKE5vbmUpIGN1bmcgdmF5LgogICAgICAgIGtl',
'dCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYiZG9pIHR1b25nIGtob25nIHBoYWkgdW5nIHZpZW46IHtsZW4oaGFuZyl9IHRl',
'cCwgY2hhbSB7Y2hhbX0sIGNhIG1vaSAiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZiJnMiBtYW5nIHZh',
'byB7bWFuZyFyfSDigJQgZGEgbGFuZD8gbmhhbSBuaGFuaD8gcGFja2V0IGtoYWM/IikKICAgIGVsc2U6CiAgICAgICAga2V0',
'KCJONycga2ljaCB0aHVvYyIsIERBVCBpZiAobGVuKGhhbmcpIDw9IFRSQU5fVEVQIGFuZCB0aGVtIDw9IFRSQU5fRE9ORykg',
'ZWxzZSBUUlVPVCwKICAgICAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IikKCiMgRGluaCBkYW5oIFRIQVQg',
'bmFtIG8gTjcnIChjYSBtb2kgZzIgbWFuZyB2YW8pLCBLSE9ORyBvICJoYXUgZHVlIGcxIjogZzEgZGEgbGFuZCBuZW4gbW9p',
'IG5oYW5oIGRldQojIGxhIGhhdSBkdWUuIERvbmcgZGF1IGtob2kgZGFuIHBoYWkgdHUga2hhaSB0aGVvIGtldCBxdWEgYXkg',
'KGRvIGR1b2M6IG1hc3RlciA0NDYyMGU4IG1vIGtob2kgYmFuZwojICJUSEUgSEUgRE8gRFVPQzogZzIiLCBKU09OICJ0aGVf',
'aGUiOiAiZzIiLCB0cm9uZyBraGkgTjcnIGRhIGtldCBsdWFuICJraG9uZyBwaGFpIHVuZyB2aWVuIikuCiMgTmhhbiBjaGkg',
'ZHVvYyBub2kgRFVORyBjYWkgZG8gZHVvYzogYFtdYCBraG9uZyB0YWNoICJkYSBsYW5kIiBraG9pICJuaGFtIG5oYW5oIi8i',
'cGFja2V0IGtoYWMiIChkbwojIGR1b2MgdHJlbiAyMDI2LTA5LTMwYjogdW5nIHZpZW4gMmE2Nzk2OCBEQSBMQU5EIGJpIGdv',
'aSAiS0hPTkcgcGhhaSB1bmcgdmllbiBnMiIpLgppZiB0aGVfaGUgPT0gImcyIiBhbmQgbm90IHNvLmdldCgiY2FfbW9pX2cy',
'X21hbmdfdmFvIik6CiAgICB0aGVfaGUgPSAoIktIT05HIG1hbmcgY2EgbW9pIGcyIG5hbyAoZGEgbGFuZD8gbmhhbSBuaGFu',
'aD8gcGFja2V0IGtoYWM/KSIgaWYgc28uZ2V0KCJjYV9tb2lfZzJfbWFuZ192YW8iKSA9PSBbXQogICAgICAgICAgICAgIGVs',
'c2UgImcyPyAoQ0hVQSBkaW5oIGRhbmggZHVvYyBkb2kgdHVvbmcpIikKICAgIGdoaSgidGhlX2hlIiwgdGhlX2hlKQoKIyBD',
'b25nIG5oYW5oOiBkbyBSSUVORyBraWNoIHRodW9jICh2YWkgZ2lheSkgcm9pIGR1bmcuIER1bmcga2hpIGNhbiB4YWMgbWlu',
'aCBsYWkKIyB2ZSBuZW4gbWEga2hvbmcgbXVvbiB0cmEgMjAtNDUgcGh1dCBjaG8gY2EgYm8gdGVzdC4KaWYgIi0tY2hpLWtp',
'Y2gtdGh1b2MiIGluIHN5cy5hcmd2OgogICAgaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQogICAgaW5uKCItLWNoaS1raWNoLXRo',
'dW9jOiBDSEkgZG8gY29uZyBraWNoIHRodW9jLiBEYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCiAgICBp',
'bm4oIi0iICogNzgpCiAgICBmb3IgX3QsIF90dCwgX2N0IGluIGNob3Q6IGlubihmIiAge190dDoxNH0ge190fSIgKyAoZiIg',
'ICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgX2sgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0RE',
'KQogICAgX3IgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCiAgICBzeXMuZXhpdCgzIGlmIF9r',
'IGVsc2UgKDEgaWYgX3IgZWxzZSAwKSkKCkNISV9QUk9CRSA9ICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YgICAgIyBibyBx',
'dWEgYm8gdGVzdCArIE43OyBnaXUgMCwgMSwgMwojIC0tLS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVzdCBkYXkgZHUgLS0tLS0t',
'LS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIyLiBCTyBURVNU',
'IERBWSBEVSAoMTAtNDAgcGh1dCkiKQogICAgcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5w',
'eSJdLCBnb2MpCiAgICBnaGkoInJjX3N1aXRlIiwgcmNfbikKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXRfbikKICAgIGlu',
'bigiICByYyA9IiwgcmNfbiwgInwiLCBtLmdyb3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBr',
'ZXQpIikKICAgIGlmIG06CiAgICAgICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGkoInRyZW4iLCBpbnQobS5n',
'cm91cCgyKSkpOyBnaGkoImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKICAgIGRvX2hldCwgZ2MsIHRpbiA9IGRvY19k',
'byhvdXRfbikKICAgIGdoaSgic29fY2FfZG8iLCBsZW4oZG9faGV0KSk7IGdoaSgibGlldF9rZV9kYXlfZHUiLCB0aW4pCiAg',
'ICBmb3IgZyBpbiBnYzogaW5uKCIgICAqIiwgZykKICAgIGlubigiIik7IGlubihmIiAgPT09IHtsZW4oZG9faGV0KX0gQ0Eg',
'RE8gPT09IikKICAgIGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaW5uKGYiICAge3Quc3Bs',
'aXQoJ18nKVswXTo3fSB7dH0iKTsgaW5uKGYiICAgICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCiAgICBnaGkoImRvX2x5',
'X2RvIiwge3Q6IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQogICAgIyAtLS0tIENIT1Q6IG1vaSBjYSBETyBw',
'aGFpIEdJQUkgVEhJQ0ggRFVPQyAtLS0tCiAgICAjIFRoaWV1IGNob3QgbmF5LCBibyBkbyBpbiBkYW5oIHNhY2ggZG8gcm9p',
'IHZhbiB0aG9hdCByYz0wLiBEbyBkdW5nIGxhIGxvaSBkYSB4YXkgcmE6CiAgICAjIGx1b3QgV2luZG93cyAxOS0wOSBjbyB0',
'MTcxIERPIG1hIGJvIGRvIGJhbyAiREFUIDEwIHwgVFJVT1QgMCIgdmEgcmM9MC4KICAgIGRlZiBfa2hvYSh0KTogcmV0dXJu',
'IHQuc3BsaXQoIl8iKVswXQogICAgZG9fcGFja2V0LCBkb19sYSwgZG9fdGhpZXVfY29uZ19jdSA9IFtdLCBbXSwgW10KICAg',
'IGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaywgbHkgPSBfa2hvYSh0KSwgZG9faGV0W3Rd',
'CiAgICAgICAgaWYgayBpbiBDQV9QQUNLRVQ6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fcGFja2V0LmFwcGVu',
'ZCh0KQogICAgICAgIGVsaWYgIktIw5RORyDEkE8gxJDGr+G7okMiIGluIGx5IG9yICJ0aGnhur91IGAiIGluIGx5OiAgZG9f',
'dGhpZXVfY29uZ19jdS5hcHBlbmQodCkKICAgICAgICBlbGlmIGsgaW4gTkdPQUlfUEhBTV9WSTogICAgICAgICAgICAgICAg',
'ICAgICAgICBwYXNzCiAgICAgICAgZWxzZTogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9f',
'bGEuYXBwZW5kKHQpCiAgICBnaGkoImRvX3BhY2tldCIsIGRvX3BhY2tldCk7IGdoaSgiZG9fbGEiLCBkb19sYSk7IGdoaSgi',
'ZG9fdGhpZXVfY29uZ19jdSIsIGRvX3RoaWV1X2NvbmdfY3UpCiAgICBpbm4oIiIpCiAgICBpbm4oZiIgIGNhIERPIHRodW9j',
'IENISU5IIHBhY2tldCBuYXkgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF0gb3IgJ2tob25nIGNvJ30iKQogICAg',
'aW5uKGYiICBjYSBETyBuZ29haSBwaGFtIHZpIChyMyBraGFpKToge1tfa2hvYSh4KSBmb3IgeCBpbiBzb3J0ZWQoZG9faGV0',
'LCBrZXk9c29fY2EpIGlmIF9raG9hKHgpIGluIE5HT0FJX1BIQU1fVkldfSIpCiAgICBpbm4oZiIgIGNhIERPIHZpIFRISUVV',
'IENPTkcgQ1UgICAgICAgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9yICdraG9uZyBjbyd9IikK',
'ICAgIGlubihmIiAgY2EgRE8gTEEgKGtob25nIGdpYWkgdGhpY2ggZHVvYyk6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFd',
'IG9yICdraG9uZyBjbyd9IikKICAgICMgLS0tLSBDSE9UOiBwaGVwIGRvIHBoYWkgVFJPTiB0cnVvYyBraGkgbW90IGNodSBE',
'QVQgbmFvIGR1b2MgcGhhdCAtLS0tCiAgICAjIEJhbiB0cnVvYyBjaGkgSU4gYHRpbmAvYHJjX3N1aXRlYDogYm8gdGVzdCBj',
'aGV0IGdpdWEgdDE3MSAocmM9MTM0LCBraG9uZyBkb25nIHRvbmcpCiAgICAjIHZhbiByYSAiREFUIDEyIHwgVFJVT1QgMCIg',
'cmM9MDsgY2EgUEFDS0VUIHZhbmcgbWF0IGhheSBiaSBCTyBRVUEgY3VuZyBkdW9jIGNoYW0gbmh1CiAgICAjICJraG9uZyBk',
'byIuIFZhbmcgbWF0IGtob25nIHBoYWkgImtob25nIGRvIiDigJQgbGEgS0hPTkcgRE8gRFVPQy4KICAgIHZhbmcgPSBbdCBm',
'b3IgdCBpbiBzb3J0ZWQoQ0FfUEFDS0VULCBrZXk9c29fY2EpIGlmIG1hdV9jYShvdXRfbiwgdCkgbm90IGluICgiUVVBIiwg',
'IkRPIildCiAgICBseV9rZGQgPSBbXQogICAgaWYgbm90IHRpbjogbHlfa2RkLmFwcGVuZCgiZGFuaCBzYWNoIGRvIEtIT05H',
'IGRheSBkdSIpCiAgICBpZiByY19uIG5vdCBpbiAoMCwgMSkgb3IgKHJjX24gPT0gMSkgIT0gYm9vbChkb19oZXQpOgogICAg',
'ICAgIGx5X2tkZC5hcHBlbmQoZiJyYyBibyB0ZXN0PXtyY19ufSBraG9uZyBraG9wIHtsZW4oZG9faGV0KX0gY2EgRE8gZG9j',
'IGR1b2MiKQogICAgaWYgdmFuZzogbHlfa2RkLmFwcGVuZChmImNhIFBBQ0tFVCB2YW5nL2JvIHF1YToge3Zhbmd9IikKICAg',
'IGdoaSgiY2FfcGFja2V0X3ZhbmciLCB2YW5nKTsgZ2hpKCJseV9kb19jaHVhX3Ryb24iLCBseV9rZGQpCiAgICBpZiBseV9r',
'ZGQ6IGtldCgiQm8gdGVzdCBjaGF5IFRST04gdmEgZG9jIERVIiwgS0RELCAiOyAiLmpvaW4obHlfa2RkKSkKICAgIGNodWFf',
'dHJvbiA9IEtERCBpZiBseV9rZGQgZWxzZSBEQVQKICAgIGtldCgiS2hvbmcgY2EgbmFvIGN1YSBQQUNLRVQgYmkgRE8iLCBj',
'aHVhX3Ryb24gaWYgbm90IGRvX3BhY2tldCBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBm',
'IkRPOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF19IOKAlCBiYW4gdmEgQ0hVQSB4b25nIikKICAgIGtldCgiTW9p',
'IGNhIERPIGRldSBnaWFpIHRoaWNoIGR1b2MiLCBjaHVhX3Ryb24gaWYgbm90IGRvX2xhIGVsc2UgVFJVT1QsCiAgICAgICAg',
'IiIgaWYgbm90IGRvX2xhIGVsc2UgZiJsYToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV19IikKICAgIGlmIGRvX3RoaWV1',
'X2NvbmdfY3U6CiAgICAgICAga2V0KCJDb25nIGN1IGRheSBkdSBkZSBkbyIsIEtERCwgZiJ0aGlldSBjb25nIGN1IGNobyB7',
'W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdfSIpCgogICAgYnEgPSBzb3J0ZWQoe3QgZm9yIHQsIF8gaW4g',
'UlhfQk9fUVVBLmZpbmRhbGwob3V0X24pfSwga2V5PXNvX2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBicSkKICAgIGlubigiIik7',
'IGlubihmIiAgQk8gUVVBICh7bGVuKGJxKX0pOiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCiAgICBpbm4o',
'IiIpOyBpbm4oIiAgTjEtTjQgKHQxNjUtdDE2OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBuYXkgbGEgY2hpIGJh',
'byBob2kgcXV5OiIpCiAgICBiNCA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBTU9JfTsgZ2hpKCJjYV9tb2ki',
'LCBiNCkKICAgIGZvciB0IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCiAgICAjIEJPX1FVQS92YW5nIGxh',
'IENIVUEgQ0hBWSwga2hvbmcgcGhhaSBETzogY2hpIG1vdCBjYSBETyBtb2kgZHVvYyBwaGF0IFRSVU9ULgogICAga2V0KCJO',
'MS1ONCAodDE2NS10MTY4KSIsIERBVCBpZiBhbGwodiA9PSAiUVVBIiBmb3IgdiBpbiBiNC52YWx1ZXMoKSkKICAgICAgICBl',
'bHNlIChUUlVPVCBpZiBhbnkodiA9PSAiRE8iIGZvciB2IGluIGI0LnZhbHVlcygpKSBlbHNlIEtERCksIHN0cihiNCkpCgog',
'ICAgaW5uKCIiKTsgaW5uKCIgIDE1IGNhIHR1bmcgZG8gdHJlbiBDSToiKQogICAgYjE1ID0ge3Q6IG1hdV9jYShvdXRfbiwg',
'dCkgZm9yIHQgaW4gQ0ExNX07IGdoaSgiY2ExNSIsIGIxNSkKICAgIGlubigiICAgICIgKyAiICAiLmpvaW4oZiJ7dH06e2Ix',
'NVt0XX0iIGZvciB0IGluIENBMTUpKQoKICAgICMgdDEzNiDigJQgTjEyIGRvIEdJQU4gVElFUCBxdWEga2V0IHF1YSBjYQog',
'ICAgdDEzNl90ZW4gPSBuZXh0KCh0IGZvciB0IGluIGRvX2hldCBpZiB0LnN0YXJ0c3dpdGgoInQxMzYiKSksIE5vbmUpCiAg',
'ICBpZiBiMTUuZ2V0KCJ0MTM2IikgPT0gIlFVQSI6CiAgICAgICAga2V0KCJOMTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwg',
'REFULCAidDEzNiBRVUEiKQogICAgZWxpZiBiMTUuZ2V0KCJ0MTM2IikgIT0gIkRPIjoKICAgICAgICBrZXQoIk4xMiB0MTM2',
'IChxdWEga2V0IHF1YSBjYSkiLCBLREQsIGYidDEzNiA9IHtiMTUuZ2V0KCd0MTM2Jykhcn0g4oCUIGtob25nIGNoYXkva2hv',
'bmcgdGhheSIpCiAgICBlbHNlOgogICAgICAgIGx5ID0gZG9faGV0LmdldCh0MTM2X3RlbiwgIiIpCiAgICAgICAga2V0KCJO',
'MTIgdDEzNiAocXVhIGtldCBxdWEgY2EpIiwgVFJVT1QsIGYiRE86IHtseVs6OTBdfSIpCgojIC0tLS0tLS0tLS0tLS0tLS0g',
'My4gcHJvYmUgVEhBTkcgdmFvIGhhbSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMy4g',
'UFJPQkUgVEhBTkcg4oCUIGdvaSBfZ2l0X3dpbmRvd3Mgdm9pIHRoYW0gc28gdGllbSIpCnNwZWMgPSBpbXBvcnRsaWIudXRp',
'bC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHA1NDEiLCBzdHIodGVwKSkKbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVf',
'ZnJvbV9zcGVjKHNwZWMpOyBzcGVjLmxvYWRlci5leGVjX21vZHVsZShscCkKc2lnID0gaW5zcGVjdC5zaWduYXR1cmUobHAu',
'X2dpdF93aW5kb3dzKQpnaGkoInRoYW1fc29fX2dpdF93aW5kb3dzIiwgbGlzdChzaWcucGFyYW1ldGVycykpCmlubigiICB0',
'aGFtIHNvIGN1YSBfZ2l0X3dpbmRvd3M6IiwgbGlzdChzaWcucGFyYW1ldGVycykpCgpkZWYgZ29pKCoqa3cpOgogICAgIiIi',
'R29pIF9naXRfd2luZG93cywgQkFUIHN0ZGVyciBkZSBtb3QgZG9uZyBjaGFuIGRvYW4ga2hvbmcgZ2lldCBsdW90IGRvLiIi',
'IgogICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAg',
'ciA9IGxwLl9naXRfd2luZG93cygqKmt3KQogICAgcmV0dXJuIHIsIGUuZ2V0dmFsdWUoKQoKIyAtLS0gZG9pIGNodW5nIHJp',
'ZzogcGhhaSB0cmEgbG9pIGR1bmcgbW90IGNhIHRhIEJJRVQgVFJVT0MgZGFwIGFuIC0tLQp3aXRoIHRlbXBmaWxlLlRlbXBv',
'cmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICBuZ29haSA9IFBhdGgodCkvIm5nb2FpIjsgbmdvYWkubWtkaXIoKTsgY3cgPSBQ',
'YXRoKHQpLyJjd2QiOyBjdy5ta2RpcigpOyBwZiA9IFBhdGgodCkvInBmIjsgcGYubWtkaXIoKQogICAgKG5nb2FpLyJnaXQu',
'ZXhlIikud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMSwgXyA9IGdvaShwYXRoPXN0cihuZ29haSks',
'IHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAoY3cvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4Iiwg',
'ZW5jb2Rpbmc9InV0Zi04IikKICAgIHIyLCBfID0gZ29pKHBhdGg9c3RyKGN3KSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBj',
'd2Q9c3RyKGN3KSkKcmlnX29rID0gYm9vbChyMSkgYW5kIHIyIGlzIE5vbmUKZ2hpKCJyaWdfZG9pX2NodW5nIiwgcmlnX29r',
'KQprZXQoIlJJRyBkb2kgY2h1bmcgKGJpZXQgdHJ1b2MgZGFwIGFuKSIsIERBVCBpZiByaWdfb2sgZWxzZSBLREQsCiAgICBm',
'Im5nb2FpLWN3ZC0+eydOSEFOJyBpZiByMSBlbHNlICdOb25lJ30gfCB0cm9uZy1jd2QtPnsnTkhBTicgaWYgcjIgZWxzZSAn',
'Tm9uZSd9IikKaWYgbm90IHJpZ19vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzogcmlnIHNhaSwgbW9pIGNo',
'b3QgZHVvaSBzZSB2byBuZ2hpYS4iKTsgc3lzLmV4aXQoMykKCiMgLS0tIE1PSSBDT05HIFBIQUkgVFUgQ0hVTkcgTUlOSCBO',
'TyBDTyBUSEUgRE8gLS0tCiMgQmFpIGhvYyBkYXQgbmhhdCBjdWEgcGFja2V0IG5heTogZG9fbjEwIGJhbiBjdSBjaGFtIERB',
'VCBjaG8gOTU4MzE2ODUgdHJvbmcga2hpIHQxNzEKIyBjdWEgY2hpbmggYmFuIHZhIGF5IERPIHZpIGR1bmcga2h1eWV0IHRh',
'dCBtYSBOMTAgc2luaCByYSBkZSBiYXQuIE5vIGRlZ2VuZXJhdGUg4oCUCiMgdHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAgREEg',
'bGEgJzsnIG5lbiAidGFjaCBkdW5nIiB2YSAidGFjaCBzYWkiIGNobyBjdW5nIGtldCBxdWEuCiMgTW90IGNvbmcga2hvbmcg',
'dGhlIERPIHRoaSBraG9uZyBwaGFpIGNvbmcsIHZhIG5vIG5ndXkgaGllbSBob24ga2hvbmcgY28gY29uZzogbm8KIyBwaGF0',
'IHJhIG1vdCBjaHUgREFULgojCiMgTmVuIHRydW9jIGtoaSBEVU5HIG5hbSBjb25nIG5heSBkZSBwaGFuIHF1eWV0LCBiYXQg',
'dHVuZyBjb25nIGdpZXQgbW90IGRvdCBiaWVuIGRhCiMgYmlldCB0cm9uZy4gQ29uZyBuYW8ga2hvbmcgZ2lldCBkdW9jIHRo',
'aSBjaHUgREFUIGN1YSBubyBiaSBIQSB4dW9uZyBLSE9ORyBETyBEVU9DOwojIFRSVU9UIGdpdSBuZ3V5ZW4gKHF1YW4gc2F0',
'IHRydWMgdGllcCwgdmQuIGcxIHZhbiBuaGFuIGdpdC5iYXQpLiBEb3QgYmllbiBjaGF5IHRyZW4gQkFOIFNBTyBUQU07IGNh',
'eSB0aGF0IGtob25nIGJpCiMgZHVuZyB0b2kgKGN1bmcga3kgbHVhdCBuaHUgTjcpLgpET1RfQklFTl9UVV9LSUVNID0gWwog',
'ICAgKCJOOCIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgJ2lmIGNoaV9kaW5oIGFuZCBQYXRoKGNoaV9kaW5oKS5u',
'YW1lLmxvd2VyKCkgPT0gImdpdC5leGUiIGFuZCBob3BfbGUoY2hpX2RpbmgpOicsCiAgICAgImlmIGNoaV9kaW5oIGFuZCBo',
'b3BfbGUoY2hpX2RpbmgpOiIpLAogICAgKCJOOSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsCiAgICAgImQgPSBkX3Jhdy5z',
'dHJpcCgpLnN0cmlwKCdcIicpIiwgImQgPSBkX3Jhdy5zdHJpcCgpIiksCiAgICAoIk4xMCIsICJvcHMvbGVhc2VfcHVibGlz',
'aC5weSIsCiAgICAgInNlcCA9IG9zLnBhdGhzZXAgaWYgcGhhbl9jYWNoIGlzIE5vbmUgZWxzZSBwaGFuX2NhY2giLCAic2Vw',
'ID0gb3MucGF0aHNlcCIpLAogICAgKCJOMTEiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLCAiaWYgY2hhbl9kb2FuIGlzIG5v',
'dCBOb25lOiIsICJpZiBGYWxzZToiKSwKICAgICgiTjEyIiwgIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiLAogICAgICdn',
'aXRfcGF0aD0iLy9raG9uZy1jby9naXQiJywgJ2dpdF9wYXRoPSIva2hvbmctY28vZ2l0IicpLApdCmlubigiIik7IGlubigi',
'ICB0dSBraWVtIGNvbmcg4oCUIG1vaSBjb25nIHBoYWkgZ2lldCBkdW9jIG1vdCBkb3QgYmllbiBkYSBiaWV0OiIpCmdpZXQg',
'PSB7fQpmb3IgbWEsIGR1b25nLCB0aW0sIHRoYXkgaW4gRE9UX0JJRU5fVFVfS0lFTToKICAgIF90ZW4sIF9oYW0gPSBuZXh0',
'KCgoYSwgYikgZm9yIGEsIGIgaW4gUFJPQkUgaWYgYS5zdGFydHN3aXRoKG1hICsgIiAiKSksIChOb25lLCBOb25lKSkKICAg',
'IGlmIF9oYW0gaXMgTm9uZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVP',
'Qzoga2hvbmcgdGltIHRoYXkgcHJvYmUgdGVuICd7bWF9IC4uLiciKTsgY29udGludWUKICAgIHRyeToKICAgICAgICB3aXRo',
'IHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIF90OgogICAgICAgICAgICBfYyA9IFBhdGgoX3QpLyJjYXkiOyBz',
'aHV0aWwuY29weXRyZWUoZ29jLyJvcHMiLCBfYy8ib3BzIikKICAgICAgICAgICAgX2YgPSBfYy9kdW9uZzsgX25kID0gX2Yu',
'cmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIGlmIF9uZC5jb3VudCh0aW0pICE9IDE6CiAgICAgICAg',
'ICAgICAgICBnaWV0W21hXSA9IE5vbmUKICAgICAgICAgICAgICAgIGlubihmIiAgICB7bWE6NH0gS0hPTkcgRE8gRFVPQzog',
'bWF1IGRvdCBiaWVuIGtob3Age19uZC5jb3VudCh0aW0pfSBsYW4gKG1vbmcgMSkiCiAgICAgICAgICAgICAgICAgICAgZiIg',
'4oCUIG1hIG5ndW9uIGRhIGRvaSwgZG90IGJpZW4gbmF5IGhldCB5IG5naGlhIik7IGNvbnRpbnVlCiAgICAgICAgICAgIF9m',
'LndyaXRlX3RleHQoX25kLnJlcGxhY2UodGltLCB0aGF5LCAxKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgX3Nw',
'ID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX2RiXyIgKyBtYSwgc3RyKF9jLyJvcHMiLyJs',
'ZWFzZV9wdWJsaXNoLnB5IikpCiAgICAgICAgICAgIF9tID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3Ap',
'OyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9tKQogICAgICAgICAgICBkZWYgX2dvaV9kYigqKmt3KToKICAgICAgICAgICAg',
'ICAgIF9lID0gaW8uU3RyaW5nSU8oKQogICAgICAgICAgICAgICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihf',
'ZSk6CiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIF9tLl9naXRfd2luZG93cygqKmt3KSwgX2UuZ2V0dmFsdWUoKQogICAg',
'ICAgICAgICBfdHQsIF9jdCwgXyA9IF9oYW0oX2dvaV9kYiwgaW5zcGVjdC5zaWduYXR1cmUoX20uX2dpdF93aW5kb3dzKSwK',
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF9jLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAg',
'IGdpZXRbbWFdID0gKF90dCA9PSBUUlVPVCkKICAgICAgICBpbm4oZiIgICAge21hOjR9IGRvdCBiaWVuIC0+IHtfdHQ6MTR9',
'IHsnR0lFVCBEVU9DJyBpZiBfdHQgPT0gVFJVT1QgZWxzZSAnU09ORyBTT1QnfSIKICAgICAgICAgICAgKyAoZiIgICAoe19j',
'dH0pIiBpZiBfY3QgZWxzZSAiIikpCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAgICAgIGdpZXRbbWFdID0gTm9u',
'ZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiB7dHlwZShfZSkuX19uYW1lX199OiB7X2V9IikKZ2hpKCJjb25n',
'X2dpZXRfZHVvY19kb3RfYmllbiIsIGdpZXQpCgpmb3IgdGVuLCAodHQsIGN0LCBkbCkgaW4gWyh0LCBmKGdvaSwgc2lnLCB0',
'ZXB0KSkgZm9yIHQsIGYgaW4gUFJPQkVdOgogICAgZ2hpKCJwcm9iZV8iICsgdGVuLnNwbGl0KClbMF0ubG93ZXIoKSwgZGwp',
'CiAgICBpZiBpc2luc3RhbmNlKGRsLCBkaWN0KToKICAgICAgICBmb3IgaywgdiBpbiBkbC5pdGVtcygpOiBpbm4oZiIgICAg',
'e2s6MzR9OiB7dn0iKQogICAgbWEgPSB0ZW4uc3BsaXQoKVswXQogICAgaWYgZ2lldC5nZXQobWEpIGlzIG5vdCBUcnVlIGFu',
'ZCB0dCA9PSBEQVQ6CiAgICAgICAgIyBEQVQgdHUgbW90IGNvbmcgY2h1YSBjaHVuZyBtaW5oIGR1b2MgbGEgYmlldCBETyB0',
'aGkga2hvbmcgZGFuZyB0aW4gaG9uIEtERC4KICAgICAgICBrZXQodGVuLCBLREQsIGYiY29uZyBLSE9ORyBnaWV0IGR1b2Mg',
'ZG90IGJpZW4gY3VhIGNoaW5oIG5vICh7Z2lldC5nZXQobWEpIXJ9KSIKICAgICAgICAgICAgICAgICAgICAgIGYiIC0+IGNo',
'dSBEQVQgbmF5IGtob25nIGNvIGdpYSB0cmkiKQogICAgZWxzZToKICAgICAgICBrZXQodGVuLCB0dCwgY3QpCgojIC0tLS0t',
'LS0tLS0tLS0tLS0gNC4gTjcgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAtLS0tLS0tLS0tLS0tLS0tCmlmIG5vdCBDSElf',
'UFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjQuIE43IOKAlCBkb3QgYmllbiB0cmVuIEJBTiBTQU8g',
'VEFNIChjYXkgdGhhdCBLSE9ORyBiaSBkdW5nIHRvaSkiKQogICAgdHJ1b2MgPSB0ZXAucmVhZF90ZXh0KGVuY29kaW5nPSJ1',
'dGYtOCIpLmNvdW50KE1BVV9XSU4pCiAgICBnaGkoIm43X3RydW9jIiwgdHJ1b2MpOyBpbm4oZiIgIHNvIGRvbmcga2hvcCB7',
'TUFVX1dJTiFyfTogVFJVT0MgPSB7dHJ1b2N9IFttb25nIDFdIikKICAgIGlmIHRydW9jICE9IDE6CiAgICAgICAga2V0KCJO',
'NyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCBmIm1hdSB4dWF0IGhpZW4ge3RydW9jfSBsYW4sIGtob25nIHBoYWkg',
'MSIpCiAgICBlbHNlOgogICAgICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdG1wOgogICAgICAg',
'ICAgICBzYW8gPSBQYXRoKHRtcCkvImNheSIKICAgICAgICAgICAgc2h1dGlsLmNvcHl0cmVlKGdvYywgc2FvLCBpZ25vcmU9',
'c2h1dGlsLmlnbm9yZV9wYXR0ZXJucygiLmdpdCIsICJfX3B5Y2FjaGVfXyIsICIqLnB5YyIpKQogICAgICAgICAgICBmMiA9',
'IHNhby8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIKICAgICAgICAgICAgZjIud3JpdGVfdGV4dChmMi5yZWFkX3RleHQoZW5j',
'b2Rpbmc9InV0Zi04IikucmVwbGFjZShNQVVfV0lOLCAiaWYgRmFsc2U6IiksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAg',
'ICAgIHNhdSA9IGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKTsgZ2hpKCJuN19zYXUiLCBz',
'YXUpCiAgICAgICAgICAgIGlubihmIiAgU0FVIChkYSBkb3QgYmllbikgPSB7c2F1fSBbbW9uZyAwXSIpCiAgICAgICAgICAg',
'IGlmIHNhdSAhPSAwOgogICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5kb3dzIiwgS0RELCAiZG90',
'IGJpZW4gS0hPTkcgYXAgZHVvYyIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICByY19tLCBvdXRfbSA9IGNo',
'YXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIHNhbykKICAgICAgICAgICAgICAgIG0xNjUgPSBtYXVfY2Eob3V0',
'X20sICJ0MTY1Iik7IGRtLCBfLCBfID0gZG9jX2RvKG91dF9tKQogICAgICAgICAgICAgICAgdGVuMTY1ID0gbmV4dCgodCBm',
'b3IgdCBpbiBkbSBpZiB0LnN0YXJ0c3dpdGgoInQxNjUiKSksIE5vbmUpCiAgICAgICAgICAgICAgICBseSA9IChkbS5nZXQo',
'dGVuMTY1KSBvciAiIikKICAgICAgICAgICAgICAgIGdoaSgibjdfdDE2NSIsIG0xNjUpOyBnaGkoIm43X2x5X2RvIiwgbHlb',
'OjIwMF0pCiAgICAgICAgICAgICAgICBpbm4oZiIgIHQxNjUgc2F1IGRvdCBiaWVuOiB7bTE2NX0gfCB7bHlbOjExMF19IikK',
'ICAgICAgICAgICAgICAgIGR1bmdfbHlfZG8gPSAiUEFUSCB0IiBpbiBseSBvciAiL3Vzci9iaW4iIGluIGx5CiAgICAgICAg',
'ICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBEQVQgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19s',
'eV9kbykgZWxzZQogICAgICAgICAgICAgICAgICAgIChUUlVPVCBpZiBtMTY1ID09ICJETyIgZWxzZSBLREQpLAogICAgICAg',
'ICAgICAgICAgICAgICJnaWV0IGR1bmcgbHkgZG8iIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pCiAgICAgICAg',
'ICAgICAgICAgICAgZWxzZSAoIkRPIG5odW5nIEtIT05HIGR1bmcgbHkgZG8gLT4gdGluIGR1bmcgZ2lhIiBpZiBtMTY1ID09',
'ICJETyIgZWxzZSAia2hvbmcgZG9jIGR1b2MgdDE2NSIpKQoKIyAtLS0tLS0tLS0tLS0tLS0tIEtFVCBMVUFOIC0tLS0tLS0t',
'LS0tLS0tLS0KaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQppbm4oZiJUSEUgSEUgRE8gRFVPQzoge3RoZV9oZX0gICBIRUFEPXto',
'ZWFkWzoxMl19IikKIyBLaG9pIGRhbiBjaG8gcmV2aWV3ZXIgYmF0IGRhdSBvIGRvbmcgdHJlbiwgbmVuIENIRSBETyBwaGFp',
'IG5hbSBOR0FZIGR1b2kgbm86IGtob25nIGNvIGRvbmcgbmF5CiMgdGhpIG1vdCBsdW90IC0tY2hpLXByb2JlIGluICJEQVQg',
'NyB8IFRSVU9UIDAgfCBLSE9ORyBETyBEVU9DIDAiIHJjPTAgbWEga2hvbmcgbm9pIGxhIGNodWEgY2hheSBibyB0ZXN0Lgpn',
'aGkoImNoZV9kbyIsICJjaGktcHJvYmUiIGlmIENISV9QUk9CRSBlbHNlICJkYXktZHUiKQppZiBDSElfUFJPQkU6CiAgICBp',
'bm4oIi0tY2hpLXByb2JlOiBDSEkgZG8gbXVjIDAsIDEsIDMuIEJvIHRlc3QsIE4xLU40LCB0MTM2LCBONyBLSE9ORyBjaGF5',
'IC0gZGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQppZiB0aGVfaGUgPT0gImcxIjoKICAgIGlubigiTFVV',
'IFk6IGRheSBsYSBORU4gRE8gKGcxKSwgS0hPTkcgcGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hvdCBOOC1OMTIgZHVvaSBk',
'YXkiKQogICAgaW5uKCIgICAgICAgVFJVT1QgbGEgRFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEgbmh1bmcgbG8gZzIgc2lu',
'aCByYSBkZSB2w6EuIikKaW5uKCItIiAqIDc4KQpmb3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAgIGlubihmIiAge3R0OjE0',
'fSB7dGVufSIgKyAoZiIgICB7Y3R9IiBpZiBjdCBlbHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90',
'IGlmIHQgPT0gS0REKQpuX3RydW90ID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQppbm4oIi0i',
'ICogNzgpCmlubihmIiAgREFUIHtzdW0oMSBmb3IgXyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8IFRSVU9UIHtuX3RydW90',
'fSB8IEtIT05HIERPIERVT0Mge25fa2RkfSIpCmlubihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgnc29fY2FfZG8nKX0gfCBk',
'YW5oIHNhY2ggZGF5IGR1OiB7J0NPJyBpZiBzby5nZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAnS0hPTkcgRE8gRFVPQyd9',
'IikKaW5uKGYiICBBZG1pbmlzdHJhdG9yOiB7c28uZ2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxpbms6IHtzby5nZXQoJ3N5',
'bWxpbmtfZHVvYycpfSIpCmlubigiIik7IGlubigiLS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5BWSBWRSBDSE8gUkVWSUVX',
'RVIgLS0tIikKZ2hpKCJjaG90IiwgW3sidGVuIjogYSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3RpZXQiOiBjfSBmb3IgYSwg',
'YiwgYyBpbiBjaG90XSkKaW5uKGpzb24uZHVtcHMoc28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50PTEsIGRlZmF1bHQ9',
'c3RyKSkKIyByYzogMCA9IG1vaSBjaG90IERBVCB8IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNvIGNob3QgS0hPTkcgRE8g',
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
if ($ChiGiaiNen) { Write-Host ''; Write-Host 'Chi giai nen theo yeu cau. Dung tai day.'; exit 0 }

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
exit $rc
