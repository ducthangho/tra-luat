tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-BAM-LOG-NEN-WINDOWS r1 — mở phép đợi cây trước khi băm log (`run.json`) sang Windows bằng Job Object

- packet_id: LAUNCHER-BAM-LOG-NEN-WINDOWS; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #387 |
| `nguon_cap_viec` | Packet B của #387, tách từ `LAUNCHER-BAM-LOG-SAU-CAY-CHET` r1 (packet A, land `e4fdf09`, PR #1388; hồ sơ `ops/land/pr1388-wp387-*`, `landed: true`). Chủ kho 2026-11-19 (phiên điều phối #1206, AskUserQuestion) quyết **bỏ Darwin**, chỉ mở Windows; tên cũ `LAUNCHER-BAM-LOG-NEN-DARWIN-WINDOWS` bỏ. |
| `phu_thuoc` | Packet A đã land trên `master` (`e4fdf09` là tổ tiên của base). |
| `review_class` | `sensitive`: `.claude/dev/launcher.py` + `.claude/dev/launcher_test.py`, cùng lý do với A. Đối chiếu `lease_publish check` khi cấp lease. |
| `base` | `3b647461db7c8ded1bddd9aafc5c6aa5eead223f` lúc soạn; lease ghi OID thật lúc cấp (phải chứa `e4fdf09`). Đo lại §0 nếu base trôi. |

## 0. Hiện trạng (đo 2026-11-19 trên `3b64746`, Linux, Python 3.13.18; `launcher.py` sha256 `f2503d59927f…` 6213 dòng, `launcher_test.py` `37042727f8b8…` 18032 dòng)

`.claude/dev/launcher.py`:
- `VERSION = "1.6.1"` (dòng 102).
- `_thanh_vien_nhom(pgid)` (542): Linux quét `/proc`; Darwin hỏi `ps` với `timeout=15` (583); nền khác trả `None`. KHÔNG đổi ở packet này.
- `_nen_do_cay_truoc_bam()` (605) là chỗ DUY NHẤT quyết nền được đo cây: `return platform.system() == "Linux"`.
- `_cho_cay_chet_truoc_bam(pid, job, han)` (610): dòng 619 `if not _nen_do_cay_truoc_bam(): return False`; vòng dò dòng 625 `nhom = _thanh_vien_nhom(pid)`; deadline monotonic chung, kết quả sau hạn bị bỏ, ngủ `min(0.1, con_sau)`. Tham số `job` hiện không dùng ("để dành cho packet B").
- `_job_windows(pid)` (906): tạo Job Object với `KILL_ON_JOB_CLOSE` (`LimitFlags = 0x2000`, dòng 959), gán SAU `Popen`; chú thích tự khai khe "cháu sinh trước lúc gán nằm ngoài job". Trả handle hoặc `None`.
- `_pid_trong_job(job)` (977): `[]` = đã chứng minh rỗng · danh sách · `None` = không đọc được. Không ngủ.
- `_cay_da_chet(pid, job)` (1125): lồng vòng 20 × 0,1 s — KHÔNG được dùng trong vòng dò của hàm đợi (sẽ phá deadline chung).
- `lenh_run` (2677): `job = _job_windows(p.pid)` (2889); `ban_ghi["job_windows"] = job is not None` chỉ trên Windows (2893); handle job KHÔNG bao giờ đóng trong `lenh_run`. Khối đợi + mốc `ket_thuc` trước đợi (~2994–3001). Quyết xoá bản chụp prompt dòng 3041: `cay_da_chet = log_cay_chet if _nen_do_cay_truoc_bam() else (_thanh_vien_nhom(p.pid) == [])`. Dòng 3049 `if not _nen_do_cay_truoc_bam():   # #387: nền khác Linux giữ mốc ở vị trí cũ, sau phép đo xoá prompt` lấy lại `ket_thuc` sau phép đo xoá cho nền khác.
- Hệ quả trên Windows hôm nay: hàm đợi trả `False` ngay (`log_bam_cay_da_chet: false`, `log_bam_cho_giay` ≈ 0); `_thanh_vien_nhom` trả `None` nên bản chụp prompt KHÔNG BAO GIỜ bị xoá ngay (thiết kế cũ, `_cap_id` quét về sau — `t77`); đột biến `xoa_prompt_khi...`/neo `            and cay_da_chet):` mang điều kiện `("posix", …)` vì Windows giữ bản chụp.

