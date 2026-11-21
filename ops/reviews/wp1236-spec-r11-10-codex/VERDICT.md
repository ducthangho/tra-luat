# Review đặc tả wp1236 r11 sửa 1 — vòng 10

**changes_requested — 1 P2, 0 P3 mở.** Review chỉ ở mức đặc tả, class `sensitive`.

- Reviewed SHA: `90cb0a69056f786aebebebb52033594185ef67fe`; tree `6e7af40e7672e4b6f74425ea4909e3becf24d954`.
- SPEC SHA-256: `84e3c8f2fbee831be02e7623c8fc7fda43e3d7394802cc8b74df4ae9228b1bc1`; byte trùng blob Git.
- Provider/surface/transport: `openai_codex / codex_cli / machine`; model/effort phục vụ `KHONG_DO_DUOC`. Run `0b363962d8164bddb8bec9b6157986b6`.

## AA01 · P2 · `nghiem-thu-khong-co-lap-chot-dich`

Luật 6 (SPEC:366–386) băm được bảng delta nhưng chưa chốt seed và phép quan sát. 36 ô `mien` lấy body/readback/chuỗi lời khai từ `DONG` và constructor trong mã tham chiếu. Phép chiếu bỏ JSON path/tên tệp/prefix của `ho_so` cũng chỉ có trong `chay_o`, chưa được định nghĩa trong đặc tả.

Phản chứng chạy được: chỉ đổi ngày hợp lệ của seed `2026-12-31` → `2026-11-30`, băm tập125 ô vẫn `6f129585…`, mã gốc khớp36/36 ô `mien` ở cả hai. Cùng đột biến chỉ nhận ngày31 khớp36/36 với seed đầu,22/36 với seed sau. Chạy chính `a126`: seed đầu rc0, seed sau rc3 ở `mien.os:H6a` (mong `os`, nhận `han`). Vì vậy tập ô phân biệt chưa được xác định duy nhất bởi băm. Không suy từ phép đo này rằng đột biến ngày31 được miễn luật ưu tiên1/2/4/5.

Sửa tại luật6/artifact: đưa seed nghiệp vụ và quy tắc dựng input/projection vào hợp đồng được băm. Đổi seed phải đổi băm hoặc bị từ chối. Giữ projection tối thiểu, không ghim đường scratch vật lý và không sửa luật sản phẩm. Bằng chứng: [seed_full.jsonl](seed_full.jsonl), [seed_probe.json](seed_probe.json), [output_projection.json](output_projection.json); script [audit_cell_semantics.py](audit_cell_semantics.py), [audit_seed_full.py](audit_seed_full.py).

## Kết quả kiểm

- **125/125** ID duy nhất, đúng băm chuẩn; `bang_o()` sinh đúng file hai lần. Mã gốc và bản chuẩn `ast.unparse` qua `a126` rc0.
- **125/125 kỳ vọng** suy được từ luật với seed/projection của mã tham chiếu; không lấy output sản phẩm làm oracle. Các tiền đề còn ngoài đặc tả được ghi trong [semantic_derivations.json](semantic_derivations.json).
- Áp đủ **25** `r7_*`/`r8_*`, mỗi neo xuất hiện đúng1 lần: **20 chết đúng `a126`, 5 xanh**; không lỗi setup. Năm xanh là URL lặp, delimiter consumer, `./`, prefix CLI, fallback stem. Chúng thuộc luật1/4/5 ưu tiên và chết đúng `a125`/`a210`, baseline hai ca đều xanh. Không thấy đột biến lịch sử có ô phân biệt theo interpreter tham chiếu mà `a126` vẫn xanh. [Kết quả25](a126_results.jsonl), [tuyến ưu tiên](priority_routes.json).
- **20/45 hàng** có125 ô; **25 hàng còn lại** được đối chiếu từng hàng trong [row_ledger.json](row_ledger.json), với lý do và tuyến luật1/4/5. Inventory61 là bản lọc lịch sử, không phải toàn bộ73 ASTCompare. Không lấy thiếu ô làm miễn ngữ pháp/hồi quy.
- `a127` và `a128` rc0; `m65`/`m79` đều chết đúng chốt `a128`. Hai chế độ nền là mô phỏng; **Windows native chưa chạy**. [Bằng chứng](seams.json).
- Kho cộng dồn **152 ID** đúng băm `f311a24c…`, phân rã127+14+11. Numstat mã tham chiếu **1777 dòng thêm /3 tệp**, dưới trần **2100 đang đề nghị**, chưa phải quyền thi công. [Số đo](counts.json).

## Đối chiếu vòng 9

| Lớp | Kết quả mức đặc tả | Bằng chứng |
|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` (Z01) | `VA_MOT_PHAN` | Tập125/ưu tiên đã có; AA01 còn seed/projection |
| `test-thieu-chot` (alias lịch sử) | `VA_MOT_PHAN` | Giữ cùng cơ chế, không đếm thêm một lớp |
| `so-do-khong-cung-pham-vi-nguon` (Z02) | `DA_VA_THAT` |152ID/hash/ledger tập khớp |

Các lớp trước đã `DA_VA_THAT` được giữ;10 khối hợp đồng liên quan không đổi byte. Không coi scope cut hay tổng suite là bằng chứng vá. Hội tụ **1/2**; giữ lịch sử lớp lặp≥3 và checkpoint§12, không tự cấp thêm vòng/ngân sách.

Chưa chạy full152 ledger, full suite/scanner, CI, native Windows hoặc mạng. Snapshot đầu/cuối kiểm HEAD/tree và hash tracked/untracked/ignored; xem `VERDICT.json`. Không có quyền merge/land từ verdict này.

KET_LUAN: changes_requested
