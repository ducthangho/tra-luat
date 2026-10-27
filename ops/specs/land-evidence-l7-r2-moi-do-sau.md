# Đặc tả packet `land-evidence-l7` r2 — L7 đọc `reviewer_assurance_81` ở mọi độ sâu, không chỉ `$.assurance_81`

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet | `land-evidence-l7` (mission #748), revision 2, generation 1 |
| review_class | `sensitive` (cổng nghiệm thu hồ sơ land) |
| write set | `ops/land_evidence_nguon.py`, `ops/land_evidence_nguon_test.py` |
| base | `origin/master` lúc cấp lease, **phải chứa merge của `land-81-ha-cap` r2** |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, read-only, neo đúng head |
| depends_on | `land-81-ha-cap` r2 (`ops/specs/land-81-ha-cap-r2-pr870-889-896.md`) |

## 1. Vì sao
L7 r1 (`ops/specs/land-evidence-l7-assurance-thuc-thi-r1.md` trên nhánh `ops/wp748-r28-l7-lease`, PR #973) chỉ đọc `du_lieu.get("assurance_81")` (`ops/land_evidence_nguon.py`, hàm `kiem_ho_so`). Một hồ sơ ghi `reviewer_assurance_81: DAT` ở bất kỳ chỗ nào khác thì qua L7 mà không bị đòi phép đo nào.

Đo trên `20a2e2b` (27-10-2026), quét mọi mapping ở mọi độ sâu, kể cả bên trong list:
- 78 hồ sơ, 14 hồ sơ có khối `assurance_81` cấp gốc;
- **2 hồ sơ** có khoá `reviewer_assurance_81` lồng bên trong, chuẩn hoá ra `DAT`, mà **không** có khối `assurance_81` cấp gốc: `pr870-claude-md-bai-hoc-c` và `pr889-claude-md-bai-hoc-c` (cùng ở `$.cap_nhat_20261026.reviewer_assurance_81`). Cả hai đều mang đúng lỗi L7 sinh ra để chặn.

Packet `land-81-ha-cap` r2 thêm khối `assurance_81` cấp gốc `CHUA_DAT` cho hai hồ sơ ấy, nên sau khi nó land thì phép đo trên ra **0**. Đó là lý do có `depends_on`: chạy packet này trước thì cây thật ĐỎ.

## 2. Luật L7 r2
- **Có khối cấp gốc ⇒ khối ấy là nguồn duy nhất.** `$.assurance_81` là mapping thì L7 áp y như r1 lên khối ấy và bỏ qua mọi khoá `reviewer_assurance_81` lồng bên trong. Lý do: hồ sơ lịch sử chỉ được thêm, không được sửa, nên câu `DAT` cũ vẫn nằm đó sau khi đã bị thay thế. Mỗi khoá lồng chuẩn hoá ra `DAT` bị bỏ qua được ghi một **ghi chú**, không phải vi phạm, nêu đường dẫn JSON của nó.
- **Không có khối cấp gốc ⇒ quét mọi độ sâu.** Duyệt mọi mapping, kể cả bên trong list. Mỗi khoá `reviewer_assurance_81` có giá trị chuỗi chuẩn hoá ra `DAT` (cùng `_chuan_hoa_81`, cùng `L7_MUC_DAT`) là **một vi phạm**, thông báo `L7 <đường dẫn JSON>: khai DAT mà không có khối $.assurance_81 cấp gốc có thuc_thi`. Không chấp nhận `thuc_thi` lồng bên trong, để mỗi hồ sơ chỉ có một chỗ khai §8.1.
- **Giá trị không phải chuỗi**, như mapping hay list, ở khoá `reviewer_assurance_81` lồng ⇒ không áp (giống r1 với `CHUA_DAT`). Ghi vào ghi chú để người đọc thấy.
- **`MIEN_TRU_L7` giữ nguyên** tên, băm và cơ chế. Không thêm tên mới.

## 3. Tiêu chí xong
- Ca cho mỗi nhánh:
  - có khối cấp gốc `DAT` đủ ba khoá ⇒ ĐẠT, dù có `reviewer_assurance_81: DAT` lồng bên trong; ghi chú nêu đường dẫn;
  - có khối cấp gốc `CHUA_DAT` và một khoá lồng `DAT` ⇒ ĐẠT kèm ghi chú;
  - không có khối cấp gốc, khoá lồng `DAT` trong mapping ⇒ ĐỎ, thông báo nêu đúng đường dẫn;
  - như trên, nhưng khoá lồng nằm trong phần tử của một list ⇒ ĐỎ;
  - không có khối cấp gốc, khoá lồng là `CHUA_DAT` hoặc không phải chuỗi ⇒ ĐẠT;
  - các biến thể chuẩn hoá (`Dat`, ` DAT `, `ĐẠT`) ở khoá lồng;
  - các ca L7 r1 hiện có vẫn đạt.
- Mỗi chốt mới có một đột biến riêng, bị giết đúng ca đích:
  - gỡ phép duyệt độ sâu;
  - gỡ phép duyệt list;
  - đảo quy tắc "khối cấp gốc là nguồn duy nhất".
- Cổng chạy trên cây thật (`c11` hiện có) vẫn ĐẠT trên base đã chứa `land-81-ha-cap` r2.
- `ops/land_evidence_nguon_test.py` N/N, `TONG: DAT`.
- Review chéo Codex qua `launcher.py run` trên đúng head, tới khi 0 P0–P3.

## 4. Trần
- Kích thước: ≤ 2 tệp / ≤ 250 dòng thêm.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- **Lời khai bằng văn xuôi** (ví dụ "§8.1 reviewer: … cross_approved" trong một chuỗi) không đọc được bằng máy, nên L7 r2 không bắt. Hồ sơ duy nhất đo được mang dạng ấy là `pr896-claude-md-bai-hoc-c-tro-nguon`, và nó được `land-81-ha-cap` r2 xử lý. Nói thẳng ra đây để không ai đọc L7 r2 thành "đã chặn mọi lời khai §8.1 vượt phép đo".
- Không sửa hồ sơ land nào.
- Không đối chiếu nội dung `run.json`. Giống r1, L7 chỉ đo rằng lời khai `measured` có tồn tại và trỏ tới nguồn có thật.
