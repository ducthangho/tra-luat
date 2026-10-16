verdict: changes_requested
reviewed_sha: 4918d5f073464b5136c4c0c6a3d538347fec2baa

Reviewer: Codex / OpenAI, phiên độc lập với executor Claude, qua API và công cụ shell cục bộ. Không gọi mạng, không sửa mirror, không dựng payload tấn công. Không tạo cây vá: các finding dưới đây cần sửa hợp đồng nghiệm thu trước khi thi công. Các phản mô hình được mô tả bằng lời, chưa phải thử nghiệm trên một bản triển khai r5.

## BẢNG ĐO

Quy ước: `G` = `cay/ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md`; `C` = `cay/ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN.md`. Dòng dẫn theo hai tệp này. Git đọc từ `cay-kho/`. “Khớp số học” không xác thực các số đo đầu vào. “THUẬT LẠI” không được tính là reviewer đã tái đo CI.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| HEAD review | `4918d5f073464b5136c4c0c6a3d538347fec2baa` | Đúng OID; tree `9cf42d0038f21e2881cc99c0fa6d894dfbfbbc22` | Có |
| Diff so base `26e2555d36c48b3c0f625ae50ab2cfb62b6cb858` | 2 tệp, +425/−16 | C +213/−0; G +212/−16 | Có |
| Hai tệp `cay/` là bản đang review | r1 và r5 | Khớp byte với blob tại HEAD | Có |
| Bản GATE r4 đối chiếu | Bản trước PR | Khớp byte với blob GATE tại base | Có |
| Mirror đầy đủ; viết tắt | không nông; 7 | `false`; `core.abbrev=7` | Có |
| A1 — SHA-256 workflow ở `d28c4b1` và `origin/master` | `8dbc730f8a66a8dc…`, bằng nhau | Cả hai: `8dbc730f8a66a8dc86da9ff487108809b320ba35aa0bdb4bc773da99cd18a22b` | Có |
| A2 — số job | 1, `gate` | 1, `gate` ở cả hai ref | Có |
| A3 — số bước YAML | 40 | 40 ở cả hai ref | Có |
| A4 — timeout và số lần xuất hiện | 60; 1 | Giá trị YAML 60; chuỗi `timeout-minutes` xuất hiện 1 lần | Có |
| A5 — bước có `if` | 10 | 10 | Có |
| A6 — `if` mức job | None | None | Có |
| B1 — ca lease-publish, `d28c4b1` / `4b5184e` | 121 / 146 | 121 / 146 hàm đăng ký bằng `@ca` | Có; không chỉ đếm tên `t` + số + `_` |
| B2 — biên nhận, hai ref trên | 73 / 118 | 73 / 118 tệp `*.receipt.yaml` trong `ops/reviews/` | Có |
| B3 — B, hai ref trên | 24,4 / 54,6 giây | KHÔNG ĐO ĐƯỢC thời lượng lượt gốc: không có log, lệnh benchmark đầy đủ, cấu hình rig và kết quả từng lượt | Chưa xác minh |
| B4 — TỔNG, hai ref trên | 75,3 / 177,0 giây | KHÔNG ĐO ĐƯỢC thời lượng lượt gốc, cùng lý do B3 | Chưa xác minh |
| B5 — TỔNG/B | 3,09 / 3,24 | 3,086065574 / 3,241758242 từ các số khai | Khớp số học |
| B6 — phần của t125 | 114,10 / 173,6 giây = 65,7% | 65,72580645%; không có hiện vật xác minh hai thời lượng thuộc cùng lượt | Khớp số học; chưa xác minh nguồn |
| C1 — dòng trong nhanh_don_duoc_test | 233 | 233 | Có |
| C2 — mục DOT_BIEN | 10 | 10 phần tử AST | Có |
| C3 — assert trần toàn tệp | 16 | 16 nút `ast.Assert` | Có; xem X1 về phân bố |
| C4 — phép so `ok = …` | dòng 211 | Dòng 211, đúng biểu thức đã trích | Có |
| C5 — raise trong run | dòng 20 | Dòng 20, `AssertionError` trần | Có |
| C6 — chay_dot_bien | 182–219 | AST: 182–219 | Có |
| C7 — kho_bare | 25–66 | AST: 25–66 | Có |
| C8 — gpgsign: packet_loop / lease_publish / bien_nhan / nhanh_don | 10 / 8 / 1 / 0 | Số DÒNG chứa: 10 / 8 / 1 / 0. Số lần xuất hiện chuỗi: 11 / 8 / 1 / 0 | Có nếu đơn vị là dòng; từ “lần nhắc” chưa chính xác |
| C9 — Errno 39 / Directory not empty ngoài hai spec | 0 | 0 dòng, tìm không phân biệt hoa/thường trên các blob `.py`, `.md`, `.sh` tại HEAD | Có trong phạm vi phép đo spec khai |
| D1 — Windows run 34552510232 | 60,32 phút, cancelled | THUẬT LẠI; không hiện vật. Giá trị gần trần 60, không mâu thuẫn nội tại | Không xác thực CI |
| D2 — Windows run 34563553711 | 60,52 phút, cancelled | THUẬT LẠI; cùng nhận xét D1 | Không xác thực CI |
| D3 — Ubuntu run 34552510232 | 29,03 phút, success | THUẬT LẠI; một job success cùng run có job cancelled không tự mâu thuẫn | Không xác thực CI |
| D4 — Ubuntu run 34563553711 | 12,38 phút, failure | THUẬT LẠI; không mâu thuẫn D2 | Không xác thực CI |
| D5 — tổng có trọng số | 60,52 × 2 + 12,38 = 133,42 | 133,42, nhỏ hơn 135 là 1,58 | Có về số học; không phải chứng cứ hoàn thành tải |
| D6 — thiết lập Windows bước 1–13 | 3,27 / 2,75 phút | THUẬT LẠI; cả hai ≤ 3,33. Chưa xác minh cùng tập bước với nền cũ 1–10 | Chỉ khớp bất đẳng thức |
| E1 — t26+t27 mỗi biên nhận | 2,44 giây / 118 = 20,7 ms | 20,67796610 ms; 118 được đếm lại, 2,44 giây chưa có hiện vật | Khớp số học |
| E2 — ngoại suy | 20,7 × 10 × 3,24 = 671 ms ≈ 0,67 giây | 670,68 ms = 0,67068 giây | Có về số học; không xác thực hệ số ×10 |
| E3 — ngưỡng A1 | 0,60 × 60 = 36,00 | 36,00 | Có |
| E4 — B tăng | 54,6 / 24,4 = 2,24 | 2,237704918 | Khớp số học |
| X1 — C:84/117, assert CỦA tám ca | 16 | T1…T8: 1+1+2+1+1+1+2+5 = 14; hai assert khác ở dòng 80 và 198 | Không |
| X2 — C:103, độ dài spec GATE | 648 dòng | r4 có 648; r5 có 844 | Trôi theo revision |
| X3 — G:94, số lần r4 nhắc t125 | 0 | 0 | Có |
| X4 — t125 chạy suite con hai lần | Hai lượt, đổi GITHUB_ACTOR | Hai lời gọi `luot`; mỗi lời gọi gọi lại cùng script với CO_AB; nhánh CO_AB return | Có về cấu trúc |
| X5 — cờ CO_AB đếm đạt | return vẫn được đếm ĐẠT | `t125` return; `main` gọi fn xong tăng `qua` | Có về luồng mã |
| X6 — write set triển khai hai packet | C: 1; G r5: 3 | Hai tập rời nhau, hợp có 4 đường | Có; ADR áp từng packet, không phải tự động cộng hai packet |
| X7 — G:466, write set hiện hành | 2 tệp | Bảng ngay dưới có 3 | Không |
| X8 — G:463–464, thêm composite action vẫn trong trần | thêm một tệp thành 3 | Với write set r5: 3+1=4 | Không |
| X9 — G metadata so A9 | depends_on=[]; chỉ chờ #456 | G:483 và 732 đòi [wp503], chỉ cấp sau khi #503 land | Mâu thuẫn nội tại |
| X10 — G A1 so phần chua_do_duoc | 36,00 ở A1; 25,00 ở G:824/828 | Hai ngưỡng còn cùng tồn tại ở hiện tại | Không |
| X11 — lịch sử timeout | 25 → 45 → 60, hai lần nâng | `9e4f361`:25; `6d88a2c`:45; `7657bfd`:60 | Có |
| X12 — trôi cây 1b3caa1→28cb898 | 46 commit; 39→40 bước | 46; 39→40; số bước run trùng bằng 0 cả hai | Có |
| X13 — consumer Ruff | chỉ đọc jobs.gate; dòng 140–158 | Đúng; hàm 19 dòng, ba điều kiện kiểm | Có |
| X14 — packet_loop_test | 4.733 dòng; 169 dòng/179 lần nhắc đột biến | 4.733 / 169 / 179 tại cả 1b3caa1 và reviewed_sha | Có |
| X15 — hiện vật CI lịch sử | job.tsv 26; buoc.tsv 1.140 | 26 / 1.140 hàng dữ liệu | Có; khác với nhóm D mới không có hiện vật |
| X16 — mẫu 11 Windows cũ | 5 master+6 nhánh; min40,20/max50,48/median46,02/mean45,84 | Đúng 11 head được liệt kê; 5 master; 40,20 / 50,48 / 46,02 / 45,83727 | Có |
| X17 — hệ số test registry | n11; min1,07/max1,71/median1,21; dải1,21–1,21 | Tính lại buoc.tsv ra đúng tất cả | Có |
| X18 — hệ số tl selftest | n11; 1,41/2,26/1,83; dải1,82–1,84 | Tính lại đúng tất cả | Có |
| X19 — hệ số packet-loop | n11; 1,88/2,89/2,37; dải2,36–2,38 | Tính lại đúng tất cả | Có |
| X20 — hệ số G5 | n11; 1,91/3,09/2,40; dải2,37–2,43 | Tính lại đúng tất cả | Có |
| X21 — hệ số lease-publish cũ | n11; 2,42/3,84/2,94; dải2,91–2,97 | Tính lại đúng tất cả | Có |
| X22 — hệ số bien-nhan v2 | n10; 7,07/9,74/7,79; dải7,71–7,88 | Tính lại đúng tất cả | Có |
| X23 — hai tổng lịch sử A5 | 110,65 nhánh; 111,08 master | job.tsv: 43,20×2+24,25=110,65; 42,28×2+26,52=111,08 | Có |
| X24 — tổng bước, run nhánh 34045664423 | Windows43,17; Ubuntu24,20 | buoc.tsv: 43,16666667; 24,20 | Có sau làm tròn |
| X25 — thiết lập cũ | Windows3,33; Ubuntu1,18; bước1–10 | buoc.tsv: 3,33333333 / 1,18333333. Nếu lấy bước1–13: 3,36666667 / 1,18333333 | Có cho tập cũ; chưa chứng minh so cùng thước với D6 |
| X26 — lỗi ghép mẫu số tự thú | 114,10/177,0 không phải65,7% | 64,46327684%; mẫu số sửa173,6 cho65,72580645% | Tự thú đúng về số học; nguồn ghép lượt chưa kiểm được |
| X27 — lỗi 0,62 tự thú | phải là0,67 giây | 0,67068 | Đã sửa số học tại chỗ |
| X28 — lỗi 14,32/26,57/126,23 tự thú | 14,31/26,56/126,22 | 13,13+1,18=14,31; 7,42+14,31+4,83=26,56; 49,83×2+26,56=126,22 | Các số hạng sửa khớp |
| X29 — số lượt không tái hiện C | 44 = 12+12+10+10 | Tổng 44; không có log xác thực 0 tái hiện | Khớp số học, chưa xác thực thực nghiệm |
| X30 — chốt ký commit khác ngoài kho_bare | M4 chỉ gọi tên kho_bare | `chay_dot_bien` tạo repo src, commit ở dòng192, không đặt gpgsign=false | Bỏ sót |

