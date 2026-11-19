tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-BAM-LOG-NEN-DARWIN-WINDOWS r1 — mở lời khai phạm vi băm log của `run.json` sang Darwin và Windows

- packet_id: LAUNCHER-BAM-LOG-NEN-DARWIN-WINDOWS; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #387 |
| `nguon_cap_viec` | Phần tách ra từ đặc tả `LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1` (packet A, `ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md`). Theo chỉ thị điều phối ngày 18-11-2026 và tiền lệ #433 (tách, không nâng trần), mã nhánh Darwin/Windows đi CÙNG ca đo của nó, không để A mang mã nền thiếu ca đo. Nội dung kỹ thuật đã qua năm lượt review Codex khi còn gộp (lịch sử ở §9 của A). |
| `phu_thuoc` | Packet A đã **land** trên nhánh mặc định. Chưa land ⇒ không cấp lease (§6). |
| `review_class` | `sensitive`: cùng hai tệp, cùng lý do với A. Đối chiếu bằng `lease_publish check` khi cấp lease. |
| `base` | Commit land của A trên `origin/master` (CHƯA có lúc soạn); lease ghi OID thật lúc cấp và phải chứa commit land của A. Số dòng §0 dưới đây là của bản vá thử A dựng trên `641108c`, phải đo lại trên base thật. |

## 0. Hiện trạng (đo trên bản vá thử, Linux, Python 3.13.18; số dòng của `641108c` trừ khi ghi khác)

- Sau packet A (theo vá thử `trA`):
  - `_cho_cay_chet_truoc_bam` trả `False` NGAY trên nền khác Linux.
  - `lenh_run` quyết định xoá bản chụp prompt bằng `log_cay_chet if platform.system() == "Linux" else
    (_thanh_vien_nhom(p.pid) == [])`.
  - `_thanh_vien_nhom(pgid)` còn `timeout=15` cứng cho `ps` trên Darwin (dòng 583 của base).
  - Ca r387 của A trả chuỗi `_R387_CHI_LINUX` (bỏ qua) trên nền khác Linux.
- Base `641108c`, các chỗ B dựa vào:
  - Windows: `_job_windows` (dòng 872) gán job SAU `Popen`; chú thích 882–886 khai khe "cháu sinh trước lúc gán nằm ngoài
    job". Job mang `KILL_ON_JOB_CLOSE` (dòng 925). `lenh_run` không bao giờ đóng handle job. `_pid_trong_job` (dòng 943)
    trả `[]`/danh sách/`None`.
  - `_cay_da_chet` (dòng 1091) lồng vòng 20 × 0,1 s quanh `_pid_trong_job`; B không được dùng nó trong hàm đợi.
  - Stub một đối số thay `m._thanh_vien_nhom` có ở dòng 1942, 2112, 2834, 13927 của `launcher_test.py` ⇒ chỉ Darwin được
    truyền đối số tên `han_giay`. Tiền lệ vá `m.platform`: dòng 13911–13930.
  - Neo đột biến `nhom_luon_rong` (dòng 16057–16059) neo chữ ký `def _thanh_vien_nhom(pgid: int) -> list[int] | None:`
    cùng đầu docstring, ca đích `t67`. `t76` tự bỏ qua trên Windows (dòng 1759–1760).
