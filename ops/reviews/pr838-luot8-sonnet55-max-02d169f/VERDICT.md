verdict: changes_requested
reviewed_sha: 02d169f47e9c171d81b17447b93bb70c53f33dc1
provider: claude
role: reviewer
review_kind: advisory_review
model_reviewer_identity: claude-sonnet-5-5 (Sonnet 5.5, tự khai; điều phối đối chiếu modelUsage)
independent_from_executor_session: true
assurance: review_deferred
review_axes: [spec, standards_security]

> TRẠNG THÁI: HOÀN TẤT 2026-10-18T20:09Z (bắt đầu 18:43:07Z; ghi TĂNG DẦN suốt lượt). Kết luận: **changes_requested** — P0=0 · P1=1 · P2=1 (nghiệm thu Windows — vẫn MỞ, KHÔNG vá được ở Linux) · P3=0 · P4=5.
> Tóm tắt một dòng: vá 8 áp HINT v3 đúng (5 hunk), lớp (e)/T64-TREO/LOI-KHAI-dạng ĐÃ VÁ THẬT, NHƯNG đối chứng (0) mới của `t63` là **VÁ SINH LỖI MỚI**: đột biến sẵn có `bn_quet_theo_chuoi` (mảnh 3/8) từ bán kính 1/61 thành 2/61 ⇒ `gate-cong-cu` mảnh 3 RC=1 (chạy THẬT, `tam/log/manh3-a.log`). Bản sửa trung hoà dòng (+420/−42, KHÔNG thêm dòng) trong `out/HINT.patch`: dry-run rc=0 trên clone mới `02d169f`; 161 đột biến `bash_nen.py` (chỉ `bn_quet_theo_chuoi` đổi); gate (a)(b) `60/60` RC=0; mảnh 3/8 THẬT RC=0.
>
> **Việc kế tiếp (executor / chủ kho):** (1) áp `out/HINT.patch` (4 hunk, 1 tệp, trung hoà dòng ⇒ +420/−42; hunk 3 là cái chặn land) rồi chạy lại **đủ 8 mảnh + gom** (lượt này chỉ chạy THẬT mảnh 3/8; 7 mảnh còn lại thay bằng quét từng đột biến) — đừng dựa vào "`lỗi đột biến=0`" của chế độ gate (số GIAO);
> (2) nghiệm thu Windows [P2] là việc tại máy: đòi `t49 = qua` (không `bo_qua`), vì nếu cờ không đủ thì `t63` ĐỎ ở đối chứng (0); (3) khai ở thân PR: tên ca `t60`–`t64` lệch spec (quyết định chủ kho) và `hint_provenance` theo hunk (hint lượt 7 + handoff §2 + hint lượt này).
> Lượt này CÙNG provider ⇒ nhãn tối đa `same_provider_approved` và KHÔNG thay `human_audited` bắt buộc cho `sensitive`; verdict là `changes_requested` nên `assurance: review_deferred`.

## SNAPSHOT ĐẦU/CUỐI
Bắt đầu lượt: 2026-10-18T18:43:07Z (`bat_dau.txt`). PROMPT sha256 `3a3768e6d945e0ca7e63943d2ef17696726d8c1eb72d10dba687c74756741a37` (= `prompt.sha256`, đo lại KHỚP). SPEC sha256 đo lại
`18504ced1549cbe62816f067b6ed16f36c12292820c8204cb6085a9c39e80b88` — KHỚP. Máy: 4 lõi, 16 GB RAM; python3.12.3 (+3.11.15, 3.13.12); git 2.43.0; ruff 0.15.8 hệ thống + **0.15.15** (đúng pin CI; `pip download` PyPI → `--target tam/ruff`, `--no-cache-dir`);
PyYAML 6.0.1 (CI 6.0.3); có `actionlint`, `rg`; KHÔNG `jsonschema` (⇒ `t2` bỏ qua, môi trường), KHÔNG `shellcheck`. `TMPDIR=$R/tam/tmp`, `PYTHONDONTWRITEBYTECODE=1`.

| đối tượng | ĐẦU (18:44:01Z) | CUỐI |
|---|---|---|
| `cay-kho` HEAD / tree | `02d169f47e9c171d81b17447b93bb70c53f33dc1` / `64e11ec5a33193a324f2171dbd62e7f19d917676` | (20:04:58Z) `02d169f47e9c171d81b17447b93bb70c53f33dc1` / `64e11ec5a33193a324f2171dbd62e7f19d917676` — TRÙNG |
| `cay-kho` `status --porcelain --ignored` / diff / diff --cached | 0 dòng / 0 B / 0 B | 0 dòng / 0 B / 0 B — TRÙNG |
| `cay-kho` index (`ls-files -s` sha256) | `61ef1691f6fe68db…`; `.git/index` mtime 18:43:19.87Z (do bên dựng rig, sát đầu phiên) | `61ef1691f6fe68db…`; mtime 18:43:19.87Z — KHÔNG đổi (mọi `status` dùng `GIT_OPTIONAL_LOCKS=0`) |
| `cay-kho` `.pyc` / `.ruff_cache` / `__pycache__` | 0 / 0 / 0 | 0 / 0 / 0 |
| `kho.git` `for-each-ref` sha256 | `45e6fe9f8c97f4a2…` | `45e6fe9f8c97f4a2…` — TRÙNG |
| `~/.gitconfig` | `75239ed3763a89e3…`, mtime 17:14:04Z (trước phiên) | `75239ed3763a89e3…`, mtime 17:14:04Z — TRÙNG |

Mọi lệnh đọc `cay-kho` dùng `git -C cay-kho …` (có `GIT_OPTIONAL_LOCKS=0` cho `status`); không lệnh nào chạy bộ ca hay ghi trong `cay-kho`/`kho.git`. `cmp cay-kho/ops/{cong_cu_test,bash_nen}.py tam/nen/ops/…` ở cuối phiên: TRÙNG.
Giới hạn snapshot: chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Hiện vật đầu vào (`SPEC`, `luot7/HINT.patch` `425e8e448eb1084b…`, `luot7/VERDICT.md`) sha256 không đổi.
Rig (MỘT lệnh mỗi bản, `clone kho.git` + `checkout --detach`): `tam/nen` @`02d169f` (cmp 2 tệp với cay-kho: TRÙNG), `tam/mst` @`577d7b9`, `tam/p7` @`abc0339`,
`tam/ga` / `tam/gb` @`02d169f` (pha ca (a)/(b); `core.abbrev 7` repo-local). sha256 `ops/cong_cu_test.py` @`02d169f` = `ce8997eea5fd744ca64a91dce5eb9d5f12dbe322d3b0c32f353f3e5b1a630e7e`,
`ops/bash_nen.py` = `28d313961fe7d434f147e76b39d54f2e248d8bc81ce5f32372bb0178b40ef22f`.

## ĐỐI CHIẾU THEO LỚP

> Đối chiếu với `luot7/VERDICT.md` (reviewer lượt 7, `302a15d`) + hai việc mới của vá 8. Nhãn §8: `ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ`.
> Vá 8 (`abc0339`→`02d169f`) = `luot7/HINT.patch` v3 (áp lên bản sao `abc0339`: `patch -p0 --fuzz=0` rc=0, offset +56, 5 hunk; **cmp với `02d169f` chỉ lệch đúng 3 chỗ — cờ `update-index`, đối chứng (0), chốt (cờ)**)
> + 3 sửa của executor (`diff -u tam/p7h/ops/cong_cu_test.py tam/nen/ops/cong_cu_test.py` = 3 hunk; `bash_nen.py` trùng byte). Mọi lệnh đo ở `tam/log/`.
> Phép đo dưới đây chạy bằng `_chay_1_ca` / `_do_mot` / `_ket_luan_ban_ghi` CỦA TỆP (nạp importlib, `-X utf8 -B`), (a) = `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`, (b) = `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`.

