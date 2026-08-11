# Bàn giao — T2 "chặn máu" còn lại: RAS-05 + ING-03 (31-07-2026)

**Dev-side, ngoài gói** (`rasoat/` nằm trong `_RELEASE_EXCLUDE_DIRS`). Dán nguyên phần
"PROMPT PHIÊN SAU" ở cuối vào phiên mới.

---

## 1. Trạng thái cây

Nhánh: **`claude/va-t1-gate-nlvoj9`** (đã đẩy, `origin/master` không đi trước — `0 6`).
VERSION hiện tại **v1.36.28**. Selftest **1509/1509**. Full gate **8/8 PASS**.
Kiểm kê tệp: **196/200** — *còn đúng 4 khe*.

| # | Commit | Mục | Trạng thái |
|---|---|---|---|
| 1 | `6001078` r285 v1.36.23 | GATE-03 | ✅ T1 |
| 2 | `c8d15fe` r286 v1.36.24 | GATE-01a | ✅ T1 |
| 3 | `37a50dc` r287 v1.36.25 | GATE-01b | ✅ T1 |
| 4 | `4c27a43` r288 v1.36.26 | Pha 1-0 Helper 1 | ✅ T2 |
| 5 | `caf1ecc` r289 v1.36.27 | **PRO-01** | ✅ T2 |
| 6 | `c8cdd02` r290 v1.36.28 | **RAS-01**(changes_pull) | ✅ T2 |
| — | — | **RAS-05** | ⬜ CÒN LẠI |
| — | — | **ING-03** | ⬜ CÒN LẠI |

Kế hoạch gốc: `git show origin/claude/audit-errors-patch-plan-56x4rq:docs/AUDIT_XAC_MINH_VA_KE_HOACH_VA_2026-07-31.md`
(phần liên quan: §4.2 ING-03, §4.4 RAS-05, §5 Mẫu A, Slice I4, Slice R0, §6.3 tranche T2).

---

## 2. Helper 1 — ĐÃ CÓ, hai mục còn lại PHẢI DÙNG

`scripts/tl_core/txn.py` (r288). **DÙNG, không SỬA.**

```python
from tl_core.txn import Txn, TxnBlocked, step_result_ok   # trong tl_core: tra tên qua globals tl (đã re-export)

t = Txn("ten-lenh")
t.record("buoc", resp, required=True, require_keys=("upsert_done",), mutating=True, wrote={...})
t.skipped("buoc_khong_yeu_cau", "KHONG_YEU_CAU")
t.guard("buoc_ke_tiep")          # ném TxnBlocked nếu bước bắt buộc trước đó hỏng
out = t.conclude(**payload)      # `ok` TÍNH; `ok`/`rc` trong payload bị BỎ QUA
return t.rc()                    # rc dẫn xuất
```

`step_result_ok` **fail-closed**: `{"ok": false, "fileId": "1AbC"}` ⇒ ÂM; `{"fileId": "1AbC"}` (thiếu hẳn
khoá `ok`) ⇒ ÂM; str/int/list ⇒ ÂM. `require_keys` = "đủ marker", lý do hỏng nêu **đích danh** marker thiếu.

**BẮT BUỘC khi gắn helper vào module mới:** cập nhật allow-list trong `tl_selftest.py`:

```python
_HELPER1_DA_GAN = {"ops_misc.py"}          # ING-03 phải thêm "ingest_ops.py"
```

Ca `r288_helper1_chi_gan_o_noi_da_khai` sẽ ĐỎ nếu quên — cố ý, để việc gắn helper vào một đường GHI mới
không lọt review im lặng.

---

## 3. Việc còn lại

### 3.1 ING-03 — validator `ingest_commit`, **SỬA CẢ HAI call site**

`scripts/tl_core/ingest_ops.py`. `grep upsert_done` toàn kho ra **đúng 1 hit** (`:1502`) và hit đó chỉ dùng
để **đặt tên bước lỗi**, không gate gì.

Hai call site đều gate bằng `org.get("fileId")` — response `ok:false` + `upsert_done:false` mà có `fileId`
vẫn **đi tiếp**:

- `_pi_stage_write` (~`:1836`, profile-ingest): `org = _ingest_commit_call(g, okw)` → `gdoc = org.get("fileId")`
  → `if not gdoc: … return {"rc": 2}`.
- `_il_stage_write` (~`:3079`, ingest-local): y hệt, thêm `_step_ok("organize", fid, bool(gdoc), …)`.

