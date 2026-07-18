# tra-luat — KERNEL APPENDIX (trích NGUYÊN VĂN từ kernel — G1b v1.34.67)

> Nếp Pha F: kernel = bất biến + con trỏ. 3 khối dưới **trích NGUYÊN VĂN** từ SKILL.md (v1.34.66),
> nội dung KHÔNG đổi, **hiệu lực như kernel** — kernel giữ mệnh lệnh tóm + con trỏ về đây.
> (Khi mâu thuẫn: LÕI + API_CONTRACT + RUNBOOK thắng phụ lục — riêng 3 khối này LÀ lõi chuyển chỗ.)

## §A — COWORK: chi tiết đường tải-về (artifact public / curl-route / ⛔ bẫy NPM-GLIBC gws)
(nguyên văn từ kernel §1 KHỞI ĐỘNG)

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

## §B — COWORK TIMEOUT 45s/lệnh: tách bước nlm-install --resume (chi tiết uv/tarball/bwrap/temp)
(nguyên văn từ kernel §1 — mục 'THIẾU config/token' bước 1)

>    ⚠ **COWORK TIMEOUT 45s/lệnh:** `--nlm` (uv/nlm-install) THƯỜNG vượt 45s → TÁCH BƯỚC: `sh tl_fetch.sh --setup` (core <45s, KHÔNG nlm) → rồi **LẶP `tl nlm-install --resume` tới rc=0** (★v1.30.1 #1: mỗi lần gọi chạy ĐÚNG 1 bước fetch→extract→install, trạng thái dò từ đĩa — tarball bền + uv cache; rc=3=PARTIAL còn bước, KHÔNG phải lỗi; thường ≤5 lần) → `tl nlm-auth-load` riêng. KHÔNG dùng nohup/setsid vờ chạy nền — bwrap --unshare-pid kill tiến trình con giữa 2 lần bash. `tl up` (không --nlm) ~30s. Mount Cowork cắt cụt → curl zip sạch TRƯỚC (BƯỚC 0). Temp ghi `$HOME` (1.23.15 tự trỏ TMPDIR khỏi /tmp).

## §C — Sharding VBQPPL: topology declared+observed, capacity, failover, push-overflow, recovery
(nguyên văn từ kernel §1)

**Sharding VBQPPL (cap mặc định 300/notebook — cấu hình được):** corpus VBQPPL trải NHIỀU notebook (shard); mỗi dòng registry mang `nlm_notebook_id` + `row_kind ∈ {own,ref,overflow}`. **(v1.34.49) TOPOLOGY = declared+observed hợp nhất, MỘT resolver cho mọi lệnh**: `config.profiles.vbqppl.shards[]` (dict `{id,role,capacity,enabled,priority}` hoặc list id legacy) là Ý ĐỊNH khai báo; registry+env là QUAN SÁT; alias (`overflowNotebookId`) lệch declared → lệnh ghi/route DỪNG fail-closed `TOPOLOGY_CONFIG_CONFLICT`. Capacity per-shard: `shards[].capacity` > env `TL_NLM_SOURCE_CAP` > 300; live count là ground truth. Nạp VBQPPL mới ⇒ `tl preflight <số hiệu>`: shard chính đầy → `overflow_route` shard phụ. Batch `ingest-missing` tự **failover shard kế TRONG CÙNG RUN** khi shard đầy giữa chừng (không upload lại); CẠN mọi shard → `partial=true + remaining + resume_command + rc=2` (KHÔNG còn "ok" giả — kể cả blocked upfront). Đọc slot LIVE fail-closed: auth-fail ⇒ `LIVE_READ_FAILED` DỪNG trước side-effect, KHÔNG coi là 0 nguồn. Sau `source_add` tay vào shard phụ ⇒ `tl push-overflow --drive-id --source-id` (set `row_kind=overflow`; validate đích ∈ topology). Recovery `nlm-reconcile --apply`/`nlm-add` nay tự ghi `row_kind` theo topology (kind `ref`/`thuong` không bao giờ bị clobber); doctor kiểm bất biến notebook↔row_kind (report-only). Tra cứu xuyên shard: registry/manifest hợp nhất + **`tl nlm-cross "<câu hỏi>"`** (mặc định TOÀN topology enabled; thay MCP `cross_notebook_query`). KHÔNG `notebook_create` mới trừ khi tất cả shard đầy + người dùng duyệt.
