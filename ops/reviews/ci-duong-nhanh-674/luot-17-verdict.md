Reviewed commit: 98377f8da2ee72978e794b6f2507ac1b8b7e5689
verdict: changes_requested
reviewed_sha: 98377f8da2ee72978e794b6f2507ac1b8b7e5689
review_class: advisory_review (reviewer cùng họ executor — Claude Opus)

> Nói thẳng: reviewer là Claude Opus 5.5 (effort max, tự khai, không có receipt runtime ⇒ model/effort thật `KHÔNG ĐO ĐƯỢC`),
> executor cũng là Claude Opus ⇒ CÙNG HỌ ⇒ lượt này là `advisory_review`, KHÔNG phải `cross_approved`. Packet `sensitive`
> vẫn cần Codex `cross_approved` hoặc `human_audited` ở cổng land.

Trạng thái: HOÀN TẤT — **changes_requested** · TONG: P0=0 P1=0 P2=0 P3=2 — P3 lượt 16 ĐÃ VÁ THẬT; quét toàn bộ chú thích/docstring
của diff packet còn 2 lớp P3 (F1 `tin-hieu-chot-ca-khong-doc-quyen`, F2 `chu-thich-khai-rong-hon-ma-con-sot`), đều không đổi hành vi
đường nhanh; lớp đã dừng S3: 0 phát hiện mới; nợ #694: 0 phát hiện tính P. Ngưỡng chủ kho 0/0/0 ⇒ chưa đạt.

## Đối tượng (đo)
- PROMPT.md sha256 `9207805a460356027edfd91c713825c676bfbb6cb34ca9dd749d7002f6bdf067` (khớp lời gọi) · SPEC-r2.md sha256
  `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` (khớp PROMPT).
- `git -C cay rev-parse HEAD` ⇒ `98377f8da2ee72978e794b6f2507ac1b8b7e5689`; cha `f9f6fb1b746381963070f7673976e0e76998d4f3`;
  `origin/master` = merge-base = `20ec8d5d0e86cb7dc01f202c7596407a957e5961`. `git -C cay status --short --ignored` RỖNG lúc mở.
- `git diff --numstat origin/master...98377f8` ⇒ đúng 4 tệp write set: `1 0 .claude/dev/ci_dang_ky_test.py` · `98 8 .github/workflows/ci.yml` ·
  `541 0 ops/ci_duong_nhanh.py` · `3137 0 ops/ci_duong_nhanh_test.py` (log `out/nen/numstat.log`). `git diff --numstat origin/master --
  .claude/dev/ci_dang_ky_test.py` ⇒ `1 0` (`out/nen/numstat-dangky.log`). Bản vá lượt 17 (`git diff --numstat f9f6fb1 98377f8`):
  `2 1 ops/ci_duong_nhanh.py` · `4 2 ops/ci_duong_nhanh_test.py` — chỉ hai docstring (`kiem_loai_tep`, `cay_t82`).

## Môi trường và số đo nền (HEAD 98377f8, chạy trong `cay/` theo PROMPT, `TMPDIR=R/tmp`; script `tmp/chay_nen.sh`)
- Linux 4 lõi, Python 3.11.15 (mặc định) + 3.12.3, git 2.43.0, actionlint 1.7.7, **shellcheck 0.9.0 CÓ MẶT**, ruff 0.15.15 (bằng
  bản CI ghim), PyYAML 6.0.1 (CI 6.0.3), node 22.22.2. Không Actions, không Windows. Chạy root.

| Lệnh | Output thật |
|---|---|
| `python3 -B ops/ci_duong_nhanh_test.py` | `CA: 101/101 dat · 0 do · 0 hong` · `DOT BIEN: 301/301 bi giet dung ly do` · `KIEM KE: ca hanh_vi=73 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 101 · dot bien .claude/dev/ci_dang_ky_test.py=2 + .github/workflows/ci.yml=78 + ops/ci_duong_nhanh.py=178 + ops/ci_duong_nhanh_test.py=43 = 301` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 · 113,9 s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 · 7,5 s (dòng `ĐĂNG KÝ:` ở ĐO HINT/H2) |
| `actionlint .github/workflows/ci.yml` (shellcheck có mặt) | rc=0, không finding |
| `python3 -m ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py` | `All checks passed!` rc=0 |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` rc=0 |
| `python3 -B ../goi/kiem_ke.py` | `CA tong: 101` (73/16/3/9) · `DOT_BIEN tong: 301` (178/43/78/2) · `MAU_RC = 5 · TU_KIEM_DOT_BIEN = 3` · `BO_QUA {'gate': 5, 'gate-ops': 3, 'gate-packet-loop': 1}` · ba ca dữ liệu trên kho thật `loi = [] · 6.1s` |
| `python3 -B ../goi/do_lai_so.py` | `[1] … do duoc diff: 345; toan allowlist: 63; … NGUYEN BAN do: 8` (khớp D1 "345 / 63 / 8/63") |

Khớp lời khai commit lượt 17 (`CA 101/101, DOT BIEN 301/301, TONG DAT; ci_dang_ky_test 23/23 + 1025/1025; actionlint rc=0; ruff F
sach; doctrine-scan rc=0; +1/-0`).

## H0 — bản vá lượt 17 CHỈ đổi chú thích? (`ast.dump` bỏ docstring, `tmp/ast/so_ast.py`, log `out/ast-so-sanh.log`)
```
tep doi: ['ops/ci_duong_nhanh.py', 'ops/ci_duong_nhanh_test.py']
ops/ci_duong_nhanh.py: ast.dump DAY DU bang nhau=False | bo docstring (17/17 docstring) bang nhau=True
  doi chung (TOI_DA_TEN_IN 5->6) bang nhau = False
ops/ci_duong_nhanh_test.py: ast.dump DAY DU bang nhau=False | bo docstring (78/78 docstring) bang nhau=True
  doi chung (them dong ma vao cay_t82) bang nhau = False
