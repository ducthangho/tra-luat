reviewed_sha: 735a0ef8480f62b9a5f003135ee5fcbf4bd0bd54
spec_sha256: 04fa50683c44f3db093ab2396ebef7e0a12b88740eb35745da39c8016e9d108d
model/effort (tự khai): Codex, nền GPT-6 theo chỉ thị phiên; model cụ thể và effort phục vụ KHONG_DO_DUOC từ giao diện phiên này, không tự xác nhận gpt-6-astra/xhigh.
provider: openai_codex
execution_surface: agent qua API có shell trong môi trường quản lý; không đo được tên launcher bên ngoài
transport: machine, tool calls trực tiếp
verdict: changes_requested

**Chưa đủ điều kiện đóng băng bằng model review.** Hai lớp thuộc điều kiện dừng Q-R vẫn còn biểu hiện. Chuyển packet sang phương án (B), human audit của chủ kho; không mở vòng vá/model review tiếp trong phiên soạn này. Việc xác minh và ghi bằng chứng của reviewer vẫn được hoàn tất theo chỉ thị.

Đối tượng là **đặc tả r2**, revision 2 / generation 1 / sensitive, không phải implementation C1a1b. HEAD đúng chỉ thị; tree `55a6098d313530f8a4d9792083334d373d8f3118`; `origin/master` của mirror là `08bcb51fbed359eaeeca41bc3a0559fe308c0aa9`; base đo `889334fb87c25136a13c6776a40a25b401820e04`. Mirror không shallow và status ban đầu rỗng. Chỉ ghi sandbox; cây review chỉ đọc.

Phạm vi: xác minh F1–F5; quét theo lớp phần r2 thay đổi, tính phân biệt của các đột biến, đo lại S4. Không chạy model bổ sung, không sửa đặc tả, không cấp quyền thi công/merge.

Kết quả đã đo: S4 = **4.360 / 64** trên base (5.444 tổ tiên, 1.084 first-parent). A7(i) đi trọn **675 commit**, không gặp MOC ⇒ `do`; A7(ii) cùng chuỗi nhưng thiếu một commit mới trong sandbox ⇒ `khong_do_duoc`. Ba tree S/C/H khác nhau; đột biến G4/G5 đổi toán hạng cho `do → qua` đúng ca đích. Producer qua symlink nội bộ chạy rc 0, JSON receipt hoàn chỉnh K1–K5 đều `qua`.

### Xác minh từng finding F1–F5

| Finding lượt 1 | Kết luận | Phép đo/lập luận trên r2 |
|---|---|---|
| F1 — `dat-lai-ngan-sach-khi-doi-truc` | **ĐÃ VÁ THẬT** ở tầng hợp đồng | §0/§8/§9 nay chỉ có một trục, tính cả output bị cắt và connector. Probe bộ đếm thật với **U giả định chính xác = 6**, init limit 4: bốn lần ghi rc 0, lần thứ năm rc 3, state blocked, tổng hiệu dụng 10. Đây là offset hợp lệ, không phải xóa lịch sử. Chưa đo được U thực tế chính xác; không suy “còn 4 lượt” từ `U ≥ 6`. Chi tiết ngân sách bên dưới. |
| F2 — `predicate-consumer-khong-khop-producer` | **ĐÃ VÁ THẬT** | G7/G8 nhận `120000`, so OID entry, không theo đích; khai rõ giới hạn. Chạy lại producer qua symlink nội bộ: rc 0, `TAP_THU_HOI_RONG`; workflow rev-parse cho OID symlink `203e9c185dec2f21482a7f1138284d2bcf531bab`; K1–K5 đều qua. Chỗ bác gitlink/thư mục nay được khai là chính sách chặt hơn, không còn suy sai “Python chạy ⇒ regular file”. Không chứng minh GitHub nạp YAML symlink. |
| F3 — `dot-bien-tuong-duong-hoac-thieu` | **VÁ MỘT PHẦN** | A9 đã có ba tree khác nhau và đúng T/tree_S đích; A4/A5 đã có iff, bool, byte stdout và rc. A18 đã sửa đúng tầng quan sát thành entrypoint, nhưng setup con thiếu dependency của nhóm JSON có thể làm caller đúng và mutant cùng qua oracle; F7. Còn phải chỉ định vị trí mutant caller/fixture assertion trong suite, ngoài module Git nêu ở §4. |
| F4 — `phan-loai-vang-va-khong-do-duoc` | **ĐÃ VÁ THẬT đối với biểu hiện G1 của F4** | G1 đi hết chuỗi không MOC nay nhất quán `do`; cặp A7 có đủ bytes/thiếu commit cho `do/khong_do_duoc`, hai mutant mới đổi màu đúng ca. **Không đồng nghĩa đóng lớp**: giao OID lệch × object vắng/hỏng trong G7/G8 tái phát mâu thuẫn ở F6. |
| F5 — `so-do-ke-thua-chua-do-lai` | **ĐÃ VÁ THẬT** | Đo lại đúng base: 5.444 − 1.084 = **4.360**, giao tập `git log --format=%H <base> -- ops/lease_publish.py` = **64**. §1 S4 đã ghi đúng; §6 bỏ khoản chưa đo cũ. |

