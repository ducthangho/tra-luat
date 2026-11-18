tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-BAM-LOG-SAU-CAY-CHET r1 — `run.json` khai phạm vi của băm log: cây tiến trình đã chết hay chưa lúc băm (Linux)

- packet_id: LAUNCHER-BAM-LOG-SAU-CAY-CHET; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #387 |
| `nguon_cap_viec` | Nợ P2 `m1-bam-sau-khi-con-thoat` của Issue #387 (verdict cross-review `claude` trên PR #381 @ `3151371d42557448750ca8b82e5597823c898881`; Issue trỏ `.claude/dev/launcher.py:1690` ở thời điểm ấy, nay là vòng băm ở dòng 3016–3028). Chủ kho duyệt hướng M1–M3 ngày 18-11-2026 (phiên điều phối). Sau năm lượt review Codex (`request_changes` cả năm, lịch sử ở §9), đặc tả gốc được TÁCH theo cùng cách chủ kho đã chọn cho #433 (tách, không nâng trần). Packet NÀY (A) làm phần Linux. Nhánh Darwin và Windows cùng ca đo của chúng thuộc packet B `LAUNCHER-BAM-LOG-NEN-DARWIN-WINDOWS` (`ops/specs/LAUNCHER-BAM-LOG-NEN-DARWIN-WINDOWS-r1.md`), packet ấy phụ thuộc A đã land. Bảy nợ còn lại của #387 không thuộc packet này (§2). |
| `review_class` | `sensitive`: `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py` nhận lớp mặc định fail-closed từ `_tinh_lop_tu_write_set` (cùng lý do với #1313). Đối chiếu lại bằng `lease_publish check` khi cấp lease. |
| `base` | `641108cb997872b0ef2a277ea9c8faf8b82532bb` (`origin/master` lúc soạn, đo 2026-11-18T04:59:49Z); lease ghi OID base thật lúc cấp. |

## 0. Hiện trạng (số dòng là của `641108c`; mỗi số kèm thời điểm đo, nền Linux, Python 3.13.18)

Đợt LỊCH SỬ (người soạn bản đầu, 04:49–04:59Z) và các đợt đo lại trên bản sao `git archive 641108c` có vá thử
(05:15Z–09:07Z). Vá thử chỉ để soạn đặc tả, không phải bản thi hành.

- `.claude/dev/launcher.py`, `VERSION = "1.6.0"` (dòng 102). `lenh_run` (dòng 2643) mở `stdout.log` (dòng 2774) và cho
  con ghi THẲNG vào tệp (dòng 2825–2826). Sau `p.wait()` (dòng 2877, hoặc 2881 khi có hạn chót), nhánh chụp workspace
  (dòng 2913–2940) và chuẩn hoá mã thoát (dòng 2942–2951), thứ tự hiện nay là:
  - dòng 2954–2966: đọc lại sổ (`so_moi = _doc_so(thu_muc)` ở dòng 2957); `stop` đã ghi `da_dung` thì giữ, không thì
    quyết `xong`/`qua_han`/`bi_ngat`. Chú thích tại đó: stop ghi `da_dung` rồi runner ghi đè là lỗi đã đo (t50).
  - dòng 2967–2971: `ngat_khi_chup` đổi `xong` thành `bi_ngat`, mã 130; `ma_thoat` vẫn là mã THẬT. Dòng 2972–2978:
    áp `kq_chup`.
  - dòng 2991: `cay_da_chet = (_thanh_vien_nhom(p.pid) == [])`, đo MỘT lần, không chờ, chỉ điều khiển xoá bản chụp
    prompt (dòng 2992–2998). Trên Windows `_thanh_vien_nhom` luôn `None` nên không bao giờ xoá ngay.
  - dòng 2999 `ket_thuc = _bay_gio()`, dòng 3013 `thoi_luong_giay`, vòng băm 3016–3028, `_ghi_so` 3029.
  `run.json` không có trường nào nói băm được lấy lúc nào hay lúc ấy còn hậu duệ ghi được không.
- `_thanh_vien_nhom(pgid)` (dòng 542): Linux quét `/proc`; Darwin gọi `ps` với `timeout=15` cứng (dòng 583); nền
  khác `None`.
- `lenh_stop` (dòng 3075) ghi `da_dung` + `ly_do_dung` ở dòng 3103–3106. Một vòng đợi đặt SAU dòng 2957 sẽ mở đúng cửa
  sổ mà chú thích ở đó cấm (review lượt 1).
- Người đọc sổ (review lượt 1 quét `git grep`): `launcher.py status` in `thoi_luong_giay`; K4 ở
  `.claude/dev/packet_loop.py:3552` so `stdout_sha256`; `docs/GOI_AGENT_DA_NEN.md:352–365` hướng dẫn đặt ngưỡng theo
  `thoi_luong_giay`; script dưới `ops/` đọc hiệu hai mốc. Không có schema hay bộ khoá cố định cho `run.json`. ⇒ giữ
  ngữ nghĩa `ket_thuc_utc` và `thoi_luong_giay` (M2).
- Tái hiện lỗi trên base: lịch sử 04:49:33Z (rc 0, `xong`, sổ 4 byte `43a9565a…`, đĩa sau 18 byte `edb02178…`).
  Reviewer lượt 1 đo lại độc lập trong tiến trình ("khoảng 05:11 UTC", không có mốc chính xác): sổ 4 byte
  `e2852c4f…`, đĩa 18 byte `907a8b9d…`.
- Bảng `DOT_BIEN` (từ dòng 14713) có 550 mục ở base: 538 không điều kiện nền, 7 `posix`, 5 `windows` (đếm bằng
  `ast.literal_eval`, 2026-11-18T05:34:50Z). `t117` đòi mỗi mẫu khớp đúng một chỗ; ngoại lệ duy nhất đã biết là
  `DA_BIET_TRUNG = {"hook_phien_bo_phep_so_nang_luc": 2}` (dòng 4150). Neo chạm vùng này:
  - `xoa_prompt_khi_wrapper_vua_thoat` (dòng 16109) neo nguyên dòng 2991, ca đích `t76` (`t76` tự bỏ qua trên Windows,
    dòng 1759–1760).
  - `ban_chup_de_lai_tren_dia` (dòng 16105, `posix`) neo `            and cay_da_chet):`, ca đích `t71`.
  - `r1252_windows_khong_dung_job` (14885) neo `                return ds == []`; `r1252_windows_bo_ngu` (14887) neo
    `            time.sleep(0.1)`; `r1252_none_la_chet` (14883) neo `        return _thanh_vien_nhom(pid) == []`.
  - `nhom_luon_rong` (16057–16059) neo chữ ký `_thanh_vien_nhom`. Packet A KHÔNG đổi chữ ký, nên neo này giữ nguyên.
- **Vá thử của packet A, bản sau lượt 7** (`trA` trong scratchpad, `diff` so base):
  - Kích thước: **`launcher.py` +46/−3, `launcher_test.py` +364/−2, tổng 410 dòng thêm**.
  - Nội dung: mười một ca, mười sáu đột biến `DOT_BIEN` mới, hai đột biến `DOT_BIEN_HARNESS` mới, một neo sửa.
  - Từng ca `python3 -B .claude/dev/launcher_test.py --lap-ca <ca> --lan 1`, 2026-11-18T08:55:54Z → 08:56:16Z: mười một
    ca r387 cùng `t117`, `t76`, `t71` đều `1/1 qua`.
  - **Đối chứng base (N1)**, 09:07:43Z: `launcher_test.py` của vá thử đặt cạnh `launcher.py` của base (`VERSION =
    "1.6.0"`), lệnh `--lap-ca r387_m1_chau_ghi_muon_khai_pham_vi_bam --lan 1` ⇒ `0/1 qua`, dòng
    `HONG … TinHieuChotCa: r387(a) cay chua chet ma khai None`. Ca đi QUA vế băm (sổ ≠ đĩa sau khi cháu ghi muộn,
    tức lỗi #387 tái hiện trên base) rồi đỏ ở vế khoá; không có `AttributeError`/`KeyError` của fixture. (Lần đo
    trước, 08:16:40Z, cùng kết quả.)
  - Runner đột biến trên bản sao ĐỦ cây (`git archive 641108c` + hai tệp vá), `DOT_BIEN` lọc còn các mục r387 và neo
    sửa, `DOT_BIEN_HOOK`/`DOT_BIEN_HARNESS` để nguyên; lệnh `python3 -B .claude/dev/launcher_test.py --dot-bien`,
    08:56:16Z → 09:00:54Z, **rc 0**, dòng cuối `DOT BIEN: 178/178 dat`, 0 dòng `SAI`. Cả 16 mục r387 `DOT_BIEN` (kể cả
    `r387_a_nen_khac_moc_truoc_unlink` mới) và 2 mục harness `OK giet 1/1` đúng ca đích; `xoa_prompt_khi_wrapper_vua_thoat`
    `giet 1/1 t76`; `nhom_luon_rong` (không đổi) `giet 1/1 t67`.
  - Toàn bộ `launcher_test.py` (09:00:58Z → 09:07:37Z, rc 0): `424/424 ca DA CHAY QUA (tong 426, bo qua 2, hong 0)`,
    real 398,7 s. Hai ca bỏ qua đúng bằng base: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`,
    `r484_g4_windows_sid_alias_identity`. Base lịch sử 04:51–04:58Z: `413/413 (tong 415, bo qua 2, hong 0)`, 386 s.
  - `ruff check --no-cache --select F` (ruff 0.17.5, 08:56Z, rc 1): đúng 5 F841 của base ở `launcher_test.py`
    (base dòng 2767, 3695, 3937, 4421, 6465); `launcher.py` 0. Delta 0.
  - Các bản trước (lượt 6: 400 dòng, 08:16–08:27Z, `177/177 dat`, suite `424/424`; lúc tách: 364 dòng) chỉ còn giá
    trị lịch sử.
- Năm lỗi của chính các bản vá thử trước, chỉ lộ ra khi chạy; mẫu ở M6 là bản đã sửa:
  - Đột biến stop-race chỉ đổi chỗ dòng gán khoá thì SỐNG.
  - Ca ngắt vá phép dò của nền thì cú ngắt rơi vào nhánh chụp workspace (dòng 2916); phải vá đúng hàm đợi.
  - Đột biến `pass` ở nhánh sau hạn làm `time.sleep` nhận số âm, thành tín dụng giả.
  - Bộ ghi kill chuyển tiếp tín hiệu thật thì chính đột biến harness có thể giết nhầm.
  - Dọn cháu theo PID có khe tái cấp PID (hai lượt cùng hình dạng), nên đã BỎ đường gửi tín hiệu.
- **Mục `DOT_BIEN` kế thừa không đo được trên Linux** (cho N4), rà toàn bảng base `641108c`:
  - Cách rà: tập ca tự bỏ qua trên Linux ở base đúng là hai ca `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` và
    `r484_g4_windows_sid_alias_identity` (suite base 04:51–04:58Z và mọi lượt suite sau). Đọc `DOT_BIEN` (550 mục) và
    `DOT_BIEN_HARNESS` bằng `ast.literal_eval`, lọc mục có ca đích thuộc hai ca ấy. `DOT_BIEN_HOOK` không parse được
    bằng `literal_eval`, nên rà bằng `grep` tên hai ca trong vùng bảng (từ dòng 16600): 0 kết quả.
  - Kết quả: ba mục. `g4_windows_sid_alias_not_normalized` và `g4_windows_LA_not_current_owner` (điều kiện `windows`,
    thuộc năm mục `windows`, ca đích `r484_g4…`). `124_khi_chau_con_song` (điều kiện `posix`, ca đích `t62`): mục DUY
    NHẤT qua được bộ lọc nền mà ca đích tự bỏ qua trên Linux.
  - Đo trên base, 2026-11-18T09:12:03Z → 09:15:52Z: bản sao đủ cây `git archive 641108c`, `DOT_BIEN` lọc còn ba mục ấy
    cùng `xoa_prompt_khi_wrapper_vua_thoat` làm đối chứng (sha256 tệp test đã lọc `7ea1dfd8…`). Lệnh
    `python3 -B .claude/dev/launcher_test.py --dot-bien`, rc 0, dòng cuối
    `DOT BIEN: 159/159 dat  (3 khong do duoc tren nen nay)`. `124_khi_chau_con_song` ra `KHONG DO DUOC tren nen nay (ca
    dich bo qua: t62_…)`; hai mục `g4_windows_*` ra `KHONG DO DUOC tren nen nay (native SID conversion)`; đối chứng
    `OK giet 1/1 t76`.
- `lease_publish.py ai-dang-giu` (lịch sử 04:52:38Z, sau `git fetch origin`; `ls-remote --heads` 306, cục bộ 307,
  `comm -23` rỗng): `NGƯỜI_GIỮ 0` cho cả hai tệp. Lease đo lại lúc cấp.

## 1. `write_set`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- **Darwin và Windows không đổi hành vi băm** (thuộc packet B), ngoài việc sổ có ba khoá mới với giá trị an toàn. Hàm
  đợi trả `false` ngay, không dò, nên trên các nền ấy `log_bam_cay_da_chet` luôn `false` (chưa chứng minh). Quyết định
  xoá bản chụp prompt trên các nền ấy giữ NGUYÊN biểu thức base `_thanh_vien_nhom(p.pid) == []`: Darwin đo một lần
  như cũ, Windows không bao giờ xoá ngay như cũ. Mốc `ket_thuc` (nên cả `ket_thuc_utc` và `thoi_luong_giay`) trên các
  nền ấy lấy ĐÚNG vị trí base: sau phép đo xoá prompt. Không đổi chữ ký hay `timeout` của `_thanh_vien_nhom`.
- Không đổi `stdout_byte`/`stdout_sha256`/`stderr_byte`/`stderr_sha256`. Không đổi ngữ nghĩa `ket_thuc_utc` và
  `thoi_luong_giay`. Không giết cây trước khi băm. Không đổi `trang_thai`/`ma_thoat` theo khoá mới; ngoại lệ duy nhất
  là Ctrl-C trong vòng đợi (M2).
- Không sửa người đọc nào ngoài launcher (K4, `PROTOCOL_DA_PHIEN.md:771`, `ADR-0065`, `GOI_AGENT_DA_NEN.md`). Không thêm
  thẻ vào dòng `# launcher-nang-luc:` (dòng 118). Không đổi `_cay_da_chet` và nhánh chụp workspace.
- Vế `cross_approved` ↔ `executor_provider` của #387 và sáu nợ còn lại (`oracle-lech-voi-jsonschema`,
  `m2-danh-tinh-tu-basename`, `transport-sha-vong-tron`, `raise-mot-provider-hai-transport-chet`,
  `r13-la-bi-danh-cua-t70`, `format-uri-khong-duoc-khang-dinh`) không thuộc packet này.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `lenh_run` ghi ba khoá mới vào `run.json`. `log_bam_cay_da_chet` (bool) lấy từ MỘT lời gọi đợi của M2. Nghĩa của `true`, viết vào docstring: "phép dò trả danh sách rỗng trong nhóm tiến trình POSIX; tiến trình rời nhóm (`setsid`) nằm ngoài phạm vi". `false` = chưa chứng minh được, gồm: còn thành viên khi hết hạn, lần dò trả về sau hạn, không đo được, bị ngắt, nền không phải Linux. `log_bam_cho_giay` (3 chữ số thập phân) = thời gian lời gọi đợi đo bằng `time.monotonic()`. `log_bam_luc_utc` (ISO UTC, `_bay_gio()`) gán NGAY TRƯỚC vòng băm. Hàm `_nen_do_cay_truoc_bam() -> bool` (= `platform.system() == "Linux"`) là CHỖ DUY NHẤT quyết nền nào được đo; hàm đợi, quyết định xoá prompt và mốc kết thúc đều hỏi nó, và ca test vá nó để giả lập nền khác. Dòng 2991 thành `cay_da_chet = log_cay_chet if _nen_do_cay_truoc_bam() else (_thanh_vien_nhom(p.pid) == [])`: Linux dùng kết quả đợi, nền khác giữ biểu thức base. Dòng `            and cay_da_chet):` giữ nguyên từng byte. | `.claude/dev/launcher.py` |
