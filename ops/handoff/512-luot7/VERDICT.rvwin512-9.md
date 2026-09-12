verdict: changes_requested
reviewed_sha: 36f68c7e95e0de1fcf8e2311db33a164816db20f
reviewed_base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
reviewed_files_sha256:
  ops/lease_publish_test.py: 13a2af8ca8cd1d4571590f0e46c751eb0d7e6964790a0d53cdd5e0058a591f84
  ops/chay_lease_publish_test.sh: 87c760294763c71a67cfaee50a440e62b31c439beb0abbfcb5e34076d32be693
model_tu_khai: GPT-6 / Codex; khác họ Claude theo lời khai tác giả; không xác minh backend độc lập
review_round: 9
so_p1: 1
so_p2: 2
so_p3: 0
so_the_hien: 10
so_p1_trong_write_set: 0
so_p2_trong_write_set: 0
hint_sha256:
previous_hint_sha256: e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0

**changes_requested đối với hồ sơ/luận cứ vòng 9. Không tìm thấy hồi quy trong hai đường write set.** Full suite độc lập có **155/155 ở CHA, [A], [B]**, không đỏ, không bỏ qua. Hai lời khai dùng để chọn bộ đo mặc định — **“v8 bắt 4/4”** và **“hồi quy có biên 8/454, bốn ca”** — không đúng với đường chạy thật. Việc giữ v8 có thể dựa trên ưu tiên giảm tín dụng giả, nhưng phải sửa bằng chứng và phạm vi lời khai trước khi kết luận từ chúng.

**Mọi finding mở dưới đây là nợ ngoài write set**, không yêu cầu PR thêm đường thứ ba. F6.7–F6.10 được chuyển sang #530 vẫn là nợ mở; riêng sự tồn tại của bốn nợ ấy không phải lý do yêu cầu sửa PR này. Không quyết định merge, không approve thay chủ kho, không cấp hoặc nâng trần.

**Cách đếm:** F6 (phân hạng bộ đo) có sáu thể hiện; F8 (sai đại lượng/nguồn của hồ sơ) có ba; F9 (tiêu chí nghiệm thu packet kế nhiệm) có một. Tổng **10**, trong đó **4 cũ + 6 mới**. Mỗi lớp chỉ tính một lần theo mức cao nhất: F6=P1, F8=P2, F9=P2. N40 riêng lẻ là P3 nhưng nằm trong lớp F8 mức P2. Không đếm các số đã đo đúng, các đính chính đã đóng, hay một lời khai chép tại nhiều vị trí thành nhiều thể hiện.

Đã append ngay trong khi đo; nhật ký trước khi sắp báo cáo nằm ở [review-logs/VERDICT-journal.md](review-logs/VERDICT-journal.md). Không nộp HINT.patch.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Lớp | Trạng thái canonical | Căn cứ vòng 9 |
|---|---|---|
| F1 thu hồi cây | **ĐÃ VÁ THẬT** | Byte khớp vòng 7/8; t154 xanh ở CHA/A/B; ba mutant giết PID, bỏ session, bỏ guard nhóm chết đúng chốt. Đo POSIX. |
| F2 bằng chứng sống | **ĐÃ VÁ THẬT** | Đủ ba tổng kết và 155 cặp vào/ra mỗi vế; t157/t158/t160 xanh; mutant tee cuối, bỏ tiền tố, bỏ flush chết đúng chốt. |
| F3 selector | **ĐÃ VÁ THẬT** | t155 xanh; bỏ guard selector chết vì trả 0 thay vì 3. |
| F4 ngân sách tổng | **ĐÃ VÁ THẬT** | t156 xanh; các mutant cấp lại hạn, trả kết quả dở, hạn ngoài 420, bỏ hạn chẩn đoán chết đúng chốt. |
| F5 tắt đệm con | **ĐÃ VÁ THẬT** | t158 xanh cả ba vế; M14 chết tại phép đo môi trường thực. |
| F6 phân hạng bộ đo | **VÁ SINH LỖI MỚI** | Vẫn false GREEN ở Unicode/thông điệp rỗng, false RED ở t96; vòng này xác nhận thêm BoQuaNen và tiền tố động t131. Nợ #530. |
| F7 classifier/consumer/phản chứng | **ĐÃ VÁ THẬT** | Byte không đổi; t160 xanh cả ba vế; M15/M16/M17 chết đúng chốt. Không tuyên đã chạy lại toàn bộ đối chứng hai head của vòng 7. |
| F8 hồ sơ đại lượng/nguồn — mới | **CHƯA VÁ** | N40/N41/N42 dưới đây. |
| F9 nghiệm thu #530 — mới | **CHƯA VÁ** | A2 chưa đo đúng kết quả mà việc chuyển sang kênh riêng cần đạt. |

