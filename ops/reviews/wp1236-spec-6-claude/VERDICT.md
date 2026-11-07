Kết luận vòng 6: **changes_requested**. Còn một finding P2, nằm ở cách thi hành việc cắt `duong_nhanh`; việc cắt thì tôi không bàn lại. Cả ba P2 vòng 5 của tôi (G01–G03) đã đóng, các P3 vòng 5 cũng đóng. Các con số đổi trong r6 tôi đo lại đều khớp. Có thêm 5 P3 mới.

- **P2 mới (G01):** r6 khẳng định "run `duong_nhanh` thì `kiem` trả `not_measured`", nhưng không ca nào đo điều đó. A23(d) của r5 là ca duy nhất kiểm việc này và đã bị bỏ theo, không có ca thay.
  - Điều khẳng định ấy đúng trên run thật 41397205258, nhưng chỉ nhờ bước bị bỏ trong từng job: 13 job thiếu bước, `gate-cong-cu-gop` thiếu dấu hiệu.
  - `kiem` không đòi run có đủ job. `F-ok` chỉ có 3 job trong J mà vẫn phải ra `passed`.
  - Vậy job nào bị bỏ cả job bằng `if:` mức job thì lọt qua (fail-open). `gate-cong-cu` ở đường nhanh đang bị bỏ đúng kiểu này.
- **P3 mới:**
  - Audit hook của A22 bị lọt khi đã có `.pyc`: tôi đo trên một module giả.
  - Hàng C của bảng đợt và dòng 20, 25–26 còn chữ cũ.
  - Danh sách Windows ở Q7 thiếu pr1095-pr1101.
  - Ước A1 quy theo số ca ra cận trên khoảng 795–810 dòng, nên trần 800 gần như không còn dư.
  - Câu "`STEP` dưới job ngoài J là dòng lạ" chưa có vế nào làm nó đỏ.

