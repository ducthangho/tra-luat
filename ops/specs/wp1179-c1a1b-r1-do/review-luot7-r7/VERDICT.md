# Review độc lập đặc tả wp1179 C1a1b r7

- reviewed_sha: `4f3738ae720fe311a222439307a91307d798d5f3`
- spec_sha256: `9f9c50b93070838cd3fb6c76a7a10969862d79ee0bc17d1183123345daab56c2`
- provider: `openai_codex`; execution_surface: Codex với shell cục bộ; transport: công cụ trực tiếp.
- model/effort tự khai: Codex (GPT-6 theo chỉ thị môi trường); tên model cụ thể và effort không được runtime công cụ công bố, không tự suy từ yêu cầu `gpt-6-astra/xhigh` của spec.
- verdict: **`changes_requested`**.
- reviewed_tree: `d3825f0d0fe465d5c365b55dab39304f367b02ca`.
- baseline số đo: `889334fb87c25136a13c6776a40a25b401820e04`.

## Preflight

Đọc `prompt.snapshot`, `AGENTS.md`, từ vựng CONTEXT, các phần protocol/CLAUDE liên quan, kế hoạch đa provider, ADR-0043/0052/0053/0055/0060, nghĩa vụ N1–N8 và hợp đồng disposition §5.0 của C1a1a, toàn bộ r7, verdict/evidence r6 và các đoạn lịch sử r1–r5 liên quan. Không đọc draft4.

`git rev-parse HEAD` rc 0 khớp reviewed_sha; `git rev-parse --is-shallow-repository` rc 0 → `false`; `sha256sum ops/specs/wp1179-c1a1b-r7.md` rc 0 khớp spec_sha256. Spec có 877 dòng. Cây review được giữ chỉ đọc; các script và hiện vật bền của reviewer nằm trong sandbox. Python chạy `-B` và `PYTHONDONTWRITEBYTECODE=1`; suite nền tự dùng thư mục tạm hệ thống rồi dọn. Không sửa spec, implementation, ref hay state trong cây review; không gọi model con, mạng, LIVE, push hay merge.

Đây là **review đặc tả**, không phải nghiệm thu implementation tương lai. Prototype chứng minh/phản chứng các quan hệ và oracle được nêu; không thay CLI Git sản phẩm, gate Windows hoặc CI. Model/effort chi tiết, bề mặt CLI/Desktop và provenance launcher phải do biên nhận runtime ngoài phiên xác minh; không tự cấp `cross_approved` hay quyền land.

## F16

Nguồn F16: verdict r6 trên `b439048e4ffe15eed0202b0a91b82be2750041af`, lớp `phan-loai-vang-va-khong-do-duoc`.

| Phần F16 | Kết luận độc lập | Bằng chứng |
|---|---|---|
| Tập đọc phải theo `(kiểu, OID)` | **Vá thật ở biểu hiện trực tiếp** | Oracle độc lập tự đọc `cat-file` trên đồ thị thật; đủ 10 hàng bảng §4 khớp. Subtree riêng và guard âm phát hiện alias đúng. |
| Reader chết là tài nguyên chung | **Vá thật ở biểu hiện trực tiếp** | A12(e): G1–G8 unknown, G9 qua; (f): G1–G5 qua, G6–G8 unknown; (g): chỉ G7 unknown; (h): G7/G8 unknown. |
| Ca alias có chủ ý | **Vá sinh lỗi setup** | Literal r7 kế thừa ops từ MOC/alternate, không xoá được bằng xoá loose cục bộ; F18(c). Đối chứng fixture sửa cho OID mới xác nhận G6/G7 cùng unknown. |
| Tài nguyên chung + memo + deadline | **Vá sinh mâu thuẫn** | F17: §2.3 giữ qua cho luật đủ memo; §2.6/A13 đòi unknown. |
| Ca/đột biến khoá bản vá | **Chưa đóng** | A12(f) và A13 reset tổng không đổi màu ca đích; F18(a,b). |

Disposition chung của **F16: VÁ SINH LỖI MỚI**, không ghi lớp đã đóng. 14 đường ở §0.8 **chưa đủ**; bảng rà từng đường và các đường bị sót nằm dưới.

## Bảng lớp

