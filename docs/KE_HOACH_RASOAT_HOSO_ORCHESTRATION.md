# KẾ HOẠCH — LỚP ĐIỀU PHỐI RÀ SOÁT HỒ SƠ DỰ THẢO LUẬT (trên skill tra-luat)

> Trạng thái: ĐỀ XUẤT (chưa triển khai). Phạm vi: lớp điều phối phía trên skill — KHÔNG đụng `scripts/tl.py`
> trừ khi nêu rõ. Nguồn gốc: phiên kiến trúc 2026-07-25.
> **Nền đo:** bản này đối chiếu trên `v1.35.38` (`ccad292`). Bản đầu (`1835b46`, nhánh
> `claude/legal-document-review-architecture-dlbrut`) đối chiếu trên `v1.35.32` (`96b56f4`) — xem §0.
> Tài liệu nền: `references/QUY_TRINH_RA_SOAT_3_TANG.md` · `references/CHECKPOINT_TEST_PLAN.md` · ADR-0001 · ADR-0004.

---

## §0. BẢN NÀY SỬA GÌ SO VỚI BẢN ĐẦU (1835b46)

Bản đầu đúng về kiến trúc và nguyên tắc. Bảy điểm sau là sai/thiếu về **hiện trạng đo được**, đã kiểm lại bằng
đọc mã nguồn — mỗi điểm dẫn `file:dòng`. Đây là phần làm thay đổi khối lượng việc, không chỉ câu chữ.

| # | Bản đầu nói | Đo lại trên v1.35.38 | Hệ quả với kế hoạch |
|---|---|---|---|
| 0.1 | "`tl loop` là loop vệ sinh registry, KHÔNG phải worklist rà" → thiếu vòng lặp (~30%) | ĐÚNG về `loop`, nhưng **BỎ SÓT `tl rasoat-loop`** — đã là orchestrator rà khép kín, report-only, hội tụ theo `--dry-rounds K`/`--max-iter` (`command_registry.py:939`, `lookup_ops.py:1681`); kèm `tl frontier-expand` xuất `missing_in_corpus` (`command_registry.py:930`) | H3 chuyển từ **XÂY MỚI** sang **BỌC/MỞ RỘNG**. Ngữ nghĩa dừng phải dùng lại `dry_rounds`/`max_iter`/PAUSE, không đặt bộ mới |
| 0.2 | Nạp bổ sung ~70%: "THIẾU hàng đợi động máy-đọc-được" | `frontier-expand --json` → `missing_in_corpus` **chính là** hàng đợi động máy-đọc-được, đã nối `ingest-missing` | Hàng đợi không cần thiết kế lại; H3 chỉ cần **lưu bền** hàng đợi đó vào PLAN |
| 0.3 | Một tham chiếu đứt: `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` | **HAI** tham chiếu đứt. Thứ hai: `scripts/nlm_log.py` — `git log --all` **rỗng**, chưa từng tồn tại, nhưng `DOCTRINE_APPENDIX.md:62,65,68,70,85` đặc tả cả cờ (`--answer`, `push`, `--file`, `--folder-name`) và `rasoat_worksheet.py:188` xuất đường dẫn tới nó | Giảm thiểu rủi ro F5 ("bắt buộc `nlm_log.py add`") **không chạy được**. H1 phải gánh cả hai |
| 0.4 | C2 bảng master: "JSONL/JSON append-only" | Bên đọc duy nhất `rasoat_phuluc.py:61 load_master` dùng `json.loads(read_text())` — **KHÔNG đọc được JSONL**. Nhưng nó **glob `*.json` trong THƯ MỤC và gộp** | Append-only đạt được **miễn phí** ở mức thư mục: 1 file `.json`/đơn vị rà. Chọn JSONL = phải sửa `rasoat_phuluc.py` |
| 0.5 | C1/C2 nằm ở "file outputs" | Repo **không có** quy ước `outputs/`. Quy ước thật: `~/.tra_luat_cache` (`rasoat_worksheet.py:22`) + `--out-dir`. `outputs/` không nằm trong `.gitignore` cũng không trong `_RELEASE_EXCLUDE_DIRS` (`release.py:325`) | **Bẫy chặn gate**: state biến động trong cây skill sẽ bị walk vào `RELEASE_MANIFEST` → lệch `package_hash` → `release-verify` ĐỎ. Xem §B.5 |
| 0.6 | "File mới cho LIVE đặt ở `references/`/`templates/` (vào zip)" | Vào zip thì đúng (walk theo loại-trừ). Nhưng thiếu 2 bước: `templates/` chưa có trong `_RELEASE_REQUIRED_FILES` (`release.py:380–420`) và `RELEASE_MANIFEST.json` phải regen (181 → 182 file) | Thêm file mà không regen manifest = `release-verify` FAIL trong gói (tiền lệ ghi ở `release.py:334`: "file_count lệch zip-set 115≠109") |
| 0.7 | Nghiệm thu H1–H6 toàn bộ do người mắt thường xác nhận | CLAUDE.md buộc "thêm test `rXX_` cho mỗi fix"; đã có sẵn cơ chế cổng: `workflow-audit` (fail-closed trong `release-verify`, `release.py:73,243`) + guard `links_missing` (`release.py:537`) | Thêm H9 (§E) biến nghiệm thu H1 thành **cổng máy**, và mỗi hạng mục gắn 1 mã test |