### Hai lớp quyết định Review Rescue

| Lớp | Kết quả lượt 2/2 | Biểu hiện còn mở / hệ quả |
|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | **CHƯA ĐÓNG** | G1 cũ đã đóng; F6 ở G7 và G8 là biểu hiện mới cùng lớp. Không đặt lại lịch sử bốn lần trước. |
| `dot-bien-tuong-duong-hoac-thieu` | **CHƯA ĐÓNG** | A9 và ABI cũ đã đóng; F7 ở A18: lỗi setup có thể che mutant caller. Không tính oracle hợp lý trong mô hình tối giản là bằng chứng setup thật đã đủ. |

Tỷ lệ đóng hai lớp Q-R: **0/2**. Việc sửa được các biểu hiện cũ không đủ để ghi hai lớp đã đóng. Lớp kế thừa `mo-rong-module-pha-hop-dong-json-thuan` vẫn đóng ở tầng đặc tả: write set tách module, A1/A3 giữ byte/kết quả cũ; blob JSON nền/HEAD cùng `3490ea0ee40081c0eba2d121f5b19a67a021a54b`, suite nền chạy lại **156/156 ca, 162/162 đột biến, 9 equivalent, 0 unresolved**. Chưa có module Git sản phẩm để nghiệm thu runtime.

### F6 — P2 — `phan-loai-vang-va-khong-do-duoc`

**Vị trí:** `ops/specs/wp1179-c1a1b-r2.md:185`, `:197`, `:250`, `:253`, `:261`, `:383`.

