# Cross-review wp1179 C1a1b r4 — lượt 4

- reviewed_sha: `3646365f965478fbe79be4a975f4eb3075ab405d`
- spec_sha256: `348340b05edf987d6de1ac504407c9065bfcd2c2c3db15c5f029126596d40188`
- reviewed_tree: `90f2f210cc18aebd7db10e857eab117bea2174e3`
- provider: `openai_codex`; execution_surface: `codex_cli`; transport: `machine`, theo `../run/6405185b/run.json` đang chạy.
- model/effort tự khai: GPT-6/Codex theo chỉ thị phiên; model triển khai cụ thể và effort đã phục vụ **KHÔNG ĐO ĐƯỢC** từ metadata của run hiện tại khi đọc. Không suy `gpt-6-astra/xhigh` từ yêu cầu trong spec; `run.json` chưa phải receipt terminal.
- run_id: `6405185bee12437984e253f2a85b9b2b`.
- verdict: **`changes_requested`** — F9 sửa được nhánh dùng trực tiếp cận dưới, nhưng chưa đóng lớp; phát hiện đường thứ bảy F10, lỗi bảng đóng F11 và hướng dẫn CLI F12.

## Phạm vi và tiến độ

Review độc lập toàn bộ r4, neo base số đo `889334fb87c25136a13c6776a40a25b401820e04`. Đã đối chiếu HEAD, tree và SHA-256; mirror không shallow, `origin/master=d26b36f5d2f952c2d952d58517571ffe27c4f826`. Đã đọc các đoạn áp dụng của AGENTS, protocol, CLAUDE, kế hoạch provider, ADR-0043/0048/0052/0055/0060, spec C1a1a và lịch sử verdict r1–r3. Không sửa kho đang review; không gọi model khác, connector, mạng, lease thật hay CI.

Đã ghi verdict tăng dần: khởi tạo sau preflight; bổ sung F9 và hai phản chứng; hoàn tất bảng lớp, A1–A21, finding và kiểm tra cuối. Script/prototype/state giả/evidence được lưu tại sandbox. **Sai sót thực thi của reviewer:** các lần chạy đầu của suite JSON, producer và A18 dùng `tempfile` mặc định dưới `/tmp`, chưa ghim vào sandbox như chỉ thị. Đã sửa `probe_common.py` để đặt cả `TMPDIR` và `tempfile.tempdir` vào `sandbox/tmp`, rồi chạy lại các phép đo liên quan. Không tuyên bố toàn bộ lượt đã tuân thủ giới hạn vị trí scratch; việc này không phải finding của spec. Kho review vẫn sạch ở phép kiểm cuối.

## F9

| Đối tượng | Kết luận | Căn cứ |
|---|---|---|
| F9, nhánh r3 §11.1(b) dùng `U=6` hoặc tự hạ limit | **Biểu hiện trực tiếp đã vá** | Nhánh bị bỏ; r4 phân biệt `U_lower`, `U_max`, allowance và số dư. Không còn dùng `10−U_lower` hay `16−U_lower` làm công thức cấp. |
| F9 theo lớp `dat-lai-ngan-sach-khi-doi-truc` | **VÁ MỘT PHẦN, chưa đóng lớp** | Nhánh phục hồi từ state ở §11.1 vẫn nâng số đếm chưa chứng minh đầy đủ thành cận trên; F10. |
| Ngoại lệ allowance khi `U_max` unknown | **Không phải finding** | §8 ghi rõ đơn vị, pha, giới hạn 4/3 và không khẳng định tổng ≤16. Chỉ thị hiện tại chấp nhận Q-NT; không dùng trường hợp unknown vượt 16 để bác ngoại lệ đã được cấp. |
| A21 và bộ đếm thật | **Các ca số học đã qua; thiếu ca nguồn cận trên** | Unknown/7/14/16 → cap 3/3/2/0. Các limit dương được đọc lại từ `status`; đúng số lời gọi được ghi rc 0, lời tiếp theo rc 3. Limit 0 thật bị rc 2, bỏ cờ thành mặc định 2. F10 không bị bảng ca hiện tại bắt. |

