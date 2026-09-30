#Requires -Version 7.1
# Phản chứng cho `.claude/dev/chay-cong-windows.ps1` — dựng một kho GIẢ (đích cổng là stub) rồi chạy
# script THẬT, byte-identical, trong tiến trình riêng. Mỗi ca khoá một lớp của cross-review PR #602:
#   t1 trang-thai-lac-quan-song-sot-cau-lenh-nem  release-bundle rc=0 mà không ghi zip / zip CŨ ⇒ ĐỎ
#   t2 bo-giai-cong-cu-theo-ten-thu-tu            `bash`/`bash.exe` nuốt argv đầu PATH ⇒ không được ĐẠT
#   t3 runner-tu-nhiem-cay-dang-do                sau một lượt, `git status` của kho giả SẠCH
#   t4 nhan-noi-hon-phep-do (nếp git)             `.git/config.lock` ⇒ rc=4, không in "→ 7" suông
#   t5 nhan-noi-hon-phep-do (khởi động)           Start-Process hỏng ⇒ không in "TREO"
#   t6 guong-ci-bo-dieu-kien-nen                  bước ci.yml `runner.os != 'Windows'` ⇒ script bỏ trên Windows
#   t7 sua-moi-truong-phien-goi                   PATH dùng dấu phân cách của nền, không chèn lặp AL_DICH; AL_DICH CHÍNH LÀ
#                                                 `dist/actionlint` (samefile — kể cả khi TEMP có sẵn `actionlint/`)
#   t8 bo-giai-cong-cu-theo-ten-thu-tu            `python` thoát 0 cho mọi lời gọi ⇒ không được ĐẠT
#   t9 han-mac-dinh-duoi-thoi-luong-da-do         mặc định -HanGiay ≥ `timeout-minutes` của job CI
#   t10 duong-dan-du-lieu-thanh-mau-wildcard      gốc kho dưới `…[1]…` ⇒ rc=2 + nói "wildcard", không "không tìm thấy gốc"
#   t11 nhan-noi-hon-phep-do (giết)               `Kill` ném, tiến trình còn sống ⇒ không in "ĐÃ GIẾT"
#   t12 nhan-noi-hon-phep-do (tham số)            `-HanGiay 0` bị từ chối, không thành "TREO > 0s"
#   t13 do-loi-goi-khong-do-hieu-qua (git)        biến môi trường, `[include]`, biến `GIT_CONFIG` (legacy) che `core.abbrev` ⇒ rc=4 (mỗi đường một chốt)
#   t14 cong-chay-ngoai-hop-dong-chay-cong        bundle treo quá `-HanGiay` ⇒ không ĐẠT, không chờ trọn
#   t15 do-loi-goi-khong-do-hieu-qua (zip)        zip cũ KHÔNG xoá được + bundle rc=0 không ghi ⇒ không ĐẠT
#   t16 treo-ngoai-han-gio                        cổng thoát ngay, CHÁU giữ stdout ⇒ chờ THÊM < 15 s so với lượt nền; ngoài Windows rc=4
#   t17 khoa-hep-hon-hop-dong (tất định)          hai zip KHÁC nhau ⇒ tất định ĐỎ
#   t18 xa-qua-han-nuot-cong-do                   cổng rc=1 + CHÁU giữ stdout ⇒ vẫn ĐỎ (rc=1), in log cổng; cổng thoát ở giây 3 ⇒ thời
#                                                 lượng trong [HanGiay−0,5; HanGiay+2,5] (gồm phần chờ, xả chỉ bằng phần hạn CÒN LẠI)
#   t19 mot-du-lieu-hai-nhan                      `ExitCode` KHÔNG đọc được ở đường chung ⇒ KHÔNG ĐO ĐƯỢC, không ĐỎ; cột rc in `-`
#   t20 tep-test-khong-kin-moi-truong-may         console code page 437 ⇒ vẫn đọc đúng output UTF-8 của script
#   t21 bo-giai-cong-cu-theo-ten-thu-tu (PATH)    `python` giả trong `<TEMP>/actionlint` (TEMP dùng chung) ⇒ cổng Python không ĐẠT
#   t22 bo-giai-cong-cu-theo-ten-thu-tu (tách)    gốc kho chứa dấu phân cách PATH (AL_DICH vỡ đôi, tiền tố lên đầu PATH) ⇒ rc=2
#   t23 bo-giai-cong-cu-theo-ten-thu-tu (tuyệt đối) `python` giả trong `dist/actionlint` ⇒ cổng Python vẫn chạy tệp ĐÃ KIỂM
#   t24 bo-giai-cong-cu-theo-ten-thu-tu (theo dõi) tệp THEO DÕI dưới `dist/actionlint` (đầu PATH của wrapper lease) ⇒ rc=2
# Bộ này KÍN với config git của máy chạy, với biến git trỏ kho khác (khối ngay dưới `$script:Rac`), với code page của
# console (`Doc-Utf8`), với dấu thập phân của locale (t18 nhận `5,1s`) và với `<TEMP>/actionlint` của máy (t7, t21 tự đặt TEMP).
# ĐỘT BIẾN để đo răng (đo trên pwsh 7.4.6/Linux, bộ 24 ca): `-Script` trỏ f2392df ⇒ 3/24 (đạt t17 — bản ấy đã so băm —, t21 —
# dấu `;` ghim cứng dán AL_DICH vào mục PATH kế nên nó không thành một mục — và t23 — AL_DICH là TEMP); 8b82d40 ⇒ 14/24 (đỏ t7
# t13 t14 t15 t16 t18 t19 t21 t22 t24); 66efc78 ⇒ 16/24 (đỏ t7 t13 t16 t18 t19 t21 t22 t24); 131c608 ⇒ 17/24 (đỏ t7 t13 t18 t19
# t21 t22 t24); bd62cad ⇒ 19/24 (đỏ t7 t19 t21 t22 t24); 131c2e7 ⇒ 20/24 (đỏ t7 t21 t22 t24); c8c2c6a ⇒ 21/24 (đỏ t22 t23 t24).
# Lượt 7, mỗi chốt một ca: Tim-Python trả TÊN ⇒ chỉ t23; bỏ chốt phân cách PATH ⇒ chỉ t22; bỏ chốt tệp theo dõi ⇒ chỉ t24;
# AL_DICH về TEMP ⇒ chỉ t7, kể cả khi TEMP của máy có sẵn `actionlint/` (bỏ vế samefile của t7 thì đột biến ấy SỐNG 24/24);
# TÊN + TEMP ⇒ t7 t21. Lượt 6: cột rc in TRỐNG thay cho `-` ⇒ t19. 29 đột biến trên script (lượt 4): 25 đỏ ÍT NHẤT ca
# của mảnh nó gỡ, 4 sống đúng là bốn mảnh khai ở cuối đoạn này. Lượt 5 đo lại trên bộ 20 ca: gỡ nhánh rc≠0 của xả / `$giay` trước xả / bỏ trừ phần hạn đã trôi /
# xả 2×HanGiay / sàn 12 s ⇒ chỉ t18; xả cố định 30 s ⇒ t16 t18; nhánh xả đếm ĐẠT ⇒ t16; rc=null đếm ĐỎ ⇒ t19; giải bash
# theo tên ⇒ t2; bỏ `$env:GIT_CONFIG = $null` ⇒ t13; sàn 0 ⇒ SỐNG (đã khai). Trên chính bộ này: `Doc-Utf8` rỗng ⇒ t20;
# bộ đọc thời lượng chỉ nhận dấu chấm ⇒ t18. Ca chung chốt thì khai: gỡ `exit 4` của nếp git đỏ t4 lẫn t13; `$td` khởi
# ĐẠT đỏ t1 t14 t15; bỏ xả luồng có hạn (bỏ hẳn / vô hạn / `WaitForExit()` / cố định 30 s) đỏ t16 lẫn t18 (vế thời
# lượng). Gỡ khối kín config của chính bộ này, dưới config toàn cục của ci.yml ⇒ t4 lẫn t20 (cùng dựng `config.lock`).
# Từng SỐNG rồi mới có ca: `$ha -eq $hb` (nay t17); nhánh xả-quá-hạn in "TREO" mà vẫn đếm ĐẠT (nay t16 đọc rc);
# giải `bash` theo tên trên Linux (nay t2 đặt cả `bash`); xả KHÔNG trừ phần hạn đã trôi / xả 2×HanGiay / sàn 12 s (18/18
# khi cổng thoát ngay — nay t18 cho cổng thoát ở giây 3); cột rc in `-` (20/20 — nay t19). Mảnh KHÔNG ca nào đo được trên
# nền này — khai thẳng: `$null -eq $rc` của nhánh xả (TƯƠNG ĐƯƠNG từ lượt 5: rc=null rơi xuống đường chung cũng ra KHÔNG ĐO
# ĐƯỢC — gỡ ra vẫn 24/24);
# `[bool]$ha`, `[string]$ban`, `-ErrorAction Stop` của Start-Process (tương đương: nó vốn ném lỗi kết thúc);
# vế `$LASTEXITCODE -ne 0` của chốt tệp theo dõi (git hỏng giữa chừng — nếp git đã đòi git chạy được);
# `$null = $tt.Handle` và `catch { $xa = $false }` (chỉ có tác dụng khi `.Handle`/`WaitForExitAsync` ném — Windows,
# pwsh 7.0); `#Requires -Version 7.1` (bộ này chạy bằng pwsh ≥ 7.1); sàn 1 s của `$conMs` (chỉ đổi kết quả khi cổng
# thoát sát hạn); phần khối kín cho `GIT_INDEX_FILE`/`GIT_DIR` (đo bằng chạy dưới biến ấy — gỡ ra ⇒ index kho khác
# 2144 → 34 mục — không có ca); dòng ép UTF-8 trong harness t11/t19 (chỉ có tác dụng khi console của tiến trình con là
# code page cũ — Windows). CHƯA ĐÓNG — khai thẳng: tệp CHƯA theo dõi trong `dist/actionlint` vẫn lên đầu PATH của wrapper lease
# (`ops/chay_lease_publish_test.sh` gọi `python` theo tên; ngoài write set) — đó là tệp của chính người chạy, không phải của nhánh.
[CmdletBinding()]
param([string]$Script)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$GocKho = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot (Join-Path '..' '..'))).Path
if (-not $Script) { $Script = Join-Path $PSScriptRoot 'chay-cong-windows.ps1' }
$Script = (Resolve-Path -LiteralPath $Script).Path
$PwshExe = (Get-Process -Id $PID).Path
$Sep = [IO.Path]::PathSeparator

