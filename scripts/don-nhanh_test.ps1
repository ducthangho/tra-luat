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
        Tra ve thu muc de dat len PATH. $null nghia la KHONG dung gh gia.

        `-Ma`      : ma thoat cua `gh` gia (mac dinh 0).
        `-ThoNguyen`: in NGUYEN VAN chuoi nay thay vi JSON — de dung ca rac / rong.

        In cung mot thu trong suot MOT ca: do la mo hinh TRANG THAI cua mot danh sach PR
        bat bien trong mot luot chay, khong phai dien kich ban theo lan goi thu may.  #>
    # `$ThoNguyen` KHONG duoc khai [string]: PowerShell ep `[string]$null` thanh CHUOI RONG,
    # nen `$null -ne $ThoNguyen` LUON dung va moi ca se dung nhanh "in tho" — do duoc: ca ba
    # ca binh thuong (t1 t2 t3) dot ngot doi rc=13 vi `gh` gia in RONG o KHAP NOI. Dung
    # `$PSBoundParameters` de phan biet "khong truyen" voi "truyen chuoi rong".
    param([object[]]$PR, [int]$Ma = 0, [string]$ThoNguyen, [string]$CanhBaoStderr)
    $d = Join-Path ([System.IO.Path]::GetTempPath()) ("gh-" + [guid]::NewGuid().ToString('N').Substring(0, 10))
    New-Item -ItemType Directory -Path $d -Force | Out-Null
    # `ConvertTo-Json` tren mang RONG cho "[]" — dung thu that `gh` tra ve.
    $than = if ($PSBoundParameters.ContainsKey('ThoNguyen')) { $ThoNguyen }
            else { ConvertTo-Json -InputObject @($PR) -Compress -Depth 5 }
    $p = Join-Path $d 'gh'
    $dong = @("#!/bin/sh")
    # GHI LAI ARGV. Finding P2 cua cross-review luot 5: `gh` gia MU VOI ARGV — no in cung
    # mot JSON bat ke duoc hoi gi. No mo phong TRANG THAI (dung doctrine kho) nhung KHONG mo
    # phong HOP DONG TRUY VAN, nen MOI dot bien vao dong goi `gh` cua script song tron. Do
    # duoc, ca bon deu 21/21 xanh:
    #   --limit $TranPR -> --limit 200   (gh that tra dung 200; `200 -ge 1000` khong bao gio
    #                                     no => chot cham-tran thanh do trang tri)
    #   bo han --limit                   (mac dinh cua `gh pr list` la 30)
    #   --state open -> --state closed   (giu base cua PR DA DONG, bo roi PR dang mo)
    #   --json headRefName,baseRefName -> --json headRefName
    #        ^ TAI TAO DUNG LO GOC MA CA PR #150 SINH RA DE VA, bang MOT token.
    #
    # Phan biet voi no da khai `gh-phan-trang-that-chua-ai-do`: no ay noi ve CAU TRA LOI cua
    # gh that (khong do duoc vi proxy). Cai nay noi ve CAU HOI cua script — do duoc ngay.
    # Duong dan TUYET DOI, khong dung `dirname "$0"`: `gh` duoc tim qua PATH nen `$0` chi la
    # `gh`, `dirname` cho `.`, va argv.txt roi vao cwd (worktree) thay vi thu muc gh gia —
    # do duoc: chot doi argv bao "khong ghi duoc argv.txt" o lan chay dau.
    $dong += ("printf '%s\n' " + '"$@"' + " > '" + (Join-Path $d 'argv.txt') + "'")
    # stderr NGUYEN VAN — `gh` that hay in canh bao cap nhat phien ban ra day.
    if ($PSBoundParameters.ContainsKey('CanhBaoStderr')) {
        $dong += "printf '%s\n' '$($CanhBaoStderr -replace "'", "'\''")' >&2"
    }
    if ([string]::IsNullOrEmpty($than)) { $dong += ":" }
    else { $dong += @("cat <<'JSONEOF'", $than, "JSONEOF") }
    $dong += "exit $Ma"
    Set-Content -Path $p -Value $dong -Encoding utf8
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

