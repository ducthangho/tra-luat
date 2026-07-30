# RÀ SOÁT PROFILE «Luật BHXH» — lượt 30-07-2026 (tiếp lượt 29-07)

Chạy trên máy Windows canonical (`C:\qh\tra-luat` = `D:\Quốc hội\tra-luat`), Python 3.13.
**NLM CHẾT cả lượt** ⇒ chạy chế độ không-NLM theo `RASOAT_HOSO_LOOP` §4b, KHÔNG tự chạy
`nlm-auth-load`/`nlm-auth-pull` để sửa auth trong lượt rà (một lần thử theo yêu cầu trực tiếp của người
dùng — kết quả ở §D).

Mọi khẳng định dưới đây neo `reg-query`/endpoint GAS hoặc lệnh `tl` chạy được, KHÔNG neo bản đọc Drive
(bài học §F lượt trước). Số nào đo bằng lệnh nào đều ghi kèm.

---

## A. ĐO LẠI TRƯỚC KHI TIN — và một số của chính prompt bàn giao là BÁO GIẢ

| Phép đo | Kết quả 30-07 | So mốc bàn giao |
|---|---|---|
| `doctor` | rc=2 — chỉ vì `nlm auth (LIVE probe)` đỏ; 14/15 cổng còn lại xanh | khớp |
| `reg-query --refresh --no-base-also` | **94 dòng** (mặc định profile BẬT base-also ⇒ 1358 dòng: 1264 nền + 94 hồ sơ) | 93 → 94 |
| `sweep` | `corpus` client **46** / luật server **31** · `loai_noncanonical` **0** · `raw_on_nlm` **3** · `nlm_drift.CORPUS_TRUE_NOT_ON_NLM` **2** | 45/30 → 46/31 |
| `nlm-auth-status` | `alive=false` — LIVE probe: `Authentication expired` | khớp (chết) |
| `ingest-missing` (không `--refresh`) | `backlog=0`, snapshot **2026-07-27T16:27** | prompt nói 2 |
| `ingest-missing --refresh` | `backlog=2`, `to_ingest=1`, snapshot 2026-07-30T03:37 | khớp |

★ **`backlog=0` là BÁO GIẢ do snapshot nguội 3 ngày.** Đúng công thức đo mà prompt bàn giao ghi
(`tl ingest-missing --json`, không `--refresh`) thì ra 0 — trong khi `sweep` cùng phiên đã nói
"2 chưa push NLM". Cùng họ bài học `reg-query --refresh` (nạp chồng 9 tài liệu 24-07):
**số 0 trên dữ liệu nguội không phải là sạch.** Đã vá thành cờ có tên (§C mục 3).

★ **`reg-query` ở profile dự án mặc định quét CẢ kho nền.** Lượt trước ghi "đúng 90 dòng" là số
`--no-base-also`; chạy trần ra 1358. Không phải lỗi (`TL_BASE_ALSO=1` là thiết kế v1.30.0), nhưng mọi
con số registry của hồ sơ PHẢI nói rõ đã `--no-base-also` chưa, kẻo lệch 14 lần.

---

## B. Việc "còn treo" — 4/11 mục HOÁ RA ĐÃ XONG, đo mới biết

Prompt bàn giao dựng từ §E của báo cáo 29-07, nhưng chính phiên đó về sau (v1.35.65→v1.35.86) đã vá
mất mấy mục. Đối chiếu lại trước khi làm (đúng dặn dò "đừng làm lại mù"):

