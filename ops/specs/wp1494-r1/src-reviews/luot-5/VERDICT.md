VERDICT: approve
reviewed_sha: 6ffb936e465c36ceba774442d8252f81a8f4ff7d
reviewed_tree: a263444f41b92769bd5e5407b200c8fc441f2b71
spec_sha256: 345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d

**Approve trong phạm vi review hẹp lượt 5. RV4-F01 đã sửa đúng cơ chế; không còn P0–P2 trong phạm vi H4..H.** Có một P3 mới về phép quan sát của test (RV5-F01), ghi đầy đủ bên dưới. Không có quyền push/merge/land phát sinh từ verdict này.

| Trục | Phán quyết |
|---|---|
| Spec | **approve hẹp**: giữ đủ bằng chứng khi cạn, giữ luật gộp, S1 vẫn thắng và không dùng kết quả một phần; P3 ở oracle test cần được theo dõi riêng. |
| Standards/Security | **Không tìm P0–P2 trong phạm vi đã đo**. Chốt dừng tài nguyên và phép so hạn không hồi quy; socket thật không đo được trong sandbox, không coi là lỗi sản phẩm hoặc pass giả. Miễn pha mở áp nguyên đúng giới hạn. |

Báo cáo được ghi tăng dần, chốt sau khi các phép đo hoàn tất. Phạm vi: RV4-F01 và hồi quy do H4..H; không mở lại lớp đã đóng.

Đã đo HEAD/tree, SPEC trước khi đọc, HANDOFF `dbc5eb70ae194d11d37af28fb67f1f529e268188ea79a19431582a8949038362`: khớp. `src` sạch. Reviewer OpenAI Codex, shell qua API, machine/local; model/effort phục vụ không có metadata độc lập để chứng thực. Không sửa src, commit, push, GitHub ghi hay dispatch.

Đo bổ sung: suite nguyên trạng rc 1, CA 480/481; đột biến 289/293; tự kiểm 5 đạt. `n16_socket_that` và bốn mục phụ thuộc không đo được do socketpair errno 1; không coi là lỗi sản phẩm. Actionlint và Ruff H/B rc 0. Probe hợp đồng báo cáo H3/H đều rc 0; script gốc rc 1 ở assert cũ. Ma trận 80 lượt cạn đạt mọi chốt dừng, script gốc rc 1 tại `lost[0]` vì không còn mất báo cáo. Các probe `_g5` rc 0. Probe độc lập 72 lượt cạn giữ dữ liệu chính xác, không I/O/ZIP/RUN sau cạn, không lọt kết luận. 16 biến thể bản vá/chốt tài nguyên, 19 cặp đều gốc 0 → mutant 3 bằng tín hiệu đúng tên ca.

## Finding trong phạm vi

Không có P0/P1/P2 được tái hiện trong phạm vi H4..H. Có một P3 mới ở phép quan sát của test, thuộc lớp đã có trong lịch sử §8.3; không phải lỗi trạng thái của mã sản phẩm H.

| id | severity | lớp nguyên nhân | tệp:dòng | mô tả | bằng chứng chạy được | gợi ý |
|---|---|---|---|---|---|---|
| RV5-F01 | P3 | `mutant-oracles-non-discriminating` | `ops/canh_tuoi_audit_test.py:927` | `get(v[0], "-")` biến cả `khong_dat` thành ký hiệu được mô tả là `khong_danh_gia`. Đổi riêng sáu phép chưa chạy của lượt dựng bù thành `khong_dat` vẫn qua `n2_can_tn_chua_danh_gia`; 480 ca chạy được trong suite cũng không bắt. H hiện thực vẫn ghi đúng; khe này làm yếu khả năng chống hồi quy của test mới. | `ulimit -v 3000000; python3 -B out/evidence/rv5_oracle_gap.py`: ca committed gốc 0 → mutant 0 (`SONG`); ca reviewer `rv5_placeholder_exact` gốc 0 → mutant 3 (`DO:rv5_placeholder_exact:`), đúng `TinHieuChotCa`. [JSON](evidence/rv5-oracle-gap.json), [log](evidence/rv5_oracle_gap.log). Không tính `SONG` là GIẾT. | So nguyên trạng thái/mã từng phép; hoặc ánh xạ đóng và từ chối giá trị ngoài miền. Không đổi mã sản phẩm để khớp test. |

