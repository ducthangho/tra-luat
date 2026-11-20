# Review đặc tả lượt 5 — CI-TAI-DUNG-THEO-CAY

**Kết luận: `changes_requested`. Còn 5 P2 và 3 P3; chưa chứng minh P0/P1.** A r4 giữ kết luận approve riêng về đặc tả. B1 r4 và B2 r4 cần revision.

Reviewer: Codex, họ model OpenAI. Phạm vi theo `PROMPT.md`: chỉ đọc trong RV, không mạng, không đọc `.codex` hoặc memory; mọi bản sao, fixture, script và kết luận mới nằm trong `RV/out/`. Không sửa đặc tả hoặc cây kho. Chuẩn L1–L7 được đọc từ chính `cay-kho/.claude/skills/soan-spec/SKILL.md` theo yêu cầu review; đây không phải phiên soạn spec hay cấp lease.

## Neo và giới hạn phép đo

| Đối tượng | Giá trị đã kiểm |
|---|---|
| SHA-256 A r4 | `0400723011a4a2f0362736de6872a177537e36aeb403e5a4ce59cf8bbd96dacc` |
| SHA-256 B1 r4 | `bd7aa007721db652167d235b43eff55974e3b7684fb345a2d2176541e4c2c816` |
| SHA-256 B2 r4 | `21bdbd5c5059e59ef03a4b415c566895618a508d75cad515cf99b69cbd653b43` |
| HEAD `cay-kho` | `45bae8d07a8cdf06a1ca9a7a2e015a6258169379` |
| HEAD tree | `30d5c7dec30dc658ae04ef29a6ffafe94eb8f197` |
| Ref `origin/master` cục bộ | `a31c680c8880786848f832a35554d9e84078b270`, khác HEAD đóng gói; review neo HEAD được giao, không fetch |
| Cây làm việc / lịch sử | `git status --porcelain` rỗng đầu và cuối; không shallow |
| Thời điểm | 20-11-2026 UTC, qua 00:00 ngày 21-11 giờ Việt Nam; thời điểm từng lệnh có trong nhật ký |
| Môi trường | Windows, PowerShell `-NoProfile` cho probe Windows; Python `-S`, PyYAML 6.0.3 từ `RV/py-lib` |

Hai ADR khai trần đều qua ba phép trên lịch sử HEAD: tệp tồn tại tại commit land (rc 0), chưa tồn tại tại cha đầu (rc 128), commit land thuộc first-parent HEAD. Băm ba spec được kiểm lại cuối phiên, không đổi. [Neo và numstat](review-evidence/20261120T165825750959.txt), [băm cuối](review-evidence/20261120T170549600458.txt), [status cuối](review-evidence/20261120T170549467057.txt).

Script chính: [review_r5.py](review_r5.py), dùng lại [review_r4.py](review_r4.py), các harness lượt 1–3 và [review_tools.py](review_tools.py). Hai YAML làm chứng: [B1 r4](thu/b1-r4-witness.yml), [B2 r4](thu/b2-r4-witness.yml). So với bản chứng kiến lượt 4, chúng có bước `ghi-ap-dung`, năm bước push có COE/timeout, biểu thức H đúng output tương ứng, `retention-days: 90`, lệnh tạo thư mục biên nhận gồm JSON/bundle và upload cả thư mục, upload `dau-vao/`, chế độ là hằng mã thay vì env của bên gọi.

`REAL` nghĩa là chạy Git hoặc hàm thật của kho. `MODEL` nghĩa là thực thi một mô hình của các điều kiện được liệt kê trong spec; chưa có triển khai B1/B2. Rc 0 của harness nghĩa là phép thử hoàn tất, không có nghĩa đặc tả đạt. Một số nhãn `R2`/`R3` còn trong output của hàm kế thừa; `pins`/`windows` của r5 thay đầu vào bằng YAML **r4**, không thay ngầm kết quả đo cũ thành bằng chứng mới. Các output r3 của `contract`, `history`, `runtime` là đối chứng trước sửa, rồi mới đến output r4.

## S1–S7 của lượt 4

| Finding | Trạng thái lượt 5 | Kết quả phép đo gốc trên r4 |
|---|---|---|
| S1 P2 — consumer Windows ngoài write set | **Đóng phản chứng Windows.** Bảng consumer vẫn có lỗi P3 T6. | `windows`: nền rc 0; thêm job chưa ghim rc 1; chỉ ghim còn đỏ vì thiếu gương; thêm cả dấu vân và `KHÔNG CHẠY` rc 0; B2 cập nhật chín dấu vân và dòng mới rc 0. Cả hai tệp đã vào write set B1. `pins`: B1/B2 đều 15/15 sau các cập nhật đã nêu; ngoại lệ rộng vẫn bị bắt. |
| S2 P2 — đuôi SHA/subject/definition | **Đóng các phản chứng đã dựng**, theo mô hình tin cậy B1:46–48. T5 là thiếu neo **lượt push**, khác lỗi object PR này. | `provenance`: Git bundle verify rc 0, object baseline được nhận; sửa đuôi SHA bị loại; lệnh bundle hai cha trên commit một cha rc 128; ngay cả cung cấp bundle hợp lệ một cha, I3 cũng loại; đổi blob workflow bị I6 loại. |
| S3 P2 — mất artefact rồi 20 tốt | **Đóng phản chứng cũ về cửa sổ; chưa đóng lớp lịch sử**, T3. | `history`: đỏ + 20 tốt ⇒ D0=false; mất artefact, H còn ⇒ b=1, D0=false; mất cả log ⇒ e=1, D0=false. Tuy nhiên quy tắc ưu tiên rc 1 che rc 2, và phạm vi c/d theo phiên bản tạo đường D0=true mới. Ca D2.33 còn tự mâu thuẫn về e. |
| S4 P2 — hai kế hoạch khác nhau vẫn được đánh dấu nhanh | **Đóng đúng phản chứng này; hợp đồng kiểm độc lập còn T1/T2/T4/T5.** | `contract` dùng lại fixture rename và `doc_diff`/`ke_hoach` thật: hai kế hoạch khác, I7=false, rc 1; I1 loại nhãn `tai_dung` có nhóm rỗng. Phát lại cùng hàm không thay cho các tiền đề mà I1–I7 còn thiếu. |
| S5 P2 — xét lỗi nhưng replay buộc skip | **Đóng phản chứng cũ.** | Tiến trình thật ghi artefact/output rồi rc 1; mô hình r4 với x=failure, t=success, H rỗng, ops success ⇒ rc 0 `khong_ap_dung`; ops failure ⇒ rc 1 `VI_PHAM_Q8`. |
| S6 P3 — hứa thời gian quá khả năng DAG | **Đóng.** | Mô hình hàng đợi cũ vẫn cho tăng 719 giây, nhưng r4:91–94 đã bỏ trần tăng 3 phút. C5/C6 đo để báo, không còn ngưỡng. YAML có đúng 5 bước mới; tổng timeout 24 < job 30; không reader bóng hoặc dependent biên nhận. |
| S7 P3 — hai ước B2 khác nhau | **Đóng ở B2.** Cùng loại lỗi xuất hiện ở B1, T7. | `sizes`: B2 cộng đúng 485, xin 550, luật dừng 550. B1 cộng đúng 600, xin 650, luật dừng lại 600. |