| Mục | Trạng thái đo được 30-07 |
|---|---|
| §E.3 — 2 PDF mạo số hiệu `DUTHAO_Luat_41_2024_QH15_*` | ✅ **XONG**. Đo qua GAS `list`: `1GM6QY15…` nay là `DUTHAO_TTr-BNV_2026_To_trinh_du_an_Luat_sua_doi_Luat_BHXH_16-7-2026.pdf`, `1UeiF7sK…` là `CV_7728-BNV-CTL-BHXH_2026_Bao_cao_tien_do_du_an_Luat_BHXH.pdf`; đối chiếu 94 dòng LIVE: KHÔNG dòng nào trỏ 2 `drive_id` này. Rủi ro vớ nhầm dự thảo làm luật hiện hành: đã gỡ. |
| §5.4 — `chunk-apply` xuất `.md` mà `profile-ingest` không nhận | ✅ **XONG từ r231** — `chunking._chunk_md_to_docx` vật chất hoá `.docx` bằng stdlib, có test `r231_chunk_docx_stdlib_doc_lai_duoc`. |
| §E.6 — chuẩn hoá vocab `hieuluc` | ✅ **ĐÓNG trong phạm vi hồ sơ**: 94 dòng chỉ còn **3** giá trị (`rỗng` 45 · `DỰ THẢO — chưa hiệu lực` 25 · `Còn` 24), không dòng dự thảo nào mang nhãn `Còn`. 10 biến thể còn lại (`Còn hiệu lực`, `Con hieu luc`, `can_kiem_tra`…) **nằm ở kho NỀN vbqppl** — ngoài phạm vi, để lượt dọn kho nền. |
| §5.3 — notebook `80742228-…` ngoài topology | ✅ **CHỐT: báo giả.** `profile-list` cho thấy `80742228-ba7a-481c-bd8e-d4115876ed6e` = `notebookId` của profile **«Khảo sát Luật Xuất bản»**. 54 dòng thấy được là do quét kèm scope nền. KHÔNG phải shard bỏ sót, KHÔNG cần khai thêm topology. |
| §E.10 — cơ sở đếm `registry-doctor` | ⚠ tầng 1 đã có từ v1.35.65 (`scanned`+`basis`) **nhưng `basis` NÓI SAI** ⇒ vá tiếp, xem §C mục 1. |
| §E.8 — dọn locks + manifest-summary | ⚠ **BÁC phần lớn tiền đề**, xem §E. |
| §E.7 — BC 6193 + raw-twin | ⏳ đã đo đủ để quyết, **chờ duyệt**, xem §F. |
| §E.9 — NQ Chính phủ cho VD-12 | ⏳ tiến được một bước lớn, chưa đóng, xem §G. |
| 1–4 (NLM) | ⛔ **chặn** — NLM chết, xem §D. |

---

## C. ĐÃ VÁ — r251 / v1.35.88 (selftest 1399/1399, gate xanh, +4 test có phản chứng)

Cả bốn lỗi đều thuộc một loại: **công cụ nói sai về chính con số nó in ra.** Bắt được bằng cách ĐO LIVE
rồi đối chiếu báo cáo lượt trước, không phải bằng đọc mã.

**1. `registry-doctor.basis` khai THIẾU phần mình loại.** `basis` viết "loại `ref` + bản gốc
`loai='thuong'`", nhưng `is_own_thuong` loại THÊM **mọi** dòng `own` có `corpus=false` bất kể `loai`.
Đo hồ sơ này: 33 dòng bị loại mà chỉ **22** là `loai='thuong'`; **11 dòng còn lại có tên/số hiệu
CHUẨN** — `TT_21-2025-TT-NHNN_Xep_hang_TCTD`, `VBT_BC_BHXH_ThaiNguyen…` (sohieu `1104-BC-BHXH`),
3 Phụ lục Thái Nguyên, `DUTHAO_CV_7728-BNV…`, `VBT_BC_7692-BC-BNV…`, `VBHN_25-VBHN-VPQH_2022_Luat_NHNN`…
— và **5 trong số đó mang cờ `MISSING_SOHIEU` mà KHÔNG vào bucket `missing_sohieu`**. Ai đọc
`missing_sohieu=25` cũng không có đường nào biết. Nay `skipped_own_corpus_false` là số đếm RIÊNG,
`scanned` = count − ba lớp, `basis` kể đủ ba lớp kèm cảnh báo về cờ bị bỏ; thêm `skip_reason(row)`.
*Cố ý KHÔNG đổi phép lọc* — sửa phép lọc là đổi ngữ nghĩa hygiene, việc khác.

