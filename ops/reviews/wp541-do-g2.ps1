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
# Nhanh mac dinh la claude/va-541-t171-20260919 (ban va dang do). Doi nhanh khac:
#     ... -Nhanh fix_issue_541
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
    [string]$Nhanh   = 'claude/va-541-t171-20260919',  # nhanh mang ban va can do
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
$ShaVa      = '2f70869'        # HEAD mong cua ban va (nhanh fix_issue_541)
$ShaBoDo    = '0b8d09a5f9bf4d8e8c4ecb464191ac4206dfed523aede6182c5d24a1a8be1260'      # SHA-256 cua bo do Python nhung ben duoi

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
$BoDo = Join-Path $Base 'wp541-do-g2-windows.py'
$B64 = @(
'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIiIiV1A1NDEgZzIgLSBQSEVQIERPIFRSRU4gV0lORE9XUyBUSEFUIGNobyBzcGVj',
'IHIzIChOMS1ONCArIE44LU4xMiArIE43ICsga2ljaCB0aHVvYykuCgpDaGF5OiAgcHkgd3A1NDEtZG8tZzItd2luZG93cy5w',
'eSAiPHRodS1tdWMta2hvPiIKCktIT05HIGdoaW0gU0hBLiBObyBkbyBCQVQgS1kgZGF1IG5hbyBkYW5nIG8gdHJlbiBuaGFu',
'aCwgcm9pIFRVIFBIQU4gTE9BSToKICBoZWFkID09IDJmNzA4NjlhICAtPiBkYXkgbGEgZzEsIENIVUEgY28gYmFuIHZhIGcy',
'LiBWYW4gZG8sIG5odW5nIG5oYW4gbGEgTkVOIERPLgogIGhlYWQgbGEgaGF1IGR1ZSAgICAtPiB1bmcgdmllbiBnMi4KICBr',
'aGFjICAgICAgICAgICAgICAgLT4gS0hPTkcgRE8gRFVPQyAocmViYXNlPyBuaGFtIG5oYW5oPykgLT4gcmM9Mywga2hvbmcg',
'a2V0IGx1YW4uCgpCQSBUUkFORyBUSEFJIG8gbW9pIGNob3Q6IERBVCAvIFRSVU9UIC8gS0hPTkcgRE8gRFVPQy4gQ2FpIHRo',
'dSBiYSBLSE9ORyBkdW9jIGxhbmcgbGUKdGhhbmggbW90IHRyb25nIGhhaSBjYWkga2lhIOKAlCBkbyBsYSBjYSBkb2N0cmlu',
'ZSBgTm9uZSAhPSBGYWxzZWAgY3VhIGtoby4KCk1PSSBjaG90IGFtIGRldSBjbyBET0kgQ0hVTkcgRFVPTkcuIE1vdCBjaG90',
'IGNoaSBkbyBjaGlldSAicGhhaSB0dSBjaG9pIiB0aGkgbW90IGhhbQpgcmV0dXJuIE5vbmVgIHZvIGRpZXUga2llbiBjdW5n',
'IHF1YSBkdW9jIG5vLgoKRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaSBkdW5nIHRv',
'aS4KIiIiCmltcG9ydCBjb250ZXh0bGliLCBoYXNobGliLCBpbXBvcnRsaWIudXRpbCwgaW5zcGVjdCwgaW8sIGpzb24sIG9z',
'LCByZSwgc2h1dGlsLCBzdWJwcm9jZXNzLCBzeXMsIHRlbXBmaWxlCmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aCwgUHVyZVBv',
'c2l4UGF0aCwgUHVyZVdpbmRvd3NQYXRoCgpvcy5lbnZpcm9uLnNldGRlZmF1bHQoIlBZVEhPTlVURjgiLCAiMSIpCm9zLmVu',
'dmlyb24uc2V0ZGVmYXVsdCgiUFlUSE9OSU9FTkNPRElORyIsICJ1dGYtOCIpCmZvciBfbCBpbiAoc3lzLnN0ZG91dCwgc3lz',
'LnN0ZGVycik6CiAgICB0cnk6IF9sLnJlY29uZmlndXJlKGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIpCiAg',
'ICBleGNlcHQgRXhjZXB0aW9uOiBwYXNzCmlmIHN5cy5wbGF0Zm9ybSA9PSAid2luMzIiOgogICAgdHJ5OgogICAgICAgIGlt',
'cG9ydCBjdHlwZXMKICAgICAgICBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlNldENvbnNvbGVPdXRwdXRDUCg2NTAwMSkKICAg',
'ICAgICBjdHlwZXMud2luZGxsLmtlcm5lbDMyLlNldENvbnNvbGVDUCg2NTAwMSkKICAgIGV4Y2VwdCBFeGNlcHRpb246IHBh',
'c3MKCmRlZiBpbm4oKnApOgogICAgdmFuID0gIiAiLmpvaW4oc3RyKHgpIGZvciB4IGluIHApCiAgICB0cnk6IHByaW50KHZh',
'biwgZmx1c2g9VHJ1ZSkKICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgdHJ5OiBzeXMuc3Rkb3V0LmJ1ZmZlci53cml0',
'ZSh2YW4uZW5jb2RlKCJ1dGYtOCIsICJyZXBsYWNlIikgKyBiIlxuIik7IHN5cy5zdGRvdXQuZmx1c2goKQogICAgICAgIGV4',
'Y2VwdCBFeGNlcHRpb246IHByaW50KHZhbi5lbmNvZGUoImFzY2lpIiwgImJhY2tzbGFzaHJlcGxhY2UiKS5kZWNvZGUoImFz',
'Y2lpIiksIGZsdXNoPVRydWUpCgpTSEFfRzEgICA9ICIyZjcwODY5YTA1Mzc4NDNlOWNhZTc4NjE4ZWU3YWU4YzI2MWQ5NzJk',
'IgojIEtIT05HIGdoaW0gYmFzZS4gU3BlYyByMyBONicga2hhaSBkbyBudW1zdGF0IHNvIGQ3MDU2MjMg4oCUIE5IVU5HIHNw',
'ZWMgQ1VORyBiYW8gZXhlY3V0b3IKIyBgZ2l0IG1lcmdlIG9yaWdpbi9tYXN0ZXJgLiBTYXUgbWVyZ2UsIHBoZXAgZG8gc28g',
'ZDcwNTYyMyBOVU9UIGNhIHBoYW4gbWFzdGVyIG1hbmcgdmFvOgojIGRvIHRoYXQgMTgtMDkgdHJlbiBiYW4gdmEgZzIgY3Vh',
'IGFneSBjaG8gNSB0ZXAgLyArODEyLCB0cm9uZyBraGkgdmllYyBjdWEgYWd5IGxhIDIgdGVwIC8gKzM1My4KIyBNb3QgY2hv',
'dCBuaHUgdGhlIHNlIGJhbyAidnVvdCB0cmFuIiBjaG8gbW90IGJhbiB2YSBLSE9ORyB2dW90LiBCYXNlIGR1bmcgbGEgTUVS',
'R0UtQkFTRS4KU0hBX0JBU0VfU1BFQyA9ICJkNzA1NjIzMTYyYjc1YjczNDBlZTdjY2E1NGFjMmQyYWJiZGRiYjZmIgpCQU5f',
'Qk9fRE8gPSAiMjAyNi0wOS0xOWUiICAgICAgICAgICAgICAjIGRvaSBNT0kga2hpIHN1YSBibyBkbyAtIGxvZyB0dSBraGFp',
'IGJhbiBuYW8KVFJBTl9URVAsIFRSQU5fRE9ORyA9IDIsIDQwMCAgICAgICAgICAjIE43JyBjdWEgc3BlYyByMwpNQVVfV0lO',
'ICA9ICdpZiBuZW5fdGh1YyA9PSAid2luZG93cyI6JwojIENhIG5nb2FpIHBoYW0gdmkgcjMgwqduZ29haV9waGFtX3ZpIOKA',
'lCBkbyBDSElOSCBTUEVDIGtoYWksIGtob25nIHBoYWkgYm8gZG8gdHUgcXV5ZXQuCiMgRG8gbGEgREFOSCBTQUNIIENITyBQ',
'SEVQOiBjYSBkbyBuYW8gS0hPTkcgbmFtIHRyb25nIGRheSB2YSBLSE9ORyBwaGFpICJ0aGlldSBjb25nIGN1IgojIHRoaSBs',
'YSBUUlVPVC4gRGFuaCBzYWNoIGNhbSB0aGkgYmFvIGdpbyBjdW5nIHRoaWV1OyBkYW5oIHNhY2ggY2hvIHBoZXAgdGhpIGJp',
'ZXQgdHJ1b2MuCk5HT0FJX1BIQU1fVkkgPSBzZXQoInQxMzEgdDEzMiB0MTUwIHQxMjUgdDM1IHQzNiB0MzcgdDM4IHQzOSB0',
'NDAiLnNwbGl0KCkpCiMgQ2EgY3VhIENISU5IIHBhY2tldCBuYXkuIE1vdCBjYSBvIGRheSBtYSBETyB0aGkga2hvbmcgYmFv',
'IGdpbyBkdW9jIGJvIHF1YS4KQ0FfUEFDS0VUID0gc2V0KCJ0MTY1IHQxNjYgdDE2NyB0MTY4IHQxNjkgdDE3MCB0MTcxIHQx',
'NzIgdDE3MyIuc3BsaXQoKSkKQ0ExNSAgPSAidDEyOSB0MTMwIHQxMzEgdDEzMiB0MTMzIHQxMzYgdDEzOCB0MTM5IHQxNDQg',
'dDE0NSB0MTQ2IHQxNDcgdDE0OSB0MTUwIHQxNTEiLnNwbGl0KCkKQ0FNT0kgPSAidDE2NSB0MTY2IHQxNjcgdDE2OCIuc3Bs',
'aXQoKQoKREFULCBUUlVPVCwgS0REID0gIkRBVCIsICJUUlVPVCIsICJLSE9ORyBETyBEVU9DIgpzbywgY2hvdCA9IHt9LCBb',
'XQpkZWYgZ2hpKGssIHYpOiBzb1trXSA9IHY7IHJldHVybiB2CmRlZiBrZXQodGVuLCB0cmFuZ190aGFpLCBjaGlfdGlldD0i',
'Iik6CiAgICBjaG90LmFwcGVuZCgodGVuLCB0cmFuZ190aGFpLCBjaGlfdGlldCkpCiAgICBpbm4oZiIgIFt7dHJhbmdfdGhh',
'aToxNH1dIHt0ZW59IiArIChmIiAgIHtjaGlfdGlldH0iIGlmIGNoaV90aWV0IGVsc2UgIiIpKQogICAgcmV0dXJuIHRyYW5n',
'X3RoYWkKCiMgLS0tLS0tLS0tLS0tLS0tLSBkb2MgbG9nIGN1YSBibyB0ZXN0IChiYW4gMywgZGEgZG8gdHJlbiBsb2cgVEhB',
'VCkgLS0tLS0tLS0tLS0tLS0tLQpSWF9ET19DSE8gID0gcmUuY29tcGlsZShyIig/bSleISEhIGRvIChcUyspICguKikkIikK',
'UlhfRE9fQ1VPSSA9IHJlLmNvbXBpbGUociIoP20pXiB7Mn0oXFN7MSw0fSkgezJ9KFxTKyk6ICguKikkIikKUlhfQk9fUVVB',
'ICA9IHJlLmNvbXBpbGUociIoP20pXiB7Mn1cU3sxLDZ9IFFVQSAoXFMrKTogKC4qKSQiKQpSWF9UT05HICAgID0gcmUuY29t',
'cGlsZShyImxlYXNlX3B1Ymxpc2g6IChcZCspLyhcZCspXGJbXlxuXSo/PShcZCspLFteXG5dKj89KFxkKykiKQoKZGVmIHNv',
'X2NhKHQpOgogICAgbSA9IHJlLm1hdGNoKHIidChcZCspIiwgdCk7IHJldHVybiAoaW50KG0uZ3JvdXAoMSkpIGlmIG0gZWxz',
'ZSAxMCoqNiwgdCkKCmRlZiBkb2NfZG8ob3V0KToKICAgIHRhaV9jaG8gPSB7dDogbC5zdHJpcCgpIGZvciB0LCBsIGluIFJY',
'X0RPX0NITy5maW5kYWxsKG91dCl9CiAgICBibyA9IHt0IGZvciB0LCBfIGluIFJYX0JPX1FVQS5maW5kYWxsKG91dCl9CiAg',
'ICBjdW9pID0ge3Q6IGwuc3RyaXAoKSBmb3IgXywgdCwgbCBpbiBSWF9ET19DVU9JLmZpbmRhbGwob3V0KSBpZiB0IG5vdCBp',
'biBib30KICAgIGhvcCA9IGRpY3QoY3VvaSk7IGhvcC51cGRhdGUodGFpX2NobykKICAgIGdjLCB0aW4gPSBbXSwgVHJ1ZQog',
'ICAgaWYgc2V0KHRhaV9jaG8pICE9IHNldChjdW9pKToKICAgICAgICBnYy5hcHBlbmQoZiJoYWkgbmd1b24gTEVDSDogY2hp',
'LXRhaS1jaG89e3NvcnRlZChzZXQodGFpX2Nobyktc2V0KGN1b2kpKX0gY2hpLWN1b2k9e3NvcnRlZChzZXQoY3VvaSktc2V0',
'KHRhaV9jaG8pKX0iKQogICAgICAgIHRpbiA9IEZhbHNlCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0KQogICAgaWYgbm90',
'IG06CiAgICAgICAgZ2MuYXBwZW5kKCJLSE9ORyBkb2MgZHVvYyBkb25nIHRvbmcga2V0Iik7IHRpbiA9IEZhbHNlCiAgICBl',
'bHNlOgogICAgICAgIGRhdCwgdHJlbiA9IGludChtLmdyb3VwKDEpKSwgaW50KG0uZ3JvdXAoMikpCiAgICAgICAgZ2MuYXBw',
'ZW5kKGYic28gaG9jOiB7dHJlbn0te2RhdH09e3RyZW4tZGF0fSBkbzsgZG9jIGR1b2Mge2xlbihob3ApfSIpCiAgICAgICAg',
'aWYgdHJlbiAtIGRhdCAhPSBsZW4oaG9wKToKICAgICAgICAgICAgZ2MuYXBwZW5kKGYiTEVDSCBTTyBIT0M6IHRoaWV1IHt0',
'cmVuLWRhdC1sZW4oaG9wKX0gY2EiKTsgdGluID0gRmFsc2UKICAgIHJldHVybiBob3AsIGdjLCB0aW4KCl9NQVUgPSAoIiEh',
'ISBkbyB0MDJiX3Rlbl9LSE9OR19DT19USEFNX1FVWUVOIGFcbiIKICAgICAgICAiISEhIGRvIHQxNTBfeCBXaW5FcnJvciAx',
'MzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgICAgICIgIELhu44gUVVBIHQxMzFfeTogbmVuIGZpeHR1cmVcbiIKICAg',
'ICAgICAiICDEkOG7jiAgdDAyYl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTjogYVxuIgogICAgICAgICIgIMSQ4buOICB0MTUw',
'X3g6IFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAgICAgImxlYXNlX3B1Ymxpc2g6IDEvMyDEkeG6',
'oXQ7IMSRw6MgY2jhuqF5PTMsIGLhu48gcXVhPTFcbiIpCgpkZWYgY2hheShhcmd2LCBjd2QsIHBodXQ9NjApOgogICAgbXQg',
'PSBkaWN0KG9zLmVudmlyb24sIFBZVEhPTlVURjg9IjEiLCBQWVRIT05JT0VOQ09ESU5HPSJ1dGYtOCIsCiAgICAgICAgICAg',
'ICAgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9IjEiLCBQWVRIT05VTkJVRkZFUkVEPSIxIikKICAgIHAgPSBzdWJwcm9jZXNz',
'LnJ1bihbc3lzLmV4ZWN1dGFibGVdICsgYXJndiwgY3dkPXN0cihjd2QpLCBjYXB0dXJlX291dHB1dD1UcnVlLAogICAgICAg',
'ICAgICAgICAgICAgICAgIHRleHQ9VHJ1ZSwgZW5jb2Rpbmc9InV0Zi04IiwgZXJyb3JzPSJyZXBsYWNlIiwgdGltZW91dD1w',
'aHV0KjYwLCBlbnY9bXQpCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5zdGRvdXQgb3IgIiIpICsgKHAuc3RkZXJyIG9y',
'ICIiKQoKZGVmIG1hdV9jYShvdXQsIHQpOgogICAgbSA9IHJlLnNlYXJjaChyIig/bSlePDw8IHJhICgiICsgdCArIHIiW2Et',
'el0/X1xTKikgWzAtOS5dK3MgKFx3KylccyokIiwgb3V0KQogICAgcmV0dXJuIG0uZ3JvdXAoMikgaWYgbSBlbHNlIE5vbmUK',
'CmRlZiBnaXQoZ29jLCAqYSwgcGh1dD01KToKICAgIHAgPSBzdWJwcm9jZXNzLnJ1bihbImdpdCIsICItQyIsIHN0cihnb2Mp',
'LCAqYV0sIGNhcHR1cmVfb3V0cHV0PVRydWUsIHRleHQ9VHJ1ZSwKICAgICAgICAgICAgICAgICAgICAgICBlbmNvZGluZz0i',
'dXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjApCiAgICByZXR1cm4gcC5yZXR1cm5jb2RlLCAocC5z',
'dGRvdXQgb3IgIiIpLnN0cmlwKCksIChwLnN0ZGVyciBvciAiIikuc3RyaXAoKQoKCiMgPT09PT09PT09PT09PT09PT0gTkFN',
'IFBST0JFLCB2aWV0IHRoYW5oIEhBTSBUSFVBTiBkZSBUVSBLSUVNIGR1b2MgPT09PT09PT09PT09PT09PT0KIyBNb2kgaGFt',
'IHRyYSAodHJhbmdfdGhhaSwgY2hpX3RpZXQsIGR1X2xpZXUpLiBLSE9ORyBpbiwgS0hPTkcgdGhvYXQg4oCUIG5obyB2YXkg',
'Y2h1bmcKIyBjaGF5IGR1b2MgdHJlbiBuZW4gQkFUIEtZLCB2YSBgLS10dS1raWVtLXByb2JlYCBnb2kgdGhhbmcgY2h1bmcg',
'ZGUga2llbSBjaGluaCBibyBkby4KCmRlZiBfc2FuKHQpOgogICAgZCA9IFBhdGgodCkvImQiOyBkLm1rZGlyKCk7IGN3ID0g',
'UGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIHJldHVybiBkLCBj',
'dywgcGYKCmRlZiBkb19uOChnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJCdW9jIDEgKENPTkdfQ1VfR0lUKSBjaGkgZHVvYyBu',
'aGFuIGdpdC5leGUuIERvaSBjaHVuZyBkdW9uZzogZ2l0LmV4ZSBWQU4gcGhhaSBuaGFuLiIiIgogICAga3EgPSB7fQogICAg',
'd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAg',
'ICAgICBmb3IgdGVuIGluICgiZ2l0LmV4ZSIsICJnaXQuYmF0IiwgImdpdC5jbWQiLCAiZ2l0LnB5IiwgImtob25nLXBoYWkt',
'Z2l0LnR4dCIpOgogICAgICAgICAgICBmID0gZC90ZW47IGYud3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAg',
'ICAgICAgICAgIHIsIF8gPSBnb2koY29uZ19jdV9naXQ9c3RyKGYpLCBwYXRoPSIiLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiks',
'IGN3ZD1zdHIoY3cpKQogICAgICAgICAgICBrcVtmIkNPTkdfQ1VfR0lUPXt0ZW59Il0gPSAiTkhBTiIgaWYgciBlbHNlICJU',
'VSBDSE9JIgogICAgbG90ID0gW2sgZm9yIGssIHYgaW4ga3EuaXRlbXMoKSBpZiB2ID09ICJOSEFOIiBhbmQgbm90IGsuZW5k',
'c3dpdGgoImdpdC5leGUiKV0KICAgIGlmIGtxLmdldCgiQ09OR19DVV9HSVQ9Z2l0LmV4ZSIpICE9ICJOSEFOIjoKICAgICAg',
'ICByZXR1cm4gS0RELCAiZG9pIGNodW5nIGR1b25nIGhvbmc6IGdpdC5leGUgaG9wIGxlIG1hIGJpIHR1IGNob2kiLCBrcQog',
'ICAgcmV0dXJuIChEQVQgaWYgbm90IGxvdCBlbHNlIFRSVU9UKSwgKCIiIGlmIG5vdCBsb3QgZWxzZSBmImNvbiBuaGFuOiB7',
'bG90fSIpLCBrcQoKZGVmIGRvX245KGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIk11YyBQQVRIIGJvYyBuaGF5IGtlcCBwaGFp',
'IE5IQU47IG11YyByb25nIC8gdG9hbiBraG9hbmcgdHJhbmcgcGhhaSBibyBxdWEsIGtob25nIG5lbS4iIiIKICAgIGtxID0g',
'e30KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8iY28g',
'Z2l0IjsgZC5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0aCh0KS8icGYiOyBwZi5t',
'a2RpcigpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0Zi04IikKICAgICAgICBm',
'b3IgbmhhbiwgbXVjIGluICgoImtob25nIG5oYXkiLCBzdHIoZCkpLCAoImNvIG5oYXkga2VwIiwgZicie2R9IicpLAogICAg',
'ICAgICAgICAgICAgICAgICAgICAgICgicm9uZyIsICIiKSwgKCJjaGkga2hvYW5nIHRyYW5nIiwgIiAgICIpKToKICAgICAg',
'ICAgICAgdHJ5OgogICAgICAgICAgICAgICAgciwgXyA9IGdvaShwYXRoPW11YywgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBj',
'd2Q9c3RyKGN3KSkKICAgICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9ICJOSEFOIiBpZiByIGVsc2UgIk5vbmUi',
'CiAgICAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgICAgIGtxW2YiUEFUSCB7bmhhbn0iXSA9',
'IGYiTkVNIHt0eXBlKGUpLl9fbmFtZV9ffSIKICAgIGlmIGtxLmdldCgiUEFUSCBraG9uZyBuaGF5IikgIT0gIk5IQU4iOgog',
'ICAgICAgIHJldHVybiBLREQsICJkb2kgY2h1bmcgZHVvbmcgaG9uZzogbXVjIFBBVEggdGh1b25nIG1hIGtob25nIHRpbSBy',
'YSBnaXQuZXhlIiwga3EKICAgIG9rID0gKGtxLmdldCgiUEFUSCBjbyBuaGF5IGtlcCIpID09ICJOSEFOIgogICAgICAgICAg',
'YW5kIGtxLmdldCgiUEFUSCByb25nIikgPT0gIk5vbmUiIGFuZCBrcS5nZXQoIlBBVEggY2hpIGtob2FuZyB0cmFuZyIpID09',
'ICJOb25lIikKICAgIHJldHVybiAoREFUIGlmIG9rIGVsc2UgVFJVT1QpLCAoIiIgaWYgb2sgZWxzZSAieGVtIGJhbmciKSwg',
'a3EKCiMgRGF1IHBoYW4gY2FjaCBkdW5nIERFIFRIVS4gUGhhaSBLSEFDIG9zLnBhdGhzZXAgdHJlbiBDQSBIQUkgbmVuICgn',
'OycgV2luZG93cywgJzonIFBPU0lYKQojIHRoaSBoYWkgZ2lhIHRodXlldCAidGFjaCB0aGVvIGRhdSBkdW9jIHRydXllbiIg',
'dmEgInRhY2ggdGhlbyBvcy5wYXRoc2VwIiBtb2kgcm9pIHJhIG5oYXUuClRIVV9OMTAgPSAifCIKCmRlZiBkb19uMTAoZ29p',
'LCBzaWcsIHRlcHQpOgogICAgIiIiSGFtIHBoYWkgdGFjaCBQQVRIIHRoZW8gZGF1IHBoYW4gY2FjaCBEVU9DIFRSVVlFTiwg',
'a2hvbmcgdGhlbyBvcy5wYXRoc2VwIGN1YSBuZW4uCgogICAgQmFuIGN1IGRvICJtb3QgZGF1ICc7JyB0cm9uZyBURU4gdGh1',
'IG11YyIgdmEgZGF0IERBVCB0cmVuIFdpbmRvd3MgZHUgaGFtIHNhaS4gTm8KICAgIGRlZ2VuZXJhdGU6IHRyZW4gV2luZG93',
'cyBvcy5wYXRoc2VwIERBIGxhICc7JywgbmVuICdDOi9hO2InIHRoYXQgc3UgQ08gTkdISUEgbGEgaGFpCiAgICBtdWMg4oCU',
'ICJ0YWNoIGR1bmciIHZhICJ0YWNoIHNhaSIgY2hvIHJhIGN1bmcga2V0IHF1YSwgcGhlcCBkbyBraG9uZyB0aGUgZG8gbmFv',
'LiBObwogICAgZGEgY2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxIGN1YSBjaGluaCBiYW4gdmEgYXkgRE8g',
'dmkgZHVuZyBraHV5ZXQgdGF0IGF5LgogICAgTW90IGNvbmcga2hvbmcgdGhlIGRvIHRoaSBraG9uZyBwaGFpIGNvbmcuCiAg',
'ICAiIiIKICAgIHRlbl9zZXAgPSBuZXh0KChrIGZvciBrIGluICgicGhhbl9jYWNoIiwgImRhdV9waGFuX2NhY2giLCAic2Vw',
'IikgaWYgayBpbiBzaWcucGFyYW1ldGVycyksIE5vbmUpCiAgICBpZiB0ZW5fc2VwIGlzIE5vbmU6CiAgICAgICAgIyBLaG9u',
'ZyBjbyB0aGFtIHNvIHRoaSB0cmVuIFdpbmRvd3MgS0hPTkcgY29uIGR1b25nIG5hbyB0YWNoIGhhaSBnaWEgdGh1eWV0Lgog',
'ICAgICAgIGlmIG9zLnBhdGhzZXAgPT0gIjsiOgogICAgICAgICAgICByZXR1cm4gKEtERCwgInRyZW4gV2luZG93cyBvcy5w',
'YXRoc2VwIERBIGxhICc7JyB2YSBoYW0ga2hvbmcgbmhhbiB0aGFtIHNvIGRhdSBwaGFuIGNhY2ggIgogICAgICAgICAgICAg',
'ICAgICAgICAgICAgIi0+IGtob25nIHRhY2ggZHVvYyBoYWkgZ2lhIHRodXlldCIsCiAgICAgICAgICAgICAgICAgICAgeyJv',
'cy5wYXRoc2VwIjogb3MucGF0aHNlcCwgInRoYW0gc28gc2VwIjogTm9uZX0pCiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1w',
'b3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgICAgICBsYSA9IFBhdGgodCkvImNvO2RhdSI7IGxhLm1rZGlyKCkKICAg',
'ICAgICAgICAgZCwgY3csIHBmID0gX3Nhbih0KQogICAgICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBl',
'bmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICByLCBfICA9IGdvaShwYXRoPXN0cihsYSkgKyBvcy5wYXRoc2VwICsgc3Ry',
'KGQpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgICAgICAgICByMCwgXyA9IGdvaShwYXRoPXN0',
'cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAgICBrcSA9IHsib3MucGF0aHNlcCI6IG9z',
'LnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IE5vbmUsCiAgICAgICAgICAgICAgImNvIG11YyBjaHVhICc7JyI6ICJOSEFOIiBp',
'ZiByIGVsc2UgIk5vbmUiLAogICAgICAgICAgICAgICJkb2kgY2h1bmcgZHVvbmcgKGtob25nIGNvICc7JykiOiAiTkhBTiIg',
'aWYgcjAgZWxzZSAiTm9uZSJ9CiAgICAgICAgaWYgbm90IHIwOgogICAgICAgICAgICByZXR1cm4gS0RELCAiZG9pIGNodW5n',
'IGR1b25nIGhvbmciLCBrcQogICAgICAgIHJldHVybiAoREFUIGlmIHIgZWxzZSBUUlVPVCksICgiIiBpZiByIGVsc2UgIm11',
'YyBnaXQuZXhlIGhvcCBsZSBiaSBNQVQiKSwga3EKCiAgICB3aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFz',
'IHQ6CiAgICAgICAgbGEgPSBQYXRoKHQpLyJjbztkYXUiOyBsYS5ta2RpcigpICAgICAgICAgICMgJzsnIG5hbSB0cm9uZyBU',
'RU4sIGtob25nIHBoYWkgZGF1IHBoYW4gY2FjaAogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0',
'LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIG5vaSA9IHN0cihsYSkgKyBUSFVfTjEw',
'ICsgc3RyKGQpCiAgICAgICAga3cgPSBkaWN0KHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICAgICAg',
'cl9jaGluaCwgXyA9IGdvaShwYXRoPW5vaSwgICAgICAqKnt0ZW5fc2VwOiBUSFVfTjEwfSwgICAqKmt3KSAgICMgdGFjaCBk',
'dW5nICAtPiBOSEFOCiAgICAgICAgcl9kdW9uZywgXyA9IGdvaShwYXRoPXN0cihkKSwgICAqKnt0ZW5fc2VwOiBUSFVfTjEw',
'fSwgICAqKmt3KSAgICMgZG9pIGNodW5nIGR1b25nCiAgICAgICAgcl9waGFuYmlldCwgXyA9IGdvaShwYXRoPW5vaSwgICAq',
'Knt0ZW5fc2VwOiBvcy5wYXRoc2VwfSwgKiprdykgICMgdGFjaCB0aGVvIG9zLnBhdGhzZXAgLT4gbWF0CiAgICBrcSA9IHsi',
'b3MucGF0aHNlcCI6IG9zLnBhdGhzZXAsICJ0aGFtIHNvIHNlcCI6IHRlbl9zZXAsICJkYXUgdGh1IjogVEhVX04xMCwKICAg',
'ICAgICAgIGYibm9pIGJhbmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17VEhVX04xMCFyfSI6ICAgICAgICJOSEFOIiBpZiBy',
'X2NoaW5oIGVsc2UgIk5vbmUiLAogICAgICAgICAgZiJkb2kgY2h1bmcgZHVvbmcgKG1vdCBtdWMsIHt0ZW5fc2VwfT17VEhV',
'X04xMCFyfSkiOiAgIk5IQU4iIGlmIHJfZHVvbmcgZWxzZSAiTm9uZSIsCiAgICAgICAgICBmInBoYW4gYmlldDogbm9pIGJh',
'bmcge1RIVV9OMTAhcn0sIHt0ZW5fc2VwfT17b3MucGF0aHNlcCFyfSI6ICJOSEFOIiBpZiByX3BoYW5iaWV0IGVsc2UgIk5v',
'bmUifQogICAgaWYgbm90IHJfZHVvbmc6CiAgICAgICAgcmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nOiBtb3Qg',
'bXVjIGhvcCBsZSBtYSBraG9uZyB0aW0gcmEgZ2l0LmV4ZSIsIGtxCiAgICAjIENvbmcgcGhhaSBDTyBUSEUgZG8uIE5ldSBj',
'YSBoYWkgZGF1IHBoYW4gY2FjaCBkZXUgcmEgTkhBTiB0aGkgcGhlcCBkbyBraG9uZyBwaGFuCiAgICAjIGJpZXQgZHVvYyBn',
'aSDigJQgZHVuZyBiYW8gREFULCBiYW8gdGhhbmcgbGEga2hvbmcgZG8gZHVvYy4KICAgIGlmIHJfcGhhbmJpZXQ6CiAgICAg',
'ICAgcmV0dXJuIChLREQsIGYicGhlcCBkbyBLSE9ORyBwaGFuIGJpZXQgZHVvYzogbm9pIGJhbmcge1RIVV9OMTAhcn0gbWEg',
'dGFjaCB0aGVvICIKICAgICAgICAgICAgICAgICAgICAgZiJ7b3MucGF0aHNlcCFyfSBWQU4gdGltIHJhIGdpdC5leGUiLCBr',
'cSkKICAgIHJldHVybiAoKERBVCwgIiIsIGtxKSBpZiByX2NoaW5oIGVsc2UKICAgICAgICAgICAgKFRSVU9ULCBmInRhY2gg',
'dGhlbyBvcy5wYXRoc2VwIHRoYXkgdmkgdGhlbyB7dGVuX3NlcH0gZHVvYyB0cnV5ZW4iLCBrcSkpCgoKZGVmIGRvX24xMShn',
'b2ksIHNpZywgdGVwdCk6CiAgICAiIiJUcnV5ZW4gY2hhbl9kb2FuID0+IHRodSBkdW9jIHRob25nIGJhbyBWQSBzdGRlcnIg',
'SU0uIEtob25nIHRydXllbiA9PiBzdGRlcnIgVkFOIGNvLiIiIgogICAgaWYgImNoYW5fZG9hbiIgbm90IGluIHNpZy5wYXJh',
'bWV0ZXJzOgogICAgICAgIHJldHVybiBLREQsICJfZ2l0X3dpbmRvd3Mga2hvbmcgbmhhbiB0aGFtIHNvIGNoYW5fZG9hbiIs',
'IHsidGhhbSBzbyI6IGxpc3Qoc2lnLnBhcmFtZXRlcnMpfQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3Rvcnko',
'KSBhcyB0OgogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAoZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngi',
'LCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIGNkID0gW10KICAgICAgICBfLCBlX2NvID0gZ29pKHBhdGg9c3RyKGQpLCBw',
'cm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpLCBjaGFuX2RvYW49Y2QpCiAgICAgICAgXywgZV9raCA9IGdvaShw',
'YXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgIGtxID0geyJjaGFuX2RvYW4gdGh1',
'IGR1b2MgKG11YykiOiBsZW4oY2QpLAogICAgICAgICAgInN0ZGVyciBraGkgQ08gY2hhbl9kb2FuIChieXRlKSI6IGxlbihl',
'X2NvLmVuY29kZSgpKSwKICAgICAgICAgICJzdGRlcnIga2hpIEtIT05HIHRydXllbiAoYnl0ZSkiOiBsZW4oZV9raC5lbmNv',
'ZGUoKSl9CiAgICBpZiBsZW4oY2QpID09IDAgYW5kIGxlbihlX2toLmVuY29kZSgpKSA9PSAwOgogICAgICAgIHJldHVybiBL',
'REQsICJuaGFuaCAlUHJvZ3JhbUZpbGVzJSBraG9uZyBwaGFuIGdpYWkgS0hPTkcgYmF5IHJhIGNoYW4gZG9hbiBuYW8gLT4g',
'Y2h1YSBkbyBkdW9jIiwga3EKICAgIG9rID0gbGVuKGNkKSA+IDAgYW5kIGxlbihlX2NvLmVuY29kZSgpKSA9PSAwIGFuZCBs',
'ZW4oZV9raC5lbmNvZGUoKSkgPiAwCiAgICByZXR1cm4gKERBVCBpZiBvayBlbHNlIFRSVU9UKSwgKCIiIGlmIG9rIGVsc2Ug',
'InhlbSBiYW5nIiksIGtxCgpkZWYgZG9fbjEyKGdvaSwgc2lnLCB0ZXB0KToKICAgICIiIkhhbmcgc2VudGluZWwgZ2l0X3Bh',
'dGggdHJvbmcgZml4dHVyZSBwaGFpIHR1eWV0IGRvaSB0cmVuIENBIEhBSSBuZW4uIiIiCiAgICBuZCA9IHRlcHQucmVhZF90',
'ZXh0KGVuY29kaW5nPSJ1dGYtOCIsIGVycm9ycz0icmVwbGFjZSIpCiAgICBoYW5nID0gc29ydGVkKHNldChyZS5maW5kYWxs',
'KHInZ2l0X3BhdGhccyo9XHMqIihbXiJdKykiJywgbmQpKSkKICAgIHhhdSA9IFtoIGZvciBoIGluIGhhbmcgaWYgbm90IChQ',
'dXJlUG9zaXhQYXRoKGgpLmlzX2Fic29sdXRlKCkgYW5kIFB1cmVXaW5kb3dzUGF0aChoKS5pc19hYnNvbHV0ZSgpKV0KICAg',
'IGtxID0geyJoYW5nIGdpdF9wYXRoIHRpbSB0aGF5IjogaGFuZywgImNoaSB0dXlldCBkb2kgTU9UIG5lbiI6IHhhdX0KICAg',
'IGlmIG5vdCBoYW5nOgogICAgICAgIHJldHVybiBLREQsICJraG9uZyB0aW0gdGhheSBoYW5nIGdpdF9wYXRoIG5hbyB0cm9u',
'ZyBmaXh0dXJlIC0+IG1hdSBkb2MgY28gdGhlIGRhIGRvaSIsIGtxCiAgICByZXR1cm4gKERBVCBpZiBub3QgeGF1IGVsc2Ug',
'VFJVT1QpLCAoIiIgaWYgbm90IHhhdSBlbHNlIGYiY2hpLW1vdC1uZW46IHt4YXV9IiksIGtxCgpQUk9CRSA9IFsoIk44IGJ1',
'b2MgMSBjaGkgbmhhbiBnaXQuZXhlIiwgZG9fbjgpLAogICAgICAgICAoIk45IGJvYyBuaGF5IGtlcCBvIG11YyBQQVRIIiwg',
'ZG9fbjkpLAogICAgICAgICAoIk4xMCBkYXUgJzsnIHRyb25nIHRlbiB0aHUgbXVjIiwgZG9fbjEwKSwKICAgICAgICAgKCJO',
'MTEgY2hhbiBkb2FuIGRvaSBrZW5oIiwgZG9fbjExKSwKICAgICAgICAgKCJOMTIgaGFuZyBzZW50aW5lbCB0dXlldCBkb2kg',
'Q0EgSEFJIG5lbiIsIGRvX24xMildCgojIC0tLSBjaGUgZG8gVFUgS0lFTTogY2hheSBuYW0gcHJvYmUgdHJlbiBtb3QgY2F5',
'IGJhdCBreSwgbmVuIGJhdCBreSAtLS0KaWYgIi0tdHUta2llbS1wcm9iZSIgaW4gc3lzLmFyZ3Y6CiAgICBfZyA9IFBhdGgo',
'c3lzLmFyZ3Zbc3lzLmFyZ3YuaW5kZXgoIi0tdHUta2llbS1wcm9iZSIpICsgMV0pLnJlc29sdmUoKQogICAgX3NwID0gaW1w',
'b3J0bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwX3RrIiwgc3RyKF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNo',
'LnB5IikpCiAgICBfbHAgPSBpbXBvcnRsaWIudXRpbC5tb2R1bGVfZnJvbV9zcGVjKF9zcCk7IF9zcC5sb2FkZXIuZXhlY19t',
'b2R1bGUoX2xwKQogICAgX3NpZyA9IGluc3BlY3Quc2lnbmF0dXJlKF9scC5fZ2l0X3dpbmRvd3MpCiAgICBkZWYgX2dvaSgq',
'Kmt3KToKICAgICAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIo',
'ZSk6CiAgICAgICAgICAgIHJldHVybiBfbHAuX2dpdF93aW5kb3dzKCoqa3cpLCBlLmdldHZhbHVlKCkKICAgIHByaW50KGYi',
'VFUgS0lFTSBQUk9CRSB0cmVuIHtfZ30gIChuZW4ge3N5cy5wbGF0Zm9ybX0pIikKICAgIGZvciBfdGVuLCBfZiBpbiBQUk9C',
'RToKICAgICAgICBfdHQsIF9jdCwgX2RsID0gX2YoX2dvaSwgX3NpZywgX2cvIm9wcyIvImxlYXNlX3B1Ymxpc2hfdGVzdC5w',
'eSIpCiAgICAgICAgcHJpbnQoZiIgIFt7X3R0OjE0fV0ge190ZW59IiArIChmIiAgIHtfY3R9IiBpZiBfY3QgZWxzZSAiIikp',
'CiAgICAgICAgZm9yIF9rLCBfdiBpbiAoX2RsIG9yIHt9KS5pdGVtcygpOiBwcmludChmIiAgICAgICAge19rOjM0fToge192',
'fSIpCiAgICBzeXMuZXhpdCgwKQoKaW5uKCI9IiAqIDc4KTsgaW5uKCJXUDU0MSBnMiAtIHBoZXAgZG8gdHJlbiBXaW5kb3dz',
'IHRoYXQgKHNwZWMgcjM6IE4xLU40LCBOOC1OMTIsIE43LCBraWNoIHRodW9jKSIpOyBpbm4oIj0iICogNzgpCgojIC0tLS0t',
'LS0tLS0tLS0tLS0gdHUga2llbSBibyBkb2MgLS0tLS0tLS0tLS0tLS0tLQpfZCwgX2csIF90ID0gZG9jX2RvKF9NQVUpCl9v',
'ayA9IChsZW4oX2QpID09IDIgYW5kIGFueSh4LnN0YXJ0c3dpdGgoInQwMmIiKSBmb3IgeCBpbiBfZCkKICAgICAgIGFuZCBu',
'b3QgYW55KHguc3RhcnRzd2l0aCgidDEzMSIpIGZvciB4IGluIF9kKSBhbmQgX3QpCmlubigiVHUga2llbSBibyBkb2MgbG9n',
'OiIsIERBVCBpZiBfb2sgZWxzZSBUUlVPVCkKaWYgbm90IF9vazoKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8gRFVPQzog',
'Ym8gZG9jIGxvZyBjdWEgY2hpbmggc2NyaXB0IG5heSBzYWkgLT4ga2hvbmcgZG8gZ2kgY2EuIik7IHN5cy5leGl0KDMpCgoj',
'IC0tLS0tLS0tLS0tLS0tLS0gMC4gbmVuIGRvIC0tLS0tLS0tLS0tLS0tLS0KZ29jID0gUGF0aChzeXMuYXJndlsxXSkucmVz',
'b2x2ZSgpIGlmIGxlbihzeXMuYXJndikgPiAxIGVsc2UgUGF0aC5jd2QoKQp0ZXAsIHRlcHQgPSBnb2MgLyAib3BzIiAvICJs',
'ZWFzZV9wdWJsaXNoLnB5IiwgZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaF90ZXN0LnB5Igppbm4oIiIpOyBpbm4oIi0i',
'ICogNzgpOyBpbm4oIjAuIE5FTiBETyIpCiMgTU9JIExPRyBQSEFJIFRVIEtIQUkgbm8gZG8gQ0FJIEdJIGJhbmcgQk8gRE8g',
'TkFPLiBCYWkgaG9jIDE5LTA5LTIwMjY6IG1vdCBsdW90IGRvCiMgZ3VpIHZlIGR1b2MgZG9jIG5odSBrZXQgcXVhIGN1YSBi',
'YW4gdmEgZGFuZyB4ZXQsIG5odW5nIHRoYXQgcmEgbGEgYmFuIGRvIENVIGNoYXkKIyB0cmVuIG5oYW5oIEtIQUMuIERvYyBy',
'YSB0aGkgbWF0IG1vdCB2b25nOyBsb2cgdHUga2hhaSB0aGkgdGhheSBuZ2F5IGRvbmcgZGF1Lgp0cnk6CiAgICBfdHUgPSBo',
'YXNobGliLnNoYTI1NihQYXRoKF9fZmlsZV9fKS5yZWFkX2J5dGVzKCkpLmhleGRpZ2VzdCgpCmV4Y2VwdCBFeGNlcHRpb24g',
'YXMgX2U6CiAgICBfdHUgPSBmImtob25nIHR1IGJhbSBkdW9jOiB7X2V9IgpnaGkoImJvX2RvX3NoYTI1NiIsIF90dSkKaW5u',
'KGYiICBCTyBETyAgICAgICAgOiBzaGEyNTYge190dVs6MTZdfSAgKGJhbiB7QkFOX0JPX0RPfSkiKQppbm4oIiAgc3lzLnBs',
'YXRmb3JtIDoiLCBzeXMucGxhdGZvcm0sICJ8IHB5dGhvbiIsIHN5cy52ZXJzaW9uLnNwbGl0KClbMF0pCmlubigiICBvcy5w',
'YXRoc2VwICAgOiIsIHJlcHIob3MucGF0aHNlcCksICJ8IFBBVEhFWFQ6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUEFUSEVY',
'VCIpKVs6NjBdKQppbm4oIiAgUHJvZ3JhbUZpbGVzIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJQcm9ncmFtRmlsZXMiKSks',
'ICJ8IFN5c3RlbVJvb3Q6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiU3lzdGVtUm9vdCIpKSkKaW5uKCIgIENPTkdfQ1VfR0lU',
'ICA6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiQ09OR19DVV9HSVQiKSkpCmlubigiICBnb2Mga2hvICAgICAgOiIsIGdvYykK',
'CnF1eWVuID0gTm9uZQppZiBzeXMucGxhdGZvcm0gPT0gIndpbjMyIjoKICAgIHRyeToKICAgICAgICBpbXBvcnQgY3R5cGVz',
'OyBxdXllbiA9IGJvb2woY3R5cGVzLndpbmRsbC5zaGVsbDMyLklzVXNlckFuQWRtaW4oKSkKICAgIGV4Y2VwdCBFeGNlcHRp',
'b246IHF1eWVuID0gTm9uZQpnaGkoInF1eWVuX2FkbWluIiwgcXV5ZW4pCnN5bWxpbmtfZHVvYyA9IE5vbmUKdHJ5OgogICAg',
'd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAgIGQgPSBQYXRoKHQpLyJhLnR4dCI7IGQu',
'd3JpdGVfdGV4dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgdHJ5OiBvcy5zeW1saW5rKHN0cihkKSwgc3RyKFBh',
'dGgodCkvImxrIikpOyBzeW1saW5rX2R1b2MgPSBUcnVlCiAgICAgICAgZXhjZXB0IE9TRXJyb3IgYXMgZTogc3ltbGlua19k',
'dW9jID0gRmFsc2U7IGdoaSgic3ltbGlua19sb2kiLCBmInt0eXBlKGUpLl9fbmFtZV9ffToge2V9IikKZXhjZXB0IEV4Y2Vw',
'dGlvbiBhcyBlOiBnaGkoInN5bWxpbmtfbG9pIiwgc3RyKGUpKQpnaGkoInN5bWxpbmtfZHVvYyIsIHN5bWxpbmtfZHVvYykK',
'aW5uKCIgIEFkbWluaXN0cmF0b3I6IiwgcXV5ZW4sICJ8IHRhbyBzeW1saW5rIGR1b2M6Iiwgc3ltbGlua19kdW9jKQoKbG9p',
'ID0gW10KIyBDb25nIGtpY2ggdGh1b2MgbGEgcGhlcCBkbyB0cmVuIExJQ0ggU1UgR0lULCBraG9uZyBkaW5oIGdpIGRlbiBu',
'ZW4uIENobyBwaGVwCiMgLS1jaGkta2ljaC10aHVvYyBjaGF5IG8gbW9pIG5lbiBkZSBjb24gVFUgS0lFTSBkdW9jIGNoaW5o',
'IGNvbmcgbmF5IChkYSBkdW5nCiMgZGUgdGFpIGR1bmcgY2EgaGFpIHZlIGN1YSBzdSBjbyBuZW4tY3UgMTktMDkpLiBNb2kg',
'Y2hvdCBDSFVDIE5BTkcgdmFuIGRvaSBXaW5kb3dzLgppZiBzeXMucGxhdGZvcm0gIT0gIndpbjMyIiBhbmQgIi0tY2hpLWtp',
'Y2gtdGh1b2MiIG5vdCBpbiBzeXMuYXJndjoKICAgIGxvaS5hcHBlbmQoZiJLSE9ORyBwaGFpIFdpbmRvd3MgKHN5cy5wbGF0',
'Zm9ybT17c3lzLnBsYXRmb3JtIXJ9KSIpCmlmIG5vdCB0ZXAuaXNfZmlsZSgpOiAgbG9pLmFwcGVuZChmImtob25nIHRoYXkg',
'e3RlcH0iKQppZiBub3QgdGVwdC5pc19maWxlKCk6IGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB0fSIpCmlmIG5vdCBz',
'aHV0aWwud2hpY2goImdpdCIpOiBsb2kuYXBwZW5kKCJraG9uZyBjbyBgZ2l0YCB0cm9uZyBQQVRIIikKCnJjLCBoZWFkLCBf',
'ID0gZ2l0KGdvYywgInJldi1wYXJzZSIsICJIRUFEIikKaWYgcmM6IGxvaS5hcHBlbmQoImtob25nIGRvYyBkdW9jIEhFQUQi',
'KQpnaGkoImhlYWQiLCBoZWFkKQpyY19hLCBfLCBfID0gZ2l0KGdvYywgIm1lcmdlLWJhc2UiLCAiLS1pcy1hbmNlc3RvciIs',
'IFNIQV9HMSwgaGVhZCBvciAiSEVBRCIpCmxhX2hhdV9kdWUgPSAocmNfYSA9PSAwKQppZiBoZWFkID09IFNIQV9HMToKICAg',
'IHRoZV9oZSA9ICJnMSI7IGlubihmIiAgSEVBRCA9IHtoZWFkWzo4XX0gLT4gREFZIExBIGcxLiBDSFVBIGNvIGJhbiB2YSBn',
'Mjsga2V0IHF1YSBkdW9pIGxhIE5FTiBETy4iKQplbGlmIGxhX2hhdV9kdWU6CiAgICB0aGVfaGUgPSAiZzIiOyBpbm4oZiIg',
'IEhFQUQgPSB7aGVhZFs6OF19IC0+IGhhdSBkdWUgY3VhIGcxICh7U0hBX0cxWzo4XX0pOiB1bmcgdmllbiBnMi4iKQplbHNl',
'OgogICAgdGhlX2hlID0gIj8iOyBsb2kuYXBwZW5kKGYiSEVBRD17aGVhZFs6OF19IEtIT05HIHBoYWkgZzEgdmEgS0hPTkcg',
'cGhhaSBoYXUgZHVlIGN1YSB7U0hBX0cxWzo4XX0g4oCUIHJlYmFzZT8gbmhhbSBuaGFuaD8iKQpnaGkoInRoZV9oZSIsIHRo',
'ZV9oZSkKcmNfciwgcmVmcywgXyA9IGdpdChnb2MsICJmb3ItZWFjaC1yZWYiLCAiLS1wb2ludHMtYXQiLCBoZWFkIG9yICJI',
'RUFEIiwKICAgICAgICAgICAgICAgICAgICAiLS1mb3JtYXQ9JShyZWZuYW1lOnNob3J0KSIpCmRzciA9IFt4IGZvciB4IGlu',
'IHJlZnMuc3BsaXRsaW5lcygpIGlmIHguc3RyaXAoKSBhbmQgeC5zdHJpcCgpICE9ICJkby10YW0iXQpnaGkoInJlZl90cm9f',
'dG9pX2hlYWQiLCBkc3IpCmlubihmIiAgcmVmIHRybyB0b2kgSEVBRDogeycsICcuam9pbihkc3IpIGlmIGRzciBlbHNlICco',
'a2hvbmcgcmVmIG5hbyAtIEhFQUQgcm9pIHR1IGRvKSd9IikKCmlmIGxvaToKICAgIGlubigiIik7IGlubigiS0hPTkcgRE8g',
'RFVPQzogbmVuIGRvIHNhaSwgS0hPTkcgaW4ga2V0IGx1YW4gbmFvLiIpCiAgICBmb3IgeCBpbiBsb2k6IGlubigiICAtIiwg',
'eCkKICAgIHN5cy5leGl0KDMpCgojIC0tLS0tLS0tLS0tLS0tLS0gMS4ga2ljaCB0aHVvYyAoTjcnIGN1YSBzcGVjIHIzKSAt',
'LS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigiLSIgKiA3OCk7IGlubigiMS4gS0lDSCBUSFVPQyDigJQgdHJhbiBzcGVj',
'IHIzOiA8PSAyIHRlcCB2YSA8PSA0MDAgZG9uZyB0aGVtIikKIyBWRSBORU4gUEhBSSBUVU9JIOKAlCB2YSBwaGFpIENIVU5H',
'IE1JTkggZHVvYyBsYSB0dW9pLCBraG9uZyBwaGFpIGdpYSBkaW5oLgojIEJhaSBob2MgdHJhIGdpYSAxOS0wOS0yMDI2OiBj',
'bG9uZSB0YWkgZHVuZyBjaGkgZmV0Y2ggbmhhbmggYmFuIHZhLCBgb3JpZ2luL21hc3RlcmAKIyBkdW5nIHllbiB0dSAxNC0w',
'OSAoYzE2YmQzMiwgc2F1IDk3IGNvbW1pdCkuIG1lcmdlLWJhc2Ugcm9pIHZlIGR1bmcgZGluaCBtYXN0ZXIgY3UsCiMgbmVu',
'IGRpZmYgTlVPVCBjYSA5NyBjb21taXQgbWFzdGVyOiBkbyByYSA0NiB0ZXAgLyArNzExOCB0aGF5IHZpIDIgdGVwIC8gKzM5',
'NyDigJQKIyBDVU5HIE1PVCBDT01NSVQgMGVhOTVkZS4gTW90IHRpZXUgY2hpIERFTFRBIG1hIHZlIG5lbiBraG9uZyB0dW9p',
'IHRoaSBraG9uZyBzYWkKIyBsZWNoIG1vdCBjaHV0LCBubyBzYWkgY2EgbW90IGJhYyBkbyBsb24uCiMgQ2hvIG5lbjogbmVu',
'IGtob25nIGNodW5nIG1pbmggZHVvYyBsYSB0dW9pID0+IEtIT05HIERPIERVT0MgKHJjPTMpLCBLSE9ORyBwaGFpIFRSVU9U',
'LgojIFRSVU9UIGxhIG1vdCBQSEFOIFFVWUVUIHZlIGJhbiB2YTsgcGhhbiBxdXlldCBjaGkgZHVvYyBwaGVwIHBoYXQgcmEg',
'a2hpIGRhIGRvIGR1b2MuCnJjX2xyLCBvdXRfbHIsIGVyX2xyID0gZ2l0KGdvYywgImxzLXJlbW90ZSIsICJvcmlnaW4iLCAi',
'cmVmcy9oZWFkcy9tYXN0ZXIiKQpyY19sbSwgbG0sIGVyX2xtICAgICA9IGdpdChnb2MsICJyZXYtcGFyc2UiLCAib3JpZ2lu',
'L21hc3RlciIpCnJtID0gb3V0X2xyLnNwbGl0KClbMF0gaWYgKG5vdCByY19sciBhbmQgb3V0X2xyLnN0cmlwKCkpIGVsc2Ug',
'IiIKaWYgbm90IHJtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwKICAgICAgICBmImtob25nIGhvaSBkdW9jIG1h',
'c3RlciB0cmVuIHJlbW90ZSAobHMtcmVtb3RlIHJjPXtyY19scn0pOiB7ZXJfbHJbOjYwXX0gIgogICAgICAgIGYi4oCUIGto',
'b25nIGNodW5nIG1pbmggZHVvYyB2ZSBuZW4gY29uIHR1b2kiKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIs',
'IDEKZWxpZiByY19sbSBvciBub3QgbG06CiAgICBrZXQoIk43JyBraWNoIHRodW9jIiwgS0RELCBmImtob25nIGRvYyBkdW9j',
'IG9yaWdpbi9tYXN0ZXIgdHJvbmcgY2xvbmU6IHtlcl9sbVs6NjBdfSIpCiAgICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIi',
'LCAiIiwgMQplbGlmIGxtICE9IHJtOgogICAgIyBEZW0geGVtIHR1dCBsYWkgYmFvIHhhLCBuZXUgZGVtIGR1b2Mg4oCUIGNv',
'biBzbyBuYXkgbm9pIHJvIG11YyBkbyBzYWkgbGVjaC4KICAgIHJjX2MsIHNhdSwgXyA9IGdpdChnb2MsICJyZXYtbGlzdCIs',
'ICItLWNvdW50IiwgZiJ7bG19Li57cm19IikKICAgIHhhID0gZiIsIHR1dCBsYWkge3NhdX0gY29tbWl0IiBpZiAobm90IHJj',
'X2MgYW5kIHNhdS5zdHJpcCgpLmlzZGlnaXQoKSkgZWxzZSAiIgogICAgaW5uKGYiICBvcmlnaW4vbWFzdGVyIHRyb25nIGNs',
'b25lIDoge2xtWzoxMl19IikKICAgIGlubihmIiAgbWFzdGVyIHRyZW4gcmVtb3RlICAgICAgICA6IHtybVs6MTJdfXt4YX0i',
'KQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAga2V0KCJONycga2lj',
'aCB0aHVvYyIsIEtERCwKICAgICAgICBmInZlIG5lbiBDVTogb3JpZ2luL21hc3Rlcj17bG1bOjEyXX0gIT0gcmVtb3RlPXty',
'bVs6MTJdfXt4YX0gIgogICAgICAgIGYi4oCUIGNoYXkgYGdpdCAtQyA8a2hvPiBmZXRjaCBvcmlnaW4gbWFzdGVyYCByb2kg',
'ZG8gbGFpIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsc2U6CiAgICBpbm4oZiIgIHZlIG5lbiBU',
'VU9JOiBvcmlnaW4vbWFzdGVyID0ge2xtWzoxMl19ID09IG1hc3RlciB0cmVuIHJlbW90ZSIpCiAgICBnaGkoIm1hc3Rlcl9j',
'bG9uZSIsIGxtKTsgZ2hpKCJtYXN0ZXJfcmVtb3RlIiwgcm0pCiAgICByY19tYiwgbWIsIGVyX21iID0gZ2l0KGdvYywgIm1l',
'cmdlLWJhc2UiLCAib3JpZ2luL21hc3RlciIsIGhlYWQpCmlmIHJjX21iIG9yIG5vdCBtYjoKICAgIGlmIG1iID09ICIiIGFu',
'ZCBybSBhbmQgbG0gPT0gcm06CiAgICAgICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyB0aW5oIGR1b2Mg',
'bWVyZ2UtYmFzZSB2b2kgb3JpZ2luL21hc3Rlcjoge2VyX21iWzo3MF19IikKICAgIG5zLCByYyA9ICIiLCAxCmVsc2U6CiAg',
'ICBnaGkoIm1lcmdlX2Jhc2UiLCBtYikKICAgIGlubihmIiAgbWVyZ2UtYmFzZShvcmlnaW4vbWFzdGVyLCBIRUFEKSA9IHtt',
'Yls6MTJdfSIpCiAgICBpZiBtYiAhPSBTSEFfQkFTRV9TUEVDOgogICAgICAgIGlubihmIiAgTFVVIFk6IGtoYWMgYmFzZSBt',
'YSBzcGVjIHIzIGtoYWkgKHtTSEFfQkFTRV9TUEVDWzoxMl19KSDigJQgdmkgbmhhbmggZGEgbWVyZ2UgbWFzdGVyLiIpCiAg',
'ICAgICAgaW5uKGYiICAgICAgICAgRG8gc28gYmFzZSBjdSBzZSBOVU9UIHBoYW4gbWFzdGVyIG1hbmcgdmFvLiBEdW5nIG1l',
'cmdlLWJhc2UgbW9pIGxhIHZpZWMgY3VhIGV4ZWN1dG9yLiIpCiAgICAgICAgcmNfeCwgbnNfeCwgXyA9IGdpdChnb2MsICJk',
'aWZmIiwgIi0tbnVtc3RhdCIsIFNIQV9CQVNFX1NQRUMsIGhlYWQpCiAgICAgICAgaWYgbm90IHJjX3g6CiAgICAgICAgICAg',
'IGggPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBuc194LnNwbGl0bGluZXMoKSBpZiBsLnN0cmlwKCldCiAgICAgICAgICAg',
'IGEgPSBzdW0oaW50KHhbMF0pIGZvciB4IGluIGggaWYgeFswXS5pc2RpZ2l0KCkpCiAgICAgICAgICAgIGdoaSgibnVtc3Rh',
'dF90aGVvX2Jhc2Vfc3BlYyIsIHsidGVwIjogbGVuKGgpLCAidGhlbSI6IGF9KQogICAgICAgICAgICBpbm4oZiIgICAgICAg',
'ICAoZG9pIGNoaWV1OiBzbyBiYXNlIHNwZWMgPSB7bGVuKGgpfSB0ZXAgLyAre2F9IOKAlCBjb24gc28gYXkgS0hPTkcgZHVu',
'ZyBkZSBjaGFtKSIpCiAgICByYywgbnMsIGVyID0gZ2l0KGdvYywgImRpZmYiLCAiLS1udW1zdGF0IiwgbWIsIGhlYWQpCmlm',
'IHJjOgogICAgcGFzcwplbHNlOgogICAgaGFuZyA9IFtsLnNwbGl0KCJcdCIpIGZvciBsIGluIG5zLnNwbGl0bGluZXMoKSBp',
'ZiBsLnN0cmlwKCldCiAgICB0aGVtID0gc3VtKGludChoWzBdKSBmb3IgaCBpbiBoYW5nIGlmIGhbMF0uaXNkaWdpdCgpKQog',
'ICAgeG9hICA9IHN1bShpbnQoaFsxXSkgZm9yIGggaW4gaGFuZyBpZiBoWzFdLmlzZGlnaXQoKSkKICAgIGdoaSgic29fdGVw',
'IiwgbGVuKGhhbmcpKTsgZ2hpKCJkb25nX3RoZW0iLCB0aGVtKTsgZ2hpKCJkb25nX3hvYSIsIHhvYSkKICAgIGZvciBoIGlu',
'IGhhbmc6IGlubihmIiAgICB7aFsyXTozNH0gK3toWzBdOjw1fSAte2hbMV19IikKICAgIGlubihmIiAgICBUT05HOiB7bGVu',
'KGhhbmcpfSB0ZXAsICt7dGhlbX0sIC17eG9hfSAgICh0cmFuOiB7VFJBTl9URVB9IHRlcCAvIHtUUkFOX0RPTkd9IGRvbmcg',
'dGhlbSkiKQogICAga2V0KCJONycga2ljaCB0aHVvYyIsIERBVCBpZiAobGVuKGhhbmcpIDw9IFRSQU5fVEVQIGFuZCB0aGVt',
'IDw9IFRSQU5fRE9ORykgZWxzZSBUUlVPVCwKICAgICAgICBmIntsZW4oaGFuZyl9IHRlcCAvICt7dGhlbX0iKQoKIyBDb25n',
'IG5oYW5oOiBkbyBSSUVORyBraWNoIHRodW9jICh2YWkgZ2lheSkgcm9pIGR1bmcuIER1bmcga2hpIGNhbiB4YWMgbWluaCBs',
'YWkKIyB2ZSBuZW4gbWEga2hvbmcgbXVvbiB0cmEgMjAtNDUgcGh1dCBjaG8gY2EgYm8gdGVzdC4KaWYgIi0tY2hpLWtpY2gt',
'dGh1b2MiIGluIHN5cy5hcmd2OgogICAgaW5uKCIiKTsgaW5uKCI9IiAqIDc4KQogICAgaW5uKCItLWNoaS1raWNoLXRodW9j',
'OiBDSEkgZG8gY29uZyBraWNoIHRodW9jLiBEYXkgS0hPTkcgcGhhaSBtb3QgbHVvdCBuZ2hpZW0gdGh1LiIpCiAgICBpbm4o',
'Ii0iICogNzgpCiAgICBmb3IgX3QsIF90dCwgX2N0IGluIGNob3Q6IGlubihmIiAge190dDoxNH0ge190fSIgKyAoZiIgICB7',
'X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgX2sgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gS0REKQog',
'ICAgX3IgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlmIHQgPT0gVFJVT1QpCiAgICBzeXMuZXhpdCgzIGlmIF9rIGVs',
'c2UgKDEgaWYgX3IgZWxzZSAwKSkKCkNISV9QUk9CRSA9ICItLWNoaS1wcm9iZSIgaW4gc3lzLmFyZ3YgICAgIyBibyBxdWEg',
'Ym8gdGVzdCArIE43OyBnaXUgMCwgMSwgMwojIC0tLS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVzdCBkYXkgZHUgLS0tLS0tLS0t',
'LS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIyLiBCTyBURVNUIERB',
'WSBEVSAoMTAtNDAgcGh1dCkiKQogICAgcmNfbiwgb3V0X24gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hfdGVzdC5weSJd',
'LCBnb2MpCiAgICBnaGkoInJjX3N1aXRlIiwgcmNfbikKICAgIG0gPSBSWF9UT05HLnNlYXJjaChvdXRfbikKICAgIGlubigi',
'ICByYyA9IiwgcmNfbiwgInwiLCBtLmdyb3VwKDApIGlmIG0gZWxzZSAiKEtIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQp',
'IikKICAgIGlmIG06CiAgICAgICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGkoInRyZW4iLCBpbnQobS5ncm91',
'cCgyKSkpOyBnaGkoImJvX3F1YV9zbyIsIGludChtLmdyb3VwKDQpKSkKICAgIGRvX2hldCwgZ2MsIHRpbiA9IGRvY19kbyhv',
'dXRfbikKICAgIGdoaSgic29fY2FfZG8iLCBsZW4oZG9faGV0KSk7IGdoaSgibGlldF9rZV9kYXlfZHUiLCB0aW4pCiAgICBm',
'b3IgZyBpbiBnYzogaW5uKCIgICAqIiwgZykKICAgIGlubigiIik7IGlubihmIiAgPT09IHtsZW4oZG9faGV0KX0gQ0EgRE8g',
'PT09IikKICAgIGZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaW5uKGYiICAge3Quc3BsaXQo',
'J18nKVswXTo3fSB7dH0iKTsgaW5uKGYiICAgICAgICAgICB7ZG9faGV0W3RdWzoxNTBdfSIpCiAgICBnaGkoImRvX2x5X2Rv',
'Iiwge3Q6IGRvX2hldFt0XVs6MzAwXSBmb3IgdCBpbiBkb19oZXR9KQogICAgIyAtLS0tIENIT1Q6IG1vaSBjYSBETyBwaGFp',
'IEdJQUkgVEhJQ0ggRFVPQyAtLS0tCiAgICAjIFRoaWV1IGNob3QgbmF5LCBibyBkbyBpbiBkYW5oIHNhY2ggZG8gcm9pIHZh',
'biB0aG9hdCByYz0wLiBEbyBkdW5nIGxhIGxvaSBkYSB4YXkgcmE6CiAgICAjIGx1b3QgV2luZG93cyAxOS0wOSBjbyB0MTcx',
'IERPIG1hIGJvIGRvIGJhbyAiREFUIDEwIHwgVFJVT1QgMCIgdmEgcmM9MC4KICAgIGRlZiBfa2hvYSh0KTogcmV0dXJuIHQu',
'c3BsaXQoIl8iKVswXQogICAgZG9fcGFja2V0LCBkb19sYSwgZG9fdGhpZXVfY29uZ19jdSA9IFtdLCBbXSwgW10KICAgIGZv',
'ciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICAgICAgaywgbHkgPSBfa2hvYSh0KSwgZG9faGV0W3RdCiAg',
'ICAgICAgaWYgayBpbiBDQV9QQUNLRVQ6ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fcGFja2V0LmFwcGVuZCh0',
'KQogICAgICAgIGVsaWYgIktIw5RORyDEkE8gxJDGr+G7okMiIGluIGx5IG9yICJ0aGnhur91IGAiIGluIGx5OiAgZG9fdGhp',
'ZXVfY29uZ19jdS5hcHBlbmQodCkKICAgICAgICBlbGlmIGsgaW4gTkdPQUlfUEhBTV9WSTogICAgICAgICAgICAgICAgICAg',
'ICAgICBwYXNzCiAgICAgICAgZWxzZTogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZG9fbGEu',
'YXBwZW5kKHQpCiAgICBnaGkoImRvX3BhY2tldCIsIGRvX3BhY2tldCk7IGdoaSgiZG9fbGEiLCBkb19sYSk7IGdoaSgiZG9f',
'dGhpZXVfY29uZ19jdSIsIGRvX3RoaWV1X2NvbmdfY3UpCiAgICBpbm4oIiIpCiAgICBpbm4oZiIgIGNhIERPIHRodW9jIENI',
'SU5IIHBhY2tldCBuYXkgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF0gb3IgJ2tob25nIGNvJ30iKQogICAgaW5u',
'KGYiICBjYSBETyBuZ29haSBwaGFtIHZpIChyMyBraGFpKToge1tfa2hvYSh4KSBmb3IgeCBpbiBzb3J0ZWQoZG9faGV0LCBr',
'ZXk9c29fY2EpIGlmIF9raG9hKHgpIGluIE5HT0FJX1BIQU1fVkldfSIpCiAgICBpbm4oZiIgIGNhIERPIHZpIFRISUVVIENP',
'TkcgQ1UgICAgICAgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9yICdraG9uZyBjbyd9IikKICAg',
'IGlubihmIiAgY2EgRE8gTEEgKGtob25nIGdpYWkgdGhpY2ggZHVvYyk6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdIG9y',
'ICdraG9uZyBjbyd9IikKICAgIGtldCgiS2hvbmcgY2EgbmFvIGN1YSBQQUNLRVQgYmkgRE8iLCBEQVQgaWYgbm90IGRvX3Bh',
'Y2tldCBlbHNlIFRSVU9ULAogICAgICAgICIiIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBmIkRPOiB7W19raG9hKHgpIGZvciB4',
'IGluIGRvX3BhY2tldF19IOKAlCBiYW4gdmEgQ0hVQSB4b25nIikKICAgIGtldCgiTW9pIGNhIERPIGRldSBnaWFpIHRoaWNo',
'IGR1b2MiLCBEQVQgaWYgbm90IGRvX2xhIGVsc2UgVFJVT1QsCiAgICAgICAgIiIgaWYgbm90IGRvX2xhIGVsc2UgZiJsYTog',
'e1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV19IikKICAgIGlmIGRvX3RoaWV1X2NvbmdfY3U6CiAgICAgICAga2V0KCJDb25n',
'IGN1IGRheSBkdSBkZSBkbyIsIEtERCwgZiJ0aGlldSBjb25nIGN1IGNobyB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1',
'X2NvbmdfY3VdfSIpCgogICAgYnEgPSBzb3J0ZWQoe3QgZm9yIHQsIF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwob3V0X24pfSwg',
'a2V5PXNvX2NhKTsgZ2hpKCJjYV9ib19xdWEiLCBicSkKICAgIGlubigiIik7IGlubihmIiAgQk8gUVVBICh7bGVuKGJxKX0p',
'OiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCiAgICBpbm4oIiIpOyBpbm4oIiAgTjEtTjQgKHQxNjUtdDE2',
'OCksIHRpZXUgY2hpIG5naGllbSB0aHUgY3VhIHIyLCBuYXkgbGEgY2hpIGJhbyBob2kgcXV5OiIpCiAgICBiNCA9IHt0OiBt',
'YXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBTU9JfTsgZ2hpKCJjYV9tb2kiLCBiNCkKICAgIGZvciB0IGluIENBTU9JOiBp',
'bm4oZiIgICAgIHt0fToge2I0W3RdfSIpCiAgICBrZXQoIk4xLU40ICh0MTY1LXQxNjgpIiwgREFUIGlmIGFsbCh2ID09ICJR',
'VUEiIGZvciB2IGluIGI0LnZhbHVlcygpKQogICAgICAgIGVsc2UgKEtERCBpZiBhbnkodiBpcyBOb25lIGZvciB2IGluIGI0',
'LnZhbHVlcygpKSBlbHNlIFRSVU9UKSwgc3RyKGI0KSkKCiAgICBpbm4oIiIpOyBpbm4oIiAgMTUgY2EgdHVuZyBkbyB0cmVu',
'IENJOiIpCiAgICBiMTUgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQTE1fTsgZ2hpKCJjYTE1IiwgYjE1KQog',
'ICAgaW5uKCIgICAgIiArICIgICIuam9pbihmInt0fTp7YjE1W3RdfSIgZm9yIHQgaW4gQ0ExNSkpCgogICAgIyB0MTM2IOKA',
'lCBOMTIgZG8gR0lBTiBUSUVQIHF1YSBrZXQgcXVhIGNhCiAgICB0MTM2X3RlbiA9IG5leHQoKHQgZm9yIHQgaW4gZG9faGV0',
'IGlmIHQuc3RhcnRzd2l0aCgidDEzNiIpKSwgTm9uZSkKICAgIGlmIGIxNS5nZXQoInQxMzYiKSA9PSAiUVVBIjoKICAgICAg',
'ICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBEQVQsICJ0MTM2IFFVQSIpCiAgICBlbGlmIGIxNS5nZXQoInQx',
'MzYiKSBpcyBOb25lOgogICAgICAgIGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIEtERCwgImtob25nIHRoYXkg',
'dDEzNiB0cm9uZyBsb2ciKQogICAgZWxzZToKICAgICAgICBseSA9IGRvX2hldC5nZXQodDEzNl90ZW4sICIiKQogICAgICAg',
'IGtldCgiTjEyIHQxMzYgKHF1YSBrZXQgcXVhIGNhKSIsIFRSVU9ULCBmIkRPOiB7bHlbOjkwXX0iKQoKIyAtLS0tLS0tLS0t',
'LS0tLS0tIDMuIHByb2JlIFRIQU5HIHZhbyBoYW0gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBp',
'bm4oIjMuIFBST0JFIFRIQU5HIOKAlCBnb2kgX2dpdF93aW5kb3dzIHZvaSB0aGFtIHNvIHRpZW0iKQpzcGVjID0gaW1wb3J0',
'bGliLnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwNTQxIiwgc3RyKHRlcCkpCmxwID0gaW1wb3J0bGliLnV0aWwu',
'bW9kdWxlX2Zyb21fc3BlYyhzcGVjKTsgc3BlYy5sb2FkZXIuZXhlY19tb2R1bGUobHApCnNpZyA9IGluc3BlY3Quc2lnbmF0',
'dXJlKGxwLl9naXRfd2luZG93cykKZ2hpKCJ0aGFtX3NvX19naXRfd2luZG93cyIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQpp',
'bm4oIiAgdGhhbSBzbyBjdWEgX2dpdF93aW5kb3dzOiIsIGxpc3Qoc2lnLnBhcmFtZXRlcnMpKQoKZGVmIGdvaSgqKmt3KToK',
'ICAgICIiIkdvaSBfZ2l0X3dpbmRvd3MsIEJBVCBzdGRlcnIgZGUgbW90IGRvbmcgY2hhbiBkb2FuIGtob25nIGdpZXQgbHVv',
'dCBkby4iIiIKICAgIGUgPSBpby5TdHJpbmdJTygpCiAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgog',
'ICAgICAgIHIgPSBscC5fZ2l0X3dpbmRvd3MoKiprdykKICAgIHJldHVybiByLCBlLmdldHZhbHVlKCkKCiMgLS0tIGRvaSBj',
'aHVuZyByaWc6IHBoYWkgdHJhIGxvaSBkdW5nIG1vdCBjYSB0YSBCSUVUIFRSVU9DIGRhcCBhbiAtLS0Kd2l0aCB0ZW1wZmls',
'ZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgbmdvYWkgPSBQYXRoKHQpLyJuZ29haSI7IG5nb2FpLm1rZGlyKCk7',
'IGN3ID0gUGF0aCh0KS8iY3dkIjsgY3cubWtkaXIoKTsgcGYgPSBQYXRoKHQpLyJwZiI7IHBmLm1rZGlyKCkKICAgIChuZ29h',
'aS8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjEsIF8gPSBnb2kocGF0aD1zdHIo',
'bmdvYWkpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQogICAgKGN3LyJnaXQuZXhlIikud3JpdGVfdGV4',
'dCgieCIsIGVuY29kaW5nPSJ1dGYtOCIpCiAgICByMiwgXyA9IGdvaShwYXRoPXN0cihjdyksIHByb2dyYW1fZmlsZXM9c3Ry',
'KHBmKSwgY3dkPXN0cihjdykpCnJpZ19vayA9IGJvb2wocjEpIGFuZCByMiBpcyBOb25lCmdoaSgicmlnX2RvaV9jaHVuZyIs',
'IHJpZ19vaykKa2V0KCJSSUcgZG9pIGNodW5nIChiaWV0IHRydW9jIGRhcCBhbikiLCBEQVQgaWYgcmlnX29rIGVsc2UgS0RE',
'LAogICAgZiJuZ29haS1jd2QtPnsnTkhBTicgaWYgcjEgZWxzZSAnTm9uZSd9IHwgdHJvbmctY3dkLT57J05IQU4nIGlmIHIy',
'IGVsc2UgJ05vbmUnfSIpCmlmIG5vdCByaWdfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IHJpZyBzYWks',
'IG1vaSBjaG90IGR1b2kgc2Ugdm8gbmdoaWEuIik7IHN5cy5leGl0KDMpCgojIC0tLSBNT0kgQ09ORyBQSEFJIFRVIENIVU5H',
'IE1JTkggTk8gQ08gVEhFIERPIC0tLQojIEJhaSBob2MgZGF0IG5oYXQgY3VhIHBhY2tldCBuYXk6IGRvX24xMCBiYW4gY3Ug',
'Y2hhbSBEQVQgY2hvIDk1ODMxNjg1IHRyb25nIGtoaSB0MTcxCiMgY3VhIGNoaW5oIGJhbiB2YSBheSBETyB2aSBkdW5nIGto',
'dXlldCB0YXQgbWEgTjEwIHNpbmggcmEgZGUgYmF0LiBObyBkZWdlbmVyYXRlIOKAlAojIHRyZW4gV2luZG93cyBvcy5wYXRo',
'c2VwIERBIGxhICc7JyBuZW4gInRhY2ggZHVuZyIgdmEgInRhY2ggc2FpIiBjaG8gY3VuZyBrZXQgcXVhLgojIE1vdCBjb25n',
'IGtob25nIHRoZSBETyB0aGkga2hvbmcgcGhhaSBjb25nLCB2YSBubyBuZ3V5IGhpZW0gaG9uIGtob25nIGNvIGNvbmc6IG5v',
'CiMgcGhhdCByYSBtb3QgY2h1IERBVC4KIwojIE5lbiB0cnVvYyBraGkgRFVORyBuYW0gY29uZyBuYXkgZGUgcGhhbiBxdXll',
'dCwgYmF0IHR1bmcgY29uZyBnaWV0IG1vdCBkb3QgYmllbiBkYQojIGJpZXQgdHJvbmcuIENvbmcgbmFvIGtob25nIGdpZXQg',
'ZHVvYyB0aGkga2V0IHF1YSB0aGF0IGN1YSBubyBiaSBIQSB4dW9uZyBLSE9ORyBETwojIERVT0Mg4oCUIGtob25nIGNobyBu',
'byBub2kgREFUIG51YS4gRG90IGJpZW4gY2hheSB0cmVuIEJBTiBTQU8gVEFNOyBjYXkgdGhhdCBraG9uZyBiaQojIGR1bmcg',
'dG9pIChjdW5nIGt5IGx1YXQgbmh1IE43KS4KRE9UX0JJRU5fVFVfS0lFTSA9IFsKICAgICgiTjgiLCAib3BzL2xlYXNlX3B1',
'Ymxpc2gucHkiLAogICAgICdpZiBjaGlfZGluaCBhbmQgUGF0aChjaGlfZGluaCkubmFtZS5sb3dlcigpID09ICJnaXQuZXhl',
'IiBhbmQgaG9wX2xlKGNoaV9kaW5oKTonLAogICAgICJpZiBjaGlfZGluaCBhbmQgaG9wX2xlKGNoaV9kaW5oKToiKSwKICAg',
'ICgiTjkiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJkID0gZF9yYXcuc3RyaXAoKS5zdHJpcCgnXCInKSIsICJk',
'ID0gZF9yYXcuc3RyaXAoKSIpLAogICAgKCJOMTAiLCAib3BzL2xlYXNlX3B1Ymxpc2gucHkiLAogICAgICJzZXAgPSBvcy5w',
'YXRoc2VwIGlmIHBoYW5fY2FjaCBpcyBOb25lIGVsc2UgcGhhbl9jYWNoIiwgInNlcCA9IG9zLnBhdGhzZXAiKSwKICAgICgi',
'TjExIiwgIm9wcy9sZWFzZV9wdWJsaXNoLnB5IiwgImlmIGNoYW5fZG9hbiBpcyBub3QgTm9uZToiLCAiaWYgRmFsc2U6Iiks',
'CiAgICAoIk4xMiIsICJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5IiwKICAgICAnZ2l0X3BhdGg9Ii8va2hvbmctY28vZ2l0',
'IicsICdnaXRfcGF0aD0iL2tob25nLWNvL2dpdCInKSwKXQppbm4oIiIpOyBpbm4oIiAgdHUga2llbSBjb25nIOKAlCBtb2kg',
'Y29uZyBwaGFpIGdpZXQgZHVvYyBtb3QgZG90IGJpZW4gZGEgYmlldDoiKQpnaWV0ID0ge30KZm9yIG1hLCBkdW9uZywgdGlt',
'LCB0aGF5IGluIERPVF9CSUVOX1RVX0tJRU06CiAgICBfdGVuLCBfaGFtID0gbmV4dCgoKGEsIGIpIGZvciBhLCBiIGluIFBS',
'T0JFIGlmIGEuc3RhcnRzd2l0aChtYSArICIgIikpLCAoTm9uZSwgTm9uZSkpCiAgICBpZiBfaGFtIGlzIE5vbmU6CiAgICAg',
'ICAgZ2lldFttYV0gPSBOb25lOyBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IGtob25nIHRpbSB0aGF5IHByb2Jl',
'IHRlbiAne21hfSAuLi4nIik7IGNvbnRpbnVlCiAgICB0cnk6CiAgICAgICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJl',
'Y3RvcnkoKSBhcyBfdDoKICAgICAgICAgICAgX2MgPSBQYXRoKF90KS8iY2F5Ijsgc2h1dGlsLmNvcHl0cmVlKGdvYy8ib3Bz',
'IiwgX2MvIm9wcyIpCiAgICAgICAgICAgIF9mID0gX2MvZHVvbmc7IF9uZCA9IF9mLnJlYWRfdGV4dChlbmNvZGluZz0idXRm',
'LTgiKQogICAgICAgICAgICBpZiBfbmQuY291bnQodGltKSAhPSAxOgogICAgICAgICAgICAgICAgZ2lldFttYV0gPSBOb25l',
'CiAgICAgICAgICAgICAgICBpbm4oZiIgICAge21hOjR9IEtIT05HIERPIERVT0M6IG1hdSBkb3QgYmllbiBraG9wIHtfbmQu',
'Y291bnQodGltKX0gbGFuIChtb25nIDEpIgogICAgICAgICAgICAgICAgICAgIGYiIOKAlCBtYSBuZ3VvbiBkYSBkb2ksIGRv',
'dCBiaWVuIG5heSBoZXQgeSBuZ2hpYSIpOyBjb250aW51ZQogICAgICAgICAgICBfZi53cml0ZV90ZXh0KF9uZC5yZXBsYWNl',
'KHRpbSwgdGhheSwgMSksIGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgICAgIF9zcCA9IGltcG9ydGxpYi51dGlsLnNwZWNf',
'ZnJvbV9maWxlX2xvY2F0aW9uKCJscF9kYl8iICsgbWEsIHN0cihfYy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQogICAg',
'ICAgICAgICBfbSA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoX3NwKTsgX3NwLmxvYWRlci5leGVjX21vZHVs',
'ZShfbSkKICAgICAgICAgICAgZGVmIF9nb2lfZGIoKiprdyk6CiAgICAgICAgICAgICAgICBfZSA9IGlvLlN0cmluZ0lPKCkK',
'ICAgICAgICAgICAgICAgIHdpdGggY29udGV4dGxpYi5yZWRpcmVjdF9zdGRlcnIoX2UpOgogICAgICAgICAgICAgICAgICAg',
'IHJldHVybiBfbS5fZ2l0X3dpbmRvd3MoKiprdyksIF9lLmdldHZhbHVlKCkKICAgICAgICAgICAgX3R0LCBfY3QsIF8gPSBf',
'aGFtKF9nb2lfZGIsIGluc3BlY3Quc2lnbmF0dXJlKF9tLl9naXRfd2luZG93cyksCiAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICAgICBfYy8ib3BzIi8ibGVhc2VfcHVibGlzaF90ZXN0LnB5IikKICAgICAgICBnaWV0W21hXSA9IChfdHQgPT0gVFJV',
'T1QpCiAgICAgICAgaW5uKGYiICAgIHttYTo0fSBkb3QgYmllbiAtPiB7X3R0OjE0fSB7J0dJRVQgRFVPQycgaWYgX3R0ID09',
'IFRSVU9UIGVsc2UgJ1NPTkcgU09UJ30iCiAgICAgICAgICAgICsgKGYiICAgKHtfY3R9KSIgaWYgX2N0IGVsc2UgIiIpKQog',
'ICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBfZToKICAgICAgICBnaWV0W21hXSA9IE5vbmU7IGlubihmIiAgICB7bWE6NH0gS0hP',
'TkcgRE8gRFVPQzoge3R5cGUoX2UpLl9fbmFtZV9ffToge19lfSIpCmdoaSgiY29uZ19naWV0X2R1b2NfZG90X2JpZW4iLCBn',
'aWV0KQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwpIGluIFsodCwgZihnb2ksIHNpZywgdGVwdCkpIGZvciB0LCBmIGluIFBST0JF',
'XToKICAgIGdoaSgicHJvYmVfIiArIHRlbi5zcGxpdCgpWzBdLmxvd2VyKCksIGRsKQogICAgaWYgaXNpbnN0YW5jZShkbCwg',
'ZGljdCk6CiAgICAgICAgZm9yIGssIHYgaW4gZGwuaXRlbXMoKTogaW5uKGYiICAgIHtrOjM0fToge3Z9IikKICAgIG1hID0g',
'dGVuLnNwbGl0KClbMF0KICAgIGlmIGdpZXQuZ2V0KG1hKSBpcyBub3QgVHJ1ZSBhbmQgdHQgPT0gREFUOgogICAgICAgICMg',
'REFUIHR1IG1vdCBjb25nIGNodWEgY2h1bmcgbWluaCBkdW9jIGxhIGJpZXQgRE8gdGhpIGtob25nIGRhbmcgdGluIGhvbiBL',
'REQuCiAgICAgICAga2V0KHRlbiwgS0RELCBmImNvbmcgS0hPTkcgZ2lldCBkdW9jIGRvdCBiaWVuIGN1YSBjaGluaCBubyAo',
'e2dpZXQuZ2V0KG1hKSFyfSkiCiAgICAgICAgICAgICAgICAgICAgICBmIiAtPiBjaHUgREFUIG5heSBraG9uZyBjbyBnaWEg',
'dHJpIikKICAgIGVsc2U6CiAgICAgICAga2V0KHRlbiwgdHQsIGN0KQoKIyAtLS0tLS0tLS0tLS0tLS0tIDQuIE43IGRvdCBi',
'aWVuIHRyZW4gQkFOIFNBTyBUQU0gLS0tLS0tLS0tLS0tLS0tLQppZiBub3QgQ0hJX1BST0JFOgogICAgaW5uKCIiKTsgaW5u',
'KCItIiAqIDc4KTsgaW5uKCI0LiBONyDigJQgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAoY2F5IHRoYXQgS0hPTkcgYmkg',
'ZHVuZyB0b2kpIikKICAgIHRydW9jID0gdGVwLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5jb3VudChNQVVfV0lOKQog',
'ICAgZ2hpKCJuN190cnVvYyIsIHRydW9jKTsgaW5uKGYiICBzbyBkb25nIGtob3Age01BVV9XSU4hcn06IFRSVU9DID0ge3Ry',
'dW9jfSBbbW9uZyAxXSIpCiAgICBpZiB0cnVvYyAhPSAxOgogICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93',
'cyIsIEtERCwgZiJtYXUgeHVhdCBoaWVuIHt0cnVvY30gbGFuLCBraG9uZyBwaGFpIDEiKQogICAgZWxzZToKICAgICAgICB3',
'aXRoIHRlbXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHRtcDoKICAgICAgICAgICAgc2FvID0gUGF0aCh0bXApLyJj',
'YXkiCiAgICAgICAgICAgIHNodXRpbC5jb3B5dHJlZShnb2MsIHNhbywgaWdub3JlPXNodXRpbC5pZ25vcmVfcGF0dGVybnMo',
'Ii5naXQiLCAiX19weWNhY2hlX18iLCAiKi5weWMiKSkKICAgICAgICAgICAgZjIgPSBzYW8vIm9wcyIvImxlYXNlX3B1Ymxp',
'c2gucHkiCiAgICAgICAgICAgIGYyLndyaXRlX3RleHQoZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLnJlcGxhY2Uo',
'TUFVX1dJTiwgImlmIEZhbHNlOiIpLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgICAgICBzYXUgPSBmMi5yZWFkX3RleHQo',
'ZW5jb2Rpbmc9InV0Zi04IikuY291bnQoTUFVX1dJTik7IGdoaSgibjdfc2F1Iiwgc2F1KQogICAgICAgICAgICBpbm4oZiIg',
'IFNBVSAoZGEgZG90IGJpZW4pID0ge3NhdX0gW21vbmcgMF0iKQogICAgICAgICAgICBpZiBzYXUgIT0gMDoKICAgICAgICAg',
'ICAgICAgIGtldCgiTjcgZG90IGJpZW4gbmhhbmggV2luZG93cyIsIEtERCwgImRvdCBiaWVuIEtIT05HIGFwIGR1b2MiKQog',
'ICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgcmNfbSwgb3V0X20gPSBjaGF5KFsib3BzL2xlYXNlX3B1Ymxpc2hf',
'dGVzdC5weSJdLCBzYW8pCiAgICAgICAgICAgICAgICBtMTY1ID0gbWF1X2NhKG91dF9tLCAidDE2NSIpOyBkbSwgXywgXyA9',
'IGRvY19kbyhvdXRfbSkKICAgICAgICAgICAgICAgIHRlbjE2NSA9IG5leHQoKHQgZm9yIHQgaW4gZG0gaWYgdC5zdGFydHN3',
'aXRoKCJ0MTY1IikpLCBOb25lKQogICAgICAgICAgICAgICAgbHkgPSAoZG0uZ2V0KHRlbjE2NSkgb3IgIiIpCiAgICAgICAg',
'ICAgICAgICBnaGkoIm43X3QxNjUiLCBtMTY1KTsgZ2hpKCJuN19seV9kbyIsIGx5WzoyMDBdKQogICAgICAgICAgICAgICAg',
'aW5uKGYiICB0MTY1IHNhdSBkb3QgYmllbjoge20xNjV9IHwge2x5WzoxMTBdfSIpCiAgICAgICAgICAgICAgICBkdW5nX2x5',
'X2RvID0gIlBBVEggdCIgaW4gbHkgb3IgIi91c3IvYmluIiBpbiBseQogICAgICAgICAgICAgICAga2V0KCJONyBkb3QgYmll',
'biBuaGFuaCBXaW5kb3dzIiwgREFUIGlmIChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pIGVsc2UKICAgICAgICAgICAg',
'ICAgICAgICAoVFJVT1QgaWYgbTE2NSA9PSAiRE8iIGVsc2UgS0REKSwKICAgICAgICAgICAgICAgICAgICAiZ2lldCBkdW5n',
'IGx5IGRvIiBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKQogICAgICAgICAgICAgICAgICAgIGVsc2UgKCJETyBu',
'aHVuZyBLSE9ORyBkdW5nIGx5IGRvIC0+IHRpbiBkdW5nIGdpYSIgaWYgbTE2NSA9PSAiRE8iIGVsc2UgImtob25nIGRvYyBk',
'dW9jIHQxNjUiKSkKCiMgLS0tLS0tLS0tLS0tLS0tLSBLRVQgTFVBTiAtLS0tLS0tLS0tLS0tLS0tCmlubigiIik7IGlubigi',
'PSIgKiA3OCkKaW5uKGYiVEhFIEhFIERPIERVT0M6IHt0aGVfaGV9ICAgSEVBRD17aGVhZFs6MTJdfSIpCmlmIHRoZV9oZSA9',
'PSAiZzEiOgogICAgaW5uKCJMVVUgWTogZGF5IGxhIE5FTiBETyAoZzEpLCBLSE9ORyBwaGFpIG5naGllbSB0aHUgZzIuIENh',
'YyBjaG90IE44LU4xMiBkdW9pIGRheSIpCiAgICBpbm4oIiAgICAgICBUUlVPVCBsYSBEVU5HIE5IVSBNT05HIOKAlCBjaHVu',
'ZyBsYSBuaHVuZyBsbyBnMiBzaW5oIHJhIGRlIHbDoS4iKQppbm4oIi0iICogNzgpCmZvciB0ZW4sIHR0LCBjdCBpbiBjaG90',
'OgogICAgaW5uKGYiICB7dHQ6MTR9IHt0ZW59IiArIChmIiAgIHtjdH0iIGlmIGN0IGVsc2UgIiIpKQpuX2tkZCA9IHN1bSgx',
'IGZvciBfLCB0LCBfIGluIGNob3QgaWYgdCA9PSBLREQpCm5fdHJ1b3QgPSBzdW0oMSBmb3IgXywgdCwgXyBpbiBjaG90IGlm',
'IHQgPT0gVFJVT1QpCmlubigiLSIgKiA3OCkKaW5uKGYiICBEQVQge3N1bSgxIGZvciBfLHQsXyBpbiBjaG90IGlmIHQ9PURB',
'VCl9IHwgVFJVT1Qge25fdHJ1b3R9IHwgS0hPTkcgRE8gRFVPQyB7bl9rZGR9IikKaW5uKGYiICBUb25nIGNhIGRvOiB7c28u',
'Z2V0KCdzb19jYV9kbycpfSB8IGRhbmggc2FjaCBkYXkgZHU6IHsnQ08nIGlmIHNvLmdldCgnbGlldF9rZV9kYXlfZHUnKSBl',
'bHNlICdLSE9ORyBETyBEVU9DJ30iKQppbm4oZiIgIEFkbWluaXN0cmF0b3I6IHtzby5nZXQoJ3F1eWVuX2FkbWluJyl9IHwg',
'c3ltbGluazoge3NvLmdldCgnc3ltbGlua19kdW9jJyl9IikKaW5uKCIiKTsgaW5uKCItLS0gREFOIE5HVVlFTiBLSE9JIEpT',
'T04gTkFZIFZFIENITyBSRVZJRVdFUiAtLS0iKQpnaGkoImNob3QiLCBbeyJ0ZW4iOiBhLCAidHJhbmdfdGhhaSI6IGIsICJj',
'aGlfdGlldCI6IGN9IGZvciBhLCBiLCBjIGluIGNob3RdKQppbm4oanNvbi5kdW1wcyhzbywgZW5zdXJlX2FzY2lpPUZhbHNl',
'LCBpbmRlbnQ9MSwgZGVmYXVsdD1zdHIpKQojIHJjOiAwID0gbW9pIGNob3QgREFUIHwgMSA9IGNvIGNob3QgVFJVT1QgfCAz',
'ID0gY28gY2hvdCBLSE9ORyBETyBEVU9DICh1dSB0aWVuIGJhbyBkb25nKQpzeXMuZXhpdCgzIGlmIG5fa2RkIGVsc2UgKDEg',
'aWYgbl90cnVvdCBlbHNlIDApKQo='
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
# In lai phan ket luan: tu dong ke ca do dau tien tro di. Khong tim thay thi in ca log.
$dong = @(Get-Content -LiteralPath $Log -Encoding UTF8)
$i = -1
for ($k = 0; $k -lt $dong.Count; $k++) {
    if ($dong[$k] -match 'CA DO doc duoc|KHONG_DO_DUOC|doi chieu bo doc') { $i = $k; break }
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