Một biểu hiện / một lớp P3 trong phạm vi. Lớp giữ nguyên slug lịch sử, không đổi tên để tính là lớp mới. Theo chỉ dẫn review hẹp, P3 này không chặn verdict khi không còn P0–P2; nghĩa vụ xử lý P3 theo M1 của packet trước bước tích hợp vẫn phải được chủ kho/điều phối giữ, reviewer không tự miễn và không cấp quyền push/merge.

## Bảng đối chiếu RV4-F01, RV3-F03, RV3-F04

H4 = `dac537eb7fdb75fb74e1f0cfa17a67dc4ec69cae`; nguồn lịch sử trực tiếp là `review-4/VERDICT.md`. Nhãn luôn kèm phạm vi đo; không suy đóng toàn bộ lớp từ tổng suite.

| finding / lớp | nhãn | phép đo và giới hạn |
|---|---|---|
| RV4-F01 / `evaluation-report-evidence-dropped` | **ĐÃ SỬA ĐÚNG LỚP** trong các đường cạn tổng thuộc RV4-F01 | Probe gốc H3=0, H=0; 80 vị trí/thứ tự cạn giữ đủ hai lượt E, 0 lệch với giá trị `_phan_luot` đã đo; thêm 72 lượt với C10, khung cũ/đóng tay, id không theo thứ tự khung, lượt đỏ/đang chạy. 0 I/O/ZIP/RUN sau cạn. Lượt chưa đánh giá có mẫu trung thực. Không còn biểu hiện do H4..H sinh ra ở cơ chế này. Đường ngoại lệ có sẵn ghi riêng, không tuyên bố mọi đường S1 toàn chương trình đã đóng. |
| RV3-F03 / `mutant-oracles-non-discriminating` | **VÁ HỜ** ở mức toàn lớp, giữ giới hạn của lượt 4 | Ba biểu hiện quá hạn Q01–Q03 vẫn được sửa: ca nguyên bản đều 0→3 đúng tên trên đột biến chỉ-so-bằng; tám phép so hạn trùng H4..H; 53 biến thể/175 cặp cho kết quả trùng lượt 4. Không đo được target socket; sáu cặp sai lý do có sẵn không được tính GIẾT. Còn P3 mới RV5-F01 cùng lớp ở helper test báo cáo, không phải hồi quy phép so hạn. Không mở lại các phần đã đóng khác. |
| RV3-F04 / `unbounded-artifact-expansion` | **ĐÃ SỬA ĐÚNG LỚP** ở đồ thị caller hiện tại | Năm chốt `f04:*` đều bị gỡ riêng và bị đúng ca đích giết: 5 biến thể/7 cặp. Ma trận cũ 80 lượt/40 vị trí ZIP, hai ca cùng ZIP và 72 lượt mới: không công việc đánh giá sau cạn. Đúng bằng tổng vẫn fresh; thiếu 1 byte trả S1. Hệ quả mất báo cáo mà lượt 4 ghi “VÁ SINH LỖI MỚI” đã được H sửa. Không bảo đảm cho caller tương lai chưa tồn tại. |

## Đột biến bản vá và chốt tài nguyên

Tất cả bản đột biến nằm ngoài `src/`, ở `review-tmp/`; mọi lệnh chạy dưới `ulimit -v 3000000`, Python `-B`/`PYTHONDONTWRITEBYTECODE=1`. Chỉ ghi GIẾT nếu gốc đạt và đột biến đỏ bằng **TinHieuChotCa của chính ca đích**. Lỗi setup/ngoại lệ thường/rc 4 không có tín dụng.

Lệnh: `python3 -B out/evidence/rv5_mutations.py`; rc 0, **16 biến thể / 19 cặp GIẾT đúng tên**. Chi tiết neo/thay, rc và output từng cặp ở [rv5-mutations.json](evidence/rv5-mutations.json).