ca 't10_gh_THOAT_KHAC_0_ma_van_in_JSON_HOP_LE_thi_TU_CHOI' {
    # FINDING CROSS-REVIEW LUOT 1 (#150). Ban dau KHONG kiem `$LASTEXITCODE` sau `gh`:
    # `ConvertFrom-Json` thanh cong nen `$doDuocPR` = $true va fail-close bi MO TOANG.
    # Reviewer do duoc: script tra rc=0 va XOA THAT, dang le rc=13 va remote khong doi.
    #
    # Day la duong lech nguy hiem nhat trong ho "rc=0 ma noi doi": JSON HOP LE lam moi
    # phep kiem NOI DUNG deu xanh, chi con ma thoat to cao.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia -PR @() -Ma 1          # JSON hop le (`[]`) NHUNG thoat 1
    $r = Chay-KichBan $k $gh @('-Xoa')
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13. `gh` thoat khac 0 ma van duoc tin. Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa du gh thoat khac 0: truoc=[$($truoc -join ', ')] sau=[$($sau -join ', ')]"
}

ca 't11_gh_rc0_nhung_in_RAC_thi_TU_CHOI' {
    # `ConvertFrom-Json` nem -> catch -> `$doDuocPR` giu $false. Ca nay khoa duong ay,
    # vi mot ban vá "bat loi roi coi nhu khong co PR nao" se bien loi thanh danh sach RONG.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia -PR @() -ThoNguyen 'khong phai JSON dau nhe'
    $r = Chay-KichBan $k $gh @('-Xoa')
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13. Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa du gh in rac"
}

ca 't12_gh_rc0_nhung_dau_ra_RONG_thi_TU_CHOI' {
    # `gh` chay dung PHAI in `[]` khi khong co PR nao. rc=0 kem dau ra RONG la bat thuong,
    # KHONG phai "khong co PR" — doc no thanh danh sach rong la dung lai lo vua va.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia -PR @() -ThoNguyen ''
    $r = Chay-KichBan $k $gh @('-Xoa')
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13. Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa du gh in RONG"
}

