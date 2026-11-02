verdict: changes_requested
reviewed_sha: b137bd809b1eaf5a06372703bb0a580ea967689d
provider: claude
role: reviewer
review_kind: advisory_review
model_reviewer_identity: claude-opus-5-5 (Opus 5.5; tự khai — phiên điều phối đối chiếu modelUsage)
independent_from_executor_session: true
assurance: review_deferred
review_axes: [spec, standards_security]

> Ngưỡng đã áp: `review_class`/`effective_review_class: sensitive`, `assurance_target: human_audited` (LEASE-g2). Lượt này CÙNG PROVIDER
> với executor (Claude review mã Claude viết) ⇒ nhãn tối đa `same_provider_approved`, và nhãn ấy KHÔNG thay mức assurance bắt buộc cho
> `sensitive` (§8). Kết luận `changes_requested` ⇒ `assurance: review_deferred`.
> Đếm theo LỚP còn mở: **P0=0 · P1=0 · P2=3 · P3=1 · P4=2** (BẢNG LỚP). Hai P2 vá được bằng mã test (HINT hunk 2–7, đã chạy); P2 thứ ba là
> nghiệm thu Windows (không vá được bằng mã ở Linux); P3 là nợ mồ côi đã khai, chờ quyết định chủ kho.
> Bắt đầu 2026-09-30T08:21:30Z (`bat_dau.txt`). SPEC sha256 đo lại: `18504ced1549cbe62816f067b6ed16f36c12292820c8204cb6085a9c39e80b88` — KHỚP.
> Mọi số dưới đây do lượt này TỰ ĐO trong `$R/tam/` (bản sao tạm), không chép báo cáo executor. Công cụ đo: `tam/cu/{chay_ca,dot_bien,
> ban_kinh_db,dem_phong,do_mo_coi}.py`, `tam/cu/tron_bo.sh`; log: `tam/log/`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

> Commit mới từ lượt advisory `bd6ad5d`: chỉ `b137bd8` (`git diff --numstat bd6ad5d b137bd8 -- ops/` ⇒ `150 54 ops/cong_cu_test.py`;
> `bash_nen.py` không đổi). Nhãn §8: `ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ` (+ `ĐÓNG MỘT PHẦN` cho lớp còn biểu hiện).
> Mọi bằng chứng dưới đây do lượt này tự đo; lệnh/đầu ra đầy đủ ở BẢNG ĐỘT BIẾN / BẢNG SĂN / BẢNG ĐO.