**Vá:** dùng `step_result_ok(org, require_keys=("organize_done", "rename_done", "upsert_done", "file"))`
(hoặc `Txn`) — đòi `ok=true` **và** đủ marker + readback row/file **trước khi chuyển stage**.
**Sửa MỘT chỗ là để lại lỗ y hệt ở chỗ kia.**

Ma trận negative-input: từng marker thiếu/sai, `ok:false` + `fileId` có, `ok` vắng mặt.
**Phản chứng bắt buộc:** response ĐỦ marker ⇒ vẫn đi tiếp bình thường (không chặn oan đường hợp lệ).

Bẫy: xem §4 dưới — `_pi_stage_write`/`_il_stage_write` nằm trong `_STUB_MAP["ingest_ops"]`, và
monkeypatch phải đi qua `_resolve286`.

### 3.2 RAS-05 — `scripts/backfill_keywords_live.py`

Đã đọc mã, ba lỗ nằm ở `main()` (dòng ~63–110):

1. `:63` `wl = [w for w in worklist(...) if w['drive_id'] not in done]` — `done` là **bộ lọc worklist**.
   `:76`/`:84`/`:87` gán `done[gid] = 'err'` / `'err:'+…` / `'empty'` ⇒ **doc lỗi bị loại VĨNH VIỄN**,
   không bao giờ thử lại.
2. `:92` và `:100` gọi `gas.post('reg_bulk', …)` rồi chỉ cộng `rb.get('patched')` — **không kiểm
   `rb.get('ok')`**. Item đã bị đánh `done[gid]='ok'` từ TRƯỚC lúc gọi ⇒ `reg_bulk` hỏng vẫn coi là xong.
3. `:107` `remaining` tính lại từ `done` (đã nhiễm) ⇒ `remaining==0` in **"XONG TẤT CẢ."**,
   `main()` return `None` ⇒ **rc=0**.

**Vá theo kế hoạch:** checkpoint state `pending/inflight/committed/retryable/blocked`; lỗi vào
**`retryable`, KHÔNG vào `done`**; chỉ commit tiến độ **sau** `reg_bulk` `ok` + readback dương;
kết luận tính từ **remaining thật**; `rc≠0` khi còn lỗi.

Lưu ý tương thích: file progress cũ (`prog['done']` dạng `{gid: 'ok'|'err'|'empty'}`) đang tồn tại trên
máy người giữ — **phải đọc được bản cũ** và coi mọi giá trị `err*` là `retryable` (đó cũng chính là đường
Pha 3.5 kê thiệt hại). Đừng vứt file cũ.

Script này **không có `--dry`** (RAS-01 vế (b) — thuộc T3, đừng gộp vào đây).

---

## 4. Nếp bắt buộc — đã trả giá trong 6 commit vừa rồi

1. **Mỗi fix một test `rXX_` ĐỎ-TRƯỚC / XANH-SAU.** Cách chứng minh đã dùng: hoàn nguyên **đúng** phần mã
   sản xuất (giữ nguyên test) → chạy selftest → phải ĐỎ đúng những ca của mục đó → khôi phục.
   Không có bước này thì chưa chứng minh được là fix.
2. **Bằng chứng DƯƠNG**: `N/N` hai số bằng nhau, `"ok": true`. **KHÔNG tin `rc=0`.**
3. **Full gate 8 bước TRƯỚC mỗi lần bump VERSION** (dùng skill `/gate`, nhớ `git config core.abbrev 7`).
   Bump 3 chỗ: `VERSION`, hằng `VERSION` trong `tl.py`, header `SKILL.md`. + mục ★ CHANGELOG.
   Thêm/xoá tệp ⇒ tái sinh `RELEASE_MANIFEST.json`.
4. **`SKILL.md` và `scripts/tl.py` là tệp CRLF.** Sửa version bằng `Path.write_text()` (text mode) sẽ
   **âm thầm đổi trọn CRLF→LF** — `git diff` 3492 dòng ở `tl.py` — và làm ĐỎ **bốn** gate cùng lúc
   (`selftest r219`, `golden` case `workflow_audit` lệch `size_bytes`, `determinism`, `release-verify`),
   **không lỗi nào chỉ thẳng vào nguyên nhân**. Dùng `read_bytes`/`write_bytes` hoặc công cụ Edit.
