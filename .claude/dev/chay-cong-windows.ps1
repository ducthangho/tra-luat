#Requires -Version 7.1
# ĐÒI pwsh 7.1+, KHÔNG phải Windows PowerShell 5.1 — và đây là phép đo, không phải sở thích:
#   · Tệp này UTF-8 KHÔNG BOM, LF — theo nhóm `scripts/*.ps1` + `tl-setup.ps1` (7 tệp không BOM trên master 8b59185).
#     Kho KHÔNG có một quy ước duy nhất: 5/12 tệp `.ps1` có sẵn (`docs/runbooks/**`) CÓ BOM (đo `git ls-tree` + 3 byte
#     đầu, master 8b59185; nền gốc d553efa: 5/10). PowerShell 5.1 đọc tệp không BOM theo ANSI ⇒ tiếng Việt thành rác.
#   · `$tt.Kill($true)` (giết cả cây tiến trình, dùng cho hạn giờ) chỉ có từ .NET Core 3.0.
#   · `$tt.WaitForExitAsync()` (xả stdout/stderr CÓ HẠN sau khi cổng thoát) chỉ có từ .NET 5 = pwsh 7.1.
#   · `ci.yml` đã gọi `pwsh -NoProfile -File scripts/don-nhanh_test.ps1`, nên pwsh 7 vốn là
#     giả định sẵn có của kho chứ không phải đòi hỏi mới.
<#
.SYNOPSIS
    Chạy các cổng của kho `tra-luat` trên máy Windows — KHÔNG chạm CI.

.DESCRIPTION
    Script này gương lại LỆNH của các bước cổng trong các job `gate*` của `.github/workflows/ci.yml`
    (tên job là cách CI chia máy và trôi theo master: nền gốc d553efa có `gate`, `gate-registry`,
    `gate-packet-loop`; master fc852ff tách thêm `gate-ops`, `gate-cong-cu` (8 mảnh) và `gate-cong-cu-gop` (gom mảnh —
    script chạy `ops/cong_cu_test.py` TRỌN một lượt thay cho mảnh + gom)), nhưng chạy TẠI MÁY. `env:` của bước do script
    làm chủ: khoá chế độ rò từ phiên gọi bị xoá, cùng `PYTHON*` lạ, biến git trỏ kho/cây/index khác, `BASH_ENV` và hàm bash
    export `BASH_FUNC_*` (job CI không có biến nào trong số đó), `test registry` mang env như lượt `pull_request` khi đo
    được diff. Nó KHÔNG gọi
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
    `day-du` — gương các bước cổng của các job `gate*` của CI. Bước KHÔNG gương được thì script in `KHÔNG CHẠY` ở
               cuối mức này — năm dòng: cgroup và `ci-duong-nhanh selftest` (chỉ có trên Linux; bước sau có từ master
               7e5958e), EOL base (đòi event `pull_request`), `tl selftest` có bằng chứng exact-identity, `release-verify`
               lane WORKER — cộng hai bước `ci.yml` bỏ trên Windows, và một dòng `THAY BẰNG` cho mảnh + gom của
               `cong_cu_test` (master từ fc852ff). Bước chỉ chạy ở chế độ `duong_nhanh` (PR chỉ đổi hồ sơ) thì không
               gương: script luôn chạy ĐỦ như lượt push/`workflow_dispatch`. t32 đòi mọi bước `gate*` còn lại có LỆNH
               trong script — mỗi (đích, MỌI đối số sau nó) của `ci.yml` BẰNG đuôi của một mảng/lệnh trong script, kể cả ghim
               phiên bản (`pkg==x.y.z`, `AL_VER`) — hoặc có TÊN ĐÚNG trong một dòng `KHÔNG CHẠY`/`THAY BẰNG`; bước không có đích
               `.py/.sh/.ps1` nào và bước `uses:` lạ phải nằm trong danh sách nếp/cài đặt của t32.

.PARAMETER CaiCongCu
    Cài PyYAML/jsonschema/ruff bản GHIM, rồi `actionlint` (vào `dist/actionlint` của bản clone), `shellcheck`, `rg`
    bằng chính installer của kho. Không có cờ này thì script chỉ ĐO xem công cụ có chưa và báo thiếu.

.PARAMETER ChiTiet
    In toàn bộ output của mọi cổng. Mặc định chỉ in output của cổng ĐỎ.