**Không phải rủi ro:** nhánh `dlbrut` dựng trên `96b56f4` — đã kiểm `git merge-base --is-ancestor`: đây là tổ tiên
của `master`, nên hợp nhất chỉ THÊM tài liệu, không lùi r202–r207. Chỉ là **nền đo bị trễ**: r203–r205 (engine
`run_pipeline`, `profile-ingest-resume` lên bảng stage, gộp `ingest_commit`) làm hàng "Nạp hồ sơ" và "kế nhiệm/resume"
ở §D mạnh hơn lúc đo. Đã cập nhật ở §D.

---

## A. MÔ TẢ BÀI TOÁN

Rà soát hồ sơ văn bản dự thảo luật là tác vụ dài, nhiều bước, frontier động:

1. Nạp hồ sơ (nhiều văn bản) vào Profile.
2. Lập kế hoạch rà nhiều bước cho cả hồ sơ.
3. Rà từng bước: kết hợp NLM (định vị/quan hệ) + đọc file trực tiếp (nguyên văn từ cache/raw).
4. Ghi kết quả trung gian ra nơi lưu state (§B.5).
5. Giữa chừng phát hiện văn bản mới → nạp bổ sung → rà thêm.
6. Gặp lỗi skill → sửa → nạp lại → chạy tiếp.
7. Lặp đến khi hết kế hoạch → tổng hợp & trình bày theo yêu cầu người dùng.

**Mục tiêu:** chạy đầu-cuối tự trị, người chỉ chạm HAI ĐẦU (giao việc + nghiệm thu); giữa chừng máy tự chạy,
trừ các điểm dừng có chủ đích (mục B.4).

## B. NGUYÊN TẮC KIẾN TRÚC (đã chốt)

1. **Một skill lõi + command quy trình mỏng.** KHÔNG tách runtime thành nhiều skill (tránh drift VERSION/deploy).
   Quy trình đóng gói dạng lớp mỏng theo pattern `/gate`, `/release-checklist` sẵn có.
2. **Agent theo tiêu chí CÁCH LY CONTEXT, không phân vai.** Mô hình hub-and-spoke: phiên chính điều phối và là
   **bên ghi duy nhất tại mỗi thời điểm**; mọi agent con read-only (bài học rogue-edit). Agent trả JSON theo
   schema cố định, phiên chính chỉ nhận kết luận (G5 §11 — giữ context sạch).
3. **Worklist loop + kế-hoạch-là-file, KHÔNG graph engine.** Frontier động (văn bản mới phát sinh) mô tả bằng
   hàng đợi trong PLAN file, không phải DAG tĩnh. **State nằm trong file, không nằm trong context** — điều kiện
   để kế nhiệm phiên: "phiên chính" là VAI TRÒ chuyển giao tuần tự, không phải một cửa sổ context bất tử.