**Quét đủ đường cùng lớp, không chỉ grep công thức:** sáu đường của §0.5 đều được đối chiếu với r3. Kết quả:

| Đường | Chỗ trong r4 | Kết quả |
|---|---|---|
| 1. §8 cấp `10−U` | 514–527 | Đổi sang allowance/min với cận trên; không reset lịch sử packet. |
| 2. §11.1 dòng “còn lại ≤4” | 589–592 | Giữ cận dưới 7, cận trên và số dư unknown. |
| 3. §11.1 phục hồi **(b)** | 599 | Bỏ rõ nhánh dùng cận dưới. |
| 4. §11.2 init | 606 | Dùng `cap(thi_cong)` và chặn cap≤0; còn lỗi đối số F12. |
| 5. §10 điểm 8 | 571 | Cùng công thức với §8. |
| 6. §0.3 F1/Q-NS | 76, 80 | Đánh dấu lịch sử và phần bị thay; không còn là chỉ dẫn dùng 10−U hiện hành. |
| **7. §11.1 phục hồi (a) của r3** | **596–598**, được §8 dòng 515 dẫn lại | **Chưa đóng:** raw status + băm + những lời gọi ngoài state đã ghi không tự chứng minh cận trên. R3 dòng 530–531 đã có đường “U lấy từ đó”; danh sách sáu chỉ liệt kê (b). R4 đổi nhãn kết quả thành `U_max` nhưng chưa thêm chứng cứ đầy đủ. F10. |

Đã quét thêm §0/§7/§9/§10, connector, timeout, đổi phiên/revision/init và sự khác nhau giữa lời gọi/vòng/attempt. Không thấy đường thứ tám độc lập cần báo ngoài F10. Cấm reset `U` và đếm theo pha vẫn có hiệu lực; state mới không chứng minh một allowance mới.

Phép đo: `PYTHONDONTWRITEBYTECODE=1 python -B probe_budget.py` **rc 0**, [log](evidence/budget-r4.txt); `python -B probe_phase.py` **rc 0**, [log](evidence/phase-r4.txt). Pha spec limit 4: đã dùng 1 thì còn 3, lần thứ 5 bị rc 3. Chỉ tạo state giả, không tạo lời gọi model. Việc đặt fixture vào `reviewing` là setup phản chứng, không giả nhận đã cấp lease hoặc replay transition production.

## Bảng lớp

| Slug lớp | Lịch sử / phạm vi quét | Mức mở | Kết quả, cách vá chung và phép đóng |
|---|---|---|---|
| `mo-rong-module-pha-hop-dong-json-thuan` | draft0–2, r1; §2.1–2.2/A1–A4 | — | Không tái mở. Byte module JSON giữ nguyên; module mới bọc nguyên dict. Giữ oracle dương/K1/K2/K4 và kiểm byte ở PR thi công. |
| `phan-loai-vang-va-khong-do-duoc` | F4/r1, F6/r2; §2.3×G6/G7/G8, A7/A10–A14/A20 | **P2** | F6 thứ tự so OID vẫn vá thật; **F11 tái mở** ở miền tên entry của `E_hong`. Bổ sung một predicate hợp lệ của tên vào parser chung và bảng đóng; khóa G6/G7/G8 cùng đối chứng không liên quan. |
| `dot-bien-tuong-duong-hoac-thieu` | F3/r1, F7/r2; A4/A5/A9/A13/A18/A20 | — | A18 dương trước, dependency registry/gốc kho, lỗi import đúng tệp và mutant caller đều phân biệt được. Không tính mutant parser chưa được yêu cầu vào F3; nghĩa vụ thiếu nằm ở F11. Bảng nghĩa vụ cuối vẫn phải audit trên implementation. |
| `oracle-trang-thai-g0-mau-thuan` | F8/r2; A6/A13 và ABI | — | Không tái mở. K1/K2 đỏ dưới trần giữ G0 qua, G1–G9 không chạy; quá trần mới G0 đỏ/json null. |
| `predicate-consumer-khong-khop-producer` | F2/r1; mode/type G6–G8 | — | Biểu hiện F2 về symlink vẫn đóng. G6 so metadata không đọc leaf; G7/G8 nhận blob của symlink, bác gitlink/tree theo ngoại lệ đã khai. Sai khác tên hỏng F11 được gán lớp parser/phân loại, không đếm hai lần. |
| `dat-lai-ngan-sach-khi-doi-truc` | F1/r1, F9/r3; toàn bộ §0/§7–§11/A21 | **P2** | **F10**, cùng cơ chế coi số đã ghi là lịch sử đủ. Chứng minh completeness/cận trên trước khi đổi unknown thành số; mở rộng A21 bằng cùng status nhưng lịch sử thật khác nhau. |
| `so-do-ke-thua-chua-do-lai` | F5/r1; S2–S6, §3, §11.5 | — | Số commit/byte/diff/suite tái lập. Không dùng ref-count hay holder lịch sử làm phép đo live; không coi ước 710 là số dòng implementation. |
| `nguon-duoc-tin-ma-chua-xac-minh` | C1a1a §6; reader/N6/§5/§6/§11 | — | Hash, replace và exact ref có đối chứng. F10 được gán riêng lớp ngân sách. C1a2/C1b, API, workflow đã chạy, quota và holder live chưa được chứng minh; spec đã giữ giới hạn ấy. |
| `huong-dan-cli-khong-khop-parser` | **Mới**, §11.2, liên hệ §8/A21 | **P3** | **F12**, hai biểu hiện cùng nguyên nhân: thiếu đối số bắt buộc và sai loại `can-cu`. Cung cấp invocation đầy đủ rồi chạy CLI thật với đối chứng âm/dương. |