Bảng đóng vẫn không cho một đáp án duy nhất khi **entry có mode nhận, OID khác receipt, và object blob vắng/hỏng/sai kiểu**. §2.3 bắt G7/G8 đọc blob khi mode thuộc tập nhận (không có điều kiện OID khớp), rồi bất kỳ `E` trên object cần đọc thắng và trả `khong_do_duoc`. Bảng G7 lại có dòng OID khác ⇒ `do`, trong khi dòng `khong_do_duoc` chỉ áp khi **OID khớp**. G8 kế thừa cả năm dòng ấy. Hai đường triển khai (đọc trước hoặc so OID trước) khác trạng thái cùng đầu vào; nếu mọi luật còn lại qua thì khác cả rc 13/12. Đây là mâu thuẫn cụ thể, không phải đòi receipt xấu phải được chấp nhận; cả hai rc đều chặn land.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_classification_r2.py`, rc 0; [log](evidence/classification-r2.txt). Dựng hai tree thật trong clone sandbox, entry `100644` trỏ `1234567890abcdef1234567890abcdef12345678`, receipt khai OID khác. Tree đọc/băm lại được; `cat-file --batch` rc 0, header đúng `<oid> missing`. Chiếu nguyên hai bảng: §2.3 = `khong_do_duoc`, §2.4 = `do`, cả G7 lẫn G8. Đây là prototype hợp đồng, chưa có implementation C1a1b để chạy.

**Đề xuất cho human audit:** chọn và ghi thứ tự ưu tiên duy nhất ngay trong bảng đóng. Nếu OID lệch là đủ bác thì cột “đọc” G7/G8 phải chỉ yêu cầu blob sau khi OID khớp; nếu sự kiện object thắng thì bảng riêng phải nhận mọi tổ hợp OID khớp/lệch × object tốt/vắng/hỏng/sai kiểu. Khóa ca cho cả G7/G8, kiểm trạng thái và rc. Rủi ro khi sửa: đọc quá sớm tiêu ngân sách và đổi rc; short-circuit quá rộng có thể bỏ đọc blob khi OID khớp. Không tự vá r2 trong lượt này.

### F7 — P2 — `dot-bien-tuong-duong-hoac-thieu`

**Vị trí:** r2 §4 dòng 356–360, A2 dòng 365, A9 dòng 372, **A18 dòng 381**; dependency đã có ở `.claude/dev/doc_receipt_thu_hoi_test.py:257` (`ca_dang_ky`) và `:510` (entrypoint chạy nhóm JSON).

A18 chép “suite + hai module” rồi chấp nhận mọi `rc ≠ 0` kèm stdout không khớp regex. Nhóm JSON bắt buộc giữ nguyên lại nạp `GOC / ci_dang_ky_test.py`; tệp ấy không nằm trong setup đã nêu. Do vậy child có thể chết vì **FileNotFoundError của sổ**, trước khi tới import Git. Đột biến caller nuốt ImportError vẫn cho cùng rc/stdout: **ca đích không đổi màu**. Đọc regex từ sổ ở tiến trình cha không tự cung cấp dependency cho tiến trình con. Cùng cơ chế che có thể xảy ra nếu child thiếu gốc kho/MOC; không cần suy diễn hoặc dựng payload thoát thư mục để đo lỗi này.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_a18_setup_r2.py`, rc **0**, [log](evidence/a18-setup-r2.txt). Prototype giữ nguyên toàn bộ ca/đột biến JSON của suite thật, chỉ bọc entrypoint để gộp Git; module Git giả tiêm `ImportError`. Với đúng ba tệp của A18, caller đúng **rc 1 / không dòng tổng / oracle A18 qua**; caller nuốt import cũng **rc 1 / không dòng tổng / oracle A18 qua**, stderr cùng `FileNotFoundError: .../ci_dang_ky_test.py`. Thêm bản chép sổ: caller đúng rc 1 bởi ImportError đích; mutant rc 0 và dòng `156/156 … 162/162` được regex **đọc từ sổ thật** nhận ⇒ A18 mới đổi màu. Probe không phải implementation C1a1b; nó chứng minh một lỗi setup được oracle hiện tại chấp nhận và một cách cô lập nguyên nhân bằng A/B.

**Quét cùng lớp trong harness:** §4 chỉ mô tả mutant trên bản sao `doc_receipt_thu_hoi_git.py`, nhưng mutant “caller nuốt lỗi import” của A18 nằm trong **suite**. E2E còn ghi đè/xóa module Git trước khi chạy, nên mutant chỉ đặt trong module ấy mất tác dụng. `probe_mutations_r2.py`, rc 0 ([log](evidence/mutations-r2.txt)): ba vế import/syntax/vắng cùng qua trên module gốc và module-mutant; mutate đúng caller trong suite mới làm vế ImportError đỏ. Mutant “bỏ assert ba tree khác nhau” của A9 cũng nằm trong hạ tầng suite. Đây là các vị trí cần khai trong harness, không được tính tín dụng từ mutant của module Git không tác động tới chúng.

**Đề xuất cho human audit:** khai đầy đủ dependency và gốc kho cho child (sổ chép nguyên byte, không sửa registry của kho); chạy **child dương trước** trên cùng setup, phải thấy cả hai nhóm và tổng đúng. Sau đó mới tiêm từng lỗi và đòi evidence lỗi đúng tại import Git, không cho lỗi setup khác thay thế. Cho phép mutant caller/hạ tầng trên bản sao suite, và bảo đảm chạy đúng assertion đích bằng `TinHieuChotCa`. Giữ child dương ngoài vòng đệ quy e2e. Rủi ro khi sửa: recursion tự gọi suite; vô tình tính lại số JSON hoặc dùng regex chép tay thay sổ thật.

### F8 — P2 — `oracle-trang-thai-g0-mau-thuan`

**Vị trí:** r2 §2.2 dòng 135–139, A6 dòng 369 (đối chiếu G0 dòng 214). A6 không sửa từ r1 nhưng mâu thuẫn trực tiếp với quy định G0 được r2 thêm để khóa ABI.

§2.2 nay ghi rõ G0 luôn `qua/do`, **không bao giờ `khong_chay`**; chỉ G1–G9 bị chặn bởi K1/K2 đỏ. A6 vẫn đòi K1 đỏ ⇒ **mọi G** `khong_chay`, và K2 “như trên”. Không có vector nào thỏa cả hai cho một receipt nhỏ nhưng JSON đỏ. Triển khai đúng guard kích thước sẽ bị oracle A6 bác; đổi G0 sang skip để qua A6 lại vi phạm ABI.

