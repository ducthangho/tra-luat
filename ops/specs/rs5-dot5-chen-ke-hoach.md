# BẢN CHÈN — Đợt 5 cho `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md`

> Bản nháp để **người giữ kho tự chèn**. Phiên soạn KHÔNG sửa thẳng kế hoạch: tệp kế hoạch
> không nằm trong write set của lease nào đang mở.
>
> Đặc tả đóng băng của lát 1: `ops/specs/rs5-h10-spec.md`
> `sha256 = caa93d3180511aefdf7d6a2355183aa47a82473f992065471b1be168fde10e30`

---

## 0. Ý tưởng — giải thích để đưa vào kế hoạch

### Kế hoạch đã tự khai lỗ hổng này ở hai chỗ

- `§D:173` — *"Nạp bổ sung giữa chừng | ~85% | … **THIẾU: lưu bền** hàng đợi qua các phiên"*
- `§D:175` — *"Vòng lặp rà đến hết plan | ~55% | … THIẾU: trạng thái theo đơn vị rà + **lưu bền** …"*

và `references/QUY_TRINH_RA_SOAT_3_TANG.md:4` khai cái giá phải trả:

> *"Hỏi NLM theo chủ đề chỉ là **lưới thô** (RAG recall hạn chế, **không chứng minh được 'vắng mặt'**)"*

### Cái đã có — Đợt 5 KHÔNG xây lại

| Đã có | Bằng chứng |
|---|---|
| Cạnh **có kiểu**: `SUA_DOI_BASE` · `CHU_THICH_LICH_SU` · `DAN_CHIEU_NOI_DUNG` | `lookup_ops.py:1684` (`tl xref`) |
| **Bắc cầu**: `consolidation_chain` + BFS `frontier`/`seen`/`dry_rounds` | `_rasoat_dedup_push` (`lookup_ops.py:1720`) |
| Cạnh **cấp Điều** + `pending_effect`/`hieu_luc` | `dieu_level_amendment_map` |
| **Lỗ hổng nguồn** ba mức + `missing_in_corpus` | `fetch_web.py:189` (`tl frontier-expand`) |

Đồ thị quan hệ **đã tồn tại và đã tốt**. Đợt 5 chỉ thêm hai thứ nó chưa có.

### Cái thiếu — đúng hai thứ

**(1) Không lưu bền.** Cache hiện có chỉ gồm `manifest.json`, `manifest_index.json`,
`manifest.dirty`, `fetch_queue.json`, `corpus_audit_ckpt_*` — **không có cache quan hệ nào**.
Mỗi lượt `xref`/`frontier-expand` đọc lại nguyên văn qua mạng rồi vứt kết quả đi.

**(2) Cạnh chỉ đi MỘT CHIỀU — đây mới là chỗ đau.** `frontier-expand` khai đúng phạm vi của
nó: *"trích mọi văn bản được DẪN CHIẾU **trong 1 văn bản**"* — tức trả lời **"tôi trỏ tới ai"**.

Câu hỏi của người rà soát dự thảo là câu **ngược**:

> *"Ai đang trỏ vào Luật A — sửa Luật A thì gãy những gì?"*

Hôm nay muốn trả lời phải chạy `xref` lên **toàn bộ ~500 văn bản**, mỗi văn bản một lượt đọc
mạng. Thực tế không ai làm, nên PHA 2 phải bù bằng NLM — và NLM không chứng minh được vắng mặt.

### Vì sao đảo chiều là thứ đáng làm

`"Không văn bản nào trong corpus trỏ vào Luật A"` là mệnh đề **QUYẾT ĐỊNH ĐƯỢC** trên một bảng
cạnh. Nó **không** quyết định được qua recall của RAG. Đảo chiều biến một **khoảng lặng** thành
một **khẳng định có thể sai** — và do đó có thể kiểm.

