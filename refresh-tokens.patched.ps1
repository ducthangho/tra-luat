# ============================================================================
#  refresh-tokens.ps1 — 1-CLICK làm tươi credential NLM + gws trên máy LOCAL
#  rồi ĐẨY lên Drive (mã hoá) để Cowork/Chat tự nhận bản mới.
#
#  VÌ SAO: NLM cookie (Google session) hết hạn RẤT NHANH (~1h); gws OAuth cred
#  bền hơn (hàng tuần). Cowork/Chat là sandbox KHÔNG mở được browser để login —
#  nên phải login TƯƠNG TÁC ở máy này (có browser) rồi propagate qua Drive.
#
#  ★ THÔNG MINH: mỗi cred CHỈ login lại khi ĐÃ CHẾT (probe canary LIVE trước).
#    Còn sống → BỎ QUA login (tránh vướng màn OAuth "Đăng nhập bằng Google" lỗi),
#    chỉ re-stage bản đang-sống lên Drive. Ép login lại bằng -Force.
#
#  Script CHỈ ORCHESTRATE lệnh skill sẵn có (nguyên tắc #15 SCRIPT-REUSE GATE):
#    NLM : (nếu chết) `nlm login`      -> `tl nlm-auth-stage` -> verify canary LIVE
#    gws : (nếu chết) `gws auth login` -> `tl gws-auth-stage` -> verify `tl gws-ping`
#    (tùy chọn) -Bundle -> `tl secrets-set --gws --nlm` (cần TL_MASTER_KEY)
#
#  CÁCH DÙNG (hoặc double-click refresh-tokens.cmd):
#    .\refresh-tokens.ps1              # làm tươi CẢ nlm + gws (chỉ login cái đã chết)
#    .\refresh-tokens.ps1 -Nlm         # chỉ NLM
#    .\refresh-tokens.ps1 -Gws         # chỉ gws
#    .\refresh-tokens.ps1 -Check       # CHỈ kiểm trạng thái (không login/không stage)
#    .\refresh-tokens.ps1 -Force       # ép login lại DÙ đang sống
#    .\refresh-tokens.ps1 -NoStage     # login local xong KHÔNG đẩy Drive
#    .\refresh-tokens.ps1 -Bundle      # đồng bộ thêm master-key bundle
# ============================================================================
param(
  [switch]$Nlm,
  [switch]$Gws,
  [switch]$Bundle,
  [switch]$NoStage,
  [switch]$Check,
  [switch]$Force
)
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

# ---- Định vị repo skill (giống upload-skill-to-Package.ps1) ----
$Root = Join-Path $PSScriptRoot "tra-luat"
if (-not (Test-Path $Root)) { $Root = "D:\Quốc hội\tra-luat" }
if (-not (Test-Path $Root)) { $Root = "C:\Users\admin\Downloads\tra-luat" }
if (-not (Test-Path $Root)) { Write-Host "[LỖI] không thấy thư mục skill: $Root" -ForegroundColor Red; exit 1 }
Set-Location $Root
$PY = "python"
$TL = Join-Path $Root "scripts\tl.py"

# Mặc định: không chọn -Nlm/-Gws nào = làm CẢ HAI
$doNlm = $Nlm -or (-not $Nlm -and -not $Gws)
$doGws = $Gws -or (-not $Nlm -and -not $Gws)