ca 't13_gh_rc0_JSON_hop_le_thi_VAN_xoa_binh_thuong' {
    # DOI CHUNG DUONG cho ba ca tren. Khong co no, mot ban vá "luon tu choi" se cho
    # t10 t11 t12 xanh het ma cong cu thanh vo dung.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $gh = Dung-Gh-Gia -PR @() -Ma 0
    $r = Chay-KichBan $k $gh @('-Xoa')
    $con = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc), doi 0. Ra:`n$($r.ra)"
    bang (-not ($con -contains 'ops/xong-viec')) "duong binh thuong khong xoa duoc gi — chot moi da chan oan"
}

ca 't14_gh_in_CANH_BAO_stderr_kem_JSON_hop_le_thi_VAN_chay' {
    # HOI QUY DO CROSS-REVIEW LUOT 2 BAT (#150). Ban truoc gop `2>&1` roi noi tat ca lai,
    # nen mot dong canh bao cua `gh` lam chuoi thanh "[]\nwarning-…" va `ConvertFrom-Json`
    # chet -> THAO TAC HOP LE BI TU CHOI. `gh` that in canh bao cap nhat phien ban rat
    # thuong xuyen, nen day khong phai ca hiem.
    #
    # Do CA HAI ve: base cua PR dang mo phai duoc GIU (tuc danh sach PR doc duoc THAT),
    # va nhanh rac phai bi XOA (tuc khong bi tu choi oan).
    $k = Dung-Kho
    Them-Nhanh $k 'nen/tichhop' $true
    Them-Nhanh $k 'ops/rac' $true
    $gh = Dung-Gh-Gia -PR @(@{ headRefName = 'con/x'; baseRefName = 'nen/tichhop' }) `
                      -CanhBaoStderr 'warning: a new release of gh is available'
    $r = Chay-KichBan $k $gh @('-Xoa')
    $con = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc), doi 0 — canh bao stderr lam thao tac hop le bi tu choi. Ra:`n$($r.ra)"
    bang ($con -contains 'nen/tichhop') "BASE bi xoa: danh sach PR khong doc duoc that. Con lai: $($con -join ', ')"
    bang (-not ($con -contains 'ops/rac')) "nhanh rac khong bi xoa. Con lai: $($con -join ', ')"
}

ca 't15_gh_in_CANH_BAO_stderr_NHUNG_thoat_khac_0_thi_VAN_TU_CHOI' {
    # Chot chong "vá qua tay theo chieu nguoc lai": tach luong stderr KHONG duoc lam mat
    # phep kiem ma thoat. Neu ai do sua thanh "bo qua stderr" roi lo luon rc thi ca nay do.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/xong-viec' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia -PR @() -Ma 1 -CanhBaoStderr 'warning: rate limit gan het'
    $r = Chay-KichBan $k $gh @('-Xoa')
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13. Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa du gh thoat khac 0"
}

ca 't16_gh_rc0_STDOUT_rong_nhung_STDERR_CO_noi_dung_thi_TU_CHOI' {
    # LO TRONG BO TEST, do cross-review luot 3 tim ra bang mot DOT BIEN SONG SOT (M9).
    #
    # `t12` kiem "rc=0 + rong" bang mot `gh` gia khong in GI CA — ke ca stderr. O ca do,
    # kiem NOI DUNG (`$vanBan`, da tach stderr) va kiem SO DONG THO (`$het.Count`) TRUNG
    # NHAU, nen khong ca nao phan biet duoc chung: doi phep kiem sang `$het.Count -eq 0`
    # van cho 15/15.
    #
    # Ca nay tach hai cach kiem ra: stdout RONG nhung stderr CO mot dong, tuc
    # `$het.Count = 1` (khong phai 0) trong khi `$vanBan` rong. Dot bien M9 se thay
    # `$het.Count -ne 0` => tuong la doc duoc => `$doDuocPR = $true` voi danh sach GIU RONG
    # => XOA CA BASE cua PR dang mo. Reviewer da chay end-to-end va thay dung the.
    #
    # Vi sao `ConvertFrom-Json ''` khong cuu duoc: no tra `$null` chu KHONG nem, ke ca voi
    # `$ErrorActionPreference='Stop'`; va `@($null).Count` trong PowerShell bang 1, khong
    # phai 0 — cung bay mang-don da ghi ngay trong ham nay.
    $k = Dung-Kho
    Them-Nhanh $k 'nen/tichhop' $true
    Them-Nhanh $k 'ops/rac' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia -PR @() -ThoNguyen '' -CanhBaoStderr 'warning: something on stderr'
    $r = Chay-KichBan $k $gh @('-Xoa')
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13 — stdout RONG ma van duoc tin. Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa: truoc=[$($truoc -join ', ')] sau=[$($sau -join ', ')]"
}

ca 't17_gh_tra_ve_DUNG_BANG_TRAN_thi_TU_CHOI' {
    # HÌNH DẠNG LỖI THỨ TƯ, do cross-review lượt kiến trúc nêu — và ho khai thang do la
    # SUY LUAN TU TAI LIEU chu khong phai phep do song (`gh` bi proxy container chan ca
    # REST lan GraphQL nen khong do that duoc).
    #
    # Ca nay do THU DUNG: khong do hanh vi cua `gh`, ma do HANH VI CUA SCRIPT khi dem tra
    # ve cham tran. Do la thu duy nhat script kiem soat duoc, va cung la thu that su quan
    # trong: `gh pr list --limit N` lay dung N phan tu va KHONG canh bao khi con nua, nen
    # "co dung N" va "BI CAT o N" cho ra CUNG mot ket qua. Khong phan biet duoc => TU CHOI.
    #
    # Dung `-TranPR 3` de khoi phai sinh 1000 PR gia. Bien co that su cham hay khong la
    # thuoc tinh cua PHEP SO SANH, khong phai cua con so.
    $k = Dung-Kho
    Them-Nhanh $k 'nen/tichhop' $true
    Them-Nhanh $k 'ops/rac' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia -PR @(
        @{ headRefName = 'a'; baseRefName = 'nen/tichhop' },
        @{ headRefName = 'b'; baseRefName = 'master' },
        @{ headRefName = 'c'; baseRefName = 'master' })
    $r = Chay-KichBan $k $gh @('-Xoa', '-TranPR', '3')
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13 — cham tran ma van tin la danh sach DU. Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa du danh sach co the DA BI CAT: truoc=[$($truoc -join ', ')] sau=[$($sau -join ', ')]"
}

ca 't18_gh_tra_ve_DUOI_TRAN_thi_VAN_chay' {
    # DOI CHUNG DUONG cho t17. Khong co no, mot ban "luon tu choi khi co PR" cho t17 xanh
    # ma cong cu thanh vo dung. Cung 3 PR nhu tren nhung tran = 4 => duoi tran.
    $k = Dung-Kho
    Them-Nhanh $k 'nen/tichhop' $true
    Them-Nhanh $k 'ops/rac' $true
    $gh = Dung-Gh-Gia -PR @(
        @{ headRefName = 'a'; baseRefName = 'nen/tichhop' },
        @{ headRefName = 'b'; baseRefName = 'master' },
        @{ headRefName = 'c'; baseRefName = 'master' })
    $r = Chay-KichBan $k $gh @('-Xoa', '-TranPR', '4')
    $con = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc), doi 0 — chot tran chan OAN duong binh thuong. Ra:`n$($r.ra)"
    bang ($con -contains 'nen/tichhop') "BASE bi xoa. Con lai: $($con -join ', ')"
    bang (-not ($con -contains 'ops/rac')) "nhanh rac khong bi xoa. Con lai: $($con -join ', ')"
}