Bằng chứng: [pins](review-evidence/20261120T165829090254.txt), [Windows](review-evidence/20261120T165904273635.txt), [bundle](review-evidence/20261120T170130856488.txt), [contract](review-evidence/20261120T170127900334.txt), [history](review-evidence/20261120T170126497584.txt), [runtime và hồi quy](review-evidence/20261120T170305955403.txt), [kích thước](review-evidence/20261120T170151160280.txt).

## F, N, R kế thừa

| Finding | Trạng thái và căn cứ |
|---|---|
| F1 | Giữ đóng ở bộ xét: fixture rename thật vẫn có before=P1 nhưng kế hoạch khác, phải loại `nhanh`; r4 giữ phép 4g. |
| F2, N2, R1 | Các consumer từng đỏ đã được đưa vào write set và phép đo r4 đạt. Lỗi kiểm kê còn T6 P3, không tiếp tục khai consumer Windows ngoài write set. |
| F3 | Giữ đóng về đặc tả: C1/D1 đòi chạy Windows trực tiếp. Phiên này chỉ chạy phép so t32, chưa chạy trọn M3 của triển khai chưa tồn tại. |
| F4, R5 | Đóng phản chứng identity PR cũ bằng object bundle, tập shard chính xác, attempt 1 và blob workflow. Không coi việc đó là đã đóng thiếu identity push T5 hoặc đã đo bốn mốc LIVE. |
| F5 | Giữ đóng: A r4 không đổi, thước A đạt; bộ phân loại thật vẫn cho push hồ sơ `duong_nhanh`, `packet_loop=chay`. |
| F6, N5 | Giữ đóng: nền A2/A3/A4/A6 đỏ; ứng viên xanh; 19 đột biến nội dung đỏ đúng tiêu chí, reflow Q1 xanh; A5 Git thật nhận hai tệp và bắt tệp thứ ba. |
| F7 | Giữ đóng: ca C5 đã khai đầy đủ tiền đề; fixture diff khác nhưng hai kế hoạch bằng nhau chạy lại được. C5 LIVE chưa chạy. |
| F8, N3 | **Chưa đóng toàn bộ:** T1–T5 là các lỗ xác thực/tất định/bất biến/lịch sử của thiết kế mới. Không chỉ là đổi tên S3–S5. |
| F9, N9 | Vòng phụ thuộc và hình thức `nang_tran` đã đóng; B2 D0 vẫn đo trước merge. Lỗi con số trần B1 còn T7; chưa có quyền nâng trần chỉ vì spec khai một khối xin. |
| F10 | Các phản chứng L6 cũ của A vẫn đóng. Thước lịch sử mới có T3; không gọi một bảng đột biến là đủ khi công thức cho kết quả khác chính kỳ vọng của bảng. |
| N1, R3 | Đóng phản chứng mode cũ và S5; các đối chứng fallback cần áp I3/I4/I6 có điều kiện như D2.29–30, xem T4. Không ép job nhóm chạy/skip khi không thuộc D/H. |
| N4, R6 | Giữ đóng đường output sau lỗi: 16 cặp outcome chỉ success/success mang output; 5 bước COE, job biên nhận COE, không đọc bóng. |
| N6 | Giữ đóng: một/hai `doc_diff=None` loại nhanh; hai diff rỗng thật hợp lệ; `manh` truyền đúng. Probe gọi hàm thật. |
| N7 | Giữ đóng: `kiem-tai-dung` nhận cây; fixture Git baseline rc 0, đổi cây/đảo cha rc 1. |
| N8, R8 | Các câu thiếu mã cũ đã sửa. r4 có lỗi L7 mới tại B2, T8. |
| N10 | Giữ đóng giới hạn producer: chỉ đảm bảo chuỗi chuẩn do bộ xét phát. Không coi `contains` là parser toàn chuỗi. |
| R2 | Đóng phản chứng thiếu lượt cuối mẫu và latest attempt; Q8 tổng thể còn T3. |
| R4 | Giữ đóng ở mức spec: job nghỉ cấp job dùng hình dạng REST đo ở D4, không tự tạo shard/runner. D4 LIVE vẫn chưa đo. |
| R7 | Đóng cùng S6: bỏ lời hứa latency, giữ phép báo thời gian. |
| R9 | Đã sửa nhất quán sang **năm** bước mới ở r4; YAML đo đúng năm. |

[Rename thật](review-evidence/20261120T165927129683.txt), [A và các đột biến](review-evidence/20261120T165905439158.txt), [hồi quy Q7/tree/A5](review-evidence/20261120T170305955403.txt), [push hồ sơ và sáu vị trí cổng](review-evidence/20261120T170405096793.txt).

## Phát hiện mới

### T1 — P2 — Xác thực danh sách tại t0 vừa bác bản lưu trung thực, vừa chưa xác thực đủ các hàng

**Vị trí:** `SPEC-B2-r4.md:136–140`, `:233–234`, `:174–180`; liên quan `SPEC-B1-r4.md:196–208`.

Một run đang `in_progress` hoàn toàn có thể đã xong `chuan-bi`, trong khi job nặng còn chạy. B2:140 lại cấm **bất kỳ job attempt 1** nào xong trước t0 nếu bản lưu chưa `completed`. Đây không phải suy luận hợp lệ về trạng thái toàn run. Tầng thu có thể ghi đúng mọi byte, bộ xét bỏ qua run đó đúng 4c, nhưng kiểm lại vẫn kết luận `sai`. Hàng ấy nằm mãi trong lịch sử cùng phiên bản; chờ job hoàn tất không làm mốc hoàn tất của job đầu biến mất.