```
Kèm: không mã nào ĐỌC hai docstring đã sửa (`grep __doc__|get_docstring`: chỉ `t98` đọc docstring MODULE của hai tệp, không đọc
docstring hàm). **Kết luận: ĐÚNG — 98377f8 so f9f6fb1 không đổi AST mã chạy** (đối chứng: một đổi mã thật làm phép so ra False).

## ĐỐI CHIẾU LƯỢT TRƯỚC (P3 lượt 16 `docstring-moi-khai-rong-hon-ma`; đột biến TỰ VIẾT trên bản sao tối thiểu)
Rig: `tmp/f3/kiem_docstring_l17.py` (log `out/f3-kiem-docstring-l17.log`; khối dưới là trích, rút gọn tên ca). Mỗi biến thể dựng bản sao tối thiểu RIÊNG trong
`tmp/f3/ban/<biến thể>/` (5 tệp `ops/` chép từ `cay`, KHÔNG chạm `cay`). Mệnh đề lấy nguyên ý từ docstring ở HEAD; đo HAI cách:
**động** (chạy MỌI ca dùng `cay_t82()` trong tiến trình, bọc `kiem_ca_chep_cay` để ghi CHUỖI kết quả) và **tĩnh** (AST: ca nào có
`bang` đọc kết quả `kiem_ca_chep_cay`; tập mẫu `ignore_patterns(...)` trong `t82` của `lease_publish_test.py`).

```
== nen
   ca dung cay_t82: [t20zi, t20zl, t20zm, t20zn, t20zp]
   t20zi: hang=DAT chuoi=['DAT', 'DO(1)'] bang_doc_ket_qua=True
   t20zl: hang=DAT chuoi=['DAT', 'DO(1)'] bang_doc_ket_qua=True
   t20zm: hang=DAT chuoi=['DAT', 'DO(1)'] bang_doc_ket_qua=True
   t20zn: hang=DAT chuoi=['DO(1)']        bang_doc_ket_qua=False
   t20zp: hang=DAT chuoi=['DO(1)', 'DAT'] bang_doc_ket_qua=True
   ignore_patterns t82: ['*.pyc', '.git', '__pycache__']
   (B) ten thuong docs/treo.md -> DO · duoi __pycache__ -> DAT · ten *.pyc -> DAT · duoi .git -> DAT ·
       duoi THU MUC ten kho.pyc/ -> DAT · ten .GIT (hoa, Linux) -> DO
   (A) menh de cay_t82: DUNG []        (B) menh de kiem_loai_tep: DUNG []
== M1 them ca moi dung cay_t82 MONG DO, khong doi chung  -> (A) SAI "t20zq…: MONG DO ma lan goi dau KHONG phai doi chung DAT: ['DO(1)']"
== M2 go doi chung loi0 cua t20zl                         -> (A) SAI "t20zl…: MONG DO ma lan goi dau KHONG phai doi chung DAT: ['DO(1)']"
== M3 t20zn doi ket qua t82                               -> (A) SAI "tap ca KHONG mong DO [t20zp] != tap ngoai le khai [t20zn, t20zp]" +
                                                             "t20zn: khai 'khong doi DAT/DO nao cua t82' ma co `bang` doc ket qua"
== M4 t82 bo qua them '*.md'                              -> (B) SAI "tap mau ignore_patterns cua t82 ['*.md', …] != tap ten docstring khai" +
                                                             "dong: ten thuong docs/treo.md -> DAT, mong DO"
```
| Lớp lượt 16 | Phép đo | Trạng thái |
|---|---|---|
| `docstring-moi-khai-rong-hon-ma` (i) `cay_t82` | 5 ca dùng cây: 3 ca MONG ĐỎ đều có đối chứng DAT trên chính cây trước đầu vào; đúng HAI ca còn lại là `t20zn` (không `bang` nào đọc kết quả `t82`) và `t20zp` (chuỗi `[DO, DAT]`) — khớp từng chữ hai ngoại lệ khai. M1/M2/M3 làm mệnh đề SAI đúng chỗ (phép đo có răng) | **ĐÃ VÁ THẬT** |
| `docstring-moi-khai-rong-hon-ma` (ii) `kiem_loai_tep` | tập mẫu bỏ qua của `t82` = `{.git, __pycache__, *.pyc}` = tập docstring khai; động: symlink treo dưới mọi tên bỏ qua (kể cả THƯ MỤC tên `*.pyc`) ⇒ DAT, tên thường ⇒ ĐỎ. M4 làm mệnh đề SAI | **ĐÃ VÁ THẬT** (ghi chú, không tính P: trên Windows `fnmatch` so không phân biệt hoa thường nên `.GIT` cũng bị bỏ qua — câu khai liệt kê MẪU nên vẫn đúng; Windows `KHÔNG ĐO ĐƯỢC` ở đây) |

Kết luận đối chiếu: P3 lượt 16 **ĐÃ VÁ THẬT** ở cả hai câu; bản vá không sinh lỗi mới trong hai câu ấy (H0: không đổi AST). Nhưng lớp
gốc của nó ("câu tổng quát hoá không kiểm trên chính mã") được vá ĐÚNG HAI CHỖ ĐƯỢC CHỈ — các hướng dưới rà phần CÒN LẠI của diff packet.

## BẢNG LỚP

| Slug | Gốc lớp | Biểu hiện trên 98377f8 | Hạng | Của ai |
|---|---|---|---|---|
| `tin-hieu-chot-ca-khong-doc-quyen` (F1) | Luật phân hạng khai trong docstring ("chỉ `bang()` ném tín hiệu; lỗi vô can ⇒ TÍN DỤNG GIẢ") RỘNG hơn chốt thật cưỡng chế: `t99` chỉ cấm `except` RỘNG, trong khi hai ca đổi lớp DỰNG SẴN thành tín hiệu. Cùng họ #355/#359 của CLAUDE.md ("tín hiệu 'đã giết' bị chính mã test giả mạo"), ở dạng HẸP | harness cấp GIẾT cho lỗi VÔ CAN TypeError/AttributeError/ValueError ở `t06` và UnicodeError ở `t20ze` (đo, H1); thêm một `except` đổi kiểu hẹp vào ca khác SỐNG SÓT qua `t99` (đo, `out/h1c-t99.log`); 0/301 đột biến hiện có bị tín dụng sai | **P3** (chủ kho có thể nâng P2: CLAUDE.md gọi phản chứng "mutant chết vì `AttributeError` qua `except` đổi kiểu phải là TÍN DỤNG GIẢ" là BẮT BUỘC) | **#674** |
| `chu-thich-khai-rong-hon-ma-con-sot` (F2) | CÙNG gốc lớp lượt 16 (`docstring-moi-khai-rong-hon-ma`: câu tổng quát hoá không kiểm trên chính mã) và lượt 15 F2 (câu cũ trôi). Lượt 17 vá ĐÚNG HAI câu được chỉ, không quét lớp trên phần còn lại của diff packet — hình dạng "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA" | năm câu đo được là sai: `kiem_mode_git` "mọi chốt khác đọc ĐĨA" (H3) · "chỉ MỘT giá trị … mọi giá trị lạ ⇒ đầy đủ" ở module + ci.yml (H4) · `kiem_lease` "D2 … còn mở" (H8) · luật `RUN_BUOC_PACKET` "PR bị CHẶN trên MỌI sự kiện" (H9) · "kiểm bản đột biến KHÁC bản gốc" (H7, tác động 0) | **P3** | **#674** |
| `docstring-moi-khai-rong-hon-ma` | (lượt 16) | **ĐÃ VÁ THẬT** — đối chiếu M1–M4 có răng | — | #674 (đóng) |
| `kiem-mode-git-chot-khong-rang` | lớp đã DỪNG theo S3 lease g4 | 0 phát hiện hành vi mới (lượt 17 không đổi mã; `t20zh` trong 101/101). Câu H3 nằm TRONG docstring `kiem_mode_git` nhưng nói về các chốt KHÁC — thuộc lớp tài liệu F2, không phải bảng quyết định | — | lớp đã dừng |
| `chot-yaml-chi-do-su-hien-dien` | nợ #694 | 0 phát hiện mới. H4 KHÔNG thuộc lớp này: `y02`/`y03` khoá đúng chữ biểu thức, lỗi nằm ở câu khai ngữ nghĩa | — | nợ #694 |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | nợ #694 | "4,1 giay moi lan" (`cay_t82`) không ghi điều kiện đo; "16/16 kich ban" (`t20zp`) không có rig trong cây — như lượt 16, không tính P | — | nợ #694 |
| QUAN SÁT | — | H10 "cổng DUY NHẤT" sai theo chiều VÔ HẠI · `ops/lease_publish.py:892` "Người gọi DUY NHẤT [của `bo_qua_han`]" hết đúng khi packet thêm `MA_KIEM_HET_HAN` (ngoài write set) · `t23` gọi lồng `t20a`/`t20d` nên dòng ĐỎ của ca ấy được tính cho `t23` — cố ý theo thiết kế (đo: `test_bo_loc_actor_o_env_git` chết bằng thông điệp của `t20a`, `out/h1b-t23.log`) | quan sát | — |

## BẢNG SĂN (ghi theo thứ tự có kết quả; mỗi hướng: giả thuyết / lệnh / output thật / kết luận. Khối output là TRÍCH log ở `out/`;
chỗ nào gộp/rút gọn dòng thì ghi rõ — nguyên văn đầy đủ ở log)

### H1 — "Chỉ `bang()` ném `TinHieuChotCa`; lỗi vô can đi ra dưới TÊN THẬT ⇒ TÍN DỤNG GIẢ" có đúng trên mã + harness THẬT không ⇒ **LỖI (F1)**
- **Giả thuyết:** docstring module (`CÁCH ĐO ĐỘT BIẾN`, dòng 16–18) và docstring lớp `TinHieuChotCa` (dòng 84) khai độc quyền; nhưng có
  ca tự `raise TinHieuChotCa` trong `except` bắt lớp DỰNG SẴN ⇒ lỗi vô can CÙNG LỚP của bản đột biến hoá thành "giết thật" — đúng
  bệnh #355/#359 mà CLAUDE.md ghi, và đúng "phản chứng bắt buộc" của nó: *"một mutant chết vì `AttributeError` phải rơi vào TÍN DỤNG
  GIẢ kể cả khi trên đường có một `except` đổi kiểu"*.
- **Lệnh:** `python3 -B tmp/h1/h1.py tmp/w` (clone @HEAD; log `out/h1.log`): (a) AST mọi `raise TinHieuChotCa` ngoài `bang` + lớp
  `except` bao quanh; (b) HARNESS THẬT (`chay_mot_dot_bien` của chính bộ test) với đột biến VÔ CAN `raise <Lớp>('vo can')` ở đầu
  `phan_loai_tu_diff` — cùng hình dạng `TU_KIEM_DOT_BIEN.sinh_ngoai_le_vo_can_KeyError` — đổi ca đích; (c) `raise UnicodeError` ở đầu
  `_doc_raw`; (d) lý do chết thật của 4 đột biến HIỆN CÓ đích `t06`.
- **Output thật** (trích `out/h1.log`; dòng (a) gộp 9 dòng SuDoGia/KhongCoFixture/sentinel; mỗi dòng (b) gộp hai dòng t01/t06):
```
(a) raise TinHieuChotCa NGOAI bang(): 11 cho  — 8 bat SuDoGia/KhongCoFixture (lop RIENG cua bo test), 1 trong sentinel cua t92, va HAI bat lop DUNG SAN:
    dong   285 ham t06_git_loi_hoac_dau_ra_hong_day_du   except (TypeError, ValueError, AttributeError)
    dong  1217 ham t20ze_kiem_re_ten_tep_khong_utf8_dat  except UnicodeError
