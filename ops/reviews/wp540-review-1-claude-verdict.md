---
verdict: approve
reviewed_sha: 7c7ad450258c640bc207c17f7f5a60077081419c
so_p1: 0
so_p2: 0
so_p3: 1
so_the_hien: 1
---

# Cross-review WP540 — claude review codex (`cross_approved`)

TỆP NÀY GHI TĂNG DẦN, tạo TRƯỚC phép đo đầu tiên.

## XUNG ĐỘT LỢI ÍCH — khai TRƯỚC

Reviewer là **phiên claude đang điều phối**, không phải tiến trình claude riêng
(`launcher.py doctor` ⇒ `rc=12`, `CHUA_XAC_THUC claude`; `claude --print` ⇒ `rc=1`,
`duration_api_ms: 0` ⇒ CLI không gọi API lần nào).

Diff WP540 do **codex** viết. Reviewer là **claude**. Khác provider thật.
Phiên này soạn `spec r2` và ghi hộ `lease g2` — hai thứ đổi đúng `Reviewer` và
`Assurance target`, KHÔNG đổi `A1`–`A7`. Phiên này cũng hướng dẫn chủ kho ĐẨY commit
`7c7ad450`, nhưng KHÔNG viết một byte nào của bản vá.

## MỎ NEO — vì sao verdict neo `7c7ad450` chứ không phải số trong lease

`lease g2` khai `reviewed_sha_required: 9963a03a` kèm `reviewed_sha_required_note`
nguyên văn: *"day la mo neo DUOI, va verdict cuoi PHAI neo dung SHA ung vien that khi
no ton tai"*. Ứng viên nay tồn tại ⇒ verdict neo `7c7ad450`. **Không cần revision mới**:
chính lease đã dự liệu, đây không phải đổi acceptance.

## HIỆN VẬT LÊN REF ĐÚNG BẢN CODEX ĐÃ ĐO — năm định danh, đo trên ref

| | codex khai (comment 5675653887) | đo trên `origin/codex/wp540-r1-g1` |
|---|---|---|
| commit | `7c7ad450258c640bc207c17f7f5a60077081419c` | **khớp** |
| tree | `3c0e4ad1333473ac8901f482e5b801a2371d8a24` | **khớp** |
| blob sản phẩm | `df4e6da9dc9179dc2c3243c21bf1a208c42533c3` | **khớp** |
| `product_sha256` | `ce2156c0f85cd…d94f892` | **khớp** |
| parent | `9963a03a88a6936eadb208e7c602d0ae63fefc96` | **khớp** |

Đẩy là **fast-forward** `9963a03..7c7ad45`, không rewrite. Nên lượt review này chấm
ĐÚNG hiện vật đã qua phép đo của executor, không phải một bản dựng lại.

## PHẠM VI ĐO

`immutable_acceptance_baseline` = `19de5669`. Delta: **3 tệp**.
Sản phẩm: `ops/nhanh_don_duoc_test.py` **+17 −14**. Phối hợp: lease +76, spec r1 +33.

## SANDBOX

mirror bare (63 ref, `is-shallow=false`, `core.abbrev 7`) + cây detached tại `7c7ad450`,
`status --porcelain` rỗng. Tập ref hai nguồn trên kho nguồn: `comm -23` **rỗng** ⇒ không mù.

## CỔNG — chạy trên chính cây ứng viên, `rc` đọc TRỰC TIẾP

| cổng | rc | bằng chứng DƯƠNG |
|---|---:|---|
| `doctrine-scan` | **0** | — |
| `adr-song` | **0** | — |
| `doc-claims-check --strict` | **0** | `core.abbrev=7` |
| `git diff --check` | **0** | — |
| `release-verify --strict` | **0** | `ok=true`, `expected == checked == 180` |
| `bien_nhan_v2` | **0** | TỔNG: ĐẠT |

Và bộ test của chính packet, chạy TRỌN trên Linux trong sandbox:
`rc=0` · `TU KIEM r523: DAT` · `23/23` nhóm bắt buộc · **`76/76`** đột biến tự-kiểm ·
`MUTANT: giet = 10 · khong giet = 0 · khong do duoc = 0 / tong 10`.