5. **Bẫy I11 — symbol MỚI trong `tl_core` PHẢI vào `_STUB_MAP`** (`scripts/tl.py`). Quên ⇒ `NameError`
   lúc chạy + ca `r90_rebase_module_names_resolvable` ĐỎ. (Đã va ở r289 với `_pfr_*`.)
   Lớp/ngoại lệ thì re-export **TRỰC TIẾP**, không qua stub (stub là function ⇒ `except`/`isinstance` sai).
6. **Monkeypatch trong selftest phải đi qua `_resolve286`** (đã có sẵn trong `tl_selftest.py`):

   ```python
   _real = _resolve286(_TL_MODULE.cmd_xxx)   # gỡ stub _STUB_MAP
   _g = _real.__globals__                    # patch trên globals của CHÍNH hàm sẽ chạy
   ```

   Lý do: `_TL_MODULE.cmd_xxx` là **STUB** ủy quyền `getattr(tl_core.<mod>, name)`. Ở tiến trình sạch,
   hàm thật được re-home `__globals__` về `tl.__dict__` nên patch `_TL_MODULE.<ten>` ăn (vì thế các ca cũ
   ở ĐẦU tệp chạy được). Nhưng tới **cuối** dãy selftest, module đã bị nạp lại ⇒
   `hygiene.cmd_sweep.__globals__ is tl.__dict__` là **False** ⇒ patch **không tới nơi**, lệnh rơi xuống
   gọi webapp THẬT rồi chết vì seal-mạng (`rc=2`, **stdout RỖNG** — triệu chứng kinh điển, mất khá lâu
   mới lần ra).
7. **Fake trong test phải khớp HỢP ĐỒNG THẬT.** Fake `_G282.post` từng trả `{"ok": True}` trần, thiếu
   `removed`/`not_found`/`skipped_live` mà `API_CONTRACT` khai là **luôn có** ⇒ bắt bản vá phải tin một
   `ok` trần, đúng cái bệnh đang chữa. Kiểm `references/API_CONTRACT.md` trước khi dựng fake.
8. **Đọc mã GAS khi nghi ngờ** — `references/Code.2.21.2n.gs`. r290 nặng hơn audit mô tả chỉ vì đọc
   `doChangesPull_`: nó **luôn** ghi `TL_CHANGES_TOKEN` bất kể `apply`, nên `applySheet=false` không cứu được.
9. **ruff**: tiêu chí là **DELTA so master = 0 theo LỚP cảnh báo**, không phải 0 tuyệt đối.
   `tl.py` nền = **12 F821 / 0 F401** (đã giữ đúng qua cả 6 commit). Tệp `tl_core` +1 F821 mỗi tên re-home
   mới là BÌNH THƯỜNG. **ĐỪNG "dọn import thừa" ở đầu `tl.py`** — gate đã đỏ 2 lượt vì việc đó.
   ruff **có** trong container này: `/root/.local/bin/ruff` (0.15.8), `python -m ruff` thì KHÔNG có.
10. **Golden**: `golden-test --write` là hành động ĐƯỢC HỎI (hook R6). Chỉ ghi lại khi đã **kiểm** diff và
    xác nhận là kiểm kê hợp lệ. Tiền lệ đã dùng ở r288: thêm `txn.py` ⇒ `files_scanned` 69→70, diff **đúng
    1 dòng**. Luôn `git diff -- references/golden/` TRƯỚC khi commit.
11. **Gate đỏ ⇒ đo lại trên `origin/master` sạch, so DELTA** trước khi nghi bản vá của mình
    (`git worktree add <tmp> origin/master`).
12. **Nền còn lại chưa kiểm.** Mọi thứ tới giờ đo THẬT trên **Linux**. **Windows chưa chạy lượt nào** —
    cần người giữ chạy `python scripts\tl.py --selftest` đối chiếu số ca bằng nhau để đóng parity.

## 5. Điều cần người giữ quyết

- **Nhánh.** Kế hoạch đặt tên `claude/va-t2-chan-mau`, nhưng nhánh chỉ định của các phiên này là
  `claude/va-t1-gate-nlvoj9` nên T1 + T2 đang **chung một nhánh**. Muốn tách thì nói rõ.
- **Trần 200 tệp: còn 4 khe.** RAS-05/ING-03 nên vá tại chỗ, đừng thêm module mới nếu tránh được.
- **Chưa deploy, chưa ghi LIVE, chưa mở PR.**

---

## PROMPT PHIÊN SAU — dán nguyên khối