`.claude/dev/launcher_test.py`:
- `San.__exit__` (177–184) `shutil.rmtree(self.d, ignore_errors=True)`.
- `_R387_CHI_LINUX` (14714); **9** ca trả nó trên nền khác Linux: (a) `r387_m1_chau_ghi_muon_khai_pham_vi_bam`, (a′) `r387_m1_doi_chung_ghi_som_lam_ve_bam_do`, (b) `r387_m1_con_thuong_chung_minh_cay_chet`, (c) `r387_m2_chau_ghi_trong_han_thi_bam_du`, (d) `r387_m2_khong_do_duoc_thi_khong_cho`, (i) `r387_a_nen_khac_giu_moc_ket_thuc_base`, (f) `r387_m1_stop_trong_luc_cho_khong_bi_de`, (g) `r387_m1_prompt_linux_xoa_khi_cay_chet`, (h) `r387_m2_ngat_trong_luc_doi_ghi_bi_ngat`. Khớp "9 ca r387 bỏ qua trên Windows" của hồ sơ land A (`launcher-windows` 44285378703: Windows 332/332). (e) `r387_m2_han_chung_cho_moi_lan_do` và (t) `r387_fixture_teardown_bao_loi_giu_loi_goc` chạy mọi nền; (e5) vòng `("Darwin","Windows","FreeBSD")` đòi `False` ngay, 0 lần ngủ.
- Fixture POSIX: `_r387_chay` vá `m._thanh_vien_nhom` để ghi mọi danh sách dò vào `m._r387_ds_do`, lưu `m._r387_pgid = so["pid"]`; `_r387_don_dep` chờ nhóm về `[]` bằng phép dò thật, không gửi tín hiệu; `_r387_don_khi_thoat` chạy teardown trước `rmtree`, giữ lỗi gốc bằng `add_note`; `_r387_nhat_ky_kill` bọc `os.kill`/`os.killpg` (Windows KHÔNG có `os.killpg` ⇒ hiện sẽ `AttributeError`).
- Bảng `DOT_BIEN`: 16 mục r387 (15072–15101), gồm 4 mục nền khác neo vào lời gọi `    if not _nen_do_cay_truoc_bam():\n        return False\n` (`r387_a_nen_khac_van_do`, `r387_a_nen_khac_ngu_thua` → ca (e)) và khối `_R387_KHOI_MOC` (chứa nguyên văn dòng 3049 kèm chú thích) (`r387_a_nen_khac_doi_moc`, `r387_a_nen_khac_moc_truoc_unlink` → ca (i)). `DOT_BIEN_HARNESS` (17290) có 2 mục r387. Neo `nhom_luon_rong` (16445) giữ nguyên (không đổi chữ ký `_thanh_vien_nhom`).
- CI: `.github/workflows/` chỉ có runner `ubuntu-latest`/`windows-latest`; kho cấm dùng CI Windows cho packet (ràng buộc chủ kho) ⇒ Windows đo NATIVE trên máy chủ kho.