**Phép đo:** `probe_classification_r2.py`, rc 0, [log](evidence/classification-r2.txt): `raw=b'{}'`, 2 byte, `kiem_json` thật trả K1 `do`. Theo §2.2: G0 `qua`, G1–G9 `khong_chay`; theo A6: G0 `khong_chay`. Receipt đủ 38 khóa có T sai miền cũng đo được K1 `qua`, K2 `do`, kích thước dưới trần và cùng xung đột G0. Đây là lỗi acceptance, không phải phát hiện lỗi runtime chưa tồn tại; không cộng nó vào lớp E của F6.

**Đề xuất cho human audit:** sửa oracle A6 thành G0 `qua`, G1–G9 `khong_chay` cho cả K1/K2; G0 quá kích thước vẫn `do`, json null. Khóa riêng mutant đổi G0 thành `khong_chay` sau JSON đỏ. Rủi ro khi sửa: đổi thành “mọi G qua” hoặc mất kiểm G0 guard trước parser; kiểm cả hai ca JSON nhỏ đỏ và receipt vượt trần.

### Audit độ phân biệt của đột biến r2

“Đổi màu” dưới đây là phép đo đồ thị/byte thật hoặc mô hình oracle được ghi rõ; **không** phải báo cáo mutant suite C1a1b đã chạy. Mã C1a1b chưa tồn tại. Các mô hình không thay audit nghĩa vụ trên implementation sau này.

| Ca / đột biến | Đo hoặc lập luận phân biệt |
|---|---|
| A4: `ok=json.ok`; bỏ vế JSON (`ok=all(G qua)`) | Mô hình ma trận a–e dùng `kiem_json` thật: mutant thứ nhất bị ca b bác (`True` thay `False`); mutant thứ hai bị ca d bác. Bool→int cũng bị chốt kiểu bác. |
| A4: bỏ `sort_keys`; thêm `giay`; trạng thái `loi` | Serializer chạy subprocess thật: cả năm tổ hợp cho byte khác khi bỏ sort; outer/inner dict giữ thứ tự của kết quả JSON thật. Thêm khóa hoặc trạng thái ngoài tập bị phép so tập khóa/tập trạng thái bác trực tiếp. Không gán tín dụng “giết” cho biến thể serializer mà sort đã tương đương do canonical hóa trước đó; disposition cuối phải xét mã thật. |
| A5: đảo ưu tiên 12/13; bỏ chốt N6 đầu | Mô hình tổ hợp có cả do/unknown cho rc 12→13. Đọc ref thật đầu/đổi/xóa cho ba quan sát khác nhau; N6 ban đầu lệch phải chặn trước CLI JSON, khác với G9. Chưa có CLI C1a1b để đo toàn bộ từng tham số sai. |
| A7: all-parent, bỏ MOC bound, loại MOC | Đồ thị thật: ca E cho `do→qua` khi dùng mọi parent; ca P cho `do→qua` khi bỏ bound; C=MOC cho `qua→do` khi loại biên. |
| A7 mới: hết chuỗi→unknown, thiếu object→hết chuỗi | Cặp 675 commit đủ / xóa commit Q1 mới cho đúng `do/unknown`; mỗi mutant đảo đúng ca đích. Không xóa object trong mirror/alternates. |
| A9: so T với S; so tree_S với H | Ba tree S/C/H đôi một khác nhau; T=tree(S) và tree_S=tree(H) đều cho `do→qua`. Ca empty-tree là đối chứng `do/do`, r2 đã không dùng nó làm witness chính. |
| A9: bỏ assert ba tree | Chỉ phân biệt được nếu ca tự kiểm chủ động đưa fixture trùng tree vào guard; guard/mutant thuộc suite, cần khai ngoại lệ phạm vi mutator như F7. Chỉ chạy fixture dương đã khác tree thì xóa assert không đổi gì. |
| A11: dùng G6 cho G7; bác symlink; theo symlink; bỏ blob read; bỏ sha256 | Các witness tương ứng: gitlink OID khớp `do→qua`; symlink `qua→do`; entry symlink khác OID target `qua→do`; accepted blob vắng `unknown→qua`; sha256 lệch `do→qua`. OID symlink/mã target đo từ Git thật. Probe workflow symlink đọc đúng chuỗi `workflow-real.yml`, sha256 entry khác sha256 target; không suy GitHub thực thi YAML ấy. F6 chỉ phát sinh ở **giao** OID lệch × lỗi object, không phủ nhận các ca đơn này. |
| A13: vượt budget→do; gộp bộ đếm các walk | Mô hình bộ đếm: vượt → unknown/do khác; với limit 3, walk [3,1,4] cho [qua,qua,unknown], bộ đếm gộp cho [qua,unknown,unknown]. Cần kéo dài H trong fixture của ca per-walk để cô lập G3, và kiểm cả vectơ. Đây là chứng minh witness khả thi, chưa chạy walker sản phẩm. |
| A13: bỏ max_object_bytes; bỏ memo; G0 `>=` | Commit thật đo [260,212,212,213] byte: limit 211 tạo witness guard. Đọc lặp H: counter mẫu 213→426 nếu bỏ memo và đọc lại tính byte. G0 với JSON thật tại 8.388.607/8.388.608/8.388.609 cho `qua/qua/do`; dùng `>=` làm ca bằng trần đỏ. Trần total/wall riêng mới được mô tả ở r2; cleanup tiến trình treo và peak RSS chưa đo. |
| A18: caller nuốt import; bỏ N_git≥1 | Caller mutant đổi màu **khi setup đủ**, sống khi thiếu registry — F7. Ca thuần N_git=0 phải giữ M_git dương và các chốt khác hợp lệ để riêng việc bỏ N_git≥1 đổi màu; nếu cả N_git=M_git=0 thì chốt M_git vẫn che. Mệnh đề đầu A18 đã đòi hai điều kiện riêng; bảng nghĩa vụ phải thực hiện tách vế như §5.0, không gán witness từ một trường hợp 0/0 ghép. |
| A20: event→do; lan event cho mọi luật | Ở mức vector oracle, `(unknown,qua)` phân biệt được với `(do,qua)` và `(unknown,unknown)` cho cả bảy tên E. Không coi in một bảng vector là đã đo đủ mọi ô luật×E. Phải xác định luật thật cần object nào, và bắt cả tổ hợp predicate×E đang thiếu ở F6. Ca tree-of-commit là blob phải nhắm G6/G7/G8; G4/G5 chỉ đọc commit nên không được gán E của tree cho chúng. |

