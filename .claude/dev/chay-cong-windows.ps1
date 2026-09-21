#Requires -Version 7.0
# ĐÒI pwsh 7, KHÔNG phải Windows PowerShell 5.1 — và đây là phép đo, không phải sở thích:
#   · Quy ước `.ps1` của kho là UTF-8 KHÔNG BOM (đo: don-nhanh.ps1, don-nhanh_test.ps1,
#     deploy-guard.ps1, tl-setup.ps1 — cả bốn đều không BOM, LF). PowerShell 5.1 đọc một tệp
#     không BOM theo ANSI, nên mọi dòng tiếng Việt trong script này sẽ thành rác. Thêm BOM thì
#     phá quy ước của kho; nâng bản pwsh thì không.
#   · `$tt.Kill($true)` (giết cả cây tiến trình, dùng cho hạn giờ) chỉ có từ .NET Core 3.0.
#   · `ci.yml` đã gọi `pwsh -NoProfile -File scripts/don-nhanh_test.ps1`, nên pwsh 7 vốn là
#     giả định sẵn có của kho chứ không phải đòi hỏi mới.
<#
.SYNOPSIS
    Chạy các cổng của kho `tra-luat` trên máy Windows — KHÔNG chạm CI.

.DESCRIPTION
    Script này gương lại các bước của job `gate`, `gate-registry` và `gate-packet-loop`
    trong `.github/workflows/ci.yml`, nhưng chạy TẠI MÁY. Nó KHÔNG gọi
    `workflow_dispatch`, KHÔNG re-run, KHÔNG đẩy gì lên remote, KHÔNG gọi GitHub API.
    Viết ra để tôn chỉ thị `manual_ci_budget: 0` mà vẫn đo được trên nền Windows.

    BA THỨ PHẢI ĐẶT ĐÚNG TRƯỚC KHI ĐO, nếu không cổng sẽ ĐỎ vì máy chứ không vì mã:

      core.autocrlf=false, core.eol=lf   `RELEASE_MANIFEST.json` băm theo LF. Checkout
                                         CRLF làm `release-verify --strict` đỏ hàng loạt
                                         — đỏ THẬT nhưng nguyên nhân là checkout.
      core.abbrev=7                      Ngưỡng L2 của `doc-claims-check` lấy độ dài SHA
                                         viết tắt từ git. Kho đủ lịch sử tự nới lên 8, mà
                                         8 đúng bằng độ dài tiền tố UUID notebook
                                         (`743ed200`, `45739ff7`…) ⇒ 18 tiền tố bị hô
                                         `SHA_NOT_A_COMMIT`. ĐÃ ĐO: abbrev 8 → rc=2;
                                         abbrev 7 → rc=0, cùng một cây.
      UTF-8 ở console                    Nhật ký từng ca in tiếng Việt. Code page 437/1252
                                         làm output thành rác và che mất tên ca đỏ.

.PARAMETER Goc
    Thư mục gốc kho. Mặc định: suy từ vị trí script, rồi tới thư mục hiện hành.

.PARAMETER Muc
    `nhanh`  — bộ cổng cốt lõi (mặc định), đủ để biết một bản vá có làm vỡ gì không.
    `day-du` — gương toàn bộ ba job gate của CI, trừ bước cgroup (chỉ có trên Linux).

.PARAMETER CaiCongCu
    Cài PyYAML/jsonschema/ruff bản GHIM, rồi `actionlint`, `shellcheck`, `rg` bằng chính
    installer của kho. Không có cờ này thì script chỉ ĐO xem công cụ có chưa và báo thiếu.

.PARAMETER ChiTiet
    In toàn bộ output của mọi cổng. Mặc định chỉ in output của cổng ĐỎ.

.PARAMETER HanGiay
    Hạn giờ cho MỘT cổng, tính bằng giây. Mặc định 900. Quá hạn thì cổng bị giết và đếm
    là **TREO** — tức `KHÔNG ĐO ĐƯỢC`, KHÔNG phải `ĐẠT`. Có tham số này vì `don-nhanh_test.ps1`
    dựng kho git thật cho từng ca và đã ĐO ĐƯỢC một lần treo quá 10 phút; một bộ chạy cục bộ
    không được phép treo vô hạn rồi bắt người ngồi đoán.

