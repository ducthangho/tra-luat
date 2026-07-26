# KẾ HOẠCH — LỚP ĐIỀU PHỐI RÀ SOÁT HỒ SƠ DỰ THẢO LUẬT (trên skill tra-luat)

> Trạng thái: ĐỀ XUẤT (chưa triển khai). Phạm vi: lớp điều phối phía trên skill — KHÔNG đụng `scripts/tl.py`
> trừ khi nêu rõ. Nguồn gốc: phiên kiến trúc 2026-07-25.
> **Nền đo:** bản này đối chiếu trên `v1.35.38` (`ccad292`). Bản đầu (`1835b46`, nhánh
> `claude/legal-document-review-architecture-dlbrut`) đối chiếu trên `v1.35.32` (`96b56f4`) — xem §0.
> Tài liệu nền: `references/QUY_TRINH_RA_SOAT_3_TANG.md` · `references/CHECKPOINT_TEST_PLAN.md` · ADR-0001 · ADR-0004.
>
> **CHỐT 25-07 chiều (grill trên máy dev):** Q1 = (ii) SỬA LÕI · Q2 = XOÁ đặc tả `nlm_log.py` khỏi chỉ dẫn sống ·
> nơi lưu state = **LAI** (§B.5) · H1b = cấu trúc hoá (xem H1b) · baseline H9 = hằng số trong `release.py` (xem H9) ·
> đối chiếu kho best-practices ĐÃ LÀM — không mâu thuẫn, 3 bổ sung A1–A3 (xem WORKFLOW doc đầu file).
> **Nền đo (cập nhật 26-07 — CHẶN ĐÃ HẾT):** master ở `v1.35.43` (`r208c`; chuỗi r208a→r208-gas→r208b→r208c
> đều đã commit, cây SẠCH; GAS 2.21.2p ATOMIC RMW LIVE, `nlm_auth_status.v2`). Các commit mới không chạm
> file Đợt 1 đụng tới — nhận định hiện trạng vẫn đứng. **Đợt 1 = MỘT bump `1.35.44`, test prefix `r209_`**
> (thay mọi tên `r208_*` dưới đây — r208 đã bị chiếm). Hằng số vận hành mặc định + từ vựng: WORKFLOW §0/§0b.
> ADR kiến trúc điều phối (state LAI · single-writer theo claim · anchor): viết MỘT bản lúc Đợt 1 khởi công,
> số kế tiếp trong `docs/adr/` (chốt 26-07).

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

### §0.8. ĐO THẬT BLAST RADIUS CỦA H9 — 75 con trỏ đứt, và 4 "tài liệu hoá nhưng chưa từng viết"

Trước khi viết guard H9, đã **đo** thay vì đoán: quét 28 tài liệu trong package-set (SKILL.md + `references/*.md`)
với mẫu `(references|templates|scripts)/…` đối chiếu 182 file của package.

**Kết quả: 75 con trỏ đứt, không phải 2.** Guard fail-closed toàn bộ là bất khả thi ngay. Nhưng phân tầng thì rõ:

| Tầng | Số lượng | Nội dung | Xử lý |
|---|---|---|---|
| **A — LÕI, đường cấp cứu** | 2 | `scripts/build_parts.py` + `scripts/tl_rebuild.sh` — **SKILL.md:114,133,134,138 ra lệnh dứt khoát** ("Sửa file đã-chunk xong **PHẢI** `python scripts/build_parts.py`", "`sh scripts/tl_rebuild.sh`"), và `COWORK_EDIT_SAFETY.md:59–74` dựng cả quy trình cứu hộ 5 bước trên hai file này. `git log --all --diff-filter=ADR` **RỖNG** → chưa từng tồn tại | **H0 (mới) — ưu tiên cao nhất.** LIVE bị bảo chạy lệnh không có, đúng lúc file bị mount cắt cụt. Cơ chế `_parts`/`FORCE_CHUNK` thì CÓ thật trong `tl.py`/`tl_boot.py`/`tl_selftest.py`, và `tl_fetch.sh` có thật — nên chuỗi cứu hộ chỉ hụt 2 mắt |
| **B — tài liệu quy trình sống** | 3 | `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (`QUY_TRINH:91`, `rasoat_phuluc.py:9`), `scripts/nlm_log.py` (`QUY_TRINH:91`), `templates/_nguon-goc/` (`THE_THUC_TRINH_BAY.md`) | H1 (đã có) + mở rộng thêm `_nguon-goc/` |
| **C — lưu trữ lịch sử** | ~66 | Gần như toàn bộ từ `DOCTRINE_APPENDIX.md` — trỏ tới lớp script tiền-hợp-nhất (`doctor.py`, `nlm_qa.py`, `wizard.py`, `reg_delete.py`…) đã gộp vào `tl.py`/`tl_core/`. **Không phải bug** | Không dọn. Cần **allow-list baseline** + 1 dòng đầu `DOCTRINE_APPENDIX.md` ghi rõ đây là tài liệu LƯU TRỮ |
| **D — lệch đường dẫn** | ≥1 | `scripts/manifest_build.py` (`API_CONTRACT.md`) thật ra ở `scripts/_fallback/manifest_build.py` | Sửa con trỏ, không tạo file |

**Hệ quả thiết kế H9 (đổi so với §0.7):** guard KHÔNG thể là "mở rộng regex rồi fail-closed". Phải là
**ratchet có baseline**: (a) phân loại tài liệu — fail-closed cho tài liệu SỐNG (SKILL.md + quy trình), advisory
cho tài liệu LƯU TRỮ; (b) allow-list baseline chốt 66 mục tầng C, để guard fail-closed **với con trỏ MỚI ngay từ
ngày đầu** mà không phải dọn 75 mục trước. Không có baseline thì H9 vĩnh viễn đỏ và sẽ bị vô hiệu hoá.

**Nhận định quan trọng hơn từng lỗi lẻ:** cả 4 mục tầng A+B đều **được đặc tả rất chi tiết rồi không bao giờ được
viết** — `nlm_log.py` có cả đặc tả cờ (`--answer`/`push`/`--file`/`--folder-name`), `build_parts.py` có cả cờ
(`--verify`/`--rebuild`) và quy trình 5 bước. Đây là **mẫu hình lặp**, không phải 4 sự cố rời. Guard H9 chính là
thứ khiến mẫu hình này không tái diễn — đó là lý do nó xứng đáng đứng ở Đợt 1, trước cả H1.

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
5. **(MỚI — §0.5, CHỐT LAI 25-07) State biến động NẰM NGOÀI cây skill — và chia hai tầng bền.** Doctrine đã trả
   giá: r193 (backup config lọt bundle → token LIVE lên Drive) và r202. Cây skill được hash toàn bộ vào
   `package_hash`; mọi file thay đổi theo lượt rà mà nằm trong cây sẽ làm `release-verify`/golden ĐỎ. Nơi lưu **LAI**:
   - **State sống-còn** (`_meta/rasoat_state.json` = PLAN + Q-UNITS + Q-INGEST + Q-NLM + `session_claim` + quota +
     note bàn giao — nhỏ, ghi ở ranh giới đơn vị): **Drive `_meta/` của profile** (P7). Đây là nguồn sự thật resume;
     `~/.tra_luat_cache` không đủ bền (Claude chat xoá trắng sandbox mỗi phiên). RMW qua GAS đã ATOMIC (2.21.2p).
     Chi phí chấp nhận được: ~1 call/đơn vị so với 6 call/file của đường nạp.
   - **Sổ nặng** (`master/`, Q-APPROVALS, Q-BUGS — mỗi đơn vị 1 file, ghi 1 lần khi done): **local `--out-dir`
     ngoài cây**, đẩy Drive THEO LÔ ở checkpoint/Pha 4. Kill giữa chừng mất tối đa 1 đơn vị dở — đúng ngưỡng H8.
     **Riêng Claude chat:** đẩy `master/` sau MỖI đơn vị hoặc lô nhỏ (sandbox không sống qua phiên).
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
| C1 | PLAN hồ sơ (= `rasoat_state.json`) | JSON máy-đọc-được, **biến động** | **Drive `_meta/` của profile** (P7 — CHỐT LAI §B.5) | văn bản × đơn vị rà × trạng thái (pending/doing/done/blocked/stale) + Q-INGEST + **Q-NLM** + note bàn giao + quota NLM còn lại + `session_claim` |
| C2 | Bảng master phát hiện | **THƯ MỤC nhiều file `.json`**, mỗi đơn vị 1 file (append-only ở mức thư mục — §0.4) | local `--out-dir` ngoài cây, đẩy Drive theo lô ở checkpoint/Pha 4 (chat: mỗi đơn vị — §B.5) | schema = bảng C Pha 4, field name theo đúng `rasoat_phuluc.py` (§E/H1) **+ `anchor` + `muc_chac_chan` ngay từ đầu (H1b)**; đầu vào duy nhất của `rasoat_phuluc.py --in <thư mục>` |
| C3 | Vòng lặp `/rasoat-hoso` | reference + command mỏng | `references/` (+ wrapper `.claude/commands/`) | kịch bản worklist **bọc `rasoat-loop`/`frontier-expand`**, dùng từ vựng `dry_rounds`/`max_iter`/PAUSE |
| C4 | Agent rà đơn vị `tl-rasoat` | prompt mẫu (read-only) | `references/` (+ wrapper `.claude/agents/`) | Tầng 1→3 + VERIFY cho MỘT đơn vị; cấp quota NLM trong prompt; trả JSON schema C2. **(A1 — best-practice)** wrapper dev ÉP CỨNG bằng frontmatter `disallowedTools: Write, Edit, NotebookEdit` + `maxTurns` (nguồn: kho best-practice `claude-subagents.md`, bảng Frontmatter); prompt chỉ là lớp 2. LIVE không có file agent → prompt-only + hậu kiểm `verify-integrity` |
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
| **(MỚI)** Cổng máy cho lớp điều phối | ~15% | `workflow-audit` + `_RELEASE_REQUIRED_WORKFLOWS` + golden 0-diff là cơ chế sẵn sàng dùng lại; nhưng guard `links_missing` **chỉ quét SKILL.md** và **chỉ khớp mẫu `references/…`** (`release.py:527,537`) → mù với **75** con trỏ đứt đo được ở §0.8, trong đó 5 mục sống (2 mục nằm ngay trong LÕI, đường cấp cứu) |
| **(MỚI)** Đường cấp cứu file bị mount cắt cụt | ~60% | Cơ chế `_parts`/`FORCE_CHUNK` có thật (`tl.py`, `tl_boot.py`, `tl_selftest.py`) và `tl_fetch.sh` có thật; nhưng **2 mắt xích LÕI ra lệnh chạy chưa từng được viết** — xem §0.8 tầng A → H0 |

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
| **H1. Khôi phục 2 tham chiếu đứt** | (a) `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` — schema **suy từ mã bên đọc**, không từ prose: gốc `{co_quan, van_ban[], noi_dung[]}`; `van_ban[]` = `so_hieu·ten·ngay·hieu_luc_tu·sua_doi_bo_sung·tinh_trang·loai·linh_vuc·ghi_chu`; `noi_dung[]` = `key·van_ban·can_cu·phan_tich·hinh_thuc·lo_trinh·tieu_chi·linh_vuc·ghi_chu` **+ `anchor` (NEO PHỤ THUỘC — schema §3 WORKFLOW doc, nhập từ đầu vì local KHÔNG có template sẵn, tạo mới không merge) + `muc_chac_chan`**. (b) **ĐÃ CHỐT 25-07 = XOÁ**: bỏ đặc tả `nlm_log.py` khỏi chỉ dẫn SỐNG (`QUY_TRINH_RA_SOAT_3_TANG.md:91` — thay bằng `NHAT_KY_NLM_<sh>.csv` của `rasoat_worksheet.py`); `DOCTRINE_APPENDIX` là lưu trữ nguyên văn, KHÔNG sửa thân; quota NLM đếm trong state | `r2xx_master_template_doc_duoc`: `rasoat_phuluc.py --in <mẫu>` rc=0, sinh đủ 03–07-BN. `r2xx_hinh_thuc_vocab`: mọi giá trị `hinh_thuc` trong mẫu route đúng bucket — **bẫy**: `route()` (`rasoat_phuluc.py:46`) khớp chuỗi cố định ("ban hành mới"→05, "bãi bỏ toàn bộ"→06, "tạm ngưng/ngừng toàn bộ"→07, "nghiên cứu"/"mục f"/`chờ…`→F), sai chính tả = **âm thầm** rơi hết vào 04 |
| **H1b. Ba trường bảng C — ĐÃ CHỐT 25-07: cấu trúc hoá 2, tính toán 1, sửa code tối thiểu** | (1) *Nguyên văn-cite* = `anchor.cite` (không đặt trường trùng thứ hai); (2) *mức chắc chắn* = trường mới **`muc_chac_chan`** enum có kiểm soát `chac_chan \| can_kiem_tra \| cho_verify_nlm` (Loop C đọc máy: TTL chỉ áp mức `can_kiem_tra`; `cho_verify_nlm` = ghi khi rà chế độ không-NLM, chờ trả nợ kiểm chéo); (3) *định tuyến phụ lục* KHÔNG thêm trường — là hàm của `hinh_thuc` (2 nguồn sự thật sẽ lệch). **Sửa `rasoat_phuluc.py` tối thiểu**: xuất phụ lục nối `muc_chac_chan` + `anchor.cite` vào cột ghi chú (vài dòng, nằm trong bump duy nhất Đợt 1) | `r2xx_bang_c_du_truong`: mỗi phát hiện trong mẫu truy lại được nguyên văn + mức chắc chắn sau khi qua `rasoat_phuluc.py` (không mất dữ liệu, kể cả trong bản phụ lục xuất ra) |
| **H2. Schema PLAN hồ sơ** | (a) `references/workflows/rasoat_hoso.json` theo **`workflow_card.v1` sẵn có** (`plan[]`, `verify[]`, `stop_conditions[]`, `idempotency_contract`, `journal_key`, `resume_behavior`, `resume_command`, `write_scope`, `risk`) — không đặt schema mới cho phần tĩnh; (b) `references/RASOAT_PLAN_SCHEMA.md` chỉ đặc tả phần **biến động** (`rasoat_plan.v1`: trạng thái/hàng đợi/bàn giao/quota/`session_claim`) + 1 JSON mẫu | `r2xx_the_rasoat_hoso_hop_le`: `workflow-audit --strict --json` ok=true với thẻ mới; thêm vào `_RELEASE_REQUIRED_WORKFLOWS` + golden 0-diff. Phần biến động: Claude sinh được PLAN từ hồ sơ mẫu bằng tay theo schema, không cần code mới |
| **H9. (MỚI, đã đổi thiết kế theo §0.8) Guard tham chiếu đứt dạng RATCHET** | `_skill_links_findings` (`release.py:527`) chỉ đọc `SKILL.md`, chỉ khớp `references/…`. Thay bằng helper thuần mới quét cả `references/*.md` và khớp `templates/…`+`scripts/…`, kèm **2 thứ bắt buộc**: (a) **phân hạng tài liệu** — fail-closed cho tài liệu SỐNG, advisory cho LƯU TRỮ (`DOCTRINE_APPENDIX.md`); (b) **allow-list baseline** chốt 66 mục tầng C. **ĐÃ CHỐT 25-07 — nơi lưu baseline: hằng số Python (frozenset) NGAY TRONG `release.py`** cạnh helper, khớp theo **cặp `(tài_liệu, con_trỏ)`** (miễn trừ trong DOCTRINE không tự động miễn trừ ở SKILL.md) + hằng phân hạng LƯU TRỮ; KHÔNG tạo file package mới (H9 không đụng manifest — chỉ H1 phải đụng). Ratchet đúng nghĩa: sửa baseline = sửa code = qua ruff→selftest→CHANGELOG→review | `r208_pointer_findings_pure`: hàm thuần — bắt `templates/`+`scripts/`, tước dấu câu/backtick, thư mục khớp prefix, manifest rỗng = fail-closed. `r208_baseline_ratchet`: con trỏ trong baseline → im; con trỏ MỚI không có trong package → ĐỎ ngay. `r208_cay_that_tang_A_B`: trên cây thật, tập fail-closed **đúng bằng** 5 mục tầng A+B trước khi sửa, **rỗng** sau H0+H1 |
| **H0. (MỚI — §0.8 tầng A) Vá lỗ hổng đường cấp cứu của LÕI** | SKILL.md ra lệnh chạy `scripts/build_parts.py` / `scripts/tl_rebuild.sh` — cả hai chưa từng tồn tại. **ĐÃ CHỐT 25-07 = hướng (ii) SỬA LÕI**: bỏ hai con trỏ khỏi SKILL.md:133–138 + `COWORK_EDIT_SAFETY.md`, trỏ về đường cứu hộ có thật (`tl_fetch.sh`, `tl_boot.py`, `tl verify-integrity`); cơ chế `_parts/` đã bỏ (`tl_boot.py:4`). ⚠ SKILL.md chỉ còn ~39B headroom dưới trần 48KB — bản sửa PHẢI giảm byte (bản nháp phiên remote giảm 42B, làm lại tay, giữ nguyên line ending) | `r208_skill_md_khong_tro_file_ma`: mọi con trỏ `scripts/…` trong SKILL.md nằm trong package-set. Nếu chọn (i): thêm test `ghép == gốc` cho `build_parts.py --verify` |

*Vì sao H9 nằm ở Đợt 1:* nó là cái duy nhất bảo đảm Đợt 1 không tự tạo thêm tham chiếu đứt mới. Làm sau = làm lại.
*Vì sao H0 chen lên trước:* nó không thuộc phạm vi rà hồ sơ, nhưng H9 sẽ phơi nó ra và LÕI không thể ở trạng thái
"chỉ dẫn cấp cứu trỏ vào hư không". Đây là lỗi nặng hơn cả 2 tham chiếu đứt mà bản đầu tìm ra.

> **Hai quyết định — NGƯỜI ĐÃ CHỐT 25-07 (không hỏi lại):**
> **(Q1)** H0 = **(ii) SỬA LÕI** — trỏ về đường có thật, không viết công cụ mới.
> **(Q2)** H1(b) = **XOÁ đặc tả** `nlm_log.py` khỏi chỉ dẫn sống; quota NLM đếm trong state file.
> Cả hai đều là hướng "sửa tài liệu" — phần code còn lại của Đợt 1: helper H9 trong `release.py` + mở rộng
> tối thiểu `rasoat_phuluc.py` (H1b), chung MỘT bump.

### Đợt 2 — Lớp điều phối ✅ **ĐÃ THI HÀNH 26-07** — nhánh `claude/r210-rasoat-dot2` (`d82ef70`), **v1.35.46 (r210)**, selftest **1316/1316**, release-verify gói 188 file XANH. Sản phẩm: `references/RASOAT_HOSO_LOOP.md` (H3) + prompt agent `tl-rasoat` §6 & wrapper dev ép cứng frontmatter (H4) + 2 wrapper `.claude/`. Kèm dọn `2.21.2m` khỏi SKILL.md (2 chỉ dẫn sai version).

| Hạng mục | Sản phẩm | Nghiệm thu (mã test) |
|---|---|---|
| **H3. Vòng lặp rà hồ sơ (BỌC, không xây mới — §0.1)** | `references/RASOAT_HOSO_LOOP.md`: worklist đọc PLAN → spawn → ghi 1 file `.json`/đơn vị → cập nhật PLAN → HỘI TỤ → chốt checkpoint. **Gọi `rasoat-loop`/`frontier-expand` làm lớp phát hiện**; PLAN chỉ thêm cái chúng không có: trạng thái theo đơn vị + lưu bền + `session_claim`. Dùng nguyên từ vựng `dry_rounds`/`max_iter`/PAUSE (§B.6). + wrapper dev `.claude/commands/rasoat-hoso.md` + 1 dòng vocab `SKILL.md` | `r2xx_loop_hoi_tu_dung_thu_tu`: chạy khô trên PLAN mẫu — đúng thứ tự, dừng đúng khi `dry_rounds` đạt K, PLAN cập nhật sau MỖI đơn vị (không dồn cuối). `r2xx_loop_khong_ghi_trong_cay`: sau lượt chạy khô, `git status` sạch và `release-verify` vẫn ok (kiểm §B.5) |
| **H4. Agent rà đơn vị** | prompt mẫu `tl-rasoat` trong `references/RASOAT_HOSO_LOOP.md` (read-only, quota NLM trong prompt, output JSON schema H1) + wrapper dev `.claude/agents/tl-rasoat.md` (cùng khung ranh giới cứng như `tl-auditor`) | `r2xx_agent_output_dung_schema`: agent rà 1 đơn vị thật, JSON hợp lệ schema H1, **không ghi file nào** (kiểm bằng `git status` + mtime cây skill); phát hiện đối chiếu được với rà tay |

### Đợt 3 — Tự trị hoá

| Hạng mục | Sản phẩm | Nghiệm thu (mã test) |
|---|---|---|
| **H5. Degrade-and-continue + bug ledger** | mục mới trong `QUY_TRINH_RA_SOAT_3_TANG.md`: phân loại lỗi (workaround/blocker), format `BUGS_FOUND.md`, quy tắc "sửa nóng CHỈ khi chặn đứng; còn lại gom vá sau lượt rà" | `r2xx_degrade_khong_dung_vong`: bơm 1 lỗi giả lập giữa vòng rà → vòng lặp ghi ledger và chạy tiếp, PLAN vẫn tiến |
| **H6. Kickoff contract + tiền kiểm** | mẫu giao việc trong `RASOAT_HOSO_LOOP.md` (phạm vi, uỷ quyền nạp văn-bản-thuộc-hồ-sơ, ngân sách NLM, chính sách lỗi, **+ chốt 25-07: uỷ quyền nguồn tải** — danh sách domain tin cậy tự tải + kênh TVPL-VIP `tl tvpl-url` qua Chrome đăng-nhập-sẵn + ngưỡng `quota_tvpl` — xem WORKFLOW §4 B.1 bậc thang TVPL) + **mở rộng PHA 0 đã có** (`QUY_TRINH:30`) thêm doctor/precheck/tuổi cookie — fail → dừng TRƯỚC khi rà | `r2xx_pha0_cookie_gia_dung_som`: cookie giả >14 ngày → dừng ở Pha 0 với thông báo 1 dòng, chưa tiêu 1 call NLM nào |

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

`H9 → H0 → H1/H1b → H2 → H3 → H4 → H5/H6 → H7 → H8`. H9 trước tiên để guard bắt được trạng thái "trước khi sửa"
làm bằng chứng (test 2 chiều, đúng bài học đắt giá trong CLAUDE.md). H0 ngay sau vì nó là mục nặng nhất mà H9
phơi ra và nằm trong LÕI. H2 sau H1 vì PLAN trỏ tới schema master.

**Đợt 1 ĐÃ THI HÀNH 26-07** — nhánh `claude/r209-rasoat-dot1`, commit `245cd4d`, **v1.35.45 (r209)**, nền
`c2ea090` (v1.35.44 — r208b/c/d đã chiếm 1.35.42–44 nên bump là 45, không phải 44 như dự kiến cũ). Trọn
H9→H0→H1/H1b→H2 + ADR-0016, selftest **1311/1311** (+7 `r209_*`), workflow/determinism/golden strict XANH,
`release-verify --archive` XANH trên gói 187 file (guard mới: `doc_pointers ok=true`, baseline đúng 10,
advisory 64). Golden regen CÓ CHỦ ĐÍCH 2 fixture (thẻ mới xuất hiện trong output). **Chờ user: merge +
deploy tay** (upload-skill-to-Package.cmd + re-import Capabilities vì SKILL.md đổi).

## F. RỦI RO & GIẢM THIỂU

| Rủi ro | Giảm thiểu |
|---|---|
| Cookie NLM chết giữa vòng rà (Cowork/chat không tự refresh) | **Phòng thủ 3 tầng (chốt 25-07, chi tiết WORKFLOW §4b):** (1) H6 tiền kiểm tuổi cookie + cron `secrets-set --nlm` phía local; (2) local: tự chạy `nlm login`/`refresh_auth` MỘT lần khi gặp lỗi xác thực; (3) chế độ **chạy-không-NLM**: T2 quét cache/Drive trực tiếp, phát hiện đánh `muc_chac_chan="cho_verify_nlm"` vào Q-VERIFY, cookie sống lại thì trả nợ kiểm chéo. Mất NLM = mất tiện, không mất đúng (nguyên văn vốn CHỈ từ cache/raw) |
| Lỗi skill chặn đứng ở LIVE (deploy là bước tay) | H5 degrade-and-continue; tần suất giảm dần theo mỗi fix khoá test `rXX_` |
| Hai phiên cùng cầm quyền ghi (vi phạm single-writer) | quy ước trong H3: nhận vai = ghi `session_claim` vào PLAN; registry đã có LockService+RMW làm lưới dưới |
| LIVE drift (kết luận lỗi đo trên bản trễ) | mọi báo lỗi skill trong `BUGS_FOUND.md` ghi rõ VERSION đo được (CONTEXT.md — LIVE vs canonical). **Bản kế hoạch này là ví dụ sống:** §0 tồn tại vì bản đầu đo trên v1.35.32 |
| Agent con vượt quota NLM | quota ghi trong prompt + phiên chính đối chiếu sau mỗi đơn vị. ⚠ **SỬA (§0.3):** cơ chế cũ ghi là "bắt buộc `nlm_log.py add`" — script đó **không tồn tại**. Cho tới khi H1(b) chốt, đếm quota bằng số lần gọi ghi trong PLAN (`quota_con_lai`), không dựa vào `nlm_log` |
| **(MỚI)** State biến động lọt cây skill → `package_hash` lệch, `release-verify`/golden ĐỎ | §B.5: PLAN/master ra ngoài cây (`~/.tra_luat_cache/rasoat/<ho_so_id>/`); test `r2xx_loop_khong_ghi_trong_cay` khoá lại |
| **(MỚI)** Thêm file mẫu mà quên regen `RELEASE_MANIFEST` → gói FAIL ở LIVE | §E: quy tắc 3 bước (a/b/c); tiền lệ đã ghi trong `release.py:334` (115≠109) |
| **(MỚI)** Guard H9 bật fail-closed toàn bộ → 75 mục đỏ → bị vô hiệu hoá cho xong | §0.8: bắt buộc có allow-list baseline + phân hạng tài liệu sống/lưu trữ. Guard chỉ chặn con trỏ MỚI; nợ cũ nằm trong baseline, gỡ dần |
| **(MỚI)** Chỉ dẫn cấp cứu của LÕI trỏ vào file không tồn tại, phát tác đúng lúc sự cố mount cắt file | H0. Trước khi H0 xong: khi gặp file cắt cụt, dùng `tl_fetch.sh` + `tl_boot.py` (có thật), **bỏ qua** bước `build_parts`/`tl_rebuild` trong SKILL.md:133–138 |
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
