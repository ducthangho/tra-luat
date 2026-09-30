#Requires -Version 7.1
# ĐÒI pwsh 7.1+, KHÔNG phải Windows PowerShell 5.1 — và đây là phép đo, không phải sở thích:
#   · Tệp này UTF-8 KHÔNG BOM, LF — theo nhóm `scripts/*.ps1` + `tl-setup.ps1` (5 tệp không BOM).
#     Kho KHÔNG có một quy ước duy nhất: 5/10 tệp `.ps1` có sẵn (`docs/runbooks/**`) CÓ BOM (đo
#     `git ls-tree` + 3 byte đầu). PowerShell 5.1 đọc tệp không BOM theo ANSI ⇒ tiếng Việt thành rác.
#   · `$tt.Kill($true)` (giết cả cây tiến trình, dùng cho hạn giờ) chỉ có từ .NET Core 3.0.
#   · `$tt.WaitForExitAsync()` (xả stdout/stderr CÓ HẠN sau khi cổng thoát) chỉ có từ .NET 5 = pwsh 7.1.
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

    BA NẾP ĐẶT TRƯỚC KHI ĐO để máy chạy giống CI. Cột phải nói điều gì ĐO ĐƯỢC khi thiếu — chỉ
    `core.abbrev` làm cổng ĐỎ vì máy; hai nếp EOL là hàng rào thứ hai, UTF-8 chỉ làm hỏng nhật ký:

      core.autocrlf=false, core.eol=lf   Gương `ci.yml`. `RELEASE_MANIFEST.json` băm theo LF,
                                         nhưng thứ ép LF lúc checkout là `.gitattributes`
                                         (`* text=auto eol=lf`, ADR-0018) — đo: clone với
                                         autocrlf=true ⇒ 0 tệp CRLF ngoài 3 tệp `*.cmd`,
                                         `release-verify --strict` ok. Hai nếp này là hàng
                                         rào THỨ HAI (tệp bị công cụ ghi lại CRLF vẫn đỏ).
      core.abbrev=7                      Ngưỡng L2 của `doc-claims-check` lấy độ dài SHA
                                         viết tắt từ git. Kho đủ lịch sử tự nới lên 8, mà
                                         8 đúng bằng độ dài tiền tố UUID notebook
                                         (`743ed200`, `45739ff7`…) ⇒ tiền tố bị hô
                                         `SHA_NOT_A_COMMIT`. ĐÃ ĐO trên f2392df: abbrev 8 →
                                         rc=2, 5 cờ L2; abbrev 7 → rc=0, cùng một cây.
                                         (Số 18 trong `ci.yml` r226 là số LỊCH SỬ.)
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
    Hạn giờ cho MỘT cổng, tính bằng giây. Mặc định 3600 = `timeout-minutes: 60` của job CI
    (`test registry` đo trên CI Windows ≈ 41 % × 43,2 phút ≈ 1060 s — VƯỢT 900 cũ, nên với hạn cũ
    mức mặc định KHÔNG BAO GIỜ ra ĐẠT được). Quá hạn thì cổng bị giết và đếm
    là **TREO** — tức `KHÔNG ĐO ĐƯỢC`, KHÔNG phải `ĐẠT`. Có tham số này vì `don-nhanh_test.ps1`
    dựng kho git thật cho từng ca và đã ĐO ĐƯỢC một lần treo quá 10 phút; một bộ chạy cục bộ
    không được phép treo vô hạn rồi bắt người ngồi đoán.

.PARAMETER AlVer
    Bản ghim của `actionlint`. Mặc định `1.7.7` — đúng bản mà `ci.yml` ghim.

.EXAMPLE
    pwsh -NoProfile -File .\.claude\dev\chay-cong-windows.ps1 -CaiCongCu
.EXAMPLE
    pwsh -NoProfile -File .\.claude\dev\chay-cong-windows.ps1 -Muc day-du -ChiTiet
