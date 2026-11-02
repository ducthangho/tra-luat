# tra-luat — GOTCHAS (bẫy ĐÃ TRẢ GIÁ, nhóm theo chủ đề)

> G2 (§11 kế hoạch guard-va-boc-tl-core, v1.34.66): các bẫy nóng trước đây phân mảnh trong CHANGELOG/
> memory phiên — agent tiêu thụ skill KHÔNG thấy. File này gom TRÍCH nguyên văn, nhóm theo CHỦ ĐỀ.
> Con trỏ chuẩn: `references/RUNBOOK.md` → đây. Đọc TRƯỚC khi: release, sửa registry, viết script mới,
> move/tách module. Chi tiết từng vụ: CHANGELOG.md theo version ghi kèm.
>
> **NHÃN (r219):** không nhãn = bẫy CÒN hiệu lực · `[B]` = tiền đề **BỊ BÁC** bởi đo về sau,
> theo câu thay thế, đừng theo câu gốc. Chỉ dán ở chỗ trạng thái ĐÃ ĐỔI; sửa CÂU trước khi dán.

## 1. Trần mount & size (lớp sự cố #5)

- **Trần mount ~343KB/file** — `tl.py` từng bị **CẮT CỤT** khi vượt (Cowork mount); self-heal chỉ cứu
  NUL-pad, **KHÔNG cứu cắt cụt**. Guard sống ở `workflow-audit`: `py_size` WARN >280KB / FAIL --strict
  >320KB (waiver `tl_selftest.py` — không bước Cowork nào import; hỏng thì fail ỒN ÀO).
- **Kernel SKILL.md: WARN >48.128B (G1a) · CỨNG 49.152B** — đo 30-10 (LF): **47.925B, đệm 203B** tới WARN.
  Đổi kernel ⇒ re-import Capabilities. Thêm chữ: bớt chỗ khác TRƯỚC.
- **Bundle import ≤200 file** — cây dev 212 từng FAIL; đóng gói CHỈ qua `tl release-bundle`.

## 2. I11 / stub-farm / bind-REBASE (tách module)

- **Hằng module-level KHÔNG vào `_STUB_MAP`** — stub là *function*; hằng vào stub → so sánh int/tuple NỔ.
  Hằng mới/di chuyển = **re-export TRỰC TIẾP** trong `tl.py` (`X = _tl_<mod>.X`), đổi nguồn CÙNG commit
  với move.
- **Move theo DANH-SÁCH-TÊN, KHÔNG sweep tự động** — máy-sweep affinity từng chuyển nhầm
  `_json_dumps` → `ocr.py` (r61 cấm token). Ranh giới = danh sách chốt trong kế hoạch.
- **Drift 2 LỚP khi move**: lớp 1 = `__tl_stub__` tuple (r71/r75/r81 pin); lớp 2 = tham chiếu
  `inspect.getsource(<module>.<fn>)` / alias `import tl_core.X as _y` trỏ THẲNG module nguồn (ca thật:
  test recat 1.23.6, r69 `_no69.cmd_nlm_add`, r83 ×4). **Quét getsource/alias TRƯỚC khi move.**
- Hàm rebase đọc **globals của tl** — stdlib trong module mới phải import tường minh (`# noqa: F401`);
  tuple-keys nội hàm giữ INLINE (hằng module không vào globals tl nếu quên re-export → NameError).

## 3. Nghi thức release (bẫy từng ăn oan)

- **`release-manifest` mặc định DRY** — regen thật PHẢI `--out RELEASE_MANIFEST.json` (in ok=true nhưng
  KHÔNG ghi → release-verify đỏ oan). Manifest regen là bước **CUỐI** sau mọi sửa file.
- **Golden `workflow_audit` NHÚNG size SKILL.md + files_scanned** — mọi chỉnh SKILL.md/thêm file runtime
  phải `golden-test --write` LẠI (CÓ CHỦ ĐÍCH, diff phải giải thích được từng dòng) rồi mới manifest.
  **Golden diff bất ngờ = BUG — DỪNG, cấm --write che.**
