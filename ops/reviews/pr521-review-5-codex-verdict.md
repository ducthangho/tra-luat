verdict: changes_requested
reviewed_sha: 36acc5235057779d861eff08988a9469b17e513a

**0 P1 / 3 P2 / 0 P3**: `adapter-chep-doctrine` (60 mệnh đề tại 38 cụm vị trí), `loi-khai-vuot-phep-do` (4 thể hiện), `prompt-qua-argv` (1). **HINT.patch: 43 hunk / 1 tệp**, dry-run thường, dry-run strict và áp thật clone đều rc=0; không fuzz/offset. Tám cổng nền cùng selftest idiom đều rc=0. Không suy cổng xanh thành nội dung đúng.

Reviewer: Codex, dựa trên GPT-6 theo chỉ thị phiên; provider OpenAI (`openai_codex`), execution surface agent Codex có shell sandbox, transport `machine`. Không có chứng cứ độc lập về backend model/effort viết verdict. CLI Codex 0.154.0 và Claude Code 2.1.269 là công cụ đã thử, không chứng nhận danh tính reviewer.

Authority: PROMPT.md của gói này. Review ngoại tuyến; không mạng, không gọi model tạo review con, không tự soạn payload tấn công, không sửa cay-kho/, không push/merge/đăng GitHub, không chuyển state/assurance. Chỉ tạo artifact trong gói và thử trên clone riêng ở /tmp. Không xác thực lease/generation/GitHub hiện hành ngoài snapshot được giao.

HEAD đúng yêu cầu; tree `56fd04e6196f8d5574e454a1130350e5ffab7bc4`. Base `bb7013c7669da19304a8769e5b25f8c1f8951e9c` là parent 2 của HEAD. Git xác nhận **1 tệp, +112/−0**, gồm L95–187 và L466–484; các số +77/−41 và 71 dòng trong prompt đã cũ. **Các finding lần này nằm trong phần có sẵn ở base**; không gọi chúng là 65 lỗi mới do PR thêm. Yêu cầu quét toàn adapter/đóng lớp của lượt 5 là lý do rà và đưa cả các vị trí cũ vào HINT. Chưa tìm thấy lỗi tái sinh tại bốn hunk HINT lượt 4.

## Vì sao bốn P2 lọt lượt 3

Đã đọc [PROMPT lượt 3 nguyên bản](evidence/PROMPT-LUOT-3.source.md) cạnh [VERDICT lượt 3](evidence/VERDICT-LUOT-3.source.md), không chỉ dựa bản thuật lại ở lượt 4. Không có nguyên văn comment connector trong gói; bốn finding/việc chấp nhận chúng được PROMPT hiện tại cung cấp, còn câu cũ và sửa đổi đối chiếu được bằng Git.

| P2 connector | Phạm vi prompt lượt 3 | Phép làm/thiếu của verdict lượt 3 | Kết luận |
|---|---|---|---|
| Prompt qua argv | Ưu tiên chạy bốn khối lệnh; nhiệm vụ 3 kiểm lệnh và mâu thuẫn trong tệp. | Chỉ dùng --help, khai full model NOT_RUN; không thử giới hạn argv/đối chiếu stdin đã có ở mục khác. | **Bỏ sót**. Cấm mạng không ngăn đo E2BIG hoặc đọc cmdline của child cục bộ. |
| lstart khác khóa launcher | Lớp trạng thái, kiểm tên field/lệnh/định dạng. | Đã viết “lstart … không bằng byte khóa” nhưng vẫn đóng lớp, chưa kiểm đầu ra có làm được phép so kế tiếp không. | **Bỏ sót dù đã có bằng chứng**, không phải thiếu quyền tái dùng PID. |
| Một mẫu mtime | Kiểm phép đo hẹp/kết luận rộng và chạy lệnh. | Văn xuôi nhắc nhiều mẫu được coi như block đã cung cấp đủ mẫu; thực tế chỉ ls một lần. | **Bỏ sót**. Có thể đo offline; giới hạn reboot không liên quan việc lấy hai mẫu. |
| Giữ mktemp vô hạn | Nội dung PR đã có giữ thư mục; nhiệm vụ 3 mở các tương tác/hậu quả. | Chỉ kiểm câu sandbox đã thu hẹp, không rà tác động vòng đời runner. | **Bỏ sót trong review tài liệu**. Lệnh “reviewer đừng dọn” giới hạn thao tác; không miễn phân tích vòng đời. |

