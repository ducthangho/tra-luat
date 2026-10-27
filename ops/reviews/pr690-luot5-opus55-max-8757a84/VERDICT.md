verdict: changes_requested
reviewed_sha: 8757a8406489a306736c8257a7933546b8c81042
provider: claude
role: reviewer
review_kind: advisory_review
model_reviewer_identity: claude-opus-5-5 (Opus 5.5; tự khai — phiên điều phối đối chiếu modelUsage)
independent_from_executor_session: true
assurance: review_deferred
review_axes: [spec, standards_security]

> Ngưỡng đã áp: `review_class`/`effective_review_class: sensitive`, `assurance_target: human_audited` (LEASE-g2). Lượt này CÙNG PROVIDER
> với executor ⇒ nhãn tối đa `same_provider_approved`, và nhãn ấy KHÔNG thay mức assurance bắt buộc cho `sensitive` (§8).
> `changes_requested` ⇒ `assurance: review_deferred`. Đếm theo LỚP còn mở: **P0=0 · P1=1 · P2=1 · P3=1 · P4=2** (BẢNG LỚP).
> P1 là lỗi của MERGE (vá 5 tự nó đóng đúng 3 lớp của lượt 4): cửa `--tu-kiem-che-do-utf8` đứng ngoài bảng `_CUA` ⇒ đột biến #668
> `f25_cua_moi_vi_tri` làm `t62` chết tín dụng giả ⇒ mảnh CI `gate-cong-cu` 5/8 ĐỎ (đo thật, env CI) ⇒ gom đỏ; HINT hunk 2–3 (mã test,
> đã chạy: mảnh 5/8 xanh). P2 là nghiệm thu Windows (không vá được bằng mã ở Linux) + một rủi ro có điều kiện của `t63` (mô phỏng).
> Trạng thái ghi: tăng dần; hai trọn bộ head (a)/(b) chạy ngầm — kết quả điền vào BẢNG ĐO khi xong.
> Bắt đầu 2026-09-30T15:54:26Z (`bat_dau.txt`). SPEC sha256 đo lại `18504ced…0b88` — KHỚP. PROMPT sha256 `aa9f0272…e0af` = `prompt.sha256`.
> Rig: `tam/tb/{head-a,head-b}` @`8757a84` + `tam/tb/{nen-a,nen-b}` @`fc852ff` dựng trong CÙNG một lệnh (clone từ `kho.git`,
> `core.abbrev 7`); `cmp` head-a/ops/cong_cu_test.py = cay-kho (sha256 `fd959d71…`). Script `tam/cu/tron_bo.sh`. 16:1xZ: khởi chạy
> ngầm trọn bộ head (a), head (b), nền (a) — mỗi cái `CONG_CU_TEST_TIEN_TRINH=2`.
> Máy: 4 lõi, 15 GB; python 3.11.15/3.12.3/3.13.12; git 2.43.0; KHÔNG `jsonschema`, KHÔNG `shellcheck`; container KHÔNG đặt
> `LANG`/`LC_ALL` ⇒ Python tự bật `utf8_mode=1` (PEP 540) ở môi trường (a) — nhánh phóng lại chỉ chạy ở (b).
> 16:27Z: reviewer DỪNG lượt nền (a) (`tam/log/nen-a.txt`, dòng `# DUNG_CHU_DONG`) để giải phóng CPU (pha bán kính 416 đột biến ~1
> phút/đột biến/worker dưới tải); so nền làm theo TỪNG dòng đỏ bằng A/B dựng cùng lệnh (f25) và mảnh CI 5/8 nền/head/HINT.
> 18:02Z: harness DỪNG hai tác vụ nền trọn bộ head (a)/(b) ở trần 2 giờ của tác vụ nền, giữa pha bán kính (~118/208 mỗi worker;
> dòng bán kính chỉ in ở cuối ⇒ mất phần ấy). Phần đã in ở CẢ HAI: vòng CA `59/59 đạt; tổng=60, bỏ qua=1`, CỔNG TRÊN CÂY THẬT ĐẠT,
> TỰ KIỂM SONG SONG ĐẠT. Thay bằng cách chia bán kính đúng như CI: 8 mảnh (mỗi mảnh là một tác vụ < 2 giờ) ở env (b) qua phóng lại
> + gom — xem BẢNG ĐO.
> MÁY DÙNG CHUNG: `ps` lúc 17:20Z thấy một phiên KHÁC (`claude --agent va-spec-opus`, `scratchpad/va-luot6/tam/tron_{a,b}`) chạy 2
> trọn bộ song song từ ~17:01Z — ngoài `$R`, lượt này không đụng tới; mọi thời lượng của lượt này đo dưới tải chung (8–11 trên 4 lõi),
> chỉ dùng để so tương đối trong cùng lần đo.

## ĐỐI CHIẾU LƯỢT TRƯỚC

> Commit mới từ lượt 4 (`b137bd8`): `c5f3da0` (vá 5: `git diff --numstat b137bd8 c5f3da0 -- ops/` ⇒ `63 50 ops/cong_cu_test.py`,
> `bash_nen.py` không đổi) và merge `8757a84` (parents `c5f3da0` + `fc852ff`; một khối giải xung đột ở `__main__`). sha256 AST:
> `_ep_utf8`, khối phóng lại, `_NAP_UTF8`, `t60`, `t61` giống từng byte `b137bd8`; `t49`/`t62`/`t63` đổi ở `c5f3da0`, merge không đổi
> chúng. Nhãn §8: `ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ` (+ `TÁI PHÁT` cho lớp đã đóng có biểu hiện mới).
> Mọi bằng chứng do lượt này tự đo trên `8757a84` (bản sao tạm).

