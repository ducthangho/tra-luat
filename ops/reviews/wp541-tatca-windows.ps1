# WP541 - MOT TEP DUY NHAT: tu lo cong cu, tu lay kho, tu chay, tu in ket qua.
#
# Chay (mot dong, khong can gi khac):
#     powershell -NoProfile -ExecutionPolicy Bypass -File "wp541-tatca-windows.ps1"
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
    [switch]$ChiGiaiNen,       # chi ghi bo do Python ra dia roi dung (de doc/kiem)
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
$ShaBoDo    = '9979d7452bad13368e0394f9317ee5207e2416ac33ae430048f5a78c6dddd9b5'      # SHA-256 cua bo do Python nhung ben duoi

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
Write-Host 'WP541 - do N7 tren Windows that (mot tep, tu lo moi thu)'
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
$BoDo = Join-Path $Base 'wp541-do-n7-windows.py'
$B64 = @(
'IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIiIiV1A1NDEgLSBQSEVQIERPIE43IFRSRU4gV0lORE9XUyBUSEFUIChiYW4gMzogbGll'
'dCBrZSBIRVQgY2EgZG8pLgoKQ2hheTogIHB5IHdwNTQxLWRvLW43LXdpbmRvd3MucHkgIjx0aHUtbXVjLWtobz4iIFtzaGEtbW9u'
'Z10KCk43IC0gRE9OIFZJIChsdWF0IEwxLCBiYSBsdW90IHJldmlldyBkYSBob2kpOgogIFNvIGRvbmcgdHJvbmcgb3BzL2xlYXNl'
'X3B1Ymxpc2gucHkga2hvcCBEVU5HIGNodW9pICAnaWYgbmVuX3RodWMgPT0gIndpbmRvd3MiOicKICB0cnVvYyA9IDEgID0+IG5o'
'YW5oIGdpYWkgdGhlbyBuZW4gQ09OIE5HVVlFTgogIHNhdSAgID0gMCAgPT4gZGEgdGF0IG5oYW5oIFdpbmRvd3MsIGNhIGRpY2gg'
'UEhBSSBkbwoKRkFJTC1DTE9TRTogbmVuIGRvIHNhaSA9PiBpbiBLSE9OR19ET19EVU9DLCByYyE9MCwgS0hPTkcgaW4ga2V0IGx1'
'YW4gbmFvLgpEb3QgYmllbiBjaGF5IHRyZW4gQkFOIFNBTyBUQU07IGNheSB0aGF0IGtob25nIGJpIGR1bmcgdG9pLgoKVmkgc2Fv'
'IGNvIGJhbiAzOiBiYW4gMiBsb2MgdGVuIGNhIGJhbmcgciIodFxcZCspKF9cXFMqKSIgbmVuIEJPIFNPVCBtb2kgdGVuIGRhbmcK'
'YHQwMmJfLi4uYCwgYHQ1NWFfLi4uYCAoY28gY2h1IGNhaSB0cnVvYyBnYWNoIGR1b2kpIC0gZHVuZyA1IGNhIG5odSB0aGUgdHJv'
'bmcgYm8uCkJhbiAzIGJhdCB0ZW4gREFZIERVIGBcXFMrYCwgZG9pIGNoaWV1IEhBSSBuZ3VvbiBkb2MgbGFwLCB2YSBjb24gZG9p'
'IGNoaWV1IHZvaQpTTyBIT0MgdHUgZG9uZyB0b25nIGtldC4gTGVjaCA9PiBiYW8gS0hPTkdfRE9fRFVPQyBjaG8gcGhhbiBsaWV0'
'IGtlLCBraG9uZyBpbSBsYW5nLgoiIiIKaW1wb3J0IGpzb24sIG9zLCByZSwgc2h1dGlsLCBzdWJwcm9jZXNzLCBzeXMsIHRlbXBm'
'aWxlCmZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAoKb3MuZW52aXJvbi5zZXRkZWZhdWx0KCJQWVRIT05VVEY4IiwgIjEiKQpvcy5l'
'bnZpcm9uLnNldGRlZmF1bHQoIlBZVEhPTklPRU5DT0RJTkciLCAidXRmLTgiKQpmb3IgX2wgaW4gKHN5cy5zdGRvdXQsIHN5cy5z'
'dGRlcnIpOgogICAgdHJ5OiBfbC5yZWNvbmZpZ3VyZShlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiKQogICAgZXhj'
'ZXB0IEV4Y2VwdGlvbjogcGFzcwppZiBzeXMucGxhdGZvcm0gPT0gIndpbjMyIjoKICAgIHRyeToKICAgICAgICBpbXBvcnQgY3R5'
'cGVzCiAgICAgICAgY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5TZXRDb25zb2xlT3V0cHV0Q1AoNjUwMDEpCiAgICAgICAgY3R5cGVz'
'LndpbmRsbC5rZXJuZWwzMi5TZXRDb25zb2xlQ1AoNjUwMDEpCiAgICBleGNlcHQgRXhjZXB0aW9uOiBwYXNzCgpkZWYgaW5uKCpw'
'KToKICAgIHZhbiA9ICIgIi5qb2luKHN0cih4KSBmb3IgeCBpbiBwKQogICAgdHJ5OiBwcmludCh2YW4pCiAgICBleGNlcHQgRXhj'
'ZXB0aW9uOgogICAgICAgIHRyeToKICAgICAgICAgICAgc3lzLnN0ZG91dC5idWZmZXIud3JpdGUodmFuLmVuY29kZSgidXRmLTgi'
'LCAicmVwbGFjZSIpICsgYiJcbiIpOyBzeXMuc3Rkb3V0LmZsdXNoKCkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAgICAg'
'ICAgICBwcmludCh2YW4uZW5jb2RlKCJhc2NpaSIsICJiYWNrc2xhc2hyZXBsYWNlIikuZGVjb2RlKCJhc2NpaSIpKQoKU0hBX01P'
'TkcgPSBzeXMuYXJndlsyXSBpZiBsZW4oc3lzLmFyZ3YpID4gMiBlbHNlICIyZjcwODY5MCIKTUFVID0gJ2lmIG5lbl90aHVjID09'
'ICJ3aW5kb3dzIjonCkNBMTUgPSAidDEyOSB0MTMwIHQxMzEgdDEzMiB0MTMzIHQxMzYgdDEzOCB0MTM5IHQxNDQgdDE0NSB0MTQ2'
'IHQxNDcgdDE0OSB0MTUwIHQxNTEiLnNwbGl0KCkKQ0FNT0kgPSAidDE2NSB0MTY2IHQxNjcgdDE2OCIuc3BsaXQoKQoKIyAtLS0g'
'RG9jIGxvZyBjdWEgYm8gdGVzdC4gVGVuIGNhIGxhIFxTKyBEQVkgRFUsIGtob25nIGdpYSBkaW5oIGRhbmcgc28uIC0tLQojIHJ1'
'bm5lciBpbjogICI+Pj4gdmFvIDx0ZW4+IDx1dGM+IiAvICI8PDwgcmEgPHRlbj4gPGdpYXk+cyBRVUF8RE98Qk9fUVVBIgojICAg'
'ICAgICAgICAgICIhISEgZG8gPHRlbj4gPGx5IGRvPiIgICAgICAgICAgICAobmdheSB0YWkgY2hvLCBBU0NJSSB0aHVhbikKIyAg'
'ICAgICAgICAgICAiICBETyAgPHRlbj46IDxseSBkbz4iICAgICAgICAgICAgKGN1b2kgYm8sIGNodSBETyBjbyBkYXUpCiMgICAg'
'ICAgICAgICAgIiAgQk8gUVVBIDx0ZW4+OiA8bHkgZG8+IiAgICAgICAgIChjdW9pIGJvLCBjaHUgQk8gY28gZGF1KQpSWF9SQSAg'
'ICAgID0gcmUuY29tcGlsZShyIig/bSlePDw8IHJhIChcUyspIFswLTkuXStzIChcdyspXHMqJCIpClJYX0RPX0NITyAgPSByZS5j'
'b21waWxlKHIiKD9tKV4hISEgZG8gKFxTKykgKC4qKSQiKQojIFRpZW4gdG8gY28gZGF1OiBraG9hbiBkdW5nIGNobyBjYSBraGkg'
'Y29uc29sZSBsYW0gaG9uZyBieXRlIC0+IFxTezEsNH0gKyBEVU5HIGhhaSBraG9hbmcgdHJhbmcuCiMgRG9uZyAiQk8gUVVBIiBj'
'aGkgY28gTU9UIGtob2FuZyB0cmFuZyBzYXUgdHUgZGF1IG5lbiBraG9uZyBsb3QgdmFvIGRheS4KUlhfRE9fQ1VPSSA9IHJlLmNv'
'bXBpbGUociIoP20pXiB7Mn0oXFN7MSw0fSkgezJ9KFxTKyk6ICguKikkIikKUlhfQk9fUVVBICA9IHJlLmNvbXBpbGUociIoP20p'
'XiB7Mn1cU3sxLDZ9IFFVQSAoXFMrKTogKC4qKSQiKQpSWF9UT05HICAgID0gcmUuY29tcGlsZShyImxlYXNlX3B1Ymxpc2g6IChc'
'ZCspLyhcZCspXGJbXlxuXSo/PShcZCspLFteXG5dKj89KFxkKykiKQoKIyBMb3AgbG9pOiBtb2kgbG9wIG1vdCBjYWNoIGNodWEg'
'S0hBQyBOSEFVIC0gZHVuZyBnb3AuCkxPUCA9IFsKICAgICgiUEFUSC1UT0ktVEhJRVUiLCByZS5jb21waWxlKHIiUEFUSCB0W+G7'
'kW9daSB0aGlb4buDZV11fC91c3IvYmluIikpLAogICAgKCJRVVlFTi1TWU1MSU5LIiwgIHJlLmNvbXBpbGUociJXaW5FcnJvciAx'
'MzE0fHJlcXVpcmVkIHByaXZpbGVnZSIpKSwKICAgICgiUVVZRU4tVFJVWS1DQVAiLCByZS5jb21waWxlKHIiV2luRXJyb3IgNVxi'
'fEFjY2VzcyBpcyBkZW5pZWQiKSksCiAgICAoIktIT05HLVBIQUktRVhFIiwgcmUuY29tcGlsZShyIldpbkVycm9yIDE5M3xub3Qg'
'YSB2YWxpZCBXaW4zMiIpKSwKICAgICgiVEhJRVUtQ09ORy1DVSIsICByZS5jb21waWxlKHIiS0hbw5RPXU5HIFvEkERdTyBbxJBE'
'XVvGr1VdW+G7ok9dQzogdGhpW+G6v2VddSIpKSwKICAgICgiVVRGOC1QT0xJQ1kiLCAgICByZS5jb21waWxlKHIia2hbw7RvXW5n'
'IHBoW+G6o2FdaSBVVEYtOCIpKSwKXQpkZWYgbG9wX2N1YShseSk6CiAgICBmb3IgdGVuLCByeCBpbiBMT1A6CiAgICAgICAgaWYg'
'cnguc2VhcmNoKGx5KTogcmV0dXJuIHRlbgogICAgcmV0dXJuICJLSEFDIgoKZGVmIHNvX2NhKHRlbik6CiAgICAiIiJLaG9hIHNv'
'IGRlIHNhcCB4ZXA7IGdpdSB0ZW4gZGF5IGR1IGxhbSBkYW5oIHRpbmguIiIiCiAgICBtID0gcmUubWF0Y2gociJ0KFxkKykiLCB0'
'ZW4pCiAgICByZXR1cm4gKGludChtLmdyb3VwKDEpKSBpZiBtIGVsc2UgMTAqKjYsIHRlbikKCmRlZiBkb2NfZG8ob3V0KToKICAg'
'ICIiIkhFVCBjYSBkbywgZG9jIEhBSSBuZ3VvbiBkb2MgbGFwIHJvaSBkb2kgY2hpZXUgdm9pIHNvIGhvYy4KCiAgICBUcmEgKGx5'
'X2RvX3RoZW9fdGVuLCBnaGlfY2h1X2RvaV9jaGlldSwgZGF0X3Rpbl9jYXkpLgogICAgIiIiCiAgICB0YWlfY2hvID0ge3Q6IGx5'
'LnN0cmlwKCkgZm9yIHQsIGx5IGluIFJYX0RPX0NITy5maW5kYWxsKG91dCl9CiAgICBibyA9IHt0IGZvciB0LCBfIGluIFJYX0JP'
'X1FVQS5maW5kYWxsKG91dCl9CiAgICBjdW9pID0ge3Q6IGx5LnN0cmlwKCkgZm9yIF8sIHQsIGx5IGluIFJYX0RPX0NVT0kuZmlu'
'ZGFsbChvdXQpIGlmIHQgbm90IGluIGJvfQogICAgaG9wID0gZGljdChjdW9pKTsgaG9wLnVwZGF0ZSh0YWlfY2hvKSAgICAgICMg'
'dGFpX2NobyBsYSBuZ3VvbiBBU0NJSSwgdXUgdGllbgogICAgZm9yIHQgaW4gY3VvaToKICAgICAgICBob3Auc2V0ZGVmYXVsdCh0'
'LCBjdW9pW3RdKQogICAgZ2hpX2NodSwgdGluID0gW10sIFRydWUKICAgIGlmIHNldCh0YWlfY2hvKSAhPSBzZXQoY3VvaSk6CiAg'
'ICAgICAgZ2hpX2NodS5hcHBlbmQoZiJoYWkgbmd1b24gTEVDSDogY2hpLXRhaS1jaG89e3NvcnRlZChzZXQodGFpX2Nobyktc2V0'
'KGN1b2kpKX0gIgogICAgICAgICAgICAgICAgICAgICAgIGYiY2hpLWN1b2ktYm89e3NvcnRlZChzZXQoY3VvaSktc2V0KHRhaV9j'
'aG8pKX0iKQogICAgICAgIHRpbiA9IEZhbHNlCiAgICBtID0gUlhfVE9ORy5zZWFyY2gob3V0KQogICAgaWYgbm90IG06CiAgICAg'
'ICAgZ2hpX2NodS5hcHBlbmQoIktIT05HIGRvYyBkdW9jIGRvbmcgdG9uZyBrZXQgLT4ga2hvbmcgZG9pIGNoaWV1IGR1b2Mgc28g'
'aG9jIik7IHRpbiA9IEZhbHNlCiAgICBlbHNlOgogICAgICAgIGRhdCwgdHJlbiA9IGludChtLmdyb3VwKDEpKSwgaW50KG0uZ3Jv'
'dXAoMikpCiAgICAgICAgZG9fdGhlb19zb19ob2MgPSB0cmVuIC0gZGF0CiAgICAgICAgZ2hpX2NodS5hcHBlbmQoZiJzbyBob2M6'
'IHt0cmVufS17ZGF0fT17ZG9fdGhlb19zb19ob2N9IGRvOyBkb2MgZHVvYyB7bGVuKGhvcCl9IikKICAgICAgICBpZiBkb190aGVv'
'X3NvX2hvYyAhPSBsZW4oaG9wKToKICAgICAgICAgICAgZ2hpX2NodS5hcHBlbmQoZiJMRUNIIFNPIEhPQzogdGhpZXUge2RvX3Ro'
'ZW9fc29faG9jIC0gbGVuKGhvcCl9IGNhIC0+IGRhbmggc2FjaCBLSE9ORyBkYXkgZHUiKQogICAgICAgICAgICB0aW4gPSBGYWxz'
'ZQogICAgcmV0dXJuIGhvcCwgZ2hpX2NodSwgdGluCgpzbyA9IHt9CmRlZiBnaGkoaywgdik6IHNvW2tdID0gdjsgcmV0dXJuIHYK'
'CmRlZiBjaGF5KGFyZ3YsIGN3ZCwgcGh1dD00NSk6CiAgICBtdCA9IGRpY3Qob3MuZW52aXJvbiwgUFlUSE9OVVRGOD0iMSIsIFBZ'
'VEhPTklPRU5DT0RJTkc9InV0Zi04IiwgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9IjEiKQogICAgcCA9IHN1YnByb2Nlc3MucnVu'
'KFtzeXMuZXhlY3V0YWJsZV0gKyBhcmd2LCBjd2Q9c3RyKGN3ZCksIGNhcHR1cmVfb3V0cHV0PVRydWUsCiAgICAgICAgICAgICAg'
'ICAgICAgICAgdGV4dD1UcnVlLCBlbmNvZGluZz0idXRmLTgiLCBlcnJvcnM9InJlcGxhY2UiLCB0aW1lb3V0PXBodXQqNjAsIGVu'
'dj1tdCkKICAgIHJldHVybiBwLnJldHVybmNvZGUsIChwLnN0ZG91dCBvciAiIikgKyAocC5zdGRlcnIgb3IgIiIpCgpkZWYgbWF1'
'X2NhKG91dCwgdCk6CiAgICAiIiJUcmFuZyB0aGFpIGN1YSBjYSBjbyB0aWVuIHRvIHNvIGB0YC4gQmllbiBnaW9pIGBfYCBkZSB0'
'MTUga2hvbmcgbnVvdCB0MTUwLiIiIgogICAgbSA9IHJlLnNlYXJjaChyIig/bSlePDw8IHJhICgiICsgdCArIHIiW2Etel0/X1xT'
'KikgWzAtOS5dK3MgKFx3KylccyokIiwgb3V0KQogICAgcmV0dXJuIG0uZ3JvdXAoMikgaWYgbSBlbHNlIE5vbmUKCmRlZiB0ZW5f'
'ZGF5X2R1KG91dCwgdCk6CiAgICBtID0gcmUuc2VhcmNoKHIiKD9tKV48PDwgcmEgKCIgKyB0ICsgciJbYS16XT9fXFMqKSAiLCBv'
'dXQpCiAgICByZXR1cm4gbS5ncm91cCgxKSBpZiBtIGVsc2UgTm9uZQoKIyAtLS0tLS0tLS0tIFRVIEtJRU0gQk8gRE9DIChjaGF5'
'IHRyb25nIG1vaSBsdW90LCB0cmVuIG1hdSBjbyBzYW4pIC0tLS0tLS0tLS0KX01BVSA9ICgKICAgICI+Pj4gdmFvIHQwMmJfdGVu'
'X0tIT05HX0NPX1RIQU1fUVVZRU5fYmlfQ0hBTiAyMDI2LTA5LTE4VDAwOjAwOjAwWlxuIgogICAgIjw8PCByYSB0MDJiX3Rlbl9L'
'SE9OR19DT19USEFNX1FVWUVOX2JpX0NIQU4gMC4wMTBzIERPXG4iCiAgICAiISEhIGRvIHQwMmJfdGVuX0tIT05HX0NPX1RIQU1f'
'UVVZRU5fYmlfQ0hBTiBsb2kgZ2lhIGRpbmggQVxuIgogICAgIj4+PiB2YW8gdDE1MF9yZXZpZXcyX0YxMF9uZ3Vvbl9raG9uZ191'
'dGY4IDIwMjYtMDktMThUMDA6MDA6MDFaXG4iCiAgICAiPDw8IHJhIHQxNTBfcmV2aWV3Ml9GMTBfbmd1b25fa2hvbmdfdXRmOCAw'
'LjAyMHMgRE9cbiIKICAgICIhISEgZG8gdDE1MF9yZXZpZXcyX0YxMF9uZ3Vvbl9raG9uZ191dGY4IFRyYWNlYmFjayBXaW5FcnJv'
'ciAxMzE0IHJlcXVpcmVkIHByaXZpbGVnZVxuIgogICAgIj4+PiB2YW8gdDEzMV9TOF90YW1fdHJhbiAyMDI2LTA5LTE4VDAwOjAw'
'OjAyWlxuIgogICAgIjw8PCByYSB0MTMxX1M4X3RhbV90cmFuIDAuMDMwcyBCT19RVUFcbiIKICAgICIgIELhu44gUVVBIHQxMzFf'
'UzhfdGFtX3RyYW46IG5lbiBmaXh0dXJlXG4iCiAgICAiICDEkOG7jiAgdDAyYl90ZW5fS0hPTkdfQ09fVEhBTV9RVVlFTl9iaV9D'
'SEFOOiBsb2kgZ2lhIGRpbmggQVxuIgogICAgIiAgxJDhu44gIHQxNTBfcmV2aWV3Ml9GMTBfbmd1b25fa2hvbmdfdXRmODogVHJh'
'Y2ViYWNrIFdpbkVycm9yIDEzMTQgcmVxdWlyZWQgcHJpdmlsZWdlXG4iCiAgICAibGVhc2VfcHVibGlzaDogMS8zIMSR4bqhdDsg'
'xJHDoyBjaOG6oXk9MywgYuG7jyBxdWE9MVxuIgopCmRlZiB0dV9raWVtKCk6CiAgICBkbywgZ2MsIHRpbiA9IGRvY19kbyhfTUFV'
'KQogICAga2llbSA9IFsKICAgICAgICAoImJhdCBkdSAyIGNhIGRvIiwgbGVuKGRvKSA9PSAyKSwKICAgICAgICAoImJhdCB0ZW4g'
'Y28gY2h1IGNhaSAodDAyYikiLCBhbnkodC5zdGFydHN3aXRoKCJ0MDJiIikgZm9yIHQgaW4gZG8pKSwKICAgICAgICAoIktIT05H'
'IGRlbSBjYSBCTyBRVUEgbGEgZG8iLCBub3QgYW55KHQuc3RhcnRzd2l0aCgidDEzMSIpIGZvciB0IGluIGRvKSksCiAgICAgICAg'
'KCJkb2kgY2hpZXUgc28gaG9jIERBVCIsIHRpbiksCiAgICAgICAgKCJsb3AgbG9pIFFVWUVOLVNZTUxJTksiLCBsb3BfY3VhKGRv'
'W1t0IGZvciB0IGluIGRvIGlmIHQuc3RhcnRzd2l0aCgndDE1MCcpXVswXV0pID09ICJRVVlFTi1TWU1MSU5LIiksCiAgICAgICAg'
'KCJtYXVfY2EgZG9jIGR1bmciLCBtYXVfY2EoX01BVSwgInQxNTAiKSA9PSAiRE8iKSwKICAgICAgICAoInQxNSBLSE9ORyBudW90'
'IHQxNTAiLCBtYXVfY2EoX01BVSwgInQxNSIpIGlzIE5vbmUpLAogICAgICAgICgiYm8gcXVhIGRvYyBkdW5nIiwgW3QgZm9yIHQs'
'IF8gaW4gUlhfQk9fUVVBLmZpbmRhbGwoX01BVSldID09IFsidDEzMV9TOF90YW1fdHJhbiJdKSwKICAgIF0KICAgIHJldHVybiBr'
'aWVtCgppbm4oIj0iICogNzgpOyBpbm4oIldQNTQxIC0gZG8gTjcgdHJlbiBXaW5kb3dzIHRoYXQgKGJhbiAzOiBsaWV0IGtlIEhF'
'VCBjYSBkbykiKTsgaW5uKCI9IiAqIDc4KQppbm4oIlR1IGtpZW0gYm8gZG9jIGxvZzoiKQpfaG9uZyA9IFt0IGZvciB0LCBrIGlu'
'IHR1X2tpZW0oKSBpZiBub3Qga10KZm9yIHQsIGsgaW4gdHVfa2llbSgpOiBpbm4oZiIgICBbeydEQVQgJyBpZiBrIGVsc2UgJ1RS'
'VU9UJ31dIHt0fSIpCmlmIF9ob25nOgogICAgaW5uKCIiKTsgaW5uKCJLSE9OR19ET19EVU9DOiBibyBkb2MgbG9nIGN1YSBjaGlu'
'aCBzY3JpcHQgbmF5IHNhaSAtPiBraG9uZyBkbyBnaSBjYS4iKQogICAgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLSAwLiBORU4g'
'RE8gLS0tLS0tLS0tLQpnb2MgPSBQYXRoKHN5cy5hcmd2WzFdKS5yZXNvbHZlKCkgaWYgbGVuKHN5cy5hcmd2KSA+IDEgZWxzZSBQ'
'YXRoLmN3ZCgpCmlmIG5vdCAoZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaC5weSIpLmlzX2ZpbGUoKToKICAgIGcyID0gUGF0'
'aChfX2ZpbGVfXykucmVzb2x2ZSgpLnBhcmVudAogICAgZm9yIHVuZyBpbiAoZzIsIGcyLnBhcmVudCwgZzIucGFyZW50LnBhcmVu'
'dCk6CiAgICAgICAgaWYgKHVuZyAvICJvcHMiIC8gImxlYXNlX3B1Ymxpc2gucHkiKS5pc19maWxlKCk6IGdvYyA9IHVuZzsgYnJl'
'YWsKdGVwID0gZ29jIC8gIm9wcyIgLyAibGVhc2VfcHVibGlzaC5weSIKCmxvaSA9IFtdCmlubigiIik7IGlubigic3lzLnBsYXRm'
'b3JtICA6Iiwgc3lzLnBsYXRmb3JtKQppbm4oInB5dGhvbiAgICAgICAgOiIsIHN5cy52ZXJzaW9uLnNwbGl0KClbMF0pCmlubigi'
'b3MucGF0aHNlcCAgICA6IiwgcmVwcihvcy5wYXRoc2VwKSkKaW5uKCJQQVRIRVhUICAgICAgIDoiLCByZXByKG9zLmVudmlyb24u'
'Z2V0KCJQQVRIRVhUIikpKQppbm4oIlByb2dyYW1GaWxlcyAgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIlByb2dyYW1GaWxlcyIp'
'KSkKaW5uKCJTeXN0ZW1Sb290ICAgIDoiLCByZXByKG9zLmVudmlyb24uZ2V0KCJTeXN0ZW1Sb290IikpKQppbm4oIkNPTkdfQ1Vf'
'R0lUICAgOiIsIHJlcHIob3MuZW52aXJvbi5nZXQoIkNPTkdfQ1VfR0lUIikpKQppbm4oImdvYyBraG8gICAgICAgOiIsIGdvYykK'
'CiMgLS0tIFF1eWVuOiBETyBUSEFORywga2hvbmcgaG9pIHJlZ2lzdHJ5IHJvaSBkb2FuIC0tLQpxdXllbl9hZG1pbiA9IE5vbmUK'
'aWYgc3lzLnBsYXRmb3JtID09ICJ3aW4zMiI6CiAgICB0cnk6CiAgICAgICAgaW1wb3J0IGN0eXBlcwogICAgICAgIHF1eWVuX2Fk'
'bWluID0gYm9vbChjdHlwZXMud2luZGxsLnNoZWxsMzIuSXNVc2VyQW5BZG1pbigpKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAg'
'ICAgICBxdXllbl9hZG1pbiA9IE5vbmUKZ2hpKCJxdXllbl9hZG1pbiIsIHF1eWVuX2FkbWluKQppbm4oImNoYXkgdm9pIHF1eWVu'
'IEFkbWluaXN0cmF0b3IgOiIsIHF1eWVuX2FkbWluKQoKc3ltbGlua19kdW9jID0gTm9uZQp0cnk6CiAgICB3aXRoIHRlbXBmaWxl'
'LlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIHQ6CiAgICAgICAgZGljaCA9IFBhdGgodCkgLyAiZGljaC50eHQiOyBkaWNoLndyaXRl'
'X3RleHQoIngiLCBlbmNvZGluZz0idXRmLTgiKQogICAgICAgIHRyeToKICAgICAgICAgICAgb3Muc3ltbGluayhzdHIoZGljaCks'
'IHN0cihQYXRoKHQpIC8gImxrIikpCiAgICAgICAgICAgIHN5bWxpbmtfZHVvYyA9IFRydWUKICAgICAgICBleGNlcHQgT1NFcnJv'
'ciBhcyBlOgogICAgICAgICAgICBzeW1saW5rX2R1b2MgPSBGYWxzZQogICAgICAgICAgICBnaGkoInN5bWxpbmtfbG9pIiwgZiJ7'
'dHlwZShlKS5fX25hbWVfX306IHtlfSIpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgIGdoaSgic3ltbGlua19sb2kiLCBmInt0'
'eXBlKGUpLl9fbmFtZV9ffToge2V9IikKZ2hpKCJzeW1saW5rX2R1b2MiLCBzeW1saW5rX2R1b2MpCmlubigidGFvIHN5bWxpbmsg'
'ZHVvYyAgICAgICAgICAgIDoiLCBzeW1saW5rX2R1b2MsCiAgICAiIiBpZiBzeW1saW5rX2R1b2MgZWxzZSBmIiAgKHtzby5nZXQo'
'J3N5bWxpbmtfbG9pJywnJylbOjcwXX0pIikKCmdpdF90aGF0ID0gc2h1dGlsLndoaWNoKCJnaXQiKQppbm4oIndoaWNoKCdnaXQn'
'KSAgOiIsIHJlcHIoZ2l0X3RoYXQpKQppZiBzeXMucGxhdGZvcm0gIT0gIndpbjMyIjogbG9pLmFwcGVuZChmIktIT05HIHBoYWkg'
'V2luZG93cyAoc3lzLnBsYXRmb3JtPXtzeXMucGxhdGZvcm0hcn0pIikKaWYgbm90IHRlcC5pc19maWxlKCk6ICAgICAgbG9pLmFw'
'cGVuZChmImtob25nIHRoYXkge3RlcH0iKQppZiBub3QgZ2l0X3RoYXQ6ICAgICAgICAgICBsb2kuYXBwZW5kKCJraG9uZyBjbyBg'
'Z2l0YCB0cm9uZyBQQVRIIHRodW9uZyIpCnJjLCBvID0gY2hheShbIi1jIiwgImltcG9ydCBzdWJwcm9jZXNzO3ByaW50KHN1YnBy'
'b2Nlc3MucnVuKFsnZ2l0JywncmV2LXBhcnNlJywnLS1zaG9ydCcsJ0hFQUQnXSwiCiAgICAgICAgICAgICAgICAgICAgImNhcHR1'
'cmVfb3V0cHV0PVRydWUsdGV4dD1UcnVlKS5zdGRvdXQuc3RyaXAoKSkiXSwgZ29jLCA1KQpoZWFkID0gKG8uc3RyaXAoKS5zcGxp'
'dGxpbmVzKCkgb3IgWyI/Il0pWy0xXQppbm4oIkhFQUQgICAgICAgICAgOiIsIGhlYWQsIGYiKG1vbmcge1NIQV9NT05HfSkiKQpp'
'ZiBub3QgaGVhZC5zdGFydHN3aXRoKFNIQV9NT05HWzo3XSk6IGxvaS5hcHBlbmQoZiJIRUFEPXtoZWFkfSBraGFjIHtTSEFfTU9O'
'R30iKQoKaWYgbG9pOgogICAgaW5uKCIiKTsgaW5uKCJLSE9OR19ET19EVU9DOiBuZW4gZG8gc2FpLCBLSE9ORyBpbiBrZXQgbHVh'
'biBuYW8uIikKICAgIGZvciB4IGluIGxvaTogaW5uKCIgIC0iLCB4KQogICAgc3lzLmV4aXQoMykKaW5uKCJuZW4gZG86IERBVCIp'
'CgojIC0tLS0tLS0tLS0gMS4gVFJVT0MgLS0tLS0tLS0tLQp0cnVvYyA9IHRlcC5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04Iiku'
'Y291bnQoTUFVKQppbm4oIiIpOyBpbm4oIi0iICogNzgpCmlubigiTjcgLSBET04gVkk6IHNvIGRvbmcga2hvcCBjaHVvaSIsIHJl'
'cHIoTUFVKSkKaW5uKGYiICBUUlVPQyAoY2h1YSBkb3QgYmllbikgPSB7Z2hpKCduN190cnVvYycsIHRydW9jKX0gICBbbW9uZyAx'
'XSIpCmlmIHRydW9jICE9IDE6CiAgICBpbm4oIktIT05HX0RPX0RVT0M6IG1hdSBkb3QgYmllbiBraG9uZyB4dWF0IGhpZW4gZHVu'
'ZyAxIGxhbi4iKTsgc3lzLmV4aXQoMykKCiMgLS0tLS0tLS0tLSAyLiBCTyBURVNUIERBWSBEVSAtLS0tLS0tLS0tCmlubigiIik7'
'IGlubigiLSIgKiA3OCkKaW5uKCJDaGF5IGJvIHRlc3QgZGF5IGR1IHRyZW4gYmFuIHZhICgxMC0zMCBwaHV0KS4uLiIpCnJjX25l'
'biwgb3V0X25lbiA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIGdvYykKaW5uKCIgIHJjID0iLCBnaGkoInJj'
'X2Jhbl92YSIsIHJjX25lbikpCm0gPSBSWF9UT05HLnNlYXJjaChvdXRfbmVuKQppbm4oIiAgdG9uZyBrZXQ6IiwgbS5ncm91cCgw'
'KSBpZiBtIGVsc2UgIihLSE9ORyBkb2MgZHVvYykiKQppZiBtOgogICAgZ2hpKCJkYXQiLCBpbnQobS5ncm91cCgxKSkpOyBnaGko'
'InRyZW4iLCBpbnQobS5ncm91cCgyKSkpCiAgICBnaGkoImRhX2NoYXkiLCBpbnQobS5ncm91cCgzKSkpOyBnaGkoImJvX3F1YV9z'
'byIsIGludChtLmdyb3VwKDQpKSkKCmRvX2hldCwgZ2hpX2NodSwgdGluX2NheSA9IGRvY19kbyhvdXRfbmVuKQpnaGkoInNvX2Nh'
'X2RvIiwgbGVuKGRvX2hldCkpOyBnaGkoImxpZXRfa2VfZGF5X2R1IiwgdGluX2NheSkKaW5uKCIiKTsgaW5uKCIgIC0tLSBkb2kg'
'Y2hpZXUgYm8gZG9jIC0tLSIpCmZvciBnIGluIGdoaV9jaHU6IGlubigiICAgKiIsIGcpCmlmIG5vdCB0aW5fY2F5OgogICAgaW5u'
'KCIgICAhISBLSE9ORyBETyBEVU9DIChkYXkgZHUpOiBkYW5oIHNhY2ggZHVvaSBkYXkgQ08gVEhFIFRISUVVLiBEYW4gY2EgbG9n'
'IHRobyB2ZS4iKQoKaW5uKCIiKTsgaW5uKGYiICA9PT0ge2xlbihkb19oZXQpfSBDQSBETyBkb2MgZHVvYywgcGhhbiBsb2FpIHRo'
'ZW8gTE9QIExPSSA9PT0iKQp0aGVvX2xvcCA9IHt9CmZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICB0aGVv'
'X2xvcC5zZXRkZWZhdWx0KGxvcF9jdWEoZG9faGV0W3RdKSwgW10pLmFwcGVuZCh0KQpmb3IgbHAgaW4gc29ydGVkKHRoZW9fbG9w'
'KToKICAgIGlubihmIiAgIFt7bHB9XSAoe2xlbih0aGVvX2xvcFtscF0pfSkge1t4LnNwbGl0KCdfJylbMF0gZm9yIHggaW4gdGhl'
'b19sb3BbbHBdXX0iKQppbm4oIiIpCmZvciB0IGluIHNvcnRlZChkb19oZXQsIGtleT1zb19jYSk6CiAgICBpbm4oZiIgICB7dC5z'
'cGxpdCgnXycpWzBdOjd9IFt7bG9wX2N1YShkb19oZXRbdF0pOjE0fV0ge3R9IikKICAgIGlubihmIiAgICAgICAgICAge2RvX2hl'
'dFt0XVs6MTYwXX0iKQpnaGkoImRvX3RoZW9fbG9wIiwgdGhlb19sb3ApCmdoaSgiZG9fbHlfZG8iLCB7dDogZG9faGV0W3RdWzoz'
'MDBdIGZvciB0IGluIGRvX2hldH0pCgpicSA9IHNvcnRlZCh7dCBmb3IgdCwgXyBpbiBSWF9CT19RVUEuZmluZGFsbChvdXRfbmVu'
'KX0sIGtleT1zb19jYSkKZ2hpKCJjYV9ib19xdWEiLCBicSkKaW5uKCIiKTsgaW5uKGYiICBjYSBCSSBCTyBRVUEgKHtsZW4oYnEp'
'fSk6IHtbeC5zcGxpdCgnXycpWzBdIGZvciB4IGluIGJxXX0iKQoKaW5uKCIiKTsgaW5uKCIgIDE1IGNhIFRVTkcgRE8gdHJlbiBD'
'SToiKQpiMTUgPSB7fQpmb3IgdCBpbiBDQTE1OgogICAgdHQgPSB0ZW5fZGF5X2R1KG91dF9uZW4sIHQpOyB0ciA9IG1hdV9jYShv'
'dXRfbmVuLCB0KTsgYjE1W3RdID0gdHIKICAgIGxwID0gZiIgW3tsb3BfY3VhKGRvX2hldFt0dF0pfV0iIGlmIHR0IGluIGRvX2hl'
'dCBlbHNlICIiCiAgICBpbm4oZiIgICAgIHt0fToge3RyfXtscH0iKQpnaGkoImNhMTUiLCBiMTUpCmlubihmIiAgPT4gY29uIERP'
'OiB7W3QgZm9yIHQgaW4gQ0ExNSBpZiBiMTVbdF0gPT0gJ0RPJ119IikKCmlubigiIik7IGlubigiICA0IGNhIE1PSSAoTjEtTjQg'
'Y3VhIGJhbiB2YSk6IikKYjQgPSB7dDogbWF1X2NhKG91dF9uZW4sIHQpIGZvciB0IGluIENBTU9JfTsgZ2hpKCJjYV9tb2kiLCBi'
'NCkKZm9yIHQgaW4gQ0FNT0k6IGlubihmIiAgICAge3R9OiB7YjRbdF19IikKCiMgLS0tLS0tLS0tLSAzLiBQUk9CRSBUSFVDIFRF'
'IC0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCJQcm9iZSB0aHVjIHRlIChraG9uZyBxdWEgdGhhbSBzbyB0'
'aWVtKToiKQpzeXMucGF0aC5pbnNlcnQoMCwgc3RyKGdvYykpCmltcG9ydCBpbXBvcnRsaWIudXRpbApzcGVjID0gaW1wb3J0bGli'
'LnV0aWwuc3BlY19mcm9tX2ZpbGVfbG9jYXRpb24oImxwNTQxIiwgc3RyKHRlcCkpCmxwID0gaW1wb3J0bGliLnV0aWwubW9kdWxl'
'X2Zyb21fc3BlYyhzcGVjKTsgc3BlYy5sb2FkZXIuZXhlY19tb2R1bGUobHApCnRyeToKICAgIGR1b25nID0gbHAuX2dpdF9leGVf'
'dG9pX3RoaWV1KCkKICAgIGlubigiICBfZ2l0X2V4ZV90b2lfdGhpZXUoKSAgICAgICAgIC0+IiwgcmVwcihkdW9uZykpCiAgICBn'
'aGkoImdpYWlfdGhhdCIsIGR1b25nKTsgZ2hpKCJnaWFpX3RoYXRfbGFfZXhlIiwgYm9vbChkdW9uZykgYW5kIGR1b25nLmxvd2Vy'
'KCkuZW5kc3dpdGgoIi5leGUiKSkKZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgaW5uKCIgIF9naXRfZXhlX3RvaV90aGlldSgp'
'IE5FTSAgICAgLT4iLCB0eXBlKGUpLl9fbmFtZV9fLCBzdHIoZSlbOjE1MF0pCiAgICBnaGkoImdpYWlfdGhhdCIsIE5vbmUpOyBn'
'aGkoImdpYWlfdGhhdF9sYV9leGUiLCBGYWxzZSkKCndpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMgdG1wOgog'
'ICAgc2hpbSA9IFBhdGgodG1wKS8ic2hpbSI7IHNoaW0ubWtkaXIoKQogICAgZm9yIG4gaW4gKCJnaXQuYmF0IiwiZ2l0LmNtZCIs'
'ImdpdC5weSIpOiAoc2hpbS9uKS53cml0ZV90ZXh0KCJAZWNobyBvZmZcclxuIiwgZW5jb2Rpbmc9InV0Zi04IikKICAgIGN3ZGsg'
'PSBQYXRoKHRtcCkvImN3ZCI7IGN3ZGsubWtkaXIoKTsgcGYgPSBQYXRoKHRtcCkvInBmIjsgcGYubWtkaXIoKQogICAga3EgPSBs'
'cC5fZ2l0X3dpbmRvd3MocGF0aD1zdHIoc2hpbSksIHByb2dyYW1fZmlsZXM9c3RyKHBmKSwgY3dkPXN0cihjd2RrKSkKICAgIGlu'
'bigiICBzaGltLW9ubHkgbyBQQVRIIG5nb2FpIGN3ZCAgIC0+IiwgcmVwcihrcSksICIobW9uZyBOb25lKSIpCiAgICBnaGkoInR1'
'X2Nob2lfc2hpbSIsIGtxIGlzIE5vbmUpCiAgICAoc2hpbS8iZ2l0LmV4ZSIpLndyaXRlX3RleHQoIngiLCBlbmNvZGluZz0idXRm'
'LTgiKQogICAga3EyID0gbHAuX2dpdF93aW5kb3dzKHBhdGg9c3RyKHNoaW0pLCBwcm9ncmFtX2ZpbGVzPXN0cihwZiksIGN3ZD1z'
'dHIoY3dkaykpCiAgICBpbm4oIiAgRE9JIENIVU5HIERVT05HOiB0aGVtIGdpdC5leGUtPiIsIHJlcHIoa3EyKSkKICAgIGdoaSgi'
'ZG9pX2NodW5nX2R1b25nIiwgYm9vbChrcTIpIGFuZCBrcTIubG93ZXIoKS5lbmRzd2l0aCgiZ2l0LmV4ZSIpKQoKIyAtLS0tLS0t'
'LS0tIDQuIE43IC0tLS0tLS0tLS0KaW5uKCIiKTsgaW5uKCItIiAqIDc4KTsgaW5uKCJONyAtIGRvdCBiaWVuIHRyZW4gQkFOIFNB'
'TyBUQU0gKGNheSB0aGF0IEtIT05HIGJpIGR1bmcgdG9pKSIpCndpdGggdGVtcGZpbGUuVGVtcG9yYXJ5RGlyZWN0b3J5KCkgYXMg'
'dG1wOgogICAgc2FvID0gUGF0aCh0bXApLyJjYXkiCiAgICBzaHV0aWwuY29weXRyZWUoZ29jLCBzYW8sIGlnbm9yZT1zaHV0aWwu'
'aWdub3JlX3BhdHRlcm5zKCIuZ2l0IiwiX19weWNhY2hlX18iLCIqLnB5YyIpKQogICAgZjIgPSBzYW8vIm9wcyIvImxlYXNlX3B1'
'Ymxpc2gucHkiCiAgICBmMi53cml0ZV90ZXh0KGYyLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKS5yZXBsYWNlKE1BVSwgImlm'
'IEZhbHNlOiIpLCBlbmNvZGluZz0idXRmLTgiKQogICAgc2F1ID0gZjIucmVhZF90ZXh0KGVuY29kaW5nPSJ1dGYtOCIpLmNvdW50'
'KE1BVSkKICAgIGlubihmIiAgU0FVIChkYSBkb3QgYmllbikgPSB7Z2hpKCduN19zYXUnLCBzYXUpfSAgIFttb25nIDBdIikKICAg'
'IGlmIHNhdSAhPSAwOiBpbm4oIktIT05HX0RPX0RVT0M6IGRvdCBiaWVuIEtIT05HIGFwIGR1b2MuIik7IHN5cy5leGl0KDMpCiAg'
'ICByY19tLCBvdXRfbSA9IGNoYXkoWyJvcHMvbGVhc2VfcHVibGlzaF90ZXN0LnB5Il0sIHNhbykKICAgIG0xNjUgPSBtYXVfY2Eo'
'b3V0X20sICJ0MTY1Iik7IGRtLCBfLCBfID0gZG9jX2RvKG91dF9tKQogICAgdDE2NSA9IHRlbl9kYXlfZHUob3V0X20sICJ0MTY1'
'IikKICAgIGlubigiICByYyBzYXUgZG90IGJpZW4gOiIsIHJjX20pCiAgICBpbm4oIiAgdDE2NSA6IiwgbTE2NSwgInwiLCAoZG0u'
'Z2V0KHQxNjUpIG9yICIiKVs6MTIwXSkKICAgIGdoaSgibjdfdDE2NV9zYXVfZG90X2JpZW4iLCBtMTY1KTsgZ2hpKCJuN19kYXQi'
'LCBtMTY1ID09ICJETyIpCiAgICBnaGkoIm43X3QxNjVfbHlfZG8iLCAoZG0uZ2V0KHQxNjUpIG9yICIiKVs6MjAwXSkKCiMgLS0t'
'LS0tLS0tLSBLRVQgTFVBTiAtLS0tLS0tLS0tCmlubigiIik7IGlubigiPSIgKiA3OCkKb2sgPSAoc28uZ2V0KCJuN190cnVvYyIp'
'PT0xIGFuZCBzby5nZXQoIm43X3NhdSIpPT0wIGFuZCBzby5nZXQoIm43X2RhdCIpCiAgICAgIGFuZCBzby5nZXQoInR1X2Nob2lf'
'c2hpbSIpIGFuZCBzby5nZXQoImRvaV9jaHVuZ19kdW9uZyIpKQppbm4oIk43ICh0cnVvYz0xLCBzYXU9MCwgdDE2NSBETyk6Iiwg'
'IkRBVCIgaWYgc28uZ2V0KCJuN19kYXQiKSBlbHNlICJUUlVPVCIpCmlubigiVHUgY2hvaSBzaGltIG8gUEFUSCB0aGF0ICAgIDoi'
'LCAiREFUIiBpZiBzby5nZXQoInR1X2Nob2lfc2hpbSIpIGVsc2UgIlRSVU9UIikKaW5uKCJEb2kgY2h1bmcgZHVvbmcgICAgICAg'
'ICAgICAgOiIsICJEQVQiIGlmIHNvLmdldCgiZG9pX2NodW5nX2R1b25nIikgZWxzZSAiVFJVT1QiKQppbm4oIlF1eWVuIHN5bWxp'
'bmsgICAgICAgICAgICAgICA6Iiwgc28uZ2V0KCJzeW1saW5rX2R1b2MiKSwgInwgQWRtaW5pc3RyYXRvcjoiLCBzby5nZXQoInF1'
'eWVuX2FkbWluIikpCmlubigiVG9uZyBjYSBkbyAgICAgICAgICAgICAgICAgIDoiLCBzby5nZXQoInNvX2NhX2RvIiksICItPiIs'
'IHtrOiBsZW4odikgZm9yIGssIHYgaW4gdGhlb19sb3AuaXRlbXMoKX0pCmlubigiRGFuaCBzYWNoIGRvIERBWSBEVSAgICAgICAg'
'IDoiLCAiQ08iIGlmIHRpbl9jYXkgZWxzZSAiS0hPTkcgRE8gRFVPQyAtIHhlbSBkb2kgY2hpZXUgbyB0cmVuIikKaW5uKCIiKTsg'
'aW5uKCItLS0gREFOIE5HVVlFTiBLSE9JIEpTT04gTkFZIFZFIENITyBSRVZJRVdFUiAtLS0iKQppbm4oanNvbi5kdW1wcyhzbywg'
'ZW5zdXJlX2FzY2lpPUZhbHNlLCBpbmRlbnQ9MSwgZGVmYXVsdD1zdHIpKQpzeXMuZXhpdCgwIGlmIG9rIGVsc2UgMSkK'
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

Write-Host 'fetch ban va fix_issue_541 ...'
G -C "$Kho" fetch --quiet origin fix_issue_541 | Out-Null
G -C "$Kho" checkout --quiet -B fix_issue_541 FETCH_HEAD | Out-Null
G -C "$Kho" reset --hard --quiet FETCH_HEAD | Out-Null

$head = (G -C "$Kho" rev-parse --short HEAD) | Select-Object -First 1
Write-Host "HEAD : $head  (mong $ShaVa)"
if ("$head" -notlike "$ShaVa*") { Dung "HEAD=$head khac $ShaVa - dang do nham ma" }

# ---------------------------------------------------------------- 5. chay
Tieu 'Chay phep do (bo test chay HAI lan - tinh 20-40 phut)'
Write-Host "log : $Log"
Write-Host ('-' * 70)
& $pyCmd.Source $BoDo $Kho $ShaVa 2>&1 | Tee-Object -FilePath $Log
$rc = $LASTEXITCODE
Write-Host ('-' * 70)

# ---------------------------------------------------------------- 6. ket qua
Write-Host ''
Write-Host "rc = $rc"
switch ($rc) {
    0       { Write-Host 'MOI CHOT DAT'   -ForegroundColor Green }
    1       { Write-Host 'CO CHOT TRUOT'  -ForegroundColor Yellow }
    3       { Write-Host 'KHONG DO DUOC'  -ForegroundColor Red }
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