Các lệnh đo đã chạy: `git -C cay-kho rev-parse HEAD HEAD^{tree} origin/master`, `git -C cay-kho diff --numstat 26e2555d36c48b3c0f625ae50ab2cfb62b6cb858 4918d5f`, `git show <ref>:<path>` qua `subprocess.check_output`, `hashlib.sha256`, `yaml.safe_load`, `ast.parse`, `git ls-tree -r --name-only <ref> ops/reviews`, và đọc TSV bằng `csv.DictReader`/`statistics`. Số ca B1 được đếm từ decorator `@ca`: phép đếm chỉ tên `t\d+_` cho 116/141, bỏ sót năm ca có hậu tố chữ. Không sử dụng con số sai đó làm finding.

Các giới hạn: không chạy lại các suite toàn kho, benchmark B3/B4/B6 hoặc các cổng executor nêu ở đầu EVIDENCE. Thời lượng lịch sử không nằm trong blob mã; chạy một lượt mới cũng không xác minh được các số gốc hay việc chúng thuộc cùng rig. Không gọi `ls-remote`; `origin/master` cục bộ là `e82af37fe66629d5378ac56fc689e24db26594fa`, không phải chứng cứ head trực tiếp trên GitHub. Không xác minh số ref máy chủ 331/332, quyền branch protection, lease đang sống trên máy chủ hoặc comment #505/#508. Kiểm workflow `ops-thu-hoi-admission.yml` thấy `pull_request_target` và ý định chạy mã base; không thấy cơ sở cục bộ bác biên bản đứng lại, không báo lại cổng `thu-hoi` đỏ.