| Từng thể hiện mở của vòng 8 | Trạng thái canonical | Đối chiếu vòng 9 |
|---|---|---|
| **F6.7** | **CHƯA VÁ** | Control Unicode vẫn nhận GIET THAT ở v8; đã thêm control nhưng chưa sửa phân hạng. |
| **F6.8** | **CHƯA VÁ** | Control Exception thông điệp rỗng vẫn nhận GIET THAT ở v8. |
| **F6.9** | **VÁ SINH LỖI MỚI** | Chốt thật t96: v6 GIET THAT, v8 TIN DUNG GIA. |
| **F6.10** | **CHƯA VÁ** | Bỏ lời gọi chốt hợp đồng: tự kiểm vẫn 7/10 với log bằng byte bản nguyên; catalogue vẫn 16/16, rc=0. |
| **N31-b** | **ĐÃ VÁ THẬT** | ERRATA:14 điểm danh PROMPT vòng 7:49; tập N01/N02/N10/N12/N17/N18 có sáu. Giữ byte prompt lịch sử là phù hợp. |
| **N32-b** | **ĐÃ VÁ THẬT** | Hai chỗ sống trong TRANG_THAI đã đổi sang 1095+6=1101 và A5 dùng 1101; khối đính chính nêu rõ 1114, 1076+32, 386 cũ. Dư 399 đúng. |
| **N37** | **ĐÃ VÁ THẬT** | 13:10:20→13:25:15 đúng 895 s = 14 ph 55 s. Không xác nhận độc lập hai mốc lịch sử. N40 là một khoảng khác. |
| **N38** | **ĐÃ VÁ THẬT** | F7 có năm ID N01/N02/N12/N17/N18; N10 thuộc F2. Bảng đã sửa 5/5. |
| **N39** | **ĐÃ VÁ THẬT** | Mục cập nhật đã sửa thành 8/10 sau vòng 8; không tự xác nhận quyền dùng trần. |

F6.5/StopIteration vẫn được v8 loại đúng. F6.6 vẫn đóng: gói nay đủ 20 hiện vật, có cả hai log suite, 20/20 bằng blob nhánh hồ sơ. Các đính chính N31/N32 tại thông điệp commit cũng khớp số đo. Không tìm thấy vị trí mới còn khẳng định 1114/386/năm mutant như số hiện hành ngoài các chỗ đã được điểm danh hoặc được giữ dưới nhãn lịch sử/đính chính.

**Hai lời khai nền:**

1. **Write set không đổi:** hai băm ở đầu báo cáo khớp nguyên văn cả verdict vòng 7 và 8; HEAD đúng, cây sạch. Không có căn cứ xét lại các kết luận đã vá do byte bị đổi.
2. **Port/exclusion có cơ sở kỹ thuật:** tự đọc `ops/nhanh_don_duoc_test.py` xác nhận `TinHieuChotCa:30`, `chot:34`, ba trạng thái `:48`, `sinh_dau_phien:51`, JSONL và neo ba chiều `:70–72`, `dong_luot:83`, `doc_kenh:90`, `DOT_BIEN_TU_KIEM:2236`. Nhưng lời dẫn “#504 giữ” sai: spec #513 tại `:129` ghi **#503 giữ**. Exclusion cùng đường và kiến trúc mẫu vẫn có thật; sai mã packet được báo N42, chưa đủ để bác toàn bộ cơ sở dời F6 thành P1 như tình huống điều kiện trong prompt. Trạng thái issue trực tiếp chưa đo.

## BẢNG ĐO