Không P2 nào hoàn toàn ngoài phạm vi lượt 3. Các giới hạn thật là full model/quota, reboot và runner dài ngày; chúng không loại bốn hướng trên khỏi việc đọc/probe. Mô thức thấy trong artifact: kiểm câu cảnh báo đã xuất hiện và lệnh có output, rồi chưa đối chiếu output với kết luận người đọc được hướng dẫn rút ra. Đây là nhận xét về artifact, không suy đoán suy nghĩ nội bộ của reviewer cũ. Lượt 5 còn bắt cùng lỗi argv ở lane Claude, minh họa vì sao đóng một câu Codex chưa đóng lớp.

## Adapter có chép doctrine không

**Có.** Protocol §13 L864–866 chỉ cho adapter cú pháp/công cụ; quy tắc, schema và completion criteria thuộc protocol. §8 L551–561 chứa nguyên yêu cầu cấu hình/đối chiếu môi trường và đối chiếu lượt trước. Đọc nghĩa toàn bộ 532 dòng thấy các nghĩa vụ chọn/kiểm reviewer, closed scope, giao sandbox, ghi evidence, bảng săn, lịch ghi verdict, phân công, xuất artifact và điều kiện hoàn tất vẫn nằm trong adapter. Có con trỏ ở đầu hoặc cuối đoạn không gỡ các mệnh lệnh ở giữa.

`doctrine-scan` chỉ chuẩn hóa rồi tìm `FORBIDDEN_DOCTRINE_PHRASES`, không phân tích nghĩa. Head rc=0/7 tệp trong khi các hàng bên dưới còn sống. M1 thêm một cụm cấm vào chính adapter cho **0→6→0**. [Mã cổng](cay-kho/.claude/dev/packet_loop.py), [log nền](evidence/gate-doctrine.json), [mutation](evidence/mutations.json).

Quy ước đếm: 60 mệnh đề/quy tắc, nhóm thành 38 cụm vị trí để vá; không gọi mỗi dòng Markdown là một lỗi. Mỗi ID dưới đây có vị trí và hunk cụ thể. ID D11/D18/D42 trong bản nháp đã bị loại sau đọc nghĩa: yêu cầu cú pháp remote URL, git config và mẫu pkill tự loại trừ là hướng dẫn công cụ, không phải ba finding. Giữ khoảng trống ID để không tráo dấu vết bản nháp.

