
param([string]$Product, [string]$Mode, [string]$OutFile)
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $Product
. $Product -NapHam
$pfCu = $env:ProgramFiles
$DungLai = 'OFFLINE-DUNG-TRUOC-MAT-KHAU'
$cuCauHinh = @{ ThuMucCongCu = $ThuMucCongCu; NlmVenv = $NlmVenv; VenvKho = $VenvKho; HomeCommander = $HomeCommander; TacVuCommander = $TacVuCommander; MayDich = $MayDich }
$cuMay = $env:COMPUTERNAME
function Invoke-DangKyGia([string]$CheDo) {
    $g = Join-Path ([IO.Path]::GetTempPath()) ("cncc-dk-" + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $g, "$g/PF/tra-luat-ops", "$g/nan-nhan/npm", "$g/nan-nhan/Python312", "$g/nan-nhan/bin" | Out-Null
    $lk = $(if ($IsWindows) { 'Junction' } else { 'SymbolicLink' })
    $Script:ThuMucCongCu = Join-Path $g 'Tools'
    # Tổ tiên của cây công cụ là LIÊN KẾT tới thư mục nạn nhân — mọi ca đều chạy trên cây độc này.
    New-Item -ItemType $lk -Path $Script:ThuMucCongCu -Target "$g/nan-nhan" | Out-Null
    $env:ProgramFiles = Join-Path $g 'PF'
    if ($CheDo -eq 'pf-lien-ket') {
        Remove-Item -LiteralPath $env:ProgramFiles -Recurse -Force
        New-Item -ItemType Directory -Path "$g/pf-that/tra-luat-ops" | Out-Null
        New-Item -ItemType $lk -Path $env:ProgramFiles -Target "$g/pf-that" | Out-Null
    }
    if ($CheDo -eq 'cai-dat-lien-ket') {
        Remove-Item -LiteralPath "$g/PF/tra-luat-ops" -Recurse -Force
        New-Item -ItemType $lk -Path "$g/PF/tra-luat-ops" -Target "$g/nan-nhan" | Out-Null
    }
    $Script:AclGia = @{}
    $Script:AclGia[(Join-Path $env:ProgramFiles 'tra-luat-ops')] = [pscustomobject]@{ Owner = "$env:COMPUTERNAME\tladmin"; Access = @(New-QuyenGia 'BUILTIN\Users' 'Modify') }
    if ($CheDo -in 'ban-cu', 'dacl-rong', 'cay-long') {
        # Bản cài cũ có sẵn ba tệp, ACL thừa kế từ Program Files (đúng trạng thái VM trước lần đăng ký lại).
        foreach ($t in 'cap-nhat-cong-cu.ps1', 'cong_cu.yaml', 'requirements.txt') {
            $f = Join-Path (Join-Path $env:ProgramFiles 'tra-luat-ops') $t; [IO.File]::WriteAllText($f, 'cu')
            $Script:AclGia[$f] = [pscustomobject]@{ Owner = 'BUILTIN\Administrators'; Access = @((New-QuyenGia 'NT AUTHORITY\SYSTEM' 'FullControl'), (New-QuyenGia 'BUILTIN\Administrators' 'FullControl'), (New-QuyenGia 'BUILTIN\Users' 'ReadAndExecute, Synchronize')) }
        }
    }

    if ($CheDo -eq 'dacl-rong') {
        foreach ($p in @($Script:AclGia.Keys)) {
            if ($p -ne (Join-Path $env:ProgramFiles 'tra-luat-ops')) { $Script:AclGia[$p].Access = @() }
        }
    }
    if ($CheDo -eq 'cay-long') {
        $root = Join-Path $env:ProgramFiles 'tra-luat-ops'
        foreach ($relative in 'long', 'long/sau') {
            New-Item -ItemType Directory -Path (Join-Path $root $relative) | Out-Null
        }
        foreach ($relative in '.tep-an', 'long/sau/.tep-an', 'long/sau/khong-duoi') {
            [IO.File]::WriteAllText((Join-Path $root $relative), 'cu')
        }
        foreach ($relative in 'long', 'long/sau', '.tep-an', 'long/sau/.tep-an', 'long/sau/khong-duoi') {
            $Script:AclGia[(Join-Path $root $relative)] = [pscustomobject]@{
                Owner = 'BUILTIN\Administrators'; Access = @(New-QuyenGia 'BUILTIN\Users' 'Modify')
            }
        }
    }
    $Script:GiaCheDo = $CheDo; $Script:SuKien = [Collections.Generic.List[object]]::new()
    $Script:HanhDong = [Collections.Generic.List[object]]::new(); $Script:TacVu = [Collections.Generic.List[object]]::new()
    $Script:NlmVenv = 'D:\nlm venv\'; $Script:VenvKho = 'D:\repo venv\\'; $Script:HomeCommander = 'D:\profile rieng'
    $Script:TacVuCommander = 'CMD-RIENG'; $Script:MayDich = 'MAY-GIA'; $env:COMPUTERNAME = 'MAY-GIA'
    $loi = $null
    try { Register-LichCapNhat (Resolve-Path (Join-Path $Here '../..')).Path *> $null } catch { $loi = $_.Exception.Message }
    $kq = [pscustomobject]@{
        acl = $Script:AclGia; loi = $loi; su_kien = @($Script:SuKien); hanh_dong = @($Script:HanhDong); tac_vu = @($Script:TacVu); cai_dat = $Script:ThuMucCaiDat
        tep = @(Get-ChildItem -LiteralPath (Join-Path $g 'PF/tra-luat-ops') -File -ErrorAction SilentlyContinue | ForEach-Object Name)
    }
    foreach ($l in "$g/PF", "$g/PF/tra-luat-ops", "$g/Tools") {
        $it = Get-Item -LiteralPath $l -Force -ErrorAction SilentlyContinue
        if ($it -and ($it.Attributes -band [IO.FileAttributes]::ReparsePoint)) { $it.Delete() }
    }
    Remove-Item -LiteralPath $g -Recurse -Force -ErrorAction SilentlyContinue
    $kq
}
try {
    # Mô hình chỉ hỗ trợ tập lệnh đăng ký này; đọc target, /T, SID owner và từng grant.
    # Không mô phỏng NTFS/effective access; tệp mới chép kế thừa các grant OI/CI của thư mục.
    function New-QuyenGia($Id, $Rights) { [pscustomobject]@{ IdentityReference = $Id; FileSystemRights = $Rights; AccessControlType = 'Allow' } }
    function Get-DanhTinhGia([string]$Id) {
        switch ($Id.TrimStart('*')) {
            'S-1-5-18' { 'NT AUTHORITY\SYSTEM' }
            'S-1-5-32-544' { 'BUILTIN\Administrators' }
            'S-1-5-32-545' { 'BUILTIN\Users' }
            default { $Id }
        }
    }
    function Invoke-Icacls([string[]]$DoiSo) {
        $Script:SuKien.Add([pscustomobject]@{ loai = 'icacls'; doi_so = $DoiSo })
        # Mô hình theo HÀNH VI THẬT đo trên VM 31-10-2026 (không theo tài liệu): đích `<thư mục>/*` = chỉ các nút con; trên TỆP,
        # ACE mang cờ (OI)/(CI) KHÔNG được áp (nên `/inheritance:r /grant:r (OI)(CI) /T` để tệp với DACL rỗng); `/reset` = tệp thừa
        # kế lại ACE của thư mục cha.
        $dich = $DoiSo[0]; $chiCon = $dich -match '[\\/]\*$'
        $goc = if ($chiCon) { $dich -replace '[\\/]\*$', '' } else { $dich }
        $prefix = $goc.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
        foreach ($key in @($Script:AclGia.Keys)) {
            $laCon = $key.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)
            $khop = if ($chiCon) { $laCon } else { $key -eq $goc -or (($DoiSo -contains '/T') -and $laCon) }
            if (-not $khop) { continue }
            $node = $Script:AclGia[$key]
            if ($DoiSo -contains '/reset') { $node.Access = @($Script:AclGia[$goc].Access); continue }
            if ($DoiSo -contains '/setowner') {
                $i = [array]::IndexOf($DoiSo, '/setowner'); $node.Owner = Get-DanhTinhGia $DoiSo[$i + 1]
            }
            if ($DoiSo -contains '/inheritance:r') { $node.Access = @() }
            if ($DoiSo -contains '/grant:r') {
                $i = [array]::IndexOf($DoiSo, '/grant:r') + 1
                while ($i -lt $DoiSo.Count -and $DoiSo[$i] -notmatch '^/') {
                    if ($DoiSo[$i] -notmatch '^([^:]+):(?:(?:\(OI\)|\(CI\))*)(F|RX|M)$') { throw "grant ngoài mô hình: $($DoiSo[$i])" }
                    $id = Get-DanhTinhGia $Matches[1]
                    $rights = switch ($Matches[2]) { 'F' { 'FullControl' } 'RX' { 'ReadAndExecute, Synchronize' } 'M' { 'Modify' } }
                    if (-not ($laCon -and $DoiSo[$i] -match '\((OI|CI)\)')) {
                        $node.Access = @($node.Access | Where-Object IdentityReference -ne $id) + @(New-QuyenGia $id $rights)
                    }
                    $i++
                }
            }
        }
    }
    function Copy-Item { param($LiteralPath, $Destination, [switch]$Force)
        $Script:SuKien.Add([pscustomobject]@{ loai = 'chep'; dich = "$Destination" })
        # Ghi đè tệp có sẵn cần Administrators có quyền ghi trên CHÍNH tệp ấy (DACL rỗng ⇒ bị từ chối, như trên VM).
        $cu = $Script:AclGia["$Destination"]
        if ($cu -and -not @($cu.Access | Where-Object { $_.IdentityReference -eq 'BUILTIN\Administrators' -and $_.FileSystemRights -eq 'FullControl' }).Count) {
            throw [UnauthorizedAccessException]::new("Access to the path '$Destination' is denied.")
        }
        Microsoft.PowerShell.Management\Copy-Item -LiteralPath $LiteralPath -Destination $Destination -Force:$Force
        $parent = Split-Path -Parent $Destination
        $Script:AclGia["$Destination"] = [pscustomobject]@{ Owner = "$env:COMPUTERNAME\tladmin"; Access = @($Script:AclGia[$parent].Access) } }
    function Get-Acl { param($LiteralPath)
        $p = "$LiteralPath"; $caiDat = $p.StartsWith($Script:ThuMucCaiDat)
        if ($caiDat) { $Script:SuKien.Add([pscustomobject]@{ loai = 'do_acl'; dich = $p }) }
        if ($caiDat) {
            $node = $Script:AclGia[$p]
            if (-not $node) { throw "thiếu trạng thái ACL giả: $p" }
            $access = @($node.Access)
            if ($Script:GiaCheDo -eq 'acl-sai') { $access += New-QuyenGia 'BUILTIN\Users' 'Modify' }
            return [pscustomobject]@{ Owner = $node.Owner; Access = $access }
        }
        [pscustomobject]@{ Owner = "$env:COMPUTERNAME\tlcommander"; Access = @(New-QuyenGia 'BUILTIN\Users' 'ReadAndExecute, Synchronize') } }
    function Get-FileHash { param($LiteralPath)
        if ($Script:GiaCheDo -eq 'bam-lech' -and "$LiteralPath".StartsWith($Script:ThuMucCaiDat)) { return [pscustomobject]@{ Hash = 'LECH' } }
        Microsoft.PowerShell.Utility\Get-FileHash -LiteralPath $LiteralPath }
    function New-ScheduledTaskSettingsSet { param([switch]$StartWhenAvailable, $ExecutionTimeLimit, $MultipleInstances) [pscustomobject]@{ swa = [bool]$StartWhenAvailable } }
    function New-ScheduledTaskTrigger { param([switch]$Weekly, $WeeksInterval, $DaysOfWeek, $At) [pscustomobject]@{ At = $At; WeeksInterval = $WeeksInterval } }
    function New-ScheduledTaskAction { param($Execute, $Argument) $a = [pscustomobject]@{ Execute = $Execute; Argument = $Argument }; $Script:HanhDong.Add($a); $a }
    function New-ScheduledTaskPrincipal { param($UserId, $LogonType, $RunLevel) [pscustomobject]@{ UserId = $UserId; LogonType = $LogonType; RunLevel = $RunLevel } }
    function Register-ScheduledTask { param($TaskName, $Action, $Trigger, $Principal, $Settings, [switch]$Force, $ErrorAction, $User, $Password, $RunLevel)
        $Script:TacVu.Add([pscustomobject]@{ ten = $TaskName; hanh_dong = $Action; chu = $Principal; cai_dat = $Settings; ea = "$ErrorAction" }) }
    function Get-Credential { param($UserName, $Message) throw $DungLai }

    $dungLaiDung = { param($k) $k.loi -eq $DungLai -and $k.tac_vu.Count -eq 1 }

    $k = Invoke-DangKyGia $Mode
    $events = @($k.su_kien | ForEach-Object {
        [ordered]@{ type=$_.loai; target=$_.dich; argv=$_.doi_so }
    })
    $states = @($k.acl.Keys | Sort-Object | ForEach-Object {
        $node = $k.acl[$_]
        [ordered]@{ path=$_; owner=$node.Owner; access=$node.Access; violations=@(Test-AclChiAdminGhi $node.Owner $node.Access) }
    })
    [ordered]@{ mode=$Mode; error=$k.loi; tasks=$k.tac_vu.Count; files=$k.tep; states=$states; events=$events } |
        ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutFile -Encoding utf8NoBOM
} finally {
    $env:ProgramFiles = $pfCu
    $env:COMPUTERNAME = $cuMay
}
