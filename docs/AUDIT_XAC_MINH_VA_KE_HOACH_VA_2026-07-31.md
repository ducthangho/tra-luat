# Xác minh audit lõi tra-luat + kế hoạch vá hợp nhất

- Ngày xác minh: 2026-07-31
- Nguồn: `audit_tra_luat_loi.md` (baseline `master@b1a86c8`, VERSION 1.36.21) + `ke_hoach_va.md`
- **Cây xác minh: `HEAD = 19a6adf` (v1.36.22, r284)** — muộn hơn baseline audit 1 commit
- Chế độ: offline/dry-run, không `--apply`, không ghi LIVE, không sửa mã sản xuất trong lượt này

---

## 1. Kết luận xác minh

| Trạng thái | Số lượng |
|---|---:|
| **TÁI HIỆN ĐƯỢC ở HEAD** (audit ĐÚNG) | **33/34** |
| **ĐÃ ĐÓNG ở HEAD** (audit đúng lúc đo, nay hết) | **1** — GATE-02 |
| Audit sai / dương tính giả | **0** |
| **LỖI MỚI phát hiện trong lượt xác minh** | **1** — GATE-03 (P1, ĐANG CHẶN GATE) |

**Tổng việc còn mở: 34** (33 cũ + 1 mới).

Audit có chất lượng cao: mọi vị trí trích dẫn đều trỏ đúng hàm, mọi mô tả cơ chế đều khớp mã.
Ba điểm cần chỉnh lại về *diễn giải* (không phải về *sự tồn tại* của lỗi) — xem §3.

### Trạng thái gate đo THẬT trên cây này

| Gate | Kết quả | Ghi chú |
|---|---|---|
| `tl --selftest` | **1490/1491 — ĐỎ** | 1 ca đỏ = **GATE-03** (mới), xem §2.1 |
| `workflow-audit --strict --json` | `ok:true` | 26 card, 187 command, 0 error/warning |
| `golden-test --json` | `ok:true`, 20/20 case | **`raw_stable` = true cho CẢ 20** (xem §3.1) |
| `gen_instructions.py --selftest` | 38/38 | |
| `doc-claims-check --strict --json` | `ok:true`, `flags=[]` | |
| ruff | **KHÔNG đo được** | `No module named ruff` trong container này — ngưỡng 12 F821 / 0 F401 phải đo trên máy chuẩn |

---

## 2. Hai thay đổi so với sổ lỗi audit

### 2.1 GATE-03 — LỖI MỚI, P1, ĐANG CHẶN GATE TRÊN LINUX/COWORK

Ca `r284_khung_test_profile_khong_doc_config_that` — chính **chốt chặn tái phát mà r284 vừa thêm** —
ĐỎ trên Linux. Đây là **cùng lớp lỗi máy-phụ-thuộc mà r284 sinh ra để chặn**, chỉ đảo nền.

`scripts/tl_selftest.py:11182`:

```python
_cands = [c for c in _TL_MODULE._config_candidates(None) if not c.startswith("/tmp/")]
...
return bool(_cands) and all(Path(c).resolve().is_relative_to(_real) for c in _cands)
```

Bộ lọc `startswith("/tmp/")` sinh ra để loại **hằng cuối hàm** `/tmp/tra_luat_config.json`
(comment ghi rõ: *"không tồn tại trên máy Windows, bỏ qua"*). Nhưng trên Linux
`tempfile.TemporaryDirectory()` trả `/tmp/tmpXXXXXXXX` ⇒ **MỌI ứng viên đều bắt đầu bằng `/tmp/`**
và bị loại sạch ⇒ `_cands == []` ⇒ `bool(_cands)` False ⇒ FAIL.

Đo trực tiếp (6 ứng viên, tempdir `/tmp/tmpurag15xo`):

```
/tmp/tmpurag15xo/tra_luat_config.v2.json          inside=True   ← bị lọc oan
/tmp/tmpurag15xo/tra_luat_config.json             inside=True   ← bị lọc oan
/tmp/tmpurag15xo/scripts/tra_luat_config.v2.json  inside=True   ← bị lọc oan
/tmp/tmpurag15xo/scripts/tra_luat_config.json     inside=True   ← bị lọc oan
/tmp/tmpurag15xo/.tra_luat_config.json            inside=True   ← bị lọc oan
/tmp/tra_luat_config.json                         inside=False  ← ĐÚNG là cái cần loại
```

**Hệ quả vận hành:** `deploy-package.sh` bước 1 chạy selftest ⇒ đường deploy Linux/Cowork **ĐỎ ngay**,
trong khi đường Windows XANH. Đúng vết xe đổ CLAUDE.md §"Script đa nền: PHẢI chạy THẬT trên nền đó,
rồi ĐỐI CHIẾU PARITY". r284 chỉ được kiểm trên Windows.

**Vá (test-only, 1 dòng):** lọc theo **bằng đúng hằng**, không theo tiền tố:

```python
_HANG_CUOI = "/tmp/tra_luat_config.json"           # hằng cuối _config_candidates
_cands = [c for c in _TL_MODULE._config_candidates(None) if c != _HANG_CUOI]
```

Kèm phản chứng: khẳng định `_HANG_CUOI` THỰC SỰ còn nằm trong `_config_candidates(None)` — nếu ai đổi
hằng đó, test phải đỏ ở đây chứ không im lặng lọc hụt.

### 2.2 GATE-02 — ĐÃ ĐÓNG, gỡ khỏi sổ

r284 (`19a6adf`) đã vá đúng nguyên nhân audit chỉ ra: khung cô lập r281/r283 dời HOME/USERPROFILE/cwd
nhưng **không dời `_TL_MODULE.HERE`**, mà `_config_candidates` xếp `HERE.parent` TRƯỚC `~/…`.
Vá dời luôn `HERE` sang `<tempdir>/scripts`, khôi phục trong `finally` — **đúng hướng Slice G0.2 đề ra**
("không đổi ưu tiên config runtime chỉ để làm test xanh"). 6 ca r281 + 1 ca r283 nay XANH.