## 1. `write_set`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- **Darwin và mọi nền khác Linux/Windows**: giữ NGUYÊN hành vi A (hàm đợi trả `False` ngay; xoá prompt theo biểu thức cũ; mốc `ket_thuc` sau phép đo xoá). Nợ có tên **`wp387-darwin-chua-do`**: không có máy macOS, CI không có runner macOS (quyết định chủ kho 2026-11-19). Không đổi `_thanh_vien_nhom` (kể cả `timeout=15` của `ps`).
- Linux: không đổi bất kỳ hành vi nào của A.
- Không đóng khe gán job sau `Popen`, không theo dõi breakaway: giới hạn khai ở docstring.
- Không đổi `_cay_da_chet`, `_job_windows`, `_pid_trong_job`, nhánh chụp workspace, `San`.
- Windows vẫn KHÔNG xoá ngay bản chụp prompt (kể cả khi job đã chứng minh rỗng): giữ thiết kế `t71`/`t77`.
- Không dùng CI Windows (nhãn `windows`, `workflow_dispatch`).

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `_nen_do_cay_truoc_bam()` trả `platform.system() in ("Linux", "Windows")`; docstring "Packet A: chỉ Linux" → "Packet B: Linux và Windows; Darwin/nền khác chưa đo (nợ `wp387-darwin-chua-do`)". | `launcher.py` |
| M2 | `_cho_cay_chet_truoc_bam`: thay ĐÚNG dòng dò 625 bằng phép dò theo nền, mỗi vòng dò đúng MỘT lần: Linux `_thanh_vien_nhom(pid)`; Windows `_pid_trong_job(job) if job is not None else None`. Dòng mới, viết NGUYÊN VĂN trên MỘT dòng (thụt 8 dấu cách) để mọi đột biến §4b neo trọn dòng — các mảnh `_pid_trong_job(job) if job is not None else None` (dòng 1131, `_cay_da_chet`) và `if platform.system() == "Linux" else` (dòng 2499) đã có ở chỗ khác nên KHÔNG được làm mẫu riêng: `nhom = _thanh_vien_nhom(pid) if platform.system() == "Linux" else (_pid_trong_job(job) if job is not None else None)  # #387 B: dò theo nền`. Mọi phần còn lại của hàm (deadline, bỏ kết quả sau hạn, `None` ⇒ `False` ngay, cách ngủ) giữ nguyên từng byte. KHÔNG gọi `_cay_da_chet`. Docstring sửa: `True` = phép dò trả rỗng trong nhóm tiến trình POSIX (Linux) hoặc trong Job Object được theo dõi (Windows); tiến trình rời nhóm (`setsid`), breakaway khỏi job, hoặc sinh trong khe giữa `Popen` và lúc gán job nằm ngoài phạm vi; Windows không có job (`job is None`) ⇒ không đo được ⇒ `False` ngay. `QueryInformationJobObject` đồng bộ, không ngủ. Bỏ câu "`job` để dành cho packet B". | `launcher.py` |
| M3 | Dòng 3041 thành `cay_da_chet = (log_cay_chet and platform.system() != "Windows") if _nen_do_cay_truoc_bam() else (_thanh_vien_nhom(p.pid) == [])`: Linux như A; Windows dùng kết quả đợi cho `run.json` nhưng KHÔNG xoá bản chụp; nền khác như cũ. Dòng `            and cay_da_chet):` giữ nguyên từng byte. Chú thích dòng 3049 đổi "nền khác Linux" → "nền khác Linux/Windows" (và hằng `_R387_KHOI_MOC` ở test đổi theo, M7). | `launcher.py` |
| M4 | `VERSION = "1.6.1"` → `"1.6.2"`. | `launcher.py` |
| M5 | **Fixture mở sang Windows** (POSIX giữ nguyên hành vi A): (i) **bắt tay gán job cho MỌI con** — mã con mà fixture sinh luôn có phần mở đầu chờ tệp `<san>/job-da-gan` tối đa 10 s, không thấy thì `sys.exit(3)`. `_r387_chay` bọc `m._job_windows`: gọi bản THẬT; nếu trả handle thì lưu `m._r387_job = handle` rồi ghi `job-da-gan`; trên POSIX `_r387_chay` ghi sẵn tệp trước khi chạy. Sau `lenh_run`: đòi `so["ma_thoat"] != 3` (ca (d)/(h) ngoại lệ ghi rõ); trên Windows đòi thêm `so.get("job_windows") is True` và `m._r387_job` khác `None`. (ii) Ghi danh sách trả của CẢ `m._thanh_vien_nhom` lẫn `m._pid_trong_job` vào `m._r387_ds_do`; tham số `do=` thay phép dò của nền hiện tại (Linux: `_thanh_vien_nhom`, nhận pid; Windows: `_pid_trong_job`, nhận handle job) và nhận đúng đối số của phép dò nó thay; `m._r387_do_that` trỏ bản THẬT của phép dò nền hiện tại (lưu trước khi vá). Tham số MỚI `do_nhom=` thay `m._thanh_vien_nhom` trên MỌI nền (dùng cho phép đo xoá prompt theo biểu thức base ở ca (i)). (iii) Teardown: `_r387_don_dep` trên Windows chờ phép dò THẬT (`m._r387_do_that(m._r387_job)`, không phải bản ca đã vá) về `[]` (cùng ba trạng thái `True/False/None` của `_r387_cho_cay_rong`); CHỈ SAU khi chờ xong (rỗng hoặc hết hạn) mới đóng handle ĐÚNG MỘT lần qua hàm `m._r387_dong_job` (mặc định `ctypes.windll.kernel32.CloseHandle`), ĐÒI giá trị trả khác 0 — bằng 0 ⇒ thông điệp lỗi teardown `"r387 teardown: CloseHandle that bai"`; xoá tham chiếu `m._r387_job = None` ngay sau lời gọi. Hết hạn mà job còn thành viên ⇒ thông điệp lỗi (ca ĐỎ, giữ lỗi gốc như A), không im lặng. Vì teardown chạy trước `San.__exit__`, `rmtree(ignore_errors=True)` chỉ chạy sau khi job đã chứng minh rỗng; job không rỗng thì ca đã ĐỎ trước đó — thư mục sót không bị nuốt im lặng (đóng P2 cũ mà không sửa `San`). (iv) `_r387_nhat_ky_kill` chỉ bọc `os.killpg` khi `hasattr(os, "killpg")`. | `launcher_test.py` |
| M6 | **Mở 9 ca** sang Windows: gỡ `_R387_CHI_LINUX` và cả 9 nhánh trả nó. Chỉ thay đổi sau: (a), (c): vế "PID cháu có trong phép dò" đọc từ `m._r387_ds_do` (Windows = danh sách `_pid_trong_job` của đúng job đã gán). (d), (f): `do=` thay phép dò của nền hiện tại. (g): giữ ID; Linux như A; Windows: `log_bam_cay_da_chet is True`, tệp bản chụp CÒN, không có khoá `prompt_ban_chup_da_xoa`. (i): mô phỏng nền khác bằng vá `_nen_do_cay_truoc_bam` → `False` như A, chạy được trên cả Linux lẫn Windows; phép dò giả ngủ 0,5 s rồi trả `[]` truyền qua `do_nhom=` (không qua `do=`: trên Windows `do=` thay `_pid_trong_job`, còn biểu thức base gọi `_thanh_vien_nhom`, vốn trả `None` trên Windows ⇒ không xoá ⇒ ca ĐỎ oan). (h): không đổi logic. **(e)**: (e5) vòng đổi thành `("Darwin", "FreeBSD")`, gọi với `job=object()` (không phải `None` — với `None` thì đột biến `r387_a_nen_khac_van_do` đi nhánh job, nhận `None`, trả `False` ngay và SỐNG): `False` ngay, 0 lần ngủ, `_thanh_vien_nhom` và `_pid_trong_job` đều bị vá thành hàm làm ca ĐỎ nếu bị gọi; thêm (e6) Windows, `job=object()`, `_pid_trong_job` luôn `[7]`, `_cay_da_chet` và `_thanh_vien_nhom` vá thành hàm làm ca ĐỎ ⇒ `False` trong ≤ 1,0 s; (e7) Windows, `job=None` ⇒ `False`, 0 lần ngủ, không lời gọi dò nào; (e8) Windows, `job=object()`, `_pid_trong_job` trả `[7]` lần đầu rồi `[]` ⇒ `True`; (e9) Linux với `_pid_trong_job` vá thành hàm làm ca ĐỎ, `_thanh_vien_nhom` trả `[]` ⇒ `True`. (t): thêm vế CloseHandle — `m._r387_job = object()`, phép dò job trả `[]`, `m._r387_dong_job = lambda h: 0`, nền vá thành Windows ⇒ teardown trả thông điệp chứa `"CloseHandle that bai"`; vế đối chứng `lambda h: 1` ⇒ `None` và `m._r387_job is None` sau đó. | `launcher_test.py` |
| M7 | Đột biến (mỗi mẫu nguyên văn khớp ĐÚNG một chỗ, `t117` giữ ĐẠT): cập nhật `_R387_KHOI_MOC` theo chú thích mới (M3); bốn mục `r387_a_nen_khac_*` GIỮ NGUYÊN tên, mẫu, ca đích (neo vào lời gọi, không vào thân `_nen_do_cay_truoc_bam`) — chúng nay đo đường "nền khác Linux/Windows" qua (e5)/(i). Thêm vào `DOT_BIEN` theo §4b (W1–W7) và vào `DOT_BIEN_HARNESS` (H1–H3). | `launcher_test.py` |