(b) vo can `raise KeyError`       | dich t01 -> TIN_DUNG_GIA | dich t06 -> TIN_DUNG_GIA
(b) vo can `raise TypeError`      | dich t01 -> TIN_DUNG_GIA | dich t06 -> GIET
(b) vo can `raise AttributeError` | dich t01 -> TIN_DUNG_GIA | dich t06 -> GIET
(b) vo can `raise ValueError`     | dich t01 -> TIN_DUNG_GIA | dich t06 -> GIET
(c) vo can `raise UnicodeError` o _doc_raw | dich t20ze -> GIET | dich t20zc -> TIN_DUNG_GIA
(d) fail_open_rc_khong_kiem / fail_open_bat_ngoai_le_bi_go / fail_open_dau_ra_cut: DO o `bang` (thuoc tinh that)
    fail_open_dau_ra_khong_phai_bytes: "DO:t06…:dau ra khong phai bytes: phan_loai ne TypeError thay vi fail-close …" (qua duong DOI KIEU)
```
- Răng của `t99` với dạng HẸP (log `out/h1c-t99.log`): đột biến THÊM `except (TypeError, KeyError): raise TinHieuChotCa` vào `t01`
  ⇒ ca đích `t99` **SONG_SOT**, `t96` **SONG_SOT**; trên bản đã thêm ấy, đột biến vô can `raise KeyError` ở đầu `phan_loai_tu_diff`
  (đúng hình dạng `TU_KIEM_DOT_BIEN.sinh_ngoai_le_vo_can_KeyError`) đích `t01` ⇒ `rc=3 phan_hang=GIET`. Tức chốt chống đổi kiểu chỉ
  có răng với `except` RỘNG; dạng hẹp chỉ bị bắt nếu rơi đúng tổ hợp (`t01`, KeyError) mà bộ tự kiểm chọn.
- Lịch sử (`git log -S`): câu "Chỉ `bang()` ném lớp này" và `except (TypeError, ValueError, AttributeError)` của `t06` CÙNG vào ở commit
  đầu `1687c69` ⇒ câu khai sai NGAY LÚC VIẾT; `except UnicodeError` của `t20ze` thêm ở `8e204f3` (lượt 13).
- **Kết luận: LỖI (F1, P3).** Hôm nay KHÔNG có đột biến nào trong 301 được tín dụng sai (đột biến duy nhất chết qua đường đổi kiểu —
  `fail_open_dau_ra_khong_phai_bytes` — có `TypeError` là HẬU QUẢ TRỰC TIẾP của chốt bị gỡ, lượt 7 đã xét và chấp nhận), nhưng harness
  CẤP ĐƯỢC "GIẾT" cho lỗi vô can ở hai ca (đo được), trái lời khai của chính nó và trái phản chứng bắt buộc của CLAUDE.md; `t99` chỉ cấm
  `except` RỘNG nên không canh dạng này; bộ tự kiểm (`sinh_ngoai_le_vo_can_KeyError` ở `t01`) chọn đúng tổ hợp không lộ lỗ.

### H3 — "Mọi chốt nội dung khác của kiem-re đọc ĐĨA" (docstring `kiem_mode_git`, dòng 318) ⇒ **LỖI tài liệu (một mục của F2)**
- **Lệnh:** `python3 -B tmp/h3/h3.py tmp/w` (log `out/h3.log`): commit tệp vào nhánh PR rồi làm ĐĨA nói khác GIT (ghi đè / xoá).
- **Output thật** (trích `out/h3.log`, mỗi dòng gộp ba vế đĩa có CÙNG kết quả):
```
(1) kiem_diff_check | git: X.md co dau xung dot | dia NGUYEN / GHI DE sach / XOA tep -> ca ba: ['git diff --check rc=2: ops/specs/X.md:2: leftover conflict marker …']
(2) kiem_nhi_phan   | git: x.md nhi phan        | dia NGUYEN / GHI DE van ban / XOA -> ca ba: ["tep ho so nhi phan …: 'ops/land/x.md'"]
(3) kiem_yaml (doi chung) | git: h.yaml hong    | dia NGUYEN -> ['YAML khong parse duoc …'] | dia GHI DE yaml lanh -> []
```
- **Kết luận: LỖI tài liệu.** `kiem_diff_check` và `kiem_nhi_phan` đọc GIT (kết luận không đổi khi đĩa khác git); chỉ `kiem_yaml`/
  `kiem_loai_tep`/`kiem_lease`/hai ca của lease-publish đọc đĩa. Lý do `--check`/numstat mù với gitlink là gitlink KHÔNG có nội dung trong
  git, không phải "đĩa nói dối". Không đổi hành vi.

### H4 — "Chỉ MỘT giá trị (`duong_nhanh`) mở đường bỏ bước; mọi giá trị lạ … đều thành đầy đủ ở phía `ci.yml`" ⇒ **LỖI tài liệu (một mục của F2)**
- **Giả thuyết:** biểu thức Actions so CHUỖI không phân biệt hoa thường (tài liệu GitHub: "GitHub ignores case when comparing strings"),
  nên `!= 'duong_nhanh'` không phải "chỉ đúng chuỗi ấy".
- **Lệnh:** trích NGUYÊN VĂN 13 `if:` mang `che_do` + output `che_do` của `chuan-bi` từ `cay/.github/workflows/ci.yml` (PyYAML) rồi đánh
  giá bằng bộ đánh giá CHÍNH THỨC `@actions/expressions@0.3.61` (actions/languageservices; cài vào `tmp/npm`, `node tmp/npm/danh_gia.mjs`,
  log `out/h4-bieu-thuc.log`); ngữ cảnh `github.event_name=pull_request`, `runner.os=Linux`.
- **Output thật (trích):**
```
doi chung bo danh gia: "'a' == 'A'" -> true | "'a' == 'b'" -> false
BUOC gate/golden-test | if: needs.chuan-bi.outputs.che_do != 'duong_nhanh'
    "duong_nhanh"=>false  "DUONG_NHANH"=>false  "Duong_Nhanh"=>false  "dUONG_nHANH"=>false  "day_du"=>true  ""=>true  "duong_nhanh "=>true