### Ngân sách và đối chiếu ADR/protocol

`probe_declarations.py` rc 0: ba dòng khai ADR-0055/0053/0060 đều có đúng một dòng hợp mẫu; mỗi OID có tệp ở L (rc 0), chưa có ở L^1 (rc 128), nằm trên first-parent `origin/master` của mirror (rc 0). Không có dòng khai ADR-0052. Trần opt-in 10 hợp lệ trong **snapshot**; không phải xác minh ref vừa fetch từ GitHub của phiên này.

§8 r2 không còn mặc định mở trục PR riêng. `--codex-review-calls-limit (10-U)` thực thi được với **U chính xác**, miễn tổng được đọc là U lịch sử + local_used, ghi cả hai ở lease. Log [call-budget-r2.txt](evidence/call-budget-r2.txt) chạy CLI `init`/`record-codex-call` thật trong state giả tại sandbox; không tạo lease hoặc lời gọi model. U=10 thì dừng; `init` không nhận limit 0, không được rơi về mặc định 2. U chỉ biết cận dưới thì phần còn lại **KHONG_DO_DUOC**, theo protocol §12; §9 sau lượt này mới chỉ chứng minh **U≥6**, không chứng minh còn đúng 4 lượt. Ví dụ U=6 trong r2 là điều kiện giả định, không được dùng làm số đo.

ADR-0055 chỉ nâng con số, giữ điều kiện cấp lượt sau lượt đầu của ADR-0052 (còn P0/P1, finding cắt ngang hoặc xác minh bản vá). Việc có limit dương không tự cấp lượt. Hai trục vòng/attempt giữ riêng; `U` không phải số formal validated rounds. Review Rescue Q-R của riêng packet chạm trước phần limit còn lại, nên **không được gọi thêm chỉ vì 10−U còn dương**. Không thấy r2 cấp quyền trái các điều này; không quy kết việc chưa reconciled U là một lần reset mới. Quota/reservation chưa đo; không tuyên bố thi công đã có đủ ngân sách.