| Phép đo | Kết quả độc lập | Hiện vật |
|---|---|---|
| Neo Git | HEAD=36f68c7, detached; base đúng bb7013c; is-shallow=false; core.abbrev=7 | `final-hygiene.json`; lệnh đầu lượt |
| Spec #504 / #530 | Hai SHA256 khớp chính xác mỏ neo người dùng | Băm trực tiếp đầu lượt |
| Diff / numstat giao kèm | Bằng byte kết quả Git; đúng hai đường, Python +1095/−27; shell +6/−0 ⇒ +1101/−27 | `verification.json` |
| Gói tác giả | 20/20 tệp bằng blob `ops/handoff-512-luot7:ops/handoff/512-luot7/…` | `artifacts.json` |
| Điều kiện full suite | Linux; Python 3.11.15; ShellCheck 0.9.0; actionlint 1.7.7, archive SHA256 `023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757` | `verification.json`, log suite |
| Full suite **[B]** | **155/155 đạt; đã chạy=155, bỏ qua=0** | `full-suite-fixed.log:1055` |
| Full suite **[A]** | **155/155 đạt; đã chạy=155, bỏ qua=0** | `full-suite-fixed.log:1060` |
| Full suite **CHA** | **155/155 đạt; đã chạy=155, bỏ qua=0** | `full-suite-fixed.log:1156` |
| Đầy đủ mỗi vế | 155 vào / 155 ra, đúng thứ tự 155 tên ca trong AST; 0 đỏ; wrapper rc=0 | `verification.json`, `full-suite-fixed.rc` |
| t125/t158/t160 tại CHA | 55.296 s / 3.356 s / 0.064 s, QUA | `verification.json` |
| Hai log tác giả | Log đủ: ba 155/155, 0 đỏ; log thiếu: ba 153/155, đúng t137/t159 đỏ mỗi vế vì thiếu ShellCheck. Mốc 1055/1060/1156 của log đủ khớp lời khai | `verification.json` |
| Tự kiểm v0 / v6 / v8, cùng 10 control | **4/10 / 7/10 / 7/10**, cả ba rc=1; số false GREEN/false RED đúng 6/0, 3/0, 2/1 | `self-v0.log`, `self-v6.log`, `self-v8.log` và `.rc` |
| Khác biệt ba bộ đo | Mỗi bản v0/v6 khác v8 đúng một dòng gán `vo_can`; CONTROL bằng nhau | `diff -u` trực tiếp |
| Catalogue nguyên | 16/16 GIET THAT, 0 tín dụng giả, 0 sống, 0 chặn; từng lý do phù hợp chốt đích | `catalogue.log`, `.rc` |
| Control quyết định bổ sung, chạy nguyên chương trình | v6 **2/5**, v8 **3/5**, rc=1; bảng loại tín hiệu bên dưới | `decision-actual-v*.log`, `.rc` |
| Gỡ chốt hợp đồng | Tự kiểm 7/10, rc=1, log bằng byte bản nguyên; catalogue 16/16, rc=0 | `gate-removed-self.log`, `gate-removed-catalogue.log` |
| Đếm đúng blob HEAD | **493** lời gọi = 295 bang + 198 chot; **454** chỉ là tập có tiền tố tĩnh; còn **39** bị phép lọc bỏ qua | `count-claims.json`; script `count-claims.py` |
| Cây sai được khai | Nhánh hồ sơ có **147** ca, **430** lời gọi, **393** tiền tố tĩnh, không có t153–t160; HEAD có **155** ca. Phân biệt hai cây đúng | `blob-counts.json` |
| Các lớp ngoại lệ | Trong hai tệp lease product/test có đúng bốn lớp được liệt kê; sự có mặt không chứng minh phân hạng 4/4 | `ast-counts.json`; log quyết định |
| Port cơ học M1 của #530 | Đổi đúng **59** lời gọi tại chín ca; số tiền tố tĩnh va chạm vẫn **8** | `port-M1-counts.json`, `review-tmp/port-M1-only.py` |
| `ci_dang_ky_test.py` | rc=0; đăng ký 21/21; phản chứng 51/51; TỔNG ĐẠT | `ci-dang-ky.log` |
| `doctrine-scan` | rc=0; sạch, quét 7 tệp, 0 chỗ chép doctrine | `doctrine-scan.json` |
| `adr-song` | rc=0; 47 ADR / 47 dòng §20, khớp 1–1; tổng kết có tha thiếu trạng thái 0016 | `adr-song.json` |
| A5 đóng băng | **Không đạt:** 1101>300. 1101≤1500 và dư 399 không đổi nhãn A5 | Spec và numstat |
| Vệ sinh cuối | `git status --porcelain` rỗng; `git log --oneline 36f68c7..HEAD` rỗng; băm giữ nguyên | `final-hygiene.json` |