**Giới hạn, nói thẳng:** chỉ chứng minh được vắng mặt **TRONG corpus**. Corpus vẫn khuyết. Nhưng
cái khuyết chuyển từ *ẩn* thành `missing_in_corpus` — một danh sách hiện ra được. Vì thế **trạng
thái thứ ba là bắt buộc, không phải trang trí**:

| Trạng thái | Nghĩa |
|---|---|
| `co_canh_vao` | có văn bản trỏ tới — kèm danh sách |
| `khong_co_canh_vao_trong_corpus` | **đã trích đủ corpus** và không ai trỏ tới ⇒ vắng mặt CHỨNG MINH ĐƯỢC |
| `chua_do_duoc` | **chưa trích đủ** ⇒ chưa kết luận được, kèm `so_van_ban_chua_trich` |

Nếu `chua_do_duoc` bị làm tròn thành `khong_co_canh_vao_trong_corpus`, công cụ sẽ **nói dối đúng
câu hỏi nó sinh ra để trả lời** — hỏng nặng hơn không có công cụ. Đúng doctrine `None ≠ False`
và luật ba trạng thái `có · không · không đo được` đã chốt trong `CLAUDE.md`.

### Nguồn ý tưởng, và cái đã BỊ BÁC

Ý tưởng lấy từ `codegraph` (`github.com/colbymchenry/codegraph`, MIT). Thứ tiếp thu **không phải
mã**, không phải SQLite, không phải tree-sitter — mà **đúng một quyết định kiến trúc: giữ lại
bảng cạnh rồi đảo chiều**; "blast radius" của nó chỉ là truy vấn cạnh vào.

Đã thẩm định và **BÁC** phần còn lại:

| Bác | Lý do đo được |
|---|---|
| SQLite/FTS5 làm kho tra | Corpus ~500 văn bản ⇒ không có nút thắt tốc độ. Kho hiện **0 sqlite** ở mọi nơi; `requirements.txt` đúng 1 dòng |
| File watcher / daemon | Corpus nằm trên Drive, không trên đĩa — không có `inotify` nào để nghe |
| Hỏi bằng ngôn ngữ tự nhiên rồi đoán mục tiêu | Xung đột doctrine *"KHÔNG dùng RAG để trả NGUYÊN VĂN"* |
| Telemetry (mặc định BẬT ở codegraph) | Kho làm việc với hồ sơ dự thảo luật |
| Chỉ dẫn *"đừng grep kiểm lại kết quả"* | Trái thẳng bài học *"cổng có thể xanh vì đồ GIẢ nói dối"* |

---

## 1. CHÈN vào bảng §C (KIẾN TRÚC ĐÍCH — THÀNH PHẦN)

Thêm một dòng sau `C7`:

```markdown
| C8 | **(MỚI)** Đồ thị quan hệ văn bản — cạnh RA + chỉ mục NGƯỢC | dữ liệu **DẪN XUẤT**, biến động, tái tạo được | cache cục bộ theo profile, **cạnh `manifest_index.json`** | Tiêu thụ output SẴN CÓ của `xref`/`frontier-expand`, KHÔNG bóc lại. Thêm đúng 2 thứ chúng không có: **lưu bền** + **đảo chiều**. Ba trạng thái `co_canh_vao`/`khong_co_canh_vao_trong_corpus`/`chua_do_duoc` — trạng thái 3 BẮT BUỘC, làm tròn nó là làm công cụ nói dối. Làm mới **tăng dần theo `md5`** (registry đã có cột). Khác `C1`/`C2`: đây KHÔNG phải sản phẩm của phiên nên KHÔNG đẩy Drive — mất thì dựng lại |
```

## 2. CHÈN vào bảng §D (HIỆN TRẠNG ĐÁP ỨNG)

Thêm một dòng:

