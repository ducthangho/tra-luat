# Cross-review wp1179 C1a1b r5 — lượt 5

- reviewed_sha: `268137452ce1d9e21a4cc635eb9ad4ca7358b57d`
- spec_sha256: `746c0ef2204eafade6d17933a0050efb8205e9910cf9d82730fb0627f6d3fabd`
- reviewed_tree: `b7d6ada03c26090600ad754c90277969d065717a`
- base số đo: `889334fb87c25136a13c6776a40a25b401820e04`.
- provider: `openai_codex`; execution_surface: `codex_cli`; transport: `machine`, theo `../run/0b6aa6d7/run.json`; run_id `0b6aa6d79864429d95ed746b79d00558`.
- model/effort tự khai: Codex, thuộc họ GPT-6; mã model cụ thể và mức effort không được môi trường công bố.
- verdict: **`changes_requested`** — 0 P1 / 2 P2 / 1 P3. Hai lỗi mới ở A20b; còn một lệnh CLI bị sót trong §8.
- Phạm vi: review độc lập, cây `../cay-kho` chỉ đọc; mọi probe và kết quả ghi trong sandbox hiện tại.

## Nhật ký kiểm tra tăng dần

- Đã xác minh `git -C ../cay-kho rev-parse HEAD` và `sha256sum ../cay-kho/ops/specs/wp1179-c1a1b-r5.md`: rc=0, khớp cả hai giá trị trên.
- Đặc tả r5 có 709 dòng (`wc -l`, rc=0).
- Đã ghi tệp này theo tiến độ: preflight → F10–F12 và phản chứng F13/F14 → bảng lớp, F15, rà toàn bộ A1–A22 và kiểm tra cuối.
- Môi trường: Linux 6.18.44, Python 3.13.18, Git 2.43.0; mirror không shallow; `origin/master` trong snapshot là `d26b36f5d2f952c2d952d58517571ffe27c4f826`. Không fetch hay kiểm GitHub live.
- Model/effort phục vụ không suy từ dòng yêu cầu `gpt-6-astra/xhigh` trong spec. Metadata đang chạy chỉ xác nhận provider/surface/transport nêu trên; không tự nhận receipt terminal hoặc quyền merge.

## F10–F12

| ID | Lớp | Kết quả |
|---|---|---|
| F10 | dat-lai-ngan-sach-khi-doi-truc | ĐÃ VÁ THẬT: chỉ nâng U_lower, cap luôn bằng allowance; A21 8/14/15 đều cấp 3. |
| F11 | phan-loai-vang-va-khong-do-duoc | Tập chốt §2.3 đã bổ sung đủ; VÁ SINH LỖI MỚI ở oracle A20b cho G8 (F13) và yêu cầu đột biến (F14). |
| F12 | huong-dan-cli-khong-khop-parser | Hai biểu hiện tại §11.2 ĐÃ VÁ THẬT; **CHƯA VÁ hết lớp**: invocation init còn sót ở §8, F15. |

## Bảng lớp