| biến thể | chốt bị gỡ/nới | ca đích | gốc → mutant / phân hạng |
|---|---|---|---|
| `keep_return` | `break` → trả S1 ngay, tái lập cách H4 bỏ dữ liệu | `n2_can_tn_giu_luot` | 0→3 GIẾT |
| `drop_measured_warning` | xoá C10 đã đo | `rv5_warning_preserved` | 0→3 GIẾT |
| `exhausted_remove` | bỏ nhánh phán lượt cạn | `n2_can_tn_chua_danh_gia` | 0→3 GIẾT |
| `exhausted_green` | phán lượt cạn thành `dat` | cùng ca trên | 0→3 GIẾT |
| `placeholder_omit` | không dựng lượt E còn lại | cùng ca trên | 0→3 GIẾT |
| `placeholder_green` | lượt chưa đánh giá thành `dat` | cùng ca trên | 0→3 GIẾT |
| `placeholder_evaluates` | gọi lại `_phan_luot` khi dựng bù | `n2_can_tn_t2`, `n2_can_tn_t5` | 2 cặp 0→3 GIẾT |
| `placeholder_substate` | mẫu mặc định mang `khong_dat` | `rv5_placeholder_exact` | 0→3 GIẾT |
| `placeholder_T4` | T4 đã đo bị ghi chưa đánh giá | `rv5_placeholder_exact` | 0→3 GIẾT |
| `s1_removed` | bỏ return S1 sau khung | `n2_can_tn_khong_dung_luot_giu` | 0→3 GIẾT; mutant dùng SHA/tiến dòng/kết luận xanh |
| `s1_after_obligations` | dời return xuống sau tính O/`dong_den` | cùng ca trên | 0→3 GIẾT; chốt phải đứng trước cập nhật kết luận |
| `f04_goi` | bỏ dừng trong cùng ZIP | `n2_can_tn_cung_goi` | 0→3 GIẾT |
| `f04_t5` | tiếp tục gói kế trong T5 | `n2_can_tn_t5` | 0→3 GIẾT |
| `f04_t3` | tiếp tục T3 sau T2 cạn | `n2_can_tn_t2` | 0→3 GIẾT |
| `f04_t7` | tiếp tục T7 sau cạn | `n2_can_tn_t2`, `n2_can_tn_t5` | 2 cặp 0→3 GIẾT |
| `f04_e` | tiếp tục lượt kế của E | `n2_can_tn_t2`, `n2_can_tn_t5` | 2 cặp 0→3 GIẾT |
| `placeholder-report-red` (probe bổ sung) | chỉ sáu phép con của lượt dựng bù đổi thành `khong_dat` | ca committed `n2_can_tn_chua_danh_gia`; ca reviewer `rv5_placeholder_exact` | **0→0 SỐNG** ở ca committed; **0→3 GIẾT** ở ca reviewer. Đây là RV5-F01, không cộng ca sống vào tín dụng |

Đột biến hồi quy cũ: `rv4_mutations.py` nguyên bản rc **1**; `53 VARIANTS 175 PAIRS SURVIVING_VARIANTS [] WRONG_REASON_PAIRS 6`. Cả 53 dòng `base_ok` và dòng tổng **trùng từng dòng** với log lượt 4. Không nói “175/175 GIẾT”. Sáu cặp sai lý do là `f02_vong_doc_{ne,lt,le}` × `n15_vong_doc_{patch,post}`, rc 4 do `KeyError W2/W5`, đã có sẵn. [Đối chiếu](evidence/rv5-measurements.json).

## BẢNG SĂN

Dùng REST JSON/ZIP dữ liệu thường, đồng hồ/trần giả; không dựng payload thù địch. Hướng thù địch chỉ mô tả dưới dạng giả thuyết về khả năng tiêu tài nguyên hoặc làm sai báo cáo.

