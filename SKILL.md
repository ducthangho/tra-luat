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

# tra-luat — LÕI VẬN HÀNH (v1.33.1)

> Đây là LÕI MỆNH LỆNH. Ba tài liệu vận hành (đọc khi cần, KHÔNG nạp toàn bộ vào context):
> - **`references/API_CONTRACT.md`** — tham số + khóa response MỌI action webapp (target `2.21.2i`). **Tra trước khi gọi action — KHÔNG đoán tham số.**
> - **`references/RUNBOOK.md`** — trình tự khởi động + cổng vận hành (đánh số, tất định).
> - **`references/DOCTRINE_APPENDIX.md`** — lịch sử + biện luận đầy đủ (changelog v1.x→v1.15.7). Tra khi cần BỐI CẢNH/lý do.
>
> Khi mâu thuẫn: LÕI + API_CONTRACT + RUNBOOK **thắng** phụ lục.

## 0. NGUYÊN TẮC BẤT BIẾN
1. **VBHN-first + LATEST-VBHN** — có VBHN còn hiệu lực → dùng VBHN, không bản gốc/sửa đổi rời. **Khi TRA/TÌM Luật theo tên:** thử keyword **'<tên> hợp nhất' TRƯỚC** (vd "Luật PPP hợp nhất") → rồi **'<tên> mới nhất'** → cuối cùng tên gốc; truy vấn theo SỐ HIỆU thì tìm thẳng. **MỌI tìm-văn-bản-trên-web dùng GOOGLE `site:` (VBHN-first), KHÔNG dùng search nội bộ TVPL/LVN (kém)** — áp cho `fetch-route`/`fetch-links`/`find-doc` VÀ QT-5 (`vbhn-check`/`status`/`relation-check` đều xuất `google_discovery`). **⚠ S9/S11 (log 🔴 2026-07-01): KHÔNG chốt ở VBHN ĐẦU TIÊN tìm thấy — số hiệu VBHN TĂNG theo mỗi lần hợp nhất (Bộ luật Hình sự: 01/VBHN 2017 → 11/VBHN → 135/VBHN 2025; KHÔNG phải semver).** Bắt buộc LƯỢT-2: tìm SỐ VBHN LỚN HƠN / NGÀY MỚI HƠN cùng cơ quan (VPQH) qua `'<tên> hợp nhất mới nhất <năm>'` + `site:congbao.chinhphu.vn`. Ứng viên VBHN chưa xác minh là mới nhất → cờ `VBHN_CANDIDATE_UNVERIFIED_LATEST`. **S10:** luật cải cách cao 2024-2026 (Hình sự/tố tụng/phí-lệ-phí/đất đai/doanh nghiệp/đầu tư/đấu thầu/thuế…) → cờ `VBHN_HIGH_AMENDMENT_VELOCITY`, PHẢI kiểm bản hợp nhất mới nhất trước khi trả.
2. **Verify nguyên văn** — điều khoản trả ra lấy từ cache/raw đã xác minh; NLM chỉ định vị + tổng hợp; KHÔNG nhận RAG làm nguyên văn.
3. **Official-first cho VBHN** — thiếu VBHN chính thức thì HỎI người dùng nạp vào `_HOP_NAP` hoặc lấy nguồn chính thức; KHÔNG tự ghép bản hợp nhất làm bản dùng. Bản tự ghép/chắp nội dung chỉ là bản tạm để so sánh, phải gắn provisional và quarantine khi có bản chính thức.
4. **Không bịa** — thiếu dữ liệu → nói "không có" / REVIEW.
5. **Dedup nhiều lớp** — cache → registry → NLM (số hiệu + biến thể + text_hash).
6. **ĐỐI CHIẾU NGAY** — phát hiện văn bản đã bị sửa đổi/lỗi thời/VBHN thiếu → DỪNG rà bản cũ, chạy `tl relation-check` + `tl vbhn-check`, hỏi người dùng nạp/ghi registry ngay. KHÔNG gác vào Mục F.
7. **Tên NLM = tên Drive** — đổi tên thì đổi đồng bộ GDoc + file gốc + registry + nlm_title + source NLM.
8. **External ingest gate** — `research_start/research_status` chỉ để phát hiện URL. CẤM dùng `research_import`/`source_add(url)` nạp thẳng VBQPPL vào NLM. Mọi nguồn mới phải đi Drive → convert → tên chuẩn → folder đúng → verify → `nlm_push` vào notebook đang dùng, sau khi người dùng duyệt đích/định dạng/tên.
9. **Corpus profile** — luôn đọc config VBQPPL trước để lấy webapp/token, rồi overlay `TL_PROFILE`/`--profile`. Văn bản thường dùng profile riêng (`vbthuong`: folder/notebook/registry/manifest riêng), KHÔNG mặc định VBQPPL. **Cách B (v1.19):** `--profile P` tự forward `registryDocId`/`manifestId` vào mọi call webapp → registry/manifest RIÊNG; nêu rõ profile ở đầu yêu cầu (xem RUNBOOK §D). **★ v1.30.0 — profile chạy CÙNG VBQPPL, KHÔNG thay thế:** profile dự án mặc định `TL_BASE_ALSO=1` → lệnh ĐỌC (`locate`/`reg-query`/`source-map`/`exists`/`nlm-cross`) quét `{scope profile} ∪ {VBQPPL nền + shards}`, **hit profile ưu tiên**, hit nền đánh dấu `scope=vbqppl`/cờ `BASE_SCOPE_HIT`; opt-out `profiles.<p>.baseAlso=false` hoặc `--no-base-also`. Đường GHI/ingest KHÔNG đổi scope (vẫn profile riêng — không đẩy nhầm đích). **BẤT BIẾN LAYOUT:** registry + manifest của profile phải nằm TRONG thư mục profile (root hoặc `_meta`) — kiểm `tl profile-doctor` (`--fix --apply` move về `_meta`, fileId GIỮ NGUYÊN). Danh mục profile-thật-trên-Drive đối chiếu config: `tl profile-list --discover`; seed profile có sẵn hạ tầng: `tl profile-adopt`; sổ cái đọc-được trên Drive: `tl profile-index` (`Van_ban_thuong/_PROFILES_INDEX` — BẢN CHIẾU, nguồn sự thật duy nhất vẫn là config).
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
```bash
# ⤵ ĐƯỜNG LOCAL / mount lành (COWORK: ĐÃ xong ở BƯỚC 0 qua tl_fetch.sh — KHÔNG chạy lại khối này, KHÔNG đụng _parts).
# A1 readconfig→env (TỰ thấy tra_luat_config.v2.json ở cwd/gốc skill; THIẾU/phiên-trống → `tl init-config --from-public --nlm`
#    để cài LUÔN gws binary + nlm NGAY TỪ ĐẦU, KHÔNG chỉ cred — tránh find/ghi rơi GAS mọi phiên) ; A2 version ; A3 corpus
python scripts/tl_boot.py ping       # PHẢI version 2.21.2i (LIVE) — lệch thì DỪNG, đối chiếu API_CONTRACT/deploy
python scripts/tl.py --profile vbthuong profile-info --json  # nếu làm văn bản thường/profile dự án
python scripts/tl.py boot            # đọc manifest (phân trang) → ~/.tra_luat_cache/manifest_index.json
python scripts/contract_check.py     # (tùy chọn) tự bắt trôi version vs hợp đồng
```
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
- **★ FILE LỚN → HỎI TÁCH (chất lượng truy vấn cao nhất):** nạp NGUYÊN văn bản QUÁ LỚN vào 1 nguồn NLM làm GIẢM chất lượng RAG (NLM tổng hợp tốt nhất ~≤100k ký tự/nguồn; webapp exporttext CAP ~200k). `tl ingest-local` có **CỔNG HỎI TÁCH**: file > `NLM_LARGE_SRC_BYTES` (~1.2MB, chỉnh `--large-threshold`) → DỪNG `--apply`, in `large_file_split_gate` + gợi ý **TÁCH theo Phần/Chương/cụm Điều rồi ingest TỪNG PHẦN (mỗi phần 1 nguồn)**. PHẢI hỏi người dùng cho phép tách (hoặc họ chọn `--allow-large` để nạp nguyên, chấp nhận giảm chất lượng). KHÔNG tự tách (cần người duyệt cách tách hợp lý theo cấu trúc văn bản).
- **★ NLM theo PROFILE (đa-corpus):** push/query NLM (`ingest-local`/`nlm-add`/`nlm-query`/`nlm-reconcile`) NHẮM `notebookId` của **PROFILE ĐANG DÙNG** (`TL_NOTEBOOK_ID` từ `config.profiles.<active>.notebookId`), KHÔNG mặc định VBQPPL base. Luôn chạy với `--profile <P>` đúng; profile thiếu `notebookId` → lỗi `NO_NOTEBOOK_ID` (truyền `--notebook-id`). `register` nhận `--nlm-notebook-id` (khỏi `backfill-notebook` riêng); `nlm-reconcile` tự bắc cầu gdoc↔source_id (link nguồn live vào dòng registry theo drive_id/số hiệu). Sau khi GHI sheet (reg_upsert/ingest/backfill) → `reg-query --refresh` mới thấy LIVE (cache cũ báo nlm rỗng).
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

