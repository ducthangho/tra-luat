# EVIDENCE — PR #512 (WINDOWS-LEASE-SUITE, lease #504) · head `353eae10120da2a1788dcaf7a906fe46261bd71b`

Tác giả: phiên `claude` (Opus 5). Lời khai này là **của tác giả**, không phải phép đo độc lập — mỗi con số dưới đây kèm CHỖ đo lại được.

## Head và base

| | |
|---|---|
| head | `353eae10120da2a1788dcaf7a906fe46261bd71b` |
| base (`origin/master`) | `015ffcc09d76fbc9cdfbc3d2ee0735c3ead8d364` |
| diff PR | `git -C cay-kho diff origin/master...HEAD` (BA chấm) ⇒ **2 tệp** |
| bản vá lượt này | `git -C cay-kho diff c3bcfa1 353eae1` |
| `ops/lease_publish_test.py` | sha256 `8bcc22934e5d1eca808674cd8d9ecbc88a01bcbfd5bda7fdb6cd5478757635ea` |
| `ops/chay_lease_publish_test.sh` | sha256 `87c760294763c71a67cfaee50a440e62b31c439beb0abbfcb5e34076d32be693` (KHÔNG đổi từ lượt 1) |

Hai commit của lượt này:

- **`a15f302`** — áp NGUYÊN `nguon/HINT.rvwin512-5.patch` (sha256 `9087726521c621617de5dc9fc40eab5e0f302f928662d23a8c62d47e81b47cdc`), 3 hunk, +78/−107, một tệp.
- **`353eae1`** — merge `origin/master` `015ffcc` vào nhánh. Diện tích **2 tệp** (`ops/dung_goi_review.sh`, `ops/reviews/DO-T33-VA-GOI-REVIEW-20260907.md`), **không tệp nào** thuộc write set: `git diff --stat a15f302 353eae1 -- ops/lease_publish_test.py ops/chay_lease_publish_test.sh` ⇒ **RỖNG**. Merge này là quy định drift (kiểm head drift trước vòng dự đoán là vòng chốt), không phải một bản vá.

## Bản vá vòng 5 làm gì — và nó là một phép XOÁ, không phải một phép THÊM

Verdict lượt 5 xếp **3 lớp P1 + 1 lớp P2, 5 thể hiện**, và bốn lớp ấy (F1 · F2 · F4 · F7) đều mang trạng thái **VÁ SINH LỖI MỚI** trên `c3bcfa1`. Gốc chung: bản vá lượt 4 thêm **một tầng chạy lại toàn suite bên trong một ca test**, và tầng ấy tái tạo đúng ba chốt mà suite này sinh ra để đóng (nhóm tiến trình riêng · tee · ngân sách tổng), cộng một lỗ thứ tư ở chỗ `t160` chỉ thử hàm thuần.

Nên bản vá lượt này **bỏ hẳn tầng chạy lại**:

- `_phan_loai_lech_ab(ket_a, ket_b)` giờ **thuần**, không callback, không chạy lại. Khớp ⇒ `LECH_KHOP`. Lệch ⇒ `LECH_CHUA_RO` kèm thân bằng chứng nói thẳng là **CHƯA loại trừ** rò `GITHUB_ACTOR`, ảnh hưởng thứ tự ca, hay tải máy.
- Consumer ở `t125`: `ket_luan, thong_diep = _phan_loai_lech_ab(khong_actor, co_actor)` rồi `bang(ket_luan == LECH_KHOP, thong_diep)` — **mọi** lệch làm CHÍNH `t125` ĐỎ.
- `t160_lech_AB_phai_giu_bang_chung_va_CHAN_tai_consumer_t125` bịa dữ liệu ở **biên tiến trình** rồi lái **CHÍNH `t125`**, nên bộ phân tích, phép so và phép chốt đều là bản THẬT — chứ không phải hàm thuần như lượt trước.

Tôi khai thẳng cái ĐÁNH ĐỔI: bản vá này **không** phân biệt được rò actor với ca chập chờn. Nó thay một lời khai nhân quả **không đo được** bằng một lời khai **không biết**. Hướng phân biệt thật (chạy lại có kiểm soát) đòi ngân sách tổng, nhóm tiến trình và tee cho tầng mới — tức đúng ba chốt vừa bị tái tạo — nên tôi cho rằng nó thuộc packet khác, không thuộc write set này.

## Phép đo trên head này — neo theo SỐ DÒNG của `nguon/suite-luot6-linux.log`

Lệnh: `AL_VER=1.7.7 AL_DICH=/tmp/actionlint bash ops/chay_lease_publish_test.sh`, Linux, container remote.