4. **Điểm dừng có chủ đích (giữ nguyên, không tự động hoá qua):** hook duyệt `--apply`/`*-delete`/`--clear-stale`;
   deploy tay ở LIVE (`upload-skill-to-Package.cmd`); kết luận cuối + ký do người rà soát (Mục G).
5. **(MỚI — §0.5) State biến động NẰM NGOÀI cây skill.** Đây là doctrine đã trả giá: r193 (backup config lọt bundle
   → token LIVE lên Drive) và r202 ("backup config profile-delete ra NGOÀI cây skill"). Cây skill được hash toàn
   bộ vào `package_hash`; mọi file thay đổi theo lượt rà mà nằm trong cây sẽ làm `release-verify`/golden ĐỎ.
   → PLAN.json + bảng master ghi ở `~/.tra_luat_cache/rasoat/<ho_so_id>/`, hoặc `--out-dir` trỏ ngoài cây.
   Chỉ **MẪU rỗng** (template, bất biến) mới được nằm trong cây và vào zip.
6. **(MỚI — §0.1) Tái dùng từ vựng hội tụ đã có, không đặt bộ mới.** `tl loop` và `tl rasoat-loop` đã dùng chung
   một idiom: `--dry-rounds K` (K vòng liên tiếp không sinh việc mới = HỘI TỤ) + `--max-iter` (fail-safe) + PAUSE
   khi no-progress/verify-hụt. Vòng lặp hồ sơ (C3) phải nói đúng bộ từ này để người đọc log không phải học 2 lần.

## C. KIẾN TRÚC ĐÍCH — THÀNH PHẦN

```
NGƯỜI: giao việc (kickoff contract) ──► PHA 0 tiền kiểm (doctor/precheck/cookie) ── fail → DỪNG SỚM
                                                       │ ok
        ┌──────────────── VÒNG LẶP WORKLIST (phiên chính) ────────────────────────────┐
        │ đọc PLAN.json → lấy đơn vị pending → spawn agent tl-rasoat (read-only)      │
        │ ← nhận JSON phát hiện đã verify → ghi 1 file .json/đơn vị → cập nhật PLAN   │
        │ frontier-expand → missing_in_corpus → append hàng đợi PLAN (trong uỷ quyền) │
        │ lỗi skill → BUGS_FOUND.md + workaround, chỉ dừng khi CHẶN ĐỨNG              │
        │ cạn context/ngân sách NLM → chốt checkpoint + note bàn giao → phiên KẾ NHIỆM│
        └── HỘI TỤ: hết pending + hàng đợi rỗng ≥K vòng + phát hiện đã verify ──► ra ─┘
                                                       │
                             PHA 4 tổng hợp (context sạch, chỉ đọc thư mục master)
                                                       │
NGƯỜI: nghiệm thu (duyệt Phiếu A–G, duyệt lô lệnh --apply chờ, ký)
```