- **Vá thử B** (vá thử gộp `tr387` = A + B, so với `trA`):
  - Kích thước: **`launcher.py` +15/−9, `launcher_test.py` +103/−62, tổng 118 dòng thêm**. Gộp A+B so base:
    `launcher.py` +47/−5, `launcher_test.py` +368/−4.
  - Từng ca `python3 -B .claude/dev/launcher_test.py --lap-ca <ca> --lan 1` trên bản gộp, 2026-11-18T06:38:35Z →
    06:38:52Z cùng các lượt ngay sau: mười ca r387 và `t117` đều `1/1 qua`.
  - Runner `--dot-bien` trên bản sao đủ cây của bản gộp, `DOT_BIEN` lọc còn r387 và hai neo, 06:39:25Z → 06:44:21Z,
    **rc 0**, `DOT BIEN: 177/177 dat (1 khong do duoc tren nen nay)`, 0 dòng `SAI`. Bốn đột biến của B đo được trên Linux
    gồm `r387_darwin_bo_han`, `r387_ps_giu_timeout_15`, `r387_windows_long_cay_da_chet`, đều `OK giet 1/1` ca (e).
    `r387_windows_xoa_prompt_khi_job_rong` ra `KHONG DO DUOC tren nen nay`. `nhom_luon_rong` với neo mới `giet 1/1 t67`.
  - Toàn bộ suite bản gộp (06:44:25Z → 06:51:14Z, rc 0): `423/423 (tong 425, bo qua 2, hong 0)`, hai ca bỏ qua đúng
    bằng base.
  - Chưa chạy trên Windows hay Darwin thật.

## 1. `write_set`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- Không đổi phần Linux của A (hàm đợi, thứ tự trong `lenh_run`, Ctrl-C, ba khoá sổ, fixture POSIX, teardown không gửi
  tín hiệu).
- Không đóng khe gán job sau `Popen` (chú thích 882–886), không theo dõi cháu `setsid`/breakaway: giới hạn được khai.
- Không đổi `_cay_da_chet` và nhánh chụp workspace. Không thêm thẻ `# launcher-nang-luc:`. Không sửa người đọc ngoài
  launcher.
