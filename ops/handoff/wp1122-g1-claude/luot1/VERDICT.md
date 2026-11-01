verdict: changes_requested
reviewed_sha: 30ee4ae1b62170c86b8c75e6b0c73663ab934d88
spec_sha256: 198e06f0f7ef6659fb711ef02ff3558ba5c4a63da1c7127b559c5fd8b0fdacb8
Ket qua: 0 P0, 1 P1, 1 P2, 0 P3.

Packet #1122 r1/g1, lease được giao `wp1122-r1-g1-claude`, review_class `sensitive`, lượt 1. Base: `c82047da4d6f9546ce1d68282c37acf9567b74bc`; reviewed tree: `2be2ced94bea17c287e57c8dc6c5f664b8280506`. Hai mở rộng được chủ kho duyệt trong prompt được tính vào nghiệm thu, không bị coi là lệch scope.

Reviewer: Codex/OpenAI, họ GPT-6 theo cấu hình phiên; không có chứng cứ độc lập xác định biến thể model/effort của từng request. Công cụ thực thi là shell cục bộ trong sandbox Linux qua API, transport machine; không tự nhận là ChatGPT Web hoặc đo Windows. Executor Claude theo packet. Không suy identity từ Git actor; verdict này không cấp quyền merge/land. Không có lượt review trước để đối chiếu.

Môi trường: Python 3.13.18, Ruff 0.16.9. `/tmp/.git` tồn tại và rỗng/read-only. `/var/tmp` không ghi được. Không đổi permission/config để làm probe xanh, không gọi API mạng/CI và không dùng credential thật; fixture mới đều dùng dữ liệu inert. Helper pip ở suite HEAD đầu có thể thử truy cập index trước khi thất bại; đã nhận ra đường này và ép PIP_NO_INDEX cho mọi phép đối chứng tiếp theo, không coi fixture thiếu gói là đã đo. Các bộ cuối được chạy với `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1`. Lượt suite HEAD đầu chưa đặt hai biến pip; mạng bị sandbox chặn và tám fixture phụ thuộc dựng venv/pypdf bỏ qua. Lượt HEAD offline đối chứng đã hoàn tất với cùng kết quả và cùng tên lỗi/bỏ qua như base.

## BANG NGHIEM THU

Các lệnh dưới đây chạy từ `cay-kho/`; script evidence tự đặt đường dẫn theo `__file__`, chỉ viết ngoài checkout. Trong lệnh suite/mutation, dùng ba biến môi trường nêu trên. Lệnh script cần chạy theo thứ tự inventory → probes → encoding_behavior. Log và mã thoát thật được lưu ở `../evidence/`.

