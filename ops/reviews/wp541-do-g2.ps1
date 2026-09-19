# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong, khong can gi khac):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1"
#
# Do RIENG cong kich thuoc (vai giay, khong chay bo test 20-45 phut):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-do-g2.ps1" -ChiKichThuoc
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
$ShaBoDo    = 'fa4c557df710ef81a30caafb8f7e9c2d5e07adfc3547a69883118917275049b3'      # SHA-256 cua bo do Python nhung ben duoi

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
'Qk9fRE8gPSAiMjAyNi0wOS0xOWQiICAgICAgICAgICAgICAjIGRvaSBNT0kga2hpIHN1YSBibyBkbyAtIGxvZyB0dSBraGFp',
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
'a3EKCmRlZiBkb19uMTAoZ29pLCBzaWcsIHRlcHQpOgogICAgIiIiTW90IGRhdSAnOycgdHJvbmcgVEVOIHRodSBtdWMga2hv',
'bmcgZHVvYyBsYW0gbWF0IG11YyBnaXQuZXhlIGhvcCBsZSBvIG11YyBraWEuIiIiCiAgICBjb19zZXAgPSBhbnkoKCJjYWNo',
'IiBpbiBrKSBvciAoInNlcCIgaW4gay5sb3dlcigpKSBmb3IgayBpbiBzaWcucGFyYW1ldGVycykKICAgIGlmIG9zLnBhdGhz',
'ZXAgPT0gIjsiIGFuZCBub3QgY29fc2VwOgogICAgICAgIHJldHVybiAoS0RELCAidHJlbiBXaW5kb3dzIG9zLnBhdGhzZXAg',
'REEgbGEgJzsnIHZhIGhhbSBraG9uZyBuaGFuIHRoYW0gc28gZGF1IHBoYW4gY2FjaCAiCiAgICAgICAgICAgICAgICAgICAg',
'ICItPiBraG9uZyB0YWNoIGR1b2MgaGFpIGdpYSB0aHV5ZXQiLCB7Im9zLnBhdGhzZXAiOiBvcy5wYXRoc2VwLCAiY28gdGhh',
'bSBzbyBzZXAiOiBjb19zZXB9KQogICAgd2l0aCB0ZW1wZmlsZS5UZW1wb3JhcnlEaXJlY3RvcnkoKSBhcyB0OgogICAgICAg',
'IGxhID0gUGF0aCh0KS8iY287ZGF1IjsgbGEubWtkaXIoKQogICAgICAgIGQsIGN3LCBwZiA9IF9zYW4odCkKICAgICAgICAo',
'ZC8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHIsIF8gPSBnb2kocGF0aD1z',
'dHIobGEpICsgb3MucGF0aHNlcCArIHN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkKICAgICAg',
'ICByMCwgXyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3KSkgICAgICMgZG9p',
'IGNodW5nIGR1b25nCiAgICBrcSA9IHsiY28gbXVjIGNodWEgJzsnIjogIk5IQU4iIGlmIHIgZWxzZSAiTm9uZSIsICJkb2kg',
'Y2h1bmcgKGtob25nIGNvICc7JykiOiAiTkhBTiIgaWYgcjAgZWxzZSAiTm9uZSJ9CiAgICBpZiBub3QgcjA6CiAgICAgICAg',
'cmV0dXJuIEtERCwgImRvaSBjaHVuZyBkdW9uZyBob25nIiwga3EKICAgIHJldHVybiAoREFUIGlmIHIgZWxzZSBUUlVPVCks',
'ICgiIiBpZiByIGVsc2UgIm11YyBnaXQuZXhlIGhvcCBsZSBiaSBNQVQiKSwga3EKCmRlZiBkb19uMTEoZ29pLCBzaWcsIHRl',
'cHQpOgogICAgIiIiVHJ1eWVuIGNoYW5fZG9hbiA9PiB0aHUgZHVvYyB0aG9uZyBiYW8gVkEgc3RkZXJyIElNLiBLaG9uZyB0',
'cnV5ZW4gPT4gc3RkZXJyIFZBTiBjby4iIiIKICAgIGlmICJjaGFuX2RvYW4iIG5vdCBpbiBzaWcucGFyYW1ldGVyczoKICAg',
'ICAgICByZXR1cm4gS0RELCAiX2dpdF93aW5kb3dzIGtob25nIG5oYW4gdGhhbSBzbyBjaGFuX2RvYW4iLCB7InRoYW0gc28i',
'OiBsaXN0KHNpZy5wYXJhbWV0ZXJzKX0KICAgIHdpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAg',
'ICAgICBkLCBjdywgcGYgPSBfc2FuKHQpCiAgICAgICAgKGQvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9',
'InV0Zi04IikKICAgICAgICBjZCA9IFtdCiAgICAgICAgXywgZV9jbyA9IGdvaShwYXRoPXN0cihkKSwgcHJvZ3JhbV9maWxl',
'cz1zdHIocGYpLCBjd2Q9c3RyKGN3KSwgY2hhbl9kb2FuPWNkKQogICAgICAgIF8sIGVfa2ggPSBnb2kocGF0aD1zdHIoZCks',
'IHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjdykpCiAgICBrcSA9IHsiY2hhbl9kb2FuIHRodSBkdW9jIChtdWMp',
'IjogbGVuKGNkKSwKICAgICAgICAgICJzdGRlcnIga2hpIENPIGNoYW5fZG9hbiAoYnl0ZSkiOiBsZW4oZV9jby5lbmNvZGUo',
'KSksCiAgICAgICAgICAic3RkZXJyIGtoaSBLSE9ORyB0cnV5ZW4gKGJ5dGUpIjogbGVuKGVfa2guZW5jb2RlKCkpfQogICAg',
'aWYgbGVuKGNkKSA9PSAwIGFuZCBsZW4oZV9raC5lbmNvZGUoKSkgPT0gMDoKICAgICAgICByZXR1cm4gS0RELCAibmhhbmgg',
'JVByb2dyYW1GaWxlcyUga2hvbmcgcGhhbiBnaWFpIEtIT05HIGJheSByYSBjaGFuIGRvYW4gbmFvIC0+IGNodWEgZG8gZHVv',
'YyIsIGtxCiAgICBvayA9IGxlbihjZCkgPiAwIGFuZCBsZW4oZV9jby5lbmNvZGUoKSkgPT0gMCBhbmQgbGVuKGVfa2guZW5j',
'b2RlKCkpID4gMAogICAgcmV0dXJuIChEQVQgaWYgb2sgZWxzZSBUUlVPVCksICgiIiBpZiBvayBlbHNlICJ4ZW0gYmFuZyIp',
'LCBrcQoKZGVmIGRvX24xMihnb2ksIHNpZywgdGVwdCk6CiAgICAiIiJIYW5nIHNlbnRpbmVsIGdpdF9wYXRoIHRyb25nIGZp',
'eHR1cmUgcGhhaSB0dXlldCBkb2kgdHJlbiBDQSBIQUkgbmVuLiIiIgogICAgbmQgPSB0ZXB0LnJlYWRfdGV4dChlbmNvZGlu',
'Zz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiKQogICAgaGFuZyA9IHNvcnRlZChzZXQocmUuZmluZGFsbChyJ2dpdF9wYXRo',
'XHMqPVxzKiIoW14iXSspIicsIG5kKSkpCiAgICB4YXUgPSBbaCBmb3IgaCBpbiBoYW5nIGlmIG5vdCAoUHVyZVBvc2l4UGF0',
'aChoKS5pc19hYnNvbHV0ZSgpIGFuZCBQdXJlV2luZG93c1BhdGgoaCkuaXNfYWJzb2x1dGUoKSldCiAgICBrcSA9IHsiaGFu',
'ZyBnaXRfcGF0aCB0aW0gdGhheSI6IGhhbmcsICJjaGkgdHV5ZXQgZG9pIE1PVCBuZW4iOiB4YXV9CiAgICBpZiBub3QgaGFu',
'ZzoKICAgICAgICByZXR1cm4gS0RELCAia2hvbmcgdGltIHRoYXkgaGFuZyBnaXRfcGF0aCBuYW8gdHJvbmcgZml4dHVyZSAt',
'PiBtYXUgZG9jIGNvIHRoZSBkYSBkb2kiLCBrcQogICAgcmV0dXJuIChEQVQgaWYgbm90IHhhdSBlbHNlIFRSVU9UKSwgKCIi',
'IGlmIG5vdCB4YXUgZWxzZSBmImNoaS1tb3QtbmVuOiB7eGF1fSIpLCBrcQoKUFJPQkUgPSBbKCJOOCBidW9jIDEgY2hpIG5o',
'YW4gZ2l0LmV4ZSIsIGRvX244KSwKICAgICAgICAgKCJOOSBib2MgbmhheSBrZXAgbyBtdWMgUEFUSCIsIGRvX245KSwKICAg',
'ICAgICAgKCJOMTAgZGF1ICc7JyB0cm9uZyB0ZW4gdGh1IG11YyIsIGRvX24xMCksCiAgICAgICAgICgiTjExIGNoYW4gZG9h',
'biBkb2kga2VuaCIsIGRvX24xMSksCiAgICAgICAgICgiTjEyIGhhbmcgc2VudGluZWwgdHV5ZXQgZG9pIENBIEhBSSBuZW4i',
'LCBkb19uMTIpXQoKIyAtLS0gY2hlIGRvIFRVIEtJRU06IGNoYXkgbmFtIHByb2JlIHRyZW4gbW90IGNheSBiYXQga3ksIG5l',
'biBiYXQga3kgLS0tCmlmICItLXR1LWtpZW0tcHJvYmUiIGluIHN5cy5hcmd2OgogICAgX2cgPSBQYXRoKHN5cy5hcmd2W3N5',
'cy5hcmd2LmluZGV4KCItLXR1LWtpZW0tcHJvYmUiKSArIDFdKS5yZXNvbHZlKCkKICAgIF9zcCA9IGltcG9ydGxpYi51dGls',
'LnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscF90ayIsIHN0cihfZy8ib3BzIi8ibGVhc2VfcHVibGlzaC5weSIpKQogICAg',
'X2xwID0gaW1wb3J0bGliLnV0aWwubW9kdWxlX2Zyb21fc3BlYyhfc3ApOyBfc3AubG9hZGVyLmV4ZWNfbW9kdWxlKF9scCkK',
'ICAgIF9zaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShfbHAuX2dpdF93aW5kb3dzKQogICAgZGVmIF9nb2koKiprdyk6CiAgICAg',
'ICAgZSA9IGlvLlN0cmluZ0lPKCkKICAgICAgICB3aXRoIGNvbnRleHRsaWIucmVkaXJlY3Rfc3RkZXJyKGUpOgogICAgICAg',
'ICAgICByZXR1cm4gX2xwLl9naXRfd2luZG93cygqKmt3KSwgZS5nZXR2YWx1ZSgpCiAgICBwcmludChmIlRVIEtJRU0gUFJP',
'QkUgdHJlbiB7X2d9ICAobmVuIHtzeXMucGxhdGZvcm19KSIpCiAgICBmb3IgX3RlbiwgX2YgaW4gUFJPQkU6CiAgICAgICAg',
'X3R0LCBfY3QsIF9kbCA9IF9mKF9nb2ksIF9zaWcsIF9nLyJvcHMiLyJsZWFzZV9wdWJsaXNoX3Rlc3QucHkiKQogICAgICAg',
'IHByaW50KGYiICBbe190dDoxNH1dIHtfdGVufSIgKyAoZiIgICB7X2N0fSIgaWYgX2N0IGVsc2UgIiIpKQogICAgICAgIGZv',
'ciBfaywgX3YgaW4gKF9kbCBvciB7fSkuaXRlbXMoKTogcHJpbnQoZiIgICAgICAgIHtfazozNH06IHtfdn0iKQogICAgc3lz',
'LmV4aXQoMCkKCmlubigiPSIgKiA3OCk7IGlubigiV1A1NDEgZzIgLSBwaGVwIGRvIHRyZW4gV2luZG93cyB0aGF0IChzcGVj',
'IHIzOiBOMS1ONCwgTjgtTjEyLCBONywga2ljaCB0aHVvYykiKTsgaW5uKCI9IiAqIDc4KQoKIyAtLS0tLS0tLS0tLS0tLS0t',
'IHR1IGtpZW0gYm8gZG9jIC0tLS0tLS0tLS0tLS0tLS0KX2QsIF9nLCBfdCA9IGRvY19kbyhfTUFVKQpfb2sgPSAobGVuKF9k',
'KSA9PSAyIGFuZCBhbnkoeC5zdGFydHN3aXRoKCJ0MDJiIikgZm9yIHggaW4gX2QpCiAgICAgICBhbmQgbm90IGFueSh4LnN0',
'YXJ0c3dpdGgoInQxMzEiKSBmb3IgeCBpbiBfZCkgYW5kIF90KQppbm4oIlR1IGtpZW0gYm8gZG9jIGxvZzoiLCBEQVQgaWYg',
'X29rIGVsc2UgVFJVT1QpCmlmIG5vdCBfb2s6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IGJvIGRvYyBsb2cg',
'Y3VhIGNoaW5oIHNjcmlwdCBuYXkgc2FpIC0+IGtob25nIGRvIGdpIGNhLiIpOyBzeXMuZXhpdCgzKQoKIyAtLS0tLS0tLS0t',
'LS0tLS0tIDAuIG5lbiBkbyAtLS0tLS0tLS0tLS0tLS0tCmdvYyA9IFBhdGgoc3lzLmFyZ3ZbMV0pLnJlc29sdmUoKSBpZiBs',
'ZW4oc3lzLmFyZ3YpID4gMSBlbHNlIFBhdGguY3dkKCkKdGVwLCB0ZXB0ID0gZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlz',
'aC5weSIsIGdvYyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2hfdGVzdC5weSIKaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5u',
'KCIwLiBORU4gRE8iKQojIE1PSSBMT0cgUEhBSSBUVSBLSEFJIG5vIGRvIENBSSBHSSBiYW5nIEJPIERPIE5BTy4gQmFpIGhv',
'YyAxOS0wOS0yMDI2OiBtb3QgbHVvdCBkbwojIGd1aSB2ZSBkdW9jIGRvYyBuaHUga2V0IHF1YSBjdWEgYmFuIHZhIGRhbmcg',
'eGV0LCBuaHVuZyB0aGF0IHJhIGxhIGJhbiBkbyBDVSBjaGF5CiMgdHJlbiBuaGFuaCBLSEFDLiBEb2MgcmEgdGhpIG1hdCBt',
'b3Qgdm9uZzsgbG9nIHR1IGtoYWkgdGhpIHRoYXkgbmdheSBkb25nIGRhdS4KdHJ5OgogICAgX3R1ID0gaGFzaGxpYi5zaGEy',
'NTYoUGF0aChfX2ZpbGVfXykucmVhZF9ieXRlcygpKS5oZXhkaWdlc3QoKQpleGNlcHQgRXhjZXB0aW9uIGFzIF9lOgogICAg',
'X3R1ID0gZiJraG9uZyB0dSBiYW0gZHVvYzoge19lfSIKZ2hpKCJib19kb19zaGEyNTYiLCBfdHUpCmlubihmIiAgQk8gRE8g',
'ICAgICAgIDogc2hhMjU2IHtfdHVbOjE2XX0gIChiYW4ge0JBTl9CT19ET30pIikKaW5uKCIgIHN5cy5wbGF0Zm9ybSA6Iiwg',
'c3lzLnBsYXRmb3JtLCAifCBweXRob24iLCBzeXMudmVyc2lvbi5zcGxpdCgpWzBdKQppbm4oIiAgb3MucGF0aHNlcCAgIDoi',
'LCByZXByKG9zLnBhdGhzZXApLCAifCBQQVRIRVhUOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlBBVEhFWFQiKSlbOjYwXSkK',
'aW5uKCIgIFByb2dyYW1GaWxlcyA6IiwgcmVwcihvcy5lbnZpcm9uLmdldCgiUHJvZ3JhbUZpbGVzIikpLCAifCBTeXN0ZW1S',
'b290OiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlN5c3RlbVJvb3QiKSkpCmlubigiICBDT05HX0NVX0dJVCAgOiIsIHJlcHIo',
'b3MuZW52aXJvbi5nZXQoIkNPTkdfQ1VfR0lUIikpKQppbm4oIiAgZ29jIGtobyAgICAgIDoiLCBnb2MpCgpxdXllbiA9IE5v',
'bmUKaWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlczsgcXV5ZW4gPSBi',
'b29sKGN0eXBlcy53aW5kbGwuc2hlbGwzMi5Jc1VzZXJBbkFkbWluKCkpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBxdXllbiA9',
'IE5vbmUKZ2hpKCJxdXllbl9hZG1pbiIsIHF1eWVuKQpzeW1saW5rX2R1b2MgPSBOb25lCnRyeToKICAgIHdpdGggdGVtcGZp',
'bGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgICAgICBkID0gUGF0aCh0KS8iYS50eHQiOyBkLndyaXRlX3RleHQo',
'IngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHRyeTogb3Muc3ltbGluayhzdHIoZCksIHN0cihQYXRoKHQpLyJsayIp',
'KTsgc3ltbGlua19kdW9jID0gVHJ1ZQogICAgICAgIGV4Y2VwdCBPU0Vycm9yIGFzIGU6IHN5bWxpbmtfZHVvYyA9IEZhbHNl',
'OyBnaGkoInN5bWxpbmtfbG9pIiwgZiJ7dHlwZShlKS5fX25hbWVfX306IHtlfSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZTog',
'Z2hpKCJzeW1saW5rX2xvaSIsIHN0cihlKSkKZ2hpKCJzeW1saW5rX2R1b2MiLCBzeW1saW5rX2R1b2MpCmlubigiICBBZG1p',
'bmlzdHJhdG9yOiIsIHF1eWVuLCAifCB0YW8gc3ltbGluayBkdW9jOiIsIHN5bWxpbmtfZHVvYykKCmxvaSA9IFtdCiMgQ29u',
'ZyBraWNoIHRodW9jIGxhIHBoZXAgZG8gdHJlbiBMSUNIIFNVIEdJVCwga2hvbmcgZGluaCBnaSBkZW4gbmVuLiBDaG8gcGhl',
'cAojIC0tY2hpLWtpY2gtdGh1b2MgY2hheSBvIG1vaSBuZW4gZGUgY29uIFRVIEtJRU0gZHVvYyBjaGluaCBjb25nIG5heSAo',
'ZGEgZHVuZwojIGRlIHRhaSBkdW5nIGNhIGhhaSB2ZSBjdWEgc3UgY28gbmVuLWN1IDE5LTA5KS4gTW9pIGNob3QgQ0hVQyBO',
'QU5HIHZhbiBkb2kgV2luZG93cy4KaWYgc3lzLnBsYXRmb3JtICE9ICJ3aW4zMiIgYW5kICItLWNoaS1raWNoLXRodW9jIiBu',
'b3QgaW4gc3lzLmFyZ3Y6CiAgICBsb2kuYXBwZW5kKGYiS0hPTkcgcGhhaSBXaW5kb3dzIChzeXMucGxhdGZvcm09e3N5cy5w',
'bGF0Zm9ybSFyfSkiKQppZiBub3QgdGVwLmlzX2ZpbGUoKTogIGxvaS5hcHBlbmQoZiJraG9uZyB0aGF5IHt0ZXB9IikKaWYg',
'bm90IHRlcHQuaXNfZmlsZSgpOiBsb2kuYXBwZW5kKGYia2hvbmcgdGhheSB7dGVwdH0iKQppZiBub3Qgc2h1dGlsLndoaWNo',
'KCJnaXQiKTogbG9pLmFwcGVuZCgia2hvbmcgY28gYGdpdGAgdHJvbmcgUEFUSCIpCgpyYywgaGVhZCwgXyA9IGdpdChnb2Ms',
'ICJyZXYtcGFyc2UiLCAiSEVBRCIpCmlmIHJjOiBsb2kuYXBwZW5kKCJraG9uZyBkb2MgZHVvYyBIRUFEIikKZ2hpKCJoZWFk',
'IiwgaGVhZCkKcmNfYSwgXywgXyA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwgIi0taXMtYW5jZXN0b3IiLCBTSEFfRzEsIGhl',
'YWQgb3IgIkhFQUQiKQpsYV9oYXVfZHVlID0gKHJjX2EgPT0gMCkKaWYgaGVhZCA9PSBTSEFfRzE6CiAgICB0aGVfaGUgPSAi',
'ZzEiOyBpbm4oZiIgIEhFQUQgPSB7aGVhZFs6OF19IC0+IERBWSBMQSBnMS4gQ0hVQSBjbyBiYW4gdmEgZzI7IGtldCBxdWEg',
'ZHVvaSBsYSBORU4gRE8uIikKZWxpZiBsYV9oYXVfZHVlOgogICAgdGhlX2hlID0gImcyIjsgaW5uKGYiICBIRUFEID0ge2hl',
'YWRbOjhdfSAtPiBoYXUgZHVlIGN1YSBnMSAoe1NIQV9HMVs6OF19KTogdW5nIHZpZW4gZzIuIikKZWxzZToKICAgIHRoZV9o',
'ZSA9ICI/IjsgbG9pLmFwcGVuZChmIkhFQUQ9e2hlYWRbOjhdfSBLSE9ORyBwaGFpIGcxIHZhIEtIT05HIHBoYWkgaGF1IGR1',
'ZSBjdWEge1NIQV9HMVs6OF19IOKAlCByZWJhc2U/IG5oYW0gbmhhbmg/IikKZ2hpKCJ0aGVfaGUiLCB0aGVfaGUpCnJjX3Is',
'IHJlZnMsIF8gPSBnaXQoZ29jLCAiZm9yLWVhY2gtcmVmIiwgIi0tcG9pbnRzLWF0IiwgaGVhZCBvciAiSEVBRCIsCiAgICAg',
'ICAgICAgICAgICAgICAgIi0tZm9ybWF0PSUocmVmbmFtZTpzaG9ydCkiKQpkc3IgPSBbeCBmb3IgeCBpbiByZWZzLnNwbGl0',
'bGluZXMoKSBpZiB4LnN0cmlwKCkgYW5kIHguc3RyaXAoKSAhPSAiZG8tdGFtIl0KZ2hpKCJyZWZfdHJvX3RvaV9oZWFkIiwg',
'ZHNyKQppbm4oZiIgIHJlZiB0cm8gdG9pIEhFQUQ6IHsnLCAnLmpvaW4oZHNyKSBpZiBkc3IgZWxzZSAnKGtob25nIHJlZiBu',
'YW8gLSBIRUFEIHJvaSB0dSBkbyknfSIpCgppZiBsb2k6CiAgICBpbm4oIiIpOyBpbm4oIktIT05HIERPIERVT0M6IG5lbiBk',
'byBzYWksIEtIT05HIGluIGtldCBsdWFuIG5hby4iKQogICAgZm9yIHggaW4gbG9pOiBpbm4oIiAgLSIsIHgpCiAgICBzeXMu',
'ZXhpdCgzKQoKIyAtLS0tLS0tLS0tLS0tLS0tIDEuIGtpY2ggdGh1b2MgKE43JyBjdWEgc3BlYyByMykgLS0tLS0tLS0tLS0t',
'LS0tLQppbm4oIiIpOyBpbm4oIi0iICogNzgpOyBpbm4oIjEuIEtJQ0ggVEhVT0Mg4oCUIHRyYW4gc3BlYyByMzogPD0gMiB0',
'ZXAgdmEgPD0gNDAwIGRvbmcgdGhlbSIpCiMgVkUgTkVOIFBIQUkgVFVPSSDigJQgdmEgcGhhaSBDSFVORyBNSU5IIGR1b2Mg',
'bGEgdHVvaSwga2hvbmcgcGhhaSBnaWEgZGluaC4KIyBCYWkgaG9jIHRyYSBnaWEgMTktMDktMjAyNjogY2xvbmUgdGFpIGR1',
'bmcgY2hpIGZldGNoIG5oYW5oIGJhbiB2YSwgYG9yaWdpbi9tYXN0ZXJgCiMgZHVuZyB5ZW4gdHUgMTQtMDkgKGMxNmJkMzIs',
'IHNhdSA5NyBjb21taXQpLiBtZXJnZS1iYXNlIHJvaSB2ZSBkdW5nIGRpbmggbWFzdGVyIGN1LAojIG5lbiBkaWZmIE5VT1Qg',
'Y2EgOTcgY29tbWl0IG1hc3RlcjogZG8gcmEgNDYgdGVwIC8gKzcxMTggdGhheSB2aSAyIHRlcCAvICszOTcg4oCUCiMgQ1VO',
'RyBNT1QgQ09NTUlUIDBlYTk1ZGUuIE1vdCB0aWV1IGNoaSBERUxUQSBtYSB2ZSBuZW4ga2hvbmcgdHVvaSB0aGkga2hvbmcg',
'c2FpCiMgbGVjaCBtb3QgY2h1dCwgbm8gc2FpIGNhIG1vdCBiYWMgZG8gbG9uLgojIENobyBuZW46IG5lbiBraG9uZyBjaHVu',
'ZyBtaW5oIGR1b2MgbGEgdHVvaSA9PiBLSE9ORyBETyBEVU9DIChyYz0zKSwgS0hPTkcgcGhhaSBUUlVPVC4KIyBUUlVPVCBs',
'YSBtb3QgUEhBTiBRVVlFVCB2ZSBiYW4gdmE7IHBoYW4gcXV5ZXQgY2hpIGR1b2MgcGhlcCBwaGF0IHJhIGtoaSBkYSBkbyBk',
'dW9jLgpyY19sciwgb3V0X2xyLCBlcl9sciA9IGdpdChnb2MsICJscy1yZW1vdGUiLCAib3JpZ2luIiwgInJlZnMvaGVhZHMv',
'bWFzdGVyIikKcmNfbG0sIGxtLCBlcl9sbSAgICAgPSBnaXQoZ29jLCAicmV2LXBhcnNlIiwgIm9yaWdpbi9tYXN0ZXIiKQpy',
'bSA9IG91dF9sci5zcGxpdCgpWzBdIGlmIChub3QgcmNfbHIgYW5kIG91dF9sci5zdHJpcCgpKSBlbHNlICIiCmlmIG5vdCBy',
'bToKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsCiAgICAgICAgZiJraG9uZyBob2kgZHVvYyBtYXN0ZXIgdHJlbiBy',
'ZW1vdGUgKGxzLXJlbW90ZSByYz17cmNfbHJ9KToge2VyX2xyWzo2MF19ICIKICAgICAgICBmIuKAlCBraG9uZyBjaHVuZyBt',
'aW5oIGR1b2MgdmUgbmVuIGNvbiB0dW9pIikKICAgIHJjX21iLCBtYiwgbnMsIHJjID0gMSwgIiIsICIiLCAxCmVsaWYgcmNf',
'bG0gb3Igbm90IGxtOgogICAga2V0KCJONycga2ljaCB0aHVvYyIsIEtERCwgZiJraG9uZyBkb2MgZHVvYyBvcmlnaW4vbWFz',
'dGVyIHRyb25nIGNsb25lOiB7ZXJfbG1bOjYwXX0iKQogICAgcmNfbWIsIG1iLCBucywgcmMgPSAxLCAiIiwgIiIsIDEKZWxp',
'ZiBsbSAhPSBybToKICAgICMgRGVtIHhlbSB0dXQgbGFpIGJhbyB4YSwgbmV1IGRlbSBkdW9jIOKAlCBjb24gc28gbmF5IG5v',
'aSBybyBtdWMgZG8gc2FpIGxlY2guCiAgICByY19jLCBzYXUsIF8gPSBnaXQoZ29jLCAicmV2LWxpc3QiLCAiLS1jb3VudCIs',
'IGYie2xtfS4ue3JtfSIpCiAgICB4YSA9IGYiLCB0dXQgbGFpIHtzYXV9IGNvbW1pdCIgaWYgKG5vdCByY19jIGFuZCBzYXUu',
'c3RyaXAoKS5pc2RpZ2l0KCkpIGVsc2UgIiIKICAgIGlubihmIiAgb3JpZ2luL21hc3RlciB0cm9uZyBjbG9uZSA6IHtsbVs6',
'MTJdfSIpCiAgICBpbm4oZiIgIG1hc3RlciB0cmVuIHJlbW90ZSAgICAgICAgOiB7cm1bOjEyXX17eGF9IikKICAgIGdoaSgi',
'bWFzdGVyX2Nsb25lIiwgbG0pOyBnaGkoIm1hc3Rlcl9yZW1vdGUiLCBybSkKICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBL',
'REQsCiAgICAgICAgZiJ2ZSBuZW4gQ1U6IG9yaWdpbi9tYXN0ZXI9e2xtWzoxMl19ICE9IHJlbW90ZT17cm1bOjEyXX17eGF9',
'ICIKICAgICAgICBmIuKAlCBjaGF5IGBnaXQgLUMgPGtobz4gZmV0Y2ggb3JpZ2luIG1hc3RlcmAgcm9pIGRvIGxhaSIpCiAg',
'ICByY19tYiwgbWIsIG5zLCByYyA9IDEsICIiLCAiIiwgMQplbHNlOgogICAgaW5uKGYiICB2ZSBuZW4gVFVPSTogb3JpZ2lu',
'L21hc3RlciA9IHtsbVs6MTJdfSA9PSBtYXN0ZXIgdHJlbiByZW1vdGUiKQogICAgZ2hpKCJtYXN0ZXJfY2xvbmUiLCBsbSk7',
'IGdoaSgibWFzdGVyX3JlbW90ZSIsIHJtKQogICAgcmNfbWIsIG1iLCBlcl9tYiA9IGdpdChnb2MsICJtZXJnZS1iYXNlIiwg',
'Im9yaWdpbi9tYXN0ZXIiLCBoZWFkKQppZiByY19tYiBvciBub3QgbWI6CiAgICBpZiBtYiA9PSAiIiBhbmQgcm0gYW5kIGxt',
'ID09IHJtOgogICAgICAgIGtldCgiTjcnIGtpY2ggdGh1b2MiLCBLREQsIGYia2hvbmcgdGluaCBkdW9jIG1lcmdlLWJhc2Ug',
'dm9pIG9yaWdpbi9tYXN0ZXI6IHtlcl9tYls6NzBdfSIpCiAgICBucywgcmMgPSAiIiwgMQplbHNlOgogICAgZ2hpKCJtZXJn',
'ZV9iYXNlIiwgbWIpCiAgICBpbm4oZiIgIG1lcmdlLWJhc2Uob3JpZ2luL21hc3RlciwgSEVBRCkgPSB7bWJbOjEyXX0iKQog',
'ICAgaWYgbWIgIT0gU0hBX0JBU0VfU1BFQzoKICAgICAgICBpbm4oZiIgIExVVSBZOiBraGFjIGJhc2UgbWEgc3BlYyByMyBr',
'aGFpICh7U0hBX0JBU0VfU1BFQ1s6MTJdfSkg4oCUIHZpIG5oYW5oIGRhIG1lcmdlIG1hc3Rlci4iKQogICAgICAgIGlubihm',
'IiAgICAgICAgIERvIHNvIGJhc2UgY3Ugc2UgTlVPVCBwaGFuIG1hc3RlciBtYW5nIHZhby4gRHVuZyBtZXJnZS1iYXNlIG1v',
'aSBsYSB2aWVjIGN1YSBleGVjdXRvci4iKQogICAgICAgIHJjX3gsIG5zX3gsIF8gPSBnaXQoZ29jLCAiZGlmZiIsICItLW51',
'bXN0YXQiLCBTSEFfQkFTRV9TUEVDLCBoZWFkKQogICAgICAgIGlmIG5vdCByY194OgogICAgICAgICAgICBoID0gW2wuc3Bs',
'aXQoIlx0IikgZm9yIGwgaW4gbnNfeC5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgpXQogICAgICAgICAgICBhID0gc3VtKGlu',
'dCh4WzBdKSBmb3IgeCBpbiBoIGlmIHhbMF0uaXNkaWdpdCgpKQogICAgICAgICAgICBnaGkoIm51bXN0YXRfdGhlb19iYXNl',
'X3NwZWMiLCB7InRlcCI6IGxlbihoKSwgInRoZW0iOiBhfSkKICAgICAgICAgICAgaW5uKGYiICAgICAgICAgKGRvaSBjaGll',
'dTogc28gYmFzZSBzcGVjID0ge2xlbihoKX0gdGVwIC8gK3thfSDigJQgY29uIHNvIGF5IEtIT05HIGR1bmcgZGUgY2hhbSki',
'KQogICAgcmMsIG5zLCBlciA9IGdpdChnb2MsICJkaWZmIiwgIi0tbnVtc3RhdCIsIG1iLCBoZWFkKQppZiByYzoKICAgIHBh',
'c3MKZWxzZToKICAgIGhhbmcgPSBbbC5zcGxpdCgiXHQiKSBmb3IgbCBpbiBucy5zcGxpdGxpbmVzKCkgaWYgbC5zdHJpcCgp',
'XQogICAgdGhlbSA9IHN1bShpbnQoaFswXSkgZm9yIGggaW4gaGFuZyBpZiBoWzBdLmlzZGlnaXQoKSkKICAgIHhvYSAgPSBz',
'dW0oaW50KGhbMV0pIGZvciBoIGluIGhhbmcgaWYgaFsxXS5pc2RpZ2l0KCkpCiAgICBnaGkoInNvX3RlcCIsIGxlbihoYW5n',
'KSk7IGdoaSgiZG9uZ190aGVtIiwgdGhlbSk7IGdoaSgiZG9uZ194b2EiLCB4b2EpCiAgICBmb3IgaCBpbiBoYW5nOiBpbm4o',
'ZiIgICAge2hbMl06MzR9ICt7aFswXTo8NX0gLXtoWzFdfSIpCiAgICBpbm4oZiIgICAgVE9ORzoge2xlbihoYW5nKX0gdGVw',
'LCAre3RoZW19LCAte3hvYX0gICAodHJhbjoge1RSQU5fVEVQfSB0ZXAgLyB7VFJBTl9ET05HfSBkb25nIHRoZW0pIikKICAg',
'IGtldCgiTjcnIGtpY2ggdGh1b2MiLCBEQVQgaWYgKGxlbihoYW5nKSA8PSBUUkFOX1RFUCBhbmQgdGhlbSA8PSBUUkFOX0RP',
'TkcpIGVsc2UgVFJVT1QsCiAgICAgICAgZiJ7bGVuKGhhbmcpfSB0ZXAgLyAre3RoZW19IikKCiMgQ29uZyBuaGFuaDogZG8g',
'UklFTkcga2ljaCB0aHVvYyAodmFpIGdpYXkpIHJvaSBkdW5nLiBEdW5nIGtoaSBjYW4geGFjIG1pbmggbGFpCiMgdmUgbmVu',
'IG1hIGtob25nIG11b24gdHJhIDIwLTQ1IHBodXQgY2hvIGNhIGJvIHRlc3QuCmlmICItLWNoaS1raWNoLXRodW9jIiBpbiBz',
'eXMuYXJndjoKICAgIGlubigiIik7IGlubigiPSIgKiA3OCkKICAgIGlubigiLS1jaGkta2ljaC10aHVvYzogQ0hJIGRvIGNv',
'bmcga2ljaCB0aHVvYy4gRGF5IEtIT05HIHBoYWkgbW90IGx1b3QgbmdoaWVtIHRodS4iKQogICAgaW5uKCItIiAqIDc4KQog',
'ICAgZm9yIF90LCBfdHQsIF9jdCBpbiBjaG90OiBpbm4oZiIgIHtfdHQ6MTR9IHtfdH0iICsgKGYiICAge19jdH0iIGlmIF9j',
'dCBlbHNlICIiKSkKICAgIF9rID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IEtERCkKICAgIF9yID0gc3Vt',
'KDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQogICAgc3lzLmV4aXQoMyBpZiBfayBlbHNlICgxIGlmIF9y',
'IGVsc2UgMCkpCgojIC0tLS0tLS0tLS0tLS0tLS0gMi4gYm8gdGVzdCBkYXkgZHUgLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIp',
'OyBpbm4oIi0iICogNzgpOyBpbm4oIjIuIEJPIFRFU1QgREFZIERVICgxMC00MCBwaHV0KSIpCnJjX24sIG91dF9uID0gY2hh',
'eShbIm9wcy9sZWFzZV9wdWJsaXNoX3Rlc3QucHkiXSwgZ29jKQpnaGkoInJjX3N1aXRlIiwgcmNfbikKbSA9IFJYX1RPTkcu',
'c2VhcmNoKG91dF9uKQppbm4oIiAgcmMgPSIsIHJjX24sICJ8IiwgbS5ncm91cCgwKSBpZiBtIGVsc2UgIihLSE9ORyBkb2Mg',
'ZHVvYyBkb25nIHRvbmcga2V0KSIpCmlmIG06CiAgICBnaGkoImRhdCIsIGludChtLmdyb3VwKDEpKSk7IGdoaSgidHJlbiIs',
'IGludChtLmdyb3VwKDIpKSk7IGdoaSgiYm9fcXVhX3NvIiwgaW50KG0uZ3JvdXAoNCkpKQpkb19oZXQsIGdjLCB0aW4gPSBk',
'b2NfZG8ob3V0X24pCmdoaSgic29fY2FfZG8iLCBsZW4oZG9faGV0KSk7IGdoaSgibGlldF9rZV9kYXlfZHUiLCB0aW4pCmZv',
'ciBnIGluIGdjOiBpbm4oIiAgICoiLCBnKQppbm4oIiIpOyBpbm4oZiIgID09PSB7bGVuKGRvX2hldCl9IENBIERPID09PSIp',
'CmZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICBpbm4oZiIgICB7dC5zcGxpdCgnXycpWzBdOjd9IHt0',
'fSIpOyBpbm4oZiIgICAgICAgICAgIHtkb19oZXRbdF1bOjE1MF19IikKZ2hpKCJkb19seV9kbyIsIHt0OiBkb19oZXRbdF1b',
'OjMwMF0gZm9yIHQgaW4gZG9faGV0fSkKIyAtLS0tIENIT1Q6IG1vaSBjYSBETyBwaGFpIEdJQUkgVEhJQ0ggRFVPQyAtLS0t',
'CiMgVGhpZXUgY2hvdCBuYXksIGJvIGRvIGluIGRhbmggc2FjaCBkbyByb2kgdmFuIHRob2F0IHJjPTAuIERvIGR1bmcgbGEg',
'bG9pIGRhIHhheSByYToKIyBsdW90IFdpbmRvd3MgMTktMDkgY28gdDE3MSBETyBtYSBibyBkbyBiYW8gIkRBVCAxMCB8IFRS',
'VU9UIDAiIHZhIHJjPTAuCmRlZiBfa2hvYSh0KTogcmV0dXJuIHQuc3BsaXQoIl8iKVswXQpkb19wYWNrZXQsIGRvX2xhLCBk',
'b190aGlldV9jb25nX2N1ID0gW10sIFtdLCBbXQpmb3IgdCBpbiBzb3J0ZWQoZG9faGV0LCBrZXk9c29fY2EpOgogICAgaywg',
'bHkgPSBfa2hvYSh0KSwgZG9faGV0W3RdCiAgICBpZiBrIGluIENBX1BBQ0tFVDogICAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICBkb19wYWNrZXQuYXBwZW5kKHQpCiAgICBlbGlmICJLSMOUTkcgxJBPIMSQxq/hu6JDIiBpbiBseSBvciAidGhp4bq/',
'dSBgIiBpbiBseTogIGRvX3RoaWV1X2NvbmdfY3UuYXBwZW5kKHQpCiAgICBlbGlmIGsgaW4gTkdPQUlfUEhBTV9WSTogICAg',
'ICAgICAgICAgICAgICAgICAgICBwYXNzCiAgICBlbHNlOiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg',
'ICAgICBkb19sYS5hcHBlbmQodCkKZ2hpKCJkb19wYWNrZXQiLCBkb19wYWNrZXQpOyBnaGkoImRvX2xhIiwgZG9fbGEpOyBn',
'aGkoImRvX3RoaWV1X2NvbmdfY3UiLCBkb190aGlldV9jb25nX2N1KQppbm4oIiIpCmlubihmIiAgY2EgRE8gdGh1b2MgQ0hJ',
'TkggcGFja2V0IG5heSA6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fcGFja2V0XSBvciAna2hvbmcgY28nfSIpCmlubihmIiAg',
'Y2EgRE8gbmdvYWkgcGhhbSB2aSAocjMga2hhaSk6IHtbX2tob2EoeCkgZm9yIHggaW4gc29ydGVkKGRvX2hldCwga2V5PXNv',
'X2NhKSBpZiBfa2hvYSh4KSBpbiBOR09BSV9QSEFNX1ZJXX0iKQppbm4oZiIgIGNhIERPIHZpIFRISUVVIENPTkcgQ1UgICAg',
'ICAgOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3RoaWV1X2NvbmdfY3VdIG9yICdraG9uZyBjbyd9IikKaW5uKGYiICBjYSBE',
'TyBMQSAoa2hvbmcgZ2lhaSB0aGljaCBkdW9jKToge1tfa2hvYSh4KSBmb3IgeCBpbiBkb19sYV0gb3IgJ2tob25nIGNvJ30i',
'KQprZXQoIktob25nIGNhIG5hbyBjdWEgUEFDS0VUIGJpIERPIiwgREFUIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBUUlVPVCwK',
'ICAgICIiIGlmIG5vdCBkb19wYWNrZXQgZWxzZSBmIkRPOiB7W19raG9hKHgpIGZvciB4IGluIGRvX3BhY2tldF19IOKAlCBi',
'YW4gdmEgQ0hVQSB4b25nIikKa2V0KCJNb2kgY2EgRE8gZGV1IGdpYWkgdGhpY2ggZHVvYyIsIERBVCBpZiBub3QgZG9fbGEg',
'ZWxzZSBUUlVPVCwKICAgICIiIGlmIG5vdCBkb19sYSBlbHNlIGYibGE6IHtbX2tob2EoeCkgZm9yIHggaW4gZG9fbGFdfSIp',
'CmlmIGRvX3RoaWV1X2NvbmdfY3U6CiAgICBrZXQoIkNvbmcgY3UgZGF5IGR1IGRlIGRvIiwgS0RELCBmInRoaWV1IGNvbmcg',
'Y3UgY2hvIHtbX2tob2EoeCkgZm9yIHggaW4gZG9fdGhpZXVfY29uZ19jdV19IikKCmJxID0gc29ydGVkKHt0IGZvciB0LCBf',
'IGluIFJYX0JPX1FVQS5maW5kYWxsKG91dF9uKX0sIGtleT1zb19jYSk7IGdoaSgiY2FfYm9fcXVhIiwgYnEpCmlubigiIik7',
'IGlubihmIiAgQk8gUVVBICh7bGVuKGJxKX0pOiB7W3guc3BsaXQoJ18nKVswXSBmb3IgeCBpbiBicV19IikKCmlubigiIik7',
'IGlubigiICBOMS1ONCAodDE2NS10MTY4KSwgdGlldSBjaGkgbmdoaWVtIHRodSBjdWEgcjIsIG5heSBsYSBjaGkgYmFvIGhv',
'aSBxdXk6IikKYjQgPSB7dDogbWF1X2NhKG91dF9uLCB0KSBmb3IgdCBpbiBDQU1PSX07IGdoaSgiY2FfbW9pIiwgYjQpCmZv',
'ciB0IGluIENBTU9JOiBpbm4oZiIgICAgIHt0fToge2I0W3RdfSIpCmtldCgiTjEtTjQgKHQxNjUtdDE2OCkiLCBEQVQgaWYg',
'YWxsKHYgPT0gIlFVQSIgZm9yIHYgaW4gYjQudmFsdWVzKCkpCiAgICBlbHNlIChLREQgaWYgYW55KHYgaXMgTm9uZSBmb3Ig',
'diBpbiBiNC52YWx1ZXMoKSkgZWxzZSBUUlVPVCksIHN0cihiNCkpCgppbm4oIiIpOyBpbm4oIiAgMTUgY2EgdHVuZyBkbyB0',
'cmVuIENJOiIpCmIxNSA9IHt0OiBtYXVfY2Eob3V0X24sIHQpIGZvciB0IGluIENBMTV9OyBnaGkoImNhMTUiLCBiMTUpCmlu',
'bigiICAgICIgKyAiICAiLmpvaW4oZiJ7dH06e2IxNVt0XX0iIGZvciB0IGluIENBMTUpKQoKIyB0MTM2IOKAlCBOMTIgZG8g',
'R0lBTiBUSUVQIHF1YSBrZXQgcXVhIGNhCnQxMzZfdGVuID0gbmV4dCgodCBmb3IgdCBpbiBkb19oZXQgaWYgdC5zdGFydHN3',
'aXRoKCJ0MTM2IikpLCBOb25lKQppZiBiMTUuZ2V0KCJ0MTM2IikgPT0gIlFVQSI6CiAgICBrZXQoIk4xMiB0MTM2IChxdWEg',
'a2V0IHF1YSBjYSkiLCBEQVQsICJ0MTM2IFFVQSIpCmVsaWYgYjE1LmdldCgidDEzNiIpIGlzIE5vbmU6CiAgICBrZXQoIk4x',
'MiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBLREQsICJraG9uZyB0aGF5IHQxMzYgdHJvbmcgbG9nIikKZWxzZToKICAgIGx5',
'ID0gZG9faGV0LmdldCh0MTM2X3RlbiwgIiIpCiAgICBrZXQoIk4xMiB0MTM2IChxdWEga2V0IHF1YSBjYSkiLCBUUlVPVCwg',
'ZiJETzoge2x5Wzo5MF19IikKCiMgLS0tLS0tLS0tLS0tLS0tLSAzLiBwcm9iZSBUSEFORyB2YW8gaGFtIC0tLS0tLS0tLS0t',
'LS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCIzLiBQUk9CRSBUSEFORyDigJQgZ29pIF9naXRfd2luZG93cyB2',
'b2kgdGhhbSBzbyB0aWVtIikKc3BlYyA9IGltcG9ydGxpYi51dGlsLnNwZWNfZnJvbV9maWxlX2xvY2F0aW9uKCJscDU0MSIs',
'IHN0cih0ZXApKQpscCA9IGltcG9ydGxpYi51dGlsLm1vZHVsZV9mcm9tX3NwZWMoc3BlYyk7IHNwZWMubG9hZGVyLmV4ZWNf',
'bW9kdWxlKGxwKQpzaWcgPSBpbnNwZWN0LnNpZ25hdHVyZShscC5fZ2l0X3dpbmRvd3MpCmdoaSgidGhhbV9zb19fZ2l0X3dp',
'bmRvd3MiLCBsaXN0KHNpZy5wYXJhbWV0ZXJzKSkKaW5uKCIgIHRoYW0gc28gY3VhIF9naXRfd2luZG93czoiLCBsaXN0KHNp',
'Zy5wYXJhbWV0ZXJzKSkKCmRlZiBnb2koKiprdyk6CiAgICAiIiJHb2kgX2dpdF93aW5kb3dzLCBCQVQgc3RkZXJyIGRlIG1v',
'dCBkb25nIGNoYW4gZG9hbiBraG9uZyBnaWV0IGx1b3QgZG8uIiIiCiAgICBlID0gaW8uU3RyaW5nSU8oKQogICAgd2l0aCBj',
'b250ZXh0bGliLnJlZGlyZWN0X3N0ZGVycihlKToKICAgICAgICByID0gbHAuX2dpdF93aW5kb3dzKCoqa3cpCiAgICByZXR1',
'cm4gciwgZS5nZXR2YWx1ZSgpCgojIC0tLSBkb2kgY2h1bmcgcmlnOiBwaGFpIHRyYSBsb2kgZHVuZyBtb3QgY2EgdGEgQklF',
'VCBUUlVPQyBkYXAgYW4gLS0tCndpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdDoKICAgIG5nb2FpID0g',
'UGF0aCh0KS8ibmdvYWkiOyBuZ29haS5ta2RpcigpOyBjdyA9IFBhdGgodCkvImN3ZCI7IGN3Lm1rZGlyKCk7IHBmID0gUGF0',
'aCh0KS8icGYiOyBwZi5ta2RpcigpCiAgICAobmdvYWkvImdpdC5leGUiKS53cml0ZV90ZXh0KCJ4IiwgZW5jb2Rpbmc9InV0',
'Zi04IikKICAgIHIxLCBfID0gZ29pKHBhdGg9c3RyKG5nb2FpKSwgcHJvZ3JhbV9maWxlcz1zdHIocGYpLCBjd2Q9c3RyKGN3',
'KSkKICAgIChjdy8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgcjIsIF8gPSBnb2ko',
'cGF0aD1zdHIoY3cpLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1zdHIoY3cpKQpyaWdfb2sgPSBib29sKHIxKSBhbmQg',
'cjIgaXMgTm9uZQpnaGkoInJpZ19kb2lfY2h1bmciLCByaWdfb2spCmtldCgiUklHIGRvaSBjaHVuZyAoYmlldCB0cnVvYyBk',
'YXAgYW4pIiwgREFUIGlmIHJpZ19vayBlbHNlIEtERCwKICAgIGYibmdvYWktY3dkLT57J05IQU4nIGlmIHIxIGVsc2UgJ05v',
'bmUnfSB8IHRyb25nLWN3ZC0+eydOSEFOJyBpZiByMiBlbHNlICdOb25lJ30iKQppZiBub3QgcmlnX29rOgogICAgaW5uKCIi',
'KTsgaW5uKCJLSE9ORyBETyBEVU9DOiByaWcgc2FpLCBtb2kgY2hvdCBkdW9pIHNlIHZvIG5naGlhLiIpOyBzeXMuZXhpdCgz',
'KQoKZm9yIHRlbiwgKHR0LCBjdCwgZGwpIGluIFsodCwgZihnb2ksIHNpZywgdGVwdCkpIGZvciB0LCBmIGluIFBST0JFXToK',
'ICAgIGdoaSgicHJvYmVfIiArIHRlbi5zcGxpdCgpWzBdLmxvd2VyKCksIGRsKQogICAgaWYgaXNpbnN0YW5jZShkbCwgZGlj',
'dCk6CiAgICAgICAgZm9yIGssIHYgaW4gZGwuaXRlbXMoKTogaW5uKGYiICAgIHtrOjM0fToge3Z9IikKICAgIGtldCh0ZW4s',
'IHR0LCBjdCkKCiMgLS0tLS0tLS0tLS0tLS0tLSA0LiBONyBkb3QgYmllbiB0cmVuIEJBTiBTQU8gVEFNIC0tLS0tLS0tLS0t',
'LS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCI0LiBONyDigJQgZG90IGJpZW4gdHJlbiBCQU4gU0FPIFRBTSAo',
'Y2F5IHRoYXQgS0hPTkcgYmkgZHVuZyB0b2kpIikKdHJ1b2MgPSB0ZXAucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNv',
'dW50KE1BVV9XSU4pCmdoaSgibjdfdHJ1b2MiLCB0cnVvYyk7IGlubihmIiAgc28gZG9uZyBraG9wIHtNQVVfV0lOIXJ9OiBU',
'UlVPQyA9IHt0cnVvY30gW21vbmcgMV0iKQppZiB0cnVvYyAhPSAxOgogICAga2V0KCJONyBkb3QgYmllbiBuaGFuaCBXaW5k',
'b3dzIiwgS0RELCBmIm1hdSB4dWF0IGhpZW4ge3RydW9jfSBsYW4sIGtob25nIHBoYWkgMSIpCmVsc2U6CiAgICB3aXRoIHRl',
'bXBmaWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHRtcDoKICAgICAgICBzYW8gPSBQYXRoKHRtcCkvImNheSIKICAgICAg',
'ICBzaHV0aWwuY29weXRyZWUoZ29jLCBzYW8sIGlnbm9yZT1zaHV0aWwuaWdub3JlX3BhdHRlcm5zKCIuZ2l0IiwgIl9fcHlj',
'YWNoZV9fIiwgIioucHljIikpCiAgICAgICAgZjIgPSBzYW8vIm9wcyIvImxlYXNlX3B1Ymxpc2gucHkiCiAgICAgICAgZjIu',
'd3JpdGVfdGV4dChmMi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikucmVwbGFjZShNQVVfV0lOLCAiaWYgRmFsc2U6Iiks',
'IGVuY29kaW5nPSJ1dGYtOCIpCiAgICAgICAgc2F1ID0gZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50KE1B',
'VV9XSU4pOyBnaGkoIm43X3NhdSIsIHNhdSkKICAgICAgICBpbm4oZiIgIFNBVSAoZGEgZG90IGJpZW4pID0ge3NhdX0gW21v',
'bmcgMF0iKQogICAgICAgIGlmIHNhdSAhPSAwOgogICAgICAgICAgICBrZXQoIk43IGRvdCBiaWVuIG5oYW5oIFdpbmRvd3Mi',
'LCBLREQsICJkb3QgYmllbiBLSE9ORyBhcCBkdW9jIikKICAgICAgICBlbHNlOgogICAgICAgICAgICByY19tLCBvdXRfbSA9',
'IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIHNhbykKICAgICAgICAgICAgbTE2NSA9IG1hdV9jYShvdXRf',
'bSwgInQxNjUiKTsgZG0sIF8sIF8gPSBkb2NfZG8ob3V0X20pCiAgICAgICAgICAgIHRlbjE2NSA9IG5leHQoKHQgZm9yIHQg',
'aW4gZG0gaWYgdC5zdGFydHN3aXRoKCJ0MTY1IikpLCBOb25lKQogICAgICAgICAgICBseSA9IChkbS5nZXQodGVuMTY1KSBv',
'ciAiIikKICAgICAgICAgICAgZ2hpKCJuN190MTY1IiwgbTE2NSk7IGdoaSgibjdfbHlfZG8iLCBseVs6MjAwXSkKICAgICAg',
'ICAgICAgaW5uKGYiICB0MTY1IHNhdSBkb3QgYmllbjoge20xNjV9IHwge2x5WzoxMTBdfSIpCiAgICAgICAgICAgIGR1bmdf',
'bHlfZG8gPSAiUEFUSCB0IiBpbiBseSBvciAiL3Vzci9iaW4iIGluIGx5CiAgICAgICAgICAgIGtldCgiTjcgZG90IGJpZW4g',
'bmhhbmggV2luZG93cyIsIERBVCBpZiAobTE2NSA9PSAiRE8iIGFuZCBkdW5nX2x5X2RvKSBlbHNlCiAgICAgICAgICAgICAg',
'ICAoVFJVT1QgaWYgbTE2NSA9PSAiRE8iIGVsc2UgS0REKSwKICAgICAgICAgICAgICAgICJnaWV0IGR1bmcgbHkgZG8iIGlm',
'IChtMTY1ID09ICJETyIgYW5kIGR1bmdfbHlfZG8pCiAgICAgICAgICAgICAgICBlbHNlICgiRE8gbmh1bmcgS0hPTkcgZHVu',
'ZyBseSBkbyAtPiB0aW4gZHVuZyBnaWEiIGlmIG0xNjUgPT0gIkRPIiBlbHNlICJraG9uZyBkb2MgZHVvYyB0MTY1IikpCgoj',
'IC0tLS0tLS0tLS0tLS0tLS0gS0VUIExVQU4gLS0tLS0tLS0tLS0tLS0tLQppbm4oIiIpOyBpbm4oIj0iICogNzgpCmlubihm',
'IlRIRSBIRSBETyBEVU9DOiB7dGhlX2hlfSAgIEhFQUQ9e2hlYWRbOjEyXX0iKQppZiB0aGVfaGUgPT0gImcxIjoKICAgIGlu',
'bigiTFVVIFk6IGRheSBsYSBORU4gRE8gKGcxKSwgS0hPTkcgcGhhaSBuZ2hpZW0gdGh1IGcyLiBDYWMgY2hvdCBOOC1OMTIg',
'ZHVvaSBkYXkiKQogICAgaW5uKCIgICAgICAgVFJVT1QgbGEgRFVORyBOSFUgTU9ORyDigJQgY2h1bmcgbGEgbmh1bmcgbG8g',
'ZzIgc2luaCByYSBkZSB2w6EuIikKaW5uKCItIiAqIDc4KQpmb3IgdGVuLCB0dCwgY3QgaW4gY2hvdDoKICAgIGlubihmIiAg',
'e3R0OjE0fSB7dGVufSIgKyAoZiIgICB7Y3R9IiBpZiBjdCBlbHNlICIiKSkKbl9rZGQgPSBzdW0oMSBmb3IgXywgdCwgXyBp',
'biBjaG90IGlmIHQgPT0gS0REKQpuX3RydW90ID0gc3VtKDEgZm9yIF8sIHQsIF8gaW4gY2hvdCBpZiB0ID09IFRSVU9UKQpp',
'bm4oIi0iICogNzgpCmlubihmIiAgREFUIHtzdW0oMSBmb3IgXyx0LF8gaW4gY2hvdCBpZiB0PT1EQVQpfSB8IFRSVU9UIHtu',
'X3RydW90fSB8IEtIT05HIERPIERVT0Mge25fa2RkfSIpCmlubihmIiAgVG9uZyBjYSBkbzoge3NvLmdldCgnc29fY2FfZG8n',
'KX0gfCBkYW5oIHNhY2ggZGF5IGR1OiB7J0NPJyBpZiBzby5nZXQoJ2xpZXRfa2VfZGF5X2R1JykgZWxzZSAnS0hPTkcgRE8g',
'RFVPQyd9IikKaW5uKGYiICBBZG1pbmlzdHJhdG9yOiB7c28uZ2V0KCdxdXllbl9hZG1pbicpfSB8IHN5bWxpbms6IHtzby5n',
'ZXQoJ3N5bWxpbmtfZHVvYycpfSIpCmlubigiIik7IGlubigiLS0tIERBTiBOR1VZRU4gS0hPSSBKU09OIE5BWSBWRSBDSE8g',
'UkVWSUVXRVIgLS0tIikKZ2hpKCJjaG90IiwgW3sidGVuIjogYSwgInRyYW5nX3RoYWkiOiBiLCAiY2hpX3RpZXQiOiBjfSBm',
'b3IgYSwgYiwgYyBpbiBjaG90XSkKaW5uKGpzb24uZHVtcHMoc28sIGVuc3VyZV9hc2NpaT1GYWxzZSwgaW5kZW50PTEsIGRl',
'ZmF1bHQ9c3RyKSkKIyByYzogMCA9IG1vaSBjaG90IERBVCB8IDEgPSBjbyBjaG90IFRSVU9UIHwgMyA9IGNvIGNob3QgS0hP',
'TkcgRE8gRFVPQyAodXUgdGllbiBiYW8gZG9uZykKc3lzLmV4aXQoMyBpZiBuX2tkZCBlbHNlICgxIGlmIG5fdHJ1b3QgZWxz',
'ZSAwKSkK'
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
