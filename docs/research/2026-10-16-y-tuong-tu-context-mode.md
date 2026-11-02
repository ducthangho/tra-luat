# Ý tưởng lấy từ context-mode cho kế hoạch tương lai của tra-luat

- **Ngày nghiên cứu:** 2026-10-16
- **Đối tượng:** [`mksglu/context-mode`](https://github.com/mksglu/context-mode) bản `1.0.169`, commit `5f6298a`
  (đọc mã nguồn, **CHƯA cài, CHƯA chạy** — mọi con số tiết kiệm của họ là lời tác giả, chưa đo).
- **Repo/head được kiểm:** `ducthangho/tra-luat` tại `653fef3` (VERSION `1.36.68`).
- **Tính chất:** báo cáo nghiên cứu non-normative. Đây là **DỮ LIỆU cho kế hoạch, KHÔNG phải giao việc** —
  mục nào muốn làm phải có Packet Issue + lease theo `docs/PROTOCOL_DA_PHIEN.md`.

## 1. Kết luận ngắn

**Không tích hợp context-mode** (không MCP server, không hook, không mã của họ) vào skill. Lý do đã nêu ở
phiên nghiên cứu: không cài được trong zip Cowork (Node ≥ 22.5 + `better-sqlite3` native + hook), hook của họ
**chặn WebFetch** rồi đổi HTML→Markdown (turndown) + trả đoạn trích BM25 — trái bất biến §0.2 SKILL.md
("KHÔNG nhận RAG làm nguyên văn"); chồng một đường chặn công cụ thứ hai lên `pretooluse_guard.py`, và chính
họ ghi rằng thiếu module bảo mật thì luật `permissions.deny` **fail-open**; giấy phép ELv2; tự `git pull`
nâng cấp ngoài gate.

Nhưng có **năm ý tưởng** đáng làm lại bằng Python thuần trong khuôn khổ doctrine của kho. Xếp theo giá trị/chi phí:

| # | Ý tưởng | Nơi áp | Giá trị | Chi phí | Đề xuất |
|---|---|---|---|---|---|
| I1 | Chỉ mục định vị FTS5 offline trên cache đã verify | runtime skill | cao | trung bình | packet nghiên cứu + spike |
| I2 | Hợp đồng "đầu ra lớn ra đĩa, context nhận tóm tắt + con trỏ" | runtime skill | cao | thấp | packet sớm |
| I3 | Nhật ký phiên + lệnh `resume` (đề xuất) sống qua compact/phiên mới | runtime + dev | trung bình–cao | trung bình | sau I2 |
| I4 | Hook PreCompact/gợi ý định tuyến phía dev | dev-side | trung bình | thấp | packet nhỏ |
| I5 | Đo byte đã giữ ngoài context (`ctx_stats`) | runtime + dev | trung bình (để ra quyết định) | thấp | đi kèm I2 |

## 2. Từng ý tưởng

### I1. Chỉ mục ĐỊNH VỊ offline (FTS5) — "search để tìm chỗ, extract để trích"

**Họ làm gì:** `ctx_index` / `ctx_search` — đánh chỉ mục nội dung vào SQLite FTS5, xếp hạng BM25, trả đoạn trích.

**tra-luat hiện có:** `tl locate` / `reg-query` tìm theo **số hiệu/tên** trên manifest; định vị theo **nội dung**
("điều nào nói về X") đang dựa vào NLM. `tl extract --dieu N` lấy nguyên văn từ cache. Grep mã nguồn: không có
`fts5`/`bm25`/`sqlite3` nào trong `scripts/`.

**Đề xuất:** hai lệnh MỚI (tên dự kiến, CHƯA tồn tại) `idx-build` · `idx-find <truy vấn>` dùng `sqlite3` của thư viện chuẩn Python (không thêm
phụ thuộc). Chỉ mục theo đơn vị **Điều/Khoản/Mục** từ cache đã verify. Điểm cốt lõi khác họ:

- `idx-find` **KHÔNG trả văn bản** — chỉ trả con trỏ `{sohieu, dieu, khoan, sha256_cache, điểm BM25}`. Nguyên văn
  vẫn đi đúng một đường: `tl extract`. Như vậy chỉ mục đứng đúng vai NLM trong §0.2 ("chỉ định vị"), nhưng
  offline, tất định, không tốn slot NLM và không phụ thuộc NLM sống.
- Mỗi con trỏ mang `sha256` của tệp cache lúc đánh chỉ mục; `extract` đối chiếu, lệch thì cờ `IDX_STALE`.
- Tôn trọng VBHN-first (§0.1): kết quả từ bản gốc khi đã có VBHN còn hiệu lực phải bị hạ hạng/gắn cờ, không bị
  trả ngang hàng.

**Rủi ro phải đo trước (spike):**
1. **FTS5 có trong Python của Cowork không** — container dev có (`sqlite 3.45.1`, tạo bảng `fts5` thành công);
   Cowork **KHÔNG ĐO ĐƯỢC** từ đây. Thiếu thì phải fail-close có thông báo, không âm thầm rơi về quét tuyến tính
   rồi nói như thể đã tìm bằng chỉ mục.
2. **Tách từ tiếng Việt.** `unicode61 remove_diacritics` làm "đất" ≡ "dát" ≡ "đạt" — sai nghĩa pháp lý. Phải so ít
   nhất hai cấu hình (giữ dấu · bỏ dấu + xếp hạng lại theo khớp có dấu) trên bộ truy vấn vàng có đáp án biết trước.
3. Kích thước chỉ mục so với trần Drive/đĩa của Cowork; chỉ mục là **dẫn xuất**, không được đẩy lên Drive làm nguồn.

**Tiêu chí nhận:** bộ golden ≥ 30 truy vấn có điều đích biết trước, đo recall@5 so với NLM trên cùng bộ;
phản chứng: sửa một byte trong cache ⇒ `IDX_STALE`.

### I2. Hợp đồng đầu ra: lớn thì ra ĐĨA, context nhận TÓM TẮT + CON TRỎ

**Họ làm gì:** `ctx_execute` chạy mã trong sandbox, chỉ `console.log` kết quả; dữ liệu thô không vào context.

**tra-luat hiện có:** ý tưởng đã sống rải rác — `extract` ghi toàn văn ra đĩa, nhiều lệnh có `--out f`, agent
`tl-auditor` tiêu hoá log dài, Loop A rà soát có ngưỡng mềm 40% context (`references/RASOAT_HOSO_LOOP.md`).
Nhưng **không có hợp đồng chung**: lệnh nào in bao nhiêu là tuỳ lệnh.

**Đề xuất:** một hợp đồng đo được, áp qua `command_registry`:
- Mỗi lệnh khai `output_budget` (byte). Vượt ngân sách ⇒ ghi đầy đủ ra `.tl_state/out/<lệnh>-<ts>.json`, stdout
  chỉ in tóm tắt + đường dẫn + `sha256` + số dòng/bản ghi bị giữ lại.
- **Ngoại lệ cứng:** nguyên văn điều luật mà người dùng yêu cầu **không bao giờ bị cắt hay tóm tắt** — chỉ được
  chuyển ra đĩa kèm lời báo rõ "nguyên văn ở tệp X". Tóm tắt nguyên văn là vi phạm §0.2.
- `workflow-audit` kiểm mọi lệnh trong registry đều có `output_budget`.

**Tiêu chí nhận:** ca test cho một lệnh vượt ngân sách (stdout ≤ ngân sách, tệp có đủ bản ghi, `sha256` khớp);
đột biến bỏ chốt ⇒ ca ĐỎ.

### I3. Nhật ký phiên + lệnh `resume` (đề xuất)

**Họ làm gì:** ghi mọi sửa tệp/thao tác git/lỗi/quyết định của người dùng vào SQLite; khi compact chỉ nạp lại
phần liên quan.

**tra-luat:** Loop A có state riêng; các việc khác (ingest lô, đối soát NLM, sắp xếp) mất mạch khi compact hoặc
khi sang phiên Cowork mới. Đã có các artefact rời (`reconcile_plan_<nb>.json`, `migrate_resume_<to>.json`).

**Đề xuất:** `.tl_state/journal.jsonl` (chỉ thêm, mỗi dòng có `ts`, lệnh, tham số đã che bí mật, rc, con trỏ
artefact) và lệnh MỚI (chưa tồn tại) `resume [--json]` in ≤ 2KB: việc đang dở, artefact resume còn hạn, lệnh kế tiếp gợi ý. Cowork
không có hook ⇒ ghi từ chính `tl` (mọi lệnh ghi), không trông vào hook. SKILL.md thêm một dòng: "mở phiên → chạy `resume`".

**Ràng buộc:** journal không bao giờ chứa token/cookie (dùng chung bộ che của `pkg_secret_scan.py`); journal là
**bằng chứng đã gọi**, không phải bằng chứng trạng thái — trạng thái registry/NLM vẫn phải đo LIVE
(bài học "registry claim NLM là ESTIMATE").

### I4. Phía dev: hook PreCompact + gợi ý định tuyến mềm

**Họ làm gì:** PreCompact chụp trạng thái phiên; PreToolUse nhắc dùng công cụ sandbox thay vì đọc thô.

**Đề xuất (chỉ `.claude/`, không vào gói):**
- `PreCompact` (hiện `.claude/settings.json` chỉ có `SessionStart`, `PreToolUse`, `SubagentStart`, `SubagentStop`):
  ghi `git status`, nhánh, packet/lease đang giữ, các lệnh gate gần nhất kèm `N/N` vào `.claude/.packet_state/`.
- Trong `pretooluse_guard.py`: khi `Read`/`cat` một tệp cache corpus lớn hoặc output selftest, **nhắc** (không
  chặn) dùng `tl extract` / giao `tl-auditor`. Chỉ nhắc — không thêm đường chặn thứ hai, và không bao giờ
  fail-open âm thầm như bản của họ.
- Dùng đường dẫn `$CLAUDE_PROJECT_DIR` (bài học hook tương đối tự khoá).

### I5. Đo byte đã giữ ngoài context

**Họ làm gì:** `ctx_stats` — mỗi công cụ đã giữ lại bao nhiêu byte.

**Đề xuất:** đi cùng I2: mỗi lần chuyển ra đĩa ghi `{lệnh, byte_đầy_đủ, byte_in}` vào journal (I3); `resume
--stats` cộng lại. Mục đích là **dữ liệu để chọn lệnh nào cần ngân sách chặt hơn**, không phải con số quảng cáo.

## 3. Không lấy (và vì sao)

- **Chặn/định tuyến lại WebFetch, fetch-and-index trả đoạn trích:** trái §0.2 và "official-first"; đổi định dạng
  trước khi lưu làm mất khả năng chứng minh byte gốc.
- **Hook làm lớp bảo mật có thể fail-open:** trái doctrine fail-close của kho.
- **Tự nâng cấp (`ctx_upgrade`, kiểm npm registry):** mã chảy vào ngoài gate.
- **Ép phong cách trả lời:** họ cũng không làm; ghi ra để khỏi ai đề xuất.

## 4. Bước kế tiếp gợi ý

1. Người giữ kho chọn mục (khuyến nghị thứ tự **I2 + I5 → I1 spike → I3 → I4**).
2. Mỗi mục được chọn: `soan-spec` → `ops/specs/<packet-id>.md` có `spec_hash` → Packet Issue + lease → làm.
3. I1 cần spike riêng trên Cowork thật để trả lời câu hỏi FTS5 + tách từ tiếng Việt **trước** khi soạn spec.
