Kết luận vòng 5: **changes_requested**. Sáu finding P0–P2 vòng 4 của tôi đóng năm. Riêng G02 (land chỉ-hồ-sơ không có đường `passed`) vẫn mở: biến thể `duong_nhanh` đã được thêm nhưng chạy trên run đường nhanh thật vẫn không qua được. Mọi con số mới của r5 đo lại đều khớp. Có 3 lỗ P2 mới, đều do r5 đưa vào:

- **Job `gate-cong-cu-gop` phá biến thể `duong_nhanh`.** Job này nằm trong J của run đường nhanh thật 41397205258 (hồ sơ pr1055) nhưng không có bước liệt kê bước bỏ qua. Bước gom của nó đổi chế độ qua biến `CONG_CU_TEST_GOP_CHE_DO`, không qua `if:`, nên in `GOM: KHÔNG ĐO — …` thay cho dấu hiệu của `day_du`.
- **Bước đọc `che_do` của `chuan-bi` có `continue-on-error: true`.** Theo đúng chữ của K7, `chan_k7` chặn bước này, mà r5 lại bắt buộc mọi run có bước ấy. Vậy cả ca A1 dương cũng không bao giờ xanh.
- **Khối `nang_tran` còn neo vào `spec_hash r4`.** Phần `can_cu` vẫn ước 520–700 dòng, trong khi trần mới là 900.

