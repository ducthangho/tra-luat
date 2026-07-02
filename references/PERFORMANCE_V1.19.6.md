# v1.19.6 — Phân tích hiệu năng + tối ưu load/tra cứu

Ngày: 2026-06-24 · Đo THẬT trên live `2.21.2i` (config `tra_luat_config.v2.json`, profile `Luật BHXH`).

## 1. Số đo khách quan (`tl perf`)

| Thao tác | wall | server_ms | Ghi chú |
|---|---|---|---|
| `ping` (round-trip median, x5) | **~3.3s** | ~25–113ms | server xử lý tí xíu |
| `ping` x4 SONG SONG (tổng) | ~4.8s | — | **~2.8–3.2x** nhanh hơn tuần tự |
| `manifest` (metadata) | ~2.9s | ~178ms | |
| `find` (1 số hiệu, fulltext) | ~5.5s | **~1448ms** | find server-heavy (Drive search) |
| `boot` lần đầu / `--refresh` | **~10–14s** | — | 2 call (manifest_export + download) |
| `boot` cache-hit (v1.19.6) | **~0.2s** | — | **0 call webapp (~50x nhanh)** |

## 2. Nút thắt (kết luận)

**Hơn 95% thời gian là ĐỘ TRỄ HTTP của Google Apps Script `/exec` (~3s/round-trip), KHÔNG phải logic/Python.**
`server_ms` chỉ vài chục ms cho hầu hết action. Hệ quả: thời gian ≈ **3s × (số call webapp)**.

- `boot` cũ làm 2 call tuần tự + **tải lại mỗi lần** → ~12s mỗi lần khởi động.
- `locate/find` miss cache → gọi webapp `find` (3s round-trip + tới ~1.4s server) → 5–6s.
- Các lệnh tra cứu nhiều số hiệu chạy TUẦN TỰ → cộng dồn 3s/số hiệu.

## 3. Đã tối ưu (client, KHÔNG cần deploy)

1. **`boot` tái dùng cache local theo TTL** (`_fallback/boot.py`): nếu `manifest_index.json` còn tươi
   (mtime < TTL, mặc định 600s; env `TL_BOOT_TTL`) → tái dùng, **0 call webapp**. `--refresh` ép tải lại,
   `--max-age <giây>` chỉnh ngưỡng. → boot lặp lại **~12s → ~0.2s (đo thật, ~50x)**.
2. **Đo thời gian tự động:**
   - `tl perf [--json]`: suite đo round-trip / lợi ích song song / trạng thái cache + chẩn đoán.
   - `--timings` (hoặc env `TL_TIMINGS=1`): in `[timing] <action> wall/server/client` cho MỌI call.
3. **`gas_parallel(calls)`**: chạy nhiều call ĐỘC LẬP song song (~2.8–3.2x). Dùng cho verify/tra cứu nhiều
   số hiệu, source-map nhóm luật, prefetch. (Đã dùng trong `tl perf`; có thể nối vào source-map/exists.)

## 4. Khuyến nghị tiếp theo

**Client (làm thêm, không deploy):**
- `locate/find/exists` ƯU TIÊN offline `manifest_index` (0 call); chỉ gọi webapp khi thật sự miss.
- Gói các tra cứu nhiều số hiệu qua `gas_parallel` thay vòng lặp tuần tự.
- Cân nhắc cache kết quả `find` theo (q → rows) trong phiên để khỏi gọi lại.

**Server (cần deploy 1 bản `.gs` mới — giảm SỐ call/giảm server_ms):**
- **Gộp boot còn 1 round-trip:** thêm action trả manifest CÓ `entries` inline (khỏi cặp `manifest_export`+`download`).
  → boot lạnh ~12s → ~3–4s.
- **`changes_pull` (delta)** thay full reload khi corpus đổi nhỏ — chỉ kéo phần thay đổi.
- **regen2 quét folder SONG SONG** bằng `UrlFetchApp.fetchAll`/Drive batch (hiện quét per-parent tuần tự, KI-27).
- **`find` rẻ hơn:** ưu tiên tầng registry/sohieu trước fulltext (server_ms ~1.4s chủ yếu ở fulltext Drive search).

## 5. Có cần REFACTOR không?

**KHÔNG cần refactor kiến trúc.** Kiến trúc (webapp Apps Script + manifest offline + CLI `tl`) là HỢP LÝ;
nút thắt là I/O latency + thiếu cache/parallel, đã/đang vá bằng thay đổi khu trú (không viết lại).

Nợ kỹ thuật nên DỌN (hygiene, không phải refactor lớn):
- Nhiều bản `.gs` lịch sử (2.21.1 → 2.21.2i) + nhiều `MERGE_/DELTA_/PROFILE_SCOPE` chồng lấn → gộp/lưu trữ.
- `SKILL.md` khá dài → tốn context khi nạp; có thể tách phần ít dùng xuống reference.
- Cân nhắc đổi nền đồng bộ nặng (regen2/manifest) sang job định kỳ thay vì trong luồng tương tác.
