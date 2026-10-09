verdict: changes_requested
reviewed_sha: 4c1915c9d5cd1008699499d0aff13914f390f06c
spec_sha256: 64c67225335cf50b2a394ffda005e03d338ff545757b210640fd05ac14564af1
model/effort tự khai: GPT-6 theo cấu hình phiên; exact served model/effort KHÔNG ĐO ĐƯỢC

Kết luận nội dung: còn **2 lớp P2, 1 lớp P3, không có P1**. Closure mới đóng P1 lượt trước trong phạm vi lời khai được giao; bằng chứng quét vẫn có một đường âm giả và hợp đồng mã thoát chưa đầy đủ. Ngưỡng prompt là 0 P1/P2/P3 nên yêu cầu revision tiếp theo. Chỉ ghi dưới goi/ và thư mục mktemp dưới R.

provider: openai_codex
execution_surface: API agent với shell cục bộ
transport: machine; hiện vật cục bộ, không có GitHub submitter
assurance: nội dung review độc lập; không tự cấp review assurance/land authority

Hai lệnh định danh đầu tiên sau đọc chỉ thị trả đúng băm và HEAD ở header. Đã đọc luật L1–L5 và bảng mục của skill soan-spec để kiểm hợp đồng, không chạy quy trình hỏi lại quyết định Q1–Q4 đã được cấp.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Thực hiện trước săn mới. Lệnh chính: `PYTHONDONTWRITEBYTECODE=1 python goi/recheck.py`; bộ quét: `review_scratch=$(cat goi/scratch-path); PYTHONDONTWRITEBYTECODE=1 TMPDIR="$review_scratch" bash tukiem_r3.sh "$review_scratch"`. Log: `goi/recheck.log`, `goi/recheck-scanner.log`. Mô hình validator ở scratch chỉ dùng phân biệt các chốt, không là mã ứng viên.

| lớp lượt 1–2 | trạng thái | bằng chứng |
|---|---|---|
| hop-dong-dong-bang-thieu-neo (lượt 2 P1) | ĐÃ ĐÓNG trong phạm vi lời khai được giao | Header có mission 682/object 5627190292; đủ các trường closure trong bytes băm. Đổi required_checks làm băm `64c67225…` thành `4e7a4304…`. Miễn trừ nói rõ phạm vi wp678, thời hạn tới policy canonical, đổi closure phải đổi revision/hash/lease. Không yêu cầu băm thân Issue mà giao thức không quy định; không nhận OWNER là bằng chứng tác giả. |
| bo-quet-nghiem-thu-thieu-mien (lượt 2) | ĐÃ ĐÓNG trong các miền đã kiểm | Tự chạy qua entry point: .yml int, thiếu ID, non-mapping, parse, bia list, thay_the_cho=[" "]/[""], bia trắng, local-only, topic/HEAD đều rc=1; thay_the_cho=[] hợp lệ rc=0; ref hỏng rc=2. |
| bo-quet-chung-cu-khong-neo-anh (lượt 2) | CÒN MỞ (hướng 2); race cũ đã đóng | Race tự dựng: ref hiện `6f1055…`, map vẫn `e4adf9…`, errors vẫn lease_id=1000 của ảnh cũ. Cùng blob hai miền: blob=1/cặp=2, mỗi miền 1/1; JSON có map ref/OID và bộ đếm theo cặp. |
| bo-quet-khong-co-cua-chay (lượt 2) | VÁ SINH LỖI MỚI (hướng 1); lỗi không thực thi đã đóng | Các ca nguyên entry point nay thật sự xuất JSON và rc; good=0, int=1, Git hỏng/không kho=2. Không dùng lời khai bảng thay kết quả chạy. |
| objective-dong-nhat-cu-phap-voi-danh-tinh (lượt 2) | ĐÃ ĐÓNG | Các cặp `'yes'`/`!!str yes`, `'1.5'`/`!!str 1.5`, fresh/escape đều bằng nhau sau safe_load và hợp lệ; objective r3 chủ động cho phép. |
| tieu-chi-dot-bien-khong-phan-biet-chot (lượt 1, đóng ở lượt 2) | ĐÃ ĐÓNG | A2 direct int: strict=8, restore_D2=RETURN, L_remove_D2=RETURN; cả ba probe=RETURN/GH=0. A5 từng toán hạng: D5_self và D5_peer False→True; D6_self và D6_peer 8→RETURN, mỗi lần giữ các chốt khác. Các đối chứng chuỗi giữ True/RETURN. |
| so-do-nen-khong-khop (lượt 1, đóng ở lượt 2) | ĐÃ ĐÓNG lỗi A6; số ảnh hiện tại đo riêng | A6 kho hai ref/path thực trả rc=11, NGƯỜI_GIỮ 1: True; r3 đòi cả nhãn lẫn hai ref/path, không chỉ nonzero. Scan hiện tại đo 562 blob/cặp, toàn str, khác số ref do ảnh cấp; không bác số lịch sử chỉ vì môi trường khác. Suite đã đo 187/187, rc=0, bỏ qua=0; xem hướng 5. |
| bang-duong-phan-loai-sai (lượt 1, đóng ở lượt 2) | TÁI PHÁT (hướng 6); các vị trí D7/D8 cũ đã đóng | SOURCE_D7_D9 trong log: D7 đọc :2110/lập khóa :2123; :2139/:2143 thuộc hiển thị con-tro-treo; D8 :1938/:1942 so raw, :1946 f-string, :1967 str rồi tra tập. Bảng và A7 r3 phân biệt đúng. |
| trang-thai-q3-chua-dong-bo (lượt 1, đóng ở lượt 2) | ĐÃ ĐÓNG | `recheck.py` xác nhận neo 5885268193 ở :11/:321, §3 ghi đã xác nhận; không còn câu hỏi mở. Authority theo prompt, không đo live. |

