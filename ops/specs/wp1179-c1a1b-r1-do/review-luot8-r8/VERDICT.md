reviewed_sha: caa5a0ec6a6bbc699c70dcfbd2541cb9ac9aec73
spec_sha256: 24418d1e68ea46324b8bb9a6cecb44eddcf31dd0e0ad0af39a2a2852f0f88454
provider: OpenAI Codex
model/effort: GPT-6 (theo định danh hệ thống); model ID triển khai và mức effort không được công cụ phiên này cung cấp, không suy từ cấu hình reviewer trong spec.
execution_surface: codex_cli (run.json của đúng run 1d06f0ca)
transport: machine (run.json); công cụ shell trực tiếp
verdict: changes_requested

**Kết luận cuối:** F17 và ba biểu hiện cũ của F18 được sửa; còn **F19 P2** cùng lớp đột biến: hai ánh xạ ca đích trong A12 chưa đúng. Không approve r8. Đây là lượt cuối được cấp trong chỉ thị; không gọi thêm reviewer hoặc sửa kho đang review.

## Neo và phạm vi

- `git -C ../cay-kho rev-parse HEAD`: rc=0, `caa5a0ec6a6bbc699c70dcfbd2541cb9ac9aec73`.
- `sha256sum ../cay-kho/ops/specs/wp1179-c1a1b-r8.md`: rc=0, khớp băm nêu trên.
- Kho được review chỉ đọc. Probe và bằng chứng mới chỉ ghi trong sandbox. Đây là review đặc tả, không tuyên bố đã chạy acceptance trên implementation C1a1b chưa tồn tại.

## Bằng chứng đã hoàn tất (cập nhật trong lượt)

