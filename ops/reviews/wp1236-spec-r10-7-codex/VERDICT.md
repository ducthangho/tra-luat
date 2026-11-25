Review ĐẶC TẢ wp1236 r10 bản sửa 2 — vòng 7 — `sensitive`.

**Kết quả: changes_requested — 1 P2, 1 lớp đặc tả còn mở**, giữ slug `nghiem-thu-khong-co-lap-chot-dich` (W01 → X01).

Neo review: `33b6803676b12fd069976dedb79f043a268c29c3`; tree `0f8f559e57d7ced781b2addaed83cad14cb497cb`. Đặc tả SHA-256 `d386636003250664b98b4657283c63bdde9f25757e16e342df4bddc4f7eb0779` khớp cả tệp đầu vào và blob Git.

**X01 — Bộ chạy vẫn làm mất mẫu số trước khi báo hoàn tất.** Manifest 800 ID sau khi bỏ `src` theo định dạng bàn giao được SPEC:338 cho phép trả `rc=0`, `TONG 0`, `HOAN_TAT`. Khi chỉ tái cấp một nguồn, bộ chạy trả `GIET 1`, `SONG_SACH 0`, `HOAN_TAT`, còn 799 ID biến mất. Nguyên nhân ở `quet_dot_bien.py:278`: lọc dòng trước validation và đối chiếu inventory. Các phép đo chỉ dùng nguồn/test thật, không soạn mã tấn công. Bằng chứng: [runner_checks.json](runner_checks.json), [partial_manifest_probe.json](partial_manifest_probe.json).

Cùng lớp còn giới hạn tái lập: Python 3.13 áp 127/127 cặp; Python 3.12 của CI chỉ áp 125/127 trên **cùng nguồn**, do `ast.unparse` đổi cách quote f-string. 800 ID sinh vẫn như nhau nhưng cả 800 hash nguồn khác. Đặc tả chưa ghim runtime; neo chỉ có bốn hash tệp. Baseline chỉ lưu `SONG`, không lưu tập ca và marker hoàn tất child; `GIET` bỏ nội dung assertion. Những hướng sửa test để báo rc=3 giả hoặc thoát 0 sớm chỉ được mô tả bằng lời, không chạy. Bằng chứng: [python_version_audit.json](python_version_audit.json), [normalization_versions.json](normalization_versions.json), mã bộ chạy :242–247,265–266,282–299.

Đề nghị sửa chung luật 3/5: phân biệt manifest bàn giao với manifest thực thi; thiếu nguồn phải bị chặn hoặc tái dựng đủ rồi kiểm hash. Đối chiếu toàn bộ ID, kết quả và ledger trước `HOAN_TAT`; ghim runtime chuẩn hoá; giữ bằng chứng baseline/ca/terminal/assertion. Chỉ kiểm tổng lớn hơn 0 không đủ. Không quay lại chốt tự bảo vệ nguyên văn sản phẩm kiểu A14-S0.

Những phần đã đo đạt:

- Sinh hai lần cùng 800 dòng/24 mã; hash nguồn và hash manifest đầy đủ khớp pilot. Docstring `a2` và `i5` đã sửa đúng. Các toán tử là phép thay cú pháp hữu hạn; không chứng minh bao mọi ngữ nghĩa.
- Tái dựng 127/127 bản gốc theo dạng chuẩn; đổi định dạng/chú thích vẫn 127/127. Neo trung bình 1,19685 dòng, tối đa 6. Bỏ đệ quy chọn lọc, truthiness của head, đổi nhãn bộ sinh, hoán vị qua try và một số phép mở rộng token/regex không được manifest sinh đúng phép thay; chúng vẫn nằm trong kho hồi quy. Chi tiết từng mã và giới hạn ở JSON.
- Pilot chạy lại **99/99 khớp**: 55 GIET, 34 SONG, 10 VO_CAN, 0 LOI_CHAY; đủ **25/25** survivor khác nghĩa và **9/9** tương đương, có `rc=0` và `HOAN_TAT`. Chọn toàn bộ survivor lịch sử, toàn bộ VO_CAN, kill theo toán tử và 34 ca đích; không phải mẫu thống kê. Không chạy lại cả 927.
- Baseline native **36/36**; **55/55** kill chạy riêng trên test gốc, không cache YAML, đều `rc=3` và `DO:<đúng ca>`. Không vì X01 mà phủ nhận các kết quả này.
- Resume đã sửa: nguồn gốc lành dưới ID từng bị giết được chạy lại thành SONG, đúng hash. Test vắng bị từ chối bằng rc=2.
- V02 giữ đóng: 30 ca sàn, năm luật, 50 mutant đánh số là sàn; pilot 800+127=927. Census 66=47/10/9 và 170=25/56/39/50 trùng byte bản ghim. Numstat r9 là 1324 dòng trên ba tệp.

Luật 4 định tuyến đúng: A qua helper và `kiem_ho_so(head=None)`; head khác None qua `kiem_mien` ở A và D2b ở C; L8 ở B. Adapter test B/C vẫn phải được chứng minh khi có mã mới. Luật 5 đã thêm ledger hữu ích: đổi tên biến cục bộ làm hai cặp KHONG_AP_DUNG, không xoá nghĩa vụ thay thế. Danh sách tương đương của head cũ không tự chuyển sang head mới; lỗi vô can không cấp tín dụng luật 1/5. Đây là nghĩa vụ review ngữ nghĩa, chưa được runner cưỡng chế đủ.

Đối chiếu lịch sử đủ **15 slug** trong JSON: **12 DA_VA_THAT**, **3 VA_MOT_PHAN** gồm W01, alias `test-thieu-chot`, và `mo-ta-duong-dan-lech-hop-dong` (L03). L03 vẫn còn ở mã r9: `./tệp` hợp lệ nhưng docstring khai cấm dấu chấm; đặc tả r10 đã chỉ thị sửa đúng. Hội tụ tính mọi lớp kế thừa, sau nối alias: **0/2**; chỉ riêng finding đặc tả là 0/1. Không xoá lịch sử lặp lớp từ ba vòng trở lên.

Trần **1700 chưa có phép đo chứng minh đủ**: nền 1324 đã đo, phần +200..+300 vẫn là ước lượng. 34 survivor kho đã nằm trong 153. Khối `nang_tran` giữ đúng nhãn đề nghị/CHỜ E2; phương án tách A1 chưa đạt luật 3 không tự có quyền land.

**Chưa kết luận E1:** các phép đo cho thấy tiến bộ thật và còn cách sửa hữu hạn về inventory/runtime/bằng chứng hoàn tất. Tuy nhiên chưa thể công nhận phương pháp hiện tại đóng lớp; cần checkpoint xét lại hợp đồng nghiệm thu theo §12, thay vì tiếp tục chỉ thêm ca cho từng survivor.

Reviewer: `openai_codex / codex_cli / machine`, run `ab68a4ed2ef640e19349764febeb41f2`; model/effort phục vụ `KHONG_DO_DUOC`. Không GitHub/mạng, không sửa hai checkout, không commit/push. Snapshot đầu/cuối của repo và ma_r9_git không có delta quan sát được. Chưa đo mã r10, Windows, CI hay release/land; verdict không cấp authority merge/land.

Schema: lệnh `kiem_verdict_lop.py VERDICT.json --vong 7` đã trả `HOP_LE` (rc=0); kết quả thực lưu ở [kiem_verdict.txt](kiem_verdict.txt). Bằng chứng chi tiết, lệnh, rc và giới hạn: [VERDICT.json](VERDICT.json).

KET_LUAN: changes_requested