Đếm riêng: **9 lớp** đã quét (8 kế thừa + 1 mới); **3 lớp mở / 3 findings mới**, F12 có hai biểu hiện. Tập lớp mở cuối r3 chỉ có lớp ngân sách; r4 chưa đóng trọn lớp ấy ⇒ **0/1 = 0%**. F11 là lớp tái mở, F12 là lớp mới, không đưa vào tử số. Lớp ngân sách đã có mặt ở lượt 1, 3, 4; cần trình tại checkpoint theo protocol §12, không đổi slug để xóa lịch sử. Q-NT vẫn là authority của lượt review hiện tại; verdict này không tự cấp lượt tiếp theo.

## Findings mới

### F10 — P2 — `dat-lai-ngan-sach-khi-doi-truc`

**Vị trí:** r4 §11.1 **596–598**, §8 **514–516**, A21 **439**; đường tiền nhiệm r3 §11.1(a) **530–531**.

**Lỗi:** câu “khi ấy `U_max` = số lời gọi trong state đó cộng mọi lời gọi ngoài state đã ghi” biến tính toàn vẹn của một sổ thành tính đầy đủ của lịch sử. `packet_loop.py` chỉ tăng tại `record-codex-call` (1296–1311); `status` chỉ đọc/in sổ (3078–3083). Một timeout có output chưa được ghi, một lần connector hoặc một state khác chưa thu hồi vẫn làm số đó là cận dưới. Băm tệp và người đăng có thẩm quyền không tự đảo chiều bất đẳng thức. Nhánh §11.1(a) nằm ngoài sáu đường đã liệt kê; A21 chỉ thử giá trị đầu vào, không thử chứng cứ đủ để gọi giá trị ấy là cận trên.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_budget.py`, **rc 0**, [evidence/budget-r4.txt](evidence/budget-r4.txt). CLI thật ghi 14 lời gọi giả, từng lần rc 0; `status` rc 0 cho `codex_review_calls_used=14`, băm state `0218bc62389e90cfd9471420fa12976579f8d0d12b1eb075c6e348f0d8722c52`. Dùng quy tắc phục hồi trên số đó cho `cap=min(3,16−14)=2`; init rc 0, hai `record-codex-call` rc 0.

| Cùng status/băm và ngoài-state đã ghi = 0 | U thật trước pha | Được nhận thêm | Tổng |
|---|---:|---:|---:|
| Sổ đầy đủ | 14 | 2 | 16 |
| Có một timeout đã sinh output nhưng chưa vào sổ | 15 | 2 | **17** |

Đây là phản chứng cho **nhánh tự nhận đã có `U_max`**, không phải phản chứng cho ngoại lệ unknown đã được chủ kho cho phép. Không khẳng định lịch sử packet thật là 14 hay 15; cả hai là state/lịch sử giả để chứng minh phép phục hồi không phân biệt được hai trường hợp.

**Đề xuất:** §11.1 chỉ được đưa `U_max` về số sau khi có chứng cứ bao phủ toàn bộ phạm vi/mốc thời gian/dispatcher và lời gọi ngoài sổ, hoặc cận trên bảo thủ độc lập. Liệt kê nguồn, đối chiếu run ID để không đếm trùng, ghi mốc tính và cộng tiếp lời gọi phát sinh sau mốc. Raw status riêng lẻ chỉ cập nhật `U_lower`; thiếu chứng cứ đầy đủ thì `U_max=unknown` và tiếp tục **đúng ngoại lệ allowance đã cấp**, không chế ra cận trên. A21 thêm cặp chứng cứ partial/complete cùng giá trị 14: partial không được gắn `U_max=14`; complete mới cấp cap 2. Đột biến đổi số đã ghi thành upper phải làm ca partial đỏ. Không cần sửa `packet_loop.py` hoặc tự tạo journal production; tránh biến bản vá thành yêu cầu hồi tố state giả.

### F11 — P2 — `phan-loai-vang-va-khong-do-duoc`

**Vị trí:** §2.3 **215–216, 228, 233–235**; bảng G6 **276–287**, G7/G8 **295–314**; A20 **438**. Đối chiếu producer `ops/lease_publish.py:2016–2027`.

**Lỗi:** bảng đóng `E_hong` có entry cụt, mode lạ, tên trùng và tên không UTF-8, nhưng thiếu **tên rỗng**. Object có tên rỗng vẫn có OID/hash đúng, mode hợp lệ và tên UTF-8 không trùng. Nó không phát sự kiện nào trong tập đóng đã viết; G6/G7/G8 vì vậy có thể nhận tree không hợp lệ. Producer `KhoObject.tree` có chốt `not ten` và bác tree ấy. Điều này trái lời khai “G6 mô phỏng đúng producer” và làm mất kết quả `khong_do_duoc` cho tree hỏng. Chỉ kiểm hash không chứng minh cấu trúc hợp lệ.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_graph.py`, **rc 0**, [evidence/graph-r4.txt](evidence/graph-r4.txt). Dựng tree bằng object plumbing trong clone scratch, **không checkout tree hỏng** và không soạn payload thoát thư mục. Tree `904feb04b25082aed73d8076ee57570d3735c34c` có một entry tên rỗng và entry checker bình thường; băm lại khớp. Prototype literal của bảng r4 nhận G6/G7 `qua`; producer thật ném `KHÔNG_XÁC_ĐỊNH: tree 904feb04b250 tên entry không hợp lệ/trùng ''`. Git thật `fsck --strict --no-reflogs <root>` rc **1**, stderr có `empty filename in tree entry` và `badTree: cannot be parsed as a tree`. Không dùng riêng rc fsck làm bằng chứng vì kho scratch còn có các object hỏng của ca khác.

