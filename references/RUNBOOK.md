# tra-luat — RUNBOOK KHỞI ĐỘNG (tất định, đánh số)

> Thay cho doctrine rải rác trong văn xuôi. Mỗi bước là MỆNH LỆNH + cổng (gate). Làm đúng
> thứ tự. Tham số/khóa response webapp: tra `references/API_CONTRACT.md` — KHÔNG đoán.
> Bẫy vận hành ĐÃ TRẢ GIÁ (nhóm theo chủ đề, trích từ CHANGELOG/hồ sơ sự cố): `references/GOTCHAS.md`
> — đọc TRƯỚC khi release / sửa registry / viết script mới / move-tách module (G2 v1.34.66).
> Kiểm chứng hệ checkpoint (precheck-gate + WAL + resume/undo) trên LIVE: `references/CHECKPOINT_TEST_PLAN.md`.
> Bootstrap Cowork nhanh — Project + direct-media, né Drive MCP: `references/COWORK_PROJECT.md`.
> (r228: hai dòng trên là CON TRỎ SỐNG bắt buộc — trong gói cài, sổ lưu trữ không đi theo,
> tài liệu chỉ được lịch sử trỏ sẽ MỒ CÔI thật và L9 nổ cờ đúng.)

---

## 0. NGUYÊN TẮC BẤT BIẾN (không bao giờ bỏ)

1. **VBHN-first** — có VBHN còn hiệu lực thì nạp/tra VBHN, không dùng bản gốc/bản sửa đổi rời.
2. **Verify nguyên văn** — điều khoản trả người dùng phải lấy từ cache/raw đã xác minh; NLM chỉ
   định vị + tổng hợp, KHÔNG nhận RAG làm nguyên văn.
3. **Không bịa** — thiếu dữ liệu → nói "không có" / REVIEW, không suy đoán.
4. **Dedup nhiều lớp** — cache → registry → NLM, theo số hiệu + biến thể + text_hash.
5. **ĐỐI CHIẾU NGAY** — khi cần đối chiếu với văn bản ĐÃ CÓ trong corpus: chạy đối chiếu NGAY
   hoặc HỎI để quyết ngay. KHÔNG gác vào Mục F/ghi chú. Mục F chỉ cho việc thực sự bị chặn.
6. **Tên NLM = tên Drive** — đổi tên thì đổi đồng bộ GDoc + file gốc + registry + nlm_title + source NLM.
7. **Research discovery-only** — `research_start/research_status` chỉ phát hiện URL. Cấm `research_import`/`source_add(url)` nạp thẳng VBQPPL vào NLM; nguồn mới phải đi QT-3 rồi mới `nlm_push`.
8. **Corpus profile** — đọc config VBQPPL trước để lấy webapp/token, rồi overlay `TL_PROFILE`/`--profile`; văn bản thường dùng folder/notebook/registry/manifest riêng.
9. **Slot theo notebook** — `nlm_slots/nlm_preflight` chỉ đếm rows có `nlm_notebook_id == notebookId`.
10. **categories=inherit** — chỉ dùng cây category VBQPPL để ORGANIZE/tra cứu fallback; không populate registry/manifest profile.

---


## A-DET. CỔNG DETERMINISM / OCR / IDEMPOTENCY (trước khi ghi hoặc release)

**A-DET.1 — OCR sidecar không đủ; phải có manifest.**
```bash
python scripts/tl.py ocr-run <file> --engine auto --mode vbqppl --json
python scripts/tl.py ocr-verify <text_file.ocr.txt> --source <file> --mode vbqppl --json
```
- `ocr-run` phải tạo `ocr_manifest.v1` cạnh `.ocr.txt`.
- `ocr-verify` phải kiểm `source_sha256`, `text_sha256`, engine/version/language, page report/coverage nếu là PDF, Điều/Phụ lục, mật độ dấu tiếng Việt và garbled ratio.
- VBQPPL OCR thiếu manifest verified ⇒ **DỪNG**, không canonical.

**A-DET.2 — Lệnh ghi phải có idempotency contract.**
```bash
python scripts/tl.py route-task --task ingest_zip --json
python scripts/tl.py route-task --task ocr_ingest --json
python scripts/tl.py route-task --task profile_ingest_chunks --json
```
Bắt buộc đọc 4 trường: `idempotency_key`, `resume_command`, `readback_command`, `rollback_hint`. Timeout giữa chừng ⇒ dùng resume/journal/readback; không tự viết script vá tay.

**A-DET.3 — Release cuối.**
```bash
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic determinism-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py --deterministic release-check --strict-determinism --full --json
```
Release pass offline chưa phải live ready. Live vẫn cần `live-readiness`, `live-contract-check`, snapshot before/after và `live-state-diff`.

---

## A0. BOOT TRANSPORT `gws` (3-env — Code/Cowork; Chat SKIP)

> **GĐ0.** `gws` (`@googleworkspace/cli`) = transport Drive direct-API cho Code/Cowork (**PRIMARY**), GAS = **FALLBACK**.
> Chat KHÔNG có shell/binary → transport = **Drive MCP**; **BỎ QUA §A0**. Chạy §A0 TRƯỚC §A khi phiên cần thao tác Drive.

**A0.1 — Cài + PIN version (KHÔNG `latest`).** gws pre-v1.0 hay breaking → ghim chính xác bản đã kiểm.
```bash
npm i -g @googleworkspace/cli@0.22.5     # PIN = tl.py GWS_PINNED_VERSION (nguồn-chân-lý)
gws --version                            # phải in: gws 0.22.5
```

**A0.2 — Cổng boot `tl gws-ping`** (đối xứng `tl ping` của webapp; env-aware).
```bash
python scripts/tl.py gws-ping            # env tự dò; ép bằng --env code|cowork|chat ; --json để máy đọc
```
- `rc 0` = SẴN SÀNG (PATH + version==pin + đã auth) **HOẶC** `env=chat` (SKIP, transport Drive MCP).
- `rc 3` = gws lệch pin / **CHƯA auth** (xem `issues`). `rc 4` = gws thiếu PATH / không chạy.
- **Cổng:** ngoài Chat mà `rc != 0` ⇒ CHƯA được thao tác Drive qua gws; sửa xong mới sang §A.

> **NHẬN DIỆN ENV (quan trọng — bài học Cowork 26/6):** `transport.runtime_env` chạy trong shell ⇒ heuristic
> **KHÔNG bao giờ tự trả `chat`** (chat thật không chạy `tl.py`). Thứ tự: `--env` → `TL_RUNTIME_ENV` → marker
> Code (`CLAUDECODE`…) → marker Cowork (`COWORK`…) → **mặc định `cowork`**. Sandbox Cowork KHÔNG set `COWORK`
> vẫn ra `cowork` (gws→GAS), không SKIP nhầm. Ép khi cần: `export TL_RUNTIME_ENV=code|cowork|chat`.
> Cowork **chưa cài gws** vẫn DÙNG ĐƯỢC: op A/B/C tự `[FALLBACK→GAS]` (chỉ `upload` cần gws). Muốn đi đường
> Drive MCP như Chat: `export TL_RUNTIME_ENV=chat`.

> **⚠ BẪY gws thao tác GHI trực tiếp (`gws drive files update` — log phiên Chỉ thị 2026-07-13):** `--params`
> CHỈ nhận **query params**; REQUEST BODY (vd `{"trashed":true}`) PHẢI qua `--json`. Truyền body nhầm chỗ →
> HTTP 200 "thành công" nhưng KHÔNG đổi gì (**im lặng thất bại**). Mọi write qua gws trần PHẢI readback
> (`files.get`) xác minh field đã đổi — hoặc tốt hơn: dùng lệnh `tl` tương đương (đã bọc verified-write).

**A0.3 — Auth (KHÔNG service-account — SA vỡ ownership folder My-Drive; dùng EXPORTED USER CREDENTIAL).**
- **Code** (có trình duyệt): `gws auth login` (OAuth tương tác) → `gws auth status` thấy `auth_method != "none"`.
- **Cowork** (headless): KHÔNG login được → NẠP credential đã xuất từ Code (A0.4).
- **Chat**: N/A — Drive MCP dùng connector claude.ai.

**A0.3b — Cài gws trên COWORK sandbox (chặn github + no root) bằng 1 LỆNH.**
npm postinstall của gws tải binary từ github (bị chặn trong Cowork) + cần root → KHÔNG cài thường được. Cách
vòng: dùng binary **MUSL-STATIC** stage sẵn trên Drive `_HOP_NAP` (static → chạy MỌI glibc; bản **gnu** cần
GLIBC_2.39 nên KHÔNG chạy trên Ubuntu 22.04/glibc 2.35). Helper tải qua webapp `download` (b64 decode THẲNG
xuống đĩa, KHÔNG vào context Claude) → md5 → chmod +x → `~/.local/bin/gws`:
```bash
python scripts/tl.py gws-bootstrap-cowork           # 1 lệnh: tải musl → verify md5 → chmod → đặt vào bindir
export PATH="$HOME/.local/bin:$PATH"                 # nếu helper báo cần
python scripts/tl.py gws-ping --env cowork           # sau khi nạp credential (A0.4) → rc 0
```
> Mặc định trỏ bản `x86_64-musl` (hằng `GWS_COWORK_FILEID`/`GWS_COWORK_MD5` trong tl.py). Arch khác
> (`aarch64`) → stage bản tương ứng rồi `gws-bootstrap-cowork --file-id <id> --md5 <hash>`. Cap webapp
> `download` = 9MB (musl ~6.9MB, đạt). Cowork ephemeral → chạy lại helper mỗi phiên (~10s).

**A0.4 — Mang credential Code → Cowork (export flow).** Trên Code (đã login), in credential đã giải mã:
```bash
gws auth export --unmasked
```
> Chuyển hướng stdout của **lệnh export** thành file `credentials.json` (toán tử `>` của shell). secret_guard CHẶN khi
> **lệnh export** đi kèm `>` hoặc pipe trên CÙNG dòng (chống lộ) → chạy redirect ở shell KHÔNG bật hook, rồi mang file sang Cowork.

