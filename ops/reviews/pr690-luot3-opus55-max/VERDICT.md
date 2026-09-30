verdict: changes_requested
reviewed_sha: e46f5693461ee2ffffc8e58f13f5c37ea934791e
provider: claude
role: reviewer
model_reviewer_identity: claude-opus-5-5 (Opus 5.5 — tự khai; phiên điều phối đối chiếu modelUsage)
independent_from_executor_session: true
assurance: review_deferred
review_axes: [spec, standards_security]

> Ngưỡng đã áp: `review_class`/`effective_review_class: sensitive`, `assurance_target: human_audited` (LEASE). Lượt này
> CÙNG PROVIDER với executor (Claude review mã Claude viết) ⇒ nhãn tối đa `same_provider_approved`, và §8 nói rõ nhãn ấy
> KHÔNG thay mức assurance bắt buộc cho `sensitive`. Kết luận ở đây là `changes_requested`, nên `assurance: review_deferred`.
> Đếm theo LỚP: **P0=0 · P1=0 · P2=5 · P3=1 · P4=1**.
>
> Mọi số dưới đây do lượt này TỰ ĐO trong `$RV/tam/` (bản sao tạm), không chép báo cáo executor.
> Môi trường đo: container Linux, `python3.12` 3.12.3 (đo chính), 3.11.15 và 3.13.12 để so; git 2.43.0; KHÔNG có
> `jsonschema` (cùng điều kiện executor khai "lỗi đột biến 1 = nền (jsonschema)"). Không đặt `LANG` ⇒ CPython tự bật UTF-8
> mode. "Cha giải mã bằng locale không UTF-8" tái hiện bằng `LC_ALL=C PYTHONUTF8=0` (đo: `utf8_mode 0 loc ANSI_X3.4-1968`);
> chỉ `PYTHONUTF8=0` thì PEP 538 ép về C.UTF-8 (đo: `utf8_mode 0 loc UTF-8`) nên KHÔNG tái hiện được.
> Công cụ đo (đều trong `$RV/tam/`): `chay_ca.py` (nạp tệp bằng importlib, chạy ca qua `_chay_1_ca` CỦA CHÍNH tệp ⇒ nhãn
> `giet_that|tin_dung_gia|qua|bo_qua`), `bang_dot_bien.py` / `bang_dot_bien_sau_hint.py` (clone mới từ `cay-kho`, thay CHÍNH
> XÁC 1 lần, xoá `__pycache__`), `do_lap.py`, `do_mo_coi.py`, `do_tin_hieu.py`, `do_argv.py`, `dem_phong.py`, `truy_env.py`.
> Phiên có sẵn `PYTHONDONTWRITEBYTECODE=1` trong môi trường (đo: `env | grep PYTHON`).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 1 (codex `gpt-6-astra`, trên `75af95c`): 1 P1 / 3 P2 / 1 P3 / 1 P4. Commit mới sau lượt 1: chỉ `e46f569`
(`git diff --numstat 75af95c e46f569 -- ops/` ⇒ `31 1 ops/cong_cu_test.py`): thêm tự phóng lại, `t62`, cửa
`--tu-kiem-che-do-utf8`, sửa con trỏ `t60b`. `t49`/`t61`/`_ep_utf8` KHÔNG đổi.

| slug (lượt 1) | hạng lượt 1 | nhãn §8 lượt này | tóm tắt bằng chứng |
|---|---|---|---|
| UTF8-BO-SOT-BO-DOC | P1 | **ĐÃ VÁ THẬT cho đường `__main__`** · **VÁ SINH LỖI MỚI** (2 lớp mới) | trước: 4 ca `tin_dung_gia`; sau: trọn bộ dưới `LC_ALL=C PYTHONUTF8=0` không còn ca nào trong 4 ca ấy đỏ; đường importlib vẫn hỏng nhưng không có consumer |
| CA-KHOA-UTF8-THIEU-QUAN-SAT | P2 | **CHƯA VÁ** + biểu hiện mới (ĐỎ oan dưới `LC_ALL=C`) | 3 đột biến sống qua CẢ 56 ca; `t61` ĐỎ oan trong lượt trọn bộ `LC_ALL=C` |
| CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG | P2 | **CHƯA VÁ** | 4 đột biến sống qua CẢ 56 ca |
| NGHIEM-THU-WINDOWS-CON-THIEU | P2 | **CHƯA VÁ** (có MỘT số đo Windows trên `75af95c`, trước bản vá) | thiếu các mục §6 cho head + bước đo giả thuyết B |
| LOI-KHAI-RONG-HON-PHEP-DO | P3 | **CHƯA VÁ** + 2 biểu hiện mới do `e46f569` | "66" vẫn ở `:15`, không tái lập; hai câu mới khai rộng hơn phép đo |
| CON-TRO-CA-CU | P4 | **ĐÃ VÁ THẬT** | `t60b` 0 lần ở head, 1 lần ở `75af95c` |

### UTF8-BO-SOT-BO-DOC (P1) — đo lại: ĐÃ VÁ THẬT cho đường chạy bộ ca; bản vá sinh lớp mới

(a) TRƯỚC — `75af95c`, cha dưới locale ASCII, nạp bằng importlib rồi chạy đúng 4 ca Windows khai đỏ:
```
$ cd tam/c75 && env LC_ALL=C PYTHONUTF8=0 PYTHONDONTWRITEBYTECODE=1 python3.12 tam/chay_ca.py ops/cong_cu_test.py t29 t39 t42 t45
CA ["t29_ban_kinh_qua_RONG_phai_neu_LY_DO_tung_ca_oan", "tin_dung_gia", "UnicodeDecodeError: 'ascii' codec can't decode byte 0xc4 in position 8: ordinal not in range(128)", 0.3]
CA ["t45_bo_ca_phai_CHAY_cong_tren_cay_THAT_chu_khong_chi_cay_gia", "tin_dung_gia", "UnicodeDecodeError: 'ascii' codec can't decode byte 0xe1 ...", 0.4]
CA ["t42_ca_do_o_NEN_bi_loai_khoi_ban_kinh_va_van_keo_ma_thoat", "tin_dung_gia", "UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 ...", 0.3]
CA ["t39_chi_CA_PHAN_QUYET_duoc_chot_tren_rc_va_trang_thai", "tin_dung_gia", "UnicodeDecodeError: 'ascii' codec can't decode byte 0xe1 ...", 0.6]
```
⇒ tái hiện trên Linux đúng tập `t29/t39/t42/t45` mà `e46f569` khai đo được trên Windows cp1258 (lượt 1 nêu 3 ca; `t39` là
biểu hiện thứ 4 cùng cơ chế).

(b) SAU — `e46f569`, đường `__main__` (thứ CI và nghiệm thu gọi): tiến trình chạy bộ ca ở UTF-8 mode, đúng MỘT lần phóng lại:
```
$ env LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii python3.12 ops/cong_cu_test.py --tu-kiem-che-do-utf8   ⇒ UTF8_MODE=1  rc=0
$ strace -f -e trace=execve ... (4 dạng gọi)  ⇒ đúng 2 execve mỗi dạng:
   ["python3.12","ops/cong_cu_test.py",...]        → ["/usr/bin/python3.12","-X","utf8","ops/cong_cu_test.py",...]
   ["python3.12","-X","utf8=0",...]                → [..., "-X","utf8","-X","utf8=0", ...]   (-X utf8 ĐẦU TIÊN thắng, đo 3.11/3.12/3.13)
   ["python3.12","-I","-X","utf8=0",...]           → [..., "-X","utf8","-I","-X","utf8=0", ...]
   ["python3.12","-m","ops.cong_cu_test",...]      → [..., "-X","utf8","-m","ops.cong_cu_test", ...]
```
Trọn bộ end-to-end, head, `env LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii ... python3.12 ops/cong_cu_test.py`
(`tam/log-full-head-ascii.txt`): `cong_cu_test: 54/55 đạt; tổng=56, bỏ qua=1` — `t29/t39/t42/t45` KHÔNG đỏ; ca đỏ duy nhất là
`t61` vì một cơ chế KHÁC (xem CA-KHOA-UTF8-THIEU-QUAN-SAT, biểu hiện 5). Dòng `SỐ LIỆU`/`RC`: xem BẢNG ĐO.