| Slug lớp | Lịch sử / phạm vi đã quét | Mức mở | Kết luận, cách vá chung và phép đóng |
|---|---|---|---|
| `mo-rong-module-pha-hop-dong-json-thuan` | draft0–2, F3 phần ABI r1; §2.1–2.2, A1–A6 | — | Không tái mở. Module JSON nguyên byte; dict được bọc nguyên vẹn. Suite nền và ma trận ABI đã đo; kiểm import/CLI sản phẩm khi có implementation. |
| `phan-loai-vang-va-khong-do-duoc` | F4 r1, F6 r2, F11 r4; §2.3×G1–G9, A7/A10–A14/A20/A20b | **P2, F13** | Tập chốt parser đủ nhưng oracle mới lan lỗi sang G8 ngoài tập đọc. Sửa theo ma trận luật→đường→object; ca tree hỏng ở từng đường phải có đối chứng luật không liên quan. |
| `dot-bien-tuong-duong-hoac-thieu` | F3 r1, F7 r2; §4, A4/A5/A7–A9/A11/A13/A18/A20/A20b/A21 | **P2, F14** | ABI/A9/A18 vẫn có ca phân biệt; A20b ép giết mutant t2 tương đương. Áp disposition và nhóm chốt che nhau theo §5.0, audit trên mã cuối; không suy số killed từ số ID. |
| `oracle-trang-thai-g0-mau-thuan` | F8 r2; §2.2, A6/A13 | — | G0 luôn qua/do, chỉ G1–G9 không chạy khi JSON K1/K2 đỏ. Ma trận prototype không tái hiện lỗi cũ. |
| `predicate-consumer-khong-khop-producer` | F2 r1; G6/G7/G8, parser c1–c2/t1–t10 | — | Không thấy lệch mới trong tập chốt. G6 không đọc leaf; G7/G8 nhận symlink, so OID trước blob; chỗ chặt hơn producer và giới hạn provenance đã khai rõ. |
| `dat-lai-ngan-sach-khi-doi-truc` | F1 r1, F9 r3, F10 r4; §0/§7–§11, A21 | — | F10 đóng ở tầng spec. Bảy đường §0.6 và các đường ngoài danh sách không còn biến status thành upper; allowance không được gọi là số dư đã chứng minh. State thử limit 3 nhận 3 lời gọi, chặn lời thứ 4. |
| `huong-dan-cli-khong-khop-parser` | F12 r4; §0.6/§3/§8/§11.2/A21/A22 | **P3, F15** | Cặp lỗi §11.2 đã sửa; danh sách audit bỏ qua fragment init ở §8. Dùng một invocation đầy đủ hoặc định danh rõ chỉ là cặp cờ, dẫn tới §11.2; đối chiếu lại phạm vi A22. |
| `so-do-ke-thua-chua-do-lai` | F5 r1; §1, §2.6, §3, §9, §11.5 | — | Các số tái lập khớp. Số thời gian/máy, holder, receipt thật S≠C và quota có giới hạn thời điểm rõ, không nâng thành đo live. |
| `nguon-duoc-tin-ma-chua-xac-minh` | lịch sử C1a1a; reader, N6, §5/§6/§11 | — | Băm lại/type/đường đọc phân biệt được. Nguồn API caller và run provenance ngoài C1a1b; không dùng snapshot hoặc status làm bằng chứng đầy đủ. Không tuyên bố đóng lớp của toàn chuỗi thu hồi. |

**Đếm theo lớp:** 3 lớp mở / 3 finding mới; F13 và F14 là tái diễn lớp cũ, không đổi slug để xóa lịch sử. Tập lớp mở cuối r4 là {ngân sách, phân loại, CLI}; chỉ ngân sách đóng hết trong r5 ⇒ tỷ lệ đóng lớp **1/3**. F14 là lớp tái mở so với tập mở cuối r4, không đưa vào tử số. Điều kiện Q-NT vẫn chi phối pha spec hiện tại; verdict không tự cấp thêm lời gọi và không miễn checkpoint/trần của pha thi công.

## Kiểm độ đầy đủ của §0.6 và đối chiếu parser

**Ngân sách:** đã kiểm cả bảy đường liệt kê: quy tắc cấp §8; khối lease §8; phục hồi §11.1; bảng §11.1; A21; §10 điểm 8; đề xuất lịch sử F9. Quét thêm §0.3 Q-NS/F1, §0.5 Q-NT, §7 stop condition, §9 lịch sử và §11.2 init: không có đường hiện hành thứ tám gán số cho `U_max`. Công thức cũ chỉ xuất hiện dưới nhãn lịch sử, cấm dùng hoặc đột biến âm. Đổi pha không reset lịch sử packet; timeout có output/connector/state khác phải tiếp tục tăng lower. Ngoại lệ allowance là quyền được chỉ thị hiện tại giữ lại, không bị bác chỉ vì tổng thật có thể vượt 16.