Trên Cowork, trỏ env tới file rồi xác minh:
```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/duong/dan/credentials.json
python scripts/tl.py gws-ping --env cowork       # phải rc 0
gws drive files list --params '{"pageSize":1}'   # khói: trả 1 file (JSON)
```
> **Cú pháp gws (v0.22):** `gws <service> <resource> <method> --params '{JSON}'` — KHÔNG `key=value`. `--format json` mặc định; `--page-all` để phân trang.

**A0.4b — AUTO-AUTH zero-setup (cred MÃ HOÁ trên Drive — KHUYẾN NGHỊ thay A0.4 thủ công).**
Cred gws được **mã hoá** (khoá dẫn xuất PBKDF2 từ **webapp token** — secret skill đã có trong config) rồi lưu
Drive `_HOP_NAP` (KHÔNG plaintext, KHÔNG trong zip). Mỗi phiên Cowork tự tải+giải mã → `~/.config/gws/
credentials.json`, gws tự dùng (không cần env). Bản giải mã chỉ tồn tại trong sandbox ephemeral.
```bash
# [CODE] 1 lần (hoặc khi refresh_token đổi): export → mã hoá → upload, in fileId để baked vào GWS_CRED_FILEID
python scripts/tl.py gws-auth-stage
# [COWORK] mỗi phiên — gộp luôn trong bootstrap (binary + cred 1 lệnh):
python scripts/tl.py gws-bootstrap-cowork        # cài gws musl + tải/giải mã cred → credentials.json
export PATH="$HOME/.local/bin:$PATH"
python scripts/tl.py gws-ping --env cowork        # auth=ok → rc 0 (KHÔNG cần mang file tay)
```
> Bảo mật: cred được bảo vệ NGANG webapp token (master secret của skill). Ai có webapp token đều giải mã được
> — đúng ranh giới tin cậy hiện có; KHÔNG thêm secret mới trong zip. Crypto = `gws_cred_store.py` (stdlib:
> PBKDF2 + HMAC-SHA256-CTR encrypt-then-MAC). Muốn tách bạch hơn → quay lại A0.4 (mang `credentials.json` tay).
> Nạp riêng: `tl gws-auth-load`; bỏ qua auto-auth: `gws-bootstrap-cowork --no-auth`.

**A0.4c — UNIFIED bootstrap: GAS token + GWS cred chung 1 khoá gốc `TL_MASTER_KEY` (env-aware).**

> Phiên ephemeral có một entry point secret-safe cho Codex, Claude subscription,
> GitHub và việc điều phối bootstrap hiện hữu: xem `docs/SESSION_CREDENTIALS.md`.
> Mọi đích ghi secret (`CODEX_HOME/auth.json`, `claude-capture --output`) phải resolve
> ra ngoài repository, kể cả qua parent symlink; hook kiểm `CODEX_HOME` trước mọi lần
> gọi Codex, kể cả khi `codex login status` sẽ báo đã đăng nhập. Từ chối sẽ đặt
> `TRA_LUAT_CODEX_BLOCKED=1`; launcher phải giữ chốt đó qua mọi đường Codex, kể cả
> generic `run -- codex`. Generic run resolve/bind executable identity đúng một lần,
> kể cả alias symlink/reparse đổi tên hoặc hard-link cùng file. argv0 tương đối có thành phần
> đường dẫn được neo vào workspace đã khai **trước mọi PATH lookup**; chỉ tên lệnh trần mới dùng
> PATH/PATHEXT. Provider child từ generic run chỉ nhận credential của chính provider và PATH
> sanitized; credential ambient của provider khác không được kế thừa, còn generic non-provider
> giữ contract môi trường cũ. Sau đó dùng cùng bound target
> cho chốt Codex, transport record, capability probe và final spawn; identity không resolve
> được hoặc mơ hồ thì fail trước child. Writer giữ **actual opened parent
> capability** đã kiểm và làm toàn bộ create/chmod/fsync/replace tương đối với capability
> ấy; không quay lại đường dẫn. Riêng shared session credential writer giữ identity của inode
> ngay sau `O_CREAT|O_EXCL`, trước chmod/write/flush/fsync. Lỗi về sau của shared writer,
> kể cả mọi lỗi parent-directory fsync (`EINVAL`/`ENOTSUP`/`EIO`) sau replace, chỉ
> được xoá entry còn đúng identity đó; replacement khác inode phải sống và exception gốc
> không bị cleanup che. Exceptional unwind phải thử đóng hết descriptor còn sở hữu; close/unlink
> phụ không được thay exception write/durability đầu tiên, nhưng close hỏng khi trước đó chưa có lỗi
> vẫn là failure. Trên POSIX writer bắt đầu từ trusted root fd, mở từng
> component đã có và tạo từng component còn thiếu tương đối với directory fd đang giữ;
> không `mkdir` theo pathname rồi reopen. Cả writer session và writer NLM/GWS đều fail
> trước khi ghi byte secret nếu một missing component bị thay bằng symlink. Bảo đảm này
> chặn việc đổi alias sang thư mục KHÁC, không
> bao gồm actor có quyền reparent chính directory inode đã mở sau validation; capability
> sẽ đi theo inode ấy, nên threat model mạnh hơn phải dùng confinement/quyền của OS.
> POSIX có primitives cần thiết; Windows thiếu primitives tương đương thì fail closed
> trước child/write và báo `not_measured`. Hai lệnh TL bắt buộc
> `--secrets-file`; entry point từ chối bundle trong repository, kiểm/canonicalize
> chính candidate và mọi ancestor của HOME/XDG/GWS/cache/temp mà TL child có thể ghi
> (exact worktree/bare root và link/junction alias bị từ chối; external root chưa tồn tại
> vẫn được canonicalize rồi giao child), rồi neo child vào `scripts/tl.py` và
> cwd của chính repository. Claude capture/probe, GitHub probe và Codex device-auth/live-check
> chỉ dùng hierarchy private do process tạo từ trusted OS temp base (`/tmp` hoặc Windows
> Shell LocalAppData, không theo ambient `TMPDIR`/`TMP`/`TEMP`). Child bị bind `HOME`, mọi
> XDG root và cả ba temp vars vào hierarchy đó; permission/repository/symlink/reparse không
> kiểm chắc được thì fail trước child. Cleanup quarantine rồi đối chiếu đúng identity root đã cấp,
> kiểm lỗi xoá và residual; root bị đổi thành link/junction/reparse không được đưa cho recursive
> delete. Cleanup raise hoặc còn residual luôn hạ kết quả thành `not_measured`, kể cả inner call vừa
> định trả thành công. Chốt này không chống actor đồng thời cùng OS principal
> có quyền reparent hierarchy đã tạo; threat model mạnh hơn phải dùng namespace/principal
> confinement của OS trong lúc child còn đang dùng storage. Riêng Codex live-check guard +
> capability-read `CODEX_HOME/auth.json` trước khi cấp provider storage hoặc spawn; direct repository
> và parent-link từ chối với zero child. Kết quả đóng gồm `passed`/`rejected`/`not_measured`: thiếu CLI,
> timeout, local spawn/provider/cleanup không đo được là `not_measured`; chỉ refusal credential/model
> có bằng chứng ngữ cảnh đóng (hoặc policy refusal) là `rejected`; từ local trần `login`/`oauth`/
> `authentication` và số trần `401`/`403` không phải refusal evidence. Với Claude, nonzero chỉ là `network_error`
> khi stderr/stdout có bằng chứng transport cụ thể (connection reset/refused, DNS...); lỗi local
> hoặc nonzero không phân loại được là `not_measured`; rc `0` thiếu marker thành công standalone chính xác
> cũng là `not_measured`, không phải approve. GitHub chỉ coi HTTP 401/403/404 là `rejected` khi cùng response
> header section có `X-GitHub-*`; body line, proxy/local output và block khác không được cấp bằng chứng.
> Timeout của `gh` không kèm bằng chứng transport-failure độc lập là `not_measured`, không phải
> `network_error`. `tl-bootstrap` giữ nguyên contract rc của
> child: `0→passed`; `1→not_measured/degraded`; `2→not_measured/precondition`;
> `3→rejected/credential_or_bundle_rejected`; rc khác `→not_measured/unclassified_exit`.
> Credential directory đã validate chỉ làm
> `CODEX_HOME`, còn `HOME`/XDG/temp nằm trong một hierarchy private tách biệt; credential
> directory thường chỉ có `auth.json` không cần provider-home scaffold. Đường device-auth
> `lay` không nhận `CODEX_HOME` từ caller và chỉ copy-out bằng guarded writer; cleanup hỏng ghi đè
> một kết quả inner ĐẠT thành KHÔNG_ĐO_ĐƯỢC. NLM restore chỉ
> nhận đúng `auth.json`, `profiles/default/cookies.json`, và
> `profiles/default/metadata.json`; traversal/extra profile bị từ chối. Base hoặc existing lexical
> parent là link/junction/reparse (kể cả resolve ra external non-repository) bị từ chối trước schema
> planning; mọi generated target parent được kiểm hết trước lần ghi đầu tiên. Component thường chưa
> tồn tại vẫn được phép để guarded writer tạo.
>
> Trước khi đọc token/token-file, Claude capture/probe và GitHub probe resolve provider từ duy nhất
> các raw PATH entry vốn đã tuyệt đối, loại entry rỗng/tương đối/tilde-relative mà không expand `~`
> hay hỏi ambient `HOME`, loại repository và process-trusted temp, rồi yêu cầu đúng một candidate.
> POSIX cho phép symlink alias tới regular executable, nhưng shebang phải resolve thành interpreter tuyệt đối
> đã bind (kể cả `#!/usr/bin/env node` chỉ khi có đúng một `node`). Windows chỉ dò `.com/.exe/.bat/.cmd`;
> `.cmd` chỉ được nhận khi đúng npm shim và bind được cả `node.exe` lẫn JS entry, rồi launch hai file tuyệt đối
> ấy trực tiếp; script/shim khác fail closed. Provider và mọi launch-support identity đều được kiểm lại ngay
> trước spawn; argv0 và PATH child đều tuyệt đối/sanitized. Candidate/support thiếu, mơ hồ, không tin cậy hoặc bị thay đổi ⇒ zero child,
> `not_measured`; invocation kế tiếp tự bind bản nâng cấp mới. Secret không xuất hiện trong argv/report.
> Writer NLM/GWS ghi identity ngay sau `O_EXCL` trước chmod, giữ inode đó mở qua cleanup để chặn tái sử dụng
> `(dev, ino)`, và giữ cả tên temp/final cho đến khi parent-directory fsync thành công. Lỗi từ chmod đến
> directory fsync (kể cả `EINVAL`/`ENOTSUP`/`EIO`) chỉ xoá đúng inode của writer, bảo toàn replacement
> và exception gốc; toàn bộ descriptor còn lại vẫn được thử close, với close-only failure là fatal.
> **Windows (Claude Code):** bấm đúp `tl-setup.cmd` (gốc skill) — menu: [1] Setup 1 lần (cài gws + auth +
> tự tạo `TL_MASTER_KEY` + mã hoá secrets + in lệnh Cowork vào `COWORK-paste.txt`), [2] Đổi token GAS,
> [3] Kiểm tra. Sau setup: Code chạy thẳng; Cowork dán khối trong `COWORK-paste.txt`.
Khi muốn CẢ webapp token (GAS) cũng mã hoá (không chỉ gws cred): dùng 1 **khoá gốc duy nhất** `TL_MASTER_KEY`
(1 env var/phiên — không file). Bundle `tl_secrets.enc` (Drive) mã hoá **FULL config + gws_cred**.
> Vì sao cần master key: GAS token là khoá mã hoá của A0.4b — không thể tự-mã-hoá-bằng-chính-nó (con gà/quả
> trứng) → phải có 1 secret gốc khác. Bundle nhỏ → Cowork tải token-less qua Drive MCP.
```bash
# [CODE] 1 lần (hoặc khi secret đổi): gói full config + gws cred → mã hoá → upload, in fileId → baked SECRETS_FILEID
export TL_MASTER_KEY='<passphrase mạnh>'
python scripts/tl.py secrets-stage
# [COWORK] mỗi phiên — env-aware: nạp GAS token + full config (+ gws binary/cred ở Code/Cowork)
export TL_MASTER_KEY='<passphrase>'
#   agent tải SECRETS_FILEID qua Drive MCP → lưu /tmp/s.enc NGOÀI repository
#   (Cowork token-less); Code có token thì tự webapp-fetch. --secrets-file là bắt buộc.
python scripts/tl.py bootstrap --env cowork --secrets-file /tmp/s.enc
python scripts/tl.py ping ; python scripts/tl.py gws-ping --env cowork
```
**Xoay vòng / đổi token** (tại chỗ, giữ fileId): `tl secrets-set --gas-token <t>` · `--webapp <url>` · `--gws`
(re-export gws cred). Sai `TL_MASTER_KEY` → HMAC chặn (báo "giải mã lỗi").
> bootstrap **MERGE** vào `~/.tra_luat_config.json` (không clobber), `chmod 600`. So A0.4b: A0.4c mã hoá CẢ token
> GAS lẫn gws cred bằng 1 master key (cao hơn 1 bậc — không gì plaintext trên Drive); đổi lại cần đặt 1 env var.