Chiều ngược lại, phép so tập chỉ yêu cầu mọi id đọc lại có created_at≤t0 xuất hiện trong bản lưu. Nó không đòi mọi id bản lưu phải tồn tại trong nguồn, không kiểm đủ các trường lựa chọn của **run không được chọn**. Một hàng `completed/success` bị lưu nhầm thành `completed/failure` vẫn qua luật này; không chọn nguồn thì nhánh xác thực “lượt nguồn” không sửa được thiếu sót ấy. Phát lại trên chính đầu vào sai vẫn trả `khong_tai_dung` giống bản ghi.

**Lệnh:** `python -S out/review_tools.py python out/review_r5.py inputs` (cwd RV, rc 0).

```text
t0=100; bản lưu run 7=in_progress
chuan-bi.completed_at=20; gate-ops.completed_at=150
honest_in_progress: consistent=false
fabricated_extra_row: consistent=true, exact_inventory=false
hide_eligible_source_with_completed_failure: consistent=true
missing_run: false; honest_completed: true  (hai đối chứng)
```

[Output](review-evidence/20261120T170151588163.txt), [fixture](thu/raw-input-model.json). Đây là mô hình REST có các trạng thái/thời gian tách biệt, không phải phản hồi LIVE.

**Hướng sửa:** định nghĩa đối chiếu hai chiều inventory và identity/trường lựa chọn của từng ứng viên đã đọc; không suy `completed` từ một job con. Chốt t0 theo từng request/trang và phân biệt trạng thái có thể chứng minh ở t0 với trạng thái chỉ biết sau đó. Thêm đối chứng dương run có một job đã xong và một job còn chạy, cùng các đột biến thêm id/đổi conclusion hoặc attempt của run bị loại. Nếu API không cho chứng minh một chuyển trạng thái lịch sử, khai giới hạn hoặc đổi dữ liệu thu thay vì kết luận bản lưu trung thực sai.

### T2 — P2 — Đơn vị được ghim chưa chứa toàn bộ logic quyết định

**Vị trí:** `SPEC-B1-r4.md:54–64`, `:199–201`, `:221–225`, `:249–251`; `SPEC-B2-r4.md:86–87`, `:147–159`.

Hàm thuần của B1 còn nạp `ci_dang_ky_test.py` theo đường dẫn hiện hành. `ke_hoach` phụ thuộc `NHE`, `VUNG_CHUNG`, `VUNG_THEM`, `TIEN_TO_CHUNG`, `TIEN_TO_THEM` và helper. Chúng không trở thành bất biến chỉ vì các SHA đầu vào Git bất biến. B2 phát lại hàm tại head đang chạy, trong khi chỉ **I7** ghi rõ nạp registry tại M. Vì thế cùng `dau-vao/`, cùng mã hàm quyết định và cùng `PHIEN_BAN_QUYET_DINH` có thể cho quyết định khác khi registry tại head đã thay đổi.

**Lệnh:** `python -S out/review_tools.py python out/review_r5.py purity` (cwd RV, rc 0). Probe dùng fixture Git rename cũ và các hàm registry thật. Chỉ trên bản sao trong `out/`, thay chính sách `TIEN_TO_THEM` của `_PTG` từ `scripts/` sang `src/`; giữ nguyên dữ kiện SHA, diff và thân hàm gọi:

```text
input_sha256=4342b84b1162b04de42dca564b4b8a6672fde5f427de2270fcb101d6be72cc0c
decision_function_source_unchanged=true
decision_before=false; decision_after=true
```

[Output](review-evidence/20261120T170151941234.txt), [registry bản sao](thu/registry-different-policy.py). Đây là thay đổi dependency để chứng minh tính phụ thuộc, không sửa registry của kho.

Ca `hash(inspect(source)) == BAM_QUYET_DINH` cũng chỉ chứng minh một snapshot nhất quán với chính hằng của nó. Mô hình đổi source **và** cập nhật BAM nhưng giữ version 1 cho thấy cả hai snapshot đều qua phép ấy. Spec chưa định nghĩa bảng bất biến version→digest hay phép so lịch sử để hiện thực lời hứa “đổi logic mà không tăng phiên bản thì đỏ”. Đây là giới hạn của thước hash, không giả định executor cố ý vô hiệu test.

**Hướng sửa:** xác định trọn dependency của quyết định; nạp code và bảng chính sách tại M qua OID đã xác thực, hoặc đưa chúng thành đầu vào có nguồn rõ ràng. Ghim version với digest của toàn đơn vị đó và quy tắc so lịch sử. Thử cùng dữ liệu với working tree registry khác, có/không object, và thay dependency mà giữ version; kết quả phải đúng hợp đồng đã chọn. Việc tái tính Git cục bộ có thể tất định khi đủ object và môi trường Git được quy định; nó không tự giải quyết dependency Python ngoài đầu vào.

### T3 — P2 — Ưu tiên rc 1 làm mất “chưa đo được” khỏi D0

**Vị trí:** `SPEC-B2-r4.md:164–181`, `:208`, `:254–255` (D2.33–34).

Mục h chọn rc 1 nếu một lượt vừa có sai vừa có nguồn không đọc được. Nhưng e chỉ đếm **rc==2**, còn c/d chỉ đếm phiên bản hiện hành. Vì vậy một lượt phiên bản cũ có lỗi schema và một nguồn còn thiếu được tính rc 1, không vào c/d/e. Thêm 20 lượt tốt phiên bản hiện hành thì D0 đạt dù nguồn trong toàn lịch sử chưa được kiểm. Bản ghi có phiên bản không xác định cũng có cùng lỗ nếu được xử lý như “khác phiên bản”.

Ngay ca bắt buộc D2.33 đã không khớp công thức: artefact mất + H còn + job nhóm đỏ phải có cả lỗi thiếu nguồn và `VI_PHAM_Q8`; mục h cho rc 1 ⇒ e=0, trong khi D2.33 đòi e=1 và b=1. b vẫn chặn ca này, nhưng e đang không mang nghĩa “mọi lượt chưa xác minh”.

**Lệnh:** `python -S out/review_tools.py python out/review_r5.py history` (cwd RV, rc 0).