Các hiện vật ngắn trong bảng nằm dưới `review-logs/`.

Lần wrapper đầu dừng trước suite với installer rc=5 vì tar không đổi được ownership trong sandbox. Lượt hoàn tất dùng **`TAR_OPTIONS=--no-same-owner`**, `TMPDIR` và `AL_DICH` trong sandbox, archive offline và bản ghim nguyên vẹn. Đây là điều kiện đo đã xử lý, cùng tình huống đã ghi ở vòng 8; không gọi là hồi quy. Không bỏ kiểm băm/phiên bản. `rc=0` được đối chiếu với ba tổng kết dương, không đứng một mình.

Chỉ dùng rc và dòng tổng kết của hai lệnh doctrine/ADR theo ngoại lệ hẹp. Không tự mở các tệp bị cấm làm chỉ dẫn. Mọi đột biến ở `review-tmp/` trong sandbox.

## Findings theo lớp

### F6 — phân hạng bộ đo làm mất loại tín hiệu; P1, 6 thể hiện, nợ #530

**F6.7 / F6.8 / F6.9 / F6.10 — bốn thể hiện cũ còn mở.** Log tự kiểm đủ 10 control xác nhận Unicode và Exception rỗng được GIET THAT; t96 thật bị TIN DUNG GIA. Gỡ `_kiem_hop_dong_main(NGUON)` trong bản sao không đổi một byte log tự kiểm, và catalogue vẫn 16/16. Tự kiểm hiện đã đỏ nên không thể dùng riêng rc=1 để nói nó bắt được việc mất chốt. So tập kết quả với bản nguyên cho thấy không có control mới nào phát hiện việc gỡ ấy.

**F6.11 — P1, mới: nhánh `BoQuaNen` nằm ngoài mô hình “hai hình dạng”; đính chính 4/4 không chứng minh được quyết định.** Vị trí: `do-cua-tac-gia/dotbien512.py:270–278`; lời khai ở `EVIDENCE.md:49–53`, `F6-HO-SO.md:175–183`, `TRANG_THAI.md:315–318`.

Đột biến control Exception có sẵn thành từng lớp **thật** của hai tệp, chạy qua `main()` thật rồi qua nguyên chương trình bộ đo. Không thay stdout hay dựng tên kiểu giả. Kết quả:

| Lớp ném trong ca | Main thật xử lý | v6 | v8 |
|---|---|---|---|
| BoQuaNen | Nhánh riêng `:6506`; không suy ra lý do skip hợp lệ ⇒ in `bỏ qua không dẫn xuất được từ runs-on` | GIET THAT | **GIET THAT** |
| Chan | Nhánh Exception in tên kiểu | GIET THAT | TIN DUNG GIA |
| HetNganSachDay | Nhánh Exception in tên kiểu | GIET THAT | TIN DUNG GIA |
| TinHieuChotCa | Là con của AssertionError; nhánh `:6513` in thông điệp, mất tên kiểu | GIET THAT | **GIET THAT** |

Vậy v8 loại **2/4**, không phải 4/4. Đồng thời, **TinHieuChotCa là chính lớp tín hiệu**, nên gọi mọi lần nhận nó là tín dụng giả cũng sai về đáp án. Trong ba control vô can còn lại, v6 lọt **3/3**, v8 lọt **1/3**. Đính chính “ba tên → bốn tên” đúng về việc đếm khai báo; suy tiếp thành “v6 false GREEN 4/4 / v8 bắt 4/4” sai. Đường BoQuaNen đủ bác lời khai này, không cần giả mạo tín hiệu.

**F6.12 — P2, mới: hồi quy v8 còn phụ thuộc dữ liệu tiền tố động; bốn ca/8 chốt không phải biên.** Tại `ops/lease_publish_test.py:4659`, ca **t131**, chỉ đảo boolean của `chot(rc == mong, f"{ten}: n=…")`; giữ nguyên thông điệp, bảng fixture và đường chạy. Chốt thật phát:

> max_parent_path_edges: n=3, bound=2 đợi 12, được 12: KHÔNG_XÁC_ĐỊNH: đường parent > 2 cạnh