**A0.4d — NLM CLI ở Cowork + lỗi OAuth `exporttext` (GAS).**
- **nlm (notebooklm-mcp-cli):** pure Python, YÊU CẦU **Python ≥3.11** (KHÔNG có binary standalone như gws).
  `tl bootstrap` thử `uv tool install --python 3.11` (uv tự tải managed Python 3.11). nlm_cli tự tìm
  `~/.local/bin/nlm`. **Auth cookies** là bước RIÊNG (hết hạn): `nlm login` / `nlm login --manual -f cookies.txt`.
  Thiếu nlm/auth → skill tự fallback NotebookLM MCP.
  - **Cowork (Python 3.10 + CHẶN egress astral CDN → uv không tải được managed Python):** chạy **`tl nlm-install`**
    → tải **Python 3.11 standalone** (python-build-standalone, `PY311_FILEID` trên Drive — egress Drive MỞ) →
    giải nén `~/.local/python311` → cài nlm bằng Python đó (uv `--python <bin>` hoặc pip; PyPI vẫn cần mở).
    Egress sandbox là allowlist HẠ TẦNG Cowork (không sửa từ skill); cách vòng = đưa artifact qua Drive.
  - Nếu cả PyPI cũng bị chặn → CLI bất khả; dùng **NotebookLM MCP** (`mcp__notebooklm-jacob__*`, đã sẵn ở Cowork) —
    CLI chỉ là tiện ích tốc độ, KHÔNG ảnh hưởng chất lượng rà soát.
- **Auth nlm headless cho Cowork (`nlm login` là cookie-based, mở trình duyệt — KHÔNG chạy được trong sandbox):**
  1) Ở **Code/máy có trình duyệt**: `nlm login` (1 lần) → cookies lưu `~/.notebooklm-mcp-cli/{auth.json, profiles/default/*}`.
  2) `tl secrets-stage` (đã có TL_MASTER_KEY) TỰ gói các file đó vào bundle `.enc` dưới khoá `nlm_auth` (SECRET — chỉ
     trong bundle mã hoá, secret_guard chặn lộ). 3) Cowork `tl bootstrap` GHI lại `~/.notebooklm-mcp-cli/…` → nlm chạy
     **headless** (`nlm login --check` xanh). `--no-nlm` để bỏ gói.
  - **Cơ chế refresh (vì sao GHI FILE, KHÔNG dùng env var):** nlm giữ 3 lớp — cookies (vài tuần, vài cái xoay/request),
    CSRF (vài phút, tự refresh mỗi lần init MCP), session-id (mỗi lần khởi động). Khi cookie hết hạn nlm đọc lại
    auth.json từ ĐĨA và tái sinh từ **browser profile** (`chrome-profiles/`) — nên PHẢI ghi ra file (bootstrap ghi
    đĩa, KHÔNG set `NOTEBOOKLM_COOKIES`/`_CSRF_TOKEN`/`_SESSION_ID` — env var "đông cứng" làm auto-refresh CHẾT).
  - **Cowork không tự refresh được** (không có Chrome/browser-profile) — nhưng 1 phiên Cowork (giờ) « tuổi cookie
    (tuần) nên đủ; CSRF/session tự sinh trong phiên từ cookie đĩa. Refresh THẬT xảy ra ở **Code** (browser profile).
  - **Bảo trì ~2–4 tuần** (bootstrap báo "cookie ~N ngày tuổi", >14 ngày thì cảnh báo): ở Code chạy `nlm login`
    (hoặc để nlm tự headless-refresh khi dùng) rồi **`tl secrets-set --nlm`** (refresh cookie tại chỗ vào bundle,
    giữ nguyên fileId — `secrets-stage` tự `nlm login --check` trước khi gói để bắt cookie mới nhất).
- **Lỗi `exporttext`: "không có quyền UrlFetchApp.fetch / cần script.external_request"** = webapp deploy
  THIẾU scope đã-cấp-quyền (dù `exportBlob_` ưu tiên `Drive.Files.export`, gặp quirk thì rơi xuống UrlFetchApp).
  Fix (chủ webapp, KHÔNG agent làm được): (1) appsscript.json có `https://www.googleapis.com/auth/
  script.external_request` (xem `references/APPSSCRIPT_MANIFEST.open-egress.json`); (2) RUN 1 hàm trong editor
  → màn hình cấp quyền → đồng ý scope mới; (3) Deploy → Manage deployments → Edit → New version.
  TẠM THỜI: đọc nguyên văn đã đi qua **gws** (`tl extract` ưu tiên transport→gws, cùng GDoc, nguyên văn 100%).

**A0.5 — BÍ MẬT.** `credentials.json` chứa refresh_token/client_secret = SECRET.
- KHÔNG echo/commit/upload; KHÔNG để vương trong cây skill hay gói INSTALL.zip. Mỗi phiên Cowork nạp lại qua env, hết phiên dọn file.
- secret_guard (v1.22) chặn `GOCSPX-` / `1//<refresh>` / khối PEM / SA-key + redirect/pipe của lệnh export.

**A0.6 — Ma trận transport Drive theo env.**
| env | shell `tl.py`/`gws` | transport Drive | auth | boot |
|---|---|---|---|---|
| **Code** | ✅ | gws → GAS fallback | `gws auth login` | §A0 → §A |
| **Cowork** | ✅ | gws → GAS fallback | exported cred (env) | §A0 → §A |
| **Chat** | ❌ | Drive MCP | connector claude.ai | **SKIP §A0** → §A (MCP) |

**A0.7 — Phân vùng op A–E + ĐỊNH TUYẾN (tự sinh: `python scripts/tl.py transport-info`).**
Router `scripts/transport.py` (`drive_op`/`run_batch`) định tuyến theo nhóm × env; bridge: `gws_bridge.py` (shell),
`mcp_bridge.py` (Chat). Nguồn-chân-lý là `OP_GROUP`; bảng dưới là ảnh chụp:

| nhóm | op | confirm | Code/Cowork | Chat | GAS-fallback |
|---|---|---|---|---|---|
| **A** read | files_get·read·files_list·search | không | **gws** | Drive MCP (get_file_metadata/read_file_content/search_files) | get-meta·read có; search=registry (không parity) |
| **B** write an toàn | upload·copy_convert·mkdir | không | **gws** | create_file/copy_file | copy_convert·mkdir có; **upload KHÔNG** (webapp không nhận binary) |
| **C** write rủi ro | move·rename·trash·restore | **THEO LÔ** | **gws** | **defer→Code/Cowork** | có (GAS forward `confirm=yes`) |
| **D** business-logic | register·manifest·preflight·slot·standardize_name·organize·footnote_map·vbhn | — | **GAS độc quyền** | **defer→shell** (`DeferToShell`) | n/a (chính GAS) |