| lớp (slug) | hạng lượt 7 | nhãn trên `02d169f` | bằng chứng tự đo (lệnh ⇒ output) |
|---|---|---|---|
| NGHIEM-THU-WINDOWS-CON-THIEU | P2 | **CHƯA VÁ — KHÔNG ĐO ĐƯỢC ở Linux** (vẫn MỞ, không vá được bằng mã; chủ kho: "Chỉ chạy tại máy") | Không có log/receipt Windows cho `02d169f`. `HANDOFF_WINDOWS_6248128895` (Git for Windows 2.55.0.windows.5, Py 3.13.1, cp1258; commit đo `8da3996` đã MẤT) chỉ là lời khai phiên Windows: giả thuyết B ĐÚNG, `-c core.protectNTFS=false` ⇒ `va_\xff.py` vào INDEX. MÔ PHỎNG (`tam/gitgia/git`, theo handoff §1): `02d169f` + cờ có hiệu lực ⇒ `t49 qua`, `t63 qua`; cờ vô hiệu ⇒ `t49 bo_qua` và **`t63 giet_that "(0) đối chứng t49 BỎ QUA …"` (suite ĐỎ)**; `abc0339` ⇒ `t49 bo_qua`, `t63 qua` cả hai chế độ. ⇒ nghiệm thu Windows phải xác nhận `t49 = qua` (không `bo_qua`) và nhánh Job Object/`sys.stderr is not None`/`t64`(k1) thật. |
| TU-PHONG-LAI-KHONG-TRONG-SUOT (e) | P3 | **ĐÃ VÁ THẬT** | K4d (POSIX `return 0` khi stdout/stderr None) ⇒ trên `abc0339` `SONG`, trên `02d169f` `giet_that "(k4) fd 1 đóng ⇒ không phóng lại tới bộ ca: rc=0 b''"`; chỉ-stderr ⇒ `(k4) fd 2`; hoàn nguyên guard ⇒ `(k4) fd 1 … AttributeError`; bỏ `-X utf8` khi stdout None ⇒ sống nhưng TƯƠNG ĐƯƠNG (`_ep_utf8()` đã đặt `PYTHONUTF8=1`). Dấu DƯƠNG `U8=1 PL=1` đọc ở luồng còn mở. |
| CA-KHOA-T64-TREO-THAY-VI-DO (đường 2: nt `wait()` + stdin; đường 3: Timer chỉ giết bao) | P4 | **ĐÃ VÁ THẬT** | đường 2: `popen(lenh[:1])` + stdin = ống mở ⇒ `giet_that (w2)` 0,9 s; gỡ `stdin=DEVNULL` ⇒ TREO (giết ở 60 s). đường 3: M1R11 + Timer vá 8 ⇒ `tin_dung_gia` giàn giáo ở **120,5 s**; cùng đột biến + Timer cũ (`kill` không `stdin.close`) ⇒ TREO (giết ở 200 s). `t64` lặp: (a) 20/20 `qua`, (b) 20/20 `qua`, 0,9–1,2 s, 0 tiến trình sót. |
| DO-GIA-DOC-DIA-CHI-TUY-Y | P4 | **VÁ HỜ** (đóng đúng đường được chỉ, bỏ sót đường thứ ba) | số nhỏ (`sizeof(gh)`=144) ⇒ `abc0339` rc=−11, `02d169f` `(w1)` (chặn `p < 64 KiB` CÓ răng: gỡ chặn ⇒ rc=−11). Nhưng **handle giả ≈ 2^60 (`job`) đưa vào chỗ con trỏ ⇒ `02d169f` vẫn rc=−11** (SIGSEGV cả tiến trình, 0 dòng kết quả). Cây sửa thử (cận trên `< 1 << 48`, trung hoà dòng) ⇒ `(w1)`; gỡ cận trên ⇒ rc=−11. → finding DO-GIA-DOC-DIA-CHI-TUY-Y [P4]. |
| LOI-KHAI-RONG-HON-PHEP-DO | P4 | dạng `env=` + docstring byref: **ĐÃ VÁ THẬT**; MỚI: vài lời khai khác lệch — **VÁ SINH LỖI MỚI (nhỏ)** | `dem_env2.py` (AST, truy biến theo phạm vi): **40** call `env=` (số cũ 40 — đúng, nay không ghi), mọi giá trị ∈ {`moi_truong(…)`, `dict(os.environ,…)`, `{**os.environ,…}`, `dict({k: v … os.environ.items() …},…)`, tham số/biến truy về chúng hay `None`}; 0 literal-dict thiếu `os.environ` ⇒ chú thích khớp. N_H ⇒ `(w1) … 'co': 0` (qua biên); N_B ⇒ `(w1) … ArgumentError` (ở biên) ⇒ docstring `_k32_gia` khớp. MỚI lệch: docstring `t63` còn "nó BỎ QUA … chiều ĐỎ oan không đo ở nền ấy" trong khi (0) nay GIẾT; `doi_chung_xanh`/`raise …"đối chứng không XANH"` trong vòng lặp thành mã chết; BAO_CAO "`lỗi đột biến=0`" ở chế độ gate là số GIAO; "thêm đúng 1 dòng >118" lệch số đo. → T63-DOI-CHUNG-0 (P1) + LOI-KHAI-VA8 [P4]. |
| TRAN-DONG-DAT-BANG-NEN | P4 | **ĐÓNG MỘT PHẦN** (vá 8 làm giãn thêm) | `tran_dong.py` (tokenize dòng THÊM so `577d7b9`): `abc0339` ⇒ `;`=9, walrus=6, dòng>118=**26**, max 154; `02d169f` ⇒ `;`=9, walrus=6, dòng>118=**33**, max 154. Cả tệp: dòng>118 336 (master) → 362 (`abc0339`) → **369** (`02d169f`). |
| TEN-CA-LECH-SPEC | P4 | theo quyết định chủ kho (khai ở thân PR) — thân PR KHÔNG ĐO ĐƯỢC | `grep -c t52_import_bash_nen…` = 0; `def t60_import_bash_nen_khong_in_gi_ra_stderr` = 1; `t52`–`t54` nay là ca #668 (master); `t61`, `t62` (ca khoá UTF-8 spec §2C chưa đặt tên), `t63`, `t64` ngoài spec r1 (`t63`/`t64` hoàn toàn mới). |
| (MỚI) cờ `protectNTFS` của `t49` | — | Linux: **VÁ HỜ**; Windows: **KHÔNG ĐO ĐƯỢC** (P2) | gỡ cờ ⇒ `t63 giet_that (cờ)`; cờ nhầm lệnh / `true` / cấu hình kho ⇒ `(cờ)`; cờ đặt SAU lệnh con ⇒ `(0)` (git rc=129). **Sống sót:** cờ có ở mọi lệnh `update-index` TRỪ lệnh cho tên mang dấu chéo ngược ⇒ `t63 qua`, `t49 qua` — chốt (cờ) chỉ nhìn vòng LẶP CUỐI (`bo_hong`, không có lệnh nào cho tên chéo) và dùng `any()`. → T63-CO-CHI-DO-HIEN-DIEN [P4]. |
| (MỚI) đối chứng (0) của `t63` | — | mục tiêu: **ĐÃ VÁ THẬT**; **VÁ SINH LỖI MỚI [P1]** | "staging luôn ném" tiền tố INDEX / tiền tố LẠ / `_add` luôn ném ⇒ `abc0339`: `GIET_NHAN_KHAC` (tình cờ) / `BO_QUA` (sống) / `GIET_NHAN_KHAC`; `02d169f`: cả 3 `giet_that "(0) …"`. Nhưng đối chứng biến MỌI `BoQuaMoiTruong` của `t49` thành ĐỎ, kể cả tiền đề của `t27` ⇒ `bn_quet_theo_chuoi`: `abc0339` `ok … bán kính 1/61` → `02d169f` **`ĐỎ giết THÊM ['t63_…'] (bán kính 2/61)`, loi=1** (mảnh 3/8). → T63-DOI-CHUNG-0 [P1]. |

## BẢNG SĂN

> Mọi phép đo trên bản sao trong `$R/tam/` (`TMPDIR=$R/tam/tmp`, `PYTHONDONTWRITEBYTECODE=1`, `-X utf8 -B`); log ở `$R/tam/log/`. Công cụ tự viết ở `$R/tam/cu/`.
> Khe đột biến chỉ chạy MỘT tiến trình harness mỗi khe (một lần tôi chạy hai harness trên cùng khe `slotF3` ⇒ kết quả lẫn — đã bỏ và chạy lại tuần tự; xem KHÔNG ĐO ĐƯỢC/sự cố rig).

