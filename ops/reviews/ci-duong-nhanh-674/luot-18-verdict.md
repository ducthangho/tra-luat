Reviewed commit: aad37ad2cd129943cac578a48f0ee377e58439c6
verdict: changes_requested
reviewed_sha: aad37ad2cd129943cac578a48f0ee377e58439c6
review_class: advisory_review (reviewer cùng họ executor — Claude Opus)

> Reviewer: Claude Opus 5.5 (effort max), lượt 18, packet #674 CI-DUONG-NHANH-HO-SO (đặc tả r2, lease g4 vòng 4).
> Executor cũng là Claude Opus ⇒ cùng họ ⇒ ĐÂY LÀ `advisory_review`, KHÔNG phải `cross_approved`.
> Tệp này ghi TĂNG DẦN; nếu thiếu mục cuối thì lượt bị cắt giữa chừng — phần đã ghi vẫn là dữ liệu.

Trạng thái: HOÀN TẤT — **changes_requested** · TONG: P0=0 P1=0 P2=0 P3=2 — F2 lượt 17 ĐÃ VÁ THẬT; F1 lượt 17 VÁ HỜ (hai ca được chỉ
đã vá, lời khai mới rộng hơn chốt ⇒ F1' P3 `tin-hieu-chot-ca-khong-doc-quyen`); mới: F3 P3 `tiem-vo-can-vang-mat-van-xanh`. Bất biến head
giữ; đúng đắn đường nhanh không có bằng chứng mới. Ngưỡng chủ kho 0/0/0 ⇒ chưa đạt.

## Đối tượng (đo)
- PROMPT.md sha256 `2fd6df5ba239a6c19ac40e9375aac36d716c067b6cccb1bdcd906e9561dedcb3` (khớp lời gọi) · SPEC-r2.md sha256
  `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` (khớp PROMPT).
- `git -C cay rev-parse HEAD` ⇒ `aad37ad2cd129943cac578a48f0ee377e58439c6` (commit cục bộ, chữ ký `%G?`=N trong sandbox vì thiếu
  allowedSignersFile — KHÔNG ĐO ĐƯỢC chữ ký); cha `98377f8`; `origin/master` = merge-base = `20ec8d5d0e86cb7dc01f202c7596407a957e5961`.
  `GIT_OPTIONAL_LOCKS=0 git -C cay status --short --ignored` ⇒ 0 dòng lúc mở.
- Mọi phép đo chạy trên clone `tmp/w` dựng từ `kho.git` tại `aad37ad` (`tmp/bin/dung_clone.sh`); `diff -rq --exclude=.git cay tmp/w` ⇒
  GIỐNG HỆT. `cay` không bị chạy lệnh nào ngoài đọc (`git -C cay log/show/diff/status` với `GIT_OPTIONAL_LOCKS=0`).

## Môi trường và số đo nền (HEAD aad37ad, clone `tmp/w`, `TMPDIR=R/tmp`; log `out/nen/`)
Linux 4 lõi, Python 3.11.15, git 2.43.0, actionlint 1.7.7, **shellcheck 0.9.0 CÓ MẶT**, ruff 0.15.15, PyYAML 6.0.1, node 22. Không Actions, không Windows.

| Lệnh | Output thật |
|---|---|
| `python3 -B ops/ci_duong_nhanh_test.py` (`out/nen/suite-head.log`) | `CA: 104/104 dat · 0 do · 0 hong` · `DOT BIEN: 317/317 bi giet dung ly do` · `KIEM KE: ca hanh_vi=74 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=11 = 104 · dot bien .claude/dev/ci_dang_ky_test.py=2 + .github/workflows/ci.yml=78 + ops/ci_duong_nhanh.py=178 + ops/ci_duong_nhanh_test.py=59 = 317` · `TIEM VO CAN: 99 ca dich x 2 diem tiem: SONG_SOT=32 · TIN_DUNG_GIA=166 · cham 99/99 ca · doi chung co rang (doi kieu qua gia tri tra ve): GIET` · `TU KIEM PHAN HANG: DAT (5 mau rc, 7 dot bien that)` · `TONG: DAT` · `RC=0` · 153 s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` (shellcheck 0.9.0 có mặt) | rc=0, không finding |
| `python3 -m ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py` | `All checks passed!` rc=0 |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` rc=0 |
| `python3 -B ../../goi/do_lai_so.py` | `[1] … do duoc diff: 345; toan allowlist: 63; … NGUYEN BAN do: 8` · `[2] … 119 tep; … dat 119, truot 0` |
| `python3 -B ../../goi/kiem_ke.py` | `CA tong: 104` (74/16/3/11) · `DOT_BIEN tong: 317` (178/59/78/2) · `MAU_RC = 5 · TU_KIEM_DOT_BIEN = 7` · ba ca dữ liệu `loi = [] · 6.0s` |
| `git diff --numstat origin/master...HEAD` | `1 0 .claude/dev/ci_dang_ky_test.py` · `99 8 .github/workflows/ci.yml` · `544 0 ops/ci_duong_nhanh.py` · `3557 0 ops/ci_duong_nhanh_test.py` (đúng 4 tệp write set) |
| `git diff --numstat origin/master -- .claude/dev/ci_dang_ky_test.py` | `1 0` |
| `git diff --numstat 98377f8 HEAD` (bản vá lượt 18) | `2 1 .github/workflows/ci.yml` · `10 7 ops/ci_duong_nhanh.py` · `478 58 ops/ci_duong_nhanh_test.py` |

Khớp lời khai commit `aad37ad` (`CA 104/104, DOT BIEN 317/317, TIEM VO CAN 99/99 ca, TU KIEM DAT, TONG DAT; ci_dang_ky_test 23/23 + 1025/1025; actionlint rc=0; ruff F sach; doctrine-scan rc=0; +1/-0`).

### H0 — Bất biến head: mã chạy của `ops/ci_duong_nhanh.py` và cấu trúc YAML `ci.yml` không đổi so `98377f8` ⇒ **ĐÚNG**
Lệnh `python3 -B tmp/ast/so_ast.py tmp/w 98377f8 aad37ad` (log `out/nen/h0-ast.log`):
```
ops/ci_duong_nhanh.py: AST bo docstring (17/17 docstring) bang nhau = True
  doi chung (TOI_DA_TEN_IN 5->6) bang nhau = False
.github/workflows/ci.yml: cau truc YAML da parse bang nhau = True
  doi chung (doi mot gia tri) bang nhau = False
ops/ci_duong_nhanh_test.py: AST bo docstring bang nhau = False (mong False: luot 18 doi ma test)
```
Kết luận: bản vá lượt 18 chỉ đổi docstring của `ops/ci_duong_nhanh.py` và chú thích của `ci.yml` (đối chứng có răng); mọi thay đổi mã nằm trong `ops/ci_duong_nhanh_test.py`.

## ĐỐI CHIẾU LƯỢT TRƯỚC — phần 1: F1 `tin-hieu-chot-ca-khong-doc-quyen` (đột biến TỰ VIẾT, harness THẬT của HEAD)

### H1a — Lặp lại đúng phép đo lượt 17 (b)(c) trên HEAD ⇒ **hai ca lượt 17 chỉ ra ĐÃ VÁ THẬT**
Lệnh `python3 -B tmp/h1/rig_l17.py tmp/w` (gọi `chay_mot_dot_bien` CỦA HEAD; log `out/h1a-l17.log`; mỗi dòng: tên · ca đích · hạng · dòng cuối):
```
(b) vo can `raise KeyError`       dau phan_loai_tu_diff | t01 -> TIN_DUNG_GIA ["KeyError: 'vo can'"]   | t06 -> TIN_DUNG_GIA
(b) vo can `raise TypeError`      dau phan_loai_tu_diff | t01 -> TIN_DUNG_GIA                        | t06 -> TIN_DUNG_GIA
(b) vo can `raise AttributeError` dau phan_loai_tu_diff | t01 -> TIN_DUNG_GIA                        | t06 -> TIN_DUNG_GIA
(b) vo can `raise ValueError`     dau phan_loai_tu_diff | t01 -> TIN_DUNG_GIA                        | t06 -> TIN_DUNG_GIA
(b) vo can `raise NameError`      dau phan_loai_tu_diff | t01 -> TIN_DUNG_GIA                        | t06 -> TIN_DUNG_GIA
(c) vo can `raise UnicodeError` dau _doc_raw            | t20ze -> TIN_DUNG_GIA                      | t20zc -> TIN_DUNG_GIA
(T1) vo can `raise AttributeError` dau _doc_raw (CA HAI duong)      | t20ze -> TIN_DUNG_GIA
(T1') vo can `raise AttributeError` dau lenh_kiem_re                | t20ze -> TIN_DUNG_GIA
(T2) AttributeError CHI khi ten khong UTF-8 (sau decode _doc_raw)    | t20ze -> GIET
(T2') UnicodeError CHI khi ten khong UTF-8 (lop ca nay do)          | t20ze -> GIET
```
(dòng (b) gộp hai đích cho gọn; nguyên văn từng dòng ở log). Lượt 17 đo `t06 -> GIET` cho TypeError/AttributeError/ValueError và
`t20ze -> GIET` cho UnicodeError; nay cả bốn ⇒ `TIN_DUNG_GIA`. `t20ze` qua tiến trình con: lỗi vô can ở CẢ HAI đường bị đối chứng
UTF-8 chặn (`T1`, `T1'` ⇒ TÍN DỤNG GIẢ). Lỗi CHỈ ở tên không UTF-8 ⇒ GIET (`T2`, `T2'`): đúng thiết kế ghi ở docstring `t20ze` (tính
chất của ca là "tên không UTF-8 phải ĐẠT kiem-re"; mọi thất bại riêng tên ấy LÀ vi phạm tính chất đó) — ghi QUAN SÁT, không tính P.

### H1b — Mỗi ĐƯỜNG VÀO đổi kiểu, đặt quanh lời gọi mã ĐẦU TIÊN của `t01`: ba cổng của chính bộ test có bắt không? ⇒ **cổng TĨNH `t99` hở 9/11 mẫu (bắt đúng hai đối chứng S2/S3); trong 10 mẫu cho GIẾT giả, phép tiêm `[ma]` bắt 9 khi ở lời gọi đầu**
Lệnh `python3 -B tmp/h1/rig_duong.py tmp/w` (log `out/h1b-duong.log`). Mỗi mẫu: (1) tệp test CÓ SẴN mẫu ấy (cây tạm `dung_cay_tam` của
HEAD) · `[nen]` t01 xanh khi chưa có lỗi · `[t99]` chốt tĩnh S1–S5 chạy như ca đích (rc=3 ⇒ BẮT) · `[tiem ma]/[tiem bang]` phép tiêm của
chính bộ test (BẮT = GIET/HONG/SONG_SOT-có-nổ) · rồi (2) lỗi VÔ CAN trong mã (`raise <Lớp>` đầu `phan_loai_tu_diff`) ⇒ hạng của t01.
```
S2 except hep goi bang (doi chung)          [nen 0] [t99 rc=3 => BAT] [tiem ma TIN_DUNG_GIA+no] [bang TIN_DUNG_GIA+no] -> TIN_DUNG_GIA (LoiHaTangTinHieu: bang() goi trong luc xu ly AttributeError)
S3 co gan truc tiep (doi chung)            [nen 0] [t99 rc=3 => BAT] [tiem ma GIET+no => BAT]  [bang TIN_DUNG_GIA+no] -> GIET
D3a nuot roi giu mac dinh (except: pass)   [nen 0] [t99 rc=0]        [tiem ma GIET+no => BAT]  [bang TIN_DUNG_GIA+no] -> GIET
D3b co qua bien trung gian                 [nen 0] [t99 rc=0]        [tiem ma GIET+no => BAT]  [bang TIN_DUNG_GIA+no] -> GIET
D3c contextlib.suppress                    [nen 0] [t99 rc=0]        [tiem ma GIET+no => BAT]  [bang TIN_DUNG_GIA+no] -> GIET
D4a helper ghi vao tham so ra (no return)  [nen 0] [t99 rc=0]        [tiem ma GIET+no => BAT]  [bang TIN_DUNG_GIA+no] -> GIET
D4b helper `return` trong finally          [nen 0] [t99 rc=0]        [tiem ma GIET+no => BAT]  [bang TIN_DUNG_GIA+no] -> GIET
D6 doi loi dung san thanh SuDoGia roi bat  [nen 0] [t99 rc=0]        [tiem ma GIET+no => BAT]  [bang TIN_DUNG_GIA+no] -> GIET
D1 tin hieu THAT cat san roi `raise tin`   [nen 0] [t99 rc=0]        [tiem ma GIET+no => BAT]  [bang SONG_SOT+no => BAT] -> GIET
D2 bang() qua LUONG khac trong except      [nen 0] [t99 rc=0]        [tiem ma GIET+no => BAT]  [bang TIN_DUNG_GIA+no] -> GIET
D3a' nuot NameError (lop ngoai LoiVoCan)   [nen 0] [t99 rc=0]        [tiem ma TIN_DUNG_GIA+no] [bang TIN_DUNG_GIA+no] -> GIET
```
(cột rút gọn; nguyên văn có cả dòng `DO:`/`HONG:` ở log). Đọc: chốt CHẠY trong `bang()` đóng đúng đường 2 (`except` gọi `bang()`), kể cả
hẹp. Các dạng D* KHÔNG phải trò lạ: D3a là chính đường 3 ("biến cờ trong MỘT hàm") ở dạng tự nhiên nhất (nuốt rồi để giá trị mặc
định), D3c là cùng đường qua `suppress`, D4a/D4b là đường 4 không qua `return` trong `except`, D6 là đường 6 ở NGOÀI helper duy nhất
mà `t23b` canh. Không dạng D* nào bị `t99` bắt. Trong 10 mẫu cho GIẾT giả (S3 + chín D*; S2 không cần bắt vì chốt chạy đã biến nó
thành TÍN DỤNG GIẢ), khi đặt ở lời gọi ĐẦU TIÊN phép tiêm `[ma]` bắt 9 — trượt D3a' vì `NameError` không nằm trong các lớp cha của
`LoiVoCan` (`[bang]` chỉ bắt thêm D1, vốn `[ma]` đã bắt).

### H1c — Cùng dạng, đặt quanh lời gọi mã VỀ SAU của `t01` + lỗi vô can chỉ ở đầu vào nhiều tệp ⇒ **KHÔNG cổng nào bắt; GIẾT GIẢ**
Lệnh `python3 -B tmp/h1/rig_sau.py tmp/w` (log `out/h1c-lan-goi-sau.log`):
```
D3a nuot (except AttributeError: pass) o lan goi SAU | loi vo can chi khi nhieu tep (len(doi) > 1)
   [nen t01 rc=0] [t99 rc=0] [tiem ma=TIN_DUNG_GIA+no · bang=TIN_DUNG_GIA+no] -> t01 GIET ['DO:t01_toan_ho_so_duong_nhanh:bon tien to ho so cung mot PR phai la duong nhanh']
D3a nuot (except AttributeError: pass) o lan goi SAU | loi vo can doi chung: moi lan goi
   [nen t01 rc=0] [t99 rc=0] [tiem ma=TIN_DUNG_GIA+no · bang=TIN_DUNG_GIA+no] -> t01 TIN_DUNG_GIA ['HONG:t01_toan_ho_so_duong_nhanh:AttributeError: vo can']
D6 doi thanh SuDoGia o lan goi SAU | loi vo can chi khi nhieu tep (len(doi) > 1)
   [nen t01 rc=0] [t99 rc=0] [tiem ma=TIN_DUNG_GIA+no · bang=TIN_DUNG_GIA+no] -> t01 GIET ['DO:t01_toan_ho_so_duong_nhanh:bon tien to: loi: vo can']
D6 doi thanh SuDoGia o lan goi SAU | loi vo can doi chung: moi lan goi
   [nen t01 rc=0] [t99 rc=0] [tiem ma=TIN_DUNG_GIA+no · bang=TIN_DUNG_GIA+no] -> t01 TIN_DUNG_GIA ['HONG:t01_toan_ho_so_duong_nhanh:AttributeError: vo can']
```
Đây là tổ hợp mà docstring `quet_doi_kieu_tin_hieu` tự khai là chỉ còn "luật tĩnh S1–S5 và chốt chạy ở `bang()` canh" — đo: cả hai
đều im, và lỗi VÔ CAN được đếm GIẾT. Đối chứng (lỗi ở MỌI lời gọi) ⇒ TÍN DỤNG GIẢ, tức phép đo có răng.

### H1d — Hôm nay tệp test có dạng D* nào trên đường của mã bị đột biến không? ⇒ **KHÔNG (0 tín dụng sai hôm nay)**
Lệnh `python3 -B tmp/h1/kiem_ke_mau.py tmp/w/ops/ci_duong_nhanh_test.py` (log `out/h1d-kiem-ke-mau.log`): mọi `except` bắt lớp ngoài
`LOP_RIENG_BO_TEST` nằm trong `_bat_ha_tang`, `_trong_luc_xu_ly`, `chay_ca_trong_tien_trinh`, `mot`, `main` (harness),
`lease_that_het_han_hop_le` (chỉ gọi `lease_publish`, không gọi mã bị đột biến), `t99a` (`except AssertionError: lop = type(e)`), `t23b`
(`except FixtureNuotLoiLa: pass`); `suppress` duy nhất là `suppress(TinHieuChotCa)` ở `y15`; 0 `return` trong `finally`. ⇒ lỗ là
TIỀM ẨN: không đột biến nào trong 317 bị tín dụng sai qua các dạng D*.

**Kết luận đối chiếu F1:** phần lượt 17 CHỈ RA (hai ca `t06`/`t20ze` đổi lớp dựng sẵn; `except` đổi kiểu HẸP lọt `t99`) **ĐÃ VÁ THẬT**
(H1a, dòng S2 của H1b). Nhưng bản vá thay lời khai cũ bằng lời khai MỚI lại rộng hơn chốt: "Sáu đường vào, mỗi đường có chốt" và
"lỗi vô can … ⇒ TIN_DUNG_GIA, ở MỌI ca" — đo được đường 3 (biến cờ trong MỘT hàm), 4 (giá trị trả về), 6 (đổi thành lớp riêng) và 1
(tín hiệu phát ngoài `bang()` bằng cất sẵn/luồng khác) đều có dạng tự nhiên mà `t99` không bắt, và ở lời gọi về sau thì phép tiêm cũng
không bắt (H1c). Trạng thái lớp: **VÁ HỜ** (vá đúng chỗ được chỉ; lớp gốc "lời khai rộng hơn chốt" tái sinh ở lời khai mới) — finding
F1' bên dưới.

## ĐỐI CHIẾU LƯỢT TRƯỚC — phần 2: F2 `chu-thich-khai-rong-hon-ma-con-sot` (năm câu) ⇒ **ĐÃ VÁ THẬT**
Lệnh `python3 -B tmp/f2/f2.py tmp/w` (log `out/f2-doi-chieu.log`):
```
(a) docstring kiem_mode_git co 'Hai chot doc GIT (`kiem_diff_check`, `kiem_nhi_phan`)': True | cau cu '... đọc ĐĨA' con: False
    gitlink: diff --check rc = 0 | numstat = '1\t0\tops/specs/con'
(b) module docstring neu so chuoi Actions KHONG phan biet hoa thuong: True | ci.yml: True | (khong chay lai bo danh gia @actions/expressions o luot nay)
(c) kiem_lease 'D2 la hanh vi chu kho DA DUYET': True | cau cu 'còn mở' con: False
(d) if: cua buoc `che do` = "${{ github.event_name != 'pull_request' }}" | comment moi neu 'KHONG o pull_request': True
    job gate/gate-ops/gate-packet-loop: needs='chuan-bi', if cap job=None (=> chuan-bi do o push/dispatch thi ba job skipped)
(e) thay_regex dong nhat -> 'x = 1\n' (khong nem) | docstring moi neu: True
```
| # | Câu lượt 17 | Bản vá lượt 18 | Trạng thái |
|---|---|---|---|
| a | "Mọi chốt nội dung khác của kiem-re đọc ĐĨA" | tách chốt đọc ĐĨA khỏi hai chốt đọc GIT; kho git tạm: gitlink ⇒ `--check` rc=0, numstat `1 0` (khớp câu mới) | ĐÃ VÁ THẬT |
| b | "Chỉ MỘT giá trị … mọi giá trị lạ ⇒ đầy đủ" | nêu so chuỗi Actions không phân biệt hoa thường, tệp chỉ ghi chữ thường (`t16`) — ở module và `ci.yml` | ĐÃ VÁ THẬT (đối chiếu số đo `@actions/expressions` lượt 17; KHÔNG chạy lại bộ đánh giá ở lượt này) |
| c | "D2 … còn mở" | "D2 là hành vi chủ kho ĐÃ DUYỆT" | ĐÃ VÁ THẬT |
| d | "`exit 1` ⇒ PR bị CHẶN trên MỌI sự kiện" | "chỉ chạy ở push/workflow_dispatch … gate của master mất" — khớp `if:` đọc từ YAML | ĐÃ VÁ THẬT |
| e | "kiểm bản đột biến KHÁC bản gốc" | "`thay_mot` còn kiểm …, `thay_regex` thì không" — khớp hành vi đo | ĐÃ VÁ THẬT |
Không câu nào trong năm câu sinh lỗi mới (H0: mã `ops/ci_duong_nhanh.py` và cấu trúc YAML không đổi). Câu MỚI mà lượt 18 viết thêm được
đo ở F1' (lời khai về chốt tín hiệu) và H6.

## BẢNG LỚP

| Slug | Gốc lớp | Biểu hiện trên aad37ad | Hạng | Trạng thái so lượt 17 |
|---|---|---|---|---|
| `tin-hieu-chot-ca-khong-doc-quyen` (F1') | Lời khai về độc quyền tín hiệu/đổi kiểu RỘNG hơn chốt cưỡng chế; chốt tĩnh là danh sách CẤM theo hình dạng (S1–S5) — đúng bệnh CLAUDE.md "danh sách CẤM không bao giờ đủ — phải đảo thành danh sách CHO PHÉP" | hai ca lượt 17 ĐÃ VÁ (H1a); chốt chạy ở `bang()` đóng đường 2 (H1b dòng S2). Nhưng 9 dạng đổi kiểu (5 tự nhiên: nuốt+mặc định, cờ trung gian, `suppress`, tham số ra, `return` trong `finally`; đổi thành lớp riêng; 3 cố ý: tín hiệu cất sẵn, luồng khác, `__new__`/thẻ qua chuỗi) lọt `t99` (H1b, H6); đặt ở lời gọi về sau thì lọt cả phép tiêm ⇒ GIẾT GIẢ đo được (H1c). Lời khai "Sáu đường vào, mỗi đường có chốt", "ở MỌI ca", "CHỈ `bang()` dựng được … kể cả qua bí danh", "Đường DUY NHẤT phát" đều rộng hơn mã. 0/317 đột biến bị ảnh hưởng hôm nay (H1d) | **P3** (chủ kho có thể nâng P2: CLAUDE.md gọi phản chứng "mutant chết vì AttributeError qua `except` đổi kiểu ⇒ TÍN DỤNG GIẢ" là BẮT BUỘC) | **VÁ HỜ** — vá đúng hai chỗ được chỉ, lớp gốc tái sinh ở lời khai mới |
| `tiem-vo-can-vang-mat-van-xanh` (F3) | Chốt MỚI (phép tiêm — phản chứng bắt buộc của lớp trên) không có đột biến/ca canh: "cổng VẮNG MẶT trông giống cổng xanh" (CLAUDE.md); "cửa không có mutant là cửa sẽ âm thầm hở lại" | gỡ lời gọi phép tiêm / bỏ điểm `ma` / nới phân hạng ⇒ 3/3 SỐNG, `TONG: DAT` (H2); `cham N/N` thoả bằng điểm `bang` một mình nên không đo điểm dò mã | **P3** | MỚI ở lượt 18 (executor tự khai một phần ở (c); đo được nặng hơn lời khai) |
| `chu-thich-khai-rong-hon-ma-con-sot` (F2 lượt 17) | (lượt 17) | năm câu ĐÃ VÁ THẬT (phần 2 đối chiếu) | — | **ĐÃ VÁ THẬT** |
| `kiem-mode-git-chot-khong-rang` | lớp đã DỪNG theo S3 lease g4 | 0 phát hiện mới (lượt 18 không đổi mã sản phẩm, H0; `t20zh` trong 104/104) | — | lớp đã dừng |
| `chot-yaml-chi-do-su-hien-dien` | nợ #694 | 0 phát hiện mới (`ci.yml` chỉ đổi chú thích, YAML ≡) | — | nợ #694 |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | nợ #694 | 0 phát hiện tính P: số trong lời khai commit (`104/104`, `317/317`, `99/99`, `4 muc TU_KIEM_DOT_BIEN moi` ⇒ 7) khớp output (nền); docstring không ghim số (`t98`) | — | nợ #694 |
| QUAN SÁT | — | (i) `t20ze`/`t91`/phần `__main__` của `t93` đọc mã thoát tiến trình con nên mọi thất bại riêng đường đích là GIẾT — đúng thiết kế, 0 tín dụng sai hôm nay (H1a T2, H3); (ii) chú thích `MA_TIEM_VO_CAN` "mỗi điểm tiêm chỉ nổ ở lời gọi ĐẦU TIÊN" sai cho điểm `ma` (nổ ở MỌI lời gọi hàm mã) — sai theo chiều VÔ HẠI (khai hẹp hơn) | quan sát | — |
| QUAN SÁT (đo) | — | (ii) đo `python3 -B tmp/h1/rig_ma_moi_lan.py tmp/w` (log `out/quan-sat-ma-moi-lan.log`): `t01` nuốt mọi lời gọi trong vòng ⇒ `diem ma: rc=4 so dong TIEM_VO_CAN_NO = 5` · `diem bang: rc=4 so dong TIEM_VO_CAN_NO = 1` — điểm `ma` nổ ở MỌI lời gọi, điểm `bang` chỉ lần đầu | quan sát | — |

## BẢNG SĂN (theo thứ tự có kết quả; H0, H1a–H1d ở trên; mỗi hướng: giả thuyết / lệnh / output thật / kết luận)

### H2 — Hở TỰ KHAI (c): phép tiêm và đối chứng `t20ze` có ĐỘT BIẾN/ca canh không? ⇒ **phép tiêm: KHÔNG (3/3 đột biến tự viết SỐNG, suite XANH); đối chứng `t20ze`: CÓ răng (qua `TU_KIEM_DOT_BIEN`)**
- **Giả thuyết:** phép tiêm chỉ được gọi từ `tu_kiem_phan_hang`; không ca `CA` hay mục `DOT_BIEN` nào chạm `tiem_vo_can_moi_ca_dich`/
  `DIEM_TIEM`/`chay_tiem_vo_can` (`grep`: chỉ dòng 3489 gọi) ⇒ gỡ/nới nó thì không gì đỏ — đúng bệnh "cổng VẮNG MẶT trông giống cổng xanh".
- **Lệnh:** bốn clone đột biến dựng bằng `tmp/hc/dung_dot_bien.py` (neo `count == 1`), mỗi clone chạy TRỌN suite
  `tmp/bin/chay_suite.sh` (log `out/hc/<tên>.log`).
- **Output thật** (trích các dòng tổng kết):
```
m1_go_lenh_goi_tiem    (xoa `loi += tiem_vo_can_moi_ca_dich()`)  : CA: 104/104 · DOT BIEN: 317/317 · (KHONG co dong TIEM VO CAN) · TU KIEM PHAN HANG: DAT · TONG: DAT · RC=0
m2_bo_diem_tiem_ma     (DIEM_TIEM = ("bang",))                   : TIEM VO CAN: 99 ca dich x 1 diem tiem: TIN_DUNG_GIA=99 · cham 99/99 ca · doi chung ...: GIET · TU KIEM: DAT · TONG: DAT · RC=0
m3_phan_hang_tiem_long (`elif not (SONG_SOT and not no)` -> `elif hang == "GIET"`): TIEM VO CAN: ... SONG_SOT=32 · TIN_DUNG_GIA=166 · cham 99/99 · GIET · TONG: DAT · RC=0
m5_go_doi_chung_t20ze  (xoa khoi doi chung UTF-8 cua t20ze)      : TU KIEM PHAN HANG: DO · [TU KIEM] tu kiem vo_can_UnicodeError_dich_t20ze: mong TIN_DUNG_GIA, duoc GIET · TONG: DO · RC=1
```
- **Kết luận:** đúng như executor tự khai cho phép tiêm, và đo được nặng hơn lời khai: (i) gỡ HẲN lời gọi phép tiêm ⇒ `TONG: DAT`;
  (ii) bỏ điểm `ma` — điểm DUY NHẤT dò mã bị đột biến — vẫn in `cham 99/99 ca`, vì điểm `bang` (lời gọi `bang()` đầu tiên, có ở mọi ca)
  một mình đủ thoả điều kiện "chạm"; tức dòng `cham N/N` đếm SỰ CÓ MẶT của điểm tiêm, không đo điểm dò mã; (iii) nới phân hạng ⇒ XANH.
  Đối chứng `t20ze` thì CÓ răng (m5 ⇒ `TONG: DO`) — phần tự khai về `t20ze` hẹp hơn thực tế, theo chiều vô hại. Finding F3 bên dưới.

### H3 — Hở TỰ KHAI (b): crash vô can trong mã harness mà tiến trình con chạy (`t91`/`t93`) thành ĐỎ qua rc ⇒ **đúng, nhưng 0 tín dụng sai hôm nay; theo thiết kế**
- **Lệnh:** `python3 -B tmp/hb/rig_b.py tmp/w` (log `out/hb-dich-tien-trinh-con.log`): chạy lại MỌI đột biến hiện có đích `t91`/`t92`/
  `t93`/`t06`/`t20ze`/`t23b` bằng `chay_con` của HEAD, giữ NGUYÊN dòng `DO:` để đọc lý do chết; cộng hai đột biến TỰ VIẾT: `{}.vo_can`
  (AttributeError) trước dòng `CA:` của `main`, và `[].vo_can` đầu `loi_cay_duoi_do`, đích `t91`.
- **Output thật** (trích; mỗi dòng: tên · đích · hạng · dòng `DO:` rút gọn):
```
fail_open_dau_ra_khong_phai_bytes   t06  GIET | DO:t06…:dau ra khong phai bytes (memoryview doi duoc ra bytes): phai la day_du (fail-close), duoc 'duong_nhanh'
test_main_ok_luon_dung              t93  GIET | DO:t93…:main/mot ca do: rc=0 mong 1, dong cuoi ['TONG: DAT']
test_runner_nuot_tin_hieu_do        t91  GIET | DO:t91…:entry/DO: rc=0, stdout='REVIEW_SENTINEL_CALLED\nCA: 1/1 dat …
test_entrypoint_rc1_thanh_0         t91  GIET | DO:t91…:entry/DO: rc=0, stdout='REVIEW_SENTINEL_CALLED\n[DO] t_fixture: review sentinel …
mode_git_raw_giai_ma_chat           t20ze GIET | DO:t20ze…:PR ten tep khong UTF-8 phai DAT kiem-re (tien trinh con, doi chung UTF-8 da DAT): rc=1: …
test_fixture_nuot_loi_khong_ghi     t23b GIET | DO:t23b…:loi VO CAN (lp.kiem nem AttributeError) bi doi thanh KhongCoFixture — t23 se cap GIET: …
TU_VIET_crash_vo_can_trong_main_truoc_dong_CA  t91 GIET | DO:t91…:entry/DAT: rc=1, stdout='REVIEW_SENTINEL_CALLED\n', stderr='…mExit(main(sys.argv[1:]))…
TU_VIET_crash_vo_can_trong_loi_cay_duoi_do     t91 GIET | DO:t91…:entry/DAT: rc=1, stdout='', stderr='…OT_THAT)…
```
  (22 đột biến hiện có × đích = 24 cặp, cả 24 `GIET` bằng ĐÚNG assertion của ca — đọc dòng `DO:` từng cặp ở log; hai dòng TU_VIET là
  crash vô can trong tiến trình con ⇒ GIẾT.) Bổ sung `python3 -B tmp/hb/rig_t93.py tmp/w` (log `out/hb-t93.log`): crash vô can
  (`{}.vo_can`) CHỈ khi `argv == ['doi-so-la']`, đích `t93` ⇒ `('GIET', '')` — phần `__main__` của `t93` cũng đếm crash là GIẾT.
- **Kết luận:** hôm nay 0 đột biến đích `t91`/`t93` được tín dụng nhờ crash; lỗ là TIỀM ẨN và theo thiết kế (tính chất `t91` là "mã thoát
  và dòng TONG đúng" — crash LÀ vi phạm). Không tính P riêng; nhưng nó làm lời khai "ở MỌI ca" của docstring module sai (gộp vào F1').
  Bên lề: `t06` nay chết bằng QUYẾT ĐỊNH (`memoryview` ⇒ `duong_nhanh`), không còn qua đường đổi kiểu — lời khai chú thích `t06` ĐÚNG.

### H6 — Lời khai mới "CHỈ `bang()` dựng được `TinHieuChotCa` … kể cả qua bí danh/chuỗi" (docstring lớp, dòng 105–106) ⇒ **SAI cho `__new__` và thẻ thật lấy qua chuỗi**
- **Lệnh:** `python3 -B tmp/h1/rig_dung.py tmp/w` (log `out/h6-dung-ngoai-bang.log`), mẫu đặt quanh lời gọi mã đầu của `t01`, lỗi vô can
  `raise AttributeError` đầu `phan_loai_tu_diff`:
```
D1b __new__ qua bi danh (lop = type(e))
   [nen t01 rc=0] [t99 rc=0] [t99a rc=0] -> loi VO CAN: t01 GIET ['DO:t01_toan_ho_so_duong_nhanh:ops/land/x.yaml: dung qua __new__']
D1c the THAT lay qua chuoi trong globals()
   [nen t01 rc=0] [t99 rc=0] [t99a rc=0] -> loi VO CAN: t01 GIET ['DO:t01_toan_ho_so_duong_nhanh:ops/land/x.yaml: the that']
```
- **Kết luận:** thẻ `_THE_BANG` chỉ chặn đường qua `__init__`; `lop.__new__(lop)` với `lop = type(e)` (đúng cách `t99a` tự lấy bí danh)
  và `globals()['_THE' + '_BANG']` đều dựng được tín hiệu, `t99`/`t99a` im. Đây là dạng CỐ Ý (không ai viết nhầm), nên chỉ tính như
  một mục của lời khai rộng hơn chốt (F1'); chốt đúng cho nó không phải thêm thẻ mà là chặn chỗ NUỐT lỗi dựng sẵn (S6 trong hint).

### H4 — Đúng đắn đường nhanh: có bằng chứng MỚI để mở lại không? ⇒ **KHÔNG**
- **Lệnh/căn cứ:** H0 (`ast.dump` bỏ docstring của `ops/ci_duong_nhanh.py` 98377f8 ≡ aad37ad; cấu trúc YAML `ci.yml` đã parse ≡) +
  numstat bản vá lượt 18 (mọi thay đổi mã nằm trong `ops/ci_duong_nhanh_test.py`) + suite HEAD `CA 104/104` (gồm mọi ca hành vi `t*`
  và cấu trúc `y*`/`k*` cũ, không ca hành vi nào bị đổi kỳ vọng — diff lượt 18 chỉ đổi CÁCH báo đỏ của `t06`/`t11b`/`t11c`/`t11d`/`t17`/
  `t20s`/`t20zb`/`t23` từ `raise TinHieuChotCa` sang `bang(False, …)` cùng điều kiện, và `t20ze` sang tiến trình con có đối chứng).
- **Kết luận:** hành vi sản phẩm và `ci.yml` không đổi so lượt 17; kết luận H5 lượt 17 (bốn ca `kiem-re` phủ bốn lối đọc hồ sơ thật)
  đứng nguyên. Không mở lại.

### H5 — Nghiệm thu 10 và manifest trên HEAD ⇒ **ĐÚNG**
| Lệnh | Output thật |
|---|---|
| `PYTHONUTF8=1 python3 -B scripts/tl.py --selftest` (clone RIÊNG `tmp/tl` @aad37ad vì lệnh này ghi `scripts/.tl_state/`; log `out/nen/tl-selftest-head.log`) | `== tl selftest 1715/1715 ==` · 0 dòng `[FAIL]` · `rc=0` · 244 s |
| `python3 -m ruff check --no-cache --select F scripts/tl.py` · `git diff --quiet origin/master HEAD -- scripts/tl.py` | `Found 12 errors.` (= nền 12 F821 của CLAUDE.md) · rc=0 ⇒ tệp KHÔNG đổi ⇒ delta = 0 |
| `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` (clone `tmp/w`) | `ok: True` · `expected_file_count 180` = `checked_file_count 180` · `failed 0` · `errors 0` · `extra_files 0`; `grep` manifest: 0 mục dưới `.github/` hay `ops/` (lượt 18 chỉ đổi hai vùng ấy) |

### H7 — Parity Python: CI ghim `python-version: "3.12"` cho job chạy `python ops/ci_duong_nhanh_test.py` (ci.yml dòng 630–666), nền đo ở trên là 3.11.15 ⇒ **KHỚP**
- **Giả thuyết:** chốt mới của lượt 18 dựa trên ngữ nghĩa `sys.exc_info()` trong `except`/`finally` (`bang()`, `t99b`) — phải chạy THẬT
  trên phiên bản CI ghim, không suy từ 3.11.
- **Lệnh:** `tmp/bin/chay_suite312.sh tmp/w out/nen/suite-head-py312.log` (`/usr/bin/python3.12` 3.12.3, mọi tiến trình con theo
  `sys.executable`); `/usr/bin/python3.12 -B tmp/h1/rig_sau.py tmp/w` (log `out/h1c-lan-goi-sau-py312.log`).
- **Output thật:** `CA: 104/104 dat · 0 do · 0 hong` · `DOT BIEN: 317/317 bi giet dung ly do` · `TIEM VO CAN: 99 ca dich x 2 diem tiem:
  SONG_SOT=32 · TIN_DUNG_GIA=166 · cham 99/99 ca · … GIET` · `TU KIEM PHAN HANG: DAT (5 mau rc, 7 dot bien that)` · `TONG: DAT` · `RC=0`
  · 154 s. Rig H1c dưới 3.12: bốn dòng y hệt 3.11 (hai `GIET` giả, hai đối chứng `TIN_DUNG_GIA`).
- **Kết luận:** HEAD và finding F1' giống nhau trên 3.11.15 và 3.12.3 (số đếm bằng nhau từng mục).

## FINDINGS

### tin-hieu-chot-ca-khong-doc-quyen [P3] (F1') Lời khai mới "Sáu đường vào, mỗi đường có chốt" / "ở MỌI ca" / "CHỈ `bang()` dựng được" rộng hơn chốt: chốt tĩnh là danh sách CẤM theo hình dạng, chín dạng đổi kiểu lọt, và ở lời gọi về sau phép tiêm cũng lọt ⇒ GIẾT GIẢ đo được
**TỆP/DÒNG:** `ops/ci_duong_nhanh_test.py:16-27` (docstring module: "CHỈ `bang()` dựng được lớp ấy", "ở MỌI ca", "Sáu đường vào, mỗi
đường có chốt: … (3) đổi kiểu qua biến cờ trong một hàm (luật S3, chỉ tĩnh) · (4) … · (6) … (`t23b`)") · `:105-106` (docstring
`TinHieuChotCa`: "CHỈ `bang()` dựng được … kể cả qua bí danh/chuỗi") · `:138-139` (`bang`: "Đường DUY NHẤT phát") · `:2611-2688`
(`quet_doi_kieu_tin_hieu` S1–S5) · `:2693-2700` (`HAM_DOI_KIEU_CHO_PHEP`) · `:3395-3399` (chú thích phép tiêm).

**VẤN ĐỀ:** lượt 18 vá đúng hai ca lượt 17 chỉ ra (`t06`, `t20ze` — đo H1a) và thêm chốt CHẠY trong `bang()` có răng cho đường
`except` gọi `bang()` (H1b dòng S2). Nhưng nó thay lời khai cũ bằng lời khai MỚI lại rộng hơn chốt. Chốt tĩnh S1–S5 là một DANH SÁCH CẤM
theo hình dạng cú pháp, nên dạng tự nhiên nhất của chính đường 3 — nuốt lỗi rồi để biến giữ giá trị mặc định (`except AttributeError:
pass`) — không bị S3 bắt (S3 chỉ bắt `except` GÁN/ĐỔI một tên mà `bang()` đọc). Tương tự với cờ qua biến trung gian, `suppress`, tham số
ra (đường 4 không qua `return` trong `except`), `return` trong `finally`, đổi lỗi dựng sẵn thành `SuDoGia` rồi bắt (đường 6 ngoài helper
duy nhất `t23b` canh), tín hiệu thật cất sẵn rồi `raise`, `bang()` gọi qua luồng khác (`sys.exc_info()` là của từng luồng), và
`__new__`/thẻ thật lấy qua chuỗi. Phép tiêm chỉ che các dạng ấy khi chúng bọc lời gọi mã ĐẦU TIÊN của ca; bọc một lời gọi về sau + lỗi
vô can chỉ ở đầu vào ấy ⇒ không cổng nào bắt và lỗi VÔ CAN được đếm GIẾT (H1c) — đúng phản chứng BẮT BUỘC của CLAUDE.md
("mutant chết vì AttributeError … phải rơi vào TÍN DỤNG GIẢ kể cả khi trên đường có một `except` đổi kiểu") ở dạng chưa canh. Hôm nay
0/317 đột biến bị ảnh hưởng (H1d: tệp test không có dạng nào trên đường của mã bị đột biến) ⇒ lỗi tài liệu + lỗ TIỀM ẨN của bộ đo,
không phải con số `317/317` sai. Câu "ở MỌI ca" còn sai thêm ở các ca đọc mã thoát tiến trình con (`t20ze`, `t91`, `t93`) — ở đó crash
riêng đường đích là GIẾT theo thiết kế (H1a T2, H3).

**PHẢN CHỨNG** (chạy được, chỉ trên cây tạm của HEAD; log `out/h1b-duong.log`, `out/h1c-lan-goi-sau.log`, `out/h6-dung-ngoai-bang.log`):
```
python3 -B tmp/h1/rig_sau.py tmp/w
D3a nuot (except AttributeError: pass) o lan goi SAU | loi vo can chi khi nhieu tep (len(doi) > 1)
   [nen t01 rc=0] [t99 rc=0] [tiem ma=TIN_DUNG_GIA+no · bang=TIN_DUNG_GIA+no] -> t01 GIET ['DO:t01_toan_ho_so_duong_nhanh:bon tien to ho so cung mot PR phai la duong nhanh']
D6 doi thanh SuDoGia o lan goi SAU | loi vo can chi khi nhieu tep (len(doi) > 1)
   [nen t01 rc=0] [t99 rc=0] [tiem ma=TIN_DUNG_GIA+no · bang=TIN_DUNG_GIA+no] -> t01 GIET ['DO:t01_toan_ho_so_duong_nhanh:bon tien to: loi: vo can']
python3 -B tmp/h1/rig_duong.py tmp/w   (9 dang D* : [t99 rc=0] o ca chin; xem H1b)
python3 -B tmp/h1/rig_dung.py tmp/w    (D1b __new__ qua bi danh, D1c the that qua chuoi: [t99 rc=0] [t99a rc=0] -> GIET)
```

**HINT** (`HINT.patch`, chỉ `ops/ci_duong_nhanh_test.py`, trong write set): đảo chốt tĩnh thành DANH SÁCH CHO PHÉP — luật **S6** của
`quet_doi_kieu_tin_hieu`: MỌI chỗ nuốt được lỗi dựng sẵn bằng cú pháp (`except` bắt lớp ngoài `LOP_RIENG_BO_TEST` và ngoài hai lớp tín
hiệu của bộ đo, trừ khi thân kết thúc bằng `raise` trần; `suppress(...)` lớp ngoài các tập ấy; `return`/`break`/`continue` trong
`finally`) chỉ được nằm trong hàm thuộc `HAM_DOI_KIEU_CHO_PHEP` (thêm hai ca tự kiểm dùng có chủ đích: `t99a`, `t23b`, mỗi ca một lý
do); 9 mẫu `MAU_DOI_KIEU` mới (mỗi dạng D* đo được một mẫu) + đối chứng "ném lại nguyên lỗi" phải SẠCH; mẫu đối chứng cũ "except ngoài
bộ test không chạm bang" đổi thành mẫu S6 (theo danh sách cho phép, nó KHÔNG còn sạch). Sửa lời khai cho khớp đo: docstring module,
`TinHieuChotCa`, `bang`, `quet_doi_kieu_tin_hieu`, chú thích phép tiêm — nêu rõ thẻ không chặn `__new__`/thẻ qua chuỗi, chốt chạy chỉ
trong CÙNG luồng, các ca đọc mã thoát tiến trình con, và phần còn lọt (nuốt KHÔNG qua cú pháp: `Future.exception()`, excepthook của
luồng, `__exit__` tự viết trả True, `gather(return_exceptions=True)`). Biên BẢO THỦ của S6 (khai): mọi `break`/`continue`
trong thân `finally` đều bị tính là nuốt lỗi, kể cả khi nằm trong vòng lặp riêng của `finally`; `except X as e: raise e` (không
trần) cũng bị bắt — tệp hiện tại không có chỗ nào như vậy (`t99` sạch trên tệp thật sau khi áp), người giữ có thể tinh chỉnh.

**ĐỘT BIẾN đo răng** (trong hint, mỗi nhánh của S6 một đột biến riêng, đích `t99`): `test_t99_bo_luat_S6_except` ·
`test_t99_bo_luat_S6_suppress` · `test_t99_bo_luat_S6_finally` · `test_t99_S6_mien_moi_raise` (nới miễn trừ "ném lại nguyên" thành
"mọi `raise`" ⇒ mẫu đổi thành lớp riêng phải lộ) · `test_t99_S6_noi_cho_phep_ten_tan_cong` (nới danh sách cho phép chứa tên tấn công —
chốt CLAUDE.md đòi cho mọi danh sách cho phép) · `test_chen_nuot_vao_lan_goi_sau_cua_t01` (chính dạng H1c). Kết quả đo ở mục ĐO HINT.
Đo lại các rig trên bản ĐÃ ÁP hint (log `out/hint/h1b-duong-sau-hint.log`, `out/hint/h1c-sau-hint.log`, `out/hint/h6-sau-hint.log`):
cả 11 dạng H1b, 2 dạng H1c và 2 dạng H6 đều `[t99 rc=3 => BAT]` — tức dạng ấy KHÔNG vào được tệp test mà suite còn xanh.

**ĐỘ TIN:** cao (đo trên harness thật, đối chứng có răng ở mỗi rig); tác động hôm nay 0, tác động tiềm ẩn: con số `DOT BIEN: M/M bị
giết ĐÚNG LÝ DO` phồng được bằng một dạng nuốt lỗi tự nhiên mà không cổng nào đỏ.

### tiem-vo-can-vang-mat-van-xanh [P3] (F3) Phép tiêm lỗi vô can — phản chứng bắt buộc mới của lượt 18 — gỡ đi, bỏ điểm dò mã, hay nới phân hạng đều để suite XANH
**TỆP/DÒNG:** `ops/ci_duong_nhanh_test.py:3400` (`DIEM_TIEM`) · `:3434-3466` (`tiem_vo_can_moi_ca_dich`) · `:3489` (lời gọi duy nhất,
trong `tu_kiem_phan_hang`).

**VẤN ĐỀ:** không ca `CA` hay mục `DOT_BIEN` nào chạm phép tiêm; `t93`/`t94` thay `tu_kiem_phan_hang` bằng đồ giả. Nên ba đột biến tự
viết đều SỐNG với `TONG: DAT` (H2): gỡ lời gọi (dòng `TIEM VO CAN:` biến mất mà không ai hỏi), bỏ điểm `ma` (điểm DUY NHẤT dò mã bị đột
biến; dòng vẫn in `cham 99/99 ca` vì điểm `bang` có ở mọi ca), nới phân hạng (HONG và SONG_SOT-có-nổ không còn là lỗi). Executor tự khai
"không có đột biến bảng cho tiêm và đối chứng t20ze"; đo được: nửa `t20ze` thật ra CÓ răng (m5 ⇒ `TONG: DO` qua `TU_KIEM_DOT_BIEN`),
nửa phép tiêm thì hở nặng hơn lời khai (dòng `cham N/N` đếm SỰ CÓ MẶT của điểm tiêm, không đo điểm dò mã). Đúng hai bài học CLAUDE.md:
"cổng VẮNG MẶT trông giống cổng xanh" và "cửa không có mutant là cửa sẽ âm thầm hở lại".

**PHẢN CHỨNG** (chạy được; clone đột biến `tmp/hc/<tên>`, log `out/hc/<tên>.log`):
```
m1_go_lenh_goi_tiem    : CA: 104/104 · DOT BIEN: 317/317 · TU KIEM PHAN HANG: DAT · TONG: DAT · RC=0  (khong co dong TIEM VO CAN)
m2_bo_diem_tiem_ma     : TIEM VO CAN: 99 ca dich x 1 diem tiem: TIN_DUNG_GIA=99 · cham 99/99 ca · … GIET · TONG: DAT · RC=0
m3_phan_hang_tiem_long : TIEM VO CAN: … · cham 99/99 ca · … GIET · TONG: DAT · RC=0
```

**HINT** (`HINT.patch`): ca tự kiểm `t99c_phep_tiem_vo_can_chay_du_diem_va_phan_hang_dung` đo bằng đồ giả, không tiến trình con: (1)
`tu_kiem_phan_hang` phải gọi phép tiêm và giữ lỗi nó trả; (2) phép tiêm phải chạy MỌI ca đích × CẢ HAI điểm `ma`/`bang`; (3) GIET, HONG,
SONG_SOT-có-nổ ở một (ca, điểm) ⇒ lỗi; toàn TIN_DUNG_GIA-có-nổ ⇒ rỗng. Kèm ba mục `DOT_BIEN` đích `t99c` = đúng m1/m2/m3 ở trên.

**ĐỘT BIẾN đo răng:** m1/m2/m3 thành mục `DOT_BIEN` (`test_tu_kiem_khong_goi_tiem`, `test_tiem_bo_diem_ma`, `test_tiem_phan_hang_long`)
— hôm nay SỐNG (đo), trên bản đã áp phải GIẾT (mục ĐO HINT).

**ĐỘ TIN:** cao; tác động: phản chứng bắt buộc của lớp F1' có thể biến mất trong một lần sửa mà cổng vẫn xanh.

## ĐO HINT (`R/HINT.patch`, 221 dòng, sha256 `0e3fee25b6b329a284ba770b7ef837b819f47982b47a974f6a64bd1a09234a3e`, 1 tệp: `ops/ci_duong_nhanh_test.py` — trong write set)
Dựng: `tmp/hint/dung_hint.py` + `tmp/hint/sua_neo.py` trên clone `tmp/hint/cay` (lần dựng đầu có ba neo đột biến KHÔNG duy nhất vì neo
xuất hiện nguyên văn trong chính dòng `DOT_BIEN` — sửa bằng nối chuỗi như các mục sẵn có; khai ra đây vì đó đúng là lỗi hạ tầng mà
`thay_mot` sinh ra để bắt). Đo trên clone MỚI `tmp/hint/ap` dựng từ `kho.git` tại `aad37ad2cd129943cac578a48f0ee377e58439c6`:

| Phép đo | Output thật |
|---|---|
| `git apply --check HINT.patch` rồi `git apply` | `apply_check_rc=0` · `apply_rc=0` · `cmp` với bản soạn ⇒ GIỐNG |
| `git diff --numstat HEAD` (đã áp) · `git diff --numstat origin/master` | `116 24 ops/ci_duong_nhanh_test.py` · vẫn đúng 4 tệp write set, `1 0 .claude/dev/ci_dang_ky_test.py` (hint không chạm) |
| `python3 -B ops/ci_duong_nhanh_test.py` (đã áp; log `out/hint/suite-ap.log`) | `CA: 105/105 dat · 0 do · 0 hong` · `DOT BIEN: 326/326 bi giet dung ly do` · `KIEM KE: ca hanh_vi=74 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=12 = 105 · dot bien … ops/ci_duong_nhanh_test.py=68 = 326` · `TIEM VO CAN: 100 ca dich x 2 diem tiem: SONG_SOT=33 · TIN_DUNG_GIA=167 · cham 100/100 ca · doi chung co rang …: GIET` · `TU KIEM PHAN HANG: DAT (5 mau rc, 7 dot bien that)` · `TONG: DAT` · `RC=0` · 151 s |
| Lý do chết của 9 đột biến MỚI (`tmp/hint/rig_ly_do.py`, log `out/hint/ly-do-dot-bien-moi.log`) | mỗi mục chết bằng ĐÚNG mẫu/chốt nó gỡ: `S6_except` ⇒ `mau 'S6 except ngoai bo test …' phai bi luat S6 bat, duoc []` · `S6_suppress` ⇒ mẫu `suppress` · `S6_finally` ⇒ mẫu `return trong finally` · `S6_mien_moi_raise` ⇒ mẫu `doi thanh lop rieng` · `S6_noi_cho_phep` ⇒ mẫu `helper ghi tham so ra` · `chen_nuot_vao_lan_goi_sau_cua_t01` ⇒ `['S6 dong 276: except AttributeError nuot loi dung san …']` · `tu_kiem_khong_goi_tiem` ⇒ `tu_kiem_phan_hang phai goi phep tiem …, duoc []` · `tiem_bo_diem_ma` ⇒ `thieu [('k01…', 'ma'), …]` · `tiem_phan_hang_long` ⇒ `mot HONG: loi cua phep tiem phai KHAC RONG, duoc []` |
| Rig H1b/H1c/H6 chạy lại trên bản đã áp (log `out/hint/h1b-duong-sau-hint.log`, `h1c-sau-hint.log`, `h6-sau-hint.log`) | 11/11 mẫu H1b, 2/2 mẫu H1c, 2/2 mẫu H6: `[t99 rc=3 => BAT]` (trước hint: 9/11, 0/2, 0/2) |
| Cùng suite dưới `/usr/bin/python3.12` (3.12.3 — bản CI ghim; `tmp/bin/chay_suite312.sh tmp/hint/ap`, log `out/hint/suite-ap-py312.log`) | `CA: 105/105 dat · 0 do · 0 hong` · `DOT BIEN: 326/326 bi giet dung ly do` · `TIEM VO CAN: 100 ca dich x 2 diem tiem: SONG_SOT=33 · TIN_DUNG_GIA=167 · cham 100/100 ca · … GIET` · `TU KIEM PHAN HANG: DAT (5 mau rc, 7 dot bien that)` · `TONG: DAT` · `RC=0` · 158 s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` (đã áp) | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` (shellcheck có mặt) · `ruff --select F` hai tệp · `doctrine-scan` | rc=0 · `All checks passed!` rc=0 · `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` rc=0 |
| Delta HAI VẾ dựng trong MỘT lệnh (`tmp/delta/hai_ve.sh`: hai clone mới cùng SHA, cùng bước; vế `sau` áp `HINT.patch`; cùng rig `rig_sau.py` + `rig_dung.py`; log `out/hint/delta-hai-ve.log`) | vế `nen` (numstat rỗng): 6/6 dòng `[t99 rc=0]` (2 mẫu × 2 lỗi của H1c + 2 mẫu H6) · vế `sau` (`116 24 ops/ci_duong_nhanh_test.py`): 6/6 dòng `[t99 rc=3 => BAT]`; cột "lỗi VÔ CAN ⇒ hạng" giống hệt hai vế (đúng: rig đo HẬU QUẢ nếu dạng ấy có mặt; hint chặn dạng ấy ở `t99` trên tệp THẬT, nên nó không vào được tệp mà suite còn xanh) |

Hint chỉ chạy trên BẢN SAO; executor phải tự áp, tự đo, tự commit. Hint KHÔNG đổi mã sản phẩm, `ci.yml` hay `ci_dang_ky_test.py`.

## KHÔNG ĐO ĐƯỢC (nói thẳng)
- Actions thật: PR thật (nghiệm thu 11), merge ref/`github.sha` thật, bộ đánh giá biểu thức của runner. Câu (b) của F2 dựa trên số đo
  `@actions/expressions@0.3.61` của lượt 17 + tài liệu GitHub; lượt này KHÔNG chạy lại bộ đánh giá.
- Windows: không có runner Windows; selftest packet chỉ chạy trên Linux ở đây (3.11.15 và 3.12.3).
- Chữ ký commit `aad37ad` (`%G?` = N vì sandbox thiếu `gpg.ssh.allowedSignersFile`) — không xác minh được chữ ký.
- `doc-claims-check` không chạy lượt này (lượt 18 và hint chỉ đổi `ops/`, chú thích `ci.yml`, docstring); `release-verify --strict` có chạy (H5).
- Model/effort thật của lượt review này (tự khai Opus 5.5 / max, không có receipt runtime).
- Dạng nuốt lỗi KHÔNG qua cú pháp (`Future.exception()`, excepthook của luồng, `__exit__` tự viết trả True, `gather(return_exceptions=True)`):
  không dựng phản chứng cho từng dạng; hint khai chúng là phần còn lọt thay vì khẳng định đã đóng.

## TÁC ĐỘNG NGOÀI SANDBOX (khai)
- `R/cay` không bị chạy lệnh ghi nào: chỉ đọc (`git -C cay log/show/diff/rev-parse/status` với `GIT_OPTIONAL_LOCKS=0`, `grep`/`sed`/đọc
  tệp, `diff -rq cay tmp/w`). `GIT_OPTIONAL_LOCKS=0 git -C cay status --short --ignored` ⇒ 0 dòng ở đầu và ở cuối lượt; HEAD vẫn `aad37ad`.
- Mọi phép đo/đột biến chạy trên clone/bản sao trong `R/tmp/` (`w`, `tl`, `hc/m1…m5`, `hint/cay`, `hint/ap`, `delta/nen`, `delta/sau`, cây tạm
  `cdn_cay_*` do harness tự dựng/xoá trong `TMPDIR=R/tmp`). Log ở `R/out/`.
- Mọi lệnh chạy git/python đều `cd` vào `R/...` trước hoặc chỉ nhận đường dẫn tuyệt đối trong `R`; vài lệnh CHỈ ĐỌC/tạo thư mục
  (`mkdir -p R/tmp/...`, `cat` tệp output tác vụ nền ở thư mục `tasks/` của phiên, `ps`, `date`) chạy với cwd khởi tạo của shell nhưng
  không ghi gì ngoài `R`. Không lệnh git/python nào chạy trong `/home/user/tra-luat` hay worktree khác. Một lệnh `sleep` bị hệ chặn
  (không chạy). Không `pkill`; các tiến trình nền đều của lượt này và đã kết thúc (kiểm `ps` cuối lượt).
- Không commit, không push, không đăng GitHub, không chạy CI. Không cài gì (dùng công cụ sẵn có).

## KẾT LUẬN
`changes_requested` (ngưỡng chủ kho 0 P1 / 0 P2 / 0 P3). Mức bảo đảm tối đa của lượt này là `advisory_review` vì reviewer cùng họ model
với executor (Claude Opus) — packet `sensitive` vẫn cần Codex `cross_approved` hoặc `human_audited` ở cổng land.
- **Bất biến head GIỮ** (đo): đúng 4 tệp write set; `.claude/dev/ci_dang_ky_test.py` `1 0`; `ops/ci_duong_nhanh.py` AST bỏ docstring ≡
  `98377f8`; cấu trúc YAML `ci.yml` ≡; suite `CA 104/104` · `DOT BIEN 317/317` · `TIEM VO CAN 99×2, cham 99/99, đối chứng GIET` ·
  `TU KIEM DAT` · `TONG DAT` trên CẢ 3.11.15 và 3.12.3; registry `23/23` + `1025/1025`; actionlint (shellcheck có mặt) / ruff F /
  doctrine-scan sạch; `tl --selftest 1715/1715`; ruff `scripts/tl.py` delta 0; `release-verify --strict` ok 180/180.
- **Đối chiếu lượt 17:** F2 `chu-thich-khai-rong-hon-ma-con-sot` **ĐÃ VÁ THẬT** (5/5 câu). F1 `tin-hieu-chot-ca-khong-doc-quyen`:
  hai ca được chỉ (`t06`, `t20ze`) **ĐÃ VÁ THẬT** và chốt chạy trong `bang()` có răng; nhưng lời khai mới lại rộng hơn chốt (chốt tĩnh là
  danh sách CẤM theo hình dạng; 9 dạng lọt; ở lời gọi về sau thì lọt cả phép tiêm ⇒ GIẾT GIẢ đo được) ⇒ lớp **VÁ HỜ** ⇒ F1' **P3**.
- **Mới:** F3 `tiem-vo-can-vang-mat-van-xanh` **P3** — phép tiêm (phản chứng bắt buộc của F1') không có ca/đột biến canh (3/3 đột biến tự
  viết sống, `TONG: DAT`).
- **Hở tự khai:** (a) đo được ⇒ gộp F1'; (b) đúng, theo thiết kế, 0 tín dụng sai hôm nay ⇒ quan sát; (c) nửa phép tiêm ⇒ F3, nửa `t20ze`
  thật ra CÓ răng.
- **Lớp đã dừng S3 / nợ #694:** 0 phát hiện mới tính P. **Đúng đắn đường nhanh:** không có bằng chứng mới (H4).
- **Hint:** `HINT.patch` (1 tệp, trong write set, không đổi mã sản phẩm): luật S6 (danh sách CHO PHÉP) + ca `t99c` + 9 đột biến, sửa lời
  khai; áp sạch trên `aad37ad`, đã chạy (3.11.15 và 3.12.3, số bằng nhau): `CA 105/105` · `DOT BIEN 326/326` · `TIEM VO CAN 100×2, cham
  100/100, GIET` · `TU KIEM DAT` · `TONG DAT`; 9/9 đột biến mới chết đúng lý do; 15/15 mẫu (11 H1b + 2 H1c + 2 H6) bị `t99` chặn trên bản đã áp.

TONG: P0=0 P1=0 P2=0 P3=2
