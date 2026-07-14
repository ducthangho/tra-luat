# ADR-0008 — Topology shard hợp nhất (declared+observed) và partial trung thực

- **Trạng thái:** Chấp nhận (v1.34.49, 2026-07-15). Grill-with-docs D1–D7 user duyệt
  (`D:\Quốc hội\ke-hoach-overflow-sharding-v1.34.49-50-2026-07-15.md`).
- **Nguồn:** audit overflow-sharding v1.34.46 (9 finding) + bundle Codex `c98321f0…a6ca` làm SPEC —
  code viết lại trên canonical (bundle nền v1.34.46 lỗi thời; GAS "2.21.2k" của bundle đụng độ định danh
  với 2.21.2k live → KHÔNG merge file; ADR-0001 giữ nguyên).

## Bối cảnh

Corpus VBQPPL vượt cap một notebook NLM → shard (base + VBQPPL-2 + …). Tới v1.34.48, đường ĐỌC đã đa-shard
qua registry (`_resolve_overflow_shards` v1.34.47) nhưng: đường GHI/ROUTE chỉ hiểu base + MỘT overflow;
`ingest-missing` chọn 1 shard/run rồi `break` khi đầy mà vẫn `ok:true, rc=0` (thành công giả); đọc slot live
không kiểm `ok` → auth-fail thành "0 nguồn" (phantom-room); recovery không ghi `row_kind` → sweep mất dấu
shard; cap 300 hard-code trong khi Google có 50/100/300/400/600 theo edition.

## Quyết định

1. **Một resolver duy nhất `_resolve_shard_topology(entries, base, cfg, profile)`** cho MỌI đường
   đọc/ghi/audit. **Declared** = `profiles.<p>.shards[]` — dict `{id, role, capacity, enabled, priority}`
   hoặc list[str] legacy (phần tử trùng `notebookId` = primary — đúng dạng config live). **Observed** =
   env `TL_OVERFLOW_NOTEBOOK_ID` + registry `row_kind='overflow'`.
2. **Fail-closed bất đối xứng có chủ đích:** alias legacy lệch declared / id trùng / capacity sai →
   `TOPOLOGY_CONFIG_CONFLICT`: đường GHI/ROUTE dừng rc=2 TRƯỚC side-effect; đường ĐỌC/SWEEP dùng UNION
   (không bỏ sót nguồn) và lộ findings — doctor/route mới là nơi chặn. Shard lạ trong registry khi ĐÃ
   declared → `enabled=false` + `UNDECLARED_REGISTRY_SHARD`, KHÔNG tự route vào.
3. **Partial trung thực (F-02):** `ingest-missing` phân bổ theo live-room MỌI shard enabled; drift đầy giữa
   run (phân loại `_nlm_add_capacity_error`: shard-full ≠ quota) → failover shard kế TRONG CÙNG RUN với
   chính drive_id (không upload lại); cạn mọi shard → `ok=false, partial=true, remaining, resume_command,
   rc=2`. Blocked upfront cũng rc=2 (bỏ rc=0 "gate có chủ đích" — orchestrator phải thấy backlog còn).
4. **Đọc slot fail-closed (F-05):** `_live_source_count()` dùng chung — `{ok:false}` không bao giờ thành 0.
   Đường ghi: self-heal `load_creds` đúng 1 lần/run rồi dừng `LIVE_READ_FAILED`; đường đọc:
   `live_read_failed=true`.
5. **row_kind suy từ topology (F-06):** reconcile/nlm-add link+backfill ghi `overflow` khi đích là shard
   overflow; primary giữ blank (=own); kind nghiệp vụ `ref`/`thuong` (hằng `_ROW_KIND_PROTECTED`) không bao
   giờ clobber. Doctor kiểm bất biến notebook↔row_kind REPORT-ONLY.
6. **Capacity là policy (F-07):** `shards[].capacity` > `TL_NLM_SOURCE_CAP` > 300 default; live count là
   ground truth khi route.
7. **Chứng minh snapshot (F-09):** `_topology_hash` (sha256 canonical, golden
   `references/golden/topology_vectors.json` — tương thích chéo GAS 2.21.2l đợt 50) + `_topology_stamp`
   (`topology_hash`/`routing_epoch`/`registry_digest`) stamp vào `tl manifest`/`registry-map` client-side.

## Hệ quả

- 47 call-site đọc/audit/query nâng đa-shard declared miễn phí qua wrapper `_resolve_overflow_shards`.
- Test đụng resolver phải HERMETIC (`_read_config_record` patch) vì resolver đọc config-of-record thật.
- Đổi hành vi công khai: `ingest-missing` blocked/partial trả rc=2 (trước: blocked rc=0).
- Đợt 50 (grill riêng trước khi code): GAS 2.21.2l = hợp nhất 2.21.2k live (doNlmPreflight_ overflow) +
  `ingest_claim` (F-04 reservation xuyên host) + `reg_get_bulk` (F-08 micro-batch ~50→9 call/25 dòng) +
  manifest stamp server-side + export bỏ default `row_kind||'own'`.