- `[B]` **«Khoá byte `* -text`, sửa EOL bằng BYTE» — BỊ BÁC (F2, ADR-0018).** `.gitattributes` ép
  LF mọi text (`*.cmd`/`*.bat` CRLF; golden + binary `-text`); `.githooks/eol_policy.py` chặn CRLF
  vào index, hook và CI chung lõi. Phái sinh ghi qua `_write_text_atomic` (canonical LF);
  `newline="\n"` KHÔNG đủ — không đụng `\r` có sẵn.
- **Commit message qua `-F <file>`** (tiếng Việt an toàn); secret-guard hook quét trước.
- Gate phải kiểm **rc THẬT từng lệnh, output ra file rồi mới parse** — `cmd | python -c ...` từng NUỐT rc
  → commit lọt khi gate ĐỎ (xem `.claude/commands/gate.md`).

## 4. Lazy-creds / offline-first

- Lệnh offline-first MỚI **PHẢI vào `_CREDS_LAZY_CMDS`** (tl.py) — thiếu → `main()` `load_creds`
  sys.exit TRƯỚC handler trên máy không config (CI máy-trắng bắt; local pass vì có config → ảo giác xanh).
- Trong handler lazy: `load_creds` **best-effort NGAY ĐẦU** (try/except nuốt SystemExit) — cache/local
  chạy không token, đường export tự fail sạch; GAS chết giữa fallback từng nổ 'Thiếu TL_WEBAPP/TL_TOKEN'.

## 5. Journal / HOME / .tl_state

- **Journal ghi theo HOME** (`~/.tl_journal`) — smoke fake-home phải copy journal về home thật mới undo
  được; intent thiếu `before` khi verify fail → undo_ops=0 (revert chuẩn = `register --clear-cols`).