- Run hiện tại: `1d06f0ca9c1042619c35f66dcbb54d4e`, đọc từ `../run/1d06f0ca/run.json`: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`. Run đang chạy nên chưa có terminal receipt/model phục vụ; không suy model từ cấu hình spec. Sandbox thực tế theo chỉ thị môi trường: `workspace-write`, approval `never`, kho review ngoài writable roots.
- Tree HEAD: `9aeea0e8b4d25bcb6c7d4f978c444b2979431088`. Snapshot trước: 12.895 mục, lưu `evidence/source-before.json`.
- `PYTHONDONTWRITEBYTECODE=1 python -B graph_probe.py > evidence/graph-probe.log 2>&1`: **rc 0**, 42 lượt mô hình trên object Git thật; mã tại `graph_probe.py`. Fixture dương: 12 object / 134.396 byte. Bảng OID và tập đọc: `evidence/graph-oids.json`, `evidence/doc-table.json`.
- A12 e/f/f2/g/h và A13 deadline cho đúng vector r8. A12 f2 giữ G4/G5 `qua`, deadline cùng điểm sau G3 đổi G4/G5 thành `khong_do_duoc`.
- A13 tổng byte trên H1 phóng to: cap **300.910**, byte riêng G6/G7/G8 = **3.925 / 115.753 / 15.474**, guard dương. Reset tổng theo luật đổi cả G6–G8 từ unknown thành qua.
- A13 object: cap **111.793**, H1 **300.214**, mọi object khác tối đa **111.792**; chỉ G3/G4 unknown. Bỏ cap trả cả hai qua.
- Alias mới: guard loose/không nằm nguồn đạt; xóa rồi `cat-file -e` báo thiếu; xóa/băm lệch đều chỉ G6/G7 unknown. Memo lỗi thành rỗng làm G7 `do`; chỉ luật đầu nhận lỗi làm G7 `qua`.
- Chín phép guard dương/âm trả đúng, gồm các họ A23(e): lưu trữ, tổng byte, object bytes, memo tại điểm tiêm. Đây là probe thước kiểm, chưa phải mutant nguồn suite sản phẩm.
- `PYTHONDONTWRITEBYTECODE=1 python -B measurements.py > evidence/measurements.log 2>&1`: **rc 0 của driver**; rc từng lệnh con trong `evidence/measurements.json`. Suite JSON thật: **156/156**, killed **162/162**, equivalent **9**, unresolved **0**, rc 0. Sổ: **29/29**, phản chứng **1.070/1.070**, rc 0. Doctrine **10 tệp/0 vi phạm**, ADR **64/64**, rc 0.
- S2: **411** gồm MOC; reader **410 / 531.751 byte**, hai lần **0,032 / 0,026 s**. S3: **5.444 / 8.480.418 byte**, **0,351 / 0,331 s**. S4: **1.084** first-parent, **4.360** ngoài chuỗi, lịch sử producer **64**, giao **64**. S5 **+650/−93**, hai tệp. Các số đếm/bản thân byte khớp spec.
- Diff check riêng r8: **rc 0**. Toàn cây base→HEAD: **rc 2**, whitespace trong evidence lịch sử; không ghi nhầm thành toàn cây xanh.

## Finding mới đã có phản chứng

### F19 — P2 — `dot-bien-tuong-duong-hoac-thieu`

**Vị trí:** `ops/specs/wp1179-c1a1b-r8.md:697` (A12, cột đột biến, hai ánh xạ e/f); quy tắc ca đích `:609–629`; danh sách tự quét F18 `:300–311`.

**(a) Đột biến coi reader chết là lỗi cục bộ vẫn sống trên ca e được chỉ định.** Ca e kết thúc tiến trình `cat-file` thật trước lần đọc đầu. Bỏ việc duy trì trạng thái lỗi chung, xử lý mỗi lỗi I/O tại từng luật và không khởi động lại tiến trình vẫn làm G1–G8 unknown: process đã chết, các lần đọc sau không thể có bytes. Không có căn cứ cho lời khẳng định ở A12 rằng mutant ấy làm G2–G8 `qua`.

Đã dựng mutant chỉ bỏ việc giữ lỗi/đóng reader cho lỗi cục bộ, **không restart**. Trên e, cả vector và số đo đều trùng bản đúng: G0/G9 qua, G1–G8 unknown, 0 object/0 byte. Trên h, cùng mutant không kết thúc reader khi seam làm framing hỏng: G7 vẫn unknown nhưng G8 từ unknown thành qua. Vì vậy mutant **không tương đương toàn miền**; không được dùng `equivalent_verified` để che việc ca e không giết được nó. Ca h đang có đủ khả năng phân biệt, nhưng hợp đồng `TinHieuChotCa` đòi đúng tên ca chỉ định nên cần sửa ánh xạ.

**(b) Đột biến “đánh giá lại luật đã hoàn tất” không đồng nghĩa “xoá kết quả thành unknown”.** Sau G5, G1–G5 đều có đầy đủ object thành công trong memo. Gọi lại đúng các luật ấy sau khi reader chết cho nguyên vector và 4 object/912 byte; cả ca có G4 `do` cũng giữ `do`. Muốn f cho G1–G5 unknown như cột đột biến ghi, phải đổi trạng thái đã lưu hoặc thêm hành vi bỏ qua memo; riêng thao tác đánh giá lại không đủ. Đối chứng kết thúc reader đồng thời hết deadline cho thấy đánh giá lại có thể đổi một luật đã hoàn tất từ qua thành unknown, nên cũng không tự gán tương đương toàn miền. Không cần thay oracle f: sửa tên/định nghĩa mutant thành **ghi đè trạng thái đã hoàn tất thành unknown** là đủ, và probe đã đo ca f giết được mutant ấy.

**Lệnh và bằng chứng:** `PYTHONDONTWRITEBYTECODE=1 python -B mutation_probe.py > evidence/mutation-probe.log 2>&1`, rc 0; mã `mutation_probe.py`, bản sao mutant `tmp/local_event_mutant.py`, trace `evidence/mutation-runs.json`. Trích output:

```text
A12_e: baseline == LOCAL_NO_RESTART; G1–G8 unknown; 0 object / 0 byte
A12_h: baseline G8=khong_do_duoc; LOCAL_NO_RESTART G8=qua
A12_f: baseline == REEVALUATE_MEMO; G1–G5 qua; 4 object / 912 byte
A12_f: INVALIDATE -> G1–G5 khong_do_duoc
COMPLETED_G4_DEATH_AND_DEADLINE qua khong_do_duoc
```

**Đề xuất đóng cả lớp ở đây:** định nghĩa đột biến theo đúng một thay đổi hành vi, tách thao tác tiêm lỗi vật lý khỏi chính sách xử lý lỗi. Chuyển ca đích của mutant lỗi cục bộ từ e sang h (giữ e cho restart); đổi mutant f thành ghi đè kết quả đã hoàn tất. Thêm hai đường này vào §0.9; giữ f2 cho xoá memo. Chạy bản đúng trước, sau đó chứng minh đúng tên ca bị giết; không lấy một mutant khác hoặc một lỗi setup làm tín dụng. Đây là cùng lớp F18, không phải lớp mới để đặt lại lịch sử.

## Đối chiếu F17–F18

| Finding lượt 7 trên `4f3738ae` | Kết luận lượt 8 | Bằng chứng độc lập |
|---|---|---|
| F17 P2 `phan-loai-vang-va-khong-do-duoc` | **ĐÃ VÁ THẬT** trong phạm vi đặc tả. Bảng §2.3 phân biệt lỗi reader/tổng byte với deadline; không còn hai oracle trái nhau cho G4/G5 tại điểm sau G3. | A12 f2: G4/G5 qua; A13 deadline: G4/G5 unknown, G9 unknown. Oracle tài nguyên độc lập lấy tập đọc trừ memo tại điểm tiêm, không lấy memo tương lai của ca dương. `guard-audit.log`, `graph-runs.json`. |
| F18(a), xoá memo sau G5 không phân biệt | **ĐÃ VÁ THẬT** cho mutant xoá memo: ca f2 mới giết được; f giữ kiểm kết quả đã hoàn tất. Có biểu hiện mới trong mô tả mutant f, ghi F19(b). | `M_f2_clear`: G4/G5 từ qua thành unknown. |
| F18(b), cap tổng bị object lớn che | **ĐÃ VÁ THẬT**. Guard mới buộc cap lớn hơn nhu cầu riêng từng luật sau G5. | B=300.910 > max(3.925,115.753,15.474). Reset tổng: G6–G8 từ unknown thành qua. Fixture không phóng to H1: B=912 <115.753, guard âm bị bác. |
| F18(c), alias lấy object từ alternate | **ĐÃ VÁ THẬT**. Subtree ops mới của A/B nằm loose tại clone; không có trong nguồn; xóa có hiệu lực thật. | Alias xóa/băm lệch: G6/G7 unknown, G4/G8 qua. Alias cũ bị guard bác. Đối chứng tạo bản loose của object kế thừa: local có, nguồn rc 0; xóa local xong clone vẫn rc 0, chứng minh cần cả chốt nguồn và hậu kiểm. |

Không đồng nhất “ba biểu hiện cũ của F18 đã vá” với “lớp F18 đóng”: F19 vẫn thuộc chính lớp đó.

## Rà đủ đường cùng lớp ở §0.9

| Danh sách | Phạm vi kiểm | Kết quả |
|---|---|---|
| F17.1–3 | §2.3 bảng phạm vi; §2.6; oracle chung §4 | Cùng một luật cho memo, kết quả hoàn tất, G9. Đã đo tại trước G1/sau G3/sau G5. |
| F17.4 | A12 e/f/h, cộng f2/g dù danh sách chỉ nêu e/f/h | Vector reader đúng; framing còn đồng bộ cục bộ, framing hỏng chung. F19 nằm ở **đột biến/ca đích**, không phải vector nền. |
| F17.5–7 | A13 tổng/deadline, hàng E_ngan_sach/E_reader_chet | Khớp bảng duy nhất. Cap object và walk không lan sang luật khác nếu tập đọc/đơn vị không liên quan. |
| Ngoài danh sách F17 | §2.2 thứ tự/G0/skip; §2.3 memo và G9; cuối §2.4; A20/A23 | Không phát hiện mâu thuẫn màu mới. Câu cuối §2.4 được đọc cùng dẫn chiếu §2.3: vẫn đánh giá/ghi trạng thái các luật sau, không có nghĩa tài nguyên chung không ảnh hưởng chúng. |
| F18.1 | A12 f và f2, thời điểm tiêm | f2 sửa đúng xoá memo. **Chưa đủ đối chiếu thao tác mutant với oracle**: đánh giá lại khác ghi đè kết quả (F19b). |
| F18.2–4 | Cap tổng, cap object, deadline | Guard tiền đề dương/âm đều phân biệt; bỏ từng guard trong probe làm đúng ca âm thất bại. |
| F18.5–6 | Alias; A7 Q1; A12 H1/ops(B); A20b; A23 | Không xóa object nguồn. Mất object Q1 chỉ đổi G1; H1 chỉ G3/G4; ops(B) chỉ G7. A20b dựng object mới băm đúng trong clone. |
| F18.7 | A9 ba root tree | Ba OID khác; fixture có hai tree trùng bị guard bác. Cả ca G4/G5 lệch có đổi màu đúng luật. |
| **Đường bị sót của F18** | **A12 e: process chết vật lý đối với mutant “lỗi cục bộ”** | **F19a.** Danh sách rà tiền đề chưa xét rằng mọi lần đọc sau đều lỗi dù không giữ cờ lỗi chung. Chỉ thay e bằng ca reader còn sống nhưng framing hỏng mới phân biệt chính sách cục bộ/chung mà không ghép thêm restart. |

## Bảng lớp theo ADR-0060 M2 / protocol §8.3

| Slug lớp | Nguồn/biểu hiện | Mức còn mở | Kết quả và phép đóng |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | draft0–2; F4/F6/F11/F13/F16/F17 | — | Đã vá thật ở tầng đặc tả: bảng đóng, OID trước blob, parser, tập đọc và phạm vi tài nguyên được kiểm độc lập. Giữ nghĩa vụ đo mã cuối. |
| `dot-bien-tuong-duong-hoac-thieu` | F3/F7/F14/F18; **F19(a,b)** r8 | **P2** | Chưa đóng. Sửa chung: ghép chính xác thay đổi hành vi ↔ trạng thái vật lý/memo ↔ tên ca đích; e→h cho lỗi cục bộ, gọi đúng mutant ghi đè kết quả cho f. Rerun đúng hai witness theo đề xuất F19. |
| `mo-rong-module-pha-hop-dong-json-thuan` | draft0–2; §0.2/A1–A3 | — | Không tái mở: JSON giữ byte, module Git riêng, kết quả JSON nguyên vẹn; suite nền thật xanh. |
| `predicate-consumer-khong-khop-producer` | F2; G6/G7/G8 | — | Không tái mở: đủ mode, null/missing/non-tree, symlink so OID entry; giới hạn provenance giữ nguyên. |
| `oracle-trang-thai-g0-mau-thuan` | F8; A6 | — | Không tái mở: G0 qua khi JSON nhỏ sai K1/K2, G0 do khi quá cỡ; JSON null chỉ trong trường hợp sau. |
| `dat-lai-ngan-sach-khi-doi-truc` | F1/F9/F10; §8/§11/A21 | — | Không tái mở: allowance=3 độc lập U_lower, U_max unknown; state readback 3, không suy số dư. |
| `huong-dan-cli-khong-khop-parser` | F12/F15; A22 | — | Không tái mở: init đủ mission, limit dương; ID/URL rescue phân biệt 2/0 trên fixture blocked đúng dạng. Hành trình tạo state thật vẫn unknown như spec khai. |
| `so-do-ke-thua-chua-do-lai` | F5; S4 | — | Không tái mở: 5.444−1.084=4.360, log producer/giao đều 64, các số đo mới lưu đủ. |
| `nguon-duoc-tin-ma-chua-xac-minh` | Lịch sử C1a1a; N6/N7 | — | Không mở biểu hiện mới trong scope này: raw hash, replace/env, exact ref và giới hạn C tự khai đã rà. C1a2/C1b chưa đo, không coi là được C1a1b chứng minh. |

Hai lớp mở cuối r7: chỉ lớp F17 đóng toàn bộ; lớp F18 còn F19. Tỷ lệ đóng lớp **1/2 = 50%**; **0 lớp mới**, **1 lớp tiếp tục mở**, **1 finding mới gồm 2 biểu hiện**. Không dùng việc đổi ID sang F19 để xóa lịch sử lớp.

## Đột biến A12/A13/A23 và guard

Các số dưới đây là phản chứng trên **prototype của reviewer**, không phải `witness_killed` của implementation/suite Git chưa được viết.

| Nghĩa vụ | Đối chứng đã chạy | Kết luận |
|---|---|---|
| A12 bỏ băm | Băm lệch ops(B): đúng G7 unknown; bỏ băm G7 qua | Có phân biệt đúng b. |
| A12 bỏ cả no-replace | Replace B→X: đúng không đổi; mutant G1/G2/G7/G8 unknown | Có phân biệt đúng c. |
| A12 bỏ lọc GIT_* | Child thừa kế GIT_OBJECT_DIRECTORY rỗng: lọc env cả G qua; mutant G1–G8 unknown | Có phân biệt đúng d; reader bình thường dùng môi trường đã lọc. |
| A12 restart reader | e: G1–G8 qua; h: G8 qua | Có phân biệt đúng e/h. |
| A12 coi chết là cục bộ | Không restart: e không đổi, h đổi G8 | **Sai ca đích e: F19a**. Mô hình “phục hồi đọc” trong probe đầu thực chất cùng hành vi restart, không dùng nó làm tín dụng cho mutant cục bộ. |
| A12 đánh giá lại kết quả đã xong | f không đổi với memo giữ nguyên; ghi đè trạng thái thì đổi | **F19b**; cần định nghĩa mutant đúng như oracle muốn khóa. |
| A12 xoá memo | f2: G4/G5 unknown | Có phân biệt. |
| A12 áp deadline cho reader chết | f2: G4/G5 và G9 unknown | Có phân biệt; `death-as-deadline.json`. |
| A12 coi framing lệch là fatal | g: G8 unknown thay qua | Có phân biệt. |
| A13 ngân sách thành do | Cap walk: G1 do thay unknown | Có phân biệt. |
| A13 gộp walk counters | Cap chung giá trị 3: bản đúng cả ba qua; mutant G2/G3 unknown | Có phân biệt, ca bổ sung sát nghĩa per-walk. |
| A13 bỏ cap object | H1 300.214 vượt 111.793; mutant G3/G4 qua | Có phân biệt. |
| A13 reset tổng theo luật | B=300.910, guard dương; mutant G6–G8 qua | Có phân biệt. |
| A13 deadline vẫn dùng memo | G4/G5 qua thay unknown | Có phân biệt. |
| A13 bỏ memo | 12/134.396 thành 19/136.712 | Có phân biệt bằng số đo; không đòi đổi màu G. |
| A13 G0 >= | 8.388.608 đổi qua→do, 8.388.609 vẫn do | Mô hình biên có phân biệt; CLI Git sản phẩm chưa có. |
| A23 bỏ guard OID | Alias cùng OID nhưng đòi chỉ G7 | Ca âm guard bị giết trong probe; không dùng lỗi vô can. |
| A23 cache lỗi rỗng / chỉ luật đầu | Alias mất object: G7 do / qua thay unknown | Cả hai có phân biệt ở d. |
| A23 oracle gọi evaluator | Đọc AST hàm oracle độc lập: dương đạt, thêm gọi evaluate bị bác | Phép tự kiểm cấu trúc có phân biệt; mã suite cuối còn phải audit. |
| A23 bỏ guard lưu trữ | Alias r7 có object trong nguồn | Ca âm bị giết; bản đúng bác setup. Không tính kết quả alias cũ làm missing thật. |
| A23(e) từng họ guard | OID, storage, tổng byte, object byte, memo | Ca âm riêng + bypass đều bắt đúng tên guard; log `coverage-probe.log`. Có thêm đối chứng riêng local duplicate/alternate/post-delete. |

Tập đọc oracle khớp **10/10 hàng** bảng §4 theo OID (`guard-audit.log`). Ngay sau G3, memo chứa H1 và A nhưng chưa có tree(A); vì vậy cả f2/deadline dùng cùng điểm tiêm nhưng cho khác kết quả, đúng yêu cầu r8.

## Review toàn bộ r8 / A1–A23

| Phạm vi | Kết quả, căn cứ và giới hạn |
|---|---|
| §2.1, A1–A3 | Module JSON blob `3490ea0ee40081c0eba2d121f5b19a67a021a54b` bằng base; test/registry/packet_loop cũng bằng blob base. Nạp JSON thật và receipt đồ thị mới: dương ok; K1/K2/K4 âm đúng. Import theo file và bọc nguyên dict là yêu cầu rõ; mã Git tương lai chưa tồn tại để chạy integration. |
| §2.2, A4–A6 | ABI bốn khóa, kiểu bool, trạng thái đóng, rc ưu tiên 12 trước 13 và serializer byte rõ. Mô hình dương/đỏ/unknown/hỗn hợp/JSON đỏ/G0 đỏ trả 0/12/13/12/12/12. G0/skip K1/K2/K4 khớp JSON thật. Không khai đã đo stdout CLI mới. |
| G1, A7, N1/N3/N4 | B và MOC qua; P/E/X do. Chuỗi Q từ P không MOC hoàn chỉnh cho do; xóa Q1 mới cho unknown, G khác giữ vector. Đồ thị thật trên MOC, không thay hằng hoặc dùng Git ancestry engine quyết luật. |
| G2/G3, A8, N2/N5 | Đo strict ancestor S=B/C=A đỏ; H=X đỏ; S=C inclusive qua. Không dùng ngày/depth để cắt ancestry. |
| G4/G5, A9 | Các root S/C/H khác nhau thật. T=tree(S) làm G4 do, tree_S=tree(H) làm G5 do; không đổi màu luật còn lại. Guard root trùng có ca âm. |
| G6, A10, N8 | Đo năm mode với đúng OID và null; gitlink tới object không có vẫn qua nếu OID khớp; vắng với null/hex, ancestor blob với null/hex đúng bảng. Không đọc leaf. Đối chiếu `KhoObject.tim`/producer, phân biệt entry mode không-tree với cạnh khai tree trỏ blob. |
| G7/G8, A11, N7 | Hai luật đều đo 100644/100755/120000 qua, 160000/40000 do, vắng/non-tree do. Blob khớp mà thiếu unknown; **OID lệch + blob thiếu do**, giữ F6. G8 sai sha256 do. Symlink hash chính chuỗi đích; không tuyên bố chứng minh Python đã chạy target hay GitHub đã nạp symlink. |
| §2.3, A12 | Một batch reader thật, băm raw body; memo thành công, các mutant cố ý phá memo được tách. Missing/hash/replace/env/death/framing đã đo. Oracle nền r8 đúng; hai witness mới sai ánh xạ: F19. |
| §2.5, A5/A14, N6 | Tách tham số và lệch/vắng ref ban đầu rc 2 khỏi drift cuối unknown/13. Prefix ref child không bị nhận là ref exact. Đọc ref Git thật trước/sau đổi và xóa; đưa giá trị đo được vào mô hình G9 cho unknown (`ref-env-probe.log`). Hợp đồng yêu cầu tiến trình ref riêng, không chịu reader chết. Nguồn tham số vẫn do caller đảm bảo. |
| §2.6, A13 | Walk cục bộ, cap object theo OID, tổng và deadline chung theo bảng mới; đo guard dương/âm. Cap receipt và hằng mặc định có nghĩa vụ acceptance rõ. Chưa đo timeout khi pipe treo, RSS hay performance Windows của implementation mới. |
| §3, A15 | Hai đường write set, JSON/sổ/producer giữ nguyên; ngưỡng **2 tệp/750 dòng thêm** theo Q-KT. Spec 927 dòng/108.609 byte không phải diff thi công. ~710 vẫn là ước, vượt phải dừng; chưa có code để chứng nhận A15. |
| A16 | Windows required, base/candidate cùng máy/cùng lệnh, skip không là pass; dẫn ADR-0060 M3 giữ yêu cầu test ID+kết quả. Miễn full audit trên Windows không miễn lượt tập trung hay CI Windows. **not_run**, không có máy chủ kho trong phiên. |
| A17 | M9/full mutant audit Ubuntu hoặc waiver scope đúng vẫn được yêu cầu. **not_run**, chưa có PR code/CI receipt tương ứng; không lấy probe local thay CI. |
| A18 | Child dương trước, đủ suite/hai module/sổ nguyên byte, gốc MOC truyền tường minh và cờ tránh đệ quy. N_git/M_git zero riêng, lỗi import phải đúng module, dòng tổng theo regex sổ. Sửa F7 còn nguyên. Chưa có module Git nên e2e sản phẩm **not_run**. |
| A19 | Doctrine 10/10 và ADR64/64 rc0; diff riêng r8 rc0. Sổ đo Ruff CI contract **3/3**; **bare Ruff không đo được**: `python -m ruff --version` và lint suite đều rc1, `No module named ruff`. Không gán “lint passed”. Toàn cây diff check rc2 do evidence cũ. |
| A20 | Đọc ma trận mọi luật×E và ô không-E, mục tiêu theo OID. Wrong type ops(C) chỉ G7 unknown. Không lan lỗi object địa phương ra mọi luật; guard với lỗi chung dùng memo tại thời điểm tiêm. Không phát hiện ô bị định sai thêm. |
| A20b | Đã chạy **21 ca tree lỗi an toàn** (7 dạng ×3 vị trí), **3 ca commit hỏng**, đối chứng tree hợp lệ; đúng G6/G7/G8 hoặc G3/G4 unknown, mọi luật ngoài đích giữ màu. Tập chốt đối chiếu nguồn producer: t1 hai nhánh, t2 có thể bị t3/t5 che, mode/UTF-8/rỗng/trùng, c1/c2. Payload tên thoát thư mục không tạo; hướng thử mô tả bên dưới. |
| A21 | `cap=allowance=3`, U_max unknown, U_lower8/14/15 không đổi cap; init/status thật readback3. Trên **fixture state reviewing thử nghiệm**, ba record-call rc0, lần4 rc3; không tuyên bố khôi phục journal thật. |
| A22 | Init thiếu mission rc2/đủ rc0; limit0 rc2; bỏ limit đọc lại2. Rescue ID rc2/URL rc0 tại fixture blocked/rescue_required sinh từ chạm cap. Holder chỉ chạy `--help`/đọc parser; **không** gọi đó là đo holder live. §11.2 đã khai rõ chưa đo đường đưa state thực vào reviewing/blocked. |
| A23 | Tập đọc exact10/10; guard OID và alias hai chiều, storage gồm local/alternate/hậu kiểm, kích thước/memo và ca âm riêng đã đo. Guard cấu trúc oracle có phản chứng. Chốt nghĩa vụ chung không sửa được ca đích A12 viết sai; F19 vẫn cần sửa riêng mapping. |
| §5–§7 | C1a2/C1b, Q17/T2, #656/#564/#499 và #1160 đúng ngoài scope. Không nâng receipt tự nhất quán thành chứng cứ land/provenance. Lịch sử lớp và stop conditions không reset. |
| §8/§11 và ADR-0043/0052/0055, protocol §12 | Ba trục độc lập, lời gọi có output tính cả timeout/connector, reject trước output không tính. Trần10 opt-in rồi ngoại lệ16 và allowance theo pha có nguồn quyền được prompt xác nhận. Không suy số dư từ cận dưới; lịch sử không reset. Quyền thêm2 thay giới hạn pha spec cũ; lượt8 còn finding phải dừng. Không phát hiện đường cấp lời gọi mới ngoài quyền đó. |

**Hướng thử chỉ mô tả bằng lời, không soạn payload:** với t6/t7/t8, dùng tree băm đúng chứa tên đại diện thư mục hiện tại, thư mục cha hoặc chứa dấu phân cách đường dẫn; t9 dùng tên thư mục metadata Git bị cấm. Đặt riêng vào subtree S, C-checker, C-workflow và alias; không checkout. Kiểm các luật trong tập đọc OID unknown, các luật ngoài tập giữ màu; thay đúng tên đó bằng tên hợp lệ để có đối chứng. Đây là `not_run` cho payload ấy, không tính vào 21 ca đã chạy.

**Disposition t2:** không separator thì tên rỗng; mode hợp lệ bị t5 chặn, mode không hợp lệ bị t3 chặn. Có separator thì t2 không kích hoạt. Vì vậy lập luận tương đương riêng t2 hợp lệ; bỏ cả t2+t3+t5 vẫn là nghĩa vụ riêng. Đây không phải lý do miễn hai mutant F19: đã có phản chứng cho thấy chúng có thể khác hành vi trên miền hợp lệ của sự kiện.

## Lệnh, số đo bổ sung và giới hạn

| Lệnh từ sandbox | rc | Output/phạm vi |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 python -B graph_probe.py > evidence/graph-probe.log 2>&1` | 0 | 42 evaluation, fixture/alias/H1 lớn, counterfactual mutants. |
| `PYTHONDONTWRITEBYTECODE=1 python -B coverage_probe.py > evidence/coverage-probe.log 2>&1` | 0 | 74 evaluation bổ sung, JSON thật, guard, N6 exact; tổng hai trace **116**, không gọi là 116 acceptance sản phẩm. |
| `PYTHONDONTWRITEBYTECODE=1 python -B mutation_probe.py > evidence/mutation-probe.log 2>&1` | 0 | F19, không restart che sai ca đích; phép đo f và đối chứng deadline. |
| `PYTHONDONTWRITEBYTECODE=1 python -B guard_audit.py > evidence/guard-audit.log 2>&1` | 0 | Tập đọc10/10; resource oracle; AST guard; spec927 dòng/108.609 byte, suiteJSON535 dòng. |
| `PYTHONDONTWRITEBYTECODE=1 python -B cli_probe.py > evidence/cli-probe.log 2>&1` | 0 | Driver ghi rc từng lệnh. Ruff hai lệnh rc1 vẫn giữ là chưa đo được. State chỉ là fixture thử nghiệm trong sandbox. |
| `PYTHONDONTWRITEBYTECODE=1 python -B measurements.py > evidence/measurements.log 2>&1` | 0 | S2–S6, suite/sổ/scanner và từng rc ADR/diff. Driver0 không xóa các rc128 kỳ vọng của ADR-parent hoặc rc2 diff toàn cây. |
| `PYTHONDONTWRITEBYTECODE=1 python -B snapshot.py evidence/source-after.json evidence/source-before.json` | 0 | 12.895 mục, **delta []**, HEAD/tree/băm spec không đổi. |