## KIỂM TỪNG TIÊU CHÍ CÓ THỂ ĐỎ

“Có” dưới đây chỉ là tồn tại phản ví dụ, không chứng minh tiêu chí đủ bao phủ. Không tìm thấy tiêu chí thuần hằng-đúng trong toàn bộ 19 tiêu chí; nhiều tiêu chí vẫn có lỗ hoặc mâu thuẫn khiến bản làm đúng không thể đồng thời đạt.

| tiêu chí | trạng thái làm ĐỎ | đánh giá |
|---|---|---|
| C A1 | Bộ chấm nhận AssertionError hạ tầng là tín hiệu chốt | Có thể đỏ; chưa kiểm tín hiệu hạ tầng mang lớp mới hoặc đường truyền kết quả |
| C A2 | Bộ chấm nhận chốt của ca ngoài đích là GIẾT | Có thể đỏ; neo tên ca chưa neo nguồn phát |
| C A3 | Một trong ba nhãn biến mất hoặc số hạng sai | Có thể đỏ; đòi kiểm số hạng là đúng |
| C A4 | Một hoặc ba lần gọi; hai lỗi liên tiếp nhưng suite xanh | Có thể đỏ; phép bỏ trần có thể treo, chưa ghi timeout cho chính phép thử |
| C A5 | config đọc lại khác false hoặc suite hỏng dưới ký commit | Có thể đỏ; M4 bỏ sót repo src |
| C A6 | Thiếu một cặp ca/đột biến riêng đã chạy đỏ | Có thể đỏ; phải tách năm ca tự kiểm khỏi tám ca sản phẩm nếu vẫn giữ 8/8 |
| C A7 | Một mutant không giết hoặc số đếm khác10/0/0 | Có thể đỏ |
| C A8 | Sửa tệp thứ hai hoặc thêm301 dòng | Có thể đỏ |
| G A1 | Job Windows dài36,01 phút khi timeout60 | Có thể đỏ; với A4 ghim60, ngưỡng tương đối chính là ngưỡng tuyệt đối36 |
| G A2 | Bộ ba tên/nền/kết luận bị mất hoặc đổi | Có thể đỏ; hiện mâu thuẫn nền bị cắt và việc thêm t125 |
| G A3 | if mới, mất tiền tố thiết lập, delta chẩn đoán khác rỗng | Có thể đỏ; chưa cập nhật tập bước cho M8 |
| G A4 | timeout thực đổi thành61 và không sửa bằng chứng đếm chuỗi | Có thể đỏ; phép grep không chứng minh timeout60 ở từng job |
| G A5 | Có job failure/cancelled, hoặc tổng vượt135 | Có thể đỏ; định nghĩa hợp lệ thiếu tập job kỳ vọng, kết quả nền lỗi chưa nhất quán |
| G A6 | Tên job công bố không khớp; required checks thiếu job | (a) có thể đỏ; (b) khai rõ không đo được từ phiên, phải có xác nhận chủ kho. Danh sách ba job chưa phủ job t125 |
| G A7 | Consumer quay lại jobs.gate khiến YAML đã tách có lỗi | Có thể đỏ; hàm cũ đúng là consumer ngoài workflow |
| G A8 | Tệp thứ tư hoặc tổng additions>300 | Có thể đỏ; đoạn composite action cũ lại cho phép tệp thứ tư |
| G A9 | Còn lease khác giữ write set hoặc #503 chưa land | Có thể đỏ; metadata vẫn khai không phụ thuộc |
| G A10 | Bước lease-publish vẫn tốn xấp xỉ100% nền, thay vì≤45% | Có thể đỏ nếu có mẫu nền cùng cách; không được coi số đo khác rig là đối chứng |
| G A11 | Bỏ job t125 mà không cổng nào đỏ; hoặc skip được đếm đạt | Có thể đỏ; chỉ hiện diện job chưa chứng minh nó thực thi đầy đủ A/B |