| Tiêu chí | Lệnh/phương thức | Output thật/bằng chứng | Đạt? |
|---|---|---|---|
| N0 Windows: tái hiện trước vá | Đọc prompt, `git log --format=%B BASE..HEAD`; không có Windows/log CI gốc offline | Prompt cung cấp run 41328709141/head 4423d18 và `TypeError: the JSON object must be str, bytes or bytearray, not NoneType`; không tự xác minh được `_readerthread`/cp1252 hay thứ tự run | KHÔNG ĐO ĐƯỢC độc lập; không quy thành lỗi code |
| N0' Linux base cùng rig | Clone cục bộ `git clone --no-hardlinks --no-checkout cay-kho evidence/base`, checkout detached BASE; chạy hai lệnh suite/mutation trong clone | Suite `319/342`, tổng 352, bỏ qua 10, hỏng 23, rc=1; mutation `516/548`, không đo 4, 32 hỏng, rc=1 | Đã đo đầy đủ nền cục bộ; giữ nguyên các lỗi môi trường |
| A1: chuyển assertion + khóa AST | `python3 ../evidence/inventory.py`; `python3 ../evidence/probes.py` | Đổi đủ 57 assert/11 ca và 8 raise/2 ca; còn đúng ba ca cố ý. Khóa xanh; 3 mutant assert/raise/tên thừa đều `giet`, `own_signal=true` | ĐẠT phạm vi cú pháp SPEC và mở rộng |
| A2: chi tiết trực tiếp 160 ký tự | `python3 ../evidence/probes.py` | `r1122_loi_mang_thong_diep_cat_160` qua; bỏ message/đổi trần đều bị chính ca giết | ĐẠT A2; mục tiêu 3 toàn bộ reporter CHƯA ĐẠT (F01) |
| A3 Windows exact HEAD | Không chạy được trên rig; không gọi mạng theo chỉ thị | Prompt khai run 41330126129, job windows-latest, runner_id 1000032894: mutation 440/440, không đo 118; suite 281/281, bỏ qua 74, hỏng 0 | KHÔNG ĐO ĐƯỢC độc lập, không nhận lời khai là đã tự đọc log |
| A4 Linux HEAD/base | `ls -d /tmp/.git`; `python3 .claude/dev/launcher_test.py`; cùng lệnh thêm `--dot-bien` | HEAD suite 322/345, tổng 355, bỏ qua 10, hỏng 23; base 319/342, bỏ qua 10, hỏng 23. Mutation HEAD 522/554, base 516/548, mỗi bên 4 không đo; cùng 32 neutral đỏ. Tập hỏng và bỏ qua giống hệt nhau | Delta suite và mutation = 0 trên tập chung; không gọi N/N xanh |
| A5 Ruff F | `ruff check --no-cache --select F --output-format json .claude/dev/launcher_test.py scripts/tl.py` ở HEAD và base | Cả hai rc=1, 17 lỗi: launcher_test.py 5 F841; tl.py 12 F821 | ĐẠT delta=0 trên Ruff có sẵn 0.16.9; chưa đo đúng pin CI 0.15.15 |
| A5 doctrine-scan | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0 | ĐẠT |
| A5 whitespace | `git diff --check BASE HEAD` | Output rỗng, rc=0 | ĐẠT |
| A5 check run ci.yml exact HEAD | Không có check-run receipt trong bundle; không truy cập mạng | Không có phép đọc check run | KHÔNG ĐO ĐƯỢC |
| A6 sau land | Chưa land, ngoài quyền reviewer | Không chạy | CHƯA ĐO ĐƯỢC theo SPEC |

## BANG DO

Cách tìm khẳng định: `python3 ../evidence/claims_extract.py` duyệt toàn bộ dòng thêm trong diff, dùng tokenize tìm comment mới và AST lấy mọi docstring bị hunk chạm, cộng toàn bộ commit message BASE..HEAD. Kết quả 186 dòng thêm, 4 comment, 4 docstring, lưu nguyên văn `claims.json`. Đọc cả dòng xóa, nhánh bắt lỗi, caller và consumer liền kề; dùng `inventory.py` đối chiếu AST hai revision. Đây không phải bộ lọc hoàn chỉnh về nghĩa: lời khai lịch sử, string sinh code, helper/call graph và quy ước liên tệp vẫn phải soi riêng; bảng không đặt trần phát hiện. Phản chứng bổ sung được ghi phía dưới, kể cả khi không có trong danh sách executor.