Kho không bị sửa, `git status` sạch. Ba thư mục `__pycache__` dưới `scripts/` sinh lúc 01:53, khi hook mở phiên, trước mọi lệnh đo của tôi; chúng nằm trong `.gitignore` và tôi để nguyên. Script đo nằm ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r5b-claude/work/`: `dem_r5.py`, `nhanh_yaml.py`, `nhanh_r5.py`, `k13_r5.py`, `a22_do.py`, kèm bản chép các script vòng 4.

# VERDICT wp1236 r5 vòng 5
spec_sha256: 9e1ffa3e94c716b77626ce254ce463c0cdfcd5c1c62b2eb3071a8ce2f7603f34
## Finding vòng 4 của tôi
- G01: ĐÓNG — *Phạm vi land* thêm điều kiện `moc.run.event == "push"`. Câu pr1127/pr1128 đã sửa (dòng 367–369), Q7 đã sửa (767–769). Có A21e/m-A21c và B14/m-B14. Ý phụ "lane WORKER không phải tên thay thế" chưa ghi, nhưng từ nay nó chỉ còn chạm lời khai phụ.
- G02: CÒN MỞ — biến thể `duong_nhanh` đã thêm theo quyết định chủ kho, nhưng đặt lên run `duong_nhanh` thật thì vẫn không có đường `passed` (xem G01 mới).
- G03: ĐÓNG — đã có `ENV_JOB_CHO_PHEP` nằm trong dict được băm, A14f dùng `CONG_CU_TEST_BAN_KINH`, có A14f′, và đặc tả ghi thẳng rằng giá trị env không được kiểm.
- G04: ĐÓNG — K1 cấm `pull_request` và đòi `trang_thai`/`repo`; K3 đòi checkout `passed` cho từng job J; có A3i, A8b/c.
- G05: ĐÓNG — có mục *API xuất* với chữ ký từng hàm; `OS_BAT_BUOC`, `KHONG_PHAI_GATE`, `ENV_JOB_CHO_PHEP` nằm trong dict được băm. Còn một chỗ hở nhỏ của API, xem G07.
- G06: ĐÓNG — (a) bỏ cột số; (b) chua_do_duoc 6 chuyển "ĐÃ ĐO"; (c) đổi thành "bộ tách HẸP thứ hai"; (d) có *Ranh giới tin cậy* và câu "§10.2.3"; (e) A15 thêm vị từ pipefail và phép chọn SHA checkout.
## Findings mới
- id: G01
  severity: P2
  vi_tri: Thiết kế mục 1, biến thể `duong_nhanh` (dòng 193–208); A23 (dòng 614); B15 (dòng 660); chua_do_duoc 8 (dòng 803–805); `hinh_dang_ke_thua` (dòng 734–741)
  van_de: Trên run `duong_nhanh` thật, job `gate-cong-cu-gop (ubuntu-latest)` nằm trong J nhưng không có bước `DUONG_NHANH - liet ke buoc bo qua (job …)`, nên vế "MỌI job trong J" không thoả được. Bước `G5 gom manh ban kinh dot bien (#668)` của nó không có `if:` theo `che_do`, nên luật "giữ nguyên dấu hiệu của `day_du`" đòi dòng `SỐ LIỆU GOM: … lỗi đột biến=0`. Nhưng bước này đổi chế độ qua env `CONG_CU_TEST_GOP_CHE_DO` và in `GOM: KHÔNG ĐO — PR chỉ đổi hồ sơ (…=duong_nhanh, 0 mảnh); …`. Kết quả: A23(a) và B15 không thể xanh trên `F-nhanh` chép từ run thật, và land chỉ-hồ-sơ vẫn không có đường `passed`. Dữ liệu offline để phát hiện việc này có sẵn trong kho từ lúc soạn. Đây là lần thứ 3 của hình dạng thứ hai trong `hinh_dang_ke_thua`: luật dựng từ việc đọc YAML thay vì từ dữ liệu thật.
  bang_chung: `python -I -B ../work/nhanh_r5.py` chạy trên `ops/land/pr1055-wp1052-provenance/readback-jobs-41397205258.json` và `ci.yml`@8983e1b (so với HEAD chỉ khác +8/−1, ở bước lease của gate-ops). Kết quả: `J = 14`; 13/14 job có bước liệt kê `success`, `chan_k7=[]`; riêng `gate-cong-cu-gop (ubuntu-latest) … liet_ke_REST=None liet_ke_YAML=0`; bước gom có `if=None`, env `['CONG_CU_TEST_GOP_CHE_DO']`. `ops/cong_cu_test.py:8228` in dòng `GOM: KHÔNG ĐO — PR chỉ đổi hồ sơ (…`. `danh-gia-gate-output-41397205258.txt` đã ghi cho job này: `-> not_measured: buoc [ops/cong_cu_test.py --gop] thieu dau hieu duong /^SỐ LIỆU GOM…/`.
  de_xuat: Thêm cho `gate-cong-cu-gop` một mục riêng trong biến thể `duong_nhanh`: bước gom với dấu hiệu `DONG` là dòng `GOM: KHÔNG ĐO — … (CONG_CU_TEST_GOP_CHE_DO=duong_nhanh, 0 mảnh) …`, chốt đuôi theo log REST (gộp vào chua_do_duoc 8), và miễn job này khỏi đòi hỏi về bước liệt kê. Sửa luật "bước không có `if:` theo `che_do`": trừ những bước đọc `che_do` qua env (`CONG_CU_TEST_GOP_CHE_DO`, `CI_DUONG_NHANH_CHE_DO`), mỗi bước phải được xét riêng. Thêm một ca offline kiểu A15 trên REST jobs của 41397205258 và `ci.yml`@8983e1b, đòi: mỗi job J có mục trong biến thể; mỗi bước luật có đúng một `buoc` `success` và đúng một bước YAML; `chan_k7` không chặn. Nâng bộ đếm hình dạng thứ hai lên 3.
- id: G02
  severity: P2
  vi_tri: Thiết kế mục 1 (dòng 194–196); K7 (dòng 259–271); `F-ok` (dòng 577–581); A23 (dòng 614); chua_do_duoc 4 (dòng 796–797)
  van_de: r5 bắt MỌI run có `STEP` của bước `phan loai diff (duong nhanh ho so)` trong `chuan-bi` để biết chế độ. K7 viết cho "Mỗi `STEP`", không giới hạn ở J, và `chan_k7` chặn mọi bước có `continue-on-error` khác `false`. Bước này lại cố ý khai `continue-on-error: true` (lùi về `day_du` khi phân loại hỏng). `F-ok` chép YAML nguyên văn, nên đọc đúng chữ thì A1 dương và A23(a) đều ra `not_measured` ở mọi run. Nếu hiểu K7 chỉ áp cho J, thì dòng `che_do` là một dòng `BUOC` gõ tay được và không đối chiếu được với provenance. Ngoài ra m-A23a "cờ trong tệp thay vì log `chuan-bi`" không xác định: `kiem` chạy offline, không có log, còn định dạng `gate_output/2` không có trường `che_do` nào.
  bang_chung: `nhanh_r5.py` ⇒ `chuan-bi YAML buoc phan loai: continue-on-error = True ; chan_k7 = ['coe']`. HEAD cho kết quả giống hệt (`nhanh_yaml.py`: `coe=true`). `k13_r5.py`: bước này `success` ở 18/33 tệp provenance `ci.yml`.
  de_xuat: Cách nên chọn: suy chế độ từ PROVENANCE. `duong_nhanh` ⇔ trong `buoc` của mọi job J, các bước `DUONG_NHANH - …` đều `success`; `day_du` ⇔ chúng `skipped`; trộn lẫn ⇒ `not_measured`. Khi ấy không cần dòng `BUOC` của `chuan-bi` nữa, và m-A23a có nghĩa rõ: "chọn theo dòng BUOC thay vì theo `buoc`". Nếu giữ thiết kế hiện tại thì ghi rõ: K7 chỉ áp cho `STEP` của job J; `STEP` của `chuan-bi` chỉ cần khớp `buoc` `success` và miễn `chan_k7`; nêu lý do miễn và mức tin của dòng `che_do`.
- id: G03
  severity: P2
  vi_tri: *kich_thuoc*, khối `nang_tran` (dòng 521–532)
  van_de: Khối `nang_tran` của r5 vẫn ghi `ai_nang: … hiệu lực khi duyệt spec_hash r4`. Bản r4 đã bị thay và sẽ không được duyệt, nên đọc đúng chữ thì trần 900 không bao giờ có hiệu lực. `can_cu` vẫn ghi "Ước 520–700" (căn cứ cho trần 750 của r4), trong khi bảng ghi 640–840 và `tran_moi` là 900. Đây là đúng ca "con số trôi chống đỡ một câu về THẨM QUYỀN" mà soan-spec L5 đòi chữa ngay.
  bang_chung: `grep -n "spec_hash r\|520–700\|900" SPEC.md` ⇒ dòng 523 (`spec_hash r4`), 526 (`Ước 520–700`), 530 (`≤ 900`). `SPEC_R4.md` dòng 431 và 434 giống hệt từng chữ.
  de_xuat: Sửa thành "hiệu lực khi duyệt spec_hash của bản đặc tả này (r5 hoặc bản thống nhất)". Cập nhật `can_cu` thành 640–840 kèm phần tăng (biến thể `duong_nhanh`, `mien_gate_output`, A19h–n, A21e, A22, A23). Giữ nguyên câu dự phòng "tách sang đợt A3".
- id: G04
  severity: P3
  vi_tri: Biến thể `duong_nhanh`, vế "mỗi dòng `echo` … là một dấu hiệu `DONG` nguyên văn" (dòng 202–203)
  van_de: Dòng `echo` trong YAML không phải thứ được in ra, vì còn lệnh `echo` và dấu nháy. Đem nó làm regex `DONG` nguyên văn thì không biên dịch được (`**`, ngoặc mở không đóng như `(packet`). Các dấu hiệu này cũng đến từ YAML tại SHA checkout, không nằm trong phần băm `luat_sha256`, mà đặc tả không nói điều đó.
  bang_chung: Chạy trên `ci.yml`@HEAD: 49 dòng echo; `re.compile(đối số sau shlex)` lỗi 49/49.
  de_xuat: Ghi rõ: dấu hiệu là đối số `echo` sau khi bỏ nháy kiểu shell, so khớp nguyên dòng theo nghĩa đen (hoặc `re.escape`), lấy từ YAML tại SHA checkout. Chỉ nhận thân bước gồm toàn dòng `echo "<…>"`; thân khác ⇒ `not_measured`.
- id: G05
  severity: P3
  vi_tri: Thiết kế mục 1, `LUAT_v1` miền `(1, None)`; *Đường sửa cho hồ sơ cũ* (dòng 395–396); `tom` (dòng 188–189)
  van_de: Các run trước wp1113 (01-11-2026) không có dòng `che_do=`, vì bước phân loại khi ấy tên `… - chi pull_request` và bị `skipped` trên push. Dưới r5 các run này luôn ra `khong_xac_dinh_che_do`. Vậy câu "chạy `tom` nếu log còn hạn (`tom` chọn đúng phiên bản luật của run)" chết với những run ấy, dù log tháng 10 vẫn còn trong hạn lưu.
  bang_chung: `k13_r5.py`: 15/33 tệp provenance `ci.yml` có `('phan loai diff (duong nhanh ho so - chi pull_request)', 'skipped')`, gồm pr1080, pr1097, pr1100, pr1115, pr1127, pr945, pr957, pr964 …; commit đổi tên bước là `0be08f8` (01-11).
  de_xuat: Cách suy chế độ theo provenance ở G02 tự xử ca này: bước `DUONG_NHANH - …` `skipped` ⇒ `day_du`. Nếu không làm thế thì ghi thẳng hệ quả ở *Đường sửa*.
- id: G06
  severity: P3
  vi_tri: A22 (dòng 623–629)
  van_de: Bọc `SourceFileLoader.exec_module` cộng `spec_from_file_location` cộng quét `__file__` vẫn để lọt hai cách thực thi nguồn mà không qua loader: `runpy.run_path` và `exec(compile(open(p).read(), …))`.
  bang_chung: `python -I -B ../work/a22_do.py`. `import` và `spec_from_file_location`: wrapper ghi `True`. `runpy.run_path` và `exec(compile(open()))`: `wrapper_ghi=False sys.modules___file__=False`. Audit hook `open` ghi `True` ở cả bốn cách.
  de_xuat: Thêm `sys.addaudithook` ghi sự kiện `open` có đường dẫn resolve bằng hai tệp cấm. Thêm đối chứng thứ ba (`runpy.run_path`) phải làm A22 đỏ.
- id: G07
  severity: P3
  vi_tri: *API xuất của module* (dòng 281–287); L-7 (dòng 380); D2b(a) (dòng 381)
  van_de: API không xuất hàm tính H. L-7 phải tự tính H để ra `khong_co_head_land` (B12), vì hồ sơ không có lời khai nào thì danh sách trả về rỗng, nên quy tắc `merge_commit` ∪ `prs[*].merge_commit` sẽ có hai bản cài đặt. D2b(a) đòi `run`/`attempt` của tệp, mà API không có hàm phân tích header.
  bang_chung: Đọc mục 6 so với L-7 và B12; danh sách bốn hàm không có H và không có hàm phân tích header.
  de_xuat: Xuất `tap_head_land(cay_yaml) -> set[str]`. Ghi rõ: D2b đọc `run`/`attempt` từ provenance (`moc.run.run_id`, `attempt_yeu_cau`), vì khi `kiem` ra `passed` thì hai giá trị ấy đã bằng giá trị của tệp.
- id: G08
  severity: P3
  vi_tri: Q7 (dòng 771–772); `chua_do_duoc` (dòng 788–809)
  van_de: Q7 vẫn ghi "30 tệp push = 26 `ci.yml` + 4 `launcher-windows.yml`" (số trên `3163f4d`) mà không có thời điểm đo (L5). Trên base hiện tại là 33 = 29 + 4, cộng 4 tệp `workflow_dispatch`. Thứ tự đánh số `chua_do_duoc` là 1–6, 8, 9, 7.
  bang_chung: `k13_r5.py` ⇒ `tep 37 ho so 31`; 33 push + 4 `workflow_dispatch`; trong đó `ci.yml` có 29 push + 4 dispatch.
  de_xuat: Ghi số kèm SHA và giờ đo (hoặc ghi rõ "trên `3163f4d`"); đánh lại số thứ tự.
## Đã đo lại, khớp
- sha256 `9e1ffa3e…` trùng với `repo/ops/specs/wp1236-r5.md`. HEAD `142bc6f` = `51d6509` + đặc tả. `4f03566..51d6509` chỉ đổi 4 tệp đã nêu. `3163f4d..4f03566`: 23 commit; diff trên ba cổng, test của chúng, `ci_provenance`, `ci_duong_nhanh`, `ci.yml`, `ci_dang_ky_test` đều rỗng; thêm 3 hồ sơ (pr1229, pr1230, pr1242).
- `land_evidence_nguon --root .`: `101 ĐẠT · 25/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 126`, rc 0. `kiem_ho_so_land --root .`: `52/52`, rc 0 (52 DAT, 74 BO_QUA).
- Bảng *Đo lại trên `4f03566`* (`dem_r5.py`): 126 hồ sơ; 31/37; 121; 67 = 47·1·3·1·9·6; 49; L8 hồi tố 39 (thêm đúng pr1229, pr1230, pr1242); L5 25/3; 52/17; L-7 hồi tố 52 (0 tệp `gate-output2-*`).
- `ENV_JOB_CHO_PHEP`: mọi job khác `chuan-bi` trong `ci.yml`@HEAD có env đúng `{PYTHONDONTWRITEBYTECODE, PYTHONIOENCODING, PYTHONUTF8}`; không có `env`/`defaults` mức workflow; `ci.yml` giống hệt giữa `fe84620` và HEAD; 0 chỗ nhắc `GITHUB_ENV`/`GITHUB_PATH`.
- Tên các bước `duong_nhanh` trong đặc tả khớp `ci.yml` (bước `kiem re` của gate-ops, `ci-duong-nhanh selftest`, dòng echo `GOM: KHONG DO — duong_nhanh, 0 manh (khong manh nao chay)`, bước liệt kê ở 7 job). Dòng in `kiem-re` ở `ops/ci_duong_nhanh.py:766` giống hệt giữa `4f03566` và HEAD; `che_do=` in ở dòng 785.
- `ci.yml` dòng 500–501 (lane LAND, `github.ref == 'refs/heads/master' && … != 'duong_nhanh'`) giống hệt ở `3163f4d`, `4f03566`, HEAD. `on.push.branches: [master]` (push chỉ có trên master).
- K1: 37/37 tệp provenance có `trang_thai: passed` và `repo` đúng kho; 33 push, 4 `workflow_dispatch`, 0 `pull_request`. K3: 33 tệp `ci.yml`, J = 22, đúng một SHA checkout, 0 job J thiếu checkout `passed`.
- `CHECK_BAT_BUOC` ở `packet_loop.py:2402`; `_canon` ở :2420; `kiem-dong-wp` in `ĐÓNG ĐƯỢC WP` ở :3495 ⇒ vế dương D8(a) dựng được, và m-D8a (chỉ chép module) rơi vào rc 8 qua `Path(__file__).with_name`.
- Regex `mien_gate_output`: ngày sai lịch và chữ số Unicode bị phép đọc ngày loại; `os=,,` không chứa `ubuntu-latest` nên bị loại. Đủ cho A19j–l.
- Không kiểm được (không có trong clone, không gọi mạng): `ai-dang-giu` và các lease `wp1240-r1-g1-claude`, `#1254`; nguyên văn issuecomment-6674366256 (chỉ có bản tóm tắt `QUYET_DINH_CHU_KHO.md`, khớp đủ 6 mục với *Phản biện*); `ops/reviews/wp1236-spec-4-*`; log REST của run `duong_nhanh` cho chua_do_duoc 8.
KET_LUAN: changes_requested