#requires -Version 7.0
# Bộ test cho ops/vm/cap-nhat-cong-cu.ps1 — nạp hàm qua -NapHam rồi đo HÀNH VI, không mạng, không cài gì.
# Python dùng cho ca đọc bản kê: $env:TL_TEST_PYTHON, mặc định `python` trên PATH. THIẾU python/PyYAML thì
# ca đó ĐỎ, không BỎ QUA — "ca có mặt" khác "ca có đo" (CLAUDE.md).
$ErrorActionPreference = 'Stop'
$Here = $PSScriptRoot
$Script = Join-Path $Here 'cap-nhat-cong-cu.ps1'
. $Script -NapHam

$Ca = [ordered]@{}
function Ca([string]$Ten, [scriptblock]$Than) {
    try { $r = & $Than; $Ca[$Ten] = ($r -eq $true) } catch { $Ca[$Ten] = $false; Write-Host "  [$Ten] ném: $($_.Exception.Message)" }
    if (-not $Ca[$Ten]) { Write-Host "  DO  $Ten" }
}
function Nem([scriptblock]$B) { try { & $B; return $false } catch { return $true } }

# ── phiên bản ──
Ca 'phien_ban_git_windows' { (ConvertTo-PhienBan 'v2.56.0.windows.4') -eq [version]'2.56.0.4' -and (ConvertTo-PhienBan '2.47.1.windows.2') -eq [version]'2.47.1.2' }
Ca 'phien_ban_khong_doc_duoc_la_null' { $null -eq (ConvertTo-PhienBan 'abc') -and $null -eq (ConvertTo-PhienBan '') -and $null -eq (ConvertTo-PhienBan $null) }
Ca 'so_sanh_so_hoc_khong_chuoi' { (Compare-PhienBan '7.6.10' '7.6.9') -eq 1 -and (Compare-PhienBan '1.7.7' '1.7.7') -eq 0 -and (Compare-PhienBan '2.47.1.windows.2' 'v2.56.0.windows.4') -eq -1 }
Ca 'so_sanh_khong_biet_la_null' { $null -eq (Compare-PhienBan '' '1.2.3') -and $null -eq (Compare-PhienBan '1.2.3' 'x') }

# ── chọn asset: đúng MỘT ──
$rel = [pscustomobject]@{ tag_name = 'v1.0.0'; assets = @(
    [pscustomobject]@{ name = 'tool-1.0.0-x86_64-pc-windows-msvc.zip'; digest = 'sha256:' + ('a' * 64) },
    [pscustomobject]@{ name = 'tool-1.0.0-x86_64-pc-windows-msvc.zip.sha256'; digest = $null },
    [pscustomobject]@{ name = 'tool-1.0.0-aarch64-pc-windows-msvc.zip'; digest = $null }) }
Ca 'chon_dung_mot_asset' { (Select-TaiSan $rel 'x86_64-pc-windows-msvc\.zip$').name -eq 'tool-1.0.0-x86_64-pc-windows-msvc.zip' }
Ca 'khong_khop_thi_nem' { Nem { Select-TaiSan $rel 'linux' } }
Ca 'khop_nhieu_thi_nem' { Nem { Select-TaiSan $rel 'windows-msvc\.zip$' } }

# ── băm ──
$h1 = 'ab' * 32; $h2 = 'cd' * 32
$tepBam = "$h1  tool.zip`n$h2 *dist/tool.zip.sha256`r`n"
Ca 'tim_bam_dung_ten' { (Find-BamTrongTep $tepBam 'tool.zip') -eq $h1 }
Ca 'tim_bam_co_tien_to_duong_dan' { (Find-BamTrongTep $tepBam 'tool.zip.sha256') -eq $h2 }
Ca 'tim_bam_ten_vang_la_null' { $null -eq (Find-BamTrongTep $tepBam 'khac.zip') -and $null -eq (Find-BamTrongTep '' 'tool.zip') }
Ca 'van_ban_tu_mang_byte' { (ConvertTo-VanBan ([Text.Encoding]::UTF8.GetBytes("$h1  tool.zip"))) -eq "$h1  tool.zip" -and (Find-BamTrongTep (ConvertTo-VanBan ([Text.Encoding]::UTF8.GetBytes($tepBam))) 'tool.zip') -eq $h1 }
Ca 'van_ban_tu_chuoi_giu_nguyen' { (ConvertTo-VanBan 'abc') -eq 'abc' -and (ConvertTo-VanBan $null) -eq '' }
Ca 'bam_tu_digest_khong_can_mang' { (Get-BamTaiSan $rel $rel.assets[0]) -eq ('a' * 64) }
Ca 'khong_co_nguon_bam_la_null' {
    $r2 = [pscustomobject]@{ tag_name = 'v1'; assets = @([pscustomobject]@{ name = 'x.zip'; digest = $null }) }
    $null -eq (Get-BamTaiSan $r2 $r2.assets[0])
}