| hướng | phép đo/soi | kết quả |
|---|---|---|
| Trả S1 bỏ lượt đã xong ở đầu/giữa/cuối E | Probe hợp đồng gốc, ma trận 80 lượt, 72 lượt mở rộng | H giữ đủ E và nguyên kết quả đã đo; không mất C10/definition, mã phép, attempt hay mốc tuổi |
| Dựng bù âm thầm đọc REST/ZIP hoặc phán xanh | Watch `_phan_luot`, `_goi`, `_tho_zip`; mutant `placeholder_evaluates`, `placeholder_green`, exact placeholder | 0 RUN/CALL/ZIP sau cạn; mọi phép chưa chạy `khong_danh_gia`, T4 `dat`; P3 nằm ở độ phân biệt của test mới |
| Lượt đã `dat` lọt qua S1 vào SHA, O, `dong_den`, fresh | Khung F có hai lượt, id đảo thứ tự khung, return bỏ/dời | S1, sha null, dòng giữ, O rỗng; 12/72 báo cáo có mọi khung `dat` vẫn không xanh tổng |
| Dữ liệu giữ lại lọt vào Issue/comment | Đọc mọi PATCH/POST giả của 72 lượt, 36 POST mới | Mọi nhịp tim đều KDD/sha null/dòng cũ; comment mới là cảnh báo KDD và câu “chưa có SHA…”; 0 D9 compare |
| Cạn ở mọi gói và ngay trong cùng tệp/ZIP | 40 vị trí × 2 thứ tự API; hai ZIP thường; năm mutant f04 | Không làm việc sau cạn; đúng bằng trần vẫn fresh, dưới tổng 1 byte S1 |
| Khung đóng tay hoặc lịch E làm sai lát cắt `E[len(luot):]` | Ma trận khung cũ/đóng tay; id 2/100/900 trái thứ tự khung; đảo D1 | Đủ đúng tập E; không đánh giá lượt khung đóng tay; khung đóng tay giữ lý do |
| Lượt đỏ/đang chạy/C10 trước cạn bị ghi lại | 72 lượt mở rộng; C10 mutant; T3 đỏ rồi T5 cạn | Quan sát đã có giữ nguyên; lượt đang đánh giá lúc cạn KDD, T3 đỏ vẫn thấy trong phép con |
| Đường S1 vì thời gian làm mất báo cáo hoặc dùng kết luận từng phần | Tiêm hết hạn ngay sau gộp, so H4/H; d99 và Q01–Q03 | H4/H cùng báo cáo giữ lượt, sha null/dòng cũ; tám phép so không đổi; ca quá hạn vẫn giết đúng |
| Lưới `danh_gia_nem` làm mất dữ liệu đã tích luỹ | Tiêm ValueError khi bắt đầu gộp sau hai lượt hoàn tất; so H4/H | Cả hai đều `khung={}`; cùng lớp nghĩa nhưng có sẵn, không do H4..H; chưa có tái hiện đầu vào thường tự gây ngoại lệ này |
| Pha mở, body hoặc hoàn tất ghi bị hồi quy | So byte sáu nút pha mở; 84 cặp body; probe POST 179,5/180/181/500 s | Pha mở trùng; 84/84 GIẾT; POST trễ chưa xác nhận, lượt sau 0 POST trùng; socket thật không đo được |
| Nhánh không cạn đổi vì tách `_luot_trong` | 25 tổ hợp F/P `dat/do/kdd/chay/vang`, so H4/H cả report và log | 25/25 hoàn toàn bằng nhau |
| Scope/registry/CI bị thay âm thầm | Git numstat, literal MOI, quét đủ tệp và commit message | Đúng bốn tệp; +3456/−0; MOI nguyên văn; 0 dấu bỏ qua CI; H4..H chỉ hai tệp |

## Phán ba câu hỏi executor

1. **Chấp nhận khung `dat` trong báo cáo có trạng thái tổng S1.** §5 gộp khung và §3/S1 quyết trạng thái tổng là hai phép khác nhau; giữ kết quả gộp đã quan sát không cấp một SHA audit hợp lệ. Không có quy tắc ép tất cả khung không thủ công thành KDD. Đo được 12 trường hợp mọi khung gộp `dat` mà S1 vẫn thắng, sha null, dòng không tiến. Người đọc phải đọc `trang_thai`/`ma_ly_do` ở cấp tổng; `khung.gop` là chi tiết. Summary dùng trạng thái tổng; Issue body không chứa `khung`, chỉ chứa nhịp tim; 36 comment mới đã đo đều là cảnh báo KDD. Không thấy diễn đạt xanh giả do bản vá. Comment đang chờ từ một lượt cũ có thể mang trạng thái cũ theo giao thức §7; đó không phải kết luận từ các lượt vừa giữ.