⇒ **Bỏ Slice G0.2 khỏi kế hoạch. Thay bằng Slice G0.0 (GATE-03).**

---

## 3. Ba điểm chỉnh diễn giải (lỗi vẫn CÓ, mức phơi nhiễm khác audit mô tả)

### 3.1 GATE-01 — cơ chế ĐÚNG, nhưng hiện là lỗ TIỀM ẨN, không phải đỏ đang hoạt động

Cơ chế fail-open **tái hiện chính xác** bằng harness bơm raw drift (cùng projection, khác byte stdout):

```
WRITE  mode -> top ok: True | case ok: True | raw_stable: False | written: True
VERIFY mode -> top ok: True | case ok: True | raw_stable: False
```

`scripts/tl_core/workflow.py:1645-1648`: `raw_stable` được tính, thậm chí sinh `raw_diff`, nhưng
`rec["ok"]` chỉ dẫn xuất từ so sánh **projection**. `--write` vẫn ghi fixture khi raw bất định.
⇒ Vi phạm "kết quả tất định" trong CONTEXT.md: **đã báo mà không cưỡng chế**. Giữ P1.

**Chỉnh:** audit nói *"case thật `sweep` cũng lệch `snapshot_age_s`"*. Chạy `golden-test --json` hai lượt
trên cây này: **20/20 case `raw_stable=true`, không case nào lệch.** `snapshot_age_s` nằm trong
`volatile_keys` nên đã được scrub ở projection; raw chỉ lệch khi tuổi cache **vắt qua mốc giây nguyên**
giữa hai lượt chạy — nghĩa là bất định **theo thời điểm**, không phải luôn luôn.

**Hệ quả cho kế hoạch (quan trọng):** nếu cưỡng chế `raw_stable ⇒ ok=false` mà chưa đóng băng clock của
`sweep` TRƯỚC, gate sẽ **đỏ chập chờn** (đỏ khi xui, xanh khi may) — đúng lớp gate không đáng tin mà
Pha 0 muốn diệt. **Slice G0.1 phải làm ĐÚNG thứ tự: đóng băng clock trước, cưỡng chế sau**, không
làm ngược, không làm cùng lúc.

### 3.2 PRO-04 — chỉ va trên Windows

`_profile_cache_component` (`profile_env.py:266-281`) trả **nguyên tên** khi tên "hợp lệ" ⇒
`Alpha` → `Alpha`, `alpha` → `alpha`. Trên Linux là hai thư mục khác nhau; **trên Windows là MỘT**
(`normcase` bằng nhau). Máy chuẩn của người giữ là Windows ⇒ **giữ P1**, nhưng test khoá phải là
**test parity hai nền** theo doctrine CLAUDE.md, không phải test chỉ chạy trên Linux (sẽ xanh giả).

### 3.3 ING-02 — danh sách cờ thiếu: đã đối chiếu bằng `--help` THẬT, audit đúng từng cờ

| Lệnh | Cờ CÓ trong CLI | Có trong `options` của plan hash? |
|---|---|---|
| `ingest-local` | `--replace-sohieu` | **KHÔNG** |
| `ingest-local` | `--no-fallback` | **KHÔNG** |
| `profile-ingest` | `--allow-dup-name` | **KHÔNG** |
| `profile-ingest` | `--no-nlm-add` | **KHÔNG** |
| `profile-ingest` | `--no-fallback` | **KHÔNG** |

(`ingest_ops.py:1671-1682` và `:2740-2752`.) Cả hai đều **không khoá hash sidecar/manifest OCR**.
⇒ Cùng `plan_hash` cấp quyền cho hành vi khác nhau. Vi phạm ADR-0006/0013. Audit **đúng nguyên văn**.

---

## 4. Sổ xác minh đầy đủ — 34 mục

Cột **Bằng chứng** ghi cách xác minh: `HARNESS` = chạy repro; `ĐỌC+ĐO` = đọc mã + đo hành vi phụ trợ
(`--help`, grep toàn kho, thực thi lệnh).

### 4.1 Gate chung

| ID | Mức | Verdict | Bằng chứng ở HEAD |
|---|---:|---|---|
| GATE-01 | P1 | **ĐÚNG** (tiềm ẩn) | HARNESS: `raw_stable=False` + `ok=True` ở CẢ write lẫn verify; write vẫn ghi fixture. Hiện 20/20 case raw ổn định — xem §3.1 |
| GATE-02 | P1 | **ĐÃ ĐÓNG** | r284 dời `_TL_MODULE.HERE` vào tempdir; 7 ca r281/r283 xanh |
| **GATE-03** | **P1** | **MỚI — ĐANG ĐỎ** | HARNESS: `_cands=[]` do lọc `/tmp/` — selftest 1490/1491 trên Linux; xem §2.1 |

### 4.2 Ingest