Đo cùng sửa chung cho cả ba luật:

| Luật | Parser theo danh sách r4 | Thêm chốt tên rỗng | Tree hợp lệ đối chứng | Luật không đọc tree hỏng |
|---|---|---|---|---|
| G6 | `qua` | `khong_do_duoc:E_hong` | `qua` | So `tree(commit)==T` giữ kết quả |
| G7 | `qua` | `khong_do_duoc:E_hong` | `qua` | Như trên |
| G8 | `qua` | `khong_do_duoc:E_hong` | `qua` | Như trên |

**Đề xuất:** bổ sung vào §2.3 predicate hợp lệ tên entry, tối thiểu tên khác rỗng, đồng bộ các điều kiện tên mà producer áp. Cập nhật `E_hong`, A20 và bảng nghĩa vụ cho G6/G7/G8; mutant bỏ kiểm tên phải bị giết bằng tree băm đúng chứa tên rỗng, cùng ca hợp lệ và luật không cần tree đó giữ màu. Rà cùng lớp: tên thành phần chỉ thư mục hiện tại/cha, tên có dấu phân cách và tên thư mục metadata Git cũng bị producer bác nhưng chưa được liệt kê đủ ở bảng; các hướng có thể biểu diễn thoát thư mục **chỉ mô tả bằng lời**, không tạo dữ liệu thử. Bổ sung validation ở parser chung, không theo symlink, không đổi thứ tự resolve→mode→OID→blob của F6 và không làm G6 đọc leaf.