(c) Đường KHÔNG qua `__main__` — nạp bằng importlib:
```
$ cd tam/h1 && env LC_ALL=C PYTHONUTF8=0 python3.12 tam/chay_ca.py ops/cong_cu_test.py t29 t39 t42 t45
t29 tin_dung_gia UnicodeDecodeError: 'ascii' ... | t45 tin_dung_gia ... | t42 tin_dung_gia ... | t39 tin_dung_gia ...
```
⇒ cơ chế gốc CÒN NGUYÊN ở đường này (bản vá chủ đích chỉ ở `__main__`, chú thích `:36` nói rõ). `git grep -n cong_cu_test`
trên head: consumer chạy ca duy nhất là `ci.yml:113 python ops/cong_cu_test.py`; `.claude/dev/ci_dang_ky_test.py:1734` chỉ liệt
kê chuỗi `python -m ops.cong_cu_test`/`cd ops && python cong_cu_test.py` (đều `__main__`; đã đo `-m`). Không consumer nào chạy
ca qua import ⇒ không tính biểu hiện mở; ghi giới hạn: một bộ chạy-ca-qua-import sau này (vd chế độ mảnh/gom của #668) sẽ gặp
lại. Con của bộ ca (`--ban-kinh-con`, `--tu-kiem-*`) chạy làm `__main__` và thừa kế `PYTHONUTF8=1` từ `_ep_utf8()` ⇒ không
phóng lại, đã ở UTF-8 (`TỰ KIỂM SONG SONG (N126): ĐẠT` trong cả ba lượt trọn bộ).

(d) Bản vá SINH hai lớp mới: `TU-PHONG-LAI-KHONG-TRONG-SUOT` (stdin ⇒ rc=0 rỗng; giết tiến trình bao ⇒ bộ ca mồ côi) và
`TU-PHONG-LAI-CHI-KHOA-CO-UTF8` (`t62` chỉ khoá CỜ; mã thoát, chống lặp, chốt `__main__` không ca nào khoá).

### CA-KHOA-UTF8-THIEU-QUAN-SAT (P2) — CHƯA VÁ, thêm biểu hiện
`t61` không đổi từ `75af95c`; `t62` mới không bắt thêm gì: `M61c` (chỉ reconfigure stdout) · `M61d` (bỏ `PYTHONUTF8`) ·
`M61e` (cháu `ascii:backslashreplace`) ⇒ cả ba `KHONG_QUA=0` trên 56 ca. Nhánh luồng thiếu `reconfigure` vẫn không có đối chứng.
Biểu hiện MỚI (5): dưới `LC_ALL=C` `t61` ĐỎ oan — chi tiết ở finding.
```
$ cd tam && TAT_CA=1 python3.12 bang_dot_bien.py M61c_chi_stdout M61d_bo_PYTHONUTF8 M61e_chau_escape   (trích tam/bang_dot_bien_tatca.out)
### M61c_chi_stdout ...    TAT_CA: 56 ca, qua=55, bo_qua=1, KHONG_QUA=0
### M61d_bo_PYTHONUTF8 ...  TAT_CA: 56 ca, qua=55, bo_qua=1, KHONG_QUA=0
### M61e_chau_escape ...    TAT_CA: 56 ca, qua=55, bo_qua=1, KHONG_QUA=0
```

### CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG (P2) — CHƯA VÁ
`_stage_byte` và chốt `ga` không đổi. `M49a` (bỏ `oid.returncode`) · `M49b` (bỏ `r.returncode`) · `M49c` (bỏ `not co`) ·
`M49d` (bỏ `ga.returncode`) ⇒ cả bốn `KHONG_QUA=0` trên 56 ca.
```
$ cd tam && TAT_CA=1 python3.12 bang_dot_bien.py M49a_bo_oid_rc M49b_bo_update_index_rc M49c_bo_ls_files_co M49d_bo_git_add_rc
### M49a_bo_oid_rc ...           TAT_CA: 56 ca, qua=55, bo_qua=1, KHONG_QUA=0
### M49b_bo_update_index_rc ...  TAT_CA: 56 ca, qua=55, bo_qua=1, KHONG_QUA=0
### M49c_bo_ls_files_co ...      TAT_CA: 56 ca, qua=55, bo_qua=1, KHONG_QUA=0
### M49d_bo_git_add_rc ...       TAT_CA: 56 ca, qua=55, bo_qua=1, KHONG_QUA=0
```

### NGHIEM-THU-WINDOWS-CON-THIEU (P2) — CHƯA VÁ
Bằng chứng Windows DUY NHẤT trong hiện vật: thân commit `e46f569` — *"Nghiem thu Windows local (Python 3.13.1, Git for
Windows 2.55.0, locale cp1258) tren 75af95c: ... t29/t39/t42/t45 DO, 47/51"*. Đó là số đo TRÊN `75af95c` (trước bản vá), và
nó ĐỎ. Đối chiếu §6: (1) `N/N` trên Windows cho head — **không có**; số `bỏ qua` và lý do từng cái — **không có** (47/51 với
tổng 55 ⇒ 4 bỏ qua trên Windows, Linux chỉ 1–2; không nói ca nào); delta lỗi đột biến so NỀN cùng máy — **không có**; (2) lượt
ép ASCII cho con trên Windows — **không có**; (3) đột biến (i)/(ii) trên Windows — **không có** ("co rang tren moi nen" không kèm
số Windows); (4) ruff — đo được trên Linux (BẢNG ĐO); §2B "BƯỚC ĐẦU trên Windows: ĐO giả thuyết B TRƯỚC khi vá (in `rc`/stderr
của `git add -A` và `ls-files -z`)" — **không có**. Lượt này là Linux: KHÔNG ĐO ĐƯỢC thay.

### LOI-KHAI-RONG-HON-PHEP-DO (P3) — CHƯA VÁ, thêm biểu hiện
`ops/cong_cu_test.py:15` vẫn "đo bằng AST có 66 điểm phóng", `:16` vẫn "kể cả điểm phóng chưa ai viết". Biểu hiện MỚI của
`e46f569`: `:36` *"`-X utf8` bật cờ bất kể môi trường ⇒ không lặp. `t62` khoá."* (t62 không khoá chống lặp: `M62b` sống) và
`:35` *"`t61` NẠP tệp này bằng importlib, và nạp thì không được phóng gì"* (`M62e` sống qua `t61`). Số đo ở BẢNG ĐO.

### CON-TRO-CA-CU (P4) — ĐÃ VÁ THẬT
`grep -n t60b` ⇒ `75af95c:17` có, head 0 dòng; `:17` head trỏ `t61`, và `t61_ep_UTF8_phai_co_RANG_...` tồn tại (`:2268`).

## BẢNG LỚP

| slug lớp | finding/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| UTF8-BO-SOT-BO-DOC | 4 ca đọc `text=True` của con Python (t29/t39/t42/t45) | — (đóng cho `__main__`) | lượt 1 `75af95c` → đóng ở `e46f569` | tự phóng lại `-X utf8` ở `__main__` | trước/sau ở trên; importlib: KHÔNG consumer (ghi giới hạn) |
| CA-KHOA-UTF8-THIEU-QUAN-SAT | (1) stderr không đo · (2) `PYTHONUTF8`/mode của cháu · (3) byte của cháu · (4) nhánh thiếu `reconfigure` · (5) MỚI: argv `-c` có chữ Việt ⇒ ĐỎ oan dưới `LC_ALL=C`, `bang` (a) quy nhầm | **P2** | lượt 1 `75af95c` (1–4); lượt 2 `e46f569` (5) | MỘT gốc: `t61` suy từ MÃ THOÁT. Vá chung: đo BYTE + tách giàn giáo (`dung` `NAP_OK`) + argv ASCII | Hunk 3; `M61c/d/e/f` chết đúng nhãn; `t61` xanh dưới `LC_ALL=C` (3.11/3.12/3.13) |
| CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG | 4 chốt `rc`/`co`/`ga` không răng | **P2** | lượt 1 `75af95c`; không đổi ở `e46f569` | dời helper ra cấp module + ca bơm lỗi từng bước | Hunk 4–6; `t63`; `H_M49a–e` chết |
| NGHIEM-THU-WINDOWS-CON-THIEU | thiếu §6.1–6.3 cho head, thiếu đo giả thuyết B, thiếu danh sách bỏ qua | **P2** | lượt 1; lượt 2 thấy 1 số đo trên `75af95c` | chạy checklist §6 trên Windows local neo `e46f569` (hoặc head mới) | KHÔNG ĐO ĐƯỢC ở Linux |
| TU-PHONG-LAI-CHI-KHOA-CO-UTF8 | MỚI: `M62f` nuốt mã thoát · `M62b` bỏ `-X utf8` (lặp vô hạn) · `M62e` bỏ chốt `__main__` — sống 56/56 | **P2** | lượt 2 `e46f569` | thêm chốt: mã thoát (cửa rc=7), `-X utf8=0`, biến chặn lần 2, (e) ở `t61` | Hunk 2/3/4/7; `H_M62b/e/f`, `H_Mg1` chết |
| TU-PHONG-LAI-KHONG-TRONG-SUOT | MỚI: (a) `python - < tệp` ⇒ rc=0, 0 byte (P2) · (b) giết tiến trình bao ⇒ bộ ca mồ côi (P3) · (c) chết vì tín hiệu ⇒ rc 247/241 thay vì tín hiệu (P4) | **P2** | lượt 2 `e46f569` | (a) từ chối nguồn không đọc lại được; (b) POSIX `os.execve` / Windows Job Object — gợi ý hướng; (c) chấp nhận, ghi chú | Hunk 2+4 (`t64` (4)); (b)(c) chỉ mô tả |
| LOI-KHAI-RONG-HON-PHEP-DO | "66" `:15`; "kể cả điểm phóng chưa ai viết" `:16`; MỚI `:35`, `:36` | **P3** | lượt 1 + lượt 2 | viết lại câu theo số đo + công thức | Hunk 1–2 |
| TEN-CA-LECH-SPEC | MỚI: spec §2A/§6.3 gọi `t52_import_bash_nen_khong_in_gi_ra_stderr`; PR đặt `t60_…`, commit không khai lệch | **P4** | lượt 2 | khai lệch trong PR/handoff (hoặc đổi tên) | `grep` |
| CON-TRO-CA-CU | `t60b` | — (đóng) | lượt 1 | — | grep |

