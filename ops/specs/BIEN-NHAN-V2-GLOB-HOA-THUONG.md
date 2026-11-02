# Đặc tả packet — `BIEN-NHAN-V2-GLOB-HOA-THUONG` (revision 1)

- `packet_id`: **BIEN-NHAN-V2-GLOB-HOA-THUONG** · `packet_issue`: **CHƯA CÓ** — chủ kho mở Issue rồi điền số vào lease; đặc tả không
  tự cấp việc. Soạn 29-10-2026 bằng skill `soan-spec` (phiên `session_015GtxrZ1Tt93F4NLUUhKYQy`). Chủ kho chốt lúc ~09:22Z 29-10:
  Q8 (a) — chỉ còn mục cổng, xếp SAU #1017 và #1007; Q9 — chiều KHÔNG phân biệt hoa thường, khớp #1007; giữ điều kiện merge có P3
  và Windows local đã chốt ở vòng trước.
- `nguon_cap_viec`: khắc phục. Issue #1017 (`BIEN-NHAN-V2-TEST-WINDOWS`) ghi thẳng ở mục *Ngoài phạm vi*: "dòng 1442/1601 dùng
  `glob("*.receipt.yaml")`, cùng lớp lỗi phụ thuộc nền với #1006". Lớp lỗi đo được ở #1006/PR #1007 (`t27`: CI run `40812761896`,
  `gate-ops (windows-latest)`, `253/254`, ca đỏ `t27`).
- `review_class`: **sensitive** — `ops/bien_nhan_v2.py` là cổng review/land authority (`docs/PROTOCOL_DA_PHIEN.md` §8; §20 dòng
  `ADR-0050` trỏ tệp này). Cần `cross_approved` (Codex) hoặc `human_audited`.
- **Điều kiện bắt đầu:** #1017 và #1007 đã land, và `ai-dang-giu` trên CẢ HAI tệp của write set ra `NGƯỜI_GIỮ 0` sau khi đồng bộ đủ
  ref (so TẬP tên `ls-remote --heads` với `for-each-ref`, thiếu cục bộ = 0). Chưa đủ ⇒ chưa cấp lease.
- Base: nhánh mặc định SAU khi cả hai land. Đo nền lúc soạn: `735b181ef3a77b9a94938bebc9e0e392db332cdc` (09:23Z 29-10). Đo lại khi
  cấp lease; mọi cột "nền" dưới đây phải chạy lại trên base thật.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab

(Packet mới ⇒ đếm lời gọi Codex từ 0. Trần riêng của packet: **4** lời gọi (đơn vị: một lần chạy `launcher.py run … codex exec`,
kể cả lượt chết giữa chừng). Lời gọi thứ 4 vẫn chưa approve ⇒ Review Rescue Checkpoint, không gọi thêm.)

## Vấn đề (một đoạn)

`ops/bien_nhan_v2.py` chọn biên nhận bằng `Path.glob("*.receipt.yaml")` ở hai chỗ (dòng 1442 trong hàm kiểm chính, dòng 1601 trong
`_sinh_no`; số dòng đo trên `735b181`). `glob` khớp KHÔNG phân biệt hoa thường trên Windows và CÓ phân biệt trên POSIX, nên cùng một
cây, hai nền có thể đếm hai tập biên nhận: tệp `X.RECEIPT.YAML` bị cổng BỎ QUA LẶNG trên Linux và bị KIỂM trên Windows. Đo 09:24Z 29-10
trên `735b181`: `ops/reviews` có **304** tệp khớp đuôi chính xác và **304** khớp không phân biệt hoa thường (đơn vị: mục trong thư mục,
kể cả thư mục con mang đuôi ấy) ⇒ hôm nay chưa lệch; lệch xuất hiện ngay khi có một tệp đuôi hoa. #1007 đã chọn chiều KHÔNG phân biệt
hoa thường cho `t26`/`t27` (`_liet_ke_theo_duoi`, so trên `name.lower()`); packet này đưa cổng về cùng chiều.

## `write_set`

`ops/bien_nhan_v2.py` · `ops/bien_nhan_v2_test.py`