| Slug lớp ổn định | Lịch sử | Trạng thái lượt này | Cách đóng / phạm vi đo |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | draft0–2, F4/F6/F11/F13/F16 | **Mở: F17 P2** | Một bảng chuyển trạng thái tài nguyên, tách deadline khỏi lỗi reader/byte; đối chứng cùng graph, cùng memo. |
| `dot-bien-tuong-duong-hoac-thieu` | F3/F7/F14; r6 đóng biểu hiện F14 | **Tái mở: F18 P2, ba biểu hiện** | Kiểm tiền đề fixture và khả năng phân biệt trước khi nhận witness; đã đo cả phản chứng lẫn ca sửa có phân biệt. |
| `mo-rong-module-pha-hop-dong-json-thuan` | draft0–2; ABI r1 | Không tái mở | Blob JSON giữ nguyên, suite nền 156/156 và 162/162; A1–A4 bảo toàn ranh giới module. |
| `predicate-consumer-khong-khop-producer` | F2 | Không tái mở | Đối chiếu producer, đo G7/G8 năm mode và giao OID lệch × blob thiếu. Giới hạn symlink được khai. |
| `oracle-trang-thai-g0-mau-thuan` | F8 | Không tái mở | JSON thật K1/K2/K4 và mô hình G0/rc: G0 luôn qua/đỏ; chỉ G1–G9 không chạy. |
| `huong-dan-cli-khong-khop-parser` | F12/F15 | Không tái mở | Init/status thật; cặp thiếu mission/limit 0; rescue ID/URL trong state thử nghiệm đúng trạng thái: 2/0. |
| `dat-lai-ngan-sach-khi-doi-truc` | F1/F9/F10 | Không tái mở | `cap=allowance=3`, `U_max=unknown`; state đọc lại limit 3, ghi call 1–3 được, thứ 4 rc 3. |
| `so-do-ke-thua-chua-do-lai` | F5 | Không tái mở | S2–S6, blob, drift và ba mỏ neo ADR được đo lại ở exact baseline. |
| `nguon-duoc-tin-ma-chua-xac-minh` | C1a1a §6 | Không thấy biểu hiện mới đủ căn cứ | Băm object, phân biệt entry/bytes vắng, hai lần đọc ref, giới hạn nguồn API/provenance được giữ. |

Tập lớp mở ở r6 có một lớp; r7 chưa đóng lớp ấy: **0/1 = 0%**. Lớp đột biến tái mở được báo riêng, không đưa vào tử số. **Hai finding / hai lớp mở / bốn biểu hiện**, không tạo slug mới để xoá lịch sử. Quyền thêm lượt 7–8 không đồng nghĩa approval; lượt này chưa đạt điều kiện 0/0/0.

## Finding mới

### F17 — P2 — `phan-loai-vang-va-khong-do-duoc`

**Vị trí:** `ops/specs/wp1179-c1a1b-r7.md` §2.3 dòng 389–392, đối chiếu §2.6 dòng 503–507, §4 dòng 598–602 và A13 dòng 649.

**Lỗi:** quy tắc chung mới vẫn đồng nhất phạm vi của deadline với reader chết/tổng byte. §2.3 nêu rõ ba loại cùng ảnh hưởng luật cần object **chưa memo**, rồi khẳng định luật có đủ memo **giữ kết quả**. §2.6 và A13 lại buộc **mọi luật chưa hoàn tất** ra `khong_do_duoc` khi hết deadline, kể cả đủ memo. Đây là hai kết quả khác nhau cho cùng đầu vào, không phải thiếu ca corner case của implementation.

**Phản chứng:** trên fixture dương thật, tiêm đồng hồ hết hạn ngay sau G3. G1 đã memo A; G3 đã memo H1. G4 chỉ cần H1, G5 chỉ cần A. Theo §2.3 cả hai vẫn `qua`; theo A13 cả hai `khong_do_duoc`. §4 đã viết ngoại lệ deadline nhưng không xoá luật chung trái nó trong §2.3.

```text
PYTHONDONTWRITEBYTECODE=1 python -B probes.py > evidence/graph-probe.log 2>&1
rc=0
A13_deadline:          G1–G3=qua; G4–G9=khong_do_duoc
A13_deadline_mut_memo: G4=qua, G5=qua (theo câu giữ memo ở §2.3)
```

[Mã probe](probes.py), [log](evidence/graph-probe.log), [trace](evidence/graph-runs.json). Prototype dùng cờ clock seam xác định ở biên luật, không ngủ 60 giây; không tuyên bố đã đo timeout I/O thực.