| ID | Dòng HEAD | Luật còn sống | Hunk |
|---|---|---|---|
| D01 | 22 | Bắt preflight trước đọc diff | H1 |
| D02 | 39–42 | Bắt làm đầu phiên; nhắc lại tự duyệt và fallback assurance | H2 |
| D03 | 44–51 | Bảng được viết thành chính sách chọn reviewer; HINT neo bảng vào công cụ sinh bậc | H3 |
| D04 | 53 | Bắt truyền bậc giữa các lượt, không cho tụt bậc | H4 |
| D05 | 60 | Đòi tập model chính và cấm đòi model phụ như tiêu chí review | H5 |
| D06 | 62 | Bắt đếm share trước khi bàn ngưỡng | H5 |
| D07 | 64–66 | Luôn kiểm sau lượt thật, chọn bậc trước phóng | H6 |
| D08 | 192–194 | Bắt khai trạng thái comment/assurance vào verdict | H9 |
| D09 | 206 | Lặp quy tắc neo SHA và làm lại khi head đổi | H10 |
| D10 | 210–211 | Định nghĩa clone/cách ly và lặp lease cấm chạm nhánh | H11 |
| D12 | 218 | Đặt điều kiện worktree sạch trước phóng trong comment | H12 |
| D13 | 228–230 | Đặt nguồn quyền reviewer thay vì chỉ cú pháp --allowedTools | H14 |
| D14 | 241–242 | Ấn định thành phần bundle | H16 |
| D15 | 242 | Thiếu EVIDENCE tự quy thành KHÔNG ĐO ĐƯỢC | H16 |
| D16 | 243–245 | Bắt closed read scope và diễn giải quyền đột biến | H16 |
| D17 | 249–250 | Lặp ràng buộc cấm đọc ngoài sau con trỏ §8 | H17 |
| D19 | 262–266 | Chép yêu cầu core.abbrev và nguyên luận cứ trong protocol §8 | H18 |
| D20 | 268–272 | Đặt thời điểm đối chiếu/giao sandbox, lặp quy tắc cùng commit | H19 |
| D21 | 282–283 | Lệch rc phải coi là lỗi sandbox; cấm giao mirror chưa đối chiếu | H20 |
| D22 | 285–286 | Bắt EVIDENCE khai cổng nào đã chạy | H20 |
| D23 | 288–290 | Bắt so nguồn trước clone và bắt khai đúng lý do | H20 |
| D24 | 295–296 | Lặp mệnh lệnh ghi lý do và chỉ thời điểm trước clone | H21 |
| D25 | 303 | Bắt fetch trước clone trong comment | H22 |
| D26 | 316 | Đặt điều kiện non-shallow trong comment | H23 |
| D27 | 319 | Bắt nội dung EVIDENCE về trạng thái GitHub | H24 |
| D28 | 321–331 | Lặp nghĩa vụ cấu hình rồi bắt reviewer khai lý do tương ứng | H24 |
| D29 | 333–337 | Lặp thời điểm duy nhất trước clone, trên kho nguồn | H24 |
| D30 | 339 | Hai chốt bộ lọc đều bắt buộc | H25 |
| D31 | 355–357 | Bắt tạo verdict ngay và dùng changes_requested/0 làm placeholder | H29 |
| D32 | 358–359 | Bắt ghi sau mỗi hướng rồi mới sửa header cuối lượt | H29 |
| D33 | 364–367 | Phân công các loại thao tác reviewer được làm | H29 |
| D34 | 368–369 | Cấm loại nội dung và phân việc viết probe cho điều phối | H29 |
| D35 | 374 | Bắt bảng săn; tự định nghĩa approve là chưa tìm nếu thiếu | H30 |
| D36 | 383–384 | Ấn định khối bảng bắt buộc | H31 |
| D37 | 394–395 | Định nghĩa loại hướng không được tính vào N | H32 |
| D38 | 396–397 | Bắt liệt kê lịch sử và cấm lặp hướng | H32 |
| D39 | 398 | Thiếu bảng thì approve bị coi KHÔNG ĐO ĐƯỢC | H32 |
| D40 | 394 | Bộ ba điều kiện bắt buộc để bảng có giá trị | H32 |
| D41 | 400–402 | Ấn định câu phải đưa vào prompt lượt xác nhận | H32 |
| D43 | 432 | Bắt dọn xong mới đo, đo nền trước nghi bản vá | H35 |
| D44 | 434–436 | Khung verdict bắt reviewer sinh | H35 |
| D45 | 439 | Sao bộ giá trị verdict canonical vào schema mẫu | H36 |
| D46 | 442–443 | Bắt đối chiếu từ lượt 2, bộ nhãn phân loại bắt buộc | H36 |
| D47 | 445 | Lặp thiếu bảng thì approve = KHÔNG ĐO ĐƯỢC trong template | H36 |
| D48 | 451 | Định mức hướng độc lập N ≥ 6 | H37 |
| D49 | 453 | Bắt kê mọi số đã đo trong template | H37 |
| D50 | 464 | Đòi cả số khớp, định nghĩa chỉ kê số lệch là giấu công | H38 |
| D51 | 485–488 | Đòi cây đã sửa, đừng đòi diff | H39 |
| D52 | 488 | Đặt nghĩa vụ sinh/tự kiểm artifact khi chọn diff | H39 |
| D53 | 492 | Bắt ghi rc vào verdict trong comment | H40 |
| D54 | 495 | Đăng lên PR là bước bắt buộc do adapter tự tuyên | H41 |
| D55 | 503–504 | Chưa đăng thì lượt review không tồn tại | H42 |
| D56 | 505–506 | Bắt ghi đường vận chuyển vào verdict | H42 |
| D57 | 519 | Lặp exact head thực đọc/đưa ra review | H43 |
| D58 | 520 | Bắt đọc lại khi head đổi | H43 |
| D59 | 522–524 | Bắt giữ slug qua lượt và cấm đặt slug mới cho lỗi cũ | H43 |
| D60 | 345 | Tiêu đề bắt reviewer ghi verdict tăng dần | H27 |
| D61 | 404 | Tiêu đề bắt dọn tiến trình trước mỗi phép đo | H33 |
| D62 | 86 | Lặp nghĩa vụ kiểm modelUsage sau phóng | H8 |
| D63 | 222–224 | Chép nguyên tắc neo theo KHO, không theo đường dẫn | H13 |

Các phần được giữ vì thuộc công cụ: ba tên Python; cờ/cú pháp CLI; mô tả input/output và lỗi của helper; giới hạn đọc header; cách giải bản ghi /proc; so tập ref thay vì đếm; cờ core.abbrev; phản chứng pkill; số đo lịch sử có gắn bối cảnh. HINT diễn đạt bảng bậc/ratchet/modelUsage như hành vi của chon_reviewer.py, không dựng một chính sách model mới. Không thay những nghĩa vụ bị bỏ bằng luật mới ở đoạn khác, cũng không tự thêm luật sang protocol ngoài phạm vi patch.

**Mục dọn thư mục L176–186 đã vá thật:** sáu nghĩa vụ D1–D6 của lượt 4 không còn; mktemp chỉ tạo thư mục, không thu hiện vật/hạn lưu/tự dọn; phần quyền/phân công/vòng đời là con trỏ. Lớp doctrine toàn adapter chưa đóng do bảng trên, không phải do ba chốt dọn tái xuất hiện ở câu mới.