(Đo 09:23Z 29-10: `ops/bien_nhan_v2.py` ⇒ `NGƯỜI_GIỮ 0`; `ops/bien_nhan_v2_test.py` ⇒ `NGƯỜI_GIỮ 1: wp1017-r1-g1-claude` — vì thế có
điều kiện bắt đầu ở trên. Tệp đặc tả này KHÔNG thuộc write set; tìm nó ở nhánh mặc định trước, chưa thấy thì fetch nhánh
`claude/wonderful-ride-03x6oh`. Thứ định danh đặc tả là BĂM blob, không phải tên nhánh.)

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| Fixture Windows của `c91`/`c93`/`c96` (gồm fixture con `cau_hinh_canh_bao/khong-no` của `c91` còn ĐỎ trên Windows ở run `40844300802`, head `abc8607` của PR #1014) | Thuộc #1017 (lease `wp1017-r1-g1-claude`). PR #1014 làm trùng việc ấy mà không có lease — chủ kho chốt Q8 (a): đóng #1014, chuyển phát hiện `c91` sang #1017. |
| `ops/lease_publish_test.py` (`t26`/`t27`) và biên nhận wp929 | Thuộc #1006/PR #1007 (lease `wp1006-r1-g1-claude`). |
| Lọc `is_file()` | Ca `c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback` đòi một THƯ MỤC tên `*.receipt.yaml` phải tới được phép băm và ra rc=2. Lọc bỏ thư mục là xoá đúng phép đo ấy. Đây là chỗ khác CỐ Ý so với helper của #1007 (có `is_file`). |
| Selector ở tệp khác (`ops/land_evidence_nguon.py`, `ops/lease_publish.py`, …) | Ngoài write set; chưa đo có cùng lớp lỗi hay không — xem `chua_do_duoc`. |
| `.github/workflows/ci.yml` | Các bước đã có. |
| Sửa `D:\Quốc hội\tra-luat` trên máy chủ kho | Kho làm việc của chủ kho, có tệp chưa commit. Chạy local chỉ trong `D:\tl-win\<session_id>\`. |

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | MỘT helper chọn mục trong `THU_MUC` bằng `iterdir()` + `name.lower().endswith(".receipt.yaml")`, KHÔNG lọc `is_file()`, trả danh sách `sorted(...)` như cũ; cả hai chỗ (hàm kiểm chính và `_sinh_no`) gọi helper ấy, không còn `glob` chọn biên nhận. | `ops/bien_nhan_v2.py` |
| M2 | Thông báo `KhongDoDuoc` "không có tệp `*.receipt.yaml` nào" giữ nguyên nghĩa, nói rõ phép so không phân biệt hoa thường. | `ops/bien_nhan_v2.py` |
| M3 | Ca `rXX_` cho M1 (xem C1) và đột biến cho nó trong bảng `_dot_bien`. | `ops/bien_nhan_v2_test.py` |

## `nghiem_thu`

"Head cuối" = commit cuối của PR packet tại lúc xin land. Mọi N/N phải là hai số BẰNG NHAU in trong log, KHÔNG suy từ `rc=0`. Không ca
nào được trừ khỏi mẫu số vì `BỎ QUA`; bộ test không có cơ chế BỎ QUA và packet không thêm (chỉ chủ kho quyết, và khi ấy là BỎ QUA có
tên, được đếm, được in).

| # | tiêu chí | phép đo làm nó ĐỎ | nền |
|---|---|---|---|
| C1 (M1, M3) | Ca `rXX_` dựng kho git thật, thư mục biên nhận có `y.receipt.yaml` hợp lệ và `x.RECEIPT.YAML` HỎNG (YAML lỗi): trên CẢ HAI nền cổng **thấy** `x.RECEIPT.YAML` — dòng tổng kết có `tổng 2` và cổng không ra `TỔNG: ĐẠT` (rc ≠ 0, stderr nêu `x.RECEIPT.YAML`). Thêm: thư mục CHỈ có `X.RECEIPT.YAML` hợp lệ ⇒ không ra `KhongDoDuoc` "không có tệp". | Đột biến thường: helper về so đuôi CHÍNH XÁC (`name.endswith(...)`) ⇒ ca `rXX_` `giet_that` trên CẢ HAI nền (`endswith` không phụ thuộc nền). | Đo 09:26Z 29-10, Python 3.13 Linux, CHỈ phép chọn (chưa chạy cả cổng): thư mục có `y.receipt.yaml` + `x.RECEIPT.YAML` ⇒ `glob` trả `['y.receipt.yaml']`, helper M1 trả `['x.RECEIPT.YAML', 'y.receipt.yaml']` — tức ca `rXX_` trên base sẽ ĐỎ đúng như "chưa làm". Cả cổng trên fixture: chưa chạy (ca chưa viết). Windows: chưa đo. |
| C2 (M1, `c89` không chết) | `c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback` vẫn ĐẠT trên cả hai nền. | Đột biến thường: thêm `and p.is_file()` vào helper ⇒ `c89` `giet_that`. | `c89` ĐẠT trên Linux `735b181` (thuộc bộ chạy toàn phần). |
| C3 (hoàn nguyên `glob`) | Hoàn nguyên helper về `tm.glob("*.receipt.yaml")` phải làm `rXX_` ĐỎ trên Linux. | Đột biến này SỐNG trên Windows (glob ở đó vốn không phân biệt hoa thường) ⇒ KHÔNG đưa vào bảng đột biến thường (nó làm cổng Windows đỏ). Đo một lần trên bản sao tạm trên Linux, ghi lệnh + kết quả vào PR. | chưa đo |
| C4 (Windows CI) | `workflow_dispatch` `ci.yml` `runner_set=windows-only` trên head cuối. Job `gate-ops (windows-latest)`: `labels` = `["windows-latest"]`, `runner_id` ≠ 0 (đọc `actions/runs/<id>/jobs`). Bước `bien-nhan v2 selftest` in `N/N ca đạt · M/M đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`; bước `lease-publish selftest` CHẠY (không `skipped`) và in N/N hai số bằng nhau. | Cặp số nào lệch; bước `skipped`; nhãn khác hoặc `runner_id` 0. | đỏ sẵn trước #1017 (run `40833816523`: `90/93`) — phải xanh sau khi #1017 land, TRƯỚC khi bắt tay (đo lại trên base). |
| C5 (Linux CI) | Lượt PR Ubuntu trên CÙNG head cuối: hai bước của C4 trong `gate-ops (ubuntu-latest)` cùng N/N bằng nhau; nhãn `ubuntu-latest`. | Như C4. | chưa đo trên head cuối |
| C6 (cổng thật không trôi) | `python ops/bien_nhan_v2.py --root .` trên head cuối (kho KHÔNG nông): `rc=0`, `TỔNG: ĐẠT`; `tổng` = số mục trong `ops/reviews` có `name.lower().endswith(".receipt.yaml")` đếm độc lập bằng một lệnh riêng ghi trong PR. | `tổng` khác số đếm độc lập ⇒ ĐỎ. | 09:24Z 29-10 trên `735b181`: `251 ĐẠT v2 · 11/11 miễn trừ · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 304`, rc=0; đếm độc lập 304 = 304 |
| C7 (Windows local) | Nếu máy chủ kho (ASUS-LAPTOP) Online qua Desktop Commander: theo quy ước dùng chung máy (khoá `D:\tl-win\KHOA.txt`; thư mục riêng `D:\tl-win\<session_id>\` clone từ GitHub, `core.abbrev 7`; `PYTHONUTF8=1` `PYTHONIOENCODING=utf-8` `PYTHONDONTWRITEBYTECODE=1`; gọi `python`), chạy `python ops/bien_nhan_v2_test.py` trên head cuối và một lần đo nền trên nhánh mặc định; mỗi lần chạy thêm MỘT dòng vào `D:\tl-win\do-luong.csv` đủ cột quy ước. PR ghi SHA, lệnh, N/N, và nói rõ là LOCAL. | Có chạy local mà còn lỗi chưa vá ⇒ CHƯA được merge. Local KHÔNG thay C4/C5. | chưa đo |
| C8 (điều kiện merge) | Hết P0, P1, P2 **và P3** trên head cuối; verdict Codex `approve` trên ĐÚNG head cuối (`reviewed_sha` 40 ký tự), trong trần 4 lời gọi; đã vá hết lỗi Windows local nếu C7 đã chạy. | Còn finding P0–P3 mở; `reviewed_sha` khác head; vượt trần. | — |
| C9 (cổng chung) | `python -m ruff check --select F` hai tệp: delta 0 so base; `python .claude/dev/packet_loop.py doctrine-scan --root .` rc=0; `git diff --check` rc=0; `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng (vế âm) — vế dương là C1 xanh trên head; `git diff --numstat <base>..<head cuối>` ghi vào PR. | Ô nào khác ⇒ ĐỎ. Đột biến cho vế âm: chèn lại một dòng `glob` ⇒ 1 dòng. | `rg` trên `735b181` ⇒ 2 dòng (1442, 1601) — đúng màu "chưa làm" |

## `hinh_dang_ke_thua`

Đơn vị: finding (mục `###` của verdict); "lượt" = một lượt review Codex. Nguồn: `ops/reviews/wp960-r2-review-{1..7}-codex-verdict.md`
(đã vào nhánh mặc định qua PR #1012, có mặt trên `735b181`), theo nhãn `HÌNH DẠNG:` tự khai của từng finding; và hai comment
cross-review trên PR #1014.

| hình dạng | wp960 r2 (7 lượt, 29 finding) | #1014 (2 lượt) | tổng lượt có mặt |
|---|---|---|---|
| `loi-do` — lỗi ĐO thành sạch/vi phạm (kể cả chiều ngược: kho lành thành rc=2) | 22 finding · lượt 1–6 | 0 | 6 |
| `bo-chon-ung-vien` — bộ chọn bỏ sót/bắt nhầm, hoặc chốt chọn không có răng riêng | 5 finding · lượt 1, 2, 3, 6, 7 | 0 | 5 |
| `khac` | 2 finding · lượt 1 | 0 | 1 |
| fixture/phép so phụ thuộc nền | 0 (cả 7 lượt chạy trên Linux) | 1 finding (`windows-fixture-path-oracle-drift`, P2, lượt 1) | 1 |

Chốt dừng: packet này SỬA ĐÚNG một bộ chọn (biên nhận nào được kiểm). `bo-chon-ung-vien` đã quá ba lượt từ wp960 r2 ⇒ **một** finding
mới mang hình dạng ấy trên M1 ⇒ DỪNG và hỏi chủ kho "có nên làm tiếp theo cách này không", không vá tiếp. Hình dạng "phụ thuộc nền"
lặp ở lượt thứ 3 (đếm cả #1014) ⇒ cùng chốt.

## Kích thước dự kiến

Ước (chưa đo): `ops/bien_nhan_v2.py` +12/−2 · `ops/bien_nhan_v2_test.py` +50/−0 ⇒ ≈ +62/−2 trên 2 tệp. Đối chiếu trần `sensitive` của
`ADR-0053`; vượt thì khai đúng dạng ADR ấy trong PR. Không khai `tran_kich_thuoc_sensitive` vì ước lượng xa dưới mọi trần đã biết — đo
lại trên head cuối (C9).

## `chua_do_duoc`

- **Windows (C4, C7)**: chưa đo cho M1. Desktop Commander KHÔNG kết nối được từ phiên soạn đặc tả (MCP `CONNECT_TIMEOUT`, ~09:00Z và
  ~09:23Z 29-10). Quy ước máy dùng chung đến từ phiên điều phối `session_01V2PEqhkb91vD5PCBM5yXbm`; chủ kho xác nhận đưa vào ~09:08Z 29-10.
- **Thứ tự `sorted` trên Windows**: `Path` so sánh không phân biệt hoa thường trên Windows và có phân biệt trên POSIX, nên THỨ TỰ duyệt có
  thể khác giữa hai nền. Cổng hiện không in gì phụ thuộc thứ tự ngoài thứ tự dòng lỗi; chưa đo có kết quả nào đổi theo thứ tự hay không.
- **Hai tệp chỉ khác hoa thường** (`a.receipt.yaml` và `a.RECEIPT.YAML`): trên Windows không tồn tại cùng lúc; trên Linux cả hai đều bị
  kiểm sau M1. Chưa có ca nào đo hành vi ấy; không đưa vào nghiệm thu vì không dựng được trên Windows.
- **Selector cùng lớp ở tệp khác** ngoài write set (`ops/land_evidence_nguon.py`, `ops/lease_publish.py`, …): chưa quét.
- **Base thật**: các cột "nền" đo trên `735b181`, TRƯỚC #1017/#1007; phải chạy lại khi cấp lease.
