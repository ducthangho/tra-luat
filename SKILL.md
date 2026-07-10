---
name: tra-luat
description: >-
  Lấy và tra cứu chính xác từng câu chữ văn bản pháp luật và văn bản của Đảng. Dùng khi
  cần: tra nguyên văn Điều/Khoản/Điểm/Mục (đúng từng chữ, không tóm tắt); lấy toàn văn từ
  AI Tra Cứu Luật (MCP), vbpl.vn, Công báo, cổng .gov.vn/.chinhphu.vn, dangcongsan.vn, Thư
  viện Pháp luật, luatvietnam.vn, NotebookLM, hoặc file tải lên (docx/doc/pdf/html/txt);
  bóc tách cấu trúc kiểu Điều (Hiến pháp, Luật, Bộ luật, Nghị định, Thông tư, Nghị quyết)
  và kiểu Mục (văn kiện, Nghị quyết/Kết luận/Chỉ thị của Đảng); chuẩn hóa JSON; sắp xếp tự
  động theo 45 chủ đề pháp điển (đặt tên chuẩn, move folder, registry/manifest — lệnh
  sapxep); đẩy Google Drive rồi nạp NotebookLM. Kích hoạt khi nói "tra Điều X của Luật Y",
  "lấy nguyên văn Mục II Nghị quyết Z", "cho tôi toàn văn Điều...", "lấy văn bản này về",
  "sắp xếp file này", "bóc tách văn kiện Đảng". Trả lời điều khoản nguyên văn từ nguồn đã
  xác minh, KHÔNG dùng RAG để sinh. Thao tác Drive qua Apps Script webapp, KHÔNG dùng
  Drive MCP.
---


# tra-luat — LÕI VẬN HÀNH (v1.34.24 — KERNEL)
> Kernel = bất biến + cổng + con trỏ. Chi tiết sống ở `references/` (danh mục cuối file).


> Đây là LÕI MỆNH LỆNH. Ba tài liệu vận hành (đọc khi cần, KHÔNG nạp toàn bộ vào context):
> - **`references/API_CONTRACT.md`** — tham số + khóa response MỌI action webapp (target `2.21.2j`). **Tra trước khi gọi action — KHÔNG đoán tham số.**
> - **`references/RUNBOOK.md`** — trình tự khởi động + cổng vận hành (đánh số, tất định).
> - **`references/DOCTRINE_APPENDIX.md`** — lịch sử + biện luận đầy đủ (changelog v1.x→v1.15.7). Tra khi cần BỐI CẢNH/lý do.
>
> Khi mâu thuẫn: LÕI + API_CONTRACT + RUNBOOK **thắng** phụ lục.


## DETERMINISTIC WORKFLOW GATES — tool inventory / route-task / dry-run / readback

Trước khi Claude viết script, hàm, tool, loop hoặc đoạn xử lý tự chế, PHẢI kiểm kho công cụ hiện có:

1. `python scripts/tl.py tool-inventory --json` để xem nhóm tool/script/workflow.
2. `python scripts/tl.py route-task --task <tac_vu> --json` với tác vụ rủi ro: `write_new_tool`, `nlm_query_quality`, `ingest_local`, `convert_rename`, `ingest_zip`, `ocr_pdf_scan`, `large_doc_chunk`.
3. `python scripts/tl.py -h` và `python scripts/tl.py <lệnh> --help` với nhóm lệnh liên quan.
4. Kiểm `scripts/*.py` và `references/API_CONTRACT.md` trước khi gọi webapp/Drive/registry/NLM hoặc thêm tool mới.
5. Khi sửa skill/workflow/release gate, chạy deterministic mode: `python scripts/tl.py --deterministic workflow-audit --strict --json`, `python scripts/tl.py --deterministic determinism-audit --strict --json`, và trước khi đóng gói `python scripts/tl.py --deterministic release-check --strict-determinism --full --json`.

PHÁT HÀNH & NHÁNH (ADR-0001, chốt grilling 2026-07-09): CHỈ canonical (D:\Quốc hội	ra-luat / github ducthangho/tra-luat) được tăng VERSION + drive-push. Phiên/nhánh song song giao nộp bằng `tl bundle-export --note "<mục đích>" --json` (zip GIỮ VERSION fork-point + BUNDLE_META.json) — KHÔNG tự đánh version, KHÔNG publish; drive-push tự TỪ CHỐI cây có BUNDLE_META.json (BLOCKED_BY_BUNDLE_META). Deploy policy: canonical qua đủ gate ⇒ deploy CÙNG NGÀY + verify tải lại VERSION; SKILL.md đổi ⇒ user re-import Capabilities.

Chỉ viết tool mới khi đã chứng minh lệnh/script/hàm hiện có không đáp ứng. Tool mới phải có input/output rõ, ưu tiên JSON, có dry-run nếu ghi dữ liệu, có verify/readback, và có selftest/audit phù hợp.

Mọi quy trình nạp/convert/rename/OCR/zip/chunk phải đi theo mẫu:

`route-task → dry-run plan → apply có chủ đích → verify/readback → commit/report`

`tool-inventory`, `route-task`, `workflow-audit`, `determinism-audit` và `golden-test` là READ-ONLY mặc định, không gọi Drive/NLM nặng và không ghi dữ liệu. Workflow chi tiết đặt tại `references/workflows/*.json`; schema ở `references/workflows/workflow_card.schema.json`; fixtures ổn định ở `references/golden/*.json`. SKILL.md chỉ giữ nguyên tắc lõi để tránh drift.

Từ v1.33.55, helper deterministic/json output tách sang `scripts/tl_core/deterministic.py` + `scripts/tl_core/jsonio.py`; `scripts/tl.py` vẫn là entrypoint public duy nhất (wrapper tương thích ngược — KHÔNG gọi tl_core trực tiếp từ ngoài). Từ v1.33.56 (Pha C), thêm `tl_core/workflow.py` (tool-inventory/route-task/cards/golden), `tl_core/release.py` (release-*/determinism-audit), `tl_core/live.py` (live-*/deploy/rollback/final-acceptance) — vẫn CHỈ gọi qua `scripts/tl.py`. Từ v1.33.57 (Pha D): thêm `tl_core/zip_ingest.py`, `tl_core/ocr.py`, `tl_core/chunking.py`. Từ v1.33.58 (Pha E): `tl_core/command_registry.py` — metadata lệnh (risk/gates/card/contract); `workflow-audit` tự đối chiếu registry↔parser↔cards; 8 lệnh determinism sinh parser từ spec.

Stage an toàn hiện có thêm các lệnh local deterministic: `ocr-run` tạo sidecar text/OCR local khi engine có sẵn; `chunk-apply` tạo chunk files + manifest; `chunk-verify` kiểm manifest/files. Các lệnh này chưa ghi Drive/NLM. Muốn đưa kết quả vào corpus vẫn phải quay về pipeline ingest/verify/readback.


