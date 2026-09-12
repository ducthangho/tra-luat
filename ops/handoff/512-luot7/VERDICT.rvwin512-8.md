verdict: changes_requested
reviewed_sha: 36f68c7e95e0de1fcf8e2311db33a164816db20f
reviewed_base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
reviewed_files_sha256:
  ops/lease_publish_test.py: 13a2af8ca8cd1d4571590f0e46c751eb0d7e6964790a0d53cdd5e0058a591f84
  ops/chay_lease_publish_test.sh: 87c760294763c71a67cfaee50a440e62b31c439beb0abbfcb5e34076d32be693
model_tu_khai: GPT-6 / Codex; khác họ Claude theo lời khai tác giả; không xác minh backend độc lập
review_round: 8
so_p1: 1
so_p2: 0
so_p3: 0
so_the_hien: 9
hint_sha256:
previous_hint_sha256: e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0

**changes_requested: còn một lớp F6 thuộc công cụ/hồ sơ ngoài write set.** PR không đổi byte. Full wrapper độc lập đạt **155/155 ở CHA, [A] và [B]**. Bản vá bộ đo đóng StopIteration, nhưng vẫn cấp tín dụng giả cho tên lớp Unicode và Exception có thông điệp rỗng; đồng thời làm sai chiều nhận chốt thật vốn được bản trước phân hạng đúng.

Đếm **một lớp theo mức cao nhất P1**, không nâng từng lỗi số thành P1 riêng. **Chín thể hiện mở** = F6.7–F6.10 (bốn phản chứng công cụ) + N31-b, N32-b, N37–N39 (năm lời khai số/đính chính chưa đủ). Các bản sao của cùng lời khai numstat được gom N32-b và chỉ rõ từng vị trí. Không tính lại 36 đại lượng vòng 7 đã đo khớp; không đếm F6.5/StopIteration hoặc F6.6 đã đóng.

Phát hiện đã được ghi tăng dần; giữ nguyên nhật ký tại [review-logs/VERDICT-journal.md](review-logs/VERDICT-journal.md). Không nộp HINT.patch: các sửa chữa còn yêu cầu thuộc hồ sơ riêng, không mở thêm write set của PR. Không quyết định merge, không approve thay chủ kho, không cấp hay nâng trần.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp | Trạng thái canonical | Căn cứ lượt 8 |
|---|---|---|
| F1 thu hồi cây | **ĐÃ VÁ THẬT** | Byte không đổi; t154 xanh trong CHA/A/B; mutant giết PID, bỏ session, bỏ guard nhóm đều chết đúng chốt. Phạm vi POSIX. |
| F2 bằng chứng sống | **ĐÃ VÁ THẬT** | Ba tổng kết dương đầy đủ; mutant tee cuối/bỏ nhãn/bỏ flush chết; N10 sống ở 353eae1, chết ở 36f68c7 vì thiếu bốn tee. |
| F3 selector | **ĐÃ VÁ THẬT** | t155 xanh trong full suite; bỏ guard selector bị bắt đúng lỗi rc=0 thay vì 3. |
| F4 ngân sách tổng | **ĐÃ VÁ THẬT** | t156 xanh; mutant cấp lại hạn, trả dở dang, hạn ngoài 420, bỏ hạn chẩn đoán đều chết đúng chốt. |
| F5 tắt đệm con | **ĐÃ VÁ THẬT** | t158 xanh cả ba lượt; M14 chết ở phép đo môi trường thực của hai vế. |
| F6 công cụ/hồ sơ | **VÁ SINH LỖI MỚI** | F6.5/StopIteration đã đóng; F6.7/F6.8 còn cấp tín dụng giả. F6.9 là hồi quy phân hạng: cùng chốt t96, bản vòng 6 nhận đúng, bản mới nhận sai. F6.10 và các số còn mở ở dưới. |
| F7 classifier/consumer/phản chứng | **ĐÃ VÁ THẬT** | Byte không đổi; t160 xanh; M15/M16/M17 và N01/N02/N17/N18 chết đúng chốt. N12 không dựng lại động trong lượt này; giới hạn riêng bên dưới. |

