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

# ── mã thoát của chính script (tiến trình con) ──
$pwsh = (Get-Process -Id $PID).Path
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

$dat = @($Ca.Values | Where-Object { $_ }).Count
Write-Host "cap-nhat-cong-cu tests: $dat/$($Ca.Count) ca QUA"
exit $(if ($dat -eq $Ca.Count) { 0 } else { 1 })
