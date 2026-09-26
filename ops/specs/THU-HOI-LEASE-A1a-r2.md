# ĐẶC TẢ — `THU-HOI-LEASE-A1a` — **revision 2** (chưa đóng băng)

| trường | giá trị |
|---|---|
| `packet_id` | `THU-HOI-LEASE-A1a` (nửa **mã** của slice A1; nửa **cấu hình** là `THU-HOI-LEASE-A1b`) |
| `revision` | 2 |
| `thay_the_cho` | revision 1 `ops/specs/THU-HOI-LEASE-A1a.md`, sha256 `64f92d4026fda7bdeb4326be660614eea2d25f6e30db9a20ff0c1c6aa4f5f37c` (211 dòng, 21 775 B; land qua PR #577, commit `9db7145`). Tệp r1 **giữ nguyên** trong kho để băm của nó vẫn tra được; r2 là tệp riêng. |
| `packet_issue` | **#564** (`[THU-HOI-LEASE-A1] Packet Issue`). Issue **không** cấp việc; chỉ Issue + lease còn hiệu lực mới giao được (protocol §3.2, §4). |
| `nguon_cap_viec` | Spec cha **r9** `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` §`write_set` dòng A1 · #499 §A (A1–A3), §B (B1–B5) · quyết định chủ kho vòng 2 tại #499 comment [`5825988768`](https://github.com/ducthangho/tra-luat/issues/499#issuecomment-5825988768) · số đo nợ `AG-T0-01B` dạng 2 tại #564 comment [`5847471844`](https://github.com/ducthangho/tra-luat/issues/564#issuecomment-5847471844) |
| `review_class` | **`sensitive`**: `ops/lease_publish.py` là cổng đọc lease (protocol §8). |
| `reviewer` | codex `gpt-6-astra`, effort `high` (chỉ thị chủ kho 26-09). Trần `codex_review_calls` của đặc tả này **4** (chủ kho nâng 2 → 4 trong phiên 26-09, khai trên #564 trước lượt 1). |
| `dong_bang` | bằng **human audit của chủ kho** sau khi lượt codex cuối sạch, rồi merge bằng merge commit. Tới lúc đó tệp này **chưa** đóng băng và **không** lease nào được neo vào nó. |

**Định danh tệp này là BĂM, không phải tên nhánh.** Tìm ở `master` trước; chưa thấy thì fetch nhánh
`claude/spec-a1a-r2-20260926`. Tên nhánh sẽ trôi hoặc bị xoá, băm thì không.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**. Trạng thái thứ ba làm cổng ĐỎ, không làm tròn thành hai.

---

## 0. Quyết định của chủ kho

### Vòng 1 (giữ nguyên từ r1; mỏ neo #499 `5748147306`)

| câu | quyết định | hệ quả |
|---|---|---|
| **Q2** schema ADR-0047 lớp 2 | hai tầng | M1 |
| **Q4** Q7/ADR-0044 cho A0 | chấp nhận ngoại lệ, không tách hồi tố | A1a không kế thừa ngoại lệ ấy |
| **Q5** tách A1 | hai spec, hai băm | M-F sang A1b |
| **Q6** va chạm write set với #570 | hỏi nhả sớm | đã hết: #570 không còn giữ (xem §1) |

### Vòng 2 (mới ở r2; mỏ neo #499 `5825988768`, 25-09-2026)

| câu | nguyên văn lựa chọn | giá trị | đo lại ở r2 |
|---|---|---|---|
| **Q1** SHA `actions/upload-artifact` | "Xác nhận cả hai" | `ea165f8d65b6e75b540449e92b4886f43607fa02` (`refs/tags/v4` = `refs/tags/v4.6.2`, lightweight) | **khớp** — `git ls-remote https://github.com/actions/upload-artifact refs/tags/v4 refs/tags/v4.6.2 'refs/tags/v4^{}' 'refs/tags/v4.6.2^{}'` lúc `2026-09-26T15:54:59Z`: hai dòng, cùng OID trên; **không** có dòng `^{}` ⇒ tag lightweight. REST `repos/actions/upload-artifact/git/ref/tags/v4` trả **403** từ container này (`15:55:00Z`), nên readback đi đường git. |
| **Q3** sha256 thân comment `5575587924` | "Xác nhận cả hai" | `f974b6dba1bfccd4f6ec4315c00ece7868a045487ffbf6ae3d4df86fb4315153`; **định nghĩa: sha256 của trường `body` UTF-8 thô, KHÔNG có `\n` cuối** | **khớp** — REST `issues/comments/5575587924` (PR #475, `updated_at` `2026-09-07T20:59:59Z`) lúc `2026-09-26T15:55:00Z`: body **1379 B**, không kết thúc bằng `\n`, sha256 đúng giá trị trên. Cùng body **thêm** `\n` cho `df81f47b50624d13faeb7a756b6f3573c999aef485ee8d741dbcd3d13ae2a7a8`: đây là giá trị SAI mà chốt A18 phải từ chối. |
| **Biên giới `BIA_MO_LICH_SU`** | "(b) Chỉ cặp còn hiệu lực" | chỉ các cặp `(cũ, mới)` mà lease **mới** còn hiệu lực; **không** ghim cặp lịch sử | §5 M4, §8 mục 2 |

Hệ quả: M-A và M-C của r1 **ra khỏi** `ngoai_pham_vi`, thành **M12** và **M13**. `chua_do_duoc` mục 2, 3, 4 của r1 đóng.

## 1. Số đo — `origin/master` `24c48e28bacd2c835e6acf7df64c7ee60ae6d424`, đo **15:47–15:56Z 26-09-2026**

Đồng bộ ref trước khi đo: tập tên `git ls-remote --heads origin` so với `for-each-ref refs/remotes/origin`
(bỏ `HEAD`), bằng `comm -23` / `comm -13`: **428 / 428, cả hai chiều rỗng**.

```
ops/lease_publish.py            2047 dòng
  :934   SO_THU_HOI_KICH_HOAT = False
  :942   PROFILE_ADAPTER_DA_DUYET: frozenset = frozenset()
  :944   BIA_MO_LICH_SU: tuple = ()               # tiêu thụ DUY NHẤT ở _du_bao_check :1783
  :948   DESCRIPTOR_Q13_SHA256 = None             # tiêu thụ ở lenh_kiem_thu_hoi_github :1857–1859, receipt :1886
  :1021  def kiem_ban_ghi_thu_hoi(..., bay_gio=None)
  :1258  def hoso_adapter_do(...)  · :1277 _HOSO_KHOA · :1281 kiem_mien_ho_so · :1307 bam_ho_so
  :1386  class KhoObject
  :1722  def _doc_blob_text_12(...) · :1762 def _du_bao_check(...)
  :1934  def lenh_ai_dang_giu(a)
  :482   def _quet_lease_toan_kho(...)            # đọc mỗi cặp (blob, path) ĐÚNG MỘT LẦN — xem M14
ops/lease_publish_test.py       7288 dòng · 168 hàm `def tNNN` · suite 168/168 đạt; đã chạy=168, bỏ qua=0
                                (bản sao `git archive` của 24c48e28, 2 phút 14 giây, rc=0)
.github/workflows/ops-thu-hoi-admission.yml   178 dòng
  :57    uses: actions/checkout@v4
  :173   uses: actions/upload-artifact@v4          # M12
```

**Neo theo TÊN symbol, không theo số dòng.** PR #589 (#579, head `190def2f`, chưa merge lúc đo) sửa
`ops/lease_publish.py` **+163 dòng** trong hunk quanh `kiem()` (`@@ -888,14 +888,173`), nên mọi số dòng
từ `:888` trở xuống sẽ trôi khi #579 land. Executor đo lại tại `base_sha` của lease A1a.

`ai-dang-giu` (đọc `rc` trực tiếp, sau khi đưa hai nhánh cục bộ tụt sau `0/122` và `0/134` về `origin/master`):

| đường dẫn | `rc` | người giữ |
|---|---:|---|
| `ops/lease_publish.py` | 11 | **NGƯỜI_GIỮ 1** — `dang-lease-dau-truoc-kiem-sau-r17-g15-claude` (#579, cấp `2026-09-26T15:01:46Z`, hết hạn `2026-09-27T00:00:00Z`) |
| `ops/lease_publish_test.py` | 11 | **NGƯỜI_GIỮ 1** — cùng lease |
| `.github/workflows/ops-thu-hoi-admission.yml` | 0 | NGƯỜI_GIỮ 0 |
| `ops/specs/THU-HOI-LEASE-A1a-r2.md` · `ops/reviews/thu-hoi-lease-a1a-r2/**` | 0 | NGƯỜI_GIỮ 0 |

## 2. Tiền đề của r1 đã trôi (L5) — đo lại, hai chiều

| r1 (20-09-2026, `a270aea`) | đo lại 26-09 (`24c48e28`) | chiều |
|---|---|---|
| `ops/lease_publish_test.py` giữ bởi `wp570-bash-nen-r2-g2-claude` | giữ bởi `…-r17-g15-claude` (#579) | người giữ đổi, **vẫn chặn** |
| suite **166** ca | **168** ca, 168/168 | +2 |
| `lease_publish.py` 2042 dòng; `BIA_MO_LICH_SU` :939, `_du_bao_check` :1757 | 2047 dòng; :944, :1762 | trôi +5 |
| `upload-artifact@v4` ở dòng **147** | dòng **173**, vẫn TAG `@v4` | trôi +26 |
| Q1, Q3 **MỞ** | có giá trị, đo lại **khớp** (§0) | đóng |
| `BIA_MO_LICH_SU`: **350** tệp lease / **155** cặp hai chiều / **6** một chiều (473 ref) | **495** cặp `(blob, path)` / **465** `lease_id` / **234** cặp hai chiều / **10** một chiều (428 ref) | tăng; nay **không** dùng tới, vì (b) chỉ lấy **4** cặp (§8 mục 2) |
| 473 ref | 428 ref | nhánh đã được dọn |

Đơn vị khai rõ, vì chính r1 ghi lại một phép đo hỏng do lẫn đơn vị (223 *tệp có trường* so với 155 *cặp*):
"cặp `(blob, path)`" là số bản ghi `_quet_lease_toan_kho` đọc, **không** phải số tệp và không phải số ref.

## 3. `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
.github/workflows/ops-thu-hoi-admission.yml
```

Đúng ba đường, không ký tự đại diện, **không đổi so r1**. Hiện vật review (`ops/reviews/**`) và
bookkeeping (`CHANGELOG.md`, `RELEASE_MANIFEST.json`) đi nhánh riêng theo tiền lệ #551/PR #567.

## 4. `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| **M-F** — `SO_THU_HOI_KICH_HOAT = True` | Q5: sang **A1b**. Điều kiện Q10(d) (required check + strict up-to-date + chặn bypass) là cấu hình ngoài kho. |
| Ghim `actions/checkout@v4` (dòng 57) | Q1 **chỉ** trả lời cho `upload-artifact`. ADR-0047 cấm executor tự chọn mỏ neo; ghim checkout cần một câu hỏi riêng cho chủ kho. |
| Nợ `AG-T0-01B` **dạng 1** (#564): lease của packet đã land vẫn giữ tới hạn | Không trường nào trong tệp lease nói packet đã land; chữa bằng sổ thu hồi, tức **A1b** kích hoạt. A1a chỉ chữa **dạng 2** (M14). |
| Ghim lại `BIA_MO_LICH_SU` lúc kích hoạt | Theo (b), tập cặp **đổi theo thời gian** (§8 mục 2). A1b phải đo lại và ghim lại **trước** khi bật cờ; A1a chỉ ghim ảnh chụp tại mốc của chính nó. |
| Duyệt giá trị đầu tiên vào `PROFILE_ADAPTER_DA_DUYET` | ADR-0047 lớp 2: executor không tự duyệt. A1a mở schema, không đổ giá trị. |
| Đổi trạng thái ADR-0047 | quyết định chủ kho |
| Đo/chốt `NGAN_SACH_MAC_DINH` trên roots production | mặt trận khác |
| Sửa `ops/leases/**`, `docs/**` | ngoài write set |
| Gọi CI, CI Windows, `workflow_dispatch`, re-run tay | chỉ thị chủ kho: `manual_ci_budget: 0` |

## 5. `muc_tieu` — mỗi dòng chiếu vào MỘT đường dẫn của `write_set` (L2)

M1–M3, M5–M11 **giữ nguyên nội dung r1**, chỉ đổi số dòng trỏ tới (§1). Dòng in đậm là mới hoặc đổi ở r2.

| # | mục tiêu | đường dẫn | nguồn |
|---|---|---|---|
| M1 | Schema hồ sơ adapter **hai tầng** (`schema_version: 2`): tầng BẮT BUỘC vào digest (`git_path`, `git_version`, `credential_helper`, `tls_thu_vien`, `http_sslCAInfo`/`http_sslCAPath`/`proxy`/`endpoint`, `image_os`/`image_version`); tầng AUDIT-ONLY ra ngoài digest (`git_sha256`, băm nhị phân khác). | `ops/lease_publish.py` | #499 A2 · Q2 |
| M2 | `bam_ho_so` băm chỉ tầng bắt buộc; `kiem_mien_ho_so` kiểm miền cả hai tầng, chỉ tầng bắt buộc quyết định `12`. | `ops/lease_publish.py` | Q2 |
| M3 | `image_os`/`image_version` ba trạng thái: chuỗi · `None` · thiếu khoá ⇒ `12`. Mỏ neo đòi runner mà hồ sơ `None` ⇒ `12`. | `ops/lease_publish.py` | Q2 |
| **M4** | **Theo (b).** Tạo `MOC_BIA_MO_LICH_SU` = OID 40-hex của commit `master` nơi executor **đo** tập cặp (tổ tiên của nhánh mặc định). Ghim `BIA_MO_LICH_SU` = đúng tập cặp `(cũ, mới)` **hai chiều** mà lease `mới` còn hiệu lực tại mốc ấy, đo bằng thuật toán §8 mục 2, theo đúng miền `_du_bao_check` tiêu thụ (`for cu, moi, *_ in …`). Thứ tự phần tử: sắp theo `(cũ, mới)`. | `ops/lease_publish.py` | Q (b) · r9 A1 |
| M5 | B1 — `_du_bao_check` đỡ decode khi đọc bản ghi qua `GOI_GIT`. | `ops/lease_publish.py` | #499 B1 |
| M6 | B2 — `_doc_blob_text_12` bắt `OSError`. | `ops/lease_publish.py` | #499 B2 |
| M7 | B3 — consumer đọc marker/policy bằng bytes thô ở mọi chỗ so băm. | `ops/lease_publish.py` | #499 B3 |
| M8 | B4/F13 — đóng đủ 3 fd ống ở đường deadline của `KhoObject.doc`. | `ops/lease_publish.py` | #499 B4 |
| M9 | B5/F14 — một snapshot clock cho cả loạt M4 của `kiem-thu-hoi-github`. | `ops/lease_publish.py` | #499 B5 |
| M10 | Mỗi M1–M9, M12–M14 có ca `t…`; suite **N/N hai số bằng nhau**. | `ops/lease_publish_test.py` | L3 |
| M11 | Workflow giữ `actionlint` DELTA = 0 so `origin/master`. | `.github/workflows/…` | — |
| **M12** | **(từ M-A)** Dòng `uses:` của `actions/upload-artifact` thành `actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4.6.2`. Chỉ dòng ấy; `actions/checkout@v4` **không** đổi (§4). | `.github/workflows/ops-thu-hoi-admission.yml` | Q1 |
| **M13** | **(từ M-C)** `DESCRIPTOR_Q13_SHA256 = "f974b6dba1bfccd4f6ec4315c00ece7868a045487ffbf6ae3d4df86fb4315153"` (chuỗi 64 hex thường). Sửa chú thích tại chỗ để nêu **định nghĩa** Q3 (body UTF-8 thô, không `\n` cuối) và mỏ neo `5825988768`. | `ops/lease_publish.py` | Q3 |
| **M14** | **(nợ `AG-T0-01B` dạng 2)** Trong `lenh_ai_dang_giu`: một `lease_id` có bia mộ **đối xứng** (`_bia_mo_doi_xung(...) is True`) trên **bản sao ở ref canonical** `refs/remotes/origin/<nhánh mặc định>` thì **mọi** bản sao cùng `lease_id` trên mọi ref khác **không** được đếm là người giữ; nhãn in `ĐÃ_BỊ_THAY_THẾ (MẶC_ĐỊNH)`. Bia mộ chỉ nằm trên nhánh **khác** nhánh mặc định **không** che bản sao nào ngoài chính nó (giữ nguyên hành vi cũ). Chi tiết và bẫy: §5.1. | `ops/lease_publish.py` | #564 `5847471844` |

### 5.1 M14 — vì sao, và cái bẫy khử trùng

**Đo được (`2026-09-26T15:55:10Z`):** `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `rc=11`, `NGƯỜI_GIỮ 2`. Lease
`ci-registry-dot-bien-theo-diff-r1-g1-claude` (#643, packet đã land) có **hai** blob:

| blob | `da_bi_thay_the` | nằm trên |
|---|---|---|
| `e6e2fa56…` | có (→ `ci-registry-pretooluse-che-do-nhe-r1-g1-claude`) | `origin/master` và 7 ref khác |
| `ab5b96a7…` | **không** | `origin/claude/ci-registry-pretooluse-nhe-r1-g1`, `origin/claude/spec-ci-registry-pretooluse-nhe-r1`, `origin/ops/cap-lease-579-g14`, `origin/ops/cap-lease-643` |

`lenh_ai_dang_giu` xét từng bản ghi `(blob, path)` độc lập, nên blob `ab5b96a7` vẫn được đếm là người giữ
dù bản trên master đã bị thay hợp lệ.

**Bẫy phải xử lý:** `_quet_lease_toan_kho` đọc mỗi `(blob, path)` **đúng một lần** và giữ **một** ref cho
nó. Blob đã bia mộ `e6e2fa56` được in dưới ref cục bộ **đầu tiên** theo thứ tự `for-each-ref`, **không** dưới
`origin/master`: lần đo `15:48Z` là `refs/heads/claude/wp523-r15-g17-a6`, lần đo `15:55:10Z` là
`refs/heads/claude/spec-a1a-r2-20260926` (nhánh của chính đặc tả này, vừa tạo). Ref được ghi **phụ thuộc
nhánh nào đang có mặt**. Nên phép hỏi "bản sao này có nằm
trên nhánh mặc định không" **không** được trả lời bằng `muc['ref']`. Phải hỏi thẳng cây của ref canonical
(ví dụ `ls-tree` `refs/remotes/origin/<nhánh mặc định>` dưới `ops/leases`) để lấy tập blob có mặt ở đó.

**Vì sao nhánh mặc định thắng bản sao khác cùng `lease_id`:** một `lease_id` định danh **một** generation.
Đường hợp lệ duy nhất để làm tiếp là generation mới khai `thay_the_cho` (protocol §4). Một bản sao khác
nội dung mà cùng `lease_id` trên nhánh chưa merge **không** hồi sinh được generation đã bị thay trên nhánh
mặc định. Nhánh mặc định là ref duy nhất đi qua review + merge, nên là ref duy nhất có thẩm quyền đặt
bia mộ che toàn kho. Chiều ngược (bia mộ trên nhánh phụ che toàn kho) **bị cấm**, vì như thế một nhánh
chưa ai review có thể tắt một lease đang sống.

**Fail-close:** ref canonical vắng trong cache ⇒ `KHÔNG_XÁC_ĐỊNH` (`rc=12`), không lùi về luật cũ.
Bia mộ **một chiều** trên nhánh mặc định ⇒ giữ nguyên hành vi hiện có (`KHÔNG_XÁC_ĐỊNH`).
Tên nhánh mặc định lấy từ cờ `--nhanh-mac-dinh` đã có (mặc định `master`).

## 6. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

**A1–A5, A8–A16 giữ nguyên nội dung r1** (tên và phép đo), trừ A13 (số ca nền nay là **168**). Dòng in đậm là mới hoặc đổi ở r2.

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| A1 | `hoso_adapter_do()` trả `schema_version == 2` và đúng tập khoá v2. | giữ `schema_version = 1` ⇒ ĐỎ; thêm một khoá lạ ⇒ ĐỎ. |
| A2 | `bam_ho_so` không đổi khi chỉ tầng AUDIT đổi. | đưa `git_sha256` trở lại dict được băm ⇒ ĐỎ. |
| A3 | `bam_ho_so` đổi khi bất kỳ khoá bắt buộc đổi. | bỏ một khoá khỏi tập được băm ⇒ đúng ca ấy ĐỎ; A2/A3 phải ĐỎ ngược chiều nhau. |
| A4 | ba trạng thái `image_os`. | gộp `None` với thiếu khoá ⇒ ĐỎ; cho `None` khớp mỏ neo runner ⇒ ĐỎ. |
| A5 | `PROFILE_ADAPTER_DA_DUYET` rỗng vẫn ⇒ `12` trên đường production. | cho mỏ neo rỗng đi tiếp ⇒ ĐỎ. |
| **A6** | `MOC_BIA_MO_LICH_SU` là OID 40-hex thường và **là tổ tiên** của nhánh mặc định (`merge-base --is-ancestor`, `rc=0`). | ghim OID không phải tổ tiên ⇒ ĐỎ; ghim chuỗi 39 ký tự ⇒ ĐỎ. **Ca "KHÔNG ĐO ĐƯỢC"**: ref nhánh mặc định vắng ⇒ ca ĐỎ, không bỏ qua êm. |
| **A7** | `_du_bao_check`: cặp trong `BIA_MO_LICH_SU` ⇒ dự báo `rc` 0; cặp vắng ⇒ dự báo 8. | `any(...)` → `True` ⇒ ca "vắng" ĐỎ; so một vế ⇒ ca "đúng cũ, sai mới" ĐỎ. |
| **A7b** | **Ảnh chụp (b) khớp phép đo tại mốc.** Một ca dựng kho giả gồm: cặp hai chiều lease mới còn hạn (phải có mặt), cặp hai chiều lease mới **hết hạn** (phải vắng), cặp hai chiều lease mới **đã bị thay tiếp** (phải vắng), cặp **một chiều** (phải vắng); chạy hàm đo §8 mục 2 và đòi đúng một cặp. | bỏ điều kiện "còn hạn" ⇒ ca ĐỎ; bỏ điều kiện "chưa bị thay tiếp" ⇒ ca ĐỎ; bỏ điều kiện "hai chiều" ⇒ ca ĐỎ. **Ba** đột biến, ba ca đích riêng. |
| A8–A12 | B1–B5 như r1 (phân hạng theo LỚP ngoại lệ riêng + tên ca, không theo chuỗi thông điệp). | như r1. A11 ba `close()` = ba đột biến riêng. |
| **A13** | Suite `ops/lease_publish_test.py` **N/N hai số bằng nhau**, `N ≥ 168 + (số ca mới)`, `bỏ qua=0`. | đọc `rc` trực tiếp, không qua pipe. |
| A14 | `actionlint` DELTA = 0 so `origin/master`; thiếu `actionlint` hoặc `shellcheck` ⇒ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ. | nền đo ở §7 của phiên thi công. |
| A15 | `doctrine-scan` và `adr-song` `rc=0`. | chạy trực tiếp. |
| A16 | `git diff --numstat origin/master..<head>` chạm đúng ba đường write set. | thêm một đường ⇒ ĐỎ. |
| **A17** | **M12.** Ca đọc `.github/workflows/ops-thu-hoi-admission.yml` và đòi: đúng **một** dòng `uses:` tham chiếu `actions/upload-artifact`, và tham chiếu ấy **bằng đúng** `actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02`. Hằng Q1 nằm trong **tệp test**, không đọc từ workflow (đọc từ workflow thì ca so tệp với chính nó). | quay về `@v4` ⇒ ĐỎ; đổi một ký tự của SHA ⇒ ĐỎ; nhân đôi dòng `upload-artifact` (một ghim, một tag) ⇒ ĐỎ. |
| **A18** | **M13.** (i) `DESCRIPTOR_Q13_SHA256` là chuỗi khớp `^[0-9a-f]{64}$` và bằng hằng Q3 trong tệp test. (ii) Đường marker MỚI của `kiem-thu-hoi-github` trên kho giả: `descriptor_sha256` = Q3 ⇒ **qua** chốt descriptor (dừng ở chốt kế tiếp hoặc thành công, không dừng ở thông điệp descriptor); = sha256 của body **có** `\n` cuối (`df81f47b50624d13faeb7a756b6f3573c999aef485ee8d741dbcd3d13ae2a7a8`) ⇒ `12` tại chốt descriptor; lệch 1 ký tự ⇒ `12`. (iii) Receipt ghi `descriptor_q13_ghim` = Q3. (iv) **Bốn chốt còn lại của marker MỚI vẫn đứng**: descriptor đúng nhưng từng điều kiện `first_policy_sha256` sai · `base_sha_before_add ≠ S` · S đã có policy · policy vắng ở T ⇒ mỗi ca `12`. | để `None` ⇒ (i),(ii) ĐỎ; so không phân biệt `\n` cuối (vd `.strip()` trước khi băm) ⇒ ca `df81f47b` ĐỎ; gỡ từng chốt trong (iv) ⇒ đúng ca ấy ĐỎ. (iv) chứng minh việc ghim **không** mở cửa rộng hơn chốt descriptor. |
| **A19** | **M14, che đúng.** Kho giả: lease `L` còn hạn, bản trên nhánh mặc định có bia mộ đối xứng tới `L'`; bản cũ **không** bia mộ trên nhánh phụ `z-landed`. `ai-dang-giu <đường của L>` ⇒ `L` **không** trong `NGƯỜI_GIỮ`. | bỏ M14 (hành vi cũ) ⇒ ca ĐỎ (`L` bị đếm). |
| **A20** | **M14, không che quá tay.** Kho giả: bia mộ đối xứng của `L` chỉ nằm trên nhánh phụ `z-side`; nhánh mặc định có `L` không bia mộ ⇒ bản trên nhánh mặc định **vẫn** được đếm, `NGƯỜI_GIỮ` chứa `L`. | đột biến "bia mộ trên **mọi** ref che toàn kho" ⇒ ca ĐỎ. |
| **A21** | **M14, bẫy khử trùng.** Kho giả: blob đã bia mộ có mặt **cả** trên nhánh mặc định **và** trên một nhánh phụ có tên sắp **trước** nhánh mặc định (vd `a-first`), để `_quet_lease_toan_kho` ghi ref nhánh phụ cho blob ấy; blob cũ không bia mộ nằm trên nhánh thứ ba ⇒ `L` **không** trong `NGƯỜI_GIỮ`. | đột biến xác định "có trên nhánh mặc định" bằng `muc['ref']` ⇒ ca ĐỎ. **Ca tự kiểm fixture:** trong cùng ca, đòi `muc['ref']` của blob bia mộ **khác** ref nhánh mặc định — không thì fixture không dựng được bẫy và ca phải ĐỎ. |
| **A22** | **M14, fail-close.** (i) Ref canonical vắng khỏi cache ⇒ `rc=12` với `KHÔNG_XÁC_ĐỊNH`. (ii) Bia mộ **một chiều** trên nhánh mặc định ⇒ `rc=12` như hiện tại. | đột biến lùi về luật cũ khi ref vắng ⇒ (i) ĐỎ; đột biến coi bia mộ một chiều là che ⇒ (ii) ĐỎ. |

**Không tiêu chí nào đóng bằng `rc=0`.** Mỗi dòng đòi bằng chứng dương: hai số bằng nhau, `ok: true`,
hoặc một đột biến ĐỔI MÀU đúng ca đích. Ca đích phân hạng bằng **lớp ngoại lệ riêng + tên ca**
(bài học tín dụng giả #355/#359). Ba chốt M14 (A19/A20/A21) phải phân biệt được bằng đầu vào: nếu
một đột biến làm đỏ cả ba thì chúng là bộ tương đương và chỉ đang đo một chốt.

## 7. `hinh_dang_ke_thua` (L4)

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao" | **3** | r9 §1 (2) · **#564 dạng 2** (bia mộ ghi vào bản sao master, bản sao khác sống tiếp) |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | r9, #473 |
| **"nguồn được tin mà chưa xác minh"** | **6** | r9 lượt 1–6 |
| "cổng CÓ MẶT khác cổng ĐO ĐƯỢC" | 1 | #499 C2a |
| "gate xanh lane PR, master đo lần đầu" | 1 | #499 C3 |
| **"khử trùng giữ một đại diện, rồi hỏi đại diện câu hỏi về cả nhóm"** | **1** (mới) | M14 §5.1: `muc['ref']` là một ref trong nhiều |

Hình dạng "nguồn được tin mà chưa xác minh" ở **6**. Một finding lớp ấy ở lượt review đầu của A1a là
**lần 7**: §12 protocol đòi xem lại cách làm, không đòi thêm bản vá.

## 8. `chua_do_duoc` và điều kiện trước khi cấp lease

1. **Số dòng thêm — ƯỚC, chưa đo, và gần như chắc VƯỢT trần.** ADR-0044:5 cho `sensitive` **≤ 300 dòng
   thêm**, đếm cả test (`git diff --numstat`).

   | phần | ước (dòng thêm) |
   |---|---|
   | M1–M3 mã | 120–180 |
   | M4 (4 cặp + mốc + chú thích) | 10–20 |
   | M5–M9 mã | 50–70 |
   | M12 · M13 mã | 2–6 |
   | M14 mã | 20–35 |
   | test M1–M9 | 100–160 |
   | test M12–M14 (A17–A22) | 90–140 |
   | **tổng** | **392–611** |

   Đặc tả này **không** tự cấp ngoại lệ và **không** tự tách. Trước khi cấp lease, chủ kho chọn **một**:
   (a) ngoại lệ ADR-0044 có phạm vi (≤ 3 tệp, ≤ N dòng, chỉ cho A1a); hoặc (b) tách `M5`–`M9` (B1–B5)
   sang `THU-HOI-LEASE-A1c` bằng revision mới của đặc tả này. Khi `numstat` thật vượt trần đã được cấp,
   executor **DỪNG** và hỏi; không viết vào thân PR rằng cổng ADR-0044 "ĐẠT".

2. **`BIA_MO_LICH_SU` theo (b) — ảnh chụp, không phải hằng số.** Thuật toán (dùng hàm của chính cổng,
   `yaml.safe_load`, không regex):

   ```
   cac   = _quet_lease_toan_kho(goc, chan_nhanh_tut_sau=True)     # sau khi đồng bộ ref (§1)
   nhóm theo lease_id
   cặp hai chiều (cũ, mới): lease `mới` khai thay_the_cho ∋ cũ  VÀ  một bản `cũ` có da_bi_thay_the == mới
   (b) giữ cặp khi lease `mới`: có ít nhất một bản _phan_loai_lease == "CÒN_HẠN"
                                VÀ không bản nào có bia mộ đối xứng (_bia_mo_doi_xung is True)
   ```

   Đo lúc **15:48Z 26-09** trên `24c48e28`, 428 ref: **4** cặp.

   | cũ | mới |
   |---|---|
   | `ci-registry-dot-bien-theo-diff-r1-g1-claude` | `ci-registry-pretooluse-che-do-nhe-r1-g1-claude` |
   | `dang-lease-dau-truoc-kiem-sau-r16-g14-claude` | `dang-lease-dau-truoc-kiem-sau-r17-g15-claude` |
   | `r378-symlink-doi-dac-quyen-r19-g19-claude` | `r378-symlink-doi-dac-quyen-r20-g20-claude` |
   | `wp570-bash-nen-r30-g30-opus` | `wp570-bash-nen-r31-g31-opus` |

   Bảng này **sẽ** trôi: bốn lease `mới` hết hạn lần lượt `2026-09-27T00:00:00Z` · `05:02:00Z` · `06:00:00Z` · `13:31:00Z` (muộn nhất ~21,6 giờ sau lúc đo), và lease
   mới sẽ sinh cặp mới. Nên giá trị ghim vào mã là phép đo **tại `MOC_BIA_MO_LICH_SU` do executor
   chọn**, chạy lại đúng thuật toán trên, kèm bản in đầu ra trong thân PR. Cặp hết hạn sau mốc **vô
   hại** với luật dự báo, vì `_du_bao_check` chỉ tra nó khi đang kiểm một lease khai `thay_the_cho`.
   Cặp **sinh sau** mốc thì **không** có trong hằng và bị dự báo `8`; đó là lý do A1b phải đo lại và
   ghim lại ngay trước khi bật cờ (§4). **KHÔNG ĐO ĐƯỢC** ở đặc tả: giá trị ghim cuối cùng.

3. **Điều kiện cấp lease A1a (không suy từ giờ hết hạn):**
   - #579 **đã land** (PR #589 merged);
   - `ai-dang-giu` đo lại **ra `NGƯỜI_GIỮ 0`** trên cả ba đường write set, `rc` đọc trực tiếp, sau khi so
     tập tên ref hai nguồn như §1;
   - chủ kho đã chọn (a) hoặc (b) ở mục 1;
   - đặc tả này đã đóng băng bằng human audit.

   Chú ý tự tham chiếu: chính nợ M14 có thể làm `ai-dang-giu` báo người giữ **giả** trên write set sau
   khi #579 land (bản sao lease #579 trên nhánh land chưa xoá). Nếu xảy ra, đường chữa là
   `ops-don-ref.yml` hoặc chờ hạn, **không** cấp lease chồng.

4. **Tương thích consumer C1a1a.** Đặc tả `LAND-DOC-RECEIPT-THU-HOI-C1a1a` revision 5 (nhánh
   `claude/spec-c1a1-doc-receipt-20260925`, chưa trên master lúc đo) đã khai `descriptor_q13_ghim` là
   "`null` hoặc hex 64" và ghi rõ *"sẽ thành hex 64 khi A1a r2 ghim Q3"* ⇒ M13 **không** làm C1a1a đỏ.
   M12 đổi blob của workflow ⇒ `workflow_definition_sha256` trong receipt đổi; luật so blob/sha256
   workflow tại C thuộc **C1a1b** (git), không thuộc C1a1a. **KHÔNG ĐO ĐƯỢC** ở đây: tác động lên C1a1b
   (chưa có đặc tả).

5. **Tác động của schema v2 lên ca đang có** (r1 mục 7): số ca dựng hồ sơ v1 bị chạm **chưa đếm** — đếm
   trước khi vá, ghi delta.

6. **Mỏ neo profile đầu tiên** và **`NGAN_SACH_MAC_DINH`**: như r1 mục 6, 8 — ngoài A1a.