v6 nhận **GIET THAT**, v8 nhận **TIN DUNG GIA**. Đây là **ca thứ năm** ngoài t96/t133/t136/t151; ít nhất **chín vị trí lời gọi** đã xác định có thể va chạm, chưa phải tổng số cuối. Chỉ riêng một vị trí này chạy qua nhiều giá trị `ten`; không được đồng nhất số vị trí AST với số lần assertion thực thi. So sánh “v6 không có biên, v8 có biên 8” đã lấy một tập lọc tĩnh làm toàn miền của v8.

Tái lập: [build-decision-meters.py](review-logs/build-decision-meters.py) sinh ba bản đo với cùng năm control; `python3 review-tmp/decision-v8.py cay-kho --tu-kiem`, tương tự v0/v6, với TMPDIR trong sandbox. Bằng chứng chính là **`decision-actual-v*.log`**. Không suy từ phép match trên bốn chuỗi tự ghép.

**Yêu cầu đối với hồ sơ vòng này:** thay lý do 4/4 và biên 8 bằng bảng hành vi thực và giới hạn phép đo. Mẫu đã đo vẫn cho thấy v8 giảm một số false GREEN và tăng false RED; chưa chứng minh bản nào tối ưu trên toàn miền. Không yêu cầu tự động lùi v6, không tuyên F6 đã đóng vì thêm control tự báo đỏ.

### F8 — số hạng và nguồn dẫn trong hồ sơ không khớp phép đo; P2, 3 thể hiện

**N40 — P3, mới, thời lượng vòng 8:** `do-cua-tac-gia/TRANG_THAI.md:199` ghi 13:36:19Z→13:49:51Z là **813 s = 13 ph 33 s**. Hiệu đúng **812 s = 13 ph 32 s**. ERRATA mới chưa điểm danh khoảng này. Không xác nhận hai mốc lịch sử là thật; lỗi nằm ngay ở phép trừ. N37 đã sửa đúng một khoảng khác. Hai số byte 24 280/21 430 đã đo khớp, không tính finding.

**N41 — P2, mới, mẫu số sau “đã ghim blob” vẫn bị khai rộng:** `EVIDENCE.md:53,84–86`; `F6-HO-SO.md:182`; `TRANG_THAI.md:318,325–329`; `SPEC-packet-F6-530.md:50`. Đúng blob có **493** lời gọi bang/chot. Con số **454** tái lập được bằng việc chỉ giữ thông điệp Constant hoặc f-string bắt đầu bằng Constant. Nó bỏ **39** lời gọi, gồm chính tiền tố động t131 của F6.12. Tử số **8** đúng trên tập lọc ấy. Cần ghi “8/454 trong tập có tiền tố tĩnh; 39 lời gọi khác chưa bao phủ” và tách khỏi kết quả động; không trình bày thành tỷ lệ toàn bộ assertion hay giới hạn hồi quy.

Lời đính chính cây sai có **cơ sở về hai nguồn**: nhánh hồ sơ đúng 147 ca, HEAD đúng 155, t153–t160 chỉ hiện diện ở HEAD. Không có log gốc của chính lần lệnh chạy sai để chứng thực lịch sử. Việc ghim blob chữa nhầm nguồn, không tự chữa thiên lệch do lọc. `origin/master` trong gói hiện trỏ commit merge #512 và cũng có 155 ca; đã dùng blob nhánh hồ sơ để đo phần lịch sử, không dùng ref chuyển động ấy thay nó.

**N42 — P2, mới, dẫn sai chủ thể của exclusion:** `EVIDENCE.md:33–35` và `TRANG_THAI.md:301–302` quy `ngoai_pham_vi #4` của #513 thành “#504 giữ”. Tệp spec thật ở `cay-kho/ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md:129–131` ghi **#503**, tên lease `m9-fetch-auth-exec-1-claude-20260911`, và phân việc t125 sang `T125-RA-JOB-RIENG`. Cần dẫn đúng lịch sử rồi trình bày riêng sự suy luận về khoảng trống do loại cùng đường. Exclusion vẫn tồn tại; không thay một câu dẫn sai bằng kết luận rằng kiến trúc port không có.

Ba thể hiện này cần đính chính ở hồ sơ; các bản sao của cùng lời khai đã được gom một thể hiện. Không sửa byte spec đóng băng trong lượt review.

### F9 — tiêu chí nghiệm thu #530 đo sai đại lượng cần hết; P2, 1 thể hiện, nợ packet kế nhiệm

