# tra-luat — GOTCHAS (bẫy ĐÃ TRẢ GIÁ, nhóm theo chủ đề)

> G2 (§11 kế hoạch guard-va-boc-tl-core, v1.34.66): các bẫy nóng trước đây phân mảnh trong CHANGELOG/
> memory phiên — agent tiêu thụ skill KHÔNG thấy. File này gom TRÍCH nguyên văn, nhóm theo CHỦ ĐỀ.
> Con trỏ chuẩn: `references/RUNBOOK.md` → đây. Đọc TRƯỚC khi: release, sửa registry, viết script mới,
> move/tách module. Chi tiết từng vụ: CHANGELOG.md theo version ghi kèm.

## 1. Trần mount & size (lớp sự cố #5)

- **Trần mount ~343KB/file** — `tl.py` từng bị **CẮT CỤT** khi vượt (Cowork mount); self-heal chỉ cứu
  NUL-pad, **KHÔNG cứu cắt cụt**. Guard sống ở `workflow-audit`: `py_size` WARN >280KB / FAIL --strict
  >320KB (waiver `tl_selftest.py` — không bước Cowork nào import; hỏng thì fail ỒN ÀO).
- **Kernel SKILL.md ≤ 49.152B (48K)** — trần SÁT NHẤT toàn hệ (hiện ~49.145B, đệm 7B); WARN >47KB
  (G1a). Đổi kernel ⇒ user re-import Capabilities. Muốn thêm chữ vào kernel: bớt chữ chỗ khác trước.
- **Bundle import ≤200 file** — cây dev 212 file từng import FAIL; đóng gói CHỈ qua `tl release-bundle`
  (không zip cây dev thô).

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
- **Repo ghi LF** (`* -text` khoá byte); riêng `references/COMMANDS.md` là **CRLF toàn phần** — chèn dòng
  phải CRLF khớp, KHÔNG mass-strip trailing-space (125 dòng cũ vốn có ` |` + CR).
- **Commit message qua `-F <file>`** (tiếng Việt/ký tự đặc biệt an toàn); secret-guard hook quét trước.
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
- docx/pdf GỐC + GDoc CONVERT cùng văn bản = **KHÔNG trùng** (định nghĩa chốt 2026-07-16); chỉ trùng khi
  ≥2 GDoc hoặc ≥2 docx cùng nội dung — text convert lệch nhẹ nên cặp hợp lệ hay rơi dải NEAR (soi
  `type` chứa `|`).

## 8. Windows console / heredoc

- Console cp1258: in tiếng Việt từ python -c/heredoc nổ UnicodeEncodeError — chạy với `PYTHONUTF8=1`
  (+`PYTHONIOENCODING=utf-8`); subprocess con cũng thừa hưởng.
- Heredoc bash+python: chuỗi có `\t` thành TAB thật — ghi path Windows từ heredoc dùng `chr(92)`/raw.
- Subprocess đổi `cwd` (fake-home): path script phải **TUYỆT ĐỐI** (`.../scripts/tl.py`), không tương đối.
- Tool đọc file không nhận path Unicode `D:\Quốc hội` → dùng junction `C:\qh`.

## 9. NLM vận hành

- **Cookie DBSC đời ~1h** — `nlm login` là đủ; tuổi >45' nên re-auth trước lô dài / chuyển `nlm-links`
  (batch >2 file đi đường batch-link).
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
  + convert GDoc. File rất lớn → cân nhắc đường gws CLI (backlog), KHÔNG đổi đường ingest chuẩn.
- Readback sau lô: `reg-query` 1 LẦN cuối (KHÔNG `--refresh` giữa chừng — mỗi refresh kéo registry đầy).