### F12 — P3 — `huong-dan-cli-khong-khop-parser`

**Vị trí:** §11.2 **606–608**, liên hệ A21 **439**; parser thật `.claude/dev/packet_loop.py:3524`, `1334–1335`.

**Lỗi:** invocation khởi tạo pha thi công thiếu `--mission`, dù parser bắt buộc. Lệnh Rescue chỉ dẫn `--can-cu "<id comment>"`, trong khi parser yêu cầu **URL issuecomment GitHub**, không nhận ID số. Đây là hai biểu hiện của hướng dẫn chưa chạy qua CLI thật. Chúng chặn người thi hành ngay ở đối số; mức P3 vì fail-closed và sửa cơ học, không phải lỗ cấp thêm quyền.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_commands.py`, **rc 0**, [evidence/commands-r4.txt](evidence/commands-r4.txt):

| Lệnh con trong state giả | rc / output |
|---|---|
| `init --packet 1179 --executor claude --reviewer codex --codex-review-calls-limit 3` | **2**; `the following arguments are required: --mission` |
| Cùng lệnh, thêm `--mission 499` | **0**; `state awaiting_lease` |
| Ở đúng `blocked/rescue_required`: `record-rescue --packet 1179 --quyet-dinh revision --can-cu 6686369822` | **2**; `phải là URL issuecomment GitHub` |
| Thay ID bằng URL đầy đủ của comment đó | **0**; `đã ghi rescue revision — state blocked` |

Đã đưa state vào đúng trạng thái bằng bộ đếm thật trước khi thử `can-cu`, nên lỗi không bị che bởi guard state.

**Đề xuất:** ghi đầy đủ `init --packet 1179 --mission 499 --executor claude --reviewer codex --codex-review-calls-limit <cap>`; ví dụ Rescue cần `--packet 1179` và `--can-cu "https://github.com/ducthangho/tra-luat/issues/1179#issuecomment-<id>"`. Giữ cùng `--state-dir` khi init/status/rescue. Chạy các cặp lệnh âm/dương trên state thử để khóa hướng dẫn. Không lấy `record-rescue revision` rc 0 làm bằng chứng đã mở lại state: đo thật vẫn `blocked`, và không tự tạo transition/lease để hợp thức hóa lịch sử.

## Audit toàn bộ r4 và A1–A21

Các kết quả prototype dưới đây kiểm **khả thi, tính phân biệt và nhất quán của đặc tả**. Module Git sản phẩm chưa có trong kho; không khai các phép này là nghiệm thu CLI C1a1b, Windows hoặc CI của implementation.

| Mục | Kết quả / giới hạn |
|---|---|
| A1 | Diff module JSON base→reviewed SHA rc 0; blob `3490ea0ee40081c0eba2d121f5b19a67a021a54b`. Module cũ giữ nguyên byte, không mở lại ABI JSON thuần. |
| A2 | Chạy suite nền thật: 156/156, 162/162, equivalent 9, unresolved 0. Registry `kiem()` trên cây chép: 29/29; thêm module Git vẫn 29/29; thêm test riêng thành 30/29 với lỗi đúng đường. Không cần sửa sổ để thêm nhóm Git. |
| A3 | Gọi `kiem_json` thật cho dương/K1/K2/K4; hợp đồng giữ nguyên dict phân biệt hằng giả/khóa thừa. Import đúng đường của module Git cần kiểm trên implementation. |
| A4 | Ma trận năm tổ hợp a–e cho outer `ok` bool đúng; serializer subprocess trả byte đúng, bỏ sort làm khác ở cả năm. `ok=json.ok` sai ở b/c; bỏ vế JSON sai ở d. Đây là witness ABI, không phải CLI sản phẩm. |
| A5 | Thứ tự 12 trước 13 nhất quán; JSON đỏ/G đỏ thắng unknown. N6 đầu là 2, cuối là 13. Mỗi vế §2.5 vẫn là nghĩa vụ riêng, gồm check-ref-format sau regex và từng OID; chưa chạy CLI sản phẩm chưa tồn tại. |
| A6 | K1 `{}` và K2 sai miền dưới trần: G0 qua, G1–G9 không chạy; K4 đỏ vẫn chạy G. F8 không tái mở. |
| A7 | Graph thật trên MOC: B/MOC qua; P/E/X đỏ. Chuỗi không qua MOC đầy đủ đỏ; mất Q1 do scratch tạo cho unknown. All-parent, bỏ bound và loại MOC có witness khác nhau. Khi thấy C sớm vẫn phải đi tới MOC/root theo cột đọc, không suy bound từ việc gặp C. |
| A8 | A≤B qua, B≤A đỏ, A≤X đỏ; equality qua. Hướng đảo được phân biệt bằng strict ancestor, không dựa ca nhánh rẽ. |
| A9 | Tree S/C/H đôi một khác; T=tree(S) và tree_S=tree(H) giết hai mutant sai nguồn. Ca empty tree chỉ là ca phụ; mutant bỏ guard fixture phải dùng fixture chủ động trùng tree như §4 yêu cầu. |
| A10 | Producer thật và prototype G6 nhận OID của cả năm mode, không đọc leaf; gitlink tới OID vắng vẫn qua. Null/có/vắng/ancestor không tree được tách. F11 bổ sung miền tree hỏng chưa được bảng nhận diện. |
| A11 | F6 đo lại 2 luật × 3 lỗi blob × 2 quan hệ OID: lệch thì đỏ không đọc leaf; khớp mới unknown do missing/hash/type. Mutant đọc trước đổi màu đúng đích. Mode symlink nhận; tree/gitlink bác; G8 sha256 lệch đỏ. Không suy Python đã chạy target hay GitHub nạp workflow symlink. |
| A12 | Loose object sai hash trả bytes qua cat-file nhưng rehash bác; replace bật đổi bytes, reader lọc/tắt replace giữ bytes gốc. Dependency H→G3/G4 và không→G1 đúng. GIT_* phải lọc ở mọi tiến trình theo spec; Windows chưa chạy. |
| A13 | Các trần có đơn vị và witness riêng; per-walk không được gộp, memo phải đếm OID một lần kể cả expected type khác. G0 biên >8 MiB nhất quán. Profile đúng, nhưng clock seam không tự chứng minh timeout pipe thực/RSS/Windows; cần audit code thực thi. |
| A14 | Đổi/xóa ref thật sau đọc đầu tạo giá trị khác/vắng; bảng cho G9 unknown, khác lỗi caller ban đầu. Exact-name phải lọc tên ref, không dựa duy nhất số dòng từ prefix. |
| A15 | Hai đường write set và ≤750 được giữ; số ~710 vẫn là ước. Không lấy diff nhánh metadata hoặc prototype của reviewer làm số dòng thi công. |
| A16 | Required theo ADR-0060 M3. Spec gọi cả hai nhóm + mutant suite; phải giữ test ID/kết quả nền/ứng viên như M3, không chỉ tổng. Windows local và CI **not_run** trong review đặc tả. |
| A17 | Full mutant audit Ubuntu hoặc owner waiver đúng scope vẫn cần vì diff tương lai chạm `.claude/dev/**`; **not_run**, không suy từ suite JSON. |
| A18 | Prototype ghép giữ logic JSON thật và bản chép sổ. Child dương rc 0; ImportError/SyntaxError/vắng module đều rc 1 đúng tệp và không tổng; mutant caller nuốt import rc 0 bị `TinHieuChotCa(g_dong_tong_e2e)` bắt. Guard N=0/M>0 và M=0/N>0 phân biệt riêng. Số 157/163 của smoke prototype không phải số suite C1a1b. |
| A19 | `git diff --check BASE HEAD -- <r4.md>` rc 0. Ruff hai tệp ứng viên, doctrine/adr-song và toàn bộ gate thi công chưa nghiệm thu vì chưa có ứng viên code; không gọi chưa chạy là passed. |
| A20 | Bảng nghĩa vụ luật×E và disposition đúng hướng, nhưng miền `E_hong` thiếu điều kiện nguồn nên bảng có đủ ID vẫn có thể bỏ lọt F11. Tree của commit là blob tác động luật cần tree, không tự làm G4/G5 unknown chỉ vì chúng so tree OID. |
| A21 | Các ca số học/readback/zero/exhaustion đã đo bằng packet_loop thật; **thiếu ca chứng minh nguồn U_max**, F10. Lệnh init để thực hiện ca còn F12. |

**§2.1–§2.6:** `json=null iff G0 do`, K1/K2 mới chặn Git, K3/K4/K5 vẫn chẩn đoán, `ok` iff và rc 12/13 không có xung đột mới. “G0 trước mọi thứ” được đọc sau preflight tham số/N6 đã được §2.5 quy định trước mọi luật. G6 không đọc leaf, G7/G8 so OID trước; đã quét mode/type/missing/hash/sha256 và độc lập target/non-target. Ngoài F11 không thấy biểu hiện phân loại mới. Trần tổng bytes/time có thể ảnh hưởng nhiều luật cần đọc thêm; không coi luật đã có đủ chứng cứ là tự đỏ theo luật khác.

**§3/§5/§6:** phương án B dùng suite đã đăng ký là khả thi. Không mở rộng sang producer, registry, C1a2/C1b/T2/Q17, #656/#564/#499 hoặc #1160. N1–N8 đều có chỗ chiếu; N4 được thay bằng reader băm/parse và phân biệt vắng entry với thiếu object. N6 ràng buộc ref hai lần; nguồn API của tham số vẫn là hợp đồng caller, N7 không được nâng thành provenance/land authority.

**§8/§11 và authority:** ba dòng opt-in có đủ phép đo 0/128/0 trên snapshot; không có opt-in ADR-0052 cạnh tranh. ADR-0055 giữ cách đếm của ADR-0052, kể cả timeout/output sai schema/connector; ADR-0043/0048 giữ trục vòng/attempt riêng và trần chạm trước thắng. Trần lời gọi 16 không tự nâng trần vòng hoặc miễn Rescue. Q-NT là ngoại lệ allowance có đơn vị riêng, không là reservation/quota; những đại lượng chưa đo phải giữ unknown. Ngoài F10/F12, §11.2 đã khai trung thực replay Rescue chưa đo; `record-rescue revision` không mở state. Các chỉ thị human audit/2 lượt cũ đã được đánh dấu lịch sử cho pha spec; audit exact head trước merge là yêu cầu khác, không tự bị verdict này miễn.

## Đo lại các con số và hồ sơ

Lệnh chính: `PYTHONDONTWRITEBYTECODE=1 python -B probe_metrics.py`, **rc 0**, [metrics](evidence/metrics-r4.txt), [suite nền](evidence/json-baseline-r4.txt). Các git argv, rc, stdout/stderr được ghi trong log.

| Đại lượng | Đo lại | Nhận định |
|---|---|---|
| S2 first-parent MOC^..base | **411** commit, gồm MOC | Khớp. Reader dừng trước đọc MOC: **410 / 531.751 byte**. |
| S3 toàn bộ tổ tiên base | **5.444 / 8.480.418 byte** | Khớp; thời gian lần chạy được ghi ở log, chỉ Linux/bộ đệm máy này. |
| S4 first-parent / ngoài first-parent / log checker / giao | **1.084 / 4.360 / 64 / 64** | Khớp. Không dùng số cũ 1.795/37. |
| S5 diff producer MOC→base | **2 tệp, +650/−93** | Workflow +1/−1; checker +649/−92. |
| S6 JSON suite | **156/156, 162/162, equivalent 9, unresolved 0, rc 0** | Chạy trên bytes base đã chép vào scratch. |
| §2.6 trần 50.000 so lịch sử | **9,184423 lần**; ngoại suy **77.887.747,979 byte** | Ước theo 5.444 commit, không phải phép đo RSS hoặc H ngoài master. |
| §3 suite cũ | **535 dòng** | Khớp; số dòng code tương lai 710 chưa đo. |
| §11.5 drift 889334fb→08bcb51f | **1 tệp, +698/−92** | Đúng `.githooks/eol_policy_test.py`; tập phụ thuộc kiểm tra không có delta, kể cả base→reviewed SHA. |
| ADR-0055/0053/0060 opt-in | Mỗi bộ **rc 0/128/0** | OID chứa ADR, cha đầu chưa chứa, thuộc first-parent origin/master; không khẳng định đã fetch live. |
| Ref snapshot mirror | **780 branch refs + origin/HEAD** | 776 của §1/§3 là số lịch sử; không coi là lỗi vì đã ghi thời điểm và yêu cầu đo lại trước lease. |
| Hash r2/r3, verdict r1–r3, model/effort lịch sử | Khớp các băm rút gọn và trạng thái được spec trích | [final-r4.txt](evidence/final-r4.txt) ghi băm đầy đủ và tóm tắt metadata. Metadata hoàn tất lượt trước không chứng minh model phục vụ lượt này. |

S7 receipt thật S≠C, S8 Windows/WSL, profile lạnh, quota/reservation, holder live và nguồn GitHub Q-NT **không đo mới**. Authority cho lượt này lấy từ chỉ thị người dùng; không giả lập readback GitHub. Số đo offline không thay kiểm lease/freshness trước thi công.

## Lệnh, rc và kiểm tra cuối

Tất cả script ở sandbox, chạy với `PYTHONDONTWRITEBYTECODE=1 python -B`. [Manifest script](evidence/probe-manifest.sha256) cho phép đối chiếu đúng bytes dùng đo; chạy lại script tạo state/clone cần thư mục scratch mới vì chúng không tự xóa state cũ.

| Script | rc cuối | Bằng chứng |
|---|---:|---|
| `probe_metrics.py` | 0 | [metrics](evidence/metrics-r4.txt), [JSON nền](evidence/json-baseline-r4.txt); `do_profile.py` được chép từ kho trước khi chạy. |
| `probe_budget.py` | 0 | [A21, recovery, zero, default, exhaustion, Rescue](evidence/budget-r4.txt). |
| `probe_phase.py` | 0 | [Allowance spec 4 có tính lượt đã dùng](evidence/phase-r4.txt). |
| `probe_graph.py` | 0 | [Graph, producer, F6, F11, N6, replace](evidence/graph-r4.txt), [OID](evidence/graph-ids-r4.json). |
| `probe_acceptance.py` | 0 | [ABI, JSON, registry, A18](evidence/acceptance-r4.txt). |
| `probe_commands.py` | 0 | [Lệnh sai và đối chứng sửa F12](evidence/commands-r4.txt). |
| `probe_final.py` | 0 | [HEAD/tree/hash, git sạch, hash lịch sử và evidence](evidence/final-r4.txt). |

Một lượt graph probe đầu rc 1 do assertion của reviewer chờ từ `emptyName`; Git 2.43.0 thực in `empty filename in tree entry`. Đã sửa oracle khớp output thật và chạy lại; không lấy lỗi assertion đó làm finding. Các rc âm của lệnh con trong ca phản chứng được giữ riêng, không làm tròn thành rc 0 của sản phẩm.

Môi trường: Linux 6.18.44, Python 3.13.18, Git 2.43.0. Kiểm cuối: HEAD/tree/spec hash giữ nguyên; tracked, staged, untracked và ignored đều không có delta quan sát được. Không tuyên bố có manifest nội dung toàn cây đầu/cuối hoặc chứng minh lịch sử mọi write. Chưa có mã C1a1b để nghiệm thu Windows/fullCI; tất cả gate đó giữ **not_run**.

**Kết luận:** `changes_requested`; cần sửa F10, F11, F12 trước khi đạt điều kiện một lượt 0/0/0. Không sửa kho, không tự đóng băng spec, cấp lease, approve merge hay land.

TONG: P1=0 P2=2 P3=1