function Test-GwsLive {
  & $PY $TL gws-ping --env code *> $null
  return ($LASTEXITCODE -eq 0)
}
function Test-NlmLive {
  # canary M1 (_nlm_auth_alive) — probe LIVE THẬT, KHÔNG tin `nlm login --check`
  $code = @'
import sys
sys.path.insert(0, "scripts")
import tl
tl.build_parser()
alive, msg = tl._imp("tl_gws")._nlm_auth_alive(tl.NLM_BASE_NOTEBOOK, 40)
print("     " + ("sống — " if alive else "CHẾT — ") + str(msg))
sys.exit(0 if alive else 1)
'@
  & $PY -c $code
  return ($LASTEXITCODE -eq 0)
}
function Get-GcloudDriveStatus {
  # 2026-07-07: gcloud = nguồn token DỰ PHÒNG cho `tl drive-push --via gcloud` (OAuth client của gcloud là
  # PRODUCTION — refresh token KHÔNG chết sau 7 ngày như app Testing của gws). Chỉ báo trạng thái, không login hộ.
  if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) { return "KHÔNG có gcloud trên PATH" }
  try { $tok = (& gcloud auth print-access-token 2>$null | Select-Object -First 1) } catch { $tok = "" }
  if ($tok) { return "SỐNG ✓ (drive-push fallback sẵn sàng; nếu push bị 403 thiếu scope: gcloud auth login --enable-gdrive-access)" }
  return "CHƯA login → gcloud auth login --enable-gdrive-access"
}

Write-Host "== refresh-tokens · repo=$Root ==" -ForegroundColor Cyan

# ---------------- CHẾ ĐỘ -Check: chỉ báo trạng thái, KHÔNG login/stage ----------------
if ($Check) {
  Write-Host "[CHECK] Kiểm trạng thái credential LIVE (không login/stage)…" -ForegroundColor Cyan
  if ($doGws) {
    if (Test-GwsLive) { Write-Host "  gws/direct-media : SỐNG ✓" -ForegroundColor Green }
    else { Write-Host "  gws/direct-media : CHẾT ✗ → .\refresh-tokens.ps1 -Gws" -ForegroundColor Red }
  }
  if ($doNlm) {
    Write-Host "  nlm auth (LIVE probe):" -ForegroundColor Cyan
    if (Test-NlmLive) { Write-Host "  => SỐNG ✓" -ForegroundColor Green }
    else { Write-Host "  => CHẾT ✗ → .\refresh-tokens.ps1 -Nlm" -ForegroundColor Red }
  }
  Write-Host "  gcloud (dự phòng drive-push): $(Get-GcloudDriveStatus)" -ForegroundColor Cyan
  exit 0
}

$fail = 0