**Đề xuất:** sửa ngay §2.3, §2.6 và oracle §4 thành một bảng phạm vi: (i) reader chết/tổng byte chỉ chặn đọc mới, memo vẫn dùng được; (ii) deadline chặn mọi luật chưa hoàn tất, kể cả G9 và luật đủ memo; (iii) kết quả đã hoàn tất bất biến. Giữ ca deadline sau G3 và thêm ca reader chết **cùng thời điểm** để chứng minh G4/G5 phải khác nhau giữa hai loại sự kiện.

**Ca khoá đã đo:** reader chết sau G3 ⇒ G4/G5 `qua`; deadline sau G3 ⇒ G4/G5 unknown. **Rủi ro khi vá:** dùng một nhánh “mọi sự kiện chung làm mọi luật unknown” sẽ làm hỏng memo/G9 của reader; ngược lại đặt deadline sau lookup memo làm A13 sai. Không đổi F6, write set hay phạm vi C1a1b.

### F18 — P2 — `dot-bien-tuong-duong-hoac-thieu`

**Vị trí:** A12 dòng 648 (cột đột biến cho f), A13 dòng 649 (ca tổng byte và mutant reset theo luật), §4 dòng 560–565/628–633 và A23 dòng 660 (fixture alias). Hợp đồng disposition áp dụng ở dòng 579–588 không biến mutant sống trên một ca thành tương đương toàn miền.

**Nguyên nhân chung:** chưa chứng minh tiền đề của ca và khả năng phân biệt mutant trước khi dùng ca làm chốt. Ba biểu hiện dưới đây cùng lớp F3/F7/F14; cần ba cách sửa fixture vì tài nguyên gây che khác nhau.

**(a) A12(f) không đo được việc giữ memo.** Reader bị giết sau khi G5 **đã hoàn tất**. G1–G5 nằm trong dict kết quả; xoá memo không đánh giá lại chúng. G6–G8 đều cần tree chưa đọc ở cả bản đúng lẫn mutant. G9 dùng tiến trình riêng. Vì vậy không luật nào đổi màu. Xoá cache cũng không xoá số đo luỹ kế: cả hai vẫn 896 byte/4 object. Lời trong cột mutant “G1–G5 ra unknown” trái quy tắc giữ luật hoàn tất.

```text
A12f                  : G0–G5 qua; G6–G8 unknown; G9 qua; 896 byte, 4 object
A12f_mut_clear_memo   : cùng vector, cùng 896 byte, cùng 4 object
```

**(b) A13 không bảo đảm reset tổng byte đổi màu ca đích.** Fixture tuân thủ r7 với message commit ngắn có `B = sum(bytes độc nhất G1–G5) = 896`, nhưng **riêng** root tree(B) là 1.020 byte. Đặt trần tổng 896 như A13: bản đúng G6–G8 unknown; reset bộ chi theo luật vẫn không đọc được root tree ấy, nên G7 vẫn unknown. Trong prototype mutant chỉ reset bộ chi dùng kiểm ngân sách, giữ riêng `do_dac` luỹ kế; **cả vector lẫn số đo vẫn trùng**, không phải mutant bị một assertion số đo khác giết hộ.

```text
A13_TOTAL_CAP 896 ROOT_B_BYTES 1020
A13_total             : G1–G5 qua; G6–G8 unknown; G9 qua; 896 byte, 4 object
A13_total_mut_reset   : cùng vector, cùng 896 byte, cùng 4 object
```

**(c) Alias mới không tạo được `E_vang` bằng thao tác đã khai.** A/B “không sửa gì dưới ops” ⇒ ops(A) = ops(B) = ops(MOC), OID `d7a9de07a99585b13f133306a605b031b1ce0e05`. Clone `--shared --no-checkout` lấy object đó từ alternate của kho nguồn; không có loose object tương ứng trong clone tạm. Kể cả tạo bản loose đúng bytes rồi xoá, Git vẫn đọc lại được từ alternate. Reader đúng trả qua, làm ca nền A23(d) đỏ trước khi xét mutant.

```text
ALIAS_LITERAL ... local_loose_exists False
ALIAS_AFTER_LOCAL_DELETE cat-file-e-rc 0
A23_alias_literal_delete: G0–G9=qua
```

Đây không phải lỗi guard OID: guard trùng OID vẫn đúng. Thiếu guard **vị trí lưu object và khả năng tạo sự kiện thật**. Không được xoá object trong kho nguồn để làm test đạt.