- **move 2-BƯỚC** (gws không tự removeParents): `files get fields=parents` → `update addParents/removeParents`.
- **Confirm-gate THEO LÔ**: `transport.run_batch(items, confirmed=False)` → `ConfirmRequired` liệt kê CẢ lô; xác nhận 1 lần (`confirmed=True`) rồi chạy hết. Đơn lẻ: `drive_op(op, confirmed=True)`.
- **Fallback ồn ào**: gws chết/`TL_GWS_DISABLE=1` → stderr `[FALLBACK→GAS] op=…` rồi gọi GAS (trừ `upload`).
- **Ngoại lệ chặn**: `ConfirmRequired` (C chưa confirm) · `DeferToShell` (D ở Chat) · `DeferToMCP` (mcp in-process, mang `.spec` để Claude gọi tool).
- **Timeout phép dò (r327)**: `gws auth status` tốn **15–50s** (liệt kê 34 API + gọi mạng) — trần cũ 20s
  nằm GIỮA vùng đó nên `is_available()` lật đỏ/xanh theo mạng, kéo `drive-push` rơi xuống gcloud thiếu
  Drive scope ⇒ `[FAIL]` dù gws SỐNG. Nay 120s, chỉnh được: `TL_GWS_AUTH_TIMEOUT` ·
  `TL_GWS_VERSION_TIMEOUT` (đè riêng) · `TL_GWS_TIMEOUT` (SÀN chung, **chỉ nâng**).
- **Timeout đường GHI (r330)**: `update_content` **120s ĐÃ CHẶN THẬT** một lượt deploy gói 2.487.725 B
  (`gws timeout sau 120.0s`); `TL_GWS_TIMEOUT=900` thì đẩy xong + byte-match. Nay **600s** cho ba lệnh
  **GHI CÓ TẢI** (`upload` · `update_content` · `download`) + SÀN riêng `TL_GWS_WRITE_TIMEOUT`
  (**chỉ nâng**, vì nó phủ nhiều lệnh mặc định khác nhau — cho hạ thì một số san phẳng cả nhóm).
  Đo trên máy chuẩn: 2,49MB tốn **6–19s**, 25MB tốn **31–47s** (băng thông ~170–850 kB/s); ca hỏng suy ra
  ≤ ~21 kB/s. Lệnh metadata (`mkdir`/`rename`/`delete`, đo 1,9–3,3s) **giữ nguyên** 60/60/30s — không
  co giãn theo băng thông. ⚠ **Đừng áp công thức «2,4× ca chậm nhất đo được» của r327 ở đây**: mọi mẫu
  đo được đều thuộc vùng LÀNH nên 2,4×19,3 = 46s, tức **thấp hơn cả 120s vốn đã hỏng**.
- ⚠ **Thấy `auth=None`, hay `drive-push` chết vì `timeout`, ĐỪNG vội `gws auth login`** — đọc
  `probe_error` trong `tl transport-info --json` trước: có chữ `timeout` nghĩa là **không dò được /
  không kịp**, KHÔNG phải mất quyền. Thông điệp của `drive-push` nay tự nói câu này (r330).

**A0.8 — Đo end-to-end (Code, gws auth oauth2; read=median 3 mẫu, mutate=1 mẫu).**

| op | nhóm | gws | GAS | ghi chú |
|---|---|---:|---:|---|
| files_get | A | ~1.1s | ~2.6s | get-meta; gws ~2.4× nhanh |
| read GDoc (~14KB) | A | ~1.5s | ~2.6s | export text/plain |
| files_list | A | ~1.0s | — | Drive list |
| upload _HOP_NAP | B | ~2.3s | — | gws-only |
| mkdir | B | ~1.5s | — | folder |
| move (2-bước) | C | ~2.5s | — | get parents + update |
| trash | C | ~1.1s | — | |
> gws PRIMARY nhanh hơn GAS rõ ở read (GAS = round-trip Apps Script `/exec` ~2.6–3.3s). Lần gọi gws ĐẦU phiên
> có thể spike (mở keyring/kết nối). Số tuyệt đối tuỳ mạng — đo lại bằng pilot `tl drive-parity` / script đo.

**A0.8b — ƯU TIÊN CÔNG CỤ THEO HIỆU NĂNG (số đo LIVE Code, median 3–4 lần).**

**DOWNLOAD — benchmark 3 cách (ms), thấp = tốt:**

| file | direct-media (token-cache) | gws get | AppsScript-b64 | byte-exact direct-media |
|---|---:|---:|---:|---|
| tiny .json 0.9KB | **1040** | N/A (gws méo JSON) | 3576 | ✓ |
| med .js 106KB | **1440** | 1485 | 4093 | ✓ |
| large bin 6.8MB | **2997** | 3156 | 20848 (5.6×!) | ✓ |
| GDoc→text (export) | 3083 | **2596** (read_text) | 3768 | ✓ |

→ **direct-media = PHƯƠNG ÁN TỐI ƯU cho download blob** (mọi loại .js/.txt/.json/binary): `alt=media` raw HTTP + access-token đổi-1-lần-cache → **nhanh nhất + byte-exact MỌI loại** (gws CLI làm méo text/JSON; AppsScript-b64 chậm 2–5.6× + cap 9MB). Router `drive_op("download")` ở Code/Cowork tự chọn direct-media khi có gws cred (`~/.config/gws/credentials.json`), fallback gws (binary) → GAS-b64.

**Các op khác (gws vs GAS):**

| op | gws | GAS | thắng | ghi chú |
|---|---:|---:|---|---|
| read GDoc→text | ~2.6s | ~2.6s, **cap 200KB** | **gws read_text** | direct-media-export ≈ ngang; file >200KB BẮT BUỘC gws/direct-media |
| get-meta / search | ~1.1s | ~2.6s | gws | |
| trash / rename (1 call) | ~1.1s | ~2.6s | **gws** | |
| move (2 call) | ~2.9s | ~2.7s | **≈ NGANG** | GAS 1-call-server-side bù 2 round-trip gws |
| upload | làm được | KHÔNG (webapp không nhận binary) | **gws** | |

**Quy tắc tinh chỉnh:**
- **Download (Code/Cowork):** thứ tự **direct-media → gws → GAS-b64** (router tự lo). direct-media cần gws cred dạng file (bootstrap ghi sẵn); Code-keyring không có file → tự rơi xuống gws/GAS (vẫn đúng bytes). Token được cache trong process → tải loạt file chỉ 1 lần đổi token.
- **Secrets `.enc` lúc bootstrap** vẫn webapp-b64 (chicken-egg: cred ở trong .enc, chưa giải mã được).
- **mcp KHÔNG phải tier-3 chung** — chỉ ở **Chat**, **vắng** cho mutation. Ở Chat: mcp là transport DUY NHẤT; mutation → defer Code/Cowork.
- Lần gọi gws ĐẦU phiên có cold-spike (~vài giây, keyring) → đừng kết luận từ 1 mẫu.

**A0.9 — Nghiệm thu tích hợp (GĐ0–4, đã chạy LIVE).**
- ✅ Parity get-meta/read 3 backend (gws≡GAS≡MCP) trùng field giao nhau (md5 chỉ gws/GAS).
- ✅ Fallback `[FALLBACK→GAS]` ồn ào khi gws chết — cả read lẫn op nhóm C (trash).
- ✅ Confirm-gate chặn move/trash đơn lẻ + THEO LÔ (`run_batch`).
- ✅ Chat: nhóm D → `DeferToShell` ("defer Code/Cowork"), không giả vờ chạy.
- ✅ secret_guard chặn credential gws (GOCSPX-/`1//`/PEM/SA-key/redirect export); get-meta MCP set `excludeContentSnippets`.
- ✅ Suite xanh: `tl` 101/101 · `transport` 9/9 · `contract` 2/2 · `gen` 14/14. GS KHÔNG đổi (không redeploy).

---

## A. KHỞI ĐỘNG — chạy đúng thứ tự (config → token → ping → manifest → index)

**A1. Đọc config (nguồn token/URL/categories/profile).**
Thứ tự nạp: `env (TL_WEBAPP/TL_TOKEN)` → `--config FILE` → `~/.tra_luat_config.json` → `/tmp/tra_luat_config.json`.
Phiên Claude: đọc mirror `tra_luat_config.json` (Drive MCP / `readconfig`) rồi export env.
```bash
export TL_WEBAPP=…  TL_TOKEN=…  TL_MANIFEST_ID=…
python scripts/tl.py --profile vbthuong profile-info --json
```
> Config v2 vẫn đọc file VBQPPL trước để lấy `webappUrl/token`, rồi overlay `profiles.<name>`.
> Mirror v1 chứa: `webappUrl, token, rootFolderId, registryDocId, manifestId, notebookVbqpplId, categories`.
> Notebook VBQPPL = `743ed200-2e55-4673-b7a0-9bfd13b41ce6` (config là chuẩn).

**A2. Cổng phiên bản — `ping` phải khớp.**
```bash
python scripts/tl.py ping        # hoặc: python scripts/gas.py
```
- LIVE/EXPECT = `2.21.2l` (đã xác minh). `version == 2.21.2l` và `registry_schema == reg_cols_row_kind_v1` → tiếp. **KHÁC** → DỪNG, đối chiếu deploy. (Doctrine: **regen2 trên profile** chỉ chạy khi `version == 2.21.2l`; version-gate tự CHẶN nếu server trôi xuống thấp hơn — an toàn, không phình.)
- Ưu tiên `tl.py`. Nếu cần client fallback tối thiểu: `python scripts/_fallback/gas.py ACTION key=value`.
- Lỗi "Sai token" → kiểm `TL_WEBAPP/TL_TOKEN` hoặc chạy `tl init-config`; mirror token có thể private nên không trông chờ tải tự động mơ hồ.

**A3. Đọc manifest + dựng index offline (HỌC corpus).**
```bash
python scripts/tl.py boot        # tái dùng cache local nếu < TTL (0 call webapp, ~0.2s); lần đầu/--refresh ~6-12s
python scripts/tl.py boot --refresh           # ép tải lại từ webapp (sau khi corpus đổi)
python scripts/tl.py perf                      # đo round-trip/song song/cache khi thấy CHẬM
```
> **Hiệu năng (v1.19.6):** mỗi call Apps Script `/exec` ~3.3s round-trip (server chỉ ~tí xíu). boot tái dùng
> cache local (TTL mặc định 600s; env `TL_BOOT_TTL`) → KHÔNG gọi webapp khi đã tươi. `--timings` in thời gian
> từng call. Tra cứu nhiều số hiệu nên gộp song song (`gas_parallel`). Chi tiết: `references/PERFORMANCE_V1.19.6.md`.
Index khóa: `so_hieu` (CÓ gạch dưới, trong manifest) / `nlm_source_id` / `gdoc_id` → entry.
Boot báo: tổng nguồn, corpus=true, văn kiện Đảng (cat 00 / `-TW`), entry **thiếu so_hieu** (mồ côi → dọn),
**trùng so_hieu** (VBHN nhân bản → dọn). Manifest = DANH MỤC CHÍNH offline; KHÔNG quét NLM thường quy.