```
HƯỚNG 1: (k4) có đo "phần đầu VẪN phóng" (dấu DƯƠNG) hay chỉ rc — họ đột biến "thoát 0 không phóng"
  lệnh   : dot_bien_van.py <khe @02d169f> a  K4d_thoat0_khong_phong K4_chi_stderr_thoat0 K4_hoan_nguyen_flush K4_dong_thi_bo_X_utf8 ; cùng K4d trên khe @abc0339
  output : 02d169f: K4d ⇒ GIET_DUNG_NHAN "(k4) fd 1 đóng ⇒ không phóng lại tới bộ ca: rc=0 b''" (0,7 s); K4-stderr ⇒ "(k4) fd 2 … rc=0 b''"; K4-flush ⇒ "(k4) fd 1 … rc=1 …
           AttributeError: 'NoneType' … flush"; K4-bỏ-X-utf8 ⇒ SONG. abc0339: K4d ⇒ SONG (vá 8 là thứ giết nó). Nền (chưa đột biến) 9 ca qua ở (a)(b).
  kết luận: KHÔNG PHẢI LỖI — lớp (e) ĐÃ VÁ THẬT. K4-bỏ-X-utf8 sống là TƯƠNG ĐƯƠNG (`_ep_utf8()` đã đặt PYTHONUTF8=1 vào os.environ trước `_phong_lai` ⇒ U8=1 không cần `-X utf8`).

HƯỚNG 2: `dat` chặn con trỏ < 64 KiB — còn đường nào đưa NGUYÊN DẠNG số khác vào chỗ con trỏ mà vẫn SIGSEGV
  lệnh   : dot_bien_van.py <khe> a  SEGV_sizeof_vao_con_tro SEGV_handle_vao_con_tro SEGV_go_chan_64KiB SEGV_nguong_1_8   (byref(gh)→sizeof(gh) / →job / gỡ chặn / ngưỡng 256)
  output : sizeof(gh)=144 ⇒ GIET_DUNG_NHAN "(w1) cha chết mà con còn sống: job={…'co': 0…} … CANH_BAO_MO_COI" (11 s); gỡ chặn ⇒ KHAC rc=-11; ngưỡng 256 ⇒ (w1) (tương đương);
           **job (handle giả ≈ 2^60) ⇒ KHAC rc=-11, 0 dòng kết quả** — chặn `p >= 64 KiB` không bắt số LỚN.
  kết luận: LỖI (nhỏ, fail-closed nhưng mất chẩn đoán) — DO-GIA-DOC-DIA-CHI-TUY-Y còn đường thứ ba [P4, VÁ HỜ]; cây sửa thử (cận trên < 2^48): job ⇒ (w1); gỡ cận trên ⇒ rc=-11.

HƯỚNG 3: popen giả `stdin=DEVNULL` mặc định (đường treo 2) — khoá có răng không (gỡ khoá thì có TREO không)
  lệnh   : dot_bien_van.py <khe> a  NT_mat_doi_so_stdin_ong_mo  NT_mat_doi_so_stdin_ong_mo_GO_KHOA   (stdin bộ test = ỐNG MỞ qua os.pipe(); nt: popen(lenh[:1]) = REPL)
  output : có khoá ⇒ GIET_DUNG_NHAN "(w2) …" 0,9 s; gỡ khoá ⇒ TREO (giết ở hạn 60 s, rc=-9).
  kết luận: KHÔNG PHẢI LỖI — CA-KHOA-T64-TREO đường 2 ĐÃ VÁ THẬT.

HƯỚNG 4: Timer `p.kill() or p.stdin.close()` (đường treo 3: bản phóng lại là tiến trình RIÊNG)
  lệnh   : dot_bien_van.py <khe> b M1R11_voi_Timer_moi M1R11_voi_Timer_cu   (POSIX chạy con riêng thay execve + mất argv ≙ Windows Job hỏng; Timer mới / Timer cũ chỉ kill)
  output : Timer mới ⇒ TIN_DUNG_GIA "giàn giáo hỏng … phần đầu không phóng lại sang UTF-8 — không đo gì: ''" sau 120,5 s; Timer cũ ⇒ TREO (giết ở 200 s).
           (lần đầu tôi gõ sai mỏ neo — `lenh[1:2]` làm con thoát ngay — nên đã bỏ và chạy lại với `lenh` đủ; log vẫn giữ ở van-slot2-b.jsonl/van-slot3-b.jsonl.)
  kết luận: KHÔNG PHẢI LỖI — đường 3 ĐÃ VÁ THẬT; `p.stdin.close()` là phần biến TREO thành ĐỎ có tên. Windows thật (Job hỏng) KHÔNG ĐO ĐƯỢC.

HƯỚNG 5: chốt (cờ) `core.protectNTFS=false` có đo ĐÚNG lệnh cần cờ không
  lệnh   : dot_bien_van.py <khe> a  GO_CO_NTFS CO_NTFS_SANG_HASH_OBJECT CO_NTFS_GIA_TRI_TRUE CO_NTFS_SAU_LENH_CON CO_NTFS_VAO_CAU_HINH_KHO CO_NTFS_THIEU_CHO_TEN_CHEO
  output : gỡ cờ / cờ sang hash-object / `true` / cờ trong cấu hình kho ⇒ GIET_DUNG_NHAN "(cờ) update-index thiếu …"; cờ SAU lệnh con ⇒ "(0) … rc=0/129 … unknown switch 'c'" (bởi (0));
           **cờ có ở mọi lệnh TRỪ lệnh cho tên mang dấu chéo ngược ⇒ SONG (t63 qua, t49 qua)** — (cờ) dùng `any()` và `nhat_ky.clear()` mỗi vòng nên chỉ thấy vòng CUỐI (`bo_hong`),
           vòng ấy KHÔNG có lệnh update-index nào cho tên chéo.
  kết luận: LỖI (P4, VÁ HỜ) — T63-CO-CHI-DO-HIEN-DIEN; hiệu lực Windows KHÔNG ĐO ĐƯỢC. Cây sửa thử (cờ trong vòng `bo_ten`, tập boolean == {True}) giết cả 6; nền vẫn 9/9.

HƯỚNG 6: đối chứng (0) của `t63`
  lệnh   : (6a) dot_bien_van.py T63_LUON_NEM_tien_to_INDEX T63_LUON_NEM_tien_to_LA T63_ADD_LUON_NEM trên abc0339 và 02d169f; (6b) quét 161 đột biến `bash_nen.py` bằng đúng
           `_dung_cay_dot_bien` + `_chay_1_ca` của tệp cho [đích, t49, t63] (dot_bien_bn.py), rồi `do_mot_tay.py` (= `_do_mot` + `_ket_luan_ban_ghi`); (6c) mảnh 3/8 THẬT (`CONG_CU_TEST_MANH=3/8`, env CI).
  output : (6a) abc0339 ⇒ GIET_NHAN_KHAC (tình cờ) / BO_QUA (sống) / GIET_NHAN_KHAC; 02d169f ⇒ cả 3 GIET_DUNG_NHAN "(0) đối chứng t49 KHÔNG tráo mà đã BỎ QUA …".
           (6b) 161/161 đích giet_that; **đúng 1 đột biến có t63 giet_that ngoài đích: bn_quet_theo_chuoi** (t49 bo_qua "cây có tệp cú pháp HỎNG mà cổng không fail-close … chuyện của `t27`", t63 giet_that "(0) …");
           `do_mot_tay.py`: abc0339 ⇒ "ok  bn_quet_theo_chuoi → giết đúng 't27_…' · bán kính 1/61" loi=0; 02d169f ⇒ "ĐỎ  bn_quet_theo_chuoi: giết THÊM ['t63_…'] ngoài đích 't27_…' (bán kính 2/61)" loi=1, cả env (a) và (b).
           (6c) mảnh 3/8 @02d169f: 58 "ok … bán kính 1/61" + "ĐỎ  bn_quet_theo_chuoi: giết THÊM ['t63_…'] …" + "ĐỎ  mảnh 3/8 [M-loi]: 1 lỗi đột biến — không ghi tệp" + `RC=1` (log manh3-a.log).
  kết luận: LỖI (P1) — VÁ SINH LỖI MỚI T63-DOI-CHUNG-0 (hồi quy so abc0339, xác nhận đầu-cuối).

HƯỚNG 7: đột biến NGOÀI `bash_nen.py` (SCRIPT/CAI_SH/GOC/TEP_TEST = 309) có bị vá 8 kéo thêm ca chết không (đặc biệt t64 vì (k4)/Timer/popen đổi)
  lệnh   : dot_bien_hk.py (3 tiến trình, 19:36Z→19:49:49Z, khi mảnh 3 thật + quét khác đang chạy: tải 4–5/4 lõi): mọi đột biến có bp ≠ BASH_NEN (TEP_TEST 286, SCRIPT 19, CAI_SH 2, GOC 2 = 309) chạy [đích, t49, t63, t64]
           qua `_dung_cay_dot_bien` + tráo biến toàn cục NHƯ `_do_ban_kinh` của tệp, trên `02d169f`
  output : 309 bản ghi, 0 mỏ neo lỗi; 308/309 đích `giet_that`; ngoại lệ DUY NHẤT `t2_go_canary` (đích `t2` `bo_qua` — thiếu `jsonschema`, môi trường, như lượt 7); **`t49`, `t63`, `t64` = `qua` dưới CẢ 309** (0 ca chết thêm),
           kể cả `t64` dưới tải (max 20,1 s cả bản ghi gồm đích; trung vị 7,5 s).
  kết luận: KHÔNG PHẢI LỖI — trên toàn bộ 470 đột biến (161 `bash_nen.py` + 309 ngoài), hồi quy bán kính của vá 8 chỉ là `bn_quet_theo_chuoi`.

HƯỚNG 8: MÔ PHỎNG Windows (git giả theo handoff §1) — vá 8 ra sao nếu cờ có/không hiệu lực
  lệnh   : PATH=tam/gitgia:$PATH GITGIA_MODE={honor|ignore_flag}  chay_ca.py <khe> t49 t63  trên 02d169f và abc0339
  output : 02d169f honor ⇒ t49 qua, t63 qua; 02d169f ignore_flag ⇒ t49 bo_qua + **t63 giet_that "(0) đối chứng t49 BỎ QUA …"**; abc0339 (cả hai chế độ) ⇒ t49 bo_qua, t63 qua.
  thêm   : Linux git 2.43.0, `update-index --add -z --index-info` cho tên `ops/va_\xff.py` (dấu chéo ngược nguyên văn) ⇒ rc=0 và VÀO INDEX với cờ mặc định, `-c core.protectNTFS=false` VÀ `=true` ⇒ cờ KHÔNG có hiệu lực quan sát được ở Linux
           (chỉ nhánh Windows/Cygwin của git từ chối `\`), nên chốt (cờ) chỉ có thể đo ARGV, không đo hiệu lực.
  kết luận: KHÔNG ĐO ĐƯỢC Windows thật (mô phỏng theo lời khai handoff). Hệ quả đo được: nếu trên `windows-latest` cờ KHÔNG đủ (t49 vẫn bo_qua) thì vá 8 làm suite ĐỎ ở `t63` (trước đó xanh) —
           nghiệm thu Windows phải xác nhận `t49 = qua`. Docstring `t63` còn nói điều ngược (xem LOI-KHAI-VA8).

HƯỚNG 9: lời khai "chú thích `env=`" (LOI-KHAI dạng) và docstring byref
  lệnh   : dem_env2.py (AST, truy biến theo phạm vi hàm) trên 02d169f; dot_bien_van.py N_H_lech_byref N_B_quen_byref
  output : 40 call `env=` (số cũ 40 — không đổi, nay không ghi): 19 trực tiếp (12 `moi_truong(…)`, 4 `{**os.environ,…}`, 3 `dict(os.environ,…)`) + 21 qua biến/tham số (10 gán bộ từ `bk_don` ⇒ `moi_truong`, 3 ⇒ `dict(os.environ,…)`,
           2 ⇒ `dict({k: v … os.environ.items() …},…)` (env của `t64`/`t62`), 1 ⇒ `moi_truong`, 1 `dict(env,…)` ⇒ `dict(os.environ,…)`, 4 tham số hàm `chay/_quet/_phong_lai/danh_sach` — mọi chỗ gọi thuộc danh sách); 0 literal-dict thiếu `os.environ`.
           N_H ⇒ "(w1) … 'co': 0" (qua biên, bắt bởi trạng thái); N_B ⇒ "(w1) … ArgumentError" (ở biên).
  kết luận: KHÔNG PHẢI LỖI — LOI-KHAI-RONG-HON-PHEP-DO (dạng + byref) ĐÃ VÁ THẬT.

HƯỚNG 10: ổn định `t64` (chập chờn/treo) và nhiều nền Python
  lệnh   : lap_t64.sh a 20; lap_t64.sh b 20; chay_ca.py 9 ca với python3.11 / 3.13 × (a)(b)
  output : t64 (a) 20/20 qua, (b) 20/20 qua, 0,9–1,2 s; 9 ca qua ×4 (3.11/3.13 × a/b); không tiến trình sót.
  kết luận: KHÔNG PHẢI LỖI.

HƯỚNG 11: hồi quy `.pyc` / cây bẩn
  lệnh   : clone mới @02d169f, `env -u PYTHONDONTWRITEBYTECODE … chay_ca.py t60 t61 t62 t63 t64 t49`; find *.pyc/__pycache__; status --porcelain --ignored
  output : TONG {"qua": 6}; 0 .pyc; status rỗng.
  kết luận: KHÔNG PHẢI LỖI.

HƯỚNG 12: tiêu chí spec §6.3 (i)(ii) còn giữ sau vá 8 (bán kính trọn 61 ca)
  lệnh   : toan_bo_van.py: (i) `r"""`→`"""` ở docstring _tach_dinh_dang; (ii) `_ep_utf8` không đặt biến UTF-8 cho con; env (a) và (b)
  output : (i) chỉ t60 giet_that "(1) … SyntaxError: invalid escape sequence '\(' (bash_nen.py, line 898)" (t2 bỏ qua) ⇒ 1/61; (ii) (a): chỉ t61 "(b) cháu (không env=) không in được byte UTF-8 thật" ⇒ 1/61;
           (ii) (b) ASCII: t61 + `t7_hai_duong_goi_khac_ban_phai_bao_khong_im` (rc=1 thay rc=2: cháu in chữ Việt ra stdout ASCII — chính hậu quả mà lớp UTF-8 sinh ra để chặn).
  kết luận: KHÔNG PHẢI LỖI (spec §6.3 đạt ở env CI; ở (b) bán kính 2 là hậu quả đã biết của thiếu ép UTF-8, không phải lỗi mã).

HƯỚNG 13: lời khai của executor so với phép đo (BAO_CAO/commit)
  lệnh   : xem BẢNG ĐO
  output : khớp: +420/−42; 9 ca ×2 env; 60/60 ×2 env; 9 đột biến; ruff F = nền; compile ×3; t64 40/40. Lệch: "`lỗi đột biến=0`" ở chế độ gate là số GIAO (`BÁN KÍNH … GIAO cho job gate-cong-cu`), không phải bán kính;
           "thêm đúng 1 dòng >118 ký tự" (đo: +7 so abc0339, 26→33 so master); docstring t63 ngược hành vi.
  kết luận: LỖI (nhỏ, P4) — LOI-KHAI-VA8; bằng chứng 9/470 không thể thấy hồi quy bán kính (nó nằm ở 1 trong 470).
```