.NOTES
    Gọi bằng `pwsh -File` (tiến trình RIÊNG). Script đổi cwd, PATH, PYTHON*, AL_* và
    [Console]::OutputEncoding của tiến trình đang chạy nó; gọi thẳng `.\chay-cong-windows.ps1`
    trong một phiên pwsh thì mọi thay đổi ấy Ở LẠI phiên sau khi script kết thúc.
#>
[CmdletBinding()]
param(
    [string]$Goc,
    [ValidateSet('nhanh', 'day-du')]
    [string]$Muc = 'nhanh',
    [switch]$CaiCongCu,
    [switch]$ChiTiet,
    [ValidateRange(1, 86400)]
    [int]$HanGiay = 3600,
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
while ($Goc -and -not (Test-Path -LiteralPath (Join-Path $Goc (Join-Path 'ops' 'lease_publish_test.py')))) {
    $cha = Split-Path -Parent $Goc
    if ($cha -eq $Goc -or -not $cha) { break }
    $Goc = $cha
}
# `-LiteralPath`: đường dẫn là DỮ LIỆU — kho nằm dưới `…\[x]\…` thì `-Path` coi `[x]` là lớp ký tự
# và không bao giờ thấy gốc (đo: rc=2 kể cả khi truyền `-Goc` đúng).
if (-not (Test-Path -LiteralPath (Join-Path $Goc (Join-Path 'ops' 'lease_publish_test.py')))) {
    Loi "không tìm thấy gốc kho tra-luat (thiếu ops\lease_publish_test.py). Dùng -Goc <đường dẫn>."
    exit 2
}
# Start-Process diễn giải `-WorkingDirectory` và `-RedirectStandard*` như MẪU (đo: gốc chứa `[1]` ⇒
# "Unable to find the specified file" cho MỌI cổng; `[WildcardPattern]::Escape` cứu được thư mục làm việc
# nhưng KHÔNG cứu được tệp chuyển hướng). Nói đúng nguyên nhân thay vì để mọi cổng KHÔNG KHỞI ĐỘNG ĐƯỢC.
if ([WildcardPattern]::ContainsWildcardCharacters($Goc)) {
    Loi "gốc kho '$Goc' chứa ký tự wildcard ([ ] * ?) — Start-Process coi đường dẫn là MẪU nên không cổng nào chạy được. Dời kho sang đường dẫn không có các ký tự ấy."
    exit 2
}
Set-Location -LiteralPath $Goc
Noi "gốc kho: $Goc"

# Nhật ký KHÔNG được nằm trong cây đang đo: `.cong-windows/` ở gốc làm `release-verify --strict`
# hô `extra_files` (đo: 12 tệp sau mức `nhanh`) và `release-bundle` đóng chúng vào zip. `dist/`
# vừa nằm trong `_RELEASE_EXCLUDE_DIRS` vừa bị `.gitignore` — cùng chỗ bước bundle x2 ghi zip.
$NhatKy = Join-Path $Goc (Join-Path 'dist' 'cong-windows')
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
            # CHỨNG MINH là Python bằng ĐẦU RA, không bằng rc: một shim thoát 0 cho mọi lời gọi
            # qua được `-c "import sys"` rồi làm MỌI cổng Python "ĐẠT" mà không chạy gì (đã đo).
            $ra = @(& $u.Ten @d -c "import sys; print('TLPY=%d.%d.%d' % sys.version_info[:3])" 2>$null)
            if ($LASTEXITCODE -eq 0 -and @($ra -match '^TLPY=3\.\d+\.\d+$').Count -gt 0) { return $u }
        }
    }
    return $null
}

$py = Tim-Python
if (-not $py) { Loi 'không tìm thấy Python (py / python / python3).'; exit 3 }
$PyTen = $py.Ten; $PyDau = $py.Dau
$ban = (& $PyTen @PyDau -c "import sys; print('%d.%d.%d' % sys.version_info[:3])")
Noi "python : $PyTen $($PyDau -join ' ') → $ban"
if ([string]$ban -notlike '3.12.*') {   # ép [string]: đầu ra RỖNG làm `-notlike` trả mảng rỗng ⇒ im lặng
    Canh "CI ghim Python 3.12, máy này $ban. Khác bản thì một cổng đỏ CHƯA chắc là lỗi mã."
}

