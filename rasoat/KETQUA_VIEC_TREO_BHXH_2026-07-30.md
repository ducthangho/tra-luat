# KẾT QUẢ làm nốt việc treo — hồ sơ «Luật BHXH», 30-07-2026

Lượt này KHÔNG rà lại từ đầu: chỉ làm nốt danh sách treo của
`RASOAT_PROFILE_LUAT_BHXH_2026-07-29.md` §E và `KETQUA_DON_DU_LIEU_BHXH_2026-07-29.md` §5.

> ⚠ **ĐỌC §1-§9 KÈM PHỤ LỤC A.** §1-§9 viết ở PHA 1, khi NLM còn chết và chưa có duyệt ghi — nên chúng
> nói "chưa ghi gì" và "chờ duyệt". Sau đó người dùng cho phép `nlm-auth-load` + duyệt "làm theo khuyến
> nghị", nên **PHA 2 đã GHI THẬT**: 4 bước NLM + 5 món G. Chỗ nào §1-§9 mâu thuẫn Phụ lục A thì
> **Phụ lục A đúng** (nó đo sau). Bảng §0 dưới đây đã cập nhật cột kết quả cuối.

## 0. Kết quả gọn

| # | Mục treo | Kết quả lượt này |
|---|---|---|
| 1 | Đẩy GDoc BIDV | **XONG** (A.2) — 71→72 nguồn, cờ rụng |
| 2 | nạp Luật 41 | **KHÔNG CHẠY — báo động giả**, đẩy nữa là nhân đôi luật (A.3) |
| 3 | gỡ 3 PDF thô | **XONG** (A.2) — 72→69, `coverage_gap=0` |
| 4 | `nlm-reconcile` neo trạng thái | **XONG** (A.2) — `desync_real=0`, `audit-physical clean` |
| 5 | §E.3 — 2 PDF `DUTHAO_Luat_41_2024_QH15_*` | **ĐÓNG** — đã đổi tên xong, đo LIVE xác nhận (§3) |
| 6 | §E.7 — đăng ký BC 6193 + raw-twin | **XONG** — BC 6193 vào corpus + NLM, 20 song sinh đã đăng ký (A.4) |
| 7 | §E.8 — dọn locks + manifest-summary | **ĐÓNG — KHÔNG PHẢI RÁC**, cả hai nửa (§5) |
| 8 | §E.10 — cơ sở đếm `registry-doctor` | **ĐÃ XONG TỪ r229**, không phải làm lại (§2) |
| 9 | §5.3 — notebook `80742228` | **ĐÓNG** — 54/54 dòng thuộc hồ sơ KHÁC, 0 dòng BHXH (§6) |
| 10 | §5.4 — `chunk-apply` xuất `.md` | **r231 đã vá nhánh apply; PLAN còn hở → vá r251** (§2) |
| 11 | §E.9 — NQ Chính phủ cho VD-12 | **ĐÓNG, và đảo kết luận cũ** (§8) |
| — | §E.6 — vocab `hieuluc` | **XONG** — cờ DỰ THẢO 37 = nhãn 37, lệch 0 (A.4) |