- Không dùng CI Windows (nhãn `windows`, `workflow_dispatch`): ràng buộc chủ kho. Windows đo native trên máy chủ kho.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Hàm đợi của A mở sang Darwin và Windows. Bỏ nhánh "nền khác Linux trả `False` ngay"; mỗi vòng dò ĐÚNG MỘT lần theo nền, giữ nguyên deadline, thứ tự xét kết quả và cách ngủ của A. Linux: `_thanh_vien_nhom(pid)` (một đối số). Darwin: `_thanh_vien_nhom(pid, han_giay=con_lai)`, với chữ ký mới `def _thanh_vien_nhom(pgid: int, han_giay: float = 15) -> list[int] \| None:` và `timeout=han_giay` thay `timeout=15` trong lời gọi `ps`; mặc định 15 giữ mọi người gọi cũ; `han_giay` nhỏ làm `ps` ném `TimeoutExpired` ⇒ `None` ⇒ `False`. Windows: `_pid_trong_job(job) if job is not None else None`, dò job từng lần, KHÔNG gọi `_cay_da_chet`. Nền khác: `None`. Docstring đổi nghĩa `true` thành: "phép dò trả rỗng trong nhóm tiến trình POSIX hoặc Job Object Windows được theo dõi; tiến trình rời nhóm/job (`setsid`, breakaway) hoặc sinh trước lúc gán job nằm ngoài phạm vi". Docstring khai thêm: `/proc` và `QueryInformationJobObject` là lời gọi đồng bộ, còn `ps` bị chặn bởi `timeout`. | `.claude/dev/launcher.py` |
| M2 | Quyết định xoá bản chụp prompt thành `cay_da_chet = log_cay_chet and platform.system() != "Windows"`. Darwin dùng kết quả đợi; Windows vẫn KHÔNG BAO GIỜ xoá ngay, kể cả khi job chứng minh rỗng (`_cap_id` quét về sau); nền khác đã `false`. Dòng `            and cay_da_chet):` giữ nguyên từng byte. | `.claude/dev/launcher.py` |
| M3 | `VERSION = "1.6.1"` → `"1.6.2"`. | `.claude/dev/launcher.py` |
| M4 | Mở fixture và ca của A sang ba nền. Không ca r387 nào còn trả chuỗi bỏ qua; gỡ `_R387_CHI_LINUX`. **Fixture:** (i) **Bắt tay cho MỌI con**, kể cả con không sinh cháu: mã con luôn có phần mở đầu chung chờ tệp `job-da-gan` tối đa 10 s, không thấy thì thoát mã 3. `_r387_chay` bọc `m._job_windows`: gọi bản thật, nếu có job thì lưu handle rồi ghi `job-da-gan`; trên POSIX ghi sẵn tệp ấy. Sau `lenh_run`, đòi `ma_thoat != 3`; trên Windows đòi thêm `job_windows is True` và đã lưu handle. (ii) Ghi lại danh sách trả của cả `m._thanh_vien_nhom` (nhận `**k`) lẫn `m._pid_trong_job`. Trong ca có cháu, PID cháu phải có trong ít nhất một danh sách (trên Windows là `_pid_trong_job(job)` của đúng job đã gán). (iii) Teardown giữ thiết kế của A (không gửi tín hiệu, chạy cả khi ca đỏ, giữ lỗi gốc), thêm nhánh Windows. `_r387_cho_cay_rong` hỏi `m._pid_trong_job(job)` bằng handle sở hữu. `_r387_don_dep` chỉ đóng handle (`ctypes.windll.kernel32.CloseHandle`) SAU bước chờ, ĐÚNG MỘT lần, và xoá tham chiếu ngay sau khi đóng. Lý do: `KILL_ON_JOB_CLOSE` khiến đóng sớm sẽ giết cháu; hết hạn mà vẫn đóng thì chỉ kết liễu thành viên của job sở hữu. (iv) Bộ ghi `_r387_nhat_ky_kill()` chỉ bọc `killpg` khi nền có (Windows không có). **Ca:** (a), (c) như A, thêm vế PID cháu theo nền. (d), (f) chọn phép dò để vá theo nền (`_pid_trong_job` trên Windows, `_thanh_vien_nhom` trên POSIX). (e) bỏ vế (e5) của A, thêm ba vế. (e1-Darwin) stub `ps_cham(pgid, han_giay=15)` ghi lại `han_giay`, ngủ `min(han_giay, 3,0)`, trả `[7]` ⇒ `False` trong ≤ 1,0 s và mọi `han_giay` ≤ 0,5. (e1-Windows) `_pid_trong_job` luôn `[7]`, `m._cay_da_chet` vá thành hàm làm ca ĐỎ nếu bị gọi ⇒ `False` trong ≤ 1,0 s. (e3) Darwin với `_thanh_vien_nhom` THẬT và `m.subprocess` vá thành `SimpleNamespace(SubprocessError=…, run=stub)`; stub ghi lại `timeout` và trả `returncode=0, stdout=""` ⇒ `True` và `timeout` ≤ 0,5. (g) đổi tên thành `r387_m1_prompt_windows_giu_posix_xoa`, hai vế. Windows: `job_windows is True`, `log_bam_cay_da_chet is True`, tệp bản chụp CÒN, không có `prompt_ban_chup_da_xoa`. POSIX: như A. | `.claude/dev/launcher_test.py` |
| M5 | Sửa neo `nhom_luon_rong` sang chữ ký mới của `_thanh_vien_nhom` (cùng đầu docstring), giữ ca đích `t67`. | `.claude/dev/launcher_test.py` |
| M6 | Gỡ đột biến `r387_a_nen_khac_van_do` của A (dòng nó neo không còn). Thêm bốn đột biến `DOT_BIEN`, mẫu nguyên văn, mỗi mẫu khớp đúng một chỗ: `r387_darwin_bo_han` (Darwin gọi `_thanh_vien_nhom(pid)` không `han_giay`) → (e); `r387_ps_giu_timeout_15` (`timeout=han_giay` thành `timeout=15`) → (e); `r387_windows_long_cay_da_chet` (nhánh Windows dò bằng `[] if _cay_da_chet(pid, job) else [7]`) → (e); `r387_windows_xoa_prompt_khi_job_rong` (bỏ vế `and platform.system() != "Windows"`) → (g), MANG điều kiện nền `("windows", "POSIX van xoa khi cay chet; chi Windows giu ban chup")`. Sau B: mười sáu đột biến r387 trong `DOT_BIEN` (mười lăm đo trên Linux) và hai trong `DOT_BIEN_HARNESS`. | `.claude/dev/launcher_test.py` |