# ───────────────────────────── tìm bash — QUA bộ giải dùng chung ─────────────────────────────
# KHÔNG giải theo TÊN: `bash.exe` đầu PATH trên Windows thường là `C:\Windows\System32\bash.exe`
# (bộ phóng WSL — nuốt argv, chạy NỀN KHÁC). `ops/bash_nen.py` quyết bằng NĂNG LỰC (Issue #570)
# và là chỗ DUY NHẤT được giải bash; rc=3 ⇒ KHÔNG ĐO ĐƯỢC, không đoán.
function Tim-Bash {
    $ra = @(& $PyTen @PyDau 'ops/bash_nen.py' 'tim' 2>$null)
    if ($LASTEXITCODE -ne 0 -or $ra.Count -eq 0) { return $null }
    $d = ([string]$ra[-1]).Trim()
    if ($d -and (Test-Path -LiteralPath $d -PathType Leaf)) { return $d }
    return $null
}
$Bash = Tim-Bash
if ($Bash) { Noi "bash   : $Bash" } else { Canh 'ops/bash_nen.py không tìm được bash LÀM ĐƯỢC VIỆC — các cổng chạy qua bash sẽ bị BỎ QUA (đếm là KHÔNG ĐO ĐƯỢC, không phải ĐẠT).' }

$Pwsh = (Get-Command pwsh -ErrorAction SilentlyContinue)
if (-not $Pwsh) { Canh 'không có pwsh 7 — `don-nhanh_test.ps1` sẽ chạy bằng PowerShell hiện hành.' }

