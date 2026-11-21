**changes_requested — còn 1 P2 và 1 P3, thuộc 2 lớp mở.** Đây là review ĐẶC TẢ r11 vòng 9, class `sensitive`; không phải approval mã. Mỗi P3 vẫn cần đóng có bằng chứng hoặc chủ kho miễn trên exact SHA.

`reviewed_sha: 9f7fd71c7cd402603db7a319f0d3e3041d595437`  
`reviewed_tree: 5e25a58665ea37dacf85b5453d5c33e2c1a6b3a0`  
`spec_sha256: 8a77e52341ba6f3a9785d10f938cb91c11e7223f69ed1154ed4bb1ee5adfd887`

SPEC khớp byte blob `HEAD:ops/specs/wp1236-r11.md`. Mã tham chiếu: `5a1bf33831bb4e3a227cfb25843cef8a922c634b`, tree `19fe7bd12a8a2e038a11ec230efb706be5756caa`. Inventory được đọc tại `b6c0063ba05fafea6629b1b0af6a607897254a91`; băm coverage khớp băm đặc tả. Snapshot đầu/cuối: 17.502 tệp tracked/untracked/ignored, delta byte 0; HEAD/tree và index giữ nguyên. Mọi tệp đo nằm trong `work/`. Hai snapshot không chứng minh lịch sử ghi rồi hoàn nguyên.

**Đối chiếu lớp ở mức đặc tả (§8.3).** JSON giữ đủ 18 dòng lịch sử, cả alias và nguồn SHA.

| Lớp/biểu hiện kế thừa | Nhãn | Căn cứ |
|---|---|---|
| `test-thieu-chot` = `nghiem-thu-khong-co-lap-chot-dich`, N01 | `VA_MOT_PHAN` | Luật 6 thêm các họ còn thiếu và seam, nhưng Z01 còn mở. Cắt miền không tính là đã vá. |
| Cùng lớp, N02 | `DA_VA_THAT` **ở mức đặc tả** | Luật 5 cho nhãn kết thúc tương đương, kèm chứng minh trên head mới; hai phép tương đương đã kiểm dưới đây. Không tự sửa/approve ledger mã8. |
| `hop-dong-dau-vao-dau-ra-chua-chot`, N03 | `DA_VA_THAT` **ở mức đặc tả** | Luật 7 đủ để thi công sửa output, số thực đo và kiểm hai nền. |
| `mo-ta-duong-dan-lech-hop-dong`, L03 | `DA_VA_THAT` | Đã đóng ở mã8; đo lại plain/`./` đạt, `..`/symlink/absolute bị chặn, docstring đúng. |
| `so-do-khong-cung-pham-vi-nguon` | `VA_MOT_PHAN` — tái mở | Số 127 từng đúng ở spec8; r11 đã nhận thêm 25 ID nhưng tổng hiện hành chưa đổi (Z02). |

Các lớp đã đóng khác được giữ nguyên. Đối chiếu 23 đoạn hợp đồng cũ: 22 đoạn nguyên văn; đoạn thay đổi còn lại là `nang_tran`, vẫn đủ bốn trường và ghi **CHỜ E2**. Không mở lại các số corpus hoặc chốt cổng đã đóng.

**Z01 · P2 · `nghiem-thu-khong-co-lap-chot-dich` — luật 6 chưa đóng được miền nghiệm thu.** Vị trí `SPEC.md:355–377`, đọc cùng luật 1/4/5.

Đã quét toàn bộ các phép so và đối chiếu họ lịch sử trước khi gộp những biểu hiện sau thành một finding:

- **Hàng và phân hạng chưa khớp.** Tự liệt kê từ mã trước khi đọc inventory: 72 `Compare` trong hàm, cộng 1 guard `__name__` ở mức module. Inventory chọn 61, coverage chọn 45. Trong 16 nút inventory bỏ khỏi coverage có **hai phép so chuỗi** `d == ''` và `'\r' in d`; câu “16 nút còn lại so số/bool/cấu trúc” sai. Phản chứng đổi `d == ''` thành `d.strip() == ''`: dòng chỉ có SPACE làm HEAD báo `dong_la`, mutant `passed`, consumer từ vi phạm thành `[]`. Đây là ngữ pháp bắt buộc, nhưng (b) lại xếp điểm ngoài 45 hàng thành P3; chưa có ưu tiên rõ cho `ngu_phap` và luật 1/4/5.
- **Quy tắc ô chưa cho cùng một tập.** `labels` so bằng chuỗi `join` nhưng mang nghĩa dãy: chọn loại chuỗi có H5 mà thiếu H7–H9; chọn dãy có H7–H9 nhưng quy tắc không nêu H5/H10. Khoá qua `_chuan` cố ý nhận biến đổi hoa/thường/khoảng trắng; không có oracle âm như nhau cho mọi hàng. OS viết hoa/cách/NFKC bị parser chặn bằng `dong_mien` trước phép so OS, nên không được lấy tín dụng khóa phép so ấy. Cần ghi miền tới được và oracle riêng từng ô.
- **Số ô hữu hạn chưa giới hạn các biến thể trong ô.** Luật 6 chỉ đòi ≥1 mẫu/ô, nhưng (a) tiếp tục bắt mọi mutant khác nghĩa cùng họ. Với hàng `event`, các mẫu `PUSH`, ` push`, `push `, `ｐｕｓｈ`, `x-push`, `push-x` đều cho cùng kết quả trên HEAD và mutant `.lstrip('\t')`. Riêng `\tpush`: HEAD từ chối `khong_phai_run_land`, mutant nhận `passed`; consumer cũng từ vi phạm thành `[]`. Cả hai mẫu SPACE/TAB đều thuộc cách đầu theo cách hiểu khoảng trắng; nếu H2 chỉ là SPACE thì đặc tả chưa nói. Mutant qua **42/42 ca mã8** sau sửa một thiếu dependency của cây scratch. Đây là phản chứng cho biên ô, không phải khẳng định đã có bộ ca r11.
- **H1–H10 không bao mọi cơ chế P2 lịch sử.** Đã ánh xạ 50 witness: 20 P2 + 5 P3 lượt6, 14 biểu hiện M01 lượt7, 11 biểu hiện N01 lượt8. Cả 11 lượt8 có họ phù hợp. Nhưng kiểu `True/1`, ngữ pháp, đệ quy metadata, URL cardinality/dedup, consumer argument và output/fallback CLI không đều có hàng/cột tương ứng. Luật 1/4/5 vẫn giữ nghĩa vụ ấy; cần nói rõ chúng thắng (b) hay phần nào được chuyển scope có authority. Stat/is_absolute cũng là lời gọi, cần route ledger rõ dù seam đã được yêu cầu.

**Cách sửa chung:** đóng băng bảng nghĩa có ID hàng/ô ổn định, nguồn và bên biến đổi, ngữ cảnh, tập mẫu/toán tử cụ thể, kỳ vọng dương/âm và consumer. Chốt tập hữu hạn nào là nghĩa vụ P2, cách xử biến thể khác trong cùng họ, cùng ưu tiên `ngu_phap`/hồi quy trước (a)/(b). Đổi biểu diễn mã không tự xoá nghĩa vụ. Hai bên phải dựng được cùng tập ô và cùng phân hạng từ hợp đồng ấy; không tiếp tục vá từng ví dụ.

Bằng chứng: [inventory_audit.json](inventory_audit.json), [all_comparison_domains.json](all_comparison_domains.json), [cell_witnesses.json](cell_witnesses.json), [historical_family_mapping.json](historical_family_mapping.json), [tab_mutant_suite.json](tab_mutant_suite.json).

**Z02 · P3 · `so-do-khong-cung-pham-vi-nguon` — tổng kho hồi quy hiện hành sai phạm vi.** `SPEC.md:463–465` vẫn ghi 127 cặp; luật 5 đòi cộng dồn. Kho ghim tại `b6c0063` có **152 dòng/152 ID duy nhất = 127 + 14 + 11**, giữ đủ ID lượt6. Cần ghi 127 là kho lịch sử lượt6 và 152 là tổng hiện hành, kèm con trỏ/băm và phép kiểm hiệu tập. Không có miễn trừ cho 25 ID sau. [counts.json](counts.json).

