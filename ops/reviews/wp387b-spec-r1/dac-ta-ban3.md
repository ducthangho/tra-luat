tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-BAM-LOG-NEN-WINDOWS r1 — mở phép đợi cây trước khi băm log (`run.json`) sang Windows bằng Job Object

- packet_id: LAUNCHER-BAM-LOG-NEN-WINDOWS; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #387 |
| `nguon_cap_viec` | Packet B của #387, tách từ `LAUNCHER-BAM-LOG-SAU-CAY-CHET` r1 (packet A, land `e4fdf09`, PR #1388; hồ sơ `ops/land/pr1388-wp387-land-evidence.yaml`, `landed: true`). Chủ kho 2026-11-19 (phiên điều phối #1206, AskUserQuestion) quyết **bỏ Darwin**, chỉ mở Windows; tên cũ `LAUNCHER-BAM-LOG-NEN-DARWIN-WINDOWS` bỏ. |
| `phu_thuoc` | Packet A đã land trên `master` (`e4fdf09` là tổ tiên của base). |
| `review_class` | `sensitive`: `.claude/dev/launcher.py` + `.claude/dev/launcher_test.py`, cùng lý do với A. Đối chiếu `lease_publish check` khi cấp lease. |
| `base` | `3b647461db7c8ded1bddd9aafc5c6aa5eead223f` lúc soạn; lease ghi OID thật lúc cấp (phải chứa `e4fdf09`). Đo lại §0 nếu base trôi. |

## 0. Hiện trạng

Đo `2026-11-19T05:20Z–05:31Z` trên `3b64746` (tree `306ec6c8…`), Linux, Python 3.13.18, bằng `wc -l`, `sha256sum`, `grep -n`, `nl -ba … | sed -n`, đọc AST bảng đột biến (`python -B -`); mọi lệnh rc 0. `launcher.py` sha256 `f2503d59927f…` 6213 dòng; `launcher_test.py` `37042727f8b8…` 18032 dòng. Reviewer lượt 1 đo lại độc lập lúc `05:26:24Z`, khớp (§11).

`.claude/dev/launcher.py`:
- `VERSION = "1.6.1"` (dòng 102).
- `_thanh_vien_nhom(pgid)` (542): Linux quét `/proc`; Darwin hỏi `ps` với `timeout=15` (583); nền khác trả `None`. KHÔNG đổi ở packet này.
- `_nen_do_cay_truoc_bam()` (605) là chỗ DUY NHẤT quyết nền được đo cây: `return platform.system() == "Linux"`. Đúng ba chỗ gọi: 619, 3041, 3049.
- `_cho_cay_chet_truoc_bam(pid, job, han)` (610): 619 `if not _nen_do_cay_truoc_bam(): return False`; vòng dò, dòng 625 `nhom = _thanh_vien_nhom(pid)`; deadline monotonic chung, kết quả về sau hạn bị bỏ, ngủ `min(0.1, con_sau)`. Tham số `job` chưa dùng.
- `_job_windows(pid)` (906): Job Object với `KILL_ON_JOB_CLOSE` (`LimitFlags = 0x2000`, dòng 959), gán SAU `Popen`; chú thích tự khai khe "cháu sinh trước lúc gán nằm ngoài job". Trả handle hoặc `None`.
- `_pid_trong_job(job)` (977): `[]` = đã chứng minh rỗng · danh sách · `None` = không đọc được. Không ngủ.
- `_cay_da_chet(pid, job)` (1125): dòng 1131 `ds = _pid_trong_job(job) if job is not None else None`, lồng vòng 20 × 0,1 s — KHÔNG được dùng trong hàm đợi.
- Dòng 2499 có sẵn mảnh `if platform.system() == "Linux" else None)` (chỗ khác, không liên quan).
- `lenh_run` (2677): `job = _job_windows(p.pid)` (2889); `ban_ghi["job_windows"] = job is not None` chỉ trên Windows (2893); handle job không đóng trong `lenh_run`. Mốc `ket_thuc = _bay_gio()` 2990; khối đợi 2991–2997 (gọi hàm đợi 2994, bắt `KeyboardInterrupt` 2995–2996, ghi `log_bam_cay_da_chet`/`log_bam_cho_giay` 2997); đọc lại sổ 3001. Quyết xoá bản chụp prompt dòng 3041: `cay_da_chet = log_cay_chet if _nen_do_cay_truoc_bam() else (_thanh_vien_nhom(p.pid) == [])`; điều kiện unlink kết thúc bằng dòng `            and cay_da_chet):`. Dòng 3049 `if not _nen_do_cay_truoc_bam():   # #387: nền khác Linux giữ mốc ở vị trí cũ, sau phép đo xoá prompt` rồi `ket_thuc = _bay_gio()`.
- Hệ quả trên Windows hôm nay: hàm đợi trả `False` ngay; `_thanh_vien_nhom` trả `None` nên bản chụp prompt không bao giờ bị xoá ngay (thiết kế, `_cap_id` quét về sau — `t77`).

