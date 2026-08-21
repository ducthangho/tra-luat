# BÀN GIAO — Đợt 5: đồ thị quan hệ văn bản BỀN + truy ngược (ý tiếp thu từ codegraph)

> **ĐÂY KHÔNG PHẢI LEASE, KHÔNG PHẢI LỆNH CẤP VIỆC.** `docs/PROTOCOL_DA_PHIEN.md` §7:
> prompt/handoff KHÔNG phải lease. Trang này là **DỮ LIỆU** để phiên có thẩm quyền nghiên cứu
> và quyết định. Chưa có Packet Issue, chưa có lease ⇒ **chưa ai được bắt tay code.**
>
> **Neo theo BĂM, không theo tên nhánh.** Trang bàn giao `don-nhanh-150-handoff.md` trong chính
> thư mục này đã chết đúng lúc merge vì neo theo tên nhánh; trang này cố ý không lặp lại.
>
> **Nguồn có thẩm quyền là HAI TỆP CÓ BĂM dưới đây. Trang này chỉ là bản chiếu.**
> Chỗ nào trang này lệch tệp thì **TỆP đúng**.

| Artefact | sha256 (định danh BỀN) |
|---|---|
| `ops/specs/rs5-h10-spec.md` — đặc tả ĐÓNG BĂNG lát 1 | `caa93d3180511aefdf7d6a2355183aa47a82473f992065471b1be168fde10e30` |
| `ops/specs/rs5-dot5-chen-ke-hoach.md` — bản chèn kế hoạch | `ed9da785f01d3ec1633d00756a12d211e41a0a79ceda1c00901de07c1f247ef4` |

**Lấy tệp:** tìm ở `master` trước; chưa thấy thì
`git fetch origin claude/codegraph-github-evaluation-749y38`.
Commit đưa hai tệp vào: `9f1ad3712d9ad4452250b9e5b29189805b2ba7d2`
(base `0333948` = `origin/master` lúc soạn, **là tổ tiên** — không rẽ nhánh, không xung đột).
Đọc bằng SHA, đừng đọc bằng tên nhánh: `git show 9f1ad371:ops/specs/rs5-h10-spec.md`.

---

## 1. Việc đã làm

Người giữ kho đưa `github.com/colbymchenry/codegraph` và hỏi có phù hợp / có ý gì đáng tiếp thu
cho tra-luat không. Phiên `Codegraph GitHub repository evaluation` thẩm định, rồi chạy skill
`soan-spec` — 2 vòng chất vấn, 8 câu, người giữ đã chốt cả 8 (bảng §5).

### Kết luận thẩm định codegraph

| Câu hỏi | Kết luận |
|---|---|
| Làm **runtime** cho tra-luat? | **KHÔNG.** Nó parse MÃ NGUỒN bằng tree-sitter; corpus tra-luat là văn bản pháp luật tiếng Việt. Cũng sai hình dạng gói: trần 200 tệp, `requirements.txt` đúng 1 dòng |
| Làm **công cụ dev** cho chính kho? | **Nửa vời, và mù đúng chỗ đau** — xem dưới |
| Có ý gì đáng lấy? | **Đúng MỘT** quyết định kiến trúc: giữ lại bảng cạnh rồi **ĐẢO CHIỀU**. "Blast radius" của nó chỉ là truy vấn cạnh vào |

**Vì sao "mù đúng chỗ đau":** `tl.py:1692` dựng toàn bộ bề mặt API lúc chạy —
`globals()[_sm_n] = _make_tl_stub(...)` từ bảng `_STUB_MAP`. Index tĩnh dựa trên AST sẽ mù y hệt
`ruff` (`CLAUDE.md` đã ghi 12 F821 BY DESIGN vì đúng mẫu này). Dự đoán kiểm chứng được: hỏi
*"ai gọi `cmd_relation_check`"* sẽ trả **"không ai"** — vì đường gọi thật đi qua **BẢNG DỮ LIỆU**
`command_registry.py`, không phải một call edge. Tức **sai một cách TỰ TIN**, trong khi
`SERVER_INSTRUCTIONS` của nó bảo agent *"đừng grep kiểm lại kết quả"*.