Q-KT ≤2 tệp/≤750 dòng và Q-NS một trục được chỉ thị review hiện tại xác nhận; không yêu cầu chủ kho duyệt lại. Khối `nang_tran` kích thước không tăng trần lời gọi. Số ~710 chỉ là ước; chưa có diff implementation để nghiệm thu A15.

### Quét phần thêm/đổi và phạm vi bằng chứng

| Phần r2 | Kết quả review |
|---|---|
| §0.3, §7, §9, §10 | Quyết định Rescue và lịch sử được giữ, không reset; Q-R kích hoạt bởi F6/F7. Không đọc lời ghi trong spec thành receipt human audit đã có. Bảng §9 chưa có kết quả lượt này là đúng thời điểm commit. |
| §2.2 | Iff outer ok, bool, serialization, G0 và skip G1–G9 đã cụ thể. A6 xung đột G0 — F8. JSON K4 đỏ vẫn cho Git chạy để chẩn đoán, ma trận d phân biệt được. |
| §2.3 / §2.4 | F6. Các đường G6 leaf vắng, gitlink không có object, ancestor mode blob đều có cách phân biệt từ metadata đã băm. **Không** gọi ancestor mode blob là E_kieu_sai: có thể kết luận `do` từ mode mà không hỏi reader đọc nó như tree. Mode `40000` nhưng object thực là blob thì mới E_kieu_sai. G6 không đọc leaf; G7/G8 có đọc accepted leaf, không được đồng nhất hai predicate. |
| §2.6 / A13 | Các giới hạn đã tách, per-walk và memo rõ hơn; profile base tái lập. 60 giây/8 MiB/128 MiB vẫn là lựa chọn chính sách, không được suy “đã kiểm timeout/RSS trên Windows”. |
| §3 / A2 / A15 | Phương án B khả thi: `kiem()` sổ thật 29/29, thêm module Git vẫn 29/29, thêm test riêng báo lỗi 30/29. Holder là snapshot cũ, r2 đã đòi đo lại trước lease; phiên này không chứng nhận holder live. |
| A4/A5/A7/A9/A11 | Các witness cũ sai đã có sửa có tác dụng như bảng trên; F6 ở giao sự kiện và F7 ở harness vẫn còn. |
| A16/A17 | A16 đã có lệnh cụ thể, chạy đủ mutant của suite, không còn câu miễn Windows CI toàn kho. Phù hợp hướng M3; khi thi công phải lưu test ID/kết quả nền và ứng viên cùng máy/lệnh, không chỉ dòng tổng. Windows, full_mutant_audit và waiver **not_run/not_present** trong review đặc tả này; không tính là pass. |
| A18/A20 | A18 bị setup che lỗi như F7; A20 phủ luật×E là cải tiến nhưng chưa giải quyết giao predicate×E của F6. Nghĩa vụ disposition/unresolved=0 vẫn phải audit trên mã thật. |
| §6 / ngoài phạm vi | S4 không còn “chưa đo”; giữ đúng nợ receipt thật S≠C, cold cache, Windows/null-device, workflow symlink. Không kết luận T2/Q16/Q17 đạt, không chứng minh provenance run hoặc cấp quyền land. |

Các probe liên quan lượt 1 đã được chạy lại/viết lại trên r2: `probe_graph.py`, `probe_counts.py`, `probe_budget.py`, `probe_reader.py`, `probe_acceptance.py`, `probe_declarations.py`; ca ABI/phân loại/registry được thay bằng probe r2 phù hợp hợp đồng mới. Script gốc có trong sandbox lượt 1; chỉ đọc chúng, bản đã điều chỉnh nằm trong sandbox lượt 2. Những probe dùng chung graph chạy nối tiếp, không ghi đồng thời. Không chạy lại holder live/full registry audit không thay đổi vì không cần cho các kết luận mới; không ghi chúng là pass mới.