```markdown
| **(MỚI)** Truy quan hệ NGƯỢC / chứng minh vắng mặt | **~25%** | Cạnh RA đã đầy đủ và có kiểu (`xref` `lookup_ops.py:1684`), bắc cầu đã có (`_rasoat_dedup_push` `:1720`), lỗ hổng nguồn đã có (`frontier-expand` `fetch_web.py:189`). THIẾU: **lưu bền** (không cache quan hệ nào tồn tại) + **chỉ mục ngược** (mọi đường đều per-document forward-only) ⇒ câu "ai trỏ vào Luật A" hôm nay tốn ~500 lượt đọc mạng nên thực tế không ai hỏi, PHA 2 phải bù bằng NLM |
```

Đồng thời **sửa** dòng `:173` — phần "THIẾU: lưu bền hàng đợi qua các phiên" nay có địa chỉ:
thêm cuối ô thứ ba ` → **Đợt 5 / H10–H11**`.

## 3. CHÈN mục Đợt 5 (sau Đợt 4, trước "Định nghĩa HOÀN THÀNH")

```markdown
### Đợt 5 — Đồ thị quan hệ BỀN + truy ngược (vá §D "THIẾU lưu bền")

Ràng buộc chung của §E vẫn áp dụng, và Đợt 5 tuân nó **bằng thiết kế chứ không bằng ngoại lệ**:
cạnh vào phơi ra bằng **cờ trên lệnh SẴN CÓ**, không phải lệnh `tl` mới ⇒ **không đụng `tl.py`**.
(Đo được: thêm lệnh mới BUỘC phải sửa bảng `_STUB_MAP` `tl.py:1419` — packet `AG-T0-03` đã phải
thêm `'cmd_registry_coverage'` vào `tl.py:1664`. Chọn cờ thay vì lệnh làm ràng buộc ấy biến mất.)

| Hạng mục | Sản phẩm | Nghiệm thu (mã test) |
|---|---|---|
| **H10. Engine THUẦN (lát 1/2)** — spec đóng băng `ops/specs/rs5-h10-spec.md` (`sha256 caa93d31…`) | `scripts/tl_core/quanhe.py` (MỚI): 4 hàm PURE, không I/O — `chuan_hoa_canh` (giữ nguyên `rel_type`/`flag` sẵn có, **KHÔNG** phân loại lại) · `dao_chieu` (dedup, giữ kiểu, thứ tự tất định) · `tra_canh_vao` (BA trạng thái + `so_van_ban_chua_trich`) · `phan_loai_do_tuoi` (so `md5` → `con_moi`/`da_cu`/`chua_trich`). Write set **2 tệp**, ≤300 dòng | Sáu ca `r333_*`, mỗi ca có **đột biến làm nó ĐỎ** (bảng §7 của spec). Hai ca MT3 đi **THÀNH CẶP đối nghịch** — `r333_quanhe_chua_do_duoc_khong_lam_tron` và `r333_quanhe_vang_mat_chung_minh_duoc`: một mình ca nào cũng bị thoả bởi một hằng số, chỉ cặp mới đo được logic |
| **H11. Cache trên đĩa + cờ truy ngược (lát 2/2)** — spec soạn SAU khi H10 vào integration | Ghi/đọc đồ thị ở cache cục bộ cạnh `manifest_index.json`; làm mới tăng dần theo `md5`; phơi cạnh vào bằng **cờ trên lệnh sẵn có** (vd `frontier-expand --nguoc`) | `r33x_*`: (a) cache nguội theo `md5` phải hiện ra là `da_cu`, không phục vụ im lặng; (b) sau lượt chạy `git status` sạch; (c) đường đọc fail-closed khi cache hỏng — **không** rơi về "không có cạnh" |

**Thứ tự bắt buộc:** H11 mọc trên `mission/<issue>/integration` **đã nhận** H10 — không mọc trên
PR chưa merge (`docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md`).

**Vì sao spec H11 chưa soạn:** write set của nó phụ thuộc tên hàm/module mà H10 đẻ ra; đóng băng
bây giờ là neo mô tả vào thứ chưa tồn tại — đúng lớp bệnh *"câu mô tả VỊ TRÍ phải đúng ở CẢ HAI
phía của lần merge"*.

**Ngoài phạm vi Đợt 5:** cạnh **cấp Điều** cho `DAN_CHIEU_NOI_DUNG` (đòi sửa tầng trích xuất —
đợt riêng); kiểm chứng LIVE (thuộc **Đợt 4**); SQLite/watcher/hỏi-tự-nhiên (đã bác, §0).
```

