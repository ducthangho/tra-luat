#Requires -Version 7.0
# Phản chứng cho `.claude/dev/chay-cong-windows.ps1` — dựng một kho GIẢ (đích cổng là stub) rồi chạy
# script THẬT, byte-identical, trong tiến trình riêng. Mỗi ca khoá một lớp của cross-review PR #602:
#   t1 trang-thai-lac-quan-song-sot-cau-lenh-nem  release-bundle rc=0 mà không ghi zip / zip CŨ ⇒ ĐỎ
#   t2 bo-giai-cong-cu-theo-ten-thu-tu            `bash.exe` nuốt argv đầu PATH ⇒ không được ĐẠT
#   t3 runner-tu-nhiem-cay-dang-do                sau một lượt, `git status` của kho giả SẠCH
#   t4 nhan-noi-hon-phep-do (nếp git)             `.git/config.lock` ⇒ rc=4, không in "→ 7" suông
#   t5 nhan-noi-hon-phep-do (khởi động)           Start-Process hỏng ⇒ không in "TREO"
#   t6 guong-ci-bo-dieu-kien-nen                  bước ci.yml `runner.os != 'Windows'` ⇒ script bỏ trên Windows
#   t7 sua-moi-truong-phien-goi                   PATH dùng dấu phân cách của nền, không chèn lặp AL_DICH
#   t8 bo-giai-cong-cu-theo-ten-thu-tu            `python` thoát 0 cho mọi lời gọi ⇒ không được ĐẠT
#   t9 han-mac-dinh-duoi-thoi-luong-da-do         mặc định -HanGiay ≥ `timeout-minutes` của job CI
#   t10 duong-dan-du-lieu-thanh-mau-wildcard      gốc kho dưới `…[1]…` ⇒ rc=2 + nói "wildcard", không "không tìm thấy gốc"
#   t11 nhan-noi-hon-phep-do (giết)               `Kill` ném, tiến trình còn sống ⇒ không in "ĐÃ GIẾT"
#   t12 nhan-noi-hon-phep-do (tham số)            `-HanGiay 0` bị từ chối, không thành "TREO > 0s"
#   t13 do-loi-goi-khong-do-hieu-qua (git)        biến môi trường đè `core.abbrev` ⇒ rc=4, không in "→ 7" suông
#   t14 cong-chay-ngoai-hop-dong-chay-cong        bundle treo quá `-HanGiay` ⇒ không ĐẠT, không chờ trọn
#   t15 do-loi-goi-khong-do-hieu-qua (zip)        zip cũ KHÔNG xoá được + bundle rc=0 không ghi ⇒ không ĐẠT
# ĐỘT BIẾN để đo răng (đo trên pwsh 7.4.6/Linux): `-Script` trỏ f2392df ⇒ 0/15; trỏ 8b82d40 ⇒ 12/15, đỏ đúng
# t13 t14 t15. Gỡ riêng MỘT mảnh vá thì chỉ ca của mảnh ấy ĐỎ (20 đột biến; riêng gỡ `exit 4` của nếp git
# đỏ cả t4 lẫn t13 vì hai ca dùng chung chốt ấy). Mảnh TƯƠNG ĐƯƠNG, không ca nào đo được — khai thẳng:
# `[bool]$ha`, `[string]$ban`, `-ErrorAction Stop` của Start-Process (nó vốn ném lỗi kết thúc).
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
    sys.exit(1 if m == "ghi-rc1" else 0)
sys.exit(0)
'@

$script:Rac = @()
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
        $ra = & $PwshExe -NoProfile -File (Join-Path $Kho '.claude/dev/chay-cong-windows.ps1') @Doi 2>&1
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
        Set-Content -LiteralPath (Join-Path $shim 'bash.exe') -Value "#!/bin/sh`nexit 0" -Encoding utf8NoBOM
        & chmod +x (Join-Path $shim 'bash.exe')
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
    $tam = Join-Path (Split-Path $k) 'tmp'
    $al = Join-Path $tam 'actionlint'
    New-Item -ItemType Directory -Force -Path $al | Out-Null
    Set-Content -LiteralPath (Join-Path $k 'ops/cong_cu.py') -Encoding utf8NoBOM -Value @'
import os, sys
al = os.environ.get("AL_DICH", "")
ds = os.environ.get("PATH", "").split(os.pathsep)
# pwsh tự chèn thư mục của nó vào ĐẦU PATH lúc khởi động, nên trên nền không phải Windows
# `"$AlDich;$env:PATH"` dán AL_DICH vào thư mục ấy chứ không đụng mục AL_DICH có sẵn —
# chỉ đếm `ds.count(al)` là ca KHÔNG CÓ RĂNG trên Linux (đã đo: bản gốc vẫn qua).
dan = os.name != "nt" and any(";" in d for d in ds)
sys.exit(0 if al and ds.count(al) == 1 and not dan else 7)
'@
    # PATH đã có sẵn AL_DICH = lượt thứ hai trong cùng một phiên.
    $a = Chay $k @() @{ TMPDIR = $tam; TEMP = $tam; TMP = $tam; PATH = "$al$Sep$env:PATH" }
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
    $ra = (& $PwshExe -NoProfile -File $h 2>&1 | ForEach-Object { "$_" }) -join "`n"
    if ($ra -notmatch 'TRANG_THAI=KHÔNG ĐO ĐƯỢC SO_KILL=[1-9]') { throw "harness khong chay toi Kill: $ra" }
    if ($ra -match 'ĐÃ GIẾT') { throw 'Kill nem, tien trinh con song ma van in "DA GIET"' }
}

Ca 't12 -HanGiay 0 bi tu choi, khong thanh "TREO > 0s"' {
    $k = Dung-Kho
    $a = Chay $k @('-HanGiay', '0')
    if ($a.ra -match 'TREO\s+>\s*0s') { throw 'HanGiay 0 duoc nhan: moi cong "TREO > 0s"' }
    if ($a.rc -eq 0 -or $a.ra -notmatch 'HanGiay') { throw "HanGiay 0 khong bi tu choi dung cho (rc=$($a.rc))" }
}

Ca 't13 bien moi truong de core.abbrev => rc=4, khong in "→ 7" suong' {
    $k = Dung-Kho
    $a = Chay $k @() @{ GIT_CONFIG_COUNT = '1'; GIT_CONFIG_KEY_0 = 'core.abbrev'; GIT_CONFIG_VALUE_0 = '8' }
    if ($a.rc -ne 4 -or $a.ra -notmatch 'KHÔNG ĐẶT ĐƯỢC') { throw "git dung abbrev 8 ma script bao nep dung (rc=$($a.rc))" }
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

foreach ($d in $script:Rac) { Remove-Item -LiteralPath $d -Recurse -Force -ErrorAction SilentlyContinue }
$script:KetQua | ForEach-Object { Write-Host $_ }
$dat = @($script:KetQua | Where-Object { $_ -like 'DAT *' }).Count
Write-Host ("chay-cong-windows: {0}/{1} dat" -f $dat, $script:KetQua.Count)
if ($dat -ne $script:KetQua.Count -or $script:KetQua.Count -eq 0) { exit 1 }
exit 0