2. **Chấp nhận `khong_do_duoc` / `het_tai_nguyen_danh_gia` cho lượt bị ngắt vì cạn tổng.** Đây là nhãn gián đoạn của pha §3/S1 và chỉ dẫn chủ kho “đánh dấu trung thực phần chưa đánh giá”, không phải kết quả phán completed qua đủ hai bậc §4. T7 chưa chạy nên không nên trình bày lượt như đã hoàn tất luật phán thông thường. `goi_vuot_tran` vẫn nguyên ở T2/T5 đã chạm trần; mã chẩn đoán không mất. Probe cả T3 đỏ rồi T5 cạn giữ `hinh_workflow_la` và `goi_vuot_tran` trong phép con, còn lượt KDD vì chưa neo xong. Không yêu cầu đổi mã lượt thành `goi_vuot_tran`. Phạm vi diễn giải này chỉ là lượt bị ngắt do cạn tổng; lượt đánh giá trọn vẫn phải giữ luật/mã đầu tiên của §4. Không có trạng thái/tên trường mới.

3. **Có, `danh_gia_nem` có thể cùng lớp nghĩa `evaluation-report-evidence-dropped`, nhưng không phải hồi quy H4..H.** Bộ bắt ngoại lệ tạo `kq` mới ở `ops/canh_tuoi_audit.py:960`–`:963`, làm mất local `luot` của `_danh_gia`. Probe lỗi tiêm sau hai lượt đã xong cho cùng kết quả trên H4/H. Mã bắt ngoại lệ không đổi, và chưa đo được đầu vào dữ liệu thường tự gây lỗi ở nhánh mới. Ghi ngoài phạm vi có sẵn, không dùng để mở lại RV4-F01 hay tính vào verdict hẹp. Không tuyên bố đường này đã được sửa.

## Bảng đo lại lời khai executor

Các script lịch sử được chép nguyên byte từ `review-4/evidence/`; băm và đối chiếu ở [rv5-measurements.json](evidence/rv5-measurements.json). Bản `_g5` của executor được chạy riêng, không dùng để thay rc của script nguyên bản. Các probe mới và lệnh chạy đều lưu trong `out/evidence/`.