**Parser:** tại base, `KhoObject.commit` dòng 1988–2000 và `KhoObject.tree` dòng 2002–2032 là chuẩn đối chiếu. Diff base→reviewed SHA của producer bằng 0. Tập chốt r5 khớp các guard nguồn sau, không thêm kiểm `.GIT`, thứ tự entry, UTF-8 nghiêm cho toàn commit, hay author/committer mà producer không áp:

| ID r5 | Chốt producer | Đo/kiểm trong lượt này |
|---|---|---|
| c1 | tree cuối đã parse/strip phải có và khớp SHA40 | Object thiếu tree và tree sai dạng đều E_hong; tree cuối hợp lệ sau dòng tree cũ sai được nhận như producer. |
| c2 | mọi parent đã parse trong header phải khớp SHA40 | Parent sai dạng E_hong; dòng giống parent trong message không được coi là header. |
| t1 | có NUL; đủ 20 byte OID | Đã chạy cả hai nhánh cụt, đều E_hong. |
| t2 | separator có mặt | Đã chạy mode hợp lệ/không hợp lệ không separator; guard có thật nhưng phụ thuộc t3/t5 (F14). |
| t3 | mode thuộc đúng 5 giá trị | Mode 100600 bị bác; đối chiếu tập nguồn trùng §2.3. |
| t4 | tên giải mã UTF-8 | Byte tên không UTF-8 bị bác. |
| t5 | tên không rỗng | Object băm đúng có tên rỗng bị bác; F11 trực tiếp được sửa. |
| t6, t7, t8 | tên khác dấu chỉ thư mục hiện tại/cha, không chứa dấu phân cách slash | Kiểm trực tiếp từng điều kiện trong nguồn; **không dựng payload**, chỉ mô tả hướng theo chỉ thị. Chưa chạy các ca bytes này. |
| t9 | tên khác đúng `.git` | `.git` bị bác, `.GIT` được nhận. Không checkout. |
| t10 | tên chưa có trong cùng tree | Tên trùng bị bác; tree sai thứ tự nhưng tên khác nhau được nhận. |

Đây là xác nhận **tập guard**, không phải chứng nhận parser C1a1b chưa viết. Phải giữ cách producer lấy header, `strip`, tree cuối thắng; không diễn giải c1 thành “bất kỳ dòng tree cũ nào sai cũng bác”. Các đường F11 thiếu trong r4 đều đã có ở §2.3, nhưng danh sách §0.6 chưa đủ để chứng minh bản vá đóng lớp: thiếu đối chiếu vị trí fixture với tập đọc của từng luật (F13), và thiếu quan hệ che giữa các chốt (F14).

**CLI:** §0.6 đã bao phủ các tên lệnh nhưng chưa mọi invocation: fragment init thứ hai ở §8 bị sót (F15). Trong §11.2, lệnh init đủ packet/mission/providers/limit chạy rc 0; record-codex-call đủ head/run-id chạy rc 0 khi fixture ở reviewing; rescue ID/URL đo ở đúng blocked/rescue_required cho rc 2/0. Lệnh status đọc lại limit 3. Limit 0 rc 2, bỏ limit ra mặc định 2. `record-rescue revision` rc 0 vẫn giữ state blocked, không được coi là đã mở lại pha. Setup đưa state giả vào reviewing được ghi rõ trong script; không tự khai đã replay lease/journal production.

## Finding mới

### F13 — P2 — `phan-loai-vang-va-khong-do-duoc`

Vị trí r5: A20b dòng 494; đối chiếu §2.3 dòng 288–301, §2.4 dòng 371–372, A20 dòng 493.