$Stub = 'import os,sys; sys.exit(int(os.environ.get("STUB_RC_"+os.path.basename(sys.argv[0]).replace(".","_").replace("-","_"),"0")))'
$TlStub = @'
import os, sys
a = sys.argv[1:]
if a and a[0] == "release-bundle":
    out = a[a.index("--out") + 1]
    m = os.environ.get("STUB_BUNDLE", "same")
    if m == "ngu":
        import time; time.sleep(float(os.environ.get("STUB_NGU", "30")))
    if m in ("same", "ghi-rc1", "ngu"):
        open(out, "wb").write(b"ZIP-CO-DINH")
    if m == "khac":
        open(out, "wb").write(b"ZIP-" + out.encode())
    sys.exit(1 if m == "ghi-rc1" else 0)
sys.exit(0)
'@

$script:Rac = @()
# KÍN với config git của MÁY CHẠY: `ci.yml` đặt `core.autocrlf/eol/abbrev` bằng `--global` ở cả ba job gate, nên khi ghi
# `--local` trượt (t4) giá trị CÓ HIỆU LỰC vẫn đúng và script chạy tiếp ⇒ t4 ĐỎ oan đúng nơi bộ này sẽ được nối (đo:
# 14/15 dưới config toàn cục của ci.yml). Mọi git — của bộ test lẫn của script đang đo — đọc config toàn cục RỖNG,
# bỏ tầng system, bỏ tham số truyền qua biến.
$GitRong = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10) + '.gitconfig')
Set-Content -LiteralPath $GitRong -Value '' -Encoding utf8NoBOM
$script:Rac += $GitRong
$env:GIT_CONFIG_GLOBAL = $GitRong; $env:GIT_CONFIG_NOSYSTEM = '1'
$env:GIT_CONFIG_COUNT = $null; $env:GIT_CONFIG_PARAMETERS = $null
# …và KÍN với biến git trỏ KHO KHÁC: hook `pre-commit` của `git commit -a` xuất `GIT_INDEX_FILE` TUYỆT ĐỐI, khi ấy
# `git -C <kho giả> add -A` ghi đè index của kho THẬT (đo: 2144 → 34 mục, index trỏ blob không có); `GIT_DIR` cùng họ
# (đo: `git -C <kho giả> commit` ghi vào kho mà biến trỏ tới). t13 tự đặt lại `GIT_CONFIG` qua `Chay`.
foreach ($n in 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
               'GIT_COMMON_DIR', 'GIT_CONFIG') { [Environment]::SetEnvironmentVariable($n, $null) }