| Thể hiện vòng 7 bắt buộc | Trạng thái canonical | Đối chiếu cụ thể |
|---|---|---|
| **F6.5** | **ĐÃ VÁ THẬT** cho thể hiện StopIteration | Cùng control: VA_VONG6 cấp GIET THAT, bản mới trả TIN DUNG GIA. Không suy đã đóng lớp ngoại lệ vô can. |
| **F6.6** | **ĐÃ VÁ THẬT** | Đủ 16 tệp, bằng byte 16/16 hiện vật trên nhánh hồ sơ; đã có cả log thiếu và đủ ShellCheck. |
| **N31** | **VÁ HỜ** về độ đầy đủ đính chính | Sáu ID trong commit đã được đính chính đúng; câu “năm mutant” ở PROMPT vòng 7 chưa được điểm danh: N31-b. |
| **N32** | **VÁ HỜ** về độ đầy đủ đính chính | 399 đúng; 418 thuộc head cũ đúng. Các câu numstat cũ tại TRANG_THAI:38,96 vẫn trình bày số hạng sai mà đính chính chưa chỉ rõ: N32-b. Không đếm lại riêng 386 đã được đính chính. |

## BẢNG ĐO

| Phép đo | Kết quả độc lập | Hiện vật |
|---|---|---|
| Neo Git | HEAD đúng SHA; merge-base đúng bb7013c; detached; is-shallow=false; core.abbrev=7 | Kiểm Git đầu/cuối lượt; final-hygiene.json |
| Hai tệp write set | Hai băm đầu báo cáo khớp nguyên văn verdict vòng 7 | Băm trực tiếp |
| SPEC | SHA256 6af324a368550eda667c67315052cf4fe1a1fb861e2c0da77202163deb34d105, đúng mỏ neo | Băm trực tiếp |
| Diff/numstat được giao | Bằng byte `git diff bb7013c 36f68c7`; hai tệp, Python +1095/−27, shell +6/−0, tổng +1101/−27 | metadata.json |
| Gói hồ sơ | 16 tệp; 16/16 bằng byte nhánh ops/handoff-512-luot7 | artifact-package.json |
| Hai log tác giả | Log thiếu: ba 153/155, đúng t137/t159 đỏ ở mỗi lượt. Log đủ: ba 155/155, không đỏ | metadata.json |
| Công cụ | Python 3.11.15, ShellCheck 0.9.0, actionlint 1.7.7 từ gói ghim đúng SHA256 023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757 | full-suite-fixed-env.log; băm trực tiếp |
| Full wrapper **[A]** | **155/155 đạt; đã chạy=155, bỏ qua=0** | full-suite-fixed-env.log:1055 |
| Full wrapper **[B]** | **155/155 đạt; đã chạy=155, bỏ qua=0** | full-suite-fixed-env.log:1060 |
| Full wrapper **CHA** | **155/155 đạt; đã chạy=155, bỏ qua=0** | full-suite-fixed-env.log:1156 |
| Tính đầy đủ log reviewer | Mỗi lượt 155 dòng vào/155 dòng ra, cùng thứ tự tên; 0 đỏ, 0 bỏ qua; wrapper rc=0 | suite-positive.json; full-suite-fixed-env.rc |
| t125/t158/t160 ở CHA | 54.801s / 3.406s / 0.057s, đều QUA | suite-positive.json |
| Tự kiểm **cả ba** bản | MỚI 7/7 rc=0; VA_VONG6 5/7 rc=1; REGEX_CU 2/4 rc=1 | dotbien512*.tukiem.log và .rc |
| “VA_VONG6 khác một dòng” | Đúng: chỉ dòng tính vo_can khác; cùng bảy control | meter-one-line.diff |
| Catalog 16 trên HEAD | 16/16 giết thật, 0 tín dụng giả, 0 sống; tên/đích/phân hạng khớp cả hai log catalog tác giả | catalogue16.log và .rc |
| N01/N02/N10/N17/N18 cố định mẫu số | Cùng năm phép biến đổi: SỐNG 5/5 ở 353eae1; CHẾT đúng chốt 5/5 ở 36f68c7 | regression-mutants.json; regression-N18-fixed.json |
| ci_dang_ky_test | rc=0; đăng ký 21/21, phản chứng 51/51, TỔNG ĐẠT | ci-dang-ky.log và .rc |
| doctrine-scan | rc=0; “sạch — đã quét 7 tệp, 0 chỗ chép doctrine” | doctrine.log và .rc |
| adr-song | rc=0; 47 ADR trên đĩa/47 dòng §20, khớp 1–1; tha thiếu trạng thái 0016 theo chính tổng kết | adr.log và .rc |
| A5 đóng băng | **không đạt**: 1101>300; phép tính 1101≤1500 và dư 399 không thay nhãn A5 | SPEC và numstat |