A20b đặt tree hỏng trong nhánh `ops/` của tree(C), nhưng đòi cả G7 và G8 `khong_do_duoc`. G8 chỉ đọc nhánh `.github/workflows/`; tree `ops/` không thuộc tập object cần của G8. Oracle mới đòi lan sự kiện sang một luật không đọc object đó, trái bảng đóng và chính mutant “lan sự kiện sang mọi luật” của A20.

Phép đo: `PYTHONDONTWRITEBYTECODE=1 python -B probes/graph_parser.py > evidence/graph-parser.txt 2>&1`, rc **0**. Reader prototype dùng đúng `KhoObject.commit/tree` của base, đọc/băm object thật trong clone shared scratch, không checkout tree hỏng. Đối chứng hợp lệ: G6/G7/G8/G4 đều `qua`. Tree tên rỗng `9eb7673e36a3bbfdf93c921bf8ab5b8e88199c6b` nằm ở `ops/`, commit `d6d278dbc2f40928dc0ac4cab6d3d31564d377d0`: **G6/G7 unknown, G8/G4 qua**. Chuyển lỗi sang `.github/workflows/`: **G8 unknown, G6/G7/G4 qua**. Đây là phản chứng tính nhất quán của spec, không phải kết quả chạy module C1a1b chưa tồn tại.

Đề xuất: tách ba vị trí fixture theo cột đọc: G6 → ops trong S; G7 → ops trong C; G8 → .github/workflows trong C. Với mỗi vị trí, khai đúng luật đích và luật không phụ thuộc giữ màu. Đồng bộ ví dụ t8 ở cuối A20b với vị trí fixture đã chọn; các ca có nội dung dạng thoát thư mục chỉ mô tả bằng lời trong review này.

Rủi ro khi vá: đặt lỗi vào root dùng chung rồi vẫn gọi G7 là “không liên quan” sẽ tạo oracle sai mới; phải chọn đối chứng theo object thật mà luật đọc, không theo tên ca.

### F14 — P2 — `dot-bien-tuong-duong-hoac-thieu`

Vị trí r5: A20b dòng 494 (“mười hai đột biến, mỗi đột biến bỏ đúng một chốt ⇒ đúng ca ... ĐỎ”); cùng cách nói ở §0.6 dòng 143 (“mutant bỏ từng chốt bị giết”); §4 dòng 460–464 dẫn hợp đồng disposition C1a1a §5.0.

Yêu cầu giết độc lập đủ 12 chốt không xử lý quan hệ che nhau. Với parser producer, t2 “không dấu cách” bị t3/t5 suy ra: `partition(b" ")` không tìm thấy separator thì tên luôn rỗng; mode ngoài tập bị t3 bác, mode trong tập bị t5 bác. Bỏ riêng `not sep` giữ nguyên kết quả `E_hong` cho mọi đầu vào. Đây là mutant tương đương đối với oracle màu luật, không thể giết bằng ca đúng như A20b yêu cầu; sự khác biệt chuỗi lý do không làm trạng thái đổi màu.

Cùng lệnh/probe trên, rc **0**: mutant literal bỏ `not sep or` khỏi bản sao producer; cả năm mode hợp lệ không separator đều `E_hong` trước/sau (sau do tên rỗng), ba token mode không hợp lệ đều `E_hong`; hai đối chứng hợp lệ vẫn nhận. Lập luận bao phủ toàn miền: có separator thì biểu thức đã bỏ là false; không có separator thì t3 hoặc t5 chắc chắn bác. Không tạo dữ liệu traversal.

Đề xuất: giữ đủ 12 ID nghĩa vụ nhưng dùng disposition của §5.0: t2 có thể `equivalent_verified` sau chứng minh/đo trên mã cuối; kiểm thêm nhóm chốt che nhau nếu cần witness vi phạm thực. Không tính mutant tương đương là đã giết, không ấn định 12 `witness_killed`; oracle căn cứ hành vi, không bắt khác câu thông báo lỗi. Rà lại mọi predicate ghép c1/c2/t1–t10 theo cùng cách trước thi công.