# ============================ gws ============================
if ($doGws) {
  Write-Host ""
  Write-Host "[gws] kiểm trạng thái trước khi quyết login…" -ForegroundColor Cyan
  $gwsAlive = Test-GwsLive
  $gwsLoginOk = $true
  if ($gwsAlive -and -not $Force) {
    Write-Host "[gws] ✓ ĐANG SỐNG → BỎ QUA login (dùng -Force nếu muốn ép login lại)." -ForegroundColor Green
  } else {
    if ($gwsAlive) { Write-Host "[gws] -Force: login lại dù đang sống." -ForegroundColor Yellow }
    else { Write-Host "[gws] ✗ CHẾT → mở browser đăng nhập (gws auth login)…" -ForegroundColor Yellow }
    Write-Host "      → Hoàn tất trong browser. (Nếu màn 'Đăng nhập bằng Google' báo lỗi: OAuth app gws" -ForegroundColor DarkGray
    Write-Host "        đang ở chế độ Testing — xem ghi chú cuối script; gws thường còn sống nên hiếm khi cần.)" -ForegroundColor DarkGray
    gws auth login
    $gwsLoginRc = $LASTEXITCODE
    if ($gwsLoginRc -ne 0) {
      Write-Host "[gws] ⚠ login trả rc=$gwsLoginRc sau bước OAuth; kiểm canary trước khi kết luận lỗi..." -ForegroundColor Yellow
      if (Test-GwsLive) {
        Write-Host "[gws] ✓ credential local ĐÃ SỐNG dù CLI login trả lỗi cuối — tiếp tục stage." -ForegroundColor Green
      } else {
        Write-Host "[gws] ✗ login lỗi thật (canary vẫn chết)." -ForegroundColor Red
        $fail++; $gwsLoginOk = $false
      }
    } else { Write-Host "[gws] ✓ login OK." -ForegroundColor Green }
  }
  if ($gwsLoginOk) {
    # [patch] sync direct-media credentials.json (TƯƠI) → gws-ping/direct-media KHÔNG báo CHẾT-GIẢ vì file stale.
    #   `gws auth login` chỉ ghi credentials.enc; nhánh direct-media đọc credentials.json → phải export lại sau mỗi login.
    if (-not $NoStage) {
      try {
        $gwsCfgDir = Join-Path $env:USERPROFILE ".config\gws"
        if (-not (Test-Path $gwsCfgDir)) { New-Item -ItemType Directory -Force -Path $gwsCfgDir | Out-Null }
        $gwsCredJson = & gws auth export --unmasked 2>$null
        if ($LASTEXITCODE -eq 0 -and $gwsCredJson) {
          # WriteAllText = UTF-8 KHÔNG BOM (reader JSON không vỡ vì BOM)
          [System.IO.File]::WriteAllText((Join-Path $gwsCfgDir "credentials.json"), ($gwsCredJson -join "`n"))
          Write-Host "[gws] ✓ sync credentials.json (direct-media tươi)." -ForegroundColor DarkGray
        } else {
          Write-Host "[gws] ⚠ gws auth export rc=$LASTEXITCODE — bỏ qua sync credentials.json." -ForegroundColor DarkYellow
        }
      } catch { Write-Host "[gws] ⚠ sync credentials.json lỗi: $_" -ForegroundColor DarkYellow }
    }
    if ($NoStage) {
      Write-Host "[gws] BỎ QUA stage (-NoStage)." -ForegroundColor Yellow
    } else {
      Write-Host "[gws] đẩy gws cred (mã hoá) lên Drive (ghi đè tại chỗ)…" -ForegroundColor Cyan
      & $PY $TL gws-auth-stage
      if ($LASTEXITCODE -ne 0) { Write-Host "[gws] ✗ stage lỗi." -ForegroundColor Red; $fail++ }
    }
    if (Test-GwsLive) { Write-Host "[gws] ✓ verify: SỐNG (canary token OK)." -ForegroundColor Green }
    else { Write-Host "[gws] ✗ verify: vẫn CHẾT — kiểm: gws auth status." -ForegroundColor Red; $fail++ }
  }
}

# ============================ NLM ============================
if ($doNlm) {
  Write-Host ""
  Write-Host "[nlm] kiểm trạng thái trước khi quyết login…" -ForegroundColor Cyan
  $nlmAlive = Test-NlmLive
  $nlmLoginOk = $true
  if ($nlmAlive -and -not $Force) {
    Write-Host "[nlm] ✓ ĐANG SỐNG → BỎ QUA login (dùng -Force nếu muốn ép login lại)." -ForegroundColor Green
  } else {
    if ($nlmAlive) { Write-Host "[nlm] -Force: login lại dù đang sống." -ForegroundColor Yellow }
    else { Write-Host "[nlm] ✗ CHẾT → mở browser đăng nhập NotebookLM (nlm login)…" -ForegroundColor Yellow }
    Write-Host "      → Hoàn tất đăng nhập trong cửa sổ Chrome vừa mở." -ForegroundColor DarkGray
    nlm login
    $nlmLoginRc = $LASTEXITCODE
    if ($nlmLoginRc -ne 0) {
      Write-Host "[nlm] ⚠ login trả rc=$nlmLoginRc sau bước browser; kiểm LIVE probe trước khi kết luận lỗi..." -ForegroundColor Yellow
      if (Test-NlmLive) {
        Write-Host "[nlm] ✓ cookie local ĐÃ SỐNG dù CLI login trả lỗi cuối — tiếp tục stage ngay." -ForegroundColor Green
      } else {
        Write-Host "[nlm] ✗ login lỗi thật (LIVE probe vẫn chết)." -ForegroundColor Red
        $fail++; $nlmLoginOk = $false
      }
    } else { Write-Host "[nlm] ✓ login OK." -ForegroundColor Green }
  }
  if ($nlmLoginOk) {
    if ($NoStage) {
      Write-Host "[nlm] BỎ QUA stage (-NoStage)." -ForegroundColor Yellow
    } else {
      Write-Host "[nlm] đẩy nlm cookie (mã hoá) lên Drive (ghi đè tại chỗ)…" -ForegroundColor Cyan
      & $PY $TL nlm-auth-stage --refresh
      if ($LASTEXITCODE -ne 0) { Write-Host "[nlm] ✗ stage lỗi." -ForegroundColor Red; $fail++ }
    }
    if (Test-NlmLive) { Write-Host "[nlm] ✓ verify: SỐNG (probe base notebook OK)." -ForegroundColor Green }
    else { Write-Host "[nlm] ✗ verify: vẫn CHẾT — thử lại nlm login." -ForegroundColor Red; $fail++ }
  }
}

