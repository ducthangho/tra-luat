# Review đặc tả wp1236 r12 — vòng 12

**changes_requested: 3 P2, 1 P3 thuộc 3 lớp.** Luật 8 thu hẹp alphabet, nhưng chưa đóng miền nghiệm thu và chưa cho một cách phân hạng duy nhất. Điều kiện approve `sensitive` chưa đạt.

- Đặc tả SHA-256: `0acd3f87046b97768bfaad83c2f42190ee0f9fb824dbc186b84e32ead605fc32`; đã đối chiếu byte với Git blob.
- Reviewed SHA: `04095f1c8707648e6a15498aae1ed53c7377cd15`, tree `4d8ff992043a43ce78ce945fd320ea113a4a4364`, nhánh `spec12`.
- Base dữ liệu: `8048551a9b1eb886c126d2a1a4df0f95fb285964`.
- Mã r11 tham chiếu: `0d814877e3acef6274a7f1c0e9a28531a24d0e65`. Bản chiếu ASCII chỉ phục vụ phép đo, không phải mã thi công hay patch đề nghị áp.
- Reviewer: `openai_codex / codex_cli / machine`; run `e8e4f968460e4b1b9ce0effc347bc09f`, session `01a1fdfb-4bcc-7862-851d-322cf5240d07`. Serving model/effort: `KHONG_DO_DUOC`. Không gọi mạng, không sửa repository.

| Finding | Mức / lớp | Kết quả kiểm |
|---|---|---|
| AC01 | P2 — `test-thieu-chot` | Luật 8 chưa vét cạn tập âm và chuỗi/ngữ cảnh; D2b còn `[^/]+` ngoài phân loại. |
| AC02 | P2 — `test-thieu-chot` | Luật 5/6 ưu tiên hồi quy và luật 8 hạ thu hẹp văn bản tự do thành P3 chưa có thứ tự giải quyết rõ. |
| AC03 | P2 — `hop-dong-dau-vao-dau-ra-chua-chot` | Mệnh đề tên job dừng ở delimiter đầu tiên trái regex; positive cho mọi general category không khả thi qua UTF-8 nghiêm. |
| AC04 | P3 — `so-do-khong-cung-pham-vi-nguon` | Mẫu số hiện hành vẫn 127/152 thay vì 201; căn cứ kích thước chưa cập nhật r12 và số đo 1985. |

AC01 — tại dòng 415–423, 193–196: `[a-z_]` và đột biến `[a-z_🙂]` cho cùng kết quả trên **138.623** vector âm/dương bắt buộc ở hàm lá, nhưng khác ở ký tự `U+1F642` thuộc So. Với fixture đã đồng bộ conclusion và trạng thái failed, bản chiếu gốc trả `not_measured/dong_la`, consumer có vi phạm; mutant trả `failed`, consumer không vi phạm. Một đại diện/category ở consumer không bảo đảm bắt mọi So khác. Đây là phản chứng về nghĩa vụ tối thiểu của đặc tả, không phải lời khai đã chạy suite r12.

Alphabet hữu hạn cũng không làm tập chuỗi hữu hạn: thay `[ \t]*` bằng `[ \t]{0,4096}` giữ kết quả các vector một ký tự và đối chứng ngắn, nhưng khác ở 4.097 space. Với tập test hữu hạn bất kỳ, có thể chọn giới hạn lớn hơn mọi prefix đã kiểm. D2b còn bốn vị trí `[^/]+` trong hai regex; phép `fullmatch` nhận thành phần mang emoji, zero-width, dấu tổ hợp và LF. Luật 8 chỉ nói *Module mới*, trong khi luật 4 vẫn áp cho C. Cần chốt một bảng vị trí/ngữ cảnh, vector hoặc họ đột biến hữu hạn; ghi giới hạn chứng minh, bao cả lượng từ, literal, assertion và D2b. `passed\n` hiện được regex token nhận vì `$`, nên oracle không thể chỉ suy từ lớp `[ \t]`.

AC02 — tại dòng 353–361, 404–409, 424–431: mất mỏ neo `\S` không đồng nghĩa chốt lý do đã bỏ. Bốn `r11_reason_*` vẫn phân biệt được trên bản ASCII: lý do bắt đầu bằng emoji, U+200B, U+0301, U+0001 được nhận, bản thu hẹp cùng nghĩa từ chối. Luật 8 gọi chúng P3; luật hồi quy trước đó vẫn đòi giết hoặc chứng minh tương đương/chốt đã bỏ. Cần một thứ tự ưu tiên và ledger di trú rõ ràng, không tự dùng `CHOT_DA_BO` hoặc tự miễn P3.

AC03 — tại dòng 89–92 và 424–429: dòng `JOB 1 alpha [bad] beta [ubuntu-latest] conclusion=success log_sha256=<64 số 0> -> passed: ok` khớp regex được ghi, với tên `alpha [bad] beta`, dù mệnh đề mới yêu cầu dừng ở ` [` đầu tiên. Ngoài ra, `U+D800` thuộc Cs không thể mã hoá UTF-8 nghiêm để làm positive qua `doc_danh_gia(bytes)`. Cần định nghĩa boundary cho từng dạng dòng và các tiền điều kiện chung decode/tách dòng/CR trước khi phân hạng nới–thu hẹp. Đây là phần r12 mới làm mất tính nhất quán; không mở lại biểu hiện CLI đã đóng.

