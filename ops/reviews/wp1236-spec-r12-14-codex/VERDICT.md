Review đặc tả wp1236 r12 — vòng 14: **changes_requested** (1 P2, 0 P3 mới).

SHA đặc tả: `02d60e53c80a7d7145930abadd516fba8d9e736d2a7bf5dc355114352e4abbe4`; đã khớp byte với Git blob.
Reviewed SHA: `03bff7fefb27ed2ea03c5235b03fd21f261b37aa`.
Tree: `75d7a8971d57b9f6e81bd2a9d96e931ee635dc91`.
Provider/surface/transport: `openai_codex / codex_cli / machine`; run `9b150ce7dd674d9c9680c7f15c467159`.
Model/effort phục vụ: `KHONG_DO_DUOC`. Review offline độc lập, chỉ đọc repository; scratch ở `work/`.

**AE01 — P2 — `test-thieu-chot`** tại `ops/specs/wp1236-r12.md:420–428` (đối chiếu regex dòng 125).
AD01 đã sửa casefold nhưng còn thiếu ngữ nghĩa assertion `$` trong oracle bảng ASCII bắt buộc. LF cuối chuỗi không thuộc lớp dấu phân cách, nhưng `token("skipped\n") == "skipped"` và `kiem_ho_so({"gate_output":"skipped\n"}) == []`: `$` khớp trước LF cuối. Quét 128 ASCII × 3 ngữ cảnh qua hàm lá và consumer cho 383 khớp, đúng một lệch này. Đối chứng LF đầu, LF còn payload và CR đều bị từ chối. Đây là mâu thuẫn của ca bắt buộc luật 4/8, không phải mutant ngoài bảng để hạ P3.

Sửa oracle theo toàn biểu thức/ngữ cảnh sau tiền xử lý, gồm `$`, lookahead và tập TOKEN. Giữ regex sản phẩm; ghi đúng biên LF cuối/đầu/giữa. Bằng chứng: `ascii_token_sweep.json`, `contract_probes.json`; lệnh `python3 -B ../work/probe_contract.py`, rc 0.

| Finding vòng 13 | Nhãn | Bằng chứng vòng 14 |
|---|---|---|
| AD01 | VÁ HỜ / VA_MOT_PHAN | Casefold đúng; AE01 còn mâu thuẫn LF cuối. |
| AD02 | ĐÃ VÁ THẬT | 3 ca lazy qua parser/consumer đều passed/[]; greedy phản chứng đỏ. Cs qua JSON escape hợp lệ được nhận; 28 category hợp lệ của readback và các đối chứng splitlines đã đo. |
| AD03 | ĐÃ VÁ THẬT | nang_tran neo r12 hiện hành; 1985 là đo, 1950–2080 là ước, 2100 giữ mức đã duyệt r11 và chờ băm r12. |

Hội tụ 13→14: **2/3**. Giữ alias `test-thieu-chot` ↔ `nghiem-thu-khong-co-lap-chot-dich`, đếm một lớp. Các lớp đã đóng được bảo toàn bằng đối chiếu delta; không tái mở. S01/Q01/P01 còn VÁ MỘT PHẦN ở lịch sử mã; S02/Q02/P03 CHƯA VÁ, chưa có code/waiver exact head mới trong đầu vào. Không coi giảm acceptance hoặc đổi scope là vá.

Luật 8 không biến ngôn ngữ chuỗi thành hữu hạn: `*`, `+` vẫn cho độ dài không chặn. Hợp đồng hiện hành đóng **miền nghiệm thu** bằng luật 9. Đã kiểm đủ sáu nhóm văn bản tự do, gồm D2b; không bỏ sót `.*`, `[^\]]*`, `[^/]+` hay assertion của token.

- A: hai lần `quet_dot_bien.py sinh` trên module `0d81487`, rc 0/0, cùng 780 đột biến/24 toán tử; manifest byte-equal, SHA-256 `e0143c6018d6a06b6ae98bc39fa2cc57bb7f7edbbed57cfb5dd30b089c99643f`.
- B: 201 ID duy nhất = 127+14+11+15+19+15, khớp băm ghim. Ledger lịch sử 186 có 172 GIET, 7 tương đương, 5 không áp dụng, 2 ngoài bảng; phải kiểm lại trên head r12. Trên bản chiếu ASCII, 53/201 neo cũ mất, không đồng nghĩa CHOT_DA_BO.
- 15 cặp `r11_*`: 9 tương đương theo ASCII mới; 4 reason vẫn phân biệt; token_single_ws và event_casefold vẫn phải GIET. Mỗi ID có bằng chứng tại `pairs11_projection.json`.
- Thứ tự B→A→ngoài là duy nhất; 65 source mutant giao A/B trên r11. Hai P3 lịch sử đã ở B phải xét luật 5/9 trên head mới. Lỗi hành vi mã thực vẫn theo mức thật; luật 9 không cấp quyền hạ chúng xuống P3.
- Base `8048551`: 66 tệp giữ **47 passed / 10 failed / 9 not_measured**, delta kết quả/parser = 0. 170 hồ sơ giữ **25 cutover / 56 đỏ / 39 đạt / 50 không lời khai**, delta = 0; 94 landed cả hai phía.
- Quét URL: 2.508 occurrence thô, chỉ một template mã `{PR_GHI_SO}` ngoài lớp; 3.624 JSON đọc được, 1.942 occurrence sau decode, 0 ngoài lớp. Không hồ sơ/readback thật nào bị đổi bởi lớp URL mới.
- 30 ca sàn, 9 luật, 50 mutant kế thừa m1–m50; 125 ô giữ băm. Numstat r11: 1+343+1641=1985; chưa đo kích thước thi công r12.

Các phép đo dùng bản chiếu r11 chỉ thay regex theo r12, không phải mã thi công r12. Chưa chạy suite r12, `do/HOAN_TAT`, Windows, CI, full selftest/release hoặc Ruff; không gọi mạng. Lỗi dò tên ref và fixture nháp được tách trong JSON, không tính là lỗi sản phẩm hay pass. Cơ chế quyền thực tế là workspace-write; checkout được giữ chỉ đọc theo chỉ thị. Launcher cần chốt rc/hash output sau run; verdict không tự tạo approval/waiver/merge authorization.

Validator và snapshot cuối được ghi trong `VERDICT.json` / `kiem_verdict.txt`.

KET_LUAN: changes_requested
