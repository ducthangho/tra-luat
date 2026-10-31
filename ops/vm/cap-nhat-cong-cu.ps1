#requires -Version 7.0
<#
cap-nhat-cong-cu.ps1 — cài/nâng cấp bộ công cụ dev cho VM Windows `tra-luat-win`, tương đương bộ mà hook
phiên cloud (`.claude/hooks/session-start.sh`) và `ops/cong_cu.yaml` dựng cho Claude/Codex.

HAI TẦNG, vì VM có HAI chủ thể quyền khác nhau (đo 31-10-2026):
  NguoiDung — chạy bằng `tlcommander` (tài khoản thường, Commander chạy dưới nó). Cần tài khoản ấy SỞ HỮU
              `C:\Tools\{npm,Python312,bin}` (không thì gói do SYSTEM cài sẵn như codex/pip không nâng được). Việc giao
              quyền ấy là bước TAY một lần của admin (README) — script KHÔNG tự làm, xem chú thích ở Register-LichCapNhat.
              Cài/nâng cấp KHÔNG cần admin: claude, codex (npm), rg,
              shellcheck, actionlint (zip có kiểm băm), PyYAML/jsonschema theo ghim của `ops/cong_cu.yaml`,
              requirements.txt vào venv của kho, notebooklm-mcp-cli (nlm) vào venv riêng.
  HeThong   — chạy bằng SYSTEM (Scheduled Task do admin đăng ký): Git, Node LTS, gh, PowerShell 7 —
              bốn thứ nằm trong `C:\Program Files`. VM KHÔNG có winget/choco/scoop, nên tải installer
              chính thức, KIỂM sha256, rồi cài im lặng.

AN NINH tầng HeThong (đừng nới): `C:\Tools` do `tlcommander` ghi được, mà `tlcommander` là tài khoản
Commander điều khiển từ xa. Vì vậy tầng SYSTEM:
  · chỉ gọi tệp chạy bằng ĐƯỜNG DẪN TUYỆT ĐỐI trong `Program Files`/`System32`, KHÔNG tra PATH;
  · tải vào một thư mục mới tạo mà ACL chỉ cho SYSTEM + Administrators;
  · chạy từ bản script đã được `-DangKyLich` chép vào `Program Files` (chỉ admin ghi được).
Một script SYSTEM đặt ở chỗ user ghi được là cửa leo quyền.

BĂM: mọi thứ tải về phải khớp sha256 trước khi chạy/chép. Nguồn băm theo thứ tự: trường `digest` của
asset GitHub → tệp checksum trong CÙNG release → (Node) SHASUMS256.txt. Không tìm được băm ⇒ TỪ CHỐI cài
công cụ đó (đo 31-10: actionlint 1.7.7 không có `digest` nhưng có `*_checksums.txt`).

