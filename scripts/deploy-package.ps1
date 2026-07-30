<#
.SYNOPSIS
  Đóng gói + deploy skill tra-luat TỪ WINDOWS/PowerShell — bản đầy đủ, thay cho
  upload-skill-to-Package.ps1 (ngoài repo, D:\Quốc hội\).

.DESCRIPTION
  Song sinh của scripts/deploy-package.sh: CÙNG quy trình §10 DEV_TOOLING_GUIDE + §6 bước 7-8 kế hoạch
  guard-va-boc-tl-core, CÙNG các chốt, CÙNG mã lỗi. Ưu điểm so với script cũ ngoài repo: nằm TRONG repo
  nên `git pull` là có bản mới nhất, và chốt chống thụt lùi + quét bí mật dùng CHUNG nguồn với bản sh
  (scripts/deploy-guard.ps1 · scripts/pkg_secret_scan.py) nên hai đường không trôi lệch nhau.

  "LUÔN đóng gói ra bản mới nhất": bước 0 tự `git fetch` và CHẶN nếu cây tụt sau origin/master
  (CLAUDE.md §Quy ước deploy mục 2) — build từ cây tụt sau chính là cách Package bị thụt lùi.
  Muốn tự lấy bản mới về luôn thì thêm -Pull (fast-forward, KHÔNG merge/rebase tự động).

  MẶC ĐỊNH AN TOÀN: build + verify, KHÔNG đẩy. Muốn đẩy thật phải nêu -Push.

.PARAMETER Push        Đẩy lên Drive/Package sau khi gate + verify xanh.
.PARAMETER NoTest      Bỏ gate 8 bước (CHỈ khi vừa chạy gate riêng ở commit NÀY).
.PARAMETER Pull        Tự fast-forward về origin/master trước khi build (không merge/rebase tự động).
.PARAMETER ForceOlder  Ghi đè dù Drive đang bản mới hơn/cùng số (chuyển tiếp cho deploy-guard.ps1).
.PARAMETER Out         Đường dẫn zip output. Mặc định <thư-mục-cha-repo>\tra-luat-skill-v<VER>-gws3env.zip
.PARAMETER Python      Lệnh python. Mặc định tự tìm: python → py -3 → python3.

.EXAMPLE
  .\scripts\deploy-package.ps1                    # gate + build + verify (KHÔNG đẩy)
.EXAMPLE
  .\scripts\deploy-package.ps1 -Pull -Push        # lấy bản mới nhất rồi deploy
.EXAMPLE
  .\scripts\deploy-package.ps1 -Push -ForceOlder  # cố ý ghi đè bản trên Drive

.OUTPUTS
  exit 0 = xong · 1 = gate đỏ · 2 = build/verify hỏng · 3 = đẩy hỏng (gồm CHẶN THỤT LÙI)