Số lớp còn mở: 7 (P2×5, P3×1, P4×1). Số biểu hiện còn mở: 5 (UTF8-QUAN-SAT) + 4 (STAGING) + 3 (WINDOWS: §6 cho head,
giả thuyết B, danh sách bỏ qua) + 3 (CHI-KHOA) + 3 (KHONG-TRONG-SUOT) + 4 (LOI-KHAI) + 1 (TEN-CA) = **23**.

## BẢNG SĂN

```
HƯỚNG 1: mã thoát của lệnh tự phóng lại khi CON chết vì tín hiệu / Ctrl-C
  giả thuyết : nếu con (bản `-X utf8`) chết vì SIGKILL/SIGTERM thì tiến trình bao có thể trả 0 ⇒ cổng nói dối
  lệnh       : python3.12 tam/do_tin_hieu.py tam/mo_coi   (Popen bộ ca, 4s sau gửi tín hiệu tới con / chính nó / cả nhóm)
  output     : PYTHONUTF8=0 gui SIGKILL toi con: rc tien trinh bao=247; con lai trong session=0
               PYTHONUTF8=0 gui SIGTERM toi con: rc tien trinh bao=241
               PYTHONUTF8=1 gui SIGKILL toi chinh_no: rc=-9 ;  SIGTERM: rc=-15
               PYTHONUTF8=0 gui SIGINT toi ca_nhom: rc=-2 (KeyboardInterrupt), con lai=0 ; PYTHONUTF8=1: rc=-2
  kết luận   : KHÔNG PHẢI LỖI (fail-close giữ: không bao giờ 0). Ghi biểu hiện P4: "chết vì tín hiệu N" thành "thoát 256−N".

HƯỚNG 2: tiến trình con mồ côi khi bộ điều phối giết tiến trình bao
  giả thuyết : nếu người gọi `subprocess.run(..., timeout=)` (kill() đúng MỘT tiến trình) thì bản phóng lại chạy tiếp
  lệnh       : python3.12 tam/do_mo_coi.py tam/mo_coi {1,0}   (timeout 8s, đếm tiến trình còn sống sau 3s)
  output     : PYTHONUTF8=1: het han sau 8.0s ... con song sau 3s: 0
               PYTHONUTF8=0: het han sau 8.0s ... con song sau 3s: 1
                   (8245, 'S', '/usr/bin/python3.12 -X utf8 ops/cong_cu_test.py ')
  kết luận   : LỖI (P3, biểu hiện (b) của TU-PHONG-LAI-KHONG-TRONG-SUOT). Trên Windows nhánh này là MẶC ĐỊNH (không
               PYTHONUTF8) và TerminateProcess/Stop-Process chỉ giết một tiến trình — KHÔNG ĐO ĐƯỢC ở đây, suy từ cơ chế.

HƯỚNG 3: lặp phóng vô hạn
  giả thuyết : nếu một dạng gọi giữ utf8_mode=0 sau khi phóng lại thì chuỗi phóng không dừng
  lệnh       : strace -f -e trace=execve python3.12 {-X utf8=0|-I -X utf8=0|-E -X utf8=0 -B -u} ops/cong_cu_test.py --tu-kiem-che-do-utf8
               python3.12 tam/do_lap.py <cây> 6 python3.12 -I -X utf8=0 ops/cong_cu_test.py --tu-kiem-che-do-utf8
  output     : head: đúng 2 execve mỗi dạng, UTF8_MODE=1 rc=0;  do_lap head: "so tien trinh trong session moi giay: [0]"
               M62b (bỏ "-X","utf8") + `-I -X utf8=0`: "rc_top= None so tien trinh trong session moi giay: [11, 19, 28, 35, 44, 53]"
               M62b + `-X utf8=0` (không -I, PYTHONUTF8=0): "[11, 18, 26, 34, 42, 50]"
               M62b + PYTHONUTF8=0 không -I (đúng thứ t62 gọi): [0], rc 0  ⇒ t62 không phân biệt được
  kết luận   : head KHÔNG lặp (KHÔNG PHẢI LỖI); nhưng thứ duy nhất chống lặp là token `-X utf8` và KHÔNG ca nào khoá nó
               ⇒ LỖI thuộc TU-PHONG-LAI-CHI-KHOA-CO-UTF8.

HƯỚNG 4: `sys.orig_argv` phát lại các dạng gọi (`-m`, đường dẫn có dấu cách + chữ Việt, cwd khác)
  giả thuyết : nếu phát lại argv sai thì con chạy thứ khác / hỏng
  lệnh       : cd / && env LC_ALL=C PYTHONUTF8=0 strace ... python3.12 "tam/có dấu cách/kho/ops/cong_cu_test.py" --tu-kiem-che-do-utf8
               env LC_ALL=C PYTHONUTF8=0 python3.12 -m ops.cong_cu_test --tu-kiem-che-do-utf8
  output     : execve("/usr/bin/python3.12", ["/usr/bin/python3.12", "-X", "utf8", "/tmp/.../có dấu cách/kho/ops/cong_cu_test.py", ...]) ⇒ UTF8_MODE=1
               -m: UTF8_MODE=1 rc=0
  kết luận   : KHÔNG PHẢI LỖI.

HƯỚNG 5: nguồn không phát lại được — stdin `-`
  giả thuyết : nếu chương trình đọc từ stdin thì bản phóng lại đọc stdin đã cạn, chạy RỖNG, rc=0
  lệnh       : cd tam/h1/ops && env LC_ALL=C.UTF-8 PYTHONUTF8=0 python3.12 - < cong_cu_test.py        (TOÀN BỘ bộ ca)
               cd tam/h1/ops && env ... PYTHONUTF8={1,0} python3.12 - --tu-kiem-cong-that /khong/ton/tai < cong_cu_test.py
               cd tam/n1/ops (NỀN 89fc4fa) && env LC_ALL=C.UTF-8 PYTHONUTF8=0 timeout 25 python3.12 - < cong_cu_test.py
  output     : head: "rc=0 thoi_gian=0.26s stdout_bytes=0 stderr_khac_SyntaxWarning=0"
               head, cửa lỗi: PYTHONUTF8=1 ⇒ rc=9 "KQ [1, ["CỔNG TRÊN CÂY THẬT: KHÔNG_ĐO_ĐƯỢC (rc=3)" ...";  PYTHONUTF8=0 ⇒ rc=0 (rỗng)
               NỀN: chạy thật — "cong_cu_test: 52/52 đạt; tổng=53, bỏ qua=1" trong 25 giây đầu (bị cắt ở pha bán kính)
  kết luận   : LỖI (P2) — đúng hình dạng "rc=0 + output rỗng" CLAUDE.md r244; hồi quy so nền (nền chạy thật).

HƯỚNG 6: `_ep_utf8` đổi `os.environ` có làm câm ca CỐ Ý đo môi trường không
  giả thuyết : nếu có ca dựa vào môi trường THỪA HƯỞNG để đo mã hoá của sản phẩm thì việc ghi đè làm nó câm
  lệnh       : grep -n "PYTHONIOENCODING\|PYTHONUTF8\|cp1252\|cp1258\|locale\.\|LC_ALL" ops/cong_cu_test.py ; grep reconfigure ops/cong_cu.py ops/bash_nen.py
               python3.12 tam/truy_env.py ops/cong_cu_test.py
  output     : chỉ t61 (:2281) và t62 (:2299) đặt biến mã hoá, đều ghi đè TƯỜNG MINH sau os.environ; cong_cu.py/bash_nen.py: 0 dòng
               35 env=: 12 moi_truong(), 5 dict(os.environ,…), 17 biến truy về moi_truong/dict(os.environ)/tham số, 1 env1←bk_don←moi_truong
  kết luận   : KHÔNG PHẢI LỖI (spec §2C(b) bắt buộc). Giới hạn parity: từ nay mọi con `cong_cu.py` trong bộ ca chạy UTF-8 mode kể
               cả trên Windows, nên bộ ca KHÔNG đo `cong_cu.py` dưới cp1258 — trước đây cũng chưa ca nào đo điều ấy.

HƯỚNG 7: `reconfigure(errors="backslashreplace")` có che lỗi một ca cần thấy không
  giả thuyết : nếu một ca dựa vào việc bộ ca CRASH khi in surrogate lạc thì backslashreplace làm nó xanh oan
  lệnh       : env PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python3.12 -c "<nạp tệp>; print('ops/xau_\udcff.py')"  (nền vs head)
  output     : nền: UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff' ... rc=1
               head: stdout.errors = backslashreplace / ops/xau_\udcff.py / SONG  rc=0
  kết luận   : KHÔNG PHẢI LỖI — chỉ dòng BÁO CÁO của chính bộ ca đổi; ca đỏ vẫn kéo mã thoát ≠0 (`hong` không rỗng); dữ liệu
               giữa tiến trình (BKCON) đi `ensure_ascii=True`, không qua đường này.

HƯỚNG 8: chốt (2) của `t60` có bị `.pyc`/cache/biến cảnh báo làm câm không
  giả thuyết : nếu `.pyc` cũ hay `PYTHONWARNINGS=ignore` tắt được cảnh báo thì chốt (2) câm
  lệnh       : M60b (chỉ còn chốt 2) với PYTHONWARNINGS=ignore / PYTHONPYCACHEPREFIX=... / .pyc cũ ở ops/__pycache__
               M60d = M60b + nạp từ THƯ MỤC THẬT (bỏ bản sao) + .pyc biên dịch từ chính nguồn hỏng
  output     : M60b: cả 3 biến thể "giet_that (2) import bash_nen rc=0, stderr không rỗng: ...SyntaxWarning..."
               M60d không .pyc: giet_that ;  M60d có .pyc (bash_nen.cpython-312.pyc): "qua"
  kết luận   : KHÔNG PHẢI LỖI — bẫy `.pyc` là THẬT (M60d câm), và bản sao tạm của `t60` là chốt chịu lực (lời khai executor đúng).

HƯỚNG 9: `t62` đo tiến trình CHẠY BỘ CA hay chỉ đo cửa ra
  giả thuyết : nếu cửa `--tu-kiem-che-do-utf8` chạy ở tiến trình khác `main()` thì t62 xanh mà bộ ca vẫn ngoài UTF-8
  lệnh       : đọc mã `:39-40` (phóng lại ở cấp module, trước `import yaml`) và `:6841-6844` (cửa trong khối `__main__`, cùng
               chỗ gọi `main()`); đột biến M62a
  output     : M62a ⇒ t62 giet_that 'UTF8_MODE=0' (3.11/3.12/3.13)
  kết luận   : KHÔNG PHẢI LỖI — cửa và `main()` cùng tiến trình theo cấu trúc mã; giới hạn: suy theo VỊ TRÍ mã, `main()` không tự in cờ.

HƯỚNG 10: số ca / bán kính đột biến đổi ngoài ý muốn
  giả thuyết : nếu ca mới rơi vào bán kính đột biến cũ thì "giết THÊM" / lỗi đột biến tăng
  lệnh       : python3.12 ops/cong_cu_test.py (tam/full-head, trọn bộ) ; AST đếm @ca và DOT_BIEN
  output     : "cong_cu_test: 55/55 đạt; tổng=56, bỏ qua=1" · "SỐ LIỆU: ca=56 · đột biến=212 · lỗi đột biến=1" · 0 dòng "giết THÊM";
               lỗi duy nhất: "KHÔNG_ĐO_ĐƯỢC t2_go_canary ... thiếu công cụ bắt buộc ['jsonschema']" ; nền: 53 ca, 212 đột biến
  kết luận   : KHÔNG PHẢI LỖI. Ghi chú: t60/t61/t62 không có mục DOT_BIEN (nền đã có 8 ca như vậy, head 11) — spec chỉ đòi đột biến tay.

HƯỚNG 11: môi trường ASCII THẬT trên Linux (`LC_ALL=C`) end-to-end
  giả thuyết : nếu bộ ca còn phụ thuộc locale ở chỗ khác ngoài 4 ca đã vá thì lượt trọn bộ dưới LC_ALL=C vẫn ĐỎ
  lệnh       : env LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii python3.12 ops/cong_cu_test.py   (tam/full-head)
               env LC_ALL=C PYTHONUTF8=0 python3.12 -c "print('chữ')"  ;  tam/do_argv.py
  output     : "ĐỎ  t61_ep_UTF8_...: (a) tiến trình nạp cong_cu_test.py dưới ASCII không in được chữ Việt: rc=1 "Unable to decode the
               command from the command line:\nUnicodeEncodeError: 'utf-8' codec can't encode characters in position 193-195: surrogates not allowed""
               "cong_cu_test: 54/55 đạt; tổng=56" ; tối thiểu: rc=1 cùng thông điệp ; mã `-c` thuần ASCII (\u…): rc=0 in đúng chữ
  kết luận   : LỖI (P2, biểu hiện 5 của CA-KHOA-UTF8-THIEU-QUAN-SAT) — ĐỎ oan, và `bang` (a) quy nhầm lỗi giàn giáo thành lỗi nghiệp vụ.

HƯỚNG 12: `_stage_byte` với tên mang `\` (va_\\xff) trên Git có `core.protectNTFS`
  giả thuyết : nếu Git for Windows từ chối `\` trong INDEX thì t49 BỎ QUA toàn ca, kể cả chốt (3) NGÀY GỠ không liên quan tên
  lệnh       : printf '100644 %s\tops/va_\\xff.py\0' $oid | git -c core.protectNTFS=true update-index --add -z --index-info
  output     : Linux git 2.43: "protectNTFS=true update-index rc=0" (và =false rc=0; byte 0xff rc=0)
  kết luận   : KHÔNG ĐO ĐƯỢC (kiểm `\` của verify_path chỉ biên dịch trên Windows). Nếu đúng, (2d) ném BoQuaMoiTruong
               TRƯỚC (3) ⇒ trên Windows t49 không đo chốt nào — 4 bỏ qua trong "47/51" khớp giả thuyết này; cần danh sách bỏ qua.
```