| Phép đo | Lệnh / rc thật | Bằng chứng dương |
|---|---|---|
| S4 / byte nền | `PYTHONDONTWRITEBYTECODE=1 python -B probe_counts.py` / 0 | [counts.txt](evidence/counts.txt): 5444/1084/4360/64; module/suite/sổ không khác base. Danh sách numstat neo base có cả master merge; không dùng làm diff implementation. |
| Profile | `python -B ../cay-kho/ops/specs/wp1179-c1a1b-r1-do/do_profile.py ../cay-kho <base> <MOC>` với PYTHONDONTWRITEBYTECODE=1 / 0 | [profile-r2.txt](evidence/profile-r2.txt): 410 commit/531.751 byte/0,029 s tới trước đọc MOC; toàn tổ tiên 5.444/8.480.418/0,252 s. |
| G0 / budget | `python -B probe_budget.py` với env trên / 0 | [budget.txt](evidence/budget.txt): guard biên đúng; trung bình 1.557,754960 byte, 50.000 commit ngoại suy 77.887.747,979 byte, max commit 8.477. |
| Producer, graph, symlink | `python -B probe_graph.py`; `python -B probe_symlink_workflow_r2.py` / mỗi lệnh 0 | [graph.txt](evidence/graph.txt), [workflow-symlink-r2.txt](evidence/workflow-symlink-r2.txt), OID ở [graph-ids.json](evidence/graph-ids.json). Các process producer/Git ghi rc thật trong log. |
| Reader / ancestry / ref | `python -B probe_reader.py`; `python -B probe_acceptance.py` / mỗi lệnh 0 | [reader.txt](evidence/reader.txt): hash lệch được quan sát dù cat-file rc 0; lọc GIT_OBJECT_DIRECTORY tránh missing giả; [acceptance.txt](evidence/acceptance.txt): ancestry đảo 1→0, ref đổi/xóa phân biệt được. |
| JSON nền | Trong clone sandbox tại base: `PYTHONDONTWRITEBYTECODE=1 python -B .claude/dev/doc_receipt_thu_hoi_test.py` / 0 | [json-baseline-r2.txt](evidence/json-baseline-r2.txt): 156/156, 162/162, equivalent 9, unresolved 0. |
| Phân loại / ABI / harness | `probe_classification_r2.py`, `probe_mutations_r2.py`, `probe_a18_setup_r2.py` bằng python -B/env trên / mỗi bản cuối 0 | Log được dẫn ở F6–F8. Hai lần phát triển đầu của `probe_mutations_r2.py` rc 1 do reviewer đặt sai kỳ vọng FileNotFoundError và thiếu import hashlib; đã sửa probe, chạy lại rc 0. **Không** tính hai lỗi probe ấy là finding hay mutant killed của sản phẩm. |
| Sổ / ngân sách / khai ADR | `probe_registry_r2.py`, `probe_call_budget_r2.py`, `probe_declarations.py` / mỗi script 0 | [registry-r2.txt](evidence/registry-r2.txt), [call-budget-r2.txt](evidence/call-budget-r2.txt), [declarations.txt](evidence/declarations.txt). Lệnh con chặn đúng có rc 3/128 như nêu, không bị ghi thành rc 0. |
| Identity cuối | `python -B probe_final_r2.py` với env trên / 0 | [final-r2.txt](evidence/final-r2.txt): HEAD/hash khớp, status kể cả ignored rỗng, cây không shallow; năm tệp runtime liên quan không đổi so base. Diff-check riêng đặc tả r2 rc 0. |

`git diff --check origin/master HEAD` cho **toàn gói hiện vật** rc **2** vì whitespace trong log lượt 1 chép vào (`basic.txt`, `counts.txt`, `holders.txt`); đã lưu nguyên output ở final-r2.txt. Không khai toàn gói xanh, không sửa log bất biến; các dòng này không nằm trong phần r2 được yêu cầu review và không được nâng thành finding nội dung mới. A19 gate implementation vẫn chưa nghiệm thu.

Môi trường: Linux, Python/Git cụ thể ghi ở final-r2.txt. Không gọi mạng, model phụ, connector, CI, push, merge hay API authority. Không tự soạn nội dung thoát thư mục; symlink thử nghiệm chỉ trỏ tên tệp nội bộ cùng thư mục. Các kết quả Git là snapshot được giao, không chứng nhận trạng thái GitHub hiện hành. Model/effort phục vụ chỉ khai tới phần quan sát được ở header; metadata launcher bên ngoài cần receipt riêng nếu dùng để định danh review.

**Kết luận:** `changes_requested`, **3 P2 mở** (F6–F8), không P1/P3 mới. Q-R áp ngay vì F6/F7 thuộc hai lớp được chỉ định: dừng vòng vá đặc tả bằng model, chuyển human audit chủ kho. Human audit là bước được yêu cầu tiếp theo, **chưa được thực hiện** bởi verdict này; verdict không tự tạo `cross_approved`, `human_audited`, freeze hay quyền land.

TONG: P1=0 P2=3 P3=0