## 0. NGUYÊN TẮC BẤT BIẾN
1. **VBHN-first + LATEST-VBHN** — có VBHN còn hiệu lực → dùng VBHN, không bản gốc/sửa đổi rời. **Khi TRA/TÌM Luật theo tên:** thử keyword **'<tên> hợp nhất' TRƯỚC** (vd "Luật PPP hợp nhất") → rồi **'<tên> mới nhất'** → cuối cùng tên gốc; truy vấn theo SỐ HIỆU thì tìm thẳng. **MỌI tìm-văn-bản-trên-web dùng GOOGLE `site:` (VBHN-first), KHÔNG dùng search nội bộ TVPL/LVN (kém)** — áp cho `fetch-route`/`fetch-links`/`find-doc` VÀ QT-5 (`vbhn-check`/`status`/`relation-check` đều xuất `google_discovery`). **⚠ S9/S11 (log 🔴 2026-07-01): KHÔNG chốt ở VBHN ĐẦU TIÊN tìm thấy — số hiệu VBHN TĂNG theo mỗi lần hợp nhất (Bộ luật Hình sự: 01/VBHN 2017 → 11/VBHN → 135/VBHN 2025; KHÔNG phải semver).** Bắt buộc LƯỢT-2: tìm SỐ VBHN LỚN HƠN / NGÀY MỚI HƠN cùng cơ quan (VPQH) qua `'<tên> hợp nhất mới nhất <năm>'` + `site:congbao.chinhphu.vn`. Ứng viên VBHN chưa xác minh là mới nhất → cờ `VBHN_CANDIDATE_UNVERIFIED_LATEST`; NGOẠI LỆ v1.33.15: VBHN duy nhất RẤT MỚI (năm ≥ năm-nay−1) + không luật-sửa nào mới hơn đã biết + không thuộc nhóm S10 → hạ thành cờ INFO `VBHN_LATEST_RECENT_COVERED` (rời hàng web lượt-2; vẫn `vbhn-verify --official-required` trước khi trích dẫn). **S10:** luật cải cách cao 2024-2026 (Hình sự/tố tụng/phí-lệ-phí/đất đai/doanh nghiệp/đầu tư/đấu thầu/thuế…) → cờ `VBHN_HIGH_AMENDMENT_VELOCITY`, PHẢI kiểm bản hợp nhất mới nhất trước khi trả.
2. **Verify nguyên văn** — điều khoản trả ra lấy từ cache/raw đã xác minh; NLM chỉ định vị + tổng hợp; KHÔNG nhận RAG làm nguyên văn.
3. **Official-first cho VBHN** — thiếu VBHN chính thức thì HỎI người dùng nạp vào `_HOP_NAP` hoặc lấy nguồn chính thức; KHÔNG tự ghép bản hợp nhất làm bản dùng. Bản tự ghép/chắp nội dung chỉ là bản tạm để so sánh, phải gắn provisional và quarantine khi có bản chính thức.
4. **Không bịa** — thiếu dữ liệu → nói "không có" / REVIEW.
5. **Dedup nhiều lớp** — cache → registry → NLM (số hiệu + biến thể + text_hash).
6. **ĐỐI CHIẾU NGAY** — phát hiện văn bản đã bị sửa đổi/lỗi thời/VBHN thiếu → DỪNG rà bản cũ, chạy `tl relation-check` + `tl vbhn-check`, hỏi người dùng nạp/ghi registry ngay. KHÔNG gác vào Mục F.
7. **Tên NLM = tên Drive** — đổi tên thì đổi đồng bộ GDoc + file gốc + registry + nlm_title + source NLM.
8. **External ingest gate** — `research_start/research_status` chỉ để phát hiện URL. CẤM dùng `research_import`/`source_add(url)` nạp thẳng VBQPPL vào NLM. Mọi nguồn mới phải đi Drive → convert → tên chuẩn → folder đúng → verify → `nlm_push` vào notebook đang dùng, sau khi người dùng duyệt đích/định dạng/tên.
9. **Corpus profile** — luôn đọc config VBQPPL trước để lấy webapp/token, rồi overlay `TL_PROFILE`/`--profile`. Văn bản thường dùng profile riêng (`vbthuong`: folder/notebook/registry/manifest riêng), KHÔNG mặc định VBQPPL. **Cách B (v1.19):** `--profile P` tự forward `registryDocId`/`manifestId` vào mọi call webapp → registry/manifest RIÊNG; nêu rõ profile ở đầu yêu cầu (xem RUNBOOK §D). **★ v1.30.0 — profile chạy CÙNG VBQPPL, KHÔNG thay thế:** profile dự án mặc định `TL_BASE_ALSO=1` → lệnh ĐỌC (`locate`/`reg-query`/`source-map`/`exists`/`nlm-cross`) quét `{scope profile} ∪ {VBQPPL nền + shards}`, **hit profile ưu tiên**, hit nền đánh dấu `scope=vbqppl`/cờ `BASE_SCOPE_HIT`; opt-out `profiles.<p>.baseAlso=false` hoặc `--no-base-also`. Đường GHI/ingest KHÔNG đổi scope (vẫn profile riêng — không đẩy nhầm đích). **BẤT BIẾN LAYOUT:** registry + manifest của profile phải nằm TRONG thư mục profile (root hoặc `_meta`) — kiểm `tl profile-doctor` (`--fix --apply` move về `_meta`, fileId GIỮ NGUYÊN). **★ v1.34.22-24 (ADR-0003) — MARKER là nguồn sự thật:** mỗi profile có `_meta/tra_luat_profile.json` = nguồn sự thật về TỒN TẠI + ĐỊNH DANH + metadata mô tả (description/style/relations); config local = LỰA CHỌN runtime (defaultProfile/token/webapp) + cache dựng lại được; `_PROFILES_INDEX` = chỉ mục đọc nhanh. Đồng bộ MỘT CHIỀU marker→config: `tl profile-sync` (`--apply` ghi config; KHÔNG bao giờ ghi marker); profile cũ thiếu marker → `tl profile-backfill-markers --apply`; ghi marker CHỈ qua lệnh tl (create/adopt/backfill — journaled + readback, CẤM sửa tay). Khám phá marker-first: `tl profile-list --discover` (configured/adoptable/broken_marker/orphaned); seed hạ tầng sẵn: `tl profile-adopt`; sổ cái: `tl profile-index`. Dùng profile trong PHIÊN: `tl profile-load <p> [--target session|project]` — Instruction Block thống nhất mọi env, KHÔNG ghi config (đổi mặc định máy: `profile-use --apply`).
10. **Link tải ≠ canonical (2 trục)** — **TẢI FILE** ưu tiên theo ĐỊNH DẠNG **docx > doc > pdf** ⇒ nguồn
**TVPL/LuatVietnam (docx) trước → vbpl.vn (doc) → Công báo (pdf)**
(docx tốt nhất để convert GDoc verbatim, giữ bảng). **CANONICAL + HIỆU-LỰC** vẫn **official-first**
(vbpl/Công báo) để xác minh bản đúng. Trang luật VN chặn HTTP server-side (TVPL 403, vbpl 404) → **bắt buộc
trình duyệt thật (Claude in Chrome)**, KHÔNG xoay proxy/giả UA. **DISCOVERY: dùng GOOGLE `site:` (WebSearch)
để tìm đúng trang văn bản — tốt hơn HẲN search nội bộ TVPL/LVN** (`site:thuvienphapluat.vn <tên> hợp nhất`).
Hàm: `tl fetch-links` (MANUAL: link Google site: cho người dùng bấm/login/tải), `tl fetch-route`/`fetch-batch`
(AUTO: Claude resolve qua WebSearch→trang văn bản→tải, throttle, dedup số-hiệu→SKIP/tên→REVIEW).
   - **10a. PDF là PHƯƠNG ÁN CUỐI (luật cứng — đặc tả 26/6).** Khi nguồn official chỉ có PDF, **KHÔNG được lùi thẳng về PDF**: PHẢI thử .docx ở **thuvienphapluat.vn + luatvietnam.vn** trước (thang `docx official → docx TVPL/LVN → doc → pdf official`). "Official-first" chỉ áp cho **canonical/hiệu-lực**, KHÔNG phải cớ bỏ qua bước thử docx ở TVPL/LVN. Chỉ dùng PDF khi **đã cạn mọi ngả docx/doc** + nêu rõ lý do; nạp xong **kiểm chất lượng text** (`source_get_content` ≥ ngưỡng ký tự, không rỗng/scan), nghi scan → xin .docx qua nhánh dưới. *(Sự cố XNC 62/VBHN-VPQH: đã lùi PDF mà chưa thử TVPL/LVN — không lặp lại.)*
   - **10b. Login-gate theo MÔI TRƯỜNG (RUNTIME_ENV ∈ {code, cowork, chat}; không chắc → `chat`).** Nguồn trong `FETCH_GATED_BLOCKLIST_` (TVPL/LVN) webapp KHÔNG auto-fetch được:
     - **code/cowork:** HỎI "Bạn có muốn tôi tự động tải các file này về không?" (kèm danh sách file+nguồn) trước; đồng ý → tải bằng cơ chế sẵn có (Claude in Chrome đã login) → `_HOP_NAP`; muốn tự làm → nhánh chat.
     - **chat (hoặc người dùng tự làm):** ĐƯA **LINK BẤM-ĐƯỢC** (markdown `[nhãn](url)`) — **TUYỆT ĐỐI không URL trần / không bắt copy-paste**: mỗi nguồn gated 1 link tải xuống + 1 link mở `_HOP_NAP` (`drive.google.com/drive/folders/1bNSAKGACtk0x0cqX5QRVEGT12udi2g67`). Người dùng báo tải lên xong → tiếp `tl ingest-local`.
     - Tiện ích chuẩn hoá: **`tl fetch-links --sohieu … [--env code|cowork|chat]`** xuất sẵn bộ link tải-xuống (C4) + link `_HOP_NAP`; mặc định auto-detect env, không chắc→chat (an toàn = chỉ đưa link, không tự tải).
     - **★ HOẶC — UPLOAD TRỰC TIẾP file vào môi trường Claude (đường gọn, đỡ phải tự mở _HOP_NAP):** người dùng đính/kéo-thả file raw (**.docx ưu tiên; .doc/.pdf cũng nhận**) vào phiên → Claude chạy **`tl ingest-local <đường-dẫn-local> --name … --sohieu … --cat NN --apply`**: tự **convert (Drive `organize convert=true`, SERVER-SIDE — KHÔNG cần libreoffice local) → rename chuẩn → upload Drive đúng folder chủ đề → organize/stamp/register → `nlm source add`** trong 1 lệnh. DRY mặc định (xem kế hoạch) → `--apply` mới chạy. (.pdf = HẠ SÁCH: convert ~OCR dễ lệch → verify nguyên văn sau; ưu tiên .docx official.)