| đại lượng | giá trị | dòng trong log |
|---|---|---:|
| tổng kết vế `[B]` | `lease_publish: 155/155 đạt; đã chạy=155, bỏ qua=0` | **1055** |
| tổng kết vế `[A]` | `lease_publish: 155/155 đạt; đã chạy=155, bỏ qua=0` | **1060** |
| tổng kết phiên CHA | `lease_publish: 155/155 đạt; đã chạy=155, bỏ qua=0` | **1156** |
| `t125` (CHA) | `72.143s QUA` | **1061** |
| `t160` (CHA) | `0.038s QUA` | **1148** |
| số ca chạy ở CHA | `grep -c '^<<< ra'` ⇒ **155** | — |

Hai số **BẰNG NHAU** trong cả ba dòng tổng kết là bằng chứng dương; `rc` một mình thì không.

## Catalogue đột biến — `nguon/dotbien-16-linux.txt`

`TONG: giet that 16/16 — tin dung gia 0, song sot 0, chan 0`.

Ba đột biến MỚI của lượt này nhắm đúng chỗ NỐI DÂY, vì lượt 5 đã chứng minh chỗ ấy là chỗ hở:

| đột biến | ca đỏ | chốt |
|---|---|---|
| `M15-classifier-tra-KHOP-khi-lech` | `t160` | `mọi lệch phải làm CHÍNH t125 đỏ, chưa rõ nguyên nhân` |
| `M16-consumer-bo-classifier-gan-KHOP` | `t160` | cùng chốt |
| `M17-consumer-nhan-ca-trang-thai-CHUA-RO` | `t160` | cùng chốt |

Bộ phân hạng đòi **bốn** điều kiện cùng lúc mới tính GIẾT THẬT: `rc≠0` · đúng **một** ca đỏ · ca ấy là ca ĐÍCH · chi tiết đỏ **không** khớp `^<Type>(Error|Exception):`. Đột biến chạy trên **cây rời** ngoài kho, tên tệp riêng từng đột biến, `-B` + `PYTHONDONTWRITEBYTECODE=1`.

## Cổng khác

| cổng | kết quả |
|---|---|
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0 — `đã quét 7 tệp, 0 chỗ chép doctrine` |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | rc=0 — `47 ADR trên đĩa, 47 dòng §20, khớp 1–1` |
| `git diff --numstat origin/master...HEAD` | 2 tệp · **+1082 / −27** |

## KHÔNG ĐO ĐƯỢC

1. **Windows.** Không lượt `workflow_dispatch` nào chạy trên head này — chủ kho ra chỉ thị KHÔNG chạy CI tay, chỉ nhận lượt tự động, và full CI khi merge. Nên `A3` của đặc tả (bước 20 Windows ≤ 15 phút) **chưa đo** trên `353eae1`. Đừng đọc suite xanh trên Linux thành `A3` đạt.
2. **Mutant `S8-bo-deadline` chập chờn.** Lượt CI đỏ trên `e6feddb` (trích ở `nguon/CI-e6feddb-gate-do-trich.md`) chết vì mutant ấy sống sót ở seam `KhoObject._con_thoi_gian`. Gốc nằm trong `ops/lease_publish.py` — **NGOÀI write set**, và chạm vào đó là điều kiện dừng `S3`. Sáu lần thử tái hiện tại chỗ đều không ra. Nợ đã khai, chưa chữa.
3. **Phân biệt rò actor / chập chờn.** Xem mục đánh đổi ở trên. Trạng thái là `KHÔNG ĐO ĐƯỢC`, không phải "đã loại trừ".

## `S2` — MỘT ĐIỀU KIỆN DỪNG TÔI ĐỂ TRÔI BỐN VÒNG (tự khai)

Lease khai `dieu_kien_dung` có **`S2` dòng thêm > 300**. Đo lại, neo `base_sha` `b98531e`, chỉ hai đường write set:

| head | dòng thêm |
|---|---:|
| `27463d4` | 67 |
| `e0b5bf0` | 195 |
| **`8ffd062`** | **746** ← vượt ở ĐÂY |
| `59a0ed4` | 914 |
| `1df4729` | 991 |
| `353eae1` | **1082** |

Vượt từ `8ffd062`, tức **bốn vòng review trước**, và không commit/PR/Issue nào của nhánh nêu nó (`grep` cho `S2`/`300`/`nâng trần` ⇒ 0). Không có khối `nang_tran` nào cho trục này. Đã báo chủ kho ở PR #512 comment `5645054339`; **tôi không tự nâng** và đã khai KHÔNG merge trước khi có quyết định.

Ghi vào đây vì đó là một lời khai về CHÍNH sự tuân thủ của packet, và nó thuộc thứ reviewer phải kiểm được chứ không phải tin.
