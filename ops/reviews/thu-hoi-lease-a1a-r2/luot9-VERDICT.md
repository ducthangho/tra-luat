verdict: changes_requested
reviewed_spec_sha256: ac7e0129b281b517c69e9a2512a05b47d55ad99f0ac964462c061ea511f70bc1
reviewed_sha: 3f1bf2e2e5a77ec2bb1a40bb65b8c26410a3ff12
P1: 0   P2: 1   P3: 0
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); biến thể và effort backend KHONG_DO_DUOC
execution_surface_tu_khai: công cụ exec_command thực thi bash trong cwd, Git 2.43.0, Python 3.11.15; danh tính sản phẩm/launcher KHONG_DO_DUOC
transport_tu_khai: KHONG_DO_DUOC

Lượt 9/10. Tree đã đọc: `04e6c5fa02e0772483135707b9d96488d18c62a3`.
Đã ghi VERDICT tạm trước khi đo và bổ sung bằng kết quả chạy. Hai P1 của lượt 8 đã đóng trong
phạm vi revision 3. Ba lệnh thi công đạt, các chốt mới đổi màu đúng. Còn một P2 ở lời khai số lượng
phần sửa trong `EVIDENCE.md`; không phải lỗi thuật toán hoặc thay đổi vượt phạm vi của SPEC.
Không nâng/hạ hạng vì chỉ còn tối đa một lượt review.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Mục lượt 8 | Trạng thái | Bằng chứng chạy được và phạm vi kết luận |
|---|---|---|
| F17 — `so-do-khong-khop` | **ĐÓNG** | `python3 -B scratch/review9.py integrity`: tám EVIDENCE lịch sử byte-equal blob HEAD. Bảng S mới ghi đúng E7: 430/429, lệch 1; E11: 435/435 chỉ so tên; lượt 3: 435/435 lúc 23:23:57Z; lượt 4: 437/437 lúc 23:47:11Z. Lượt 5–7 được ghi KHÔNG ĐO ĐƯỢC độc lập. Không còn dùng phép so tên để bảo đảm OID hoặc khẳng định mọi lượt lệch 0. Đây là đối chiếu hồ sơ, không phải đo lại máy chủ lịch sử. |
| F18 — `q6-thieu-kiem-id-ten` | **ĐÓNG** ở hợp đồng r3 được review | `SPEC.md:379–408` thay rõ mọi lệnh gốc ở trên bằng hai script `_hk`, băm đúng và ba lệnh cụ thể. `scratch/baseline.json`: cả ba rc0, tự kiểm 35/35, ma trận 27/27, Q6 byte-equal. `scratch/criteria.json`, `scratch/extra-lech.json`: băm sai, số ca đổi, thêm hàng mong LECH đều bị tiêu chí r3 từ chối. R3 vẫn cần human audit theo quyết định đã giao; không tự tuyên bố đã đóng băng. |
| C3 — khai execution surface / transport | **ĐÓNG-MỘT-PHẦN** | Bảng S vẫn chỉ là lời khai có nguồn, không sửa hiện vật reviewer. `integrity.json` xác nhận hiện vật đang đọc; không có run.json/header lịch sử trong packet để xác thực các trường ấy. Lượt này khai đúng bề mặt quan sát được, transport KHONG_DO_DUOC. Không suy từ dòng cấu hình yêu cầu `gpt-6-astra/high` hoặc lời khai của tác giả. |
| C4 — origin cục bộ và bảo đảm ref | **ĐÓNG-MỘT-PHẦN** | Bootstrap hiện tại đạt: origin là endpoint thật; 441/441 cặp tên/OID cache bằng snapshot được cấp, sai khác đối xứng rỗng. F17 sửa đúng lịch sử. Việc đó không hồi tố biến origin cục bộ của lượt 1–7 thành remote thật, không xác thực được số đo lịch sử còn thiếu hoặc advertisement sống. `scratch/integrity.json`, trường `refs`, `history`, `origin`. |
| C5 — Git quote tên rồi bỏ qua | **ĐÓNG** trong bộ đo thi công r3 | `python3 -B scratch/probes9.py`: dùng nguyên bốn fixture có sẵn; gốc rc0, đưa tên vào ngoài miền; `_hk` rc3, có vi phạm, JSON CLI giải mã được. Hai ca DEL/byte mới và hai mutant riêng thực sự đổi màu. F18 không còn buộc executor chạy gốc. |
| C6 — bỏ qua returncode | **ĐÓNG** trong bộ đo thi công r3 | `probes9.py`: kiểm rc 0,1,2,3,127,-9,-15 và tiến trình thật bị SIGTERM. Gỡ chốt rc riêng bị assert chặn; gỡ cả bảy assert thì hàng âm thành `SAI  KHOP chet-im-lang-rc2`, tổng `CO_LECH`, rc1. R3 cho phép duy nhất hàng âm đã định danh, không bỏ qua mọi LECH. |