Các phần còn lại đã kiểm:

- **Luật 7:** producer mã8 nhánh `nt` rc0 nhưng `chay_moi` trả 1. Đưa khai báo bỏ qua lên trước và giữ đúng bốn dòng theo luật7 thì consumer trả 0 ở cả hai chế độ. Ca đỏ, mutant sống, tên POSIX lạ và mẫu số 0 đều đỏ. Mẫu `999/999` giả vẫn qua regex; vì vậy câu **mẫu số là số thực đo** phải kiểm riêng bằng danh sách dispatch, không suy từ consumer pass. Luật7 đã đòi tính chất này. [output_contract.json](output_contract.json).
- **m65/m79:** mock filesystem giữ nguyên logic sản phẩm: stat `OSError` cho HEAD rc2 đúng prefix, mutant ném lỗi; đối chứng rc0. Đường tuyệt đối với `PurePosixPath` thật cho HEAD `None`, mutant nhận tệp; đường tương đối cả hai nhận. Yêu cầu seam đủ để thi công, không cần đặc tả thêm framework mock. Đây không phải chạy Windows thật. [portable_seams.json](portable_seams.json).
- **Luật 5 và `tep_danh_gia`:** dạng mới không miễn hồi quy nếu vẫn giữ ID, replacement cùng nghĩa và chứng minh tương đương trên head mới. Với regex hiện tại, tìm trái nhất bắt đầu ở đầu dải ký tự được phép; tính tham lam lấy hậu tố hợp lệ cuối cùng trong dải. Phần còn lại sau một match không thể chứa hậu tố hợp lệ khác, nên quy nạp qua `findall` cho cùng spans khi thêm/bỏ lookbehind. **22.197 mẫu, delta 0** chỉ bổ trợ chứng minh đó. Hai Pattern của skipped có mẫu khác nhau; `is` và `==` chọn đúng cùng nhánh trong miền binding này. Không thay luật cổng hoặc thêm ranh giới bên phải. [equivalence.json](equivalence.json).
- **Số và trần:** 30 ca sàn, m1–m50 đủ, 7 luật. Numstat `010046f…→5a1bf33` là 3 tệp, `1+343+1248=1592` dòng thêm. Cộng 300–450 ra **1892–2042**, phù hợp ước ~1900–2050; trần 2100 vẫn chờ duyệt. Dòng `thay_the` “giữ1400” là phương án hẹp cũ, không phải trần hiện hành1700; nên cập nhật nếu dùng. Không mở lại lớp authority đã đóng chỉ vì đề nghị E2 đang chờ.

Hội tụ `vong8_sang_9 = 1/2` ở **mức đặc tả**, dùng hai lớp còn mở sau mã8, không đếm đôi alias. Luật7 đóng thiếu hợp đồng output; lớp nghiệm thu còn Z01. L03 đã đóng trước vòng9 nên không lấy thêm tín dụng. JSON cũng ghi hợp thô hai danh sách spec8/mã8 là 2/3 và giải thích vì sao không dùng tỷ lệ ấy. Z02 tái mở, không vào tử số. Lịch sử mã7→8 = 0/2 và điều kiện lớp lặp ≥3 giữ nguyên; không reset ngân sách.

Reviewer `openai_codex / codex_cli / machine`, run `298fef3034494c03a87654a39ff885c8`, context độc lập. Model/effort phục vụ: `KHONG_DO_DUOC`; không suy từ actor hoặc cấu hình yêu cầu. Python 3.13.18 trên Linux, sandbox `workspace-write`, ghi thực tế chỉ trong `work/`. Các script đối chứng trả rc0 với bằng chứng dương; hai lỗi setup đã được giữ và sửa trong scratch, không lấy tín dụng. Không chạy Windows thật, remote CI, mạng/GitHub, Ruff, full release hoặc nghiệm thu mã r11.

Schema được kiểm bằng `kiem_verdict_lop.py --vong 9`; kết quả ở [kiem_verdict.txt](kiem_verdict.txt). Schema hợp lệ không chứng minh tự động nội dung review hoặc authority.

KET_LUAN: changes_requested