### doi-ca-assert-ha-tang-thanh-tin-hieu-chot  [P1]  M1 chuyển nhầm hai assert hạ tầng sang tín hiệu dành riêng cho ca
TỆP/DÒNG: C:84,117–118,128–140,206–208; mã tại `cay-kho/ops/nhanh_don_duoc_test.py:80` và `:198`.
VẤN ĐỀ: Tổng16 đúng nhưng “16 assert của8 ca” sai. Chỉ14 assert ở T1…T8; hai assert còn lại kiểm loader và ống stdout của archive. M1 đòi đổi cả16 sang chot(), đồng thời khẳng định lớp mới chỉ do thân ca phát và ngoại lệ hạ tầng phải KHÔNG ĐO ĐƯỢC. Thực hiện đúng số16 sẽ tự cấp lớp tín hiệu chốt cho hạ tầng; giữ hai assert kia lại thì trái lệnh đổi16. A1 chỉ tiêm AssertionError trần từ run(), A2 chỉ đổi tên ca, nên cả hai không kiểm đường hạ tầng này. Lớp riêng không tự chứng minh nguồn phát.
ĐÃ THỬ VÁ: không — chưa có bản triển khai; cần chốt lại chính xác tập assertion được chuyển và phản chứng hạ tầng cùng ca đích.
ĐÃ THỬ NGHIỆM: `ast.parse` trên `git show 4918d5f:ops/nhanh_don_duoc_test.py`, đếm Assert theo từng FunctionDef ⇒ T1…T8 có14; nap_tool có1 tại80; chay_dot_bien có1 tại198. Không dựng payload.
ĐỘ TIN: cao