Tôi không sửa gì trong kho, `git status` sạch. Các thư mục `__pycache__` do hook mở phiên sinh ra, nằm trong `.gitignore`. Script đo nằm ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r6-claude/work/`: `q7_r6.py`, `win_head.py`, `a22b_do.py`, `dem_ca2.py`, cùng bản chép script vòng 5. Tôi định lưu bản VERDICT vào thư mục đó nhưng lệnh ghi tệp không được cấp quyền, nên VERDICT chỉ có ở dưới đây.

# VERDICT wp1236 r6 vòng 6
spec_sha256: b945aec0f5ab15be3b35a37a623a86446a5676ac17ee45a7bc4efc6492caa3b3
## Finding vòng 5 của tôi
- G01: ĐÓNG — biến thể `duong_nhanh` đã cắt khỏi phạm vi theo quyết định chủ kho; `F-nhanh`, A23, B15 và `chua_do_duoc` 8 cũ đã bỏ; grep chỉ còn tham chiếu ở mục cắt phạm vi, lịch sử, *Phản biện* và `ngoai_pham_vi`. Hệ quả của việc cắt xem G01 mới.
- G02: ĐÓNG — r6 không đọc `che_do`; K6 ghi rõ K6/K7 chỉ áp cho J, nên `continue-on-error` của `chuan-bi` không còn chặn.
- G03: ĐÓNG — `nang_tran` neo vào băm của chính tệp chứa khối; `can_cu` ghi 580–760; `tran_moi` ≤ 800. Độ dư của trần xem G05 mới.
- G04 (P3): ĐÓNG — hết đối tượng.
- G05 (P3): ĐÓNG — hết đối tượng.
- G06 (P3): ĐÓNG — đã thêm audit hook `open` và hai đối chứng (3), (4). Còn một lỗ khi có `.pyc`, xem G02 mới.
- G07 (P3): ĐÓNG — đã xuất `tap_head_land` và `la_run_land`; D2b đọc run/attempt từ provenance (`attempt_yeu_cau` là int và bằng `moc.run.run_attempt` ở 37/37 tệp).
- G08 (P3): ĐÓNG — Q7 ghi số trên cả hai base, kèm ngày; `chua_do_duoc` đánh số 1–8 liên tục. Danh sách hồ sơ thiếu một mục, xem G04 mới.
## Findings mới
- id: G01
  severity: P2
  vi_tri: *Chế độ `duong_nhanh`* (dòng 376–377); K3/K6 (dòng 239–251); *Phạm vi của passed* (dòng 291–293); *Hạn chế (2)* (dòng 295); `F-ok`/A1 dương (dòng 590–594, 602)
  van_de: Sau khi cắt, đặc tả khẳng định "run `duong_nhanh` ⇒ `kiem` trả `not_measured`" nhưng không ca nào đo điều đó (A23(d) của r5, ca duy nhất đánh giá log đường nhanh bằng luật `day_du`, đã bị bỏ mà không có ca thay thế); và `kiem` không đòi đủ job (K3 lấy J từ chính run, không có chiều luật→job), nên một job bị bỏ CẢ JOB bằng `if:` mức job (đúng cách `ci.yml` đang bỏ `gate-cong-cu` ở đường nhanh) là FAIL-OPEN, trái câu "lệch luật/output lộ ra ở lượt `tom` kế tiếp".
  bang_chung: `ci.yml`@HEAD: `gate-cong-cu if=${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}`. `readback-jobs-41397205258.json`: `gate-cong-cu` chỉ còn 1 mục `skipped` (8 mảnh không có trong T), J = 14; 13 job thiếu bước (có bước `skipped`); `gate-cong-cu-gop` 10/10 bước `success`, chỉ hỏng vì dấu hiệu (`danh-gia-gate-output-41397205258.txt`: `thieu dau hieu`). Như vậy lý do thật là "thiếu bước" ×13 và "thiếu dấu hiệu" ×1, không có `khong_co_luat` nào như dòng 377 ghi. `F-ok` có J = 3 (`gate-packet-loop`, `gate-registry`, `gate`) trên 8 tiền tố luật Ubuntu mà A1 vẫn đòi `passed`, tức theo thiết kế một run thiếu job vẫn qua. `grep "mỗi mục\|thiếu job\|đủ job"` không tìm thấy chốt đủ job nào.
  de_xuat: (a) Thêm một ca offline trên dữ liệu thật, thay A23(d): dựng provenance từ `readback-jobs-41397205258.json` và `ci.yml`@`8983e1b` (đều có trong kho), cùng một tệp `gate_output/2` viết tay có `STEP`/`BUOC` cho mọi bước luật mà REST ghi `success`. Đòi `kiem` ⇒ `not_measured`, lý do theo từng job. Đột biến "K6 bỏ qua bước luật vắng" phải làm ca đỏ. (b) Chọn một trong hai. Hoặc thêm `JOB_BAT_BUOC` vào dict được băm (tối thiểu năm tên của `CHECK_BAT_BUOC`), mỗi tên đúng một job trong J, thiếu ⇒ `not_measured` `thieu_job_bat_buoc`; `F-ok` thêm `gate-cong-cu-gop` và `gate-ops`; thêm ca A3j và đột biến gỡ chốt. Hoặc ghi thẳng vào *Phạm vi của passed* "KHÔNG phủ đủ job: job bị bỏ cả job không làm `kiem` đỏ", sửa câu *Hạn chế (2)*, và đưa thành câu hỏi cho chủ kho. Lý do: packet `duong_nhanh` riêng rất có thể đổi `ci.yml` sang bỏ cả job, trong khi `LUAT_v1` vẫn ở miền mở.
- id: G02
  severity: P3
  vi_tri: A22, lớp thứ ba (dòng 638–641)
  van_de: Audit hook so ĐÚNG đường dẫn `.py`. Khi đã có `.pyc`, `import` chỉ mở `.pyc`, nên câu "audit hook `open` bắt được cả bốn" chỉ đúng khi không có `.pyc`. `runpy.run_path(<.pyc của tệp cấm>)` lọt cả ba lớp. Đây là danh sách CẤM theo cách viết đường dẫn.
  bang_chung: `python -I work/a22b_do.py` trên module giả `dich.py` có `__pycache__/dich.cpython-313.pyc`: `import dich (co pyc)  wrapper=True __file__=True audit_open_dung_duong_dan=False`; `runpy.run_path(pyc)  wrapper=False __file__=False audit_open_dung_duong_dan=False audit_thay_pyc=True`. Vòng 5 tôi đo bằng `-B`, không có `.pyc`, nên không thấy ca này.
  de_xuat: Đảo thành danh sách CHO PHÉP (bài học CLAUDE.md): mọi đường dẫn mã nguồn hoặc bytecode dưới gốc kho được mở hay thực thi phải thuộc {`ops/gate_output_doi_chieu.py`, `ops/ci_provenance.py`} (kể cả `.pyc` của chúng). Nếu giữ danh sách cấm thì khớp theo stem ở cả `.py` lẫn `__pycache__/<stem>.*.pyc`, và sửa câu "cả bốn" thành "khi không có `.pyc`".
- id: G03
  severity: P3
  vi_tri: *Định danh* dòng 20 và 25–26; bảng *Đợt*, hàng C (dòng 501); *Phản biện* r5→r6, hàng cuối (dòng 914)
  van_de: Dòng 20 vẫn ghi "Base của r5 cho review". Dòng 25–26 vẫn ghi lease #1240 "VẪN `CÒN_HẠN` … phải thu hồi nó", và hàng C vẫn ghi `CÒN_HẠN` rc 11, trong khi dòng 78–79 đo 02:54Z ra `NGƯỜI_GIỮ 0` ("đã nhả"). Hàng D đã cập nhật, hàng C thì không, dù *Phản biện* ghi là đã sửa "bảng đợt".
  bang_chung: đọc SPEC.md dòng 20, 25–26, 78–80, 501–502, 914.
  de_xuat: Hàng C thêm "02:54Z: `NGƯỜI_GIỮ 0`"; dòng 20 đổi thành r6; đánh dấu dòng 25–26 là trạng thái 01:51Z, đã bị dòng 78–79 thay.
- id: G04
  severity: P3
  vi_tri: Q7 (dòng 790–791)
  van_de: Danh sách "Run có Windows cùng `merge_commit` có ở pr1127, pr1128, pr945, pr957, pr964" thiếu pr1095-pr1101.
  bang_chung: `python -I -B ../work/win_head.py`: pr1095-pr1101 có hai run `ci.yml` `workflow_dispatch` (41398722520, 41398738297), mỗi run có 14 job `windows-latest`, `head_in_H=True`. Tổng 6 hồ sơ. Run `launcher-windows.yml` của pr1115 (41365578430) có `head_in_H=False`, nên loại đúng.
  de_xuat: Thêm pr1095-pr1101 vào danh sách.
- id: G05
  severity: P3
  vi_tri: *kich_thuoc* hàng A1 (dòng 524); `nang_tran.tran_moi` (dòng 543)
  van_de: Ước A1 giảm nhanh hơn phạm vi. Quy theo số ca thì cận trên ≈ 795–810 dòng, tức trần 800 gần như không còn dư (chứ không phải dư 40).
  bang_chung: `python -I -B work/dem_ca2.py` (vế + đột biến của bảng A1): r4 61+55 = 116, ước 520–700; r5 73+69 = 142, ước 640–840; r6 69+65 = 134, ước 580–760. Mật độ dòng test trên mỗi (vế+đột biến): r4 3,62 · r5 3,52 · r6 3,36, thấp nhất trong ba bản. Quy theo phạm vi: từ r4 ra 601–809, từ r5 ra 604–793. A22 nay có ba lớp và bốn đối chứng chạy trong tiến trình con, nặng hơn một vế thường.
  de_xuat: Hoặc nâng `tran_moi` lên khoảng 850, hoặc ghi thẳng trong `can_cu` rằng chạm trần (đường DỪNG) là khả năng thật. Chủ kho chọn.
- id: G06
  severity: P3
  vi_tri: K6 (dòng 249–250); A16 (dòng 618)
  van_de: Câu mới "dòng `STEP` dưới job ngoài J là dòng lạ (K9)" không có vế nào làm nó đỏ. A16 chỉ thử một dòng ngoài định dạng chung chung.
  bang_chung: đọc bảng A1: không vế nào đặt `STEP` dưới `chuan-bi` hay dưới job `windows-latest`.
  de_xuat: Thêm vào A16 hai vế: `STEP` dưới `chuan-bi`, và `STEP` dưới job Windows ⇒ `not_measured`. Thêm đột biến "nhận `STEP` dưới job ngoài J".
## Đã đo lại, khớp
- sha256 `b945aec0…` khớp với `repo/ops/specs/wp1236-r6.md`. HEAD `0a8d89f` = `51d6509` + đúng một tệp (914 dòng). `git status` sạch: các thư mục `__pycache__` đều bị bỏ qua theo `.gitignore` và sinh lúc 03:01:43–49, do hook mở phiên, trước mọi lệnh đo.
- Q7 trên HEAD (`ops/land` giống `51d6509`): 37 tệp / 31 hồ sơ = 33 `push` (29 `ci.yml`, T = 23 job; 4 `launcher-windows.yml`, T = 2 job) + 4 `workflow_dispatch` `ci.yml` (T = 37: 23 Ubuntu, 14 Windows). Trên `3163f4d`: 34 = 30 `push` (26 + 4) + 4 dispatch. Khớp.
- `la_run_land` trên dữ liệu thật: 29 đúng / 8 sai. `moc.run.loi_khai_rest_path` và `event` có ở 37/37 tệp. K1/K3: 33 `push` + 4 dispatch, mọi tệp `trang_thai: passed`, `repo` đúng kho; `ci.yml` J = 22, đúng một SHA checkout, 0 job J thiếu checkout.
- `land_evidence_nguon --root .`: `101 ĐẠT · 25/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 126`, `TỔNG: ĐẠT`. `kiem_ho_so_land --root .`: `52/52`, rc 0.
- Số dòng trích dẫn: `CHECK_BAT_BUOC` :2402, `_canon` :2420, `DAT_MOC` :3095, `cmd_kiem_dong_wp` :3456, `ĐÓNG ĐƯỢC WP` :3495. `git diff 3163f4d 51d6509` trên `packet_loop.py`, `kiem_ho_so_land.py`, `ci_provenance.py`, `ci.yml`, `ci_duong_nhanh.py` rỗng.
- Tham chiếu sót: `grep duong_nhanh|che_do|F-nhanh|A23|B15` chỉ thấy ở mục cắt phạm vi, lịch sử, Q8, `ngoai_pham_vi` và *Phản biện*. `che_do_khong_xac_dinh` ở dòng 264 là lý do về chế độ SHELL của K7, không liên quan. Danh sách ca A1–A22 / B1–B14 / D1–D10 (có D7b) khớp các bảng.
- So r5 với r6, bảng A1: bớt 1 hàng (A23), 4 vế, 4 đột biến; phần fixture về đúng 957 ký tự như r4.
- D10 và m-D10 có răng trên giấy: K1 nhận `workflow_dispatch`, nên `kiem` qua và chỉ còn `la_run_land` phân biệt hai vế.
- Không kiểm được (clone không có nhánh khác, cấm gọi mạng): `ai-dang-giu` 02:53–02:54Z và trạng thái lease #1240, #1254 (trên master `ops/leases/` không có tệp của hai lease này); nguyên văn issuecomment-6675490171 (chỉ có `QUYET_DINH_CHU_KHO.md`, khớp các việc r6 làm); `ops/reviews/wp1236-spec-5-*`.
KET_LUAN: changes_requested