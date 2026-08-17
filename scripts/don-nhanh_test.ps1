<#
.SYNOPSIS
  Phản chứng cho `don-nhanh.ps1`. Chạy: pwsh -NoProfile -File scripts/don-nhanh_test.ps1

.DESCRIPTION
  VÌ SAO ĐO BẰNG KHO GIT THẬT, CHỈ GIẢ `gh`
  Kho này đã trả giá cho đồ giả DIỄN KỊCH BẢN: bộ test của `ops-don-ref` từng cho 40/40
  trong khi một đột biến XOÁ HẲN lệnh xoá vẫn qua, vì `gh` giả trả lời theo kịch bản
  thay vì mô phỏng TRẠNG THÁI. Nên ở đây `git` là git THẬT, "remote" là một kho bare
  THẬT, và phép đo cuối cùng luôn là `git ls-remote` hỏi lại kho bare ấy — tức đo
  THAO TÁC CÓ XẢY RA KHÔNG, không đo script đã in gì.

  Chỉ `gh` là giả, vì nó là thứ duy nhất thật sự nằm ngoài máy.

  MỖI CA MỘT KHO RIÊNG. Ca trước xoá nhánh thì ca sau không được thấy hậu quả ấy.
#>

[CmdletBinding()]
param([string]$LapCa = '')

$ErrorActionPreference = 'Stop'
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
} catch { }

$KichBan = Join-Path $PSScriptRoot 'don-nhanh.ps1'
if (-not (Test-Path $KichBan)) { Write-Host "THIEU $KichBan" -ForegroundColor Red; exit 3 }
$PwshExe = (Get-Process -Id $PID).Path
if (-not $PwshExe) { $PwshExe = 'pwsh' }

$script:CA = [ordered]@{}
function ca([string]$ten, [scriptblock]$than) { $script:CA[$ten] = $than }
function bang([bool]$dk, [string]$vi) { if (-not $dk) { throw $vi } }

function Git-Tho {
    param([string]$Cwd, [Parameter(ValueFromRemainingArguments)][string[]]$Doi)
    $out = & git -C $Cwd @Doi 2>&1
    if ($LASTEXITCODE -ne 0) { throw "git $($Doi -join ' ') rc=$LASTEXITCODE : $out" }
    return [string[]]($out | ForEach-Object { "$_" })
}

function Dung-Kho {
    <#  Kho bare lam "remote" + worktree co origin tro vao no.
        Tra ve @{ ban; lam }.  #>
    $goc = Join-Path ([System.IO.Path]::GetTempPath()) ("dn-" + [guid]::NewGuid().ToString('N').Substring(0, 10))
    $ban = Join-Path $goc 'origin.git'
    $lam = Join-Path $goc 'lam'
    New-Item -ItemType Directory -Path $goc, $lam -Force | Out-Null
    & git init -q --bare $ban 2>&1 | Out-Null
    & git init -q -b master $lam 2>&1 | Out-Null
    Git-Tho $lam config user.email 'test@example.invalid' | Out-Null
    Git-Tho $lam config user.name  'test' | Out-Null
    Git-Tho $lam remote add origin $ban | Out-Null
    Set-Content -Path (Join-Path $lam 'a.txt') -Value 'goc' -NoNewline
    Git-Tho $lam add -A | Out-Null
    Git-Tho $lam commit -q -m goc | Out-Null
    Git-Tho $lam push -q origin master | Out-Null
    return @{ ban = $ban; lam = $lam; goc = $goc }
}

function Them-Nhanh {
    <#  $DaMerge=$true  -> nhanh tro DUNG master hien tai (moi commit cua no da o master)
        $DaMerge=$false -> nhanh co mot commit RIENG chua vao master  #>
    param([hashtable]$K, [string]$Ten, [bool]$DaMerge)
    if ($DaMerge) {
        Git-Tho $K.lam branch $Ten master | Out-Null
    } else {
        Git-Tho $K.lam checkout -q -b $Ten master | Out-Null
        Set-Content -Path (Join-Path $K.lam "$($Ten -replace '[/\\]', '_').txt") -Value 'rieng' -NoNewline
        Git-Tho $K.lam add -A | Out-Null
        Git-Tho $K.lam commit -q -m "rieng $Ten" | Out-Null
        Git-Tho $K.lam checkout -q master | Out-Null
    }
    Git-Tho $K.lam push -q origin $Ten | Out-Null
}

