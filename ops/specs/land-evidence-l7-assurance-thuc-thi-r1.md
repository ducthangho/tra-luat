# Đặc tả packet `land-evidence-l7` r1 — `land_evidence_nguon.py` từ chối khai §8.1 ĐẠT khi thiếu phép đo thực thi

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet | `land-evidence-l7` (mission #748), revision 1, generation 1 |
| review_class | `sensitive` (cổng nghiệm thu hồ sơ land) |
| write set | `ops/land_evidence_nguon.py`, `ops/land_evidence_nguon_test.py` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `f577ab5`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, read-only, neo đúng head |

## 1. Vì sao
Connector Codex P1 trên PR #934 (review comment `4372912640`) bắt được một lỗi trong hồ sơ `pr932-wp748-r26`. Hồ sơ ấy khai `assurance_81.reviewer_assurance_81: DAT`, nhưng biên nhận chỉ đo model, không đo effort và sandbox mode như §8.1/§8.2 đòi. Connector đề xuất thêm một regression check để chặn đúng lớp lỗi này.

Từ r27 (PR #957), `launcher.py run` đã ghi được `effort_phuc_vu` và `sandbox_trang_thai`, nên đòi đo cả ba giờ đã khả thi.

Đo trên `f577ab5` (27-10-2026): trong 74 hồ sơ, 11 hồ sơ có khối `assurance_81`. **3 hồ sơ khai `DAT` mà không có khối đo thực thi:** `pr924-wp923`, `pr931-wp835` (đang `landed: true`), `pr950-wp834`.

## 2. Luật mới L7
- **Khi nào áp.** `assurance_81` là mapping có `reviewer_assurance_81`, và giá trị ấy, sau khi chuẩn hoá (bỏ khoảng trắng hai đầu, viết hoa, thay khoảng trắng bằng `_`), bằng `DAT`.
- **Đòi hỏi.** Phải có `assurance_81.thuc_thi` là mapping, chứa đủ ba khoá `model`, `effort`, `sandbox_mode`. Mỗi khoá là chuỗi bắt đầu bằng lời khai đo `measured` (cùng `RE_KHAI_DO` với L1). Nhờ vậy L1 tự đòi mỗi lời khai có token nguồn phân giải được.
- **Vi phạm ⇒ ĐỎ**, với thông báo `L7 $.assurance_81…` nêu đúng khoá thiếu hoặc khoá không phải `measured`.
- **`CHUA_DAT` hay giá trị khác ⇒ L7 không đòi gì.** L7 chỉ chặn chiều khai mạnh hơn phép đo.
- **Miễn trừ cutover L7.** Hằng `MIEN_TRU_L7 = {tên: sha256 byte}` chỉ gồm 3 hồ sơ nêu ở §1. Cơ chế giống L5:
  - băm khớp ⇒ bỏ qua L7 cho hồ sơ ấy, kèm ghi chú;
  - băm lệch ⇒ mất miễn trừ, L7 kiểm đủ;
  - bản kỳ vọng được chép riêng trong test, nên thêm tên vào danh sách sẽ làm test ĐỎ.
- **Nợ có tên.** Ba hồ sơ được miễn trừ là `NO-L7-3-HO-SO-KHAI-DAT-THIEU-DO`. Hạ chúng về `CHUA_DAT` hay bổ sung phép đo là việc ghi sổ riêng, chủ kho quyết. Packet này không sửa hồ sơ nào.

## 3. Tiêu chí xong
- Ca cho mỗi nhánh:
  - `DAT` đủ ba khoá `measured` có nguồn ⇒ ĐẠT;
  - thiếu `thuc_thi` ⇒ ĐỎ;
  - thiếu từng khoá trong ba khoá ⇒ ĐỎ;
  - một khoá là `not_measured` ⇒ ĐỎ;
  - `CHUA_DAT` không có `thuc_thi` ⇒ ĐẠT;
  - các biến thể chuẩn hoá (`Dat`, ` DAT `, `CHUA DAT`);
  - miễn trừ: băm khớp ⇒ bỏ qua, băm lệch ⇒ kiểm.
- Mỗi chốt có một đột biến riêng, bị giết đúng ca đích.
- Cổng chạy trên cây thật (`c11` hiện có) vẫn ĐẠT, nhờ 3 hồ sơ được miễn trừ.
- Hồ sơ `pr932-wp748-r26` (`CHUA_DAT`) vẫn ĐẠT.
- `ops/land_evidence_nguon_test.py` N/N, `TONG: DAT`.
- Review chéo Codex qua `launcher.py run` trên đúng head, tới khi 0 P0–P3.

## 4. Trần
- Kích thước: ≤ 2 tệp / ≤ 250 dòng thêm.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- Không đọc `run.json` hay biên nhận để đối chiếu nội dung lời khai. Giống L1, L7 chỉ đo rằng lời khai có tồn tại và trỏ tới nguồn có thật.
- Không sửa hồ sơ land nào.