**A4. ĐỌC NLM — BẮT BUỘC qua CLI `nlm` (Claude Code/Cowork), KHÔNG qua MCP.**
- **Mọi thao tác ĐỌC NLM** đi qua CLI (nhanh hơn, không tràn token, không timeout):
  - Liệt kê nguồn: `tl nlm-list <nb>` = `nlm source list <nb> --drive --skip-freshness -j` (~4s; cờ `--skip-freshness` MCP THIẾU).
  - Toàn văn raw: `tl nlm-content <source_id>` = `nlm source content -j` (thay MCP `source_get_content` vốn TRÀN TOKEN).
  - RAG: `tl nlm-query <q> [--source-id …]` = `nlm notebook query -j` (thay MCP `notebook_query`); verify nguyên văn sau.
  - **Xuyên shard:** `tl nlm-cross "<q>" [--notebooks csv|--all]` = `nlm cross query` (thay MCP `cross_notebook_query`; mặc định base+overflow VBQPPL — đã test 2/2 shard).
  - **Số nguồn vật lý (slot/preflight):** `tl nlm-get <nb>` = `nlm notebook get -j` (thay MCP `notebook_get.source_count`).
  - get/describe: `nlm source get|describe`, `nlm notebook get|describe`.
- **GHI NLM cũng qua CLI:** thêm nguồn = `tl nlm-add`/`tl ingest-local` (`nlm source add --drive … --wait`,
**thay MCP `source_add`**); xóa = `nlm source delete -y`; sync = `nlm source sync`; đổi tên =
`nlm source rename <sid> "<title>" -n <nb>` (**thay MCP `source_rename`**, giữ tên NLM=Drive §0.7). **MCP CHỈ
fallback** khi thiếu CLI/auth (hoặc studio nếu CLI chưa có). `source_list_drive` MCP timeout ~4' → cấm dùng
thường quy. **LƯU Ý CLI:** chỉ `source list`/`source content`/`notebook query|get` có `-j`;
`source add/delete/rename/sync` + `cross query` KHÔNG có `-j` → wrapper parse text (`Source ID: <uuid>`). (Bài
học 25/6: ingest 2 VBHN trước còn phải gọi MCP source_add thủ công → đã thay bằng CLI để pipeline
`tl ingest-local` chạy trọn vẹn.)
- **Đối soát registry↔NLM:** `tl nlm-reconcile <nb>` (ground-truth từ CLI) → backfill `nlm_notebook_id`; báo `desync_real`/`already_removed`/`other_notebook`/`unregistered`. DRY mặc định; `--apply [--clear-stale]`.
- Auth CLI: tự refresh CSRF khi 401; nếu hết hạn hẳn → `nlm login` (TƯƠNG TÁC, không headless).
Freshness/`source_sync_drive` CHỈ trên tập `source_ids` đích (`nlm_status='stale'`), `confirm=True`.

---

## B. CỔNG VẬN HÀNH (áp dụng suốt phiên)

**B1. Định tuyến tìm file.**
- TRONG cây corpus (cat dưới rootFolderId) → webapp `find`/`search scope=corpus` / registry offline.
- NGOÀI corpus (shared, My Drive root, shared drive) → **Drive MCP `search_files`** (webapp `scope=all` quét THIẾU).
- Link-shared chưa add + không khớp tên → truy cập THEO ID (`get_file_metadata`/`copy_convert` by id).

**B1a. Corpus profile + fallback.**
Khi làm văn bản thường hoặc dự án riêng, chạy với `--profile <name>` hoặc `TL_PROFILE=<name>`.
Profile gồm `rootFolderId/notebookId/registryDocId/manifestId/categories` riêng. `vbqppl` là nền dùng chung, không phải đích mặc định cho văn bản thường.

Thứ tự tra/dedup: manifest+registry của profile hiện tại trước → miss mới fallback VBQPPL và báo rõ. QA xuyên corpus dùng `tl nlm-cross --notebooks <profile_nb>,<vbqppl_nb>` (CLI; thay MCP `cross_notebook_query`); canonical của profile thắng.

Cache manifest tách theo profile: `vbqppl` dùng cache cũ, profile khác dùng `~/.tra_luat_cache/<profile>/`.

**v1.19 (Cách B — registry/manifest RIÊNG theo profile, GS ≥ 2.21.2h):** webapp 1 deployment nhận
`registryDocId`/`manifestId` mỗi request. Khi `--profile P` (KHÁC `vbqppl`), `tl.py` tự forward
`registryDocId=<P.registryDocId>` + `manifestId=<P.manifestId>` vào MỌI call (env `TL_REGISTRY_DOC_ID`/
`TL_MANIFEST_ID`); thiếu/`vbqppl` ⇒ webapp dùng Sheet/manifest VBQPPL nền. Vì vậy `find/locate/source-map/
reg_*/map_set/organize/regen2/manifest_export/nlm_*` — **kể cả `tl boot` và `tl manifest`** (qua
`_fallback/boot.py`, `_fallback/manifest_build.py` đã forward scope) — đọc-ghi ĐÚNG registry của profile.
Cache offline tách theo profile (`~/.tra_luat_cache/<profile>/`). Thiết lập 1 lần cho profile mới + backfill:
xem `references/DELTA_v1.19.md §C`.

> **DOCTRINE backfill (DELTA §C.1):** notebook dự án thường gồm cả VĂN BẢN THƯỜNG riêng *và* VBQPPL canonical
> dùng chung. CHỈ đăng ký văn bản thường vào registry profile. VBQPPL canonical: **GIỮ NGUYÊN ở registry VBQPPL,
> KHÔNG move/xoá** (xoá = hỏng corpus pháp điển); nếu cần slot/dedup của notebook dự án đúng thì THÊM dòng tham
> chiếu (cùng `drive_id`/`nlm_source_id`, `nlm_notebook_id=<NB dự án>`). Khi nghi ngờ một nguồn là canonical →
> mặc định coi là VBQPPL.

**B1b. Locate có cờ cảnh báo registry.**
```bash
python scripts/tl.py locate <số hiệu/tên> [--refresh]
```
Nếu output có `WARN=OMNIBUS_NARROW_TITLE_CHECK`, `TITLE_METADATA_MISMATCH`, `ORPHAN_CAT`, `RAW_NAME_NOT_NLM`... thì KHÔNG chọn theo tên file ngay. Chạy `tl status <sohieu>` để kiểm VBHN/hiệu lực và `tl hygiene plan <query> --json` để xem canonical. Đây là lớp chặn lỗi chạy thật khi tên file hẹp/sai, ví dụ một luật sửa nhiều luật bị đặt tên như riêng "Bảo hiểm y tế".

**B1b.1. Không kết luận vắng mặt từ API thô.**
Không bao giờ kết luận "không có trong nguồn" chỉ từ `gas.py reg_get name_contains=...`. Action này khớp chuỗi nguyên văn, phân biệt dấu/gạch nối/gạch dưới, và dễ bị cắt kết quả khi người dùng chỉ in vài dòng đầu. Trước khi kết luận vắng mặt phải chạy ít nhất 2 góc bằng công cụ chuẩn hóa:
```bash
python scripts/tl.py source-map "<tên/chủ đề>" --json
python scripts/tl.py exists "<số hiệu/tên>" --json
python scripts/tl.py locate "<số hiệu>" --refresh
# hoặc:
python scripts/tl.py status <số hiệu>
```
Nếu vẫn dùng `reg_get` để soi nhanh, chỉ dùng theo khóa chắc (`sohieu`, `drive_id`, `nlm_source_id`) hoặc in đủ `count`/`rows`; không dùng `name_contains` làm bằng chứng vắng mặt.

**B1c. Source-map trước khi rà soát nhóm luật.**
```bash
python scripts/tl.py source-map "74/2025/QH15" "41/2024/QH15" "84/2015/QH13" "Bảo hiểm y tế"
```
`source-map` đọc manifest offline, áp VBHN-first theo trường `goc`, trả canonical và cảnh báo `NO_VERIFIED_VBHN_IN_CORPUS`, `QT5_WEB_REQUIRED`, `VBHN_NUMBER_REUSE_RISK`, `NAME_QUERY_MULTIPLE_HITS`, `TITLE_OR_REGISTRY_WARN`. Từ v1.17.24, `source-map` còn quét `amendment_candidates` theo chủ đề/dấu hiệu "sửa đổi"; nếu có `AMENDMENT_CANDIDATE_IN_CORPUS`/`UNLINKED_AMENDMENT_CANDIDATE`/`PAUSE_AND_ASK_USER`, phải dừng rà soát và hỏi người dùng để link/nạp/VBHN trước. Với nhóm luật thực tế, chạy lệnh này trước khi `extract`/`notebook_query`.

Nếu `source-map` báo `NO_VERIFIED_VBHN_IN_CORPUS`, nghĩa là corpus chưa có VBHN đã xác minh, **không phải** kết luận VBHN không tồn tại. Phải chạy QT-5 web bằng trích yếu/chủ đề + "hợp nhất" trên nguồn chính thức/đáng tin. Nếu truy vấn số VBHN trần như `14/VBHN-VPQH` có `VBHN_NUMBER_REUSE_RISK`, phải verify ngày ban hành, tiêu đề và dòng "Luật ... được sửa đổi, bổ sung bởi..." vì Văn phòng Quốc hội có thể tái sử dụng cùng số VBHN ở năm khác.

VBHN cấp Bộ cũng phải có năm. Với các số hiệu như `09/VBHN-BYT`, `05/VBHN-BGDĐT`, `2279/VBHN-BLĐTBXH`, không đổi tên/quarantine theo số hiệu trần. Phải verify năm ban hành + chủ đề + nội dung; tên chuẩn dạng `VBHN_<so>-VBHN-<co_quan>_<year>_<ten_rut_gon>`.