| Cùng 20 lượt tốt phiên bản 2, thêm lượt đầu | a | b | c | d | e | D0 |
|---|---:|---:|---:|---:|---:|---|
| Phiên bản 1, chỉ thiếu nguồn, rc 2 | 20 | 0 | 0 | 0 | 1 | false |
| Chính lượt đó thêm lỗi schema; h đổi rc thành 1 | 20 | 0 | 0 | 0 | 0 | **true** |
| Lượt đỏ mất artefact, H còn | 20 | 1 | 0 | 0 | 0 | false, nhưng khác e=1 của D2.33 |
| Lượt đỏ mất cả log/artefact | 20 | 0 | 0 | 0 | 1 | false |

[Output](review-evidence/20261120T170126497584.txt), [các lịch sử](thu/q8-r4-scenarios.json).

**Hướng sửa:** lưu các cờ độc lập `sai`, `lech_ham`, `thieu_nguon`, `vi_pham_q8`; rc chỉ là cách trình bày/exit status. e phải đếm cờ thiếu nguồn trên toàn bảng, dù rc là 1; version chưa xác minh không được loại khỏi điều kiện toàn cục. Sửa D2.33 và thêm ca lỗi hỗn hợp ở phiên bản cũ/không xác định. Không cần quay lại cửa sổ trượt.

### T4 — P2 — I1–I7 không đủ để kiểm độc lập Q1, và phạm vi áp dụng chưa nhất quán

**Vị trí:** `SPEC-B2-r4.md:149–159`; đối chiếu `SPEC-A-r4.md:230–248`, `SPEC-B1-r4.md:204–225`.

Q1 yêu cầu PR nguồn ở làn `day_du`. I2 được gắn nhãn “Q1, Q2” nhưng chỉ kiểm cha M/before. I4 kiểm kho/path/conclusion/attempt/ảnh, không kiểm làn. I5 kiểm job success, vốn có thể success dù các bước nặng bị bỏ theo chế độ. I6 kiểm blob bằng nhau; I7 chỉ áp cho nhanh. Vì vậy lỗi logic bỏ phép kiểm làn của 4d có thể được **chính hàm lỗi đó** phát lại thành công, trong khi cả bảy bất biến đều đúng. Ca ghim chứng minh đang dùng cùng hàm, không chứng minh hàm đúng Q1.

**Lệnh:** `python -S out/review_tools.py python out/review_r5.py contract` (cwd RV, rc 0).

```text
che_do_pr=duong_nhanh; groups=[ops]; các identity/cha/cây/blob/ảnh đúng;
job nguồn success; cùng hàm lỗi đã ghim được phát lại;
I1_I7=[true,true,true,true,true,true,true]
Q1_source_full=false; listed_invariants_accept=true
```

[Output](review-evidence/20261120T170127900334.txt), [fixture bất biến](thu/invariants-r4.json). Không tuyên bố một run GitHub như vậy đã xảy ra; đây là phản chứng cho độ phủ của checker độc lập mà spec đang hứa.

Ngoài ra I3/I4/I6 được viết vô điều kiện ở nhánh x=success. Với `khong_xet` hoặc `khong_tai_dung` không có nguồn, các object/ảnh/source là null; với fallback do ảnh khác, I4 không đúng. Nếu thực hiện nguyên văn thì các đối chứng rc 0 ở D2.29–30 đỏ. Review hiểu ý định là áp chúng khi đang nhận một tập tái dùng khác rỗng; cần ghi rõ, không để executor tự chọn giữa hai câu mâu thuẫn.

**Hướng sửa:** lập bảng bất biến theo trạng thái và theo Q, thêm làn PR/push cùng nguồn xác thực của chúng; Q4 phải có kiểm riêng về điều kiện job/bước và gate vẫn chạy, không gắn nhãn Q4 chỉ từ blob equality. Đột biến hàm vẫn trả cùng quyết định sai khi replay phải bị checker độc lập bắt. Q6 giữ nghĩa vụ bốn mốc riêng như B2 đã khai; không cần nhét nó vào hàm quyết định.

### T5 — P2 — Chưa ràng M trong chứng cứ với commit của run push đang kiểm

**Vị trí:** `SPEC-B2-r4.md:121–146`, `:152–159`; `SPEC-B1-r4.md:189`, `:196–200`, `:236–239`.

Mục a kiểm event/branch/path/status; d kiểm run_id và có trường M; e đối chiếu env chỉ nêu before/che_do/GITHUB_REF rồi “git: tính lại từ SHA”. Chưa có phép buộc M của bản ghi/đầu vào bằng `head_sha` của REST attempt push hoặc `github.sha` độc lập của đúng job. Tự tính cha/cây/blob từ một SHA có thật chỉ chứng minh object đó, không chứng minh run này đã dùng nó.

**Lệnh:** `python -S out/review_tools.py python out/review_r5.py identity` (cwd RV, rc 0). Fixture Git thật có hai merge commit cùng before=P1, cùng blob workflow và blob hằng mode/version, nhưng P2/cây khác. Bản ghi trỏ merge nguồn, REST/env SHA mô hình trỏ merge thực của push:

```text
record.M=5e304ca6817a958b9ede5e11653e093bd1657462
REST.head_sha=cd8fc54ff281206eb223606560a0086e264c2b00
I2=true; I3=true; I6=true; same_mode_version=true
record_tree != actual_tree; required_M_binding=false
```

[Output](review-evidence/20261120T170445841649.txt), [fixture và đường dẫn repo](thu/push-identity.json). Git/object là thật; REST và các quan sát job là mô hình. Lỗ nằm trong hợp đồng xác thực B2, không phải một tuyên bố rằng Git có thể đổi nội dung dưới cùng SHA hoặc Actions đã chạy sai commit.

**Hướng sửa:** neo trước tiên `(repo, run_id, attempt, event, path, head_sha)` của lượt push; buộc M bằng SHA ấy rồi mới đọc constants/blob/Git. Quy định nguồn cho từng raw input, gồm SHA, repository, ref và làn; không dùng “tính Git từ SHA” thay cho neo SHA với run. Thêm đột biến M sang một merge hợp lệ khác có cùng before/workflow/version và đổi đồng bộ các trường suy ra.

