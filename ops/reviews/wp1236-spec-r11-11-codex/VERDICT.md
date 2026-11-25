# Review đặc tả wp1236 r11 — vòng 11

**Verdict: approve ở mức ĐẶC TẢ.** Không có P0/P1/P2/P3 mở; không dùng waiver để đóng P3.

- `reviewed_sha`: `2d9baf001983871efb4af9dc3c7ad65ba24e0667`
- `reviewed_tree`: `a6f95229f02f56b9ad15ad9e99f5a3002e311d59`
- `spec_sha256`: `30386131d8017bf982ca0be7707c8d5fd3035e9586c5f94a446f45c40fc863d1`
- Nguồn: `SPEC.md` bằng byte với `2d9baf0:ops/specs/wp1236-r11.md`. Nội dung thực tế là r11 bản sửa 2 (đóng AA01), dù tiêu đề lời giao ghi bản sửa 1.
- Mã tham chiếu: `2719f81dd5c3f89e4986f6710ed2145cfd4c057b`, chỉ dùng đo khả năng thi công; module sản phẩm không đổi so `79b3c24`.
- Identity: `openai_codex / codex_cli / machine`, họ `openai`; run `ce758fc0cbc74dd3a09ba110f0e1fbd7`, session `01a1fc8d-40cb-7920-8d89-4bb268c984b1`. Serving model/effort: `KHONG_DO_DUOC`; nguồn provider/surface/transport là `../run/ce758fc0/run.json`. Sandbox thực tế `workspace-write`; thao tác trong repo chỉ đọc. Không dùng subagent/context executor.

## Đối chiếu §8.3