## BẢNG ĐỘT BIẾN

Mỗi đột biến: clone mới `cay-kho` → `tam/mut/<tên>` (sau HINT: `tam/mutH/<tên>`), thay chính xác 1 lần (assert đếm = 1),
xoá `__pycache__`, `PYTHONDONTWRITEBYTECODE=1`, chạy bằng `tam/chay_ca.py` (phân hạng bằng `_chay_1_ca` CỦA CHÍNH TỆP ⇒
`giet_that` chỉ khi `TinHieuChotCa` mang đúng tên ca). Cột "56 ca": chạy LẠI toàn bộ `CA` trên cùng bản sao (`TAT_CA=1`).
Đối chứng không đột biến: 56 ca ⇒ `qua=55, bo_qua=1` (`t2`, thiếu `jsonschema`).

### Trên head `e46f569`

| đột biến | ca đích | kết quả ca đích (3.12) | 56 ca | phân loại |
|---|---|---|---|---|
| M60a `bash_nen.py` `r"""`→`"""` (spec §6.3(i)) | t60 | `giet_that` "(1) ... SyntaxError: invalid escape sequence '\('" | 1/55 (chỉ t60) | giết thật; bán kính 1/N ✔ |
| M60b = M60a + gỡ chốt (1) (`simplefilter("ignore")`) | t60 | `giet_that` "(2) import bash_nen rc=0, stderr không rỗng: ...SyntaxWarning..." | — | chốt (2) có răng riêng ✔ |
| M60c = M60a + gỡ chốt (2) (`-W ignore`) | t60 | `giet_that` "(1) ..." | — | chốt (1) có răng riêng ✔ |
| M60d = M60b + nạp từ thư mục thật + `.pyc` cũ | t60 | `qua` | — | đối chứng bẫy `.pyc`: bản sao là chốt chịu lực |
| M61a gỡ `reconfigure` | t61 | `giet_that` "(a) ... rc=1 ... UnicodeEncodeError" | 1/55 | giết thật ✔ |
| M61b gỡ env cho con (spec §6.3(ii)) | t61 | `giet_that` "(b) ... rc=7" | 1/55 (chỉ t61) | giết thật; bán kính 1/N ✔ (Linux) |
| M62a gỡ tự phóng lại | t62 | `giet_that` "'UTF8_MODE=0'" | 1/55 | giết thật ✔ |
| M61c chỉ reconfigure stdout | t61 | `qua` | 0 | **SỐNG SÓT** (lượt 1, chưa vá) |
| M61d bỏ `PYTHONUTF8` khỏi `_BIEN_UTF8` | t61, t62 | `qua`, `qua` | 0 | **SỐNG SÓT** (lượt 1, chưa vá) |
| M61e `PYTHONIOENCODING=ascii:backslashreplace` cho con | t61, t62 | `qua`, `qua` | 0 | **SỐNG SÓT** (lượt 1, chưa vá) |
| M62b bỏ `"-X", "utf8"` | t62 | `qua` | 0 | **SỐNG SÓT** — và lặp vô hạn khi gọi `-X utf8=0` / `-I -X utf8=0` (HƯỚNG 3) |
| M62e bỏ chốt `__name__ == "__main__"` | t61, t62 | `qua`, `qua` | 0 | **SỐNG SÓT** |
| M62f nuốt mã thoát (`subprocess.run(...); sys.exit(0)`) | t62 | `qua` | 0 | **SỐNG SÓT** — trên Windows (nhánh mặc định) cổng luôn rc=0 |
| M49a bỏ `oid.returncode` | t49 | `qua` | 0 | **SỐNG SÓT** (lượt 1, chưa vá) |
| M49b bỏ `r.returncode` | t49 | `qua` | 0 | **SỐNG SÓT** (lượt 1, chưa vá) |
| M49c bỏ `not co` | t49 | `qua` | 0 | **SỐNG SÓT** (lượt 1, chưa vá) |
| M49d bỏ `ga.returncode` | t49 | `qua` | 0 | **SỐNG SÓT** (lượt 1, chưa vá) |