**B1c.1. Relation-check khi phát hiện văn bản lỗi thời/sửa đổi.**
Nếu biết hoặc nghi văn bản đang rà đã bị sửa đổi, DỪNG rà trên bản cũ và chạy ngay:
```bash
python scripts/tl.py relation-check --base <số hiệu gốc> --subject <trích yếu> [--amendment <số hiệu sửa đổi>] --json
```
`vb_status` có thể bỏ lọt nếu registry thiếu `goc/sua_doi`. `relation-check` quét theo số hiệu + chủ đề + dấu hiệu "sửa đổi"; nếu thấy `AMENDMENT_FOUND_IN_CORPUS` hoặc `RELATION_BACKFILL_REQUIRED`, hỏi người dùng xác nhận ghi registry ngay, không đưa vào mục xử lý sau.

**B1d. QT-5 verification gate cho VBHN.**
```bash
python scripts/tl.py vbhn-check --subject "an toàn vệ sinh lao động" --goc "84/2015/QH13" --year 2024 --json
python scripts/tl.py vbhn-verify --text-file vbhn_atvsld_2024.txt --expect-title "an toàn vệ sinh lao động" --expect-goc "84/2015/QH13" --expect-goc "41/2024/QH15" --expect-year 2024 --official-required --json
python scripts/tl.py vbhn-check --scan --json
```
Với luật đã bị sửa đổi, workflow là `source-map → relation-check → vbhn-check → vbhn-verify → mới chốt nguồn rà soát`. `vbhn-check` chỉ tìm ứng viên và sinh truy vấn QT-5; `vbhn-verify` mới bắt dương tính giả kiểu đúng số hiệu nhưng sai chủ đề/năm. Nếu không thấy VBHN trong corpus, phải chạy các query gợi ý ngoài corpus, gồm query đơn giản kiểu `"luật <chủ đề>" "hợp nhất"` và nguồn secondary như Thư viện Pháp luật để phát hiện nhanh; canonical vẫn official-first.

**B1e. Official-first cho VBHN, không tự ghép làm bản dùng.**
Nếu corpus không có VBHN chính thức, hỏi người dùng nạp file vào `_HOP_NAP` hoặc lấy từ nguồn chính thức/đáng tin. Không tự lắp bản hợp nhất từ bản gốc + luật sửa đổi để đăng ký canonical/NLM. Bản tự lắp chỉ được dùng như bản tạm để phân tích, phải đặt tên có `PROVISIONAL`/`ASSEMBLED`, không add NLM làm nguồn rà soát chính, và đưa QUARANTINE khi có bản chính thức.

Khi người dùng nạp bản chính thức, so với bản tạm trước khi thay:
```bash
python scripts/tl.py vbhn-verify --text-file official.txt --expect-title "an toàn vệ sinh lao động" --expect-goc "84/2015/QH13" --expect-goc "41/2024/QH15" --expect-year 2024 --official-required --source-name "14_VBHN-VPQH_629950.docx" --json
python scripts/tl.py vbhn-compare --official-text official.txt --candidate-text assembled.txt --focus "Điều 53" --json
```
Nếu `vbhn-compare` báo `CANDIDATE_MISSING_FOOTNOTES`, `FOCUS_DIFF:*`, hoặc `FOCUS_REF_DIFF:*`, lấy bản chính thức làm canonical; bản tạm phải gỡ khỏi NLM/registry canonical và chuyển QUARANTINE.

**B1f. External-ingest gate cho nguồn web/NotebookLM.**
`research_start`/`research_status` chỉ dùng để tìm URL ứng viên. Không dùng `research_import` hoặc
`source_add(url)` để nạp thẳng VBQPPL vào notebook tạm hoặc notebook chính. Đồng ý "tìm nguồn" KHÁC
đồng ý "ghi vào corpus/NLM".

Trước khi ghi/nạp nguồn web, phải trình người dùng duyệt: URL, official|secondary, định dạng, cat/folder/notebook
đích, tên chuẩn dự kiến, số hiệu/năm/trích yếu, quan hệ gốc/sửa đổi/VBHN. Đích mặc định là folder Drive + notebook
đang dùng; không tạo notebook/folder mới trừ khi người dùng yêu cầu rõ. Ưu tiên docx/doc/GDoc-convertible hơn PDF;
nếu chỉ có PDF thì convert/OCR trước, không nạp PDF thô làm canonical NLM khi có thể tạo GDoc chuẩn.

**B1g. AUTO-DOWNLOAD VBQPPL từ TVPL (Claude Code/Cowork + Claude in Chrome đã login VIP).**
TVPL chặn fetch server-side (403/CORS) → Apps Script/WebFetch KHÔNG tải được (kết luận "full-auto bất khả" CŨ chỉ
đúng cho môi trường Apps-Script/Chrome-only). **Trong Claude Code/Cowork ĐÃ KHẢ THI** vì Bash đọc được file ở
`~/Downloads` (không cần file picker OS). Luồng (`tl tvpl-url <số hiệu>` in ra):
1. Người dùng **đăng nhập TVPL VIP** trong trình duyệt (Claude in Chrome) — KHÔNG nhập mật khẩu hộ.
2. Claude in Chrome: navigate `tim-van-ban.aspx?keyword=<số hiệu>` → mở đúng `/van-ban/...aspx` → tab **"Tải về"** → link **"Tải Văn bản tiếng Việt (docx)"** (HỎI người dùng trước khi tải — tải file là hành động cần xác nhận).
3. Bash: `*.docx` mới nhất trong `~/Downloads`.
4. Upload `_HOP_NAP`: Drive `create_file` (docx→convert GDoc) hoặc webapp `importext`.
5. Chuẩn hóa tên → cat → `tl preflight` → `source_add` (shard overflow topology nếu base đầy — v1.34.49: `_ingest_target` duyệt MỌI shard enabled, đọc slot fail-closed) → `tl push-overflow` (validate đích ∈ topology) → verify. Batch: `ingest-missing` failover trong-run; partial → làm theo `resume_command` (rc=2 = còn backlog, KHÔNG phải lệnh hỏng).
Văn bản Đảng (NQ-TW…) thường KHÔNG có trang /van-ban/ tải được trên TVPL → dùng nguồn official khác / tải thủ công.

**B1g-bis. BÀI HỌC THỰC CHIẾN tải qua Claude in Chrome (đã kiểm chứng) — `tl fetch-route`/`fetch-links`/`find-doc`:**
- **DISCOVERY = Google `site:`** (search nội bộ TVPL/LVN kém): `tl find-doc <q>` / WebSearch `site:thuvienphapluat.vn <tên> hợp nhất` → ra ĐÚNG trang VBHN. VBHN-first ('hợp nhất' → 'mới nhất' → gốc).
- **TVPL:** mở trang văn bản → **CLICK TAB 'Tải về' TRƯỚC** (link docx đổi từ `javascript:__doPostBack` → URL `/documents/d...` thật) → rồi click link `(docx)`. Click link khi tab 'Nội dung' đang active ⇒ KHÔNG tải.
- **Trang quá lớn → `find` tràn token (>200k):** dùng `javascript_tool` lấy phần tử + **tọa độ theo TỈ LỆ viewport** (`sx=center/innerWidth*1568`, `sy=…/innerHeight*737`; viewport thật ~949×445 ≠ screenshot 1568×737) rồi `computer left_click` thật. JS `.click()` chỉ chạy cho thẻ `<a href>` thật, KHÔNG cho `javascript:` href.
- **QUOTA TVPL ~1 docx/ngày/tài khoản:** lần tải thứ 2 trong ngày 'bật về trang chủ'/không ra file ⇒ HẾT QUOTA. **Fallback: LuatVietnam** (docx, nếu đã login; nút tải là thẻ `<a>` ICON, JS click `<a>` được) → **vbpl.vn** (.doc FREE, nhưng **không có VBHN**, chỉ bản gốc) → Công báo (.pdf).
- **vbpl.vn:** tìm theo radio 'Số hiệu' → 'Tải về' → dialog 'File đính kèm' → 'Tải xuống' .doc. KHÔNG index VBHN (số VBHN → 0 kết quả).
- **D1 — egress Công báo CDN (ĐÃ KIỂM CHỨNG 25/6/2026):** PDF official ở `g7.cdnchinhphu.vn`; bash mặc định → 403 'Host not in allowlist'. Cách:
  - **② Bash `dangerouslyDisableSandbox` + curl link g7 TRÍCH từ trang congbao** (`grep -oE 'https://g7\.cdnchinhphu\.vn/api/download/stream\?Url=…&file_name=…'`, đổi `&amp;`→`&`) → tải thẳng container → `_HOP_NAP`. Test thật: congbao=200, tải PDF 2.1MB/111 trang OK. CHỈ host official `.gov.vn`/`.chinhphu.vn`.
  - ① Chrome (đã login) tải về MÁY người dùng → kéo vào `_HOP_NAP`.
  - ③ Allowlist mạng cấp sandbox (bản quản trị) thêm `*.cdnchinhphu.vn` (`settings.local.json permissions.allow` KHÔNG phải allowlist mạng).
- Verify file: magic `PK..` (docx) / `D0CF11E0` (.doc) + đọc đầu nội dung khớp số hiệu.

Instruction cho Claude/NLM phải tự ràng buộc với skill:
```bash
python scripts/tl.py instruction-audit --generate --target nlm --json
python scripts/tl.py instruction-audit --file instruction.md --json
```
Audit fail thì không dùng Instruction đó cho phiên có ghi/nạp.

**B1g. Slot/preflight theo notebook.**
Nếu `nlm_preflight` báo `NOTEBOOK_FULL` nhưng `tl nlm-get <nb>` (CLI) của notebook đích không full, nghi lỗi đếm slot theo registry chung.
```bash
python scripts/tl.py --profile vbthuong slot-audit --notebook-id fec6c125-e01c-433d-aed5-666c16540dd8 --json
```
Đếm đúng gồm rows có `nlm_notebook_id == notebook đích`; dòng RỖNG `nlm_notebook_id` được quy về notebook NỀN
(VBQPPL) — nên KHÔNG cộng vào notebook dự án (hết full giả), nhưng VẪN đếm đúng cho VBQPPL mà không cần
backfill hàng loạt. `row_kind=ref` không tính vào slot registry mặc định; dùng
`countRefs=true`/`count_refs=true` khi cần ước lượng gồm dòng tham chiếu. `slot-audit` trả
`slots_for_notebook` (registry estimate) + `slots_effective` (gồm dòng rỗng nếu là notebook nền) +
`is_base_notebook` + `rows_missing_nlm_notebook_id`. Trước khi thêm nguồn, luôn lấy số vật lý qua
`tl nlm-get <nb>` (CLI `nlm notebook get`); registry estimate không thay thế nguồn đếm thật của NLM. Khi đẩy
nguồn nên `map_set notebookId=…` để slot phản ánh đúng.