`.claude/dev/launcher_test.py`:
- `class San` dòng 177, `__exit__` 184, `shutil.rmtree(self.d, ignore_errors=True)` 185.
- 426 ca `@ca`. `_R387_CHI_LINUX` định nghĩa 14714 (thông điệp nhắc tên packet cũ); đúng **9** dòng `return _R387_CHI_LINUX` (14880, 14888, 14901, 14916, 14931, 14981, 15005, 15028, 15042) trong 9 ca: (a) `r387_m1_chau_ghi_muon_khai_pham_vi_bam`, (a′) `r387_m1_doi_chung_ghi_som_lam_ve_bam_do`, (b) `r387_m1_con_thuong_chung_minh_cay_chet`, (c) `r387_m2_chau_ghi_trong_han_thi_bam_du`, (d) `r387_m2_khong_do_duoc_thi_khong_cho`, (i) `r387_a_nen_khac_giu_moc_ket_thuc_base`, (f) `r387_m1_stop_trong_luc_cho_khong_bi_de`, (g) `r387_m1_prompt_linux_xoa_khi_cay_chet`, (h) `r387_m2_ngat_trong_luc_doi_ghi_bi_ngat`. Khớp hồ sơ land A (`launcher-windows` 44285378703: Windows 332/332, tổng 426, bỏ qua 94 gồm 9 ca r387, hỏng 0). (e) `r387_m2_han_chung_cho_moi_lan_do` và (t) `r387_fixture_teardown_bao_loi_giu_loi_goc` chạy mọi nền.
- (e): `goi()` (14942) luôn truyền `job=None` (14950); (e5) vòng `("Darwin","Windows","FreeBSD")` đòi `False` ngay, 0 lần ngủ.
- Fixture POSIX: `_r387_chay` vá `m._thanh_vien_nhom` bằng bộ ghi vào `m._r387_ds_do`, lưu `m._r387_pgid = so["pid"]`; với `co_chau=False` gọi `_r387_don_dep` SAU khi `_r1252_run` trả về (không trong `finally`); `_r387_don_dep` chờ nhóm về `[]` bằng `m._r387_do_that`, báo lỗi cho cả `False` lẫn `None`; `_r387_don_khi_thoat` (dùng bởi ca có cháu) chạy teardown trước `rmtree`, giữ lỗi gốc bằng `add_note`; `_r387_nhat_ky_kill` gán `os.killpg` vô điều kiện (Windows không có ⇒ `AttributeError`).
- Hằng neo (15061–15067): `_R387_KHOI_MOC` (chứa nguyên văn dòng 3049 kèm chú thích), `_R387_DONG_CAY` (= nguyên văn dòng 3041), `_R387_KHOI_CHO`, `_R387_DONG_DOC_SO`.
- `DOT_BIEN`: 16 mục `r387_*` (15072–15101), không mục nào mang điều kiện nền; trong đó `r387_a_nen_khac_van_do`, `r387_a_nen_khac_ngu_thua` neo vào lời gọi guard ở 619 (ca (e)); `r387_a_nen_khac_doi_moc` neo `_R387_KHOI_MOC`, `r387_a_nen_khac_moc_truoc_unlink` neo `_R387_KHOI_MOC` + `_R387_DONG_CAY` (ca (i)); `r387_ket_thuc_sau_vong_cho` → (a). `DOT_BIEN_HARNESS` có 2 mục `r387_*` (17292, 17295); vòng chạy harness unpack ĐÚNG ba trường `ten, cap, phai_chet` — không có trường nền. Ở bảng sản phẩm khác: `ban_chup_de_lai_tren_dia` (16493) neo `            and cay_da_chet):`, điều kiện `("posix", …)`, ca `t71`; `xoa_prompt_khi_wrapper_vua_thoat` (16497) neo dòng gọi hàm đợi (2994), ca `t76` (t76 bỏ qua trên Windows).
- Runner `--dot-bien`: ca đích của mục bị bỏ qua hết ⇒ `KHONG DO DUOC tren nen nay`; kết luận ở mức CA (`TinHieuChotCa` của đúng ca), không ở mức nhãn trong ca. Không có cờ lọc mục.
- CI chỉ có `ubuntu-latest`/`windows-latest`; ràng buộc chủ kho: không dùng CI Windows cho packet này ⇒ Windows đo NATIVE.