**Lệnh/rc:** `PYTHONDONTWRITEBYTECODE=1 python -B probes.py > evidence/graph-probe.log 2>&1` và `PYTHONDONTWRITEBYTECODE=1 python -B more_probes.py > evidence/extended-probe.log 2>&1`, đều **rc 0**. [Mã chính](probes.py), [mã đối chứng](more_probes.py), [log chính](evidence/graph-probe.log), [log đối chứng](evidence/extended-probe.log), [trace 1](evidence/graph-runs.json), [trace 2](evidence/extended-runs.json).

**Đề xuất và phép kiểm đã đo:**

1. Giữ f hiện tại để kiểm kết quả đã xong bất biến; **thêm ca chết sau G3** để G4/G5 chưa xong nhưng đủ memo. Bản đúng G4/G5 qua, mutant xoá memo G4/G5 unknown. Hai ca tách nghĩa vụ giữ *kết quả* và giữ *dữ liệu đã xác minh*.
2. A13 phải guard một luật sau G5 có tổng bytes cần đọc dưới `B` khi có ngân sách riêng, nhưng ngân sách chung đã cạn. Ví dụ tăng message H1 lên 300.000 byte và đặt `B=300.896`: bản đúng G6–G8 unknown; mutant reset cho cả ba qua. Các cap khác giữ mặc định. Guard kích thước phải tính trên OID thật; có ca âm cho setup không phân biệt.
3. Đổi alias thành **A tạo một subtree ops mới, B giữ nguyên subtree đó**; A/B vẫn có root tree khác nhau. Guard `ops(A)==ops(B)`, object loose thuộc clone tạm, **không tồn tại trong alternate**, xoá xong query object báo missing. Đối chứng đã chạy: G6/G7 unknown, G4/G8 qua; mutant cache lỗi thành rỗng làm G7 đỏ, mutant chỉ luật đầu thấy lỗi làm G7 qua.

**Không dùng `equivalent_verified` để đóng hai mutant sống trên ca cũ:** các ca sửa ở trên đã làm chúng đổi hành vi, chứng minh chúng **không tương đương toàn miền**. Rủi ro sửa: đổi thời điểm giết reader sẽ đổi oracle, nên không đổi seam mà giữ vector cũ; message quá lớn có thể đụng cap object; alias trỏ object kế thừa sẽ lại làm “xoá local” vô hiệu. Các guard phải kiểm trạng thái trước/sau tiêm, không chỉ tên vị trí.

## Rà 14 đường §0.8 và đồ thị thật

| # ở §0.8 | Kết luận |
|---:|---|
| 1 | Đã phân cục bộ/chung nhưng câu giữ memo còn bao trùm deadline: **F17**. |
| 2 | Tách framing có thể đồng bộ với reader chết đúng. A12(g)/(h) phân biệt G8 qua/unknown. |
| 3 | Tổng byte là chung được mô tả đúng; deadline ở §2.6 đúng oracle A13 nhưng trái §2.3. |
| 4 | Bảng `doc(G)` khớp theo OID, không còn dựa tên vị trí. |
| 5 | Guard OID loại được ca “chỉ G7” khi ops dùng chung. Chưa thay guard storage/khả năng gây missing. |
| 6 | Fixture dương mới cô lập ops(A), ops(B), workflows(B). Biến thể alias lại mượn ops(MOC): **F18(c)**. |
| 7 | H1 thiếu ⇒ G3/G4 unknown, guard ngoài tập đúng; xóa loose thật đã đo. |
| 8 | ops(B) băm lệch ⇒ chỉ G7 unknown, đã ghi bytes lệch tại OID trong clone riêng. |
| 9 | Các vector cap tổng/deadline mới đo được; mutant cap tổng còn bị root-tree-size che: **F18(b)**. |
| 10 | Reader chết sớm/muộn/framing hỏng cho đúng vector; ca f không phân biệt xoá memo: **F18(a)**. |
| 11 | Tree sai type/commit hỏng được gắn vị trí và guard; tập parser khớp producer. |
| 12 | Ba vị trí tree riêng làm đúng G6/G7/G8 unknown; chốt commit H1 làm G3/G4 unknown. |
| 13 | Chuỗi Q từ P không qua MOC: đầy đủ ⇒ G1 đỏ; xóa Q1 mới ⇒ chỉ G1 unknown. |
| 14 | G7/G8 thiếu blob riêng và giao OID lệch × thiếu blob đúng thứ tự F6; G6 không đọc leaf. |