# …và KÍN với code page của console: pwsh GIẢI MÃ output lệnh ngoài bằng `[Console]::OutputEncoding` của tiến trình NÀY — trên
# Windows mặc định là code page OEM/ANSI (437/1252; chính script khai ở `.DESCRIPTION`) — còn script và harness GHI UTF-8. Không ép
# thì mọi regex tiếng Việt thành rác (giả lập console 437 trên Linux: 13/18, t1 t4 t11 t13 t17 ĐỎ oan, vế phủ định `tất định … rc=0`
# của t14/t15 mù). Ép UTF-8 quanh lời gọi rồi trả lại (trên Windows setter đổi code page của CẢ console). Setter ném (máy không
# có console) thì đi tiếp: giải mã sai làm ca đòi KHỚP thành ĐỎ nhưng làm MÙ vế phủ định (đo, 437 + setter gỡ + `$td` khởi ĐẠT ⇒
# t14 ĐẠT) — cả bộ vẫn ĐỎ vì t20 đỏ trong đúng tình huống ấy.
function Doc-Utf8 { param([scriptblock]$Lam)
    $enc = [Console]::OutputEncoding
    try { [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false) } catch { }
    try { & $Lam } finally { try { [Console]::OutputEncoding = $enc } catch { } } }
function Dung-Kho {
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    $k = Join-Path $d 'k'
    foreach ($t in 'ops', '.claude/dev', 'scripts/tl_core', '.githooks', '.github/checks') {
        New-Item -ItemType Directory -Force -Path (Join-Path $k $t) | Out-Null
    }
    Copy-Item -LiteralPath $Script -Destination (Join-Path $k '.claude/dev/chay-cong-windows.ps1')
    Copy-Item -LiteralPath (Join-Path $GocKho 'ops/bash_nen.py') -Destination (Join-Path $k 'ops/bash_nen.py')
    Copy-Item -LiteralPath (Join-Path $GocKho '.gitignore') -Destination (Join-Path $k '.gitignore')
    foreach ($f in 'ops/lease_publish_test.py', 'ops/cong_cu.py', 'ops/cong_cu_test.py',
                   '.claude/dev/packet_loop_test.py', '.claude/dev/ci_dang_ky_test.py',
                   '.claude/dev/codex_cred_test.py', 'ops/bien_nhan_v2_test.py', '.claude/dev/idiom_py_test.py',
                   '.githooks/eol_policy_test.py', '.githooks/pre_push_test.py', '.claude/dev/gate_lifecycle_test.py',
                   '.githooks/eol_policy.py', '.github/checks/bundle_fragment_check.py', 'scripts/gen_instructions.py',
                   'scripts/tl_core/command_registry_test.py', '.github/checks/ci_phamvi.py',
                   '.github/checks/ci_phamvi_test.py', 'scripts/tl_boot.py', 'scripts/tl_core/__init__.py',
                   'scripts/tl_core/deterministic.py', 'scripts/tl_core/jsonio.py', 'scripts/tl_core/workflow.py',
                   'scripts/tl_core/release.py', 'scripts/tl_core/live.py', 'scripts/tl_core/zip_ingest.py',
                   'scripts/tl_core/ocr.py', 'scripts/tl_core/chunking.py', 'scripts/tl_core/command_registry.py') {
        Set-Content -LiteralPath (Join-Path $k $f) -Value $Stub -Encoding utf8NoBOM
    }
    Set-Content -LiteralPath (Join-Path $k 'scripts/tl.py') -Value $TlStub -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $k 'ops/chay_lease_publish_test.sh') -Value "exit `${STUB_RC_LEASE:-0}" -Encoding utf8NoBOM
    Set-Content -LiteralPath (Join-Path $k 'scripts/don-nhanh_test.ps1') -Value 'exit 0' -Encoding utf8NoBOM
    & git -C $k init -q
    & git -C $k add -A
    & git -C $k -c user.email=t@t -c user.name=t commit -qm fx
    return $k
}

function Chay {
    param([string]$Kho, [string[]]$Doi = @(), [hashtable]$Env = @{})
    $cu = @{}
    foreach ($n in $Env.Keys) { $cu[$n] = [Environment]::GetEnvironmentVariable($n); [Environment]::SetEnvironmentVariable($n, $Env[$n]) }
    try {
        $ra = Doc-Utf8 { & $PwshExe -NoProfile -File (Join-Path $Kho '.claude/dev/chay-cong-windows.ps1') @Doi 2>&1 }
        $rc = $LASTEXITCODE
    } finally { foreach ($n in $cu.Keys) { [Environment]::SetEnvironmentVariable($n, $cu[$n]) } }
    $txt = (($ra | ForEach-Object { "$_" }) -join "`n") -replace "\x1b\[[0-9;]*m", ''
    return @{ rc = $rc; ra = $txt }
}

# Python cho t6/t9: chọn theo NĂNG LỰC (in được `TLYAML=ok` sau `import yaml`), không lấy tên đầu tiên —
# đúng lớp `bo-giai-cong-cu-theo-ten-thu-tu` mà bộ này khoá (alias Store `python.exe` trên Windows).
function Tim-PyYaml {
    foreach ($u in @([pscustomobject]@{ Ten = 'py'; Dau = @('-3') }, [pscustomobject]@{ Ten = 'python'; Dau = @() },
                     [pscustomobject]@{ Ten = 'python3'; Dau = @() })) {
        if (Get-Command $u.Ten -ErrorAction SilentlyContinue) {
            $d = $u.Dau
            $ra = @(& $u.Ten @d -c "import yaml; print('TLYAML=ok')" 2>$null)
            if ($LASTEXITCODE -eq 0 -and @($ra -match '^TLYAML=ok$').Count -gt 0) { return $u }
        }
    }
    throw 'KHONG DO DUOC: khong co Python nao import duoc yaml'
}

$script:KetQua = @()
function Ca { param([string]$Ten, [scriptblock]$Than)
    try { & $Than; $script:KetQua += "DAT  $Ten" }
    catch { $script:KetQua += "DO   $Ten — $($_.Exception.Message)" } }

Ca 't1 bundle rc=0 khong ghi zip / zip cu => DO' {
    $k = Dung-Kho
    $a = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'none' }
    if ($a.ra -notmatch 'release-bundle tất định\s+rc=1') { throw "khong zip: van khong DO (rc_script=$($a.rc))" }
    $b = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'same' }
    if ($b.rc -ne 0) { throw "nen: luot same phai DAT, rc=$($b.rc)" }
    $c = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'none' }
    if ($c.ra -notmatch 'release-bundle tất định\s+rc=1') { throw "luot none sau luot same: tat dinh khong ra rc=1 — zip CU bi bam hoac khong xoa duoc (rc_script=$($c.rc))" }
    $e = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'ghi-rc1' }
    if ($e.ra -match 'release-bundle tất định\s+rc=0' -or $e.rc -eq 0) { throw "bundle rc=1 (da ghi zip) ma tat dinh DAT (rc_script=$($e.rc))" }
}