Một tiền đề liên quan còn chưa được chứng minh: YAML r4 được phép bởi B1 truyền `BEFORE`, `SHA`, `CHE_DO`, `ImageOS`, `ImageVersion`, nhưng không khai `GITHUB_REF` trong `env` bước xét; B2 lại muốn đọc giá trị đó từ khối env được in. `inputs` ghi `explicit_ref_present=false`. Cần chỉ định một alias được truyền rõ qua env hoặc nguồn REST tương ứng và fixture log chứng minh cách đọc. Không nên chờ B1 tích luỹ lịch sử rồi mới phát hiện thiếu kênh chứng cứ. Đây là phần cần chốt của hợp đồng đầu vào, chưa phải phép đo LIVE về cách Actions in biến ngầm định.

### T6 — P3 — Bảng consumer thiếu một tệp và xếp sai một consumer có đọc dữ liệu

**Vị trí:** `SPEC-B1-r4.md:108–124`, `:335–339`; `SPEC-B2-r4.md:71–72`.

Chạy lại chính phạm vi grep đã công bố cho ra **22 tệp mã**, 4 workflow ngoài `ci.yml`, không phải 21. Thiếu `ops/ci_duong_nhanh.py`: đây đã là tệp trong write set; hiện có đường dẫn workflow trong `PHU_THUOC_PACKET_LOOP` và các tham chiếu mô tả hợp đồng, nên lỗi kiểm kê này không chứng minh cần thêm một tệp sửa mới.

Bảng còn xếp `ops/specs/wp1434-r3/do/thu_thap.py` vào “chỉ nhắc trong chú thích hay tài liệu”. Thực tế `M4_CI` tại :1491, `m4_quet` tại :1037 và `m4_doi_chieu` tại :1524 phân tích lời khai trong bytes workflow đã chụp, so với đo lường. Hàm `m4_quet` thật nhận nội dung ci.yml nền và trả 13 hàng. Đây là công cụ phân tích bằng chứng, không phải gate chặn YAML r4, nhưng mô tả consumer đang sai.

**Lệnh:** `python -S out/review_tools.py python out/review_r5.py consumers` và `... extra_consumer` (cwd RV, rc 0).

```text
REAL_CONSUMER_SEARCH: code_count=22, other_workflows=4
REAL_RESEARCH_CONSUMER: reads_actual_workflow_claims=true, rows=13
```

[Tập tệp và phép đo](review-evidence/20261120T165841585579.txt), [consumer nghiên cứu](review-evidence/20261120T170257265046.txt), [ngữ cảnh từng kết quả grep](consumer-context.json), [hai hàm M4](thu-thap-consumer.json).

**Hướng sửa:** bổ sung hàng thiếu, sửa vai trò thu_thap và số đếm, phân biệt gate với công cụ đọc snapshot. Giữ phép so tập tệp, không chỉ số lượng. C7/D6 cần xét lại khi consumer xuất hiện hoặc đổi loại. Chưa thấy consumer ngoài write set đỏ trên các phép được yêu cầu.

### T7 — P3 — B1 dùng 600 như trần đã xin, trong khi khối nâng trần xin 650

**Vị trí:** `SPEC-B1-r4.md:31–37`, `:155–158`, `:286–289`.

Bảng 12 khối cộng đúng 600 dòng. `tran_moi` là 650, nhưng luật dừng ghi “trần của khối nang_tran (600 dòng thêm)”. Một diff 625 dòng sẽ vừa ở dưới trần xin vừa phải dừng theo mục 5. Đây là con số làm thay đổi điểm hỏi E2, không chỉ phép làm tròn ước lượng.

**Lệnh:** `python -S out/review_tools.py python out/review_r5.py sizes` (cwd RV, rc 0): `B1 total=600; requested=650; stop=600`. B2 đối chứng: `total=485; requested=550; stop=550`. [Output](review-evidence/20261120T170151160280.txt).

**Hướng sửa:** phân biệt ước 600 với trần xin 650 ở mọi chỗ; luật dừng dẫn một nguồn trần duy nhất, chỉ áp sau duyệt hợp lệ. Các khối `nang_tran` đều có đủ bốn trường, có căn cứ tách/không tách; review không coi đó là thẩm quyền đã được cấp, cũng không hứa dự toán sẽ đủ khi triển khai.

### T8 — P3 — B2 đặt mốc hỏi E2 sớm chưa gắn với thiếu tài nguyên; còn câu duyệt thiếu mã

**Vị trí:** `SPEC-B2-r4.md:269–271`, `:291–295`; chuẩn `cay-kho/.claude/skills/soan-spec/SKILL.md:127–144`, `cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md:27`.

E2 đòi chạm trần cứng hoặc thiếu tài nguyên/quyền. B2 yêu cầu hỏi ngay khi lịch sử còn ≤14 ngày mà D0 chưa đạt, dù chưa chứng minh thiếu thời gian lưu. Ví dụ có 19 lượt tốt, còn 14 ngày, tốc độ một lượt/ngày: thiếu một lượt, ước một ngày, không chạm trần và không thiếu thời gian, nhưng câu hiện tại vẫn bắt hỏi E2. Mã E gắn vào câu không tự biến mốc 14 ngày thành một điểm hỏi được ADR đặt ra.

Câu đầu mục luật dừng (:269–270) còn nói chủ kho duyệt băm nhưng không mang mã E. E2 ở câu kế nói về vượt trần; E5 ở mục 6 không làm câu này tự có mã theo yêu cầu L7. B1 đã có cách viết E2 gộp E5 ngay câu tương ứng.

**Lệnh:** `python -S out/review_tools.py python out/review_r5.py l7` (cwd RV, rc 0).

```text
first_sentence.codes=[]
a=19; remaining_days=14; estimated_missing_days=1
hard_limit_reached=false; resources_insufficient=false; r4_asks_E2=true
```

[Output](review-evidence/20261120T170548992253.txt), [câu chữ và bảng E](review-evidence/20261120T170257743302.txt).

**Hướng sửa:** để 14 ngày là mốc tự đo/báo nội bộ; chỉ hỏi E2 khi phép so thời gian cần với hạn còn lại hoặc giới hạn cụ thể chứng minh thiếu tài nguyên/quyền. Gắn E2/E5 cùng dẫn hồ sơ ngay câu duyệt băm. Các payload E1/E2/E3/E5 khác đã nêu đủ; không cần thêm một lần xin phép cho phiên review này.

## Bảng consumer: phép đo từng hàng trên YAML r4

