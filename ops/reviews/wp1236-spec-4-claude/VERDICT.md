Tôi đã review xong vòng 4. Kết luận: **changes_requested**. Cả 8 finding vòng 3 của tôi đã đóng thật. Mô hình `chan_k7` dựng đúng như đặc tả chạy được trên dữ liệu thật: 22/22 job ở F-that, 26/26 run push `ci.yml`. Nhưng r4 có 2 lỗ P2 mới, cùng nằm ở *Phạm vi land*.

- **Run `workflow_dispatch` của `ci.yml` tại merge SHA bị xếp là lời khai land, mà không bao giờ `passed` được.** Bước `release-verify strict (lane LAND)` chỉ chạy trên ref `master`. Đặc tả lại ghi pr1127/pr1128 là `launcher-windows.yml`, và lấy chính run #1127 làm ví dụ ở Q7.
- **Land của packet chỉ chạm hồ sơ hoặc đặc tả không có đường `passed` nào.** Từ wp1113, push master của loại merge này chạy chế độ đường nhanh (`duong_nhanh`) nên bỏ qua các bước luật. Đường vòng đang dùng là dispatch trên nhánh phụ, và đường ấy lại vướng đúng lỗ thứ nhất. Đặc tả không nhắc chế độ này lần nào.

Còn 4 lỗ P3. Kho không bị sửa: hai thư mục `__pycache__` do lệnh đo của tôi sinh ra đã được xoá, `git status` sạch. Script đo nằm ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r4-claude/work/` (`k7_r4.py`, `k7_r4_tat_ca.py`, `land_r4.py`, `land_r4b.py`, `dang_tep.py`, `dang_tep_ten.py`).

# VERDICT wp1236 r4 vòng 4
spec_sha256: c8e79de93545c6003e36162f03465213c4d97566a32156faf7a1ba69042b519b
## Finding vòng 3 của tôi
- H01: ĐÓNG — dựng `chan_k7` đúng mục K7 (`work/k7_r4.py`): 22/22 job J của F-that không bị chặn, 26/26 run push `ci.yml` qua phần bước REST + YAML; đột biến m-A15b (gọi `chan_buoc` nguyên trạng) ra đúng 19 job bị chặn. Phần còn hở (env mức job, A14f) ghi ở G03.
- H02: ĐÓNG — H = `merge_commit` gốc ∪ `prs[*].merge_commit`. Đo: 118/123 hồ sơ có `merge_commit` gốc, cộng pr1042-pr1068 (3 head) và pr1095-pr1101 (2 head). pr721/pr732 để `merge_commit` dạng mapping dưới `trang_thai_packet` nên H rỗng và vào miễn trừ. Có B10, B12, A21d.
- H03: ĐÓNG — `tom` chọn phiên bản DUY NHẤT có miền chứa run; các miền rời nhau; `kiem_so_luat`; có T6 và A20d/e.
- H04: ĐÓNG — D2b(b) đòi `gate_output_mien {chuoi, readback}`; có D6 và D9. API dùng chung với module chưa ghi ở A1, xem G05.
- H05: ĐÓNG — (a) có `tach_buoc`; (b) bỏ số `STEP`; (c) đọc workflow tại SHA checkout (hệ quả với run PR ở G04); (d) `shell: bash` tính là có pipefail, có A14i; (e) nạp qua `Path(__file__).with_name`, có D7b.
- H06: ĐÓNG — A22 đo bằng `sys.modules`, thay m-B9; `kiem_so_luat` chạy đầu `kiem`/`tom`; có A20c.
- H07: ĐÓNG — ba hàng nay cùng một cách đếm; chua_do_duoc 3 đã chuyển sang "đã đo"; có tên thay thế cho `tl selftest`; có mẫu neo. Câu mô tả đơn vị vẫn lệch với cách đếm, xem G06(a).
- H08: ĐÓNG — tên tệp bắt buộc `gate-output2-<run>-a<n>.txt`, chỉ phân giải trong `<hồ sơ>-provenance/`, có A18l.
## Findings mới
- id: G01
  severity: P2
  vi_tri: *Phạm vi land* (dòng 276–282); Q7 (dòng 662–668); B8/B9 (dòng 551–552); A21 (dòng 517)
  van_de: Run `workflow_dispatch` của `ci.yml` trên nhánh phụ tại merge SHA được xếp là lời khai land, nhưng không bao giờ `passed` được vì bước `release-verify strict (lane LAND …)` chỉ chạy khi `github.ref == 'refs/heads/master'`. Vì "MỌI lời khai land phải hợp lệ", chỉ cần ghi trung thực một run như vậy (kể cả `not_measured`, kể cả bên cạnh một lời khai push hợp lệ) là L-7 TRUOT. Tác giả vì thế có lý do đổi tên khoá để giấu run. Thêm nữa, đặc tả ghi pr1127/pr1128 là `launcher-windows.yml`, và Q7 lấy chính run #1127 làm ví dụ "phần Ubuntu vẫn passed".
  bang_chung:
    · Provenance pr1127 (run 41356691133) và pr1128 (run 41361081437): `event: workflow_dispatch`, workflow `ci.yml`, head bằng `merge_commit` (f2102fc, c165a5d), 37 job. Ở `gate (ubuntu-latest)`, lane LAND `skipped`, lane WORKER `success`. Run push pr1231 thì ngược lại. `ci.yml`@3163f4d dòng 500–501: `if: ${{ github.ref == 'refs/heads/master' && … }}`.
    · `work/k7_r4_tat_ca.py`: 26/26 run push `ci.yml` qua; 4/4 run `workflow_dispatch` `ci.yml` trượt đúng job `gate (ubuntu-latest)` với lý do `rest0 release-verify … ['skipped']`.
    · `work/land_r4.py` (áp *Neo* + *Phạm vi land* của r4 lên 123 hồ sơ): có 17 lời khai land kèm provenance, gồm 13 run push và 4 run `workflow_dispatch` (pr1127, pr1128, pr1095-pr1101 ×2). Với pr1127 và pr1128, đó là lời khai land DUY NHẤT của hồ sơ.
    · Provenance `launcher-windows.yml` chỉ có ở pr945, pr957, pr964 (cộng pr1115-provenance, giữ run của c7174bf là merge của pr1130). Hồ sơ pr1127/pr1128 không nhắc `launcher-windows` lần nào.
    · pr1095-pr1101 (dòng 65, 67, 78): push master bị huỷ do concurrency, nên tác giả chạy "ci.yml workflow_dispatch trên nhánh claude/gate-hau-merge-… — ĐÚNG merge SHA". Đây là cách đang dùng ở hồ sơ ngày 04-11.
  de_xuat: Thêm vào định nghĩa lời khai land điều kiện `moc.run.event == "push"`; run không có provenance vẫn coi là land (fail-closed). Run khác cùng head thì là lời khai phụ, được phép `not_measured`. Nếu giữ định nghĩa cũ thì phải nêu thẳng hệ quả này. Sửa ngoặc ở dòng 279 (pr1127/pr1128 là `ci.yml` dispatch hai nền; `launcher-windows` là pr945/pr957/pr964) và sửa ví dụ ở Q7. Ghi rõ lane WORKER KHÔNG phải tên thay thế của bước `release-verify` trong `LUAT_v1`. Thêm ca B14 "push hợp lệ + dispatch nhánh phụ cùng head ghi `not_measured`" với kết quả đã chọn, kèm đột biến.
- id: G02
  severity: P2
  vi_tri: *Phạm vi land* (dòng 272–282); K6 (dòng 195–196); Q1 (dòng 641–642); Q8 (dòng 671–673); *Đường sửa* (dòng 304–305)
  van_de: Từ wp1113, push master của một diff chỉ nằm trong `ops/{land,leases,reviews,specs}/**` chạy `che_do=duong_nhanh`. Mọi bước luật nặng mang `if: … != 'duong_nhanh'` nên bị bỏ, và K6 không bao giờ đạt. Đường vòng hiện hành (dispatch trên nhánh phụ) cũng không đạt, xem G01. Vậy hồ sơ landed của packet chỉ-đặc-tả hay ghi-sổ chỉ còn hai cách: `owner_waived` cho TỪNG head, hoặc hạ `landed: false`. Đặc tả không nhắc `duong_nhanh` lần nào, nên chủ kho duyệt Q1/Q8 mà không biết hệ quả này.
  bang_chung:
    · `grep -n -i "duong_nhanh|đường nhanh" SPEC.md` ⇒ 0 dòng. `ci.yml`@3163f4d: 50 chỗ `che_do != 'duong_nhanh'`; dòng 71 ghi "wp1113: cả ba sự kiện … đều được phân loại"; `ops/ci_duong_nhanh.py:115` là `ALLOWLIST_TIEN_TO`.
    · Run thật: hồ sơ pr1055 (dòng 130–134) ghi run 41397205258, push master tại 8983e1b, `che_do=duong_nhanh`, 14/15 job in "DUONG_NHANH: bo qua".
    · Trong 49 hồ sơ landed, 2 hồ sơ (4 head) có merge diff nằm trọn trong allowlist: pr1042-pr1068 (3 head, mỗi head chỉ thêm một tệp `ops/specs/…`) và pr1118 (50 tệp dưới `ops/land`). Hai hồ sơ này merge trước wp1113 nên push còn chạy đủ bước; cùng loại merge hôm nay sẽ chạy `duong_nhanh`.
  de_xuat: Nêu hệ quả ở *Phạm vi land* và Q8 (hoặc thêm Q11). Đưa chủ kho chọn một trong hai: (a) land chỉ-hồ-sơ dùng `owner_waived` cho từng head; (b) thêm một biến thể luật cho chế độ `duong_nhanh`, chọn theo `che_do` của `chuan-bi`, đòi dấu hiệu của các bước `kiem-re`. Thêm một ca B cho hồ sơ landed có run push chạy `duong_nhanh`.
- id: G03
  severity: P3
  vi_tri: K7 `chan_k7` (dòng 203–207); A14(f) (dòng 509)
  van_de: `_env_chan` chỉ chặn `env:` không phải dict hoặc có khoá `CI_DANG_KY_*`. Cả 22 job J đều đã có `env:` mức job (`PYTHONIOENCODING`, `PYTHONUTF8`, `PYTHONDONTWRITEBYTECODE`), nên A14(f) "env ở mức job ⇒ not_measured" chỉ đỏ được với khoá `CI_DANG_KY_*` hoặc env không phải dict. Tập khoá cho phép theo bước cũng bị lách khi đưa khoá chế độ lên mức job/workflow. Và chỉ khoá được kiểm, giá trị thì không.
  bang_chung: Chạy `work/k7_r4.py` trên bản sao YAML: thêm `CONG_CU_TEST_BAN_KINH: nho` vào env job gate-registry ⇒ 22/22 job qua; thêm `CI_DANG_KY_WORKERS` vào env job ⇒ bị chặn (`env_job_wf`); đặt `env: {NHANH_DON_DUOC_DICH: 0/8}` ở mức workflow ⇒ 22/22 qua; thêm `CI_DANG_KY_LA` vào env của bước registry ⇒ bị chặn (`env_buoc`).
  de_xuat: A14(f) ghi rõ fixture: khoá `CI_DANG_KY_*` hoặc env không phải dict. Nên cân nhắc thêm: env mức job/workflow phải thuộc một tập cố định kèm giá trị; giá trị hằng của env bước nằm trong luật; regex `MẢNH`/`MANH` buộc số mảnh khớp chỉ số ma trận trong tên job.
- id: G04
  severity: P3
  vi_tri: K1 (dòng 185); K7 "Workflow tại SHA checkout" (dòng 199–202)
  van_de: Ba chỗ hở quanh checkout và neo run.
    (a) Run `pull_request` có SHA checkout là merge tổng hợp, mà clone thường không chứa. `ci_provenance` chỉ ghi checkout `passed` khi object ấy có mặt lúc chụp. Vậy cùng một hồ sơ, L8 xanh ở máy đã chụp provenance và đỏ `khong_doc_duoc_workflow` trên CI.
    (b) Không đòi checkout `passed` cho từng job trong J.
    (c) K1 không đòi `moc.run.trang_thai == passed` và `repo` đúng kho.
  bang_chung: `ci_provenance.py:271–289` (`moc_checkout`, lý do `khong_co_object_de_doi_chieu_parents`); `git for-each-ref refs/pull` trong clone ⇒ 0. Hiện 0/34 provenance là `pull_request`, nên chưa có ca thật. 15 checkout không `passed` đều là `chuan-bi`. 34/34 tệp có `moc.run.trang_thai: passed` và `repo: ducthangho/tra-luat`.
  de_xuat: Chốt một luật không phụ thuộc clone: event `pull_request` ⇒ `not_measured` `su_kien_ngoai_pham_vi`, hoặc ghi rõ hệ quả. K3 đòi checkout `passed` với đúng SHA cho mọi job J. K1 đòi thêm `moc.run.trang_thai == passed` và `repo`.
- id: G05
  severity: P3
  vi_tri: A1-M1 (dòng 451–454); mục 1 (dòng 150–151); D2b (dòng 290)
  van_de: A1-M1 không ghi chữ ký và giá trị trả của `kiem_ho_so_gate_output`, cũng không có hàm kiểm `owner_waived` nhận đường dẫn readback tường minh như D2b(b) cần (L8/L-7 thì tìm readback theo mẫu tên trong `<hồ sơ>-provenance/`). Đợt B/C/D không được sửa module, nên executor hoặc phải viết bộ kiểm thứ hai, hoặc DỪNG. Ngoài ra A1-M1 liệt kê `KHONG_PHAI_GATE` tách khỏi `LUAT_v1` và không nhắc `OS_BAT_BUOC`, trong khi mục 1 đặt cả hai TRONG `LUAT_v1`. Nếu chúng nằm ngoài phần băm thì sửa chúng không đổi `luat_sha256`, và A20(b) không bắt được.
  bang_chung: Đọc A1-M1 so với mục 1 và D2b(b); write set của đợt D chỉ có `packet_loop.py` và test của nó.
  de_xuat: A1-M1 liệt kê các hàm xuất kèm chữ ký, vd `kiem_waiver(chuoi, head, readback_path, url_hop_le)` và `kiem_ho_so_gate_output(...) -> [{duong_dan, token, neo, la_land, hop_le, ly_do}]`. Ghi rõ `OS_BAT_BUOC` và `KHONG_PHAI_GATE` nằm trong dict được băm, và `KHONG_PHAI_GATE` khớp nguyên văn tên job.
- id: G06
  severity: P3
  vi_tri: Bảng ba dạng (dòng 98–106); chua_do_duoc 6 (dòng 696–698); *Trích tệp* (dòng 236–237); `owner_waived` (dòng 245–246); Q10 (dòng 680–681); A15 (dòng 511) so với `hinh_dang_ke_thua` (dòng 637)
  van_de: Năm chỗ chữ hoặc số lệch.
    (a) Đặc tả ghi đơn vị là "tệp được trích tên chứa `gate-output`/`kiem-gate`", nhưng 6/4 · 4/4 · 13/11 là số của cách đếm mọi tệp `.txt` mà token trỏ tới.
    (b) chua_do_duoc 6 đã đo được ngay.
    (c) Câu "Không có bộ tách thứ hai" không đúng: regex trích tệp chính là một bộ tách thứ hai, dù hẹp.
    (d) "Readback chứng minh comment CÓ THẬT": đọc offline thì nó chỉ chứng minh có một tệp trong kho nói như vậy, cùng mức tin với provenance. §10.2.3 còn đòi context/OS, phạm vi/hạn và điều kiện thay thế, mà r4 không kiểm.
    (e) `hinh_dang_ke_thua` nói "MỌI vị từ của K7 phải có ca chạy trên F-that", nhưng A15 không liệt kê `ong_khong_pipefail` và phép chọn SHA checkout duy nhất.
  bang_chung: `work/dang_tep.py` (mọi `.txt`) ⇒ 6/4, 4/4, 13/11; `work/dang_tep_ten.py` (lọc theo tên) ⇒ 6/5, 4/4, 12/11 (pr1231 rời hàng `tu_do`). `git diff --stat fe84620 3163f4d -- .github/workflows/ci.yml` ⇒ rỗng, nên tập khoá env giữa hai SHA y hệt. `work/k7_r4.py` với phép thử pipefail đúng nghĩa đen ⇒ 0 bước bị cờ trên F-that.
  de_xuat: Sửa câu đơn vị cho khớp cách đếm. Chuyển chua_do_duoc 6 sang "đã đo". Viết lại: "readback là hiện vật do phiên chép, cùng mức tin với provenance". Thông điệp của waiver ghi "điều kiện cần cho §10.2.3". Thêm hai vị từ còn thiếu vào A15.
## Đã đo lại, khớp
- sha256 `c8e79de9…` bằng `repo/ops/specs/wp1236-r4.md`. HEAD `aebc69c` = `3163f4d` + đặc tả. Chuỗi r1–r3 khớp: `b9766fe` → `d599ff33`, `4672b15` → `570b1085`, `0340658` → `e4166c02`.
- `CHECK_BAT_BUOC` ở `packet_loop.py:2402` là năm job `ci.yml` trên `ubuntu-latest`.
- Provenance: 34 tệp / 28 hồ sơ; 753 job `not_measured` + 1 `failed`. Có 30 tệp push = 26 `ci.yml` (23 job) + 4 `launcher-windows.yml` (2 job); ngoài ra 4 tệp `workflow_dispatch` `ci.yml` (37 job).
- J = 22 ở run 42032872356 (pr1231); SHA checkout duy nhất là `fe84620`.
- `chan_k7`: 22/22 job không bị chặn; m-A15b ⇒ 19 job bị chặn; thêm khoá env ngoài tập cho phép ⇒ bị chặn.
- `ci.yml` ở `fe84620` giống hệt `3163f4d`.
- `merge_commit` gốc 118/123. `prs` có 3 head (pr1042-pr1068) và 2 head (pr1095-pr1101). H rỗng ở pr721, pr732. pr838 dùng khoá `pr` và không landed.
- L-6: 49 DAT, 74 BO_QUA. L-7 hồi tố: 32 hồ sơ có lời khai, 17 hồ sơ không có.
- Bảng ba dạng: 6/4, 4/4, 13/11 theo `dang_tep.py`.
- `land_evidence_nguon`: 98 · 25/28 · 0 · 0 · 123, rc 0. `kiem_ho_so_land`: 49/49, rc 0.
- Nếp readback: 17 tệp `readback-*issuecomment-*.json`. Tệp của pr1130 có đủ `html_url`, `user.login`, `author_association: OWNER`, `body`.
- Không kiểm được (không có trong clone): nhánh `ops/wp1240-r1-g1-lease` (N1/N2), `ops/specs/wp1237-r1.md`, VERDICT và script vòng 3 dưới `ops/reviews/wp1236-spec-3-*` (không có trên master, cũng không có trong `0340658`), con số 755 nhánh.
KET_LUAN: changes_requested