#>
[CmdletBinding()]
param(
  [switch]$Push,
  [switch]$NoTest,
  [switch]$Pull,
  [switch]$ForceOlder,
  [string]$Out,
  [string]$Python,
  [string]$Repo
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false   # native rc KHÔNG throw — ta tự kiểm $LASTEXITCODE

# ── Xác định GỐC REPO, và FAIL RÕ RÀNG nếu không tìm được ──
# Mặc định script nằm ở <repo>\scripts\ nên gốc repo = lên HAI cấp. Nhưng nếu ai copy script ra chỗ
# khác (vd D:\Quốc hội\) thì "lên hai cấp" ra `D:\` và bước 0 chết với thông báo vô nghĩa
# "Cannot find path 'D:\VERSION'" — người đọc không thể suy ra nguyên nhân thật là SAI CHỖ ĐẶT.
# Đã sập thật một lượt. Nay: thử nhiều ứng viên, KIỂM dấu hiệu repo (VERSION + scripts/tl.py), và
# nếu không đạt thì in ra ĐÃ THỬ NHỮNG ĐÂU + hai cách chữa.
function Test-TlRepo {
  param([string]$p)
  if ([string]::IsNullOrWhiteSpace($p)) { return $false }
  return (Test-Path (Join-Path $p 'VERSION')) -and (Test-Path (Join-Path $p 'scripts/tl.py'))
}
$here = Split-Path -Parent $PSCommandPath
$cands = [ordered]@{}
if ($Repo) { $cands['-Repo'] = $Repo }
$cands['lên 2 cấp từ script (bố trí chuẩn <repo>\scripts\)'] = (Split-Path -Parent $here)
$cands['thư mục của script (nếu script ở gốc repo)']          = $here
$cands['thư mục đang đứng']                                    = (Get-Location).Path
$Root = $null
foreach ($k in $cands.Keys) {
  if (Test-TlRepo $cands[$k]) { $Root = (Resolve-Path $cands[$k]).Path; break }
}
if (-not $Root) {
  Write-Host "  [FAIL] Không tìm được gốc repo tra-luat (cần có VERSION + scripts/tl.py)." -ForegroundColor Red
  foreach ($k in $cands.Keys) { Write-Host ("         đã thử [{0}]: {1}" -f $k, $cands[$k]) -ForegroundColor Red }
  Write-Host '         Chữa — chọn MỘT:' -ForegroundColor Yellow
  Write-Host '           (a) Chạy bản TRONG repo:  <repo>\scripts\deploy-package.cmd   ← khuyên dùng' -ForegroundColor Yellow
  Write-Host '           (b) Giữ script ở chỗ khác thì nêu repo:  -Repo "C:\qh\tra-luat"' -ForegroundColor Yellow
  Write-Host '         Đừng để HAI bản deploy-package.ps1 song song — chúng sẽ trôi lệch nhau.' -ForegroundColor Yellow
  exit 2
}
Set-Location $Root
$State = Join-Path $Root 'scripts/.tl_state/deploy'
New-Item -ItemType Directory -Force -Path $State | Out-Null

function Say  { param($m) Write-Host "`n== $m ==" -ForegroundColor White }
function Ok   { param($m) Write-Host "  [OK]   $m" -ForegroundColor Green }
function Bad  { param($m) Write-Host "  [FAIL] $m" -ForegroundColor Red }
function Warn { param($m) Write-Host "  [WARN] $m" -ForegroundColor Yellow }

# ── tìm python ──
function Resolve-Python {
  if ($Python) { return $Python }
  foreach ($c in @('python', 'python3')) {
    $p = Get-Command $c -ErrorAction SilentlyContinue
    if ($p) { return $p.Source }
  }
  if (Get-Command 'py' -ErrorAction SilentlyContinue) { return 'py' }
  throw 'không tìm được python (thử -Python "C:\Python313\python.exe")'
}
$PY = Resolve-Python
# `py` cần thêm -3; giữ dạng mảng để nối đối số cho gọn
$PYARGS = @(); if ([IO.Path]::GetFileNameWithoutExtension($PY) -eq 'py') { $PYARGS = @('-3') }
function Invoke-Py {
  # KHÔNG đặt tên tham số là $Args — đó là BIẾN TỰ ĐỘNG của PowerShell trong hàm, nên `@Args` sẽ nở
  # ra mảng tự động (RỖNG) thay vì đối số ta truyền ⇒ python chạy KHÔNG đối số, đọc stdin, EOF, rc=0
  # và output rỗng: gate "xanh rc=0" mà chẳng chạy gì. Đã sập đúng bẫy này ở lượt chạy đầu.
  param([string[]]$Argv, [string]$OutFile)
  if ($OutFile) { & $PY @PYARGS @Argv *> $OutFile } else { & $PY @PYARGS @Argv }
  return $LASTEXITCODE
}

# ═════════════════ 0. VERSION khớp 3 chỗ · core.abbrev · không tụt sau master ═════════════════
Say '0. Tiền kiểm'
$VER  = (Get-Content (Join-Path $Root 'VERSION') -Raw).Trim()
$V_TL = ([regex]::Match((Get-Content (Join-Path $Root 'scripts/tl.py') -Raw), '(?m)^VERSION = "([^"]+)"')).Groups[1].Value
$V_SK = ([regex]::Match((Get-Content (Join-Path $Root 'SKILL.md') -Raw), 'LÕI VẬN HÀNH \(v([0-9.]+) — KERNEL\)')).Groups[1].Value
Write-Host "  VERSION=$VER · tl.py=$V_TL · SKILL.md=$V_SK"
if ($VER -ne $V_TL -or $VER -ne $V_SK) {
  Bad '3 chỗ VERSION LỆCH — sửa cho khớp rồi chạy lại (selftest có guard skill_md_version_matches_VERSION).'
  exit 1
}
Ok "khớp v$VER"

# core.abbrev=7 — điều kiện TẤT ĐỊNH của gate. Xem chú thích dài trong deploy-package.sh và
# ★ v1.35.78 (r241): auto-abbrev của git trôi theo số commit ⇒ golden/determinism/doc-claims đỏ giả.
$ab = (& git config --local core.abbrev 2>$null)
if ($ab -ne '7') {
  & git config --local core.abbrev 7
  Warn "đã đặt core.abbrev=7 cho repo này (trước đó: '$(if($ab){$ab}else{'<chưa đặt, git tự suy>'})') — gate cần ngưỡng cố định"
} else { Ok 'core.abbrev=7 (khớp CI)' }
if (Test-Path (Join-Path $Root '.git/shallow')) {
  Warn 'repo đang SHALLOW — doc-claims-check sẽ đỏ vì SHA cũ không resolve được; chữa: git fetch --unshallow'
}

# CLAUDE.md §Quy ước deploy mục 2: build từ cây TỤT SAU = đóng gói bản thụt lùi.
& git fetch origin master --quiet 2>$null
$behind = (& git rev-list --count 'HEAD..origin/master' 2>$null)
if ($LASTEXITCODE -eq 0 -and $behind -and [int]$behind -gt 0) {
  if ($Pull) {
    & git merge --ff-only origin/master
    if ($LASTEXITCODE -ne 0) {
      Bad "cây tụt sau origin/master $behind commit và KHÔNG fast-forward được — phải merge/rebase tay rồi chạy lại gate."
      exit 1
    }
    Warn "đã fast-forward $behind commit từ origin/master — ĐỌC LẠI VERSION"
    $VER = (Get-Content (Join-Path $Root 'VERSION') -Raw).Trim()
    Ok "VERSION sau khi cập nhật: v$VER"
  } else {
    Bad "cây TỤT SAU origin/master $behind commit — build bây giờ là đóng gói bản cũ."
    Write-Host '        Chữa: thêm -Pull (fast-forward), hoặc git merge/rebase tay rồi chạy lại gate.' -ForegroundColor Red
    exit 1
  }
} else { Ok 'không tụt sau origin/master' }

# ═════════════════ 1. Gate offline 8 bước ═════════════════
if (-not $NoTest) {
  Say '1. Gate offline 8 bước'
  $gates = [ordered]@{
    selftest    = @('scripts/tl.py', '--selftest')
    gen_inst    = @('scripts/gen_instructions.py', '--selftest')
    workflow    = @('scripts/tl.py', 'workflow-audit', '--strict', '--json')
    golden      = @('scripts/tl.py', 'golden-test', '--json')          # KHÔNG BAO GIỜ --write ở đây (R6)
    docclaims   = @('scripts/tl.py', 'doc-claims-check', '--strict', '--json')
    determinism = @('scripts/tl.py', 'determinism-audit', '--strict', '--json')
    relcheck    = @('scripts/tl.py', 'release-check', '--full', '--json')
    relverify   = @('scripts/tl.py', 'release-verify', 'RELEASE_MANIFEST.json', '--strict', '--json')
  }
  $fail = $false
  foreach ($n in $gates.Keys) {
    $f = Join-Path $State "$n.out"
    $rc = Invoke-Py -Argv $gates[$n] -OutFile $f
    # -Raw trên tệp RỖNG trả $null ⇒ [regex]::Match ném "Value cannot be null" (đã sập lượt đầu).
    $txt = if (Test-Path $f) { [string](Get-Content $f -Raw) } else { '' }
    if ($null -eq $txt) { $txt = '' }
    $pass = $false; $extra = ''
    if ($n -in @('selftest', 'gen_inst')) {
      $extra = ($txt -split "`n" | Where-Object { $_.Trim() } | Select-Object -Last 1)
      # N/N: hai số BẰNG NHAU mới là xanh (regex backreference), không chỉ "có dấu /"
      $pass = ($rc -eq 0) -and ($extra -match '(\d+)/\1\b')
    } else {
      $m = [regex]::Match($txt, '"ok":\s*(true|false)')
      $extra = if ($m.Success) { '"ok": ' + $m.Groups[1].Value } else { '' }
      $pass = ($rc -eq 0) -and ($m.Success) -and ($m.Groups[1].Value -eq 'true')
    }
    if ($pass) { Ok ("{0,-12} rc={1} {2}" -f $n, $rc, $extra); continue }

    # doc-claims-check trên clone SHALLOW: SHA cũ trong changelog_archive không resolve được ⇒
    # SHA_NOT_A_COMMIT là khuyết MÔI TRƯỜNG. Chỉ hạ WARN khi repo THẬT SỰ shallow VÀ mọi cờ đều
    # thuộc loại đó; cờ loại khác ⇒ đỏ như thường. Chữa dứt điểm: git fetch --unshallow.
    if ($n -eq 'docclaims' -and (Test-Path (Join-Path $Root '.git/shallow'))) {
      try {
        $j = $txt | ConvertFrom-Json
        $flags = @($j.flags)
        if ($flags.Count -gt 0 -and -not ($flags | Where-Object { $_.reason -ne 'SHA_NOT_A_COMMIT' })) {
          Warn ("{0,-12} rc={1} — {2} cờ, TẤT CẢ là SHA_NOT_A_COMMIT trên clone SHALLOW ⇒ khuyết môi trường, KHÔNG chặn" -f $n, $rc, $flags.Count)
          Warn '       muốn chắc: git fetch --unshallow rồi chạy lại — cờ phải về 0'
          continue
        }
      } catch { }
    }
    Bad ("{0,-12} rc={1} {2}  → soi {3}" -f $n, $rc, $extra, $f)
    if ($n -eq 'relverify' -and $txt -match '"failed"') {
      Warn "       cây đã đổi so với manifest — chữa: $PY scripts/tl.py release-manifest --out RELEASE_MANIFEST.json"
      try {
        foreach ($x in (($txt | ConvertFrom-Json).failed | Select-Object -First 8)) {
          Write-Host ("         · {0}: {1}→{2} byte" -f $x.path, $x.expected_size, $x.actual_size) -ForegroundColor Yellow
        }
      } catch { }
    }
    $fail = $true
  }
  if ($fail) { Bad 'GATE ĐỎ — DỪNG, không build/không đẩy (golden diff = BUG của thay đổi, R6)'; exit 1 }
  Ok 'gate xanh'
} else {
  Warn 'BỎ QUA gate (-NoTest) — chỉ hợp lệ khi vừa chạy gate riêng ở commit NÀY'
}

# ═════════════════ 2. Build bundle ×2, đòi same-SHA ═════════════════
# release-bundle TỪ CHỐI ghi vào trong skill root (OUT_INSIDE_SKILL_ROOT → tự chuyển ra ngoài, kẻo zip
# nuốt chính nó) ⇒ mặc định xuất ra thư mục CHA, và luôn đọc đường dẫn THẬT từ khoá "out" của JSON.
Say '2. Build bundle ×2 (đòi tất định same-SHA)'
$buildDir = Split-Path -Parent $Root
$zipWant = if ($Out) { $Out } else { Join-Path $buildDir "tra-luat-skill-v$VER-gws3env.zip" }
# KHÔNG đặt tên bắt đầu bằng dấu '.': trên Unix đó là tệp ẨN, và `Get-Item` KHÔNG trả tệp ẩn khi
# thiếu -Force ⇒ Test-Path thấy có mà Get-Item ném "Could not find item" (đã sập đúng bẫy này).
$zip2Want = Join-Path $buildDir 'tl-reproducibility-probe.zip'
Remove-Item -Force -ErrorAction SilentlyContinue $zipWant, $zip2Want

function Get-BundleOut {
  param([string]$Want, [string]$Tag)
  $f = Join-Path $State "bundle$Tag.out"
  $rc = Invoke-Py -Argv @('scripts/tl.py', 'release-bundle', '--out', $Want, '--json') -OutFile $f
  if ($rc -ne 0) { Bad "release-bundle lỗi (rc=$rc) — soi $f"; exit 2 }
  try { $out = (Get-Content $f -Raw | ConvertFrom-Json).out } catch { Bad "không parse được output release-bundle — soi $f"; exit 2 }
  if (-not $out -or -not (Test-Path $out) -or (Get-Item -Force $out).Length -eq 0) {
    Bad "release-bundle báo ok nhưng KHÔNG có zip thật: '$out' — soi $f"; exit 2
  }
  return $out
}
$ZIP  = Get-BundleOut -Want $zipWant  -Tag '1'
$ZIP2 = Get-BundleOut -Want $zip2Want -Tag '2'
if ($ZIP -ne $zipWant) { Warn "release-bundle CHUYỂN chỗ xuất → $ZIP (không ghi được trong skill root)" }
$S1 = (Get-FileHash $ZIP  -Algorithm SHA256).Hash.ToLower()
$S2 = (Get-FileHash $ZIP2 -Algorithm SHA256).Hash.ToLower()
if ($S1 -ne $S2) { Bad "BUILD KHÔNG TẤT ĐỊNH: $S1 ≠ $S2 — có thứ phi-tất-định lọt vào gói, DỪNG."; exit 2 }
Remove-Item -Force $ZIP2
Ok "same-SHA ✓ sha256=$($S1.Substring(0,16))… · $((Get-Item -Force $ZIP).Length) byte · $ZIP"

# ═════════════════ 3. Verify nội dung gói ═════════════════
Say '3. Verify nội dung gói'
$tmp = Join-Path ([IO.Path]::GetTempPath()) ("tlpkg_" + [Guid]::NewGuid().ToString('N').Substring(0, 8))
try {
  Expand-Archive -Path $ZIP -DestinationPath $tmp -Force
  $top = (Get-ChildItem -Force $tmp | Select-Object -First 1).Name
  $pkg = Join-Path $tmp $top

  $zver = (Get-Content (Join-Path $pkg 'VERSION') -Raw).Trim()
  if ($zver -ne $VER) { Bad "VERSION trong gói ($zver) ≠ repo ($VER)"; exit 2 }
  Ok "VERSION trong gói = $zver"

  # 3b. thứ TUYỆT ĐỐI không được vào gói (dev-side + secrets)
  $leak = $false
  foreach ($p in @('.git', '.claude', '.githooks', '.github', 'CLAUDE.md',
                   'tra_luat_config.json', 'tra_luat_config.v2.json',
                   'claude-code-best-practice', 'references/changelog_archive')) {
    if (Test-Path (Join-Path $pkg $p)) { Bad "RÒ: gói chứa '$p'"; $leak = $true }
  }
  # -Force BẮT BUỘC: không có nó Get-ChildItem BỎ QUA tệp ẩn ⇒ bộ tìm secrets sẽ MÙ với '.env',
  # '.netrc', '.tl_secrets'… Đây là lỗ an ninh thật, không phải chuyện đếm cho đẹp.
  $secretFiles = Get-ChildItem -Force $pkg -Recurse -File -ErrorAction SilentlyContinue |
                 Where-Object { $_.Name -like '*.enc' -or $_.Name -like '*cookie*' -or
                                $_.Name -like '*token*' -or $_.Name -like 'credentials*' }
  if ($secretFiles) {
    Bad 'RÒ: gói chứa tệp secrets (*.enc/cookie/token/credentials):'
    $secretFiles | ForEach-Object { Write-Host "        $($_.FullName.Substring($pkg.Length+1))" -ForegroundColor Red }
    $leak = $true
  }
  if (-not $leak) { Ok 'không có tệp dev-side/secrets trong gói' }

  # 3c. quét bí mật trong NỘI DUNG — bảng mẫu DÙNG CHUNG với bản sh (scripts/pkg_secret_scan.py)
  $scanOut = & $PY @PYARGS (Join-Path $Root 'scripts/pkg_secret_scan.py') $pkg 2>&1 | Out-String
  if ($LASTEXITCODE -ne 0) {
    Bad 'QUÉT BÍ MẬT BẮT ĐƯỢC trong gói — DỪNG, KHÔNG đẩy:'
    $scanOut -split "`n" | Where-Object { $_.Trim() } | ForEach-Object { Write-Host "        $_" -ForegroundColor Red }
    $leak = $true
  } else { Ok 'quét bí mật: sạch' }
  if ($leak) { Bad 'gói KHÔNG đạt — dừng trước khi đẩy'; exit 2 }

  # 3d. release-verify CHẠY TRONG GÓI (manifest tự mô tả)
  if (Test-Path (Join-Path $pkg 'RELEASE_MANIFEST.json')) {
    $f = Join-Path $State 'relverify_inzip.out'
    Push-Location $pkg
    try { & $PY @PYARGS 'scripts/tl.py' 'release-verify' 'RELEASE_MANIFEST.json' '--strict' '--json' *> $f }
    finally { Pop-Location }
    if ((Get-Content $f -Raw) -match '"ok":\s*true') { Ok 'release-verify TRONG gói: ok' }
    else { Bad "release-verify TRONG gói ĐỎ — soi $f"; exit 2 }
  } else { Warn 'gói không có RELEASE_MANIFEST.json — bỏ qua verify trong gói' }

  # đếm SAU khi release-verify đã chạy ⇒ loại __pycache__ do chính lần chạy đó sinh ra
  $files = (Get-ChildItem -Force $pkg -Recurse -File | Where-Object { $_.FullName -notmatch '__pycache__' }).Count
  Ok "gói: $files tệp · top-level '$top'"
} finally {
  Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $tmp
}

# ═════════════════ 4. Đẩy Drive ═════════════════
if (-not $Push) {
  Say 'XONG (build-only)'
  Write-Host "  Gói sẵn sàng: $ZIP"
  Write-Host '  Đẩy thật:     .\scripts\deploy-package.ps1 -Push'
  exit 0
}

Say '4. Đẩy lên Drive/Package'
# CHỐT CHỐNG THỤT LÙI — dùng CHUNG deploy-guard.ps1 (đừng inline lại phép so ở đây)
$guard = Join-Path $Root 'scripts/deploy-guard.ps1'
if ($ForceOlder) { & $guard -Version $VER -ForceOlder } else { & $guard -Version $VER }
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $PY @PYARGS 'scripts/tl.py' 'drive-push' $ZIP '--rename-to-file'
if ($LASTEXITCODE -ne 0) { Bad 'drive-push lỗi (cần `gws auth login` có quyền GHI Drive)'; exit 3 }
Ok 'đã đẩy'

# ═════════════════ 5. Verify SAU đẩy — byte-match ═════════════════
Say '5. Verify sau đẩy — tải về đối chiếu byte'
$dl = Join-Path $State 'verify-download.zip'
Remove-Item -Force -ErrorAction SilentlyContinue $dl
& gws drive files get --params '{"fileId":"1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P","alt":"media"}' --output $dl *> $null
if (-not (Test-Path $dl) -or (Get-Item -Force $dl).Length -eq 0) { Bad 'không tải lại được Package để verify'; exit 3 }
$S3 = (Get-FileHash $dl -Algorithm SHA256).Hash.ToLower()
if ($S3 -ne $S1) { Bad "LỆCH BYTE: local=$($S1.Substring(0,16))… drive=$($S3.Substring(0,16))… — đẩy KHÔNG toàn vẹn"; exit 3 }
Ok "BYTE-MATCH ✓ sha256 Drive = local ($($S1.Substring(0,16))…)"

$dtmp = Join-Path ([IO.Path]::GetTempPath()) ("tlver_" + [Guid]::NewGuid().ToString('N').Substring(0, 8))
try {
  Expand-Archive -Path $dl -DestinationPath $dtmp -Force
  $dTop = (Get-ChildItem -Force $dtmp | Select-Object -First 1).Name
  $dver = (Get-Content (Join-Path $dtmp "$dTop/VERSION") -Raw).Trim()
  if ($dver -ne $VER) { Bad "VERSION trên Drive ($dver) ≠ $VER"; exit 3 }
  Ok "VERSION trên Drive = $dver"
} finally {
  Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $dtmp
  Remove-Item -Force -ErrorAction SilentlyContinue $dl
}

Say "DEPLOY XONG — Package = v$VER"
Write-Host "  Phiên Cowork mới bootstrap từ zip này sẽ nhận v$VER."
exit 0