Không mở lại C2/human audit, F1 prediction-only, F2 cây mốc + (b), ngoại lệ ADR-0044 ≤3 tệp/≤663 dòng,
trần 10 hoặc quyết định revision 3 tối thiểu. C3/C4 còn giới hạn xác minh như lượt trước; không tự
biến thiếu nguồn ngoài sandbox thành một finding mới về số đo sai.

## Findings

### F19 — P2 — `so-do-khong-khop`: lời khai đếm 7 phần sửa nhưng danh sách kèm theo có 8

**Vị trí:** `EVIDENCE.md:11–12` — hiện vật lời khai lượt này, không phải SPEC.

Câu “thay đúng 7 đoạn” đi cùng danh sách tám mục: tiêu đề; hàng revision; thay_the_cho; reviewer;
dong_bang; câu nhánh fetch; §0 vòng 5; khối thi công §8 mục 2. Vì vậy số lượng khai và phần liệt kê
làm căn cứ không khớp. Đối chiếu diff độc lập xác nhận các vùng được phép thực sự giữ đúng phạm vi;
không dùng lỗi đếm này để cáo buộc r3 sửa lén nội dung khác.

**Bằng chứng chạy được:**

```sh
python3 -B scratch/count-evidence9.py
```

Kết quả `scratch/evidence-count.json`: `claimed=7`, `enumerated=8`, `difference=1`, kèm đủ tám mục
trích trực tiếp từ EVIDENCE. `scratch/integrity.json` lưu các vùng thay đổi của diff thật. Các vùng
liền nhau được diff gộp thành sáu opcode thay đổi; sáu opcode không phải số mục trong lời khai.
Không có script tạo r3 trong packet để đếm số lời gọi replace, nên không khẳng định script đã gọi
replace tám lần.

**Xếp hạng:** P2 theo đúng quy tắc “con số sai không chống đỡ thẩm quyền”. Đây là số mô tả thao tác
soạn, không cấp quyền, không là căn cứ human audit hoặc số đo ref thẩm quyền; không phải P1.

**Đề xuất:** bỏ số thao tác không được chứng minh, viết “rồi sửa các phần sau” và giữ nguyên danh
sách. Nếu muốn giữ số, cần định nghĩa đơn vị đếm và làm nó khớp danh sách/bằng chứng. `HINT.patch`
chỉ sửa câu này trong hiện vật review `EVIDENCE.md`. Đã dry-run và áp lên bản sao dưới scratch bằng
`patch -p0 --fuzz=0`, rc0; bản sau áp bằng đúng đề xuất. Không áp vào đầu vào gốc hoặc `cay-kho/`.
Không có hunk SPEC; không cần thay băm r3 hay băm hai script vì finding này.

## Bảng đo lại