Các hiện vật ngắn trong bảng ở `review-logs/`. Lần wrapper đầu bị tar từ chối đổi ownership, installer rc=5 trước khi chạy test. Lần hoàn tất dùng **TAR_OPTIONS=--no-same-owner**, TMPDIR/AL_DICH trong sandbox, AL_GOI là gói offline được giao, AL_VER=1.7.7. Không sửa installer, không bỏ kiểm băm hay phiên bản. Log lỗi đầu được giữ tại full-suite.log.

Chỉ dùng mã thoát và dòng tổng kết của hai lệnh doctrine/ADR theo ngoại lệ hẹp. Không tự mở các tệp bị cấm để đọc chỉ dẫn.

## Findings theo lớp

### F6 — công cụ/hồ sơ bằng chứng, một lớp P1

**F6.7 — định danh Unicode vẫn được cấp tín dụng giả.** Trong control có sẵn, đổi duy nhất tên lớp `Bung` thành `Bùng`, giữ thông điệp, câu raise, ca đích và đáp án. Python chạy bình thường; main in `Bùng: CONTROL vo can, ten lop khong theo quy uoc nao`. Bộ đo nhận **GIET THAT**, tự kiểm còn **6/7, rc=1**. `_DANG_VO_CAN` dùng `[A-Za-z_]`, nên không phủ mọi định danh Python như EVIDENCE/F6-HO-SO tuyên bố. Không cần thay `__name__` hay giả mạo tín hiệu.

Tái lập: [unicode-control.py](review-tmp/unicode-control.py), [unicode-control.self.log](review-logs/unicode-control.self.log); stdout/stderr thật trong `review-logs/unicode-control/`.

**F6.8 — thông điệp rỗng phá ngay cả tên built-in ASCII.** Xoá nội dung thông điệp của control Exception trần có sẵn. Main in `Exception: `, có dấu cách cuối. Tại `dotbien512.py`, phép lấy `chi_tiet_do` gọi `.strip()`, biến nó thành `Exception:`; regex đòi `: ` nên trượt. Kết quả **GIET THAT**, tự kiểm **6/7, rc=1**. Chốt hợp đồng vẫn có đủ cả hai mảnh nguồn và cho qua. Đây là lỗi giữa đầu ra main và bước chuẩn hoá trước regex, không phải thiếu một tên trong danh sách.

Tái lập: [empty-exception-control.py](review-tmp/empty-exception-control.py), [empty-exception-control.self.log](review-logs/empty-exception-control.self.log); log thô giữ nguyên khoảng trắng trong `review-logs/empty-exception-control/`.

**F6.9 — bản vá sinh lỗi ở chiều chốt thật.** Dùng nguyên assertion và thông điệp đã có tại `ops/lease_publish_test.py:3158–3159`; chỉ đảo boolean để làm control dương. Main nhận AssertionError thật, in `t96: khớp đúng nghĩa (bằng nhau tuyệt đối) bị từ chối`. Bộ đo vòng 6 nhận **GIET THAT, 1/1, rc=0**; bộ đo mới nhận **TIN DUNG GIA, 0/1, rc=1**, gọi sai nó là ngoại lệ vô can.

`t96: ` là tiền tố tên ca thông thường đã có trong cây, không phải chuỗi giả tên ngoại lệ do reviewer soạn. Fail-close ở đây làm từ chối bằng chứng đúng. Hai miền chuỗi “thông điệp assertion” và “tên lớp + thông điệp” giao nhau; nới regex thêm nữa không tự giải quyết được sự nhập nhằng ấy.

Tái lập: [positive-t96.py](review-tmp/positive-t96.py), [positive-t96.log](review-logs/positive-t96.log), [positive-t96-v6.log](review-logs/positive-t96-v6.log).

**F6.10 — tự kiểm chưa canh việc mất chốt hợp đồng.** Chốt nguyên bản có tác dụng: đổi dòng in ngoại lệ sang dòng `str(ex)` sẵn có trong bản sao làm bộ đo **CHAN, rc=1**. Nhưng:

- Bỏ lời gọi `_kiem_hop_dong_main(NGUON)` vẫn **7/7 tự kiểm, 16/16 catalog, rc=0**.
- Nới điều kiện `if thieu` thành False vẫn **7/7 tự kiểm trên HEAD, rc=0**.
- Dùng bản nới ấy trên cây **đã đổi hợp đồng main** vẫn **16/16 catalog, rc=0**.

Bảy control không chứa một ca chủ động làm mất hợp đồng và đòi chặn trước catalog. Phép thử đổi main được tác giả khai đã chứng minh nhánh chặn đang hoạt động, chưa chứng minh tự kiểm phát hiện khi chính nhánh đó bị vô hiệu hoá.

**Giới hạn cần giữ:** nếu chạy riêng `--tu-kiem` trên cây đã đổi main với chốt đã nới, kết quả là **2/7, rc=1**; năm control ngoại lệ phát hiện sai phân hạng. Không tuyên mọi phép thử đều xanh. Finding là thiếu control trực tiếp cho chốt và catalog vẫn cấp 16/16 trong đối chứng mất hợp đồng.

Tái lập: [prepare_contract.py](review-logs/prepare_contract.py), `gate-removed.*`, `gate-relaxed.*`, `contract-present-changed-main.*` trong review-logs; các bản đột biến tại review-tmp.

**Các số còn sai hoặc chưa được đính chính đủ vị trí — năm thể hiện, cùng lớp F6:**

| ID | Vị trí | Lời khai sai/chưa được điểm danh | Đo và đính chính cần có |
|---|---|---|---|
| **N31-b** | do-cua-tac-gia/PROMPT.rvwin512-7.md:49 | “năm mutant” rồi liệt kê N01 N02 N10 N12 N17 N18 | **Sáu**. Đính chính N31 chỉ điểm danh subject commit. Vòng 7 từng không tính lỗi câu chữ prompt; lượt 8 yêu cầu tìm tiếp các vị trí số cũ. Chỉ yêu cầu bổ sung đính chính, không sửa lịch sử. |
| **N32-b** | do-cua-tac-gia/TRANG_THAI.md:38 và :96 | +1114 với số hạng Python 1076+32; `1114≤1500`; `1114>300` | Python thật **1095**, shell **6**, tổng **1101**. Sau HINT, cột thêm Python tăng **19**, không tăng 32. Quan hệ với 1500/300 đều vẫn đúng nhưng số hạng sai. EVIDENCE vòng 7 chỉ điểm danh commit; cập nhật sau vòng 7 chưa chỉ rõ hai câu này. Gom cùng một thể hiện số tổng bị chép lại; không tính lại dư 386 đã sửa thành 399. |
| **N37** | do-cua-tac-gia/TRANG_THAI.md:120 | 13:10:20Z → 13:25:15Z là “~8,5 phút” | Hiệu hai mốc tự khai là **895 giây = 14 phút 55 giây ≈14,92 phút**. Không chứng thực độc lập thời điểm thật; chính phép trừ nội tại đã sai. |
| **N38** | do-cua-tac-gia/TRANG_THAI.md:129 | Tập F7 gồm N01 N02 N12 N17 N18 nhưng ghi SỐNG 6/6 và CHẾT 6/6 | Tập liệt kê có **năm**, nên **5/5 mỗi head**. Sáu là tổng F2+F7, có thêm N10 ở hàng F2. Quan hệ sống→chết không làm đúng lại số phần tử tập con. |
| **N39** | do-cua-tac-gia/TRANG_THAI.md:168 | Sau khi phóng vòng 8 “sẽ là 7/10” | Theo chính neo EVIDENCE vòng 8, đã dùng 7/10 trước lượt này; sau phóng phải **8/10**. Không xác nhận hay thay đổi quyền dùng trần. |

Không báo lại các số đã khớp như 24 280 byte của verdict vòng 7; không biến một mốc lịch sử thiếu nguồn thành số chắc chắn sai.

Cần sửa **bộ đo và hồ sơ riêng** để bảo toàn bằng chứng phân biệt loại tín hiệu, kiểm chiều dương với thông điệp hợp lệ, và kiểm chính các giả định của bộ đo. Không nhận cách thêm một tên ngoại lệ làm đóng lớp. Một regex có thể là thành phần của phép đo; các phản chứng trên bác tính bao phủ của phép đo cụ thể này. Không yêu cầu PR mở đường thứ ba hay sửa product/workflow ngoài write set.

## Mutant đã chạy