| Khẳng định | Diff/commit khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Base có 12 ca, 58 assert; helper 0 | SPEC, lý do chuyển | `inventory.py`: đúng 12 ca/58 câu; helper trực tiếp 0 | Có |
| Chuyển 57 assert trong 11 ca | Commit fcada389 và 57 hunk | `inventory.py`: `converted 57 cases 11 mismatches []`; điều kiện và message cũ giống AST, ca không có message nhận biểu thức mô tả | Có |
| Raise AssertionError tín hiệu được đổi, giữ ba ca cố ý | Commit 30ee4ae và allowlist | Base 11 raise trực tiếp, HEAD 3: 8 chuyển trong t33 (1), storage (7). HEAD còn 1 ast.Assert và 3 ast.Raise, đều trong đúng ba tên allowlist | Có |
| Ca Windows không phụ thuộc nền khi quét | Docstring khóa assert | `probes.py`: ba mutant Windows/assert/allowlist chết ngay trên Linux bằng tín hiệu chính khóa | Có; không thay đo hành vi Windows |
| Hai đường assert/raise, gồm raise Name và hàm lồng | Docstring khóa assert | `probes.py`: raise Name, nested assert và nested raise đều `giet`, own_signal=true | Có trong @ca ở module; không suy phủ helper/alias |
| Allowlist không mục dần | Code so bằng đúng tập | Mutant thêm t73: `cho phep khong con dung ['t73_doctor_phai_do_bash_va_npm']` | Có |
| Chi tiết lỗi trực tiếp cắt thông điệp đúng 160, rỗng chỉ có loại | `mo_ta_loi`, A2 | `probes.py`: TypeError 500 → đúng 160 x, vẫn `loi`; nhánh rỗng đọc trực tiếp trong helper | Có ở cham_mot_ca |
| Reporter cũng có thông điệp cắt đúng 160 | Mục tiêu 3 + comment kênh kết quả | `probes.py`: suite/CLI in 500; kênh TypeError lặp loại, còn 149 x | Không; F01 |
| Thêm encoding vào 14 chỗ Python, để shell/git nguyên | Commit 30ee4ae | `inventory.py`: 14 vị trí thêm; 17 text-mode Python tổng cộng (3 chỗ đã có), 22 text-mode shell/git/hệ thống không đổi | Có |
| Khóa bảo vệ giải mã UTF-8 | Tên ca `r1122_con_python_giai_ma_utf8`, mở rộng đã duyệt | Bỏ keyword bị bắt; đổi cp1252 hoặc None vẫn qua. `encoding_behavior.py`: `review ✓` → `review âœ“` mà khóa vẫn xanh | Thiếu răng; F02 (P2), không có lời gọi sai đang tồn tại trên HEAD |
| Gốc Windows cp1252 → reader thread → stdout None → TypeError | Docstring và commit | Lịch sử log không có để tự đo; code launcher hiện ép stdout UTF-8, nhưng không phải bằng chứng tái hiện Windows | KHÔNG ĐO ĐƯỢC độc lập |
| Sáu đột biến thêm vào catalog thật sự giết ca đích | Bảng DOT_BIEN_HARNESS | `probes.py` chạy cả sáu trên bản sao, tất cả own_signal=true; catalog đầy đủ cũng in cả sáu OK 1/1 | Có ở phép đo độc lập từng mutant |
| Không đổi khớp phai_chet/neutral | Mục tiêu 3 | `probes.py` NAME_MATCH: `SAI, 0, 1`, không cấp tín dụng dù message có dấu phẩy/ngoặc/xuống dòng. `ket_luan_mutant` dùng key tên và loai, không parse chi tiết | Có |

## BANG TEST

| Bộ | N/M | Bỏ qua/không đo | rc |
|---|---|---|---|
| Base suite (offline) | 319/342; tổng 352; hỏng 23 | 10 | 1 |
| HEAD suite ban đầu | 322/345; tổng 355; hỏng 23 | 10 | 1 |
| HEAD suite offline đối chứng | 322/345; tổng 355; hỏng 23 | 10 | 1 |
| Base --dot-bien | 516/548; 32 hỏng neutral; catalog 552 | 4 | 1 |
| HEAD --dot-bien | 522/554; 32 hỏng neutral; catalog 558 | 4 | 1 |
| Ba khóa r1122 ở HEAD | 3/3 | 0 | Script probes: 0 |
| Sáu mutant #1122 độc lập | 6/6 chết đúng ca, own_signal=true | 0 | Script probes: 0 |
| Gợi ý vá trên bản sao: bốn khóa r1122 | 4/4 | 0 | Script build_hint: 0 |
| Sáu mutant cho gợi ý vá | 6/6 chết đúng ca, own_signal=true | 0 | Script build_hint: 0 |