**Các đường mà danh sách chưa giải quyết:** luật giữ memo trong bảng đóng phải loại deadline; vị trí lưu object kế thừa ở biến thể alias; trạng thái đã hoàn tất so với dữ liệu memo trong mutant chết muộn; ngưỡng tổng so với kích thước *từng luật sau điểm tiêm*. Vì vậy việc “đã quét 14 đường” không đủ chứng minh F16 đóng.

Oracle ở [probes.py](probes.py) không gọi evaluator/Reader sản phẩm, tự đọc raw `git cat-file` trên graph. Parser là mã probe; tập chốt được đối chiếu với `KhoObject.commit/tree`, và phép tương đương t2 dùng chính method producer trích bằng AST. Không dùng `rev-list`, `merge-base` hoặc `ls-tree` để quyết G. `rev-list` chỉ dùng cho phép đo lịch sử S2–S4 và xác minh ADR.

| Luật | Tập đọc đo được trên fixture dương |
|---|---|
| G0 | Rỗng. |
| G1 | commit D, B, A; dừng tại OID MOC, không đọc MOC. |
| G2 | commit B. |
| G3 / G4 | commit H1 / commit H1. |
| G5 | commit A. |
| G6 | commit A; root tree(A), ops(A); không đọc leaf. |
| G7 | commit B; root tree(B), ops(B); checker blob khi mode/OID khớp. |
| G8 | commit B; root tree(B), github(B), workflows(B); workflow blob khi mode/OID khớp. |
| G9 | Không object; tiến trình đọc ref riêng. |

OID đầy đủ: [graph-oids.json](evidence/graph-oids.json), [doc-table.json](evidence/doc-table.json). Mười hàng đối chiếu đúng; ca dương đọc **12 object độc nhất / 134.396 byte**. Không memo đọc 19 lần / 136.688 byte, nên chốt đếm memo có phân biệt.

## Đối chiếu đột biến A12/A13/A23

“Có phân biệt” dưới đây là phép đo trên prototype/guard của reviewer, chưa phải tín dụng `witness_killed` của suite sản phẩm chưa tồn tại. Chỉ công nhận khi đúng oracle liên quan đổi; một ngoại lệ setup không được tính.

| Nghĩa vụ / mutant khai trong spec | Kết quả |
|---|---|
| A12(b) bỏ băm | Có phân biệt: G7 từ unknown thành qua. |
| A12(c) bỏ cả cờ/biến no-replace | Có phân biệt: replace B→X bị reader băm phát hiện; G1/G2/G7/G8 từ qua thành unknown. |
| A12(d) bỏ lọc GIT_* | Có phân biệt: object directory rỗng làm G1–G8 unknown; bản lọc qua. |
| A12(e)/(h) restart reader | Có phân biệt: luật sau điểm chết lại đọc được, G8 qua thay unknown. |
| A12(e) coi chết là cục bộ | Mô hình phục hồi cho request kế tiếp làm các luật sau qua, ca e bắt được. |
| A12(f) xoá memo | **Sống trên ca chỉ định**, cả vector/số đo trùng: F18(a). Ca chết sau G3 giết được, không tương đương toàn miền. |
| A12(g) coi framing lệch là fatal | Có phân biệt: G8 unknown thay qua. |
| A13 vượt cap thành đỏ | Có phân biệt: G1 đỏ thay unknown. |
| A13 gộp bộ đếm walk | Có phân biệt: với cap 3 riêng từng walk, bản đúng qua; bộ đếm chung làm G2/G3 unknown. |
| A13 bỏ cap object | Có phân biệt: H1 300.212 byte, cap 250.000, mọi object khác tối đa 111.792; G3/G4 qua thay unknown. |
| A13 reset tổng theo luật | **Sống trên fixture hợp lệ có B=896**, F18(b); fixture có B=300.896 giết được. |
| A13 deadline cho memo chạy tiếp | Có phân biệt: G4/G5 qua thay unknown; đồng thời phơi mâu thuẫn F17. |
| A13 bỏ memo | Có phân biệt bằng tổng bytes/object, không cần đổi màu G. |
| A13 G0 dùng >= | Mô hình đọc bounded byte đổi biên 8.388.608 từ qua thành đỏ; CLI sản phẩm `not_run`. |
| A23 bỏ guard | Ca alias “chỉ G7”: bản đúng lỗi setup, bỏ guard chạy tiếp; guard có phân biệt. |
| A23 cache lỗi thành rỗng | Trên alias có thể gây missing thật: G7 đỏ thay unknown. Literal alias r7 chưa đạt nền, F18(c). |
| A23 chỉ luật đầu nhận lỗi | Trên alias đã sửa setup: G6 unknown, G7 qua thay unknown. |
| A23 oracle gọi module đang kiểm | Nghĩa vụ kiểm cấu trúc hợp lý; nguồn oracle prototype độc lập. **Suite sản phẩm chưa tồn tại**, chưa có mutant nguồn cuối để ghi killed. |

