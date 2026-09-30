# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong, khong can gi khac):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
#
# Do RIENG cong kich thuoc (vai giay, khong chay bo test 20-45 phut):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1" -ChiKichThuoc
#
# Do RIENG probe + tu kiem cong (vai giay, khong chay bo test):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1" -ChiProbe
#
# Nhanh mac dinh la fix_issue_541 - nhanh mang ung vien g2 (lease g2 khai dung nhanh
# nay). Ung vien nay gio la mot merge commit: 0ea95de + origin/master. Doi nhanh khac:
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
    [string]$Base    = '',     # thu muc lam viec. Mac dinh: thu muc chua chinh tep nay
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
$ShaBoDo    = 'd13971704dde594a9ac41e6236347c266871306a13d0a8e99c3b853deb5173b3'      # SHA-256 cua bo do Python nhung ben duoi

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
        Write-Host ($out | Out-String)
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
if (-not $Base) { $Base = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path } }
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
if ($Py) { $pyCmd = Get-Command $Py -ErrorAction SilentlyContinue }
foreach ($ten in @('py','python','python3')) {
    if ($pyCmd) { break }
    $pyCmd = Get-Command $ten -ErrorAction SilentlyContinue
}
if ($pyCmd) {
    # "CO MAT" khac "DUNG DUOC": py launcher khong co ban nao thi goi la gay.
    $ok = $true
    try { $thu = & $pyCmd.Source -c "import sys;print(sys.version.split()[0])" 2>&1 } catch { $ok = $false; $thu = $_.Exception.Message }
    if (-not $ok -or $LASTEXITCODE -ne 0) { Write-Host "  $($pyCmd.Name) co mat nhung khong chay duoc ($thu) -> bo qua"; $pyCmd = $null }
}
if (-not $pyCmd) {
    if ($BoQuaTaiCongCu) { Dung 'khong co python dung duoc (va -BoQuaTaiCongCu dang bat)' }
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
# Giai nen vao thu muc CONG CU, KHONG vao $Base: chay tai cho trong kho thi $Base la
# ops/reviews, va `Move-Item -Force` ban cu DE THANG tep .py dang duoc theo doi.
New-Item -ItemType Directory -Force -Path $CongCu | Out-Null
$BoDo = Join-Path $CongCu 'wp541-do-g2-windows.py'
# Tep .py canh ps1 (chay tai cho trong kho) la BAN SAO THU HAI. Lech ban nhung => DUNG:
# khong cong nao trong kho buoc hai ban khop (kiem tren Linux: --kiem-dong-bo).
$Canh = if ($PSScriptRoot) { Join-Path $PSScriptRoot 'wp541-do-g2-windows.py' } else { $null }
if ($Canh -and (Test-Path -LiteralPath $Canh) -and ((Bam $Canh) -ne $ShaBoDo)) {
    Dung "tep canh ps1 ($Canh) LECH ban nhung - hai ban sao da troi. Xoa tep cu, hoac dong bo lai ca hai"
}
$B64 = @(
'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIiIiV1A1NDEgZzIgLSBQSEVQIERPIFRSRU4gV0lORE9XUyBUSEFUIGNobyBzcGVj',
'IHIzIChOMS1ONCArIE44LU4xMiArIE43ICsga2ljaCB0aHVvYykuCgpDaGF5OiAgcHkgd3A1NDEtZG8tZzItd2luZG93cy5w',
'eSAiPHRodS1tdWMta2hvPiIKCktIT05HIGdoaW0gU0hBLiBObyBkbyBCQVQgS1kgZGF1IG5hbyBkYW5nIG8gdHJlbiBuaGFu',
'aCwgcm9pIFRVIFBIQU4gTE9BSToKICBoZWFkID09IDJmNzA4NjlhICAtPiBkYXkgbGEgZzEsIENIVUEgY28gYmFuIHZhIGcy',
'LiBWYW4gZG8sIG5odW5nIG5oYW4gbGEgTkVOIERPLgogIGhlYWQgbGEgaGF1IGR1ZSAgICAtPiB1bmcgdmllbiBnMi4KICBr',
'aGFjICAgICAgICAgICAgICAgLT4gS0hPTkcgRE8gRFVPQyAocmViYXNlPyBuaGFtIG5oYW5oPykgLT4gcmM9Mywga2hvbmcg',
'a2V0IGx1YW4uClR1IDIwLTA5IGcxIERBIExBTkQgdmFvIG1hc3RlciwgbmVuICJoYXUgZHVlIGN1YSBnMSIgS0hPTkcgY29u',
'IGxvYWkgZHVvYyBuaGFuaCBuYW8gKGRvIGR1b2M6Cm1hc3RlciA0NDYyMGU4IHZhIG1vdCBuaGFuaCBib29ra2VlcGluZyBk',
'ZXUgcmEgInVuZyB2aWVuIGcyIiwgREFUIHJjPTApLiBWaSB2YXkgZG9pIHR1b25nIGNvbgpwaGFpIChhKSBjbyB0aGF5IGRv',
'aSBzbyB2b2kgbWVyZ2UtYmFzZSB2YSAoYikgY2hhbSBXUklURV9TRVRfRzIg4oCUIGtob25nIHRoaSBLSE9ORyBETyBEVU9D',
'LgoKQkEgVFJBTkcgVEhBSSBvIG1vaSBjaG90OiBEQVQgLyBUUlVPVCAvIEtIT05HIERPIERVT0MuIENhaSB0aHUgYmEgS0hP',
'TkcgZHVvYyBsYW5nIGxlCnRoYW5oIG1vdCB0cm9uZyBoYWkgY2FpIGtpYSDigJQgZG8gbGEgY2EgZG9jdHJpbmUgYE5vbmUg',
'IT0gRmFsc2VgIGN1YSBraG8uCgpNT0kgY2hvdCBhbSBkZXUgY28gRE9JIENIVU5HIERVT05HLiBNb3QgY2hvdCBjaGkgZG8g',
'Y2hpZXUgInBoYWkgdHUgY2hvaSIgdGhpIG1vdCBoYW0KYHJldHVybiBOb25lYCB2byBkaWV1IGtpZW4gY3VuZyBxdWEgZHVv',
'YyBuby4KCkRvdCBiaWVuIGNoYXkgdHJlbiBCQU4gU0FPIFRBTTsgY2F5IHRoYXQga2hvbmcgYmkgZHVuZyB0b2kuCiIiIgpp',
'bXBvcnQgY29udGV4dGxpYiwgaGFzaGxpYiwgaW1wb3J0bGliLnV0aWwsIGluc3BlY3QsIGlvLCBqc29uLCBvcywgcmUsIHNo',
'dXRpbCwgc3VicHJvY2Vzcywgc3lzLCB0ZW1wZmlsZQpmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgsIFB1cmVQb3NpeFBhdGgs',
'IFB1cmVXaW5kb3dzUGF0aAoKb3MuZW52aXJvbi5zZXRkZWZhdWx0KCJQWVRIT05VVEY4IiwgIjEiKQpvcy5lbnZpcm9uLnNl',
'dGRlZmF1bHQoIlBZVEhPTklPRU5DT0RJTkciLCAidXRmLTgiKQpmb3IgX2wgaW4gKHN5cy5zdGRvdXQsIHN5cy5zdGRlcnIp',
'OgogICAgdHJ5OiBfbC5yZWNvbmZpZ3VyZShlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiKQogICAgZXhjZXB0',
'IEV4Y2VwdGlvbjogcGFzcwppZiBzeXMucGxhdGZvcm0gPT0gIndpbjMyIjoKICAgIHRyeToKICAgICAgICBpbXBvcnQgY3R5',
'cGVzCiAgICAgICAgY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5TZXRDb25zb2xlT3V0cHV0Q1AoNjUwMDEpCiAgICAgICAgY3R5',
'cGVzLndpbmRsbC5rZXJuZWwzMi5TZXRDb25zb2xlQ1AoNjUwMDEpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBwYXNzCgpkZWYg',
'aW5uKCpwKToKICAgIHZhbiA9ICIgIi5qb2luKHN0cih4KSBmb3IgeCBpbiBwKQogICAgdHJ5OiBwcmludCh2YW4sIGZsdXNo',
'PVRydWUpCiAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAgIHRyeTogc3lzLnN0ZG91dC5idWZmZXIud3JpdGUodmFuLmVu',
'Y29kZSgidXRmLTgiLCAicmVwbGFjZSIpICsgYiJcbiIpOyBzeXMuc3Rkb3V0LmZsdXNoKCkKICAgICAgICBleGNlcHQgRXhj',
'ZXB0aW9uOiBwcmludCh2YW4uZW5jb2RlKCJhc2NpaSIsICJiYWNrc2xhc2hyZXBsYWNlIikuZGVjb2RlKCJhc2NpaSIpLCBm',
'bHVzaD1UcnVlKQoKIyBOZ29haSBsZSBLSE9ORyBiYXQgPT4gUHl0aG9uIHRob2F0IHJjPTEsIG1hIHJjPTEgbyBkYXkgREEg',
'Q08gTkdISUEgImNvIGNob3QgVFJVT1QiIChkb25nCiMgY3VvaSB0ZXApIOKAlCBkdW5nIGx5IGRvIHBzMSBkYXQgYHRyYXBg',
'IC0+IHJjPTMuIERvIGR1b2M6IGdpdCB2YW5nIFBBVEggKGRvbmcgYGdpdChnb2MsCiMgInJldi1wYXJzZSIpYCBjaGF5IFRS',
'VU9DIGBpZiBsb2k6YCksIGJvIHRlc3QgcXVhIGhhbiwgdW5nIHZpZW4gdGhpZXUgX2dpdF93aW5kb3dzLCBwcm9iZQojIHRo',
'YXQgbmVtIG5nb2FpIGxlIOKAlCBjYSBib24gdHVuZyByYSByYz0xIG1hIHBoZXAgZG8gQ0hVQSBIRSBjaGF5IHhvbmcuCmRl',
'ZiBfbmdvYWlfbGVfbGFfS0REKGtpZXUsIGd0LCB2ZXQpOgogICAgaW1wb3J0IHRyYWNlYmFjawogICAgdHJhY2ViYWNrLnBy',
'aW50X2V4Y2VwdGlvbihraWV1LCBndCwgdmV0KQogICAgaW5uKCIiKTsgaW5uKGYiS0hPTkcgRE8gRFVPQzogbmdvYWkgbGUg',
'a2hvbmcgbHVvbmcgdHJ1b2Mge2tpZXUuX19uYW1lX199OiB7Z3R9IikKICAgIGlubigiUGhlcCBkbyBDSFVBIGNoYXkgeG9u',
'Zy4gS2hvbmcga2V0IGx1YW4gZ2kuIikKICAgIGZvciBfbCBpbiAoc3lzLnN0ZG91dCwgc3lzLnN0ZGVycik6CiAgICAgICAg',
'dHJ5OiBfbC5mbHVzaCgpCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjogcGFzcwogICAgb3MuX2V4aXQoMykKc3lzLmV4Y2Vw',
'dGhvb2sgPSBfbmdvYWlfbGVfbGFfS0RECgpTSEFfRzEgICA9ICIyZjcwODY5YTA1Mzc4NDNlOWNhZTc4NjE4ZWU3YWU4YzI2',
'MWQ5NzJkIgojIEtIT05HIGdoaW0gYmFzZS4gU3BlYyByMyBONicga2hhaSBkbyBudW1zdGF0IHNvIGQ3MDU2MjMg4oCUIE5I',
'VU5HIHNwZWMgQ1VORyBiYW8gZXhlY3V0b3IKIyBgZ2l0IG1lcmdlIG9yaWdpbi9tYXN0ZXJgLiBTYXUgbWVyZ2UsIHBoZXAg',
'ZG8gc28gZDcwNTYyMyBOVU9UIGNhIHBoYW4gbWFzdGVyIG1hbmcgdmFvOgojIGRvIHRoYXQgMTgtMDkgdHJlbiBiYW4gdmEg',
'ZzIgY3VhIGFneSBjaG8gNSB0ZXAgLyArODEyLCB0cm9uZyBraGkgdmllYyBjdWEgYWd5IGxhIDIgdGVwIC8gKzM1My4KIyBN',
'b3QgY2hvdCBuaHUgdGhlIHNlIGJhbyAidnVvdCB0cmFuIiBjaG8gbW90IGJhbiB2YSBLSE9ORyB2dW90LiBCYXNlIGR1bmcg',
'bGEgTUVSR0UtQkFTRS4KU0hBX0JBU0VfU1BFQyA9ICJkNzA1NjIzMTYyYjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZm',
'IgpCQU5fQk9fRE8gPSAiMjAyNi0wOS0xOWUiICAgICAgICAgICAgICAjIGRvaSBNT0kga2hpIHN1YSBibyBkbyAtIGxvZyB0',
'dSBraGFpIGJhbiBuYW8KVFJBTl9URVAsIFRSQU5fRE9ORyA9IDIsIDQwMCAgICAgICAgICAjIE43JyBjdWEgc3BlYyByMwpN',
'QVVfV0lOICA9ICdpZiBuZW5fdGh1YyA9PSAid2luZG93cyI6JwojIFdyaXRlIHNldCBjdWEgcGFja2V0ICM1NDEgZzIuIERp',
'ZmYga2hvbmcgY2hhbSB0ZXAgbmFvIG8gZGF5ID0+IGRvIE5IQU0gTkhBTkguCldSSVRFX1NFVF9HMiA9IHsib3BzL2xlYXNl',
'X3B1Ymxpc2gucHkiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJ9CiMgIlR1b2kiIGNoaSBjbyBuZ2hpYSBraGkgc28g',
'dm9pIE1BWSBDSFUgVEhBVC4gTW90IG1pcnJvciBjdWMgYm8gY3UgY3VuZyB0cmEgbHMtcmVtb3RlID09CiMgb3JpZ2luL21h',
'c3RlciAoZG8gZHVvYzogbWFzdGVyIGMxNmJkMzIgLT4gInZlIG5lbiBUVU9JIiwgNDYgdGVwIC8gKzcxMTggY2hvIDBlYTk1',
'ZGUpLgojIERhbmggc2FjaCBDSE8gUEhFUDsgYHJlbW90ZSBnZXQtdXJsYCBkYSBraGFpIHRyaWVuIGluc3RlYWRPZiBuZW4g',
'Y2h1eWVuIGh1b25nIGN1bmcgbG8gcmEuClVSTF9LSE9fSE9QX0xFID0geyJodHRwczovL2dpdGh1Yi5jb20vZHVjdGhhbmdo',
'by90cmEtbHVhdCIsICJodHRwczovL2dpdGh1Yi5jb20vZHVjdGhhbmdoby90cmEtbHVhdC5naXQifQojIENhIG5nb2FpIHBo',
'YW0gdmkgcjMgwqduZ29haV9waGFtX3ZpIOKAlCBkbyBDSElOSCBTUEVDIGtoYWksIGtob25nIHBoYWkgYm8gZG8gdHUgcXV5',
'ZXQuCiMgRG8gbGEgREFOSCBTQUNIIENITyBQSEVQOiBjYSBkbyBuYW8gS0hPTkcgbmFtIHRyb25nIGRheSB2YSBLSE9ORyBw',
'aGFpICJ0aGlldSBjb25nIGN1IgojIHRoaSBsYSBUUlVPVC4gRGFuaCBzYWNoIGNhbSB0aGkgYmFvIGdpbyBjdW5nIHRoaWV1',
'OyBkYW5oIHNhY2ggY2hvIHBoZXAgdGhpIGJpZXQgdHJ1b2MuCk5HT0FJX1BIQU1fVkkgPSBzZXQoInQxMzEgdDEzMiB0MTUw',
'IHQxMjUgdDM1IHQzNiB0MzcgdDM4IHQzOSB0NDAiLnNwbGl0KCkpCiMgQ2EgY3VhIENISU5IIHBhY2tldCBuYXkuIE1vdCBj',
'YSBvIGRheSBtYSBETyB0aGkga2hvbmcgYmFvIGdpbyBkdW9jIGJvIHF1YS4KQ0FfUEFDS0VUID0gc2V0KCJ0MTY1IHQxNjYg',
'dDE2NyB0MTY4IHQxNjkgdDE3MCB0MTcxIHQxNzIgdDE3MyIuc3BsaXQoKSkKQ0ExNSAgPSAidDEyOSB0MTMwIHQxMzEgdDEz',
'MiB0MTMzIHQxMzYgdDEzOCB0MTM5IHQxNDQgdDE0NSB0MTQ2IHQxNDcgdDE0OSB0MTUwIHQxNTEiLnNwbGl0KCkKQ0FNT0kg',
'PSAidDE2NSB0MTY2IHQxNjcgdDE2OCIuc3BsaXQoKQoKREFULCBUUlVPVCwgS0REID0gIkRBVCIsICJUUlVPVCIsICJLSE9O',
'RyBETyBEVU9DIgpzbywgY2hvdCA9IHt9LCBbXQpkZWYgZ2hpKGssIHYpOiBzb1trXSA9IHY7IHJldHVybiB2CmRlZiBrZXQo',
'dGVuLCB0cmFuZ190aGFpLCBjaGlfdGlldD0iIik6CiAgICBjaG90LmFwcGVuZCgodGVuLCB0cmFuZ190aGFpLCBjaGlfdGll',
'dCkpCiAgICBpbm4oZiIgIFt7dHJhbmdfdGhhaToxNH1dIHt0ZW59IiArIChmIiAgIHtjaGlfdGlldH0iIGlmIGNoaV90aWV0',
'IGVsc2UgIiIpKQogICAgcmV0dXJuIHRyYW5nX3RoYWkKCiMgLS0tLS0tLS0tLS0tLS0tLSBkb2MgbG9nIGN1YSBibyB0ZXN0',
'IChiYW4gMywgZGEgZG8gdHJlbiBsb2cgVEhBVCkgLS0tLS0tLS0tLS0tLS0tLQpSWF9ET19DSE8gID0gcmUuY29tcGlsZShy',
'Iig/bSleISEhIGRvIChcUyspICguKikkIikKUlhfRE9fQ1VPSSA9IHJlLmNvbXBpbGUociIoP20pXiB7Mn0oXFN7MSw0fSkg',
'ezJ9KFxTKyk6ICguKikkIikKUlhfQk9fUVVBICA9IHJlLmNvbXBpbGUociIoP20pXiB7Mn1cU3sxLDZ9IFFVQSAoXFMrKTog',
'KC4qKSQiKQpSWF9UT05HICAgID0gcmUuY29tcGlsZShyImxlYXNlX3B1Ymxpc2g6IChcZCspLyhcZCspXGJbXlxuXSo/PShc',
'ZCspLFteXG5dKj89KFxkKykiKQoKZGVmIHNvX2NhKHQpOgogICAgbSA9IHJlLm1hdGNoKHIidChcZCspIiwgdCk7IHJldHVy',
'biAoaW50KG0uZ3JvdXAoMSkpIGlmIG0gZWxzZSAxMCoqNiwgdCkKCmRlZiBkb2NfZG8ob3V0KToKICAgIHRhaV9jaG8gPSB7',
'dDogbC5zdHJpcCgpIGZvciB0LCBsIGluIFJYX0RPX0NITy5maW5kYWxsKG91dCl9CiAgICBibyA9IHt0IGZvciB0LCBfIGlu',
'IFJYX0JPX1FVQS5maW5kYWxsKG91dCl9CiAgICBjdW9pID0ge3Q6IGwuc3RyaXAoKSBmb3IgXywgdCwgbCBpbiBSWF9ET19D',
'VU9JLmZpbmRhbGwob3V0KSBpZiB0IG5vdCBpbiBib30KICAgIGhvcCA9IGRpY3QoY3VvaSk7IGhvcC51cGRhdGUodGFpX2No',
'bykKICAgIGdjLCB0aW4gPSBbXSwgVHJ1ZQogICAgaWYgc2V0KHRhaV9jaG8pICE9IHNldChjdW9pKToKICAgICAgICBnYy5h',
'cHBlbmQoZiJoYWkgbmd1b24gTEVDSDogY2hpLXRhaS1jaG89e3NvcnRlZChzZXQodGFpX2Nobyktc2V0KGN1b2kpKX0gY2hp',
'LWN1b2k9e3NvcnRlZChzZXQoY3VvaSktc2V0KHRhaV9jaG8pKX0iKQogICAgICAgIHRpbiA9IEZhbHNlCiAgICBtID0gUlhf',
'VE9ORy5zZWFyY2gob3V0KQogICAgaWYgbm90IG06CiAgICAgICAgZ2MuYXBwZW5kKCJLSE9ORyBkb2MgZHVvYyBkb25nIHRv',
'bmcga2V0Iik7IHRpbiA9IEZhbHNlCiAgICBlbHNlOgogICAgICAgIGRhdCwgdHJlbiA9IGludChtLmdyb3VwKDEpKSwgaW50',
'KG0uZ3JvdXAoMikpCiAgICAgICAgZ2MuYXBwZW5kKGYic28gaG9jOiB7dHJlbn0te2RhdH09e3RyZW4tZGF0fSBkbzsgZG9j',
'IGR1b2Mge2xlbihob3ApfSIpCiAgICAgICAgaWYgdHJlbiAtIGRhdCAhPSBsZW4oaG9wKToKICAgICAgICAgICAgZ2MuYXBw',
'ZW5kKGYiTEVDSCBTTyBIT0M6IHRoaWV1IHt0cmVuLWRhdC1sZW4oaG9wKX0gY2EiKTsgdGluID0gRmFsc2UKICAgIHJldHVy',
'biBob3AsIGdjLCB0aW4KCl9NQVUgPSAoIiEhISBkbyB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOIGFcbiIKICAgICAg',
'ICAiISEhIGRvIHQxNTBfeCBXaW5FcnJvciAxMzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICIgIELhu44gUVVB',
'IHQxMzFfeTogbmVuIGZpeHR1cmVcbiIKICAgICAgICAiICDEkOG7jiAgdDAyYl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTjog',
'YVxuIgogICAgICAgICIgIMSQ4buOICB0MTUwX3g6IFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAg',
'ICAgImxlYXNlX3B1Ymxpc2g6IDEvMyDEkeG6oXQ7IMSRw6MgY2jhuqF5PTMsIGLhu48gcXVhPTFcbiIpCgpkZWYgY2hheShh',
'cmd2LCBjd2QsIHBodXQ9NjApOgogICAgbXQgPSBkaWN0KG9zLmVudmlyb24sIFBZVEhPTlVURjg9IjEiLCBQWVRIT05JT0VO',
'Q09ESU5HPSJ1dGYtOCIsCiAgICAgICAgICAgICAgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9IjEiLCBQWVRIT05VTkJVRkZF',
'UkVEPSIxIikKICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbc3lzLmV4ZWN1dGFibGVdICsgYXJndiwgY3dkPXN0cihjd2QpLCBj',
'YXB0dXJlX291dHB1dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04Iiwg',
'ZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD1waHV0KjYwLCBlbnY9bXQpCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5z',
'dGRvdXQgb3IgIiIpICsgKHAuc3RkZXJyIG9yICIiKQoKZGVmIG1hdV9jYShvdXQsIHQpOgogICAgbSA9IHJlLnNlYXJjaChy',
'Iig/bSlePDw8IHJhICgiICsgdCArIHIiW2Etel0/X1xTKikgWzAtOS5dK3MgKFx3KylccyokIiwgb3V0KQogICAgcmV0dXJu',
'IG0uZ3JvdXAoMikgaWYgbSBlbHNlIE5vbmUKCmRlZiBnaXQoZ29jLCAqYSwgcGh1dD01KToKICAgIHAgPSBzdWJwcm9jZXNz',
'LnJ1bihbImdpdCIsICItQyIsIHN0cihnb2MpLCAqYV0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwKICAgICAg',
'ICAgICAgICAgICAgICAgICBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjApCiAg',
'ICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpLnN0cmlwKCksIChwLnN0ZGVyciBvciAiIikuc3RyaXAo',
'KQoKCiMgPT09PT09PT09PT09PT09PT0gTkFNIFBST0JFLCB2aWV0IHRoYW5oIEhBTSBUSFVBTiBkZSBUVSBLSUVNIGR1b2Mg',
'PT09PT09PT09PT09PT09PT0KIyBNb2kgaGFtIHRyYSAodHJhbmdfdGhhaSwgY2hpX3RpZXQsIGR1X2xpZXUpLiBLSE9ORyBp',
'biwgS0hPTkcgdGhvYXQg4oCUIG5obyB2YXkgY2h1bmcKIyBjaGF5IGR1b2MgdHJlbiBuZW4gQkFUIEtZLCB2YSBgLS10dS1r',
'aWVtLXByb2JlYCBnb2kgdGhhbmcgY2h1bmcgZGUga2llbSBjaGluaCBibyBkby4KCmRlZiBfc2FuKHQpOgogICAgZCA9IFBh',
'dGgodCkvImQiOyBkLm1rZGlyKCk7IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7',
'IHBmLm1rZGlyKCkKICAgIHJldHVybiBkLCBjdywgcGYKCmRlZiBkb19uOChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJCdW9j',
'IDEgKENPTkdfQ1VfR0lUKSBjaGkgZHVvYyBuaGFuIGdpdC5leGUuIERvaSBjaHVuZyBkdW9uZzogZ2l0LmV4ZSBWQU4gcGhh',
'aSBuaGFuLiIiIgogICAga3EgPSB7fQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAg',
'ICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICBmb3IgdGVuIGluICgiZ2l0LmV4ZSIsICJnaXQuYmF0IiwgImdpdC5j',
'bWQiLCAiZ2l0LnB5IiwgImtob25nLXBoYWktZ2l0LnR4dCIpOgogICAgICAgICAgICBmID0gZC90ZW47IGYud3JpdGVfdGV4',
'dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIHIsIF8gPSBnb2koY29uZ19jdV9naXQ9c3RyKGYpLCBwYXRo',
'PSIiLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICBrcVtmIkNPTkdfQ1VfR0lUPXt0',
'ZW59Il0gPSAiTkhBTiIgaWYgciBlbHNlICJUVSBDSE9JIgogICAgbG90ID0gW2sgZm9yIGssIHYgaW4ga3EuaXRlbXMoKSBp',
'ZiB2ID09ICJOSEFOIiBhbmQgbm90IGsuZW5kc3dpdGgoImdpdC5leGUiKV0KICAgIGlmIGtxLmdldCgiQ09OR19DVV9HSVQ9',
'Z2l0LmV4ZSIpICE9ICJOSEFOIjoKICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IGdpdC5leGUg',
'aG9wIGxlIG1hIGJpIHR1IGNob2kiLCBrcQogICAgcmV0dXJuIChEQVQgaWYgbm90IGxvdCBlbHNlIFRSVU9UKSwgKCIiIGlm',
'IG5vdCBsb3QgZWxzZSBmImNvbiBuaGFuOiB7bG90fSIpLCBrcQoKZGVmIGRvX245KGdvaSwgc2lnLCB0ZXB0KToKICAgICIi',
'Ik11YyBQQVRIIGJvYyBuaGF5IGtlcCBwaGFpIE5IQU47IG11YyByb25nIC8gdG9hbiBraG9hbmcgdHJhbmcgcGhhaSBibyBx',
'dWEsIGtob25nIG5lbS4iIiIKICAgIGtxID0ge30KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMg',
'dDoKICAgICAgICBkID0gUGF0aCh0KS8iY28gZ2l0IjsgZC5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGly',
'KCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4Iiwg',
'ZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBmb3IgbmhhbiwgbXVjIGluICgoImtob25nIG5oYXkiLCBzdHIoZCkpLCAoImNv',
'IG5oYXkga2VwIiwgZicie2R9IicpLAogICAgICAgICAgICAgICAgICAgICAgICAgICgicm9uZyIsICIiKSwgKCJjaGkga2hv',
'YW5nIHRyYW5nIiwgIiAgICIpKToKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgciwgXyA9IGdvaShwYXRoPW11',
'YywgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0i',
'XSA9ICJOSEFOIiBpZiByIGVsc2UgIk5vbmUiCiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAg',
'ICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9IGYiTkVNIHt0eXBlKGUpLl9fbmFtZV9ffSIKICAgIGlmIGtxLmdldCgiUEFU',
'SCBraG9uZyBuaGF5IikgIT0gIk5IQU4iOgogICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogbXVj',
'IFBBVEggdGh1b25nIG1hIGtob25nIHRpbSByYSBnaXQuZXhlIiwga3EKICAgIG9rID0gKGtxLmdldCgiUEFUSCBjbyBuaGF5',
'IGtlcCIpID09ICJOSEFOIgogICAgICAgICAgYW5kIGtxLmdldCgiUEFUSCByb25nIikgPT0gIk5vbmUiIGFuZCBrcS5nZXQo',
'IlBBVEggY2hpIGtob2FuZyB0cmFuZyIpID09ICJOb25lIikKICAgIHJldHVybiAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAo',
'IiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwga3EKCiMgRGF1IHBoYW4gY2FjaCBkdW5nIERFIFRIVS4gUGhhaSBLSEFDIG9z',
'LnBhdGhzZXAgdHJlbiBDQSBIQUkgbmVuICgnOycgV2luZG93cywgJzonIFBPU0lYKQojIHRoaSBoYWkgZ2lhIHRodXlldCAi',
'dGFjaCB0aGVvIGRhdSBkdW9jIHRydXllbiIgdmEgInRhY2ggdGhlbyBvcy5wYXRoc2VwIiBtb2kgcm9pIHJhIG5oYXUuClRI',
'VV9OMTAgPSAifCIKCmRlZiBkb19uMTAoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiSGFtIHBoYWkgdGFjaCBQQVRIIHRoZW8g',
'ZGF1IHBoYW4gY2FjaCBEVU9DIFRSVVlFTiwga2hvbmcgdGhlbyBvcy5wYXRoc2VwIGN1YSBuZW4uCgogICAgQmFuIGN1IGRv',
'ICJtb3QgZGF1ICc7JyB0cm9uZyBURU4gdGh1IG11YyIgdmEgZGF0IERBVCB0cmVuIFdpbmRvd3MgZHUgaGFtIHNhaS4gTm8K',
'ICAgIGRlZ2VuZXJhdGU6IHRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JywgbmVuICdDOi9hO2InIHRoYXQgc3Ug',
'Q08gTkdISUEgbGEgaGFpCiAgICBtdWMg4oCUICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIHJhIGN1bmcga2V0IHF1',
'YSwgcGhlcCBkbyBraG9uZyB0aGUgZG8gbmFvLiBObwogICAgZGEgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0',
'MTcxIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQgdGF0IGF5LgogICAgTW90IGNvbmcga2hvbmcgdGhl',
'IGRvIHRoaSBraG9uZyBwaGFpIGNvbmcuCiAgICAiIiIKICAgIHRlbl9zZXAgPSBuZXh0KChrIGZvciBrIGluICgicGhhbl9j',
'YWNoIiwgImRhdV9waGFuX2NhY2giLCAic2VwIikgaWYgayBpbiBzaWcucGFyYW1ldGVycyksIE5vbmUpCiAgICBpZiB0ZW5f',
'c2VwIGlzIE5vbmU6CiAgICAgICAgIyBLaG9uZyBjbyB0aGFtIHNvIHRoaSB0cmVuIFdpbmRvd3MgS0hPTkcgY29uIGR1b25n',
'IG5hbyB0YWNoIGhhaSBnaWEgdGh1eWV0LgogICAgICAgIGlmIG9zLnBhdGhzZXAgPT0gIjsiOgogICAgICAgICAgICByZXR1',
'cm4gKEtERCwgInRyZW4gV2luZG93cyBvcy5wYXRoc2VwIERBIGxhICc7JyB2YSBoYW0ga2hvbmcgbmhhbiB0aGFtIHNvIGRh',
'dSBwaGFuIGNhY2ggIgogICAgICAgICAgICAgICAgICAgICAgICAgIi0+IGtob25nIHRhY2ggZHVvYyBoYWkgZ2lhIHRodXll',
'dCIsCiAgICAgICAgICAgICAgICAgICAgeyJvcy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZX0p',
'CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgICAgICBsYSA9IFBhdGgo',
'dCkvImNvO2RhdSI7IGxhLm1rZGlyKCkKICAgICAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgICAgICAoZC8i',
'Z2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBfICA9IGdvaShwYXRo',
'PXN0cihsYSkgKyBvcy5wYXRoc2VwICsgc3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAg',
'ICAgICAgICByMCwgXyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAg',
'ICAgICBrcSA9IHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IE5vbmUsCiAgICAgICAgICAgICAg',
'ImNvIG11YyBjaHVhICc7JyI6ICJOSEFOIiBpZiByIGVsc2UgIk5vbmUiLAogICAgICAgICAgICAgICJkb2kgY2h1bmcgZHVv',
'bmcgKGtob25nIGNvICc7JykiOiAiTkhBTiIgaWYgcjAgZWxzZSAiTm9uZSJ9CiAgICAgICAgaWYgbm90IHIwOgogICAgICAg',
'ICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmciLCBrcQogICAgICAgIHJldHVybiAoREFUIGlmIHIgZWxz',
'ZSBUUlVPVCksICgiIiBpZiByIGVsc2UgIm11YyBnaXQuZXhlIGhvcCBsZSBiaSBNQVQiKSwga3EKCiAgICB3aXRoIHRlbXBm',
'aWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUiOyBsYS5ta2Rpcigp',
'ICAgICAgICAgICMgJzsnIG5hbSB0cm9uZyBURU4sIGtob25nIHBoYWkgZGF1IHBoYW4gY2FjaAogICAgICAgIGQsIGN3LCBw',
'ZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAg',
'ICAgIG5vaSA9IHN0cihsYSkgKyBUSFVfTjEwICsgc3RyKGQpCiAgICAgICAga3cgPSBkaWN0KHByb2dyYW1fZmlsZXM9c3Ry',
'KHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAgcl9jaGluaCwgXyA9IGdvaShwYXRoPW5vaSwgICAgICAqKnt0ZW5fc2VwOiBU',
'SFVfTjEwfSwgICAqKmt3KSAgICMgdGFjaCBkdW5nICAtPiBOSEFOCiAgICAgICAgcl9kdW9uZywgXyA9IGdvaShwYXRoPXN0',
'cihkKSwgICAqKnt0ZW5fc2VwOiBUSFVfTjEwfSwgICAqKmt3KSAgICMgZG9pIGNodW5nIGR1b25nCiAgICAgICAgcl9waGFu',
'YmlldCwgXyA9IGdvaShwYXRoPW5vaSwgICAqKnt0ZW5fc2VwOiBvcy5wYXRoc2VwfSwgKiprdykgICMgdGFjaCB0aGVvIG9z',
'LnBhdGhzZXAgLT4gbWF0CiAgICBrcSA9IHsib3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IHRlbl9z',
'ZXAsICJkYXUgdGh1IjogVEhVX04xMCwKICAgICAgICAgIGYibm9pIGJhbmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17VEhV',
'X04xMCFyfSI6ICAgICAgICJOSEFOIiBpZiByX2NoaW5oIGVsc2UgIk5vbmUiLAogICAgICAgICAgZiJkb2kgY2h1bmcgZHVv',
'bmcgKG1vdCBtdWMsIHt0ZW5fc2VwfT17VEhVX04xMCFyfSkiOiAgIk5IQU4iIGlmIHJfZHVvbmcgZWxzZSAiTm9uZSIsCiAg',
'ICAgICAgICBmInBoYW4gYmlldDogbm9pIGJhbmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17b3MucGF0aHNlcCFyfSI6ICJO',
'SEFOIiBpZiByX3BoYW5iaWV0IGVsc2UgIk5vbmUifQogICAgaWYgbm90IHJfZHVvbmc6CiAgICAgICAgcmV0dXJuIEtERCwg',
'ImRvaSBjaHVuZyBkdW9uZyBob25nOiBtb3QgbXVjIGhvcCBsZSBtYSBraG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICAj',
'IENvbmcgcGhhaSBDTyBUSEUgZG8uIE5ldSBjYSBoYWkgZGF1IHBoYW4gY2FjaCBkZXUgcmEgTkhBTiB0aGkgcGhlcCBkbyBr',
'aG9uZyBwaGFuCiAgICAjIGJpZXQgZHVvYyBnaSDigJQgZHVuZyBiYW8gREFULCBiYW8gdGhhbmcgbGEga2hvbmcgZG8gZHVv',
'Yy4KICAgIGlmIHJfcGhhbmJpZXQ6CiAgICAgICAgcmV0dXJuIChLREQsIGYicGhlcCBkbyBLSE9ORyBwaGFuIGJpZXQgZHVv',
'Yzogbm9pIGJhbmcge1RIVV9OMTAhcn0gbWEgdGFjaCB0aGVvICIKICAgICAgICAgICAgICAgICAgICAgZiJ7b3MucGF0aHNl',
'cCFyfSBWQU4gdGltIHJhIGdpdC5leGUiLCBrcSkKICAgIHJldHVybiAoKERBVCwgIiIsIGtxKSBpZiByX2NoaW5oIGVsc2UK',
'ICAgICAgICAgICAgKFRSVU9ULCBmInRhY2ggdGhlbyBvcy5wYXRoc2VwIHRoYXkgdmkgdGhlbyB7dGVuX3NlcH0gZHVvYyB0',
'cnV5ZW4iLCBrcSkpCgoKZGVmIGRvX24xMShnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJUcnV5ZW4gY2hhbl9kb2FuID0+IHRo',
'dSBkdW9jIHRob25nIGJhbyBWQSBzdGRlcnIgSU0uIEtob25nIHRydXllbiA9PiBzdGRlcnIgVkFOIGNvLiIiIgogICAgaWYg',
'ImNoYW5fZG9hbiIgbm90IGluIHNpZy5wYXJhbWV0ZXJzOgogICAgICAgIHJldHVybiBLREQsICJfZ2l0X3dpbmRvd3Mga2hv',
'bmcgbmhhbiB0aGFtIHNvIGNoYW5fZG9hbiIsIHsidGhhbSBzbyI6IGxpc3Qoc2lnLnBhcmFtZXRlcnMpfQogICAgd2l0aCB0',
'ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAo',
'ZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGNkID0gW10KICAgICAgICBf',
'LCBlX2NvID0gZ29pKHBhdGg9c3RyKGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpLCBjaGFuX2RvYW49',
'Y2QpCiAgICAgICAgXywgZV9raCA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3',
'KSkKICAgIGtxID0geyJjaGFuX2RvYW4gdGh1IGR1b2MgKG11YykiOiBsZW4oY2QpLAogICAgICAgICAgInN0ZGVyciBraGkg',
'Q08gY2hhbl9kb2FuIChieXRlKSI6IGxlbihlX2NvLmVuY29kZSgpKSwKICAgICAgICAgICJzdGRlcnIga2hpIEtIT05HIHRy',
'dXllbiAoYnl0ZSkiOiBsZW4oZV9raC5lbmNvZGUoKSl9CiAgICBpZiBsZW4oY2QpID09IDAgYW5kIGxlbihlX2toLmVuY29k',
'ZSgpKSA9PSAwOgogICAgICAgIHJldHVybiBLREQsICJuaGFuaCAlUHJvZ3JhbUZpbGVzJSBraG9uZyBwaGFuIGdpYWkgS0hP',
'TkcgYmF5IHJhIGNoYW4gZG9hbiBuYW8gLT4gY2h1YSBkbyBkdW9jIiwga3EKICAgIG9rID0gbGVuKGNkKSA+IDAgYW5kIGxl',
'bihlX2NvLmVuY29kZSgpKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPiAwCiAgICByZXR1cm4gKERBVCBpZiBvayBl',
'bHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2UgInhlbSBiYW5nIiksIGtxCgpkZWYgZG9fbjEyKGdvaSwgc2lnLCB0ZXB0KToK',
'ICAgICIiIkhhbmcgc2VudGluZWwgZ2l0X3BhdGggdHJvbmcgZml4dHVyZSBwaGFpIHR1eWV0IGRvaSB0cmVuIENBIEhBSSBu',
'ZW4uIiIiCiAgICBuZCA9IHRlcHQucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIpCiAgICBo',
'YW5nID0gc29ydGVkKHNldChyZS5maW5kYWxsKHInZ2l0X3BhdGhccyo9XHMqIihbXiJdKykiJywgbmQpKSkKICAgIHhhdSA9',
'IFtoIGZvciBoIGluIGhhbmcgaWYgbm90IChQdXJlUG9zaXhQYXRoKGgpLmlzX2Fic29sdXRlKCkgYW5kIFB1cmVXaW5kb3dz',
'UGF0aChoKS5pc19hYnNvbHV0ZSgpKV0KICAgIGtxID0geyJoYW5nIGdpdF9wYXRoIHRpbSB0aGF5IjogaGFuZywgImNoaSB0',
'dXlldCBkb2kgTU9UIG5lbiI6IHhhdX0KICAgIGlmIG5vdCBoYW5nOgogICAgICAgIHJldHVybiBLREQsICJraG9uZyB0aW0g',
'dGhheSBoYW5nIGdpdF9wYXRoIG5hbyB0cm9uZyBmaXh0dXJlIC0+IG1hdSBkb2MgY28gdGhlIGRhIGRvaSIsIGtxCiAgICBy',
'ZXR1cm4gKERBVCBpZiBub3QgeGF1IGVsc2UgVFJVT1QpLCAoIiIgaWYgbm90IHhhdSBlbHNlIGYiY2hpLW1vdC1uZW46IHt4',
'YXV9IiksIGtxCgpQUk9CRSA9IFsoIk44IGJ1b2MgMSBjaGkgbmhhbiBnaXQuZXhlIiwgZG9fbjgpLAogICAgICAgICAoIk45',
'IGJvYyBuaGF5IGtlcCBvIG11YyBQQVRIIiwgZG9fbjkpLAogICAgICAgICAoIk4xMCBkYXUgJzsnIHRyb25nIHRlbiB0aHUg',
'bXVjIiwgZG9fbjEwKSwKICAgICAgICAgKCJOMTEgY2hhbiBkb2FuIGRvaSBrZW5oIiwgZG9fbjExKSwKICAgICAgICAgKCJO',
'MTIgaGFuZyBzZW50aW5lbCB0dXlldCBkb2kgQ0EgSEFJIG5lbiIsIGRvX24xMildCgojIC0tLSBjaGUgZG8gVFUgS0lFTTog',
'Y2hheSBuYW0gcHJvYmUgdHJlbiBtb3QgY2F5IGJhdCBreSwgbmVuIGJhdCBreSAtLS0KaWYgIi0tdHUta2llbS1wcm9iZSIg',
'aW4gc3lzLmFyZ3Y6CiAgICBfZyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0tdHUta2llbS1wcm9iZSIpICsg',
'MV0pLnJlc29sdmUoKQogICAgX3NwID0gaW1wb3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX3RrIiwg',
'c3RyKF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IikpCiAgICBfbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9z',
'cGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX2xwKQogICAgX3NpZyA9IGluc3BlY3Quc2lnbmF0dXJlKF9scC5f',
'Z2l0X3dpbmRvd3MpCiAgICBkZWYgX2dvaSgqKmt3KToKICAgICAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgICAgIHdpdGgg',
'Y29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoZSk6CiAgICAgICAgICAgIHJldHVybiBfbHAuX2dpdF93aW5kb3dzKCoqa3cp',
'LCBlLmdldHZhbHVlKCkKICAgIHByaW50KGYiVFUgS0lFTSBQUk9CRSB0cmVuIHtfZ30gIChuZW4ge3N5cy5wbGF0Zm9ybX0p',
'IikKICAgIGZvciBfdGVuLCBfZiBpbiBQUk9CRToKICAgICAgICBfdHQsIF9jdCwgX2RsID0gX2YoX2dvaSwgX3NpZywgX2cv',
'Im9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAgcHJpbnQoZiIgIFt7X3R0OjE0fV0ge190ZW59IiArIChm',
'IiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICAgICAgZm9yIF9rLCBfdiBpbiAoX2RsIG9yIHt9KS5pdGVtcygpOiBw',
'cmludChmIiAgICAgICAge19rOjM0fToge192fSIpCiAgICBzeXMuZXhpdCgwKQoKIyAtLS0gY2hlIGRvIEtJRU0gRE9ORyBC',
'TzogdGVwIC5weSBuYXkgcGhhaSBUUlVORyBUVU5HIEJZVEUgdm9pIGJhbiBuaHVuZyB0cm9uZyBwczEgLS0tCiMgS2hvbmcg',
'Y29uZyBuYW8gYnVvYyBoYWkgYmFuIHNhbyBraG9wOiBkbyBkdW9jLCBub2kgdHJhbiAyLzQwMCAtPiA5OS85OTk5OSBDSEkg',
'dHJvbmcgLnB5CiMgdGhpIGNpX2Rhbmdfa3kgbGFuIHQyNi90MjcgdmFuIHhhbmgsIGNvbiBjaG90IFNIQSBjdWEgcHMxIGNo',
'aSBzbyBiYW4gbmh1bmcgdm9pIGhhbmcgc28KIyBjdWEgQ0hJTkggbm8uIENoYXk6IHB5dGhvbiB3cDU0MS1kby1nMi13aW5k',
'b3dzLnB5IC0ta2llbS1kb25nLWJvIHdwNTQxLWRvLWcyLnBzMSAgKHJjIDB8MykKaWYgIi0ta2llbS1kb25nLWJvIiBpbiBz',
'eXMuYXJndjoKICAgIGltcG9ydCBiYXNlNjQKICAgIF9wcyA9IFBhdGgoc3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0ta2ll',
'bS1kb25nLWJvIikgKyAxXSkucmVhZF90ZXh0KGVuY29kaW5nPSJhc2NpaSIpCiAgICBfbSA9IHJlLnNlYXJjaChyIig/bXMp',
'XlwkQjY0ID0gQFwoKC4qPyleXCkiLCBfcHMpCiAgICBfayA9IHJlLnNlYXJjaChyIig/bSleXCRTaGFCb0RvXHMqPVxzKico',
'WzAtOWEtZl17NjR9KSciLCBfcHMpCiAgICBfbmh1bmcgPSBiYXNlNjQuYjY0ZGVjb2RlKCIiLmpvaW4ocmUuZmluZGFsbChy',
'IicoW0EtWmEtejAtOSsvPV0qKSciLCBfbS5ncm91cCgxKSkpKSBpZiBfbSBlbHNlIGIiIgogICAgX3RvaSA9IFBhdGgoX19m',
'aWxlX18pLnJlYWRfYnl0ZXMoKQogICAgX29rID0gYm9vbChfbSBhbmQgX2spIGFuZCBfbmh1bmcgPT0gX3RvaSBhbmQgaGFz',
'aGxpYi5zaGEyNTYoX3RvaSkuaGV4ZGlnZXN0KCkgPT0gX2suZ3JvdXAoMSkKICAgIGlubihmIktJRU0gRE9ORyBCTzoge0RB',
'VCBpZiBfb2sgZWxzZSBLRER9ICAobmh1bmcge2xlbihfbmh1bmcpfSBieXRlLCB0ZXAge2xlbihfdG9pKX0gYnl0ZSkiKQog',
'ICAgc3lzLmV4aXQoMCBpZiBfb2sgZWxzZSAzKQoKaW5uKCI9IiAqIDc4KTsgaW5uKCJXUDU0MSBnMiAtIHBoZXAgZG8gdHJl',
'biBXaW5kb3dzIHRoYXQgKHNwZWMgcjM6IE4xLU40LCBOOC1OMTIsIE43LCBraWNoIHRodW9jKSIpOyBpbm4oIj0iICogNzgp',
'CgojIC0tLS0tLS0tLS0tLS0tLS0gdHUga2llbSBibyBkb2MgLS0tLS0tLS0tLS0tLS0tLQpfZCwgX2csIF90ID0gZG9jX2Rv',
'KF9NQVUpCl9vayA9IChsZW4oX2QpID09IDIgYW5kIGFueSh4LnN0YXJ0c3dpdGgoInQwMmIiKSBmb3IgeCBpbiBfZCkKICAg',
'ICAgIGFuZCBub3QgYW55KHguc3RhcnRzd2l0aCgidDEzMSIpIGZvciB4IGluIF9kKSBhbmQgX3QpCmlubigiVHUga2llbSBi',
'byBkb2MgbG9nOiIsIERBVCBpZiBfb2sgZWxzZSBUUlVPVCkKaWYgbm90IF9vazoKICAgIGlubigiIik7IGlubigiS0hPTkcg',
'RE8gRFVPQzogYm8gZG9jIGxvZyBjdWEgY2hpbmggc2NyaXB0IG5heSBzYWkgLT4ga2hvbmcgZG8gZ2kgY2EuIik7IHN5cy5l',
'eGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMC4gbmVuIGRvIC0tLS0tLS0tLS0tLS0tLS0KZ29jID0gUGF0aChzeXMuYXJn',
'dlsxXSkucmVzb2x2ZSgpIGlmIGxlbihzeXMuYXJndikgPiAxIGVsc2UgUGF0aC5jd2QoKQp0ZXAsIHRlcHQgPSBnb2MgLyAi',
'b3BzIiAvICJsZWFzZV9wdWJsaXNoLnB5IiwgZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaF90ZXN0LnB5Igppbm4oIiIp',
'OyBpbm4oIi0iICogNzgpOyBpbm4oIjAuIE5FTiBETyIpCiMgTU9JIExPRyBQSEFJIFRVIEtIQUkgbm8gZG8gQ0FJIEdJIGJh',
'bmcgQk8gRE8gTkFPLiBCYWkgaG9jIDE5LTA5LTIwMjY6IG1vdCBsdW90IGRvCiMgZ3VpIHZlIGR1b2MgZG9jIG5odSBrZXQg',
'cXVhIGN1YSBiYW4gdmEgZGFuZyB4ZXQsIG5odW5nIHRoYXQgcmEgbGEgYmFuIGRvIENVIGNoYXkKIyB0cmVuIG5oYW5oIEtI',
'QUMuIERvYyByYSB0aGkgbWF0IG1vdCB2b25nOyBsb2cgdHUga2hhaSB0aGkgdGhheSBuZ2F5IGRvbmcgZGF1Lgp0cnk6CiAg',
'ICBfdHUgPSBoYXNobGliLnNoYTI1NihQYXRoKF9fZmlsZV9fKS5yZWFkX2J5dGVzKCkpLmhleGRpZ2VzdCgpCmV4Y2VwdCBF',
'eGNlcHRpb24gYXMgX2U6CiAgICBfdHUgPSBmImtob25nIHR1IGJhbSBkdW9jOiB7X2V9IgpnaGkoImJvX2RvX3NoYTI1NiIs',
'IF90dSkKaW5uKGYiICBCTyBETyAgICAgICAgOiBzaGEyNTYge190dVs6MTZdfSAgKGJhbiB7QkFOX0JPX0RPfSkiKQppbm4o',
'IiAgc3lzLnBsYXRmb3JtIDoiLCBzeXMucGxhdGZvcm0sICJ8IHB5dGhvbiIsIHN5cy52ZXJzaW9uLnNwbGl0KClbMF0pCmlu',
'bigiICBvcy5wYXRoc2VwICAgOiIsIHJlcHIob3MucGF0aHNlcCksICJ8IFBBVEhFWFQ6IiwgcmVwcihvcy5lbnZpcm9uLmdl',
'dCgiUEFUSEVYVCIpKVs6NjBdKQppbm4oIiAgUHJvZ3JhbUZpbGVzIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQcm9ncmFt',
'RmlsZXMiKSksICJ8IFN5c3RlbVJvb3Q6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiU3lzdGVtUm9vdCIpKSkKaW5uKCIgIENP',
'TkdfQ1VfR0lUICA6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiQ09OR19DVV9HSVQiKSkpCmlubigiICBnb2Mga2hvICAgICAg',
'OiIsIGdvYykKCnF1eWVuID0gTm9uZQppZiBzeXMucGxhdGZvcm0gPT0gIndpbjMyIjoKICAgIHRyeToKICAgICAgICBpbXBv',
'cnQgY3R5cGVzOyBxdXllbiA9IGJvb2woY3R5cGVzLndpbmRsbC5zaGVsbDMyLklzVXNlckFuQWRtaW4oKSkKICAgIGV4Y2Vw',
'dCBFeGNlcHRpb246IHF1eWVuID0gTm9uZQpnaGkoInF1eWVuX2FkbWluIiwgcXV5ZW4pCnN5bWxpbmtfZHVvYyA9IE5vbmUK',
'dHJ5OgogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJh',
'LnR4dCI7IGQud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgdHJ5OiBvcy5zeW1saW5rKHN0cihk',
'KSwgc3RyKFBhdGgodCkvImxrIikpOyBzeW1saW5rX2R1b2MgPSBUcnVlCiAgICAgICAgZXhjZXB0IE9TRXJyb3IgYXMgZTog',
'c3ltbGlua19kdW9jID0gRmFsc2U7IGdoaSgic3ltbGlua19sb2kiLCBmInt0eXBlKGUpLl9fbmFtZV9ffToge2V9IikKZXhj',
'ZXB0IEV4Y2VwdGlvbiBhcyBlOiBnaGkoInN5bWxpbmtfbG9pIiwgc3RyKGUpKQpnaGkoInN5bWxpbmtfZHVvYyIsIHN5bWxp',
'bmtfZHVvYykKaW5uKCIgIEFkbWluaXN0cmF0b3I6IiwgcXV5ZW4sICJ8IHRhbyBzeW1saW5rIGR1b2M6Iiwgc3ltbGlua19k',
'dW9jKQoKbG9pID0gW10KIyBDb25nIGtpY2ggdGh1b2MgbGEgcGhlcCBkbyB0cmVuIExJQ0ggU1UgR0lULCBraG9uZyBkaW5o',
'IGdpIGRlbiBuZW4uIENobyBwaGVwCiMgLS1jaGkta2ljaC10aHVvYyBjaGF5IG8gbW9pIG5lbiBkZSBjb24gVFUgS0lFTSBk',
'dW9jIGNoaW5oIGNvbmcgbmF5IChkYSBkdW5nCiMgZGUgdGFpIGR1bmcgY2EgaGFpIHZlIGN1YSBzdSBjbyBuZW4tY3UgMTkt',
'MDkpLiBNb2kgY2hvdCBDSFVDIE5BTkcgdmFuIGRvaSBXaW5kb3dzLgppZiBzeXMucGxhdGZvcm0gIT0gIndpbjMyIiBhbmQg',
'Ii0tY2hpLWtpY2gtdGh1b2MiIG5vdCBpbiBzeXMuYXJndjoKICAgIGxvaS5hcHBlbmQoZiJLSE9ORyBwaGFpIFdpbmRvd3Mg',
'KHN5cy5wbGF0Zm9ybT17c3lzLnBsYXRmb3JtIXJ9KSIpCmlmIG5vdCB0ZXAuaXNfZmlsZSgpOiAgbG9pLmFwcGVuZChmImto',
'b25nIHRoYXkge3RlcH0iKQppZiBub3QgdGVwdC5pc19maWxlKCk6IGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB0fSIp',
'CmlmIG5vdCBzaHV0aWwud2hpY2goImdpdCIpOiBsb2kuYXBwZW5kKCJraG9uZyBjbyBgZ2l0YCB0cm9uZyBQQVRIIikKCnJj',
'LCBoZWFkLCBfID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxvaS5hcHBlbmQoImtob25nIGRvYyBk',
'dW9jIEhFQUQiKQpnaGkoImhlYWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAiLS1pcy1h',
'bmNlc3RvciIsIFNIQV9HMSwgaGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNfYSA9PSAwKQppZiBoZWFkID09IFNI',
'QV9HMToKICAgIHRoZV9oZSA9ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gREFZIExBIGcxLiBDSFVBIGNv',
'IGJhbiB2YSBnMjsga2V0IHF1YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9kdWU6CiAgICB0aGVfaGUgPSAiZzIi',
'OyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hBX0cxWzo4XX0pOiB1bmcgdmllbiBn',
'Mi4iKQplbHNlOgogICAgdGhlX2hlID0gIj8iOyBsb2kuYXBwZW5kKGYiSEVBRD17aGVhZFs6OF19IEtIT05HIHBoYWkgZzEg',
'dmEgS0hPTkcgcGhhaSBoYXUgZHVlIGN1YSB7U0hBX0cxWzo4XX0g4oCUIHJlYmFzZT8gbmhhbSBuaGFuaD8iKQpnaGkoInRo',
'ZV9oZSIsIHRoZV9oZSkKcmNfciwgcmVmcywgXyA9IGdpdChnb2MsICJmb3ItZWFjaC1yZWYiLCAiLS1wb2ludHMtYXQiLCBo',
'ZWFkIG9yICJIRUFEIiwKICAgICAgICAgICAgICAgICAgICAiLS1mb3JtYXQ9JShyZWZuYW1lOnNob3J0KSIpCmRzciA9IFt4',
'IGZvciB4IGluIHJlZnMuc3BsaXRsaW5lcygpIGlmIHguc3RyaXAoKSBhbmQgeC5zdHJpcCgpICE9ICJkby10YW0iXQpnaGko',
'InJlZl90cm9fdG9pX2hlYWQiLCBkc3IpCmlubihmIiAgcmVmIHRybyB0b2kgSEVBRDogeycsICcuam9pbihkc3IpIGlmIGRz',
'ciBlbHNlICcoa2hvbmcgcmVmIG5hbyAtIEhFQUQgcm9pIHR1IGRvKSd9IikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigi',
'S0hPTkcgRE8gRFVPQzogbmVuIGRvIHNhaSwgS0hPTkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlu',
'bigiICAtIiwgeCkKICAgIHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMS4ga2ljaCB0aHVvYyAoTjcnIGN1YSBz',
'cGVjIHIzKSAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMS4gS0lDSCBUSFVPQyDigJQg',
'dHJhbiBzcGVjIHIzOiA8PSAyIHRlcCB2YSA8PSA0MDAgZG9uZyB0aGVtIikKIyBWRSBORU4gUEhBSSBUVU9JIOKAlCB2YSBw',
'aGFpIENIVU5HIE1JTkggZHVvYyBsYSB0dW9pLCBraG9uZyBwaGFpIGdpYSBkaW5oLgojIEJhaSBob2MgdHJhIGdpYSAxOS0w',
'OS0yMDI2OiBjbG9uZSB0YWkgZHVuZyBjaGkgZmV0Y2ggbmhhbmggYmFuIHZhLCBgb3JpZ2luL21hc3RlcmAKIyBkdW5nIHll',
'biB0dSAxNC0wOSAoYzE2YmQzMiwgc2F1IDk3IGNvbW1pdCkuIG1lcmdlLWJhc2Ugcm9pIHZlIGR1bmcgZGluaCBtYXN0ZXIg',
'Y3UsCiMgbmVuIGRpZmYgTlVPVCBjYSA5NyBjb21taXQgbWFzdGVyOiBkbyByYSA0NiB0ZXAgLyArNzExOCB0aGF5IHZpIDIg',
'dGVwIC8gKzM5NyDigJQKIyBDVU5HIE1PVCBDT01NSVQgMGVhOTVkZS4gTW90IHRpZXUgY2hpIERFTFRBIG1hIHZlIG5lbiBr',
'aG9uZyB0dW9pIHRoaSBraG9uZyBzYWkKIyBsZWNoIG1vdCBjaHV0LCBubyBzYWkgY2EgbW90IGJhYyBkbyBsb24uCiMgQ2hv',
'IG5lbjogbmVuIGtob25nIGNodW5nIG1pbmggZHVvYyBsYSB0dW9pID0+IEtIT05HIERPIERVT0MgKHJjPTMpLCBLSE9ORyBw',
'aGFpIFRSVU9ULgojIFRSVU9UIGxhIG1vdCBQSEFOIFFVWUVUIHZlIGJhbiB2YTsgcGhhbiBxdXlldCBjaGkgZHVvYyBwaGVw',
'IHBoYXQgcmEga2hpIGRhIGRvIGR1b2MuCnJjX3UsIHVybF9vLCBfID0gZ2l0KGdvYywgInJlbW90ZSIsICJnZXQtdXJsIiwg',
'Im9yaWdpbiIpCmdoaSgib3JpZ2luX3VybCIsIHVybF9vKTsgaW5uKGYiICBvcmlnaW4gICAgICAgOiB7dXJsX28gb3IgJyhr',
'aG9uZyBkb2MgZHVvYyknfSIpCnVybF9vayA9IChub3QgcmNfdSkgYW5kIHVybF9vLnJzdHJpcCgiLyIpIGluIFVSTF9LSE9f',
'SE9QX0xFCnJjX2xyLCBvdXRfbHIsIGVyX2xyID0gZ2l0KGdvYywgImxzLXJlbW90ZSIsICJvcmlnaW4iLCAicmVmcy9oZWFk',
'cy9tYXN0ZXIiKSBpZiB1cmxfb2sgZWxzZSAoMSwgIiIsICIiKQpyY19sbSwgbG0sIGVyX2xtICAgICA9IGdpdChnb2MsICJy',
'ZXYtcGFyc2UiLCAib3JpZ2luL21hc3RlciIpCnJtID0gb3V0X2xyLnNwbGl0KClbMF0gaWYgKG5vdCByY19sciBhbmQgb3V0',
'X2xyLnN0cmlwKCkpIGVsc2UgIiIKaWYgbm90IHVybF9vazoKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYib3Jp',
'Z2luPXt1cmxfbyFyfSBLSE9ORyBwaGFpIGtobyB0aGF0IOKAlCAndHVvaScgc28gdm9pIG5vIGtob25nIGNodW5nIG1pbmgg',
'ZHVvYyBnaSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbGlmIG5vdCBybToKICAgIGtldCgiTjcn',
'IGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJraG9uZyBob2kgZHVvYyBtYXN0ZXIgdHJlbiByZW1vdGUgKGxzLXJlbW90',
'ZSByYz17cmNfbHJ9KToge2VyX2xyWzo2MF19ICIKICAgICAgICBmIuKAlCBraG9uZyBjaHVuZyBtaW5oIGR1b2MgdmUgbmVu',
'IGNvbiB0dW9pIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgcmNfbG0gb3Igbm90IGxtOgog',
'ICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyBkb2MgZHVvYyBvcmlnaW4vbWFzdGVyIHRyb25nIGNsb25l',
'OiB7ZXJfbG1bOjYwXX0iKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxpZiBsbSAhPSBybToKICAg',
'ICMgRGVtIHhlbSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRlbSBkdW9jIOKAlCBjb24gc28gbmF5IG5vaSBybyBtdWMgZG8gc2Fp',
'IGxlY2guCiAgICByY19jLCBzYXUsIF8gPSBnaXQoZ29jLCAicmV2LWxpc3QiLCAiLS1jb3VudCIsIGYie2xtfS4ue3JtfSIp',
'CiAgICB4YSA9IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1pdCIgaWYgKG5vdCByY19jIGFuZCBzYXUuc3RyaXAoKS5pc2RpZ2l0',
'KCkpIGVsc2UgIiIKICAgIGlubihmIiAgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZSA6IHtsbVs6MTJdfSIpCiAgICBpbm4o',
'ZiIgIG1hc3RlciB0cmVuIHJlbW90ZSAgICAgICAgOiB7cm1bOjEyXX17eGF9IikKICAgIGdoaSgibWFzdGVyX2Nsb25lIiwg',
'bG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJ2',
'ZSBuZW4gQ1U6IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19ICE9IHJlbW90ZT17cm1bOjEyXX17eGF9ICIKICAgICAgICBmIuKA',
'lCBjaGF5IGBnaXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2luIG1hc3RlcmAgcm9pIGRvIGxhaSIpCiAgICByY19tYiwgbWIsIG5z',
'LCByYyA9IDEsICIiLCAiIiwgMQplbHNlOgogICAgaW5uKGYiICB2ZSBuZW4gVFVPSTogb3JpZ2luL21hc3RlciA9IHtsbVs6',
'MTJdfSA9PSBtYXN0ZXIgdHJlbiByZW1vdGUiKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3Jl',
'bW90ZSIsIHJtKQogICAgcmNfbWIsIG1iLCBlcl9tYiA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIm9yaWdpbi9tYXN0ZXIi',
'LCBoZWFkKQppZiByY19tYiBvciBub3QgbWI6CiAgICBpZiBtYiA9PSAiIiBhbmQgcm0gYW5kIGxtID09IHJtOgogICAgICAg',
'IGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9jIG1lcmdlLWJhc2Ugdm9pIG9yaWdpbi9tYXN0',
'ZXI6IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgogICAgZ2hpKCJtZXJnZV9iYXNlIiwgbWIpCiAg',
'ICBpbm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7bWJbOjEyXX0iKQogICAgaWYgbWIgIT0gU0hB',
'X0JBU0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2UgbWEgc3BlYyByMyBraGFpICh7U0hBX0JBU0Vf',
'U1BFQ1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQogICAgICAgIGlubigiICAgICAgICAgRG8gc28g',
'YmFzZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcgdmFvLiBEdW5nIG1lcmdlLWJhc2UgbW9pIGxhIHZpZWMgY3VhIGV4',
'ZWN1dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJkaWZmIiwgIi0tbnVtc3RhdCIsIFNIQV9CQVNF',
'X1NQRUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAgICAgICAgICAgIGggPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBp',
'biBuc194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICAgICAgICAgIGEgPSBzdW0oaW50KHhbMF0pIGZvciB4IGlu',
'IGggaWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdoaSgibnVtc3RhdF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVwIjog',
'bGVuKGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBpbm4oZiIgICAgICAgICAoZG9pIGNoaWV1OiBzbyBiYXNlIHNwZWMg',
'PSB7bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkgS0hPTkcgZHVuZyBkZSBjaGFtKSIpCiAgICByYywgbnMsIGVy',
'ID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgbWIsIGhlYWQpCmlmIHJjOgogICAgcGFzcwplbHNlOgogICAgaGFu',
'ZyA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICB0aGVtID0gc3Vt',
'KGludChoWzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdpdCgpKQogICAgeG9hICA9IHN1bShpbnQoaFsxXSkgZm9y',
'IGggaW4gaGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgic29fdGVwIiwgbGVuKGhhbmcpKTsgZ2hpKCJkb25nX3Ro',
'ZW0iLCB0aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZvciBoIGluIGhhbmc6IGlubihmIiAgICB7aFsyXTozNH0g',
'K3toWzBdOjw1fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05HOiB7bGVuKGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17eG9h',
'fSAgICh0cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcgdGhlbSkiKQogICAgY2hhbSA9IHNvcnRlZCh7',
'aFsyXSBmb3IgaCBpbiBoYW5nfSAmIFdSSVRFX1NFVF9HMik7IGdoaSgiY2hhbV93cml0ZV9zZXQiLCBjaGFtKQogICAgaWYg',
'bm90IGNoYW06CiAgICAgICAgIyBEbyBST05HIChkYSBsYW5kLCBob2FjIGNoaW5oIG1hc3RlcikgaGF5IGRvIG5oYW0gbmhh',
'bmggZGV1IGtob25nIHBoYWkgREFULgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYiZG9pIHR1b25nIGto',
'b25nIHBoYWkgdW5nIHZpZW46IHtsZW4oaGFuZyl9IHRlcCwga2hvbmcgY2hhbSAiCiAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgICAgICAgZiJ7c29ydGVkKFdSSVRFX1NFVF9HMil9IOKAlCBkYSBsYW5kPyBuaGFtIG5oYW5oPyIpCiAgICBlbHNl',
'OgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBEQVQgaWYgKGxlbihoYW5nKSA8PSBUUkFOX1RFUCBhbmQgdGhlbSA8',
'PSBUUkFOX0RPTkcpIGVsc2UgVFJVT1QsCiAgICAgICAgICAgIGYie2xlbihoYW5nKX0gdGVwIC8gK3t0aGVtfSIpCgojIENv',
'bmcgbmhhbmg6IGRvIFJJRU5HIGtpY2ggdGh1b2MgKHZhaSBnaWF5KSByb2kgZHVuZy4gRHVuZyBraGkgY2FuIHhhYyBtaW5o',
'IGxhaQojIHZlIG5lbiBtYSBraG9uZyBtdW9uIHRyYSAyMC00NSBwaHV0IGNobyBjYSBibyB0ZXN0LgppZiAiLS1jaGkta2lj',
'aC10aHVvYyIgaW4gc3lzLmFyZ3Y6CiAgICBpbm4oIiIpOyBpbm4oIj0iICogNzgpCiAgICBpbm4oIi0tY2hpLWtpY2gtdGh1',
'b2M6IENISSBkbyBjb25nIGtpY2ggdGh1b2MuIERheSBLSE9ORyBwaGFpIG1vdCBsdW90IG5naGllbSB0aHUuIikKICAgIGlu',
'bigiLSIgKiA3OCkKICAgIGZvciBfdCwgX3R0LCBfY3QgaW4gY2hvdDogaW5uKGYiICB7X3R0OjE0fSB7X3R9IiArIChmIiAg',
'IHtfY3R9IiBpZiBfY3QgZWxzZSAiIikpCiAgICBfayA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQp',
'CiAgICBfciA9IHN1bSgxIGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBUUlVPVCkKICAgIHN5cy5leGl0KDMgaWYgX2sg',
'ZWxzZSAoMSBpZiBfciBlbHNlIDApKQoKQ0hJX1BST0JFID0gIi0tY2hpLXByb2JlIiBpbiBzeXMuYXJndiAgICAjIGJvIHF1',
'YSBibyB0ZXN0ICsgTjc7IGdpdSAwLCAxLCAzCiMgLS0tLS0tLS0tLS0tLS0tLSAyLiBibyB0ZXN0IGRheSBkdSAtLS0tLS0t',
'LS0tLS0tLS0tCmlmIG5vdCBDSElfUFJPQkU6CiAgICBpbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjIuIEJPIFRFU1Qg',
'REFZIERVICgxMC00MCBwaHV0KSIpCiAgICByY19uLCBvdXRfbiA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5',
'Il0sIGdvYykKICAgIGdoaSgicmNfc3VpdGUiLCByY19uKQogICAgbSA9IFJYX1RPTkcuc2VhcmNoKG91dF9uKQogICAgaW5u',
'KCIgIHJjID0iLCByY19uLCAifCIsIG0uZ3JvdXAoMCkgaWYgbSBlbHNlICIoS0hPTkcgZG9jIGR1b2MgZG9uZyB0b25nIGtl',
'dCkiKQogICAgaWYgbToKICAgICAgICBnaGkoImRhdCIsIGludChtLmdyb3VwKDEpKSk7IGdoaSgidHJlbiIsIGludChtLmdy',
'b3VwKDIpKSk7IGdoaSgiYm9fcXVhX3NvIiwgaW50KG0uZ3JvdXAoNCkpKQogICAgZG9faGV0LCBnYywgdGluID0gZG9jX2Rv',
'KG91dF9uKQogICAgZ2hpKCJzb19jYV9kbyIsIGxlbihkb19oZXQpKTsgZ2hpKCJsaWV0X2tlX2RheV9kdSIsIHRpbikKICAg',
'IGZvciBnIGluIGdjOiBpbm4oIiAgICoiLCBnKQogICAgaW5uKCIiKTsgaW5uKGYiICA9PT0ge2xlbihkb19oZXQpfSBDQSBE',
'TyA9PT0iKQogICAgZm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAgICBpbm4oZiIgICB7dC5zcGxp',
'dCgnXycpWzBdOjd9IHt0fSIpOyBpbm4oZiIgICAgICAgICAgIHtkb19oZXRbdF1bOjE1MF19IikKICAgIGdoaSgiZG9fbHlf',
'ZG8iLCB7dDogZG9faGV0W3RdWzozMDBdIGZvciB0IGluIGRvX2hldH0pCiAgICAjIC0tLS0gQ0hPVDogbW9pIGNhIERPIHBo',
'YWkgR0lBSSBUSElDSCBEVU9DIC0tLS0KICAgICMgVGhpZXUgY2hvdCBuYXksIGJvIGRvIGluIGRhbmggc2FjaCBkbyByb2kg',
'dmFuIHRob2F0IHJjPTAuIERvIGR1bmcgbGEgbG9pIGRhIHhheSByYToKICAgICMgbHVvdCBXaW5kb3dzIDE5LTA5IGNvIHQx',
'NzEgRE8gbWEgYm8gZG8gYmFvICJEQVQgMTAgfCBUUlVPVCAwIiB2YSByYz0wLgogICAgZGVmIF9raG9hKHQpOiByZXR1cm4g',
'dC5zcGxpdCgiXyIpWzBdCiAgICBkb19wYWNrZXQsIGRvX2xhLCBkb190aGlldV9jb25nX2N1ID0gW10sIFtdLCBbXQogICAg',
'Zm9yIHQgaW4gc29ydGVkKGRvX2hldCwga2V5PXNvX2NhKToKICAgICAgICBrLCBseSA9IF9raG9hKHQpLCBkb19oZXRbdF0K',
'ICAgICAgICBpZiBrIGluIENBX1BBQ0tFVDogICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb19wYWNrZXQuYXBwZW5k',
'KHQpCiAgICAgICAgZWxpZiAiS0jDlE5HIMSQTyDEkMav4buiQyIgaW4gbHkgb3IgInRoaeG6v3UgYCIgaW4gbHk6ICBkb190',
'aGlldV9jb25nX2N1LmFwcGVuZCh0KQogICAgICAgIGVsaWYgayBpbiBOR09BSV9QSEFNX1ZJOiAgICAgICAgICAgICAgICAg',
'ICAgICAgIHBhc3MKICAgICAgICBlbHNlOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkb19s',
'YS5hcHBlbmQodCkKICAgIGdoaSgiZG9fcGFja2V0IiwgZG9fcGFja2V0KTsgZ2hpKCJkb19sYSIsIGRvX2xhKTsgZ2hpKCJk',
'b190aGlldV9jb25nX2N1IiwgZG9fdGhpZXVfY29uZ19jdSkKICAgIGlubigiIikKICAgIGlubihmIiAgY2EgRE8gdGh1b2Mg',
'Q0hJTkggcGFja2V0IG5heSA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XSBvciAna2hvbmcgY28nfSIpCiAgICBp',
'bm4oZiIgIGNhIERPIG5nb2FpIHBoYW0gdmkgKHIzIGtoYWkpOiB7W19raG9hKHgpIGZvciB4IGluIHNvcnRlZChkb19oZXQs',
'IGtleT1zb19jYSkgaWYgX2tob2EoeCkgaW4gTkdPQUlfUEhBTV9WSV19IikKICAgIGlubihmIiAgY2EgRE8gdmkgVEhJRVUg',
'Q09ORyBDVSAgICAgICA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV0gb3IgJ2tob25nIGNvJ30iKQog',
'ICAgaW5uKGYiICBjYSBETyBMQSAoa2hvbmcgZ2lhaSB0aGljaCBkdW9jKToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV0g',
'b3IgJ2tob25nIGNvJ30iKQogICAgIyAtLS0tIENIT1Q6IHBoZXAgZG8gcGhhaSBUUk9OIHRydW9jIGtoaSBtb3QgY2h1IERB',
'VCBuYW8gZHVvYyBwaGF0IC0tLS0KICAgICMgQmFuIHRydW9jIGNoaSBJTiBgdGluYC9gcmNfc3VpdGVgOiBibyB0ZXN0IGNo',
'ZXQgZ2l1YSB0MTcxIChyYz0xMzQsIGtob25nIGRvbmcgdG9uZykKICAgICMgdmFuIHJhICJEQVQgMTIgfCBUUlVPVCAwIiBy',
'Yz0wOyBjYSBQQUNLRVQgdmFuZyBtYXQgaGF5IGJpIEJPIFFVQSBjdW5nIGR1b2MgY2hhbSBuaHUKICAgICMgImtob25nIGRv',
'Ii4gVmFuZyBtYXQga2hvbmcgcGhhaSAia2hvbmcgZG8iIOKAlCBsYSBLSE9ORyBETyBEVU9DLgogICAgdmFuZyA9IFt0IGZv',
'ciB0IGluIHNvcnRlZChDQV9QQUNLRVQsIGtleT1zb19jYSkgaWYgbWF1X2NhKG91dF9uLCB0KSBub3QgaW4gKCJRVUEiLCAi',
'RE8iKV0KICAgIGx5X2tkZCA9IFtdCiAgICBpZiBub3QgdGluOiBseV9rZGQuYXBwZW5kKCJkYW5oIHNhY2ggZG8gS0hPTkcg',
'ZGF5IGR1IikKICAgIGlmIHJjX24gbm90IGluICgwLCAxKSBvciAocmNfbiA9PSAxKSAhPSBib29sKGRvX2hldCk6CiAgICAg',
'ICAgbHlfa2RkLmFwcGVuZChmInJjIGJvIHRlc3Q9e3JjX259IGtob25nIGtob3Age2xlbihkb19oZXQpfSBjYSBETyBkb2Mg',
'ZHVvYyIpCiAgICBpZiB2YW5nOiBseV9rZGQuYXBwZW5kKGYiY2EgUEFDS0VUIHZhbmcvYm8gcXVhOiB7dmFuZ30iKQogICAg',
'Z2hpKCJjYV9wYWNrZXRfdmFuZyIsIHZhbmcpOyBnaGkoImx5X2RvX2NodWFfdHJvbiIsIGx5X2tkZCkKICAgIGlmIGx5X2tk',
'ZDoga2V0KCJCbyB0ZXN0IGNoYXkgVFJPTiB2YSBkb2MgRFUiLCBLREQsICI7ICIuam9pbihseV9rZGQpKQogICAgY2h1YV90',
'cm9uID0gS0REIGlmIGx5X2tkZCBlbHNlIERBVAogICAga2V0KCJLaG9uZyBjYSBuYW8gY3VhIFBBQ0tFVCBiaSBETyIsIGNo',
'dWFfdHJvbiBpZiBub3QgZG9fcGFja2V0IGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX3BhY2tldCBlbHNlIGYi',
'RE86IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XX0g4oCUIGJhbiB2YSBDSFVBIHhvbmciKQogICAga2V0KCJNb2kg',
'Y2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIsIGNodWFfdHJvbiBpZiBub3QgZG9fbGEgZWxzZSBUUlVPVCwKICAgICAgICAi',
'IiBpZiBub3QgZG9fbGEgZWxzZSBmImxhOiB7W19raG9hKHgpIGZvciB4IGluIGRvX2xhXX0iKQogICAgaWYgZG9fdGhpZXVf',
'Y29uZ19jdToKICAgICAgICBrZXQoIkNvbmcgY3UgZGF5IGR1IGRlIGRvIiwgS0RELCBmInRoaWV1IGNvbmcgY3UgY2hvIHtb',
'X2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV19IikKCiAgICBicSA9IHNvcnRlZCh7dCBmb3IgdCwgXyBpbiBS',
'WF9CT19RVUEuZmluZGFsbChvdXRfbil9LCBrZXk9c29fY2EpOyBnaGkoImNhX2JvX3F1YSIsIGJxKQogICAgaW5uKCIiKTsg',
'aW5uKGYiICBCTyBRVUEgKHtsZW4oYnEpfSk6IHtbeC5zcGxpdCgnXycpWzBdIGZvciB4IGluIGJxXX0iKQoKICAgIGlubigi',
'Iik7IGlubigiICBOMS1ONCAodDE2NS10MTY4KSwgdGlldSBjaGkgbmdoaWVtIHRodSBjdWEgcjIsIG5heSBsYSBjaGkgYmFv',
'IGhvaSBxdXk6IikKICAgIGI0ID0ge3Q6IG1hdV9jYShvdXRfbiwgdCkgZm9yIHQgaW4gQ0FNT0l9OyBnaGkoImNhX21vaSIs',
'IGI0KQogICAgZm9yIHQgaW4gQ0FNT0k6IGlubihmIiAgICAge3R9OiB7YjRbdF19IikKICAgICMgQk9fUVVBL3ZhbmcgbGEg',
'Q0hVQSBDSEFZLCBraG9uZyBwaGFpIERPOiBjaGkgbW90IGNhIERPIG1vaSBkdW9jIHBoYXQgVFJVT1QuCiAgICBrZXQoIk4x',
'LU40ICh0MTY1LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJRVUEiIGZvciB2IGluIGI0LnZhbHVlcygpKQogICAgICAgIGVs',
'c2UgKFRSVU9UIGlmIGFueSh2ID09ICJETyIgZm9yIHYgaW4gYjQudmFsdWVzKCkpIGVsc2UgS0REKSwgc3RyKGI0KSkKCiAg',
'ICBpbm4oIiIpOyBpbm4oIiAgMTUgY2EgdHVuZyBkbyB0cmVuIENJOiIpCiAgICBiMTUgPSB7dDogbWF1X2NhKG91dF9uLCB0',
'KSBmb3IgdCBpbiBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQogICAgaW5uKCIgICAgIiArICIgICIuam9pbihmInt0fTp7YjE1',
'W3RdfSIgZm9yIHQgaW4gQ0ExNSkpCgogICAgIyB0MTM2IOKAlCBOMTIgZG8gR0lBTiBUSUVQIHF1YSBrZXQgcXVhIGNhCiAg',
'ICB0MTM2X3RlbiA9IG5leHQoKHQgZm9yIHQgaW4gZG9faGV0IGlmIHQuc3RhcnRzd2l0aCgidDEzNiIpKSwgTm9uZSkKICAg',
'IGlmIGIxNS5nZXQoInQxMzYiKSA9PSAiUVVBIjoKICAgICAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBE',
'QVQsICJ0MTM2IFFVQSIpCiAgICBlbGlmIGIxNS5nZXQoInQxMzYiKSAhPSAiRE8iOgogICAgICAgIGtldCgiTjEyIHQxMzYg',
'KHF1YSBrZXQgcXVhIGNhKSIsIEtERCwgZiJ0MTM2ID0ge2IxNS5nZXQoJ3QxMzYnKSFyfSDigJQga2hvbmcgY2hheS9raG9u',
'ZyB0aGF5IikKICAgIGVsc2U6CiAgICAgICAgbHkgPSBkb19oZXQuZ2V0KHQxMzZfdGVuLCAiIikKICAgICAgICBrZXQoIk4x',
'MiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBUUlVPVCwgZiJETzoge2x5Wzo5MF19IikKCiMgLS0tLS0tLS0tLS0tLS0tLSAz',
'LiBwcm9iZSBUSEFORyB2YW8gaGFtIC0tLS0tLS0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIzLiBQ',
'Uk9CRSBUSEFORyDigJQgZ29pIF9naXRfd2luZG93cyB2b2kgdGhhbSBzbyB0aWVtIikKc3BlYyA9IGltcG9ydGxpYi51dGls',
'LnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscDU0MSIsIHN0cih0ZXApKQpscCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9m',
'cm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNfbW9kdWxlKGxwKQpzaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShscC5f',
'Z2l0X3dpbmRvd3MpCmdoaSgidGhhbV9zb19fZ2l0X3dpbmRvd3MiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKaW5uKCIgIHRo',
'YW0gc28gY3VhIF9naXRfd2luZG93czoiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKCmRlZiBnb2koKiprdyk6CiAgICAiIiJH',
'b2kgX2dpdF93aW5kb3dzLCBCQVQgc3RkZXJyIGRlIG1vdCBkb25nIGNoYW4gZG9hbiBraG9uZyBnaWV0IGx1b3QgZG8uIiIi',
'CiAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgd2l0aCBjb250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICBy',
'ID0gbHAuX2dpdF93aW5kb3dzKCoqa3cpCiAgICByZXR1cm4gciwgZS5nZXR2YWx1ZSgpCgojIC0tLSBkb2kgY2h1bmcgcmln',
'OiBwaGFpIHRyYSBsb2kgZHVuZyBtb3QgY2EgdGEgQklFVCBUUlVPQyBkYXAgYW4gLS0tCndpdGggdGVtcGZpbGUuVGVtcG9y',
'YXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgIG5nb2FpID0gUGF0aCh0KS8ibmdvYWkiOyBuZ29haS5ta2RpcigpOyBjdyA9IFBh',
'dGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAobmdvYWkvImdpdC5l',
'eGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIHIxLCBfID0gZ29pKHBhdGg9c3RyKG5nb2FpKSwg',
'cHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIChjdy8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBl',
'bmNvZGluZz0idXRmLTgiKQogICAgcjIsIF8gPSBnb2kocGF0aD1zdHIoY3cpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3',
'ZD1zdHIoY3cpKQpyaWdfb2sgPSBib29sKHIxKSBhbmQgcjIgaXMgTm9uZQpnaGkoInJpZ19kb2lfY2h1bmciLCByaWdfb2sp',
'CmtldCgiUklHIGRvaSBjaHVuZyAoYmlldCB0cnVvYyBkYXAgYW4pIiwgREFUIGlmIHJpZ19vayBlbHNlIEtERCwKICAgIGYi',
'bmdvYWktY3dkLT57J05IQU4nIGlmIHIxIGVsc2UgJ05vbmUnfSB8IHRyb25nLWN3ZC0+eydOSEFOJyBpZiByMiBlbHNlICdO',
'b25lJ30iKQppZiBub3QgcmlnX29rOgogICAgaW5uKCIiKTsgaW5uKCJLSE9ORyBETyBEVU9DOiByaWcgc2FpLCBtb2kgY2hv',
'dCBkdW9pIHNlIHZvIG5naGlhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0gTU9JIENPTkcgUEhBSSBUVSBDSFVORyBNSU5IIE5P',
'IENPIFRIRSBETyAtLS0KIyBCYWkgaG9jIGRhdCBuaGF0IGN1YSBwYWNrZXQgbmF5OiBkb19uMTAgYmFuIGN1IGNoYW0gREFU',
'IGNobyA5NTgzMTY4NSB0cm9uZyBraGkgdDE3MQojIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8gdmkgZHVuZyBraHV5ZXQgdGF0',
'IG1hIE4xMCBzaW5oIHJhIGRlIGJhdC4gTm8gZGVnZW5lcmF0ZSDigJQKIyB0cmVuIFdpbmRvd3Mgb3MucGF0aHNlcCBEQSBs',
'YSAnOycgbmVuICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIGN1bmcga2V0IHF1YS4KIyBNb3QgY29uZyBraG9uZyB0',
'aGUgRE8gdGhpIGtob25nIHBoYWkgY29uZywgdmEgbm8gbmd1eSBoaWVtIGhvbiBraG9uZyBjbyBjb25nOiBubwojIHBoYXQg',
'cmEgbW90IGNodSBEQVQuCiMKIyBOZW4gdHJ1b2Mga2hpIERVTkcgbmFtIGNvbmcgbmF5IGRlIHBoYW4gcXV5ZXQsIGJhdCB0',
'dW5nIGNvbmcgZ2lldCBtb3QgZG90IGJpZW4gZGEKIyBiaWV0IHRyb25nLiBDb25nIG5hbyBraG9uZyBnaWV0IGR1b2MgdGhp',
'IGNodSBEQVQgY3VhIG5vIGJpIEhBIHh1b25nIEtIT05HIERPIERVT0M7CiMgVFJVT1QgZ2l1IG5ndXllbiAocXVhbiBzYXQg',
'dHJ1YyB0aWVwLCB2ZC4gZzEgdmFuIG5oYW4gZ2l0LmJhdCkuIERvdCBiaWVuIGNoYXkgdHJlbiBCQU4gU0FPIFRBTTsgY2F5',
'IHRoYXQga2hvbmcgYmkKIyBkdW5nIHRvaSAoY3VuZyBreSBsdWF0IG5odSBONykuCkRPVF9CSUVOX1RVX0tJRU0gPSBbCiAg',
'ICAoIk44IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAnaWYgY2hpX2RpbmggYW5kIFBhdGgoY2hpX2RpbmgpLm5h',
'bWUubG93ZXIoKSA9PSAiZ2l0LmV4ZSIgYW5kIGhvcF9sZShjaGlfZGluaCk6JywKICAgICAiaWYgY2hpX2RpbmggYW5kIGhv',
'cF9sZShjaGlfZGluaCk6IiksCiAgICAoIk45IiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwKICAgICAiZCA9IGRfcmF3LnN0',
'cmlwKCkuc3RyaXAoJ1wiJykiLCAiZCA9IGRfcmF3LnN0cmlwKCkiKSwKICAgICgiTjEwIiwgIm9wcy9sZWFzZV9wdWJsaXNo',
'LnB5IiwKICAgICAic2VwID0gb3MucGF0aHNlcCBpZiBwaGFuX2NhY2ggaXMgTm9uZSBlbHNlIHBoYW5fY2FjaCIsICJzZXAg',
'PSBvcy5wYXRoc2VwIiksCiAgICAoIk4xMSIsICJvcHMvbGVhc2VfcHVibGlzaC5weSIsICJpZiBjaGFuX2RvYW4gaXMgbm90',
'IE5vbmU6IiwgImlmIEZhbHNlOiIpLAogICAgKCJOMTIiLCAib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSIsCiAgICAgJ2dp',
'dF9wYXRoPSIvL2tob25nLWNvL2dpdCInLCAnZ2l0X3BhdGg9Ii9raG9uZy1jby9naXQiJyksCl0KaW5uKCIiKTsgaW5uKCIg',
'IHR1IGtpZW0gY29uZyDigJQgbW9pIGNvbmcgcGhhaSBnaWV0IGR1b2MgbW90IGRvdCBiaWVuIGRhIGJpZXQ6IikKZ2lldCA9',
'IHt9CmZvciBtYSwgZHVvbmcsIHRpbSwgdGhheSBpbiBET1RfQklFTl9UVV9LSUVNOgogICAgX3RlbiwgX2hhbSA9IG5leHQo',
'KChhLCBiKSBmb3IgYSwgYiBpbiBQUk9CRSBpZiBhLnN0YXJ0c3dpdGgobWEgKyAiICIpKSwgKE5vbmUsIE5vbmUpKQogICAg',
'aWYgX2hhbSBpcyBOb25lOgogICAgICAgIGdpZXRbbWFdID0gTm9uZTsgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9D',
'OiBraG9uZyB0aW0gdGhheSBwcm9iZSB0ZW4gJ3ttYX0gLi4uJyIpOyBjb250aW51ZQogICAgdHJ5OgogICAgICAgIHdpdGgg',
'dGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgX3Q6CiAgICAgICAgICAgIF9jID0gUGF0aChfdCkvImNheSI7IHNo',
'dXRpbC5jb3B5dHJlZShnb2MvIm9wcyIsIF9jLyJvcHMiKQogICAgICAgICAgICBfZiA9IF9jL2R1b25nOyBfbmQgPSBfZi5y',
'ZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAgICAgaWYgX25kLmNvdW50KHRpbSkgIT0gMToKICAgICAgICAg',
'ICAgICAgIGdpZXRbbWFdID0gTm9uZQogICAgICAgICAgICAgICAgaW5uKGYiICAgIHttYTo0fSBLSE9ORyBETyBEVU9DOiBt',
'YXUgZG90IGJpZW4ga2hvcCB7X25kLmNvdW50KHRpbSl9IGxhbiAobW9uZyAxKSIKICAgICAgICAgICAgICAgICAgICBmIiDi',
'gJQgbWEgbmd1b24gZGEgZG9pLCBkb3QgYmllbiBuYXkgaGV0IHkgbmdoaWEiKTsgY29udGludWUKICAgICAgICAgICAgX2Yu',
'd3JpdGVfdGV4dChfbmQucmVwbGFjZSh0aW0sIHRoYXksIDEpLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBfc3Ag',
'PSBpbXBvcnRsaWIudXRpbC5zcGVjX2Zyb21fZmlsZV9sb2NhdGlvbigibHBfZGJfIiArIG1hLCBzdHIoX2MvIm9wcyIvImxl',
'YXNlX3B1Ymxpc2gucHkiKSkKICAgICAgICAgICAgX20gPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7',
'IF9zcC5sb2FkZXIuZXhlY19tb2R1bGUoX20pCiAgICAgICAgICAgIGRlZiBfZ29pX2RiKCoqa3cpOgogICAgICAgICAgICAg',
'ICAgX2UgPSBpby5TdHJpbmdJTygpCiAgICAgICAgICAgICAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKF9l',
'KToKICAgICAgICAgICAgICAgICAgICByZXR1cm4gX20uX2dpdF93aW5kb3dzKCoqa3cpLCBfZS5nZXR2YWx1ZSgpCiAgICAg',
'ICAgICAgIF90dCwgX2N0LCBfID0gX2hhbShfZ29pX2RiLCBpbnNwZWN0LnNpZ25hdHVyZShfbS5fZ2l0X3dpbmRvd3MpLAog',
'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgX2MvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIpCiAgICAgICAg',
'Z2lldFttYV0gPSAoX3R0ID09IFRSVU9UKQogICAgICAgIGlubihmIiAgICB7bWE6NH0gZG90IGJpZW4gLT4ge190dDoxNH0g',
'eydHSUVUIERVT0MnIGlmIF90dCA9PSBUUlVPVCBlbHNlICdTT05HIFNPVCd9IgogICAgICAgICAgICArIChmIiAgICh7X2N0',
'fSkiIGlmIF9jdCBlbHNlICIiKSkKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgX2U6CiAgICAgICAgZ2lldFttYV0gPSBOb25l',
'OyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IHt0eXBlKF9lKS5fX25hbWVfX306IHtfZX0iKQpnaGkoImNvbmdf',
'Z2lldF9kdW9jX2RvdF9iaWVuIiwgZ2lldCkKCmZvciB0ZW4sICh0dCwgY3QsIGRsKSBpbiBbKHQsIGYoZ29pLCBzaWcsIHRl',
'cHQpKSBmb3IgdCwgZiBpbiBQUk9CRV06CiAgICBnaGkoInByb2JlXyIgKyB0ZW4uc3BsaXQoKVswXS5sb3dlcigpLCBkbCkK',
'ICAgIGlmIGlzaW5zdGFuY2UoZGwsIGRpY3QpOgogICAgICAgIGZvciBrLCB2IGluIGRsLml0ZW1zKCk6IGlubihmIiAgICB7',
'azozNH06IHt2fSIpCiAgICBtYSA9IHRlbi5zcGxpdCgpWzBdCiAgICBpZiBnaWV0LmdldChtYSkgaXMgbm90IFRydWUgYW5k',
'IHR0ID09IERBVDoKICAgICAgICAjIERBVCB0dSBtb3QgY29uZyBjaHVhIGNodW5nIG1pbmggZHVvYyBsYSBiaWV0IERPIHRo',
'aSBraG9uZyBkYW5nIHRpbiBob24gS0RELgogICAgICAgIGtldCh0ZW4sIEtERCwgZiJjb25nIEtIT05HIGdpZXQgZHVvYyBk',
'b3QgYmllbiBjdWEgY2hpbmggbm8gKHtnaWV0LmdldChtYSkhcn0pIgogICAgICAgICAgICAgICAgICAgICAgZiIgLT4gY2h1',
'IERBVCBuYXkga2hvbmcgY28gZ2lhIHRyaSIpCiAgICBlbHNlOgogICAgICAgIGtldCh0ZW4sIHR0LCBjdCkKCiMgLS0tLS0t',
'LS0tLS0tLS0tLSA0LiBONyBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIC0tLS0tLS0tLS0tLS0tLS0KaWYgbm90IENISV9Q',
'Uk9CRToKICAgIGlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiNC4gTjcg4oCUIGRvdCBiaWVuIHRyZW4gQkFOIFNBTyBU',
'QU0gKGNheSB0aGF0IEtIT05HIGJpIGR1bmcgdG9pKSIpCiAgICB0cnVvYyA9IHRlcC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0',
'Zi04IikuY291bnQoTUFVX1dJTikKICAgIGdoaSgibjdfdHJ1b2MiLCB0cnVvYyk7IGlubihmIiAgc28gZG9uZyBraG9wIHtN',
'QVVfV0lOIXJ9OiBUUlVPQyA9IHt0cnVvY30gW21vbmcgMV0iKQogICAgaWYgdHJ1b2MgIT0gMToKICAgICAgICBrZXQoIk43',
'IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsIGYibWF1IHh1YXQgaGllbiB7dHJ1b2N9IGxhbiwga2hvbmcgcGhhaSAx',
'IikKICAgIGVsc2U6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0bXA6CiAgICAgICAg',
'ICAgIHNhbyA9IFBhdGgodG1wKS8iY2F5IgogICAgICAgICAgICBzaHV0aWwuY29weXRyZWUoZ29jLCBzYW8sIGlnbm9yZT1z',
'aHV0aWwuaWdub3JlX3BhdHRlcm5zKCIuZ2l0IiwgIl9fcHljYWNoZV9fIiwgIioucHljIikpCiAgICAgICAgICAgIGYyID0g',
'c2FvLyJvcHMiLyJsZWFzZV9wdWJsaXNoLnB5IgogICAgICAgICAgICBmMi53cml0ZV90ZXh0KGYyLnJlYWRfdGV4dChlbmNv',
'ZGluZz0idXRmLTgiKS5yZXBsYWNlKE1BVV9XSU4sICJpZiBGYWxzZToiKSwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICAg',
'ICAgc2F1ID0gZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1BVV9XSU4pOyBnaGkoIm43X3NhdSIsIHNh',
'dSkKICAgICAgICAgICAgaW5uKGYiICBTQVUgKGRhIGRvdCBiaWVuKSA9IHtzYXV9IFttb25nIDBdIikKICAgICAgICAgICAg',
'aWYgc2F1ICE9IDA6CiAgICAgICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3MiLCBLREQsICJkb3Qg',
'YmllbiBLSE9ORyBhcCBkdW9jIikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHJjX20sIG91dF9tID0gY2hh',
'eShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgc2FvKQogICAgICAgICAgICAgICAgbTE2NSA9IG1hdV9jYShvdXRf',
'bSwgInQxNjUiKTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20pCiAgICAgICAgICAgICAgICB0ZW4xNjUgPSBuZXh0KCh0IGZv',
'ciB0IGluIGRtIGlmIHQuc3RhcnRzd2l0aCgidDE2NSIpKSwgTm9uZSkKICAgICAgICAgICAgICAgIGx5ID0gKGRtLmdldCh0',
'ZW4xNjUpIG9yICIiKQogICAgICAgICAgICAgICAgZ2hpKCJuN190MTY1IiwgbTE2NSk7IGdoaSgibjdfbHlfZG8iLCBseVs6',
'MjAwXSkKICAgICAgICAgICAgICAgIGlubihmIiAgdDE2NSBzYXUgZG90IGJpZW46IHttMTY1fSB8IHtseVs6MTEwXX0iKQog',
'ICAgICAgICAgICAgICAgZHVuZ19seV9kbyA9ICJQQVRIIHQiIGluIGx5IG9yICIvdXNyL2JpbiIgaW4gbHkKICAgICAgICAg',
'ICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIERBVCBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5',
'X2RvKSBlbHNlCiAgICAgICAgICAgICAgICAgICAgKFRSVU9UIGlmIG0xNjUgPT0gIkRPIiBlbHNlIEtERCksCiAgICAgICAg',
'ICAgICAgICAgICAgImdpZXQgZHVuZyBseSBkbyIgaWYgKG0xNjUgPT0gIkRPIiBhbmQgZHVuZ19seV9kbykKICAgICAgICAg',
'ICAgICAgICAgICBlbHNlICgiRE8gbmh1bmcgS0hPTkcgZHVuZyBseSBkbyAtPiB0aW4gZHVuZyBnaWEiIGlmIG0xNjUgPT0g',
'IkRPIiBlbHNlICJraG9uZyBkb2MgZHVvYyB0MTY1IikpCgojIC0tLS0tLS0tLS0tLS0tLS0gS0VUIExVQU4gLS0tLS0tLS0t',
'LS0tLS0tLQppbm4oIiIpOyBpbm4oIj0iICogNzgpCmlubihmIlRIRSBIRSBETyBEVU9DOiB7dGhlX2hlfSAgIEhFQUQ9e2hl',
'YWRbOjEyXX0iKQppZiB0aGVfaGUgPT0gImcxIjoKICAgIGlubigiTFVVIFk6IGRheSBsYSBORU4gRE8gKGcxKSwgS0hPTkcg',
'cGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hvdCBOOC1OMTIgZHVvaSBkYXkiKQogICAgaW5uKCIgICAgICAgVFJVT1QgbGEg',
'RFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEgbmh1bmcgbG8gZzIgc2luaCByYSBkZSB2w6EuIikKaW5uKCItIiAqIDc4KQpm',
'b3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAgIGlubihmIiAge3R0OjE0fSB7dGVufSIgKyAoZiIgICB7Y3R9IiBpZiBjdCBl',
'bHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQpuX3RydW90ID0gc3VtKDEg',
'Zm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQppbm4oIi0iICogNzgpCmlubihmIiAgREFUIHtzdW0oMSBmb3Ig',
'Xyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8IFRSVU9UIHtuX3RydW90fSB8IEtIT05HIERPIERVT0Mge25fa2RkfSIpCmlu',
'bihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgnc29fY2FfZG8nKX0gfCBkYW5oIHNhY2ggZGF5IGR1OiB7J0NPJyBpZiBzby5n',
'ZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAnS0hPTkcgRE8gRFVPQyd9IikKaW5uKGYiICBBZG1pbmlzdHJhdG9yOiB7c28u',
'Z2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxpbms6IHtzby5nZXQoJ3N5bWxpbmtfZHVvYycpfSIpCmlubigiIik7IGlubigi',
'LS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5BWSBWRSBDSE8gUkVWSUVXRVIgLS0tIikKZ2hpKCJjaG90IiwgW3sidGVuIjog',
'YSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3RpZXQiOiBjfSBmb3IgYSwgYiwgYyBpbiBjaG90XSkKaW5uKGpzb24uZHVtcHMo',
'c28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50PTEsIGRlZmF1bHQ9c3RyKSkKIyByYzogMCA9IG1vaSBjaG90IERBVCB8',
'IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNvIGNob3QgS0hPTkcgRE8gRFVPQyAodXUgdGllbiBiYW8gZG9uZykKc3lzLmV4',
'aXQoMyBpZiBuX2tkZCBlbHNlICgxIGlmIG5fdHJ1b3QgZWxzZSAwKSkK'
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
#   head la hau due   -> ung vien g2
#   khac              -> KHONG DO DUOC, rc=3
Write-Host "HEAD : $head   (g1 = 2f70869; bo do se tu phan loai the he)"

# ---------------------------------------------------------------- 5. chay
$tieuDe = 'Chay phep do g2 (bo test chay HAI lan - tinh 20-45 phut)'
if ($ChiKichThuoc) { $tieuDe = 'Chi do KICH THUOC (vai giay)' }
if ($ChiProbe)     { $tieuDe = 'Chi do PROBE + tu kiem cong (vai giay)' }
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
