# ĐẶC TẢ — `LEASE-ID-EP-KIEU-YAML` — **revision 3, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp678` (ID bền theo protocol §3.2, `wp<issue>`); tên đọc được: `LEASE-ID-EP-KIEU-YAML`. Hai tên chỉ cùng một packet; lease dùng `wp678` hoặc tên đọc được đều phải kèm `packet_issue: 678`. |
| `revision` | **3** |
| `thay_the_cho` | revision 2: `ops/specs/lease-id-ep-kieu-yaml-r2.md`, sha256 `1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715`, commit `aecdccd`. Chuỗi lịch sử: revision 1 `ops/specs/lease-id-ep-kieu-yaml-r1.md`, sha256 `578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c`, commit `342e62c7`. |
| `packet_issue` | **#678** |
| `mission_issue` | **#682** (Mission Issue, object ID `5627190292`, tạo 29-09-2026, tiêu đề *"Mission wp678: quyết định chủ kho + miễn trừ closure có phạm vi cho LEASE-ID-EP-KIEU-YAML"*). Issue này do **phiên agent đăng HỘ chủ kho** bằng credential chủ kho, nên `author_association: OWNER` không chứng minh chủ kho tự gõ; nguồn thẩm quyền là các câu trả lời của chủ kho trong phiên (Q0–Q6) được trích trong thân #682. Packet cha #579 (đặc tả `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md`) không khai `mission_issue` và không cấp ngoại lệ gì cho packet này. |
| `nguon_cap_viec` | Phát hiện phụ của #677 (mục *"Phát hiện phụ — TÁCH packet riêng"*). Chủ kho quyết định tách packet 29-09-2026, rồi trả lời *"Đồng ý"* trong phiên cho ba đề xuất: (a) mở Issue + soạn đặc tả; (b) chỉ nhận **chuỗi thật**, bỏ cả `int`; (c) xếp sau `T131-DEADLINE-DEM-SPAWN`. Q3 xác nhận riêng: #678 comment `5885268193`. **r2** là hệ quả của cross-review lượt 1 trên PR #679 (comment `5885578969`, VERDICT sha256 `d4acdd38…b8add`), dưới chỉ thị chủ kho *"cross-review #679 đi, theo phân lớp, không theo từng lỗi, có hint patch"*. **r3** là hệ quả của cross-review lượt 2 trên PR #679 (comment `5886034260`, VERDICT sha256 `aa9a68d3…d4882`: 1 P1 / 3 P2 / 1 P3 theo lớp), và của quyết định chủ kho chọn neo lớp P1 bằng Mission Issue mới (#682). |
| `objective` | Mọi đường đưa `lease_id` vào danh tính chỉ nhận chuỗi thật khớp `LEASE_ID`, đóng va chạm do ép giá trị không phải chuỗi thành chuỗi. Danh tính là giá trị sau `yaml.safe_load`: các cách viết ra cùng một chuỗi hợp lệ cố ý là cùng danh tính (ví dụ `'yes'` và `!!str yes`), không yêu cầu phân biệt cú pháp YAML. |
| `review_class` | **`sensitive`**: chạm `ops/lease_publish.py`, tức cổng đăng lease. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` (Claude Opus 5.5, effort ≥ medium) |
| `environment` | **`cloud`**. Packet không đo hành vi phụ thuộc nền (không đồng hồ ngủ máy, không đường dẫn Windows); tiền lệ các đặc tả `ops/specs/*` cùng lớp khai `cloud`. Chủ kho đổi thì phải ra revision mới. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium) |
| `depends_on` | Lease `t131-deadline-dem-spawn-exec-1-claude-20260929` phải được **thu hồi** trước khi cấp lease cho `wp678`. T131 **đã land** (PR #680, `89fc4fa`), nhưng đo 07:59Z 29-09: `ai-dang-giu ops/lease_publish_test.py` vẫn ⇒ `NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929` — lease không tự chết khi packet land; chủ kho thu hồi. `ai-dang-giu ops/lease_publish.py` ⇒ `NGƯỜI_GIỮ 0`. |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518` (PR #680, T131 land). Đây là **nền bất biến** để đo diff và nghiệm thu. r1 và r2 dùng `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; packet CHƯA thi hành, chưa có diff hay lịch sử finding trên mã, nên dời nền ở revision này là quyết định bền (chính revision này) theo protocol §3.2.1, không phải dùng HEAD mới để xoá diff. `ops/lease_publish.py` giống hệt giữa hai nền (`git diff --quiet` rc=0), nên các phép đo §1/§2 làm trên `1741e0a` vẫn hợp lệ; chỉ `ops/lease_publish_test.py` đổi (+13/−19, bốn hunk quanh t130, t131, t139, t191). Nền tiếp nối (continuation base), nếu khác, phải được khai riêng lúc cấp lease, không thay nền này. |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/lease-id-ep-kieu-yaml-r3.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #678 và lease, kèm OID commit + đường dẫn. Hai tên `spec_hash`
và `spec_sha256` nếu cùng xuất hiện thì mang **cùng** một giá trị. Đổi bất kỳ byte nào ⇒
revision mới, băm mới, lease mới. Vì khối closure dưới đây nằm **trong** tệp, cùng một `spec_hash`
không thể đi với hai closure khác nhau (đóng phản chứng "hai lease khác `required_checks` cùng
một băm" của lượt 2).

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2). Kho chưa có dispatcher
sinh chúng và chưa có policy canonical cho closure; khối này do phiên điều phối điền tay theo
**miễn trừ có phạm vi** ghi ở Mission Issue #682: chỉ `wp678`, mọi revision từ r3, hết hiệu lực
ở lần đầu một policy canonical cho closure xuất hiện trên nhánh mặc định; đổi bất kỳ giá trị
closure ⇒ revision mới, `spec_hash` mới, lease mới; write set không mở rộng.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #682 |
| `effective_write_set` | `ops/lease_publish.py` · `ops/lease_publish_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành: `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)` của `.github/workflows/ci.yml`, và workflow `thu-hoi`; cross-review codex 0 P1/P2/P3 |
| `land_obligations` | Chủ kho audit + merge (không tự merge/approve); ghi sổ verdict + HINT các lượt vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #678; cập nhật #677 về tương tác A2 |

**Descriptor nguồn closure** = `{mission_issue: 682, object_id: 5627190292}`. Closure do phiên
điều phối điền tay theo miễn trừ ấy, **không** do executor tự khai. Lease phải **chép** đúng các
giá trị trên, không được thêm hay đổi; lệch ⇒ **DỪNG**. Băm thân Issue ở phía nhận là
**KHÔNG ĐO ĐƯỢC** từ phiên này (đường đọc MCP chuẩn hoá thực thể HTML trong thân issue, xem
CLAUDE.md), nên descriptor neo bằng object ID + số Issue, không bằng băm thân.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## 1. Vấn đề

`_doc_yaml` dùng `yaml.safe_load` (YAML 1.1), nên một vô hướng không nháy được tự ép kiểu.
`kiem()` làm `str(lease["lease_id"])` **rồi mới** `LEASE_ID.fullmatch`. Vì vậy nhiều cách viết
khác nhau cho ra **cùng một danh tính**, và danh tính ấy là thứ cổng đăng dùng để chống đăng trùng.

Bảng đo 06:2xZ 29-09-2026 trên `1741e0a`. Cách dựng: lease
`wp55-r4-review-viet-lai-codex-20260815.yaml`, bỏ các trường `prompt_*`, gọi
`kiem(bo_qua_han=True)` không truyền `tep`, nên **đường bia mộ chưa chạy** ở phép đo này.

| YAML `lease_id:` | kiểu | `str()` | `_tien_kiem_mien_dang` | `kiem()` |
|---|---|---|---|---|
| `true` `yes` `on` `True` | bool | `True` | rc=8 | qua |
| `1.5` `1.50` | float | `1.5` | rc=8 | qua |
| `0x1F` | int | `31` | qua | qua |
| `017` | int | `15` | qua | qua |
| `1_000` | int | `1000` | qua | qua |
| `2026-09-29` | date | `2026-09-29` | rc=8 | qua |
| `'yes'` (đối chứng) | str | `yes` | qua | qua |

Va chạm đo tại `_kiem_comment_da_co`, với `_doc_gh` giả trả **một** comment của
`github-actions[bot]`. Sáu cặp (comment có sẵn ↔ lease mới) `True`↔`yes`, `True`↔`on`,
`1.5`↔`1.50`, `31`↔`0x1F`, `15`↔`017`, `1000`↔`1_000` đều cho **rc=9**, tức cổng coi lease là
đã đăng nên lease mới **không bao giờ được đăng**. Đối chứng `khac-lease`↔`yes` cho rc=0, nên
cách dựng không cho kết quả giả.

Ở **biên workflow** (thân bước `đăng` trích bằng `_buoc_workflow`, `lease_publish.py` thật, `gh`
giả trên PATH, giữ trạng thái), cross-review lượt 1 đo trên `342e62c7` (cùng blob hai tệp Python
với `1741e0a`): lease `yes` gặp comment ``**Lease `True`**`` ⇒ bước `rc=0`, **0 POST**; đối chứng
`'fresh-id'` ⇒ `rc=0`, **1 POST**. Tức lease hợp lệ bị bỏ qua mà bước vẫn xanh. Ca khoá ở A3
biến phép đo ấy thành ca của suite.

## 2. Các đường `lease_id` đi vào danh tính (số dòng trên `1741e0a`)

Liệt kê HẾT trước khi vá (bài học *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"*). Tìm bằng
`grep -n '"lease_id"\|\[.lease_id.\]' ops/lease_publish.py`, không phải bằng trí nhớ.

| # | chỗ | hiện trạng |
|---|---|---|
| D1 | `kiem()` :861 | `str()` rồi mới so regex ⇒ nhận bool/float/int/date |
| D2 | `_tien_kiem_mien_dang` :949 | nhận `str\|int`, chặn `bool`; lệch với D1 |
| D3 | `_kiem_comment_da_co` :668 | `str()` ⇒ va chạm ở §1 |
| D4 | `dung_than` :1070 | f-string ⇒ đăng dấu đã bị ép kiểu |
| D5 | `_bia_mo_doi_xung` :587/:592 | `str(... or "")` cho cả lease cũ lẫn lease được quét |
| D6 | `_kiem_bia_mo` :609/:612 | `str(... or "")`; trong khi `_danh_sach_thay_the_cho` đòi chuỗi thật |
| D7 | `lenh_ai_dang_giu` :2110/:2123 | `str(...)` rồi dùng làm khoá người giữ ⇒ `yes` và `on` gộp về `True` |
| D8 | `_du_bao_check` :1938/:1942/:1946; `_du_bao_ai_dang_giu` :1967 | :1938/:1942 so giá trị thô; :1946 f-string, :1967 `str()` rồi tra tập ID thu hồi |
| D9 | in :2074/:2089; `lenh_con_tro_treo` :2139/:2143 | chỉ hiển thị; không gán hai chỗ sau cho D7 |
| — | `kiem_ban_ghi_thu_hoi` :1192 | **ĐÃ** đòi `isinstance(str)`: tiền lệ trong chính tệp, không sửa |

Ngoài tệp: `.github/workflows/*.yml` **không** đọc `lease_id` (grep 0 dòng).
`.claude/dev/packet_loop.py` :769–771 **đã** đòi `isinstance(str)` cho `lease_id` (tiền lệ thứ hai).

## 3. Quyết định

- **Q1 — Danh sách CHO PHÉP kiểu** (chủ kho, 29-09): `lease_id` hợp lệ khi và chỉ khi nó là
  `str` **ngay sau `yaml.safe_load`** **và** khớp `LEASE_ID`. `int` cũng bị từ chối. Sai ⇒
  `Chan(RC_NOI_DUNG)`, tức rc=8.
- **Q2 — Một hàm dùng chung** (chủ kho, 29-09): mọi đường D1–D8 đọc `lease_id` qua **một**
  hàm, không ai tự gọi `str()` lên giá trị thô.
- **Q3 — Lease sai kiểu gặp trong lúc QUÉT** (đã được chủ kho xác nhận cùng Q1–Q4 tại
  packet #678, theo authority giao cross-review): ở D5, D6, D7, một lease **khác** mang `lease_id` không phải
  chuỗi thì **không** được ép sang chuỗi để so. D7 in `KHÔNG_XÁC_ĐỊNH` cho nó và thoát khác 0
  (fail-close, cùng hình dạng với nhánh bia mộ một chiều đang có). D5/D6 coi nó là **không
  khớp** bất kỳ tên nào, và vì vậy bia mộ trỏ tới nó sẽ không thoả.
- **Q4 — Thứ tự**: sau `T131-DEADLINE-DEM-SPAWN`. Hai packet còn chồng write set là #677 và
  `LEASE-PUBLISH-WINDOWS-DO`; chủ kho xếp, packet này không tự nhảy lên trước.

## 4. `write_set`

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

Không đường dẫn nào khác. Riêng đặc tả này (`ops/specs/lease-id-ep-kieu-yaml-r3.md`, và các bản r1, r2 nó thay) là hồ sơ
của lượt soạn spec, **không** thuộc write set của lượt thi hành.

## 5. `ngoai_pham_vi`

- `.github/workflows/**`: không đọc `lease_id`, và phiếu cấm sửa trừ khi chủ kho cho phép rõ.
- `.claude/dev/packet_loop.py`: đã đòi chuỗi (§2).
- `kiem_ban_ghi_thu_hoi` và sổ thu hồi: đã đòi chuỗi (§2).
- Ép kiểu của **các trường khác** (`reviewed_sha_required`, `expires_utc`…): cùng họ lỗi, nhưng
  không nằm trong quyết định của chủ kho. Lượt thi hành gặp thì ghi thành phát hiện ngoài spec,
  **không** tự mở rộng.
- Idempotency theo nội dung thay vì theo `lease_id`: là việc của #584.
- Thêm/đổi lease trên Issue thật để thử: không làm, mọi phép đo dùng `gh` giả.

## 6. `muc_tieu`

Mỗi dòng chiếu vào **một** đường dẫn trong write set (L2).

1. `ops/lease_publish.py` — Thêm một hàm (tên tuỳ executor, ví dụ `_lease_id_hop_le`) nhận giá
   trị thô và trả `str` hoặc ném `Chan(RC_NOI_DUNG)`. Dùng nó ở D1 và D2.
2. `ops/lease_publish.py` — D3 và D4 tự gọi hàm ấy. Không dựa vào việc `kiem()` đã chạy trước;
   mỗi đường một chốt riêng.
3. `ops/lease_publish.py` — D5 và D6 so danh tính theo Q3, bỏ `str(... or "")` lên giá trị thô.
4. `ops/lease_publish.py` — D7 theo Q3: gặp lease sai kiểu thì in `KHÔNG_XÁC_ĐỊNH` và thoát khác 0.
5. `ops/lease_publish.py` — D8 so bằng giá trị đã qua hàm ở mục 1, hoặc chứng minh đường ấy
   không tới được với giá trị sai kiểu (xem A7).
6. `ops/lease_publish_test.py` — Một ca cho mỗi mục 1–5, theo §7.
7. `ops/lease_publish_test.py` — Sửa các docstring/chú thích đang **khai hiện trạng lỗi** thành
   sự thật mới. Ví dụ đã biết: `t178` :7763–7764 (trên `89fc4fa`; trước là 7769–7770 trên `1741e0a`) viết *"`lease_id` sai KIỂU thì không có chốt
   tương ứng trong `kiem()`"*. Executor phải grep tìm hết, đừng chỉ sửa chỗ này.

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). "Đột biến" nghĩa là chạy trên **bản sao tạm**, với
`PYTHONDONTWRITEBYTECODE=1`.

- **A1 (mục 1, D1)** — Ca mới: các dạng `true` `yes` `on` `1.5` `1.50` `0x1F` `017` `1_000`
  `5` `2026-09-29`, viết thành **văn bản YAML** và đọc qua `_doc_yaml` (không dựng dict bằng
  tay, để phép đo đi qua đúng lớp gây lỗi), đều cho `kiem()` ⇒ rc=8. Đối chứng `'yes'` có nháy
  ⇒ qua.
  **ĐỎ khi:** trả D1 về `str(lease["lease_id"])` ⇒ các dạng trên qua. Trên nền `89fc4fa` (mã `ops/lease_publish.py` giống hệt `1741e0a`) ca
  này ĐỎ.
- **A2 (mục 1, D2)** — Mở rộng trục `lease_id` sai kiểu của `t178` thêm `int`; giữ chốt
  `_do_dau_da_dang` trả về bình thường và **0** lời gọi GitHub. Đo thêm D2 trực tiếp:
  `_tien_kiem_mien_dang` nhận `int` ⇒ `Chan(RC_NOI_DUNG)`; chuỗi hợp lệ ⇒ trả về.
  **ĐỎ khi:** trả riêng D2 về `(str, int)` ⇒ ca trực tiếp nhận trả về thay vì rc=8.
  Không đòi phép dò gọi GitHub khi D2 bị gỡ: D3 có chốt độc lập trước `_doc_gh`, nên vẫn
  có thể giữ số gọi bằng 0. Không dời chốt D3 xuống sau mạng chỉ để giết mutant D2.
  Tương tác #677: `L` gỡ riêng D2 nay có thể sống ở phép đếm mạng của `t178`; ca trực tiếp
  phải giết `L` bằng `TinHieuChotCa` đúng ca. #677 **chưa có đặc tả đóng băng** (Issue #677
  khai `revision 0`, đo 06:2xZ 29-09; vẫn chưa có đặc tả đóng băng tại 07:59Z 29-09, nội dung nghĩa vụ hai thứ tự dưới đây không đổi), nên không có acceptance nào của nó để neo lúc này.
  Hai thứ tự, hai nghĩa vụ: packet này land TRƯỚC ⇒ đặc tả #677 phải được soạn trên nền mới
  và coi ca trực tiếp của A2 là nơi `L` chết; #677 land TRƯỚC ⇒ ca của #677 nằm trong
  `ops/lease_publish_test.py`, tức trong write set này, và lượt thi hành phải giữ nó xanh
  với ý nghĩa đã đổi. Executor **không** sửa đặc tả #677.
  Sửa cả docstring D2 và `t178` để tách bằng chứng lịch sử khỏi hành vi sau D3.
- **A3 (mục 2, D3) — CA BIÊN WORKFLOW** — Thân bước `đăng` trích từ
  `.github/workflows/ops-publish-lease.yml` (dùng lại bộ trích sẵn có trong suite, không chép
  lại), `lease_publish.py` thật, `gh` giả **trên PATH** và **giữ trạng thái**. Issue đã có comment
  bot ``**Lease `True`**``; lease mới khai `lease_id: yes` ⇒ bước **khác 0** và **0 POST**. Kèm
  ca đối chứng dương: một `lease_id` chuỗi hợp lệ khác ⇒ bước 0 và đúng **1 POST**, để giàn hỏng
  không thể xanh.
  **ĐỎ khi:** chạy trên nền `89fc4fa` (mã giống hệt `1741e0a`) ⇒ bước `rc=0`, 0 POST (lời khai của phiếu; ca này là phép
  đo đầu tiên của nó).
  Kèm ca **đơn vị**: gọi thẳng `_kiem_comment_da_co` với `lease_id=True` ⇒ rc=8, **không** rc=9.
  Đột biến gỡ chốt riêng của D3 (giữ nguyên D1) ⇒ ca đơn vị ĐỎ.
- **A4 (mục 2, D4)** — Gọi thẳng `dung_than` với `lease_id` không phải chuỗi ⇒ rc=8.
  **ĐỎ khi:** gỡ chốt riêng của D4 ⇒ nó trả thân có ``**Lease `True`**``.
- **A5 (mục 3, D5/D6)** — Fixture kho git tạm: lease cũ `lease_id: 1_000` (int) mang
  `da_bi_thay_the: <mới>`; lease mới khai `thay_the_cho: "1000"` ⇒ `_kiem_bia_mo` rc=8. Đối
  chứng: lease cũ `lease_id: "1000"` có nháy ⇒ qua. Đo riêng `_bia_mo_doi_xung` bằng cặp tương
  tự: bản sai kiểu ⇒ `False`, bản chuỗi ⇒ `True`.
  Bổ sung đầu còn lại: ở D5, lease cũ chuỗi trỏ `da_bi_thay_the: "1000"`, lease được
  quét có `lease_id: 1_000` và trỏ ngược ⇒ `False`; đổi ID được quét thành `"1000"` ⇒ `True`.
  Ở D6, gọi trực tiếp với lease mới `lease_id: 1_000`, lease cũ chuỗi trỏ ngược `"1000"`
  ⇒ rc=8; đổi ID lease mới thành `"1000"` ⇒ qua. Không đi qua D1 trong các ca đơn vị này.
  **ĐỎ khi:** trả phép ép kiểu về riêng từng toán hạng ở D5 (:587, :592) và D6 (:609, :612),
  giữ nguyên các chốt còn lại; mỗi mutant phải giết đúng ca đổi kiểu toán hạng ấy.
  Không hoàn nguyên cả hàm rồi nhận đó là bằng chứng mọi vị trí đọc đều có răng.
- **A6 (mục 4, D7)** — Hai lease trên hai ref, `lease_id: yes` và `lease_id: on`, cùng giữ một
  đường dẫn ⇒ `ai-dang-giu` in `KHÔNG_XÁC_ĐỊNH` cho cả hai và thoát khác 0.
  **ĐỎ khi:** chạy trên nền với hai lease còn hạn ⇒ `NGƯỜI_GIỮ 1: True`, rc=11.
  Vì nền đã khác 0, ca phải chốt nhãn `KHÔNG_XÁC_ĐỊNH` và danh tính ref/path của cả hai
  lease lỗi; không chỉ kiểm `rc != 0`. Đo lại 29-09-2026 bằng fixture hai ref trong review #679.
- **A7 (mục 5, D8)** — Đo riêng cả `check --du-bao` và `ai-dang-giu --du-bao`.
  `check` qua D1 trước; `ai-dang-giu` gọi dự báo trước vòng D7 và không gọi D1. Không dùng
  kết quả không tới được của `check` để miễn nhánh `ai-dang-giu`, hoặc chỉ đo lời gọi trực
  tiếp helper rồi suy thành khả năng tới được từ CLI. Lease sai kiểu vẫn tới :1967 trên
  nền; khi thêm chốt ở D8 cần ca trực tiếp để D7/D1 không che mutant của chính D8.
  · Tới được ⇒ chốt + ca, đột biến gỡ chốt ⇒ ĐỎ.
  · Không tới được ⇒ một ca chứng minh lease sai kiểu bị chặn **trước** các dòng ấy, kèm đột biến
  gỡ chốt D1 để chứng minh ca có răng. Ghi rõ đã chọn nhánh nào và bằng phép đo nào.
- **A8 (mục 6/7, cả write set)** — Toàn suite `ops/lease_publish_test.py` **delta = 0 ca đỏ**
  so với nền. Số lịch sử đo 06:4xZ 29-09 trên `1741e0a`: **185/187**. Hai ca đỏ là `t137` và `t159`,
  cả hai `KHÔNG ĐO ĐƯỢC: thiếu shellcheck` (lời khai lịch sử, không dùng làm nền hiện tại).
  Review #679 đo lại 29-09-2026: **187/187**, rc=0, bỏ qua=0, với shellcheck 0.9.0 và
  actionlint 1.7.7; hai tệp Python có cùng blob với `1741e0a` (lịch sử). **Nền hiện tại**
  (`89fc4fa`): suite **187/187**, rc=0, bỏ qua 0, đo 08:0xZ 29-09 trên commit merge `589336f`
  (cây của `89fc4fa` + các tệp spec) với shellcheck 0.9.0 + actionlint 1.7.7. Lệnh: từ gốc repo chạy
  `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python ops/lease_publish_test.py`.
  Khi thi hành, đo lại **cả hai vế** (nền và ứng viên) trong **một** lệnh, cùng công cụ.
  `python -m ruff check --select F ops/lease_publish.py ops/lease_publish_test.py`: delta F = 0.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, hoặc có thêm lỗi F.
- **A9 (quét lại, không đổi lease)** — Trước cấp lease và trước xin land, quét miền bao trùm
  runtime: `refs/heads/*` và `refs/remotes/*`, chỉ bỏ ref có leaf HEAD VÀ là symbolic ref;
  ref thường có hậu tố `/HEAD` vẫn phải quét (runtime hiện bỏ cả hậu tố này; đây là miền
  nghiệm thu bảo thủ hơn, không yêu cầu đổi bộ liệt kê ref runtime). Đọc cả `.yaml` lẫn `.yml`
  dưới `ops/leases/`. Quét thêm `ops/leases_retired/` với nhãn lịch sử riêng. Kiểm rc của
  mọi lệnh Git, lỗi parse, tài liệu không phải ánh xạ, thiếu ID và ID không qua Q1; bất kỳ
  trường hợp nào ⇒ **DỪNG**, báo chủ kho. Không im lặng bỏ mục lỗi khỏi mẫu số.
  Kiểm `thay_the_cho` theo schema chuỗi/danh sách chuỗi và `da_bi_thay_the` theo schema
  chuỗi; không dùng chung phép chấp nhận list cho cả hai. Chỉ đo, không sửa lease cũ.
  Ghi UTC, lệnh/script nguyên văn, tập ref+OID, số blob, số cặp (blob,path), số ánh xạ đủ
  ID, số từng kiểu và lỗi riêng; đối chiếu tên+OID với nguồn ref được cấp. Offline chỉ
  chứng minh snapshot mirror, không khai đã đo máy chủ live. Khi công bố cần nguồn ref
  đầy đủ đã được xác minh; không truy cập được nguồn cần thiết là KHÔNG ĐO ĐƯỢC.
  **ĐỎ khi:** self-test của chính phép quét trên kho tạm thêm lần lượt lease `int` ở `.yml`,
  lease sai kiểu chỉ trên local head, thiếu ID, tài liệu không phải ánh xạ, YAML lỗi,
  `da_bi_thay_the` list hoặc lỗi Git ⇒ từng vế phải báo lỗi; đối chứng chuỗi hợp lệ phải qua.
  Kiểm thêm `thay_the_cho: [""]`, `["   "]`, `da_bi_thay_the: "   "` (đều lỗi),
  đối chứng `thay_the_cho: []` (hợp lệ), và ID sai kiểu chỉ ở ref thường `topic/HEAD`.
  Quy tắc con trỏ phải khớp schema hiện hữu: phần tử list là chuỗi không trắng;
  bia mộ khi có phải là chuỗi không trắng. Không biến việc kiểm schema thành yêu cầu
  mọi bia mộ lịch sử đều còn cặp đối xứng trên cùng ref.
  Đặt helper/self-test mới trong `ops/lease_publish_test.py`; ghi lệnh tái lập trong
  handoff, không thêm đường dẫn mã ngoài write set. Không dùng `quet.py` nháp chưa có ca
  kiểm làm cổng: nó bỏ qua `.yml`, thiếu ID và tài liệu không phải ánh xạ.
- **A10 (tự kiểm của bộ đột biến)** — Mỗi đột biến ở A1–A7 phải giết ca đích **bằng
  `TinHieuChotCa` của đúng ca ấy**, không bằng một ngoại lệ vô can (bài học *"ĐỘT BIẾN BỊ GIẾT
  KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Bảng kết quả khai ba hạng: giết thật / tín dụng giả /
  sống sót.

## 8. Số đo nền (thời điểm đo cạnh từng số)

Đo lại 07:59Z 29-09-2026 trong container phiên soạn, kho đã `--unshallow`, `origin/master` đã tiến
từ `1741e0a` lên `89fc4fac8cea65979cc2483043dc8cd07a6e8518` (PR #680). Số của r1, r2 và của các
lượt cross-review giữ dưới nhãn lịch sử.

- **Ref.** `git ls-remote --heads origin` (hỏi máy chủ) so `git for-each-ref
  refs/remotes/origin` (đọc đệm), theo **tập tên**, bỏ `HEAD`: **506 = 506**, thiếu 0, thừa 0.
  Lịch sử: 503 ở r1 (06:1xZ); 505 ở r2 (07:2xZ).
- **Người giữ** (07:59Z). `ai-dang-giu ops/lease_publish.py` ⇒ `NGƯỜI_GIỮ 0`;
  `ai-dang-giu ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929`
  (T131 đã land nhưng lease chưa thu hồi; xem `depends_on`).
- **Quét lease** bằng đúng khối mã ở **Phụ lục A** (bản r3), chạy qua entry point
  (`python quet.py <goc-kho>`), JSON `utc` `2026-09-29T07:59:26Z`, rc=0: `ref_count` **508**
  (506 `refs/remotes` + 2 `refs/heads`), `blob_count` **562**, `pair_count` **562**,
  `mapping_count_pairs` **562**, `id_count_pairs` **562**, `type_counts_pairs` `{str: 562}`,
  `ops/leases` 562 blob / 562 cặp, `ops/leases_retired` 0 blob / 0 cặp, `errors` **0**.
  `ops/leases_retired` = 0 trên mọi ref là số **đo**, không phải giả định.
  Lịch sử: 559 ở r1 và lượt 1; 560 ở r2 (sau `fetch` 07:21Z). Hai nhánh đẩy sau lượt `fetch`
  trước đó (`ops/cap-lease-ci-duong-nhanh-ho-so`, `ops/cap-lease-ci-g5-cong-cu-chia-manh`)
  mỗi nhánh thêm một tệp lease so với master mà tổng chỉ tăng 1 blob; phần chênh chưa truy
  nguyên (`KHÔNG ĐO ĐƯỢC`, không đổi kết luận vì mọi `lease_id` đều là chuỗi). Đây là trôi số
  của L5 xảy ra ngay trong lúc soạn.
- **Suite.** Nền hiện tại: **187/187**, rc=0, bỏ qua 0, đo 08:0xZ 29-09 trên commit merge
  `589336f` (cây `89fc4fa` + tệp spec), `PYTHONDONTWRITEBYTECODE=1 python ops/lease_publish_test.py`
  với `shellcheck` 0.9.0 + `actionlint` 1.7.7.
  Lịch sử trên `1741e0a`: r1 khai 185/187 lúc container thiếu `shellcheck` (`t137`, `t159` báo
  `KHÔNG ĐO ĐƯỢC: thiếu shellcheck`); lượt 1 đo 187/187.
- **Kích thước.** `ops/lease_publish.py` 2206 dòng (không đổi giữa hai nền);
  `ops/lease_publish_test.py` **10502** dòng trên `89fc4fa` (10508 trên `1741e0a`), 187 ca,
  số ca lớn nhất `t192`.
- **Ruff**: vẫn `KHÔNG ĐO ĐƯỢC` ở phiên soạn (module vắng trong sandbox);
  A8 bắt lượt thi hành đo cả hai vế.

Mọi con số trên phải được **đo lại** trước mỗi bước công bố: đăng băm/revision, cấp lease
và land (L5). Ghi thời điểm đầy đủ và lệnh cạnh số mới; giữ số cũ với nhãn lịch sử nếu cần.
Quyết định neo vào **bất biến** (mọi `lease_id` là chuỗi; người giữ T131 còn giữ), không neo
vào con số 506/562.

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: đây không phải packet khắc phục một lượt thất bại. Nguồn là một phát hiện phụ
của #677, không kèm bộ đếm hình dạng lỗi nào.

Rủi ro hình dạng đã biết, ghi để lượt thi hành canh: *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ
BA"*. §2 liệt kê 8 đường sửa (D1–D8) cộng D9 chỉ hiển thị; lượt thi hành phải **grep lại** chứ không tin bảng này là
đủ, và khai đường nào mới tìm thấy.

## 10. `chua_do_duoc`

- Mã thực thi chưa tồn tại, nên mọi tiêu chí A1–A10 mới được kiểm **khả thi**: hai lượt
  cross-review đã dựng mô hình chốt tạm trên bản sao để kiểm A1–A10; vẫn **chưa có ứng viên
  thật**.
- Đường `DU_BAO`: lượt 1 đo được `ai-dang-giu --du-bao` đưa `int` tới :1967 (không qua D1).
  `check --du-bao` sau D1: chưa đo trên ứng viên. A7 bắt đo cả hai.
- Ruff: `KHÔNG ĐO ĐƯỢC` ở phiên soạn và ở mọi lượt review.
- Băm thân Mission Issue #682 ở phía nhận: `KHÔNG ĐO ĐƯỢC` (đường đọc MCP chuẩn hoá thực thể
  HTML); descriptor neo bằng số Issue + object ID `5627190292`.
- Lease T131 còn giữ `ops/lease_publish_test.py` là trạng thái đo 07:59Z 29-09; phải đo lại
  (`ai-dang-giu`) trước khi cấp lease cho `wp678`.
- Trạng thái máy chủ GitHub ngoài `ls-remote`: không đo (REST tới `repos/…` bị proxy chặn).
- Q3 đã được chủ kho xác nhận (#678 comment `5885268193`); không còn là câu hỏi mở.

## Phụ lục A — bộ quét lease của §8 và tự kiểm của nó

Bộ quét tham chiếu, dùng để ra các số ở §8. Nó là công cụ của phiên soạn, **không** phải mã sản
phẩm; A9 bắt lượt thi hành dựng helper tương đương có ca kiểm trong `ops/lease_publish_test.py`.
Giữ map ref→OID của lần liệt kê và đọc tree bằng OID, không đọc lại tên ref có thể trôi.
Kết quả chỉ chứng minh ảnh các OID đó; đối chiếu map với nguồn ref đầy đủ được cấp như A9,
không lấy số ref bằng nhau thay cho map bằng nhau. Số kiểu/ánh xạ tính theo cặp (blob,path);
số blob riêng phải ghi riêng, không suy hai mẫu số bằng nhau. Báo riêng miền lịch sử.
Tự kiểm bổ sung: đổi ref từ commit ID sai kiểu sang commit chuỗi ngay sau liệt kê; phép
quét phải vẫn đọc OID đã liệt kê và báo lỗi. Cùng blob ở live/retired phải báo đúng các
miền và cặp; map ref/OID phải có mặt. Kết quả chạy thật của các ca này nằm ở bảng cuối phụ lục.

```python
import subprocess, sys, yaml, re, json, os
from datetime import datetime, timezone
LID = re.compile(r"^[A-Za-z0-9._-]+$")
class KhongDoDuoc(Exception):
    pass
def git(*a, cwd):
    p = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True,
                       env={**os.environ, "LC_ALL": "C"})
    if p.returncode or "ignoring broken ref" in p.stderr or "ignoring ref with broken name" in p.stderr:
        raise KhongDoDuoc(f"git {' '.join(a)} rc={p.returncode}: {p.stderr.strip()[:200]}")
    return p.stdout
def quet(goc):
    dong = git("for-each-ref", "--format=%(objectname) %(refname) %(symref)", "refs/heads", "refs/remotes", cwd=goc)
    ref_map = {r: oid for oid, r, sym in (l.split(" ", 2) for l in dong.splitlines())
               if not (r.endswith("/HEAD") and sym)}
    refs = list(ref_map)
    blobs, cap, loi = {}, {}, []
    kieu, so_anh_xa, so_co_id = {}, 0, 0
    for ref in refs:
        for m in git("ls-tree", "-r", "-z", ref_map[ref], "--", "ops/leases/", "ops/leases_retired/", cwd=goc).split("\0"):
            if not m: continue
            meta, p = m.split("\t", 1)
            if not p.endswith((".yaml", ".yml")) or meta.split()[1] != "blob": continue
            blobs.setdefault(meta.split()[2], p)
            cap.setdefault((meta.split()[2], p), []).append(ref)
    for b, p in cap:
        try: d = yaml.safe_load(git("cat-file", "blob", b, cwd=goc))
        except yaml.YAMLError: loi.append((p, "parse")); continue
        if not isinstance(d, dict): loi.append((p, "khong_phai_anh_xa")); continue
        so_anh_xa += 1
        if "lease_id" not in d: loi.append((p, "thieu_lease_id")); continue
        so_co_id += 1
        v = d["lease_id"]
        ten_kieu = type(v).__name__
        kieu[ten_kieu] = kieu.get(ten_kieu, 0) + 1
        if not isinstance(v, str) or not LID.fullmatch(v): loi.append((p, f"lease_id={v!r}"))
        t = d.get("thay_the_cho")
        if t not in (None, "") and not (isinstance(t, str) or (isinstance(t, list) and all(isinstance(x, str) and x.strip() for x in t))):
            loi.append((p, "thay_the_cho"))
        t = d.get("da_bi_thay_the")
        if t not in (None, "") and (not isinstance(t, str) or not t.strip()):
            loi.append((p, "da_bi_thay_the"))
    return {"refs": ref_map, "ref_count": len(refs), "blob_count": len(blobs),
            "pair_count": len(cap), "mapping_count_pairs": so_anh_xa,
            "id_count_pairs": so_co_id, "type_counts_pairs": kieu,
            "areas": {area: {"pairs": sum(p.startswith(area + "/") for _, p in cap),
                              "blobs": len({b for b, p in cap if p.startswith(area + "/")})}
                      for area in ("ops/leases", "ops/leases_retired")},
            "pairs": [{"blob": b, "path": p, "refs": rs} for (b, p), rs in cap.items()],
            "errors": loi}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("cach dung: python quet.py <goc-kho>")
    try:
        if not os.path.isdir(sys.argv[1]):
            raise KhongDoDuoc(f"khong co thu muc {sys.argv[1]!r}")
        bao_cao = quet(sys.argv[1])
    except KhongDoDuoc as e:
        print(f"KHONG_DO_DUOC: {e}", file=sys.stderr)
        raise SystemExit(2)
    bao_cao["utc"] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(bao_cao, ensure_ascii=False, sort_keys=True))
    raise SystemExit(1 if bao_cao["errors"] else 0)
```

Lệnh tái lập: trích đúng khối Python ra scratch ngoài checkout, chạy
`PYTHONDONTWRITEBYTECODE=1 python <scratch>/quet.py <goc-kho>`. Cần cả JSON có map/đếm
và rc phù hợp: không lỗi ⇒ 0, lỗi lease ⇒ 1, lỗi Git/đầu vào (`KHÔNG ĐO ĐƯỢC`) ⇒ **2** —
tách khỏi 1 để "có lease hỏng" và "không đo được" không đọc lẫn nhau. stdout rỗng
không là bằng chứng dương. Kiểm chính entry point này bằng các fixture, không chỉ gọi
hàm rồi tự tính một biến mang tên rc. Tệp ngoài repo không tồn tại cũng phải khác 0.

Bảng cũ của r2 (đo 07:28Z 29-09) là lời khai lịch sử, không tái lập được bằng chạy nguyên
khối vì r2 không công bố wrapper sinh mã thoát. Bảng dưới là kết quả **thật**, đo 07:5xZ 29-09
qua entry point (`python quet.py <goc-kho>`), **mỗi ca một kho git tạm riêng** (dựng mọi ca
trong một kho thì từ ca thứ hai trở đi `rc=1` có thể do ca trước, tức không đo gì). Script
dựng ca là `tukiem_r3.sh` của phiên soạn, nằm ở thư mục scratch, **không** vào kho; output
gốc lưu ở `tukiem_r3.out` cạnh nó.

| ca | mong | được |
|---|---|---|
| đối chứng: một lease chuỗi hợp lệ | 0 | 0, `errors` rỗng |
| `lease_id: 1_000` trong tệp `.yml` | 1 | 1, `lease_id=1000` |
| thiếu `lease_id` | 1 | 1, `thieu_lease_id` |
| tài liệu là danh sách | 1 | 1, `khong_phai_anh_xa` |
| YAML hỏng | 1 | 1, `parse` |
| `da_bi_thay_the: [x]` | 1 | 1, `da_bi_thay_the` |
| `thay_the_cho: [""]` | 1 | 1, `thay_the_cho` |
| `thay_the_cho: ["   "]` | 1 | 1, `thay_the_cho` |
| `da_bi_thay_the: "   "` | 1 | 1, `da_bi_thay_the` |
| `thay_the_cho: []` (hợp lệ) | 0 | 0 |
| `lease_id: on` chỉ trên head cục bộ | 1 | 1, `lease_id=True`, `ref_count` 2 |
| `lease_id: yes` chỉ trên ref thường `topic/HEAD` | 1 | 1, `lease_id=True`, `ref_count` 2 |
| cùng blob ở `ops/leases` và `ops/leases_retired` | 0 | 0; blob 1, cặp 2; mỗi miền 1 blob / 1 cặp |
| ref hỏng (OID toàn 0) | 2 | 2, `KHONG_DO_DUOC` trên stderr, không JSON |
| thư mục kho không tồn tại | 2 | 2, `KHONG_DO_DUOC`, không JSON |
| ref đổi sang commit sạch NGAY SAU `for-each-ref` (seam chèn `update-ref` vào hàm `git`, gọi `quet()` trực tiếp) | báo lỗi | ref đã sang `d2a4d13` nhưng bộ quét đọc OID đã liệt kê `3c78354` và báo `lease_id=1000` |

Ca cuối là lý do bộ quét đọc `stderr` chứ không chỉ `rc`: git **bỏ lặng lẽ** một ref hỏng và vẫn
trả 0, tức một phép quét "mọi ref" có thể quét thiếu mà không báo.