**2. `sohieu_conflict` GIẢ cho họ chunk.** 3 dòng cùng `41-2024-QH15` (canonical + `__part01__` +
`__part02__`) ra 3 chữ ký `_subject_sig` khác nhau ⇒ bị xếp `sohieu_conflict_different_doc` = "văn bản
KHÁC cùng số hiệu, NGUY HIỂM tra sai", dù chẻ chunk là CHỦ ĐÍCH (lách trần 100k của NLM). Nay bỏ hậu tố
`__partNN__…` trước khi lấy chữ ký ⇒ `sohieu_conflict_groups` **1 → 0**, họ này về `sohieu_dup_same_doc`.
★ Lượt trước định chữa bằng cách GHI CHÚ vào registry (journal `register-bulk_1785320950_22129`,
KETQUA §3) — **đo lại 30-07 thấy `goc`/`title_vn`/`sua_doi` của cả ba dòng vẫn RỖNG**, ghi chú không neo
được, nên chữa ở CODE. Kèm **drift-lock hai mirror** `registry_hygiene._subject_sig` ↔
`classify._subject_sig` (docstring nói "Mirror" mà trước r251 không gì khoá).

**3. `ingest-missing` báo `backlog=0` trên manifest 3 ngày tuổi** (§A). Nay có `snapshot_age_s` + cờ TÊN
`STALE_SNAPSHOT` (ngưỡng 1h, xa hẳn cache GAS ~600s); khi `backlog=0` thì nói thẳng "số 0 trên snapshot
cũ KHÔNG có nghĩa hết việc"; mốc không đọc được ⇒ `SNAPSHOT_TS_UNPARSEABLE`, không im lặng.

**4. `deploy-guard.ps1` fail-closed OAN ⇒ ĐƯỜNG DEPLOY WINDOWS TẮC HẲN.** `gws` in banner
`Using keyring backend: keyring` TRƯỚC JSON; guard gộp stderr (`2>&1`) rồi đổ THẲNG vào
`ConvertFrom-Json` ⇒ chết ngay ký tự `U` ⇒ `exit 4`, dù `gws` rc=0 và tên file đọc được bình thường.
Twin `deploy-package.sh` không vướng vì `sed` trên cả khối — đúng cảnh báo "hai bản sẽ trôi lệch", lần
này bên PS là bên **chặn oan**. Sau vá: guard chạy đúng, báo `Drive đang v1.35.87 < v1.35.88 sắp đẩy`.
★ Bẫy môi trường kèm theo: guard là **pwsh 7**; chạy bằng `powershell.exe` (5.1) vỡ ở
`ParserError: Missing closing '}'` — KHÔNG phải lỗi script.

**Bẫy khi vá (3):** thêm 2 hàm + 1 hằng vào `tl_core/ingest_ops.py` làm đỏ CÙNG LÚC hai drift-lock —
`r90` (tên top-level của module REBASE phải resolve qua `tl`) và `r81` (mọi tên trong `_STUB_MAP` phải
**callable**). Hằng `_SNAPSHOT_STALE_S` phải re-export TRỰC TIẾP, không vào `_STUB_MAP`.

★ **Trùng số hiệu đợt:** phiên song song đã chiếm `r250`/`v1.35.87` giữa lúc lượt này đang chạy
(commit `14d1e35` được `pull` vào cây này lúc ~11:5x). Đã đánh lại toàn bộ thành **r251 / v1.35.88**.

---

## D. NLM: người dùng báo đã sống, ĐO thì vẫn chết — chẩn đoán chính xác

