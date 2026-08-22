# ĐẶC TẢ ĐÓNG BĂNG — `CI-FASTPATH-THEO-DIFF`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `CI-FASTPATH-THEO-DIFF`
`packet_issue`: `CHUA_CO` — người giữ kho chưa mở. **Không bịa số.**

## `nguon_cap_viec`

**KHÔNG phải packet khắc phục.** Slice thứ hai của việc phát hiện ngày 2026-08-22 (xem
`ops/specs/CI-BANG-PHU-THUOC.md` §`nguon_cap_viec`). Toàn bộ **bằng chứng B1–B5** nằm ở đặc tả ấy;
tệp này **không chép lại** — chép là dựng hai bản sẽ trôi lệch.

**ĐIỀU KIỆN MỌC:** packet này chỉ được bắt đầu khi `CI-BANG-PHU-THUOC` **đã có hiện vật trên
`master`** — không phải khi PR của nó merged (revert được), không phải khi Issue đóng.
`ADR-0044` đòi slice sau mọc trên nhánh đã NHẬN slice trước, không mọc trên một PR chưa merge.

`review_class`: **`sensitive`** — sửa thẳng `ci.yml`, tức `docs/PROTOCOL_DA_PHIEN.md:571`
*"workflow/CI authority"*.

## Ba quyết định của người giữ kho — chốt in-session 2026-08-22

| # | quyết định | căn cứ |
|---|---|---|
| Q1 | **Fast-path ÁP CHO `master`, nhưng có ĐIỀU KIỆN DÂY CHUYỀN**: chỉ đi đường tắt khi lượt `gate` của commit `master` **CHA** đã `success` trên **CẢ HAI** nền. Không tra được ⇒ chạy hết. | Loại trừ `master` giữ được **16%** tổng phút; áp cho `master` giữ **40%**. Điều kiện dây chuyền cho phép lấy 40% mà cổng phát hành không lúc nào thiếu bằng chứng: nếu merge chỉ chạm nhóm ngoài cả tập đọc lẫn tập băm thì cây runtime **giống hệt** commit cha, nên lượt mới **kế thừa** bằng chứng còn hiệu lực thay vì dựng lại. |
| Q2 | **HAI nhóm luật**, không phải một. Nhóm 1: chỉ chạm `ops/**` ⇒ bỏ trọn 13 bước runtime. Nhóm 2: không chạm `scripts|SKILL.md|references|RELEASE_MANIFEST.json|VERSION` ⇒ bỏ 6 bước băm nhưng **VẪN chạy** `tl selftest` và `doc-claims-check`. | Nhóm 1 phủ 54% số lần land; thêm nhóm 2 lên **80%**. Đúng 25% ấy là loại PR gây phiền nhất (sửa `docs/`/`CLAUDE.md`). |
| Q3 | Ca canh bảng chạy khi **chạm `ci.yml` hoặc tệp bảng**, CỘNG một **lượt định kỳ hàng tuần** trên `master`. | Chạy mọi PR thì tự phản (cộng 3–5 phút vào đúng thứ đang đi cắt). Chỉ chạy khi chạm `ci.yml` thì hở: ai thêm một `open()` mới trong `scripts/` làm bảng lệch mà không đụng `ci.yml`. Lượt định kỳ bịt lỗ ấy — *"cổng chỉ chạy khi có người bấm là cổng không có ai canh"*. |

## `write_set`

- `.github/workflows/ci.yml`
- `.github/checks/ci_phamvi.py` — thêm hàm quyết định (bảng đã có từ slice trước)
- `.github/checks/ci_phamvi_test.py` — thêm phản chứng cho hàm quyết định

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| **`paths:` mức workflow hoặc mức job** | CẤM, ba lý do đã trả giá: ⑴ kho đo được workflow có `paths:` **không chạy** ở lần đẩy tạo nhánh mới (nguyên nhân chưa biết — `CLAUDE.md`); ⑵ check **bắt buộc** bị `paths:` bỏ qua sẽ ở lại `pending` và **chặn merge vĩnh viễn**; ⑶ *"một job CI mặc định SKIP là một cổng KHÔNG TỒN TẠI"*. |
| bước `cgroup` (82s) | Bảo đảm cô lập, không phải kiểm nội dung. Chưa đo phụ thuộc. |
| `tl selftest` theo phạm vi | Packet riêng. |
| `launcher-windows.yml` | Cơ chế riêng, không trộn. |

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | Một bước duy nhất tính **tập tệp đã đổi** rồi xuất hai cờ `bo_nhom_runtime` / `bo_nhom_bam` ra `GITHUB_OUTPUT`. | `.github/workflows/ci.yml` |
| M2 | Hàm quyết định sống trong **Python có test**, không trong shell nhúng YAML. `ci.yml` chỉ gọi và đọc cờ. | `.github/checks/ci_phamvi.py` |
| M3 | **`if:` mức BƯỚC** cho 13 + 6 bước. Job LUÔN chạy và LUÔN trả `conclusion` ⇒ check bắt buộc không bao giờ treo. | `.github/workflows/ci.yml` |
| M4 | **Fail-close**: không xác định được tập tệp đã đổi (clone nông, thiếu base, lần đẩy đầu, `git` lỗi) ⇒ **chạy hết**. | `.github/checks/ci_phamvi.py` |
| M5 | Điều kiện dây chuyền cho `master` (Q1): tra `conclusion` của lượt `gate` trên commit CHA, cả hai nền. Không tra được ⇒ chạy hết. | `.github/checks/ci_phamvi.py` |
| M6 | Mỗi bước bị bỏ phải **IN RA** nó bỏ cái gì và **vì sao** (nhóm nào đã đổi / chưa đổi). Bỏ qua im lặng là bị cấm. | `.github/workflows/ci.yml` |
| M7 | Lượt canh bảng: `schedule:` hàng tuần trong chính `ci.yml`, và `if:` khi diff chạm `ci.yml` hoặc `ci_phamvi.py`. | `.github/workflows/ci.yml` |
| M8 | Phản chứng cho từng luật + đột biến giết đúng ca của nó. | `.github/checks/ci_phamvi_test.py` |

