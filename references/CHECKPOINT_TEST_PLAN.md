# KẾ HOẠCH TEST HỆ THỐNG CHECKPOINT — chạy LIVE trên Cowork/Chat (dữ liệu THẬT)

> **Mục đích:** kiểm chứng đầy đủ hệ thống checkpoint (precheck-gate + WAL journal + verified-write + resume/undo + loop)
> trên corpus THẬT, an toàn. **Nguyên tắc xuyên suốt:** DRY trước → --apply lô NHỎ → verify bằng số liệu thật → undo nếu cần.
> **Chạy trên Cowork/Chat** (có gws + nlm cred). Dev KHÔNG chạy được phần --apply (không cred).
>
> Mỗi lệnh mutate ghi registry giờ **tự sinh 1 `journal=<run_id>`** trong output → dùng nó cho `tl journal`/`tl resume`/`tl undo`.

---

## 0. Chuẩn bị (1 lần)

```bash
sh scripts/tl_fetch.sh --setup --nlm      # hoặc `tl up --nlm` — bootstrap gws+nlm+manifest
tl doctor --json                          # phải xanh; xem registryDocId
tl boot --refresh                         # nạp manifest MỚI
```
**Kỳ vọng:** `doctor` OK. Nếu `registryDocId` = Doc legacy `1mATG` → **DỪNG**, sửa config về Sheet `tra_luat_registry` thật
(hoặc để rỗng cho webapp auto-discover). Đây chính là cái `precheck` sẽ chặn ở Test 1.

---

## 1. PRECHECK — cổng bất biến (chống clobber/mispoint/ghi-mù) · READ-ONLY

```bash
tl precheck                               # kiểm bất biến môi trường ĐANG active
tl precheck --cols "so_hieu,corpus"       # cột SAI → phải báo blocker WRITE_COLS_IN_SCHEMA
tl precheck --cols "sohieu,corpus"        # cột ĐÚNG → không blocker cột
tl --profile <ProfileDựÁn> precheck       # nếu có profile dự án registryDocId rỗng → blocker PROFILE_REGISTRY_ID_NOT_EMPTY
```
**Kỳ vọng:**
- registryDocId hợp lệ + snapshot tươi → `✓ Không có blocker` (rc=0).
- `--cols so_hieu` → `⛔ WRITE_COLS_IN_SCHEMA` (rc=1) — chứng minh chống ghi-mù `so_hieu`≠`sohieu`.
- registryDocId legacy / profile-registry rỗng → `⛔ ...` (rc=1) — chống mispoint/clobber 766 dòng.
- snapshot > 900s → cảnh báo `⚠ MANIFEST_FRESH` (không chặn).

**PASS nếu:** blocker xuất hiện ĐÚNG ca sai; không blocker khi môi trường sạch.

---

## 2. VERIFIED-WRITE + JOURNAL — qua 1 lệnh reversible NHỎ

Chọn lệnh an toàn nhất có việc thật. Ưu tiên `corpus-fix --tier safe` (chỉ set corpus=false cho infra/dup — reversible).

```bash
tl corpus-fix --json                      # DRY: xem infra/dedup còn bao nhiêu (nếu 0 → dùng lệnh khác, xem Test 8)
tl corpus-fix --apply --tier safe         # GHI: chú ý dòng "journal": "corpus-fix_..." trong output
```
**Kỳ vọng output:** `corpus_false_patched` = số dòng, `journal=corpus-fix_<ts>_<pid>`. stderr KHÔNG có `⚠ patched<len`.
Nếu có `REG_WRITE_FAIL`/`patched<len` → registry chưa vá đủ (webapp index chưa thấy) → `tl boot --refresh` rồi thử lại.

```bash
tl journal                                # liệt kê các run
tl journal corpus-fix_<ts>_<pid>          # xem run vừa chạy: done/inflight/undo_ops
```
**Kỳ vọng:** `done=<số patched>`, `inflight=0`, `undo khả dụng: <n> op reversible`.

**PASS nếu:** patched = số dự kiến (verified), journal ghi đủ `done`, `inflight=0`.

---

## 3. UNDO — hoàn tác về giá trị cũ (reversibility)