(… y het o 7 buoc bi bo con lai tren Linux; buoc lifecycle nen => false voi MOI gia tri vi `runner.os != 'Linux'`;
 4 buoc `== 'duong_nhanh'` => true voi moi bien the hoa/thuong)
OUTPUT che_do | github.event_name == 'pull_request' && steps.phan-loai.outputs.che_do || 'day_du'
    "DUONG_NHANH"=>"DUONG_NHANH"  ""=>"day_du"
```
- **Kết luận: LỖI tài liệu, KHÔNG phải fail-open.** 1023 biến thể khác hoa/thường của `duong_nhanh` (10 chữ cái ⇒ 2^10 cách viết) đều bỏ bước nặng; nhưng
  nguồn DUY NHẤT của `che_do` là `main()` ghi hằng `DAY_DU`/`DUONG_NHANH` (chữ thường, `t16` khoá) — không đường nào sinh biến thể. Câu
  khai "chỉ MỘT giá trị … mọi giá trị lạ ⇒ đầy đủ" (module docstring dòng 18–19, ci.yml dòng 45) rộng hơn ngữ nghĩa Actions; không ca nào
  đo ngữ nghĩa ấy (`y02`/`y03` khoá CHỮ của biểu thức). Chạy trên Actions thật: `KHÔNG ĐO ĐƯỢC` (đo bằng bộ đánh giá TS chính thức + tài liệu).

### H2 — Bất biến của head (nghiệm thu 9, 10; phạm vi lượt mục 2) ⇒ **ĐÚNG**
- `python3 -B .claude/dev/ci_dang_ky_test.py` (trong `cay/`): dòng 1 `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0.
- `git diff --numstat origin/master -- .claude/dev/ci_dang_ky_test.py` ⇒ `1 0`; diff packet đúng 4 tệp write set (bảng Đối tượng).
- `PYTHONUTF8=1 … python3.12 scripts/tl.py --selftest` trên clone `tmp/w` @HEAD (KHÔNG chạy trong `cay` vì lệnh này ghi
  `scripts/.tl_state/`): `== tl selftest 1715/1715 ==` · 0 dòng `[FAIL]` · rc=0 (log `out/tl-selftest-head.log`).
- ruff F `scripts/tl.py`: `Found 12 errors.` (= nền 12 F821 của CLAUDE.md); `git diff --quiet origin/master HEAD -- scripts/tl.py` ⇒ tệp
  KHÔNG đổi ⇒ delta = 0. Hai tệp mới: `All checks passed!`.
- `git -C cay status --short --ignored` trước/sau toàn bộ lệnh nền: RỖNG cả hai (`out/nen/status-*.txt`). `do_lai_so.py [2]`:
  `ops/leases/*.yaml … 119 tep; kiem(bo_qua_han=True) dat 119, truot 0` (clone đủ 527 ref — khớp "0/113 trên bản sao đủ ref" về chiều).

### H5 — Mở lại đúng đắn đường nhanh CHỈ khi có bằng chứng mới: còn bước bị bỏ nào ĐỌC hồ sơ thật mà `kiem-re` không chạy? ⇒ **KHÔNG PHẢI LỖI**
- **Giả thuyết:** docstring `kiem_ca_du_lieu` khai "ba ca nay doc NOI DUNG ho so that"; nếu `lease_publish_test`/`packet_loop_test`/
  `tl` còn ca khác đọc `ops/{land,leases,reviews,specs}` của CÂY THẬT thì PR hồ sơ làm master ĐỎ ở bước bị bỏ.
- **Lệnh:** `grep` mọi lối đọc cây thật trong `ops/lease_publish_test.py` (`HERE.parent`, `HERE /`, glob/iterdir) và đọc từng chỗ;
  `grep` `ops/{leases,reviews,land,specs}` trong `.claude/dev/packet_loop{,_test}.py`, `scripts/tl_core/*.py`; đọc `main()` runner
  (`lease_publish_test.py:11037-11083`).