.PARAMETER HanGiay
    Hạn giờ cho MỘT cổng, tính bằng giây. Mặc định 9000 = `timeout-minutes: 150` — trần LỚN NHẤT của các job
    `gate*` trên master 1a269f5 (`gate-cong-cu` từ #849; #910 đưa thêm `gate` `gate-ops` `gate-packet-loop`
    `gate-nhanh-manh` `gate-registry` lên 150), t9 đọc `ci.yml` của cây và đòi ≥ (wp923: 6300 → 9000, t9 ĐỎ trên
    1a269f5). Trước đó 6300 = `timeout-minutes: 105` của job `gate-registry` trên master 8b59185. Trước nữa
    5400 (= 90 phút của fc852ff); master nâng lên 105 nên khi merge t9 ĐỎ (đo: cây merge 8b59185 + bản 5400 ⇒
    32/33, chỉ t9) — trần này TRÔI theo master, t9 là chốt bắt nó. Chính
    `ci.yml` ghi lý do: `test registry` chạy tuần tự, 52,15 phút trên ubuntu ⇒ 60 → 90, và "90 KHÔNG đủ
    Windows". Hạn 3600 cũ (= 60 phút của nền gốc d553efa) làm t9 ĐỎ ngay khi merge (đo: cây merge + PR ⇒ chỉ
    t9 ĐỎ), như hạn 900 trước đó: thấp hơn trần CI thì mức mặc định có thể KHÔNG BAO GIỜ ra ĐẠT. Trần ấy chỉ so được khi khối việc
    BẰNG của CI — vì thế `test registry` mang cả `env:` của bước (xem chỗ gọi). Quá hạn thì cổng bị giết và đếm
    là **TREO** — tức `KHÔNG ĐO ĐƯỢC`, KHÔNG phải `ĐẠT`. Cổng đã THOÁT mà CHÁU còn giữ stdout/stderr
    tới hạn thì không giết được gì (cháu đã mồ côi): rc=0 ⇒ `KHÔNG ĐO ĐƯỢC`, rc≠0 ⇒ vẫn `ĐỎ` — rc đọc từ
    chính tiến trình; rc KHÔNG đọc được ⇒ `KHÔNG ĐO ĐƯỢC` ở mọi nhánh. Có tham số này vì `don-nhanh_test.ps1`
    dựng kho git thật cho từng ca và đã ĐO ĐƯỢC một lần treo quá 10 phút; một bộ chạy cục bộ
    không được phép treo vô hạn rồi bắt người ngồi đoán.

.PARAMETER AlVer
    Bản ghim của `actionlint`. Mặc định `1.7.7` — đúng bản mà `ci.yml` ghim.

.EXAMPLE
    pwsh -NoProfile -File .\.claude\dev\chay-cong-windows.ps1 -CaiCongCu
.EXAMPLE
    pwsh -NoProfile -File .\.claude\dev\chay-cong-windows.ps1 -Muc day-du -ChiTiet
.NOTES
    Gọi bằng `pwsh -File` (tiến trình RIÊNG). Script đổi cwd, PATH, PYTHON* (xoá HẾT rồi đặt bốn biến), AL_*, GIT_CONFIG, xoá
    khoá `env:` của bước cổng, biến git cục bộ của kho, BASH_ENV và BASH_FUNC_* (danh sách ở đầu script) rồi ĐẶT `CI_DANG_KY_*` (kể cả GOC/DAU là SHA lúc chạy), và [Console]::OutputEncoding của tiến
    trình đang chạy nó; gọi thẳng `.\chay-cong-windows.ps1` trong một phiên pwsh thì mọi thay đổi ấy Ở LẠI phiên sau khi
    script kết thúc — một `ci_dang_ky_test.py --chay` gõ tay sau đó trong phiên ấy lấy kế hoạch NHẸ từ SHA CŨ.