11. **Slot theo notebook** — khi tính `nlm_slots/nlm_preflight`, chỉ đếm rows có `nlm_notebook_id == notebook đích`; dòng RỖNG quy về notebook nền (VBQPPL) nên VBQPPL vẫn đếm đúng, notebook dự án hết `NOTEBOOK_FULL` giả. Dòng registry phải có `row_kind=own|ref|overflow`; `ref` không làm đầy notebook trừ khi `countRefs=true`, `overflow` vẫn là VBQPPL host trong profile. Trước khi thêm nguồn, lấy số vật lý qua **`tl nlm-get <nb>`** (CLI `nlm notebook get`, thay MCP `notebook_get`); registry slot chỉ là estimate/dedup. Đẩy nguồn phải `map_set notebookId=…`. Đối chiếu registry: `tl slot-audit`.
12. **`categories=inherit` không sở hữu cây VBQPPL** — chỉ dùng chung category để ORGANIZE/tra cứu fallback; KHÔNG dùng để populate registry/manifest của profile. Registry/manifest profile chỉ gồm dòng `own` + `ref` (+ `overflow` khi profile host VBQPPL).
13. **Cat = 45 chủ đề pháp điển CHÍNH THỨC** (Pháp lệnh pháp điển 2012 + QĐ 843/QĐ-TTg) — mã `01`–`45`, tra
`references/phap_dien_45.json` (`tl cat-list`). Mã `00` Văn bản của Đảng + `46` Luật sửa nhiều luật là rổ
PHI-pháp-điển tự thêm. **KHÔNG đoán cat**
(vd tố tụng=**37** không phải 09; xuất nhập cảnh người NN=**01 An ninh quốc gia** không phải 23; Dân tộc=10).
`ingest-local` validate cat ∈ 45; hợp lệ mà thiếu folder → tự `mkdir` đúng tên; ngoài 45 → REVIEW_CAT (chặn).
Upload phải `convert=false` (nếu không `upload` tự convert→GDoc rồi organize tạo GDoc thứ 2 ⇒ TRÙNG).
QUARANTINE = corpus:false (cách ly). **Quyết định 26/6 (giữ tới khi Bộ Tư pháp công bố đề mục):** luật
**AI/Trí tuệ nhân tạo, Chuyển đổi số, Công nghiệp công nghệ số** (134/2025, 148/2025, 71/2025, các NĐ AI…)
**TẠM giữ cat 19 (KHCN)** — pháp điển CHƯA có đề mục riêng → KHÔNG tự chuyển 03/tạo rổ mới/flag là misfile.
(Dữ liệu/CSDL/CNTT/GDĐT thì ĐÃ về 03 vì đề mục CNTT = chủ đề 3, đã xác minh phapdien.)
14. **DÙNG LỆNH CÓ SẴN — đừng viết snippet `json.load(manifest)`/`g.get("move")` tay** (bài học 26/6: nhiều thao tác ad-hoc trùng lệnh sẵn có). Tra/lọc registry → **`tl reg-query`**; tìm trùng + kế hoạch quarantine → **`tl hygiene scan/plan/apply`** (đã subject-aware: KHÔNG gộp khác-cơ-quan/phụ-lục); rà sai chủ đề → **`tl cat-audit`** → sửa bằng **`tl recat … --cat NN [--apply]`** (hoặc `--quarantine`); đếm/đối soát NLM → `tl nlm-get/-list/-reconcile/-cross`; check trùng 1 văn bản → `tl dedup-check`. Chỉ viết Python tay khi KHÔNG lệnh nào phủ.
15. **SCRIPT-REUSE GATE — KIỂM KHO TRƯỚC KHI VIẾT MỚI (bắt buộc; mở rộng #14).** Trước khi viết BẤT KỲ script/hàm/loop mới, PHẢI kiểm kho sẵn có theo 3 bước: (a) **subcommand** — `tl -h` / `tl <lệnh> --help`; (b) **script + mục đích** — liệt kê `scripts/*.py` kèm docstring dòng đầu (§7 BẢN ĐỒ SCRIPT là mục lục); (c) **hàm nghiệp vụ** — `grep -nE "def .*<từ khoá>" scripts/tl.py scripts/common.py`. CHỈ viết mới khi KHÔNG lệnh/script/hàm nào phủ chức năng. Có sẵn thì DÙNG bản của skill (đã xử ca biên + có journal/undo), KHÔNG hand-roll — vd: bóc **TRÍCH YẾU** = `tl backfill-title-vn` (`_title_block_from_text`/`_title_vn_from_header`, đã xử BỘ-LUẬT-trước-LUẬT + trích yếu đa dòng); lọc registry = `tl reg-query`; dedup = `tl dedup-plan`/`hygiene`; chuẩn tên = `standardize_name.py`/`tl source-rename`; đọc toàn văn = `tl extract`. **Bài học 2026-07-06:** suýt viết lại loop bóc trích yếu tay trong khi `tl backfill-title-vn` đã có và tốt hơn. **Enforcement:** bước kiểm-kho là TIỀN-ĐIỀU-KIỆN của mọi việc viết/loop; SỬA hoặc THÊM file skill CHỈ qua `tl edit-skill` (DRY + py_compile/assert) rồi `tl verify-integrity` — KHÔNG Edit/Write native (mount Cowork cắt cụt). Instruction/loop phải khai khối `SCRIPT_REUSE_GATE` (bổ sung vào `tl instruction-audit`/selftest).


## 1. KHỞI ĐỘNG (bắt buộc, đúng thứ tự — chi tiết: RUNBOOK §A)
> ## ★★ BƯỚC 0 — CHỌN ĐÚNG 1 ĐƯỜNG THEO MÔI TRƯỜNG (ĐỪNG TRỘN, ĐỪNG ĐỤNG `_parts` SỚM) ★★
> - **COWORK: mount LUÔN cắt cụt file — KỂ CẢ `scripts/tl_fetch.sh`, `tl_boot.py`, `_parts`. ĐÂY LÀ SỰ THẬT ĐÃ BIẾT —
>   ĐỪNG inspect/confirm/điều tra truncation, ĐỪNG chạy file mount nào. LỆNH ĐẦU TIÊN = DÁN NGUYÊN KHỐI dưới, chạy NGAY
>   (chỉ cần `curl`+`unzip`, KHÔNG phụ thuộc bất kỳ file mount nào còn nguyên vẹn):**
>   ```sh
>   D=$HOME/.tl_fetch; mkdir -p "$D"
>   curl -fsSL "https://drive.usercontent.google.com/download?id=1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P&export=download&confirm=t" -o "$D/skill.zip"
>   rm -rf "$D/live"; mkdir -p "$D/live"; unzip -oq "$D/skill.zip" -d "$D/live"
>   R=$(dirname "$(dirname "$(find "$D/live" -path '*/scripts/tl.py' | head -1)")"); echo "$R" >"$D/ROOT"
>   sh "$R/scripts/tl_fetch.sh" --setup        # CORE NHANH: config(curl)+ping+gws+boot — KHÔNG nlm (né timeout 45s Cowork)
>   ```
>   **NLM tách RIÊNG (chỉ khi cần nlm-list/-query/-cross — rà soát đọc cache KHÔNG cần):** chạy SAU, có thể >45s:
>   ```sh
>   cd "$(cat ~/.tl_fetch/ROOT)" && python3 scripts/tl.py nlm-install --uv && python3 scripts/tl.py nlm-auth-load
>   ```
>   **Vì sao khối này, KHÔNG phải `sh scripts/tl_fetch.sh`:** mount cắt cụt CẢ `tl_fetch.sh` → chạy bản mount hay lỗi/cụt.
>   Khối trên tải zip SẠCH (public, chỉ cần curl) rồi chạy `tl_fetch.sh` **bên trong zip sạch** → config(curl)+ping+uv+gws(musl)+
>   boot. **Tách nlm** vì cài nlm (uv+Python+PyPI) hay vượt **45s/lệnh Cowork** → `--setup` (không nlm) xong nhanh, nlm chạy
>   riêng khi cần. Xong: `cd "$(cat ~/.tl_fetch/ROOT)" && TL_CONFIG=~/.tra_luat_config.json python3 scripts/tl.py <args>`.
>   ⛔ **ĐỪNG** `tl_boot.py ping` / `verify-integrity` / `build_parts` / ghép `_parts` / "dig into recovery" — VÔ ÍCH, đã biết
>   mount cắt. Chỉ khi **`curl` zip LỖI** (mất mạng Drive) mới tính nhánh `_parts`/Drive MCP. (A1–A3 dưới là ĐƯỜNG LOCAL.)
> - **LOCAL / mount lành (vd máy Windows) →** chạy thẳng khối **A1–A3** bên dưới. `tl_boot.py ping` ở local KHÔNG đụng `_parts`
>   (on-disk khớp MANIFEST → chạy thẳng; chỉ ghép `_parts` khi thật sự cắt cụt).
>
> **COWORK — chi tiết đường tải-về (mount HAY CẮT CỤT FILE #51435/#53940). ROUTE TỐI ƯU (egress = proxy
> allowlist: `drive.usercontent.google.com` + `script.google.com` MỞ; `google.com`/GitHub/astral CDN CHẶN):**
> **(v1.22.44) MỌI artifact bootstrap nay PUBLIC ở Drive/Package (anyone-with-link) → curl HẾT, KHÔNG cần Drive MCP.**
> | File (Package) | Visibility | Tool nhanh nhất |
> |---|---|---|
> | zip skill | public | **curl** `drive.usercontent` (off-context, không token) — **Cowork TẢI BẮT BUỘC** (mount cắt cụt) |
> | **config (apps script + token)** | **public** | **curl** `drive.usercontent` (LOAD ĐẦU TIÊN; fallback Drive MCP nếu chưa bật public) |
> | gws cred, nlm cred, secrets.enc | public | **curl** / GAS / direct-media |
> | **gws binary (MUSL-static)** | public | **`tl gws-bootstrap-cowork`** (public-curl binary→chmod). ⛔ KHÔNG `npm i -g @googleworkspace/cli` |
> | Python 3.11 | public | **public-curl** binary (`_fast_drive_fetch`); uv chỉ nếu system≥3.11 |
> | nlm CLI | PyPI | **uv** (`nlm-install --uv` → `uv tool install --python 3.11 notebooklm-mcp-cli`; PyPI MỞ) |
> - ⛔ **gws trên Cowork = BINARY MUSL-STATIC tải từ Drive** (chạy mọi glibc). **NPM `@googleworkspace/cli` LÀ BẪY**: bản GNU
>   yêu cầu **GLIBC 2.39**, Cowork (Ubuntu 22, glibc 2.35) → `GLIBC_2.39 not found`, KHÔNG chạy. Luôn `tl gws-bootstrap-cowork`.
> ```sh
> # 1 LỆNH DUY NHẤT — tự curl config(public)+zip+gws+creds, KHÔNG cần Drive MCP:
> sh scripts/tl_fetch.sh --setup --nlm
> #   → curl CONFIG public→$HOME/.tra_luat_config.json (ĐẦU TIÊN) → init-config → ping → gws(direct-media) → boot → nlm(uv)
> #   Nếu curl config trả trang login (CHƯA public) → exit 10, in 2 cách: chạy set-package-public.cmd HOẶC Drive MCP fileId.
> # subsequent (nhanh): cd "$(cat ~/.tl_fetch/ROOT)" && python3 scripts/tl.py <args>
> ```
> `tl_fetch.sh` curl PUBLIC vào **`$HOME/.tl_fetch`** (KHÔNG `/tmp` — sticky bit: file rác owner `nobody` chặn `curl -o`→exit23).
> **Thứ tự (user yêu cầu): CONFIG(apps script) + GWS cred TRƯỚC** → rồi nlm. gws trước nlm để Python tải qua direct-media nhanh.
> Fallback config: webapp `download` (token) → Drive MCP. Bật public 1 lần bằng `set-package-public.cmd` (xem §Đóng gói).
>
> **Còn local (mount lành):** `python scripts/tl_boot.py …` THAY cho `tl.py` — tự strip NUL + verify sha (MANIFEST) +
> ghép từ `_parts` nếu cắt cụt; báo rõ + exit≠0 thay vì im lặng exit 0. tl_boot/build_parts cũng cắt → SHELL
> `sh scripts/tl_rebuild.sh`. Soi mảnh hỏng: `python scripts/build_parts.py --verify`. **`_parts` cũng hỏng → `tl_fetch.sh`
> (Drive) hoặc RE-SYNC skill** là cách dứt điểm.
> **Khi SỬA file skill trong Cowork: ĐỪNG tin Edit/Write
> native (hay cắt cụt) — ghi bằng Python `pathlib.write_text()`/heredoc qua Bash, rồi `tl verify-integrity` để xác minh.
> Chi tiết: `references/COWORK_EDIT_SAFETY.md`.** (Sửa file đã-chunk xong PHẢI `python scripts/build_parts.py`.)
> **THIẾU config/token (phiên trống)?** `ping` báo lỗi + đường KHÔI PHỤC (fileId baked sẵn, ƯU TIÊN trên xuống):
> 1) ★★ **`tl up --nlm`** = BOOTSTRAP TẤT ĐỊNH 1-LỆNH (idempotent): config→gws cred+binary→nlm→manifest→readiness, in
>    trạng thái từng bước. **MỌI env (Chat/Cowork/Code) NÊN chạy `tl up --nlm` ĐẦU PHIÊN** để cài gws+nlm + nạp corpus NGAY.
>    (Chỉ token, không binary: `--no-binary`; bỏ nlm: bỏ `--nlm`.) Tương đương thủ công: `tl init-config --from-public --nlm`
>    rồi `tl boot`. Hoặc shell: `sh scripts/tl_fetch.sh --setup --nlm`.
>    ⚠ **COWORK TIMEOUT 45s/lệnh:** `--nlm` (uv/nlm-install) THƯỜNG vượt 45s → TÁCH BƯỚC: `sh tl_fetch.sh --setup` (core <45s, KHÔNG nlm) → rồi **LẶP `tl nlm-install --resume` tới rc=0** (★v1.30.1 #1: mỗi lần gọi chạy ĐÚNG 1 bước fetch→extract→install, trạng thái dò từ đĩa — tarball bền + uv cache; rc=3=PARTIAL còn bước, KHÔNG phải lỗi; thường ≤5 lần) → `tl nlm-auth-load` riêng. KHÔNG dùng nohup/setsid vờ chạy nền — bwrap --unshare-pid kill tiến trình con giữa 2 lần bash. `tl up` (không --nlm) ~30s. Mount Cowork cắt cụt → curl zip sạch TRƯỚC (BƯỚC 0). Temp ghi `$HOME` (1.23.15 tự trỏ TMPDIR khỏi /tmp).
> 2) curl thất bại (chưa bật public) → Drive MCP tải `CONFIG_FILEID` → `cfg.json` ($HOME, KHÔNG /tmp) → `tl init-config --file cfg.json`.
> 3) Có `TL_MASTER_KEY` → `tl bootstrap --secrets-file <s.enc>` (SECRETS public Package; token+gws+nlm); hoặc có gws cred → `tl init-config --from-drive`.
>    Sau đó `tl boot` (A3) để nạp corpus.
> Chú giải chi tiết từng bước khởi động (khối lệnh A1-A3), lý do thiết kế:
> `references/RUNBOOK.md` §A (đã chuyển khỏi kernel — nội dung không đổi).