## Ba lớp — bảng quét

Cách quét: [diff -U0](evidence/diff-u0.patch), phân hoạch **23 vùng liên tiếp, phủ 532/532 dòng toàn tệp và 112/112 dòng thêm**. Với từng vùng đọc chủ thể/lượng từ/loại nguồn và suy luận; trạng thái thực, rc và dữ liệu thiếu; mọi con số, mẫu số, đơn vị và quy đổi. Đối chiếu phần mới với các mục cũ. [Bảng đủ 23 vùng](evidence/scan-inventory.md), [dữ liệu](evidence/scan-inventory.json), [script](evidence/write_verdict.py). Script kiểm độ phủ dòng; đánh giá nghĩa là công việc reviewer, không phải một semantic gate tự động.

**loi-khai-vuot-phep-do: 4 dòng sống** ngoài diff mới:

| ID | Dòng HEAD | Phép hỏi hẹp → kết luận rộng | Bằng chứng / hunk |
|---|---|---|---|
| E01 | 232–233 | status/log sạch ở thời điểm kiểm → “reviewer đã tuân cấm”. | Clone sạch → ghi adapter → hoàn nguyên: trước/sau hai output đều rỗng; đã ghi là sự kiện ghi nhận được. [Probe](evidence/clean-snapshot-counterexample.json). H15. |
| E02 | 341–343 | Ba lượt bị ngắt và hiện vật còn lại → hai chốt làm hậu quả rẻ hơn, có số chống đỡ. | Bảng không đo cùng một workload có/không từng chốt, không có đại lượng chi phí và không cô lập hiệu quả nhân quả. H26 giữ 3/13 và loại kết luận hiệu quả. |
| E03 | 353 | Prompt lượt 12 có ba câu → “khác biệt duy nhất” với lượt 8/11. | Tệp chỉ đưa thời điểm ngắt/hiện vật; không có phép so đủ ba prompt, đầu vào, trạng thái model/môi trường. Không xác định được tính duy nhất từ bảng đó. H28. |
| E04 | 406–408 | Hai lần có child còn sống → mọi test phóng con rồi bị giết đều bỏ rơi con. | Fixture bị SIGTERM giữa lượt có handler terminate/wait child: parent rc=143, ps child trước 0/sau 1. [Probe](evidence/child-lifecycle-counterexample.json). H34. Không khái quát fixture này thành xử lý được SIGKILL. |

E02/E03 là phân tích phạm vi của bằng chứng được tài liệu đưa ra, không tự khai đã replay bộ lọc hoặc phủ nhận các số lịch sử. HINT giữ bảng 154/437/299 giây, 3/13, 35 lệnh, các finding và 526 child/14,5 GB; hạ kết luận nhân quả/phổ quát, không phủ dữ liệu bằng lời “có thể” vô nghĩa.

**phan-hoach-trang-thai: 3 dòng sống**, đã tính trong finding doctrine, không cộng ba P2 mới:

| ID | Dòng HEAD | Trạng thái bị tự quy lại | Hunk |
|---|---|---|---|
| D35 | 374 | approve thiếu bảng bị đồng nhất với “chưa tìm”. | H30 |
| D39 | 398 | approve thiếu bảng thành KHÔNG ĐO ĐƯỢC theo tiêu chí adapter tự đặt. | H32 |
| D47 | 445 | Cùng phép quy trạng thái trong template. | H36 |

Trong **112 dòng thêm**, hai lớp trên đều 0 thể hiện sống sau phản chứng: EOF/CLI lỗi/chưa review tách đúng; không đọc được khóa là chưa đo; khóa khớp không suy sống; S/Z/vắng tách đúng. Hai mẫu mtime bằng nhau không suy đã chết. Các mẫu stat chỉ là thuộc tính tệp, không chứng nhận reviewer hoàn tất. Không dùng rc cuối block để chứng nhận mọi lệnh trước.

**don-vi-byte: 0 dòng sống.** Bảng thể hiện sống rỗng:

| Vị trí | Sai đơn vị / quy đổi / tỷ số | Bằng chứng |
|---|---|---|

Đã rà: bốn nhóm Codex/ba model từ chối/bốn effort; ngày và khoảng 4 giờ; hai sự cố; khóa Linux trường 22 là tick, không phải lstart; 80 dòng đầu/50 dòng cuối; hai mẫu cách 60 giây, %Y giây mtime và %s byte; 7 lượt/6 HINT/13 hunk riêng #518, không cộng mẫu số 2/5 #250/#252; 3/13 bộ lọc; 154/437/299 giây; số hướng ≥6/8/2; 526 tiến trình và 14,5/16 GB. “131072 byte” của probe là 131072 ký tự ASCII trên Linux này, không phải ngưỡng mọi OS. Lỗi argv là giới hạn cách truyền dữ liệu, không phải sai quy đổi byte.

