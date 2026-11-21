Review offline MÃ wp1236 A r11 — lượt 11, lời gọi Codex 12/12 cuối.

HEAD `0d814877e3acef6274a7f1c0e9a28531a24d0e65` · tree `fac4f2e0d8d9bcd41389c8ae40d1de2cc44639eb`. Spec SHA-256 `30386131d8017bf982ca0be7707c8d5fd3035e9586c5f94a446f45c40fc863d1`;  lease `wp1236-a-r11-g1-claude-20261121`. Provider `openai_codex`, surface `codex_cli`, transport `machine`;  model/effort phục vụ `KHONG_DO_DUOC`. Linux, Python 3.13.18;  checkout read-only, mọi hiện vật nằm trong work.

**S01 — P2 — `test-thieu-chot`: Q01 VÁ HỜ.** Cả 16 mutant cũ đã bị a130 giết riêng trên cả hai tuyến (32/32 phép cô lập). Tuy nhiên quét độc lập 15 mutant tìm được **6 survivor**, mỗi mutant qua 47/47 ca và có witness đổi kết quả. Các ID: `r11_url_bmp_only` · `r11_url_no_zero_width` · `r11_reason_bmp_only` · `r11_reason_no_zero_width` · `r11_word_ascii_first` · `r11_consumer_ascii_conclusion`.

Nguyên nhân chung: `\S` chỉ được thử bằng 26 đại diện/category, không có ký tự ngoài BMP;  `\w` chỉ được ghép sau `success` ở parser, consumer chỉ nhận 4 chữ ASCII của `success`. Unicode đầu conclusion và kiểm ASCII riêng ở consumer còn lọt. Các mutant mới thuộc **luật 4**, xét trước luật 6, không được hạ thành ngoài bảng đóng. Bằng chứng: [scan](scan_results.jsonl), [phân hạng từng ID](scan_classification.json), [đối chứng](independent_witnesses.json), [coverage thực đo](a130_observed_coverage.json).

Tự liệt kê từ mã:10 regex,17 vị trí Unicode (12 `\d`,2 `\s`,2 `\S`,1 `\w`);  `RE_TEP_DG` chỉ dùng lớp ASCII tường minh. Parser được thử 680 Nd ở 7 vị trí;  consumer dùng đại diện theo 67 khối, không đủ 680 ký tự mỗi vị trí (quan sát 71–387). `landed` và URL id thử 680;  token thử 29 whitespace ở cả 2 vị trí qua 2 tuyến;  ngày thử 670 Nd không-ASCII ở năm/tháng/ngày và đúng lý do `han`. Các số này mô tả **a130**, không tuyên bố mọi tổ hợp đã phủ. Xem [inventory](regex_inventory.json).

Hướng đóng S01: dùng ma trận cùng đầu vào cho parser/consumer, đưa ký tự `\w` vào vị trí đầu/đơn lẻ và đồng bộ fixture thành failed hợp lệ;  vét miền `\S` thay đại diện/category;  giữ đối chứng, thứ tự lý do, giữ đối chứng lượng từ hiện có. Ghim các cặp mới. Không đổi sản phẩm/spec để né test. Rủi ro cần kiểm: thời gian chạy, phiên bản Unicode, chốt khác bắt thay. Đã hết trần lời gọi: chuyển checkpoint trước vòng sửa/review mới.

**S02 — P3 — `test-thieu-chot`: Q02 CHƯA VÁ, chờ miễn chủ kho.** `r9b_event_tab` và `r9b_name_inner_spaces` vẫn 47/47;  baseline 125/125 ô đúng, mỗi mutant 0/125 ô phân biệt, nhưng witness TAB cuối event/khoảng trắng kép name đổi hai tuyến. Giữ `ngoai_bang_dong` theo luật 6(b). Miễn phải neo chính SHA trên, nêu slug/hai ID/lý do/hướng xử lý. Chưa có comment miễn trong đầu vào;  không gọi mạng. Miễn này không đóng S01.

| Lớp kế thừa | Nhãn trên HEAD |
| --- | --- |
| `yaml-ngoai-schema-bi-chan` | ĐÃ VÁ THẬT |
| `k2-mat-loi-doc` | ĐÃ VÁ THẬT |
| `cli-vong-yaml-traceback` | ĐÃ VÁ THẬT |
| `mo-ta-duong-dan-lech-hop-dong` | ĐÃ VÁ THẬT |
| `test-thieu-chot` | VÁ HỜ |
| `hop-dong-dau-vao-dau-ra-chua-chot` | ĐÃ VÁ THẬT |

Chi tiết từng lớp, nguồn lịch sử và phần chưa đo trong `prior_class_status`/`class_table` của [VERDICT.json](VERDICT.json). P02 nguồn hạt giống đã kiểm lại bằng 7 đối chứng;  không có nhãn VÁ SINH LỖI MỚI. Hội tụ 10→11 **0/1**, lớp `test-thieu-chot` tiếp tục lặp;  không đổi slug hay hạ hạng.

Ledger 186 ID tự đo: **172 GIET · 7 TUONG_DUONG · 5 KHONG_AP_DUNG · 2 NGOAI_BANG_DONG**. Các anchor không áp được có tái dẫn xuất/luận chứng kết thúc;  không chuyển nhãn cũ sang head mới theo lời khai. [Ledger đã kiểm](ledger_186_verified.json);  [kho mới 15 cặp](kho_dot_bien_luot11.jsonl);  [kho cộng dồn 201 cặp](kho_dot_bien_luot6_7_8_9_10_11.jsonl).

| Phép đo | Kết quả |
| --- | --- |
| `python3 -B ops/gate_output_doi_chieu_test.py` | rc 0; 47/47 ca; 146/146 mutant;  tự kiểm 2/2; TỔNG ĐẠT |
| Ruff `--no-cache --select F`,3 tệp | rc 0;  Ruff 0.15.15 |
| Ruff pin/probe contract | rc 0; 3 contract,0 lỗi |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | rc 0; 1226/1226 phản chứng; TỔNG ĐẠT |
| `git diff --check 010046f… HEAD` | rc 0 |
| Numstat |3 tệp; +1985/−0, dưới trần 2100 |
| `tl.py --selftest`, HEAD và nền 2719 f 81 | **rc 1 cả hai; 1768/1784**, cùng 16 lỗi, stdout byte-bằng, delta 0 |
| Windows native/CI/LIVE | not_run |

Không tái hiện lời khai 1770/1784. Bất biến(a) chưa đạt N/N;  **đỏ nền delta 0 vẫn là failed**. Các skipped của mô phỏng nt không phải Windows native pass. Snapshot 17969 tệp cả tracked/untracked/ignored, HEAD/tree/index/diff ở đầu/cuối không đổi. JSON ghi command/rc/hash và giới hạn quan sát;  validator schema không chứng nhận nội dung.

**CHƯA ĐỦ ĐIỀU KIỆN MERGE:** còn S01/P2, S02 chờ miễn exact SHA, gate selftest chưa N/N và Windows/CI chưa được đo trong lượt offline này. Handoff Review Rescue Checkpoint theo §12;  không tự mở lời gọi review mới.

KET_LUAN: changes_requested