## 1. `write_set`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- **Darwin và mọi nền khác Linux/Windows**: giữ NGUYÊN hành vi A (hàm đợi `False` ngay; xoá prompt theo biểu thức cũ; mốc `ket_thuc` sau phép đo xoá). Nợ có tên **`wp387-darwin-chua-do`** (không có máy macOS, CI không có runner macOS). Không đổi `_thanh_vien_nhom`.
- Linux: không đổi hành vi nào của A.
- Không đóng khe gán job sau `Popen`, không theo dõi breakaway: giới hạn khai ở docstring.
- Không đổi `_cay_da_chet`, `_job_windows`, `_pid_trong_job`, nhánh chụp workspace, `San`, runner đột biến.
- Windows vẫn KHÔNG xoá ngay bản chụp prompt, kể cả khi job đã chứng minh rỗng (giữ `t71`/`t77`).
- Không dùng CI Windows.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `_nen_do_cay_truoc_bam()` trả `platform.system() in ("Linux", "Windows")`; docstring: "Packet B: Linux và Windows; Darwin/nền khác chưa đo (nợ `wp387-darwin-chua-do`)". | `launcher.py` |
| M2 | `_cho_cay_chet_truoc_bam`: thay ĐÚNG dòng 625 bằng MỘT dòng nguyên văn (thụt 8 dấu cách) — **dòng M2**: `nhom = _thanh_vien_nhom(pid) if platform.system() == "Linux" else (_pid_trong_job(job) if job is not None else None)  # #387 B: dò theo nền`. Mỗi vòng dò đúng một lần; mọi phần còn lại của hàm giữ nguyên từng byte. KHÔNG gọi `_cay_da_chet`. Docstring (thay toàn bộ phần mô tả kết quả, dòng 611–617): `True` = phép dò trả rỗng trong nhóm tiến trình POSIX (Linux) hoặc trong Job Object được theo dõi (Windows); rời nhóm (`setsid`), breakaway, hoặc sinh trong khe giữa `Popen` và lúc gán job nằm ngoài phạm vi. `False` ngay (không dò, không ngủ) khi: nền ngoài Linux/Windows; Windows không có job; phép dò trả `None`. Deadline chung bao cả thời gian của phép dò đồng bộ ở hai nền (`/proc` · `QueryInformationJobObject`). Bỏ câu "`job` để dành cho packet B". | `launcher.py` |
| M3 | Dòng 3041 thành `    cay_da_chet = (log_cay_chet and platform.system() != "Windows") if _nen_do_cay_truoc_bam() else (_thanh_vien_nhom(p.pid) == [])`. Dòng `            and cay_da_chet):` giữ nguyên. Chú thích dòng 3049 đổi "nền khác Linux" → "nền khác Linux/Windows". | `launcher.py` |
| M4 | `VERSION = "1.6.1"` → `"1.6.2"`. | `launcher.py` |
| M5 | **Fixture Windows** (POSIX giữ hành vi A). Mọi thứ dưới đây nằm trong `_r387_chay` và các hàm `_r387_*`. (i) **Bắt tay gán job**: `_r387_chay` ghép trước `ma_con` một đoạn mở đầu chờ tệp `<s>/job-da-gan` tối đa 10 s, không thấy thì `sys.exit(3)`. Hàm mới `_r387_boc_job(m, s, that)` trả bộ bọc của `m._job_windows`: vào bộ bọc, nếu `m._r387_job` khác `None` ⇒ ca ĐỎ ("r387 fixture: job cu chua dong") và KHÔNG gọi `that`; gọi `that(pid)`; trả `None` ⇒ không phát dấu, trả `None`; trả handle ⇒ lưu `m._r387_job = handle`, RỒI gọi `_r387_bao_da_gan(m, s)` — hàm này đòi `m._r387_job is not None` ("r387 fixture: bao gan khi chua luu handle") rồi mới ghi `job-da-gan`. `_r387_chay` cài bộ bọc trên MỌI nền (POSIX: `lenh_run` không gọi `_job_windows`, vô hại) bằng `that` = `m._job_windows` lúc vào `_r387_chay`; trên POSIX ghi sẵn `job-da-gan` trước khi chạy. Quyền sở hữu job được ghi ĐÚNG lúc gán (trong bộ bọc), không đợi `_r1252_run` trả. Sau `lenh_run`: mọi ca đòi `so["ma_thoat"] != 3`; Windows đòi thêm `so.get("job_windows") is True` và `m._r387_job` khác `None`. (ii) Bộ ghi phép dò: `do=` thay phép dò của nền hiện tại (Linux `_thanh_vien_nhom`, nhận pid; Windows `_pid_trong_job`, nhận handle) và nhận đúng đối số của phép dò nó thay; mọi danh sách trả (của phép dò nền hiện tại) ghi vào `m._r387_ds_do`; `m._r387_do_that` = bản THẬT của phép dò nền hiện tại; `m._r387_do_job` = `m._pid_trong_job` lúc vào `_r387_chay` (mọi nền; teardown nhánh job chỉ dùng nó); `m._r387_nen = platform.system()`. Tham số mới `do_nhom=` thay `m._thanh_vien_nhom` trên mọi nền. (iii) **Teardown** (`_r387_don_dep`): nếu `m._r387_job` khác `None` ⇒ nhánh job: chờ `m._r387_do_job(h)` về `[]` bằng `_r387_cho_cay_rong` (ba trạng thái) bên trong `try`, phép dò ném thì đổi thành lỗi "phep do nem <kiểu>"; trong `finally` của khối chờ, gọi đóng ĐÚNG MỘT lần, viết thành hai dòng tách rời `ket_dong = m._r387_dong_job(h)` rồi `if ket_dong == 0:` (mặc định `ctypes.windll.kernel32.CloseHandle`; hàm đóng ném cũng đổi thành lỗi), gán `m._r387_job = None` ngay sau lời gọi (không gọi lại, kể cả khi thất bại); thông điệp lỗi khi chờ ra `False` ("con thanh vien"), `None` ("cay khong do duoc"), phép dò/hàm đóng ném, hoặc `ket_dong == 0` ("CloseHandle that bai" — thông điệp nói rõ handle CHƯA đóng được); nhiều lỗi thì nối. `_r387_don_dep` KHÔNG BAO GIỜ ném (mọi ngoại lệ thành thông điệp), để `add_note` luôn chạy được khi đã có lỗi gốc. Không có job mà `getattr(m, "_r387_nen", None) == "Windows"` ⇒ lỗi "khong co job de chung minh cay rong". Còn lại ⇒ nhánh pgid của A (không đổi). (iv) **Quyền sở hữu dưới `finally`**: `_r387_chay` bọc lời gọi `_r1252_run` và các kiểm sau nó trong `try`; với `co_chau=False`, `_r387_don_dep` chạy trong `finally` — lỗi gốc (cùng đối tượng) giữ nguyên và nhận thông điệp teardown qua `add_note`; không có lỗi gốc mà teardown lỗi ⇒ ca ĐỎ. Với `co_chau=True`, `_r387_don_khi_thoat` (đặt sau `San()`) giữ vai đó như A. Hệ quả: `San.__exit__` (`rmtree(ignore_errors=True)`) chỉ chạy SAU teardown; teardown không chứng minh được cây rỗng thì ca đã ĐỎ — thư mục sót không còn bị nuốt im lặng. (v) `_r387_nhat_ky_kill` chỉ đọc/lưu/thay/khôi phục `os.killpg` khi `hasattr(os, "killpg")`. | `launcher_test.py` |
| M6 | **Ca**: thay `_R387_CHI_LINUX` bằng `_R387_CHI_LINUX_WINDOWS` ("BO QUA r387 chi do tren Linux va Windows; nen khac: no wp387-darwin-chua-do") và đổi guard của 9 ca thành `platform.system() not in ("Linux", "Windows")`. Thay đổi riêng: (a), (c): vế PID cháu đọc `m._r387_ds_do` (Windows = danh sách `_pid_trong_job` của đúng job đã gán). (d): `do=lambda _x: None`; vế thời gian đổi thành `so["log_bam_cho_giay"] < 0.5` (đo riêng đoạn đợi, thay `dt < 3.0` đo cả dựng kho). (f): `do_roi_stop` nhận đối số của phép dò nền hiện tại, chuyển tiếp cho `m._r387_do_that`. (a′): chỉ chấp nhận lỗi vế băm khi lỗi KHÔNG mang ghi chú teardown — tách điều kiện thành hàm `_r387_loi_bam_hop_le(e)` (`"ve bam" in str(e)` VÀ không có `__notes__` chứa `"r387 teardown"`); lỗi băm kèm ghi chú teardown ⇒ (a′) ĐỎ, thông điệp kèm ghi chú. (g): giữ ID; Linux như A; Windows: `log_bam_cay_da_chet is True`, tệp bản chụp CÒN, không có khoá `prompt_ban_chup_da_xoa` (nhãn "r387(g) Windows xoa ban chup"). (h): mỗi lượt h1/h2 là một job riêng (đóng trong `finally` của lượt đó); không đổi logic. (i): phép dò giả ngủ 0,5 s rồi trả `[]` truyền qua `do_nhom=`. **(e)**: `goi()` nhận thêm `job=None`; (e1)–(e4) giữ nguyên. (e5) vòng `("Darwin", "FreeBSD")`, `job=object()`, `_thanh_vien_nhom` và `_pid_trong_job` đều vá thành hàm làm ca ĐỎ ⇒ `False` ngay, 0 lần ngủ. (e6) nền Windows, `job=object()`, `_pid_trong_job` luôn `[7]`, `_thanh_vien_nhom` vá thành `bang(False, "r387(e6) goi _thanh_vien_nhom tren Windows")`, `_cay_da_chet` vá thành `bang(False, "r387(e6) goi _cay_da_chet")` ⇒ `False` trong ≤ 1,0 s. (e7) Windows, `job=None` ⇒ `False`, 0 lần ngủ, `_pid_trong_job` không được gọi. (e8) Windows, `job=object()`, `_pid_trong_job` trả `[7]` lần đầu rồi `[]` ⇒ `True`. (e9) Linux, `job=object()`, `_pid_trong_job` vá thành `bang(False, "r387(e9) Linux goi _pid_trong_job")`, `_thanh_vien_nhom` trả `[]` ⇒ `True`. **(t)**: vế cũ giữ nguyên (đặt `m._r387_job = None`, nên đi nhánh pgid). Vế mới (t2) đóng thành công: `m._r387_job = object()`, `m._r387_do_job` ghi `("do",)` vào trace cục bộ rồi trả `[]`, `m._r387_dong_job` ghi `("dong",)` rồi trả `1` ⇒ `_r387_don_dep` trả `None`, trace đúng `[("do",), ("dong",)]`, `m._r387_job is None`. (t3) `CloseHandle` thất bại: như (t2) nhưng hàm đóng trả `0` ⇒ thông điệp chứa `"CloseHandle that bai"`, trace có đúng một `("dong",)` (nhãn "r387(t3) CloseHandle that bai khong bao"); (t3b) phép dò trả `None` VÀ hàm đóng trả `0` ⇒ thông điệp chứa cả `"cay khong do duoc"` lẫn `"CloseHandle that bai"`; (t3c) phép dò ném `OSError` ⇒ `_r387_don_dep` không ném, thông điệp chứa `"phep do nem"`, hàm đóng vẫn được gọi đúng một lần (nhãn "r387(t3c) do nem ma khong dong"). (t4) bắt tay, với `that_gia` đếm số lần gọi và ghi `job-da-gan` có tồn tại không lúc nó chạy: (t4a) `that_gia` trả `object()` ⇒ lúc nó chạy tệp CHƯA có, sau khi bộ bọc trả thì tệp CÓ và `m._r387_job` là đúng handle ấy (nhãn "r387(t4) job-da-gan ghi truoc khi gan"); (t4b) `that_gia` trả `None` ⇒ tệp KHÔNG có, `m._r387_job is None` (nhãn "r387(t4b) gan that bai van phat dau"); (t4c) gọi khi `m._r387_job` chưa đóng ⇒ lỗi "job cu chua dong" được bắt và `that_gia` KHÔNG được gọi thêm; (t4d) `_r387_bao_da_gan` gọi khi `m._r387_job is None` ⇒ lỗi "bao gan khi chua luu handle". (t5) teardown dưới `finally` (X1, tất định): vá biến toàn cục `_r1252_run` của tệp test bằng hàm giả gọi `m._job_windows(1)` (đã vá trước `_r387_chay` thành hàm trả `object()`, nên bộ bọc nhận quyền sở hữu) rồi ném `TinHieuChotCa("SENTINEL")`; `m._pid_trong_job` vá trước thành `lambda h: None`, `m._r387_dong_job` đếm lời gọi trả `1`; gọi `_r387_chay(..., co_chau=False)` ⇒ bắt được ĐÚNG đối tượng sentinel, `__notes__` chứa `"r387 teardown"` và `"cay khong do duoc"`, hàm đóng gọi đúng 1 lần (nhãn "r387(t5) teardown khong chay khi ne"). (t6) `_r387_loi_bam_hop_le`: lỗi `"ve bam"` không ghi chú ⇒ `True`; cùng lỗi có ghi chú `"r387 teardown: CloseHandle that bai"` ⇒ `False` (nhãn "r387(t6) loi bam nuot loi teardown"). (t2)–(t6) chạy mọi nền; mọi vá khôi phục trong `finally`. | `launcher_test.py` |
| M7 | **Neo và bảng đột biến**: cập nhật CẢ `_R387_KHOI_MOC` (theo chú thích mới M3) LẪN `_R387_DONG_CAY` (theo dòng M3), để mỗi mẫu của `r387_a_nen_khac_doi_moc`/`r387_a_nen_khac_moc_truoc_unlink` khớp đúng một chỗ (`t117`). Bốn mục `r387_a_nen_khac_*` giữ tên, ca đích; hai mục neo guard giữ nguyên mẫu. Thêm vào `DOT_BIEN` **6** mục mới W1–W6 (§4b); thêm vào `DOT_BIEN_HARNESS` **7** mục mới H1–H7. W7–W12 tái dùng mục có sẵn của A. | `launcher_test.py` |