## Lớp KHÁC tìm được

**prompt-qua-argv, A01 tại L81–84:** lệnh Claude còn `-p "$(cat PROMPT.md)"`, cùng lỗi nền OS với câu Codex đã sửa tại L101–105. Chạy **CLI Claude thật cộng --help** để không gọi mạng/model: prompt 131072 byte làm bash trả **126 / Argument list too long**, OS probe execve trả errno 7/E2BIG. Lệnh stdin sửa lại cộng --help trả **0**. Probe child riêng xác nhận marker argv đọc được trong /proc/cmdline. Stand-in được ghi nhãn rõ kiểm đúng shell redirection mới: đọc đủ 131072 byte ở stdin, không có đối số lớn. [Log](evidence/argv-probes.json). **H7** đóng cả lời hướng dẫn chủ động và diễn giải đi kèm. --help/stand-in không được gọi là full Claude review thành công.

Lớp doctrine đã kê đầy đủ ở trên. Không tìm thêm lớp mới ngoài ba finding cuối verdict. Các hướng ưu tiên khác:

| Hướng | Phép kiểm thực tế | Kết quả và giới hạn |
|---|---|---|
| HINT 4: EOF qua launcher | CLI Codex 0.154.0 nhận stdin rỗng; launcher thật gọi child Python đọc stdin và child đọc {PROMPT_FILE}. | CLI rc=1/No prompt provided via stdin.; child stdin rỗng, snapshot đúng byte. [EOF](evidence/codex-eof.json), [launcher](evidence/launcher-stdin.json). Không có review model được chạy. |
| HINT 4: helper runpy | Trích đúng dòng lệnh từ adapter; chạy 5 tên child thật: plain, khoảng trắng, dấu ), newline, hỗn hợp. | Tất cả rc=0/khớp helper. Cùng PID 13: S→Z giữ linux:66673; sau wait rc=1/KHONG_DO_DUOC. [Log](evidence/key-probes.json). Không có lỗi import/runpy ở lệnh mới. |
| HINT 4: trạng thái | So khóa và ps ở S/Z/vắng; đọc lại L164–171. | Câu mới phân biệt danh tính/trạng thái/tiến triển, không tuyên sống khi khóa khớp. Không tái lập reboot/PID reuse. |
| Hai mẫu tệp | Chạy nguyên block chẩn đoán, gồm sleep 60 thật, child yên lặng. | 60,183 giây; cả hai mẫu `1789216569 8`; child vẫn sống. [Log](evidence/diagnostic-full-block.json). Không thấy câu khác lấy hai mẫu bằng nhau làm bằng chứng chết. |
| HINT 2: sed/80/cảnh báo | Sáu fixture đủ/rỗng/body-only/thiếu effort/header sau 90 dòng/tiếng Việt; thêm tệp vắng và đọc 81–160. | Sáu ca đọc rc=0, tệp vắng rc=2; sed chỉ hiển thị ngữ cảnh. Câu mới đã khai giới hạn, không coi 80 là parser hoặc ngưỡng đủ. Không có phép đo chọn 80 tối ưu. [Log](evidence/display-probes.json). |
| Idiom hai dòng Python | PATH chỉ có lần lượt python3, python, py trỏ interpreter thật; chạy assignment và json.tool. | Ba ca rc=0; selftest 7/7, 9 mutant. Chưa đo Windows thật. [Log](evidence/idiom-three-names.json). |
| Replay HINT cũ | Áp HINT 1/2/4 lên blob gốc đúng lượt, --fuzz=0. | rc=0; HINT 2/4 bằng byte commit sửa, HINT 1 chỉ lệch phần idiom bổ sung. [Log](evidence/prior-hint-replay.json). Không nhận đây là replay sáu HINT #518. |
| HINT ở trên lane cây | Chạy lane p0 strict và lane diff có label a/cay,b/cay + patch -p1. | Hai layout dùng được; diff rc=1 vì có thay đổi, patch strict rc=0. Mệnh lệnh “đòi cây, đừng diff” là D51, đã hạ thành dữ kiện của mẫu #250/#252. |
| Fuzz | Đổi context fixture. | Dry-run mặc định rc=0/fuzz 1; strict rc=1; hoàn nguyên strict rc=0. [Log](evidence/lane-and-fuzz.json). Câu mới của HINT #518 giữ --fuzz=0. |
| Model/account/quota | Đọc từng câu L115–139 cạnh các lỗi được prompt thuật lại. | max chỉ nói spark; ba lần từ chối không suy tập account nhỏ; cạn/gọi được không suy số pool/độc lập; reset là dữ liệu dịch vụ. Thiếu raw model log để tái xác thực lịch sử. |
| Hai merge | Hợp cây theo path/mode/blob từ merge-base và hai parent; kiểm toàn cây merge. | Cả #479 và #472 đều 2082 entry, 0 conflict, 0 sai khác so cây hợp. Adapter giữ đúng phía nhánh. [Log](evidence/structural.json). |
| Merge #479 | Bỏ dòng comment của wrapper phía master rồi so. | 130 dòng không-comment mỗi phía, byte/thứ tự bằng nhau; master đổi wrapper và tài liệu review. Không chạy wrapper có mạng/dọn. |
| Merge #472 | So ba path master thay đổi. | release.py thêm loại .agents; tl_selftest thêm 62 dòng regression; manifest lấy đúng phía master. Không gọi #472 là chỉ-comment. Các thay đổi này có trong base, không thuộc diff adapter. |
| Manifest | `python3 scripts/tl.py release-manifest --root . --out <scratch>/RELEASE_MANIFEST.generated.json --json`. | rc=0, bằng byte manifest HEAD; manifest merge bằng parent master. **Tái lập được bằng tooling**, không chứng minh công cụ/actor tạo commit lịch sử. |
| Ref và băm gói | So tập tên+OID refs/heads, băm lại ARTIFACTS.sha256. | Review/mirror/hai clone đều 355 ref, mỗi delta=0; 3572 mục băm, 0 lệch. [Log](evidence/package-integrity.json). Không kiểm GitHub trực tiếp, tag hay namespace ngoài heads. |