| lớp (slug ổn định) | nguồn | hạng cũ | nhãn trên `8757a84` | bằng chứng tự đo |
|---|---|---|---|---|
| T49-CO-CHE-HOAN-BO-QUA | advisory `bd6ad5d` P2-E; lượt 4 P2; S5 chủ kho | P2 | **ĐÃ VÁ THẬT** (Linux) | `grep -c bo_qua_va` = 0; (3) đứng trước (2d), stage `\` đứng CUỐI (`:6221-6264`); H49f ⇒ "(update-index/bo_ten) … chờ 'va_'", H49l (≙ M49i/M49l cũ) ⇒ "… ĐỎ OAN", H49g ⇒ "(bo_ten) … trước khi đo (3)", H49h ⇒ "(bo_ten) … trước hai chốt THUẦN (2d)" — cả 4 `giet_that` đúng nhãn; N1/N2 (gỡ ghi `(2d)` / t49 bỏ `nap`) ⇒ chết ⇒ chốt thứ tự có răng. Windows: KHÔNG ĐO ĐƯỢC |
| CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG | lượt 1 `75af95c` → lượt 4 đóng một phần | P2 | **ĐÃ VÁ THẬT** (Linux) | chiều "stage hỏng ⇒ ĐỎ OAN": M49m, M49n, C2_bt_do, C2_xau_do, C2_hong_do, C2_va_do, C2_nocu_do ⇒ `giet_that` "… ĐỎ OAN" (7/7); chiều "hỏng mà xanh": M49a/b/c/d/e/h, C2_bt_nuot/C2_xau_nuot/C2_nocu_nuot ⇒ chết đúng bước (C2_hong_nuot ⇒ `bo_qua` — kỳ vọng: KHÔNG ĐO ĐƯỢC, không ĐỎ oan); T63a+M49m ⇒ `bo_qua` (chính `bang(not doi_chung_xanh…)` là thứ giết); 4 `DOT_BIEN` đích t49 ⇒ `ok … 1/60`, t63 `bo_qua` (không giết thêm); T63b (nuốt đỏ đối chứng) ⇒ "giết THÊM ['t63_…']" (nhánh đối chứng có răng); "ĐỎ vì chốt khác" 0 lần. Windows: KHÔNG ĐO ĐƯỢC |
| NGHIEM-THU-WINDOWS-CON-THIEU | lượt 1 → nay | P2 | **CHƯA VÁ — KHÔNG ĐO ĐƯỢC ở Linux** | hiện vật lượt này không có log/receipt Windows nào cho `c5f3da0`/`8757a84`; BAO_CAO §7: "Nghiệm thu Windows: KHÔNG làm ở đây" |
| TU-PHONG-LAI-KHONG-TRONG-SUOT | lượt 3 `e46f569` | P3 (b) | **CHƯA VÁ** (chờ quyết định chủ kho — không đòi vá vòng này) | `tam/cu/do_mo_coi.py`: `LC_ALL=C.UTF-8 PYTHONUTF8=0` ⇒ bao rc=-9, còn sống sau 2s: 1 (`python3.12 -X utf8 -B ops/cong_cu_test.py`); SIGTERM tới con ⇒ rc bao=241; đối chứng `PYTHONUTF8=1` ⇒ 0. Khối phóng lại giống từng byte `b137bd8` |
| T62-GHI-PYC-VAO-CAY | lượt 4 `b137bd8` | P4 | **ĐÃ VÁ THẬT** | `t62` một mình, clone mới, `PYTHONDONTWRITEBYTECODE=1`: `8757a84` ⇒ 0 `.pyc`; `b137bd8` ⇒ 2 (`ops/__pycache__/{lease_publish_test,bash_nen}.cpython-312.pyc`); P0 ⇒ "(2) … B=0", P4 ⇒ "(4) … (giữ `-B`) … B=0"; trọn bộ/CI gate: `pyc_con_lai=0` |
| TEN-CA-LECH-SPEC | lượt 2/3 | P4 | **theo quyết định chủ kho** (khai ở PR) | `t52_import` 0 lần, `def t60_import_bash_nen_khong_in_gi_ra_stderr` 1 lần; thân PR: KHÔNG ĐO ĐƯỢC (không gọi mạng) ⇒ còn P4 tới khi PR khai |
| UTF8-BO-SOT-BO-DOC | lượt 1 `75af95c` | P1 | ĐÃ VÁ THẬT (giữ) | vòng CA head dưới `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` ⇒ `59/59 đạt` (trọn bộ (b): BẢNG ĐO) |
| CA-KHOA-UTF8-THIEU-QUAN-SAT (+ lượt 2 P3-C) | lượt 1–3 | P2 | ĐÃ VÁ THẬT (giữ) | M61a–g ⇒ `giet_that` đúng nhãn (a)(b)(c)(d)(b)(f)(g) |
| TU-PHONG-LAI-CHI-KHOA-CO-UTF8 | lượt 2 P2-C | P2 | ĐÃ VÁ THẬT (giữ) | R1–R10 ⇒ `giet_that` đúng vế (UTF8_MODE/(1)…(6)/(e)) |
| LOI-KHAI-RONG-HON-PHEP-DO | lượt 1–3 | P3 | **TÁI PHÁT (biểu hiện mới do ghép #668)** | chú thích `:14-17` "ĐÃ ĐO (AST, lượt vá 4): 36 Call mang `env=` trong tệp này — … 3 `{**os.environ, …}` …"; đo AST trên `8757a84`: **38** Call, `{**os.environ,…}` = **5** (+2 của #668 ở `:7234`, `:8073`; cả hai vẫn thừa kế ⇒ tính chất đúng, con số trôi). "66" 0 lần |
| CON-TRO-CA-CU | lượt 1 | P4 | ĐÃ VÁ THẬT (giữ) | `t60b` 0 lần |

**Lời khai riêng của executor vòng 5 (BAO_CAO §9: "lớp 1/2/3 ĐÓNG")** — đo: lớp 1 (HOAN) 6 đường 1.1–1.6 ⇒ khớp (H49f/l/g/h,
M49m, grep); lớp 2 (STAGING) 11 đường 2.1–2.11 ⇒ khớp (M49m/n, C2_* ×9 kể cả `C2_hong_nuot` = `bo_qua` kỳ vọng, T63a/T63b); lớp 3
(PYC) ⇒ khớp. Lời khai đúng cho các đường đã liệt kê; phần MỚI lộ ra ở lượt này nằm ở MERGE (không thuộc vá 5) — xem
CUA-UTF8-NGOAI-BANG-CUA.

## BẢNG LỚP
| slug lớp | finding/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| CUA-UTF8-NGOAI-BANG-CUA (MỚI) | (1) `f25_cua_moi_vi_tri` (#668) ⇒ `t62` `tin_dung_gia` ⇒ dòng bán kính ĐỎ, +1 lỗi đột biến so nền, mảnh CI 5/8 đỏ ⇒ gom đỏ; (2) N6 "cửa dò mọi vị trí" SỐNG 60/60 | **P1** | lượt 5, merge `8757a84` (không có ở `c5f3da0` — trước ghép chưa có `f25`) | MỘT gốc: cửa UTF-8 là đường dispatch thứ hai ngoài `_CUA`. Vá chung: đăng ký cửa vào `_CUA` (HINT hunk 2–3) ⇒ cả (1) và (2) đóng theo cấu trúc | bản áp: `f25` ⇒ `ok 1/60`; 9 đột biến dispatcher ⇒ `ok 1/60`; 8 ca liên quan `qua`; mảnh CI 5/8 trên bản áp: BẢNG ĐO |
| NGHIEM-THU-WINDOWS-CON-THIEU | (1) không có §6.1–6.3 Windows cho head; (2) giả thuyết B chưa đo; (3) mảnh/gom #668 trên Windows với `t60`–`t63`; (4) MỚI (mô phỏng): nền không nhận `\xff` ⇒ `t63` ĐỎ oan | **P2** | lượt 1 → nay | (1)–(3) không vá được bằng mã; (4) phải ĐO trên Windows trước (spec §2B/S2), hướng vá sẵn: phép dò năng lực độc lập trong nhánh `os.name == "nt"` | (1)–(3) KHÔNG ĐO ĐƯỢC ở Linux; (4) mô phỏng `tam/gitgia/git` |
| TU-PHONG-LAI-KHONG-TRONG-SUOT | (b) mồ côi khi harness giết bao (đo: 1 tiến trình; SIGTERM ⇒ 241) | **P3** | lượt 3 `e46f569` | chờ quyết định chủ kho (không đòi vá vòng này) | `tam/cu/do_mo_coi.py`; Windows KHÔNG ĐO ĐƯỢC |
| LOI-KHAI-RONG-HON-PHEP-DO | tái phát do ghép: "36 Call … 3 `{**os.environ}`" nay 38 / 5 | **P4** | lượt 1–3; tái phát `8757a84` | sửa chữ (HINT hunk 1) | `tam/cu/dem_env.py` trên bản áp = 38/5 |
| TEN-CA-LECH-SPEC | spec `t52` → mã `t60`; sau ghép `t52` trong tệp là của #668 | **P4** | lượt 2/3 | quyết định chủ kho: khai ở PR | thân PR KHÔNG ĐO ĐƯỢC |
| T49-CO-CHE-HOAN-BO-QUA | — | đóng | advisory `bd6ad5d` → `c5f3da0` | — | H49f/l/g/h, N1/N2 chết; `bo_qua_va` 0 |
| CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG | — | đóng (Linux) | lượt 1 → `c5f3da0` | — | M49*, C2_*, T63a/b; 4 DOT_BIEN t49 1/60 |
| T62-GHI-PYC-VAO-CAY | — | đóng | lượt 4 → `c5f3da0` | — | 0 `.pyc` (t62 một mình, trọn bộ, CI gate) |
| UTF8-BO-SOT-BO-DOC · CA-KHOA-UTF8-THIEU-QUAN-SAT · TU-PHONG-LAI-CHI-KHOA-CO-UTF8 · CON-TRO-CA-CU | — | đóng (giữ) | lượt 1–3 | — | R1–R10, M61a–g, vòng CA (b) 59/59, `t60b` 0 |

Đếm: **5 lớp còn mở** (P1×1 · P2×1 · P3×1 · P4×2); **7 lớp đóng** (tính cả 4 lớp gộp ở dòng cuối). Biểu hiện còn mở: CUA 2 ·
WINDOWS 4 · KHONG-TRONG-SUOT 1 · LOI-KHAI 1 · TEN-CA 1 = **9**.

## BẢNG SĂN

> Môi trường: container Linux 4 lõi, `python3.12` 3.12.3 (đo chính), 3.11.15/3.13.12 để so, git 2.43.0, KHÔNG `jsonschema`/`shellcheck`.
> `TMPDIR` trong `$R/tam`, `PYTHONDONTWRITEBYTECODE=1`, xoá `__pycache__` trước mỗi lượt; mọi phép đo trên bản sao tạm trong `$R/tam/`.

```
HƯỚNG 1: khối giải xung đột `__main__` (merge) có đúng quy ước #668 — cửa UTF-8 có đi CÙNG đường dispatch với mọi cửa khác không
  giả thuyết : cửa `--tu-kiem-che-do-utf8` đặt NGOÀI bảng `_CUA` là một đường dispatch THỨ HAI; đột biến #668 nhắm dispatcher
               (`f25_cua_moi_vi_tri`, "dò theo _CUA") sẽ đổi hành vi cửa UTF-8 mà không ai chờ ⇒ `t62` chết vô can
  lệnh       : (A/B cùng lệnh) git clone kho.git tam/db/f25h @8757a84 ; tam/db/f25n @fc852ff ;
               python3.12 -X utf8 tam/cu/mot_db.py <cây> f25_cua_moi_vi_tri      (gọi `_do_mot` + `_ket_luan_ban_ghi` CỦA tệp)
  output     : head: ĐỎ  f25_cua_moi_vi_tri: ca ['t62_…'] chết bằng lỗi VÔ CAN (tín dụng giả) ⇒ bán kính không đọc được   (loi=1)
                     t62 tin_dung_gia "giàn giáo hỏng …: cửa --tu-kiem-che-do-utf8 không in gì: rc=1 … FileNotFoundError"
               nền : ok  f25_cua_moi_vi_tri → giết đúng 't52_…' · bán kính 1/56   (loi=0)
               tái hiện lời gọi con: f25 ⇒ `cua=None` ⇒ `sys.exit(main())` ⇒ `_chay_tien_kiem(batch_behavior_test)` ⇒
               `shutil.copy2(CAI_SH, …)` FileNotFoundError (cây đột biến chỉ có cong_cu_test.py + _KEM_TEP_TEST) ⇒ rc=1
               DOT_BIEN.index('f25_cua_moi_vi_tri') = 325 ⇒ mảnh CI 5/8
  kết luận   : LỖI — xem finding CUA-UTF8-NGOAI-BANG-CUA (argv[1]-only thì đúng quy ước, nhưng "một bảng cửa" thì không).

HƯỚNG 2: chế độ mảnh/gom ĐI QUA tự phóng lại (argv/env giữ không; có phóng lặp không)
  lệnh       : cd tam/h2 (@8757a84); env -u PYTHONDONTWRITEBYTECODE LC_ALL=C.UTF-8 PYTHONUTF8=0 python3.12 -B ops/cong_cu_test.py …
               (a) cấu hình mảnh lỗi qua env; (b) bộ 8 mảnh HỢP LỆ dựng bằng CHÍNH `_ket_thuc_manh`+`_ban_ghi_du_gia`+`_van_tay()`
               rồi `--gop ../gom8` dưới `strace -f -e trace=execve`; (c) bỏ mảnh 5 rồi gom lại
  output     : (a) CONG_CU_TEST_MANH=5/8 ⇒ "[C-thieu-ra]" rc=2 · CONG_CU_TEST_BAN_KINH=x ⇒ "[C-ban-kinh]" rc=2 ·
                   CONG_CU_TEST_MANH_RA= (rỗng) ⇒ "[C-thieu-ra]" rc=2 · --gop (thiếu) ⇒ "[G-doi-so]" rc=2 · --la ⇒ "đối số lạ" rc=2
               (b) rc=0 "GOM MẢNH 8/8" … "SỐ LIỆU GOM: ca=60 · đột biến=416 · lỗi đột biến=0", 416 dòng `ok … bán kính 1/60`;
                   execve: python3.12 -B ops/cong_cu_test.py --gop ../gom8 → /usr/bin/python3.12 -X utf8 -B ops/cong_cu_test.py
                   --gop ../gom8 → git rev-parse HEAD   (ĐÚNG MỘT lần phóng; argv nguyên vẹn)
               (c) "[G-tap]: tập mảnh [0, 1, 2, 3, 4, 6, 7] ≠ 0..7" rc=1 ; cùng bộ dưới PYTHONUTF8=1 (CI) ⇒ rc=0 ; 0 .pyc
               (d) job `gate` THẬT qua phóng lại (`LC_ALL=C.UTF-8 PYTHONUTF8=0 CONG_CU_TEST_BAN_KINH=manh`, tam/ci/gate-r, strace -f):
                   RC=0 · `59/59 đạt; tổng=60, bỏ qua=1` · CỔNG TRÊN CÂY THẬT ĐẠT · TỰ KIỂM SONG SONG ĐẠT · `lỗi đột biến=0`;
                   1196 execve python: 15 mang `-X utf8` (mọi cái mang dấu =1) = 1 phóng lại cấp đỉnh + 14 phóng lại CỐ Ý của
                   `t62` (vế (0) `-B` và (4) `-B -X utf8=0` × 7 lần chạy `t62` = vòng CA + 3 tuần tự + 3 song song của tự kiểm; khớp
                   7 lần chạy của t60/t61/t52/t54); 32 con `--ban-kinh-con` đều PYTHONUTF8=1, không dấu, không `-X` ⇒ không phóng
                   lại; 36 python ngoài UTF-8 = 1 cấp đỉnh + 7 con `t61` + 28 con `t62` (ép ASCII CỐ Ý, theo thiết kế).
                   (Lần đếm đầu của lượt này ra 847/9/21 — regex bỏ sót dòng strace có PID đệm khoảng trắng; đã đếm lại, số trên.)
               (e) mảnh THẬT 0/8 ở env (b) (`LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii CONG_CU_TEST_MANH=0/8 …`), cây tiến trình
                   sống lúc 18:15Z (`/proc/<pid>/{cmdline,environ}`): 25004 `python3.12 ops/cong_cu_test.py` (PYTHONUTF8=0, ascii) →
                   25012 `/usr/bin/python3.12 -X utf8 ops/cong_cu_test.py` (PYTHONUTF8=1, utf-8, MANH=0/8, MANH_RA=manh/manh-0.txt,
                   DA_PHONG_LAI=1 lúc exec) → 31984 `… --ban-kinh-con [] t1_rc_gop …` (PYTHONUTF8=1, MANH giữ nguyên, KHÔNG dấu,
                   không `-X`) ⇒ đúng một lần phóng lại, biến mảnh đi qua, worker không phóng lại, dấu không sót
  kết luận   : KHÔNG PHẢI LỖI — env (kể cả chuỗi rỗng) và argv đi qua nguyên vẹn, mã 0/1/2 truyền đúng, không lặp. CI đặt
               PYTHONUTF8=1 ở `gate`, `gate-cong-cu` (8 mảnh) và `gate-cong-cu-gop` (ci.yml:69-72, 452-455, 510-513) ⇒ CI
               KHÔNG bao giờ đi nhánh phóng lại. Trọn 8 mảnh THẬT qua phóng lại (env (b)) + gom thật: BẢNG ĐO — 6/8 mảnh xanh,
               mảnh 1 đỏ vì thiếu jsonschema (môi trường), mảnh 5 đỏ vì P1; mọi tệp mảnh qua bộ nhận của chính tệp (60 ca/bản ghi).