Đối chiếu mutation dùng `python3 ../evidence/summarize.py`: catalog base 552 và HEAD 558, toàn bộ mục đều có dòng output; tập 32 tên SAI và 4 tên không đo giống hệt nhau, sáu mục tăng thêm đều OK. Cả 32 mục SAI đều do neutral đỏ, không gọi chúng là skipped để làm mẫu số nhỏ lại. Bốn mục không đo là `124_khi_chau_con_song`, `g2_windows_directory_pin_access`, `g4_windows_LA_not_current_owner`, `g4_windows_sid_alias_not_normalized` (Windows). `doctor_bo_do_bash` ở cả hai đều OK, giết 1/1 t73. Danh sách và chi tiết đầy đủ trong `mutation-comparison.json`. Không dùng số baseline của executor (523/548) thay số vừa đo (516/548).

Tập 23 ca đỏ giống hệt base/HEAD: 10 ca đường launcher run đã có sẵn; 11 ca r484 bị ngữ cảnh `/tmp/.git`/materializer; hai ca `r858_goc_tam_tranh_to_tien_co_git` và `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac` thử đường dự phòng `/var/tmp` rồi gặp read-only. Danh sách tên và skip đầy đủ trong `suite-comparison.json`. Bỏ qua gồm t62 (Windows), r484_g4 SID (Windows) và 8 ca r345/r347/r348 không dựng được venv/pypdf offline. Không gộp bỏ qua vào tử số; không báo các lỗi môi trường này là hồi quy.

## BANG SAN

Mọi output dưới đây là đã chạy. Trừ các probe chỉ đọc HEAD, các biến thể được dựng trong `evidence/probes/`, `evidence/encoding-behavior/` và `evidence/hint/`, ngoài checkout được review.

| Hướng độc lập | Lệnh (từ cay-kho) | Output thật | Phân loại |
|---|---|---|---|
| Chuyển đổi assertion và giữ điều kiện/message | `python3 ../evidence/inventory.py` | 57/11; mismatches []; helper_raw [] | KHÔNG PHẢI LỖI |
| Helper không @ca được gọi bởi @ca | `python3 ../evidence/probes.py` / ASSERT_ROUTE helper_assert, helper_raise | Khóa `qua`; target `loi`, AssertionError | Giới hạn scanner đã đo; HEAD helper trực tiếp như vậy = 0, KHÔNG PHẢI lỗi bỏ sót đang tồn tại |
| Raise Name và hàm lồng trong ca | Cùng lệnh / raise_name, nested_assert, nested_raise | Khóa `giet`, own_signal=true; target vẫn là loi | KHÔNG PHẢI LỖI |
| Alias AssertionError, unittest style | Cùng lệnh / raise_alias, unittest_fail, unittest_equal | Cả ba khóa `qua`; target `loi` | Giới hạn: HEAD alias raise = 0, self.fail/assertEqual/pytest.raises = 0; KHÔNG PHẢI lỗi hiện hữu |
| Đăng ký trực tiếp CA | Cùng lệnh / direct_append, direct_assign | Khóa `qua`; target `loi` | Giới hạn: primary CA có 0 đăng ký ngoài decorator. Có 1 phép gán m.CA trong t119 để thử main, ca_hong của nó đã được allowlist theo tên t119 |
| Allowlist thừa, kể cả ca Windows không chạy | Cùng lệnh / REQUIRED_MUTANT | Tên t73 thừa và hai bare assertion đều bị chính khóa giết | KHÔNG PHẢI LỖI |
| Giá trị encoding thay vì chỉ có keyword | Cùng lệnh / encoding_cp1252, encoding_none; `python3 ../evidence/encoding_behavior.py` | Guard qua; Unicode sai ở cp1252 | LỖI F02, P2 |
| Dạng argv/launcher khác | probes / sys_executable, argv_variable, universal_newlines, popen_universal, check_output | Bốn dạng đầu lọt; check_output([PY],text=True) bị bắt bằng tín hiệu khóa | Giới hạn đã đo; inventory không thấy Python text-mode đang thiếu encoding ở HEAD |
| Cắt message ở reporter suite và CLI | probes / REPORTER, CLI_REPORTER | TypeError và AssertionError 500 x đều in 500 x | LỖI F01, P1 |
| Truyền type/message qua kênh --lap-ca | probes / REPORTER review_typeerror_500 | `khac:TypeError: TypeError:` + 149 x | LỖI F01, cùng lớp cấu trúc reporter |
| Khớp tên và neutral khi chi tiết có ký tự phân cách | probes / NAME_MATCH | SAI, 0/1; không đổi thành giet/qua | KHÔNG PHẢI LỖI |
| errors=replace và kiểm byte lỗi UTF-8 | `python3 ../evidence/encoding_behavior.py` | Byte-check neutral qua; mutant decode replace trong launcher bị `r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat` giết, own_signal=true | KHÔNG thấy che một lần giết thật này |
| Tolerance khi trường JSON không được t73 kiểm | Cùng lệnh / REPLACEMENT_T73 | t73 qua, contains_U_FFFD=True | Đã đo giới hạn. t73 chỉ đòi tên bash/npm; không khai kiểm UTF-8 toàn payload. Lỗi decode vô can trước đây là loi, không phải một lần giết hợp lệ |
| Windows native/CI hiện tại | Không có năng lực trong rig offline | Không chạy/không đọc check run | KHÔNG ĐO ĐƯỢC |