**B2. Đọc-cache-TIẾT-KIỆM-TOKEN (bắt buộc).**
Lưu toàn văn ra **file trên đĩa** (`exporttext`/`download` → 0 token vào context) → **regex** đúng Điều
→ in **đoạn ngắn**. TUYỆT ĐỐI không `cat`/đọc nguyên văn cả văn bản vào context.
```bash
python scripts/tl.py extract <gdocId> --dieu 64 [--dieu 65]   # export ra đĩa, in đúng Điều
```

**B3. Chọn nguồn để `notebook_query` (LỌC-THÔ trước, đọc-thật sau).**
1. Lọc-thô (rẻ, cấu trúc): `linhvuc` + `so_hieu`/`loai` + khớp `tukhoa`.
2. Chọn-đúng-phiên-bản: `goc`/`sua_doi`/`hieuluc`/`nlm_status` → ưu tiên **VBHN + còn hiệu lực**.
3. Còn 3–5 ứng viên → mới kéo nội dung THẬT nhóm nhỏ để chốt.
4. `notebook_query` scope đúng 1–5 `source_id` → verify với cache/raw (NLM_QA_POLICY).

**B4. CỔNG TIỀN-NẠP (QT-2) — TRƯỚC khi organize+map_set/source_add văn bản sửa đổi/VBHN/nghi bị thay.**
Nếu việc phát hiện sửa đổi xảy ra trong lúc đang rà soát, không được chỉ ghi chú "xử lý sau": chạy `relation-check`/`vbhn-check`, hỏi người dùng nạp hoặc ghi registry ngay rồi mới tiếp tục.
```bash
python scripts/tl.py relation-check --base 06/2022/QH15 --subject "thi đua khen thưởng" --amendment 06/2026/QH16 --json
python scripts/tl.py status 187/2025/NĐ-CP --amendment --targets 78-2025-ND-CP,79-2025-ND-CP
# (bọc preingest_gate → vb_status số hiệu chính + đích → ADD/SKIP/REVIEW)
```
- Có VBHN hợp nhất đúng số đang nạp, còn hiệu lực → **SKIP** bản gốc/sửa đổi, nạp VBHN.
- Bản sửa đổi mà CHƯA có VBHN cho mọi đích → **GIỮ** + `reg_upsert sua_doi='<đích1>;<đích2>' hieuluc='Còn hiệu lực'`.
- REVIEW → HỎI người dùng. **Surface quan hệ (sửa gì / bị VBHN nào hợp nhất / còn hiệu lực) TRƯỚC khi chốt.**

**B5. Đặt tên + sắp xếp hậu-convert.**
`copy_convert` → `standardize_name.py` (GDoc + file gốc cùng base name) → `organize` (rename+move+stamp+register
1 RTT) → verify bằng `list cat=<NN>` (ĐỪNG tin response của `move`). File gốc .docx/.pdf nằm CẠNH GDoc, KHÔNG add NLM.
Khi khớp `.docx/.pdf` sidecar vào canonical, đọc nội dung để xác minh số hiệu thật + ngày ban hành; không quarantine theo tên file đơn thuần. Sau rename/move, nếu manifest còn tên cũ do Drive trễ, chạy `tl manifest` export-only và verify bằng registry/`source-map`.

**B5b. Bẫy path phi-ASCII (`D:\Dữ liệu\…`)**: pdftotext build Git Bash/cp1258 nhận arg tiếng Việt HỎNG (im lặng không output) — từ v1.34.58 `_read_local_text_for_analysis` tự copy-temp-ASCII; thao tác file path Việt bằng tay thì dùng PowerShell hoặc copy sang temp trước, ĐỪNG đưa path thẳng cho tool CLI cũ.

**B6. Link cho người dùng = markdown click-mở-được** (QT-1). Cung cấp ĐỦ cả link UPLOAD (`_HOP_NAP`)
lẫn link DOWNLOAD click-thẳng-tải-được. Với link để người dùng tự tải, ưu tiên:
`thuvienphapluat.vn` → `luatvietnam.vn` → `congbao.chinhphu.vn` → cổng official khác (`vbpl.vn`, `vanban.chinhphu.vn`) → trang khác.
Quy tắc này CHỈ áp cho link tải tiện dụng; canonical lưu/đối chiếu vẫn official-first.

**B7. Ingest an toàn + resume định danh + marker v2 (r184–r190).**
- **Resume có định danh (ADR-0011)**: `profile-ingest --resume` name-only chỉ DRY repair;
  `--apply` cần `--journal <run_id>` (apply nay ghi journal) hoặc `--drive-id` fingerprint khớp registry.
- **Marker schema v2 (ADR-0012)**: writer phát v2 + fingerprint từ v1.35.17; corpus đã migrate trọn 23-07.
  Doctor báo `MARKER_SCHEMA_V1` trên marker mới xuất hiện → `profile-doctor --plan-marker-migration`
  (canary trước, user duyệt `--apply`).
- **Biến môi trường ingest**: `TL_INGEST_MEMORY_BUDGET_MB` (ngân sách RAM worker ZIP, mặc định 256,
  clamp 64-4096 — D7); `TL_DOCX_XML_MAX_MB` (trần giải nén per-member DOCX/XML chống zip-bomb,
  mặc định 50, clamp 1-500 — SEC-01; đường repack the_thuc thêm trần TỔNG = 4× member).
- **Đường bulk GAS ≥2.21.2n** (`profile_catalog`, `drive_info_bulk` — API_CONTRACT): discover/sync/doctor
  in `via` (bulk hay fallback) + `degraded_reason` khi rơi fallback — perf chỉ được coi đạt trên đường bulk.

---

## C. KẾT PHIÊN — sinh manifest chuẩn

```bash
python scripts/tl.py manifest                 # mặc định: CHỈ manifest_export (KHÔNG regen2) — phiên không đụng cấu trúc
# profile inherit → CHỈ export-only
# KHÔNG manifest --touched-drive trên profile văn bản thường (gây PROFILE_MANIFEST_SCOPE_BLOWUP)
python scripts/tl.py manifest --touched-drive --confirm yes # chỉ khi cần quét rootFolderId riêng của profile
```
- `regen2` GIỮ cột curate `REG_NLM_KEEP_`; cột mới muốn sống qua regen2 phải khai báo + Deploy + `reg_addcols`.
- Profile khác `vbqppl` mặc định `manifestScope=own`; tuyệt đối không đi vào folder category kế thừa.
- Guard dừng trước ghi nếu `new_own_count > max(2×old_own_count, old_own_count+50)`; chỉ override bằng `--confirm-blowup yes` sau khi đã kiểm scope.
- Regen profile chỉ chạy khi `ping.version=2.21.2l`; server cũ bị chặn trước khi ghi.
- KHÔNG chèn `changes_init` ở END (sửa lệch v1.12.0).

Nếu registry profile đã bị phình:

```bash
# DRY: giữ file trong rootFolderId + dòng notebook đích + mọi row_kind=ref
python scripts/tl.py --profile <P> profile-rebuild-registry --keep-notebook <id>
# APPLY sau khi kiểm drop_sample
python scripts/tl.py --profile <P> profile-rebuild-registry --keep-notebook <id> --apply --confirm yes
```

Lệnh phải dừng nếu cây `rootFolderId` bị `capped`; không xóa dựa riêng vào `nlm_notebook_id`.

---

## D. QUY ƯỚC PROMPT/LỆNH THEO PROFILE (Cách B, v1.19)

Nguyên tắc: **nêu rõ profile ở đầu yêu cầu** để định tuyến đúng registry/notebook/manifest. Khỏi nhắc mỗi lần:
đặt `defaultProfile="vbthuong"` cho không gian dự án, hoặc thêm khối `corpus_profile=vbthuong` vào Instruction.
Không nêu profile ⇒ `defaultProfile` (hiện `vbqppl`).