| ID | Mức | Verdict | Bằng chứng ở HEAD |
|---|---:|---|---|
| ING-01 | P1 | **ĐÚNG** | `ocr.py:487-494` `_bridge_run_child_apply`: chạy child DRY **lúc apply**, lấy `plan_hash` vừa sinh, tự gắn `--expected-plan-hash`. Hash người dùng duyệt ở lượt DRY trước **không hề được so**. `--confirm yes` có chặn người, **không** chặn nội dung đổi giữa DRY và apply |
| ING-02 | P1 | **ĐÚNG** | Bảng §3.3 — 5 cờ đổi-hành-vi ngoài hash, cả hai đường |
| ING-03 | P1 | **ĐÚNG** | ĐỌC+ĐO: `grep upsert_done scripts/tl_core/*.py` → **đúng 1 hit** (`ingest_ops.py:1502`) và hit đó chỉ dùng để **đặt tên bước lỗi**. Caller `:1836` và `:3079` gate bằng `org.get("fileId")` ⇒ response `ok:false` + `upsert_done:false` mà có `fileId` vẫn **đi tiếp** |
| ING-04 | P1 | **ĐÚNG** | `ingest_ops.py:2202-2240`: nhánh mismatch bị **bỏ qua khi `drive_id` rỗng**; nhánh journal chỉ đòi `plan_hash`/`identity_hash` **tồn tại**, không **so với plan hiện hành**, không so `source_sha256` |
| ING-05 | P2 | **ĐÚNG** | `ingest_ops.py:1975-1992`: nhánh `--no-nlm-add` in kết quả rồi `return {"stop":"DONE"}` — **không** `_journal_append(..., "run_end")`. Đối chiếu: nhánh thường có run_end ở `:2045` |
| ING-06 | P2 | **ĐÚNG** | `zip_ingest.py:39` `_ALLOWED_INGEST_EXTS ⊇ {".txt",".md"}` vs `ingest_ops.py:2608` `allowed_exts={".docx",".doc",".pdf",".rtf",".odt"}`. Member `.txt` được lên plan rồi child chết chắc |
| ING-07 | P2 | **ĐÚNG** (+ xác định được BÊN NÀO SAI) | Bảng cứng `workflow.py:220` = `content-v2: norm_path+crc32+size`; card `references/workflows/ingest_zip.json` = `content-v3: NFC portable_path+sha256+size`. **Mã thật tính `sha256`** (`zip_ingest.py:~296`) ⇒ **card ĐÚNG, bảng cứng LỖI THỜI**. `workflow-audit --strict` xanh, không bắt |
| ING-08 | P3 | **ĐÚNG** (Windows console) | `ingest_to_cache.py:754` `print(json.dumps(..., ensure_ascii=False))` chạy **SAU** `_write_json_atomic` ⇒ cache đã ghi rồi mới có cơ hội chết Unicode. `tl cache-build` không dính (đã chuẩn hoá UTF-8) |

### 4.3 Profile

| ID | Mức | Verdict | Bằng chứng ở HEAD |
|---|---:|---|---|
| PRO-01 | P1 | **ĐÚNG — nặng nhất nhóm** | `ops_misc.py:1784-1806`: `_dr`/`r` chỉ được **ghi nhật ký**, không kiểm; `reg_delete` chạy **vô điều kiện** với `require_removed="no"`; kết luận **`ok: True` gán cứng**, `return 0`. Mọi bước con hỏng vẫn `rc=0`, mà **con trỏ registry đã bị tháo** ⇒ tài sản mồ côi không còn đường tìm lại |
| PRO-02 | P1 | **ĐÚNG** | `_marker_required_keys` (`:1595-1604`) v2 = `profile, rootFolderId, metaFolderId` (+3 khi `manifestScope=own`) — **không có `fingerprint`**; `_marker_validate:1655` kiểm fingerprint **chỉ khi nó tồn tại** ⇒ **bỏ trường fingerprint đi là qua sạch** |
| PRO-03 | P1 | **ĐÚNG** | `profile_mgmt.py:864-878`: chuỗi kiểm chỉ có error/duplicate/name-conflict rồi **ghi đè**. **Không gọi `_marker_mutation_guard`, không gọi `_marker_validate`** ⇒ marker `FINGERPRINT_MISMATCH` bị self-heal im lặng |
| PRO-04 | P1 | **ĐÚNG (Windows)** | §3.2 |
| PRO-05 | P2 | **ĐÚNG** | `profile_env.py:775`: `if role == "registry" and mime != REGISTRY_SHEET_MIME` — vòng lặp chạy cho cả `manifest` nhưng **điều kiện MIME khoá cứng vào `registry`** |
| PRO-06 | P2 | **ĐÚNG** | `profile_mgmt.py:220` `"ok": True` gán cứng ở nhánh có config, độc lập `profile_found` ⇒ `rc=0` |
| PRO-07 | P2 | **ĐÚNG** | `profile_mgmt.py:2191`: lọc `target` không kiểm tập rỗng ⇒ `findings=[]` ⇒ `final_ok=True` ⇒ `rc=0` |
| PRO-08 | P3 | **ĐÚNG** | `command_registry.py:709` help: *"cho phép merge nếu profile đích đã tồn tại"*; `profile_mgmt.py:391-405`: **`a.force` không hề được đọc**, luôn `PROFILE_TARGET_EXISTS` rc=2, note nói thẳng *"không merge hai profile bằng --force"* — help mâu thuẫn với chính note |

### 4.4 Rà soát