function Nhanh-Tren-Remote {
    param([hashtable]$K)
    return @(Git-Tho $K.lam ls-remote --heads origin |
             ForEach-Object { ($_ -split "`t")[-1] -replace '^refs/heads/', '' } |
             Sort-Object)
}

function Dung-Gh-Gia {
    <#  `gh` gia tra ve DUNG JSON ma `gh pr list --json headRefName,baseRefName` tra ve.
        Tra ve thu muc de dat len PATH. $null nghia la KHONG dung gh gia.  #>
    param([object[]]$PR)
    $d = Join-Path ([System.IO.Path]::GetTempPath()) ("gh-" + [guid]::NewGuid().ToString('N').Substring(0, 10))
    New-Item -ItemType Directory -Path $d -Force | Out-Null
    $json = (ConvertTo-Json -InputObject @($PR) -Compress -Depth 5)
    # `ConvertTo-Json` tren mang RONG cho "[]" — dung thu that `gh` tra ve.
    $p = Join-Path $d 'gh'
    # In NGUYEN VAN roi thoat 0. Khong dien kich ban theo lan goi thu may.
    Set-Content -Path $p -Value @("#!/bin/sh", "cat <<'JSONEOF'", $json, "JSONEOF") -Encoding utf8
    & chmod +x $p
    return $d
}

function Chay-KichBan {
    <#  Chay don-nhanh.ps1 trong mot tien trinh RIENG, cwd = worktree, PATH do ta dung.
        Tra @{ rc; ra }.  #>
    param([hashtable]$K, [string]$ThuMucGh, [string[]]$Doi = @())
    $pathCu = $env:PATH
    try {
        # PATH toi thieu + (tuy chon) thu muc chua `gh` gia. KHONG de lot `gh` that cua may.
        $env:PATH = if ($ThuMucGh) { "$ThuMucGh$([IO.Path]::PathSeparator)/usr/bin$([IO.Path]::PathSeparator)/bin" }
                    else { "/usr/bin$([IO.Path]::PathSeparator)/bin" }
        Push-Location $K.lam
        try {
            $ra = & $PwshExe -NoProfile -File $KichBan @Doi 2>&1
            $rc = $LASTEXITCODE
        } finally { Pop-Location }
    } finally { $env:PATH = $pathCu }
    return @{ rc = $rc; ra = ([string[]]($ra | ForEach-Object { "$_" })) -join "`n" }
}

# ---------------------------------------------------------------- các ca

ca 't1_BASE_cua_PR_dang_mo_DA_MERGE_thi_GIU' {
    # CA TRUNG TAM CUA BAN VA NAY.
    # `nen/tichhop` DA vao master (lop 1 noi "xoa duoc" va no dung ve COMMIT) nhung
    # dang la BASE cua mot PR con mo -> xoa se DONG PR do.
    $k = Dung-Kho
    Them-Nhanh $k 'nen/tichhop' $true
    Them-Nhanh $k 'con/dang-lam' $false
    Them-Nhanh $k 'ops/rac' $true
    $gh = Dung-Gh-Gia @(@{ headRefName = 'con/dang-lam'; baseRefName = 'nen/tichhop' })
    $r = Chay-KichBan $k $gh @('-Xoa')
    $con = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc), doi 0. Ra:`n$($r.ra)"
    bang ($con -contains 'nen/tichhop') "BASE cua PR dang mo DA BI XOA — day dung la lo can va. Con lai: $($con -join ', ')"
    bang (-not ($con -contains 'ops/rac')) "nhanh rac le ra phai bi xoa. Con lai: $($con -join ', ')"
}

ca 't2_HEAD_cua_PR_dang_mo_DA_MERGE_thi_GIU' {
    # Head DA vao master bang duong khac trong khi PR van mo -> lop 1 khong che nua.
    $k = Dung-Kho
    Them-Nhanh $k 'con/da-vao-master' $true
    $gh = Dung-Gh-Gia @(@{ headRefName = 'con/da-vao-master'; baseRefName = 'master' })
    $r = Chay-KichBan $k $gh @('-Xoa')
    $con = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc). Ra:`n$($r.ra)"
    bang ($con -contains 'con/da-vao-master') "HEAD cua PR dang mo da bi xoa. Con lai: $($con -join ', ')"
}