Rủi ro khi vá: không gắn nhãn equivalent hàng loạt từ prototype này; thay parser có thể thay quan hệ che. Mỗi disposition phải có lập luận và phép đo trên implementation cuối, và bỏ cả nhóm chốt không được suy tương đương từ việc bỏ từng chốt.

### F15 — P3 — `huong-dan-cli-khong-khop-parser`

**Vị trí:** §8 dòng **590–591**, §0.6 dòng **168–176**, A22 dòng **496**.

§8 vẫn viết ``packet_loop init --executor claude --reviewer codex`` “qua chốt cùng provider”. Nếu chạy invocation này, parser dừng trước chốt provider vì thiếu cả `--packet` và `--mission`. A22 lại nêu tường minh **mọi lệnh có đối số**, gồm **§8**, phải chạy được trên parser thật; §0.6 tuyên bố đã chạy từng lệnh. Sửa invocation §11.2 không sửa đường này. Đây là lỗi hướng dẫn/khẳng định phép đo, fail-closed nên P3; không phải lỗ cấp quyền.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probes/final_checks.py > evidence/final-checks.txt 2>&1`, rc script **0**. Chuẩn hóa duy nhất executable thành `python -B base/.claude/dev/packet_loop.py`, giữ nguyên đối số `init --executor claude --reviewer codex`, đặt state-dir trong sandbox: rc con **2**, stdout rỗng, stderr **`the following arguments are required: --packet, --mission`**. Cặp dương đầy đủ ở `evidence/metrics-cli.txt` rc **0**, status đọc limit **3**.

**Đề xuất cụ thể:** §8 dẫn tới lệnh hoàn chỉnh ở §11.2, hoặc ghi nguyên invocation có `--packet 1179 --mission 499 --codex-review-calls-limit 3` và cùng state-dir. Nếu chủ đích chỉ minh họa hai cờ provider, đổi câu thành “cặp cờ ... trong invocation §11.2 qua chốt provider”, không trình bày như lệnh đã chạy; đồng bộ §0.6/A22. Khóa bằng chạy đúng invocation được dẫn và đọc lại limit. Không chỉ thêm hai cờ bắt buộc rồi vô tình để mặc định limit 2, cũng không tự sửa state thật.

## Rà toàn bộ đặc tả và A1–A22

Các probe chỉ kiểm tính khả thi, phân biệt và nhất quán của **đặc tả**; module `.claude/dev/doc_receipt_thu_hoi_git.py` chưa tồn tại. Không lấy prototype làm nghiệm thu sản phẩm.

| Phạm vi | Kết quả / giới hạn |
|---|---|
| §2.1–§2.2, A1 | JSON cũ giữ nguyên bytes base→HEAD; blob `3490ea0ee40081c0eba2d121f5b19a67a021a54b`. Module mới/bọc nguyên dict không mở lại ABI JSON thuần. |
| A2 | Suite base thực: 156/156 ca, 162/162 mutant, equivalent 9, unresolved 0. Registry thật 29/29; cây giả thêm module vẫn 29/29; thêm test riêng 30/29 và lỗi đúng đường. |
| A3 | Gọi `kiem_json` thật với dương/K1/K2/K4: đúng vectơ luật và dict. Nghĩa vụ wrapper giữ nguyên dict được nêu rõ; chưa nghiệm thu import của module mới. |
| A4 | Ma trận a–e và mixed được dựng, outer ok là bool; serializer subprocess bằng đúng byte công thức. Bỏ sort đổi bytes; vế bỏ G hoặc bỏ JSON có đối chứng phân biệt. |
| A5 | Rc 12 ưu tiên 13, rc 0 iff ok, lỗi đầu vào/N6 đầu rc 2 không JSON nhất quán. Đã đo mô hình rc cho ma trận, chưa chạy CLI sản phẩm. Mỗi chốt tham số vẫn cần ca riêng, gồm check-ref-format sau regex. |
| A6 | K1/K2 đỏ dưới trần: G0 qua, G1–G9 không chạy; K4 đỏ vẫn cho G chạy. G0 quá trần cho json null. F8 không tái mở. |
| A7 | Clone shared trên MOC thật: C=B/MOC qua; P/E/X đỏ. Chuỗi đầy đủ không MOC đỏ; xóa commit scratch giữa chuỗi ra E_vang. G1 phải tiếp tục xác minh biên dù đã gặp C. |
| A8 | A≤B qua; B≤A đỏ; A≤X đỏ; bằng nhau qua. Ca strict ancestor phân biệt đảo toán hạng, không dùng nhánh rẽ làm witness duy nhất. |
| A9 | Đã dựng tree(S), tree(C), tree(H) đôi một khác. T=tree(S), tree_S=tree(H) phân biệt nguồn tree; guard fixture có yêu cầu ca chủ động trùng tree. Không thấy mutant tương đương mới tại đây. |
| A10 | G6 nhận OID cả năm mode ngay cả leaf vắng; không đọc leaf. Null/có/vắng và tổ tiên không-tree được phân loại riêng. Câu “bảy ô” là cách nhóm; hai giá trị null/hex ở hàng ancestor đều có ca, không dùng con số bảy cắt coverage. |
| A11 | F6 giữ đúng: 2 luật × 3 lỗi blob (missing/hash/type) × 2 quan hệ OID. Lệch → do và không đọc leaf; khớp → unknown do lỗi blob. Nhánh symlink/blob, gitlink/tree, sha256 có mệnh đề riêng; không chứng minh target Python đã chạy hoặc GitHub nạp symlink. |
| A12 | Đã đo loose object có hash sai bằng reader rehash; missing/type được phân biệt. Filter GIT_*, replace và framing có nghĩa vụ rõ, chưa chạy lại đầy đủ các ca replace/env/Windows của sản phẩm; kiểm code thi công vẫn cần thiết. |
| §2.6, A13 | Các giới hạn có đơn vị riêng và ca riêng; G1/G2/G3 per-walk, tổng byte mỗi object một lần, thời gian không vào ABI. 50.000 chỉ suy dư so với lịch sử master, không bảo đảm H ngoài master. G0 > chứ không ≥ 8 MiB. Timeout pipe/RSS/cold-cache/Windows chưa nghiệm thu; không dùng clock seam làm bằng chứng cho chúng. |
| N6, A14 | Ref thật trong scratch được đọc đúng tên rồi đổi/xóa; lần cuối có giá trị khác/vắng. Preflight rc 2 tách G9 unknown/rc 13; không có mâu thuẫn mới. Việc caller lấy tham số từ API vẫn là hợp đồng ngoài phạm vi. |
| §3, A15 | Hai đường write set, JSON/registry ngoài write set, trần ≤750 và yêu cầu dừng khi vượt giữ nguyên. ~710 là ước từ r2, có khai chưa đo; không coi số dòng prototype là số dòng implementation. |
| A16 | Windows required theo M3; tập trung hai nhóm và mutant suite, base/candidate cùng máy/cùng lệnh. Khi thi công vẫn phải lưu ID/kết quả từng test theo M3, không chỉ tổng. Windows local/CI: **not_run**. |
| A17 | M9 áp vì code tương lai chạm `.claude/dev/**`; full_mutant_audit Ubuntu hoặc owner waiver đúng scope còn bắt buộc. **not_run**, không miễn vì suite JSON xanh. |
| A18 | Smoke prototype giữ JSON thật, bản chép sổ, root tường minh và cờ tránh e2e đệ quy. Child dương rc 0, tổng 157/163 (Git giả 1/1). ImportError/SyntaxError/vắng module: rc 1 đúng tệp, không tổng. Mutant caller nuốt import bị TinHieuChotCa đúng tên g_dong_tong_e2e bắt. Tổng smoke không phải tổng sản phẩm. N_git=0 và M_git=0 vẫn là hai guard riêng trong spec. |
| A19 | doctrine-scan rc 0: 10 tệp, 0 vi phạm; adr-song rc 0: 64/64; git diff --check spec rc 0. Ruff hai tệp code ứng viên: **not_run** vì chưa có module mới; không ghi “Ruff passed”. |
| A20 | ID theo luật×E và disposition là cách phủ phù hợp. Phải tiếp tục dùng cột đọc làm chuẩn target/non-target; oracle A20b hiện đi ngược chốt này (F13). |
| A20b | Tập parser đủ, nhưng fixture G8 sai đường (F13) và ép killed cho mutant bị che (F14). Hai điều phải sửa trước triển khai. |
| A21 | U_lower=8/14/15, U_max unknown, cap đều 3. Readback limit 3; ba call rc 0, call thứ tư rc 3; limit 0 rc 2; bỏ cờ mặc định 2. Không gọi model trong các state thử. |
| A22 | Các cặp âm/dương §11.2 chạy đúng; chưa thỏa tuyên bố mọi invocation §8 (F15). |

**§2.3/G6/G7/G8:** missing entry trong tree đã xác minh là kết quả đo; object bắt buộc missing/hash/type/parser/framing là unknown. G6 leaf thuộc mọi mode hợp lệ không được đọc. G7/G8 chốt mode/OID trước blob. E không lan ra ngoài tập đọc; reader chết có thể ảnh hưởng các luật còn cần reader, không làm luật đã có đủ chứng cứ tự đỏ. Bảng đóng và thứ tự rc nhất quán ngoài oracle A20b đã báo.

**§8/§11 so với ADR-0043/0048/0052/0055 và protocol §12:** lời gọi, vòng hợp lệ và attempt vẫn là ba trục; nâng call 10→16 không tự nâng trục khác. Ba dòng opt-in mỗi dòng duy nhất, phép kiểm nguồn 0/128/0 khớp trên snapshot. Allowance 4/3 có đơn vị pha riêng và không khẳng định tổng ≤16 khi upper unknown; state chỉ đếm các call đã ghi, không tự làm sổ đầy đủ. Init phải truyền limit; dispatcher phải tính cả connector/output timeout. Q-NT thay lối human audit đóng băng spec, không xóa human audit exact head trước merge. Các đoạn Q-R/hai call cũ được đánh dấu lịch sử; điều kiện Rescue của pha thi công giữ nguyên. §11.2 đã khai đường replay Rescue production chưa đo, không giả mạo lịch sử bằng sửa state thật.

**Phạm vi còn lại:** N1–N8 đều có nơi chiếu; N4 được đáp ứng về ngữ nghĩa bằng đọc/băm/parse object thay cho suy từ rc của rev-parse. C1a1b chỉ kiểm nhất quán với C tự khai; C1a2/C1b/T2/Q17, #656/#564/#499, producer/registry và #1160 vẫn ngoài phạm vi. Không thấy điều khoản cho phép ok=true tự tạo quyền land.

## Đo lại số liệu

Lệnh chính: `PYTHONDONTWRITEBYTECODE=1 python -B probes/metrics_cli.py > evidence/metrics-cli.txt 2>&1`, rc **0**. Script chép nguồn theo exact base, ghim TMPDIR và bytecode trong sandbox; lệnh con và rc/output có trong log.

| Số đo | Kết quả lần này | Nhận định |
|---|---|---|
| S2 first-parent MOC^..base | 411; reader 410 commit / 531.751 byte / 0,030 s | Khớp, reader không đọc MOC. |
| S3 mọi tổ tiên base | 5.444 / 8.480.418 byte / 0,366 s | Khớp số lượng/bytes; thời gian chỉ máy/bộ đệm lượt này. |
| S4 | first-parent 1.084; ngoài first-parent 4.360; log checker 64; giao 64 | Khớp. |
| S5 | 2 tệp, +650/−93 (workflow +1/−1; producer +649/−92) | Khớp. |
| S6 | 156/156 ca; 162/162 killed; equivalent 9; unresolved 0; rc 0; 11,994 s | Đã chạy suite thật trên bytes base. |
| §2.6 tỷ lệ | 50.000/5.444 ≈9,184 lần; ngoại suy ≈77,89 MB | Chỉ ước từ profile, không là phép đo H/RSS. |
| §3 suite nền | 535 dòng | Khớp. Kích thước thi công chưa tồn tại nên chưa đo. |
| §11.5 base→08bcb51f | 1 tệp .githooks/eol_policy_test.py, +698/−92 | Khớp. Tập phụ thuộc code/protocol đã kiểm base→HEAD không có delta. |
| Hash spec/verdict lịch sử | Các băm r2/r3/r4, verdict r1–r4 khớp các giá trị được dẫn | Log final-checks ghi hash đầy đủ. |
| Các opt-in ADR-0055/0053/0060 | Có tại L rc 0; vắng ở L^ rc 128; L thuộc first-parent origin/master | Đạt trên mirror; không thay freshness live trước lease. |

S7 receipt thật S≠C, S8 Windows/WSL, cold-cache, quota/reservation, journal dispatcher cũ, holder hiện hành và nguồn comment GitHub **không đo mới**. Không lấy số lịch sử 776 refs/holder làm readback hiện tại. Quyền review và các quyết định được giữ lấy từ chỉ thị người dùng; không giả nhận đã kiểm live authority.

## Hồ sơ chạy và giới hạn

| Script | Rc cuối | Log |
|---|---:|---|
| `probes/metrics_cli.py` | 0 | [metrics-cli](evidence/metrics-cli.txt), [suite JSON](evidence/json-baseline.txt) |
| `probes/graph_parser.py` | 0 | [graph-parser](evidence/graph-parser.txt), [OID đồ thị](evidence/graph-ids.json) |
| `probes/acceptance.py` | 0 | [ABI/registry/A18](evidence/acceptance.txt) |
| `probes/final_checks.py` | 0 | [gate/CLI/hash/snapshot](evidence/final-checks.txt) |

Các rc âm 1/2/3/8/128 của lệnh con là kết quả phản chứng có chủ ý, đã tách khỏi rc script; không gọi chúng là product pass. Không chạy toàn bộ test sản phẩm mới, fullCI, Windows hoặc holder live. Các ca t6–t8 chỉ đối chiếu nguồn, không soạn nội dung dạng thoát thư mục. Đã đọc skill cloud-environment-runtime; phiên không có tool environment_status, không sử dụng mạng hoặc suy readiness từ đó.

[Manifest SHA-256 của các script probe](evidence/probe-manifest.sha256). Các probe tự cấp thư mục scratch mới khi chạy lại; không sửa hoặc tái dùng state production.

Snapshot đầu/cuối gồm HEAD/tree, index hash, status tracked/untracked/ignored và SHA-256 nội dung **12.842 tệp** trong working tree (symlink băm chính chuỗi đích). Hai snapshot bằng nhau hoàn toàn: [đầu](evidence/snapshot-start.json), [cuối](evidence/snapshot-end.json). `.git/objects` và mọi thời điểm trung gian không thuộc manifest nội dung; snapshot không chứng minh chưa từng ghi rồi hoàn nguyên. Mọi script/state/clone/prototype/output được tạo ở sandbox; dùng Python -B và PYTHONDONTWRITEBYTECODE=1. Không sửa cây đang review, không gọi thêm model/connector, không cấp lease, push, merge hay land.

**Kết luận:** cần sửa F13, F14, F15 để có thể đạt một lượt 0/0/0. Bản này chưa đủ điều kiện approve hoặc đóng băng spec.

TONG: P1=0 P2=2 P3=1