| ID | Mức | Verdict | Bằng chứng ở HEAD |
|---|---:|---|---|
| RAS-01 | P1 | **ĐÚNG cả 3 vế** | (a) `cli.py:509-511`: `add_parser("rasoat")` + `argparse.REMAINDER` + `subprocess.call` thẳng, **không có row metadata** ⇒ không dry-run gate, không risk, không idempotency contract. (b) `backfill_nlm_title.py:143`: `gas.post("reg_bulk")` là **mặc định**, chỉ `--dry` mới thoát ⇒ **đảo ngược nguyên tắc dry-mặc-định**; `backfill_keywords_live.py` **không có `--dry`** gì cả. (c) `registry_orchestrator.py:196`: `gas.post("changes_pull")` (applySheet=true ⇒ GHI Sheet) chạy ở `phase=boot` **TRƯỚC** cổng `if args.dry or not args.apply` ở `:218` ⇒ gọi "dry" vẫn ghi |
| RAS-02 | P1 | **ĐÚNG** | `lookup_ops.py:3149`: **toàn bộ** khối CAS nằm trong `if expect:`. Không truyền `--expect-claim` ⇒ bỏ qua sạch, ghi đè state đang tồn tại |
| RAS-03 | P1 | **ĐÚNG** | `state-get:3058-3071` sắp theo `modifiedTime` giảm dần rồi lấy `stamped[0]`; `state-put:3153` đọc `olds[0]` — **thứ tự list thô**. Hai bên chọn hai bản khác nhau khi trùng tên |
| RAS-04 | P1 | **ĐÚNG** | `lookup_ops.py:1750-1753`: `except Exception: added = 0`, ngay dưới `dry_rounds = 0 if added else dry_rounds + 1` ⇒ **lỗi đọc = "không có gì mới"**. `out["ok"]` luôn `True` |
| RAS-05 | P1 | **ĐÚNG — nặng** | `backfill_keywords_live.py:76`: `if not r.get('ok'): done[gid]='err'` mà `done` chính là bộ lọc worklist (`:63`) ⇒ **doc lỗi bị loại VĨNH VIỄN**. `:92,:100`: `reg_bulk` **không kiểm `rb.get('ok')`**, chỉ cộng `patched`; item đã đánh `done='ok'` từ TRƯỚC. `:107` `remaining==0` ⇒ in **"XONG TẤT CẢ."**, `main()` return None ⇒ `rc=0` |
| RAS-06 | P1 | **ĐÚNG** | `rasoat_phuluc.py:load_master` **có** dùng chung `_rasoat_merge_units` nhưng **không** gọi `_rasoat_trung_lap` (cổng trùng fail-closed chỉ có ở `lookup_ops.py:3236`). `dedup():97` gặp key trùng thì `continue` — **giữ bản đầu, mất payload sau**, chỉ để lại một dòng `ghi_chu` |
| RAS-07 | P1 | **ĐÚNG** | `lookup_ops.py:3272`: `uids = [f.stem for f in files ...]` ⇒ **tên file** quyết định state, không phải `payload.unit_id` |
| RAS-08 | P2 | **ĐÚNG** | `_rasoat_meta_folder(a)` gọi ở `:3036` (get) và `:3128` (put), **TRƯỚC** `load_creds(..., profile)` ở `:3041`/`:3137`. Mà `_rasoat_meta_folder` đọc `os.environ["TL_META_FOLDER_ID"]` — biến do chính `load_creds` đặt. Cộng thêm `tl.py:1298-1299` xếp `state-get`/`state-put` vào tập **bỏ qua `load_creds` ở `main()`** ⇒ không có đường nào nạp env kịp |
| RAS-09 | P2 | **ĐÚNG** | `lookup_ops.py:3121-3126`: chỉ `json.loads` rồi `json.dumps` đẩy lên — không kiểm schema/root-object/claim/q_units/enum |
| RAS-10 | P2 | **ĐÚNG** | Frontier rỗng từ đầu ⇒ `while` không chạy ⇒ `it=0, dry_rounds=0` ⇒ `converged = (not frontier) and 0 >= K` = **False**, `stop_reason="frontier_empty"`, mà `ok=True` |
| RAS-11 | P2 | **ĐÚNG** | `lookup_ops.py:3264`: `write_text(...)` chạy rồi `:3286` mới `return 0 if not bo_qua else 2` ⇒ **ghi trước, báo lỗi sau** |
| RAS-12 | P2 | **ĐÚNG** | `lookup_ops.py:3276-3279`: `except` chỉ nhét `hoa_giai={"loi": ...}`; `out ok = not bo_qua` ⇒ input sạch + state hỏng ⇒ `ok:true`, `rc=0`, lỗi chôn ở field phụ |
| RAS-13 | P2 | **ĐÚNG** | `lookup_ops.py:1935-1944` `_in_corpus` và `:2670` `cands`: khớp **thuần theo số hiệu**, không lọc `corpus`, không loại quarantine. (Quarantine CHỈ được loại ở `:2686` để tính `ambiguous`, không dùng cho `in_corpus`) |
| RAS-14 | P2 | **ĐÚNG** | ĐO: `tl rasoat phuluc --profile TEST --json` ⇒ `--profile`/`--json` chuyển **nguyên xi** cho `rasoat_phuluc.py`, script con báo usage error. `REMAINDER` không phân biệt cờ global với cờ con |
| RAS-15 | P2 | **ĐÚNG** | `rasoat_phuluc.py:74` `sorted(path.glob("*.json"))` — **không** lọc `_rasoat_la_ban_sao`; bộ lọc đó chỉ có ở `lookup_ops.py:3217` |
| RAS-16 | P3 | **ĐÚNG** | `rasoat_phuluc.py:118,137`: `dict.get(k, default)` **chỉ thay khi thiếu khoá**; `linh_vuc=""` ⇒ heading `LĨNH VỰC ` rỗng |

---

## 5. Hai mẫu lỗi chi phối — chốt lại để vá theo mẫu, không vá theo `if`

Audit gọi tên đúng. Bổ sung **đo đếm** để chọn cách vá:

**Mẫu A — kết luận giao dịch bằng HÌNH DẠNG thay vì bằng KẾT QUẢ** (13/34 mục):
GATE-01, ING-03, ING-05, PRO-01, PRO-06, PRO-07, RAS-04, RAS-05, RAS-10, RAS-11, RAS-12 + `ok:True`
gán cứng ở PRO-01/PRO-06.
Dấu hiệu chung: `ok` được **gán**, không được **tính**; hoặc được tính từ "có trường X" thay vì "bước X
báo thành công". ⇒ Vá bằng **một helper kết luận giao dịch dùng chung**, không sửa từng `if` (nếu sửa lẻ,
mục thứ 14 sẽ tái sinh ở chỗ khác).