Bốn khối trọng tâm chạy thật: doctrine bằng idiom; Codex nhánh EOF (full model NOT_RUN); sed trên fixture; block chẩn đoán đầy đủ với sleep 60. Lệnh bộ chọn chon_reviewer.py cũng chạy rc=0. Không gọi các lệnh cài đặt, publish/comment/record state, phóng full reviewer hoặc pkill theo mẫu trong các phần cũ. Probe lifecycle chỉ gửi tín hiệu cho tiến trình do chính script tạo.

## Phép đo nền

Clone đầy đủ từ mirror **cục bộ**: `/tmp/rv521-l5.Sc0QH0/gates-main`; clone phản chứng `/tmp/rv521-l5.Sc0QH0/experiments`. Detached exact head, non-shallow, 355 refs/heads, core.abbrev=7, core.autocrlf=false; status ban đầu rỗng. Origin đặt URL thật để tái lập cấu hình danh tính, không fetch URL ấy. [Setup gates](evidence/setup-gates-main.json), [setup probes](evidence/setup-experiments.json), [runner](evidence/run_gates.py).

| Lệnh từ gốc clone gates-main | rc | Bằng chứng dương |
|---|---:|---|
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | 7 tệp, 0 chuỗi cấm. [Log](evidence/gate-doctrine.json). |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | 47 ADR ↔ 47 hàng; ngoại lệ trạng thái 0016 được công bố. [Log](evidence/gate-adr.json). |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | 113 đạt v2 + 11/11 miễn legacy + 42 nợ đóng băng = 166; 0 vi phạm/chưa đo. Không gọi cả 166 là đạt v2. [Log](evidence/gate-receipts.json). |
| `python3 ops/lease_publish_test.py` | 0 | 147/147 chạy, bỏ qua 0; 37 mutant: giết 34, sống chủ ý 3, tín dụng giả 0. [Log](evidence/gate-lease.json). |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | ok=true, expected=checked=180, package hash khớp; thiếu/lỗi/thừa đều rỗng. [Log](evidence/gate-release.json). |
| `python3 scripts/tl.py golden-test --json` | 0 | ok=true, 20 ca. [Log](evidence/gate-golden.json). |
| `python3 scripts/tl.py doc-claims-check --strict --json` | 0 | ok=true; 107 tệp, 0 hard flag, 374 advisory, 0 layer skipped. [Log](evidence/gate-claims.json). |
| `python3 .githooks/eol_policy.py --all --json` | 0 | 2082 scanned, 2060 checked, 22 skipped, 0 vi phạm. [Log](evidence/gate-eol.json). |
| Bổ sung: `python3 .claude/dev/idiom_py_test.py` | 0 | 7/7, bỏ qua 0, 9 mutant, 7 tệp; 389 lời gọi trần ngoài phạm vi là nợ chẩn đoán. [Log](evidence/gate-idiom.json). |