| lời khai / phép chạy | rc thực | kết quả đo |
|---|---:|---|
| `git -C src rev-parse HEAD HEAD^{tree}`; hash SPEC trước đọc; hash HANDOFF | 0 | Khớp toàn bộ định danh đầu báo cáo; clone không shallow, nhánh `agent/wp1494-r5-g5-fable` |
| `python3 -B out/evidence/rv5_baseline.py` | 0 | B trên first-parent `origin/master` snapshot; đúng merge #1516; schema/fixture/khối Lệnh kiểm đúng ghim; bốn hàm nguyên văn trùng; KHUNG_DAU/Issue/B khớp lease và Mission; upload B, 11 tên/11 khoá T3, tệp mới vắng ở B. [Log](evidence/rv5_baseline.log) |
| `python3 -B out/evidence/rv5_static.py` | 0 | B..H đúng 4 tệp, +3456/−0; H4..H +16/−5 sản phẩm, +30/−0 test. Sáu nút pha mở và tám phép so hạn trùng byte/biểu thức. MOI literal đúng, không bỏ CI. [JSON](evidence/rv5-static.json) |
| `python3 -B ops/canh_tuoi_audit_test.py --chi-tiet` (cwd bản sao H) | **1** | **CA 480/481**, **DOT BIEN 289/293**, tự kiểm **5 đạt**, **TONG DO**. Không tái lập lời khai rc 0 tại sandbox này. Một ca `n16_socket_that`, bốn mục `f02_nen_han`, `f02_nen_han_bien`, `f02_nen_socket`, `f02_nen_loi` bị socketpair errno 1; không tính thành lỗi sản phẩm. [Log](evidence/suite.log) |
| Bốn mutant mới committed `rv4_giu`, `rv4_can`, `rv4_con`, `rv4_s1` | trong suite | 4/4 GIẾT đúng ca đích; ba ca mới đạt. Độc lập đã gỡ/nới thêm như bảng đột biến |
| `python3 -B .claude/dev/ci_dang_ky_test.py` (H) | 0 | **PHẢN CHỨNG 1677/1677 đỏ đúng; TỔNG ĐẠT**. Khớp executor. [Log](evidence/registry.log) |
| `actionlint -shellcheck /usr/bin/shellcheck .github/workflows/canh-tuoi-audit.yml` (H) | 0 | Log rỗng; actionlint 1.7.7, ShellCheck 0.9.0 |
| Ruff `--no-cache --select F` ba `.py` đổi ở H; registry B | 0 / 0 | `All checks passed!`; delta F=0; Ruff 0.15.15 |
| `packet_loop.py doctrine-scan --root .`; `adr-song --root .` (H) | 0 / 0 | Sạch 12 tệp; 66/66 ADR |
| `rv4_report_contract.py` nguyên bản | **1** | **H3 rc 0, H rc 0**. Assertion cuối vẫn đòi H=3 nên script đỏ. Không phải product fail. `_g5` rc 0, `REPORT_CONTRACT_HELD` |
| `rv4_resource_matrix.py` nguyên bản | **1** | Mọi assert 80 lượt/40 vị trí và hai ZIP đạt; `AFTER_WORK=0`; đúng tổng fresh. `lost=[]`, script đỏ tại `lost[0]`. `_g5` rc 0; dữ liệu kiểm độc lập 0 thiếu lượt, 0 lệch quan sát, 0 lọt SHA/dòng |
| `resource_stop.py`; `resource_stop_signals_g4.py` | 0 / 0 | `RESOURCE_STOP_COMPLETE`; `2/2 CURRENT_CODE_MEETS_NAMED_EXPECTATION` |
| `rv4_mutations.py` nguyên bản | **1** | 53 biến thể/175 cặp; 0 biến thể sống hoàn toàn, 6 cặp sai lý do có sẵn; 53 dòng kết quả trùng lượt 4 |
| `rv4_inventory.py` | 0 | 24 mục hạn; 2 mục có target socket; D134 vắng khỏi bảng thực thi; không xoá ca/mutant cũ |
| `rv4_test_structure.py` | 0 | **65 cặp tương đương**, gồm gốc và 12 mutant |
| `rv3_deadline_coverage.py` | 0 | Q01/Q02/Q03 gốc 0 → mutant 3 đúng ca; cả đầu vào quá hạn được khôi phục cũng phân biệt. Socket trong sweep toàn ca vẫn tách riêng |
| `rv3_body_deadlines.py` | 0 | **84/84** gốc đạt, mutant GIẾT; HTTPResponse/BufferedReader thật trên raw và đồng hồ giả, không phải socket thật |
| `rv4_post_deadline.py` | 0 | **4/4**; 179,5 s xác nhận, 180/181/500 s giữ pending; lượt sau 0 POST trùng |
| `rv5_class.py` | 0 | 72 lượt cạn, 25 tổ hợp không cạn H4/H bằng nhau, 2 nhánh S1 thời gian/lưới ngoại lệ đối chiếu H4/H |
| `rv5_mutations.py`; `rv5_oracle_gap.py` | 0 / 0 | 16 biến thể/19 cặp GIẾT đúng; thêm mutant báo cáo cho thấy khe P3: ca committed SỐNG, ca reviewer GIẾT |

Không nhận kết quả executor/phiên điều phối trên clone khác làm kết quả đo của reviewer. Lệnh gốc, cwd và rc các gate có ở [check-commands.json](evidence/check-commands.json), [probe-results.json](evidence/probe-results.json), [secondary-commands.json](evidence/secondary-commands.json).

## Write set, MOI và dấu bỏ qua CI