## `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Diff chỉ chạm `ops/**` ⇒ cả hai cờ bật | Đột biến: nới tập an toàn để chứa `scripts/` ⇒ ca `scripts_khong_duoc_bo` ĐỎ. Đây là hình dạng đã trả giá ở `v1.36.68` — **nới danh sách cho phép để chứa chính thứ đang tấn công**. |
| N2 | Diff chạm `docs/` ⇒ `bo_nhom_bam` bật, `bo_nhom_runtime` **TẮT** | Đột biến: gộp hai cờ làm một ⇒ ca `docs_van_phai_chay_selftest` ĐỎ. Chốt này neo thẳng vào B2: `tl selftest` đọc `docs/` **69 tệp**. |
| N3 | Fail-close có răng | Ca `khong_biet_diff_thi_chay_het`: base không tra được ⇒ cả hai cờ **TẮT**. Đột biến đổi mặc định thành "bật" ⇒ ĐỎ. **Đây là ca quan trọng nhất của packet**: hỏng nó là cổng fail-OPEN, tức xanh mà không đo gì. |
| N4 | Điều kiện dây chuyền `master` có răng | Ca `master_cha_do_thi_chay_het` và `master_cha_khong_tra_duoc_thi_chay_het`. Đột biến bỏ phép tra cha ⇒ cả hai ĐỎ. |
| N5 | Không bước nào bỏ im lặng | Ca `bo_buoc_phai_in_ly_do`: mọi bước bị bỏ phải in một dòng chứa tên nhóm. Đột biến xoá dòng in ⇒ ĐỎ. |
| N6 | KHÔNG có `paths:` ở mức workflow/job | Ca `ci_yml_khong_duoc_co_paths`: parse `ci.yml`, thấy khoá `paths` dưới `on:` hoặc dưới `jobs.*` ⇒ ĐỎ. Đột biến thêm `paths:` ⇒ ĐỎ. Chốt này biến ba bài học đã trả giá thành **máy canh**, không phải chữ trong `ngoai_pham_vi`. |
| N7 | Job vẫn trả `conclusion` khi đi đường tắt | **Hai phép đo, vì một mình phép nào cũng hở.** ⑴ Trên lượt CI THẬT của PR: `gate (ubuntu-latest)` phải `conclusion: success`, **0 bước hỏng**, và job KHÔNG được `skipped` — đo theo **JOB**, không theo `check_suite` (nợ `ops/NO_KY_THUAT.md` §17: 6 ca thông báo khai xanh sai, 2 trong đó trên head cuối). ⑵ Ca `ci_yml_khong_dat_if_o_muc_job`: parse `ci.yml`, thấy khoá `if:` ở mức `jobs.<ten>` (thay vì mức bước) ⇒ ĐỎ. Đột biến chuyển một `if:` từ bước lên job ⇒ ca ấy ĐỎ. Không có ⑵ thì ⑴ chỉ chứng minh MỘT lượt chạy đã đúng, không chặn được lượt sau đặt sai chỗ. |
| N8 | Cắt được đúng như khai | Đo lượt CI của chính PR này khi nó chạm `ci.yml` (⇒ nhóm D, chạy hết), rồi một lượt `workflow_dispatch` trên một ref chỉ chạm `ops/**`. Chênh lệch phải ≈ **184s ubuntu**. Không đo được chênh lệch ⇒ tiêu chí này **chưa đạt**, không được làm tròn thành đạt. |

## `hinh_dang_ke_thua`

Chép từ `CI-BANG-PHU-THUOC` §`hinh_dang_ke_thua`: hình dạng **"phép dò yếu cho kết quả an toàn
giả"** đã đếm **3**. Packet này thừa hưởng bộ đếm ấy — nếu phiên thi hành thấy mình đang chứng
minh "bỏ bước này an toàn" bằng bất cứ thứ gì **nhẹ hơn** tập-đọc/tập-băm của slice trước, đó là
lần thứ tư và phải dừng lại hỏi.

## `chua_do_duoc`

- **Chưa biết `github.event.before` có dùng được ở lần đẩy đầu của một nhánh mới không.** Đây là
  cùng vùng với hiện tượng *"workflow có `paths:` không chạy ở lần đẩy tạo nhánh mới"* mà kho đã
  đo được **triệu chứng** nhưng **chưa biết nguyên nhân**. M4 (fail-close) là chốt che cho chỗ này,
  nhưng phải có ca đo THẬT trên một nhánh mới, không suy từ tài liệu GitHub.
- **Cách tra `conclusion` của lượt cha (M5) chưa chọn.** Hai đường: `gh`/REST — nhưng phiên remote
  đo được **REST bị chặn ĐÚNG chỗ làm việc** (`/repos/...` trả 403 không header GitHub) — hoặc
  `actions/github-script`. Phải ĐO trong runner thật trước khi chốt; runner GitHub khác container
  remote và **không được suy từ nền này sang nền kia**.
- **Chưa đo tập đọc trên `windows-latest`** (kế thừa từ slice trước).
- **Ước lượng kích thước ±30%**: `ci.yml` +50, `ci_phamvi.py` +80, test +120 ⇒ ~250 dòng thêm.
  Neo từ tệp cùng loại: `bundle_fragment_check.py` = 224 dòng, `pre_push_test.py` = 431.
  Nếu chạm trần `ADR-0044` (≤300) thì **khai vượt trong PR**, không cắt phản chứng.