**Rà tương đương:** bỏ t2 riêng vẫn `E_hong` với cả năm mode hợp lệ và mode sai; bỏ nhóm t2+t3+t5 nhận đầu vào. Lập luận toàn miền: có separator thì t2 vốn không kích hoạt; không separator thì tên rỗng bị t5 bác khi mode đúng, hoặc t3 bác khi mode sai. F14 không tái mở; F18 là các witness mới khác, không phủ nhận disposition r6.

## Review toàn bộ r7 / A1–A23

| Phạm vi | Kết luận và giới hạn |
|---|---|
| §2.1; A1–A3 | Module JSON nguyên blob `3490ea0ee40081c0eba2d121f5b19a67a021a54b`. Module Git riêng, import theo file, bọc nguyên dict; K1/K2/K4 kiểm bằng module JSON thật. Không thấy ABI cũ bị mở rộng. |
| §2.2; A4–A6 | Bốn khóa, trạng thái đóng, bool nghiêm, serializer ASCII/sort_keys rõ. Mô hình rc: dương 0, đỏ 12, chỉ unknown 13, hỗn hợp 12; JSON đỏ/G0 đỏ 12. K1/K2 giữ G0 qua, G1–G9 không chạy; K4 không chặn G. CLI Git mới chưa có để đo byte stdout hoặc stderr. |
| G1; A7; N1/N3/N4 | B/MOC qua, P/E/X đỏ. Chuỗi phụ không MOC đỏ; xoá Q1 làm unknown, mọi G khác giữ màu. Guard dùng Q1 mới, không xoá object nguồn. Cả biên MOC và phân biệt thiếu bytes/vắng đường đã rà. |
| G2/G3; A8; N2/N5 | Strict ancestor S=B,C=A làm G2 đỏ; H=X làm G3 đỏ. Ca S=C và H con của C phù hợp inclusive ancestry; không có suy luận từ timestamp/depth. |
| G4/G5; A9 | Ba root khác, T=tree(S) làm G4 đỏ; tree_S=tree(H) làm G5 đỏ. Guard hạ tầng có nghĩa vụ ca âm riêng. Không suy khác subtree từ khác root. |
| G6; A10; N8 | Đối chiếu producer: leaf có mode bất kỳ nhận theo OID, không đọc leaf; missing-entry/null qua, ancestor không-tree đỏ. Không nhầm object theo cạnh tree sai type với entry có mode không-tree. Rà văn bản/producer, không nhận đã chạy toàn ma trận G6 sản phẩm. |
| G7/G8; A11; N7 | Năm mode đã đo riêng: 100644/100755/120000 qua; 160000/40000 đỏ. OID lệch + missing blob đỏ; khớp + missing unknown. Symlink so chính blob chuỗi đích; G8 hash nội dung, giới hạn GitHub nạp symlink khai rõ. |
| §2.3; A12 | Missing, băm lệch, replace, GIT_OBJECT_DIRECTORY, chết sớm/muộn, framing có/không đồng bộ đều chạy. F17/F18; một process thật, memo chỉ lưu thành công trong baseline. |
| §2.5; A5/A14; N6 | Tham số/N6 ban đầu rc 2, G9 trôi/xoá unknown/13. Probe ref thật kiểm cả prefix child không phải exact ref; đổi/xoá ref sau lần đầu cho đúng G9. Nguồn --master/base/head API thuộc hợp đồng caller, không được giả định đã xác minh provenance. |
| §2.6; A13 | Đơn vị walk/object/total/deadline/receipt rõ. Cap object riêng H1 và memo có guard đo được. Deadline chưa thống nhất, cap tổng thiếu guard phân biệt: F17/F18. Timeout thật khi pipe treo, RSS và Windows chưa đo. |
| §3; A15 | Hai đường write set, không sửa JSON/sổ/producer. 750 dòng là trần **thi công**, không áp 877 dòng spec. ~710 được ghi là ước; code ứng viên chưa có để đo. Vượt phải dừng, không cắt ca. |
| A16 | Windows required theo M3, base/candidate cùng máy/cùng lệnh, không dùng skipped làm pass. M3 còn yêu cầu test ID+kết quả; dẫn chiếu M3 giữ nghĩa vụ ấy. Máy Windows không có trong phiên: `not_run`. |
| A17 | M9 áp vì chạm .claude/dev: full_mutant_audit Ubuntu hoặc waiver đúng scope. Local suite không thay CI. `not_run` đối với code tương lai. |
| A18 | Child dương, đủ suite/hai module/registry nguyên byte, MOC tường minh, chặn đệ quy và lỗi đúng import Git giữ được sửa F7. N_git/M_git bằng 0 riêng, regex lấy từ sổ. Chưa có suite Git để chạy e2e sản phẩm. |
| A19 | Doctrine sạch 10/10 tệp, adr-song 64/64. Diff check riêng r7 rc 0. Bare Ruff hai tệp sản phẩm chưa chạy, không lấy “RUFF CI contract” từ registry thay lint. |
| A20 | Bảng đóng luật×E và nghĩa vụ không-E hợp lý; target/non-target theo OID được đo. F17 là quy tắc chung trái bảng ngân sách, không chỉ lỗi một hàng test. |
| A20b | 21 ca tree an toàn (7 dạng × 3 vị trí) + 3 dạng commit hỏng đã chạy; đúng G6/G7/G8 hoặc G3/G4 unknown. t1 hai nhánh; t2, t3, t4, t5, t10. Các tên đặc biệt/thoát thư mục chỉ mô tả dưới đây. |
| A21 | Allowance 3 bất biến với U_lower 8/14/15, U_max unknown. Init thật/readback 3; counter chặn thứ 4. State thử nghiệm không phải phục hồi journal thật. |
| A22 | Lệnh init đủ packet/mission/provider/limit; thiếu mission và limit 0 rc 2. Rescue ID/URL 2/0 ở blocked/rescue_required thử nghiệm. Cặp cờ §8 không bị coi invocation đầy đủ. Holder chỉ kiểm parser, không đo live holder. |
| A23 | Oracle độc lập, doc table, guard âm đúng. Ca alias xoá object sai tiền đề storage: F18(c); các mutant alias có phân biệt trên đối chứng sửa setup. |
| §5–§7 | C1a2/C1b, receipt thật S≠C, T2/Q17, #656/#564/#499, #1160 ngoài scope được giữ; không đồng nhất “nhất quán C tự khai” với provenance/land authority. Lịch sử lớp và điều kiện dừng không reset. |
| §8/§11 | Dòng ADR-0055 + nang_tran 16, đơn vị allowance theo pha và U_max unknown phù hợp ngoại lệ đã được chủ kho cấp trong prompt. Không suy 16−U_lower, không gọi mặc định limit 2. Quyền thêm 2 lượt tại §0.8/§8 là sửa giới hạn pha spec 4 của lịch sử. Không phát hiện đường cấp cap mới trái quy tắc. |