## 4. `nghiem_thu`

Mọi số công bố kèm thời điểm UTC tới giây, phiên bản công cụ, lệnh nguyên văn, mã thoát.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux (head): 9 ca mở + (e), (t) ĐẠT; mọi ca r387 của A giữ kết quả. | Đột biến W2, W3, W4, W6, W7 và H1, H3 qua runner `--dot-bien` ⇒ mỗi mục `OK giet 1/1` đúng ca đích (§4b). |
| N2 | `t117` ĐẠT trên head (mọi mẫu khớp đúng một chỗ, kể cả `_R387_KHOI_MOC` mới). | Không cập nhật `_R387_KHOI_MOC` ⇒ `t117` ĐỎ. |
| N3 | `launcher_test.py` trên head (Linux, CI gate + tại chỗ): N/N, hai số bằng nhau; tập bỏ qua của head ⊆ tập bỏ qua của base (không thêm bỏ qua mới). `--dot-bien`: rc 0, `DOT BIEN: N/N dat`; mục `KHONG DO DUOC tren nen nay` = các mục `windows` của base cộng W5, H2. | Tập bỏ qua head có ID không có ở base; dòng cuối `--dot-bien` hai số khác nhau. |
| N4 | **Windows NATIVE** trên Desktop `DESKTOP-T9R33P2` (VM `tra-luat-win` dự phòng), exact head (`git rev-parse HEAD` = head; cây sạch), ghi `python --version`, `platform.platform()`, giờ UTC: (L1) 9 ca mở + (e) + (t) + `t71` + `t77`: mỗi ca `1/1 qua, 0 bo qua, 0 hong` qua `python .claude/dev/launcher_test.py --lap-ca <ca> --lan 1`; **log toàn suite Windows** (`python .claude/dev/launcher_test.py`) KHÔNG còn dòng nào chứa `BO QUA r387` (đóng P3 cũ: đếm trên log Windows, không trên log Linux) và số ca bỏ qua giảm đúng 9 so với base trên cùng máy (đo base `3b64746` cùng lượt). (L2) Đột biến Windows (§4b cột "nền đo" = Windows): W5, H2 bắt buộc giết đúng ca đích; W1–W4, W6, W7, H1, H3 đo lại trên Windows (kỳ vọng giết như Linux). Dùng runner `--dot-bien` trên bản sao đủ cây của exact head (`git archive`), `DOT_BIEN`/`DOT_BIEN_HARNESS` lọc còn các mục r387 bằng `ast.literal_eval`; ghi sha256 tệp đã lọc. (L3) Lặp (a), (c) mỗi ca 5 lần trên Windows: 5/5. | Ca L1 `bo qua`/`hong`; log còn `BO QUA r387`; số bỏ qua không giảm đúng 9; mục L2 sống hoặc chết sai ca; các tình huống sau làm ca ĐỎ bằng `TinHieuChotCa` chứ không thành bỏ qua: thiếu job (`job_windows` không `True`), con thoát mã 3, PID cháu không có trong `_pid_trong_job(job)`, thiếu dấu `chau-xong`, teardown báo lỗi. HEAD khác exact head ⇒ N4 vô hiệu. Chưa có log native ⇒ `chưa đo được`. |
| N5 | `run.json` của một lượt `run` thật trên Windows native (lệnh `python .claude/dev/launcher.py run …` với con `python -c "print(1)"`): `"version": "1.6.2"`, `log_bam_cay_da_chet: true`, `job_windows: true`, `log_bam_cho_giay` < 10. | Thiếu một khoá hoặc giá trị khác. |
| N6 | `git diff --numstat base..H` đúng 2 tệp write set, tổng thêm ≤ 450; Ruff 0.15.15 `--select F` tập diagnostic head = base trên 2 tệp; `doctrine-scan`, `adr-song` rc 0; `git diff --check` sạch; `eol_policy --all` ok. | Đường dẫn thứ ba ⇒ ĐỎ; diagnostic mới ⇒ ĐỎ. (`doctrine-scan`/`adr-song`: không có phản chứng riêng ở packet này — khai thẳng.) |