# ==================== (tùy chọn) đồng bộ master-key bundle ====================
if ($Bundle -and -not $NoStage) {
  Write-Host ""
  if (-not $env:TL_MASTER_KEY) {
    Write-Host "[bundle] ⚠ BỎ QUA: chưa đặt TL_MASTER_KEY (đường public .enc đã đủ cho Cowork/Chat)." -ForegroundColor Yellow
  } else {
    $flags = @()
    if ($doGws) { $flags += "--gws" }
    if ($doNlm) { $flags += "--nlm" }
    Write-Host "[bundle] đồng bộ master-key bundle: tl secrets-set $($flags -join ' ')…" -ForegroundColor Cyan
    & $PY $TL secrets-set @flags
    if ($LASTEXITCODE -ne 0) { Write-Host "[bundle] ✗ secrets-set lỗi." -ForegroundColor Red; $fail++ }
    else { Write-Host "[bundle] ✓ bundle + public .enc đã đồng bộ." -ForegroundColor Green }
  }
}

Write-Host ""
if ($fail -eq 0) {
  Write-Host "=== XONG. Credential đã tươi + đẩy lên Drive. Cowork/Chat: tl nlm-auth-load / tl gws-auth-load sẽ nhận bản mới. ===" -ForegroundColor Green
  Write-Host "    LƯU Ý HẠN CRED (2026-07-07 — 'expire nhanh hơn trước' là ĐÚNG THIẾT KẾ của Google, không phải lỗi script):" -ForegroundColor DarkGray
  Write-Host "    • NLM cookie: ~1h (Google session rotation) — chạy -Nlm NGAY TRƯỚC phiên Cowork cần NLM." -ForegroundColor DarkGray
  Write-Host "    • gws OAuth: app đang chế độ TESTING → refresh token TỰ CHẾT SAU 7 NGÀY (trước đây app ở" -ForegroundColor DarkGray
  Write-Host "      production nên tưởng 'bền hàng tuần'). Hết cách chỉnh từ script; 2 lối thoát:" -ForegroundColor DarkGray
  Write-Host "      (a) Google Cloud Console → OAuth consent screen của app gws → PUBLISH (In production) → refresh token bền lại;" -ForegroundColor DarkGray
  Write-Host "      (b) khỏi phụ thuộc gws cho upload: tl drive-push tự FALLBACK gcloud (--via auto, v1.33.49)." -ForegroundColor DarkGray
  Write-Host "    gcloud (dự phòng drive-push): $(Get-GcloudDriveStatus)" -ForegroundColor DarkGray
} else {
  Write-Host "=== CÓ $fail BƯỚC LỖI — xem log đỏ ở trên. ===" -ForegroundColor Red
  Write-Host "    'Lỗi ở bước cuối sau khi cấp quyền' của gws = triệu chứng OAuth app TESTING (403 access_denied/redirect):" -ForegroundColor DarkGray
  Write-Host "    • Script đã tự probe canary sau login — nếu canary SỐNG thì lỗi đó VÔ HẠI (cred đã ghi)." -ForegroundColor DarkGray
  Write-Host "    • Canary vẫn chết: kiểm account trong Test users của OAuth app, hoặc PUBLISH app (In production)." -ForegroundColor DarkGray
  Write-Host "    • Upload skill KHÔNG cần gws nữa: tl drive-push fallback gcloud — $(Get-GcloudDriveStatus)" -ForegroundColor DarkGray
}
exit $fail