**Mẫu B — định danh không khoá vào quyền ghi** (8/34 mục):
ING-01, ING-02, ING-04, ING-07, PRO-02, PRO-03, PRO-04, RAS-03/RAS-07.
Dấu hiệu chung: có **hai** cách gọi tên cùng một thứ (bảng cứng vs card; tên file vs `unit_id`;
`Alpha` vs `alpha`; hash sinh lúc apply vs hash người duyệt), và **không bên nào là nguồn sự thật**.
⇒ Vá bằng **chọn một nguồn, sinh bên còn lại từ nó**, kèm gate bắt drift.

---

## 6. Kế hoạch vá hợp nhất

Giữ kiến trúc pha của `ke_hoach_va.md`. Thay đổi so với bản gốc được đánh **[MỚI]** / **[SỬA]** / **[BỎ]**.

### Nguyên tắc tích hợp (giữ nguyên, bổ sung 3 điều)

1-6. Như bản gốc (worker chỉ đọc/đề xuất; canonical integrator là đầu mối ghi duy nhất; một owner mỗi
hotspot; không format hàng loạt; VERSION/CHANGELOG do integrator).

7. **[MỚI] Mọi slice chạm mã đa nền phải chạy THẬT trên CẢ Windows lẫn Linux rồi đối chiếu parity**
   — GATE-03 là bằng chứng tươi: r284 chỉ kiểm trên Windows và đẩy một ca đỏ sang Linux. Áp cho
   PRO-04 (cache key), GATE-03, ING-08.
8. **[MỚI] Không cưỡng chế một gate trước khi làm cho nó tất định** — xem §3.1; sai thứ tự thì được
   một gate đỏ chập chờn, tệ hơn gate hiện tại.
9. **[MỚI] Ruff phải có trong môi trường gate trước khi tuyên bố "delta F = 0"** — container này
   không có ruff, nên tiêu chí đó **chưa đo được**; đo trên máy chuẩn hoặc cài vào gate.

### Sơ đồ phụ thuộc (đã cập nhật)

```text
Pha 0 — làm gate đáng tin
  ├─ [MỚI] G0.0  GATE-03  selftest xanh lại trên Linux   ← CHẶN MỌI THỨ, làm TRƯỚC
  ├─ [SỬA] G0.1a GATE-01  đóng băng clock `sweep`  (tất định TRƯỚC)
  ├─ [SỬA] G0.1b GATE-01  cưỡng chế raw_stable     (cưỡng chế SAU)
  └─ [BỎ]  G0.2  GATE-02  — r284 đã đóng
        │
        ├─ Pha 1A — canonical ingest plan ── ING-02 ──┬─ ING-01
        │                                             └─ ING-07
        ├─ Pha 1B — fail-closed write ───── ING-03 ──── ING-04 ── ING-05
        ├─ Pha 1C — marker/profile safety ─ PRO-02 ──── PRO-03 ── PRO-01
        └─ Pha 1D — rasoat writer/state ─── RAS-01 ──── RAS-08/09 ── RAS-02/03

Pha 2 — correctness pipeline   (ingest: ING-06/08 · profile: PRO-04..08 · rasoat: RAS-04..16)
Pha 3 — characterization các RISK destructive
Pha 4 — full regression, smoke LIVE có phê duyệt, release
```

### Thứ tự làm theo RỦI RO THỰC (khác thứ tự pha — dùng khi phải cắt phạm vi)

Nếu chỉ làm được một phần, làm theo thứ tự này:

| # | Mục | Vì sao đứng đây |
|---:|---|---|
| 1 | **GATE-03** | Đang chặn deploy Linux/Cowork **ngay bây giờ**. Vá 1 dòng |
| 2 | **PRO-01** | Fail-open **phá huỷ**: tháo con trỏ registry sau khi bước xoá đã hỏng ⇒ tài sản mồ côi. `ok:True` gán cứng |
| 3 | **RAS-05** | **Mất dữ liệu im lặng**: doc lỗi rơi khỏi worklist vĩnh viễn, rồi in "XONG TẤT CẢ" |
| 4 | **RAS-01** | Ba writer công khai **không có gate nào**, dry-run bị đảo ngược, "dry" vẫn ghi Sheet |
| 5 | **ING-03** | Commit một phần được nhận là thành công ⇒ registry lệch Drive |
| 6 | **ING-01/02** | Quyền apply không khoá vào thứ người dùng đã duyệt |
| 7 | **PRO-02/03** | Marker — nguồn sự thật profile — tự chữa lành khi bị sửa trái phép |
| 8 | **RAS-02/03** | Single-writer trên giấy; hai bên chọn hai bản khác nhau |
| 9 | **GATE-01** | Lỗ tiềm ẩn (hiện 20/20 ổn định) — quan trọng nhưng chưa chảy máu |
| 10 | Còn lại | Theo Pha 2 |

---

### Pha 0

#### [MỚI] Slice G0.0 — GATE-03 (chặn; làm trước tiên)

- `tl_selftest.py:11182`: đổi lọc tiền tố `/tmp/` thành **so bằng đúng hằng** `/tmp/tra_luat_config.json`.
- Thêm khẳng định: hằng đó **phải** còn xuất hiện trong `_config_candidates(None)` — đổi hằng mà quên
  test thì đỏ tại đây, không lọc hụt im lặng.
- **Chạy THẬT trên Linux và Windows, đối chiếu số ca bằng nhau** (nguyên tắc 7). Đây chính là bước
  r284 thiếu.
- Acceptance: selftest **1491/1491 trên CẢ hai nền**, hai lượt liên tiếp cùng verdict.

#### [SỬA] Slice G0.1a — làm `sweep` tất định (TRƯỚC khi cưỡng chế)

- Deterministic mode phải scrub/đóng băng `snapshot_age_s` **ở raw output**, hoặc thay input bằng
  fixture có clock cố định. **Không nới định nghĩa raw-stability.**