## 4. `nghiem_thu`

Mọi số công bố kèm thời điểm UTC tới giây, phiên bản công cụ, lệnh nguyên văn, mã thoát.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux: (e) và (g) ĐẠT; mọi ca r387 của A vẫn ĐẠT. | `r387_darwin_bo_han`, `r387_ps_giu_timeout_15`, `r387_windows_long_cay_da_chet` qua runner ⇒ mỗi cái `OK giet 1/1` ca (e) (đã đo trên vá thử gộp, §0). |
| N2 | `t67` vẫn bị giết bởi `nhom_luon_rong` với neo mới; `t117` ĐẠT. | Không sửa neo M5 ⇒ `t117` ĐỎ (mẫu cũ mất chỗ khớp). |
| N3 | `launcher_test.py` trên head (Linux): N/N, hai số bằng nhau, tập bỏ qua đúng bằng base. `--dot-bien`: rc 0, `DOT BIEN: N/N dat`. Liệt kê riêng `KHONG DO DUOC tren nen nay`: 5 mục `windows` của base cộng `r387_windows_xoa_prompt_khi_job_rong`. | Như A N4. |
| N4 | Linux: không ca r387 nào còn trả chuỗi bỏ qua (tìm dòng `BO QUA r387` trong log ⇒ 0). | Còn `_R387_CHI_LINUX` ở một ca ⇒ dòng `BO QUA r387…` xuất hiện trên Windows (đo ở N5). |
| N5 | **Windows, đo NATIVE trên máy Windows của chủ kho** (phiên điều phối qua Desktop; KHÔNG dùng nhãn `windows` hay `workflow_dispatch` của CI). Ghi kèm `git rev-parse HEAD` (bằng exact head), `python --version`, `python -c "import platform;print(platform.platform())"`, giờ UTC. **Danh sách CHUNG cho cả hai cách chạy:** (L1) mười ca r387 cộng `t71`, `t77`: mỗi ca `1/1 qua, 0 bo qua, 0 hong`. (L2) mười sáu đột biến r387 trong `DOT_BIEN` cộng hai trong `DOT_BIEN_HARNESS`: mỗi mục giết đúng ca đích; riêng `r387_windows_xoa_prompt_khi_job_rong` bắt buộc đo ở đây. (L3) hai neo không thuộc danh sách phải đo: `xoa_prompt_khi_wrapper_vua_thoat` miễn đo (`t76` tự bỏ qua trên Windows); kết quả `nhom_luon_rong` là tuỳ chọn. Bằng chứng giết của hai neo này nằm ở N2 và A N3 (Linux). **Hai cách chạy:** (A) `python .claude/dev/launcher_test.py --lap-ca <ca> --lan 1` cho L1, rồi `python .claude/dev/launcher_test.py --dot-bien` đủ. (B) Như (A) cho L1. Cho L2 dùng CHÍNH runner `--dot-bien` (đối chứng neutral, phân hạng theo `TinHieuChotCa`) trên một bản sao đủ cây của exact head (`git archive`), với bảng `DOT_BIEN` lọc còn các mục r387 bằng script `ast.literal_eval`; ghi sha256 tệp đã lọc và danh sách tên mục. Hai cách đòi cùng bằng chứng: `OK giet 1/1: <ca đích>` cho từng mục L2 và dòng cuối `DOT BIEN: N/N dat` hai số bằng nhau. | Ca L1 in `bo qua` hoặc `hong` ⇒ ĐỎ. Mục L2 sống hoặc chết sai ca ⇒ ĐỎ. Các tình huống sau làm ca ĐỎ bằng `TinHieuChotCa`, không thành bỏ qua: thiếu job, con thoát mã 3, thiếu PID cháu trong `_pid_trong_job(job)`, thiếu dấu `chau-xong`, teardown báo lỗi. `git rev-parse HEAD` khác exact head ⇒ N5 vô hiệu. Trước khi có log native: `chưa đo được`. |
| N6 | Như A N6, với `"version": "1.6.2"` và `git diff --numstat base..H` (base = land của A) đúng 2 tệp, tổng thêm ≤ 450. | Như A N6. |