Không cổng nền nào đỏ nên không có finding cổng cần lặp trên clone sạch thứ hai. Các rc đỏ trong mutation, CLI thiếu prompt, argv quá dài và fuzz là kết quả phản chứng có chủ đích. Sự cố harness của reviewer được xử lý trước khi nhận kết quả: lần clone đầu fetch heads khi master checkout trả 128, dựng clone mới và detach trước fetch; PATH chỉ Python làm không tìm thấy bash, sửa gọi /bin/bash rồi tiếp tục từ phần chưa chạy. Không nhận hai lỗi harness ấy là lỗi sản phẩm. Thư mục thử dở vẫn được giữ, không dọn.

Môi trường: Python 3.11.15, Git 2.43.0, GNU patch 2.7.6, shellcheck 0.9.0; actionlint 1.7.7 của gói được đặt trong PATH. Không gọi bộ cổng này là full CI GitHub hoặc full runtime selftest.

## Đột biến và khôi phục

Thử trên clone experiments, không chạm cây review. [Script probes](evidence/probes.py), [log M1/M2](evidence/mutations.json), [M3](evidence/clean-snapshot-counterexample.json).

| Phép thử | Lệnh / biến đổi | rc trước → sau → khôi phục | Kết luận |
|---|---|---|---|
| M1 — cổng doctrine đúng tệp | Thêm `max_attempts_per_packet` vào adapter rồi chạy doctrine-scan. | **0 → 6 → 0** | Cổng có răng với chuỗi, không phát hiện 60 mệnh đề nghĩa. |
| M2 — mới của lượt 5, câu helper HINT 4 được ưu tiên nghi | Trong adapter tạm đổi `sys.exit(0 if k else 1)` thành `sys.exit(0)`; trích/chạy lệnh đó với PID vắng, oracle đòi rc=1 và KHONG_DO_DUOC. | CLI **1 → 0 → 1**; oracle **0 → 1 → 0**; doctrine mutant vẫn **0**. | Oracle bắt mất trạng thái chưa đo dù stdout giữ nguyên. Không chỉ nhìn mã 0/chuỗi cổng. |
| M3 — lời khai E01 | status/log tại HEAD, ghi thêm một dòng bình thường vào adapter clone, ghi lại quan sát, rồi hoàn nguyên và đọc lại. | Hai lệnh rc **0 → 0 → 0**; status chỉ có dòng thay đổi ở giữa, trước/sau rỗng. | Ảnh chụp sạch không phân biệt không-ghi với ghi-rồi-hoàn-nguyên. SHA-256 trước/thay/khôi phục lưu trong log. |

Mỗi mutation đã khôi phục adapter đúng byte; git status --porcelain rỗng. Cả việc áp HINT thật sau đó cũng hoàn nguyên đúng byte, status rỗng. Không chạy chuỗi tấn công đường dẫn hay payload thoát thư mục.

## HINT.patch và giới hạn

**Nhãn patch-as-hint:** “chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”. Quyền tạo HINT và thử clone được PROMPT.md giao tường minh. HINT là dữ liệu review, không là commit hoặc approval.

HINT.patch có **43 hunk / 1 tệp** `.claude/skills/cross-review/SKILL.md`; unified diff repo-relative, dùng patch -p0. Mỗi hunk thuộc đúng một finding; các hunk không có dòng context để không gộp hai finding, nhưng các dòng xóa được so nguyên byte. Đã chạy đúng `cd cay-kho && patch -p0 --dry-run < ../HINT.patch`: rc=0; thêm --fuzz=0 --verbose cũng rc=0. Áp thật ở clone experiments bằng patch -p0 --fuzz=0: rc=0, 43/43 hunk, **không fuzz/offset**, byte bằng [bản soạn](evidence/adapter.fixed.md). [Log kiểm](evidence/hint-validation.json), [bản đồ hunk](evidence/hint-map.json), [script tạo](evidence/build_hint.py).

SHA-256 HINT.patch: `c1248ed9ae7c6df61d6fa3abc520575765082449b51d165701e0c90144e6d778`.

| Finding | Hunk sở hữu duy nhất | Thể hiện đóng |
|---|---|---|
| adapter-chep-doctrine | H1, H2, H3, H4, H5, H6, H8, H9, H10, H11, H12, H13, H14, H16, H17, H18, H19, H20, H21, H22, H23, H24, H25, H27, H29, H30, H31, H32, H33, H35, H36, H37, H38, H39, H40, H41, H42, H43 | 60 ID trong bảng doctrine, 38 cụm vị trí |
| loi-khai-vuot-phep-do | H15, H26, H28, H34 | E01–E04 |
| prompt-qua-argv | H7 | A01 |