- Acceptance: `golden-test` chạy **≥5 lượt** liên tiếp, `sweep` `raw_stable=true` mọi lượt.
  (Chạy 1 lượt là không đủ — lỗi này bất định theo thời điểm, xem §3.1.)

#### [SỬA] Slice G0.1b — cưỡng chế raw stability (SAU khi G0.1a xanh)

- `raw_stable=false` ⇒ `case ok=false` ⇒ `top ok=false` ⇒ `rc≠0` + error code riêng
  (`GOLDEN_RAW_UNSTABLE`).
- `--write`: **cấm ghi/regen fixture** khi raw bất định.
- Characterization test giả lập hai stdout khác byte / cùng projection — **phải đỏ**
  (harness đã dựng sẵn ở §4.1, tái dùng).
- Acceptance: 20/20 case `ok=true, raw_stable=true, projection_stable=true`; harness bơm drift ⇒ đỏ.

#### Acceptance Pha 0

- `tl --selftest` → N/N **hai lượt, hai nền**.
- `workflow-audit --strict` → `ok:true`.
- `golden-test` → mọi case `raw_stable=true`, ≥5 lượt.
- `determinism-audit --strict` → `ok:true`. (Audit ghi nhận một lượt đỏ do `gws --version` timeout 10s,
  8 lần gọi sau đều xanh 0,17–0,37s. **Tách probe version ra cache riêng, KHÔNG nuốt lỗi thật** — nếu
  gộp chung thì lỗi gws thật cũng bị nuốt theo.)
- **[MỚI]** ruff có mặt trong môi trường gate; đo lại nền `tl.py` = 12 F821 / 0 F401 (CLAUDE.md
  §Quy trình sửa code) rồi mới nói delta.

---

### Pha 1A — Canonical ingest plan và quyền apply

**Slice I1 — ING-02.** Một builder schema duy nhất bao phủ: hash bytes nguồn · target scope/profile/
canonical name · **mọi** cờ đổi hành vi · hash sidecar text/OCR manifest/quality evidence.
**[SỬA] Danh sách cờ đã chốt bằng `--help` thật (§3.3)** — `replace_sohieu`, `no_fallback` (ingest-local);
`allow_dup_name`, `no_nlm_add`, `no_fallback` (profile-ingest). Test tham số hoá: **đảo từng cờ** hoặc
**đổi một byte artifact** ⇒ `plan_hash` phải đổi.

**Slice I2 — ING-01.** OCR dry-run xuất **immutable plan bundle** gồm child plan hash. Apply **chỉ**
nhận hash caller đã xác nhận; **cấm** chạy child dry rồi tự phê duyệt hash mới. Test TOCTOU: đổi
sidecar/source/options giữa dry và apply ⇒ **zero mutation**.

**Slice I3 — ING-07.** **[SỬA] Hướng đã xác định: card ĐÚNG, bảng cứng SAI.** Xoá
`_IDEMPOTENCY_CONTRACTS["ingest_zip"]` hard-code, sinh từ card (hoặc ngược lại — nhưng nội dung phải
lấy theo card `content-v3/SHA256` vì đó là thứ mã thật tính). `workflow-audit --strict` phải **fail**
khi route output lệch card — hiện tại nó xanh trong khi drift đã có thật.

### Pha 1B — Fail-closed write, journal, resume

**Slice I4 — ING-03.** Validator `ingest_commit` đòi `ok=true` **và** đủ marker
(`organize_done`, `rename_done`, `upsert_done`, readback row/file) trước khi chuyển stage.
**[MỚI]** Sửa cả **hai** call site (`:1836`, `:3079`) — cùng một lỗ, hai chỗ; sửa một chỗ là để lại lỗ.
Ma trận negative-input cho từng marker thiếu/sai.

**Slice I5 — ING-04.** Journal commit ghi: source hash · plan hash · identity · src/GDoc IDs · target scope.
Resume **so** committed identity với nguồn/registry hiện hành. **[MỚI]** Cụ thể hai lỗ đã đo:
(a) `drive_id` rỗng **không được** làm nhánh mismatch bị bỏ qua — rỗng = *không chứng minh được*,
fail-closed; (b) `plan_hash`/`identity_hash` phải được **so khớp**, không chỉ kiểm tồn tại.

**Slice I6 — ING-05.** Mọi terminal path ghi **đúng một** `run_end`. Mọi external write có
intent → result → readback → commit/failure. `--no-nlm-add` kết thúc rõ ràng là *thành công
Drive/registry, NLM deferred*, không để journal giả inflight.
**[MỚI]** Thêm test quét: liệt kê mọi `return {"stop": "DONE"}` trong `ingest_ops.py` và khẳng định
mỗi đường đều đi qua `run_end` — chống tái phát ở nhánh thứ N.

### Pha 1C — Marker và Profile safety

**Slice P1 — PRO-02/PRO-03.** `fingerprint` vào `_marker_required_keys` cho v2 (**bỏ điều kiện
"nếu có"** — đó chính là cửa hậu). Mọi mutation profile đi qua `_marker_mutation_guard`.
`profile-adopt` gặp marker invalid ⇒ **zero mutation**; repair chỉ qua lệnh migration/force đã duyệt.
**[MỚI]** Phản chứng bắt buộc: marker v2 **bị xoá trường `fingerprint`** phải `validate` ĐỎ
(hiện đang xanh) và phải chặn adopt.

**Slice P2 — PRO-01.** `profile-file-remove` kiểm **kết quả dương** từng bước, dừng trước mutation kế tiếp.
Registry chỉ được tháo khi các thao tác **được yêu cầu trước đó** đã thành công + readback.
**[MỚI]** Bỏ `ok: True` gán cứng — `ok` phải **tính** từ kết quả. Xét lại `require_removed="no"`
(đang tự tắt readback của chính bước xoá registry). Test ma trận `--delete-nlm` × `--trash-drive` ×
`--keep-registry`, mỗi ô có ca **bước con hỏng** ⇒ đòi `rc≠0` **và** registry còn nguyên.