| # | Thành phần | Dạng | Nơi lưu | Ghi chú |
|---|---|---|---|---|
| C1 | `PLAN.json` hồ sơ | JSON máy-đọc-được, **biến động** | `~/.tra_luat_cache/rasoat/<ho_so_id>/PLAN.json` | văn bản × đơn vị rà × trạng thái (pending/doing/done) + hàng đợi phát sinh + note bàn giao + quota NLM còn lại + `session_claim` |
| C2 | Bảng master phát hiện | **THƯ MỤC nhiều file `.json`**, mỗi đơn vị 1 file (append-only ở mức thư mục — §0.4) | `~/.tra_luat_cache/rasoat/<ho_so_id>/master/` | schema = bảng C Pha 4, field name theo đúng `rasoat_phuluc.py` (§E/H1); đầu vào duy nhất của `rasoat_phuluc.py --in <thư mục>` |
| C3 | Vòng lặp `/rasoat-hoso` | reference + command mỏng | `references/` (+ wrapper `.claude/commands/`) | kịch bản worklist **bọc `rasoat-loop`/`frontier-expand`**, dùng từ vựng `dry_rounds`/`max_iter`/PAUSE |
| C4 | Agent rà đơn vị `tl-rasoat` | prompt mẫu (read-only) | `references/` (+ wrapper `.claude/agents/`) | Tầng 1→3 + VERIFY cho MỘT đơn vị; cấp quota NLM trong prompt; trả JSON schema C2 |
| C5 | `BUGS_FOUND.md` + chính sách degrade-and-continue | quy ước trong quy trình | ngoài cây skill (§B.5) | lỗi có workaround → ghi + đi vòng; chỉ blocker mới dừng chờ người |
| C6 | Kickoff contract | mẫu giao việc | `references/` | phạm vi hồ sơ, uỷ quyền ghi (nạp văn bản THUỘC hồ sơ), ngân sách, chính sách lỗi |
| C7 | **(MỚI)** Thẻ quy trình `rasoat_hoso` | `workflow_card.v1` — **bất biến**, có cổng | `references/workflows/rasoat_hoso.json` | MẪU tĩnh của vòng lặp: `plan[]`/`verify[]`/`stop_conditions[]`/`resume_behavior`. Được `workflow-audit` + `release-verify` kiểm tự động (§E/H2) |

**Tách MẪU (bất biến, trong zip, có cổng) khỏi THỰC THỂ (biến động, ngoài cây, không hash):** C7 + mẫu rỗng của
C1/C2 nằm trong cây; C1/C2 thực tế của từng hồ sơ nằm ngoài cây. Nhập nhèm hai thứ này là cách nhanh nhất
làm gate đỏ (§0.5).

**Lưu ý đóng gói:** zip deploy LOẠI `.claude/` (`release.py:326`) → mọi thứ LIVE cần phải nằm ở `references/` +
`templates/` + 1 dòng vocab trong `SKILL.md`. `.claude/commands/` + `.claude/agents/` chỉ là wrapper dev-side.
Agent cho LIVE = phiên chính spawn general-purpose với prompt mẫu trong references (LIVE không có file agent riêng).

## D. HIỆN TRẠNG ĐÁP ỨNG (đo lại trên v1.35.38)

Tầng công cụ ~88% · tầng điều phối ~45% · tổng ~**70–75%** (bản đầu: 65–70% — nâng do §0.1/§0.2: vòng lặp và
hàng đợi động đã có phần lõi, và do r203–r205 làm chặt đường nạp/resume).