$tam = Join-Path ([IO.Path]::GetTempPath()) ("cncc-test-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory $tam | Out-Null
try {
    $tep = Join-Path $tam 'f.bin'
    Set-Content -LiteralPath $tep -Value 'noi dung' -NoNewline
    $dung = (Get-FileHash -LiteralPath $tep -Algorithm SHA256).Hash.ToLowerInvariant()
    Ca 'bam_khop_giu_tep' { Assert-Bam $tep $dung; Test-Path -LiteralPath $tep }
    Ca 'bam_khop_khong_phan_biet_hoa' { Assert-Bam $tep $dung.ToUpperInvariant(); Test-Path -LiteralPath $tep }
    Ca 'thieu_bam_thi_tu_choi_va_giu_tep' { (Nem { Assert-Bam $tep '' }) -and (Nem { Assert-Bam $tep $null }) -and (Test-Path -LiteralPath $tep) }
    Ca 'bam_lech_thi_xoa_tep' { (Nem { Assert-Bam $tep ('0' * 64) }) -and -not (Test-Path -LiteralPath $tep) }
} finally { Remove-Item -LiteralPath $tam -Recurse -Force -ErrorAction SilentlyContinue }

# ── Node: chỉ nâng trong cùng major ──
$idx = @([pscustomobject]@{ version = 'v26.13.0'; lts = 'Krypton' }, [pscustomobject]@{ version = 'v25.9.0'; lts = $false },
         [pscustomobject]@{ version = 'v24.23.0'; lts = 'Jod' }, [pscustomobject]@{ version = 'v24.22.1'; lts = 'Jod' },
         [pscustomobject]@{ version = 'v22.30.0'; lts = 'Iron' })
Ca 'node_cung_major' { $r = Select-NodeLts $idx '24.22.1'; $r.cung_major -eq '24.23.0' -and $r.moi_nhat -eq '26.13.0' }
Ca 'node_bo_qua_ban_khong_lts' { (Select-NodeLts $idx '25.1.0').cung_major -eq $null }
Ca 'node_chua_cai_lay_moi_nhat' { (Select-NodeLts $idx '').cung_major -eq '26.13.0' }
Ca 'node_major_cu_van_co_lts' { (Select-NodeLts $idx '22.1.0').cung_major -eq '22.30.0' }

# ── PATH ──
Ca 'path_them_vao_dau' { (Add-DuongDanVaoChuoi 'C:\a;C:\b' 'C:\Tools\bin') -eq 'C:\Tools\bin;C:\a;C:\b' }
Ca 'path_khong_nhan_doi' { (Add-DuongDanVaoChuoi 'C:\a;c:\tools\BIN\;C:\b' 'C:\Tools\bin') -eq 'C:\a;c:\tools\BIN\;C:\b' }
Ca 'path_rong' { (Add-DuongDanVaoChuoi '' 'C:\x') -eq 'C:\x' -and (Add-DuongDanVaoChuoi $null 'C:\x') -eq 'C:\x' }

# ── SDDL ──
$ace = '(A;;GRGX;;;S-1-5-21-1-2-3-1001)'
Ca 'sddl_noi_cuoi_khi_khong_co_sacl' { (Add-AceVaoSddl 'O:BAD:(A;;FA;;;SY)' $ace) -eq "O:BAD:(A;;FA;;;SY)$ace" }
Ca 'sddl_chen_truoc_sacl' { (Add-AceVaoSddl 'D:(A;;FA;;;SY)S:(AU;FA;FA;;;WD)' $ace) -eq "D:(A;;FA;;;SY)${ace}S:(AU;FA;FA;;;WD)" }
Ca 'sddl_khong_nhan_doi' { (Add-AceVaoSddl "D:(A;;FA;;;SY)$ace" $ace) -eq "D:(A;;FA;;;SY)$ace" }
Ca 'sddl_khong_dacl_thi_nem' { Nem { Add-AceVaoSddl 'O:BA' $ace } }

# ── bản kê: đọc ghim từ CHÍNH ops/cong_cu.yaml, đối chiếu bằng regex độc lập ──
Ca 'doc_ghim_tu_ban_ke_that' {
    $py = if ($env:TL_TEST_PYTHON) { $env:TL_TEST_PYTHON } else { 'python' }
    $yaml = Join-Path $Here '..\cong_cu.yaml'
    $g = Read-BanGhim $yaml $py
    $nd = Get-Content -LiteralPath $yaml -Raw
    $al = [regex]::Match($nd, '(?ms)^  actionlint:.*?ban_ghim:\s*"([^"]+)"').Groups[1].Value
    $g.actionlint -eq $al -and $g.PyYAML -match '^\d+\.\d+\.\d+$' -and $g.jsonschema -match '^\d+\.\d+\.\d+$' -and
        $nd.Contains("PyYAML==$($g.PyYAML)") -and $nd.Contains("jsonschema==$($g.jsonschema)")
}
Ca 'ban_ke_thieu_ghim_thi_nem' {
    $py = if ($env:TL_TEST_PYTHON) { $env:TL_TEST_PYTHON } else { 'python' }
    $t = Join-Path ([IO.Path]::GetTempPath()) ("cncc-" + [guid]::NewGuid().ToString('N') + '.yaml')
    Set-Content -LiteralPath $t -Value "cong_cu:`n  PyYAML: {cai: {lenh: 'pip install PyYAML==6.0.3'}}`n"
    try { Nem { Read-BanGhim $t $py } } finally { Remove-Item -LiteralPath $t -Force }
}

# ── tĩnh: mọi lệnh *-ScheduledTask* làm thay đổi phải có -ErrorAction Stop (hàm CDXML không thừa hưởng preference) ──
Ca 'scheduledtask_co_erroraction_stop' {
    $dong = @(Get-Content -LiteralPath $Script | Where-Object { $_ -match '^\s*Register-ScheduledTask\b' })
    $dong.Count -ge 2 -and -not ($dong | Where-Object { $_ -notmatch '-ErrorAction Stop' })
}
Ca 'dang_ky_loi_co_ma_thoat_rieng' { (Get-Content -LiteralPath $Script -Raw) -match 'catch \{ Write-Loi "-DangKyLich hỏng: [^"]*"; exit 6 \}' }

# ── cross-review PR #1065 lượt 1: mỗi finding một ca đo HÀNH VI ──
Ca 'co_tep_khong_doc_phien_ban_thi_khong_cai' {
    (Test-CoTheCai $true '') -eq $false -and (Test-CoTheCai $true $null) -eq $false -and
    (Test-CoTheCai $false '') -eq $true -and (Test-CoTheCai $true '24.1.0') -eq $true
}
Ca 'acl_chi_admin_ghi' {
    $ok = @([pscustomobject]@{ IdentityReference = 'NT AUTHORITY\SYSTEM'; FileSystemRights = 'FullControl'; AccessControlType = 'Allow' },
            [pscustomobject]@{ IdentityReference = 'BUILTIN\Administrators'; FileSystemRights = 'FullControl'; AccessControlType = 'Allow' },
            [pscustomobject]@{ IdentityReference = 'BUILTIN\Users'; FileSystemRights = 'ReadAndExecute, Synchronize'; AccessControlType = 'Allow' })
    $xau = $ok + @([pscustomobject]@{ IdentityReference = 'TRA-LUAT-WIN\tlcommander'; FileSystemRights = 'Modify, Synchronize'; AccessControlType = 'Allow' })
    @(Test-AclChiAdminGhi 'BUILTIN\Administrators' $ok).Count -eq 0 -and
    @(Test-AclChiAdminGhi 'BUILTIN\Administrators' $xau).Count -eq 1 -and
    @(Test-AclChiAdminGhi 'TRA-LUAT-WIN\tlcommander' $ok).Count -eq 1 -and
    @(Test-AclChiAdminGhi 'BUILTIN\Administrators' @([pscustomobject]@{ IdentityReference = 'BUILTIN\Users'; FileSystemRights = 'CreateFiles, Synchronize'; AccessControlType = 'Allow' })).Count -eq 1
}
Ca 'doi_so_tac_vu_mang_du_cau_hinh' {
    $MayDich = 'MAY-KHAC'; $ThuMucCongCu = 'D:\cong-cu'; $TacVuCommander = 'CMD-KHAC'
    $a = New-DoiSoTacVu 'C:\x\cap-nhat-cong-cu.ps1' 'HeThong'
    $a.Contains('-PhamVi "HeThong"') -and $a.Contains('-MayDich "MAY-KHAC"') -and $a.Contains('-ThuMucCongCu "D:\cong-cu"') -and
    $a.Contains('-TacVuCommander "CMD-KHAC"') -and $a.Contains('-NlmVenv "') -and $a.Contains('-VenvKho "') -and
    $a.Contains('-HomeCommander "') -and $a.Contains('-TaiKhoanNguoiDung "') -and (Nem { $MayDich = 'a"b'; New-DoiSoTacVu 'C:\x.ps1' 'HeThong' })
}
Ca 'reparse_trong_cay_bi_phat_hien' {
    $g = Join-Path ([IO.Path]::GetTempPath()) ("cncc-rp-" + [guid]::NewGuid().ToString('N')); $ngoai = "$g-ngoai"
    New-Item -ItemType Directory -Path "$g\con", $ngoai | Out-Null
    try {
        $sach = @(Find-Reparse $g).Count -eq 0
        $kieu = if ($IsWindows) { 'Junction' } else { 'SymbolicLink' }
        New-Item -ItemType $kieu -Path "$g\con\lienket" -Target $ngoai | Out-Null
        New-Item -ItemType $kieu -Path "$g-goc-la-lienket" -Target $ngoai | Out-Null
        $sach -and @(Find-Reparse $g).Count -eq 1 -and @(Find-Reparse "$g-goc-la-lienket").Count -eq 1 -and @(Find-Reparse "$g-khong-co").Count -eq 0
    } finally {
        foreach ($x in "$g\con\lienket", "$g-goc-la-lienket") { if (Test-Path -LiteralPath $x) { (Get-Item -LiteralPath $x -Force).Delete() } }
        Remove-Item -LiteralPath $g, $ngoai -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Ca 'dang_ky_chan_reparse_ca_hai_noi' {
    $ast = [Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $f = $ast.FindAll({ param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Register-LichCapNhat' }, $true)[0]
    $goi = @($f.FindAll({ param($n) $n -is [Management.Automation.Language.CommandAst] -and $n.GetCommandName() -eq 'Assert-KhongReparse' }, $true) | ForEach-Object { $_.Extent.Text })
    ($goi -contains 'Assert-KhongReparse $d') -and ($goi -contains 'Assert-KhongReparse $Script:ThuMucCaiDat')
}
Ca 'assert_khong_reparse_nem_khi_co_lien_ket' {
    $g = Join-Path ([IO.Path]::GetTempPath()) ("cncc-ak-" + [guid]::NewGuid().ToString('N')); $ngoai = "$g-ngoai"
    New-Item -ItemType Directory -Path $g, $ngoai | Out-Null
    try {
        $sach = -not (Nem { Assert-KhongReparse $g })
        New-Item -ItemType $(if ($IsWindows) { 'Junction' } else { 'SymbolicLink' }) -Path "$g\lk" -Target $ngoai | Out-Null
        $sach -and (Nem { Assert-KhongReparse $g })
    } finally {
        if (Test-Path -LiteralPath "$g\lk") { (Get-Item -LiteralPath "$g\lk" -Force).Delete() }
        Remove-Item -LiteralPath $g, $ngoai -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Ca 'icacls_dang_ky_khong_di_theo_lien_ket' {
    $ast = [Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $f = $ast.FindAll({ param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Register-LichCapNhat' }, $true)[0]
    $goi = @($f.FindAll({ param($n) $n -is [Management.Automation.Language.CommandAst] -and $n.CommandElements[0].Extent.Text -eq '$icacls' }, $true))
    $goi.Count -ge 4 -and -not ($goi | Where-Object { $_.Extent.Text -notmatch '\s/L\s' })
}
Ca 'thu_muc_tai_bo_thua_ke' {
    $ast = [Management.Automation.Language.Parser]::ParseFile($Script, [ref]$null, [ref]$null)
    $f = $ast.FindAll({ param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'New-ThuMucTai' }, $true)[0]
    $goi = $f.FindAll({ param($n) $n -is [Management.Automation.Language.CommandAst] -and $n.Extent.Text -match 'icacls\.exe' }, $true)[0]
    [bool](@($goi.CommandElements | ForEach-Object { $_.Extent.Text }) -contains '/inheritance:r')
}
Ca 'ma_thoat_2_pham_vi_sai' {
    & (Get-Process -Id $PID).Path -NoProfile -File $Script -PhamVi Sai *> $null
    $LASTEXITCODE -eq 2
}

# ── mã thoát của chính script (tiến trình con) ──
$pwsh = (Get-Process -Id $PID).Path
# Không có ProgramFiles (như Linux): nạp hàm vẫn được, và chạy thường vẫn tới được chốt (mã 4 ngoài Windows, mã 5 sai máy
# trên Windows) thay vì chết ở dòng khởi tạo — Codex review P2 trên PR #1065.
$boPF = "Remove-Item Env:ProgramFiles -ErrorAction SilentlyContinue; "
Ca 'napham_khong_can_programfiles' {
    & $pwsh -NoProfile -Command ($boPF + ". '$Script' -NapHam; if (Get-Command Select-TaiSan -ErrorAction SilentlyContinue) { exit 0 } else { exit 9 }") *> $null
    $LASTEXITCODE -eq 0
}
Ca 'khong_programfiles_van_toi_chot' {
    & $pwsh -NoProfile -Command ($boPF + "& '$Script' -ChiKiem -MayDich 'KHONG-PHAI-MAY-NAY'; exit `$LASTEXITCODE") *> $null
    $LASTEXITCODE -eq $(if ($IsWindows) { 5 } else { 4 })
}
if (-not $IsWindows) {
    Ca 'khong_phai_windows_thoat_4' { & $pwsh -NoProfile -File $Script -ChiKiem *> $null; $LASTEXITCODE -eq 4 }
} else {
    Ca 'sai_may_thoat_5_truoc_moi_thay_doi' {
        $gia = 'KHONG-PHAI-' + $env:COMPUTERNAME
        $o = & $pwsh -NoProfile -File $Script -DangKyLich -MayDich $gia 2>&1 | Out-String
        $LASTEXITCODE -eq 5 -and $o.Contains($gia)
    }
    $laAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $laAdmin) {
        Ca 'he_thong_khong_admin_thoat_3' { & $pwsh -NoProfile -File $Script -PhamVi HeThong -ChiKiem -MayDich $env:COMPUTERNAME *> $null; $LASTEXITCODE -eq 3 }
        Ca 'dang_ky_lich_khong_admin_thoat_3' { & $pwsh -NoProfile -File $Script -DangKyLich -MayDich $env:COMPUTERNAME *> $null; $LASTEXITCODE -eq 3 }
    } else {
        Ca 'admin_ca_ma_thoat_3_khong_do_duoc' { Write-Host '  chạy bằng admin: ca mã thoát 3 không đo được ở đây — chạy lại bằng tài khoản thường'; $false }
    }
}

# ── luồng thật với đồ giả (CHẠY CUỐI: các hàm giả che hàm của script) — gợi ý của cross-review lượt 1 ──
$tamGia = Join-Path ([IO.Path]::GetTempPath()) ("cncc-gia-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory $tamGia | Out-Null
$pfCu = $env:ProgramFiles
try {
    $Script:Payload = 'payload-offline'; $Script:VanBanMang = ''
    function Invoke-WebRequest { param($Uri, $Headers, $TimeoutSec, $OutFile)
        if ($OutFile) { [IO.File]::WriteAllText($OutFile, $Script:Payload); return }
        [pscustomobject]@{ Content = $Script:VanBanMang } }
    Ca 'save_that_su_kiem_bam_va_xoa_tep_lech' {
        (Nem { Save-CoKiemBam 'OFFLINE' ('0' * 64) $tamGia 'xau.msi' }) -and -not (Test-Path (Join-Path $tamGia 'xau.msi'))
    }
    $ts = [pscustomobject]@{ name = 'muon.msi'; digest = $null }
    $rl = [pscustomobject]@{ assets = @($ts, [pscustomobject]@{ name = 'muon.msi.sha256'; browser_download_url = 'OFFLINE' }) }
    Ca 'sidecar_ten_khac_bi_tu_choi' { $Script:VanBanMang = ('a' * 64) + '  khac.msi'; $null -eq (Get-BamTaiSan $rl $ts) }
    Ca 'sidecar_bam_tran_duoc_nhan' { $Script:VanBanMang = ('a' * 64) + "`n"; (Get-BamTaiSan $rl $ts) -eq ('a' * 64) }
    Ca 'sidecar_chon_dung_dong_ten' {
        $Script:VanBanMang = ('a' * 64) + "  khac.msi`n" + ('b' * 64) + "  muon.msi`n"; (Get-BamTaiSan $rl $ts) -eq ('b' * 64)
    }

    $env:ProgramFiles = Join-Path $tamGia 'PF'
    New-Item -ItemType Directory -Path (Join-Path $env:ProgramFiles 'nodejs') | Out-Null
    [IO.File]::WriteAllText((Join-Path $env:ProgramFiles 'nodejs/node.exe'), 'chi-co-mat')
    $Script:CheDo = ''; $Script:DaCai = $false; $Script:DaDungLai = $false; $Script:CoLucCai = $false
    function Get-PhienBanLenh($Exe, $DoiSo, $Mau) {
        if ($Exe -match 'git.exe$') { return '2.56.0.windows.4' }
        if ($Exe -match 'gh.exe$') { return '1.0.0' }
        if ($Exe -match 'pwsh.exe$') { return '7.6.9' }
        if ($Script:CheDo -eq 'khong-doc') { return $null }
        return '24.1.0' }
    function Get-Release($Repo) {
        $tag = '7.6.9'; $f = 'PowerShell-7.6.9-win-x64.msi'
        if ($Repo -eq 'git-for-windows/git') { $tag = '2.56.0.windows.4'; $f = 'Git-2.56.0-64-bit.exe' }
        if ($Repo -eq 'cli/cli') { $tag = '1.0.0'; $f = 'gh_1.0.0_windows_amd64.msi' }
        [pscustomobject]@{ tag_name = "v$tag"; assets = @([pscustomobject]@{ name = $f; browser_download_url = 'OFFLINE' }) } }
    function Invoke-RestMethod { param($Uri, $TimeoutSec) @([pscustomobject]@{ version = 'v26.2.0'; lts = 'moi' }, [pscustomobject]@{ version = 'v24.2.0'; lts = 'cu' }) }
    function Save-CoKiemBam($Url, $Bam, $ThuMuc, $Ten) { Join-Path $tamGia $Ten }
    function Install-Msi($Msi, $Ten) { $Script:DaCai = $true; $Script:CoLucCai = $Script:DaCaiNode; throw 'msi-hong-sau-khi-node-co-the-da-tat' }
    function Stop-ScheduledTask { param($TaskName, $ErrorAction) }
    function Start-ScheduledTask { param($TaskName, $ErrorAction) $Script:DaDungLai = $true }
    function Get-ScheduledTask { param($TaskName, $ErrorAction) [pscustomobject]@{ State = 'Running' } }
    function Start-Sleep { param($Seconds) }
    function New-ThuMucTai { param([switch]$ChiAdmin) $d = Join-Path $tamGia ([guid]::NewGuid().ToString('N')); New-Item -ItemType Directory $d | Out-Null; $d }
    $Script:VanBanMang = ('a' * 64) + "  node-v26.2.0-x64.msi`n" + ('a' * 64) + "  node-v24.2.0-x64.msi`n"
    Ca 'node_co_tep_khong_doc_phien_ban_khong_cai' {
        $Script:CheDo = 'khong-doc'; $Script:DaCai = $false; $Script:DaCaiNode = $false; $Script:KetQua.Clear()
        Invoke-TangHeThong *> $null
        -not $Script:DaCai -and @($Script:KetQua | Where-Object { $_.cong_cu -eq 'node' -and $_.hanh_dong -eq 'loi' }).Count -eq 1
    }
    Ca 'node_cai_hong_van_dung_lai_commander' {
        $Script:CheDo = ''; $Script:DaCai = $false; $Script:DaDungLai = $false; $Script:CoLucCai = $false; $Script:DaCaiNode = $false; $Script:KetQua.Clear()
        Invoke-TangHeThong *> $null
        $Script:DaCai -and $Script:CoLucCai -and $Script:DaDungLai -and
            @($Script:KetQua | Where-Object { $_.cong_cu -eq 'node-major' -and $_.hanh_dong -eq 'can_quyet_dinh' }).Count -eq 1
    }
} finally {
    $env:ProgramFiles = $pfCu
    Remove-Item -LiteralPath $tamGia -Recurse -Force -ErrorAction SilentlyContinue
}

$dat = @($Ca.Values | Where-Object { $_ }).Count
Write-Host "cap-nhat-cong-cu tests: $dat/$($Ca.Count) ca QUA"
exit $(if ($dat -eq $Ca.Count) { 0 } else { 1 })