Thống kê đường assertion tại HEAD: bare Name raise không gọi = 0; alias-rồi-raise = 0; helper module có assert/raise trực tiếp = 0; assertion trong nested functions = 4 câu (1 assert + 3 raise), đều thuộc đúng ba ca cố ý. `CA.append(fn)` có một site trong chính decorator `ca`; không tính nó thành bypass. Những mẫu code nằm trong string của các self-test không phải assertion thi hành trong tiến trình cha. Không soạn payload nội dung nhạy cảm; mọi phép thử mới dùng `review inert`/x hoặc dữ liệu Unicode vô hại.

## BANG LOP

| Slug lớp | Biểu hiện | Mức cao nhất | Nguồn | Phép kiểm đóng lớp |
|---|---|---|---|---|
| reporter-thong-diep | F01: suite không cắt; channel trộn type/message; transport mất message | P1 | Lượt 1, reviewed_sha ở đầu tệp | Suite/CLI/kênh cùng giữ đúng 160 ký tự message và type hiển thị đúng, mutant từng đường chết đúng ca |
| khoa-encoding-chi-kiem-khoa | F02: cp1252/None được nhận | P2 | Lượt 1, cùng SHA | Khóa nhận HEAD đúng, từ chối mutant giá trị sai bằng tín hiệu của chính nó |

Hai lớp, bốn biểu hiện; chưa tuyên bố đã đóng lớp nào trên HEAD.

## FINDINGS

### reporter-thong-diep [P1] Reporter chưa cắt đúng thông điệp và kênh lặp tên loại lỗi (F01)

TEP/DONG: `.claude/dev/launcher_test.py:15063`, `:15069`, `:15226`, `:15032`, `:15025`.

VAN DE: Mục tiêu 3 yêu cầu reporter cũng cắt 160 ký tự thông điệp. `chay_bo_ca` vẫn giữ toàn bộ `str(e)` hoặc `<type>: <e>` trong hong_ds; hai nhánh main in nguyên dữ liệu đó. Trong kênh mới, `hong_ds[-1][1][:160]` cắt cả prefix `TypeError: ` thay vì chỉ message; consumer ghép thêm LOAI_HONG (`khac:TypeError`) lần nữa. Với TypeError("x"*500), chi tiết trả về là `<ca>(khac:TypeError: TypeError: <149 x>)`, không phải `<ca>(TypeError: <160 x>)`. Ngoài ra nhánh OSError/SubprocessError/ValueError ở cham_lap_ca vẫn bỏ message, chỉ trả tên loại. Các biểu hiện này cùng lớp reporter chưa chuẩn hóa dữ liệu loại/message. A2 hiện tại chỉ đo cham_mot_ca nên vẫn xanh.

