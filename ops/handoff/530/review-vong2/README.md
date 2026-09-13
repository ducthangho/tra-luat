# Cross-review vòng `2/10` cho PR #532 — hồ sơ

| thứ | giá trị |
|---|---|
| `reviewed_sha` | `3f1cda17aa254e1a10afa12aa387bc782a945c6f` |
| `reviewed_tree` | `98ffde01a2bf14eb5150aa09044323ed20c71121` |
| verdict | **`changes_requested`** — `0 P1` · **`4 P2`** · `1 P3` · `6 NỢ` (ngoài write set) |
| lượt chạy | `run/c8070bbc` — `trang_thai=xong`, `ma_thoat=0`, `thoi_luong_giay=2044.185`, `stderr_byte=3223985` |
| reviewer | `codex` / `gpt-6-astra` `xhigh`, nền khác, độc lập với phiên executor |
| `VERDICT.rv530-2.md` | sha256 `f840d87ea5f94061ce78200c8f4a383ace0ec72b40c85e595e8f8a2027111596`, 30323 B |

**Nguồn có thẩm quyền là các TỆP trong thư mục này.** Bản chiếu đăng trên PR #532 chỉ là bản chiếu;
lệch nhau thì tệp đúng.

## Ba lượt phóng, hai lượt CHẾT — và `setsid` đã bị BÁC bằng phép đo

| lượt | phóng | kết cục | phiên điều phối trong lúc chạy |
|---|---|---|---|
| `ad33fc0d` | `19:00:29Z` | chết `~19:08:56Z` (**8,5 phút**) | kết thúc lượt trò chuyện ngay sau khi phóng |
| `ed2d19ad` (`setsid`) | `21:27:01Z` | chết `~21:33:13Z` (**6 phút**) | như trên |
| `c8070bbc` | — | **`xong`, 2044.185s** | **BẬN liên tục** ở foreground suốt lượt |

`setsid` tách hẳn nhóm tiến trình (`sid=31226` ≠ `sid=31791` của phiên) mà **vẫn chết** ⇒ cơ chế
KHÔNG phải "giết theo nhóm tiến trình". Giải thích khả dĩ nhất là container bị thu hồi khi phiên
nhàn rỗi — **đó là TƯƠNG QUAN, chưa phải nhân quả đã chứng minh**: thứ đo được chỉ là *lượt duy nhất
sống là lượt duy nhất có phiên bận liên tục*. Cách chết đo bằng ba tín hiệu, không đoán: `ps` rỗng ·
`os.kill(pid,0)` ⇒ `ProcessLookupError` · mtime cuối của `stderr.log`; `run.json` vẫn ghi `dang_chay`
vì launcher bị giết trước khi kịp đóng sổ.

⇒ Nếp vận hành: **giữ phiên BẬN ở foreground suốt lượt review**, mỗi lệnh chờ ≤ 600s, nối tiếp nhau.

## Bốn `P2` — ba là LẶP LẠI lớp của vòng 1, một là lỗ MỚI do chính bản vá vòng 1 mở

| lớp | trạng thái | phép đo của reviewer |
|---|---|---|
| `m5-van-cham-chet-bang-chuoi` | **VÁ SINH LỖI MỚI** | `t163` nhận `KDD` cho bốn mục `DO` ⇒ tiêm `Exception` vào chốt cuối `t162` vẫn `7/7`, `rc=0`; kênh thật ghi `nhan=DO_KHAC` (`m5-falsecredit.log`, `m5-unrelated-real.jsonl`) |
| `control-bo-sot-chot-va-trang-thai` | lời khai của executor **bị bác** | gỡ riêng **19** nhánh `if` của bộ đọc ⇒ chỉ **6** làm `t164` đỏ; **6** hành vi thiếu tự kiểm phân biệt (`guard-matrix.json`, `absorption.log`, `unguarded.log`) |
| `vat-hoa-tuong-duong-qua-rong` | **VÁ HỜ** | chú thích `:7144–7148` còn khai *"một bộ TƯƠNG ĐƯƠNG"*, **trái** docstring đã sửa ở `:6592–6612` (`materialization.log`) |
| `m3-bo-sot-loi-chuan-bi` | **MỚI** | `_cay_mut_512` và `sinh_dau_phien` ngoài phạm vi bắt `OSError` ⇒ **thoát**; `attempts=1` thay vì `2` (`transport.log`) |

Cùng lượt ấy xác nhận bản vá vòng 1 cho byte stdout không UTF-8 **ĐÃ VÁ THẬT**.

Hình dạng chung là bài học `CLAUDE.md` *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"*: mỗi bản vá
**ĐÚNG** nhưng **HẸP**.

## `1 P3` và `6 NỢ`

`dem-cau-truc-sai-don-vi` (P3). NỢ: `moc-nen-review-khong-dong-bo` ·
`phan-ra-dong-them-khong-phai-so-do-chinh-xac` · `neo-blob-cua-mau-so-493-sai` ·
`bang-khai-bo-sot-dai-luong` · `thoi-luong-khac-giua-cac-luot-do` · `script-chi-phi-chap-nhan-suite-do`.

Đáng chú ý trong `moc-nen-review-khong-dong-bo`: `BANG_KHAI` #1 ghi *"numstat so `dc02c9b`: 1 tệp"*
trong khi diff **toàn cây** so base ấy có **3** tệp. Reviewer đã đo và kết luận **KHÔNG vi phạm write
set** — hai tệp kia (`.claude/dev/chon_reviewer.py` `+1/−1`, `chon_reviewer_test.py` `+49/−4`) đến từ
**merge master**, và diff so master trong gương (`d706abd`) chỉ có đúng `ops/lease_publish_test.py`.
Bài học: khi đang **lọc đường dẫn** thì phải ghi *"1 đường thuộc packet"*, đừng dùng phép lọc để
chứng minh diff toàn cây chỉ một tệp.

## Điều kiện đo

`actionlint 1.7.7` và `shellcheck 0.9.0` **CÓ MẶT**. Gương `--mirror` **412 ref** (`8 heads + 365
remotes + 39 tags`), không shallow. Một con số không ghi điều kiện đo thì sẽ trôi mà không ai biết.

**Windows / full CI: `KHÔNG ĐO ĐƯỢC`** — chỉ thị chủ kho không cho chạy CI tay, và lỗi Windows là
lỗi đã biết.