### lop-ngoai-le-chua-bao-ve-duong-truyen-ket-qua  [P1]  A1/A2 chưa chặn giả tín hiệu trên stdout giữa lượt con và bộ chấm
TỆP/DÒNG: C:117,128–140; mã hiện tại `cay-kho/ops/nhanh_don_duoc_test.py:172–181,208–211`.
VẤN ĐỀ: Đặc tả hứa “không giả mạo được” bằng lớp và tên ca, nhưng bộ chấm hiện gọi tiến trình con rồi đọc dòng văn bản; object ngoại lệ không đi qua ranh giới tiến trình. `chay_ca` in nguyên nội dung exception, còn matcher đọc các dòng có tiền tố CASE. C không quy định kênh kết quả, xử lý dòng giả/trùng/thiếu, xác minh lượt chạy hoặc nguồn phát. Hướng phản chứng bằng lời: để stdout hoặc thông điệp lỗi nhiều dòng của mã được thử mang hình dạng một kết quả ca có tên đích và nhãn lớp mà bộ đọc tin. A1/A2 chỉ dựng ngoại lệ đúng đường dự kiến; một implementation gắn thêm tên lớp vào văn bản vẫn có thể qua hai ca ấy mà giữ bệnh tin chuỗi. Đây là lỗ hợp đồng, chưa phải tuyên bố đã khai thác một bản vá chưa tồn tại.
ĐÃ THỬ VÁ: không — cần xác định ranh giới tin cậy và phản chứng đi qua chính subprocess/parser, không chỉ gọi bộ phân loại trong bộ nhớ.
ĐÃ THỬ NGHIỆM: đọc `git show 4918d5f:ops/nhanh_don_duoc_test.py` ⇒ kết quả truyền bằng stdout, exception được nội suy nguyên văn, matcher neo đầu dòng. KHÔNG ĐO ĐƯỢC parser r1 sau sửa vì PR chỉ có đặc tả; không tạo chuỗi giả.
ĐỘ TIN: vừa

### fixture-ky-commit-con-mot-kho-chua-phu  [P1]  M4 không đủ làm trọn suite chạy được trong môi trường ký commit
TỆP/DÒNG: C:120,159–165; mã `cay-kho/ops/nhanh_don_duoc_test.py:184–192`.
VẤN ĐỀ: Ngoài kho work do kho_bare dựng, chay_dot_bien còn tạo repo src và git commit nguồn. Repo đó chỉ được đặt user.name/email, chưa tắt ký. Chỉ sửa fixture như M4 thì tám ca có thể qua, nhưng suite đầy đủ chết khi commit nguồn mutant. Nếu phép A5 chỉ đo8/8 ở chế độ bỏ đột biến, nó bỏ sót đúng lần commit này; nếu đo trọn suite như câu chữ yêu cầu, bản sửa theo M4 chưa đủ. Cấu hình phạm vi lệnh còn có thể ưu tiên hơn repo-local, điều đã được bộ packet_loop_test mô tả trong kho.
ĐÃ THỬ VÁ: không — chưa thống nhất phạm vi cách ly cấu hình Git và các kho cần phủ.
ĐÃ THỬ NGHIỆM: đọc mã dòng184–192 và `rg -n gpgsign cay-kho/ops/nhanh_don_duoc_test.py` ⇒ không có ghim ở repo src. Không dựng helper ký hoặc payload môi trường theo giới hạn của người giao review.
ĐỘ TIN: cao

### them-t125-nhung-giu-hop-dong-ba-job  [P1]  M8 không thể thi công theo hợp đồng cũ về lệnh, tập bước và required checks
TỆP/DÒNG: G:385–389,529–530,552–553,596–614,686–697,750–769.
VẤN ĐỀ: M8 thêm job riêng chạy t125; A11 đòi cờ MỚI trong lượt lease-publish chính. Nhưng ngoai_pham_vi#6 vẫn cấm đổi bất kỳ lệnh hoặc tập bước nào, chỉ cho dời job. A2 giữ nguyên tập tên/nền/kết luận và A3 giữ nguyên tập tên/if, không định nghĩa phép chiếu cho bước t125 thêm mới. A6 còn đòi require “cả ba job”, trong khi cấu trúc mục tiêu nay cần ít nhất bốn job: gate, registry, packet-loop, t125. Bản thi công thêm cờ đúng A11 sẽ trái điều cấm đổi lệnh; thêm một bước có tên riêng sẽ làm phép so tập cũ đỏ. Chỉ cập nhật ba required checks cũng để kết quả t125 ngoài hợp đồng bảo vệ nhánh.
ĐÃ THỬ VÁ: không — phải thống nhất bố cục bốn job, ánh xạ độ phủ và các thay đổi lệnh được phép; không tự sửa thiết kế hộ executor.
ĐÃ THỬ NGHIỆM: đọc đối chiếu các dòng trên; AST t125 xác nhận hiện chưa có chế độ chỉ chạy t125, chỉ có CO_AB chống đệ quy. Không có mã mới để chạy integration test.
ĐỘ TIN: cao