```bash
tl undo corpus-fix_<ts>_<pid>                       # DRY: xem sẽ khôi phục gì (restore corpus=true)
tl undo corpus-fix_<ts>_<pid> --apply --confirm yes # GHI: trả các dòng về corpus=true
tl boot --refresh
tl reg-query --no-corpus --refresh --json | ...     # đối chiếu: các drive_id đó CÒN corpus=false không
```
**Kỳ vọng:** `restored=<n>`, `failed=0`. Sau `boot --refresh`, các dòng đã trở lại `corpus=true` (undo thành công).
⚠ Nếu undo báo `failed>0` với cột trống (vd `nlm_source_id:""`): kiểm webapp có set-empty được không (một số ca cần `reg_clear`).

**PASS nếu:** giá trị cũ được khôi phục; corpus-fix + undo = no-op ròng (chứng minh mọi ghi đảo-ngược-được).

---

## 4. RESUME — tiếp tục 1 run bị NGẮT (idempotent)

Cách tạo run "dở" thật: chạy `ingest-missing --apply` với `--limit` vừa phải rồi để timeout NGẮT giữa chừng (client kill).
Hoặc dùng chính run ở Test 2 (nếu có `inflight`).

```bash
tl ingest-missing --limit 3 --json         # DRY: xem 3 target
tl ingest-missing --limit 3 --apply        # nếu bị timeout/kill giữa chừng → có op DỞ. Ghi lại journal=ingest-missing_...
tl journal ingest-missing_<...>            # xem inflight (op chưa commit-ok)
tl resume ingest-missing_<...>             # DRY: op dở sẽ làm lại
tl resume ingest-missing_<...> --apply     # GHI LẠI op dở (idempotent — chỉ registry)
```
**Kỳ vọng:** `resume` DRY liệt kê đúng op inflight; `--apply` `reapplied=<n> failed=0`. (NLM `source_add` KHÔNG do resume —
chạy lại `ingest-missing` để nạp phần thiếu; live-dedup chống trùng.)

**PASS nếu:** op dở được ghi lại, không tạo trùng, `tl journal` sau đó thấy inflight=0.

---

## 5. LOOP — vòng lặp hội tụ có cổng-verify + fail-safe

```bash
tl loop --json                             # DRY: detect_now = số việc reversible hiện tại
tl loop --apply                            # chạy vòng lặp thật (verified + journaled)
```
**Kỳ vọng stderr:** in từng vòng `[vòng k] phát hiện X · sửa X · verify=ok`, rồi **HỘI TỤ** sau ~2-3 vòng
(`status: converged`). KHÔNG lặp quá `--max-iter` (mặc định 8). Nếu `status: paused` với `NO_PROGRESS`/`VERIFY_FAILED` →
đọc `reason`, `tl boot --refresh` rồi rà tay.

```bash
tl undo loop_<...> --apply --confirm yes   # (tùy chọn) hoàn tác toàn bộ loop
```
**PASS nếu:** loop hội tụ (converged) hoặc PAUSE có lý do rõ; toàn bộ ghi trong 1 journal `loop_*` → undo được.

---

## 6. FAIL-SAFE — precheck CHẶN --apply khi môi trường sai

Tạm để registryDocId = legacy (hoặc test trên profile dự án registry rỗng), rồi:
```bash
tl corpus-fix --apply --tier safe          # phải ABORT rc=2 với "PRECHECK_BLOCKED"
tl corpus-fix --apply --tier safe --force-unsafe   # bỏ qua (RỦI RO) — CHỈ khi bạn CHẮC
```
**Kỳ vọng:** không `--force-unsafe` → `aborted: true, reason: PRECHECK_BLOCKED` (KHÔNG ghi gì). Khôi phục registryDocId đúng.

**PASS nếu:** --apply bị chặn khi có blocker; --force-unsafe mới cho qua.

---

## 7. VERIFIED-WRITE bắt "ghi mù" (mô phỏng)