**Slice P3 — PRO-04.** Canonical profile key dùng chung cho lookup · sync · create/adopt · cache.
Chặn collision **trước** khi ghi. Dual-read/migrate cache cũ; **không** rename/delete cache hàng loạt mù.
**[MỚI]** Test parity hai nền (§3.2) — test chỉ chạy Linux sẽ **xanh giả**.

**Slice P4 — PRO-05/06/07/08.** Doctor kiểm MIME **manifest** (bỏ điều kiện khoá cứng `role=="registry"`).
Missing profile/target ⇒ lỗi có cấu trúc, `rc≠0` (PRO-06, PRO-07). Bỏ `--force` giả **và** help tương
ứng — **không** triển khai merge profile trong slice này (PRO-08).

### Pha 1D — Rà soát: khoá writer và state

**Slice R1 — RAS-01/RAS-14.** Tách nested writer thành command metadata thật
(`rasoat-keywords`, `rasoat-titles`, `rasoat-orchestrate`). **Dry-run mặc định**; apply/confirm/readback
bắt buộc. Áp profile offline **trước** dispatch; bỏ `argparse.REMAINDER` cho đường có cờ global.
Inventory/strict audit phải nhìn thấy **mọi** public writer.
**[MỚI]** Đóng riêng lỗ `changes_pull`: **không** gọi action ghi nào trước cổng `--apply`
(`registry_orchestrator.py:196` chạy trước cổng ở `:218`) — đây là "dry mà vẫn ghi", nặng hơn phần
metadata và có thể vá độc lập, sớm.

**Slice R2 — RAS-08/RAS-09.** Áp profile **trước** resolve meta folder — **[MỚI]** nhớ cả
`tl.py:1298-1299` (tập bỏ qua `load_creds` ở `main()`), nếu chỉ đảo thứ tự trong handler mà quên chỗ này
thì `--profile` vẫn không tới nơi. Validator máy cho `rasoat_plan.v1`: root **object** · schema · claim ·
q_units · enum · trường bắt buộc. Xác minh folder đích **thật sự** là `_meta` của profile.

**Slice R3 — RAS-02/RAS-03.** Một helper `authoritative-newest` **dùng chung** cho state-get và state-put
(hiện mỗi bên một cách chọn). State **đã tồn tại** ⇒ bắt buộc `expect_claim`; chỉ create-first được thiếu.
Sau khi vá client, triển khai CAS nguyên tử qua GAS `LockService`/revision precondition (ADR-0016) —
**không tuyên bố single-writer hoàn tất** nếu mới chỉ read-then-write phía client.

### Pha 2 — Correctness pipeline

**Ingest.** ING-06: planner và child dùng **chung** capability/extension registry — mọi member accepted
phải tạo được child plan (quyết định rõ: hoặc bỏ `.txt/.md` khỏi `_ALLOWED_INGEST_EXTS`, hoặc cho child
nhận chúng qua `--text-file`; **không để hai bảng**). ING-08: chốt support boundary — nếu direct script
còn được hỗ trợ thì chuẩn hoá UTF-8 **và chỉ publish cache sau khi output thành công**; nếu không thì
deprecate rõ, bắt buộc `tl cache-build`.

**Rà soát loop.** RAS-04: thêm trạng thái `unreadable`; lỗi đọc **không** được tính dry round; output
`converged=false` + hướng retry/pause actionable. RAS-10: định nghĩa frontier-rỗng là empty-pass/hội tụ
tương đương **rõ ràng**; khoá `max_iter, dry_rounds > 0`.

**Keywords.** RAS-05: checkpoint state `pending/inflight/committed/retryable/blocked`. Chỉ commit
progress sau `reg_bulk ok` **và** patched/readback dương; lỗi **ở lại** remaining, `rc≠0`.
**[MỚI]** Bỏ hẳn lối `done[gid]='err'` — lỗi đi vào `retryable`, không vào `done`; và đổi
"XONG TẤT CẢ" thành kết luận **tính từ** remaining thật.

**Merge/phụ lục.** RAS-06/15: direct và wrapper dùng chung collector + backup filter + duplicate validator
(`_rasoat_merge_units` đã chung — **thêm `_rasoat_la_ban_sao` và `_rasoat_trung_lap` vào cùng bộ**).
RAS-07: filename phải **khớp** `payload.unit_id`. RAS-11/12: validate **toàn bộ** input và state
**trước** write; staging + atomic replace; lỗi reconcile state làm **cả giao dịch** fail.
RAS-16: normalize chuỗi rỗng → "Chưa phân loại" (dùng `or`, không dùng `dict.get` default).

**Chồng chéo.** RAS-13: shared effective-corpus predicate; test quarantine-only · `corpus=false` · ref ·
bare-VBHN.

### Pha 3 — Characterization các RISK (chỉ nâng thành bug khi harness đỏ)

Giữ nguyên 7 mục bản gốc: NLM source ID journal chết/sai · profile delete/remove trên manifest stale ·
config-marker drift trước profile-ingest · orphan window create/adopt/promote · state CAS TOCTOU ·
state newest khi mọi `modifiedTime` lỗi · kill giữa lúc ghi output local.
**Dùng fake adapter/recorded response — không thử bằng destructive LIVE.**

---

## 7. Ranh giới commit logic (đã cập nhật)