Ca 't2 bash.exe nuot argv dau PATH => lease khong DAT' {
    $k = Dung-Kho
    $shim = Join-Path (Split-Path $k) 'shim'
    New-Item -ItemType Directory -Force -Path $shim | Out-Null
    if ($IsWindows) {
        Set-Content -LiteralPath (Join-Path $shim 'bash.cmd') -Value '@exit /b 0' -Encoding ascii
    } else {
        # Cả tên TRẦN `bash`: chỉ đặt `bash.exe` thì ca chỉ bắt bộ giải thử `bash.exe` trước — bộ giải `Get-Command bash`
        # (cùng lớp "theo tên") sống qua cả bộ trên Linux (đo: 18/18).
        foreach ($n in 'bash.exe', 'bash') {
            Set-Content -LiteralPath (Join-Path $shim $n) -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
            & chmod +x (Join-Path $shim $n)
        }
    }
    $a = Chay $k @() @{ STUB_RC_LEASE = '1'; PATH = "$shim$Sep$env:PATH" }
    if ($a.ra -match 'lease-publish selftest\s+rc=0') { throw 'shim duoc chon, cong lease DAT ma khong chay gi' }
}

Ca 't3 luot chay khong de rac trong cay' {
    $k = Dung-Kho
    $null = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'same' }
    $rac = @(& git -C $k status --porcelain --untracked-files=all)
    if ($rac.Count -gt 0) { throw "git status ban: $($rac -join ' | ')" }
}

Ca 't4 .git/config.lock => rc=4, khong in "→ 7" suong' {
    $k = Dung-Kho
    New-Item -ItemType File -Path (Join-Path $k '.git/config.lock') | Out-Null
    $a = Chay $k
    Remove-Item -LiteralPath (Join-Path $k '.git/config.lock') -Force
    if ($a.rc -ne 4) { throw "rc=$($a.rc), mong 4" }
    if ($a.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw 'khong bao nep hong' }
}

Ca 't5 Start-Process hong => khong goi la TREO' {
    $k = Dung-Kho
    foreach ($d in (Join-Path $k 'dist/cong-windows'), (Join-Path $k '.cong-windows')) {
        New-Item -ItemType Directory -Force -Path (Join-Path $d 'cong_cu_kiem-tra.out') | Out-Null
    }
    $a = Chay $k
    if ($a.ra -match 'cong_cu kiem-tra\s+TREO') { throw 'khoi dong hong ma in TREO/DA GIET' }
    if ($a.rc -eq 0) { throw 'rc=0 cho mot cong khong chay' }
}

# Đo được trên MỌI nền (không cần `$IsWindows` thật): đọc `if:` từ ci.yml, rồi đòi mỗi đích của
# bước `runner.os != 'Windows'` chỉ xuất hiện trong nhánh `else` của một `if ($IsWindows)`.
Ca 't6 buoc ci.yml bo tren Windows => script cung bo tren Windows' {
    $ci = Join-Path $GocKho '.github/workflows/ci.yml'
    $py = Tim-PyYaml; $pd = $py.Dau
    $ma = "import re,sys,yaml`nd=yaml.safe_load(open(sys.argv[1],encoding='utf-8'))`n" +
          "for j in d['jobs'].values():`n for s in j.get('steps',[]):`n  c=str(s.get('if',''))`n" +
          "  if 'Windows' in c and '!=' in c:`n   [print(t) for t in re.findall(r'[\w./-]+\.(?:py|sh|ps1)', s.get('run') or '')]"
    $dich = @(& $py.Ten @pd -c $ma $ci)
    if ($LASTEXITCODE -ne 0 -or $dich.Count -eq 0) { throw "khong doc duoc ci.yml (rc=$LASTEXITCODE, $($dich.Count) dich)" }
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    foreach ($t in $dich) {
        $hits = @($ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.StringConstantExpressionAst] -and $n.Value -eq $t }, $true))
        # 0 lần khớp = ca KHÔNG ĐO gì (tên viết bằng phép nối / Join-Path lọt qua) ⇒ ĐỎ, không ĐẠT êm.
        if ($hits.Count -eq 0) { throw "KHONG DO DUOC: '$t' khong xuat hien NGUYEN VAN trong script — viet dich thanh hang chuoi" }
        foreach ($h in $hits) {
            $p = $h.Parent; $gac = $false
            while ($p) {
                if ($p -is [System.Management.Automation.Language.IfStatementAst] -and $p.ElseClause -and
                    $p.Clauses[0].Item1.Extent.Text -match '^\$IsWindows$' -and
                    $p.ElseClause.Extent.StartOffset -le $h.Extent.StartOffset -and
                    $h.Extent.EndOffset -le $p.ElseClause.Extent.EndOffset) { $gac = $true; break }
                $p = $p.Parent
            }
            if (-not $gac) { throw "'$t' chay vo dieu kien trong khi ci.yml bo no tren Windows" }
        }
    }
}

Ca 't7 PATH: dau phan cach cua NEN, khong chen lap AL_DICH' {
    $k = Dung-Kho
    $al = Join-Path $k (Join-Path 'dist' 'actionlint')
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu.py') -Encoding utf8NoBOM -Value @'
import os, sys
al = os.environ.get("AL_DICH", "")
ds = os.environ.get("PATH", "").split(os.pathsep)
# pwsh tự chèn thư mục của nó vào ĐẦU PATH lúc khởi động, nên trên nền không phải Windows
# `"$AlDich;$env:PATH"` dán AL_DICH vào thư mục ấy chứ không đụng mục AL_DICH có sẵn —
# chỉ đếm `ds.count(al)` là ca KHÔNG CÓ RĂNG trên Linux (đã đo: bản gốc vẫn qua).
dan = os.name != "nt" and any(";" in d for d in ds)
# AL_DICH phải CHÍNH LÀ `dist/actionlint` của gốc (cwd của cổng) — so bằng samefile, không so chuỗi. Thiếu vế này thì
# AL_DICH về TEMP vẫn qua t7 trên máy CÓ SẴN `<TEMP>/actionlint` (đo: 131c2e7 ⇒ 20/21, chỉ t21 đỏ).
dung = bool(al) and os.path.isdir(al) and os.path.samefile(al, os.path.join(os.getcwd(), "dist", "actionlint"))
sys.exit(0 if dung and ds.count(al) == 1 and not dan else 7)
'@
    # PATH đã có sẵn AL_DICH = lượt thứ hai trong cùng một phiên. TEMP CÓ SẴN `actionlint/` (như máy đã từng chạy installer
    # với mặc định `/tmp/actionlint`) ⇒ kết quả ca không phụ thuộc máy chạy.
    $tam = Join-Path (Split-Path $k) 'tmp'
    New-Item -ItemType Directory -Force -Path (Join-Path $tam 'actionlint') | Out-Null
    $a = Chay $k @() @{ PATH = "$al$Sep$env:PATH"; TMPDIR = $tam; TEMP = $tam; TMP = $tam }
    if ($a.ra -notmatch 'cong_cu kiem-tra\s+rc=0') { throw 'PATH sai dau phan cach hoac chen lap AL_DICH' }
}