**F9.1 — A2 “va chạm hình dạng chuỗi về 0” không đi theo M1/M2/M6.** `SPEC-packet-F6-530.md:102–114`: M1 đổi đúng 59 bang→chot ở chín ca #504, giữ bang ngoài nhóm; M2/M6 chuyển phân hạng sang kênh và thôi đọc hình dạng chuỗi. Nhưng A2 đòi phép đếm chuỗi nguồn mô tả tại §nguon_cap_viec về 0.

Đã đổi cơ học đúng **59** vị trí trên bản sao: phép đếm nguồn vẫn có **8** tiền tố tĩnh, ở đúng t96/t133/t136/t151. Hai tên hàm đều thuộc phép đếm; đổi loại ngoại lệ hoặc thêm JSONL không xoá các thông điệp bình thường ấy. Đây là phép đo giới hạn của M1 và đối chiếu yêu cầu, **chưa phải chạy một implementation hoàn chỉnh của #530**.

Cần làm A2 đo **0 sai phân hạng qua kênh** trên tập control xác định, hoặc nêu phép đo mới cụ thể. Nếu giữ literal source-count=0, một port kênh đúng vẫn bị đánh đỏ và người triển khai bị thúc sửa thông điệp ngoài mục tiêu. Bộ control còn chứa t96 ở ngoài chín ca M1: đặc tả cũng cần nói rõ tín hiệu của control dương này đi vào kênh thế nào. Điểm sau là quan hệ cần làm rõ trong cùng thể hiện, không đếm thêm một lỗi thực thi chưa có mã.

## Mutant đã chạy

**Catalogue gốc, trên bản sao từ HEAD:**

| Mutant | Ca đích | Kết quả/lý do đã kiểm |
|---|---|---|
| giet-chi-PID-khong-giet-cay | t154 | GIET THAT; nhịp cháu tiếp tục tăng |
| bo-start_new_session | t154 | GIET THAT; con không là lãnh đạo nhóm riêng |
| bo-chot-selector-khong-khop | t155 | GIET THAT; rc=0 thay vì 3 |
| AB_HAN_GIAY-ghi-tay-420 | t156 | GIET THAT; hạn ngoài không chứa trần trong |
| tee-chi-in-o-cuoi | t157 | GIET THAT; không có dòng sống trong hạn |
| tee-bo-tien-to | t157 | GIET THAT; thiếu nhãn đầu dòng |
| ngan-sach-cap-lai-han-toi-thieu | t156 | GIET THAT; dãy không dừng ở ngân sách tổng |
| M09-tee-bo-flush-CA-HAI-print | t157 | GIET THAT; không thấy dòng trước khi con xong |
| M10-ngan-sach-chi-cap-lai-khi-CAN | t156 | GIET THAT; hết ngân sách giữa lệnh nhưng không ném |
| M11-nhanh-can-tra-ket-do-dang | t156 | GIET THAT; kết quả dở thay cho báo hết hạn |
| M13-killpg-khong-chot-truong-nhom | t154 | GIET THAT; chạm nhóm không được giết |
| M15-classifier-tra-KHOP-khi-lech | t160 | GIET THAT; chẩn đoán không giữ đúng vế |
| M16-consumer-bo-classifier-gan-KHOP | t160 | GIET THAT; classifier không nhận tuple đúng nhãn |
| M17-consumer-nhan-ca-trang-thai-CHUA-RO | t160 | GIET THAT; chẩn đoán không giữ đúng vế |
| M14-moi-truong-con-khong-TAT-DEM | t158 | GIET THAT; môi trường thực không tắt đệm |
| T137_TRAN-bo-chan-doan | t156 | GIET THAT; thiếu một trong ba hạn trong |

Đã chạy cả **10 control** nguyên của từng bản: Exception trần, Error trần, RuntimeError, chốt dương M15, StopIteration, Bung, GeneratorExit, chốt dương t96, Unicode Bùng, Exception rỗng. Giữ log đầy đủ trong `self-v*.log`; ba đáp án tổng khớp bảng tác giả.

**Đột biến bổ sung:** năm control quyết định (bốn lớp thật + đảo chốt t131) ở cả ba chương trình; gỡ lời gọi chốt hợp đồng rồi chạy tự kiểm/catalogue; đổi cơ học 59 vị trí bang→chot để kiểm chỉ số của A2 #530. Các cây riêng ở `review-tmp/`. Full suite còn chạy catalogue A0 t139, tổng kết **34 giết thật / 37**, ba sống có chủ đích; không lấy ba sống ấy làm finding mới của #504.