| tệp B..H | thêm | xoá |
|---|---:|---:|
| `.claude/dev/ci_dang_ky_test.py` | 1 | 0 |
| `.github/workflows/canh-tuoi-audit.yml` | 29 | 0 |
| `ops/canh_tuoi_audit.py` | 1062 | 0 |
| `ops/canh_tuoi_audit_test.py` | 2364 | 0 |
| Tổng | **3456** | **0** |

Đúng bốn tệp giao nộp; dưới trần 3500 còn 44 dòng. Registry chỉ thêm một mục MOI nguyên văn SPEC, không sửa/xoá mục khác. Quét **toàn nội dung bốn tệp** và **18 commit message B..H**: 0 dấu bỏ qua CI. `git diff --check B H` rc 0. H4..H không đổi workflow/registry. Hai bản sao H/B dùng `core.abbrev=7`.

## Rủi ro tồn dư đã miễn

- **Pha mở urllib**: giữ đúng [miễn 7162892740](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7162892740), được [quyết định review hẹp 7170825561](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7170825561) giữ nguyên. `_mot_lan`, `_goi`, `transport_that`, `_NenCoHan`, `_NguCanh`, `_KhongChuyenHuong` **6/6 trùng byte H4..H**, băm riêng ở rv5-static.json. DNS/connect/TLS/gửi/status+header trong `open()` chưa có hạn tuyệt đối toàn pha; kết quả mở trễ bị từ chối sau đó. Không mở rộng miễn sang body/HTTPError/ghi/đối soát/giải nén.
- **D134**: giữ [miễn 7157619068](https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7157619068): quan sát bất khả với schema ghim, ngoài mẫu số, không tín dụng GIẾT. Inventory xác nhận không có mutant D134 thực thi.
- Đã đọc ba quyết định bằng GitHub GET chỉ đọc; [bản lưu](evidence/owner-comments.json). Không ghi Issue thật, không gọi dispatch.

## Ngoài phạm vi, có sẵn

| id ghi nhận | severity | lớp | vị trí / bằng chứng | xử lý trong verdict |
|---|---|---|---|---|
| OOS-01 | P2 có điều kiện khi phát sinh ngoại lệ giữa pha | `evaluation-report-evidence-dropped` | `ops/canh_tuoi_audit.py:962`: lưới an toàn dựng báo cáo rỗng. Tiêm ValueError ở gộp sau hai lượt xong: H4 và H cùng mất quan sát. [rv5-class.json](evidence/rv5-class.json), `other_S1/safety` | Có sẵn H4, không bị sửa. Chưa tái hiện bằng dữ liệu thường tự gây ngoại lệ; không nâng thành lỗi sản phẩm mới, không tính vào verdict hẹp. Không tuyên bố toàn lớp toàn chương trình đã đóng |
| OOS-02 | P3 | `mutant-oracles-non-discriminating` | Sáu cặp `f02_vong_doc_{ne,lt,le}` × `n15_vong_doc_{patch,post}` rc 4 vì thiếu W2/W5. Kết quả trùng log lượt 4 | Không tín dụng GIẾT cho sáu cặp; vẫn có target khác giết từng biến thể. Không do H4..H, không tính vào verdict |

Không tìm P0/P1 có sẵn cần kéo vào phạm vi. Các S1 trước T4/D1/E hợp lệ chưa có quan sát lượt để giữ; không dùng chúng làm phản chứng cho việc bỏ lượt đã đo. Nhánh cạn thời gian sau gộp giữ `khung` cả H4/H; không phát hiện đường S-sớm mới mất bằng chứng do bản vá.

## KHÔNG ĐO ĐƯỢC / không chạy

