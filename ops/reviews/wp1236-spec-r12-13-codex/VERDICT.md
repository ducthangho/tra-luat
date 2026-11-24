Review đặc tả wp1236 r12 bản sửa 1 — vòng 13, call 14/14 (cuối).

Reviewed SHA: `138ecd74ef5b65999d212a73f53ec4956caf4958`  
Tree: `9135390903cba1de48737b13eb5694529bff9952`  
Spec SHA-256: `8372a138e5121f108e0547cf86d3a6289c5ddeb5e69ce7b172a062eb9b9f9f39`  
Provider/surface/transport: `openai_codex / codex_cli / machine`; model và effort phục vụ: `KHONG_DO_DUOC`. Review offline, checkout chỉ đọc.

Còn **2 P2, 1 P3**, thuộc ba lớp đã có:

| ID | Mức | Slug | Vấn đề |
|---|---|---|---|
| AD01 | P2 | test-thieu-chot | Luật 8 buộc Unicode ngoài ASCII là ca âm, nhưng API `token` còn `casefold()`: `paſſed` thành `passed`, qua cả consumer. Luật 9 vẫn giữ bảng này bắt buộc. |
| AD02 | P2 | hop-dong-dau-vao-dau-ra-chua-chot | Regex lazy chọn delimiter sớm nhất khả thi, không phải delimiter cuối như dòng 428. Hai suffix hợp lệ cho kết quả consumer khác nhau. Lý do loại `Cs` cũng chưa phân biệt raw UTF-8 với JSON escape. |
| AD03 | P3 | so-do-khong-cung-pham-vi-nguon | `nang_tran.ai_nang` dòng 559 vẫn ghi chờ `spec_hash r11`, trong khi căn cứ và băm đang xét thuộc r12. |

Đã đo:

- Bộ quét đúng băm, Python 3.13.18; hai lần `sinh` với hash seed khác nhau: **780 mutant, 24 toán tử, byte-equal**. SHA-256 manifest: `e0143c6018d6a06b6ae98bc39fa2cc57bb7f7edbbed57cfb5dd30b089c99643f`. A hữu hạn cho một source; ngôn ngữ grammar vẫn không hữu hạn về độ dài. R12 mới đã bỏ lời hứa bắt mọi mutant.
- Kho **201 ID = 186 + 15**, đúng băm và tập ID. Chiếu từng `r11_*`: **9 tương đương; 4 reason còn phân biệt; 2 nghĩa vụ khác còn phải GIET**. Mất neo không là `CHOT_DA_BO`. Không nhận lại ledger cũ như pass cho head mới.
- Base `8048551a9b1eb886c126d2a1a4df0f95fb285964`: **66/66 tệp, 170/170 hồ sơ không đổi kết quả**; 47 passed / 10 failed / 9 not_measured; 25 miễn cutover / 56 ĐỎ / 39 ĐẠT / 50 không lời khai; 94 landed, lệch 0.
- **0 URL ngoài lớp mới** trong 2.504 lượt trích từ hồ sơ và 1.797 lượt trích sau giải mã 2.812 JSON readback. Quét cả script thấy một URL mẫu chứa `{PR_GHI_SO}`; đó không phải hồ sơ/readback thật.
- Numstat mã r11: **1985** dòng thêm, ba tệp; đề nghị **2100**, dự toán r12 **1950–2080** chưa phải số đo. Tập 125 ô giữ đúng băm; các khối hợp đồng cũ ngoài delta không đổi.

Luật 9 đặt thứ tự B → A → ngoài cho **đột biến kiểm test**; nó không hạ mức lỗi hành vi thật của candidate. P3 ngoài bảng vẫn phải đóng hoặc được chủ kho miễn đúng SHA. Hai ID P3 lịch sử của S02 có trong B201: nghĩa vụ B của luật 9 phải được áp trên head r12, không tự lấy nhãn lịch sử làm ngoại lệ.

Đối chiếu vòng 12: **AC02 ĐÃ VÁ THẬT ở mức đặc tả**; AC01, AC03, AC04 **VÁ HỜ / VA_MOT_PHAN**. Hai slug `test-thieu-chot` và `nghiem-thu-khong-co-lap-chot-dich` nối cùng lớp, giữ lịch sử và không đếm hai lần. P02/AA01 đã đóng được giữ; S02 chưa có bằng chứng đóng/waiver code mới. Hội tụ **12→13 = 0/3**; không có lớp mới hoặc lớp đã đóng bị tái mở. Thu hẹp acceptance không được tính là đã vá theo §8.3.

Phép đo là r11 cộng projection riêng cho delta regex, **không phải nghiệm thu implementation r12**. `do`/`HOAN_TAT` cho r12, worker/land gates, Ruff, Windows và GitHub readback: `not_run`. Không gọi mạng, không commit/push, không cấp lease/waiver. Hết call 14/14; chuyển kết quả về Review Rescue Checkpoint, không tự mở vòng tiếp theo.

Chi tiết từng finding, nhãn mọi lớp lịch sử, command/rc, giới hạn và hiện vật: [VERDICT.json](VERDICT.json). Probes: [contract_probes.json](contract_probes.json), [pairs11_projection.json](pairs11_projection.json), [manifest_comparison.json](manifest_comparison.json), [base_summary.json](base_summary.json).

Validator: `HOP_LE (§8.3): 3 finding, 3 lop` (rc 0), lưu [kiem_verdict.txt](kiem_verdict.txt). Snapshot đầu/cuối cùng HEAD/tree, diff/index/untracked rỗng; chỉ `.codex/` rỗng có sẵn.

KET_LUAN: changes_requested
