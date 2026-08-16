<#
.SYNOPSIS
  Dọn nhánh remote đã merge vào master. MẶC ĐỊNH CHỈ IN, không xoá gì.

.DESCRIPTION
  VÌ SAO KHÔNG NHẬN MỘT DANH SÁCH CỨNG
  Bản đầu của việc này là một danh sách 19 tên nhánh chép tay. Đo lại sau vài giờ:
  cả 19 đã KHÔNG CÒN — một phiên khác đã chuyển chúng sang `luu-tru/wp55-r4/**`.
  Chạy danh sách ấy sẽ báo "Everything up-to-date" 19 lần và người chạy tưởng đã dọn.
  Nên script này TỰ ĐO mỗi lần chạy, không nhận tên nhánh từ ai.

  CHỐT AN TOÀN — bốn lớp, mỗi lớp đủ một mình:
    1. Chỉ xoá nhánh mà `git merge-base --is-ancestor <nhánh> origin/master` trả 0,
       tức mọi commit của nó ĐÃ nằm trong master. Xoá một nhánh như vậy không mất
       commit nào; muốn dựng lại chỉ cần trỏ tên vào SHA cũ.
    2. Danh sách GIỮ theo mẫu (`master`, `luu-tru/**`, HEAD của PR đang mở…).
    3. Mặc định DRY RUN. Phải nêu `-Xoa` mới thật sự xoá.
    4. Đối chiếu SAU khi xoá: hỏi lại remote và báo nhánh nào còn sót.

.PARAMETER Xoa
  Thật sự xoá. Không nêu thì chỉ in ra sẽ xoá gì.

.PARAMETER GiuThem
  Tên nhánh giữ thêm, ngoài danh sách mặc định. Nhận cả mẫu glob.

.PARAMETER Remote
  Tên remote. Mặc định `origin`.

.PARAMETER CoLo
  Số nhánh mỗi lượt `git push --delete`. Mặc định 25.

.EXAMPLE
  .\scripts\don-nhanh.ps1
  # chỉ xem sẽ xoá gì

.EXAMPLE
  .\scripts\don-nhanh.ps1 -Xoa
  # xoá thật
#>

# KHÔNG đặt tên tham số là `$Args`: đó là BIẾN TỰ ĐỘNG của PowerShell trong hàm,
# nên `@Args` nở ra mảng RỖNG thay vì đối số truyền vào — đã trả giá ở r244, khi một
# gate báo `rc=0` với đầu ra rỗng mà chẳng chạy gì.
[CmdletBinding()]
param(
    [switch]$Xoa,
    [string[]]$GiuThem = @(),
    [string]$Remote = 'origin',
    [int]$CoLo = 25
)

$ErrorActionPreference = 'Stop'

# Console máy Việt là cp1258: in đường dẫn/tên nhánh có dấu sẽ ném lỗi mã hoá và
# giết cả lượt chạy TRƯỚC khi logic kịp sai. Ép UTF-8 trước khi in bất cứ thứ gì.
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
} catch { }

function Ghi([string]$m, [string]$mau = 'Gray') { Write-Host $m -ForegroundColor $mau }

function Chay-Git {
    <#  Trả (rc, dòng đầu ra). KHÔNG dùng `$LASTEXITCODE` sau một pipeline —
        pipeline đổi nó theo lệnh CUỐI. Bắt ngay sau lời gọi.  #>
    param([Parameter(Mandatory)][string[]]$Doi)
    $out = & git @Doi 2>&1
    $rc = $LASTEXITCODE
    # `$out` là $null khi không có dòng nào; ép [string[]] để phía gọi khỏi phải
    # phân biệt null với mảng rỗng (cùng bẫy với `Get-Content -Raw` trên tệp rỗng).
    return @{ rc = $rc; dong = [string[]]($out | ForEach-Object { "$_" }) }
}

# ---------------------------------------------------------------- chuẩn bị
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Ghi 'THIEU git tren PATH.' 'Red'; exit 12
}
$r = Chay-Git @('rev-parse', '--is-inside-work-tree')
if ($r.rc -ne 0) { Ghi 'Khong phai kho git. Chay script nay TRONG kho.' 'Red'; exit 3 }

Ghi "== dong bo ref tu $Remote ==" 'Cyan'
$r = Chay-Git @('fetch', '--prune', '--quiet', $Remote)
if ($r.rc -ne 0) { Ghi "git fetch that bai: $($r.dong -join ' ')" 'Red'; exit 3 }

$r = Chay-Git @('rev-parse', "$Remote/master")
if ($r.rc -ne 0 -or -not $r.dong) { Ghi "khong doc duoc $Remote/master" 'Red'; exit 3 }
$masterSha = $r.dong[0]
Ghi "master = $masterSha"

# ---------------------------------------------------------------- danh sách GIỮ
#
# `luu-tru/**` là KHO LƯU TRỮ, không phải rác: một phiên khác đã chuyển hồ sơ wp55 r4
# vào đó thay vì xoá. Nhánh lưu trữ có thể CHƯA merge (nên lớp 1 đã che), nhưng nêu
# tường minh vẫn hơn — để người đọc thấy nó là quyết định, không phải may mắn.
$GiuMau = @(
    'master',
    'luu-tru/*',
    'HEAD'
) + $GiuThem