Sau áp, doctrine/idiom/doc-claims strict/eol đều rc=0. Đọc lại toàn bản thay thế: các 60 mệnh đề nghĩa vụ đã chuyển thành con trỏ hoặc mô tả hành vi công cụ; những chữ “phải” còn lại trong ví dụ lệnh/cú pháp và trích prompt lịch sử không tạo tiêu chí áp dụng chung. E01–E04 được thu hẹp đúng đối tượng/bằng chứng; lệnh Claude truyền stdin. Bảng thể hiện của các lớp đã kê về 0 trên bản gợi ý. Đây là đánh giá nghĩa kèm phản chứng, không suy từ doctrine-scan. Verdict vẫn changes_requested vì HEAD được giao chưa chứa HINT.

Giới hạn: không đo account/model/API/quota/reset/pool thật, danh tính backend hay tác động effort lên chất lượng; không phóng full Claude/Codex review. Không có raw log sáu HINT #518, năm hiện vật #250/#252, toàn bộ prompt/run #513 để replay nhân quả; không tái lập reboot/PID reuse/Windows/Darwin/runner tích clone dài ngày. Không gọi GitHub/CI/lease trực tiếp. Tái sinh manifest chứng minh byte tái lập được, không chứng minh provenance lịch sử. Không sửa protocol, launcher, release/gate hoặc nợ ở tệp khác. Các pointer HINT không tự tạo chính sách dọn còn thiếu trong hệ thống.

Đã tạo VERDICT/HINT trước phép đo, cập nhật sau các hướng/cổng; [nhật ký trước bản chốt](evidence/verdict-progress.md). Chỉ số và log evidence/ là phép đo của lượt này, trừ các tệp `.source.md` được ghi nhãn thừa kế.

### adapter-chep-doctrine  [P2]  Luật review vẫn được đặt rải rác trong adapter mỏng

60 mệnh đề tại 38 cụm vị trí, liệt kê đủ ID/dòng/hunk ở bảng doctrine. Ví dụ rõ nhất: L394–398 đặt ba điều kiện bảng săn và tự hạ approve; L439–453 lặp schema/định mức ≥6; L495–506 định nghĩa hoàn tất. Chúng vi phạm ranh giới nội dung của protocol §13 dù có con trỏ và dù doctrine-scan xanh. Lỗi nằm ở vị trí đặt thẩm quyền, không phải ý tưởng lưu bằng chứng/cách ly là sai. **38 hunk thuộc hàng adapter-chep-doctrine ở bảng HINT đóng cả nhóm**, giữ lệnh/công cụ và dữ kiện lịch sử; đọc lại bản thay thế không còn các nghĩa vụ đã kê. Độ tin cao cho các tiêu chí/phân công/hoàn tất; phần lựa chọn model được sửa bằng neo rõ hành vi công cụ, không thay bảng bậc.

### loi-khai-vuot-phep-do  [P2]  Ảnh chụp và vài sự cố bị dùng làm chứng nhận toàn lượt hoặc kết luận phổ quát

**4 thể hiện E01–E04; H15/H26/H28/H34 đóng cả lớp đã tìm.** E01 có phản chứng ghi-rồi-hoàn-nguyên trên clone; E04 có fixture SIGTERM thu hồi con. E02/E03 là suy luận nhân quả/tính duy nhất vượt bảng lịch sử có trong tệp; không có bằng chứng đối chứng được cung cấp để giữ các lượng từ ấy. HINT giữ các số thực đã kể và chỉ hạ phạm vi kết luận. Đây cùng mô thức phép hỏi hẹp→kết luận rộng được prompt yêu cầu săn, ở những đoạn cũ chưa được lượt trước đóng. Độ tin cao cho E01; cao với lượng từ phổ quát của E04 trong phạm vi SIGTERM; vừa cho E02/E03 do giới hạn nguồn lịch sử đã khai.

### prompt-qua-argv  [P2]  Bản vá stdin cho Codex còn bỏ sót lane Claude

**A01 tại L81–84; H7 đóng lớp.** Shell mở rộng cả PROMPT.md thành một đối số trước exec; 131072 byte ASCII làm lệnh Claude thật với --help thất bại rc=126/E2BIG trước CLI, độc lập với model/quota. Một prompt nhỏ còn hiện trong cmdline của tiến trình được tạo. Cùng tệp đã mô tả đúng hai nhược điểm này cho Codex, nhưng mẫu Claude vẫn chủ động dùng argv. H7 dùng -p với stdin và thu hẹp câu “hai dạng đều chạy” về phép thử lịch sử. Đã kiểm CLI help và tuyến dữ liệu shell; full model không chạy vì cấm mạng. Độ tin cao về lỗi OS/tuyến argv, không khai đã đo end-to-end Claude review.

Kiểm cuối: HEAD/tree đúng; cây review và hai clone status rỗng, adapter bằng byte blob HEAD; 3 heading finding hợp lệ, liên kết evidence tồn tại, HINT khớp hash đã áp thử. [Log kiểm cuối](evidence/final-check.json).
