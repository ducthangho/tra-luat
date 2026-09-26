# ĐẶC TẢ — `THU-HOI-LEASE-A1a` — **revision 2**, bản nháp 2 (chưa đóng băng)

| trường | giá trị |
|---|---|
| `packet_id` | `THU-HOI-LEASE-A1a` (nửa **mã** của slice A1; nửa **cấu hình** là `THU-HOI-LEASE-A1b`) |
| `revision` | 2 — **bản nháp 2**. Bản nháp 1: commit `f8a37c04`, sha256 `a5aacafac1e69c78ad3dd56e5c977527600fe6dad320656dd7ed29688f7bc313`, đã qua codex lượt 1 (`changes_requested`, 2 P1 + 5 P2; `ops/reviews/thu-hoi-lease-a1a-r2/luot1-VERDICT.md`). Revision chỉ tăng khi đóng băng; bản nháp định danh bằng băm. |
| `thay_the_cho` | revision 1 `ops/specs/THU-HOI-LEASE-A1a.md`, sha256 `64f92d4026fda7bdeb4326be660614eea2d25f6e30db9a20ff0c1c6aa4f5f37c` (211 dòng, 21 775 B; land qua PR #577, commit `9db7145`). Tệp r1 **giữ nguyên** trong kho để băm của nó vẫn tra được; r2 là tệp riêng. |
| `packet_issue` | **#564** (`[THU-HOI-LEASE-A1] Packet Issue`). Issue **không** cấp việc; chỉ Issue + lease còn hiệu lực mới giao được (protocol §3.2, §4). |
| `nguon_cap_viec` | Spec cha **r9** `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` §`write_set` dòng A1 · #499 §A (A1–A3), §B (B1–B5) · quyết định chủ kho vòng 2 tại #499 comment [`5825988768`](https://github.com/ducthangho/tra-luat/issues/499#issuecomment-5825988768) · số đo nợ `AG-T0-01B` dạng 2 tại #564 comment [`5847471844`](https://github.com/ducthangho/tra-luat/issues/564#issuecomment-5847471844) |
| `review_class` | **`sensitive`**: `ops/lease_publish.py` là cổng đọc lease (protocol §8). |
| `reviewer` | codex `gpt-6-astra`, effort `high` (chỉ thị chủ kho 26-09). Trần `codex_review_calls` của đặc tả này **4** (chủ kho nâng 2 → 4 trong phiên 26-09, khai trên #564 `5847670544` trước lượt 1). Đã dùng **1/4**. |
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

### Vòng 3 (mới ở bản nháp 2; checkpoint §12 sau codex lượt 1; mỏ neo PR #652 [`5850620663`](https://github.com/ducthangho/tra-luat/pull/652#issuecomment-5850620663), 26-09-2026)

| finding lượt 1 | nguyên văn lựa chọn | hệ quả |
|---|---|---|
| **F1** (P1, lớp `nguon-duoc-tin-ma-chua-xac-minh`, **lần 7**): bản nháp 1 để M14 dùng một ref cache (`refs/remotes/origin/<nhánh mặc định>`, do cờ `--nhanh-mac-dinh` chọn) **xoá** holder mà không xác minh nguồn | **"Prediction-only (Recommended)"** | M14 thành **dự báo**: chỉ thêm dòng `DU_BAO:` dưới `--du-bao`, **không** đổi `rc`, **không** đổi `NGƯỜI_GIỮ`. Việc xoá holder theo bia mộ nhánh mặc định sang **A1b**, nơi có nguồn đã xác minh (ADR-0047). |
| **F2** (P1): bản nháp 1 đổi nguồn của `BIA_MO_LICH_SU` (quét mọi ref tại master do executor chọn), trong khi quyết định (b) chỉ thêm bộ lọc | **"Q6 tree + (b) (Recommended)"** | Giữ nguồn r9 Q6: dẫn xuất từ **đúng cây mốc** A0, rồi lọc (b) ở một clock ghim. Kết quả đo: **0 cặp** ⇒ `BIA_MO_LICH_SU = ()` (M4, §8 mục 2). |

F1 là lần thứ 7 của hình dạng đã đếm ở §7. Đáp ứng của bản nháp 2 **không** phải một chốt nữa cho M14 mà là **rút thẩm quyền** của nó: dự báo đọc cache thì không có gì để lừa, vì nó không quyết định gì.

## 1. Số đo — `origin/master` `24c48e28bacd2c835e6acf7df64c7ee60ae6d424`, đo **15:47–15:56Z 26-09-2026** (đo lại một phần **22:48–22:55Z**, master **không đổi**)

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

**Neo theo TÊN symbol, không theo số dòng.** PR #589 (#579) chưa merge lúc đo; head `23e16979` lúc 22:49Z
(bản nháp 1 ghi `190def2f`, head đã tiến). `git diff --numstat 24c48e28 23e16979 -- ops/lease_publish.py` ⇒
**+161 / −2**, tăng ròng **+159** (bản nháp 1 ghi "+163 dòng": đó là tổng thêm + xoá, sai đơn vị — F6 lượt 1).
Tại `23e16979`: `lease_publish.py` **2206** dòng; `BIA_MO_LICH_SU` :1103 · `DESCRIPTOR_Q13_SHA256` :1107 ·
`_du_bao_check` :1921 · `_du_bao_ai_dang_giu` :1951 · `lenh_ai_dang_giu` :2093. Executor đo lại tại `base_sha` của lease A1a.

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
| `BIA_MO_LICH_SU`: **350** tệp lease / **155** cặp hai chiều / **6** một chiều (473 ref) | **495** cặp `(blob, path)` / **465** `lease_id` / **234** cặp hai chiều / **10** một chiều (428 ref) | tăng; **không** phải nguồn của `BIA_MO_LICH_SU` (quyết định F2: nguồn là cây mốc Q6, §8 mục 2). Bản nháp 1 đã lọc (b) trên phép quét mọi ref này ra 4 cặp — phép đo ấy nay chỉ còn là chẩn đoán, **không** có thẩm quyền. |
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
| Nợ `AG-T0-01B` **dạng 1** (#564): lease của packet đã land vẫn giữ tới hạn | Không trường nào trong tệp lease nói packet đã land; chữa bằng sổ thu hồi, tức **A1b** kích hoạt. |
| **Xoá holder** theo bia mộ nhánh mặc định (nợ `AG-T0-01B` **dạng 2**, #564) | Quyết định vòng 3 (F1): cần nguồn đã xác minh (OID máy chủ, profile ADR-0047) ⇒ **A1b**. A1a chỉ **dự báo** (M14). |
| Chuyển cặp sinh **sau** mốc Q6 vào `BIA_MO_LICH_SU` | r9 Q6: *"Feature tomb không bổ sung lịch sử"*. Thay thế sau mốc đi sổ thu hồi (A1b). Cho tới khi A1b kích hoạt, `_du_bao_check` dự báo `8` cho chúng — **bảo thủ**, không mở quyền. |
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
| **M4** | **Q6 + (b).** Tạo `MOC_BIA_MO_LICH_SU = "072181157a27804e69deb35bb792a88c70ac31e3"` — OID merge của PR #492 (A0 land), readback **sau** khi A0 land, là tổ tiên của `master` (`merge-base --is-ancestor`, `rc=0`, đo `2026-09-26T22:52:50Z` trên `24c48e28`). Giữ `BIA_MO_LICH_SU: tuple = ()` — đúng giá trị mà thuật toán §8 mục 2 dẫn xuất từ **cây của mốc**, lọc (b) ở clock ghim = giờ commit của mốc. Chú thích tại chỗ ghi: định dạng phần tử `(cũ, mới, blob cũ, blob mới)` (r9 Q6); số cặp hai chiều trong cây mốc (11) và digest `8f372ccd…` của chúng; lý do rỗng (hạn muộn nhất 2026-09-08T10:17:12Z < giờ mốc). **Không** thêm mã dẫn xuất lúc chạy: hằng là dữ liệu, phép dẫn xuất là bằng chứng (§8 mục 2). | `ops/lease_publish.py` | r9 Q6 · (b) · vòng 3 F2 |
| M5 | B1 — `_du_bao_check` đỡ decode khi đọc bản ghi qua `GOI_GIT`. | `ops/lease_publish.py` | #499 B1 |
| M6 | B2 — `_doc_blob_text_12` bắt `OSError`. | `ops/lease_publish.py` | #499 B2 |
| M7 | B3 — consumer đọc marker/policy bằng bytes thô ở mọi chỗ so băm. | `ops/lease_publish.py` | #499 B3 |
| M8 | B4/F13 — đóng đủ 3 fd ống ở đường deadline của `KhoObject.doc`. | `ops/lease_publish.py` | #499 B4 |
| M9 | B5/F14 — một snapshot clock cho cả loạt M4 của `kiem-thu-hoi-github`. | `ops/lease_publish.py` | #499 B5 |
| M10 | Mỗi M1–M9, M12–M14 có ca `t…`; suite **N/N hai số bằng nhau**. | `ops/lease_publish_test.py` | L3 |
| M11 | Workflow giữ `actionlint` DELTA = 0 so `origin/master`. | `.github/workflows/…` | — |
| **M12** | **(từ M-A)** Dòng `uses:` của `actions/upload-artifact` thành `actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4.6.2`. Chỉ dòng ấy; `actions/checkout@v4` **không** đổi (§4). | `.github/workflows/ops-thu-hoi-admission.yml` | Q1 |
| **M13** | **(từ M-C)** `DESCRIPTOR_Q13_SHA256 = "f974b6dba1bfccd4f6ec4315c00ece7868a045487ffbf6ae3d4df86fb4315153"` (chuỗi 64 hex thường). Sửa chú thích tại chỗ để nêu **định nghĩa** Q3 (body UTF-8 thô, không `\n` cuối) và mỏ neo `5825988768`. | `ops/lease_publish.py` | Q3 |
| **M14** | **Dự báo** (nợ `AG-T0-01B` dạng 2; quyết định vòng 3 F1). Trong `_du_bao_ai_dang_giu` (chỉ chạy khi có `--du-bao`), với **mỗi** `lease_id` còn hạn chạm đường dẫn, in đúng một dòng `DU_BAO: <lease_id> · BIA_MỘ_MẶC_ĐỊNH=<trạng thái>`, trạng thái thuộc tập đóng `{CHE, KHONG, KHONG_XAC_DINH}`, xác định **chỉ** từ cây `refs/remotes/origin/<nhánh mặc định>` dưới `ops/leases` (§5.1). **Bất biến:** mọi dòng không mang tiền tố `DU_BAO:`, danh sách `NGƯỜI_GIỮ` và `rc` của `ai-dang-giu` **giống hệt** khi chạy không có `--du-bao`, và giống hệt `origin/master` trước A1a. | `ops/lease_publish.py` | #564 `5847471844` · vòng 3 F1 |

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

**Vì sao chỉ DỰ BÁO (codex lượt 1, F1, tái hiện được):** ref `refs/remotes/origin/<nhánh>` là bộ đệm
**cục bộ**, ghi được bằng `git update-ref`; `_quet_lease_toan_kho` chỉ so **tập tên** ref với máy chủ, không so
OID; và cờ `--nhanh-mac-dinh` do người gọi chọn. Bản nháp 1 để ref ấy **xoá** holder, nên một ref cache bị sửa
tay biến `rc=11` thành `rc=0`. Dự báo không có quyền ấy: nó in thêm thông tin, còn verdict vẫn là luật cũ.
Chữa thật (xoá holder) cần OID máy chủ + nguồn đã duyệt ⇒ A1b. Dự báo **đọc cache và nói thẳng điều đó**:
dòng tóm tắt của `_du_bao_ai_dang_giu` phải ghi nguồn là `refs/remotes/origin/<nhánh>` (bộ đệm), không phải máy chủ.

**Định nghĩa ba trạng thái** — mọi câu hỏi đều hỏi **cây canonical**, không hỏi `muc['ref']` và không hỏi
toàn kho:

| trạng thái | điều kiện, đọc từ cây `refs/remotes/origin/<nhánh mặc định>:ops/leases` |
|---|---|
| `CHE` | cây có một lease `L` (`yaml.safe_load`, `lease_id == L`) khai `da_bi_thay_the: N`, **và** chính cây ấy có lease `N` khai `thay_the_cho ∋ L` |
| `KHONG` | cây **không** có lease `L` nào khai `da_bi_thay_the` |
| `KHONG_XAC_DINH` | ref canonical vắng khỏi cache · cây có bản `L` khai `da_bi_thay_the: N` mà **cây** không có `N` trỏ ngược (kể cả khi `N` nằm ở nhánh khác — F1 "cặp chia nhánh") · YAML của một bản `L` trong cây hỏng · cây có hai bản cùng `lease_id == L` mâu thuẫn |

Kiểm đối xứng bằng `_bia_mo_doi_xung(lease, cac_lease)` trên **toàn kho** là **sai** cho mục này: nó nhận
đầu mới nằm ở nhánh phụ (F1). Phải truyền đúng tập lease của cây canonical.

**Fail-close của dự báo:** `KHONG_XAC_DINH` là một trạng thái được IN, không làm tròn thành `KHONG`; nó
**không** đổi `rc` (bất biến M14). Hành vi luật cũ với bia mộ một chiều của lease còn hạn chạm đường dẫn
(`Chan` `KHÔNG_XÁC_ĐỊNH`, `rc=12`) giữ nguyên; lease hết hạn hoặc không chạm đường dẫn vẫn được bỏ qua như
hiện tại (ca `t123`). Tên nhánh mặc định lấy từ cờ `--nhanh-mac-dinh` đã có (mặc định `master`).

## 6. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

**A1–A3, A5, A8–A15 giữ nguyên nội dung r1** (tên và phép đo), trừ A13 (số ca nền nay là **168**). Dòng in đậm là mới hoặc đổi ở r2 (bản nháp 2 đổi A4, A6, A7, A7b, A16, A18–A22).

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| A1 | `hoso_adapter_do()` trả `schema_version == 2` và đúng tập khoá v2. | giữ `schema_version = 1` ⇒ ĐỎ; thêm một khoá lạ ⇒ ĐỎ. |
| A2 | `bam_ho_so` không đổi khi chỉ tầng AUDIT đổi. | đưa `git_sha256` trở lại dict được băm ⇒ ĐỎ. |
| A3 | `bam_ho_so` đổi khi bất kỳ khoá bắt buộc đổi. | bỏ một khoá khỏi tập được băm ⇒ đúng ca ấy ĐỎ; A2/A3 phải ĐỎ ngược chiều nhau. |
| **A4** | Ba trạng thái cho **từng** khoá `image_os` và `image_version` (tham số hoá theo khoá; khoá kia giữ hợp lệ): chuỗi ⇒ qua · `None` ⇒ qua nhưng **không** khớp mỏ neo đòi runner · thiếu khoá ⇒ `12`. | Với **mỗi** khoá: gộp `None` với thiếu khoá ⇒ đúng ca của khoá ấy ĐỎ; cho `None` khớp mỏ neo runner ⇒ đúng ca của khoá ấy ĐỎ. Bốn đột biến, bốn ca đích (F5 lượt 1). |
| A5 | `PROFILE_ADAPTER_DA_DUYET` rỗng vẫn ⇒ `12` trên đường production. | cho mỏ neo rỗng đi tiếp ⇒ ĐỎ. |
| **A6** | `MOC_BIA_MO_LICH_SU` **bằng** hằng Q6 `072181157a27804e69deb35bb792a88c70ac31e3` ghi trong **tệp test** (không đọc từ mã), khớp `^[0-9a-f]{40}$`, và **là tổ tiên** của `HEAD` của checkout (`git merge-base --is-ancestor`, `rc` đọc trực tiếp). Job `gate` checkout `fetch-depth: 0` (`ci.yml:90`) nên phép đo tổ tiên chạy được ở CI. | ghim OID khác ⇒ ĐỎ; ghim chuỗi 39 ký tự ⇒ ĐỎ. **KHÔNG ĐO ĐƯỢC** (object vắng, `rc` khác 0 và khác 1, không phải kho git) ⇒ ca **ĐỎ**, không bỏ qua êm; chỉ được tha khi cây rõ ràng là bản sao rời (không `.git`) — bài học `t24`. |
| **A7** | `_du_bao_check` với `BIA_MO_LICH_SU` **tiêm** trong ca (hằng thật rỗng) = `((L, N, b1, b2),)`, sổ rỗng: `(L, N)` ⇒ dự báo `rc` 0 · `(L, khác)` ⇒ 8 · `(khác, N)` ⇒ 8. | `any(...)` → `True` ⇒ hai ca 8 ĐỎ; chỉ so vế cũ ⇒ ca `(L, khác)` ĐỎ; chỉ so vế mới ⇒ ca `(khác, N)` ĐỎ. Ba đột biến, ánh xạ riêng (F5 lượt 1). |
| **A7b** | **Dự báo KHÔNG dẫn xuất lúc chạy** (r9 Q6: *"không lấy HEAD lúc A1"*). (i) `BIA_MO_LICH_SU == ()`. (ii) Kho giả có cặp hai chiều `Z → W` còn hạn trên **nhánh mặc định**, sổ rỗng: `_du_bao_check` cho lease `W thay_the_cho Z` ⇒ dự báo **8**. | đột biến dẫn xuất tập cặp từ cây hiện tại lúc chạy ⇒ (ii) ra 0 ⇒ ĐỎ. Đây là ca "mutant đọc cây sau ⇒ ĐỎ" của r9 Q6. |
| A8–A12 | B1–B5 như r1 (phân hạng theo LỚP ngoại lệ riêng + tên ca, không theo chuỗi thông điệp). | như r1. A11 ba `close()` = ba đột biến riêng. |
| **A13** | Suite `ops/lease_publish_test.py` **N/N hai số bằng nhau**, `N ≥ 168 + (số ca mới)`, `bỏ qua=0`. | đọc `rc` trực tiếp, không qua pipe. |
| A14 | `actionlint` DELTA = 0 so `origin/master`; thiếu `actionlint` hoặc `shellcheck` ⇒ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ. | nền đo ở §7 của phiên thi công. |
| A15 | `doctrine-scan` và `adr-song` `rc=0`. | chạy trực tiếp. |
| **A16** | `git diff --numstat <base_sha>..<reviewed_head>` chạm **đúng ba** đường write set, với `base_sha` là OID **bất biến** trong lease A1a (protocol §3.2.1) và `reviewed_head` là OID khai trong evidence — **không** dùng ref động (`origin/master`, merge-base tính lại). Việc nhánh có tụt sau nhánh mặc định hay không là phép kiểm **riêng**, không gộp vào đây. | thêm một đường ⇒ ĐỎ. Ca master tiến độc lập (thêm tệp ngoài write set sau `base_sha`) ⇒ phép đo **không** đổi (F7 lượt 1). |
| **A17** | **M12.** Ca đọc `.github/workflows/ops-thu-hoi-admission.yml` và đòi: đúng **một** dòng `uses:` tham chiếu `actions/upload-artifact`, và tham chiếu ấy **bằng đúng** `actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02`. Hằng Q1 nằm trong **tệp test**, không đọc từ workflow (đọc từ workflow thì ca so tệp với chính nó). | quay về `@v4` ⇒ ĐỎ; đổi một ký tự của SHA ⇒ ĐỎ; nhân đôi dòng `upload-artifact` (một ghim, một tag) ⇒ ĐỎ. |
| **A18** | **M13 — đo phía CONSUMER.** Consumer chỉ so **hai chuỗi digest** (`lenh_kiem_thu_hoi_github`, chốt `descriptor_sha256 != DESCRIPTOR_Q13_SHA256`); nó **không** nhận và **không** băm body comment. Nên A18 đo phép so digest, còn định nghĩa Q3 phía **producer** (body thô, không `\n` cuối) được chứng minh bằng **readback** §0 (REST, 15:55:00Z), không bằng ca unit. (i) `DESCRIPTOR_Q13_SHA256` khớp `^[0-9a-f]{64}$` và bằng hằng Q3 trong **tệp test**. (ii) **Đối chứng dương đầy đủ:** kho giả có marker MỚI với **mọi** điều kiện hợp lệ và `descriptor_sha256` = Q3 ⇒ `rc=0`, receipt có `descriptor_q13_ghim` = Q3. (iii) `descriptor_sha256` = `df81f47b50624d13faeb7a756b6f3573c999aef485ee8d741dbcd3d13ae2a7a8` (body **có** `\n`) ⇒ `12` tại chốt descriptor; lệch 1 ký tự ⇒ `12`. (iv) Bốn chốt còn lại của marker MỚI vẫn đứng: descriptor đúng nhưng từng điều kiện `first_policy_sha256` sai · `base_sha_before_add ≠ S` · S đã có policy · policy vắng ở T ⇒ mỗi ca `12`. Phân hạng theo **mã `Chan` + tên chốt**, không theo chuỗi thông điệp; ca policy vắng phải đòi đúng `Chan` 12 (bản vá hỏng có thể ném `TypeError` thay vì `Chan` — lượt 1 đo được). | để `None` ⇒ (i),(ii) ĐỎ; bỏ phép so descriptor ⇒ (iii) ĐỎ; nới phép so nhận thêm một digest (vd `in {Q3, df81f47b…}`) ⇒ ca `df81f47b` ĐỎ; gỡ từng chốt trong (iv) ⇒ đúng ca ấy ĐỎ. (iv) chứng minh việc ghim **không** mở cửa rộng hơn chốt descriptor (F4 lượt 1). |
| **A19** | **M14 — `CHE` và BẤT BIẾN verdict.** Kho giả dạng #564: trên nhánh mặc định, `L` có bia mộ đối xứng tới `N` (cả hai tệp trong cây); bản cũ của `L` **không** bia mộ nằm trên nhánh phụ `z-landed`; `L` còn hạn, chạm đường dẫn. Chạy `ai-dang-giu <đường>` **có** và **không** có `--du-bao`: (a) có dòng `DU_BAO: L · BIA_MỘ_MẶC_ĐỊNH=CHE`; (b) hai lần chạy cho **cùng** `rc` (=11), **cùng** dòng `NGƯỜI_GIỮ` (chứa `L`), và **cùng** tập dòng không mang tiền tố `DU_BAO:`. | đột biến "dự báo `CHE` thì bỏ `L` khỏi `NGƯỜI_GIỮ`" ⇒ (b) ĐỎ — đây là chốt **bất biến**, chốt quan trọng nhất của M14; bỏ dòng dự báo ⇒ (a) ĐỎ. |
| **A20** | **M14 — bia mộ ngoài nhánh mặc định không được `CHE`.** Bia mộ đối xứng của `L` (cả `L` lẫn `N`) chỉ nằm trên nhánh phụ `z-side`; cây mặc định có `L` **không** bia mộ ⇒ `BIA_MỘ_MẶC_ĐỊNH=KHONG`. | đột biến "hỏi mọi ref" ⇒ ra `CHE` ⇒ ĐỎ. |
| **A21** | **M14 — bẫy khử trùng.** Blob bia mộ của `L` có mặt **cả** trên nhánh mặc định **và** trên nhánh phụ `a-first` (sắp **trước**, nên `_quet_lease_toan_kho` ghi `a-first` cho blob ấy); blob cũ không bia mộ nằm trên nhánh thứ ba ⇒ `CHE`. **Tự kiểm fixture:** trong cùng ca, đòi `muc['ref']` của blob bia mộ **khác** ref nhánh mặc định — không thì fixture không dựng được bẫy và ca phải ĐỎ. | đột biến xác định "có trên nhánh mặc định" bằng `muc['ref']` ⇒ ra `KHONG` ⇒ ĐỎ. |
| **A22** | **M14 — `KHONG_XAC_DINH`.** (i) **Cặp chia nhánh:** cây mặc định có `L` khai `da_bi_thay_the: N` nhưng `N` chỉ nằm trên nhánh phụ ⇒ `KHONG_XAC_DINH`. (ii) Ref canonical vắng khỏi cache ⇒ dự báo in `KHÔNG ĐO ĐƯỢC`, và `rc`/`NGƯỜI_GIỮ` vẫn bằng lần chạy không `--du-bao`. (iii) YAML của bản `L` trong cây mặc định hỏng ⇒ `KHONG_XAC_DINH`. | đột biến kiểm đối xứng bằng `_bia_mo_doi_xung` trên **toàn kho** ⇒ (i) ra `CHE` ⇒ ĐỎ (F1 lượt 1); đột biến làm tròn `KHONG_XAC_DINH` thành `KHONG` ⇒ (i),(iii) ĐỎ; đột biến ném khi ref vắng ⇒ (ii) ĐỎ vì `rc` đổi. |

**Không tiêu chí nào đóng bằng `rc=0`.** Mỗi dòng đòi bằng chứng dương: hai số bằng nhau, `ok: true`,
hoặc một đột biến ĐỔI MÀU đúng ca đích. Ca đích phân hạng bằng **lớp ngoại lệ riêng + tên ca**
(bài học tín dụng giả #355/#359). Các chốt M14 phải phân biệt được bằng đầu vào: mỗi đột biến có **scope**
riêng nêu ở cột phải và phải làm đỏ **đúng** ca đích của nó; một đột biến thô làm đỏ nhiều ca không tự
chứng minh các ca tương đương, nhưng một đột biến có scope mà làm đỏ ca khác ngoài ca đích thì phải giải thích.

## 7. `hinh_dang_ke_thua` (L4)

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao" | **3** | r9 §1 (2) · **#564 dạng 2** (bia mộ ghi vào bản sao master, bản sao khác sống tiếp) |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | r9, #473 |
| **"nguồn được tin mà chưa xác minh"** | **7** | r9 lượt 1–6 · **A1a r2 lượt 1 F1** (M14 tin ref cache) |
| "cổng CÓ MẶT khác cổng ĐO ĐƯỢC" | 1 | #499 C2a |
| "gate xanh lane PR, master đo lần đầu" | 1 | #499 C3 |
| **"khử trùng giữ một đại diện, rồi hỏi đại diện câu hỏi về cả nhóm"** | **1** | M14 §5.1: `muc['ref']` là một ref trong nhiều |
| **"quyết định đổi bộ lọc bị đọc thành quyền đổi nguồn"** | **1** (mới) | A1a r2 lượt 1 F2 (M4 bản nháp 1) |

Hình dạng "nguồn được tin mà chưa xác minh" đã chạm **7** ở lượt 1 (F1). Checkpoint §12 đã chạy (vòng 3,
§0): cách làm đổi từ *"thêm chốt cho quyền xoá holder"* sang *"rút quyền"*. Một finding lớp ấy ở lượt sau
là lần 8, và nó phải nhắm vào chỗ **còn** trao thẩm quyền cho một nguồn chưa xác minh — không phải vào dự báo.

## 8. `chua_do_duoc` và điều kiện trước khi cấp lease

1. **Số dòng thêm — ƯỚC, chưa đo, và gần như chắc VƯỢT trần.** ADR-0044:5 cho `sensitive` **≤ 300 dòng
   thêm**, đếm cả test (`git diff --numstat`).

   | phần | ước (dòng thêm) |
   |---|---|
   | M1–M3 mã | 120–180 |
   | M4 (mốc + chú thích; tuple rỗng) | 5–12 |
   | M5–M9 mã | 50–70 |
   | M12 · M13 mã | 2–6 |
   | M14 mã (dự báo, đọc cây canonical) | 25–45 |
   | test M1–M9 (A4 nay tham số hoá hai khoá) | 110–180 |
   | test M4/M12–M14 (A6, A7, A7b, A17–A22) | 110–170 |
   | **tổng** | **422–663** |

   Đặc tả này **không** tự cấp ngoại lệ và **không** tự tách. Trước khi cấp lease, chủ kho chọn **một**:
   (a) ngoại lệ ADR-0044 có phạm vi (≤ 3 tệp, ≤ N dòng, chỉ cho A1a); hoặc (b) tách `M5`–`M9` (B1–B5)
   sang `THU-HOI-LEASE-A1c` bằng revision mới của đặc tả này. Khi `numstat` thật vượt trần đã được cấp,
   executor **DỪNG** và hỏi; không viết vào thân PR rằng cổng ADR-0044 "ĐẠT".

2. **`BIA_MO_LICH_SU` theo Q6 + (b) — dẫn xuất từ cây mốc, clock ghim.** Script
   `ops/reviews/thu-hoi-lease-a1a-r2/do_q6.py` (hiện vật review, **không** thuộc write set), dùng
   `yaml.safe_load` và `_danh_sach_thay_the_cho` của chính cổng, **không** regex, **không** đọc ref nào ngoài cây mốc:

   ```
   L     = mọi tệp ops/leases/* trong CÂY của MOC, parse bằng yaml.safe_load; trùng lease_id hoặc YAML hỏng ⇒ rc=3
   cặp   = (cũ, mới, blob cũ, blob mới): `mới` khai thay_the_cho ∋ cũ  VÀ  `cũ` (cùng cây) khai da_bi_thay_the == mới
   (b)   = trạng thái của `mới` tại clock C: HET_HAN (hạn ≤ C) · DA_BI_THAY (mới có bia mộ đối xứng TRONG CÂY)
           · KHONG_XAC_DINH (mới có bia mộ một chiều trong cây) ⇒ rc=3 · CON_HIEU_LUC ⇒ giữ
   C     = giờ commit của MOC (ghim, không phải giờ chạy)
   ```

   Chạy `python3 -B do_q6.py <kho> 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z` lúc **~22:53Z 26-09**
   (bản ghi `ops/reviews/thu-hoi-lease-a1a-r2/q6-do-2026-09-26.json`, `rc=0`; một lần chạy trước đó lúc 22:50Z với
   C = `2026-09-26T22:50:00Z` cho cùng kết quả): **92** lease trong cây; **0** YAML hỏng/trùng;
   **11** cặp hai chiều, digest biểu diễn sắp xếp `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48`;
   **3** cặp một chiều (không tính); **0** `KHONG_XAC_DINH`; cả 11 lease `mới` hết hạn, muộn nhất
   `2026-09-08T10:17:12Z`. Giờ commit của mốc là `2026-09-10T04:55:37Z` (`11:55:37+07:00`) ⇒ tại C, (b) giữ
   **0** cặp ⇒ `BIA_MO_LICH_SU = ()`. Kết quả **không phụ thuộc** C với mọi C ≥ `2026-09-08T10:17:12Z`, nên
   clock không phải một nguồn trôi. Executor chạy lại đúng lệnh trên tại lúc thi công và dán bản in vào thân
   PR; lệch digest hoặc lệch số cặp ⇒ **DỪNG**, không ghim.

   Hệ quả đã khai, không phải lỗ: cặp thay thế sinh **sau** mốc không vào hằng (r9 Q6 *"Feature tomb không
   bổ sung lịch sử"*), nên `_du_bao_check` dự báo `8` cho chúng — **bảo thủ**, không mở quyền nào, và
   `lenh_check` kiểm hạn trước khi dự báo (reviewer lượt 1 đã đọc). Chúng thuộc sổ thu hồi của A1b.

3. **Điều kiện cấp lease A1a (không suy từ giờ hết hạn):**
   - #579 **đã land** (PR #589 merged);
   - `ai-dang-giu` đo lại **ra `NGƯỜI_GIỮ 0`** trên cả ba đường write set, `rc` đọc trực tiếp, sau khi so
     tập tên ref hai nguồn như §1;
   - chủ kho đã chọn (a) hoặc (b) ở mục 1;
   - đặc tả này đã đóng băng bằng human audit.

   Chú ý tự tham chiếu: nợ `AG-T0-01B` dạng 2 (mà M14 chỉ **dự báo**, không chữa) có thể làm `ai-dang-giu`
   báo người giữ **giả** trên write set sau khi #579 land (bản sao lease #579 trên nhánh land chưa xoá). Nếu
   xảy ra, đường chữa là `ops-don-ref.yml` hoặc chờ hạn, **không** cấp lease chồng, và **không** dùng dòng
   `DU_BAO` của M14 làm căn cứ cấp — dự báo không có thẩm quyền.

4. **Tương thích consumer C1a1a.** Đặc tả `LAND-DOC-RECEIPT-THU-HOI-C1a1a` revision 5 (nhánh
   `claude/spec-c1a1-doc-receipt-20260925`, chưa trên master lúc đo) đã khai `descriptor_q13_ghim` là
   "`null` hoặc hex 64" và ghi rõ *"sẽ thành hex 64 khi A1a r2 ghim Q3"* ⇒ M13 **không** làm C1a1a đỏ.
   M12 đổi blob của workflow ⇒ `workflow_definition_sha256` trong receipt đổi; luật so blob/sha256
   workflow tại C thuộc **C1a1b** (git), không thuộc C1a1a. **KHÔNG ĐO ĐƯỢC** ở đây: tác động lên C1a1b
   (chưa có đặc tả).

5. **Tác động của schema v2 lên ca đang có** (r1 mục 7): số ca dựng hồ sơ v1 bị chạm **chưa đếm** — đếm
   trước khi vá, ghi delta.

6. **Mỏ neo profile đầu tiên** và **`NGAN_SACH_MAC_DINH`**: như r1 mục 6, 8 — ngoài A1a.