| Slug giữ nguyên | Nhãn vòng 11 | Bằng chứng |
|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` — Z01 → AA01 | `DA_VA_THAT` ở mức đặc tả | Hạt giống, byte fixture và projection nằm trong hash; 125 oracle luật và reader độc lập; phản chứng thay seed/projection bị chặn. |
| `test-thieu-chot` — alias lịch sử `VA_MOT_PHAN` | `DA_VA_THAT` ở mức đặc tả | 25 mutant lịch sử, 45 hàng, các tuyến ưu tiên; không có ô phân biệt bị a126 bỏ sót. Không đồng nghĩa đóng review mã đợt A. |
| `so-do-khong-cung-pham-vi-nguon` — Z02 | Giữ `DA_VA_THAT` | Kho đúng 152 ID, băm khớp; 125 ô; 1.795 dòng thêm. |

Các lớp đã đóng khác giữ trạng thái: tám khối hợp đồng không đổi, 125 delta/kỳ vọng cũ giữ nguyên và mã sản phẩm không đổi. Chi tiết từng slug trong `prior_class_status` của JSON. Không tái mở lớp khi chưa có phép đo hồi quy.

Hội tụ vòng 10 → 11: **1/1**; hai slug đầu là alias đã nối từ vòng 10, đếm một lớp. Giữ nguyên lịch sử lớp lặp lần ba. Đây là lời gọi **12/12**, không tự cấp thêm lượt.

## Phép đo quyết định

1. **Tập đóng:** JSON chuẩn `{hat_giong,chieu,o}` có băm `628e27046ab4ba7a7b3cf31eb65ded9b88c718c5bfd067401d12b60d2c21b857`. `bang_o()` sinh đúng artifact hai lần, 125 ID duy nhất, 4/4 hash byte fixture khớp. Phần `o` giữ nguyên băm cũ `6f129585…`.
2. **Oracle:** reader do reviewer viết chỉ dùng JSON frozen dựng đầu vào; suy kỳ vọng từ K2–K8/`kiem_mien` trong *Module mới*, rồi mới chạy sản phẩm. **125/125** khớp cả hàm lá và consumer; không dùng kết quả sản phẩm để tạo oracle. Đổi ngày hợp lệ 31→30, đổi bốn projection hoặc byte fixture đều bị guard từ chối.
3. **Phủ đột biến:** áp đủ **25/25** `r7_*`/`r8_*`, mỗi neo đúng một lần trên `ast.unparse`. Riêng `a126`: baseline rc0, **20 GIẾT rc3 đúng tên ca**, **5 sống rc0**. Reader độc lập xác nhận 20 ô phân biệt và kiểm trọn 125 ô cho từng mutant sống: **25/25 phân hạng khớp**, 645 quan sát; không có ô phân biệt mà a126 xanh.
4. **Năm mutant sống ở a126:** `r7_url_dedup`, `r7_consumer_delimiter`, `r7_dotpath_raw` bị `a125` giết theo luật 4/5; `r7_cli_limit_prefix`, `r7_cli_fallback_stem` bị `a210` giết theo luật 1/5. Mỗi ca baseline rc0, mutant rc3 đúng `TinHieuChotCa`. Vì vậy không hạ chúng thành P3 ngoài bảng. Luật 1/2/4/5 xét trước luật 6; sau đó ô phân biệt quyết P2, thiếu ô quyết P3 và vẫn phải đóng/miễn theo M1.
5. **45 hàng:** 20 hàng nối đủ 125 ô; 25 hàng còn lại có lý do riêng và tuyến luật 1/2/4 trong [row_ledger.json](row_ledger.json). Đặc biệt `attempt` là số nguyên dù cột lịch sử ghi nhầm `run.head_sha`; `conclusion` dùng `\w+` không phải enum đóng, vẫn chịu K5 và luật ngữ pháp. Không lấy nhãn `ngu_phap` để miễn hồi quy. Các họ lượt 6 nối luật trong [r6_family_routes.json](r6_family_routes.json).
6. **Số tổng:** kho **152 ID duy nhất = 127 + 14 + 11**, băm `f311a24c21693df4f291fe4cdb34c1c3575b4d646cfae6106b2d5e3b09a72d05`; bảo toàn 127 ID cũ. Diff mã tham chiếu từ `010046f…`: **3 tệp, +1.795 = 343 + 1.451 + 1**, phù hợp “≈1.800”. **2.100 là đề nghị chờ chủ kho duyệt**, verdict này không cấp authority đó.
7. **Hai nền/seam:** `a127` đạt cả hai chế độ mock và bốn phản chứng mỗi chế độ; `a128` baseline rc0, hai mutant stat/absolute-path rc3 đúng ca. Không dùng các số này làm bằng chứng Windows native.

Lệnh và rc chi tiết ở `da_do_khop`; từng tiến trình đột biến ở [a126_results.jsonl](a126_results.jsonl), phân hạng ở [classification_ledger.json](classification_ledger.json), đối chứng ở [controls.jsonl](controls.jsonl), oracle ở [independent_cells.jsonl](independent_cells.jsonl), guard ở [seed_guards.json](seed_guards.json).

## Giới hạn và bàn giao

- `passed`: các phép đo ở trên; `failed`: không có phép đo nội dung thất bại; `skipped`: không có. Một lỗi setup đọc sai ref chứa kho lượt 6 đã được sửa nguồn sang exact spec SHA rồi đo lại rc0; không tính lỗi setup là finding sản phẩm.
- `not_run`: native Windows, full ledger 152 trên mã cuối, full scanner/product suite, selftest/CI/release, Ruff contract/lint, GitHub/network readback. Đây là review đặc tả, không phải review/approval mã hoặc xác nhận gate phát hành.
- Snapshot đầu/cuối: **17.515 hash tệp không đổi**, HEAD/tree/status/diff/index giữ nguyên; `git diff --check` rc0. Chỉ chứng minh không có delta ở hai mốc, không chứng minh lịch sử ghi rồi hoàn nguyên. Mọi script/bản sao/tempfile đo nằm dưới `work`.
- `approve` chỉ cho nội dung đặc tả trên exact SHA/hash trên. E2/E5, lease thi công, Windows/CI, audit chủ kho, merge/land và terminal receipt của launcher vẫn theo hợp đồng riêng; không tự ghi `cross_approved` hoặc `human_audited`.
- Kiểm schema: `python3 ../kiem_verdict_lop.py VERDICT.json --vong 11`; **rc0, HOP_LE (§8.3): 0 finding, 1 lop**, lưu tại `kiem_verdict.txt`.

KET_LUAN: approve