## 4. CLI `tl` (đầu mối — bọc gas.py + module đã kiểm thử)
| lệnh | việc |
|---|---|
| `tl ping` | ping + cổng version 2.21.2i |
| `tl perf` / `--timings` | đo thời gian thật từng call (round-trip ~3.3s; song song ~3x); chẩn đoán nút thắt |
| `tl xref <gdocId\|sh>` | bóc dẫn chiếu → cờ MISSING/OUTDATED/SOHIEU_MISMATCH/OMNIBUS + **bản đồ sửa đổi cấp Điều** (B3) + rel_type (report-only) |
| `tl footnote-map <gdocId\|sh>` | **B3**: bản đồ sửa đổi cấp Điều từ footnote VBHN (marker[n]↔chú thích luật sửa) + `PENDING_EFFECT` (hiệu lực tương lai) |
| `tl cluster [<pháp luật về X>]` | **E2**: cụm lĩnh vực → số hiệu canonical (VBHN-first); bỏ trống = liệt kê |
| `tl rasoat-chongcheo <base> [--text-file]` | **E1 (v1)**: dựng tập liên quan (cụm E2 + footnote B3) + hiện diện corpus + PENDING (so sánh quy phạm = giai đoạn sau) |
| `tl dedup-check <q>` | dedup offline theo bộ danh tính/alias (thay nlm_dedup); DUPLICATE/MAYBE/NEW |
| `tl ingest-route <file/sh>` | cây quyết định định hướng file nhập (advisory) |
| `tl slot-audit --physical N` | neo sức chứa vật lý (notebook_get.source_count), in gap |
| `tl backfill-notebook --notebook <id> …` | ghi nlm_notebook_id (reg_bulk, DRY mặc định) |
| `tl cache-snapshot export\|import` | snapshot manifest_index có cổng treeHash |
| `tl nlm-list <nb>` | fast-lane CLI `nlm` --skip-freshness (~4s) — thay source_list_drive (MCP timeout) |
| `tl nlm-reconcile <nb> [--apply] [--clear-stale]` | đối soát registry↔NLM ground-truth: backfill nlm_notebook_id, báo stale/unregistered |
| `tl preflight <số hiệu>` | sharding: định tuyến nạp VBQPPL mới (nlm_preflight); base đầy 300 → `overflow_route` sang shard phụ |
| `tl push-overflow --drive-id <> --source-id <>` | sau source_add vào shard overflow → cập nhật registry `row_kind=overflow` |
| `tl nlm-add <nb> --drive <id> [--wait]` | **(1)** thêm nguồn NLM qua CLI `nlm source add` (thay MCP source_add) |
| `tl ingest-analyze --file <f> [--text-file <txt>] [--cat NN]` | **(v1.25) TỰ PHÂN TÍCH (DRY, read-only):** đọc HEADER → ĐỀ XUẤT `name` chuẩn (`Luat_113-2025-QH15_Dan_so`; dự thảo→`DUTHAO_`) + `cat` (boundary-rule > content, kèm `cat_plan`/confidence) + sohieu/loai + **lệnh `ingest-local --auto-plan --apply` điền sẵn**. Dùng chung analyzer `_vb_ingest_auto_plan`. .docx/.pdf: Claude đọc→lưu `.txt`→`--text-file`. Verify TRƯỚC `--apply` |
| `tl ingest-local <file> --auto-plan [--text-file <txt>] [--force-cat] [--apply]` | **(v1.25) NẠP TÍCH HỢP:** `--auto-plan` đọc nội dung local → tự suy `name/sohieu/loai/cat` (chỉ điền ô còn trống; explicit `--name/--cat` thắng) → upload→convert GDoc→cat folder→registry→`nlm add`. Cat mơ hồ/thiếu text → DRY, chặn `--apply` trừ `--cat`/`--force-cat`. `--source-quality ocr --ocr-verified` cho PDF OCR |
| `tl ingest-local <file> --name --sohieu --cat --goc [--apply]` | **(2)+(3) ĐƯỜNG UPLOAD TRỰC TIẾP (file local trong môi trường Claude)** 1-lệnh: upload **MIME thật (.docx/.doc/.pdf)**(convert=false)→organize(convert=true server-side+rename+cat+stamp+register)→preflight→CLI nlm add→push. DRY mặc định; validate cat theo 45 chủ đề + auto `mkdir`. .pdf→cảnh báo `format_warn` (verify nguyên văn). **Luồng khuyến nghị: `ingest-analyze` (suy name+cat) → verify → `ingest-local --apply`** |
| `tl cat-list [--missing]` | liệt kê 45 chủ đề pháp điển chính thức (`references/phap_dien_45.json`) + folder đã có |
| `tl reg-query [--name/--sohieu/--cat/--nlm/--no-nlm/--row-kind/--corpus/--mime] [--json]` | **truy vấn registry/manifest OFFLINE + lọc** — thay viết tay `json.load(manifest)+filter`; tra drive_id theo tên, liệt kê 1 cat, lọc nlm/corpus… ⚠ `--corpus`/`--nlm` là CỜ TRẦN (lọc =true); từ v1.29.6 nhận cả `--corpus true/false`; lọc corpus=false dùng `--no-corpus` |
| `tl recat <drive_id…> --cat NN [--quarantine] [--apply]` | **di dời file → folder chủ đề** (mkdir đúng tên nếu thiếu) + cập nhật registry; `--quarantine` cách ly. DRY mặc định |
| `tl cat-audit [--json]` | **audit cấp 2**: doc corpus có folder ≠ chủ đề suy từ tên (heuristic) → rà tay rồi `recat`. **(v1.30.1 #8)** precision-first CỐ Ý ít cờ — KHÔNG dùng làm audit duy nhất; audit sâu đọc header thật: `tl corpus-audit` |
| `tl confirm --sohieu/-drive-id/-cat NN/--all-unconfirmed [--apply] [--force]` | **GÁN NHÃN ĐÃ-RÀ-KỸ** (registry.verified): ĐỌC HEADER xác minh sohieu+tiêu đề+loại+cat khớp tên+thư mục → mismatch KHÔNG gán (trừ `--force`). DRY mặc định. Entry đã confirm → source-map/dedup TIN dùng luôn (bỏ DIRTY/WARN, tăng tốc rà soát) |
| `tl nlm-cross "<câu hỏi>" [--notebooks csv\|--all]` | cross-shard query CLI (thay `cross_notebook_query`; mặc định base+overflow) |
| `tl nlm-get <nb>` | số nguồn vật lý + chi tiết notebook CLI (thay `notebook_get`; slot/preflight) |
| `tl nlm-content <source_id> [--out\|--dieu N]` | NLM read qua CLI: toàn văn raw 1 source (thay MCP `source_get_content`) |
| `tl nlm-query <q> [--source-id …]` | NLM RAG qua CLI (thay MCP `notebook_query`); verify nguyên văn sau |
| `tl reg-delete --drive-ids id,… [--force]` | gỡ dòng registry (bọc reg_delete); chỉ xóa DÒNG, không đụng Drive/NLM |
| `tl bench [--rounds N]` | đo hiệu năng tính năng in-code (offline) trên manifest |
| `tl tvpl-url <số hiệu>` | URL tìm TVPL + luồng auto-download docx (Claude in Chrome login VIP → ~/Downloads → _HOP_NAP) |
| `tl find-doc <số hiệu\|tên>` | tìm văn bản web = **Google site: + VBHN-first** (primitive dùng chung, thay search nội bộ kém) |
| `tl fetch-links <số hiệu\|tên> [--env]` | **C2(b)**: link bấm-được TẢI XUỐNG (gated docx, VBHN-first) + TẢI LÊN `_HOP_NAP`; `--env code\|cowork\|chat` (mặc định auto; không chắc→chat). code/cowork: nhắc HỎI trước |
| `tl fetch-route <số hiệu\|tên>` | **AUTO** (Claude tải): dedup + kế hoạch tải ưu tiên **docx>doc>pdf** + biến thể VBHN-first |
| `tl fetch-batch <…> [--file --delay --jitter]` | điều phối danh sách: SKIP_DEDUP/REVIEW_DEDUP/FETCH + checkpoint; tải thật do agent chạy Chrome có throttle |
| `tl boot [--refresh] [--max-age N]` | đọc manifest → index offline; **tái dùng cache local nếu < TTL (0 call, ~0.2s)**; `--refresh` ép tải lại |
| `tl profile-info --json` | đọc config v2, in profile active và folder/notebook/registry/manifest |
| `tl locate <q>` | tra số hiệu/từ khóa (manifest offline → fallback `find`), in `WARN=...` khi tên/registry có rủi ro. **(v1.30.0)** ở profile dự án mặc định quét THÊM nền VBQPPL (mục `[nền VBQPPL]` riêng, profile ưu tiên); tắt: `--no-base-also` — cùng cặp cờ này ở `exists`/`source-map`/`reg-query`/`nlm-cross` |
| `tl exists <q>` | kiểm tra hiện diện/nguồn liên quan bằng `source-map` chuẩn hóa; miss → `UNKNOWN_NOT_ABSENT`, không kết luận vắng mặt |
| `tl source-map <q...>` | lập bản đồ nguồn rà soát VBHN-first; tránh nhầm hit theo tên trước khi chốt nguồn. **TRA THEO SỐ HIỆU cho kết quả SẠCH; tra theo TÊN TỰ NHIÊN ở corpus lớn dễ nhiễu (§14) → có số hiệu thì dùng số hiệu.** Cờ mới: `GOC_SUBJECT_MISMATCH` (registry.goc của 1 VBHN trỏ số này nhưng tên/chủ đề VBHN khác hẳn = goc NHIỄM → KHÔNG redirect, xem `goc_mismatch_vbhn`); `AMENDMENTS_ALREADY_CONSOLIDATED` (luật-sửa đã trong chuỗi goc VBHN → không PAUSE); `AMENDMENT_CANDIDATES_COVERED_BY_VBHN_DATE` (cổng PHỤ: VBHN ban hành ≥ mọi luật-sửa có ngày rõ → hạ PAUSE→INFO); `CANONICAL_VBHN_NUMBER_DIFFERS` (số hiệu chỉ mục ≠ số hiệu VBHN thật của canonical → trích dẫn theo số VBHN). **`tl status` cũng có cổng chủ đề:** webapp gợi ý VBHN lệch chủ đề → trả REVIEW `VBHN_GOC_SUBJECT_MISMATCH` (không tự SKIP/USE_VBHN sai) — luôn đối chiếu `source-map`. **v1.24.4:** `--json` có `verdict` (OK/REVIEW/PAUSE_AND_ASK_USER/UNKNOWN_NOT_ABSENT) + `flags` top-level (per-item VÀ aggregate cả batch) → driver batch khỏi regex trên text; `TITLE_OR_REGISTRY_WARN` HẾT nhiễu (bỏ dòng ghost rỗng-tên + cờ TRÔI registry↔NLM của bản thô — đã ở doctor/sweep/nlm_gaps); nhận diện số hiệu luật trước-1992 `NN-LCT-HDNNx` (query+tên+goc-chain base) |
| `tl relation-check --base <sh> --subject <tên> [--amendment <sh>]` | bắt văn bản sửa đổi/VBHN đã có trong corpus nhưng registry thiếu `goc/sua_doi`; trả hành động backfill cần hỏi người dùng |
| `tl instruction-audit --file <instruction.md>` | kiểm Instruction/Project prompt có ràng buộc `SKILL_OF_RECORD`, QT-3, research discovery-only, official/docx-first |
| `tl instruction-audit --generate --target nlm --print-text` | sinh Instruction chuẩn bằng `gen_instructions.py` rồi tự audit |
| `tl external-ingest <url> --json` | kiểm kế hoạch nạp nguồn web/NLM-native; chỉ kiểm, không ghi |
| `tl link-priority <url...> --json` | xếp link tải cho người dùng theo TVPL/LuatVietnam/Công báo |
| `tl slot-audit --notebook-id <id> --json` | đếm slot theo `nlm_notebook_id`, chống `NOTEBOOK_FULL` giả |
| `tl instructions --target project` | sinh Instruction — **mặc định VBQPPL**; `--profile <tên> --notebook <id> --folder-name <tên>` ⇒ gắn profile văn bản thường (fallback VBQPPL) |
| `tl profile-create --name <X> --notebook <id> [--apply]` | dựng profile văn bản thường: tạo folder `Van_ban_thuong/<X>` (khi `--apply`) + config patch + Instruction gắn profile (DRY mặc định) |
| `tl profile-list [--json]` · `tl registry-map` | **(v1.25) VIEW**: `profile-list` liệt kê MỌI profile (folder/notebook/registry/manifest/cat + default); `registry-map` bản đồ hợp nhất VBQPPL (base+overflow shard) + mọi profile + notebook. Dẫn xuất config — validate live bằng `nlm-get`/`profile-info`, KHÔNG store ghi tay |
| `tl profile-list --discover [--folder-cap N] [--json]` | **(v1.30.0) KHÁM PHÁ**: quét `Van_ban_thuong` LIVE (2 cấp: con + `_meta`), đối chiếu config → 🟠 profile-thật-chưa-đăng-ký (kèm lệnh `profile-adopt` điền sẵn), ⚪ vỏ rỗng, 🔴 registry/manifest LẠC GỐC (ca NQ36), ⚠ config-only. READ-ONLY |
| `tl profile-adopt --name <p> --folder <id> [--notebook <nb>] [--registry <id>] [--manifest <id>] [--bootstrap-manifest] [--apply]` | **(v1.30.0) SEED profile ĐÃ CÓ hạ tầng** vào config (khác `profile-create` = dựng mới): tự dò registry Sheet + manifest JSON trong folder/`_meta`; **GUARD**: mime Sheet thật + ≠ Doc legacy `1mATG` + schema `REGISTRY_SCHEMA_COLS` (bài học CLOBBER); notebookId lấy `--notebook` > manifest JSON; nhiều ứng viên → AMBIGUOUS bắt chọn. Ghi qua `_persist_profile_config` (journaled `config_write`). DRY mặc định |
| `tl profile-doctor [--profile-name <p>] [--fix --apply] [--json]` | **(v1.30.0) BẤT BIẾN LAYOUT**: registry+manifest phải TRONG thư mục profile (root/`_meta`) — bắt lạc chỗ (`MISPLACED_ASSET`), Doc-legacy/mime-sai/trashed/thiếu id. `--fix --apply`: move về `_meta` (tạo nếu thiếu; fileId GIỮ NGUYÊN → config không đổi; journal `drive_move`). rc=1 khi có finding |
| `tl profile-index [--rebuild --apply] [--json]` | **(v1.30.0) SỔ CÁI** `Van_ban_thuong/_PROFILES_INDEX` (Google Sheet): cột profile/folder/notebook/registry/manifest/categories/baseAlso — **BẢN CHIẾU từ config** (nguồn sự thật duy nhất vẫn là config). DRY in CSV; `--rebuild --apply` tạo Sheet MỚI rồi trash bản cũ + CSV trung gian (upload không ghi-đè-tại-chỗ; id Sheet ĐỔI mỗi rebuild — mở qua folder) |
| `tl profile-use <name> [--apply]` | **(v1.25)** chọn profile mặc định (ghi `defaultProfile` vào config LOCAL; per-lệnh vẫn override bằng `--profile`). DRY mặc định. KHÔNG đụng Drive/NLM |
| `tl profile-rename <old> <new> [--rename-assets] [--apply]` | **(v1.25)** đổi tên = đổi KEY config; **IDs GIỮ NGUYÊN** (khóa thật). `--rename-assets` đổi CẢ tên hiển thị folder/registry/manifest trên Drive (LIVE). TỪ CHỐI đổi `vbqppl`. DRY mặc định |
| `tl profile-delete <name> [--delete-nlm-sources] [--trash-assets] [--apply --confirm yes]` | **(v1.25) MẶC ĐỊNH detach**: gỡ config (+backup, defaultProfile→vbqppl), **GIỮ Drive+NLM**. `--delete-nlm-sources` xóa nguồn NLM của profile (LIVE) — **GUARD `shared_source_id`**: nguồn dùng chung KHÔNG xóa (báo `nlm_blocked_shared_source_id`). `--trash-assets` trash folder/registry Drive. TỪ CHỐI `vbqppl`; `--apply` cần `--confirm yes`. DRY |
| `tl profile-files [profile] [--nlm/--no-nlm/--corpus/--row-kind/--name]` · `tl profile-manifest [--out f]` | **(v1.25)** `profile-files` liệt kê file trong manifest của profile (lọc); `profile-manifest` load/xuất manifest profile |
| `tl profile-file-add …` (= `profile-ingest`) · `tl profile-file-remove <drive_id…> [--delete-nlm] [--trash-drive] [--keep-registry] [--apply --confirm yes]` | **(v1.25)** thêm/bớt file khỏi profile. Remove: reg-delete + (tùy cờ) nlm delete + drive trash; **GUARD `shared_source_id`** ở nlm delete. DRY mặc định |
| `tl vbhn-check [--subject ... --goc ... --year ...]` | QT-5: dò VBHN theo trích yếu + gốc + năm; không overclaim nếu corpus không có hit. **Khi truyền `--goc`:** ứng viên chỉ trùng CHỦ ĐỀ mà KHÔNG dẫn-chiếu goc → tách sang `uncertain_candidates` (cờ `GOC_NOT_EVIDENT_FILTERED`/`GOC_FILTER_NO_DIRECT_HIT`), KHÔNG coi là kết quả đã lọc theo goc. **v1.24.4:** `--json` có `verdict`+`flags` top-level (vocab nhất quán với source-map: OK/REVIEW/QT5_WEB_REQUIRED/UNKNOWN_NOT_ABSENT) |
| `tl vbhn-verify --text-file/--gdoc-id ... --official-required` | verify nội dung VBHN và chặn bản tự ghép/tạm làm canonical |
| `tl vbhn-normalize [--json]` | **report-only**: đề xuất chuẩn hoá số hiệu/tên/năm VBHN + liệt kê ghost NLM |
| `tl vbhn-year-fix [--with-name] [--apply]` | BẤT BIẾN năm: VBHN sohieu thiếu năm → `NN-YYYY-VBHN-XXX` (reg_upsert); conflicts/needs_year tách riêng |
| `tl sweep [--json]` | **COMPOSITE read-only**: chấm sức khoẻ corpus 1 lệnh (hygiene+cat+slot+drift+vbhn-year+quarantine+**goc_pollution**) + NEXT ACTIONS điền sẵn — thay chuỗi 6 lệnh audit. `goc_pollution` = VBHN có registry.goc nhiễm (gốc rễ §1.1 redirect sai) → sửa goc về `suggested_goc` qua `tl register` (reg_upsert). **(v1.30.1 #7)** in CẢ 2 thước đo corpus trên cùng snapshot: `corpus` (client `corpus=true`) + `corpus_server_rule_equiv` (≈ `boot.corpus_count`: thêm corpus='vbqppl'/overflow, trừ ref/loai='thuong') + tuổi snapshot — boot 527 vs sweep 515 là KHÁC ĐỊNH NGHĨA + snapshot, không phải mất dữ liệu |
| `tl backfill-loai [--normalize] [--apply]` | điền `loai` cho dòng RỖNG (suy từ tên/số hiệu). **(v1.30.1 #4)** `--normalize`: sửa CẢ dòng loai SAI enum map tất định ('Luat'→'Luật', 'nd'→'Nghị định'); giá trị lạ → báo nonmappable, KHÔNG đoán |
| `tl backfill-title-vn [--limit N] [--offset N] [--force-refresh] [--apply]` | **(v1.31.0 P0-1)** điền cột `title_vn` (SẴN CÓ) = TRÍCH YẾU CÓ DẤU đọc từ HEADER thật → QT-5 (`vbhn-check`/`source-map`) suy chủ đề CÓ DẤU thay vì tên file ASCII (query web recall đúng). Đọc header chậm → lô 40 + `--offset` (next_offset in cuối trang); skip loud NO_DIACRITICS/BOILERPLATE (sửa tay `tl register --title-vn`); journaled, undo được. Chạy 1 LẦN sau khi nạp corpus mới. `--force-refresh` đè title_vn là-tên-file (KHÔNG đè trích yếu thật) |
| `tl corpus-fix [--json] [--apply --tier safe]` | **(v1.26) ORCHESTRATOR dọn/chỉnh lý**: gộp mọi detector (sweep) → kế hoạch **THEO THỨ TỰ PHỤ THUỘC** (shared-link→goc→infra→dedup→year→loai→title/cat→nlm-relabel→ingest→consolidation→quarantine — *sai thứ tự = hỏng thêm*) + **2 tầng** (✅safe_auto reversible / 🟡meta / 🔴human / 🏗structural). `--apply --tier safe` chỉ chạy REVERSIBLE (infra+dedup→corpus=false); còn lại in lệnh, người duyệt. DRY mặc định |
| `tl loop [--apply] [--dry-rounds K] [--max-iter N]` | **(v1.28.4 Pha 3) LOOP hợp nhất có cổng-verify + hội tụ + fail-safe**: mỗi vòng detect(infra+dedup an toàn)→`corpus=false`(**verified-write+journaled**)→re-detect đến **HỘI TỤ**; **PAUSE** khi no-progress/verify-hụt/max-iter. `done_ids` trong-phiên (chống NO_PROGRESS giả do GAS cache ~600s). CHỈ tầng reversible → **undo được** (`tl undo <loop_run>`). DRY mặc định |
| `tl source-rename <drive_id\|sohieu> [--name] [--sohieu] [--rename-drive] [--apply]` | **(v1.26)** đổi TÊN nguồn VBQPPL: `reg_upsert` registry.name (+`--sohieu`) + `--rename-drive` đổi CẢ tên GDoc Drive **+ nguồn NLM** (nlm source_rename). Bỏ `--name` = gợi ý tên chuẩn + `ALREADY_STANDARD`. Xoá cache manifest sau ghi. **Verify `header-verify` trước.** DRY mặc định |
| `tl source-update-corpus <drive_id\|sohieu> true\|false [--apply --confirm yes]` | **(v1.26.1) BỎ RA / ĐƯA VÀO corpus**: `false` = reg_upsert corpus=false (**reversible**) + gỡ nguồn NLM (**GUARD `shared_source_id`** — nguồn dùng chung KHÔNG xóa); `true` = đưa vào lại (nhắc `nlm-add`/`ingest` nếu chưa có nguồn). DRY mặc định |
| `tl source-delete <drive_id\|sohieu> [--apply --confirm yes]` | **(v1.26.1) XÓA CỨNG** (bất khả nghịch): gỡ NLM (**GUARD `shared_source_id`**) + trash Drive + xóa dòng registry. **Cân nhắc `source-update-corpus … false` (reversible) TRƯỚC.** DRY mặc định |
| `tl shared-source-fix [<nb>] [--apply --confirm yes]` | **(v1.26) FIXER FALSE-LINK** `shared_source_id` (≥2 drive_id chung 1 nlm_source_id): GIỮ bản điểm cao, `reg_clear` link bản kia (để re-push riêng). **SỬA TRƯỚC** mọi `nlm-reconcile`/xóa nguồn. ⚠ verify `nlm-content <source_id>` xem source thuộc bản nào TRƯỚC `--apply`. DRY/report mặc định |
| `tl consolidation-cleanup [--json] [--apply]` | **(v1.27) Pha sau** — 'có ĐỒNG THỜI VBHN + gốc/sửa đổi RỜI' → GIỮ VBHN, set THÀNH PHẦN corpus=false (**reversible**) khi VBHN phủ **đã verify (on NLM)** + **CORROBORATE goc** (chống goc-pollution: khớp goc nhưng tên VBHN mã hoá base khác/chủ đề xung khắc → **review `GOC_POLLUTION_SUSPECT`**, KHÔNG auto). Component còn NLM → review (gỡ nguồn tay). `--apply` reg_bulk corpus=false CHỈ nhóm ✗ corroborated. Tìm thành phần vẫn ra VBHN (source-map VBHN-first). DRY mặc định |
| `tl corpus-audit [--all\|--sohieu\|--drive-id\|--cat NN] [--limit] [--strict] [--json]` | **(v1.27.1) AUDITOR toàn corpus** — đọc HEADER thật → SO registry → **worklist SỬA XẾP HẠNG** + **lệnh điền sẵn**: 🔴`SOHIEU_MISMATCH`(→`source-rename --sohieu`)/🔴`LOAI_MISMATCH`, 🟠`NAME_TRICH_YEU`(tên hỏng cấu trúc→`source-rename --name`, GUARD boilerplate+chia-sẻ-token, GIỮ năm), 🟡`MISSING_YEAR`(→`vbhn-year-fix`), 🟢`CAT_MISMATCH`(FILL-missing→`recat`). **PROPOSE-ONLY (KHÔNG `--apply`** — sửa qua fixer chuyên dụng). Dùng CHUNG engine với `header-verify --fix-suggest` (nay kèm `suggested_name`+lệnh). Sai-nội-dung = người duyệt. DRY |
| `tl ping --json` / `tl doctor --json` | (1.24.1) xuất JSON máy-đọc cho 2 lệnh khởi động (nhất quán với phần còn lại của CLI) |
| `tl precheck [--cols c1,c2] [--json]` | **(v1.28 Pha 0, write-safety)** kiểm BẤT BIẾN TRƯỚC KHI GHI: `registryDocId`≠Doc-legacy-1mATG · profile-`registryDocId`≠rỗng (**chống CLOBBER 766 dòng**) · snapshot manifest tươi (GAS cache ~600s) · `--cols`∈`REGISTRY_SCHEMA_COLS` (**chống `so_hieu`≠`sohieu` bị bỏ im lặng**). READ-ONLY, rc=1 nếu có blocker. ⚠ KHÁC `preflight` (=định tuyến sharding NLM) |
| `tl journal [<run_id>] [--json]` | **(v1.28 Pha 0)** soi nhật ký WAL `~/.tl_journal/<run>.jsonl`: không tham số=liệt kê run; `<run_id>`=done/inflight + số op undo. READ-ONLY |
| `tl resume <run_id> [--apply]` | **(v1.28.3 Pha 2)** tiếp tục run bị NGẮT — LÀM LẠI op DỞ (intent chưa commit) bằng `set` đã lưu (idempotent, chỉ registry; NLM `source_add` do chạy lại lệnh gốc). DRY mặc định |
| `tl undo <run_id> [--apply --confirm yes]` | **(v1.28.3 Pha 2)** HOÀN TÁC ghi registry của 1 run — khôi phục `before` các dòng đã commit-ok reversible (đúng loại reg_upsert/reg_bulk gốc). ⚠ CHỈ registry — xóa NLM/Drive/reg_clear KHÔNG undo được. DRY mặc định |
| `tl quarantine-fix [--apply]` | **COMPOSITE**: dọn quarantine mâu thuẫn — set corpus=false (raw-dup) + chuẩn nhãn (auto); review_restore (GDoc kẹt) + ghost_nlm chỉ BÁO |
| `tl vbhn-compare --official-text ... --candidate-text ... --focus "Điều 53"` | so bản chính thức với bản tạm/tự ghép, soi footnote và stale-ref ở điều trọng tâm |
| `tl status <sh> [--amendment\|--vbhn] [--targets a,b]` | CỔNG TIỀN-NẠP QT-2 |
| `tl extract <số hiệu\|gdocId> --dieu N` | export ra đĩa + in đúng Điều (token-saving); vị trí nhận cả số hiệu (tự resolve) |
| `tl ingest <fileId> [--apply]` | QT-2 → copy_convert + organize (mặc định DRY) |
| `tl register --drive-id … \| --bulk f.json` | reg_upsert / reg_bulk (khóa `sohieu`, KHÔNG `so_hieu`) |
| `tl manifest [--touched-drive] [--confirm yes]` | kết phiên; profile inherit mặc định export-only, regen2 scope own |
| `tl profile-rebuild-registry --keep-notebook <id>` | phục hồi profile: giữ file trong own-root + notebook + ref; DRY mặc định |
| `tl hygiene scan\|plan\|query\|reconcile` | quét duplicate/orphan/title-mismatch, lập plan QUARANTINE; `--apply --confirm yes` mới move |
| `tl reconcile [query]` | alias của `tl hygiene reconcile`, gom cụm theo số hiệu parse từ tên hoặc md5 |
| `tl registry-doctor [--manifest f.json]` | compat/report-only: phát hiện duplicate/orphan/root rows, không sửa Drive |
| `tl rasoat <keywords\|titles\|worksheet\|phuluc\|orchestrate>` | passthrough script rà soát |

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
Live/post-deploy contract = **2.21.2i** (đã xác minh `ping.version=2.21.2i`, `registry_schema=reg_cols_row_kind_v1`, 27 cột). Bản `.gs` hiện hành = **`references/Code.2.21.2i.gs`**. Tham số/khóa/gotcha MỌI action: **`references/API_CONTRACT.md`**.
- **`references/Code.2.21.2i.gs`:** giữ toàn bộ Cách B/`row_kind` của 2.21.2h, đồng thời thêm `manifestScope=own|inherited`, quét đệ quy đúng `rootFolderId` của profile, giữ nguyên dòng `ref`, và chặn ghi với `PROFILE_MANIFEST_SCOPE_BLOWUP` nếu số dòng own tăng quá `max(2×old, old+50)`.
- **`references/REGEN2_PROFILE_SCOPE_V1.19.5.md`:** quyết định best-combined, khác biệt hai nhánh và quy trình phục hồi an toàn.
- Bản `.gs` đời trước (2.21.1→2.21.2h) ĐÃ đưa ra archive ngoài skill (gọn gói ≤200 file) — chỉ giữ bản LIVE `Code.2.21.2i.gs`; lịch sử/biện luận ở `DOCTRINE_APPENDIX.md` + `CHANGELOG.md`.
- Deploy `Code.2.21.2i.gs` → New version (giữ URL+token), `tl ping` phải ra `2.21.2i`, rồi `contract_check.py --audit`. **KHÔNG deploy từ skill được.**
- Cột registry mới muốn sống qua `regen2` → khai báo `REG_COLS_` + `REG_NLM_KEEP_` trong `.gs` → Deploy → `reg_addcols&confirm=yes`.
- Lịch sử vá: F1–F16c → 2.21.2b; profile-scope guard → 2.21.2i. `API_CONTRACT.md`, `tl.py EXPECT_VERSION`, SKILL/RUNBOOK đồng bộ `2.21.2i`.

## 9. PHỤ THUỘC
`pip install -r requirements.txt`. Cần env `TL_WEBAPP` / `TL_TOKEN` (mirror `tra_luat_config.json`).

### Runtime overlay v1.18.0 — các lệnh bổ sung khi thiếu bộ rasoat đầy đủ
- `--profile <name>` + `tl profile-info --json`: đọc config v2 đa-corpus; VBQPPL là profile nền lấy token/webapp, profile đang dùng quyết định folder/notebook/registry/manifest.
- `tl link-priority <url...> --json`: xếp link tải cho người dùng theo TVPL → LuatVietnam → Công báo → official khác; không đổi canonical official-first.
- `tl slot-audit --notebook-id <id> [--manifest f.json]`: đếm slot theo `nlm_notebook_id`, phát hiện `NOTEBOOK_FULL` giả do registry cũ đếm mọi `nlm_status`.
- Cache manifest tách theo profile: `vbqppl` dùng cache cũ, profile khác dùng thư mục con `~/.tra_luat_cache/<profile>/`.
- `tl extract --sohieu <số hiệu/tên> --dieu N`: tự chọn canonical từ manifest, export text ra đĩa và chỉ in Điều cần xem.
- `tl exists <số hiệu/tên> [--refresh]`: cổng chống overclaim thay cho `reg_get name_contains`; nếu không thấy thì trả `UNKNOWN_NOT_ABSENT` và yêu cầu kiểm tiếp bằng số hiệu/chủ đề/QT-5.
- `tl source-map <số hiệu/tên...> [--refresh]`: sau boot, lập bản đồ nguồn rà soát theo VBHN-first; dùng cho nhóm luật trước khi query/extract thật.
- `tl relation-check --base <số hiệu gốc> --subject <trích yếu> [--amendment <số hiệu sửa đổi>] --json`: quét corpus/NLM để bắt bản sửa đổi đã có nhưng thiếu `goc/sua_doi`; nếu có `missing_links` thì hỏi người dùng ghi registry ngay.
- `tl vbhn-check --subject <trích yếu> --goc <số hiệu> --year <năm>`: cổng QT-5 sau `source-map`; trả query ngoài corpus nếu manifest không có hit.
- `tl vbhn-verify --text-file <txt> --expect-title ... --expect-goc ... --expect-year ... --official-required`: gate nội dung + nguồn chính thức; bản tự ghép/provisional không được chốt canonical.
- `tl vbhn-compare --official-text <txt> --candidate-text <txt> --focus "Điều 53"`: so bản chính thức với bản tự ghép để bắt thiếu footnote, giữ tham chiếu cũ, khác điều trọng tâm.
- `tl instruction-audit --file <instruction.md>`: fail nếu Instruction thiếu `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web`, hoặc còn mở đường `research_import/source_add(url)` nạp thẳng NLM.
- `tl instruction-audit --generate --target <project|nlm|both|config> --print-text`: sinh khối Instruction chuẩn từ `scripts/gen_instructions.py` và tự kiểm.
- `tl locate <số hiệu/tên> [--refresh]`: ưu tiên manifest offline; nếu thấy `WARN=OMNIBUS_NARROW_TITLE_CHECK`, `TITLE_METADATA_MISMATCH`, `ORPHAN_CAT`... thì phải chạy `tl status`/`tl hygiene plan --json` trước khi dùng làm nguồn rà soát.
- `tl hygiene scan`: quét duplicate/orphan/title-mismatch, bắt cả dòng số hiệu rỗng mà `vb_status` không thấy.
- `tl hygiene plan <query>`: chọn canonical theo NLM/cat/số hiệu/hiệu lực và lập danh sách đưa QUARANTINE; với VBHN tái sử dụng số hiệu, cụm được tách theo năm/chủ đề/gốc để không quarantine nhầm văn bản khác; chỉ thực thi khi `--apply --confirm yes`.
- `tl rasoat ...`: nếu thiếu script chuyên sâu thì trả `RASOAT_FALLBACK_PLAN`, không crash.

Overlay độc lập có `_fallback` cho core runtime; các pipeline chuyên sâu `rasoat_*`, `backfill_*`, `registry_orchestrator.py` vẫn thuộc bộ skill đầy đủ. Cài overlay lên base skill để chạy tự động toàn phần; nếu chạy riêng, `tl doctor` sẽ báo thiếu optional thay vì crash.

Ưu tiên dùng `python scripts/tl.py ...`. Nếu cần gọi client tối thiểu thì cú pháp fallback là `python scripts/_fallback/gas.py ACTION key=value`; không dùng cú pháp cũ `gas.py get ACTION`.



### v1.18.0 multi-corpus + link priority + notebook slot guard
- Thêm mô hình `corpus profile`: `vbqppl` giữ webapp/token và corpus pháp điển; `vbthuong`/profile dự án có folder, notebook, registry, manifest riêng. `--profile`/`TL_PROFILE` overlay config v2.
- Khi tra cứu ở profile P: manifest/registry P trước, miss mới fallback VBQPPL; QA xuyên corpus dùng `cross_notebook_query` với notebook P + VBQPPL, canonical của P thắng.
- Link tải cho người dùng ưu tiên TVPL/LuatVietnam/Công báo vì tiện tải Word/PDF và xem hiệu lực; canonical lưu/đối chiếu vẫn official-first.
- `slot-audit` và tài liệu .gs yêu cầu `nlm_slots/nlm_preflight` đếm theo `nlm_notebook_id == notebookId`, sửa lỗi `NOTEBOOK_FULL` giả.
- Tài liệu chi tiết: `references/MULTI_CORPUS_PROFILE_V1_18.md`.

### v1.17.25 external-ingest + Instruction gate
- Từ log Nghị định 129/2025: không được nạp thẳng PDF vào notebook tạm bằng `research_import`/`source_add(url)`. `research_*` chỉ discovery; nguồn mới phải đi QT-3 rồi mới `nlm_push`.
- Thêm `scripts/gen_instructions.py` thật, không còn chỉ nhắc trong tài liệu. Output mọi target có `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web`, official-first, ưu tiên docx/GDoc, và mặc định notebook đang dùng.
- Thêm `tl instruction-audit` để kiểm Instruction/Project prompt; selftest fail nếu thiếu các khối bắt buộc.
- Tài liệu chi tiết: `references/EXTERNAL_INGEST_GATE.md`.

### v1.17.24 amendment gate best-combined
- Hợp nhất thêm nhánh `amendment existence gate`: `source-map` tự quét `amendment_candidates` theo chủ đề/dấu hiệu "sửa đổi", kể cả khi registry thiếu `goc/sua_doi`.
- Nếu phát hiện bản sửa đổi liên quan, `source-map` trả `AMENDMENT_CANDIDATE_IN_CORPUS`, `UNLINKED_AMENDMENT_CANDIDATE`, `VBHN_RECHECK_REQUIRED`, `PAUSE_AND_ASK_USER`; phải dừng và hỏi người dùng trước khi rà tiếp.
- Thêm `tl exists` để kiểm tra hiện diện bằng `source-map` chuẩn hóa; không còn phải dùng `reg_get name_contains` thô.
- `tl vbhn-check --goc <số hiệu>` tự suy trích yếu từ manifest nếu không truyền `--subject`, để sinh query kiểu `"luật thi đua khen thưởng" "hợp nhất"` và `site:thuvienphapluat.vn ...`.

### v1.17.22 stale relation guard
- Từ log Luật Thi đua, khen thưởng: không được kết luận văn bản sửa đổi/VBHN vắng mặt chỉ vì `vb_status` thiếu quan hệ; có thể văn bản đã ở corpus/NLM nhưng registry trống `goc/sua_doi`.
- Thêm `tl relation-check` để quét theo số hiệu gốc + chủ đề + số hiệu sửa đổi đã biết; nếu phát hiện bản sửa đổi đã có, trả `RELATION_BACKFILL_REQUIRED` và hành động `BACKFILL_SUA_DOI_ON_BASE`/`BACKFILL_GOC_ON_AMENDMENT`.
- `tl vbhn-check`/`relation-check` gợi ý cả query web đơn giản như `"luật <chủ đề>" "hợp nhất"` và `site:thuvienphapluat.vn ...`; nguồn secondary chỉ để phát hiện nhanh, canonical vẫn official-first.
- Tài liệu chi tiết: `references/STALE_RELATION_GUARD.md`.

### v1.17.17 merge hardening
- Giữ nền `v1.17.15-vbhn-hygiene-guards` và bổ sung lại `tl vbhn-normalize --json` để report-only các việc cần backfill/rename VBHN và ghost NLM.
- Chặn lỗi tên rỗng match mọi query: mọi so khớp tên phải yêu cầu `nk` không rỗng; tránh NLM ghost lọt vào `locate/source-map/hygiene plan`.
- `_goc_keys` xử lý đúng `goc` dạng list/dict; khóa hygiene VBHN sạch hơn khi manifest lưu nhiều số hiệu gốc.
- `registry_hygiene.py` đồng bộ flag với `tl.py`: `VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH`, `VBHN_NAME_MISSING_YEAR`, `NLM_GHOST_SOURCE`.

### v1.17.19 VBHN cấp Bộ phải có năm
- Từ log "lô 33 đổi tên": VBHN cấp Bộ (`NN/VBHN-BYT`, `05/VBHN-BGDĐT`, `2279/VBHN-BLĐTBXH`...) cũng là VBQPPL, không được để tên/metadata thiếu năm.
- `tl.py` và `registry_hygiene.py` nhận diện số hiệu VBHN cấp Bộ, gắn `VBHN_MINISTRY_SCOPE`, `VBHN_MINISTRY_MISSING_YEAR`, `VBHN_MINISTRY_NAME_MISSING_YEAR` để đưa vào `title_mismatch_candidates`.
- `tl vbhn-normalize --json` report-only mẫu tên riêng cho cấp Bộ: `VBHN_<so>-VBHN-<co_quan>_<year>_<ten_rut_gon>`; thiếu `issue_year` thì bắt backfill từ dòng ngày ban hành trước khi rename.
- Không quarantine/move văn bản cấp Bộ theo số hiệu trần; phải verify năm + chủ đề + nội dung, vì số hiệu cấp Bộ cũng có thể tái dùng theo năm.

### v1.17.15 VBHN hygiene/source-map guard
- Chuẩn hóa runtime số hiệu VBHN VPQH thiếu đoạn `VBHN`: `19-VPQH`/`40-VPQH` được xem như `19-VBHN-VPQH`/`40-VBHN-VPQH`.
- Sửa parser năm trong tên có underscore (`_2024_`, `_2026_`), tránh cảnh báo sai `VBHN_MISSING_YEAR_OR_DATE`.
- `hygiene` không còn gom VBHN theo số hiệu trần; tách theo số hiệu + năm/chủ đề/gốc/md5 để không quarantine nhầm các văn bản khác cùng số.
- Hạ điểm nguồn NLM rỗng metadata (`NLM_GHOST_SOURCE`) và tách file `.docx/.pdf` gốc cạnh GDoc thành `sidecar_source_files`, giảm báo động giả.
- Tài liệu chi tiết: `references/VBHN_HYGIENE_GUARDS.md`, `references/VBHN_MINISTRY_YEAR_GUARD.md`.


### v1.17.14 VBHN official-first gate
- Từ log ATVSLĐ: bản tự ghép VBHN có lỗi quy phạm ở Điều 53 và thiếu footnote; từ nay không tự ghép VBHN làm bản dùng.
- Thêm `tl vbhn-verify --official-required` và `tl vbhn-compare` để chặn/chứng minh khác biệt giữa bản chính thức và bản tạm.
- Quy trình khi thiếu VBHN: hỏi người dùng nạp file chính thức vào `_HOP_NAP`; nếu buộc dựng bản tạm để phân tích thì gắn provisional, không add NLM/canonical, và quarantine khi có bản chính thức.
- Tài liệu chi tiết: `references/VBHN_OFFICIAL_FIRST.md`.


### v1.17.13 VBHN QT-5 verification gate
- Hợp nhất bản `vbhn_qt5`: thêm `tl vbhn-check`, `tl vbhn-verify`, `tl vbhn-check --scan`.
- Giữ guard v1.17.12: `NO_VERIFIED_VBHN_IN_CORPUS`, `VBHN_NUMBER_REUSE_RISK`, `VBHN_BARE_NUMBER`, `VBHN_MISSING_YEAR_OR_DATE`.
- Quy trình bắt buộc với luật đã sửa đổi: `source-map → vbhn-check → vbhn-verify → mới chốt nguồn rà soát`.
- Tài liệu chi tiết: `references/VBHN_QT5_VERIFICATION.md`.


### v1.17.12 VBHN year/reuse guard
- Không kết luận "không có VBHN" từ manifest/corpus. Khi không thấy VBHN đã xác minh, `source-map` trả `NO_VERIFIED_VBHN_IN_CORPUS` + `QT5_WEB_REQUIRED` và gợi ý query theo trích yếu/chủ đề + "hợp nhất".
- Số VBHN có thể tái sử dụng theo năm; hit theo `14/VBHN-VPQH` phải verify ngày ban hành + tiêu đề + dòng "được sửa đổi, bổ sung bởi..." trước khi tin.
- `hygiene/registry-doctor` gắn `VBHN_BARE_NUMBER`, `VBHN_MISSING_YEAR_OR_DATE` cho VBHN tên trơ/thiếu năm, để bắt kiểu `VBHN_14-VBHN-VPQH`.


### v1.17.11 best-combined source-map
- Hợp nhất `source-map hotfix` với runtime-log hardening: `source-map` chọn VBHN liên quan qua trường `goc`, vẫn xuất `WARN`/`risky_candidates` từ `_title_flags`.
- `_entry_score` đồng bộ hơn với `registryRank_` 2.21.2b: cộng điểm VBHN như tiebreaker, trừ điểm bản hết hiệu lực/thay thế.
- Tài liệu chi tiết: `references/REALRUN_4LAWS_SOURCE_MAP_FIXES.md`.


### v1.17.10 post-run hardening
- Từ log chạy thật: `locate/hygiene/registry-doctor` nay phát hiện nhãn tên hẹp nhưng quan hệ sửa nhiều luật (`OMNIBUS_NARROW_TITLE_CHECK`) và mismatch tên-metadata, tránh chọn nhầm kiểu `Luat_57-2024-QH15_Bao_hiem_y_te`.
- `tl locate` nhận `--refresh/--debug`, ưu tiên manifest đầy đủ trước webapp `find` để thấy metadata/cờ cảnh báo.


### v1.17.9 hotfix
- Khép version post-deploy `2.21.2b` trong CLI/contract/SKILL/RUNBOOK.
- Thêm `requirements.txt` rỗng-phụ-thuộc để lệnh cài đặt trong tài liệu không lệch thực tế.
- `tl extract --find` tìm chuỗi sau Unicode NFC normalize, tránh âm tính giả khi grep tiếng Việt có dấu.
- `tl hygiene/reconcile` không parse tên `Mẫu_*/PL_*` thành số hiệu văn bản, tránh QUARANTINE nhầm phụ lục/biểu mẫu làm việc.


### v1.17.19 safe issue_year parser
- (Lịch sử) parser `issue_year` an toàn (từ bản 2.21.2d) — logic này tiếp tục được giữ trong `Code.2.21.2i.gs`.

### v1.17.20 registry hygiene parity
- Đồng bộ `registry_hygiene.py` với parser an toàn của `tl.py`: không lấy năm từ `tukhoa/keywords/trich_yeu`, tránh làm mất cờ `VBHN_MISSING_YEAR_OR_DATE` khi chạy hygiene độc lập.
- Tên VBHN phải chứa đúng năm ban hành đã xác định; năm của văn bản gốc trong tên/keyword không được coi là đạt.
- (Lịch sử v1.17.20) parser năm an toàn ở server-side; bản target/EXPECT hiện hành là `2.21.2i`.

### v1.17.21 lessons hardening
- Không dùng `reg_get name_contains` để kết luận văn bản vắng mặt; phải chạy ít nhất `tl source-map <tên/chủ đề>` và `tl locate/status <số hiệu>`.
- `_fallback/gas.py` cảnh báo khi gọi `reg_get name_contains`; `hygiene scan` có thêm `duplicate_identity_groups`, `duplicate_sohieu_groups_raw`, và cờ `NLM_STATUS_MISMATCH`.


## v1.17.26 combined external-ingest + instruction-audit gate

- Trước mọi nạp nguồn web/NLM-native, chạy `tl external-ingest <url> ... --json` để kiểm kế hoạch. Lệnh này chỉ kiểm, không ghi Drive/NLM.
- `research_start/research_status` chỉ dùng để phát hiện URL; `research_import/source_add(url)` không được dùng để nạp VBQPPL làm nguồn canonical.
- Instruction dùng cho Claude Project/NLM phải qua `tl instruction-audit` hoặc sinh bằng `tl instructions`/`scripts/gen_instructions.py`; thiếu `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web` thì không dùng.