#>
[CmdletBinding()]
param(
    [string]$Goc,
    [ValidateSet('nhanh', 'day-du')]
    [string]$Muc = 'nhanh',
    [switch]$CaiCongCu,
    [switch]$ChiTiet,
    [ValidateRange(1, 86400)]
    [int]$HanGiay = 9000,
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
# `PYTHON*` của phiên gọi đổi NGỮ NGHĨA mọi cổng Python, và job CI không đặt biến `PYTHON*` nào ngoài bốn biến dưới đây:
# `PYTHONOPTIMIZE` gỡ mọi `assert` trần (đo trên cây merge 163fd5d: `lease_publish_test.py --chi-ca=t33_` với workflow actionlint
# ĐỎ ⇒ rc=0 `1/1 đạt`; đầu-cuối trên 34e7a9d: cổng `assert False` ⇒ ĐẠT, script rc=0). Danh sách CHO PHÉP, không danh sách CẤM:
# xoá HẾT `PYTHON*` (không phân biệt hoa thường — Windows cũng không) rồi đặt đúng bốn biến.
foreach ($n in @(Get-ChildItem Env: | Where-Object Name -like 'PYTHON*' | ForEach-Object Name)) {
    [Environment]::SetEnvironmentVariable($n, $null)
}
$env:PYTHONUTF8           = '1'
$env:PYTHONIOENCODING     = 'utf-8'
$env:PYTHONUNBUFFERED     = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
# `env:` của BƯỚC cổng là một phần của lệnh: biến chế độ RÒ từ phiên gọi đổi cổng thành bản NHẸ hơn mà rc vẫn 0 (đo trên cây merge
# 20ec8d5: `CONG_CU_TEST_BAN_KINH=manh` ⇒ `cong_cu_test` rc=0 sau 258 s, bán kính 416 đột biến "GIAO cho job gate-cong-cu" — không
# cổng nào ở đây chạy job ấy). XOÁ mọi khoá `env` mà một job `gate*` của `ci.yml` hay một job của `ci-dot-bien-du.yml` (lượt tuần)
# khai — t30 đọc cả hai tệp và đòi đủ, rồi RÒ từng khoá vào cổng; bước nào CI ĐẶT thì script đặt lại đúng giá trị ấy ở chỗ chạy
# bước (AL_VER; `test registry`). `NHANH_DON_DUOC_MANH` rò (đo trên cây merge: tới registry, `nhanh_don_duoc_test` bỏ chế độ NHẸ để
# chạy MẢNH, registry ĐỎ vì máy) và `CONG_CU_TEST_MANH` rò (đo: `cong_cu_test` rc=0, 26/416 đột biến, bỏ cổng cây thật).
# `CI_DUONG_NHANH_*`: env bước `kiem re` của `gate-ops` (master 7e5958e, packet #674) — script không chạy bước ấy (chỉ có ở chế độ
# `duong_nhanh`), nên xoá như mọi khoá khác (đo: cây merge 7e5958e với ad4e724 ⇒ t30 vế tĩnh ĐỎ, thiếu đúng bốn khoá này).
foreach ($n in 'AL_VER', 'PR_HEAD_SHA', 'EOL_BASE_SHA', 'CONG_CU_TEST_BAN_KINH', 'CONG_CU_TEST_MANH', 'CONG_CU_TEST_MANH_RA',
               'CI_DANG_KY_WORKERS', 'CI_DANG_KY_SU_KIEN', 'CI_DANG_KY_GOC', 'CI_DANG_KY_DAU', 'CI_DANG_KY_DOT_BIEN_MANH',
               'NHANH_DON_DUOC_MANH', 'NHANH_DON_DUOC_MANH_RA', 'CI_DUONG_NHANH_SU_KIEN', 'CI_DUONG_NHANH_GOC',
               'CI_DUONG_NHANH_DAU', 'CI_DUONG_NHANH_MERGE') {
    [Environment]::SetEnvironmentVariable($n, $null)
}
# Biến git CỤC BỘ CỦA KHO (đúng tập `git rev-parse --local-env-vars` in ra, trừ `GIT_CONFIG*` — nếp git đọc giá trị CÓ HIỆU LỰC, t13)
# trỏ mọi lệnh git — của script lẫn của cổng con — sang kho/cây/index KHÁC; hook `pre-commit` của `git commit -a` xuất
# `GIT_INDEX_FILE` tuyệt đối. Đo trên 34e7a9d: `GIT_WORK_TREE` trỏ bản sạch ⇒ `git status` đo cây KHÁC ⇒ registry mang env
# `pull_request` trên cây BẨN; `GIT_DIR` trỏ kho khác ⇒ nếp git ghi vào config KHO ẤY. `BASH_ENV`: bash nạp tệp ấy trước mọi cổng
# bash (đo: 3 lần, có lần ngay trước `ops/chay_lease_publish_test.sh`). t31 đọc tập ấy từ git và RÒ từng biến.
foreach ($n in 'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_OBJECT_DIRECTORY', 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_IMPLICIT_WORK_TREE',
               'GIT_GRAFT_FILE', 'GIT_INDEX_FILE', 'GIT_NO_REPLACE_OBJECTS', 'GIT_REPLACE_REF_BASE', 'GIT_PREFIX', 'GIT_SHALLOW_FILE',
               'GIT_COMMON_DIR', 'BASH_ENV') {
    [Environment]::SetEnvironmentVariable($n, $null)
}
# Hàm bash EXPORT (`BASH_FUNC_<tên>%%`): bash nạp chúng lúc khởi động như `BASH_ENV`, và một hàm che được cả lệnh NỘI TRÚ. Đo trên
# ad4e724 với wrapper lease THẬT (installer giả): hàm `exec` ⇒ dòng `exec … lease_publish_test.py` cuối wrapper thành lời gọi hàm,
# `lease-publish selftest` rc=0 ĐẠT, script rc=0, trong khi bộ test thoát 1. Xoá cả HỌ như `PYTHON*`: không workflow nào khai
# `BASH_FUNC_*` (đo: 0 dòng ở cả ba cây nhánh / merge 163fd5d / merge 7e5958e).
foreach ($n in @(Get-ChildItem Env: | Where-Object Name -like 'BASH_FUNC_*' | ForEach-Object Name)) {
    [Environment]::SetEnvironmentVariable($n, $null)
}

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
# `dist/actionlint` (AL_DICH, DẪN TỪ `$Goc`) lên ĐẦU PATH — của script lẫn của `ops/chay_lease_publish_test.sh` (nó tự chèn
# `$AL_DICH` rồi gọi `python` theo TÊN). Gốc chứa dấu phân cách PATH của nền (`:` POSIX, `;` Windows) thì mục ấy VỠ ĐÔI: tiền tố
# lên ĐẦU PATH, phần sau thành mục TƯƠNG ĐỐI (đo: gốc `…/a:b/k` ⇒ PATH0=`…/a`, PATH1=`b/k/dist/actionlint`, AL_DICH không nằm
# trên PATH; `python` giả trong `…/a` ⇒ 6/6 cổng ĐẠT, rc=0). Từ chối như gốc có wildcard.
if ($Goc.Contains([string][IO.Path]::PathSeparator)) {
    Loi "gốc kho '$Goc' chứa dấu phân cách PATH '$([IO.Path]::PathSeparator)' — dist/actionlint lên đầu PATH sẽ vỡ thành hai mục. Dời kho sang đường dẫn không có ký tự ấy."
    exit 2
}
Set-Location -LiteralPath $Goc
Noi "gốc kho: $Goc"

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
        # Trả `.Source` của đúng tệp đã chứng minh (tuyệt đối; mục PATH TƯƠNG ĐỐI cho `rel/python`, tương đối với `$Goc` — cwd
        # không đổi nên vẫn đúng tệp), KHÔNG trả TÊN: sau hàm này script chèn `dist/actionlint` lên ĐẦU
        # PATH, nên `python` theo tên lúc chạy cổng có thể là tệp KHÁC tệp đã kiểm — lớp này đã tái phát ba lần (shim đầu PATH;
        # `<TEMP>/actionlint`; `python` trong `dist/actionlint` ⇒ đo: 6/6 cổng ĐẠT, rc=0).
        $lenh = @(Get-Command $u.Ten -CommandType Application -ErrorAction SilentlyContinue)
        if ($lenh.Count -gt 0) {
            $exe = $lenh[0].Source
            $d = $u.Dau
            # CHỨNG MINH là Python bằng ĐẦU RA, không bằng rc: một shim thoát 0 cho mọi lời gọi
            # qua được `-c "import sys"` rồi làm MỌI cổng Python "ĐẠT" mà không chạy gì (đã đo).
            $ra = @(& $exe @d -c "import sys; print('TLPY=%d.%d.%d' % sys.version_info[:3])" 2>$null)
            if ($LASTEXITCODE -eq 0 -and @($ra -match '^TLPY=3\.\d+\.\d+$').Count -gt 0) {
                return [pscustomobject]@{ Ten = $exe; Dau = $u.Dau }
            }
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
# `AL_DICH` RIÊNG của bản clone (như `$RUNNER_TEMP` của job CI), KHÔNG phải TEMP dùng chung: thư mục này lên ĐẦU PATH SAU khi
# Tim-Python đã chứng minh Python, mà `ops/chay_lease_publish_test.sh` chèn `$AL_DICH` lên đầu PATH rồi gọi `python` theo TÊN
# (cổng Python của script từng cũng vậy — nay chạy `.Source` mà Tim-Python đã chứng minh). `GetTempPath()` trên Linux là `/tmp/`
# (1777) ⇒ ai cũng tạo được `/tmp/actionlint`; đặt `python` vào đó là mọi cổng Python ĐẠT mà không chạy gì (đo trên 131c2e7:
# 5/5 ĐẠT, rc=0; đối chứng 4 ĐỎ, rc=1). `dist/` đã bị `.gitignore` và nằm
# trong `_RELEASE_EXCLUDE_DIRS` (đo: 9 cổng quét cây giữ nguyên rc khi có `dist/actionlint`).
$AlDich = Join-Path $Goc (Join-Path 'dist' 'actionlint')
# `dist/` bị `.gitignore`: mọi thứ dưới nó là của MÁY (installer, nhật ký), không phải DỮ LIỆU của nhánh đang đo — mà
# `dist/actionlint` lên ĐẦU PATH của script lẫn wrapper lease (gọi `python` theo tên; `ops/`, ngoài write set). Đo: `python` giả
# theo dõi ở đó ⇒ `lease-publish selftest` ĐẠT dù bộ test thoát 1 (131c2e7, AL_DICH = TEMP: ĐỎ). Hỏi CẢ mục `dist`, KHÔNG phân
# biệt hoa thường: symlink `dist` THEO DÕI (mẫu `dist/` chỉ khớp THƯ MỤC nên nó vào bằng `git add` thường) và `DIST/…` theo dõi
# đều làm `ls-files -- dist/actionlint` RỖNG, còn danh sách CHO PHÉP bên dưới chỉ so TÊN — `actionlint` giả qua symlink ấy lọt cả
# hai (đo trên f1f753b: `cong_cu kiem-tra` ĐẠT, script rc=0; không có actionlint: cổng rc=3 ĐỎ). `GIT_LITERAL_PATHSPECS` làm git từ chối
# `--icase-pathspecs` (rc=128) ⇒ rơi vào nhánh "không hỏi được git", không fail-open.
$alTheoDoi = @(& git --icase-pathspecs ls-files -- 'dist' 2>$null)
if ($LASTEXITCODE -ne 0 -or $alTheoDoi.Count -gt 0) {
    Loi "dist có mục THEO DÕI ($($alTheoDoi -join ', ')) hoặc không hỏi được git — dist/actionlint lên đầu PATH nên không dùng dữ liệu của nhánh."
    exit 2
}
# `dist` CHƯA theo dõi mà là symlink/junction (hoặc không phải thư mục) thì mọi thứ script ghi "vào dist" — nhật ký `dist/cong-windows`,
# installer `dist/actionlint`, hai zip của bước bundle — rơi vào thư mục mà `dist` trỏ tới, có thể NGOÀI kho; và bước bundle `-Muc day-du`
# XOÁ `a.zip`/`b.zip` ở đó trước khi build (Codex PR #602, review 5479765901). Chốt `ls-files` ở trên không thấy (chưa theo dõi), danh sách
# CHO PHÉP chỉ nhìn `dist/actionlint` nên qua khi đích không có thư mục ấy. Đo trên 16522a9: symlink `dist` ⇒ thư mục ngoài kho có
# `cong-windows/` mọc ra, script đi tiếp (t36). Từ chối ở cả ba mục script ghi vào, TRƯỚC mọi lần ghi; `Get-Item -Force` vì thiếu `-Force`
# thì PowerShell bỏ qua mục ẩn, và "có mà không đọc được" cũng là từ chối.
foreach ($dd in @('dist', (Join-Path 'dist' 'actionlint'), (Join-Path 'dist' 'cong-windows'))) {
    $q = Join-Path $Goc $dd
    if (-not (Test-Path -LiteralPath $q)) { continue }
    try { $it = Get-Item -LiteralPath $q -Force -ErrorAction Stop } catch { $it = $null }
    if ($null -eq $it -or -not $it.PSIsContainer -or ($it.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        Loi "$dd là symlink/junction hoặc không phải thư mục thường — script ghi và xoá tệp dưới nó (nhật ký, công cụ, zip), có thể NGOÀI kho. Xoá mục ấy rồi chạy lại."
        exit 2
    }
}
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
# Danh sách CHO PHÉP theo TÊN, không phải danh sách CẤM: thư mục đầu PATH (của script lẫn wrapper lease) chỉ được chứa TÊN mà
# `ops/cai_actionlint.sh` sinh ra TRÊN NỀN NÀY — không phải hợp của hai nền. Gói ghim 1.7.7: linux/darwin `actionlint LICENSE.txt
# README.md docs man` + `goi.gz goi_giai_nen.tar.gz`; windows `actionlint.exe LICENSE.txt README.md docs man` + `goi.zip
# goi_giai_nen.zip` (đo `unzip -l` gói `7f12f180…`: KHÔNG có `actionlint` không đuôi). Hợp hai nền từng cho `actionlint` không đuôi
# qua trên Windows, mà lượt cài KHÔNG BAO GIỜ giải nén đè tên ấy — và `ops/cai_actionlint.sh` còn chọn nó TRƯỚC `actionlint.exe` để
# đối chiếu bản (đo trên 543f2e8: installer thật, `AL_NEN=Windows`, gói Windows thật, `actionlint` giả in `1.7.7` ⇒ rc=0, băm tệp giả
# không đổi). Nó chặn thứ git KHÔNG thấy: tệp chưa theo dõi, symlink/junction `dist` chưa theo dõi (đo: `python` qua symlink ⇒
# rc=2). Nó KHÔNG chứng minh XUẤT XỨ: một `actionlint[.exe]` (tên của nền này) chưa theo dõi mà installer không ghi (vd. mã của nhánh
# ở một lượt trước) vẫn qua, tới khi một lượt installer THÀNH CÔNG (`-CaiCongCu`, wrapper lease) giải nén đè ĐÚNG tên ấy từ gói đã
# băm (đo trên Linux: GNU tar với gói linux, Info-ZIP `unzip -o` với gói windows — tệp giả lẫn symlink đều bị thay; công cụ giải
# nén trên Windows thật: KHÔNG ĐO ĐƯỢC).
$AlChoPhep = if ($IsWindows) { @('actionlint.exe', 'LICENSE.txt', 'README.md', 'docs', 'man', 'goi.zip', 'goi_giai_nen.zip') }
             else            { @('actionlint', 'LICENSE.txt', 'README.md', 'docs', 'man', 'goi.gz', 'goi_giai_nen.tar.gz') }
if (Test-Path -LiteralPath $AlDich) {
    try { $alLa = @(Get-ChildItem -LiteralPath $AlDich -Force -ErrorAction Stop | Where-Object { $AlChoPhep -cnotcontains $_.Name } | ForEach-Object Name) }
    catch { $alLa = @("(không liệt kê được: $($_.Exception.Message))") }
    if ($alLa.Count -gt 0) {
        Loi "dist/actionlint lên đầu PATH mà chứa thứ installer không sinh ra: $($alLa -join ', '). Xoá thư mục ấy rồi chạy lại (-CaiCongCu cài lại)."
        exit 2
    }
}
# Dấu phân cách của NỀN (không ghim `;`), và không chèn lặp khi PATH đã có sẵn thư mục ấy.
$SepPath = [IO.Path]::PathSeparator
if ((Test-Path -LiteralPath $AlDich) -and (($env:PATH -split [regex]::Escape($SepPath)) -notcontains $AlDich)) {
    $env:PATH = "$AlDich$SepPath$env:PATH"
}
$env:AL_VER  = $AlVer
$env:AL_DICH = $AlDich

# Nhật ký KHÔNG được nằm trong cây đang đo: `.cong-windows/` ở gốc làm `release-verify --strict`
# hô `extra_files` (đo: 12 tệp sau mức `nhanh`) và `release-bundle` đóng chúng vào zip. `dist/`
# vừa nằm trong `_RELEASE_EXCLUDE_DIRS` vừa bị `.gitignore` — cùng chỗ bước bundle x2 ghi zip.
# Tạo SAU hai chốt `dist` ở trên, không trước: `dist` THEO DÕI là dữ liệu của nhánh, `New-Item` qua nó là ghi vào chỗ nhánh
# chọn RỒI mới bị từ chối (đo trên eba9b1d: symlink `dist` theo dõi sang `tools` ⇒ `tools/cong-windows` mọc ra, rồi rc=2).
$NhatKy = Join-Path $Goc (Join-Path 'dist' 'cong-windows')
New-Item -ItemType Directory -Force -Path $NhatKy | Out-Null

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
    # `-FilePath` cũng là MẪU với Start-Process, như `-WorkingDirectory` ở chốt gốc kho (đo: Python đã kiểm bằng `&` là
    # `…/p[1]/python`, Start-Process chạy `…/p1/python` ⇒ 6/6 cổng ĐẠT, rc=0; `[WildcardPattern]::Escape` ⇒ "No such file").
    # Đường dẫn công cụ là DỮ LIỆU — Python của Tim-Python, bash của `ops/bash_nen.py`, pwsh — nên CỬA DUY NHẤT tới Start-Process
    # từ chối nó ở đây: tệp được chạy có thể không phải tệp đã kiểm.
    if ([WildcardPattern]::ContainsWildcardCharacters($Tep)) {
        Write-Host ("  {0,-42} KHÔNG KHỞI ĐỘNG ĐƯỢC — '{1}' chứa ký tự wildcard ([ ] * ?): Start-Process coi đường dẫn là MẪU" -f $Ten, $Tep) -ForegroundColor Yellow
        [void]$KetQua.Add([pscustomobject]@{ Ten = $Ten; Rc = $null; TrangThai = 'KHÔNG ĐO ĐƯỢC'; NhatKy = '' })
        return
    }

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

    # rc KHÔNG đọc được (`ExitCode` = $null — lỗi handle ở trên; getter ném cũng ra $null, kể cả dưới StrictMode) là KHÔNG ĐO ĐƯỢC ở
    # MỌI nhánh, như nhánh xả đã nói: rơi xuống `else` là đếm một lỗi của MÁY thành cổng ĐỎ (đo: `rc=  0.1s ĐỎ`, exit 1).
    $tt2 = if ($null -eq $rc) { 'KHÔNG ĐO ĐƯỢC' } elseif ($rc -eq 0) { 'ĐẠT' } else { 'ĐỎ' }
    $mau = switch ($tt2) { 'ĐẠT' { 'Green' } 'ĐỎ' { 'Red' } default { 'Yellow' } }
    Write-Host ("  {0,-42} rc={1,-4} {2,7}s  {3}" -f $Ten, $(if ($null -eq $rc) { '-' } else { $rc }), $giay, $tt2) -ForegroundColor $mau
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
# Wrapper lease (`ops/`, ngoài write set) chọn Python THEO TÊN — `python`, rồi `python3`, rồi `py -3` — trên PATH của phiên gọi, KHÔNG
# dùng tệp Tim-Python đã chứng minh. Đo trên 9b8a420 (wrapper THẬT, bộ test giả thoát 1): `python` giả thoát 0 đầu PATH, `python3` thật
# sau nó ⇒ Tim-Python bỏ `python` và chọn `python3`, mà `lease-publish selftest` rc=0 ĐẠT, script rc=0. Hỏi CHÍNH bash ấy theo đúng
# thứ tự của wrapper, rồi đòi bằng chứng dương như Tim-Python; không chứng minh được ⇒ KHÔNG ĐO ĐƯỢC. Phần `AL_DICH` (một cổng chạy
# trước wrapper ghi vào đó) vẫn là phần đã khai CHƯA ĐÓNG ở bộ test. t33 khoá.
$PyLeaseDung = $false
if ($Bash) {
    $raL = @(& $Bash -c 'if command -v python >/dev/null 2>&1; then P=(python); elif command -v python3 >/dev/null 2>&1; then P=(python3); elif command -v py >/dev/null 2>&1; then P=(py -3); else exit 11; fi; exec "${P[@]}" -c "$1"' 'tl-lease' "import sys; print('TLPY=%d.%d.%d' % sys.version_info[:3])" 2>$null)
    $PyLeaseDung = ($LASTEXITCODE -eq 0) -and (@($raL -match '^TLPY=3[.][0-9]+[.][0-9]+$').Count -gt 0)
}
if (-not $Bash -or $PyLeaseDung) { Chay-Bash 'lease-publish selftest'  @('ops/chay_lease_publish_test.sh') }
else { Chay-Cong -Ten 'lease-publish selftest' -Tep '' -DoiSo @() -BoQua -LyDoBoQua 'Python mà wrapper chọn THEO TÊN (python → python3 → py -3) không chứng minh được là Python' }
Chay-Py   'packet-loop selftest'    @('.claude/dev/packet_loop_test.py')
# Bước `test registry` của master khai `env:` (`CI_DANG_KY_WORKERS: "2"` + sự kiện/GOC/DAU). Vắng ⇒ `doc_diff` KHÔNG ĐO ĐƯỢC ⇒ kế
# hoạch ĐỦ cho cả ba vòng đột biến, `nhanh_don_duoc` không chia mảnh — lượt PR THƯỜNG của CI giao khối việc ấy cho lượt tuần + 4 job
# mảnh, nhưng job `gate-registry` (105 phút trên 8b59185) VẪN chạy nó khi diff không đo được hoặc chạm vùng chung (`workflow_dispatch` — đường chắc
# có lượt Windows, N=1 —; PR chạm `ci.yml`, `requirements.txt`, `ops/cong_cu*`, `ops/cai_*`, tệp gốc NGOÀI bảy tài liệu `GOC_TAI_LIEU`: đo bằng `ke_hoach` THẬT ⇒
# ĐỦ ×3; `README.md`, `CHANGELOG.md` ⇒ NHẸ ×3)
# (đo trên cây merge 20ec8d5: vắng ⇒ ĐỦ ×3; env `pull_request` của chính diff PR ⇒ NHẸ ×3; `nhanh_don_duoc_test` ĐỦ > 540 s, NHẸ 2 s). Gương như lượt `pull_request` CHỈ KHI đo được diff như CI: cây SẠCH (CI đo commit, không đo cây làm việc)
# và HEAD đi TRƯỚC `origin/master`; không thì để vắng ⇒ ĐỦ (fail-closed như chính `doc_diff`). Nhánh gốc d553efa không đọc các biến.
# `git status` TIN cờ index: mục `assume-unchanged` (thẻ thường của `ls-files -v`) / `skip-worktree` (`S`) bị sửa thì status RỖNG mà
# cây làm việc KHÁC commit (đo: sửa `ops/nhanh_don_duoc.py` + `--assume-unchanged` ⇒ status rỗng ⇒ NHẸ; `.claude/settings.json` +
# `--skip-worktree` ⇒ NHẸ cho bộ SGD; không cờ ⇒ ĐỦ). Có mục mang cờ, hoặc không hỏi được git ⇒ không coi là SẠCH.
$env:CI_DANG_KY_WORKERS = '2'
$regGoc = [string](& git rev-parse --verify --quiet 'refs/remotes/origin/master^{commit}' 2>$null)
$regDau = [string](& git rev-parse --verify --quiet 'HEAD^{commit}' 2>$null)
$regBan = @(& git status --porcelain --untracked-files=all 2>$null)
$regSach = ($LASTEXITCODE -eq 0) -and ($regBan.Count -eq 0)
$regCo = @(& git ls-files -v 2>$null)
$regSach = $regSach -and ($LASTEXITCODE -eq 0) -and (@($regCo | Where-Object { $_ -cmatch '^[a-zS] ' }).Count -eq 0)
$regTruoc = if ($regGoc -and $regDau) { [string](& git rev-list --count "$regGoc..$regDau" 2>$null) } else { '' }
if ($regSach -and $regTruoc -match '^[1-9]\d*$') {
    $env:CI_DANG_KY_SU_KIEN = 'pull_request'; $env:CI_DANG_KY_GOC = $regGoc; $env:CI_DANG_KY_DAU = $regDau
} else {
    Canh 'registry test: không đo được diff như CI (cây bẩn hoặc có mục assume-unchanged/skip-worktree, thiếu origin/master, hoặc HEAD không đi trước nó) — kế hoạch ĐỦ (như lượt workflow_dispatch của CI), có thể vượt -HanGiay.'
}
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
    Noi 'KHÔNG CHẠY (chỉ có trên Linux runner; master từ 7e5958e): "ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)".'
    Noi 'KHÔNG CHẠY (đòi event pull_request): "PR head contains required EOL base".'
    Noi 'KHÔNG CHẠY (đòi event KHÁC pull_request + gate_lifecycle evidence): "tl selftest (co bang chung exact-identity)".'
    Noi 'KHÔNG CHẠY (đòi ref KHÁC master): "release-verify strict (lane WORKER — manifest TẠM ngoài repo)" — script chạy lane LAND thay vào.'
    Noi 'THAY BẰNG MỘT LƯỢT (master từ fc852ff): "G5 manh ban kinh dot bien (#668)" + "G5 gom manh ban kinh dot bien (#668)" — script chạy ops/cong_cu_test.py TRỌN.'
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
Noi '  BA TRẠNG THÁI, không hai: ĐẠT / ĐỎ / KHÔNG ĐO ĐƯỢC (gồm TREO quá hạn và rc không đọc được; cổng đã thoát rc≠0 luôn ĐỎ).'
Noi '  Một cổng không chạy được'
Noi '  KHÔNG phải một cổng đã đạt — script này không bao giờ đếm nó là xanh.'

if ($do.Count -gt 0)    { exit 1 }
if ($khong.Count -gt 0) { exit 4 }   # rc riêng: phân biệt "có cổng đỏ" với "có cổng không đo được"
exit 0