| Đối tượng | Thực đo | Hiện vật |
|---|---|---|
| HEAD / tree | đúng header / `04e6c5fa02e0772483135707b9d96488d18c62a3` | `scratch/integrity.json` |
| SPEC r3 | 436 dòng, 55.526 byte, băm đúng header; packet = checkout = blob HEAD | `scratch/integrity.json` |
| SPEC r2 | 400 dòng, 50.574 byte; băm `9bc0fe282fbebc02791f47a30e4ff187b1182a2e5e357ee2e66c04d4f7dac7cd`; bằng bản origin/master | `scratch/integrity.json` |
| Phạm vi r2→r3 | chỉ header, thêm §0 vòng 5, thay chỉ dẫn §8 mục 2; mọi byte còn lại nguyên r2 | `spec_changes`, `spec_delta_in_permitted_blocks=true` |
| DIFF.r2-r3 | payload hunk bằng diff tái tạo, bỏ khác biệt tên đường trong header diff | `r2_r3_patch_payload_equal=true` |
| DIFF.luot8-luot9 | byte-equal `git diff d766717 HEAD`: 2 tệp, +440/−2 | `scratch/integrity.json` |
| DIFF.pr658 | byte-equal `git diff origin/master HEAD`: 16 tệp; chỉ hiện vật review và SPEC r3 | `scratch/integrity.json` |
| Gốc `do_q6.py` | `36d8f1667aaa72a1bf00dfb7d1ded4331cb65efab5a0376bb3506528fd6d89d0` | bằng r2, HEAD và origin/master |
| Gốc `mut_q6.py` | `272dc1e82a32331348f59c182803c7cada373f98fbbdd6d4f91ce40d6641e794` | bằng r2, HEAD và origin/master |
| Thi công `do_q6_hk.py` | `0ec537e48b34631eee1e6161be2419bb7ba861a5a446b89afd4937672a974967` | khớp SPEC:388 |
| Thi công `mut_q6_hk.py` | `c4f04f03cf781089ae51faf1e8e63f1d7773bf301d2d61de0919f85a8428bb94` | khớp SPEC:389 |
| Tự kiểm | rc0, 35/35, 35 dòng DAT, 0 HONG, stderr rỗng; byte-equal log cấp | `scratch/self.out`, `scratch/baseline.json` |
| Ma trận | rc0, 27 DUNG, 0 SAI, cuối TAT_CA_KHOP; duy nhất DUNG LECH chet-im-lang-rc2; byte-equal log cấp | `scratch/matrix.out` |
| Q6 thật | rc0, 6.128 byte; sha256 `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61`; byte-equal JSON ghim | `scratch/q6.out` |
| Giá trị Q6 | 89/89, ngoài miền 3, vi phạm 0, cặp hai chiều 11, một chiều 3, KXD 0, giữ 0 | `scratch/final-audit.json` |
| Digest cặp | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | `scratch/q6.out` |
| Mốc / clock | mốc là tổ tiên HEAD và origin/master, cả hai rc0; giờ commit `2026-09-10T11:55:37+07:00` = clock ghim | `scratch/final-audit.json` |
| Ref hiện tại | 441/441 tên/OID, lệch 0; snapshot sha256 `9d58ae52ceded0c21ffa825f9a51a0170a45cfbf3e44c86b7c238849cb3b1b4b` khớp .mirror-info | `scratch/integrity.json` |
| HINT lượt này | chỉ EVIDENCE.md; nhãn đúng; dry-run, áp bản sao và cmp đều đạt | `scratch/final-audit.json` |
| Bảo toàn đầu vào | băm 11 tệp đầu vào kiểm lúc đầu/cuối không đổi; HEAD không đổi; git status sạch | `scratch/final-audit.json` |

`d766717` là mốc sau khi tác giả xử lý lượt 8; head thực sự được lượt 8 review là `4abfdeb`.
Đã đọc thêm diff `4abfdeb..HEAD` để kiểm các thay đổi F17, DEL/byte và mutant không nằm trong
`DIFF.luot8-luot9.patch`. Không lấy riêng diff từ d766717 để khai đã review toàn bộ delta sau lượt 8.
27 là số hàng ma trận, gồm gốc, đối chứng và hàng chốt bị che; không phải 27 mutant đều bị giết.