## ADR-0044

`sensitive` = ≤3 tệp VÀ ≤300 dòng. Đo: **3 tệp**, sản phẩm **+17 −14**, phối hợp +76/+33.
**Trong ngưỡng cả hai chiều.** Không cần khai ngoại lệ.

## BẢNG SĂN — sáu hướng, mỗi hướng có lệnh + kết quả thật

| # | hướng | kết quả | phán |
|---|---|---|---|
| H1 | bản vá có chữa đúng GỐC lỗi không | fixture `bs` chuyển từ dưới `d` sang dưới `Path.cwd()`; `d` chỉ còn giữ bản sao MODULE, không tham gia `relpath` | **SẠCH** — đường sinh `ValueError` cross-drive bị cắt tận gốc, không phải bọc `try` |
| H2 | dòng `unlink()` có RĂNG không, hay chỉ là nghi lễ | **đột biến M-a**: gỡ đúng dòng ấy ⇒ `rc=1`, `TU KIEM r523: DO_CHOT — chot cua ca r523 that bai`, `22/23` | **SẠCH** — giết THẬT, và giết **đúng lý do**: chết bằng chốt của chính ca ấy, không bằng lỗi vô can |
| H3 | gộp 2 bản sao module thành 1 có làm YẾU ca không | `_nap_ban_sao` đặt tên **ngẫu nhiên** (`ban_sao_{token}`), nên bản GỐC cho `bs` **hai thư mục khác nhau** — trái chính docstring của nó (*"dùng cùng một thư mục thật cho cả hai cách viết"*) | **CẢI THIỆN, không phải hồi quy** — bản mới dùng MỘT thư mục, tức làm mã KHỚP lời khai sẵn có. Đây cũng là lý do `unlink()` mới cần tới |
| H4 | `.ket-qua-2.jsonl` có đầu độc lượt so không | `chay_mot_mutant` lặp `lan_thu in (1,2)`, nhưng `chot(tuyet_doi == (GIET,"",1))` đứng **TRƯỚC** `unlink()` ⇒ tới được `unlink` thì đã chứng minh chỉ có 1 lượt | **SẠCH** — thứ tự hai dòng là chốt, không phải may |
| H5 | fixture đặt trong `cwd` có rò vào checkout không | chạy trọn: `porcelain` rỗng trước VÀ sau, không còn `r523-*`. **Phản chứng SIGKILL**: dựng đúng mẫu `TemporaryDirectory(dir=Path.cwd())` rồi `kill -9` ⇒ `r523-xukn0ewr` **SỐNG SÓT** | **LỆCH** — xem `PHÁT HIỆN 1` |
| H6 | đường nào ngoài `write_set` | 3 đường đổi: `ops/nhanh_don_duoc_test.py`, `ops/specs/…-r1.md`, `ops/leases/…-g1.yaml` | **SẠCH** — cả ba đều trong `write_set` của g2 |

Ghi rõ: **bốn hướng ra SẠCH và một hướng ra CẢI THIỆN.** Một kết luận sạch có giá ngang một
phát hiện, nên chúng được kê đầy đủ chứ không lược đi.

## PHÁT HIỆN

### 1. `fixture-trong-cwd-song-sot-khi-tien-trinh-bi-giet` — **P3**, 1 thể hiện

`tempfile.TemporaryDirectory(prefix="r523-", dir=Path.cwd())` dọn bằng context manager, tức
bằng một đường `finally`. Đường ấy **không chạy** khi tiến trình bị giết cứng.

Phản chứng **chạy được**, không phải lập luận: dựng đúng mẫu ấy trong một thư mục, `kill -9`
giữa chừng ⇒ `r523-xukn0ewr` còn nguyên. Khi `cwd` là checkout — trường hợp thường gặp nhất,
vì bộ test hay chạy từ gốc kho — thư mục thừa ấy làm `git status --porcelain` **khác rỗng**,
mà đó lại đúng là điều kiện tiên quyết của cross-review và của cổng land.