## 5. `pham_vi_e`

Không chạm E4, không chạm E5.

## 6. `luat_dung`

- Packet A chưa land trên nhánh mặc định ⇒ không cấp lease, không thi hành (`phu_thuoc`).
- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước theo dòng khai `ADR-0053` (450 dòng thêm); không xin `nang_tran` (tiền lệ #433). Vá thử đo 118, cận
  trên dự toán 180. Vượt 450 ⇒ DỪNG và đi revision đặc tả.
- Chưa có log native Windows (N5) ⇒ không công bố `landed`/`ready`; báo N5 `chưa đo được`.
- Cần sửa ngoài write set ⇒ dừng và đi revision đặc tả.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung` — phần nền của một packet tách, không phải packet khắc phục một bản vá cũ.

## 8. `chua_do_duoc`

- Toàn bộ hành vi Windows chưa chạy thật:
  - bắt tay `job-da-gan` có giữ được con tới lúc gán job không;
  - cháu `Popen(stdout=sys.stdout)` có nằm trong job và giữ handle `stdout.log` không;
  - danh sách job cập nhật trễ có quá hạn 10 s không;
  - teardown chờ job rỗng rồi `CloseHandle` một lần có chạy đúng không.
  N5 là phép đo duy nhất.
- Darwin: không có máy. Chỉ thử bằng `m.platform`/`m.subprocess` vá ở (e); `ps` thật với `timeout` nhỏ chưa chạy.
- Giới hạn có tên: cháu `setsid`/breakaway, hoặc sinh trong khe giữa `Popen` và gán job, thì `true` có thể sai.
- Dung sai thời gian của (e) chỉ đo trên container Linux; máy Windows chậm hơn có thể cần nới — nới thì ghi số đo.
- Số dòng §0 đo trên vá thử dựng từ `641108c`; phải đo lại trên base thật (land của A).

## 9. Việc mở cho revision sau (ghi 18-11-2026, CHƯA sửa; sửa sau khi A land, trước khi cấp lease cho B)

Nguồn: review Codex lượt 6 (cho A) ghi kèm hai điểm thuộc phạm vi B. Chúng chưa được sửa ở bản này. Hai lý do: điều phối
chỉ thị không sửa B lúc này, và B phải dựng lại trên base thật (land của A).
- **P2 — teardown khi hết hạn trên Windows.** M4 (iii) gọi `CloseHandle` mà không kiểm giá trị trả về. Ngoài ra
  `San.__exit__` (`launcher_test.py` dòng 177–184) `rmtree(…, ignore_errors=True)` nuốt mất thư mục sót khi cháu còn
  giữ `stdout.log`. Revision B phải kiểm kết quả `CloseHandle` (thất bại ⇒ lỗi rõ, giữ lỗi gốc như A), và không để thư
  mục sót bị nuốt im lặng (đo thư mục còn sau `rmtree`, hoặc đòi teardown chứng minh job rỗng trước khi xoá).
- **P3 — N4 đếm `BO QUA` trên sai nền.** N4 tìm dòng `BO QUA r387` trong log Linux, nhưng chuỗi bỏ qua của A chỉ xuất
  hiện trên nền khác Linux. Phép đếm phải chạy trên log Windows native (N5), không phải log Linux. Revision B phải
  chuyển tiêu chí ấy vào N5 hoặc đổi nền đo.
- Số dòng §0 của B đo so với vá thử A TRƯỚC lượt 6 của A (`trA` 364 dòng). A sau lượt 6 đổi thêm `_nen_do_cay_truoc_bam`,
  ca (i) và hai đột biến `r387_a_nen_khac_*`. B phải gỡ hai đột biến ấy (hoặc đổi neo) khi mở nhánh Darwin/Windows, nên
  đo lại numstat trên land thật của A.

## 10. Đo lại trên base thật và câu hỏi CHẶN (ghi 19-11-2026, trước mọi lượt Codex)

Base đo: `origin/master` `3b647461db7c8ded1bddd9aafc5c6aa5eead223f` (chứa land A `e4fdf09`). A land KHÁC vá thử `trA` mà §0/§3
mô tả, nên §0, M1, M2, M6 phải viết lại trên base này trước khi review:
- `launcher.py`: `VERSION = "1.6.1"` (102); `_thanh_vien_nhom(pgid)` 542 (một đối số; `ps … timeout=15` ở 583);
  `_nen_do_cay_truoc_bam()` 605 là CHỖ DUY NHẤT quyết nền (trả `platform.system() == "Linux"`); `_cho_cay_chet_truoc_bam`
  610 trả `False` ngay ở 619 khi nền không phải Linux; `_job_windows` 906 (`KILL_ON_JOB_CLOSE` 959); `_pid_trong_job` 977;
  `_cay_da_chet` 1125; `lenh_run`: đợi 2994, quyết xoá prompt 3041
  (`log_cay_chet if _nen_do_cay_truoc_bam() else (_thanh_vien_nhom(p.pid) == [])`), mốc `ket_thuc` nền khác 3049.
- `launcher_test.py`: `_R387_CHI_LINUX` 14714, **9** chỗ `return _R387_CHI_LINUX` (khớp "9 ca r387 bỏ qua trên Windows"
  trong hồ sơ land A); ca `r387_a_nen_khac_giu_moc_ket_thuc_base` 14977 MÔ PHỎNG nền khác trên Linux; bảng đột biến r387
  15072–15101 gồm `r387_a_nen_khac_van_do`, `r387_a_nen_khac_ngu_thua`, `r387_a_nen_khac_doi_moc`,
  `r387_a_nen_khac_moc_truoc_unlink` neo vào `_nen_do_cay_truoc_bam` và khối mốc 3049 — B mở nền phải xử lý cả bốn
  (không chỉ hai như §9 ghi).
- `.github/workflows/`: **không có runner macOS nào** (chỉ `ubuntu-latest`, `windows-latest`; `runner_set` không có macOS).

**Câu hỏi CHẶN cho chủ kho (chưa gọi Codex vì câu trả lời đổi phạm vi đặc tả):**
- **Q-D (Darwin).** Môi trường không có máy macOS và CI không có runner macOS, nên nhánh Darwin của M1 (`ps` +
  `timeout=han_giay`) KHÔNG đo native được ở đâu cả; chỉ thử được bằng stub `m.platform`/`m.subprocess` trên Linux.
  Lựa chọn: (1) **bỏ Darwin khỏi B** — B chỉ mở Windows; `_nen_do_cay_truoc_bam` thêm Windows; Darwin giữ `False`
  ngay như A và ghi nợ có tên `wp387-darwin-chua-do` *(khuyến nghị: chỉ đưa vào mã thứ đo được; khớp nguyên tắc
  kho "có MẶT khác có ĐO")*; (2) giữ Darwin với chỉ phép thử stub, khai rõ "chưa đo native" (rủi ro: mã chạy thật trên
  macOS lần đầu là ở máy người dùng); (3) thêm runner `macos-latest` vào CI cho đúng các ca r387 (ngoài write set ⇒
  packet riêng sửa `.github/workflows/ci.yml`, đi trước B).
- **Q-W (phạm vi khi Darwin bị bỏ).** Nếu chọn (1): tên packet đổi thành `LAUNCHER-BAM-LOG-NEN-WINDOWS` (revision 1
  mới), và bốn đột biến `r387_a_nen_khac_*` của A vẫn phải giữ ý nghĩa cho Darwin (nền khác còn lại) — tức B không gỡ
  mà đổi neo. *(Khuyến nghị: đồng ý đổi tên; giữ các đột biến nền-khác, neo lại theo `platform.system() not in
  ("Linux", "Windows")`.)*