HƯỚNG 3: `__file__` không phải tệp ở các dạng gọi khác — đo lại trên cây đã ghép (khối phóng lại giống từng byte b137bd8)
  lệnh       : cd tam/h2; env -u PYTHONDONTWRITEBYTECODE LC_ALL=C.UTF-8 PYTHONUTF8=0 python3.12 -B <dạng> --tu-kiem-che-do-utf8
  output     : tệp / -m ops.cong_cu_test / symlink ngoài cây / -I / -X utf8=0 ⇒ rc=5 "UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0"
               cat | /dev/stdin ⇒ rc=1 "KHONG_PHONG_LAI — nguồn '/dev/stdin'…" · - < tệp ⇒ rc=1 "'<stdin>'" · -c exec ⇒ rc=1 "''"
               zipapp cct.pyz ⇒ rc=1 "KHONG_PHONG_LAI — nguồn '…/cct.pyz/__main__.py'…" (PYTHONUTF8=1: ModuleNotFoundError
               'lease_publish_test' — dạng không được hỗ trợ ở cả nền); 0 .pyc để lại
  kết luận   : KHÔNG PHẢI LỖI (khớp lượt 4 HƯỚNG 2; sha256 AST của `_ep_utf8`, khối phóng lại, `_NAP_UTF8`, t60, t61:
               b137bd8 = c5f3da0 = 8757a84).