### a2-doi-giu-ca-ket-luan-cua-nen-bi-cat  [P1]  A2 không tương thích với A5 khi lượt nền Windows không hoàn tất
TỆP/DÒNG: G:122–137,593–604,672–680,803–808.
VẤN ĐỀ: r5 thừa nhận lượt nền trước tách vẫn có thể bị cắt, và A5(3) cho ghi nền KHÔNG ĐO ĐƯỢC. A2 không có nhánh tương ứng: vẫn bắt tập bộ ba có conclusion của lượt sau bằng đúng lượt trước tại start_from_sha. Theo chính tình huống r5 xử lý, những bước chưa chạy ở nền sẽ skipped/cancelled, còn sau tách làm đúng phải success; hai tập không thể bằng nhau. Nếu ép chúng bằng nhau thì phá điều kiện lượt sau hợp lệ của A5. A2 chứng minh độ phủ bằng so kết luận chỉ dùng được khi đã xác định một nền hợp lệ; r5 mới xử lý thiếu nền ở A5, bỏ quên A2.
ĐÃ THỬ VÁ: không — cần quyết định cách chứng minh độ phủ khi nền bị cắt và trạng thái nghiệm thu trong trường hợp đó.
ĐÃ THỬ NGHIỆM: đối chiếu chữ A2/A5. Phản mô hình tập bằng lời: cùng một tên bước và nền, trước skipped, sau success ⇒ bộ ba khác nhau. KHÔNG ĐO ĐƯỢC conclusion CI mới ngoài các số THUẬT LẠI nhóm D.
ĐỘ TIN: cao

### a5-hop-le-chua-doi-du-job-va-du-luot  [P1]  Mọi job trả về success chưa chứng minh một lượt đo đủ tải
TỆP/DÒNG: G:672–681; liên quan G:596–607,686–697,759–763.
VẤN ĐỀ: Điều kiện (1) chỉ lượng hóa trên các job có trong dữ liệu đọc được. Không đòi dữ liệu đủ trang/đủ job, tập job×nền bằng tập kỳ vọng, cùng attempt, hay đủ timestamp trước khi cộng. Một danh sách chỉ có các job success nhưng thiếu Windows hoặc thiếu một job nặng vẫn thỏa điều kiện này và cho tổng thấp giả. Danh sách rỗng cũng thỏa mệnh đề “mọi job đều success”; giá trị tổng là0 nếu phép đo không chặn rỗng. A2 kiểm tập bước có giúp phát hiện một số trường hợp, nhưng r5 chưa định nghĩa tập của job t125 mới và cũng không yêu cầu manifest phép đo chung để ngăn hai tiêu chí dùng hai tập đọc khác nhau. R5 sửa được trường hợp job failure/cancelled CÓ TRONG mẫu, chưa sửa trường hợp job vắng khỏi mẫu.
ĐÃ THỬ VÁ: không — cần điều kiện đầy đủ và neo lượt đo trước bước kiểm success và cộng thời lượng.
ĐÃ THỬ NGHIỆM: kiểm định nghĩa A5 trong tệp. Phản mô hình logic nêu bằng lời, không gọi API, không tạo payload phản hồi. KHÔNG ĐO ĐƯỢC một implementation thu thập số vì chưa có.
ĐỘ TIN: cao

### a4-dem-chuoi-khong-phai-timeout-tung-job  [P2]  Chốt chống nới biên A1 có quy tắc đúng nhưng phép đo chưa đủ
TỆP/DÒNG: G:569–571,613–616,651–654.
VẤN ĐỀ: A1 có chặn cửa hậu nới trần bằng A4 và M4, nên không được báo rằng spec hoàn toàn không chặn. Tuy nhiên phép A4 là đếm chuỗi timeout-minutes:60 bằng số job, rồi loại giá trị khác60. Phép ấy không xác định vị trí khóa: chú thích và timeout mức bước cũng có thể đóng góp, một job thiếu timeout riêng không tạo ra “giá trị khác60”. Tổng đúng không chứng minh từng job được ghim. A3 có thể hỗ trợ nếu đối chiếu với bộ ba nền bất biến, nhưng câu “bằng bộ ba của gate” cần được neo rõ vào bản trước; so các job sau tách với nhau vẫn có thể đồng loạt sai. Không khẳng định đã qua được mọi tiêu chí của GATE; finding là phép đo A4 không chứng minh đúng điều nó nhận canh.
ĐÃ THỬ VÁ: không — cần kiểm giá trị đã parse tại từng jobs.<id>.timeout-minutes, cùng danh sách job kỳ vọng.
ĐÃ THỬ NGHIỆM: `yaml.safe_load` xác nhận workflow nền có đúng jobs.gate.timeout-minutes=60; đọc A4 xác nhận nghiệm thu chỉ đưa phép grep. Không dựng YAML giả theo giới hạn người giao review.
ĐỘ TIN: cao