| lớp (slug ổn định) | nguồn | hạng cũ | nhãn trên `b137bd8` | bằng chứng tự đo |
|---|---|---|---|---|
| UTF8-BO-SOT-BO-DOC | lượt 1 `75af95c` | P1 | **ĐÃ VÁ THẬT** (đường `__main__`) | trọn bộ (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`: `56/56 đạt` — `t29/t39/t42/t45` không đỏ; HƯỚNG 3: `main()` chạy ở bản phóng lại `utf8_mode=1` |
| CA-KHOA-UTF8-THIEU-QUAN-SAT (= lượt 2 P2-A, P3-C; advisory P2-A, P3-C) | lượt 1–3 | P2 | **ĐÃ VÁ THẬT** | M61a/b/c/d/e/f/g ⇒ `giet_that` đúng nhãn (a)(b)(c)(d)(f)(g), bán kính 1/56 mỗi cái; biểu hiện 5 (ĐỎ oan dưới `LC_ALL=C`): `t61` `qua` 3.11/3.12/3.13 và trọn bộ (b) 56/56; giàn giáo: G28 (nạp hỏng vô can) ⇒ `t61`/`t62` `tin_dung_gia`, không phải giết |
| TU-PHONG-LAI-CHI-KHOA-CO-UTF8 (= lượt 2 P2-C; advisory P2-C) | lượt 3 `e46f569` | P2 | **ĐÃ VÁ THẬT** | R2 (nuốt mã) ⇒ `t62` (1) · R3 (`-B`) ⇒ (2) · R4 (dấu sót) ⇒ (3) · R5 (bỏ `-X utf8`) ⇒ (4) rc=1 KHÔNG lặp · R6 (chặn lần hai) ⇒ (5) · R8 (`__main__`) ⇒ `t61` (e) · R9 (MỚI, không đặt dấu) ⇒ (4); tất cả 1/56 |
| TU-PHONG-LAI-KHONG-TRONG-SUOT (= lượt 2 P3-B; advisory P3-B, P3-D) | lượt 3 `e46f569` | P2 [(a) P2 · (b) P3 · (c) P4] | **ĐÓNG MỘT PHẦN** | (a) stdin rc=0 rỗng: nền `bd6ad5d` `python -B [-] < cong_cu_test.py` ⇒ `rc=0 stdout=0B`; head ⇒ `rc=1` "KHONG_PHONG_LAI — nguồn '<stdin>' …"; R7 ⇒ `t62` (6) — **ĐÃ VÁ THẬT**. (b) mồ côi: HƯỚNG 10 còn 2 tiến trình sau khi harness giết bao — **CHƯA VÁ, đã KHAI** trong mã (P3-D của advisory: lời khai "chỉ Windows" nay đúng ⇒ đóng). (c) SIGTERM ⇒ 241: đo lại 241, đã ghi chú theo hướng lượt 3 ("chấp nhận, ghi chú") — đóng |
| CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG (= lượt 2 P2-B; advisory P2-B) | lượt 1 `75af95c` | P2 | **ĐÓNG MỘT PHẦN** | chiều "stage hỏng mà vẫn XANH/đo tiếp": M49a/b/c/d/e/h ⇒ `t63` `giet_that` đúng bước — ĐÃ VÁ THẬT. Chiều "stage hỏng ⇒ ĐỎ OAN" (spec §2B "không ĐỎ oan"): M49i/M49l/M49m/M49n **SỐNG** trên cả 57 ca (`t63` đổi `TinHieuChotCa` của `t49` thành BỎ QUA "vì chốt khác") — HƯỚNG 6 |
| (advisory `bd6ad5d` P2-E) T49-CO-CHE-HOAN-BO-QUA | advisory `bd6ad5d` | P2 | **CHƯA VÁ theo quyết định S5** (cơ chế còn nguyên) | 5 dòng `bo_qua_va` (HƯỚNG 12); thân commit tự khai "CHUA bo (S5, vong sau)". Ba đột biến của P2-E: (i) nuốt `raise` = M49f ⇒ nay CHẾT (`t63`); (ii) ném sớm = M49g ⇒ nay CHẾT; (iii) quét cả khi stage hỏng = M49i ⇒ **VẪN SỐNG** |
| NGHIEM-THU-WINDOWS-CON-THIEU (= lượt 2 P2-D; advisory P2-D) | lượt 1 | P2 | **CHƯA VÁ — KHÔNG ĐO ĐƯỢC ở Linux** | hiện vật lượt này không có log/receipt Windows nào cho `b137bd8`; số Windows duy nhất vẫn là lời khai trong thân `e46f569` (47/51 trên `75af95c`) và `bd6ad5d` ("52 qua / 4 bỏ qua", môi trường CI) — không neo exact head, không §6.1–6.3 |
| LOI-KHAI-RONG-HON-PHEP-DO (= lượt 2 P3-A; advisory P3-A) | lượt 1–3 | P3 | **ĐÃ VÁ THẬT** (trong mã) | "66" 0 lần; chú thích `:14-18` "36 Call … 12/3/3/18" khớp AST (HƯỚNG 13); `:37-40` trỏ `t61` (e), `t62` (1)–(6) — mỗi trỏ có đột biến chết; `t61` docstring không còn suy từ mã thoát. Biểu hiện MỚI (thuộc lớp STAGING, không tách lớp): docstring/thông điệp `t63` "`t49` đỏ … vì lý do KHÁC ⇒ KHÔNG ĐO ĐƯỢC" / "ĐỎ vì chốt khác" — sai với M49m (đỏ do CHÍNH phép tráo) |
| TEN-CA-LECH-SPEC | lượt 3 | P4 | **theo quyết định chủ kho** (khai ở PR, không đổi tên) | `t52` 0 lần, `t60_import_bash_nen_khong_in_gi_ra_stderr` `:2248`; thân PR: KHÔNG ĐO ĐƯỢC (không gọi mạng) ⇒ còn P4 tới khi PR khai |
| CON-TRO-CA-CU | lượt 1 | P4 | ĐÃ VÁ THẬT (từ lượt 3) | `t60b` 0 lần |

**Lời khai riêng của executor ("lớp 1 đóng 8/10, lớp 2 9/9, lớp 3 8/8, lớp 4 6/6")** — đo:

| lớp | executor khai | đo được | khớp? |
|---|---|---|---|
| 1 tự phóng lại | 8/10 đường đóng (1.1–1.8); 1.9 mồ côi, 1.10 tín hiệu là NỢ | 1.1–1.8: R1–R8 `giet_that` đúng vế (+R9 của tôi); 1.9: 2 tiến trình mồ côi; 1.10: rc 241 | **khớp** (và executor không khai "đóng lớp") |
| 2 `t61` | 9/9 | 2.1–2.6: M61a/c/b/e/d/f/g giết; 2.7: `t61` xanh dưới `LC_ALL=C` + đường dẫn có dấu (HƯỚNG 5); 2.8: G28 ⇒ `tin_dung_gia`; 2.9 = R8 | **khớp** |
| 3 staging `t49` | 8/8 — "ĐÃ ĐÓNG" | 3.1–3.8 (M49a/b/c/d/f/g/h/e) giết đúng bước; nhưng danh sách đường **bỏ sót chiều ĐỎ OAN** — M49i/M49l/M49m/M49n sống 57/57 | **KHÔNG khớp**: "8/8 đường đã liệt kê" đúng, "lớp ĐÃ ĐÓNG" sai (lời khai rộng hơn phép đo) |
| 4 lời khai | 6/6 | 4.1–4.6 đo khớp (HƯỚNG 13, R-mutations) | **khớp**; lời khai mới lệch nằm trong `t63` (xem lớp STAGING) |

## BẢNG LỚP
| slug lớp | finding/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| T49-CO-CHE-HOAN-BO-QUA | cơ chế hoãn `bo_qua_va` còn nguyên (5 dòng); quyết định S5 chủ kho (30-09) chưa thi hành; đột biến (iii) của P2-E sống | **P2** | advisory `bd6ad5d` P2-E; S5; còn ở `b137bd8` | (3) lên TRƯỚC (2d), stage đứng CUỐI, `BoQuaMoiTruong` nổ tự nhiên — HINT hunk 2–4 (mã test) | `grep bo_qua_va` = 0; trên HINT: H49f (nuốt⇒return) ⇒ `t63` (update-index/bo_ten), H49g (stage trước (3)) ⇒ `t63` (bo_ten), H49l (nuốt⇒quét tiếp) ⇒ `t63` ĐỎ OAN; `t49`,`t63` `qua` 3.11/3.12/3.13 × 2 locale; Windows: KHÔNG ĐO ĐƯỢC |
| CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG | (1)–(4) lượt 1 + 3.7 (`git add -A` không rc): ĐÃ ĐÓNG. MỚI mở: chiều "stage hỏng ⇒ ĐỎ OAN" không có khoá — M49i, M49l, M49m, M49n sống 57/57; `t63` ghi nhầm "t49 ĐỎ vì chốt khác"; docstring `t63` "đỏ … vì lý do KHÁC ⇒ KHÔNG ĐO ĐƯỢC" rộng hơn phép đo | **P2** | lượt 1 `75af95c` → `b137bd8` đóng một phần | MỘT gốc: `t63` đổi MỌI `TinHieuChotCa` của `t49` thành BỎ QUA. Vá chung: `t63` chạy `t49` KHÔNG tráo làm đối chứng; đối chứng XANH mà ĐỎ dưới phép tráo ⇒ `bang` (giết) — HINT hunk 5–7 (mã test) | trên HINT: M49m ⇒ "(hash-object/rc) … ĐỎ OAN", M49n ⇒ "(add/rc) … ĐỎ OAN", H49l ⇒ "(update-index/bo_ten) … ĐỎ OAN"; 4 `DOT_BIEN` đích `t49` vẫn `{t49: giet_that, t63: bo_qua}` (1/N) |
| NGHIEM-THU-WINDOWS-CON-THIEU | không có §6.1–6.3 trên Windows cho exact head `b137bd8` (N/N, danh sách bỏ qua + lý do, delta lỗi đột biến so nền cùng máy, lượt ép ASCII, đột biến (i)(ii)); giả thuyết B và "Git for Windows bỏ tên mang `\`" chỉ là lời khai trong thân commit | **P2** (spec §6) | lượt 1 → nay | không vá được bằng mã; chạy checklist §6 trên máy Windows local neo head SAU khi vá (chủ kho: "Chỉ chạy tại máy") | KHÔNG ĐO ĐƯỢC ở Linux |
| TU-PHONG-LAI-KHONG-TRONG-SUOT | (a) stdin rc=0 rỗng: ĐÓNG; (b) harness giết tiến trình bao ⇒ bản `-X utf8` mồ côi (đo: 2 tiến trình) — đã KHAI trong mã, có hướng; (c) SIGTERM ⇒ 241: ghi chú, đóng | **P3** (biểu hiện (b), giữ hạng lượt 3) | lượt 3 `e46f569` | cần QUYẾT ĐỊNH chủ kho: nhận nợ có tên + packet kế nhiệm, hay vá (POSIX `os.execve` + khoá ép nhánh `subprocess` cho `t62`; Windows Job Object) — không hunk: vá POSIX một mình để nguyên nhánh Windows (nền đích packet) mồ côi | HƯỚNG 10/11; Windows: KHÔNG ĐO ĐƯỢC |
| T62-GHI-PYC-VAO-CAY | `t62` (4) `hoi("-X","utf8=0",…)` thiếu `-B` sau khi gỡ `PYTHONDONTWRITEBYTECODE` ⇒ ghi `ops/__pycache__/{bash_nen,lease_publish_test}.cpython-312.pyc` vào cây đang đo | **P4** | MỚI, `b137bd8` (nền `bd6ad5d` không có) | thêm `-B` vào (4) và (5) — HINT hunk 1 (mã test) | trên HINT: 0 tệp `.pyc`; R5/R6/R9 vẫn giết `t62` (4)/(5) |
| TEN-CA-LECH-SPEC | spec `t52` → mã `t60` (+`t61`/`t62`/`t63`) | **P4** | lượt 3 | quyết định chủ kho: khai ở PR, không đổi tên | thân PR: KHÔNG ĐO ĐƯỢC |
| UTF8-BO-SOT-BO-DOC · CA-KHOA-UTF8-THIEU-QUAN-SAT · TU-PHONG-LAI-CHI-KHOA-CO-UTF8 · LOI-KHAI-RONG-HON-PHEP-DO · CON-TRO-CA-CU | — | đóng | lượt 1–3 | — | xem ĐỐI CHIẾU |

Đếm: **6 lớp còn mở** (P2×3 · P3×1 · P4×2); **5 lớp đóng**. Biểu hiện còn mở: HOAN 2 (cơ chế còn; M49i) + STAGING 5 (M49i, M49l, M49m, M49n, lời khai `t63`) + WINDOWS 3 (§6 cho head; giả thuyết B; danh sách bỏ qua) + KHONG-TRONG-SUOT 1 ((b)) + PYC 1 + TEN-CA 1 = **13** (M49i đếm ở cả hai lớp vì nó là đột biến (iii) của P2-E và cùng gốc `t63`; không trùng khi đếm lớp).

## BẢNG SĂN

> Môi trường: container Linux, `python3.12` 3.12.3 (đo chính), 3.11.15 / 3.13.12 để so, git 2.43.0, KHÔNG `jsonschema`.
> `TMPDIR=$R/tam`, `PYTHONDONTWRITEBYTECODE=1`, xoá `__pycache__` trước mỗi lượt. Mọi phép đo trên bản sao tạm trong `$R/tam/`.

```
HƯỚNG 1: dấu chống lặp `CONG_CU_TEST_DA_PHONG_LAI` sót sang con/cháu, hoặc bị ca nào vô tình đặt
  giả thuyết : nếu dấu sót sang cháu thì mọi cháu Python chạy `cong_cu_test.py` ngoài UTF-8 sẽ tự từ chối (đỏ oan)
  lệnh       : grep -n "CONG_CU_TEST_DA_PHONG_LAI\|_DAU_PHONG_LAI" ops/cong_cu_test.py ; git grep (các tệp khác)
               cd tam/h1 && env -u PYTHONDONTWRITEBYTECODE LC_ALL=C.UTF-8 PYTHONUTF8=0 strace -f -v -s 80 -e trace=execve \
                  python3.12 -B ops/cong_cu_test.py --tu-kiem-cong-that tam/h1      (cửa này phóng `bash_nen quet` + git)
  output     : chỗ đặt dấu: :45 (tên), :46 `pop`, :53 (env của lần phóng lại), :2357 (`t62` (5), CỐ Ý), :6952 (cửa in) — tệp khác: 0
               rc=0 `KQ [0, ["CỔNG TRÊN CÂY THẬT: ĐẠT …"]]` ; 39 execve, đúng 1 execve mang dấu:
               6142 python3.12 -B ops/cong_cu_test.py …              PYTHONUTF8=0
               6187 /usr/bin/python3.12 -X utf8 -B ops/cong_cu_test.py … PYTHONUTF8=1 PYTHONIOENCODING=utf-8 CONG_CU_TEST_DA_PHONG_LAI=1
               6233 python3.12 …/bash_nen.py quet …                   PYTHONUTF8=1 PYTHONIOENCODING=utf-8   (KHÔNG dấu)
               6244 git --no-replace-objects …                        PYTHONUTF8=1 PYTHONIOENCODING=utf-8   (KHÔNG dấu)
  kết luận   : KHÔNG PHẢI LỖI — dấu chỉ nằm trên đúng execve phóng lại; cháu không thừa hưởng; không ca nào vô tình đặt.

HƯỚNG 2: `__file__` không phải tệp ở các dạng gọi khác (`-m`, symlink, /dev/stdin, ống, process substitution, zipapp, -c)
  giả thuyết : nếu `isfile(__file__)` sai chiều thì một dạng gọi hoặc phóng lại chương trình RỖNG (rc=0) hoặc từ chối oan
  lệnh       : env -u PYTHONDONTWRITEBYTECODE LC_ALL=C.UTF-8 PYTHONUTF8=0 python3.12 -B <dạng> --tu-kiem-che-do-utf8  (tam/h1)
  output     : tệp (đối chứng)            rc=5 UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0
               -m ops.cong_cu_test        rc=5 UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0
               symlink ngoài cây          rc=5 UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0
               /dev/stdin < tệp thường    rc=5 UTF8_MODE=1 …   (mở lại /proc/self/fd/0 của tệp thường ⇒ đọc lại từ đầu)
               cat tệp | … /dev/stdin     rc=1 "KHONG_PHONG_LAI — nguồn '/dev/stdin' không đọc lại được"
               <(cat tệp)                 rc=1 "… nguồn '/dev/fd/63' …"
               - < tệp (cwd=ops)          rc=1 "… nguồn '<stdin>' …"
               -c 'exec(open(…).read())'  rc=1 "… nguồn '' …"
               zipapp cct.pyz             rc=1 "… nguồn '…/cct.pyz/__main__.py' …" (có PYTHONUTF8=1 thì vẫn hỏng: ModuleNotFoundError — dạng không được hỗ trợ ở cả nền)
               -I -B / -E -B / -I -X utf8=0 -B  rc=5 UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0 (cả ba)
               -B -W error::SyntaxWarning rc=1 SyntaxError '\s' ở `lease_publish_test.py` (nợ ngoài write set, spec §3 — có từ nền)
  kết luận   : KHÔNG PHẢI LỖI — mọi dạng đọc lại được thì phóng đúng; dạng không đọc lại được thì DỪNG ồn ào rc=1, không dạng nào ra rc=0 rỗng.

HƯỚNG 3: `t62` có đo đúng tiến trình CHẠY BỘ CA không (cửa và `main()` cùng một loại tiến trình?)
  giả thuyết : nếu cửa `--tu-kiem-che-do-utf8` chạy ở tiến trình khác `main()` thì t62 xanh mà bộ ca vẫn ngoài UTF-8
  lệnh       : bản sao tam/h3, chèn vào ĐẦU `main()` một dòng in `utf8_mode pid ppid DA_PHONG_LAI` rồi thoát; chèn vào cửa in `pid ppid`
               env -u PYTHONDONTWRITEBYTECODE <E> python3.12 -B ops/cong_cu_test.py [--tu-kiem-che-do-utf8]
  output     : PYTHONUTF8=0 LC_ALL=C.UTF-8: MAIN utf8_mode=1 pid=14687 ppid=14680 DA_PHONG_LAI=1 (ppid = python bao, không phải shell 14262)
                                            GATE pid=14730 ppid=14715 → UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0
               PYTHONUTF8=0 LC_ALL=C      : MAIN utf8_mode=1 … DA_PHONG_LAI=1 ; GATE … DA_PHONG_LAI=1
               PYTHONUTF8=1               : MAIN utf8_mode=1 pid=14972 ppid=14262 DA_PHONG_LAI=0 (không phóng lại)
  kết luận   : KHÔNG PHẢI LỖI — `main()` chạy trong CHÍNH loại tiến trình mà cửa báo (bản phóng lại, UTF-8); đo bằng đo đạc, không suy từ vị trí mã.

HƯỚNG 4: mã thoát 5 của cửa tự kiểm có va chạm mã nào khác
  giả thuyết : nếu một đường khác cũng ra 5 thì chốt (1) "mã thoát đi qua" xanh oan
  lệnh       : grep -n "sys.exit(\|os._exit(" ops/cong_cu_test.py ; git grep -n "cong_cu_test" (consumer) ; grep "== 5\|in (0, 5)"
  output     : mã của tệp: main 0/1 · --tu-kiem-cong-that 0/9 · --ban-kinh-con `ma_thoat` 0/7 · các cửa tự kiểm khác 0 ·
               KHONG_PHONG_LAI `sys.exit(str)` ⇒ 1 · cửa UTF-8 ⇒ 5 (DUY NHẤT). Consumer: `ci.yml:113 python ops/cong_cu_test.py`
               (đòi 0), `.claude/dev/ci_dang_ky_test.py` chỉ liệt kê chuỗi lệnh; không ai đọc mã 5. Con chết tín hiệu ⇒ `sys.exit(-N)`
               ⇒ 256−N (≠ 5 với mọi tín hiệu 1..64).
  kết luận   : KHÔNG PHẢI LỖI.

HƯỚNG 5: `t61` (mã con `encode("ascii","backslashreplace")`) và `t62`/`t63` khi đường dẫn kho mang chữ Việt + dấu cách
  giả thuyết : nếu argv mang byte ngoài ASCII dưới `LC_ALL=C` thì con chết lúc giải mã (đúng lỗi lượt 3 biểu hiện 5)
  lệnh       : git clone --shared head "tam/có dấu cách/kho việt" ; <py> -X utf8 tam/cu/chay_ca.py ops/cong_cu_test.py t49 t60 t61 t62 t63
               (thường và `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`, 3.11/3.12/3.13) ; cửa UTF-8 gọi bằng đường dẫn có dấu dưới LC_ALL=C
  output     : 6 lượt × 5 ca ⇒ `TONG {"qua": 5}` cả sáu ; cửa: `UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0` rc=5
  kết luận   : KHÔNG PHẢI LỖI — đường dẫn đi qua argv RIÊNG (surrogateescape khứ hồi), mã `-c` thuần ASCII.
```

```
HƯỚNG 6: `t63` bơm lỗi có đo đúng chốt, hay bị chốt khác bắt hộ / có chiều nào bị quy nhầm
  giả thuyết : `t63` chỉ đòi "BỎ QUA đúng bước"; nếu `t49` ĐỎ dưới phép tráo thì `t63` đổi thành BỎ QUA ("chốt khác") —
               tức chiều "stage hỏng ⇒ ĐỎ OAN" mà spec §2B cấm KHÔNG có ca nào khoá
  lệnh       : python3.12 tam/cu/dot_bien.py M49i_quet_ca_khi_stage_hong M49l_nuot_bo_qua_va M49m_stage_hong_thanh_DO M49n_add_hong_thanh_DO
               (+ `--tat-ca` cho bán kính trên cả 57 ca)
               M49m = trong `_stage_byte`: `raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC: INDEX …` → `bang(False, f"KHÔNG ĐO ĐƯỢC: INDEX …`
               M49n = trong `_add`:       `raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC: git add …` → `bang(False, …)`
               M49i = `if bo_qua_va is None:` (trước `quet(d_va)`) → `if True:` ; M49l = `bo_qua_va = e` → `pass`
  output     : M49m  t63 bo_qua: "KHÔNG ĐO ĐƯỢC: t49 ĐỎ vì chốt khác khi tráo hash-object/rc: KHÔNG ĐO ĐƯỢC: INDEX không nhận tên b'ops/xau_\xff.py': rc=128/0 b''" ; t49 qua
               M49n  t63 bo_qua: "… t49 ĐỎ vì chốt khác khi tráo add/rc: KHÔNG ĐO ĐƯỢC: git add ops/bình_thường.py rc=128 ''" ; t49 qua
               M49i  t63 bo_qua: "… t49 ĐỎ vì chốt khác khi tráo update-index/bo_ten: (2d) HAI đường … chỉ còn MỘT khoá …" ; t49 qua
               M49l  (như M49i)
               bán kính M49i/M49l/M49m/M49n trên CẢ 57 ca: mỗi cái `TONG {"qua": 55, "bo_qua": 2}` KHONG_QUA=[] BO_QUA=['t2','t63']
  kết luận   : LỖI (P2, lớp CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG — đóng MỘT PHẦN). Đúng hình dạng lỗi gốc của packet (Windows: stage
               hỏng ⇒ `t49` ĐỎ `(2) chiều ngược: … []`) mà không ca nào trên Linux bắt; thông điệp "vì chốt khác" còn quy nhầm nguyên nhân.
               M49i chính là đột biến (iii) "quét cả khi stage hỏng ⇒ ĐỎ oan" của advisory `bd6ad5d` P2-E — vòng vá không dùng HINT ấy nên
               bỏ sót đúng đường thứ ba ("vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba").

HƯỚNG 7: bán kính đột biến có bị ca mới kéo rộng (tín dụng giả / "giết THÊM") không
  giả thuyết : `t63` gọi `t49` trong tiến trình; nếu nó không tách được "t49 đỏ vì sản phẩm" thì mọi `DOT_BIEN` đích `t49` giết thêm `t63`
  lệnh       : python3.12 -X utf8 tam/cu/ban_kinh_db.py ops/cong_cu_test.py bn_ngay_go_chi_la_chu bn_hien_thi_khong_don_anh \
                   bn_loi_ra_duong_tho bn_json_khong_ascii        (gọi `_do_ban_kinh` CỦA CHÍNH tệp, cả 57 ca; trên head và trên HINT)
               python3.12 tam/cu/dot_bien.py --tat-ca <27 đột biến tay>   (tam/log/dot-bien-tatca-312.txt)
  output     : head và HINT, cả 4 mục: không-qua = {'t2': 'bo_qua', 't49': 'giet_that', 't63': 'bo_qua'}  ⇒ bán kính 1/N
               đột biến tay: mỗi cái giết ĐÚNG 1 ca (1/56 chạy được); M49e: 1/55 (t49 bo_qua — đúng: KHÔNG ĐO ĐƯỢC, không ĐỎ oan)
               `DOT_BIEN` = 212 mục (bằng nền); ca KHÔNG có mục DOT_BIEN: 12 (nền 89fc4fa: 8; thêm t60 t61 t62 t63 — spec chỉ đòi đột biến tay)
  kết luận   : KHÔNG PHẢI LỖI (trọn bộ: xem BẢNG ĐO — dòng "giết THÊM").

HƯỚNG 8: `t5` SIGPIPE `rc=141` có liên quan PR không
  giả thuyết : nếu PR đổi môi trường con của `t5` thì chập chờn là hồi quy
  lệnh       : git diff 89fc4fa b137bd8 --stat ; grep -n pipefail ops/cai_cong_cu.sh ; sed -n 64p ops/cai_cong_cu.sh ;
               git -C kho.git merge-base --is-ancestor d553efa5 89fc4fa ; grep "rc=141" tam/log/head-*.txt
  output     : PR chỉ đổi 2 tệp (`bash_nen.py` 2 dòng, `cong_cu_test.py`); `t5`/`cai_cong_cu.sh` KHÔNG trong diff;
               `ops/cai_cong_cu.sh:7 set -euo pipefail` + `:64 LENH="$(printf '%s\n' "$DAU_RA" | head -1)"` ⇒ cơ chế SIGPIPE có sẵn ở nền;
               `master` trong kho.git = d553efa5 là TỔ TIÊN của merge-base ⇒ bản sao master CŨ, không mang #675 ⇒ bản vá #675: KHÔNG ĐO ĐƯỢC ở đây
  kết luận   : KHÔNG PHẢI LỖI của PR (có ở nền; hết khi nhánh ghép master sau #668 → #675). Số lần gặp trong trọn bộ của lượt này: xem BẢNG ĐO.

HƯỚNG 9: ca mới có ghi vào cây đang đo không (bẫy `.pyc`, §8.2)
  giả thuyết : `t62` gỡ `PYTHONDONTWRITEBYTECODE` khỏi env con (để đo `-B`); lời gọi nào thiếu `-B` sẽ ghi `ops/__pycache__` vào cây THẬT
  lệnh       : với mỗi ca c ∈ {t49,t60,t61,t62,t63} và mỗi cây ∈ {head b137bd8, nền bd6ad5d}: clone --shared mới,
               PYTHONDONTWRITEBYTECODE=1 python3.12 -X utf8 tam/cu/chay_ca.py ops/cong_cu_test.py c ; find -name '*.pyc'
  output     : head t62 ⇒ ops/__pycache__/lease_publish_test.cpython-312.pyc + ops/__pycache__/bash_nen.cpython-312.pyc ; head t49/t60/t61/t63 ⇒ 0
               nền t62 ⇒ 0 (bd6ad5d: env con thừa hưởng PYTHONDONTWRITEBYTECODE) ; chạy `_do_ban_kinh` trên head cũng để lại hai tệp ấy trong cây
               bản HINT (thêm `-B` vào `t62` (4)(5)): 0 tệp
  kết luận   : LỖI (P4, T62-GHI-PYC-VAO-CAY) — `t62` (4) `hoi("-X","utf8=0",…)` thiếu `-B`: bộ ca ghi bytecode vào CHÍNH checkout nó đo
               dù người chạy đã tắt ghi bytecode; reviewer chạy bộ ca trong checkout read-only sẽ thấy snapshot "ignored" đổi. `t60` miễn
               nhiễm (chép bash_nen ra thư mục tạm) nên không câm chốt nào đã đo — vì vậy chỉ P4.

HƯỚNG 10: mồ côi / mã thoát tín hiệu của lần phóng lại (nợ 1.9/1.10 executor khai) — đo lại trên b137bd8
  giả thuyết : harness có hạn chót `kill()` đúng MỘT tiến trình ⇒ bản `-X utf8` chạy tiếp
  lệnh       : python3.12 tam/cu/do_mo_coi.py tam/mc   (Popen trong session RIÊNG, wait(timeout=5) → kill → đếm tiến trình còn trong
               session sau 2s; SIGTERM tới con `-X utf8`; dọn bằng killpg)
  output     : (i)  PYTHONUTF8=0: bao rc=-9; còn sống sau 2s: 2 [(…,'/usr/bin/python3.12 -X utf8 -B ops/cong_cu_test.py'), (…,'… -B - --tu-kiem-che-do-utf8')]
               (ii) PYTHONUTF8=0: SIGTERM tới con ⇒ rc bao=241
               (i)  PYTHONUTF8=1: bao rc=-9; còn sống: 0 (đối chứng)
  kết luận   : LỖI đã KHAI (P3, TU-PHONG-LAI-KHONG-TRONG-SUOT biểu hiện (b), giữ hạng lượt 3) — chú thích khối phóng lại nay nói đúng
               ("mồ côi trên CẢ POSIX … mã 241"), nên P3-D của advisory `bd6ad5d` (lời khai "chỉ Windows") ĐÃ ĐÓNG; hành vi còn nguyên,
               cần quyết định chủ kho (nhận nợ có tên + packet kế nhiệm, hay vá). Số "3 tiến trình" trong chú thích là ảnh chụp theo thời điểm (đo được 2).

HƯỚNG 11: nhánh phóng lại có phải chỉ của Windows không (phạm vi của nợ HƯỚNG 10)
  lệnh       : for e in "-u LANG -u LC_ALL" LC_ALL=C LC_ALL=C.UTF-8 LANG=C.UTF-8 LANG=en_US.UTF-8; do env $e python3.1x -c 'print(sys.flags.utf8_mode)'
  output     : không LANG / LC_ALL=C ⇒ 1 (PEP 540 tự bật) ; LC_ALL=C.UTF-8 / LANG=C.UTF-8 ⇒ 0 (3.11/3.12/3.13) ; en_US.UTF-8 không có trong container
  kết luận   : KHÔNG PHẢI LỖI riêng — nhưng đo được rằng máy Linux dev thông thường (locale `*.UTF-8`, không `PYTHONUTF8`) CŨNG đi nhánh
               phóng lại ⇒ nợ mồ côi không chỉ của Windows (đúng như chú thích mới khai). CI đặt `PYTHONUTF8=1` nên không chạm.

HƯỚNG 12: cơ chế hoãn `bo_qua_va` (S5 chủ kho 30-09: BỎ) còn trong b137bd8 không
  lệnh       : grep -c "bo_qua_va" ops/cong_cu_test.py ; git log -1 --format=%B b137bd8 | grep -i hoan
  output     : 5 dòng / 5 lần (`:5663` `= None`, `:5668` `= e  # ném SAU (3)`, `:5669` `if … is None:`, `:5693` `if … is not None:`, `:5694` `raise`)
               thân commit: "Co che hoan bo_qua_va cua bd6ad5d CHUA bo (S5, vong sau)."
  kết luận   : LỖI (P2, T49-CO-CHE-HOAN-BO-QUA) — quyết định chủ kho chưa thi hành; HINT hunk 2–4 theo đúng hướng đã chốt.

HƯỚNG 13: lời khai số trong chú thích đầu tệp (AST) và trong BAO_CAO §4
  lệnh       : python3.12 tam/cu/dem_phong.py <tệp@SHA> (-v) ; truy tay 18 `env=` dạng biến
  output     : 89fc4fa: S=49 · chay 26 · _g 27 · env= 33 {Name 16, moi_truong 12, dict(os.environ) 3, {**os.environ} 2}
               bd6ad5d: S=56 · chay 26 · _g 25 · env= 35 {Name 18, moi_truong 12, dict(os.environ) 3, {**os.environ} 2}
               b137bd8: S=54 · chay 26 · _g 23 · goi_git 4 · env= 36 {Name 17, moi_truong 12, dict(os.environ) 3, dict(biến) 1, {**os.environ} 3}
               18 `env=` dạng biến ⇒ `chay(env=None)`, `bk_don`→`moi_truong(d)` (10), `moi_truong(...)`, `dict(os.environ…)` (:1984 :2214 t61),
               `_quet`/`danh_sach(env=None)` với người gọi truyền `dict(os.environ,…)`/`{**os.environ,…}`, `t62` `dict(env, **them)` ; os.system/exec*/spawn*: 0
  kết luận   : KHÔNG PHẢI LỖI — chú thích `:14-18` ("36 Call … 12 / 3 / 3 / 18") khớp phép đo; câu "Điểm phóng viết SAU … chưa ca nào khoá" nói đúng giới hạn.

HƯỚNG 14: chi phí thời gian của ca mới trong pha bán kính (212 đột biến × mọi ca) — trần `gate` 60 phút
  giả thuyết : `t62` (7 tiến trình Python) + `t63` (7 lần `t49`) chạy lại cho MỌI đột biến ⇒ kéo dài `gate`, nhất là trên Windows
  lệnh       : chay_ca.py --tat-ca trên 89fc4fa / bd6ad5d / b137bd8 / HINT (máy rảnh, 2 lần) ; strace -f -e trace=execve (t62) ;
               grep -n "timeout-minutes" .github/workflows/ci.yml
  output     : một vòng CA: 21,5–23,2 s · 21,9–23,5 s · 22,6–24,7 s · 24,2–26,3 s ; t60–t63: 0 · 0,93 · 2,68–3,62 · 3,07–3,74 s
               t62: 7 execve python (vế (1)(4) mỗi vế 2, (5) 1, (6) 2) ; `gate` timeout-minutes: 60 (`ci.yml:68`), CI đặt PYTHONUTF8=1
               trọn bộ head (a)/(b) trên Linux: 45m34s / 45m41s với 2 tiến trình, chạy song song và dưới tải thêm của reviewer
  kết luận   : KHÔNG PHẢI LỖI trên Linux (+~1,5–2,5 phút với 4 tiến trình); trên Windows KHÔNG ĐO ĐƯỢC — ghi vào mục nghiệm thu Windows
               (so thời lượng bước `cong_cu_test` với nền trên CÙNG máy).

HƯỚNG 15: giàn giáo `t61`/`t62` có biến lỗi nạp VÔ CAN thành "giết" không (tín dụng giả)
  lệnh       : G28 = chèn `if os.environ.get('PYTHONIOENCODING') == 'ascii': raise KeyError('rv4_vo_can')` ngay trước `_ep_utf8()` (chỉ nổ
               trong tiến trình con mà t61/t62 dựng) ; python3.12 tam/cu/dot_bien.py G28_nap_hong_vo_can
  output     : t61 tin_dung_gia "giàn giáo: nạp cong_cu_test.py hỏng, chưa tới chốt nào: rc=1 stdout=b'(0) nap\n' …"
               t62 tin_dung_gia "giàn giáo … cửa --tu-kiem-che-do-utf8 không in gì: rc=1 …"
  kết luận   : KHÔNG PHẢI LỖI — `dung` (`NAP_OK`, cửa không in gì) tách đúng giàn giáo khỏi chốt nghiệp vụ.
```

## BẢNG ĐỘT BIẾN

> Công cụ: `tam/cu/dot_bien.py` — mỗi đột biến `git clone --shared` từ bản sao sạch (head: `tam/head` @`b137bd8`; HINT: `tam/hint`/`tam/ap3`,
> chép cây làm việc), thay ĐÚNG MỘT lần mỗi mỏ neo (assert đếm == 1), xoá `__pycache__`, `PYTHONDONTWRITEBYTECODE=1`, rồi `tam/cu/chay_ca.py`
> nạp tệp bằng importlib (tên module ≠ `__main__`) và chạy ca qua `_chay_1_ca` CỦA CHÍNH tệp ⇒ `giet_that` chỉ khi `TinHieuChotCa` mang đúng
> tên ca. Tiến trình đo chạy `-X utf8` (như bộ ca sau phóng lại). Cột "57 ca": `--tat-ca` chạy LẠI toàn bộ `CA` trên cùng bản sao
> (`tam/log/dot-bien-tatca-312.txt`). Đối chứng không đột biến (head): `t49 t60 t61 t62 t63` ⇒ `qua` trên 3.11/3.12/3.13 × (thường,
> `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`); vòng CA không đột biến ⇒ `qua 56, bo_qua 1` (`t2`, thiếu jsonschema).

**Trên head `b137bd8`**

| đột biến (thay đúng 1 chỗ) | ca đích | kết quả ca đích (3.12) — tín hiệu | 57 ca | phân loại |
|---|---|---|---|---|
| R1 gỡ khối phóng lại (`if False:`) | t62 | `giet_that` "chạy làm __main__ … KHÔNG ở chế độ UTF-8: 'UTF8_MODE=0 B=1 …'" | 1/56 | giết thật |
| R2 nuốt mã thoát (`.returncode * 0`) | t62 | `giet_that` "(1) mã thoát KHÔNG đi qua lần phóng lại: rc=0, chờ 5" | 1/56 | giết thật |
| R3 `sys.argv` thay `sys.orig_argv[1:]` | t62 | `giet_that` "(2) cờ `-B` mất … B=0" | 1/56 | giết thật |
| R4 `.get` thay `.pop` (dấu sót) | t62 | `giet_that` "(3) dấu phóng lại còn … DAU_SOT=1" | 1/56 | giết thật |
| R5 bỏ `"-X", "utf8"` | t62 | `giet_that` "(4) gọi `-X utf8=0` … rc=1 … KHONG_PHONG_LAI" (không lặp) | 1/56 | giết thật |
| R6 bỏ `_DA_PHONG_LAI or` (chặn lần hai) | t62 | `giet_that` "(5) … rc=5 'UTF8_MODE=1 …'" | 1/56 | giết thật |
| R7 bỏ `not os.path.isfile(_nguon)` | t62 | `giet_that` "(6) `python -B - …` … rc=0 stdout=0 ký tự" | 1/56 | giết thật |
| R8 bỏ `__name__ == "__main__"` | t61 | `giet_that` "(e) NẠP … bị PHÓNG LẠI … `(0) nap\n(0) nap`" | 1/56 | giết thật |
| R9 (MỚI) không đặt dấu cho con (`env={**os.environ}`) | t62 | `giet_that` "(4) … 'DA_PHONG_LAI=0'" | 1/56 | giết thật |
| R10 (MỚI) từ chối nhưng thoát 0 (`sys.exit(sys.stderr.write(…) * 0)`) | t62 | `giet_that` "(5) … rc=0 … KHONG_PHONG_LAI" | — | giết thật |
| M61a gỡ `reconfigure` | t61 | `giet_that` "(a) … rc=1" | 1/56 | giết thật |
| M61c chỉ reconfigure stdout | t61 | `giet_that` "(c) stderr … không mang chữ Việt UTF-8 THẬT" | 1/56 | giết thật |
| M61b gỡ env cho con (spec §6.3 ii) | t61 | `giet_that` "(b) cháu … không in được byte UTF-8 thật" | **1/56** | giết thật; bán kính 1/N ✔ |
| M61e con `ascii:backslashreplace` | t61 | `giet_that` "(b) … `(b) ch\\u1eef Vi\\u1ec7t`" | 1/56 | giết thật |
| M61d bỏ `PYTHONUTF8` | t61 | `giet_that` "(d) … `[0, "0", "utf-8"]`" | 1/56 | giết thật |
| M61f bỏ `hasattr` | t61 | `giet_that` "(f) … `(f) AttributeError`" | 1/56 | giết thật |
| M61g `errors="strict"` | t61 | `giet_that` "(g) … rc=1" | 1/56 | giết thật |
| G28 (MỚI) nạp hỏng VÔ CAN chỉ trong con ASCII | t61, t62 | `tin_dung_gia` cả hai ("giàn giáo … chưa tới chốt nào" / "cửa … không in gì") | — | đúng: không cấp tín dụng |
| M60a docstring raw → thường ở `bash_nen.py` (spec §6.3 i) | t60 | `giet_that` "(1) … SyntaxError: invalid escape sequence '\(' (bash_nen.py, line 898)" | **1/56** | giết thật; bán kính 1/N ✔ |
| M49a bỏ `oid.returncode` | t63 | `giet_that` "(hash-object/rc) … chờ 'rc=128/0'"; t49 `qua` | 1/56 | giết thật |
| M49b bỏ `r.returncode` | t63 | `giet_that` "(update-index/rc) … chờ 'rc=0/128'" | 1/56 | giết thật |
| M49c bỏ `not co` | t63 | `giet_that` "(ls-files/rong) … chờ 'xau_'" | 1/56 | giết thật |
| M49d bỏ `ga.returncode` (`_add`) | t63 | `giet_that` "(add/rc) … chờ 'bình_thường'" | 1/56 | giết thật |
| M49e luôn ném | t63 | `giet_that` "(ops/no_cu.py/rc) … 'xau_' …"; t49 `bo_qua` | 1/55 | giết thật (t49 không ĐỎ oan) |
| M49f xoá `raise bo_qua_va` | t63 | `giet_that` "(update-index/bo_ten) … chờ 'va_': None" | 1/56 | giết thật |
| M49g ném ngay trong `except` | t63 | `giet_that` "(bo_ten) t49 BỎ QUA trước khi đo (3)" | 1/56 | giết thật |
| M49h (3) quay lại `git add -A` không `rc` | t63 | `giet_that` "(ops/no_cu.py/rc) … chờ 'no_cu': None" | 1/56 | giết thật |
| **M49i (MỚI) quét cả khi stage hỏng** (`if bo_qua_va is None:`→`if True:`) | t63, t49 | t63 **`bo_qua`** "t49 ĐỎ vì chốt khác khi tráo update-index/bo_ten: (2d) … MỘT khoá"; t49 `qua` | **0/57** | **SỐNG SÓT** — ĐỎ OAN |
| **M49l (MỚI) nuốt lỗi stage** (`bo_qua_va = e` → `pass`) | t63, t49 | t63 **`bo_qua`** (cùng thông điệp); t49 `qua` | **0/57** | **SỐNG SÓT** — ĐỎ OAN |
| **M49m (MỚI) `_stage_byte` hỏng ⇒ `bang(False, …)`** thay vì BỎ QUA | t63, t49 | t63 **`bo_qua`** "t49 ĐỎ vì chốt khác khi tráo hash-object/rc: … rc=128/0"; t49 `qua` | **0/57** | **SỐNG SÓT** — ĐỎ OAN |
| **M49n (MỚI) `_add` hỏng ⇒ `bang(False, …)`** | t63, t49 | t63 **`bo_qua`** "… khi tráo add/rc: … git add ops/bình_thường.py rc=128"; t49 `qua` | **0/57** | **SỐNG SÓT** — ĐỎ OAN |

Chéo phiên bản / locale: M49i, M49m, M49n trên head ⇒ cùng `bo_qua` (SỐNG) với python3.11, python3.13 và `--lc-c` (3.12).

**Trên head + `out/HINT.patch`** (`tam/log/dot-bien-hint-312.txt`; byte cuối kiểm lại trên `tam/ap3`)

| đột biến | ca đích | kết quả (3.12) | phân loại |
|---|---|---|---|
| M49m `_stage_byte` hỏng ⇒ `bang(False)` | t63 | `giet_that` "(hash-object/rc) stage hỏng mà t49 ĐỎ thay vì BỎ QUA — ĐỎ OAN" | giết thật (sống trên head) |
| M49n `_add` hỏng ⇒ `bang(False)` | t63 | `giet_that` "(add/rc) … ĐỎ OAN" | giết thật (sống trên head) |
| H49l (cấu trúc S5) `try/except BoQuaMoiTruong: pass` quanh stage cuối rồi quét | t63 | `giet_that` "(update-index/bo_ten) … ĐỎ OAN: (2d) … MỘT khoá" | giết thật (≙ M49i/M49l) |
| H49f (S5) `try/except BoQuaMoiTruong: return` quanh stage cuối | t63 | `giet_that` "(update-index/bo_ten) … chờ 'va_': None" | giết thật (≙ M49f) |
| H49g (S5) stage tên mang `\` TRƯỚC (3) | t63 | `giet_that` "(bo_ten) t49 BỎ QUA trước khi đo (3) — phần stage phải đứng CUỐI ca" | giết thật (≙ M49g) |
| M49a/b/c/d/e/h | t63 | `giet_that` đúng bước như trên head | giết thật |
| R1–R10, M60a, M61a–g | t60/t61/t62 | `giet_that` đúng nhãn như trên head | giết thật |

28 đột biến trên bản HINT (+R10 kiểm riêng) ⇒ 0 sống, 0 `tin_dung_gia`. Chéo phiên bản: M49m, M49n, H49l, H49f, H49g chết đúng nhãn trên
python3.11, python3.13 và `--lc-c`. Chỉ áp phần `t63` (hunk 5–7) lên head (`tam/hintB`): M49i, M49l, M49m, M49n chết; M49f, M49g vẫn chết.
Bán kính `DOT_BIEN` đích `t49` (`ban_kinh_db.py`, gọi `_do_ban_kinh` của CHÍNH tệp): head và HINT như nhau —
`bn_ngay_go_chi_la_chu`, `bn_hien_thi_khong_don_anh`, `bn_loi_ra_duong_tho`, `bn_json_khong_ascii` ⇒ `{t2: bo_qua, t49: giet_that, t63: bo_qua}`.

## BẢNG ĐO
| khẳng định | executor khai | đo được | khớp? |
|---|---|---|---|
| dòng thêm so merge-base (ADR-0044 ≤ 300) | +265 (commit, BAO_CAO §9) | `git diff --numstat 89fc4fa b137bd8 -- ops/` ⇒ `1 1 bash_nen.py` + `264 27 cong_cu_test.py` = **+265/−28**, 2 tệp; `git diff --stat 89fc4fa b137bd8` (cả cây) cũng chỉ 2 tệp | khớp |
| trước lượt này / lượt này | 164 ⇒ +101 | `89fc4fa..bd6ad5d` +164/−23; `bd6ad5d..b137bd8` +150/−54 (`bash_nen.py` không đổi) | khớp (265−164 = 101) |
| sha256 `cong_cu_test.py` bản vá | `5746c084…` | `5746c0845d7d984e…` (clone từ kho.git @ b137bd8, `cmp` = `cay-kho`) | khớp |
| ruff `--select F` delta 0 (0.15.15) | tập bằng nền | ruff 0.15.15 `--no-cache`: 89fc4fa = bd6ad5d = b137bd8 = b137bd8+HINT = {`bash_nen.py` F401 `ast`; `cong_cu_test.py` F841 `ci`} (so tập, bỏ số dòng) | khớp |
| docstring `_tach_dinh_dang` không đổi byte (spec §2A) | `3bc957a6…` 897 ký tự | 1741e0a = 89fc4fa = b137bd8 = `3bc957a67247801b…` 897 | khớp |
| compile sạch (không `SyntaxWarning` mới) | 3.11/3.12/3.13 | `-W error` compile `cong_cu_test.py` + `bash_nen.py`: sạch cả 3 bản (head và HINT) | khớp |
| AST điểm phóng (BAO_CAO §4) | S=54 · W=26+23 · env= 36 {Name 17, moi_truong 12, dict(os.environ) 3, {**os.environ} 3, dict(env,…) 1} | `tam/cu/dem_phong.py`: S=54 · chay 26 · _g 23 (+ goi_git 4) · env= 36 {Name 17, moi_truong 12, dict(os.environ) 3, dict(biến) 1, {**os.environ} 3}; os.system/exec*/spawn*: 0 | khớp |
| chú thích `:14-18` "36 Call … 12 / 3 / 3 / 18" | có | như trên (17 Name + 1 dict(biến) = 18); 18 truy tay về os.environ/None | khớp |
| `hasattr(io.StringIO(), "reconfigure")` | False 3.11/3.12/3.13 | False ×3 | khớp |
| `-X utf8 -X utf8=0` ⇒ 1; `-X utf8=0 -X utf8` ⇒ 0 | có | 1 / 0 trên 3.11/3.12/3.13 | khớp |
| mã con `t61` thuần ASCII, nguồn không có `\` | có | `_NAP_UTF8` không chứa `\`; sau `encode("ascii","backslashreplace")` `isascii()` = True; nguồn NFC = True | khớp |
| mọi dòng thêm ≤ 118 ký tự | có | 0 dòng thêm > 118 ký tự (so merge-base) | khớp |
| đột biến đích (BAO_CAO §6) | 24/24 giết đúng nhãn, không `tin_dung_gia` | 24 đột biến tương ứng (R1–R8 ≙ M62a/f/g/h/b, Mg1, Mg2, M62e; M61a–g; M60a; M49a–h) `giet_that` đúng nhãn, 0 `tin_dung_gia` (+ R9 của lượt này cũng chết) | khớp |
| bán kính mỗi đột biến | 1/56 (M49e 1/55) | `--tat-ca` 57 ca: mỗi cái đúng 1 ca đỏ trên 56 chạy được; M49e 1/55 (`t49` `bo_qua`) | khớp |
| "Lớp 3 ĐÃ ĐÓNG 8/8" | có | 8 đường đã liệt kê chết, nhưng M49i/M49l/M49m/M49n sống 57/57 (chiều ĐỎ OAN) | **KHÔNG khớp** — xem finding CA-KHOA-STAGING |
| mồ côi (chú thích + BAO_CAO §1) | "3 tiến trình còn sống"; SIGTERM ⇒ 241 | 2 tiến trình (ảnh chụp theo thời điểm); 241 | khớp về bản chất (con số là ảnh chụp) |
| "0 `__pycache__` trong $WT" | có | executor không chạy bộ ca trong $WT; chạy `t62` trong checkout với `PYTHONDONTWRITEBYTECODE=1` ⇒ ghi 2 `.pyc` (HƯỚNG 9) | lời khai đúng cho $WT, nhưng che một tác dụng phụ thật (P4) |
| `t63` 0,76–0,88 s; `t49` ~0,4 s/lần | có | `t63` 0,97–2,22 s, `t49` 0,43–0,86 s (đo khi máy đang chạy 2 trọn bộ song song) | cùng bậc (tải khác) |

**Trọn bộ `python3.12 ops/cong_cu_test.py`** (`tam/cu/tron_bo.sh`: bản sao clone từ kho.git, `core.abbrev 7`, xoá `__pycache__`,
`PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=$R/tam`, `CONG_CU_TEST_TIEN_TRINH=2`; hai vế head dựng cùng MỘT lệnh với hai vế nền; (a) và (b) chạy
song song trên cùng máy 4 lõi):

| lượt | cây | vòng ca | SỐ LIỆU | "giết THÊM" / nhắc t60–t63 trong bán kính | `rc=141` | RC | thời lượng | log |
|---|---|---|---|---|---|---|---|---|
| (a) thường | head `b137bd8` | **`56/56 đạt; tổng=57, bỏ qua=1`** (`t2`, thiếu jsonschema) | `ca=57 · đột biến=212 · lỗi đột biến=1` (chỉ `KHÔNG_ĐO_ĐƯỢC t2_go_canary`, jsonschema) · cổng cây thật ĐẠT · tự kiểm song song ĐẠT | 0 / 0 · 220 dòng `ok` | 0 | 1 | 08:24:06Z→09:09:40Z (45m34s) | `tam/log/head-a.txt` |
| (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` | head `b137bd8` | **`56/56 đạt; tổng=57, bỏ qua=1`** | `ca=57 · đột biến=212 · lỗi đột biến=1` (cùng `t2_go_canary`) · ĐẠT · ĐẠT | 0 / 0 · 220 `ok` | 0 | 1 | 08:24:07Z→09:09:48Z (45m41s) | `tam/log/head-b.txt` |

`RC=1` ở cả hai là do lỗi đột biến jsonschema (môi trường), không phải ca đỏ. Hai lượt head chạy CÙNG lúc với các lượt đột biến của reviewer
(tải cao hơn), nên thời lượng không so thẳng với nền.

**Một vòng CA không đột biến** (`chay_ca.py --tat-ca`, máy rảnh, 2 lần, tiến trình `-X utf8`) — chi phí mỗi đột biến trong pha bán kính (212
đột biến × mọi ca):

| cây | tổng (lần 1 / lần 2) | kết quả | tổng thời gian `t60`–`t63` |
|---|---|---|---|
| merge-base `89fc4fa` | 21,5 s / 23,2 s | `qua 52, bo_qua 1` | 0 (chưa có) |
| nền `bd6ad5d` | 23,5 s / 21,9 s | `qua 55, bo_qua 1` | 0,92 s / 0,94 s |
| head `b137bd8` | 24,7 s / 22,6 s | `qua 56, bo_qua 1` (khớp lời khai "56 qua, 1 bỏ qua") | 3,62 s / 2,68 s |
| head + HINT | 26,3 s / 24,2 s | `qua 56, bo_qua 1` | 3,74 s / 3,07 s |

⇒ `t60`–`t63` thêm ~1,7–2,7 s mỗi đột biến so `bd6ad5d` (≈ +6–10 phút tuần tự, +1,5–2,5 phút với 4 tiến trình trên Linux); HINT thêm
~0,1–0,4 s (đối chứng của `t63`). Trên Windows (tạo tiến trình đắt hơn; `t62` phóng 7 tiến trình Python — đo `strace -f -e trace=execve`: mỗi cái biên dịch
`cong_cu_test.py` 6 973 dòng, hai bản phóng lại (vế (1), (4)) nạp thêm `lease_publish_test.py` 10 502 + `bash_nen.py` 3 129 dòng — vế (1) dưới `-B` nên biên dịch lại mỗi lần) và trần `gate` `timeout-minutes: 60` (`ci.yml:68`): **KHÔNG ĐO ĐƯỢC** — phải xem trong nghiệm thu Windows.

**Trọn bộ NỀN `bd6ad5d`** (cùng script, cùng máy; hai vế nền dựng cùng MỘT lệnh với hai vế head; (a)(b) nền chạy song song với trọn bộ
HINT (a) ⇒ 6 tiến trình bán kính trên 4 lõi):

| lượt | cây | vòng ca | SỐ LIỆU | "giết THÊM" | `rc=141` | RC | thời lượng | log |
|---|---|---|---|---|---|---|---|---|
| (a) thường | nền `bd6ad5d` | `55/55 đạt; tổng=56, bỏ qua=1` | `ca=56 · đột biến=212 · lỗi đột biến=1` (jsonschema) | 0 · 220 `ok` | 0 | 1 | 09:16:15Z→10:04:46Z (48m31s) | `tam/log/nen-a.txt` |
| (b) ASCII | nền `bd6ad5d` | **`54/55 đạt`** — `ĐỎ t61 … (a) … rc=1 "Unable to decode the command from the command line"` | `lỗi đột biến=2` (jsonschema + `KHÔNG_ĐO_ĐƯỢC bán kính cho ['t61_…']` — đỏ ở nền) | 0 · 220 `ok` | 0 | 1 | 09:16:17Z→10:04:13Z (47m56s) | `tam/log/nen-b.txt` |

| khẳng định | executor khai | đo được | khớp? |
|---|---|---|---|
| trọn bộ (a) bản vá | `56/56`, lỗi đột biến 1 (jsonschema) | `56/56 đạt; tổng=57, bỏ qua=1` · `lỗi đột biến=1` (jsonschema) · 220 `ok`, 0 "giết THÊM" | khớp |
| trọn bộ (b) bản vá | `56/56`, lỗi đột biến 1 | `56/56 đạt` · `lỗi đột biến=1` · 220 `ok` | khớp |
| nền (a) / (b) | `55/55` lỗi 1 / `54/55` lỗi 3 (jsonschema + `t61` + chập chờn `t5` rc=141) | `55/55` lỗi 1 / `54/55` lỗi **2** (jsonschema + `t61`); 0 lần `rc=141` | khớp phần xác định; lỗi thứ 3 của executor là chập chờn (họ khai rõ) |
| "lỗi đột biến = nền" / delta | (a) 1→1 = 0 · (b) 3→1 = −2 | (a) 1→1 = **0** · (b) 2→1 = **−1** | (a) khớp; (b) "−2" gồm một lần chập chờn `t5` ở nền — đo sạch là −1 (vẫn ≤ 0, không đổi kết luận) |
| "220 dòng ok, không dòng nào nhắc t63; 4 DOT_BIEN đích t49 vẫn 1/57" | có | head (a)(b): 220 `ok`, 0 dòng bán kính nhắc `t60`–`t63`; 4 mục đích `t49`: `{t49 giet_that, t63 bo_qua}` (`ban_kinh_db.py`) | khớp |
| chập chờn `t5` rc=141 | 2/5 lượt của executor | 0/4 lượt trọn bộ + 0 trong bán kính của lượt này | không tái hiện ở đây; không trong diff (HƯỚNG 8) |

**Trọn bộ trên bản áp HINT** (`tam/ap`, cùng script; `ast.dump` bằng byte cuối của HINT.patch — chỉ khác chữ một chú thích):

| lượt | cây | vòng ca | SỐ LIỆU | "giết THÊM" | `rc=141` | RC | thời lượng | log |
|---|---|---|---|---|---|---|---|---|
| (a) thường | `b137bd8` + HINT | **`56/56 đạt; tổng=57, bỏ qua=1`** | `ca=57 · đột biến=212 · lỗi đột biến=1` (jsonschema) — **= head = nền** | 0 · 220 `ok` | 0 | 1 | 09:18:53Z→10:12:08Z (53m15s, 6 tiến trình bán kính trên 4 lõi) | `tam/log/hint-a.txt` |

`.pyc` còn lại trong cây SAU trọn bộ (dù `tron_bo.sh` xoá `__pycache__` trước và đặt `PYTHONDONTWRITEBYTECODE=1`): head (a) 2 tệp, head (b)
2 tệp (`ops/__pycache__/{lease_publish_test,bash_nen}.cpython-312.pyc`); nền (a)(b) 0; bản HINT 0 — xác nhận T62-GHI-PYC-VAO-CAY ở mức trọn bộ.

### T49-CO-CHE-HOAN-BO-QUA  [P2]  Cơ chế hoãn `bo_qua_va` của `bd6ad5d` còn nguyên — quyết định S5 của chủ kho (BỎ) chưa được thi hành
TỆP/DÒNG: `ops/cong_cu_test.py:5652-5655` (chú thích "#671 (review) … chỉ HOÃN phần cần INDEX"), `:5663-5676` (`bo_qua_va = None`,
`try/except … bo_qua_va = e  # ném SAU (3)`, `if bo_qua_va is None:` quanh `quet(d_va)`), `:5693-5694` (`raise bo_qua_va` sau (3)).
VẤN ĐỀ: S5 (chủ kho, 30-09): hình dạng "chốt chỉ có nhánh Windows, không có ca âm" đã lặp lần 3 ⇒ BỎ cơ chế hoãn; (3) lên trước (2d),
stage để cuối, `BoQuaMoiTruong` ném tự nhiên. `b137bd8` làm trước quyết định; thân commit tự khai "Co che hoan bo_qua_va cua bd6ad5d CHUA
bo (S5, vong sau)"; đo: 5 dòng còn (HƯỚNG 12). `t63` nay khoá được 2/3 đường của cơ chế (M49f nuốt `raise`, M49g ném sớm — chết), nhưng
đường (iii) "quét cả khi stage hỏng" (M49i) vẫn sống 57/57. Biến giữ ngoại lệ vắt qua một khối đo khác chính là thứ đẻ ra ba đường ấy;
cấu trúc tuần tự (stage đứng cuối) xoá hai đường theo KIẾN TRÚC, đường còn lại là việc của `t63` (finding kế).
VÁ Ở ĐÂU: `t49`, đoạn (2d)+(3).
VÁ THẾ NÀO: (mã TEST đầy đủ — hunk 2–4: +28/−36, ròng −8 dòng) chuyển nguyên khối (3) lên ngay trước "# (2d) N54 (r17)"; bỏ `bo_qua_va`, `try/except`,
`if bo_qua_va is None:` và `raise bo_qua_va`; vòng `_stage_byte` cho `hai` + `quet(d_va)` + `bang(len(khoa) == 2)` đứng CUỐI ca; chú thích
4 dòng viết lại thành 3 dòng nói đúng cấu trúc mới (không còn chữ "HOÃN").
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t63` (bo_ten). Sau vá, đã chạy trên bản áp: H49f (bọc stage cuối bằng `try/except BoQuaMoiTruong: return`)
⇒ `giet_that` "(update-index/bo_ten) … chờ 'va_': None"; H49g (stage tên mang `\` TRƯỚC (3)) ⇒ `giet_that` "(bo_ten) t49 BỎ QUA trước
khi đo (3) — phần stage phải đứng CUỐI ca"; H49l (`except: pass` rồi quét tiếp) ⇒ `giet_that` "… ĐỎ OAN" (cần hunk 5–7).
BẢN VÁ CÓ THỂ ĐẺ RA: (1) thứ tự đỏ đổi: đột biến sản phẩm hỏng cả (3) lẫn (2d) nay chết ở (3) trước — vẫn `t49`; đo 4 `DOT_BIEN` đích
`t49` trên bản áp: `{t49: giet_that, t63: bo_qua}` (1/N, không đổi). (2) `d`, `m` bị (3) gán lại TRƯỚC (2d) — (2d) chỉ dùng `d_va`, `mv`,
`bq` (đọc mã). (3) Windows (nếu lời khai `bd6ad5d` đúng): `t49` vẫn BỎ QUA "va_" ở CUỐI ca sau khi (3) và hai chốt thuần đã đo — y hệt
cơ chế hoãn; KHÔNG ĐO ĐƯỢC ở đây. (4) Khối (3) di chuyển được `git diff --numstat` tính là dòng thêm: so merge-base 265 → **279** (≤ 300).
HINT (hunk nào): hunk 2 (`@@ -5640`), hunk 3 (`@@ -5649`), hunk 4 (`@@ -5660`).
ĐÃ THỬ NGHIỆM HINT: xem "HINT.patch — tự kiểm".
ĐỘ TIN: cao trên Linux; hành vi Windows KHÔNG ĐO ĐƯỢC.

### CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG  [P2]  `t63` đổi MỌI ĐỎ của `t49` dưới phép tráo thành BỎ QUA — chiều "stage hỏng ⇒ ĐỎ OAN" (spec §2B) không có khoá
TỆP/DÒNG: `ops/cong_cu_test.py:5698-5735` (`t63`); cụ thể `:5727-5728` `except TinHieuChotCa as ex: raise BoQuaMoiTruong(f"KHÔNG ĐO ĐƯỢC:
t49 ĐỎ vì chốt khác khi tráo …")` và docstring `:5703` "`t49` đỏ/bỏ qua vì lý do KHÁC dưới phép tráo ⇒ KHÔNG ĐO ĐƯỢC".
VẤN ĐỀ: spec §2B: "Không stage được ⇒ `BoQuaMoiTruong` (KHÔNG ĐO ĐƯỢC), **không ĐỎ oan**" — và lỗi gốc của packet trên Windows chính là ĐỎ
oan (`(2) chiều ngược: … []`). `t63` khoá chiều "stage hỏng mà vẫn đo tiếp/xanh" (M49a/b/c/d/e/h chết), nhưng đổi mọi `TinHieuChotCa` của
`t49` dưới phép tráo thành BỎ QUA — kể cả khi CHÍNH phép tráo gây ra ĐỎ. Đo (HƯỚNG 6): M49m (`_stage_byte` hỏng ⇒ `bang(False, …)` thay vì
BỎ QUA), M49n (`_add` hỏng ⇒ `bang(False, …)`), M49i (quét cả khi stage hỏng), M49l (nuốt lỗi stage rồi quét tiếp): cả bốn `t49` `qua`
(Linux luôn stage được), `t63` `bo_qua` với lý do "t49 ĐỎ vì chốt khác" — nguyên nhân bị ghi SAI; trên cả 57 ca: 0 ca đỏ (cả bốn). Tức một bản
vá tái sinh ĐÚNG lỗi Windows gốc vẫn xanh trên Linux. Executor khai lớp 3 "ĐÃ ĐÓNG 8/8" — danh sách 8 đường thiếu chiều này (M49i là đột biến
(iii) của advisory `bd6ad5d` P2-E, HINT vòng vá không dùng): đúng hình dạng "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba".
VÁ Ở ĐÂU: `t63` — ca khoá duy nhất của staging.
VÁ THẾ NÀO: (mã TEST đầy đủ — hunk 5–7: +14/−4, ròng +10 dòng) chạy `t49` KHÔNG tráo làm ĐỐI CHỨNG trước vòng tráo: XANH ⇒ `doi_chung_xanh = True`;
BỎ QUA (nền không stage được) ⇒ `False`; ĐỎ ⇒ `t63` BỎ QUA ngay (đỏ của `t49` là việc của `t49`, giữ bán kính 1/N). Dưới phép tráo, gặp
`TinHieuChotCa` ⇒ `bang(not doi_chung_xanh, "(bước/cách) stage hỏng mà t49 ĐỎ thay vì BỎ QUA — ĐỎ OAN: …")`, chỉ khi đối chứng không xanh
mới đổi thành BỎ QUA. Docstring và thông điệp (bo_ten) viết lại cho đúng.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t63`. Đã chạy trên bản áp: M49m ⇒ `giet_that` "(hash-object/rc) stage hỏng mà t49 ĐỎ thay vì BỎ QUA — ĐỎ
OAN"; M49n ⇒ "(add/rc) … ĐỎ OAN"; H49l ⇒ "(update-index/bo_ten) … ĐỎ OAN: (2d) HAI đường … chỉ còn MỘT khoá"; vẫn chết như cũ: M49a/b/c/d/e/h.
KHÔNG được chết thêm: 4 `DOT_BIEN` đích `t49` ⇒ `t63` `bo_qua` (đo trên bản áp).
BẢN VÁ CÓ THỂ ĐẺ RA: (1) `t63` chạy `t49` thêm một lần (~0,45 s) ⇒ pha bán kính +~95 s tuần tự (212 đột biến chạy mọi ca). (2) Nếu `t49`
chập chờn (hạn chót dưới tải) thì đối chứng BỎ QUA ⇒ lượt ấy mất chiều ĐỎ oan (an toàn: không giết oan). (3) Windows: nếu `t49` tự BỎ QUA
("va_", theo lời khai `bd6ad5d`) thì chiều ĐỎ oan KHÔNG ĐO ĐƯỢC ở nền ấy — docstring mới nói thẳng; năm phép tráo còn lại vẫn đo.
HINT (hunk nào): hunk 5 (`@@ -5699`), hunk 6 (`@@ -5715`), hunk 7 (`@@ -5725`).
ĐÃ THỬ NGHIỆM HINT: xem "HINT.patch — tự kiểm". Thêm: hunk 5–7 ĐỘC LẬP với hunk 2–4 — áp RIÊNG phần `t63` lên head (`tam/hintB`, cơ chế
hoãn còn nguyên): M49i, M49l ⇒ `giet_that` "(update-index/bo_ten) … ĐỎ OAN"; M49m ⇒ "(hash-object/rc) … ĐỎ OAN"; M49n ⇒ "(add/rc) … ĐỎ OAN";
M49f, M49g vẫn chết như trên head. Tức lớp này đóng được mà không phụ thuộc quyết định S5.
ĐỘ TIN: cao.

### NGHIEM-THU-WINDOWS-CON-THIEU  [P2]  Chưa có nghiệm thu §6 trên Windows neo exact head (và bước đo giả thuyết B)
TỆP/DÒNG: spec §2B ("BƯỚC ĐẦU trên Windows: ĐO giả thuyết B TRƯỚC khi vá"), §6.1–6.3; hiện vật: thân `e46f569`, `bd6ad5d`; BAO_CAO §6'.
VẤN ĐỀ: không có, cho `b137bd8`: `N/N` Windows với hai số bằng nhau; danh sách + lý do từng ca bỏ qua; delta lỗi đột biến so NỀN cùng máy;
lượt ép ASCII cho con; đột biến §6.3 (i)(ii) chạy trên Windows; log `git add -A`/`ls-files -z`/`update-index` của giả thuyết B. Lời khai
Windows duy nhất là thân `e46f569` (47/51 trên `75af95c`) và `bd6ad5d` ("52 qua / 4 bỏ qua", môi trường CI — không phải lượt chạy tay
không `PYTHONUTF8` mà §6.1 đòi) — SHA khác, không log. Linux không thay được: `t62` đo nhánh `subprocess.run` (mặc định Windows) chỉ
trên Linux; `t63` (bo_ten) là MÔ PHỎNG lời khai "Git for Windows bỏ tên mang `\`".
VÁ Ở ĐÂU: nghiệm thu (hiện vật), không phải mã.
VÁ THẾ NÀO: trên máy Windows local, neo head SAU khi vá hai P2 trên: nền `1741e0a` (hoặc merge-base đang dùng) rồi head
`python ops\cong_cu_test.py` (KHÔNG đặt `PYTHONUTF8`) ⇒ in nguyên khối BỎ QUA/ĐỎ/SỐ LIỆU; cùng bộ với `PYTHONIOENCODING=ascii
PYTHONUTF8=0` cho con; §6.3 (i)(ii) trên bản sao tạm; log staging thật của `t49`. Điểm riêng cần nhìn: nếu `t63` ĐỎ ở `(ops/no_cu.py/rc)`
với chữ "xau_" thì Git for Windows từ chối cả `\xff` (spec §8 "chưa đo được") — khi ấy `t63` cần chốt "phép tráo không kịp tác dụng vì nền đã
bỏ qua trước ⇒ KHÔNG ĐO ĐƯỢC" (suy từ mã, KHÔNG ĐO ĐƯỢC ở Linux).
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: không áp dụng (nghiệm thu); đột biến §6.3 (i) M60a và (ii) M61b phải chạy TRÊN Windows (Linux: cả hai 1/56, đo).
BẢN VÁ CÓ THỂ ĐẺ RA: không.
HINT (hunk nào): không có hunk (không vá được bằng mã ở Linux — chủ kho: "Chỉ chạy tại máy").
ĐÃ THỬ NGHIỆM HINT: không áp dụng.
ĐỘ TIN: cao (đối chiếu hiện vật); mọi phần Windows KHÔNG ĐO ĐƯỢC.

### TU-PHONG-LAI-KHONG-TRONG-SUOT  [P3]  (biểu hiện (b), còn lại) Harness giết tiến trình bao ⇒ bản phóng lại `-X utf8` mồ côi — đã KHAI, chờ quyết định chủ kho
TỆP/DÒNG: `ops/cong_cu_test.py:52-53` (`sys.exit(subprocess.run([sys.executable, "-X", "utf8", …]).returncode)`), chú thích `:40-44` (NỢ).
VẤN ĐỀ: đo trên `b137bd8` (HƯỚNG 10): `subprocess` có hạn chót `kill()` tiến trình bao ⇒ 2 tiến trình (`-X utf8 … cong_cu_test.py` và con
của nó) còn chạy sau 2 s; đối chứng `PYTHONUTF8=1`: 0. Nhánh này là MẶC ĐỊNH trên Windows VÀ trên Linux locale `*.UTF-8` không `PYTHONUTF8`
(HƯỚNG 11). Fail-close giữ (rc ≠ 0; SIGTERM ⇒ 241). Chú thích mới khai đúng phạm vi (POSIX lẫn Windows) và hướng — P3-D của advisory
(lời khai "chỉ Windows") đã đóng; hành vi thì chưa. Hạng giữ theo lượt 3 cho biểu hiện này (P3); protocol §8 `sensitive` đòi quyết định
có căn cứ cho finding còn mở.
VÁ Ở ĐÂU: khối phóng lại (`:45-53`) — hoặc không vá, nếu chủ kho nhận nợ.
VÁ THẾ NÀO: (gợi ý HƯỚNG, không phải mã đủ điều kiện) chủ kho chọn: (A) nhận nợ có tên (vd `PHONG-LAI-MO-COI`) + packet kế nhiệm như
executor đề xuất; hoặc (B) POSIX `os.execve` (cùng PID ⇒ hết mồ côi, tín hiệu trong suốt) + một khoá môi trường CHỈ cho test ép nhánh
`subprocess.run` để `t62` vẫn đo nhánh Windows trên Linux (hướng HINT advisory `bd6ad5d`), Windows: Job Object `KILL_ON_JOB_CLOSE` (ctypes).
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: nếu (B): `t62` thêm vế PID (bản phóng lại trùng PID dưới `execve`) và chạy lại (1)–(6) dưới khoá ép
`subprocess`; đột biến "bỏ `execve`" ⇒ vế PID chết; "bỏ khoá ép" ⇒ (1)/(2) dưới khoá chết. Nếu (A): không.
BẢN VÁ CÓ THỂ ĐẺ RA: (B) Linux mặc định thôi chạy nhánh Windows (phải có khoá ép mới đo được); `execve` bỏ qua buffer/`atexit` của tiến
trình bao (phải flush trước); Windows vẫn mồ côi tới khi có Job Object — không chạy được ở đây.
HINT (hunk nào): KHÔNG có hunk — lựa chọn kiến trúc chờ chủ kho; vá POSIX một mình để nguyên nhánh Windows (nền đích của packet) mồ côi, đúng thứ
executor đã cân nhắc và khai trong mã.
ĐÃ THỬ NGHIỆM HINT: không áp dụng.
ĐỘ TIN: cao cho Linux (đo trực tiếp, có đối chứng); số Windows "15,7 s" là lời khai phiên Windows — KHÔNG ĐO ĐƯỢC.

### T62-GHI-PYC-VAO-CAY  [P4]  `t62` (4) thiếu `-B` sau khi gỡ `PYTHONDONTWRITEBYTECODE` ⇒ ghi `.pyc` vào chính checkout đang đo
TỆP/DÒNG: `ops/cong_cu_test.py:2339-2340` (gỡ `PYTHONDONTWRITEBYTECODE` khỏi env con), `:2354` `hoi("-X", "utf8=0", str(TEP_TEST), …)`, `:2357`.
VẤN ĐỀ: HƯỚNG 9: chạy riêng `t62` trong clone mới với `PYTHONDONTWRITEBYTECODE=1` ⇒ để lại `ops/__pycache__/lease_publish_test.cpython-312.pyc`
và `bash_nen.cpython-312.pyc` (nền `bd6ad5d`: 0; `t49/t60/t61/t63`: 0); trọn bộ: head (a)(b) để lại 2 tệp, nền 0, HINT 0 (BẢNG ĐO). Hệ quả: vi phạm vệ sinh §8.2 (reviewer chạy bộ ca trong checkout
read-only thấy snapshot "ignored" đổi); `.pyc` hợp lệ cạnh nguồn làm câm `SyntaxWarning` ở các lần nạp sau — `t60` miễn nhiễm (chép
`bash_nen.py` ra thư mục tạm, đọc nguồn), nên không chốt nào đã đo bị câm ⇒ chỉ P4.
VÁ Ở ĐÂU: `t62` vế (4); vế (5) cho đồng bộ ((5) chỉ ghi khi đột biến R6 làm nó phóng tiếp).
VÁ THẾ NÀO: (mã TEST đầy đủ — hunk 1) `hoi("-B", "-X", "utf8=0", …)` và `hoi("-B", str(TEP_TEST), …)`.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: không thêm ca (vệ sinh); phép kiểm: `t62` một mình trên bản áp ⇒ 0 `.pyc` (đo). R5 ⇒ (4), R6 ⇒ (5), R9 ⇒ (4)
vẫn `giet_that` trên bản áp (đo) — `-B` không đổi nghĩa đo của hai vế.
BẢN VÁ CÓ THỂ ĐẺ RA: không đổi nghĩa (cờ `-B` độc lập với `utf8_mode`/dấu). Muốn khoá bằng máy thì thêm chốt "`HERE/__pycache__` không có
tệp mới sau `t62`" — tốn dòng, không đề xuất.
HINT (hunk nào): hunk 1 (`@@ -2351`).
ĐÃ THỬ NGHIỆM HINT: xem "HINT.patch — tự kiểm".
ĐỘ TIN: cao.

### TEN-CA-LECH-SPEC  [P4]  Ca khoá mang tên `t60`–`t63` thay vì `t52` của spec
TỆP/DÒNG: `ops/cong_cu_test.py:2248` (`t60_import_bash_nen_khong_in_gi_ra_stderr`), `:2304`, `:2329`, `:5698`; spec §2A, §6.3.
VẤN ĐỀ: người nghiệm thu theo spec tìm `t52` không thấy; lý do (#668 đã dùng `t52`–`t54`) chỉ có ở BAO_CAO §5.
VÁ Ở ĐÂU: thân PR / handoff (ngoài hai tệp) — theo quyết định chủ kho, không đổi tên trong mã.
VÁ THẾ NÀO: khai ánh xạ `t52`→`t60`; "ca khoá UTF-8" (spec §2C/§6.3 ii) → `t61` + `t62`; ca mới `t63`; người land kiểm `t60`–`t63` chưa bị #668 dùng.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: không áp dụng.
BẢN VÁ CÓ THỂ ĐẺ RA: không.
HINT (hunk nào): không có hunk (ngoài mã).
ĐÃ THỬ NGHIỆM HINT: không áp dụng.
ĐỘ TIN: cao; thân PR KHÔNG ĐO ĐƯỢC (không gọi mạng).

## HINT.patch — tự kiểm

- Tệp: `out/HINT.patch` — 7 hunk, MỘT tệp `ops/cong_cu_test.py`, định dạng `git diff --no-prefix` (đường dẫn repo-relative, không `a/`/`b/`),
  có đoạn đầu mang nhãn §8 nguyên văn và bảng phân loại hunk; sha256/kích thước ghi ở cuối mục (đo lại sau lần ghi cuối).
- Mọi hunk là **mã TEST** trong tệp test (§8 ràng buộc 3(a)); không hunk nào chạm `bash_nen.py` hay khối tự phóng lại. Mức: mã đầy đủ, đã chạy
  trên bản sao tạm — không phải mệnh lệnh; executor tự áp, tự đo, tự commit.
- Lệnh tự kiểm BẮT BUỘC (đúng nguyên văn prompt, clone mới từ kho.git; lần cuối trên BYTE CUỐI của HINT.patch):
  ```
  $ git clone -q kho.git tam/ap3 && git -C tam/ap3 checkout -q --detach b137bd8 && cd tam/ap3 && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch
  checking file ops/cong_cu_test.py
  dry_run_rc=0
  $ patch -p0 --fuzz=0 < ../../out/HINT.patch            ⇒ patching file ops/cong_cu_test.py   apply_rc=0   (không .orig/.rej)
  $ cmp ops/cong_cu_test.py tam/hint/ops/cong_cu_test.py  ⇒ trùng từng byte với bản soạn
  $ git diff --numstat 89fc4fa -- ops/                     ⇒ 1 1 ops/bash_nen.py · 278 39 ops/cong_cu_test.py  ⇒ +279 so merge-base (≤ 300)
  ```
  (lượt đầu dùng `tam/ap` đúng tên trong prompt; sau đó sửa CHỈ chữ của chú thích hunk 3 — `ast.dump` bản cuối == bản đã chạy trọn bộ —
  nên tự kiểm lại trên clone mới `tam/ap3`. Cuối lượt (10:13Z) chạy lại ĐÚNG nguyên văn với `tam/ap` (xoá rồi clone mới) trên byte cuối:
  `checking file ops/cong_cu_test.py` · **`hint_dry_run_rc=0`** · áp thật `apply_rc=0` · `cmp` = `tam/hint` · thêm so merge-base **279**.)
- Byte cuối: `out/HINT.patch` sha256 **`a5c991ba7a383e9b52d77e071bdeea79fd65cd5020c265dd1e5c482452acee0d`**, 12 180 byte, 7 hunk
  (hunk 1 +2/−2 · hunk 2 +16/−0 · hunk 3 +3/−4 · hunk 4 +9/−32 · hunk 5 +4/−2 · hunk 6 +7/−0 · hunk 7 +3/−2 ⇒ +44/−42 so head).
- Trên bản áp (`tam/ap`/`tam/ap3` ≡ `tam/hint`):
  - `t49 t60 t61 t62 t63` ⇒ `qua` trên python3.11/3.12/3.13 × (môi trường thường, `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` với tiến trình
    đo `-X utf8`) — 6/6 lượt `TONG {"qua": 5}`; `find -name '*.pyc'` sau khi chạy ⇒ 0 tệp.
  - 28 đột biến (`tam/log/dot-bien-hint-312.txt`): M49a/b/c/d/e/h, **M49m, M49n** (sống trên head), **H49f, H49l, H49g** (cấu trúc S5), R1–R9,
    M60a, M61a–g ⇒ **28/28 `giet_that` đúng nhãn**, 0 `tin_dung_gia`, 0 sống.
  - `ban_kinh_db.py` (gọi `_do_ban_kinh` của chính tệp, cả 57 ca) cho 4 `DOT_BIEN` đích `t49`: `{t2: bo_qua, t49: giet_that, t63: bo_qua}` —
    y hệt head ⇒ `t63` mới không kéo rộng bán kính.
  - `grep -c bo_qua_va` ⇒ 0; ruff 0.15.15 `--select F` ⇒ tập bằng nền; `-W error` compile sạch 3.11/3.12/3.13; mọi dòng thêm ≤ 118 ký tự.
  - Trọn bộ `python3.12 ops/cong_cu_test.py` trên bản áp (a): `56/56 đạt`, `lỗi đột biến=1` (jsonschema, = head = nền), 220 `ok`, 0 "giết THÊM",
    0 `.pyc` để lại (BẢNG ĐO). (b) trên bản áp: KHÔNG chạy trọn bộ (chỉ 5 ca đích × 3 bản Python dưới `LC_ALL=C` — đều `qua`).

## KHÔNG ĐO ĐƯỢC

- **Mọi hành vi Windows** (chủ kho: "Chỉ chạy tại máy"; không `workflow_dispatch`): Git for Windows có nhận `xau_\xff`/`hong_\xff` và tên
  mang `\` trong INDEX không (spec §8) — `t63` (bo_ten) chỉ MÔ PHỎNG lời khai trong thân `bd6ad5d`; `sys.orig_argv` qua `py`/venv launcher;
  mồ côi dưới TerminateProcess (số "15,7 s" là lời khai phiên Windows); mã thoát NTSTATUS lớn qua `sys.exit`; console cp1258; thời lượng
  bước `cong_cu_test` so trần `gate` 60 phút (HƯỚNG 14). Rủi ro suy từ mã, cần nhìn khi nghiệm thu: nếu Git for Windows từ chối cả `\xff`
  thì `t63` (ở head lẫn bản HINT) sẽ ĐỎ ở `(ops/no_cu.py/rc)` với chữ "xau_" vì `t49` bỏ qua trước khi phép tráo kịp tác dụng.
- **Thân PR #690** (không gọi mạng): ánh xạ tên ca `t52`→`t60…t63`, `hint_provenance` theo hunk (§7/§8) cho vòng này — thân `b137bd8` chỉ
  khai gộp "theo HINT luot 2/3 (e46f569)"; BAO_CAO không có bảng hunk ↔ hint. Handoff/PR của vòng này chưa tồn tại (commit cục bộ, chưa đẩy)
  nên KHÔNG tính finding; người đẩy phải khai.
- **Bản vá #675 trên master**: `master` trong kho.git = `d553efa5`, là TỔ TIÊN của merge-base ⇒ bản sao master cũ, không mang #675.
- **Thẩm quyền ghi của phiên tạo `b137bd8`**: trailer `Claude-Session: …session_014dEtdMqShJhdQ8JfNbEeLU` là phiên của lease g1 (đã bị g2 thay
  thế theo `LEASE-g2.yaml` `thay_the_cho`); `LEASE-g2.yaml` ghi `environment: local` (máy Windows), còn BAO_CAO ghi "container Linux". Có thể
  chủ kho đã giao trong phiên — hiện vật của lượt này không chứng minh được theo chiều nào; chủ kho/người land xác nhận.
- **Model/effort thật của executor**: thân commit tự khai "Opus 5.5, effort xhigh", BAO_CAO khai effort KHÔNG ĐO ĐƯỢC.
- **Trọn bộ có `jsonschema`** (CI cài `jsonschema==4.26.0`): không cài, để giữ cùng điều kiện executor khai — `t2`/`t2_go_canary` là
  KHÔNG_ĐO_ĐƯỢC ở mọi cây trong lượt này.
- **Giới hạn §8.2**: snapshot đầu/cuối của `cay-kho` (HEAD, tree, status kể cả ignored, diff, diff --cached) chỉ chứng minh không có delta
  ở hai mốc (kết quả ở cuối tệp).
- **Sự cố trong lượt (khai trước)**: (1) 08:22Z một lệnh `git -C cay-kho write-tree` (định dùng để in tree cho snapshot) — object tree
  `33b0e063` đã có sẵn trong pack; `find cay-kho/.git/objects -newer bat_dau.txt` ⇒ 0 tệp, mtime pack không đổi ⇒ không ghi gì.
  (2) 09:00Z `pip install --target $R/tam/ruff ruff==0.15.15` (đúng lệnh prompt, thiếu `--no-cache-dir`) ghi lại MỘT tệp siêu dữ liệu
  cache HTTP 1 777 B `/root/.cache/pip/http-v2/5/b/e/6/4/5be64ddd…` (mục cache có sẵn từ 2026-09-29, `.body` 793 185 B không đổi) — ngoài
  `$R`; không khôi phục được bản cũ; không liên quan kho. (3) `git -C cay-kho status` (không `--no-optional-locks`) lúc 08:21:48Z đã
  GHI LẠI `cay-kho/.git/index` (làm mới stat-cache sau checkout 08:20:28Z — "racy" timestamps); NỘI DUNG mục không đổi: sha256 của
  `git ls-files -s` = sha256 của `ls-tree -r HEAD` (`e653b3a8…`), `diff --cached` rỗng; các lần `status` sau chỉ tạo/xoá `index.lock`
  (mtime thư mục `.git` đổi). Snapshot cuối dùng `--no-optional-locks`. Không ghi gì khác ngoài `$R` (`~/.gitconfig` sha256 đầu/cuối:
  xem cuối tệp).

## SNAPSHOT ĐẦU/CUỐI (§8.2)

| đối tượng | đầu (08:22Z) | cuối (10:13Z) | ghi chú |
|---|---|---|---|
| `cay-kho` HEAD / tree | `b137bd809b1eaf5a06372703bb0a580ea967689d` / `33b0e063e28956190d98654d8f258255ed105907` | như đầu | — |
| `cay-kho` `status --porcelain --ignored`, `diff`, `diff --cached` | rỗng | rỗng (`--no-optional-locks`) | tệp ngoài `.git` mới hơn mốc bắt đầu: 0 |
| `cay-kho/.git` | — | `.git/index` mtime 08:21:48Z (sự cố (3) ở KHÔNG ĐO ĐƯỢC; nội dung mục = cây HEAD), mtime thư mục `.git` đổi do `index.lock` | không object nào mới |
| `kho.git` | — | 0 tệp mới hơn mốc bắt đầu; refs sha256 `6429414a…` | — |
| `~/.gitconfig` | sha256 `75239ed3…`, mtime 06:14:40Z | sha256 `75239ed3…`, mtime 06:14:40Z | không đổi |

Giới hạn: snapshot chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên.