**Hướng thử có tên dạng thoát thư mục (không tạo payload):** với t6/t7/t8, dựng tree băm đúng chứa tên đại diện thư mục hiện tại, thư mục cha hoặc tên chứa dấu phân cách; với t9 dùng tên thư mục metadata Git bị cấm. Đặt riêng vào subtree của S, C-checker, C-workflow, không checkout, kiểm chỉ tập luật theo OID nhận `E_hong`; đổi riêng tên sang tên hợp lệ làm đối chứng. Đối chiếu nguồn producer đã thấy đủ các chốt; không tuyên bố các payload này đã chạy.

## Số đo và bằng chứng chạy

Lệnh tổng hợp: `PYTHONDONTWRITEBYTECODE=1 python -B measurements.py > evidence/measurements.log 2>&1`, **rc 0** của driver. Mỗi lệnh con có rc riêng trong log; driver rc 0 **không** có nghĩa mọi lệnh con xanh.

| Phép đo trên base | Kết quả mới | Đối chiếu |
|---|---|---|
| S2 first-parent gồm MOC | 411 commit | Khớp. |
| S2 reader dừng trước bytes MOC | 410 commit / 531.751 byte; 0,034 s và 0,029 s | Count/bytes khớp; thời gian là phép đo mới. |
| S3 mọi tổ tiên | 5.444 commit / 8.480.418 byte; 0,363 s và 0,388 s | Count/bytes khớp. |
| S4 | first-parent 1.084; ngoài first-parent 4.360; log producer 64; giao 64 | Khớp đủ bốn đại lượng. |
| S5 producer + workflow | +649/−92 và +1/−1 = **+650/−93**, 2 tệp | Khớp. |
| S6 JSON suite | rc 0; 156/156 ca, 162/162 killed; equivalent 9, unresolved 0; 11,873 s | Khớp. |
| Sổ CI hiện tại | rc 0; 29/29, phản chứng 1.070/1.070 | Khớp r6; không sửa sổ. |
| JSON/suite/registry/packet_loop base→HEAD | Bốn cặp blob bằng nhau | Không cần chạy lại cùng byte như hai bản khác nhau. |
| §11.5 drift base→08bcb51f | Một tệp .githooks/eol_policy_test.py +698/−92 | Khớp số lịch sử. |
| Các đường phụ thuộc chính base→HEAD | Numstat rỗng | Không thấy drift ở các đường đã lọc trong script. |
| ADR-0055/0053/0060 | Mỗi mỏ neo: present rc 0 / parent rc 128 / có trong first-parent rc 0 | Khớp snapshot local không shallow; không khai ref vừa fetch live. |
| Doctrine / adr-song | rc 0; 10 tệp/0 vi phạm; 64 ADR/64 dòng | Scanner không thay review ngữ nghĩa. |
| Diff check **riêng r7** từ head r6→HEAD | rc 0 | Spec không có whitespace error. |
| Diff check **toàn cây** base→HEAD | **rc 2**: whitespace trong hiện vật review cũ | Giữ là failed, không ghi toàn cây xanh. Ngoài nội dung spec r7 được giao; không sửa lịch sử evidence. |