Chéo phiên bản: M60a/M61a/M61b/M62a với `python3.11` và `python3.13` ⇒ cùng ca, cùng `giet_that`, cùng thông điệp (3.13 báo
dòng 900). Head không đột biến: `t49 t60 t61 t62` `qua` trên 3.11/3.12/3.13. Không có `tin_dung_gia` nào trong bảng.
`t60`/`t61`/`t62` KHÔNG có mục nào trong `DOT_BIEN` (212 mục, không đổi so nền) — spec §6.3 chỉ đòi đột biến tay.

### Trên head + `out/HINT.patch` (bằng chứng hint có răng — `tam/bang_dot_bien_sau_hint.out`)

| đột biến | ca đích | kết quả (3.12) |
|---|---|---|
| H_M60a docstring | t60 | `giet_that` "(1) ..." |
| H_M61a gỡ reconfigure | t61 | `giet_that` "(a) ... rc=1" |
| H_M61b gỡ env con | t61 | `giet_that` "(b) ... rc=7" |
| H_M61c chỉ stdout | t61 | `giet_that` "(c) stderr ... không mang chữ Việt UTF-8 THẬT" |
| H_M61d bỏ PYTHONUTF8 | t61 | `giet_that` "(d) ... đo được [0, '0', 'utf-8']" |
| H_M61e cháu escape | t61 | `giet_that` "(b') cháu in chữ Việt đã bị THOÁT ... '(b) ch\\u1eef Vi\\u1ec7t'" |
| H_M61f bỏ `hasattr` | t61 | `giet_that` "(f) ... 'AttributeError'" |
| H_M62a gỡ phóng lại | t62, t64 | `giet_that` 'UTF8_MODE=0' ; `giet_that` "(1) ... 'UTF8_MODE=0'" |
| H_M62b bỏ `-X utf8` | t64 | `giet_that` "(2) gọi `-X utf8=0` ... mà không vào UTF-8 sau ĐÚNG một lần phóng" (rc=3, không lặp) ; t62 `qua` |
| H_M62e bỏ chốt `__main__` | t61 | `giet_that` "(e) NẠP cong_cu_test.py bằng importlib ... TỰ PHÓNG LẠI" |
| H_M62f nuốt mã thoát | t64 | `giet_that` "(1) ... rc=0 (chờ 7) 'UTF8_MODE=1'" |
| H_Mg1 bỏ chặn lần 2 | t64 | `giet_that` "(3) ... rc=0 'UTF8_MODE=1'" |
| H_Mg2 bỏ chặn stdin | t64 | `giet_that` "(4) nguồn đọc từ stdin: rc=0 mà KHÔNG chạy gì (stdout 0 ký tự)" |
| H_M49a/b/c/d | t63 | `giet_that` "(oid) … 'rc=128/0'", "(idx) … 'rc=0/128'", "(ls) … 'rc=0/0'", "(add) …" |
| H_M49e luôn ném | t63, t49 | `giet_that` "(0) đối chứng ... chốt ném bừa" ; t49 `bo_qua` (đúng: không đỏ oan) |

Bán kính (58 ca, `TAT_CA=1`, `tam/bang_dot_bien_sau_hint_tatca.out`): H_M62b, H_M62f, H_Mg2, H_M61d, H_M49a, H_M62e ⇒ mỗi cái
`KHONG_QUA=1` (đúng ca đích) trên 57 ca chạy được; bản áp không đột biến ⇒ `qua=57, bo_qua=1`.
Lưu ý đo: `t64` (2) lúc đầu gọi `-I -X utf8=0`; đổi sang `-X utf8=0` vì `-I` bỏ user-site ⇒ máy cài PyYAML bằng `--user` sẽ
ĐỎ oan. Đo lại: head `e46f569` + M62b + `python3.12 -X utf8=0 ops/cong_cu_test.py --tu-kiem-che-do-utf8` (không `-I`) ⇒
`[11, 18, 26, 34, 42, 50]` tiến trình sau 1..6 giây — vòng lặp chỉ cần `-X utf8=0`; head + HINT + H_M62b ⇒ rc=3, một dòng từ chối.

## BẢNG ĐO

| khẳng định | PR/commit khai | đo được | khớp? |
|---|---|---|---|
| số đạt (f43aa1e: "UTF-8 54/54") | 54/54 | head `e46f569` trọn bộ: `55/55 đạt; tổng=56, bỏ qua=1` (`t2`, thiếu jsonschema) | số của `f43aa1e` (55 ca − 1); **không còn là số của head** |
| "55 ca" | 55 | `@ca` bằng AST: nền 53 · `75af95c` 55 · head **56** (`+t60 t61 t62`) | **lệch** với head (đúng cho `75af95c`) |
| +114 dòng, 2 tệp (f43aa1e) | +114 | `git diff --numstat 1741e0a f43aa1e -- ops/` ⇒ 1+113 = 114, 2 tệp | khớp |
| +144 (PR) | +144 | `git diff --numstat 89fc4fa e46f569 -- ops/` ⇒ `1 1 bash_nen.py`, `143 15 cong_cu_test.py` = +144/−16, 2 tệp | khớp (trần S3 ≤300 ✔) |
| "66 điểm phóng" (`:15`, f43aa1e) | 66 | AST (`tam/dem_phong.py`): f43aa1e `subprocess.run` 53 + `Popen` 1 = **54**, `chay(` 26, `_g(` 25; head **56**/26/25; 54+26=80; 107 | **không tái lập** |
| "mọi `env=` dựng từ `os.environ`" | có | head: 35 `env=`; truy từng cái (`tam/truy_env.py` + đọc tay 8 chỗ gán bằng tuple): moi_truong 12, dict(os.environ,…) 5, 17 biến ⇒ moi_truong/dict(os.environ)/tham số, `env1`←`bk_don`←`moi_truong` | **khớp** (cho mã hiện có); "kể cả điểm phóng chưa ai viết" không đo được |
| lỗi đột biến = nền (jsonschema) | 1 = 1 | head: `SỐ LIỆU: ca=56 · đột biến=212 · lỗi đột biến=1` (chỉ `KHÔNG_ĐO_ĐƯỢC t2_go_canary`, jsonschema); nền `89fc4fa`: `SỐ LIỆU: ca=53 · đột biến=212 · lỗi đột biến=1` (cùng `t2_go_canary`) | **khớp**, delta 0 (môi trường mặc định, cùng máy) |
| ruff `--select F` delta 0 | 0 | ruff 0.15.15 `--no-cache`: nền = head = {`bash_nen.py` F401 `ast` imported but unused; `cong_cu_test.py` F841 `ci`} (so tập, bỏ số dòng) | khớp |
| docstring `_tach_dinh_dang` không đổi byte | có (spec §2A) | sha256 `ast.get_docstring(clean=False)`: nền = 1741e0a = head = `3bc957a67247801b5dea3052f346751223122a086400cbab315b7181412f8296` (897 ký tự) | khớp |
| nạp `bash_nen` không in gì | có | head: 3.11/3.12/3.13 `-B -W default` stderr rỗng; nền: DeprecationWarning (3.11) / SyntaxWarning (3.12, 3.13) | khớp |
| "go reconfigure giet t61 (a); go env giet t61 (b); r\"\"\"→\"\"\" giet t60" | có | M61a, M61b, M60a `giet_that` đúng nhãn, bán kính 1/55 | khớp |
| "t62 giet_that 'UTF8_MODE=0'" (e46f569) | có | M62a ⇒ `giet_that` 'UTF8_MODE=0' trên 3.11/3.12/3.13 (Linux) | khớp (Linux); Windows KHÔNG ĐO ĐƯỢC |
| "CI dat PYTHONUTF8=1 nen khong di nhanh nay" | có | `ci.yml` job `gate` env `PYTHONUTF8: "1"` (`:71`) cho cả ma trận ubuntu/windows | khớp — hệ quả: CI chỉ chạm nhánh phóng lại qua `t62` |
| "ep ASCII 54/54 (nen: chet o print dau tien)" | có | nền `PYTHONIOENCODING=ascii PYTHONUTF8=0`: rc=1 sau 20s, `UnicodeEncodeError: 'ascii' codec can't encode character '\u1ece' in position 3` ở `print(f"  BỎ QUA ...")` (khớp vế nền). Head dưới `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`: **54/55** (`t61` đỏ) | vế head **lệch** khi ASCII là locale thật |
| "bán kính 2/54" của `bn_doc_cay_lam_viec` nếu thiếu tệp đĩa (chú thích `_stage_byte`) | có | head trọn bộ: `bn_doc_cay_lam_viec` bán kính 1 (không dòng "giết THÊM") — vế "có ghi đĩa ⇒ 1" | khớp vế đo được |
| "47/51" trên Windows 75af95c | có | — | KHÔNG ĐO ĐƯỢC |
| trọn bộ head, môi trường mặc định | — | `tam/log-full-head.txt`: 23:17:16Z→23:36:10Z, `rc=1` (do lỗi đột biến=1 jsonschema) | — |
| trọn bộ NỀN `89fc4fa`, môi trường mặc định | — | `tam/log-full-nen.txt` (23:45:30Z→00:21:05Z, `CONG_CU_TEST_TIEN_TRINH=2`, `TMPDIR` trong `$RV`; lượt đầu bị cắt 23:43Z khi phiên hết giờ, chạy lại): `52/52 đạt; tổng=53, bỏ qua=1` · `SỐ LIỆU: ca=53 · đột biến=212 · lỗi đột biến=1` · `RC=1` · 220 dòng `ok` | đối chứng |
| trọn bộ head `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` | — | `tam/log-full-head-ascii.txt` (23:45:30Z→00:21:50Z): `54/55 đạt; tổng=56, bỏ qua=1`, `ĐỎ t61` (Unable to decode the command…), `KHÔNG_ĐO_ĐƯỢC bán kính cho ['t61_…']` · `SỐ LIỆU: ca=56 · đột biến=212 · lỗi đột biến=2` · `RC=1` | P1 gốc đóng (t29/t39/t42/t45 xanh); **+1 lỗi so nền** do `t61` ĐỎ oan |