| Hàng B1 mục 0 | B1 r4 | B2 r4 | Cách kiểm và giới hạn |
|---|---|---|---|
| `ops/ci_duong_nhanh_test.py` | 15/15 | 15/15 | `pins`, gọi guard thật sau đúng các họ cập nhật; y15 kiểm loader không nằm trong 15; mutant nới if/env/y06 vẫn đỏ |
| Hai tệp Windows | t32 tương đương rc 0 | t32 tương đương rc 0 | Trích nguyên AST 5 hàm so và bảng ghim; chỉ thay chọn Python để dùng `-S`; chưa chạy toàn suite Windows |
| `ci_dang_ky_test.py` | Các helper không lỗi | Không lỗi sau các cập nhật B2 đã liệt kê | `loi_gate_nhanh`, `loi_vung_thiet_lap`, `loi_g5_workflow`, `loi_ruff_ci`; `loi_workflow_dot_bien_du` thật rỗng trên cả ba YAML |
| `lease_publish_test.py` | t31/t161/t162 đạt | t31/t161/t162 đạt | Chạy nguyên hàm ca và helper bằng AST trên thư mục bản sao các workflow; các dòng “KHÔNG ĐO ĐƯỢC” trong output là fixture âm của t162, không phải nền lỗi |
| `cong_cu_test.py` | t6 đạt | t6 đạt | Hàm thật, YAML và bản kê công cụ trong out; bước mới vẫn sau G5 |
| `scripts/tl_selftest.py` | ok3=true | ok3=true | Áp đúng predicate thứ tự core.abbrev/fetch-depth/doc-claims-check, không tuyên bố chạy toàn selftest |
| `launcher_test.py` | 5 chỗ 1.7.7 | 5 chỗ 1.7.7 | Predicate ghim trong t152; so với version ở hook thật, không chạy phần hook có thể cài công cụ |
| `packet_loop.py`, `packet_loop_test.py`, `ci_provenance_test.py`, `chon_reviewer_test.py`, `gate_lifecycle.py` | Không có parser job/bước thực trong các hit này | Như B1 | Đọc các định nghĩa check/path và fixture tổng hợp; tên check không đổi |
| `launcher.py`, `session-start.sh`, `bien_nhan_v2.py`, `bien_nhan_v2_test.py`, `cai_actionlint.sh`, `codex_cloud_setup.sh`, `cong_cu.py` | Không có predicate YAML mới bị tác động | Như B1 | Đọc các hit; launcher còn có chuỗi hướng dẫn cài PyYAML, không phân tích job ci.yml |
| `ops/specs/wp1434-r3/do/thu_thap.py` | Bảng mô tả sai loại | Như B1 | T6; công cụ đọc snapshot/claim thực, không phải guard của YAML. Không chạy nhánh thu mạng |
| 4 workflow khác | Không lỗi phép so liên quan | Không lỗi | Các hit là chú thích; weekly đối chiếu bằng helper thật ở hàng registry |
| Tệp bị bỏ sót `ops/ci_duong_nhanh.py` | Kiểm kê thiếu | Kiểm kê thiếu | T6; classifier/tuple dependency thật, không có consumer hình dạng job mới trên nền |

Phép grep độc lập dùng `git grep -l -E 'workflows/ci\.yml|ci\.yml' HEAD -- '*.py' '*.ps1' '*.sh' '*.yml'` cùng loại trừ `ops/reviews/**`, `ops/land/**`, `.codex/**`. Tập kết quả gồm 27 đường dẫn: 22 mã + ci.yml + 4 workflow. Đây là kiểm kê trong phạm vi truy vấn công bố; không suy rằng mọi consumer động của một YAML bất kỳ trong kho đều chứa literal `ci.yml`.

## Đối chiếu thiết kế mới

| Nghĩa vụ A | B1 / B2 r4 | Đánh giá |
|---|---|---|
| Q1: push đúng phạm vi, PR nguồn đầy đủ, nhóm xanh | B1 4a/4c/4d/4f; I2/I4/I5 | B1 đã có điều kiện; checker độc lập thiếu làn, T4 |
| Q2: hai cha, before, source checkout/tree, merge-tree | B1 4b/4d/4e; I2/I3 | Object bundle đóng phản chứng cũ; còn neo M với run push, T5 |
| Q3: kho/workflow/attempt/ảnh/tập shard | B1 4c/4d/4f; I4/I5 | Inventory nguồn đúng thiết kế; snapshot lựa chọn và dependency nguồn còn T1; ảnh/log LIVE chưa đo |
| Q4: gate vẫn chạy, không if theo event/ref trong nhóm | Ca YAML B1 C3; B2 giữ gate, thêm bước kiểm | Nền và YAML chứng kiến không có if event/ref trong tám job nhóm; I6 chỉ chứng minh blob, không tự là phép kiểm Q4 |
| Q5: lỗi chung ⇒ không nhóm nào; lỗi nhóm ⇒ loại nhóm | Hai tầng, COE/outcome, C2; replay | Output sau lỗi đóng; độ đúng của replay còn phụ thuộc T1/T2/T4/T5 |
| Q6: bốn mốc cho push và PR khi landed | B2:41–42 tách rõ | Không dùng rc 0 replay thay hồ sơ land; LIVE chưa đo |
| Q7: kế hoạch thật bằng nhau | B1 4g; B2 I7 tại M | Phản chứng rename bị bắt; tính tất định toàn hàm còn T2 |
| Q8: ≥20 bóng và không vi phạm | B2 lịch sử toàn bộ, đếm theo version | Bỏ cửa sổ là tiến bộ có thật; lỗi cờ tổng hợp T3 vẫn cho xanh sai |

**Dòng `TAI_DUNG_AP_DUNG`.** Trên YAML r4, env BO bằng nguyên biểu thức output tương ứng của B1/B2; chỉ success/success có tập khác rỗng. Không có job đọc `_bong`; gate không bị gắn vế bỏ nhóm; tám job nhóm mới mang vế đó. S5 được đóng ở mô hình outcome. Chưa có chứng cứ LIVE để khẳng định dòng log luôn bằng output job đã được Actions truyền cho các job sau, đặc biệt khi hủy run hoặc không còn log. D4 và D5 vẫn là điều kiện chưa đo, không được tính đạt từ probe YAML.