- **`.tl_state/` là REPO-relative** (`scripts/.tl_state`), KHÔNG theo HOME — fake-home KHÔNG cô lập nó
  (listing-cache C-#8, resume-artifact, charact đều nằm đây); field tuổi (`age_s`) tick theo đồng hồ.
- Fake-home có **2 tầng đúng mục đích**: GAS-chết (config giả `webappUrl:""` — lỗi nội bộ tất định,
  0 mạng; cho characterization) ≠ GAS-sống/NLM-chết (config thật, không `.notebooklm-mcp-cli`/
  `.config/gws`; cho dead-path E2/E3 thật). Lệnh non-lazy cần tầng 2.

## 6. Ghi registry (GAS webapp)

- **Ghi giá trị RỖNG qua `reg_bulk`/`reg_upsert` bị webapp BỎ QUA im lặng** — xoá field phải đi
  **`reg_clear`** (`_journaled_reg_clear`); cột đúng là `sohieu` (KHÔNG `so_hieu`) khi reg_bulk.
- **Readback field-level có thể ÂM TÍNH GIẢ dưới GAS cache** (~600s) — verified=False chưa chắc write
  fail; đường quyết định phải **re-check AUTHORITATIVE `reg_get_bulk`** trước khi kết luận (khuôn
  v1.34.62); journal `run_end` = verdict CUỐI.
- Registry claim NLM là **ESTIMATE** — slot/FULL/overflow phải neo `nlm-get`/`nlm-reconcile` LIVE.
- Đọc row cache manifest thô: key là **`gdoc_id`/`id`** (không phải `drive_id`) — dùng bộ alias như
  `_entry_drive_id`, đừng đọc 1 key trần.

## 7. Dedup / data-op văn bản

- **md5-group có thể là 2 tên LUẬT KHÁC NHAU cùng bytes** (gán-nhãn-sai) — KHÔNG xóa mù; content-verify
  header quyết định tên đúng (số hiệu thắng tên file).
- **`dedup-plan --apply` picker có thể chọn NGƯỢC** (ca 59-2023: lấy .docx thô làm canonical) — dùng
  `dedup-corpus` (picker on-NLM-first) hoặc tự phân vùng + verify trước.
- `_read_doc_text` với `.docx` trả **BINARY zip** — text .docx thật = `tl doc-text` (unzip
  `word/document.xml`); so nội dung bằng content-hash/bag-of-words, KHÔNG so char-count text-vs-binary.
- Mọi số hiệu/tên VBQPPL **phải có NĂM** (số tái dùng theo năm → collision, nhất là VBHN).
- docx/pdf GỐC + GDoc CONVERT cùng văn bản = **KHÔNG trùng**; chỉ trùng khi ≥2 GDoc hoặc ≥2 docx cùng
  nội dung — text convert lệch nhẹ nên cặp hợp lệ hay rơi dải NEAR (soi `type` chứa `|`).

## 8. Windows console / heredoc

- Console cp1258: in tiếng Việt từ python -c/heredoc nổ UnicodeEncodeError — chạy với `PYTHONUTF8=1`
  (+`PYTHONIOENCODING=utf-8`); subprocess con cũng thừa hưởng.
- Heredoc bash+python: chuỗi có `\t` thành TAB thật — ghi path Windows từ heredoc dùng `chr(92)`/raw.
- Subprocess đổi `cwd` (fake-home): path script phải **TUYỆT ĐỐI** (`.../scripts/tl.py`), không tương đối.
- Tool đọc file không nhận path Unicode `D:\Quốc hội` → dùng junction `C:\qh`.

## 9. NLM vận hành

- `[B]` **«Cookie DBSC đời ~1h, `nlm login` là đủ» — BỊ BÁC (đo 26+27-07).** Không cookie nào TTL 1h;
  chết do token XOAY `__Secure-1PSIDRTS` CLI không xoay lại ⇒ giờ chết KHÔNG đoán trước, đừng hứa "còn
  N phút". **`nlm login` TRẦN = NO-OP** (probe homepage → xanh giả, rc=0) ⇒ phải `--force`; verdict
  `all_failed` ⇒ `--clear`. Lô dài chuyển `nlm-links` (batch >2 file).
- NLM chết ≠ dừng: đọc → fallback corpus (verbatim-return, KHÔNG máy sinh RAG); ghi → DEFER (không
  corpus-ảo); audit/plan trên cache stale = **belief** (`UNVERIFIED_NLM_STATE`) — không xử theo.
- `nlm-migrate --apply` cần đúng 1 bộ lọc (`FILTER_REQUIRED` fail-closed); NLM chết → KHÔNG ghi trên
  belief, chỉ BATCH_LINKS + resume-artifact (`--from-plan` chạy nốt khi sống).

## 10. PERF nạp lô (mổ xẻ 30 phút / 3 file — 2026-07-19)

- **Chờ NLM settle mặc định ăn ≈NỬA thời gian mỗi `ingest-local --apply`** (journal đo ~260s/file).
  Nạp LÔ ≥2 file: `--nlm-no-wait` (−~50%/file) + `tl nlm-reconcile <nb> --apply` MỘT lần cuối lô;
  3 lệnh chạy SONG SONG được (upload/organize stateless, reg_bulk nguyên tử). Lô lớn: `--no-nlm-add`
  → `nlm-links` batch → reconcile. Đơn lẻ giữ mặc định verify-then-link (an toàn v1.34.56).
- **Upload đi b64 qua webapp là BẮT BUỘC** (Apps Script doPost không nhận multipart binary; trần 35MB).
  Với file <1MB b64 KHÔNG phải bottleneck (phình +33% ≈ <1s mạng) — độ trễ nằm ở Apps Script runtime
  + convert GDoc. File rất lớn → cân nhắc gws CLI (backlog).
- Readback sau lô: `reg-query` 1 LẦN cuối (KHÔNG `--refresh` giữa chừng — mỗi refresh kéo registry đầy).

## 11. Chẩn đoán sự cố registry + phiên REMOTE (bài học 2026-07-25)

- **`nlm-reconcile` báo ~100% nguồn live thành `unregistered` KHÔNG mặc nhiên là bệnh kênh liệt kê.**
  Ca thật 25-07: registry nền bị xoá còn **2 dòng** → 300/300 unregistered, trong khi `tl nlm-auth-status`
  báo `alive:true`, cookie mới 6,6′. Guard r201 chỉ nhìn TỶ LỆ nên hô nhầm `LISTING_CHANNEL_SUSPECT` +
  playbook `nlm login` — chữa nhầm bệnh. Từ r206 guard soi thêm `registry_rows_seen` và hô
  `REGISTRY_SCOPE_SUSPECT` khi registry mỏng (<20% số live). **Dù verdict nào cũng ĐỪNG `--force-unsafe`**
  trước khi `tl counts --refresh` xác nhận registry còn đủ dòng.
- **`tl counts` KHÔNG kèm `--refresh` đọc SNAPSHOT cache** (`snapshot NNNs`) — có thể là ảnh cũ của trạng
  thái đã hỏng. Phân định sự cố 25-07 chính nhờ so cached (2 dòng) với `--refresh` (1300 dòng). Mọi kết
  luận "mất dữ liệu" phải chốt bằng `--refresh`, không chốt bằng snapshot.
- **`tl journal` là file CỤC BỘ theo máy/clone.** Thao tác chạy từ clone khác (`C:\qh` vs `D:\...`), phiên
  Cowork/Chat, hay máy khác KHÔNG xuất hiện ở đây — journal sạch KHÔNG đồng nghĩa "không ai ghi". Truy
  nguyên có thẩm quyền: **version history của Sheet registry** (mốc giờ + tài khoản từng revision) và
  **Apps Script → Executions** (mọi `doPost/doGet` bất kể client). Journal chỉ là manh mối thứ ba.
- **`profile-delete-assets` xoá ĐÚNG scope** (kiểm 25-07 qua 4 lần chạy: 0/16 id trùng tài sản nền —
  mỗi lần đúng 1 Sheet + 3 thư mục của CHÍNH profile đó). Đừng đổ tội cho nó khi chưa đối chiếu id —
  so `done_keys` của `tl journal <run_id> --json` với `registryDocId`/`rootFolderId`/`manifestId`/categories
  trong `tl profile-info --json`.
- **Phiên Claude Code REMOTE (web) KHÔNG chạy được lệnh live**: egress policy chặn `script.google.com`,
  `notebooklm.google.com`, `drive.usercontent.google.com` (403 tại CONNECT — xem `curl "$HTTPS_PROXY/__agentproxy/status"`).
  Muốn mở: environment → Network access → **Custom** + `*.google.com`, `*.googleusercontent.com`,
  `*.googleapis.com`, nhớ tick "include default list" (giữ npm/pypi). **Bẫy dễ sót: `script.googleusercontent.com`** —
  GAS redirect payload phản hồi sang host này, thiếu nó thì mọi call webapp vẫn chết dù đã mở `script.google.com`.
  Drive MCP VẪN sống khi Google bị chặn (traffic connector đi qua server Anthropic, không qua egress sandbox)
  → "Drive đọc được" KHÔNG mâu thuẫn với "webapp chết".
- **Clone tươi báo 12 `F821` là GIẢ**: các tên bơm động vào `globals()` qua vòng `_STUB_MAP` (`tl.py`)
  — `build_parser`, `load_creds`, `_active_profile`… Selftest xanh là bằng chứng runtime resolve đúng.
  Chỉ coi là bug khi số F821 LỆCH khỏi baseline này.