| Yêu cầu | Mức | Đã có / Còn thiếu (bằng chứng) |
|---|---|---|
| Nạp hồ sơ vào Profile | ~95% | profile-promote/ingest-*, apply fail-closed (plan-hash+confirm), 3 van NLM, bảng tay, `--resume`. **+r203–r205:** engine `run_pipeline` (ADR-0004 D1), `profile-ingest-resume` lên 5 stage `_pr_stage_*` parity byte-equal |
| Rà NLM + đọc file | ~90% | quy trình 3 tầng, `rasoat_worksheet` (Tầng 1 tất định), `tra_cuu --cite --exact`, nlm_qa verify |
| Write-safety registry | ~90% | precheck, WAL journal, resume, undo, `journal --close` |
| Nạp bổ sung giữa chừng | **~85%** (↑70) | `frontier-expand --json` → `missing_in_corpus` = hàng đợi động máy-đọc-được, nối `ingest-missing` (`command_registry.py:930`). THIẾU: **lưu bền** hàng đợi qua các phiên |
| Kế hoạch mức HỒ SƠ | ~40% | worksheet chỉ per-văn-bản, định dạng cho người; THIẾU PLAN.json (C1) |
| Vòng lặp rà đến hết plan | **~55%** (↑30) | `tl rasoat-loop` đã hội tụ khép kín (SEED→expand→đệ quy in-corpus→dedup seen→`dry_rounds≥K`), report-only (`lookup_ops.py:1681`). THIẾU: **trạng thái theo đơn vị rà** + lưu bền + spawn agent. (`tl loop` là việc khác: vệ sinh registry, `command_registry.py:1215`) |
| Sửa skill giữa chừng | ~60% | ADR-0001 bundle, gate, `tl_boot` self-heal; THIẾU C5 |
| Tổng hợp & trình bày | ~70% | `rasoat_phuluc`, văn phong/thể thức references. ⚠ **HAI tham chiếu đứt** (§0.3): `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (`QUY_TRINH:91`, `DOCTRINE_APPENDIX:78`, `rasoat_phuluc.py:9`) và `scripts/nlm_log.py` (`QUY_TRINH:91`, `DOCTRINE_APPENDIX:62–85`, `rasoat_worksheet.py:188`) — cái sau chưa từng tồn tại trong git |
| Kế nhiệm phiên | ~55% | journal/resume phủ phần ghi (r205 chặt thêm); THIẾU note bàn giao trạng thái rà (gộp vào C1) |
| **(MỚI)** Cổng máy cho lớp điều phối | ~15% | `workflow-audit` + `_RELEASE_REQUIRED_WORKFLOWS` + golden 0-diff là cơ chế sẵn sàng dùng lại; nhưng guard `links_missing` **chỉ quét SKILL.md** và **chỉ khớp mẫu `references/…`** (`release.py:527,537`) → mù với 2 tham chiếu đứt ở §0.3 |

## E. KẾ HOẠCH TRIỂN KHAI

Ràng buộc chung: KHÔNG đụng `tl.py` (trừ H7 nếu lộ bug thật — theo đúng quy trình sửa code + test `rXX_`).
H9 có sửa `scripts/tl_core/release.py`; H1 có thể sửa `scripts/rasoat_phuluc.py` — **cả hai đều phải qua quy trình
đầy đủ**: ruff → selftest N/N (thêm test `rXX_`) → CHANGELOG → bump VERSION 3 chỗ. Mỗi hạng mục dưới đây có
**1 mã test** để nghiệm thu bằng máy, không bằng mắt (§0.7).

Thêm file vào cây skill = 3 bước, không phải 1: (a) tạo file; (b) thêm vào `_RELEASE_REQUIRED_FILES` nếu là file
bắt buộc; (c) **regen `RELEASE_MANIFEST.json`** (181 → 182) trong bước bump/đóng gói rồi `release-verify` trên
GÓI. Bỏ (c) = gói ĐỎ ở LIVE (§0.6).

> Đo được 2026-07-25: `RELEASE_MANIFEST.json` trên `master` mới chỉ regen tới r205 (`v1.35.36`), trong khi cây
> đang ở `v1.35.38` — tức manifest **thường xuyên trễ giữa chu kỳ** và chỉ khớp lại ở bước bump. Vì vậy (c) là
> việc của bước đóng gói, KHÔNG phải việc lúc tạo file; và `release-verify` trên cây dev không phải cổng có
> nghĩa cho hạng mục này (nguồn sự thật là package-set — xem chú thích r184/REL-01 tại `release.py:527`).

### Đợt 1 — Nền tảng state (điều kiện tiên quyết của mọi thứ sau)

| Hạng mục | Sản phẩm | Nghiệm thu (mã test) |
|---|---|---|
| **H1. Khôi phục 2 tham chiếu đứt** | (a) `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` — schema **suy từ mã bên đọc**, không từ prose: gốc `{co_quan, van_ban[], noi_dung[]}`; `van_ban[]` = `so_hieu·ten·ngay·hieu_luc_tu·sua_doi_bo_sung·tinh_trang·loai·linh_vuc·ghi_chu`; `noi_dung[]` = `key·van_ban·can_cu·phan_tich·hinh_thuc·lo_trinh·tieu_chi·linh_vuc·ghi_chu`. (b) Quyết một trong hai: viết `scripts/nlm_log.py` đúng đặc tả `DOCTRINE_APPENDIX:62–85`, HOẶC xoá đặc tả đó và đổi F5 sang cơ chế có thật | `r2xx_master_template_doc_duoc`: `rasoat_phuluc.py --in <mẫu>` rc=0, sinh đủ 03–07-BN. `r2xx_hinh_thuc_vocab`: mọi giá trị `hinh_thuc` trong mẫu route đúng bucket — **bẫy**: `route()` (`rasoat_phuluc.py:46`) khớp chuỗi cố định ("ban hành mới"→05, "bãi bỏ toàn bộ"→06, "tạm ngưng/ngừng toàn bộ"→07, "nghiên cứu"/"mục f"/`chờ…`→F), sai chính tả = **âm thầm** rơi hết vào 04 |
| **H1b. Ba trường bảng C không có chỗ trong schema hiện tại** | Bảng C yêu cầu *nguyên văn-cite*, *định tuyến phụ lục*, *mức độ chắc chắn*; `noi_dung[]` không có trường nào cho 3 thứ đó (định tuyến thì **tính** từ `hinh_thuc`). Chốt: mở rộng `rasoat_phuluc.py` thêm trường, HOẶC quy ước dồn vào `ghi_chu` | `r2xx_bang_c_du_truong`: mỗi phát hiện trong mẫu truy lại được nguyên văn + mức chắc chắn sau khi qua `rasoat_phuluc.py` (không mất dữ liệu) |
| **H2. Schema PLAN hồ sơ** | (a) `references/workflows/rasoat_hoso.json` theo **`workflow_card.v1` sẵn có** (`plan[]`, `verify[]`, `stop_conditions[]`, `idempotency_contract`, `journal_key`, `resume_behavior`, `resume_command`, `write_scope`, `risk`) — không đặt schema mới cho phần tĩnh; (b) `references/RASOAT_PLAN_SCHEMA.md` chỉ đặc tả phần **biến động** (`rasoat_plan.v1`: trạng thái/hàng đợi/bàn giao/quota/`session_claim`) + 1 JSON mẫu | `r2xx_the_rasoat_hoso_hop_le`: `workflow-audit --strict --json` ok=true với thẻ mới; thêm vào `_RELEASE_REQUIRED_WORKFLOWS` + golden 0-diff. Phần biến động: Claude sinh được PLAN từ hồ sơ mẫu bằng tay theo schema, không cần code mới |
| **H9. (MỚI) Mở rộng guard tham chiếu đứt** | `_skill_links_findings` (`release.py:527`) hiện chỉ đọc `SKILL.md` và chỉ khớp regex `references/…`. Mở rộng: quét thêm `references/*.md`, và khớp cả `templates/…` + `scripts/…` | `r2xx_links_guard_bat_2_ref_dut`: chạy guard trên cây **trước H1** phải báo đúng 2 mục (`templates/MAU_…json`, `scripts/nlm_log.py`); chạy **sau H1** phải rỗng. Đây là thứ biến nghiệm thu H1 thành cổng máy — và là lý do 2 tham chiếu đứt sống được nhiều bản |

*Vì sao H9 nằm ở Đợt 1:* nó là cái duy nhất bảo đảm Đợt 1 không tự tạo thêm tham chiếu đứt mới. Làm sau = làm lại.

### Đợt 2 — Lớp điều phối

| Hạng mục | Sản phẩm | Nghiệm thu (mã test) |
|---|---|---|
| **H3. Vòng lặp rà hồ sơ (BỌC, không xây mới — §0.1)** | `references/RASOAT_HOSO_LOOP.md`: worklist đọc PLAN → spawn → ghi 1 file `.json`/đơn vị → cập nhật PLAN → HỘI TỤ → chốt checkpoint. **Gọi `rasoat-loop`/`frontier-expand` làm lớp phát hiện**; PLAN chỉ thêm cái chúng không có: trạng thái theo đơn vị + lưu bền + `session_claim`. Dùng nguyên từ vựng `dry_rounds`/`max_iter`/PAUSE (§B.6). + wrapper dev `.claude/commands/rasoat-hoso.md` + 1 dòng vocab `SKILL.md` | `r2xx_loop_hoi_tu_dung_thu_tu`: chạy khô trên PLAN mẫu — đúng thứ tự, dừng đúng khi `dry_rounds` đạt K, PLAN cập nhật sau MỖI đơn vị (không dồn cuối). `r2xx_loop_khong_ghi_trong_cay`: sau lượt chạy khô, `git status` sạch và `release-verify` vẫn ok (kiểm §B.5) |
| **H4. Agent rà đơn vị** | prompt mẫu `tl-rasoat` trong `references/RASOAT_HOSO_LOOP.md` (read-only, quota NLM trong prompt, output JSON schema H1) + wrapper dev `.claude/agents/tl-rasoat.md` (cùng khung ranh giới cứng như `tl-auditor`) | `r2xx_agent_output_dung_schema`: agent rà 1 đơn vị thật, JSON hợp lệ schema H1, **không ghi file nào** (kiểm bằng `git status` + mtime cây skill); phát hiện đối chiếu được với rà tay |

### Đợt 3 — Tự trị hoá

| Hạng mục | Sản phẩm | Nghiệm thu (mã test) |
|---|---|---|
| **H5. Degrade-and-continue + bug ledger** | mục mới trong `QUY_TRINH_RA_SOAT_3_TANG.md`: phân loại lỗi (workaround/blocker), format `BUGS_FOUND.md`, quy tắc "sửa nóng CHỈ khi chặn đứng; còn lại gom vá sau lượt rà" | `r2xx_degrade_khong_dung_vong`: bơm 1 lỗi giả lập giữa vòng rà → vòng lặp ghi ledger và chạy tiếp, PLAN vẫn tiến |
| **H6. Kickoff contract + tiền kiểm** | mẫu giao việc trong `RASOAT_HOSO_LOOP.md` (phạm vi, uỷ quyền nạp văn-bản-thuộc-hồ-sơ, ngân sách NLM, chính sách lỗi) + **mở rộng PHA 0 đã có** (`QUY_TRINH:30`) thêm doctor/precheck/tuổi cookie — fail → dừng TRƯỚC khi rà | `r2xx_pha0_cookie_gia_dung_som`: cookie giả >14 ngày → dừng ở Pha 0 với thông báo 1 dòng, chưa tiêu 1 call NLM nào |

### Đợt 4 — Kiểm chứng LIVE (không thể cổng-máy — đây là phần duy nhất cần người)

| Hạng mục | Sản phẩm | Nghiệm thu |
|---|---|---|
| **H7. Chạy thật 1 hồ sơ nhỏ (2–3 văn bản) trên Cowork LIVE** | log đếm: số lần người phải xen vào giữa chừng + lý do; PLAN/bảng master/phiếu ra đúng | ≤2 lần xen giữa chừng; mỗi lần đều thuộc danh mục điểm-dừng-có-chủ-đích (B.4) |
| **H8. Kiểm chứng kế nhiệm** | kill phiên giữa đơn vị đang rà → mở phiên mới | phiên mới đọc PLAN + note bàn giao, rà tiếp đúng chỗ, không lặp lại đơn vị `done`, mất tối đa 1 đơn vị dở |

### Định nghĩa HOÀN THÀNH toàn kế hoạch

Một hồ sơ thật chạy đầu-cuối: người giao việc 1 lần, nghiệm thu 1 lần; giữa chừng ≤2 điểm dừng thuộc B.4;
kill-phiên giữa chừng resume được; sản phẩm cuối = dự thảo Phiếu A–G + bảng master + danh sách đề xuất
chờ duyệt `--apply` + `BUGS_FOUND.md`. **Thêm:** gate offline vẫn N/N và `release-verify` ok sau toàn bộ Đợt 1–3
(lớp điều phối không được làm hỏng cổng phát hành), và guard H9 báo 0 tham chiếu đứt.

### Thứ tự phụ thuộc

`H9 → H1/H1b → H2 → H3 → H4 → H5/H6 → H7 → H8`. H9 trước H1 để guard bắt được trạng thái "trước khi sửa"
làm bằng chứng (test 2 chiều, đúng bài học đắt giá trong CLAUDE.md). H2 sau H1 vì PLAN trỏ tới schema master.

## F. RỦI RO & GIẢM THIỂU

| Rủi ro | Giảm thiểu |
|---|---|
| Cookie NLM chết giữa vòng rà (Cowork không tự refresh) | H6 tiền kiểm tuổi cookie; cron `secrets-set --nlm` phía local (COWORK_PROJECT.md §3) |
| Lỗi skill chặn đứng ở LIVE (deploy là bước tay) | H5 degrade-and-continue; tần suất giảm dần theo mỗi fix khoá test `rXX_` |
| Hai phiên cùng cầm quyền ghi (vi phạm single-writer) | quy ước trong H3: nhận vai = ghi `session_claim` vào PLAN; registry đã có LockService+RMW làm lưới dưới |
| LIVE drift (kết luận lỗi đo trên bản trễ) | mọi báo lỗi skill trong `BUGS_FOUND.md` ghi rõ VERSION đo được (CONTEXT.md — LIVE vs canonical). **Bản kế hoạch này là ví dụ sống:** §0 tồn tại vì bản đầu đo trên v1.35.32 |
| Agent con vượt quota NLM | quota ghi trong prompt + phiên chính đối chiếu sau mỗi đơn vị. ⚠ **SỬA (§0.3):** cơ chế cũ ghi là "bắt buộc `nlm_log.py add`" — script đó **không tồn tại**. Cho tới khi H1(b) chốt, đếm quota bằng số lần gọi ghi trong PLAN (`quota_con_lai`), không dựa vào `nlm_log` |
| **(MỚI)** State biến động lọt cây skill → `package_hash` lệch, `release-verify`/golden ĐỎ | §B.5: PLAN/master ra ngoài cây (`~/.tra_luat_cache/rasoat/<ho_so_id>/`); test `r2xx_loop_khong_ghi_trong_cay` khoá lại |
| **(MỚI)** Thêm file mẫu mà quên regen `RELEASE_MANIFEST` → gói FAIL ở LIVE | §E: quy tắc 3 bước (a/b/c); tiền lệ đã ghi trong `release.py:334` (115≠109) |
| **(MỚI)** `hinh_thuc` sai chính tả → phát hiện âm thầm rơi hết vào phụ lục 04 | test `r2xx_hinh_thuc_vocab` (H1) khoá bộ từ vựng có kiểm soát; không để `route()` fallback im lặng |

---

## PHỤ LỤC — CÁI GÌ ĐÃ CÓ MÀ KẾ HOẠCH NÊN DÙNG LẠI (chống xây trùng)

| Đã có | Ở đâu | Dùng cho hạng mục |
|---|---|---|
| `tl rasoat-loop` — orchestrator rà khép kín, hội tụ `dry_rounds`, report-only | `command_registry.py:939`, `lookup_ops.py:1681` | H3 (lớp phát hiện) |
| `tl frontier-expand` — `missing_in_corpus` = hàng đợi động | `command_registry.py:930` | H3 (hàng đợi) |
| `workflow_card.v1` + `workflow-audit` fail-closed + golden 0-diff | `references/workflows/workflow_card.schema.json`, `release.py:73,243` | H2 (phần tĩnh + cổng) |
| Guard `links_missing` (cần mở rộng) | `release.py:527,537` | H9 |
| `load_master` đọc **thư mục** `*.json` và gộp | `rasoat_phuluc.py:61` | C2 append-only, miễn phí |
| PHA 0 / ĐK DỪNG / NGÂN SÁCH đã có sẵn mục | `QUY_TRINH_RA_SOAT_3_TANG.md:30,85,103` | H6, H5 (mở rộng, không viết mới) |
| Khung agent read-only `tl-auditor` | `.claude/agents/tl-auditor.md` | H4 (khuôn ranh giới cứng) |
| Idiom `--dry-rounds`/`--max-iter`/PAUSE | `command_registry.py:1215` (`loop`), `:939` (`rasoat-loop`) | H3 (từ vựng dừng) |
