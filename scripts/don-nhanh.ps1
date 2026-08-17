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
    2. Danh sách GIỮ theo mẫu (`master`, `luu-tru/**`, HEAD *và* BASE của PR đang mở…).
    3. Mặc định DRY RUN. Phải nêu `-Xoa` mới thật sự xoá.
    4. Đối chiếu SAU khi xoá: hỏi lại remote và báo nhánh nào còn sót.

  LỖ ĐÃ VÁ 17-08-2026 — BASE, KHÔNG PHẢI HEAD
  Bản đầu chỉ đọc `headRefName`. Nhưng xoá một nhánh đang là BASE của PR đang mở thì
  GitHub ĐÓNG LUÔN các PR nhắm vào nó — mất cả review lẫn thảo luận, và không có
  thao tác "hoàn tác nhánh" nào dựng lại được trạng thái mở ấy.

  Lớp 1 KHÔNG che được ca này, và lý do đáng đọc: lớp 1 loại nhánh CHƯA merge, mà
  một nhánh tích hợp (`mission/**/integration`) hoàn toàn có thể ĐÃ vào master trong
  khi vẫn còn PR mở nhắm vào nó. Lúc ấy lớp 1 nói "xoá được" và nó đúng về mặt
  commit — không mất commit nào — nhưng sai về mặt HẬU QUẢ.

  Đo lúc vá: kho có 4 PR mở nhắm `mission/76/integration`; nhánh ấy CHƯA vào master
  nên lớp 1 tình cờ giữ lại. Tức lỗ này chưa cắn, và "chưa cắn" không phải "không có"
  — nó chỉ đang được che bởi một điều kiện có thể đổi bất cứ lúc nào.

  VÀ VÌ SAO LỚP NÀY PHẢI FAIL-CLOSE
  Với HEAD, thiếu `gh` chỉ làm mất một lớp thừa: PR mở thì head chưa merge, lớp 1 che.
  Với BASE thì KHÔNG có lớp nào khác che. Nên khi `-Xoa` mà không đọc được danh sách
  PR, script TỪ CHỐI XOÁ (thoát 13) thay vì xoá rồi mong không sao — "không đo được"
  khác "không có", đúng doctrine `None ≠ False` của kho. Muốn bỏ qua thì phải nêu
  tường minh `-BoQuaLopPR`, tức có người chịu trách nhiệm cho quyết định ấy.

.PARAMETER Xoa
  Thật sự xoá. Không nêu thì chỉ in ra sẽ xoá gì.

.PARAMETER GiuThem
  Tên nhánh giữ thêm, ngoài danh sách mặc định. Nhận cả mẫu glob.

.PARAMETER Remote
  Tên remote. Mặc định `origin`.

.PARAMETER CoLo
  Số nhánh mỗi lượt `git push --delete`. Mặc định 25.

.PARAMETER BoQuaLopPR
  Xoá kể cả khi KHÔNG đọc được danh sách PR đang mở. Chỉ dùng khi bạn đã tự kiểm
  rằng không nhánh nào trong danh sách xoá là base của một PR còn mở. Không nêu cờ
  này thì `-Xoa` sẽ TỪ CHỐI (thoát 13) trong tình huống ấy.

.EXAMPLE
  .\scripts\don-nhanh.cmd
  # ĐƯỜNG NÊN DÙNG trên Windows — chỉ xem sẽ xoá gì

.EXAMPLE
  .\scripts\don-nhanh.cmd -Xoa
  # xoá thật

.NOTES
  GỌI TRÊN WINDOWS: dùng `don-nhanh.cmd`, đừng gọi thẳng `.ps1`.

  ĐÃ TRẢ GIÁ 16-08-2026. Hướng dẫn ban đầu ghi `.\scripts\don-nhanh.ps1`, và máy
  người dùng ở chế độ `AllSigned` nên chặn ngay:

      File ...\don-nhanh.ps1 cannot be loaded. The file is not digitally signed.

  Người viết kiểm script trên `pwsh` Linux, nơi ExecutionPolicy mặc định là
  `Unrestricted` — đúng lớp lỗi "chạy được ở đây khác chạy được ở đó" mà kho này
  đã ghi nhiều lần. Và khuôn `.cmd` bọc `.ps1` ĐÃ CÓ SẴN ở `deploy-package.cmd`
  lẫn `tl-setup.cmd`; bỏ qua một lời giải đã viết sẵn thì đắt hơn là không biết.

  Muốn gọi thẳng `.ps1` (CI, hoặc máy đã nới chính sách):

      pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\don-nhanh.ps1

  `-ExecutionPolicy Bypass` chỉ áp cho ĐÚNG tiến trình ấy, không đổi cài đặt máy.