# ───────────────────────────── nếp git cho hash parity ─────────────────────────────
Tieu 'nếp git (bắt buộc cho hash parity)'
# Biến `GIT_CONFIG` (legacy) chỉ tác động lên LỆNH `git config`: có nó thì `--local` ném "only one config file at a time"
# (ghi trượt, rc=129) và `--get` CHỈ đọc tệp ấy, không đọc giá trị mà mọi lệnh git khác dùng (đo: in "→ 7" trong khi
# `rev-parse --short` dài 8). `ci.yml` không đặt biến này — bỏ nó cho tiến trình này và mọi cổng con.
$env:GIT_CONFIG = $null
$cu = @{}
foreach ($k in 'core.autocrlf', 'core.eol', 'core.abbrev') {
    $v = (& git config --local --get $k 2>$null)
    $cu[$k] = if ($LASTEXITCODE -eq 0) { $v } else { '(chưa đặt)' }
}
$muon = [ordered]@{ 'core.autocrlf' = 'false'; 'core.eol' = 'lf'; 'core.abbrev' = '7' }
$nepHong = @()
foreach ($k in $muon.Keys) {
    & git config --local $k $muon[$k]
    # ĐỌC LẠI, đừng tin lời gọi ghi: `.git/config.lock` còn sót ⇒ ghi trượt mà ta vẫn in "→ 7".
    # Và đọc giá trị CÓ HIỆU LỰC (mọi tầng) chứ không đọc lại tầng `--local` vừa ghi: biến
    # `GIT_CONFIG_COUNT/KEY/VALUE`, `--worktree`, `[include]` đè `--local` mà `--local --get` không thấy
    # (đo: in "→ 7" trong khi git dùng 8 ⇒ `doc-claims-check` rc=2, 5 cờ — ĐỎ vì máy mà bị đếm là ĐỎ vì mã).
    $that = (& git config --get $k 2>$null)
    if ($that -ne $muon[$k]) { $nepHong += $k }
    Noi ("  {0,-13} {1} → {2}{3}" -f $k, $cu[$k], $that, $(if ($that -ne $muon[$k]) { '   (KHÔNG ĐẶT ĐƯỢC)' } else { '' }))
    if ($that -ne $muon[$k]) {
        $tang = @(& git config --show-scope --show-origin --get $k 2>$null)
        if ($tang.Count -gt 0) { Noi "      tầng đang thắng: $($tang -join ' ')" }
    }
}
Noi '  (chỉ đổi --local; khôi phục: `git config --local <khoá> <giá trị cũ in bên trái>`, hoặc `--unset` nếu cũ là "(chưa đặt)")'
if ($nepHong.Count -gt 0) {
    Loi ("không đặt được nếp: {0}. Đo trong môi trường sai thì kết quả KHÔNG ĐO ĐƯỢC." -f ($nepHong -join ', '))
    exit 4
}

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
# Dấu phân cách của NỀN (không ghim `;`), và không chèn lặp khi PATH đã có sẵn thư mục ấy.
$SepPath = [IO.Path]::PathSeparator
if ((Test-Path -LiteralPath $AlDich) -and (($env:PATH -split [regex]::Escape($SepPath)) -notcontains $AlDich)) {
    $env:PATH = "$AlDich$SepPath$env:PATH"
}
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
    try { $tt = Start-Process @thamSo -ErrorAction Stop }
    catch {
        # KHÔNG KHỞI ĐỘNG được ≠ TREO: không có gì chạy, không có gì để giết.
        Write-Host ("  {0,-42} KHÔNG KHỞI ĐỘNG ĐƯỢC — {1}" -f $Ten, $_.Exception.Message) -ForegroundColor Yellow
        [void]$KetQua.Add([pscustomobject]@{ Ten = $Ten; Rc = $null; TrangThai = 'KHÔNG ĐO ĐƯỢC'; NhatKy = '' })
        return
    }
    # Giữ handle NGAY: trên Windows, Start-Process chuyển hướng bằng CreateProcess rồi trả `Process` KHÔNG giữ handle, nên
    # sau khi tiến trình thoát `ExitCode`/`WaitForExitAsync` có thể không đọc được (lỗi đã biết; KHÔNG ĐO ĐƯỢC ở Linux).
    try { $null = $tt.Handle } catch { }
    $xong = $tt.WaitForExit($Han * 1000)

    if (-not $xong) {
        try { $tt.Kill($true) } catch { try { $tt.Kill() } catch { } }
        # "Đã gọi lệnh giết" ≠ "đã chết" (CLAUDE.md, tách 124/125): KIỂM LẠI.
        $chet = $false
        try { $chet = $tt.WaitForExit(10000) -and $tt.HasExited } catch { $chet = $false }
        $nhanGiet = if ($chet) { 'ĐÃ GIẾT' } else { 'GIẾT KHÔNG ĐƯỢC — tiến trình CÒN SỐNG, cổng sau có thể bị nhiễu' }
        Write-Host ("  {0,-42} TREO  > {1}s — {2}" -f $Ten, $Han, $nhanGiet) -ForegroundColor Yellow
        [void]$KetQua.Add([pscustomobject]@{ Ten = $Ten; Rc = $null; TrangThai = 'KHÔNG ĐO ĐƯỢC'; NhatKy = $fOut })
        return
    }
    # `WaitForExit()` KHÔNG hạn còn chờ EOF của stdout/stderr, mà Start-Process trên Unix chuyển hướng qua ỐNG
    # (`StartInfo.RedirectStandardOutput=True`): một tiến trình CHÁU còn giữ ống làm nó chờ tới khi cháu chết,
    # vượt `-HanGiay` (đo: cổng thoát sau 0,1 s, cháu ngủ 40 s ⇒ chờ 42 s với HanGiay 5 rồi ĐẠT; cháu sống lâu ⇒
    # treo vô hạn). Xả luồng CÓ HẠN bằng phần hạn còn lại; quá hạn ⇒ cây tiến trình của cổng CHƯA xong ⇒ KHÔNG ĐO ĐƯỢC.
    $rc = $tt.ExitCode
    $conMs = [math]::Max(1000, [int]($Han * 1000 - ((Get-Date) - $t0).TotalMilliseconds))
    $xa = $false
    try { $xa = $tt.WaitForExitAsync([Threading.CancellationToken]::None).Wait($conMs) } catch { $xa = $false }
    if (-not $xa) {
        Write-Host ("  {0,-42} TREO  > {1}s — tiến trình đã thoát rc={2} nhưng CHÁU còn giữ stdout/stderr (CÒN SỐNG — cổng sau có thể bị nhiễu)" -f $Ten, $Han, $rc) -ForegroundColor Yellow
        # rc ĐÃ đọc từ chính tiến trình: rc≠0 là ĐỎ THẬT. Hạ nó xuống KHÔNG ĐO ĐƯỢC là giấu một cổng đỏ (đo: exit 4 thay
        # vì 1, "ĐỎ 0", log của cổng không in). Chỉ rc=0 (hoặc rc không đọc được) mới chưa kết luận được.
        if ($null -eq $rc -or $rc -eq 0) {
            [void]$KetQua.Add([pscustomobject]@{ Ten = $Ten; Rc = $rc; TrangThai = 'KHÔNG ĐO ĐƯỢC'; NhatKy = $fOut })
            return
        }
    }
    # Thời lượng tính TỚI khi xả xong: cổng chưa xong khi script còn chờ cây tiến trình của nó (đo: cháu 3 s ⇒ in "0.2s").
    $giay = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)

    $tt2 = if ($rc -eq 0) { 'ĐẠT' } else { 'ĐỎ' }
    $mau = if ($rc -eq 0) { 'Green' } else { 'Red' }
    Write-Host ("  {0,-42} rc={1,-4} {2,7}s  {3}" -f $Ten, $rc, $giay, $tt2) -ForegroundColor $mau
    if ($ChiTiet -or $rc -ne 0) {
        foreach ($f in @($fOut, $fErr)) {
            if ((Test-Path -LiteralPath $f) -and (Get-Item -LiteralPath $f).Length -gt 0) {
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

# GƯƠNG CẢ `if:` của CI, không chỉ lệnh: `ci.yml` chạy bước này với `if: runner.os != 'Windows'`
# (NỢ CÓ TÊN `don-nhanh-test-chua-chay-duoc-tren-windows`, ops/NO_KY_THUAT.md §10 — bộ test ghim
# PATH POSIX + `gh` giả `#!/bin/sh`). Chạy nó trên Windows là ĐỎ vì NỢ, không vì mã.
if ($IsWindows) {
    Noi '  KHÔNG CHẠY trên Windows (ci.yml cũng không): "don-nhanh selftest" — nợ don-nhanh-test-chua-chay-duoc-tren-windows.'
} else {
    $psExe = if ($Pwsh) { $Pwsh.Source } else { (Get-Process -Id $PID).Path }
    Chay-Cong -Ten 'don-nhanh selftest (ps1)' -Tep $psExe -Han ([math]::Min($HanGiay, 600)) `
              -DoiSo @('-NoProfile', '-File', 'scripts/don-nhanh_test.ps1')
}

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
    # `ci.yml`: `if: runner.os != 'Windows'` — nợ `ci-phamvi-test-chua-chay-duoc-tren-windows` (§20).
    if ($IsWindows) { Noi '  KHÔNG CHẠY trên Windows (ci.yml cũng không): "ci-phamvi selftest".' }
    else { Chay-Py 'ci-phamvi selftest' @('.github/checks/ci_phamvi_test.py') }
    Chay-Py 'release-check full'        @('scripts/tl.py', 'release-check', '--full', '--json')
    Chay-Py 'release-verify strict'     @('scripts/tl.py', 'release-verify', 'RELEASE_MANIFEST.json', '--strict', '--json')
    Chay-Py 'tl_boot smoke'             @('scripts/tl_boot.py', '--version')

    # release-bundle x2 phải cho CÙNG sha256 — đo tất định, không phải đo "chạy được".
    Tieu 'release-bundle x2 cùng SHA-256'
    New-Item -ItemType Directory -Force -Path (Join-Path $Goc 'dist') | Out-Null
    $za = Join-Path $Goc (Join-Path 'dist' 'a.zip')
    $zb = Join-Path $Goc (Join-Path 'dist' 'b.zip')
    # Zip của LƯỢT TRƯỚC còn nằm đó thì "băm khớp" là đo lượt trước — xoá trước khi build, rồi KIỂM
    # LẠI: "đã gọi lệnh xoá" ≠ "đã mất" (tệp bị khoá/bất biến ⇒ xoá trượt im lặng; đo: ĐẠT bằng băm lượt trước).
    Remove-Item -LiteralPath $za, $zb -Force -ErrorAction SilentlyContinue
    $conCu = @(@($za, $zb) | Where-Object { Test-Path -LiteralPath $_ })
    # Ba trạng thái. MẶC ĐỊNH KHÔNG ĐO ĐƯỢC (zip cũ còn / build không ĐẠT); build ĐẠT thì mặc định ĐỎ,
    # và chỉ một phép băm ĐÃ CHẠY XONG mới lật sang ĐẠT — câu lệnh ném để lại ĐỎ, không để lại giá trị khởi tạo.
    $td = 'KHÔNG ĐO ĐƯỢC'
    if ($conCu.Count -gt 0) {
        Canh "không xoá được zip của lượt trước ($($conCu -join ', ')) — KHÔNG build, tất định KHÔNG ĐO ĐƯỢC."
    } else {
        # Hai lần build đi QUA `Chay-Cong`: cùng hạn giờ, cùng `KHÔNG KHỞI ĐỘNG ĐƯỢC`, rc đọc từ chính
        # tiến trình — đo: gọi bằng `&` thì `-HanGiay 3` vẫn chờ trọn 2×25 s rồi đếm ĐẠT.
        $build = @()
        foreach ($f in 'a', 'b') {
            Chay-Py "release-bundle $f" @('scripts/tl.py', 'release-bundle', '--out', "dist/$f.zip", '--json')
            $build += $KetQua[$KetQua.Count - 1].TrangThai
        }
        if (@($build | Where-Object { $_ -ne 'ĐẠT' }).Count -eq 0) {
            $td = 'ĐỎ'
            try {
                $ha = (Get-FileHash -Algorithm SHA256 -LiteralPath $za -ErrorAction Stop).Hash
                $hb = (Get-FileHash -Algorithm SHA256 -LiteralPath $zb -ErrorAction Stop).Hash
                if ([bool]$ha -and ($ha -eq $hb)) { $td = 'ĐẠT' }
                Noi "      a=$ha"
                Noi "      b=$hb"
            } catch { Canh "release-bundle trả rc=0 mà không băm được zip: $($_.Exception.Message)" }
        }
    }
    $rcB = switch ($td) { 'ĐẠT' { 0 } 'ĐỎ' { 1 } default { $null } }
    Write-Host ("  {0,-42} rc={1,-4} {2}" -f 'release-bundle tất định', $(if ($null -eq $rcB) { '-' } else { $rcB }), $td) `
        -ForegroundColor $(switch ($td) { 'ĐẠT' { 'Green' } 'ĐỎ' { 'Red' } default { 'Yellow' } })
    [void]$KetQua.Add([pscustomobject]@{ Ten = 'release-bundle tất định'; Rc = $rcB; TrangThai = $td; NhatKy = '' })

    Noi ''
    Noi 'KHÔNG CHẠY (chỉ có trên Linux runner): "bo ca gate chay TRONG cgroup duoc uy quyen".'
    Noi 'KHÔNG CHẠY (đòi event pull_request): "PR head contains required EOL base".'
    Noi 'KHÔNG CHẠY (đòi event KHÁC pull_request + gate_lifecycle evidence): "tl selftest (co bang chung exact-identity)".'
    Noi 'KHÔNG CHẠY (đòi ref KHÁC master): "release-verify lane WORKER" — script chạy lane LAND thay vào.'
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