**Đính chính phép đo của reviewer:** rig thăm dò đầu lấy `_DANG_VO_CAN` chung cho v0/v6, trong khi hai bản ấy dùng dòng `vo_can` riêng. Đã ghi ngay sai sót, giữ kết quả đầu ở `decision-probes-FIRST-RIG-INVALID-v0-v6.json`, sửa rig và chạy lại; sau đó chạy nguyên chương trình cả ba bản. Các cột v0/v6 của kết quả đầu bị loại khỏi căn cứ verdict. `decision-probes.json` hiện là lượt sửa; `decision-actual-v*.log` là đối chứng chính.

## chua_do_duoc

Ba trạng thái dùng theo từng mệnh đề: **có · không · KHÔNG ĐO ĐƯỢC**. Không lấy thiếu phép đo làm xanh.

| Mệnh đề | Trạng thái | Giới hạn |
|---|---|---|
| Linux HEAD có đủ ba tổng kết dương CHA/A/B | **có** | Lượt reviewer độc lập, 155/155 mỗi vế, đủ công cụ |
| Write set đổi byte từ vòng 7/8 | **không** | Hai băm và Git cuối khớp |
| Tìm thấy P1/P2 mới phải sửa trong hai đường write set | **không** | Trong phạm vi đã chạy; không chứng nhận mọi nền |
| A5 đạt ngưỡng đóng băng 300 | **không** | +1101; override không sửa nhãn A5 |
| v8 loại cả bốn lớp được tác giả liệt kê | **không** | Nhận GIET THAT với BoQuaNen và TinHieuChotCa |
| 8/454 là biên toàn bộ hồi quy v8 | **không** | Bỏ 39 lời gọi; t131 đã tái hiện thêm |
| Có kiến trúc mẫu và exclusion cùng đường trong #513 | **có** | Mã và spec có thật; câu dẫn tên packet trong EVIDENCE sai |
| Tình trạng issue/lease/GitHub trực tiếp, run 34699156658 | **KHÔNG ĐO ĐƯỢC** | Không mạng; workflow đỏ do gen 1 hết hạn là lời khai nợ tác giả, chưa tái chứng thực lượt ấy |
| Windows A2/A3/A4, ngưỡng 15 phút, so ubuntu với A2 | **KHÔNG ĐO ĐƯỢC** | Không chạy Windows/CI; Linux không chứng nhận Windows |
| Các mốc Windows N07/N11–N15/N17/N18/N30 | **KHÔNG ĐO ĐƯỢC** | Thiếu log nguồn trong gói; không gán nhãn số sai |
| Chính lần tác giả chạy phép đếm trên cây sai | **KHÔNG ĐO ĐƯỢC** | Đã xác nhận chênh lệch hai blob, thiếu log lệnh lịch sử |
| Biên đầy đủ false GREEN/false RED của bộ đo | **KHÔNG ĐO ĐƯỢC** | Đã bác hai biên khai; chưa khảo sát hết thông điệp động và mọi loại lỗi |
| Chống giả mạo bởi mã cùng interpreter | **KHÔNG ĐO ĐƯỢC** | Không tự soạn mã tấn công; giới hạn còn nợ #530 |
| Toàn bộ sáu mutant N01/N02/N10/N12/N17/N18 ở cả hai head | **KHÔNG ĐO ĐƯỢC trong lượt 9** | Dùng byte không đổi, full suite và 16 mutant được giao cho kết luận không hồi quy; không gán lượt chạy của reviewer trước cho mình |
| S8-bo-deadline đã được chữa | **KHÔNG ĐO ĐƯỢC / chưa có bằng chứng chữa** | Nợ product ngoài write set; t139 vẫn khai ba mutant sống có chủ đích |
| Kênh #530 hoàn chỉnh đạt nghiệm thu/chi phí Windows | **KHÔNG ĐO ĐƯỢC** | Chưa có implementation/lease của packet trong lượt này; F9 là lỗi tiêu chí, không phải verdict chạy kênh |

Kết thúc đã kiểm: `git -C cay-kho status --porcelain` **RỖNG**; `git -C cay-kho log --oneline 36f68c7..HEAD` **RỖNG**. HEAD và hai băm ở đầu báo cáo giữ nguyên.

XONG VERDICT