ADR-0055/0053/0060: cả ba neo đều có file tại land (rc0), cha thứ nhất chưa có (rc128), thuộc first-parent của `origin/master` trong mirror (rc0). Mirror không shallow. Đây là xác minh snapshot local, **không** khai remote vừa fetch. Drift lịch sử `889334fb→08bcb51f` đúng 1 tệp +698/−92; base→reviewed_sha không có numstat ở tập phụ thuộc đã lọc (`evidence/dependency-drift.txt`). S7 receipt thật khác S/C, S8 Windows/WSL, quota và holder live không đo lại.

Môi trường: Linux `6.18.44-fc-v242`, Python `3.13.18`, Git `2.43.0`. `evidence/measurements.json` có command, cwd, rc, output, thời gian từng phép; `ref-env-probe.log` (driver `ref_env_probe.py`, rc0) bổ sung ref thật và child thừa kế GIT_OBJECT_DIRECTORY; `class-scan.txt` giữ danh sách dòng memo/deadline/hoàn tất/reader/guard/đột biến để kiểm ngược phạm vi quét.

**Lỗi probe của reviewer được giữ, không đẩy thành finding:** lần CLI đầu gọi `record-codex-call` ngay sau init nhận rc8 vì state còn awaiting_lease; driver rc1, log `evidence/cli-setup-error.log`. Đã sửa setup bằng fixture reviewing **chỉ cho test**, chạy lại rc0. Phép đó không chứng minh đường cấp lease/transition thực tế, không tạo/ghi lại state của packet đang chạy, không tính các run ID giả lập vào ngân sách Codex thật.

**Toàn vẹn:** snapshot trước/sau bao gồm nội dung tracked/untracked/ignored ngoài `.git`, status, HEAD/tree, diff/index và refs: 12.895 mục bằng nhau. Chỉ chứng minh không có delta quan sát được tại hai mốc, không suy toàn lịch sử chưa từng ghi rồi hoàn nguyên. Không sửa kho review; mọi probe/object/state/bằng chứng mới ở sandbox, Python chạy `-B`/`PYTHONDONTWRITEBYTECODE=1`.

**Phần chưa đo:** implementation Git cuối và byte stdout CLI, timeout/kill-tree/RSS, Windows thật, full mutant audit CI, raw authority/journal/quota/remote live. Đây là nghĩa vụ pha thi công hoặc dữ liệu ngoài phiên; không biến thành pass. Không có finding P1/P3 mới đủ căn cứ. F19 P2 đủ để yêu cầu sửa r8; lượt cuối kết thúc ở đây và cần checkpoint theo chỉ thị, không tự mở lượt thứ chín.

TONG: P1=0 P2=1 P3=0