## BẢNG ĐỘT BIẾN
> Công cụ (tự viết, trong `tam/cu/`): `chay_ca.py` (importlib nạp ĐÚNG `ops/cong_cu_test.py` của khe + `_chay_1_ca` CỦA TỆP, `-X utf8 -B`), `dot_bien_van.py`
> (đột biến VĂN BẢN lên khe `git clone --shared` @`02d169f`, mỏ neo đếm đúng 1, xoá `__pycache__`, khôi phục + `status --porcelain --ignored` sau mỗi cái; phân hạng
> `GIET_DUNG_NHAN` chỉ khi `giet_that` VÀ lý do chứa nhãn chốt chờ), `dot_bien_bn.py`/`do_mot_tay.py` (đột biến SẴN CÓ của `DOT_BIEN` qua `_dung_cay_dot_bien` + `_do_mot` +
> `_ket_luan_ban_ghi` CỦA TỆP). Nền (chưa đột biến) trong khe: 9 ca `t49 t52 t53 t54 t60–t64` ⇒ `TONG {"qua": 9}` ở (a) và (b) TRƯỚC khi đột biến (chống tín dụng giả).
> Cột "sot" trong log = `pgrep -f <khe>` tự khớp tiến trình của chính harness ⇒ 1 = 0 tiến trình sót.

| # | đột biến (mỏ neo NGUYÊN VĂN `02d169f`) | ca đích | kết quả — tín hiệu chốt (rút gọn) | phân loại |
|---|---|---|---|---|
| K4d | `_phong_lai` POSIX: `if sys.stdout is None or sys.stderr is None: return 0` (thoát 0, KHÔNG phóng, KHÔNG chạy ca) | t64 | `giet_that` `(k4) fd 1 đóng ⇒ không phóng lại tới bộ ca: rc=0 b''` (0,7 s) | giết thật |
| K4-flush | hoàn nguyên guard `is not None` (flush trên None) | t64 | `giet_that` `(k4) fd 1 … rc=1 … AttributeError: 'NoneType' … flush` | giết thật |
| K4-in | (đối chứng ngược, sản phẩm ĐÚNG) gỡ `file=sys.stdout or sys.stderr` của `dau.py` | t64 | `giet_that` `(k4) fd 1 … rc=0 b''` ⇒ hunk 4 cần thiết | đối chứng |
| SEGV-144 | `byref(gh)`→`sizeof(gh)` (số 144 vào chỗ con trỏ) | t64 | `giet_that` `(w1) cha chết mà con còn sống: job={…'co': 0…} … CANH_BAO_MO_COI …` (11 s), rc=0 | giết thật |
| SEGV-gỡ-chặn | như trên + gỡ `(p or 0) >= 1 << 16` | t64 | KHÁC rc=**-11** (SIGSEGV cả tiến trình, 0 dòng kết quả) | chặn 64 KiB CÓ RĂNG |
| SEGV-ngưỡng-256 | như SEGV-144 + ngưỡng `1 << 8` | t64 | `giet_that` `(w1)` | tương đương (144 < 256) |
| **SEGV-handle** | `byref(gh)`→`job` (handle job GIẢ ≈ 2^60 đưa vào chỗ con trỏ) | t64 | KHÁC rc=**-11** (SIGSEGV cả tiến trình, 0 dòng kết quả) | **SỐNG SÓT (fail-closed nhưng mất chẩn đoán)** — xem finding DOC-DIA-CHI |
| N_H | `byref(gh, 16)` (lệch byref) | t64 | `giet_that` `(w1) … 'co': 0 …` (qua biên ctypes, bắt bởi TRẠNG THÁI) | giết thật; khớp docstring "lệch byref đọc cờ sai chỗ" |
| N_B | `byref(gh)`→`gh` (thiếu byref) | t64 | `giet_that` `(w1) … CANH_BAO_MO_COI … (Ar…` (ArgumentError ở BIÊN) | giết thật; khớp docstring "thiếu byref lỗi ở BIÊN" |
| popen-stdin | nt: `popen(lenh[:1], …)` (mất đối số ⇒ REPL), stdin bộ test = ỐNG MỞ | t64 | `giet_that` `(w2)` (0,9 s), KHÔNG treo | giết thật |
| popen-stdin-GỠ-KHOÁ | như trên + gỡ `stdin=DEVNULL` của `popen` giả | t64 | TREO (bị giết ở hạn 60 s), rc=-9 | khoá CÓ RĂNG |
| cờ-gỡ | gỡ `"-c", "core.protectNTFS=false"` khỏi `update-index` | t63 | `giet_that` `(cờ) update-index thiếu -c core.protectNTFS=false …` | giết thật |
| cờ-nhầm-lệnh | cờ đặt vào `hash-object` thay `update-index` | t63 | `giet_that` `(cờ)` | giết thật |
| cờ-true | `core.protectNTFS=true` | t63 | `giet_that` `(cờ)` | giết thật |
| cờ-sau-lệnh-con | `update-index -c core.protectNTFS=false …` (cú pháp sai) | t63 | `giet_that` `(0) đối chứng … INDEX không nhận tên … rc=0/129` — chốt (0) bắt, chuỗi cờ vẫn có trong argv | giết thật (bởi (0), không bởi (cờ)) |
| cờ-cấu-hình-kho | cờ chuyển sang `git config core.protectNTFS false` của kho tạm (tương đương Windows) | t63 | `giet_that` `(cờ)` | chốt (cờ) CHẶT HƠN hiệu lực (xem finding) |
| (0)-INDEX | `_stage_byte` luôn ném, tiền tố "KHÔNG ĐO ĐƯỢC: INDEX" | t63 | `giet_that` `(0) đối chứng …` | giết thật |
| (0)-LẠ | `_stage_byte` luôn ném, tiền tố LẠ | t63 | `giet_that` `(0) đối chứng …` | giết thật |
| (0)-add | `_add` luôn ném | t63 | `giet_that` `(0) đối chứng … git add …` | giết thật |
| **bn_quet_theo_chuoi** | ĐỘT BIẾN SẴN CÓ của `DOT_BIEN` (đích `t27`) — `_do_mot` + `_ket_luan_ban_ghi` | t27 (+t63) | **`ĐỎ giết THÊM ['t63_…'] ngoài đích 't27_…' (bán kính 2/61)`, loi=1** (trên `abc0339`: `ok … bán kính 1/61`) | **VÁ SINH LỖI MỚI** — finding T63-DOI-CHUNG-0 |
| M1R11+Timer-mới | POSIX `subprocess.run(lenh)` thay `execve` + mất `*sys.orig_argv[1:]` (≙ lượt 7 M1R11: bản phóng lại là tiến trình RIÊNG, treo đọc stdin) + Timer của vá 8 (`kill` + `stdin.close`) | t64 | `tin_dung_gia` giàn giáo "phần đầu không phóng lại sang UTF-8 — không đo gì: ''" sau **120,5 s**, rc=0, 0 tiến trình sót | khoá CÓ RĂNG (ĐỎ có tên, không treo) |
| M1R11+Timer-cũ | như trên nhưng Timer CHỈ `p.kill` (không `stdin.close`) | t64 | **TREO** (bị giết ở hạn 200 s, rc=-9) | `p.stdin.close()` là phần biến treo thành đỏ |
| K4-chỉ-stderr | `if sys.stderr is None: return 0` | t64 | `giet_that` `(k4) fd 2 đóng ⇒ không phóng lại tới bộ ca: rc=0 b''` | giết thật |
| K4-bỏ-X-utf8 | stdout None ⇒ phóng lại KHÔNG có `-X utf8` | t64 | SỐNG — TƯƠNG ĐƯƠNG: `_ep_utf8()` đã đặt `PYTHONUTF8=1` vào `os.environ` trước `_phong_lai`, con vẫn `U8=1` | sống KỲ VỌNG (tương đương) |
| **cờ-thiếu-cho-tên-chéo** | cờ có ở mọi lệnh `update-index` TRỪ lệnh cho tên mang dấu chéo ngược (đúng tên cần cờ trên Windows) | t63, t49 | **SỐNG** `t63 qua`, `t49 qua` (Linux): chốt (cờ) dùng `any()` và `nhat_ky.clear()` mỗi vòng ⇒ chỉ thấy vòng CUỐI (`bo_hong`, KHÔNG có lệnh nào cho tên chéo) | **SỐNG SÓT** — finding T63-CO-CHI-DO-HIEN-DIEN |
| SWEEP-161 | toàn bộ 161 đột biến SẴN CÓ của `bash_nen.py` (BASH_NEN), cho [đích, t49, t63] | đích + t49 + t63 | 161/161 đích `giet_that`; t63 `giet_that` ngoài đích: 1 (`bn_quet_theo_chuoi`); 4 đột biến đích `t49` có t63 `bo_qua` | 1 hồi quy |
| SWEEP-309 | 309 đột biến SẴN CÓ ngoài `bash_nen.py` (TEP_TEST/SCRIPT/CAI_SH/GOC), cho [đích, t49, t63, t64] | đích + t49 + t63 + t64 | 308/309 đích `giet_that` (`t2_go_canary` bỏ qua: thiếu `jsonschema`); t49/t63/t64 `qua` dưới cả 309 | 0 hồi quy |
| MẢNH-3/8 | mảnh `gate-cong-cu` 3/8 THẬT (59 đột biến) trên `02d169f` env CI | cả bộ | 58 `ok … 1/61` + `ĐỎ bn_quet_theo_chuoi … 2/61` ⇒ `ĐỎ mảnh 3/8 [M-loi]: 1 lỗi đột biến`, RC=1 | hồi quy xác nhận đầu-cuối |
| MẢNH-3/8 (cây áp HINT) | cùng mảnh 3/8 THẬT trên commit nháp của cây áp HINT (`tam/m3h`, 19:39:20Z→20:04:28Z) | cả bộ | `60/60 đạt`; **59/59 `ok … 1/61`** gồm `ok  bn_quet_theo_chuoi → giết đúng 't27_…' · bán kính 1/61`; `manh/manh-3.txt` (395 810 B, `head`=commit nháp, `sha256_test` ghi) ; **RC=0**; 0 `.pyc` | HINT sửa hồi quy đầu-cuối |

**Cây SỬA thử (`tam/fix` @ commit tạm `f8a4e45` — chỉ trong `$R/tam/`; chính là cây của `out/HINT.patch`)**: nền 9 ca `qua` ×(a)(b); `bn_quet_theo_chuoi` ⇒ `ok … bán kính 1/61`; SEGV-sizeof, SEGV-handle ⇒ `(w1)` (không SEGV); gỡ cận trên 2^48 + handle ⇒ rc=-11 (cận trên CÓ răng);
cờ-gỡ / cờ-nhầm-lệnh / cờ-true / cờ-thiếu-cho-tên-chéo / cờ-cấu-hình-kho ⇒ `giet_that (cờ)`; cờ-sau-lệnh-con và (0)×3 ⇒ `giet_that (0)`; K4d ⇒ `(k4)`; popen-stdin ⇒ `(w2)`.