.PARAMETER AlVer
    Bản ghim của `actionlint`. Mặc định `1.7.7` — đúng bản mà `ci.yml` ghim.

.EXAMPLE
    .\chay-cong-windows.ps1 -CaiCongCu
.EXAMPLE
    .\chay-cong-windows.ps1 -Muc day-du -ChiTiet
#>
[CmdletBinding()]
param(
    [string]$Goc,
    [ValidateSet('nhanh', 'day-du')]
    [string]$Muc = 'nhanh',
    [switch]$CaiCongCu,
    [switch]$ChiTiet,
    [int]$HanGiay = 900,
    [string]$AlVer = '1.7.7'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'   # CỐ Ý: cổng đỏ là DỮ LIỆU, không phải sự cố script.

# ───────────────────────────── tiện ích in ─────────────────────────────
function Noi   { param($s) Write-Host $s }
function Tieu  { param($s) Write-Host ''; Write-Host "── $s " -ForegroundColor Cyan }
function Canh  { param($s) Write-Host "CẢNH BÁO: $s" -ForegroundColor Yellow }
function Loi   { param($s) Write-Host "LỖI: $s" -ForegroundColor Red }

# ───────────────────────────── UTF-8 ─────────────────────────────
try {
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    $OutputEncoding = [System.Text.UTF8Encoding]::new($false)
} catch { Canh "không đặt được console UTF-8: $($_.Exception.Message)" }
$env:PYTHONUTF8           = '1'
$env:PYTHONIOENCODING     = 'utf-8'
$env:PYTHONUNBUFFERED     = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'

# ───────────────────────────── gốc kho ─────────────────────────────
if (-not $Goc) {
    $Goc = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
}
$Goc = (Resolve-Path -LiteralPath $Goc).Path
while ($Goc -and -not (Test-Path (Join-Path $Goc (Join-Path 'ops' 'lease_publish_test.py')))) {
    $cha = Split-Path -Parent $Goc
    if ($cha -eq $Goc -or -not $cha) { break }
    $Goc = $cha
}
if (-not (Test-Path (Join-Path $Goc (Join-Path 'ops' 'lease_publish_test.py')))) {
    Loi "không tìm thấy gốc kho tra-luat (thiếu ops\lease_publish_test.py). Dùng -Goc <đường dẫn>."
    exit 2
}
Set-Location -LiteralPath $Goc
Noi "gốc kho: $Goc"

$NhatKy = Join-Path $Goc '.cong-windows'
New-Item -ItemType Directory -Force -Path $NhatKy | Out-Null

# ───────────────────────────── tìm python ─────────────────────────────
function Tim-Python {
    # KHÔNG dùng mảng lồng: PowerShell LÀM PHẲNG `@(@('py',@('-3.12')))` thành
    # `@('py','-3.12')`, và khi ấy `@dau` splat một CHUỖI chứ không phải mảng.
    $ungVien = @(
        [pscustomobject]@{ Ten = 'py';      Dau = @('-3.12') },
        [pscustomobject]@{ Ten = 'py';      Dau = @('-3')    },
        [pscustomobject]@{ Ten = 'python';  Dau = @()        },
        [pscustomobject]@{ Ten = 'python3'; Dau = @()        }
    )
    foreach ($u in $ungVien) {
        if (Get-Command $u.Ten -ErrorAction SilentlyContinue) {
            $d = $u.Dau
            & $u.Ten @d -c "import sys" *> $null
            if ($LASTEXITCODE -eq 0) { return $u }
        }
    }
    return $null
}

$py = Tim-Python
if (-not $py) { Loi 'không tìm thấy Python (py / python / python3).'; exit 3 }
$PyTen = $py.Ten; $PyDau = $py.Dau
$ban = (& $PyTen @PyDau -c "import sys; print('%d.%d.%d' % sys.version_info[:3])")
Noi "python : $PyTen $($PyDau -join ' ') → $ban"
if ($ban -notlike '3.12.*') {
    Canh "CI ghim Python 3.12, máy này $ban. Khác bản thì một cổng đỏ CHƯA chắc là lỗi mã."
}

# ───────────────────────────── tìm bash (Git for Windows) ─────────────────────────────
function Tim-Bash {
    foreach ($n in 'bash.exe', 'bash') {
        $c = Get-Command $n -ErrorAction SilentlyContinue
        if ($c) { return $c.Source }
    }
    foreach ($d in @("$env:ProgramFiles\Git\bin\bash.exe",
                     "${env:ProgramFiles(x86)}\Git\bin\bash.exe",
                     "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe")) {
        if (Test-Path $d) { return $d }
    }
    return $null
}
$Bash = Tim-Bash
if ($Bash) { Noi "bash   : $Bash" } else { Canh 'không có bash.exe — các cổng chạy qua Git Bash sẽ bị BỎ QUA (đếm là KHÔNG ĐO ĐƯỢC, không phải ĐẠT).' }

$Pwsh = (Get-Command pwsh -ErrorAction SilentlyContinue)
if (-not $Pwsh) { Canh 'không có pwsh 7 — `don-nhanh_test.ps1` sẽ chạy bằng PowerShell hiện hành.' }

# ───────────────────────────── nếp git cho hash parity ─────────────────────────────
Tieu 'nếp git (bắt buộc cho hash parity)'
$cu = @{}
foreach ($k in 'core.autocrlf', 'core.eol', 'core.abbrev') {
    $v = (& git config --local --get $k 2>$null)
    $cu[$k] = if ($LASTEXITCODE -eq 0) { $v } else { '(chưa đặt)' }
}
& git config --local core.autocrlf false
& git config --local core.eol lf
& git config --local core.abbrev 7
Noi ("  core.autocrlf {0} → false" -f $cu['core.autocrlf'])
Noi ("  core.eol      {0} → lf"    -f $cu['core.eol'])
Noi ("  core.abbrev   {0} → 7"     -f $cu['core.abbrev'])
Noi '  (chỉ đổi --local; khôi phục bằng: git config --local --unset <khoá>)'

# CRLF đã nằm trong CÂY LÀM VIỆC thì đổi config KHÔNG cứu được — phải normalize lại.
$eol = (& git ls-files --eol -- 'ops/*.py' 'scripts/*.py' 2>$null)
$crlf = @($eol | Where-Object { $_ -match '\bw/crlf\b' })
if ($crlf.Count -gt 0) {
    Canh "$($crlf.Count) tệp đang là CRLF trong cây làm việc. `release-verify --strict` SẼ ĐỎ và đó là lỗi checkout, không phải lỗi mã."
    Noi  '  Sửa (LƯU Ý: bỏ mọi thay đổi chưa commit):  git rm --cached -r . ; git reset --hard'
}

# ───────────────────────── worktree phụ: cổng sẽ ĐỎ vì CHỖ ĐỨNG ─────────────────────────
# ĐÃ ĐO: chạy trong một `git worktree` liên kết làm `packet_loop_test.py` đỏ SÁU ca với
# `rc=14`, `ly_do_dung: "workspace la git worktree; dung ban clone doc lap"`. Đó là cổng
# TỪ CHỐI ĐÚNG THIẾT KẾ, không phải mã hỏng. Nói trước, để không ai đi săn một con ma.
$gitDir    = (& git rev-parse --git-dir 2>$null)
$gitCommon = (& git rev-parse --git-common-dir 2>$null)
if ($gitDir -and $gitCommon -and ($gitDir -ne $gitCommon)) {
    Canh 'đây là một git worktree LIÊN KẾT. `packet-loop selftest` sẽ ĐỎ rc=14 vì chỗ đứng, không vì mã.'
    Noi  '  Muốn đo thật thì chạy trong bản clone chính, hoặc `git clone` riêng một bản.'
}

# ───────────────────────────── công cụ ─────────────────────────────
$AlDich = Join-Path ([System.IO.Path]::GetTempPath()) 'actionlint'
if ($CaiCongCu) {
    Tieu 'cài công cụ bản ghim'
    & $PyTen @PyDau -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0 ruff==0.15.15
    if ($LASTEXITCODE -ne 0) { Canh "pip trả rc=$LASTEXITCODE" }
    if ($Bash) {
        $env:AL_VER = $AlVer
        $env:AL_DICH = $AlDich
        & $Bash 'ops/cai_actionlint.sh'
        if ($LASTEXITCODE -ne 0) { Canh "cai_actionlint.sh rc=$LASTEXITCODE" }
        foreach ($t in 'shellcheck', 'rg') {
            & $Bash 'ops/cai_cong_cu.sh' $t
            if ($LASTEXITCODE -ne 0) { Canh "cai_cong_cu.sh $t rc=$LASTEXITCODE" }
        }
    } else {
        Canh 'không có bash — bỏ qua actionlint/shellcheck/rg.'
    }
}
if (Test-Path $AlDich) { $env:PATH = "$AlDich;$env:PATH" }
$env:AL_VER  = $AlVer
$env:AL_DICH = $AlDich

# ───────────────────────────── bộ chạy ─────────────────────────────
$KetQua = New-Object System.Collections.ArrayList

function Chay-Cong {
    <#
      Đọc mã thoát TỪ CHÍNH TIẾN TRÌNH (`$tt.ExitCode`), không qua `$LASTEXITCODE` và
      tuyệt đối không qua `|`: mã thoát của một pipeline là của PIPELINE, không phải của
      tiến trình — đúng cái bẫy "đọc rc qua pipe" mà doctrine của kho cấm.

      Có HẠN GIỜ vì một cổng treo mà không ai giết thì không phải "chưa xong", nó là
      KHÔNG ĐO ĐƯỢC đội lốt "đang chạy".
    #>
    param([string]$Ten, [string]$Tep, [string[]]$DoiSo,
          [int]$Han = 0, [switch]$BoQua, [string]$LyDoBoQua)

    if ($BoQua) {
        Write-Host ("  {0,-42} BỎ QUA — {1}" -f $Ten, $LyDoBoQua) -ForegroundColor Yellow
        [void]$KetQua.Add([pscustomobject]@{ Ten = $Ten; Rc = $null; TrangThai = 'KHÔNG ĐO ĐƯỢC'; NhatKy = '' })
        return
    }
    if ($Han -le 0) { $Han = $HanGiay }

    $nen  = $Ten -replace '[^\w\.-]', '_'
    $fOut = Join-Path $NhatKy ($nen + '.out')
    $fErr = Join-Path $NhatKy ($nen + '.err')

    $thamSo = @{
        FilePath               = $Tep
        WorkingDirectory       = $Goc
        NoNewWindow            = $true
        PassThru               = $true
        RedirectStandardOutput = $fOut
        RedirectStandardError  = $fErr
    }
    if ($DoiSo -and $DoiSo.Count -gt 0) { $thamSo['ArgumentList'] = $DoiSo }

    $t0 = Get-Date
    $tt = Start-Process @thamSo
    $xong = $tt.WaitForExit($Han * 1000)
    $giay = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)

    if (-not $xong) {
        try { $tt.Kill($true) } catch { try { $tt.Kill() } catch { } }
        Write-Host ("  {0,-42} TREO  > {1}s — ĐÃ GIẾT" -f $Ten, $Han) -ForegroundColor Yellow
        [void]$KetQua.Add([pscustomobject]@{ Ten = $Ten; Rc = $null; TrangThai = 'KHÔNG ĐO ĐƯỢC'; NhatKy = $fOut })
        return
    }
    $tt.WaitForExit()
    $rc = $tt.ExitCode

    $tt2 = if ($rc -eq 0) { 'ĐẠT' } else { 'ĐỎ' }
    $mau = if ($rc -eq 0) { 'Green' } else { 'Red' }
    Write-Host ("  {0,-42} rc={1,-4} {2,7}s  {3}" -f $Ten, $rc, $giay, $tt2) -ForegroundColor $mau
    if ($ChiTiet -or $rc -ne 0) {
        foreach ($f in @($fOut, $fErr)) {
            if ((Test-Path $f) -and (Get-Item $f).Length -gt 0) {
                Get-Content -LiteralPath $f -Tail $(if ($ChiTiet) { 10000 } else { 40 }) |
                    ForEach-Object { Noi "      | $_" }
            }
        }
    }
    [void]$KetQua.Add([pscustomobject]@{ Ten = $Ten; Rc = $rc; TrangThai = $tt2; NhatKy = $fOut })
}