Người dùng nhắc giữa lượt: "nlm đã sống lại, hãy kiểm tra và sử dụng". Đã kiểm, **không sống**:

| Phép đo | Kết quả |
|---|---|
| `nlm --version` | 0.9.4, bản mới nhất |
| `nlm notebook get 59e8d0de…` (gọi TRỰC TIẾP CLI) | `Failed to get notebook: Authentication expired. Run 'nlm login'` |
| `tl nlm-auth-status` | `alive=false`, `age_min` 0–10′ (jar bị GHI LẠI mỗi lần probe ⇒ **`age_min` không phải chỉ báo tươi**) |
| `tl nlm-auth-load` | rc=2 — guard r208c **TỪ CHỐI HẠ CẤP**: bundle Drive 482′ tuổi vs jar cục bộ 1′ |
| `chrome-port-map.json` | trỏ **PID 18600** — `Get-Process 18600` = **ĐÃ CHẾT** |

⇒ Nghĩa là: **đã có một lượt làm tươi cục bộ** (jar mới hơn bundle Drive nên guard chặn ghi đè), nhưng
phiên tạo ra KHÔNG xác thực được. Và `chrome-port-map.json` còn trỏ PID chết ⇒ theo đúng ca đã ghi sổ,
`nlm login` sẽ **vỡ bằng traceback** `os.kill(pid,0)` (`cdp.py:167`) chứ không phải báo lỗi tử tế.

**Việc của người dùng (tôi không tự chạy — `nlm login` cần browser tương tác):**

```bash
D:\Quốc hội\refresh-tokens.cmd
```

Script này (bản đã vá 27-07) làm đủ `Stop-NlmChrome` + `Repair-NlmPortMap` + `-ClearProfile`, tức dọn
đúng PID chết ở trên. Xong thì kiểm `tl nlm-auth-status --json` phải `alive=true` **rồi mới**
`tl nlm-auth-stage` để bundle trên Drive khỏi tụt lại. (Nhắc: `nlm login` TRẦN là **no-op** — phải
`--force`; profile Chrome của nlm bị đăng xuất thì cần `--clear`.)

Phiên song song `r250` vừa thêm `scripts/nlm-auto-refresh.sh` (tự phát hiện export mới trên Drive →
import → mã hoá → xoá) — đó là đường tự động cho mắt xích này, nhưng nó **không thay được** một lần
`nlm login` khi phiên đã chết hẳn.

---

## E. §E.8 — BÁC tiền đề "dọn locks hết hạn", giữ nửa manifest

**Không có sheet `locks`.** Đọc GAS `Code.gs`: registry spreadsheet chỉ có `files`, `_meta`, `claims`
(+ `files_bak_*`). Cái lượt trước gọi là "locks còn ~12 dòng pending hết hạn" chính là tab **`claims`**
— và **giữ dòng `pending` hết hạn là CHỦ ĐÍCH**, có chú thích trong mã:

- `_claimGcFilter_` chỉ dọn `committed`/`released` quá 24h; `pending` **giữ nguyên — "tự chữa qua reclaim (D10)"**.
- `_claimAcquireDecide_`: `pending` mà `now > expires_at` ⇒ `EXPIRED_RECLAIM` = **cấp quyền**, không chặn.

⇒ Claim hết hạn **không khoá gì cả**, không phải rác cần dọn. Thêm nữa **không có endpoint/lệnh nào để
đọc hay xoá `claims`** (chỉ acquire/commit/release), nên "dọn" sẽ phải sửa GAS + deploy webapp — không
đáng, vì không có hại. Việc còn lại duy nhất (nếu muốn): dọn dòng `pending` của những `identity_hash`
không bao giờ được acquire lại — thuần thẩm mỹ, xếp hàng cùng lượt dọn kho nền.

**Nửa manifest thì tự phục vụ:** `manifest_export` sinh lại theo yêu cầu — `--refresh` đưa snapshot từ
27-07T16:27 về 30-07T03:37. Cái thiếu không phải lệnh dọn mà là **cảnh báo khi đọc bản nguội** → đã vá
(§C mục 3).

