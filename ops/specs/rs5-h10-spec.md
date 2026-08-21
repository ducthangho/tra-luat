# ĐẶC TẢ PACKET — RS5-H10 · Engine đồ thị quan hệ văn bản (lát 1/2, THUẦN)

> **Đặc tả ĐÓNG BĂNG.** Sửa = soạn bản mới, KHÔNG sửa đè — băm trong lease sẽ trỏ vào thứ
> không còn tồn tại (`.claude/skills/soan-spec/SKILL.md` §5).
>
> **Đặc tả KHÔNG phải lease.** Đọc xong tệp này vẫn chưa được bắt tay: phải có Packet Issue
> + lease còn hiệu lực theo `docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4.

## 0. Bối cảnh — ý tưởng này giải quyết cái gì

Kho đã có đồ thị quan hệ văn bản, và nó tốt hơn vẻ ngoài:

| Đã có | Bằng chứng |
|---|---|
| Cạnh **có kiểu**: `SUA_DOI_BASE` · `CHU_THICH_LICH_SU` · `DAN_CHIEU_NOI_DUNG` | `scripts/tl_core/lookup_ops.py:1684` (`tl xref`) |
| **Bắc cầu**: `consolidation_chain` + BFS `frontier`/`seen`/`dry_rounds` | `_rasoat_dedup_push` (`lookup_ops.py:1720`), `tl rasoat-loop` |
| Cạnh **cấp Điều** kèm `pending_effect`/`hieu_luc` | `dieu_level_amendment_map` |
| **Lỗ hổng nguồn**: `OK`/`MISSING`/`OUTDATED`/`SOHIEU_MISMATCH` + `missing_in_corpus` | `tl frontier-expand` (`scripts/tl_core/fetch_web.py:189`) |

Thiếu đúng hai thứ, và cả hai đã được chính kế hoạch khai:

**(1) Không lưu bền.** Không có cache quan hệ nào — cache hiện có chỉ gồm `manifest.json`,
`manifest_index.json`, `manifest.dirty`, `fetch_queue.json`, `corpus_audit_ckpt_*`. Mỗi lượt
`xref`/`frontier-expand` đọc lại nguyên văn qua mạng rồi **vứt kết quả đi**.

**(2) Cạnh chỉ đi MỘT CHIỀU.** `frontier-expand` khai đúng phạm vi của nó: *"trích mọi văn bản
được DẪN CHIẾU trong 1 văn bản"* — tức trả lời **"tôi trỏ tới ai"**. Câu hỏi của người rà soát
dự thảo là câu **ngược**: *"ai đang trỏ vào Luật A — sửa nó thì gãy những gì?"* Hôm nay muốn
trả lời phải chạy `xref` lên toàn bộ corpus, mỗi văn bản một lượt đọc mạng; thực tế không ai
làm, nên PHA 2 phải bù bằng NLM — mà `references/QUY_TRINH_RA_SOAT_3_TANG.md:4` đã tự khai NLM
*"RAG recall hạn chế, **không chứng minh được 'vắng mặt'**"*.

**Vì sao đảo chiều là thứ đáng làm:** `"không văn bản nào trong corpus trỏ vào Luật A"` là mệnh
đề **QUYẾT ĐỊNH ĐƯỢC** trên một bảng cạnh; nó **không** quyết định được qua recall của RAG.
Đảo chiều biến một khoảng lặng thành một khẳng định có thể sai và do đó có thể kiểm.

**Giới hạn, nói thẳng:** chỉ chứng minh được vắng mặt **TRONG corpus**. Corpus vẫn khuyết. Nhưng
cái khuyết chuyển từ *ẩn* thành `missing_in_corpus` — một danh sách hiện ra được. Đó là lý do
trạng thái thứ ba (`chua_do_duoc`) là bắt buộc chứ không phải trang trí: **nếu "chưa trích" bị
làm tròn thành "không có cạnh", công cụ sẽ nói dối đúng câu hỏi nó sinh ra để trả lời** — hỏng
nặng hơn không có công cụ.

**Nguồn ý tưởng:** kiến trúc `codegraph` (`github.com/colbymchenry/codegraph`, MIT). Thứ bê sang
KHÔNG phải mã, không phải SQLite, không phải tree-sitter — mà đúng một quyết định: **giữ lại
bảng cạnh rồi đảo chiều**; "blast radius" của nó chỉ là truy vấn cạnh vào. Mọi thứ khác của
codegraph (index tốc độ, watcher, hỏi bằng ngôn ngữ tự nhiên) đã bị bác — xem `ngoai_pham_vi`.

**Lát này (RS5-H10) là lát 1/2:** engine THUẦN, không I/O, không CLI. Lát 2 (RS5-H11) phơi ra
CLI + cache trên đĩa; spec của nó soạn SAU khi lát này đã vào integration (lý do ở §9).

---

## 1. packet_id · packet_issue

| trường | giá trị |
|---|---|
| `packet_id` | `RS5-H10` |
| `packet_issue` | **CHƯA MỞ** — phải có trước khi bắt tay (`docs/PROTOCOL_DA_PHIEN.md` §3.2) |
| lát | 1/2 (lát 2 = `RS5-H11`, chưa soạn spec) |
| hạng mục kế hoạch | `H10` (H0–H9 đã dùng hết trong kế hoạch rà soát) |

## 2. nguon_cap_viec

`docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md:173` — dòng bảng §D:

> *"Nạp bổ sung giữa chừng | **~85%** (↑70) | … THIẾU: **lưu bền** hàng đợi qua các phiên"*

Phụ trợ, cùng tệp:
- `:175` — *"Vòng lặp rà đến hết plan | ~55% | … THIẾU: trạng thái theo đơn vị rà + **lưu bền** + spawn agent"*
- `references/QUY_TRINH_RA_SOAT_3_TANG.md:4` — *"không chứng minh được 'vắng mặt'"*

**Không phải packet khắc phục.** Không kế thừa biên nhận nào (xem §8).

## 3. review_class

`systemic` (mức khai tối thiểu).

Căn cứ: `scripts/tl_core/**` là runtime của gói phát hành, nhưng lát này **không** chạm
authority · credential · workflow · dispatcher · migration dữ liệu · LIVE adapter — tức không
thuộc danh sách `sensitive` tường minh của `docs/PROTOCOL_DA_PHIEN.md` §8. Lát này còn không có
I/O nào.

Nhắc: §8 tính **fail-closed** — dispatcher ghi `effective_review_class` bằng mức **cao hơn**
giữa mức khai ở đây và mức classifier tính từ diff thật. Con số ở đây là **sàn, không phải trần**.

## 4. write_set

Đúng hai đường dẫn, không ký tự đại diện:

1. `scripts/tl_core/quanhe.py` *(tệp MỚI)*
2. `scripts/tl_selftest.py`

**Đối chiếu ngưỡng** `docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md`: packet thường
≤ 6 tệp và ≤ 1.000 dòng. Đây là **2 tệp**, dự kiến **≤ 300 dòng thêm** — nằm trong cả ngưỡng
`sensitive` (≤3 tệp/≤300 dòng) dù chỉ khai `systemic`. Vượt 300 dòng thì DỪNG trước review và
khai lý do, không tự nới.

### 4.1. Ba ràng buộc kỹ thuật của write set — đo được, và sai một cái là phải sửa `tl.py`

**(a) Selftest PHẢI truy cập module mới bằng `import tl_core.quanhe`, KHÔNG dùng tên trần.**
Tiền lệ gần nhất (`_frontier_candidates`) gọi **tên trần** và vì thế **có mặt trong `_STUB_MAP`**
(`scripts/tl.py:1419`, đã đo: 1 lần khớp trong vùng 1419–1700). Đi theo tiền lệ gần nhất sẽ buộc
phải sửa `tl.py` — **vi phạm ràng buộc §E của kế hoạch ("KHÔNG đụng `tl.py`")** và làm write set
phình. Tiền lệ ĐÚNG phải theo: `scripts/tl_selftest.py:3807`
(`import tl_core.hygiene as _hyg_ms  # nguồn THẬT ở tl_core.hygiene (tên trong tl là stub)`).

**(b) KHÔNG thêm tên nào vào `_STUB_MAP`.** Lát này không xuất khẩu hàm nào ra bề mặt `tl`.

**(c) KHÔNG regen `RELEASE_MANIFEST.json` trong packet này.** `KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md`
§E chốt: regen là *"việc của bước đóng gói, KHÔNG phải việc lúc tạo file"*. Đo kèm: gói đang
**180/200** tệp — còn 20 khe, thêm 1 tệp không chạm trần.

**Đã loại trừ một rủi ro write set:** canary tính toàn vẹn gói (`tl_selftest.py:2423`) dựng cây
mock liệt kê **22** module `tl_core`, trong khi cây thật có **32** — danh sách ấy vốn đã KHÔNG
vét cạn và hiện vẫn xanh, nên thêm module thứ 33 không làm nó đỏ. Không cần đụng tệp thứ ba.

## 5. ngoai_pham_vi

Cố ý KHÔNG làm trong packet này:

| Không làm | Vì sao |
|---|---|
| Ghi cache ra đĩa | Thuộc lát 2 (`RS5-H11`). Lát này thuần, không I/O |
| Thêm/sửa lệnh CLI; đụng `tl.py`, `SKILL.md`, `VERSION`, golden | Quyết định Q6: cạnh vào sẽ là **cờ trên lệnh SẴN CÓ**, không phải lệnh mới ⇒ không chạm `_STUB_MAP` |
| Đọc mạng / Drive / registry LIVE | Lát thuần. Đường offline đã có: `--text-file` (`command_registry.py:436,457,501`) |
| Cạnh **cấp Điều** cho `DAN_CHIEU_NOI_DUNG` | Quyết định Q2 = B (cấp văn bản). Cấp Điều đòi sửa tầng trích xuất ⇒ packet khác |
| Sửa `xref` / `frontier-expand` / `rasoat-loop` | Packet này **TIÊU THỤ** output của chúng, không sửa chúng. Chống xây trùng (§PHỤ LỤC kế hoạch) |
| SQLite / FTS5 / file watcher / hỏi bằng ngôn ngữ tự nhiên | Đã bác khi thẩm định codegraph: corpus ~500 văn bản nên không có nút thắt tốc độ; corpus nằm trên Drive nên không có `inotify`; hỏi-đoán xung đột doctrine *"KHÔNG dùng RAG để trả NGUYÊN VĂN"* |
| Kiểm chứng hiệu quả trên corpus LIVE | Quyết định Q8: thuộc **Đợt 4** của kế hoạch (*"không thể cổng-máy — phần duy nhất cần người"*) |
| Sửa con trỏ đứt `guard-va-boc-tl-core` | Phát hiện rời, ghi ở §9. Gộp vào đây là nới phạm vi |

## 6. muc_tieu

Mỗi mục chiếu vào **một** đường dẫn trong `write_set` (L2).

| # | Mục tiêu | Đường dẫn |
|---|---|---|
| **MT1** | `chuan_hoa_canh(refs_classed, fnmap) -> list[canh]` — PURE. Từ output ĐÃ phân loại của `xref`/`frontier-expand` sinh cạnh chuẩn hoá, **giữ nguyên** `rel_type` và `flag` sẵn có. Không tự phân loại lại, không I/O | `scripts/tl_core/quanhe.py` |
| **MT2** | `dao_chieu(canh_ra_nhieu_vb) -> dict[dich, list[canh_vao]]` — PURE. Đảo chiều, dedup, **giữ kiểu cạnh**, thứ tự xuất TẤT ĐỊNH | `scripts/tl_core/quanhe.py` |
| **MT3** | `tra_canh_vao(do_thi, dich) -> dict` — PURE. Trả **BA trạng thái**: `co_canh_vao` · `khong_co_canh_vao_trong_corpus` · `chua_do_duoc`, kèm `so_van_ban_chua_trich`. Trạng thái 3 khi độ phủ trích xuất chưa kín | `scripts/tl_core/quanhe.py` |
| **MT4** | `phan_loai_do_tuoi(do_thi, entries) -> dict` — PURE. So `md5` đóng dấu ở nút với `md5` trong entries registry → `con_moi` / `da_cu` / `chua_trich`. Không đọc mạng, không đọc đĩa | `scripts/tl_core/quanhe.py` |
| **MT5** | Ca `r333_*` cho MT1–MT4, chạy offline, truy cập module theo ràng buộc §4.1(a) | `scripts/tl_selftest.py` |

**Khai đơn vị đếm (L1):** mọi con số "N" trong §7 đếm **CA TEST** (`cases.append`), không đếm
phát hiện, không đếm đột biến. Nền hiện tại: `scripts/tl_selftest.py` có **1.040** lời gọi
`cases.append` ở mức tĩnh (một số nằm trong vòng lặp nên N thực tế cao hơn — mốc CHANGELOG gần
nhất ghi 1.526 ca). **Tiêu chí là N/N hai số BẰNG NHAU, không phải một con số tuyệt đối.**

## 7. nghiem_thu

Mỗi tiêu chí nêu **đột biến làm nó ĐỎ** (L3). Tiêu chí không thể đỏ thì không phải tiêu chí.
Tiền tố ca: `r333_` (`r332_` là số đang dùng cao nhất).

| Ca | Đo gì | ĐỘT BIẾN phải làm ca này ĐỎ |
|---|---|---|
| `r333_quanhe_chuan_hoa_giu_rel_type` | MT1 — input đủ 3 `rel_type` + một ref `flag=MISSING` ⇒ cạnh giữ nguyên phân loại VÀ **giữ cạnh `MISSING`** | Lọc bỏ cạnh có `flag=MISSING` (lý lẽ nghe hợp lý: "chưa có trong corpus thì chưa phải cạnh") ⇒ ĐỎ. `MISSING` **là** lỗ hổng nguồn, phải hiện |
| `r333_quanhe_dao_chieu_dedup_giu_kieu` | MT2 — hai văn bản cùng trỏ một đích, một trong hai trỏ **hai lần** ⇒ `canh_vao` đúng **2** mục, mỗi mục giữ đúng `rel_type` | (a) Bỏ dedup ⇒ 3 mục ⇒ ĐỎ. (b) Bỏ `rel_type` khỏi mục xuất ⇒ ĐỎ |
| `r333_quanhe_dao_chieu_tat_dinh` | MT2 — chạy hai lần trên cùng input ⇒ JSON **byte-equal** | Xuất trực tiếp từ `set` không sắp xếp ⇒ thứ tự trôi ⇒ ĐỎ |
| `r333_quanhe_chua_do_duoc_khong_lam_tron` | **MT3, ca quan trọng nhất** — đồ thị 3 văn bản, mới trích **2**; hỏi cạnh vào của một đích không ai trỏ tới ⇒ phải trả `chua_do_duoc` và `so_van_ban_chua_trich == 1` | Bỏ phép kiểm độ phủ (coi nút chưa trích như đã trích) ⇒ hàm trả `khong_co_canh_vao_trong_corpus` ⇒ ĐỎ |
| `r333_quanhe_vang_mat_chung_minh_duoc` | **MT3, ca ĐỐI NGHỊCH** — cùng đồ thị nhưng đã trích **đủ 3/3**, không ai trỏ tới đích ⇒ phải trả `khong_co_canh_vao_trong_corpus` | Làm hàm luôn trả `chua_do_duoc` ("cho chắc") ⇒ ĐỎ |
| `r333_quanhe_md5_doi_thi_nut_hoa_cu` | MT4 — nút đóng dấu `md5=A`, entries có `md5=B` ⇒ nút vào `da_cu` | Bỏ so `md5`, luôn coi còn mới ⇒ nút vào `con_moi` ⇒ ĐỎ |

**Vì sao hai ca MT3 phải đi THÀNH CẶP:** một mình `r333_quanhe_chua_do_duoc_khong_lam_tron` bị
thoả bởi một hằng số (`return "chua_do_duoc"` luôn luôn) — hàm sẽ vô dụng mà cổng vẫn xanh. Một
mình ca kia bị thoả bởi hằng số ngược lại. **Chỉ cặp đối nghịch mới đo được logic.** Đây là áp
dụng trực tiếp bài học *"cổng có thể xanh vì đồ GIẢ nói dối"* (`CLAUDE.md`).

### 7.1. Cổng chung phải xanh (ngoài các ca trên)

| Cổng | Tiêu chí | Ghi chú |
|---|---|---|
| `python scripts/tl.py --selftest` | **N/N, hai số BẰNG NHAU** | `rc=0` một mình KHÔNG đủ — đòi bằng chứng dương (`CLAUDE.md`) |
| `python -m ruff check --select F scripts/tl.py` | **DELTA so `origin/master` = 0** | KHÔNG phải "0 tuyệt đối". Nền đo 29-07-2026: 12 F821 + 0 F401 là BY DESIGN |
| `git status --porcelain` sau khi chạy selftest | **rỗng** | Lát thuần không được ghi gì trong cây |
| `git diff --numstat` | ≤ 2 tệp, ≤ 300 dòng thêm | Vượt ⇒ DỪNG trước review, khai lý do |

### 7.2. Điều kiện HOÀN TẤT

Đủ **cả sáu** ca `r333_*` xanh **và** cả bốn cổng §7.1 xanh **và** mỗi đột biến ở bảng §7 đã
được CHẠY THẬT trên **bản sao tạm** rồi ghi kết quả vào biên nhận.

> **Đột biến phải chạy trên BẢN SAO TẠM, không ghi vào tệp thật.** Bài học đã trả giá: khôi phục
> trong `finally` là bom hẹn giờ — lượt chạy bị `SIGTERM` cắt giữa chừng thì `finally` không chạy
> và tệp ở lại trạng thái đã méo (`CLAUDE.md`).
>
> **Và: nghĩ ra một đột biến mà KHÔNG CHẠY nó thì đột biến ấy KHÔNG TỒN TẠI.** Bảng §7 là danh
> sách việc phải chạy, không phải danh sách để đọc.

## 8. hinh_dang_ke_thua

`khong_ap_dung` — đây **không** phải packet khắc phục, không có biên nhận tiền nhiệm để chép bộ
đếm hình dạng lỗi (L4).

Bộ đếm bắt đầu từ **0**. Packet khắc phục nào mọc ra từ đây **phải chép bộ đếm sang**, kẻo chốt
*"cùng một hình dạng lỗi lặp ≥3 lần thì câu hỏi đúng là 'có nên làm việc này không', không phải
'vá thế nào'"* mất tác dụng đúng lúc cần nhất.

## 9. chua_do_duoc

Thứ **không** kiểm được từ phiên soạn spec này — ghi thẳng, không giấu sau chữ "có thể":

1. **Chưa chạy selftest trong phiên này.** Mọi con số ca (1.040 tĩnh / 1.526 theo CHANGELOG) đọc
   từ mã và CHANGELOG, **chưa đo lại bằng một lượt chạy**. Phiên thi hành phải đo nền TRƯỚC khi
   sửa, rồi so DELTA — đừng nghi bản vá của mình trước khi đo nền.
2. **Chưa chạy `ruff`** trong phiên này; ngưỡng 12 F821 + 0 F401 chép từ `CLAUDE.md`, mốc đo
   29-07-2026 trên v1.35.60. Cây nay ở **v1.36.68** ⇒ **ngưỡng có thể đã trôi**. Đo lại trên
   `origin/master` sạch trước khi kết luận.
3. **Hiệu quả thật trên corpus LIVE chưa đo** — cần creds webapp + ~500 lượt đọc nguyên văn.
   Thuộc **Đợt 4** (Q8=A). Packet này KHÔNG được khai là đã chứng minh giá trị nghiệp vụ.
4. **`codex` đang `SAP_HET_HAN`** (ảnh chụp cũ 122.8h, `last_refresh=2026-08-16`) ⇒ cross-review
   khác nền có thể bị chặn vì hạ tầng chứ không vì rủi ro. Đây là lý do khai `systemic` chứ
   không `sensitive` (Q7=A).
5. **Con trỏ đứt:** `CLAUDE.md:33` viện dẫn *"G5 §11 kế hoạch guard-va-boc-tl-core"*, mà **không
   tệp nào trong kho mang tên đó** (đo bằng `rg` toàn kho). Ngoài phạm vi packet này; ghi ra để
   không rơi vào khoảng lặng.
6. **Spec lát 2 (`RS5-H11`) CHƯA soạn, có chủ đích.** Hai lý do: (a) ADR-0044 đòi lát sau mọc
   trên `mission/<issue>/integration` **đã nhận** lát trước, không mọc trên PR chưa merge; (b)
   write set của lát 2 phụ thuộc tên hàm/module mà lát này đẻ ra — đóng băng bây giờ là neo một
   mô tả vào thứ chưa tồn tại, đúng lớp bệnh *"câu mô tả VỊ TRÍ phải đúng ở CẢ HAI phía của lần
   merge"*.
7. **Chưa đo thời lượng/chi phí thi hành.** Ước lượng ≤300 dòng dựa trên hai packet tương đương
   (`58900b2` = 5 tệp +442/−40 · `47847b1` = 10 tệp +414/−27), không phải trên một lượt thử.

## 10. Quyết định đã chốt (người giữ kho, phiên 2026-08-21)

| # | Câu hỏi | Chốt |
|---|---|---|
| Q1 | Kế hoạch nào nhận | **A** — `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md`, thành Đợt 5 |
| Q2 | Phạm vi | **B** — lưu bền **+ chỉ mục ngược cấp văn bản** (không cấp Điều) |
| Q3 | Đồ thị lưu ở đâu | **A** — cache cục bộ theo profile, cạnh `manifest_index.json` (lát 2) |
| Q4 | Làm mới thế nào | **A** — tăng dần theo `md5`, **bắt buộc** trạng thái thứ ba `chua_do_duoc` |
| Q5 | Cắt mấy lát | **A** — hai lát; đây là lát 1 |
| Q6 | Phơi ra CLI thế nào | **A** — cờ trên lệnh SẴN CÓ ⇒ không đụng `tl.py`/`_STUB_MAP` |
| Q7 | `review_class` | **A** — `systemic` cho cả hai lát (sàn, không phải trần) |
| Q8 | Nghiệm thu tới đâu | **A** — cổng máy offline; LIVE đẩy sang Đợt 4 |