## 4. `nghiem_thu`

Mọi số công bố kèm thời điểm UTC tới giây, phiên bản công cụ, lệnh nguyên văn, mã thoát.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux (head): (e), (t) và 9 ca mở ĐẠT; mọi ca r387 của A giữ kết quả. | Mỗi mục W1–W4, W6, H1–H7 qua runner `--dot-bien` ⇒ `OK giet 1/1` đúng ca đích. Ngoài runner (vốn chỉ kết luận ở mức CA), executor đo NHÃN: áp từng mục vào bản sao đủ cây, chạy `--lap-ca <ca đích> --lan 1`, lấy dòng chi tiết DUY NHẤT có dạng `HONG <ID ca đích>: <lý do>` (sau khi bỏ thụt lề; KHÔNG phải dòng tổng `lan 1/1: HONG`); `<lý do>` phải chứa nhãn ở cột "nhãn đỏ" của §4b. Không có đúng một dòng như thế, hoặc nhãn khác ⇒ mục đó tính SAI (tín dụng giả) dù runner báo giết. |
| N2 | `t117` ĐẠT trên head. | Bỏ cập nhật `_R387_KHOI_MOC` ⇒ mẫu `r387_a_nen_khac_doi_moc` khớp 0 chỗ ⇒ `t117` ĐỎ; bỏ cập nhật `_R387_DONG_CAY` ⇒ mẫu thứ hai của `r387_a_nen_khac_moc_truoc_unlink` khớp 0 ⇒ ĐỎ. Executor chạy cả hai phản chứng, ghi rc. |
| N3 | `launcher_test.py` trên head (Linux, gate + tại chỗ): N/N, hai số bằng nhau; TẬP ID bỏ qua của head ⊆ của base (không thêm bỏ qua mới). `--dot-bien`: rc 0, `DOT BIEN: N/N dat`; tập mục `KHONG DO DUOC tren nen nay` của head = của base ∪ {W5}. | Tập ID bỏ qua head có ID ngoài base; hai số dòng cuối khác nhau; tập `KHONG DO DUOC` khác kỳ vọng. |
| N4 | **Windows NATIVE** trên Desktop `DESKTOP-T9R33P2` (VM `tra-luat-win` dự phòng), exact head (`git rev-parse HEAD` = head, cây sạch), ghi `python --version`, `platform.platform()`, giờ UTC. (L1) (e), (t), 9 ca mở, `t71`, `t77`: mỗi ca `1/1 qua, 0 bo qua, 0 hong` qua `python .claude/dev/launcher_test.py --lap-ca <ca> --lan 1`. **Toàn suite** Windows (`python .claude/dev/launcher_test.py`) trên head VÀ base `3b64746` cùng máy cùng lượt: log head KHÔNG có dòng `BO QUA r387`; tập ID bỏ qua head = tập ID bỏ qua base trừ đúng 9 ID r387 ở §0 (so TẬP, không so tổng). (L2) Đột biến trên Windows: bản sao đủ cây của exact head (`git archive`); trong tệp test của bản sao: `DOT_BIEN_HOOK = []`; thân danh sách `DOT_BIEN` và `DOT_BIEN_HARNESS` được thay bằng nguyên văn đoạn nguồn (`ast.get_source_segment`) của từng phần tử có ID bắt đầu `r387_`, mỗi phần tử một dòng kết thúc bằng dấu phẩy, GIỮ NGUYÊN hai mốc runner dùng để tách bảng harness (`\nDOT_BIEN_HARNESS = [` và `\n]\n\n\ndef chay_dot_bien()`) — `]` đóng phải đứng dòng riêng; các hằng `_R387_*` ở mức module không đụng tới. Trước khi chạy: bản sao `py_compile` rc 0, đếm `len(DOT_BIEN)=22`, `len(DOT_BIEN_HOOK)=0`, `len(DOT_BIEN_HARNESS)=9`, tập ID = 16 ID r387 cũ của `DOT_BIEN` + {W1–W6 ở §4b} và 2 ID r387 cũ của harness + {H1–H7}, không trùng; ghi sha256 tệp đã lọc. W5 bắt buộc `OK giet 1/1`; mọi mục khác kỳ vọng như Linux. Đo nhãn như N1 cho W5 và W7. (L3) (a), (c) mỗi ca `--lan 5` trên Windows: 5/5. | Ca L1 `bo qua`/`hong`; log head còn `BO QUA r387`; hiệu tập ID khác đúng 9 ID r387; mục L2 sống, chết sai ca, hoặc nhãn sai; số mục từng bảng khác 22/0/9 hoặc tập ID khác kỳ vọng. Thiếu job, con thoát mã 3, PID cháu không có trong phép dò job, thiếu `chau-xong`, teardown lỗi ⇒ ca ĐỎ bằng `TinHieuChotCa`, không thành bỏ qua. HEAD khác exact head ⇒ N4 vô hiệu. Chưa có log native ⇒ `chưa đo được`. |
| N5 | Một lượt `run` thật trên Windows native: `python .claude/dev/launcher.py run <cờ bắt buộc của hợp đồng run, ghi nguyên văn> -- python -c "import time;time.sleep(2);print(1)"` (con sống 2 s để `_job_windows` kịp gán). `run.json`: `"version": "1.6.2"`, `ma_thoat` 0, `job_windows: true`, `log_bam_cay_da_chet: true`, `log_bam_cho_giay` < 10. | Thiếu một khoá hoặc giá trị khác. |
| N6 | `git diff --numstat base..H` đúng 2 tệp write set, tổng cột thêm ≤ 450; Ruff 0.15.15 `--select F` tập diagnostic head = base trên 2 tệp; `doctrine-scan`, `adr-song` rc 0; `git diff --check` rỗng; `eol_policy --all` ok. | Đường dẫn thứ ba, tổng thêm > 450, diagnostic Ruff mới, `diff --check` có dòng, `eol_policy` không ok ⇒ ĐỎ. (`doctrine-scan`/`adr-song`: không có phản chứng riêng ở packet này — khai thẳng.) |