**Vì sao vẫn chỉ là P3, không phải P2.** Ba lý do, cả ba đo được:
(a) đường thoát BÌNH THƯỜNG sạch — chạy trọn bộ, `porcelain` rỗng cả trước lẫn sau;
(b) đường thoát NGOẠI LỆ cũng sạch — context manager dọn khi có exception, và codex đã tiêm
    hai ca lỗi setup;
(c) `A3` của spec **cho phép tường minh**: *"Use scoped temporary context on a suitable drive
    if needed"*. Đây đúng là thứ nó cho phép.

**Lựa chọn của codex là CÓ LÝ, không phải sơ suất** — và tôi nói thẳng thế vì bản thay thế
cũng có giá. Đặt fixture ở `Path.cwd().parent` thì cùng ổ đĩa, ngoài checkout, nhưng đường
tương đối sinh ra sẽ mang `..`, tức **đổi HÌNH DẠNG** của chính đường dẫn mà ca này sinh ra để
dò (docstring mô tả lỗi ghép-hai-lần `P/r/r/.ket-qua-N`). Đổi hình dạng thì phải đo lại từ đầu,
không được suy ra là vẫn đúng.

Nên đây là một **rủi ro tồn dư đã đo được**, nêu ra để người giữ biết mà chọn, không phải một
lỗi đòi sửa trước khi land.

## KHÔNG ĐO ĐƯỢC — và approve dưới đây KHÔNG phủ những mục này

- **Toàn bộ số đo Windows của executor.** `8/8 base · 10/10 product mutant · 23/23 selfcheck ·
  76/76 selfcheck mutant · 2901,378s`, bốn thế bố trí ổ đĩa `C:/C:`, `D:/D:`, `D:/C:`, `C:/D:`,
  và hai ca baseline `rc=1` với `ValueError` thật — tôi **không chạy lại được** trong container
  Linux này. Chúng là lời khai của executor, có biên bản, nhưng **không phải phép đo của tôi**.
  Thứ tôi kiểm được là hiện vật lên ref **đúng byte** bản đã đo (năm định danh khớp), nên nếu
  lời khai ấy đúng thì nó đúng về CHÍNH mã này.
- **Hành vi thật khi `cwd` và temp khác ổ đĩa.** Đây là bản chất của lỗi, và Linux **không tái
  hiện được** — một ổ đĩa duy nhất thì `relpath` không bao giờ ném `ValueError`. Đó cũng chính
  là lý do lớp lỗi này sống sót tới tận CI Windows.
- **CI của ứng viên.** Không gọi CI tay lần nào (`manual_ci_budget: 0`, chỉ thị chủ kho). Chưa
  có lượt CI nào cho `7c7ad450` tại thời điểm chấm.

## KẾT LUẬN

**`approve`** — 0 P1 · 0 P2 · **1 P3** · 1 thể hiện.

Bản vá cắt đúng gốc lỗi thay vì bọc triệu chứng; chốt mới (`không tuyệt đối` **và** `resolve()
== bs`) chặn đúng đường "vá bằng cách tuyệt-đối-hoá" mà một bản sửa lười sẽ đi; dòng `unlink()`
có răng đo được bằng đột biến; và việc gộp về một thư mục vật lý làm mã khớp lại docstring vốn
đã sai từ trước. Sáu cổng `rc=0`, bộ test của packet `76/76` đột biến, `10/10` mutant, phạm vi
đúng ba đường trong write set, ADR-0044 trong ngưỡng cả hai chiều.

`P3` **không chặn approve**: `review_class: sensitive` đòi không P1/P2, và ở đây là 0/0. Nó
được ghi ra để người giữ quyết, không phải để giữ lại bản vá.

**Approve này chỉ phủ thứ tôi ĐO ĐƯỢC** — đọc mã, đột biến, sáu cổng, và bộ test trên Linux.
Nó **không** xác nhận các con số Windows của executor, và **không** thay `A7` (admission, CI,
merge, cổng hậu merge), vốn vẫn `not_run`.