## Nghiệm thu

Khối thi công r3 đáp ứng mục tiêu F18: tên/băm đúng, ba lệnh chạy được, tiêu chí không chấp nhận
mọi LECH, dữ liệu Q6 không đổi. Các điều kiện mới đều có đối chứng đỏ ở phần dưới. Không phát hiện
bộ đo sai nào qua được toàn bộ hợp đồng ghim băm + chạy đúng lệnh + đọc kết quả trong các phép thử.

Còn F19 P2, nên ngưỡng 0 P1/P2/P3 chưa đạt và verdict là `changes_requested`. Đề xuất sửa nằm hoàn
toàn trong hiện vật lời khai; không đòi đổi đặc tả đã đo. Đây là review đặc tả/bộ đo, không phải
nghiệm thu implementation A1a, cấp lease, CI, human audit hoặc quyền merge.

Tiêu chí bản in không phải cơ chế xác thực xuất xứ log: một văn bản tự gõ chỉ có dòng tổng kết
35/35 vẫn thỏa riêng ba điều kiện đọc log tự kiểm. Đã thử trường hợp đó trong `criteria.json`.
Nó không chứng minh đã chạy script ghim và không thay thế nghĩa vụ chạy đúng lệnh. Không nâng một
log giả tùy ý thành phản chứng rằng chính bộ đo ghim đã tạo ra kết quả sai. Ngược lại, các bản sao
script thực sự đổi bên dưới đều bị băm và/hoặc điều kiện kết quả chặn.

## Phản chứng đã chạy

Các runner trong scratch tự đặt môi trường sau trước khi gọi Git hoặc script con:

```sh
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL="$PWD/scratch/gitconfig.empty"
export TMPDIR="$PWD/scratch/tmp"
export GIT_OPTIONAL_LOCKS=0
export PYTHONDONTWRITEBYTECODE=1
```

Config global là tệp rỗng. Kho giả, mutant và mọi đầu ra ở scratch. Không gọi mạng, không dựng
helper/object Git giả; các tên nhạy cảm chạy ở đây đều lấy nguyên fixture đã cấp, không tự soạn tên
thoát cây, đồng tự Unicode hoặc chuỗi thoát mới. Đọc script gốc để đối chứng không thay byte gốc.

**Tái chạy ba lệnh:** `python3 -B scratch/review9.py baseline`. Runner dùng cwd `cay-kho`, đường dẫn
script tương đối đúng như SPEC; `<kho>` là đường tuyệt đối tới cay-kho; `<tmp>` là thư mục đã tạo ở
scratch/matrix. `baseline.json` lưu argv, cwd, rc và băm từng stdout. Cả ba stderr rỗng.

**Từng tiêu chí dương đều đỏ được:** `python3 -B scratch/criteria9.py`. Có 14 phép đổi bản in/băm/rc
và một bản sao script bỏ ca thật. Các phép riêng biệt kiểm:

| Thay đổi thử | Chốt đỏ |
|---|---|
| Đổi byte mỗi script | băm tương ứng, đo độc lập với bảng SPEC |
| Đổi rc từng lệnh thành 2, giữ stdout đẹp | rc0 của đúng lệnh ấy |
| Tổng tự kiểm thành 34/34 | dòng cuối cố định 35/35 |
| Thêm HONG, vẫn cuối 35/35 | 0 HONG |
| Cuối ma trận thành CO_LECH | TAT_CA_KHOP |
| Bỏ một hàng DUNG | đúng 27 hàng |
| Thêm SAI, giữ 27 DUNG | 0 SAI |
| Đổi gốc thành DUNG LECH, vẫn 27 DUNG | duy nhất đối chứng âm được phép |
| Đổi tên đối chứng âm hoặc đổi nó thành KHOP | phải có đúng đối chứng định danh |
| Thêm một byte khoảng trắng vào JSON Q6 | cmp chính xác từng byte |
| Bản sao script bỏ ca sạch, chạy thật rc0, cuối 34/34 | cả băm script và dòng tổng kết |