| M2 | Hàm mới `_cho_cay_chet_truoc_bam(pid, job, han) -> bool` và hằng `_HAN_CHO_CAY_TRUOC_BAM_LOG = 10.0` (giây, bằng `bo_loc.ket_thuc(10)`), tra theo tên lúc chạy. Tham số `job` để dành cho packet B, A không dùng. **Nền mà `_nen_do_cay_truoc_bam()` trả `False` thì hàm đợi trả `False` NGAY: không dò, không ngủ.** Trên Linux: một deadline monotonic `het = monotonic() + han` phủ lần dò đầu, mọi lần dò và mọi lần ngủ. Mỗi vòng: `con_lai = het - monotonic()`, `<= 0` ⇒ `False`; dò ĐÚNG MỘT lần `_thanh_vien_nhom(pid)` (một đối số, giữ tương thích stub ở dòng 1942, 2112, 2834, 13927 của `launcher_test.py`); `None` ⇒ `False` ngay; lấy mốc SAU lần dò `con_sau = het - monotonic()`, `<= 0` ⇒ `False` (bỏ kết quả của lần dò quá hạn, kể cả `[]`); `[]` ⇒ `True`; còn thành viên ⇒ ngủ `min(0,1, con_sau)` rồi lặp. Docstring khai: quét `/proc` là lời gọi đồng bộ, tổng thời gian ≤ `han` cộng một lần dò. **Chỗ đặt trong `lenh_run`:** sau khối chụp workspace và chuẩn hoá `ma` (dòng 2913–2951), TRƯỚC chú thích và phép đọc lại sổ (dòng 2954–2957), theo thứ tự: `ket_thuc = _bay_gio()` (dời lên từ dòng 2999) → mốc monotonic → gọi đợi → ghi `log_bam_cay_da_chet`/`log_bam_cho_giay` → `so_moi = _doc_so(...)`. Vì vậy `stop` hoàn tất trong lúc đợi vẫn được thấy, còn `ket_thuc_utc`/`thoi_luong_giay` không gồm thời gian đợi. **Nền khác Linux:** ngay trước dòng `ban_ghi.update(ket_thuc_utc=…)`, nếu `not _nen_do_cay_truoc_bam()` thì lấy lại `ket_thuc = _bay_gio()`, tức đúng vị trí base (sau phép đo xoá prompt ở dòng 2991, vốn gồm `ps` tới 15 s trên Darwin). **Ctrl-C trong lúc đợi:** bắt `KeyboardInterrupt`, ghi `false`, đặt cờ `ngat_khi_cho`. Cờ chỉ được xét SAU khối áp `kq_chup` (dòng 2972–2978) và chỉ khi `trang_thai == "xong"`: đổi thành `bi_ngat`, `ly_do_dung = "bi ngat trong luc doi cay truoc khi bam log"`, `ma = 130`. KHÔNG đổi `ma_that`, cùng quy tắc `ngat_khi_chup`. Mã mới không được tạo chỗ khớp mới cho mẫu `DOT_BIEN` nào có sẵn: tránh nguyên văn `                return ds == []`, `            time.sleep(0.1)`, `            if ds is None or ds == []:`, `        return _thanh_vien_nhom(pid) == []`; không dùng tên biến `ds`. | `.claude/dev/launcher.py` |
| M3 | `VERSION = "1.6.0"` → `"1.6.1"` (dòng 102). | `.claude/dev/launcher.py` |
| M4 | Mười một ca mới, đăng ký vào `CA`. Nạp module qua `_tai_launcher_thu()`; gọi `m.lenh_run` trong tiến trình theo khuôn `r12`; khôi phục mọi thứ đã vá trong `finally`; khẳng định bằng `bang(...)`, thông điệp định danh ca và vế. MỌI ca gọi `lenh_run` (qua `_r387_chay`), kể cả ca (i) mô phỏng nền khác, bắt đầu bằng `if platform.system() != "Linux": return _R387_CHI_LINUX`. Lý do: teardown hỏi nhóm tiến trình bằng `_thanh_vien_nhom` thật, mà hàm ấy trả `None` trên Windows nên teardown sẽ báo `cay khong do duoc` trước khi ca kịp đo. Đã rà: chỉ (t) và (e) không qua `_r387_chay` và chạy được trên mọi nền ((t) vá phép dò, (e) gọi thẳng hàm đợi với nền vá) (chuỗi bỏ qua nêu tên packet B); tập ca bỏ qua trên Linux không đổi. **Fixture chung (POSIX):** (i) `_r387_chay` đọc hằng hạn bằng `getattr(m, "_HAN_CHO_CAY_TRUOC_BAM_LOG", None)`, để fixture chạy được với `launcher.py` của base (đối chứng N1); bọc `m._thanh_vien_nhom` để ghi lại mọi danh sách phép dò trả, gọi `lenh_run`, rồi lưu `pgid = run.json["pid"]` làm tham chiếu SỞ HỮU. (ii) Con sinh cháu bằng `Popen([PY, "-c", …], stdout=sys.stdout)` (không `start_new_session`) và ghi PID cháu ra tệp; cháu ngủ `N` ≤ 4 s, ghi một dòng, flush, viết dấu `chau-xong`, rồi TỰ thoát. (iii) **Không có đường gửi tín hiệu nào.** Teardown `_r387_don_dep(m, han=8,0)` chờ nhóm của con về `[]` (`_r387_cho_cay_rong` trả ba trạng thái: `True`/`False` hết hạn/`None` không đo được) rồi trả `None` hoặc thông điệp lỗi rõ. Ca có cháu bọc thân trong `with San() as s, _r387_don_khi_thoat(m):`, nên teardown chạy trước `rmtree` của `San` (dòng 177–184), kể cả khi ca đỏ. Ca đã đỏ thì giữ lỗi gốc và gắn thông điệp teardown bằng `add_note`; ca xanh mà teardown lỗi thì ĐỎ. Ca không cháu được `_r387_chay(co_chau=False)` tự teardown. (iv) Phần fixture SAU `lenh_run` của ca có cháu chạy trong `_r387_nhat_ky_kill()`: `os.kill`/`os.killpg` bị thay bằng hàm GIẢ chỉ ghi nhật ký, không bao giờ chuyển tiếp. Bộ ghi không bọc `lenh_run`, vì launcher dùng `os.kill(pid, 0)`. Ca đòi nhật ký RỖNG. (v) Ca chờ `chau-xong` tối đa 10 s; thiếu dấu là ĐỎ. PID cháu phải có trong ít nhất một danh sách đã ghi ở (i). **Các ca:** (t) `r387_fixture_teardown_bao_loi_giu_loi_goc`: phép dò luôn `[7]`, hạn 0,2 s. Thân ném `TinHieuChotCa("LOI-GOC")` ⇒ lỗi vẫn là `LOI-GOC` và `__notes__` chứa `r387 teardown`. Thân không lỗi ⇒ `TinHieuChotCa` mang `r387 teardown`. (a) `r387_m1_chau_ghi_muon_khai_pham_vi_bam`: hạn vá 2,0 s, cháu ngủ 4 s. Vế theo THỨ TỰ: dấu `chau-xong` → **vế băm** `sha256(stdout.log) != stdout_sha256`, thông điệp chứa `ve bam` → PID cháu có trong phép dò → `false` → `1,8 <= log_bam_cho_giay <= 2,5` → `log_bam_luc_utc − ket_thuc_utc >= 1,8 s` → (sau khối ghi) nhật ký kill RỖNG. (a′) `r387_m1_doi_chung_ghi_som_lam_ve_bam_do`: thân (a) với con đợi cháu (`c.wait()`), cháu ngủ 0 s; đòi `TinHieuChotCa` chứa `ve bam`. (b) `r387_m1_con_thuong_chung_minh_cay_chet`: con in một dòng; đòi `true`, `log_bam_luc_utc >= ket_thuc_utc`, băm sổ = băm đĩa; đọc khoá bằng `d.get` rồi `bang`. (c) `r387_m2_chau_ghi_trong_han_thi_bam_du`: hạn mặc định, cháu ngủ 1 s; PID cháu có trong phép dò, `true`, băm sổ = băm đĩa đọc sau dấu. (d) `r387_m2_khong_do_duoc_thi_khong_cho`: hạn vá 5,0 s, `_thanh_vien_nhom` vá trả `None`; đòi `false` và `lenh_run` < 3 s. (e) `r387_m2_han_chung_cho_moi_lan_do`: gọi THẲNG hàm đợi, `m.platform` vá bằng `types.SimpleNamespace`, hạn 0,5 s, dung sai đo 0,5 s (khai trong docstring). (e1) Linux, phép dò luôn `[7]` ⇒ `False` trong ≤ 1,0 s. (e2) Linux, phép dò ngủ 0,6 s rồi trả `[]` ⇒ `False`. (e4) Đồng hồ giả (`m.time` vá thành `monotonic`/`sleep` giả, `sleep` cộng vào đồng hồ), phép dò cộng 0,47 s rồi trả `[7]` ⇒ `False` và đối số ngủ đúng `[0.03]`. (e5) `Darwin`/`Windows`/`FreeBSD`, phép dò vá thành hàm làm ca ĐỎ nếu bị gọi, `m.time.sleep` vá thành bộ ghi ⇒ `False` và 0 lời ngủ. (i) `r387_a_nen_khac_giu_moc_ket_thuc_base` (chạy trên Linux, MÔ PHỎNG nền khác): vá `m._nen_do_cay_truoc_bam = lambda: False`, vá `m._thanh_vien_nhom` thành phép đo giả ngủ 0,5 s rồi trả `[]` (đại diện `ps` Darwin), và bọc `m._bay_gio` để ghi mỗi lần gọi `(giá trị ISO, bản chụp rr/*/prompt.snapshot còn trên đĩa không)`. Lượt chạy có `--prompt-file` thật, con `pass`. Đòi: `false`; `log_bam_cho_giay` < 0,1; `prompt_ban_chup_da_xoa is True`; `thoi_luong_giay` ≥ 0,45 (mốc lấy sau phép đo xoá prompt); và lần gọi `_bay_gio` sinh ra đúng giá trị `ket_thuc_utc` phải ghi "bản chụp KHÔNG còn", tức mốc lấy SAU unlink, đúng vị trí base. (f) `r387_m1_stop_trong_luc_cho_khong_bi_de`: lần dò ĐẦU ghi sổ đúng như nhánh `else` của `lenh_stop` (`trang_thai="da_dung"`, `ly_do_dung="r387-stop-gia"`, `_ghi_so` không khoá) rồi dò thật; đòi sổ cuối giữ `da_dung` và lý do ấy. (g) `r387_m1_prompt_linux_xoa_khi_cay_chet`: `--prompt-file` + `--expected-prompt-sha256`, con `pass`; đòi `true`, tệp bản chụp đã mất, `prompt_ban_chup_da_xoa is True`. (h) `r387_m2_ngat_trong_luc_doi_ghi_bi_ngat`: vá `m._cho_cay_chet_truoc_bam` ném `KeyboardInterrupt`. Vế (h1), con `pass`: `rc == 130`, `ma_thoat == 0`, `bi_ngat`, `ly_do_dung` đúng chuỗi M2, `false`, `stdout_sha256` khác rỗng. Vế (h2), `--chup-workspace` và con ghi một tệp mới vào workspace: `rc == MA_GHI_WORKSPACE`, `trang_thai == "ghi_workspace"`. | `.claude/dev/launcher_test.py` |
| M5 | Sửa đúng MỘT neo: `xoa_prompt_khi_wrapper_vua_thoat` neo sang dòng gọi đợi (vd `        log_cay_chet = _cho_cay_chet_truoc_bam(p.pid, job, _HAN_CHO_CAY_TRUOC_BAM_LOG)`), thay bằng `True` không chờ, ca đích `t76`. | `.claude/dev/launcher_test.py` |
| M6 | Mười sáu đột biến mới trong `DOT_BIEN`, không mục nào mang điều kiện nền. Mỗi mẫu `(tìm, thay)` lấy nguyên văn và khớp đúng một chỗ; không thêm gì vào `DA_BIET_TRUNG`. Danh sách, dạng tên (thay đổi) → ca đích: `r387_khai_cay_chet_luon_true` (gán khoá sổ `True`) → (a); `r387_khai_cay_chet_luon_false` (gán `False`) → (b); `r387_moc_bam_truoc_khi_con_thoat` (`log_bam_luc_utc` = `bat_dau_utc`) → (b); `r387_ket_thuc_sau_vong_cho` (`ket_thuc_utc` lấy `_bay_gio()` tại dòng ghi) → (a); `r387_bo_vong_cho` (hạn truyền vào thành `0`) → (c); `r387_khong_do_duoc_van_cho` (nhánh `None` không trả ngay) → (d); `r387_nhan_ket_qua_sau_han` (nhánh `con_sau <= 0` gán `con_sau = 0.0` thay vì trả `False`; KHÔNG dùng `pass`, vì sleep âm thành tín dụng giả) → (e); `r387_ngu_khong_tru_lan_do` (`min(0.1, con_sau)` thành `0.1`) → (e); `r387_a_nen_khac_van_do` (bỏ `return False` của nền khác Linux) → (e); `r387_a_nen_khac_ngu_thua` (chèn `time.sleep(0.1)` trước `return False` ấy) → (e); `r387_a_nen_khac_doi_moc` (bỏ dòng lấy lại `ket_thuc` cho nền khác) → (i); `r387_a_nen_khac_moc_truoc_unlink` (hai thay thế áp tuần tự: xoá khối lấy lại `ket_thuc` ở chỗ cũ, rồi chèn chính khối ấy ngay sau dòng `cay_da_chet = …`, tức trước khối unlink; thứ tự này cần vì runner thay chỗ khớp ĐẦU TIÊN) → (i); `r387_cho_sau_doc_lai_stop` (dời CẢ khối `try`/lời gọi đợi và dòng ghi khoá xuống SAU `so_moi = _doc_so(...)`) → (f); `r387_ngat_khi_doi_bi_nuot` (điều kiện ngắt thành `False`) → (h); `r387_ngat_che_ket_qua_chup` (bỏ vế `trang_thai == "xong"`) → (h); `r387_ngat_ghi_130_vao_so` (thêm `ma_that = 130`) → (h). Hai đột biến `DOT_BIEN_HARNESS`: `r387_fixture_gui_tin_hieu_theo_pid_chau` (chèn `os.kill(pid_chau, signal.SIGTERM)` sau dòng đọc PID cháu trong (a); lời gọi rơi vào hàm giả, ca chết ở vế nhật ký) → (a); `r387_teardown_nuot_loi` (`e.add_note(loi)` thành `pass`) → (t). | `.claude/dev/launcher_test.py` |