**Catalog tác giả trên HEAD — 16/16 chết đúng chốt**, sau khi đã chạy tự kiểm cả ba bản:

| Mutant | Ca đích | Lý do chết đã kiểm |
|---|---|---|
| giet-chi-PID-khong-giet-cay | t154 | Nhịp cháu còn tăng sau thu hồi |
| bo-start_new_session | t154 | Con không làm lãnh đạo nhóm riêng |
| M13-killpg-khong-chot-truong-nhom | t154 | Chạm nhóm không được giết |
| bo-chot-selector-khong-khop | t155 | Selector sai trả 0 thay vì 3 |
| AB_HAN_GIAY-ghi-tay-420 | t156 | Hạn ngoài không chứa tổng hạn trong |
| ngan-sach-cap-lai-han-toi-thieu | t156 | Dãy lệnh không dừng ở ngân sách tổng |
| M10-ngan-sach-chi-cap-lai-khi-CAN | t156 | Cấp lại hạn giữa hai lời gọi |
| M11-nhanh-can-tra-ket-do-dang | t156 | Thiếu tín hiệu hết ngân sách |
| T137_TRAN-bo-chan-doan | t156 | 360 khác tổng 180+180+120 |
| tee-chi-in-o-cuoi | t157 | Không thấy dòng lúc con còn sống |
| tee-bo-tien-to | t157 | Mất tiền tố ở đầu dòng |
| M09-tee-bo-flush-CA-HAI-print | t157 | Không thấy byte đã xả trong cửa sổ đo |
| M14-moi-truong-con-khong-TAT-DEM | t158 | Môi trường thật hai vế thiếu tắt đệm |
| M15-classifier-tra-KHOP-khi-lech | t160 | Mất chẩn đoán đúng vế |
| M16-consumer-bo-classifier-gan-KHOP | t160 | Classifier không nhận tuple |
| M17-consumer-nhan-ca-trang-thai-CHUA-RO | t160 | Consumer không chặn lệch |

Log catalog: [catalogue16.log](review-logs/catalogue16.log). Log thô của lượt lặp catalog bỏ chốt (cùng nguồn HEAD, cùng 16 phép biến đổi) được giữ tại `review-logs/gate-removed/`; bỏ chốt không đổi các kết quả này.

**Các phép bổ sung:**

| Phép biến đổi/control | Kết quả |
|---|---|
| Bảy control nguyên bản; bốn control REGEX_CU | MỚI 7/7, VA_VONG6 5/7, REGEX_CU 2/4; đúng từng phân hạng tác giả khai |
| Bung → Bùng | MỚI 6/7; cấp tín dụng giả, F6.7 |
| Thông điệp Exception → rỗng | MỚI 6/7; cấp tín dụng giả, F6.8 |
| Đảo boolean assertion t96, giữ thông điệp | Vòng 6 1/1; MỚI 0/1; F6.9 |
| Bỏ/nới chốt; đổi dòng in main trong bản sao | Ma trận kết quả tại F6.10 |
| CTRL-GeneratorExit nguyên bản | Traceback đi qua main và ca t160, có dòng vào, không dòng ra/tổng kết/ĐỎ; rc=1, TIN DUNG GIA qua ĐỎ=[] |
| GeneratorExit → BaseException/KeyboardInterrupt/SystemExit | Mỗi bản 7/7, cùng nhánh ĐỎ=[]; không chứng minh regex mới |
| N01 đảo đối số; N02 đảo biến nhận | Sống ở 353eae1; chết ở HEAD vì tuple không đúng nhãn |
| N10 bỏ danh sách tee | Sống ở 353eae1; chết ở HEAD vì bốn cặp tệp/nhãn thành [] |
| N17 bỏ so mẫu số | Sống ở 353eae1; chết ở HEAD vì mất chẩn đoán 1/2 |
| N18 cố định mẫu số bằng "2" | Sống ở 353eae1; chết ở HEAD vì tuple parser sai |
| Thử phụ lấy tử số làm mẫu số | Chết ở cả hai head; giữ log nhưng **không** coi là tái lập N18 vòng 7 |

`CTRL-GeneratorExit` không phải control rỗng: log thô chứng minh raise đã chạy và bị nhánh “không có dòng ĐỎ của ca đích” loại. Lời tự khai giới hạn của tác giả là đúng; nó không cho bằng chứng về `_DANG_VO_CAN`.