Hai mục treo (#8, #10) hoá ra **đã được vá từ lượt trước** mà bảng §E chưa kịp cập nhật — §E viết
trước khi r229/r231 landed cùng ngày 29-07. Đã kiểm HÀNH VI, không chỉ đọc code.

---

## 1. NLM: vẫn CHẾT, và trên container này còn KHÔNG ĐO ĐƯỢC

```
nlm-auth-status → alive=false · why="nlm CLI không có trên PATH"
doctor          → rc=2 (chỉ vì nlm CLI + gws chưa nạp; credential=env OK, webapp ping 2.21.2p khớp)
```

**Đính chính một chỗ dễ tin lầm:** container này là container MỚI — `nlm` CLI chưa hề được cài, nên
`why` là *"không có trên PATH"*, **KHÔNG phải** một phép đo nói rotation token đã hết hạn. Nói cách
khác: lượt này **không đo được** liveness NLM, chứ không phải đo được là chết. Kết luận
"rotation token hết hạn" của lượt trước vẫn là căn cứ duy nhất.

Theo `RASOAT_HOSO_LOOP` §4b: KHÔNG tự chạy `nlm-auth-load`/`nlm-auth-pull` trong lượt rà ⇒ chuyển
chế độ không-NLM, đi tiếp. Mục 1-4 giữ nguyên thứ tự đã chốt (đẩy GDoc BIDV **trước**, gỡ PDF thô
**sau**) — không đảo được vì đảo là tạo lỗ hổng nguồn.

Hàng đợi vẫn đúng như bàn giao: `backlog=2`, `to_ingest=1` (`Luat_41-2024-QH15`),
`skipped_no_sohieu=1` (`VBT_BIDV_…`, cần `--allow-no-sohieu` — đúng bản chất, không phải khiếm khuyết).

## 2. Hai mục treo ĐÃ ĐƯỢC VÁ TỪ LƯỢT TRƯỚC — và một chỗ CÒN HỞ

### 2a. §E.10 (cơ sở đếm `registry-doctor`) — xong từ r229, không cần làm gì

`registry-doctor --json` LIVE đã trả sẵn:

```
count 94 · scanned 34 · skipped_ref 27 · skipped_own_thuong 33
basis: "count = TỔNG dòng registry; MỌI bucket dưới đây chỉ tính trên `scanned` …"
```

`27 + 33 + 34 = 94` ✓. Có selftest khoá (`r229_registry_doctor_noi_ro_co_so_dem`). **Đóng, không sửa lại.**

Nhân đây đối chiếu luôn **ba cách đếm "thiếu số hiệu"** mà lượt trước để ngỏ — cả ba đều đúng, khác cơ sở:

| Nguồn | Số | Cơ sở |
|---|---|---|
| đếm thẳng 94 dòng | **57** | mọi dòng có `sohieu` rỗng |
| `manifest.so_hieu_missing` | **57** | y hệt — khớp 1-1 |
| cờ `MISSING_SOHIEU` | **53** | 57 trừ 4 dòng `loai=thuong` mà TÊN TỆP đã mang số hiệu (`Nghị-định-233-2025-NĐ-CP.docx`, `…159…`, `Thông-tư-21-2025-TT-NHNN.docx`, `212_2025_ND-CP_666742.docx`) — cờ nghĩa là "không biết số hiệu", 4 ca này biết |
| `registry-doctor.missing_sohieu` | **25** | trên `scanned=34` |

Không có mâu thuẫn nào. Ghi lại để lượt sau không đi điều tra lần thứ ba.

### 2b. §5.4 (`chunk-apply` xuất `.md`) — r231 vá nhánh apply, PLAN vẫn nói dối ⇒ vá r251

r231 (v1.35.67) đã dựng cầu nối `_chunk_md_to_docx` (stdlib `zipfile`+XML). Kiểm HÀNH VI trên fixture
40 Điều / 86.479 ký tự: `chunk-apply` → 5 chunk · `chunk-verify` **13/13** · bản `.docx` do cầu nối
sinh ra **đi qua `profile-ingest` DRY `ok:true`**, đọc đúng 9 Điều.

**Chỗ CÒN HỞ:** cầu nối chỉ chạy trong nhánh `--apply`. Nhánh DRY vẫn in `planned_child_commands`
trỏ đường `.md`, kèm `ok: true`. Ai soi pipeline theo cách bình thường — chạy tay từng lệnh con
trước khi cho ghi — ăn `rc=2 UNSUPPORTED_EXTENSION` và kết luận pipeline gãy. **Đây đúng là lý do
lượt 29-07 phải "lách bằng cách dựng .docx thủ công" dù cầu nối đã có sẵn trong cây.**

Đã vá (r251, v1.35.88) — chi tiết + bằng chứng 2 chiều ở CHANGELOG ★ v1.35.88 Ca 1. Sau vá: chạy
**y nguyên** 5 lệnh con mà plan in ra ⇒ **5/5 `rc=0 ok=true`**, tổng 9+9+9+9+4 = **40 Điều** = đúng
số Điều fixture.

## 3. §E.3 — 2 PDF "mạo số hiệu": ĐÓNG, đo LIVE xác nhận

Đọc thẳng thư mục root profile qua webapp (`list`), đối chiếu với 94 `drive_id` LIVE:

| drive_id | Tên HIỆN TẠI trên Drive | Dòng registry |
|---|---|---|
| `1GM6QY15PhE9J7PA8jcfvjCcDlLBjg7xo` | `DUTHAO_TTr-BNV_2026_To_trinh_du_an_Luat_sua_doi_Luat_BHXH_16-7-2026.pdf` | không có (mồ côi) |
| `1UeiF7sKO3j03Ae20uwROilMmIgpsx6yt` | `CV_7728-BNV-CTL-BHXH_2026_Bao_cao_tien_do_du_an_Luat_BHXH.pdf` | không có (mồ côi) |

Tên mới đã landed. **Không còn tệp nào trong hồ sơ mang chuỗi `Luat_41_2024_QH15` gắn vào một bản
dự thảo** ⇒ rủi ro vớ nhầm dự thảo làm luật hiện hành: gỡ xong. Giữ mồ côi là ĐÚNG quyết định đã
chốt (cả hai là bản TRÙNG của dòng đã đăng ký: 0.944 và 0.885). Không có việc gì thêm.

## 4. §E.7 — BC 6193: đúng MỘT tài liệu chưa đăng ký, và một lỗi CODE lộ ra

### 4a. Kiểm kê mồ côi trên Drive — 26 mục, phân loại xong

| Nhóm | Số | Ghi chú |
|---|---|---|
| Hạ tầng | 2 | `tra_luat_manifest.LuatBHXH.json`, `tra_luat_registry.LuatBHXH` — đúng là không có dòng |
| **Trung gian `.docx` của đợt nạp Công báo** | **4** | `Luat_41…__part01/02.docx`, `Luat_41…_Bao_hiem_xa_hoi.docx`, `ND_159…_CongBao.docx` |
| Song sinh THÔ của dòng canonical | 19 | gồm 2 PDF ở §3; ILO C102/C168 là song sinh của dòng `ref` (`CU_ILO-102…`, `CU_ILO-168…`) |
| **Chưa đăng ký ở BẤT KỲ đâu** | **1** | `BC_6193_2026_BNV_CTL_V_v_tien_do_chuan_bi…pdf` (`1ksTzDiDXj4IEhWvjGPTj3CDJQwqlCz6U`) |

⇒ Sổ cũ (B7) liệt 12 tệp "không có dòng registry"; đo lại thì **11/12 là song sinh thô của dòng đã
có**, chỉ **BC 6193** là tài liệu thật sự khuyết. Đó là món §E.7 duy nhất.

**Cảnh báo mới — 4 tệp `.docx` trung gian là BẪY.** Chúng là bản LibreOffice/chunk dựng giữa đường
của đợt nạp Công báo, nằm cạnh bản canonical trong cùng thư mục, và theo BANGIAO §6c thì bản trung
gian **XẤU HƠN** bản trong kho (mang rác field-code `196856985` mà GDoc đã bỏ đúng). Ai mở Drive
chọn tệp bằng mắt rất dễ lấy bản trung gian. Đề xuất ở §7.

### 4b. BC 6193: KHÔNG phải bản quét — và `profile-ingest` từng nói dối về chuyện đó

DRY lần đầu trả `source_quality=ocr`, `probe_text_source=null`, `header_chars=0`,
`sohieu='6193_2026_BNV'` (rác), `loai=''`. Nhìn thì đúng hình dạng "PDF scan".

Đo lại bằng poppler: `pdfinfo` cho `Creator: Microsoft® Word 2019`, và `pdftotext` bóc **33.917 ký
tự** tiếng Việt sạch. **Nó là PDF số hoá, không phải bản quét.** Kết luận "scan" trước đó thuần là
artefact của container thiếu `pdftotext`.

Đây là **lỗi CODE thật, có sức nổ rộng** — đã vá trong lượt này (r251, CHANGELOG ★ v1.35.88 Ca 2).
Cùng tệp, cùng lệnh, chỉ khác việc máy có `pdftotext`:

| | thiếu `pdftotext` | có `pdftotext` |
|---|---|---|
| `sohieu` | `6193_2026_BNV` | `6193/BNV-CTL` |
| `loai` | *(rỗng)* | `Báo cáo` |
| `doc_name` | `VB_6193_2026_BNV_BC_6193_2026_BNV_CTL_…` | `BC_6193_2026_BNV_CTL_…` |
| **`plan_hash`** | `42ca6386…` | `71582728…` |

`ok:true`, rc=0 ở CẢ HAI, không một dòng cảnh báo. `plan_hash` lệch nghĩa là
`--expected-plan-hash` lấy ở máy A không dùng được ở máy B mà không ai biết vì sao.

**Vẫn cần `--ocr-verified` mới vào corpus** — `.pdf` luôn = `source_quality=ocr` là THIẾT KẾ, bản vá
không chạm. Nghĩa là: dù text sạch, BC 6193 vào corpus vẫn cần người cam kết đã đối chiếu.

**Một chỗ phải cẩn thận về số hiệu:** tên tệp khẳng định `BC_6193`, nhưng đọc thân văn bản thì
`6193/BNV-CTL&BHXH` là **công văn gửi lấy ý kiến phản biện xã hội của UBTW MTTQ**, còn tệp này là
**BÁO CÁO "V/v tiến độ chuẩn bị và một số nội dung lớn…"** gửi Thường trực UBVHXH, làm theo văn bản
`569/UBVHXH16` ngày 16/7/2026. Khối đầu văn bản **không hiện số/ký hiệu riêng của báo cáo**. Vậy
`6193` có thể là số của công văn ĐI KÈM, không phải số của chính báo cáo. Đúng bài học "mọi số
hiệu phải có năm và phải đúng" ⇒ **đừng để `profile-ingest` tự suy `sohieu`; phải truyền tay** sau
khi người dùng xác định. Đây là lý do món này vào §7 chờ duyệt chứ không tự chạy.

## 5. §E.8 — cả hai nửa: KHÔNG PHẢI RÁC

### 5a. `manifest-summary` — đã tươi, và nó tự sinh mỗi lần đọc

```
profile-manifest --json → generatedAt 2026-07-30T04:52:13Z · treeHash c753375c-94
                          count 94 · corpus_count 94   (= registry LIVE 94)
```

Không lệch một dòng. Con số cũ "43 / 25-06" là bản đọc **sheet** `manifest-summary` qua bộ render
Drive — đúng thứ §F đã tuyên là không đáng tin. Không có việc gì làm.

### 5b. `locks` — giữ `pending` là ĐÚNG THIẾT KẾ, dọn là sai

Đọc GAS `2.21.2p` (đúng bản `ping` LIVE trả về), cụm `ingest_claim`:

```js
CLAIM_TTL_MS_           = 5 * 60 * 1000;        // D4: 5 phút
CLAIM_GC_RETENTION_MS_  = 24 * 60 * 60 * 1000;  // D10: 24h cho committed/released

function _claimGcFilter_(rows, nowMs, retentionMs) { … return true; /* pending giữ nguyên — tự chữa qua reclaim (D10) */ }
function _claimAcquireDecide_(…) { … if (nowMs > Date.parse(existingRow.expires_at||0)) return {action:'grant', reason:'EXPIRED_RECLAIM'}; … }
```

⇒ Dòng `pending` hết hạn **không chặn gì cả**: lần acquire sau cùng `identity_hash` được cấp ngay với
lý do `EXPIRED_RECLAIM`. GC cố ý chỉ dọn `committed`/`released`. **Cùng họ với A1** (`files_bak_*` bị
tưởng là sheet rác): cả hai lần đều là cơ chế đúng thiết kế bị bộ render Drive làm cho trông như rác.

Hai điều phải nói thật kèm theo:
- **Không có endpoint nào đọc/dọn tab `claims`** (rà hết bảng endpoint API_CONTRACT). Nên con số
  "~12 dòng" **không kiểm lại được qua đường tin cậy** — nó đến từ bản đọc Drive. Muốn có số thật thì
  phải thêm endpoint chỉ-đọc, hoặc đọc Sheets bằng cred `gws`.
- Tôi **không** thử chứng minh `EXPIRED_RECLAIM` bằng cách acquire thật: việc đó GHI vào đúng cái tab
  đang bàn, và chưa được duyệt. Căn cứ ở đây là đọc GAS bản LIVE, đã nói rõ.

**Đề xuất: đóng nửa `locks` của §E.8 là "không làm, đúng thiết kế".**

## 6. §5.3 — notebook `80742228`: ĐÓNG, số dứt khoát

```
reg-query (scope hồ sơ, 94 dòng):  59e8d0de… = 82 · (rỗng) = 12 · 80742228… = 0
doctor --json:  UNKNOWN_NOTEBOOK_NOT_IN_TOPOLOGY = 0 ·  chuỗi "80742228" = 0 lần
reg-query --base-also (1358 dòng): 80742228… = 54, trong đó thuộc scope BHXH = 0
```

54 dòng đó là `Luật Xuất bản hợp nhất 43/VBHN-VPQH`, `Chương trình làm việc - NXB Giáo dục`,
`BC chuyên đề 02 — …xuất bản`… ⇒ đúng hồ sơ **«Khảo sát Luật XB»**, xác nhận kết luận KETQUA §5b.
Hồ sơ BHXH **sạch**; phần "notebook chưa khai trong topology" là việc của **kho NỀN**, không phải của
hồ sơ này. Ghi sang sổ dọn kho nền.

## 7. Món GHI — DRY xong, CHỜ DUYỆT (chưa chạy)

Xếp theo mức chắc chắn. Không món nào đã chạy.

| # | Việc | Điểm chạm | Vì sao |
|---|---|---|---|
| G1 | 2 dòng thiếu nhãn DỰ THẢO (§9) | `reg_bulk` 2 dòng, field `hieuluc` | Cờ `DRAFT_NOT_EFFECTIVE` đã bắt, nhãn còn rỗng — rào an toàn mà profile style bắt buộc |
| G2 | 3 dòng `corpus` RỖNG → `false` (§9) | `reg_bulk` 3 dòng, field `corpus` | Rỗng không phải true cũng chẳng phải false; 4 dòng em ruột cùng bộ đều `false` |
| G3 | Đăng ký BC 6193 | `profile-ingest --apply` + `--name`/`--sohieu` TRUYỀN TAY | Tài liệu thật sự khuyết duy nhất. **Cần bạn chốt số hiệu trước** (§4b) |
| G4 | 4 tệp `.docx` trung gian | quyết: xoá, hay `move` vào `_meta` | Bản xấu hơn bản trong kho, đứng cạnh bản canonical ⇒ bẫy chọn tay (§4a) |
| G5 | Chính sách raw-twin | quyết chính sách, chưa phải lệnh | xem dưới |

**G5 — raw-twin, đây là chỗ cần bạn quyết, kèm số đo:**

Hiện trạng **không nhất quán**: 22 dòng `loai=thuong` (đều `corpus=false`) đã đăng ký, còn 19 song
sinh thô khác thì mồ côi. Giá trị của dòng `thuong` là **chống nạp trùng** (dedup-gate chặn khi ai đó
nạp lại đúng tệp thô đó).

- *Đăng ký nốt 19* → dedup đồng đều; giá phải trả: +19 dòng, và `missing_sohieu` / `loai_noncanonical`
  ồn thêm (đã biết là ồn theo cơ sở đếm, xem §2a).
- *Bỏ đăng ký 22* → registry gọn; mất lá chắn dedup, và mất dấu vết xuất xứ.
- **Khuyến nghị của tôi: ĐĂNG KÝ NỐT 19** — rẻ, đối xứng, và luật corpus phía server vốn đã loại
  `loai='thuong'` nên không làm sai con số corpus nào. **Trừ 4 tệp trung gian ở G4** — chúng không
  phải "bản gốc" của gì cả, đăng ký là hợp thức hoá một bản xấu.

## 8. §E.9 / VD-12 — ĐÓNG, và kết luận cũ bị ĐẢO

Câu hỏi cũ: *tìm "văn bản công bố tiếp tục hiệu lực" cho NĐ 30/2016, dạng NGHỊ QUYẾT CHÍNH PHỦ
(tiền lệ NQ 31/NQ-CP 03/3/2026).*

**Trả lời: không có NQ nào để tìm, và không cần có.** Căn cứ hiệu lực còn lại của NĐ 30/2016 nằm
NGAY TRONG NĐ 212/2025, kèm điều kiện tự tắt. Nguyên văn lấy bằng `tl extract` trên **bản corpus**
(`1vXZQ5K03E…`, `corpus=true`, `nlm=pushed`) — nguồn đã verify, KHÔNG phải RAG:

> **Điều 24. Hiệu lực thi hành**
> 1. Nghị định này có hiệu lực thi hành kể từ ngày ký.
> 2. Nghị định số 30/2016/NĐ-CP … hết hiệu lực thi hành kể từ ngày Nghị định này có hiệu lực thi
> hành. Đối với quy định tại điểm đ khoản 1, khoản 2 Điều 4 và Điều 11 Nghị định số 30/2016/NĐ-CP
> tiếp tục thực hiện cho đến khi Luật Việc làm số 38/2013/QH13 ngày 16 tháng 11 năm 2013 hết hiệu
> lực thi hành.

(Điều 23 khoản 5 nói cùng nội dung cho hình thức đầu tư "dự án quan trọng do Thủ tướng phê duyệt".)

Cơ chế NQ-CP kiểu NQ 31/NQ-CP dùng cho ca KHÁC: khi một **LUẬT** mẹ bị thay mà các nghị định con
không có điều khoản chuyển tiếp, Chính phủ phải ra NQ công bố chúng tiếp tục hiệu lực. Ở đây việc
thay diễn ra ở cấp NGHỊ ĐỊNH và nghị định thay đã tự mang điều khoản ⇒ không sinh NQ.

### 8b. Và điều kiện tự tắt ĐÃ NỔ — sổ rà đang ghi lỗi thời

Sổ ghi «`30-2016-NĐ-CP` còn hiệu lực **MỘT PHẦN** theo Đ23k5+Đ24k2 NĐ 212». Truy tiếp mốc tắt —
`Luat_74-2025-QH15_Viec_lam` (`1PfTsnRY…`, `corpus=true`, kho nền), cùng đường `tl extract`:

> **Điều 54. Hiệu lực thi hành**
> 1. Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026.
> 2. Luật Việc làm số 38/2013/QH13 đã được sửa đổi, bổ sung một số điều theo Luật số 41/2024/QH15
> hết hiệu lực kể từ ngày Luật này có hiệu lực thi hành, trừ trường hợp quy định tại các khoản 1, 2
> và 3 Điều 55 của Luật này.

(Luật 74/2025 thông qua 16/6/2025, Kỳ họp thứ 9 Quốc hội khoá XV.)

⇒ Chuỗi suy: `38/2013/QH13` hết hiệu lực **01/01/2026** ⇒ `điểm đ k1, k2 Điều 4 và Điều 11` NĐ
30/2016 **hết hiệu lực từ 01/01/2026**. Hôm nay 30-07-2026 ⇒ **NĐ 30/2016 hết hiệu lực TOÀN BỘ**,
không còn "một phần". Ghi chú "còn hiệu lực MỘT PHẦN" chỉ đúng trong khoảng **25/7/2025 – 31/12/2025**.

**Ảnh hưởng tới thẩm tra Điều 122 (đầu tư quỹ):** lý do nạp NĐ 30/2016 đổi bản chất — không còn là
"luật đang áp dụng" mà là **tham chiếu lịch sử**, và vẫn CẦN, vì Đ23 k2/k3 NĐ 212 giữ các **hợp đồng
gửi tiền / hợp đồng theo Điều 14** ký trước 25/7/2025 chạy **đến hết thời hạn** — muốn kiểm những hợp
đồng đó thì phải có văn bản gốc. Đề nghị sửa nhãn trong Q-INGEST cho đúng.

*Nói rõ giới hạn nguồn:* cả hai trích dẫn đọc từ **bản Google Doc trong kho** (`--markup strip`), và
`extract` có cảnh báo rằng bản GDoc không CHỨNG MINH được đã lọc markup. Với điều khoản hiệu lực
thuần (không phải dự thảo có markup) thì chấp nhận được; neo mạnh nhất vẫn là bản Công báo. Nếu định
dùng hai đoạn này trong văn bản thẩm tra chính thức thì nên đối chiếu Công báo trước.

*Ghi thêm cho sổ dọn kho nền:* `Luat_74-2025-QH15_Viec_lam` có **2 dòng** cùng số hiệu, khác
`drive_id` (`1PfTsnRY…` corpus=true · `1mGRs4vs…` corpus=false) — cùng rọ B3, kho nền xử lý.

## 9. §E.6 — vocab `hieuluc`: gần xong, còn 2 dòng (+ 3 dòng bệnh khác)

Đo LIVE 94 dòng: `hieuluc` chỉ còn **3 giá trị** — `''` 45 · `DỰ THẢO — chưa hiệu lực` 25 · `Còn` 24.
Bộ chuẩn `{Còn, Hết, Chưa}` giữ nguyên. **Không dòng dự thảo nào mang nhãn `Còn`** ⇒ việc chính của
§E.6 đã xong.

**Còn dư việc thật — 2 dòng CÓ cờ `DRAFT_NOT_EFFECTIVE` mà nhãn `hieuluc` RỖNG** (cờ 27 vs nhãn 25):

| drive_id | Tên | `loai` | `hieuluc` |
|---|---|---|---|
| `1uAbxo_NjsJ0o5PYeYcuqlklg1KPXFR9d` | `02. Du thao Luat 16.06.2026 - PCT (ban sach).pdf` | `thuong` | *(rỗng)* |
| `1HtV9jEGyHuM_ACQ5c9b4qsXIku6GEbwe` | `01. Du thao To trinh Chinh phu_16.6.2026 - PCT (ban sach).pdf` | `thuong` | *(rỗng)* |

Lượt trước sửa 12 nhãn trên các dòng canonical; hai dòng này là bản THÔ nên trượt ra ngoài. Chiều
ngược lại sạch: **0 dòng có nhãn mà thiếu cờ**. → G1.

**Phát hiện MỚI — 3 dòng `corpus` RỖNG** (không `true`, không `false`):

| drive_id | Tên | `loai` |
|---|---|---|
| `13dQ-k8Rt68Vkb9ja4qXpyKoIeJCD-FL68iMh7gzffww` | `VBT_BC_BHXH_HaNoi_thuc_hien_chinh_sach_phap_luat_BHXH_2025` | `Báo cáo` |
| `18e7DoDOMQKf95EFG7_ha-8Z9Hul9tqbLCzwAd_EkObY` | `VBT_PL_BC_BHXH_HaNoi_thuc_hien_chinh_sach_phap_luat_BHXH_2025` | `Phụ lục` |
| `1vD6Dy5egI42xHfGzOfJp-7eeDnNbGmkTybwyzRQz-w8` | `VBT_BC_ATVSLD_BQL_KCN_ThaiNguyen_2025` | `Báo cáo` |

Bốn dòng em ruột cùng bộ (`…ThaiNguyen…` BC + PL1/2/3) đều `corpus=false` ⇒ 3 dòng này gần như chắc
chắn phải là `false`. Rỗng thì luật client (`corpus=='true'`) coi như false, nên **hôm nay chưa lệch
con số nào** — nhưng nó là ô mờ nghĩa, sớm muộn có người đọc thành "chưa quyết". → G2.
**Lưu ý cách ghi:** đây là điền `false`, KHÔNG phải xoá field ⇒ đi `reg_bulk` được; nếu có lúc nào cần
XOÁ hẳn field thì phải đi `reg_clear` (webapp BỎ QUA giá trị rỗng qua `reg_bulk`/`upsert`).

## 10. Món mang sang lượt sau (không phải việc của lượt này)

- **B4 xác nhận LIVE, vẫn mở:** cả **10/10** tệp thế hệ 16.6.2026 còn nguyên trong thư mục con
  «Hồ sơ Luật», trong khi 10 dòng registry ghi `nlm_status=removed_from_drive`. Trạng thái đó nói một
  việc **không hề xảy ra**. Kèm `removed_family_still_pointing: 10` (KETQUA §5b). Cần `superseded_by`
  / note thế hệ để khỏi trích bản cũ; `nlm-reconcile --clear-stale` thì chờ NLM sống.
- Kho NỀN: `80742228` chưa khai topology · 2 dòng `Luat_74-2025-QH15` trùng · B2/B3/B5 cũ.
- 2 vá code lượt trước ĐỀ XUẤT mà chưa làm: guard doctype trước khi ép cat 46 → **đã làm ở r231 Ca 1**;
  chặn `NAME_TRICH_YEU` khi tên khớp `phan_N_cua_M` → **đã làm ở r231 Ca 2**. Cả hai đóng.

## 11. Lệnh đã chạy trong lượt này (đều chỉ-đọc / DRY)

`doctor [--json]` · `reg-query [--refresh/--base-also/--limit]` · `registry-doctor --json` · `sweep --json` ·
`ingest-missing --json` · `nlm-auth-status --json` · `profile-manifest [--json] [--refresh]` ·
`profile-files --json` · `profile-doctor --json` · `download --file-id` · `ocr-analyze` ·
`extract [--dieu/--find]` · `chunk-apply` · `chunk-verify` · `profile-ingest-chunks` (DRY) ·
`profile-ingest [--drive-id]` (DRY) · webapp `list` (GET, chỉ đọc).

## 12. Trạng thái cuối (đo 30-07-2026)

| Chỉ số | Giá trị |
|---|---|
| registry | `count=94` (lượt trước 93) |
| `hieuluc` | 3 giá trị: `Còn` 24 · rỗng 45 · `DỰ THẢO — chưa hiệu lực` 25 |
| `corpus` | `true` 46 · `false` 45 · **rỗng 3** (§9) |
| `registry-doctor` | `scanned=34` / `count=94`, có `basis` · `missing_sohieu=25` · `duplicate_sohieu_groups=1` (3 dòng Luật 41: canonical + 2 chunk — đúng thiết kế) |
| manifest | `count=94` · `treeHash c753375c-94` · tươi |
| cờ | `MISSING_SOHIEU` 53 · `DRAFT_NOT_EFFECTIVE` 27 · `ORPHAN_CAT` 20 · `CORPUS_TRUE_NOT_ON_NLM` 2 |
| NLM | **không đo được** trên container này (thiếu `nlm` CLI) — mục 1-4 vẫn chặn |
| Drive root | 63 mục · 26 mồ côi (phân loại ở §4a) · «Hồ sơ Luật» 10 tệp |
| selftest | **1399/1399** · VERSION **1.35.88** |
| ruff `--select F` | DELTA theo TÊN so master: `tl.py` 0 · `chunking.py` 0 · `tl_selftest.py` 0 · `ingest_ops.py` +1 (`PROFILE_INGEST_ALLOWED_EXTS`, re-home I11, đã kiểm hành vi) · F401 0 |

---

# PHỤ LỤC A — NLM đã sống lại: chạy nốt 4 bước + 5 món GHI (cùng ngày 30-07-2026)

Người dùng cho phép `tl nlm-auth-load` và duyệt "thực hiện theo khuyến nghị". Phần này ghi những gì
ĐÃ GHI THẬT.

## A.1 Cài `nlm` + xác thực

`tl nlm-install` (không cần `--resume` — container này không bị trần 45s/lệnh): tải Python 3.11
standalone 30,9 MB từ Drive (md5 khớp) → cài `notebooklm-mcp-cli` → `nlm 0.9.4` tại
`/root/.local/bin/nlm`. `doctor` gate `nlm CLI (fast-lane)` chuyển ✓.

**Chẩn đoán đổi sau khi cài:** trước đó `why="nlm CLI không có trên PATH"` (không đo được gì); sau khi
cài, `nlm rc=1: Profile 'default' not found` — tức container mới, CHƯA có bundle, **không phải** rotation
token chết. `tl nlm-auth-load` → bundle **~0 ngày tuổi (2 phút)** ⇒ routine auto-refresh r250 đang chạy
tốt. `alive=true`.

## A.2 Bốn bước NLM

| # | Việc | Kết quả |
|---|---|---|
| 1 | `nlm-add` GDoc BIDV | `source_id 3f1dd2e8…` ready · **71→72** nguồn · dòng BIDV `nlm_status=pushed` · cờ `CORPUS_TRUE_NOT_ON_NLM` rụng · journal `nlm-add-link_1785391381_4884` |
| 2 | nạp `Luat_41-2024-QH15` | **KHÔNG CHẠY — báo động giả**, xem A.3 |
| 3 | gỡ 3 PDF thô ngân hàng | **72→69** nguồn · `coverage_gap=0` · 3 con trỏ treo đã dọn (`nlm-reconcile_1785391865_13641`) |
| 4 | neo trạng thái | `desync_real=0` · `coverage_gap=0` · `nlm_claim 69 = physical 69 = live 69` · `audit-physical clean=true` |

**Trước khi gỡ, đã đo lỗ hổng nguồn — và phải đo tới HAI lần mới đúng.** Lần đầu so bản GDoc với text
`pdftotext` của PDF thô: Agribank ra 2 byte, Vietcombank 4 byte ⇒ **hai PDF đó là bản QUÉT, không có
lớp text**, so kiểu đó vô nghĩa. Phép đo đúng là so **nội dung NotebookLM đang giữ** (NLM tự OCR):

| cặp | từ (thô → GDoc) | phủ 5-gram của bản thô trong GDoc |
|---|---|---|
| Agribank | 1020 → 1024 | 96,06% |
| Vietcombank | 1971 → 1974 | 96,19% |
| BIDV | 1032 → 1033 | 98,93% |

Phần lệch là **rác OCR của bản thô** (`βηχη`, `bhχη`, `luru`, `jơng`, `oại` — GDoc không có), tức GDoc
sạch hơn. Hai "lỗ hổng" tôi tưởng tìm được (ngày ký Agribank; `14/2025` của Vietcombank) đều là
**regex của tôi tự bắt sai**: so lại sau khi bỏ SẠCH khoảng trắng thì `ngày23tháng6năm2026`,
`10593/NHNo-ALCO`, `14/2025/TT-NHNN`, `15/09/2025`, `10838` đều CÓ ở cả hai bên. `coverage_gap=0` của
`nlm-reconcile` sau khi gỡ là bằng chứng chốt.

## A.3 Vì sao KHÔNG nạp Luật 41 — và footgun phải vá

`note` của dòng canonical đã ghi sẵn: *"NLM đi qua 2 chunk part01/part02 nên dòng này corpus=true mà
không mang nlm_source_id"*. Đo lại: 2 chunk đã `pushed`, `chunk-plan` cho `total 183.428 = part01
99.043 + part02 84.385`, **hụt 0**, Điều 1..64 + 65..141 = đủ 141 Điều.

⇒ Đẩy bản canonical nữa là **nhân đôi toàn bộ luật** trên notebook — đúng loại rác lượt trước phải dọn
(69→74→71). Thêm nữa 183k > ngưỡng chunk 100k nên chính sách vốn không cho đẩy một nguồn cỡ đó.

**`backlog=2 / to_ingest=1` là BÁO ĐỘNG GIẢ** — trạng thái đích đã đạt. Suýt nữa chính chỉ dẫn của
lượt này làm hỏng notebook. Cờ `CORPUS_TRUE_NOT_ON_NLM` và `ingest-missing` chưa biết khái niệm "phủ
bằng chunk con": chúng không tra dòng `__partNN__` cùng số hiệu đã `pushed`. **Việc cần làm (chưa
làm):** dạy hai chỗ đó nhận diện phủ-bằng-chunk, để hết mời nạp trùng.

## A.4 Năm món GHI — đã chạy

| # | Việc | Kết quả |
|---|---|---|
| G1 | 2 dòng thiếu nhãn DỰ THẢO | xong (`register_1785392091_16548`, `…392106_16551`) |
| G2 | 3 dòng `corpus` RỖNG → `false` | xong (`register_1785392000_15821`, `…392056_16541`, `…392075_16544`) — kiểm 1 dòng đầy đủ: CHỈ `corpus` đổi, `loai`/`cat`/`nlm_source_id`/`nlm_status`/`hieuluc`/`row_kind` nguyên vẹn |
| G3 | đăng ký BC 6193 | GDoc `1h0OfDtHG0Hm…` · `corpus=true` · NLM `43a3b93c…` · **sohieu ĐÃ XOÁ** |
| G4 | 4 `.docx` trung gian | `move` vào `_meta` (KHÔNG xoá — hồi được) |
| G5 | 20 song sinh thô | đăng ký `loai=thuong · corpus=false · row_kind=own`, 42/42 đồng nhất |

**G3 — số hiệu: đã xoá, và đây là lý do.** Đọc kỹ văn bản: khối đầu chỉ có `BỘ NỘI VỤ` / `BÁO CÁO` /
`V/v tiến độ chuẩn bị…`, **không dòng `Số:`, không dòng ngày, không khối ký**; kết thúc `Trên đây là báo
cáo của Bộ Nội vụ…/.`. Ba số `/BNV` trong thân đều là **dẫn chiếu văn bản KHÁC**: `3895` (23/4/2026),
`6192` (xin ý kiến 34 Đoàn ĐBQH), `6193` (gửi lấy ý kiến phản biện xã hội UBTW MTTQ). Vậy `6193` trong
tên tệp là số của **CÔNG VĂN**, không phải của báo cáo. Đã `--clear-cols sohieu --confirm yes` + ghi
`note` giải thích. Tên chuẩn: `DUTHAO_VBT_BC_BNV_tien_do_va_noi_dung_lon_du_an_Luat_BHXH_2026`
(profile-ingest tự thêm tiền tố `DUTHAO_` vì nhãn dự thảo).
Đối chiếu GDoc ↔ PDF nguồn trước khi cho vào corpus: **5461 → 5464 từ, phủ 5-gram 98,52%, 0 từ thiếu**,
mọi dẫn chiếu + mốc ngày còn đủ.

**Nhất quán nhãn:** sau G5, 9 dòng song sinh `DUTHAO_*` mang cờ `DRAFT_NOT_EFFECTIVE` mà nhãn rỗng ⇒ đã
gắn nhãn cho cả 9 (`reg_bulk` cols=hieuluc, patched 9/9). Nay **cờ 37 = nhãn 37, lệch 0**.

## A.5 Ba cái bẫy công cụ gặp trong lượt ghi (ghi để không mất lần nữa)

1. **`tl register` GHI NGAY, không DRY-by-default.** Tôi giả định sai và ghi sớm hơn dự định một dòng
   (`13dQ-k8R…`). Đã kiểm ngay: chỉ `corpus` đổi, không hư hại phụ, journal undo được. Các lệnh khác
   trong bộ này (`source-update-corpus`, `nlm-source-remove`, `nlm-reconcile`) đều DRY-by-default —
   `register` là ngoại lệ.
2. **`reg_bulk` nhận `cols` là CHUỖI phân tách bằng dấu phẩy, KHÔNG phải JSON.** GAS làm
   `String(p.cols).split(',')` ⇒ truyền `["note"]` thì ALLOW rỗng và trả `cols không hợp lệ (phải thuộc
   REG_COLS_)` — nghe như tên cột sai, thực ra là định dạng sai.
3. **`register` báo `FIELDS_DROPPED_ON_WRITE` / `verified=false` cho 18/18 dòng mà THỰC TẾ ghi ĐỦ CẢ 18.**
   Đo lại registry: `count 99→115`, `loai=thuong 26→42`, cả 18 dòng có `name`. Nguyên nhân: readback
   xác minh đọc qua cache GAS (TTL ~600s) nên không thấy dòng nó vừa ghi. **Đây là cổng báo ĐỎ OAN** —
   mặt ngược của bài học "rc=0 có thể bị lừa"; cả hai chiều đều phải đòi bằng chứng dương từ dữ liệu.
   *Việc cần làm (chưa làm):* readback của `register` nên bust cache trước khi kết luận.

## A.6 Vá code thêm trong lượt này

- **r251 (v1.35.88)** — 2 cổng xanh mà nói dối: PLAN `profile-ingest-chunks` in lệnh không chạy nổi;
  plan ingest suy metadata TỪ TÊN TỆP khi máy thiếu `pdftotext`.
- **r252 (v1.35.89)** — `&amp;` `&lt;` chui NGUYÊN VĂN vào kho: 3 reader `.docx` bóc tag mà quên
  unescape. Bắt được đúng lúc đối chiếu BC 6193: `tl extract` trả `6193/BNV-CTL&amp;BHXH` còn webapp
  `exporttext` đọc `&` trần 3/3 chỗ ⇒ **sai ở đường đọc của ta, không phải ở corpus**. Gom về
  `docx_markup.plain_from_document_xml()`. ⚠ cache `extract_*` cũ mang text sai — đã xoá cache của hồ
  sơ này; hồ sơ khác nên xoá khi đọc lại.

*Tự phê:* lúc bump VERSION tôi dùng `Path.write_text` cho `SKILL.md` — hàm đó **chuẩn hoá CRLF→LF**, làm
mất 307 byte và `golden`/`selftest` đỏ. Đã `git checkout` rồi bump lại bằng byte. SKILL.md và
tl_selftest.py là tệp CRLF; sửa chúng phải đi đường bytes.

## A.7 Trạng thái cuối (đo sau bước cuối)

| Chỉ số | Trước lượt | Sau lượt |
|---|---|---|
| registry `count` | 94 | **115** (+1 BC 6193 GDoc, +20 song sinh thô) |
| `corpus` | true 46 / false 45 / **rỗng 3** | true 47 / false 68 / **rỗng 0** |
| `hieuluc` | Còn 24 · rỗng 45 · DỰ THẢO 25 | Còn 24 · rỗng 54 · **DỰ THẢO 37** |
| cờ DỰ THẢO vs nhãn | 27 vs 25 (lệch 2) | **37 vs 37 (lệch 0)** |
| `loai=thuong` | 22 | **42** |
| `CORPUS_TRUE_NOT_ON_NLM` | 2 | **1** (bản canonical Luật 41 — báo động giả, xem A.3) |
| NLM nguồn | 71 (không đo được) | **70** LIVE (+BIDV +BC 6193, −3 PDF thô) |
| `desync_real` / `coverage_gap` | — | **0 / 0** |
| `nlm-audit-physical` | — | **clean=true** |
| Drive root mồ côi | 26 | **2** (chỉ manifest + registry = hạ tầng) |
| selftest / VERSION | 1395 / 1.35.86 | **1400 / 1.35.89** · gate xanh 8/8 |

## A.8 Còn treo sang lượt sau

1. **B4** — 10/10 tệp thế hệ 16.6.2026 vẫn nằm trong «Hồ sơ Luật» mà registry ghi
   `nlm_status=removed_from_drive` (nói một việc KHÔNG xảy ra); `removed_family_still_pointing=10`.
   Cần `superseded_by`/note thế hệ. NLM đang sống nên lượt sau làm được.
2. **Vá cờ phủ-bằng-chunk** (A.3) — để `ingest-missing` hết mời nạp trùng bản canonical.
3. **Vá readback `register`** (A.5 mục 3) — bust cache trước khi kết luận `verified`.
4. Kho NỀN: `80742228` chưa khai topology · 2 dòng `Luat_74-2025-QH15` trùng · B2/B3/B5 cũ.
5. Xoá cache `extract_*` của các hồ sơ KHÁC (hệ quả r252).