---

## F. §E.7 — BC 6193: KHÔNG nên đăng ký dưới cái tên đang có. Chờ người quyết.

**Vị trí:** `1ksTzDiDXj4IEhWvjGPTj3CDJQwqlCz6U` ·
`BC_6193_2026_BNV_CTL_V_v_tien_do_chuan_bi_va_mot_so_noi_dung_lon_cua_du_an_Luat_sua_doi.pdf` ·
9 trang · 25.066 ký tự · không dòng registry, không bản GDoc.

**Hai phát hiện khi mở ra đọc (bóc bằng `fitz`, xem ghi chú công cụ ở §H):**

1. **Số hiệu "6193" trong TÊN không phải số hiệu của chính nó.** Thân văn bản không có dòng `Số: …`,
   không có dòng `Hà Nội, ngày…`, không có khối chữ ký. `6193/BNV-CTL&BHXH` được **dẫn chiếu bên trong**
   như một công văn KHÁC ("*công văn số 6193/BNV-CTL&BHXH gửi lấy ý kiến phản biện xã hội của Uỷ ban
   Trung ương Mặt trận Tổ quốc Việt Nam*"). Văn bản này thực chất là **BÁO CÁO của Bộ Nội vụ gửi Thường
   trực UBVHXH**, làm theo văn bản `569/UBVHXH16` ngày 16/7/2026. ⇒ Đăng ký nguyên tên hiện tại là
   **đóng đinh một số hiệu sai vào registry** — đúng lớp lỗi mà §E.3 vừa mất công gỡ.
2. **Nó gần trùng một dòng ĐÃ có, nhưng không phải bản trùng.** So với
   `VBT_PL_BC_tien_do_noi_dung_lon_du_an_Luat_BHXH_kem_CV_UBVHXH` (`12WxSW-xxNW…`, `corpus=true`):
   ratio **0.865**, Jaccard **0.839**, PDF **DÀI HƠN** (24.385 vs 20.088 ký tự chuẩn hoá). Và bản đang ở
   corpus **CÓ MARKUP SỬA ĐỔI** (`strike=4`), còn bản PDF thì sạch markup. ⇒ Hai **phiên bản khác nhau**
   của cùng một báo cáo: corpus đang giữ bản có vết sửa, bản PDF đầy đủ hơn thì mồ côi.

**Đề xuất (chờ duyệt điểm chạm, chưa chạy gì):**
- (a) `rename` file Drive về tên KHÔNG mang số hiệu vay:
  `DUTHAO_VBT_BC_BNV_tien_do_va_noi_dung_lon_du_an_Luat_BHXH_16-7-2026.pdf`;
- (b) người thẩm tra quyết bản nào là bản dẫn chiếu (PDF sạch-markup & dài hơn, hay GDoc đang trong
  corpus) — **rồi mới** bàn `corpus=true`; nhãn bắt buộc `hieuluc=DỰ THẢO — chưa hiệu lực`;
- (c) KHÔNG đăng ký thêm dòng nếu chọn giữ GDoc — tránh dòng thứ hai cùng nội dung.

**Chính sách raw-twin — đo đủ để quyết (44 file thô trong 2 thư mục):**

| Nhóm | Số | Ví dụ |
|---|---|---|
| raw **ĐÃ** đăng ký (`loai=thuong`, `corpus=false`) | **20** | 10 PDF thế hệ 16.6 trong `Hồ sơ Luật`, `Nghị-định-159-2025-NĐ-CP.docx`, 3 PDF ngân hàng… |
| raw **CHƯA** đăng ký (mồ côi) | **24** | `Luat_41-2024-QH15_2024_Bao_hiem_xa_hoi.pdf` (bản Công báo official), `…docx` trung gian, BC 6193, `THAMKHAO_ILO_C102/C168`, các `DUTHAO_*.docx/.pdf` song sinh |

⇒ Kho đang chạy **cả hai chính sách cùng lúc** — đó mới là vấn đề, không phải chuyện thiếu 1 dòng.
Khuyến nghị: **thôi đăng ký raw** (bỏ hẳn `loai=thuong` khỏi profile hồ sơ, để 20 dòng kia về mồ côi
như 24 dòng còn lại) vì `loai=thuong` không mang giá trị tra cứu nào mà lại làm lệch mọi phép đếm —
chính nó là lớp (2) khiến `registry-doctor` bỏ qua 22 dòng ở §C mục 1. Là quyết định của người dùng;
làm thì đi `reg-delete` có duyệt, KHÔNG tự chạy.

---

## G. §E.9 / VD-12 — tiến được một bước lớn: xác nhận LOẠI văn bản và CĂN CỨ, chưa tìm ra bản cho BHXH

**Mạng đo được từ máy này:** `congbao.chinhphu.vn` 200 · `chinhphu.vn` 200 · `vanban.chinhphu.vn` 200 ·
**`vbpl.vn` vẫn 000** (không bắt tay được ở tầng mạng, y như 27-07 và 29-07 — không phải lỗi proxy của
Cowork).

**Xác nhận tiền lệ mà lượt trước phỏng đoán là ĐÚNG, và tìm thêm một tiền lệ thứ hai:**

| Nghị quyết | Ngày | Công bố văn bản nào tiếp tục hiệu lực |
|---|---|---|
| **31/NQ-CP** | 03/3/2026 | 3 Nghị định thi hành **Luật Giá 16/2023/QH15** (NĐ 78/2024, 85/2024, 87/2024) — hiệu lực từ 01/01/2026 tới khi có bản thay |
| **32/NQ-CP** | ~05/3/2026 | 3 Nghị định thi hành **Luật Kinh doanh bảo hiểm 08/2022/QH15** (có NĐ 46/2023) |

**CĂN CỨ PHÁP LÝ của cơ chế này — đây là mảnh còn thiếu của VD-12:**
**khoản 3 Điều 58 Luật Ban hành VBQPPL số 64/2025/QH15** — khi các VBQPPL có quy định khác nhau về cùng
một vấn đề thì áp dụng văn bản có **hiệu lực pháp lý cao hơn**.

⇒ Vậy loại văn bản cần tìm là **có thật**, đi theo **loạt** ban hành đầu tháng 3/2026, mỗi luật một
nghị quyết. **Chưa tìm được bản tương ứng cho Luật BHXH / NĐ 30/2016** qua 3 lượt tra (2 lượt tìm mở,
1 lượt giới hạn `baochinhphu.vn`/`vanban.chinhphu.vn`/`congbao.chinhphu.vn`).

★ **Và cần xét lại chính tiền đề VD-12:** NĐ **212/2025** đã tự giữ NĐ 30/2016 còn hiệu lực MỘT PHẦN
bằng **Đ23k5 + Đ24k2** của chính nó — tức tính liên tục đã được tuyên ở **tầng nghị định**. Nếu vậy thì
một Nghị quyết Chính phủ có thể **không cần thiết** cho NĐ 30/2016, và VD-12 nên đóng bằng lập luận đó
chứ không phải bằng việc tìm mãi một văn bản có thể không tồn tại. **Người thẩm tra quyết hướng đóng.**

**Bước còn lại (rẻ, làm được từ máy này):** liệt kê Nghị quyết Chính phủ trên
`vanban.chinhphu.vn?classid=509&mode=1` quanh tháng 3/2026 và soi thủ công — trang render sẵn HTML
trang đầu, phân trang bằng JavaScript nên phải mở bằng browser thật.

---

## H. Ghi chú công cụ (không phải lỗi dữ liệu, nhưng vướng khi làm)

1. **`tl doc-text`/`doc-compare` KHÔNG đọc được PDF trên máy Windows này.** `pdftotext` có nhưng ở
   `/mingw64/bin` (MSYS2), không nằm trên PATH của Windows Python ⇒ `doc-compare` trả
   `TEXT_UNAVAILABLE side=["a"]`. Phải bóc tay bằng `fitz` (PyMuPDF có sẵn). `doctor` **không kiểm**
   năng lực đọc PDF nên lỗi chỉ lộ khi lệnh chạy hỏng. Ứng viên vá lượt sau: thêm một cổng `doctor`
   cho `pdftotext`/`pypdf`/`fitz`, hoặc cho `_read_doc_text` rơi về `fitz` khi thiếu `pdftotext`.
2. **Console Windows là `cp1258`** ⇒ mọi script phụ in tiếng Việt phải `PYTHONIOENCODING=utf-8`, kẻo
   `UnicodeEncodeError` giữa lúc đang đo (đã dính 3 lần trong lượt này).
3. **ruff:** 4487 lỗi sẵn trên nền ở 3 tệp đụng tới; delta của lượt này **+2** (F821 `Path` + E702 —
   đúng idiom sẵn có của `tl_selftest.py`). So theo DELTA, không so số tuyệt đối.

---

## I. Việc còn lại, xếp theo cổng

**Chờ NGƯỜI DÙNG (ngoài lượt rà):**
1. `D:\Quốc hội\refresh-tokens.cmd` → `nlm-auth-status` phải `alive=true` → `tl nlm-auth-stage` (§D).

**Chờ DUYỆT ĐIỂM CHẠM (đã chuẩn bị đủ, chưa chạy gì):**
2. BC 6193: rename + quyết bản dẫn chiếu (§F).
3. Chính sách raw-twin: bỏ 20 dòng `loai=thuong` hay đăng ký nốt 24 file mồ côi (§F).
4. `cat_label_variants`: 3 mã có cả nhãn trơ lẫn đủ tên (`02` vs `02_Bao_hiem` — 9 dòng vs 21 dòng;
   `20` vs `20_Lao_dong`; `00` vs `00_Van_ban_cua_Dang`) → `tl recat <id> --cat NN`.

**Mở lại NGAY khi NLM sống (thứ tự bắt buộc):**
5. `tl nlm-add 59e8d0de-c0fa-4dc7-ae69-66be0e8afc6b --drive-id 1dBkksHisu_qzu8S_xj4NDMo_yf-SVFZdA1zK5el7j7w`
   → đẩy GDoc BIDV, gỡ `CORPUS_TRUE_NOT_ON_NLM`.
6. **KHÔNG đẩy `Luat_41-2024-QH15` canonical như prompt bàn giao ghi** — nội dung ĐÃ trên NLM qua
   `part01`+`part02` (`nlm_status=pushed`, source id đủ), và bản canonical 183k ký tự vượt trần chunk
   100k. Việc đúng là **đánh dấu quan hệ chunk→canonical** (điền `goc` = `1WHqzh9lH…` cho 2 dòng part)
   để `ingest-missing` thôi coi nó là backlog — GHI registry, chờ duyệt.
7. Gỡ 3 PDF thô ngân hàng khỏi NLM (`deb9c377` Agribank · `4292d3eb` Vietcombank · `4ab81c4b` BIDV) —
   **sau** mục 5, duyệt điểm chạm trước khi gỡ.
8. `tl nlm-reconcile … --all-notebooks` neo lại trạng thái LIVE.

**Kho NỀN (lượt riêng, ngoài phạm vi hồ sơ):** 10 biến thể `hieuluc`; `removed_family_still_pointing`
10 dòng; cụm trùng/thiếu năm B3 (`40-VBHN-VPQH`, `89_VBHN-VPQH_670749`, `25-VBHN-VPQH` thiếu năm);
2 dòng `18-2026-VBHN-VPQH`.