Ca 't8 python gia thoat 0 dau PATH => cong Python khong DAT' {
    $k = Dung-Kho
    $shim = Join-Path (Split-Path $k) 'shimpy'
    New-Item -ItemType Directory -Force -Path $shim | Out-Null
    foreach ($n in 'py', 'python', 'python3') {
        if ($IsWindows) { Set-Content -LiteralPath (Join-Path $shim "$n.cmd") -Value '@exit /b 0' -Encoding ascii }
        else {
            $f = Join-Path $shim $n
            Set-Content -LiteralPath $f -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
            & chmod +x $f
        }
    }
    $a = Chay $k @() @{ STUB_RC_cong_cu_py = '1'; PATH = "$shim$Sep$env:PATH" }
    if ($a.ra -match 'cong_cu kiem-tra\s+rc=0') { throw 'python gia duoc chon, cong Python DAT ma khong chay gi' }
}

# Hạn mặc định cho MỘT cổng không được thấp hơn trần job CI chạy chính cổng ấy: thấp hơn thì mức
# mặc định có thể KHÔNG BAO GIỜ ra ĐẠT (đo: `test registry` > 900 s cả trên CI Windows lẫn ở đây).
Ca 't9 han mac dinh >= timeout-minutes cua job CI' {
    $ci = Join-Path $GocKho '.github/workflows/ci.yml'
    $py = Tim-PyYaml; $pd = $py.Dau
    $ma = "import sys,yaml`nd=yaml.safe_load(open(sys.argv[1],encoding='utf-8'))`n" +
          "print(max(int(d['jobs'][j]['timeout-minutes']) for j in ('gate','gate-registry','gate-packet-loop')))"
    $phut = @(& $py.Ten @pd -c $ma $ci)
    if ($LASTEXITCODE -ne 0 -or $phut.Count -ne 1) { throw "khong doc duoc timeout-minutes (rc=$LASTEXITCODE)" }
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $p = @($ast.ParamBlock.Parameters | Where-Object { $_.Name.VariablePath.UserPath -eq 'HanGiay' })
    if ($p.Count -ne 1 -or -not $p[0].DefaultValue) { throw 'khong thay mac dinh cua -HanGiay' }
    $mac = [int]$p[0].DefaultValue.SafeGetValue()
    if ($mac -lt [int]$phut[0] * 60) { throw "HanGiay mac dinh $mac s < $([int]$phut[0] * 60) s cua job CI" }
}

Ca 't10 goc kho co [ ] => bao dung nguyen nhan, khong bao "khong tim thay goc"' {
    $k = Dung-Kho
    $moi = Join-Path (Split-Path $k) 'b[1]'
    New-Item -ItemType Directory -Force -Path $moi | Out-Null
    & git clone -q $k (Join-Path $moi 'k')
    if ($LASTEXITCODE -ne 0) { throw "git clone vao duong dan co [ ] that bai (rc=$LASTEXITCODE)" }
    $a = Chay (Join-Path $moi 'k')
    if ($a.ra -match 'không tìm thấy gốc kho') { throw 'goc CO THAT ma bao "khong tim thay goc" (Test-Path doc [1] thanh mau)' }
    if ($a.rc -ne 2 -or $a.ra -notmatch 'wildcard') { throw "khong noi dung nguyen nhan wildcard (rc=$($a.rc))" }
}

