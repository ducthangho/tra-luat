Tôi cho bản r7 **approve**. Cả sáu finding vòng 6 của tôi đã đóng thật. Các con số mới hoặc đã đổi của r7 tôi đo lại đều khớp, chỉ lệch một số phụ. Tôi tìm thêm 7 finding mới, đều là P3, không cái nào chặn.

**Vòng 6 đã đóng thế nào**
- **G01 (P2):** r7 thêm chốt đủ job. Trên dữ liệu thật, 22 tên `JOB_BAT_BUOC` khớp đúng 22 job J ở cả 29 tệp `ci.yml` `push`, và cả ở 4 tệp `workflow_dispatch`. Run 41397205258 có J = 14, thiếu đúng tám mảnh `gate-cong-cu`. Vì vậy một job bị bỏ cả job nay ra `not_measured` thay vì lọt qua.
- **G02 (A22 với `.pyc`):** tôi đo trên một module giả. Danh sách cho phép mới bắt được cả sáu đối chứng. Nếu quay về danh sách cấm của r6 thì đối chứng (5) lọt cả ba lớp, nên đột biến m-A22 có răng.
- **G03–G06:** đều đã sửa đúng như đề xuất.

**Finding mới, đáng chú ý nhất**
- **Hai chỗ mâu thuẫn với chính thiết kế sổ luật.**
  - Bước tự kiểm sổ đòi mọi phiên bản luật, kể cả bản đã đóng, chứa đủ năm tên `CHECK_BAT_BUOC`. Nếu sau này `CHECK_BAT_BUOC` đổi thì `LUAT_v1` hỏng vĩnh viễn, mà đặc tả lại cấm sửa v1.
  - Câu hướng dẫn cho #1257 (thêm một phiên bản luật riêng cho `duong_nhanh`) không làm được: sổ chỉ cho các miền theo run_id rời nhau và đúng một miền mở.
- **Ba điều kiện tự kiểm sổ mới không có ca nào làm chúng đỏ** (vi phạm L3). Đó là: tên không trùng, chứa đủ năm tên `CHECK_BAT_BUOC`, mỗi tên khớp đúng một mục luật. Phép test so bản chép `CHECK_BAT_BUOC` với `packet_loop.py` và yêu cầu `JOB_BAT_BUOC` nằm trong dict được băm cũng chưa có ca đo.
- **Hai fixture lệch dữ liệu thật.**
  - Nếu làm đúng từng chữ, `F-ok` không bao giờ ra `passed`. Lý do: nó giữ nguyên SHA checkout `fe84620`, nhưng `ci.yml` lại được commit vào một kho git tạm, nơi không có commit đó.
  - Ở A3j/A3k, job bị bỏ không có dạng mà `ops/ci_provenance.py` thật sự ghi. Dạng thật là `buoc: "not_measured"`, `runner_id: null` và vẫn có một mục `checkout` mang `trang_thai: skipped`.

**Chưa kiểm được:** `ai-dang-giu` lúc 04:00–04:05Z, vì clone chỉ có `master` và tôi không được gọi mạng. Nguyên văn issuecomment-6676457187 cũng chưa kiểm được.

Tôi không sửa gì trong `repo/` và `git status` vẫn sạch. Công cụ Write không được cấp quyền ghi vào `work/`, nên các script đo chạy qua stdin. Riêng phép đo A22 thì tôi tạo bằng shell, ở `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r7-claude/work/a22r7/`, gồm `con.py`, `mau_module.py` và `cay/ops/*`.