function Chay-Py { param([string]$Ten, [string[]]$DoiSo)
    Chay-Cong -Ten $Ten -Tep $PyTen -DoiSo ($PyDau + $DoiSo) }

function Chay-Bash { param([string]$Ten, [string[]]$DoiSo)
    if ($Bash) { Chay-Cong -Ten $Ten -Tep $Bash -DoiSo $DoiSo }
    else { Chay-Cong -Ten $Ten -Tep '' -DoiSo @() -BoQua -LyDoBoQua 'không có bash.exe' } }

# ───────────────────────────── bảng cổng ─────────────────────────────
Tieu ('cổng — mức ' + $Muc)

Chay-Py   'cong_cu kiem-tra'        @('ops/cong_cu.py', 'kiem-tra', '--json')
Chay-Py   'cong_cu_test'            @('ops/cong_cu_test.py')
Chay-Bash 'lease-publish selftest'  @('ops/chay_lease_publish_test.sh')
Chay-Py   'packet-loop selftest'    @('.claude/dev/packet_loop_test.py')
Chay-Py   'registry test'           @('.claude/dev/ci_dang_ky_test.py', '--chay')

$psExe = if ($Pwsh) { $Pwsh.Source } else { (Get-Process -Id $PID).Path }
Chay-Cong -Ten 'don-nhanh selftest (ps1)' -Tep $psExe -Han ([math]::Min($HanGiay, 600)) `
          -DoiSo @('-NoProfile', '-File', 'scripts/don-nhanh_test.ps1')

if ($Muc -eq 'day-du') {
    Tieu 'cổng — phần còn lại của job gate'

    $tl = @('scripts/tl.py', 'scripts/tl_boot.py', 'scripts/gen_instructions.py',
            'scripts/tl_core/__init__.py', 'scripts/tl_core/deterministic.py',
            'scripts/tl_core/jsonio.py', 'scripts/tl_core/workflow.py',
            'scripts/tl_core/release.py', 'scripts/tl_core/live.py',
            'scripts/tl_core/zip_ingest.py', 'scripts/tl_core/ocr.py',
            'scripts/tl_core/chunking.py', 'scripts/tl_core/command_registry.py')
    Chay-Py 'py_compile'               (@('-m', 'py_compile') + $tl)
    Chay-Py 'codex credential selftest' @('.claude/dev/codex_cred_test.py')
    Chay-Py 'bien-nhan v2 selftest'     @('ops/bien_nhan_v2_test.py')
    Chay-Py 'idiom-ba-ten selftest'     @('.claude/dev/idiom_py_test.py')
    Chay-Py 'eol-policy selftest'       @('.githooks/eol_policy_test.py')
    Chay-Py 'pre-push selftest'         @('.githooks/pre_push_test.py')
    Chay-Py 'gate lifecycle selftest'   @('.claude/dev/gate_lifecycle_test.py')
    Chay-Py 'eol-policy survey'         @('.githooks/eol_policy.py', '--all', '--json')
    Chay-Py 'bundled-fragment check'    @('.github/checks/bundle_fragment_check.py', '--json')
    Chay-Py 'gen_instructions selftest' @('scripts/gen_instructions.py', '--selftest')
    Chay-Py 'command-registry unit'     @('scripts/tl_core/command_registry_test.py')
    Chay-Py 'tl selftest'               @('scripts/tl.py', '--selftest')
    Chay-Py 'workflow-audit strict'     @('scripts/tl.py', 'workflow-audit', '--strict', '--json')
    Chay-Py 'golden-test'               @('scripts/tl.py', 'golden-test', '--json')
    Chay-Py 'doc-claims-check strict'   @('scripts/tl.py', 'doc-claims-check', '--strict', '--json')
    Chay-Py 'determinism-audit strict'  @('scripts/tl.py', 'determinism-audit', '--strict', '--json')
    Chay-Py 'ci-phamvi guard'           @('.github/checks/ci_phamvi.py', '--kiem-bam')
    Chay-Py 'ci-phamvi selftest'        @('.github/checks/ci_phamvi_test.py')
    Chay-Py 'release-check full'        @('scripts/tl.py', 'release-check', '--full', '--json')
    Chay-Py 'release-verify strict'     @('scripts/tl.py', 'release-verify', 'RELEASE_MANIFEST.json', '--strict', '--json')
    Chay-Py 'tl_boot smoke'             @('scripts/tl_boot.py', '--version')

    # release-bundle x2 phải cho CÙNG sha256 — đo tất định, không phải đo "chạy được".
    Tieu 'release-bundle x2 cùng SHA-256'
    New-Item -ItemType Directory -Force -Path (Join-Path $Goc 'dist') | Out-Null
    $bamOk = $true
    foreach ($f in 'a', 'b') {
        & $PyTen @PyDau 'scripts/tl.py' 'release-bundle' '--out' "dist/$f.zip" '--json' *> (Join-Path $NhatKy "bundle-$f.log")
        if ($LASTEXITCODE -ne 0) { $bamOk = $false }
    }
    if ($bamOk) {
        $ha = (Get-FileHash -Algorithm SHA256 (Join-Path $Goc (Join-Path 'dist' 'a.zip'))).Hash
        $hb = (Get-FileHash -Algorithm SHA256 (Join-Path $Goc (Join-Path 'dist' 'b.zip'))).Hash
        $bamOk = ($ha -eq $hb)
        Noi "      a=$ha"
        Noi "      b=$hb"
    }
    $rcB = if ($bamOk) { 0 } else { 1 }
    Write-Host ("  {0,-42} rc={1,-4} {2}" -f 'release-bundle tất định', $rcB, $(if ($bamOk) { 'ĐẠT' } else { 'ĐỎ' })) `
        -ForegroundColor $(if ($bamOk) { 'Green' } else { 'Red' })
    [void]$KetQua.Add([pscustomobject]@{ Ten = 'release-bundle tất định'; Rc = $rcB; TrangThai = $(if ($bamOk) { 'ĐẠT' } else { 'ĐỎ' }); NhatKy = '' })

    Noi ''
    Noi 'KHÔNG CHẠY (chỉ có trên Linux runner): "bo ca gate chay TRONG cgroup duoc uy quyen".'
    Noi 'KHÔNG CHẠY (đòi ngữ cảnh pull_request): "PR head contains required EOL base",'
    Noi '            "tl selftest (co bang chung exact-identity)", "release-verify lane WORKER".'
}