## chua_do_duoc

| Câu hỏi | Trạng thái | Giới hạn |
|---|---|---|
| PR giữ đúng byte từ vòng 7? | **có** | HEAD và hai băm khớp; diff/numstat đúng gói. |
| Reviewer có ba tổng kết dương CHA/A/B độc lập? | **có** | Mỗi lượt 155/155, 0 đỏ, 0 bỏ qua; không dùng rc=0 một mình. |
| Hồi quy F1/F2/F3/F4/F5/F7 trong phạm vi Linux đã đo? | **không** | Byte không đổi, full suite và các đối chứng nêu trên; không ngoại suy Windows. |
| Bộ đo mới phủ toàn bộ ngoại lệ vô can main có thể in? | **không** | Unicode và thông điệp rỗng lọt. |
| Bộ đo mới luôn nhận đúng thông điệp chốt hợp lệ? | **không** | t96 bị từ chối sai; bản trước nhận đúng. |
| Chốt hợp đồng có tác dụng lúc còn nguyên? | **có** | Đổi main bị CHAN trước catalog. |
| Tự kiểm hiện tại phát hiện việc bỏ/nới chốt trên HEAD? | **không** | Vẫn 7/7; catalog vẫn 16/16. |
| GeneratorExit đã thật sự chạy và bị loại? | **có** | Traceback thật, rc=1, ĐỎ=[]; đường khác regex như tác giả khai. |
| doctrine-scan và adr-song tại HEAD? | **có** | Chạy theo ngoại lệ hẹp, rc=0 và tổng kết 7/0, 47/47. |
| Hai log và đủ 16 hiện vật hồ sơ? | **có** | Đếm và đối chiếu byte với nhánh hồ sơ. |
| A5≤300? | **không** | +1101; override được khai không sửa đặc tả. |
| N12 tái sinh retry bằng Popen/PIPE được chạy lại động lượt này? | **KHÔNG ĐO ĐƯỢC** | Không có mã mutant N12 trong hiện vật Python đã tìm; không tự soạn lại đường ấy. t160 và các chốt run/Popen không đổi byte; kết luận vòng 7 được kế thừa có giới hạn. |
| Tên lớp không phải định danh, __name__ bị ghi đè, mọi cách in nhiều dòng? | **KHÔNG ĐO ĐƯỢC** đầy đủ | Không có fixture riêng đã nhận diện để chạy; không tự soạn mã giả mạo. Đề nghị phiên điều phối cung cấp control cho tên runtime khác định danh và thông điệp bắt đầu bằng xuống dòng, đi qua toàn pipeline main→splitlines→strip. Unicode/rỗng đã đủ bác tuyên bố phủ toàn lớp. |
| Chống giả mạo tín hiệu assertion/stdout nói chung? | **KHÔNG ĐO ĐƯỢC** đầy đủ | Nợ đã khai; không tự soạn payload, đường thoát cây hay mã tấn công. Các thử thêm chỉ biến đổi control/boolean/dòng in đã có. |
| Windows exact head, A2/A3/A4, ngưỡng 15 phút và Ubuntu chậm ≤10%? | **KHÔNG ĐO ĐƯỢC** | Không có Windows/CI tại sandbox; log lịch sử nguồn vẫn thiếu. Linux xanh không chứng nhận các tiêu chí này. |
| Tần suất S8-bo-deadline hoặc nguyên nhân GITHUB_ACTOR? | **KHÔNG ĐO ĐƯỢC** | Nợ ngoài write set; một lần xanh không loại trừ chập chờn. |
| Chứng thực online override, trạng thái GitHub, backend mô hình? | **KHÔNG ĐO ĐƯỢC** | Chỉ đọc dữ liệu trong sandbox; model_tu_khai không phải xác minh backend độc lập. |

Các đột biến ở review-tmp; TMPDIR được đặt trong sandbox và ngoài cay-kho. Không sửa ops/lease_publish.py, packet_loop.py hay workflows trong cây gốc; không phát sinh yêu cầu PR sửa các đường ngoài write set.

Kiểm cuối: `git -C cay-kho status --porcelain` **RỖNG**; `git -C cay-kho log --oneline 36f68c7..HEAD` **RỖNG**. HEAD và hai băm giữ nguyên. Hiện vật kiểm cuối: [final-hygiene.json](review-logs/final-hygiene.json).

XONG VERDICT