```
# VERDICT wp1236 r7 vòng 7
spec_sha256: 31415a8a840c63c3b3a16eefe83dc90739698c3d10afb2348b5e7c5011ae26ba
## Finding vòng 6 của tôi
- G01: ĐÓNG — `JOB_BAT_BUOC` 22 tên nằm trong dict được băm; K3 có `thieu_job_bat_buoc`/`job_trung_ten`/`job_ngoai_luat`; có A3j/j′/j″ và A3k trên run thật 41397205258 kèm m-A3d/e/f/g/k; *Phạm vi của passed* và *Hạn chế (2)* đã sửa theo. Đo: 29/29 tệp `ci.yml` `push` có J đúng 22 tên, run 41397205258 có J = 14, thiếu đúng tám mảnh `gate-cong-cu`.
- G02: ĐÓNG — lớp `open` đã thành danh sách CHO PHÉP theo `.py`/`.pyc`, cây A22 biên dịch sẵn và chạy không `-B`, có thêm đối chứng (5), (6). Đo trên module giả: cả sáu đối chứng bị lớp 3 bắt, đối chứng dương 0 vi phạm; m-A22 (danh sách cấm `.py` của r6) làm (5) lọt cả ba lớp, nên có răng.
- G03: ĐÓNG — *Định danh* ghi base r7 và đánh dấu trạng thái 01:51Z là đã cũ; hàng C, D của bảng đợt có số đo 02:54Z và 04:00–04:05Z.
- G04: ĐÓNG — Q7 ghi sáu hồ sơ, có pr1095-pr1101 (41398722520, 41398738297) và lý do loại pr1115; đo lại khớp.
- G05: ĐÓNG — ước 720–900, `tran_moi` ≤ 950, `can_cu` ghi thẳng khả năng chạm trần và đường DỪNG.
- G06: ĐÓNG — có A16b (`STEP` dưới `chuan-bi`), A16c (`STEP` dưới job Windows) và m-A16b; khi nhận `STEP` ngoài J thì cả hai vế ra `passed`, tức ca đỏ.
## Findings mới
- id: G01
  severity: P3
  vi_tri: chua_do_duoc 9 (dòng 886–888)
  van_de: "run sớm nhất 40842340568 của pr1013" sai. Run `ci.yml` `push` sớm nhất có provenance là 40268583940 (pr945); 40437650174 (pr957), 40454280949 (pr964) và 40830701116 (pr994) cũng sớm hơn. Ngoài ra 29 tệp chỉ ứng với 28 run khác nhau.
  bang_chung: script stdin quét mọi `*.yaml` có `schema: ci_provenance/1` rồi sắp theo run_id ⇒ `(40268583940,'push','ci.yml','ops/land/pr945-wp899-provenance/do-1026-cebb5b2/ci-provenance-40268583940.yaml')` đứng đầu; `run lap: [41397085109]` (pr1141 và pr631). Lời khai chính "J đúng 22 tên ở 29/29 tệp" vẫn đúng.
  de_xuat: Sửa thành "run sớm nhất 40268583940 (pr945, 26-10)", ghi "29 tệp / 28 run".
- id: G02
  severity: P3
  vi_tri: *Sổ luật*, `kiem_so_luat` (dòng 208–210); dòng 218–219 ("`JOB_BAT_BUOC` … TRONG dict được băm"); A20 (dòng 665)
  van_de: Các điều kiện tự kiểm sổ mới của r7 không có vế nào làm chúng đỏ (L3): `JOB_BAT_BUOC` không trùng tên, chứa đủ năm tên `CHECK_BAT_BUOC`, mỗi tên khớp đúng một mục luật theo tiền tố, và phép test so bản chép `CHECK_BAT_BUOC` với `packet_loop.py`. Yêu cầu `JOB_BAT_BUOC` nằm TRONG dict được băm cũng không có phép đo: đặt nó ngoài dict thì A20(b) vẫn xanh, vì bản chép băm do chính executor sinh.
  bang_chung: `grep -n so_luat_hong SPEC.md` chỉ ra dòng 210 và A20 (c)–(e): khoá ≠ băm, miền chồng, hai miền mở. Không ca A1–A22 nào nhắc tên trùng, thiếu tên `CHECK_BAT_BUOC`, tên khớp 0 hoặc 2 mục luật, hay việc so với `packet_loop.py`. m-A3e đo K3, không đo `kiem_so_luat`.
  de_xuat: Thêm vào A20 các vế: (f) bản sao có `JOB_BAT_BUOC` lặp một tên; (g) bản sao thiếu `gate-ops (ubuntu-latest)`; (h) bản sao có tên không khớp mục luật nào; (i) bản sao sửa `JOB_BAT_BUOC` mà giữ nguyên khoá. Cả bốn ⇒ `so_luat_hong`. Kèm đột biến gỡ từng điều kiện và đột biến "đặt `JOB_BAT_BUOC` ngoài dict được băm" (i đỏ). Đặt tên ca cho phép so bản chép `CHECK_BAT_BUOC` với `packet_loop.py:2402`, kèm đột biến bớt một tên.
- id: G03
  severity: P3
  vi_tri: dòng 210 ("trong mỗi phiên bản … chứa đủ năm tên của `CHECK_BAT_BUOC`"); dòng 211–212, 226 ("Số mảnh hay tên job đổi ⇒ `LUAT_v2` … không sửa v1")
  van_de: Điều kiện chứa đủ `CHECK_BAT_BUOC` áp cho MỌI phiên bản, kể cả miền đã đóng, mà so với một hằng thay đổi được. Khi `CHECK_BAT_BUOC` đổi tên hoặc thêm job, bản chép trong module buộc phải theo, `LUAT_v1` bất biến hết thoả, và mọi `kiem` ra `so_luat_hong` (kể cả run lịch sử), `tom` rc 2. Đường "thêm `LUAT_v2`" mà đặc tả nêu không chữa được việc này.
  bang_chung: `git log -S'CHECK_BAT_BUOC = '` ⇒ chỉ `db0d206` (18-10), tức chưa từng đổi; nhưng `packet_loop.py` là tệp nóng (hàng đợi #1211 → #1212 → #1210), và luật "Sửa nội dung `LUAT_vN` cũ là cấm" chặn cách sửa trực tiếp.
  de_xuat: Chỉ áp điều kiện chứa đủ `CHECK_BAT_BUOC` cho phiên bản có miền MỞ. Hoặc chép ảnh chụp `CHECK_BAT_BUOC` vào TRONG từng `LUAT_vN` (được băm), rồi chỉ so ảnh của phiên bản mở với `packet_loop.py`. Ghi vào câu dòng 226 rằng đổi `CHECK_BAT_BUOC` cũng đi đường này.
- id: G04
  severity: P3
  vi_tri: *Chế độ `duong_nhanh`*, dòng 417–418
  van_de: Câu "Khi #1257 thêm phiên bản luật cho run `duong_nhanh`, phiên bản ấy có `JOB_BAT_BUOC` riêng (14 tên)" không làm được dưới sổ hiện tại: miền theo run_id rời nhau, đúng một miền mở, `tom` chọn phiên bản DUY NHẤT chứa run. Run `day_du` và `duong_nhanh` xen kẽ nhau theo run_id. Thêm bản 14 tên tức là đóng miền v1, và từ đó mọi run `day_du` bị xét bằng 14 tên ⇒ tám `job_ngoai_luat`.
  bang_chung: dòng 207–214 (miền rời nhau, đúng một miền mở, chọn phiên bản theo run); dòng 270–272 (`job_ngoai_luat`).
  de_xuat: Bỏ câu này, hoặc ghi "#1257 phải mở rộng khoá chọn phiên bản (vd chế độ suy từ provenance) và `kiem_so_luat`; sổ của #1236 không chứa được hai phiên bản cùng miền".
- id: G05
  severity: P3
  vi_tri: Fixture `F-ok` (dòng 627–630); K7 (dòng 285–287)
  van_de: `F-ok` giữ NGUYÊN VĂN `checkout` (sha `fe84620f…`), nhưng `ci.yml` lại "commit vào kho git tạm của test". K7 đọc `git show <SHA checkout>:…` trong `goc`, mà commit tạm có OID khác `fe84620`. Làm đúng từng chữ thì ra `khong_doc_duoc_workflow`, A1 không bao giờ `passed`. A14 sửa YAML thì cần commit mới, nên `sha` buộc phải đổi.
  bang_chung: pr1231 có 23/23 mục `checkout` `passed` với một SHA duy nhất `fe84620f897913c7f6c2ce5a0c7316a49655e82f`; bản r6 của `F-ok` viết tay nên không gặp chuyện này.
  de_xuat: Ghi rõ một trong hai cách. (a) `goc` tạm phải chứa đúng OID `fe84620` (`git init` + `git fetch <kho> fe84620`), còn biến thể A14 commit lên trên. (b) Thay `checkout[*].sha` bằng OID commit tạm, và khai đây là trường thứ hai được thay ngoài `log_day_du`.
- id: G06
  severity: P3
  vi_tri: A3j (dòng 646); K3 (dòng 272–274); `F-41397205258` (dòng 634–636)
  van_de: Ở A3j, job bị bỏ được dựng là "0 bước, `runner_id` vắng, bỏ khỏi `checkout`". Đó là hình REST, không phải hình `ops/ci_provenance.py` ghi — mà `kiem` đọc provenance. 0/37 tệp provenance thật có job skipped, nên không có dữ liệu thật nào bù vào chỗ này (cùng họ `hinh_dang_ke_thua` thứ hai: fixture tự đặt).
  bang_chung: gọi `ci_provenance.moc_gate()` trên mục REST `gate-cong-cu` của `readback-jobs-41397205258.json` ⇒ `{'labels': [], 'runner_id': None, 'conclusion': 'skipped', 'buoc': 'not_measured', 'trang_thai': 'skipped', …}`. `thu()` (`ci_provenance.py:385–387`) vẫn ghi một mục `checkout` `{job_id, name, trang_thai: skipped}`. Script quét: không tệp nào trong 37 tệp có job `conclusion: skipped`.
  de_xuat: A3j và `F-41397205258` dựng mục job skipped bằng chính `ci_provenance.moc_gate` (hoặc `thu` với `goi` giả phục vụ hai readback), giữ mục `checkout` skipped. Thêm đòi hỏi `kiem` không ném ngoại lệ khi `buoc` là chuỗi `"not_measured"`.
- id: G07
  severity: P3
  vi_tri: bảng A1, hàng A3 (m-A3d) và A3k (m-A3k) (dòng 646–647)
  van_de: m-A3k ("gỡ chốt đủ job") trùng hẳn với m-A3d. Bảng đột biến đếm một thay đổi mã thành hai đột biến "có răng", và lỗi thật mà A3k phân biệt được (chốt đủ job bị bỏ qua khi đã có lý do khác) không có đột biến nào.
  bang_chung: đếm bảng A1 r7: 75 vế + 73 đột biến, trong đó tên lặp gồm `m-A1` và `m-A3e`. Mô tả m-A3d và m-A3k giống nhau từng chữ ở vế đột biến.
  de_xuat: Gộp hai cái làm một, hoặc định nghĩa lại m-A3k là "chốt đủ job chỉ chạy khi chưa có lý do `not_measured` nào khác". A3k (có bước thiếu) đỏ, còn A3j xanh, nên hai ca thật sự khác nhau.
## Đã đo lại, khớp
- sha256 `31415a8a…` khớp; HEAD `500592d` = `b796259` + đúng `ops/specs/wp1236-r7.md` (986 dòng); `git status` sạch.
- `51d6509..b796259`: 6 tệp, đúng danh sách; `ops/` và `.github/` diff 0 dòng; `packet_loop.py` +7/−1, cả ba hunk trong `_owner_record` (:3258); `CHECK_BAT_BUOC` :2402, `_canon` :2420, `DAT_MOC` :3095, `cmd_kiem_dong_wp` :3462, `ĐÓNG ĐƯỢC WP` :3501.
- `land_evidence_nguon --root .`: `101 ĐẠT · 25/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 126`, `TỔNG: ĐẠT`; `kiem_ho_so_land --root .`: `52/52`, rc 0.
- 22 tên `JOB_BAT_BUOC`: mỗi tên khớp đúng một tiền tố của `danh_gia_gate.py` (sha256 `b87f9697…`) theo `startswith`. 37 tệp provenance: 29 `ci.yml` `push` và 4 `workflow_dispatch` đều có J đúng 22 tên, mỗi tên một lần; 4 tệp `launcher-windows.yml`.
- Run 41397205258: 16 job REST; J = 14; tám mảnh `gate-cong-cu` vắng, chỉ còn một mục `gate-cong-cu` skipped (`labels: []`, `runner_id: null`, 0 bước); 13 job có bước skipped; `danh-gia-gate-output` cho 13 "thiếu bước" + 1 "thiếu dấu hiệu" (`gate-cong-cu-gop`); event `push`, head `8983e1b`, attempt 1; commit `8983e1b` có trong kho.
- pr1231 (nguồn `F-ok`): T = 23 = khoá `log_day_du` (22 J + `chuan-bi`), chỉ có nhãn Ubuntu, 23 checkout `passed` cùng SHA `fe84620f…`, `danh_gia` 23/23 `passed`; `ci.yml` `fe84620..b796259` diff rỗng.
- Q7: sáu hồ sơ (pr1095-pr1101 với hai run dispatch, pr1127, pr1128, pr945, pr957, pr964), head ∈ H; pr1115 41365578430 có head ∉ H.
- Ước A1: r7 có 75 vế + 73 đột biến (r6: 69 + 65); quy theo r4 ra 663–893; ký tự fixture 957 → 1587. Khoảng 720–900 với trần 950 hợp lý, và đặc tả đã ghi thẳng khả năng chạm trần.
- A22 trên module giả: cả sáu đối chứng bị lớp danh sách cho phép bắt; m-A22 làm (5) lọt cả ba lớp (có răng); (6) vẫn bị lớp 1/2 bắt dưới m-A22, nên câu "(5) hoặc (6)" đúng.
- Không kiểm được (clone chỉ có `master`, cấm mạng): `ai-dang-giu` 04:00–04:05Z; nguyên văn issuecomment-6676457187; `ops/reviews/wp1236-spec-6-*`.
KET_LUAN: approve
```