### r5-con-giu-nguong-cu-trong-dieu-kien-hien-hanh  [P2]  Tự thú hết hạn nhưng 25 và 135 vẫn có hiệu lực không nhất quán
TỆP/DÒNG: G:244,559–571,661–664,672–682,824–829.
VẤN ĐỀ: A1 mới đặt36 nhưng chua_do_duoc#3 vẫn hai lần nói A1 GIỮ NGUYÊN≤25 ở thì hiện tại. A5 gọi cả ngưỡng135 là giá trị lịch sử trong đoạn “Tiêu chí phải đổi hình, không được giữ số”, rồi câu phép làm ĐỎ vẫn dùng135. Thêm nữa A5(1) nói nền failure/cancelled ⇒ ĐỎ, trong khi (3) cùng chua_do_duoc#0 cho công bố nền KHÔNG ĐO ĐƯỢC và báo chủ kho, không nói đây vẫn là ĐỎ hay có cơ chế chấp nhận nào. Vì vậy hai reviewer có thể đưa verdict khác nhau cho cùng một lượt. Không coi việc giữ135 tự nó sai; sai là hợp đồng chưa xác định nó còn là ngưỡng được duyệt hay chỉ là lịch sử.
ĐÃ THỬ VÁ: không — thay ngưỡng và quy tắc chấp nhận là quyết định thiết kế, cần một hợp đồng duy nhất.
ĐÃ THỬ NGHIỆM: đọc r4 so r5, tìm các chuỗi `25,00`, `135,00`, `KHÔNG ĐO ĐƯỢC`; các câu điều kiện cũ còn nguyên trong r5.
ĐỘ TIN: cao

### metadata-va-loi-thoat-composite-chua-theo-write-set-r5  [P2]  Metadata bỏ wp503 và phương án dự phòng vượt trần ba tệp
TỆP/DÒNG: G:30–31,460–466,472–484,731–734,839–842.
VẤN ĐỀ: Metadata vẫn depends_on=[] và chỉ chờ #456, trái r5 đòi wp503 land. Phần kích thước vẫn nói write set2 và thêm composite action thành3, trong khi bảng r5 đã dùng đủ3: phương án ấy thành4 và vi phạm chính A8. Đoạn A9 về #456 đã gắn nhãn lịch sử nhưng metadata, phương án composite và chua_do_duoc#7 chưa được thu hồi tương ứng. Đây là chỗ sửa bằng thêm giải thích mà không gỡ chỉ thị cũ. Hai packet C/G có write set rời nhau; 1+3=4 KHÔNG là vi phạm ADR vì ADR áp từng packet, trừ khi gộp thi công thành một packet. Không có finding chồng lấn giữa C và G.
ĐÃ THỬ VÁ: không — cần cập nhật đồng bộ metadata và phương án dự phòng; chưa đề xuất thêm tệp.
ĐÃ THỬ NGHIỆM: đếm ba hàng bảng write_set G và một hàng C; đọc ADR-0044 trong mirror ⇒ trần theo một packet sensitive là3 tệp/300 dòng thêm. Đối chiếu depends_on ở đầu tệp với dòng483.
ĐỘ TIN: cao

### so-ci-moi-chua-duoc-khai-la-thuat-lai-trong-spec  [P2]  Các kết luận dựa nhóm D được trình bày như bằng chứng có thể tái kiểm
TỆP/DÒNG: G:114–153,581–591,803–818; C:15–30,65–68.
VẤN ĐỀ: EVIDENCE gọi nhóm D là THUẬT LẠI và xác nhận không hiện vật trong kho. Hai đặc tả không có nhãn ấy ở các kết luận tương ứng: G gọi số là “đo lại”, suy nền A1/A5 không còn đo được; C đặt trích log dưới “Vấn đề — đo được, không suy diễn”. Run ID và giờ là mỏ neo truy tìm, không thay hiện vật. Theo yêu cầu review này, kết luận dựa nhóm D phải khai rõ mức chứng cứ. Ngoài ra G nói bốn lượt liên tiếp nhưng chỉ đưa hai lượt: D không đủ chứng minh số4 hoặc khẳng định “chưa hoàn tất lần nào kể từ ~07-09”. D1/D2 phù hợp với giả thuyết chạm trần nhưng một mình duration+cancelled không phân biệt nguyên nhân huỷ.
ĐÃ THỬ VÁ: không — chưa có log để bổ sung; phải phân biệt THUẬT LẠI, suy luận có điều kiện và số tái tính được.
ĐÃ THỬ NGHIỆM: `rg -n 'THUẬT LẠI|thuật lại' cay/ops/specs/*.md` ⇒ không khớp. Đối chiếu bảng G:126–129 với lời “bốn lượt” và EVIDENCE nhóm D. Không gọi mạng theo phạm vi cứng.
ĐỘ TIN: cao