- **Output thật:** lối đọc hồ sơ của cây thật trong `lease_publish_test.py` chỉ có `HERE / "leases"` (dòng 923, `t23`), `HERE / "reviews"`
  (dòng 1168, `_doi_thu_muc_reviews` của `t26`/`t27`), `copytree(HERE.parent …)` (dòng 3166, `t82`); các `HERE.parent` khác đọc
  `.github/workflows`, `ops/NO_KY_THUAT.md`, `ops/cai_actionlint.sh`, `.claude/dev/*` (ngoài allowlist ⇒ PR đổi chúng là `day_du`).
  `packet_loop.py` đọc `ops/reviews` thật chỉ trong `cmd_bien_nhan` theo `--root` (bộ test dựng kho giả; lượt 16 H5 `xoa_reviews` ⇒
  `packet_loop_test` rc=0). `scripts/tl_core/release.py:399` có `"ops"` trong danh sách LOẠI khỏi gói. `main()` runner gọi MỌI ca bằng
  cùng một `fn()` trong cùng vòng lặp ⇒ khung gọi của `t82` trong suite đầy đủ = khung của `t01` mà `t20zn` đo (khẳng định "CÙNG độ
  sâu khung gọi" của docstring module đứng được).
- **Kết luận: KHÔNG PHẢI LỖI** — không bằng chứng mới; bốn ca `kiem-re` chạy (`t23`,`t26`,`t27`,`t82`) phủ đúng bốn lối đọc hồ sơ thật.

### H6 — Mọi con số kiểm được offline trong chú thích/docstring của packet ⇒ **ĐÚNG** (trừ số thời gian, phụ thuộc máy)
| Lời khai (vị trí) | Lệnh | Output |
|---|---|---|
| "master có ba tệp `.gitattributes` dưới `ops/reviews/`" (`ci_duong_nhanh.py:73`) | `git ls-tree -r --name-only origin/master -- ops/reviews \| grep -c '\.gitattributes$'` | `3` (cả allowlist cũng 3) |
| "master: 0 tệp nhị phân dưới allowlist" (`:75`, `:378`) | `git --attr-source=origin/master diff --numstat -z <cây rỗng> origin/master -- ops/{land,leases,reviews,specs}` đếm `-\t-\t` | `0` / 1991 tệp |
| "345 … 63 … 8/63" (D1 `:54-56`), "8/63 lan merge" (`t20d`) | `goi/do_lai_so.py` | `345 / 63 / 8` |
| "123 tep doi" (`t20zm`) | `git ls-tree -r --name-only origin/master -- ops/leases \| wc -l` | `123` |
| "`JOB_G5` … KHÔNG có `gate-ops`" (docstring module test) | `grep JOB_G5 .claude/dev/ci_dang_ky_test.py` | `("gate", "gate-registry", "gate-packet-loop", JOB_G5_MANH, JOB_G5_GOP)` |
| "`cong_cu_test.t6` chỉ soi các bước TRƯỚC G5" | đọc `ops/cong_cu_test.py:266-294` | `buoc[:idx_kiem[0]]` của `jobs.gate` — đúng |
| "ngưỡng 492 (3.11.15) / 494 (3.12.3)", "~120 MB", "~6 giây", "4,1 giây" | đã đo lại ở lượt 16 (`nguong.py`, copytree 120,8 MB); `kiem_ke.py` ở đây: ba ca dữ liệu `6.1s` | khớp; số giây phụ thuộc máy (nợ #694, không tính P) |

### H7 — "Mỗi đột biến: neo `count == 1` …, kiểm bản đột biến KHÁC bản gốc, …" (docstring module test, dòng 19) ⇒ **LỖI tài liệu nhỏ (một mục của F2, tác động 0)**
- **Lệnh:** nạp module test từ `tmp/w`, phân loại 301 mục `DOT_BIEN` theo hàm neo (tên trong `co_names` của hàm biến đổi) + thử đồng nhất
  (log `out/h7.log`).
- **Output thật:**
```
DOT_BIEN theo ham neo: {'thay_mot': 288, 'thay_regex': 13, 'khac': 0} | tong 301
thay_mot dong nhat -> ha tang: dot bien khong doi gi
thay_regex dong nhat -> 'x = 1\n' (KHONG nem, tra ban GIONG HET ban goc)
```
- **Kết luận:** neo `count == 1` đúng cho cả 301; chốt "khác bản gốc" chỉ có ở `thay_mot` — 13 đột biến YAML qua `thay_regex` không có.
  Tác động 0: một đột biến đồng nhất sẽ SỐNG SÓT ⇒ suite ĐỎ (fail-close), không cấp được tín dụng. Ghi để câu khai bằng mã.

### H8 — Chú thích CŨ trôi sau quyết định: docstring `kiem_lease` "D2 (quyết định của chủ kho) còn mở" ⇒ **LỖI tài liệu (một mục của F2)**
- **Lệnh:** đọc `ops/ci_duong_nhanh.py:410-411` và `:50-53`; `git log -S` từng câu trên `origin/master..HEAD`; đọc `lease_publish.py`
  (`lenh_check` dòng 2061-2077, `kiem` dòng 792-899) để đo nửa còn lại của câu ("vẫn kiểm mọi chốt khác, chỉ bỏ chốt hạn").
- **Output thật** (trích dòng nguồn + hai kết quả `git log -S`; dòng cuối là tóm tắt phép đọc mã):
```
kiem_lease: "… vẫn kiểm mọi chốt khác, chỉ bỏ chốt hạn. Cả `.yaml` và `.yml`. D2 (quyết định của chủ kho) còn mở: xem docstring module."
module    : "Hai chỗ khác chữ trần của đặc tả r2 … CHỦ KHO ĐÃ DUYỆT CẢ HAI (lựa chọn (a)) — erratum …"
git log -S"D2 (quyết định của chủ kho) còn mở" -> 3d12524 2026-09-29T09:32:30Z
git log -S"CHỦ KHO ĐÃ DUYỆT CẢ HAI"            -> 1cec719 2026-09-29T09:54:09Z  (docs: ghi D1/D2 la hanh vi da duoc chu kho duyet)
lease_publish.py: lenh_check = kiem(_doc_yaml(tep), tep, goc) + in; `bo_qua_han` chi xuat hien o dong 894 (`if not bo_qua_han and han <= now`)
```
- **Kết luận:** nửa HÀNH VI đúng (`check` ≡ `kiem()`; `bo_qua_han` bỏ đúng một chốt). Nửa TRẠNG THÁI sai: câu "D2 … còn mở" viết lúc
  09:32Z, chủ kho duyệt và module docstring ghi lại lúc 09:54Z, câu ở `kiem_lease` không ai sửa — hai docstring CÙNG TỆP nói ngược nhau
  về đúng thứ mà PROMPT bảo reviewer đừng ghi finding chính sách. Cùng lớp lượt 15 F2 (`chu-thich-co-san-khai-hanh-vi-cu`).
- Quan sát ngoài write set (không tính P): `ops/lease_publish.py:892` viết "Người gọi DUY NHẤT [của `bo_qua_han`]: nhánh đã-có-dấu của
  `kiem_github`" — packet thêm người gọi THỨ HAI (`MA_KIEM_HET_HAN`), nên câu ấy hết đúng; tệp ngoài write set, chỉ ghi để người giữ biết.

### H9 — Chú thích luật `RUN_BUOC_PACKET` (`ci_duong_nhanh_test.py:2180-2181`): "`che do` … thêm `exit 1` ⇒ … PR bị CHẶN trên MỌI sự kiện" ⇒ **LỖI tài liệu (một mục của F2)**
- **Lệnh:** trích `if:` của bước `che do (push / workflow_dispatch luon day du)` từ `cay/.github/workflows/ci.yml` rồi đánh giá bằng
  `@actions/expressions` (`node tmp/npm/su_kien.mjs`, log `out/h9-che-do-exit1.log`).
- **Output thật:**
```
if: github.event_name != 'pull_request' | event_name=pull_request -> false
if: github.event_name != 'pull_request' | event_name=push -> true
if: github.event_name != 'pull_request' | event_name=workflow_dispatch -> true
```
- **Kết luận:** bước ấy KHÔNG chạy ở `pull_request`, nên `exit 1` trong nó không chặn được PR nào; hậu quả thật là `chuan-bi` đỏ ở
  `push`/`workflow_dispatch` (gate của master mất ba job). Đột biến `yml_che_do_exit1` và ca `y14` vẫn đúng và có răng; chỉ câu lý do khai
  rộng hơn ngữ nghĩa `if:`.

### H10 — "ĐÂY LÀ CỔNG DUY NHẤT canh `if:` cấp job của `gate-ops`" (docstring module test; chú thích ci.yml gate-ops) ⇒ **QUAN SÁT, không tính P**
- **Lệnh:** `python3 -B tmp/h10.py tmp/w2` — chèn `if:` cấp job vào `gate-ops` của clone `tmp/w2`, chạy `ci_dang_ky_test` (cổng KHÁC) và
  `y11`, khôi phục sau mỗi lần (log `out/h10.log`).
- **Output thật** (trích; danh sách mục ĐỎ rút gọn bằng `…`):
```
[nen] ci_dang_ky_test rc=0 ['ĐĂNG KÝ: 23/23', 'TỔNG: ĐẠT'] | y11 rc=0
[if: false] ci_dang_ky_test rc=1 ['ĐỎ: CI không gọi mục đăng ký: .claude/dev/gate_lifecycle_test.py', … 'ops/ci_duong_nhanh_test.py', …] | y11 rc=3
[if: ${{ false }}] ci_dang_ky_test rc=1 [… y het …] | y11 rc=3
[if: che_do != duong_nhanh] ci_dang_ky_test rc=0 ['ĐĂNG KÝ: 23/23', 'TỔNG: ĐẠT'] | y11 rc=3
```
- **Kết luận:** câu "duy nhất" sai theo chiều VÔ HẠI (dạng `false` hằng còn có `ci_dang_ky_test.bi_tat` chặn); dạng điều kiện — thứ nợ
  Q6-i nói tới — đúng là chỉ `y11` chặn. Không tính P (khai HẸP hơn bảo vệ thật, không mở đường nào).

## FINDINGS

### tin-hieu-chot-ca-khong-doc-quyen [P3] (F1) Docstring khai `TinHieuChotCa` chỉ do `bang()` ném và lỗi vô can luôn là TÍN DỤNG GIẢ — hai ca đổi lớp dựng sẵn nên harness CẤP GIẾT cho lỗi vô can
**TỆP/DÒNG:** `ops/ci_duong_nhanh_test.py:16-18` (docstring module, "CÁCH ĐO ĐỘT BIẾN") · `:84` (docstring `TinHieuChotCa`) ·
`:283-285` (`t06`: `except (TypeError, ValueError, AttributeError) … raise TinHieuChotCa`) · `:1216-1217` (`t20ze`: `except UnicodeError`) ·
`:2501-2518` (`t99` chỉ xét `except` trần/Exception/BaseException/AssertionError).

**VẤN ĐỀ:** docstring khai hai điều mà mã không có: (1) "Ca đích chỉ báo ĐỎ bằng `TinHieuChotCa` … do CHÍNH `bang()` ném" / "Chỉ
`bang()` ném lớp này" — đo: 11 chỗ `raise TinHieuChotCa` ngoài `bang()`; (2) "Lỗi vô can trong mã bị đột biến (TypeError, KeyError, ...)
đi ra dưới TÊN THẬT ⇒ … `TIN_DUNG_GIA`" — sai cho `t06` (TypeError/ValueError/AttributeError) và `t20ze` (UnicodeError): ở hai ca ấy
lỗi vô can CÙNG LỚP thành "giết thật". Đó đúng là phản chứng BẮT BUỘC mà CLAUDE.md ghi sau #355/#359 ("một mutant chết vì
`AttributeError` phải rơi vào TÍN DỤNG GIẢ kể cả khi trên đường có một `except` đổi kiểu") — và nó KHÔNG đạt. `t99` chỉ canh dạng RỘNG,
nên một `except` đổi kiểu HẸP mới ở ca bất kỳ cũng lọt (đo). Bộ tự kiểm `sinh_ngoai_le_vo_can_KeyError` chọn đúng tổ hợp (`t01`,
KeyError) không lộ lỗ. Hôm nay 0/301 đột biến bị tín dụng sai (đột biến duy nhất chết qua đường đổi kiểu, `fail_open_dau_ra_khong_phai_bytes`,
có `TypeError` là hậu quả TRỰC TIẾP của chốt bị gỡ — lượt 7 đã xét), nên đây là lỗi tài liệu + lỗ TIỀM ẨN của bộ đo, không phải con số
301/301 sai. Câu sai ngay lúc viết: lời khai và `except` của `t06` cùng vào ở commit đầu `1687c69`.

**PHẢN CHỨNG** (chạy được, chỉ trên clone `tmp/w`; `python3 -B tmp/h1/h1.py tmp/w`, log `out/h1.log`, `out/h1c-t99.log`):
```
(b) vo can `raise TypeError`      | dich t01 -> TIN_DUNG_GIA | dich t06 -> GIET
(b) vo can `raise AttributeError` | dich t01 -> TIN_DUNG_GIA | dich t06 -> GIET
(b) vo can `raise ValueError`     | dich t01 -> TIN_DUNG_GIA | dich t06 -> GIET
(c) vo can `raise UnicodeError` o _doc_raw | dich t20ze -> GIET | dich t20zc -> TIN_DUNG_GIA
them `except (TypeError, KeyError): raise TinHieuChotCa` vao t01 | ca dich t99 -> SONG_SOT
```

**HINT** (`HINT.patch`, chỉ chú thích/docstring): viết lại gạch đầu dòng "CÁCH ĐO ĐỘT BIẾN" và docstring `TinHieuChotCa` cho khớp mã —
tín hiệu do `bang()` ném HOẶC do ca ném khi bắt lớp RIÊNG của bộ test; nêu tên HAI ngoại lệ có chủ đích (`t06`, `t20ze`) cùng hệ quả đo
được (lỗi vô can cùng lớp ở đó là GIẾT) và rằng `t99` chỉ cấm `except` RỘNG; chú thích dòng `t20ze` bỏ chữ "CHI loi giai ma" (bắt cả
lớp `UnicodeError`). Muốn ĐÓNG lỗ (CLAUDE.md đòi) thì cần mã, KHÔNG có trong patch: `t99` đòi mọi `except` dẫn tới tín hiệu chỉ bắt lớp
RIÊNG của bộ test (`SuDoGia`, `KhongCoFixture`) hoặc nằm trong một bảng cho phép tường minh `{t06: {TypeError, ValueError, AttributeError},
t20ze: {UnicodeError}}`, kèm đột biến đích `t99` = đúng đột biến "thêm `except (TypeError, KeyError)` vào `t01`" ở trên (hôm nay SỐNG SÓT,
phải thành GIẾT) và đột biến gỡ một mục khỏi bảng cho phép (phải làm `t99` ĐỎ).

**ĐỘT BIẾN đo răng:** hint tài liệu — không cổng nào canh nội dung docstring (nói thẳng: phần này là kỷ luật đọc). Đo hint: suite
không đổi (mục ĐO HINT). Răng cho hướng mã nêu trên đã đo sẵn trạng thái hiện tại: `SONG_SOT` (`out/h1c-t99.log`).

**ĐỘ TIN:** cao (đo trên harness thật, đối chứng hai đích); tác động hôm nay thấp (0/301), tác động tiềm ẩn: con số `DOT BIEN: M/M bị
giết ĐÚNG LÝ DO` có thể phồng ở các đột biến sau này đích `t06`/`t20ze` hoặc ca có `except` đổi kiểu mới.

### chu-thich-khai-rong-hon-ma-con-sot [P3] (F2) Năm câu khai CŨ của packet rộng hơn (hoặc trôi khỏi) mã/ngữ nghĩa — lớp lượt 16 vá đúng hai câu được chỉ
**TỆP/DÒNG và PHẢN CHỨNG từng mục** (mỗi mục có lệnh chạy được ở hướng tương ứng):
| # | Câu khai | Vị trí | Phép đo | Thực tế |
|---|---|---|---|---|
| a | "Mọi chốt nội dung khác của kiem-re đọc ĐĨA" | `ops/ci_duong_nhanh.py:318` | H3 `tmp/h3/h3.py` | `kiem_diff_check`/`kiem_nhi_phan` đọc GIT: ghi đè/xoá tệp trên đĩa, kết luận KHÔNG đổi; chỉ `kiem_yaml` (đối chứng) đổi theo đĩa |
| b | "Chỉ MỘT giá trị (`duong_nhanh`) mở đường bỏ bước; mọi giá trị lạ … đều thành đầy đủ" / ci.yml "chi dung chuoi `duong_nhanh` moi bo buoc" | `ops/ci_duong_nhanh.py:18-19`, `.github/workflows/ci.yml:45` | H4 `@actions/expressions` trên 13 `if:` thật | so chuỗi Actions không phân biệt hoa thường: `DUONG_NHANH`, `Duong_Nhanh`… cũng bỏ mọi bước nặng mang `!= 'duong_nhanh'` (không phải fail-open: nguồn `che_do` duy nhất ghi hằng chữ thường) |
| c | "D2 (quyết định của chủ kho) còn mở" | `ops/ci_duong_nhanh.py:411` | H8 `git log -S` | viết 09:32Z (`3d12524`); chủ kho duyệt, module ghi "ĐÃ DUYỆT CẢ HAI" 09:54Z (`1cec719`); câu này không ai sửa — hai docstring cùng tệp nói ngược nhau |
| d | "`che do` … thêm `exit 1` ⇒ … PR bị CHẶN trên MỌI sự kiện" | `ops/ci_duong_nhanh_test.py:2180-2181` | H9 `@actions/expressions` | bước ấy `false` ở `pull_request`: `exit 1` chỉ làm đỏ `chuan-bi` ở push/dispatch, không chặn PR nào |
| e | "Mỗi đột biến: … kiểm bản đột biến KHÁC bản gốc" | `ops/ci_duong_nhanh_test.py:19` | H7 | 13/301 đột biến qua `thay_regex` không có chốt ấy (tác động 0: đột biến đồng nhất sẽ SỐNG SÓT ⇒ suite ĐỎ) |

**VẤN ĐỀ:** cùng gốc với P3 lượt 16 (câu tổng quát hoá/ trạng thái không kiểm trên chính mã khi viết, hoặc không cập nhật khi mã/quyết
định đổi). Lượt 17 sửa đúng hai câu lượt 16 chỉ ra mà không quét phần còn lại của diff packet; PROMPT lượt này đòi quét TOÀN BỘ. Không
mục nào đổi hành vi sản phẩm; (b) và (d) là lời khai về NGỮ NGHĨA `ci.yml` mà không ca `y*` nào đo (chúng khoá CHỮ, đúng thiết kế).

**HINT** (`HINT.patch`, chỉ chú thích/docstring, 3 tệp trong write set): (a) tách "chốt đọc ĐĨA" (`kiem_yaml`/`kiem_loai_tep`/
`kiem_lease`) khỏi "hai chốt đọc GIT" (`kiem_diff_check`, `kiem_nhi_phan` — gitlink không có nội dung trong git); (b) nêu so chuỗi
Actions không phân biệt hoa thường và rằng tệp chỉ ghi hằng chữ thường (`t16` khoá) — ở cả module docstring lẫn chú thích `ci.yml`;
(c) "D2 là hành vi chủ kho ĐÃ DUYỆT (erratum đặc tả r2)"; (d) bước `che do` chỉ chạy ở push/workflow_dispatch nên `exit 1` làm mất gate
của master, không chặn PR; (e) "`thay_mot` còn kiểm bản đột biến KHÁC bản gốc, `thay_regex` thì không — đột biến đồng nhất ở đó SỐNG SÓT".

**ĐỘT BIẾN đo răng:** không áp dụng (tài liệu; không cổng nào canh nội dung chú thích — nói thẳng). Đo hint không làm đỏ gì (ĐO HINT);
riêng sửa chú thích `ci.yml`: actionlint rc=0 và cấu trúc YAML đã parse BẰNG HỆT bản gốc.

**ĐỘ TIN:** cao (mỗi mục một phép đo chạy được); tác động thấp. Chủ kho có thể hạ thành quan sát, như lượt 16.

## ĐO HINT (`R/HINT.patch`, sha256 `f257372081f418053ec72ef48600d04856204fd50a478078acdac1d6e9d6803b`, 3 tệp — đều trong write set, chỉ chú thích/docstring)
Script `tmp/do_hint.sh` (log `out/hint/`), clone MỚI `tmp/ap` từ mirror, `HEAD = 98377f8da2ee72978e794b6f2507ac1b8b7e5689`:
| Phép đo | Output thật |
|---|---|
| `git apply --check HINT.patch` rồi `git apply` | `apply_check_rc=0` · `apply_rc=0` · `cmp` cả 3 tệp GIỐNG bản soạn (`tmp/hint`) |
| `git diff --numstat` (đã áp) | `2 1 .github/workflows/ci.yml` · `10 7 ops/ci_duong_nhanh.py` · `16 10 ops/ci_duong_nhanh_test.py`; `git diff --numstat origin/master -- .claude/dev/ci_dang_ky_test.py` ⇒ `1 0` (hint không chạm) |
| `ast.dump` bỏ docstring HEAD vs đã áp; YAML đã parse | `ops/ci_duong_nhanh.py … bang nhau: True` · `ops/ci_duong_nhanh_test.py … bang nhau: True` · `ci.yml cau truc YAML bang nhau: True` |
| `python3 -B ops/ci_duong_nhanh_test.py` (đã áp) | `CA: 101/101 dat · 0 do · 0 hong` · `DOT BIEN: 301/301 bi giet dung ly do` · `KIEM KE: … = 101 · … = 301` (không đổi) · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 · 121 s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` (đã áp) | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` (shellcheck có mặt) · `ruff --select F` hai tệp · `doctrine-scan` | rc=0 · `All checks passed!` · `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `tl.py doc-claims-check --strict --json`, HAI VẾ dựng trong MỘT lệnh (`tmp/docclaims_2ve.sh`: clone mới → checkout → [áp] → đo) | nền `rc=0 ok True files 110 advisory 381 flags 0` · sau `rc=0 ok True files 110 advisory 381 flags 0` · `advisories bang nhau: True` |
- **Lỗi rig (khai):** lần đo doc-claims ĐẦU dùng `tmp/w` (đã chạy `tl --selftest`, sinh `references/golden/fixtures/`) làm vế nền và
  `tmp/ap` làm vế sau ⇒ lệch giả `advisory 379 → 381` (cả hai mục chênh là `PATH_MISSING_IN_HISTORICAL_DOC` của
  `references/golden/fixtures/` trong `CHANGELOG.md`, không dính hint). Dựng lại hai vế trong MỘT lệnh ⇒ delta 0. Đúng bài học CLAUDE.md
  "phép đo delta hai vế phải dựng trong MỘT lệnh".
- Neo đột biến: 0/301 đột biến có chuỗi neo (ô đóng + hằng trong thân hàm biến đổi) chứa một dòng mà hint xoá/thay (log
  `out/hint/neo-giao.log`: hint đổi 1 + 7 + 10 dòng); suite 301/301 trên bản đã áp xác nhận mọi neo còn khớp đúng một lần. Hint mới
  chạy trên BẢN SAO; executor phải tự áp, tự đo, tự commit.

## KHÔNG ĐO ĐƯỢC (nói thẳng)
- Actions thật: PR thật (nghiệm thu 11), merge ref/`github.sha` thật, bộ đánh giá biểu thức của runner (C#). H4/H9 đo bằng bộ đánh giá
  TypeScript CHÍNH THỨC `@actions/expressions@0.3.61` + tài liệu GitHub ("GitHub ignores case when comparing strings"), không bằng runner.
- Windows: `gate-ops` có nhãn `windows` chạy `kiem-re` (gồm `t82` qua runner) trên Windows; selftest packet chỉ Linux. `fnmatch` trên Windows
  không phân biệt hoa thường (`.GIT` cũng bị bỏ qua) — suy từ tài liệu Python, không đo.
- Bước cgroup thật của `gate-ops`; G5/`gate-cong-cu` (không bị bỏ ở đường nhanh, ngoài phạm vi lượt này).
- Model/effort thật của lượt review này (tự khai Opus 5.5 / max, không receipt runtime).

## TÁC ĐỘNG NGOÀI SANDBOX (khai)
- `R/cay` không bị chạm: `git -C cay status --short --ignored` RỖNG trước/sau mọi lệnh chạy trong đó và ở cuối lượt; HEAD vẫn `98377f8`.
  Mọi đột biến/phản chứng chạy trên clone/bản sao trong `R/tmp/` (`w`, `w2`, `hint`, `hint-nhap1`, `ap`, `dc-nen`, `dc-sau`, `f3/ban/*`).
- Mọi lệnh Bash mở đầu bằng `cd R`, TRỪ ba lệnh `mkdir -p <R/tmp/...> && cat > <R/tmp/.../*.py> <<'EOF'` (tạo `f3`, `h1`, `h3`): chúng chạy
  với cwd khởi tạo của shell nhưng chỉ ghi đường dẫn TUYỆT ĐỐI trong `R/tmp/`; không lệnh git/python nào chạy trong `/home/user/tra-luat`.
- Cài `@actions/expressions` vào `R/tmp/npm` (cache npm `R/tmp/npm-cache`), tải từ `registry.npmjs.org`; không cài gì toàn cục.
- Không `pkill`, không xoá đệ quy; tiến trình nền (`tmp/chay_nen.sh`, `tl --selftest`, `tmp/do_hint.sh`) đều đã kết thúc (`ps` cuối lượt: 0).
- Không commit, không push, không đăng GitHub, không chạy CI.

## KẾT LUẬN
`changes_requested` (ngưỡng chủ kho 0 P1 / 0 P2 / 0 P3; mức bảo đảm tối đa của lượt này là `advisory_review` vì cùng họ model — packet
`sensitive` vẫn cần Codex `cross_approved` hoặc `human_audited` ở cổng land).
- P3 lượt 16 `docstring-moi-khai-rong-hon-ma` **ĐÃ VÁ THẬT** ở cả hai câu (4/4 đột biến tự viết làm mệnh đề SAI đúng chỗ; nền: mệnh đề
  ĐÚNG). Bản vá 98377f8 không đổi AST mã chạy (H0). Bất biến head giữ: 4 tệp write set, `ci_dang_ky_test.py` `1 0`, suite `101/101` +
  `301/301` + `TU KIEM DAT` + `TONG DAT`, registry `23/23` + `1025/1025`, actionlint/ruff/doctrine sạch, `tl --selftest 1715/1715`, ruff
  `scripts/tl.py` delta 0.
- Quét TOÀN BỘ chú thích/docstring của diff packet (253 mục: 95 docstring + 158 chú thích) theo PROMPT mục 1 ⇒ hai lớp P3 còn mở:
  **F1** `tin-hieu-chot-ca-khong-doc-quyen` (lời khai "chỉ `bang()` ném; lỗi vô can ⇒ TÍN DỤNG GIẢ" sai, harness cấp GIẾT cho lỗi vô can
  ở `t06`/`t20ze`, phản chứng bắt buộc của CLAUDE.md không đạt — 0/301 bị ảnh hưởng hôm nay) và **F2**
  `chu-thich-khai-rong-hon-ma-con-sot` (năm câu cũ đo được là sai/trôi). Cả hai không đổi hành vi đường nhanh; `HINT.patch` (chỉ chú
  thích) áp sạch trên 98377f8 và đã chạy: suite `101/101 · 301/301 · TONG DAT`, registry `23/23 + 1025/1025`, doc-claims delta 0.
- Đúng đắn đường nhanh: không bằng chứng mới (H5) — bốn ca dữ liệu/cây mà `kiem-re` chạy phủ đúng bốn lối đọc hồ sơ thật của bước bị bỏ.

TONG: P0=0 P1=0 P2=0 P3=2