## 4. CHÈN vào §PHỤ LỤC (chống xây trùng)

```markdown
| `tl xref` — cạnh RA có kiểu (`SUA_DOI_BASE`/`CHU_THICH_LICH_SU`/`DAN_CHIEU_NOI_DUNG`) + `consolidation_chain` | `lookup_ops.py:1601,1684` | H10 (nguồn cạnh — TIÊU THỤ, không bóc lại) |
| `dieu_level_amendment_map` — cạnh cấp Điều + `pending_effect`/`hieu_luc` | `lookup_ops.py` (`resolve_footnote_amendments`) | H10 (cạnh cấp Điều đã có cho footnote) |
| Khuôn index tự-hồi-phục `_rebuild_manifest_index` + marker `manifest.dirty` | `regio.py:853` | H11 (dùng lại nguyên khuôn làm mới, không thiết kế lại) |
| Cột `md5` + `modified_time` trong 27 cột `REG_COLS_` | `references/API_CONTRACT.md:165` | H11 (khoá làm mới tăng dần) |
| Idiom hàm `PURE (test offline)` — **8 tiền lệ** | `fetch_web.py:128`, `lookup_ops.py:1720`, `hygiene.py:138,1475,3096`, `ingest_ops.py:178`, `nlm_ops.py:51,586` | H10 (khuôn kiểm offline) |
| Truy cập tl_core KHÔNG qua `_STUB_MAP`: `import tl_core.<mod>` | `tl_selftest.py:3807` | H10 (**BẮT BUỘC** — tiền lệ gần nhất `_frontier_candidates` dùng tên trần và VÌ THẾ phải vào `_STUB_MAP`, tức phải sửa `tl.py`) |
```

---

## 5. Cạm bẫy đã đo — đừng để phiên thi hành đạp lại

| Bẫy | Đo được | Cách tránh |
|---|---|---|
| Đi theo tiền lệ **gần nhất** thay vì tiền lệ **đúng** | `_frontier_candidates` gọi bằng tên trần ⇒ có trong `_STUB_MAP` (`tl.py:1419`, khớp 1 lần trong vùng 1419–1700) ⇒ **buộc sửa `tl.py`** | Selftest dùng `import tl_core.quanhe` (`tl_selftest.py:3807`) |
| Tưởng thêm tệp `tl_core` làm đỏ canary toàn vẹn gói | Canary `tl_selftest.py:2423` liệt kê **22** module trong khi cây thật có **32** — vốn đã KHÔNG vét cạn và vẫn xanh | Không cần đụng tệp thứ ba |
| Tưởng phải regen `RELEASE_MANIFEST.json` ngay | §E: regen là *"việc của bước đóng gói, KHÔNG phải việc lúc tạo file"*. Gói đang **180/200**, còn 20 khe | Để bước đóng gói làm |
| Lọc bỏ cạnh `flag=MISSING` cho "sạch" | `MISSING` **LÀ** lỗ hổng nguồn — thứ Đợt 5 sinh ra để phơi | Ca `r333_quanhe_chuan_hoa_giu_rel_type` khoá lại |
| "Cho chắc thì luôn trả `chua_do_duoc`" | Làm công cụ vô dụng mà cổng vẫn xanh | Ca đối nghịch `r333_quanhe_vang_mat_chung_minh_duoc` khoá lại |
| Tin `rc=0` là cổng xanh | Bài học `CLAUDE.md` | Đòi `N/N` hai số BẰNG NHAU |
| Nghi bản vá của mình khi ruff đỏ | Ngưỡng 12 F821 chép từ mốc **v1.35.60**, cây nay **v1.36.68** ⇒ có thể đã trôi | Đo nền trên `origin/master` sạch TRƯỚC, so DELTA |