DA THU NGHIEM: `PYTHONDONTWRITEBYTECODE=1 PIP_NO_INDEX=1 python3 ../evidence/probes.py`, rc=0. `suite_reason_len=511`, `suite_x=500`, `CLI_REPORTER ... x_count=500`; đường lap `lap_x=149`. AssertionError cũng in 500 x (kênh giữ 160 x nhưng type vẫn mang tiền tố phân loại). Tên/loai dùng chấm điểm không bị message làm đổi. `python3 ../evidence/detail_edges.py` đo OSError("review inert") từ subprocess: nhận `review_transport(OSError)` và mất thông điệp; helper message rỗng ra TypeError, 500 ký tự Unicode vẫn cắt đúng 160.

GOI Y VA: trong chay_bo_ca lưu metadata `(tên loại thật, thông điệp cắt 160)` tách khỏi LOAI_HONG; dùng mo_ta_loi cho reporter; serialize message thuần và tên loại hiển thị riêng qua kênh, giữ LOAI_HONG cho nhận diện giết/loi. Khóa bằng ca chạy thật cả chay_bo_ca lẫn cham_lap_ca, với TypeError và TinHieuChotCa. Đột biến bỏ cắt từng nhánh, đưa prefix loại trở lại message và bỏ message ở nhánh lỗi transport phải chết đúng khóa. Kiểm tác động lên consumer đọc hong_ds, kênh kết quả cũ và phân loại tín hiệu; đừng đổi prefix phân loại để sửa hiển thị.

DO TIN: cao, đo được trên chính HEAD bằng ca lỗi vô hại. Gợi ý cụ thể trong HINT.patch được chạy riêng trên bản sao, chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.

### khoa-encoding-chi-kiem-khoa [P2] Khóa UTF-8 chấp nhận encoding=None hoặc bảng mã sai (F02)

TEP/DONG: `.claude/dev/launcher_test.py:10050`.

VAN DE: Khóa chỉ xét `"encoding" not in kw`; `encoding=None` dùng lại bảng mã mặc định và `encoding="cp1252"` dùng chính bảng mã gây sự cố đều xanh. Đột biến bỏ hẳn keyword hiện có không bao phủ giá trị sai. P2 là thiếu răng của ca khóa; tất cả 17 lời gọi text-mode Python hiện tại trên HEAD đều đã đúng utf-8/replace, không khai có lỗi giải mã production đang tồn tại.

DA THU NGHIEM: probes cho encoding_cp1252 và encoding_none đều `qua`. encoding_behavior chạy chay thật với script con in byte UTF-8 vô hại: HEAD `'review ✓'`, mutant `'review âœ“'`; khóa vẫn `('qua','r1122_con_python_giai_ma_utf8')`. Không cần giả Windows để chứng minh bảng mã sai lọt; tác hại của None trên Windows được giữ là giới hạn chưa đo native.

GOI Y VA: kiểm giá trị literal UTF-8 và errors=replace cho các call hiện được nhận diện, thêm mutant cp1252/None; nếu cho phép encoding qua biến thì phải resolve/đo hành vi tương ứng. Các dạng sys.executable, biến argv và universal_newlines hiện không có sai phạm trên HEAD: ghi giới hạn hoặc mở phạm vi có chủ ý, không khai đã phủ hết mọi đường Python chỉ từ scanner hiện tại. HINT.patch sửa phần giá trị và thêm hai mutant, giữ phạm vi nhận diện cũ. Nguy cơ của cách kiểm literal là từ chối alias/giá trị động hợp lệ về sau; khi thay cách khai cần sửa hợp đồng và phép đo cùng lúc.

DO TIN: cao cho mutant lọt; mức P2 vì khoảng trống kiểm thử, không phải lỗi đang xảy ra tại lời gọi HEAD.

