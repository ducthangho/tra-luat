verdict: changes_requested
reviewed_sha: 302a15dd56c58918a4ca9e4965eb54907204a9f9
provider: claude
role: reviewer
review_kind: advisory_review
model_reviewer_identity: claude-opus-5-5 (Opus 5.5, tự khai; phiên điều phối đối chiếu modelUsage)
independent_from_executor_session: true
assurance: review_deferred
review_axes: [spec, standards_security]

> TRẠNG THÁI: HOÀN TẤT 2026-10-01T14:05Z (bắt đầu 11:36:19Z; ghi tăng dần suốt lượt). Đếm theo LỚP còn mở: **P0=0 · P1=0 · P2=1 · P3=1 ·
> P4=5** (BẢNG LỚP). P3 lượt 6 (đồ giả kernel32 bỏ qua tầng ctypes) và P4 báo-hiệu ĐÃ VÁ THẬT; (d) fd-đóng ĐÃ VÁ; mồ côi (b)(c) giữ đóng. Còn: P2
> nghiệm thu Windows (không vá được bằng mã ở Linux) · P3 MỚI: chốt (k4) chỉ đo `rc==0` — đột biến "thoát 0, không phóng, không chạy ca" (K4d) sống,
> trái lời khai "phần đầu VẪN phóng" · P4×5 (đường treo 2/3 của `t64`, đồ giả SIGSEGV, lời khai dạng `env=`/docstring byref, nén dòng, tên ca).
> Trọn bộ dạng mảnh như CI @`302a15d` ở (a) và (b): 415/416 `ok … 1/61` mỗi env + `t2_go_canary` (môi trường) — mảnh 1 chạy lại có `jsonschema` ⇒
> GOM 8/8 416/416, lỗi đột biến 0 ở cả hai env; job `gate` (a)/(b) RC=0; delta lỗi đột biến so nền = 0. `out/HINT.patch` v3: dry-run rc=0;
> áp ⇒ +418/−42 (≤ 420); lô 70 đột biến trên cây áp: mọi nhãn head giữ nguyên + đúng 3 đổi theo chủ đích; `gate` (b) trên cây HINT RC=0.
> Ngưỡng áp: `review_class`/`effective_review_class: sensitive`, `assurance_target: human_audited` (LEASE-g3). Lượt này CÙNG PROVIDER ⇒ nhãn tối
> đa `same_provider_approved`, và nhãn ấy KHÔNG thay mức assurance bắt buộc cho `sensitive` (§8). Executor vòng 7 = Opus 4.8 (fallback, 283/285
> lượt — lời khai prompt/commit, KHÔNG ĐO ĐƯỢC ở đây); mọi lời khai BAO_CAO đã đo lại: BẢNG ĐO + ĐỐI CHIẾU (2 lời khai sai, 1 mô tả lẫn).
> Bắt đầu: 2026-10-01T11:36:19Z (bat_dau.txt). Tệp này ghi TĂNG DẦN.
> SPEC sha256 đo lại `18504ced…0b88` — KHỚP. PROMPT sha256 `959a8c9c…2cd1` = `prompt.sha256`.
> Máy: 4 lõi, 15 GB RAM, đĩa `/` còn 15–18 GB; python 3.11.15/3.12.3/3.13.12; git 2.43.0; KHÔNG `jsonschema`, KHÔNG `shellcheck`.
> Rig (11:37:46Z, MỘT lệnh, `core.abbrev 7`): `tam/{n,l6,h}` = clone `kho.git` @`fc852ff`/`0ce1ad3`/`302a15d`; `cmp` h = cay-kho (2 tệp);
> sha256 `cong_cu_test.py`: h `467248e89ae0c1b7…` (= lời khai `467248e8…`), l6 `05dce551…`, n `cb295ee1…`.
> 16 clone mảnh `tam/m{a,b}/s{0..7}` @`302a15d`; khởi chạy 11:40:10Z (`tam/cu/chay_manh.sh`, setsid; (a) `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`,
> (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` qua `__main__` ⇒ execve thật; mỗi mảnh `CONG_CU_TEST_TIEN_TRINH=1`, `PYTHONDONTWRITEBYTECODE=1`).
> Công cụ: `tam/cu/chay_ca.py` (importlib + `_chay_1_ca` CỦA tệp, luôn `-X utf8`), `tam/cu/dot_bien.py` (clone `--shared` + chép tệp nền,
> mỗi mỏ neo đếm đúng 1, xoá `__pycache__`, `GIET_DUNG_NHAN` chỉ khi `giet_that` VÀ lý do chứa nhãn chờ).

## SNAPSHOT ĐẦU/CUỐI (§8.2)
| đối tượng | đầu (11:37:24Z) | cuối (14:04:30Z) |
|---|---|---|
| `cay-kho` HEAD / tree | `302a15dd56c58918a4ca9e4965eb54907204a9f9` / `9e475a1ba75e86caf098fa5a6d418e43164a1dcd` | `302a15dd56c58918a4ca9e4965eb54907204a9f9` / `9e475a1ba75e86caf098fa5a6d418e43164a1dcd` |
| `cay-kho` `status --porcelain --ignored` / diff / diff --cached | 0 dòng / 0 B / 0 B | 0 dòng / 0 B / 0 B |
| `cay-kho` index (`ls-files -s` sha256) / mtime | `c0d4d87f8a0eaac8` / 11:35:40Z (trước phiên) | `c0d4d87f8a0eaac8` / 11:35:40Z — lệnh khảo sát đầu (`git status --short`, chưa có `GIT_OPTIONAL_LOCKS=0`) KHÔNG ghi index |
| `cay-kho` `.pyc` / `.ruff_cache` | — | 0 / 0 |
| `kho.git` `for-each-ref` sha256 | `b66f6c26b56d2e97` | `b66f6c26b56d2e97` |
| `~/.gitconfig` | `75239ed3763a89e3`, mtime 09:47:50Z (trước phiên) | `75239ed3763a89e3`, mtime 09:47:50Z |
| `~/.cache/pip` | — | tệp mới hơn mốc bắt đầu: 0 (pip luôn `--no-cache-dir`) |
| `out/HINT.patch` | — | sha256 `425e8e448eb1084b7f0443dcc143eae4947965da688f5eb883c4e424a41afa77` (v3, bản cuối) |

Giới hạn: snapshot chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Không lệnh nào của lượt
này chạy bộ ca hay ghi trong `cay-kho`/`kho.git` (chỉ đọc: `git -C cay-kho …`, `git clone kho.git`, Read/grep tệp); không mount, không ghi ngoài `$R`
(trừ khác biệt bắt buộc của công cụ: không có). Mọi bản sao/đột biến/venv/ruff nằm trong `$R/tam/`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

> Commit mới từ lượt 6 (`0ce1ad3`): chỉ `302a15d` (`git diff --numstat 0ce1ad3 302a15d` ⇒ `47 30 ops/cong_cu_test.py` theo myers; `bash_nen.py`
> không đổi). AST từng định nghĩa cấp module (bỏ docstring): code KHÁC đúng `_k32_gia`, `_phong_lai`, `t64`; mọi định nghĩa khác (gồm `_ep_utf8`,
> khối phóng lại, `t49`, `t60`–`t63`, `main`, `_main_gop`, `_in_tu_kiem_che_do_utf8`) TRÙNG `0ce1ad3`. Nhãn §8: `ĐÃ VÁ THẬT` · `VÁ HỜ` ·
> `VÁ SINH LỖI MỚI` · `CHƯA VÁ` (+ `ĐÓNG MỘT PHẦN`). Mọi bằng chứng tự đo trên bản sao tạm của lượt này.

| lớp (slug ổn định) | nguồn | hạng cũ | nhãn trên `302a15d` | bằng chứng tự đo |
|---|---|---|---|---|
| DO-GIA-KERNEL32-BO-QUA-TANG-CTYPES | lượt 6 `0ce1ad3` | P3 | **ĐÃ VÁ THẬT** + **VÁ SINH LỖI MỚI (nhỏ)** ⇒ slug mới DO-GIA-DOC-DIA-CHI-TUY-Y [P4] | lô 1: N_B ⇒ (w1) `ArgumentError: argument 3: TypeError: wrong type` ở BIÊN ctypes; N_H ⇒ (w1) `co: 0`; W6/W6r/W6a/Rc/Ra×2/W5b/W5size/OFS/GCP ⇒ (w1); tương đương thật vẫn sống (N_A, N_C, Rg, W5f, W10); trạng thái W1–W4/W7–W13/M6 giữ nhãn. Đồ giả nay là hàm C thật (`CFUNCTYPE` → con trỏ `CFUNCTYPE(c_int)` trần, sản phẩm tự gán argtypes/restype) — không còn luật viết tay `argtypes is not None`/`_obj`. MỚI: SEGV (số đưa làm con trỏ) ⇒ rc=-11 cả tiến trình |
| DO-GIA-BAO-HIEU-TRUOC-TRANG-THAI | lượt 6 | P4 | **ĐÃ VÁ THẬT** | BH_cu_ngu02 (set() TRƯỚC + `sleep(0.2)`) ⇒ (w1) chết; BH_moi_ngu02 (thứ tự mới + `sleep(0.2)`) ⇒ sống; 60/60 `t64` tự nhiên xanh dưới tải; `k.execve` giả đã đúng thứ tự (tuple trái→phải) |
| TU-PHONG-LAI-KHONG-TRONG-SUOT | lượt 3 → vá 6 (d) | P4 | **(d) ĐÃ VÁ THẬT; khoá (k4) HẸP hơn lời khai ⇒ biểu hiện (e) [P3]** | A/B `_phong_lai` l6/h: `sys.stdout`/`sys.stderr` = None ⇒ l6 ném `AttributeError`, h exec đúng đối số; K4/K4b/K4c ⇒ `(k4) fd 1`/`fd 2`; gỡ (k4)+K4 ⇒ sống (chốt duy nhất); W14 ⇒ sống (tương đương thật). **K4d (thoát 0 không phóng) ⇒ SỐNG** — (k4) chỉ đo rc. (b)(c) giữ đóng: M1 ⇒ (k1), M3 ⇒ (k2) 241, M4 ⇒ (k3), M5 ⇒ (k1); HƯỚNG 2 cùng PID |
| CA-KHOA-T64-TREO-THAY-VI-DO | lượt 6 | P4 | **ĐÓNG MỘT PHẦN** | R11 ⇒ `tin_dung_gia` "giàn giáo … ''" ở 126 s (head lượt 6: treo); R11_HEN_go ⇒ TREO 260 s (Timer có răng); 60/60 `t64` 2,9–4,4 s dưới tải (biên 27×). **Đường thứ hai còn mở**: nt `popen(lenh[:1])` + stdin mở ⇒ treo ở `t64:3061 → _phong_lai:71 wait()` (faulthandler) |
| LOI-KHAI-RONG-HON-PHEP-DO | lượt 1–3; tái phát `8757a84`, `0ce1ad3` | P4 | **ĐÃ VÁ THẬT phần số đếm; còn 1 biểu hiện DẠNG [P4]** | 0 số đếm trôi được trong chú thích/docstring trên dòng thêm (HƯỚNG 11); AST `env=` 39→40 (số cũ sẽ trôi lần 3 — nay không ghi); `t49._add` "2/54" đã bỏ. Còn: danh sách dạng `env=` thiếu `dict({k: v … os.environ.items() …}, …)` |
| NGHIEM-THU-WINDOWS-CON-THIEU | lượt 1 → nay | P2 | **CHƯA VÁ — KHÔNG ĐO ĐƯỢC ở Linux** | không log/receipt Windows cho `302a15d`; vá 7 thêm mã nt chưa chạy (`if sys.stderr is not None`); mô phỏng (4) `tam/gitgia/git` trên h: `t49` `bo_qua`, `t63` `giet_that` "(ops/no_cu.py/rc) … chờ 'no_cu'" — TÁI HIỆN |
| TEN-CA-LECH-SPEC | lượt 2/3 | P4 | theo quyết định chủ kho (khai ở PR) — thân PR KHÔNG ĐO ĐƯỢC | `t52_import` 0; `def t60_import_bash_nen_khong_in_gi_ra_stderr` 1; `t64` ngoài spec |
| TRAN-DONG-DAT-BANG-NEN | lượt 6 | P4 | **ĐÓNG MỘT PHẦN** | `tokenize` dòng thêm: `;` 11→9, > 118 ký tự 29→26, walrus 5→6, max 143→154 (vá 7 thêm 9 dòng > 118) |
| CUA-UTF8-NGOAI-BANG-CUA | lượt 5 `8757a84` | đóng | ĐÃ VÁ THẬT (giữ) | C1 (gỡ khỏi `_CUA`) ⇒ `tin_dung_gia` (fail-closed, kỳ vọng); C2 ⇒ (1); bán kính dispatcher `f25`/`f13`/`f27`/`f28` ⇒ BẢNG ĐO (mảnh) |
| T49-CO-CHE-HOAN-BO-QUA · CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG | advisory `bd6ad5d`; lượt 1 | đóng | ĐÃ VÁ THẬT (giữ) | `bo_qua_va` 0 lần; AST `t49`/`t63` = `0ce1ad3`; M49a ⇒ "(hash-object/rc) … chờ 'rc=128/0'", M49d ⇒ "(add/rc) … chờ 'bình_thường'" |
| T62-GHI-PYC-VAO-CAY | lượt 4 | đóng | ĐÃ VÁ THẬT (giữ) | `t60`–`t64` một mình, clone mới, env con KHÔNG có `PYTHONDONTWRITEBYTECODE` ⇒ 0 `.pyc`, `status --ignored` 0 dòng; R3 (mất `-B`) ⇒ (2) chết VÀ để lại `ops/__pycache__/` (chốt đo đúng thứ nó bảo vệ) |
| UTF8-BO-SOT-BO-DOC | lượt 1 | đóng | ĐÃ VÁ THẬT (giữ) | 8 mảnh env (b) qua execve: vòng CA `60/60 đạt; tổng=61, bỏ qua=1` |
| CA-KHOA-UTF8-THIEU-QUAN-SAT · TU-PHONG-LAI-CHI-KHOA-CO-UTF8 | lượt 1–3 | đóng | ĐÃ VÁ THẬT (giữ) | M61a–g ⇒ (a)…(g) đúng nhãn; R1, R3–R10, C2 ⇒ đúng nhãn; M60a ⇒ t60 (1) |
| CON-TRO-CA-CU | lượt 1 | đóng | ĐÃ VÁ THẬT (giữ) | `t60b` 0 lần |

**Lời khai executor vòng 7 (BAO_CAO/DUONG_VAO, Opus 4.8 do fallback) — soát riêng:** khớp đo: +417/−42; +45/−28 (= histogram, myers ra
+47/−30); sha256 `467248e8…`; ruff F = nền; compile sạch ×3; 9/9 × 2 env; mọi dòng bảng đột biến P3 (N_B, N_H, W6, W5size, N_A, N_C, W5f, W10) và
"regress trạng thái" W1/W2/W7/M1; BAO-HIEU nới 0,2 s hai chiều; (d) K4/K4b; R11 ~120 s; `t64` lặp xanh (của tôi: 60/60). **Không khớp:** (1)
"`readline()` dòng đầu là phép chờ DUY NHẤT không hạn (mọi join/wait khác đã có hạn)" — sai: `_phong_lai:71` `wait()` ở vòng (w2) luồng chính
treo được (HƯỚNG 7); (2) "(k4) … phần đầu VẪN phóng ⇒ rc=0" — rc=0 không chứng minh đã phóng (K4d sống); (3) "A4: argtypes SAI KIỂU làm thu nhỏ
handle/đối số (W5b…)" — mô tả lẫn: W5b là sai KÍCH THƯỚC struct, không phải argtypes (đột biến thì vẫn chết — không phải lỗi mã); (4) BAO_CAO
dừng ở "ĐANG CHẠY (nền) — sẽ điền khi xong": không có kết quả mảnh của executor; số mảnh trong thân commit là của phiên điều phối (HƯỚNG 12).

**Log 16 mảnh của phiên điều phối:** vòng CA 16/16 `60/60 đạt; tổng=61, bỏ qua=1`; 14 mảnh `52/52 … bán kính 1` + mảnh 1 (a)(b) `ĐỎ mảnh 1/8
[M-loi]: 1 lỗi đột biến`; `pyc_con_lai=0`; 0 `rc=141`. NHƯNG 16 log mang 16 `head=` khác nhau, không cái nào là `302a15d`, không cái nào có trong
`kho.git`, không log nào ghi băm tệp test ⇒ không neo được vào commit được review — tôi chạy lại đủ 16 mảnh trên `302a15d` (BẢNG ĐO).

## BẢNG LỚP
| slug lớp | finding/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| NGHIEM-THU-WINDOWS-CON-THIEU | (1) không §6.1–6.3 Windows cho head; (2) giả thuyết B chưa đo; (3) mảnh/gom #668 trên Windows; (4) mô phỏng nền từ chối `\xff` ⇒ `t63` ĐỎ OAN (tái hiện trên `302a15d`); (5) nhánh Job Object + guard `sys.stderr` (vá 7) chưa chạy trên Windows; (6) thời lượng `t64` trên Windows | **P2** | lượt 1 → `302a15d` | (1)–(3),(5),(6) không vá được bằng mã; (4) ĐO Windows trước (spec §2B/S2), hướng vá có từ lượt 5 | KHÔNG ĐO ĐƯỢC ở Linux; (4) mô phỏng `tam/gitgia/git` |
| TU-PHONG-LAI-KHONG-TRONG-SUOT | (b)(c) mồ côi/241 — đóng (POSIX); (d) fd đóng ⇒ nổ — ĐÃ VÁ; **(e) MỚI: (k4) chỉ đo rc ⇒ K4d (thoát 0 không phóng) sống; chú thích/BAO_CAO khai "VẪN phóng"** | **P3** | lượt 3 → vá 6 → vá 7 | (e): (k4) đòi dấu `U8=1 PL=1` ở luồng còn mở (HINT hunk 4+5, mã TEST) | K4d sống trên head, chết trên cây HINT; K4/K4b/K4c giữ nhãn; Windows KHÔNG ĐO ĐƯỢC |
| CA-KHOA-T64-TREO-THAY-VI-DO | đường 1 (readline) — ĐÃ VÁ (R11 ⇒ đỏ 126 s); **đường 2 (nt `wait()` + stdin kế thừa) và đường 3 (Timer chỉ giết bao, bản phóng lại là tiến trình riêng) — còn mở**; lời khai "DUY NHẤT" sai | **P4** | lượt 6 → `302a15d` | `popen` giả `stdin=DEVNULL` (hunk 3) + Timer giết bao và đóng stdin (hunk 4) | faulthandler `:3061 → :71`; M1+R11 head TREO 300 s ⇒ HINT ĐỎ 121,6 s |
| DO-GIA-DOC-DIA-CHI-TUY-Y (MỚI) | `dat` đọc địa chỉ bất kỳ ⇒ SEGV khi số đưa làm con trỏ (Windows thật: FALSE) | **P4** | vá 7 (theo HINT lượt 6) | chặn `p < 64 KiB` (HINT hunk 3) | SEGV rc=-11 trên head; (w1) trên bản sao có chốt |
| LOI-KHAI-RONG-HON-PHEP-DO | số đếm — ĐÃ VÁ; dạng `env=` chưa đủ (dict comprehension của `t64`); docstring `_k32_gia` "lệch byref ⇒ lỗi ở BIÊN" (đo: qua biên) | **P4** | lượt 1–3 → `302a15d` | sửa chú thích + docstring (HINT hunk 1+2) | `tam/cu/dem_env.py`, `so_trong_chu_thich.py` |
| TRAN-DONG-DAT-BANG-NEN | `;` 11→9, >118: 29→26, max 143→154 | **P4** | lượt 6 → `302a15d` | chủ kho quyết thước đo | `tokenize` |
| TEN-CA-LECH-SPEC | `t60`–`t64` thay `t52`; `t64` ngoài spec | **P4** | lượt 2/3 | quyết định chủ kho: khai ở PR | thân PR KHÔNG ĐO ĐƯỢC |
| DO-GIA-KERNEL32-BO-QUA-TANG-CTYPES | — | đóng | lượt 6 → `302a15d` | — | lô 1 (16 ABI + 12 trạng thái) đúng nhãn; tương đương sống |
| DO-GIA-BAO-HIEU-TRUOC-TRANG-THAI | — | đóng | lượt 6 → `302a15d` | — | BH_cu chết / BH_moi sống |
| CUA-UTF8-NGOAI-BANG-CUA · T49-CO-CHE-HOAN-BO-QUA · CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG · T62-GHI-PYC-VAO-CAY · UTF8-BO-SOT-BO-DOC · CA-KHOA-UTF8-THIEU-QUAN-SAT · TU-PHONG-LAI-CHI-KHOA-CO-UTF8 · CON-TRO-CA-CU | — | đóng (giữ) | lượt 1–5 | — | xem ĐỐI CHIẾU |

Đếm: **7 lớp còn mở** (P2×1 · P3×1 · P4×5); **10 lớp đóng** (2 đóng ở lượt này + 8 giữ). Biểu hiện còn mở: WINDOWS 6 · KHONG-TRONG-SUOT 1 (e) ·
T64-TREO 3 (đường 2 + đường 3 + lời khai) · DOC-DIA-CHI 1 · LOI-KHAI 2 (dạng `env=` + docstring byref) · TRAN-DONG 1 · TEN-CA 1 = **15**.
Ngưỡng: `review_class`/`effective_review_class: sensitive`, `assurance_target: human_audited` (LEASE-g3); chỉ thị lượt "approve chỉ khi không còn
P0/P1/P2/P3" ⇒ **changes_requested**, `assurance: review_deferred`. Lượt này CÙNG PROVIDER ⇒ nhãn tối đa `same_provider_approved`, và nhãn ấy KHÔNG
thay mức assurance bắt buộc cho `sensitive` (§8).

## BẢNG SĂN

> Mọi phép đo trên bản sao trong `$R/tam/`, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR trong `$R/tam/tmp`; log `tam/log/`. Lúc đo: 16 mảnh đang
> chạy song song (tải 17–22 / 4 lõi) — tức mọi phép đo thời lượng dưới đây là dưới tải.

```
HƯỚNG 1: dấu chống lặp CONG_CU_TEST_DA_PHONG_LAI có sót sang con/cháu không
  lệnh   : đọc /proc/<pid>/{cmdline,environ} của 3 mảnh env (b) đang chạy + worker `--ban-kinh-con` con của chúng (11:45Z)
  output : pid 14297/14329/14339 `/usr/bin/python3.12 -X utf8 ops/cong_cu_test.py` (cha = bash chay_manh.sh — KHÔNG tầng bao; PID giữ
           qua execve); environ KHỞI ĐẦU mang `CONG_CU_TEST_DA_PHONG_LAI=1` (đúng: execve truyền dấu; `os.environ.pop` lúc nạp xoá
           khỏi môi trường Python); con 29435/29521/29424 (worker): PYTHONUTF8=1 PYTHONIOENCODING=utf-8 CONG_CU_TEST_MANH=k/8, KHÔNG dấu.
           grep: chỉ `t62` (5) cố ý đặt dấu cho con (`hoi(..., **{_DAU_PHONG_LAI: "1"})`); `t64` env loại dấu; `_phong_lai` call site đặt "1".
  kết luận: KHÔNG PHẢI LỖI.

HƯỚNG 2: `__file__` không phải tệp / các dạng gọi khác — trên TỆP THẬT (bản sao gắn `PID=` vào cửa UTF-8), qua execve
  lệnh   : tam/cu/dang_goi.py tam/thu — env -i LC_ALL=C.UTF-8 PYTHONUTF8=0; so PID harness biết với PID cửa in
  output : tệp · `-m ops.cong_cu_test` · symlink · `-I` · `-X utf8=0` ⇒ rc=5 `UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0`, PID in ra = PID
           harness (9933/10055/10178/10324/10465 — cùng PID); stdin `-` ⇒ rc=1 KHONG_PHONG_LAI '<stdin>'; `-c exec(…)` ⇒ rc=1 ''; zipapp ⇒
           rc=1 '…/cct.pyz/__main__.py'; 0 `.pyc`.
  kết luận: KHÔNG PHẢI LỖI — và `t62` đo đúng tiến trình CHẠY BỘ CA (exec giữ PID; `main()` chạy cùng tiến trình).

HƯỚNG 3: mã thoát 5 của cửa tự kiểm có va chạm
  lệnh   : grep `sys.exit(|raise SystemExit|_MA_TU_KIEM_UTF8|return ` trong main/_main_gop/cửa
  output : 5 chỉ ở `_in_tu_kiem_che_do_utf8` (:8747) + 3 chốt `t62`; main 0/1/2/None; `--gop` 0/1/2; worker `--ban-kinh-con` 0/7; cửa tự
           kiểm khác 0/9; đối số lạ 2; KHONG_PHONG_LAI `sys.exit(str)` ⇒ 1.
  kết luận: KHÔNG PHẢI LỖI.

HƯỚNG 4: `t60`–`t64` (đồ giả CFUNCTYPE MỚI) ở đường dẫn kho VÀ TMPDIR chữ Việt + dấu cách, 3 phiên bản × 2 env
  lệnh   : clone --shared "tam/có dấu cách/kho việt"; TMPDIR="tam/tmp/thư mục tạm có dấu"; <py> -X utf8 chay_ca.py … t60_ t61_ t62_ t63_ t64_
           × {3.11.15, 3.12.3, 3.13.12} × {thường, LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii}
  output : 6/6 `TONG {"qua": 5}`; 0 `.pyc`; `status --ignored` 0 dòng (tam/log/viet.txt)
  kết luận: KHÔNG PHẢI LỖI (mã con `t61` dựng bằng `encode("ascii","backslashreplace")` đúng ở đường dẫn ngoài ASCII; CFUNCTYPE chạy cả 3 bản).

HƯỚNG 5: (ii) `t64` (k4) + hạn chót dưới tải và chạy nền: chập chờn? sót tiến trình?
  lệnh   : tam/cu/lap_t64.sh 30 thuong; rồi `trap '' INT` (SIGINT=SIG_IGN kế thừa như job nền) lap_t64.sh 30 sigign; đếm tiến trình mang
           TMPDIR riêng của từng lần sau 2 s
  output : thường 30/30 `qua`, 2,96–4,4 s (trung vị 3,7); SIG_IGN 30/30 `qua` (sigint_ign=1 cả 30), 2,89–4,34 s; sót 0/60; tải 17,5–18,4
  kết luận: KHÔNG PHẢI LỖI — biên hạn chót 120 s ≈ 27× thời lượng lớn nhất đo được dưới tải.

HƯỚNG 6: (ii) chốt (k4) có đo đúng tính chất nó tuyên bố ("phần đầu VẪN phóng") không
  lệnh   : đột biến K4d (lô 2): POSIX `if sys.stdout is None or sys.stderr is None: return 0` trước vòng xả đệm ⇒ bộ ca THOÁT 0 không phóng,
           không chạy ca nào — đúng hình "cổng xanh nhờ rc=0"
  output : `t64` ⇒ `SONG`. (k4) chỉ đòi `r.returncode == 0`; luồng còn mở KHÔNG được đọc. Đối chứng: K4/K4b/K4c (nổ) ⇒ giết đúng `(k4) fd 1`/`fd 2`.
  kết luận: LỖI — finding TU-PHONG-LAI-KHONG-TRONG-SUOT (e) [P3]: chú thích `:3041` + BAO_CAO khai "(k4) … phần đầu VẪN phóng", phép đo
           chỉ là rc; đột biến fail-OPEN sống.

HƯỚNG 7: (ii) "readline dòng đầu là phép chờ DUY NHẤT không hạn" (DUONG_VAO/BAO_CAO) — còn đường treo nào khác của `t64`
  giả thuyết: `_phong_lai` nhánh nt chờ `popen(lenh, env=env).wait()` KHÔNG hạn; trong vòng (w2) nó chạy ở LUỒNG CHÍNH, và con của `popen`
           giả kế thừa stdin của bộ test ⇒ một hồi quy kiểu R11 ở nhánh nt (mất đối số ⇒ REPL) treo khi stdin là terminal/ống mở
  lệnh   : bản sao tam/thu, nt `popen(lenh[:1], env=env)`; chay_ca t64_ với (a) stdin `/dev/null`; (b) stdin = FIFO giữ mở bằng `sleep 300`,
           bọc `faulthandler.dump_traceback_later(90, exit=True)` (tam/cu/chay_ca_fh.py)
  output : (a) `giet_that` (w2) … rc=0, 3 s. (b) KHÔNG dòng kết quả nào; lần 1 bị `timeout -s KILL 200` giết (rc=137); lần 2 ngăn xếp ở 90 s:
           `t64…:3061` (vòng (w2) `phong(k := _k32_gia(hong), …)`) → `_phong_lai:71` → `subprocess.wait` → `_try_wait` (luồng DUY NHẤT).
           Bản vá thử (đồ giả `popen` cho con `stdin=DEVNULL`) trên CÙNG bản sao, CÙNG FIFO ⇒ `giet_that` (w2) sau 3 s.
  kết luận: LỖI (nhỏ) — CA-KHOA-T64-TREO-THAY-VI-DO đóng MỘT PHẦN [P4]; lời khai "phép chờ DUY NHẤT" rộng hơn phép đo. Bán kính CI không chạm
           (stdin worker là DEVNULL; 0 DOT_BIEN nhắm phần đầu tệp) — đường của chạy TAY trong terminal.

HƯỚNG 8: (i) đồ giả MỚI đọc cờ tại ĐỊA CHỈ ctypes truyền — đột biến đưa SỐ vào chỗ con trỏ thì sao
  lệnh   : đột biến SEGV (lô 2): `ctypes.byref(gh), ctypes.sizeof(gh)` → `ctypes.sizeof(gh), ctypes.sizeof(gh)` (argtypes `vp` nhận số 144)
  output : `KHAC` rc=-11 — `ctypes.string_at(144 + 16, 4)` ⇒ SIGSEGV CẢ tiến trình chạy ca, 0 dòng kết quả. Windows thật: nhân kiểm con trỏ ⇒
           SetInformationJobObject trả FALSE (ERROR_NOACCESS) ⇒ CANH_BAO ⇒ (k1)/(w1) đỏ CÓ TÊN. Thử chốt `(p or 0) >= 1 << 16` trong `dat`
           (vùng 64 KiB thấp không bao giờ được ánh xạ: Windows dành sẵn, Linux `vm.mmap_min_addr`=65536) trên bản sao ⇒ `giet_that` (w1).
  kết luận: LỖI (nhỏ, fail-closed nhưng mất chẩn đoán) — finding DO-GIA-DOC-DIA-CHI-TUY-Y [P4].

HƯỚNG 9: `t5` SIGPIPE rc=141 — có liên quan PR
  lệnh   : grep `rc=141` mọi log (16 log điều phối + 16 log mảnh của tôi); `git log fc852ff | grep sigpipe`; diff PR có chạm cai_cong_cu.sh
  output : 0 `rc=141`; `7b308bc Merge pull request #681 … cai-cong-cu-sigpipe` trong `fc852ff`, `cai_cong_cu.sh:64-65` đã thay `| head -1`;
           PR chạm 0 tệp ngoài 2 tệp write set.
  kết luận: KHÔNG PHẢI LỖI (nền cũ đã vá trên master, không liên quan PR).

HƯỚNG 10: (i) đồ giả mô phỏng TRẠNG THÁI hay diễn kịch bản; độ trung thực ABI so ctypes thật
  lệnh   : lô 1 — 16 đột biến ABI/cấu trúc (N_B, N_H, W6, W6r, W6a, Rc, Ra×2, N_A, N_C, Rg, W5b, W5size, W5f, OFS, GCP) + 12 trạng thái (W1–W13, M6)
  output : mọi lỗi ABI "khai/đưa SAI" nay chết (w1): quên byref ⇒ `ArgumentError: argument 3: TypeError: wrong type` ở BIÊN ctypes; lệch
           byref/đổi chỗ trường (144 B, cờ ở offset 40) ⇒ cờ đọc tại địa chỉ thật = 0; quên restype/khai `c_int` cho HANDLE ⇒ handle 1<<60 bị
           cắt; quên argtypes ⇒ handle bị chuyển mặc định; struct 152 B ⇒ `dat` từ chối kích thước. Sống ĐÚNG những biến thể ctypes dung thứ
           (N_A, N_C, Rg = GetCurrentProcess `c_int` ⇒ −1 mở rộng dấu, W5f byte giống hệt, W10). Trạng thái (bảng job/cờ/thành viên/kế thừa)
           vẫn thật: W1–W4/W7–W13/M6 chết đúng nhãn.
  kết luận: KHÔNG PHẢI LỖI — lớp DO-GIA-KERNEL32-BO-QUA-TANG-CTYPES ĐÃ VÁ THẬT. Ghi nhận: đồ giả CHẶT HƠN Windows ở cắt HANDLE (handle nhân
           Windows vừa 32 bit — Microsoft cho phép cắt/mở rộng dấu) ⇒ W6r/Rc có thể tương đương trên Windows thật; chặt hơn là fail-closed.
           Lệch lời khai nhỏ: docstring `_k32_gia` "thiếu/lệch `byref` thì lỗi ở BIÊN" — N_H (lệch) QUA biên (stderr rỗng), bị bắt bởi trạng
           thái (`co: 0`); chỉ N_B (thiếu) lỗi ở biên ⇒ biểu hiện thứ hai của LOI-KHAI [P4] (HINT hunk 2).

HƯỚNG 11: (iii) con số/khẳng định trong chú thích còn trôi được không
  lệnh   : tam/cu/so_trong_chu_thich.py — mọi chữ số trong CHÚ THÍCH/DOCSTRING trên dòng THÊM fc852ff→302a15d; tam/cu/dem_env.py (AST mọi `env=`)
  output : 0 số ĐẾM trôi được: còn lại là ngày (27-09/30-09-2026), SHA (`8757a84`), issue (#671/#570), run CI (36454930689), hằng ABI
           (144/112/16/0x2000/9/32/64 bit), mã thoát (241/5/0), nhãn mệnh đề, `47/51` neo "đo 30-09-2026 Windows", `56/56` neo "review lượt
           2+3", `bash_nen.py:900` trích log run 36454930689. AST `env=`: 39 (l6) → **40** (h) — đúng con số chú thích cũ sẽ trôi lần nữa; nay
           không ghi. Nhưng danh sách DẠNG chưa đủ: `t64` `env = dict({k: v for k, v in os.environ.items() if …}, PYTHONUTF8="0")` (:3017,
           dùng ở :3024 và :3042 mới) KHÔNG thuộc `moi_truong(…)`/`dict(os.environ, …)`/`{**os.environ, …}`/biến truy về chúng.
  kết luận: LỖI (vặt) — LOI-KHAI-RONG-HON-PHEP-DO còn biểu hiện nhỏ [P4] (dạng, không phải số; + docstring byref ở HƯỚNG 10).

HƯỚNG 12: lời khai "16/16 mảnh … 415/416" của phiên điều phối neo vào đâu
  lệnh   : head -1 do-manh-dieu-phoi/*.log; `git -C kho.git cat-file -t fa48c26b…`; grep `467248` trong log
  output : 16 log mang 16 `head=` KHÁC NHAU (fa48c26b…, d370a346…, …, 492dda29…) — KHÔNG cái nào là `302a15d`, và 0 cái có trong kho.git;
           0 log ghi sha256 tệp test. Thân commit khai "ban sao, sha256 cong_cu_test.py 467248e8…" — log không chứng minh được băm ấy.
  kết luận: KHÔNG ĐO ĐƯỢC từ hiện vật điều phối ⇒ đo lại TRÊN `302a15d` (BẢNG ĐO). Không phải lỗi mã; ghi nợ bằng chứng (P4 quan sát, không đếm lớp).

HƯỚNG 13: (iv) giãn mã có đổi hành vi so 0ce1ad3
  lệnh   : tam/cu/ast_so.py (AST từng định nghĩa) + tam/cu/ab_phong_lai.py (A/B `_phong_lai` l6 vs h dưới CẢ HAI đồ giả)
  output : code đổi đúng 3 định nghĩa; A/B 11/13 kịch bản GIỐNG từng trường (rc, stderr nguyên văn, số con, bảng job); KHÁC đúng 2 = luồng None
  kết luận: KHÔNG PHẢI LỖI.

HƯỚNG 14: `t63` bơm lỗi đo đúng chốt hay bị chốt khác bắt hộ
  lệnh   : M49a (bỏ `oid.returncode`), M49d (`if ga.returncode:` → `if False:`) trên head (lô 2)
  output : giết đúng `(hash-object/rc) … chờ 'rc=128/0'` và `(add/rc) … chờ 'bình_thường'`; AST `t49`/`t63` = `0ce1ad3`
  kết luận: KHÔNG PHẢI LỖI.

HƯỚNG 15: (ii) hạn chót `t64` khi bản phóng lại là TIẾN TRÌNH RIÊNG (đường Windows khi Job hỏng ⇒ CANH_BAO, `popen(...).wait()`)
  giả thuyết: `threading.Timer(120, p.kill)` giết đúng PID harness biết; POSIX execve thì đó là bộ ca, nhưng khi bản phóng lại là con riêng
           (Windows không Job; POSIX hồi quy M1) thì cháu còn giữ stdout và đọc stdin của harness ⇒ `readline()` vẫn chặn
  lệnh   : đột biến kép M1+R11 (dot_bien.py, khe riêng) trên head; rồi cùng đột biến trên bản sao cây HINT có Timer
           `lambda: p.kill() or p.stdin.close()`
  output : head ⇒ `TREO` (bị giết ở 300 s, 0 dòng kết quả); bản có Timer mới ⇒ `TIN_DUNG_GIA` "giàn giáo: phần đầu không phóng lại … ''" sau 121,6 s
  kết luận: LỖI (nhỏ) — đường (3) của CA-KHOA-T64-TREO-THAY-VI-DO [P4]; Windows thật (Job hỏng) KHÔNG ĐO ĐƯỢC, đây là mô phỏng POSIX.
```

## BẢNG ĐỘT BIẾN

> Công cụ: `tam/cu/spec_l7.py` (lô 1, 57 đột biến) + `tam/cu/spec_l7b.py` (lô 2, 8) — mỏ neo NGUYÊN VĂN từ `302a15d`, kiểm trước mỗi mỏ
> neo đếm ĐÚNG 1. Chạy: `tam/cu/chay_lo.sh` — 3 khe clone `--shared` dựng một lần; mỗi đột biến chép lại 2 tệp từ nền, áp, xoá `__pycache__`,
> `PYTHONDONTWRITEBYTECODE=1`, TMPDIR riêng, stdin `DEVNULL`, `python3.12 -X utf8 tam/cu/chay_ca.py` (importlib + `_chay_1_ca` CỦA tệp) ⇒
> `GIET_DUNG_NHAN` chỉ khi `giet_that` (tức `TinHieuChotCa` mang ĐÚNG tên ca) VÀ lý do chứa nhãn chốt chờ. Sau mỗi đột biến: khe trả về nền,
> `status --porcelain --ignored` ghi vào log (rỗng ở 56/57; R3 để lại `ops/__pycache__/` — đúng là đột biến "mất `-B`"). Dưới tải 17–22 (16 mảnh
> song song). Log: `tam/log/db-l7.jsonl` (lô 1, xong 11:59:32Z), `tam/log/db-l7b.jsonl` (lô 2).
> **Lô 1:** 47 giết thật đúng nhãn · 8 sống KỲ VỌNG (N_A, N_C, Rg, W5f, W10, W14 tương đương; T_K4_go_va_K4 chứng minh (k4) là chốt DUY NHẤT
> bắt K4; T_HEN_go = Timer chỉ có tác dụng khi treo) · C1 tín dụng giả kỳ vọng (fail-closed) · R11 ĐỎ có tên (giàn giáo) sau 126 s thay vì treo.
> **0 sống sót ngoài kỳ vọng ở lô 1.** Lô 2: xem dưới bảng.

| đột biến (thay đúng chỗ trên 302a15d) | ca đích | kết quả — tín hiệu (rút gọn) | phân loại |
|---|---|---|---|
| N_H — `byref(gh, 16)` (lệch offset) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': {<Popen: returncode: -9 args: ['/usr/bin/python (21.3 s) | giết thật |
| W6_khong_khai — bỏ hẳn khai restype/argtypes | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (22.9 s) | giết thật |
| N_B — truyền `gh` thay `byref(gh)` (quên byref) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (27.7 s) | giết thật |
| W6a_quen_argtypes — chỉ khai restype (quên argtypes) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (18.5 s) | giết thật |
| Rc_create_c_int — Create restype `vp`→`c_int` (cắt HANDLE) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (17.9 s) | giết thật |
| W6r_quen_restype — chỉ khai argtypes (quên restype ⇒ HANDLE c_int) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (15.0 s) | giết thật |
| N_A_assign_proc_c_int — Assign argtypes process `vp`→`c_int` (N_A) | t64_ | `SONG`  (7.7 s) | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| Ra_assign_job_c_int — Assign argtypes job `vp`→`c_int` | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 8192, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_CO (16.4 s) | giết thật |
| Ra_set_handle_c_int — Set argtypes handle `vp`→`c_int` | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (16.8 s) | giết thật |
| Rg_getcur_c_int — GetCurrentProcess restype `vp`→`c_int` | t64_ | `SONG`  (3.9 s) | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| W5b_u32_64bit — `u32`=c_uint64 MỌI nơi (struct 152 B) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (13.8 s) | giết thật |
| W5f_co_u64 — CHỈ trường `co` → c_uint64 | t64_ | `SONG`  (10.8 s) | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| N_C_create_argtypes_rong — Create argtypes `()` (N_C) | t64_ | `SONG`  (11.4 s) | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| OFS_co_sl_doi_cho — đổi chỗ `co`/`sl` (144 B, cờ ở offset 40) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': {<Popen: returncode: -9 args: ['/usr/bin/python (21.4 s) | giết thật |
| W1_co0 — cờ 0 | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': {'cha', <Popen: returncode: -9 args: ['/usr/bin (18.1 s) | giết thật |
| W5size_tg3 — `tg` c_int64*3 (struct 152 B) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (18.3 s) | giết thật |
| W7_nuot_canh_bao — nuốt CANH_BAO (`if False`) | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở CreateJobObjectW (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test): phải VẪN chạy đúng một lần, m (7.1 s) | giết thật |
| W2_co3000 — cờ 0x3000 (thêm BREAKAWAY) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 12288, 'tv': {'cha'}}} stderr='' (13.6 s) | giết thật |
| W10_bo_job_and — bỏ `job and` | t64_ | `SONG`  (6.2 s) | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| W8_bo_kiem_set — bỏ kiểm Set (`or 1`) | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở SetInformationJobObject (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test): phải VẪN chạy đúng một (8.0 s) | giết thật |
| GCP_getpid — Assign(job, os.getpid()) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 8192, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_CO (16.4 s) | giết thật |
| W11_except_oserror — `except OSError` | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở WinDLL (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test): phải VẪN chạy đúng một lần, mã 7 đi qua (9.0 s) | giết thật |
| M6_nt_di_exec — nt đi exec | t64_ | `GIET_DUNG_NHAN` (w0) nhánh Windows gọi exec — trên nt `os.exec*` phóng MỚI rồi thoát cha ⇒ MỒ CÔI: [('/usr/bin/python3.12', ['/usr/bin/p (3.5 s) | giết thật |
| W13_phong_hai_lan — phóng hai lần | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 8192, 'tv': {<Popen: returncode: -9 args: ['/usr/bin/pyt (18.7 s) | giết thật |
| M4_sigint_ign — SIG_IGN SIGINT trước exec | t64_ | `GIET_DUNG_NHAN` (k3) tiến trình chạy bộ ca 3585 LỜ SIGINT/Ctrl-C: 'PID=3585 U8=1 PL=1 INT=0\n' (2.7 s) | giết thật |
| W3_lop2 — lớp thông tin 9→2 | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1152921504606846977: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_MO_COI — (18.8 s) | giết thật |
| M3_pdeathsig — subprocess + PR_SET_PDEATHSIG | t64_ | `GIET_DUNG_NHAN` (k2) SIGTERM tới tiến trình chạy bộ ca 4145 (harness biết 4089) mà harness thấy rc=241, chờ -15 (5.8 s) | giết thật |
| K4_xa_dem_cu — hoàn nguyên `stdout.flush() or stderr.flush()` | t64_ | `GIET_DUNG_NHAN` (k4) fd 1 đóng ⇒ nổ trước khi phóng lại: rc=1 b"sys.stderr.flush()\n    ^^^^^^^^^^^^^^^^\nAttributeError: 'NoneType' obj (6.7 s) | giết thật |
| W9_bo_kiem_assign — bỏ kiểm Assign (`or 1`) | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở AssignProcessToJobObject (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test): phải VẪN chạy đúng mộ (10.4 s) | giết thật |
| W14_bo_xa_dem — bỏ hẳn vòng xả đệm | t64_ | `SONG`  (10.6 s) | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| W12_wait_nhan0 — `.wait() * 0` | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở CreateJobObjectW (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test): phải VẪN chạy đúng một lần, m (6.1 s) | giết thật |
| K4c_bo_guard — bỏ `if luong is not None` | t64_ | `GIET_DUNG_NHAN` (k4) fd 1 đóng ⇒ nổ trước khi phóng lại: rc=1 b"g_lai\n    luong.flush()\n    ^^^^^^^^^^^\nAttributeError: 'NoneType' ob (4.6 s) | giết thật |
| T_HEN_go — không `start()` Timer (head) | t64_ | `SONG`  (4.8 s) | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| R4_get_thay_pop — `.get` thay `.pop` | t62_ | `GIET_DUNG_NHAN` (3) dấu phóng lại còn trong môi trường của bản phóng lại: 'UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=1' (2.6 s) | giết thật |
| M1_subprocess — POSIX `subprocess.run` thay execve | t64_ | `GIET_DUNG_NHAN` (k1) harness kill() pid 6138 mà tiến trình chạy bộ ca 6170 vẫn giữ pipe sau 10s — MỒ CÔI (14.0 s) | giết thật |
| R7_bo_not_isfile — bỏ `not isfile` | t62_ | `GIET_DUNG_NHAN` (6) `python -B - --tu-kiem-che-do-utf8 < cong_cu_test.py` ngoài UTF-8 phải DỪNG ồn ào, không chạy chương trình RỖNG: rc= (6.9 s) | giết thật |
| R10_tu_choi_thoat0 — từ chối nhưng thoát 0 | t62_ | `GIET_DUNG_NHAN` (5) đã mang dấu phóng lại mà vẫn ngoài UTF-8 phải DỪNG, không phóng tiếp: rc=5 'UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0 (8.0 s) | giết thật |
| M60a_khong_raw — `r"""`→`"""` (bash_nen, §6.3 i) | t60_ | `GIET_DUNG_NHAN` (1) bash_nen.py biên dịch kèm cảnh báo: SyntaxError: invalid escape sequence '\(' (bash_nen.py, line 898) (1.9 s) | giết thật |
| M5_posix_di_nt — POSIX đi nhánh nt | t64_ | `GIET_DUNG_NHAN` (k1) harness kill() pid 8837 mà tiến trình chạy bộ ca 8897 vẫn giữ pipe sau 10s — MỒ CÔI (13.7 s) | giết thật |
| M61c_chi_stdout — chỉ stdout | t61_ | `GIET_DUNG_NHAN` (c) stderr của tiến trình nạp không mang chữ Việt UTF-8 THẬT: rc=0 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe1\xbb\xaf Vi\xe1\x (6.3 s) | giết thật |
| K4b_chi_bao_ve_stdout — chỉ bảo vệ stdout | t64_ | `GIET_DUNG_NHAN` (k4) fd 2 đóng ⇒ nổ trước khi phóng lại: rc=1 b'' (5.8 s) | giết thật |
| M61f_bo_hasattr — bỏ hasattr | t61_ | `GIET_DUNG_NHAN` (f) luồng KHÔNG có `reconfigure` làm `_ep_utf8` ném: rc=0 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe1\xbb\xaf Vi\xe1\xbb\x87t\n (6.8 s) | giết thật |
| T_K4_go_va_K4 — GỠ chốt (k4) + K4 | t64_ | `SONG`  (4.8 s) | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| R3_sys_argv — `sys.argv` thay orig_argv | t62_ | `GIET_DUNG_NHAN` (2) cờ `-B` mất ở lần phóng lại: 'UTF8_MODE=1 B=0 DA_PHONG_LAI=1 DAU_SOT=0' (3.8 s) | giết thật |
| R6_bo_da_phong_lai_or — bỏ `_DA_PHONG_LAI or` | t62_ | `GIET_DUNG_NHAN` (5) đã mang dấu phóng lại mà vẫn ngoài UTF-8 phải DỪNG, không phóng tiếp: rc=5 'UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0 (8.3 s) | giết thật |
| R9_khong_dat_dau — không đặt dấu | t62_ | `GIET_DUNG_NHAN` (4) gọi `-X utf8=0` mà không ra UTF-8 (giữ `-B`) sau đúng MỘT lần phóng: rc=5 'UTF8_MODE=1 B=1 DA_PHONG_LAI=0 DAU_SOT=0' (6.6 s) | giết thật |
| C1_go_khoi_CUA — gỡ cửa khỏi `_CUA` | t62_ | `TIN_DUNG_GIA` giàn giáo hỏng (chưa tới chốt nghiệp vụ): cửa --tu-kiem-che-do-utf8 không in gì: rc=2 'cklink phải còn marker.\n/tmp/cla (4.2 s) | tín dụng giả — kỳ vọng (fail-closed: suite ĐỎ) |
| M61b_go_env_con — gỡ env cho con (§6.3 ii) | t61_ | `GIET_DUNG_NHAN` (b) cháu (không `env=`) không in được byte UTF-8 thật: rc=0 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe1\xbb\xaf Vi\xe1\xbb\x87t (4.0 s) | giết thật |
| M61e_ascii_br — con `ascii:backslashreplace` | t61_ | `GIET_DUNG_NHAN` (b) cháu (không `env=`) không in được byte UTF-8 thật: rc=0 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe1\xbb\xaf Vi\xe1\xbb\x87t (3.8 s) | giết thật |
| R11_mat_argv — bỏ `*sys.orig_argv[1:]` khi phóng lại | t64_ | `TIN_DUNG_GIA` giàn giáo hỏng (chưa tới chốt nghiệp vụ): giàn giáo: phần đầu không phóng lại sang UTF-8 — không đo gì: '' (126.0 s) | ĐỎ có tên (giàn giáo) sau ~120 s — không treo (vá T64-TREO có răng); xem lô 2 R11_HEN_go |
| R1_if_false — khối phóng lại `if False` | t62_ | `GIET_DUNG_NHAN` chạy làm __main__ với PYTHONUTF8=0 mà tiến trình chạy bộ ca KHÔNG ở chế độ UTF-8: 'UTF8_MODE=0 B=1 DA_PHONG_LAI=0 DAU_SO (3.7 s) | giết thật |
| R5_bo_X_utf8 — bỏ `-X utf8` | t62_ | `GIET_DUNG_NHAN` (4) gọi `-X utf8=0` mà không ra UTF-8 (giữ `-B`) sau đúng MỘT lần phóng: rc=1 '' 'cong_cu_test: KHONG_PHONG_LAI — đã phó (5.6 s) | giết thật |
| R8_bo_main — bỏ `__name__ == "__main__"` | t61_ | `GIET_DUNG_NHAN` (e) NẠP cong_cu_test.py mà người nạp bị PHÓNG LẠI — chốt `__main__` mất: rc=0 stdout=b'(0) nap\n(0) nap\nNAP_OK\n(a) ch\ (3.8 s) | giết thật |
| C2_cua_thoat0 — cửa UTF-8 thoát 0 | t62_ | `GIET_DUNG_NHAN` (1) mã thoát KHÔNG đi qua lần phóng lại: rc=0, chờ 5 (3.2 s) | giết thật |
| M61a_go_reconfigure — gỡ reconfigure | t61_ | `GIET_DUNG_NHAN` (a) stdout của tiến trình nạp không mang chữ Việt UTF-8: rc=1 stdout=b'(0) nap\nNAP_OK\n' stderr=b'g con \\u0111ang ghi, (3.2 s) | giết thật |
| M61d_bo_PYTHONUTF8 — bỏ PYTHONUTF8 | t61_ | `GIET_DUNG_NHAN` (d) cháu phải ở UTF-8 mode, PYTHONUTF8=1, PYTHONIOENCODING=utf-8: rc=0 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe1\xbb\xaf Vi\x (3.1 s) | giết thật |
| M61g_strict — `errors=strict` | t61_ | `GIET_DUNG_NHAN` (g) in surrogate lạc phải ra chữ thoát, không ném: rc=1 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe1\xbb\xaf Vi\xe1\xbb\x87t\n(b (3.4 s) | giết thật |

**Lô 2** (`tam/log/db-l7b.jsonl`, xong 12:06:39Z):

| đột biến | ca đích | kết quả — tín hiệu | phân loại |
|---|---|---|---|
| K4d — POSIX: `if sys.stdout is None or sys.stderr is None: return 0` (THOÁT 0, KHÔNG phóng, KHÔNG chạy bộ ca) | t64_ | `SONG` (10,2 s) | **SỐNG SÓT — chốt (k4) chỉ đo `rc==0`**, không đo "phần đầu VẪN phóng" như chú thích `:3041` khai ⇒ finding TU-PHONG-LAI-KHONG-TRONG-SUOT (e) |
| BH_moi_ngu02 — thứ tự MỚI + `sleep(0.2)` giữa ghi thành viên và `set()` | t64_ | `SONG` (11,4 s) | sống — KỲ VỌNG (thứ tự mới chịu được cửa sổ nới) |
| BH_cu_ngu02 — `set()` TRƯỚC ghi thành viên + `sleep(0.2)` (thứ tự lượt 6) | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={…{'co': 8192, 'tv': {'cha', <Popen … -9>}}} | giết thật (thứ tự cũ thua đúng cửa sổ) |
| R11_HEN_go — R11 + KHÔNG `start()` Timer | t64_ | `TREO` (bị giết ở 260 s) | sống-treo KỲ VỌNG — chứng minh chính Timer biến treo thành đỏ (R11 có Timer: đỏ ở 126 s) |
| M49a — bỏ `oid.returncode` | t63_ | `GIET_DUNG_NHAN` (hash-object/rc) … chờ 'rc=128/0' | giết thật |
| M49d — `if ga.returncode:` → `if False:` | t63_ | `GIET_DUNG_NHAN` (add/rc) … chờ 'bình_thường' | giết thật |
| NT_mat_doi_so — nt: `popen(lenh[:1], …)` (mất đối số), stdin DEVNULL | t64_ | `GIET_DUNG_NHAN` (w2) … rc=0 | giết thật KHI stdin là DEVNULL — **stdin là ống còn mở ⇒ TREO** (HƯỚNG 8) |
| SEGV — sản phẩm đưa `ctypes.sizeof(gh)` vào chỗ con trỏ | t64_ | `KHAC` rc=**-11** (SIGSEGV cả tiến trình test, 0 dòng kết quả) | fail-closed nhưng MẤT chẩn đoán — Windows thật trả FALSE (nhân kiểm con trỏ) ⇒ CANH_BAO; finding DO-GIA-DOC-DIA-CHI-TUY-Y |
| M1R11 — kép: POSIX `subprocess.run` thay execve (≙ Windows Job hỏng/CANH_BAO) + mất argv | t64_ | `TREO` (300 s) | **SỐNG-TREO — đường (3) của T64-TREO**: Timer chỉ giết bao, cháu REPL giữ ống; cây HINT (Timer giết + đóng stdin) ⇒ `TIN_DUNG_GIA` giàn giáo 121,6 s |
| T64_bo_preexec — bỏ `preexec_fn=mac_dinh`, chạy dưới `trap '' INT` (×5) / tiền cảnh (×2) | t64_ | 5/5 `GIET_DUNG_NHAN` (k3) "LỜ SIGINT … INT=0" / 2/2 `SONG` | kiểm lời khai docstring "bỏ `preexec_fn` thì LUÔN đỏ oan (chạy nền)" — khớp |

## BẢNG ĐO
| khẳng định | executor khai | đo được | khớp? |
|---|---|---|---|
| dòng thêm so `fc852ff` (trần ~420) | +417/−42 (commit + BAO_CAO) | `git diff --numstat fc852ff 302a15d` ⇒ `1 1 ops/bash_nen.py` + `416 41 ops/cong_cu_test.py` = **+417/−42** | khớp |
| PR so master chỉ 2 tệp | có | `--name-only` ⇒ `ops/bash_nen.py`, `ops/cong_cu_test.py`; merge-base = `fc852ff` | khớp |
| vá 7 so `0ce1ad3` | +45/−28 (BAO_CAO) | myers/minimal (mặc định git) **+47/−30**; histogram/patience **+45/−28** — cùng net +17, khác cách ghép dòng | khớp (theo histogram; khai thiếu thuật toán) |
| sha256 `cong_cu_test.py` đã vá | `467248e8…` | `467248e89ae0c1b7179299f6cb3a9ac979ba1ed147e7b6b0abd63700d06410e5` = tệp ở `302a15d` | khớp |
| vá 7 chỉ đổi `_k32_gia`, `_phong_lai`, `t64` (+ chú thích) | (ngầm) | so AST từng định nghĩa cấp module `0ce1ad3`→`302a15d` (bỏ docstring): code KHÁC đúng 3 = `_k32_gia`, `_phong_lai`, `t64`; 225/225 định nghĩa; `t49` chỉ đổi CHÚ THÍCH | khớp |
| 9 ca giao `t49 t52 t53 t54 t60–t64` (a) 9/9, (b) 9/9, 0 `.pyc` | có | `chay_ca.py` trên h: (a) `TONG {"qua": 9}`, (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` `TONG {"qua": 9}`; 0 `.pyc`; `status --ignored` rỗng | khớp |
| vòng ca 16 mảnh "60/60 đạt" | có (commit) | 16/16 mảnh tự chạy @`302a15d`: `cong_cu_test: 60/60 đạt; tổng=61, bỏ qua=1, tiền kiểm bỏ qua=0` | khớp (log điều phối ở 16 HEAD lạ — xem HƯỚNG 12; số này là của lượt này @`302a15d`) |
| giãn mã không đổi hành vi (iv) | có | `tam/cu/ab_phong_lai.py`: `_phong_lai` l6 vs h dưới CẢ HAI đồ giả (cũ/mới) × {bình thường, hỏng Create/Set/Assign, thiếu WinDLL} + posix ⇒ 11/13 GIỐNG từng trường (rc, stderr nguyên văn, số con, job/cờ/thành viên); KHÁC đúng 2 = `sys.stdout`/`sys.stderr` `None` (l6 ném `AttributeError`, h exec) — chính là vá (d) | khớp |
| `;`/dòng dài ở dòng thêm | "Token `;` trong vùng sửa: về 0" | `tokenize` trên dòng thêm vá 7: `;` = 0 (khớp). Toàn PR: dòng thêm > 118 ký tự 29 → 26, `;` 11 → 9, walrus 5 → 6, **max 143 → 154** (vá 7 THÊM 9 dòng > 118, dài nhất `:3012` docstring `t64` 154 ký tự) | khớp phần khai; giãn chưa trọn |
| compile `-W error` 3.11.15/3.12.3/3.13.12 sạch | có | `bash_nen.py` + `cong_cu_test.py` ×3 phiên bản: "sach" ×6 | khớp |
| ruff 0.15.15 `--select F` = nền | có | `--no-cache --isolated` (cài `pip --target tam/ruff`): tập `fc852ff` = `0ce1ad3` = `302a15d` = {`bash_nen.py` F401 `ast`; `cong_cu_test.py` F841 `ci`} (so sau khi bỏ số dòng/cột); 0 `.ruff_cache` | khớp |
| docstring `_tach_dinh_dang` không đổi byte (spec §2A) | — | `ast.get_docstring(clean=False)` sha256 `3bc957a67247801b…`, 897 ký tự ở `fc852ff` = `0ce1ad3` = `302a15d` | đạt |
| spec §6.3 (i) docstring raw → không raw ⇒ ca khoá ĐỎ bằng tín hiệu của chính nó | — | M60a trên TRỌN 61 ca (env a): `t60` `giet_that` "(1) … SyntaxError: invalid escape sequence '\(' (bash_nen.py, line 898)", 59 qua, `t2` bỏ qua (môi trường) ⇒ bán kính 1/61 | đạt (Linux) |
| spec §6.3 (ii) gỡ ép UTF-8 cho con ⇒ ca khoá UTF-8 ĐỎ, bán kính 1/N | — | M61b trên TRỌN 61 ca (env a): chỉ `t61` `giet_that` "(b) cháu (không `env=`) không in được byte UTF-8 thật", 59 qua, `t2` bỏ qua ⇒ **1/61** | đạt (Linux) |
| bảng đột biến P3 trong BAO_CAO (N_B, N_H, W6, W5size chết (w1); N_A, N_C, W5f, W10 sống) | có | lô 1: đúng từng dòng (N_B ⇒ `ArgumentError … wrong type`; N_H ⇒ `co: 0`; W6 ⇒ (w1); W5size ⇒ (w1); N_A/N_C/W5f/W10 `SONG`) | khớp |
| "regress trạng thái W1→(w1), W2→(w1), W7→(w2), M1→(k1)" | có | lô 1: W1/W2 (w1), W7 (w2), M1 (k1) | khớp |
| BAO-HIEU: nới 0,2 s — thứ tự cũ đỏ, mới xanh | có | lô 2: BH_cu_ngu02 ⇒ (w1); BH_moi_ngu02 ⇒ `SONG` | khớp |
| (d): hoàn nguyên ⇒ (k4) fd 1; chỉ stdout ⇒ (k4) fd 2 | có | K4 ⇒ `(k4) fd 1 … AttributeError`; K4b ⇒ `(k4) fd 2 … rc=1`; K4c ⇒ `(k4) fd 1` | khớp |
| "(k4) … phần đầu VẪN phóng ⇒ rc=0" | có | K4d (thoát 0 không phóng) ⇒ `SONG` — rc=0 không chứng minh đã phóng | **không khớp** (P3) |
| R11 ⇒ `tin_dung_gia` ~120 s, 0 sót | có | R11 ⇒ `TIN_DUNG_GIA` "giàn giáo … ''" 126,0 s (cây HINT 125,1 s); R11_HEN_go ⇒ TREO 260 s | khớp |
| "readline() là phép chờ DUY NHẤT không hạn" | có (DUONG_VAO, BAO_CAO) | nt `wait()` ở (w2) treo khi stdin mở (faulthandler `:3061 → :71`) | **không khớp** (P4) |
| `t64` lặp "22/22 + 6/6 + 4/4 = 32/32" | có | 30/30 thường + 30/30 SIG_IGN, 2,89–4,4 s dưới tải 17,5–18,4, sót 0/60 | khớp (chiều) |
| **trọn bộ dạng MẢNH như CI, env (a)** — 8 mảnh THẬT @`302a15d` (`PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 CONG_CU_TEST_MANH=k/8 CONG_CU_TEST_MANH_RA=manh/manh-k.txt CONG_CU_TEST_TIEN_TRINH=1`), clone riêng `tam/ma/s{k}`, SONG SONG 11:40:10Z→13:32:24Z | thân commit: "16/16 mảnh pha ca 60/60 … bán kính 415/416 ok mỗi env, còn lại t2_go_canary KHÔNG ĐO ĐƯỢC" | mảnh 0,2–7: RC=0 · vòng CA `60/60 đạt; tổng=61, bỏ qua=1` · `52/52 đột biến bán kính 1` · ghi `manh/manh-k.txt`; mảnh 1: RC=1 · 51 `ok` + `KHÔNG_ĐO_ĐƯỢC t2_go_canary` (thiếu `jsonschema`) ⇒ `[M-loi]`, không ghi tệp. **415 `ok … bán kính 1/61` · 1 KHÔNG ĐO ĐƯỢC · 0 ĐỎ**; 6647–6734 s dưới tải 16–22; 0 `.pyc`; status chỉ `?? manh/`; 0 `rc=141` | khớp |
| **trọn bộ dạng MẢNH, env (b)** `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` — qua `__main__` ⇒ execve THẬT ở mỗi mảnh, `tam/mb/s{k}` | (như trên) | y hệt (a): 7 mảnh RC=0 52/52; mảnh 1 RC=1 chỉ vì `t2_go_canary` (môi trường); **415 `ok … 1/61` · 1 KHÔNG ĐO ĐƯỢC · 0 ĐỎ** | khớp |
| ca mới `t60`–`t64` không kéo rộng bán kính (tín dụng giả) | (ngầm) | 0/830 dòng bán kính (a)+(b) nhắc `t60`–`t64`; mọi `ok` đều `1/61` | đạt |
| bán kính #668 `f25_cua_moi_vi_tri`/`f13`/`f27_entry_drop`/`f28_gate_di_tat` ⇒ 1/61 | có | từ mảnh (a): `f25_cua_moi_vi_tri`, `f25_bo_chot_doi_so_la`, `f13_dispatcher_nuot` ⇒ `t52` · 1/61; `f27_entry_drop`, `f27_entry_rc`, `f28_gate_di_tat`, `f28_can_cau_hinh`, `f28_du_nuot_ma`, `f28_nen_ma` ⇒ `t54` · 1/61 (9/9) | khớp |
| delta lỗi đột biến so NỀN (spec §6.1 "≤ 0", Linux) | "delta lỗi đột biến so nền = 0" | head: 1 (`t2_go_canary`, môi trường) mỗi env; nền `fc852ff` cùng máy: `mot_db t2_go_canary` ⇒ `KHÔNG_ĐO_ĐƯỢC … loi=1 n_ca=56` (cùng nguyên nhân); mọi đột biến còn lại `ok` ⇒ **delta = 0** | khớp |
| gom 7 tệp (thiếu mảnh 1) như job `gate-cong-cu-gop` (`python3.12 ops/cong_cu_test.py --gop manh`, clone sạch @`302a15d`, env (a) và (b) — (b) qua execve, argv `--gop manh` giữ nguyên) | — | cả hai: `ĐỎ  gom [G-tap]: tập mảnh [0, 2, 3, 4, 5, 6, 7] ≠ 0..7`, RC=1 — fail-closed đúng thiết kế | — |
| CI `gate` (`CONG_CU_TEST_BAN_KINH=manh`) @`302a15d` — env (a) CI và env (b) qua execve (clone `tam/ga`, `tam/gb`) | (không ai khai) | (a) RC=0 · `60/60 đạt; tổng=61, bỏ qua=1` · CỔNG TRÊN CÂY THẬT: ĐẠT (nguon_tep=git, nguon_noi_dung=blob-index) · TỰ KIỂM SONG SONG (N126): ĐẠT · `SỐ LIỆU: ca=61 · đột biến=416 (giao mảnh) · lỗi đột biến=0 · cổng cây thật=ĐẠT` · 302 s · 0 `.pyc` · status sạch; (b) y hệt, 302 s | — |
| mảnh 1 chạy lại bằng venv (`--system-site-packages` + `jsonschema==4.26.0` đúng pin `ci.yml`, venv đầu PATH), (a) và (b) — (b) qua execve giữ python của venv; clone `tam/mv{a,b}` @`302a15d` | — | vòng CA **`61/61 đạt; tổng=61, bỏ qua=0`** (t2 nay ĐO được) · `52/52 đột biến bán kính 1` kể cả `t2_go_canary → giết đúng 't2_canary_thieu_shellcheck_phai_SUY_GIAM' · bán kính 1/61` · ghi `manh/manh-1.txt` · RC=0 · 1863 s / 1860 s · 0 `.pyc` | — |
| **GOM 8/8** như job `gate-cong-cu-gop` (clone sạch @`302a15d`, `python3.12 ops/cong_cu_test.py --gop manh`; 7 tệp mảnh gốc + `manh-1.txt` bản venv; mọi tệp mang `head=302a15d…`, `sha256_test=467248e8…` — KHAI: CI chạy cả 8 mảnh có `jsonschema`) | — | env (a): RC=0 · `GOM MẢNH 8/8` · **416/416 `ok … bán kính 1/61`** · 0 ĐỎ · `SỐ LIỆU GOM: ca=61 · đột biến=416 · lỗi đột biến=0`; env (b) qua execve: y hệt, RC=0 · 0 `.pyc` | **đạt** (spec §6.5 mô phỏng cục bộ) |

## FINDINGS

### TU-PHONG-LAI-KHONG-TRONG-SUOT  [P3]  (biểu hiện (e), MỚI ở vá 7) Chốt (k4) chỉ đo `rc == 0` — đột biến "THOÁT 0, không phóng, không chạy ca nào" khi stdout/stderr đóng SỐNG; chú thích khai "phần đầu VẪN phóng"
TỆP/DÒNG: `ops/cong_cu_test.py:3041-3044` (`for fd in (1, 2) …  # (k4) … phần đầu VẪN phóng` · `bang(r.returncode == 0, …)`); `dau.py` dựng ở
`:3020-3022` in dấu `PID=… U8=… PL=…` CHỈ ra stdout; lời khai: BAO_CAO §"P4 — TU-PHONG-LAI (d) ⇒ ĐÓNG (POSIX)" + DUONG_VAO D1/D2 "phần đầu
VẪN phóng ⇒ rc=0".
VẤN ĐỀ: biểu hiện (d) của lượt 6 (fd 1/2 đóng ⇒ `AttributeError` trước khi phóng) ĐÃ VÁ THẬT — K4 (hoàn nguyên) ⇒ `(k4) fd 1`, K4b (chỉ bảo vệ
stdout) ⇒ `(k4) fd 2`, K4c (bỏ guard) ⇒ `(k4) fd 1`; gỡ (k4) + K4 ⇒ sống (chốt là thứ DUY NHẤT bắt). Nhưng khoá mới đo "không nổ" chứ không đo
"đã phóng": K4d (POSIX `if sys.stdout is None or sys.stderr is None: return 0` ⇒ `sys.exit(0)` — bộ ca không phóng, KHÔNG chạy ca nào) ⇒
`t64` **SỐNG** (lô 2), và cả bộ ca (luồng mở) không đổi ⇒ sống qua trọn suite. Đúng hình CLAUDE.md "cổng xanh nhờ rc=0 là cổng có thể bị lừa":
người gọi đóng stdio thì rc là tín hiệu DUY NHẤT họ còn, và đột biến này biến nó thành xanh giả. Tài liệu (chú thích `:3041`, BAO_CAO) khai
một tính chất phép đo không đo ⇒ P3 (lời khai lệch phép đo); hệ quả thật cần một hồi quy tương lai + stdio đóng.
VÁ Ở ĐÂU: `t64` (mã TEST — HINT mức mã đầy đủ). Sản phẩm `_phong_lai` KHÔNG cần đổi.
VÁ THẾ NÀO: (1) `dau.py` in dấu ra luồng CÒN MỞ: `print(…, flush=True, file=sys.stdout or sys.stderr)` (k1–k3 không đổi vì stdout mở);
(2) (k4) đòi bằng chứng DƯƠNG: `bang(r.returncode == 0 and b"U8=1 PL=1" in r.stdout + r.stderr, …)` — fd 1 đóng ⇒ dấu ở stderr, fd 2 đóng ⇒ ở stdout.
Đo trực tiếp `dau.py` (k4): head — fd 1 đóng ⇒ rc 0, stdout `b''`, stderr `b''` (KHÔNG còn dấu nào để đọc); fd 2 đóng ⇒ dấu ở stdout
nhưng (k4) không đọc. Cây HINT — fd 1 đóng ⇒ stderr `b'PID=… U8=1 PL=1 INT=1\n'`; fd 2 đóng ⇒ stdout `b'PID=… U8=1 PL=1 INT=1\n'`.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t64` (k4). Sau vá: K4d ⇒ `(k4) fd 1 đóng ⇒ không phóng lại tới bộ ca: rc=0 …`; K4/K4b/K4c vẫn chết đúng
`(k4) fd 1`/`fd 2`; W14 (bỏ hẳn xả đệm) vẫn SỐNG (tương đương thật); head chưa đột biến ⇒ `qua`.
BẢN VÁ CÓ THỂ ĐẺ RA: (a) +1 dòng (⇒ +418/420); (b) nếu một nền in cảnh báo khởi động ra luồng còn mở thì dấu vẫn có mặt (chốt dò chuỗi con) —
không đỏ oan; (c) (k4) vẫn chỉ POSIX — Windows KHÔNG ĐO ĐƯỢC (nhánh `sys.stderr is not None` của `except` nt chưa có ca nào).
HINT (hunk nào): hunk 4 (`@@ -3018`, `dau.py`) + hunk 5 (`@@ -3041`, chốt (k4)).
ĐÃ THỬ NGHIỆM HINT: xem "HINT.patch — tự kiểm".
ĐỘ TIN: cao (K4d sống trên head, đo; hai chiều trên cây HINT ở mục tự kiểm).

### CA-KHOA-T64-TREO-THAY-VI-DO  [P4]  (đóng MỘT PHẦN) Hai đường treo còn mở: (2) nhánh nt `popen(…).wait()` không hạn + con kế thừa stdin; (3) Timer chỉ `p.kill()` bao — bản phóng lại là tiến trình RIÊNG (Windows Job hỏng ≙ POSIX M1) mà treo thì vẫn TREO; lời khai "readline là phép chờ DUY NHẤT không hạn" sai
TỆP/DÒNG: `ops/cong_cu_test.py:2994` (`_k32_gia.popen`: `subprocess.Popen(lenh, **kw)` — con kế thừa stdin), `:71` (`return popen(lenh,
env=env).wait()` — chờ không hạn, đúng cho SẢN PHẨM), `:3061` (vòng (w2) gọi `phong` trên LUỒNG CHÍNH, không bọc hạn chót); lời khai:
DUONG_VAO §T64-TREO "Rà hết: … ĐỀU có hạn; CHỈ `p.stdout.readline()` (dòng đầu) KHÔNG hạn", BAO_CAO "phép chờ DUY NHẤT không hạn".
VẤN ĐỀ: hunk của lượt 6 đã vá đúng đường được chỉ — R11 nay ĐỎ có tên ở 126 s; gỡ `start()` Timer (R11_HEN_go) ⇒ TREO tới 260 s (Timer có
răng). Nhưng đường cùng lớp ở nhánh nt còn mở (HƯỚNG 7): đột biến `popen(lenh[:1], …)` (mất đối số ⇒ REPL) — stdin `/dev/null` ⇒ (w2) đỏ 3 s;
stdin là ống còn mở (≙ chạy TAY trong terminal) ⇒ KHÔNG dòng kết quả, ngăn xếp faulthandler ở 90 s: `t64:3061 → _phong_lai:71 → wait()`.
Bán kính CI không chạm (worker `stdin=DEVNULL`, 0 DOT_BIEN nhắm phần đầu tệp) — đường của người chạy tay, đúng thứ `t64` sinh ra để chẩn đoán.
Đường (3), đo: đột biến kép M1+R11 (POSIX `subprocess.run` thay execve ≙ đường Windows khi Job hỏng/CANH_BAO + mất argv) trên head ⇒ TREO tới
300 s: Timer giết bao (`p.pid`), cháu REPL vẫn giữ stdout và đọc stdin (ống của harness còn mở) ⇒ `readline()` không trở về. Timer giết bao VÀ
đóng `p.stdin` (cây HINT) ⇒ `tin_dung_gia` "giàn giáo … ''" sau 121,6 s. Trên Windows có Job, giết bao đóng job ⇒ đủ; KHÔNG ĐO ĐƯỢC ở đây.
VÁ Ở ĐÂU: `_k32_gia.popen` + Timer của `t64` (mã TEST — đầy đủ). VÁ THẾ NÀO: (2) `subprocess.Popen(lenh, **{"stdin": subprocess.DEVNULL, **kw})` —
con của đồ giả nhận EOF thay vì terminal; (3) `threading.Timer(120, lambda: p.kill() or p.stdin.close())`; cả hai trung hoà dòng. (Không đổi sản phẩm: `wait()` không hạn là ĐÚNG cho bao chờ bộ ca.) Sửa lời khai: không còn
"DUY NHẤT".
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t64` (w2)/giàn giáo. Sau vá: NT_mat_doi_so + stdin là FIFO mở ⇒ `giet_that (w2)` sau 3 s (head: treo); M1+R11 ⇒
ĐỎ có tên ~120 s (head: treo); R11 vẫn ĐỎ có tên; (w1)/(w2) của mọi đột biến lô 1 giữ nhãn (xem tự kiểm HINT).
BẢN VÁ CÓ THỂ ĐẺ RA: con (w1) `sleep(60)` và (w2) `SystemExit(7)` không đọc stdin ⇒ không đổi hành vi; một hồi quy làm con NGỦ (không đọc stdin)
vẫn bị giới hạn bởi `th.join(60)` + `[p.kill() …]` ở (w1) nhưng KHÔNG ở (w2) — còn lại, ghi rõ.
HINT (hunk nào): hunk 3 (`@@ -2984`, dòng `popen`) + hunk 4 (dòng Timer). ĐỘ TIN: cao (ngăn xếp + A/B cùng FIFO; M1+R11 A/B).

### DO-GIA-DOC-DIA-CHI-TUY-Y  [P4]  (MỚI, sinh từ đồ giả vá 7) `dat` đọc `ctypes.string_at(p + 16, 4)` tại địa chỉ bất kỳ — đột biến đưa SỐ vào chỗ con trỏ ⇒ SIGSEGV CẢ tiến trình test thay vì FALSE như nhân Windows
TỆP/DÒNG: `ops/cong_cu_test.py:2987-2990` (`dat`: `ok = … and p and n == …` rồi `string_at(p + 16, 4)`).
VẤN ĐỀ: đồ giả nay đúng ở tầng chuyển kiểu (lớp lượt 6 đã đóng) nhưng tin MỌI địa chỉ. Đột biến SEGV (`SetInformationJobObject(job, 9,
ctypes.sizeof(gh), ctypes.sizeof(gh))` — argtypes `vp` nhận số 144) ⇒ `string_at(160, 4)` ⇒ rc=-11, 0 dòng kết quả (lô 2). Trên Windows thật
nhân kiểm con trỏ người dùng ⇒ API trả FALSE (ERROR_NOACCESS) ⇒ CANH_BAO ⇒ (k1)/(w1) đỏ CÓ TÊN. Trong CI một SIGSEGV giữa `t64` giết cả vòng
ca (mất mọi dòng báo); ở bán kính, worker chết ⇒ "tiến trình con KHÔNG trả kết quả hợp lệ". Fail-closed nhưng mất chẩn đoán ⇒ P4.
VÁ Ở ĐÂU: `_k32_gia.dat` (mã TEST — đầy đủ). VÁ THẾ NÀO: `(p or 0) >= 1 << 16` thay `p` — 64 KiB thấp không bao giờ được ánh xạ (Windows dành
sẵn; Linux `vm.mmap_min_addr` mặc định 65536) ⇒ số/kích thước/handle nhỏ bị trả FALSE như nhân; địa chỉ thật của struct luôn lớn hơn.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t64` (w1). Sau vá: SEGV ⇒ `giet_that (w1) … CANH_BAO_MO_COI … (OSError …)` (đo trên bản sao lẻ VÀ trên cây
HINT v3 trong lô đầy đủ); N_B/N_H/W5b/OFS giữ nhãn (w1); head ⇒ `qua`.
BẢN VÁ CÓ THỂ ĐẺ RA: địa chỉ hoang LỚN (vd. `id(gh)`) vẫn đọc được bộ nhớ hợp lệ ⇒ không SIGSEGV, cờ rác ⇒ (w1) — ổn; không chặn được địa chỉ lớn
chưa ánh xạ (hiếm ở đột biến). Trung hoà dòng.
HINT (hunk nào): hunk 3 (`@@ -2984`, dòng `def dat` + `ok =`). ĐỘ TIN: cao (rc=-11 đo; chốt trên cây HINT ⇒ (w1)).

### LOI-KHAI-RONG-HON-PHEP-DO  [P4]  (phần SỐ ĐẾM đã vá thật; còn một biểu hiện DẠNG) Chú thích `:15-16` "ĐÃ ĐO (AST…): giá trị là …" thiếu dạng `dict({k: v … os.environ.items() …}, …)` của `t64`
TỆP/DÒNG: `ops/cong_cu_test.py:15-16`; dạng thiếu ở `:3017` (dùng tại `:3024`, `:3042` mới).
VẤN ĐỀ: vá 7 bỏ đúng số đếm — và phép đo xác nhận số ấy SẼ trôi lần nữa: AST `env=` 39 (`0ce1ad3`) → 40 (`302a15d`, thêm (k4)). Rà mọi chữ
số trong chú thích/docstring trên dòng thêm: 0 số đếm trôi được (HƯỚNG 11). Nhưng câu "giá trị là A, B, C, hoặc biến truy về các dạng ấy" vẫn
là lời khai ĐÃ ĐO, và `env` của `t64` truy về dạng thứ tư (dict comprehension lọc `os.environ.items()`), không thuộc danh sách.
Kèm (MỚI ở vá 7): docstring `_k32_gia` `:2975` "thiếu/lệch `byref` thì lỗi ở BIÊN" — đo N_H (`byref(gh, 16)`): QUA biên ctypes (stderr rỗng, không
CANH_BAO), bị bắt bởi TRẠNG THÁI (`co: 0`); chỉ "thiếu byref" (N_B) mới lỗi ở biên (`ArgumentError`).
VÁ Ở ĐÂU/THẾ NÀO: chú thích (hunk 1) thêm dạng ấy; docstring (hunk 2) tách "thiếu byref ⇒ lỗi ở BIÊN" / "lệch byref ⇒ đọc cờ sai chỗ"; trung hoà
dòng. CA KHOÁ: không (chú thích). BẢN VÁ CÓ THỂ ĐẺ RA: không. HINT: hunk 1 + 2. ĐỘ TIN: cao.

### NGHIEM-THU-WINDOWS-CON-THIEU  [P2]  Chưa có nghiệm thu §6 trên Windows neo exact head — nhánh Job Object và (vá 7) nhánh `sys.stderr is not None` chưa từng chạy trên Windows; mô phỏng (4) vẫn ĐỎ OAN
TỆP/DÒNG: spec §2B, §6.1–6.3; `ops/cong_cu_test.py:53-71` (nhánh nt); `t63` (`:6389`).
VẤN ĐỀ: giữ (1)–(6) lượt 6 — không log/receipt Windows cho `302a15d` trong hiện vật; giả thuyết B chưa đo; mảnh/gom #668 trên Windows; (5) Job
Object + (MỚI) guard `sys.stderr is not None` chưa chạy trên Windows; (6) thời lượng `t64` trên Windows. (4) TÁI HIỆN trên `302a15d` (MÔ PHỎNG,
`tam/gitgia/git` bỏ bản ghi `\xff` khỏi `update-index --index-info`, in "Ignoring path", rc=0): `t49` ⇒ `bo_qua` (đúng spec §2B), `t63` ⇒
`giet_that` "(ops/no_cu.py/rc) … chờ 'no_cu'" — trên nền như thế bộ ca ĐỎ OAN. Hướng vá đã có từ lượt 5 (dò năng lực trong nhánh nt) nhưng
spec §2B/S2 đòi ĐO Windows trước.
VÁ Ở ĐÂU / THẾ NÀO: nghiệm thu trên máy Windows local neo head SAU khi vá (như lượt 6: N/N không đặt `PYTHONUTF8` — đi nhánh Job; cùng bộ với
`PYTHONIOENCODING=ascii PYTHONUTF8=0`; §6.3 (i)(ii); log staging `t49`; `t64` (k1) thật; `taskkill /F` tiến trình bao). CA KHOÁ: không áp dụng.
HINT: không hunk — KHÔNG vá được bằng mã ở Linux (chủ kho: "Chỉ chạy tại máy"). ĐỘ TIN: cao.

### TRAN-DONG-DAT-BANG-NEN  [P4]  (đóng MỘT PHẦN) Giãn mã có thật nhưng vá 7 thêm 9 dòng > 118 ký tự, dòng dài nhất PR 143 → 154 (docstring `t64:3012`)
TỆP/DÒNG: dòng thêm fc852ff→302a15d; `:3012` (154 ký tự), `:3011` (132), `:3026` (127), `:2997` (125), `:3041` (124).
VẤN ĐỀ: đo `tokenize` trên dòng thêm: `;` 11 → 9 (vá 7 thêm 0), dòng > 118 29 → 26, walrus 5 → 6 (Timer `hen :=`), max 143 → **154**.
BAO_CAO khai đúng phần giữ nén (`_GioiHan` một dòng, 4 lời gọi `api(...)`). Kho không có luật độ dài dòng (master sẵn nhiều dòng > 118) ⇒ quan
sát cho chủ kho. VÁ: chủ kho quyết; HINT KHÔNG giãn thêm (mọi hunk trung hoà trừ +1 của (k4)). ĐỘ TIN: cao (đo).

### TEN-CA-LECH-SPEC  [P4]  `t60`–`t64` thay `t52` của spec (quyết định chủ kho: khai ở PR)
`t52_import` 0 lần, `def t60_import_bash_nen_khong_in_gi_ra_stderr` 1 lần; `t64` ngoài spec r1. Thân PR KHÔNG ĐO ĐƯỢC. HINT: không.

## HINT.patch — tự kiểm

- Tệp: `out/HINT.patch` (**bản CUỐI v3**: 96 dòng, sha256 `425e8e448eb1084b7f0443dcc143eae4947965da688f5eb883c4e424a41afa77`) — 5 hunk, MỘT tệp
  `ops/cong_cu_test.py`, định dạng `git diff --no-prefix` (repo-relative, không `a/`/`b/`); đầu tệp mang nhãn §8 NGUYÊN VĂN ("chưa chạy trên cây
  thật — executor tự áp, tự đo, tự chịu trách nhiệm commit") + bảng phân loại hunk. MỌI hunk là mã TEST (`_k32_gia`, `t64`) hoặc CHÚ THÍCH/DOCSTRING
  ⇒ đủ điều kiện patch-as-hint cho packet `sensitive` (§8 (3)(a)); KHÔNG hunk nào chạm sản phẩm (`_ep_utf8`, `_phong_lai`, khối phóng lại, `main`,
  `_main_gop`, `_CUA`), `bash_nen.py`, `.github/workflows/**`. Ánh xạ: hunk 1+2 = LOI-KHAI [P4] (chú thích `env=` + docstring `_k32_gia`) · hunk 3 =
  DO-GIA-DOC-DIA-CHI-TUY-Y [P4] + CA-KHOA-T64-TREO đường 2 [P4] · hunk 4 = TU-PHONG-LAI (e) [P3] (`dau.py`) + CA-KHOA-T64-TREO đường 3 [P4] (Timer) ·
  hunk 5 = TU-PHONG-LAI (e) [P3] (chốt (k4)). NGHIEM-THU-WINDOWS [P2]: không hunk (không vá được bằng mã ở Linux).
- Lệnh tự kiểm BẮT BUỘC (nguyên văn prompt; `tam/ap` clone MỚI từ `kho.git`, chạy lại cho v3 lúc ~12:58Z):
  ```
  $ git clone -q kho.git tam/ap && git -C tam/ap checkout -q --detach 302a15d && cd tam/ap && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch
  checking file ops/cong_cu_test.py
  hint_dry_run_rc=0
  $ patch -p0 --fuzz=0 < ../../out/HINT.patch      ⇒ patching file ops/cong_cu_test.py · apply_rc=0 · 0 tệp .orig/.rej
  $ cmp ops/cong_cu_test.py ../hint/ops/cong_cu_test.py ⇒ trùng từng byte (sha256 tệp 701f1c554fc833c5…; commit nháp d831e32 trong tam/hint, không ký)
  $ git diff --numstat fc852ff -- ops/             ⇒ 1 1 ops/bash_nen.py · 417 41 ops/cong_cu_test.py ⇒ +418/−42 (≤ 420)
  ```
- TRẦN DÒNG: so head +12/−11; hunk 1–4 trung hoà; hunk 5 +1 ⇒ **+418** (≤ ~420 chủ kho; còn 2 dòng đệm). Dòng thêm dài nhất 142 ký tự (dòng gốc
  `:3021` đã 142 — chỉ đổi `)` → `,`); compile `-W error` sạch trên 3.11.15/3.12.3/3.13.12; ruff `--select F` trên cây áp = tập head = tập nền.
- Trên cây áp cuối (`tam/ap`): `t49 t52 t53 t54 t60`–`t64` ⇒ `TONG {"qua": 9}` ở (a) thường và (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`
  (bản v2; v3 chỉ đổi dòng Timer — lô dưới chạy trên v3); `t60`–`t64` × 3.11/3.13 env (b) `qua: 5`; 0 `.pyc`; `status` 1 dòng = chính `M ops/cong_cu_test.py`.
- Lô đột biến ĐẦY ĐỦ trên cây áp v3 (`tam/log/db-ap3.jsonl` + `db-ap3b.jsonl`, xong 13:13:06Z): 67 + 3 biến thể mỏ neo Timer. **61/61 đột biến dùng
  chung mỏ neo TRÙNG nhãn head** (mọi giết thật vẫn giết đúng nhãn; mọi tương đương vẫn sống; C1 tín dụng giả kỳ vọng; R11 ĐỎ có tên ở 125,6 s;
  BH_cu ⇒ (w1), BH_moi sống). **Đổi đúng chủ đích:** K4d `SONG` → `GIET_DUNG_NHAN` "(k4) fd 1 đóng ⇒ không phóng lại tới bộ ca: rc=0 b''"; SEGV `rc=-11`
  → `GIET_DUNG_NHAN` "(w1) … CANH_BAO_MO_COI … (OSError …)"; M1R11 `TREO` → `TIN_DUNG_GIA` giàn giáo 122,0 s. **Răng của Timer mới (đo trên v3):**
  không `start()` (T_HEN_go_ap3) ⇒ head sống; + R11 (R11_HEN_go_ap3) ⇒ TREO 330 s; Timer CŨ chỉ `p.kill` + M1R11 (M1R11_hen_cu_ap3) ⇒ TREO 330 s — tức
  phần `p.stdin.close()` là thứ biến đường (3) thành đỏ.
- Đường treo (2) trên cây áp: NT_mat_doi_so + stdin = FIFO giữ mở ⇒ `giet_that` (w2) sau 3 s (head: treo, ngăn xếp `:3061 → :71`).
- Job `gate` env (b) (`CONG_CU_TEST_BAN_KINH=manh`, qua `__main__` ⇒ execve) trên commit nháp HINT `d831e32` (= cây áp v3, cổng đọc INDEX ⇒
  thay đổi HINT được commit trong bản sao): RC=0 · `60/60 đạt; tổng=61, bỏ qua=1` · CỔNG TRÊN CÂY THẬT: ĐẠT · TỰ KIỂM SONG SONG (N126): ĐẠT ·
  `lỗi đột biến=0` · 302 s · 0 `.pyc` · status sạch.

- Kiểm lại lần cuối (~14:07Z, sau SNAPSHOT): đúng lệnh bắt buộc trên `tam/ap` dựng MỚI ⇒ `checking file ops/cong_cu_test.py` · `hint_dry_run_rc=0` · `apply_rc=0` · trùng từng byte cây HINT `d831e32` · +418/−42.

## KHÔNG ĐO ĐƯỢC

- **Mọi hành vi Windows**: Job Object THẬT (TerminateProcess cha ⇒ handle cuối đóng ⇒ con chết; job lồng dưới runner/`py.exe`; handle job không
  kế thừa), `t64` (k1) trên Windows, guard `sys.stderr is not None` của nhánh nt (vá 7) dưới `pythonw`, CFUNCTYPE/con trỏ trần của đồ giả trên
  Windows x64/x86, thời lượng `t64`/mảnh trên `windows-latest`, Git for Windows với tên `\xff`/`\` (spec §8). Đồ giả CHẶT HƠN Windows ở chỗ cắt
  HANDLE (handle nhân vừa 32 bit) — nên W6r/Rc chết trên đồ giả có thể là tương đương trên Windows thật; chặt hơn là fail-closed, ghi để khỏi
  đọc thành "Windows sẽ hỏng".
- **CI thật trên GitHub** (không gọi mạng): mọi kết luận mảnh/gom/gate là MÔ PHỎNG cục bộ đúng lệnh + env `ci.yml`. Khác runner: máy này KHÔNG có
  `jsonschema` hệ thống (bù bằng venv `jsonschema==4.26.0` đúng pin, chỉ cho lượt chạy lại mảnh 1), `shellcheck` vắng (không bắt buộc), `PyYAML`
  6.0.1 (CI 6.0.3); GitHub Actions cấp stdin gì cho bước `run` — KHÔNG ĐO ĐƯỢC (quyết định đường treo thứ hai có hiện trong CI hay chỉ khi chạy tay).
- **Lời khai mảnh của phiên điều phối**: 16 log ở 16 HEAD lạ, không băm tệp ⇒ không neo được vào `302a15d`; thay bằng phép đo của lượt này.
- **Thân PR #690 / handoff vòng 7**: ánh xạ tên ca, `hint_provenance` (hunk lượt 6 do executor áp), nguồn gốc fallback Opus 4.8 — người đẩy phải khai.
- **Model/effort thật của executor**: thân commit + prompt khai 283/285 lượt do `claude-opus-4-8` (fallback); BAO_CAO dừng giữa chừng (mục "ĐANG CHẠY").
  Lượt này không có modelUsage của phiên executor.
- **Ctypes callback (libffi closure) của đồ giả vá 7** trên nền chặn bộ nhớ ghi+thực thi (vd. SELinux `deny_execmem` với libffi cũ):
  có thể làm `t64` ĐỎ (`MemoryError`) — ubuntu/Windows runner không chặn; KHÔNG ĐO ĐƯỢC ở đây, không tính finding.
- **Snapshot**: chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Không lệnh nào của lượt này
  chạy bộ ca hay ghi trong `cay-kho`/`kho.git` (chỉ đọc: `git -C cay-kho …` với `GIT_OPTIONAL_LOCKS=0` từ lệnh thứ 3, `git clone kho.git`).
- **Sự cố rig trong lượt (khai)**: (1) lô 1 lần đầu clone mỗi đột biến dưới tải IO quá chậm (~70 MB/65 s) — dừng, đổi sang 3 khe clone sẵn; khi dừng,
  một `pkill -f` khớp CHÍNH lệnh shell đang chạy (cùng chuỗi trong dòng lệnh) và cắt lệnh ấy (rc=144) — không đột biến nào đã ghi kết quả, chạy lại
  từ đầu (11:53Z). (2) Phép thử "stdin là ống mở" lần 1 kết thúc bằng `pkill -f 'sleep 400'` tự khớp shell của nó (rc=144) SAU khi đã ghi `rc=137
  giay=400` — kết quả hợp lệ; lần 2 dùng FIFO + `kill <pid>` và faulthandler. (3) `status --porcelain --ignored` của khe 1 sau R3 = `!! ops/__pycache__/` (đột biến
  mất `-B` thật sự ghi `.pyc` — khe được xoá `__pycache__` trước mỗi đột biến kế; các đột biến khác: status rỗng).