HƯỚNG 4: `_ep_utf8` ghi `os.environ` — có đụng ca #668 nào đo môi trường (t52/t53/t54) không
  lệnh       : awk 'NR>=7000 && /os\.environ|PYTHONUTF8|PYTHONIOENCODING|getenv/' ops/cong_cu_test.py
  output     : #668 chỉ đọc/ghi CONG_CU_TEST_{BAN_KINH,MANH,MANH_RA,TIEN_TRINH}: :7234/:8073 `{**os.environ, …}` (thừa kế);
               t54 F28 :7243 `cu_env = dict(os.environ)` … :7264-7265 `clear()` + `update(cu_env)` (khôi phục cả biến UTF-8);
               `_in_tu_kiem_main` :8221-8268 ghi os.environ trong TIẾN TRÌNH CON cửa; `_doc_che_do` thuần (:7708). 0 chỗ đọc
               PYTHONUTF8/PYTHONIOENCODING. Vòng CA head: (a) `59/59 đạt`, (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`
               `59/59 đạt` (t52/t53/t54 xanh ở cả hai).
  kết luận   : KHÔNG PHẢI LỖI.

HƯỚNG 5: dấu chống lặp `CONG_CU_TEST_DA_PHONG_LAI` sót sang con/cháu hay bị ca nào vô tình đặt
  lệnh       : grep -n "_DAU_PHONG_LAI\|CONG_CU_TEST_DA_PHONG_LAI" ops/cong_cu_test.py ; strace -f -v -e trace=execve trên
               `PYTHONUTF8=0 LC_ALL=C.UTF-8 python3.12 -B ops/cong_cu_test.py --gop ../gom8`
  output     : chỗ đặt: :45 (tên), :46 pop, :53 env lần phóng, `t62` (5) CỐ Ý, cửa in; #668: 0 chỗ.
               execve: python3.12 (PYTHONUTF8=0, dau=[]) → python3.12 -X utf8 (dau=CONG_CU_TEST_DA_PHONG_LAI=1, PYTHONUTF8=1,
               PYTHONIOENCODING=utf-8) → git (dau=[], PYTHONUTF8=1, PYTHONIOENCODING=utf-8)
  kết luận   : KHÔNG PHẢI LỖI — dấu chỉ trên đúng execve phóng lại; cháu không mang dấu nhưng mang biến UTF-8.

HƯỚNG 6: mã thoát 5 của cửa tự kiểm có va chạm mã nào khác sau khi ghép #668
  lệnh       : grep -n 'sys\.exit(' ; AST các `return` của main/_main_gop ; grep consumer trong ci.yml/.claude/dev
  output     : main {1, 2, 1-if-lỗi} · _main_gop {0/1, 2} · cửa `_CUA` ⇒ 0 (cong_that 0/9, ban_kinh_con 0/7) · đối số lạ 2 ·
               KHONG_PHONG_LAI `sys.exit(str)` ⇒ 1 · cửa UTF-8 ⇒ 5 (DUY NHẤT). Consumer: ci.yml:117,490 (không đối số, đòi 0),
               :534 `--gop manh`; `.claude/dev/ci_dang_ky_test.py:1068-1073` chỉ ghim chuỗi lệnh. Không ai đọc mã 5.
  kết luận   : KHÔNG PHẢI LỖI.

HƯỚNG 7: `t62` có đo đúng tiến trình CHẠY BỘ CA không (sau ghép: cửa đứng TRƯỚC phép tra `_CUA`, `main()` ở cuối khối)
  lệnh       : bản sao tam/h3: chèn `print(MAIN utf8_mode pid ppid DA_PHONG_LAI)` vào đầu `main()` và `print(GATE pid ppid)`
               vào cửa; `CONG_CU_TEST_BAN_KINH=hong` để main() dừng sớm rc=2
  output     : LC_ALL=C.UTF-8 PYTHONUTF8=0  ⇒ MAIN utf8_mode=1 pid=7488 ppid=7437 DA_PHONG_LAI=1 · GATE pid=7577 ppid=7562 →
                                               UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0
               LC_ALL=C … ascii             ⇒ MAIN utf8_mode=1 … DA_PHONG_LAI=1 · GATE … DA_PHONG_LAI=1
               PYTHONUTF8=1                 ⇒ MAIN utf8_mode=1 pid=7793 ppid=6014(shell) DA_PHONG_LAI=0 · GATE ppid=6014
  kết luận   : KHÔNG PHẢI LỖI — cửa và `main()` cùng loại tiến trình (bản phóng lại) ở mọi môi trường.

HƯỚNG 8: `t5` SIGPIPE `rc=141` có liên quan PR không
  lệnh       : git log 89fc4fa..fc852ff | grep 675 ; git diff 89fc4fa fc852ff -- ops/cai_cong_cu.sh ; git diff --stat fc852ff 8757a84
  output     : 7b308bc4 "Merge pull request #681 … cai-cong-cu-sigpipe" nằm trong fc852ff; `ops/cai_cong_cu.sh:64-66` thay
               `| head -1` bằng `LENH="${DAU_RA%%$'\n'*}"`; `ops/do_sigpipe.sh` có trong cây; PR (fc852ff..8757a84) không chạm hai tệp.
  kết luận   : KHÔNG PHẢI LỖI của PR — cơ chế ở nền cũ, đã vá trên master, cây ghép mang bản vá. Số lần `rc=141` trong các
               lượt trọn bộ của lượt này: xem BẢNG ĐO.

HƯỚNG 9: `t61` (mã con `encode("ascii","backslashreplace")`) + ca mới/ca #668 khi đường dẫn kho mang chữ Việt + dấu cách
  giả thuyết : sau ghép, con của `t61` nạp CẢ mã #668 cấp module (`_do_co_symlink`, đăng ký DOT_BIEN theo năng lực) — dưới LC_ALL=C
               và đường dẫn ngoài ASCII có thể chết lúc nạp (ĐỎ oan) hoặc vô can
  lệnh       : git clone --shared … "tam/có dấu cách/kho việt" ; <py> -X utf8 tam/cu/chay_ca.py . t49_ t52_ t53_ t54_ t60_ t61_ t62_ t63_
               × {python3.11, 3.12, 3.13} × {thường, LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii}
  output     : 6/6 lượt `TONG {"qua": 8}` ; 0 .pyc
  kết luận   : KHÔNG PHẢI LỖI.

HƯỚNG 10: chi phí của ca mới trong pha bán kính (mỗi đột biến chạy lại trọn CA) — trần mảnh CI 30 phút
  lệnh       : A/B cùng lệnh tam/tg/{h@8757a84,n@fc852ff}; python3.12 -X utf8 tam/cu/chay_ca.py . --tat-ca, xen kẽ h n h n (tải ~7)
  output     : head: 60 ca, 42,4 s / 43,2 s (t60 0,12–0,16 · t61 0,47–0,56 · t62 2,08–2,17 · t63 2,33–3,18 · t49 0,71–0,94) ;
               nền: 56 ca, 38,3 s / 37,3 s  ⇒ +5–6 s mỗi vòng CA ⇒ mỗi mảnh (52 đột biến, 2 tiến trình) +~2–3 phút.
               Thực đo mảnh 5/8 nền (env CI, 1 tiến trình, máy đang tải 8–10): 2209 s.
  kết luận   : KHÔNG PHẢI LỖI trên Linux; Windows KHÔNG ĐO ĐƯỢC (ghi vào nghiệm thu Windows).

HƯỚNG 11: merge có làm rơi/nhân đôi thay đổi nào của hai phía không
  lệnh       : so tập dòng ± của `git diff -U0 89fc4fa c5f3da0 -- ops/` với `git diff -U0 fc852ff 8757a84 -- ops/` (comm)
  output     : 332 / 333 dòng; chỉ ở nền cũ: `+    if "--tu-kiem-che-do-utf8" in sys.argv[1:]:` ; chỉ ở nền mới: chú thích `# #671:
               cửa tự kiểm …` + `+    if cua == "--tu-kiem-che-do-utf8":` — ngoài ra trùng khít
  kết luận   : KHÔNG PHẢI LỖI — merge chỉ đổi đúng dòng giải xung đột; PR so `fc852ff` chỉ 2 tệp (`git diff --stat`).

HƯỚNG 12: `t63` bơm lỗi có đo đúng chốt hay bị chốt khác bắt hộ; ca mới có kéo rộng bán kính không
  lệnh       : bảng đột biến (BẢNG ĐỘT BIẾN) + `mot_db.py` 4 `DOT_BIEN` đích t49 trên head + T63b (nuốt đỏ đối chứng) trên bản sao
  output     : mỗi phép tráo chết bằng ĐÚNG nhãn bước của nó ("(hash-object/rc)", "(update-index/rc)", "(ls-files/rong)", "(add/rc)",
               "(ops/no_cu.py/rc)", "(update-index/bo_ten)", "(update-index/bo_hong)"), không nhãn nào bắt hộ nhãn khác; T63a+M49m ⇒
               `bo_qua` (dòng ĐỎ OAN là thứ giết); N1/N2/N3 ⇒ chết. 4 `DOT_BIEN` đích t49 ⇒ `ok … 1/60`, t63 `bo_qua` "t49 ĐỎ cả khi
               KHÔNG tráo"; T63b ⇒ "ĐỎ bn_hien_thi_khong_don_anh: giết THÊM ['t63_…']"
  kết luận   : KHÔNG PHẢI LỖI cho `t63`. (Tín dụng giả do CA mới gây cho đột biến #668: có — HƯỚNG 1.)

HƯỚNG 13: quy ước argv[1] của cửa UTF-8 (#668 F25) có ca nào khoá không
  lệnh       : N6 = `if cua == "--tu-kiem-che-do-utf8":` → `if "--tu-kiem-che-do-utf8" in sys.argv[1:]:` (đúng dạng trước merge);
               python3.12 tam/cu/dot_bien.py --tat-ca N6_cua_do_moi_vi_tri
  output     : `SONG` — 60 ca, khác `qua` chỉ `t2` (bo_qua, jsonschema). Hậu quả đo trên bản sao N6 (tam/n6):
               `python3.12 -B ops/cong_cu_test.py --gop ../gom8 --tu-kiem-che-do-utf8` ⇒ in "UTF8_MODE=1 …", rc=5 (không gom);
               head cùng lệnh ⇒ "[G-doi-so]: cần đúng một thư mục sau --gop …" rc=2
  kết luận   : LỖI (biểu hiện 2 của CUA-UTF8-NGOAI-BANG-CUA): cửa đứng ngoài `cua`/`_CUA` nên phép đo F25 của `t52` không phủ nó.
               Hậu quả dưới N6: `--gop --tu-kiem-che-do-utf8` chạy cửa UTF-8 (rc=5) thay vì gom — đỏ, không xanh giả ⇒ gộp vào lớp P1.

HƯỚNG 14: (MÔ PHỎNG Windows) nền KHÔNG nhận tên byte `\xff` vào INDEX — `t63` có giữ "không ĐỎ oan" (spec §2B) không
  giả thuyết : `t63` dựng đối chứng năng lực nền bằng CHÍNH mã staging của `t49`; nền từ chối `\xff` thì `t49` bỏ qua ở (2) và mọi
               phép tráo "chờ bước X" sau (2) thành ĐỎ
  lệnh       : tam/gitgia/git (python, đầu PATH): `update-index --index-info` bỏ bản ghi có `\xff`, stderr "Ignoring path", rc=0;
               mọi lệnh khác exec /usr/bin/git. PATH=tam/gitgia:$PATH python3.12 -X utf8 tam/cu/chay_ca.py <cây> t49_ t63_
  output     : head: t49 `bo_qua` "KHÔNG ĐO ĐƯỢC: INDEX không nhận tên b'ops/xau_\xff.py': rc=0/0 b\"Ignoring path …\"" ;
                     t63 `giet_that` "(ops/no_cu.py/rc) bằng chứng stage hỏng mà t49 không BỎ QUA đúng bước (chờ 'no_cu'): …xau_…"
               bản HINT: y hệt (HINT không chạm `t63`)
  kết luận   : LỖI CÓ ĐIỀU KIỆN (mô phỏng; Windows thật KHÔNG ĐO ĐƯỢC) — biểu hiện (4) của NGHIEM-THU-WINDOWS-CON-THIEU [P2].
```

## BẢNG ĐỘT BIẾN

> Công cụ: `tam/cu/dot_bien.py` + `tam/cu/spec_db.py` (47 đột biến, mỏ neo nguyên văn từ `8757a84`, kiểm trước: mọi mỏ neo đếm
> đúng 1). Mỗi đột biến: `git clone --shared tam/dbv/base` (@`8757a84`) → thay ĐÚNG một lần mỗi mỏ neo → xoá `__pycache__` →
> `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` riêng → `python3.12 -X utf8 tam/cu/chay_ca.py` nạp tệp bằng importlib (module ≠ `__main__`)
> và chạy ca qua `_chay_1_ca` CỦA CHÍNH tệp ⇒ `giet_that` chỉ khi `TinHieuChotCa` mang đúng tên ca; cột "nhãn" = chuỗi chốt
> phải có trong lý do. Log: `tam/log/db-head-312.jsonl` (+ `db2-head-312.jsonl`, `db-N6-tatca.jsonl`). Tổng: **49 đột biến tay đúng
> kỳ vọng** (45 `giet_that` đúng nhãn · 3 `bo_qua` + 1 `tin_dung_gia` kỳ vọng) + **N6 SỐNG** (lỗ của lớp P1); 0 ca khác đỏ (trừ
> `t49 bo_qua` ở M49e — đúng: KHÔNG ĐO ĐƯỢC, không ĐỎ oan). Chéo phiên bản/locale (`tam/log/db-cheo-*.jsonl`): H49h, M49m, C2_hong_do,
> P4, N1, R5, M61b, M60a ⇒ `giet_that` đúng nhãn trên python3.11, python3.13 và python3.12 dưới `LC_ALL=C PYTHONUTF8=0
> PYTHONIOENCODING=ascii` (8/8 × 3).

| đột biến (thay đúng 1 chỗ trên 8757a84) | ca đích | kết quả (3.12) — tín hiệu | phân loại |
|---|---|---|---|
| R1 `if False:` thay khối phóng lại | t62 | `giet_that` "chạy làm __main__ … KHÔNG ở chế độ UTF-8: 'UTF8_MODE=0 …'" | giết thật |
| R2 nuốt mã (`.returncode * 0`) | t62 | `giet_that` "(1) mã thoát KHÔNG đi qua … rc=0, chờ 5" | giết thật |
| R3 `sys.argv` thay `sys.orig_argv[1:]` | t62 | `giet_that` "(2) cờ `-B` mất … B=0" | giết thật |
| R4 `.get` thay `.pop` (dấu sót) | t62 | `giet_that` "(3) … DAU_SOT=1" | giết thật |
| R5 bỏ `"-X", "utf8"` | t62 | `giet_that` "(4) … rc=1 … KHONG_PHONG_LAI — đã phóng một lần" | giết thật |
| R6 bỏ `_DA_PHONG_LAI or` | t62 | `giet_that` "(5) … rc=5 'UTF8_MODE=1 …'" | giết thật |
| R7 bỏ `not os.path.isfile` | t62 | `giet_that` "(6) `python -B - …` … rc=0 stdout=0" | giết thật |
| R8 bỏ `__name__ == "__main__"` | t61 | `giet_that` "(e) NẠP … bị PHÓNG LẠI … `(0) nap\n(0) nap`" | giết thật |
| R9 không đặt dấu (`env={**os.environ}`) | t62 | `giet_that` "(4) … 'DA_PHONG_LAI=0'" | giết thật |
| R10 từ chối nhưng thoát 0 | t62 | `giet_that` "(5) … rc=0 … KHONG_PHONG_LAI" | giết thật |
| M61a gỡ `reconfigure` | t61 | `giet_that` "(a) … rc=1" | giết thật |
| M61b gỡ env cho con (spec §6.3 ii) | t61 | `giet_that` "(b) cháu … không in được byte UTF-8 thật" | giết thật |
| M61c chỉ stdout | t61 | `giet_that` "(c) stderr … không mang chữ Việt UTF-8 THẬT" | giết thật |
| M61d bỏ `PYTHONUTF8` | t61 | `giet_that` "(d) cháu phải ở UTF-8 mode …" | giết thật |
| M61e con `ascii:backslashreplace` | t61 | `giet_that` "(b) … `(b) ch\\u1eef`" | giết thật |
| M61f bỏ `hasattr` | t61 | `giet_that` "(f) luồng KHÔNG có `reconfigure` …" | giết thật |
| M61g `errors="strict"` | t61 | `giet_that` "(g) … rc=1" | giết thật |
| M60a docstring `r"""`→`"""` ở bash_nen (spec §6.3 i) | t60 | `giet_that` "(1) … SyntaxError: invalid escape sequence '\(' (bash_nen.py, line 898)" | giết thật |
| P0 gỡ `-B` ở (0) | t62 | `giet_that` "(2) cờ `-B` mất … B=0" | giết thật |
| P4 gỡ `-B` ở (4) (vá 5) | t62 | `giet_that` "(4) … (giữ `-B`) … B=0" | giết thật |
| M49a/b/c bỏ `oid.returncode`/`r.returncode`/`not co` | t63 | `giet_that` "(hash-object/rc)… 'rc=128/0'" · "(update-index/rc)… 'rc=0/128'" · "(ls-files/rong)… 'xau_'" | giết thật ×3 |
| M49d bỏ `ga.returncode` | t63 | `giet_that` "(add/rc) … chờ 'bình_thường'" | giết thật |
| M49e luôn ném | t63 | `giet_that` "(ops/no_cu.py/rc) … chờ 'no_cu'"; t49 `bo_qua` | giết thật (t49 không ĐỎ oan) |
| M49h (3) quay lại `git add -A` không rc | t63 | `giet_that` "(ops/no_cu.py/rc) … chờ 'no_cu'" | giết thật |
| M49m `_stage_byte` hỏng ⇒ `bang(False)` | t63 | `giet_that` "(hash-object/rc) stage hỏng mà t49 ĐỎ thay vì BỎ QUA — ĐỎ OAN" | giết thật (sống ở b137bd8) |
| M49n `_add` hỏng ⇒ `bang(False)` | t63 | `giet_that` "(add/rc) … ĐỎ OAN" | giết thật (sống ở b137bd8) |
| H49f nuốt lỗi stage `\` rồi `return` | t63 | `giet_that` "(update-index/bo_ten) … chờ 'va_'" | giết thật |
| H49l nuốt lỗi stage `\` rồi quét tiếp | t63 | `giet_that` "(update-index/bo_ten) … ĐỎ OAN: (2d) HAI đường … MỘT khoá" | giết thật (≙ M49i/M49l lượt 4) |
| H49g stage tên `\` TRƯỚC (3) | t63 | `giet_that` "(bo_ten) t49 BỎ QUA trước khi đo (3)" | giết thật |
| H49h stage tên `\` SAU (3), TRƯỚC (2d) thuần | t63 | `giet_that` "(bo_ten) t49 BỎ QUA trước hai chốt THUẦN (2d)" | giết thật |
| C2_bt_do / C2_bt_nuot (chỗ gọi `_add(bình_thường)`) | t63 | "(add/rc) … ĐỎ OAN" / "(add/rc) … chờ 'bình_thường'" | giết thật ×2 |
| C2_xau_do / C2_xau_nuot (chỗ gọi `xau_`) | t63 | "(hash-object/rc) … ĐỎ OAN" / "(ls-files/rong) … chờ 'xau_'" | giết thật ×2 |
| C2_hong_do (chỗ gọi `hong_` ⇒ ĐỎ) | t63 | `giet_that` "(update-index/bo_hong) … ĐỎ OAN … b'Ignoring path'" | giết thật |
| C2_hong_nuot (nuốt lỗi `hong_`) | t63 | `bo_qua` "t49 bỏ qua vì lý do khác … cú pháp HỎNG mà cổng không fail-close" | kỳ vọng (KHÔNG ĐO ĐƯỢC, không ĐỎ oan — spec §2B) |
| C2_va_do (stage `va_` ⇒ ĐỎ) | t63 | `giet_that` "(update-index/bo_ten) … ĐỎ OAN" | giết thật |
| C2_nocu_do / C2_nocu_nuot | t63 | "(ops/no_cu.py/rc) … ĐỎ OAN" / "… chờ 'no_cu'" | giết thật ×2 |
| T63a gỡ `bang(not doi_chung_xanh…)` + M49m | t63 | `bo_qua` (M49m SỐNG khi thiếu chốt) | kỳ vọng — chứng minh chính dòng ấy là thứ giết |
| **N1 (MỚI)** `nap` không ghi `("(2d)", s)` | t63 | `giet_that` "(bo_ten) … trước hai chốt THUẦN (2d)" | giết thật (chốt thứ tự có răng) |
| **N2 (MỚI)** t49 bỏ qua `nap` (`runpy.run_path`) | t63 | `giet_that` "(bo_ten) … trước hai chốt THUẦN (2d)" | giết thật |
| **N3 (MỚI)** khoá tráo `bo_hong` sai (`b"hong_X"`) | t63 | `giet_that` "(update-index/bo_hong) … chờ 'hong_'" | giết thật |
| **N5 (MỚI)** cửa UTF-8 thoát 0 | t62 | `giet_that` "(1) … rc=0, chờ 5" | giết thật |
| **N6 (MỚI)** cửa UTF-8 dò MỌI vị trí (`in sys.argv[1:]` — đúng dạng trước merge) | cả 60 ca (`--tat-ca`) | **SỐNG** — khác `qua` chỉ `t2` (bo_qua, jsonschema) | **SỐNG SÓT** — biểu hiện (2) của CUA-UTF8-NGOAI-BANG-CUA |
| M49o `_stage_byte` ném `RuntimeError` | t63 | `tin_dung_gia` "RuntimeError: …" | kỳ vọng (doctrine `TinHieuChotCa`; `main()` vẫn đếm ĐỎ) |
| RIG (đối chứng chạy dưới `bo_ten`) + M49n | t63 | `bo_qua` "… đối chứng không XANH" | kỳ vọng |
| T63d (`doi_chung_xanh = False`→`True`) + RIG + M49n | t63 | `giet_that` "(add/rc) … ĐỎ OAN" | giết thật (nhánh BỎ QUA của đối chứng phân biệt được) |
| T63b (nuốt ĐỎ của đối chứng: `raise BoQuaMoiTruong(…KHÔNG tráo…)` → `doi_chung_xanh = True`) | bán kính `bn_hien_thi_khong_don_anh` (đích t49) | `ĐỎ … giết THÊM ['t63_…']` (head không T63b: `ok … 1/60`, t63 `bo_qua`) | giết thật (qua bán kính — nhánh ĐỎ-đối-chứng giữ 1/N) |
| **f25_cua_moi_vi_tri (DOT_BIEN #668, đích t52)** | t52 (+t62) | head: t52 `giet_that`, **t62 `tin_dung_gia`** ⇒ dòng ĐỎ; nền fc852ff: `ok … 1/56`; bản HINT: `ok … 1/60` | **TÍN DỤNG GIẢ do ca #671** — finding CUA-UTF8-NGOAI-BANG-CUA |

## BẢNG ĐO
| khẳng định | executor khai | đo được | khớp? |
|---|---|---|---|
| dòng thêm so merge-base mới `fc852ff` (ADR-0044 ≤ 300) | +292 (phiên điều phối; thân merge) | `git diff --numstat fc852ff 8757a84` ⇒ `1 1 ops/bash_nen.py` + `291 40 ops/cong_cu_test.py` = **+292/−41** | khớp |
| PR so master chỉ 2 tệp | có | `git diff --stat fc852ff 8757a84` ⇒ 2 files changed | khớp |
| vá 5 so `b137bd8` | `63 insertions(+), 50 deletions(-)`, 1 tệp | `63 50 ops/cong_cu_test.py` | khớp |
| so merge-base cũ `89fc4fa` (BAO_CAO §6) | +291/−41 | `1 1` + `290 40` | khớp |
| sha256 `cong_cu_test.py` bản vá (BAO_CAO) | `5460de71…` | `c5f3da0`: `5460de71681b0522…`; `b137bd8`: `5746c084…` | khớp |
| ruff `--select F` delta 0 | tập bằng nền | ruff 0.15.15 (`pip --target tam/ruff --no-cache-dir`), `--no-cache --isolated`: `fc852ff` = `c5f3da0` = `8757a84` = `89fc4fa` = {`bash_nen.py` F401 `ast`; `cong_cu_test.py` F841 `ci`} (so tập, bỏ số dòng) | khớp |
| docstring `_tach_dinh_dang` không đổi byte (spec §2A) | có | `1741e0a` = `fc852ff` = `8757a84` = `3bc957a67247801b…`, 897 ký tự | khớp |
| compile không `SyntaxWarning` mới | có | `-W error` compile 2 tệp @`8757a84`: rc=0 trên 3.11/3.12/3.13 | khớp |
| mọi dòng thêm ≤ 118 ký tự | có | 292 dòng thêm so `fc852ff`, max 118, 0 vượt | khớp |
| trọn bộ (a) trên `c5f3da0` | `56/56`, lỗi đột biến 1 | vòng CA thật (`__main__`, dừng sau dòng tổng): `56/56 đạt; tổng=57, bỏ qua=1` (t2, jsonschema). Pha bán kính của `c5f3da0` KHÔNG đo lại (SHA trước merge) | khớp phần đo được |
| trọn bộ (b) trên `c5f3da0` | `56/56` | vòng CA (b) qua phóng lại: `56/56 đạt; tổng=57, bỏ qua=1` | khớp phần đo được |
| thân merge: "t49 t52 t53 t54 t60 t61 t62 t63 xanh ca moi truong thuong lan LC_ALL=C ep ASCII" | có | 8/8 `qua` × {thường, ascii} × {3.11, 3.12, 3.13}, kể cả đường dẫn chữ Việt + dấu cách (HƯỚNG 9) | khớp |
| thân merge: "0 .pyc" | có | `t62` một mình ⇒ 0; CI `gate` + mảnh ⇒ `pyc_con_lai=0` | khớp |
| thân merge: "doctrine-scan sach" | có | `python3.12 -B .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ rc=0 "sạch — đã quét 10 tệp, 0 chỗ chép doctrine" | khớp |
| thân merge: "dat cua UTF-8 theo dung quy uoc #668" | có | argv[1]-only: đúng; một bảng `_CUA`: KHÔNG — cửa ngoài bảng ⇒ `f25` tín dụng giả, N6 sống | **KHÔNG khớp** (P1) |
| **"lỗi đột biến = nền"** (phiên điều phối, sau merge) | = nền | A/B `f25_cua_moi_vi_tri`: head loi=1 (t62 `tin_dung_gia`) · nền loi=0 (`ok 1/56`). **Mảnh CI 5/8 thật (env CI `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 CONG_CU_TEST_MANH=5/8 CONG_CU_TEST_MANH_RA=manh/manh-5.txt`, 1 tiến trình, hai vế dựng cùng lệnh):** head ⇒ **RC=1**, 51 `ok` + `ĐỎ f25_cua_moi_vi_tri … tín dụng giả`, `ĐỎ mảnh 5/8 [M-loi]: 1 lỗi đột biến — không ghi tệp` (2489 s, `tam/log/ci-m5-head.txt`); nền ⇒ **RC=0**, 52/52 `ok`, `MẢNH 5/8: 52/52 … ghi manh/manh-5.txt` (2209 s). Gom thiếu mảnh 5 ⇒ `[G-tap]` rc=1 (HƯỚNG 2c) | **KHÔNG khớp** (+1) |
| BAO_CAO §3 "41/41 phải chết chết đúng nhãn; 4 kỳ vọng không giết (M49o · C2_hong_nuot · T63a+M49m · RIG+M49n)" | có | cùng 41 + N1/N2/N3/N5 của lượt này ⇒ 45 `giet_that` đúng nhãn; M49o `tin_dung_gia`, C2_hong_nuot/T63a+M49m/RIG+M49n `bo_qua`; T63d+RIG+M49n `giet_that` "(add/rc) … ĐỎ OAN" | khớp |
| BAO_CAO "4 `DOT_BIEN` đích t49 ⇒ ok … 1/57; T63b ⇒ giết THÊM t63" | có (trước merge) | sau merge: 4/4 `ok … bán kính 1/60`, t63 `bo_qua`; T63b ⇒ "giết THÊM ['t63_…']" | khớp (mẫu số đổi do merge) |
| BAO_CAO §2 lớp 3: `t62` một mình head 2 `.pyc` → bản vá 0 | có | `b137bd8` 2 · `8757a84` 0 | khớp |
| chú thích khối phóng lại "(lượt 4 đo: 3 tiến trình còn sống)" | 3 | lượt này: 1 (lượt 4 reviewer: 2) | ảnh chụp theo thời điểm — không tính finding mới |
| `t63` ~2,1–2,4 s (BAO_CAO) | có | 2,33–3,18 s dưới tải ~7 | cùng bậc |
| mảnh 5/8 bản HINT (env CI, `tam/ap` = 8757a84 + HINT, 2 tiến trình) | — | **RC=0** · `59/59 đạt` · 52/52 `ok` (`f25_cua_moi_vi_tri → giết đúng 't52_…' · bán kính 1/60`) · `MẢNH 5/8: 52/52 … ghi manh/manh-5.txt` · 1758 s · 0 `.pyc` (`tam/log/ci-m5-hint.txt`) | bản vá đóng P1 ở mức mảnh CI |
| **trọn bộ (b) dạng chia mảnh** — 8 mảnh THẬT ở env (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` (qua phóng lại), mỗi mảnh `TIEN_TRINH=1`, clone riêng `tam/mb/s{k}` @8757a84 | — | mảnh 0: RC=0 · 52/52 `ok` · ghi `manh/manh-0.txt` (2574 s) · mảnh 1: RC=1 · 51 `ok` + `KHÔNG_ĐO_ĐƯỢC t2_go_canary` (thiếu jsonschema — môi trường, = lượt 4/executor) · `[M-loi]` (2581 s) · mảnh 2: RC=0 · 52/52 (2574 s) · mảnh 3: RC=0 · 52/52 (2583 s); mảnh 4: RC=0 · 52/52 (2840 s) · mảnh 5: **RC=1** · 51 `ok` + **ĐỎ `f25_cua_moi_vi_tri` (t62 `tin_dung_gia`)** · `[M-loi]`, không ghi tệp (2841 s) · mảnh 6: RC=0 · 52/52 (2843 s) · mảnh 7: RC=0 · 52/52 (2873 s). Mọi mảnh: vòng CA `59/59` qua phóng lại, `rc=141` 0, `.pyc` 0. **Tổng bán kính 416: 414 `ok … bán kính 1/60` · 1 `KHÔNG_ĐO_ĐƯỢC t2_go_canary` (môi trường) · 1 ĐỎ `f25` (P1)**; ngoài `f25`, 0 dòng bán kính/chi tiết nào nhắc `t60`–`t63` ⇒ ca mới không kéo rộng bán kính của 415 đột biến còn lại. **Gom** (env (b), qua phóng lại) trên 6 tệp thật ⇒ `[G-tap]: tập mảnh [0, 2, 3, 4, 6, 7] ≠ 0..7` rc=1; 6 tệp đều qua `_nhan_ket_qua_con` CỦA tệp (vân tay khớp, 312/312 bản ghi, mỗi bản ghi đủ 60 ca, 0 lỗi) | lỗi đột biến head = 2 (1 môi trường + 1 P1) so nền = 1 (môi trường) ⇒ **delta +1** (spec §6.1 đòi ≤ 0) |
| CI `gate` (env CI, `CONG_CU_TEST_BAN_KINH=manh`) trên head | (không ai khai) | RC=0 · `59/59 đạt; tổng=60, bỏ qua=1` · CỔNG TRÊN CÂY THẬT ĐẠT · TỰ KIỂM SONG SONG ĐẠT · `SỐ LIỆU: ca=60 · đột biến=416 (giao mảnh) · lỗi đột biến=0` · 326 s · 0 `.pyc` | — |

## FINDINGS

### CUA-UTF8-NGOAI-BANG-CUA  [P1]  Cửa `--tu-kiem-che-do-utf8` đặt NGOÀI bảng `_CUA` ⇒ đột biến #668 `f25_cua_moi_vi_tri` làm `t62` chết tín dụng giả ⇒ dòng bán kính ĐỎ (lỗi đột biến +1 so nền), mảnh CI `gate-cong-cu` 5/8 đỏ ⇒ `gate-cong-cu-gop` đỏ
TỆP/DÒNG: `ops/cong_cu_test.py:8630-8635` (khối `__main__` — khối DUY NHẤT giải xung đột của merge `8757a84`); đột biến
`DOT_BIEN["f25_cua_moi_vi_tri"]` (`:2129`, đích `t52`, #668 F25); `t62` `:2906-2943` (gọi cửa ở argv[1], `dung("UTF8_MODE=" in ra)`).
VẤN ĐỀ: thân merge khai "dat cua UTF-8 theo dung quy uoc #668, TRUOC phep tra _CUA". Đúng một nửa: cửa chỉ đọc argv[1] (khớp F25),
nhưng quy ước #668 là MỘT bảng cửa `_CUA` — mọi phép đo dispatcher (đột biến `f13`/`f25`/`f27`/`f28`) giả định mọi cửa đi qua bảng ấy.
Cửa UTF-8 đứng NGOÀI bảng là một đường dispatch THỨ HAI mà các đột biến dispatcher của #668 không biết tới. Hệ quả ĐO ĐƯỢC:
(1) dưới `f25_cua_moi_vi_tri` ("dò cửa theo `_CUA`"), lời gọi `… --tu-kiem-che-do-utf8` của `t62` không được nhận ra ⇒ con rơi vào
`sys.exit(main())` ⇒ chết `FileNotFoundError` trong cây đột biến tối giản ⇒ `t62` `tin_dung_gia` ⇒ `_ket_luan_ban_kinh` in
"ĐỎ … chết bằng lỗi VÔ CAN (tín dụng giả) ⇒ bán kính không đọc được", +1 lỗi đột biến (nền `fc852ff`: `ok … 1/56`). Đây ĐÚNG câu hỏi
(iii) của prompt — "đột biến mới của #668 có bị ca #671 giết thêm (tín dụng giả) không": CÓ, một cái. Trong CI: `f25` thuộc mảnh 5/8
⇒ mảnh ấy `[M-loi]`, KHÔNG ghi tệp ⇒ job gom `[G-tap]` ⇒ PR đỏ (spec §6.5 "CI PR (ubuntu): xanh"; §6.1 "delta lỗi đột biến ≤ 0" —
nay +1). (2) N6 (cửa UTF-8 đổi về "dò MỌI vị trí" — đúng dạng lỗi F25 của #668) SỐNG cả 60 ca: quy ước argv[1] của cửa này không
ca nào khoá, vì nó không đi qua `cua`/`_CUA` mà `t52` đo. Lời khai "lỗi đột biến = nền" của phiên điều phối không được đo sau merge
(thân merge chỉ liệt kê 8 ca + doctrine-scan + số dòng) — lời khai rộng hơn phép đo.
VÁ Ở ĐÂU: khối `__main__` + một hàm cửa cạnh các `_in_tu_kiem_*` (tệp test, cửa tự kiểm chỉ `t62` gọi).
VÁ THẾ NÀO: (mã TEST đầy đủ — HINT hunk 2–3) chuyển thân cửa thành `_in_tu_kiem_che_do_utf8()` (in bốn cờ, `sys.exit(_MA_TU_KIEM_UTF8)`
— tự thoát mã RIÊNG nên `sys.exit(0)` sau `_CUA[cua]()` không bao giờ chạy tới), ĐĂNG KÝ `"--tu-kiem-che-do-utf8"` trong `_CUA`, bỏ khối
`if cua == "--tu-kiem-che-do-utf8"` viết riêng. Khối `__main__` trở lại y hệt master `fc852ff` trừ một khoá bảng.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: khoá là CHÍNH vòng bán kính của `f25_cua_moi_vi_tri` (mảnh CI 5/8) cộng `t62`. Đã chạy trên bản áp
(`tam/hint` ≡ `tam/ap`): `f25_cua_moi_vi_tri` ⇒ `ok … giết đúng 't52_…' · bán kính 1/60`; cả 9 đột biến dispatcher #668 (`f13`, `f25`×2,
`f27`×2, `f28`×4) ⇒ `ok … 1/60`; `t49 t52 t53 t54 t60 t61 t62 t63` ⇒ `qua`. Đột biến phải chết sau vá: "đưa cửa ra lại ngoài `_CUA`"
(= cấu trúc `8757a84`) ⇒ `f25` ĐỎ tín dụng giả (đo: chính `8757a84`); N5 (cửa thoát 0) ⇒ `t62` (1); gỡ khoá khỏi bảng ⇒ `t62`
`tin_dung_gia` + suite ĐỎ (cửa trả "đối số lạ" rc=2, `dung` bắt — không lọt xanh). N6 không còn biểu diễn được riêng (cửa dùng chung
`cua`; đột biến `cua` là `f25`, `t52` giết).
BẢN VÁ CÓ THỂ ĐẺ RA: (1) thứ tự: `--gop` vẫn được tra trước `_CUA` như master — không đổi. (2) `t54` F28 exec khối `__main__` trích từ
tệp với `globals()` ⇒ cần `_in_tu_kiem_che_do_utf8` ở cấp module (đã đặt) — `t54` `qua` trên bản áp. (3) Một cửa trong `_CUA` mà tự
`sys.exit` khác 0 là ngoại lệ duy nhất của bảng (các cửa khác trả về rồi `sys.exit(0)`); `_in_tu_kiem_cong_that` cũng đã tự
`sys.exit(0/9)` ⇒ có tiền lệ. (4) +297 dòng so `fc852ff` (trần 300) — còn 3 dòng biên cho vòng vá sau.
HINT (hunk nào): hunk 2 (`@@ -8619`), hunk 3 (`@@ -8626`).
ĐÃ THỬ NGHIỆM HINT: xem "HINT.patch — tự kiểm" (dry-run rc=0, áp thật, `cmp` = bản đã chạy, các phép đo trên).
ĐỘ TIN: cao (A/B cùng lệnh; tái hiện đường gọi con; mảnh 5/8 THẬT ở env CI (head RC=1 / nền RC=0 / head+HINT RC=0) và ở env (b)
qua phóng lại (head RC=1); trọn bán kính 416 ở env (b): `f25` là dòng ĐỎ DUY NHẤT do PR — ngoài nó chỉ còn `t2_go_canary` môi trường).
ĐO (A/B, hai vế `tam/db/f25h`@`8757a84` + `tam/db/f25n`@`fc852ff` dựng trong CÙNG một lệnh; `tam/cu/mot_db.py` gọi `_do_mot` +
`_ket_luan_ban_ghi` CỦA CHÍNH tệp):
```
head 8757a84: DB f25_cua_moi_vi_tri dich=t52_… giay=41.2 loi= 1
    t62_ tin_dung_gia giàn giáo hỏng (chưa tới chốt nghiệp vụ): cửa --tu-kiem-che-do-utf8 không in gì: rc=1 … FileNotFoundError
  >   ĐỎ  f25_cua_moi_vi_tri: ca ['t62_chay_lam_main_phai_o_che_do_UTF8_ca_khi_PYTHONUTF8_0'] chết bằng lỗi VÔ CAN (tín dụng giả) ⇒ bán kính không đọc được
nền fc852ff:  DB f25_cua_moi_vi_tri dich=t52_… giay=37.7 loi= 0
  >   ok  f25_cua_moi_vi_tri → giết đúng 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' · bán kính 1/56
```
Cơ chế (tái hiện lời gọi con của `t62` trên cây đột biến tối giản do `_dung_cay_dot_bien` dựng): f25 thay `cua = sys.argv[1] …` bằng
`next((c for c in reversed(sys.argv[1:]) if c in _CUA or c == "--gop"), None)`; `--tu-kiem-che-do-utf8` không thuộc `_CUA` ⇒ `cua=None`
⇒ `sys.exit(main())` ⇒ `_chay_tien_kiem(batch_behavior_test)` ⇒ `shutil.copy2(CAI_SH, …)` ⇒ `FileNotFoundError` (`ops/cai_cong_cu.sh`
không có trong cây đột biến) ⇒ rc=1, stdout rỗng ⇒ `dung("UTF8_MODE=" in ra)` ⇒ `LoiDungCa` ⇒ `tin_dung_gia`. Vị trí: `f25` ở chỉ số 325
của `DOT_BIEN` ⇒ mảnh CI **5/8** (`t2_go_canary` — lỗi môi trường jsonschema — ở mảnh 1).

### NGHIEM-THU-WINDOWS-CON-THIEU  [P2]  Chưa có nghiệm thu §6 trên Windows neo exact head (vá 5 + merge đổi cả hai tệp so lần đo Windows cuối)
TỆP/DÒNG: spec §2B ("BƯỚC ĐẦU trên Windows: ĐO giả thuyết B TRƯỚC khi vá"), §6.1–6.3; BAO_CAO §7 ("KHÔNG làm ở đây").
VẤN ĐỀ: không có, cho `8757a84`: `N/N` Windows hai số bằng nhau; danh sách + lý do từng ca bỏ qua; delta lỗi đột biến so NỀN cùng
máy; lượt ép ASCII cho con; §6.3 (i)(ii) chạy trên Windows; log staging thật của `t49`. Lời khai Windows duy nhất vẫn ở thân
`e46f569`/`bd6ad5d` (SHA khác, không log). Sau merge còn thêm hai điểm Windows chưa đo: (a) mảnh/gom #668 trên `windows-latest`
(ma trận `chuan-bi` cho master) với ca `t60`–`t63` (một vòng CA +5–6 s trên Linux; Windows tạo tiến trình đắt hơn, trần mảnh 30 phút);
(b) `t63` (bo_ten/bo_hong) chỉ MÔ PHỎNG lời khai "Git for Windows bỏ tên mang `\`"; (c) **MÔ PHỎNG MỚI của lượt này** — nếu nền cũng
KHÔNG nhận tên byte `\xff` (spec §8 "chưa đo được"; BAO_CAO §7 tự khai rủi ro, không đo): `git` giả đầu PATH (`tam/gitgia/git`: bỏ bản
ghi chứa `\xff` ở `update-index --index-info`, in "Ignoring path", rc=0) ⇒ head VÀ bản HINT: `t49` `bo_qua` "INDEX không nhận tên
b'ops/xau_\xff.py'" (đúng spec), nhưng **`t63` `giet_that` "(ops/no_cu.py/rc) … chờ 'no_cu'"** — ĐỎ OAN ở chính ca khoá (spec §2B
"không ĐỎ oan"). Gốc: `t63` lấy chính mã staging của `t49` làm đối chứng năng lực nền nên không tách được "nền không stage được `\xff`"
khỏi đột biến "luôn ném" (M49e — đang được giết đúng qua chính phép tráo ấy). Theo spec §2B/S2 phải ĐO trên Windows trước; nếu đo ra
từ chối `\xff` thì DỪNG, báo chủ kho; hướng vá sẵn (mã TEST, chưa đưa vào HINT vì phải đo trước + trần 300): phép dò năng lực ĐỘC LẬP
(`git init` tạm, `hash-object` + `update-index --index-info` một tên `n_\xff`, `ls-files -z`) chỉ trong nhánh `os.name == "nt"` ⇒
`BoQuaMoiTruong`; POSIX giữ nguyên nên M49e vẫn chết (như `_do_co_symlink` của #668 cho symlink).
VÁ Ở ĐÂU: nghiệm thu (hiện vật), không phải mã. VÁ THẾ NÀO: trên máy Windows local, neo head SAU khi vá P1: nền `fc852ff` rồi head,
`python ops\cong_cu_test.py` KHÔNG đặt `PYTHONUTF8` ⇒ in nguyên khối BỎ QUA/ĐỎ/SỐ LIỆU; cùng bộ với `PYTHONIOENCODING=ascii
PYTHONUTF8=0`; §6.3 (i)(ii) trên bản sao tạm; log `git add`/`update-index`/`ls-files -z` của `t49`.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: không áp dụng (nghiệm thu); M60a và M61b phải chạy TRÊN Windows (Linux: cả hai `giet_that` đúng nhãn).
BẢN VÁ CÓ THỂ ĐẺ RA: không. HINT (hunk nào): không có hunk — không vá được bằng mã ở Linux (chủ kho: "Chỉ chạy tại máy").
ĐÃ THỬ NGHIỆM HINT: không áp dụng. ĐỘ TIN: cao (đối chiếu hiện vật); mọi phần Windows KHÔNG ĐO ĐƯỢC.

### TU-PHONG-LAI-KHONG-TRONG-SUOT  [P3]  (biểu hiện (b)) Harness giết tiến trình bao ⇒ bản phóng lại `-X utf8` mồ côi — đã khai, CHƯA có quyết định chủ kho
TỆP/DÒNG: `ops/cong_cu_test.py:47-53` (khối phóng lại, giống từng byte `b137bd8`), chú thích `:40-44`.
VẤN ĐỀ: đo lại trên `8757a84` (`tam/cu/do_mo_coi.py`): `LC_ALL=C.UTF-8 PYTHONUTF8=0` ⇒ bao rc=-9, còn 1 tiến trình
`python3.12 -X utf8 -B ops/cong_cu_test.py` sau 2 s; SIGTERM tới con ⇒ rc bao 241; `PYTHONUTF8=1` ⇒ 0. Hạng giữ theo lượt 3/4.
VÁ Ở ĐÂU / THẾ NÀO: chờ quyết định chủ kho (prompt: "giữ hạng, không đòi vá vòng này") — (A) nhận nợ có tên + packet kế nhiệm, hoặc
(B) POSIX `os.execve` + khoá ép nhánh `subprocess` cho `t62`, Windows Job Object. CA KHOÁ: nếu (B) — `t62` thêm vế PID. BẢN VÁ CÓ THỂ
ĐẺ RA: (B) Linux mặc định thôi đi nhánh Windows. HINT: không có hunk (lựa chọn kiến trúc). ĐÃ THỬ NGHIỆM HINT: không áp dụng. ĐỘ TIN: cao.

### LOI-KHAI-RONG-HON-PHEP-DO  [P4]  (tái phát do ghép #668) Con số AST trong chú thích đầu tệp đã trôi: "36 Call … 3 `{**os.environ}`" nay là 38 / 5
TỆP/DÒNG: `ops/cong_cu_test.py:14-17`.
VẤN ĐỀ: `tam/cu/dem_env.py` (AST, Call có keyword `env`): b137bd8 = c5f3da0 = 36 {Name 17, moi_truong 12, dict(os.environ) 3,
dict(env) 1, {**os.environ} 3}; fc852ff = 35; **8757a84 = 38** {Name 17, {**os.environ} **5**, moi_truong 12, dict(os.environ) 3,
dict(env) 1}. Hai điểm phóng MỚI là của #668 (`:7234` `t54` F26, `:8073` `_in_tu_kiem_gom`), cả hai `{**os.environ, …}` ⇒ vẫn thừa kế
biến UTF-8 (tính chất ĐÚNG — câu "Điểm phóng viết SAU phải tự giữ điều đó" được giữ); chỉ SỐ HẠNG trôi. Có neo điều kiện "(AST, lượt
vá 4)" nên hạ P4, nhưng "trong tệp này" đọc trên `8757a84` là sai — đúng bài học "một bất biến còn đúng không chứng minh các số hạng
còn đúng".
VÁ Ở ĐÂU: chú thích `:15-16`. VÁ THẾ NÀO: (chú thích — HINT hunk 1) "ĐÃ ĐO (AST, sau ghép #668): 38 Call … 5 `{**os.environ, …}` (2 của
#668) …". CA KHOÁ: không (chú thích); phép kiểm: `tam/cu/dem_env.py` trên bản áp ⇒ 38/5 khớp chữ. BẢN VÁ CÓ THỂ ĐẺ RA: không đổi dòng
thêm (sửa dòng PR đã thêm). HINT: hunk 1 (`@@ -12`). ĐÃ THỬ NGHIỆM HINT: áp sạch; compile `-W error` sạch. ĐỘ TIN: cao.

### TEN-CA-LECH-SPEC  [P4]  Ca khoá mang tên `t60`–`t63` thay vì `t52` của spec
TỆP/DÒNG: `ops/cong_cu_test.py:2825` (`t60_import_bash_nen_khong_in_gi_ra_stderr`), `:2881`, `:2906`, `:6268`; spec §2A, §6.3.
VẤN ĐỀ: người nghiệm thu theo spec tìm `t52` sẽ gặp `t52_gom_manh_phai_DO_…` của #668 (nay CÙNG tệp sau merge) — lệch tên giờ còn dễ
nhầm hơn trước merge. Quyết định chủ kho: khai ở PR, không đổi tên. VÁ Ở ĐÂU: thân PR/handoff. VÁ THẾ NÀO: khai ánh xạ `t52`(spec)→`t60`;
"ca khoá UTF-8" (§2C/§6.3 ii)→`t61`+`t62`; `t63` ca mới; nói rõ `t52`–`t54` trong tệp là của #668. CA KHOÁ: không áp dụng. BẢN VÁ CÓ
THỂ ĐẺ RA: không. HINT: không có hunk (ngoài mã). ĐÃ THỬ NGHIỆM HINT: không áp dụng. ĐỘ TIN: cao; thân PR KHÔNG ĐO ĐƯỢC.

## HINT.patch — tự kiểm

- Tệp: `out/HINT.patch` — 3 hunk, MỘT tệp `ops/cong_cu_test.py`, định dạng `git diff --no-prefix` (đường dẫn repo-relative, không
  `a/`/`b/`), đoạn đầu mang nhãn §8 nguyên văn ("chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit") và
  bảng phân loại hunk. Mọi hunk là tệp TEST thuần (§8 ràng buộc 3(a)): một cửa tự kiểm chỉ `t62` gọi + một chú thích; không chạm
  `bash_nen.py`, khối tự phóng lại, `main()`, `_main_gop()`, `.github/workflows/**`, hay hai đường CI gọi (không đối số · `--gop manh`).
  Mức: mã đầy đủ đã chạy trên bản sao tạm — KHÔNG phải mệnh lệnh; executor tự áp, tự đo, tự commit, và khai `hint_provenance`.
- Lệnh tự kiểm BẮT BUỘC (nguyên văn prompt, clone mới từ kho.git):
  ```
  $ git clone -q kho.git tam/ap && git -C tam/ap checkout -q --detach 8757a84 && cd tam/ap && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch
  checking file ops/cong_cu_test.py
  dry_run_rc=0
  $ patch -p0 --fuzz=0 < ../../out/HINT.patch                 ⇒ patching file ops/cong_cu_test.py · apply_rc=0 · 0 .orig/.rej
  $ cmp ops/cong_cu_test.py ../hint/ops/cong_cu_test.py        ⇒ trùng từng byte với bản đã chạy thử (sha256 72fe8798…)
  $ git diff --numstat fc852ff -- ops/                          ⇒ 1 1 ops/bash_nen.py · 296 41 ops/cong_cu_test.py ⇒ +297 (≤ 300)
  ```
  So head: +12/−8 (hunk 1 +2/−2 · hunk 2 +8/−0 · hunk 3 +2/−6); mọi dòng thêm ≤ 118 ký tự (max 114); compile `-W error` sạch.
- Trên bản áp (`tam/hint` ≡ `tam/ap`):
  - `t49 t52 t53 t54 t60 t61 t62 t63` ⇒ `TONG {"qua": 8}` × {python3.11, 3.12, 3.13} × {thường, `LC_ALL=C PYTHONUTF8=0
    PYTHONIOENCODING=ascii`} = 6/6 lượt; 0 `.pyc`.
  - `mot_db.py` (gọi `_do_mot`+`_ket_luan_ban_ghi` CỦA tệp): `f25_cua_moi_vi_tri` ⇒ `ok … bán kính 1/60` (head: ĐỎ tín dụng giả);
    `f13_dispatcher_nuot`, `f25_bo_chot_doi_so_la`, `f27_entry_drop`, `f27_entry_rc`, `f28_can_cau_hinh`, `f28_gate_di_tat`,
    `f28_du_nuot_ma`, `f28_nen_ma` ⇒ `ok … bán kính 1/60` (9/9).
  - 416 mỏ neo `DOT_BIEN`: số lần xuất hiện head = bản áp (0 mỏ neo đổi số đếm).
  - `tam/cu/dem_env.py` trên bản áp: 38 Call {Name 17, `{**os.environ}` 5, moi_truong 12, dict(os.environ) 3, dict(env) 1} = chữ mới.
  - Mảnh CI 5/8 trên bản áp (env CI `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 CONG_CU_TEST_MANH=5/8 CONG_CU_TEST_MANH_RA=manh/manh-5.txt`):
    **RC=0**, 52/52 `ok`, `f25_cua_moi_vi_tri … bán kính 1/60`, ghi tệp mảnh (head `8757a84`: RC=1 `[M-loi]`, không ghi tệp).

## KHÔNG ĐO ĐƯỢC

- **Mọi hành vi Windows** (chủ kho: "Chỉ chạy tại máy"; không `workflow_dispatch`): nghiệm thu §6.1–6.3 cho head; Git for Windows
  có nhận `xau_\xff`/`hong_\xff`/tên mang `\` trong INDEX không (spec §8) — `t63` (bo_ten/bo_hong) chỉ MÔ PHỎNG; `sys.orig_argv` qua
  `py`/venv launcher; mồ côi dưới TerminateProcess; thời lượng mảnh `gate-cong-cu` trên `windows-latest` (trần 30 phút) với
  `t60`–`t63`. Suy từ mã (không đo): nếu Git for Windows từ chối cả `\xff` thì `t63` ĐỎ ở `(ops/no_cu.py/rc)` như BAO_CAO §7 đã khai.
- **CI thật trên GitHub** (không gọi mạng/không chạy CI): kết luận "mảnh 5/8 đỏ ⇒ gom đỏ" là MÔ PHỎNG cục bộ đúng lệnh + env của
  `ci.yml` (`gate-cong-cu`/`gate-cong-cu-gop`), thiếu `jsonschema`/`shellcheck` so với runner (không ảnh hưởng `f25`: đích `t52`,
  ca đỏ `t62`). `gate-cong-cu-gop (ubuntu-latest)` đã vào ruleset bắt buộc chưa: KHÔNG ĐO ĐƯỢC.
- **Một lượt chạy tay KHÔNG đối số (du-mode) trọn vẹn trong MỘT tiến trình**: hai lượt (a)/(b) bị harness dừng ở trần 2 giờ của
  tác vụ nền (máy dùng chung với một phiên khác); phần đã in: vòng CA `59/59`, CỔNG TRÊN CÂY THẬT ĐẠT, TỰ KIỂM SONG SONG ĐẠT. Pha bán
  kính đo trọn qua 8 mảnh mỗi môi trường — cùng `_phong_con` → `_do_mot` → `_nhan_ket_qua_con` → `_ket_luan_ban_ghi` mà du-mode dùng
  (`t54` khoá dây nối `main()` ⇄ bán kính ở từng chế độ, `qua`). Dòng `SỐ LIỆU: … lỗi đột biến=N` của du-mode vì thế là SUY từ tổng các
  mảnh (= 2 ở (b): `t2_go_canary` môi trường + `f25` P1), không phải một dòng in thật.
- **Thân PR #690 / handoff vòng này** (không gọi mạng; commit cục bộ chưa đẩy): ánh xạ tên ca, `hint_provenance` theo hunk — người
  đẩy phải khai.
- **Pha bán kính của `c5f3da0`** (lời khai "lỗi đột biến 1"): không chạy lại — SHA trước merge; lượt này đo vòng CA của nó và trọn
  bộ của head `8757a84`.
- **Trọn bộ có `jsonschema`** (CI cài `jsonschema==4.26.0`): không cài, giữ cùng điều kiện executor/lượt 4 ⇒ `t2`/`t2_go_canary`
  KHÔNG ĐO ĐƯỢC ở mọi cây.
- **Model/effort thật của executor**: thân commit tự khai "Claude Opus 5.5"; BAO_CAO khai effort KHÔNG ĐO ĐƯỢC.
- **Thẩm quyền ghi của phiên tạo `c5f3da0`/`8757a84`**: trailer `Claude-Session: …session_014dEtdMqShJhdQ8JfNbEeLU` là phiên của
  lease g1 (đã bị g2 thay thế theo `LEASE-g2.yaml`); `LEASE-g2.yaml` ghi `environment: local` (máy Windows). Hiện vật lượt này
  không chứng minh theo chiều nào — chủ kho/người land xác nhận.
- **Sự cố trong lượt (khai trước)**: (1) 15:54:35Z lệnh khảo sát đầu tiên `git -C cay-kho status --short` (thiếu
  `--no-optional-locks`) đã GHI LẠI `cay-kho/.git/index` (làm mới stat-cache sau checkout 15:53:37Z); NỘI DUNG mục không đổi:
  sha256 của `git ls-files -s` (mode, oid, path) = sha256 của `ls-tree -r HEAD` = `2ca23d8bf20b0539…`, `diff --cached` rỗng. Từ đó mọi
  lệnh git trên `cay-kho` dùng `GIT_OPTIONAL_LOCKS=0`. (2) Không lệnh nào của lượt này chạy bộ ca trong `cay-kho`; mọi clone/đột
  biến/áp vá nằm trong `$R/tam/`. (3) `pip install --no-cache-dir --target tam/ruff ruff==0.15.15`: 0 tệp mới trong `~/.cache/pip`.

## SNAPSHOT ĐẦU/CUỐI (§8.2)

| đối tượng | đầu (15:54–15:56Z) | cuối | ghi chú |
|---|---|---|---|
| `cay-kho` HEAD / tree | `8757a8406489a306736c8257a7933546b8c81042` / `91d7c4dfd11a325a29df3a1e503f595b3bdaefab` | (điền cuối lượt) | — |
| `cay-kho` `status --porcelain --ignored`, `diff`, `diff --cached` | rỗng / rỗng / rỗng | (điền cuối lượt) | `GIT_OPTIONAL_LOCKS=0` |
| `cay-kho` mục index (sha256 `ls-files -s`) | `2ca23d8bf20b0539…` = cây HEAD | (điền cuối lượt) | mtime index 15:54:35Z — sự cố (1) |
| `kho.git` | refs sha256 `2200e58bfe1c7873…` | (điền cuối lượt) | — |
| `~/.gitconfig` | sha256 `75239ed3763a89e3…`, mtime 14:41:09Z | (điền cuối lượt) | — |

Giới hạn: snapshot chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên.