### TU-PHONG-LAI-KHONG-TRONG-SUOT  [P2]  Lệnh tự phóng lại không trong suốt: `python - < tệp` ra rc=0 rỗng; giết tiến trình bao để bộ ca mồ côi
TỆP/DÒNG: `ops/cong_cu_test.py:39-40` (`if __name__ == "__main__" and not sys.flags.utf8_mode: sys.exit(subprocess.run([sys.executable, "-X", "utf8", *sys.orig_argv[1:]]).returncode)`).
VẤN ĐỀ: lệnh phóng lại giả định (1) chương trình ĐỌC LẠI ĐƯỢC từ `sys.orig_argv`, (2) tiến trình bao là "chính bộ ca". Cả hai sai
ở nhánh mặc định của Windows (không `PYTHONUTF8`): (a) `cd ops && python - < cong_cu_test.py` ngoài UTF-8 ⇒ bản phóng lại đọc
stdin đã cạn ⇒ **rc=0, 0 byte, 0,26 giây, không ca nào chạy**; nền `89fc4fa` chạy thật (52/52). Cùng hình dạng "rc=0 + output
rỗng" của CLAUDE.md r244. Không nâng P1 vì không cổng/CI/lệnh nghiệm thu nào gọi dạng này (`git grep`); không hạ P3 vì đây là
hành vi sai, không phải lời khai. (b) Người gọi giết tiến trình bao (timeout của bộ điều phối) ⇒ bộ ca thật (`-X utf8`) chạy
tiếp, mồ côi (đo: 1 tiến trình còn sống; đối chứng không phóng lại: 0). (c) Con chết vì SIGKILL/SIGTERM ⇒ bao thoát 247/241
(mã thường) thay vì trạng thái tín hiệu — fail-close vẫn giữ.
VÁ Ở ĐÂU: chính khối phóng lại `:39-40` — chỗ duy nhất quyết định có phát lại hay không; ca khoá đặt cạnh `t62` (cùng họ).
VÁ THẾ NÀO: (gợi ý, người vá được làm khác) (a) trước khi phóng, nếu `__file__` không phải tệp thật (`<stdin>`, ống) ⇒ in lý do
ra stderr và `sys.exit(3)` — không bao giờ phóng một chương trình không đọc lại được. (b) POSIX: có thể dùng `os.execve` (cùng PID
⇒ không mồ côi, tín hiệu/mã thoát trong suốt); Windows: Job Object `KILL_ON_JOB_CLOSE`, hoặc tối thiểu ghi rõ trong chú thích +
hướng dẫn nghiệm thu "giết CẢ CÂY". Hint chỉ làm (a); (b) để executor chọn — `os.execve` làm nhánh Windows không còn được Linux CI
chạm tới (đánh đổi, xem "BẢN VÁ CÓ THỂ ĐẺ RA"). (c) chấp nhận, ghi chú.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t64` chốt (4) (stdin ⇒ rc≠0 hoặc thật sự chạy). Đột biến phải chết: bỏ chặn nguồn (`H_Mg2`) ⇒
`t64` `giet_that` "(4) nguồn đọc từ stdin: rc=0 mà KHÔNG chạy gì". Trên head không hint, chốt (4) ĐỎ (đó là bằng chứng lỗi).
BẢN VÁ CÓ THỂ ĐẺ RA: `-c` và `/dev/fd/N` cũng bị từ chối (trước đó `-c` phát lại được) — không ai gọi bộ ca bằng `-c`; nếu có thì
thông điệp rc=3 nói rõ cách gọi đúng. Nếu chọn `os.execve` trên POSIX: mọi chốt của `t64` đo nhánh POSIX, còn nhánh
`subprocess` chỉ Windows chạm (master CI windows + nghiệm thu local) — phải ghi rõ.
HINT (hunk nào trong HINT.patch): Hunk 2 (`@@ -33`, chặn nguồn + chặn lần 2 — GỢI Ý), Hunk 4 (`t64` chốt (4)).
ĐÃ THỬ NGHIỆM HINT: dry-run `patch -p0 --fuzz=0` rc=0; áp thật rc=0 trên clone mới; `t64` `qua` trên 3.11/3.12/3.13, môi trường
mặc định và `LC_ALL=C PYTHONUTF8=0`; `H_Mg2` ⇒ `giet_that` (4); 58 ca trên bản áp: `qua=57, bo_qua=1`.
ĐỘ TIN: cao cho (a)(c) (đo trực tiếp, có đối chứng nền); vừa cho (b) trên Windows (đo trên Linux, suy cơ chế cho Windows).

### TU-PHONG-LAI-CHI-KHOA-CO-UTF8  [P2]  `t62` chỉ khoá CỜ: nuốt mã thoát, bỏ `-X utf8` (lặp vô hạn), bỏ chốt `__main__` đều sống 56/56
TỆP/DÒNG: `ops/cong_cu_test.py:39-40` (lệnh phóng lại), `:2294-2306` (`t62`), `:6842-6844` (cửa).
VẤN ĐỀ: lệnh phóng lại là LỐI THOÁT MỚI của cả bộ ca trên Windows (nhánh mặc định), nhưng ca khoá duy nhất (`t62`) chỉ đọc
`UTF8_MODE=1`. Đo: `M62f` (`subprocess.run(...); sys.exit(0)`) sống 56/56 ⇒ trên Windows bộ ca sẽ LUÔN rc=0 dù ca đỏ; CI không
bắt được vì CI đặt `PYTHONUTF8=1` (không bao giờ đi nhánh này). `M62b` (bỏ `-X utf8`) sống 56/56 vì con thừa kế `PYTHONUTF8=1`
từ `_ep_utf8()`; cùng đột biến ấy + gọi `-X utf8=0` (có hay không `-I`) ⇒ phóng VÔ HẠN (`-I -X utf8=0`:
`[11, 19, 28, 35, 44, 53]`; `-X utf8=0`: `[11, 18, 26, 34, 42, 50]` tiến trình sau 1..6 giây).
`M62e` (bỏ chốt `__main__`) sống 56/56 — trái với chú thích `:35`.
VÁ Ở ĐÂU: ca mới cạnh `t62` (cùng hợp đồng "chạy làm `__main__`"), cửa mới trong khối `__main__`, chốt (e) trong trình nạp của
`t61` (nơi DUY NHẤT nạp tệp bằng importlib dưới `PYTHONUTF8=0`); chặn lần 2 trong chính lệnh phóng lại.
VÁ THẾ NÀO: (1) cửa `--tu-kiem-ma-thoat-phong-lai` in cờ rồi thoát **7**; `t64` gọi nó dưới `PYTHONUTF8=0`, đòi rc==7 VÀ
`UTF8_MODE=1`. (2) `t64` gọi `-X utf8=0` (cờ dòng lệnh thắng `PYTHONUTF8=1` mà con thừa kế) đòi UTF-8 sau đúng một lần
phóng — không dùng `-I` vì `-I` bỏ user-site (máy cài PyYAML `--user` sẽ đỏ oan). (3) (gợi ý) biến
`CONG_CU_TEST_DA_PHONG_LAI` do lệnh phóng lại đặt cho con, con `os.environ.pop` ngay khi nạp; gặp nó mà vẫn ngoài UTF-8 ⇒ rc=3,
không phóng nữa — biến vòng lặp thành lỗi ồn ào và cho (2) một kết cục có hạn; `t64` (3) khoá. (4) trình nạp của `t61` khởi động
ngoài UTF-8: gặp UTF-8 mode hoặc `SystemExit` lúc nạp ⇒ 11; `t61` (e) khoá.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t64` (1)(2)(3), `t61` (e). Phải chết: `H_M62f` ⇒ t64 (1) "rc=0 (chờ 7)"; `H_M62b` ⇒ t64 (2) "rc=3"
(KHÔNG lặp); `H_Mg1` ⇒ t64 (3); `H_M62e` ⇒ t61 (e); `H_M62a` ⇒ t62 + t64 (1). Đã đo: tất cả `giet_that` đúng nhãn.
BẢN VÁ CÓ THỂ ĐẺ RA: biến môi trường mới là trạng thái xuyên tiến trình — `pop` lúc nạp là bắt buộc (không có nó, con của `t62`
thừa kế biến và tự từ chối). Đột biến kép (bỏ cả `-X utf8` lẫn chặn lần 2) vẫn lặp vô hạn và `t64` (2) sẽ treo tới timeout 120s
rồi để lại chuỗi tiến trình — muốn chặn cả ca này phải chạy (2) trong session riêng và `killpg` khi quá hạn (POSIX). Nhãn thông
điệp (1) gộp hai điều kiện (rc và cờ) — dưới `H_M62a` nó in "rc=7 (chờ 7)" kèm 'UTF8_MODE=0': đúng ca, lời hơi lệch; tách hai `bang` nếu muốn.
HINT (hunk nào trong HINT.patch): Hunk 2 (lệnh phóng lại — GỢI Ý), Hunk 3 (`t61` (e)), Hunk 4 (`t64`), Hunk 7 (cửa).
ĐÃ THỬ NGHIỆM HINT: như trên; `t62` vẫn `qua` và vẫn giết `H_M62a`.
ĐỘ TIN: cao.