function Nhieu-PR {
    <#  Sinh $So PR gia, base deu la `master` (khong lam ban danh sach GIU cua ca goi).

        HAI BAY, cross-review luot 5 do duoc — ca hai NGOAI mien goi hien tai (10/999/1000)
        nhung vao tay lan sau thi can:
          `Nhieu-PR 0` -> `1..0` chay NGUOC (pr/1, pr/0) = 2 phan tu, khong phai 0.
          `Nhieu-PR 1` -> PowerShell unwrap mang mot phan tu thanh hashtable TRAN, roi
                          `.Count` dem KEY = 2. Dung ho bay mang-don ma chinh tep nay ghi o
                          `t9`; hien duoc bien `[object[]]` cua `Dung-Gh-Gia` trung hoa.
        Guard duoi day dong bay thu nhat tai nguon; bay thu hai da co `@()` bao o `return`.  #>
    param([int]$So)
    if ($So -lt 1) { return @() }
    return @(1..$So | ForEach-Object { @{ headRefName = "pr/$_"; baseRefName = 'master' } })
}

ca 't19_dem_VUOT_TRAN_thi_TU_CHOI_va_so_sanh_phai_la_SO_HOC' {
    # F1 cua cross-review luot 4 (P2). Cap t17/t18 chi ghim bien TU PHIA DUOI, nen HAI dot
    # bien lam chot FAIL-OPEN van song sot 18/18:
    #   M12  `-ge` -> `-eq` : chi chan khi dem BANG DUNG tran. Do duoc: `-TranPR 0` voi 1 PR
    #        mo => rc=0 va XOA THAT, trong khi HEAD tu choi.
    #   M16  so sanh CHUOI  : `"10" -ge "9"` la $false => vuot tran ma van cho qua.
    #
    # Ca nay giet CA HAI trong MOT: 10 PR, tran 9. `10 -ge 9` dung ve SO HOC nhung sai ve
    # CHUOI, va 10 khac 9 nen `-eq` cung khong bat.
    #
    # LOI KHAI CU O DAY SAI, cross-review luot 5 bat duoc va DO phan chung: ban dau viet
    # "10/9 la CAP SO nho nhat phan biet so hoc voi chuoi". Sai — do tren pwsh 7.4.6:
    #   (10,9) so hoc True / chuoi False -> phan biet duoc
    #   (10,2) so hoc True / chuoi False -> CUNG phan biet duoc
    #   (9,2)  so hoc True / chuoi True  -> KHONG phan biet duoc
    # Tuc moi cap (10,2)..(10,9) deu phan biet duoc, va thu NHO NHAT that su la DEM = 10
    # (buoc HAI chu so so voi MOT); moi cap mot-chu-so deu mu. Chon tran 9 la de SAT BIEN,
    # khong phai vi 9 co gi dac biet.
    # Ghi lai vi kho nay DO loi khai trong chu thich — chinh nguoi va vua do loi khai t21.
    $k = Dung-Kho
    Them-Nhanh $k 'nen/tichhop' $true
    Them-Nhanh $k 'ops/rac' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia -PR (Nhieu-PR 10)
    $r = Chay-KichBan $k $gh @('-Xoa', '-TranPR', '9')
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13 — dem 10 VUOT tran 9 ma van duoc tin. Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa du danh sach VUOT tran: truoc=[$($truoc -join ', ')] sau=[$($sau -join ', ')]"
}

