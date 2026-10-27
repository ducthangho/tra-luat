# Đặc tả packet `land-81-ha-cap` r1 — hạ §8.1 của 3 hồ sơ land khai `DAT` mà thiếu phép đo effort và sandbox

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

| trường | giá trị |
|---|---|
| packet | `land-81-ha-cap` (mission #748), revision 1, generation 1 |
| review_class | `sensitive` (hồ sơ land là căn cứ cho `landed`) |
| write set | `ops/land/pr924-wp923-land-evidence.yaml`, `ops/land/pr931-wp835-land-evidence.yaml`, `ops/land/pr950-wp834-land-evidence.yaml` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `7129f7d`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, read-only, neo đúng head |

## 1. Vì sao
Connector Codex P1 trên PR #934 (review comment `4372912640`) chỉ ra một lỗi. §8.1 đòi ghi effort thực tế, §8.2 đòi ghi sandbox mode thực tế. Một hồ sơ khai `reviewer_assurance_81: DAT` trong khi biên nhận chỉ đo model là khai mạnh hơn phép đo. Hồ sơ `pr932` đã được sửa như vậy.

Đo trên `7129f7d` (27-10-2026): 3 hồ sơ còn mang đúng lỗi ấy. Không biên nhận `run.json` nào của chúng có trường effort hay sandbox: 1 của `pr924`, 3 của `pr931`, 8 của `pr950`, cả 12 tệp đều chỉ đo model. Đó là các hồ sơ mà packet `land-evidence-l7` miễn trừ L7 theo băm, ghi thành nợ `NO-L7-3-HO-SO-KHAI-DAT-THIEU-DO`. Chủ kho chọn hạ chúng (phương án a, trong phiên ngày 27-10-2026).

## 2. Thay đổi, cho mỗi hồ sơ
1. **Sửa tại chỗ khối `assurance_81`**, theo tiền lệ `pr932-wp748-r26` (PR #934):
   - `reviewer_assurance_81: CHUA_DAT`;
   - `review_exact_sha: DAT`, kèm `review_exact_sha_nguon` là lời khai `measured` trỏ tới đúng `run.json` và verdict của lượt approve trên `authorized_head_sha` mà hồ sơ đang dẫn;
   - `thuc_thi` có ba khoá:
     - `model`: `measured` trỏ tới `run.json` ấy, ghi số response và tên model đúng như trong tệp;
     - `effort`: `not_measured`, kèm lý do;
     - `sandbox_mode`: `not_measured`, kèm lý do;
   - `lich_su`: ghi rằng bản trước khai `DAT`, lỗi do connector P1 #934 phát hiện, và việc hạ thuộc packet này.

   Các khoá khác đang có trong khối được giữ nguyên.
2. **Thêm một khối cấp gốc `ha_cap_assurance_81_20261027`** ở cuối tệp. Khối này nói rằng mọi câu khác trong tệp nhắc "§8.1 DAT" hay "assurance_81 DAT" đều đã bị khối `assurance_81` thay thế. Các câu đó **giữ nguyên** làm lịch sử, giống nếp `landed_20261027` "không sửa dòng nào ở trên".
3. **`landed` giữ nguyên.** §10.2.4 định nghĩa `landed` là "vào canonical ở exact SHA được duyệt, hậu-merge gate xanh và bookkeeping xong", không đòi §8.1. Khối ở mục 2 phải ghi thêm hai điều:
   - lời duyệt `landed` của chủ kho (với `pr924`/`pr950`: comment `6432778847` trên #962; với `pr931`: căn cứ ghi trong hồ sơ) từng dẫn assurance `DAT` làm điều kiện (4);
   - rút `landed` là quyết định riêng của chủ kho, packet này không tự làm.

## 3. Tiêu chí xong
- Với mỗi hồ sơ, `reviewer_assurance_81` chuẩn hoá thành `CHUA_DAT`, và `thuc_thi` đủ ba khoá.
- `python ops/land_evidence_nguon.py` trên cây thật ra `TỔNG: ĐẠT`.
- Nếu L7 (packet `land-evidence-l7`) đã có trên base, cả 3 hồ sơ ĐẠT mà không cần miễn trừ L7: băm lệch thì mất miễn trừ, nhưng L7 không áp vì giá trị là `CHUA_DAT`. Nếu L7 chưa có, chạy bộ kiểm của nhánh L7 lên ba tệp, kết quả phải ĐẠT.
- Mỗi lời khai `measured` mới có token nguồn phân giải được (L1).
- Các khoá đã có và giá trị `landed` không đổi. Kiểm bằng cách so diff YAML đã nạp: chỉ `assurance_81` và khoá mới được phép khác.
- Review chéo Codex qua `launcher.py run` trên đúng head, tới khi 0 P0–P3.

## 4. Trần
- Kích thước: ≤ 3 tệp / ≤ 150 dòng thêm.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- Không sửa `ops/land_evidence_nguon.py` hay test. Sau packet này, `MIEN_TRU_L7` thành các mục chết (vô hại: băm không còn khớp và L7 không áp). Gỡ chúng là nợ `NO-L7-MIEN-TRU-CHET`, làm sau khi L7 land.
- Không rút `landed`, không đo lại hay chạy lại review nào, không tạo provenance mới.