**`env:` và `Runner Image`.** Không có fixture log thật của kênh này trong vật liệu review. B2 công khai D4(iii) chưa đo, vì vậy review không tự dựng fixture rồi gọi nó là dữ liệu runner. Cần chốt nguồn/alias GITHUB_REF như T5; với ảnh, cần chốt cách trích và ánh xạ nhãn Image trong log với giá trị `ImageOS`, cùng trường Version. Bằng nhau giữa hai chuỗi chưa được định nghĩa chuẩn hóa không đủ để kết luận bằng nhau giữa hai biến runner. Không kết luận đã có lỗi LIVE về tên ảnh, hoặc đã xác minh ảnh từ tài liệu mạng.

**Lịch sử và retention.** Quy tắc toàn lịch sử chặn được mất artefact/log đơn lẻ thay vì bỏ qua chúng. Nhưng chưa nên gọi lịch sử là bất biến: `overwrite: true` của artefact PR có thể làm lần tải lại không còn hiện vật attempt 1 sau rerun; retention cũng làm mất nguồn. Spec đã khai đường E1 khi nguồn mất, không phải đường tự động đạt. Trước B1 land cần đo đường đọc lại theo id/attempt và quyết định bảo tồn nguồn cần thiết; hiện review không có API để chứng minh nguồn ấy còn tồn tại. Băm một bảng đã in không tự lưu inventory hoặc biến nguồn ngoài thành bền. Các giới hạn này không được dùng để bỏ hàng hoặc giảm e, và T3 phải sửa trước bật.

## Trích dẫn, lời khai về mã, L1–L7

Đã trích và đọc **46 vị trí dẫn rõ số dòng**: A 10, B1 10, B2 26, tất cả tồn tại và khớp chủ thể được dẫn trên HEAD. [Bảng đầy đủ gồm nguyên văn từng đoạn](citation-audit-r5.json), [output audit](review-evidence/20261120T170125698620.txt). Phép đếm “in_bounds” chỉ kiểm vị trí; kết luận khớp nghĩa còn dựa vào các đoạn mã và phép gọi thật nêu trong bảng consumer. Lời khai “21 tệp mã” và “thu_thap chỉ chú thích” không đúng, T6.

Các lời khai còn lại đã đối chiếu: registry import yaml tại :24; `doc_diff` trả None và kế hoạch None vẫn hợp lệ; m lấy đúng env registry; `goi_that` trả status/bytes và không chở token sang URL chuyển hướng; Windows bỏ riêng chuan-bi; nhóm có lần lượt 9/1/10/17 instance Ubuntu; y06 khóa required jobs; t6 khóa phần trước G5; ci_duong_nhanh_test chỉ chạy ở nhánh Linux của job CI; push luôn chạy packet-loop; sáu vị trí cổng của A chưa đọc ADR-0068. Dữ liệu thời gian nhóm lấy từ bảng đã lưu, không phải đo CI mới.

Numstat tham chiếu: `7e5958e` có +618 dòng `ci_duong_nhanh.py`, +3608 test; `b8bc64f` cộng +226 trong bốn tệp liên quan, đúng lời dẫn B1. JSON 60 lượt có 28 xanh đầy đủ; trung vị wall 30.35, runner 266.5 từ số đã làm tròn trong JSON; báo cáo đo gốc ghi 30.4 và 266.1. Không nhầm hai độ chính xác ấy thành phép đo REST mới. Các tổng nhóm 146.4/25.3/33.1/41.7 là **cộng trung vị từng job**, đúng đơn vị đặc tả. Các số lease/server và log runner không thể kiểm lại LIVE trong phạm vi không mạng; không xác nhận lease hiện còn hiệu lực hay origin/master máy chủ.

| Luật | A r4 | B1 r4 | B2 r4 |
|---|---|---|---|
| L1: đơn vị đếm | Đạt các phép A | Các số khối có đơn vị; số consumer sai T6, trần lẫn ước T7 | 485 và 550 phân biệt đúng; định nghĩa e có lỗi T3 |
| L2: write set kham mục tiêu | Hai đường dẫn, A5 đo được | Năm đường dẫn nay gồm Windows; không tìm thấy guard đỏ cần sửa ngoài write set | Sáu đường dẫn gồm registry/Windows; các cập nhật kiểm được |
| L3: phép đỏ, đột biến | Nền/ứng viên/19 đột biến và reflow đã chạy | Có ca outcome/bundle/YAML; lời hứa ghim phiên bản chưa có thước đủ, T2 | Thước D0, độc lập I và ca D2 còn T1/T3/T4/T5 |
| L4: kế thừa hình dạng lỗi | Giữ như lượt 4 | Có số lần 4/3/4 và phương án xử lý mới | Có số lần 4/3/4; review này không reset vì đổi thiết kế |
| L5: thời điểm, neo và đo lại | Neo HEAD/băm; số đo có nguồn ngày | Ước và cap phải sửa T7; consumer đo lại ra khác T6 | Có thời điểm; LIVE trước cấp/merge chưa có, không được khai đã đạt |
| L6: kiểm chính thước đo | Ca A vẫn bắt các phản chứng cũ | Predicate YAML và mutant hẹp đã kiểm; C5/C6 khai chưa LIVE | Ca D2.33 trái công thức e, T3; schema/input cần đột biến T1/T5 |
| L7: điểm hỏi và mã E | Không thấy lỗi mới | Payload E1/E2/E5 đủ; trần sai gây điểm dừng sai T7 | T8: ngưỡng 14 ngày chưa đủ điều kiện E2; một câu thiếu mã. Payload các điểm còn lại đầy đủ |

Payload đã đọc với bảng ADR-0067: E1 gồm gốc rễ, các cách đã thử/vì sao hỏng, đề xuất; E2 gồm mức dùng, thiếu bao nhiêu, mục đích (các câu xin lời gọi dùng finding còn mở làm mục đích); E3 của B2 nêu hai quyết định 20-11, bằng chứng, hậu quả; E5 ở cả ba spec nêu diff/lý do/quyền thay đổi. E4 đều khai không chạm. Quét [các đoạn L7](l7-audit-r5.json) chỉ là chỉ mục; việc nhận mã ở cùng đoạn dài không thay cho kiểm **từng câu**, như T8 minh họa.

## Bảng lệnh đã chạy

Mọi lệnh dưới đây có output đầy đủ và timestamp trong [commands.jsonl](review-evidence/commands.jsonl). `RV` = `C:\r\d2`, `REPO` = `C:\r\d2\cay-kho`. Các lần `Get-Content`, `rg` đọc tài liệu và sao chép harness trước khi có logger chỉ phục vụ đọc/chuẩn bị; không có mutation ở nguồn. Bảng này ghi các phép kiểm, không coi việc tạo fixture là thi hành packet.