AC04 — tại dòng 357, 404–405 và 513–531: kho hợp nhất tại `lease-moi` có **201 ID duy nhất = 127 + 14 + 11 + 15 + 19 + 15**. Kho trước lượt 11 có 186 ID; thêm 15 cặp lượt 11. SHA-256 kho hợp nhất: `191225cac93a5bec155cc9116911022b334df5d7b6f0bf6094632973b82af740`. Numstat mã r11 cuối: **1 + 343 + 1641 = 1985** dòng thêm, còn **115** so trần đề nghị 2100. Chưa có mã r12 để đo số sau viết lại; không kết luận đã vượt trần. Cần sửa các câu “đúng 127/152 hiện hành”, ghim kho 201 ID và cập nhật dự toán/authority theo revision r12.

Đối chiếu từng cặp lượt 11 có trong [pairs11_projection.json](pairs11_projection.json). Kết quả phân nhóm:

| ID / nhóm ID | Nghĩa trên bản ASCII |
|---|---|
| `r11_url_bmp_only`, `r11_url_no_zero_width`, `r11_url_no_combining`, `r11_url_no_control` | Neo cũ mất; loại cùng tập ký tự khỏi alphabet URL mới không đổi nghĩa — thay thế tương đương. |
| `r11_reason_bmp_only`, `r11_reason_no_zero_width`, `r11_reason_no_combining`, `r11_reason_no_control` | Neo cũ mất nhưng vẫn phân biệt; cần quyết định hồi quy/P3 nêu ở AC02. |
| `r11_word_ascii_first`, `r11_word_ascii_last` | Tương đương vì mọi ký tự conclusion mới đã ASCII. |
| `r11_token_single_ws` | Vẫn phân biệt; A2-2 có `  passed` để bắt bản `[ \t]?`. |
| `r11_token_no_nel`, `r11_run_no_arabic` | Tương đương: NEL và chữ số Arabic-Indic đã ngoài lớp. |
| `r11_consumer_ascii_conclusion` | Neo còn áp; tương đương vì parser chỉ sinh conclusion ASCII. |
| `r11_event_casefold` | Neo còn áp, vẫn phải bị ô `run.event:H1` bắt. |

Tổng **9 tương đương / 4 lý do còn phân biệt / 2 nghĩa vụ kiểm còn phân biệt**. Không khai đã giết trên mã r12 chưa tồn tại; không áp nguyên văn toàn regex cũ làm phục hồi ngữ pháp r11.

Phép đo an toàn trên base cho kết quả dương:

- **66/66** tệp giữ nguyên trạng thái và lý do: **47 passed / 10 failed / 9 not_measured**; kết quả parse cũng không đổi.
- **170/170** hồ sơ giữ nguyên danh sách vi phạm, kể cả trước cutover; phân rã **25 miễn cutover / 56 đỏ / 39 đạt / 50 không lời khai**; landed **94/94**.
- **119** lời khai có cùng token, trích tệp và URL trước/sau.
- Quét **8.902** tệp, **2.504** lượt URL: không có path ngoài `[A-Za-z0-9._~/%-]`. Giải mã độc lập **2.812** readback JSON, **1.797** lượt URL: cũng không có; không lỗi JSON.
- Bảng đóng băng vẫn đúng hash; **125/125** ô đạt cả tuyến lá và consumer trên bản chiếu r12. **30** ca sàn, **8** luật, **50** đột biến kế thừa giữ đúng số.

Kết quả này xác nhận chưa thấy hồi quy trên dữ liệu base; không thay thế việc sửa các mâu thuẫn trong hợp đồng mới. Các phép đo nằm ở `base_summary.json`, `lexical_base.json`, `decoded_readback_urls.json`, `cells125_projection.json`, `grammar_probes.json`; command và rc thật nằm trong `VERDICT.json`.

Bảng lớp §8.3 giữ nguyên slug:

- `test-thieu-chot` / alias đặc tả `nghiem-thu-khong-co-lap-chot-dich`: **VA_MOT_PHAN**. S01/P01/Q01 chỉ đóng một phần; đổi phạm vi hay phân hạng không được tính `DA_VA_THAT`.
- S02 ← Q02 ← P03, hai ID `r9b_event_tab` và `r9b_name_inner_spaces`: **CHUA_VA**; lời hẹn miễn ở spec:710 chưa là waiver neo exact code SHA. Theo dõi ở bảng kế thừa, không nhân đôi thành finding mới của đặc tả.
- P02/AA01 về nguồn seed: giữ **DA_VA_THAT** theo evidence mã10–11; r12 không làm hỏng bảng đóng băng.
- Hai lớp AC03/AC04 tái mở có phép đo vì delta r12; các lớp đã đóng khác giữ evidence lịch sử, không tự mở lại hay giả nhận đã chạy lại mã.

Hội tụ trên lớp còn mở kế thừa từ **mã lượt 11 → spec vòng 12: 0/1**. Riêng chuỗi **spec vòng 11 → spec vòng 12 là N/A**, vì verdict spec vòng 11 approve và U rỗng. Hai alias nghiệm thu chỉ tính một lớp; lịch sử và stop condition không reset. Lượt này là 13/14 theo assignment, không cấp quyền tự gọi vòng mới.

Ruff/full worker/land gates, suite mã r12, native Windows và GitHub readback: **not_run**, đúng phạm vi review đặc tả offline. Các lỗi setup ban đầu của script reviewer được khai riêng, đã sửa trong `work/` rồi chạy lại; không tính là lỗi sản phẩm. Validator §8.3: **HOP_LE**, rc 0, lưu `kiem_verdict.txt`. HEAD/tree và snapshot repo đầu/cuối không đổi; điều này chỉ chứng minh không có delta quan sát tại hai mốc.

KET_LUAN: changes_requested