> ⚠ **MỨC TIN CẬY:** phiên soạn **CHƯA CHẠY** codegraph trên kho. Đoạn trên là **suy luận từ
> kiến trúc, chưa phải phép đo.** Theo doctrine của kho (*"nghĩ ra được phép thử mà không chạy
> nó thì phép thử ấy không tồn tại"*), muốn dùng kết luận này để quyết thì phải chạy thật.

### Đã BÁC, kèm lý do đo được (đừng dựng lại)

| Bác | Lý do |
|---|---|
| SQLite/FTS5 làm kho tra | `rg -l "sqlite3\|fts5"` toàn kho trả **RỖNG** — và đó không phải thiếu sót: corpus ~500 văn bản, quét tuyến tính trong Python là miễn phí. Nút thắt là **round-trip mạng**, không phải CPU |
| File watcher / daemon | Corpus nằm trên Drive, không trên đĩa — không có `inotify` nào để nghe |
| Hỏi bằng ngôn ngữ tự nhiên rồi đoán mục tiêu | Xung đột doctrine *"KHÔNG dùng RAG để trả NGUYÊN VĂN"*. Code đoán sai thì lập trình viên thấy ngay; điều luật đoán sai thì ra nguyên văn sai điều |
| Telemetry (codegraph mặc định **BẬT**) | Kho làm việc với hồ sơ dự thảo luật |
| *"Trust results — don't re-verify with grep"* | Trái thẳng bài học *"cổng có thể xanh vì đồ GIẢ nói dối"* |

---

## 2. Phát hiện chính — đo được, không phải ý kiến

### Đồ thị quan hệ ĐÃ TỒN TẠI, và tốt hơn vẻ ngoài

| Đã có | Bằng chứng |
|---|---|
| Cạnh **CÓ KIỂU**: `SUA_DOI_BASE` · `CHU_THICH_LICH_SU` · `DAN_CHIEU_NOI_DUNG` | `scripts/tl_core/lookup_ops.py:1684` |
| **BẮC CẦU**: `consolidation_chain` + BFS `frontier`/`seen`/`dry_rounds` | `_rasoat_dedup_push` — `lookup_ops.py:1720` |
| Cạnh **CẤP ĐIỀU** + `pending_effect`/`hieu_luc` | `dieu_level_amendment_map` |
| **Lỗ hổng nguồn** ba mức + `missing_in_corpus` | `scripts/tl_core/fetch_web.py:189` |

> **Đính chính đã ghi:** lượt trả lời đầu của phiên soạn báo *"không có bắc cầu"* — **SAI**, đã sửa.
> Ghi ra đây vì nó là bằng chứng rằng phép đo đã lật một phần lập luận ban đầu, và có thể lật tiếp.

### Thiếu đúng HAI thứ — và cả hai kế hoạch ĐÃ TỰ KHAI

**(1) KHÔNG LƯU BỀN.** Cache hiện có chỉ gồm `manifest.json`, `manifest_index.json`,
`manifest.dirty`, `fetch_queue.json`, `corpus_audit_ckpt_*` — **không có cache quan hệ nào**.
Mỗi lượt `xref`/`frontier-expand` đọc lại nguyên văn qua mạng rồi **vứt kết quả đi**.

- `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md:173` — *"THIẾU: **lưu bền** hàng đợi qua các phiên"* (~85%)
- cùng tệp `:175` — *"THIẾU: trạng thái theo đơn vị rà + **lưu bền** + spawn agent"* (~55%)

**(2) CẠNH CHỈ ĐI MỘT CHIỀU — đây mới là chỗ đau.** `frontier-expand` khai đúng phạm vi của nó:
*"trích mọi văn bản được DẪN CHIẾU **trong 1 văn bản**"* = trả lời **"tôi trỏ tới ai"**.

Câu của người rà soát dự thảo là câu **NGƯỢC**: *"ai đang trỏ vào Luật A — sửa nó thì gãy gì?"*
Hôm nay phải chạy `xref` lên **toàn bộ ~500 văn bản** mới biết, mỗi văn bản một lượt đọc mạng
⇒ thực tế không ai làm ⇒ PHA 2 bù bằng NLM — mà `references/QUY_TRINH_RA_SOAT_3_TANG.md:4`
đã tự khai NLM *"RAG recall hạn chế, **không chứng minh được 'vắng mặt'**"*.

### Lý lẽ cốt lõi, và giới hạn phải giữ nguyên khi trình bày lại

`"Không văn bản nào trong corpus trỏ vào Luật A"` là mệnh đề **QUYẾT ĐỊNH ĐƯỢC** trên một bảng
cạnh; nó **KHÔNG** quyết định được qua recall của RAG.

**Giới hạn:** chỉ chứng minh được vắng mặt **TRONG corpus**. Corpus vẫn khuyết. Vì thế trạng thái
thứ ba **`chua_do_duoc` là BẮT BUỘC, không phải trang trí** — làm tròn nó thành *"không có cạnh"*
là để công cụ **nói dối đúng câu hỏi nó sinh ra để trả lời** (doctrine `None ≠ False`, luật ba
trạng thái `có · không · không đo được`).

---

## 3. Ràng buộc kỹ thuật SUÝT làm hỏng packet (đã khoá ở spec §4.1)

| Bẫy | Đo được | Chốt |
|---|---|---|
| Đi theo tiền lệ **GẦN NHẤT** thay vì tiền lệ **ĐÚNG** | `_frontier_candidates` gọi hàm PURE bằng **tên trần** ⇒ **có trong `_STUB_MAP`** (`tl.py:1419`) ⇒ **buộc sửa `tl.py`** ⇒ vi phạm ràng buộc §E *"KHÔNG đụng `tl.py`"* | Selftest phải dùng `import tl_core.quanhe` — tiền lệ `tl_selftest.py:3807` |
| Thêm **lệnh `tl` mới** | BUỘC sửa `_STUB_MAP` — `AG-T0-03` đã phải thêm `'cmd_registry_coverage'` vào `tl.py:1664` | Q6=A chọn **CỜ trên lệnh sẵn có** ⇒ mâu thuẫn với §E **biến mất bằng thiết kế**, không cần miễn trừ |
| Tưởng thêm tệp `tl_core` làm đỏ canary gói | Canary `tl_selftest.py:2423` liệt kê **22** module trong khi cây thật có **32** — vốn đã KHÔNG vét cạn, vẫn xanh | Không cần tệp thứ ba. Gói đang **180/200** |

---

## 4. Yêu cầu của người giữ kho cho phiên nhận

> *"Nghiên cứu, tích hợp phù hợp, có **tham khảo đa chiều**."*

1. **THÁCH THỨC các phép đo trên — đừng nhận nguyên.** Bốn chỗ dễ sai nhất:
   - (a) *"không có cache quan hệ nào"* — chỉ grep `_cache_file`, có thể sót đường khác;
   - (b) *"cạnh chỉ một chiều"* — có chắc không có chỉ mục ngược ở đâu đó không;
   - (c) ngưỡng ruff **12 F821** chép từ mốc **v1.35.60**, cây nay **v1.36.68** ⇒ **có thể đã trôi**, phải đo nền lại trên `origin/master` sạch;
   - (d) con số corpus **~500** đọc từ ghi chú `v1.34.42` trong `tl.py`, **chưa đo LIVE**.
2. **ĐỐI CHIẾU kế hoạch mà phiên soạn CHƯA đọc kỹ:** `ops/KE_HOACH_DIEU_CHINH_DA_NEN_TANG.md` ·
   `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md` · `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` ·
   `docs/WORKFLOW_RASOAT_TU_DONG.md`. Đợt 5 có va lane nào không, nên xếp sau gì.
3. **XÉT THỨ TỰ ƯU TIÊN thật.** Lane PLAT/W0–W2 đang chạy dở. Đợt 5 chen vào đâu, hay xếp hàng —
   **phiên soạn KHÔNG có thẩm quyền quyết định điều này.**
4. **THAM KHẢO ĐA CHIỀU.** Nếu `codex` còn quota, xin một lượt cross-review khác nền trên chính
   hai tệp spec, neo exact `9f1ad3712d9ad4452250b9e5b29189805b2ba7d2`.
   ⚠ Đo được trong container phiên soạn: `codex` đang **`SAP_HET_HAN`** (ảnh chụp cũ ~122.8h,
   `last_refresh=2026-08-16`; refresh token **xoay vòng** nên bản trong `CODEX_AUTH_JSON` có thể
   **đã bị vô hiệu**). Kiểm bằng `launcher.py doctor` TRƯỚC — **đừng tin `codex login status`**,
   nó NÓI DỐI (chỉ kiểm tệp đọc được, không kiểm token còn sống).
5. **Nếu thấy ý này KHÔNG đáng làm, nói thẳng, nêu lý do đo được.** Người giữ đã được chào phương
   án *"không làm"* (Q2=D) và chọn làm — nhưng **phép đo mới có quyền lật lại**.

---

## 5. Tám quyết định người giữ đã chốt (21-08-2026)

| # | Câu hỏi | Chốt |
|---|---|---|
| Q1 | Kế hoạch nhận | **A** — `KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md`, thành **Đợt 5** |
| Q2 | Phạm vi | **B** — lưu bền **+ chỉ mục ngược CẤP VĂN BẢN** (không cấp Điều) |
| Q3 | Nơi lưu | **A** — cache cục bộ theo profile, cạnh `manifest_index.json` (KHÔNG đẩy Drive) |
| Q4 | Làm mới | **A** — tăng dần theo `md5` + **bắt buộc** trạng thái thứ ba |
| Q5 | Cắt lát | **A** — 2 lát: `RS5-H10` engine thuần / `RS5-H11` CLI+cache |
| Q6 | Phơi CLI | **A** — **cờ** trên lệnh sẵn có, KHÔNG lệnh `tl` mới |
| Q7 | `review_class` | **A** — `systemic` (sàn, không phải trần) |
| Q8 | Nghiệm thu | **A** — cổng máy **OFFLINE**; LIVE đẩy sang **Đợt 4** |

## 6. Thứ CHƯA làm, có chủ đích

- **KHÔNG** sửa thẳng `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md` — tệp đó không nằm trong write
  set của lease nào đang mở. Bản chèn (§C/§D/Đợt 5/§PHỤ LỤC) để người có thẩm quyền tự đưa vào.
- **KHÔNG** mở Packet Issue, **KHÔNG** xin lease, **KHÔNG** viết dòng mã nào.
- **KHÔNG** soạn spec `RS5-H11` (lát 2): ADR-0044 đòi lát sau mọc trên `mission/<issue>/integration`
  **đã nhận** lát trước; và write set H11 phụ thuộc tên hàm mà H10 đẻ ra — đóng băng bây giờ là neo
  mô tả vào thứ chưa tồn tại.
- **CHƯA** chạy `selftest`, **CHƯA** chạy `ruff` trong phiên soạn. Mọi con số ca (1.040 tĩnh /
  1.526 theo CHANGELOG) đọc từ mã, chưa đo lại.
- **CHƯA** chạy codegraph (xem cảnh báo mức tin cậy ở §1).