## LOG, KHỚP TÊN VÀ NỘI DUNG NHẠY CẢM

`ket_luan_mutant` và danh sách dich/phai_chet dùng tên/loai đã cấu trúc, không parse chuỗi chi tiết mới. Cắt message không làm vỡ ghép tên ở các consumer đã kiểm; dấu ngoặc, phẩy và newline trong probe vẫn chỉ là loi. Chi tiết có newline được in nguyên nên log có thể nhiều dòng; chưa tìm thấy consumer chấm điểm từ những dòng đó ở phạm vi packet này. Nhánh hook vẫn chấm theo ngoại lệ, không theo nội dung message.

Cắt 160 là giới hạn độ dài, không phải che dữ liệu. Exception có thể mang path, stdout/stderr, URL hoặc nội dung đầu vào gây lỗi; nếu bí mật nằm trong 160 ký tự đầu thì vẫn có thể vào log. Test suite hiện gỡ CODEX_AUTH_JSON và fixture credential dùng dữ liệu inert; chưa đo được luồng làm lộ credential thật, cũng không dùng credential thật để thử. Hướng nhạy cảm chỉ mô tả bằng lời: kiểm cách lỗi từ API/subprocess đưa dữ liệu người dùng vào exception và cách CI bảo vệ log. Không tự nâng giả thuyết đó thành finding rò bí mật. F01 làm trần 160 chưa được áp ở reporter, nhưng thêm cắt cũng không tự chứng minh redaction.

## GỢI Ý VÀ TOÀN VẸN CHECKOUT

`HINT.patch` là patch -p0 tính từ cay-kho, chỉ chạm launcher_test.py khi executor tự áp. Đã áp trong evidence/hint/apply và byte-compare với bản đã kiểm (rc=0). Chạy `python3 ../evidence/build_hint.py`: bốn ca r1122 qua, sáu mutant mới bị đúng TinHieuChotCa của ca đích; số lỗi Ruff F của bản hint vẫn 5 F841. Các mỏ neo mutation cũ được đối chiếu và không đổi số lần xuất hiện. Chưa chạy full suite/full mutation trên hint; không dùng kết quả hint thay kết quả HEAD.

Không chỉnh mã nguồn checkout; bytecode/cache bị vô hiệu hoặc đặt ngoài. Suite có tác dụng phụ đã thấy: t152 chạy hook thật và tạo/ghi lại ignored marker `.claude/.packet_state/session-start.ran` (28 byte, chỉ dấu thời gian/trạng thái); đã lưu size/mtime/hash ở source-generated-marker.json và dọn đúng marker cùng thư mục rỗng do test tạo sau khi suite xong. Vì vậy không khẳng định execution chưa từng ghi checkout. Snapshot đầu git status không hiển thị ignored; đây là giới hạn quan sát đầu phiên. Có một thao tác mkdir nhầm tạo thư mục rỗng cay-kho/evidence ở đầu phép đo, được rmdir ngay trước khi chạy suite; không tạo tệp nguồn trong đó. Snapshot đầu có git status sạch; snapshot cuối kiểm tracked/untracked/ignored, HEAD/tree, diff working tree và index đều sạch, identity không đổi (source-*-final.log). Snapshot không chứng minh chưa từng có ghi tạm; chi tiết thao tác rỗng này được khai riêng. Sandbox workspace-write là khả năng kỹ thuật, không giả nhận filesystem checkout bị mount read-only.

Kết luận: changes_requested vì F01 và F02. Mọi phép đo cục bộ đã kết thúc; lỗi suite/mutation trên tập chung đều đỏ sẵn, delta = 0. Windows N0/A3 và CI check run A5 vẫn KHÔNG ĐO ĐƯỢC độc lập trong rig offline; A6 giữ CHƯA ĐO ĐƯỢC theo SPEC. Không sửa mã nguồn cay-kho, không push/merge/land. Hoàn tất 2026-11-01 UTC.