## BẢNG ĐO

> Tự đo lại từng khẳng định; KHÔNG chép lời khai executor (BAO_CAO/DUONG_VAO/thân commit). Thứ tự = thứ tự khai trong prompt + BAO_CAO. "executor khai" lấy từ `bao-cao-va-luot8/*` và thân commit `02d169f`.

| khẳng định | executor khai | đo được (lệnh ⇒ output) | khớp? |
|---|---|---|---|
| dòng thêm so master `577d7b9` (trần ~420) | +420/−42; `419 + 1 = 420`, HEADROOM 0 | `git diff --numstat 577d7b9 02d169f` ⇒ `1 1 ops/bash_nen.py` + `419 41 ops/cong_cu_test.py` = **+420/−42** (myers = patience = minimal); `--histogram` ⇒ +422/−44 (phụ thuộc thuật toán); GitHub tính thế nào: KHÔNG ĐO ĐƯỢC | khớp (thuật toán mặc định) — headroom 0 |
| PR chỉ 2 tệp = write set | có | `git diff --name-only 577d7b9 02d169f` ⇒ `ops/bash_nen.py`, `ops/cong_cu_test.py`; merge-base `577d7b9`; `git diff --check` rc=0; 0 CRLF; 0 `.orig/.rej/.pyc` trong cây commit | khớp |
| vá 8 so `abc0339` | "+417 head + 3" | `numstat abc0339 02d169f` ⇒ `17 14` (net +3); `577d7b9..abc0339` ⇒ +417/−42 | khớp |
| áp `luot7/HINT.patch` v3, "dry-run rc=0, offset +56" | có | clone mới `abc0339`: `patch -p0 --fuzz=0 --dry-run` ⇒ rc=0, `Hunk #2..#5 succeeded … (offset 56 lines)`; áp thật rc=0; `diff -u` với `02d169f` chỉ lệch ĐÚNG 3 hunk của executor (cờ `update-index`, đối chứng (0), chốt (cờ)); `bash_nen.py` TRÙNG | khớp |
| 9 ca giao `t49 t52 t53 t54 t60–t64` (a) 9/9, (b) 9/9 | có | `chay_ca.py` (`_chay_1_ca` của tệp, importlib, `-X utf8 -B`) trên `02d169f`: (a) `TONG {"qua": 9}`, (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` `TONG {"qua": 9}`; thêm python3.11.15 và 3.13.12 × (a)(b): `TONG {"qua": 9}` ×4 | khớp |
| pha ca như CI, chế độ gate `CONG_CU_TEST_BAN_KINH=manh`: `60/60 đạt` (a) và (b), RC=0 | có (bỏ qua=1 `t2`: thiếu `jsonschema`) | clone mới `tam/ga`/`tam/gb` @`02d169f`, (a) `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`, (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` qua `__main__` (PID giữ qua execve `-X utf8`): cả hai `cong_cu_test: 60/60 đạt; tổng=61, bỏ qua=1, tiền kiểm bỏ qua=0` · `CỔNG TRÊN CÂY THẬT: ĐẠT · nguon_tep=git · nguon_noi_dung=blob-index` · `TỰ KIỂM BỘ PHÂN HẠNG (7 ca)` 7 ok · `TỰ KIỂM SONG SONG (N126): ĐẠT` · `RC=0` · ~308 s · 0 `.pyc` | khớp |
| "`lỗi đột biến=0`" ở pha gate | có (BAO_CAO §2.3) | cùng log: `BÁN KÍNH ĐỘT BIẾN (470 đột biến): GIAO cho job gate-cong-cu (mảnh) + gate-cong-cu-gop (gom) — KHÔNG đo trong tiến trình này` ⇒ `lỗi đột biến=0` là số GIAO. Số đột biến thật = **470** (`len(DOT_BIEN)` trên master, `abc0339`, `02d169f`; prompt ghi 416 là số cũ) | **không khớp ý nghĩa** (xem T63-DOI-CHUNG-0, LOI-KHAI-VA8) |
| 9/9 đột biến giết đúng nhãn (5 chốt mới/sửa + 4 #668) | có | K4d ⇒ `(k4) fd 1 … rc=0 b''` (abc0339: SONG); SEGV-144 ⇒ `(w1)` (abc0339: rc=−11); GO_CO_NTFS ⇒ `(cờ)`; T63_LUON_NEM ⇒ `(0)` (abc0339: `GIET_NHAN_KHAC` tình cờ); T63_LUON_NEM_GENERIC ⇒ `(0)` (abc0339: `BO_QUA`); `do_mot_tay.py` f25 ⇒ `t52` 1/61, f13 ⇒ `t52` 1/61, f27 ⇒ `t54` 1/61, f28 ⇒ `t54` 1/61, loi=0 | khớp (9 trên 470 — không phủ hồi quy bán kính) |
| bán kính TOÀN BỘ đột biến `bash_nen.py` (161) sau vá 8 | (không khai) | `dot_bien_bn.py` ⇒ 161/161 đích `giet_that`; **t63 `giet_that` ngoài đích: 1 (`bn_quet_theo_chuoi`)**; `do_mot_tay.py`: `02d169f` loi=1, `abc0339` loi=0 | **không khớp spec §6.1 (delta ≤ 0)** |
| mảnh `gate-cong-cu` 3/8 trên `02d169f` (env CI) | (không khai) | `CONG_CU_TEST_MANH=3/8 CONG_CU_TEST_MANH_RA=manh/manh-3.txt CONG_CU_TEST_TIEN_TRINH=2` (nice 10): `60/60 đạt`; 58 × `ok … bán kính 1/61`; `ĐỎ bn_quet_theo_chuoi: giết THÊM […] (bán kính 2/61)`; `ĐỎ mảnh 3/8 [M-loi]: 1 lỗi đột biến — không ghi tệp`; `RC=1` (18:58:03Z→19:21:58Z) | ĐỎ |
| đột biến NGOÀI `bash_nen.py` (309) có bị vá 8 kéo thêm ca chết không | (không khai) | `dot_bien_hk.py` ⇒ 309 bản ghi, 308/309 đích `giet_that` (ngoại lệ `t2_go_canary`: thiếu `jsonschema`), `t49`/`t63`/`t64` `qua` dưới cả 309 | đạt |
| `ruff --select F` trên 2 tệp = nền {F401 `ast` bash_nen, F841 `ci`} | có | ruff **0.15.15** (đúng pin CI; `pip download` PyPI → `--target tam/ruff`) và 0.15.8: `master 577d7b9` = `abc0339` = `02d169f` = {`ops/bash_nen.py: F401 \`ast\``, `ops/cong_cu_test.py: F841 \`ci\``}; cây áp HINT cũng vậy; 0 `.ruff_cache` | khớp |
| compile `-W error` 3.11/3.12/3.13 sạch | có | `python3.11.15/3.12.3/3.13.12`: "sạch" ×3 cho cả hai tệp | khớp |
| `t64` lặp ≥20, không treo, 40/40 | "20/20 (a) + 20/20 (b)" | `lap_t64.sh` trên `tam/nen`: (a) 20/20 `qua`, (b) 20/20 `qua`; 0,9–1,2 s mỗi lần; 0 tiến trình sót | khớp |
| docstring `_tach_dinh_dang` không đổi byte (spec §2A) | — | `ast.get_docstring(clean=False)` sha256 `3bc957a67247801b…`, 897 ký tự ở `577d7b9` = `02d169f` | đạt |
| spec §6.3(i) `r"""`→`"""` ⇒ `t60` ĐỎ bằng tín hiệu của chính nó | — | `toan_bo_van.py` TRỌN 61 ca (a): chỉ `t60 giet_that "(1) … SyntaxError: invalid escape sequence '\(' (bash_nen.py, line 898)"`, `t2` bỏ qua ⇒ **1/61** | đạt |
| spec §6.3(ii) gỡ ép UTF-8 cho con ⇒ ca khoá UTF-8 ĐỎ, bán kính 1/N | — | TRỌN 61 ca (a): chỉ `t61 "(b) cháu (không env=) không in được byte UTF-8 thật"` ⇒ **1/61**; (b) ASCII: `t61` + `t7_hai_duong_goi_khac_ban_phai_bao_khong_im` (hậu quả của thiếu ép UTF-8) ⇒ 2/61 | đạt (env CI) |
| spec §6.1 "delta lỗi đột biến ≤ 0 so nền" | "delta = 0" (lượt trước) | `02d169f`: **+1** (`bn_quet_theo_chuoi`); cây áp HINT: 0 trên 161 | ĐỎ → HINT |
| doctrine-scan sạch | có (thân commit) | `packet_loop.py doctrine-scan --root .` @`02d169f` ⇒ "sạch — đã quét 10 tệp, 0 chỗ chép doctrine", rc=0 | khớp |
| TRAN-DONG "thêm đúng 1 dòng >118 ký tự" | có | `tokenize` dòng thêm vs master: dòng>118 `abc0339` 26 → `02d169f` **33**; cả tệp 362 → 369; `;` 9 → 9; walrus 6 → 6; max 154 → 154 | **không khớp** (+7) |
| TEN-CA: `t60`–`t64` thay `t52` | quyết định chủ kho | `t52_import…` 0; `def t60_import_bash_nen_khong_in_gi_ra_stderr` 1 | đạt (thân PR KHÔNG ĐO ĐƯỢC) |
| `.pyc`/cây sạch sau khi chạy | có | clone mới, `env -u PYTHONDONTWRITEBYTECODE`, `chay_ca.py t60 t61 t62 t63 t64 t49` ⇒ 0 `.pyc`, `status --porcelain --ignored` rỗng | khớp |
| `out/HINT.patch` (bản sửa) | — | `patch -p0 --fuzz=0 --dry-run` rc=0 trên clone MỚI `02d169f`; áp rc=0; byte-trùng cây sửa; **+420/−42 so master (KHÔNG thêm dòng)**; ruff F = nền; 9 ca (a)(b) 9/9; gate (a)(b) `60/60 đạt` RC=0 trên commit nháp; 161 đột biến `bash_nen.py`: 161/161 đích, t63 ngoài đích 0 | đạt |

## FINDINGS

> Đếm theo LỚP còn mở: **P0=0 · P1=1 · P2=1 · P3=0 · P4=5**. P2 = nghiệm thu Windows (không vá được bằng mã ở Linux). Mỗi finding đủ 4 phần §8; HINT ở `out/HINT.patch`.

### T63-DOI-CHUNG-0-PHA-CO-LAP-BAN-KINH  [P1]  VÁ SINH LỖI MỚI — đối chứng (0) mới của `t63` biến `BoQuaMoiTruong` của TIỀN ĐỀ `t27` (không phải staging) thành `giet_that` ⇒ đột biến `bn_quet_theo_chuoi` (đích `t27`) từ bán kính 1/61 thành 2/61 ⇒ mảnh 3/8 `RC=1`, `gate-cong-cu-gop` ĐỎ
TỆP/DÒNG: `ops/cong_cu_test.py` @`02d169f`: `t63` `except BoQuaMoiTruong as ex:` + `bang(False, "(0) đối chứng …")` (L6477–6478); nguồn của lỗi: `t49` L6383–6386 `raise BoQuaMoiTruong("KHÔNG ĐO ĐƯỢC: cây có tệp cú pháp HỎNG mà cổng không fail-close … đó là chuyện của `t27`")`.
VẤN ĐỀ: sửa B của executor ("đối chứng (0) ĐỎ khi staging ném bừa") đổi `doi_chung_xanh = False` thành `bang(False, …)` cho MỌI `BoQuaMoiTruong` mà `t49` KHÔNG tráo ném ra. Nhưng `t49` có HAI nguồn `BoQuaMoiTruong`:
(1) staging (`_add`/`_stage_byte`: "KHÔNG ĐO ĐƯỢC: git add …"/"INDEX không nhận tên …") — đúng thứ (0) muốn giết; (2) **tiền đề của `t27`** — chốt do các vòng trước cố ý đặt để đột biến `bn_quet_theo_chuoi` (đích `t27`) KHÔNG kéo `t49` vào bán kính ("bán kính 2/53 vì bản đầu kết luận thẳng mà không hỏi tiền đề").
Trước vá 8, `t63` trước nguồn (2) vẫn `bo_qua` (`doi_chung_xanh=False`, vòng `bo_ten` ra "lý do khác"). Sau vá 8, `t63` `giet_that "(0) đối chứng t49 KHÔNG tráo mà đã BỎ QUA …: KHÔNG ĐO ĐƯỢC: cây có tệp cú pháp HỎNG mà cổng không fail-close …"` ⇒ bán kính {`t27`, `t63`}.
ĐO (mọi lệnh ở `tam/log/`, env (a) và (b)):
  · `do_mot_tay.py` (= `_do_mot` + `_ket_luan_ban_ghi` CỦA TỆP) trên `abc0339`: `ok  bn_quet_theo_chuoi → giết đúng 't27_…' · bán kính 1/61`, loi=0; trên `02d169f`: `ĐỎ  bn_quet_theo_chuoi: giết THÊM ['t63_t49_hong_STAGE_tung_buoc_phai_BO_QUA_dung_buoc'] ngoài đích 't27_…' (bán kính 2/61)`, loi=1 — (a) VÀ (b).
  · quét 161 đột biến `bash_nen.py` (đích + t49 + t63): 161/161 đích `giet_that`; t63 `giet_that` ngoài đích: **đúng 1** (`bn_quet_theo_chuoi`); 4 đột biến đích `t49` có t63 `bo_qua` (không đổi so `abc0339`).
  · mảnh 3/8 THẬT trên `02d169f` (`CONG_CU_TEST_MANH=3/8 CONG_CU_TEST_MANH_RA=manh/manh-3.txt`, env CI, ~23 phút): `cong_cu_test: 60/60 đạt` … 58 dòng `ok … bán kính 1/61` … `ĐỎ  bn_quet_theo_chuoi: giết THÊM […]` … **`ĐỎ  mảnh 3/8 [M-loi]: 1 lỗi đột biến — không ghi tệp`**, `RC=1` (`tam/log/manh3-a.log`) ⇒ job `gate-cong-cu` (matrix 3) ĐỎ, tệp `manh/manh-3.txt` không có ⇒ `gate-cong-cu-gop` ĐỎ (thiếu mảnh).
  · Hệ quả spec §6.1 "delta lỗi đột biến ≤ 0 so nền": **+1** (nền `abc0339`/`577d7b9`: 0).
  · Vì sao executor không thấy: bằng chứng của vòng 8 là 9/470 đột biến (5 chốt mới + 4 #668) và pha ca chế độ gate — chế độ `CONG_CU_TEST_BAN_KINH=manh` in "BÁN KÍNH ĐỘT BIẾN (470 đột biến): GIAO cho job `gate-cong-cu` … KHÔNG đo trong tiến trình này" và `lỗi đột biến=0` là số GIAO, không phải bán kính. Hồi quy nằm ở đúng 1/470.
VÁ Ở ĐÂU: `ops/cong_cu_test.py::t63`, mệnh đề `except BoQuaMoiTruong as ex:` (HINT hunk 3).
VÁ THẾ NÀO: miễn trừ tiền đề của `t27`, giữ (0) cho mọi `BoQuaMoiTruong` khác — `doi_chung_xanh = False if "fail-close" in str(ex) else bang(False, f"(0) đối chứng t49 mà BỎ QUA: {ex}")` (một dòng, trung hoà dòng). Nhánh tiền đề: `t63` đi tiếp như trước vá 8 (vòng `bo_ten` ra "lý do khác" ⇒ `bo_qua`); mã `bang(not doi_chung_xanh, …)`/`raise … đối chứng không XANH` trong vòng lặp (nay là mã chết vì (0) luôn ném) sống lại đúng thiết kế. Phương án KHÔNG chọn (cho chủ kho cân): giới hạn (0) vào hai tiền tố staging (`KHÔNG ĐO ĐƯỢC: INDEX`/`git add`) — đơn giản hơn nhưng để SỐNG lại đột biến "staging ném tiền tố LẠ" mà vòng 8 muốn giết (`T63_LUON_NEM_tien_to_LA`: `abc0339` `BO_QUA`).
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: (0) vẫn giết: `T63_LUON_NEM_tien_to_INDEX`, `T63_LUON_NEM_tien_to_LA`, `T63_ADD_LUON_NEM` ⇒ `giet_that "(0) đối chứng t49 mà BỎ QUA: …"` (đo trên cây áp, (a) và (b)). Miễn trừ được canh bởi CHÍNH cổng bán kính: đột biến "bỏ miễn trừ" (quay về `bang(False, …)`) làm `bn_quet_theo_chuoi` ĐỎ 2/61 (mảnh 3/8 RC=1) — đo trên `02d169f`. Cây áp: `bn_quet_theo_chuoi` ⇒ `ok … bán kính 1/61` (a)(b); 161/161 đột biến `bash_nen.py` đích `giet_that`, t63 ngoài đích: 0; **mảnh 3/8 THẬT trên cây áp: `60/60 đạt`, 59/59 `ok`, ghi `manh-3.txt`, RC=0** (`tam/log/manh3-hint-a.log`).
BẢN VÁ CÓ THỂ ĐẺ RA: (a) miễn trừ dựa vào chuỗi "fail-close" của thông điệp tiền đề: đổi lời `t49` mà không đổi chốt ⇒ (0) lại giết `bn_quet_theo_chuoi` — cổng bán kính ĐỎ ngay (không im lặng), tức fail-closed; (b) một đột biến "staging luôn ném" mà thông điệp có "fail-close" sẽ được miễn — không tự nhiên, không có trong 161; (c) trung hoà dòng ⇒ +420/−42 (không đổi); (d) trên Windows nếu cờ `protectNTFS` KHÔNG đủ (t49 vẫn `bo_qua` vì staging) thì (0) vẫn đỏ (đúng thiết kế chủ kho/handoff §2) — xem NGHIEM-THU-WINDOWS.
HINT (hunk nào): hunk 3 (+ hunk 2 docstring). ĐỘ TIN: cao (hồi quy tái hiện đầu-cuối bằng mảnh thật; bản sửa đo 161 đột biến + 3 đột biến (0) + gate (a)(b)).

### T63-CO-CHI-DO-HIEN-DIEN  [P4]  (VÁ HỜ) Chốt (cờ) `core.protectNTFS=false` chỉ thấy vòng lặp CUỐI của `t63` (`bo_hong`) và dùng `any()` — đột biến "cờ có ở mọi lệnh `update-index` TRỪ lệnh cho tên mang dấu chéo ngược" (đúng chỗ Windows cần cờ) SỐNG
TỆP/DÒNG: `ops/cong_cu_test.py` @`02d169f` `t63` L6503–6504 (`bang(any("core.protectNTFS=false" in lenh for lenh in nhat_ky if "update-index" in lenh), "(cờ) …")`); `nhat_ky.clear()` ở đầu MỖI vòng (L6481).
VẤN ĐỀ: `nhat_ky` bị `clear()` mỗi vòng, nên sau vòng lặp chỉ còn nhật ký của vòng CUỐI = `("update-index", "bo_hong", "hong_")`. Vòng ấy dừng ở staging `hong_` TRƯỚC (3) và (2d) ⇒ chỉ có lệnh `update-index` cho `xau_\xff.py` và `hong_\xff.py` — hai tên KHÔNG cần cờ (handoff §1: `xau_<0xFF>` vào INDEX với mọi protectNTFS). Lệnh cho tên mang dấu chéo ngược (thứ DUY NHẤT Windows bỏ nếu thiếu cờ) chỉ có ở vòng `bo_ten` — không ai đọc. `any()` cũng cho qua nếu chỉ MỘT lệnh có cờ.
ĐO: `CO_NTFS_THIEU_CHO_TEN_CHEO` (`goi_git(["git"] + ([] if b"\x5c" in ten else ["-c","core.protectNTFS=false"]) + […])`) trên `02d169f` ⇒ `SONG`: `t63 qua`, `t49 qua` (Linux). Đối chứng cùng mô phỏng git-Windows: lệnh tên-chéo thiếu cờ ⇒ `t49 bo_qua` (chặn trong thực tế Windows, KHÔNG đo ở đây). Gỡ cờ hoàn toàn / cờ sang `hash-object` / `true` / cờ cấu hình kho ⇒ `(cờ)` (đúng); cờ đặt SAU lệnh con ⇒ `(0)` (git rc=129).
Lời khai: BAO_CAO D-flag "đòi lệnh `update-index` thật … MANG cờ" đúng nghĩa đen "một lệnh nào đó"; khái quát "gỡ cờ ⇒ t63 đỏ" đúng cho gỡ HẲN, không đúng cho gỡ cục bộ.
VÁ Ở ĐÂU: đuôi vòng lặp của `t63` (HINT hunk 4).
VÁ THẾ NÀO: chuyển chốt (cờ) vào CUỐI thân vòng lặp, sau hai chốt `bo_ten`, đo đúng vòng có lệnh cho tên chéo: `bang(cach != "bo_ten" or {"core.protectNTFS=false" in l for l in nhat_ky if "update-index" in l} == {True}, "(cờ) …")` — tập boolean bằng `{True}` ⇒ MỌI lệnh `update-index` đều mang cờ VÀ có ít nhất một (rỗng ⇒ `set()` ≠ `{True}` ⇒ đỏ); xoá khối cuối hàm. Trung hoà dòng.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t63` (cờ). Trên cây áp: `GO_CO_NTFS`, `CO_NTFS_SANG_HASH_OBJECT`, `CO_NTFS_GIA_TRI_TRUE`, **`CO_NTFS_THIEU_CHO_TEN_CHEO`** (trước: SỐNG), `CO_NTFS_VAO_CAU_HINH_KHO` ⇒ `giet_that "(cờ) MỌI update-index phải mang -c core.protectNTFS=false …"`; `CO_NTFS_SAU_LENH_CON` ⇒ `(0)`; nền 9/9 `qua` (a)(b).
BẢN VÁ CÓ THỂ ĐẺ RA: (a) nếu sau này chuyển cờ vào cấu hình kho `_kho` (tương đương trên Windows) thì (cờ) đỏ — cố ý: chốt gắn với ARGV; đổi cơ chế thì sửa chốt cùng lúc; (b) vòng `bo_ten` phải còn gọi `update-index` cho tên chéo (đang có — `(bo_ten)` chốt thứ tự giữ nó); (c) hiệu lực Windows KHÔNG ĐO ĐƯỢC ở đây.
HINT (hunk nào): hunk 4. ĐỘ TIN: cao (SỐNG đo trên `02d169f`, CHẾT đo trên cây áp).

### DO-GIA-DOC-DIA-CHI-TUY-Y  [P4]  (VÁ HỜ) `dat` chặn con trỏ < 64 KiB nhưng handle giả ≈ 2^60 (chính `job`) đưa vào chỗ con trỏ vẫn SIGSEGV cả tiến trình
TỆP/DÒNG: `ops/cong_cu_test.py` @`02d169f` `_k32_gia.dat` L3043–3046 (`ok = … and (p or 0) >= 1 << 16 and …` rồi `ctypes.string_at(p + 16, 4)`).
VẤN ĐỀ: lượt 7 chỉ ra "số đưa làm con trỏ ⇒ SIGSEGV" kèm ví dụ `sizeof(gh)`=144; vá 8 chặn `p < 64 KiB`. Đường thứ ba cùng lớp: handle giả của CHÍNH đồ giả là `H + n` với `H = 1 << 60` (L3032–3033) — một lệch tham số kiểu `SetInformationJobObject(job, 9, job, size)` đưa số ≈ 2^60 vào chỗ con trỏ; `2^60 ≥ 64 KiB` ⇒ qua chặn ⇒ `string_at(2^60+16, 4)` ⇒ SIGSEGV. Đây đúng hình "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba" (CLAUDE.md). Lượt 7 đã ghi phần dư ("địa chỉ hoang LỚN … hiếm") nhưng đo cho thấy nó rơi đúng vào dải handle của đồ giả.
ĐO: `byref(gh)`→`sizeof(gh)` ⇒ `abc0339` KHÁC rc=−11; `02d169f` `giet_that (w1)`. `byref(gh)`→`job` ⇒ `02d169f` **KHÁC rc=−11** (SIGSEGV cả tiến trình, 0 dòng kết quả), (a) và cây áp (b) `(w1)`. Gỡ chặn 64 KiB + sizeof ⇒ rc=−11 (chặn CÓ răng).
VÁ Ở ĐÂU: `_k32_gia.dat` (HINT hunk 1). VÁ THẾ NÀO: `1 << 16 <= (p or 0) < 1 << 48` (địa chỉ người dùng hợp lệ nằm trong [64 KiB, 2^48) trên x86-64/arm64 mặc định; handle giả ≥ 2^60 bị trả FALSE như nhân Windows ERROR_NOACCESS), sửa chú thích cho khớp; trung hoà dòng.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t64` (w1): `SEGV_sizeof_vao_con_tro` và `SEGV_handle_vao_con_tro` ⇒ `giet_that (w1) cha chết mà con còn sống …` (cây áp, (a)(b)); gỡ cận trên 2^48 (`SEGV_handle_go_can_tren`) ⇒ rc=−11 (cận trên CÓ răng).
BẢN VÁ CÓ THỂ ĐẺ RA: địa chỉ người dùng ≥ 2^48 (arm64 LVA/ppc64 52-bit chỉ khi opt-in) bị từ chối ⇒ `(w1)` đỏ oan — không nền nào trong CI; khoảng [64 KiB, 2^48) chưa ánh xạ vẫn SIGSEGV (chỉ chặn bằng thăm dò bộ nhớ — quá nặng cho đồ giả).
HINT: hunk 1. ĐỘ TIN: cao (rc=−11 đo; (w1) đo trên cây áp).

### LOI-KHAI-VA8  [P4]  Vá 8 để lại hoặc sinh vài lời khai lệch phép đo (dạng `env=`/byref ĐÃ VÁ THẬT; xem ĐỐI CHIẾU)
TỆP/DÒNG: docstring `t63` L6454–6455; `t63` vòng lặp L6489–6494; BAO_CAO §2.3, §2.8; thân commit.
VẤN ĐỀ: (a) docstring `t63` còn "nó BỎ QUA (nền không stage được) ⇒ chiều ĐỎ oan không đo ở nền ấy" — vá 8 làm đúng điều ngược (đối chứng BỎ QUA ⇒ `giet_that (0)`); (b) sau (0), `doi_chung_xanh` luôn `True` khi vào vòng lặp ⇒ `bang(not doi_chung_xanh, …)` luôn đỏ và dòng `raise BoQuaMoiTruong("… đối chứng không XANH …")` kế tiếp là MÃ CHẾT (đọc mã; hunk 3 làm nó sống lại); (c) BAO_CAO §2.3 "`lỗi đột biến=0`" ở chế độ gate là số GIAO (xem T63-DOI-CHUNG-0) — và số đột biến thật là **470**, không phải 416 như prompt lượt này/lượt 7; (d) BAO_CAO §2.8 "thêm đúng 1 dòng >118 ký tự": đo `tokenize` dòng thêm so master: `abc0339` 26 → `02d169f` **33** (+7; cả tệp 362 → 369), vì 6 dòng >118 đến từ HINT (không phải cờ) — đúng ở nghĩa hẹp "edit của executor"; (e) `t49` L6425 còn mô tả "Git for Windows bỏ tên ấy với `Ignoring path`" (hành vi TRƯỚC cờ) và `_stage_byte` không có dòng nào nói vì sao có `-c core.protectNTFS=false` (chỉ thông điệp (cờ) ở `t63`).
VÁ Ở ĐÂU/THẾ NÀO: (a)(b) — HINT hunk 2 (docstring) + hunk 3; (c)(d) khai đúng ở thân PR; (e) tuỳ chủ kho (cần thêm một dòng chú thích ⇒ vượt trần 420, KHÔNG đưa vào HINT).
CA KHOÁ: không (chú thích). BẢN VÁ CÓ THỂ ĐẺ RA: không. HINT: hunk 2+3. ĐỘ TIN: cao (đọc + đo).

### NGHIEM-THU-WINDOWS-CON-THIEU  [P2]  VẪN MỞ — không vá được bằng mã ở Linux
TỆP/DÒNG: spec §2B, §6.1–6.3, §8; `ops/cong_cu_test.py` nhánh nt của `_phong_lai` (L53–71), `t64` (k1) thật, `t49`/`t63`.
VẤN ĐỀ: chưa có nghiệm thu §6 trên Windows neo `02d169f` (hiện vật `8da3996` đã MẤT — HANDOFF_WINDOWS ghi). Vá 8 thêm một giả định chưa đo ở Linux: `-c core.protectNTFS=false` làm `t49` từ `bo_qua` thành `qua` trên `windows-latest` (handoff đo trên Git for Windows 2.55.0.windows.5, Python 3.13.1; KHÔNG biết bản Git của runner). Mô phỏng (`tam/gitgia/git`): cờ hiệu lực ⇒ `t49 qua`, `t63 qua`; cờ vô hiệu ⇒ `t49 bo_qua` và **`t63 giet_that "(0)"` ⇒ suite ĐỎ** (trước vá 8 `t63 qua`) — tức vá 8 chuyển "KHÔNG ĐO ĐƯỢC" thành "ĐỎ" nếu giả định sai.
VÁ Ở ĐÂU / THẾ NÀO: chạy tại máy Windows (chủ kho: "Chỉ chạy tại máy"): `python ops/cong_cu_test.py` N/N hai số bằng nhau (không đặt `PYTHONUTF8` ⇒ đi nhánh Job), cùng bộ với `PYTHONIOENCODING=ascii PYTHONUTF8=0`, §6.3 (i)(ii), log staging `t49` (đòi `t49 = qua`, không `bo_qua`), `t64` (k1) thật + `taskkill /F` tiến trình bao, mảnh/gom #668 trên Windows. CA KHOÁ: không áp dụng. BẢN VÁ CÓ THỂ ĐẺ RA: n/a (không có mã). Kết quả Windows có thể ĐẢO nhãn: nếu `t49` vẫn `bo_qua` thì `t63` ĐỎ ở (0) (trước vá 8 `t63` xanh) — khi đó hướng xử lý là chỉnh cờ/đối chứng theo SỐ ĐO Windows, không đoán. HINT: không hunk. ĐỘ TIN: cao.

### TRAN-DONG-DAT-BANG-NEN  [P4]  (đóng MỘT PHẦN) Giãn mã không giảm, vá 8 thêm 7 dòng >118 ký tự
Số đo `tokenize` trên dòng thêm so master `577d7b9` (tệp `cong_cu_test.py`): `;` 9 → 9, walrus 6 → 6, dòng >118: 26 (`abc0339`) → **33** (`02d169f`), dòng dài nhất 154 → 154 (`t64:3068` docstring). Cả tệp: >118: 336 (master) → 362 → 369. Thêm đúng 1 dòng vì cờ (L6316 = 121). HINT KHÔNG thêm dòng >118 mới (hunk 1: `def dat` 123→114, `ok =` 110→120). Thước đo do chủ kho quyết; kho không có luật độ dài dòng.
VÁ Ở ĐÂU/THẾ NÀO: không vá bằng mã (chủ kho quyết thước; HINT không làm giãn thêm). CA KHOÁ: không (không có luật). BẢN VÁ CÓ THỂ ĐẺ RA: không. HINT: không hunk riêng. ĐỘ TIN: cao (đo `tokenize`).

### TEN-CA-LECH-SPEC  [P4]  `t60`–`t64` thay `t52` của spec (quyết định chủ kho: khai ở PR)
`t52_import_bash_nen_khong_in_gi_ra_stderr` 0 lần; `def t60_import_bash_nen_khong_in_gi_ra_stderr` 1 lần (`t52`–`t54` nay là ca #668); `t63`, `t64` ngoài spec r1. Thân PR KHÔNG ĐO ĐƯỢC.
VÁ Ở ĐÂU/THẾ NÀO: khai ở thân PR (quyết định chủ kho), không đổi tên bằng mã. CA KHOÁ: không. BẢN VÁ CÓ THỂ ĐẺ RA: đổi tên ca làm lệch `DOT_BIEN`/bán kính — vì thế KHÔNG đổi. HINT: không hunk. ĐỘ TIN: cao.

## HINT.patch — tự kiểm

- Tệp: `out/HINT.patch` — 65 dòng, sha256 `1adfdfdac7aba232ec938361ed3849550aaddebc26132d757b52bb041c1d74eb`; 4 hunk, MỘT tệp `ops/cong_cu_test.py`; định dạng `git diff --no-prefix` (repo-relative, không `a/` `b/`);
  đầu tệp mang nhãn §8 NGUYÊN VĂN ("chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit") + ánh xạ hunk→finding. MỌI hunk là mã TEST (`_k32_gia.dat`, `t63`) hoặc
  docstring/chú thích ⇒ đủ điều kiện patch-as-hint cho packet `sensitive` (§8 (3)(a)); KHÔNG hunk nào chạm sản phẩm (`_ep_utf8`, `_phong_lai`, khối phóng lại, `main`, `_main_gop`, `_CUA`),
  `bash_nen.py`, `.github/workflows/**`. Ánh xạ: hunk 1 = DO-GIA-DOC-DIA-CHI-TUY-Y [P4] · hunk 2 = LOI-KHAI-VA8 [P4] (docstring) · hunk 3 = **T63-DOI-CHUNG-0 [P1]** · hunk 4 = T63-CO-CHI-DO-HIEN-DIEN [P4].
  NGHIEM-THU-WINDOWS [P2]: không hunk.
- Lệnh tự kiểm (MỘT lệnh dựng hai vế; clone MỚI từ `kho.git`):
  ```
  $ git clone -q kho.git tam/ap && git -C tam/ap checkout -q --detach 02d169f47e9c171d81b17447b93bb70c53f33dc1 && cd tam/ap && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch
  checking file ops/cong_cu_test.py
  hint_dry_run_rc=0
  $ patch -p0 --fuzz=0 < ../../out/HINT.patch          ⇒ patching file ops/cong_cu_test.py · apply_rc=0 · 0 tệp .orig/.rej
  $ cmp tam/ap/ops/cong_cu_test.py tam/fix/ops/cong_cu_test.py ⇒ trùng từng byte (cây sửa dựng độc lập, commit nháp trong tam/)
  $ git diff --numstat 577d7b9 ⇒ 1 1 ops/bash_nen.py · 419 41 ops/cong_cu_test.py ⇒ **+420/−42 (KHÔNG thêm dòng so 02d169f; ≤ trần ~420)**
  $ git diff --numstat 02d169f ⇒ 7 7 ops/cong_cu_test.py (4 hunk, 7 dòng đổi, 0 dòng thêm ròng)
  ```
- TRẦN DÒNG: không vượt (420). Dòng >118 ký tự: cả tệp 369 → 369 (hunk 1: dòng `def dat` 123→114 ký tự, dòng `ok =` 110→120). Dòng dài nhất PR vẫn 154. `;` 9, walrus 6 không đổi.
- Trên cây áp (`tam/ap`, `tam/fix` cùng nội dung): 9 ca `t49 t52 t53 t54 t60–t64` ⇒ `TONG {"qua": 9}` ở (a) VÀ (b); ruff 0.15.15 `--select F` = nền {F401 `ast`, F841 `ci`}; compile `-W error` ×3 (3.11.15/3.12.3/3.13.12) trên `tam/ap`: "sạch" ×3 cho cả hai tệp; 9 ca trực tiếp trên `tam/ap` (a)(b) `TONG {"qua": 9}`, và với python3.11.15/3.13.12 × (a)(b) `TONG {"qua": 9}` ×4; chuỗi miễn trừ "fail-close" chỉ có trong thông điệp tiền đề `t49` (L6384; hai chỗ khác trong `t49` là chú thích);
  `CONG_CU_TEST_BAN_KINH=manh` (a) và (b) trên commit nháp của cây áp (`tam/gha`, `tam/ghb`, 19:29:18Z→19:34:36Z): cả hai `60/60 đạt; tổng=61, bỏ qua=1` · `CỔNG TRÊN CÂY THẬT: ĐẠT` · `TỰ KIỂM SONG SONG: ĐẠT` · `RC=0` · 0 `.pyc` · status sạch.
- Đột biến trên cây áp (khe `slotF1–F3`, mỗi khe MỘT harness): nền 9/9 `qua` trước khi đột biến; `bn_quet_theo_chuoi` ⇒ `ok … bán kính 1/61` (a)(b); quét 161 đột biến `bash_nen.py` (dot_bien_bn.py) ⇒ 161/161 đích `giet_that`, **chỉ 1 đổi so `02d169f`** (`bn_quet_theo_chuoi`: t63 `giet_that` → `bo_qua`), t63 `giet_that` ngoài đích: 0.
  Chết đúng nhãn: SEGV-sizeof/SEGV-handle ⇒ `(w1)`; gỡ cận trên ⇒ rc=−11; K4d ⇒ `(k4) fd 1`; cờ ×5 ⇒ `(cờ)` (kể cả `CO_NTFS_THIEU_CHO_TEN_CHEO`, trước SỐNG); cờ-sau-lệnh-con ⇒ `(0)`; (0) ×3 ⇒ `(0)`; popen-stdin ⇒ `(w2)`.
- Giới hạn: HINT KHÔNG vá P2 Windows; KHÔNG đổi sản phẩm; chưa chạy 7 mảnh còn lại của `gate-cong-cu` trên cây áp (xem KHÔNG ĐO ĐƯỢC) — thay bằng quét 161 đột biến `bash_nen.py` (+309 ngoài, mục HƯỚNG 7).

## KHÔNG ĐO ĐƯỢC

- **Mọi hành vi Windows thật**: Job Object (`TerminateProcess` cha ⇒ con chết), `t64` (k1)/(w*) trên Windows, guard `sys.stderr is not None` của nhánh nt dưới `pythonw`, ctypes/CFUNCTYPE trên Windows x64/x86,
  thời lượng `t64`/mảnh trên `windows-latest`, **hiệu lực thật của `-c core.protectNTFS=false` trên Git for Windows của runner** (handoff đo Git for Windows 2.55.0.windows.5 / Python 3.13.1 / cp1258, hiện vật `8da3996` đã MẤT),
  `t49` có thực sự `qua` (không `bo_qua`) trên Windows — nếu không, `t63` ĐỎ (HƯỚNG 8, mô phỏng). Đây là P2 NGHIEM-THU-WINDOWS: còn mở, không vá được ở Linux.
- **CI thật trên GitHub** (không gọi mạng): mọi kết luận gate/mảnh là MÔ PHỎNG cục bộ đúng lệnh + env của `ci.yml`. Khác runner: không `jsonschema` (⇒ `t2` bỏ qua; không ảnh hưởng `bn_quet_theo_chuoi`), không `shellcheck`
  (có `actionlint`, `rg`), PyYAML 6.0.1 (CI 6.0.3), stdin của bước `run` trên GitHub Actions. **Chỉ chạy THẬT 1/8 mảnh** (mảnh 3, env (a)); 7 mảnh còn lại KHÔNG chạy nguyên mảnh — thay bằng quét từng đột biến
  (161 `bash_nen.py` + 309 ngoài, HƯỚNG 6/7) vì chỉ các đột biến ấy có thể đổi trạng thái của `t49`/`t63`/`t64` (mã vá 8 đụng). Mảnh 3 ở env (b) chỉ đo bằng `do_mot_tay.py`, không chạy trọn mảnh.
- **Số dòng GitHub hiển thị** (+420/−42 "head khai"): không gọi được GitHub; git cục bộ (myers/patience/minimal) khớp, `--histogram` +422/−44.
- **Thân PR #690, `hint_provenance` theo hunk, nguồn gốc fallback `claude-opus-4-8` (153/167 lượt), model/effort thật của executor**: lời khai prompt/commit, KHÔNG ĐO ĐƯỢC ở đây (BAO_CAO nêu hunk gốc `luot7/HINT.patch`; thân commit dẫn
  comment 5933156034/5933157223; trailer `Co-Authored-By: Claude Opus 5.5`).
- **Chữ ký commit**: `02d169f` có khối `gpgsig` (SSH) nhưng `gpg.ssh.allowedSignersFile` chưa cấu hình nên `%G?` = N — danh tính người ký (#566, lease `chua_do_duoc`) KHÔNG ĐO ĐƯỢC.
- **Ctypes callback (libffi closure) của đồ giả** trên nền chặn bộ nhớ ghi+thực thi (SELinux `deny_execmem`): có thể làm `t64` ĐỎ (`MemoryError`) — như lượt 7, không tính finding.
- **Giải thích SEGV ở dải [64 KiB, 2^48) chưa ánh xạ**: chỉ chặn được bằng thăm dò bộ nhớ (quá nặng cho đồ giả) — ghi trong "BẢN VÁ CÓ THỂ ĐẺ RA" của DO-GIA-DOC-DIA-CHI-TUY-Y.
- **Sự cố rig của lượt này (khai)**: (1) đột biến M1R11 lần đầu gõ sai mỏ neo (`lenh[1:2]` làm con thoát ngay ⇒ `tin_dung_gia` 0,5 s) — bỏ, sửa, chạy lại (log cũ vẫn trong `tam/log/van-slot2-b.jsonl`/`van-slot3-b.jsonl` ghi chồng, bản đúng ở cuối);
  (2) một lần chạy HAI harness trên cùng khe `slotF3` ⇒ kết quả lẫn (`T63_LUON_NEM_tien_to_INDEX` ra nhãn `(cờ)`) — bỏ và chạy lại tuần tự từng khe, mọi số trong tệp này lấy từ lần chạy sạch; (3) cột `sot` của harness (`pgrep -f <khe>`) tự khớp
  tiến trình của chính harness nên `sot=1` nghĩa là 0 tiến trình sót; (4) `cwd` của shell từng trôi vào `tam/nen` làm hệ thống nạp CLAUDE.md của bản sao — không ảnh hưởng phép đo.
- **Snapshot**: chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên (lệnh đọc dùng `GIT_OPTIONAL_LOCKS=0` cho `status`).