### 4b. Bảng đường vào và đột biến (liệt kê HẾT đường trước; mỗi đường một chốt, một đột biến, một dấu hiệu đỏ riêng)

| # | đường vào / chốt | đột biến (tìm → thay, khớp đúng một chỗ) | ca đích & dấu hiệu | nền đo |
|---|---|---|---|---|
| W1 | Windows thuộc tập nền được đo (M1) | `return platform.system() in ("Linux", "Windows")` → `return platform.system() in ("Linux",)` | (e8): `False` thay vì `True` ("r387(e8)…") | Linux + Windows |
| W2 | Windows dò bằng job, không bằng nhóm POSIX (M2) | trọn dòng M2 → `nhom = _thanh_vien_nhom(pid)  # #387 B: dò theo nền` | (e6): hàm vá `_thanh_vien_nhom` làm ca ĐỎ ("r387(e6) goi _thanh_vien_nhom tren Windows") | Linux + Windows |
| W3 | Windows thiếu job ⇒ không đo được (M2) | trọn dòng M2 → cùng dòng với `else None)` cuối đổi thành `else [])` | (e7): `True` thay vì `False` ("r387(e7)…") | Linux + Windows |
| W4 | Windows không dùng `_cay_da_chet` (giữ deadline chung) | trọn dòng M2 → cùng dòng với `_pid_trong_job(job)` đổi thành `([] if _cay_da_chet(pid, job) else [7])` | (e6): `_cay_da_chet` vá làm ca ĐỎ ("r387(e6) goi _cay_da_chet") | Linux + Windows |
| W5 | Windows KHÔNG xoá bản chụp kể cả khi job rỗng (M3) | `(log_cay_chet and platform.system() != "Windows")` → `log_cay_chet` | (g) vế Windows: bản chụp mất ("r387(g) Windows xoa ban chup") — điều kiện nền `("windows", "POSIX van xoa khi cay chet; chi Windows giu ban chup")` | chỉ Windows |
| W6 | Linux vẫn dò nhóm, không đi nhánh job (M2) | trọn dòng M2 → cùng dòng với `"Linux"` đổi thành `"LinuxX"` | (e9): hàm vá `_pid_trong_job` làm ca ĐỎ ("r387(e9)…") | Linux + Windows |
| W7 | Mốc `ket_thuc` Windows lấy TRƯỚC khi đợi (hệ quả M1) | không cần đột biến mới: `r387_ket_thuc_sau_vong_cho` (A) chạy trên Windows với ca đích (a) | (a) vế lệch mốc ("r387(a) log_bam_luc_utc - ket_thuc_utc…") | Windows (đo lại mục A) |
| W8 | Darwin/nền khác giữ `False` ngay | giữ `r387_a_nen_khac_van_do`, `r387_a_nen_khac_ngu_thua` (A) | (e5) Darwin/FreeBSD | Linux + Windows |
| W9 | Nền khác giữ mốc `ket_thuc` cũ | giữ `r387_a_nen_khac_doi_moc`, `r387_a_nen_khac_moc_truoc_unlink` (A; neo `_R387_KHOI_MOC` mới) | (i) | Linux + Windows |
| H1 | Fixture chờ job rỗng TRƯỚC khi đóng handle (M5 iii) | trong `_r387_don_dep` nhánh Windows: dời lời gọi `m._r387_dong_job(...)` lên TRƯỚC vòng chờ (mẫu nguyên văn khi viết) | (t) vế CloseHandle đối chứng: thứ tự ghi nhận sai ("r387(t) dong handle truoc khi cho") — (t) ghi thứ tự lời gọi dò/đóng | Linux + Windows |
| H2 | Bắt tay `job-da-gan` giữ con tới lúc gán (M5 i) | bọc `m._job_windows` ghi `job-da-gan` TRƯỚC khi gọi bản thật | (c) Windows: PID cháu không có trong `_pid_trong_job(job)` hoặc `job_windows` khác `True` — khe gán thật trên máy | chỉ Windows |
| H3 | CloseHandle trả 0 ⇒ lỗi teardown (M5 iii) | `if m._r387_dong_job(h) == 0:` → `if False:` (mẫu nguyên văn khi viết) | (t) vế `lambda h: 0` không ra thông điệp ("r387(t) CloseHandle that bai khong bao") | Linux + Windows |