## 4. `nghiem_thu`

Mọi số công bố kèm thời điểm UTC tới giây, phiên bản công cụ, lệnh nguyên văn, mã thoát. Phép đo tay ghi tách khỏi
kết quả runner.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux, Python 3.13 của gate: (a), (a′) ĐẠT trên head. (a) ĐỎ trên base: chạy `launcher_test.py` của head với `launcher.py` của base qua `--lap-ca`, ghi dòng `LAP …`/`HONG …` và rc. Đỏ phải là `TinHieuChotCa: r387(a) cay chua chet ma khai None`, tức ca đã qua vế băm (sổ ≠ đĩa, lỗi #387 tái hiện) rồi đỏ ở vế khoá; một `AttributeError`/`KeyError` hay lỗi fixture khác KHÔNG tính là đỏ đúng (đã đo, §0). | `r387_khai_cay_chet_luon_true`, `r387_ket_thuc_sau_vong_cho`, `r387_fixture_gui_tin_hieu_theo_pid_chau` qua runner ⇒ mỗi cái `OK giet 1/1` ca (a). Đo tay trên bản sao: xoá vế băm khỏi (a) ⇒ (a′) ĐỎ. |
| N2 | (b) ĐẠT. | `r387_khai_cay_chet_luon_false`, `r387_moc_bam_truoc_khi_con_thoat` ⇒ (b). Đo tay: xoá dòng gán `log_bam_luc_utc` ⇒ (b) ĐỎ bằng `TinHieuChotCa`, không `KeyError`. |
| N3 | (t), (c), (d), (e), (i), (f), (g), (h) ĐẠT; mười một ca cộng lại dưới 25 s wall trên Linux. | `r387_teardown_nuot_loi` ⇒ (t); `r387_bo_vong_cho` ⇒ (c); `r387_khong_do_duoc_van_cho` ⇒ (d); `r387_nhan_ket_qua_sau_han`, `r387_ngu_khong_tru_lan_do`, `r387_a_nen_khac_van_do`, `r387_a_nen_khac_ngu_thua` ⇒ (e); `r387_a_nen_khac_doi_moc`, `r387_a_nen_khac_moc_truoc_unlink` ⇒ (i); `r387_cho_sau_doc_lai_stop` ⇒ (f); `xoa_prompt_khi_wrapper_vua_thoat` (neo M5) ⇒ `t76`; ba đột biến `r387_ngat_*` ⇒ (h). Mỗi cái `OK giet 1/1` đúng ca đích (đã đo trên vá thử, §0). |
| N4 | `launcher_test.py` trên head: N/N, hai số BẰNG NHAU; tập ca bỏ qua trên Linux đúng bằng base. `t76`, `t67`, `t71`, `t77`, `r14`, `r1252_*`, `t117` ĐẠT. `launcher_test.py --dot-bien` trên Linux: rc 0, dòng cuối `DOT BIEN: N/N dat` hai số bằng nhau. Mọi mục `DOT_BIEN` ĐO ĐƯỢC trên Linux phải `OK`, gồm đủ 18 đột biến mới của A (16 `DOT_BIEN` + 2 `DOT_BIEN_HARNESS`) và neo M5. Các mục `KHONG DO DUOC tren nen nay` được phép là ĐÚNG sáu mục kế thừa từ base, liệt kê riêng: (1) năm mục mang điều kiện `windows`; (2) MỘT mục qua được bộ lọc nền nhưng ca đích tự bỏ qua trên Linux, là `124_khi_chau_con_song` (điều kiện `posix`, ca đích `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, cần fixture Windows). Dòng cuối runner trên head đủ bảng phải có dạng `DOT BIEN: N/N dat  (6 khong do duoc tren nen nay)`; số khác 6 ⇒ ĐỎ, trừ khi giải thích được bằng thay đổi của base. Kèm ngoại lệ trùng của `t117`. Báo đúng: MỘT neo sửa, MƯỜI SÁU đột biến `DOT_BIEN` mới, HAI đột biến `DOT_BIEN_HARNESS` mới. | Không sửa neo M5 ⇒ `t117` ĐỎ. Thêm một dòng `            time.sleep(0.1)` vào mã mới ⇒ `t117` ĐỎ. |
| N5 | **Không đổi hành vi băm trên Darwin/Windows** (M1, M2, §2), nên A KHÔNG đòi phép đo native. Đường nền khác Linux được đo trên Linux bằng (e5), (i) và các đột biến `r387_a_nen_khac_*`. Biểu thức xoá prompt của nền khác là nguyên văn base. Phép đo native Windows thuộc packet B. | (e5) ĐỎ nếu hàm đợi dò trên nền khác Linux. Chưa đo trên Windows/Darwin thật: §8. |
| N6 | Trên exact head, ghi lệnh + phiên bản + rc + bằng chứng dương: `ruff check --no-cache --select F` hai tệp, delta 0 so base (base rc 1, 5 F841); `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `python .claude/dev/packet_loop.py adr-song --root .` rc 0; `git diff --check base..H` rỗng; `git diff --numstat base..H` đúng 2 tệp, tổng cột thêm ≤ 450; `python .claude/dev/launcher.py doctor` rc bằng base trên cùng máy; `run.json` của một lượt `run` có `"version": "1.6.1"` và đủ ba khoá M1. | ruff: thêm tên chưa định nghĩa trên bản sao ⇒ delta ≠ 0. `git diff --check`: thêm khoảng trắng cuối dòng ⇒ không rỗng. numstat: đường dẫn thứ ba ⇒ 3 tệp. Quên M3 ⇒ `1.6.0`. `doctrine-scan`/`adr-song`/`doctor`: không có phản chứng ở packet này; ghi `phép đỏ: chưa đo`, chỉ báo rc. |

## 5. `pham_vi_e`

Không chạm E4, không chạm E5.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước theo dòng khai `ADR-0053` (450 dòng thêm). Theo quyết định của chủ kho (tiền lệ #433), không xin
  `nang_tran`. Vá thử A đo 410 dòng thêm (§0); bản thi hành viết gọn như vá thử, dự toán 410–445 (biên tới trần chỉ còn 40). TRƯỚC khi mở
  review, đo `git diff --numstat base..H`; tổng cột thêm vượt 450 ⇒ DỪNG và đi revision đặc tả. Không nén chú thích
  để lọt trần.
- Cần sửa ngoài write set (người đọc `stdout_sha256`/`ket_thuc_utc`/`thoi_luong_giay`, hay một bộ khoá cố định của
  `run.json` mà §0 không thấy) ⇒ dừng và đi revision đặc tả. Tầm quét preflight trên exact base:
  `git grep -n -E 'stdout_sha256|ket_thuc_utc|thoi_luong_giay|log_bam_|run\.json' -- '*.py' ':!ops/**'`.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung` — thêm lời khai phạm vi cho băm log, không phải packet khắc phục một bản vá cũ.

## 8. `chua_do_duoc`

- Windows và Darwin thật: chưa chạy. A giữ biểu thức base cho quyết định xoá prompt trên các nền ấy và ghi khoá sổ
  `false`. Đường hàm đợi chỉ được thử bằng `m.platform` vá ở (e5). Đo native là việc của packet B.
- Giới hạn có tên (viết vào docstring M1): cháu `setsid()`/`start_new_session` rời nhóm thì `true` có thể SAI cho nó.
  Không có ca cho tiến trình ngoài phạm vi.
- Dung sai thời gian ở (a), (d), (e) (0,5 s; trần 2,5 s cho lần đợi 2,0 s) chỉ đo trên container này. Nới thì ghi số đo
  và lý do.
- Thời lượng một lần quét `/proc` trên máy tải nặng chưa đo; M2 chỉ hứa bỏ kết quả của lần dò quá hạn.
- Ca đỏ giữa chừng có thể để cháu sống thêm tới `N` ≤ 4 s; teardown đợi tối đa 8 s rồi báo lỗi, không gửi tín hiệu.
- Dự toán: vá thử đo 410 (+46 và +364, 2026-11-18T08:56Z). Bản thi hành có chú thích ước 410–445, vượt mục tiêu
  420 của điều phối; trần cứng 450 và luật dừng ở §6 không đổi.

## 9. Lịch sử sửa theo review (revision 1, chưa đóng băng)

Bảng `L1`–`L7` mà các lượt review nhắc là bảy luật soạn đặc tả ở `.claude/skills/soan-spec/SKILL.md` §2 ("Bảy luật
riêng của kho", dòng 36), không phải mục của tệp này. Đối chiếu từng luật:
- L1: mọi con số "N cái" nói đếm gì.
- L2: mỗi M chiếu vào một đường dẫn trong write set.
- L3: mỗi N có cột phép đo làm nó ĐỎ.
- L4: `khong_ap_dung`.
- L5: số kèm mốc giờ; mốc không chính xác thì ghi đúng như vậy.
- L6: tiêu chí khớp chuỗi là dòng `LAP`/`OK giet`/`DOT BIEN: N/N dat` của runner, mỗi cái kèm đột biến đổi màu.
- L7: `luat_dung` chỉ dẫn `ADR-0053`, `ADR-0055`, `ADR-0067` và mã E2.

Các lượt sửa:
- Lượt 1 (`813795bd…` → `eccb0d34…`):
  - Deadline monotonic chung; vòng đợi đặt trước phép đọc lại sổ cho `stop`.
  - Phạm vi `true`; giữ `ket_thuc_utc`/`thoi_luong_giay`, thêm `log_bam_cho_giay`.
  - Ca (a′), ca prompt, ca Ctrl-C (h).
- Lượt 2 (`eccb0d34…` → `7611a4a0…`):
  - Bỏ kết quả của lần dò quá hạn.
  - Ctrl-C giữ `ma_that` và xét sau `kq_chup`; ca (h2).
  - Giờ chính xác.
- Lượt 3 (`7611a4a0…` → `b8a7f053…` → `9181b833…`):
  - Ngủ tính từ mốc sau lần dò.
  - Chốt trần: không `nang_tran`.
- Lượt 4 (`9181b833…` → `633e7500…`):
  - Bỏ đường gửi tín hiệu theo PID (hai lượt cùng hình dạng).
  - Ca (e4) đồng hồ giả.
  - Thêm §9.
- Lượt 5 (`633e7500…` → `cefbebe6…`):
  - Bộ ghi kill thành hàm giả.
  - Teardown chạy cả khi ca đỏ, giữ lỗi gốc; ca (t).
  - Dẫn đúng vị trí L1–L7.
- **Tách** (`cefbebe6…` → bản này), theo chỉ thị điều phối và tiền lệ #433. Vá thử gộp đo 415 dòng thêm, biên tới trần
  chỉ còn 35, nên tách ngay thay vì tách sau. A giữ M1–M3 cho Linux. Nhánh Darwin (`han_giay` cho `ps`), nhánh Windows
  (dò job từng lần, giữ bản chụp prompt), bắt tay `job-da-gan`, teardown đóng handle job, phần Darwin/Windows của ca
  (e), vế Windows của ca prompt, và bốn đột biến `r387_darwin_bo_han`, `r387_ps_giu_timeout_15`,
  `r387_windows_long_cay_da_chet`, `r387_windows_xoa_prompt_khi_job_rong` chuyển sang packet B. A không mang mã nền nào
  thiếu ca đo: nền khác Linux trả `false` không dò (có (e5) và đột biến), quyết định xoá prompt ở đó là biểu thức base.
  Numstat đo trên vá thử lúc tách: A = +364 (so base), B = +118 (so A).
- Lượt 6 (`85cd970f…` → bản này), chỉ cho A:
  - Nền khác Linux giữ mốc `ket_thuc` ở vị trí base; thêm `_nen_do_cay_truoc_bam()`, ca (i), đột biến
    `r387_a_nen_khac_doi_moc`.
  - Fixture đọc hằng bằng `getattr`, nên chạy được với base; N1 đòi đỏ đúng vế khoá (đã đo).
  - (e5) đòi 0 lời ngủ; đột biến `r387_a_nen_khac_ngu_thua`.
  - A lên 400 dòng thêm.
- Lượt 7 (`14442304…` → bản này), chỉ cho A:
  - Ca (i) chỉ chạy trên Linux, mô phỏng nền khác bằng `_nen_do_cay_truoc_bam`; đã rà mọi ca A dùng `_r387_chay`.
  - Ca (i) dùng bản chụp prompt thật và ghi trạng thái bản chụp tại từng lần gọi `_bay_gio`; đột biến
    `r387_a_nen_khac_moc_truoc_unlink` (dời mốc lên trước unlink) bị giết.
  - A lên 410 dòng thêm.
- Lượt 8 (`b65b8971…` → bản này), chỉ đặc tả: N4 liệt kê ngoại lệ kế thừa `124_khi_chau_con_song` cạnh năm mục
  `windows`, đòi đúng 6 mục `KHONG DO DUOC` trên head và đủ 18 đột biến mới `OK`. Đã rà toàn bảng base và đo
  trên base (§0).