### 4b. Bảng đường vào và chốt (danh sách CHO PHÉP: mọi đường M1–M5 mở ra đều có một hàng; mỗi hàng một chốt, một phép đo làm đỏ)

Mẫu "trọn dòng M2" = nguyên văn dòng M2 (§3), khớp đúng một chỗ; các mảnh con của nó KHÔNG được làm mẫu riêng vì đã có ở 1131 và 2499.

| # | đường vào / chốt | đột biến (tìm → thay) | ca đích & nhãn đỏ | nền đo |
|---|---|---|---|---|
| W1 `r387_b_windows_khong_do` | Windows thuộc tập nền được đo (M1) | `return platform.system() in ("Linux", "Windows")` → `return platform.system() in ("Linux",)` | (e8) "r387(e8)…" (`False` thay `True`) | Linux + Windows |
| W2 `r387_b_windows_dung_nhom` | Windows dò job, không dò nhóm POSIX (M2) | trọn dòng M2 → `nhom = _thanh_vien_nhom(pid)  # #387 B: dò theo nền` | (e6) "r387(e6) goi _thanh_vien_nhom tren Windows" | Linux + Windows |
| W3 `r387_b_job_none_thanh_rong` | Windows thiếu job ⇒ không đo được (M2) | trọn dòng M2 → cùng dòng, `else None)` cuối thành `else [])` | (e7) "r387(e7)…" (`True` thay `False`) | Linux + Windows |
| W4 `r387_b_windows_long_cay_da_chet` | Windows không dùng `_cay_da_chet` (M2) | trọn dòng M2 → cùng dòng, `_pid_trong_job(job)` thành `([] if _cay_da_chet(pid, job) else [7])` | (e6) "r387(e6) goi _cay_da_chet" | Linux + Windows |
| W5 `r387_b_windows_xoa_prompt_khi_job_rong` | Windows KHÔNG xoá bản chụp kể cả khi job rỗng (M3) | `(log_cay_chet and platform.system() != "Windows")` → `log_cay_chet`; điều kiện `("windows", "POSIX xoa ban chup khi cay chet; chi Windows giu")` | (g) "r387(g) Windows xoa ban chup" | chỉ Windows |
| W6 `r387_b_linux_di_nhanh_job` | Linux dò nhóm, không đi nhánh job (M2) | trọn dòng M2 → cùng dòng, `"Linux"` thành `"LinuxX"` | (e9) "r387(e9) Linux goi _pid_trong_job" | Linux + Windows |
| W7 | Mốc `ket_thuc` lấy TRƯỚC khi đợi — Windows nay đi đường Linux (M1) | tái dùng `r387_ket_thuc_sau_vong_cho` (A) | (a) nhãn lệch mốc `ket_thuc_utc` (đo nhãn N4 L2) | Windows (đo lại mục A) |
| W8 | Darwin/nền khác: `False` ngay, không dò, không ngủ | tái dùng `r387_a_nen_khac_van_do`, `r387_a_nen_khac_ngu_thua` (A) | (e5) — `job=object()` nên bỏ guard ⇒ đi nhánh job ⇒ chạm bẫy; thêm ngủ ⇒ `ngu != []` | Linux + Windows |
| W9 | Nền khác giữ mốc `ket_thuc` sau phép đo xoá; nền khác vẫn xoá theo biểu thức base | tái dùng `r387_a_nen_khac_doi_moc`, `r387_a_nen_khac_moc_truoc_unlink` (A, neo hai hằng mới) | (i) nhãn mốc; vế `prompt_ban_chup_da_xoa is True` của (i) đo biểu thức base | Linux + Windows |
| W10 | Job có handle nhưng truy vấn trả `None` ⇒ `False` ngay | tái dùng `r387_khong_do_duoc_van_cho` (A, neo `if nhom is None:` — chung hai nền) | (d) trên Windows: `do=` trả `None` ở nhánh job | Linux + Windows |
| W11 | Kết quả dò về sau hạn bị bỏ; ngủ trừ thời gian dò | tái dùng `r387_nhan_ket_qua_sau_han`, `r387_ngu_khong_tru_lan_do` (A, thân vòng chung hai nền) | (e2)/(e4) | Linux + Windows |
| W12 | `stop` trong lúc đợi; Ctrl-C trong lúc đợi; kết quả chụp không bị ngắt che | tái dùng `r387_cho_sau_doc_lai_stop`, `r387_ngat_*` (A) | (f), (h) — nay chạy native trên Windows | Windows (đo lại mục A) |
| H1 `r387_fx_dong_truoc_khi_cho` | Teardown chờ job rỗng TRƯỚC khi đóng handle (M5 iii) | trong `_r387_don_dep` nhánh job: dời dòng `ket_dong = m._r387_dong_job(h)` lên trước khối chờ (mẫu nguyên văn khi viết) | (t2) "r387(t2) thu tu do/dong" (trace `[("dong",),("do",)]`) | Linux + Windows |
| H2 `r387_fx_bao_gan_truoc_khi_gan` | Bắt tay: dấu chỉ phát SAU khi gán thành công (M5 i) | trong `_r387_boc_job`: dời lời gọi `_r387_bao_da_gan(m, s)` lên trước `that(pid)`, bỏ chốt "đã lưu handle" trong `_r387_bao_da_gan` để mutant không chết ở chốt khác | (t4a) "r387(t4) job-da-gan ghi truoc khi gan" — tất định; hai thay thế áp tuần tự (dời lời gọi; bỏ chốt) |  Linux + Windows |
| H3 `r387_fx_bo_kiem_closehandle` | Hàm đóng trả 0 ⇒ lỗi teardown (M5 iii) | `if ket_dong == 0:` → `if False:` (lời gọi đóng giữ nguyên) | (t3) "r387(t3) CloseHandle that bai khong bao" | Linux + Windows |
| H4 `r387_fx_khong_dong_job` | Teardown đóng handle đúng một lần (M5 iii) | `ket_dong = m._r387_dong_job(h)` → `ket_dong = 1` (biên dịch được, tới được assertion trace) | (t2) "r387(t2) thu tu do/dong" (trace thiếu `("dong",)`) | Linux + Windows |
| H5 `r387_fx_phat_dau_khi_gan_hong` | Gán thất bại không phát dấu (M5 i) | trong `_r387_boc_job`, nhánh `that(pid)` trả `None`: chèn ghi THẲNG `job-da-gan` trước khi trả (không qua `_r387_bao_da_gan`, để mutant không chết ở chốt khác; mẫu nguyên văn khi viết) | (t4b) "r387(t4b) gan that bai van phat dau" | Linux + Windows |
| H6 `r387_fx_don_dep_ngoai_finally` | Teardown `co_chau=False` chạy dưới `finally` khi `_r1252_run` ném (M5 iv, X1) | dời lời gọi `_r387_don_dep` của `co_chau=False` ra khỏi `finally` (sau khối `try`) | (t5) "r387(t5) teardown khong chay khi ne" | Linux + Windows |
| H7 `r387_fx_loi_bam_nuot_teardown` | (a′) không nuốt lỗi teardown (M6) | trong `_r387_loi_bam_hop_le`: bỏ vế kiểm `__notes__` | (t6) "r387(t6) loi bam nuot loi teardown" | Linux + Windows |
| X1 | Phép dò/hàm đóng ném trong teardown | đo bằng (t3c); đột biến bỏ `try` quanh phép dò làm (t3c) ĐỎ bằng `OSError` lọt ra — đó là tín dụng giả theo định nghĩa nên KHÔNG đưa vào bảng; (t3c) giữ vai ca hành vi | (t3c) | Linux + Windows |
| X2 | `os.killpg` vắng trên Windows (M5 v) | không đột biến: gỡ `hasattr` chỉ làm ca chết bằng `AttributeError` — tín dụng giả theo định nghĩa | đo bằng N4 L1 (ca có `_r387_nhat_ky_kill` ĐẠT trên Windows) | Windows |
| X3 | `VERSION` (M4) | không đột biến | N5 `"version": "1.6.2"` | Windows |