Mã thoát: 0 mọi công cụ ĐẠT · 1 có công cụ LỖI · 2 thiếu bản kê, -PhamVi sai, hoặc -NhatKy/-ChiKiem đi kèm -DangKyLich · 3 tầng HeThong mà không
phải SYSTEM/admin · 4 không phải Windows · 5 sai máy (không phải -MayDich), chưa đụng gì · 6 -DangKyLich hỏng giữa chừng.
Tham số KHÔNG TỒN TẠI do chính PowerShell từ chối lúc gán tham số ⇒ rc 1, script không chạy tới để đổi được (cross-review
PR #1065 lượt 1, P2 `ma-thoat-tham-so-sai`).
#>
[CmdletBinding()]
param(
    [string]$PhamVi = 'NguoiDung',    # NguoiDung | HeThong — tự kiểm (mã 2), KHÔNG ValidateSet (ValidateSet ra rc 1)
    [switch]$ChiKiem,                 # đo + so phiên bản, KHÔNG cài gì
    [switch]$DangKyLich,              # (admin) chép script vào Program Files + đăng ký 2 Scheduled Task
    [string]$ThuMucCongCu = 'C:\Tools',
    [string]$NlmVenv = 'C:\work\nlm-venv',
    [string]$VenvKho = 'C:\work\tra-luat\.venv',
    [string]$HomeCommander = 'C:\ProgramData\TraLuatCommander\profile',
    [string]$TaiKhoanNguoiDung = 'tlcommander',
    [string]$MayDich = 'TRA-LUAT-WIN',  # chốt tên máy: đổi ACL/đăng ký tác vụ chỉ được làm đúng trên VM này
    [string]$TacVuCommander = 'TraLuatRemoteCommander',  # Desktop Commander chạy trên Node — cài lại Node là giết nó
    [string]$NhatKy = '',
    [switch]$NapHam                   # chỉ nạp hàm (cho bộ test), không chạy gì
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
# Ép UTF-8 TRƯỚC khi in: console VM không phải UTF-8 nên dòng tiếng Việt ra thành `b?n kh�ng` (đo 31-10-2026).
try { [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false) } catch { }
$OutputEncoding = [Text.UTF8Encoding]::new($false)

$Script:TenTacVuHeThong = 'TraLuat-CapNhatCongCu-HeThong'
$Script:TenTacVuNguoiDung = 'TraLuat-CapNhatCongCu-NguoiDung'
$Script:ThuMucCaiDat = $null   # tính trong Register-LichCapNhat — xem chú thích ở đó
$Script:KetQua = [System.Collections.Generic.List[object]]::new()
$Script:DaCaiNode = $false
$Script:GhHeader = @{ 'User-Agent' = 'tra-luat-cap-nhat-cong-cu'; Accept = 'application/vnd.github+json' }

# ───────────────────────── hàm thuần (bộ test gọi thẳng) ─────────────────────────

function ConvertTo-PhienBan([string]$Chuoi) {
    # Chuẩn hoá về [version]; null khi không đọc được (KHÔNG đoán).
    # Git for Windows: `2.56.0.windows.4` / tag `v2.56.0.windows.4` ⇒ 2.56.0.4.
    if ([string]::IsNullOrWhiteSpace($Chuoi)) { return $null }
    $s = $Chuoi.Trim() -replace '^[vV]', '' -replace '\.windows\.', '.'
    $m = [regex]::Match($s, '^(\d+(?:\.\d+){1,3})')
    if (-not $m.Success) { return $null }
    try { return [version]$m.Groups[1].Value } catch { return $null }
}

function Compare-PhienBan([string]$A, [string]$B) {
    # -1/0/1 như CompareTo; null khi một vế không đọc được — người gọi phải coi null là "không biết".
    $va = ConvertTo-PhienBan $A; $vb = ConvertTo-PhienBan $B
    if ($null -eq $va -or $null -eq $vb) { return $null }
    return $va.CompareTo($vb)
}

function Select-TaiSan($Release, [string]$Mau) {
    # Đúng MỘT asset khớp, không thì ném: không khớp hay khớp nhiều đều là release lạ, đừng tự chọn.
    $khop = @($Release.assets | Where-Object { $_.name -match $Mau })
    if ($khop.Count -ne 1) { throw "release $($Release.tag_name): $($khop.Count) asset khớp '$Mau' (cần đúng 1)" }
    return $khop[0]
}

function Find-BamTrongTep([string]$NoiDung, [string]$TenTep) {
    # Dòng dạng `<64 hex>  <tên>` hoặc `<64 hex> *<tên>`; trả hex thường hoặc $null.
    foreach ($dong in ([string]$NoiDung) -split "`r?`n") {
        $m = [regex]::Match($dong, '^\s*([0-9A-Fa-f]{64})\s+\*?(\S+)\s*$')
        if ($m.Success -and ($m.Groups[2].Value -eq $TenTep -or (Split-Path $m.Groups[2].Value -Leaf) -eq $TenTep)) {
            return $m.Groups[1].Value.ToLowerInvariant()
        }
    }
    return $null
}

function ConvertTo-VanBan($NoiDung) {
    # Invoke-WebRequest trả `.Content` là byte[] khi máy chủ gửi application/octet-stream (tệp checksum trên
    # GitHub Releases) — `[string]` của byte[] là dãy SỐ, không phải văn bản (đo 31-10-2026: actionlint bị từ chối).
    if ($NoiDung -is [byte[]]) { return [Text.Encoding]::UTF8.GetString($NoiDung) }
    return [string]$NoiDung
}

function Assert-Bam([string]$Tep, [string]$BamMongDoi) {
    # Fail-close: không có băm mong đợi ⇒ ném; lệch ⇒ XOÁ tệp rồi ném.
    $BamMongDoi = ([string]$BamMongDoi).ToLowerInvariant()
    if ($BamMongDoi -notmatch '^[0-9a-f]{64}$') { throw "không có sha256 hợp lệ để kiểm $(Split-Path $Tep -Leaf) — từ chối" }
    $thuc = (Get-FileHash -LiteralPath $Tep -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($thuc -ne $BamMongDoi) {
        Remove-Item -LiteralPath $Tep -Force -ErrorAction SilentlyContinue
        throw "sha256 lệch cho $(Split-Path $Tep -Leaf): $thuc ≠ $BamMongDoi — đã xoá tệp"
    }
}

function Add-DuongDanVaoChuoi([string]$Chuoi, [string]$ThuMuc) {
    # Thêm vào ĐẦU nếu chưa có (không phân biệt hoa/thường, bỏ qua `\` cuối); không nhân đôi.
    $phan = @(([string]$Chuoi) -split ';' | Where-Object { $_ -ne '' })
    $chuan = $ThuMuc.TrimEnd('\')
    if ($phan | Where-Object { $_.TrimEnd('\') -ieq $chuan }) { return ($phan -join ';') }
    return ((@($ThuMuc) + $phan) -join ';')
}

function Add-AceVaoSddl([string]$Sddl, [string]$Ace) {
    # Chèn ACE vào CUỐI phần DACL (`D:`), TRƯỚC `S:` nếu có — nối thẳng vào cuối chuỗi sẽ rơi vào SACL.
    if ($Sddl -notmatch 'D:') { throw "SDDL không có DACL: $Sddl" }
    if ($Sddl.Contains($Ace)) { return $Sddl }
    $iS = $Sddl.IndexOf('S:', $Sddl.IndexOf('D:'))
    if ($iS -lt 0) { return $Sddl + $Ace }
    return $Sddl.Substring(0, $iS) + $Ace + $Sddl.Substring($iS)
}

function Select-NodeLts($DanhSach, [string]$Truoc) {
    # Chọn bản LTS mới nhất CÙNG MAJOR với bản đang cài (index.json của nodejs.org xếp mới nhất trước).
    # Lên major mới KHÔNG tự làm: đó là thay đổi lớn cho mọi công cụ npm, và lịch 2 tuần chạy không ai canh.
    # Trả @{ cung_major = <ver|null>; moi_nhat = <ver|null> }; chưa cài gì thì cung_major = LTS mới nhất.
    $lts = @($DanhSach | Where-Object { $_.lts } | ForEach-Object { ([string]$_.version) -replace '^v', '' })
    $moiNhat = if ($lts.Count) { $lts[0] } else { $null }
    $v = ConvertTo-PhienBan $Truoc
    if ($null -eq $v) { return @{ cung_major = $moiNhat; moi_nhat = $moiNhat } }
    $cung = $lts | Where-Object { (ConvertTo-PhienBan $_).Major -eq $v.Major } | Select-Object -First 1
    return @{ cung_major = $cung; moi_nhat = $moiNhat }
}

function Test-CoTheCai([bool]$CoTep, [string]$PhienBan) {
    # Có tệp chạy mà KHÔNG đọc được phiên bản ⇒ không biết đang ở major nào ⇒ KHÔNG cài (tránh nhảy major / ghi đè mù).
    # Cross-review PR #1065 lượt 1, P1 `node-khong-doc-duoc-van-nang-major`.
    return -not ($CoTep -and [string]::IsNullOrWhiteSpace($PhienBan))
}

function ConvertTo-MatNaQuyen($Quyen) {
    # FileSystemRights → số. ToString của mask lạ (vd GENERIC_WRITE|WriteData = 0x40000002) ra SỐ, nên so TÊN bỏ lọt
    # (cross-review PR #1065 lượt 2, P2 `acl-mat-na-khong-nhan-dien`). Không quy đổi được ⇒ $null (người gọi coi là vi phạm).
    if ($null -eq $Quyen) { return $null }
    if ($Quyen -is [enum] -or $Quyen -is [int] -or $Quyen -is [long]) { return [long]$Quyen }
    $t = ([string]$Quyen).Trim()
    if ($t -match '^-?\d+$') { return [long]$t }
    try { return [long][Security.AccessControl.FileSystemRights]$t } catch { return $null }
}

function Test-AclChiAdminGhi($Owner, $Rules) {
    # Thư mục/tệp mà SYSTEM chạy: chủ phải là SYSTEM/Administrators/TrustedInstaller, và KHÔNG ai khác có quyền ghi.
    # $Rules: các đối tượng có IdentityReference, FileSystemRights, AccessControlType (như Get-Acl().Access).
    # Trả danh sách vi phạm (rỗng = đạt). So BIT, không so tên.
    $tin = '^(NT AUTHORITY\\SYSTEM|BUILTIN\\Administrators|NT SERVICE\\TrustedInstaller|S-1-5-18|S-1-5-32-544)$'
    # WriteData 0x2 · AppendData 0x4 · WriteExtendedAttributes 0x10 · DeleteSubdirectoriesAndFiles 0x40 · WriteAttributes 0x100
    # · Delete 0x10000 · ChangePermissions 0x40000 · TakeOwnership 0x80000 · GENERIC_ALL 0x10000000 · GENERIC_WRITE 0x40000000
    $bitGhi = 0x2 -bor 0x4 -bor 0x10 -bor 0x40 -bor 0x100 -bor 0x10000 -bor 0x40000 -bor 0x80000 -bor 0x10000000 -bor 0x40000000
    $vp = @()
    if ("$Owner" -notmatch $tin) { $vp += "chủ sở hữu '$Owner'" }
    foreach ($r in @($Rules)) {
        if ("$($r.AccessControlType)" -ne 'Allow') { continue }
        if ("$($r.IdentityReference)" -match $tin) { continue }
        $m = ConvertTo-MatNaQuyen $r.FileSystemRights
        if ($null -eq $m) { $vp += "$($r.IdentityReference): quyền không nhận diện '$($r.FileSystemRights)'"; continue }
        if ($m -band $bitGhi) { $vp += "$($r.IdentityReference): $($r.FileSystemRights)" }
    }
    return $vp
}

function New-DoiSoTacVu([string]$Script, [string]$Pham) {
    # Đối số của Scheduled Task mang ĐỦ cấu hình đang dùng lúc đăng ký — bản cũ chỉ ghi -PhamVi nên -MayDich/-ThuMucCongCu
    # tuỳ biến bị mất ở lần chạy theo lịch (cross-review PR #1065 lượt 1, P1 `dang-ky-lam-mat-tham-so`).
    $cap = [ordered]@{ PhamVi = $Pham; MayDich = $MayDich; ThuMucCongCu = $ThuMucCongCu; NlmVenv = $NlmVenv; VenvKho = $VenvKho
                       HomeCommander = $HomeCommander; TaiKhoanNguoiDung = $TaiKhoanNguoiDung; TacVuCommander = $TacVuCommander }
    $ds = @('-NoProfile', '-NonInteractive', '-File', "`"$Script`"")
    foreach ($k in $cap.Keys) {
        $v = [string]$cap[$k]
        if ($v -match '"' -or [string]::IsNullOrWhiteSpace($v)) { throw "giá trị -$k không dùng được trong tác vụ: '$v'" }
        # Luật CommandLineToArgvW: dãy `\` ngay trước nháy đóng phải NHÂN ĐÔI, không thì `\"` thành nháy THẬT và mọi
        # tham số sau bị gộp vào giá trị này (cross-review PR #1065 lượt 2, P1 `doi-so-duong-dan-ket-thuc-backslash`).
        $v = [regex]::Replace($v, '(\\+)$', { param($m) $m.Value * 2 })
        $ds += "-$k"; $ds += "`"$v`""
    }
    return ($ds -join ' ')
}

function Find-Reparse([string]$Goc) {
    # Mọi reparse point (junction/symlink) trong cây, KHÔNG đi theo chúng; kể cả chính gốc. Rỗng = sạch.
    $ra = @()
    # Tổ tiên trước: một thư mục cha là liên kết thì cả cây con thật ra nằm chỗ khác (cross-review lượt 2, P0).
    $cha = Split-Path -Parent ([IO.Path]::GetFullPath($Goc))
    while ($cha) {
        $gc = Get-Item -LiteralPath $cha -Force -ErrorAction SilentlyContinue
        if ($gc -and ($gc.Attributes -band [IO.FileAttributes]::ReparsePoint)) { return @($gc.FullName) }
        $tiep = Split-Path -Parent $cha; if ($tiep -eq $cha) { break }; $cha = $tiep
    }
    $g = Get-Item -LiteralPath $Goc -Force -ErrorAction SilentlyContinue
    if (-not $g) { return $ra }
    if ($g.Attributes -band [IO.FileAttributes]::ReparsePoint) { return @($g.FullName) }
    $ra += @(Get-ChildItem -LiteralPath $Goc -Recurse -Force -Attributes ReparsePoint -ErrorAction Stop | ForEach-Object { $_.FullName })
    return $ra
}

function Assert-KhongReparse([string]$Goc) {
    $rp = @(Find-Reparse $Goc)
    if ($rp.Count) { throw "từ chối: $Goc có reparse point (junction/symlink): $($rp -join ', ')" }
}

function Invoke-Icacls([string[]]$DoiSo) {
    # MỘT cửa cho mọi lời gọi icacls của bước đăng ký: đường dẫn TUYỆT ĐỐI trong System32, rc≠0 ⇒ ném. Gom về đây để bộ
    # test giả được icacls trên cả Windows lẫn Linux và chạy Register-LichCapNhat THẬT (cross-review PR #1065 lượt 3, P2).
    $o = & "$env:SystemRoot\System32\icacls.exe" @DoiSo 2>&1
    if ($LASTEXITCODE -ne 0) { throw "icacls $($DoiSo -join ' ') rc=$LASTEXITCODE`: $($o | Select-Object -Last 1)" }
}

function Read-BanGhim([string]$TepYaml, [string]$Python) {
    # Đọc ghim từ `ops/cong_cu.yaml` bằng PyYAML — MỘT nguồn với CI. PyYAML/jsonschema ghim trong
    # `cai.lenh` (`==X.Y.Z`); actionlint ghim ở `ban_ghim`.
    $ma = @'
import json, re, sys, yaml
d = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))["cong_cu"]
def tu_lenh(t):
    m = re.search(r"==([0-9][0-9A-Za-z.+-]*)", ((d.get(t) or {}).get("cai") or {}).get("lenh", ""))
    return m.group(1) if m else None
print(json.dumps({"PyYAML": tu_lenh("PyYAML"), "jsonschema": tu_lenh("jsonschema"),
                  "actionlint": (d.get("actionlint") or {}).get("ban_ghim")}))
'@
    $out = & $Python -c $ma $TepYaml 2>&1
    if ($LASTEXITCODE -ne 0) { throw "đọc $TepYaml hỏng (rc=$LASTEXITCODE): $($out | Select-Object -Last 1)" }
    $g = ($out | Select-Object -Last 1) | ConvertFrom-Json
    foreach ($k in 'PyYAML', 'jsonschema', 'actionlint') {
        if (-not $g.$k) { throw "bản kê thiếu ghim cho $k" }
    }
    return $g
}

# ───────────────────────── hàm có hiệu ứng ─────────────────────────

function Write-Loi([string]$Thong) {
    # KHÔNG dùng Write-Error trước `exit N`: với $ErrorActionPreference='Stop' nó thành lỗi kết thúc và script
    # thoát rc=1, nuốt mã thoát đã khai (bộ test bắt được ở lượt đo đầu trên VM, 31-10-2026).
    [Console]::Error.WriteLine("cap-nhat-cong-cu: $Thong")
}

function Add-KetQua([string]$CongCu, [string]$Truoc, [string]$Sau, [string]$HanhDong, [string]$ChiTiet = '') {
    $Script:KetQua.Add([pscustomobject]@{ cong_cu = $CongCu; truoc = $Truoc; sau = $Sau; hanh_dong = $HanhDong; chi_tiet = $ChiTiet })
    Write-Host ("{0,-22} {1,-14} -> {2,-14} {3} {4}" -f $CongCu, $Truoc, $Sau, $HanhDong, $ChiTiet)
}

function Get-PhienBanLenh([string]$Exe, [string[]]$DoiSo, [string]$Mau) {
    if (-not $Exe -or -not (Test-Path -LiteralPath $Exe)) { return $null }
    # rc lấy NGAY sau lệnh; rc≠0 ⇒ không biết phiên bản. CLI hỏng vẫn có thể in một chuỗi giống phiên bản (vd
    # `Node.js v24.2.0` trong stderr của lỗi node) — trước đây nó được nhận là phiên bản của chính công cụ và ghi `giu`
    # (cross-review PR #1065 lượt 5, P1 `loi-native-tang-nguoi-dung`).
    try { $o = (& $Exe @DoiSo 2>&1 | Out-String); $rc = $LASTEXITCODE } catch { return $null }
    if ($rc -ne 0) { return $null }
    $m = [regex]::Match($o, $Mau)
    if ($m.Success) { return $m.Groups[1].Value } else { return $null }
}

function Get-Release([string]$Repo, [string]$Tag = '') {
    $u = if ($Tag) { "https://api.github.com/repos/$Repo/releases/tags/$Tag" } else { "https://api.github.com/repos/$Repo/releases/latest" }
    return Invoke-RestMethod -Headers $Script:GhHeader -Uri $u -TimeoutSec 60
}

function Get-BamTaiSan($Release, $TaiSan) {
    if ($TaiSan.digest -match '^sha256:([0-9a-fA-F]{64})$') { return $Matches[1].ToLowerInvariant() }
    $tepBam = @($Release.assets | Where-Object { $_.name -match '(checksums?\.txt|sha256(sums)?(\.txt)?|hashes\.sha256)$' -or $_.name -eq "$($TaiSan.name).sha256" })
    foreach ($t in $tepBam) {
        $nd = ConvertTo-VanBan (Invoke-WebRequest -Uri $t.browser_download_url -Headers @{ 'User-Agent' = 'tra-luat' } -TimeoutSec 60).Content
        $b = Find-BamTrongTep $nd $TaiSan.name
        # Tệp riêng `<asset>.sha256` chỉ được nhận dạng TRẦN khi CẢ tệp là đúng một băm; có tên tệp thì tên phải khớp
        # (Find-BamTrongTep). Bản cũ nhận 64 hex đầu dòng bất kể tên ghi kèm (cross-review PR #1065 lượt 1, P1).
        if (-not $b -and $t.name -eq "$($TaiSan.name).sha256" -and ([string]$nd).Trim() -match '^[0-9A-Fa-f]{64}$') {
            $b = ([string]$nd).Trim().ToLowerInvariant()
        }
        if ($b) { return $b }
    }
    return $null
}

function Save-CoKiemBam([string]$Url, [string]$Bam, [string]$ThuMuc, [string]$Ten) {
    $dich = Join-Path $ThuMuc $Ten
    Invoke-WebRequest -Uri $Url -OutFile $dich -Headers @{ 'User-Agent' = 'tra-luat' } -TimeoutSec 600
    Assert-Bam $dich $Bam
    return $dich
}

function New-ThuMucTai([switch]$ChiAdmin) {
    $d = Join-Path ([IO.Path]::GetTempPath()) ("tl-cap-nhat-" + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $d | Out-Null
    if ($ChiAdmin) {
        # SYSTEM + Administrators, bỏ thừa kế: user không thả/đổi được installer giữa lúc kiểm băm và lúc chạy.
        $o = & "$env:SystemRoot\System32\icacls.exe" $d /inheritance:r /grant:r '*S-1-5-18:(OI)(CI)F' '*S-1-5-32-544:(OI)(CI)F' 2>&1
        if ($LASTEXITCODE -ne 0) { throw "icacls thư mục tải hỏng: $o" }
    }
    return $d
}

function Set-PathNguoiDung([string[]]$ThuMuc) {
    $u = [Environment]::GetEnvironmentVariable('Path', 'User')
    $moi = $u
    foreach ($t in $ThuMuc) { $moi = Add-DuongDanVaoChuoi $moi $t; $env:Path = Add-DuongDanVaoChuoi $env:Path $t }
    if ($moi -ne $u) { [Environment]::SetEnvironmentVariable('Path', $moi, 'User') }
}

function Update-CongCuZip([string]$Ten, [string]$Repo, [string]$Tag, [string]$MauTaiSan, [string]$TenExe,
                          [string[]]$DoiSoPhienBan, [string]$MauPhienBan, [string]$ThuMucBin) {
    $exe = Join-Path $ThuMucBin $TenExe
    $truoc = Get-PhienBanLenh $exe $DoiSoPhienBan $MauPhienBan
    try {
        $rel = Get-Release $Repo $Tag
        $moi = ($rel.tag_name -replace '^v', '')
        $ss = Compare-PhienBan $truoc $moi
        if ($null -ne $ss -and $ss -ge 0 -and -not ($Tag -and $ss -gt 0)) { Add-KetQua $Ten $truoc $truoc 'giu'; return }
        if ($ChiKiem) { Add-KetQua $Ten "$truoc" $moi 'can_cap_nhat'; return }
        $ts = Select-TaiSan $rel $MauTaiSan
        $bam = Get-BamTaiSan $rel $ts
        $tai = New-ThuMucTai
        try {
            $zip = Save-CoKiemBam $ts.browser_download_url $bam $tai $ts.name
            $giai = Join-Path $tai 'giai'
            Expand-Archive -LiteralPath $zip -DestinationPath $giai
            $tim = @(Get-ChildItem -LiteralPath $giai -Recurse -Force -File -Filter $TenExe)
            if ($tim.Count -ne 1) { throw "zip có $($tim.Count) tệp $TenExe (cần 1)" }
            New-Item -ItemType Directory -Force -Path $ThuMucBin | Out-Null
            Copy-Item -LiteralPath $tim[0].FullName -Destination $exe -Force
        } finally { Remove-Item -LiteralPath $tai -Recurse -Force -ErrorAction SilentlyContinue }
        $sau = Get-PhienBanLenh $exe $DoiSoPhienBan $MauPhienBan
        if ((Compare-PhienBan $sau $moi) -ne 0) { throw "sau khi cài đo được '$sau', mong '$moi'" }
        Add-KetQua $Ten "$truoc" $sau $(if ($truoc) { 'nang_cap' } else { 'cai_moi' })
    } catch { Add-KetQua $Ten "$truoc" '' 'loi' $_.Exception.Message }
}

function Invoke-TangNguoiDung([string]$GocKho) {
    $py = Join-Path $ThuMucCongCu 'Python312\python.exe'
    $bin = Join-Path $ThuMucCongCu 'bin'
    $npmPrefix = Join-Path $ThuMucCongCu 'npm'
    $npm = Join-Path ${env:ProgramFiles} 'nodejs\npm.cmd'
    $banKe = @((Join-Path $GocKho 'cong_cu.yaml'), (Join-Path $GocKho 'ops\cong_cu.yaml')) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    $yeuCau = @((Join-Path $GocKho 'requirements.txt')) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $banKe) { Write-Loi "không thấy cong_cu.yaml dưới $GocKho"; exit 2 }
    if (-not (Test-Path -LiteralPath $py)) { Add-KetQua 'python' '' '' 'loi' "không có $py"; return }
    if (-not $ChiKiem) { Set-PathNguoiDung @($bin, $npmPrefix) }

    # 1. pip + PyYAML/jsonschema theo ghim của bản kê (Python dùng chung của máy, như `python` trên PATH).
    $pyTruoc = Get-PhienBanLenh $py @('--version') 'Python\s+(\S+)'
    if (-not $pyTruoc) { Add-KetQua 'python' '' '' 'loi' "$py --version không chạy được"; return }
    Add-KetQua 'python' $pyTruoc $pyTruoc 'giu' 'bản Python không tự nâng (đổi minor phá venv) — chỉ báo'
    try {
        if (-not $ChiKiem) { & $py -m pip install --quiet --disable-pip-version-check PyYAML 2>&1 | Out-Null }
        $ghim = Read-BanGhim $banKe $py
    } catch { Add-KetQua 'cong_cu.yaml' '' '' 'loi' $_.Exception.Message; return }
    # Mỗi công cụ một ranh giới try/catch: lỗi KHỞI CHẠY lệnh native (tệp biến mất giữa Test-Path và lúc gọi, quyền…) ném
    # CommandNotFoundException chứ không đặt $LASTEXITCODE — trước đây nó giết cả tầng, mất các công cụ sau và mất nhật
    # ký (cross-review PR #1065 lượt 4, P1 `loi-native-tang-nguoi-dung`).
    foreach ($goi in 'pip', 'PyYAML', 'jsonschema') {
      try {
        $truoc = (& $py -c "import importlib.metadata as m; print(m.version('$goi'))" 2>$null)
        $spec = if ($goi -eq 'pip') { 'pip' } else { "$goi==$($ghim.$goi)" }
        if ($ChiKiem) { Add-KetQua $goi "$truoc" $(if ($goi -eq 'pip') { 'moi nhat' } else { $ghim.$goi }) 'kiem'; continue }
        $o = & $py -m pip install --quiet --disable-pip-version-check --upgrade $spec 2>&1
        $rc = $LASTEXITCODE
        $sau = (& $py -c "import importlib.metadata as m; print(m.version('$goi'))" 2>$null)
        if ($rc -ne 0 -or -not $sau -or ($goi -ne 'pip' -and $sau -ne $ghim.$goi)) { Add-KetQua $goi "$truoc" "$sau" 'loi' "pip rc=$rc $($o | Select-Object -Last 1)" }
        else { Add-KetQua $goi "$truoc" "$sau" $(if ($truoc -eq $sau) { 'giu' } else { 'nang_cap' }) }
      } catch { Add-KetQua $goi '' '' 'loi' $_.Exception.Message }
    }

    # 2. venv của kho: requirements.txt (giữ ghim của kho, không --upgrade bừa).
    $vpy = Join-Path $VenvKho 'Scripts\python.exe'
    if ((Test-Path -LiteralPath $vpy) -and $yeuCau) {
        if ($ChiKiem) { Add-KetQua 'venv-kho' '' '' 'kiem' $VenvKho }
        else {
            try {
                $o = & $vpy -m pip install --quiet --disable-pip-version-check -r $yeuCau "PyYAML==$($ghim.PyYAML)" "jsonschema==$($ghim.jsonschema)" 2>&1
                if ($LASTEXITCODE -ne 0) { Add-KetQua 'venv-kho' '' '' 'loi' "$($o | Select-Object -Last 1)" } else { Add-KetQua 'venv-kho' '' '' 'giu' 'requirements.txt đã khớp' }
            } catch { Add-KetQua 'venv-kho' '' '' 'loi' $_.Exception.Message }
        }
    } else { Add-KetQua 'venv-kho' '' '' 'bo_qua' "không có $vpy hoặc requirements.txt" }

    # 3. claude + codex qua npm global vào C:\Tools\npm (cùng chỗ codex đang nằm).
    foreach ($p in @(@('claude', '@anthropic-ai/claude-code', 'claude.cmd'), @('codex', '@openai/codex', 'codex.cmd'))) {
        $exe = Join-Path $npmPrefix $p[2]
        $truoc = Get-PhienBanLenh $exe @('--version') '(\d+\.\d+\.\d+)'
        if (-not (Test-Path -LiteralPath $npm)) { Add-KetQua $p[0] "$truoc" '' 'loi' "không có $npm"; continue }
        if ($ChiKiem) { Add-KetQua $p[0] "$truoc" '' 'kiem'; continue }
        try { $o = & $npm install -g --prefix $npmPrefix "$($p[1])@latest" --no-fund --no-audit 2>&1; $rc = $LASTEXITCODE }
        catch { Add-KetQua $p[0] "$truoc" '' 'loi' "không chạy được npm: $($_.Exception.Message)"; continue }
        $sau = Get-PhienBanLenh $exe @('--version') '(\d+\.\d+\.\d+)'
        if ($rc -ne 0 -or -not $sau) { Add-KetQua $p[0] "$truoc" "$sau" 'loi' "npm rc=$rc $($o | Select-Object -Last 1)" }
        else { Add-KetQua $p[0] "$truoc" $sau $(if ($truoc -eq $sau) { 'giu' } elseif ($truoc) { 'nang_cap' } else { 'cai_moi' }) }
    }

    # 4. Nhị phân portable vào C:\Tools\bin, có kiểm băm. actionlint theo ghim; rg/shellcheck bản mới nhất.
    Update-CongCuZip 'rg' 'BurntSushi/ripgrep' '' 'x86_64-pc-windows-msvc\.zip$' 'rg.exe' @('--version') '(?m)^ripgrep\s+(\d+\.\d+\.\d+)' $bin
    Update-CongCuZip 'shellcheck' 'koalaman/shellcheck' '' '^shellcheck-v[\d.]+\.zip$' 'shellcheck.exe' @('--version') 'version:\s*(\d+\.\d+\.\d+)' $bin
    Update-CongCuZip 'actionlint' 'rhysd/actionlint' "v$($ghim.actionlint)" "^actionlint_$([regex]::Escape($ghim.actionlint))_windows_amd64\.zip$" 'actionlint.exe' @('-version') '(?m)^(\d+\.\d+\.\d+)' $bin

    # 5. nlm (notebooklm-mcp-cli) trong venv riêng; sau nâng cấp, chế độ lưu credential phải còn là `file`
    #    — `tl nlm-auth-stage` chỉ đọc `cookies.json` (scripts/tl_gws.py `_NLM_AUTH_RELS`).
    $nlmPy = Join-Path $NlmVenv 'Scripts\python.exe'
    $nlm = Join-Path $NlmVenv 'Scripts\nlm.exe'
    if (-not (Test-Path -LiteralPath $nlmPy)) { Add-KetQua 'nlm' '' '' 'bo_qua' "không có venv $NlmVenv" }
    else {
        $truoc = Get-PhienBanLenh $nlm @('--version') 'nlm version\s+(\S+)'
        if ($ChiKiem) { Add-KetQua 'nlm' "$truoc" '' 'kiem' }
        else {
          try {
            $o = & $nlmPy -m pip install --quiet --disable-pip-version-check --upgrade notebooklm-mcp-cli 2>&1
            $rcPip = $LASTEXITCODE
            $sau = Get-PhienBanLenh $nlm @('--version') 'nlm version\s+(\S+)'
            # rc của lệnh status đo RIÊNG, ngay sau lệnh: trước đây phép so dùng rc của pip nên status rc≠0 mà vẫn in JSON
            # mode=file thì được ghi ĐẠT (lượt 4, P1). Đòi rc=0 VÀ JSON đọc được VÀ mode=file.
            $cheDo = $null; $rcSt = $null; $loiSt = ''
            $hTruoc = $env:USERPROFILE, $env:HOME
            try {
                $env:USERPROFILE = $HomeCommander; $env:HOME = $HomeCommander
                $raSt = & $nlm auth storage status --json 2>$null | Out-String
                $rcSt = $LASTEXITCODE
                $cheDo = ($raSt | ConvertFrom-Json).mode
            } catch { $loiSt = $_.Exception.Message } finally { $env:USERPROFILE, $env:HOME = $hTruoc }
            if ($rcPip -ne 0 -or -not $sau) { Add-KetQua 'nlm' "$truoc" "$sau" 'loi' "pip rc=$rcPip $($o | Select-Object -Last 1)" }
            elseif ($rcSt -ne 0) { Add-KetQua 'nlm' "$truoc" $sau 'loi' "nlm auth storage status rc=$rcSt $loiSt" }
            elseif ($cheDo -ne 'file') { Add-KetQua 'nlm' "$truoc" $sau 'loi' "chế độ lưu credential = '$cheDo' (cần 'file' cho nlm-auth-stage)" }
            else { Add-KetQua 'nlm' "$truoc" $sau $(if ($truoc -eq $sau) { 'giu' } else { 'nang_cap' }) 'storage=file' }
          } catch { Add-KetQua 'nlm' "$truoc" '' 'loi' $_.Exception.Message }
        }
    }
}

function Install-Msi([string]$Msi, [string]$Ten) {
    $log = "$Msi.log"
    $p = Start-Process -FilePath "$env:SystemRoot\System32\msiexec.exe" -ArgumentList @('/i', "`"$Msi`"", '/qn', '/norestart', '/l*v', "`"$log`"") -Wait -PassThru
    if ($p.ExitCode -eq 3010) { return 'can_khoi_dong_lai' }
    if ($p.ExitCode -ne 0) { throw "msiexec $Ten rc=$($p.ExitCode) (log: $log)" }
    return 'ok'
}

function Invoke-TangHeThong {
    # CHỈ đường dẫn tuyệt đối — xem đầu tệp.
    $pf = ${env:ProgramFiles}
    $muc = @(
        @{ ten = 'git'; exe = "$pf\Git\cmd\git.exe"; ds = @('--version'); mau = 'git version\s+(\S+)'; repo = 'git-for-windows/git'; ts = '^Git-[\d.]+-64-bit\.exe$'; kieu = 'exe' },
        @{ ten = 'gh'; exe = "$pf\GitHub CLI\gh.exe"; ds = @('--version'); mau = 'gh version\s+(\d+\.\d+\.\d+)'; repo = 'cli/cli'; ts = '^gh_[\d.]+_windows_amd64\.msi$'; kieu = 'msi' },
        @{ ten = 'node'; exe = "$pf\nodejs\node.exe"; ds = @('--version'); mau = 'v(\d+\.\d+\.\d+)'; repo = ''; ts = ''; kieu = 'node' },
        # pwsh CUỐI: đang chạy chính nó, MSI có thể đòi khởi động lại (3010) — vẫn là kết quả hợp lệ.
        @{ ten = 'pwsh'; exe = "$pf\PowerShell\7\pwsh.exe"; ds = @('-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()'); mau = '(\d+\.\d+\.\d+)'; repo = 'PowerShell/PowerShell'; ts = '^PowerShell-[\d.]+-win-x64\.msi$'; kieu = 'msi' }
    )
    foreach ($c in $muc) {
        $truoc = Get-PhienBanLenh $c.exe $c.ds $c.mau
        if (-not (Test-CoTheCai (Test-Path -LiteralPath $c.exe) $truoc)) {
            Add-KetQua $c.ten '' '' 'loi' "có $($c.exe) nhưng không đọc được phiên bản — KHÔNG tự cài (tránh đổi major/ghi đè mù)"
            continue
        }
        try {
            if ($c.kieu -eq 'node') {
                $ds = Invoke-RestMethod -Uri 'https://nodejs.org/dist/index.json' -TimeoutSec 60
                $chon = Select-NodeLts $ds $truoc
                if ($chon.moi_nhat -and (Compare-PhienBan $chon.moi_nhat $truoc) -gt 0 -and
                    (ConvertTo-PhienBan $chon.moi_nhat).Major -ne (ConvertTo-PhienBan $truoc).Major) {
                    Add-KetQua 'node-major' "$truoc" $chon.moi_nhat 'can_quyet_dinh' 'có LTS major mới — KHÔNG tự nâng; chủ kho quyết định'
                }
                if (-not $chon.cung_major) { Add-KetQua $c.ten "$truoc" '' 'can_quyet_dinh' 'major đang cài không còn bản LTS nào'; continue }
                $moi = $chon.cung_major
                $tenTep = "node-v$moi-x64.msi"
                $url = "https://nodejs.org/dist/v$moi/$tenTep"
                $sums = ConvertTo-VanBan (Invoke-WebRequest -Uri "https://nodejs.org/dist/v$moi/SHASUMS256.txt" -TimeoutSec 60).Content
                $bam = Find-BamTrongTep $sums $tenTep
            } else {
                $rel = Get-Release $c.repo
                $moi = $rel.tag_name -replace '^v', ''
                $ts = Select-TaiSan $rel $c.ts
                $tenTep = $ts.name; $url = $ts.browser_download_url
                $bam = $null
            }
            $ss = Compare-PhienBan $truoc $moi
            if ($null -ne $ss -and $ss -ge 0) { Add-KetQua $c.ten $truoc $truoc 'giu'; continue }
            if ($ChiKiem) { Add-KetQua $c.ten "$truoc" $moi 'can_cap_nhat'; continue }
            if ($c.kieu -ne 'node') { $bam = Get-BamTaiSan $rel $ts }
            $tai = New-ThuMucTai -ChiAdmin
            try {
                $tep = Save-CoKiemBam $url $bam $tai $tenTep
                # Đánh dấu TRƯỚC khi cài: MSI Node tắt node.exe đang chạy kể cả khi cài hỏng giữa chừng.
                if ($c.kieu -eq 'node') { $Script:DaCaiNode = $true }
                $trangThai = 'ok'
                if ($c.kieu -eq 'exe') {
                    $p = Start-Process -FilePath $tep -ArgumentList @('/VERYSILENT', '/NORESTART', '/NOCANCEL', '/SP-', '/SUPPRESSMSGBOXES') -Wait -PassThru
                    if ($p.ExitCode -ne 0) { throw "installer $($c.ten) rc=$($p.ExitCode)" }
                } else { $trangThai = Install-Msi $tep $c.ten }
            } finally { Remove-Item -LiteralPath $tai -Recurse -Force -ErrorAction SilentlyContinue }
            $sau = Get-PhienBanLenh $c.exe $c.ds $c.mau
            if ($trangThai -eq 'can_khoi_dong_lai') { Add-KetQua $c.ten "$truoc" "$sau" 'can_khoi_dong_lai' "đã cài $moi, có hiệu lực sau khởi động lại"; continue }
            if ((Compare-PhienBan $sau $moi) -ne 0) { throw "sau khi cài đo được '$sau', mong '$moi'" }
            Add-KetQua $c.ten "$truoc" $sau $(if ($truoc) { 'nang_cap' } else { 'cai_moi' })
        } catch { Add-KetQua $c.ten "$truoc" '' 'loi' $_.Exception.Message }
    }
    # Đo 31-10-2026: lượt HeThong đầu tiên cài Node bằng MSI ⇒ Desktop Commander (chạy trên node.exe) rớt Offline
    # giữa chừng, và phiên điều khiển mất đường vào VM. Lượt này chạy bằng pwsh dưới SYSTEM nên còn sống để dựng lại.
    if ($Script:DaCaiNode) {
        try {
            Stop-ScheduledTask -TaskName $TacVuCommander -ErrorAction SilentlyContinue
            Start-ScheduledTask -TaskName $TacVuCommander -ErrorAction Stop
            Start-Sleep -Seconds 10
            $st = (Get-ScheduledTask -TaskName $TacVuCommander -ErrorAction Stop).State
            if ("$st" -ne 'Running') { throw "trạng thái sau khởi động lại: $st" }
            Add-KetQua 'commander' '' 'Running' 'khoi_dong_lai' "đã cài lại Node ⇒ khởi động lại $TacVuCommander"
        } catch { Add-KetQua 'commander' '' '' 'loi' "không dựng lại được $TacVuCommander`: $($_.Exception.Message)" }
    }
}

function Register-LichCapNhat([string]$GocKho) {
    # Chép script + bản kê + requirements vào Program Files (chỉ admin ghi) rồi đăng ký 2 tác vụ.
    # Tính đường dẫn Ở ĐÂY, không ở mức script: ngoài Windows `ProgramFiles` không có, và `Join-Path $null` ném lỗi
    # TRƯỚC chốt nền ⇒ mất mã 4 và `-NapHam` không nạp được (Codex review P2 trên PR #1065, head 6733d09).
    $Script:ThuMucCaiDat = Join-Path ${env:ProgramFiles} 'tra-luat-ops'
    # KHÔNG tự giao quyền C:\Tools cho tài khoản NguoiDung nữa — chỉ ĐỌC và báo. Hai lượt cross-review liên tiếp (PR #1065,
    # P0 `giao-acl-theo-junction`) cho thấy mọi ACL đệ quy THEO TÊN trên cây mà tài khoản ấy kiểm soát đều có khe tráo
    # (junction ở con, rồi ở tổ tiên, rồi tráo giữa hai lệnh) và đích bị trao quyền có thể là BẤT KỲ thư mục hệ thống nào.
    # Cùng một hình dạng lỗi lặp lại ⇒ bỏ việc làm, không vá tiếp (CLAUDE.md "BẢY phát hiện cùng MỘT đường"). Trên VM việc
    # giao quyền đã làm xong 31-10-2026. Kho cũng KHÔNG đưa công thức tay (lượt 3: công thức tay mang đúng khe ấy) — README.
    $ai = "$env:COMPUTERNAME\$TaiKhoanNguoiDung"
    foreach ($con in 'npm', 'Python312', 'bin') {
        $d = Join-Path $ThuMucCongCu $con
        $chu = if (Test-Path -LiteralPath $d) { "$((Get-Acl -LiteralPath $d).Owner)" } else { '(chưa có)' }
        if ($chu -ne $ai) { Write-Host "LƯU Ý: $d thuộc '$chu', không phải '$ai' — tầng NguoiDung không nâng được gói có sẵn ở đó; kho không tự giao quyền (README mục 'Giao C:\Tools')" }
    }
    # Thư mục cài đặt: tạo, từ chối nếu là liên kết, ĐẶT LẠI ACL (bỏ thừa kế; SYSTEM/Administrators toàn quyền, Users đọc).
    New-Item -ItemType Directory -Force -Path $Script:ThuMucCaiDat | Out-Null
    Assert-KhongReparse $Script:ThuMucCaiDat
    Invoke-Icacls @($Script:ThuMucCaiDat, '/setowner', '*S-1-5-32-544', '/T', '/C', '/L', '/Q')
    Invoke-Icacls @($Script:ThuMucCaiDat, '/inheritance:r', '/grant:r', '*S-1-5-18:(OI)(CI)F', '*S-1-5-32-544:(OI)(CI)F', '*S-1-5-32-545:(OI)(CI)RX', '/T', '/C', '/L', '/Q')
    $nguon = @{
        'cap-nhat-cong-cu.ps1' = $PSCommandPath
        'cong_cu.yaml'         = @((Join-Path $GocKho 'ops\cong_cu.yaml'), (Join-Path $GocKho 'cong_cu.yaml')) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
        'requirements.txt'     = Join-Path $GocKho 'requirements.txt'
    }
    foreach ($k in $nguon.Keys) {
        if (-not $nguon[$k] -or -not (Test-Path -LiteralPath $nguon[$k])) { throw "thiếu $k để chép" }
        if ((Resolve-Path -LiteralPath $nguon[$k]).Path -ne (Join-Path $Script:ThuMucCaiDat $k)) {
            Copy-Item -LiteralPath $nguon[$k] -Destination (Join-Path $Script:ThuMucCaiDat $k) -Force
        }
    }
    # Tệp vừa chép có thể mang chủ là chính tài khoản admin đang chạy (tuỳ chính sách "default owner") ⇒ đặt lại về nhóm.
    Invoke-Icacls @($Script:ThuMucCaiDat, '/setowner', '*S-1-5-32-544', '/T', '/C', '/L', '/Q')
    # Đo lại SAU khi chép: thư mục + từng tệp chỉ admin ghi được, và bản chép trùng băm nguồn.
    foreach ($k in @('') + @($nguon.Keys)) {
        $dich = if ($k) { Join-Path $Script:ThuMucCaiDat $k } else { $Script:ThuMucCaiDat }
        $acl = Get-Acl -LiteralPath $dich
        $vp = @(Test-AclChiAdminGhi $acl.Owner $acl.Access)
        if ($vp.Count) { throw "ACL $dich không đạt: $($vp -join '; ')" }
        if ($k -and (Get-FileHash -LiteralPath $dich).Hash -ne (Get-FileHash -LiteralPath $nguon[$k]).Hash) { throw "bản chép $dich lệch băm nguồn" }
    }
    $script = Join-Path $Script:ThuMucCaiDat 'cap-nhat-cong-cu.ps1'
    $pwsh = Join-Path ${env:ProgramFiles} 'PowerShell\7\pwsh.exe'
    $caiDat = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2) -MultipleInstances IgnoreNew
    $tHT = New-ScheduledTaskTrigger -Weekly -WeeksInterval 2 -DaysOfWeek Sunday -At '02:30'
    $tND = New-ScheduledTaskTrigger -Weekly -WeeksInterval 2 -DaysOfWeek Sunday -At '03:30'
    $aHT = New-ScheduledTaskAction -Execute $pwsh -Argument (New-DoiSoTacVu $script 'HeThong')
    $aND = New-ScheduledTaskAction -Execute $pwsh -Argument (New-DoiSoTacVu $script 'NguoiDung')
    $pHT = New-ScheduledTaskPrincipal -UserId 'NT AUTHORITY\SYSTEM' -LogonType ServiceAccount -RunLevel Highest
    # -ErrorAction Stop TƯỜNG MINH: Register-ScheduledTask là hàm module CDXML, KHÔNG thừa hưởng $ErrorActionPreference
    # của script — đo 31-10-2026, lỗi của nó trôi qua, script chết ở bước sau và in rc=0 (mã của icacls trước đó).
    Register-ScheduledTask -TaskName $Script:TenTacVuHeThong -Action $aHT -Trigger $tHT -Principal $pHT -Settings $caiDat -Force -ErrorAction Stop | Out-Null
    # Tầng NguoiDung lưu mật khẩu (như TraLuatRemoteCommander có sẵn). S4U cho tài khoản KHÁC bị từ chối trên VM
    # (`Access is denied`, đo 31-10-2026). Mật khẩu chỉ đi từ hộp nhập vào Task Scheduler, không vào lệnh/log.
    $ten = "$env:COMPUTERNAME\$TaiKhoanNguoiDung"
    $cred = Get-Credential -UserName $ten -Message "Mật khẩu của $ten (để tác vụ $($Script:TenTacVuNguoiDung) chạy khi không ai đăng nhập)"
    if (-not $cred) { throw 'không nhập mật khẩu — chưa đăng ký tác vụ NguoiDung' }
    Register-ScheduledTask -TaskName $Script:TenTacVuNguoiDung -Action $aND -Trigger $tND -Settings $caiDat -Force -ErrorAction Stop `
        -User $ten -Password $cred.GetNetworkCredential().Password -RunLevel Limited | Out-Null
    Remove-Variable cred
    # Cho tlcommander quyền ĐỌC + CHẠY hai tác vụ (không sửa được): Commander bấm "chạy ngay" khi được yêu cầu,
    # còn nội dung chạy vẫn là script trong Program Files mà tlcommander không ghi được.
    $sid = (New-Object Security.Principal.NTAccount("$env:COMPUTERNAME\$TaiKhoanNguoiDung")).Translate([Security.Principal.SecurityIdentifier]).Value
    $svc = New-Object -ComObject Schedule.Service; $svc.Connect()
    foreach ($tenTv in $Script:TenTacVuHeThong, $Script:TenTacVuNguoiDung) {
        $t = $svc.GetFolder('\').GetTask($tenTv)
        # 4 = DACL_SECURITY_INFORMATION; đọc cả SACL (0xF) cần SeSecurityPrivilege mà admin thường chưa bật.
        $sd = Add-AceVaoSddl $t.GetSecurityDescriptor(4) "(A;;GRGX;;;$sid)"
        $t.SetSecurityDescriptor($sd, 0)
    }
    Get-ScheduledTask -TaskName $Script:TenTacVuHeThong, $Script:TenTacVuNguoiDung -ErrorAction Stop |
        Select-Object TaskName, State, @{ n = 'User'; e = { $_.Principal.UserId } }, @{ n = 'Logon'; e = { $_.Principal.LogonType } } | Format-Table -AutoSize | Out-String | Write-Host
}

if ($NapHam) { return }

if ($PhamVi -notin 'NguoiDung', 'HeThong') { Write-Loi "-PhamVi '$PhamVi' không hợp lệ (NguoiDung | HeThong)"; exit 2 }
# -NhatKy/-ChiKiem chỉ có nghĩa cho MỘT lượt chạy; lịch luôn ghi nhật ký có dấu thời gian ở thư mục mặc định và luôn cài
# thật. Đi kèm -DangKyLich là mơ hồ ⇒ từ chối thay vì lặng lẽ bỏ (cross-review PR #1065 lượt 2, P1 `dang-ky-lam-mat-tham-so`).
if ($DangKyLich -and ($ChiKiem -or $NhatKy)) { Write-Loi '-NhatKy/-ChiKiem không đi kèm -DangKyLich (lịch luôn cài thật, nhật ký mặc định)'; exit 2 }

# ───────────────────────── chạy ─────────────────────────

if (-not $IsWindows) { Write-Loi 'chỉ chạy trên Windows'; exit 4 }
# Chốt tên máy TRƯỚC mọi thay đổi. Đo 31-10-2026: chủ kho chạy `-DangKyLich` nhầm trên laptop (cùng là Windows,
# cùng là admin) — script kịp chép vào Program Files và tạo C:\Tools\npm rồi mới chết ở icacls (1332, máy ấy không
# có tlcommander). Kiểm quyền admin không bắt được ca này; chỉ tên máy phân biệt được.
if ($env:COMPUTERNAME -ne $MayDich) { Write-Loi "máy này là '$env:COMPUTERNAME', không phải '$MayDich' — dừng, chưa đụng gì"; exit 5 }
$goc = if ((Split-Path $PSScriptRoot -Leaf) -eq 'vm') { (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path } else { $PSScriptRoot }
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$laAdmin = ([Security.Principal.WindowsPrincipal]$id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
$laSystem = $id.User.Value -eq 'S-1-5-18'

if ($DangKyLich) {
    if (-not $laAdmin) { Write-Loi '-DangKyLich cần PowerShell chạy bằng quyền admin'; exit 3 }
    try { Register-LichCapNhat $goc }
    catch { Write-Loi "-DangKyLich hỏng: $($_.Exception.Message)"; exit 6 }
    exit 0
}
if ($PhamVi -eq 'HeThong' -and -not ($laSystem -or $laAdmin)) { Write-Loi 'tầng HeThong cần SYSTEM hoặc admin'; exit 3 }

$batDau = Get-Date
Write-Host "cap-nhat-cong-cu: pham_vi=$PhamVi chi_kiem=$([bool]$ChiKiem) may=$env:COMPUTERNAME nguoi=$($id.Name)"
# Lưới cuối: lỗi lọt khỏi ranh giới từng công cụ vẫn thành một dòng `loi` và nhật ký vẫn được ghi (lượt 4, P1).
try { if ($PhamVi -eq 'NguoiDung') { Invoke-TangNguoiDung $goc } else { Invoke-TangHeThong } }
catch { Add-KetQua "tang-$PhamVi" '' '' 'loi' "dừng giữa chừng: $($_.Exception.Message)" }

$loi = @($Script:KetQua | Where-Object { $_.hanh_dong -eq 'loi' })
$tom = [ordered]@{
    pham_vi = $PhamVi; chi_kiem = [bool]$ChiKiem; may = $env:COMPUTERNAME; nguoi = $id.Name
    bat_dau = $batDau.ToString('o'); ket_thuc = (Get-Date).ToString('o')
    tong = $Script:KetQua.Count; loi = $loi.Count; ok = ($loi.Count -eq 0); ket_qua = $Script:KetQua
}
if (-not $NhatKy) {
    $thu = if ($PhamVi -eq 'HeThong') { Join-Path $env:ProgramData 'tra-luat-cap-nhat' } else { Join-Path $ThuMucCongCu 'nhat-ky-cap-nhat' }
    New-Item -ItemType Directory -Force -Path $thu | Out-Null
    $NhatKy = Join-Path $thu ("$PhamVi-" + $batDau.ToString('yyyyMMdd-HHmmss') + '.json')
}
$tom | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $NhatKy -Encoding utf8NoBOM
Write-Host "TONG: $($Script:KetQua.Count - $loi.Count)/$($Script:KetQua.Count) dat · loi $($loi.Count) · nhat ky: $NhatKy"
exit $(if ($loi.Count -eq 0) { 0 } else { 1 })