# HEAD cua PR dang MO. Ve nguyen tac lop 1 da che (PR mo thi head chua merge), nhung
# mot PR VAN co the mo trong khi head da vao master bang duong khac — luc do lop 1
# khong che nua. Hai lop doc lap, va lop nay chi chay duoc khi co `gh`.
$prMo = @()
if (Get-Command gh -ErrorAction SilentlyContinue) {
    try {
        $prMo = (& gh pr list --state open --limit 200 --json headRefName |
                 ConvertFrom-Json).headRefName
        Ghi "giu them $($prMo.Count) head cua PR dang mo (doc bang gh)"
    } catch { Ghi 'gh co nhung khong doc duoc PR — bo qua lop nay' 'Yellow' }
} else {
    Ghi 'KHONG co `gh`: khong doc duoc head cua PR dang mo.' 'Yellow'
    Ghi '  Lop 1 (chi xoa nhanh DA MERGE) van che duoc gan het;' 'Yellow'
    Ghi '  neu muon chac, them tay: -GiuThem nhanh-a,nhanh-b' 'Yellow'
}
$GiuMau += $prMo

function Duoc-Giu([string]$ten) {
    foreach ($m in $GiuMau) {
        if ([string]::IsNullOrWhiteSpace($m)) { continue }
        if ($ten -like $m) { return $true }
    }
    return $false
}

# ---------------------------------------------------------------- phân loại
Ghi '== do tung nhanh ==' 'Cyan'
$r = Chay-Git @('ls-remote', '--heads', $Remote)
if ($r.rc -ne 0) { Ghi 'git ls-remote that bai' 'Red'; exit 3 }

$tenNhanh = $r.dong |
    ForEach-Object { ($_ -split "`t")[-1] } |
    Where-Object { $_ -like 'refs/heads/*' } |
    ForEach-Object { $_ -replace '^refs/heads/', '' } |
    Sort-Object

if (-not $tenNhanh) { Ghi 'khong thay nhanh nao — nghi mau khop hong' 'Red'; exit 3 }
Ghi "tong: $($tenNhanh.Count) nhanh"

$seXoa = @(); $giuLai = @(); $chuaMerge = @()
foreach ($b in $tenNhanh) {
    if (Duoc-Giu $b) { $giuLai += $b; continue }
    # `--is-ancestor` tra 0 khi MOI commit cua nhanh da nam trong master.
    $k = Chay-Git @('merge-base', '--is-ancestor', "$Remote/$b", "$Remote/master")
    if ($k.rc -eq 0) { $seXoa += $b } else { $chuaMerge += $b }
}

Ghi ''
Ghi "DA MERGE, se xoa      : $($seXoa.Count)" 'Green'
Ghi "CHUA merge, giu       : $($chuaMerge.Count)" 'Yellow'
Ghi "trong danh sach giu   : $($giuLai.Count)" 'Yellow'
Ghi ''

if ($seXoa.Count -eq 0) { Ghi 'Khong co nhanh nao de xoa.' 'Green'; exit 0 }

Ghi '--- se xoa ---' 'Green'
$seXoa | ForEach-Object { Ghi "  $_" }

if (-not $Xoa) {
    Ghi ''
    Ghi 'DRY RUN — chua xoa gi. Them -Xoa de xoa that.' 'Cyan'
    exit 0
}

# ---------------------------------------------------------------- xoá
Ghi ''
Ghi "== XOA THAT: $($seXoa.Count) nhanh, moi lot $CoLo ==" 'Red'
$hong = @()
for ($i = 0; $i -lt $seXoa.Count; $i += $CoLo) {
    $lo = $seXoa[$i..([Math]::Min($i + $CoLo - 1, $seXoa.Count - 1))]
    $doi = @('push', '--delete', $Remote) + $lo
    $k = Chay-Git $doi
    if ($k.rc -eq 0) {
        Ghi "  lo $([Math]::Floor($i / $CoLo) + 1): xoa $($lo.Count) nhanh — OK" 'Green'
    } else {
        # Ca lo hong thi thu TUNG CAI: mot nhanh hong khong duoc keo ca lo chet theo,
        # va ta can biet DUNG cai nao hong chu khong phai "lo nay hong".
        Ghi "  lo $([Math]::Floor($i / $CoLo) + 1) hong, thu tung nhanh..." 'Yellow'
        foreach ($b in $lo) {
            $k2 = Chay-Git @('push', '--delete', $Remote, $b)
            if ($k2.rc -ne 0) { $hong += $b; Ghi "    HONG $b : $($k2.dong -join ' ')" 'Red' }
        }
    }
}

# ---------------------------------------------------------------- đối chiếu SAU
#
# KHONG tin thong bao "da xoa". `git push --delete` co the tra ve "Everything
# up-to-date" ma rc=1 khi proxy chan, hoac im lang khi nhanh von khong ton tai.
# Hoi lai remote la thu duy nhat phan biet duoc "da xoa" voi "tuong da xoa".
Ghi ''
Ghi '== doi chieu SAU khi xoa (hoi lai remote) ==' 'Cyan'
$r = Chay-Git @('ls-remote', '--heads', $Remote)
$conLai = @()
if ($r.rc -eq 0) {
    $sau = $r.dong |
        ForEach-Object { ($_ -split "`t")[-1] } |
        Where-Object { $_ -like 'refs/heads/*' } |
        ForEach-Object { $_ -replace '^refs/heads/', '' }
    $conLai = $seXoa | Where-Object { $sau -contains $_ }
} else {
    Ghi 'khong doi chieu duoc — ls-remote that bai' 'Red'
}

if ($conLai.Count -eq 0) {
    Ghi "DA XOA HET: $($seXoa.Count) nhanh, con lai 0" 'Green'
    Chay-Git @('fetch', '--prune', '--quiet', $Remote) | Out-Null
    exit 0
}

Ghi "CON SOT $($conLai.Count) nhanh:" 'Red'
$conLai | ForEach-Object { Ghi "  $_" 'Red' }
Ghi ''
Ghi 'Neu loi la 403 / "not in this session authorized repository set" thi do la' 'Yellow'
Ghi 'proxy chan XOA REF (push tao/cap nhat van chay). Chay script nay tu may that.' 'Yellow'
exit 1