Mẫu (tìm, thay) của H1–H7 chốt nguyên văn khi executor viết mã, mỗi mẫu khớp đúng một chỗ trong phần mã test (kiểm neo harness). Mọi đột biến chỉ tính GIẾT khi ca đích đỏ bằng `TinHieuChotCa` của đúng ca, ca đích ĐẠT trên bản sạch, và (N1/N4) nhãn khớp.

## 5. `pham_vi_e`

Không chạm E4, không chạm E5.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint (`docs/PROTOCOL_DA_PHIEN.md` §12); xin tăng mang **E2**, ghi mức đã dùng, phần thiếu và mục đích (`ADR-0067`).
- Trần kích thước `ADR-0053` (450 dòng thêm, `git diff --numstat base..H` toàn diff). > 450 ⇒ DỪNG, không push, báo điều phối; không cắt ca/phép đo để lọt trần.
- Chưa có log native Windows (N4, N5) ⇒ không công bố `landed`/`ready`.
- Cần sửa ngoài write set (§1; §2 cấm sửa `San`, runner đột biến) ⇒ dừng, đổi Packet Spec theo `docs/PROTOCOL_DA_PHIEN.md` §12 (revision mới, băm mới, chủ kho duyệt — E2).
- Dung sai (a) 1,8–2,5 s và (e6) ≤ 1,0 s là điều kiện nghiệm thu của N1/N4: vượt trên Windows ⇒ N4 ĐỎ, không tự nới; nới hoặc đổi hàm đợi ⇒ đổi Packet Spec như trên.
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm (`ADR-0067`) — **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung` — phần nền của một packet tách (#387 A → B), không phải packet khắc phục bản vá cũ. Hai finding mở mang sang từ review A ghi ở §9.

## 8. `chua_do_duoc`

- Toàn bộ hành vi Windows native (bắt tay giữ con tới lúc gán, cháu trong job, job cập nhật trễ, `CloseHandle` thật): N4/N5 là phép đo duy nhất.
- Darwin: không đo (nợ `wp387-darwin-chua-do`).
- Giới hạn có tên: cháu breakaway hoặc sinh trong khe `Popen`→gán job ⇒ `true` có thể sai.
- POSIX: quyền sở hữu nhóm (`m._r387_pgid`) vẫn chỉ ghi SAU khi `_r1252_run` trả (hành vi A, không đổi ở packet này); `_r1252_run` ném sau khi đã sinh con thì teardown nhánh pgid không có tham chiếu. Ghi nợ `wp387-pgid-so-huu-muon`. Windows không mắc vì quyền sở hữu job ghi lúc gán (M5 i).
- Dung sai (a) 1,8–2,5 s và (e6) ≤ 1,0 s mới đo trên Linux.
- Kích thước, ước lượng theo khối tương tự trên base (đo `2026-11-19T05:31Z`): `launcher.py` ~ +8/−6 (M1 1, M2 1 + docstring ~4, M3 1, chú thích 1, M4 1). `launcher_test.py`: fixture A hiện tại (`_r387_cho_cay_rong` → `_r387_chay`, 14728–14808) ~80 dòng; phần Windows thêm (bắt tay, bộ bọc, nhánh job của teardown, `finally`, `hasattr`) ước ~45–70; (e6)–(e9) ~25–35 (so (e1)–(e5) ~30 dòng); (t2)–(t4) ~30–40 (so (t) ~18 dòng); (g)/(d)/(f)/(i) ~10–15; guard 9 ca ±0; bảng 10 mục ~15–25. Tổng ~140–200, reviewer lượt 1 ước 180–300; ≤ 450. Đo lại bằng numstat.

## 9. Quyết định đã ghi

- **Q-D (2026-11-19, chủ kho, AskUserQuestion, phiên #1206):** bỏ Darwin khỏi B, chỉ mở Windows; Darwin giữ hành vi A; nợ có tên `wp387-darwin-chua-do`.
- **Q-W (cùng quyết định):** tên packet `LAUNCHER-BAM-LOG-NEN-WINDOWS` r1; 4 đột biến `r387_a_nen_khac_*` giữ, tiếp tục đo đường "không phải Linux/Windows" qua (e5) Darwin/FreeBSD và (i).
- **Finding mở từ review A, đóng ở bản này:** P2 teardown Windows — M5(i)(iii)(iv) + M6(a′): quyền sở hữu job ghi lúc gán; chờ job rỗng rồi mới đóng (đóng trong `finally` kể cả khi phép dò ném); kiểm giá trị trả `CloseHandle`; báo lỗi cho `False`/`None`/ném/`CloseHandle=0`; teardown không bao giờ ném; dưới `finally` và chạy trước `rmtree`; (a′) không nuốt ghi chú teardown (H1, H3–H4, H6–H7, (t2)–(t6)). Phần POSIX còn lại ghi nợ `wp387-pgid-so-huu-muon` (§8). P3 đếm `BO QUA` — so TẬP ID trên log Windows native head vs base (N4 L1).

## 10. Nhật ký

- 2026-11-18: bản Darwin+Windows dựng trên vá thử `trA` (`rv387b/dac-ta-ban0.md`).
- 2026-11-19: đo lại trên base thật `3b64746` (`rv387b/dac-ta-ban0b-darwin-c1cbe870.md`); chủ kho bỏ Darwin; viết lại thành bản 1 (`rv387b/dac-ta-ban1.md`, sha256 `7b1f2324…`); bản 2 (`rv387b/dac-ta-ban2.md`, `24d06138…`); bản 3 sau lượt 2.

## 11. Nhật ký review

- **Lượt 1** (Codex, read-only, worktree `3b64746`; verdict `rv387b/luot1.verdict.txt`): `request_changes` — 1 P1, 7 P2, 3 P3. Sửa ở bản 2:
  - P1 `_R387_DONG_CAY` bị bỏ sót ⇒ M7 cập nhật cả hai hằng; N2 thêm hai phản chứng.
  - P2 (e9)/W6 thiếu job giả ⇒ `goi()` nhận `job=`; (e5)/(e6)/(e8)/(e9) dùng `job=object()`; nhãn riêng từng bẫy.
  - P2 H2 phụ thuộc lịch ⇒ bắt tay tách thành `_r387_boc_job`, đo tất định bằng (t4).
  - P2 runner: harness không có trường nền ⇒ H1–H4 đều chạy mọi nền qua (t2)–(t4); lọc bằng nút nguồn thay `literal_eval`; đo nhãn ngoài runner (N1, N4).
  - P2 §4b thiếu đường ⇒ thêm W10–W12, H4, X1–X3.
  - P2 teardown ⇒ M5(iii)(iv): `finally`, ba loại lỗi, đóng một lần, (t) cũ đi nhánh pgid tất định (chọn nhánh theo `m._r387_job`).
  - P2 N5 con quá ngắn ⇒ con sống 2 s, đòi `ma_thoat` 0.
  - P3 vị trí §0 ⇒ sửa (2990/2991–2997/3001, `San` 177/184/185, `ban_chup_de_lai_tren_dia` 16493).
  - P3 gỡ guard ra cả nền khác ⇒ giữ guard cho nền ngoài Linux/Windows (`_R387_CHI_LINUX_WINDOWS`).
  - P3 đếm bỏ qua ⇒ so TẬP ID.
  - Ghi thêm: (d) đo `log_bam_cho_giay` thay thời gian toàn ca; (h) bỏ miễn mã 3.
- **Lượt 2** (Codex, read-only, `3b64746`; `rv387b/luot2.verdict.txt`): `request_changes` — 5 P2, 2 P3; xác nhận đóng 7/11 finding lượt 1 (P1 `_R387_DONG_CAY`, (e9)/W6, phụ thuộc lịch H2, trường nền harness, N5, vị trí §0, guard nền khác + đếm theo tập). Sửa ở bản 3:
  - P2 đọc nhãn ⇒ N1 lấy dòng `HONG <ID ca đích>: …`, không phải dòng tổng.
  - P2 lọc nút nguồn ⇒ `DOT_BIEN_HOOK = []`, giữ hai mốc tách, `]` dòng riêng, kiểm compile + 22/0/9 + tập ID; chốt ID cho W1–W6/H1–H7.
  - P2 teardown ⇒ quyền sở hữu job ghi lúc gán; đóng trong `finally` kể cả khi dò ném; `_r387_don_dep` không ném; (t3b)/(t3c)/(t5) + H6; phần POSIX ghi nợ `wp387-pgid-so-huu-muon`.
  - P2 (a′) nuốt ghi chú teardown ⇒ `_r387_loi_bam_hop_le` + (t6) + H7.
  - P2 H1–H4 ⇒ H3/H4 tách dòng gọi/kiểm; (t4) mở bốn đường (t4a–t4d) + H5.
  - P3 docstring M2 ⇒ thay toàn phần mô tả kết quả.
  - P3 L7 §6 ⇒ dẫn protocol §12, §1/§2; dung sai là điều kiện N1/N4.