Các trạng thái giới hạn ở biểu hiện đã thử, không tự suy toàn bộ lớp sạch. Bảng đã được cập nhật theo các kết quả mới bên dưới, giữ cùng slug để bảo toàn lịch sử.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện (vị trí trong SPEC) | phương án chung | phép kiểm / giới hạn |
|---|---|---|---|---|
| bo-quet-chung-cu-khong-neo-anh | P2 | Phụ lục A :327–328/:339–342/:354/:361: ls-tree/cat-file đọc OID nhưng còn Git replace | Tắt replace ở mọi lời gọi Git; kiểm commit và blob replacement | Cùng map: r3 rc=0, tắt replace hoặc HINT rc=1. Snapshot thật không có refs/replace; lỗi được dựng ở kho tạm. |
| bo-quet-khong-co-cua-chay | P2 | Phụ lục A :336/:339–342/:360–362/:389–407: chỉ bắt KhongDoDuoc/YAMLError, usage dùng SystemExit chuỗi | Một biên CLI phân loại mọi lỗi chưa biết thành KHÔNG ĐO ĐƯỢC; JSON+errors là điều kiện của rc=1 | Thiếu Git/argv, decode, ValueError/RecursionError đều rc=1/no JSON ở r3; HINT cho 2. OS kill/timeout chưa đo, caller phải coi output không đủ là không đo được. |
| bang-duong-phan-loai-sai | P3 | Header :19 gán hunk sai hàm; Phụ lục A :410–416/:433/:435 gán sai nguồn/cửa chạy và “ca cuối” | Đối chiếu nhãn/vị trí với diff và script/output thật; tách CLI khỏi seam | +13/−19 đúng nhưng hunk ở t131×2/t139/t192; table 16 dòng, script/output 15 CLI, race trực tiếp tự đo riêng. Không đổi hành vi executor. |

Bảo toàn slug: lớp provenance không tách riêng commit/blob replacement vì cùng cách chữa; lớp entry point gom lỗi import/spawn/decode/parser/tài nguyên vì cùng biên phân loại. Lớp P3 giữ slug gán sai vị trí/phân loại từ lượt 1; **không** nói D7/D8 tái hỏng — biểu hiện mới nằm ở nhãn của phép đo nền và tự kiểm. Không mở lớp số liệu chỉ vì ref/time khác snapshot.

## BẢNG SĂN

### HƯỚNG 1: Bảng mã thoát mới ở biên gọi Git/giải mã