#>

# KHÔNG đặt tên tham số là `$Args`: đó là BIẾN TỰ ĐỘNG của PowerShell trong hàm,
# nên `@Args` nở ra mảng RỖNG thay vì đối số truyền vào — đã trả giá ở r244, khi một
# gate báo `rc=0` với đầu ra rỗng mà chẳng chạy gì.
[CmdletBinding()]
param(
    [switch]$Xoa,
    [string[]]$GiuThem = @(),
    [string]$Remote = 'origin',
    [int]$CoLo = 25,
    [switch]$BoQuaLopPR
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
# HEAD *VA* BASE cua PR dang MO.
#
# HEAD: ve nguyen tac lop 1 da che (PR mo thi head chua merge), nhung mot PR VAN co the
# mo trong khi head da vao master bang duong khac — luc do lop 1 khong che nua.
#
# BASE: lop 1 KHONG che, va day moi la ca nguy hiem. Xoa mot nhanh dang la base cua PR
# dang mo thi GitHub DONG LUON cac PR nham vao no. Mot nhanh tich hop hoan toan co the
# DA vao master trong khi van con PR mo nham vao no — luc ay lop 1 noi "xoa duoc" va no
# dung ve COMMIT (khong mat commit nao) nhung sai ve HAU QUA.
#
# `$doDuocPR` la TRANG THAI THU BA: khong phai "co PR" / "khong co PR" ma la "KHONG DO
# DUOC". No phai chan viec xoa, khong duoc lang le thanh danh sach rong.
$prMo = @()
$doDuocPR = $false
$lyDoKhongDo = ''
if (Get-Command gh -ErrorAction SilentlyContinue) {
    try {
        # BAT MA THOAT NGAY SAU LOI GOI, TRUOC MOI PIPELINE/PARSE.
        #
        # Finding cross-review luot 1 (#150), da chay: `gh` THOAT KHAC 0 nhung van in JSON
        # HOP LE thi `ConvertFrom-Json` thanh cong, `$doDuocPR` thanh $true, va fail-close bi
        # MO TOANG — script tra rc=0 roi xoa that. Do duoc: gh in `[]` + exit 1 -> nhanh da
        # merge bi xoa, trong khi phai la rc=13 va remote khong doi.
        #
        # Chinh ham `Chay-Git` phia tren da dan dung dieu nay ("dung `$LASTEXITCODE` sau mot
        # pipeline") va loi goi nay vi pham no. Mot loi dan chi bao ve doan ma no duoc VIET
        # RA, khong bao ve doan ke ben.
        $het = & gh pr list --state open --limit 200 --json headRefName,baseRefName 2>&1
        $ghRc = $LASTEXITCODE
        # TACH HAI LUONG THEO KIEU, khong nem chung vao mot chuoi.
        #
        # Hoi quy cua cross-review luot 2 (#150), da CHAY: ban truoc gop `2>&1` roi noi tat
        # ca lai, nen mot dong CANH BAO cua `gh` tren stderr (vi du "a new release of gh is
        # available") lam chuoi thanh "[]\nwarning-…" va `ConvertFrom-Json` chet — tuc mot
        # thao tac HOP LE bi tu choi. Va mot lo roi mo lo khac trong cung ham; day la hinh
        # dang loi CLAUDE.md da ghi o writer "nguyen tu".
        #
        # PowerShell gan nhan ErrorRecord cho dong stderr cua lenh native, nen loc theo KIEU
        # tach sach — DA DO tren pwsh 7.4.6: gh in canh bao + `[]`, rc=0 => 2 dong (1 loi,
        # 1 stdout), stdout noi lai = "[]", parse OK. Giu van ban loi de con chan doan.
        $loiGh = @($het | Where-Object { $_ -is [System.Management.Automation.ErrorRecord] })
        $raGh  = @($het | Where-Object { -not ($_ -is [System.Management.Automation.ErrorRecord]) })
        if ($ghRc -ne 0) { throw "gh thoat rc=$ghRc : $(($loiGh + $raGh) -join ' ')" }
        # RONG cung la KHONG DO DUOC. `gh` chay dung phai in `[]` khi khong co PR nao; rc=0
        # kem dau ra rong la bat thuong, khong phai "khong co PR". Doctrine `rc=0 ma stdout
        # RONG` cua kho: chi kiem rc la lot.
        $vanBan = ($raGh -join "`n").Trim()
        if ([string]::IsNullOrWhiteSpace($vanBan)) { throw 'gh rc=0 nhung STDOUT rong' }
        $js = ConvertFrom-Json $vanBan
        # `ConvertFrom-Json` tra $null khi mang rong, va mot phan tu don KHONG phai mang.
        # Ep [object[]] de hai truong hop bien do khong lam `.headRefName` no ra sai.
        $js = @($js)
        $prMo = @($js | ForEach-Object { $_.headRefName; $_.baseRefName }) |
                Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
                Sort-Object -Unique
        $doDuocPR = $true
        Ghi "giu them $($prMo.Count) ref cua $($js.Count) PR dang mo (head VA base, doc bang gh)"
    } catch {
        $lyDoKhongDo = "gh co nhung khong doc duoc PR: $($_.Exception.Message)"
        Ghi $lyDoKhongDo 'Yellow'
    }
} else {
    $lyDoKhongDo = 'KHONG co `gh` tren PATH'
    Ghi 'KHONG co `gh`: khong doc duoc head/base cua PR dang mo.' 'Yellow'
    Ghi '  HEAD: lop 1 (chi xoa nhanh DA MERGE) van che duoc gan het.' 'Yellow'
    Ghi '  BASE: KHONG lop nao che. Xoa nham base cua PR dang mo se DONG cac PR do.' 'Red'
    Ghi '  Cach chua: cai gh, hoac neu tay -GiuThem <base-a>,<base-b>' 'Yellow'
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

if (-not $doDuocPR) {
    Ghi ''
    Ghi 'CANH BAO: danh sach tren CHUA loai base cua PR dang mo.' 'Red'
    Ghi "  ly do: $lyDoKhongDo" 'Red'
}

if (-not $Xoa) {
    Ghi ''
    Ghi 'DRY RUN — chua xoa gi. Them -Xoa de xoa that.' 'Cyan'
    exit 0
}

# FAIL-CLOSE, dat TRUOC moi lenh xoa.
#
# Vi sao khong "canh bao roi chay tiep": CLAUDE.md ghi thang — "Tu choi ma van de duong
# nguy hiem chay tiep la FAIL-OPEN, khong phai than trong". Xoa mot base la thao tac
# KHONG hoan tac duoc ve mat PR: GitHub dong cac PR nham vao no, va tao lai nhanh khong
# mo lai chung.
#
# Cua thoat phai TUONG MINH (`-BoQuaLopPR`) chu khong phai mac dinh, de quyet dinh ay co
# nguoi chiu trach nhiem thay vi tro thanh hanh vi im lang cua cong cu.
if (-not $doDuocPR -and -not $BoQuaLopPR) {
    Ghi ''
    Ghi 'TU CHOI XOA — khong do duoc danh sach PR dang mo.' 'Red'
    Ghi "  $lyDoKhongDo" 'Red'
    Ghi '  Xoa nham mot nhanh dang la BASE cua PR dang mo se DONG cac PR do,' 'Red'
    Ghi '  va tao lai nhanh KHONG mo lai chung.' 'Red'
    Ghi ''
    Ghi '  Chon mot:' 'Yellow'
    Ghi '    - cai `gh` roi chay lai (duong nen dung)' 'Yellow'
    Ghi '    - neu tay:  -GiuThem base-a,base-b' 'Yellow'
    Ghi '    - da tu kiem va chap nhan:  -BoQuaLopPR' 'Yellow'
    exit 13
}
if (-not $doDuocPR -and $BoQuaLopPR) {
    Ghi ''
    Ghi 'BO QUA LOP PR theo yeu cau tuong minh (-BoQuaLopPR).' 'Yellow'
    Ghi 'Neu mot trong cac nhanh tren la base cua PR dang mo, PR do se BI DONG.' 'Yellow'
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