ca 't20_MAC_DINH_phai_cho_qua_o_999_PR' {
    # F2 cua cross-review luot 4 (P3). MOI ca da-PR deu truyen `-TranPR` tuong minh, nen nua
    # "nang tran 200 -> 1000" cua ban va KHONG co bang chung duong nao: dot bien ha mac dinh
    # ve 200 (M13) hoac ve 3 (M13b) deu song sot 18/18.
    #
    # Ghim bang HANH VI, khong bang chuoi nguon — kho nay da ghi "chot chi tim chuoi nguon la
    # chot rat yeu". Cap t20/t21 ghim mac dinh DUNG tai 1000: 999 phai QUA, 1000 phai DUNG.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/rac' $true
    $gh = Dung-Gh-Gia -PR (Nhieu-PR 999)
    $r = Chay-KichBan $k $gh @('-Xoa')          # KHONG truyen -TranPR: dung MAC DINH
    $con = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 0) "rc=$($r.rc), doi 0 — mac dinh co the da bi ha xuong duoi 1000. Ra:`n$($r.ra)"
    bang (-not ($con -contains 'ops/rac')) "nhanh rac khong bi xoa. Con lai: $($con -join ', ')"
    # DOI DUNG SO PR DOC DUOC. No khai bao cua luot 5: neu helper tra `@()` thi ca nay VAN
    # XANH (0 < 1000 => di tiep, rac bi xoa, rc=0) — tuc "doc duoc THAT" dang la thuoc tinh
    # cua CAP t20/t21 chu khong cua rieng ca nay, va t21 thanh diem hong DON cua ca phep
    # ghim. Chot duoi day tra tinh doc lap cho t20.
    bang ($r.ra -match 'cua\s+999\s+PR dang mo') "khong thay '999 PR dang mo' trong dau ra — danh sach co the doc RONG chu khong phai doc duoc 999. Ra:`n$($r.ra)"
}