Không có cách trực tiếp gõ cột sai qua lệnh đã bọc (chúng dùng cột đúng). Kiểm gián tiếp:
```bash
tl precheck --cols "so_hieu"               # blocker (đã test ở #1) — đây là lớp chặn cột sai
```
Và quan sát: mọi lệnh --apply nếu `reg_bulk` trả `patched < số dòng` → in LOUD `⚠ patched<len` + rc≠0 (không âm thầm).
Ví dụ chạy `missing-sohieu --apply` trên vài dòng row-mới chưa index → nếu patched hụt sẽ báo to (không như bug cũ 193 dòng im lặng).

**PASS nếu:** không bao giờ có "ghi thành công ảo" — patched hụt luôn được báo + rc≠0.

---

## 8. Bao phủ 16 lệnh mutate (mỗi lệnh: DRY → apply nhỏ → undo)

Tất cả đều theo mẫu **DRY → --apply (lô nhỏ) → `tl journal <run>` → `tl undo <run>` (nếu reversible)**:

| Lệnh | Ghi gì | Reversible (undo được)? |
|---|---|---|
| `corpus-fix --tier safe` | corpus=false (infra+dedup) | ✅ (→corpus=true) |
| `loop` | corpus=false hội tụ | ✅ |
| `consolidation-cleanup` | corpus=false (thành phần) | ✅ |
| `dedup-plan` | corpus=false (dup) | ✅ |
| `quarantine-fix` | corpus=false + cat | ✅ (corpus) |
| `recat <id> --cat NN` | cat (+ move Drive) | ✅ (cat registry; KHÔNG hoàn move Drive) |
| `backfill-loai` | loai | ✅ |
| `missing-sohieu` | sohieu | ✅ (→ rỗng) |
| `vbhn-year-fix` | sohieu (+name) | ✅ (reg_upsert) |
| `relation-backfill` | goc/sua_doi | ⚠ (backfill; undo có thể rỗng) |
| `nlm-reconcile` | nlm_source_id/notebook | ✅ (link); reg_clear KHÔNG |
| `shared-source-fix` | nlm_source_id='' | ✅ (→ source_id cũ) |
| `source-rename` | name/sohieu (reg_upsert) | ✅ registry (KHÔNG hoàn tên GDoc/NLM) |
| `source-update-corpus` | corpus (reg_upsert) | ✅ (cờ corpus) |
| `confirm` | verified | ✅ |
| `source-delete` | XÓA CỨNG | ❌ bất khả nghịch — journal LƯU snapshot dòng (khôi phục TAY) |
| `ingest-missing` | nlm link (source_add) | resume được; xóa nguồn NLM tay |

**Lưu ý an toàn:**
- Luôn DRY (`--json`) TRƯỚC. Đọc kỹ số dòng sẽ đụng.
- `--apply` lô nhỏ (`--limit 2-3` nơi có).
- `source-delete` / `nlm-reconcile --clear-stale`: **bất khả nghịch** một phần — cân nhắc `source-update-corpus false`
  (reversible) trước.
- Sau mỗi --apply: `tl boot --refresh` để cache thấy thay đổi (GAS cache ~600s — đợi nếu cần).

---

## 9. Checklist PASS toàn hệ thống

- [ ] `precheck` chặn ĐÚNG (legacy doc / cột sai / profile rỗng); không chặn khi sạch.
- [ ] Lệnh --apply sinh `journal=<run>`; `tl journal <run>` thấy done/inflight đúng.
- [ ] `verified-write`: patched = số dự kiến; patched hụt → báo LOUD, không âm thầm.
- [ ] `tl undo <run>` khôi phục giá trị cũ (reversible), failed=0.
- [ ] `tl resume <run>` làm lại op dở, không tạo trùng.
- [ ] `tl loop --apply` hội tụ (converged) hoặc PAUSE có lý do; undo được toàn bộ.
- [ ] `--apply` bị chặn khi có blocker (fail-safe); `--force-unsafe` mới bỏ qua.
- [ ] `source-delete` lưu snapshot forensic trong journal (dù bất khả nghịch).

**Khi có sự cố bất kỳ trong lúc chạy LIVE:** `tl journal <run>` để xem dừng ở đâu → `tl undo <run> --apply --confirm yes`
hoàn tác → sửa nguyên nhân → chạy lại. Đây chính là điều hệ thống checkpoint bảo đảm: **hỏng ở đâu cũng lần ra + hoàn tác được.**