| Lệnh | cwd | rc | Kết luận / output |
|---|---|---:|---|
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'anchor'` | RV | 0 | Băm, HEAD/tree/ref, ADR hiệu lực, numstat và 60 lượt đã lưu. [log](review-evidence/20261120T165825750959.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'pins'` | RV | 0 | 15/15 cho B1/B2 r4 sau cập nhật; mutant hẹp bị bắt; helper registry/t6. [log](review-evidence/20261120T165829090254.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'consumers'` | RV | 0 | 22 mã + 4 workflow; t31/t161/t162, ok3, AL_VER, weekly đạt. [log](review-evidence/20261120T165841585579.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'windows'` | RV | 0 | t32 tương đương rc 0 sau cập nhật Windows của từng packet. [log](review-evidence/20261120T165904273635.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r3.py' 'a_check'` | RV | 0 | Nền đỏ, ứng viên xanh; 19 đột biến nội dung đỏ; reflow xanh; A1/A7 có răng. [log](review-evidence/20261120T165905439158.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r2.py' 'rename'` | RV | 0 | Git và registry thật: before=P1 nhưng kế hoạch PR/push khác. [log](review-evidence/20261120T165927129683.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'audit'` | RV | 0 | 46 citation và đoạn L7; inventory, Q4, sáu vị trí cổng, dependency yaml. [log](review-evidence/20261120T170125698620.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'history'` | RV | 0 | S3 cũ bị chặn; T3 cho D0=true khi lỗi rc 1 che thiếu nguồn phiên bản cũ. [log](review-evidence/20261120T170126497584.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'contract'` | RV | 0 | S4/S5 cũ được sửa trong mô hình; T4 thiếu Q1 và phạm vi I3/I4/I6. [log](review-evidence/20261120T170127900334.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'provenance'` | RV | 0 | Bundle thật chặn đuôi SHA giả, một cha và blob workflow lệch. [log](review-evidence/20261120T170130856488.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'sizes'` | RV | 0 | Tổng B1=600, xin 650, stop 600; B2=485/550/550. [log](review-evidence/20261120T170151160280.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'inputs'` | RV | 0 | T1 snapshot trung thực bị bác, hàng sai lọt; env/identity T5. [log](review-evidence/20261120T170151588163.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'purity'` | RV | 0 | Hàm registry thật thay dependency làm đổi quyết định với cùng đầu vào. [log](review-evidence/20261120T170151941234.txt) |
| `python -S out/review_tools.py 'rg' 'workflows/ci\.yml&#124;ci\.yml' '.claude/dev/packet_loop.py' '.claude/dev/packet_loop_test.py' 'ops/ci_provenance_test.py' '.claude/dev/chon_reviewer_test.py' '.claude/dev/gate_lifecycle.py' '.claude/dev/launcher.py' '.claude/hooks/session-start.sh' 'ops/bien_nhan_v2.py' 'ops/bien_nhan_v2_test.py' 'ops/cai_actionlint.sh' 'ops/codex_cloud_setup.sh' 'ops/cong_cu.py' 'ops/specs/wp1434-r3/do/thu_thap.py' '.github/workflows/ci-dot-bien-du.yml' '.github/workflows/launcher-windows.yml' '.github/workflows/ops-publish-lease.yml' '.github/workflows/ops-thu-hoi-admission.yml'` | REPO | 0 | Đọc từng hit của các hàng consumer được xếp không phân tích YAML. [log](review-evidence/20261120T170204830689.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'extra_consumer'` | RV | 0 | Hàm M4 thật đọc 13 claim từ ci.yml; không chỉ chú thích trong consumer. [log](review-evidence/20261120T170257265046.txt) |
| `python -S out/review_tools.py 'read' 'SPEC-B2-r4.md@260:301' 'cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md@19:45' 'cay-kho/.claude/skills/soan-spec/SKILL.md@31:149'` | RV | 0 | Đối chiếu câu luật dừng, bảng E và L1–L7. [log](review-evidence/20261120T170257743302.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'regression'` | RV | 0 | A5, F7, N6/N7, outcome 4×4; năm bước, 24<30 phút, BO bằng output. [log](review-evidence/20261120T170305955403.txt) |
| `python -S out/review_tools.py 'python' 'out/review_probes.py' 'policy_probe'` | RV | 0 | Push hồ sơ vẫn nhanh và packet-loop chạy; sáu vị trí cổng không marker mới. [log](review-evidence/20261120T170405096793.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'identity'` | RV | 0 | Hai merge Git hợp lệ khác cây; I2/I3/I6 đúng nhưng M khác REST head_sha. [log](review-evidence/20261120T170445841649.txt) |
| `python -S out/review_tools.py 'python' 'out/review_r5.py' 'l7'` | RV | 0 | Câu thiếu mã; mốc 14 ngày hỏi E2 dù chưa thiếu tài nguyên. [log](review-evidence/20261120T170548992253.txt) |
| `python -S out/review_tools.py 'git' 'status' '--porcelain'` | REPO | 0 | Cây kho sạch cuối phiên. [log](review-evidence/20261120T170549467057.txt) |
| `python -S out/review_tools.py 'hash' 'SPEC-A-r4.md' 'SPEC-B1-r4.md' 'SPEC-B2-r4.md'` | RV | 0 | Băm ba spec cuối phiên không đổi. [log](review-evidence/20261120T170549600458.txt) |

Không chạy mạng, actionlint/shellcheck của runner CI, toàn bộ suite Ubuntu/Windows, C5/C6 hoặc D0/D4/D5 LIVE. Các tiêu chí đó vẫn chưa đo; các probe được giới hạn đúng hàm/predicate được báo, không dùng rc harness để thay một cổng triển khai.

## Kết luận

A r4 tiếp tục đủ điều kiện approve riêng về đặc tả. B1/B2 có cải thiện đo được: Windows đã vào write set, bundle chặn SHA/subject giả cũ, I7 chặn hai kế hoạch khác, outcome phân biệt ý định với áp dụng, lịch sử không còn cửa sổ trượt. Tuy nhiên T1–T5 vẫn là P2 mở trong chính thiết kế kiểm lại/bật; T6–T8 là P3 mở. Cần sửa các hợp đồng ấy và chạy lại đúng phản chứng nêu trên trước khi approve toàn bộ.

KET_LUAN: changes_requested
