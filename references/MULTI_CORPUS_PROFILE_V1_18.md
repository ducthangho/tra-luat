# MULTI-CORPUS PROFILE v1.18

> **[TÀI LIỆU LỊCH SỬ — đúng theo thời điểm viết.]** Các nhắc webapp/version-gate trong file
> (ví dụ `2.21.2g`, "nếu chưa deploy .gs sửa slot") là lịch sử. Version-gate/contract HIỆN HÀNH:
> `references/API_CONTRACT.md` (webapp **2.21.2m**) + `references/RUNBOOK.md`. Nội dung dưới đây
> giữ nguyên văn, KHÔNG cập nhật.

Ngày: 2026-06-22 (cập nhật trạng thái v1.19.1)  
Contract live: webapp **2.21.2g** (Cách B registry/manifest riêng theo profile + writeconfig giữ profiles, đã deploy). Doctrine backfill: xem `DELTA_v1.19.md §C.1` (KHÔNG xoá VBQPPL canonical; thêm dòng tham chiếu). Không tự deploy Apps Script.

## Mục tiêu

v1.18 giải quyết ba vấn đề:

1. Link tải cho người dùng cần ưu tiên nguồn tiện tải Word/PDF và xem hiệu lực.
2. Văn bản thường không được mặc định vào corpus/notebook VBQPPL.
3. Mỗi corpus cần registry/manifest riêng; slot NLM phải tính theo notebook đích.

## Link tải cho người dùng

Thứ tự ưu tiên link DOWNLOAD người dùng tự tải:

1. `thuvienphapluat.vn`
2. `luatvietnam.vn`
3. `congbao.chinhphu.vn`
4. cổng official khác: `vbpl.vn`, `vanban.chinhphu.vn`, `.gov.vn`
5. trang khác

Quy tắc này chỉ áp cho link tải tiện dụng. Canonical để lưu, đối chiếu nguyên văn và làm nguồn rà soát vẫn official-first.

Kiểm bằng:

```bash
python scripts/tl.py link-priority <url1> <url2> --json
```

## Config v2 và profile

Mỗi corpus là một profile:

```json
{
  "schema": 2,
  "webappUrl": "<từ VBQPPL>",
  "token": "<từ VBQPPL>",
  "defaultProfile": "vbqppl",
  "profiles": {
    "vbqppl": {
      "rootFolderId": "...",
      "notebookId": "743ed200-2e55-4673-b7a0-9bfd13b41ce6",
      "registryDocId": "...",
      "manifestId": "...",
      "categories": {}
    },
    "vbthuong": {
      "rootFolderId": "...",
      "notebookId": "fec6c125-e01c-433d-aed5-666c16540dd8",
      "registryDocId": "...",
      "manifestId": "...",
      "categories": "inherit"
    }
  }
}
```

Luôn đọc `tra_luat_config.json` của VBQPPL trước để lấy `webappUrl/token`, rồi overlay `TL_PROFILE` hoặc `--profile`.

```bash
python scripts/tl.py --config config.json --profile vbthuong profile-info --json
```

`vbqppl` giữ tương thích cũ. Khi xử lý văn bản thường, dùng `vbthuong` hoặc profile dự án; folder/notebook/registry/manifest mặc định không phải VBQPPL.

## Manifest fallback

Khi ở profile P:

1. Tra/dedup theo manifest + registry của P trước.
2. Miss mới fallback VBQPPL và báo rõ nguồn fallback.
3. QA xuyên corpus dùng `cross_notebook_query` với notebook P + notebook VBQPPL.
4. Canonical của P thắng; VBQPPL chỉ là nền dùng chung.

Cache manifest cũng tách theo profile: `vbqppl` dùng cache cũ, profile khác dùng `~/.tra_luat_cache/<profile>/`.

## Registry/manifest riêng cho profile mới

Quy trình tạo profile mới, sau khi người dùng xác nhận:

1. Chọn hoặc tạo folder Drive gốc của profile, lấy `rootFolderId`.
2. Tạo registry Google Sheet mới theo đúng cột hiện hành, gồm `nlm_notebook_id`.
3. Chạy manifest export riêng cho registry/notebook profile, tạo `tra_luat_manifest.<profile>.json`, lấy `manifestId`.
4. Ghi các ID vào `profiles.<profile>` trong config v2.

## Slot theo notebook

Lỗi cũ: `nlm_slots`/`nlm_preflight` đếm mọi row có `nlm_status`, khiến notebook dự án bị báo full giả.

Quy tắc mới:

- Khi đẩy nguồn, ghi `nlm_notebook_id = <notebook đích>`.
- `nlm_slots(notebookId)` và `nlm_preflight(... notebookId)` chỉ đếm rows có `nlm_notebook_id == notebookId`.
- Với registry riêng theo profile, cách đếm này tự nhiên chính xác hơn.

Kiểm offline:

```bash
python scripts/tl.py slot-audit --manifest manifest.json --notebook-id <notebookId>
```

Nếu chưa deploy .gs sửa slot, có thể dùng MCP `source_add(source_type=drive, document_id=<drive_id>, notebook_id=<đích>)` sau khi người dùng xác nhận, rồi đối chiếu `notebook_get`.

## Khóa định danh chặt

Không chốt nguồn hoặc push NLM theo hit mờ chỉ khớp số. Với các số trùng như `90/VPQH`, `80/2025`, `26/2026`, `121/VBHN`, phải khớp theo:

- số hiệu đầy đủ;
- năm;
- loại;
- chủ đề/trích yếu;
- verify dòng đầu hoặc nội dung.