| phần | trạng thái |
|---|---|
| Socket thật `n16_socket_that` và bốn mutant liên quan | **KHÔNG ĐO ĐƯỢC**: `socket.socketpair()` bị `PermissionError: [Errno 1] Operation not permitted` ngay trên bản gốc. Không bỏ ca, không giả rc 0, không vượt sandbox. Không coi là lỗi sản phẩm |
| Loopback/TLS thực và hạn wall-clock thực | Không đo; phép body dùng HTTPResponse/BufferedReader thật nhưng raw/clock giả |
| Python 3.12 của workflow | Không chạy lại trong lượt 5; lần này Python 3.13.18. Không lấy đo lượt 4 hay executor làm kết quả hiện tại |
| Windows M3, CI PR, full M9, registry `--chay`, toàn kho `tl.py --selftest` | Không chạy trong review hẹp chỉ đọc; gate registry mặc định không thay các gate này |
| GitHub thật/Issue #1520, artifact B1a thực, kênh người nhận | Không thử ghi/gửi/dispatch. Mọi luồng Issue/comment đã đo dùng GitHub giả trong bộ nhớ |
| Trigger tự nhiên cho lưới an toàn sau khi có quan sát | Chưa đo được. Chỉ có phép tiêm lỗi ghi rõ, không tuyên bố dữ liệu thường đã gây ra |
| Ref remote sau snapshot được bàn giao | Không fetch vào src; chỉ xác nhận object/ref trong clone được cấp và GET quyết định chủ kho |
| Model/effort phục vụ | `KHONG_DO_DUOC`; không biến tên model/effort trong prompt/lease thành attestation. Identity provider/surface/session lưu riêng |

Đây là kết quả review mã hẹp trên exact H, không phải chứng nhận toàn bộ cổng merge/land hay nghiệm thu vận hành.

## Receipt chỉ đọc, hiện vật và điểm dừng

Đối chiếu hai mốc toàn worktree ngoài `.git`: **18.097 → 18.097 tệp; 0 đổi băm, 0 thêm, 0 xoá**. HEAD/tree đúng H; status, diff và index diff rỗng. [Receipt](evidence/readonly-result.json), [log](evidence/readonly.log). Không tuyên bố đã băm mọi byte `.git` hay chứng minh mọi thời điểm trung gian.

Provider `openai_codex`; execution surface công cụ shell qua API (`codex_service` theo định nghĩa kho), transport `machine/local`; session/thread đo được `01a21420-8332-79b3-a8bc-97e2aab0910d`. Sandbox workspace-write, approval never, mạng shell bị hạn chế. [Identity](evidence/reviewer-identity.json), [phiên bản công cụ](evidence/versions.json). Không lấy GitHub actor hay yêu cầu tên model làm danh tính model đã phục vụ.

Phép bổ sung `rv5_pending.py` rc 0, **2/2**: sự kiện cũ đang chờ được giao đúng nguyên object của lượt trước; nhịp tim hiện tại vẫn S1, sha null, dòng cũ, cảnh báo hiện tại được hoãn đúng giao thức. [Log](evidence/rv5_pending.log), [JSON](evidence/rv5-pending.json). Không nhầm chữ `fresh` của một sự kiện cũ với rò kết luận từ lượt vừa giữ.

Đã dọn `review-tmp/` và các bản nháp/nguồn probe cũ không dùng do reviewer tạo; giữ `out/` cùng đầu vào được bàn giao. Không sửa branch executor, không commit sản phẩm, push, GitHub ghi hay dispatch. Bộ registry có thể tạo commit fixture trong thư mục test tạm của chính nó; đó không phải commit vào `src/` hay nhánh packet.

Để chạy lại: từ thư mục chứa `src/`, `review-4/`, `bang-chung-executor/`, dùng `python3 -B out/evidence/setup.py` dựng clone H/B và ghim abbrev 7; rồi chạy `run_checks.py`, `run_probes.py` hoặc từng probe đã nêu. Với mọi suite/mutant, giữ `ulimit -v 3000000` vì có ca luồng vô hạn chủ ý. `rv4_mutations.py` cần chạy trước `rv4_test_structure.py` để tạo các bản đột biến mà phép đối chiếu dùng. Định nghĩa mutant, target, output, mã thoát đã được giữ trong JSON nên không cần giữ bản nguồn tạm để đọc verdict.

**Lượt review mã 5 kết thúc tại exact H.** Không mở vòng vá/review mới. Quyết định cuối là `approve` cho phạm vi được giao, với P3 và các giới hạn đo ghi rõ; mọi gate tích hợp và nghĩa vụ P3 theo packet vẫn thuộc bước của chủ kho/điều phối.