# ───────────────────────────── tổng kết ─────────────────────────────
Tieu 'tổng kết'
$do   = @($KetQua | Where-Object { $_.TrangThai -eq 'ĐỎ' })
$khong = @($KetQua | Where-Object { $_.TrangThai -eq 'KHÔNG ĐO ĐƯỢC' })
$dat  = @($KetQua | Where-Object { $_.TrangThai -eq 'ĐẠT' })

Noi ("  ĐẠT {0}   ĐỎ {1}   KHÔNG ĐO ĐƯỢC {2}   (tổng {3})" -f $dat.Count, $do.Count, $khong.Count, $KetQua.Count)
foreach ($r in $do)    { Write-Host ("    ĐỎ            {0}  → {1}" -f $r.Ten, $r.NhatKy) -ForegroundColor Red }
foreach ($r in $khong) { Write-Host ("    KHÔNG ĐO ĐƯỢC {0}" -f $r.Ten) -ForegroundColor Yellow }
Noi ''
Noi "  nhật ký đầy đủ: $NhatKy"
Noi '  BA TRẠNG THÁI, không hai: ĐẠT / ĐỎ / KHÔNG ĐO ĐƯỢC (gồm cả TREO quá hạn).'
Noi '  Một cổng không chạy được'
Noi '  KHÔNG phải một cổng đã đạt — script này không bao giờ đếm nó là xanh.'

if ($do.Count -gt 0)    { exit 1 }
if ($khong.Count -gt 0) { exit 4 }   # rc riêng: phân biệt "có cổng đỏ" với "có cổng không đo được"
exit 0