### benchmark-moi-thieu-hien-vat-neo-luot  [P2]  Sửa phép chia chưa chứng minh đã sửa lỗi ghép lượt
TỆP/DÒNG: G:83–108,114–118,810–814.
VẤN ĐỀ: B3/B4/B6 và tử số2,44 của E1 chỉ có văn xuôi, không có hiện vật benchmark kèm lệnh đầy đủ, rig, rc, số ca đạt/bỏ qua và mốc từng lượt. Chia lại cho173,6 cho đúng65,7%, nhưng không xác thực được173,6 là tổng của lượt sinh114,10. Phần suy “hệ số nền đã đổi ≥7,8×” cũng không đưa cặp thời lượng cùng lượt/cùng bước: nếu chỉ dùng hai số hiện ra177,0 giây và≥22,7 phút thì cận suy được là≥7,694915×, chưa phải≥7,8×; một phép đo độc lập mạnh hơn cần được khai. Không báo các timing là sai chỉ vì reviewer chưa tái đo được.
ĐÃ THỬ VÁ: không — cần hiện vật gốc; không thay thế bằng timing mới khác rig.
ĐÃ THỬ NGHIỆM: đọc các đoạn số; tìm trong `git grep` ở ops/reviews và ops/specs tại4918d5f không tìm được hiện vật benchmark tương ứng ngoài lời khai spec. Python tính `114.1/173.6*100`, `114.1/177*100`, `22.7*60/177` ⇒65,72580645;64,46327684;7,69491525.
ĐỘ TIN: cao về thiếu khả năng kiểm; vừa về cận7,8 vì có thể executor có phép đo chưa bàn giao

### lan-thu-ba-khong-cung-hinh-dang-tin-dung-gia  [P2]  Bảng kế thừa gộp từ chối giết thật với chấp nhận giết giả
TỆP/DÒNG: C:40–42,187–190,210–213.
VẤN ĐỀ: Hai sự kiện #355/#359 trong CLAUDE.md là cấp tín dụng giả: mutant không chết đúng chốt vẫn được tính giết. Sự cố hiện tại theo chính log lại là T1 đã chết đúng, T7 lỗi dọn dẹp làm bộ chấm TỪ CHỐI ghi công. C đếm sự cố này thành lần3 của “bộ chấm tin tín hiệu mã vô can dựng lên được” rồi dùng số3 kích hoạt §12. Cùng thuộc họ thước đo bị lỗi hạ tầng không làm chúng tự động cùng thuộc tính hẹp đang đếm. Sự cố AssertionError do git commit ở C:55–56 cũng được khai đã thấy ca đỏ, chưa chứng minh bộ chấm đã cấp GIẾT giả. Cần phân biệt hiện tượng đã quan sát với đường giả mạo cần phòng.
ĐÃ THỬ VÁ: không — cần định nghĩa lại loại sự kiện được đếm hoặc đưa bằng chứng lần thứ ba đúng loại.
ĐÃ THỬ NGHIỆM: đọc `cay-kho/CLAUDE.md:410–433` và C:22–42,189 ⇒ hai sự kiện cũ chấp nhận sai; sự cố mới chấm0/1. Không cần chạy lại ca thu-hoi hay CI.
ĐỘ TIN: cao

### bang-gom-bo-sot-cac-khang-dinh-kiem-duoc  [P3]  Danh mục A–E bỏ sót cả số hạng sai lẫn số hạng đúng
TỆP/DÒNG: `EVIDENCE.md`, mục “TRẦN CỦA BẠN”; các vị trí X1–X30 trong BẢNG ĐO.
VẤN ĐỀ: Theo yêu cầu riêng của lượt review, các khẳng định kiểm được bị bỏ sót cũng phải ghi finding. X1–X30 là danh mục bổ sung đã kiểm, không chỉ liệt kê số lệch. Những sai lệch có tác động đã tách finding ở trên. Sai lệch nhỏ còn lại: C:103 vẫn gọi đặc tả GATE648 dòng, nhưng r5 là844; C8 dùng “lần nhắc” trong khi10 là số dòng, chuỗi gpgsign thực xuất hiện11 lần trong packet_loop_test. Các mục khớp như X3–X5, X11–X25, X27–X28 không phải lỗi sản phẩm; chúng là thiếu sót của bảng gom theo tiêu chuẩn do người giao review đặt ra.
ĐÃ THỬ VÁ: không — đã bổ sung phép đo vào chính verdict, không sửa EVIDENCE của executor.
ĐÃ THỬ NGHIỆM: đếm dòng hai revision; AST và luồng main/t125; đọc blob lịch sử; tính lại CSV/TSV và số học như bảng. Các kết quả khớp lẫn không khớp đều được ghi.
ĐỘ TIN: cao