```
Repo tra-luat, nhánh claude/va-t1-gate-nlvoj9 (đã có 6 commit T1+T2, VERSION v1.36.28, selftest 1509/1509,
full gate 8/8 xanh). Đọc TRƯỚC khi làm:
  cat rasoat/BANGIAO_T2_con_lai_RAS05_ING03_2026-07-31.md
  cat CLAUDE.md
  git show origin/claude/audit-errors-patch-plan-56x4rq:docs/AUDIT_XAC_MINH_VA_KE_HOACH_VA_2026-07-31.md

Làm nốt hai mục cuối của tranche T2 "chặn máu", mỗi mục MỘT commit, đúng thứ tự này:

(1) ING-03 — Slice I4. scripts/tl_core/ingest_ops.py, HAI call site `_pi_stage_write` (~:1836) và
    `_il_stage_write` (~:3079) đều gate bằng `org.get("fileId")` ⇒ response ok:false + upsert_done:false
    mà có fileId vẫn ĐI TIẾP. Vá bằng Helper 1 (tl_core/txn.py, ĐÃ CÓ — DÙNG, KHÔNG SỬA): đòi ok=true VÀ
    đủ marker (organize_done, rename_done, upsert_done, readback row/file) trước khi chuyển stage.
    SỬA CẢ HAI — sửa một chỗ là để lại lỗ y hệt ở chỗ kia.
    Ma trận negative-input cho từng marker thiếu/sai + PHẢN CHỨNG "đủ marker vẫn đi tiếp bình thường".
    NHỚ thêm "ingest_ops.py" vào `_HELPER1_DA_GAN` trong tl_selftest.py, không thì ca
    r288_helper1_chi_gan_o_noi_da_khai ĐỎ (cố ý).

(2) RAS-05 — Slice R0. scripts/backfill_keywords_live.py. Ba lỗ (chi tiết dòng trong file bàn giao §3.2):
    `done` vừa là sổ-đã-xong vừa là BỘ LỌC worklist nên doc lỗi bị loại VĨNH VIỄN; reg_bulk không kiểm
    `ok` mà item đã đánh done='ok' từ TRƯỚC; remaining==0 ⇒ in "XONG TẤT CẢ." + rc=0.
    Vá: state pending/inflight/committed/retryable/blocked; lỗi vào retryable KHÔNG vào done; chỉ commit
    tiến độ sau reg_bulk ok + readback dương; kết luận tính từ remaining THẬT; rc≠0 khi còn lỗi.
    PHẢI đọc được file progress bản CŨ và coi mọi giá trị `err*` là retryable (đừng vứt file cũ).
    Script này không có --dry — đó là RAS-01 vế (b), thuộc T3, ĐỪNG gộp.

Quy trình bắt buộc (§4 file bàn giao — 12 nếp đã trả giá, đọc hết):
- Mỗi fix một test rXX_ ĐỎ-TRƯỚC/XANH-SAU: hoàn nguyên ĐÚNG phần mã sản xuất, giữ test, selftest phải ĐỎ
  đúng ca của mục đó, rồi khôi phục. Không có bước này thì chưa chứng minh được là fix.
- Bằng chứng DƯƠNG: N/N hai số BẰNG NHAU, "ok": true. KHÔNG tin rc=0.
- Full gate 8 bước (skill /gate, nhớ `git config core.abbrev 7`) TRƯỚC mỗi lần bump VERSION.
  Bump 3 chỗ + CHANGELOG mục ★ + tái sinh RELEASE_MANIFEST.json.
- SKILL.md và scripts/tl.py là CRLF — sửa version phải byte-level, KHÔNG dùng Path.write_text.
- Symbol MỚI trong tl_core PHẢI vào _STUB_MAP (bẫy I11). Monkeypatch trong selftest phải qua _resolve286.
- ruff: /root/.local/bin/ruff (python -m ruff KHÔNG có). Nền tl.py = 12 F821 / 0 F401. Delta theo LỚP.
  ĐỪNG dọn import ở đầu tl.py.
- Gate đỏ ⇒ đo lại trên origin/master sạch, so DELTA, trước khi nghi bản vá của mình.
- Trần 200 tệp, hiện 196 — tránh thêm module mới.

CẤM: --apply, source-delete, reg-delete, --clear-stale, ghi LIVE, deploy, đọc/ghi secrets, Drive/Sheets MCP,
subagent sửa tl.py canonical.
```