### CA-KHOA-UTF8-THIEU-QUAN-SAT  [P2]  `t61` suy từ MÃ THOÁT: 3 đột biến sống 56/56, và ĐỎ oan dưới `LC_ALL=C`
TỆP/DÒNG: `ops/cong_cu_test.py:2267-2291` (`t61`), `:18-26` (`_BIEN_UTF8`, `_ep_utf8`).
VẤN ĐỀ: (1)–(4) như lượt 1, đo lại: `M61c`, `M61d`, `M61e` sống qua CẢ 56 ca; nhánh `hasattr(reconfigure)` không có đối chứng.
(5) MỚI: `t61` đưa mã NGUỒN có chữ Việt qua argv `-c` cho con mà nó CỐ Ý tắt UTF-8 mode; dưới `LC_ALL=C` con không giải mã
được argv ("Unable to decode the command from the command line", rc=1) — chết TRƯỚC khi nạp — và chốt `bang` (a) (`rc != 1`)
quy thành "không in được chữ Việt". Hệ quả đo được: lượt trọn bộ head dưới `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` ra
**54/55**, `t61` bị loại khỏi bán kính như "đỏ ở nền", `SỐ LIỆU: … lỗi đột biến=2` (nền và head môi trường mặc định: 1). Cùng gốc: rc=1 là mã chung của MỌI lỗi Python, nên (a) cũng sẽ cấp
`giet_that` cho một đột biến làm hỏng việc nạp tệp vì lý do vô can (dạng tín dụng giả CLAUDE.md đã ghi).
VÁ Ở ĐÂU: `t61` — ca khoá duy nhất của `_ep_utf8`.
VÁ THẾ NÀO: đo BYTE thay vì mã thoát: (c) stderr của trình nạp phải chứa byte UTF-8 của chữ Việt (stderr mặc định
`backslashreplace` nên KHÔNG ném — mã thoát không bao giờ thấy); (b') stdout của cháu chứa byte UTF-8 thật; (d) cháu tự báo
`[utf8_mode, PYTHONUTF8, PYTHONIOENCODING]` = `[1, "1", "utf-8"]`; (f) gọi `_ep_utf8` với StringIO (không có `reconfigure`) ⇒
không ném, vẫn đặt biến. Tách giàn giáo: trình nạp in `NAP_OK` sau khi nạp xong, thiếu ⇒ `dung` (tín dụng giả, không phải giết).
Argv thuần ASCII: `ma = ma.encode("ascii", "backslashreplace").decode("ascii")` (và tương tự cho mã của cháu) — dựng lúc chạy
nên không phải viết chuỗi thoát trong nguồn.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t61` mới. Phải chết: `H_M61c` ⇒ (c); `H_M61d` ⇒ (d) `[0, '0', 'utf-8']`; `H_M61e` ⇒ (b');
`H_M61f` (bỏ `hasattr`) ⇒ (f) 'AttributeError'; vẫn giết `H_M61a` (a), `H_M61b` (b). Và `t61` phải XANH dưới `LC_ALL=C
PYTHONUTF8=0 PYTHONIOENCODING=ascii` (đã đo: `qua` trên 3.11/3.12/3.13).
BẢN VÁ CÓ THỂ ĐẺ RA: (d) giả định trình nạp được khởi động với `PYTHONUTF8=0` tường minh (không phải "tự bật" do locale C) —
đúng vì `t61` đặt biến ấy; nếu ai bỏ nó thì (e) cũng đổi nghĩa. `NAP_OK` in qua `print(..., flush=True)` TRƯỚC (a).
HINT (hunk nào trong HINT.patch): Hunk 3.
ĐÃ THỬ NGHIỆM HINT: như bảng "Trên head + HINT"; 58 ca `qua=57, bo_qua=1`.
ĐỘ TIN: cao.

### CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG  [P2]  Bốn chốt `rc` của staging trong `t49` không răng
TỆP/DÒNG: `ops/cong_cu_test.py:5485-5508` (`_stage_byte` lồng trong `t49`), `:5519-5521` (`ga`).
VẤN ĐỀ: `t49` chỉ đi đường THÀNH CÔNG; `M49a/b/c/d` sống qua cả 56 ca (đo lại). Đây là chốt quyết định "KHÔNG ĐO ĐƯỢC" vs "đỏ/xanh
oan" mà spec §2B đòi — trên Windows nó là thứ quyết định `t49` có bị bỏ qua không.
VÁ Ở ĐÂU: dời `_stage_byte` và chốt `git add` ra cấp module (`_dat_ten_byte_vao_index`, `_git_add_hoac_bo_qua`) với tham số
`chay=subprocess.run`, để một ca bơm được lỗi TỪNG bước; `t49` dùng lại y nguyên (thân không đổi nghĩa).
VÁ THẾ NÀO: `t63` bơm `hash-object` rc=128 · `update-index` rc=128 · `ls-files` thiếu tên · `git add` rc=128, đòi đúng
`BoQuaMoiTruong` mang dấu `rc=128/0` · `rc=0/128` · `rc=0/0` · `git add rc=128`; đối chứng mọi bước thành công ⇒ không ném.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t63`. Phải chết: `H_M49a/b/c/d` (đo: `giet_that` đúng nhãn), `H_M49e` "luôn ném" ⇒ (0) — và
khi ấy `t49` ra `bo_qua`, không ĐỎ oan (đúng spec).
BẢN VÁ CÓ THỂ ĐẺ RA: `t63` gọi helper TRONG tiến trình ⇒ bộ `DOT_BIEN` (đột biến trên bản sao đĩa) không chạm tới — cùng giới hạn
`t29` từng ghi; nếu muốn đưa vào `DOT_BIEN` thì cần một cửa tiến trình con như `--tu-kiem-ban-kinh`. Thông điệp `git add` đổi từ
`str` sang `bytes` repr (helper đọc bytes để khỏi phụ thuộc mã hoá).
HINT (hunk nào trong HINT.patch): Hunk 4 (helper + `t63`), Hunk 5–6 (`t49` dùng helper).
ĐÃ THỬ NGHIỆM HINT: `t49` `qua` trên 3.11/3.12/3.13 và dưới `LC_ALL=C`; `t63` `qua`; bảng đột biến sau hint.
ĐỘ TIN: cao.

### NGHIEM-THU-WINDOWS-CON-THIEU  [P2]  Chưa có nghiệm thu Windows cho head theo §6 (và bước đo giả thuyết B)
TỆP/DÒNG: spec §2B (bước đầu), §6.1–6.3; hiện vật: thân commit `e46f569`.
VẤN ĐỀ: chỉ có MỘT số đo Windows, trên `75af95c` và ĐỎ (47/51). Không có: N/N trên Windows cho `e46f569`; danh sách + lý do 4 ca bỏ
qua trên Windows (Linux chỉ 1); delta lỗi đột biến so nền cùng máy; lượt ép ASCII; đột biến (i)/(ii) trên Windows; phép đo giả
thuyết B trước khi vá. HƯỚNG 12 cho thấy vì sao danh sách bỏ qua quan trọng: nếu Git for Windows từ chối `\` trong INDEX, `t49`
bỏ qua TOÀN CA — kể cả chốt (3) NGÀY GỠ không dính gì tới tên — mà "t49 không ĐỎ" vẫn được tính là đạt.
VÁ Ở ĐÂU: nghiệm thu (hiện vật), không phải mã.
VÁ THẾ NÀO: trên máy Windows local, neo exact head (sau khi vá các finding trên): (1) nền `1741e0a` (hoặc merge-base đã đổi) rồi
head `python ops\cong_cu_test.py` ⇒ in NGUYÊN khối `BỎ QUA`/`ĐỎ`/`SỐ LIỆU`; (2) cùng bộ với `PYTHONIOENCODING=ascii PYTHONUTF8=0`;
(3) hai đột biến §6.3 trên bản sao tạm; (4) log `git add -A`/`ls-files -z`/`update-index` của `t49` (giả thuyết B) — gồm tên
mang `\`. Nếu `t49` bỏ qua vì `\`, cân nhắc tách (2d) thành ca riêng để phần còn lại của `t49` vẫn đo được trên Windows.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: không áp dụng (nghiệm thu); đột biến §6.3 (i)(ii) phải chạy TRÊN Windows.
BẢN VÁ CÓ THỂ ĐẺ RA: không.
HINT: không có hunk.
ĐÃ THỬ NGHIỆM HINT: không áp dụng.
ĐỘ TIN: cao (đối chiếu hiện vật); phần Windows KHÔNG ĐO ĐƯỢC.

### LOI-KHAI-RONG-HON-PHEP-DO  [P3]  Chú thích khai "66 điểm phóng", "kể cả điểm phóng chưa ai viết", "`t62` khoá" chống lặp, "`t61`… nạp thì không được phóng gì"
TỆP/DÒNG: `ops/cong_cu_test.py:14-16`, `:35-37`.
VẤN ĐỀ: "66" không tái lập được bằng công thức nào (54 / 56 / 80 / 107); "kể cả điểm phóng chưa ai viết" là lời khai cho mã chưa
có; `:36` gán cho `t62` việc khoá chống lặp mà `M62b` sống; `:35` ngụ ý `t61` canh "nạp không phóng" mà `M62e` sống.
VÁ Ở ĐÂU: chính các dòng chú thích ấy.
VÁ THẾ NÀO: ghi số đo kèm SHA và công thức; nói thẳng phần chưa khoá; sau khi có `t64`/`t61` (e) thì trỏ đúng ca.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: không (lời văn); các lời khai mới trỏ tới `t64` (1)(2)(3)(4) và `t61` (e) — đã có đột biến chết ở trên.
BẢN VÁ CÓ THỂ ĐẺ RA: số "56 / 35" neo `e46f569` sẽ cũ khi thêm lời gọi — nên để kèm SHA như hint làm.
HINT (hunk nào trong HINT.patch): Hunk 1, Hunk 2 (phần chú thích).
ĐÃ THỬ NGHIỆM HINT: áp sạch; AST của tệp sau áp hợp lệ; không đổi hành vi.
ĐỘ TIN: cao.

### TEN-CA-LECH-SPEC  [P4]  Ca khoá mới tên `t60_…` trong khi spec §2A/§6.3 gọi `t52_import_bash_nen_khong_in_gi_ra_stderr`
TỆP/DÒNG: `ops/cong_cu_test.py:2235`; spec §2A, §6.3(i).
VẤN ĐỀ: người nghiệm thu theo spec tìm `t52` sẽ không thấy; hai commit không khai lệch (có thể để tránh va với ca của #668 —
không thấy ghi). Không đổi hành vi.
VÁ Ở ĐÂU / THẾ NÀO: khai lệch trong PR/handoff (lý do + ánh xạ `t52`→`t60`), hoặc đổi tên. Nếu thân PR đã khai thì đóng.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: không áp dụng. BẢN VÁ CÓ THỂ ĐẺ RA: đổi tên sẽ chạm mọi tham chiếu `t60` trong chú thích.
HINT: không có hunk. ĐÃ THỬ NGHIỆM HINT: không áp dụng. ĐỘ TIN: cao (không đọc được thân PR — ngoài hiện vật).

## HINT.patch — tự kiểm

- Tệp: `out/HINT.patch` (sha256 `e9cad80139a4ba20c9528e146d82d5828a0999b96b7308fc60cf942d2247c597`) — 7 hunk trên
  `ops/cong_cu_test.py`, +187/−39 so head; tổng so merge-base sau khi áp **+292** (trần S3: 300 — còn 8 dòng dư).
- `git clone -q cay-kho tam/ap3 && cd tam/ap3 && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch` ⇒ **rc=0**; áp thật rc=0;
  nội dung sau áp trùng từng byte với bản soạn (`cmp`).
- ruff 0.15.15 `--select F` trên bản áp: đúng 2 finding của nền (F401 `ast` ở `bash_nen.py`, F841 `ci`) ⇒ delta 0.
- Trên bản áp: `t49 t60 t61 t62 t63 t64` `qua` trên 3.11/3.12/3.13, cả môi trường mặc định lẫn `LC_ALL=C PYTHONUTF8=0
  PYTHONIOENCODING=ascii`; 58 ca ⇒ `qua=57, bo_qua=1` (`t2`, jsonschema). Trọn bộ (pha bán kính 212 đột biến) trên bản áp:
  KHÔNG chạy — hết thời gian lượt; chỉ đo vòng ca + đột biến tay.
- Nhãn §8 nằm ở đầu tệp; Hunk 2 là GỢI Ý cho mã chạy bộ ca (lệnh tự phóng lại), không phải mã đủ điều kiện "tệp TEST thuần".

## KHÔNG ĐO ĐƯỢC

- Mọi hành vi Windows: `sys.orig_argv` qua `py`/venv launcher, `sys.exit` với mã NTSTATUS lớn, mồ côi dưới TerminateProcess/
  Stop-Process, `update-index` với tên mang `\` dưới `core.protectNTFS` (Linux git nhận cả khi `protectNTFS=true` — kiểm ấy chỉ
  biên dịch trên Windows), danh sách 4 ca bỏ qua trong "47/51", số liệu Windows của `e46f569`.
- Thân PR #690 (không có trong hiện vật, không gọi mạng) — các lời khai chỉ đối chiếu với commit message.
- Trọn bộ có `jsonschema` (CI cài `jsonschema==4.26.0`): lượt này không cài để giữ cùng điều kiện executor khai.
- Trọn bộ (pha bán kính) trên head + HINT.
- Giới hạn §8.2: snapshot đầu/cuối của `cay-kho`/`nen` (HEAD, tree, status kể cả ignored, diff, diff --cached) — đo lúc 00:05Z:
  **đầu == cuối** cho cả hai; chỉ chứng minh không có delta ở hai mốc.
- Sự cố trong lượt: một lệnh `git config --global advice.detachedHead false` đã ghi vào `~/.gitconfig` (ngoài `$RV`); đã gỡ ngay
  (`--unset`, rc=0; các khoá khác không đổi; mtime tệp đổi). Lượt trọn bộ đầu và các lượt đơn ca trước 23:45Z dùng `TMPDIR`
  mặc định (`/tmp`); đã xoá 5 thư mục `dotbien_*`/`bn-import-*` do lượt bị cắt để lại; các lượt sau 23:45Z đặt `TMPDIR` trong
  `$RV/tam/`. Một lệnh `pkill -f` tự khớp shell của chính nó (đúng bẫy SKILL mô tả) — không ảnh hưởng số đo.