ca 't21_MAC_DINH_phai_TU_CHOI_o_1000_PR' {
    # Ve tren cua cap ghim mac dinh. Cung F2. Neu ai nang mac dinh len 2000 thi ca nay DO —
    # co y: doi tran la doi HANH VI CONG BO, phai co nguoi sua ca test va noi ly do.
    $k = Dung-Kho
    Them-Nhanh $k 'ops/rac' $true
    $truoc = Nhanh-Tren-Remote $k
    $gh = Dung-Gh-Gia -PR (Nhieu-PR 1000)
    $r = Chay-KichBan $k $gh @('-Xoa')          # KHONG truyen -TranPR
    $sau = Nhanh-Tren-Remote $k
    bang ($r.rc -eq 13) "rc=$($r.rc), doi 13 — cham mac dinh 1000 ma van tin la danh sach DU. Ra:`n$($r.ra)"
    bang (($truoc -join ',') -eq ($sau -join ',')) "CO nhanh bi xoa du cham tran mac dinh"

    # CHOT ARGV — F1 luot 5, va P1 luot 6 da va lai CHINH cho nay. Ca nay la ca DUY NHAT di
    # du bo ba tham so voi GIA TRI MAC DINH, tuc "loi hoi cuoi cung truoc khi tin".
    #
    # VI SAO SO NGUYEN CAU chu khong `-contains` tung token (P1 cross-review luot 6):
    # ban truoc duyet tung token bang `-contains`, tuc do su CO MAT cua token chu KHONG do
    # CAU HOI duoc gui di. No mu voi token THUA, va bon dot bien song tron 21/21:
    #   them `--limit 30` SAU `--limit $TranPR`  -> gh that: co SAU thang => limit = 30
    #        ^ TAI SINH DUNG LO GOC MA CA PR #150 SINH RA DE VA, bang MOT token thua.
    #   them `--state closed` cuoi dong          -> giu base PR DA DONG
    #   them `--repo x/y`                        -> hop dong doi, test khong thay
    #   `pr list` -> `issue list`                -> `pr`/`list` khong nam trong danh sach doi
    # Danh-sach-cam-theo-token thua tu trong THIET KE: no phai doan truoc moi cach viet.
    # So NGUYEN CAU thi chi phai biet DUNG mot chuoi — va no ghim luon `pr list`, cam token
    # thua, cam lap co, cam dao thu tu, tat ca bang mot phep.
    #
    # PHAI `-ceq` CHU KHONG `-eq`: `-eq` tren chuoi cua PowerShell MU HOA-THUONG
    # (do duoc tren pwsh 7.4.6: '--STATE OPEN' -eq '--state open' => True; -ceq => False).
    # Phan chung cho chinh dieu do, da chay: dot bien `--state`->`--STATE` o dong 184
    #   giu `-ceq` => 20/21, do dung ca nay   |   ha xuong `-eq` => 21/21, SONG.
    # Tuc `-ceq` la thu dang giet no, khong phai thu khac.
    #
    # Phan chung cho ca chot: go han hai dong duoi + dot bien `--limit 30` sau
    #   => 21/21 (dot bien SONG LAI). Khong co phep thu ay thi khong biet ca nay dang
    #   do ARGV hay do thu khac.
    #
    # Chuoi ky vong duoi day DO duoc, khong doan: dump `$tok -join ' '` o HEAD ra 8 token.
    # `printf '%s\n' "$@"` cua gh gia ghi MOI token mot dong nen join lai la nguyen cau.
    # Danh doi da biet: neu mai kia mot token CHINH DANG chua khoang trang thi phep join
    # nhap nhang va ca nay phai doi cach ghi. No hong theo huong DO (an toan), khong phai
    # theo huong xanh — nen day la no, khong phai lo dang chay mau.
    #
    # CO Y: them mot co chinh dang (vd `--repo`) SE lam ca nay DO. Doi cau hoi gui `gh` la
    # doi HOP DONG, phai co nguoi sua test va noi ly do — do khong phai do oan.
    # (Loi khai nay tung SAI o ban truoc — luot 6 do ra `--repo` van xanh. Nay no DUNG,
    # va da do: dot bien `--repo x/y` => 20/21, do dung ca nay.)
    # `Dung-Gh-Gia` tra ve THU MUC (de dat len PATH), khong phai duong dan tep `gh`.
    $argv = Join-Path $gh 'argv.txt'
    bang (Test-Path $argv) "gh gia khong ghi duoc argv.txt — chot nay dang khong do gi"
    $tok = @(Get-Content -Path $argv)
    $mong = 'pr list --state open --limit 1000 --json headRefName,baseRefName'
    bang (($tok -join ' ') -ceq $mong) `
        "cau hoi gui gh KHAC hop dong.`n  mong : [$mong]`n  thuc : [$($tok -join ' ')]"
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