- Giả thuyết: rc=2 mới chỉ bắt Git trả mã lỗi, không bắt lỗi trước khi có CompletedProcess.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py io`.
- Output thật: `no_args rc=1 json=False`; `no_git rc=1 json=False FileNotFoundError`; `invalid_utf8 rc=1 json=False UnicodeDecodeError`; `utf16 rc=1 json=False UnicodeDecodeError`; đối chứng UTF-8 tiếng Việt `rc=0 json=True errors=[]`.
- Kết luận: LỖI. Bảng “lỗi Git/đầu vào ⇒ 2” chưa phủ các nhánh này. `no_git` là không đo được nhưng rơi vào mã dành cho lease hỏng. Giữ slug `bo-quet-khong-co-cua-chay`, trạng thái **VÁ SINH LỖI MỚI**: entry point đã có, hợp đồng thoát mới chưa đủ. Không phải âm giả xanh: không JSON vẫn buộc cổng từ chối.

Bổ sung HƯỚNG 1 — parser không chỉ ném YAMLError. Lệnh `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py yaml`: ngày 2026-02-31, `!!int nope`, integer 5000 chữ số đều `rc=1/no JSON/ValueError`. YAML `[` thông thường lại `rc=1/JSON/errors=parse`; ngày hợp lệ và ngày sai có nháy đều `rc=0/JSON`. Không tính bổ sung này là hướng độc lập: cùng lớp phân loại lỗi entry point. Giới hạn chuyển integer của Python không được đánh đồng với bằng chứng lease sai schema.

### HƯỚNG 2: OID đã chốt có thực sự quyết định bytes được đọc?

- Giả thuyết: Git replace làm `ls-tree <OID>` đọc cây khác, dù map ref/OID đã cố định.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py provenance` (kho Git tạm, replacement commit có cùng file nhưng sửa int thành chuỗi; chạy nguyên entry point hai lần).
- Output thật: `replace_on rc=0 refs={'refs/heads/main': '4ca4f002…'} errors=[] blob=f2226976…`; `replace_off rc=1`, cùng refs/OID, `errors=[['ops/leases/a.yaml','lease_id=1000']] blob=0a0253c7…`. Hai lần chỉ khác `GIT_NO_REPLACE_OBJECTS=1`.
- Kết luận: LỖI P2, **CÒN MỞ** lớp `bo-quet-chung-cu-khong-neo-anh`. Race tên ref đã đóng; nhưng cùng map vẫn chứng nhận bytes khác OID. Không khẳng định replacement đang có ở snapshot thật. Cần tắt replace cho mọi lệnh đọc object và khóa bằng phản chứng trên cả commit/blob. Ca cùng path hai blob vẫn đếm đúng 2 cặp; không khai lỗi số mẫu.

Bổ sung HƯỚNG 1 — tài nguyên: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py resource` cho tài liệu sâu 1200 tầng (2420 bytes) `rc=1/no JSON/RecursionError`; tài liệu 2000021 bytes hợp lệ `rc=0/JSON/errors=[]`. Không suy đã thử mọi kích thước hay OOM. Độ sâu/tài nguyên cần phân loại không đo được; không cần cấm một tệp chỉ vì lớn nếu vẫn đo thành công.

### HƯỚNG 3: Ref symbolic không phải HEAD và object thiếu

- Giả thuyết: sửa bộ lọc suffix ở r3 làm bỏ nhầm alias hợp lệ hoặc không bắt object mà tree tham chiếu bị thiếu.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py refs`.
- Output thật: symbolic HEAD hợp lệ không có trong map; symbolic alias có mặt cùng OID với main, rc=0; mất blob ⇒ rc=2/KHONG_DO_DUOC. Dangling symbolic alias không được Git liệt kê, rc=0/errors=[], `map_has_dangling=False`.
- Kết luận: KHÔNG PHẢI LỖI đã chứng minh. Alias trỏ object hợp lệ được quét; object thiếu bị chặn. Alias dangling không định danh commit/lease nào, nên chưa có phản chứng lease bị bỏ sót; vẫn phải đối chiếu nguồn refs được cấp theo A9, không nhận một map rỗng làm bằng chứng đầy đủ. Không mở yêu cầu mới quét raw `.git/refs` từ phép thử này.

### HƯỚNG 4: Closure mới có chỉ tới job thật và đòi ghi ngoài phạm vi?

- Giả thuyết: closure điền tay nêu check không tồn tại hoặc chuyển nghĩa vụ land sang executor chỉ được sửa hai tệp.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py contract`; đọc protocol §3.2/§3.2.1/§4/§8/§13 và lease wp461 có Mission #470.
- Output thật: ci.yml có jobs `gate`, `gate-ops`, `gate-registry`, `gate-packet-loop`, đều matrix `os`; thu-hoi có workflow/job `thu-hoi`; `POLICY_AT_BASE=128` (không có path policy); lease wp461-exec-1g3 dẫn miễn trừ trường dispatcher theo #470.
- Kết luận: KHÔNG PHẢI LỖI. Tên job Ubuntu khớp cấu trúc YAML; không tuyên bố chúng đã chạy trên GitHub. Chuẩn protocol có closure do dispatcher, nhưng prompt cấp xem ngoại lệ #682 như lời khai đã chọn; phạm vi và thời hạn rõ, closure được băm, không lấy wp461 làm authority thay #682. `land_obligations` thuộc vai land theo §4/§13, không tự nới write set executor. Nền mới là tổ tiên candidate (`ANCESTOR=0`), revision mới ghi quyết định bền; không có product diff bị che.

### HƯỚNG 5: Mẫu số của ảnh r3 và phép đếm độc lập sau đổi nền

- Giả thuyết: 562/562 chỉ đúng vì cùng một cấu trúc khử trùng che lỗi; hoặc ref_count 508 được giữ như hằng ở ảnh mới.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/measure.py`; `PYTHONDONTWRITEBYTECODE=1 python goi/independent.py` (đọc bytes Git bằng bộ quét độc lập, tắt replace).
- Output thật: checkout `509 ref / 562 blob / 562 cặp / mapping=562 / id=562 / str=562 / errors=[]`; mirror `508/562/562`; map origin/mirror `508=508`, tên+OID bằng nhau, thiếu/thừa=[]; checkout có 1 local head. Phép độc lập cũng trả `509/562/562`, toàn str, errors=[]; refs/replace hiện rỗng. Suite `187/187 đạt; đã chạy=187, bỏ qua=0`, rc=0, shellcheck 0.9.0/actionlint 1.7.7.
- Kết luận: KHÔNG PHẢI LỖI số lease. 508 của §8 = 506 remote + 2 local lúc soạn; hiện 509 = 508 remote + 1 local. Prompt mô tả 505 remote không khớp ảnh thực cấp, nhưng hai định danh bắt buộc đúng và mirror khớp toàn map. Không có map lịch sử 07:59 nên chưa truy nguyên chính xác từng ref tăng; không lấy commit timestamp làm thời điểm ref xuất hiện. Các số hiện tại không bác số lịch sử hay chứng minh đã đo live. Lần đầu script đo MAX dùng parse tiền tố quá hẹp gặp t02b, đã sửa dùng regex và chạy lại; đó là lỗi dụng cụ, không là finding.

### HƯỚNG 6: Chú giải mới về đổi nền và bảng tự kiểm có khớp hiện vật?

- Giả thuyết: phần diễn giải ngoài HINT gắn phép đo vào nhầm ca/hàm dù số tổng vẫn đúng.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/hunts.py contract`; `PYTHONDONTWRITEBYTECODE=1 python goi/independent.py`; đọc `tukiem_r3.sh`/`.out` và SPEC :19/:412–436.
- Output thật: numstat +13/−19, bốn hunk thực ở `t131`, `t131`, `t139`, `t192`; header spec ghi `t130`, `t131`, `t139`, `t191`. `SELFTEST table_rows=16 supplied_output_cases=15 script_has_update_ref=False`. Dòng cuối bảng ghi rõ gọi quet trực tiếp tại seam; câu dẫn lại nói bảng chạy qua entry point và chỉ tới script không chứa ca race. “Ca cuối” sau bảng nói ref hỏng dù ca cuối là race.
- Kết luận: LỖI P3, **TÁI PHÁT** lớp `bang-duong-phan-loai-sai`: gán sai vị trí/phạm vi của bằng chứng. D7/D8 đã sửa đúng; biểu hiện mới ở mô tả nền và bảng tự kiểm. Ca race đã được reviewer tự đo lại và đúng, nên không nâng thành lỗi hành vi hay phủ nhận kết quả lịch sử. Sửa nhãn và nêu riêng nguồn của ca trực tiếp; không bịa output CLI cho ca seam.

Bổ sung HƯỚNG 5 — người giữ có biến thời gian: `PYTHONDONTWRITEBYTECODE=1 python goi/holders.py` (seam duy nhất là nguồn tên nhánh máy chủ thay bằng map mirror đã đối chiếu; không gọi mạng). Output `SCANNED=562`, cả hai tệp `NGƯỜI_GIỮ 0`, rc=0. Log đầy đủ `goi/holder-lease_publish_test.py.log` chỉ rõ T131 **HẾT_HẠN**; lease tại `refs/remotes/origin/claude/bookkeeping-676` có hạn **2026-09-29T08:15:00Z**, không có bia mộ. Điều này không bác số 1 của mốc 07:59Z: phép review đã qua giờ hết hạn. Không dùng số 0 hiện tại để tự cấp lease hay tuyên bố đã đo máy chủ.

### HƯỚNG 7: Nghĩa vụ hai thứ tự ở A2 đối với spec #677 mới trong snapshot

- Giả thuyết: sau D3, mutant L có thể sống ở biên công khai dù dữ liệu đang đỏ, khiến “giữ test #677 xanh” bị hiểu thành giữ nguyên oracle cũ.
- Lệnh: `git -C cay-kho show c78a5d0651dd80023cde04b04c378511d8fb7af0:ops/specs/dot-bien-l-bien-cong-khai-r1.md > goi/spec-677.md`; `PYTHONDONTWRITEBYTECODE=1 python goi/interaction.py` (trích nguyên giàn phụ lục #677; chỉ thay các biến thể mã trong scratch).
- Output thật: spec #677 sha256 `81468e21c7a7d32167d210b17813dab2b825992a1587b86d8bc8b3dc9142a4da`, soạn sau 08:01Z. Null/Issue: nền và L đều rc=1, nhưng GET 0→1; mô hình D3 và L đều rc=1/GET=0. Bool/float/date + PR + dấu: nền rc=1, L rc=0/skip=True; mô hình D3 và L đều rc=1/GET=0/skip=False. Đối chứng chuỗi giữ rc=0/POST=1 ở mọi vế.
- Kết luận: KHÔNG PHẢI LỖI mới đã chứng minh trong r3. Lời “chưa có spec lúc 07:59” là lịch sử, không còn là trạng thái snapshot hiện tại. Mất răng của L đúng điều A2 đã dự liệu; A2 cho phép đổi ý nghĩa ca kế thừa trong chính test file và bắt chuyển phép giết L sang D2 trực tiếp. Phải giữ các quan sát an toàn của ca biên, không báo ca biên đã giết L sau D3. Q10 của #677 khai thứ tự #677→#678, nhưng chỉ xem đây là lời khai trong spec sibling; không tự thay authority/lease. Chưa có implementation #677 trong candidate để xác nhận catalog thật đã được thích nghi. Không mở finding chỉ vì snapshot sibling mới hơn mốc lịch sử.

### HƯỚNG 8: Đổi nền có che đường workflow/D8 hoặc thêm chuẩn hóa chuỗi không?

- Giả thuyết: các phép đo §1/A3 vẫn lấy blob cũ không áp cho nền mới; hoặc D1 khiến executor bỏ cả D8 của ai-dang-giu.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python goi/runtime.py`; inventory `rg -n 'lease_id|thay_the_cho|da_bi_thay_the|cap_lai_cho|\.stem|name\[:-5\]' cay-kho/ops/lease_publish.py` (`goi/identity-paths.log`); đọc luồng caller và `goi/callers.log`.
- Output thật: workflow nền yes `rc=0/POST=0`, fresh-id `0/1`; mô hình D1–D4 yes `1/0`, fresh-id `0/1`. D8 ở nền: check nhận int rc=0, ai-dang-giu nhận int rc=11; thêm D1: check không tới D8 rc=8, ai-dang-giu vẫn tới với int rc=11. Q1 chặn whitespace/newline/Unicode dựng sẵn-tổ hợp/fullwidth; A/a hợp lệ và khác nhau; `!!str 1.5` hợp lệ; YAML khóa lặp dùng giá trị cuối `fresh`.
- Kết luận: KHÔNG PHẢI LỖI. Các đầu vào cho ra cùng chuỗi thuộc cùng danh tính theo objective r3; không cần mở phạm vi loader/Unicode. D8 ai-dang-giu cần chốt độc lập như A7 đã ghi. Không tìm thấy consumer danh tính chưa phân loại trong tệp qua inventory+đọc flow; cap_lai_cho/tên file thu hồi đã kiểm chuỗi/regex/tên tương ứng. Không có caller vận hành ngoài write set cần sửa được chứng minh bởi Q3; grep workflow không có lease_id, caller ngoài hai tệp chủ yếu hồ sơ review/chú thích. Không suy grep phủ mọi caller động.

Các hướng 1–8 kiểm các giả thuyết khác nhau; không tính riêng việc kiểm hash, đọc tài liệu, bảng đối chiếu mục 0, hay các nhánh YAML/tài nguyên của hướng 1 thành hướng mới. Hướng 5 không chỉ chạy suite: đối chiếu mẫu số và map ảnh r3 bằng thuật toán độc lập; hướng 6 kiểm phần diễn giải mới ngoài HINT; hướng 7 sử dụng sibling spec mới chưa có trong các review cũ.

## BẢNG ĐO

Lệnh và UTC: `goi/runtime.py`/`runtime.log`, `goi/measure.py`/`measure.log`, `goi/independent.py`/`independent.log`, `goi/holders.py`/`holders.log`, `goi/history_counts.py`/`history-counts.log`. Tất cả chạy với `PYTHONDONTWRITEBYTECODE=1`; `common.py` đặt TMPDIR vào thư mục có đường dẫn lưu ở `goi/scratch-path`. Suite chạy bằng `review_scratch=$(cat goi/scratch-path); PYTHONDONTWRITEBYTECODE=1 TMPDIR="$review_scratch" python cay-kho/ops/lease_publish_test.py > goi/suite.log 2>&1` từ R; test xác định tài nguyên theo HERE. Không có mã ứng viên nên không khai delta mã đã đạt.

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| §1 true/yes/on/True | bool, str=True; D2=8/D1 qua | từng giá trị đúng, mô hình D1 mới=8 | Có |
| §1 1.5/1.50 | float, str=1.5; D2=8/D1 qua | đúng từng giá trị | Có |
| §1 0x1F/017/1_000 | int 31/15/1000; D2/D1 qua | đúng từng giá trị; thêm 5 cũng int/qua | Có |
| §1 date | date/2026-09-29; D2=8/D1 qua | đúng | Có |
| §1 quoted yes | str yes; D2/D1 qua | đúng, mô hình mới vẫn qua | Có |
| §1 va chạm | sáu cặp rc=9; khác tên rc=0 | mỗi cặp đúng như log COLLISION | Có |
| §1/A3 biên workflow | yes rc=0/POST=0; fresh-id 0/1 | Python thật, gh giữ trạng thái: đúng; strict 1/0 và 0/1 | Có trên nền mới |
| §2 D1/D2/D3/D4 | :861/:949/:668/:1070 | inventory đúng các dòng | Có |
| §2 D5/D6 | :587/:592 và :609/:612 | inventory đúng các toán hạng | Có |
| §2 D7 | :2110/:2123 | đọc ID/lập khóa đúng | Có |
| §2 D8 | :1938/:1942/:1946/:1967 | raw/raw/f-string/str tra sổ đúng | Có |
| §2 D9 | :2074/:2089/:2139/:2143 | chỉ hiển thị như khai | Có |
| §2 sổ thu hồi | :1192 đã đòi str | đọc :1192, kiểm str+regex+tên :1193; cap_lai_cho :1232–1236 | Có |
| §2 packet_loop | :769–771 str | đúng loop/read/guard | Có |
| §2 workflow | 0 dòng đọc lease_id | rg trên workflows/*.yml không khớp (rc=1 của rg) | Có |
| Header đổi nền | sản phẩm không đổi; test +13/−19, bốn hunk | git diff sản phẩm rc=0; numstat 13/19, bốn hunk | Có số; sai nhãn hàm (P3) |
| §6.7 t178 | :7763–7764 | :7763 nối ngữ cảnh, :7764 chứa câu khai thiếu chốt | Có |
| §8 ref remote | 506 so nguồn lúc 07:59Z | snapshot origin/mirror 508/508, map bằng nhau | Khác ảnh; live/lịch sử map KHÔNG ĐO ĐƯỢC |
| §8 tổng ref | 508=506 remote+2 local | checkout 509=508 remote+1 local; mirror 508 head | Khác thành phần ảnh; không dùng số 508 trùng ngẫu nhiên trên mirror làm chứng minh cùng miền |
| §8 blob/cặp/mapping/id | 562/562/562/562 | 562/562/562/562 bằng hai phép quét | Có |
| §8 kiểu/lỗi | str 562, lỗi 0 | str 562, lỗi 0 | Có trên snapshot; không chứng minh dụng cụ đủ mọi miền lỗi |
| §8 lịch sử | retired 0 blob/0 cặp | 0/0 ở mọi ref đã quét | Có |
| §8 người giữ sản phẩm/test | 0/1 (T131) tại 07:59Z | 0/0 sau 08:15Z, T131 hết hạn | Khác do thời gian; không bác mốc cũ |
| §8 suite | 187/187, rc=0, bỏ qua 0 | 187/187, rc=0, bỏ qua 0 | Có; 185/187 là lịch sử thiếu shellcheck |
| §8 dòng sản phẩm/test | 2206/10502 | 2206/10502; nền cũ test 10508 theo diff −6 | Có |
| §8 số ca/max | 187/t192 | len(CA)=187, max tiền tố số=192 | Có |
| §8 mỗi nhánh sau fetch thêm 1, tăng 559→560 | lịch sử, chưa truy nguyên | current HEAD mỗi nhánh được nêu có 2 tệp thêm so 89fc4fa; nhánh G5 còn 2 tệp xóa do khác nền | Không có ref-map lịch sử nên không bác/khẳng định 559→560; không lấy delta hiện tại thay lịch sử |
| Ruff | không đo được | python -m ruff --version rc=1, No module named ruff | Bare lint F và delta ứng viên: KHÔNG ĐO ĐƯỢC |
| Phụ lục tự kiểm | bảng 16 dòng, mô tả qua CLI | script/output được cấp 15 CLI; 1 race trực tiếp; reviewer tự chạy lại race | Sai phạm vi mô tả (P3), không bác hành vi race |
| Mã thoát Phụ lục | 0 sạch, 1 lỗi lease, 2 không đo được | các nhánh lỗi ngoài YAMLError/KhongDoDuoc trả 1 không JSON | Không (P2) |

## KHẢ NĂNG ĐỎ A1–A10

| tiêu chí | bằng chứng và chốt che | giới hạn còn lại |
|---|---|---|
| A1 | runtime.py: đọc YAML qua _doc_yaml, D1 nền=0/strict=8 cho mọi scalar âm; quoted yes vẫn0 | Gọi kiem không tep, bo_qua_han để D6/neo/hạn không che; chưa có ca ứng viên |
| A2 | recheck.py: direct D2 int strict8 → restore/L RETURN; probe vẫn RETURN/GH0 | A2 đã chọn đúng đơn vị; không ép D3 xuống sau mạng |
| A3 | workflow thực 0/0→1/0; đối chứng 0/1; direct D3 base9→strict8 | Không lấy đỏ tích hợp qua D1 làm bằng chứng chốt D3; caller thật dùng helper _buoc_workflow |
| A4 | dung_than trực tiếp bool base trả thân → strict8 | Cài chốt D4 riêng là khả thi; chưa có mutant catalog ứng viên |
| A5 | kho Git tạm và hai chiều đầu vào giết riêng D5_self/D5_peer/D6_self/D6_peer; đối chứng đúng | Quan sát kết quả trong mô hình, không khai đã có TinHieuChotCa của executor |
| A6 | hai ref/path còn hạn trên nền rc11/NGƯỜI_GIỮ1:True | A6 mới đo cả nhãn/ref/path; executor phải gom cả hai sai kiểu trước thoát, không chỉ assert nonzero |
| A7 | runtime.py tách đúng check và ai-dang-giu; D1 chỉ che check | Chưa có D8 ứng viên để giết mutant của chốt đó; cần direct helper như A7, không miễn bằng kết quả check |
| A8 | suite nền chạy thực đủ; hai tệp Python của candidate-spec bằng nền 89fc4fa | Delta ứng viên và Ruff chưa đo; các ca kế thừa #677 phải đổi oracle có khai, không xóa test để delta đẹp |
| A9 | entry point/self-test thật; phát hiện hai P2 ở provenance và phân loại lỗi | Snapshot sạch không đóng được lỗi thước đo; helper mới chỉ nằm trong test file |
| A10 | suite có TinHieuChotCa/chot và cửa phân hạng; A2/A5 có tín hiệu phân biệt quan sát được | Catalog A1–A7 thực chưa có, không thể xác nhận actual target/cause matrix. Yêu cầu đúng tên ca và tín hiệu/cause vẫn cần executor thực hiện |

Các fixture cần thiết sẵn có: `_buoc_workflow` :555 trích bước thật; `_kho_thu` :1506, `_git_fixture` :3746, `_kho_do_thi` :4730 hỗ trợ kho tạm; `GhGia` :193 hỗ trợ seam nhưng không tự là executable trên PATH. `_chay_buoc_dang` :2703 dùng Python stub nên không đủ A3; runtime.py đã chứng minh có thể dựng gh stateful trên PATH và Python thật trong đúng test write set. Không cần sửa workflow/helper ngoài hai tệp được cấp.

## CHI TIẾT TỪNG LỚP

### bo-quet-chung-cu-khong-neo-anh [P2] Map OID còn có thể chứng nhận nội dung replacement
VỊ TRÍ: Phụ lục A :327–328, :339–342, :354, :361; A9 :238–242.

VẤN ĐỀ: Đọc theo OID đóng cuộc đua tên ref, nhưng Git vẫn tra replace object theo mặc định. Kho tạm có main trỏ commit ID int, replacement trỏ commit chuỗi: JSON vẫn ghi OID commit int mà errors=[]/rc=0. Thay blob cũng cho cùng âm giả. Đây là cùng lớp provenance, không là yêu cầu triển khai object-reader mới trong sản phẩm.

HINT: có — nhóm `# lop: bo-quet-chung-cu-khong-neo-anh`, tắt replacement bằng tùy chọn Git ở một cửa chung và bổ sung ca commit/blob replacement.

ĐÃ THỬ: `python goi/hunts.py provenance`; `python goi/verify_hint.py`, đều với PYTHONDONTWRITEBYTECODE=1. Cả commit và blob: r3=0, HINT=1, map bằng nhau. Snapshot gốc refs/replace rỗng; chỉ chứng minh công cụ có đường âm giả, không cáo buộc có lease hỏng trong kho.

ĐỘ TIN: cao.

### bo-quet-khong-co-cua-chay [P2] Bảng rc mới không bao phủ các đường lỗi CLI
VỊ TRÍ: Phụ lục A :336, :339–342, :360–362, :389–407.

VẤN ĐỀ: Import yaml nằm ngoài biên bắt lỗi, spawn/decode có thể ném trước khi kiểm p.returncode, safe_load có thể ném ValueError/RecursionError, sai argv dùng SystemExit(str). Chúng đều rc=1/no JSON, lẫn với mã “lease hỏng”. Vì r3 đòi JSON dương, đây **không** phải đường xanh giả; lỗi là bảng phân loại và tự kiểm không đủ miền. Khả năng phân biệt “có lỗi lease”/“không đo được” đã được hứa là hành vi của dụng cụ nghiệm thu, nên P2 theo ngưỡng prompt.

HINT: có — nhóm `# lop: bo-quet-khong-co-cua-chay`. Đưa import và toàn cửa JSON/CLI vào biên lỗi, chỉ nhận rc1+JSON+errors làm lỗi lease; ngoại lệ chưa phân loại ⇒2. Không bắt BaseException. Ghi riêng giới hạn signal/timeout/OS kill ở caller; không hứa Python bắt được SIGKILL. Không mở giới hạn byte cố định tùy tiện cho lease hợp lệ.

ĐÃ THỬ: hunts.py io/yaml/resource và verify_hint.py. HINT cho good0+JSON, int/parse1+JSON; argv/noGit/noYaml/UTF8/ValueError/RecursionError đều2. Tệp 2000021 bytes xử lý thành công trên r3. Không đo OOM/OS kill hay mọi nền/encoding; không làm tròn thành đã phủ hết tài nguyên.

ĐỘ TIN: cao cho các nhánh đã chạy; không tuyên bố toàn bộ không gian lỗi đã được vét cạn.

### bang-duong-phan-loai-sai [P3] Chú giải mới gán nhầm vị trí và phạm vi bằng chứng
VỊ TRÍ: header :19; Phụ lục A :410–416, :433, :435.

VẤN ĐỀ: Bốn hunk +13/−19 được mô tả là quanh t130/t131/t139/t191, nhưng Git chỉ ra t131 hai hunk/t139/t192. Bảng tự kiểm nói chạy entry point qua script kèm theo trong khi ca race trực tiếp không có trong script/output được cấp; câu “ca cuối” trỏ nhầm ref hỏng. Các ca đúng vẫn đúng; sai ở nhãn nguồn/phạm vi, không đổi mục tiêu thi hành. Lớp D7/D8 cũ đã đóng, biểu hiện cùng hình dạng tái phát ở đoạn r3 mới viết.

HINT: có — nhóm `# lop: bang-duong-phan-loai-sai`, sửa tên ca và tách nguồn CLI/seam, yêu cầu kèm script race khi công bố r4; không tự bịa kết quả mới.

ĐÃ THỬ: `python goi/independent.py`, `git diff --unified=0 1741e0a 89fc4fa -- ops/lease_publish_test.py`, tự chạy `tukiem_r3.sh`, race trong recheck.py. Table=16/script output=15; script không chứa update-ref. Ca race tự dựng đúng map OID cũ và báo lỗi.

ĐỘ TIN: cao về hiện vật được cấp. Không suy phiên soạn chưa từng chạy ca race ngoài script ấy.

## DRY-RUN HINT.patch

Nhãn: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. HINT chỉ nhắm r3; r1/r2 bất khả xâm phạm. Điều phối dùng để soạn revision 4, không sửa đè r3 đã băm. Hunk Python bên trong Markdown là dụng cụ tham chiếu của đặc tả, không patch sản phẩm.

Lệnh đã chạy (R là cwd tuyệt đối được giao):
```sh
PYTHONDONTWRITEBYTECODE=1 python goi/build_hint.py
hint_tmp=$(mktemp -d -p "$R")
cp -a "$R/cay-kho" "$hint_tmp/cay"
patch -d "$hint_tmp/cay" -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Output nguyên văn:
```text
Hmm...  Looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: bo-quet-chung-cu-khong-neo-anh
|--- ops/specs/lease-id-ep-kieu-yaml-r3.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r3.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r3.md
Using Plan A...
Hunk #1 succeeded at 327.
Hunk #2 succeeded at 345.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|
|# lop: bo-quet-khong-co-cua-chay
|--- ops/specs/lease-id-ep-kieu-yaml-r3.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r3.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r3.md
Using Plan A...
Hunk #1 succeeded at 335 (offset -4 lines).
Hunk #2 succeeded at 347 (offset -4 lines).
Hunk #3 succeeded at 388 (offset -4 lines).
Hunk #4 succeeded at 394 (offset -4 lines).
Hunk #5 succeeded at 407 (offset -4 lines).
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|
|# lop: bang-duong-phan-loai-sai
|--- ops/specs/lease-id-ep-kieu-yaml-r3.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r3.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r3.md
Using Plan A...
Hunk #1 succeeded at 18.
Hunk #2 succeeded at 410 (offset -17 lines).
Hunk #3 succeeded at 437 (offset -17 lines).
done
```

Đã áp thật trên chính bản sao tạm để bắt tương tác giữa các nhóm cùng tệp, rồi cmp với bản dự kiến do build_hint.py tạo:
```text
dry_run_rc=0
apply_rc=0
expected_spec_cmp_rc=0
```

`PYTHONDONTWRITEBYTECODE=1 python goi/verify_hint.py` trích scanner từ **bản đã áp HINT** rồi kiểm các ca đối chứng và phản chứng. Output:
```text
good 0 json True
bad_id 1 json True
parse 1 json True
bad_date 2 json False
int_constructor 2 json False
int_limit 2 json False
deep 2 json False
utf8 2 json False
args 2 KHONG_DO_DUOC: KhongDoDuoc: cach dung: python quet.py <goc-kho>
no_git 2 KHONG_DO_DUOC: FileNotFoundError: [Errno 2] No such file or directory: 'git'
no_yaml 2 KHONG_DO_DUOC: ModuleNotFoundError: No module named 'yaml'
REPLACE commit r3 0 hint 1 same_map True
REPLACE blob r3 0 hint 1 same_map True
R2 good entry_rc 0 stdout '' quet (1, 1, 1, []) R3 0 []
R2 blank_list entry_rc 0 stdout '' quet (1, 1, 1, []) R3 1 [['ops/leases/a.yaml', 'thay_the_cho']]
verified_hint=True
```

R2 đã được trích và chạy nguyên khối, không tin bảng tự kiểm: good và blank-list đều entry rc0/stdout rỗng; gọi hàm blank-list cũng báo sạch, còn r3 báo rc1 đúng lỗi. Đây là kiểm bổ sung bắt buộc, không đếm thành hướng săn mới.

## TOÀN VẸN VÀ GIỚI HẠN

Snapshot trước/sau băm mọi tệp tracked/untracked/ignored và Git metadata dưới cả cay-kho lẫn kho.git: `PYTHONDONTWRITEBYTECODE=1 python goi/snapshot.py goi/snapshot-after.json`, so với snapshot-before.json. Output:
```text
snapshot_files_before=3009
snapshot_files_after=3009
delta=[]
```

Chỉ chứng minh không có delta ở hai mốc, không audit toàn bộ syscall. Sandbox workspace-write; kỷ luật đường dẫn giữ mọi script/cache/fixture trong goi hoặc mktemp dưới R. Không dùng mạng, không đổi checkout/mirror, không đăng GitHub. HEAD/tree cuối `4c1915c9d5cd1008699499d0aff13914f390f06c` / `fc0769c29fc11136bc695b24d9f1326d1effc8f0`; băm ba revision khớp prompt. Nguồn authoritative là blob tại reviewed SHA/path, SPEC.md là bản sao cùng băm; không định danh bằng tên nhánh.

Nội dung live #678/#682, byte thân Issue, model/effort thực phục vụ request, Windows, candidate thi hành và bare Ruff lint: KHÔNG ĐO ĐƯỢC hoặc chưa chạy như đã ghi. Không biến `author_association: OWNER` thành bằng chứng người gõ; không bác miễn trừ #682 vì thiếu network. Verdict này chỉ là review đặc tả, không là executor lease, CI check, approval hay land authority.