# Nạp NGUYÊN VĂN `Chay-Cong` từ AST, cho `Start-Process` một đồ giả GIỮ TRẠNG THÁI: không bao giờ thoát,
# `Kill` ném (ca `taskkill Access denied` của CLAUDE.md). Trên nền thật không dựng được tiến trình giết-không-chết.
Ca 't11 Kill nem + tien trinh con song => khong in "DA GIET"' {
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $fn = $ast.Find({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Chay-Cong' }, $true)
    if (-not $fn) { throw 'khong thay ham Chay-Cong trong script' }
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    $h = Join-Path $d 'h.ps1'
    Set-Content -LiteralPath $h -Encoding utf8NoBOM -Value (@'
Set-StrictMode -Version Latest
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$KetQua = New-Object System.Collections.ArrayList
$NhatKy = $PSScriptRoot; $Goc = $PSScriptRoot; $HanGiay = 1; $ChiTiet = $false
$script:SoKill = 0
function Start-Process {
    $o = [pscustomobject]@{ HasExited = $false; ExitCode = $null }
    $o | Add-Member -MemberType ScriptMethod -Name WaitForExit -Value { $false }
    $o | Add-Member -MemberType ScriptMethod -Name Kill -Value { $script:SoKill++; throw 'Access is denied' }
    return $o
}
'@ + "`n" + $fn.Extent.Text + "`n" + @'
Chay-Cong -Ten 'gia' -Tep 'khong-co' -DoiSo @()
Write-Host ("TRANG_THAI=" + $KetQua[0].TrangThai + " SO_KILL=" + $script:SoKill)
'@)
    $ra = (Doc-Utf8 { & $PwshExe -NoProfile -File $h 2>&1 } | ForEach-Object { "$_" }) -join "`n"
    if ($ra -notmatch 'TRANG_THAI=KHÔNG ĐO ĐƯỢC SO_KILL=[1-9]') { throw "harness khong chay toi Kill: $ra" }
    if ($ra -match 'ĐÃ GIẾT') { throw 'Kill nem, tien trinh con song ma van in "DA GIET"' }
}

Ca 't12 -HanGiay 0 bi tu choi, khong thanh "TREO > 0s"' {
    $k = Dung-Kho
    $a = Chay $k @('-HanGiay', '0')
    if ($a.ra -match 'TREO\s+>\s*0s') { throw 'HanGiay 0 duoc nhan: moi cong "TREO > 0s"' }
    if ($a.rc -eq 0 -or $a.ra -notmatch 'HanGiay') { throw "HanGiay 0 khong bi tu choi dung cho (rc=$($a.rc))" }
}

Ca 't13 bien moi truong / [include] de core.abbrev => rc=4, khong in "→ 7" suong' {
    $k = Dung-Kho
    $a = Chay $k @() @{ GIT_CONFIG_COUNT = '1'; GIT_CONFIG_KEY_0 = 'core.abbrev'; GIT_CONFIG_VALUE_0 = '8' }
    if ($a.rc -ne 4 -or $a.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw "git dung abbrev 8 ma script bao nep dung (rc=$($a.rc))" }
    # Đường thứ hai, chốt riêng: `[include]` nằm SAU `[core]` trong `.git/config` ⇒ thắng giá trị `--local` vừa ghi.
    $k2 = Dung-Kho
    $inc = Join-Path (Split-Path $k2) 'inc.gitconfig'
    Set-Content -LiteralPath $inc -Value "[core]`n`tabbrev = 8" -Encoding utf8NoBOM
    & git -C $k2 config --local include.path $inc
    $b = Chay $k2
    if ($b.rc -ne 4 -or $b.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw "[include] de abbrev 8 ma script bao nep dung (rc=$($b.rc))" }
    # Đường thứ ba, chốt riêng: biến `GIT_CONFIG` (legacy) làm `--local` ghi trượt (rc=129) và `--get` CHỈ đọc tệp ấy —
    # tệp nói 7 trong khi mọi lệnh git khác dùng 8 từ `[include]`.
    $k3 = Dung-Kho
    $inc3 = Join-Path (Split-Path $k3) 'inc.gitconfig'
    Set-Content -LiteralPath $inc3 -Value "[core]`n`tabbrev = 8" -Encoding utf8NoBOM
    & git -C $k3 config --local include.path $inc3
    $leg = Join-Path (Split-Path $k3) 'legacy.gitconfig'
    Set-Content -LiteralPath $leg -Value "[core]`n`tautocrlf = false`n`teol = lf`n`tabbrev = 7" -Encoding utf8NoBOM
    $c = Chay $k3 @() @{ GIT_CONFIG = $leg }
    if ($c.rc -ne 4 -or $c.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw "GIT_CONFIG legacy che abbrev 8 ma script bao nep dung (rc=$($c.rc))" }
}

Ca 't14 bundle treo qua HanGiay => khong DAT, khong cho tron' {
    $k = Dung-Kho
    $w = [Diagnostics.Stopwatch]::StartNew()
    $a = Chay $k @('-Muc', 'day-du', '-HanGiay', '3') @{ STUB_BUNDLE = 'ngu'; STUB_NGU = '30' }
    $w.Stop()
    if ($a.ra -match 'release-bundle tất định\s+rc=0') { throw 'bundle treo ma tat dinh DAT' }
    if ($w.Elapsed.TotalSeconds -ge 45) { throw "bundle khong co han gio: cho $([math]::Round($w.Elapsed.TotalSeconds))s voi HanGiay 3" }
}

Ca 't15 zip cu KHONG xoa duoc + bundle rc=0 khong ghi => khong DAT' {
    $k = Dung-Kho
    $b = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'same' }
    if ($b.rc -ne 0) { throw "nen: luot same phai DAT, rc=$($b.rc)" }
    $dist = Join-Path $k 'dist'
    $zip = @((Join-Path $dist 'a.zip'), (Join-Path $dist 'b.zip'))
    $do = Join-Path $dist 'do.zip'
    Set-Content -LiteralPath $do -Value 'x'
    $mo = @(); $go = $null
    try {
        if ($IsWindows) {
            foreach ($f in $zip + $do) { $mo += [IO.File]::Open($f, 'Open', 'Read', 'Read') }   # không FileShare.Delete
        } elseif ((& id -u) -eq '0') {
            & chattr +i @($zip + $do) 2>$null; $go = { & chattr -i @($zip + $do) 2>$null }
        } else {
            & chmod 0555 $dist; $go = { & chmod 0755 $dist }
        }
        # TỆP DÒ: khoá không có tác dụng trên nền này thì ca KHÔNG ĐO ĐƯỢC — ĐỎ, không bỏ qua êm.
        Remove-Item -LiteralPath $do -Force -ErrorAction SilentlyContinue
        if (-not (Test-Path -LiteralPath $do)) { throw 'KHONG DO DUOC: khong dung duoc tep khong xoa duoc tren nen nay' }
        $a = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'none' }
    } finally {
        foreach ($m in $mo) { $m.Dispose() }
        if ($go) { & $go }
    }
    if ($a.ra -match 'release-bundle tất định\s+rc=0') { throw "zip CU khong xoa duoc ma tat dinh DAT (rc_script=$($a.rc))" }
    if ($a.rc -eq 0) { throw 'rc=0 khi tat dinh khong do duoc' }
}

# Cổng thoát NGAY nhưng để lại CHÁU giữ stdout: hạn giờ phải phủ cả phần xả luồng (Start-Process trên Unix đọc qua
# ỐNG, `WaitForExit()` không hạn chờ EOF). Windows chuyển hướng bằng handle tệp ⇒ vế trạng thái chỉ đòi ngoài Windows.
# Đo phần chờ THÊM so với một lượt nền cùng tham số: trần tuyệt đối 40 s để lọt một bản xả cố định 30 s — gấp 6 lần
# `-HanGiay 5` (đo: 34 s vẫn ĐẠT). Vế trạng thái đọc MÃ THOÁT, không chỉ đọc chữ: một bản in "TREO" mà vẫn đếm ĐẠT
# thì script thoát 0 (đo).
Ca 't16 cong thoat ngay, CHAU giu stdout => khong treo qua -HanGiay' {
    $k0 = Dung-Kho
    $w0 = [Diagnostics.Stopwatch]::StartNew(); $null = Chay $k0 @('-HanGiay', '5'); $w0.Stop()
    $k = Dung-Kho
    $pidf = Join-Path (Split-Path $k) 'chau.pid'
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu.py') -Encoding utf8NoBOM -Value @'
import os, subprocess, sys
if sys.argv[1:2] == ["kiem-tra"]:
    p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    open(os.environ["STUB_CHAU_PID"], "w").write(str(p.pid))
sys.exit(0)
'@
    $w = [Diagnostics.Stopwatch]::StartNew()
    try { $a = Chay $k @('-HanGiay', '5') @{ STUB_CHAU_PID = $pidf } }
    finally {
        $w.Stop()
        if (Test-Path -LiteralPath $pidf) { Stop-Process -Id ([int](Get-Content -LiteralPath $pidf)) -Force -ErrorAction SilentlyContinue }
    }
    $them = $w.Elapsed.TotalSeconds - $w0.Elapsed.TotalSeconds
    if ($them -ge 15) { throw "cong thoat roi ma cho CHAU them $([math]::Round($them))s so voi luot nen $([math]::Round($w0.Elapsed.TotalSeconds))s (HanGiay 5)" }
    if (-not $IsWindows -and $a.ra -match 'cong_cu kiem-tra\s+rc=0') { throw 'CHAU con giu stdout ma cong van DAT' }
    if (-not $IsWindows -and $a.rc -ne 4) { throw "CHAU con giu stdout ma rc_script=$($a.rc), mong 4 (KHONG DO DUOC)" }
}

# Lõi của cổng: hai lần build ra zip KHÁC nhau ⇒ ĐỎ. Mọi ca khác dùng stub ghi CÙNG byte, nên bỏ `$ha -eq $hb` không ca nào thấy.
Ca 't17 hai zip KHAC nhau => tat dinh DO' {
    $k = Dung-Kho
    $a = Chay $k @('-Muc', 'day-du') @{ STUB_BUNDLE = 'khac' }
    if ($a.ra -notmatch 'release-bundle tất định\s+rc=1' -or $a.rc -eq 0) { throw "a.zip khac b.zip ma tat dinh khong DO (rc_script=$($a.rc))" }
}

# Cổng ĐỎ (rc=1) mà để lại CHÁU giữ stdout — hai sự cố hay đi cùng nhau (ca hỏng bỏ dở phần dọn). rc đã đọc từ chính
# tiến trình ⇒ vẫn ĐỎ; hạ thành KHÔNG ĐO ĐƯỢC là exit 4 + "ĐỎ 0" + log cổng không in (đo trên 131c608).
Ca 't18 cong rc=1 + CHAU giu stdout => van DO, in log' {
    $k = Dung-Kho
    $pidf = Join-Path (Split-Path $k) 'chau.pid'
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu.py') -Encoding utf8NoBOM -Value @'
import os, subprocess, sys
if sys.argv[1:2] == ["kiem-tra"]:
    import time
    print("DONG-LOI-CUA-CONG-T18", flush=True)
    p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    open(os.environ["STUB_CHAU_PID"], "w").write(str(p.pid))
    time.sleep(3)
    sys.exit(1)
sys.exit(0)
'@
    try { $a = Chay $k @('-HanGiay', '5') @{ STUB_CHAU_PID = $pidf } }
    finally { if (Test-Path -LiteralPath $pidf) { Stop-Process -Id ([int](Get-Content -LiteralPath $pidf)) -Force -ErrorAction SilentlyContinue } }
    if ($a.rc -ne 1) { throw "cong rc=1 ma rc_script=$($a.rc), mong 1 (DO)" }
    if ($a.ra -notmatch 'DONG-LOI-CUA-CONG-T18') { throw 'cong DO ma log cua no khong duoc in' }
    # Ngoài Windows script chờ cháu tới hạn 5 s. Cổng thoát ở giây 3 nên hạn CÒN LẠI ≈ 2 s: cột thời lượng ≈ 5 s — không phải 3
    # (bỏ phần chờ), không phải 3 + 5 (xả bằng CẢ hạn: đo 8,1 s), 13 s (xả 2×HanGiay), 15 s (sàn 12 s). Số in theo văn hoá của máy:
    # locale vi_VN in `5,1s` (đo: regex chỉ nhận dấu chấm ĐỎ oan 1/6 lượt dưới tải) — lỗi ấy chập chờn theo phép làm tròn, nên bộ
    # đọc tự kiểm trên một dòng CỐ ĐỊNH trước khi đọc dòng thật.
    $reGiay = 'cong_cu kiem-tra\s+rc=1\s+(\d+(?:[.,]\d+)?)s'
    if ('  cong_cu kiem-tra   rc=1        5,1s  ĐỎ' -notmatch $reGiay) { throw 'bo doc cot thoi luong khong nhan dau phay thap phan (locale vi_VN)' }
    if (-not $IsWindows) {
        $m = [regex]::Match($a.ra, $reGiay)
        if (-not $m.Success) { throw 'khong thay cot thoi luong cua cong_cu kiem-tra' }
        $g = [double]($m.Groups[1].Value -replace ',', '.')
        if ($g -lt 4.5 -or $g -gt 7.5) { throw "cot thoi luong ${g}s ngoai [4.5; 7.5] (HanGiay 5, cong thoat o giay 3)" }
    }
}

# rc KHÔNG đọc được (`ExitCode` = $null — lỗi handle của Start-Process trên Windows; getter ném cũng ra $null) phải là KHÔNG ĐO ĐƯỢC
# ở đường CHUNG, không chỉ ở nhánh xả-quá-hạn (đo trên bd62cad: `rc=  0.1s ĐỎ`, exit 1). Nạp NGUYÊN VĂN `Chay-Cong` như t11.
Ca 't19 ExitCode khong doc duoc => KHONG DO DUOC, khong DO' {
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $fn = $ast.Find({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Chay-Cong' }, $true)
    if (-not $fn) { throw 'khong thay ham Chay-Cong trong script' }
    $d = Join-Path ([IO.Path]::GetTempPath()) ('ccw-' + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $script:Rac += $d
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    $h = Join-Path $d 'h.ps1'
    Set-Content -LiteralPath $h -Encoding utf8NoBOM -Value (@'
Set-StrictMode -Version Latest
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$KetQua = New-Object System.Collections.ArrayList
$NhatKy = $PSScriptRoot; $Goc = $PSScriptRoot; $HanGiay = 5; $ChiTiet = $false
function Start-Process {
    $o = [pscustomobject]@{ HasExited = $true; ExitCode = $null }
    $o | Add-Member -MemberType ScriptMethod -Name WaitForExit -Value { $true }
    $o | Add-Member -MemberType ScriptMethod -Name WaitForExitAsync -Value { [Threading.Tasks.Task]::CompletedTask }
    return $o
}
'@ + "`n" + $fn.Extent.Text + "`n" + @'
Chay-Cong -Ten 'gia' -Tep 'khong-co' -DoiSo @()
Write-Host ("TRANG_THAI=" + $(switch ($KetQua[0].TrangThai) { 'ĐẠT' { 'DAT' } 'ĐỎ' { 'DO' } 'KHÔNG ĐO ĐƯỢC' { 'KDD' } default { '?' } }))
'@)
    $ra = (Doc-Utf8 { & $PwshExe -NoProfile -File $h 2>&1 } | ForEach-Object { "$_" }) -join "`n"
    if ($ra -notmatch 'TRANG_THAI=') { throw "harness khong chay toi het Chay-Cong: $ra" }
    if ($ra -notmatch 'TRANG_THAI=KDD') { throw "ExitCode null o duong chung ma khong ra KHONG DO DUOC: $ra" }
    # Cột rc in `-`, không in TRỐNG (bản vá lượt 5 khai vậy; thiếu vế này thì gỡ nó vẫn 20/20).
    if ($ra -notmatch 'gia\s+rc=-\s') { throw "ExitCode null ma cot rc khong in '-': $ra" }
}

# Đo được trên MỌI nền: đặt console 437 (mặc định kiểu Windows) ngay trong ca rồi đòi `Chay` vẫn thấy chữ tiếng Việt của script.
Ca 't20 console code page 437 => van doc dung output UTF-8 cua script' {
    $k = Dung-Kho
    New-Item -ItemType File -Path (Join-Path $k '.git/config.lock') | Out-Null
    $enc = [Console]::OutputEncoding
    try {
        try { [Console]::OutputEncoding = [Text.Encoding]::GetEncoding(437) } catch { throw "KHONG DO DUOC: khong dat duoc code page 437 ($($_.Exception.Message))" }
        $a = Chay $k
    } finally {
        [Console]::OutputEncoding = $enc
        Remove-Item -LiteralPath (Join-Path $k '.git/config.lock') -Force -ErrorAction SilentlyContinue
    }
    if ($a.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw 'console 437: output UTF-8 cua script bi giai ma thanh rac' }
}

# `AL_DICH` lên ĐẦU PATH SAU khi Tim-Python đã kiểm Python, mà cổng Python gọi theo TÊN: nếu nó là TEMP dùng chung (`/tmp/` 1777
# trên Linux) thì ai cũng đặt được `python` vào `<TEMP>/actionlint` ⇒ Python đã kiểm ≠ Python được chạy (cùng lớp t8, đường thứ ba).
Ca 't21 python gia trong <TEMP>/actionlint => cong Python khong DAT' {
    $k = Dung-Kho
    $tam = Join-Path (Split-Path $k) 'tmp'
    $al = Join-Path $tam 'actionlint'
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    foreach ($n in 'py', 'python', 'python3') {
        if ($IsWindows) { Set-Content -LiteralPath (Join-Path $al "$n.cmd") -Value '@exit /b 0' -Encoding ascii }
        else {
            $f = Join-Path $al $n
            Set-Content -LiteralPath $f -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
            & chmod +x $f
        }
    }
    $a = Chay $k @() @{ TMPDIR = $tam; TEMP = $tam; TMP = $tam; STUB_RC_cong_cu_py = '1' }
    if ($a.ra -notmatch 'cong_cu kiem-tra\s+rc=1') { throw "python gia trong TEMP/actionlint duoc chon, cong Python khong chay that (rc_script=$($a.rc))" }
}

# Gốc kho chứa dấu phân cách PATH của nền ⇒ AL_DICH (DẪN TỪ gốc) vỡ đôi trên PATH: tiền tố lên ĐẦU PATH của script VÀ của
# wrapper lease. Đo trên c8c2c6a: `python` giả trong tiền tố ⇒ 6/6 cổng ĐẠT, rc=0. Từ chối như gốc có wildcard (t10).
Ca 't22 goc kho co dau phan cach PATH => rc=2, noi dung nguyen nhan' {
    $k = Dung-Kho
    $moi = Join-Path (Split-Path $k) ('a' + $Sep + 'b')
    New-Item -ItemType Directory -Force -Path $moi | Out-Null
    & git clone -q $k (Join-Path $moi 'k')
    if ($LASTEXITCODE -ne 0) { throw "git clone vao duong dan co dau phan cach PATH that bai (rc=$LASTEXITCODE)" }
    New-Item -ItemType Directory -Force -Path (Join-Path $moi (Join-Path 'k' (Join-Path 'dist' 'actionlint'))) | Out-Null
    $a = Chay (Join-Path $moi 'k')
    if ($a.rc -ne 2 -or $a.ra -notmatch 'phân cách PATH') { throw "goc co dau phan cach PATH ma khong bi tu choi dung cho (rc=$($a.rc))" }
}

# `python` giả trong `dist/actionlint` (thư mục lên ĐẦU PATH sau khi Tim-Python đã kiểm): cổng Python phải chạy ĐÚNG tệp đã
# kiểm (đường dẫn tuyệt đối), không chạy `python` đầu PATH. Tệp CHƯA theo dõi để ca đo riêng chốt đường dẫn tuyệt đối (t24 đo
# chốt tệp THEO DÕI).
Ca 't23 python gia trong dist/actionlint => cong Python van chay tep DA KIEM' {
    $k = Dung-Kho
    $al = Join-Path $k (Join-Path 'dist' 'actionlint')
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    foreach ($n in 'py', 'python', 'python3') {
        if ($IsWindows) { Set-Content -LiteralPath (Join-Path $al "$n.cmd") -Value '@exit /b 0' -Encoding ascii }
        else {
            $f = Join-Path $al $n
            Set-Content -LiteralPath $f -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
            & chmod +x $f
        }
    }
    $a = Chay $k @() @{ STUB_RC_cong_cu_py = '1' }
    if ($a.ra -notmatch 'cong_cu kiem-tra\s+rc=1') { throw "python gia trong dist/actionlint duoc chon, cong Python khong chay tep da kiem (rc_script=$($a.rc))" }
}

# Tệp THEO DÕI dưới `dist/actionlint` (bị `.gitignore`, chỉ vào được bằng `git add -f`) là dữ liệu của NHÁNH, mà thư mục ấy lên
# ĐẦU PATH của wrapper lease (gọi `python` theo tên). Đo trên c8c2c6a với wrapper thật: lease ĐẠT dù bộ test thoát 1.
Ca 't24 tep THEO DOI duoi dist/actionlint => rc=2' {
    $k = Dung-Kho
    $al = Join-Path $k (Join-Path 'dist' 'actionlint')
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    Set-Content -LiteralPath (Join-Path $al 'python') -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
    & git -C $k add -f -- dist/actionlint
    & git -C $k -c user.email=t@t -c user.name=t commit -qm theo-doi
    $a = Chay $k
    if ($a.rc -ne 2 -or $a.ra -notmatch 'THEO DÕI') { throw "dist/actionlint co tep theo doi ma khong bi tu choi (rc=$($a.rc))" }
}

foreach ($d in $script:Rac) { Remove-Item -LiteralPath $d -Recurse -Force -ErrorAction SilentlyContinue }
$script:KetQua | ForEach-Object { Write-Host $_ }
$dat = @($script:KetQua | Where-Object { $_ -like 'DAT *' }).Count
Write-Host ("chay-cong-windows: {0}/{1} dat" -f $dat, $script:KetQua.Count)
if ($dat -ne $script:KetQua.Count -or $script:KetQua.Count -eq 0) { exit 1 }
exit 0