| Ý định | Prompt mẫu | Lệnh tl chạy ngầm |
|---|---|---|
| Nạp vb mới không trùng | "vbthuong: nạp các văn bản mới không trùng trong `_HOP_NAP` vào notebook dự án" | `--profile vbthuong` ingest/preingest → dedup theo registry vbthuong → `map_set notebookId=$NB` |
| **Nạp LÔ ≥2 file (PERF v1.34.73)** | "nạp nhanh 3 file này" | reg-query MỌI số hiệu trước (dedup) → `ingest-local --nlm-no-wait` ×N SONG SONG (−~50%/file — bỏ chờ settle) → `tl nlm-reconcile <nb> --apply` MỘT lần cuối → readback 1 lần. Chi tiết: `references/GOTCHAS.md §10` |
| **Soạn/kiểm THỂ THỨC (R1 v1.34.74)** | "soạn công văn đúng thể thức", "văn bản này đúng thể thức chưa" | căn cứ 4 hệ (hành chính NĐ30 / VBQPPL NĐ78+PL I NĐ187 / VBHN NĐ250 / Đảng QĐ399+HD05) + bảng ngưỡng + ma trận loại-VB→mẫu: `references/THE_THUC_TRINH_BAY.md`; dựng .docx bằng `tl the-thuc-build --spec <json> --out <docx>` (v1.34.84+: hệ hanh-chinh/dang, v1.34.86+ thêm vbqppl-qh, v1.34.87+ `mau=phieu_trinh`) hoặc công cụ docx MÔI TRƯỜNG theo mẫu kho chung `_meta/templates`; kiểm thành phẩm: `tl the-thuc-check <docx> [--he …] [--strict]` (v1.34.77: T1 đo cứng + T2 cấu trúc 9 thành phần/số ký hiệu/checklist VBHN/sao-gạch Đảng + T3 khuyến nghị; file phụ lục trộn ví dụ nhiều hệ thì ép `--he`) |
| Tra nguyên văn | "vbthuong: tra nguyên văn Điều X của <văn bản>" | query notebook `fec6c125` + verify; miss → fallback vbqppl |
| Rà soát đối chiếu VBQPPL | "vbthuong: rà soát Điều X, đối chiếu thêm VBQPPL" | `tl nlm-cross --notebooks fec6c125,743ed200` |
| Kiểm slot trước khi nạp | "vbthuong: kiểm slot notebook dự án" | `--profile vbthuong slot-audit --notebook-id $NB` |
| Link tải cho người dùng | "cho link tải <văn bản>" | `link-priority`: TVPL → LuatVietnam → Công báo → official khác |
| Chuyển corpus | "chuyển sang vbqppl" / "làm trên VBQPPL" | đổi `--profile vbqppl` |
| Tạo profile dự án mới | "tạo profile <tên> cho dự án …, folder <id>, notebook <id>" | dựng profile mới như `DELTA_v1.19.md §C` |
| **Tạo Instruction (mặc định VBQPPL)** | "tạo Instruction" / "tạo prompt cho Project" | `tl instructions --target project` (profile vbqppl, KHÔNG có profile_setup) |
| **Tạo Instruction văn bản thường** | "tạo Project văn bản thường tên <X>, notebook <id>" | `tl profile-create --name <X> --notebook <id> --apply` → tạo folder `Van_ban_thuong/<X>` + config patch + Instruction gắn profile `<X>` (fallback VBQPPL) |
| **Soạn theo mẫu trình bày của profile (v1.34.71)** | "vbthuong: soạn <văn bản> theo mẫu <tên mẫu>" | mẫu quản trên MARKER: `profile-set-meta --template-add <id> --template-drive-id <fid>` \| `--template-upload <file.docx>` \| `--template-remove <id>` (1 op/lần, probe fail-closed, DRY mặc định); xem kho: `profile-list --templates`; block phiên `profile-load <p>` mang khối `trinh_bay_theo_mau` (đọc khung `tl doc-text`, GIỮ NGUYÊN khung/đề mục, căn cứ verify nguyên văn; dựng .docx bằng công cụ docx MÔI TRƯỜNG — tra-luat không sinh docx) |

Mặc định khi KHÔNG nêu profile = `defaultProfile` (hiện `vbqppl`). **Tạo Instruction mà không nêu corpus ⇒ VBQPPL.**

---

## TÓM TẮT 1 MÀN HÌNH

```
A1 readconfig→env   A2 ping==2.21.2h(cổng)   A3 boot→index   A4 NLM via CLI (nlm-list/-get/-cross/-content/-query)+registry
B1 route/profile  B1c.1 relation-check khi nghi lỗi thời  B1f research discovery-only  B1g slot notebook  B2 extract-ra-đĩa  B3 lọc-thô→query→verify  B4 QT-2 trước nạp sửa đổi/VBHN  B5 đặt tên+verify list  B6 link markdown
C  manifest (--touched-drive nếu đụng cấu trúc)
Bất biến: VBHN-first · verify nguyên văn · không bịa · dedup · ĐỐI CHIẾU NGAY · tên NLM=Drive
```


## H. OVERLAY RUNTIME — khi thiếu rasoat/backfill chuyên sâu

Nếu `tl doctor` báo thiếu `rasoat_*.py`/`backfill_*.py`, đây là trạng thái overlay có kiểm soát:

```bash
python scripts/tl.py boot --json
python scripts/tl.py exists <số hiệu/tên> --json
python scripts/tl.py source-map <số hiệu/tên...> --json
python scripts/tl.py relation-check --base <số hiệu gốc> --subject <trích yếu> [--amendment <số hiệu sửa đổi>] --json
python scripts/tl.py vbhn-check --subject <trích yếu> --goc <số hiệu> --year <năm> --json
python scripts/tl.py vbhn-verify --text-file <vbhn.txt> --official-required --expect-title <trích yếu> --expect-goc <số hiệu> --expect-year <năm> --json
python scripts/tl.py extract --sohieu <số hiệu/tên> --dieu <N>
python scripts/tl.py hygiene scan --json
python scripts/tl.py hygiene plan <số hiệu/tên> --json
python scripts/tl.py rasoat keywords --json   # trả RASOAT_FALLBACK_PLAN nếu thiếu script thật
```

### r310 — `rasoat <sub>` là lệnh THẬT, đường GHI đòi `--apply`

Từ v1.36.44, `tl rasoat` không còn nuốt trọn đuôi dòng lệnh (`argparse.REMAINDER`). Mỗi nhánh là một
subcommand khai đủ cờ, nên `tl rasoat <sub> --help` liệt kê được, cờ gõ sai bị TỪ CHỐI ngay thay vì rơi
xuống script con, và `tool-inventory`/`workflow-audit --strict` nhìn thấy cả ba đường ghi.

**Chạy trần = CHỈ ĐỌC. Muốn ghi phải gõ `--apply`.**

```bash
python scripts/tl.py rasoat keywords --manifest tra_luat_manifest.json            # DRY: kê worklist, KHÔNG ghi
python scripts/tl.py rasoat keywords --manifest tra_luat_manifest.json --apply    # GHI registry (tukhoa)
python scripts/tl.py rasoat titles --from-nlm <notebook_id>                       # DRY
python scripts/tl.py rasoat titles --from-nlm <notebook_id> --apply --export      # GHI registry (nlm_title)
python scripts/tl.py rasoat orchestrate boot                                      # DRY (chỉ in KẾ HOẠCH)
python scripts/tl.py rasoat orchestrate end --apply --touched-drive               # GHI
python scripts/tl.py rasoat worksheet 18/VBHN-VPQH --out-dir .                    # chỉ ghi file cục bộ
python scripts/tl.py rasoat phuluc master.json --out-dir .                        # chỉ ghi file cục bộ
```

Hai điểm dễ vấp:

- **`--profile` giờ thuộc về `tl`** (corpus profile), gõ TRƯỚC hay SAU subcommand đều được, và được áp
  offline TRƯỚC khi gọi script con. Muốn truyền profile của **nlm CLI** cho `backfill_nlm_title.py` thì
  dùng `--nlm-profile` — trước r310 hai nghĩa này đổi chỗ cho nhau trong im lặng (RAS-14).
- **`--selftest` của bộ điều phối** đổi tên thành `--orchestrator-selftest` (`--selftest` ở tầng `tl` là
  selftest của chính `tl`, main() đọc nó TRƯỚC khi dispatch).

Nguyên tắc hygiene: giữ bản canonical có `nlm_source_id` + cat đúng + số hiệu/hiệu lực; bản trùng/orphan chỉ đưa `QUARANTINE`, không trash, và chỉ chạy apply khi đã có xác nhận. `hygiene plan` không đưa cụm thiếu canonical vào tập apply; đọc `skipped_clusters[].skip_reason=MISSING_CANONICAL_REVIEW_ONLY` để rà tay. `hygiene scan` cũng đếm `title_mismatch_candidates` để soi các dòng tên file/metadata lệch trước khi rà soát, gồm `VBHN_BARE_NUMBER`/`VBHN_MISSING_YEAR_OR_DATE`, bộ cờ VBHN cấp Bộ `VBHN_MINISTRY_SCOPE`/`VBHN_MINISTRY_MISSING_YEAR`/`VBHN_MINISTRY_NAME_MISSING_YEAR`, `NLM_STATUS_MISMATCH`, `NLM_NOTEBOOK_ID_MISSING`, và `CORPUS_TRUE_NOT_ON_NLM`. `duplicate_sohieu_groups_raw` là thống kê thô; ưu tiên đọc `duplicate_identity_groups` khi quyết định dọn thật.

### v1.17.24 amendment gate best-combined
- `tl exists` là cổng chống overclaim thay cho `reg_get name_contains`; miss chỉ là `UNKNOWN_NOT_ABSENT`.
- `source-map` tự đưa `amendment_candidates` và `action_required=PAUSE_AND_ASK_USER` khi phát hiện bản sửa đổi liên quan trong corpus/NLM.
- `vbhn-check --goc` tự suy chủ đề từ manifest nếu thiếu `--subject`, để sinh query web đủ mạnh.

### v1.17.22 stale relation guard
- `vb_status` có thể bỏ lọt văn bản sửa đổi đã có nếu registry thiếu `goc/sua_doi`. Cổng bắt buộc là `relation-check`, không chỉ `status`.
- Khi phát hiện luật mới đã sửa luật đang rà, phải hỏi người dùng để nạp/ghi registry ngay; không ghi vào mục sau nếu việc đó quyết định nguồn rà soát.
- Nếu thiếu VBHN trong corpus, phải search web QT-5 bằng query gợi ý trước khi nói "chưa có"; TVPL/luatvietnam dùng để phát hiện nhanh, official-first để chốt.
- Chi tiết: `references/STALE_RELATION_GUARD.md`.


### v1.17.19 safe issue_year parser
- (Lịch sử) parser `issue_year` an toàn của manifest (từ bản 2.21.2d) tránh lấy nhầm năm từ `tukhoa/keywords` chứa số hiệu luật gốc — giữ qua tới bản LIVE `Code.2.21.2l.gs`.
- Gói khớp LIVE/EXPECT `2.21.2l` (đã xác minh `ping.version`). `Code.2.21.2l.gs` = regen2 own-scope + guard + row_kind; nếu ping khác thì dừng và đối chiếu deploy.


## v1.17.26 combined external-ingest + instruction-audit gate

- Trước mọi nạp nguồn web/NLM-native, chạy `tl external-ingest <url> ... --json` để kiểm kế hoạch. Lệnh này chỉ kiểm, không ghi Drive/NLM.
- `research_start/research_status` chỉ dùng để phát hiện URL; `research_import/source_add(url)` không được dùng để nạp VBQPPL làm nguồn canonical.
- Instruction dùng cho Claude Project/NLM phải qua `tl instruction-audit` hoặc sinh bằng `tl instructions`/`scripts/gen_instructions.py`; thiếu `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web` thì không dùng.
