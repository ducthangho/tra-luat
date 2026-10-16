# ĐẶC TẢ — `THU-HOI-LEASE-A1a` — **revision 1, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `THU-HOI-LEASE-A1a` (nửa **mã** của slice A1; nửa **cấu hình** là `THU-HOI-LEASE-A1b`) |
| `revision` | 1 |
| `packet_issue` | **CHƯA ĐĂNG** — đặc tả không cấp việc (soan-spec §5). Issue + lease còn hiệu lực mới giao được. |
| `nguon_cap_viec` | Spec cha **r9** `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md`, sha256 `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79` (đo lại 06:37Z 20-09-2026 trên `origin/master` `a270aea`, khớp), §`write_set` dòng **A1** · Issue **#499** §A (A2) và §B (B1–B5) · quyết định chủ kho vòng 1 mở tại `#499` comment `5748147306` |
| `review_class` | **`sensitive`** — `ops/lease_publish.py` là cổng đọc lease (protocol §8). Vế đo được của ADR-0044:5 — 3 tệp ≤ trần 3 tệp; **dòng thêm là ƯỚC, chưa đo** (xem `chua_do_duoc` #1). |
| `thay_the_cho` | không — bản nháp 0 `ops/specs/THU-HOI-LEASE-A1.md` **không** có băm, chưa từng được lease nào neo ⇒ không phải revision kế tục, là **tách phạm vi** theo Q5. |

**GIỚI HẠN LỜI KHAI:** mọi khẳng định trong tệp này chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — trạng thái thứ ba làm cổng ĐỎ, không làm tròn thành hai.

---

## 0. Bốn quyết định của chủ kho — vòng 1 đã đóng

Mỏ neo bền: `#499` comment [`5748147306`](https://github.com/ducthangho/tra-luat/issues/499#issuecomment-5748147306)
(bản chiếu do phiên agent đăng hộ) · `#571` comment [`5748145023`](https://github.com/ducthangho/tra-luat/pull/571#issuecomment-5748145023).

| câu | quyết định | hệ quả trong đặc tả này |
|---|---|---|
| **Q2** — schema ADR-0047 lớp 2 | **Hai tầng** như khuyến nghị | `M1` — tầng BẮT BUỘC vào digest, tầng AUDIT ra ngoài digest |
| **Q4** — Q7/ADR-0044 cho A0 | **Chấp nhận ngoại lệ, không tách hồi tố** | A0 đóng; A1a **không** kế thừa ngoại lệ ấy — trần của A1a đo riêng |
| **Q5** — tách A1 | **Tách — hai spec, hai băm** | `M-F` (bật cờ) **ra khỏi** đặc tả này, sang `A1b` |
| **Q6** — va chạm write set với #570 | **Hỏi phiên #570 nhả sớm** | lease A1a chỉ cấp được sau khi `ops/lease_publish_test.py` hết người giữ |

**Q1** (SHA 40-hex của `actions/upload-artifact`) và **Q3** (sha256 thân comment `5575587924`) **vẫn MỞ**.
Chừng nào chưa có giá trị thì **M-A** và **M-C** không đóng được — chúng nằm ở `ngoai_pham_vi`, và
đặc tả này **không bịa** một SHA hay một băm để lấp ô trống.

## 1. Số đo — `origin/master` `a270aea`, đo **06:36–06:40Z 20-09-2026**

```
ops/lease_publish.py:929   SO_THU_HOI_KICH_HOAT = False
ops/lease_publish.py:937   PROFILE_ADAPTER_DA_DUYET: frozenset = frozenset()     # RỖNG ⇒ mọi discovery production 12
ops/lease_publish.py:939   BIA_MO_LICH_SU: tuple = ()
ops/lease_publish.py:943   DESCRIPTOR_Q13_SHA256 = None
ops/lease_publish.py:948   NGAN_SACH_MAC_DINH = {...}      # tự khai: "ĐỀ XUẤT của reviewer lượt 6, CHƯA đo trên roots production"
ops/lease_publish.py:1253  def hoso_adapter_do(...)        # 9 khoá, schema_version = 1
ops/lease_publish.py:1272  _HOSO_KHOA = (...)              # 9 tên — phép so TẬP KHOÁ khít
ops/lease_publish.py:1276  def kiem_mien_ho_so(...)        # miền TRƯỚC, digest SAU
ops/lease_publish.py:1302  def bam_ho_so(...)              # digest = sha256(JSON toàn bộ dict)
ops/lease_publish.py:1717  def _doc_blob_text_12(...)      # B2: chưa bắt OSError
ops/lease_publish.py:1757  def _du_bao_check(...)          # B1: đọc bản ghi qua GOI_GIT không đỡ decode
ops/lease_publish.py:1459  KhoObject.doc(...)              # B4: 3 fd ống ở đường deadline (Popen :1477)
ops/lease_publish.py:1016  kiem_ban_ghi_thu_hoi(..., bay_gio=None)   # B5: clock per-record; caller M4 tại :1864
.github/workflows/ops-thu-hoi-admission.yml:147  uses: actions/upload-artifact@v4   # M-A, vẫn TAG
```

`MOC_BIA_MO_LICH_SU` **chưa tồn tại** trong `ops/lease_publish.py` (grep toàn kho: chỉ thấy trong
`ops/reviews/thu-hoi-lease-va-cap-lai-spec/*` — tức trong đặc tả, chưa trong mã). M-D phải **tạo** nó.

| đường dẫn | dòng (master) | `ai-dang-giu` 06:36Z |
|---|---|---|
| `ops/lease_publish.py` | 2042 | `rc=0` · **NGƯỜI_GIỮ 0** |
| `ops/lease_publish_test.py` | 7043 · **166** ca | `rc=11` · **NGƯỜI_GIỮ 1** — `wp570-bash-nen-r2-g2-claude`, hết hạn `2026-09-21T01:55:00Z` |
| `.github/workflows/ops-thu-hoi-admission.yml` | 152 | `rc=0` · **NGƯỜI_GIỮ 0** |
| `ops/specs/THU-HOI-LEASE-A1a.md` | — | `rc=0` · NGƯỜI_GIỮ 0 |

Tập tên ref hai nguồn so bằng `comm -23` / `comm -13` (KHÔNG bằng `wc -l`): **473 / 473, cả hai chiều rỗng**
⇒ phép quét lease không mù vì thiếu ref.

## 2. Năm tiền đề của bản nháp 0 ĐÃ TRÔI (L5) — đo lại, hai chiều

| bản nháp 0 (11-09-2026) | đo lại 06:2x–06:40Z 20-09-2026 | chiều |
|---|---|---|
| cả ba đường `NGƯỜI_GIỮ 0` | `ops/lease_publish_test.py` **NGƯỜI_GIỮ 1** (`wp570-bash-nen-r2-g2-claude`) | **xấu đi** — chặn MỚI |
| `ops-thu-hoi-admission.yml` *"không bao giờ xanh"* ⇒ phụ thuộc cứng | **`success`** trên master `a270aea` và trên cả hai lượt của PR #575 (run `35494084038`) | tốt lên |
| `M9-FETCH-AUTH` chưa land ⇒ `depends_on` cứng | **ĐÃ LAND** — packet #503, `fe05fa6`, PR #505 | tốt lên |
| canary raw response *"chưa có vì C2a"* | **CÓ** — artifact `thu-hoi-receipt-12d8638e…-1`, 1081 B, `sha256:4506fd35…`, run `35494084038` | tốt lên |
| `upload-artifact` ở dòng **136** | dòng **147**, vẫn là TAG `@v4` | trôi vị trí, bản chất không đổi |

Bài học chép vào đây vì nó là lý do đặc tả này tồn tại ở dạng đã đo lại: **một con số đúng lúc viết
vẫn sai lúc người khác đọc**, và bốn trong năm dòng trên trôi theo chiều **làm nhẹ** việc — tức nếu
không đo lại thì A1a sẽ mang một `depends_on` đã chết và một `chua_do_duoc` đã hết hạn.

Trớ trêu đáng ghi: packet sinh ra để chữa *"lease không tự chết khi packet đã land"*
(nợ `AG-T0-01B`) đang **bị chặn bởi đúng cái nợ ấy** — `wp570` giữ một đường dẫn của nó.

## 3. `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
.github/workflows/ops-thu-hoi-admission.yml
```

Đúng ba đường, không ký tự đại diện. Hiện vật review (`ops/reviews/**`) và bookkeeping
(`CHANGELOG.md`, `RELEASE_MANIFEST.json`) **KHÔNG** trong write set — đi nhánh bookkeeping riêng
theo tiền lệ #551/PR #567 và #565/PR #575.

## 4. `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| **M-A** — ghim `actions/upload-artifact` bằng SHA 40-hex | **Q1 chưa có giá trị.** Container không readback được kho ngoài (REST tới `repos/…` bị proxy chặn 403, đo hai lần trong phiên 20-09); ADR-0047 cấm executor tự chọn mỏ neo. |
| **M-C** — `DESCRIPTOR_Q13_SHA256` | **Q3 chưa có giá trị.** Đường MCP trả thân comment **đã chuẩn hoá thực thể HTML** (đo 22-08-2026) ⇒ băm qua MCP là băm của một chuỗi KHÁC. Cần client thứ hai. |
| **M-F** — `SO_THU_HOI_KICH_HOAT = True` | Q5: sang **A1b**. Điều kiện Q10(d) (required check + strict up-to-date + chặn bypass) là cấu hình NGOÀI kho, chỉ chủ kho làm được. |
| Duyệt giá trị đầu tiên vào `PROFILE_ADAPTER_DA_DUYET` | ADR-0047 lớp 2: *"executor không tự duyệt"*, và **cấm** đo profile từ deployment tuỳ ý rồi tự đăng ký trong cùng lượt chạy. A1a **mở schema**, không **đổ giá trị**. |
| Đổi trạng thái ADR-0047 `Proposed` → `Accepted` | Trạng thái ADR là quyết định chủ kho; đặc tả không tự promote (r9 S10 đã chốt). |
| Đo/chốt `NGAN_SACH_MAC_DINH` trên roots production | Tự khai là ĐỀ XUẤT chưa đo — mở một mặt trận khác, không thuộc A1a. |
| Sửa `ops/leases/**`, `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/**` | ngoài write set. |
| Gọi CI Windows / `workflow_dispatch` / re-run tay | Chỉ thị chủ kho đang hiệu lực: **`manual_ci_budget: 0`**. |

## 5. `muc_tieu` — mỗi dòng chiếu vào MỘT đường dẫn của `write_set` (L2)

| # | mục tiêu | đường dẫn | nguồn |
|---|---|---|---|
| **M1** | Schema hồ sơ adapter **hai tầng** (`schema_version: 2`): tầng **BẮT BUỘC** vào digest — `git_path`, `git_version`, `credential_helper` (đường dẫn chương trình thật hoặc `""`), `tls_thu_vien` (tên+phiên bản, vd `OpenSSL 3.x`), `http_sslCAInfo`/`http_sslCAPath`/`proxy`/`endpoint`, và `image_os`/`image_version` của runner; tầng **AUDIT-ONLY** ra **ngoài** digest — `git_sha256` và các băm nhị phân khác. | `ops/lease_publish.py` | #499 A2 · Q2 |
| **M2** | `bam_ho_so` băm **chỉ tầng bắt buộc**; `kiem_mien_ho_so` kiểm miền **cả hai tầng** nhưng chỉ tầng bắt buộc quyết định `12`. | `ops/lease_publish.py` | Q2 |
| **M3** | `image_os`/`image_version` là **ba trạng thái**: chuỗi · `None` (*"không phải runner"*, giá trị tường minh) · thiếu khoá ⇒ `12`. Mỏ neo đòi runner mà hồ sơ `None` ⇒ `12`. | `ops/lease_publish.py` | Q2, fail-close |
| **M4** | Tạo `MOC_BIA_MO_LICH_SU` = OID canonical của lần land A0 (`0721811…`, đã kiểm là **tổ tiên** của `master`, rc=0) và ghim `BIA_MO_LICH_SU` theo đúng miền mà `_du_bao_check` tiêu thụ (cặp `(cũ, mới)`). | `ops/lease_publish.py` | r9 A1 · #499 |
| **M5** | **B1** — `_du_bao_check` đỡ decode khi đọc bản ghi qua `GOI_GIT`. | `ops/lease_publish.py` | #499 B1 |
| **M6** | **B2** — `_doc_blob_text_12` bắt `OSError`, đối xứng `_ls_tree_z`. | `ops/lease_publish.py` | #499 B2 |
| **M7** | **B3** — consumer đọc marker/policy bằng **bytes thô** (không text-mode `\r\n`→`\n`) ở mọi chỗ có so băm. | `ops/lease_publish.py` | #499 B3 |
| **M8** | **B4/F13** — đóng đủ **3** fd ống ở đường deadline của `KhoObject.doc` khi thread kẹt `read`. | `ops/lease_publish.py` | #499 B4 |
| **M9** | **B5/F14** — **một** snapshot clock cho cả loạt M4: caller truyền `bay_gio` xuống `kiem_ban_ghi_thu_hoi`/`kiem_metadata_retired` thay vì mỗi lời gọi tự `datetime.now`. | `ops/lease_publish.py` | #499 B5 |
| **M10** | Mỗi M1–M9 có ca `t…` trong suite; suite giữ **N/N hai số BẰNG NHAU**. | `ops/lease_publish_test.py` | L3 |
| **M11** | `.github/workflows/ops-thu-hoi-admission.yml` giữ `actionlint` sạch sau mọi thay đổi; **không** đụng dòng `upload-artifact` (M-A ngoài phạm vi). | `.github/workflows/…` | M-A ở `ngoai_pham_vi` |

## 6. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A1** | `hoso_adapter_do()` trả `schema_version == 2` và **đúng tập khoá** của schema v2. | Đột biến giữ `schema_version = 1` ⇒ ca đích ĐỎ. Đột biến thêm **một** khoá lạ ⇒ `kiem_mien_ho_so` ném `12` ⇒ ca ĐỎ. |
| **A2** | `bam_ho_so` **không** đổi khi chỉ tầng AUDIT đổi. | Ca dựng hai hồ sơ khác nhau **đúng ở `git_sha256`** và đòi `bam_ho_so(a) == bam_ho_so(b)`. Đột biến đưa `git_sha256` trở lại dict được băm ⇒ ca ĐỎ. **Đây là chốt chống "mỏ neo chết mỗi tuần khi image runner cập nhật".** |
| **A3** | `bam_ho_so` **ĐỔI** khi bất kỳ khoá tầng BẮT BUỘC đổi. | Bảng tham số: mỗi khoá bắt buộc, đổi một giá trị ⇒ digest phải khác. Đột biến bỏ **một** khoá khỏi tập được băm ⇒ đúng ca ấy ĐỎ. Cặp A2/A3 phải ĐỎ **ngược chiều nhau** — chỉ một trong hai đỏ là bộ tương đương, không phải hai chốt. |
| **A4** | Ba trạng thái của `image_os`: chuỗi ⇒ qua · `None` ⇒ qua nhưng **không khớp** mỏ neo đòi runner · **thiếu khoá** ⇒ `12`. | Đột biến gộp `None` và thiếu-khoá thành một ⇒ ca "thiếu khoá" ĐỎ. Đột biến cho `None` khớp mỏ neo runner ⇒ ca "None không khớp" ĐỎ. |
| **A5** | `kham_pha_nguon` với `PROFILE_ADAPTER_DA_DUYET` **rỗng** vẫn ⇒ `12` trên đường production. | Đột biến cho mỏ neo rỗng đi tiếp ⇒ ca ĐỎ. Chốt này chứng minh A1a **không** tự duyệt nền. |
| **A6** | `MOC_BIA_MO_LICH_SU` là OID 40-hex và **là tổ tiên** của nhánh mặc định. | Đột biến ghim một OID không phải tổ tiên ⇒ ca ĐỎ. Đột biến ghim chuỗi 39 ký tự ⇒ ca ĐỎ. |
| **A7** | `_du_bao_check` nhận cặp trong `BIA_MO_LICH_SU` ⇒ `rc` dự báo 0; cặp **không** trong sổ lẫn `BIA_MO_LICH_SU` ⇒ `rc` dự báo 8. | Đột biến `any(...)` → `True` ⇒ ca "không có trong sổ" ĐỎ. Đột biến so **một** vế của cặp ⇒ ca "đúng lease cũ, sai lease mới" ĐỎ. |
| **A8** | **B1** — bản ghi chứa byte không decode được ⇒ đường `_du_bao_check` trả `12`, **không** ném `UnicodeDecodeError` trần. | Ca bơm byte `0x80` vào bản ghi. Đột biến bỏ `errors=`/`try` ⇒ ca ĐỎ vì kiểu ngoại lệ sai. **Phân hạng theo LỚP ngoại lệ riêng, không theo chuỗi thông điệp** (bài học #355/#359: một `except` đổi kiểu giả được chuỗi). |
| **A9** | **B2** — `_doc_blob_text_12` gặp `OSError` ⇒ `12`. | Ca tiêm `OSError` tại điểm đọc. Đột biến bỏ `except OSError` ⇒ ca ĐỎ vì ngoại lệ thoát ra ngoài. |
| **A10** | **B3** — nội dung có `\r\n` cho **cùng** băm ở consumer và ở nguồn. | Ca dựng blob CRLF. Đột biến quay về `read_text()` ⇒ ca ĐỎ vì băm lệch. |
| **A11** | **B4** — sau một lời gọi `KhoObject.doc` chết ở deadline, số fd của tiến trình **không tăng**. | Ca đo `len(os.listdir('/proc/self/fd'))` trước/sau (nền không có `/proc` ⇒ ghi **KHÔNG ĐO ĐƯỢC** và ca ĐỎ, không bỏ qua êm). Đột biến bỏ **một** trong ba `close()` ⇒ ca ĐỎ. Ba `close()` phải có **ba** đột biến riêng — một đột biến gỡ cả ba chỉ chứng minh có ít nhất một. |
| **A12** | **B5** — trong một loạt M4, **mọi** bản ghi thấy **cùng một** `bay_gio`. | Clock tiêm đếm số lần gọi: đòi **đúng 1**. Đột biến để callee tự `datetime.now` khi caller đã truyền ⇒ ca ĐỎ. |
| **A13** | Suite `ops/lease_publish_test.py` **N/N hai số BẰNG NHAU**, `N ≥ 166 + (số ca mới)`. | Đọc `rc` **trực tiếp**, không qua pipe (nợ `RC-QUA-PIPE-KHONG-CO-CHOT`). |
| **A14** | `actionlint` trên **cả** workflow `rc` **không đổi so `origin/master`** (DELTA = 0). Thiếu `actionlint` **hoặc** thiếu `shellcheck` ⇒ in **KHÔNG ĐO ĐƯỢC** và ĐỎ. | Nền 23-08-2026 đã đo `rc=1` (1 finding `SC1003:info` ở `ops-don-ref.yml:106`) khi **có** `shellcheck`, và `rc=0` khi **vắng** — nên tiêu chí là DELTA, không phải `rc=0` tuyệt đối. |
| **A15** | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` `rc=0`; `adr-song` `rc=0`. | Chạy trực tiếp, `rc` không qua pipe. |
| **A16** | `git diff --numstat origin/master..<head>` chạm **đúng ba** đường của `write_set`, không đường thứ tư. | Đột biến thêm một đường ⇒ tiêu chí ĐỎ. Đây là chốt write-set exclusion của protocol §5. |

**Không tiêu chí nào trong bảng này được đóng bằng `rc=0`.** Mỗi dòng đòi **bằng chứng dương**:
hai số bằng nhau, `ok: true`, hoặc một đột biến ĐỔI MÀU đúng ca đích — và ca đích phải phân hạng
bằng **lớp ngoại lệ riêng + tên ca**, không bằng chuỗi thông điệp (bài học tín dụng giả #355/#359).

## 7. `hinh_dang_ke_thua` (L4) — chép từ r9 + #499

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao" | 2 | r9 §1 |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | r9, #473 |
| **"nguồn được tin mà chưa xác minh"** | **6** | r9 lượt 1, 2, 3, 4b, 5, 6 |
| "cổng CÓ MẶT khác cổng ĐO ĐƯỢC" | 1 | #499 C2a |
| "gate xanh lane PR, master đo lần đầu" | 1 | #499 C3 |

Hình dạng thứ tư đã chạm **6** — r4 từng tuyên bố *"lượt 4 còn tìm ra ⇒ dừng packet, ADR riêng"*,
và chủ kho đã reroute sang **ADR-0047**. Nên với A1a, một finding lớp *"nguồn được tin mà chưa xác
minh"* ở lượt review đầu **không** phải cớ vá tiếp: nó là **lần thứ 7**, và §12 protocol đòi hỏi lại
cách làm chứ không đòi thêm một bản vá.

## 8. `chua_do_duoc`

1. **Số dòng thêm của A1a.** Ước **+180…+320** (M1–M3 ~120–180 trong `lease_publish.py`; M4–M9 ~60;
   test M10 ~100+). Trần `sensitive` của ADR-0044:5 là **300 dòng thêm**. **Chưa đo** vì chưa có mã.
   Chốt bắt buộc: khi `numstat` thật vượt **300**, executor **DỪNG** và xin một dòng quyết định bền
   của chủ kho (ngoại lệ có phạm vi, hoặc tách `M5`–`M9` ra `A1c`) — **không** tự đi tiếp, và
   **không** viết vào thân PR rằng cổng ADR-0044 "ĐẠT". Ca đã trả giá: `PLAT-X8` để con số trôi bốn
   lần, và lần thứ tư nó khai sai rằng **một thẩm quyền đã có**.
2. **`BIA_MO_LICH_SU` gồm những cặp nào.** Đã đo bằng `yaml.safe_load` (KHÔNG regex) trên `ops/leases/**`
   của **473** ref, gom theo `lease_id`, đo **06:40–06:47Z 20-09-2026**:

   | đại lượng — **đơn vị khai rõ** (L1) | số |
   |---|---|
   | tệp lease phân tích được thành `dict` có `lease_id` | **350** |
   | YAML hỏng / bỏ qua | **0** |
   | **cặp `(cũ, mới)` hai chiều hợp lệ** — lease mới khai `thay_the_cho: cũ` **VÀ** lease cũ khai `da_bi_thay_the` | **155** |
   | cặp một chiều (lease cũ không có trong kho, hoặc thiếu `da_bi_thay_the`) | **6** |

   Con số cần cho `BIA_MO_LICH_SU` là **155**, không phải một con số "số tệp có trường bia mộ" —
   hai đơn vị khác nhau, và bản đo đầu của phiên này (regex, **223** tệp *"có trường"*) đúng là ca
   *"số hạng trôi trong khi câu văn vẫn nghe hợp lý"* mà L5 tố cáo. Ghi lại cả phép đo hỏng vì
   **nguyên nhân sai trong tài liệu tệ hơn không ghi**.

   Còn **KHÔNG ĐO ĐƯỢC** trong lượt này: bao nhiêu trong 155 cặp ấy nằm **trước** `MOC_BIA_MO_LICH_SU`.
   Phép đo cần: với mỗi tệp lease, tìm commit đầu tiên đưa nó vào rồi hỏi `merge-base --is-ancestor`
   với mốc — chưa chạy vì chi phí, **không** vì không có đường.

   Và miền đúng của hằng vẫn là **quyết định biên giới chưa hỏi**: (a) mọi cặp hai chiều có trước
   `MOC_BIA_MO_LICH_SU`, hay (b) chỉ những cặp mà lease mới còn hiệu lực. Câu này thuộc **vòng 2**;
   A1a **không** tự chọn. Lưu ý kích thước: **155** cặp ghim thẳng vào một `tuple` trong
   `ops/lease_publish.py` là ~155 dòng — **tự nó đã ăn nửa trần ADR-0044** ở mục 1 trên. Nếu vòng 2
   chọn (a) thì gần như chắc chắn phải tách `M4` ra một packet riêng, hoặc đổi cách chứa (tệp dữ
   liệu có băm thay vì hằng trong mã) — và **đổi cách chứa là đổi `write_set`**, tức revision mới.
3. **Q1** — SHA 40-hex của `actions/upload-artifact`. Chỉ chủ kho readback được.
4. **Q3** — sha256 thân comment `5575587924`. Lệnh chủ kho chạy trên máy cá nhân:
   `gh api repos/ducthangho/tra-luat/issues/comments/5575587924 --jq .body | sha256sum`.
5. **Va chạm write set với #570.** `ops/lease_publish_test.py` do `wp570-bash-nen-r2-g2-claude` giữ
   tới `2026-09-21T01:55:00Z`. Đã hỏi nhả sớm (#571 comment `5748145023`, theo Q6). **Không** có
   đường thu hồi sớm trong quyền của phiên: bia mộ hai chiều là một **khe** đã lách **bảy** lần và
   chủ kho chọn không đi; sổ thu hồi ADR-0047 bị chặn ở `PROFILE_ADAPTER_DA_DUYET` rỗng mà chính
   ADR cấm executor tự duyệt. **Không cấp lease A1a trước khi đường ấy `NGƯỜI_GIỮ 0`** — đo lại,
   đừng suy từ giờ hết hạn.
6. **Mỏ neo profile đầu tiên.** Sau khi A1a land, giá trị đầu cho `PROFILE_ADAPTER_DA_DUYET` đo trên
   lượt canary và **chủ kho duyệt bằng commit có review**. Không thuộc A1a (xem `ngoai_pham_vi`).
7. **Tác động của schema v2 lên hằng đã có.** `_HOSO_KHOA` là phép so **tập khoá khít**; đổi nó làm
   đỏ mọi ca đang dựng hồ sơ v1. Số ca bị chạm **chưa đếm** — đếm trước khi vá, và ghi lại delta.
8. **`NGAN_SACH_MAC_DINH` chưa đo trên roots production** (tự khai ngay tại `lease_publish.py:944`).
   Mọi tiêu chí của A1a **không** dựa vào tính đúng của các biên ấy.