ca 't3_nhanh_DA_MERGE_khong_lien_quan_PR_thi_XOA' {
    # Doi chung DUONG: neu ca nay xanh vi script khong xoa gi thi t1/t2 vo nghia.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $gh = Dung-Gh-Gia @()
    $r = Chay-KichBan $k $gh @('-Xoa')
    $con = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc). Ra:`n$($r.ra)"
    bang (-not ($con -contains 'ops/xong-viec')) "nhanh da merge KHONG bi xoa — script co the dang khong lam gi. Con lai: $($con -join ', ')"
    bang ($con -contains 'master') "master bi xoa (!). Con lai: $($con -join ', ')"
}

ca 't4_nhanh_CHUA_MERGE_thi_GIU' {
    $k = Dung-Kho
    Them-Nhanh $k 'ops/dang-lam' $false
    $gh = Dung-Gh-Gia @()
    $r = Chay-KichBan $k $gh @('-Xoa')
    $con = Nhanh-Tren-Remote $k
    bang ($con -contains 'ops/dang-lam') "nhanh CHUA merge bi xoa. Con lai: $($con -join ', ')"
}

ca 't5_khong_gh_va_Xoa_thi_TU_CHOI_va_KHONG_xoa_gi' {
    # FAIL-CLOSE. Do hai thu doc lap: ma thoat, VA trang thai remote.
    # Chi do ma thoat thi mot ban "in loi roi van xoa" van xanh.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $truoc = Nhanh-Tren-Remote $k
    $r = Chay-KichBan $k $null @('-Xoa')
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13 (tu choi vi khong do duoc PR). Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa du da tu choi: truoc=[$($truoc -join ', ')] sau=[$($sau -join ', ')]"
}

ca 't6_khong_gh_nhung_BoQuaLopPR_tuong_minh_thi_van_xoa' {
    # Cua thoat phai THAT SU mo — neu khong, chot tren chi la be tac.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $r = Chay-KichBan $k $null @('-Xoa', '-BoQuaLopPR')
    $con = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc), doi 0. Ra:`n$($r.ra)"
    bang (-not ($con -contains 'ops/xong-viec')) "-BoQuaLopPR khong xoa duoc gi. Con lai: $($con -join ', ')"
}

ca 't7_dry_run_khong_dung_ref_nao' {
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia @()
    $r = Chay-KichBan $k $gh @()
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc). Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "DRY RUN da doi remote: truoc=[$($truoc -join ', ')] sau=[$($sau -join ', ')]"
    bang ($r.ra -match 'DRY RUN') "khong thay dong DRY RUN trong dau ra"
}

ca 't8_luu_tru_DA_MERGE_van_GIU' {
    $k = Dung-Kho
    Them-Nhanh $k 'luu-tru/ho-so-cu' $true
    $gh = Dung-Gh-Gia @()
    $r = Chay-KichBan $k $gh @('-Xoa')
    $con = Nhanh-Tren-Remote $k
    bang ($con -contains 'luu-tru/ho-so-cu') "nhanh luu-tru/* bi xoa. Con lai: $($con -join ', ')"
}

ca 't9_mot_PR_duy_nhat_van_doc_duoc_base' {
    # `ConvertFrom-Json` tra ve OBJECT DON (khong phai mang) khi JSON co dung 1 phan tu.
    # Khong ep [object[]] thi `.baseRefName` van chay nhung `$js.Count` sai va mot vai
    # duong xu ly mang im lang hong. Ca nay khoa dung cho ay.
    $k = Dung-Kho
    Them-Nhanh $k 'nen/mot' $true
    $gh = Dung-Gh-Gia @(@{ headRefName = 'khong-ton-tai'; baseRefName = 'nen/mot' })
    $r = Chay-KichBan $k $gh @('-Xoa')
    $con = Nhanh-Tren-Remote $k
    bang ($con -contains 'nen/mot') "base cua PR DUY NHAT bi xoa. Ra:`n$($r.ra)"
}

# ---------------------------------------------------------------- chạy
$ten = @($script:CA.Keys)
if ($LapCa) { $ten = @($ten | Where-Object { $_ -eq $LapCa }) }
if (-not $ten) { Write-Host "khong co ca nao khop '$LapCa'" -ForegroundColor Red; exit 2 }

$qua = 0; $hong = @()
foreach ($t in $ten) {
    try { & $script:CA[$t]; $qua++ }
    catch { $hong += @{ ten = $t; vi = "$_" } }
}
foreach ($h in $hong) {
    Write-Host "  DO  $($h.ten)" -ForegroundColor Red
    Write-Host "      $($h.vi)" -ForegroundColor Red
}
Write-Host ""
Write-Host "don-nhanh: $qua/$($ten.Count) dat" -ForegroundColor $(if ($hong.Count) { 'Red' } else { 'Green' })
if ($hong.Count) { exit 1 }
exit 0