Mẫu (tìm, thay) của H1/H3 chốt nguyên văn khi executor viết mã, mỗi mẫu khớp đúng một chỗ (`t117`). Mọi đột biến: phân hạng bằng `TinHieuChotCa`, chỉ tính GIẾT khi ca đích đỏ đúng nhãn, ca đích ĐẠT trên bản sạch.

## 5. `pham_vi_e`

Không chạm E4, không chạm E5.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước `ADR-0053` (450 dòng thêm). Executor đo `git diff --numstat base..H` (không lọc đường dẫn) trước khi công bố; > 450 ⇒ DỪNG, không push, báo điều phối; không cắt ca/phép đo để lọt trần.
- Chưa có log native Windows (N4, N5) ⇒ không công bố `landed`/`ready`.
- Cần sửa ngoài write set (kể cả `San`) ⇒ dừng, đi revision đặc tả.
- Phát hiện Windows cần ngủ/chờ khác trong hàm đợi (vd. danh sách job cập nhật trễ quá 10 s) ⇒ dừng, đi revision; không tự nới hạn.
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm (`ADR-0067`) — **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung` — phần nền của một packet tách (#387 A → B), không phải packet khắc phục bản vá cũ.

## 8. `chua_do_duoc`

- Toàn bộ hành vi Windows native: bắt tay `job-da-gan` có giữ con tới lúc gán; cháu `Popen(stdout=sys.stdout)` có trong job và giữ handle `stdout.log`; job cập nhật danh sách trễ; teardown + `CloseHandle`. N4/N5 là phép đo duy nhất.
- Darwin: không đo (ngoài phạm vi, nợ `wp387-darwin-chua-do`).
- Giới hạn có tên: cháu breakaway hoặc sinh trong khe giữa `Popen` và gán job ⇒ `true` có thể sai.
- Dung sai thời gian (e6) ≤ 1,0 s chỉ đo trên Linux; Windows chậm hơn có thể cần nới — nới thì ghi số đo và đi revision.
- Kích thước ước lượng (đếm theo khối tương tự trên base): `launcher.py` ~ +8/−6 (M1 1 dòng, M2 3 dòng + docstring ~4, M3 1, M4 1); `launcher_test.py` ~ +110–170 (fixture Windows ~35–50, gỡ 9 nhánh −18, (e6)–(e9) ~25–35, (g) Windows ~8, (t) vế CloseHandle ~12–18, bảng đột biến ~12–16). Tổng ~120–180 ≤ 450. Đo lại bằng numstat.

## 9. Quyết định đã ghi

- **Q-D (2026-11-19, chủ kho, AskUserQuestion, phiên #1206):** bỏ Darwin khỏi B, chỉ mở Windows; Darwin giữ hành vi A, nợ có tên `wp387-darwin-chua-do`.
- **Q-W (cùng quyết định):** đổi tên packet thành `LAUNCHER-BAM-LOG-NEN-WINDOWS` r1; 4 đột biến `r387_a_nen_khac_*` giữ (neo vào lời gọi nên vẫn đo đường "không phải Linux/Windows" qua (e5) Darwin/FreeBSD và (i)).
- **Finding mở từ review lượt 6 của A, đóng ở bản này:** P2 teardown Windows — M5(iii) kiểm giá trị trả `CloseHandle`, chờ job rỗng trước khi đóng, teardown chạy trước `rmtree` nên thư mục sót không bị nuốt im lặng (H1, H3, (t)); P3 đếm `BO QUA` — chuyển sang log Windows native (N4 L1). Bốn đột biến `r387_a_nen_khac_*`: xử lý ở M7/W8/W9.

## 10. Nhật ký

- 2026-11-18: bản Darwin+Windows dựng trên vá thử `trA` (lưu `rv387b/dac-ta-ban0.md`).
- 2026-11-19: đo lại trên base thật `3b64746` (lưu `rv387b/dac-ta-ban0b-darwin-c1cbe870.md`); chủ kho bỏ Darwin; viết lại toàn bộ thành bản này.

## 11. Nhật ký review

(chưa có lượt nào)