| # | Commit | Đổi so bản gốc |
|---:|---|---|
| 0 | `test: fix cross-platform config isolation guard` | **[MỚI]** GATE-03 — làm trước tiên |
| 1a | `gate: make sweep raw output deterministic` | **[SỬA]** tách khỏi #1b |
| 1b | `gate: enforce raw stability` | **[SỬA]** phụ thuộc 1a |
| — | ~~`test: make selftest config-hermetic`~~ | **[BỎ]** r284 đã làm |
| 2 | `ingest: bind complete plan identity` | |
| 3 | `ocr: require caller-confirmed child plan` | |
| 4 | `ingest: fail closed on partial ingest_commit` | |
| 5 | `ingest: bind journal resume identity and terminal state` | |
| 6 | `profile: enforce marker v2 and mutation guard` | |
| 7 | `profile: make file removal transactional` | |
| 8 | `profile: prevent profile/cache identity collisions` | |
| 9 | `profile: tighten doctor/read command contracts` | |
| 10 | `rasoat: gate orchestrator writes behind --apply` | **[MỚI]** tách khỏi #11, vá được sớm |
| 11 | `rasoat: register writers and default to dry-run` | |
| 12 | `rasoat: validate/profile-bind state` | |
| 13 | `rasoat: make state CAS authoritative and atomic` | |
| 14 | `rasoat: distinguish unreadable from convergence` | |
| 15 | `rasoat: make keyword checkpoint verified` | |
| 16 | `rasoat: validate merge before atomic output` | |
| 17 | `rasoat: unify appendix collector and effective-corpus checks` | |
| 18 | `ingest: align ZIP capability and cache support boundary` | |

VERSION/CHANGELOG do canonical integrator cập nhật theo tranche đã duyệt — worker không chạm hai file này.

---

## 8. Phân công worker (đã cập nhật)

| Worker | Mục | Hotspot | Điều kiện |
|---|---|---|---|
| **W-GATE** | **GATE-03** → GATE-01 → ING-07 | `tl_selftest.py`, `workflow.py` | **GATE-03 đi trước mọi worker khác**; phải chạy thật hai nền |
| W-INGEST-PLAN | ING-01/02 | `ocr.py`, vùng plan `ingest_ops.py` | Chờ Pha 0 |
| W-INGEST-TXN | ING-03/04/05 | vùng write/resume `ingest_ops.py` | Không song song W-INGEST-PLAN trên canonical |
| W-PROFILE | PRO-01..08 | `profile_mgmt.py`, `profile_env.py`, `ops_misc.py` | PRO-01 ưu tiên cao nhất nhóm; PRO-04 cần parity hai nền |
| W-RAS-STATE | RAS-02/03/08/09 | vùng state `lookup_ops.py`, GAS contract | Chờ RAS-01 metadata |
| W-RAS-LOOP | RAS-04/10/13 | vùng loop/chồng chéo `lookup_ops.py` | Không cùng lúc W-RAS-STATE trên canonical |
| W-RAS-MERGE | RAS-06/07/11/12/15/16 | `rasoat_phuluc.py`, vùng merge `lookup_ops.py` | Collector contract chốt trước |
| **W-RAS-WRITE** | **RAS-01 (vế changes_pull) + RAS-05** | `registry_orchestrator.py`, `backfill_keywords_live.py`, `backfill_nlm_title.py` | **[MỚI]** — hai script rời, không tranh `lookup_ops.py`, chạy song song được ngay |

Worker giao: repro đã chạy · test đỏ đề xuất · patch/diff đề xuất · danh sách file/hunk + giả định.
Canonical integrator tái hiện trên HEAD mới rồi mới áp dụng.

---

## 9. Full acceptance trước release

### Offline

- Selftest N/N **hai lượt × hai nền** (Windows + Linux), có mặt config local ignored.
- Workflow audit strict xanh — **và** phải ĐỎ khi bơm drift route↔card (test mới của I3).
- Golden: mọi case `raw_stable=true`, **≥5 lượt** (không phải 1).
- Determinism audit strict xanh.
- Gen-instructions selftest N/N.
- Doc-claims strict `flags=[]`.
- **Ruff cài trong môi trường gate**; delta F so nền repo = 0 (nền: `tl.py` 12 F821 / 0 F401).
- **34 regression test đỏ-trước/xanh-sau** — mỗi mục một `rXX_`.
- `git diff` chỉ chứa file thuộc tranche; không stage artifact/cache/report.
- **[MỚI]** Nếu tranche thêm/xoá tệp: tái sinh `RELEASE_MANIFEST.json` + ghi lại golden nếu số đếm
  kiểm kê đổi (CLAUDE.md §Quy ước deploy mục 5); kiểm `git diff -- references/golden/` TRƯỚC commit.
- **[MỚI]** Canh **trần 200 tệp** — tệp dev-side mới cho vào `_RELEASE_EXCLUDE_NAMES_ANYWHERE`,
  giữ trong git, loại khỏi gói.

### LIVE — chỉ sau phê duyệt riêng

Profile/fixture disposable · chụp live-state trước · một apply có plan hash đã duyệt cho từng đường
ingest/profile/state · readback Drive/registry/NLM/marker/state · chụp sau + diff chỉ path dự kiến ·
undo/cleanup kiểm chứng · **không dùng corpus nghiệp vụ thật làm fixture**.

### Release

`release-check --strict-determinism --full` · bundle hai lần cùng SHA-256 · verify manifest/bundle ·
`core.abbrev=7` khi chạy gate · **chốt chống thụt lùi Package** (đọc VERSION trên Drive; Drive ≥ bản sắp
đẩy ⇒ DỪNG, hỏi user) · sau push tải lại đối chiếu byte/VERSION.

---

## 10. Ghi chú trạng thái cây

Lượt xác minh này **không sửa một dòng mã sản xuất nào**. Lệnh chạy đều là read-only/dry-run
(`--selftest`, `golden-test --json`, `workflow-audit --strict --json`, `doc-claims-check --strict --json`,
`gen_instructions.py --selftest`, `--help`). Harness GATE-01 chạy trong `tempfile.mkdtemp()` với
`_GOLDEN_CASES` bị monkey-patch **trong tiến trình con**, không chạm `references/golden/`.
Không `--apply`, không ghi Drive/registry/NLM.