> **MÔI TRƯỜNG THỐNG NHẤT (Chat = Cowork = Code):** cả ba nay đều có **uv + Python ≥3.11** sẵn → cài `nlm`/`gws` NHƯ THƯỜNG,
> KHÔNG còn coi Chat là môi trường hạn chế. **Chat KHÔNG tải binary Python/gws từ Drive** (đã có sẵn runtime): `nlm` =
> `tl nlm-install --uv` (uv tool install, system Python); `gws` = `tl gws-auth-load` (cred public) [+ `gws-bootstrap-cowork`
> nếu chưa có gws binary — musl-static chạy mọi OS]. gws/direct-media/GAS dùng đầy đủ ở **mọi** env (gỡ mọi hạn chế "chat
> chỉ MCP/GAS"). Khác biệt env CÒN LẠI **chỉ** ở login-gate fetch trình duyệt (§10b: code/cowork tự tải qua Claude-in-Chrome;
> chat đưa link bấm-được) — KHÔNG liên quan nlm/gws/direct-media.
Liệt kê nguồn NLM — **FAST-LANE (mọi env): `tl nlm-list <nb>`**
(CLI `nlm source list -S -d`, ~4s, ground-truth) thay `source_list_drive`
(MCP timeout ~4', không phơi `skip_freshness`). Thiếu CLI/auth → fallback MCP. Đối soát registry↔NLM:
`tl nlm-reconcile`. **Nguyên tắc (BẮT BUỘC mọi env — Chat/Cowork/Code):** MỌI thao tác NLM (ĐỌC **lẫn GHI**) đi
qua CLI `nlm`, KHÔNG qua MCP. Đọc: list→`tl nlm-list`, toàn văn→`tl nlm-content` (thay `source_get_content`),
RAG→`tl nlm-query` (thay `notebook_query`), **xuyên shard→`tl nlm-cross` (thay `cross_notebook_query`)**, **số
nguồn vật lý→`tl nlm-get` (thay `notebook_get`)**, get/describe→`nlm source get/describe`. **GHI:** thêm
nguồn→`tl nlm-add`/`tl ingest-local` (`nlm source add --drive … --wait`, **thay MCP `source_add`**),
xóa→`nlm source delete`, sync→`nlm source sync`. MCP CHỈ fallback khi thiếu CLI/auth
(hoặc studio nếu CLI chưa hỗ trợ). Lợi ích then chốt: **pipeline ingest chạy trọn trong tl
(không gãy bởi round-trip MCP)** + không tràn token/timeout.

**Sharding VBQPPL (cap 300/notebook):** corpus VBQPPL trải NHIỀU notebook (shard); mỗi dòng registry mang `nlm_notebook_id` + `row_kind ∈ {own,ref,overflow}`. Nạp VBQPPL mới ⇒ `tl preflight <số hiệu>`: shard chính đầy → `overflow_route` sang shard phụ (`config.profiles.vbqppl.overflowNotebookId`; `shards[]` forward-compatible). Sau `source_add` vào shard phụ ⇒ `tl push-overflow --drive-id --source-id` (set `row_kind=overflow`). Tra cứu xuyên shard: registry/manifest hợp nhất + **`tl nlm-cross "<câu hỏi>"`** (CLI `nlm cross query`, mặc định base+overflow; thay MCP `cross_notebook_query`). KHÔNG `notebook_create` mới trừ khi tất cả shard đầy + người dùng duyệt.
**(L4/L5 26/6) preflight đã cứng hóa:** `tl preflight` nay (a) **dedup phía tl lỏng-năm** — cảnh báo `⚠DUP-TL` khi số hiệu ĐÃ trên NLM dù KHÁC TÊN (vd `72/NQ-TW` ≡ `72/2025/NQ-TW` — đừng push lại kẻo nhân bản trong notebook đầy); (b) **verify-LIVE slot** qua `nlm-get` khi webapp báo FULL (registry từng đếm cả `removed_*` → used=322>300 ảo). **Luôn tin `nlm-get` LIVE hơn registry estimate trước khi chốt FULL/overflow/delete.**
**(L6) Notebook ĐẦY thật (LIVE 300/300) → nạp mới cần GIẢI PHÓNG slot hoặc OVERFLOW.** Ứng viên giải phóng an toàn = **bản GỐC đã có VBHN thay thế còn nằm NLM** (vd Luật 45/2019←VBHN 18 BLLĐ; 84/2015←VBHN 14/2024; 69/2020←VBHN 8/BNV) — dùng `tl reg-query --no-... ` + `tl relation-check` để lập danh sách. `source_delete` **BẤT KHẢ NGHỊCH** ⇒ LUÔN lập danh sách + **chờ người dùng xác nhận** trước khi gỡ; ưu tiên overflow nếu còn shard.

## 2. CỔNG VẬN HÀNH (mệnh lệnh — chi tiết: RUNBOOK §B)
- **Định tuyến tìm file:** TRONG corpus → webapp `find`/`search scope=corpus`/registry. NGOÀI corpus/shared/My Drive root → **Drive MCP `search_files`** (webapp `scope=all` quét thiếu). Wrapper Drive MCP chỉ hỗ trợ `fullText contains '...'` và `parentId = '...'`; KHÔNG dùng `name/title contains` vì sẽ lỗi `Unsupported query field: name`. Link-shared chưa add → theo ID.
- **Đọc cache TIẾT KIỆM TOKEN:** `tl extract <số hiệu|gdocId> --dieu N` (vị trí nhận **CẢ số hiệu** — vd `tl extract 109-2025-QH15` tự resolve canonical, KHÔNG còn báo 404 giả) → toàn văn ra ĐĨA → in đúng Điều. TUYỆT ĐỐI không cat nguyên văn vào context. (extract qua exporttext webapp **CAP ~200k ký tự**: khi chạm cap có cảnh báo "có thể bị CẮT" → toàn văn dùng `tl cache-build <sohieu>`.)
- **EXIT CODE (A3):** `xref`/`vbhn-check`/`status` trả **rc=0 khi CHẠY OK** kể cả khi phát hiện MISSING/SOHIEU_MISMATCH/REVIEW/không-có-hit (đó là PHÁT HIỆN dữ liệu / VERDICT, KHÔNG phải lệnh lỗi — không phá `&&`/CI; driver agentic không hiểu nhầm REVIEW = lệnh hỏng). Chỉ `xref --strict`/`status --strict` mới rc=1 khi có findings/REVIEW. rc≠0 = lệnh THỰC SỰ lỗi (không đọc được manifest/text).
- **Chọn nguồn `notebook_query`:** lọc-thô (`linhvuc`+`so_hieu`/`loai`+`tukhoa`) → chọn-đúng-phiên-bản (`goc`/`sua_doi`/`hieuluc`/`nlm_status`, VBHN+còn hiệu lực) → còn 3–5 mới đọc thật → query scope 1–5 source_id → verify.
- **Đa-corpus/profile:** khi ở profile P, `locate/source-map/vb_status/nlm_preflight` đọc manifest/registry của P trước; miss mới fallback VBQPPL và phải báo rõ. QA xuyên corpus dùng `cross_notebook_query` với notebook P + notebook VBQPPL. Canonical của P thắng.
- **Khóa định danh chặt:** không push/query theo hit mờ chỉ khớp số; phải khớp số + năm + loại + chủ đề, và verify dòng đầu/nội dung trước khi chốt.
- **CỔNG QUAN HỆ SỬA ĐỔI:** nếu biết/nghi có luật sửa đổi mới, chạy `tl relation-check --base <gốc> --subject <chủ đề> [--amendment <số>] --json` trước khi kết luận corpus thiếu. Nếu thấy văn bản đã có nhưng thiếu `goc/sua_doi`, hỏi người dùng xác nhận ghi registry ngay.
- **CỔNG TIỀN-NẠP QT-2** (TRƯỚC khi nạp văn bản sửa đổi/VBHN/nghi bị thay): `tl status <sohieu> --amendment --targets …` → ADD/SKIP/REVIEW. Surface quan hệ (sửa gì/bị VBHN nào hợp nhất/còn hiệu lực) TRƯỚC khi chốt. Bản sửa đổi chưa đủ VBHN cho mọi đích → GIỮ + ghi `sua_doi`.
- **CỔNG TIỀN-NẠP WEB/NLM:** đồng ý "tìm nguồn" KHÁC đồng ý "ghi vào corpus/NLM". Trước khi nạp nguồn web, phải trình người dùng duyệt `{URL, official|thứ cấp, định dạng, cat/folder/notebook đích, tên chuẩn dự kiến, số hiệu/năm/trích yếu, quan hệ gốc/sửa đổi/VBHN}`. Đích mặc định là folder Drive + notebook đang dùng; không tạo notebook mới trừ khi người dùng yêu cầu rõ.
- **Ưu tiên định dạng:** official-first; nếu có docx/doc/GDoc-convertible thì ưu tiên hơn PDF. Nếu chỉ có PDF thì convert/OCR trước; không nạp PDF thô làm canonical NLM khi có thể tạo GDoc chuẩn.
- **★ VĂN BẢN LỚN → TÁCH CÓ KIỂM SOÁT (chất lượng truy vấn cao nhất):** nạp NGUYÊN văn bản QUÁ LỚN vào 1 nguồn NLM làm GIẢM chất lượng RAG (NLM tổng hợp tốt nhất ~≤100k ký tự/nguồn; webapp exporttext CAP ~200k). Với **VBQPPL**, KHÔNG tách bản canonical: luôn giữ 1 bản đầy đủ để `tl extract`, kiểm Điều/khoản/điểm, hiệu lực, VBHN và quan hệ sửa đổi. Chỉ tạo bản tách như **nguồn phụ phục vụ truy vấn NLM** khi thật sự cần; chunk phải có `row_kind=ref`, `corpus=false`, `goc=<drive_id canonical>`, ghi chú `nlm_query_chunk`, và không dùng làm căn cứ pháp lý cuối cùng. Với **văn bản thường/profile**, được tách để tăng chất lượng truy vấn: `tl profile-ingest` lập `chunk_plan` dry-run, ưu tiên tách theo Phần/Chương/Mục/Điều/Phụ lục/heading/pagebreak; mỗi chunk nên ≤100.000 ký tự, tên ổn định và có phạm vi rõ. `tl ingest-local` với file lớn > `NLM_LARGE_SRC_BYTES` (~1.2MB, chỉnh `--large-threshold`) vẫn DỪNG ở `large_file_split_gate`, hỏi người dùng chọn tách hoặc `--allow-large`; KHÔNG tự tách tùy tiện.
- **★ PDF SCAN/OCR → CỔNG CHẤT LƯỢNG:** ưu tiên tìm bản `.docx`/`.doc`/GDoc hoặc text-layer sạch trước. Nếu cần tạo sidecar text local, dùng `tl ocr-run` (an toàn: text-layer/ocrmypdf nếu có; Drive/Paddle/DocumentAI vẫn bị gate nếu chưa cấu hình live), sau đó bắt buộc chạy `tl ocr-verify`. Khi ingest nguồn OCR phải gắn `--source-quality ocr`; chỉ dùng `--ocr-verified` sau khi đã đối chiếu không mất trang, không mất Điều, không sai Phụ lục và không lỗi chữ nghiêm trọng. Với VBQPPL, PDF scan/OCR chưa đạt thì KHÔNG đưa vào corpus/NLM làm canonical. Với profile văn bản thường, OCR chưa verify có thể lưu làm bản tham khảo/corpus=false, phải cảnh báo và không dùng làm căn cứ cuối cùng. Công cụ sẵn có: `tl ocr-analyze`, `tl ocr-run`, `tl ocr-verify`, `tl ingest-local --text-file --source-quality ocr --ocr-verified`, `tl profile-ingest --text-file --source-quality ocr --ocr-verified`, `tl source-verify`, `tl cat-verify`, `scripts/verify_deep.py`.
- **★ NLM theo PROFILE (đa-corpus):** push/query NLM (`ingest-local`/`nlm-add`/`nlm-query`/`nlm-reconcile`) NHẮM `notebookId` của **PROFILE ĐANG DÙNG** (`TL_NOTEBOOK_ID` từ `config.profiles.<active>.notebookId`), KHÔNG mặc định VBQPPL base. Luôn chạy với `--profile <P>` đúng; profile thiếu `notebookId` → lỗi `NO_NOTEBOOK_ID` (truyền `--notebook-id`). **(v1.33.48)** `--profile`/`--config` nhận Ở CẢ SAU subcommand (`tl reg-query --profile "Luật BHXH"` hết gãy rc=2); tên profile CHỊU-LỖI-GÕ (không-dấu/hoa-thường/space-_- khớp DUY NHẤT → dùng tên canonical config); tên KHÔNG có trong config → **PROFILE_NOT_FOUND + scope RỖNG** (KHÔNG rơi âm thầm về nền vbqppl như trước — hết lớp 'ghi nhầm corpus nền vì gõ sai tên profile'). `register` nhận `--nlm-notebook-id` (khỏi `backfill-notebook` riêng); `nlm-reconcile` tự bắc cầu gdoc↔source_id (link nguồn live vào dòng registry theo drive_id/số hiệu). Sau khi GHI sheet (reg_upsert/ingest/backfill) → `reg-query --refresh` mới thấy LIVE (cache cũ báo nlm rỗng).
- **Đặt tên + sắp xếp** (QT-3): `copy_convert` → `standardize_name.py` → `organize` → verify `list cat=<NN>` (ĐỪNG tin response `move`). File gốc nằm CẠNH GDoc, KHÔNG add NLM.
- **Link cho người dùng** (QT-1): markdown click-mở-được; ĐỦ cả link upload (`_HOP_NAP`) lẫn download. Với link để người dùng tự tải: ưu tiên `thuvienphapluat.vn` → `luatvietnam.vn` → `congbao.chinhphu.vn` → official khác → trang khác. Không đổi canonical official-first.
- **Slot notebook:** nếu preflight báo full nhưng `notebook_get` không full, chạy `tl slot-audit --notebook-id <id> --json`; lỗi thường do đếm mọi row `nlm_status` thay vì `nlm_notebook_id`.
- **QT-5 tìm VBHN:** theo TRÍCH YẾU văn bản GỐC (+ "hợp nhất"), KHÔNG theo số hiệu/tên bản sửa đổi. Sau `source-map`/`relation-check`, chạy `tl vbhn-check`; nếu corpus không có hit thì BẮT BUỘC search web bằng query gợi ý (`luật <chủ đề> hợp nhất`, TVPL/luatvietnam để phát hiện nhanh, official để chốt). Sau khi có ứng viên, chạy `tl vbhn-verify --official-required`.

## 3. KẾT PHIÊN
```bash
python scripts/tl.py manifest                 # mặc định: chỉ manifest_export (không đụng cấu trúc)
# profile categories=inherit → CHỈ export-only
# KHÔNG manifest --touched-drive trên profile văn bản thường (gây PROFILE_MANIFEST_SCOPE_BLOWUP)
# nếu thật sự cần quét cây own của profile:
python scripts/tl.py manifest --touched-drive --confirm yes

# phục hồi nếu registry profile đã bị phình (DRY trước):
python scripts/tl.py --profile <P> profile-rebuild-registry --keep-notebook <id>
python scripts/tl.py --profile <P> profile-rebuild-registry --keep-notebook <id> --apply --confirm yes
```


## 4. CLI `tl` — nhóm lệnh chính (bảng đầy đủ: `references/COMMANDS.md`)

Nguồn sự thật MÁY-ĐỌC: `tl tool-inventory --json` (kèm registry metadata risk/gate/card/contract) và
`tl route-task <tác_vụ> --json` cho tác vụ rủi ro. Nhóm chính:

| Nhóm | Lệnh tiêu biểu |
|---|---|
| Bootstrap & health | `up` · `boot` · `doctor` · `ping` · `gws-ping` · `verify-integrity` · `precheck` |
| Tìm & xác minh nguồn | `find-doc` · `exists` · `locate` · `source-map` · `status` · `relation-check` · `vbhn-check/verify/compare` · `extract` |
| Nạp & convert (GHI — dry-run trước) | `ingest-local` · `profile-ingest` · `ingest-zip` · `ingest-ocr` · `profile-ingest-chunks` · `convert-verify` · `nlm-add` |
| OCR & chunk (local an toàn) | `ocr-analyze/run/verify` · `chunk-plan/apply/verify` |
| NLM | `nlm-list/get/query/cross/content` · `nlm-reconcile` · `nlm-orphans` · `counts --live-nlm` · `slot-audit` |
| Registry & corpus | `reg-query` · `register` · `recat` · `backfill-loai/title-vn/hieuluc` · `sweep` · `dedup-plan` · `corpus-audit` · `source-rename/delete/update-corpus` · `hygiene` |
| Audit & release | `workflow-audit` · `determinism-audit` · `golden-test` · `release-manifest/verify/bundle/check` · `bundle-export` |
| Live & deploy | `live-readiness` · `live-contract-check` · `live-state-snapshot/diff` · `deploy-plan` · `rollback-plan` · `go-live-runbook` · `final-acceptance` · `drive-push` |

Quy tắc chung mọi lệnh GHI: DRY mặc định → `--apply` (± `--confirm yes`) → verify/readback → journal (undo được).
Cờ `--profile/--config/--deterministic` nhận ở mọi lệnh (trước hoặc sau subcommand); `--json`/`--out` KHÔNG toàn cục — chỉ những lệnh có khai, đặt SAU subcommand (tra `references/COMMANDS.md` hoặc `tl <lệnh> -h`).

## 5. HAI KIỂU CẤU TRÚC (tự nhận diện)
- **Kiểu Điều** (Hiến pháp/Luật/Bộ luật/NĐ/TT/NQ): Phần/Chương/Mục/Điều/Khoản/Điểm. Tra "Điều 7 khoản 2 điểm a".
- **Kiểu Mục Đảng** (văn kiện, NQ/KL/CT của Đảng): bố cục La Mã/số — Profile B heuristic; xem trước `split_structure.py f.txt deep auto` rồi mới tra.

## 6. TRA CỨU NHANH
- Đảo thứ tự được: "khoản 2 Điều 7" = "Điều 7 khoản 2". Mặc định prefix (Điều 7 trả cả khoản/điểm con); `--exact` chỉ đúng đơn vị.
- `light` = toàn văn 1 đơn vị · `article` = tới Điều/Mục · `deep` = tới Khoản/Điểm.
- `tra_cuu.py` (viết tắt Đ7/K2, từ cache) · `get_legal_article` (MCP) · DEEP mode: verbatim từ cache, NLM chỉ định vị.

## 7. BẢN ĐỒ SCRIPT (đầu mối qua `tl`; danh sách đầy đủ + lý do: DOCTRINE_APPENDIX)
- **Khởi động/hạ tầng:** `tl.py` · `gas.py` (client webapp) · `contract_check.py` · `apply_gs_patches.py` (áp patch .gs) · `boot.py` · `common.py` · `cache.py` · `manifest_build.py`.
- **Nạp/sắp xếp:** `ingest_to_cache.py` · `standardize_name.py` · `preingest_gate.py` (QT-2) · `import_drive_link.py` · `sapxep.py` · `normalize_document.py` · `split_structure.py`.
- **NLM:** `nlm_push.py` · `nlm_qa.py` · `nlm_sources.py` (`-S`) · `nlm_map.py` · `dedup_gate2.py`.
- **Rà soát/registry:** `registry_orchestrator.py` · `rasoat_worksheet.py` · `rasoat_phuluc.py` · `backfill_keywords_live.py` · `backfill_nlm_title.py` · `vbhn_query.py` (QT-5) · `vb_status.py`.
- **Tra cứu/Instruction:** `tra_cuu.py` · `keywords.py` · `verify_deep.py` · `gen_instructions.py` (sinh/audit Instruction có `SKILL_OF_RECORD` + external-ingest gate).

## 8. APPS SCRIPT WEBAPP
Live/post-deploy contract = **2.21.2j** (đã xác minh `ping.version=2.21.2j`, `registry_schema=reg_cols_row_kind_v1`, 27 cột). Bản `.gs` hiện hành = **`references/Code.2.21.2j.gs`**. Tham số/khóa/gotcha MỌI action: **`references/API_CONTRACT.md`**.
- **`references/Code.2.21.2j.gs`:** giữ toàn bộ Cách B/`row_kind` của 2.21.2h, đồng thời thêm `manifestScope=own|inherited`, quét đệ quy đúng `rootFolderId` của profile, giữ nguyên dòng `ref`, và chặn ghi với `PROFILE_MANIFEST_SCOPE_BLOWUP` nếu số dòng own tăng quá `max(2×old, old+50)`.
- **`references/REGEN2_PROFILE_SCOPE_V1.19.5.md`:** quyết định best-combined, khác biệt hai nhánh và quy trình phục hồi an toàn.
- Bản `.gs` đời trước (2.21.1→2.21.2h) ĐÃ đưa ra archive ngoài skill (gọn gói ≤200 file) — chỉ giữ bản LIVE `Code.2.21.2j.gs`; lịch sử/biện luận ở `DOCTRINE_APPENDIX.md` + `CHANGELOG.md`.
- Deploy `Code.2.21.2j.gs` → New version (giữ URL+token), `tl ping` phải ra `2.21.2j`, rồi `contract_check.py --audit`. **KHÔNG deploy từ skill được.**
- Cột registry mới muốn sống qua `regen2` → khai báo `REG_COLS_` + `REG_NLM_KEEP_` trong `.gs` → Deploy → `reg_addcols&confirm=yes`.
- Lịch sử vá: F1–F16c → 2.21.2b; profile-scope guard → 2.21.2j. `API_CONTRACT.md`, `tl.py EXPECT_VERSION`, SKILL/RUNBOOK đồng bộ `2.21.2j`.


## 9. PHỤ THUỘC
`pip install -r requirements.txt`. Cần env `TL_WEBAPP` / `TL_TOKEN` (mirror `tra_luat_config.json`).

> Chi tiết runtime-overlay (từng lệnh bổ sung, fileId phụ, cache per-profile, hạn cred NLM ~1h /
> gws 7-ngày-Testing + gcloud fallback): `references/DEPENDENCIES.md` (nguyên văn §9 cũ).
> Bảng lệnh đầy đủ kèm ghi chú version: `references/COMMANDS.md`.

## v1.17.26 combined external-ingest + instruction-audit gate

- Trước mọi nạp nguồn web/NLM-native, chạy `tl external-ingest <url> ... --json` để kiểm kế hoạch. Lệnh này chỉ kiểm, không ghi Drive/NLM.
- `research_start/research_status` chỉ dùng để phát hiện URL; `research_import/source_add(url)` không được dùng để nạp VBQPPL làm nguồn canonical.
- Instruction dùng cho Claude Project/NLM phải qua `tl instruction-audit` hoặc sinh bằng `tl instructions`/`scripts/gen_instructions.py`; thiếu `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web` thì không dùng.



## OCR / CHUNK / RELEASE — doctrine rút gọn (chi tiết: workflow cards + DOCTRINE_APPENDIX)

- OCR sidecar + chunk local KHÔNG ghi thẳng Drive/registry/NLM — mọi đường vào corpus quay về pipeline
  ingest/verify/readback. VBQPPL: OCR thiếu manifest `verification_status=verified` → CHẶN canonical;
  KHÔNG tách bản canonical (chunk chỉ là nguồn phụ `row_kind=ref, corpus=false, goc=<canonical>`).
- Release: sau MỌI sửa file → `release-manifest --out RELEASE_MANIFEST.json` trước khi đóng zip;
  gate đóng gói = selftest + workflow-audit/determinism-audit --strict + golden-test + bundle ×2 cùng SHA
  + release-verify trong gói giải nén. Workflow cards: `references/workflows/*.json` (schema v1);
  golden fixtures: `references/golden/` (fixtures sinh-tại-chỗ tất định).
- Golden fixtures: use `golden-test --write` only after an intentional CLI/schema change and then rerun
  `determinism-audit --strict` — CẤM `--write` để "xanh hóa" gate golden đỏ (che regression thật).
- Từ v1.33.53, mọi snapshot/report vận hành phải ưu tiên ghi vào `.tl_state/`; `before.json`, `after.json`,
  `reports/`, `dist/` và các runtime artifact không được tính vào release manifest.

## LỆNH KIỂM CUỐI TRƯỚC BÀN GIAO (mọi thay đổi skill)

```sh
python scripts/tl.py --selftest
python scripts/tl.py workflow-audit --strict --json
python scripts/tl.py golden-test --json
python scripts/tl.py determinism-audit --strict --json
python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --json
```

## DANH MỤC REFERENCES

| File | Nội dung |
|---|---|
| `references/COMMANDS.md` | Bảng lệnh `tl` đầy đủ (nguyên văn §4 cũ) |
| `references/DEPENDENCIES.md` | Phụ thuộc + runtime-overlay (nguyên văn §9 cũ) |
| `references/RUNBOOK.md` | Khởi động chi tiết theo môi trường, vận hành LIVE |
| `references/API_CONTRACT.md` | Hợp đồng webapp GAS (action/param/version) |
| `references/DOCTRINE_APPENDIX.md` | Toàn bộ doctrine mở rộng + lý do thiết kế |
| `references/workflows/*.json` | Workflow cards máy-đọc (schema, risk, idempotency) |
| `references/golden/*.json` | Golden fixtures tất định |
| `CONTEXT.md` (gốc repo) | Từ điển thuật ngữ chuẩn của dự án |
| `docs/adr/` | Quyết định kiến trúc (ADR-0001 bundle-protocol, ADR-0002 bind-giàn-giáo) |
| `references/changelog_archive/` | CHANGELOG cũ (kernel giữ 10 version gần nhất) |

