# Bổ sung 1 cho handoff f4e93b3 (không đổi ứng viên, không đổi `handoff.yaml`)

Lập 2026-11-24 ~13:2xZ, sau khi đọc tin của phiên điều phối (xếp hàng 11:53Z, tới phiên executor sau lúc lập handoff).

## Câu hỏi E3 đã có quyết định

Chủ kho quyết, phiên điều phối ghi hộ ở #1236 issuecomment-7130670276 (đã đọc lại qua REST: `created_at` 2026-11-24T11:52:50Z):

1. Luật 9 cho đợt B và C dùng miền DELTA cộng điều kiện không hồi quy trên phần kế thừa; đột biến sống sẵn của mã cũ khai là nợ.
2. Cho phép bí danh `GATE_OUTPUT_DOI_CHIEU_MA` trong test.

Hai mục `cau_hoi_mo` mã E3 trong `handoff.yaml` vì thế đã đóng. Mục M3 (phân loại Windows) còn mở.

## Tệp nộp thêm theo yêu cầu của điều phối

| tệp | nội dung | kiểm |
|---|---|---|
| `luat9/base-f602325/manifest.jsonl.xz` | manifest ĐẦY ĐỦ của base (550 đột biến, kèm toàn văn nguồn) | giải nén rồi `sha256sum` phải bằng dòng `manifest.jsonl` trong `luat9/base-f602325/SHA256SUMS-D` |
| `luat9/head-f4e93b3/manifest.jsonl.xz` | manifest ĐẦY ĐỦ của head (624 đột biến) | như trên, với `luat9/head-f4e93b3/SHA256SUMS-D` |
| `luat9/ke-thua-base-len-head.jsonl.xz` | đầu ra đầy đủ của `hoi-quy` (bảng tách delta: 548 áp được, 2 không) | sha256 từng dòng áp được nằm trong manifest head ⇒ kế thừa |

Đã có sẵn từ commit đầu: `luat9/so-base-head-f4e93b3.md` (ledger delta 76 ID và bảng kế thừa không GIET, từng ID), `luat9/so_base_head.py` (script
sinh bảng), `luat9/*/kq.jsonl`.

Bảng kế thừa trong `so-base-head-f4e93b3.md` chỉ liệt kê ID KHÔNG GIET ở head (186). Bảng so đủ 548 ID dựng lại bằng:
`python3 luat9/so_base_head.py <D_base> <D_head> <ke_thua.jsonl> <ra.md>` với `D_*` chứa `manifest.jsonl` + `kq.jsonl` đã giải nén.
Số tóm tắt: ở base 333 GIET · 187 SONG · 28 VO_CAN; ở head 362 GIET · 173 SONG · 13 VO_CAN; 0 ID GIET ở base mà không GIET ở head.
