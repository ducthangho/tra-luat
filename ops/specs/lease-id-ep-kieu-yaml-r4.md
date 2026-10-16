# ĐẶC TẢ — `LEASE-ID-EP-KIEU-YAML` — **revision 4, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp678` (ID bền theo protocol §3.2, `wp<issue>`); tên đọc được: `LEASE-ID-EP-KIEU-YAML`. Hai tên chỉ cùng một packet; lease dùng `wp678` hoặc tên đọc được đều phải kèm `packet_issue: 678`. |
| `revision` | **4** |
| `thay_the_cho` | revision 3: `ops/specs/lease-id-ep-kieu-yaml-r3.md`, sha256 `64c67225335cf50b2a394ffda005e03d338ff545757b210640fd05ac14564af1`, commit `4c1915c`. Chuỗi lịch sử: revision 2 `ops/specs/lease-id-ep-kieu-yaml-r2.md`, sha256 `1575fb3e605b88e94d29e704789dcbaecbbcc3fb25e5c963796655b4d55d5715`, commit `aecdccd`; revision 1 `ops/specs/lease-id-ep-kieu-yaml-r1.md`, sha256 `578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c`, commit `342e62c7`. |
| `packet_issue` | **#678** |
| `mission_issue` | **#682** (Mission Issue, object ID `5627190292`, tạo 29-09-2026, tiêu đề *"Mission wp678: quyết định chủ kho + miễn trừ closure có phạm vi cho LEASE-ID-EP-KIEU-YAML"*). Issue này do **phiên agent đăng HỘ chủ kho** bằng credential chủ kho, nên `author_association: OWNER` không chứng minh chủ kho tự gõ; nguồn thẩm quyền là các câu trả lời của chủ kho trong phiên (Q0–Q6) được trích trong thân #682. Packet cha #579 (đặc tả `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md`) không khai `mission_issue` và không cấp ngoại lệ gì cho packet này. |
| `nguon_cap_viec` | Phát hiện phụ của #677 (mục *"Phát hiện phụ — TÁCH packet riêng"*). Chủ kho quyết định tách packet 29-09-2026, rồi trả lời *"Đồng ý"* trong phiên cho ba đề xuất: (a) mở Issue + soạn đặc tả; (b) chỉ nhận **chuỗi thật**, bỏ cả `int`; (c) xếp sau `T131-DEADLINE-DEM-SPAWN`. Q3 xác nhận riêng: #678 comment `5885268193`. **r2** là hệ quả của cross-review lượt 1 trên PR #679 (comment `5885578969`, VERDICT sha256 `d4acdd38…b8add`), dưới chỉ thị chủ kho *"cross-review #679 đi, theo phân lớp, không theo từng lỗi, có hint patch"*. **r3** là hệ quả của cross-review lượt 2 trên PR #679 (comment `5886034260`, VERDICT sha256 `aa9a68d3…d4882`: 1 P1 / 3 P2 / 1 P3 theo lớp), và của quyết định chủ kho chọn neo lớp P1 bằng Mission Issue mới (#682). **r4** là hệ quả của cross-review lượt 3 trên PR #679 (comment `5887068702`, VERDICT sha256 `1eb00c7a…7e819`: 0 P1 / 2 P2 / 1 P3 theo lớp; P1 của lượt 2 đã đóng). |
| `objective` | Mọi đường đưa `lease_id` vào danh tính chỉ nhận chuỗi thật khớp `LEASE_ID`, đóng va chạm do ép giá trị không phải chuỗi thành chuỗi. Danh tính là giá trị sau `yaml.safe_load`: các cách viết ra cùng một chuỗi hợp lệ cố ý là cùng danh tính (ví dụ `'yes'` và `!!str yes`), không yêu cầu phân biệt cú pháp YAML. |
| `review_class` | **`sensitive`**: chạm `ops/lease_publish.py`, tức cổng đăng lease. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` (Claude Opus 5.5, effort ≥ medium) |
| `environment` | **`cloud`**. Packet không đo hành vi phụ thuộc nền (không đồng hồ ngủ máy, không đường dẫn Windows); tiền lệ các đặc tả `ops/specs/*` cùng lớp khai `cloud`. Chủ kho đổi thì phải ra revision mới. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium) |
| `depends_on` | Trước khi cấp lease cho `wp678`, không lease nào còn hiệu lực được giữ `ops/lease_publish.py` hoặc `ops/lease_publish_test.py`; **đo lại lúc cấp** (`ai-dang-giu`), không nhận số dưới đây thay phép đo. Lease `t131-deadline-dem-spawn-exec-1-claude-20260929`: T131 **đã land** (PR #680, `89fc4fa`). Lịch sử, đo 07:59Z 29-09: `ai-dang-giu ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929`; `ai-dang-giu ops/lease_publish.py` ⇒ `NGƯỜI_GIỮ 0`. **Hiện tại, đo 09:44Z 29-09:** cả hai tệp ⇒ `NGƯỜI_GIỮ 0: không có`, rc=0; lease T131 hiện ở nhãn `HẾT_HẠN` (tệp lease ở `refs/remotes/origin/claude/bookkeeping-676` khai `lease_expires_at_utc: 2026-09-29T08:15:00Z`). Điều kiện thu hồi của r3 không còn là điều kiện chặn ở thời điểm đo này, nhưng phải đo lại vì người giữ có thể đổi. |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518` (PR #680, T131 land). Đây là **nền bất biến** để đo diff và nghiệm thu. r1 và r2 dùng `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; packet CHƯA thi hành, chưa có diff hay lịch sử finding trên mã, nên việc dời nền ở r3 là quyết định bền (chính r3) theo protocol §3.2.1, không phải dùng HEAD mới để xoá diff. r4 **giữ nguyên** nền của r3: `git fetch` rồi `git rev-parse origin/master` đo 09:44Z 29-09 vẫn ra `89fc4fac8cea65979cc2483043dc8cd07a6e8518`. `ops/lease_publish.py` giống hệt giữa hai nền (`git diff --quiet` rc=0), nên các phép đo §1/§2 làm trên `1741e0a` vẫn hợp lệ; chỉ `ops/lease_publish_test.py` đổi (+13/−19, bốn hunk: hai trong t131, một trong t139, một trong t192). Nền tiếp nối (continuation base), nếu khác, phải được khai riêng lúc cấp lease, không thay nền này. |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/lease-id-ep-kieu-yaml-r4.md`, không loại dòng nào. Giá trị được công
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

Không đường dẫn nào khác. Riêng đặc tả này (`ops/specs/lease-id-ep-kieu-yaml-r4.md`, và các bản r1, r2, r3 nó thay) là hồ sơ
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
  khai `revision 0`, đo 06:2xZ 29-09; vẫn chưa có đặc tả đóng băng tại 07:59Z 29-09, nội dung nghĩa vụ hai thứ tự dưới đây không đổi). Cập nhật đo 09:45Z 29-09: tệp `ops/specs/dot-bien-l-bien-cong-khai-r1.md` (sha256 `81468e21c7a7d32167d210b17813dab2b825992a1587b86d8bc8b3dc9142a4da`) đã có ở `refs/remotes/origin/claude/spec-dot-bien-l-bien-cong-khai-20260929` (`c78a5d06`), chưa có trên master; trạng thái đóng băng và lease của nó không đo ở lượt này, nên packet này vẫn không neo acceptance nào vào nó.
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

Đo lại 09:44Z 29-09-2026 trong container phiên soạn, kho đã `--unshallow` (`git rev-parse
--is-shallow-repository` ⇒ `false`). Số của r1, r2, r3 và của các lượt cross-review giữ dưới
nhãn lịch sử, không dùng làm số hiện tại.

- **Nền.** `git fetch -q origin '+refs/heads/*:refs/remotes/origin/*'` rồi `git rev-parse
  origin/master`, đo 09:04Z và 09:44Z: cả hai lần `89fc4fac8cea65979cc2483043dc8cd07a6e8518`.
  Nền nghiệm thu không phải dời. `git diff --quiet origin/master -- ops/lease_publish.py
  ops/lease_publish_test.py` ⇒ rc=0 (09:46Z).
- **Ref.** `git ls-remote --heads origin` (hỏi máy chủ) so `git for-each-ref
  refs/remotes/origin` (đọc đệm), theo **tập tên**, bỏ `HEAD`, `comm -23` và `comm -13`:
  **510 = 510**, thiếu 0, thừa 0 (09:44Z, sau `fetch`). `refs/replace` hiện có 0 ref.
  Lịch sử: 503 ở r1 (06:1xZ); 505 ở r2 (07:2xZ); 506 = 506 ở r3 (07:59Z).
- **Người giữ** (09:44Z). `python ops/lease_publish.py ai-dang-giu ops/lease_publish.py` ⇒
  `NGƯỜI_GIỮ 0: không có`, rc=0; `ai-dang-giu ops/lease_publish_test.py` (dòng cuối) ⇒
  `NGƯỜI_GIỮ 0: không có`, rc=0. Không gặp `CHẶN [12]` (master cục bộ và `origin/master` cùng
  `89fc4fac`). Lease T131 hiện ở nhãn `HẾT_HẠN` (xem `depends_on`).
  Lịch sử 07:59Z: `ai-dang-giu ops/lease_publish.py` ⇒ `NGƯỜI_GIỮ 0`;
  `ai-dang-giu ops/lease_publish_test.py` ⇒ `NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929`.
- **Quét lease** bằng đúng khối mã ở **Phụ lục A** (bản r4, đã áp HINT lượt 3), chạy qua entry
  point: `PYTHONDONTWRITEBYTECODE=1 python3 quet_r4.py /home/user/tra-luat`, JSON `utc`
  `2026-09-29T09:44:23.898266+00:00`, rc=0: `ref_count` **512** (510 `refs/remotes` + 2
  `refs/heads`), `blob_count` **563**, `pair_count` **563**, `mapping_count_pairs` **563**,
  `id_count_pairs` **563**, `type_counts_pairs` `{str: 563}`, `areas`: `ops/leases` 563 blob /
  563 cặp, `ops/leases_retired` 0 blob / 0 cặp, `errors` **0**.
  `ops/leases_retired` = 0 trên mọi ref là số **đo**, không phải giả định.
  Lịch sử r3 (07:59:26Z, khối mã r3): rc=0, `ref_count` 508 (506 + 2), 562 blob / 562 cặp /
  562 ánh xạ / 562 có ID, `{str: 562}`, `errors` 0. Chênh r3 → r4: ref +4 (đều `refs/remotes`,
  khớp 506 → 510 của `ls-remote`), blob +1; vì sao 4 ref mới chỉ thêm 1 blob thì chưa truy nguyên
  (`KHÔNG ĐO ĐƯỢC`, không đổi kết luận vì mọi `lease_id` đều là chuỗi). Lịch sử xa hơn: 559 ở r1
  và lượt 1; 560 ở r2 (sau `fetch` 07:21Z), khi hai nhánh đẩy sau lượt `fetch` trước đó
  (`ops/cap-lease-ci-duong-nhanh-ho-so`, `ops/cap-lease-ci-g5-cong-cu-chia-manh`) mỗi nhánh thêm
  một tệp lease so với master mà tổng chỉ tăng 1 blob. Đây là trôi số của L5 xảy ra ngay trong
  lúc soạn, và nó lặp lại ở r4.
- **Suite.** Nền hiện tại: **187/187**, rc=0, bỏ qua 0, đo 08:0xZ 29-09 trên commit merge
  `589336f` (cây `89fc4fa` + tệp spec), `PYTHONDONTWRITEBYTECODE=1 python ops/lease_publish_test.py`
  với `shellcheck` 0.9.0 + `actionlint` 1.7.7. Không đo lại ở r4 (hai tệp Python giống hệt
  `origin/master`, xem mục **Nền**).
  Lịch sử trên `1741e0a`: r1 khai 185/187 lúc container thiếu `shellcheck` (`t137`, `t159` báo
  `KHÔNG ĐO ĐƯỢC: thiếu shellcheck`); lượt 1 đo 187/187.
- **Kích thước** (09:46Z, `git show origin/master:<tệp> | wc -l`). `ops/lease_publish.py` 2206
  dòng (không đổi giữa hai nền); `ops/lease_publish_test.py` **10502** dòng trên `89fc4fa`
  (10508 trên `1741e0a`); 187 ca, số ca lớn nhất `t192` (đo 08:0xZ, không đo lại).
- **Ruff**: vẫn `KHÔNG ĐO ĐƯỢC` ở phiên soạn (module vắng trong sandbox);
  A8 bắt lượt thi hành đo cả hai vế.

Mọi con số trên phải được **đo lại** trước mỗi bước công bố: đăng băm/revision, cấp lease
và land (L5). Ghi thời điểm đầy đủ và lệnh cạnh số mới; giữ số cũ với nhãn lịch sử nếu cần.
Quyết định neo vào **bất biến** (mọi `lease_id` là chuỗi; không lease nào còn hiệu lực giữ hai
tệp của write set lúc cấp), không neo vào con số 510/563.

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: đây không phải packet khắc phục một lượt thất bại. Nguồn là một phát hiện phụ
của #677, không kèm bộ đếm hình dạng lỗi nào.

Rủi ro hình dạng đã biết, ghi để lượt thi hành canh: *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ
BA"*. §2 liệt kê 8 đường sửa (D1–D8) cộng D9 chỉ hiển thị; lượt thi hành phải **grep lại** chứ không tin bảng này là
đủ, và khai đường nào mới tìm thấy.

**Bộ đếm hình dạng (phát sinh trong chuỗi review của chính đặc tả này).** Lớp `bo-quet-*`, tức
bộ quét tham chiếu ở Phụ lục A, có mặt ở **cả 3 lượt** review (đếm hình dạng, đừng chỉ đếm lỗi):

| lượt | bản được review | biểu hiện của lớp `bo-quet-*` |
|---|---|---|
| 1 | r1 | thiếu miền |
| 2 | r2 | thiếu miền; không neo ảnh; không có cửa chạy |
| 3 | r3 | không neo ảnh (`git replace`); cửa chạy phân loại lỗi còn hở |

Mỗi bản vá đều đúng chỗ được chỉ, và lần nào lượt sau cũng ra một biểu hiện khác của cùng lớp.
r4 vá đúng hai biểu hiện lượt 3 chỉ ra (tắt replace ở mọi lệnh Git; một biên CLI phân loại
mọi lỗi chưa biết thành `KHONG_DO_DUOC`, rc=2) và chạy thật mọi ca ở Phụ lục A; đó là bằng chứng
cho hai biểu hiện ấy, **không** phải lời khai rằng lớp đã sạch.

**Điều kiện dừng, đã đăng ký trước** trên PR #679 (comment `5887068702`): nếu lượt 4 còn ra
một lớp `bo-quet-*`, thì r5 **GỠ mã bộ quét khỏi đặc tả**; §8 hạ số quét xuống "tham khảo,
không phải cổng"; cổng là helper A9 có ca kiểm trong `ops/lease_publish_test.py`.

## 10. `chua_do_duoc`

- Mã thực thi chưa tồn tại, nên mọi tiêu chí A1–A10 mới được kiểm **khả thi**: hai lượt
  cross-review đã dựng mô hình chốt tạm trên bản sao để kiểm A1–A10; vẫn **chưa có ứng viên
  thật**.
- Đường `DU_BAO`: lượt 1 đo được `ai-dang-giu --du-bao` đưa `int` tới :1967 (không qua D1).
  `check --du-bao` sau D1: chưa đo trên ứng viên. A7 bắt đo cả hai.
- Ruff: `KHÔNG ĐO ĐƯỢC` ở phiên soạn và ở mọi lượt review.
- Băm thân Mission Issue #682 ở phía nhận: `KHÔNG ĐO ĐƯỢC` (đường đọc MCP chuẩn hoá thực thể
  HTML); descriptor neo bằng số Issue + object ID `5627190292`.
- Lease T131 còn giữ `ops/lease_publish_test.py` là trạng thái đo 07:59Z 29-09 (lịch sử);
  đo 09:44Z 29-09 cả hai tệp `NGƯỜI_GIỮ 0` và lease T131 ở nhãn `HẾT_HẠN`. Vẫn phải đo lại
  (`ai-dang-giu`) trước khi cấp lease cho `wp678`.
- Bộ quét Phụ lục A: các ca ở bảng cuối đều đã CHẠY (28 ca CLI của r4 không lệch mong đợi, cộng
  1 ca race gọi `quet()` trực tiếp). Còn `KHÔNG ĐO ĐƯỢC`: timeout, OS kill, hết bộ nhớ; Python
  khác 3.11.15; PyYAML khác 6.0.1; ngưỡng độ sâu và kích thước (chỉ thử 5000 lớp và 400026 byte).
  Script và output của các phép đo ở thư mục scratch của phiên soạn, không vào kho.
- Tệp `ops/specs/dot-bien-l-bien-cong-khai-r1.md` của #677 có trên nhánh
  `claude/spec-dot-bien-l-bien-cong-khai-20260929` (đo 09:45Z); trạng thái đóng băng và lease
  của nó không đo ở lượt này (xem A2).
- Trạng thái máy chủ GitHub ngoài `ls-remote`: không đo (REST tới `repos/…` bị proxy chặn).
- Q3 đã được chủ kho xác nhận (#678 comment `5885268193`); không còn là câu hỏi mở.

## Phụ lục A — bộ quét lease của §8 và tự kiểm của nó

Bộ quét tham chiếu, dùng để ra các số ở §8. Nó là công cụ của phiên soạn, **không** phải mã sản
phẩm; A9 bắt lượt thi hành dựng helper tương đương có ca kiểm trong `ops/lease_publish_test.py`.
Giữ map ref→OID của lần liệt kê và đọc tree bằng OID, không đọc lại tên ref có thể trôi.
Tắt Git replace ở MỌI lệnh Git của phép đo: OID phải chỉ đúng object gốc, không phải
object do refs/replace hoặc GIT_REPLACE_REF_BASE thay thế. Khóa bằng ca Git tạm có
commit thay thế và ca blob thay thế: map giữ OID chứa ID sai kiểu thì vẫn phải rc=1,
kể cả khi replacement chứa chuỗi hợp lệ; đối chứng không replacement giữ nguyên kết quả.
Kết quả chỉ chứng minh ảnh các OID đó; đối chiếu map với nguồn ref đầy đủ được cấp như A9,
không lấy số ref bằng nhau thay cho map bằng nhau. Số kiểu/ánh xạ tính theo cặp (blob,path);
số blob riêng phải ghi riêng, không suy hai mẫu số bằng nhau. Báo riêng miền lịch sử.
Tự kiểm bổ sung: đổi ref từ commit ID sai kiểu sang commit chuỗi ngay sau liệt kê; phép
quét phải vẫn đọc OID đã liệt kê và báo lỗi. Cùng blob ở live/retired phải báo đúng các
miền và cặp; map ref/OID phải có mặt. Kết quả chạy thật của các ca này nằm ở bảng cuối phụ lục.

```python
import subprocess, sys, re, json, os
from datetime import datetime, timezone
LID = re.compile(r"^[A-Za-z0-9._-]+$")
class KhongDoDuoc(Exception):
    pass
def git(*a, cwd):
    p = subprocess.run(["git", "--no-replace-objects", *a], cwd=cwd, capture_output=True, text=True,
                       env={**os.environ, "LC_ALL": "C"})
    if p.returncode or "ignoring broken ref" in p.stderr or "ignoring ref with broken name" in p.stderr:
        raise KhongDoDuoc(f"git {' '.join(a)} rc={p.returncode}: {p.stderr.strip()[:200]}")
    return p.stdout
def quet(goc):
    import yaml
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
    try:
        if len(sys.argv) != 2:
            raise KhongDoDuoc("cach dung: python quet.py <goc-kho>")
        if not os.path.isdir(sys.argv[1]):
            raise KhongDoDuoc(f"khong co thu muc {sys.argv[1]!r}")
        bao_cao = quet(sys.argv[1])
        bao_cao["utc"] = datetime.now(timezone.utc).isoformat()
        print(json.dumps(bao_cao, ensure_ascii=False, sort_keys=True))
    except Exception as e:
        # Biên CLI: lỗi chưa được phân loại không phải bằng chứng lease hỏng.
        # Không bắt BaseException (SystemExit/KeyboardInterrupt).
        print(f"KHONG_DO_DUOC: {type(e).__name__}: {str(e)[:200]}", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(1 if bao_cao["errors"] else 0)
```

Lệnh tái lập: trích đúng khối Python ra scratch ngoài checkout, chạy
`PYTHONDONTWRITEBYTECODE=1 python <scratch>/quet.py <goc-kho>`. Cần cả JSON có map/đếm
và rc phù hợp: không lỗi ⇒ 0, lỗi lease ⇒ 1, lỗi Git/đầu vào (`KHÔNG ĐO ĐƯỢC`) ⇒ **2** —
tách khỏi 1 để "có lease hỏng" và "không đo được" không đọc lẫn nhau. Chỉ rc=1 KÈM
JSON đầy đủ và errors khác rỗng mới là bằng chứng lỗi lease. Lỗi môi trường/giải mã,
constructor YAML ném ngoại lệ ngoài YAMLError, vượt khả năng parser/tài nguyên hoặc
lỗi chưa phân loại ⇒ 2/KHONG_DO_DUOC, không gán cho lease. Quy tắc 0/1/2 áp cho
lượt CLI kết thúc có kiểm soát; nếu timeout, OS kill hoặc không đọc được output thì
caller ghi KHÔNG ĐO ĐƯỢC, không biến mã thoát thô ấy thành kết luận về lease. stdout rỗng
không là bằng chứng dương. Kiểm chính entry point này bằng các fixture, không chỉ gọi
hàm rồi tự tính một biến mang tên rc. Tệp ngoài repo không tồn tại cũng phải khác 0.
Kết quả chạy của các ca bổ sung (thiếu/thừa argv, Git/PyYAML vắng, blob không giải mã được,
ngày không tồn tại, số vượt giới hạn chuyển đổi, tài liệu quá sâu, replace commit/blob, đối
chứng) nằm ở hai bảng dưới; mỗi dòng ghi riêng loại ngoại lệ, rc và sự hiện diện JSON, không
nhận chỉ nonzero làm đạt.

**Lịch sử.** Bảng r2 (đo 07:28Z 29-09) là lời khai không tái lập được (r2 không công bố wrapper
sinh mã thoát). Bảng r3 (07:5xZ 29-09) có 15 ca CLI cộng 1 ca race, cả 15 ca CLI khớp mong đợi;
15 ca ấy được chạy lại nguyên ở r4 và cho cùng rc và cùng loại lỗi. Bảng r3 không có ca replace,
argv, Git/PyYAML vắng, giải mã, ngày, số, độ sâu; hai P2 của lượt 3 nằm đúng ở các miền đó.

**Phép đo 1 — CLI.** Đo 09:43:32Z–09:43:37Z 29-09 (Python 3.11.15, PyYAML 6.0.1, git 2.43.0).
Khối mã ở trên được trích đúng byte từ chính tệp này ra `quet_r4.py`; script `tukiem_r4.sh`
(mở rộng từ `tukiem_r3.sh`) chạy `python3 quet_r4.py <kho>` cho từng dòng, **mỗi ca một kho git
tạm riêng** (dựng mọi ca trong một kho có thể để lỗi ca trước làm ca sau đỏ, nên không dùng cách
đó để chứng nhận ca độc lập). Output gốc: `tukiem_r4.out`. Script và output nằm ở thư mục scratch
của phiên soạn, **không** vào kho. 28 ca của r4 (15 kế thừa + 13 mới) và 2 lần chạy khối mã r3
trên kho replace làm đối chứng độ răng. Mọi dòng có rc=2 đều có stdout rỗng, không JSON, và
dòng stderr `KHONG_DO_DUOC: <Loại>`.

| ca | mong | được (rc, JSON?, errors hoặc loại lỗi) |
|---|---|---|
| đối chứng: một lease chuỗi hợp lệ | 0 | 0, JSON, `errors` rỗng |
| `lease_id: 1_000` trong tệp `.yml` | 1 | 1, JSON, `lease_id=1000` |
| thiếu `lease_id` | 1 | 1, JSON, `thieu_lease_id` |
| tài liệu là danh sách | 1 | 1, JSON, `khong_phai_anh_xa` |
| YAML hỏng | 1 | 1, JSON, `parse` |
| `da_bi_thay_the: [x]` | 1 | 1, JSON, `da_bi_thay_the` |
| `thay_the_cho: [""]` | 1 | 1, JSON, `thay_the_cho` |
| `thay_the_cho: ["   "]` | 1 | 1, JSON, `thay_the_cho` |
| `da_bi_thay_the: "   "` | 1 | 1, JSON, `da_bi_thay_the` |
| `thay_the_cho: []` (hợp lệ) | 0 | 0, JSON, `errors` rỗng |
| `lease_id: on` chỉ trên head cục bộ | 1 | 1, JSON, `lease_id=True`, `ref_count` 2 |
| `lease_id: yes` chỉ trên ref thường `topic/HEAD` | 1 | 1, JSON, `lease_id=True`, `ref_count` 2 |
| cùng blob ở `ops/leases` và `ops/leases_retired` | 0 | 0, JSON; blob 1, cặp 2; mỗi miền 1 blob / 1 cặp |
| ref hỏng (OID toàn 0) | 2 | 2, không JSON, `KhongDoDuoc` (git for-each-ref) |
| thư mục kho không tồn tại | 2 | 2, không JSON, `KhongDoDuoc` |
| **replace commit**: `main` trỏ commit X (`lease_id: 1_000`), `git replace X Y` với Y mang `lease_id` chuỗi hợp lệ (`refs/replace` có 1 ref) | 1 | 1, JSON, `lease_id=1000` |
| đối chứng, cùng kho, **khối mã r3** (không tắt replace) | r3 âm giả | 0, JSON, `errors` rỗng (đúng âm giả lượt 3 nêu) |
| đối chứng, cùng dựng nhưng KHÔNG replace | 1 | 1, JSON, `lease_id=1000` |
| **replace blob**: blob chứa `lease_id: 1_000` bị `git replace` bằng blob sạch | 1 | 1, JSON, `lease_id=1000` |
| đối chứng, cùng kho, **khối mã r3** | r3 âm giả | 0, JSON, `errors` rỗng |
| thiếu argv (không đối số) | 2 | 2, không JSON, `KhongDoDuoc` (cách dùng) |
| thừa argv (2 đối số) | 2 | 2, không JSON, `KhongDoDuoc` (cách dùng) |
| PyYAML vắng (`yaml.py` giả ném `ImportError` đặt ở `PYTHONPATH`) | 2 | 2, không JSON, `ImportError` |
| git vắng (`PATH` là thư mục rỗng, python gọi bằng đường dẫn tuyệt đối) | 2 | 2, không JSON, `FileNotFoundError` |
| blob không phải UTF-8 (`lease_id: ` rồi hai byte 0xFF 0xFE, dựng bằng `printf`) | 2 | 2, không JSON, `UnicodeDecodeError` |
| `lease_id: 2026-02-30` (ngày không tồn tại) | 2 | 2, không JSON, `ValueError` (day is out of range for month) |
| `lease_id` là số 5000 chữ số | không định trước; HINT dự kiến 2 | 2, không JSON, `ValueError` (Exceeds the limit (4300 digits) for integer string conversion) |
| tài liệu 5000 lớp `[` lồng nhau | không định trước; HINT dự kiến 2 | 2, không JSON, `RecursionError` |
| đối chứng: YAML lỗi thông thường (`lease_id: [`) | 1 | 1, JSON, `parse` |
| đối chứng: tệp lease hợp lệ 400026 byte (khoá `ghi_chu` dài) | 0 | 0, JSON, `errors` rỗng |

**Không có ca nào lệch mong đợi** (0/28 ca r4; hai lần chạy khối mã r3 cho 0 đúng như lượt 3
báo). Giới hạn của phép đo: ngưỡng 4300 chữ số là của CPython 3.11 và `RecursionError` phụ thuộc
giới hạn đệ quy mặc định, chưa đo phiên bản Python khác; chưa thử timeout, OS kill hay hết bộ
nhớ (caller phải coi output thiếu là KHÔNG ĐO ĐƯỢC, xem trên); độ sâu chỉ thử 5000 lớp và kích
thước chỉ thử 400026 byte, không suy ra ngưỡng.

**Phép đo 2 — race.** Đo 09:43:57Z 29-09. Script `race_r4.py` nạp `quet_r4.py`, dựng kho tạm
(`main` trỏ commit `lease_id: 1_000`, một commit sạch riêng), chèn `git update-ref` vào hàm
`git` của module ngay sau lần `for-each-ref` đầu tiên, rồi gọi `quet()` **trực tiếp**. Đây là
phép đo tại seam: nó **không** chứng minh mã thoát CLI và không nằm trong `tukiem_r4.sh`. Output
gốc: `race_r4.out`, cùng thư mục scratch, không vào kho.

| ca | mong | được |
|---|---|---|
| ref đổi sang commit sạch NGAY SAU `for-each-ref` (seam, gọi `quet()` trực tiếp) | map giữ OID cũ; `errors` có `lease_id=1000` | seam đã chèn; ref đã sang commit sạch `8dce401e`, nhưng `refs` vẫn giữ OID cũ `cdeca03d` và `errors` = `lease_id=1000` |

Lần chạy đầu của `race_r4.py` (09:43:53Z) in `False` ở dòng tự kiểm cuối vì script so tuple với
list, một lỗi của chính phép so trong script chứ không phải của khối mã (map và `errors` đã
đúng ở lần đó); phép so được sửa và chạy lại, `race_r4.out` là output của lần chạy lại.

Ca ref hỏng (OID toàn 0) là lý do bộ quét đọc `stderr` chứ không chỉ `rc`: git **bỏ lặng lẽ** một ref hỏng và vẫn
trả 0, tức một phép quét "mọi ref" có thể quét thiếu mà không báo.