**Khai thêm mong LECH có bị lọt không:** `python3 -B scratch/extra-lech9.py` sửa bản sao harness để
hàng gốc có tập đích sai và khai mong LECH. Chạy thật vẫn rc0, TAT_CA_KHOP, 27 DUNG, 0 SAI, nhưng
có **hai** DUNG LECH; tiêu chí duy nhất đối chứng âm bác, và băm harness cũng lệch. Kết quả ở
`scratch/extra-lech.json`. Đây chứng minh chỉ xem rc/TAT_CA_KHOP/số DUNG sẽ thiếu, còn r3 đã có
hai điều kiện bổ sung chặn đúng trường hợp này.

**Bốn mutant tên tệp:** `python3 -B scratch/probes9.py`, dùng bản mutant do chính ma trận đã cấp sinh:

| Mutant | rc suite | Tập HONG thực đo |
|---|---:|---|
| doc-ls-tree-khong-z | 1 | ten-co-tab, ten-xuong-dong-sau-duoi, ten-DEL-sau-duoi, ten-byte-sau-duoi |
| bo-chot-ky-tu-dieu-khien | 1 | ten-xuong-dong-sau-duoi, ten-DEL-sau-duoi |
| bo-rieng-DEL | 1 | ten-DEL-sau-duoi |
| bo-chot-utf8 | 1 | ten-byte-sau-duoi |

Không Traceback, stderr rỗng; tập bằng đúng khai. Chốt tên vẫn che tab khi chỉ gỡ chốt ký tự điều
khiển; không khai mọi fixture cô lập. CLI trên bốn fixture gốc cũng được chạy riêng với bản sao
byte-equal của lease_publish.py: gốc rc0, `_hk` rc3, JSON bằng báo cáo gọi hàm; cả bốn lỗi được
phân loại thay vì crash.

**C6:** classifier từ chối rc2/3/127 và mã âm; target rỗng chỉ nhận 0, target có phần tử chỉ nhận 1
với đúng tập HONG. Tiến trình Python con thật bị SIGTERM trả -15, không stdout/stderr, bị từ chối.
Bản sao bỏ chốt rc nhưng giữ assert chết AssertionError trước ma trận. Bỏ thêm bảy assert cho
`SAI  KHOP chet-im-lang-rc2`, `CO_LECH`, rc1; đối chứng âm có tác dụng độc lập với assert.

**Đối chiếu lời khai và kiểm HINT:** `python3 -B scratch/count-evidence9.py` và
`python3 -B scratch/final-audit9.py`. File sau lưu rc dry-run/áp bản sao và kiểm lại băm đầu vào.
Không có đề xuất sửa SPEC dạng mã hoặc hunk trong HINT.

## KHÔNG ĐO ĐƯỢC

- Advertisement máy chủ sống, nguồn và thời điểm tạo snapshot, CI/REST comments. Phép so 441/441
  chỉ xác nhận cache bằng snapshot được cấp; không tự chứng minh snapshot thực sự do GitHub trả.
- run.json, stderr header, launcher và workspace lịch sử ngoài cwd. Bảng S về model/effort/surface/
  transport/thời gian vẫn là lời khai; không dùng nó để tự xác thực lượt này hoặc các lượt trước.
- Script tạo r3 và số thao tác replace của script ấy; F19 chỉ đối chiếu số mục được công bố.
- Chưa đo byte tên Git ngoài bốn fixture đã cấp. Các tổ hợp mới giữa byte không UTF-8 và ký tự điều
  khiển, đường thoát cây, đồng tự hoặc helper/object giả chỉ là hướng cần executor khảo sát bằng
  lời; không dựng chúng và không khai đã thử hoặc đã chứng minh lỗi.
- Không chạy ai-dang-giu tới origin thật, CI Windows/LIVE hoặc bộ nghiệm thu A1–A22 của implementation
  tương lai. Không mở lại các quyết định chủ kho chỉ vì sandbox không thể readback mạng.