Môi trường mới: Linux `6.18.44-fc-v242`, Python `3.13.18`, Git `2.43.0`. S7 receipt thật, S8 Windows/WSL cũ, quota, ref remote/holder live không đo lại; không suy từ mirror. Cần người cấp lease đo lại theo §11.6.

Các lệnh probe chính đều chạy từ sandbox:

```text
PYTHONDONTWRITEBYTECODE=1 python -B probes.py > evidence/graph-probe.log 2>&1           # rc 0
PYTHONDONTWRITEBYTECODE=1 python -B more_probes.py > evidence/extended-probe.log 2>&1    # rc 0
PYTHONDONTWRITEBYTECODE=1 python -B acceptance_checks.py > evidence/acceptance-checks.log 2>&1  # rc 0
```

[Log số đo](evidence/measurements.log), [log acceptance/CLI](evidence/acceptance-checks.log). Hai file trace JSON chứa **85** lần đánh giá graph; acceptance_checks bổ sung JSON thật, mô hình ABI/rc/G0, Q không MOC, ref drift và mutant alias. Đây không phải “85 acceptance sản phẩm passed”.

Lỗi của công cụ reviewer được giữ riêng: lần graph đầu rc 1 do cố ghi loose object 0444, sửa bằng unlink/tạo lại trong scratch; lần extended đầu rc 1 do prototype quên nhận C=MOC ở biên, đã sửa và chạy lại. [Log setup](evidence/graph-probe-setup-error.log), [log lỗi prototype](evidence/extended-probe-prototype-error.log). Không dùng hai lần hỏng ấy để kết luận spec sai hay tính tín dụng giết mutant.

## Kiểm toàn vẹn và giới hạn còn lại

Snapshot nội dung trước các suite nền và sau toàn bộ probe: **12.875 mục** (12.871 tệp cùng bốn mục Git/status/index/ref), delta **0**; HEAD/tree/băm spec không đổi; status tracked/untracked/ignored rỗng. [Snapshot trước](evidence/source-before.json), [snapshot sau](evidence/source-after.json), [log trước](evidence/snapshot-before.log), [log sau](evidence/snapshot-after.log). Phép đo hai mốc chứng minh không có delta quan sát được, không tự chứng minh toàn lịch sử chưa từng ghi/hoàn nguyên; sandbox và cách gọi read-only là biên bổ sung.

Chưa đo implementation Git cuối, Windows, CI/full mutant audit, timeouts/kill-tree thật, RSS/cold-cache, authority/journal dispatcher ngoài mirror. Các mục đó là nghĩa vụ pha thi công hoặc dữ liệu ngoài phiên, không biến thành pass. Không có finding P1/P3 mới đủ căn cứ; hai P2 ở trên đủ để **không approve r7**.

TONG: P1=0 P2=2 P3=0
